r"""Checks that could kill the CPS joint job-loss headline (2026-10-17). [Paper A; referee review items 1, 2, 4, 7]

Headline (30.CPSJointJobLoss.py; EVIDENCE 3.24): married couples, both employed at t, CPS basic monthly 1994-2023; the
wife's probability of becoming a job loser at t+1 is 0.0545 when her husband becomes one at t+1 vs 0.0054 when he stays
employed; LPM with state x year-month FE +0.040***. The referee review (proposals/fable_review_paperA.md, Sec. 3.2 and
plan items 1, 2, 7) lists the alternatives that could produce this without a joint shock to both jobs. This script runs
them, reusing the couples panel, the definitions and the estimator of script 30 (imported read-only).

DATA
  The cached panel of 30 (IGE/data/cps_couples_panel.pkl) and, new here, PUSLFPRX (labor-force information given by
  1 self, 2 proxy, 3 both) and HURESPLI (line number of the household respondent) for every married person aged 20-62,
  requested from the Census API with 30's own request function (fetch(): same predicate PEMARITL=1 & PRTAGE=20:62, same
  retries; the key is read from the environment and never printed or saved) and stored unchanged as
  IGE/data/ext/cps_couples_proxy/cpl_YYYY_MM.csv.gz (git-ignored; the raw files of 30 are not touched). A couple's
  reporting status is matched to the panel by the couple key of 30 (household id + both line numbers + month).
CHECKS (every regression: LPM, state x year-month FE of the base month t, s.e. clustered by household [and by state])
  1. Proxy reporting: same-month excess (a) all, (b) both spouses self-report, (c) wife self-reports and the husband is
     reported by proxy, (d) the reverse; reporting status in the month of the job loss (t+1); also with status at t and
     t+1 both, and with the wife (husband) as the household respondent.
  2. Temporary layoffs, seasonality, duration, class of worker: excess (i) for husbands' job losses other than "on layoff"
     (PRUNTYPE 2-3) and with the wife's outcome excluding PRUNTYPE 1; (ii) excluding job-loss months June-September;
     (iii) by the husband's major industry (harmonised across the 2003 recode); (iv) persistent job loss (still
     unemployed at t+2) for him and for her; (v) by both spouses' class of worker; (vi) every row also excluding
     2020-21.
  3. Same-employer bound: with a share s of couples at the same establishment (Hyatt 2019: 10-12% of dual-earner couples)
     whose wives lose their job with probability p when the husband does, and all other wives at the base rate p0, the
     excess is s (p - p0); the p that reproduces the estimated excess; and the tightest CPS proxy for a shared employer
     (same detailed industry x same detailed occupation x same class of worker).
  4. Selection: couples observed (linked, still naming each other) in all four months of the rotation.
  5. Figure 1 for the paper: the wife's excess monthly job-loss hazard in months tau-3..tau+3 around the husband's
     job-loss month tau. tau-2..tau+2 are the flow events of 30 (employed in the previous month, job loser now). The CPS
     rotation spans 4 consecutive months, so at tau-3 (tau+3) the previous month of the wife (husband) falls outside the
     rotation; there that spouse's job loss is identified as a job loser with unemployment duration <= DUR_MAX weeks
     (risk set: employed or such a new job loser), marked with open symbols.
Outputs: IGE/output/cps_joint_loss_checks.md / .csv; IGE/paperA_joint_loss/fig_cps_monthly_hazard.pdf / .png and
fig_cps_monthly_hazard_awe.png.
Associations, not causal effects. Run from IGE/ with `python -I 37.CPSJointLossChecks.py` (raw files are data only).
"""
import gzip
import importlib.util
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import numpy as np                            # noqa: E402
import pandas as pd                           # noqa: E402

from common import DATA, OUT, stars           # noqa: E402


