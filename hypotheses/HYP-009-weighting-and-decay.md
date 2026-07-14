# HYP-009 — Value-weighted implementations decay more

*Registered 2026-07-14 before analysis. AI-led.*

Value-weighted portfolios emphasize larger, more liquid stocks and may be more scalable for arbitrage capital. The unregistered EXP-005 summary showed roughly 94% versus 55% proportional decay for VW versus EW constructions.

- **P1 primary:** VW indicator coefficient on proportional decay >= +0.20 with t >= 2 after controlling for in-sample mean, publication year, and log post-publication months; require in-sample mean > 0.10.
- **P2:** VW post-publication mean remains lower than EW after controlling for in-sample mean.
- **P3 robustness:** P1 remains positive under 5/95 winsorization and clear-only restriction.
- **Falsifier:** Primary coefficient is insignificant and robustness is unstable.

This is a preregistered follow-up to a seen descriptive result, not an independent discovery. Stock Weight is paper-chosen and only about 28 qualifying signals are VW; causal language is forbidden. Expected failure probability 60%.

## Connections

EXP-005 descriptive check · limits-to-arbitrage lineage · `experiments/EXP-009-weighting-and-decay/design.md`
