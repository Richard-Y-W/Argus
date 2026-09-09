"""CRSP CIZ schema and event-coverage gates for the failure reconstruction.

CRSP CIZ daily total returns incorporate delisting returns. A security that ends
before day +100 is complete only when its terminal record is explicitly marked
as a delisting record with a usable total return.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import os
import re
from typing import Iterable, Mapping, Sequence

import pandas as pd


HISTORY_COLUMN_ALIASES: Mapping[str, tuple[str, ...]] = {
    "permno": ("permno",),
    "permco": ("permco",),
    "ticker": ("ticker", "tickersymbol", "tradingsymbol"),
    "issuer_name": ("issuernm", "comnam"),
    "start_date": ("secinfostartdt", "namedt"),
    "end_date": ("secinfoenddt", "nameenddt"),
}
DAILY_COLUMN_ALIASES: Mapping[str, tuple[str, ...]] = {
    "permno": ("permno",),
    "date": ("dlycaldt", "date"),
    "return": ("dlyret", "ret"),
    "price": ("dlyprc", "prc"),
    "market_cap": ("dlycap",),
    "delisting_flag": ("dlydelflg",),
    "missing_return_flag": ("dlyretmissflg",),
}


@dataclass(frozen=True)
class CoverageAudit:
    event_session: date
    pre_event_sessions: int
    post_event_sessions: int
    terminal_delisting: bool
    complete: bool
    reason: str


def credential_status() -> dict[str, bool]:
    return {
        "wrds_package_installed": _wrds_installed(),
        "wrds_username_configured": bool(os.environ.get("WRDS_USERNAME")),
    }


def _wrds_installed() -> bool:
    try:
        import wrds  # noqa: F401
    except ImportError:
        return False
    return True


def resolve_columns(
    available: Iterable[str], aliases: Mapping[str, Sequence[str]]
) -> dict[str, str]:
    normalized = {column.lower(): column for column in available}
    resolved = {}
    for semantic_name, candidates in aliases.items():
        match = next((normalized[name] for name in candidates if name in normalized), None)
        if match is None:
            raise ValueError(f"missing CRSP column for {semantic_name}")
        resolved[semantic_name] = match
    return resolved


def build_security_link_query(
    *,
    table: str,
    columns: Mapping[str, str],
    tickers: Sequence[str],
    start_date: str,
    end_date: str,
) -> str:
    """Build the return-blind security-history query after schema discovery.

    SQL identifiers and literals are deliberately restricted because WRDS's
    ``raw_sql`` API does not expose a portable parameter style across versions.
    """
    required = {"permno", "permco", "ticker", "issuer_name", "start_date", "end_date"}
    if not required.issubset(columns):
        raise ValueError("security-history columns are incomplete")
    identifiers = [table, *(columns[name] for name in required)]
    if any(not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.]*", item) for item in identifiers):
        raise ValueError("unsafe SQL identifier")
    clean_tickers = sorted({ticker.upper() for ticker in tickers})
    if not clean_tickers or any(
        not re.fullmatch(r"[A-Z0-9.-]+", ticker) for ticker in clean_tickers
    ):
        raise ValueError("unsafe or empty ticker set")
    start = pd.Timestamp(start_date).date().isoformat()
    end = pd.Timestamp(end_date).date().isoformat()
    if start > end:
        raise ValueError("start_date follows end_date")
    ticker_literals = ", ".join(f"'{ticker}'" for ticker in clean_tickers)
    selected = ", ".join(
        f"{columns[name]} AS {name}"
        for name in ("permno", "permco", "ticker", "issuer_name", "start_date", "end_date")
    )
    return (
        f"SELECT {selected} FROM {table} "
        f"WHERE UPPER({columns['ticker']}) IN ({ticker_literals}) "
        f"AND {columns['end_date']} >= '{start}' "
        f"AND {columns['start_date']} <= '{end}'"
    )


def validate_security_link(
    *,
    event_ticker: str,
    sponsor_name: str,
    announcement_date: str,
    candidates: pd.DataFrame,
) -> int:
    required = {"permno", "ticker", "issuer_name", "start_date", "end_date"}
    if not required.issubset(candidates.columns):
        raise ValueError("link candidates lack normalized columns")
    target = pd.Timestamp(announcement_date)
    rows = candidates.copy()
    rows["start_date"] = pd.to_datetime(rows["start_date"])
    rows["end_date"] = pd.to_datetime(rows["end_date"])
    rows = rows[
        rows["ticker"].str.upper().eq(event_ticker.upper())
        & rows["start_date"].le(target)
        & rows["end_date"].ge(target)
    ]
    sponsor_root = sponsor_name.split()[0].lower()
    rows = rows[rows["issuer_name"].str.lower().str.contains(sponsor_root, regex=False)]
    permnos = rows["permno"].drop_duplicates().tolist()
    if len(permnos) != 1:
        raise ValueError(f"expected one event-time PERMNO, found {len(permnos)}")
    return int(permnos[0])


def audit_return_coverage(
    *,
    announcement_date: str,
    security_returns: pd.DataFrame,
    trading_calendar: Sequence[pd.Timestamp],
    estimation_sessions: int = 252,
    post_sessions: int = 100,
) -> CoverageAudit:
    required = {"date", "return", "delisting_flag", "missing_return_flag"}
    if not required.issubset(security_returns.columns):
        raise ValueError("return data lack normalized columns")
    calendar = pd.DatetimeIndex(pd.to_datetime(trading_calendar)).tz_localize(None).normalize()
    calendar = calendar.drop_duplicates().sort_values()
    event_position = int(calendar.searchsorted(pd.Timestamp(announcement_date)))
    if event_position >= len(calendar):
        raise ValueError("announcement follows trading calendar")
    event_session = calendar[event_position]

    returns = security_returns.copy()
    returns["date"] = pd.to_datetime(returns["date"]).dt.tz_localize(None).dt.normalize()
    returns = returns.sort_values("date").drop_duplicates("date", keep=False)
    before = returns[returns["date"] < event_session]
    through_target = calendar[min(event_position + post_sessions, len(calendar) - 1)]
    after = returns[(returns["date"] >= event_session) & (returns["date"] <= through_target)]
    pre_count = len(before.tail(estimation_sessions))
    post_count = len(after)
    full_post = post_count >= post_sessions + 1

    terminal_delisting = False
    if not after.empty:
        terminal = after.iloc[-1]
        terminal_delisting = (
            str(terminal["delisting_flag"]).upper() == "Y"
            and pd.notna(terminal["return"])
            and str(terminal["missing_return_flag"]).upper() in {"", "NA", "NAN", "NONE"}
        )
    complete = pre_count >= estimation_sessions and (full_post or terminal_delisting)
    if pre_count < estimation_sessions:
        reason = "insufficient pre-event estimation history"
    elif full_post:
        reason = "full +100-session history"
    elif terminal_delisting:
        reason = "terminal delisting-inclusive return before +100"
    else:
        reason = "post-event history truncates without a usable delisting return"
    return CoverageAudit(
        event_session=event_session.date(),
        pre_event_sessions=pre_count,
        post_event_sessions=post_count,
        terminal_delisting=terminal_delisting,
        complete=complete,
        reason=reason,
    )
