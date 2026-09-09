# RTDSM vintage and release-map audit

**Stage:** exploration and data-engineering gate  
**Attribution:** AI-led  
**Decision:** quarterly as-of infrastructure is feasible; exact-release experiments remain unregistered

## Question and competing mechanisms

Can Argus compare macro model rankings under historically feasible and final-vintage data using a common, auditable information cutoff?

The target mechanism is revision-induced ranking fragility. Alternatives include ragged-edge availability, inconsistent source concepts, benchmark redefinitions, shutdown-delayed releases, and transformation artifacts. A difference between vintage protocols would not by itself identify why a statistical agency revised a series.

## Evidence inspected

Official quarterly-vintage workbooks for real output (`ROUTPUT`), CPI, and unemployment (`RUC`) were downloaded without any market data. The Philadelphia Fed describes RTDSM as snapshots of the historical series available at past vintage dates. Variable notes define quarterly vintages as the information available in the middle of February, May, August, and November.

## Deterministic audit result

| Series | Observation rows | Usable vintages | First usable | Last usable | Latest observation |
|---|---:|---:|---|---|---|
| ROUTPUT | 318 | 244 | 1965:Q4 | 2026:Q3 | 2026:Q2 |
| CPI | 955 | 129 | 1994:Q3 | 2026:Q3 | 2026:07 |
| RUC | 955 | 244 | 1965:Q4 | 2026:Q3 | 2026:07 |

All three series share 129 usable quarterly snapshots from 1994-08-15 through 2026-08-15. Observation-date keys contain no duplicates. The CPI workbook declares 244 vintage columns, but the 115 columns before CPI94Q3 are completely empty; the audit excludes them rather than claiming synthetic coverage.

The three-target and deterministic as-of-date gates pass. The exact-release gate does not. A quarterly column tells us what was present at the mid-quarter cutoff; it does not label each cell first, second, third, annual-benchmark, or comprehensive-revision status.

## Decision rule and result

The earlier scouting gate required three targets with consistent vintages, an executable acquisition path, and an unambiguous forecast-origin mapping. This audit supplies three targets, verified downloads, and a conservative mid-quarter as-of map. It therefore supports a future quarterly model-ranking design whose forecasts are formed no earlier than the 15th of the middle month.

No `HYP` or `EXP` is registered yet. Exact-release or announcement-window studies need the Philadelphia Fed's first/second/third-release files and agency release calendars. The model menu, transformations, forecast horizons, loss, expanding-window start, final-vintage comparator, and joint uncertainty rule also remain unfrozen.

## Strongest adversarial interpretation

The infrastructure can prevent obvious final-vintage leakage while still mixing conceptual revisions with ordinary release noise. CPI begins only in 1994:Q3, so any common-sample comparison excludes earlier inflation regimes. Mid-month snapshots are too coarse for daily market timing.

## Minimum next test

Create a return-free release-status table for ROUTPUT, CPI, and RUC over the 129 common vintages. Freeze a small model set and evaluate whether transformations remain semantically comparable across benchmark changes before inspecting any ranking result.

## Connections

`source_scouting/2026-08-02-real-time-macro-vintages.md` · `datasets/philadelphia_fed_macro_data_gates.md` · `engineering/sandbox/macro_data_gates/audit.py` · `knowledge_graph/macro-real-time-thread.md`
