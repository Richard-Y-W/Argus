from __future__ import annotations

import pandas as pd
import pytest

from .event_path_smoke import calculate_window, summarize


def test_calculate_window_uses_first_session_on_or_after_event() -> None:
    dates = pd.bdate_range("2024-01-01", periods=10)
    stock = pd.Series([100, 100, 100, 100, 100, 110, 110, 110, 110, 110], index=dates)
    benchmark = pd.Series(100.0, index=dates)

    result = calculate_window(
        event_id="E1",
        ticker="ABC",
        outcome="negative",
        event_date="2024-01-06",
        stock_prices=stock,
        benchmark_prices=benchmark,
        start_offset=-2,
        end_offset=1,
    )

    assert result.start_session == "2024-01-04"
    assert result.end_session == "2024-01-09"
    assert result.abnormal_return == pytest.approx(0.10)


def test_calculate_window_rejects_reversed_offsets() -> None:
    prices = pd.Series([100, 101], index=pd.bdate_range("2024-01-01", periods=2))
    with pytest.raises(ValueError, match="precede"):
        calculate_window(
            event_id="E1",
            ticker="ABC",
            outcome="positive",
            event_date="2024-01-01",
            stock_prices=prices,
            benchmark_prices=prices,
            start_offset=1,
            end_offset=0,
        )


def test_summarize_reports_fraction_and_interval() -> None:
    result = summarize([0.10, -0.05, 0.20])
    assert result["events"] == 3
    assert result["mean"] == pytest.approx(1 / 12)
    assert result["positive_fraction"] == pytest.approx(2 / 3)
