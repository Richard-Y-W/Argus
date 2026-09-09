# Hwang current-collaborator probe — 2026-08-21

**Stage:** sandbox exploration  
**Attribution:** Human-directed  
**Claim eligibility:** none

Richard asked Argus to proceed from feasibility toward an alpha test. Argus first selected a public, peer-reviewed event seed rather than choosing memorable biotech winners. Hwang (2013) publishes 24 announcements with NCT IDs and pre-coded outcome signs: 16 positive and 8 negative.

The live ClinicalTrials.gov API was queried for each record on 2026-08-21. Current collaborator fields appeared in 4/16 positive events (25.0%) and 3/8 negative events (37.5%). The exploratory positive-outcome odds ratio was 0.556 and the two-sided Fisher exact p-value was 0.647.

## Interpretation

The broad “any collaborator listed” proxy points in the wrong direction and is not supported even as an attractive exploratory pattern. More importantly, the records carry a 2026-08-21 version holder and may include collaborators or vendors added after the 2011–2013 announcements. The result is therefore a feature-sparsity and definition test, not historical prediction.

The exercise narrows the program: registry collaborator presence is too administrative and weak. Only a historically public, asset-specific, costly external commitment remains worth testing. Examples in the probe illustrate the contamination problem: acquisitions can turn a former outside collaborator into the sponsor's owner, and a current record can list numerous trial-service vendors without showing when they were added.

## Decision

Do not attach returns to this invalid proxy. Do not register an alpha experiment. Build a newer small-biotech event universe with recoverable SEC acceptance timestamps and archived ClinicalTrials.gov versions, then code commitments without inspecting returns. The current broad collaborator proxy is rejected; the narrow commitment hypothesis remains untested.

## Connections

`datasets/hwang_2013_clinical_events.md` · `ideas/2026-08-21-biotech-collaborator-capacity-signals.md` · `weekly_reviews/2026-08-21-biotech-collaborator-signal-review.md`

