# Scout report — real-time macro vintages and false predictability

*Scouted 2026-08-02. AI-led macro/quant discovery cycle. This is a design audit, not an empirical result.*

## Question

How much apparent macro-financial predictability is created by using revised economic data that an investor could not have observed at the forecast origin?

This is deliberately not a race to nowcast GDP faster. The economically useful object is the gap between a historically feasible information set and the final-vintage panel commonly used in research. That gap can change model rankings, forecast errors, and apparent bond-return predictability.

## Prior evidence

- Croushore and Stark built the Real-Time Data Set for Macroeconomists (RTDSM) specifically to preserve snapshots of the information available at historical dates. Their forecasting work reports that vintage choice matters unevenly across tasks and can make forecast-error measures look deceptively favorable when final data replace real-time data ([RTDSM](https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/real-time-data-set-for-macroeconomists); [forecasting study](https://www.philadelphiafed.org/the-economy/macroeconomics/forecasting-with-a-real-time-data-set-for-macroeconomists)).
- Ghysels, Horan, and Moench show that revisions account for a sizeable share of the Treasury-return predictability attributed to macro data, while real-time survey forecasts contain distinct information ([New York Fed Staff Report 581](https://www.newyorkfed.org/research/staff_reports/sr581.html)).
- The New York Fed Staff Nowcast formalizes the ragged-edge problem with a dynamic-factor/Kalman-filter architecture that incorporates releases as news. Its public description also shows that mixed frequency, missing releases, time-varying volatility, and outliers are first-order design issues rather than implementation details ([Staff Nowcast](https://www.newyorkfed.org/research/policy/nowcast)).

The literature therefore occupies the broad claim that revisions matter. A useful Argus contribution cannot be “real-time data are better.” It must identify where a transparent, modest model loses its apparent advantage and why.

## Candidate designs

Scores are 1–5; higher confounding risk is worse.

| Candidate | Falsifiable | Data feasible | Novel | Mechanism | Learning | Confounding risk | Decision |
|---|---:|---:|---:|---:|---:|---:|---|
| Vintage fragility map for macro model rankings | 5 | 5 | 3 | 4 | 5 | 2 | Priority data audit |
| Revision-news decomposition of Treasury forecasts | 5 | 4 | 3 | 5 | 5 | 3 | Second; prior claim is occupied |
| Nonlinear nowcast versus simple benchmarks | 5 | 4 | 2 | 2 | 4 | 4 | Defer; invites model tournament |
| Cross-country vintage fragility | 5 | 2 | 4 | 4 | 5 | 4 | Defer pending comparable vintages |

## Proposed narrow hypothesis

For a preregistered set of parsimonious quarterly forecasting models, final-vintage evaluation will overstate performance relative to a fully vintage-correct evaluation, but the distortion will be concentrated in targets and horizons with large revisions rather than universal.

The strongest falsifier is not “no model predicts.” It is that model rankings and loss differentials are stable across vintage protocols. The analysis should compare first release, fixed-lag release, and latest vintage; freeze the model set; use expanding windows; and report the full target-by-horizon matrix with familywise control. A small, transparent model menu is preferable to tuning a large learner.

## Internal debate

- **Optimist:** This builds an institutional habit that transfers to every macro strategy: reconstruct the information set before interpreting a forecast.
- **Skeptic:** The main fact is known. A generic replication would be educational but not novel.
- **Statistician:** Model Confidence Set or conditional predictive ability methods should not be introduced until the target, loss, estimation window, and revision protocol are frozen. Dependence across horizons requires joint uncertainty.
- **Economist:** Revisions combine noise removal, conceptual redefinition, seasonal adjustment, and benchmark updates. “Look-ahead bias” is accurate operationally but not a single economic mechanism.
- **Portfolio manager:** A GDP forecast score is not a return forecast. Keep decision value separate from statistical accuracy.
- **ML researcher:** The honest benchmark is expanding-window linear or factor models. Flexible models add a second search problem before the vintage problem is measured.

## Promotion gate

Do not register `HYP-025` yet. First build a read-only inventory of RTDSM series, vintage coverage, release conventions, missing values, and stable download endpoints. Promotion requires at least three targets with consistent vintages, an executable acquisition script, and an unambiguous mapping from forecast origin to available observations.

## Connections

`literature_reviews/2026-08-02-macro-quant-research-map.md` · `ideas/hypothesis_queue.md` · `research_journal/2026-08-02-four-macro-quant-discovery-cycles.md`
