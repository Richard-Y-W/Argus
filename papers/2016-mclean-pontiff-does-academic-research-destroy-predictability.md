# McLean & Pontiff (2016) — Does Academic Research Destroy Stock Return Predictability?

*Journal of Finance 71(1), 5–32. SSRN 2156623. Note written by Argus 2026-07-10 (facts verified against published sources; researcher digest pending).*

## Main hypothesis

Publication of a cross-sectional return predictor changes its subsequent returns. Two channels are separately identifiable: **statistical bias** (in-sample returns overstated by data mining / sampling error) and **publication-informed trading** (arbitrageurs learn from the paper and trade the effect away).

## Design (the paper's core innovation)

Replicate 97 published cross-sectional predictors and compare mean long-short returns across three windows per predictor:

1. **In-sample** — the original study's sample period.
2. **Post-sample, pre-publication** — after the sample ends, before publication. Decay here can only be statistical bias (no one has read the paper yet).
3. **Post-publication** — decay here is bias *plus* the publication effect.

Identification: post-sample decay estimates statistical bias; the *additional* post-publication decay estimates the effect of publication itself. Panel regressions of predictor returns on post-sample and post-publication dummies, with predictor fixed effects and month-clustered standard errors.

## Key results

- Returns are **26% lower post-sample** → upper bound on data-mining bias.
- Returns are **58% lower post-publication** → implies a **32-point publication effect** (58 − 26).
- **Returns do not go to zero** — decay is partial.
- Post-publication: volume, variance, and short interest in anomaly stocks **rise** → arbitrageurs respond to publication.
- Predictors concentrated in **costlier-to-arbitrage** stocks (illiquid, high idiosyncratic risk, small) decay **less** → limits to arbitrage bound the correction.
- Anomaly returns correlate more with *other published* anomalies post-publication → common arbitrage capital.

## Assumptions & limitations

- Replication of predictors is approximate (they match published t-stats imperfectly).
- Publication date is a coarse information-release proxy (working papers circulate years earlier — attenuates the measured publication effect toward zero).
- US equities only. (See Jacobs & Müller 2020: the decline does not replicate reliably outside the US.)
- Post-sample windows are short for many predictors → noisy bias estimates predictor-by-predictor; only the pooled estimate is well identified.

## Criticisms / open questions

- Working-paper circulation blurs the post-sample/post-publication boundary.
- Decay could partly reflect regime change (falling trading costs, decimalization) coinciding with publication dates rather than caused by publication.
- Which anomalies decay fastest — and does the *rate* of decay accelerate as publication count grows (crowding)?

## Connections

- Predicted (partially) by the researcher's day-zero prior: `ideas/2026-07-09-anomaly-decay-prior.md`
- Statistical-bias channel formalized by [[harvey-liu-zhu-2016]] (multiple testing)
- International non-replication: `papers/2020-jacobs-muller-anomalies-across-the-globe.md`
- Data for replication: `papers/2022-chen-zimmermann-open-source-asset-pricing.md`
- Replicated in: `experiments/EXP-001-anomaly-decay/`
