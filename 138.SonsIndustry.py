r"""The son's industry: does a lower-paying industry carry the layoff's cost? (committee re-read memo, action 8, 2026-10-24)

106 / 133: across age bands the wage cost is two thirds within the son's occupation; within son it sits in his
self-employed years. The employer side not yet held fixed is the son's own industry: its CPS wage premium (32's P, the
industry's ln-wage premium; B, its premium's slope in experience) and the industry group itself.
DESIGN (75's son-years with a valid wage; within-son slopes of the layoff share x (age-40)/10, 91's fe_fit, 75's
controls as 118; all years and employee years (118's self-employment code)):
  outcomes: the son's industry premium P; his ln wage net of P;
  controls: his 33 industry groups (time-varying dummies), and the groups x (age-40)/10, added to the ln earnings and
  ln wage slopes.
Writes output/sons_industry.md / .json (aggregates only). DESCRIPTIVE.
"""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import OUT  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R118 = _load("s118", "118.SonsEmployerType.py")
R91, R75 = R118.R91, R118.R75
c, COMPS, STRUCT = R91.c, R91.COMPS, R91.STRUCT
RES = {}


def main():
    r = R75.build()
    r = r.merge(R118.items()[["wave", "int", "self"]], on=["wave", "int"], how="left")
    r["selfemp"] = r["self"].isin([2, 3]).astype(float).where(r["self"].isin([1, 2, 3]))
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    cohd = pd.get_dummies(r["coh5"], prefix="coh", drop_first=True).astype(float)
    r = pd.concat([r, cohd], axis=1)
    r["agec"] = (r["age"] - 40) / 10
    XB = R91.xage(r, ["lyp"] + COMPS + STRUCT + list(cohd.columns))
    v = r[r["lw"].notna() & r["igrp"].notna()].copy()
    v["P_v"] = v["P"]
    v["lw_netP"] = v["lw"] - v["P"]
    ig = pd.get_dummies(v["igrp"].astype(int), prefix="ig", drop_first=True).astype(float)
    v = pd.concat([v, ig], axis=1)
    IG = list(ig.columns)
    IGA = []
    for x in IG:
        v[f"{x}_xa"] = v[x] * v["agec"]
        IGA.append(f"{x}_xa")
    g = lambda f, x: (f["b"][x], float(np.sqrt(f["V"].loc[x, x])))  # noqa: E731
    md = ["# The son's industry and the layoff's cost (committee re-read memo, action 8)", "",
          "Built by `138.SonsIndustry.py` (2026-10-24); design in its docstring. Within-son slope of the father's teen "
          "layoff share x (age-40)/10; s.e. clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**", "",
          f"Son-years with an industry group {len(v):,} of {v['pid'].nunique():,} sons.", "",
          "| years | outcome / control | layoff share x age | son-years |", "|---|---|---|---|"]
    for ylab, sub in (("all years", pd.Series(True, index=v.index)), ("employee years", v["selfemp"] == 0)):
        q = v[sub]
        for y, lab, xs in (("P_v", "industry wage premium (outcome)", []), ("lw_netP", "ln wage net of the premium", []),
                           ("ly", "ln earnings", []), ("ly", "ln earnings, industry groups held fixed", IG),
                           ("ly", "ln earnings, industry groups and x age", IG + IGA), ("lw", "ln wage", []),
                           ("lw", "ln wage, industry groups held fixed", IG),
                           ("lw", "ln wage, industry groups and x age", IG + IGA)):
            f = R91.fe_fit(q.dropna(subset=[y]), y, XB + xs)
            md.append(f"| {ylab} | {lab} | {c(g(f, 'f_sh_layoff_xa'))} | {f['n']:,} |")
            RES[f"{ylab}|{lab}"] = list(g(f, "f_sh_layoff_xa"))
            print(md[-1], flush=True)
    md.append("")
    (OUT / "sons_industry.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "sons_industry.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
