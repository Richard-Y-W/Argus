# Delisting-safe price-source audit for the small-biotech reconstruction

**Status:** source selected; access not authenticated  
**Decision:** use academic CRSP CIZ, subject to identifier and coverage gates

## Requirement

The eight-event feasibility seed contains firms that were acquired, renamed, merged, or disappeared. A usable source therefore needs permanent security identifiers, historical name/ticker intervals, daily total returns, corporate-action continuity, and explicit delisting treatment. Coverage may not be defined by whether a current ticker still downloads.

## Sources evaluated

| Source | Finding | Decision |
|---|---|---|
| Yahoo chart history | Only 2/8 identity-matched seed histories cover the frozen estimation and +100 windows; no permanent identifier or documented delisting-return treatment | Reject for claim-bearing analysis |
| Stooq public CSV | Direct historical endpoint returned a JavaScript verification page in the audit environment; no verified delisting-return semantics | Reject as current route |
| Nasdaq Data Link WIKI | Legacy endpoint is not an available maintained source for this universe | Reject |
| Nasdaq Daily List | Useful corporate-action/event metadata, but historical price products are subscription products and the list alone does not supply research returns | Supplement only |
| CRSP CIZ through WRDS | PERMNO provides lifecycle-stable security identity; historical security info supplies effective-date linkage; WRDS documents CIZ `DlyRet` as already incorporating delisting returns | Select |

## Local readiness result

The `wrds` Python package is installed. No `WRDS_USERNAME` was configured on 2026-08-21, so Argus did not initiate a connection or inspect any return. The adapter and its tests are under `engineering/sandbox/clinical_evidence_mispricing/`.

The first authenticated operation is deliberately return-blind: describe the two CRSP schemas and retrieve only historical PERMNO/PERMCO, ticker, issuer name, and effective dates for the eight candidates. Return extraction is prohibited until each link is reviewed.

## Primary documentation

- CRSP, “PERMNO & PERMCO”: permanent identifiers remain stable through name changes, mergers, and restructurings: https://www.crsp.org/research/permno/
- WRDS, “Run an Event Study (CIZ Format)”: the current CIZ event-study implementation uses `DlyRet` and states that delisting return is already incorporated: https://wrds-www.wharton.upenn.edu/pages/wrds-research/macros/run-an-event-study-ciz-format-macro/
- WRDS, “How to Log In to WRDS Using Multi-Factor Authentication”: remote PostgreSQL connections use Duo Mobile push: https://wrds-www.wharton.upenn.edu/pages/about/log-in-to-wrds-using-two-factor-authentication/

## Boundary

CRSP resolves survivorship-safe return coverage, not the whole design. Event-time market capitalization, independent clinical-event coding, exact announcement timing, concurrent news, and borrow feasibility remain unresolved. Passing the source gate will permit registration design; it will not establish alpha.
