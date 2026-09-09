# Biotech failure-reversal WRDS access pause and resume protocol

**Effective:** 2026-08-21  
**Decision owner:** researcher  
**Research stage:** exploratory reconstruction  
**Attribution:** Human-directed  
**Status:** active, reversible data-access pause

## Decision

Pause new empirical work on the small-biotech Phase III failure-reversal and positive-spike short branches until the researcher's institutional WRDS representative responds. Preserve the event seed, timing audit, source audit, code, tests, and negative smoke tests unchanged.

This is not an evidentiary rejection. It is a deliberate stop before outcome inspection because the available free histories select on corporate survival. Work resumes only after the response is reviewed and the available datasets are identified.

## Research question being preserved

The main replication question is whether small, concentrated biotechnology firms exhibit economically meaningful abnormal reversal after a Phase III failure. A related but separate question is whether small-biotech stocks that rise sharply after positive clinical news subsequently underperform enough to support a short after realistic costs and borrow constraints.

Competing explanations remain open:

1. a failure initially causes forced selling or valuation overshoot followed by reversal;
2. apparent reversal comes from survivorship, acquisition payments, delisting treatment, or a few influential firms;
3. prices rationally reflect a permanent loss in asset value, leaving no reversal;
4. any gross path is unavailable after spreads, borrow fees, halts, recalls, and short-sale constraints; and
5. the published finding depends on an unrecoverable sample or implementation choice rather than a portable mechanism.

## Evidence accumulated before the pause

### What was actually tested

- A frozen large-company positive-readout rule shorted from close +1 through close +20 after a positive initial reaction. Ten of sixteen Hwang events were eligible. The mean short abnormal return was **-1.148% gross**, **-1.648% after a frozen 50 bp cost**, and the positive fraction was **40%**. This exact implementation is rejected; it may not be retuned on the consumed events.
- A wrong-universe placebo examined eight large-firm clinical failures through +100. Its mean XBI-adjusted path was +2.37%, median -0.62%, and positive fraction 50%, with the mean dominated by one BIIB observation. It does not test the small-biotech claim.
- An eight-row, SEC-supported Phase III failure seed was constructed without inspecting its event returns. A free Yahoo coverage probe found complete identity-matched windows for only PRTA and historical AXON: **2/8 coverage**.
- The six missing histories belong disproportionately to acquired, merged, renamed, or disappeared firms. Testing only the two available names would condition on survival and is prohibited.
- A supplementary primary-source timing audit classified all eight announcements by market session. The classifications remain single-coded and require an independent second pass.

### What has not been tested

- No return for any of the eight small-biotech candidates has been calculated or inspected.
- No small/large classification has been assigned because event-time equity market value is unavailable locally.
- No development/holdout test of the failure reversal exists.
- No small-biotech positive-spike short has been tested.
- Borrow availability, fees, recalls, halts, spreads, capacity, financing overlap, cash runway, pipeline concentration, and concurrent news remain unidentified.
- The work is an independent reconstruction, not a replication of Afik, Lahav, and Zaguri (2025), because their 92-event table and several exact implementation choices are unavailable.

## Why CRSP/WRDS was selected

The required price source must support lifecycle-stable security linkage, historical name and ticker intervals, daily total returns, corporate actions, event-time market capitalization, and explicit delisting treatment. CRSP's PERMNO is designed to track a security through ticker and name changes. WRDS's current CIZ event-study documentation states that `DlyRet` already incorporates delisting return.

Argus implemented and tested:

- live schema discovery for `crsp.stkSecurityInfoHist` and `crsp.dsf_v2`;
- a return-blind historical PERMNO/PERMCO query;
- event-time ticker, issuer-name, and effective-date validation;
- protection against ticker reuse, including historical AXON;
- a 252-session pre-event and +100-session coverage audit; and
- acceptance of an early terminal row only when CIZ explicitly marks a delisting and supplies a usable total return.

The local `wrds` package is installed. The researcher was not approved for an Undergraduate/Master's WRDS account, so no username was configured, no WRDS session was opened, no PERMNO was retrieved, and no CRSP return was inspected.

## Institutional request now pending

The researcher will ask the school representative:

1. why the Undergraduate/Master's request was denied;
2. whether the school subscribes to CRSP US Stock data;
3. whether programmatic WRDS access is included;
4. whether the researcher qualifies for the combined Undergraduate/Master's account type;
5. whether a faculty-sponsored Research Assistant account is possible; and
6. which survivorship-safe equity datasets the library offers if CRSP is unavailable.

No password, Duo code, API token, or licensed raw data may be pasted into chat, committed to Git, or written into research artifacts.

## Alternative-source decision standard

The representative's response should be evaluated in this order:

### A. WRDS account approved with CRSP US Stock

