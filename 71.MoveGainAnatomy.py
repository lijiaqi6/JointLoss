r"""Fable T1/T8 (proposals/fable_search_friction_ige.md, 2026-10-19): anatomy of the wage gain at a job move by race and
parental income. PSID (main) and NLSY79 (replication, with the AFQT).

The fact (Table jobmoves, 42 section C): growth at a non-displaced move falls with parental income for Black sons
(-0.064***, 25-34) and not for White sons (0.005); difference 0.069**. Two readings with the same reduced form:
  (i)  search friction in offer quality: sons of richer Black parents get worse outside offers -> the gradient sits in
       the DESTINATION wage (lower for Black), the origin wage gradient equal by race, at every origin tenure;
  (ii) an entry premium in the job, lost at the move: sons of richer Black parents start on a premium that is not
       portable -> the gradient sits in the ORIGIN wage (higher for Black relative to their own career), destination
       equal, concentrated at short origin tenure.
  (iii) neither: the gradient does not survive schooling, and origin and destination gradients are equal by race.
STATISTICS, by race and band (25-34, 35-55), raw and at equal schooling (years; NLSY79 also + AFQT):
  (1) annual wage growth over the pair, movers (PSID: no displacement between the wage years)
  (2) origin ln wage, (3) destination ln wage (levels), movers
  (4) origin residual, (5) destination residual: ln wage minus the son's mean ln wage over all his valid years, movers
  (6) the same residual for stayers at the later interview (reference)
  (7) P(move) on all pairs
  splits of (1): origin tenure < 3 years / >= 3 years; origin job type G / O (PSID, the model's job types).
Pairs: consecutive interviews 1-2 years apart with a wage at both (PSID waves 1985-2023, 27's rows; NLSY79 CPS job,
employer change between rounds; the NLSY79 does not flag displacement here, so its movers include the displaced).
Controls: quartic in age, year FE. OLS, s.e. clustered by 1968 family / 1979 household; the race difference from the
fully interacted regression. DESCRIPTIVE. Writes output/move_gain_anatomy.md and .json.
"""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import DATA, OUT  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R36 = _load("s36", "36.SameEmployerGrowthChecks.py")
BANDS = [(25, 34), (35, 55)]


def ols_cl(d, y, x, ctrl, cl):
    """y on [x, ctrl..., age quartic, year FE] separately by race and fully interacted; clustered s.e."""
    out = {}
    d = d[d[y].notna() & d[x].notna() & d[cl].notna()].copy()
    for c in ctrl:
        d = d[d[c].notna()]
    a = (d["age"] - 40) / 10
    base = pd.DataFrame({"a1": a, "a2": a ** 2, "a3": a ** 3, "a4": a ** 4}, index=d.index)
    yfe = pd.get_dummies(d["yfe"].astype(int), prefix="y", drop_first=True).astype(float)
    Z = pd.concat([d[[x] + ctrl].astype(float), base, yfe], axis=1)

    def fit(Xm, yv, g):
        Xm = np.column_stack([Xm, np.ones(len(yv))])
        XtXi = np.linalg.pinv(Xm.T @ Xm)
        b = XtXi @ Xm.T @ yv
        u = yv - Xm @ b
        S = pd.DataFrame(u[:, None] * Xm).groupby(g).sum().to_numpy()
        G = S.shape[0]
        n, k = Xm.shape
        V = XtXi @ (S.T @ S) @ XtXi * G / (G - 1) * (n - 1) / (n - k)
        return b, V

    for r in ("White", "Black"):
        m = (d["race"] == r).to_numpy()
        b, V = fit(Z[m].to_numpy(float), d.loc[m, y].to_numpy(float), d.loc[m, cl].to_numpy())
        out[r] = (float(b[0]), float(np.sqrt(V[0, 0])), int(m.sum()), float(d.loc[m, y].mean()))
    bl = (d["race"] == "Black").astype(float).to_numpy()[:, None]
    Zf = np.column_stack([Z.to_numpy(float), Z.to_numpy(float) * bl, bl])
    b, V = fit(Zf, d[y].to_numpy(float), d[cl].to_numpy())
    j = Z.shape[1]                                                  # Black x x
    out["B-W"] = (float(b[j]), float(np.sqrt(V[j, j])), int(len(d)), np.nan)
    return out


