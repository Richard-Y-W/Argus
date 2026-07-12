# EXP-005 — Which predictors decay? (hypothesis rejected)

*Completed 2026-07-12. Full materials: `experiments/EXP-005-decay-heterogeneity/`. First entry in this directory.*

**One line:** post-publication decay is a roughly constant ~50% haircut on whatever a predictor earned in-sample — the "significant" interactions with original-paper t-stat (−0.151, t = −5.1) and strategy volatility (−0.153, t = −3.2) both collapse to zero (t = −0.55, −0.13) once decay is allowed to scale with the in-sample mean (−0.247, t = −5.2). No characteristic-specific decay mechanism survives.

**Filed as failed:** HYP-005's claim was that decay concentrates in strong, cheap-to-arbitrage signals. P1 passed its registered decision rule but only as a proxy for in-sample scale (the labeled post-hoc overturned the interpretation); P2 failed at its registered boundary with the *opposite* sign to the Pontiff arbitrage-cost prediction; P3 (citations → decay) failed in direction. The rejection is the finding: publication seems to tax every signal at close to the same proportional rate.

**What the failure bought:** (1) a specification lesson of record — levels-interactions confound rate with scale, and a registered pass is not a mechanism; (2) a sharpened follow-up menu — sample-length sorts to split proportional-arbitrage from shrinkage, and a registered VW/EW test of the near-full correction seen descriptively in value-weighted ports (94% vs 55%, n = 28, unregistered); (3) a cleaner scaffold for EXP-004 — placebos have no in-sample edge, so scale predicts ~zero placebo decay, making any correlated-placebo drift cleanly attributable to spillover if Richard's test finds it.

**Caveats that travel with the result:** the scale diagnostic was post-hoc (labeled, single regressor, no specification search); the pp × in-sample-mean coefficient is mechanically exposed to luck-reversion, so it cannot itself separate arbitrage from shrinkage; gross of costs; 188/212 predictors (OP t-stat availability filter, excluded set documented).
