r"""Compile bps_reconciliation results (2026-10-18): Step 0 replication vs published, Step 1 relaxations, Step 2.

Reads the run outputs in the local work folder (argv[1]; est_*.csv and reps_*.dta per specification, step2_results,
attrition, attrition_duw, separation) and writes
  bps_reconciliation/bps_reconciliation.csv   every number (table, spec, parameter, value, se, p, se_type, ...)
  bps_reconciliation/tables/*.md              markdown tables (pasted into bps_reconciliation.md)
Standard errors: GMM (clustered by household) for the wage-process parameters, as in BPS Table 3; block bootstrap
(households resampled, BPS's bootstrap.do; s.e. = interquartile range / 1.349 over successful replications, as in
BPS) for everything else where a bootstrap was run; otherwise the GMM s.e. of the second step, which does not
correct for the first-step estimates (marked with a dagger). p-values from the normal distribution.
"""
import sys
from math import erf, sqrt
from pathlib import Path

import numpy as np
import pandas as pd

OUTDIR = Path(__file__).resolve().parents[1]
W = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    r"C:\Users\cm1jil\AppData\Local\Temp\claude\g--My-Drive-Selection-vs-risk\c16f819d-4913-4b50-9f11-a4daf3178246"
    r"\scratchpad\bps_work")
ROWS = []


def pnorm(z):
    return 0.5 * (1 + erf(z / sqrt(2)))


def pval(b, se):
    if se is None or not np.isfinite(se) or se <= 0 or not np.isfinite(b):
        return np.nan
    return 2 * (1 - pnorm(abs(b / se)))


def stars(p):
    if not np.isfinite(p):
        return ""
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""


def fmt(b, se=np.nan, p=np.nan, d=3, dagger=False):
    if b is None or not np.isfinite(b):
        return "n/a"
    s = f"{b:.{d}f}{stars(p)}"
    if np.isfinite(se) and se > 0:
        s += f" ({se:.{d}f}{'†' if dagger else ''}; p={p:.3f})"
    return s


# ------------------------------------------------------------------ loading
def load_est(spec, run):
    f = W / spec / f"est_{run}.csv"
    if not f.exists():
        return None
    e = pd.read_csv(f).set_index("_varname")
    return e


def load_reps(spec, run):
    f = W / spec / f"reps_{run}.dta"
    if not f.exists():
        return None
    r = pd.read_stata(f)
    r = r[r["rep"] > 0]
    if "pi" in r:
        r = r[r["pi"].notna()]
    return r


def bs_se(reps, var):
    if reps is None or var not in reps:
        return np.nan, 0
    x = reps[var].dropna()
    x = x[np.isfinite(x)]
    if len(x) < 5:
        return np.nan, len(x)
    q1, q3 = np.percentile(x, [25, 75])
    return (q3 - q1) / 1.349, len(x)


def nrows(spec):
    f = W / spec / "data4estimation.dta"
    if not f.exists():
        return np.nan
    return len(pd.read_stata(f, columns=["year"]))


PARAMS = [  # (key, label, source, decimals)
    ("s_u1", "Var. transitory, husband (sigma2_u1)", "g9", 4),
    ("s_v1", "Var. permanent, husband (sigma2_v1)", "g9", 4),
    ("s_u2", "Var. transitory, wife (sigma2_u2)", "g9", 4),
    ("s_v2", "Var. permanent, wife (sigma2_v2)", "g9", 4),
    ("r_u1u2", "Cov. transitory shocks (sigma_u1u2)", "g9", 4),
    ("corr_u", "  correlation, transitory", "g9c", 2),
    ("r_v1v2", "Cov. permanent shocks (sigma_v1v2)", "g9", 4),
    ("corr_v", "  correlation, permanent", "g9c", 2),
    ("pi", "E(pi)", "g10", 3),
    ("s_report", "E(s)", "g10", 3),
    ("eta_c_p", "eta_c,p", "g10", 3),
    ("eta_h1_w1", "eta_h1,w1", "g10", 3),
    ("eta_h2_w2", "eta_h2,w2", "g10", 3),
    ("eta_c_w1", "eta_c,w1", "g10", 3),
    ("eta_h1_p", "eta_h1,p", "g10", 3),
    ("eta_c_w2", "eta_c,w2", "g10", 3),
    ("eta_h2_p", "eta_h2,p", "g10", 3),
    ("eta_h1_w2", "eta_h1,w2", "g10", 3),
    ("eta_h2_w1", "eta_h2,w1", "g10", 3),
    ("ch_m_h2v1", "Marshallian: wife's hours / husband's wage (kappa_h2,v1)", "g10", 3),
    ("ch_m_h1v1", "Marshallian: husband own (kappa_h1,v1 - 1)", "g10", 3),
    ("ch_m_h2v2", "Marshallian: wife own (kappa_h2,v2 - 1)", "g10", 3),
    ("ch_m_cv1", "Marshallian: consumption / husband's wage (kappa_c,v1)", "g10", 3),
    ("ch_c0", "Chain (10% perm. fall): fixed labor supply, no taxes, no savings", "g10", 2),
    ("ch_c1", "  + taxes and transfers", "g10", 2),
    ("ch_c2", "  + husband's labor supply", "g10", 2),
    ("ch_c3", "  + wife's labor supply", "g10", 2),
    ("ch_c4", "  + savings (= 10 x kappa_c,v1)", "g10", 2),
    ("ch_gov", "Share of insurance: government", "g10", 3),
    ("ch_fam", "Share of insurance: family labor supply", "g10", 3),
    ("ch_sav", "Share of insurance: savings", "g10", 3),
    ("beta", "Outside insurance beta (Table 4 col. 5 spec.)", "beta", 3),
    ("observations", "N (preference GMM, household-years)", "g10", 0),
    ("n_rows", "N (household-years in data4estimation)", "rows", 0),
]


