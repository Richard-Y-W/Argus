# EXP-003 — Design: Calendar-time vs event-time decomposition of predictor decay

*Registered 2026-07-11, before any era-controlled regression was run. Hypothesis: `hypotheses/HYP-003-calendar-vs-event-time.md`.*

**Pre-registration disclosure:** the uncontrolled benchmarks (β_ps = −0.247, β_pp = −0.369 for predictors; +0.082/−0.110 for placebos) are known from EXP-001/002. No regression including calendar-era terms has been run on either panel before this design was committed.

## Objective
Decompose the post-publication decline of the 212 C&Z predictors into an event-time component (years since the predictor's own publication) and a calendar-era component shared across predictors; cross-check the era component against the placebo panel.

## Data
Exactly the EXP-001/EXP-002 panels (predictors + placebos, LS %/mo, windows dated as before). No new data. Provenance: `datasets/chen_zimmermann_oct2025.md`.

## Era bins (fixed now, external justification)
`E0` 1926–1992 (base) · `E1` 1993–2000 (pre-decimalization quant expansion) · `E2` 2001–2010 (decimalization, CST break) · `E3` 2011–2019 (post-GFC quant boom) · `E4` 2020–2024 (COVID/meme/rates). Calendar year of the return month decides the bin.

## Event-time bins (fixed now)
In-sample (base) · post-sample (pre-publication) · post-publication split at years since Dec-31-of-publication-year: `pp1` 1–5y · `pp2` 6–10y · `pp3` 11+y.

## Estimands and estimators
All: signal FE (within transformation), SEs clustered by month.
- **E1 (primary):** `ret_it = α_i + β₁·PS_it + β₂·PP_it + Σ_k δ_k·Era_k,t + ε_it` on predictors. Test P1 (β₂ survives) and P2/P3 (δ pattern).
- **E2 (event-time profile):** replace PP with pp1/pp2/pp3, keep era dummies. Test P4.
- **E3 (placebo cross-check):** E1 specification on the placebo panel. Test P6.
- **Descriptives:** predictor-month counts per era × window cell (composition table).

## Registered predictions (from HYP-003)
P1: β₂ ≤ −0.148 (40% of 0.369) with t ≤ −2 under era controls. P2: δ_E2 ≤ 0 with t ≤ −2. P3: δ_E4 > δ_E3. P4: pp2 ≤ pp1 (direction only). P5 falsifier: |t(β₂)| < 1 under era controls. P6: placebo |β_pp| < 0.08 under era controls.

## Robustness (all decided now)
R1. Alternative eras: 5-year bins from 1990 (1926–89 base, 1990–94, …, 2020–24).
R2. Linear calendar trend (year/10) instead of era dummies.
R3. Winsorize 1/99 within signal.
R4. `1_clear` predictors only.

## What we will NOT do
No post-hoc re-binning. No interaction fishing (era × event-time cells). No structural interpretation of any single δ beyond sign/ordering. No claim that the decomposition is identified beyond the registered binning (APC caveat in HYP-003 travels with every number).

## Success criteria
HYP-003 supported if P1–P3 pass. P5 firing sends the experiment to `failed_experiments/` and reopens the causal story. Mixed outcomes documented as mixed; P6 adjudicates between spillover and calendar readings of EXP-002's placebo drift regardless of P1–P3.

## Engineering
`analysis.py` deterministic, reusing the EXP-002 loader; outputs CSVs + run log to `results/`; `plots.py` for the event-time profile figure.
