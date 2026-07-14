# EXP-008 — Registered design: post-publication crowding

*Registered 2026-07-14 before analysis.*

Use pinned predictor/placebo LS returns and SignalDoc. Normalize dates to months. For every target signal, construct a leave-target-out equal-weighted composite of clear/likely predictors published strictly earlier. Compute target/composite Pearson correlation for months −60:-1 and +1:+60 around publication; require 36 paired months and five composite members each month. Score predictor mean changes using a one-sample HC3 intercept regression and report sign share. Repeat identically for placebos. Predictor-minus-placebo mean-change difference uses Welch standard error.

Robustness: 120-month windows requiring 60 months. No exposure or return optimization.
