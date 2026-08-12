# EBA 2025 schema audit for safety-constrained intervention

**Stage:** data-lineage and identification audit; no hypothesis registered  
**Attribution:** Human-directed  
**Decision:** **STOP BEFORE EXP-032**

## Question

Does the EBA 2025 stress-test release expose enough external structure to test whether targeted balance-sheet intervention preserves more function while remaining noninferior on safety?

## Evidence inspected

The audit downloaded and fingerprinted all three official data tables plus the dictionary and bank metadata. It inspected 64 banks, 1,194,554 data rows, 168 dictionary entries, four time endpoints, baseline/adverse scenarios, and the exposure, portfolio, geography, performance, capital, loss, and provision dimensions. Exact provenance is recorded in `datasets/eba_2025_stress_test.md`.

The data are materially better than the EXP-030/031 simulator for describing actual bank starting states and regulator-specified stress projections. They include granular credit exposure and projected impairment structure, CET1 and leverage ratios, capital requirements, risk exposure amounts, profit and loss, and a small capital-measures template.

## Gate findings

| Required element | Finding | Gate |
|---|---|---|
| Immutable release | Stable official URLs, sizes, and hashes recorded | Pass |
| Regulatory health endpoint | CET1, total capital, leverage, and requirements are available | Pass for solvency only |
| Collateral-function endpoint | Lending/exposure preservation can be proxied, but “healthy” exposure is not observed | Material unresolved |
| Liquidity endpoint | No LCR, funding, deposit, or operational liquidity series | **Fail for the inherited leverage-plus-liquidity mechanism** |
| Intervention response | Projected outcomes assume a constrained/static balance sheet; no mapping from selective exposure cuts to capital/loss outcomes is observed | **Blocking** |
| Treatment comparator | Targeted and proportional counterfactuals would both be researcher-generated | **Blocking** |
| Dependence and lineage | Bank, country, scenario, and item identifiers exist; cross-bank dependence remains estimable only with few country/scenario clusters | Material unresolved |
| Untouched confirmation | Earlier EBA releases exist, but methodology and sample change; no release was reserved after a fixed response model because none exists | **Fail for registration** |

## Why a static counterfactual would not be evidence

One could rank credit cells by projected loss or risk weight, delete exposure, and mechanically scale losses and risk exposure amounts. That would guarantee that a targeted optimizer looks efficient under the same coefficients used to select cells. The result would be an algebraic property of the imposed linear response, not an empirical test of how a bank, borrowers, funding markets, or supervisors respond.

Observed capital measures do not solve this problem. They are a seven-item bank-level disclosure at one reporting period, not randomized or plausibly exogenous choices, and they do not encode exposure-specific deleveraging. Regressing later capital outcomes on observed actions would be confounded by supervisory information, management quality, funding access, and initial vulnerability.

## Adversarial decision

**INCONCLUSIVE on the external mechanism; NOT REGISTRABLE.** EBA 2025 can validate that the synthetic state space omitted important heterogeneity, but cannot test intervention superiority without importing the central response function. The smallest credible continuation would require either:

1. a natural or institutional experiment that changes permissible intervention composition while leaving stress exposure plausibly comparable; or
2. an independently validated structural balance-sheet model, frozen before applying it to a held-out EBA release.

Neither is currently in the repository. The financial-defense branch is paused. The biological vocabulary should not be revived to bypass this identification failure.

## Researcher digest

Rich data do not automatically create identification. Here the missing object is not another bank variable; it is the counterfactual response to an action. If we supply that response ourselves and then “discover” that the optimizer works, we have tested our equations against themselves.

## Connections

`datasets/eba_2025_stress_test.md` · `source_scouting/2026-08-11-financial-defense-external-benchmark-audit.md` · EXP-031
