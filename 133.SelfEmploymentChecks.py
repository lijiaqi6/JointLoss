r"""Pinning down the self-employment result (committee re-read memo, action 1, 2026-10-24)

118 / 119 / 123: within the same son the father's teen layoff bends his earnings by -0.885*** a decade in his
self-employed years and by -0.084 in his years as an employee; hourly wage -0.609** against -0.004. A reader asks:
how many treated sons stand behind it; is it men who work for themselves only or also for others; incorporated or
not; is it underreported self-employment income rather than lower income; and where in the occupation structure does
the employee-years cost sit?
ITEMS (son as head; 118's 'work for self / others' for the main job: 1 someone else, 2 both, 3 self only):
  incorporation of the head's business, 1985-2001 'B5 CORP/UNCORP BUS(HD-E)', 2003+ 'BC23 CORP/UNCORP BUS--JOB 1'
    (1 unincorporated, 2 corporation);
  family food spending (38.PSIDJointLossChecks.py's cache: food at home + away (+ delivered), 2000 dollars; waves
    1981-87, 1990-97, 1999-2023), ln;
  the family's net worth with home equity (121's cache, wealth waves), asinh(net worth / 1,000);
  the son's occupation wage score and wage within occupation (106's os / res).
DESIGN: 75's son-years with a valid wage; within-son slope of the layoff share x (age-40)/10 (91's fe_fit, 75's
  controls as 118) by year type, and the layoff x age x self-employed interaction on all years; PSID weights; clusters
  1968 family.
Writes output/self_employment_checks.md / .json (aggregates only); caches data/sons_incorp.pkl (family-level).
DESCRIPTIVE.
"""
import importlib.util
import json
import re
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


R118 = _load("s118", "118.SonsEmployerType.py")
R121 = _load("s121", "121.WealthMeasures.py")
R91, R18, R75 = R118.R91, R118.R18, R118.R75
c, COMPS, STRUCT = R91.c, R91.COMPS, R91.STRUCT
CACHE = DATA / "sons_incorp.pkl"
RES = {}


def incorp():
    if CACHE.exists():
        return pd.read_pickle(CACHE)
    out = []
    for w in [x for x in R18.FS.WAVES if x >= 1985]:
        do = next(f for f in (R18.FAM / (f"fam{w}" if w < 1994 else f"fam{w}er")).glob("*.do") if "formats" not in f.name)
        pos, labs = R18.layout(do)
        idv = labs[1][0]
        v = next((v for v, l in labs if re.match(r"^(B5 CORP/UNCORP BUS\(HD-E\)|B5 WTR BUSINESS CORP/UNINCORP \(HD-E\)|"
                                                   r"BC23 CORP/UNCORP BUS--JOB 1)", l)), None)
        if v is None:
            print(f"  {w}: none", flush=True)
            continue
        f = R18.read(do.with_suffix(".txt"), [idv, v], pos)
        x = pd.DataFrame({"wave": w, "int": f[idv], "corp": pd.to_numeric(f[v], errors="coerce")})
        x["corp"] = (x["corp"] == 2).astype(float).where(x["corp"].isin([1, 2]))
        print(f"  {w}: {v}; corporation share {x['corp'].mean():.3f}", flush=True)
        out.append(x)
    F = pd.concat(out, ignore_index=True)
    F.to_pickle(CACHE)
    return F