Use CRSP CIZ. Configure `WRDS_USERNAME` locally and authenticate using the normal WRDS/Duo process. The first operation remains identifier-only. Do not request returns in the same step.

### B. WRDS approved but CRSP absent

Inventory the institution's Compustat, LSEG/Refinitiv, Bloomberg, FactSet, or other historical-security products. A source passes only after permanent-identifier, corporate-action, terminal-value, historical-market-cap, and license checks. Brand recognition or visible old price bars is not sufficient.

### C. Individual account denied but faculty sponsorship available

Request the appropriate faculty-sponsored Research Assistant account. Do not use another person's credentials or a shared faculty login.

### D. No institutional route

Run a documented trial or small coverage audit before purchasing anything:

- EODHD documents retained histories for delisted symbols and is a candidate coverage source, but its terminal merger/liquidation value and total-return semantics must be verified on the eight-event seed.
- Norgate Platinum/Diamond documents a US Delisted universe, but does not claim complete historical delisted coverage and still requires terminal-return and identifier auditing for this design.
- Sharadar documents active and delisted major-exchange securities but is a premium product and requires the same corporate-action and terminal-value audit.

None is called “CRSP-equivalent” merely because it includes delisted tickers. Do not purchase a product until an eight-event schema/coverage demonstration and license review show that it can answer the research question.

## Prohibited work during the pause

- Do not calculate the two Yahoo-covered event returns.
- Do not replace missing firms with current survivors.
- Do not infer a delisting return from the last quoted close or assign an arbitrary -100% return.
- Do not tune event windows, spike thresholds, exits, benchmarks, size cutoffs, or cost assumptions on the eight-event seed or consumed Hwang events.
- Do not call the seed an analysis sample, call the work a replication, assign it a hypothesis or experiment ID, or describe alpha as supported.
- Do not combine CIZ `DlyRet` with a second legacy delisting adjustment.
- Do not begin a paid-data subscription without checking coverage, semantics, cancellation terms, and license restrictions.

## Resume decision tree

When the representative replies, record the response date and the datasets/account type actually offered, then follow exactly one branch:

```text
CRSP + programmatic access
    -> authenticate locally
    -> schema audit
    -> identifier-only eight-event PERMNO query
    -> manual link review
    -> return and event-time-cap coverage audit

WRDS without CRSP / another institutional vendor
    -> source-semantic audit
    -> eight-event identifier and terminal-value probe
    -> compare against frozen acceptance requirements

No institutional access
    -> evaluate one paid trial at a time, return-blind
    -> stop if permanent identity or terminal value fails
```

Only after all eight links and coverage paths are reviewed may return extraction begin. Registration still requires independent event coding, a predeclared size rule, concurrent-news controls, development/holdout separation, estimator and inference choices, multiple-testing accounting, and explicit long-versus-short cost models.

## Exact CRSP resume commands

Set the username only in the local PowerShell session:

```powershell
$env:WRDS_USERNAME = "your_wrds_username"
```

Run the identifier-only gate:

```powershell
python -m engineering.sandbox.clinical_evidence_mispricing.probe_wrds_crsp_access --connect --link-ledger engineering/sandbox/clinical_evidence_mispricing/small_biotech_phase3_failures_seed.csv
```

Then run focused validation before any new extraction:

```powershell
python -m pytest engineering/sandbox/clinical_evidence_mispricing -q
```

## Adversarial status at pause

**INCONCLUSIVE; promotion prohibited.** The strongest evidence is that the reconstruction and CRSP adapter are technically coherent and the eight-event seed preserves disappeared firms. The blocking weakness is that no eligible, delisting-complete return panel or event-time size data has been obtained. The smallest uncertainty-reducing next step is the return-blind identifier and coverage audit, not a backtest.

## Resume checklist

- [ ] Institutional response archived without private credentials
- [ ] Available vendor and exact subscribed datasets confirmed
- [ ] Programmatic/license restrictions confirmed
- [ ] Historical identifier schema verified
- [ ] All eight event-time security links manually reviewed
- [ ] Delisting/terminal-value semantics verified
- [ ] Event-time market capitalization coverage verified
- [ ] Independent event/timestamp second coding complete
- [ ] Concurrent-news and corporate-action coding complete
- [ ] Development/holdout and decision rules registered before returns

## Connections

- `datasets/small_biotech_phase3_failure_reconstruction.md`
- `source_scouting/2026-08-21-delisting-safe-price-source-audit.md`
- `source_scouting/2026-08-21-small-biotech-announcement-timing-audit.md`
- `research_journal/2026-08-21-crsp-ciz-access-gate.md`
- `weekly_reviews/2026-08-21-small-biotech-reconstruction-review.md`
- `engineering/sandbox/clinical_evidence_mispricing/README.md`
- `ideas/hypothesis_queue.md`
