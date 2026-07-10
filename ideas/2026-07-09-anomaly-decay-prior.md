# Prior: why published anomalies stop working

*Elicited 2026-07-09, before reading any of the anomaly-decay literature. Recorded so it can be compared against McLean & Pontiff (2016) later. This is the researcher's first human-originated research statement in the repository.*

## The researcher's prior (own words, lightly cleaned)

> Once the shortcoming — the anomaly — is identified and there is information on it, the markets work to optimize it and it no longer is an anomaly. I think this is because finance is just very well optimized: it will catch and patch the holes once they get identified.

## Restated as a mechanism

Publication releases information → arbitrage capital flows toward the mispricing → trading pressure moves prices until the excess return is gone. Decay is caused by **correction**, and the implied end state is **full decay** (the anomaly disappears entirely).

## What this prior implicitly rules out (to be tested against the literature)

The prior covers one mechanism. At least three competitors exist and predict different things:

1. **It was never real** — the "anomaly" was data mining; there was nothing to correct.
2. **Limits to arbitrage** — correction happens but stalls (costs, shorting constraints, capital limits), so decay is partial.
3. **Risk premium** — the return is compensation for real risk and should *not* decay after publication at all.

## The researcher's three-window prediction (2026-07-09, before reading the paper)

Asked what each story predicts for in-sample / post-sample-pre-publication / post-publication returns, the researcher predicted (own words, lightly cleaned):

> In-sample the anomaly looks good, perhaps because of overfitting and hindsight. Post-sample but pre-publication it still looks good. Post-publication it might be decayed. The post-publication window is the key to telling story 1 (arbitraged away) apart from story 2 (never real).

**What this got right:** the story-1 timeline is exactly correct — a real effect persists after the sample ends (no one knows about it yet) and decays only once publication releases the information.

**The contradiction (teaching point):** the answer attributes in-sample performance to *overfitting* but then predicts the effect *persists* post-sample. Overfitting cannot do both — noise fitted in-sample has no reason to continue out-of-sample. The answer blended story 2's explanation with story 1's prediction into a single timeline, instead of generating separate window-by-window predictions per mechanism.

**The correct discriminator:** the **post-sample, pre-publication** window — not post-publication. Story 1 (real, later arbitraged) predicts returns *hold up* there; story 2 (data mining) predicts returns are *already gone* there, since nothing real ever existed. By the post-publication window, both stories predict low returns and can no longer be told apart. Story 3 (risk premium) predicts no decay in any window.

## Resolution vs. McLean & Pontiff (2016)

M&P's design is precisely this three-window comparison across ~97 published predictors. Their findings:

- Post-sample (pre-publication) returns fall by roughly a quarter relative to in-sample → part of published performance was statistical bias (story 2 is partly true).
- Post-publication returns fall by roughly 55–60% relative to in-sample → publication itself destroys an additional large chunk (story 1 is partly true — the researcher's original mechanism is real and operative).
- **But returns do not go to zero.** Decay is partial, contradicting the original prior's implied end state of full correction.
- Supporting evidence for the arbitrage channel: post-publication increases in volume and short interest in anomaly stocks; and predictors that are *costlier to arbitrage* (illiquid, high idiosyncratic risk) decay *less* — pointing to **limits to arbitrage** as the reason correction stalls.

**Gap between prior and evidence:** the researcher's mechanism (information → correction) was confirmed as one operative channel, but the prior overestimated market efficiency in two directions — it assumed everything published was real (ignoring statistical bias) and assumed correction completes (ignoring arbitrage costs). "Finance is very well optimized" survives only in weakened form: *optimization is real but bounded by the costs of doing it.*

## Status

- [x] Compare against McLean & Pontiff (2016), *"Does Academic Research Destroy Stock Return Predictability?"*
- [x] Record the gap between this prior and the evidence (above)
- [ ] Researcher reads the paper itself (free on SSRN) and writes the `papers/` note
- [ ] Candidate first research cycle: reproduce the decay pattern on open data (Chen & Zimmermann's Open Source Asset Pricing dataset)

## Connections

- `research_journal/2026-07-09-day-zero.md` (where the question was posed)
- Future: `papers/` note on McLean & Pontiff 2016; candidate first hypothesis on decay dynamics
