# HYP-016 — Standalone US publication decay under JKP construction

*Registered 2026-07-18 before the standalone US return file was downloaded or any US window outcome was computed. AI-led.*

## Motivation and prior evidence

EXP-013 found weak world-ex-US publication decay in JKP portfolios. EXP-014 rejected shorter history as the explanation. EXP-015 found stronger decay when US stocks entered JKP's world aggregate, but `world - world_ex_us` is not a pure US portfolio and its paired gap was imprecise. The official JKP library exposes standalone US factor portfolios under the same construction, so the clean next discriminator is an observed US series.

## Hypothesis and mechanism

If the cross-dataset gap is geographic rather than an artifact of C&Z versus JKP construction, standalone JKP US factors should exhibit economically and statistically stronger post-publication decay than the construction-matched world-ex-US factors. This is a geography prediction, not a direct arbitrage test: investor response, market structure, original-study concentration, and latent portfolio differences remain observationally entangled.

## Registered predictions

- **P1 (primary):** the US factor-fixed-effect post-publication coefficient is at most -0.15 percentage points per month with absolute month-clustered t-statistic at least 2.0.
- **P2:** US post-publication minus post-sample return is at most -0.10 percentage points per month with absolute t-statistic at least 1.65.
- **P3:** in common factor-months, the US-minus-world-ex-US post-publication coefficient is at most -0.10 percentage points per month with absolute t-statistic at least 1.65.
- **P4:** more than 60% of US factors have lower equal-window post-publication than in-sample means; both the significant-factor US coefficient and the equal-factor US-minus-world-ex-US change have negative signs.

The hypothesis survives only if all four predictions pass. The falsifier fires if P1 fails, the paired P3 coefficient is nonnegative, or the equal-factor US-minus-world-ex-US change is nonnegative.

## Alternatives and limitations

Annual publication dates create coarse event timing. Factor histories and security counts can differ by location. Original papers disproportionately study US data, so publication timing may be more meaningful for US portfolios even without post-publication trading. Returns are gross of costs, factors share securities, and month clustering does not model every cross-factor dependence. No holdings, flows, short interest, lending fees, or price impact are observed.

## Internal debate

- **Optimist:** construction-matched standalone US returns remove EXP-015's most important aggregation objection.
- **Skeptic:** a US result may merely reflect that original studies and their sample dates are US-centric.
- **Statistician:** common-factor paired inference is the binding test; aggregate coefficient differences alone are insufficient.
- **Economist:** geography can discriminate transport but cannot identify arbitrage without trading quantities.
- **Portfolio Manager:** gross long-short returns do not establish implementability, costs, or capacity.
- **ML Researcher:** thresholds are fixed before acquisition; no factor filtering may be tuned after outcomes.

## Data, difficulty, and value

Use the official April 2026 JKP public `[usa]_[all_factors]_[monthly]_[vw]` file, the already pinned aggregate file, and the pinned factor-details workbook. Difficulty is low-to-moderate; novelty is moderate; expected failure probability is 45%; publication value is low alone; practical value is low; learning value is high because it distinguishes direct location measurement from aggregate differencing.

## Connections

`experiments/EXP-016-standalone-us-jkp-decay/design.md` · HYP-013 · HYP-014 · HYP-015 · Jensen, Kelly, and Pedersen (2023)
