# EXP-014 — Historical truncation does not explain weak international decay

## Verdict

**HYP-014 is rejected and its falsifier fires.** Starting the C&Z US panel in 1986 makes the post-publication coefficient more negative, not 25% smaller.

## Results

The contemporaneously recomputed full-history coefficient is -0.369 percentage points per month (t = -6.49). With a 1986 floor it is **-0.415** (t = -5.67), 12.3% larger in absolute magnitude; with a 1990 floor it grows to -0.473 (t = -5.42). The clear-predictor 1986 result is also -0.472 (t = -5.84). P1, P2, and P4 fail; only P3's negative second-step contrast survives.

## Adversarial review and learning

This rejects a simple history-length explanation for EXP-013. It does not make C&Z and JKP comparable: factor definitions, universes, breakpoints, and portfolio aggregation still differ. Restriction also changes eligible factors and emphasizes later cohorts. The useful result is narrow: JKP's mainly post-1986 coverage cannot explain its smaller ex-US coefficient merely by truncating the C&Z time axis.

## Reproduction

Run `python experiments/EXP-014-coverage-matched-us-decay/analysis.py` against the pinned C&Z files.

## Connections

HYP-014 · EXP-001 · EXP-013 · EXP-015
