# Chen & Zimmermann (2022) — Open Source Cross-Sectional Asset Pricing

*Critical Finance Review 11(2). SSRN 3604626. Data: openassetpricing.com, GitHub OpenSourceAP/CrossSection. Note by Argus 2026-07-10.*

## What it is

A full open-source reproduction of the published cross-sectional predictor literature: code + data reproducing ~200 predictors (212 in the October 2025 release), each following the original paper's construction as closely as possible, with documented reproduction quality. Signal documentation records authors, journal, publication year, sample start/end, and the original portfolio construction — which is exactly the metadata needed for McLean–Pontiff-style event studies.

## Why it matters

- Turns "trust me, I replicated 97 anomalies" into an auditable public artifact. Reproductions match original papers' t-stats closely for the "clear predictor" set.
- The `Cat.Signal` field separates **Predictors** (original paper found significance) from **Placebos** (characteristics the literature did not claim predict returns) — a built-in control group most studies lack.
- Monthly long-short returns per predictor (`PredictorPortsFull.csv`, `port == 'LS'`), signed so the in-sample mean is positive per the original paper's direction.

## Limitations

- US equities (CRSP/Compustat) only.
- "Original paper" portfolio implementations vary in weighting/rebalancing; alternative constructions (deciles EW/VW, liquidity screens) are provided separately and can change magnitudes materially.
- Reproduction quality varies; `Predictability in OP` flags how clearly each signal's predictability reproduced.

## October 2025 release (used by Argus)

- 212 predictors; monthly data through 2024-12.
- Accessed via the `openassetpricing` Python package (mk0417/open-asset-pricing-download).
- Local copies: `datasets/raw/PredictorPortsFull.parquet`, `datasets/raw/SignalDoc.csv` (gitignored; provenance in `datasets/chen_zimmermann_oct2025.md`).

## Connections

- Enables: `experiments/EXP-001-anomaly-decay/` (M&P three-window replication)
- Complements (as evidence vs. description): `papers/2018-kakushadze-serur-151-trading-strategies.md`
- Target design: `papers/2016-mclean-pontiff-does-academic-research-destroy-predictability.md`
