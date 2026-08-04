# PLEX archive extractor

Streams EVE Ref `.csv.bz2` market-order snapshots, validates the documented schema, filters PLEX type `44992`, and writes a provenance manifest plus compact summary. Raw full-market archives live only in a temporary directory and are deleted automatically.

The source JSON is an array of pinned index entries containing `name`, `url`, `size`, `etag`, `last_modified`, and `file_time`. The extractor verifies byte size and records SHA-256 plus research-download time.

The daily index selector targets 12:15 UTC, excludes files below half the daily median compressed size, permits the adjacent scheduled scrape within 31 minutes, and otherwise marks the day missing. The one-minute tolerance accommodates archive filenames whose scrape seconds fall just after `:15` or `:45`.

```powershell
python engineering\plex_archive\extract_plex.py `
  --sources engineering\plex_archive\transition_sources.json `
  --manifest engineering\plex_archive\results\transition_manifest.json `
  --summary engineering\plex_archive\results\transition_summary.csv
```

Filtered order rows are optional. The transition audit commits summaries and hashes, not raw full-market snapshots.
