"""Stream-filter EVE Ref market-order snapshots with auditable provenance.

Raw archives are downloaded to a temporary directory and never retained. The tool
writes a compact source manifest and per-snapshot PLEX summaries. Filtered order
rows are optional and disabled by default.
"""

from __future__ import annotations

import argparse
import bz2
import csv
import hashlib
import json
import tempfile
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

PLEX_TYPE_ID = "44992"
GLOBAL_REGION_ID = "19000001"
REQUIRED = {
    "duration", "is_buy_order", "issued", "location_id", "min_volume",
    "order_id", "price", "range", "system_id", "type_id", "volume_remain",
    "volume_total", "http_last_modified", "region_id", "station_id",
    "constellation_id",
}


def stream_snapshot(path: Path, keep_rows: bool = False) -> tuple[dict, list[dict]]:
    total = 0
    plex_rows: list[dict] = []
    regions: Counter[str] = Counter()
    buys = sells = 0
    buy_volume = sell_volume = 0
    with bz2.open(path, "rt", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        missing = REQUIRED - fields
        if missing:
            raise ValueError(f"missing required columns: {sorted(missing)}")
        for row in reader:
            total += 1
            if row["type_id"] != PLEX_TYPE_ID:
                continue
            regions[row["region_id"]] += 1
            volume = int(row["volume_remain"])
            if row["is_buy_order"].lower() == "true":
                buys += 1
                buy_volume += volume
            else:
                sells += 1
                sell_volume += volume
            if keep_rows:
                plex_rows.append({key: row[key] for key in reader.fieldnames})
    summary = {
        "total_rows": total,
        "plex_orders": buys + sells,
        "plex_buy_orders": buys,
        "plex_sell_orders": sells,
        "plex_buy_volume": buy_volume,
        "plex_sell_volume": sell_volume,
        "distinct_plex_regions": len(regions),
        "plex_regions": dict(sorted(regions.items())),
        "global_region_only": bool(regions) and set(regions) == {GLOBAL_REGION_ID},
    }
    return summary, plex_rows


def download_and_extract(source: dict, keep_rows: bool = False) -> tuple[dict, list[dict]]:
    with tempfile.TemporaryDirectory(prefix="argus-plex-") as temp_dir:
        target = Path(temp_dir) / source["name"]
        sha = hashlib.sha256()
        with urllib.request.urlopen(source["url"], timeout=120) as response, target.open("wb") as output:
            while chunk := response.read(1024 * 1024):
                output.write(chunk)
                sha.update(chunk)
        actual_size = target.stat().st_size
        if actual_size != int(source["size"]):
            raise ValueError(f"size mismatch for {source['name']}: {actual_size} != {source['size']}")
        summary, rows = stream_snapshot(target, keep_rows=keep_rows)
        record = {
            **source,
            "research_download_utc": datetime.now(timezone.utc).isoformat(),
            "sha256": sha.hexdigest(),
            **summary,
        }
        return record, rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", required=True, type=Path,
                        help="JSON array containing name, url, size, etag, last_modified, and file_time")
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--summary", required=True, type=Path)
    parser.add_argument("--filtered-rows", type=Path)
    args = parser.parse_args()
    sources = json.loads(args.sources.read_text(encoding="utf-8"))
    records, all_rows = [], []
    for source in sources:
        record, rows = download_and_extract(source, keep_rows=args.filtered_rows is not None)
        records.append(record)
        for row in rows:
            all_rows.append({"snapshot_name": source["name"], **row})
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(records, indent=2), encoding="utf-8")
    columns = ["name", "file_time", "size", "total_rows", "plex_orders", "plex_buy_orders",
               "plex_sell_orders", "plex_buy_volume", "plex_sell_volume", "distinct_plex_regions",
               "global_region_only", "etag", "sha256"]
    with args.summary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows([{key: record[key] for key in columns} for record in records])
    if args.filtered_rows is not None and all_rows:
        with args.filtered_rows.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=all_rows[0].keys())
            writer.writeheader()
            writer.writerows(all_rows)
    print(json.dumps(records, indent=2))


if __name__ == "__main__":
    main()

