---
name: run-argus-research-cycle
description: Develop and execute rigorous Argus quantitative-finance research from question triage through literature lineage, preregistration, reproducible testing, interpretation, and archival updates. Use for new research questions, hypothesis proposals, experiment design or implementation, replications, robustness work, and deciding what Argus should test next.
---

# Run Argus Research Cycle

Read `ARGUS_CHARTER.md`, `CLAUDE.md`, and the closest relevant prior artifacts before acting. Use `references/research-gates.md` as the stage-gate checklist.

## Route the request

1. Classify the work as scouting, exploration, registration, execution, interpretation, replication, or synthesis.
2. Trace the closest prior claims, experiments, failures, datasets, and literature before creating a new artifact.
3. Decide whether the task can support a claim. Sandbox exploration and practitioner sources may generate questions but cannot establish evidence.

## Execute the cycle

1. State the question and competing mechanisms in falsifiable terms.
2. Establish literature and data lineage. Distinguish primary evidence from commentary.
3. Specify predictions, falsifiers, estimand, sample, timing, controls, uncertainty method, and robustness checks before confirmatory execution.
4. Record expected failure modes, leakage risks, multiple-testing exposure, dependence structure, and what the design cannot identify.
5. Establish the preregistration boundary before inspecting confirmatory outcomes.
6. Implement with canonical loaders and small deterministic modules. Keep raw data immutable and record provenance or fingerprints.
7. Run relevant tests and the registered analysis. Preserve outputs and exact configuration needed to reproduce the result.
8. Interpret magnitude, uncertainty, breadth, and external validity separately. Distinguish statistical evidence, economic mechanism, and tradability.
9. Write the result whether it succeeds, fails, or is inconclusive. Do not silently change the hypothesis or endpoint.
10. Update the appropriate journal, scorecard, knowledge graph, queue, and failure/success location.

## Output contract

Report the research stage and attribution level; question, mechanism, and alternatives; evidence inspected and missing; registered decision rule or reason registration is premature; result with magnitude and uncertainty; strongest adversarial interpretation; bounded conclusion and next discriminating test; files changed and verification performed.

Stop and label the work exploratory when the evidence boundary cannot be established.
