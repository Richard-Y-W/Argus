# HYP-019 — US publication decay survives portfolio-breadth controls

*Registered 2026-07-21 before computing breadth-adjusted outcomes. AI-led.*

## Motivation and prediction

The standalone JKP US file reports monthly stock counts. Expanding coverage can alter factor composition around publication and masquerade as decay. If composition is not the primary explanation, controlling flexibly for within-factor log stock-count changes should not erase the post-publication coefficient.

P1: with factor fixed effects, window indicators, and within-factor demeaned log stock count, post-publication decay is at most -0.10 pp/month with |t| >= 2.0. P2: adding the control attenuates the absolute frozen EXP-016 coefficient by less than 25%. P3: adding interactions between log breadth and both post-sample windows leaves post-publication decay negative with |t| >= 1.65 at each factor's mean breadth. Survival requires all three. A non-negative adjusted coefficient is a falsifier.

## Alternatives and limits

Stock count is a composition proxy, not turnover, holdings, flows, short interest, or price impact. It may be endogenous to data coverage. Survival rules out only a simple breadth explanation.

## Data, debate, and value

Pinned JKP US monthly value-weighted factors; low data difficulty, moderate confounding risk and learning value. The Optimist expects the decay coefficient to persist; the Skeptic expects secular coverage growth to absorb it; the Statistician requires within-factor centering and month clustering; the Economist rejects a causal reading; the Portfolio Manager notes no cost data; the ML Researcher prohibits nonlinear searches after outcomes.

## Connections

EXP-016 · `experiments/EXP-019-portfolio-breadth-control/design.md`
