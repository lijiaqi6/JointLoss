r"""Does more generous unemployment insurance in childhood weaken the stability channel of the IGE? (Paper B primary
goal, policy row 3: "employment stability -> UI, income smoothing for families with children"; follows
75.WhatIsPassedOn.py, EVIDENCE 11.29)

QUESTION. 75's stability component (the parents' spells in the son's childhood) carries 6%*** of the pooled earnings
IGE and 13.5%*** at 45-49. If the channel is lost income during the spells, a more generous state UI system during
the son's childhood should weaken it: a father's layoff should cost the son less where UI replaces more of the wage.

UI GENEROSITY (12b.UIGenerosity.py, data/ui_generosity.csv; statutory, DOL Significant Provisions, July issues)
  ui     = maximum weekly benefit amount / the state's average weekly wage (max_wba_repl), mean over the son's income
           years at ages 12-18 in his state at 17 (72's state17, waves 1976+), >= 3 years. The statutory maximum relative
           to the state wage is the usual generosity measure (it does not move with who claims, unlike the average
           benefit / wage ratio). Alternative: ln of the maximum total benefit (maximum WBA x maximum weeks, 2000 $).
  ui_z   = ui standardised over sons (weighted).
DESIGNS (son-years 25-55 as 75; sons with a state at 17 and >= 3 UI years, i.e. born 1958+)
  (1) Interactions. ln earnings (and employment, his share of years unemployed) on ln parental income, all of 75's
      components (each standardised, 1 s.d.), its structure flags, ui_z, and ui_z x each stability element; placebo
      ui_z x the parents' wage elements. State-at-17 fixed effects absorbed and 5-year birth-cohort dummies, so ui_z
      varies across cohorts within a state (law changes and wage growth), single-age dummies, PSID weights, s.e.
      clustered by 1968 family. A negative coefficient on ui_z x (father's layoff share) = his layoff costs the son
      less where UI is more generous.
  (2) The Gelbach split by UI generosity. Sons above vs below the median of ui net of 5-year birth-cohort means (more vs
      less generous than other states for the same cohort). 75's exact split in each half, one set of 200 cluster-
      bootstrap draws of 1968 families stratified by race shared by both halves; the stability contribution and its
      share of the IGE in each half and the difference.
  Pooled and by race (race panels of (1); (2) pooled, as halves by race are small). (1) also on son-years at 40-55,
  where 75's stability contribution sits (0.060*** at 45-49 vs 0.017** at 25-29).
DESCRIPTIVE: UI generosity is not randomly assigned; state fixed effects remove its level differences across states.
Writes output/ui_stability_channel.md and .json (aggregates only).
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
STAB = R75.GROUPS["stability"]
WAGE = R75.GROUPS["wage"]
COMPS = [v for g in ("wage", "hours", "stability", "group") for v in R75.GROUPS[g]]
CELLS, CLAB = R75.CELLS, R75.CLAB
RES = {}


def ui_child(r):
    one = r.drop_duplicates("pid")[["pid", "birth_year"]].copy()
    st = R72.state17(one)
    ui = pd.read_csv(DATA / "ui_generosity.csv")[["state_fips", "year", "max_wba_repl", "max_benefit_2000"]]
    rows = st.dropna(subset=["fips17"]).assign(key=1).merge(pd.DataFrame({"off": range(12, 19), "key": 1}), on="key")
    rows["year"] = (rows["birth_year"] + rows["off"]).astype(int)
    rows = rows.merge(ui.rename(columns={"state_fips": "fips17"}), on=["fips17", "year"], how="left")
    g = rows.groupby("pid")
    U = pd.DataFrame({"ui": g["max_wba_repl"].mean().where(g["max_wba_repl"].count() >= 3),
                      "lmaxben": np.log(g["max_benefit_2000"].mean()).where(g["max_benefit_2000"].count() >= 3)})
    return st[["pid", "fips17"]].merge(U.reset_index(), on="pid", how="left")


def zs(z, v):
    one = z.drop_duplicates("pid")
    mu = np.average(one[v], weights=one["wt"])
    sd = np.sqrt(np.cov(one[v], aweights=one["wt"]))
    return (z[v] - mu) / sd if sd > 0 else 0.0 * z[v]


def main():
    t0 = time.time()
    r = R75.build()
    r = r.merge(ui_child(r), on="pid", how="left")
    r = r[r["ui"].notna() & r["fips17"].notna()].copy()
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    md = ["# UI generosity in childhood and the stability channel of the IGE", "",
          "Built by `82.UIStabilityChannel.py` (2026-10-20); design in its docstring. PSID sons 25-55 with a state at 17 "
          "and >= 3 UI years at ages 12-18 (born 1958+); estimate (s.e.; p), *** p<0.01, ** p<0.05, * p<0.1. "
          "**Descriptive.**", ""]
    one = r.drop_duplicates("pid")
    md += [f"Sons {len(one):,} (White {int((one.race == 'White').sum()):,}, Black {int((one.race == 'Black').sum()):,}); "
           f"son-years {len(r):,}; states {one['fips17'].nunique()}. UI (max WBA / AWW, ages 12-18): mean "
           f"{np.average(one['ui'], weights=one['wt']):.3f}, s.d. {np.sqrt(np.cov(one['ui'], aweights=one['wt'])):.3f}; "
           f"within state and cohort (s.d. of the residual on state and cohort means): "
           f"{(one['ui'] - one.groupby('fips17')['ui'].transform('mean') - one.groupby('coh5')['ui'].transform('mean') + one['ui'].mean()).std():.3f}.", ""]
    # ---------------- (1) interactions
    for v in COMPS:
        r[v + "_z"] = zs(r, v)
    r["ui_z"] = zs(r, "ui")
    r["lmb_z"] = zs(r, "lmaxben")
    for u in ("ui_z", "lmb_z"):
        for v in STAB + WAGE:
            r[f"{v}_x_{u}"] = r[v + "_z"] * r[u]
    base = ["lyp"] + [v + "_z" for v in COMPS] + R75.GROUPS["structure"]
    for u, ulab in (("ui_z", "max WBA / average weekly wage"), ("lmb_z", "ln maximum total benefit")):
        inter = [f"{v}_x_{u}" for v in STAB + WAGE]
        xs = base + [u] + inter
        rows = [("lyp", "ln parental income")] + [(v + "_z", v) for v in STAB] + [(u, f"UI generosity ({ulab}, 1 s.d.)")] \
            + [(f"{v}_x_{u}", f"{v} x UI") for v in STAB] + [(f"{v}_x_{u}", f"{v} x UI (placebo)") for v in WAGE]
        md += [f"## (1) Interactions, UI = {ulab}", "",
               "Each column one regression: the son's outcome on ln parental income, all 75 components (1 s.d.), the "
               "structure flags, UI and UI x each stability and wage element; state-at-17 fixed effects, 5-year birth "
               "cohort and single-age dummies; weighted; s.e. clustered by 1968 family.", ""]
        outs = [("ln earnings", "ly"), ("employed", "emp"), ("share of years unemployed", "sb_unemp")]
        panels = (("Pooled", r), ("White", r[r.race == "White"]), ("Black", r[r.race == "Black"]),
                  ("Pooled, ages 40-55", r[r.age >= 40]), ("White, ages 40-55", r[(r.race == "White") & (r.age >= 40)]))
        md += ["| | " + " | ".join(f"({i + 1}) {h}" for i, (h, _) in enumerate(outs)) + " |", "|---" * 4 + "|"]
        for plab, d in panels:
            md.append(f"| **{plab}** | | | |")
            fits = []
            for _, y in outs:
                z = d[d[y].notna()]
                if y == "ly":
                    z = z[z["lw"].notna()]
                keep = [v for v in xs if z[v].std() > 0]
                fits.append(wreg(z, y, keep, absorb="fips17", fe=("coh5",)))
            for v, lab in rows:
                md.append(f"| {lab} | " + " | ".join(c(f[0][v]) if v in f[0] else "" for f in fits) + " |")
                for (h, y), f in zip(outs, fits):
                    if v in f[0]:
                        RES[f"inter|{u}|{plab}|{y}|{v}"] = list(f[0][v])
            md.append("| N son-years / sons / clusters | " + " | ".join(f"{f[1]:,} / {f[2]:,} / {f[3]:,}" for f in fits)
                      + " |")
        md.append("")
        print(f"(1) {u} {time.time() - t0:.0f}s", flush=True)
    # ---------------- (2) split by generosity relative to the cohort
    one = r.drop_duplicates("pid").copy()
    one["ui_rel"] = one["ui"] - one.groupby("coh5")["ui"].transform("mean")
    med = float(np.median(one["ui_rel"]))
    r = r.merge(one[["pid", "ui_rel"]], on="pid")
    r["hi"] = (r["ui_rel"] > med).astype(int)
    BT = Boot(r["fam68"].to_numpy(), r["race"].to_numpy())
    res = {}
    for h in (1, 0):
        d = r[(r["hi"] == h) & r["lw"].notna()]
        res[h] = run_spec(d, ["ly"], R75.GROUPS, BT, cells=CELLS)
    md += ["## (2) The Gelbach split in states more vs less generous than average for the son's cohort", "",
           f"Sons above / below the median of UI net of 5-year birth-cohort means (median {med:+.4f}). Ln earnings; one "
           "set of bootstrap draws shared by both halves.", "",
           "| component | half | " + " | ".join(CLAB[k] for k in CELLS) + " | share 25-55 |", "|---" * 7 + "|"]
    for gname in ["b0"] + list(R75.GROUPS) + ["b"]:
        stat = gname if gname in ("b0", "b") else f"c:{gname}"
        lab = {"b0": "IGE (b0)", "b": "rest"}.get(gname, R75.GLAB.get(gname, gname))
        ent = {}
        for h, hl in ((1, "more generous"), (0, "less generous")):
            ent[h] = [est(res[h], k, stat, 0) for k in CELLS]
            sh = est(res[h], 6, stat, 0, share=True) if gname != "b0" else None
            md.append(f"| {lab} | {hl} | " + " | ".join(cc(e) for e in ent[h]) + f" | {cc(sh)} |")
            RES[f"split|{gname}|{hl}"] = [list(e[:2]) if e else None for e in ent[h]]
            RES[f"split|{gname}|{hl}|share"] = [float(sh[0]), float(sh[1])] if sh else None
        dd = []
        for a, b in zip(ent[1], ent[0]):
            dd.append(None if a is None or b is None else (a[0] - b[0], float(np.nanstd(a[2] - b[2], ddof=1))))
        shd = None
        if gname != "b0":
            a, b = est(res[1], 6, stat, 0, share=True), est(res[0], 6, stat, 0, share=True)
            shd = (a[0] - b[0], R74.rse(a[2] - b[2]))
        md.append(f"| {lab} | **more - less** | " + " | ".join(c(e) if e else "" for e in dd) + f" | {c(shd) if shd else ''} |")
        RES[f"split|{gname}|diff"] = [list(e) if e else None for e in dd]
        RES[f"split|{gname}|diff|share"] = [float(shd[0]), float(shd[1])] if shd else None
    n1, n0 = res[1]["n"], res[0]["n"]
    md += [f"Sons / son-years / families: more generous {n1[0]:,} / {n1[1]:,} / {n1[2]:,}; less generous {n0[0]:,} / "
           f"{n0[1]:,} / {n0[2]:,}.", ""]
    (OUT / "ui_stability_channel.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "ui_stability_channel.json", "w"), indent=1, default=float)
    print(f"done {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
