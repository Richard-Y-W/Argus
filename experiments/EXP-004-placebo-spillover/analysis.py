"""EXP-004: registered placebo-spillover analysis. Deterministic."""
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from engineering.argus_lab.statistics import hc3_ols  # noqa: E402

RAW = ROOT / "datasets" / "raw"
OUT = Path(__file__).resolve().parent / "results"
OUT.mkdir(exist_ok=True)


def load_data():
    doc = pd.read_csv(RAW / "SignalDoc.csv")
    required = ["Acronym", "Cat.Signal", "Predictability in OP", "SampleStartYear", "SampleEndYear", "Year"]
    doc = doc[required].dropna(subset=["SampleStartYear", "SampleEndYear", "Year"])
    pred_doc = doc[(doc["Cat.Signal"] == "Predictor") & doc["Predictability in OP"].isin(["1_clear", "2_likely"])]
    plac_doc = doc[(doc["Cat.Signal"] == "Placebo")]
    pred = pd.read_parquet(RAW / "PredictorPortsFull.parquet")
    plac = pd.read_parquet(RAW / "PlaceboPortsFull.parquet")
    pred = pred[pred["port"] == "LS"].copy(); plac = plac[plac["port"] == "LS"].copy()
    for frame in [pred, plac]:
        frame["date"] = pd.to_datetime(frame["date"])
        # The two release files use different within-month timestamps.
        frame["date"] = frame["date"].dt.to_period("M").dt.to_timestamp()
        frame.drop(frame[frame["date"] > "2024-12-31"].index, inplace=True)
    pred = pred[pred.signalname.isin(pred_doc.Acronym)].copy()
    plac = plac.merge(plac_doc, left_on="signalname", right_on="Acronym", how="inner")
    y = plac.date.dt.year
    plac["window"] = np.select(
        [y < plac.SampleStartYear, y <= plac.SampleEndYear, y <= plac.Year],
        ["pre", "in_sample", "post_sample"], default="post_pub"
    )
    counts = plac.pivot_table(index="signalname", columns="window", values="ret", aggfunc="count").fillna(0)
    keep = counts.index[(counts.get("in_sample", 0) >= 12) & (counts.get("post_pub", 0) >= 12)]
    return pred, plac[plac.signalname.isin(keep)].copy(), pred_doc.set_index("Acronym")


def max_corr_exposure(plac, pred, pred_doc, years, min_months, future=False):
    pp = pred.pivot(index="date", columns="signalname", values="ret")
    rows = []
    for name, group in plac.groupby("signalname"):
        pub = int(group.Year.iloc[0]); end = pd.Timestamp(pub - 1, 12, 31); start = end - pd.DateOffset(years=years) + pd.DateOffset(days=1)
        s = group.set_index("date").ret.loc[start:end]
        candidates = pred_doc.index[pred_doc.Year > pub] if future else pred_doc.index[pred_doc.Year < pub]
        x = pp.reindex(s.index).reindex(columns=candidates)
        ns = x.notna().mul(s.notna(), axis=0).sum()
        x = x.loc[:, ns >= min_months]
        ns = ns[ns >= min_months]
        corrs = x.corrwith(s).dropna()
        if corrs.empty:
            continue
        chosen = corrs.abs().idxmax()
        rows.append({"signalname": name, "exposure": corrs[chosen], "matched_predictor": chosen, "corr_n": int(ns[chosen])})
    return pd.DataFrame(rows).set_index("signalname")


def composite_exposure(plac, pred, pred_doc, years=5, min_months=36):
    pp = pred.pivot(index="date", columns="signalname", values="ret")
    rows = []
    for name, group in plac.groupby("signalname"):
        pub = int(group.Year.iloc[0]); end = pd.Timestamp(pub - 1, 12, 31); start = end - pd.DateOffset(years=years) + pd.DateOffset(days=1)
        s = group.set_index("date").ret.loc[start:end]
        candidates = pred_doc.index[pred_doc.Year < pub]
        x = pp.reindex(s.index).reindex(columns=candidates)
        composite = x.where(x.notna().sum(axis=1) >= 5).mean(axis=1)
        pair = pd.concat([s.rename("p"), composite.rename("c")], axis=1).dropna()
        if len(pair) >= min_months:
            rows.append({"signalname": name, "exposure": pair.p.corr(pair.c), "matched_predictor": "published_composite", "corr_n": len(pair)})
    return pd.DataFrame(rows).set_index("signalname")


def outcomes(plac):
    means = plac.pivot_table(index="signalname", columns="window", values="ret", aggfunc="mean")
    meta = plac.groupby("signalname").agg(pub_year=("Year", "first"))
    out = meta.join(means[["in_sample", "post_pub"]]).dropna()
    out["change"] = out.post_pub - out.in_sample
    return out


def regression(out, exposure, label):
    q = out.join(exposure, how="inner").copy()
    q = q.dropna(subset=["change", "exposure", "corr_n"])
    if q.empty:
        raise ValueError(f"{label}: no usable joined observations")
    cols = []
    for col in ["exposure", "in_sample", "pub_year", "corr_n"]:
        if q[col].std() > 0:
            q[col + "_z"] = (q[col] - q[col].mean()) / q[col].std()
            cols.append(col + "_z")
    result = hc3_ols(q.change, q[cols])
    table = pd.DataFrame({"spec": label, "term": result.params.index, "coef": result.params.values, "se": result.bse.values, "t": result.tvalues.values, "n": len(q)})
    return q, table


def main():
    pred, plac, pred_doc = load_data(); out = outcomes(plac)
    primary = max_corr_exposure(plac, pred, pred_doc, 5, 36)
    future = max_corr_exposure(plac, pred, pred_doc, 5, 36, future=True)
    long_window = max_corr_exposure(plac, pred, pred_doc, 10, 60)
    composite = composite_exposure(plac, pred, pred_doc)
    print(f"eligible placebos={out.shape[0]}, primary exposures={len(primary)}, "
          f"future controls={len(future)}, 120m={len(long_window)}, composite={len(composite)}")
    specs = []
    q, tab = regression(out, primary, "primary_maxcorr_60m"); specs.append(tab)
    _, tab = regression(out, future, "negative_control_future"); specs.append(tab)
    _, tab = regression(out, long_window, "R1_maxcorr_120m"); specs.append(tab)
    _, tab = regression(out, composite, "R2_published_composite"); specs.append(tab)
    regs = pd.concat(specs, ignore_index=True); regs.to_csv(OUT / "regressions.csv", index=False)
    q["tercile"] = pd.qcut(q.exposure, 3, labels=["low", "middle", "high"])
    terc = q.groupby("tercile", observed=True).agg(n=("change", "size"), exposure=("exposure", "mean"), change=("change", "mean"), in_sample=("in_sample", "mean"), post_pub=("post_pub", "mean"))
    terc.to_csv(OUT / "terciles.csv")
    primary.add_prefix("primary_").join(future.add_prefix("future_"), how="outer").join(out, how="left").to_csv(OUT / "exposures.csv")
    print(regs.round(3).to_string(index=False)); print("\nTerciles\n", terc.round(3).to_string())


if __name__ == "__main__":
    main()
