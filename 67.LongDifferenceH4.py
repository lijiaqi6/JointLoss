r"""H4 in long differences (Paper B, Fable 10-hour plan Block 5, 2026-10-19).

Question: is the White sons' pay-off of parental income in human capital accumulation (H4) ability correlated with
parental income? The annual same-employer growth regressions are underpowered for it; the cumulative statistic is
the change of a son's own mean log hourly wage between 25-29 and 35-39 (ten years) and 45-49 (twenty years) on log
parental income, by race, on sons with a wage in both bands.

  PSID: the model's son panel (model/output/data_panel.pkl; Section 8's sample); (1) raw, (2) + years of
        schooling. Clusters: 1968 family.
  NLSY79: men, hourly rate of pay of the CPS job by round (27's extract, CPI 2000 dollars, 2-200), parental income
        1979-81 (2.NLSY79.py logic, nlsy79_kids.pkl), highest grade completed by 35 and the AFQT-3 standardised
        within birth year (36's construction); (3) raw, (4) + schooling, (5) + schooling + AFQT. Clusters: 1979
        household. Unweighted, as the model's targets.
  Model: model E at its estimates (model/output/final_x4/estimates_E.json), seeds 7-16, R = 20, core.longdiff
        on the simulated panel with the PSID observation scheme (mean, seed s.d.).
White - Black from a pooled regression with every regressor interacted with Black.
Writes output/long_difference_h4.csv / .md and paperB_age_profile/tab_h4_longdiff.tex.
Run from IGE/ with IGE_STEPS=age,rehire,xacc IGE_FIX=muG,du IGE_R=20 (for the model part).
"""
import importlib.util
import json
import re
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import norm

IGE = Path(__file__).resolve().parent
OUT = IGE / "output"
DATA = IGE / "data"
sys.path.insert(0, str(IGE / "model"))
import core  # noqa: E402
import estimate as est  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, IGE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def nlsy_sons():
    R27 = _load("e27", "27.CareerWageGrowth.py")
    R36 = _load("e36", "36.SameEmployerGrowthChecks.py")
    X = R36.nlsy_extract()
    k = X[["pid", "sample_id", "sex", "birth_year"]].copy()
    k["birth_year"] = np.where(k["birth_year"] < 100, 1900 + k["birth_year"], k["birth_year"])
    a = pd.to_numeric(X["AFQT-3"], errors="coerce")
    k["afqt_pct"] = (a.where(a >= 0) / 1000).to_numpy()
    k["wt79"] = X["wt79"].to_numpy()
    k["afqt"] = np.nan
    civ = k["sample_id"].between(1, 14) & k["afqt_pct"].notna() & (k["wt79"] > 0)
    for by, z in k[civ].groupby("birth_year"):
        mu = np.average(z["afqt_pct"], weights=z["wt79"])
        sd = np.sqrt(np.average((z["afqt_pct"] - mu) ** 2, weights=z["wt79"]))
        idx = k.index[(k["birth_year"] == by) & k["afqt_pct"].notna()]
        k.loc[idx, "afqt"] = (k.loc[idx, "afqt_pct"] - mu) / sd
    hg = {int(c[-2:]) + (1900 if int(c[-2:]) > 50 else 2000): c for c in X.columns if re.fullmatch(r"HGCREV\d\d", c)}
    edu = pd.Series(np.nan, index=X.index)
    for y in sorted(hg):
        v = pd.to_numeric(X[hg[y]], errors="coerce").where(lambda s: s.between(0, 20))
        edu = v.where(v.notna() & ((y - k["birth_year"]) <= 35), edu)
    k["educ"] = edu.to_numpy()
    kids = pd.read_pickle(DATA / "nlsy79_kids.pkl")
    kids = kids[(kids["female"] == 0) & kids["lpinc_av"].notna() & kids["race"].isin(["Black", "White"])]
    k = k[["pid", "afqt", "educ"]].merge(kids[["pid", "race", "birth_year", "hhid", "lpinc_av"]], on="pid")
    # wages: 27's extract, CPS job by round
    d = R27.nlsy_extract()
    d = d[d["pid"].isin(k["pid"])].reset_index(drop=True)
    rx = re.compile(r"EMPLOYERS_ALL_(HRLY_WAGE|CPSJOB)_(\d{4})\.(\d\d)$")
    recs = {}
    for c in d.columns:
        m = rx.match(c)
        if m:
            recs.setdefault((int(m.group(2)), m.group(3)), {})[m.group(1)] = c
    rows = []
    for (y, jj), cs in recs.items():
        if {"HRLY_WAGE", "CPSJOB"} <= set(cs):
            x = pd.DataFrame({"pid": d["pid"], "round": y, "hw": d[cs["HRLY_WAGE"]], "cps": d[cs["CPSJOB"]]})
            rows.append(x[x["cps"] == 1])
    J = pd.concat(rows, ignore_index=True).drop_duplicates(["pid", "round"]).merge(k, on="pid")
    J["age"] = J["round"] - J["birth_year"]
    w = J["hw"].where(J["hw"] > 0) / 100 * J["round"].map(lambda y: R27.CPI[2000] / R27.CPI[min(int(y), 2022)])
    J["lw"] = np.log(w.where(w.between(2, 200)))
    J = J[J["age"].between(25, 49) & J["lw"].notna()]
    S = {"pid": [], "x": [], "e": [], "afqt": [], "black": [], "cl": []}
    g = J.groupby("pid")
    base = k.set_index("pid")
    bands = {"m2529": (25, 29), "m3539": (35, 39), "m4549": (45, 49)}
    tab = pd.DataFrame({b: J[J["age"].between(lo, hi)].groupby("pid")["lw"].mean() for b, (lo, hi) in bands.items()})
    tab = tab.join(base[["lpinc_av", "educ", "afqt", "race", "hhid"]], how="inner")
    tab["black"] = (tab["race"] == "Black").astype(float)
    return tab.rename(columns={"lpinc_av": "x", "educ": "e", "hhid": "cl"})


