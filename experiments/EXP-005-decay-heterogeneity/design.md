# EXP-005 — Design: cross-predictor heterogeneity in post-publication decay

*2026-07-12. Registered before any analysis code is written. Hypothesis: `hypotheses/HYP-005-decay-heterogeneity.md`.*

## Question
Which predictors decay after publication? Specifically: does decay scale with original-paper evidence strength (t-stat), with strategy volatility (arbitrage-cost proxy), and with attention (citations)?

## Data
Chen & Zimmermann Oct 2025 release, already cached (`datasets/chen_zimmermann_oct2025.md`):
- `datasets/raw/PredictorPortsFull.parquet`, LS ports only, through 2024-12.
- `datasets/raw/SignalDoc.csv` for sample dates, publication year, `T-Stat` (original paper), `GScholarCites202509`, `Cat.Data`, `Stock Weight`.

Panel construction identical to EXP-001/EXP-003: predictors with `Cat.Signal == "Predictor"`, `Predictability in OP ∈ {1_clear, 2_likely}`, non-missing sample/publication years; windows in_sample / post_sample / post_pub by calendar year against SampleStartYear / SampleEndYear / Year; pre-sample months dropped; ≥ 12 months in in_sample and in post_pub. **Additional filter for this experiment: non-missing OP `T-Stat`** (188 of 212 before the month filters). Predictors excluded by that filter are counted and their window means reported, so the selection is visible.

## Characteristics (all computed once per predictor, then z-scored across the final estimation sample)
| Name | Definition | Transform |
|------|-----------|-----------|
| `op_t` | `T-Stat` from SignalDoc (original paper) | z-score |
| `vol` | std dev of monthly LS return over the predictor's in-sample window | log, then z-score |
| `cites` | `GScholarCites202509` | log, then z-score (exploratory) |
| `rt` | realized in-sample t-stat of the LS mean (robustness contrast for `op_t`) | z-score |

## Estimation
All regressions: predictor fixed effects via within-transformation, month-clustered SEs (same machinery as EXP-001/003).

- **E1 (primary):** `ret_it = a_i + b1·ps + b2·pp + g1·(ps×op_t) + d1·(pp×op_t) + g2·(ps×vol) + d2·(pp×vol)`. P1 and P2 are read off `d1` and `d2`.
- **E2 (sorts, for readability):** terciles by `op_t` and, separately, by `vol`; window means per tercile with month-clustered SEs. P1's sort statement is read here.
- **E3 (exploratory):** E1 plus `(ps, pp) × cites` — P3.
- **E4 (one-at-a-time):** each characteristic's interaction alone, to expose collinearity between `op_t` and `vol`.

## Robustness (registered now, run regardless of E1's outcome)
- **R1:** E1 + EXP-003's registered era dummies (1993/2001/2011/2020 cuts) — does heterogeneity survive calendar controls?
- **R2:** E1 + `(pp × pubyear_z)` — cohort trend control (older papers have higher cites, possibly different t-hurdles).
- **R3:** replace `op_t` with realized in-sample t (`rt`). A materially stronger interaction for `rt` than `op_t` is evidence that mechanical shrinkage contributes to the heterogeneity.
- **R4:** winsorize monthly returns at 1/99 pct within predictor (as EXP-001 R3).
- **R5:** `1_clear` predictors only.

## Outputs
`results/regressions.csv` (all specs), `results/terciles.csv`, `results/characteristics.csv` (per-predictor characteristics + window means, for the scatter), `results/run_log.txt`, two figures (window means by OP-t tercile; per-predictor decay vs OP t-stat).

## Decision rules (from HYP-005)
- P1 passes iff `d1 ∈ [−0.30, −0.05]` with |t| ≥ 2 in E1 **and** top-tercile decline ≥ 1.5× bottom-tercile decline in E2.
- P2 passes iff `d2 ∈ [−0.05, +0.25]` in E1; it fails if `d2 < −0.15` with |t| ≥ 2.
- P3 (direction only): sign of the `pp×cites` coefficient in E3.
- P4: if all interaction |t| < 1 in E1/E3 and terciles are flat, declare decay homogeneous and demote HYP-005 (that outcome goes to `failed_experiments/`).

## What this experiment does *not* test
Placebo spillover (reserved: EXP-004, researcher-led), stock-level arbitrage costs (no holdings data), international decay (no non-US data yet).

## Connections
`hypotheses/HYP-005-decay-heterogeneity.md` · `experiments/EXP-001-anomaly-decay/design.md` (panel construction) · `experiments/EXP-003-calendar-vs-event-time/design.md` (era bins) · `knowledge_graph/anomaly-decay-thread.md`
