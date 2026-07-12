"""EXP-005 figures. Reads results/ CSVs produced by analysis.py; writes PNGs.

Style: matches EXP-001 (single-hue blue, recessive grid, ink-token text).
Terciles are ordered, so they get a sequential light->dark ramp of one hue,
not categorical hues.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent / "results"

BLUE = "#2a78d6"
RAMP = {"T1_low": "#a8cdf0", "T2_mid": "#5a9bd8", "T3_high": "#1c5a8a"}
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

WINDOWS = ["in_sample", "post_sample", "post_pub"]
WLABELS = ["In-sample", "Post-sample,\npre-publication", "Post-\npublication"]
TLABELS = {"T1_low": "Bottom tercile", "T2_mid": "Middle tercile", "T3_high": "Top tercile"}


def fig1_terciles() -> None:
    terc = pd.read_csv(OUT / "terciles.csv")
    terc = terc[terc["char"] == "op_t"]

    fig, ax = plt.subplots(figsize=(6.6, 4.4))
    ax.hlines(0, -0.5, 2.5, color=MUTED, linewidth=1, linestyle=(0, (3, 3)))
    offsets = {"T1_low": -0.18, "T2_mid": 0.0, "T3_high": 0.18}
    for t, off in offsets.items():
        d = terc[terc["tercile"] == t].set_index("window").reindex(WINDOWS)
        x = np.arange(3) + off
        lo = d["mean"] - 1.96 * d["se"]
        hi = d["mean"] + 1.96 * d["se"]
        ax.vlines(x, lo, hi, color=RAMP[t], linewidth=2)
        ax.plot(x, d["mean"], "o-", color=RAMP[t], markersize=7, linewidth=1.2,
                label=TLABELS[t], zorder=3)
    # Direct labels on the outer terciles at the endpoints
    for t, va in [("T3_high", "bottom"), ("T1_low", "top")]:
        d = terc[terc["tercile"] == t].set_index("window")
        for wi, w in [(0, "in_sample"), (2, "post_pub")]:
            ax.annotate(f"{d.loc[w, 'mean']:.2f}", (wi + offsets[t], d.loc[w, "mean"]),
                        textcoords="offset points",
                        xytext=(10, 4 if va == "bottom" else -10), ha="left",
                        color=INK, fontsize=9, fontweight="bold")
    ax.set_xticks(range(3), WLABELS)
    ax.set_ylabel("Mean long–short return (% per month)")
    ax.set_xlim(-0.5, 2.5)
    ax.legend(frameon=False, loc="upper right", title="Original-paper t-stat",
              title_fontsize=9, fontsize=9)
    ax.set_title(
        "Strong-evidence predictors lose more per month, but every tercile\n"
        "keeps roughly half its in-sample return after publication\n"
        "Terciles of original-paper t-stat, 188 predictors. 95% CIs, month-clustered.\n"
        "Gross of costs. Data: Chen–Zimmermann Oct 2025",
        loc="left",
        fontsize=10,
        color=MUTED,
    )
    ax.grid(axis="x", visible=False)
    fig.tight_layout()
    fig.savefig(OUT / "fig1_windows_by_op_t_tercile.png")
    plt.close(fig)


def fig2_decline_vs_op_t() -> None:
    ch = pd.read_csv(OUT / "characteristics.csv")

    fig, ax = plt.subplots(figsize=(6.0, 4.6))
    ax.axhline(0, color=MUTED, linewidth=1, linestyle=(0, (3, 3)))
    ax.scatter(ch["op_t_raw"], ch["decline_pp"], s=22, color=BLUE, alpha=0.55,
               edgecolors="white", linewidths=0.5, zorder=2)
    b, a = np.polyfit(ch["op_t_raw"], ch["decline_pp"], 1)
    xs = np.array([ch["op_t_raw"].min(), ch["op_t_raw"].max()])
    ax.plot(xs, a + b * xs, color="#1c5a8a", linewidth=2, zorder=3)
    ax.annotate(f"OLS slope: {b:.3f} %/mo per t-stat unit", (xs[1], a + b * xs[1]),
                textcoords="offset points", xytext=(-8, 10), ha="right",
                color=INK, fontsize=9, fontweight="bold")
    ax.set_xlabel("Original-paper t-statistic")
    ax.set_ylabel("In-sample minus post-publication mean (%/month)")
    ax.set_title(
        "Predictors with stronger published evidence give back more\n"
        "One dot per predictor (n=188); positive y = decay. Gross of costs.\n"
        "Data: Chen–Zimmermann Oct 2025",
        loc="left",
        fontsize=10,
        color=MUTED,
    )
    fig.tight_layout()
    fig.savefig(OUT / "fig2_decline_vs_op_t.png")
    plt.close(fig)


if __name__ == "__main__":
    fig1_terciles()
    fig2_decline_vs_op_t()
    print("figures written")
