# How an academic result becomes an arbitrage trade

*Lineage review, 2026-07-14. This is a conceptual genealogy, not a claim that every later paper formally cites every earlier node.*

## The central mechanism

An empirical paper can convert costly private research into public information. Investors then encode the published rule into portfolios; their trades move prices against the rule, borrow and impact costs limit the correction, and the remaining return reflects some mixture of risk compensation, residual mispricing, and implementation friction. “The market digests the edge” is therefore not magic. It is a chain with separately testable links:

`costly discovery → selective publication → public signal → capital entry → price/quantity response → lower gross return → residual bounded by limits to arbitrage`

## Intellectual build-up

| Layer | Contribution | What the next layer inherited |
|---|---|---|
| Efficient-markets research | Public information should be incorporated into prices; event studies supply the timing logic. | Publication can be treated as an information event rather than merely a label. |
| Grossman–Stiglitz (1980) | Perfect informational efficiency is impossible when information is costly: informed traders need compensation. | Some edge can survive because discovery and implementation are costly. |
| Limits-to-arbitrage theory, especially Shleifer–Vishny (1997) | Mispricing can persist when arbitrage capital faces agency risk, redemptions, shorting limits, and horizon mismatch. | Publication need not erase an anomaly completely; decay should vary with implementability. |
| Data-snooping and publication-selection work | Researchers try many specifications, while journals disproportionately reveal successful ones. | A fall after the original sample can occur without any investor learning. |
| Harvey–Liu–Zhu (2016) | The factor zoo makes ordinary t-statistic thresholds unreliable under multiple testing. | Separates statistical overstatement from genuine post-disclosure trading effects. |
| McLean–Pontiff (2016) | Uses three windows—original sample, post-sample/pre-publication, post-publication—to estimate 26% OOS decline and 58% post-publication decline; interprets the extra 32 points alongside trading/correlation evidence as publication-informed arbitrage. | Supplies the empirical artifact Argus replicates and tries to falsify. |
| Chordia–Subrahmanyam–Tong (2014) | Attributes anomaly attenuation to cheaper trading and more arbitrage capital around common calendar changes. | Creates the competing “market infrastructure clock,” tested against publication event time. |
| Jacobs–Müller (2020) | Finds reliable post-publication decay mainly in the US. | Makes frictionless global learning implausible and raises the home-bias/frictions puzzle. |
| Chen–Zimmermann (2022) | Open implementations, metadata, and placebo characteristics make large-sample replication and control groups possible. | Turns a literature claim into an auditable panel for Argus. |

## What Argus added

1. **Replication:** EXP-001 reproduced the three-window pattern on 212 predictors through 2024.
2. **Negative control:** EXP-002 showed that published placebo characteristics do not reproduce predictor decay; predictor-minus-placebo post-publication decline was −0.26%/month (t ≈ −3.3).
3. **Two clocks:** EXP-003 found that 88% of the publication coefficient survives calendar-era controls. Staggered publication dates identify event time more sharply than a common 2001 break.
4. **Scale correction:** EXP-005 showed that apparent targeting of high-t-stat or volatile anomalies disappears after controlling for in-sample scale. Publication looks like an approximately proportional haircut, not selective hunting of the “best” anomaly.
5. **Failed discriminators:** EXP-006 and EXP-007 show that sample length and publication cohort do not cleanly identify the haircut's mechanism.
6. **Next link:** EXP-004 tests spillover. If capital trades published predictors, correlated placebo portfolios may be dragged along even though their papers made no predictability claim.

## Evidence map: what would demonstrate actual arbitrage?

| Link | Observable evidence | Current status |
|---|---|---|
| Investors learn the rule | Return decline begins on each paper's event clock | Supported by EXP-001/003, annual dates only |
| Capital trades it | Volume, short interest, holdings, flows, or price impact changes | Present in M&P; not yet independently replicated by Argus |
| Trades transmit across related signals | Correlated placebo decay tracks pre-publication exposure | EXP-004 |
| Frictions bound correction | More costly portfolios retain more return after scale controls | Open; current VW/EW hint is unregistered and small-n |
| Not just data mining | Post-sample and post-publication changes differ; placebos do not match | Supported by EXP-001/002 |
| Not just secular attenuation | Staggered publication clock survives calendar controls | Supported by EXP-003 |

## Important distinction

No-arbitrage pricing and “arbitrageurs trade away an anomaly” are different claims. A characteristic spread is not a literal riskless arbitrage. Here *arbitrage* means capital allocated to a positive-expected-return long–short rule, with factor risk, shorting costs, turnover, crowding, and model risk. The incomplete ~50% correction is therefore economically plausible without violating no-arbitrage theory.

## Sources and connections

- Grossman & Stiglitz (1980), *On the Impossibility of Informationally Efficient Markets*, AER, https://www.aeaweb.org/aer/top20/70.3.393-408.pdf
- Shleifer & Vishny (1997), *The Limits of Arbitrage*, Journal of Finance, DOI: 10.1111/j.1540-6261.1997.tb03807.x
- Harvey, Liu & Zhu (2016), *…and the Cross-Section of Expected Returns*, DOI: 10.1093/rfs/hhv059
- McLean & Pontiff (2016), *Does Academic Research Destroy Stock Return Predictability?*, DOI: 10.1111/jofi.12365
- Repository notes: `papers/` · `literature_reviews/2026-07-10-anomaly-decay.md` · `knowledge_graph/anomaly-decay-thread.md`