def psid_sons():
    P = pd.read_pickle(IGE / "model" / "output" / "data_panel.pkl")
    S = core.son_bands({c: P[c].to_numpy() for c in P.columns})
    t = pd.DataFrame(S).set_index("pid")
    t["cl"] = P.drop_duplicates("pid").set_index("pid")["fam68"].reindex(t.index)
    return t


def reg(t, horizon, ctrl):
    """by race and W - B (pooled, fully interacted); returns {group: (coef, se, p, n)} for the x coefficient."""
    out = {}
    y = t[f"m{horizon}"] - t["m2529"]
    d = t.assign(y=y).dropna(subset=["y", "x", *ctrl, "cl"])
    for g, sub in (("White", d[d["black"] == 0]), ("Black", d[d["black"] == 1])):
        X = sm.add_constant(sub[["x", *ctrl]].astype(float))
        r = sm.OLS(sub["y"], X).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(sub["cl"])[0]})
        out[g] = (r.params["x"], r.bse["x"], r.pvalues["x"], len(sub))
    Z = d[["x", *ctrl]].astype(float)
    Xp = pd.concat([Z, Z.mul(d["black"], axis=0).add_suffix("_B"), d[["black"]]], axis=1)
    r = sm.OLS(d["y"], sm.add_constant(Xp)).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d["cl"])[0]})
    out["White - Black"] = (-r.params["x_B"], r.bse["x_B"], r.pvalues["x_B"], len(d))
    return out


def model_task(args):
    th, seed = args
    T = est.G_["T"]
    idx = np.repeat(np.arange(T.n), 20)
    _, P = est.sim_moments(th, idx=idx, Dr=core.Draws(len(idx), seed))
    return core.longdiff(P)


def star(p):
    return "^{***}" if p < 0.01 else "^{**}" if p < 0.05 else "^{*}" if p < 0.10 else ""


