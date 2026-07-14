# HYP-007 — Is the proportional publication haircut stable across cohorts?

*Registered 2026-07-14, before analysis. Attribution: AI-led.*

## Motivation

EXP-003 found that publication event time dominates calendar time; EXP-005 found an approximately 50% proportional haircut. A stable mechanism should reproduce across publication cohorts. A changing haircut would weaken the claim that there is one publication-decay parameter and could expose changes in dissemination or arbitrage capacity.

## Hypothesis and alternatives

The proportional haircut strengthens for newer cohorts because dissemination and quantitative arbitrage became faster and cheaper. Alternatives are a stable fraction, weaker modern decay, or mechanical truncation because recent publications have shorter post-publication windows.

## Registered predictions

- **P1:** In a predictor-level regression of proportional decay `(in_sample - post_pub) / in_sample` on publication year, the slope is positive with |t| >= 2 after controlling for log post-publication months and in-sample mean; primary denominator floor is in-sample mean > 0.10.
- **P2:** The newest cohort (publication 2001+) has at least 10 percentage points more proportional decay than the oldest cohort (through 1989).
- **P3:** The publication-year slope remains positive in both a 5/95 winsorized outcome and the clear-reproduction subsample.
- **Falsifier:** A nonsignificant primary slope and a newest-minus-oldest difference inside ±10 points reject the strengthening claim.

## Cohorts

Registered bins: publication <=1989, 1990–2000, and 2001+. Bins are chosen ex ante for usable counts and to isolate the post-decimalization/dissemination era, not after viewing returns.

## Data and value

Same pinned panel. Difficulty low, novelty modest, expected failure probability 50%, practical value low, learning value high. The main threat is unequal post-publication horizon; log months is therefore mandatory.

## Connections

`experiments/EXP-007-cohort-haircut/design.md` · EXP-003 · EXP-005
