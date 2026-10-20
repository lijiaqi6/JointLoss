r"""The cost of a father's childhood layoff by the son's age: robustness of Paper B's headline (PI, 2026-10-20).

HEADLINE (81.StabilityOpeningByRace.py, EVIDENCE 11.30): among White sons, the partial relation g of the father's layoff
share at the son's ages 13-19 to the son's ln earnings - at equal ln parental income and all of 75's components - goes
from 0.158 (25-29) to -0.818*** (45-49). This script asks whether that statement survives:
  (1) every band (25-29 ... 50-55), not two; per layoff year (the share is over 7 window years: g / 7 = one layoff year)
      and per s.d. of the share; layoffs vs closures vs the father's unemployment share vs the mother's;
  (2) 5-year birth-cohort dummies in every band (are older ages = older cohorts with costlier layoffs?);
  (3) which outcome carries it at 45-49: ln hourly wage, ln annual hours, employment, the son's own share of years
      unemployed (the human-capital reading needs the wage);
  (4) WITHIN THE SAME SON: son-years 25-55 with son fixed effects, ln earnings on single-age dummies and every parental
      component x (age - 40)/10 (lyp x age too; 5-year cohort x age), so the coefficient on layoff x age is the growth of
      the same son's earnings with age that goes with his father's childhood layoffs (a son observed at 30 and at 50
      identifies it; no balanced panel imposed);
  (5) TIMING: the father's layoff share at the son's ages 6-12 and 20-26 next to 13-19 (his own head-years in the
      PSID, any family unit), in (4) and in the band regressions: is it childhood (the teens) or the father's layoff
      propensity at any time?
DEFINITIONS: 75's son-years and components (R75.build()); layoff = psid_displacement 'layoff' (main and not a closure:
  PSID codes 'laid off / fired'), closure = 'strict' (plant closed / moved), in year t or t-1 of the window wave.
  Weighted (PSID weights); s.e. clustered by 1968 family; (1)-(3) also with 200 cluster-bootstrap draws for the change
  45-49 minus 25-29 (81's draws). Descriptive: a layoff is not randomly assigned; closures are the exogenous contrast.
Writes output/layoff_cost_by_age.md / .json (aggregates only).
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
R74, R24 = R75.R74, R75.R24
c, wreg, wls, dummies, Boot = R74.c, R74.wreg, R74.wls, R74.dummies, R74.Boot
BLAB = ["25-29", "30-34", "35-39", "40-44", "45-49", "50-55"]
COMPS = [v for g in ("wage", "hours", "stability", "group") for v in R75.GROUPS[g]]
STRUCT = R75.GROUPS["structure"]
FOCUS = ["f_sh_layoff", "f_sh_close", "f_sh_unemp", "m_sh_unemp"]
RES = {}


def layoff_windows(r):
    """father's layoff / closure shares over the son's ages 6-12 and 20-26 (fpid's male-head years, any unit)."""
    a = pd.read_pickle(R24.CACHE)
    fa = a[a["head"] & (a["female"] == 0)][["pid", "wave"]].drop_duplicates().rename(columns={"pid": "fpid"})
    dp = pd.read_pickle(DATA / "psid_displacement.pkl")
    lay = set(zip(dp.loc[dp["layoff"] == 1, "pid"], dp.loc[dp["layoff"] == 1, "year"]))
    clo = set(zip(dp.loc[dp["strict"] == 1, "pid"], dp.loc[dp["strict"] == 1, "year"]))
    sons = r.drop_duplicates("pid")[["pid", "fpid", "birth_year"]].dropna()
    out = sons[["pid"]].copy()
    for lo, hi, tag in ((6, 12, "a6"), (20, 26, "a20")):
        rows = sons.assign(key=1).merge(pd.DataFrame({"off": range(lo, hi + 1), "key": 1}), on="key")
        rows["wave"] = (rows["birth_year"] + rows["off"] + 1).astype(int)       # income year = son's age year
        rows = rows.merge(fa, on=["fpid", "wave"])
        y = rows["wave"] - 1
        rows["lay"] = [float((p, t) in lay or (p, t - 1) in lay) for p, t in zip(rows["fpid"], y)]
        rows["clo"] = [float((p, t) in clo or (p, t - 1) in clo) for p, t in zip(rows["fpid"], y)]
        g = rows.groupby("pid")
        ok = g.size() >= 3
        W = pd.DataFrame({f"lay_{tag}": g["lay"].mean().where(ok), f"clo_{tag}": g["clo"].mean().where(ok)})
        out = out.merge(W.reset_index(), on="pid", how="left")
    return out


def band_g(d, y, k, BT, extra=(), ctrl=()):
    """g of the FOCUS elements (+ extra) in band k: y on lyp, all components, structure, extra; age dummies (+ ctrl);
    weighted; point + bootstrap draws."""
    z = d[d["band"] == k].dropna(subset=[y, "lyp"] + COMPS + list(extra))
    cols = COMPS + STRUCT + list(extra)
    cols = [v for v in cols if z[v].std() > 0]
    parts = [dummies(z["age"])] + ([z[list(ctrl)].to_numpy(float)] if ctrl else []) + [np.ones((len(z), 1))]
    A = np.column_stack(parts)
    X = np.column_stack([z["lyp"].to_numpy(float), z[cols].to_numpy(float), A])
    Y = z[[y]].to_numpy(float)
    w0 = z["wt"].to_numpy(float)
    ii = [1 + cols.index(v) for v in FOCUS + list(extra) if v in cols]
    names = [v for v in FOCUS + list(extra) if v in cols]
    pt = wls(X, Y, np.sqrt(w0))[ii, 0]
    ri = BT.rows(z["fam68"].to_numpy())
    D = np.zeros((BT.cnt.shape[0], len(ii)))
    for b in range(BT.cnt.shape[0]):
        w = w0 * BT.cnt[b, ri]
        keep = w > 0
        D[b] = wls(X[keep], Y[keep], np.sqrt(w[keep]))[ii, 0]
    return {n: (pt[j], D[:, j]) for j, n in enumerate(names)}, z["pid"].nunique()


def fmt(t, scale=1.0, dec=3):
    return "" if t is None else c((t[0] * scale, float(np.nanstd(t[1] * scale, ddof=1))), dec)


def main():
    t0 = time.time()
    r = R75.build()
    r = r.merge(layoff_windows(r), on="pid", how="left")
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    cohd = pd.get_dummies(r["coh5"], prefix="coh", drop_first=True).astype(float)
    r = pd.concat([r, cohd], axis=1)
    BT = Boot(r["fam68"].to_numpy(), r["race"].to_numpy())
    one = r.drop_duplicates("pid")
    md = ["# The cost of a father's childhood layoff by the son's age (robustness of the headline)", "",
          "Built by `88.LayoffCostByAge.py` (2026-10-20); design in its docstring. PSID sons 25-55; g = coefficient of "
          "the element on the son's outcome at equal ln parental income and all of 75's components (weighted, single-age "
          "dummies); estimate (s.e.; p), *** p<0.01, ** p<0.05, * p<0.1; s.e. from 200 cluster-bootstrap draws of 1968 "
          "families (common to all rows). **Descriptive.**", ""]
    md += ["## 0. The layoff share", "", "| sample | sons | mean layoff share 13-19 | share with any layoff year | "
           "s.d. | mean closure share |", "|---" * 6 + "|"]
    sds = {}
    for lab, q in (("pooled", one), ("White", one[one.race == "White"]), ("Black", one[one.race == "Black"])):
        f = q[(q.nofa == 0)]
        sd = float(np.sqrt(np.cov(f["f_sh_layoff"], aweights=f["wt"])))
        sds[lab] = sd
        md.append(f"| {lab} | {len(f):,} | {np.average(f['f_sh_layoff'], weights=f['wt']):.4f} | "
                  f"{np.average((f['f_sh_layoff'] > 0).astype(float), weights=f['wt']):.3f} | {sd:.4f} | "
                  f"{np.average(f['f_sh_close'], weights=f['wt']):.4f} |")
    md += ["", "Father present; the share is over the son's wave-ages 13-19 (7 waves), so one layoff year = 1/7 = 0.143 "
           "and g / 7 is the cost of one layoff year.", ""]
    # (1)-(2) every band, layoff vs others, main and with cohort dummies
    for spec, ctrl in (("single-age dummies", ()), ("+ 5-year birth-cohort dummies", tuple(cohd.columns))):
        md += [f"## 1. g on ln earnings by band, {spec}", "",
               "| element | race | " + " | ".join(BLAB) + " | change 45-49 - 25-29 | per layoff year at 45-49 (g/7) |",
               "|---" * 10 + "|"]
        for race in ("White", "Black", "pooled"):
            d = r[r["lw"].notna()] if race == "pooled" else r[(r.race == race) & r["lw"].notna()]
            ct = tuple(v for v in ctrl if d[v].std() > 0)
            G = [band_g(d, "ly", k, BT, ctrl=ct)[0] for k in range(6)]
            for v in FOCUS:
                ent = [g.get(v) for g in G]
                ch = (ent[4][0] - ent[0][0], ent[4][1] - ent[0][1]) if ent[4] and ent[0] else None
                md.append(f"| {v} | {race} | " + " | ".join(fmt(e) for e in ent) + f" | {fmt(ch)} | "
                          + (fmt(ent[4], 1 / 7) if v == "f_sh_layoff" else "") + " |")
                RES[f"bands|{spec}|{race}|{v}"] = {"g": [[float(e[0]), float(np.nanstd(e[1], ddof=1))] for e in ent],
                                                  "change": [float(ch[0]), float(np.nanstd(ch[1], ddof=1))]}
        md.append("")
        print(f"(1) {spec} {time.time() - t0:.0f}s", flush=True)
    # (3) outcomes at 25-29 and 45-49
    md += ["## 2. Which outcome carries it (g of the layoff share), White and pooled", "",
           "| outcome | race | 25-29 | 45-49 | change |", "|---" * 5 + "|"]
    for race in ("White", "pooled"):
        d0 = r if race == "pooled" else r[r.race == race]
        for y, sub in (("ly", d0["lw"].notna()), ("lw", d0["lw"].notna()), ("lh", d0["lw"].notna()),
                       ("emp", d0["emp"].notna()), ("sb_unemp", d0["sb_unemp"].notna())):
            d = d0[sub]
            a = band_g(d, y, 0, BT)[0]["f_sh_layoff"]
            b = band_g(d, y, 4, BT)[0]["f_sh_layoff"]
            md.append(f"| {R75.OL[y]} | {race} | {fmt(a)} | {fmt(b)} | {fmt((b[0] - a[0], b[1] - a[1]))} |")
            sd = lambda t: float(np.nanstd(t, ddof=1))  # noqa: E731
            RES[f"outcome|{race}|{y}"] = {"a": [float(a[0]), sd(a[1])], "b": [float(b[0]), sd(b[1])],
                                         "ch": [float(b[0] - a[0]), sd(b[1] - a[1])]}
    md.append("")
    print(f"(3) {time.time() - t0:.0f}s", flush=True)
    # (4)-(5) within son: son FE, components x age
    md += ["## 3. Within the same son: son fixed effects, every parental component x (age - 40)/10", "",
           "Son-years 25-55, ln earnings (valid years); son fixed effects absorbed; single-age dummies; lyp x age, every "
           "75 component and structure flag x age, 5-year cohort x age; weighted; s.e. clustered by 1968 family. The "
           "coefficient = change per 10 years of age in the same son's ln earnings per unit layoff share (one layoff "
           "year = 1/7).", "",
           "| | (1) White | (2) White + timing | (3) Black | (4) Black + timing | (5) pooled | (6) pooled + timing |",
           "|---" * 7 + "|"]
    r["agec"] = (r["age"] - 40) / 10
    base = ["lyp"] + COMPS + STRUCT
    for v in base + ["lay_a6", "lay_a20", "clo_a6", "clo_a20"] + list(cohd.columns):
        r[f"{v}_xa"] = r[v] * r["agec"] if v in r else np.nan
    fits = []
    for race in ("White", "Black", "pooled"):
        for timing in (False, True):
            d = r[r["lw"].notna()] if race == "pooled" else r[(r.race == race) & r["lw"].notna()]
            xs = [f"{v}_xa" for v in base + list(cohd.columns)]
            if timing:
                d = d.dropna(subset=["lay_a6", "lay_a20"])
                xs += ["lay_a6_xa", "lay_a20_xa", "clo_a6_xa", "clo_a20_xa"]
            xs = [x for x in xs if d[x].std() > 0]
            fits.append(wreg(d, "ly", xs, absorb="pid"))
    rows = [("f_sh_layoff_xa", "layoff share 13-19 x age"), ("f_sh_close_xa", "closure share 13-19 x age"),
            ("f_sh_unemp_xa", "father's unemployment share 13-19 x age"), ("m_sh_unemp_xa", "mother's unemployment x age"),
            ("lay_a6_xa", "layoff share 6-12 x age"), ("lay_a20_xa", "layoff share 20-26 x age"),
            ("clo_a6_xa", "closure share 6-12 x age"), ("clo_a20_xa", "closure share 20-26 x age"),
            ("lyp_xa", "ln parental income x age"), ("f_lw_xa", "father's ln wage x age")]
    for v, lab in rows:
        md.append(f"| {lab} | " + " | ".join(c(f[0][v]) if v in f[0] else "" for f in fits) + " |")
        RES[f"fe|{v}"] = [list(f[0][v]) if v in f[0] else None for f in fits]
    md.append("| N son-years / sons / clusters | " + " | ".join(f"{f[1]:,} / {f[2]:,} / {f[3]:,}" for f in fits) + " |")
    md.append("")
    (OUT / "layoff_cost_by_age.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "layoff_cost_by_age.json", "w"), indent=1, default=float)
    print(f"done {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
