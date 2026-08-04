"""Generate EXP-028 figures strictly from archived outputs."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"


def main() -> None:
    daily = pd.read_csv(OUT / "daily_returns.csv", parse_dates=["date"])
    comparisons = pd.read_csv(OUT / "comparisons.csv")
    colors = {"localized": "#7B2CBF", "all_gene": "#D95F02", "random": "#1B9E77",
              "min_variance": "#377EB8", "equal_weight": "#555555"}
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.8))
    for period, style in (("confirmation", "-"), ("later_vintage", "--")):
        subset = daily.query("period == @period")
        for method, group in subset.groupby("method"):
            wealth = (1 + group.sort_values("date")["net_return"]).cumprod()
            axes[0].plot(group.sort_values("date")["date"], wealth, linestyle=style,
                         color=colors[method], linewidth=1.6,
                         label=f"{method.replace('_', ' ')} — {period.replace('_', ' ')}")
    axes[0].axvline(pd.Timestamp("2025-01-01"), color="black", linewidth=0.8, alpha=0.5)
    axes[0].set_title("Walk-forward net wealth\nsolid: frozen 2015–2024; dashed: separate 2025+ check")
    axes[0].set_ylabel("Growth of $1 within each period")
    axes[0].grid(alpha=0.2)
    axes[0].legend(fontsize=7, ncol=2)

    y = range(len(comparisons))
    axes[1].errorbar(comparisons["mean_monthly_ce_difference"], y,
                     xerr=[comparisons["mean_monthly_ce_difference"] - comparisons["ci_low"],
                           comparisons["ci_high"] - comparisons["mean_monthly_ce_difference"]],
                     fmt="o", color="#7B2CBF", capsize=4)
    axes[1].axvline(0, color="black", linewidth=0.9)
    axes[1].set_yticks(list(y), comparisons["comparator"].str.replace("_", " "))
    axes[1].set_xlabel("Localized minus comparator\nmean monthly certainty equivalent")
    axes[1].set_title("Primary paired block-bootstrap intervals")
    axes[1].grid(axis="x", alpha=0.2)
    fig.suptitle("EXP-028: modular repair shows a narrow sub-result, not a joint pass", fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT / "exp028_modular_repair.png", dpi=180, bbox_inches="tight")
    fig.savefig(OUT / "exp028_modular_repair.pdf", bbox_inches="tight")
    print("EXP-028 figures written")


if __name__ == "__main__":
    main()

