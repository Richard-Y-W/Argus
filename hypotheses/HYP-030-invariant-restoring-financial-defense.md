# HYP-030 — Invariant-restoring financial defense

**Status:** registered 2026-08-05 before execution  
**Attribution:** Collaborative

## Question

When leverage or liquidity health approaches a breach, can a targeted defense identify the largest observable contributor and restore the invariant with less damage to healthy modules than system-wide controls?

## Mechanism

This is the first direct defense test:

`health invariant -> danger signal -> contributor isolation -> bounded intervention -> recovery`

The controller observes no pathology label. It ranks modules using current exposure, stressed funding-outflow contribution, and trailing loss contribution, then reduces the highest score only until both buffers are restored. This corresponds to local containment, not return-seeking mutation.

## Alternatives

- Systemic shocks make targeted isolation inadequate.
- Contribution scores misidentify causes.
- Early intervention creates false alarms and needless losses.
- Proportional deleveraging or liquidation restores health more reliably.
- The simulator mechanically favors the proposed controller.

## Internal debate

- **Optimist:** explicit invariants finally match the original defense idea.
- **Skeptic:** a hand-built simulator can encode the desired answer; hostile systemic and benign families are essential.
- **Statistician:** compare paired seeds within pathology families and require family breadth.
- **Economist:** simplified balance-sheet mechanics cannot establish real institutional behavior.
- **Portfolio manager:** liquidation, proportional deleveraging, volatility targeting, and no action are required baselines.
- **ML researcher:** the controller cannot access hidden labels and all thresholds must be frozen.

## Connections

`experiments/EXP-030-invariant-restoring-defense/design.md` · EXP-029 · `literature_reviews/2026-08-05-financial-health-invariants.md`

