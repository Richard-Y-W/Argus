# HYP-020 — US publication decay survives factor-balanced estimation

*Registered 2026-07-21 before computing factor-balanced outcomes. AI-led.*

## Motivation and prediction

EXP-016 pools factor-months, so factors with longer histories receive more weight. A broad publication-decay pattern should remain when each eligible factor contributes one equally weighted post-publication-minus-in-sample contrast.

P1: the equal-factor mean contrast is at most -0.10 percentage points per month. P2: its conventional cross-factor t-statistic is at most -2.0. P3: at least 55% of factor-level contrasts are negative. Survival requires all three. A non-negative equal-factor mean is a falsifier.

## Alternatives and limits

Failure would show that the pooled estimate depends materially on unequal time-series length or a narrow tail. Survival establishes breadth across factor summaries, not publication-induced trading or a causal mechanism. The cross-factor t-statistic treats factors as sampling units and is descriptive when factor dependence remains.

## Data, debate, and value

Pinned JKP US monthly value-weighted factors and EXP-016 eligibility rules; low data difficulty, moderate identification value. The Optimist expects broad negative contrasts; the Skeptic expects long-history factors to dominate EXP-016; the Statistician requires one frozen contrast per factor and no trimming; the Economist rejects causal language; the Portfolio Manager notes the absence of costs and capacity; the ML Researcher prohibits threshold searches.

## Connections

EXP-016 · `experiments/EXP-020-factor-balanced-us-decay/design.md`
