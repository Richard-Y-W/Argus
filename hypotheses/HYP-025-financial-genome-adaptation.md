# HYP-025 — Inherited local mutation after regime change

**Status:** registered for a synthetic methods experiment  
**Registered:** 2026-08-02, before EXP-025 execution  
**Attribution:** Collaborative — Richard proposed the financial-DNA and mutation program; Argus selected and specified the first vertical slice.

## Question

Does bounded local mutation around inherited strategy genomes adapt a population to an unseen regime more efficiently than equally budgeted global random search?

## Mechanism

A surviving genome carries useful partial structure across related environments. Local mutation searches its neighborhood, preserving useful genes while changing a few parameters. It should therefore recover faster than rebuilding a population from unrelated genomes.

## Competing explanations

1. Global random search is equally good once evaluation budgets are matched.
2. Any advantage comes from lower average risk rather than adaptation.
3. Trailing-window selection overfits recent noise.
4. Local inheritance helps only when the new regime resembles the old one and fails under a structurally different confirmation family.

## Genome and phenotype

The fixed-length genome is:

\[
G=(h_s,h_v,\tau,c,\delta),
\]

where \(h_s\) is the trend horizon, \(h_v\) the volatility horizon, \(\tau\) the annual risk target, \(c\) the per-asset cap, and \(\delta\) the drawdown-response threshold. Stable species rules—asset universe, available information, long/cash constraint, cost model, leverage ceiling, and execution timing—cannot mutate.

The phenotype is the daily portfolio-weight and net-return path created by the genome. Genotypic diversity and phenotypic diversity are distinct.

## Predictions

- **P1 (primary):** across the untouched confirmation seeds, evolutionary local mutation has lower mean 252-day post-change regret than equal-budget random restart. A paired 95% bootstrap confidence interval for `random regret - evolution regret` must be strictly above zero.
- **P2:** evolution has shorter median recovery time than random restart, with a paired 95% bootstrap confidence interval for `random - evolution` strictly above zero.
- **P3:** evolution does not obtain its result by taking materially less risk: its mean realized volatility must be at least 90% of random restart's and no more than 110%.
- **P4:** evolution's mean post-change expected shortfall at 5% is no worse than random restart's by more than 5 annualized basis points.

The joint hypothesis is supported only if P1–P4 all pass. There is no alpha, market, or practical-trading claim.

## Search and multiplicity boundary

EXP-025 uses one frozen genome, one mutation kernel, one evaluation budget, one adaptation schedule, one development family, and one untouched confirmation family. All four predictions are jointly required; no alternative parameter grid or subgroup may replace a failed prediction.

## Expected failure probability and value

Failure probability is high (approximately 60–75%). Local mutation is likely to fail after a sufficiently discontinuous regime shift. A rejection would establish that ancestry is not automatically useful and would motivate conditional mutation radius or differentiation rather than unrestricted evolutionary claims.

## Connections

`ideas/2026-08-02-lineage-aware-financial-immune-system.md` · `experiments/EXP-011-search-breadth/` · `experiments/EXP-012-untouched-confirmation/`

