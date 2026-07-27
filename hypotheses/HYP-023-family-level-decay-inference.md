# HYP-023 — US decay survives family-level exact inference

*Registered 2026-07-26 before computing family assignments or outcomes. AI-led.*

## Prediction

Freeze the 13 pre-publication clusters from EXP-022. Compute each factor's post-publication-minus-in-sample mean-return contrast, then one equal-weight mean per cluster. P1: the equal-cluster grand mean is at most -0.10 percentage points per month. P2: at least 9 of 13 cluster means are negative. P3: a two-sided exact sign-randomization test over all `2^13` cluster sign flips has p <= 0.05. Survival requires all three. A non-negative grand mean is a falsifier.

## Debate and limits

Equal cluster weighting prevents large families from dominating but changes the estimand from EXP-020. The exact test assumes cluster-level sign symmetry under the sharp null; learned clusters and only 13 units limit calibration. The Optimist predicts broad family decay; the Skeptic expects one or two crowded families to carry it; the Statistician requires enumeration without Monte Carlo; the Economist and Portfolio Manager prohibit mechanism, cost, or tradability language.

## Connections

EXP-022 · `experiments/EXP-023-family-level-decay-inference/design.md`
