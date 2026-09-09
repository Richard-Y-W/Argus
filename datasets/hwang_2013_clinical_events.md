# Hwang 2013 public clinical-event sample

**Source:** Hwang, “Stock Market Returns and Clinical Trial Results of Investigational Compounds,” PLOS ONE 8(8), Table 2. DOI: 10.1371/journal.pone.0071966.  
**Accessed:** 2026-08-21  
**License:** PLOS Creative Commons Attribution License  
**Local extract:** `engineering/sandbox/clinical_evidence_mispricing/hwang_2013_events.csv`

## Contents

Twenty-four result announcements for 23 ClinicalTrials.gov records from 2011–2013. The extract preserves only event ID, date, sponsor ticker used by the paper, expected outcome sign, phase, and NCT ID. Counts reproduce the paper: 16 positive, 8 negative, 13 Phase III, and 23 unique NCT IDs.

## Provenance and use

Rows were transcribed from the paper's published Table 2 and checked by deterministic tests. This sample was not discovered through return screening. On 2026-08-21 it seeded a current-record ClinicalTrials.gov collaborator prevalence probe.

## Limitations

- The sample covers seven large biopharmaceutical firms, not concentrated small biotechs.
- It was constructed by the original author from Factiva and company disclosures and is not a complete population.
- The outcome distribution is not balanced and all negative events are Phase III.
- Repeated events and sponsors create dependence.
- Current ClinicalTrials.gov collaborator fields are not historical versions and can reflect later acquisitions or edits.
- No licensed Bloomberg returns from the paper are included.

The sample may support data-pipeline feasibility and a bounded replication. It cannot validate a collaborator alpha signal without historical public commitment timestamps and separately sourced returns.

## Re-fetch

Retrieve Table 2 from `https://doi.org/10.1371/journal.pone.0071966.t002` or the PLOS article and compare the local count tests.

