# Foundations Curriculum — Phase 1

*Created 2026-07-09. Chosen by the researcher over immediate replication: build the base first.*

**Starting point (self-reported):** solid undergrad core — comfortable with calculus, linear algebra, probability; limited exposure to econometrics and time series.

**Destination:** the ability to read an empirical asset-pricing paper and (a) follow its statistics without skipping equations, (b) name the assumptions the authors did not state, (c) design the robustness check they should have run.

**Design principle (mentor mode):** every module is *exercise-first*. Attempt the exercises before reading the solutions or asking Argus. The reading list supports the exercises, not the other way around. A module is complete only when its mastery check passes and a `learning_notes/` entry exists in the researcher's own words.

**Pacing:** modules are ordered, not scheduled. Expect roughly 1–2 weeks each at consistent effort. Rushing defeats the purpose; the scorecard tracks mastery, not speed.

---

## Module 1 — Probability, aimed at prediction

Undergrad probability teaches distributions; research requires *conditional expectation as the object of prediction*. This module re-aims what you already know.

**Key ideas:** conditional expectation E[Y|X] as the best L² predictor; the law of iterated expectations (the single most-used identity in empirical finance); why the CLT's assumptions (independence, finite variance) are exactly the ones financial returns violate; heavy tails and when moments fail to exist.

**Reading:** Blitzstein & Hwang, *Introduction to Probability* (free online), ch. 9 (conditional expectation) and ch. 10 (inequalities & limit theorems). Skim earlier chapters only where the exercises expose gaps.

**Exercises (attempt before reading):**
1. Prove that E[Y|X] minimizes E[(Y − g(X))²] over all functions g. What does this say about what a "forecast" is?
2. Simulate 10,000 draws from a Student-t with ν = 2.5 and from a normal matched to the same scale. Compare the behavior of the sample mean and sample variance as n grows. What breaks, and why does ν matter?
3. Daily S&P 500 returns have kurtosis far above 3. List three distinct mechanisms that could generate that (hint: one involves mixtures, one involves dependence, one involves genuine jumps). This question returns in Module 5.

**Mastery check:** explain to Argus, without notes, why E[E[Y|X]] = E[Y] and give one example where a naive analyst uses unconditional moments when conditional ones were required.

## Module 2 — Statistical inference and the multiple-testing trap

The core skill of a quant researcher is knowing when a number is *distinguishable from luck*. This module is the heart of Phase 1.

**Key ideas:** sampling distributions; bias–variance; MLE; what a p-value is and is not; power; the bootstrap; and the finance-specific catastrophe — multiple hypothesis testing. Thousands of researchers mining the same data means the 5% threshold is meaningless; this is why most published anomalies are suspect.

**Reading:** Blitzstein for review as needed; then Harvey, Liu & Zhu (2016), *"…and the Cross-Section of Expected Returns"* (free on SSRN) — read it after exercise 3, not before.

**Exercises:**
1. Simulate 1,000 random "strategies" (pure noise returns, 60 months each). What is the best Sharpe ratio among them? How does it grow with the number of strategies tried? Derive the intuition from extreme value thinking before simulating.
2. Implement a basic bootstrap for the standard error of a Sharpe ratio. Compare with the asymptotic formula. When do they disagree?
3. *Before* reading Harvey–Liu–Zhu: you've discovered a factor with t = 2.3 in a universe where 300 factors have been published. Write down, in `ideas/`, your guess for how to adjust the evidence threshold. Then read the paper and record the gap between your prior and theirs.

**Mastery check:** given a backtest with a claimed t-statistic, articulate the three questions you must ask before believing it (search breadth, data snooping, out-of-sample), and correctly explain what a p-value conditions on.

## Module 3 — Regression as geometry, then as econometrics

OLS is the workhorse of empirical finance. Understanding it as projection makes everything downstream (factor models, betas, alpha) obvious rather than memorized.

**Key ideas:** OLS as orthogonal projection onto the column space of X; Gauss–Markov and which of its assumptions financial data violate (all the interesting ones); heteroskedasticity and autocorrelation; robust (White) and HAC (Newey–West) standard errors — *why* they exist, not just when to click them; omitted variable bias as the reason "alpha" claims usually die.

