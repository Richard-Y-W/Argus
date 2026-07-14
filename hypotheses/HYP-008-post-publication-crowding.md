# HYP-008 — Publication increases common predictor exposure

*Registered 2026-07-14 before analysis. AI-led.*

If common arbitrage capital adopts published signals, a predictor should become more correlated with the return of predictors already public at its publication date. For each signal, compare correlation over the 60 months before publication with the first 60 months after it, using an equal-weighted composite of earlier-published predictors and requiring 36 observations and at least five composite members per month.

- **P1:** Mean post-minus-pre correlation change for predictors >= +0.05 with |t| >= 2.
- **P2:** At least 60% of predictors have positive changes.
- **P3 negative control:** Placebo mean change is smaller than predictor change by >= 0.04 and placebo change has |t| < 2.
- **Falsifier:** P1 fails and placebos change similarly or more.

Shared factors, changing composition, and annual dates remain alternative explanations. Expected failure probability 55%; novelty modest; learning value high.

## Connections

McLean–Pontiff correlation result · EXP-004 · `experiments/EXP-008-post-publication-crowding/design.md`
