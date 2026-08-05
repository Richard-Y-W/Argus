# Financial health invariants for immune-style defense

The Basel framework treats leverage and liquidity as constraints on system resilience rather than return objectives. Its leverage ratio is a non-risk-based backstop intended to restrict leverage accumulation and destabilizing deleveraging. Its liquidity coverage ratio compares high-quality liquid assets with stressed net cash outflows and is intended to protect short-term liquidity resilience.

EXP-030 borrows only this invariant logic. It is not a regulatory-capital model and does not claim Basel compliance. The synthetic system defines gross exposure/equity no greater than 3 and liquid buffer/projected stressed outflows no less than 1. These round thresholds make damage, recovery, and collateral intervention observable.

The immune analogy is narrower than artificial immune anomaly detection. A detector is useful only if its response restores an invariant with less damage to healthy modules than conventional system-wide controls.

## Primary sources

- Basel Committee on Banking Supervision, consolidated Basel Framework, LEV leverage ratio and LCR liquidity coverage ratio.
- Matzinger, P. (1994), *Tolerance, Danger, and the Extended Family*.

## Connections

`hypotheses/HYP-030-invariant-restoring-financial-defense.md` · EXP-029

