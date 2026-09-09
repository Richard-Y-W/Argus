# Clinical-evidence mispricing: lineage and data gate

**Stage:** scouting and data-feasibility audit; no hypothesis registered  
**Attribution:** Collaborative  
**Decision:** proceed to a point-in-time event-ledger pilot; stop before return testing

## Research question

Why do some biomedical companies reprice discontinuously when scientific evidence accumulated gradually? The discriminating question is whether the jump reflects genuinely new blinded information, public evidence that investors did not aggregate, difficult evidence that was incorporated slowly after release, or nonlinear exposure of a concentrated company to one asset.

## Competing mechanisms and observable predictions

| Mechanism | Prediction that would distinguish it |
|---|---|
| Rational uncertainty resolution | Pre-readout public features add little out-of-sample outcome information; the immediate jump is explained by the newly disclosed result and company exposure; no conditional drift follows. |
| Pre-readout scientific underreaction | A frozen point-in-time evidence model predicts readout outcomes beyond historical phase/disease base rates while pre-event returns or expectation proxies do not fully reflect that ranking. |
| Post-readout interpretation underreaction | Conditional on outcome, immediate return, firm exposure, and liquidity, more complex or lower-clarity announcements exhibit same-direction CAR over sessions +2 to +20. |
| Valuation convexity | Immediate absolute returns scale with lead-asset dependence and probability-weighted asset value, without predictable outcome residuals or delayed drift. |
| Leakage or informed trading | Return or volume changes concentrate before the public timestamp; this is not evidence that public scientific analysis generated the signal. |

## Primary lineage inspected

- Singh et al. (2022), DOI 10.1371/journal.pone.0272851, analyze 13,807 outcomes and show that early-biotech sponsor status is a major return discriminator. Their restricted Citeline/CRSP inputs prevent direct public replication.
- Hwang (2013), DOI 10.1371/journal.pone.0071966, manually links trial-result announcements to daily returns for large biopharmaceutical firms. The narrow large-firm sample does not answer concentrated small-biotech exposure.
- ClinicalTrials.gov documents current JSON downloads, daily refreshes, and human-readable record histories. A live schema probe on 2026-08-21 confirmed trial design, sponsor, phase, enrollment, endpoint, and posting-date fields for NCT04470427.
- The same live probe also demonstrated the central leakage problem: the current record contains actual enrollment and results posted in 2024, long after Moderna’s 2020 efficacy announcement. Current records cannot stand in for historical information sets.
- AACT offers current and historical static ClinicalTrials.gov snapshots, but each current full export is roughly 2.3 GB. Availability of a targeted, version-complete extraction path remains to be established.
- SEC EDGAR exposes filing histories, former names, exchanges, tickers, accession numbers, and dissemination-time records. It can anchor 8-K/6-K timestamps but will not cover every press release or conference disclosure.

## Required event ledger

One row represents the first public disclosure of a prespecified clinical readout, not every article repeating it. Minimum fields are event ID, NCT ID, asset/drug, indication, sponsor, CIK, point-in-time security ID, announcement timestamp and source, disclosure channel, scheduled status, trial-record version timestamp, outcome label, confounding-news flags, and an immutable provenance hash.

The first universe should be US-listed sponsor Phase III topline efficacy readouts across therapeutic areas. Vaccines are a preregistered subgroup candidate, not the sampling frame; COVID-specific events receive an explicit regime flag.

## Blocking data gates

1. Reconstruct the latest publicly posted trial version strictly before each announcement.
2. Establish exact or bounded announcement times and align after-hours disclosures to the next tradable session.
3. Build a sponsor–licensee–security history that retains delisted and acquired firms.
4. Obtain survivorship-safe daily returns; intraday quotes are preferable for timestamp validation.
5. Define and independently code outcome, endpoint quality, safety, and concurrent-news exclusions without looking at post-event returns.
6. Freeze development and untouched confirmation periods before estimating return relationships.

## Promotion decision

The question passes the question-to-exploration gate but not exploration-to-registration. The next action is a 100–200 event gold-ledger audit with dual coding and no return inspection. Registration is premature because point-in-time record recovery, exact timestamps, sponsor-security linkage, and survivorship-safe prices are not yet demonstrated.

## Connections

`papers/2022-singh-et-al-clinical-trial-stock-reactions.md` · `ideas/2026-08-21-clinical-evidence-mispricing.md` · `engineering/sandbox/clinical_evidence_mispricing/README.md` · `knowledge_graph/clinical-evidence-pricing-thread.md`
