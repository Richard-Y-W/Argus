# EXP-026 — Registered design: diversity-preserving financial genetics

**Registered:** 2026-08-02 before execution  
**Stage:** synthetic methods confirmation  
**Attribution:** Collaborative

## Frozen inheritance from EXP-025

EXP-026 reuses without tuning the EXP-025 five-gene representation, global prior, one-gene mutation kernel, long/cash phenotype, 5 bp cost, 12-member population, 48-candidate budget, 126-day trailing fitness window, 21-day adaptation interval, and fitness function.

The common pre-change period is days 0–251. All endpoints are scored immediately after the break on days 252–503 while adaptation continues causally every 21 days. No future-aware oracle is used.

## Untouched families

There is no development-result stage. Unit tests use fixed mechanical fixtures only. Confirmation has three structural families with 12 seeds each:

1. `rotation`, seeds 20,000–20,011: leadership and persistence rotate;
2. `correlation_flip`, seeds 30,000–30,011: equity/bond-style correlation turns strongly positive and volatility ordering changes;
3. `mean_reversion`, seeds 40,000–40,011: all risky assets lose trend persistence, with the prior leader becoming most mean reverting.

The family parameters are fixed in code before execution. Inference resamples seeds independently within each family and averages family means, preventing a family with more paths from dominating.

## Equal-budget contestants

At every adaptation date each method evaluates its 12 incumbents and exactly 48 new candidates:

- `evolution`: four one-gene children per incumbent;
- `random`: 48 independent global-prior genomes;
- `hybrid_quality`: three children per incumbent plus 12 global immigrants, retain the top 12 by fitness;
- `hybrid_diverse`: the same 36 children and 12 immigrants; retain the top eight by fitness, then fill four reserve slots greedily for phenotype distance from candidates whose fitness is at or above the candidate-pool median.

Candidate RNG streams are separate but deterministic. The two hybrid methods receive identically distributed generation rules, not identical candidate realizations.

## Phenotype distance

At each selection date a candidate's phenotype signature is its mean and standard deviation of the three risky-asset weights over the trailing 21 days: a six-element vector. Each component is scaled by its cross-candidate standard deviation at that selection date. Reserve candidates are selected greedily to maximize their minimum Euclidean distance from already retained genomes. Ties use original candidate order.

Terminal phenotype diversity is mean pairwise Euclidean distance between the six raw weight signatures at day 504. All six components are naturally measured as portfolio-weight fractions in [0, 1], so no within-method rescaling is applied. This avoids mechanically normalizing a concentrated population back to unit dispersion.

## Endpoints

- cumulative net log return on days 252–503;
- cumulative net log return on days 252–377;
- annualized realized volatility and historical 5% expected shortfall;
- annualized one-way turnover;
- terminal genome and phenotype diversity;
- candidate count.

Ten thousand deterministic family-stratified paired-bootstrap resamples produce intervals for P1–P3. P4 is a family-by-family ratio of mean phenotype diversity. P5 compares pooled family-balanced mean expected shortfall.

## Decision and audit

P1–P5 must all pass. Tests must establish causal weighting, equal budgets, hybrid composition, reserve fitness floor, and deterministic market paths. The experiment is rejected on any failed prediction. No mutation-scale, immigrant-share, reserve-size, fitness-floor, family, or endpoint change is permitted after execution.

### Execution deviation

The registered numerical run completed and wrote `seed_metrics.csv` and `summary.csv`, but JSON serialization then failed because NumPy boolean objects were passed directly to the standard-library encoder. After outcome computation, the output layer was repaired only to cast decision values to native booleans and support finalization from the already written seed-level CSV. No simulation, selection, endpoint, threshold, or numerical result was rerun or changed for this repair.

## Connections

`hypotheses/HYP-026-diversity-preserving-financial-genetics.md` · EXP-025
