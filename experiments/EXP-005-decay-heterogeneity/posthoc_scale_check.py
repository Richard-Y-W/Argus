"""EXP-005 post-hoc diagnostic — NOT REGISTERED in design.md.

Motivation (visible in the registered tercile output): proportional decay is
roughly flat (~50%) across op_t terciles, while in-sample means rise steeply.
Under pure proportional decay, post_pub = theta * is_mean, so the absolute
decline is (1-theta)*is_mean, and any characteristic correlated with is_mean
inherits a "significant" levels interaction with no mechanism of its own.

Diagnostic: add (ps, pp) x z(is_mean) to the registered E1 spec. If the
is_mean interaction absorbs op_t and vol, the levels heterogeneity is scale,
not characteristic-specific mechanism. Interpreted as exploratory only.
"""

from pathlib import Path

import pandas as pd

import analysis  # registered machinery; this script only adds one regressor

OUT = Path(__file__).resolve().parent / "results"


def main() -> None:
    df, _ = analysis.load_panel()
    ch = analysis.characteristics(df)
    ch["is_mean_z"] = (ch["is_mean"] - ch["is_mean"].mean()) / ch["is_mean"].std()

    d, xcols = analysis.with_interactions(df, ch, ["op_t", "vol"])
    m = ch["is_mean_z"]
    d = d.merge(m.rename("is_mean_z"), left_on="signalname", right_index=True)
    d["ps_x_ismean"] = d["ps"] * d["is_mean_z"]
    d["pp_x_ismean"] = d["pp"] * d["is_mean_z"]
    tab = analysis.fe_reg(d, xcols + ["ps_x_ismean", "pp_x_ismean"])
    tab.to_csv(OUT / "posthoc_scale_check.csv", index=False)
    print("== post-hoc: E1 + (ps,pp) x z(is_mean) — NOT REGISTERED ==")
    print(tab.round(3).to_string(index=False))

    # Solo is_mean for reference
    d2, x2 = analysis.with_interactions(df, ch, ["op_t"])  # base windows
    d2 = d2.merge(m.rename("is_mean_z"), left_on="signalname", right_index=True)
    d2["ps_x_ismean"] = d2["ps"] * d2["is_mean_z"]
    d2["pp_x_ismean"] = d2["pp"] * d2["is_mean_z"]
    tab2 = analysis.fe_reg(d2, ["ps", "pp", "ps_x_ismean", "pp_x_ismean"])
    tab2.to_csv(OUT / "posthoc_scale_check_solo.csv", index=False)
    print("\n== post-hoc: windows + (ps,pp) x z(is_mean) only ==")
    print(tab2.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
