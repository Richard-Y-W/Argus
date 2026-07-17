# HYP-011 — Search breadth manufactures regime evidence under the null

*Registered 2026-07-16 before execution. AI-led.*

## Motivation and prior

The regime-filter sandbox selected the best of 50 meaningless filters and found a positive training mean in 98.1% of simulations, with no test persistence. White (2000) shows why inference after specification search must account for the search. This experiment preregisters the breadth gradient rather than another single search size.

## Registered predictions

- **P1 primary:** the mean selected training z-statistic increases strictly across search sizes `K = 1, 5, 20, 50, 200`.
- **P2 multiplicity:** the share of selected training z-statistics exceeding the one-sided 5% cutoff 1.644854 is within 0.035–0.065 at K=1 and above 0.95 at K=200.
- **P3 untouched test:** at every K, the mean independent test z-statistic has absolute value below 0.05 and its positive share lies in 0.47–0.53.
- **Falsifier:** failure of P1, or a systematic test shift outside P3's bounds.

## Data, alternatives, and risk

Generate independent standard-normal train and test z-statistics for 20,000 Monte Carlo runs at each K with seed 20260716. The null is known and all candidates have zero expected performance. The exercise does not represent autocorrelation, common strategy exposure, fat tails, adaptive search, or transaction costs. Expected failure probability is 10%; novelty and practical value are modest, while learning value is high.

## Internal debate

- **Optimist:** the gradient gives Richard a quantitative prior for how quickly search destroys naive significance.
- **Skeptic:** independent Gaussian candidates are too clean to describe real strategies.
- **Statistician:** use a known null, fixed K grid, Monte Carlo uncertainty, and an untouched test draw for the selected index.
- **Economist:** this identifies a research-process mechanism, not an economic regime mechanism.
- **Portfolio manager:** no result may be described as tradable or cost-aware.
- **ML researcher:** fixing the full grid before execution prevents choosing a visually convenient curve.

The hypothesis survives as a calibration experiment with bounded scope.

## Connections

`literature_reviews/2026-07-16-data-snooping-and-holdout-discipline.md` · `experiments/EXP-011-search-breadth/design.md` · White (2000)
