# Clinical-evidence mispricing sandbox

**Evidence status:** exploratory infrastructure only; no market or clinical claim.

This vertical slice fixes two semantics before any outcome or return analysis:

1. an event can use only the latest trial-record version publicly posted by its exact announcement timestamp; and
2. after-hours information belongs to the next supplied trading session.

`point_in_time.py` also provides a deliberately simple market-adjusted CAR calculation for synthetic tests. It is not yet the registered estimator. A confirmatory event study must separately freeze the expected-return model, estimation window, exchange calendar, treatment of halts and missing returns, overlapping events, uncertainty estimator, and dependence correction.

`public_signals.py` adds a public collaborator/capacity ledger. It deliberately separates an economic action date from the date the signal was publicly observable. It also labels availability as `exact`, `date_upper_bound`, or `retrieval_only`. A current USAspending or ClinicalTrials.gov record is never backdated to its underlying action date; historical use requires an archived release or another timestamped public source. General company procurement is also kept separate from asset-specific evidence.

The 2026-08-21 live ClinicalTrials.gov probe of NCT04470427 was a schema check only. It confirmed that the current v2 response exposes sponsor, phase, randomized design, masking, endpoints, enrollment, and posting dates. It also returned actual enrollment and results added years after the 2020 readout, demonstrating why a current API response cannot reconstruct the pre-announcement evidence set.

Run:

```powershell
pytest engineering/sandbox/clinical_evidence_mispricing
```

The read-only USAspending schema probe can be run without saving data:

```powershell
python -m engineering.sandbox.clinical_evidence_mispricing.probe_usaspending "MODERNATX, INC." 2019-01-01 2021-12-31
```

The Hwang (2013) sample probe fetches current ClinicalTrials.gov collaborator fields for 24 published events:

```powershell
python -m engineering.sandbox.clinical_evidence_mispricing.probe_hwang_collaborators
```

Its output is explicitly not historical evidence. The 2026-08-21 snapshot found current collaborators in 4/16 positive and 3/8 negative events (odds ratio 0.556; Fisher exact p-value 0.647), rejecting the broad collaborator-presence proxy as a promising exploratory pattern while leaving costly point-in-time commitments untested.

The frozen positive-spike reversal smoke test can be reproduced with:

```powershell
python -m engineering.sandbox.clinical_evidence_mispricing.probe_positive_spike_reversal
```

It uses mutable Yahoo adjusted closes and is not claim eligible. In the 16 positive Hwang events, 10 had a positive SPY-adjusted reaction through close +1. Shorting those events from close +1 to close +20 produced a -1.15% mean gross abnormal return, -1.65% after the frozen 50 bp cost, and a 40% positive fraction. The frozen sandbox rule therefore failed. This rejects only that exact large-company, short-horizon implementation; it does not test small-biotech spikes, scientific-quality conditioning, borrow feasibility, or an independently assembled event universe.

Two related event-path premise checks are available with:

```powershell
python -m engineering.sandbox.clinical_evidence_mispricing.probe_hwang_event_paths
```

They found almost no positive-versus-negative separation in SPY-adjusted run-ups (+9.27% versus +8.52%) and a noisy +2.37% XBI-adjusted mean path after eight large-firm failures from +2 to +100 (median -0.62%; 50% positive). The latter is explicitly a wrong-universe placebo for the small-biotech reversal claim.

The small-biotech reconstruction now has an eight-row, SEC-supported, return-blind seed and schema validator. All rows remain single-coded candidates. The free-price coverage probe is:

```powershell
python -m engineering.sandbox.clinical_evidence_mispricing.probe_failure_price_coverage
```

Only 2/8 seed securities had identity-matched 252-session pre-event and 100-session post-event coverage. No event returns were calculated. Dropping the six missing histories would induce severe corporate-survivorship bias, so a delisting-complete permanent-identifier source is a blocking requirement.

The CRSP CIZ access gate is now implemented and tested. It discovers the live WRDS schema, issues a return-blind historical ticker/name/date query, validates event-time links to one PERMNO, and accepts a history ending before +100 only when CRSP explicitly supplies a usable delisting-inclusive terminal return. Check local readiness without connecting:

```powershell
python -m engineering.sandbox.clinical_evidence_mispricing.probe_wrds_crsp_access
```

After configuring the researcher's WRDS username and normal WRDS authentication locally, run the schema and identifier-only audit:

```powershell
python -m engineering.sandbox.clinical_evidence_mispricing.probe_wrds_crsp_access --connect --link-ledger engineering/sandbox/clinical_evidence_mispricing/small_biotech_phase3_failures_seed.csv
```

The 2026-08-21 readiness probe found the `wrds` package installed but no `WRDS_USERNAME`. No connection or return query was attempted. WRDS currently requires Duo Mobile push for remote PostgreSQL access; credentials must not be committed or pasted into research artifacts.

The branch is now under an active, reversible institutional-access pause because the researcher's Undergraduate/Master's WRDS request was not approved. Do not run a survivor-only return test while waiting. Resume from `research_governance/2026-08-21-biotech-wrds-access-pause.md` after the school representative identifies the available account type and subscribed datasets.

## Connections

`source_scouting/2026-08-21-clinical-evidence-mispricing.md` · `source_scouting/2026-08-21-biotech-collaborator-capacity-signals.md` · `ideas/2026-08-21-clinical-evidence-mispricing.md` · `ideas/2026-08-21-biotech-collaborator-capacity-signals.md` · `papers/2022-singh-et-al-clinical-trial-stock-reactions.md`
