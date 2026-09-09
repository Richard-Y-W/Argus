"""Run the frozen Hwang-sample positive-spike reversal feasibility probe.

Yahoo's public chart endpoint is used only for this disposable sandbox probe. Its
mutable data and lack of a licensed point-in-time snapshot make the output
ineligible for registered evidence.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote

import pandas as pd
import requests

from .positive_spike_reversal import build_results, summarize_reversal
from .probe_hwang_collaborators import DEFAULT_EVENTS, load_events


CHART_ROOT = "https://query1.finance.yahoo.com/v8/finance/chart"
START = datetime(2010, 1, 1, tzinfo=timezone.utc)
END = datetime(2014, 6, 1, tzinfo=timezone.utc)


def parse_adjusted_close(payload: dict[str, Any]) -> pd.Series:
    chart = payload.get("chart", {})
    if chart.get("error") is not None:
        raise ValueError(f"price provider error: {chart['error']}")
    results = chart.get("result") or []
    if len(results) != 1:
        raise ValueError("expected exactly one chart result")
    result = results[0]
    timestamps = result.get("timestamp") or []
    adjclose_groups = result.get("indicators", {}).get("adjclose") or []
    if len(adjclose_groups) != 1:
        raise ValueError("adjusted-close data missing")
    closes = adjclose_groups[0].get("adjclose") or []
    if len(timestamps) != len(closes):
        raise ValueError("timestamp and adjusted-close lengths differ")
    observations = [
        (pd.Timestamp(timestamp, unit="s", tz="UTC"), close)
        for timestamp, close in zip(timestamps, closes, strict=True)
        if close is not None
    ]
    if not observations:
        raise ValueError("no adjusted-close observations")
    return pd.Series(
        [float(close) for _, close in observations],
        index=pd.DatetimeIndex([timestamp for timestamp, _ in observations]),
        dtype=float,
    )


def fetch_chart_payload(
    ticker: str,
    *,
    start: datetime = START,
    end: datetime = END,
) -> dict[str, Any]:
    response = requests.get(
        f"{CHART_ROOT}/{quote(ticker, safe='')}",
        params={
            "period1": int(start.timestamp()),
            "period2": int(end.timestamp()),
            "interval": "1d",
            "events": "history",
        },
        timeout=30,
        headers={"User-Agent": "Argus research feasibility probe"},
    )
    response.raise_for_status()
    return response.json()


def fetch_adjusted_close(
    ticker: str,
    *,
    start: datetime = START,
    end: datetime = END,
) -> pd.Series:
    return parse_adjusted_close(fetch_chart_payload(ticker, start=start, end=end))


def run(events_path: Path = DEFAULT_EVENTS) -> dict[str, Any]:
    events = load_events(events_path)
    positive_events = [event for event in events if event["outcome"] == "positive"]
    aliases = {"BMS": "BMY"}
    tickers = sorted({aliases.get(event["ticker"], event["ticker"]) for event in positive_events})
    prices = {ticker: fetch_adjusted_close(ticker) for ticker in tickers}
    benchmark = fetch_adjusted_close("SPY")
    results = build_results(events, prices, benchmark)
    summary = summarize_reversal(results)
    return {
        "evidence_status": "exploratory sandbox only; not claim eligible",
        "price_source": "Yahoo public chart endpoint, retrieved at run time",
        "design": "positive paper-coded events; enter short at close +1; exit close +20; SPY-adjusted; 50 bp fixed round-trip cost",
        "summary": summary,
        "rows": [
            {
                "event_id": result.event_id,
                "ticker": result.ticker,
                "event_session": result.event_session.isoformat(),
                "initial_abnormal_return": result.initial_abnormal_return,
                "eligible": result.eligible,
                "future_abnormal_return": result.future_abnormal_return,
                "gross_short_abnormal_return": result.gross_short_abnormal_return,
            }
            for result in results
        ],
    }


def main() -> None:
    print(json.dumps(run(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
