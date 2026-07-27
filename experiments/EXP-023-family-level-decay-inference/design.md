# EXP-023 — Registered design: family-level exact inference

*Registered 2026-07-26 before computing dependence outputs. AI-led.*

Reuse EXP-022 assignments without modification. Average factor contrasts within each cluster, weight the 13 cluster means equally, and enumerate every sign vector in `{−1,+1}^13`. The two-sided p-value is the share of permuted absolute grand means at least as large as observed, including equality. Report every cluster's size, mean, median, and negative-factor share. No normal approximation is part of the decision rule.

## Connections

HYP-023 · EXP-020 · EXP-022 · EXP-024
