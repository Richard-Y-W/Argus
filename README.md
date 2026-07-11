# Argus

An autonomous quantitative finance **research laboratory** — not a trading bot.

Argus exists to do one thing: compress a multi-year research apprenticeship into the shortest honest timeframe, by pairing a human researcher with an AI that acts as mentor, scientist, critic, and archivist. The measure of success is not returns. It is the growth of the researcher and the compounding of documented, reproducible knowledge.

- **Founding document:** [`ARGUS_CHARTER.md`](ARGUS_CHARTER.md)
- **Operating conventions:** [`CLAUDE.md`](CLAUDE.md)
- **Researcher growth record:** [`researcher_scorecard.md`](researcher_scorecard.md)
- **The story so far:** [`research_journal/`](research_journal/)

## What you will find here

Papers read and criticized. Hypotheses debated before they were tested. Experiments designed with controls, baselines, and leakage checks. Failed experiments documented with the same care as successes — most hypotheses *should* fail. Mathematical notes. Weekly meta-learning reviews. A knowledge graph connecting all of it.

## What you will not find here

Cherry-picked backtests. Hidden failures. Unlabeled axes. Claims of causality without evidence. Strategies sold as products.

## Current state — read this before judging the architecture

*Honest as of 2026-07-11.* The directory structure was built ahead of the evidence, deliberately: conventions are cheapest to fix before content exists. A reviewer should weigh the completed work, not the scaffolding. What actually exists:

- **Three completed experiments** on Chen–Zimmermann open data, each with a registered hypothesis committed before analysis ran: a replication of McLean & Pontiff's publication-decay result (EXP-001), a placebo control-group test of it (EXP-002), and a calendar-time vs event-time decomposition (EXP-003). Four of twelve registered predictions across EXP-002/003 failed; the failures are documented at the same resolution as the passes.
- **A contribution ledger** (`researcher_scorecard.md`) stating plainly which cycles were AI-led and which were human-directed. So far the researcher has directed one thread and executed nothing — the ledger says so.
- **Empty folders** (`failed_experiments/`, `monthly_reviews/`, `mathematical_notes/`, …) that are commitments, not accomplishments.

The next milestone is a fully researcher-led cycle (EXP-004): the researcher's own prediction, mechanism, design, and postmortem, with the AI as critic and implementer — the artifact that lets a reader distinguish what the human believed, designed, and learned from what the machine contributed.

*Suggested reading order for a skeptical reviewer: `experiments/EXP-003-calendar-vs-event-time/results.md` (the most complete single artifact), then the research journal from the first entry, then the scorecard.*
