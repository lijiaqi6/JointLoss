r"""Does a father's teen layoff leave the family poorer in wealth, and does wealth carry the son's delayed cost?
(Paper B exploration, 2026-10-24)

Wealth carries three tenths of the IGE where it is measured (98). If a father's layoffs in the son's teens deplete the
family's wealth, the son loses what wealth buys later (help with a house, a business, a fall-back), which could show
in his forties. PSID net worth with home equity (18's wealth(): 1984, 1989, 1994, 1999 on; 2000 dollars):
  (1) the parents' net worth when the son is 20-30 (the father's family unit, mean over the wealth waves), as asinh and
      as its rank within the son's birth year, on the father's teen layoff share (one row per son; at equal ln parental
      income and all of 75's components; PSID weights; clustered by 1968 family);
  (2) the son's own net worth at 35-49 (his family unit) on the teen layoff share, the same controls;
  (3) the within-son ln earnings slope of the layoff share with the parents' later net worth (rank) x age added, on the
      sons who have it.
75's baseline sample, father present. DESCRIPTIVE. Writes output/layoff_wealth.md / .json (aggregates only).
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


R91 = _load("s91", "91.LayoffSelection.py")
R18 = _load("s18", "18.HusbandIndustryShocks.py")
R93 = _load("s93", "93.LayoffIndustryShocks.py")
R75, R24 = R91.R75, R91.R24
c, dummies = R91.c, R91.dummies
COMPS, STRUCT = R91.COMPS, R91.STRUCT
CACHE = DATA / "layoff_wealth_items.pkl"
RES = {}


def wealth_waves():
    if CACHE.exists():
        return pd.read_pickle(CACHE)
    W = R18.wealth()[["wave", "int", "wealth2"]].rename(columns={"wealth2": "nw"})
    W.to_pickle(CACHE)
    return W


def main():
    r = R75.build()
    r = r[r["nofa"] == 0].copy()
    W = wealth_waves()
    a = pd.read_pickle(R24.CACHE)
    fa = a[a["head"] & (a["female"] == 0)][["pid", "wave", "int"]].rename(columns={"pid": "fpid"}).drop_duplicates()
    sons = r.drop_duplicates("pid")[["pid", "fpid", "birth_year"]].dropna()
    rows = sons.assign(key=1).merge(pd.DataFrame({"off": range(20, 31), "key": 1}), on="key")
    rows["wave"] = (rows["birth_year"] + rows["off"] + 1).astype(int)
    rows = rows.merge(fa, on=["fpid", "wave"]).merge(W, on=["wave", "int"])
    pw = rows.groupby("pid")["nw"].mean().rename("par_nw")
    sw = r[r["age"].between(35, 49)].merge(W, on=["wave", "int"]).groupby("pid")["nw"].mean().rename("son_nw")
    one = r.drop_duplicates("pid").set_index("pid").join(pw).join(sw).reset_index()
    for v in ("par_nw", "son_nw"):
        one[f"{v}_as"] = np.arcsinh(one[v] / 1000)
        one[f"{v}_rk"] = one.groupby("birth_year")[v].rank(pct=True)
    ctl = [x for x in ["lyp"] + COMPS + STRUCT if one[x].std() > 0]
    jl = ctl.index("f_sh_layoff")
    jc = ctl.index("f_sh_close")
    md = ["# A father's teen layoff and the family's wealth", "",
          "Built by `117.LayoffWealth.py` (2026-10-24); design in its docstring. Per unit teen layoff share (one layoff year = "
          "1/7). *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**", "",
          "| outcome | mean | layoff share | closure share | sons |", "|---|---|---|---|---|"]
    for y, lab in (("par_nw_as", "parents' net worth at the son's 20-30, asinh($1,000)"),
                   ("par_nw_rk", "parents' net worth at 20-30, rank within birth year"),
                   ("son_nw_as", "son's net worth at 35-49, asinh($1,000)"),
                   ("son_nw_rk", "son's net worth at 35-49, rank within birth year")):
        q = one.dropna(subset=[y])
        X = np.column_stack([q[ctl].to_numpy(float), dummies(q["birth_year"] // 5), np.ones(len(q))])
        b, V, _ = R93.ols(X, q[y].to_numpy(float), q["wt"].to_numpy(float), q["fam68"].to_numpy())
        lay, clo = (b[jl], np.sqrt(V[jl, jl])), (b[jc], np.sqrt(V[jc, jc]))
        md.append(f"| {lab} | {np.average(q[y], weights=q['wt']):.3f} | {c(lay)} | {c(clo)} | {len(q):,} |")
        RES[y] = {"layoff": list(map(float, lay)), "closure": list(map(float, clo)), "n": len(q)}
    md.append("")
    # (3) within son with the parents' later wealth x age
    r = r.merge(one[["pid", "par_nw_rk"]], on="pid", how="left")
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    cohd = pd.get_dummies(r["coh5"], prefix="coh", drop_first=True).astype(float)
    r = pd.concat([r, cohd], axis=1)
    r["agec"] = (r["age"] - 40) / 10
    XB = R91.xage(r, ["lyp"] + COMPS + STRUCT + list(cohd.columns))
    R91.xage(r, ["par_nw_rk"])
    v = r[r["lw"].notna() & r["par_nw_rk"].notna()].copy()
    g = lambda f, x: (f["b"][x], float(np.sqrt(f["V"].loc[x, x])))  # noqa: E731
    f0 = R91.fe_fit(v, "ly", XB)
    f1 = R91.fe_fit(v, "ly", XB + ["par_nw_rk_xa"])
    md += ["## The within-son ln earnings slope with the parents' later net worth (rank) x age", "",
           f"Sons with the parents' net worth at 20-30: {v['pid'].nunique():,}. Layoff share x age: {c(g(f0, 'f_sh_layoff_xa'))} "
           f"-> {c(g(f1, 'f_sh_layoff_xa'))} with the parents' wealth rank x age ({c(g(f1, 'par_nw_rk_xa'))}).", ""]
    RES["fe"] = {"base": list(g(f0, "f_sh_layoff_xa")), "with": list(g(f1, "f_sh_layoff_xa")), "own": list(g(f1, "par_nw_rk_xa")),
                 "sons": int(v["pid"].nunique())}
    (OUT / "layoff_wealth.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "layoff_wealth.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
