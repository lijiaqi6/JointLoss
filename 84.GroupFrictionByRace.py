r"""Group search friction by race and state in the son's childhood, from the CPS (Paper B primary goal, component 4:
"search friction faced by a group"; 75.WhatIsPassedOn.py measured the group component with the state's unemployment
rate and a Bartik labour-demand shock only, which are the same for Black and White families in a state).

MEASURES (CPS aggregates already built by 17.AtlasFrictions.py; read only)
  g_jf    MONTHLY JOB FINDING of non-employed men of the son's race in his state at 17 = P(employed at t+1 | not
          employed at t), CPS basic monthly 1994-2021 matched across adjacent months (data/atlas_cps_monthly.pkl:
          weighted counts fNE (non-employed at t, matched) and fNE_E (of whom employed at t+1); ages 20-45 at t), pooled
          over the son's calendar years at ages 12-18 (sum fNE_E / sum fNE; >= 3 years and >= 40 unweighted matched
          non-employed men). Sons born 1976+.
  g_jf_f  the same for women of the son's race (his mother's labour market).
  g_re    ANNUAL RE-EMPLOYMENT of men of his race in his state, March CPS 1977-1992 (Mare-Winship extracts,
          data/atlas_mare_winship.pkl): employed in the March survey week among those with 0 weeks worked in the
          previous year, pooled over his ages 12-18 (>= 3 years, >= 20 unweighted non-employed men). Sons born 1959-1980.
          Black cells are small (median 3 non-employed men per state-year), so it is reported as a second measure.
  g_gap   White minus Black monthly job finding of men in his state (the racial friction of his place).
  Each standardised over sons (weighted), so a contribution is per s.d. of the measure.
DESIGN: 75's son-years and components (R75.build()); GROUP = {g_ur, g_bart} + the CPS measure(s); 75's exact Gelbach
  split (74's run_spec), 200 cluster-bootstrap draws of 1968 families stratified by race; pooled and by race. Each
  design is on the sons with the measure, with 75's group as the comparison on the same sons. Also: the racial gap in
  the measure among the sons, its gradient in ln parental income within race (does a richer Black family live where
  Black men find jobs faster?), and the 4 x 4 row (son's outcome on the standardised measure at equal lyp and
  components).
Writes output/group_friction_by_race.md and .json (aggregates only). Descriptive accounting.
"""
import importlib.util
import json
import sys
import time
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


R75 = _load("s75", "75.WhatIsPassedOn.py")
R74, R72 = R75.R74, R75.R72
c, wreg, Boot, run_spec, est, cc = R74.c, R74.wreg, R74.Boot, R74.run_spec, R74.est, R74.cc
CELLS, CLAB = (0, 2, 4, 6), R75.CLAB
RES = {}


def windows(one):
    st = R72.state17(one[["pid", "birth_year"]].copy()).dropna(subset=["fips17"])
    st = st.merge(one[["pid", "race"]], on="pid")
    st["black"] = (st["race"] == "Black").astype(int)
    rows = st.assign(key=1).merge(pd.DataFrame({"off": range(12, 19), "key": 1}), on="key")
    rows["year"] = (rows["birth_year"] + rows["off"]).astype(int)
    M = pd.read_pickle(DATA / "atlas_cps_monthly.pkl")
    M["year"] = M["ym"] // 100
    A = M.groupby(["state", "sex", "black", "year"])[["fNE", "fNE_E", "nNE"]].sum().reset_index()
    out = []
    for sex, tag in ((1, "g_jf"), (2, "g_jf_f")):
        a = A[A.sex == sex].rename(columns={"state": "fips17"})
        z = rows.merge(a, on=["fips17", "black", "year"], how="left")
        g = z.groupby("pid")
        ok = (g["fNE"].count() >= 3) & (g["nNE"].sum() >= 40)
        out.append((g["fNE_E"].sum() / g["fNE"].sum()).where(ok).rename(tag))
    # racial gap of men's job finding in his state (both races' rates, his years)
    a = A[A.sex == 1].rename(columns={"state": "fips17"})
    zz = rows.drop(columns="black").merge(a, on=["fips17", "year"], how="left")
    g = zz.groupby(["pid", "black"])
    r_ = (g["fNE_E"].sum() / g["fNE"].sum()).where((g["fNE"].count() >= 3) & (g["nNE"].sum() >= 40)).unstack()
    out.append((r_.get(0) - r_.get(1)).rename("g_gap"))
    W = pd.read_pickle(DATA / "atlas_mare_winship.pkl")
    w = W[W.sex == 1].rename(columns={"fips": "fips17"})
    z = rows.merge(w, on=["fips17", "black", "year"], how="left")
    g = z.groupby("pid")
    ok = (g["wNW"].count() >= 3) & (g["nNW"].sum() >= 20)
    out.append((g["wNW_E"].sum() / g["wNW"].sum()).where(ok).rename("g_re"))
    return pd.concat(out, axis=1).reset_index().rename(columns={"index": "pid"})


