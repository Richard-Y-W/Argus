# Singh et al. (2022) — Sponsor stock reactions to clinical-trial outcomes

**Primary source:** Manish Singh, Roland Rocafort, Cathy Cai, Kien Wei Siah, and Andrew W. Lo, “The reaction of sponsor stock prices to clinical trial outcomes: An event study analysis,” *PLOS ONE* 17(9), e0272851. DOI: https://doi.org/10.1371/journal.pone.0272851

## Question and framework

The paper asks how sponsor stock prices react to clinical-trial outcomes and whether trial and sponsor characteristics explain cross-event abnormal returns. It links 13,807 trial outcomes from 2000–2020 to 379 publicly traded US sponsors, estimates short-window abnormal returns relative to a linear factor model, and uses bootstrap uncertainty for a return-attribution model.

## Main evidence

Sponsor type is the largest reported discriminator: early biotechnology firms react more than large pharmaceutical firms. Phase, disease, target accrual, design, and outcome also matter, but the observed variables leave substantial cross-event return variation unexplained. The paper therefore establishes that clinical outcomes are important valuation events; it does not establish that public pre-readout science predicts the outcome or that post-event prices underreact.

## Assumptions and limitations

- Citeline trial data and CRSP returns are subscription datasets, so the published sample cannot be reconstructed from public inputs alone.
- Sponsor-to-security linkage, delisting coverage, corporate actions, and exact announcement-time alignment are central but not independently verified here.
- Short-window abnormal returns measure repricing, not irrationality, causality, or executable profit.
- Trial and sponsor variables are largely coarse. Scientific effect size, uncertainty, endpoint quality, safety severity, prior-evidence consistency, and asset-level company exposure are not the paper’s central point-in-time predictors.
- Event-date construction needs a dedicated replication audit before Argus borrows it; event selection based on observed return magnitude would invalidate inference.
- The 2000–2020 sample overlaps any retrospective Argus development sample and cannot serve as untouched confirmation for a closely adapted specification.

## Argus implication

Replicating “clinical news moves biotech stocks” has low novelty. The open question is whether strictly pre-event scientific evidence predicts readout outcomes beyond frozen base rates, or whether announcement complexity predicts delayed abnormal returns conditional on the disclosed outcome and immediate price response.

## Connections

`source_scouting/2026-08-21-clinical-evidence-mispricing.md` · `ideas/2026-08-21-clinical-evidence-mispricing.md` · `engineering/sandbox/clinical_evidence_mispricing/README.md`
