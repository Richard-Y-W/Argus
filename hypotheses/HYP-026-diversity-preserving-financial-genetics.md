# HYP-026 — Diversity-preserving financial genetics

**Status:** rejected by EXP-026  
**Registered:** 2026-08-02 before EXP-026 execution  
**Attribution:** Collaborative

## Question

Can a population combining inherited local mutation, globally novel immigrants, and an explicit phenotype-diversity reserve outperform pure local evolution and pure global random search immediately after structural regime changes?

## Motivation from EXP-025

EXP-025 found lower confirmation regret for local mutation but rejected its recovery hypothesis. Local evolution compressed normalized genome diversity from 0.808 to 0.213. The next uncertainty is whether that concentration represents efficient specialization or harmful premature convergence.

## Mechanism and alternatives

The proposed mechanism is an exploration–exploitation balance: descendants preserve locally useful structure; immigrants reach distant genome regions; phenotype-reserved slots prevent high-fitness but behaviorally redundant lineages from displacing every alternative.

Alternatives are:

1. local mutation alone is sufficient;
2. global random search is sufficient;
3. diversity sacrifices too much fitness;
4. any benefit comes from the 25% immigrant mixture, not phenotype-aware selection;
5. synthetic families favor the registered genome vocabulary.

## Predictions

- **P1:** across all untouched paths, diversity-hybrid cumulative net return over the 252-day post-change year exceeds local evolution; the family-stratified paired-bootstrap 95% interval for hybrid minus evolution is strictly above zero.
- **P2:** diversity-hybrid cumulative net return exceeds random restart under the same rule.
- **P3:** during the first 126 post-change days, diversity-hybrid is not economically inferior to either baseline by more than 0.005 cumulative log-return. Both paired-bootstrap lower bounds must exceed -0.005.
- **P4:** diversity-hybrid's mean terminal phenotype diversity is at least 25% higher than local evolution's in every confirmation family.
- **P5:** diversity-hybrid annualized 5% expected shortfall is no worse than the better of local evolution and random restart by more than 0.05 annualized return units.

All five must pass. The quality-only hybrid is an ablation and cannot rescue a failed joint rule.

## Identification boundary

This is a synthetic optimizer comparison. It cannot establish literal financial DNA, market alpha, practical profitability, or superiority over Bayesian optimization and reinforcement learning.

## Connections

EXP-025 · EXP-011/012 · `knowledge_graph/financial-genetics-thread.md`
