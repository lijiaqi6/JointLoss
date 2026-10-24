r"""Mothers' own layoffs in two-parent families, and AFDC / TANF as a moderator (committee re-read memo, action 10, 2026-10-24)

131: in mother-headed families a mother's teen layoffs lower her daughters' within-child earnings profile (-0.561**)
and not her sons' (-0.079), while fathers' layoffs lower sons' profiles and raise daughters' wages: a same-sex
pattern? The direct test is in two-parent families, where both parents' job ends are reported.
(a) TWO-PARENT FAMILIES: 107's frame (sons and daughters, father present, 24's children); the mother = the wife of
    the head in the child's window waves; her layoff share = share of window waves with her own report of a layoff /
    firing (code 3, not a closure; 25's wife_events, waves 1984-2023, dated 1983-2022) in the income year or the year
    before; window waves from 1984 only. Within child: the mother's and the father's layoff shares x (age-40)/10, each
    by the child's sex, with 107's reduced controls x age, person FE, single-age dummies; PSID weights; clusters 1968
    family.
(b) AFDC / TANF: the state's maximum benefit for a family of three (UKCPR, policy_calendar.csv afdc_max3, 2000
    dollars), mean over the son's 12-18 in his state at 17, standardised; within son: layoff x age x benefit, with
    benefit x age, on 75's son-years (91's machinery).
Writes output/mothers_afdc.md / .json (aggregates only). DESCRIPTIVE.
"""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import CPI, DATA, OUT  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R107 = _load("s107", "107.LayoffSexDifference.py")
R25 = _load("s25", "25.JointJobLoss.py")
R91 = _load("s91", "91.LayoffSelection.py")
R101 = _load("s101", "101.EITCByAge.py")
R24, R75, R72 = R107.R24, R91.R75, R101.R72
c, ols, dummies = R101.c, R101.ols, R101.dummies
RES = {}


def mother_shares(rr, py):
    ev = R25.wife_events(py, R25.P23.extras()["R"])
    lay = ev["main"] - ev["strict"]
    kids = rr.drop_duplicates("pid")[["pid"]]
    k = py[py["child"] & py["age"].between(13, 19) & py["faminc"].between(R24.LO, R24.HI) & py["pid"].isin(kids["pid"])
           & (py["wave"] >= 1984)][["pid", "wave", "int"]]
    wf = py[py["wife"]][["wave", "int", "pid"]].rename(columns={"pid": "mpid"}).drop_duplicates(["wave", "int"])
    fw = k.merge(wf, on=["wave", "int"], how="inner")
    y = fw["wave"] - 1
    fw["mlay"] = [float((int(p), int(t)) in lay or (int(p), int(t) - 1) in lay) for p, t in zip(fw["mpid"], y)]
    g = fw.groupby("pid")["mlay"].agg(["mean", "size"])
    return g[g["size"] >= 3]["mean"].rename("m_sh_layoff")


