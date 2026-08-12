# Argus Agent Guidance

Argus is an autonomous quantitative-finance research laboratory, not a trading bot or financial-advice system. Read `ARGUS_CHARTER.md` before substantive research and follow `CLAUDE.md` for repository conventions.

## Working rules

- Optimize for credible knowledge, reproducibility, and researcher learning rather than attractive returns.
- Separate exploration, registered evidence, mechanism, and tradability. Never promote sandbox output into a claim.
- Preserve failures at the same resolution as successes. Never cherry-pick, conceal nulls, or rewrite a hypothesis after seeing results.
- Use only information available at the relevant decision time; actively check leakage, survivorship, data revisions, multiple testing, and dependence.
- Keep language proportional to identification. Do not infer causality, trading activity, capacity, or net profitability from return patterns alone.
- Reuse canonical loaders and statistics under `engineering/argus_lab/`; place disposable probes under `engineering/sandbox/`.
- Run the narrowest relevant tests during iteration. Before declaring repository work complete, run `pytest engineering/tests` and `python engineering/verify_repository.py` when the required local data are available.
- Do not modify unrelated work or raw/licensed datasets.

## Project skills

- Use `$run-argus-research-cycle` for question triage, literature lineage, hypothesis registration, experiment design, execution, and archival updates.
- Use `$review-argus-evidence` for adversarial reviews of hypotheses, code, results, figures, claims, and proposed next steps.

Keep durable project facts in repository documents. Keep repeatable procedures in skills and load detailed artifacts only when the active task requires them.
