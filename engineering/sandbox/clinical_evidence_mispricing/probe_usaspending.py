"""Read-only USAspending schema probe for a named recipient."""

from __future__ import annotations

import argparse
import json

import requests

from .public_signals import usaspending_award_search_request


ENDPOINT = "https://api.usaspending.gov/api/v2/search/spending_by_award/"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("recipient")
    parser.add_argument("start_date")
    parser.add_argument("end_date")
    parser.add_argument("--limit", type=int, default=25)
    args = parser.parse_args()
    request = usaspending_award_search_request(
        recipient_name=args.recipient,
        start_date=args.start_date,
        end_date=args.end_date,
        limit=args.limit,
    )
    response = requests.post(
        ENDPOINT,
        json=request,
        headers={"User-Agent": "Argus research audit contact: local researcher"},
        timeout=30,
    )
    response.raise_for_status()
    print(json.dumps(response.json(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
