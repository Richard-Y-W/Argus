# Positive clinical-announcement spike reversal — frozen sandbox design

**Frozen before price retrieval:** 2026-08-21  
**Stage:** exploratory smoke test; not HYP/EXP registered and not claim eligible

## Question

After a clinical announcement produces an initially positive sponsor reaction, does shorting after that reaction earn positive sector-adjusted returns over the next 20 sessions?

## Sample

Use all 16 positive announcements in Hwang (2013) Table 2. Do not filter by the size of the initial move. Duplicate firms and the two sofosbuvir announcements remain in the sample and are disclosed as dependent observations.

Ticker mapping follows the paper except `BMS -> BMY`, the traded Bristol-Myers Squibb ticker. SPY is the market benchmark. Public adjusted daily closes are retrieved without altering the event list.

## Timing

- Session 0 is the first trading session on or after the published announcement date.
- Initial reaction is the sponsor cumulative return minus SPY cumulative return from the prior-session close through session +1 close.
- A trade is eligible only when that initial abnormal reaction is greater than zero.
- Enter the short at the session +1 close. This conservative delay avoids needing an announcement-time assumption.
- Primary exit is session +20 close. Secondary descriptive exits are +5 and +60; they cannot rescue the primary result.

## Estimand and decision rule

For each eligible event:

`short abnormal return = -(stock holding return - SPY holding return)`

Primary estimand is the equal-event mean gross short abnormal return from +1 to +20. Also report median, fraction positive, a t-based 95% interval, and a sponsor-cluster bootstrap interval when the larger event panel is built.

This small sandbox passes only if:

1. at least eight events are eligible;
2. mean +1-to-+20 gross short abnormal return is positive;
3. the 50 bp round-trip-cost mean remains positive; and
4. at least 60% of eligible events have positive short abnormal returns.

Passing does not establish alpha; it only justifies reconstructing a small-biotech universe. Failing rejects this exact untuned rule in the Hwang sample.

## Known limitations

The sample contains large surviving firms, exact announcement times are unavailable, prices are not survivorship-safe for a broader biotech universe, borrow is assumed available, and a fixed cost is not actual historical execution. No inference from this sandbox may be promoted.

