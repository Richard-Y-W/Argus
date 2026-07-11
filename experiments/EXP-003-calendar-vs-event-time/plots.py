"""EXP-003 figure. Reads results/regressions.csv; writes PNG.

Style: EXP-001/002 house style; blue = event-time terms, aqua = calendar-era
terms (palette validated in EXP-002; aqua's contrast WARN relieved by direct
value labels).
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

OUT = Path(__file__).resolve().parent / "results"

BLUE = "#2a78d6"
AQUA = "#1baf7a"
INK = "#333333"
MUTED = "#6b6b6b"
GRID = "#e3e3e0"

plt.rcParams.update(
    {
        "figure.dpi": 150,
        "font.size": 10,
        "text.color": INK,
        "axes.edgecolor": GRID,
        "axes.labelcolor": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.grid": True,
        "grid.color": GRID,
        "grid.linewidth": 0.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)

TERMS = [
    ("ps", "Post-sample (pre-pub.)", BLUE),
    ("pp1", "Post-pub. years 1–5", BLUE),
    ("pp2", "Post-pub. years 6–10", BLUE),
    ("pp3", "Post-pub. years 11+", BLUE),
    ("era_1993_2000", "Era 1993–2000", AQUA),
    ("era_2001_2010", "Era 2001–2010", AQUA),
    ("era_2011_2019", "Era 2011–2019", AQUA),
    ("era_2020_2024", "Era 2020–2024", AQUA),
]


def fig1_coefficients() -> None:
    reg = pd.read_csv(OUT / "regressions.csv")
    e2 = reg[reg["spec"] == "E2_pred_eventtime"].set_index("term")

    fig, ax = plt.subplots(figsize=(7.4, 4.8))
    ys = list(range(len(TERMS)))[::-1]
    ax.axvline(0, color=MUTED, linewidth=1, linestyle=(0, (3, 3)))
    for y, (term, label, color) in zip(ys, TERMS):
        r = e2.loc[term]
        lo, hi = r["coef"] - 1.96 * r["se"], r["coef"] + 1.96 * r["se"]
        ax.hlines(y, lo, hi, color=color, linewidth=2)
        ax.plot(r["coef"], y, "o", color=color, markersize=8, zorder=3)
        ax.annotate(f"{r['coef']:+.2f}", (r["coef"], y),
                    textcoords="offset points", xytext=(0, 8),
                    ha="center", color=INK, fontweight="bold", fontsize=9)
    ax.set_yticks(ys, [t[1] for t in TERMS])
    for tick, (_, _, color) in zip(ax.get_yticklabels()[::-1], TERMS):
        tick.set_color(INK)
    ax.set_xlabel("Change in mean LS return vs in-sample (% per month)")
    ax.set_title(
        "Decay follows each predictor's own clock (blue),\n"
        "not the calendar (green)\n"
        "212 predictors, signal FE, 95% CIs month-clustered.\n"
        "Base: in-sample window, pre-1993 era. Gross of costs.\n"
        "Data: Chen–Zimmermann Oct 2025",
        loc="left", fontsize=10, color=MUTED,
    )
    ax.grid(axis="y", visible=False)
    fig.tight_layout()
    fig.savefig(OUT / "fig1_eventtime_vs_era_coefficients.png")
    plt.close(fig)


if __name__ == "__main__":
    fig1_coefficients()
    print("figures written")
