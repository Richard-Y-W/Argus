"""EXP-015: construction-matched world versus world-ex-US publication decay."""
from pathlib import Path
import re
import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[2]
RETURNS = ROOT / "datasets/raw/jkp_global/[all_regions]_[all_factors]_[monthly]_[vw].csv"
METADATA = ROOT / "datasets/raw/jkp_factor_details.xlsx"
OUT = Path(__file__).parent / "results"

def metadata():
    raw = pd.read_excel(METADATA, sheet_name="details"); rows=[]
    for _, r in raw.iterrows():
        yrs=[int(x) for x in re.findall(r"(?<!\d)(?:18|19|20)\d{2}(?!\d)", str(r.get("in-sample period", "")))]; pubs=re.findall(r"\(((?:18|19|20)\d{2})\)", str(r.get("cite", "")))
        if pd.notna(r.get("abr_jkp")) and yrs and pubs:
            rows.append({"name":r["abr_jkp"], "sample_start":yrs[0], "sample_end":yrs[-1], "publication_year":int(pubs[-1]), "significance":pd.to_numeric(r.get("significance"), errors="coerce")})
    d=pd.DataFrame(rows); d=d[d.publication_year >= d.sample_end]; return d.drop_duplicates("name", keep=False)

def panel():
    d=pd.read_csv(RETURNS, usecols=["location","name","date","ret"]); d=d[d.location.isin(["world","world_ex_us"])].merge(metadata(), on="name", validate="many_to_one")
    d["date"]=pd.to_datetime(d.date); y=d.date.dt.year; d=d[y >= d.sample_start].copy(); y=d.date.dt.year
    d["window"]=np.select([y <= d.sample_end, y <= d.publication_year], ["in_sample","post_sample"], default="post_pub")
    c=d.groupby(["location","name","window"]).size().unstack(fill_value=0)
    for col in ["in_sample","post_pub"]:
        if col not in c: c[col]=0
    eligible=c[(c.in_sample>=12)&(c.post_pub>=12)].reset_index(); common=set(eligible.groupby("name").filter(lambda x: len(x)==2).name)
    return d[d.name.isin(common)].copy()

def estimate(d, spec):
    d=d.copy(); d["ps"]=(d.window=="post_sample").astype(float); d["pp"]=(d.window=="post_pub").astype(float)
    y=d.ret-d.groupby("name").ret.transform("mean"); x=d[["ps","pp"]]-d.groupby("name")[["ps","pp"]].transform("mean")
    fit=sm.OLS(y,x).fit(cov_type="cluster",cov_kwds={"groups":d.date}); a=np.array([-1.,1.]); diff=float(a@fit.params); se=float(np.sqrt(a@fit.cov_params()@a))
    return {"spec":spec,"factors":d.name.nunique(),"observations":len(d),"post_sample":fit.params.ps,"post_sample_t":fit.tvalues.ps,"post_pub":fit.params.pp,"post_pub_t":fit.tvalues.pp,"postpub_minus_postsample":diff,"contrast_t":diff/se}

def factor_changes(d):
    w=d.groupby(["location","name","window"]).ret.mean().unstack(); w["change"]=w.post_pub-w.in_sample
    return w.reset_index()

def main():
    d=panel(); rows=[estimate(d[d.location==x],x) for x in ["world","world_ex_us"]]
    paired=d.pivot_table(index=["name","date","window","significance"],columns="location",values="ret").dropna().reset_index(); paired["ret"]=paired.world-paired.world_ex_us
    rows.append(estimate(paired,"world_minus_world_ex_us")); sig=d[d.significance==1]; rows += [estimate(sig[sig.location==x],x+"_significant") for x in ["world","world_ex_us"]]
    estimates=pd.DataFrame(rows); changes=factor_changes(d); means=changes.groupby("location").change.mean(); breadth=float((changes[changes.location=="world"].change<0).mean())
    e=estimates.set_index("spec"); gap=e.loc["world"].post_pub-e.loc["world_ex_us"].post_pub; sig_gap=e.loc["world_significant"].post_pub-e.loc["world_ex_us_significant"].post_pub; ew_gap=means["world"]-means["world_ex_us"]
    verdicts={"P1":bool(e.loc["world"].post_pub<0 and abs(e.loc["world"].post_pub_t)>=2 and gap<=-.0005),"P2":bool(e.loc["world"].postpub_minus_postsample<0 and abs(e.loc["world"].contrast_t)>=1.65),"P3":bool(breadth>.55),"P4":bool(sig_gap<0 and ew_gap<0)}; falsifier=bool(e.loc["world"].post_pub>=0 or gap>=0 or ew_gap>=0)
    OUT.mkdir(exist_ok=True); estimates.to_csv(OUT/"estimates.csv",index=False); changes.to_csv(OUT/"factor_changes.csv",index=False); pd.DataFrame([{**verdicts,"panel_gap":gap,"equal_factor_gap":ew_gap,"world_negative_breadth":breadth,"falsifier":falsifier}]).to_csv(OUT/"summary.csv",index=False)
    log="\n".join([*(f"{k}={v}" for k,v in verdicts.items()),f"falsifier={falsifier}"]); (OUT/"run_log.txt").write_text(log+"\n",encoding="utf-8"); print(estimates.to_string(index=False)); print(f"panel_gap={gap:.6f} equal_factor_gap={ew_gap:.6f} breadth={breadth:.4f}\n{log}")

if __name__=="__main__": main()
