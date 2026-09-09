"""Frozen exploratory short-after-positive-reaction calculation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from math import sqrt
from statistics import mean, median, stdev
from typing import Mapping, Sequence

import pandas as pd


@dataclass(frozen=True)
class ReversalEventResult:
    event_id: str
    ticker: str
    event_session: date
    initial_abnormal_return: float
    future_abnormal_return: float

    @property
    def eligible(self) -> bool:
        return self.initial_abnormal_return > 0

    @property
    def gross_short_abnormal_return(self) -> float:
        return -self.future_abnormal_return


def _clean_prices(prices: pd.Series) -> pd.Series:
    series = prices.copy()
    series.index = pd.to_datetime(series.index).tz_localize(None).normalize()
    series = pd.to_numeric(series, errors="raise").dropna().sort_index()
    if series.index.has_duplicates:
        raise ValueError("price index contains duplicate sessions")
    if (series <= 0).any():
        raise ValueError("prices must be positive")
    return series


def calculate_event_reversal(
    *,
    event_id: str,
    ticker: str,
    event_date: str,
    stock_prices: pd.Series,
    benchmark_prices: pd.Series,
    initial_end_offset: int = 1,
    exit_offset: int = 20,
) -> ReversalEventResult:
    stock = _clean_prices(stock_prices)
    benchmark = _clean_prices(benchmark_prices)
    common = stock.index.intersection(benchmark.index).sort_values()
    target = pd.Timestamp(event_date).normalize()
    positions = common.searchsorted(target)
    if positions >= len(common):
        raise ValueError("event follows available prices")
    event_position = int(positions)
    prior_position = event_position - 1
    entry_position = event_position + initial_end_offset
    final_position = event_position + exit_offset
    if prior_position < 0 or final_position >= len(common):
        raise ValueError("insufficient event-window prices")

    prior, entry, final = (
        common[prior_position],
        common[entry_position],
        common[final_position],
    )
    initial_stock = stock.loc[entry] / stock.loc[prior] - 1
    initial_benchmark = benchmark.loc[entry] / benchmark.loc[prior] - 1
    future_stock = stock.loc[final] / stock.loc[entry] - 1
    future_benchmark = benchmark.loc[final] / benchmark.loc[entry] - 1
    return ReversalEventResult(
        event_id=event_id,
        ticker=ticker,
        event_session=common[event_position].date(),
        initial_abnormal_return=float(initial_stock - initial_benchmark),
        future_abnormal_return=float(future_stock - future_benchmark),
    )


def summarize_reversal(
    results: Sequence[ReversalEventResult],
    *,
    round_trip_cost: float = 0.005,
) -> dict[str, float | int | bool]:
    eligible = [result for result in results if result.eligible]
    if not eligible:
        raise ValueError("no events have a positive initial abnormal reaction")
    gross = [result.gross_short_abnormal_return for result in eligible]
    count = len(gross)
    standard_error = stdev(gross) / sqrt(count) if count > 1 else float("nan")
    gross_mean = mean(gross)
    positive_fraction = sum(value > 0 for value in gross) / count
    return {
        "events": len(results),
        "eligible_events": count,
        "mean_gross_short_abnormal_return": gross_mean,
        "median_gross_short_abnormal_return": median(gross),
        "positive_fraction": positive_fraction,
        "t_interval_low": gross_mean - 1.96 * standard_error,
        "t_interval_high": gross_mean + 1.96 * standard_error,
        "mean_after_fixed_cost": gross_mean - round_trip_cost,
        "passes_frozen_sandbox_rule": bool(
            count >= 8
            and gross_mean > 0
            and gross_mean - round_trip_cost > 0
            and positive_fraction >= 0.60
        ),
    }


def build_results(
    events: Sequence[Mapping[str, str]],
    price_map: Mapping[str, pd.Series],
    benchmark_prices: pd.Series,
) -> list[ReversalEventResult]:
    ticker_aliases = {"BMS": "BMY"}
    results = []
    for event in events:
        if event["outcome"] != "positive":
            continue
        ticker = ticker_aliases.get(event["ticker"], event["ticker"])
        results.append(
            calculate_event_reversal(
                event_id=event["event_id"],
                ticker=ticker,
                event_date=event["event_date"],
                stock_prices=price_map[ticker],
                benchmark_prices=benchmark_prices,
            )
        )
    return results
