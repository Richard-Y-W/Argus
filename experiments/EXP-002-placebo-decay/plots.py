"""EXP-002 figures. Reads results/ CSVs produced by analysis.py; writes PNGs.

Style: EXP-001 house style. Two-group palette blue/aqua validated
(CVD deltaE 73.6, aqua contrast WARN relieved by direct value labels).
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

OUT = Path(__file__).resolve().parent / "results"
EXP1 = Path(__file__).resolve().parents[1] / "EXP-001-anomaly-decay" / "results"

BLUE = "#2a78d6"   # predictors (series color carried over from EXP-001)
AQUA = "#1baf7a"   # placebos
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
WINDOWS = ["in_sample", "post_sample", "post_pub"]


def fig1_group_window_means() -> None:
    est = pd.read_csv(OUT / "window_level_by_group.csv")
    est = est[est["group"].isin(["predictor", "placebo_all"])]
    est["lo"] = est["mean"] - 1.96 * est["se"]
    est["hi"] = est["mean"] + 1.96 * est["se"]

    fig, ax = plt.subplots(figsize=(6.6, 4.4))
    ax.hlines(0, -0.5, 2.5, color=MUTED, linewidth=1, linestyle=(0, (3, 3)))
    offsets = {"predictor": -0.13, "placebo_all": 0.13}
    colors = {"predictor": BLUE, "placebo_all": AQUA}
    names = {"predictor": "Predictors (n=212)", "placebo_all": "Placebos (n=114)"}
    for grp, g in est.groupby("group"):
        g = g.set_index("window").reindex(WINDOWS).reset_index()
        x = [i + offsets[grp] for i in range(3)]
        ax.vlines(x, g["lo"], g["hi"], color=colors[grp], linewidth=2)
        ax.plot(x, g["mean"], "o", color=colors[grp], markersize=8, zorder=3,
                label=names[grp])
        for xi, (_, r) in zip(x, g.iterrows()):
            ax.annotate(f"{r['mean']:.2f}", (xi, r["hi"]),
                        textcoords="offset points", xytext=(0, 6),
                        ha="center", color=INK, fontweight="bold", fontsize=9)
    ax.set_xticks(range(3), [LABELS[w] for w in WINDOWS])
    ax.set_ylabel("Mean long–short return (% per month)")
    ax.set_xlim(-0.5, 2.5)
    ax.legend(frameon=False, loc="upper right")
    ax.set_title(
        "Predictors decay after publication; placebos barely move\n"
        "95% CIs, month-clustered. Gross of costs. Data: Chen–Zimmermann Oct 2025",
        loc="left", fontsize=10, color=MUTED,
    )
    ax.grid(axis="x", visible=False)
    fig.tight_layout()
    fig.savefig(OUT / "fig1_group_window_means.png")
    plt.close(fig)


def fig2_scatter_both_groups() -> None:
    plc = pd.read_csv(OUT / "window_means_by_placebo.csv")
    prd = pd.read_csv(EXP1 / "window_means_by_predictor.csv")

    fig, ax = plt.subplots(figsize=(5.8, 5.4))
    lim_lo, lim_hi = -1.0, 2.5
    ax.plot([lim_lo, lim_hi], [lim_lo, lim_hi], color=MUTED, linewidth=1,
            linestyle=(0, (3, 3)), zorder=1)
    ax.axhline(0, color=GRID, linewidth=1, zorder=1)
    ax.axvline(0, color=GRID, linewidth=1, zorder=1)
    ax.scatter(prd["in_sample"], prd["post_pub"], s=22, color=BLUE, alpha=0.5,
               edgecolors="white", linewidths=0.5, zorder=2, label="Predictors")
    ax.scatter(plc["in_sample"], plc["post_pub"], s=26, color=AQUA, alpha=0.7,
               edgecolors="white", linewidths=0.5, zorder=3, label="Placebos")
    ax.annotate("no decay (45° line)", (-0.35, -0.28), rotation=45,
                color=MUTED, ha="center", va="center", fontsize=9)
    ax.set_xlim(lim_lo, lim_hi)
    ax.set_ylim(lim_lo, lim_hi)
    ax.set_aspect("equal")
    ax.set_xlabel("In-sample mean return (%/month)")
    ax.set_ylabel("Post-publication mean return (%/month)")
    ax.legend(frameon=False, loc="upper left")
    ax.set_title(
        "Placebos cluster at the origin and on the 45° line;\n"
        "predictors sit right and below it\n"
        "One dot per signal, gross of costs.\n"
        "Data: Chen–Zimmermann Oct 2025",
        loc="left", fontsize=10, color=MUTED,
    )
    fig.tight_layout()
    fig.savefig(OUT / "fig2_scatter_predictors_vs_placebos.png")
    plt.close(fig)


if __name__ == "__main__":
    fig1_group_window_means()
    fig2_scatter_both_groups()
    print("figures written")
