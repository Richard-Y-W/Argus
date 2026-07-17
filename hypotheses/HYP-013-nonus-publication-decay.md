# HYP-013 — Publication decay appears outside the United States

*Registered 2026-07-16 before publication-window outcomes were computed. AI-led.*

## Motivation and prior

EXP-001–003 establish a publication-timed decline in the US Chen–Zimmermann panel, but one market and one data family cannot distinguish a general publication effect from US-specific construction or market history. Jensen, Kelly, and Pedersen (2023) provide standardized, signed factor returns across 93 countries. If published knowledge prompts broad learning or arbitrage, factors should also weaken after publication in the world-ex-US aggregate.

## Registered predictions

- **P1 primary:** in `world_ex_us`, the factor-fixed-effect post-publication coefficient relative to the original in-sample window is at most -0.10 percentage points per month and has a month-clustered |t| of at least 2.0.
- **P2 two-stage pattern:** the post-sample/pre-publication coefficient is negative, and the post-publication coefficient is at least 0.05 percentage points more negative than the post-sample coefficient; the post-publication-minus-post-sample contrast has |t| at least 1.65.
- **P3 regional breadth:** the post-publication coefficient is negative in both `developed` and `emerging`; at least one region has |t| at least 2.0.
- **P4 factor breadth:** more than 55% of eligible world-ex-US factors have a lower post-publication mean than in-sample mean.
- **P5 robustness:** P1 remains negative when restricting metadata to factors marked significant in the source workbook and when equal-weighting factor window means in a factor-level regression.
- **Falsifier:** P1 misses either its magnitude or inference rule, or reverses sign in either registered P5 robustness sample.

## Data, alternatives, and risk

Use the JKP April 2026 public release, downloaded 2026-07-16, monthly value-weighted signed factor returns through 2025-12. Primary location is `world_ex_us`; `developed` and `emerging` are registered robustness locations. Map `name` to `abr_jkp`, parse original sample start/end from `in-sample period`, and publication year from the final four-digit year in `cite`. Require nonmissing dates, at least 12 observations in both in-sample and post-publication windows, and no pre-sample observations. Empty post-sample windows are allowed.

Alternative explanations include international diffusion of US discoveries, common global shocks, changing country coverage, standardized reconstruction effects, factor dependence, risk-premium changes, and data mining. Expected failure probability: 45%. Novelty is moderate; learning and external-validity value are high; direct arbitrage identification and practical value remain low.

## Internal debate

- **Optimist:** a non-US data family is the cleanest available test of whether the US result travels.
- **Skeptic:** `world_ex_us` is not untreated; globally traded firms and investors transmit US publication effects.
- **Statistician:** keep one primary location, cluster by month, expose factor breadth, and add a factor-level robustness so long histories do not dominate.
- **Economist:** a replicated event-time decline would strengthen generality, not prove arbitrage causality.
- **Portfolio manager:** public aggregate returns are gross and reveal neither capacity nor executable costs.
- **ML researcher:** factor mapping, years, thresholds, windows, and regional splits must be fixed before outcome calculation.

The hypothesis survives internal debate as an external-validity test with explicitly bounded mechanism language.

## Connections

`experiments/EXP-013-nonus-publication-decay/design.md` · `papers/2023-jensen-kelly-pedersen-replication-crisis.md` · EXP-001 · EXP-003