def spec_values(spec):
    """{key: (value, se, p, se_type, nreps)} for one specification."""
    g10, g9, gb = load_est(spec, "gmm10"), load_est(spec, "gmm9"), load_est(spec, "beta")
    rb, rbb = load_reps(spec, "bs"), load_reps(spec, "bsbeta")
    out = {}
    for key, _, src, _ in PARAMS:
        v, se, st, nr = np.nan, np.nan, "", 0
        if src == "g9" and g9 is not None:
            v, se, st = g9.loc[f"{key}_1", "value"], g9.loc[f"{key}_1", "se"], "GMM"
        elif src == "g9c" and g9 is not None:
            if key == "corr_u":
                c, a, b = g9.loc["r_u1u2_1", "value"], g9.loc["s_u1_1", "value"], g9.loc["s_u2_1", "value"]
            else:
                c, a, b = g9.loc["r_v1v2_1", "value"], g9.loc["s_v1_1", "value"], g9.loc["s_v2_1", "value"]
            v = c / sqrt(a * b) if a > 0 and b > 0 else np.nan
            st = "-"
        elif src == "g10" and g10 is not None and key in g10.index:
            v = g10.loc[key, "value"]
            se, nr = bs_se(rb, key)
            st = "bootstrap"
            if not np.isfinite(se) and key not in ("observations",):
                se = g10.loc[key, "se"] if "se" in g10.columns else np.nan
                st = "GMM2" if np.isfinite(se) else ""
            if key == "observations":
                se, st = np.nan, ""
        elif src == "beta" and gb is not None:
            v = gb.loc["beta", "value"]
            se, nr = bs_se(rbb, "beta")
            st = "bootstrap"
            if not np.isfinite(se):
                se, st = gb.loc["beta", "se"], "GMM2"
            if abs(v) > 100:                 # GMM did not converge
                v, se, st = np.nan, np.nan, "not converged"
        elif src == "rows":
            v = nrows(spec)
        p = pval(v, se) if st in ("GMM", "bootstrap", "GMM2") else np.nan
        out[key] = (v, se, p, st, nr)
    return out


# ------------------------------------------------------------------ Step 0: published values
PUB_T3 = {  # age groups 30-37, 38-42, 43-47, 48-52, 53-57, all ages: (estimate, s.e.)
    "s_u1": [(0.0431, 0.0127), (0.0163, 0.0113), (0.0364, 0.0141), (-0.0024, 0.0135), (0.0408, 0.0182), (0.0275, 0.0063)],
    "s_v1": [(0.0273, 0.0085), (0.0264, 0.0075), (0.0146, 0.0121), (0.0500, 0.0142), (0.0377, 0.0106), (0.0303, 0.0049)],
    "s_u2": [(0.0257, 0.0142), (0.0053, 0.0106), (0.0157, 0.0107), (0.0111, 0.0088), (-0.0191, 0.0116), (0.0125, 0.0057)],
    "s_v2": [(0.0442, 0.0120), (0.0447, 0.0097), (0.0245, 0.0070), (0.0324, 0.0071), (0.0506, 0.0128), (0.0382, 0.0044)],
    "r_u1u2": [(0.0124, 0.0067), (0.0060, 0.0058), (0.0007, 0.0059), (0.0020, 0.0048), (0.0116, 0.0056), (0.0058, 0.0027)],
    "r_v1v2": [(-0.0008, 0.0067), (0.0018, 0.0046), (0.0051, 0.0037), (0.0072, 0.0041), (0.0002, 0.0053), (0.0027, 0.0023)],
}
T3LAB = {"s_u1": "Males, transitory sigma2_u1", "s_v1": "Males, permanent sigma2_v1",
         "s_u2": "Females, transitory sigma2_u2", "s_v2": "Females, permanent sigma2_v2",
         "r_u1u2": "Covariance, transitory sigma_u1u2", "r_v1v2": "Covariance, permanent sigma_v1v2"}
