# CRSP CIZ access gate for the Phase III failure reconstruction

**Evidence status:** engineering gate; no result

The free-history failure was not interpreted as a null and the two surviving stocks were not tested. Instead, the lab audited sources capable of preserving disappeared firms. CRSP CIZ is the only currently verified route that supplies lifecycle-stable PERMNO linkage and documented delisting-inclusive daily returns.

Argus implemented schema discovery, identifier-only query construction, event-time name/ticker/effective-date validation, and a daily-coverage audit. The audit requires 252 pre-event sessions plus the full +100 path, or a terminal row explicitly marked as a delisting with a usable CIZ total return. It rejects unexplained truncation and prevents historical AXON from being confused with the later ticker user.

Eight focused tests pass. A readiness probe found the WRDS package installed but `WRDS_USERNAME` absent. No connection was attempted, no identifier was retrieved, and no return was inspected.

While that access gate remained closed, a separate return-blind timestamp audit resolved the seed's four `date_only` rows as pre-market and independently confirmed the one after-market row. All eight candidates now have a single-coded market-session classification; none is dual-coded.

## Decision

Keep the hypothesis unregistered. The next action is a Duo-authenticated, return-blind historical identifier query for all eight candidates. Only after manual link review may the lab audit CRSP return and event-time capitalization coverage. Clinical second coding and concurrent-news checks remain required before a development/holdout design can be registered.

## Institutional pause

The researcher's Undergraduate/Master's WRDS account request was not approved. Richard chose to pause and return after the institutional representative responds. `research_governance/2026-08-21-biotech-wrds-access-pause.md` preserves the full state, alternative-source standards, prohibited shortcuts, and resume decision tree. This changes scheduling, not the inconclusive evidence classification.
