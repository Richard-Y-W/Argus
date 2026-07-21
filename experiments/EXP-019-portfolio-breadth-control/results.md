# EXP-019 — Simple portfolio breadth does not explain US decay

## Verdict

**HYP-019 survives all registered rules.** The adjusted coefficient stays negative and precise, attenuation is below 25%, and the falsifier does not fire.

## Results

All 101,920 observations have positive stock counts. Adding within-factor demeaned log stock count makes post-publication decay **-0.176 pp/month** (t = **-2.96**), a -7.1% attenuation—that is, a modest amplification relative to the frozen coefficient. Adding the registered window interactions yields **-0.180 pp/month** (t = **-2.73**) at centered breadth. The breadth main effect is +0.040 pp/month (t = 0.81), imprecise.

Median stock count rises from 2,675 in-sample to 3,393 post-sample and 3,041 post-publication. That changing composition does not absorb the window coefficient under the registered linear control.

## Adversarial review

- Stock count is a coarse composition proxy and may itself respond to coverage, listings, and data construction.
- A linear log-breadth control cannot rule out security-level composition changes or nonlinear effects.
- Counts do not measure turnover, holdings, shorting, flows, lending fees, or price impact.
- The test narrows one confounder; it does not provide direct publication-arbitrage evidence.

## Reproduction and connections

Run `python experiments/EXP-019-portfolio-breadth-control/analysis.py`. HYP-019 · EXP-016 · EXP-017 · EXP-018
