"""EXP-010: paired within-signal EW/VW publication-decay comparison."""
from pathlib import Path
import sys
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from engineering.argus_lab.data import assign_event_windows, load_signal_doc, normalize_month

RAW = ROOT / "datasets" / "raw"
OUT = Path(__file__).parent / "results"
PANEL_END = pd.Timestamp("2024-12-01")


def load_weighting(name):
    frame = pd.read_parquet(RAW / f"deciles_{name}.parquet")
    frame = frame[frame["port"] == "LS"].copy()
    frame["date"] = normalize_month(frame["date"])
    frame = frame[frame["date"] <= PANEL_END]
    return frame[["signalname", "date", "ret"]].rename(columns={"ret": f"ret_{name}"})


def paired_sample():
    doc = load_signal_doc(RAW)
    doc = doc[(doc["Cat.Signal"] == "Predictor") & doc["Predictability in OP"].isin(["1_clear", "2_likely"])]
    doc = doc.dropna(subset=["SampleStartYear", "SampleEndYear", "Year"])
    monthly = load_weighting("ew").merge(load_weighting("vw"), on=["signalname", "date"], how="inner", validate="one_to_one")
    monthly = monthly.merge(doc[["Acronym", "Predictability in OP", "SampleStartYear", "SampleEndYear", "Year"]], left_on="signalname", right_on="Acronym", validate="many_to_one")
    flow = {"eligible_metadata_signals": doc["Acronym"].nunique(), "paired_monthly_signals": monthly["signalname"].nunique()}
    monthly["window"] = assign_event_windows(monthly)
    monthly = monthly[monthly["window"] != "pre_sample"]
    stats_by_signal = monthly.groupby(["signalname", "window"])[["ret_ew", "ret_vw"]].agg(["mean", "count"]).unstack("window")
    rows = []
    for signal, row in stats_by_signal.iterrows():
        try:
            item = {"signalname": signal}
            for weight in ("ew", "vw"):
                item[f"is_mean_{weight}"] = row[(f"ret_{weight}", "mean", "in_sample")]
                item[f"pp_mean_{weight}"] = row[(f"ret_{weight}", "mean", "post_pub")]
                item[f"is_n_{weight}"] = row[(f"ret_{weight}", "count", "in_sample")]
                item[f"pp_n_{weight}"] = row[(f"ret_{weight}", "count", "post_pub")]
            rows.append(item)
        except KeyError:
            continue
    paired = pd.DataFrame(rows).merge(doc[["Acronym", "Predictability in OP", "Year"]], left_on="signalname", right_on="Acronym", validate="one_to_one")
    flow["signals_with_both_windows"] = len(paired)
    eligible_months = (paired[["is_n_ew", "is_n_vw", "pp_n_ew", "pp_n_vw"]] >= 12).all(axis=1)
    flow["signals_with_min_months"] = int(eligible_months.sum())
    eligible = eligible_months & (paired[["is_mean_ew", "is_mean_vw"]] > 0.10).all(axis=1)
    flow["primary_signals"] = int(eligible.sum())
    paired = paired[eligible].copy()
    for weight in ("ew", "vw"):
        paired[f"decay_{weight}"] = (paired[f"is_mean_{weight}"] - paired[f"pp_mean_{weight}"]) / paired[f"is_mean_{weight}"]
    paired["decay_diff_vw_minus_ew"] = paired["decay_vw"] - paired["decay_ew"]
    paired["levels_did"] = (paired["pp_mean_vw"] - paired["is_mean_vw"]) - (paired["pp_mean_ew"] - paired["is_mean_ew"])
    return paired.sort_values("signalname"), flow


def summarize(values, spec, metric):
    values = pd.Series(values).dropna()
    n = len(values)
    mean = values.mean()
    se = values.std(ddof=1) / np.sqrt(n)
    tstat = mean / se
    critical = stats.t.ppf(0.975, n - 1)
    return {"spec": spec, "metric": metric, "n": n, "mean": mean, "se": se, "t": tstat, "ci_low": mean - critical * se, "ci_high": mean + critical * se, "median": values.median(), "positive_share": (values > 0).mean()}


def main():
    OUT.mkdir(exist_ok=True)
    paired, flow = paired_sample()
    primary = paired["decay_diff_vw_minus_ew"]
    clipped = primary.clip(primary.quantile(0.05), primary.quantile(0.95))
    clear = paired.loc[paired["Predictability in OP"] == "1_clear", "decay_diff_vw_minus_ew"]
    summary = pd.DataFrame([
        summarize(primary, "primary", "decay_vw_minus_ew"),
        summarize(paired["levels_did"], "secondary_levels_did", "levels_did"),
        summarize(clipped, "robust_winsor_5_95", "decay_vw_minus_ew"),
        summarize(clear, "robust_clear_only", "decay_vw_minus_ew"),
    ])
    paired.to_csv(OUT / "paired_signals.csv", index=False)
    summary.to_csv(OUT / "summary.csv", index=False)
    pd.DataFrame([flow]).to_csv(OUT / "sample_flow.csv", index=False)
    tails = paired.nsmallest(5, "decay_diff_vw_minus_ew")[["signalname", "decay_diff_vw_minus_ew"]]
    tails = pd.concat([tails, paired.nlargest(5, "decay_diff_vw_minus_ew")[["signalname", "decay_diff_vw_minus_ew"]]])
    log = "SAMPLE FLOW\n" + pd.Series(flow).to_string() + "\n\nSUMMARY\n" + summary.to_string(index=False, float_format=lambda x: f"{x:.6f}") + "\n\nFIVE LOWEST / HIGHEST PRIMARY DIFFERENCES\n" + tails.to_string(index=False)
    (OUT / "run_log.txt").write_text(log + "\n", encoding="utf-8")
    print(log)


if __name__ == "__main__":
    main()
