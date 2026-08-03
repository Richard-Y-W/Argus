"""EXP-027 figures from archived result CSVs."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OUT = Path(__file__).parent / "results"
NAVY, BLUE, ORANGE, RED = "#17365D", "#2E75B6", "#ED7D31", "#C00000"
GREEN, MUTED, GRID, PAPER = "#70AD47", "#666666", "#D9E1F2", "#FAFBFD"

plt.rcParams.update({
    "figure.dpi": 160, "savefig.dpi": 240, "font.family": "DejaVu Sans",
    "font.size": 9.5, "axes.facecolor": PAPER, "figure.facecolor": "white",
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.65,
    "axes.spines.top": False, "axes.spines.right": False,
})


def intervals() -> None:
    s = pd.read_csv(OUT / "summary.csv").iloc[:3].copy()
    labels = ["Gate − local evolution", "Gate − global random", "Gate − fixed hybrid"]
    colors = [BLUE, RED, ORANGE]
    fig, ax = plt.subplots(figsize=(8.4, 4.5))
    for y, (label, (_, r), color) in enumerate(zip(labels[::-1], list(s.iterrows())[::-1], colors[::-1])):
        ax.hlines(y, r.ci_low, r.ci_high, color=color, linewidth=3)
        ax.plot(r.estimate, y, "o", color=color, markersize=8)
        ax.annotate(f"{r.estimate:+.4f} [{r.ci_low:+.4f}, {r.ci_high:+.4f}]",
                    (r.ci_high, y), xytext=(7, 0), textcoords="offset points", va="center")
    ax.axvline(0, color="#333333", linewidth=1, linestyle=(0, (4, 3)))
    ax.set_yticks(range(3), labels[::-1])
    ax.set_xlabel("Family-balanced 252-day cumulative net log-return difference")
    ax.set_title("EXP-027: the observable distance gate beat no fixed search policy",
                 loc="left", color=NAVY, fontsize=13, fontweight="bold")
    ax.text(0, -0.23, "Whiskers: preregistered 95% family-stratified paired bootstrap intervals. Synthetic paths only.",
            transform=ax.transAxes, color=MUTED, fontsize=8.5)
    ax.grid(axis="y", visible=False)
    fig.subplots_adjust(left=0.25, bottom=0.23, top=0.82, right=0.94)
    fig.savefig(OUT / "fig1_gate_performance.png", bbox_inches="tight")
    fig.savefig(OUT / "fig1_gate_performance.pdf", bbox_inches="tight")
    plt.close(fig)


def routing() -> None:
    data = pd.read_csv(OUT / "seed_metrics.csv")
    gate = data[data.method == "gate"]
    order = ["small_drift", "moderate_rotation", "mean_reversion", "correlation_break"]
    grouped = gate.groupby("family").mean(numeric_only=True).loc[order]
    x = np.arange(len(order))
    fig, ax = plt.subplots(figsize=(8.8, 5.0))
    ax.bar(x, grouped.local_share, color=BLUE, label="Local mutation")
    ax.bar(x, grouped.hybrid_share, bottom=grouped.local_share, color=ORANGE, label="Mixed search")
    ax.bar(x, grouped.global_share, bottom=grouped.local_share + grouped.hybrid_share,
           color=GREEN, label="Global restart")
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Mean fraction of adaptation blocks")
    ax.set_xticks(x, [s.replace("_", " ").title() for s in order])
    ax.legend(frameon=False, ncol=3, loc="upper left")
    ax2 = ax.twinx()
    ax2.plot(x, grouped.mean_distance, color=RED, marker="D", linewidth=2, label="Mean observed distance")
    ax2.axhline(1.25, color=MUTED, linestyle=(0, (3, 3)), linewidth=0.9)
    ax2.axhline(2.50, color=MUTED, linestyle=(0, (3, 3)), linewidth=0.9)
    ax2.set_ylabel("Mean standardized environmental distance", color=RED)
    ax2.tick_params(axis="y", colors=RED)
    ax.set_title("EXP-027 routing: the score separated the correlation break,\n"
                 "but not moderate rotation from mean reversion",
                 loc="left", color=NAVY, fontsize=13, fontweight="bold")
    ax.text(0, -0.19, "Routing is causal and delayed; thresholds 1.25 and 2.50 were frozen before execution.",
            transform=ax.transAxes, color=MUTED, fontsize=8.5)
    fig.subplots_adjust(bottom=0.21, top=0.78, right=0.86)
    fig.savefig(OUT / "fig2_gate_routing.png", bbox_inches="tight")
    fig.savefig(OUT / "fig2_gate_routing.pdf", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    intervals()
    routing()
    print("EXP-027 figures written")

