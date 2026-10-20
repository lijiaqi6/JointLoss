r"""Is the delayed cost of a father's layoff general, or one era and one way of asking? (Fable round 2, Objection 1;
plan proposals/paperB_round2_plan_20261020.md, step 1)

The within-son layoff slope is -0.236** on all sons (88 / 91) but 0.040 (0.113) on the sons whose teens fall in 1976+
(99's sample). The father's job ends were recorded under different nets (19.FatherDisplacement.py): 1968-75 the
employed head (E) only if his job was < 1 year old, the unemployed head (U) undated; 1976-83 E if the present position
was < 12 months, plus the retired head (R); 1984-87 every main-job end of the year; 1988-2001 also the unemployed head's
earlier employer (U2); 2003+ a roster of up to four jobs since January 1 two years before (J1-J4).

LAYOFF SHARES (the son's window waves at 13-19 in which the father is the male head; laid off / fired = main and not
a plant closure, as in 75):
  (a) as in 75: a report of any branch with end year t or t-1 of the window wave's income year;
  (b) ONE NET IN EVERY WAVE: only reports of the interview wave itself from branches E and U (to 2001) or J1 and J2
      (2003+: the most recent job and the one before it) for a job that ended within about 12 months of the interview
      (end year >= interview year - 1, or undated where the question itself restricts to the last year, 1968-75 E / U);
      U2, R, J3, J4 dropped. In the biennial waves (1999+) the 12-month net covers half of the two years: the share is a
      rate per observed 12 months in every era. Closures likewise.
CELLS: sons born before 1963 / 1963-75 / 1976 and later (the 1963-75 cohort reaches 45-49 in 2008-25); and the regime
  of the father's window years (the majority of the son's income years at 12-18 in 1968-75 / 1976-83 / 1984+).
ESTIMATES (75's son-years, valid wage, PSID weights; 91's machinery): band coefficients of the layoff (and closure)
  share at 25-29, 40-44 and 45-49 at equal lyp and all components, the change 45-49 (or 40-44) minus 25-29, 200 common
  draws; the within-son slope (son FE, every component, lyp, structure and 5-year cohort x (age-40)/10, clustered by
  1968 family); treated counts; and the pooled within-son model with layoff x age x cohort to test equality across
  cohorts. DESCRIPTIVE.
Writes output/layoff_cohort_regime.md / .json (aggregates only).
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
R75, R24 = R91.R75, R91.R24
c, Boot, fmt, sd = R91.c, R91.Boot, R91.fmt, R91.sd
COMPS, STRUCT = R91.COMPS, R91.STRUCT
RES = {}


def shares_b(r):
    """layoff and closure shares under definition (b), one net in every wave."""
    a = pd.read_pickle(R24.CACHE)
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    dp = pd.read_pickle(DATA / "psid_displacement.pkl")
    dp = dp[dp["branch"].isin(["E", "U", "J1", "J2"]) & dp["wave"].notna()].copy()
    dp["wave"] = dp["wave"].astype(int)
    dated = dp["dated"].astype(str) == "True"
    recent = ~dated | (dp["year"] >= dp["wave"] - 1)
    dp = dp[recent]
    lay = set(zip(dp.loc[(dp["main"] == 1) & (dp["strict"] != 1), "pid"], dp.loc[(dp["main"] == 1) & (dp["strict"] != 1), "wave"]))
    clo = set(zip(dp.loc[dp["strict"] == 1, "pid"], dp.loc[dp["strict"] == 1, "wave"]))
    sons = r.drop_duplicates("pid")[["pid", "fpid"]].dropna()
    k = py[py["child"] & py["age"].between(13, 19) & py["faminc"].between(R24.LO, R24.HI) & py["pid"].isin(sons["pid"])][
        ["pid", "wave"]]
    fa = a[a["head"] & (a["female"] == 0)][["pid", "wave"]].rename(columns={"pid": "fpid"}).drop_duplicates()
    fw = k.merge(sons, on="pid").merge(fa, on=["fpid", "wave"])
    fw["lb"] = [float((p, w) in lay) for p, w in zip(fw["fpid"], fw["wave"])]
    fw["cb"] = [float((p, w) in clo) for p, w in zip(fw["fpid"], fw["wave"])]
    fw["yr"] = fw["wave"] - 1
    g = fw.groupby("pid")
    out = pd.DataFrame({"f_sh_layoff_b": g["lb"].mean(), "f_sh_close_b": g["cb"].mean(),
                        "yr_med": g["yr"].median()}).reset_index()
    return out


def cell_estimates(d, BT, comps, lay, clo, md, lab):
    focus = [lay, clo]
    g = {k: R91.band_fit(d, "ly", k, BT, comps, focus) for k in (0, 3, 4)}
    n_tr = {k: int(d[(d["band"] == k) & (d[lay] > 0) & (d["nofa"] == 0)]["pid"].nunique()) for k in (0, 3, 4)}
    hi = 4 if n_tr[4] >= 30 and lay in g[4] else 3
    a, b = g[0].get(lay), g[hi].get(lay)
    ch = (b[0] - a[0], b[1] - a[1]) if a and b else None
    ac, bc = g[0].get(clo), g[hi].get(clo)
    chc = (bc[0] - ac[0], bc[1] - ac[1]) if ac and bc else None
    XB = [f"{v}_xa" for v in ["lyp"] + comps + STRUCT + COH]
    f = R91.fe_fit(d, "ly", [x for x in XB if x in d])
    fe = (f["b"].get(f"{lay}_xa", np.nan), float(np.sqrt(f["V"].loc[f"{lay}_xa", f"{lay}_xa"])) if f"{lay}_xa" in f["V"] else np.nan)
    fec = (f["b"].get(f"{clo}_xa", np.nan), float(np.sqrt(f["V"].loc[f"{clo}_xa", f"{clo}_xa"])) if f"{clo}_xa" in f["V"] else np.nan)
    hl = "45-49" if hi == 4 else "40-44"
    md.append(f"| {lab} | {d['pid'].nunique():,} | {n_tr[0]} / {n_tr[3]} / {n_tr[4]} | {fmt(a)} | {fmt(b)} ({hl}) | "
              f"{fmt(ch)} | {c(fe)} | {fmt(chc)} | {c(fec)} |")
    RES[lab] = {"sons": int(d["pid"].nunique()), "treated_25_40_45": [n_tr[0], n_tr[3], n_tr[4]], "high_band": hl,
                "g0": [float(a[0]), sd(a[1])] if a else None, "g_hi": [float(b[0]), sd(b[1])] if b else None,
                "change": [float(ch[0]), sd(ch[1])] if ch else None, "fe": list(map(float, fe)),
                "closure_change": [float(chc[0]), sd(chc[1])] if chc else None, "closure_fe": list(map(float, fec))}


COH = []


def main():
    global COH
    r = R75.build()
    r = r.merge(shares_b(r), on="pid", how="left")
    pres = r["nofa"] == 0
    for v in ("f_sh_layoff_b", "f_sh_close_b"):
        r[v] = r[v].where(pres, 0.0).fillna(0.0)
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    cohd = pd.get_dummies(r["coh5"], prefix="coh", drop_first=True).astype(float)
    r = pd.concat([r, cohd], axis=1)
    COH = list(cohd.columns)
    r["agec"] = (r["age"] - 40) / 10
    COMPS_B = [("f_sh_layoff_b" if v == "f_sh_layoff" else "f_sh_close_b" if v == "f_sh_close" else v) for v in COMPS]
    for v in set(["lyp"] + COMPS + COMPS_B + STRUCT + COH):
        r[f"{v}_xa"] = r[v] * r["agec"]
    r["cohort"] = np.select([r["birth_year"] < 1963, r["birth_year"] <= 1975], ["born < 1963", "born 1963-75"],
                            "born 1976+")
    yr = r["birth_year"] + 15
    r["regime"] = np.select([yr <= 1975, yr <= 1983], ["teens 1968-75", "teens 1976-83"], "teens 1984+")
    v = r[r["lw"].notna()].copy()
    BT = Boot(v["fam68"].to_numpy(), v["race"].to_numpy())
    one = v[v["nofa"] == 0].drop_duplicates("pid")
    md = ["# Is the delayed layoff cost general, or one era and one way of asking? (Fable round 2, Objection 1)", "",
          "Built by `103.LayoffCohortRegime.py` (2026-10-20); design in its docstring. PSID sons 25-55, valid wage, PSID "
          "weights. Band coefficients at equal ln parental income and all of 75's components (single-age dummies; 200 "
          "common bootstrap draws); within son: son FE, every component, lyp, structure and cohort x (age-40)/10, "
          "clustered by 1968 family; per unit share (one layoff year = 1/7 in annual waves). *** p<0.01, ** p<0.05, * p<0.1.",
          "", "## 0. The two layoff shares", "",
          "| sample | sons | mean share (a) | any layoff (a) | mean share (b) | any layoff (b) | corr (a, b) |",
          "|---" * 7 + "|"]
    for lab, q in [("all", one)] + [(k, one[one["cohort"] == k]) for k in ("born < 1963", "born 1963-75", "born 1976+")]:
        w = q["wt"]
        md.append(f"| {lab} | {len(q):,} | {np.average(q['f_sh_layoff'], weights=w):.4f} | "
                  f"{np.average(q['f_sh_layoff'] > 0, weights=w):.3f} | {np.average(q['f_sh_layoff_b'], weights=w):.4f} | "
                  f"{np.average(q['f_sh_layoff_b'] > 0, weights=w):.3f} | {np.corrcoef(q['f_sh_layoff'], q['f_sh_layoff_b'])[0, 1]:.3f} |")
    md.append("")
    head = ("| cell | sons | treated at 25-29 / 40-44 / 45-49 | layoff 25-29 | layoff, oldest band | change | within son "
            "x age | closure change | closure within son x age |")
    for defn, comps, lay, clo in (("(a) as in 75", COMPS, "f_sh_layoff", "f_sh_close"),
                                  ("(b) one net in every wave", COMPS_B, "f_sh_layoff_b", "f_sh_close_b")):
        md += [f"## Layoff share {defn}", "", head, "|---" * 9 + "|"]
        cell_estimates(v, BT, comps, lay, clo, md, f"{defn} | all sons")
        for col, cells in (("cohort", ("born < 1963", "born 1963-75", "born 1976+")),
                           ("regime", ("teens 1968-75", "teens 1976-83", "teens 1984+"))):
            for k in cells:
                cell_estimates(v[v[col] == k], BT, comps, lay, clo, md, f"{defn} | {k}")
        # equality of the within-son slope across birth cohorts (pooled model, layoff x age x cohort)
        for k in ("born 1963-75", "born 1976+"):
            v[f"L_{k}"] = v[lay] * v["agec"] * (v["cohort"] == k)
        XB = [f"{x}_xa" for x in ["lyp"] + comps + STRUCT + COH]
        f = R91.fe_fit(v, "ly", XB + [f"L_{k}" for k in ("born 1963-75", "born 1976+")])
        names = [f"L_{k}" for k in ("born 1963-75", "born 1976+")]
        W = R91.wald(f, np.eye(2), names)
        dif = {k: (f["b"][f"L_{k}"], float(np.sqrt(f["V"].loc[f"L_{k}", f"L_{k}"]))) for k in ("born 1963-75", "born 1976+")}
        md += ["", f"Within-son slope relative to sons born before 1963: born 1963-75 {c(dif['born 1963-75'])}; born "
               f"1976+ {c(dif['born 1976+'])}; all equal chi2(2) = {W[0]:.2f}, p = {W[2]:.3f}.", ""]
        RES[f"{defn}|cohort_diff"] = {k: list(map(float, x)) for k, x in dif.items()}
        RES[f"{defn}|cohort_wald"] = list(W)
        print(defn, "done", flush=True)
    (OUT / "layoff_cohort_regime.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "layoff_cohort_regime.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
