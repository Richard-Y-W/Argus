"""EXP-030 figures from archived outputs."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"


def main() -> None:
    outcomes = pd.read_csv(OUT / "seed_outcomes.csv")
    summary = outcomes.groupby("policy").mean(numeric_only=True)
    family = pd.read_csv(OUT / "family_breadth.csv")
    colors = {"immune": "#7B2CBF", "proportional": "#1B9E77", "vol_target": "#377EB8",
              "liquidate": "#D95F02", "none": "#777777"}
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.7))
    order = ["immune", "proportional", "vol_target", "liquidate", "none"]
    axes[0].bar(order, summary.loc[order, "violation_area"], color=[colors[x] for x in order])
    axes[0].set_yscale("symlog", linthresh=0.01)
    axes[0].set_title("Invariant-violation area\n(lower is safer; symlog scale)")
    axes[0].tick_params(axis="x", rotation=25)

    for policy in order:
        axes[1].scatter(summary.loc[policy, "healthy_reduction"], summary.loc[policy, "violation_area"],
                        s=70, color=colors[policy], label=policy.replace("_", " "))
    axes[1].set_yscale("symlog", linthresh=0.01)
    axes[1].set_xlabel("Healthy-module exposure reduction")
    axes[1].set_ylabel("Invariant-violation area")
    axes[1].set_title("Safety versus collateral intervention")
    axes[1].grid(alpha=0.2)
    axes[1].legend(fontsize=7)

    x = range(len(family))
    axes[2].bar([i - 0.18 for i in x], family.immune_mean, width=0.36, color=colors["immune"], label="immune")
    axes[2].bar([i + 0.18 for i in x], family.proportional_mean, width=0.36,
                color=colors["proportional"], label="proportional")
    axes[2].set_xticks(list(x), family.family.str.replace("_", " "), rotation=30, ha="right")
    axes[2].set_title("Targeted defense beat proportional\nin every pathology family")
    axes[2].set_ylabel("Invariant-violation area")
    axes[2].legend(fontsize=8)
    fig.suptitle("EXP-030: targeted containment works, but does not dominate conventional defense", fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT / "exp030_invariant_defense.png", dpi=180, bbox_inches="tight")
    fig.savefig(OUT / "exp030_invariant_defense.pdf", bbox_inches="tight")
    print("EXP-030 figures written")


if __name__ == "__main__":
    main()

