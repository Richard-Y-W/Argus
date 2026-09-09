# SPF composition and horizon schema audit

**Stage:** exploration and data-feasibility audit  
**Attribution:** AI-led  
**Decision:** preserve the point-forecast branch; reject promotion of the three-horizon density design as written

## Question and competing mechanisms

Can an inflation-disagreement curve be estimated at several comparable horizons without confusing changing beliefs with changing respondents or changing probability bins?

The intended mechanism is heterogeneous information or models across forecast horizons. The main alternatives are mechanical horizon-specific missingness, panel entry and exit, confidential-ID reassignment, and density-bin changes. A balanced panel is not automatically causal correction: persistent respondents can be a selected subpopulation.

## Evidence inspected

The official 2026:Q3 `SPFmicrodata.xlsx` workbook was acquired return-free and fingerprinted. The audit used only `COREPCE` and `PRCPCE`; no yield or asset-return series was joined.

The Philadelphia Fed documents that `COREPCE2` is the current-quarter forecast and `COREPCE3` through `COREPCE6` are the next four quarters. It also documents that PRCPCE uses ten fixed bins for current-year core-PCE inflation and the same ten bins for the next year. Those bins have remained fixed since PRCPCE began in 2007:Q1. The Bank separately warns that confidential IDs do not always identify the same person or institution over time.

## Deterministic audit result

- 79 quarterly surveys span 2007:Q1 through 2026:Q3.
- The point panel contains 98 distinct codes and 2,702-2,768 responses per horizon.
- 97.51% of rows with any quarterly point forecast contain all five horizons; the median within-survey all-horizon respondent share is 97.30%.
- Median adjacent-survey retention is 87.34%; median participation is 24 surveys per ID and the maximum is 79.
- 2,425 rows contain both complete ten-bin density distributions, and no complete distribution fails the 100% sum check at 0.11 percentage-point tolerance.
- The point data pass a three-horizon availability gate. The density data do not: they contain two annual horizons, not three.

## Decision rule and result

The pre-existing promotion rule required at least three comparable inflation horizons, documented respondent continuity, and a deterministic bin-change rule. A five-horizon **point-forecast** curve is feasible from 2007:Q1. A three-horizon **density** curve is not. Respondent codes are useful clustering labels but cannot be interpreted as error-free person identities.

No `HYP` or `EXP` is registered. Promoting a density/Wasserstein term-structure experiment would silently change a failed data gate. A future point-disagreement design must preregister the estimand separately and report unbalanced-survey, common-within-survey, and consecutive-participant versions as different populations rather than selecting the most favorable one.

## Strongest adversarial interpretation

High same-survey completeness does not solve endogenous panel turnover. The audit establishes technical feasibility for descriptive point disagreement, not that composition adjustment identifies belief changes, not that disagreement represents uncertainty or de-anchoring, and not that it predicts yields or returns.

## Minimum next test

Before registration, freeze three point horizons, a primary population estimand, the role of IDs, and a block-bootstrap unit. Generate a return-free panel-flow table and compare dispersion under all-row and same-survey common-responder definitions. Do not use subsequent forecast accuracy to weight respondents.

## Connections

`source_scouting/2026-08-02-inflation-disagreement-term-structure.md` · `datasets/philadelphia_fed_macro_data_gates.md` · `engineering/sandbox/macro_data_gates/audit.py` · `knowledge_graph/macro-real-time-thread.md`
