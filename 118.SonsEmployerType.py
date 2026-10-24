r"""Does the kind of employer carry the delayed cost of a father's teen layoff? (Paper B exploration, 2026-10-24)

At equal schooling, health, place and family wealth, the cost is a lower wage within the son's occupation in his forties
(106, 115-117). Union and public-sector jobs have flatter, protected wage paths, self-employment and small workplaces
riskier ones. From the family files (the head's items for his main job; 18's reader):
  UNION    covered by a union contract or belongs to a union: 'JOB COV(ERD) BY UNION', 'BELONG TO (LABOR) UNION',
           'JOB NOW UNION? (H-E)', 'BELONG UNION? (HD-E)' (1 = yes, 5 = no), 1976+
  GOVT     works for government: 1980-84 'WORK FOR GOVT' 1 = yes; 1985+ codes 1-3 (federal, state, local) vs 4
           (private), 2003+ 'BC24 WORK FOR GOVT?--JOB 1' (49's coding)
  SELF     works for himself (alone or also for others): 'WORK FOR SELF/OTH', codes 2-3 vs 1
  SIZE     ln number employed at his work location, 2003+ ('BC25A NUMBER EMPLOYED AT WORK LOCATION', 1-9,000,000)
For each: the teen layoff coefficient at 25-29 and 45-49 and the change (91's band_fit, at equal ln parental income and
all of 75's components, 200 draws) and the within-son slope; then the within-son ln earnings and ln wage slopes of the
layoff share with each one added as a time-varying control. 75's baseline sample. DESCRIPTIVE.
Writes output/sons_employer_type.md / .json (aggregates only); caches data/sons_employer_items.pkl (family-level).
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


R91 = _load("s91", "91.LayoffSelection.py")
R18 = _load("s18", "18.HusbandIndustryShocks.py")
R75 = R91.R75
c, fmt, sd, Boot = R91.c, R91.fmt, R91.sd, R91.Boot
COMPS, STRUCT = R91.COMPS, R91.STRUCT
CACHE = DATA / "sons_employer_items.pkl"
PAT = {
    "cov": [r"JOB COV(ERD|ERED)? BY UNION", r"JOB NOW UNION\?\s*\(H-E\)", r"^BC26 JOB NOW UNION"],
    "mem": [r"BELONG TO (LABOR |THAT )?UNION", r"BELONG UNION\?\s*\(HD-E\)", r"^BC27 BELONG UNION"],
    "gov": [r"^[A-Z]\d+ (WTR )?WORK FOR GOVT.*\(HD-E\)", r"^BC24 WORK FOR GOVT\?--JOB 1"],
    "self": [r"^[A-Z]\d+ WORK SELF/OTR\??\s*\(HD-E\)", r"^BC\d+ WORK SELF/OTR\?--JOB 1"],
    "size": [r"^BC25A NUMBER EMPLOYED AT WORK LOCATION"],
}
RES = {}


def items():
    if CACHE.exists():
        return pd.read_pickle(CACHE)
    out = []
    for w in [x for x in R18.FS.WAVES if x >= 1976]:
        folder = R18.FAM / (f"fam{w}" if w < 1994 else f"fam{w}er")
        do = next(f for f in folder.glob("*.do") if "formats" not in f.name)
        pos, labs = R18.layout(do)
        idv = labs[1][0]
        sel = {}
        for k, pats in PAT.items():
            for p in pats:
                hit = next((v for v, l in labs if re.search(p, l)), None)
                if hit:
                    sel[k] = hit
                    break
        f = R18.read(do.with_suffix(".txt"), [idv] + list(sel.values()), pos).rename(
            columns={idv: "int", **{v: k for k, v in sel.items()}})
        f["wave"] = w
        for k in PAT:
            if k not in f:
                f[k] = np.nan
        print(f"  {w}: " + ", ".join(f"{k}={sel.get(k, '-')}" for k in PAT), flush=True)
        out.append(f[["wave", "int"] + list(PAT)])
    F = pd.concat(out, ignore_index=True)
    F.to_pickle(CACHE)
    return F


def main():
    r = R75.build()
    F = items()
    r = r.merge(F, on=["wave", "int"], how="left")
    cov = r["cov"].where(r["cov"].isin([1, 5]))
    mem = r["mem"].where(r["mem"].isin([1, 5]))
    r["union"] = np.fmax((cov == 1).astype(float).where(cov.notna()), (mem == 1).astype(float).where(mem.notna()))
    early = r["wave"] <= 1984
    r["govt"] = np.where(early, (r["gov"] == 1).astype(float), r["gov"].isin([1, 2, 3]).astype(float))
    r["govt"] = r["govt"].where(np.where(early, r["gov"].isin([1, 5]), r["gov"].isin([1, 2, 3, 4])))
    r["selfemp"] = r["self"].isin([2, 3]).astype(float).where(r["self"].isin([1, 2, 3]))
    r["lsize"] = np.log(r["size"].where(r["size"].between(1, 9_000_000)))
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    cohd = pd.get_dummies(r["coh5"], prefix="coh", drop_first=True).astype(float)
    r = pd.concat([r, cohd], axis=1)
    r["agec"] = (r["age"] - 40) / 10
    XB = R91.xage(r, ["lyp"] + COMPS + STRUCT + list(cohd.columns))
    BT = Boot(r["fam68"].to_numpy(), r["race"].to_numpy())
    md = ["# Does the kind of employer carry the delayed cost of a father's teen layoff?", "",
          "Built by `118.SonsEmployerType.py` (2026-10-24); design in its docstring. Coefficient of the father's teen layoff "
          "share (per unit share). *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**", "",
          "## 1. The son's employer as an outcome", "",
          "| outcome | mean | 25-29 | 45-49 | change | within son x age | sons |", "|---|---|---|---|---|---|---|"]
    cands = (("union", "union-covered or member"), ("govt", "works for government"), ("selfemp", "self-employed"),
             ("lsize", "ln employed at his workplace (2003+)"))
    for y, lab in cands:
        q = r.dropna(subset=[y])
        ok = lambda k: q[(q["band"] == k)].dropna(subset=COMPS + ["lyp"])["pid"].nunique() >= 200  # noqa: E731
        a0 = R91.band_fit(q, y, 0, BT, COMPS, ["f_sh_layoff"]).get("f_sh_layoff") if ok(0) else None
        a4 = R91.band_fit(q, y, 4, BT, COMPS, ["f_sh_layoff"]).get("f_sh_layoff") if ok(4) else None
        ch = (a4[0] - a0[0], a4[1] - a0[1]) if a0 and a4 else None
        f = R91.fe_fit(q, y, XB)
        fe = (f["b"]["f_sh_layoff_xa"], float(np.sqrt(f["V"].loc["f_sh_layoff_xa", "f_sh_layoff_xa"])))
        md.append(f"| {lab} | {np.average(q[y], weights=q['wt']):.3f} | {fmt(a0)} | {fmt(a4)} | {fmt(ch)} | {c(fe)} | "
                  f"{q['pid'].nunique():,} |")
        RES[f"outcome|{y}"] = {"a": [float(a0[0]), sd(a0[1])] if a0 else None, "b": [float(a4[0]), sd(a4[1])] if a4 else None,
                               "ch": [float(ch[0]), sd(ch[1])] if ch else None, "fe": list(map(float, fe))}
    md.append("")
    md += ["## 2. The within-son layoff slope with each held fixed (time-varying control)", "",
           "| outcome | control | sample: as before | + control | control's own coefficient | son-years |",
           "|---|---|---|---|---|---|"]
    g = lambda f, x: (f["b"][x], float(np.sqrt(f["V"].loc[x, x])))  # noqa: E731
    for y in ("ly", "lw"):
        for cand, lab in cands[:3]:
            q = r[r["lw"].notna()].dropna(subset=[cand]).copy()
            f0 = R91.fe_fit(q, y, XB)
            f1 = R91.fe_fit(q, y, XB + [cand])
            md.append(f"| {y} | {lab} | {c(g(f0, 'f_sh_layoff_xa'))} | {c(g(f1, 'f_sh_layoff_xa'))} | {c(g(f1, cand))} | "
                      f"{f1['n']:,} |")
            RES[f"control|{y}|{cand}"] = {"base": list(g(f0, "f_sh_layoff_xa")), "with": list(g(f1, "f_sh_layoff_xa")),
                                         "own": list(g(f1, cand))}
        q = r[r["lw"].notna()].dropna(subset=["union", "govt", "selfemp"]).copy()
        f0 = R91.fe_fit(q, y, XB)
        f1 = R91.fe_fit(q, y, XB + ["union", "govt", "selfemp"])
        md.append(f"| {y} | all three | {c(g(f0, 'f_sh_layoff_xa'))} | {c(g(f1, 'f_sh_layoff_xa'))} | | {f1['n']:,} |")
        RES[f"control|{y}|all"] = {"base": list(g(f0, "f_sh_layoff_xa")), "with": list(g(f1, "f_sh_layoff_xa"))}
    md.append("")
    # 3. where the cost sits: employee years vs self-employed years; size held fixed (2003+)
    md += ["## 3. Where the cost sits: employee years and self-employed years; workplace size (2003+)", "",
           "| outcome | spec | layoff share x age | interaction / control | son-years / sons |", "|---|---|---|---|---|"]
    for y in ("ly", "lw"):
        q = r[r["lw"].notna()].dropna(subset=["selfemp"]).copy()
        for lab, sub in (("employee years only", q["selfemp"] == 0), ("self-employed years only", q["selfemp"] == 1)):
            f = R91.fe_fit(q[sub], y, XB)
            md.append(f"| {y} | {lab} | {c(g(f, 'f_sh_layoff_xa'))} | | {f['n']:,} / {f['sons']:,} |")
            RES[f"split|{y}|{lab}"] = list(g(f, "f_sh_layoff_xa"))
        q["lay_self_xa"] = q["f_sh_layoff"] * q["selfemp"] * q["agec"]
        q["self_xa"] = q["selfemp"] * q["agec"]
        f = R91.fe_fit(q, y, XB + ["selfemp", "self_xa", "lay_self_xa"])
        md.append(f"| {y} | all years, layoff x age x self-employed | {c(g(f, 'f_sh_layoff_xa'))} | "
                  f"{c(g(f, 'lay_self_xa'))} | {f['n']:,} / {f['sons']:,} |")
        RES[f"inter|{y}"] = {"base": list(g(f, "f_sh_layoff_xa")), "inter": list(g(f, "lay_self_xa"))}
        q = r[r["lw"].notna() & (r["wave"] >= 2003)].dropna(subset=["lsize"]).copy()
        f0 = R91.fe_fit(q, y, XB)
        f1 = R91.fe_fit(q, y, XB + ["lsize"])
        md.append(f"| {y} | 2003+, as before -> + ln workplace size | {c(g(f0, 'f_sh_layoff_xa'))} -> "
                  f"{c(g(f1, 'f_sh_layoff_xa'))} | {c(g(f1, 'lsize'))} | {f1['n']:,} / {f1['sons']:,} |")
        RES[f"size|{y}"] = {"base": list(g(f0, "f_sh_layoff_xa")), "with": list(g(f1, "f_sh_layoff_xa")),
                            "own": list(g(f1, "lsize"))}
    md.append("")
    (OUT / "sons_employer_type.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "sons_employer_type.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