PUB_T4 = {  # col 1, col 4, col 5
    "pi": [(0.150, 0.004)] * 3, "s_report": [(0.708, 0.013)] * 3,
    "eta_c_p": [(0.417, 0.122), (0.494, 0.168), (0.433, 0.121)],
    "eta_h1_w1": [(0.681, 0.189), (0.653, 0.178), (0.697, 0.189)],
    "eta_h2_w2": [(0.958, 0.267), (0.976, 0.281), (0.961, 0.271)],
    "eta_c_w1": [(-0.162, 0.074), (-0.182, 0.066), (-0.169, 0.070)],
    "eta_h1_p": [(0.126, 0.057), (0.141, 0.052), (0.131, 0.055)],
    "eta_c_w2": [(-0.050, 0.077), (-0.072, 0.090), (-0.049, 0.074)],
    "eta_h2_p": [(0.079, 0.121), (0.114, 0.140), (0.077, 0.116)],
    "eta_h1_w2": [(0.159, 0.071), (0.160, 0.068), (0.166, 0.068)],
    "eta_h2_w1": [(0.325, 0.140), (0.325, 0.138), (0.339, 0.136)],
    "beta": [None, None, (-0.137, 0.270)],
}
PUB_T5 = [("ch_f_h1u1", "Frisch: male labor supply", 0.58, 0.16), ("ch_f_h2u2", "Frisch: female labor supply", 0.88, 0.23),
          ("ch_f_h1u2", "Frisch: male labor supply / female wage", 0.11, 0.06),
          ("ch_f_h2u1", "Frisch: female labor supply / male wage", 0.17, 0.11),
          ("ch_f_cu1", "Frisch: consumption / male wage", -0.14, 0.07),
          ("ch_f_cu2", "Frisch: consumption / female wage", -0.04, 0.07),
          ("ch_m_h1v1", "Marshallian: male labor supply", -0.08, 0.08),
          ("ch_m_h2v2", "Marshallian: female labor supply", 0.42, 0.08),
          ("ch_m_h1v2", "Marshallian: male labor supply / female wage", -0.22, 0.04),
          ("ch_m_h2v1", "Marshallian: female labor supply / male wage", -0.75, 0.14),
          ("ch_m_cv1", "Marshallian: consumption / male wage", 0.32, 0.05),
          ("ch_m_cv2", "Marshallian: consumption / female wage", 0.19, 0.03)]
PUB_CHAIN = [("ch_c0", "Fixed labor supply, no taxes, no savings (= 10 E[s])", 7.1),
             ("ch_c1", "+ progressive taxes and transfers", 6.3), ("ch_c2", "+ husband's labor supply", 5.8),
             ("ch_c3", "+ wife's labor supply (household earnings)", 3.9), ("ch_c4", "+ savings (consumption)", 3.2),
             ("ch_gov", "Share: government", 0.20), ("ch_fam", "Share: family labor supply", 0.63),
             ("ch_sav", "Share: savings", 0.17),
             ("ch_f0", "Food-Stamp eligible: fixed labor supply", 7.2), ("ch_f1", "FS: + taxes and transfers", 3.6),
             ("ch_f3", "FS: + wife's labor supply", 2.3), ("ch_f4", "FS: + savings", 2.1),
             ("ch_fgov", "FS: share government", 0.71)]


def rec(table, spec, param, v, se=np.nan, p=np.nan, se_type="", nreps=0, published=np.nan, pub_se=np.nan, note=""):
    ROWS.append(dict(table=table, spec=spec, parameter=param, value=v, se=se, p=p, stars=stars(p), se_type=se_type,
                     nreps=nreps, published=published, published_se=pub_se, note=note))


