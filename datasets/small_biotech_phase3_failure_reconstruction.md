# Small-biotech Phase III failure reconstruction

## Status

Paused on 2026-08-21 pending the institutional WRDS representative's response. The eight-row local CSV is a single-coded feasibility seed, not the study sample and not evidence. A tested CRSP CIZ security-link and coverage gate is ready, but the researcher's Undergraduate/Master's account request was not approved. Resume under `research_governance/2026-08-21-biotech-wrds-access-pause.md`.

## Target lineage

Afik, Lahav, and Zaguri (2025), DOI `10.1016/j.frl.2025.108139`, report 92 BioSpace-derived Phase III success/failure events for US-listed firms from 2011–2019. Accessible article text says they retain only the earliest event when a company has multiple drugs, split firms by event-time equity market value, and report different long-run failure paths for small and large firms. The article does not expose its event table, return inputs, exact size cutoff, or all implementation choices through the accessible record.

This Argus dataset is therefore an **independent reconstruction**, not yet a literal replication. Exact replication requires the authors' event list and complete methodology or a demonstrated rule-equivalent reconstruction.

## Current seed

`engineering/sandbox/clinical_evidence_mispricing/small_biotech_phase3_failures_seed.csv` contains eight SEC-supported failure candidates from 2017–2019. Each row records the historical ticker and CIK, asset, trial, failure definition, source timing, and announcement-time precision. All rows are `single_coded_candidate`; none may enter a return analysis.

A supplementary timestamp audit resolved the four `date_only` rows as pre-market. VTL's company wire was timestamped 05:00 ET; PRTA's event-time SEC filing was accepted 08:01 ET; ImmunoGen's event-time SEC filing was accepted 07:02 ET before its 08:00 call; and Sage's event-time SEC filing was accepted 07:01 ET. Tetraphase's already coded after-market announcement is independently confirmed by its 16:01 ET company wire. These are single-coded timing determinations, not dual-coded eligibility.

## Eligibility gates

An event becomes eligible only after independent second coding confirms:

- a pivotal or explicitly Phase III interventional trial;
- public disclosure that the primary endpoint failed or that a Phase III program stopped for efficacy, safety, or futility;
- the earliest public timestamp and whether the market was open;
- the event-time listed security and sponsor ownership;
- no earlier retained drug event for the same company under the reconstruction rule;
- event-time equity market value and the predeclared size split;
- delisting-complete daily returns through day +100; and
- simultaneous financing, acquisition, regulatory, or earnings news.

## Unresolved acquisition blockers

- BioSpace permits article access but its robots policy disallows automated archive/search crawling; the current public sitemap has only recent entries.
- Singh et al. (2022)'s 13,807-event inputs require Citeline and CRSP subscriptions and are not publicly redistributable.
- Yahoo history is insufficient for delisted firms, permanent identifier linkage, and claim-bearing returns.
- The local repository has no CRSP-equivalent extract, historical market capitalization, or borrow data.
- The academic WRDS/CRSP route is technically supported by `probe_wrds_crsp_access.py`; the installed client currently lacks a configured `WRDS_USERNAME` and successful Duo-authenticated session.
- The institutional representative's account and CRSP-subscription decision is pending; do not substitute a survivor-only free panel while waiting.

## Frozen CRSP boundary

The next permitted query is identifier-only: historical ticker, issuer name, effective dates, PERMNO, and PERMCO from `crsp.stkSecurityInfoHist`. Event-time ticker, sponsor-name root, and effective dates must identify exactly one PERMNO. Return extraction may begin only after all eight identifier links are reviewed.

The planned daily source is CRSP CIZ `crsp.dsf_v2` (or its documented equivalent). The coverage gate requires 252 pre-event sessions and 100 post-event sessions. An earlier endpoint is accepted only when the terminal CIZ row explicitly identifies a delisting and supplies a usable total return. WRDS documents that CIZ `DlyRet` already incorporates the delisting return, so it must not be combined with a second legacy delisting adjustment.

## Planned raw-data boundary

Raw licensed data, if obtained, remain outside version control. Dataset documentation will record vendor release, extraction date, query, hashes, identifiers, exclusions, and coverage. Derived event labels can be stored only when licensing permits.

## Connections

`ideas/2026-08-21-biotech-eight-candidate-test-gates.md` · `source_scouting/2026-08-21-biotech-alpha-candidates.md` · `engineering/sandbox/clinical_evidence_mispricing/positive_spike_reversal_design.md`
