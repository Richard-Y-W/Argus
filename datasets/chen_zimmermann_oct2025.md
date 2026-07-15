# Dataset: Chen & Zimmermann Open Source Asset Pricing — October 2025 release

*Acquired 2026-07-10 by Argus.*

- **Source:** openassetpricing.com (Chen & Zimmermann), October 2025 release; monthly data through 2024-12.
- **Access method:** Python package `openassetpricing` (mk0417/open-asset-pricing-download), which pulls the official release from the project's Google Drive. Re-fetch: `pip install openassetpricing`, then `OpenAP().dl_port('op')` and `OpenAP().dl_signal_doc()`.
- **Local files (gitignored, re-fetchable):**
  - `datasets/raw/PredictorPortsFull.parquet` — 1,226,794 rows: `signalname, port, date, ret, signallag, Nlong, Nshort`. `port == 'LS'` rows are monthly long-short returns in **percent**, signed so the original paper's direction gives positive in-sample means. Portfolio construction follows each original paper ("original paper" implementation).
  - `datasets/raw/SignalDoc.csv` — 331 signals × 29 columns. Key fields: `Acronym`, `Cat.Signal` (Predictor/Placebo), `Predictability in OP` (reproduction quality), `Year` (publication), `SampleStartYear`, `SampleEndYear`.
  - `datasets/raw/PlaceboPortsFull.parquet` — 514,271 rows, same schema as PredictorPortsFull; acquired 2026-07-11. 114 placebo signals (`Cat.Signal == 'Placebo'`): characteristics from published papers that did **not** clearly claim return predictability. Two subtypes via `Predictability in OP`: `indirect` (n=100, predictability implied but not the paper's demonstrated claim) and `4_not` (n=14, paper explicitly found no predictability). **Signing:** placebo LS portfolios are signed by the direction implied in the original paper, *not* by in-sample performance — verified 2026-07-11: only 68% have positive in-sample mean LS (vs ~98% of predictors), and the `4_not` group's in-sample mean is ≈0.06%/mo. Not exposed by the `openassetpricing` package; fetched directly from the release Drive folder ("Full Sets OP"), file id `1kByPQWke42gzqb5ewHZPnXSXK6J56vgH`.
  - `datasets/raw/deciles_ew.parquet` and `deciles_vw.parquet` — official alternative decile portfolios, 1,595,223 and 1,595,220 rows; acquired 2026-07-14 with `engineering/acquire_alternative_ports.py`. These enable within-signal weighting comparisons and are not yet claim-bearing results.
- **Integrity:** SHA-256 hashes for all five cached files are recorded in `datasets/manifest.json` and checked by `engineering/verify_repository.py`.
- **Known biases / caveats:**
  - US CRSP/Compustat universe only.
  - Reproductions are approximate; quality flagged per signal.
  - Returns are gross of transaction costs.
  - Publication `Year` has annual resolution only — window boundaries dated to Dec 31 introduce ±1y noise around publication.
- **License:** data provided freely for research by the authors (CC BY-NC 4.0 per project site).

## Used by
`experiments/EXP-001-anomaly-decay/` · `EXP-002-placebo-decay/` · `EXP-003-calendar-vs-event-time/` · `EXP-004-placebo-spillover/` · `EXP-005-decay-heterogeneity/` · `EXP-006-sample-length/` · `EXP-007-cohort-haircut/` · `EXP-008-post-publication-crowding/` · `EXP-009-weighting-and-decay/` · `EXP-010-within-signal-weighting-decay/`
