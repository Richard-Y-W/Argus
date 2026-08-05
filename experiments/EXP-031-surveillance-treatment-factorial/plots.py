"""EXP-031 figures from archived outputs."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"


def main() -> None:
    outcomes = pd.read_csv(OUT / "seed_outcomes.csv")
    comparisons = pd.read_csv(OUT / "comparisons.csv")
    means = outcomes.groupby("policy").mean(numeric_only=True)
    order = ["breach_proportional", "breach_targeted", "early_proportional", "early_targeted"]
    colors = ["#1B9E77", "#7B2CBF", "#66C2A5", "#B565D9"]
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))
    axes[0].bar(range(4), means.loc[order, "violation_area"], color=colors)
    axes[0].set_xticks(range(4), [x.replace("_", "\n") for x in order])
    axes[0].set_ylabel("Invariant-violation area")
    axes[0].set_title("Early warning improves safety\nunder either treatment")

    axes[1].bar(range(4), means.loc[order, "healthy_reduction"], color=colors)
    axes[1].set_xticks(range(4), [x.replace("_", "\n") for x in order])
    axes[1].set_ylabel("Healthy-module exposure reduction")
    axes[1].set_title("Targeting preserves healthy modules")

    treatment = comparisons.query("estimand.str.startswith('treatment')", engine="python").reset_index(drop=True)
    labels = [f"{row.metric.replace('_', ' ')}\n{row.estimand.replace('_', ' ')}" for row in treatment.itertuples()]
    y = range(len(treatment))
    axes[2].errorbar(treatment.estimate, y,
                     xerr=[treatment.estimate - treatment.ci_low, treatment.ci_high - treatment.estimate],
                     fmt="o", color="#7B2CBF", capsize=4)
    axes[2].axvline(0, color="black", linewidth=1)
    axes[2].set_yticks(list(y), labels, fontsize=8)
    axes[2].set_xlabel("Targeted minus proportional")
    axes[2].set_title("Paired treatment contrasts")
    axes[2].grid(axis="x", alpha=0.2)
    fig.suptitle("EXP-031: surveillance drives safety; localization reduces collateral action", fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT / "exp031_factorial_defense.png", dpi=180, bbox_inches="tight")
    fig.savefig(OUT / "exp031_factorial_defense.pdf", bbox_inches="tight")
    print("EXP-031 figures written")


if __name__ == "__main__":
    main()

