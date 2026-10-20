r"""Referee 2 (and 1) checks on the father's childhood layoff (simulated JPE round, proposals/jpe_simulated_review_20261020.md)

  R2.1 PRE-TRENDS. Father-year event study around the father's first layoff in any of his son's teen windows (75's
       layoff definition: main and not a closure, by end year): his ln earnings (valid years) and employment (hours > 0)
       on event-time dummies -6 ... +6 (ends binned), father FE, calendar-year FE and single-age dummies; reference
       event time -1; control fathers = fathers of 75's sons with no layoff in any son's teen window. Joint test of the
       pre-event coefficients (-6 ... -2). PSID weights of the father-year; clustered by 1968 family.
  R2.2 PLACEBO WITH LATER LAYOFFS. The father's layoff share at the son's ages 27-35 (his head-years, any unit), added
       to the within-son model of 91 (son FE, every component, lyp, structure and cohort x (age-40)/10): if the cost
       works through childhood exposure, layoffs after the son is 26 carry nothing; if the layoff marks a trait of the
       father, they carry it too.
  R2.3 / R2.6 THE CLOSURE BOUND AND POWER. From 91's common-draw estimates: the 95% interval of the closure change and the
       largest closure cost it allows as a share of the layoff cost; minimum detectable effects (80% power, 5% two-sided:
       2.8 s.e.) for the layoff change and the within-son slope; treated counts by band (91).
  R1   RANK PROFILE. The son's earnings rank (weighted percentile within single year of age x calendar year, among 75's
       son-years) on the layoff share at 25-29 and 45-49 at equal lyp and all components (91's band_fit, 200 draws).
Writes output/layoff_referee_checks.md / .json (aggregates only). DESCRIPTIVE.
"""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import DATA, OUT  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R91 = _load("s91", "91.LayoffSelection.py")
R93 = _load("s93", "93.LayoffIndustryShocks.py")
R75, R24, R73 = R91.R75, R91.R24, R91.R73
c, Boot, fmt, sd, dummies = R91.c, R91.Boot, R91.fmt, R91.sd, R91.dummies
COMPS, STRUCT = R91.COMPS, R91.STRUCT
RES = {}


def wpct(x, w):
    o = np.argsort(x)
    cw = np.cumsum(w[o])
    p = np.empty(len(x))
    p[o] = (cw - 0.5 * w[o]) / cw[-1] * 100
    return p


def event_study(r):
    a = pd.read_pickle(R24.CACHE)
    dp = pd.read_pickle(DATA / "psid_displacement.pkl")
    m = (dp["main"] == 1) & (dp["strict"] != 1)
    lay = dp.loc[m, ["pid", "year"]].rename(columns={"pid": "fpid"})
    sons = r[r["nofa"] == 0].drop_duplicates("pid")[["pid", "fpid", "birth_year"]].dropna()
    win = sons.assign(lo=sons["birth_year"] + 12, hi=sons["birth_year"] + 18)
    L = lay.merge(win[["fpid", "lo", "hi"]], on="fpid")
    L = L[(L["year"] >= L["lo"]) & (L["year"] <= L["hi"])]
    first = L.groupby("fpid")["year"].min().rename("ev")
    fathers = sons["fpid"].unique()
    fa = a[a["head"] & (a["female"] == 0) & a["pid"].isin(fathers)][["pid", "fam68", "year", "age", "valid", "ly", "hours", "wt"]]
    fa = fa.rename(columns={"pid": "fpid"}).merge(first, on="fpid", how="left")
    fa = fa[fa["age"].between(25, 64) & (fa["wt"] > 0)].copy()
    fa["emp"] = (fa["hours"] > 0).astype(float).where(fa["hours"].notna())
    fa["et"] = (fa["year"] - fa["ev"]).clip(-6, 6)
    ets = [k for k in range(-6, 7) if k != -1]
    for k in ets:
        fa[f"e{k}"] = ((fa["et"] == k) & fa["ev"].notna()).astype(float)
    out = {}
    for y in ("ly", "emp"):
        d = fa.dropna(subset=[y]) if y == "emp" else fa[fa["valid"] == True].dropna(subset=["ly"])  # noqa: E712
        X = np.column_stack([d[[f"e{k}" for k in ets]].to_numpy(float), dummies(d["year"]), dummies(d["age"])])
        b, V, _ = R93.ols(X, d[y].to_numpy(float), d["wt"].to_numpy(float), d["fam68"].to_numpy(),
                          absorb=d["fpid"].to_numpy())
        k = len(ets)
        bb, VV = b[:k], V[:k, :k]
        pre = [ets.index(j) for j in range(-6, -1)]
        q = bb[pre]
        W = float(q @ np.linalg.pinv(VV[np.ix_(pre, pre)]) @ q)
        out[y] = {"coef": {str(j): [float(bb[i]), float(np.sqrt(VV[i, i]))] for i, j in enumerate(ets)},
                  "pre_wald": [W, len(pre), float(stats.chi2.sf(W, len(pre)))],
                  "n_treated": int(d.loc[d["ev"].notna(), "fpid"].nunique()), "n_fathers": int(d["fpid"].nunique())}
    return out