**Reading:** Cochrane's free lecture notes on regression/time series for finance; Wooldridge, *Introductory Econometrics*, ch. 2–5, 8, 12 as reference.

**Exercises:**
1. Derive the OLS estimator by projection (no calculus — pure linear algebra). Then show residuals are orthogonal to fitted values, and explain what R² means geometrically.
2. Simulate a regression where errors are autocorrelated (AR(1), ρ = 0.9). Compare naive OLS standard errors to Newey–West across 1,000 replications. How wrong are the naive t-stats? This is the overlapping-returns problem in disguise.
3. Take a made-up "signal" that is truly useless but correlated with market beta. Show that regressing returns on the signal alone produces significant "alpha," which disappears when beta is controlled. Write up the mechanism.

**Mastery check:** explain omitted variable bias with the formula, and state exactly what CAPM regression alpha measures and under what assumptions it means anything.

## Module 4 — Time series

The dimension undergrad stats skips and finance lives in.

**Key ideas:** stationarity (strict vs. weak, and why it's an *assumption about the world*, not a test result); autocorrelation and the ACF; AR/MA processes; unit roots and spurious regression (regressing one random walk on another gives significant nonsense — the classic Granger–Newbold result); volatility clustering and a first look at ARCH/GARCH.

**Reading:** Hyndman & Athanasopoulos, *Forecasting: Principles and Practice* (free online) for mechanics; Cochrane's time-series notes for the finance angle; Tsay, *Analysis of Financial Time Series*, ch. 2–3 as reference.

**Exercises:**
1. Simulate two independent random walks, regress one on the other, repeat 1,000 times. Plot the distribution of t-statistics. Explain why standard inference collapses.
2. Fit an AR(1) to daily returns and to daily *squared* returns of an index (free data). What do the two very different autocorrelations tell you about markets? (This is the deepest single fact in empirical finance.)
3. Take any published "signal predicts returns" claim; identify whether the predictor is highly persistent and what the Stambaugh bias implies for its t-statistic. Guess first, then look up Stambaugh (1999).

**Mastery check:** state the difference between a trend-stationary and unit-root process, why it matters for prediction, and describe volatility clustering with the evidence from exercise 2.

## Module 5 — Capstone: the stylized facts of asset returns

Foundations end with real data and a real research artifact. Target: independently reproduce the stylized facts catalogued in Cont (2001), *"Empirical properties of asset returns: stylized facts and statistical issues."*

**Task:** using free data (an index plus a handful of single names, documented in `datasets/`), verify or challenge: heavy tails, absence of linear autocorrelation, volatility clustering, aggregational Gaussianity, leverage effect. Every figure reproducible from a script. Every claim with a statistic and its uncertainty. Written up under `replications/` as the first entry.

**Why this capstone:** it exercises every module — tail behavior (M1), inference on the statistics (M2), regression for the leverage effect (M3), ACF machinery (M4) — and it produces the repository's first real research document without requiring a novel hypothesis.

**Mastery check:** the write-up itself, plus one paragraph on which stylized fact has the *weakest* statistical support in your own analysis and why.

---

## Rules of engagement for this phase

1. **Attempt before asking.** Argus answers questions with questions first when the struggle is productive.
2. **Write to learn.** Each module ends with a `learning_notes/` entry in the researcher's own words — explaining is the mastery test.
3. **Update the scorecard** after each module: move the topic's level only when the mastery check passes.
4. **Log surprises.** Any time reality disagrees with your prior (exercises 2.3, 4.3 are designed for this), record it — those gaps are the measurement of learning.
5. **Environment:** Python, one repo-level virtualenv, every exercise a runnable script under `learning_notes/exercises/`, seeds fixed.

## Connections

- Feeds: `researcher_scorecard.md` (mastery levels), `replications/` (capstone), `papers/` (Harvey–Liu–Zhu, Stambaugh 1999, Cont 2001 notes)
- Successor: Phase 2 — landmark replication with WRDS/CRSP data (momentum or size/value), where survivorship bias and delisting returns become real.
