# EXP-030 — Registered design: invariant-restoring defense

**Registered:** 2026-08-05 before execution  
**Stage:** externally specified synthetic mechanism benchmark  
**Attribution:** Collaborative

## System

Simulate six strategy modules for 120 days. Initial gross exposures are 40 each, equity is 100, liquid buffer is 32, and each module contributes `0.08 * exposure` to projected stressed outflows plus a system base of 5.

Protected invariants:

- gross leverage `sum(exposure) / equity <= 3.0`;
- simplified liquidity coverage `liquid_buffer / projected_stressed_outflows >= 1.0`.

This is inspired by prudential backstop logic but is not a bank, accounting, or Basel implementation.

Returns are iid multivariate Student-t innovations, not EXP-025–027's AR(1) family. Selling exposure repays funding, releases 15% of the reduction into the liquid buffer, reduces associated stressed outflows, and costs `0.2% * (1 + current stress multiplier)` of reduction against equity.

## Frozen pathology families

Use 100 independent seeds in each family:

1. `liquidity_drain`: module 0 funding outflow rises sharply on days 30–59;
2. `leverage_cancer`: module 1 has positive private drift while financed exposure and funding needs grow on days 20–69;
3. `systemic_correlation`: all modules experience correlated heavy losses on days 40–69;
4. `combined`: module 2 liquidity damage overlaps a shorter systemic shock on days 45–74;
5. `benign_volatility`: volatility rises without an intended funding or leverage pathology, testing false intervention.

Policies receive returns and observable state only, never the family or culprit labels.

## Policies

- `none`: no intervention;
- `proportional`: after an actual breach, reduce every exposure proportionally in 5% steps until leverage <=2.9 and liquidity coverage >=1.05;
- `vol_target`: proportionally scale exposures when trailing 20-day annualized portfolio volatility exceeds 18%, targeting 15%;
- `liquidate`: after an actual breach, reduce every exposure by 90%;
- `immune`: at leverage >2.9 or liquidity coverage <1.05, rank modules by equal-weighted normalized exposure contribution, stressed-outflow contribution, and nonnegative trailing 10-day loss contribution. Reduce the highest-ranked module in 5% system-exposure increments, moving to the next only if needed, until leverage <=2.85 and liquidity coverage >=1.10.

No policy observes hidden pathology labels. Actions occur after the day's state update and affect subsequent days.

## Endpoints

Primary endpoint is 120-day invariant-violation area:

`sum_t[max(leverage_t-3,0) + max(1-LCR_t,0)]`.

Secondary endpoints are days in breach, time from first breach to five consecutive healthy days, total exposure reduction, reduction applied to modules not designated by the simulator as pathological, terminal equity, maximum equity drawdown, and false-action days when neither invariant was breached.

Use 10,000 family-stratified paired bootstrap resamples of seed-level differences.

## Decision rule

Classify `SUPPORTED WITH LIMITS` only if:

1. immune minus proportional violation area has a 95% interval below zero;
2. immune minus volatility-target violation area has a 95% interval below zero;
3. immune violation area is no more than 0.02 above liquidation on average;
4. immune reduces healthy-module exposure less than both proportional and liquidation, with both 95% intervals below zero;
5. immune terminal equity exceeds liquidation, with a 95% interval above zero;
6. immune false-action days average below 10% of the horizon; and
7. immune has lower violation area than proportional in at least three of the four non-benign pathology families.

All conditions are joint. Benign-family intervention and systemic-family failure are reported even if the joint rule passes.

## Evidence limits

This benchmark can validate internal logic only. Pathologies, balance-sheet mechanics, liquidation rules, and thresholds are designed rather than observed. A pass would justify external validation, not an edge, causal financial claim, or production control.

## Connections

`hypotheses/HYP-030-invariant-restoring-financial-defense.md` · EXP-029

