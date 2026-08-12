# External benchmark audit for safety-constrained financial defense

**Date:** 2026-08-11  
**Stage:** scouting and data feasibility; no hypothesis registered  
**Attribution:** Human-directed

## Question

Can the narrow mechanism surviving EXP-031—early boundary surveillance plus minimal collateral intervention—be tested outside the consumed EXP-030/031 simulator?

The proposed estimand is not whether low-risk banks subsequently perform better. It is the safety cost of a response rule: how much balance-sheet function must be removed to keep a preregistered health measure within a noninferiority margin. A valid design needs pre-action state, action composition, post-action health, and a credible comparator or externally imposed scenario.

## Candidate data families

| Candidate | Observable structure | Main value | Blocking limitation | Decision |
|---|---|---|---|---|
| FFIEC Call Reports | Quarterly institution-level balance-sheet, income, and past-due schedules; bulk annual files cover all reporters | Long panel, public regulatory definitions, possible leverage/liquidity contribution accounting | Quarterly frequency is coarse; management actions and treatment assignment are endogenous; merger/failure survivorship and reporting-form changes require explicit handling | **Best US state panel; not yet an intervention benchmark** |
| Federal Reserve supervisory stress tests | Historical bank results, scenarios, and data dictionaries; the 2025 page exposes a 2013–2025 results CSV | Common hypothetical shocks and bank-level capital outcomes | Published results do not reveal counterfactual targeted and proportional actions; methodology changes create revision/comparability risks | **Useful external stress calibration, not treatment identification** |
| EBA stress tests and transparency exercises | Granular bank-level starting points and baseline/adverse outcomes with dictionaries and metadata | Cross-bank exposure structure and common scenarios; richer public decomposition than the synthetic benchmark | Static-balance-sheet assumptions suppress the adaptive treatment being studied; sample composition and regulation change across exercises | **Best structural benchmark candidate; cannot establish policy superiority alone** |

## Primary-source lineage

- FFIEC, [Call Report bulk data](https://cdr.ffiec.gov/public/pws/downloadbulkdata.aspx) and [public-data FAQ](https://cdr.ffiec.gov/public/HelpFiles/FAQ.htm). The bulk interface reports its update date and the FAQ describes annual four-period files containing all reporters for selected schedules.
- Federal Reserve, [Dodd-Frank Act Stress Tests 2025](https://www.federalreserve.gov/supervisionreg/dfa-stress-tests-2025.htm). The page provides scenarios, methodology inputs, a data dictionary, and historical 2013–2025 results in CSV form.
- European Banking Authority, [2025 EU-wide stress test](https://www.eba.europa.eu/eu-wide-stress-test-2025) and [2025 data-exploitation guide](https://www.eba.europa.eu/assets/st25/full_database/763451/CSV_guide.pdf). The release provides granular bank results, metadata, dictionaries, and three detailed CSV families.
- European Banking Authority, [EU-wide transparency exercise](https://www.eba.europa.eu/risk-and-data-analysis/risk-analysis/eu-wide-transparency-exercise). The final 2025 exercise covers 119 banks and four reference dates; the series is being replaced by the Pillar 3 Data Hub.

These are authoritative dataset descriptions, not evidence that the proposed defense works.

## Identification debate

**Optimist:** EBA exposure decompositions can replace hand-designed pathology labels. A common adverse scenario supplies an externally specified stress, and a frozen optimization can ask how much exposure must be removed to satisfy a capital or leverage noninferiority bound.

**Skeptic:** Applying alternative actions to disclosed balance sheets still requires a response model. If that model maps exposure cuts to health outcomes, the result remains a simulation whose conclusions may be built into its equations.

**Statistician:** Banks are dependent through common scenarios, countries, regulation, and exposures. Bank count is not the effective sample size. Repeated stress-test vintages are not untouched replications when methodology and participating institutions change.

**Economist:** Observed deleveraging is endogenous to latent supervisory information, funding access, and management quality. A panel regression of action on later health would not identify the effect of targeting.

**Portfolio manager:** “Healthy exposure preserved” needs an economically defensible counterpart in bank data—such as lending capacity, liquid assets, or risk-weighted exposure—not a simulator-only culprit label.

**ML researcher:** No search over health metrics, safety margins, contribution scores, and datasets is admissible without a complete search ledger and a later untouched exercise.

## Promotion gate

Do not register EXP-032 yet. Registration becomes admissible only after a design note fixes:

1. one public data release and immutable file fingerprints;
2. a health endpoint grounded in reported regulatory fields;
3. a collateral-function endpoint that does not use future outcomes or hidden pathology labels;
4. a response model whose assumptions can be falsified or sensitivity-bounded;
5. a safety-noninferiority margin justified before outcome inspection;
6. treatment comparators with equal information and optimization budgets;
7. institution lineage, missingness, revisions, dependence, and methodology-change handling; and
8. an untouched external exercise or jurisdiction reserved for confirmation.

## Decision

**CONTINUE ONLY AS DESIGN AND DATA-LINEAGE WORK.** Do not run another controller on EXP-030/031 paths and do not describe the remaining question as an immune-system edge. The smallest useful next cycle is an EBA-2025 schema audit that determines whether capital/leverage and exposure fields support a transparent static counterfactual. If they do not, archive the branch rather than substituting a looser return backtest.

## Connections

`experiments/EXP-031-surveillance-treatment-factorial/results.md` · `literature_reviews/2026-08-05-financial-health-invariants.md` · `ideas/hypothesis_queue.md`
