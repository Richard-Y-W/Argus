# Research program — self-replication, fluid mechanics, and biology in finance

*Generated 2026-08-02 from Richard's cross-disciplinary direction. These are candidate mechanisms, not claims or strategies.*

## Governing rule

A cross-disciplinary model needs four explicit maps:

| Source concept | Financial counterpart | Observable measurement | Distinguishing falsifier |
|---|---|---|---|
| State | What exists at each time/location | Point-in-time data field | State cannot be reconstructed without future data |
| Flow or interaction | What moves or interacts | Orders, trades, holdings, flows, links | Standard dependence model explains it equally well |
| Conservation/fitness law | Why the system changes | Accounting identity or payoff rule | Identity does not close in observed data |
| Boundary/environment | What constrains the dynamics | Market rules, capacity, capital, access | Boundary changes without predicted response |

If one row has only a metaphor, the model is not ready.

## 1. Fluid mechanics of an order book

### Possible mapping

Let price be the spatial coordinate `p`, time be `t`, and displayed buy/sell quantity density be `rho_side(p,t)`. Order submission, cancellation, and execution are source/sink terms. Quote motion or order repricing can be represented by a velocity field `u(p,t)` only if individual order identities or sufficiently fine snapshots reveal movement.

A conservation-style equation would resemble:

`partial_t rho + partial_p(rho u) = arrivals - cancellations - executions`.

This is closer to a continuity equation than to full Navier–Stokes. “Pressure” might represent order imbalance or latent demand, and “viscosity” might represent dissipative book replenishment or resistance to price displacement, but those labels are earned only after units and closure equations are defined.

### Why the mapping can fail

- Orders are created and destroyed, so quantity is not conserved without source/sink observations.
- Strategic agents change rules after observing the book; particles do not usually anticipate the fluid.
- Displayed liquidity omits hidden intentions, contracts, and inaccessible venues.
- Snapshot-to-snapshot order changes combine trades, cancellations, modifications, and missing observations.
- A fitted PDE can interpolate a smooth surface without providing an economic mechanism or forecast.

### Researchable PLEX version

Estimate order-density fields in relative-price coordinates and ask whether post-shock depth recovery is better forecast by a continuity/reaction–diffusion specification than by vector autoregression, exponential recovery, and simple state-space benchmarks. First test whether the continuity residual can be reconciled with daily reported volume. If it cannot, fluid inference stops.

**Status:** high-value mathematical note and sandbox; data closure must be audited first.

## 2. Turbulence and intermittent volatility

Fluid turbulence motivated multifractal and cascade descriptions of volatility long ago. Financial multifractality can also be produced by finite samples, heavy tails, and dependence; many diagnostics and detrending choices create search breadth. A turbulence analogy is therefore not novel.

The defensible question is narrower: does a preregistered cascade or multifractal model improve held-out liquidity-risk or volatility-density forecasts beyond GARCH, realized-volatility, and Markov-switching benchmarks? Evaluate probability forecasts, not attractive scaling plots. Include shuffled and phase-randomized surrogates to determine whether estimated multifractality exceeds what marginal tails and linear dependence produce.

**Status:** hostile replication candidate, not priority PLEX work.

## 3. Reaction–diffusion markets

