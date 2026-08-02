# Scout report — monetary-policy communication shocks

*Scouted 2026-08-02. AI-led macro/quant discovery cycle. No shock series was estimated.*

## Question

Can a reproducible decomposition separate a policy-rate-path surprise, central-bank information, and a non-yield risk-premium communication shock around FOMC announcements without labeling the components after seeing asset returns?

This is not a low-latency event-trading project. It is an identification project about what an announcement surprise means.

## Prior evidence

- Faust, Swanson, and Wright use federal-funds futures around policy decisions to identify the expected rate-path surprise and show that standard recursive VAR restrictions are rejected ([Federal Reserve IFDP](https://www.federalreserve.gov/econres/ifdp/identifying-vars-based-on-high-frequency-futures-data.htm)).
- The modern literature warns that a positive rate surprise accompanied by stronger equities may contain central-bank information rather than a pure contractionary shock. This creates a sign-labeling and interpretation problem, not merely a measurement problem.
- Boehm and Kroner estimate a “Fed non-yield shock” from announcement-window excess volatility in equities and exchange rates. Their component is orthogonal to yield changes, moves equities and the dollar strongly, and is associated with risk measures and communication ([Federal Reserve IFDP 1392](https://www.federalreserve.gov/econres/ifdp/monetary-policy-without-moving-interest-rates-the-fed-non-yield-shock.htm)).
- A recent Federal Reserve comparison emphasizes that differences across published monetary shock series reflect both the underlying data and extraction methods, warning against treating one convenient series as ground truth ([Monetary Policy Shocks: Data or Methods?](https://www.federalreserve.gov/econres/feds/files/2024011r1pap.pdf)).

The broad decomposition is heavily occupied. The research gap is reproducibility and stability: do economically named components persist across reasonable windows, instruments, and sign restrictions fixed before downstream outcomes are inspected?

## Candidate designs

| Candidate | Falsifiable | Data feasible | Novel | Mechanism | Learning | Confounding risk | Decision |
|---|---:|---:|---:|---:|---:|---:|---|
| Shock-taxonomy stability audit | 5 | 3 | 4 | 5 | 5 | 3 | Priority; data-license audit |
| Statement-versus-press-conference decomposition | 5 | 3 | 3 | 5 | 5 | 4 | Second; regime-limited |
| LLM classification of FOMC text | 4 | 5 | 2 | 2 | 4 | 5 | Reject as first project |
| Announcement-window cross-asset prediction | 4 | 2 | 2 | 2 | 3 | 5 | Reject; microstructure and mining risk |

## Proposed narrow hypothesis

The economic labels attached to high-frequency FOMC shock components will be less stable than their in-sample covariance decompositions suggest: component signs and event rankings will change materially across preregistered, defensible measurement windows and instrument sets.

A stability audit would freeze event timestamps, use only securities with documented historical quotes, estimate components without future macro outcomes, align signs using predetermined instrument loadings, and evaluate subspace similarity, event-rank concordance, and downstream impulse-response sensitivity. The null worth preserving is that the published taxonomy is stable.

## Internal debate

- **Optimist:** This teaches identification, PCA/rotations, event studies, and macro-financial interpretation in one coherent project.
- **Skeptic:** Many researchers already compare shock series. Without raw intraday data and timestamp discipline, Argus would produce an inferior rehash.
- **Statistician:** Factor rotations are not identified by variance alone. Sign restrictions chosen after looking at equities or macro responses are outcome contamination.
- **Economist:** “Fed information” and “risk-premium communication” can coexist in one announcement. Orthogonality in observables does not prove structural independence.
- **Portfolio manager:** Close-to-close returns blur the release with a full day of news; free intraday histories may be insufficient for claim-bearing work.
- **ML researcher:** Text models should be used, if at all, as externally evaluated measurements after the financial decomposition—not to manufacture labels.

## Promotion gate

Do not register. Inventory public event timestamps and published shock-series licenses, then determine whether the raw instruments can be reconstructed without proprietary intraday futures. Promotion requires a point-in-time event calendar, at least two defensible measurement windows, and a sign convention defined independently of the outcomes used for validation.

## Connections

`literature_reviews/2026-08-02-macro-quant-research-map.md` · `ideas/hypothesis_queue.md` · `research_journal/2026-08-02-four-macro-quant-discovery-cycles.md`
