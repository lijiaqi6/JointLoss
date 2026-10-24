r"""Total consumption in the self-employed years (committee re-read memo, action 1 remainder, 2026-10-24)

133: in the self-employed years of sons of laid-off fathers, reported earnings and food spending fall behind with age
but net worth does not. Here the family's total consumption (Paper A's nondurables + services, 47.PSIDConsumptionEvent's
cache, 2000 dollars, waves 1999-2021): within son, the layoff share x (age-40)/10 in employee and self-employed years
and the layoff x age x self-employed interaction (75's controls, 91's fe_fit).
Writes output/se_consumption.md / .json (aggregates only). DESCRIPTIVE.
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


R118 = _load("s118", "118.SonsEmployerType.py")
R91, R75 = R118.R91, R118.R75
c, COMPS, STRUCT = R91.c, R91.COMPS, R91.STRUCT
RES = {}


def main():
    r = R75.build()
    r = r.merge(R118.items()[["wave", "int", "self"]], on=["wave", "int"], how="left")
    C = pd.read_pickle(DATA / "psid_consumption_9921.pkl")["C"][["wave", "int", "r_totcons_t"]].drop_duplicates(["wave", "int"])
    r = r.merge(C, on=["wave", "int"], how="left")
    r["lcons"] = np.log(r["r_totcons_t"])
    r["selfemp"] = r["self"].isin([2, 3]).astype(float).where(r["self"].isin([1, 2, 3]))
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    cohd = pd.get_dummies(r["coh5"], prefix="coh", drop_first=True).astype(float)
    r = pd.concat([r, cohd], axis=1)
    r["agec"] = (r["age"] - 40) / 10
    XB = R91.xage(r, ["lyp"] + COMPS + STRUCT + list(cohd.columns))
    v = r[r["lw"].notna()].dropna(subset=["selfemp", "lcons"]).copy()
    v["lay_self_xa"] = v["f_sh_layoff"] * v["selfemp"] * v["agec"]
    v["self_xa"] = v["selfemp"] * v["agec"]
    g = lambda f, x: (f["b"][x], float(np.sqrt(f["V"].loc[x, x])))  # noqa: E731
    md = ["# Total consumption in the self-employed years (committee re-read memo, action 1 remainder)", "",
          "Built by `142.SelfEmploymentConsumption.py` (2026-10-24); design in its docstring. *** p<0.01, ** p<0.05, "
          "* p<0.1. **Descriptive.**", "", "| outcome | employee years | self-employed years | interaction | son-years |",
          "|---|---|---|---|---|"]
    for y, lab in (("ly", "ln earnings (same son-years)"), ("lcons", "ln total consumption")):
        fE = R91.fe_fit(v[v["selfemp"] == 0], y, XB)
        fS = R91.fe_fit(v[v["selfemp"] == 1], y, XB)
        fA = R91.fe_fit(v, y, XB + ["selfemp", "self_xa", "lay_self_xa"])
        md.append(f"| {lab} | {c(g(fE, 'f_sh_layoff_xa'))} | {c(g(fS, 'f_sh_layoff_xa'))} | {c(g(fA, 'lay_self_xa'))} | "
                  f"{fA['n']:,} |")
        RES[y] = {"emp": list(g(fE, "f_sh_layoff_xa")), "se": list(g(fS, "f_sh_layoff_xa")), "inter": list(g(fA, "lay_self_xa")),
                  "n": fA["n"], "se_years": int((v["selfemp"] == 1).sum())}
    md.append(f"\nSelf-employed son-years with consumption: {int((v['selfemp'] == 1).sum()):,}.\n")
    (OUT / "se_consumption.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "se_consumption.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
