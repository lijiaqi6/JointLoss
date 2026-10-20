r"""Where in the son's career does the father's teen layoff cost show? (Fable round 2, Objection 3; plan step 4)

Section 5's career tools applied to the layoff (all at equal ln parental income and all of 75's components; PSID
weights; band coefficients with 200 common draws, within-son slopes with son FE and every component, lyp, structure and
cohort x (age-40)/10, clustered by 1968 family; 91's machinery):
  (a) BETWEEN OR WITHIN OCCUPATIONS: the son's ln wage = his occupation's CPS wage score (os, 27) + his wage within the
      occupation (res); the layoff coefficient on each at 25-29 and 45-49 and within son.
  (b) THE EARLY JOB: access to a good job at 25-34 (G25: the son's modal occupation x industry cell at 25-34 is in the
      well-paid, fast-growing set of 35 / 49), one row per son; and the cost after 35 with the early cell held fixed
      (early occupation-group and industry-group dummies x age in the within-son model).
  (c) SAME-EMPLOYER GROWTH: annual ln wage growth between interviews with the same employer (g_lw_t where stay == 1),
      at 25-34 and 35-55.
  (d) THE SON'S OWN CAREER: his displacement and unemployment (24's flags), job change (stay == 0) and tenure at
      35-49, by band and within son.
Decision rule (plan): a lower start in the fast-growing cells at 25-34 -> the cost is where the son starts; a shortfall
within cells after 40 -> look at his own displacement and job changes; if nothing carries it, the mechanism is open.
Writes output/layoff_career_mechanism.md / .json (aggregates only). DESCRIPTIVE.
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


R91 = _load("s91", "91.LayoffSelection.py")
R49 = _load("s49", "49.PaperBPolicyShocks.py")
R93 = _load("s93", "93.LayoffIndustryShocks.py")
R75 = R91.R75
c, Boot, fmt, sd, dummies = R91.c, R91.Boot, R91.fmt, R91.sd, R91.dummies
COMPS, STRUCT = R91.COMPS, R91.STRUCT
RES = {}


def main():
    r = R75.build()
    _, d49, S = R49.son_frames()
    early = d49.drop_duplicates("pid")[["pid", "egrp", "eo11", "eset"]]
    early["G25"] = (early["eset"] == 1).astype(float).where(early["eset"].notna())
    r = r.merge(early, on="pid", how="left")
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    cohd = pd.get_dummies(r["coh5"], prefix="coh", drop_first=True).astype(float)
    r = pd.concat([r, cohd], axis=1)
    COH = list(cohd.columns)
    r["agec"] = (r["age"] - 40) / 10
    for v in ["lyp"] + COMPS + STRUCT + COH:
        r[f"{v}_xa"] = r[v] * r["agec"]
    XB = [f"{v}_xa" for v in ["lyp"] + COMPS + STRUCT + COH]
    r["os_v"] = r["os"].where(r["valid"] & r["lw"].notna())
    r["res_v"] = r["res"].where(r["valid"] & r["lw"].notna())
    r["g_stay"] = r["g_lw_t"].where(r["stay"] == 1)
    r["moved"] = (1 - r["stay"]).where(r["stay"].notna())
    r["disp"] = pd.to_numeric(r["disp"], errors="coerce")
    r["unemp"] = pd.to_numeric(r["unemp"], errors="coerce")
    BT = Boot(r["fam68"].to_numpy(), r["race"].to_numpy())
    md = ["# Where in the son's career does the father's teen layoff cost show? (Fable round 2, Objection 3)", "",
          "Built by `106.LayoffCareerMechanism.py` (2026-10-20); design in its docstring. Coefficient of the father's teen "
          "layoff share (per unit share; one layoff year = 1/7). *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**", ""]

    def row(y, lab, sub=None, extra_fe=None):
        q = r if sub is None else r[sub]
        q = q.dropna(subset=[y])
        a = R91.band_fit(q, y, 0, BT, COMPS, ["f_sh_layoff"]).get("f_sh_layoff")
        b = R91.band_fit(q, y, 4, BT, COMPS, ["f_sh_layoff"]).get("f_sh_layoff")
        ch = (b[0] - a[0], b[1] - a[1]) if a and b else None
        f = R91.fe_fit(q, y, XB)
        fe = (f["b"]["f_sh_layoff_xa"], float(np.sqrt(f["V"].loc["f_sh_layoff_xa", "f_sh_layoff_xa"])))
        md.append(f"| {lab} | {fmt(a)} | {fmt(b)} | {fmt(ch)} | {c(fe)} | {q['pid'].nunique():,} |")
        RES[lab] = {"a": [float(a[0]), sd(a[1])] if a else None, "b": [float(b[0]), sd(b[1])] if b else None,
                    "ch": [float(ch[0]), sd(ch[1])] if ch else None, "fe": list(map(float, fe))}

    md += ["## (a) Between or within occupations; (c) same-employer growth; (d) the son's own career", "",
           "| outcome | 25-29 | 45-49 | change | within son x age | sons |", "|---|---|---|---|---|---|"]
    for y, lab in (("lw", "ln hourly wage"), ("os_v", "occupation wage score (between)"),
                   ("res_v", "wage within the occupation (within)"), ("g_stay", "same-employer annual wage growth"),
                   ("moved", "changed employer since the last interview"), ("tenure", "tenure with the employer (years)"),
                   ("disp", "displaced (closure / layoff) in the year"), ("unemp", "unemployed in the year")):
        row(y, lab)
    md.append("")
    # (b) the early job
    one = r.drop_duplicates("pid")
    one = one[one["G25"].notna()].copy()
    ctl = ["lyp"] + COMPS + STRUCT
    ctl = [v for v in ctl if one[v].std() > 0]
    X = np.column_stack([one[["f_sh_layoff"] + ctl].to_numpy(float), dummies(one["coh5"]), np.ones(len(one))])
    b, V, _ = R93.ols(X, one["G25"].to_numpy(float), one["wt"].to_numpy(float), one["fam68"].to_numpy())
    g25 = (b[0], np.sqrt(V[0, 0]))
    md += ["## (b) The early job", "",
           f"Good job at 25-34 (modal cell in the well-paid, fast-growing set) on the teen layoff share, one row per son "
           f"({len(one):,} sons, mean {np.average(one['G25'], weights=one['wt']):.3f}): {c(g25)}.", ""]
    RES["G25"] = list(map(float, g25))
    q = r[r["egrp"].notna() & r["eo11"].notna() & r["lw"].notna()].copy()
    E = np.column_stack([dummies(q["egrp"]), dummies(q["eo11"])]) * q["agec"].to_numpy()[:, None]
    for j in range(E.shape[1]):
        q[f"early_{j}"] = E[:, j]
    early_x = [f"early_{j}" for j in range(E.shape[1])]
    f0 = R91.fe_fit(q, "ly", XB)
    f1 = R91.fe_fit(q, "ly", XB + early_x)
    e0 = (f0["b"]["f_sh_layoff_xa"], float(np.sqrt(f0["V"].loc["f_sh_layoff_xa", "f_sh_layoff_xa"])))
    e1 = (f1["b"]["f_sh_layoff_xa"], float(np.sqrt(f1["V"].loc["f_sh_layoff_xa", "f_sh_layoff_xa"])))
    md += [f"Within-son ln earnings slope of the layoff share on sons with an early job ({q['pid'].nunique():,}): {c(e0)}; "
           f"with the early industry group and occupation group x age held fixed: {c(e1)}.", ""]
    RES["fe_early"] = {"base": list(map(float, e0)), "early_fixed": list(map(float, e1))}
    (OUT / "layoff_career_mechanism.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "layoff_career_mechanism.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
