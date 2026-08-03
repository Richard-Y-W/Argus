"""Professional figures for Argus digital-assets and financial-genetics threads.

All empirical panels read archived experiment outputs. The PLEX panel is explicitly
a research-design schematic and must not be interpreted as an estimated effect.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
EXP25 = ROOT / "experiments" / "EXP-025-financial-genome-adaptation" / "results"
EXP26 = ROOT / "experiments" / "EXP-026-diversity-preserving-financial-genetics" / "results"

NAVY = "#17365D"
BLUE = "#2E75B6"
CYAN = "#5B9BD5"
ORANGE = "#ED7D31"
GREEN = "#70AD47"
RED = "#C00000"
INK = "#252525"
MUTED = "#666666"
GRID = "#D9E1F2"
PAPER = "#FAFBFD"

plt.rcParams.update({
    "figure.dpi": 160, "savefig.dpi": 240, "font.family": "DejaVu Sans",
    "font.size": 9.5, "axes.facecolor": PAPER, "figure.facecolor": "white",
    "axes.edgecolor": "#A6A6A6", "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.grid": True,
    "grid.color": GRID, "grid.linewidth": 0.65, "grid.alpha": 0.85,
    "axes.spines.top": False, "axes.spines.right": False,
})


def save(fig: plt.Figure, name: str) -> None:
    fig.savefig(OUT / name, bbox_inches="tight", facecolor="white")
    fig.savefig(OUT / name.replace(".png", ".pdf"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


def evidence_intervals() -> None:
    s25 = pd.read_csv(EXP25 / "summary.csv")
    s26 = pd.read_csv(EXP26 / "summary.csv")
    rows = [
        ("EXP-025: mutation − random\n(lower regret)",
         s25.loc[s25.endpoint == "random_minus_evolution_regret"].iloc[0], BLUE),
        ("EXP-026: diverse hybrid − evolution\n(full-year return)",
         s26.loc[s26.endpoint == "hybrid_minus_evolution_full"].iloc[0], ORANGE),
        ("EXP-026: diverse hybrid − random\n(full-year return)",
         s26.loc[s26.endpoint == "hybrid_minus_random_full"].iloc[0], RED),
    ]
    fig, ax = plt.subplots(figsize=(9.0, 4.8))
    for y, (label, row, color) in enumerate(rows[::-1]):
        ax.hlines(y, row.ci_low, row.ci_high, color=color, linewidth=3)
        ax.plot(row.estimate, y, "o", color=color, markersize=8, zorder=3)
        ax.annotate(f"{row.estimate:+.4f}  [{row.ci_low:+.4f}, {row.ci_high:+.4f}]",
                    (row.ci_high, y), xytext=(8, 0), textcoords="offset points",
                    va="center", color=INK, fontsize=9)
    ax.axvline(0, color=INK, linewidth=1.1, linestyle=(0, (4, 3)))
    ax.set_yticks(range(len(rows)), [r[0] for r in rows[::-1]])
    ax.set_xlabel("Paired effect in cumulative log-return units")
    ax.set_xlim(-0.02, 0.038)
    ax.set_title("Financial genetics: inherited search showed a bounded advantage,\n"
                 "but the fixed diversity hybrid did not generalize",
                 loc="left", color=NAVY, fontsize=13, fontweight="bold")
    ax.text(0, -0.28, "Whiskers: preregistered 95% paired bootstrap intervals. Synthetic experiments; no market-alpha claim.",
            transform=ax.transAxes, color=MUTED, fontsize=8.5)
    ax.grid(axis="y", visible=False)
    fig.subplots_adjust(left=0.31, bottom=0.24, right=0.94, top=0.78)
    save(fig, "fig1_financial_genetics_evidence.png")


def diversity_performance() -> None:
    data = pd.read_csv(EXP26 / "seed_metrics.csv")
    grouped = data.groupby(["family", "method"], as_index=False).agg(
        full_return=("full_return", "mean"),
        phenotype_diversity=("phenotype_diversity", "mean"),
        annual_es_5=("annual_es_5", "mean"),
    )
    colors = {"evolution": BLUE, "random": GREEN, "hybrid_quality": ORANGE, "hybrid_diverse": RED}
    markers = {"rotation": "o", "correlation_flip": "s", "mean_reversion": "^"}
    labels = {"evolution": "Local evolution", "random": "Global random",
              "hybrid_quality": "Mixed candidates", "hybrid_diverse": "Diversity reserve"}
    fig, ax = plt.subplots(figsize=(8.6, 5.8))
    for _, r in grouped.iterrows():
        size = (48 + 18 * (r.annual_es_5 - grouped.annual_es_5.min()) /
                max(grouped.annual_es_5.max() - grouped.annual_es_5.min(), 1e-9))
        ax.scatter(r.phenotype_diversity, r.full_return, s=size,
                   marker=markers[r.family], color=colors[r.method],
                   edgecolor="white", linewidth=0.8, zorder=3)
    for method, color in colors.items():
        subset = grouped[grouped.method == method]
        ax.plot(subset.phenotype_diversity.mean(), subset.full_return.mean(),
                marker="D", markersize=8, color=color, linestyle="none", label=labels[method])
    ax.axhline(0, color=MUTED, linewidth=0.9, linestyle=(0, (3, 3)))
    ax.set_xlabel("Terminal phenotype diversity (mean pairwise weight-signature distance)")
    ax.set_ylabel("Mean 252-day cumulative net log return")
    ax.set_title("EXP-026: more behavioral diversity did not imply better adaptation",
                 loc="left", color=NAVY, fontsize=13, fontweight="bold")
    legend1 = ax.legend(title="Method mean across families", frameon=False, loc="lower right")
    ax.add_artist(legend1)
    family_handles = [plt.Line2D([0], [0], marker=m, color="none", markerfacecolor=MUTED,
                                 markeredgecolor="white", markersize=7, label=f.replace("_", " ").title())
                      for f, m in markers.items()]
    ax.legend(handles=family_handles, title="Structural family", frameon=False, loc="upper right")
    ax.text(0, -0.19, "Diamonds are method means; circles/squares/triangles are family means. Point size encodes tail loss.",
            transform=ax.transAxes, color=MUTED, fontsize=8.5)
    fig.subplots_adjust(bottom=0.2, top=0.86)
    save(fig, "fig2_diversity_performance_map.png")


def plex_design() -> None:
    fig, ax = plt.subplots(figsize=(10.2, 5.7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.set_title("Digital-asset research design: EVE PLEX venue integration",
                 loc="left", color=NAVY, fontsize=14, fontweight="bold", pad=14)
    ax.text(0, 5.55, "Research-design schematic — not an estimated effect",
            color=RED, fontsize=9.5, fontweight="bold")

    center_pre = np.array([2.0, 3.1])
    angles = np.linspace(0, 2 * np.pi, 12, endpoint=False)
    for i, angle in enumerate(angles):
        radius = 1.05 if i < 8 else 0.68
        p = center_pre + radius * np.array([np.cos(angle), np.sin(angle)])
        ax.plot([center_pre[0], p[0]], [center_pre[1], p[1]], color=GRID, linewidth=0.8)
        ax.scatter(*p, s=34 + 3 * i, color=CYAN, edgecolor="white", linewidth=0.7, zorder=3)
    ax.scatter(*center_pre, s=145, color=NAVY, edgecolor="white", linewidth=1, zorder=4)
    ax.text(2.0, 1.62, "Before pooling\n59 verified regional books\n2,003 orders in sampled snapshot",
            ha="center", va="top", color=INK, fontsize=9.5)

    ax.annotate("July 2025 platform rule\nregional cancellations → global formation",
                xy=(5.15, 3.1), xytext=(3.65, 4.35), ha="center", color=INK,
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2), fontsize=9.5)

    center_post = np.array([7.3, 3.1])
    ax.scatter(*center_post, s=850, color=NAVY, alpha=0.95, edgecolor="white", linewidth=2, zorder=3)
    ax.scatter(*center_post, s=330, color=CYAN, edgecolor="white", linewidth=1.3, zorder=4)
    ax.text(7.3, 1.62, "After pooling\none global book (region 19000001)\n322 orders in sampled snapshot",
            ha="center", va="top", color=INK, fontsize=9.5)

    measures = ["Spread & depth", "Quote-gap diffusion", "Concentration", "Shock resilience"]
    for i, label in enumerate(measures):
        x = 8.65
        y = 4.55 - i * 0.75
        ax.add_patch(plt.Rectangle((x, y - 0.24), 1.2, 0.48, facecolor=PAPER, edgecolor=BLUE, linewidth=1.1))
        ax.text(x + 0.6, y, label, ha="center", va="center", color=NAVY, fontsize=8.5)
        ax.plot([7.85, x], [3.1, y], color=GRID, linewidth=0.8)
    ax.text(0.1, 0.35,
            "Identification boundary: regional dispersion mechanically disappears; the study must target non-mechanical liquidity and adjustment outcomes.\n"
            "Verified archive facts: EVE Ref snapshots on 2025-07-06 and 2025-07-08. Executable in ISK, not a USD-investability claim.",
            color=MUTED, fontsize=8.4, va="bottom")
    save(fig, "fig3_plex_market_integration_design.png")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    evidence_intervals()
    diversity_performance()
    plex_design()
    print(f"figures written to {OUT}")
