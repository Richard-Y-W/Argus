# Kakushadze & Serur (2018) — *151 Trading Strategies*

*Note type: reference/catalog, not an empirical paper. Read: TOC + abstract + structure skim, 2026-07-09. SSRN 3247865. Local copy: `C:\Users\richa\Downloads\ssrn-3247865.pdf`.*

## What it is

A book-length **catalog** of 150+ trading strategy *descriptions* across asset classes — options (ch. 2 is ~57 option payoff structures: spreads, straddles, condors), stocks (momentum, value, low-vol, pairs, mean-reversion, moving averages), fixed income, futures, FX, commodities, volatility, crypto, and more. Over 550 formulas, ~2,000 bibliographic references, a glossary, and illustrative backtesting code. By its own abstract: *"the presentation is intended to be descriptive and pedagogical."*

## Main claim / framework

There is no hypothesis and no empirical result. The framework is taxonomic: for each strategy, a definition, construction formulas, and citations to the literature that studied it.

## What it does NOT contain (the important part)

- **No performance data** — no returns, no Sharpe ratios with standard errors, no out-of-sample tests.
- **No publication dates or sample periods per strategy** — so no way to run in-sample / post-sample / post-publication comparisons.
- **Little transaction-cost or capacity analysis.**
- Chapter 2's option structures are not anomalies at all — a covered call is a *payoff shape*, not a return predictor. Cataloging it next to momentum blurs a distinction that matters: a strategy's *construction* vs. its *edge*.

## How Argus will use it

1. **Vocabulary and map**: when an unfamiliar strategy name appears in a paper or conversation, this is the lookup table.
2. **Bibliography mining**: the ~2,000 references are a decent index into the literature by topic.
3. **Not as a research agenda.** See criticism below.

## Criticism / hazard

Treating this catalog as a menu of 151 things to backtest is the multiple-testing trap industrialized. Testing 151 strategies guarantees that the best few look excellent by luck alone; the significance hurdle rises with the number of trials (Harvey–Liu–Zhu 2016). A catalog with no evidence attached is maximally tempting and minimally informative — useful precisely and only as a reference.

## Relationship to Chen & Zimmermann (Open Source Asset Pricing)

Complementary, different objects:

| | Kakushadze & Serur 2018 | Chen & Zimmermann (openassetpricing.com) |
|---|---|---|
| Object | strategy *descriptions* + formulas | replicated predictor *returns* + code |
| Scope | all asset classes | cross-sectional US stock predictors (~200+) |
| Evidence | none | monthly returns per predictor, full history |
| Publication metadata | no | yes (sample end, publication year) |
| Usable for decay research | no | yes — it is the raw material |

For the anomaly-decay thread, C&Z is the workhorse dataset; this book is a shelf reference.

## Connections

- `ideas/2026-07-09-anomaly-decay-prior.md` — the active research thread this does *not* serve directly
- McLean & Pontiff (2016), SSRN 2156623 — next read (researcher's own read + `papers/` note)
- Harvey, Liu & Zhu (2016) — why a 151-strategy menu is statistically dangerous
- Chen & Zimmermann — candidate dataset for EXP-001
