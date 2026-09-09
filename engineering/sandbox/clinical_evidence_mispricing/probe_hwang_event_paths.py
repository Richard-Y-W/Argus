"""Check two published event-path premises in the small Hwang sample.

This is deliberately not a test of the small-biotech failure-reversal claim or
of a public-information run-up signal: the Hwang sample contains large firms and
the run-up calculation contains no explanatory public predictors.
"""

from __future__ import annotations

import json
from typing import Any

from .event_path_smoke import calculate_window, summarize
from .probe_hwang_collaborators import DEFAULT_EVENTS, load_events
from .probe_positive_spike_reversal import fetch_adjusted_close


ALIASES = {"BMS": "BMY"}


def _row(result: Any) -> dict[str, Any]:
    return {
        "event_id": result.event_id,
        "ticker": result.ticker,
        "outcome": result.outcome,
        "start_session": result.start_session,
        "end_session": result.end_session,
        "abnormal_return": result.abnormal_return,
    }


def run() -> dict[str, Any]:
    events = load_events(DEFAULT_EVENTS)
    tickers = sorted({ALIASES.get(event["ticker"], event["ticker"]) for event in events})
    prices = {ticker: fetch_adjusted_close(ticker) for ticker in tickers}
    spy = fetch_adjusted_close("SPY")
    xbi = fetch_adjusted_close("XBI")

    runups = []
    failure_reversals = []
    for event in events:
        ticker = ALIASES.get(event["ticker"], event["ticker"])
        runups.append(
            calculate_window(
                event_id=event["event_id"],
                ticker=ticker,
                outcome=event["outcome"],
                event_date=event["event_date"],
                stock_prices=prices[ticker],
                benchmark_prices=spy,
                start_offset=-120,
                end_offset=-3,
            )
        )
        if event["outcome"] == "negative":
            failure_reversals.append(
                calculate_window(
                    event_id=event["event_id"],
                    ticker=ticker,
                    outcome=event["outcome"],
                    event_date=event["event_date"],
                    stock_prices=prices[ticker],
                    benchmark_prices=xbi,
                    start_offset=2,
                    end_offset=100,
                )
            )

    positive_runups = [row.abnormal_return for row in runups if row.outcome == "positive"]
    negative_runups = [row.abnormal_return for row in runups if row.outcome == "negative"]
    failure_values = [row.abnormal_return for row in failure_reversals]
    return {
        "evidence_status": "exploratory sandbox only; mutable prices; not claim eligible",
        "runup_premise": {
            "design": "SPY-adjusted close[-120] to close[-3] by paper-coded outcome",
            "positive": summarize(positive_runups),
            "negative": summarize(negative_runups),
            "difference_in_means_positive_minus_negative": sum(positive_runups) / len(positive_runups) - sum(negative_runups) / len(negative_runups),
            "rows": [_row(row) for row in runups],
        },
        "large_firm_failure_path_placebo": {
            "design": "XBI-adjusted long close[+2] to close[+100] after negative event; Hwang large-firm sample",
            "scope_warning": "wrong universe for the proposed small-biotech failure-reversal replication",
            "summary": summarize(failure_values),
            "mean_after_fixed_50bp_cost": sum(failure_values) / len(failure_values) - 0.005,
            "rows": [_row(row) for row in failure_reversals],
        },
    }


def main() -> None:
    print(json.dumps(run(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
