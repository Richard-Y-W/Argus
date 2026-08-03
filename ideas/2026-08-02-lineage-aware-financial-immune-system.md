# Lineage-aware financial immune system

**Stage:** exploratory design; registration is premature  
**Attribution:** Collaborative  
**Primary objective:** system robustness, not low latency and not assumed alpha

## Question and mechanism

Can a layered controller protect a portfolio or multi-strategy fund from novel regimes and internally generated risk better than conventional controls?

The proposed mechanism has five layers:

1. **Innate layer:** nonlearned leverage, liquidity, concentration, loss, and kill-switch constraints.
2. **Adaptive detector:** calibrated change/novelty scores with explicit safe signals and false-alarm control.
3. **Progenitor library:** dormant strategy or hedge templates that can be differentiated into bounded specialists.
4. **Memory and clonal allocation:** retain validated regime responses; increase weight sequentially and reversibly.
5. **Cancer surveillance:** track strategy lineage and quarantine components whose private fitness diverges from system health.

This is not yet an alpha hypothesis. Its first credible target is lower expected shortfall, drawdown, and recovery time at a fixed cost and false-alarm budget.

## Alternatives that could explain any success

- ordinary change-point detection;
- a generic mixture of experts;
- volatility targeting or dynamic risk budgets;
- policy-library continual learning;
- diversification across conservative/aggressive agents;
- more parameters or a larger tuning budget;
- crisis-specific tuning or leakage.

The immune interpretation receives credit only for incremental performance in ablations against these alternatives.

## Synthetic pathology battery

Use a controlled simulator before historical backtesting because crisis labels and causal counterfactuals are otherwise unavailable.

| Pathology | Financial construction | Required diagnosis |
|---|---|---|
| Novel infection | Abrupt unseen return/covariance/liquidity regime | Detect quickly without tuning on the episode |
| Slow infection | Smooth parameter drift | Avoid waiting for an obvious crash |
| Autoimmunity | Benign high-volatility episode | Avoid excessive turnover/deleveraging |
| Immunodeficiency | Quiet buildup followed by a tail event | Avoid missing low-salience danger |
| Cytokine storm | Feedback from forced selling to price impact | Do not amplify the shock |
| Cancer | High standalone reward with hidden short-volatility tail | Detect fitness–health divergence |
| Metastasis | Cloned policies share an unobserved exposure | Detect lineage/common-risk concentration |
| Antigenic drift | Gradual adversarial change in a known pathology | Adapt without unlimited search |

## Equal-budget contestants

- **B0:** fixed risk limits and static allocation;
- **B1:** statistical change detector plus fixed response table;
- **B2:** conformal or one-class novelty detector plus fixed response;
- **B3:** generic mixture-of-experts/meta-controller;
- **B4:** layered controller without lineage/cancer surveillance;
- **B5:** full lineage-aware immune controller.

Equalize observable information, parameter/search budget, training samples, transaction-cost model, random seeds, and crisis exposure during development.

## Outcomes and falsification

Primary outcomes should be prespecified jointly:

- detection delay conditional on a true pathology;
- false-alarm rate in benign states;
- expected shortfall and maximum drawdown;
- turnover and modeled implementation cost;
- recovery time;
- missed-pathology rate;
- concentration by policy lineage and residual exposure.

The idea fails as a distinctive architecture if B5 does not outperform B3 and B4 on a held-out pathology family after multiplicity correction, or if lower tail loss comes only from permanently lower gross risk. It also fails operationally if false alarms, turnover, or feedback losses erase the benefit.

## Minimum cancer-surveillance rule

For policy \(i\), distinguish private fitness from system health:

\[
F_i = \text{net standalone reward}_i,
\qquad
H_i = -\Delta ES_i - \lambda_L L_i - \lambda_C C_i,
\]

where \(\Delta ES_i\) is the policy's incremental portfolio expected shortfall, \(L_i\) its stressed liquidity demand, and \(C_i\) its lineage/common-exposure concentration. A cancer alarm requires sustained \(F_i>0\) with materially negative \(H_i\), not merely poor recent returns.

The lineage graph should record parent model, training windows, features, objective, mutations, stress-test ancestry, and residual return similarity. This makes “metastasis” measurable instead of metaphorical.

## Promotion gates

Do not create a `HYP-*` record until all of the following exist:

1. simulator and pathology generators with untouched seeds/families;
2. operational definitions for every alarm and response;
3. equal-budget B0–B5 implementations;
4. frozen primary outcomes and family-wise inference rule;
5. complete mutation/search ledger;
6. a historical data plan with rolling-origin splits and an untouched confirmation era.

The first useful build is therefore a benchmark, not a live self-modifying trader.