def zs(r, v):
    one = r.drop_duplicates("pid")
    q = one[one[v].notna()]
    mu, sd = np.average(q[v], weights=q["wt"]), np.sqrt(np.cov(q[v], aweights=q["wt"]))
    return (r[v] - mu) / sd


def split_table(md, title, res, gl):
    md += [f"#### {title}", "", "| component | " + " | ".join(CLAB[k] for k in CELLS) + " | share 25-55 |",
           "|---" * 6 + "|"]
    md.append("| IGE (b0) | " + " | ".join(cc(est(res, k, "b0", 0)) for k in CELLS) + " | |")
    for gname in list(gl) + ["b"]:
        stat = "b" if gname == "b" else f"c:{gname}"
        e6 = est(res, 6, stat, 0, share=True)
        RES[f"{title}|{gname}"] = {"contrib": [list(e[:2]) if e else None for e in [est(res, k, stat, 0)
                                                                                for k in CELLS]],
                                  "share": [float(e6[0]), float(e6[1])] if e6 else None}
        md.append(f"| {R75.GLAB.get(gname, gname) if gname != 'b' else 'rest'} | "
                  + " | ".join(cc(est(res, k, stat, 0)) for k in CELLS) + f" | {cc(est(res, 6, stat, 0, share=True))} |")
    for kk, col in enumerate(res["cols"]):
        if col.startswith("g_"):
            md.append(f"| element {col} | " + " | ".join(cc(est(res, k, f'e:{kk}', 0)) for k in CELLS) + " | |")
            RES[f"{title}|{col}"] = [list(e[:2]) if e else None for e in [est(res, k, f"e:{kk}", 0) for k in CELLS]]
    n = res["n"]
    md += [f"Sons / son-years / families: {n[0]:,} / {n[1]:,} / {n[2]:,}.", ""]


