r"""Is the delayed cost of a father's teen layoff selection? Fable's additions A2, A3, A6 (2026-10-20).

Memo: proposals/fable_top5_distance_paperB_20261020.md, Section 4 A. Headline under test (88.LayoffCostByAge.py,
EVIDENCE 11.39): at equal ln parental income and all of 75's components, the father's layoff share at the son's ages
13-19 is unrelated to the son's ln earnings at 25-29 and -0.768*** at 45-49 (pooled); within the same son -0.236** per
ten years of age.

  A6  MISSING NUMBERS AND TESTS
      (a) treated sons: father-present sons with a teen layoff year, by band (son-years with a valid wage), by race;
      (b) layoff change minus closure change (45-49 minus 25-29) on the common bootstrap draws;
      (c) equality of the three timing windows (6-12, 13-19, 20-26) in the within-son design, pairwise and jointly
          (Wald, cluster-robust covariance);
      (d) leave-one-five-year-cohort-out: the band change and the within-son slope dropping each birth cohort.
  A2  TIMING AS THE CONTROL GROUP (Hilger 2016 logic): sons whose father was laid off at SOME time in 6-12, 13-19 or
      20-26 (all three windows measured), so that every father has a layoff; groups T = a layoff at 13-19, E = at 6-12
      and not 13-19, L = only at 20-26 (reference). Within-son: ln earnings on son FE, single-age dummies,
      T x (age-40)/10, E x (age-40)/10, lyp and every component x age; and the band profile T x band (b_a). Equality of
      the T, E, L age slopes.
  A3  WHAT THE LAYOFF IS VS WHAT IT DOES: the teen layoff share split into parts that add up to it -
      (i)   income loss: layoff years with a fall in ln family income (the wave against the mean of the son's other,
            layoff-free teen waves) below vs above the median fall among layoff years (unmeasured -> its own part);
      (ii)  unemployment: layoff years with the father's hours unemployed (head, waves to 1993) above vs below 500;
      (iii) UI receipt: layoff years in which the head received unemployment compensation vs not (PSID flag);
      (iv)  repeat: sons with one teen layoff year vs two or more (Stevens 1997);
      (v)   temporary: layoff years with the head 'temporarily laid off' at that or the next interview (employment
            status, waves 1983+ only) vs not;
      and (vi) ln parental income at the son's 20-26 (the father's unit, >= 2 waves) as a control: the money after the
      teens that the 13-19 measure leaves out.
      If the cost is what the layoff does (income, turmoil), the large-loss / long-unemployment / uninsured parts carry
      it; if it marks a trait of the father, all parts carry it alike.
DATA: 75's son-years and components (R75.build()), 88's timing windows; 24's head-and-wife panel for the father's
  window years (lfam, hu, ub, est). Weighted (PSID weights); s.e. clustered by 1968 family or 200 cluster-bootstrap
  draws (74's Boot, common to all rows). DESCRIPTIVE.
Writes output/layoff_selection.md / .json (aggregates only).
"""
import importlib.util
import json
import sys
import time
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


R88 = _load("s88", "88.LayoffCostByAge.py")
R75, R74, R24, R73 = R88.R75, R88.R74, R88.R24, R88.R74.R73
c, wls, dummies, Boot = R74.c, R74.wls, R74.dummies, R74.Boot
COMPS, STRUCT = R88.COMPS, R88.STRUCT
BLAB = R88.BLAB
RES = {}


def sd(x):
    return float(np.nanstd(x, ddof=1))


def pval(b, s):
    return float(2 * stats.norm.sf(abs(b / s))) if s and s > 0 else np.nan


def fmt(t, scale=1.0):
    return "" if t is None else c((t[0] * scale, sd(t[1] * scale)))


