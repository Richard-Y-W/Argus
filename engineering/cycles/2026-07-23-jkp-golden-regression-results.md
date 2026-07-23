# Cycle result — JKP decay golden regression coverage

## Verdict

**Passed every available frozen check.** Four tests now cover metadata exclusions, event-year boundaries, the 12-month eligibility floor, estimator contrasts, and full local-data parity with committed EXP-016 estimates.

## Evidence

- `python -m pytest engineering/tests -q`: **10 passed**; no skips on the local machine because the licensed JKP files were present.
- The local-data golden test matched eight EXP-016 US numeric fields at zero relative tolerance and `1e-10` absolute tolerance.
- The balanced synthetic fixture recovered frozen differences of 150, 450, and 300 percentage points for post-sample, post-publication, and their contrast.
- Metadata tests preserved explicit reasons for missing names/years, invalid date order, and duplicate names.
- `python engineering/verify_repository.py`: dataset manifest verified.
- `python -m compileall -q engineering experiments/EXP-016-standalone-us-jkp-decay`: passed.

## Adversarial review

The golden test deliberately skips with an explicit message in data-free CI; it therefore protects licensed-data runs but is not part of the always-on CI guarantee. Golden outputs can also fossilize errors. The small synthetic tests reduce that risk by asserting readable boundary and estimand semantics independently of the raw JKP release.

## What remains unknown

These tests detect implementation drift, not faulty source metadata or misspecification. They add no market claim and do not validate causal or trading interpretations.

## Reproduction and connections

Run `python -m pytest engineering/tests -q` and `python engineering/verify_repository.py`. Plan: `engineering/cycles/2026-07-23-jkp-golden-regression-plan.md`. EXP-016 · canonical migration cycle · `engineering/tests/test_jkp_decay.py`
