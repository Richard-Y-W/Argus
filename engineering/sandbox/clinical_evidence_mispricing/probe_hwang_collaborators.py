"""Inspect current collaborator-field prevalence in Hwang's public event sample.

This is a data-feasibility probe, not a historical or alpha test. ClinicalTrials.gov
returns the current record, which can contain collaborators added after the event.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

import requests

from .contingency import fisher_exact_two_sided, odds_ratio


API_ROOT = "https://clinicaltrials.gov/api/v2/studies"
DEFAULT_EVENTS = Path(__file__).with_name("hwang_2013_events.csv")


def extract_current_collaborators(study: dict[str, Any]) -> list[str]:
    module = study.get("protocolSection", {}).get("sponsorCollaboratorsModule", {})
    return [
        item["name"]
        for item in module.get("collaborators", [])
        if item.get("name")
    ]


def load_events(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def probe(events: list[dict[str, str]]) -> dict[str, Any]:
    rows = []
    for event in events:
        response = requests.get(f"{API_ROOT}/{event['nct_id']}", timeout=30)
        response.raise_for_status()
        study = response.json()
        collaborators = extract_current_collaborators(study)
        rows.append(
            {
                **event,
                "current_collaborator_count": len(collaborators),
                "current_collaborators": collaborators,
                "version_holder": study.get("derivedSection", {})
                .get("miscInfoModule", {})
                .get("versionHolder"),
            }
        )

    summary: dict[str, Any] = {
        "evidence_status": "current-record feasibility only; historically contaminated",
        "events": len(rows),
        "rows": rows,
    }
    for outcome in ("positive", "negative"):
        subset = [row for row in rows if row["outcome"] == outcome]
        summary[outcome] = {
            "events": len(subset),
            "with_current_collaborator": sum(
                row["current_collaborator_count"] > 0 for row in subset
            ),
        }
    positive_with = summary["positive"]["with_current_collaborator"]
    negative_with = summary["negative"]["with_current_collaborator"]
    table = (
        (positive_with, summary["positive"]["events"] - positive_with),
        (negative_with, summary["negative"]["events"] - negative_with),
    )
    summary["exploratory_association"] = {
        "table": table,
        "odds_ratio_positive_outcome": odds_ratio(table),
        "fisher_exact_two_sided_p": fisher_exact_two_sided(table),
        "claim_eligible": False,
    }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    args = parser.parse_args()
    print(json.dumps(probe(load_events(args.events)), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
