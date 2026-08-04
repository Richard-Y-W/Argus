"""EXP-029 figures from archived outputs."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"


def main() -> None:
    daily = pd.read_csv(OUT / "daily_returns.csv", parse_dates=["date"])
    comparisons = pd.read_csv(OUT / "comparisons.csv")
    decisions = pd.read_csv(OUT / "decisions.csv", parse_dates=["date"])
    confirmation = daily.query("period == 'confirmation'")
    controller = decisions.query("period == 'confirmation' and method == 'controller'")
    colors = {"controller": "#7B2CBF", "localized": "#1B9E77", "random": "#D95F02",
              "all_gene": "#E7298A", "min_variance": "#377EB8", "equal_weight": "#555555"}
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))
    for method, group in confirmation.groupby("method"):
        group = group.sort_values("date")
        axes[0].plot(group.date, (1 + group.net_return).cumprod(), label=method.replace("_", " "),
                     color=colors[method], linewidth=1.5)
    axes[0].set_title("2005–2024 walk-forward net wealth")
    axes[0].set_ylabel("Growth of $1")
    axes[0].grid(alpha=0.2)
    axes[0].legend(fontsize=7)

    counts = controller.route.value_counts(normalize=True).reindex(["tolerate", "localized", "systemic"])
    axes[1].bar(counts.index, counts.values, color=["#777777", "#1B9E77", "#D95F02"])
    axes[1].axhline(0.05, color="black", linestyle="--", linewidth=1, label="registered 5% minimum")
    axes[1].set_title("Immune-controller route shares")
    axes[1].set_ylabel("Fraction of evaluation months")
    axes[1].tick_params(axis="x", rotation=20)
    axes[1].legend(fontsize=7)

    y = range(len(comparisons))
    axes[2].errorbar(comparisons.mean_monthly_ce_difference, y,
                     xerr=[comparisons.mean_monthly_ce_difference - comparisons.ci_low,
                           comparisons.ci_high - comparisons.mean_monthly_ce_difference],
                     fmt="o", color="#7B2CBF", capsize=4)
    axes[2].axvline(0, color="black", linewidth=1)
    axes[2].set_yticks(list(y), comparisons.comparator.str.replace("_", " "))
    axes[2].set_title("Controller minus comparator\npaired block-bootstrap intervals")
    axes[2].set_xlabel("Mean monthly certainty equivalent")
    axes[2].grid(axis="x", alpha=0.2)
    fig.suptitle("EXP-029: danger routing restores the immune architecture, not an edge", fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT / "exp029_immune_controller.png", dpi=180, bbox_inches="tight")
    fig.savefig(OUT / "exp029_immune_controller.pdf", bbox_inches="tight")
    print("EXP-029 figures written")


if __name__ == "__main__":
    main()