def star(p):
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""


def fmt(t):
    b, s = t[0], t[1]
    p = 2 * (1 - norm.cdf(abs(b) / s)) if s > 0 else np.nan
    return f"{b:.4f}{star(p)} ({s:.4f}; p={p:.3f})", p


def psid_pairs():
    r, *_ = R36.psid_build()
    dp = pd.read_pickle(DATA / "psid_displacement.pkl")
    dy = set(zip(dp.loc[dp["main"] == 1, "pid"], dp.loc[dp["main"] == 1, "year"]))
    r = r.sort_values(["pid", "wave"]).copy()
    r["mlw"] = r.groupby("pid")["lw"].transform("mean")             # son's mean ln wage over his valid years
    r["ten_prev"] = r.groupby("pid")["tenure"].shift(1)
    r["wave_prev"] = r.groupby("pid")["wave"].shift(1)
    try:
        G = pd.read_pickle(HERE / "model" / "output" / "data_panel.pkl")[["pid", "wave", "G"]]
        G = G.rename(columns={"wave": "wave_prev", "G": "G_prev"})
        r = r.merge(G, on=["pid", "wave_prev"], how="left")
    except Exception:                                               # job types are optional
        r["G_prev"] = np.nan
    d = r[r["g_lw_t"].notna() & r["wave"].ge(1985) & r["race"].isin(["Black", "White"])].copy()
    gap = d["gap"].fillna(1).astype(int)
    disp = np.zeros(len(d), bool)
    for k in range(0, 3):
        yrs = d["wave"] - 1 - k
        disp |= np.array([(p, y) in dy for p, y in zip(d["pid"], yrs)]) & (k <= gap).to_numpy()
    d["move"] = ((d["stay"] == 0) & ~disp).astype(float)
    d["stayer"] = ((d["stay"] == 1) & ~disp).astype(float)
    d = d[(d["move"] == 1) | (d["stayer"] == 1)].copy()
    d["lw_o"] = d["lw"] - d["d_lw"]                                 # origin (earlier interview) ln wage
    d["lw_d"] = d["lw"]
    d["res_o"], d["res_d"] = d["lw_o"] - d["mlw"], d["lw_d"] - d["mlw"]
    d["gain"] = d["g_lw_t"]
    d["yfe"], d["cl"], d["x"] = d["year"], d["fam68"].astype(float), d["lyp"]
    return d


def nlsy_pairs():
    r, D32, D27, W, M, XWD = R36.psid_build()
    J, kids = R36.nlsy_build(D32, D27, W, M, XWD)
    if "educ" not in J:
        J = J.merge(kids[["pid", "educ"]], on="pid", how="left")
    J = J.sort_values(["pid", "round"]).copy()
    J["mlw"] = J.groupby("pid")["lw"].transform("mean")
    J["ten_prev"] = J.groupby("pid")["ten_y"].shift(1)
    ok = J["gap"].between(1, 2) & J["lw"].notna() & J["lw_l1"].notna()
    d = J[ok & J["race"].isin(["Black", "White"])].copy()
    d["move"] = (d["jj"] != d["jj_l1"]).astype(float)
    d["stayer"] = 1 - d["move"]
    d["lw_o"], d["lw_d"] = d["lw_l1"], d["lw"]
    d["res_o"], d["res_d"] = d["lw_o"] - d["mlw"], d["lw_d"] - d["mlw"]
    d["gain"] = (d["lw"] - d["lw_l1"]) / d["gap"]
    d["x"], d["G_prev"] = d["lyp"], np.nan
    return d


COLS = [("gain", "move", "(1) growth | moved"), ("lw_o", "move", "(2) origin ln wage | moved"),
        ("lw_d", "move", "(3) destination ln wage | moved"), ("res_o", "move", "(4) origin residual | moved"),
        ("res_d", "move", "(5) destination residual | moved"), ("res_d", "stayer", "(6) residual | stayed"),
        ("move", None, "(7) P(moved)")]