# ================================================================ the father's teen layoff years in detail
def teen_detail(r):
    """per son: the teen layoff share split by income loss, unemployment, UI receipt, repeat and temporary layoff;
    ln parental income at 20-26; number of teen layoff years."""
    a = pd.read_pickle(R24.CACHE)
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    sons = r.drop_duplicates("pid")[["pid", "fpid", "birth_year"]]
    k = py[py["child"] & py["age"].between(13, 19) & py["faminc"].between(R24.LO, R24.HI) & py["pid"].isin(sons["pid"])][
        ["pid", "wave", "int"]]
    dp = pd.read_pickle(DATA / "psid_displacement.pkl")
    lay = set(zip(dp.loc[(dp["main"] == 1) & (dp["strict"] != 1), "pid"],
                  dp.loc[(dp["main"] == 1) & (dp["strict"] != 1), "year"]))
    fa = a[a["head"] & (a["female"] == 0)][["pid", "wave", "lfam", "hu", "ub", "est"]].rename(columns={"pid": "fpid"})
    fa = fa.drop_duplicates(["fpid", "wave"])
    fw = k.merge(sons[["pid", "fpid"]].dropna(), on="pid").merge(fa, on=["fpid", "wave"])
    yr = fw["wave"] - 1
    fw["lay"] = [float((p, y) in lay or (p, y - 1) in lay) for p, y in zip(fw["fpid"], yr)]
    # temporary layoff at this or the next interview (employment status exists from 1983)
    est = fa.set_index(["fpid", "wave"])["est"]
    nxt = fa.sort_values(["fpid", "wave"]).groupby("fpid")["est"].shift(-1)
    nxt.index = pd.MultiIndex.from_frame(fa.sort_values(["fpid", "wave"])[["fpid", "wave"]])
    fw["temp"] = [float(est.get((p, w)) == 2 or nxt.get((p, w)) == 2) if w >= 1983 else np.nan
                  for p, w in zip(fw["fpid"], fw["wave"])]
    # income loss against the son's layoff-free teen waves
    base = fw[fw["lay"] == 0].groupby("pid")["lfam"].mean().rename("lfam0")
    fw = fw.merge(base, on="pid", how="left")
    fw["drop"] = fw["lfam"] - fw["lfam0"]
    L = fw[fw["lay"] == 1]
    med_drop = float(L["drop"].median())
    n = fw.groupby("pid").size()
    out = pd.DataFrame(index=n.index)

    def share(mask):
        return (fw["lay"] * mask).groupby(fw["pid"]).sum() / n

    out["lay_loss_big"] = share((fw["drop"] < med_drop).astype(float))
    out["lay_loss_small"] = share((fw["drop"] >= med_drop).astype(float))
    out["lay_loss_na"] = share(fw["drop"].isna().astype(float))
    out["lay_hu_long"] = share((fw["hu"] >= 500).astype(float))
    out["lay_hu_short"] = share((fw["hu"] < 500).astype(float))
    out["lay_hu_na"] = share(fw["hu"].isna().astype(float))
    out["lay_ui"] = share((fw["ub"] == 1).astype(float))
    out["lay_noui"] = share((fw["ub"] == 0).astype(float))
    out["lay_ui_na"] = share(fw["ub"].isna().astype(float))
    out["lay_temp"] = share((fw["temp"] == 1).astype(float))
    out["lay_perm"] = share((fw["temp"] == 0).astype(float))
    out["lay_temp_na"] = share(fw["temp"].isna().astype(float))
    nl = fw.groupby("pid")["lay"].sum()
    out["n_lay"] = nl
    sh = fw.groupby("pid")["lay"].mean()
    out["lay_one"] = sh.where(nl == 1, 0.0)
    out["lay_multi"] = sh.where(nl >= 2, 0.0)
    # ln parental income at the son's 20-26 (the father's unit)
    rows = sons.dropna().assign(key=1).merge(pd.DataFrame({"off": range(20, 27), "key": 1}), on="key")
    rows["wave"] = (rows["birth_year"] + rows["off"] + 1).astype(int)
    rows = rows.merge(fa[["fpid", "wave", "lfam"]], on=["fpid", "wave"])
    g = rows.groupby("pid")["lfam"]
    out["lyp20"] = g.mean().where(g.count() >= 2)
    out.index.name = "pid"
    info = {"median_drop_layoff_years": med_drop, "layoff_years": int(len(L)),
            "share_layoff_years_hu_measured": float(L["hu"].notna().mean()),
            "share_layoff_years_ub_measured": float(L["ub"].notna().mean()),
            "share_layoff_years_ui": float((L["ub"] == 1).sum() / L["ub"].notna().sum()),
            "share_layoff_years_temp_measured": float(L["temp"].notna().mean())}
    return out.reset_index(), info


