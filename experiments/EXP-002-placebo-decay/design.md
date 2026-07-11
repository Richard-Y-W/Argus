# EXP-002 — Design: Placebo test of publication-timed decay

*Registered 2026-07-11, before any window-level analysis of placebo data. Hypothesis: `hypotheses/HYP-002-placebo-decay.md`.*

**Pre-registration disclosure:** during data-feasibility checks (2026-07-11) we inspected placebo *in-sample* means to verify C&Z's signing convention (mean 0.24%/mo, 68% positive, `4_not` subgroup ≈ 0.06). No post-sample or post-publication quantity was computed before this design was written. The researcher was offered this design as an exercise after EXP-001 and had not responded; Argus designed it autonomously.

## Objective
Estimate the three-window (in-sample / post-sample / post-publication) return pattern for the 114 C&Z placebo signals, and test whether the publication-timed decline measured for predictors in EXP-001 is absent for characteristics that carried no predictive claim.

## Data
`datasets/raw/PlaceboPortsFull.parquet` (`port == 'LS'`, %/month) + `datasets/raw/SignalDoc.csv` placebo rows + the EXP-001 predictor panel for pooling. Provenance: `datasets/chen_zimmermann_oct2025.md`.

## Sample construction (fixed before running; mirrors EXP-001 exactly)
1. Placebos: `Cat.Signal == 'Placebo'` (both `indirect` and `4_not`), non-missing `SampleStartYear`, `SampleEndYear`, `Year`.
2. Window boundaries per signal *i*, identical to EXP-001 step 4 (annual Dec-31 dating; pre-sample months dropped; empty post-sample window if published within sample).
3. ≥ 12 monthly LS observations in-sample and ≥ 12 post-publication; post-sample column additionally requires ≥ 12 post-sample months.
4. Predictors for the pooled DiD: the exact EXP-001 primary sample (212 predictors).

## Estimands and estimators
- **E1 (placebo-only panel):** `ret_it = α_i + β₁·PostSample_it + β₂·PostPub_it + ε_it`, signal FE, SEs clustered by month. Primary readout in **levels** (%/mo). Percent-of-in-sample reported descriptively only.
- **E2 (pooled DiD, primary test for P2):** on predictors + placebos jointly,
  `ret_it = α_i + β₁·PS_it + β₂·PP_it + γ₁·PS_it×Pred_i + γ₂·PP_it×Pred_i + ε_it`,
  signal FE (absorbing the Pred_i main effect), month-clustered SEs. γ₂ is the extra publication-timed decline of predictors over placebos.
- **E3 (descriptive):** per-signal window means; cross-signal mean/median/IQR by group (placebo-indirect, placebo-4_not, predictor).

## Registered predictions (from HYP-002)
P1: |β₂_placebo| < 0.20 %/mo and < half of predictors' 0.37. P2: γ₂ ≥ 0.15 %/mo, t ≥ 2. P3: |β₁_placebo| < 0.15 %/mo. P4: R4's selected placebos show a post-sample decline (direction only; no magnitude registered). P5 falsifier as stated in HYP-002.

## Robustness (all decided now)
R1. `indirect` only (n=100) and `4_not` only (n=14, descriptive — underpowered, no pass/fail).
R2. Winsorize monthly LS at 1/99 within signal.
R3. End panel 2019-12.
R4. **Selection-bias demonstration:** placebos with positive in-sample mean only — expect an *induced* post-sample decline (P4). This subsample conditions on in-sample performance, which is exactly the selection predictors underwent.
R5. Balanced windows: ≥ 36 months in all three windows.

## What we will NOT do
No spillover correction (declared interpretive limit). No cost modeling. No per-placebo storytelling about which "work". No extension to international data. No respecification if results are ambiguous — ambiguity gets written up as ambiguity.

## Success criteria
HYP-002 supported if P1–P3 all pass. Partial support (e.g., P2 passes but P1 fails) documented as partial with the spillover caveat. If P5's falsifier fires, EXP-002 is a *successful experiment that rejects the hypothesis* — it goes to `failed_experiments/` with the calendar-time confound escalated.

## Engineering
`analysis.py` (deterministic, no resampling), reusing EXP-001's window/FE/cluster machinery; outputs to `results/` as CSV + figures via `plots.py`.
