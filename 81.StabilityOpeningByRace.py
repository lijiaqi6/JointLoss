r"""Does the stability component open with age for White sons and not for Black sons? A formal test (Paper B primary
goal; follows 75.WhatIsPassedOn.py, EVIDENCE 11.29).

75 found the stability component's contribution to the earnings IGE opening between 25-29 and 45-49 for White sons
(0.066**, p = 0.011) and not for Black sons (-0.042, p = 0.273), with separate bootstrap draws by race. This script
tests the difference on common draws and asks where it sits.

DESIGN
  Son-years and components exactly as 75 (R75.build()); 75's exact Gelbach split (74's run_spec), x = lyp, by race,
  every band 25-29 ... 50-55 and 25-55. ONE set of 200 cluster-bootstrap draws of 1968 families stratified by race is
  shared by both races (74's Boot on the pooled frame), so the White - Black difference of any statistic has its draws.
  Tests, for each component (wage, hours, stability, group, structure, rest) and the IGE:
   (1) opening = contribution at 45-49 minus at 25-29, by race and White - Black;
   (2) age slope = OLS slope of the six band contributions on the band mid-ages (27, 32, 37, 42, 47, 52.5), per 10
       years, by race and White - Black (uses every band, not two);
   (3) the same with 5-year birth-cohort dummies added to every regression (are the openings across ages or across
       cohorts?).
  Stability's elements (father's closures, layoffs, unemployment, zero hours, transitory variance, not measured;
  mother's unemployment): openings by race and the difference. For each element the contribution g_k d_k is split into
  its two pieces at 25-29 and 45-49: d_k = gradient of the element in lyp (at equal age), g_k = its partial relation
  to the son's ln earnings (at equal lyp and all other components) - does the opening come from the son's earnings
  responding more to the childhood spells at older ages (g) or from the sons observed at older ages having a steeper
  gradient (d)?
  Outcome: ln earnings (valid years), with ln wage and ln hours for the stability component.
Writes output/stability_opening_by_race.md and .json (aggregates only). Descriptive accounting.
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
from common import OUT  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R75 = _load("s75", "75.WhatIsPassedOn.py")
R74 = R75.R74
c, wls, dummies, Boot, run_spec, est = R74.c, R74.wls, R74.dummies, R74.Boot, R74.run_spec, R74.est
MID = np.array([27, 32, 37, 42, 47, 52.5])
CL = ["25-29", "30-34", "35-39", "40-44", "45-49", "50-55", "25-55"]
ROWS = list(R75.GROUPS) + ["b", "b0"]
LAB = {**R75.GLAB, "b0": "IGE (b0)", "b": "rest"}
YS = ["ly", "lw", "lh"]
RES = {}


def stat_draws(res, k, stat, j):
    if k not in res or stat not in res[k]["pt"]:
        return None
    return res[k]["pt"][stat][j], res[k]["bs"][stat][:, j]


def slope(res, stat, j):
    pts, drs = [], []
    for k in range(6):
        t = stat_draws(res, k, stat, j)
        if t is None:
            return None
        pts.append(t[0])
        drs.append(t[1])
    m = (MID - MID.mean()) / 10
    p = float(np.dot(m, pts) / np.dot(m, m))
    d = (m @ np.array(drs)) / np.dot(m, m)
    return p, d


def opening(res, stat, j):
    a, b = stat_draws(res, 4, stat, j), stat_draws(res, 0, stat, j)
    return None if a is None or b is None else (a[0] - b[0], a[1] - b[1])


def fmt(t):
    return "" if t is None else c((t[0], float(np.nanstd(t[1], ddof=1))))


def diff(a, b):
    return None if a is None or b is None else (a[0] - b[0], a[1] - b[1])


def pieces(d, BT, cols, k):
    """g_k and d_k of each stability element in band k (point, draws), ln earnings."""
    z = d[d["band"] == k].dropna(subset=["ly", "lyp", "age", "fam68", "wt"] + cols)
    allc = [v for g in R75.GROUPS.values() for v in g]
    A = np.column_stack([dummies(z["age"]), np.ones(len(z))])
    x, Y, Med = z["lyp"].to_numpy(float), z[["ly"]].to_numpy(float), z[allc].to_numpy(float)
    w0 = z["wt"].to_numpy(float)
    ri = BT.rows(z["fam68"].to_numpy())
    ii = [allc.index(v) for v in cols]

    def one(w):
        sw = np.sqrt(w)
        keep = w > 0
        sw_, x_, A_, Y_, M_ = sw[keep], x[keep], A[keep], Y[keep], Med[keep]
        dd = wls(np.column_stack([x_, A_]), M_, sw_)[0]
        gg = wls(np.column_stack([x_, M_, A_]), Y_, sw_)[1:1 + M_.shape[1], 0]
        return gg[ii], dd[ii]

    g0, d0 = one(w0)
    G = np.zeros((BT.cnt.shape[0], len(ii)))
    D = np.zeros_like(G)
    for b in range(BT.cnt.shape[0]):
        G[b], D[b] = one(w0 * BT.cnt[b, ri])
    return g0, G, d0, D


def main():
    t0 = time.time()
    r = R75.build()
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    cohd = pd.get_dummies(r["coh5"], prefix="coh", drop_first=True).astype(float)
    r = pd.concat([r, cohd], axis=1)
    BT = Boot(r["fam68"].to_numpy(), r["race"].to_numpy())
    md = ["# The stability component's opening with age, White vs Black sons", "",
          "Built by `81.StabilityOpeningByRace.py` (2026-10-20); design in its docstring. Son-years, components and split "
          f"as `75.WhatIsPassedOn.py`; one set of {R74.NBOOT} cluster-bootstrap draws of 1968 families (stratified by race) "
          "shared by both races, so White - Black differences have their own draws; estimate (s.e.; p), *** p<0.01, "
          "** p<0.05, * p<0.1. Opening = 45-49 minus 25-29; slope = OLS slope of the six band contributions on the band "
          "mid-ages, per 10 years. **Descriptive accounting.**", ""]
    res = {}
    for spec, ctrl in (("main", ()), ("cohort", tuple(cohd.columns))):
        for race in ("White", "Black"):
            d = r[(r.race == race) & r["lw"].notna()]
            ct = tuple(v for v in ctrl if d[v].std() > 0)
            res[(spec, race)] = run_spec(d, YS, R75.GROUPS, BT, cells=range(7), ctrl=ct)
            print(f"{spec} {race} {time.time() - t0:.0f}s", flush=True)
    for spec, title in (("main", "single-age dummies"), ("cohort", "single-age dummies + 5-year birth-cohort dummies")):
        W, B = res[(spec, "White")], res[(spec, "Black")]
        for j, y in enumerate(YS if spec == "main" else ["ly"]):
            md += [f"## {R75.OL[y]}: contributions by band, {title}", "",
                   "| component | race | " + " | ".join(CL) + " | opening 45-49 - 25-29 | slope per 10 years |",
                   "|---" * 11 + "|"]
            for stat in (ROWS if y == "ly" else ["stability", "b0"]):
                st = stat if stat in ("b", "b0") else f"c:{stat}"
                for lab, R_ in (("White", W), ("Black", B)):
                    ent = [stat_draws(R_, k, st, j) for k in range(7)]
                    md.append(f"| {LAB[stat]} | {lab} | " + " | ".join(fmt(e) for e in ent)
                              + f" | {fmt(opening(R_, st, j))} | {fmt(slope(R_, st, j))} |")
                dif = [diff(stat_draws(W, k, st, j), stat_draws(B, k, st, j)) for k in range(7)]
                do = diff(opening(W, st, j), opening(B, st, j))
                ds = diff(slope(W, st, j), slope(B, st, j))
                md.append(f"| {LAB[stat]} | **White - Black** | " + " | ".join(fmt(e) for e in dif)
                          + f" | **{fmt(do)}** | **{fmt(ds)}** |")
                for nm, t in (("open_W", opening(W, st, j)), ("open_B", opening(B, st, j)), ("open_diff", do),
                              ("slope_W", slope(W, st, j)), ("slope_B", slope(B, st, j)), ("slope_diff", ds)):
                    if t is not None:
                        RES[f"{spec}|{y}|{stat}|{nm}"] = [t[0], float(np.nanstd(t[1], ddof=1))]
            n = W["n"], B["n"]
            md += [f"Sons / son-years / families: White {n[0][0]:,} / {n[0][1]:,} / {n[0][2]:,}; Black {n[1][0]:,} / "
                   f"{n[1][1]:,} / {n[1][2]:,}.", ""]
    # elements of stability, ln earnings
    W, B = res[("main", "White")], res[("main", "Black")]
    cols = W["cols"]
    stab = R75.GROUPS["stability"]
    md += ["## Stability's elements, ln earnings: contribution g d by race", "",
           "| element | White 25-29 | White 45-49 | White opening | Black 25-29 | Black 45-49 | Black opening | "
           "White - Black opening |", "|---" * 8 + "|"]
    for v in stab:
        kk = cols.index(v)
        st = f"e:{kk}"
        e = [stat_draws(W, 0, st, 0), stat_draws(W, 4, st, 0), opening(W, st, 0), stat_draws(B, 0, st, 0),
             stat_draws(B, 4, st, 0), opening(B, st, 0)]
        md.append(f"| {v} | " + " | ".join(fmt(t) for t in e) + f" | {fmt(diff(e[2], e[5]))} |")
        RES[f"element|{v}|open_diff"] = [diff(e[2], e[5])[0], float(np.nanstd(diff(e[2], e[5])[1], ddof=1))]
    md.append("")
    md += ["## Stability's elements: g (partial relation to the son's ln earnings) and d (gradient in ln parental "
           "income), 25-29 and 45-49", "",
           "| element | race | g 25-29 | g 45-49 | g change | d 25-29 | d 45-49 | d change |", "|---" * 8 + "|"]
    for race in ("White", "Black"):
        d = r[(r.race == race) & r["lw"].notna()]
        P = {k: pieces(d, BT, stab, k) for k in (0, 4)}
        for i, v in enumerate(stab):
            g0, g4 = (P[0][0][i], P[0][1][:, i]), (P[4][0][i], P[4][1][:, i])
            d0, d4 = (P[0][2][i], P[0][3][:, i]), (P[4][2][i], P[4][3][:, i])
            md.append(f"| {v} | {race} | {fmt(g0)} | {fmt(g4)} | {fmt(diff(g4, g0))} | {fmt(d0)} | {fmt(d4)} | "
                      f"{fmt(diff(d4, d0))} |")
            RES[f"pieces|{race}|{v}"] = {"g": [g0[0], g4[0]], "d": [d0[0], d4[0]]}
    md.append("")
    (OUT / "stability_opening_by_race.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "stability_opening_by_race.json", "w"), indent=1, default=float)
    print(f"done {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
