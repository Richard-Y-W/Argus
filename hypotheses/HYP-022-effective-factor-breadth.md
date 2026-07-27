# HYP-022 — Nominal factor count materially overstates independent breadth

*Registered 2026-07-26 before computing factor correlations or family outcomes. AI-led.*

## Motivation and predictions

EXP-020 treats 141 factor contrasts as sampling units. Related constructions can make that count misleading. Using only each factor's pre-publication monthly returns, estimate the correlation matrix and its participation-ratio effective rank, `(sum eigenvalues)^2 / sum squared eigenvalues`.

P1: effective rank is at most 70. P2: it is at most half the nominal eligible-factor count. P3: median within-cluster correlation from a frozen 13-cluster solution exceeds median between-cluster correlation by at least 0.10. Survival requires all three. Effective rank above 100 is a falsifier.

## Alternatives, debate, and limits

Low effective rank can reflect shared economic exposures, construction overlap, or common shocks; it does not identify publication effects. The Skeptic warns that pairwise histories are unbalanced; the Statistician requires at least 60 overlapping pre-publication months, zero-fills unavailable off-diagonals, projects to the nearest positive-semidefinite correlation matrix, and reports coverage. The Economist rejects interpreting empirical clusters as structural themes. The ML Researcher prohibits choosing cluster count or thresholds after inspection.

## Data and value

Pinned JKP US value-weighted monthly factors and frozen EXP-016 eligibility. Moderate novelty and high diagnostic value; no trading claim.

## Connections

EXP-020 · EXP-021 · `experiments/EXP-022-effective-factor-breadth/design.md`
