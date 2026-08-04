# PLEX transition-boundary and archive-engineering audit

**Stage:** external-data engineering and treatment-semantics audit; not hypothesis execution  
**Attribution:** Human-directed  
**Research date:** 2026-08-03 America/New_York; source downloads occurred after 00:00 UTC on 2026-08-04.

## Classification

**SUPPORTED WITH LIMITS:** EVE Ref preserves a complete sequence that identifies regional cancellation, an empty PLEX interval, and first observed global-book formation at half-hour resolution. This supports treatment-timing registration. It does not establish any liquidity or welfare effect.

## Reconstructed sequence

| Snapshot UTC | Full-market rows | PLEX orders | PLEX regions | Classification |
|---|---:|---:|---:|---|
| 2025-07-07 10:45:07 | 1,517,657 | 1,928 | 59 | Last observed regional regime |
| 2025-07-07 11:15:07 | 1,515,806 | 0 | 0 | Complete snapshot; PLEX cancellation/empty phase |
| 2025-07-07 11:45:08 | 1,515,683 | 130 | 1 (`19000001`) | First observed global book |
| 2025-07-07 12:15:12 | 1,516,116 | 158 | 1 (`19000001`) | Early global-book formation |

Therefore:

- regional cancellation is interval-censored to `(10:45:07, 11:15:07]` UTC;
- first observed global formation is interval-censored to `(11:15:07, 11:45:08]` UTC;
- the 11:15 zero is not archive absence because the full-market row count remains comparable;
- July 8 at 13:15 and 13:45 contains separate incomplete full-market snapshots and must not be interpreted as a PLEX event.

The prior two-snapshot audit correctly classified July 6 as regional and July 8 at 14:15 as global, but it could not identify the cancellation/formation sequence. That uncertainty is now materially reduced.

## Provenance and integrity

Each inspected payload was discovered through EVE Ref `index.json`, pinned by URL, byte size, ETag, last-modified time, and file time, then verified by byte size and SHA-256. The extractor streamed bzip2 CSV content, validated all documented columns, retained compact summaries, and deleted full-market archives automatically.

The key SHA-256 fingerprints are:

- 10:45 regional: `993386e78f7dc78f8dc76b07b5a23f058a5a9f7c8a40e7d2511ea098cf58c3cf`
- 11:15 empty: `93059eae1af9793bbbbaa277b61d5d870799bcb025ba52a47e40d7be3864dcc5`
- 11:45 first global: `8ec4ee57eb180e3cb46d57dd6ba9d778d6aeaffb459f8d0a398f1a2facef883d`
- 12:15 early global: `b183dac0d4bdccd4f4d9b850c57697d49722cb9d98819517017b38a94bd87ec2`

## ±60-day index panel

Daily index metadata from 2025-05-08 through 2025-09-05 were pinned: 121 UTC days. The fixed snapshot target is 12:15 UTC. Files below half the daily median compressed size are invalid; an adjacent scheduled scrape within 31 minutes is permitted; otherwise the day is missing.

- 120 days have a valid fixed-time candidate.
- 2025-07-16 is missing because only 15 later-day files exist and the nearest is 16:45.
- 2025-07-18 contains six sub-half-median files; the valid 12:45 scrape is selected.
- 2025-07-08 contains two sub-half-median files at 13:15 and 13:45; its valid 12:15 scrape is selected.

No daily payload panel has been downloaded yet.

## Strongest adversarial interpretation

EVE Ref is a third-party replay of ESI, not CCP-certified historical ground truth. ETags and hashes establish what Argus downloaded, not that upstream scraping was complete. The exact cancellation and formation could occur anywhere inside the half-hour intervals. Zero open orders does not reveal whether outstanding orders were cancelled, migrated outside ESI visibility, or temporarily suppressed, although CCP's stated cancellation policy makes cancellation plausible.

One issuer-controlled event still does not create an untreated counterfactual. The next study can estimate descriptive and bounded associational changes in non-mechanical market quality, not causal welfare.

## Promotion decision

The transition-timing and extractor gates pass. Registration remains premature until:

1. control types are chosen using pre-event liquidity only;
2. the 120 selected daily payloads are streamed and completeness diagnostics are frozen;
3. spread, depth, imbalance, and concentration metrics pass synthetic fixture tests;
4. the announcement, cancellation, empty interval, global formation, and July 12 promotion are modeled separately;
5. an estimand and inference method appropriate to one treated event are fixed.

## Connections

`datasets/eve_online_market_archives_2025.md` · `engineering/plex_archive/` · PLEX novelty audit · evidence-boundary record

