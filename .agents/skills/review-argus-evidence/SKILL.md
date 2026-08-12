---
name: review-argus-evidence
description: Adversarially audit Argus quantitative research for statistical, econometric, economic, engineering, and communication weaknesses. Use when reviewing a hypothesis, preregistration, experiment, result, figure, backtest, literature synthesis, pull request, research claim, or proposed next step before accepting or promoting it.
---

# Review Argus Evidence

Read the claim artifact, its registration, code, generated outputs, dataset record, and closest prior failures. Use `references/review-rubric.md` to keep the audit systematic.

## Review procedure

1. Restate the narrowest claim actually supported by the artifact.
2. Reconstruct the evidence chain from source data through transformations, estimator, output, and prose.
3. Check whether the hypothesis, sample, endpoint, and decision rule were fixed before outcome inspection.
4. Attack timing, leakage, survivorship, revisions, selection, missing data, dependence, inference, multiple testing, researcher degrees of freedom, and robustness design.
5. Compare effect magnitude with uncertainty and practical scale. Do not treat significance as importance.
6. Identify alternative mechanisms and whether the experiment discriminates among them.
7. Check code reuse, determinism, provenance, tests, and agreement among tables, figures, and prose.
8. Search prior Argus failures for repeated assumptions or already-rejected explanations.
9. Classify findings by severity: blocking, material, or improvement.
10. Recommend the smallest test or change that most reduces uncertainty.

## Output contract

Lead with `SUPPORTED`, `SUPPORTED WITH LIMITS`, `INCONCLUSIVE`, or `NOT SUPPORTED`. Then state the exact claim, strongest evidence, findings with file evidence, unidentified quantities, required wording changes, minimum next verification, and whether the artifact may be promoted.

Do not manufacture objections. If a risk is hypothetical because an artifact is missing, label it as an unresolved check.
