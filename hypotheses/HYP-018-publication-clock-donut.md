# HYP-018 — US decay is not an annual publication-boundary artifact

*Registered 2026-07-21 before computing donut-window outcomes. AI-led.*

## Motivation and prediction

JKP metadata identifies publication years, not exact dates. Months inside the boundary year can therefore be assigned to the wrong information regime. Genuine post-publication decay should remain when ambiguous boundary observations are removed.

P1: after excluding the publication year, post-publication decay is at most -0.10 pp/month with |t| >= 2.0. P2: after excluding the publication year plus the preceding and following calendar years, decay remains negative with |t| >= 1.65. P3: the strict-donut estimate differs from EXP-016's -0.164 pp/month benchmark by no more than 0.08 pp/month. Survival requires all three. A non-negative estimate in either donut is a falsifier.

## Alternatives and limits

Failure would implicate coarse event dating or local time trends. Survival would address timing misclassification, not identify who traded.

## Data, debate, and value

Pinned JKP US panel; low implementation difficulty, moderate identification value. The Optimist expects little change; the Skeptic expects the boundary year to carry the result; the Statistician requires unchanged metadata and month clustering; the Economist warns that annual donuts also discard legitimate treatment months; the Portfolio Manager and ML Researcher see no strategy or tuning claim.

## Connections

EXP-016 · `experiments/EXP-018-publication-clock-donut/design.md`
