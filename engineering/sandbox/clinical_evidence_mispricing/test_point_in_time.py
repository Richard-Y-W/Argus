import pandas as pd
import pytest

from .point_in_time import (
    Announcement,
    PublicRecordVersion,
    TradingSession,
    build_point_in_time_event,
    effective_trading_session,
    latest_public_version,
    market_adjusted_car,
)


def _sessions() -> list[TradingSession]:
    return [
        TradingSession("2024-01-02", "2024-01-02 14:30Z", "2024-01-02 21:00Z"),
        TradingSession("2024-01-03", "2024-01-03 14:30Z", "2024-01-03 21:00Z"),
    ]


def _version(posted_at: str, enrollment: int) -> PublicRecordVersion:
    return PublicRecordVersion(
        "NCT00000001",
        posted_at,
        {"enrollment": enrollment},
        f"https://example.test/history/{enrollment}",
    )


def test_timestamps_must_be_timezone_aware() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        _version("2024-01-01 12:00", 100)


def test_latest_public_version_excludes_future_updates() -> None:
    versions = [
        _version("2023-12-01 12:00Z", 100),
        _version("2024-01-01 12:00Z", 120),
        _version("2024-01-04 12:00Z", 999),
    ]
    selected = latest_public_version(
        versions,
        entity_id="NCT00000001",
        decision_at="2024-01-03 13:00Z",
    )
    assert selected.payload["enrollment"] == 120


def test_latest_public_version_fails_when_history_starts_after_event() -> None:
    with pytest.raises(ValueError, match="no public"):
        latest_public_version(
            [_version("2024-01-04 12:00Z", 999)],
            entity_id="NCT00000001",
            decision_at="2024-01-03 13:00Z",
        )


@pytest.mark.parametrize(
    ("timestamp", "expected"),
    [
        ("2024-01-02 13:00Z", "2024-01-02"),
        ("2024-01-02 16:00Z", "2024-01-02"),
        ("2024-01-02 22:00Z", "2024-01-03"),
    ],
)
def test_effective_session_respects_after_hours(timestamp: str, expected: str) -> None:
    assert effective_trading_session(timestamp, _sessions()) == pd.Timestamp(expected)


def test_point_in_time_event_binds_snapshot_and_session() -> None:
    event = build_point_in_time_event(
        Announcement(
            "EVT-001",
            "NCT00000001",
            "2024-01-02 22:00Z",
            "https://example.test/announcement",
        ),
        [
            _version("2024-01-01 12:00Z", 120),
            _version("2024-01-04 12:00Z", 999),
        ],
        _sessions(),
    )
    assert event["event_session"] == pd.Timestamp("2024-01-03")
    assert event["trial_payload"]["enrollment"] == 120


def test_market_adjusted_car_uses_session_relative_window() -> None:
    index = pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"])
    asset = pd.Series([0.01, 0.10, 0.03, -0.01], index=index)
    benchmark = pd.Series([0.00, 0.02, 0.01, 0.00], index=index)
    assert market_adjusted_car(
        asset,
        benchmark,
        event_session="2024-01-03",
        start=0,
        end=1,
    ) == pytest.approx(0.10)


def test_market_adjusted_car_rejects_misaligned_returns() -> None:
    asset = pd.Series([0.01], index=pd.to_datetime(["2024-01-02"]))
    benchmark = pd.Series([0.01], index=pd.to_datetime(["2024-01-03"]))
    with pytest.raises(ValueError, match="identical indexes"):
        market_adjusted_car(
            asset,
            benchmark,
            event_session="2024-01-02",
            start=0,
            end=0,
        )
