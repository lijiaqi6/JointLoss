r"""Parental income measured before the window (committee re-read memo, action 6, 2026-10-24)

The layoff estimates hold ln parental income over the son's 13-19 fixed, the same window as the layoff share, so part
of what the layoff does to family income is held fixed with it (a mediator), and the father's earnings dip in the
years before his first layoff (108: about 0.1 higher three to six years before than in the year before). Here
parental income is measured at the son's 6-12 (126's pre_income: ln mean family income over >= 2 income years in
bounds), before the window.
SPECS (75's son-years with a valid wage, sons with the pre-window measure; 91's machinery, 200 common draws):
  (a) baseline (13-19 income) on these sons; (b) 6-12 income in place of 13-19 income; (c) both.
  Outcomes ln earnings and ln wage: layoff band change, closure change, layoff - closure, within-son slope.
Writes output/prewindow_income.md / .json (aggregates only). DESCRIPTIVE.
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


R126 = _load("s126", "126.EITCDesign.py")
R91 = _load("s91", "91.LayoffSelection.py")
R75 = R91.R75
c, fmt, sd, Boot = R91.c, R91.fmt, R91.sd, R91.Boot
COMPS, STRUCT = R91.COMPS, R91.STRUCT
RES = {}


def main():
    r = R75.build()
    r = r.merge(R126.pre_income(r), left_on="pid", right_index=True, how="left")
    r = r[r["lyp612"].notna()].copy()
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    cohd = pd.get_dummies(r["coh5"], prefix="coh", drop_first=True).astype(float)
    r = pd.concat([r, cohd], axis=1)
    r["agec"] = (r["age"] - 40) / 10
    rest = COMPS + STRUCT + list(cohd.columns)
    v = r[r["lw"].notna()].copy()
    v["lyp1319"] = v["lyp"]
    BT = Boot(v["fam68"].to_numpy(), v["race"].to_numpy())
    md = ["# Parental income measured before the window (committee re-read memo, action 6)", "",
          "Built by `135.PreWindowIncome.py` (2026-10-24); design in its docstring. Per unit teen layoff share; band s.e. "
          "from 200 cluster-bootstrap draws; within-son s.e. clustered by 1968 family. *** p<0.01, ** p<0.05, * p<0.1. "
          "**Descriptive.**", "",
          f"Sons with income at 6-12: {v['pid'].nunique():,}; corr(ln income 6-12, 13-19) "
          f"{np.corrcoef(v.drop_duplicates('pid')['lyp612'], v.drop_duplicates('pid')['lyp1319'])[0, 1]:.3f}.", ""]
    md += ["| outcome | parental income | layoff change | closure change | layoff - closure | within son x age |",
           "|---|---|---|---|---|---|"]
    for y in ("ly", "lw"):
        for lab, lypcol, ctrl in (("13-19 (baseline)", "lyp1319", ()), ("6-12 instead", "lyp612", ()),
                                  ("13-19 and 6-12", "lyp1319", ("lyp612",))):
            q = v.copy()
            q["lyp"] = q[lypcol]
            g0 = R91.band_fit(q, y, 0, BT, COMPS, ["f_sh_layoff", "f_sh_close"], ctrl)
            g4 = R91.band_fit(q, y, 4, BT, COMPS, ["f_sh_layoff", "f_sh_close"], ctrl)
            ch = lambda k: (g4[k][0] - g0[k][0], g4[k][1] - g0[k][1])  # noqa: E731
            chL, chC = ch("f_sh_layoff"), ch("f_sh_close")
            XB = R91.xage(q, ["lyp"] + list(ctrl) + rest)
            f = R91.fe_fit(q, y, XB)
            fe = (f["b"]["f_sh_layoff_xa"], float(np.sqrt(f["V"].loc["f_sh_layoff_xa", "f_sh_layoff_xa"])))
            md.append(f"| {y} | {lab} | {fmt(chL)} | {fmt(chC)} | {fmt((chL[0] - chC[0], chL[1] - chC[1]))} | {c(fe)} |")
            RES[f"{y}|{lab}"] = {"ch": [float(chL[0]), sd(chL[1])], "chC": [float(chC[0]), sd(chC[1])],
                                 "dif": [float(chL[0] - chC[0]), sd(chL[1] - chC[1])], "fe": list(map(float, fe))}
            print(md[-1], flush=True)
    md.append("")
    (OUT / "prewindow_income.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "prewindow_income.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