def main():
    t0 = time.time()
    r = R75.build()
    one = r.drop_duplicates("pid")
    G = windows(one)
    r = r.merge(G, on="pid", how="left")
    for v in ("g_jf", "g_jf_f", "g_gap", "g_re"):
        r[v + "_z"] = zs(r, v)
    one = r.drop_duplicates("pid")
    md = ["# Group search friction by race and state in childhood (CPS) and the IGE", "",
          "Built by `84.GroupFrictionByRace.py` (2026-10-20); measures and design in its docstring. PSID sons 25-55; "
          f"estimate (s.e.; p), *** p<0.01, ** p<0.05, * p<0.1; {R74.NBOOT} cluster-bootstrap draws of 1968 families "
          "stratified by race. **Descriptive accounting.**", "", "## 1. The measures among the sons", "",
          "| measure | sons with it (White / Black) | White mean | Black mean | Black - White (s.e.; p) | gradient in lyp, "
          "White | gradient in lyp, Black |", "|---" * 7 + "|"]
    lab = {"g_jf": "men's monthly job finding, own race, state (CPS 1994-2021)",
           "g_jf_f": "women's monthly job finding, own race, state (CPS 1994-2021)",
           "g_gap": "White - Black men's job finding in the state (CPS 1994-2021)",
           "g_re": "men's annual re-employment, own race, state (March CPS 1977-92)"}
    for v in ("g_jf", "g_jf_f", "g_gap", "g_re"):
        q = one[one[v].notna()].assign(blk=lambda z: (z.race == "Black").astype(float), age=0)
        wm = [np.average(q.loc[q.race == rr, v], weights=q.loc[q.race == rr, "wt"]) if (q.race == rr).any() else np.nan
              for rr in ("White", "Black")]
        gap = wreg(q, v, ["blk"], age_dummies=False)[0]["blk"]
        gr = [wreg(q[q.race == rr], v, ["lyp"], age_dummies=False)[0]["lyp"] for rr in ("White", "Black")]
        md.append(f"| {lab[v]} | {int((q.race == 'White').sum()):,} / {int((q.race == 'Black').sum()):,} | {wm[0]:.4f} | "
                  f"{wm[1]:.4f} | {c(gap, 4)} | {c(gr[0], 4)} | {c(gr[1], 4)} |")
        RES[f"measure|{v}"] = {"means": wm, "gap": list(gap), "grad_W": list(gr[0]), "grad_B": list(gr[1])}
    md.append("")
    BT = Boot(r["fam68"].to_numpy(), r["race"].to_numpy())
    designs = [("monthly job finding of men and women of his race (CPS 1994-2021)", ["g_jf_z", "g_jf_f_z"], "g_jf"),
               ("+ the White - Black job-finding gap of his state", ["g_jf_z", "g_jf_f_z", "g_gap_z"], "g_jf"),
               ("annual re-employment of men of his race (March CPS 1977-92)", ["g_re_z"], "g_re")]
    for title, add, need in designs:
        md += [f"## 2. {title}", ""]
        for samp, d in (("pooled", r), ("White", r[r.race == "White"]), ("Black", r[r.race == "Black"])):
            d = d[d[need].notna() & d["lw"].notna()]
            d = d.dropna(subset=add)                                   # same sons in both splits
            if d["pid"].nunique() < 150:
                md += [f"{samp}: {d['pid'].nunique()} sons, not run.", ""]
                continue
            g0 = dict(R75.GROUPS)
            g1 = {**R75.GROUPS, "group": R75.GROUPS["group"] + add}
            if samp != "pooled":                                        # constant within race: drop
                g1["group"] = [v for v in g1["group"] if d[v].std() > 1e-9]
            r0 = run_spec(d, ["ly"], g0, BT, cells=CELLS)
            r1 = run_spec(d, ["ly"], g1, BT, cells=CELLS)
            split_table(md, f"{samp}, ln earnings, 75's group on the same sons", r0, list(g0))
            split_table(md, f"{samp}, ln earnings, group with {', '.join(add)}", r1, list(g1))
            # 4x4 row: partial relation of the son's outcomes to the measures
            comps = [v for g_ in ("wage", "hours", "stability") for v in R75.GROUPS[g_]] + g1["group"]
            xs = [v for v in ["lyp"] + comps + R75.GROUPS["structure"] if d[v].std() > 0]
            outs = [(y, wreg(d[d[y].notna()], y, xs)) for y in ("lw", "lh")] + \
                   [(y, wreg(r[(r.pid.isin(d.pid)) & r[y].notna()], y, xs)) for y in ("emp", "sb_unemp")]
            md += [f"{samp}: partial coefficients of the son's outcomes (25-55) at equal lyp and all components: "
                   + "; ".join(f"{R75.OL[y]}: " + ", ".join(f"{v} {c(o[0][v])}" for v in add if v in o[0])
                               for y, o in outs), ""]
            for y, o in outs:
                for v in add:
                    if v in o[0]:
                        RES[f"{title}|{samp}|4x4|{y}|{v}"] = list(o[0][v])
        print(f"{title} {time.time() - t0:.0f}s", flush=True)
    (OUT / "group_friction_by_race.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "group_friction_by_race.json", "w"), indent=1, default=float)
    print(f"done {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
