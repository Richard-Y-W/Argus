# EXP-029 — Registered design: danger-routed immune controller

**Registered:** 2026-08-04 before return parsing  
**Stage:** historical cross-resolution mechanism test  
**Attribution:** Collaborative

## Data boundary

Use the official French 10-industry daily value-weighted returns. The frozen December 2024 archive supplies calibration and primary evaluation. Calibration is 1995–2004 and may determine signal quantiles only; no portfolio-performance outcome may tune a rule. Primary evaluation is 2005–2024. The current file supplies a descriptive 2025+ check and cannot rescue failure.

## Frozen immune routing

Every monthly decision uses the previous 252 trading days. Per-industry damage is EXP-028's frozen absolute standardized 63-versus-189-day mean shift plus absolute log-volatility shift. Overall danger is the root mean square of ten damage scores. Localization is the fraction of total positive damage carried by the two largest scores.

Using calibration signal values only:

- danger below its 75th percentile: `tolerate` and preserve memory unchanged;
- danger at or above its 75th percentile and localization at or above its 70th percentile: `localized` repair;
- danger at or above its 75th percentile and lower localization: `systemic` regeneration.

Quantiles are frozen before primary performance is computed. No hysteresis, cooldown, or threshold tuning is allowed.

## Responses and baselines

The genome is ten long-only weights summing to one. Lagged fitness, 10 bp turnover cost, risk aversion 1.5, 64-candidate budget, Normal(0,0.35) all-gene mutation, Dirichlet global restart, and exact two-gene transfer are inherited unchanged from EXP-028.

Compare `controller` with fixed `localized`, `all_gene`, and `random` responses. When the controller invokes a response, it evaluates the incumbent plus 63 new candidates from its own deterministic stream; tolerance evaluates no new candidate. Fixed strategies receive 64 candidates every month. Also report deterministic minimum variance and equal weight.

## Outcomes and inference

Primary endpoint is monthly realized certainty equivalent. Secondary outcomes are cumulative net log return, annualized volatility, 5% expected shortfall, drawdown, turnover, candidate count, route shares, and paired monthly win fraction. Use 10,000 paired circular moving-block bootstrap resamples with 12-month blocks.

## Joint decision rule

Classify `SUPPORTED WITH LIMITS` only if, during 2005–2024:

1. controller minus fixed-localized mean monthly CE has a 95% interval above zero;
2. controller minus fixed-random mean monthly CE has a 95% interval above zero;
3. controller minus fixed-all-gene mean monthly CE has a 95% interval above zero;
4. controller expected shortfall is no more than 10% worse than the best fixed search response;
5. controller turnover is below every fixed search response; and
6. tolerance, localized, and systemic routes each occur in at least 5% of evaluation months.

Any failure rejects the joint controller. Minimum variance or equal weight dominance does not alter the formal rule but forces practical-potential language to remain weak.

## Limitations

The 10-industry panel overlaps EXP-028's US market and is not independent geography. Calibration fixes signal frequency, not biological truth. The controller does not model antibodies, cell lineages, clonal populations, infection, cancer, or systemic financial stability. It is a falsifiable danger-routing abstraction.

## Connections

`hypotheses/HYP-029-danger-routed-immune-controller.md` · EXP-028 · `datasets/french_10_industry_daily.md`