def main():
    r = R75.build()
    r = r.merge(R118.items()[["wave", "int", "self"]], on=["wave", "int"], how="left")
    r = r.merge(incorp(), on=["wave", "int"], how="left")
    food = pd.read_pickle(DATA / "psid_joint_loss_food.pkl")
    food = food[list(food)[0]] if isinstance(food, dict) else food
    r = r.merge(food[["wave", "int", "food"]].drop_duplicates(["wave", "int"]), on=["wave", "int"], how="left")
    C = R121.components()[["wave", "int", "total"]].drop_duplicates(["wave", "int"])
    r = r.merge(C, on=["wave", "int"], how="left")
    r["lfood"] = np.log(r["food"].where(r["food"] > 0))
    r["anw"] = np.arcsinh(r["total"] / 1000)
    r["os_v"] = r["os"].where(r["lw"].notna())
    r["res_v"] = r["res"].where(r["lw"].notna())
    r["selfemp"] = r["self"].isin([2, 3]).astype(float).where(r["self"].isin([1, 2, 3]))
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    cohd = pd.get_dummies(r["coh5"], prefix="coh", drop_first=True).astype(float)
    r = pd.concat([r, cohd], axis=1)
    r["agec"] = (r["age"] - 40) / 10
    XB = R91.xage(r, ["lyp"] + COMPS + STRUCT + list(cohd.columns))
    v = r[r["lw"].notna()].dropna(subset=["selfemp"]).copy()
    v["lay_self_xa"] = v["f_sh_layoff"] * v["selfemp"] * v["agec"]
    v["self_xa"] = v["selfemp"] * v["agec"]
    pres = v["nofa"] == 0
    g = lambda f, x: (f["b"][x], float(np.sqrt(f["V"].loc[x, x])))  # noqa: E731
    md = ["# Pinning down the self-employment result (committee re-read memo, action 1)", "",
          "Built by `133.SelfEmploymentChecks.py` (2026-10-24); design in its docstring. Within-son slope of the father's "
          "teen layoff share x (age-40)/10; s.e. clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1. "
          "**Descriptive.**", "", "## 1. Who stands behind the self-employed-years slope", "",
          "| band | son-years | self-employed son-years | of which self only | sons with a self-employed year | treated "
          "(teen layoff) sons with a self-employed year |", "|---|---|---|---|---|---|"]
    for kb, lab in enumerate(R91.BLAB):
        q = v[v["band"] == kb]
        se = q[q["selfemp"] == 1]
        md.append(f"| {lab} | {len(q):,} | {len(se):,} | {float((se['self'] == 3).mean()):.3f} | {se['pid'].nunique():,} | "
                  f"{se[(se['f_sh_layoff'] > 0) & pres.loc[se.index]]['pid'].nunique():,} |")
    se = v[v["selfemp"] == 1]
    tr = se[(se["f_sh_layoff"] > 0) & pres.loc[se.index]]
    RES["counts"] = {"se_years": len(se), "se_sons": int(se["pid"].nunique()), "treated_se_sons": int(tr["pid"].nunique()),
                     "treated_se_years": len(tr), "self_only_share": float((se["self"] == 3).mean())}
    md += ["", f"All bands: {len(se):,} self-employed son-years of {se['pid'].nunique():,} sons; {tr['pid'].nunique():,} "
           f"treated sons with {len(tr):,} self-employed years; self only {RES['counts']['self_only_share']:.3f} of "
           "self-employed years.", "",
           "## 2. By type of year (ln earnings, ln wage)", "",
           "| year type | ln earnings | ln wage | son-years / sons |", "|---|---|---|---|"]
    types = (("employee", v["self"] == 1), ("self-employed (both kinds)", v["selfemp"] == 1),
             ("self only", v["self"] == 3), ("self and others", v["self"] == 2),
             ("self-employed, unincorporated (1985+)", (v["selfemp"] == 1) & (v["corp"] == 0)),
             ("self-employed, incorporated (1985+)", (v["selfemp"] == 1) & (v["corp"] == 1)))
    for lab, m in types:
        q = v[m]
        f1 = R91.fe_fit(q, "ly", XB)
        f2 = R91.fe_fit(q, "lw", XB)
        md.append(f"| {lab} | {c(g(f1, 'f_sh_layoff_xa'))} | {c(g(f2, 'f_sh_layoff_xa'))} | {f1['n']:,} / {f1['sons']:,} |")
        RES[f"type|{lab}"] = {"ly": list(g(f1, "f_sh_layoff_xa")), "lw": list(g(f2, "f_sh_layoff_xa")), "n": f1["n"],
                              "sons": f1["sons"]}
        print(md[-1], flush=True)
    md += ["", "## 3. Underreporting: food spending and net worth in self-employed and employee years", "",
           "| outcome | employee years | self-employed years | all years: layoff x age x self-employed | son-years |",
           "|---|---|---|---|---|"]
    for y, lab in (("ly", "ln earnings (reference)"), ("lfood", "ln family food spending"), ("anw", "asinh family net worth")):
        q = v.dropna(subset=[y])
        fE = R91.fe_fit(q[q["selfemp"] == 0], y, XB)
        fS = R91.fe_fit(q[q["selfemp"] == 1], y, XB)
        fA = R91.fe_fit(q, y, XB + ["selfemp", "self_xa", "lay_self_xa"])
        md.append(f"| {lab} | {c(g(fE, 'f_sh_layoff_xa'))} | {c(g(fS, 'f_sh_layoff_xa'))} | {c(g(fA, 'lay_self_xa'))} | "
                  f"{fA['n']:,} |")
        RES[f"under|{y}"] = {"emp": list(g(fE, "f_sh_layoff_xa")), "se": list(g(fS, "f_sh_layoff_xa")),
                             "inter": list(g(fA, "lay_self_xa")), "n": fA["n"]}
        print(md[-1], flush=True)
    md += ["", "## 4. Employee years: between or within occupations", "",
           "| outcome | all years | employee years | self-employed years |", "|---|---|---|---|"]
    for y, lab in (("lw", "ln wage"), ("os_v", "occupation wage score"), ("res_v", "wage within occupation")):
        cells = []
        for m in (pd.Series(True, index=v.index), v["selfemp"] == 0, v["selfemp"] == 1):
            q = v[m].dropna(subset=[y])
            f = R91.fe_fit(q, y, XB)
            cells.append(g(f, "f_sh_layoff_xa"))
        md.append(f"| {lab} | " + " | ".join(c(x) for x in cells) + " |")
        RES[f"occ|{y}"] = [list(x) for x in cells]
        print(md[-1], flush=True)
    md.append("")
    (OUT / "self_employment_checks.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "self_employment_checks.json", "w"), indent=1, default=float)
    print("\n".join(md))


if __name__ == "__main__":
    main()
