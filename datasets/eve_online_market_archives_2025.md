# EVE Online market archives — 2025 PLEX integration

*Data-access audit completed 2026-08-02. This record documents provenance and feasibility; raw archives are not committed.*

## Research use

The primary candidate event is the transition from regional PLEX order books to a single global PLEX market. CCP announced the global market in advance and assigned it region ID `19000001`. The developer notice states that existing ESI market routes would expose its current orders and history ([CCP developer notice](https://developers.eveonline.com/blog/global-plex-market-and-sde-updates)). PLEX type ID is `44992`.

The event can support a market-integration and liquidity study inside EVE. It cannot support a USD investment-return claim: PLEX is executable against ISK inside the platform, but players do not have a lawful issuer-provided fiat off-ramp for ISK.

## Sources

| Source | Coverage observed | Frequency | Fields relevant to study | Status |
|---|---|---|---|---|
| EVE Ref market-order snapshots | Year directories 2021–2026; 2025 contains daily directories | Twice hourly, normally at `:15` and `:45` | Side, limit price, remaining and original quantity, order ID, issue time, location, system, region | Verified from live indexes and two files |
| EVE Ref market history | Year directories 2003–2026 | Daily | Region/type daily low, high, average, volume, order count | Verified from live index; crawler coverage is not uniform across inactive pairs |
| CCP Monthly Economic Reports mirrored by EVE Ref | 2016–2026; all twelve 2025 archives listed | Monthly plus daily tables inside some releases | Economy-wide sinks, faucets, production, trade and destruction controls | Verified from live index |
| ESI | Current official interface | Endpoint-dependent | Official current orders and history | Use for semantics, not historical reconstruction |

EVE Ref documents full regional order snapshots, the scrape schedule, and archive schema ([order-snapshot documentation](https://docs.everef.net/datasets/market-orders)). Its market-history crawler documents a 450-day active-pair lookback and exploration process, which means missing region/type history must not automatically be coded as zero activity ([history crawler documentation](https://docs.everef.net/commands/scrape-market-history.html)). EVE Ref is a third-party archive of official ESI responses, not an issuer-certified historical database.

## Direct feasibility probe

Two compressed full-market snapshots were downloaded to a temporary directory, streamed with Python's standard-library `bz2` and `csv` readers, filtered to type ID `44992`, and deleted after inspection.

| Snapshot | PLEX orders | Distinct region IDs | Interpretation |
|---|---:|---:|---|
| 2025-07-06 12:15:08 UTC | 2,003 | 59 | Regional-book regime is preserved before integration |
| 2025-07-08 14:15:10 UTC | 322 | 1 (`19000001`) | Global-book regime is preserved after integration |

Both files expose: `duration`, `is_buy_order`, `issued`, `location_id`, `min_volume`, `order_id`, `price`, `range`, `system_id`, `type_id`, `volume_remain`, `volume_total`, `http_last_modified`, `station_id`, `region_id`, and `constellation_id`.

The observed discontinuity verifies archive usability, not an economic effect. The new global region mechanically replaces regional segmentation, and the total number of open orders is not comparable without checking cancellation/migration rules and deployment timing.

## Scale and acquisition design

A full snapshot is roughly 19–20 MB compressed around the event. Downloading all 48 daily snapshots for a 360-day window would be hundreds of gigabytes and is unnecessary. One fixed UTC snapshot per day would be roughly 7 GB compressed for 180 days on either side. A narrower 60-day discovery window would be roughly 2.3 GB.

The recommended staged acquisition is:

1. query and pin every daily index plus ETag without downloading payloads;
2. acquire one fixed snapshot per day for ±60 days, excluding incomplete snapshots by a total-row/size rule fixed without viewing PLEX outcomes;
3. stream-filter PLEX and a preregistered set of control types; retain only filtered rows and a manifest of source URL, timestamp, ETag, byte size, and SHA-256;
4. examine missingness and the exact deployment transition before expanding to ±180 days;
5. acquire daily market history and June–August 2025 MER controls separately.

## Known hazards

- CCP's July 4 developer notice described a July 7 deployment window, while the initial audit sampled July 6 and July 8. The exact first valid global snapshot and order-migration sequence must be identified from the archive before event time is frozen.
- The policy was announced, so price and inventory responses may precede implementation.
- Regional best quotes are executable only for characters with relevant access and logistics. “Global dispersion” before integration mixes information frictions, transport/access, and stale thin books.
- PLEX is unique in fiat issuance and subscription utility; ordinary EVE items are imperfect controls.
- Orders can be cancelled, modified, or migrate. Snapshot differencing does not identify trades.
- A global book mechanically sets displayed cross-region dispersion to zero. That fact cannot be presented as an estimated benefit.
- EVE Ref archive corrections can change `last_modified` or ETag after the observation date. Every acquired object needs a research-download timestamp and hash.

## Reproducibility boundary

No raw archive is stored in Git. A claim-bearing experiment must commit an acquisition manifest, extraction code, schema checks, filtered-data fingerprints, and enough synthetic fixtures to test order-book metrics without network access.

## Connections

`source_scouting/2026-08-02-digital-assets-and-complex-systems.md` · `source_scouting/2026-07-29-virtual-economy-event-data-audit.md` · `ideas/hypothesis_queue.md`