def later_layoffs(r):
    a = pd.read_pickle(R24.CACHE)
    dp = pd.read_pickle(DATA / "psid_displacement.pkl")
    m = (dp["main"] == 1) & (dp["strict"] != 1)
    lay = set(zip(dp.loc[m, "pid"], dp.loc[m, "year"]))
    fa = a[a["head"] & (a["female"] == 0)][["pid", "wave"]].rename(columns={"pid": "fpid"}).drop_duplicates()
    sons = r.drop_duplicates("pid")[["pid", "fpid", "birth_year"]].dropna()
    rows = sons.assign(key=1).merge(pd.DataFrame({"off": range(27, 36), "key": 1}), on="key")
    rows["wave"] = (rows["birth_year"] + rows["off"] + 1).astype(int)
    rows = rows.merge(fa, on=["fpid", "wave"])
    y = rows["wave"] - 1
    rows["lay"] = [float((p, t) in lay or (p, t - 1) in lay) for p, t in zip(rows["fpid"], y)]
    g = rows.groupby("pid")
    return pd.DataFrame({"lay_a27": g["lay"].mean().where(g.size() >= 3)}).reset_index()


def main():
    r = R75.build()
    md = ["# Referee checks on the father's childhood layoff (simulated JPE round)", "",
          "Built by `108.LayoffRefereeChecks.py` (2026-10-20); design in its docstring. *** p<0.01, ** p<0.05, * p<0.1.", ""]
    # R2.1 event study
    E = event_study(r)
    RES["event"] = E
    md += ["## R2.1 The father before and after his first layoff in a son's teens (event study, father FE)", "",
           "| event time (years) | " + " | ".join(["-6", "-5", "-4", "-3", "-2", "0", "+1", "+2", "+3", "+4", "+5", "+6"]) + " |",
           "|---" * 13 + "|"]
    for y, lab in (("ly", "father's ln earnings"), ("emp", "father employed")):
        cells = [c(tuple(E[y]["coef"][str(k)])) for k in (-6, -5, -4, -3, -2, 0, 1, 2, 3, 4, 5, 6)]
        md.append(f"| {lab} | " + " | ".join(cells) + " |")
    for y, lab in (("ly", "ln earnings"), ("emp", "employed")):
        W = E[y]["pre_wald"]
        md.append(f"\nPre-event coefficients (-6 ... -2) jointly zero, {lab}: chi2({W[1]}) = {W[0]:.2f}, p = {W[2]:.3f}; "
                  f"treated fathers {E[y]['n_treated']:,} of {E[y]['n_fathers']:,}.")
    md.append("")
    print("event study done", flush=True)
    # R2.2 placebo with later layoffs
    r = r.merge(later_layoffs(r), on="pid", how="left")
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    cohd = pd.get_dummies(r["coh5"], prefix="coh", drop_first=True).astype(float)
    r = pd.concat([r, cohd], axis=1)
    r["agec"] = (r["age"] - 40) / 10
    XB = R91.xage(r, ["lyp"] + COMPS + STRUCT + list(cohd.columns))
    r["lay_a27_xa"] = r["lay_a27"] * r["agec"]
    v = r[r["lw"].notna()].copy()
    q = v.dropna(subset=["lay_a27"])
    f0 = R91.fe_fit(q, "ly", XB)
    f1 = R91.fe_fit(q, "ly", XB + ["lay_a27_xa"])
    g = lambda f, x: (f["b"][x], float(np.sqrt(f["V"].loc[x, x])))  # noqa: E731
    md += ["## R2.2 Placebo: the same fathers' layoffs after the son is 26 (within son, ln earnings)", "",
           f"Sons whose father is observed as a head in >= 3 waves at their 27-35: {q['pid'].nunique():,} "
           f"(father laid off then: {int((q.drop_duplicates('pid')['lay_a27'] > 0).sum()):,}).", "",
           "| spec | teen layoff share x age | layoff share at 27-35 x age |", "|---|---|---|",
           f"| teen share only | {c(g(f0, 'f_sh_layoff_xa'))} | |",
           f"| + share at 27-35 | {c(g(f1, 'f_sh_layoff_xa'))} | {c(g(f1, 'lay_a27_xa'))} |", ""]
    RES["placebo27"] = {"base": list(g(f0, "f_sh_layoff_xa")), "teen": list(g(f1, "f_sh_layoff_xa")),
                        "later": list(g(f1, "lay_a27_xa")), "sons": int(q["pid"].nunique())}
    # R2.3 / R2.6 closure bound and MDEs
    S = json.load(open(OUT / "layoff_selection.json"))
    L, C = S["A6b|pooled"]["layoff"], S["A6b|pooled"]["closure"]
    lo, hi = C[0] - 1.96 * C[1], C[0] + 1.96 * C[1]
    fe = json.load(open(OUT / "layoff_cost_by_age.json"))["fe|f_sh_layoff_xa"][4]
    md += ["## R2.3 / R2.6 The closure bound and minimum detectable effects", "",
           f"Closure change 45-49 - 25-29 {C[0]:.3f} (s.e. {C[1]:.3f}); 95% interval [{lo:.3f}, {hi:.3f}]: the largest "
           f"closure cost it allows is {-lo:.3f}, {(-lo) / (-L[0]):.0%} of the layoff change ({L[0]:.3f}).",
           f"Minimum detectable effect (80% power, 5% two-sided) for the layoff change: {2.8 * L[1]:.3f} (s.e. {L[1]:.3f}); "
           f"for the closure change: {2.8 * C[1]:.3f}; for the within-son layoff slope: {2.8 * fe[1]:.3f} (s.e. {fe[1]:.3f}).",
           ""]
    RES["closure_bound"] = {"ci": [lo, hi], "share_of_layoff": float(-lo / -L[0]), "mde_layoff": 2.8 * L[1],
                            "mde_closure": 2.8 * C[1], "mde_fe": 2.8 * fe[1]}
    # R1 rank profile
    v["rk"] = np.nan
    for (ag, yr), idx in v.groupby(["age", "year"]).groups.items():
        z = v.loc[idx]
        v.loc[idx, "rk"] = wpct(z["ly"].to_numpy(float), z["wt"].to_numpy(float))
    BT = Boot(v["fam68"].to_numpy(), v["race"].to_numpy())
    a0 = R91.band_fit(v, "rk", 0, BT, COMPS, ["f_sh_layoff", "f_sh_close"])
    a4 = R91.band_fit(v, "rk", 4, BT, COMPS, ["f_sh_layoff", "f_sh_close"])
    md += ["## R1 The layoff profile in ranks (son's earnings percentile within age x year)", "",
           "| element | 25-29 | 45-49 | change |", "|---|---|---|---|"]
    for e in ("f_sh_layoff", "f_sh_close"):
        x0, x4 = a0[e], a4[e]
        ch = (x4[0] - x0[0], x4[1] - x0[1])
        md.append(f"| {e} | {fmt(x0)} | {fmt(x4)} | {fmt(ch)} |")
        RES[f"rank|{e}"] = {"a": [float(x0[0]), sd(x0[1])], "b": [float(x4[0]), sd(x4[1])], "ch": [float(ch[0]), sd(ch[1])]}
    md.append("")
    (OUT / "layoff_referee_checks.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "layoff_referee_checks.json", "w"), indent=1, default=float)
    print("\n".join(md))


if __name__ == "__main__":
    main()
