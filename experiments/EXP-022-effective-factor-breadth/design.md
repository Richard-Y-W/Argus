# EXP-022 — Registered design: effective factor breadth

*Registered 2026-07-26 before computing dependence outputs. AI-led.*

Use EXP-016 eligible factors. For every factor pair, correlate returns only in months that are in-sample or post-sample for both factors and require 60 overlapping months. Set unavailable off-diagonal correlations to zero, shrink the matrix 10% toward identity, project negative eigenvalues to `1e-8`, and renormalize to a correlation matrix. Compute participation-ratio effective rank. Cluster `sqrt(0.5 * (1-rho))` by average linkage into exactly 13 clusters. Report pair coverage, cluster sizes, and within/between median correlations. No alternative shrinkage, overlap, distance, linkage, or cluster count enters the decision.

## Connections

HYP-022 · EXP-020 · EXP-023
