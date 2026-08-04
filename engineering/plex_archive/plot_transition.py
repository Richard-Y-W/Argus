"""Descriptive transition figure from pinned, hashed PLEX snapshot summaries."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).parent
OUT = HERE / "results"
NAVY, BLUE, ORANGE, GREEN = "#17365D", "#5B9BD5", "#ED7D31", "#70AD47"
MUTED, GRID, PAPER = "#666666", "#D9E1F2", "#FAFBFD"

plt.rcParams.update({
    "figure.dpi": 160, "savefig.dpi": 240, "font.family": "DejaVu Sans",
    "font.size": 9.5, "axes.facecolor": PAPER, "figure.facecolor": "white",
    "axes.grid": True, "grid.color": GRID, "axes.spines.top": False,
    "axes.spines.right": False,
})


def main() -> None:
    boundary = pd.read_csv(OUT / "transition_july7_summary.csv")
    formation = pd.read_csv(OUT / "transition_formation_summary.csv")
    data = pd.concat([boundary, formation], ignore_index=True)
    data["file_time"] = pd.to_datetime(data.file_time, utc=True)
    data = data.sort_values("file_time")
    labels = data.file_time.dt.strftime("%H:%M")
    colors = [BLUE, ORANGE, GREEN, GREEN]
    fig, ax = plt.subplots(figsize=(9.2, 5.2))
    bars = ax.bar(labels, data.plex_orders, color=colors, width=0.62, edgecolor="white")
    for bar, (_, row) in zip(bars, data.iterrows()):
        regime = (f"{int(row.distinct_plex_regions)} regions" if row.distinct_plex_regions > 1
                  else ("empty PLEX book" if row.plex_orders == 0 else "global region 19000001"))
        ax.annotate(f"{int(row.plex_orders):,} orders\n{regime}",
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    xytext=(0, 7), textcoords="offset points", ha="center", va="bottom",
                    color=NAVY, fontweight="bold", fontsize=9)
    ax.set_ylabel("Displayed PLEX orders in full-market snapshot")
    ax.set_xlabel("2025-07-07 UTC snapshot time")
    ax.set_ylim(0, 2200)
    ax.set_title("PLEX transition reconstructed from complete archived order books",
                 loc="left", color=NAVY, fontsize=13, fontweight="bold")
    ax.text(0.5, 0.57, "regional cancellation\ninterval", transform=ax.transAxes,
            ha="center", color=ORANGE, fontsize=9)
    ax.annotate("", xy=(0.585, 0.52), xytext=(0.415, 0.52), xycoords="axes fraction",
                arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=1.6))
    ax.text(0, -0.22,
            "Descriptive transition evidence, not an economic effect. Raw full-market archives were hashed and deleted after streaming.\n"
            "Cancellation: (10:45:07, 11:15:07]; first observed global formation: (11:15:07, 11:45:08]. Source: EVE Ref.",
            transform=ax.transAxes, color=MUTED, fontsize=8.5)
    ax.grid(axis="x", visible=False)
    fig.subplots_adjust(bottom=0.24, top=0.83)
    fig.savefig(OUT / "fig_plex_transition_sequence.png", bbox_inches="tight")
    fig.savefig(OUT / "fig_plex_transition_sequence.pdf", bbox_inches="tight")
    plt.close(fig)
    print("transition figure written")


if __name__ == "__main__":
    main()