def step0():
    md = []
    g10, g9, gb = load_est("base", "gmm10"), load_est("base", "gmm9"), load_est("base", "beta")
    rb, rbb = load_reps("base", "bs"), load_reps("base", "bsbeta")
    nb = 0 if rb is None else len(rb)
    # Table 3
    md += ["### Table S0.1. Wage-process estimates (BPS Table 3): published vs replicated", "",
           "Each cell: estimate (GMM s.e. clustered by household; p). Replicated from BPS's own code and data "
           "(T4C11 = age-varying variances, T4C41 = 'all ages' stationary model).", "",
           "| Parameter | | 30-37 | 38-42 | 43-47 | 48-52 | 53-57 | All ages |", "|---|---|---|---|---|---|---|---|"]
    for k, lab in T3LAB.items():
        pub = PUB_T3[k]
        rp = []
        for a in range(1, 6):
            v, se = g10.loc[f"{k}_{a}", "value"], g10.loc[f"{k}_{a}", "se"]
            rp.append((v, se))
            rec("S0_T3", "base", f"{k}_age{a}", v, se, pval(v, se), "GMM", 0, pub[a - 1][0], pub[a - 1][1])
        v, se = g9.loc[f"{k}_1", "value"], g9.loc[f"{k}_1", "se"]
        rp.append((v, se))
        rec("S0_T3", "base", f"{k}_all", v, se, pval(v, se), "GMM", 0, pub[5][0], pub[5][1])
        md.append(f"| {lab} | published | " + " | ".join(fmt(b, s, pval(b, s), 4) for b, s in pub) + " |")
        md.append("| | replicated | " + " | ".join(fmt(b, s, pval(b, s), 4) for b, s in rp) + " |")
    md += ["", f"N (husband wage-growth moments) = {int(g10.loc['observations', 'value']):,} (published 7,295).", ""]
    # Table 4
    md += ["### Table S0.2. Preference parameters (BPS Table 4, cols. 1, 4, 5): published vs replicated", "",
           f"Replicated s.e.: block bootstrap (BPS's bootstrap.do, {nb} successful replications for col. 1, "
           f"{0 if rbb is None else len(rbb)} for col. 5; BPS used 200), with the second-step GMM s.e. (not corrected for "
           "the first step) after 'GMM'; a dagger marks cells where only the GMM s.e. is available (col. 4).", "",
           "| Parameter | Col. 1 published | Col. 1 replicated | Col. 4 published | Col. 4 replicated | Col. 5 published | Col. 5 replicated |",
           "|---|---|---|---|---|---|---|"]
    for k, pubs in PUB_T4.items():
        cells = []
        for j, (est, reps) in enumerate(((g10, rb), (g9, None), (gb, rbb))):
            pub = pubs[j]
            cells.append(fmt(pub[0], pub[1], pval(*pub)) if pub else "-")
            if k not in est.index or (k == "beta" and j < 2):
                cells.append("-")
                continue
            v = est.loc[k, "value"]
            sb, n = bs_se(reps, k)
            sg = est.loc[k, "se"] if np.isfinite(est.loc[k, "se"]) else np.nan
            se = sb if np.isfinite(sb) else sg
            c = fmt(v, se, pval(v, se), dagger=not np.isfinite(sb))
            if np.isfinite(sb) and np.isfinite(sg):
                c = c[:-1] + f"; GMM {sg:.3f})"
            cells.append(c)
            rec("S0_T4", "base", f"{k}_col{[1, 4, 5][j]}", v, se, pval(v, se),
                "bootstrap" if np.isfinite(sb) else "GMM2", n, pub[0] if pub else np.nan, pub[1] if pub else np.nan)
        md.append(f"| {k} | " + " | ".join(cells) + " |")
    md += ["", "N = 7,295 in all three columns (published 7,295).", ""]
    # Table 5
    md += ["### Table S0.3. Frisch and Marshallian elasticities (BPS Table 5, col. 1, before-tax wage change)", "",
           "| Elasticity | Published | Replicated (bootstrap s.e.) |", "|---|---|---|"]
    for k, lab, pb, ps in PUB_T5:
        v = g10.loc[k, "value"]
        se, n = bs_se(rb, k)
        md.append(f"| {lab} | {fmt(pb, ps, pval(pb, ps), 2)} | {fmt(v, se, pval(v, se), 2)} |")
        rec("S0_T5", "base", k, v, se, pval(v, se), "bootstrap", n, pb, ps)
    md += [""]
    md += ["### Table S0.4. Insurance accounting (BPS p. 425-426): response of consumption to a 10% permanent fall in "
           "the husband's wage, percent", "",
           "| Step | Published | Replicated (bootstrap s.e.) |", "|---|---|---|"]
    for k, lab, pb in PUB_CHAIN:
        v = g10.loc[k, "value"]
        se, n = bs_se(rb, k)
        d = 3 if "share" in lab.lower() else 2
        md.append(f"| {lab} | {pb} | {fmt(v, se, pval(v, se), d)} |")
        rec("S0_chain", "base", k, v, se, pval(v, se), "bootstrap", n, pb)
    md += ["", "BPS's 20 / 63 / 17 split is stated in rounded percentage points of a 39 p.p. total (8 / 25 / 7 p.p.); "
           "the replicated unrounded chain gives 7.6 / 24.5 / 7.2 p.p. of 39.3 p.p.", ""]
    return md


