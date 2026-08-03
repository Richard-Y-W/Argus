# EXP-027 — Registered design: environmental-distance gate

**Registered:** 2026-08-03 before execution  
**Stage:** synthetic methods confirmation  
**Attribution:** Collaborative

## Inherited specification

The experiment reuses EXP-025's five-gene genome, prior, mutation kernel, phenotype, fitness, transaction cost, population size, 48-candidate budget, 126-day fitness window, and 21-day causal adaptation schedule. It reuses EXP-026's quality-only 36-descendant/12-immigrant hybrid. No phenotype-diversity reserve is used because EXP-026 rejected that intervention.

Pre-change observations are days 0–251. The structural change occurs at day 252, and days 252–503 are scored while adaptation continues. Confirmation uses four new families with six independent seeds each:

- `small_drift`: 50,000–50,005;
- `moderate_rotation`: 60,000–60,005;
- `mean_reversion`: 70,000–70,005;
- `correlation_break`: 80,000–80,005.

The small family modestly changes means, persistence, and volatility; moderate rotates leadership; mean reversion makes all AR coefficients negative; correlation break additionally turns the first two assets strongly positively correlated and reorders volatility.

## Observable distance

At each adaptation date, compare the most recent 63 observations available with the fixed pre-change reference window, days 126–251. At day 252 both windows are pre-change; detection is necessarily delayed.

Create twelve standardized components:

1. three mean differences divided by their reference-based standard errors;
2. three log-volatility differences divided by the Gaussian log-volatility standard error;
3. three Fisher-z correlation differences divided by their two-window standard error;
4. three AR(1) coefficient differences divided by `sqrt((1-phi_ref^2)/n_recent + (1-phi_ref^2)/n_reference)`.

Distance is the root mean square of the twelve finite component z-scores. The gate chooses local mutation below 1.25, the fixed hybrid from 1.25 to below 2.50, and global restart at 2.50 or above. Thresholds receive no calibration on market outcomes or confirmation families.

## Equal-budget methods

- `evolution`: 48 local descendants;
- `random`: 48 global-prior candidates;
- `hybrid`: 36 descendants and 12 immigrants;
- `gate`: generation rule selected by the lagged distance score.

All methods evaluate 48 new candidates plus 12 incumbents at every adaptation. All retain the top 12 by the unchanged trailing fitness rule. Separate deterministic RNG streams prevent candidate sharing.

## Outcomes and inference

- 252-day cumulative net log return;
- first-126-day cumulative net log return;
- annualized volatility, historical 5% expected shortfall, and one-way turnover;
- route shares and mean detected distance by family;
- candidate count.

P1–P3 use 10,000 family-stratified paired-bootstrap resamples. P4 uses raw family mean global-route shares with strict ordering. P5 uses family-balanced method mean expected shortfall. The joint claim requires P1–P5.

## Audit

Tests must cover causal distance, finite distance under constant columns, threshold routing, deterministic distinct families, hybrid composition, and equal candidate counts. No threshold, window, feature, family, or endpoint change is allowed after execution.

## Connections

`hypotheses/HYP-027-regulated-evolvability.md` · EXP-025 · EXP-026

