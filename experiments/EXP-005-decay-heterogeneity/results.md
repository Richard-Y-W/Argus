# EXP-005 — Results: which predictors decay?

*Run 2026-07-12 on the registered design (`design.md`, committed before analysis). Data: Chen & Zimmermann Oct 2025 (pinned, `datasets/chen_zimmermann_oct2025.md`). Code: `analysis.py` (registered), `posthoc_scale_check.py` (labeled post-hoc). Log: `results/run_log.txt`.*

**Verdict: HYP-005 rejected.** The registered interactions are individually "significant," but a labeled post-hoc diagnostic shows they are all one thing in disguise: decay is proportional to a predictor's in-sample mean — a roughly constant ~50% haircut — and neither original-paper t-stat nor strategy volatility carries any information about decay beyond its correlation with that scale. The lab's first entry in `failed_experiments/`, and the most instructive result so far.

## Sample

188 predictors with non-missing original-paper t-stat (24 of 212 excluded; their window means are in `results/excluded_missing_op_t.csv`), 121,977 predictor-months, windows and filters identical to EXP-001/003.

## Registered results

**E1 (primary, joint):** on top of the baseline decline (β_pp = −0.379, t = −6.6):

| Interaction | coef (%/mo per 1 sd) | t |
|---|---|---|
| post-pub × OP t-stat | −0.151 | −5.15 |
| post-pub × log volatility | −0.153 | −3.20 |
| post-pub × log citations (E3) | +0.050 | +1.70 |

**E2 (terciles of OP t-stat):** in-sample → post-publication means: bottom 0.50 → 0.25, middle 0.60 → 0.31, top 0.88 → 0.39 %/mo. Absolute declines 0.25 / 0.29 / 0.48 — top ≈ 1.95× bottom. **But in proportional terms the terciles are flat: 50% / 49% / 55% of the in-sample mean survives-to-dies at nearly the same rate everywhere.** The same pattern holds for volatility terciles (61% / 49% / 52% declines proportionally).

**Predictions scored (registered decision rules):**

- **P1 ✓ as registered** — pp × OP-t = −0.151 ∈ [−0.30, −0.05], |t| = 5.1 ≥ 2; tercile ratio 1.95 ≥ 1.5. *Interpretation overturned by the post-hoc below: the test passed, the mechanism reading did not.* A registered prediction can pass because the spec was mis-aimed, not because the hypothesis is right.
- **P2 ✗** — pp × vol = −0.153 with |t| = 3.2, below the registered failure line (−0.15, |t| ≥ 2) — by 0.003, but a rule that only binds when convenient is not a rule. The point prediction (positive, Pontiff arbitrage-cost sign) was wrong in direction.
- **P3 ✗** — pp × cites is *positive* (+0.050, t = 1.70): more-cited predictors decay less, if anything. Direction bet lost. Post-treatment caveat applies in both directions (durable factors may earn citations *because* they endure).
- **P4** — not triggered (interactions were nonzero).

**Robustness (all registered, all run):** the E1 interactions survive era controls (R1), a publication-year cohort control (R2), winsorization (R4), and the 1_clear subsample (R5) essentially unchanged. R3 is the tell: replacing OP t-stat with the *realized* in-sample t strengthens the interaction (−0.201 vs −0.151, t = −7.2) — the closer the sorting variable sits to the realized in-sample mean, the stronger the "effect." That ordering is what a scale/shrinkage account predicts and what a capital-chases-published-evidence account does not.

## Post-hoc diagnostic (NOT registered — labeled exploratory)

Motivated by the flat proportional terciles in the registered E2 output. Adding (ps, pp) × z(in-sample mean) to E1 (`posthoc_scale_check.py`):

| Interaction | coef | t |
|---|---|---|
| post-pub × in-sample mean | **−0.247** | **−5.23** |
| post-pub × OP t-stat | −0.018 | −0.55 |
| post-pub × log volatility | −0.006 | −0.13 |

One regressor annihilates both registered interactions. The correlations doing the smuggling: corr(in-sample mean, OP t) = 0.39, corr(in-sample mean, log vol) = 0.48. Cross-sectionally, in-sample mean = 0.68 %/mo (sd 0.47) and mean absolute decline = 0.41 %/mo — the panel is consistent with "publication costs a predictor about half of whatever it had, regardless of what kind of predictor it is."

