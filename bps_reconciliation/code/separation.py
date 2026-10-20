"""Step 1e / Step 2: couples lost to separation at BPS's composition break (2026-10-18).

Reads BPS's psid_cons.dta (shipped, read only; work copy) and build_flags.py's flags. For each married-couple row
(marit 1, wife present, male head 30-57 = age - 1, head in IGE's person file) finds the same head's next interview
(two years later) and classifies: same wife / separated or new wife (marit != 1 or another wife pid) / head not
observed. BPS drop the year of the change (fchg > 1) and restart the household as a new unit, so a couple whose
marriage ends after a displacement contributes no difference across the separation. Reports the shares by the
couple-year's displacement status (husband only, wife only, joint, none) with s.e. clustered by head (linear
probability), and the counts of couples and couple-years lost.
Usage: python separation.py <work dir>   -> <work>/separation.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


def main(work):
    work = Path(work)
    b = pd.read_stata(work / "psid_cons.dta", columns=["year", "id", "marit", "agew", "sex", "age", "fchg", "seo"],
                      convert_categoricals=False)
    f = pd.read_csv(work / "flags.csv")
    d = b.merge(f, on=["year", "id"], how="left")
    d = d[d["h_pid"] > 0].sort_values(["h_pid", "year"])
    nxt = d[["h_pid", "year", "marit", "w_pid", "fchg"]].copy()
    nxt["year"] = nxt["year"] - 2
    nxt.columns = ["h_pid", "year", "n_marit", "n_w_pid", "n_fchg"]
    d = d.merge(nxt, on=["h_pid", "year"], how="left")
    U = d[(d["marit"] == 1) & (d["agew"] > 0) & (d["sex"] == 1) & d["age"].sub(1).between(30, 57) &
          (d["w_pid"] > 0) & (d["year"] <= 106)].copy()
    U["observed_next"] = U["n_marit"].notna()
    U["sep"] = (U["observed_next"] & ((U["n_marit"] != 1) | (U["n_w_pid"] != U["w_pid"]))).astype(float)
    U["sep_obs"] = U["sep"].where(U["observed_next"])
    U["bps_break_next"] = (U["n_fchg"] > 1).astype(float).where(U["observed_next"])
    U["grp"] = np.select([(U["hd"] == 1) & (U["wd"] == 0), (U["wd"] == 1) & (U["hd"] == 0), U["jd"] == 1],
                         ["h_only", "w_only", "joint"], "none")
    rows = []
    for samp, S in (("SRC+SEO", U), ("SRC (BPS)", U[U["seo"] == 0])):
        for y in ("sep_obs", "bps_break_next"):
            X = S.dropna(subset=[y]).copy()
            m = smf.ols(f"{y} ~ C(grp, Treatment('none'))", data=X).fit(cov_type="cluster",
                                                                          cov_kwds={"groups": X["h_pid"]})
            for g in ("none", "h_only", "w_only", "joint"):
                rows.append(dict(sample=samp, outcome=y, group=g, mean=X.loc[X["grp"] == g, y].mean(),
                                 n=int((X["grp"] == g).sum()), events=int(X.loc[X["grp"] == g, y].sum())))
            for g in ("h_only", "w_only", "joint"):
                k = f"C(grp, Treatment('none'))[T.{g}]"
                rows.append(dict(sample=samp, outcome=y, group=f"diff {g}-none", mean=m.params[k], se=m.bse[k],
                                 p=m.pvalues[k], n=int(m.nobs)))
        rows.append(dict(sample=samp, outcome="couples_ending_in_separation", group="all",
                         n=int(S.loc[S["sep"] == 1, ["h_pid", "w_pid"]].drop_duplicates().shape[0])))
        rows.append(dict(sample=samp, outcome="couples_ending_in_separation", group="any displacement before",
                         n=int(S.loc[(S["sep"] == 1) & ((S["hd"] == 1) | (S["wd"] == 1)),
                                     ["h_pid", "w_pid"]].drop_duplicates().shape[0])))
        rows.append(dict(sample=samp, outcome="couples", group="all",
                         n=int(S[["h_pid", "w_pid"]].drop_duplicates().shape[0])))
    out = pd.DataFrame(rows)
    out.to_csv(work / "separation.csv", index=False)
    print(out.round(4).to_string())


if __name__ == "__main__":
    main(sys.argv[1])