def block(d, ctrl, label, res, md, src):
    rows = {}
    for lo, hi in BANDS:
        z = d[d["age"].between(lo, hi)]
        for y, cond, h in COLS:
            zz = z if cond is None else z[z[cond] == 1]
            rows[(lo, hi, h)] = ols_cl(zz, y, "x", ctrl, "cl")
    md += [f"### {src}: {label}", "", "| | " + " | ".join(h for _, _, h in COLS) + " |", "|---" * (len(COLS) + 1) + "|"]
    for lo, hi in BANDS:
        for g in ("White", "Black", "B-W"):
            cells = []
            for _, _, h in COLS:
                s, p = fmt(rows[(lo, hi, h)][g])
                cells.append(s)
                res[f"{src}|{label}|{lo}-{hi}|{g}|{h}"] = dict(zip(("b", "se", "n", "mean"), rows[(lo, hi, h)][g]),
                                                               p=p)
            md.append(f"| {lo}-{hi} {g} | " + " | ".join(cells) + " |")
        md.append(f"| {lo}-{hi} N (W / B) | " + " | ".join(
            f"{rows[(lo, hi, h)]['White'][2]:,} / {rows[(lo, hi, h)]['Black'][2]:,}" for _, _, h in COLS) + " |")
    md.append("")


def splits(d, ctrl, res, md, src):
    md += [f"### {src}: growth | moved, by origin tenure and origin job type ({'raw' if not ctrl else ' + '.join(ctrl)})",
           "", "| | " + " | ".join(f"{lo}-{hi} {g}" for lo, hi in BANDS for g in ("White", "Black", "B-W")) + " |",
           "|---" * 7 + "|"]
    for lab, m in (("origin tenure < 3 years", d["ten_prev"] < 3), ("origin tenure >= 3 years", d["ten_prev"] >= 3),
                   ("origin job G", d["G_prev"] == 1), ("origin job O", d["G_prev"] == 0)):
        z = d[m & (d["move"] == 1)]
        if len(z) < 200:
            continue
        cells = []
        for lo, hi in BANDS:
            o = ols_cl(z[z["age"].between(lo, hi)], "gain", "x", ctrl, "cl")
            for g in ("White", "Black", "B-W"):
                s, p = fmt(o[g])
                cells.append(s + (f" n={o[g][2]:,}" if g != "B-W" else ""))
                res[f"{src}|split|{lab}|{lo}-{hi}|{g}"] = dict(zip(("b", "se", "n", "mean"), o[g]), p=p)
        md.append(f"| {lab} | " + " | ".join(cells) + " |")
    md.append("")


if __name__ == "__main__":
    res = {}
    md = ["# Anatomy of the wage gain at a job move by race and parental income (Fable T1 / T8)", "",
          "Built by `71.MoveGainAnatomy.py` (2026-10-19); definitions in its docstring. Coefficient on log parental "
          "income: estimate (s.e.; p), *** p<0.01, ** p<0.05, * p<0.1; s.e. clustered by 1968 family (PSID) / 1979 "
          "household (NLSY79). Controls: quartic in age, year FE. **Descriptive.**", ""]
    P = psid_pairs()
    md += ["## PSID (parental income: mean log family income at 13-19)", ""]
    for ctrl, lab in (([], "raw"), (["educ"], "at equal schooling")):
        block(P, ctrl, lab, res, md, "PSID")
    for ctrl in ([], ["educ"]):
        splits(P, ctrl, res, md, "PSID")
    N = nlsy_pairs()
    md += ["## NLSY79 (parental income: 1979-81 mean; movers include the displaced)", ""]
    for ctrl, lab in (([], "raw"), (["educ"], "at equal schooling"), (["educ", "afqt"], "at equal schooling and AFQT")):
        block(N, ctrl, lab, res, md, "NLSY79")
    for ctrl in ([], ["educ"]):
        splits(N, ctrl, res, md, "NLSY79")
    (OUT / "move_gain_anatomy.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(res, open(OUT / "move_gain_anatomy.json", "w"), indent=1)
    print("\n".join(md))
