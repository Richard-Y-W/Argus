# EXP-021 — No single factor carries pooled US decay

## Verdict

**HYP-021 survives all registered rules.** The pooled coefficient is insensitive to deleting any one of the 141 eligible factors.

## Results

The full-sample post-publication coefficient is -0.1643 percentage points per month (t = -2.97). Across every leave-one-factor-out refit, it ranges only from **-0.1698 to -0.1585 pp/month**. The maximum absolute shift is **0.0058 pp/month**, and the complete range is **0.0112 pp/month**. Deleting `seas_2_5na` produces the largest absolute shift.

Every deletion estimate remains below the registered -0.10 threshold; the maximum shift is far below 0.03; and the range is below 0.05. The non-negative falsifier never fires.

## Adversarial review

- Leave-one-out stability rules out single-factor dominance, not dominance by a correlated family.
- All refits retain the same annual publication metadata and common data construction.
- Influence stability makes the return association more credible but adds no causal or trading-quantity evidence.
- The named most-influential factor is a diagnostic, not a justified target for exclusion.

## Reproduction and connections

Run `python experiments/EXP-021-us-decay-influence-audit/analysis.py`. HYP-021 · EXP-016 · EXP-020