def main():
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    md = ["# Mothers' own layoffs in two-parent families, and AFDC / TANF (committee re-read memo, action 10)", "",
          "Built by `139.MothersAndAFDC.py` (2026-10-24); design in its docstring. Within-person slopes x (age-40)/10 per "
          "unit share; s.e. clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**", ""]
    # (a)
    a, py24, ch = R24.load()
    rr = R107.frame(a, py24, ch)
    rr = rr.merge(mother_shares(rr, py), left_on="pid", right_index=True, how="inner")
    X0 = ["lyp", "f_lw", "f_lh", "f_sh_unemp", "f_sh_zero", "f_vtr", "f_sh_close"]
    one = rr.drop_duplicates("pid")
    md += ["## (a) Two-parent families: the mother's and the father's teen layoffs, by the child's sex", "",
           f"Children {len(one):,} ({int((one['female'] == 0).sum()):,} sons); with a mother's teen layoff year "
           f"{int((one['m_sh_layoff'] > 0).sum()):,} (sons {int(((one['m_sh_layoff'] > 0) & (one['female'] == 0)).sum()):,}); "
           f"with a father's {int((one['f_sh_layoff'] > 0).sum()):,}.", "",
           "| outcome | mother's layoffs: sons | mother's: daughters | daughters - sons | father's layoffs: sons | "
           "father's: daughters | children |", "|---|---|---|---|---|---|---|"]
    for y in ("ly", "lw"):
        d = rr.dropna(subset=[y] + X0 + ["m_sh_layoff", "f_sh_layoff"])
        aa = d["agec"].to_numpy()[:, None]
        fe_ = d["female"].to_numpy()[:, None]
        core = d[["m_sh_layoff", "f_sh_layoff"] + X0].to_numpy(float) * aa
        X = np.column_stack([core, core * fe_, dummies(d["age"]), dummies(d["age"]) * fe_])
        b, V = ols(X, d[y].to_numpy(float), d["wt"].to_numpy(float), d["fam68"].to_numpy(), absorb=d["pid"].to_numpy())
        n0 = 2 + len(X0)
        se = lambda i: float(np.sqrt(V[i, i]))  # noqa: E731
        lin = lambda i, j: (b[i] + b[j], float(np.sqrt(V[i, i] + V[j, j] + 2 * V[i, j])))  # noqa: E731
        ms, md_, mdiff = (b[0], se(0)), lin(0, n0), (b[n0], se(n0))
        fs, fd = (b[1], se(1)), lin(1, n0 + 1)
        md.append(f"| {y} | {c(ms)} | {c(md_)} | {c(mdiff)} | {c(fs)} | {c(fd)} | {d['pid'].nunique():,} |")
        RES[f"a|{y}"] = {"m_sons": list(map(float, ms)), "m_daughters": list(map(float, md_)), "m_diff": list(map(float, mdiff)),
                         "f_sons": list(map(float, fs)), "f_daughters": list(map(float, fd)), "n": int(d["pid"].nunique())}
        print(md[-1], flush=True)
    md.append("")
    # (b) AFDC
    r = R75.build()
    r = R72.state17(r)
    pc = pd.read_csv(DATA / "policy_calendar.csv", usecols=["state_fips", "year", "afdc_max3"])
    pc["real"] = [x * CPI[2000] / CPI[int(y)] if int(y) in CPI and pd.notna(x) else np.nan
                  for x, y in zip(pc["afdc_max3"], pc["year"])]
    rate = {(int(f), int(y)): v for f, y, v in zip(pc["state_fips"], pc["year"], pc["real"])}
    one = r.drop_duplicates("pid")[["pid", "birth_year", "fips17"]]
    vals = []
    for b_, f_ in zip(one["birth_year"], one["fips17"]):
        xs = [rate.get((int(f_), int(b_) + k)) for k in range(12, 19)] if pd.notna(f_) else []
        xs = [x for x in xs if x is not None and np.isfinite(x)]
        vals.append(np.mean(xs) if len(xs) >= 3 else np.nan)
    one["afdc"] = vals
    r = r.merge(one[["pid", "afdc"]], on="pid", how="left")
    q = r[r["lw"].notna() & r["afdc"].notna()].copy()
    mu, s_ = q.drop_duplicates("pid")["afdc"].mean(), q.drop_duplicates("pid")["afdc"].std()
    q["afdc_z"] = (q["afdc"] - mu) / s_
    q["coh5"] = (q["birth_year"] // 5 * 5).astype(int)
    cohd = pd.get_dummies(q["coh5"], prefix="coh", drop_first=True).astype(float)
    q = pd.concat([q, cohd], axis=1)
    q["agec"] = (q["age"] - 40) / 10
    XB = R91.xage(q, ["lyp"] + R91.COMPS + R91.STRUCT + list(cohd.columns) + ["afdc_z"])
    q["lay_afdc_xa"] = q["f_sh_layoff"] * q["afdc_z"] * q["agec"]
    q["lay_afdc"] = q["f_sh_layoff"] * q["afdc_z"]
    g = lambda f, x: (f["b"][x], float(np.sqrt(f["V"].loc[x, x])))  # noqa: E731
    md += ["## (b) AFDC / TANF maximum benefit in the son's teens as a moderator of the layoff's cost", "",
           f"Sons {q['pid'].nunique():,}; mean maximum benefit for three over 12-18 ${mu:,.0f} (s.d. ${s_:,.0f}, 2000 dollars).",
           "", "| outcome | layoff share x age | x age x benefit (per s.d.) | son-years |", "|---|---|---|---|"]
    for y in ("ly", "lw"):
        f = R91.fe_fit(q, y, XB + ["lay_afdc_xa"])
        md.append(f"| {y} | {c(g(f, 'f_sh_layoff_xa'))} | {c(g(f, 'lay_afdc_xa'))} | {f['n']:,} |")
        RES[f"b|{y}"] = {"lay": list(g(f, "f_sh_layoff_xa")), "inter": list(g(f, "lay_afdc_xa"))}
        print(md[-1], flush=True)
    md.append("")
    (OUT / "mothers_afdc.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "mothers_afdc.json", "w"), indent=1, default=float)
    print("\n".join(md))


if __name__ == "__main__":
    main()
