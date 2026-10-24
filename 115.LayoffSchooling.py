r"""Does schooling carry the father's layoff's delayed cost to sons and its gain to daughters? (Paper B exploration,
2026-10-24)

Section 3: the return to schooling rises with age. 109: a father's teen layoff goes with 0.89 more years of schooling for
daughters than for sons (p = 0.069). If a teen layoff lowers sons' schooling and raises daughters', and schooling pays
more with age, schooling would produce both age profiles.
  A  SONS (75's baseline sample; at equal ln parental income and all of 75's components; PSID weights; clustered by 1968
     family): (1) one row per son - years of schooling, college (16+ years) and some college (13+) on the teen layoff
     and closure shares; (2) the within-son ln earnings and ln wage slopes of the layoff share (son FE, every component,
     lyp, structure and cohort x (age-40)/10) without and with years of schooling x age (and college x age);
     (3) the band change 45-49 - 25-29 without and with schooling (91's band_fit, 200 draws).
  B  SONS AND DAUGHTERS (107's stacked reduced specification): schooling and college on the layoff share by sex and the
     difference; the within-person wage slopes by sex and their difference, without and with schooling x age (by sex).
Schooling = the child's highest years of schooling observed at 25-55 (24's educ; 0-20). Writes
output/layoff_schooling.md / .json (aggregates only). DESCRIPTIVE.
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
R107 = _load("s107", "107.LayoffSexDifference.py")
R93 = _load("s93", "93.LayoffIndustryShocks.py")
R75, R24 = R91.R75, R91.R24
c, fmt, sd, Boot, dummies = R91.c, R91.fmt, R91.sd, R91.Boot, R91.dummies
ols_cl = R107.ols_cl
COMPS, STRUCT = R91.COMPS, R91.STRUCT
RES = {}


def main():
    md = ["# Does schooling carry the layoff's delayed cost to sons and its gain to daughters?", "",
          "Built by `115.LayoffSchooling.py` (2026-10-24); design in its docstring. Per unit teen layoff share (one layoff "
          "year = 1/7). *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**", ""]
    # ---------------- A. sons, baseline sample
    r = R75.build()
    ed = r[r["educ"].between(0, 20)].groupby("pid")["educ"].max()
    r["sch"] = r["pid"].map(ed)
    r = r[r["sch"].notna()].copy()
    r["coll"] = (r["sch"] >= 16).astype(float)
    r["some"] = (r["sch"] >= 13).astype(float)
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    cohd = pd.get_dummies(r["coh5"], prefix="coh", drop_first=True).astype(float)
    r = pd.concat([r, cohd], axis=1)
    r["agec"] = (r["age"] - 40) / 10
    XB = R91.xage(r, ["lyp"] + COMPS + STRUCT + list(cohd.columns))
    R91.xage(r, ["sch", "coll"])
    one = r.drop_duplicates("pid")
    ctl = [x for x in ["lyp"] + COMPS + STRUCT if one[x].std() > 0]
    md += ["## A1. Sons' schooling on the father's teen layoff and closure shares (one row per son)", "",
           "| outcome | mean | layoff share | closure share | sons |", "|---|---|---|---|---|"]
    for y, lab in (("sch", "years of schooling"), ("coll", "college (16+ years)"), ("some", "some college (13+)")):
        X = np.column_stack([one[ctl].to_numpy(float), dummies(one["coh5"]), np.ones(len(one))])
        b, V, _ = R93.ols(X, one[y].to_numpy(float), one["wt"].to_numpy(float), one["fam68"].to_numpy())
        jl, jc = ctl.index("f_sh_layoff"), ctl.index("f_sh_close")
        lay, clo = (b[jl], np.sqrt(V[jl, jl])), (b[jc], np.sqrt(V[jc, jc]))
        md.append(f"| {lab} | {np.average(one[y], weights=one['wt']):.3f} | {c(lay)} | {c(clo)} | {len(one):,} |")
        RES[f"A1|{y}"] = {"layoff": list(map(float, lay)), "closure": list(map(float, clo))}
    md.append("")
    md += ["## A2. Within the same son: the layoff share x age, without and with schooling x age", "",
           "| outcome | as before | + years of schooling x age | + college x age | sons |", "|---|---|---|---|---|"]
    v = r[r["lw"].notna()].copy()
    for y, lab in (("ly", "ln earnings"), ("lw", "ln hourly wage")):
        out = []
        for extra in ([], ["sch_xa"], ["coll_xa"]):
            f = R91.fe_fit(v, y, XB + extra)
            out.append((f["b"]["f_sh_layoff_xa"], float(np.sqrt(f["V"].loc["f_sh_layoff_xa", "f_sh_layoff_xa"]))))
            if extra == ["sch_xa"]:
                RES[f"A2|{y}|sch_xa"] = [float(f["b"]["sch_xa"]), float(np.sqrt(f["V"].loc["sch_xa", "sch_xa"]))]
        md.append(f"| {lab} | " + " | ".join(c(o) for o in out) + f" | {v['pid'].nunique():,} |")
        RES[f"A2|{y}"] = [list(map(float, o)) for o in out]
    md.append("")
    BT = Boot(v["fam68"].to_numpy(), v["race"].to_numpy())
    md += ["## A3. The band change 45-49 - 25-29 of the layoff share, without and with schooling", "",
           "| outcome | as before | + years of schooling |", "|---|---|---|"]
    for y, lab in (("ly", "ln earnings"), ("lw", "ln hourly wage")):
        cells = []
        for ctrl in ((), ("sch",)):
            a0 = R91.band_fit(v, y, 0, BT, COMPS, ["f_sh_layoff"], ctrl)["f_sh_layoff"]
            a4 = R91.band_fit(v, y, 4, BT, COMPS, ["f_sh_layoff"], ctrl)["f_sh_layoff"]
            cells.append((a4[0] - a0[0], a4[1] - a0[1]))
        md.append(f"| {lab} | {fmt(cells[0])} | {fmt(cells[1])} |")
        RES[f"A3|{y}"] = [[float(x[0]), sd(x[1])] for x in cells]
    md.append("")
    print("A done", flush=True)
    # ---------------- B. sons and daughters, 107's reduced specification
    a, py, ch = R24.load()
    q = R107.frame(a, py, ch)
    edq = q[q["educ"].between(0, 20)].groupby("pid")["educ"].max()
    q["sch"] = q["pid"].map(edq)
    q = q[q["sch"].notna()].copy()
    X0 = ["lyp", "f_lw", "f_lh", "f_sh_unemp", "f_sh_zero", "f_vtr", "f_sh_close", "f_sh_layoff"]
    kL = X0.index("f_sh_layoff")
    one = q.drop_duplicates("pid").dropna(subset=X0)
    md += ["## B1. Schooling by sex (one row per child, stacked, every regressor x daughter)", "",
           "| outcome | sons | daughters | daughters - sons | children |", "|---|---|---|---|---|"]
    one["coll"] = (one["sch"] >= 16).astype(float)
    for y, lab in (("sch", "years of schooling"), ("coll", "college (16+ years)")):
        fe = one["female"].to_numpy(float)[:, None]
        base = np.column_stack([one[X0].to_numpy(float), dummies(one["birth_year"] // 5), np.ones(len(one))])
        b, V = ols_cl(np.column_stack([base, base * fe]), one[y].to_numpy(float), one["wt"].to_numpy(float),
                      one["fam68"].to_numpy())
        K = base.shape[1]
        son = (b[kL], np.sqrt(V[kL, kL]))
        dau = (b[kL] + b[K + kL], np.sqrt(V[kL, kL] + V[K + kL, K + kL] + 2 * V[kL, K + kL]))
        dif = (b[K + kL], np.sqrt(V[K + kL, K + kL]))
        md.append(f"| {lab} | {c(son)} | {c(dau)} | {c(dif)} | {len(one):,} |")
        RES[f"B1|{y}"] = {"sons": list(map(float, son)), "daughters": list(map(float, dau)), "diff": list(map(float, dif))}
    md += ["", "## B2. Within-person ln wage slopes of the layoff share by sex, without and with schooling x age (by sex)", "",
           "| spec | sons | daughters | daughters - sons |", "|---|---|---|---|"]
    d = q.dropna(subset=["lw"] + X0)
    ag = d["agec"].to_numpy()[:, None]
    fd = d["female"].to_numpy()[:, None]
    for lab, extra in (("as in 107", []), ("+ schooling x age (by sex)", ["sch"])):
        Z = d[X0 + extra].to_numpy(float) * ag
        Xw = np.column_stack([Z, Z * fd, dummies(d["age"]), dummies(d["age"]) * fd])
        b, V = ols_cl(Xw, d["lw"].to_numpy(float), d["wt"].to_numpy(float), d["fam68"].to_numpy(), absorb=d["pid"].to_numpy())
        n0 = len(X0) + len(extra)
        son = (b[kL], np.sqrt(V[kL, kL]))
        dau = (b[kL] + b[n0 + kL], np.sqrt(V[kL, kL] + V[n0 + kL, n0 + kL] + 2 * V[kL, n0 + kL]))
        dif = (b[n0 + kL], np.sqrt(V[n0 + kL, n0 + kL]))
        md.append(f"| {lab} | {c(son)} | {c(dau)} | {c(dif)} |")
        RES[f"B2|{lab}"] = {"sons": list(map(float, son)), "daughters": list(map(float, dau)), "diff": list(map(float, dif))}
    md.append("")
    (OUT / "layoff_schooling.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "layoff_schooling.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
