"""EXP-001 figures. Reads results/ CSVs produced by analysis.py; writes PNGs.

Style: single-hue (blue), recessive grid, text in ink tokens, direct labels.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

OUT = Path(__file__).resolve().parent / "results"

BLUE = "#2a78d6"
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

LABELS = {
    "in_sample": "In-sample",
    "post_sample": "Post-sample,\npre-publication",
    "post_pub": "Post-\npublication",
}


def fig1_window_means() -> None:
    est = pd.read_csv(OUT / "window_level_estimates.csv")
    est["lo"] = est["mean"] - 1.96 * est["se"]
    est["hi"] = est["mean"] + 1.96 * est["se"]

    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    x = range(len(est))
    ax.hlines(0, -0.5, len(est) - 0.5, color=MUTED, linewidth=1, linestyle=(0, (3, 3)))
    ax.vlines(x, est["lo"], est["hi"], color=BLUE, linewidth=2)
    ax.plot(x, est["mean"], "o", color=BLUE, markersize=8, zorder=3)
    for i, r in est.iterrows():
        ax.annotate(
            f"{r['mean']:.2f}%",
            (i, r["hi"]),
            textcoords="offset points",
            xytext=(0, 6),
            ha="center",
            color=INK,
            fontweight="bold",
        )
    ax.set_xticks(list(x), [LABELS[w] for w in est["window"]])
    ax.set_ylabel("Mean long–short return (% per month)")
    ax.set_xlim(-0.5, len(est) - 0.5)
    ax.set_title(
        "Published predictor returns by window — 212 predictors, 1926–2024\n"
        "95% CIs, month-clustered. Gross of costs. Data: Chen–Zimmermann Oct 2025",
        loc="left",
        fontsize=10,
        color=MUTED,
    )
    ax.grid(axis="x", visible=False)
    fig.tight_layout()
    fig.savefig(OUT / "fig1_window_means.png")
    plt.close(fig)


def fig2_scatter() -> None:
    pp = pd.read_csv(OUT / "window_means_by_predictor.csv")

    fig, ax = plt.subplots(figsize=(5.8, 5.4))
    lim_lo, lim_hi = -1.0, 2.5
    ax.plot([lim_lo, lim_hi], [lim_lo, lim_hi], color=MUTED, linewidth=1,
            linestyle=(0, (3, 3)), zorder=1)
    ax.axhline(0, color=GRID, linewidth=1, zorder=1)
    ax.axvline(0, color=GRID, linewidth=1, zorder=1)
    ax.scatter(
        pp["in_sample"], pp["post_pub"],
        s=22, color=BLUE, alpha=0.55, edgecolors="white", linewidths=0.5, zorder=2,
    )
    ax.annotate("no decay (45° line)", (-0.35, -0.28), rotation=45,
                color=MUTED, ha="center", va="center", fontsize=9)
    ax.set_xlim(lim_lo, lim_hi)
    ax.set_ylim(lim_lo, lim_hi)
    ax.set_aspect("equal")
    ax.set_xlabel("In-sample mean return (%/month)")
    ax.set_ylabel("Post-publication mean return (%/month)")
    ax.set_title(
        "Most predictors fall below the 45° line:\n"
        "decay, but not to zero\n"
        "One dot per predictor (n=212), gross of costs.\n"
        "Data: Chen–Zimmermann Oct 2025",
        loc="left",
        fontsize=10,
        color=MUTED,
    )
    fig.tight_layout()
    fig.savefig(OUT / "fig2_is_vs_postpub.png")
    plt.close(fig)


if __name__ == "__main__":
    fig1_window_means()
    fig2_scatter()
    print("figures written")
