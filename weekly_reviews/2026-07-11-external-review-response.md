# 2026-07-11 — Response to first external review

An external reviewer assessed the repository (verbally, via the researcher). Verdict in brief: strong research philosophy (8/10), weak as a portfolio of demonstrated research (5.5–6/10) — "more impressive as a manifesto than as a research project." The criticisms were specific, and most were correct. Actions taken the same day:

## Accepted and fixed

1. **Grandiose charter language.** "One of the world's best quantitative researchers" and the named-firms audience list announced ambition instead of demonstrating work. Reworded: the charter now describes an apprenticeship that improves the researcher's ability to formulate, test, and communicate hypotheses independently, written to withstand skeptical senior review — without name-dropping the reviewers.
2. **False precision in the Independent Thinking Index.** "15% human-originated direction" had no measurement model behind it, and this lab forbids exactly that kind of number elsewhere. Replaced (charter + scorecard) with a four-level categorical attribution ledger — AI-led / Human-directed / Collaborative / Human-led — where the dated evidence column carries the claim. Existing rows were relabeled, not softened: two cycles are AI-led, one thread selection and EXP-001 are Human-directed, nothing yet is Human-led.
3. **Structure outrunning evidence.** True: ~20 top-level folders, three experiments, an empty failed-experiments archive. The folders stay (conventions are cheapest before content exists) but the README now says this out loud in a "Current state" section, tells reviewers to weigh completed work rather than scaffolding, and points to the strongest single artifact first.
4. **The missing artifact: one cycle with visible human intellectual contribution.** The reviewer's ten-part structure (prediction → mechanism → competing explanations → own design → AI critique → revision → code → results → postmortem → attribution) is now the standing template for EXP-004: `experiments/EXP-004-placebo-spillover/researcher-worksheet.md`. The cycle is blocked until the researcher fills sections 1–5. This was already the plan (the EXP-004 prediction question was left open after EXP-003); the worksheet formalizes it.

## Noted, not actioned

- The reviewer praised the scorecard's honesty about who did what. That stays untouched — it is the load-bearing credibility of the whole ledger, and softening it to look better would be the exact failure mode the charter forbids.
- "Fifty more automated experiments would do less than one human-led one" — agreed; the queue after EXP-004 is deliberately short until that artifact exists.

## Meta-lesson for the lab

The reviewer applied our own charter to us: claims should not outrun evidence, and precision should not outrun measurement. Both violations lived in the *governance documents* rather than the experiments — the place we were least in the habit of auditing. Standards documents need the same skeptical read as results documents.
