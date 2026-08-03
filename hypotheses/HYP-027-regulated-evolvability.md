# HYP-027 — Regulated evolvability from observable environmental distance

**Status:** rejected by EXP-027  
**Registered:** 2026-08-03 before EXP-027 execution  
**Attribution:** Collaborative

## Question

Can a causal environmental-distance gate choose between inherited local mutation, mixed search, and global restart better than any fixed search policy across regime changes of different structural magnitude?

## Mechanism

Parental genomes should remain informative after small changes but become liabilities after large changes. Regulated evolvability maps an observed standardized change score to search radius:

- distance < 1.25: local mutation;
- 1.25 <= distance < 2.50: 75% descendants / 25% global immigrants;
- distance >= 2.50: global restart.

The score uses lagged changes in return means, volatilities, correlations, and first-order autocorrelation. No outcome or true regime label enters routing.

## Alternatives

1. Distance estimates are too noisy and delayed to route search.
2. Global restart dominates because the genome space is small.
3. Local mutation dominates because all registered families share the same phenotype class.
4. A fixed hybrid is more stable than switching policies.
5. Any apparent success is threshold luck or synthetic-family engineering.

## Predictions

- **P1:** gate 252-day cumulative net return exceeds always-local evolution; the family-stratified paired-bootstrap 95% lower bound for gate minus evolution is above zero.
- **P2:** gate return exceeds always-global random restart under the same rule.
- **P3:** gate return exceeds the fixed 75/25 quality hybrid under the same rule.
- **P4:** routing responds monotonically to true family severity: the mean global-restart share is strictly ordered `small_drift < moderate_rotation < mean_reversion < correlation_break`.
- **P5:** gate annualized 5% expected shortfall is no worse than the best fixed method by more than 0.05 annualized return units.

All five must pass. Route diagnostics cannot rescue failed performance predictions.

## Identification boundary

The experiment tests one frozen distance statistic, threshold pair, genome, and simulator class. It cannot establish an optimal gate, market alpha, literal biological regulation, or external validity.

## Connections

EXP-025 · EXP-026 · `knowledge_graph/financial-genetics-thread.md`
