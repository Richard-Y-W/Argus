"""Simple session-relative abnormal returns for sandbox data-feasibility checks."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from statistics import mean, median, stdev
from typing import Sequence

import pandas as pd

from .positive_spike_reversal import _clean_prices


@dataclass(frozen=True)
class EventWindowReturn:
    event_id: str
    ticker: str
    outcome: str
    start_session: str
    end_session: str
    abnormal_return: float


def calculate_window(
    *,
    event_id: str,
    ticker: str,
    outcome: str,
    event_date: str,
    stock_prices: pd.Series,
    benchmark_prices: pd.Series,
    start_offset: int,
    end_offset: int,
) -> EventWindowReturn:
    if start_offset >= end_offset:
        raise ValueError("start offset must precede end offset")
    stock = _clean_prices(stock_prices)
    benchmark = _clean_prices(benchmark_prices)
    common = stock.index.intersection(benchmark.index).sort_values()
    event_position = int(common.searchsorted(pd.Timestamp(event_date).normalize()))
    start_position = event_position + start_offset
    end_position = event_position + end_offset
    if event_position >= len(common) or start_position < 0 or end_position >= len(common):
        raise ValueError("insufficient event-window prices")
    start_session = common[start_position]
    end_session = common[end_position]
    stock_return = stock.loc[end_session] / stock.loc[start_session] - 1
    benchmark_return = benchmark.loc[end_session] / benchmark.loc[start_session] - 1
    return EventWindowReturn(
        event_id=event_id,
        ticker=ticker,
        outcome=outcome,
        start_session=start_session.date().isoformat(),
        end_session=end_session.date().isoformat(),
        abnormal_return=float(stock_return - benchmark_return),
    )


def summarize(values: Sequence[float]) -> dict[str, float | int]:
    if not values:
        raise ValueError("cannot summarize an empty sample")
    count = len(values)
    average = mean(values)
    standard_error = stdev(values) / sqrt(count) if count > 1 else float("nan")
    return {
        "events": count,
        "mean": average,
        "median": median(values),
        "positive_fraction": sum(value > 0 for value in values) / count,
        "t_interval_low": average - 1.96 * standard_error,
        "t_interval_high": average + 1.96 * standard_error,
    }
