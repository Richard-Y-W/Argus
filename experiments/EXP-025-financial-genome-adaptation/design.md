# EXP-025 — Registered design: inherited local mutation

**Registered:** 2026-08-02 before execution  
**Stage:** synthetic methods experiment  
**Attribution:** Collaborative

## Data-generating process

Each run contains 756 daily observations for three risky assets plus cash. Days 0–251 are a common warm-up regime; the environment changes at day 252. Days 252–503 are available sequentially for adaptation and evaluation. Days 504–755 form the scored post-change period. Strategies receive only information dated before each position is applied.

Daily risky returns follow a multivariate AR(1):

\[
r_t=\mu+\phi\odot(r_{t-1}-\mu)+\epsilon_t,
\qquad \epsilon_t\sim N(0,D\Sigma D).
\]

The development family changes trend persistence and asset leadership. The untouched confirmation family additionally reverses the equity/bond-style correlation and changes relative volatility. Development seeds are 0–9; confirmation seeds are 10,000–10,029. Confirmation outcomes may be inspected only after code behavior is checked on development seeds.

## Genome

`signal_horizon` is an integer in [5, 160]; `vol_horizon` in [10, 80]; `risk_target` in [0.05, 0.15]; `asset_cap` in [0.35, 0.85]; `drawdown_threshold` in [0.04, 0.20]. A genome holds long positions only in assets with positive trailing mean return, weights them by inverse trailing volatility, clips per-asset weights, scales to its risk target with a leverage ceiling of 1, and halves risky exposure when the trailing 63-day drawdown of the equal-weight risky-asset benchmark exceeds its threshold. Positions use lagged observations. Cash earns zero.

## Population and equal search budget

- Initial population: 12 genomes drawn once per run from the same global prior.
- Adaptation every 21 days from day 252 through day 503.
- Candidate evaluation: trailing 126 days ending before deployment.
- Fitness: annualized mean net return minus 2 times annualized downside deviation minus 0.25 times annualized turnover.
- Transaction cost: 5 basis points per unit one-way turnover.
- At each adaptation, both methods evaluate exactly 48 new candidates plus the same 12 incumbents.
- **Evolution:** each incumbent produces four children. Each child mutates exactly one uniformly selected gene using zero-mean Gaussian perturbation (`signal_horizon` SD 15, `vol_horizon` SD 8, `risk_target` SD 0.015, `asset_cap` SD 0.08, `drawdown_threshold` SD 0.025), clipped to the registered bounds.
- **Random restart:** 48 candidates are independent draws from the global genome prior.
- Each method retains the top 12 candidates by trailing fitness. Deployed weights are the equal-weight average phenotype of its 12 retained genomes.
- **Static:** retains the initial population and never searches.
- **Oracle:** at each adaptation selects from a fixed 100-genome pool using the next 21 days; it is an infeasible diagnostic upper bound and defines regret only.

Random restart and evolution share the market path, initial population, transaction-cost rule, and candidate count. Candidate randomness uses separate deterministic streams.

## Outcomes

Primary scored interval: days 504–755.

- cumulative log-return regret relative to the oracle;
- recovery time: first scored day on which cumulative net return regains its value at day 503, capped at 252 days;
- annualized realized volatility;
- annualized historical expected shortfall of daily net return at 5%;
- annualized turnover;
- mean pairwise genome distance after range normalization;
- total evaluated candidates.

Uncertainty uses a deterministic paired percentile bootstrap with 10,000 resamples over the 30 confirmation seeds. The paired differences are formed before resampling.

### Pre-execution feasibility amendment

The initial registration specified 40 development seeds, 200 confirmation seeds, and a 2,000-genome oracle pool. Deterministic unit-test timing showed that the transparent reference implementation would require hours. Before any development or confirmation outcome was generated, the counts were reduced to 10, 30, and 100 respectively. The mutation-versus-random candidate budget, algorithms, endpoints, thresholds, seed ranges, and joint decision rule were not changed. The amendment materially lowers precision and makes the run a pilot; it does not favor either feasible contestant.

After P1–P4 were generated, the audit found that annual turnover—registered as a diagnostic but not a decision endpoint—was used in costs and fitness but omitted from `seed_metrics.csv`. The output layer was repaired to export implied one-way turnover from gross-minus-net returns. No algorithm, path, endpoint, threshold, or decision rule was changed. The regenerated file necessarily receives a new hash.

## Decision rule

P1–P4 are exactly those in HYP-025 and must all pass. P1 and P2 use two-sided 95% paired bootstrap intervals and require the lower bound above zero. No correction is added because the claim requires their intersection rather than accepting any one endpoint.

## Robustness and audit

Registered diagnostics, not substitute endpoints:

1. development-family results;
2. static and oracle bounds;
3. search-budget equality assertion;
4. deterministic rerun hash;
5. no-look-ahead unit tests for weights;
6. mutation-bound and one-gene-only tests;
7. performance separated from average volatility and turnover.

## Identification boundary

This experiment can establish only whether this particular local mutation kernel helps in these synthetic families. It cannot establish that markets have DNA, that real strategies reproduce biologically, that the design earns alpha, or that mutation beats other adaptive optimizers.

## Connections

`hypotheses/HYP-025-financial-genome-adaptation.md` · `ideas/2026-08-02-lineage-aware-financial-immune-system.md` · EXP-011/012
