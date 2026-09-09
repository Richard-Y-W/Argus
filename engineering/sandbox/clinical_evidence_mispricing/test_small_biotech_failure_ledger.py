from __future__ import annotations

from pathlib import Path

import pytest

from .small_biotech_failure_ledger import load_ledger, validate_ledger


LEDGER = Path(__file__).with_name("small_biotech_phase3_failures_seed.csv")


def test_seed_ledger_validates() -> None:
    rows = load_ledger(LEDGER)
    assert len(rows) == 8
    assert all(row["coding_status"] == "single_coded_candidate" for row in rows)
    assert all(row["announcement_timing"] != "date_only" for row in rows)


def test_duplicate_event_ids_are_rejected() -> None:
    row = load_ledger(LEDGER)[0]
    with pytest.raises(ValueError, match="duplicate"):
        validate_ledger([row, row])


def test_non_sec_seed_source_is_rejected() -> None:
    row = {**load_ledger(LEDGER)[0], "source_url": "https://example.com/story"}
    with pytest.raises(ValueError, match="SEC archive"):
        validate_ledger([row])
