# EXP-016 — Registered design: standalone US JKP publication decay

*Registered 2026-07-18 before the standalone US return file was downloaded or any US window outcome was computed. AI-led.*

Acquire the official April 2026 JKP `[usa]_[all_factors]_[monthly]_[vw]` archive from the public data library and record its SHA-256 fingerprint. Reuse EXP-013's metadata parser without outcome-conditioned edits. Define in-sample, post-sample/pre-publication, and post-publication windows from the original sample and publication years. Require at least 12 in-sample and 12 post-publication months.

Estimate US and world-ex-US factor-fixed-effect regressions with standard errors clustered by month. For the direct geography comparison, inner-join common factor-months, form US minus world-ex-US returns, and estimate the same regression. Report significant-factor results, factor-level window means, breadth, observation flow, and security-count summaries. All returns remain in decimal units in code and are converted to percentage points in reporting.

No thresholds, metadata rules, or sample filters may change after US outcomes are computed. Any unregistered diagnostics must be labeled exploratory.

## Connections

`hypotheses/HYP-016-standalone-us-jkp-decay.md` · EXP-013 · EXP-015
