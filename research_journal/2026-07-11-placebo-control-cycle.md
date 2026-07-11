# 2026-07-11 — The control group the literature forgot (EXP-002)

The researcher asked for two cycles today (he missed a day; the lab did not). This entry covers the first.

EXP-001 left an obvious hole: everything in the three-window design decays *in recent decades*, and post-publication windows live in recent decades. Without a control group, "publication causes decay" and "recent decades are hostile to characteristic spreads" are observationally similar. Chen & Zimmermann quietly ship the control group: 114 placebo characteristics — published in the same journals over the same decades, reproduced with the same machinery, but never claimed as return predictors. Remarkably little published work uses them this way.

Mechanics worth recording: the `openassetpricing` package does not expose the placebo portfolios; we pulled `PlaceboPortsFull.csv` straight from the release's Drive folder and cached it (provenance updated). Before registering, we checked one thing only — the signing convention — because the whole design collapses if C&Z sign placebos by in-sample performance. They don't (68% positive in-sample vs ~98% for predictors; the explicitly-rejected `4_not` group sits at 0.06%/mo). That check is disclosed in the design doc, and post-sample quantities stayed unseen until after registration was committed.

Results: placebos simply do not show the pattern. Post-sample change +0.08 (t = 1.2) — nothing; post-publication −0.11 (t = −2.6) — small drift; predictors' extra decline over placebos: −0.33 post-sample, −0.26 post-publication, both t ≈ 3. The M&P causal story survives its sharpest cheap falsification test.

Two things matter more than the passes:

1. **P4 failed.** I registered a side-prediction that screening placebos on positive in-sample mean would *manufacture* post-sample decay (selection bias, demonstrated). It didn't budge (−0.03, t = −0.5). The post-mortem explanation — long-sample means have too little sampling error for a sign screen to select noise — was formed after the fact and is labeled as such. A failed prediction inside a successful experiment is exactly the kind of thing the charter says to keep at full resolution.
2. **The placebo drift (−0.11) is the confound's upper bound, and it is not zero.** Spillover from correlated true predictors, or a common calendar trend — indistinguishable here. This converts EXP-003 (calendar vs event time) from "candidate" to "mandatory," and the second cycle of the day runs it.

The researcher hadn't answered the EXP-002 design question before this ran; the design reasoning is recorded so he can diff his instinct against it. His digest question this cycle: what evidence separates spillover from calendar-time trend. That is EXP-003's identification problem, stated in his terms.