SPEC1 = [("base", "BPS baseline"), ("base_noimm", "baseline without 1997 immigrants (fn. 15)"), ("a_nowork", "(a) year-level no-work drop"), ("b_nostatus", "(b) no status controls"),
         ("c_notrim", "(c) both trims off"), ("c1_nojump", "(c) jump trim off"), ("c2_nominw", "(c) min-wage trim off"),
         ("d_seo", "(d) SEO in"), ("d_seo_w", "(d) SEO in, weighted"), ("d_base_w", "(d) no SEO, weighted"),
         ("d_white", "(d) White, SEO in"), ("d_black", "(d) Black, SEO in"), ("d_white_noseo", "(d) White, no SEO"),
         ("e_brk", "(e) break on spouse identity"), ("f_noseo", "(f) a+b+c+e, no SEO"), ("f_all", "(f) all, SEO in"),
         ("f_all_w", "(f) all, SEO in, weighted")]


def step1(specs=SPEC1, table="S1", title=""):
    vals = {s: spec_values(s) for s, _ in specs if (W / s / "est_gmm10.csv").exists()}
    cols = [(s, l) for s, l in specs if s in vals]
    md = [title, "", "| Parameter | " + " | ".join(l for _, l in cols) + " |", "|---" * (len(cols) + 1) + "|"]
    for key, lab, src, d in PARAMS:
        cells = []
        for s, _ in cols:
            v, se, p, st, nr = vals[s][key]
            rec(table, s, key, v, se, p, st, nr)
            if key in ("observations", "n_rows"):
                cells.append(f"{int(v):,}" if np.isfinite(v) else "n/a")
            elif src == "g9c" or not np.isfinite(se):
                cells.append(f"{v:.{d}f}" if np.isfinite(v) else ("n.c." if st == "not converged" else "n/a"))
            else:
                cells.append(fmt(v, se, p, d, dagger=(st == "GMM2")))
        md.append(f"| {lab} | " + " | ".join(cells) + " |")
    nb = {s: (len(load_reps(s, "bs")) if load_reps(s, "bs") is not None else 0) for s, _ in cols}
    md.append("| Bootstrap replications (preference / beta) | " + " | ".join(
        f"{nb[s]} / {len(load_reps(s, 'bsbeta')) if load_reps(s, 'bsbeta') is not None else 0}" for s, _ in cols) + " |")
    return md, vals


EV_OUT = [("uc", "Consumption residual"), ("uy", "Husband earnings residual"), ("uyw", "Wife earnings residual"),
          ("uww", "Wife wage residual"), ("uw", "Husband wage residual"), ("dpart", "Wife participation change"),
          ("arc_yw", "Wife earnings arc change (zeros in)"), ("dlogc_raw", "Consumption log change (raw)")]
EV_TERM = [("ho_n", "k=-1 husband only"), ("wo_n", "k=-1 wife only"), ("jt_n", "k=-1 joint"),
           ("ho", "k=0 husband only"), ("wo", "k=0 wife only"), ("jt", "k=0 joint"),
           ("ho_p", "k=+1 husband only"), ("wo_p", "k=+1 wife only"), ("jt_p", "k=+1 joint"),
           ("jt-ho", "k=0 joint minus husband only"), ("jt_p-ho_p", "k=+1 joint minus husband only")]


def cellf(y, d=3, n=True):
    c = fmt(y["b"], y["se"], y["p"], d)
    if n and np.isfinite(y["nev"]):
        c += f" [{int(y['nev'])}]"
    return c


