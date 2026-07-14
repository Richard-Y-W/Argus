# EXP-009 — Results: the VW/EW decay gap is composition, not evidence

*Run 2026-07-14. Status: **HYP-009 rejected**. Primary n=208: 180 EW, 28 VW.*

Raw proportional decay was 94.7% for VW portfolios versus 56.4% for EW, reproducing the seen EXP-005 descriptive gap. After controlling for in-sample mean, publication year, and post-publication horizon, the VW coefficient was **+0.152** (HC3 se 0.305, t = 0.50). P1 fails.

For post-publication mean, the adjusted VW coefficient was −0.132%/month (t = −1.00), so P2 fails conventional significance. Robust proportional-decay coefficients were +0.059 (winsorized, t=0.57) and +0.329 (clear-only, t=0.96): positive but imprecise. P3's directional wording passes narrowly, but the registered falsifier fires because the primary is insignificant and magnitudes are unstable.

The raw gap is not credible evidence that scalable large-cap implementations are arbitraged away more completely. Only 28 VW signals exist, portfolio weighting is chosen by original authors, ratio outcomes are unstable, and composition differs. Security-level alternative portfolios that implement both EW and VW for the *same signal* are required for a within-signal test.

Run `python analysis.py`; outputs are in `results/`.
