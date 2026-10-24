r"""Parental income at a fixed parental age, the income cap, and attrition (committee memo K3 + K4, 2026-10-24)

K3 (Nybom and Stuhler 2016, 2017): the bias from measuring the parent's income at the wrong age can be as large as the
child's. The baseline measures parental income over the son's 13-19, so at different parental ages across families; a
quartic in the head's age at 16 controls only the mean. And both sides drop yearly amounts outside $100-$150,000 of
1967 (6.IGEMain.py), which trims the top.
K4: 42 percent of White and 60 percent of Black sons are gone by 45-49; inverse-probability weights correct on
observables only.
DESIGNS (75's baseline sample, son-years with a valid wage; 113's band estimator: single-age dummies, PSID weights,
clusters 1968 family; IGE of ln earnings at 25-29, 45-49 and the change):
  1. baseline;
  2. sons whose parental head was 40-50 in every income year of the son's 13-19 (head's age at each child wave);
  3. parental income re-measured at the FATHER's ages 40-50 (mean family income of his unit as head over the waves in
     which he is 40-50, >= 3 years in bounds), whatever the son's age; father-present sons, and the baseline on the same
     sons;
  4. the cap: share of parental child-years and of son-years above $150,000 of 1967; the profile with parental income
     and son's earnings without the upper bound (lower bound and the hours / wage screen kept);
  5. attrition: sons observed in each band as a share of those observed at 25-29; the 25-29 IGE of sons later observed
     at 45-49 against all sons at 25-29 (one stacked regression, same son-years).
Writes output/parent_age_cap_attrition.md / .json (aggregates only). DESCRIPTIVE.
"""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import DATA, OUT  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R113 = _load("s113", "113.BaselineProfile.py")
R75, R24 = R113.R75, R113.R75.R24
c, fit = R113.c, R113.fit
RES = {}


def profile(d, y="ly"):
    P = fit(d, y)
    hi = "45-49" if P.has("45-49") else "40-44"
    a, b = P.lin([("25-29", "x", 1)]), P.lin([(hi, "x", 1)])
    ch = P.lin([(hi, "x", 1), ("25-29", "x", -1)])
    return a, b, ch, hi, int(d["pid"].nunique())


def main():
    r = R75.build()
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    sons = r.drop_duplicates("pid")[["pid", "fpid", "birth_year"]]
    k = py[py["child"] & py["age"].between(13, 19) & py["pid"].isin(sons["pid"])][["pid", "wave", "age", "hage", "faminc"]]
    g = k[k["faminc"].between(R24.LO, R24.HI)].groupby("pid")["hage"]
    fixed = (g.min() >= 40) & (g.max() <= 50)
    # parental income at the father's 40-50
    fy = py[py["head"] & py["pid"].isin(sons["fpid"].dropna()) & py["age"].between(40, 50)
            & py["faminc"].between(R24.LO, R24.HI)][["pid", "faminc"]].groupby("pid")["faminc"].agg(["mean", "count"])
    fy = fy[fy["count"] >= 3]
    lyp40 = sons.dropna(subset=["fpid"]).assign(lyp40=lambda s: np.log(s["fpid"].map(fy["mean"])))[["pid", "lyp40"]]
    # uncapped parental income
    kk = k[k["faminc"] >= R24.LO].groupby("pid")["faminc"].agg(["mean", "count"])
    lyp_nc = np.log(kk["mean"].where(kk["count"] >= 3)).rename("lyp_nc")
    cap_par = float((k["faminc"] > R24.HI).mean())
    r = r.merge(lyp40, on="pid", how="left").merge(lyp_nc, left_on="pid", right_index=True, how="left")
    a = pd.read_pickle(R24.CACHE)[["pid", "wave", "earn", "hours"]].drop_duplicates(["pid", "wave"])
    r = r.merge(a.rename(columns={"earn": "earn_raw", "hours": "hours_raw"}), on=["pid", "wave"], how="left")
    v = r[r["lw"].notna()].copy()
    md = ["# Parental income at a fixed parental age, the income cap, and attrition (committee memo K3 + K4)", "",
          "Built by `125.ParentAgeCapAttrition.py` (2026-10-24); design in its docstring. IGE of ln earnings; estimate "
          "(s.e.; p) clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1.", "",
          "## K3. Parental age and the cap", "", "| specification | 25-29 | oldest band | change | sons |",
          "|---|---|---|---|---|"]

    def row(lab, d, y="ly"):
        a_, b_, ch, hi, n = profile(d, y)
        md.append(f"| {lab} | {c(a_)} | {c(b_)} ({hi}) | {c(ch)} | {n:,} |")
        RES[lab] = {"a": list(map(float, a_)), "b": list(map(float, b_)), "ch": list(map(float, ch)), "hi": hi, "sons": n}
        print(md[-1], flush=True)

    row("baseline", v)
    row("parental head 40-50 in every window year", v[v["pid"].map(fixed).fillna(False).astype(bool)])
    q = v.dropna(subset=["lyp40"])
    row("father-present sons with income at the father's 40-50: baseline income", q)
    row("same sons: parental income at the father's 40-50", q.assign(lyp=q["lyp40"]))
    # uncapped
    nc = r.copy()
    e, h = nc["earn_raw"], nc["hours_raw"]
    okn = (e >= R24.LO) & (h >= R24.HMIN) & ((e / h) >= R24.WLO)
    nc["ly_nc"] = np.log(e.where(okn))
    capped_son = float(((e > R24.HI) & okn).sum() / okn.sum())
    nc = nc.dropna(subset=["ly_nc", "lyp_nc"]).assign(lyp=lambda s: s["lyp_nc"])
    row("no upper bound on parental income or son's earnings", nc, "ly_nc")
    md += ["", f"Share of parental child-years (son's 13-19) above $150,000 of 1967: {cap_par:.4f}; share of son-years "
           f"with earnings above it (of those passing the lower bound and the hours screen): {capped_son:.4f}.", ""]
    RES["cap"] = {"parent_years": cap_par, "son_years": capped_son}
    # K4 attrition
    md += ["## K4. Attrition", "", "| band | sons observed | as a share of sons at 25-29 |", "|---|---|---|"]
    n0 = v[v["band"] == 0]["pid"].nunique()
    for kb, lab in enumerate(R113.BL):
        n = v[v["band"] == kb]["pid"].nunique()
        md.append(f"| {lab} | {n:,} | {n / n0:.3f} |")
        RES[f"ret|{lab}"] = n / n0
    stay = set(v[v["band"] == 4]["pid"])
    v0 = v[v["band"] == 0].copy()
    v0["stay"] = v0["pid"].isin(stay)
    v0["cellb"] = np.where(v0["stay"], "stayers", "others")
    from scipy.stats import norm
    S = R113.R33.Cells(v0.assign(_y=v0["ly"], agei=v0["age"].round().astype(int)), "_y", "lyp", "cellb", [], "agei", w="wt")
    st, ot = S.lin([("stayers", "x", 1)]), S.lin([("others", "x", 1)])
    dif = S.lin([("stayers", "x", 1), ("others", "x", -1)])
    allb = profile(v)[0]
    md += ["", f"IGE at 25-29: all sons {c(allb)}; sons later observed at 45-49 {c(st)} ({len(stay & set(v0['pid'])):,} "
           f"sons); the others {c(ot)}; stayers - others {c(dif)}.", ""]
    RES["stayers"] = {"all": list(map(float, allb)), "stay": list(map(float, st)), "others": list(map(float, ot)),
                      "diff": list(map(float, dif))}
    (OUT / "parent_age_cap_attrition.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "parent_age_cap_attrition.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