if __name__ == "__main__":
    ps, nl = psid_sons(), nlsy_sons()
    specs = [("PSID", ps, []), ("PSID", ps, ["e"]), ("NLSY79", nl, []), ("NLSY79", nl, ["e"]),
             ("NLSY79", nl, ["e", "afqt"])]
    res = {}
    for h in ("3539", "4549"):
        for i, (src, t, ctrl) in enumerate(specs):
            res[(h, i)] = reg(t, h, ctrl)
    E = json.load(open(IGE / "model" / "output" / "final_x4" / "estimates_E.json"))
    th = core.theta_vec(E["E"]["theta"])
    est.G_.update(est.setup())
    with Pool(est.WORKERS, initializer=est.init_worker) as pool:
        mr = pool.map(model_task, [(th, s) for s in range(7, 17)])
    mod = {k: (float(np.mean([r[k] for r in mr])), float(np.std([r[k] for r in mr], ddof=1))) for k in mr[0]}
    recs = []
    for (h, i), d in res.items():
        for g, (c, s, p, n) in d.items():
            recs.append(dict(horizon=h, spec=i + 1, source=specs[i][0], controls="+".join(specs[i][2]) or "none",
                             group=g, coef=c, se=s, p=p, n=n))
    for h, lab in (("3539", "10"), ("4549", "20")):
        for g, r in (("White", "W"), ("Black", "B")):
            for j, key in ((6, f"ld{lab}_x_{r}"), (7, f"ld{lab}_x_net_e_{r}")):
                recs.append(dict(horizon=h, spec=j, source="model E", controls="none" if j == 6 else "e", group=g,
                                 coef=mod[key][0], se=mod[key][1], p=np.nan, n=mod[f"ld{lab}_n_{r}"][0]))
        for j, key in ((6, f"ld{lab}_x"), (7, f"ld{lab}_x_net_e")):
            recs.append(dict(horizon=h, spec=j, source="model E", controls="none" if j == 6 else "e",
                             group="White - Black", coef=mod[key + "_W"][0] - mod[key + "_B"][0], se=np.nan, p=np.nan,
                             n=np.nan))
    R = pd.DataFrame(recs)
    R.to_csv(OUT / "long_difference_h4.csv", index=False)
    # table: one regression per column
    rows = []
    for h, hl in (("3539", "Change 25--29 to 35--39"), ("4549", "Change 25--29 to 45--49")):
        rows.append(r"\multicolumn{8}{l}{\textit{" + hl + r": coefficient on log parental income}} \\")
        for g in ("White", "Black", "White - Black"):
            cells, ses = [], []
            for j in range(1, 8):
                z = R[(R["horizon"] == h) & (R["spec"] == j) & (R["group"] == g)].iloc[0]
                if j <= 5:
                    cells.append(f"${z['coef']:.3f}{star(z['p'])}$")
                    ses.append(f"({z['se']:.3f})")
                else:
                    cells.append(f"${z['coef']:.3f}$")
                    ses.append(f"[{z['se']:.3f}]" if np.isfinite(z["se"]) else "")
            rows.append(f"\\quad {g.replace(' - ', ' $-$ ')} & " + " & ".join(cells) + r" \\")
            rows.append(" & " + " & ".join(ses) + r" \\")
        for g in ("White", "Black"):
            ns = [R[(R["horizon"] == h) & (R["spec"] == j) & (R["group"] == g)].iloc[0]["n"] for j in range(1, 6)]
            rows.append(f"\\quad Sons, {g} & " + " & ".join(f"{int(n):,}" for n in ns) + r" & & \\")
    head = (r" & \multicolumn{2}{c}{PSID} & \multicolumn{3}{c}{NLSY79} & \multicolumn{2}{c}{Model E} \\"
            "\n" r" & (1) & (2) & (3) & (4) & (5) & (6) & (7) \\"
            "\n" r"Controls & none & schooling & none & schooling & schooling, AFQT & none & schooling \\")
    T = [r"\begin{table}[!htbp]", r"\centering",
         r"\caption{The pay-off of parental income in accumulation in long differences: growth of a son's own wage}",
         r"\label{tab:h4longdiff}", r"\resizebox{\ifdim\width>\textwidth\textwidth\else\width\fi}{!}{%",
         r"\begin{tabular}{lccccccc}", r"\toprule", head, r"\midrule", *rows, r"\bottomrule", r"\end{tabular}}",
         r"\par\smallskip",
         r"\begin{minipage}{\textwidth}\footnotesize \textit{Notes:} Outcome: the change of the son's mean log hourly "
         r"wage between the bands, on sons with a wage in both; regressor: log parental income (PSID 13--19 mean; "
         r"NLSY79 1979--81), with years of schooling (PSID; NLSY79 highest grade completed by 35) and the AFQT "
         r"(NLSY79, standardised within birth year) as controls. Columns (1)--(5): OLS by race, standard errors "
         r"clustered by 1968 family (PSID) or 1979 household (NLSY79) in parentheses; White $-$ Black from the pooled "
         r"regression with every regressor interacted with race. Columns (6)--(7): the same statistic on model E's "
         r"simulated panel (PSID observation scheme, 20 simulated sons per PSID son), mean over ten seeds with the "
         r"seed s.d.\ in brackets. $^{***}$ $p<0.01$, $^{**}$ $p<0.05$, $^{*}$ $p<0.1$. Code: "
         r"\texttt{IGE/67.LongDifferenceH4.py}.\end{minipage}", r"\end{table}"]
    (IGE / "paperB_age_profile" / "tab_h4longdiff.tex").write_text("\n".join(T) + "\n", encoding="utf-8")
    L = ["# H4 in long differences", ""] + [f"| {r.horizon} | ({r.spec}) {r.source} | {r.controls} | {r.group} | "
                                             f"{r.coef:.4f} | ({r.se:.4f}) | p {r.p:.3f} | n {r.n} |"
                                             for r in R.itertuples()]
    (OUT / "long_difference_h4.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))
