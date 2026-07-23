# Cycle plan — JKP decay golden regression coverage

*Registered 2026-07-23 before test implementation or execution. AI-led; non-claim-bearing engineering cycle.*

## Objective

Add deterministic tests for the shared JKP event-window and estimator semantics, plus a local-data golden comparison against the committed EXP-016 output. The tests should catch changes to boundary years, eligibility rules, fixed effects, clustering, or reported contrasts.

## Frozen checks

1. Synthetic metadata tests cover ambiguous years, publication-before-sample-end, duplicates, and valid rows.
2. Synthetic panel tests cover exact sample-end and publication-year boundaries and the 12-month eligibility floor.
3. A synthetic estimator fixture has frozen coefficient and contrast values.
4. When licensed local JKP files exist, a golden test compares the canonical estimator with committed EXP-016 estimates at absolute tolerance `1e-10`; in data-free CI it skips explicitly.
5. The complete data-independent unit suite and repository verifier must pass.

## Failure rule

No tolerance widening or fixture replacement is allowed in response to a failure unless the behavioral change is separately explained and reviewed. This cycle passes only if all available checks pass and data-dependent skips are reported.

## Adversarial review before execution

- **Skeptic:** a golden test can fossilize a bug; pair it with small synthetic tests whose expected semantics are intelligible.
- **Statistician:** assert estimands and contrasts, not implementation-private objects.
- **Engineer:** licensed data cannot become a CI dependency; absence must produce an explicit skip.
- **Economist/portfolio reviewer:** regression stability is not external validity or economic validation.

## Connections

EXP-016 · `engineering/tests/` · `engineering/verify_repository.py` · canonical migration cycle
