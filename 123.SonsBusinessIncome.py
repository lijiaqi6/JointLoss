r"""Business income of self-employed sons: does it change the IGE profile or the layoff cost? (committee memo Z3, 2026-10-24)

Headlines 7-8 (118, 119): sons of laid-off fathers are more often self-employed, and the delayed cost sits in their
self-employed years (within son -0.885*** vs -0.084 as employees; wage -0.609** vs -0.004). For an owner, the split of
business income into a labor part (in the PSID's labor income, so in the son's earnings) and an asset part (only in
family income) is the respondent's, and his 'hourly wage' is earnings over hours. If sons of laid-off fathers shift
their business income into the asset part with age, the measured cost is an accounting artefact.
ITEMS (head of the son's family unit, income year = wave - 1, 2000 dollars; 1976-2023):
  bus_lab   labor part of business income ('LABOR PART BUS Y', 'HD/RP LABOR INCOME FROM BUSINESS'); inside earnings
            (1.PSID.py adds it back from 1994)
  bus_ast   asset part ('ASSET PART BUS Y', 'HD/RP ASSET INCOME FROM BUSINESS'); not in earnings
  self      118's 'work for self / others' for the main job at the interview (2-3 = self-employed)
OUTCOMES: ly (ln earnings, 75's); ly_tot = ln(earnings + max(asset part, 0)); lw, lh; asinh of the business labor part
  and of earnings minus it (the rest of labor income).
DESIGNS (75's son-years with a valid wage, son as head, 1976+):
  1. self-employment by band and parental-income tercile; the business share of earnings in self-employed years.
  2. the IGE by band on all son-years, on employee son-years only, and with ly_tot (ln earnings on ln parental income,
     single-age dummies, weighted, clustered by 1968 family; change 45-49 minus 25-29 from one stacked regression).
  3. the within-son layoff slope (91's fe_fit, 75's controls) in self-employed and employee years for each outcome,
     and the layoff x age x self-employed interaction on all years; without sons of self-employed fathers (119).
Writes output/sons_business_income.md / .json (aggregates only); caches data/sons_business_items.pkl (family-level).
DESCRIPTIVE.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import DATA, OUT, to2000  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R119 = _load("s119", "119.FatherSelfEmployment.py")
R91, R118, R18, R75 = R119.R91, R119.R118, R119.R18, R119.R75
c, COMPS, STRUCT = R91.c, R91.COMPS, R91.STRUCT
CACHE = DATA / "sons_business_items.pkl"
PAT = {"bl": r"^(LABOR PART BUS|LABOR BUSIN INCOM|HD LABOR PART .*BUSINESS INCOME|(HD|RP) LABOR INCOME FROM BUSINESS)",
       "ba": r"^(ASSET PART BUS|ASSET BUSI INCOME|HD ASSET PART .*BUSINESS INCOME|(HD|RP) ASSET INCOME FROM BUSINESS)"}
RES = {}


def items():
    if CACHE.exists():
        return pd.read_pickle(CACHE)
    out = []
    for w in [x for x in R18.FS.WAVES if x >= 1976]:
        do = next(f for f in (R18.FAM / (f"fam{w}" if w < 1994 else f"fam{w}er")).glob("*.do")
                  if "formats" not in f.name)
        pos, labs = R18.layout(do)
        idv = labs[1][0]
        sel = {k: next((v for v, l in labs if re.search(p, l)), None) for k, p in PAT.items()}
        f = R18.read(do.with_suffix(".txt"), [idv] + [v for v in sel.values() if v], pos)
        x = pd.DataFrame({"wave": w, "int": f[idv]})
        for k, v in sel.items():
            x[k] = to2000(pd.to_numeric(f[v], errors="coerce"), w - 1) if v else np.nan
        print(f"  {w}: {sel}", flush=True)
        out.append(x)
    F = pd.concat(out, ignore_index=True)
    F.to_pickle(CACHE)
    return F


def band_ige(d, y):
    """IGE at 25-29 and 45-49 and the change, one stacked regression (every regressor x band 4), clusters 1968 family."""
    s = d[d["band"].isin([0, 4])].dropna(subset=[y, "lyp", "wt"])
    s = s[s["wt"] > 0]
    b4 = (s["band"] == 4).astype(float)
    ag = pd.get_dummies(s["age"], prefix="a", drop_first=True).astype(float)
    X = pd.concat([s[["lyp"]], (s["lyp"] * b4).rename("lyp_b4"), ag], axis=1)
    X = sm.add_constant(X)
    r = sm.WLS(s[y], X, weights=s["wt"]).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(s["fam68"])[0]})
    V = r.cov_params()
    a = (r.params["lyp"], np.sqrt(V.loc["lyp", "lyp"]))
    ch = (r.params["lyp_b4"], np.sqrt(V.loc["lyp_b4", "lyp_b4"]))
    b = (a[0] + ch[0], np.sqrt(V.loc["lyp", "lyp"] + V.loc["lyp_b4", "lyp_b4"] + 2 * V.loc["lyp", "lyp_b4"]))
    return a, b, ch, int(s["pid"].nunique())


def main():
    r = R75.build()
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    sons = r.drop_duplicates("pid")[["pid", "fpid", "birth_year"]]
    r = R119.attach(r, R119.father_se(sons, py, R119.head_se()), r["nofa"] == 0)
    hd = py[py["head"]][["pid", "wave"]].drop_duplicates().assign(is_head=1.0)
    r = r.merge(hd, on=["pid", "wave"], how="left")
    r = r.merge(R118.items()[["wave", "int", "self"]], on=["wave", "int"], how="left").merge(items(), on=["wave", "int"],
                                                                                            how="left")
    r = r[(r["wave"] >= 1976) & (r["is_head"] == 1)].copy()
    r["selfemp"] = r["self"].isin([2, 3]).astype(float).where(r["self"].isin([1, 2, 3]))
    earn = np.exp(r["ly"])
    r["bl"] = r["bl"].fillna(0.0).clip(lower=0)
    r["ba"] = r["ba"].fillna(0.0)
    r["ly_tot"] = np.log(earn + r["ba"].clip(lower=0))
    r["a_bus"] = np.arcsinh(r["bl"].where(r["ly"].notna()) / 1000)
    r["a_rest"] = np.arcsinh((earn - r["bl"]).clip(lower=0) / 1000)
    r["bus_sh"] = (r["bl"] / earn).clip(0, 1)
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    cohd = pd.get_dummies(r["coh5"], prefix="coh", drop_first=True).astype(float)
    r = pd.concat([r, cohd], axis=1)
    r["agec"] = (r["age"] - 40) / 10
    XB = R91.xage(r, ["lyp"] + COMPS + STRUCT + list(cohd.columns))
    v = r[r["lw"].notna()].copy()
    one = v.drop_duplicates("pid")
    q3 = one["lyp"].quantile([1 / 3, 2 / 3]).to_numpy()
    v["terc"] = np.select([v["lyp"] <= q3[0], v["lyp"] <= q3[1]], [1, 2], 3)
    md = ["# Business income of self-employed sons (committee memo Z3)", "",
          "Built by `123.SonsBusinessIncome.py` (2026-10-24); design in its docstring. 75's son-years with a valid wage, "
          "son as head, 1976+. *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**", "",
          "## 1. Self-employment and business income", "",
          "| band | self-employed: tercile 1 | tercile 2 | tercile 3 | business labor share of earnings, self-employed "
          "years | asset part > 0, self-employed years | son-years |", "|---|---|---|---|---|---|---|"]
    s = v.dropna(subset=["selfemp"])
    for k, lab in enumerate(R91.BLAB):
        q = s[s["band"] == k]
        if not len(q):
            continue
        sh = [float(np.average(q.loc[q["terc"] == t, "selfemp"], weights=q.loc[q["terc"] == t, "wt"]))
              for t in (1, 2, 3)]
        se = q[q["selfemp"] == 1]
        bs = float(np.average(se["bus_sh"], weights=se["wt"])) if len(se) else np.nan
        ap = float(np.average(se["ba"] > 0, weights=se["wt"])) if len(se) else np.nan
        md.append(f"| {lab} | " + " | ".join(f"{x:.3f}" for x in sh) + f" | {bs:.3f} | {ap:.3f} | {len(q):,} |")
        RES[f"desc|{lab}"] = {"se_terc": sh, "bus_share_se": bs, "asset_pos_se": ap}
    emp = s[s["selfemp"] == 0]
    md += ["", f"Business labor share of earnings in employee years: {np.average(emp['bus_sh'], weights=emp['wt']):.3f}.",
           "", "## 2. The IGE by band: all son-years, employee years, earnings + business asset income", "",
           "| sample / outcome | 25-29 | 45-49 | change | sons |", "|---|---|---|---|---|"]
    for lab, q, y in (("all son-years, ln earnings", v, "ly"), ("all son-years with a self-employment code", s, "ly"),
                      ("employee years only, ln earnings", s[s["selfemp"] == 0], "ly"),
                      ("all son-years, ln(earnings + business asset income)", v, "ly_tot")):
        a, b, ch, n = band_ige(q, y)
        md.append(f"| {lab} | {c(a)} | {c(b)} | {c(ch)} | {n:,} |")
        RES[f"ige|{lab}"] = {"a": list(map(float, a)), "b": list(map(float, b)), "ch": list(map(float, ch))}
        print(md[-1], flush=True)
    md += ["", "## 3. The within-son layoff slope in self-employed and employee years", "",
           "| sample | outcome | employee years | self-employed years | all years: layoff x age x self-employed | "
           "son-years (SE) / sons (SE) |", "|---|---|---|---|---|---|"]
    g = lambda f, x: (f["b"][x], float(np.sqrt(f["V"].loc[x, x])))  # noqa: E731
    ylab = {"ly": "ln earnings", "ly_tot": "ln(earnings + business asset income)", "lw": "ln hourly wage",
            "lh": "ln hours", "a_bus": "asinh business labor income", "a_rest": "asinh other labor income"}
    for slab, q0 in (("all sons", s), ("without self-employed fathers", s[s["f_se"] == 0])):
        q0 = q0.copy()
        q0["lay_self_xa"] = q0["f_sh_layoff"] * q0["selfemp"] * q0["agec"]
        q0["self_xa"] = q0["selfemp"] * q0["agec"]
        for y in ylab:
            fE = R91.fe_fit(q0[q0["selfemp"] == 0], y, XB)
            fS = R91.fe_fit(q0[q0["selfemp"] == 1], y, XB)
            fA = R91.fe_fit(q0, y, XB + ["selfemp", "self_xa", "lay_self_xa"])
            md.append(f"| {slab} | {ylab[y]} | {c(g(fE, 'f_sh_layoff_xa'))} | {c(g(fS, 'f_sh_layoff_xa'))} | "
                      f"{c(g(fA, 'lay_self_xa'))} | {fS['n']:,} / {fS['sons']:,} |")
            RES[f"fe|{slab}|{y}"] = {"emp": list(g(fE, "f_sh_layoff_xa")), "se": list(g(fS, "f_sh_layoff_xa")),
                                     "inter": list(g(fA, "lay_self_xa"))}
            print(md[-1], flush=True)
    md.append("")
    (OUT / "sons_business_income.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "sons_business_income.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