## What this does and does not establish

- **Established:** heterogeneity in *absolute* decay exists and is fully accounted for by in-sample scale under this design. No residual role for published t-stat, strategy volatility, or citations.
- **Not separable here:** *why* decay is proportional. Two candidates remain observationally equivalent in this design: (a) proportional arbitrage correction — capital consumes a roughly constant fraction of any revealed edge; (b) shrinkage — measured in-sample means contain luck proportional to their size, and the luck reverts. The pp × is_mean regressor is mechanically exposed to (b), so its coefficient cannot arbitrate. Tension worth recording: EXP-002's P4 found that screening *placebos* on in-sample mean does **not** manufacture decay, which argues against pure selection-on-mean shrinkage — but placebos lack genuine signal dispersion, so the transfer is imperfect. Separating (a) from (b) needs a design where expected luck and expected edge move independently — e.g., sorting on sample length (luck shrinks with √n; the edge doesn't).
- **One surviving hint of an implementability effect (descriptive only, n = 28):** value-weighted predictor portfolios lose ~94% of their in-sample mean post-publication vs ~55% for equal-weighted — the large-cap, actually-tradeable versions get corrected nearly fully. Unregistered, composition-confounded, but it points the same way as M&P's cost results and deserves its own registered test on C&Z's alternative-ports files.

## Five-minute digest for the researcher

We asked *which* anomalies die after publication — the strong ones? the cheap-to-trade ones? the famous ones? We ran the interactions and got beautiful t-stats: strong signals decay more (t = −5!), volatile ones decay more (t = −3!). Then one diagnostic ruined everything, and that ruin is the lesson: once you control for *how big the signal was in-sample*, nothing else matters. Publication takes roughly the same bite — about half — out of everything. Big signals lose more per month for the same reason expensive houses lose more dollars in a crash: they had more to lose, not because arbitrageurs target them specially.

Two ideas to sit with. First: an interaction term in a *levels* regression confounds "this characteristic changes the decay *rate*" with "this characteristic correlates with the signal's *size*." Our registered P1 passed its test and was still wrong as a mechanism claim. Registration keeps you honest about *what you predicted*; it cannot save a mis-aimed specification. Second: **post-treatment bias** — we used 2025 citation counts to explain decay that happened decades earlier. If durable anomalies collect citations, causality runs backward through our regressor. That's why P3 was fenced as exploratory, and its failure costs the thread nothing.

Argus's scorecard this cycle: one registered pass that didn't deserve its interpretation, two clean fails — again by over-predicting how visibly a mechanism would show up. The pattern now spans three experiments; treat any Argus mechanism prediction as optimistic until the diagnostic runs.

**Your prediction question (answer before looking at anything in EXP-004):** EXP-005 says a predictor's post-publication fate is a roughly constant fraction of its in-sample mean. A placebo has *no in-sample edge by construction* — so scale predicts its decay should be near zero, and any real drift has to come from somewhere else (your spillover story is the leading candidate). Commit to two numbers for the worksheet, section 1: the post-publication drift, in %/mo, of (a) the third of placebos *most* correlated with published predictors, and (b) the *least* correlated third. If your numbers for (a) and (b) are the same, you don't believe in spillover — say that instead. The worksheet is still the gate for EXP-004; nothing runs until sections 1–5 are yours.

## What remains unknown

- Proportional-arbitrage vs shrinkage decomposition (sample-length sort is the candidate design).
- The VW/EW near-full-correction hint (needs C&Z alt ports, registered).
- Whether the ~50% haircut is stable across publication decades (interacts with EXP-003's era machinery).
- Everything about placebo spillover — reserved for the researcher (EXP-004).

## Connections

`hypotheses/HYP-005-decay-heterogeneity.md` (rejected) · `failed_experiments/EXP-005-decay-heterogeneity.md` (summary of record) · EXP-001 (baseline), EXP-002 (P4 tension on shrinkage), EXP-003 (era controls reused) · `papers/2016-mclean-pontiff-does-academic-research-destroy-predictability.md` (their Tables 5–6 heterogeneity now looks scale-confounded too — worth a re-read with this lens) · feeds `experiments/EXP-004-placebo-spillover/` · `knowledge_graph/anomaly-decay-thread.md`