def _load30():
    spec = importlib.util.spec_from_file_location("cps30", HERE / "30.CPSJointJobLoss.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


m30 = _load30()
PRX = DATA / "ext" / "cps_couples_proxy"
PAPER = HERE / "paperA_joint_loss"


# ================================================================ 1. download (30's fetch, other variables / folder)
def prx_vars(y, m):
    ids = "HRHHID,HRHHID2" if (y, m) >= (2004, 5) else "HRHHID,HRSAMPLE,HRSERSUF,HUHHNUM"
    v = f"{ids},HRMIS,PULINENO,GESTFIPS,PESPOUSE,PESEX,PUSLFPRX,HURESPLI".split(",")
    return v, v


def download(workers=4):
    """Re-uses m30.fetch (safe: key from the environment, URL and exception text never printed) with this script's
    variable list and folder; kind 'cpl' keeps 30's predicate (PEMARITL=1, PRTAGE 20-62)."""
    PRX.mkdir(parents=True, exist_ok=True)
    m30.RAW, m30.req_vars = PRX, prx_vars
    jobs = [(y, m) for y in m30.YEARS for m in range(1, 13)]
    with ThreadPoolExecutor(workers) as ex:
        for (y, m), r in zip(jobs, ex.map(lambda a: m30.fetch(a[0], a[1], "cpl"), jobs)):
            if r != "cached":
                print(y, m, r, flush=True)


# ================================================================ 2. reporting status per couple-month
PRX_CACHE = DATA / "cps_couples_proxy.pkl"


def prx_month(y, m):
    f = PRX / f"cpl_{y}_{m:02d}.csv.gz"
    if not f.exists():
        return None
    d = pd.read_csv(f, dtype=str, keep_default_na=False)
    p = pd.DataFrame({"hkey": m30._idkey(d), "line": m30._num(d, "PULINENO"), "sp": m30._num(d, "PESPOUSE"),
                      "sex": m30._num(d, "PESEX"), "prx": m30._num(d, "PUSLFPRX"), "resp": m30._num(d, "HURESPLI")})
    p = p[p.sp > 0]
    c = p[p.sex == 1].merge(p[p.sex == 2], left_on=["hkey", "sp"], right_on=["hkey", "line"], suffixes=("_h", "_w"))
    c = c[c.sp_w == c.line_h]
    c = c.drop_duplicates(["hkey", "line_h"], keep=False).drop_duplicates(["hkey", "line_w"], keep=False)
    return pd.DataFrame({
        "cid": m30._hash(c.hkey + "|" + c.line_h.astype(str) + "|" + c.line_w.astype(str)),
        "t": np.int16((y - 1994) * 12 + m - 1),
        "h_prx": c.prx_h.clip(-1, 3).astype("int8").values, "w_prx": c.prx_w.clip(-1, 3).astype("int8").values,
        "resp_h": (c.resp_h == c.line_h).astype("int8").values, "resp_w": (c.resp_h == c.line_w).astype("int8").values})


def build_prx():
    if PRX_CACHE.exists():
        return pd.read_pickle(PRX_CACHE)
    parts = [r for y in m30.YEARS for m in range(1, 13) if (r := prx_month(y, m)) is not None]
    R = pd.concat(parts, ignore_index=True).drop_duplicates(["cid", "t"], keep=False)
    R.to_pickle(PRX_CACHE)
    return R


# ================================================================ 3. helpers
ROWS = []
lpm, pval, wmean, cellr = m30.lpm, m30.pval, m30.wmean, m30.cellr
DUR_MAX = 4                                   # weeks: "new" job loser when the previous month is outside the rotation

# harmonised major industry of the main job (1994-2002: 22 groups; 2003-: 14 groups)
IND_OLD = {1: 1, 2: 1, 21: 1, 3: 2, 4: 3, 5: 3, 9: 4, 10: 4, 6: 5, 7: 5, 8: 5, 11: 6, 13: 7, 20: 7, 16: 8, 17: 8,
           18: 8, 19: 8, 12: 9, 14: 9, 15: 9, 22: 10}
IND_NEW = {1: 1, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 5, 8: 6, 9: 7, 10: 8, 11: 9, 12: 9, 13: 10}
IND_LAB = {1: "Agriculture, forestry, fishing, mining", 2: "Construction", 3: "Manufacturing",
           4: "Wholesale and retail trade", 5: "Transport, utilities, communications / information",
           6: "Finance, insurance, real estate", 7: "Business, repair and professional services",
           8: "Education, health and social services", 9: "Leisure, personal and other services (incl. private hh)",
           10: "Public administration"}


def harm_ind(ind, year):
    old = pd.Series(np.asarray(ind)).map(IND_OLD).fillna(0).to_numpy()
    new = pd.Series(np.asarray(ind)).map(IND_NEW).fillna(0).to_numpy()
    return np.where(np.asarray(year) < 2003, old, new).astype("int8")


def cowg(c):
    c = np.asarray(c)
    return np.select([np.isin(c, [4, 5]), np.isin(c, [1, 2, 3]), np.isin(c, [6, 7])], [1, 2, 3], 0).astype("int8")


def rec(table, sample, outcome, r, x="H", cells=None, spec="state x ym FE"):
    se = r["se_hh"][x]
    ROWS.append(dict(table=table, sample=sample, outcome=outcome, spec=spec, regressor=x, coef=r["b"][x], se_hh=se,
                     p_hh=pval(r["b"][x], se), se_state=r["se_state"][x], p_state=pval(r["b"][x], r["se_state"][x]),
                     n=r["N"], clusters_hh=r["G_hh"], clusters_state=r["G_state"], n_fe=r["nfe"], **(cells or {})))


def cells(d, y):
    a, b = d[d.H == 0], d[d.H == 1]
    return dict(p0=wmean(a[y], a.w), p1=wmean(b[y], b.w), n1=len(b), n11=int(b[y].sum()))


def table(md, tab, cols, panels, min_h=20, fe=("sm",)):
    """cols: [(header, frame, outcome)]; panels: [(name, fn(frame) -> mask)]. One regression per cell."""
    md.append("| | " + " | ".join(f"({i + 1}) {h}" for i, (h, _, _) in enumerate(cols)) + " |")
    md.append("|---" * (len(cols) + 1) + "|")
    out = {}
    for pn, f in panels:
        cl, mn, nn = [], [], []
        for h, d, y in cols:
            dd = d[np.asarray(f(d), bool)]
            if dd.H.sum() < min_h or (dd.H == 0).sum() < min_h or dd.loc[dd.H == 1, y].sum() == 0:
                cl.append("n/a"), mn.append(""), nn.append(f"{len(dd):,} / {int(dd.H.sum()):,}")
                continue
            r = lpm(dd, y, ["H"], fe=list(fe))
            c = cells(dd, y)
            rec(tab, pn, h, r, cells=c)
            out[(pn, h)] = (r, c)
            cl.append(cellr(r, "H"))
            mn.append(f"{c['p0']:.4f} / {c['p1']:.4f}")
            nn.append(f"{r['N']:,} / {c['n1']:,}")
        md.append(f"| **{pn}** |" + " |" * len(cols))
        md.append("| Husband becomes job loser (t+1) | " + " | ".join(cl) + " |")
        md.append("| Mean H = 0 / H = 1 (weighted) | " + " | ".join(mn) + " |")
        md.append("| N / N(H = 1) | " + " | ".join(nn) + " |")
    md.append("| Fixed effects | " + " | ".join("state x year-month" for _ in cols) + " |")
    md.append("| Clusters | " + " | ".join("household [state]" for _ in cols) + " |\n")
    return out


def shift(P, cols, k):
    """Values of `cols` at t+k for the same couple (used only where the panel's own link to t+k exists)."""
    L = P[["cid", "t"] + cols].copy()
    L["t"] = (L.t - k).astype("int16")
    L.columns = ["cid", "t"] + [f"{c}{k:+d}" for c in cols]
    m = P[["cid", "t"]].merge(L, on=["cid", "t"], how="left")
    return {c: m[c].fillna(-1).to_numpy() for c in L.columns[2:]}




# ================================================================ 4. analysis
def main():
    OUT.mkdir(exist_ok=True)
    P = m30.add_vars(m30.build_panel())
    P.attrs = {}
    P["mo1"] = ((P.t + 1) % 12 + 1).astype("int8")                    # calendar month of t+1
    P["summer"] = P.mo1.between(6, 9).astype("int8")
    P["y2021"] = (P.year.between(2020, 2021) | ((P.t + 1) // 12 + 1994).between(2020, 2021)).astype("int8")
    P["hind"] = harm_ind(P.h_ind, P.year)
    P["h_cg"], P["w_cg"] = cowg(P.h_cow), cowg(P.w_cow)
    for k in (-2, -1):
        for c, v in shift(P, ["w_dur"], k).items():
            P[c] = v.astype("int16")
    R = build_prx()
    for k in (0, 1):
        L = R.copy()
        L["t"] = (L.t - k).astype("int16")
        L.columns = ["cid", "t"] + [f"{c}_{k}" for c in R.columns[2:]]
        P = P.merge(L, on=["cid", "t"], how="left")
        for c in L.columns[2:]:
            P[c] = P[c].fillna(-9).astype("int8")
    nonc = lambda d: d.y2021 == 0                                       # noqa: E731
    allr = lambda d: np.ones(len(d), bool)                              # noqa: E731

    W0 = m30.jl_sample(P, 0)
    W0["y"] = (W0["w_s+1"] == 2).astype("int8")
    md = ["# Checks of the CPS joint job-loss headline\n",
          "Built by `IGE/37.CPSJointLossChecks.py` (2026-10-17; definitions in its docstring), on the couples panel and "
          "definitions of `30.CPSJointJobLoss.py`, answering the referee review `proposals/fable_review_paperA.md` (Sec. "
          "3.2; plan items 1, 2, 4, 7). Sample unless stated: both spouses employed at t; H = 1 if the husband becomes a "
          "job loser at t+1 (unemployed, reason job loser on layoff / other job loser / temporary job ended), H = 0 if "
          "he stays employed; outcome: the wife becomes a job loser at t+1. Each cell is a separate LPM of the outcome "
          "in the column header on H with state x year-month FE (base month t): coefficient*** (s.e. clustered by "
          "household; p) [s.e. clustered by state; p]; *** p<0.01, ** p<0.05, * p<0.1. Means weighted by the wife's "
          "composite weight. 'Excl. 2020-21' drops base or job-loss months in calendar 2020-2021. Row panels are "
          "samples. Associations, not causal effects.\n"]
    base = lpm(W0, "y", ["H"], fe=["sm"])
    c0 = cells(W0, "y")
    rec("0_headline", "all", "wife job loser t+1", base, cells=c0)
    EXC, P0 = base["b"]["H"], c0["p0"]
    md.append(f"Headline reproduced: P(wife job loser | husband job loser) {c0['p1']:.4f} vs {c0['p0']:.4f} "
              f"| husband employed; state x month FE {cellr(base, 'H')}; N {base['N']:,}, husband job losers "
              f"{c0['n1']:,}, joint events {c0['n11']:,}.\n")

    # ---------------- 1. proxy reporting
    md.append("## 1. Proxy reporting (PUSLFPRX: labor-force information given by self / proxy / both)\n")
    known = (W0.h_prx_1 > 0) & (W0.w_prx_1 > 0)
    kn = W0[known]
    md.append(f"Reporting status found for {known.mean():.3f} of the couple-months in the sample (status in the month of "
              f"the job loss, t+1; couple key of 30). Among them (unweighted): both self-report "
              f"{((kn.h_prx_1 == 1) & (kn.w_prx_1 == 1)).mean():.3f}; wife self, husband by proxy "
              f"{((kn.w_prx_1 == 1) & (kn.h_prx_1 == 2)).mean():.3f}; husband self, wife by proxy "
              f"{((kn.h_prx_1 == 1) & (kn.w_prx_1 == 2)).mean():.3f}; both by proxy "
              f"{((kn.h_prx_1 == 2) & (kn.w_prx_1 == 2)).mean():.3f}; 'both self and proxy' (code 3) for either "
              f"{((kn.h_prx_1 == 3) | (kn.w_prx_1 == 3)).mean():.3f}. Wife self-reports, husband by proxy: the wife is "
              f"the household respondent in {(kn.resp_w_1[(kn.w_prx_1 == 1) & (kn.h_prx_1 == 2)] == 1).mean():.3f} of "
              "these couple-months. Status at t+1 can respond to the job loss itself (a man at home after losing his job "
              "is more likely to answer for himself), so panel B uses couples with the same status at t (before the "
              "event) and at t+1.\n")
    S = lambda h, w, k=1: (lambda d: (d[f"h_prx_{k}"] == h) & (d[f"w_prx_{k}"] == w))     # noqa: E731
    S2 = lambda h, w: (lambda d: S(h, w, 0)(d) & S(h, w, 1)(d))                           # noqa: E731
    W0n = W0[nonc(W0)]
    cols1 = [("wife job loser t+1", W0, "y"), ("wife job loser t+1, excl. 2020-21", W0n, "y")]
    pan1 = [("(a) All couples", allr),
            ("(a') Reporting status known for both at t+1", lambda d: (d.h_prx_1 > 0) & (d.w_prx_1 > 0)),
            ("A (b) Both spouses self-report (t+1)", S(1, 1)),
            ("A (c) Wife self-reports, husband by proxy (t+1)", S(2, 1)),
            ("A (c'') ... and the wife is the household respondent (she reports his job loss)",
             lambda d: S(2, 1)(d) & (d.resp_w_1 == 1)),
            ("A (d) Husband self-reports, wife by proxy (t+1)", S(1, 2)),
            ("A (d'') ... and the husband is the household respondent (he reports her job loss)",
             lambda d: S(1, 2)(d) & (d.resp_h_1 == 1)),
            ("A (e) Both by proxy (another member reports both, t+1)", S(2, 2)),
            ("A (f) One spouse reports both ((c) or (d); third-person reports excluded)",
             lambda d: S(2, 1)(d) | S(1, 2)(d)),
            ("B (b) Both self-report at t and t+1", S2(1, 1)),
            ("B (c) Wife self, husband proxy at t and t+1", S2(2, 1)),
            ("B (d) Husband self, wife proxy at t and t+1", S2(1, 2)),
            ("B (e) Both by proxy at t and t+1", S2(2, 2))]
    table(md, "1_proxy", cols1, pan1)
    md.append("**Differences between reporting groups** (pooled LPM on the two groups, state x month FE; regressors H, "
              "group, H x group)\n")
    md.append("| Comparison | H x group | H (reference group) | N |\n|---|---|---|---|")
    cr = lambda d: S(2, 1)(d) & (d.resp_w_1 == 1)                        # noqa: E731
    dr = lambda d: S(1, 2)(d) & (d.resp_h_1 == 1)                        # noqa: E731
    for lab, ga, gb in (("(c'') wife reports both (vs (d'') husband reports both), t+1", cr, dr),
                        ("(c) vs (d), same status at t and t+1", S2(2, 1), S2(1, 2)),
                        ("(e) third person reports both (vs (c) or (d)), t+1", S(2, 2),
                         lambda d: S(2, 1)(d) | S(1, 2)(d))):
        d = W0[ga(W0) | gb(W0)].assign(g=lambda x: ga(x).astype("int8"))
        d["Hg"] = d.H * d.g
        r = lpm(d, "y", ["H", "Hg", "g"], fe=["sm"])
        rec("1_proxy_diff", lab, "wife job loser t+1", r, "Hg")
        md.append(f"| {lab} | {cellr(r, 'Hg')} | {cellr(r, 'H')} | {r['N']:,} |")
    md.append("")
    md.append("The CPS takes one respondent per household and month, who answers for everyone else: couples in which "
              "both spouses self-report (b) are almost absent (cells n/a), so the review's sample (b) cannot be formed. "
              "The informative contrast is (c'') vs (d''): one spouse, the respondent, reports both statuses; if the "
              "joint loss were a reporting artefact of the respondent it should differ by who reports. Share of couple-"
              f"months with the husband reporting both (d''): {dr(W0[W0.H == 0]).mean():.3f} when he stays employed, "
              f"{dr(W0[W0.H == 1]).mean():.3f} when he becomes a job loser (a man at home is more often the "
              "respondent).\n")

    # ---------------- 2. temporary layoffs, seasonality, duration, class of worker
    md.append("## 2. Temporary layoffs, seasonality, duration, class of worker\n")
    W0["ynl"] = ((W0["w_s+1"] == 2) & W0["w_unt+1"].isin([2, 3])).astype("int8")
    W0nl = W0[~((W0["w_s+1"] == 2) & (W0["w_unt+1"] == 1))]                 # wives on layoff at t+1 dropped
    W1 = m30.jl_sample(P, 1)
    W1["y"] = (W1["w_s+1"] == 2).astype("int8")
    W1["yp"] = ((W1["w_s+1"] == 2) & W1["w_s+2"].isin([2, 3])).astype("int8")
    W1["ynl"] = ((W1["w_s+1"] == 2) & W1["w_unt+1"].isin([2, 3])).astype("int8")
    W1nl = W1[~((W1["w_s+1"] == 2) & (W1["w_unt+1"] == 1))]
    md.append("Columns: (1)-(2) wife becomes a job loser at t+1 (any reason code); (3)-(4) wife becomes a job loser other "
              "than on layoff (PRUNTYPE 2-3; wives on layoff at t+1 dropped); (5)-(6) wife becomes a job loser at t+1 "
              "and is still unemployed at t+2 (sample linked to t+2; husbands in the control group employed at t+1 and "
              "t+2). Row panels define the husband's event and the sample: 'other than on layoff' drops husbands whose "
              "job loss is PRUNTYPE 1; 'persistent' keeps husbands still unemployed at t+2 (t+2-linked sample in every "
              "column). Industry and class of worker refer to the main job at t; industry harmonised across the 2003 "
              "recode into 10 groups. Even columns exclude 2020-21 (item vi).\n")

    def cols2(dA, dNL, dP):
        return [("wife job loser", dA, "y"), ("wife job loser, excl. 2020-21", dA[nonc(dA)], "y"),
                ("wife job loser not on layoff", dNL, "ynl"),
                ("wife not on layoff, excl. 2020-21", dNL[nonc(dNL)], "ynl"),
                ("wife persistent job loser", dP, "yp"), ("wife persistent, excl. 2020-21", dP[nonc(dP)], "yp")]
    notlay = lambda d: (d.H == 0) | d["h_unt+1"].isin([2, 3])                # noqa: E731
    onlay = lambda d: (d.H == 0) | (d["h_unt+1"] == 1)                       # noqa: E731
    pers = lambda d: (d.H == 0) | d["h_s+2"].isin([2, 3])                     # noqa: E731
    pan2a = [("(0) All", allr), ("(i) His job loss other than on layoff (PRUNTYPE 2-3)", notlay),
             ("(i') His job loss on layoff (PRUNTYPE 1) only", onlay),
             ("(ii) Job-loss month (t+1) not June-September", lambda d: d.summer == 0),
             ("(i)+(ii) Not on layoff, not June-September", lambda d: notlay(d) & (d.summer == 0))]
    C2 = cols2(W0, W0nl, W1)
    table(md, "2_layoff_season", C2, pan2a)
    md.append("**(iv) Persistent job loss of the husband (still unemployed at t+2); t+2-linked sample in every "
              "column**\n")
    pan2b = [("(0) All, t+2-linked sample", allr), ("(iv) His job loss persistent", pers),
             ("(iv)+(i) Persistent and not on layoff", lambda d: pers(d) & notlay(d)),
             ("(iv)+(i)+(ii) Persistent, not on layoff, not June-September",
              lambda d: pers(d) & notlay(d) & (d.summer == 0))]
    table(md, "2_persistent", cols2(W1, W1nl, W1), pan2b)
    md.append("**(iii) By the husband's major industry at t (harmonised)**\n")
    pan2c = [(IND_LAB[g], (lambda g: lambda d: d.hind == g)(g)) for g in range(1, 11)]
    pan2c += [(f"{IND_LAB[g]}: his job loss other than on layoff", (lambda g: lambda d: (d.hind == g) & notlay(d))(g))
              for g in (2, 3, 8)]
    table(md, "2_industry", C2, pan2c)
    md.append("**(v) By both spouses' class of worker at t (private = for-profit or nonprofit; government = federal, "
              "state, local; self-employed = incorporated or not)**\n")
    G = {1: "private", 2: "government", 3: "self-employed"}
    pan2d = [(f"Husband {G[a]}, wife {G[b]}", (lambda a, b: lambda d: (d.h_cg == a) & (d.w_cg == b))(a, b))
             for a in (1, 2, 3) for b in (1, 2, 3)]
    pan2d += [("Both private, his job loss other than on layoff",
               lambda d: (d.h_cg == 1) & (d.w_cg == 1) & notlay(d))]
    table(md, "2_class_of_worker", C2, pan2d)

    # ---------------- 3. same-employer bound
    md.append("## 3. Same-employer bound\n")
    W0["m_maj"] = W0.same_ind
    W0["m_det"] = W0.same_dind
    W0["m_do"] = (W0.same_dind & ((W0.h_docc == W0.w_docc) & (W0.h_docc > 0)).astype("int8")).astype("int8")
    W0["m_doc"] = (W0.m_do & ((W0.h_cow == W0.w_cow) & (W0.h_cow > 0)).astype("int8")).astype("int8")
    raw = c0["p1"] - c0["p0"]
    rdiff = lpm(W0[(W0.same_ind == 0) & (W0.h_ind > 0) & (W0.w_ind > 0)], "y", ["H"], fe=["sm"])
    ex_diff = rdiff["b"]["H"]
    md.append(f"Arithmetic. Let a share s of couples work at the same establishment and suppose that, when the husband "
              f"loses his job, the wife in such a couple loses hers in the same month with probability p, while all other "
              f"wives lose theirs at the base rate p0 = {P0:.4f}. Then P(w | h) - p0 = s (p - p0), so p = p0 + excess / s. "
              f"Hyatt (2019, Monthly Labor Review, LEHD): 10-12% of dual-earner couples work at the same establishment. "
              f"The last column lets couples outside the same establishment keep the excess estimated for couples in "
              f"different major industries ({cellr(rdiff, 'H')}), so the same-employer p it gives is a lower bound.\n")
    md.append("| s (share at the same establishment) | p reproducing the state x month FE excess "
              f"{EXC:.4f} | p reproducing the raw difference {raw:.4f} | p if other couples keep {ex_diff:.4f} |\n"
              "|---|---|---|---|")
    for s in (0.10, 0.11, 0.12):
        p1, p2, p3 = P0 + EXC / s, P0 + raw / s, P0 + (EXC - (1 - s) * ex_diff) / s
        ROWS.append(dict(table="3_bound", sample=f"s={s:.2f}", outcome="required p (FE excess)", coef=p1, p0=P0,
                         p_raw=p2, p_other_excess=p3))
        md.append(f"| {s:.2f} | {p1:.3f} | {p2:.3f} | {p3:.3f} |")
    md.append("\n**The tightest CPS proxies for a shared employer.** Shares are weighted shares of couples in the sample "
              "with H = 0 / H = 1; 'contribution' = share of H = 1 couples in the group x (P(w|h) - P(w|not h) within the "
              "group), divided by the raw difference P(w|h) - P(w|not h) in the whole sample.\n")
    md.append("| Match of the spouses' main jobs at t | Share H = 0 | Share H = 1 | P(w\\|not h) / P(w\\|h) in group | "
              "Excess in group (state x month FE) | N / N(H = 1) | Contribution to raw excess |\n"
              "|---|---|---|---|---|---|---|")
    for g, lab in (("m_maj", "Same major industry"), ("m_det", "Same detailed industry"),
                   ("m_do", "Same detailed industry x same detailed occupation"),
                   ("m_doc", "Same detailed industry x detailed occupation x class of worker")):
        dd = W0[W0[g] == 1]
        r = lpm(dd, "y", ["H"], fe=["sm"])
        c = cells(dd, "y")
        s0 = wmean(W0.loc[W0.H == 0, g], W0.loc[W0.H == 0, "w"])
        s1 = wmean(W0.loc[W0.H == 1, g], W0.loc[W0.H == 1, "w"])
        contrib = s1 * (c["p1"] - c["p0"]) / raw
        rec("3_proxy_match", lab, "wife job loser t+1", r, cells=dict(**c, share0=s0, share1=s1, contrib=contrib))
        md.append(f"| {lab} | {s0:.4f} | {s1:.4f} | {c['p0']:.4f} / {c['p1']:.4f} | {cellr(r, 'H')} | "
                  f"{r['N']:,} / {c['n1']:,} | {contrib:.3f} |")
    dn = W0[W0.m_doc == 0]
    rn = lpm(dn, "y", ["H"], fe=["sm"])
    cn = cells(dn, "y")
    rec("3_proxy_match", "Not same detailed industry x occupation x class", "wife job loser t+1", rn, cells=cn)
    md.append(f"| All couples not in the tightest cell | {1 - s0:.4f} | {1 - s1:.4f} | {cn['p0']:.4f} / {cn['p1']:.4f} "
              f"| {cellr(rn, 'H')} | {rn['N']:,} / {cn['n1']:,} | |")
    md.append(f"\nThe tightest proxy covers {s0:.1%} of couples (weighted, H = 0) against 10-12% at the same "
              f"establishment in the LEHD; within it the wife loses her job in the husband's month with probability "
              f"{c['p1']:.3f}. The proxy is too wide (same cell, different employer) and too narrow (same employer, "
              f"different occupation or class), so it brackets rather than measures the same-employer channel; the LEHD "
              f"is needed for the definitive answer.\n")

    # ---------------- 4. selection
    md.append("## 4. Selection: couples observed in all four months of the rotation\n")
    pos = ((W0.mis - 1) % 4 + 1).to_numpy()
    lk = lambda k: (W0[f"h_s{k:+d}"] != -1).to_numpy()                    # noqa: E731
    full = np.select([pos == 1, pos == 2, pos == 3], [lk(2) & lk(3), lk(-1) & lk(2), lk(-2) & lk(-1)], False)
    W0["full4"] = full.astype("int8")
    sh0, sh1 = W0.loc[W0.H == 0, "full4"].mean(), W0.loc[W0.H == 1, "full4"].mean()
    md.append(f"A couple-month counts as fully observed if the same couple (both spouses, still naming each other, same "
              f"line numbers) is linked in the other months of its 4-month rotation (base months with household-ID "
              f"breaks count as not linked). Share fully observed (unweighted): {sh0:.3f} when the husband stays "
              f"employed, {sh1:.3f} when he becomes a job loser.\n")
    pan4 = [("All couples", allr), ("Observed in all four months", lambda d: d.full4 == 1),
            ("Not observed in all four months", lambda d: d.full4 == 0)]
    table(md, "4_selection", [("wife job loser t+1", W0, "y"),
                              ("wife job loser t+1, excl. 2020-21", W0[nonc(W0)], "y")], pan4)
    ROWS.append(dict(table="4_selection", sample="share fully observed", outcome="H=0 / H=1", p0=sh0, p1=sh1))

    # ---------------- 5. event study for the figure
    md.append("## 5. Figure 1: the wife's excess monthly job-loss hazard around the husband's job-loss month\n")
    ev = event_samples(P)
    md.append(f"tau = month in which the husband becomes a job loser. tau-2..tau+2 as in 30 (flow events: employed in "
              f"the previous month, job loser now; base month tau-1; control husbands employed in every month of the "
              f"window). At tau-3 the wife's previous month, and at tau+3 the husband's, falls outside the 4-month "
              f"rotation: there that spouse's job loss is a job loser with unemployment duration <= {DUR_MAX} weeks "
              f"(risk set: employed or such a new job loser); base month tau-1 (tau-3) or tau (tau+3). The 'duration' "
              f"columns redo tau-2, tau and tau+2 with the same duration rule (tau: both spouses by duration in one "
              f"month, no linkage at all). 79% of flow job losers report a duration of 4 weeks or less.\n")
    evcols = list(ev)
    md.append("| | " + " | ".join(f"({i + 1}) wife job loser at {j}" for i, j in enumerate(evcols)) + " |")
    md.append("|---" * (len(evcols) + 1) + "|")
    evres = {}
    for j in evcols:
        r = lpm(ev[j], "y", ["H"], fe=["sm"])
        c = cells(ev[j], "y")
        evres[j] = (r, c)
        rec("5_event", j, f"wife job loser at {j}", r, cells=c)
    md.append("| Husband job loser at tau | " + " | ".join(cellr(evres[j][0], "H") for j in evcols) + " |")
    md.append("| Mean H = 0 / H = 1 (weighted) | " + " | ".join(
        f"{evres[j][1]['p0']:.4f} / {evres[j][1]['p1']:.4f}" for j in evcols) + " |")
    md.append("| N / N(H = 1) | " + " | ".join(f"{evres[j][0]['N']:,} / {evres[j][1]['n1']:,}" for j in evcols) + " |")
    md.append("| Fixed effects | " + " | ".join("state x year-month" for _ in evcols) + " |")
    md.append("| Clusters | " + " | ".join("household [state]" for _ in evcols) + " |\n")
    aw = awe_samples(P)
    awres = {}
    md.append("**Panel B of the second figure: wives not employed at t (30's section 5)**\n")
    acols = [(k, o) for o in ("emp", "une") for k in sorted(aw)]
    alab = {"emp": "employed", "une": "unemployed (looking / layoff)"}
    md.append("| | " + " | ".join(f"({i + 1}) wife {alab[o]} at t+{k}" for i, (k, o) in enumerate(acols)) + " |")
    md.append("|---" * (len(acols) + 1) + "|")
    for k, o in acols:
        r = lpm(aw[k], o, ["H"], fe=["sm"])
        c = cells(aw[k], o)
        awres[(k, o)] = (r, c)
        rec("5_awe", f"t+{k}", f"wife {alab[o]}", r, cells=c)
    md.append("| Husband becomes job loser (t+1) | " + " | ".join(cellr(awres[a][0], "H") for a in acols) + " |")
    md.append("| Mean H = 0 / H = 1 (weighted) | " + " | ".join(
        f"{awres[a][1]['p0']:.3f} / {awres[a][1]['p1']:.3f}" for a in acols) + " |")
    md.append("| N / N(H = 1) | " + " | ".join(f"{awres[a][0]['N']:,} / {awres[a][1]['n1']:,}" for a in acols) + " |")
    md.append("| Fixed effects | " + " | ".join("state x year-month" for _ in acols) + " |\n")
    plot(evres, awres)
    md.append("Figure files: `paperA_joint_loss/fig_cps_monthly_hazard.pdf` / `.png` (single panel, 95% CIs from "
              "household-clustered s.e.) and `fig_cps_monthly_hazard_awe.png` (adds panel B). The CPS observes t+1..t+3 "
              "and t+12 only (rotation 4-8-4).\n")
    (OUT / "cps_joint_loss_checks.md").write_text("\n".join(md), encoding="utf-8")
    out = pd.DataFrame(ROWS)
    out["stars"] = out["p_hh"].map(lambda p: stars(p) if pd.notna(p) else "")
    out.to_csv(OUT / "cps_joint_loss_checks.csv", index=False)
    print("\n".join(md))


def event_samples(P):
    b = (P.h_s == 1) & P["h_s+1"].isin([1, 2])
    Hm = P["h_s+1"] == 2
    H = lambda d: (d["h_s+1"] == 2).astype("int8")                        # noqa: E731
    ev = {}
    # tau-3: wife new job loser at tau-3 by duration (offset -2 from base tau-1); husband employed tau-3..tau-1
    rs = (P["w_s-2"] == 1) | ((P["w_s-2"] == 2) & P["w_dur-2"].between(0, DUR_MAX))
    ev["tau-3"] = P[b & (P["h_s-2"] == 1) & (P["h_s-1"] == 1) & rs].assign(
        y=lambda d: (d["w_s-2"] == 2).astype("int8"), H=H)
    ev["tau-2"] = P[b & (P["h_s-2"] == 1) & (P["h_s-1"] == 1) & (P["w_s-2"] == 1) & (P["w_s-1"] >= 1)].assign(
        y=lambda d: (d["w_s-1"] == 2).astype("int8"), H=H)
    rs = (P["w_s-1"] == 1) | ((P["w_s-1"] == 2) & P["w_dur-1"].between(0, DUR_MAX))
    ev["tau-2 duration"] = P[b & (P["h_s-1"] == 1) & rs].assign(y=lambda d: (d["w_s-1"] == 2).astype("int8"), H=H)
    ev["tau-1"] = P[b & (P["h_s-1"] == 1) & (P["w_s-1"] == 1)].assign(y=lambda d: (d.w_s == 2).astype("int8"), H=H)
    ev["tau"] = P[b & (P.w_s == 1) & (P["w_s+1"] >= 1)].assign(y=lambda d: (d["w_s+1"] == 2).astype("int8"), H=H)
    hn = (P.h_s == 2) & P.h_dur.between(0, DUR_MAX)
    wr = (P.w_s == 1) | ((P.w_s == 2) & P.w_dur.between(0, DUR_MAX))
    ev["tau duration"] = P[((P.h_s == 1) | hn) & wr].assign(y=lambda d: (d.w_s == 2).astype("int8"),
                                                            H=lambda d: (d.h_s == 2).astype("int8"))
    ev["tau+1"] = P[b & (P["w_s+1"] == 1) & (P["w_s+2"] >= 1) & (P["h_s+2"] >= 1) & (Hm | (P["h_s+2"] == 1))].assign(
        y=lambda d: (d["w_s+2"] == 2).astype("int8"), H=H)
    ev["tau+2"] = P[b & (P["w_s+2"] == 1) & (P["w_s+3"] >= 1) & (P["h_s+2"] >= 1) & (P["h_s+3"] >= 1)
                    & (Hm | ((P["h_s+2"] == 1) & (P["h_s+3"] == 1)))].assign(
        y=lambda d: (d["w_s+3"] == 2).astype("int8"), H=H)

    def hyb(k):
        """Husband new job loser at base month tau by duration; controls employed tau..tau+k; wife's flow at tau+k."""
        later = np.ones(len(P), bool)
        ctrl = (P.h_s == 1).to_numpy(copy=True)
        for j in range(1, k + 1):
            later &= (P[f"h_s{j:+d}"] >= 1).to_numpy()
            ctrl &= (P[f"h_s{j:+d}"] == 1).to_numpy()
        m = ((hn.to_numpy() | ctrl) & later & (P[f"w_s{k - 1:+d}"] == 1).to_numpy()
             & (P[f"w_s{k:+d}"] >= 1).to_numpy())
        return P[m].assign(y=lambda d: (d[f"w_s{k:+d}"] == 2).astype("int8"), H=lambda d: (d.h_s == 2).astype("int8"))
    ev["tau+2 duration"] = hyb(2)
    ev["tau+3"] = hyb(3)
    order = ["tau-3", "tau-2", "tau-2 duration", "tau-1", "tau", "tau duration", "tau+1", "tau+2", "tau+2 duration",
             "tau+3"]
    return {k: ev[k] for k in order}


def awe_samples(P):
    """30's section 5: wives not employed at t, husband employed at t; H = husband job loser at t+1."""
    base = (P.h_s == 1) & P.w_s.isin([2, 3, 4]) & P["h_s+1"].isin([1, 2])
    aw = {}
    for k in (1, 2, 3, 12):
        mk = base & (P[f"w_s{k:+d}"] >= 1)
        if k != 12:
            for j in range(2, k + 1):
                mk &= (P[f"h_s{j:+d}"] >= 1) & ((P["h_s+1"] == 2) | (P[f"h_s{j:+d}"] == 1))
        aw[k] = P[mk].assign(H=lambda d: (d["h_s+1"] == 2).astype("int8"),
                             emp=lambda d, k=k: (d[f"w_s{k:+d}"] == 1).astype("int8"),
                             une=lambda d, k=k: d[f"w_s{k:+d}"].isin([2, 3]).astype("int8"))
    return aw


# ================================================================ 5. figure
def plot(evres, awres):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"],
                         "mathtext.fontset": "stix", "font.size": 11, "axes.labelsize": 11, "xtick.labelsize": 10.5,
                         "ytick.labelsize": 10.5, "pdf.fonttype": 42})
    blue, orange, ink, ink2, grid = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#d9d8d4"
    keys = ["tau-3", "tau-2", "tau-1", "tau", "tau+1", "tau+2", "tau+3"]
    xs = np.arange(-3, 4)
    p0 = evres["tau"][1]["p0"]

    def style(ax):
        ax.grid(axis="y", color=grid, lw=0.7)
        ax.set_axisbelow(True)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        for sp in ("left", "bottom"):
            ax.spines[sp].set_color(ink2)
        ax.tick_params(colors=ink, length=3)
        ax.axhline(0, color=ink2, lw=0.8)

    def panel_a(ax):
        b = np.array([100 * evres[k][0]["b"]["H"] for k in keys])
        se = np.array([100 * evres[k][0]["se_hh"]["H"] for k in keys])
        ax.plot(xs, b, color=blue, lw=1.4, zorder=2)
        for x, bb, s in zip(xs, b, se):
            ax.errorbar(x, bb, yerr=1.96 * s, fmt="o", ms=7, color=blue, mfc="white" if abs(x) == 3 else blue,
                        mew=1.6, elinewidth=1.4, capsize=3, zorder=3)
        ax.set_xticks(xs, [r"$\tau-3$", r"$\tau-2$", r"$\tau-1$", r"$\tau$", r"$\tau+1$", r"$\tau+2$", r"$\tau+3$"])
        ax.set_xlabel(r"Month of the wife's job loss relative to the husband's job-loss month $\tau$")
        ax.set_ylabel("Excess monthly job-loss probability (pp)")
        style(ax)
        ax.annotate(f"+{b[3]:.1f} pp", (0, b[3]), xytext=(10, 0), textcoords="offset points", va="center",
                    color=ink, fontsize=10.5)
        ax.text(0.02, 0.97, f"Base rate, husband employed:\n{100 * p0:.2f}% a month\n\n"
                "Open symbols: previous month\noutside the 4-month rotation\n(duration-based)",
                transform=ax.transAxes, ha="left", va="top", fontsize=9.5, color=ink2, linespacing=1.3)

    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    panel_a(ax)
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(PAPER / f"fig_cps_monthly_hazard.{ext}", dpi=300)
    plt.close(fig)

    fig, axs = plt.subplots(1, 2, figsize=(12, 4.4))
    panel_a(axs[0])
    ax = axs[1]
    ks, pos = [1, 2, 3, 12], np.array([1, 2, 3, 5])
    for o, col, mk, lab, dx in (("une", orange, "s", "Unemployed (looking or on layoff)", -0.06),
                                ("emp", blue, "o", "Employed", 0.06)):
        b = np.array([100 * awres[(k, o)][0]["b"]["H"] for k in ks])
        se = np.array([100 * awres[(k, o)][0]["se_hh"]["H"] for k in ks])
        ax.plot(pos[:3] + dx, b[:3], color=col, lw=1.4)
        ax.plot(pos[2:] + dx, b[2:], color=col, lw=1.0, ls=":")
        ax.errorbar(pos + dx, b, yerr=1.96 * se, fmt=mk, ms=7, color=col, elinewidth=1.4, capsize=3, label=lab)
    ax.set_xticks(pos, ["t+1", "t+2", "t+3", "t+12"])
    ax.set_xlabel("Month after the base month t (husband's job loss at t+1)")
    ax.set_ylabel("Excess probability, wives not employed at t (pp)")
    style(ax)
    ax.legend(frameon=False, fontsize=10, loc="upper right")
    for a, lab in zip(axs, "AB"):
        a.text(-0.1, 1.03, lab, transform=a.transAxes, fontsize=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(PAPER / "fig_cps_monthly_hazard_awe.png", dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    download()
    if "--download-only" not in sys.argv:
        main()
