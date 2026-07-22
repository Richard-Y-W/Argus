# HYP-021 — No single factor carries pooled US publication decay

*Registered 2026-07-21 before computing leave-one-factor-out outcomes. AI-led.*

## Motivation and prediction

A precise pooled coefficient can still be fragile if one factor with unusual returns or a long history carries the result. A leave-one-factor-out audit tests single-factor influence without choosing exclusions after seeing outcomes.

P1: every leave-one-factor-out post-publication coefficient is at most -0.10 percentage points per month. P2: the largest absolute shift from the full-sample coefficient is no more than 0.03 percentage points per month. P3: the range across leave-one-out coefficients is no more than 0.05 percentage points per month. Survival requires all three. Any non-negative leave-one-out coefficient is a falsifier.

## Alternatives and limits

Survival rules out single-factor dominance only. It does not rule out influence by a correlated family of factors, common metadata error, or common market structure. This is a stability audit, not new mechanism evidence.

## Data, debate, and value

Pinned JKP US panel, EXP-016 eligibility, factor fixed effects, and month-clustered covariance. The Optimist expects negligible shifts; the Skeptic expects one extreme factor to matter; the Statistician freezes deletion units and thresholds; the Economist warns that stable association is not causal; the Portfolio Manager sees no tradability result; the ML Researcher prohibits iterative exclusion.

## Connections

EXP-016 · EXP-020 · `experiments/EXP-021-us-decay-influence-audit/design.md`
