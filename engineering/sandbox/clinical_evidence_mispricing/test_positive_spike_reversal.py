import pandas as pd
import pytest

from .positive_spike_reversal import (
    ReversalEventResult,
    build_results,
    calculate_event_reversal,
    summarize_reversal,
)


def _prices(values: list[float]) -> pd.Series:
    return pd.Series(values, index=pd.bdate_range("2024-01-01", periods=len(values)))


def test_event_on_weekend_maps_to_next_trading_session() -> None:
    stock = _prices([100, 100, 110, 105, 104, 103, 102, 101])
    benchmark = _prices([100] * 8)
    result = calculate_event_reversal(
        event_id="E1",
        ticker="BIO",
        event_date="2024-01-06",
        stock_prices=stock,
        benchmark_prices=benchmark,
        initial_end_offset=1,
        exit_offset=2,
    )
    assert result.event_session == pd.Timestamp("2024-01-08").date()


def test_short_return_is_negative_future_abnormal_return() -> None:
    result = ReversalEventResult(
        event_id="E1",
        ticker="BIO",
        event_session=pd.Timestamp("2024-01-02").date(),
        initial_abnormal_return=0.10,
        future_abnormal_return=-0.08,
    )
    assert result.eligible
    assert result.gross_short_abnormal_return == pytest.approx(0.08)


def test_frozen_rule_requires_breadth_and_cost_survival() -> None:
    results = [
        ReversalEventResult(
            event_id=f"E{index}",
            ticker="BIO",
            event_session=pd.Timestamp("2024-01-02").date(),
            initial_abnormal_return=0.01,
            future_abnormal_return=-0.02,
        )
        for index in range(8)
    ]
    summary = summarize_reversal(results)
    assert summary["positive_fraction"] == 1.0
    assert summary["mean_after_fixed_cost"] == pytest.approx(0.015)
    assert summary["passes_frozen_sandbox_rule"]


def test_build_results_excludes_negative_events_and_maps_bms() -> None:
    prices = _prices([100 + index for index in range(30)])
    events = [
        {
            "event_id": "P",
            "event_date": "2024-01-02",
            "ticker": "BMS",
            "outcome": "positive",
        },
        {
            "event_id": "N",
            "event_date": "2024-01-02",
            "ticker": "BMS",
            "outcome": "negative",
        },
    ]
    results = build_results(events, {"BMY": prices}, prices)
    assert len(results) == 1
    assert results[0].ticker == "BMY"
