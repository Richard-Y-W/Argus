"""Pin EVE Ref daily index metadata without downloading market payloads."""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import hashlib
import json
import statistics
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


def dates(start: date, end: date):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def choose_file(files: list[dict], target_hour: int = 12, target_minute: int = 15,
                max_offset_seconds: int = 1860) -> tuple[dict | None, dict]:
    sizes = [int(f["size"]) for f in files]
    median = statistics.median(sizes) if sizes else 0
    valid = [f for f in files if int(f["size"]) >= 0.5 * median]
    target_seconds = target_hour * 3600 + target_minute * 60

    def distance(entry: dict):
        stamp = datetime.fromisoformat(entry["file_time"].replace("Z", "+00:00"))
        seconds = stamp.hour * 3600 + stamp.minute * 60 + stamp.second
        return abs(seconds - target_seconds), stamp

    selected = min(valid, key=distance) if valid else None
    selected_offset = distance(selected)[0] if selected else None
    if selected_offset is not None and selected_offset > max_offset_seconds:
        selected = None
    audit = {"file_count": len(files), "median_size": median,
             "invalid_below_half_median": len(files) - len(valid),
             "selected_offset_seconds": selected_offset}
    return selected, audit


def fetch_day(day: date) -> dict:
    day_text = day.isoformat()
    url = f"https://data.everef.net/market-orders/history/{day.year}/{day_text}/index.json"
    with urllib.request.urlopen(url, timeout=60) as response:
        raw = response.read()
    payload = json.loads(raw)
    selected, audit = choose_file(payload.get("files", []))
    return {
        "date": day_text,
        "index_url": url,
        "index_retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "index_sha256": hashlib.sha256(raw).hexdigest(),
        **audit,
        "selected": selected,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", required=True, type=date.fromisoformat)
    parser.add_argument("--end", required=True, type=date.fromisoformat)
    parser.add_argument("--json", required=True, type=Path)
    parser.add_argument("--csv", required=True, type=Path)
    args = parser.parse_args()
    day_list = list(dates(args.start, args.end))
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        records = list(executor.map(fetch_day, day_list))
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(records, indent=2), encoding="utf-8")
    columns = ["date", "index_url", "index_retrieved_utc", "index_sha256", "file_count",
               "median_size", "invalid_below_half_median", "selected_offset_seconds", "selected_name", "selected_url",
               "selected_size", "selected_last_modified", "selected_etag", "selected_file_time"]
    with args.csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for record in records:
            selected = record["selected"] or {}
            writer.writerow({
                **{key: record[key] for key in columns[:8]},
                "selected_name": selected.get("name"), "selected_url": selected.get("url"),
                "selected_size": selected.get("size"),
                "selected_last_modified": selected.get("last_modified"),
                "selected_etag": selected.get("etag"),
                "selected_file_time": selected.get("file_time"),
            })
    print(f"pinned {len(records)} daily indexes; missing selections={sum(r['selected'] is None for r in records)}")


if __name__ == "__main__":
    main()
