# Dataset: Chen & Zimmermann Open Source Asset Pricing — October 2025 release

*Acquired 2026-07-10 by Argus.*

- **Source:** openassetpricing.com (Chen & Zimmermann), October 2025 release; monthly data through 2024-12.
- **Access method:** Python package `openassetpricing` (mk0417/open-asset-pricing-download), which pulls the official release from the project's Google Drive. Re-fetch: `pip install openassetpricing`, then `OpenAP().dl_port('op')` and `OpenAP().dl_signal_doc()`.
- **Local files (gitignored, re-fetchable):**
  - `datasets/raw/PredictorPortsFull.parquet` — 1,226,794 rows: `signalname, port, date, ret, signallag, Nlong, Nshort`. `port == 'LS'` rows are monthly long-short returns in **percent**, signed so the original paper's direction gives positive in-sample means. Portfolio construction follows each original paper ("original paper" implementation).
  - `datasets/raw/SignalDoc.csv` — 331 signals × 29 columns. Key fields: `Acronym`, `Cat.Signal` (Predictor/Placebo), `Predictability in OP` (reproduction quality), `Year` (publication), `SampleStartYear`, `SampleEndYear`.
- **Known biases / caveats:**
  - US CRSP/Compustat universe only.
  - Reproductions are approximate; quality flagged per signal.
  - Returns are gross of transaction costs.
  - Publication `Year` has annual resolution only — window boundaries dated to Dec 31 introduce ±1y noise around publication.
- **License:** data provided freely for research by the authors (CC BY-NC 4.0 per project site).

## Used by
`experiments/EXP-001-anomaly-decay/`
