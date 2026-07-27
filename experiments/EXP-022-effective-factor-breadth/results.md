# EXP-022 — Nominal factor count overstates independent breadth

## Verdict

**HYP-022 survives all registered rules.** The 141 eligible factors contain an estimated **12.99 effective correlation dimensions**, only 9.2% of the nominal count.

## Results

Pre-publication pair coverage is 97.8%. Median regularized correlation is 0.325 within the frozen 13-cluster partition and -0.032 between clusters, a 0.356 gap. Effective rank is below both 70 and half the nominal count; the >100 falsifier does not fire.

Cluster sizes are highly uneven (1 to 59), reinforcing why factor count is not evidence count. This result downgrades the interpretation of EXP-020's conventional factor-level t-statistic; it does not negate the factor-weighted point estimate.

## Adversarial review

- Empirical clusters are not named economic themes and must not be interpreted as such.
- Zero-filling 2.2% of insufficient-overlap pairs, 10% identity shrinkage, and PSD projection are frozen regularization choices.
- Effective rank diagnoses redundancy; it neither supplies a valid p-value nor identifies trading.

## Reproduction and connections

Run `python experiments/EXP-022-effective-factor-breadth/analysis.py`. HYP-022 · EXP-020 · EXP-023
