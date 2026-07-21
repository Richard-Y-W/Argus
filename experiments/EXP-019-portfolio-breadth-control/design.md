# EXP-019 — Registered design: portfolio-breadth control

*Registered 2026-07-21 before computing results. AI-led.*

Reuse EXP-016's eligible US observations. Define `log_n_stocks = log(n_stocks)` and center it within factor. Estimate (A) the frozen window-only factor-fixed-effect model, (B) window indicators plus centered log breadth, and (C) model B plus interactions of centered breadth with post-sample and post-publication indicators. Cluster by month. Report observation loss, stock-count summaries, coefficients, t-statistics, and attenuation relative to the frozen benchmark. No transformations or thresholds may change after execution.

## Connections

`hypotheses/HYP-019-portfolio-breadth-control.md` · EXP-016