# ================================================================ regressions
def band_fit(d, y, k, BT, comps, focus, ctrl=()):
    """band k: y on lyp, comps, structure (+ ctrl); single-age dummies; weighted; point + bootstrap draws for focus."""
    z = d[d["band"] == k].dropna(subset=[y, "lyp"] + comps + list(ctrl))
    cols = [v for v in comps + STRUCT + list(ctrl) if z[v].std() > 0]
    X = np.column_stack([z["lyp"].to_numpy(float), z[cols].to_numpy(float), dummies(z["age"]), np.ones((len(z), 1))])
    Y = z[[y]].to_numpy(float)
    w0 = z["wt"].to_numpy(float)
    names = [v for v in focus if v in cols]
    ii = [1 + cols.index(v) for v in names]
    pt = wls(X, Y, np.sqrt(w0))[ii, 0]
    ri = BT.rows(z["fam68"].to_numpy())
    D = np.zeros((BT.cnt.shape[0], len(ii)))
    for b in range(BT.cnt.shape[0]):
        w = w0 * BT.cnt[b, ri]
        keep = w > 0
        D[b] = wls(X[keep], Y[keep], np.sqrt(w[keep]))[ii, 0]
    return {n: (pt[j], D[:, j]) for j, n in enumerate(names)}


def fe_fit(d, y, xs):
    """son FE (weighted within), single-age dummies; cluster-robust (1968 family) covariance for xs."""
    z = d.dropna(subset=[y] + xs + ["fam68", "wt", "pid"])
    xs = [x for x in xs if z[x].std() > 0]
    X = np.column_stack([z[xs].to_numpy(float), dummies(z["age"])])
    yv = z[y].to_numpy(float)
    ww = z["wt"].to_numpy(float)
    M = R73.demean(np.column_stack([yv, X]), z["pid"].to_numpy(), ww)
    yv, X = M[:, 0], M[:, 1:]
    keep = np.abs(X).sum(axis=0) > 1e-9
    keep[:len(xs)] = True
    X = X[:, keep]
    Xw = X * ww[:, None]
    XtXi = np.linalg.pinv(X.T @ Xw)
    b = XtXi @ Xw.T @ yv
    u = yv - X @ b
    S = pd.DataFrame(Xw * u[:, None]).groupby(z["fam68"].to_numpy()).sum().to_numpy()
    G, (n, kk) = S.shape[0], X.shape
    V = XtXi @ (S.T @ S) @ XtXi * G / (G - 1) * (n - 1) / (n - kk)
    k = len(xs)
    return {"b": dict(zip(xs, b[:k])), "V": pd.DataFrame(V[:k, :k], index=xs, columns=xs), "n": len(z),
            "sons": int(z["pid"].nunique()), "cl": int(z["fam68"].nunique()), "G": G}


def wald(f, R, names):
    """H0: R b = 0 for the rows of R over names; returns chi2, df, p."""
    b = np.array([f["b"][v] for v in names])
    V = f["V"].loc[names, names].to_numpy()
    R = np.atleast_2d(R)
    q = R @ b
    W = float(q @ np.linalg.pinv(R @ V @ R.T) @ q)
    return W, R.shape[0], float(stats.chi2.sf(W, R.shape[0]))


def lincom(f, wts):
    names = list(wts)
    a = np.array([wts[v] for v in names])
    b = np.array([f["b"][v] for v in names])
    V = f["V"].loc[names, names].to_numpy()
    return float(a @ b), float(np.sqrt(a @ V @ a))


def xage(r, cols):
    for v in cols:
        r[f"{v}_xa"] = r[v] * r["agec"]
    return [f"{v}_xa" for v in cols]


