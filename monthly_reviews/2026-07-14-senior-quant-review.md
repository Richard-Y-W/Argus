# Senior quantitative research review of Argus

*Perspective: skeptical internal review at a top systematic-equities organization; not an assertion of employment or affiliation.*

## Executive judgment

Argus is a strong early-stage **scientific research record** and a weak **production quant platform**. I would keep the project alive, but I would not allocate capital, headcount, or a production mandate based on its current evidence.

Indicative grades: scientific honesty **A−**; empirical identification **B−**; research breadth **C−**; engineering **C**; alpha/trading readiness **D**.

## What is genuinely good

- Registration precedes results in Git.
- Negative results are first-class artifacts; six of nine experiments are failed or inconclusive.
- Controls have killed appealing findings rather than being used cosmetically.
- The lab distinguishes gross anomaly returns, causal mechanism, and tradability.
- Dataset provenance, timing limits, AI attribution, and post-hoc work are disclosed.
- EXP-002/003 are the strongest work: placebo comparison and staggered event-time identification materially improve on a simple replication.

## What would fail an institutional review

1. **One dataset, one market, one theme.** Nine experiment IDs over the same C&Z US panel are not nine independent pieces of evidence.
2. **No alpha object.** There is no implementable forecast, portfolio optimizer, risk model, capacity model, or net performance analysis.
3. **No direct arbitrage observables.** Return decay and correlations do not show who traded, how much capital entered, or what price impact occurred.
4. **Gross returns only.** No borrow, turnover, spread, market impact, financing, or crowding stress.
5. **Weak engineering depth.** Two synthetic tests, duplicated loaders, loose dependency bounds instead of a lockfile, no CI, no dataset checksums, no schema validation.
6. **Research degrees of freedom remain high across cycles.** Individual experiments are registered, but the sequence of questions is adaptively chosen from prior results. That is appropriate science, but the full thread is not one untouched confirmatory test.
7. **Human key-person risk has become AI process risk.** Autonomy solves throughput, not judgment. A second independent reviewer has not reproduced the claims.

## Decision

Continue as a research apprenticeship and falsification engine. Freeze additional cross-sectional slicing of the same panel unless the design is within-signal or uses a genuinely new identification source.

## Required next phase

1. Acquire one direct quantity dataset: FINRA short volume, institutional holdings, securities lending, or CRSP volume/turnover around publication.
2. Acquire C&Z alternative portfolios and run within-signal EW/VW and liquidity-screen comparisons.
3. Add a reproducible environment lock, checksums, schema tests, CI, and one canonical event-window loader.
4. Replicate the strongest result in a second market or data family.
5. Predeclare a small confirmatory battery before acquiring outcomes; separate it from exploratory sandbox work.
6. Only then evaluate net-of-cost economic magnitude and capacity.

## Bottom line

Argus currently demonstrates unusually good research hygiene and increasingly good skepticism. It does **not** yet demonstrate proprietary alpha, an arbitrage mechanism, or institutional research infrastructure. The main risk is no longer dishonesty or cherry-picking; it is spending too many cycles extracting fragile stories from one exhausted panel.
