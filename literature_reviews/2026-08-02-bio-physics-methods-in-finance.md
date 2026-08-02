# Biology and physics in finance: mechanisms before metaphors

*Reviewed 2026-08-02. AI-led screening of candidate methods for digital-asset and broader quant research. Sources were screened at abstract/method level; this is not a claim of full-paper mastery.*

## Research rule

Borrowing a mathematical object from biology or physics can be useful. Borrowing its vocabulary is not. A method earns a place in Argus only if:

1. the financial state variable has an observable counterpart to the original model;
2. the mechanism implies a prediction that a standard time-series or panel model does not already imply;
3. parameters can be estimated without selecting crises, regimes, or species after seeing outcomes;
4. it beats a simple benchmark out of sample or adds an interpretable diagnostic;
5. failure is recorded rather than repaired with a new analogy.

## Candidate families

### 1. Spatial diffusion and network integration — strongest fit

Physics models diffusion over a topology. Before global pooling, EVE PLEX traded in regional books separated by information and access frictions; after pooling, the topology changed by rule. Here nodes, quotes, depth, and the intervention are observable.

The useful prediction is not that prices “diffuse.” It is that pre-event price gaps and quote adjustment should relate to market connectivity, local depth, and hub distance, while a topology-removing intervention changes the cross-sectional adjustment process. Standard benchmarks are region fixed effects, autoregressive convergence, and common-factor models. A graph or diffusion model must improve held-out regional quote-gap forecasts or explain a preregistered response pattern beyond those benchmarks.

**Verdict:** Promote to sandbox after the PLEX extraction pipeline is built. It can add mechanism evidence about fragmentation, though not necessarily a trading edge.

### 2. Self-exciting point processes — useful only with event timestamps

Hawkes processes model events whose occurrence raises the near-term intensity of later events. Bacry, Mastromatteo, and Muzy review uses in trade arrivals, volatility, systemic contagion, execution, and order books ([review](https://arxiv.org/abs/1502.04592)); Bacry and Muzy connect trade arrivals, price changes, mean reversion, and market impact in a multivariate model ([model](https://arxiv.org/abs/1301.1135)).

EVE Ref order snapshots are not a transaction tape. Order `issued` timestamps can identify surviving order arrivals, but deleted orders and trades between snapshots are latent. Fitting Hawkes models to snapshot changes would confuse censoring with excitation. The method becomes defensible only if inferred-trade or event-level data are validated against daily volume.

**Verdict:** Conditional candidate, not the first experiment. Potential edge is intensity/risk forecasting, not directional returns.

### 3. Market ecology and evolutionary selection — promising theory, weak current measurement

Market-ecology models treat capital allocated to strategies as species abundance and strategy returns as density-dependent fitness. Scholl, Calinescu, and Farmer show in a toy market that strategy profitability depends on invested wealth and use community matrices and food-web concepts to explain instability ([working paper](https://arxiv.org/abs/2009.09454)). Empirically calibrated agent-based work extends this idea to mutual-fund styles ([Evology](https://arxiv.org/abs/2210.11344)).

For a real test, Argus needs strategy abundances or holdings—not merely asset prices. EVE market orders do not reveal whether the owner is a market maker, speculator, industrial user, or subscription buyer. Item categories can be “species” descriptively, but that does not identify ecological competition among strategies.

One narrower digital-economy use survives: model *assets* competing for a fixed spending or attention budget only when quantities and substitution sets are observed. Cross-price responses around an exogenous utility or sink change could distinguish competition from common demand. A flexible Lotka–Volterra fit without such a shock would be curve-fitting.

**Verdict:** High learning value; low immediate empirical readiness. Do not claim edge until abundance proxies exist.

### 4. Critical transitions and early-warning signals — highest false-discovery risk

Critical slowing down predicts rising recovery time, often measured through lag-one autocorrelation or variance, near particular bifurcations. Scheffer et al. synthesize the cross-disciplinary theory ([Nature review](https://www.nature.com/articles/nature08227)). Financial applications propose information-network flickering or information-dissipation diagnostics ([Scientific Reports 2019](https://www.nature.com/articles/s41598-019-42223-9); [Scientific Reports 2013](https://www.nature.com/articles/srep01898)). The latter also reports that conventional critical-slowing indicators did not clearly warn in its application.

The danger is selecting a famous crash, trying many windows/indicators, and calling a pre-crash rise predictive. Markets can jump because of news without approaching a bifurcation; nonstationary volatility can mimic the indicators; the number of independent crises is small.

A valid test must define collapse events mechanically from market rules or liquidity outcomes, freeze indicators and horizons, use rolling-origin evaluation, compare against volatility/liquidity baselines, and include non-event periods in the loss. Digital markets offer many platform-policy events but few independent issuer regimes.

**Verdict:** Suitable as a hostile replication with an untouched event holdout, not as an alpha-mining program.

### 5. Entropy and information flow — diagnostic, not automatically predictive

Entropy can measure concentration of displayed depth, order-size diversity, or distributional change. Mutual information and transfer entropy can capture nonlinear dependence, but finite-sample bias and multiple lag searches are severe. A falling order-book entropy may simply restate concentration already measured by Herfindahl indexes.

For PLEX, compare entropy diagnostics to spread, depth, Herfindahl concentration, and price-impact proxies. Require incremental held-out prediction of quote recovery or volume—not merely a visually striking regime chart.

**Verdict:** Reasonable secondary measurement family; must face simple concentration benchmarks.

## Ranked research program

| Rank | Imported idea | Observable mechanism in current data | Edge target | Readiness |
|---:|---|---|---|---|
| 1 | Network/spatial diffusion | Regional PLEX books become one global topology | Quote-gap and liquidity-state forecasting | High after extraction |
| 2 | Order-book entropy/resilience | Depth distribution and recovery after shocks | Incremental liquidity-risk signal | Medium |
| 3 | Hawkes excitation | Clustering of valid order/trade events | Event-intensity and execution risk | Low until event tape validated |
| 4 | Ecological competition | Density-dependent asset/strategy performance | Regime and crowding diagnostics | Low without abundance data |
| 5 | Critical slowing down | Recovery weakens before a defined transition | Crash/liquidity warning | High statistical risk |

## What “edge” should mean here

Three different claims must not be collapsed:

- **scientific edge:** explains a mechanism better than standard models;
- **forecasting edge:** improves truly out-of-sample loss after search accounting;
- **trading edge:** survives execution, fees, capacity, and operational constraints.

The PLEX archive can plausibly support the first two for in-platform liquidity. It cannot establish a fiat-investable trading edge. A biology/physics model that improves in-sample fit but not frozen out-of-sample loss has no forecasting edge.

## Recommended falsification sequence

1. Reproduce simple spread, depth, imbalance, dispersion, and recovery metrics.
2. Freeze standard autoregressive, factor, and panel benchmarks.
3. Add exactly one cross-disciplinary structure at a time.
4. Use rolling-origin or event holdouts chosen before fitting.
5. Correct for the number of method families tried, including abandoned ones.
6. Ask whether the imported structure adds mechanism, prediction, both, or neither.

## Connections

`datasets/eve_online_market_archives_2025.md` · `source_scouting/2026-08-02-digital-assets-and-complex-systems.md` · `ideas/hypothesis_queue.md`