def step2():
    md = []
    f = W / "step2_results.csv"
    if not f.exists():
        return md
    r = pd.read_csv(f)
    for c in ("b", "se", "p", "N", "nev"):
        r[c] = pd.to_numeric(r[c], errors="coerce")
    for _, x in r.iterrows():
        rec(f"S2_{x['block']}", x["spec"], f"{x['outcome']}|{x['term']}", x["b"], x["se"], x["p"], "cluster", 0,
            note=f"N={x['N']}; events={x['nev']}")
    # shares
    md += ["### Table S2.1. Couple-years with a displacement in BPS's panel", "",
           "Share of BPS couple-years (head in IGE's PSID person file: BPS's rows less the 1997 immigrant refresher) "
           "whose two-year interval (calendar years t-1, t) contains a displacement (closure or layoff, own report). "
           "Cell: share [events].", ""]
    for sp in r["spec"].unique():
        x = r[(r["spec"] == sp) & (r["block"] == "share")]
        if x.empty:
            continue
        md += [f"Sample: {sp}", "", "| Rows | Husband displaced | Wife displaced | Joint (same interval) | "
               "Joint (same year) | Husband: closure | Wife: closure | Wife: any job end | N |",
               "|---|---|---|---|---|---|---|---|---|"]
        for o, lab in (("all_rows", "all rows"), ("rows_duw", "rows with husband wage difference"),
                       ("rows_duw_duww", "rows with both wage differences")):
            y = x[x["outcome"] == o].set_index("term")
            cells = [f"{y.loc[t, 'b']:.4f} [{int(y.loc[t, 'nev'])}]" for t in ("hd", "wd", "jd", "jd_sy", "hs", "ws", "wa")]
            md.append(f"| {lab} | " + " | ".join(cells) + f" | {int(y.loc['hd', 'N']):,} |")
        y = x[x["outcome"] == "cond"].set_index("term")
        md += ["", "Wife displaced in the same interval: " + "; ".join(
            f"{t} = {y.loc[t, 'b']:.4f} (N={int(y.loc[t, 'N'])}, events={int(y.loc[t, 'nev'])})" for t in y.index), ""]
    # event studies
    md += ["### Table S2.3. BPS residuals around single and joint displacements (biennial event study)", "",
           "One regression per column: residual (or raw change) of the two-year difference on indicators of a "
           "displacement in the interval after it (k=-1), in it (k=0) and in the interval before it (k=+1), separately "
           "for husband only, wife only and joint. Reference: couple-years with no displacement in these intervals. "
           "S.e. clustered by household. Cell: coefficient (s.e.; p) [couple-years with the event in the regression].", ""]
    for sp in r["spec"].unique():
        x = r[(r["spec"] == sp) & (r["block"] == "event")]
        if x.empty:
            continue
        outs = [o for o in EV_OUT if o[0] in set(x["outcome"])]
        md += [f"Sample: {sp}", "", "| | " + " | ".join(l for _, l in outs) + " |", "|---" * (len(outs) + 1) + "|"]
        for t, lab in EV_TERM:
            cells = []
            for o, _ in outs:
                y = x[(x["outcome"] == o) & (x["term"] == t)]
                cells.append(cellf(y.iloc[0]) if not y.empty else "")
            md.append(f"| {lab} | " + " | ".join(cells) + " |")
        md.append("| N | " + " | ".join(f"{int(x[x['outcome'] == o]['N'].iloc[0]):,}" for o, _ in outs) + " |")
        md.append("")
    # moments
    x = r[r["block"] == "moment"]
    if not x.empty:
        md += ["### Table S2.5. Cross-spouse residual moments with and without displacement couple-years", "",
               "Mean of the product of BPS residuals (s.e. clustered by household): m_ww = E(du_w1 du_w2) "
               "(contemporaneous wage growth = 2 sigma_u1u2 + 2 sigma_v1v2 in BPS's model), m_wwlag = average of "
               "E(du_w1 du_w2,t-2) and E(du_w1,t-2 du_w2) (= -sigma_u1u2), m_yy = E(du_y1 du_y2) (earnings), "
               "m_cy = E(du_c du_y1); shift_x = change in the mean product in couple-years with displacement x "
               "(regression on hd, wd, jd).", "",
               "| Sample | Moment | All | Without displacement years | Without joint years | shift: husband displaced | "
               "shift: wife displaced | shift: joint (extra) |", "|---|---|---|---|---|---|---|---|"]
        for sp in x["spec"].unique():
            for m in ("m_ww", "m_wwlag", "m_yy", "m_cy"):
                y = x[(x["spec"] == sp) & (x["outcome"] == m)].set_index("term")
                if y.empty:
                    continue
                cells = []
                for t in ("all", "no_disp", "no_joint", "shift_hd", "shift_wd", "shift_jd"):
                    c = fmt(y.loc[t, "b"], y.loc[t, "se"], y.loc[t, "p"], 4)
                    if t in ("all", "no_disp", "no_joint"):
                        c += f" [N={int(y.loc[t, 'N']):,}]"
                    cells.append(c)
                md.append(f"| {sp} | {m} | " + " | ".join(cells) + " |")
        md.append("")
    # Table 7 split
    x = r[r["block"] == "t7"]
    if not x.empty:
        md += ["### Table S2.6. BPS Table 7 (added worker, extensive margin) split into entries and exits", "",
               "IV regressions as in tables_7_8_9.do: dependent variable = change in the wife's participation (net), "
               "entry (0 -> 1) or minus exit (1 -> 0), so that net = entries + (minus exits); husband's wage growth "
               "instrumented with long-run wage growth (theta_1, permanent) or future wage growth (theta_0, "
               "transitory). Published (BPS sample): theta_1 = -0.168* (0.087), N = 3,143; theta_0 = 0.002 (0.030), "
               "N = 4,941. S.e. clustered by household; p from the normal. [N; couple-years with a nonzero outcome]", ""]
        for sp in x["spec"].unique():
            y = x[x["spec"] == sp]
            md += [f"Sample: {sp}", "", "| | Net change in participation | Entries | Minus exits |", "|---|---|---|---|"]
            for t, lab in (("theta_perm", "theta_1: permanent shock to husband's wage"),
                           ("theta_tran", "theta_0: transitory shock to husband's wage")):
                cells = []
                for o in ("dpart", "entry", "exitn"):
                    z = y[(y["outcome"] == o) & (y["term"] == t)]
                    if z.empty:
                        cells.append("")
                        continue
                    z = z.iloc[0]
                    cells.append(fmt(z["b"], z["se"], z["p"], 3) + f" [N={int(z['N']):,}; nonzero={int(z['nev']):,}]")
                md.append(f"| {lab} | " + " | ".join(cells) + " |")
            md.append("")
        x = r[r["block"] == "t7ctl"]
        for sp in x["spec"].unique():
            y = x[x["spec"] == sp]
            md += [f"theta_1 with the couple-year's displacement indicators as controls (head in IGE person file), "
                   f"sample {sp}:", "", "| | Net | Entries | Minus exits |", "|---|---|---|---|"]
            for t in ("duw", "hd", "wd", "jd"):
                cells = []
                for o in ("dpart", "entry", "exitn"):
                    z = y[(y["outcome"] == o) & (y["term"] == t)]
                    cells.append(fmt(z["b"].iloc[0], z["se"].iloc[0], z["p"].iloc[0], 3) if not z.empty else "")
                md.append(f"| {t} | " + " | ".join(cells) + " |")
            md.append("| N | " + " | ".join(f"{int(y[y['outcome'] == o]['N'].iloc[0]):,}"
                                           for o in ("dpart", "entry", "exitn")) + " |")
            md.append("")
    return md


