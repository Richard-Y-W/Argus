from __future__ import annotations

import pandas as pd
import pytest

from .crsp_ciz_gate import (
    DAILY_COLUMN_ALIASES,
    audit_return_coverage,
    build_security_link_query,
    resolve_columns,
    validate_security_link,
)


def test_build_security_link_query_is_return_blind_and_deterministic() -> None:
    columns = {
        "permno": "PERMNO",
        "permco": "PERMCO",
        "ticker": "TickerSymbol",
        "issuer_name": "IssuerNm",
        "start_date": "SecInfoStartDt",
        "end_date": "SecInfoEndDt",
    }
    query = build_security_link_query(
        table="crsp.stkSecurityInfoHist",
        columns=columns,
        tickers=["VTL", "TORC", "VTL"],
        start_date="2017-01-01",
        end_date="2019-12-31",
    )
    assert "DlyRet" not in query
    assert "'TORC', 'VTL'" in query
    assert "SecInfoEndDt >= '2017-01-01'" in query


def test_build_security_link_query_rejects_unsafe_ticker() -> None:
    columns = {
        "permno": "permno",
        "permco": "permco",
        "ticker": "ticker",
        "issuer_name": "issuernm",
        "start_date": "startdt",
        "end_date": "enddt",
    }
    with pytest.raises(ValueError, match="unsafe"):
        build_security_link_query(
            table="crsp.history",
            columns=columns,
            tickers=["TORC'); DROP TABLE x;--"],
            start_date="2017-01-01",
            end_date="2019-12-31",
        )


def test_resolve_columns_accepts_official_ciz_names_case_insensitively() -> None:
    available = [
        "PERMNO",
        "DlyCalDt",
        "DlyRet",
        "DlyPrc",
        "DlyCap",
        "DlyDelFlg",
        "DlyRetMissFlg",
    ]
    result = resolve_columns(available, DAILY_COLUMN_ALIASES)
    assert result["return"] == "DlyRet"
    assert result["delisting_flag"] == "DlyDelFlg"


def test_validate_security_link_requires_event_time_name_and_ticker() -> None:
    candidates = pd.DataFrame(
        [
            {
                "permno": 12345,
                "ticker": "AXON",
                "issuer_name": "Axovant Sciences Ltd",
                "start_date": "2015-01-01",
                "end_date": "2018-05-01",
            },
            {
                "permno": 99999,
                "ticker": "AXON",
                "issuer_name": "Axon Enterprise Inc",
                "start_date": "2018-05-02",
                "end_date": "2030-01-01",
            },
        ]
    )
    assert (
        validate_security_link(
            event_ticker="AXON",
            sponsor_name="Axovant Sciences Ltd",
            announcement_date="2017-09-26",
            candidates=candidates,
        )
        == 12345
    )


def _returns(calendar: pd.DatetimeIndex, end: int, *, delist: bool) -> pd.DataFrame:
    frame = pd.DataFrame(
        {
            "date": calendar[:end],
            "return": 0.0,
            "delisting_flag": "N",
            "missing_return_flag": "NA",
        }
    )
    if delist:
        frame.loc[frame.index[-1], "delisting_flag"] = "Y"
        frame.loc[frame.index[-1], "return"] = -0.35
    return frame


def test_coverage_accepts_explicit_delisting_return_before_day_100() -> None:
    calendar = pd.bdate_range("2015-01-01", periods=500)
    event_date = calendar[300].date().isoformat()
    result = audit_return_coverage(
        announcement_date=event_date,
        security_returns=_returns(calendar, 350, delist=True),
        trading_calendar=calendar,
    )
    assert result.complete
    assert result.terminal_delisting


def test_coverage_rejects_unexplained_post_event_truncation() -> None:
    calendar = pd.bdate_range("2015-01-01", periods=500)
    event_date = calendar[300].date().isoformat()
    result = audit_return_coverage(
        announcement_date=event_date,
        security_returns=_returns(calendar, 350, delist=False),
        trading_calendar=calendar,
    )
    assert not result.complete
    assert "truncates" in result.reason


def test_coverage_rejects_short_estimation_history() -> None:
    calendar = pd.bdate_range("2015-01-01", periods=300)
    returns = pd.DataFrame(
        {
            "date": calendar,
            "return": 0.0,
            "delisting_flag": "N",
            "missing_return_flag": "NA",
        }
    )
    result = audit_return_coverage(
        announcement_date=calendar[100].date().isoformat(),
        security_returns=returns,
        trading_calendar=calendar,
    )
    assert not result.complete
    assert "pre-event" in result.reason


def test_missing_delisting_return_is_rejected() -> None:
    calendar = pd.bdate_range("2015-01-01", periods=500)
    event_date = calendar[300].date().isoformat()
    returns = _returns(calendar, 350, delist=True)
    returns.loc[returns.index[-1], "return"] = None
    returns.loc[returns.index[-1], "missing_return_flag"] = "MV"
    result = audit_return_coverage(
        announcement_date=event_date,
        security_returns=returns,
        trading_calendar=calendar,
    )
    assert not result.complete
