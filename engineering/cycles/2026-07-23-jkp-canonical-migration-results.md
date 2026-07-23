# Cycle result — canonical JKP decay migration

## Verdict

**Passed every frozen parity check.** EXP-016 now imports its metadata parser, annual event-window assignment, eligibility filter, fixed-effects estimator, and result-row formatter from `engineering.argus_lab.jkp_decay`.

## Evidence

- Regenerating EXP-016 produced no diff in any committed result file.
- The primary US specification retained 101,920 observations and 141 factors.
- All eight numeric fields for all four EXP-016 specifications remained unchanged in the regenerated CSV.
- Metadata flow still records every source row and its exclusion reason.
- The six pre-existing engineering tests passed after migration.

## Adversarial review

This is reproducibility evidence, not independent replication. Both the old committed output and migrated implementation use the same raw release, annual publication metadata, and statistical specification. Exact parity can preserve an old modeling error; cycle 2 therefore adds intelligible synthetic semantic tests rather than relying only on output identity.

## What remains unknown

The migration does not improve publication-date precision, external validity, mechanism identification, transaction-cost realism, or evidence about who traded.

## Reproduction and connections

Run `python experiments/EXP-016-standalone-us-jkp-decay/analysis.py`, then inspect `git diff -- experiments/EXP-016-standalone-us-jkp-decay/results`. Plan: `engineering/cycles/2026-07-23-jkp-canonical-migration-plan.md`. EXP-016 · EXP-017–021 · golden regression cycle
