# Biotech collaborator and capacity signals: source audit

**Stage:** source feasibility and identification audit  
**Attribution:** Collaborative  
**Decision:** proceed only to a return-blind 30-event gold-ledger pilot

## Public sources and time semantics

| Source | Observable | Historical-time limitation | Use |
|---|---|---|---|
| SEC EDGAR filings and exhibits | Material agreements, licenses, manufacturing deals, exact filing acceptance time | Agreement effective date can precede disclosure; exhibits may omit economic terms | Preferred source for public availability |
| ClinicalTrials.gov history | Lead sponsor and collaborators by record version | Current JSON contains later amendments and results; historical version must be recovered | Asset and collaborator linkage |
| USAspending awards | Awardee, agency, amount, action/modification dates, description | Action date is not publication date; reporting/publication lag varies by award class and agency | Government-commitment discovery, with archived release evidence required for historical tests |
| HHS/BARDA/agency releases and contract reading rooms | Contract announcements, scale-up, ancillary-supply programs | Emergency preparedness can support multiple candidates and reflect policy objectives | Source confirmation and government-risk-sharing flag |
| Company 8-K/6-K/press release | Asset-specific partner announcement and management description | Promotional framing; release timestamp may be less exact than EDGAR acceptance | Discovery, then primary-document validation |
| 10-K insurance disclosures | Coverage types and limits | Usually annual, boilerplate, not asset-specific, and potentially stale | Deprioritized control only |

## Moderna schema demonstration — not evidence

The COVID-19 program illustrates the source taxonomy but is outcome-known and cannot test prediction:

- ClinicalTrials.gov links the mRNA-1273 study with public-sector collaborators, subject to historical-version recovery.
- BARDA contract 75A50120C00034 funded development and domestic manufacturing scale-out; current USAspending data cannot establish the exact historical publication timestamp by itself.
- Moderna's filed Lonza announcement described worldwide manufacturing capacity that could reach one billion doses annually, conditional on the vaccine proving safe and effective. This is asset-specific and costly, but it may represent manufacture-at-risk rather than privileged efficacy information.
- The federal distribution strategy describes acquiring needles, syringes, vials, and related supplies for multiple vaccine candidates before regulatory decisions. That makes generic ancillary procurement a system-level preparedness measure rather than a Moderna-specific success signal.

## Identification threats

1. **Manufacture-at-risk:** rational option value can justify capacity before success is likely.
2. **Government risk sharing:** public money changes the counterparty's downside and weakens commitment as a belief-revelation device.
3. **Expected demand versus efficacy:** a signal can reveal market size or policy demand without revealing clinical probability.
4. **Endogenous selection:** stronger, larger, or better-financed sponsors attract partners and also have higher base success rates.
5. **Publication lag:** contract action dates, amendment dates, and registry update dates are not necessarily investable timestamps.
6. **Network dependence:** one agreement can generate many filings, releases, awards, and news stories; these are not independent confirmations.
7. **Survivorship and hindsight mapping:** successful assets and extant companies are easier to reconstruct.
8. **COVID regime:** emergency procurement, government guarantees, and unprecedented demand make generalization especially weak.

## Required fields

`signal_id`, `event_id`, `asset_id`, `focal_entity`, `related_entity`, `signal_type`, `published_at`, `availability_precision`, `action_date`, `source_url`, `source_hash`, `amount_or_capacity`, `asset_specific`, `external_party`, `costly_or_irreversible`, `government_risk_share`, `covid_regime`, and `coder_decision`.

Availability precision is one of `exact`, `date_upper_bound`, or `retrieval_only`. Only exact timestamps and conservative upper bounds may enter a historical test. Retrieval-only observations are discovery aids, not historical evidence.

## Sources inspected

- SEC EDGAR application programming interfaces and filing archives.
- ClinicalTrials.gov data API and record histories.
- USAspending API documentation, data-source/reporting-lag documentation, and Moderna award page.
- HHS Operation Warp Speed contract reading room and vaccine-distribution strategy.
- Moderna/Lonza SEC-filed press-release exhibit.
- Liu, Pu, and Schramm (2016), *Journal of Product Innovation Management*, on stock reactions to biopharmaceutical alliance announcements. That literature concerns announcement valuation and does not establish pre-readout clinical prediction.

## Gate decision

The source families are adequate for a small schema and coding-reliability pilot, but not yet for registration. The pilot must be return-blind, include negative outcomes, preserve archived public timestamps, and treat procurement and insurance as controls unless they pass the asset-specific commitment rule.

