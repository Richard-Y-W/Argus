# Exploratory question: can regime selection rescue noise?

Practitioners often add a volatility/trend “regime filter” after a base strategy disappoints. On synthetic independent returns with no signal, select the best of 50 random regime masks in-sample and measure its untouched out-of-sample mean. This calibrates the research process; it is not market evidence.

## Result

Across 1,000 simulations, selected in-sample mean was +0.0997 standard deviations per period and positive in 98.1% of runs. Untouched test mean was −0.0021 and positive in 49.2%. Searching only 50 meaningless filters manufactures an apparently successful regime almost every time and produces no persistence. Output: `output.csv`.
