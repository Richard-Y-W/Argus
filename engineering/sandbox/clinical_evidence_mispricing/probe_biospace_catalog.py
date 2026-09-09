"""Report return-blind BioSpace sitemap coverage and candidate slugs."""

from __future__ import annotations

import json

from .biospace_reconstruction import candidate_entries, fetch_catalog


def run() -> dict[str, object]:
    catalog = fetch_catalog()
    candidates = candidate_entries(catalog)
    return {
        "evidence_status": "source-discovery only; candidates require manual dual coding",
        "source": "BioSpace news-sitemap-content.xml",
        "catalog_entries": len(catalog),
        "phase_outcome_slug_candidates": len(candidates),
        "candidate_urls": [entry.url for entry in candidates],
        "warning": "slug filtering is a recall/precision probe, not an event label or study sample",
    }


def main() -> None:
    print(json.dumps(run(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
