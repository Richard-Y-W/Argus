# EXP-010 — Registered design: within-signal EW/VW decay

*Registered 2026-07-15 before analysis. AI-led.*

## Sample and construction

Use the official October 2025 `deciles_ew.parquet` and `deciles_vw.parquet` LS rows through 2024-12. Join predictor metadata restricted to `1_clear` or `2_likely`. Assign annual event windows with the canonical Argus rule: sample-start year through sample-end year is in-sample; the following years through publication year are post-sample; later years are post-publication. Exclude pre-sample observations.

Pair EW and VW by signal and month before summarizing, so both implementations use identical dates. Require at least 12 common observations in the in-sample and post-publication windows and require both in-sample means above 0.10% per month. No direction is selected from realized performance: official LS rows preserve the source portfolio's signed direction.

## Estimands and decision rules

For each weighting, proportional decay is `(in-sample mean - post-publication mean) / in-sample mean`. The primary observation is the within-signal difference `decay_vw - decay_ew`; report its mean, conventional paired t-statistic, 95% t interval, median, and positive share. P1 requires mean >= 0.10 and t >= 2.0. P2 uses the paired levels difference-in-differences and requires a negative coefficient with |t| >= 2.0. P3 requires a primary-difference positive share above 55%.

Registered robustness checks are 5/95 winsorization of the primary paired difference and restriction to `1_clear` signals. Both must remain positive for P4. Report unfiltered eligibility counts and all signal-level inputs. Tests are cross-sectional across signals; no claim of causal identification is permitted.

## Bias and scope controls

The panel end, thresholds, windows, and tests are fixed before execution. Pairing prevents between-signal composition confounding but does not remove within-signal stock-universe composition, exposure-strength, microstructure, or cost differences. Returns are gross of costs; annual publication dates induce boundary noise; signals are not guaranteed independent. No walk-forward validation is relevant because this tests a historical event pattern, not a forecasting model. No multiple-testing adjustment is used because P1 is the sole primary test; secondary outcomes are explicitly labeled.

## Outputs

`analysis.py` deterministically writes `results/paired_signals.csv`, `results/summary.csv`, `results/sample_flow.csv`, and `results/run_log.txt`.

## Connections

`hypotheses/HYP-010-within-signal-weighting-decay.md` · EXP-009 · EXP-001 · Chen–Zimmermann October 2025 alternative portfolios
