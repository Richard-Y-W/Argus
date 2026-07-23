# 2026-07-23 — Making a stable result harder to change accidentally

Two AI-led infrastructure cycles addressed the repository's next-phase engineering priority without presenting another return-only slice as new evidence. The first migrated EXP-016's duplicated JKP workflow into the canonical shared module and reproduced every committed result. The second added synthetic semantic tests and a licensed-data golden comparison. Ten tests, the manifest verifier, and compilation checks passed.

The main lesson is modest: reproducibility is not just the ability to rerun code today. It also requires alarms when tomorrow's refactor silently changes the sample, event clock, covariance estimator, or contrast. Exact parity is useful but circular, so it must sit beside small tests whose expected behavior can be reasoned through by hand.

## Human growth digest

- **Concept:** a golden test freezes observed behavior; a semantic unit test states why that behavior should be correct.
- **Mistake to avoid:** interpreting refactor parity as independent empirical confirmation.
- **Question:** which parts of an empirical pipeline deserve exact golden tolerances, and which should allow principled numerical variation across library versions?

## Connections

EXP-016 · `engineering/argus_lab/jkp_decay.py` · `engineering/tests/test_jkp_decay.py` · `researcher_scorecard.md`
