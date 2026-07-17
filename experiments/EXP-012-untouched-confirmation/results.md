# EXP-012 — Consumed versus untouched holdout

## Verdict

**HYP-012 survives within its idealized null scope.** All four registered predictions passed. The result supports strict holdout governance, not a claim that three-way splitting alone solves backtest overfitting.

## Results

Across 100,000 runs and 100 null candidates per run, selecting on training data and reporting a favorable validation statistic produced a 5.145% false claim rate (Monte Carlo SE 0.070 percentage points). Requiring that same candidate to pass an independent confirmation statistic reduced the unconditional false claim rate to 0.274% (SE 0.017 percentage points).

The relative reduction was 94.67%. Only 5.33% of validation-pass cases also passed confirmation. P1–P4 all pass their registered bounds.

## Adversarial review and limitations

- Under independence and a 5% cutoff, the joint rate is expected to be about 0.25%; the simulation verifies implementation and sampling variation rather than discovering a surprising theorem.
- Confirmation protects only while untouched. Repeatedly checking it, modifying the strategy, and rerunning converts it into another selection sample.
- The experiment measures type-I error under a complete null. It does not quantify power when a weak signal exists or choose an optimal data split.
- Candidate dependence, time-series dependence, heavy tails, costs, and adaptive analyst behavior are absent.

## What was learned

A holdout is a consumable research asset. Validation used to decide whether a candidate looks promising is not final confirmation. Under this clean null, a second independent pass turns a roughly 1-in-20 false claim process into roughly 1-in-365, at the cost of rejecting nearly 95% of validation-pass null candidates. Power and realistic dependence remain open.

## Reproduction

Run `python experiments/EXP-012-untouched-confirmation/analysis.py`. Fixed seed: 20260717. Outputs are in `results/`.

## Connections

`hypotheses/HYP-012-untouched-confirmation.md` · EXP-011 · White (2000) · Bailey et al. (2016)
