# EXP-018 — Annual boundary ambiguity does not carry US decay

## Verdict

**HYP-018 survives all three registered rules.** Neither donut estimate is non-negative, so the falsifier does not fire.

## Results

Removing every factor's publication calendar year leaves post-publication decay at **-0.164 pp/month** (t = **-2.97**). Removing the publication year and both adjacent years leaves **-0.161 pp/month** (t = **-2.85**). The strict estimate differs from the frozen -0.164 benchmark by only **+0.003 pp/month**, well inside P3's 0.08 bound. The strict post-publication-minus-post-sample contrast is -0.255 pp/month (t = -2.87).

## Adversarial review

- Donuts reduce boundary misclassification but do not recover exact dissemination dates.
- Removing three years changes the estimand and can discard legitimate adjustment dynamics.
- Publication-year metadata can still be wrong at the paper level.
- Robust timing does not establish a publication-arbitrage mechanism.

## Reproduction and connections

Run `python experiments/EXP-018-publication-clock-donut/analysis.py`. HYP-018 · EXP-016 · EXP-017 · EXP-019