def main():
    t0 = time.time()
    r = R75.build()
    r = r.merge(R88.layoff_windows(r), on="pid", how="left")
    det, info = teen_detail(r)
    r = r.merge(det, on="pid", how="left")
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    cohd = pd.get_dummies(r["coh5"], prefix="coh", drop_first=True).astype(float)
    r = pd.concat([r, cohd], axis=1)
    COH = list(cohd.columns)
    r["agec"] = (r["age"] - 40) / 10
    pres = r["nofa"] == 0
    split_cols = [v for v in det.columns if v.startswith("lay_")]
    for v in split_cols:
        r[v] = r[v].where(pres, 0.0).fillna(0.0)
    r["n_lay"] = r["n_lay"].where(pres)
    r["lyp20_na"] = r["lyp20"].isna().astype(float)
    r["lyp20"] = r["lyp20"].fillna(np.average(r["lyp20"].dropna(), weights=r.loc[r["lyp20"].notna(), "wt"]))
    v = r[r["lw"].notna()].copy()
    BT = Boot(v["fam68"].to_numpy(), v["race"].to_numpy())
    RES["info"] = info
    md = ["# Is the delayed cost of a father's teen layoff selection? (Fable A2, A3, A6)", "",
          "Built by `91.LayoffSelection.py` (2026-10-20); design in its docstring. PSID sons 25-55, son-years with a "
          "valid wage; estimate (s.e.; p), *** p<0.01, ** p<0.05, * p<0.1. Band coefficients: at equal ln parental "
          "income and all of 75's components, single-age dummies, weighted, s.e. from 200 cluster-bootstrap draws of "
          "1968 families (common to all rows). Within-son: son FE, single-age dummies, lyp, every component, structure "
          "flag and 5-year cohort x (age-40)/10; s.e. clustered by 1968 family. **Descriptive.**", ""]

    # ---------------------------------------------------------------- A6 (a) treated counts
    md += ["## A6a. Treated sons: father-present sons with a teen layoff year (son-years with a valid wage)", "",
           "| sample | " + " | ".join(BLAB) + " | 25-55 |", "|---" * 8 + "|"]
    for lab, q in (("pooled", v), ("White", v[v.race == "White"]), ("Black", v[v.race == "Black"])):
        q = q[q["nofa"] == 0]
        cnt = [int(q[(q["band"] == k) & (q["f_sh_layoff"] > 0)]["pid"].nunique()) for k in range(6)]
        tot = [int(q[q["band"] == k]["pid"].nunique()) for k in range(6)]
        alls = (int(q[q["f_sh_layoff"] > 0]["pid"].nunique()), int(q["pid"].nunique()))
        md.append(f"| {lab}: treated / father-present sons | " + " | ".join(f"{a:,} / {b:,}" for a, b in zip(cnt, tot))
                  + f" | {alls[0]:,} / {alls[1]:,} |")
        RES[f"A6a|{lab}"] = {"treated": cnt, "sons": tot, "all": alls}
    md += ["", f"Teen layoff years: {info['layoff_years']:,}; median fall in ln family income in a layoff year against "
           f"the son's layoff-free teen waves {info['median_drop_layoff_years']:.3f}; hours unemployed measured in "
           f"{info['share_layoff_years_hu_measured']:.0%} of layoff years, UI receipt in "
           f"{info['share_layoff_years_ub_measured']:.0%} (received in {info['share_layoff_years_ui']:.0%}), employment "
           f"status (1983+) in {info['share_layoff_years_temp_measured']:.0%}.", ""]
    print(f"A6a {time.time() - t0:.0f}s", flush=True)

    # ---------------------------------------------------------------- A6 (b) layoff vs closure change, common draws
    md += ["## A6b. Layoff change vs closure change (45-49 minus 25-29), ln earnings, common draws", "",
           "| sample | layoff change | closure change | layoff - closure |", "|---" * 4 + "|"]
    for lab, q in (("pooled", v), ("White", v[v.race == "White"])):
        g0 = band_fit(q, "ly", 0, BT, COMPS, ["f_sh_layoff", "f_sh_close"])
        g4 = band_fit(q, "ly", 4, BT, COMPS, ["f_sh_layoff", "f_sh_close"])
        chL = (g4["f_sh_layoff"][0] - g0["f_sh_layoff"][0], g4["f_sh_layoff"][1] - g0["f_sh_layoff"][1])
        chC = (g4["f_sh_close"][0] - g0["f_sh_close"][0], g4["f_sh_close"][1] - g0["f_sh_close"][1])
        dif = (chL[0] - chC[0], chL[1] - chC[1])
        md.append(f"| {lab} | {fmt(chL)} | {fmt(chC)} | {fmt(dif)} |")
        RES[f"A6b|{lab}"] = {k: [float(t[0]), sd(t[1])] for k, t in (("layoff", chL), ("closure", chC), ("diff", dif))}
    md.append("")
    print(f"A6b {time.time() - t0:.0f}s", flush=True)

    # ---------------------------------------------------------------- within-son base and timing tests (A6 c)
    base = ["lyp"] + COMPS + STRUCT + COH
    XB = xage(r, base)
    xage(r, ["lay_a6", "lay_a20", "clo_a6", "clo_a20", "lyp20", "lyp20_na"] + split_cols)
    v = r[r["lw"].notna()].copy()
    md += ["## A6c. Within the same son: equality of the three timing windows (ln earnings)", "",
           "Sons with all three windows measured (the father is a head at the son's 6-12 and 20-26). Coefficients per "
           "unit share x (age-40)/10.", "",
           "| sample | layoff 6-12 x age | layoff 13-19 x age | layoff 20-26 x age | 13-19 minus 6-12 | 13-19 minus "
           "20-26 | all three equal (chi2, p) | N son-years / sons |", "|---" * 8 + "|"]
    T = ["lay_a6_xa", "f_sh_layoff_xa", "lay_a20_xa"]
    for lab, q in (("pooled", v), ("White", v[v.race == "White"]), ("Black", v[v.race == "Black"])):
        q = q.dropna(subset=["lay_a6", "lay_a20"])
        f = fe_fit(q, "ly", XB + ["lay_a6_xa", "lay_a20_xa", "clo_a6_xa", "clo_a20_xa"])
        b = {x: (f["b"][x], float(np.sqrt(f["V"].loc[x, x]))) for x in T}
        d1 = lincom(f, {"f_sh_layoff_xa": 1, "lay_a6_xa": -1})
        d2 = lincom(f, {"f_sh_layoff_xa": 1, "lay_a20_xa": -1})
        W = wald(f, np.array([[1, -1, 0], [0, -1, 1]]), T)
        md.append(f"| {lab} | {c(b[T[0]])} | {c(b[T[1]])} | {c(b[T[2]])} | {c(d1)} | {c(d2)} | "
                  f"{W[0]:.2f} (p={W[2]:.3f}) | {f['n']:,} / {f['sons']:,} |")
        RES[f"A6c|{lab}"] = {"b": {x: list(b[x]) for x in T}, "d_6": list(d1), "d_20": list(d2), "wald": list(W),
                            "n": f["n"], "sons": f["sons"]}
    md.append("")
    print(f"A6c {time.time() - t0:.0f}s", flush=True)

    # ---------------------------------------------------------------- A6 (d) leave one cohort out
    md += ["## A6d. Leave one five-year birth cohort out (pooled, ln earnings)", "",
           "| cohort left out | sons left | band change 45-49 - 25-29 (layoff) | within-son layoff x age |",
           "|---" * 4 + "|"]
    for coh in [None] + sorted(v["coh5"].unique()):
        q = v if coh is None else v[v["coh5"] != coh]
        g0 = band_fit(q, "ly", 0, BT, COMPS, ["f_sh_layoff"])["f_sh_layoff"]
        g4 = band_fit(q, "ly", 4, BT, COMPS, ["f_sh_layoff"])
        ch = None
        if "f_sh_layoff" in g4:
            ch = (g4["f_sh_layoff"][0] - g0[0], g4["f_sh_layoff"][1] - g0[1])
        f = fe_fit(q, "ly", [x for x in XB if not (coh is not None and x == f"coh_{coh}_xa")])
        fe = (f["b"]["f_sh_layoff_xa"], float(np.sqrt(f["V"].loc["f_sh_layoff_xa", "f_sh_layoff_xa"])))
        md.append(f"| {'none' if coh is None else f'{coh}-{coh + 4}'} | {q['pid'].nunique():,} | {fmt(ch)} | {c(fe)} |")
        RES[f"A6d|{coh}"] = {"change": [float(ch[0]), sd(ch[1])] if ch else None, "fe": list(fe)}
    md.append("")
    print(f"A6d {time.time() - t0:.0f}s", flush=True)

    # ---------------------------------------------------------------- A2 timing as the control group
    q = v.dropna(subset=["lay_a6", "lay_a20"]).copy()
    q = q[(q["nofa"] == 0) & ((q["f_sh_layoff"] > 0) | (q["lay_a6"] > 0) | (q["lay_a20"] > 0))].copy()
    q["T"] = (q["f_sh_layoff"] > 0).astype(float)
    q["E"] = ((q["T"] == 0) & (q["lay_a6"] > 0)).astype(float)
    q["L"] = ((q["T"] == 0) & (q["E"] == 0)).astype(float)
    for g in ("T", "E"):
        q[f"{g}_xa"] = q[g] * q["agec"]
    for k in range(6):
        q[f"T_b{k}"] = q["T"] * (q["band"] == k)
        q[f"E_b{k}"] = q["E"] * (q["band"] == k)
    XB2 = [x for x in XB if x != "f_sh_layoff_xa"]
    md += ["## A2. Timing as the control group: sons whose father was laid off at some time (6-12, 13-19 or 20-26)", "",
           "Groups: T = a layoff at the son's 13-19; E = at 6-12, not 13-19; L = only at 20-26 (reference). Son FE; "
           "single-age dummies; lyp and every component except the layoff share x (age-40)/10.", "",
           "| sample | sons T / E / L | T x age | E x age | T - E | all equal (chi2, p) | N son-years |",
           "|---" * 7 + "|"]
    for lab, qq in (("pooled", q), ("White", q[q.race == "White"]), ("Black", q[q.race == "Black"])):
        f = fe_fit(qq, "ly", XB2 + ["T_xa", "E_xa"])
        bt = (f["b"]["T_xa"], float(np.sqrt(f["V"].loc["T_xa", "T_xa"])))
        be = (f["b"]["E_xa"], float(np.sqrt(f["V"].loc["E_xa", "E_xa"])))
        d = lincom(f, {"T_xa": 1, "E_xa": -1})
        W = wald(f, np.eye(2), ["T_xa", "E_xa"])
        o = qq.drop_duplicates("pid")
        ns = (int(o["T"].sum()), int(o["E"].sum()), int(o["L"].sum()))
        md.append(f"| {lab} | {ns[0]:,} / {ns[1]:,} / {ns[2]:,} | {c(bt)} | {c(be)} | {c(d)} | {W[0]:.2f} "
                  f"(p={W[2]:.3f}) | {f['n']:,} |")
        RES[f"A2|{lab}"] = {"sons": ns, "T": list(bt), "E": list(be), "T-E": list(d), "wald": list(W)}
    # band profile, pooled: T x band and E x band (band 0 the base through the son FE)
    f = fe_fit(q, "ly", XB2 + [f"T_b{k}" for k in range(1, 6)] + [f"E_b{k}" for k in range(1, 6)])
    md += ["", "Band profile (pooled): T x band and E x band relative to 25-29 (son FE absorbs the level).", "",
           "| group | " + " | ".join(BLAB[1:]) + " |", "|---" * 6 + "|"]
    for g in ("T", "E"):
        cells = [(f["b"][f"{g}_b{k}"], float(np.sqrt(f["V"].loc[f"{g}_b{k}", f"{g}_b{k}"]))) for k in range(1, 6)]
        md.append(f"| {g} | " + " | ".join(c(x) for x in cells) + " |")
        RES[f"A2|bands|{g}"] = [list(x) for x in cells]
    W = wald(f, np.hstack([np.eye(5), -np.eye(5)]), [f"T_b{k}" for k in range(1, 6)] + [f"E_b{k}" for k in range(1, 6)])
    md += ["", f"T and E profiles equal: chi2({W[1]}) = {W[0]:.2f}, p = {W[2]:.3f}.", ""]
    RES["A2|bands|wald_T_eq_E"] = list(W)
    print(f"A2 {time.time() - t0:.0f}s", flush=True)

    # ---------------------------------------------------------------- A3 splits
    SPL = [("income loss", ["lay_loss_big", "lay_loss_small", "lay_loss_na"]),
           ("unemployment (hours >= 500)", ["lay_hu_long", "lay_hu_short", "lay_hu_na"]),
           ("UI receipt", ["lay_ui", "lay_noui", "lay_ui_na"]),
           ("repeat", ["lay_one", "lay_multi"]),
           ("temporary layoff (1983+)", ["lay_temp", "lay_perm", "lay_temp_na"])]
    md += ["## A3. What the layoff is vs what it does: the teen layoff share split into parts", "",
           "Each row replaces the layoff share by its parts (they add up to it). Band columns: coefficient at equal lyp "
           "and all other components (bootstrap s.e.); within-son: part x (age-40)/10, son FE. Last column: equality "
           "of the first two parts in the within-son design.", "",
           "| split | part | 25-29 | 45-49 | change | within-son x age | first two equal (within-son) |",
           "|---" * 7 + "|"]
    noL = [x for x in COMPS if x != "f_sh_layoff"]
    for title, parts in SPL:
        comps = noL + parts
        g0 = band_fit(v, "ly", 0, BT, comps, parts)
        g4 = band_fit(v, "ly", 4, BT, comps, parts)
        f = fe_fit(v, "ly", XB2 + [f"{p}_xa" for p in parts])
        W = wald(f, np.array([[1, -1]]), [f"{parts[0]}_xa", f"{parts[1]}_xa"])
        for j, p in enumerate(parts):
            a, b = g0.get(p), g4.get(p)
            ch = (b[0] - a[0], b[1] - a[1]) if a and b else None
            fe = (f["b"][f"{p}_xa"], float(np.sqrt(f["V"].loc[f"{p}_xa", f"{p}_xa"])))
            md.append(f"| {title if j == 0 else ''} | {p} | {fmt(a)} | {fmt(b)} | {fmt(ch)} | {c(fe)} | "
                      + (f"chi2 {W[0]:.2f}, p={W[2]:.3f}" if j == 0 else "") + " |")
            RES[f"A3|{title}|{p}"] = {"a": [float(a[0]), sd(a[1])] if a else None,
                                      "b": [float(b[0]), sd(b[1])] if b else None,
                                      "ch": [float(ch[0]), sd(ch[1])] if ch else None, "fe": list(fe)}
        RES[f"A3|{title}|wald"] = list(W)
    md.append("")
    # (vi) parental income at 20-26 as a control
    md += ["### A3 (vi). Parental income at the son's 20-26 as a control", "",
           "| spec | layoff 25-29 | layoff 45-49 | change | within-son layoff x age |", "|---" * 5 + "|"]
    for lab, ctrl, xs in (("as in 88", (), XB), ("+ ln parental income at 20-26 (and its flag)", ("lyp20", "lyp20_na"),
                                                  XB + ["lyp20_xa", "lyp20_na_xa"])):
        a = band_fit(v, "ly", 0, BT, COMPS, ["f_sh_layoff"], ctrl)["f_sh_layoff"]
        b = band_fit(v, "ly", 4, BT, COMPS, ["f_sh_layoff"], ctrl)["f_sh_layoff"]
        ch = (b[0] - a[0], b[1] - a[1])
        f = fe_fit(v, "ly", xs)
        fe = (f["b"]["f_sh_layoff_xa"], float(np.sqrt(f["V"].loc["f_sh_layoff_xa", "f_sh_layoff_xa"])))
        md.append(f"| {lab} | {fmt(a)} | {fmt(b)} | {fmt(ch)} | {c(fe)} |")
        RES[f"A3vi|{lab}"] = {"a": [float(a[0]), sd(a[1])], "b": [float(b[0]), sd(b[1])],
                             "ch": [float(ch[0]), sd(ch[1])], "fe": list(fe)}
    md.append("")
    (OUT / "layoff_selection.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "layoff_selection.json", "w"), indent=1, default=float)
    print(f"done {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
