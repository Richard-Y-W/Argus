# Cycle plan — canonical JKP decay migration

*Registered 2026-07-23 before implementation or parity execution. AI-led; non-claim-bearing engineering cycle.*

## Objective

Remove the duplicated metadata parsing, event-window construction, and fixed-effects estimator from EXP-016 by making `engineering.argus_lab.jkp_decay` the canonical implementation. Preserve every committed EXP-016 estimate and eligibility count within numerical tolerance.

## Frozen checks

1. The migrated EXP-016 analysis must reproduce all numeric fields in its committed `estimates.csv` to absolute tolerance `1e-10`.
2. The eligible US factor count and observation count must not change.
3. Metadata exclusions must remain auditable by reason; migration cannot silently convert malformed rows into eligible rows.
4. The experiment-owned script remains the deterministic entry point and continues to write the same result filenames.

## Failure rule

Any failed parity check blocks the migration. A mismatch will be documented rather than reconciled by changing tolerances after inspection.

## Adversarial review before execution

- **Skeptic:** refactoring can change a result while appearing cosmetic; compare all estimates, not one headline coefficient.
- **Statistician:** covariance and within-factor demeaning semantics must remain identical.
- **Engineer:** shared code should expose explicit metadata flow rather than hiding exclusions.
- **Economist/portfolio reviewer:** this cycle improves provenance only and adds no evidence about trading or mechanism.

## Connections

EXP-016 · EXP-017–021 · `engineering/argus_lab/jkp_decay.py` · `README.md`
