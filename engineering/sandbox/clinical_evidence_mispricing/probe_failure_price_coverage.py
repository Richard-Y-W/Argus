"""Audit free-price coverage without calculating failure-event returns."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
import time
from typing import Any

import pandas as pd

from .probe_positive_spike_reversal import fetch_chart_payload, parse_adjusted_close
from .small_biotech_failure_ledger import load_ledger


LEDGER = Path(__file__).with_name("small_biotech_phase3_failures_seed.csv")
START = datetime(2016, 1, 1, tzinfo=timezone.utc)
END = datetime(2020, 6, 1, tzinfo=timezone.utc)


def has_event_window(prices: pd.Series, announcement_date: str) -> bool:
    dates = pd.to_datetime(prices.index).tz_localize(None).normalize()
    target = pd.Timestamp(announcement_date)
    location = int(dates.searchsorted(target))
    return location >= 252 and location + 100 < len(dates)


def run() -> dict[str, Any]:
    rows = []
    for event in load_ledger(LEDGER):
        try:
            payload = fetch_chart_payload(event["event_ticker"], start=START, end=END)
            result = payload["chart"]["result"][0]
            provider_name = result.get("meta", {}).get("longName")
            prices = parse_adjusted_close(payload)
            window_available = has_event_window(prices, event["announcement_date"])
            expected_root = event["sponsor_name"].split()[0].lower()
            identity_matches = bool(provider_name) and expected_root in provider_name.lower()
            rows.append(
                {
                    "event_id": event["event_id"],
                    "ticker": event["event_ticker"],
                    "observations": len(prices),
                    "provider_name": provider_name,
                    "identity_matches_sponsor": identity_matches,
                    "has_252_pre_and_100_post_sessions": window_available,
                    "usable_after_identity_check": window_available and identity_matches,
                    "error": None,
                }
            )
        except Exception as exc:  # provider failures are the object of this probe
            rows.append(
                {
                    "event_id": event["event_id"],
                    "ticker": event["event_ticker"],
                    "observations": 0,
                    "provider_name": None,
                    "identity_matches_sponsor": False,
                    "has_252_pre_and_100_post_sessions": False,
                    "usable_after_identity_check": False,
                    "error": type(exc).__name__,
                }
            )
        finally:
            time.sleep(1.0)
    return {
        "evidence_status": "coverage audit only; no returns calculated",
        "provider": "Yahoo public chart endpoint",
        "events": len(rows),
        "window_covered_events": sum(row["has_252_pre_and_100_post_sessions"] for row in rows),
        "usable_events": sum(row["usable_after_identity_check"] for row in rows),
        "rows": rows,
        "decision": "Yahoo cannot support the study if any historical event is absent; a delisting-complete source remains required",
    }


def main() -> None:
    print(json.dumps(run(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