def attrition_md():
    md = []
    f = W / "attrition.csv"
    if f.exists():
        a = pd.read_csv(f)
        for _, x in a.iterrows():
            for v in ("rows", "hd", "wd", "jd", "anyd", "hs", "ws", "jd_cpl", "hd_cpl"):
                rec("S2_attrition", "base", f"step{int(x['step'])}|{v}", x[v], note=x["label"])
        md += ["### Table S2.2. Which of BPS's restrictions drop the displaced couple-years", "",
               "Universe: married couples, husband 30-57 (age - 1), head in IGE's PSID person file (SRC + SEO), "
               "PSID 1999-2009 waves (income years 1998-2008). BPS's restrictions applied in their order "
               "(psid_sample.do, prepare_bootstrap.do); each row = couple-years still in the sample after the step. "
               "hd / wd / jd = husband / wife / joint displacement in the couple-year's interval.", "",
               "| Step | Rows | Husband displaced | Wife displaced | Joint | Either | Husband closure | Wife closure | "
               "Joint: couples | Husband displaced: men |", "|---|---|---|---|---|---|---|---|---|---|"]
        for _, x in a.iterrows():
            cells = [f"{int(x[v]):,}" if np.isfinite(x[v]) else "" for v in
                     ("rows", "hd", "wd", "jd", "anyd", "hs", "ws", "jd_cpl", "hd_cpl")]
            md.append(f"| {int(x['step'])}. {x['label']} | " + " | ".join(cells) + " |")
        md.append("")
    f = W / "attrition_duw.csv"
    if f.exists():
        a = pd.read_csv(f)
        reasons = list(a["reason"].unique())
        md += ["Why rows in data4estimation have no husband wage-growth moment (head in IGE person file):", "",
               "| Group | " + " | ".join(reasons) + " |", "|---" * (1 + len(reasons)) + "|"]
        for g in a["grp"].unique():
            y = a[a["grp"] == g].set_index("reason")["n"]
            md.append(f"| {g} | " + " | ".join(f"{int(y[k]):,}" for k in reasons) + " |")
            for k in reasons:
                rec("S2_attrition_duw", "base", f"{g}|{k}", y[k])
        md.append("")
    f = W / "separation.csv"
    if f.exists():
        a = pd.read_csv(f)
        for _, x in a.iterrows():
            rec("S1e_separation", x["sample"], f"{x['outcome']}|{x['group']}", x.get("mean"), x.get("se"), x.get("p"),
                note=f"n={x.get('n')}; events={x.get('events')}")
        md += ["### Table S1e. Couples lost to separation at BPS's composition break", "",
               "Married couples (husband 30-57, head in IGE person file, income years 1998-2006 so that the next wave "
               "exists). sep_obs = at the head's next interview the marriage has ended or the wife is another person "
               "(heads observed again); bps_break_next = the next interview carries fchg > 1 (BPS drop that year and "
               "restart the household). Cell: share [events / couple-years]; differences = linear probability, s.e. "
               "clustered by head.", "",
               "| Sample | Outcome | No displacement | Husband only | Wife only | Joint | Husband only - none | "
               "Wife only - none | Joint - none |", "|---|---|---|---|---|---|---|---|---|"]
        sub = a[a["outcome"].isin(["sep_obs", "bps_break_next"])]
        for (samp, out), y in sub.groupby(["sample", "outcome"], sort=False):
            y = y.set_index("group")
            cells = [f"{y.loc[g, 'mean']:.4f} [{int(y.loc[g, 'events'])}/{int(y.loc[g, 'n']):,}]"
                     for g in ("none", "h_only", "w_only", "joint")]
            cells += [fmt(y.loc[g, "mean"], y.loc[g, "se"], y.loc[g, "p"], 4)
                      for g in ("diff h_only-none", "diff w_only-none", "diff joint-none")]
            md.append(f"| {samp} | {out} | " + " | ".join(cells) + " |")
        y = a[~a["outcome"].isin(["sep_obs", "bps_break_next"])]
        md += ["", "Counts: " + "; ".join(f"{x['sample']}: {x['outcome']} ({x['group']}) = {int(x['n']):,}"
                                          for _, x in y.iterrows()), ""]
    return md


