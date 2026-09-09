# Clinical-evidence pricing foundation

Richard proposed a medical-research quantitative-finance program after observing abrupt vaccine-related stock jumps and asked why gradually accumulating science appears to enter prices discontinuously. The idea survived question triage only after separating a rational Bayesian jump at a blinded readout from two possible inefficiencies: failure to aggregate public pre-readout evidence and slow interpretation of complex disclosed evidence.

Primary lineage shows that the descriptive event effect is not novel. Singh et al. (2022) analyze 13,807 clinical outcomes and find especially large reactions among early biotechnology sponsors, but use restricted Citeline and CRSP data and do not establish the proposed point-in-time scientific disagreement mechanism. Argus therefore ranked complexity-conditioned post-readout drift as the leading eventual return test, with pre-readout scientific probability as the more difficult information test and lead-asset exposure as a required baseline.

A live ClinicalTrials.gov v2 probe of Moderna trial NCT04470427 confirmed useful sponsor, phase, design, endpoint, enrollment, and posting fields. It also returned actual enrollment and results added years after the 2020 announcement. That is direct schema evidence that current records would leak future information into a historical feature set. The new sandbox selects only record versions public by the announcement timestamp, maps after-hours disclosures to the next supplied trading session, and tests a simple market-adjusted CAR calculation on synthetic returns. These tests establish software semantics, not an empirical result.

Repository cleanup preceded the new branch: full-suite pytest import collisions were repaired, CI now runs the whole suite, EXP-020/021 received their missing success records, experiment counts were corrected, and the PyArrow constraint was reconciled with the lockfile.

**Decision:** remain exploratory. Build a return-blind 100–200 event Phase III gold ledger before assigning a hypothesis ID or inspecting event returns. Attribution is collaborative: Richard originated and sharpened the research question; Argus performed lineage, formalization, and engineering.

## Connections

`source_scouting/2026-08-21-clinical-evidence-mispricing.md` · `ideas/2026-08-21-clinical-evidence-mispricing.md` · `papers/2022-singh-et-al-clinical-trial-stock-reactions.md` · `engineering/sandbox/clinical_evidence_mispricing/README.md` · `researcher_scorecard.md`
