# EXP-001 — Design: Three-window replication of McLean & Pontiff (2016)

*Registered 2026-07-10, before any analysis code was written. Hypothesis: `hypotheses/HYP-001-decay-replication.md`.*

## Objective
Estimate mean long-short returns of published US cross-sectional predictors in three windows — in-sample, post-sample-pre-publication, post-publication — on Chen–Zimmermann (Oct 2025) data, and compare decay magnitudes to M&P's 26% / 58%.

## Data
`datasets/raw/PredictorPortsFull.parquet` (`port == 'LS'`, returns in %/month) + `datasets/raw/SignalDoc.csv`. Provenance: `datasets/chen_zimmermann_oct2025.md`.

## Sample construction (fixed before running)
1. Keep signals with `Cat.Signal == 'Predictor'`.
2. Keep `Predictability in OP` in {`1_clear`, `2_likely`} (robustness: `1_clear` only).
3. Require non-missing `SampleStartYear`, `SampleEndYear`, `Year`.
4. Window boundaries per predictor *i*:
   - In-sample: `[Jan 1 SampleStartYear_i, Dec 31 SampleEndYear_i]`
   - Post-sample: `(Dec 31 SampleEndYear_i, Dec 31 Year_i]`
   - Post-publication: `(Dec 31 Year_i, 2024-12-31]`
   - If `Year_i <= SampleEndYear_i` (published before/as sample ended), the post-sample window is empty; predictor contributes to in-sample and post-publication only.
5. Require ≥ 12 monthly LS observations in-sample and ≥ 12 post-publication; post-sample column additionally requires ≥ 12 post-sample months.

**Known deviation from M&P:** publication dated to Dec 31 of publication year (annual resolution) vs. M&P's issue dates → measured publication effect is attenuated. Direction of bias stated in advance: toward *underestimating* the publication effect.

## Estimands and estimators
- **E1 (primary, M&P Table 2 analog):** pooled panel regression on predictor-month LS returns:
  `ret_it = α_i + β₁·PostSample_it + β₂·PostPub_it + ε_it`
  with predictor fixed effects α_i and standard errors clustered by month. Decay percentages: β₁ and β₂ relative to the (FE-weighted) mean in-sample return; report as −β/mean_IS.
- **E2 (descriptive):** per-predictor window means, then cross-predictor averages (equal weight per predictor); report distribution (median, IQR) as well as mean.
- **E3 (existence of residual returns, P3):** mean post-publication return with month-clustered SE; test H0: mean = 0.

## Registered predictions (from HYP-001)
P1: post-sample decline in [10%, 45%]. P2: post-publication decline in [40%, 75%] and > P1. P3: post-pub mean > 0, p < .05. P4: falsifiers as stated in HYP-001.

## Robustness (all decided now)
R1. `1_clear` predictors only.
R2. Drop predictors with in-sample mean LS ≤ 0 in our data (reproduction failures masquerading as decay).
R3. Winsorize monthly LS returns at 1%/99% within predictor.
R4. Exclude the post-2020 COVID/meme era (end panel 2019-12) to check recent-regime sensitivity.
R5. Balanced-window check: only predictors with ≥ 36 months in every window.

## What we will NOT do
No specification search beyond R1–R5. No cost modeling (returns are gross; results language must say so). No claim about exploitability. No extension analyses (event-time profiles, placebos) — those are EXP-002 candidates regardless of how EXP-001 turns out.

## Success criteria
Replication succeeds if the qualitative ordering (IS > PS > PP > 0) holds with statistical support and magnitudes fall in the registered ranges. A failure on magnitudes with the ordering intact is a *partial* replication and gets documented as such — not massaged.

## Engineering
Single deterministic script `analysis.py` (no notebook), config constants at top, outputs written to `results/` as CSV + figures; figures follow repo dataviz standards. Seed irrelevant (no resampling in primary spec).