def main():
    (OUTDIR / "tables").mkdir(exist_ok=True)
    md0 = step0()
    md1, _ = step1(title="### Table S1. Relaxing BPS's restrictions one at a time and together (PSID 1999-2009)")
    (OUTDIR / "tables" / "step0.md").write_text("\n".join(md0), encoding="utf-8")
    (OUTDIR / "tables" / "step1.md").write_text("\n".join(md1), encoding="utf-8")
    md2, _ = step1([("base", "BPS baseline"), ("base_dx", "baseline, no displacement years"),
                    ("base_jx", "baseline, no joint-displacement years"), ("b_nostatus", "(b) no status controls"),
                    ("b_dx", "(b), no displacement years"), ("f_all", "(f) all relaxations"),
                    ("f_all_dx", "(f), no displacement years")], table="S2cov",
                   title="### Table S2.4. Wage-shock covariances and preference estimates with and without "
                         "displacement couple-years")
    (OUTDIR / "tables" / "step2_cov.md").write_text("\n".join(md2), encoding="utf-8")
    md3 = step2()
    md4 = attrition_md()
    (OUTDIR / "tables" / "step2.md").write_text("\n".join(md3), encoding="utf-8")
    (OUTDIR / "tables" / "attrition.md").write_text("\n".join(md4), encoding="utf-8")
    pd.DataFrame(ROWS).to_csv(OUTDIR / "bps_reconciliation.csv", index=False)
    print("\n".join(md0 + [""] + md1 + [""] + md2))


if __name__ == "__main__":
    main()
