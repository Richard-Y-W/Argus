# HYP-010 — Value weighting increases post-publication decay within signal

*Registered 2026-07-15 before analysis. AI-led.*

## Motivation and prior

EXP-009 found a large raw VW/EW decay gap, but only across different signals and therefore rejected a weighting interpretation. The official Chen–Zimmermann alternative portfolios now permit the same signal to be implemented both equal weighted and value weighted. If publication-induced arbitrage concentrates in liquid, scalable stocks, the value-weighted version should retain less of its in-sample return after publication.

Relevant prior evidence is McLean and Pontiff (2016), the publication-decay replication in EXP-001, and the composition failure in EXP-009. This is an association test: weighting changes stock exposure, not just scalability, and no capital-flow or price-impact quantity is observed.

## Registered predictions

- **P1 primary:** among paired signals with positive EW and VW in-sample means above 0.10% per month and at least 12 observations in both the in-sample and post-publication windows, `VW proportional decay - EW proportional decay` is at least +0.10 with a two-sided paired t-statistic of at least 2.0.
- **P2 levels discriminator:** the paired difference-in-differences, `(VW post-publication - VW in-sample) - (EW post-publication - EW in-sample)`, is negative with |t| >= 2.0.
- **P3 breadth:** more than 55% of paired signals have greater proportional decay under VW.
- **P4 robustness:** P1 remains positive under 5/95 winsorization of the paired differences and in the `1_clear` reproduction subset.
- **Falsifier:** P1 misses either its magnitude or inference threshold, or its sign reverses in either registered robustness sample.

## Data, alternatives, and risk

Required data are the October 2025 Chen–Zimmermann `deciles_ew` and `deciles_vw` LS portfolios, SignalDoc dates, and the fixed 2024-12 panel end. Alternative explanations include microcap composition, different exposure strength, transaction costs, stale prices, and errors in annual publication timing. Expected failure probability: 55%. Novelty: modest; learning value: high because pairing directly repairs EXP-009's confounding. Practical value is low without costs and capacity data.

## Internal debate

- **Optimist:** within-signal pairing removes the most obvious author-choice composition problem in EXP-009.
- **Skeptic:** EW/VW changes are not a clean intervention on arbitrage capacity and ratios can explode near zero.
- **Statistician:** require both denominators above 0.10, report a levels DiD, winsorize paired differences, and expose breadth rather than relying on a mean alone.
- **Economist:** a VW result would be consistent with liquidity-mediated correction, not proof that arbitrage capital caused it.
- **Portfolio manager:** gross decile spreads cannot establish implementability; EW may be dominated by costly microcaps.
- **ML researcher:** do not tune thresholds or add subgroups after observing the paired outcomes.

The hypothesis survives as a cheap discriminator with deliberately bounded interpretation.

## Connections

`experiments/EXP-010-within-signal-weighting-decay/design.md` · `failed_experiments/EXP-009-weighting-and-decay.md` · `datasets/chen_zimmermann_oct2025.md` · McLean and Pontiff (2016)
