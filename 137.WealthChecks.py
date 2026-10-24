r"""Wealth: is it permanent income, and does its age profile hold within cohorts and within son? (re-read action 7, 2026-10-24)

121: parental net worth carries 14.5 (asinh) to 29.1 (rank) percent of the earnings IGE, most of it housing. 122: the
rank-rank slope of the son's net worth on his parents' rises from 0.228*** at 25-29 to 0.408*** at 35-39. A wealth
economist asks (a) whether wealth only stands in for permanent income that the teen-window mean misses, (b) whether
the wealth profile is a cross-cohort pattern, (c) whether gifts received so far carry it, (d) whether it is the home.
DESIGNS
  (a) 121's split (98's sons, split B) with ln parental income re-measured at the father's ages 40-50 (125's lyp40,
      father-present sons) and over the son's whole childhood (wave-ages 1-19, >= 5 years): wealth share with each.
  (b) 122's son-years: the rank-rank slope by band within birth cohorts 1964-69, 1970-75, 1976-81; and within son,
      the son's net-worth rank on parents' rank x (age-40)/10 with son FE and single-age dummies.
  (c) the same slopes holding fixed the cumulative value of gifts and inheritances the son's family received up to the
      wave (asinh, 1999+ waves) and its interaction with age.
  (d) the son's housing equity rank and non-housing net-worth rank (121's components, within wave x birth year) on the
      parents' total wealth rank, by band.
Writes output/wealth_checks.md / .json (aggregates only). DESCRIPTIVE.
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


R122 = _load("s122", "122.WealthTransmission.py")
R121, R80, R18 = R122.R121, R122.R80, R122.R18
R74 = R121.R74
est, cc, Boot, run_spec = R74.est, R74.cc, R74.Boot, R74.run_spec
R24 = R80.R75.R24
c, wls = R122.c, R122.wls
BANDS = R122.BANDS
RES = {}


def alt_parent_income(sons, py):
    fy = py[py["head"] & py["pid"].isin(sons["fpid"].dropna()) & py["age"].between(40, 50)
            & py["faminc"].between(R24.LO, R24.HI)].groupby("pid")["faminc"].agg(["mean", "count"])
    fy = fy[fy["count"] >= 3]
    lyp40 = np.log(sons["fpid"].map(fy["mean"]))
    k = py[py["child"] & py["age"].between(1, 19) & py["faminc"].between(R24.LO, R24.HI) & py["pid"].isin(sons["pid"])]
    g = k.groupby("pid")["faminc"].agg(["mean", "count"])
    lyp_all = np.log(sons["pid"].map(g["mean"].where(g["count"] >= 5)))
    return pd.DataFrame({"pid": sons["pid"].values, "lyp40": lyp40.values, "lyp_all": lyp_all.values})


def main():
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    # ---------------- (a) wealth share with other parental-income measures
    r, _, _ = R80.build()
    C = R121.components()
    r = r.merge(R121.son_means(r, C), on="pid", how="left")
    d = r[r["lw"].notna() & r["total"].notna()].copy()
    one = d.drop_duplicates("pid")[["pid", "birth_year", "total"]].copy()
    one["total_rank"] = one.groupby("birth_year")["total"].rank(pct=True)
    one["total_asinh"] = np.arcsinh(one["total"] / 1000)
    d = d.merge(one[["pid", "total_rank", "total_asinh"]], on="pid", how="left")
    d = d.merge(alt_parent_income(d.drop_duplicates("pid")[["pid", "fpid"]], py), on="pid", how="left")
    base = {**{g: v for g, v in R121.R75.GROUPS.items() if g != "structure"}, **R80.NEW,
            "structure": R121.R75.GROUPS["structure"] + ["f_educ_na", "m_educ_na", "inc_na"]}
    md = ["# Wealth: permanent income, cohorts, gifts and the home (committee re-read memo, action 7)", "",
          "Built by `137.WealthChecks.py` (2026-10-24); design in its docstring. *** p<0.01, ** p<0.05, * p<0.1. "
          "**Descriptive.**", "", "## (a) The wealth share of the 25-55 IGE with other measures of parental income", "",
          "| parental income | sons | IGE | wealth share: rank | wealth share: asinh | parents' wage share (rank spec) |",
          "|---|---|---|---|---|---|"]
    for lab, col in (("teen window 13-19 (as 121)", "lyp"), ("father's ages 40-50", "lyp40"),
                     ("son's whole childhood, 1-19", "lyp_all")):
        q = d.dropna(subset=[col]).copy()
        q["lyp"] = q[col]
        BT = Boot(q["fam68"].to_numpy(), q["race"].to_numpy())
        rr = run_spec(q, ["ly"], {**base, "wealth": ["total_rank"]}, BT, cells=(6,))
        ra = run_spec(q, ["ly"], {**base, "wealth": ["total_asinh"]}, BT, cells=(6,))
        b0 = est(rr, 6, "b0", 0)
        wr, wa = est(rr, 6, "c:wealth", 0, share=True), est(ra, 6, "c:wealth", 0, share=True)
        wg = est(rr, 6, "c:wage", 0, share=True)
        md.append(f"| {lab} | {q['pid'].nunique():,} | {cc(b0)} | {cc(wr)} | {cc(wa)} | {cc(wg)} |")
        RES[f"a|{lab}"] = {"b0": list(b0[:2]), "rank": list(wr[:2]), "asinh": list(wa[:2]), "wage": list(wg[:2])}
        print(md[-1], flush=True)
    md.append("")
    # ---------------- (b)-(d) the son's wealth
    sons = r.drop_duplicates("pid")[["pid", "birth_year", "fam68"]].copy()
    pw = R121.son_means(r, C)[["pid", "total"]].rename(columns={"total": "pnw"})
    sons = sons.merge(pw, on="pid", how="left")
    sons["pw_rank"] = sons.groupby("birth_year")["pnw"].rank(pct=True)
    y = py[(py["head"] | py["wife"]) & py["pid"].isin(sons["pid"]) & py["age"].between(25, 55)
           & py["wave"].isin(R18.WEALTH_WAVES)][["pid", "wave", "int", "age", "wt"]]
    y = y.merge(C, on=["wave", "int"], how="inner").merge(R122.gifts(), on=["wave", "int"], how="left")
    y = y.merge(sons, on="pid", how="left").dropna(subset=["pw_rank"])
    for v_ in ("total", "home"):
        y[f"{v_}_r"] = y.groupby(["wave", "birth_year"])[v_].rank(pct=True)
    y["nonhome"] = y["total"] - y["home"]
    y["nonhome_r"] = y.groupby(["wave", "birth_year"])["nonhome"].rank(pct=True)
    y["band"] = pd.cut(y["age"], [24, 29, 34, 39, 44, 49, 55], labels=False)
    y = y.sort_values(["pid", "wave"])
    y["gv"] = y["gift_val"].fillna(0.0)
    y["cum_gift"] = np.arcsinh(y.groupby("pid")["gv"].cumsum() / 1000)
    md += ["## (b) The son's net-worth rank on his parents' wealth rank, within birth cohorts", "",
           "| cohort | " + " | ".join(f"{lo}-{hi}" for lo, hi in BANDS[:5]) + " |", "|---" * 6 + "|"]
    for lo_b, hi_b in ((1964, 1969), (1970, 1975), (1976, 1981)):
        q = y[y["birth_year"].between(lo_b, hi_b)]
        cells = []
        for k in range(5):
            z = q[q["band"] == k]
            cells.append(c(wls(z, "total_r", "pw_rank")[0]) if z["pid"].nunique() >= 150 else "")
        md.append(f"| born {lo_b}-{hi_b} | " + " | ".join(cells) + " |")
        RES[f"b|{lo_b}"] = cells
    # within son
    y["agec"] = (y["age"] - 40) / 10
    y["pr_a"] = y["pw_rank"] * y["agec"]
    y["cg_a"] = y["cum_gift"] * y["agec"]
    ols = _load("s101", "101.EITCByAge.py").ols
    dummies = _load("s101b", "101.EITCByAge.py").dummies
    z = y.dropna(subset=["total_r"])
    out = {}
    for lab, xs, q in (("within son", ["pr_a"], z), ("within son, 1999+ waves", ["pr_a"], z[z["wave"] >= 1999]),
                       ("within son, 1999+, + cumulative gifts (and x age)", ["pr_a", "cum_gift", "cg_a"],
                        z[z["wave"] >= 1999])):
        X = np.column_stack([q[xs].to_numpy(float), dummies(q["age"])])
        b, V = ols(X, q["total_r"].to_numpy(float), q["wt"].clip(lower=1e-9).to_numpy(float), q["fam68"].to_numpy(),
                   absorb=q["pid"].to_numpy())
        out[lab] = (b[0], float(np.sqrt(V[0, 0])))
    md += ["", "Within son (son FE, single-age dummies): parents' wealth rank x (age-40)/10 on the son's net-worth rank: "
           + "; ".join(f"{k} {c(v_)}" for k, v_ in out.items()) + ".", ""]
    RES["b|within"] = {k: list(map(float, v_)) for k, v_ in out.items()}
    # (c) by band with cumulative gifts
    md += ["## (c) and (d) By band: holding cumulative gifts fixed (1999+), and housing vs non-housing outcomes", "",
           "| band | net worth, 1999+ | + cumulative gifts | son's housing equity rank | son's non-housing rank |",
           "|---|---|---|---|---|"]
    for k, (lo, hi) in enumerate(BANDS[:5]):
        q = y[y["band"] == k]
        q99 = q[q["wave"] >= 1999]
        a1 = wls(q99, "total_r", "pw_rank")[0]
        a2 = wls(q99, "total_r", "pw_rank", ["cum_gift"])[0]
        h = wls(q, "home_r", "pw_rank")[0]
        n = wls(q, "nonhome_r", "pw_rank")[0]
        md.append(f"| {lo}-{hi} | {c(a1)} | {c(a2)} | {c(h)} | {c(n)} |")
        RES[f"cd|{lo}-{hi}"] = {"nw99": list(a1), "gifts": list(a2), "home": list(h), "nonhome": list(n)}
        print(md[-1], flush=True)
    md.append("")
    (OUT / "wealth_checks.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "wealth_checks.json", "w"), indent=1, default=float)
    print("\n".join(md))


if __name__ == "__main__":
    main()
