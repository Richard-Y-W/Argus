"""Point-in-time guards for the clinical-evidence pricing sandbox.

These utilities establish timing semantics only. They do not create a research
result and must not be used to describe a return relationship as evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


def _utc(value: Any, *, field: str) -> pd.Timestamp:
    timestamp = pd.Timestamp(value)
    if timestamp.tzinfo is None:
        raise ValueError(f"{field} must be timezone-aware")
    return timestamp.tz_convert("UTC")


@dataclass(frozen=True)
class PublicRecordVersion:
    entity_id: str
    published_at: pd.Timestamp
    payload: Mapping[str, Any]
    source_url: str

    def __post_init__(self) -> None:
        if not self.entity_id.strip():
            raise ValueError("entity_id must be non-empty")
        if not self.source_url.strip():
            raise ValueError("source_url must be non-empty")
        object.__setattr__(
            self,
            "published_at",
            _utc(self.published_at, field="published_at"),
        )


@dataclass(frozen=True)
class Announcement:
    event_id: str
    entity_id: str
    available_at: pd.Timestamp
    source_url: str

    def __post_init__(self) -> None:
        if not self.event_id.strip() or not self.entity_id.strip():
            raise ValueError("event_id and entity_id must be non-empty")
        if not self.source_url.strip():
            raise ValueError("source_url must be non-empty")
        object.__setattr__(
            self,
            "available_at",
            _utc(self.available_at, field="available_at"),
        )


@dataclass(frozen=True)
class TradingSession:
    label: pd.Timestamp
    opens_at: pd.Timestamp
    closes_at: pd.Timestamp

    def __post_init__(self) -> None:
        label = pd.Timestamp(self.label).normalize().tz_localize(None)
        opens_at = _utc(self.opens_at, field="opens_at")
        closes_at = _utc(self.closes_at, field="closes_at")
        if opens_at >= closes_at:
            raise ValueError("session open must precede session close")
        object.__setattr__(self, "label", label)
        object.__setattr__(self, "opens_at", opens_at)
        object.__setattr__(self, "closes_at", closes_at)


def latest_public_version(
    versions: Iterable[PublicRecordVersion],
    *,
    entity_id: str,
    decision_at: Any,
) -> PublicRecordVersion:
    """Return the latest version public by the decision timestamp."""
    cutoff = _utc(decision_at, field="decision_at")
    eligible = sorted(
        (
            version
            for version in versions
            if version.entity_id == entity_id and version.published_at <= cutoff
        ),
        key=lambda version: version.published_at,
    )
    if not eligible:
        raise ValueError(f"no public {entity_id} version exists by {cutoff.isoformat()}")
    timestamps = [version.published_at for version in eligible]
    if len(timestamps) != len(set(timestamps)):
        raise ValueError(f"duplicate publication timestamps for {entity_id}")
    return eligible[-1]


def effective_trading_session(
    available_at: Any,
    sessions: Sequence[TradingSession],
) -> pd.Timestamp:
    """Map a public timestamp to the first session whose close has not passed."""
    timestamp = _utc(available_at, field="available_at")
    ordered = sorted(sessions, key=lambda session: session.opens_at)
    if not ordered:
        raise ValueError("at least one trading session is required")
    for previous, current in zip(ordered, ordered[1:]):
        if previous.closes_at >= current.opens_at:
            raise ValueError("trading sessions overlap or are unordered")
    for session in ordered:
        if timestamp <= session.closes_at:
            return session.label
    raise ValueError("announcement occurs after the supplied trading calendar")


def build_point_in_time_event(
    announcement: Announcement,
    versions: Iterable[PublicRecordVersion],
    sessions: Sequence[TradingSession],
) -> dict[str, Any]:
    """Bind an announcement to only the evidence public at that timestamp."""
    version = latest_public_version(
        versions,
        entity_id=announcement.entity_id,
        decision_at=announcement.available_at,
    )
    session = effective_trading_session(announcement.available_at, sessions)
    return {
        "event_id": announcement.event_id,
        "entity_id": announcement.entity_id,
        "available_at": announcement.available_at,
        "event_session": session,
        "trial_version_published_at": version.published_at,
        "trial_payload": dict(version.payload),
        "announcement_source_url": announcement.source_url,
        "trial_source_url": version.source_url,
    }


def market_adjusted_car(
    asset_returns: pd.Series,
    benchmark_returns: pd.Series,
    *,
    event_session: Any,
    start: int,
    end: int,
) -> float:
    """Sum daily asset-minus-benchmark returns over session-relative bounds."""
    if start > end:
        raise ValueError("start must not exceed end")
    if not asset_returns.index.equals(benchmark_returns.index):
        raise ValueError("asset and benchmark returns must have identical indexes")
    if not asset_returns.index.is_unique or not asset_returns.index.is_monotonic_increasing:
        raise ValueError("return index must be unique and increasing")
    if asset_returns.isna().any() or benchmark_returns.isna().any():
        raise ValueError("returns must not contain missing values")

    label = pd.Timestamp(event_session).normalize().tz_localize(None)
    try:
        location = asset_returns.index.get_loc(label)
    except KeyError as exc:
        raise ValueError("event session is absent from return index") from exc
    if not isinstance(location, int):
        raise ValueError("event session must identify one observation")
    left = location + start
    right = location + end
    if left < 0 or right >= len(asset_returns):
        raise ValueError("event window exceeds available returns")
    abnormal = asset_returns.iloc[left : right + 1] - benchmark_returns.iloc[left : right + 1]
    return float(abnormal.sum())
