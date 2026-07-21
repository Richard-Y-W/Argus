# HYP-017 — US publication decay survives dependence-aware inference

*Registered 2026-07-21 before computing two-way-clustered results. AI-led.*

## Motivation and prediction

EXP-016 clustered standard errors by month, accounting for common shocks but not persistent within-factor dependence. If its US result is not an artifact of that choice, the post-publication level and the post-sample-to-post-publication contrast should survive Cameron–Gelbach–Miller two-way clustering by factor and month.

P1: post-publication decay is at most -0.10 percentage points per month with |t| >= 2.0. P2: post-publication minus post-sample is at most -0.10 pp/month with |t| >= 2.0. The hypothesis survives only if both pass. A non-negative coefficient or |t| < 1.65 on either quantity is a falsifier.

## Alternatives and limits

Failure may reflect dependence-aware uncertainty rather than absence of decay. Survival would strengthen inference about the return pattern, not establish publication arbitrage, causality, or tradability.

## Data, difficulty, and value

Pinned April 2026 JKP standalone US value-weighted monthly factors and the existing metadata parser; moderate statistical difficulty, low data difficulty, moderate novelty, high learning value, low practical value.

## Internal debate

- **Optimist:** the large EXP-016 coefficient should survive.
- **Skeptic:** repeated observations per factor made month-only inference optimistic.
- **Statistician:** use the identical eligible panel and point estimator; change only covariance estimation.
- **Economist:** robust inference still does not identify a trading mechanism.
- **Portfolio manager:** gross factor returns remain far from an implementable portfolio.
- **ML researcher:** no tuning or model selection is permitted.

## Connections

EXP-016 · `experiments/EXP-017-dependence-aware-us-decay/design.md`