Reaction–diffusion order-book models already exist. Buyers and sellers diffuse through price space and react when compatible orders meet; continuum approximations can yield price-volume scaling. Published work predates the PLEX event by decades, so the general idea is occupied ([2018 model](https://doi.org/10.1016/j.physleta.2017.12.024); [earlier branching model](https://arxiv.org/abs/cond-mat/9811114)). Hydrodynamic limits for Markov order books are also established ([hydrodynamic limit](https://arxiv.org/abs/1411.7502)).

For PLEX, the potentially new object is diffusion over *regions* before pooling, not invention of reaction–diffusion finance. A regional graph model must beat panel autoregression on held-out nodes and dates.

**Status:** highest-priority physics-informed empirical branch.

## 4. Kinetic theory and statistical mechanics

Kinetic finance treats agents or wealth shares like interacting particles and derives Boltzmann or Fokker–Planck equations. This is a mature econophysics program, particularly for wealth distributions and Pareto tails ([Toscani review](https://arxiv.org/abs/1005.5006); [knowledge and wealth model](https://arxiv.org/abs/1401.4550)).

PLEX order books do not reveal agent wealth or bilateral exchanges, so a kinetic wealth model is not identified. A possible future use is creator-level Roblox data or EVE wallet/holding microdata obtained through a platform partnership.

**Status:** mathematically relevant; blocked empirically.

## 5. Biological self-replication as strategy search

“Self-replication” can mean two different things.

### Economic replication

A strategy reproduces when successful variants attract more capital, are imitated by other agents, or survive while competitors lose wealth. If `x_i` is the capital share using strategy `i` and `f_i` its net payoff, replicator dynamics take the schematic form:

`dx_i/dt = x_i (f_i - average_fitness)`.

Evolutionary finance and wealth-driven strategy selection already study this mechanism ([wealth-driven selection](https://doi.org/10.1016/j.jebo.2009.11.006); [market selection](https://doi.org/10.1016/j.jmateco.2009.11.011)). It becomes empirical only with strategy classifications and capital flows. Prices alone do not identify population shares.

### Computational replication

Programs can copy, mutate, recombine, and select trading rules. Genetic programming has been used in finance for decades; a classic study found no consistent net out-of-sample excess return over buy-and-hold ([Allen and Karjalainen](https://doi.org/10.1016/S0304-405X(98)00052-X)). Recent systems use LLM-generated code and evolutionary search, so “self-improving trading agents” are also no longer new ([ProFiT](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5889762)).

The central danger is reproductive search breadth: every mutation is another implicit hypothesis. Natural selection optimizes in-sample fitness extremely well, including noise.

### Argus-safe evolutionary protocol

1. Define a small typed grammar of permissible strategy components.
2. Fix mutation, recombination, population size, generations, fitness, costs, and failure rules before search.
3. Log every evaluated genome and count the full search breadth.
4. Evolve only on a training era.
5. Select using a separate validation era with a complexity penalty.
6. Permit exactly one untouched confirmation run.
7. Compare with random search at equal evaluation budget and with simple economic baselines.
8. Require stability across random seeds; disagreement among evolutionary runs is evidence of search noise.
9. Never allow failed confirmation data to re-enter mutation.
10. Report survival, turnover, and lineage diversity—not only the winning genome.

EXP-011/012 already provide Argus's conceptual warning: broad search can make naive significance nearly certain, while untouched confirmation sharply reduces false claims. An evolutionary engine without an evaluation ledger would violate that lesson.

**Status:** valuable methodology experiment after a synthetic null calibration; not an immediate market-edge program.

## 6. Ecology of strategies

Possible mechanisms include:

- **competition:** momentum and mean-reversion capital reduce one another's opportunity;
- **predator–prey:** arbitrage capital grows when mispricing grows, then removes its own resource;
- **niches:** strategies survive in distinct horizons, assets, or volatility regimes;
- **carrying capacity:** impact and crowding reduce fitness as deployed capital increases;
- **invasion tests:** a new strategy enters an existing ecology and changes equilibrium returns;
- **extinction debt:** a strategy remains funded after its opportunity disappears because capital exits slowly.

Scholl, Calinescu, and Farmer explicitly model strategy wealth as species abundance and density-dependent returns, so the general framework is occupied ([market ecology](https://arxiv.org/abs/2009.09454)). The empirical gap is measuring abundances and interaction coefficients without labeling strategies after their outcomes.

Possible data: institutional holdings, fund style flows, futures participant categories, on-chain wallet behavior, or platform-provided player roles. PLEX order books alone are insufficient.

**Status:** strong long-run macro/quant branch; requires a new dataset family.

## 7. Immune systems and anomaly detection

The useful immune-system analogy is not “detect unusual prices.” It is adaptive detection under changing self/non-self distributions, memory, false positives, and adversarial evasion. Finance already has change-point detection, conformal methods, robust statistics, and adversarial learning, so an immune label adds nothing by itself.

A valid project could compare an immune-inspired detector with conformal, robust covariance, and Bayesian change-point baselines under controlled contamination and regime drift. Score detection delay, false alarms, calibration, and recovery—not returns.

**Status:** useful engineering research, low direct economic novelty.

## 8. Epidemiology and contagion

Assets, narratives, or liquidity shocks may spread through observed networks. SIR-style models require susceptible, infected, and recovered states with credible transition observations. Price correlation is not infection.

Potential data include timestamped holdings, social repost networks, payment networks, or cross-market liquidations. For digital assets, on-chain transaction graphs may fit better than closed-platform price panels. Network Hawkes models may be more appropriate when event times are observed.

**Status:** promising separate data program; not identified in current PLEX snapshots.

## Ranked roadmap

| Rank | Program | Why it survives | Immediate next artifact |
|---:|---|---|---|
| 1 | Regional reaction–diffusion/network adjustment | Topology and quotes are observed | PLEX regional extraction + benchmark forecast design |
| 2 | Fluid continuity audit of order density | Mathematically explicit, falsifiable closure | Synthetic/order-snapshot accounting note |
| 3 | Evolutionary search under a strict confirmation budget | Directly tests self-replication without market claims | Synthetic null experiment extending EXP-011/012 |
| 4 | Ecological strategy competition | Strong mechanism and capacity relevance | Dataset scouting for strategy abundance/capital flows |
| 5 | Entropy/resilience | Feasible secondary metric | Incremental forecast test versus concentration |
| 6 | Immune anomaly detection | Clear benchmarkable engineering task | Contamination/regime simulation |
| 7 | Epidemiological contagion | Requires real network states | On-chain/network data audit |
| 8 | Turbulence/critical-transition forecasting | High false-discovery risk | Hostile replication only |

## Promotion decision

No hypothesis or experiment is registered. The PLEX extraction pipeline remains the closest claim-bearing work. The fluid-continuity and evolutionary-search ideas should first be synthetic or sandbox studies, because their measurement and search-validity questions precede market inference.

## Connections

`literature_reviews/2026-08-02-bio-physics-methods-in-finance.md` · `literature_reviews/2026-08-02-plex-global-market-novelty-audit.md` · `datasets/eve_online_market_archives_2025.md` · `successful_experiments/EXP-011-search-breadth.md` · `successful_experiments/EXP-012-untouched-confirmation.md`
