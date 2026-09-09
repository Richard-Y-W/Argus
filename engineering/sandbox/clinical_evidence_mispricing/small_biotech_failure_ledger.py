"""Validation for the return-blind Phase III failure reconstruction ledger."""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path
from typing import Iterable


REQUIRED_COLUMNS = (
    "event_id",
    "announcement_date",
    "announcement_timing",
    "sponsor_name",
    "event_ticker",
    "cik",
    "asset",
    "trial_name",
    "phase",
    "failure_definition",
    "source_url",
    "source_timing",
    "coding_status",
)
ALLOWED_ANNOUNCEMENT_TIMING = {"pre_market", "market_hours", "after_market", "date_only"}
ALLOWED_SOURCE_TIMING = {"event_time_primary", "retrospective_primary"}
ALLOWED_CODING_STATUS = {"single_coded_candidate", "dual_coded_eligible", "rejected"}


def load_ledger(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != REQUIRED_COLUMNS:
            raise ValueError("ledger columns do not match the frozen schema")
        rows = list(reader)
    validate_ledger(rows)
    return rows


def validate_ledger(rows: Iterable[dict[str, str]]) -> None:
    seen_ids: set[str] = set()
    for row in rows:
        missing = [column for column in REQUIRED_COLUMNS if not row.get(column)]
        if missing:
            raise ValueError(f"{row.get('event_id', '<unknown>')} missing {missing}")
        if row["event_id"] in seen_ids:
            raise ValueError(f"duplicate event_id {row['event_id']}")
        seen_ids.add(row["event_id"])
        date.fromisoformat(row["announcement_date"])
        if row["announcement_timing"] not in ALLOWED_ANNOUNCEMENT_TIMING:
            raise ValueError("invalid announcement_timing")
        if row["source_timing"] not in ALLOWED_SOURCE_TIMING:
            raise ValueError("invalid source_timing")
        if row["coding_status"] not in ALLOWED_CODING_STATUS:
            raise ValueError("invalid coding_status")
        if row["phase"] != "3":
            raise ValueError("ledger accepts only Phase III candidates")
        if not row["source_url"].startswith("https://www.sec.gov/Archives/"):
            raise ValueError("seed source must be an SEC archive URL")
