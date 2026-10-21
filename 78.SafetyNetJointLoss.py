r"""The safety net around a joint loss: SNAP, UI, TANF and where the EITC puts the couple (2026-10-20) [Paper A; WP6 of
proposals/fable_10h_plan_paperA.md]

Why. Counterfactual (iii) of Paper A ranks an EITC-type earnings subsidy against an equal-cost transfer on the claim
that the subsidy 'pays least when both spouses have lost their jobs'. Section 5's safety-net subsection had one PSID
number (SNAP after his displacement) and the two SNAP level targets. This script supplies the monthly SNAP / UI path
around single and joint losses (SIPP) and places the couple on the EITC schedule before and after (PSID).

DATA (all read only; nothing of the source scripts is edited)
  SIPP  40.SIPPJointLoss.py couples panel (panels 2004, 2008, 2014; reference months 2003-2016) with the person-month
        program variables of both spouses, extracted from the raw core files by 75.EstablishedWifeExits.sipp_extras
        (scratch cache outside the repository): 2004/08 household food-stamp amount THFDSTP, own food-stamp receipt
        ER27 / amount T27AMT / coverage RCUTYP27, state UI receipt ER05 / amount T05AMT, TANF ER20 / T20AMT; 2014
        (event-history calendar, monthly) SNAP RFSYN / TFS_AMT / RFSCOV, UI EUC1-3MNYN / TUC1-3AMT, TANF RTANFYN /
        TTANF_AMT. Amounts deflated to 2000 dollars with the CPI-U of IGE/common.py.
  PSID  60.PaperATargets.py's cached objects (data/paperA_targets_psid.pkl, read only; 60 is not run): 25's
        couple-years CY (consecutive interviews of the same couple, both spouses with positive hours in the earlier
        year, intervals ending 1984-2021; h / w = husband / wife displaced in the interval) and the men's panel m
        (labor incomes of both spouses in 2000 $, number of children, food-stamp and AFDC/TANF receipt in the income
        year). EITC schedule: 61's era-mean schedules paperA_model/inputs/schedules_era{1,2,3}.json (read only;
        married-joint phase-out start; 2000 dollars; children 0 / 1 / 2 / 3+).
DESIGNS
  SIPP event study (months around his job loss). Event: husband's involuntary separation (40's INV: layoff, closure,
  discharge, temporary job ended, other involuntary) at month tau, both spouses employed at tau-1, wife 25-59, the
  couple observed tau-3..tau+3; the couple's first such event. (a) his loss alone: no INV of the wife in tau-3..tau+3;
  (b) joint loss: an INV of the wife in tau-3..tau+3. Controls (clean): couples never with a husband event, one random
  pseudo-event month b per couple among the months with both employed at b-1, him employed at b, no INV of his in
  b-6..b+12 and none of hers in b-3..b+3. Rows: s = tau-6..tau+12. Outcomes: household SNAP receipt and amount (2000 $
  a month, zeros included), UI receipt of him, of her, of either, TANF receipt of either, no earner and no UI in the
  month, employment of each. Levels: weighted (wife's weight at tau-1) means by event month and group. Regression:
  y = unit FE + panel x rotation x calendar-month FE + event-month dummies x group (reference s = -3..-1), unweighted
  (as in 40), s.e. clustered by household; bins s = -6..-4 (pre-trend), 0..2, 3..5, 6..11 and the joint - alone
  difference.
  PSID couple-years: the EITC region of the couple's earnings (his + her labor income, married-joint schedule of the
  era of the income year, number of children capped at 3) in the year before the interval (earlier interview) and at
  the end of the interval: no earnings / phase-in / plateau / phase-out / above the range; the schedule credit and its
  change; food-stamp and AFDC/TANF receipt in the same years; by group (neither displaced, his displacement alone, hers
  alone, joint = both in the same interval) and race. LPMs of the changes on the group dummies with calendar-year FE
  (no region x year FE), s.e. clustered by 1968 family; also annual intervals only (to 1996). This is an accounting of
  where the schedule puts the couple (no AGI or investment-income tests, no take-up), not a receipt measure.
  Associations, not causal effects. *** p<0.01, ** p<0.05, * p<0.1 (normal approximation).
OUTPUTS (aggregate only)
  output/safety_net_joint_loss.csv  every estimate: dataset, table, sample, cell, outcome, coef, se, p, stars, n
  output/safety_net_joint_loss.md   tables
  output/safety_net_joint_loss.png  monthly SNAP / UI paths around his loss alone vs a joint loss (SIPP)
  paperA_joint_loss/fig_sipp_household_months.pdf (.png)  event-study coefficients by month, six outcomes (2026-10-21:
                                    family earnings added; Fable's figure 1)
Run from the repository root: .venv/Scripts/python.exe -I IGE/78.SafetyNetJointLoss.py [--only sipp,psid]
  [--scratch DIR] (the scratch of IGE/75; the extracts are built there if missing)
"""
import argparse
import importlib.util
import json
import sys
import tempfile
import time
import warnings
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import numpy as np                            # noqa: E402
import pandas as pd                           # noqa: E402
from scipy.stats import norm                  # noqa: E402

from common import CPI, DATA, OUT, stars      # noqa: E402

warnings.simplefilter("ignore", FutureWarning)
warnings.simplefilter("ignore", RuntimeWarning)
T0 = time.time()
TAG = "safety_net_joint_loss"
ROWS = []
SCHED = HERE / "paperA_model" / "inputs"


def log(*a):
    print(f"[{time.time() - T0:7.0f}s]", *a, flush=True)


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def pval(b, se):
    return float(2 * norm.sf(abs(b / se))) if (np.isfinite(se) and se > 0) else np.nan


def add(dataset, table, sample, cell, outcome, coef, se=np.nan, n=np.nan, note=""):
    p = pval(coef, se)
    ROWS.append(dict(dataset=dataset, table=table, sample=sample, cell=cell, outcome=outcome, coef=float(coef),
                     se=float(se) if np.isfinite(se) else np.nan, p=p, stars=stars(p) if np.isfinite(p) else "",
                     n=n, note=note))


def wmean(x, w):
    x, w = np.asarray(x, float), np.asarray(w, float)
    ok = np.isfinite(x) & np.isfinite(w)
    return float(np.sum(x[ok] * w[ok]) / np.sum(w[ok])) if ok.any() and np.sum(w[ok]) > 0 else np.nan


def within(A, groups, iters=200, tol=1e-9):
    """Unweighted within transformation for one or two sets of FE (alternating projections)."""
    A = A.copy()
    codes = [pd.factorize(g)[0] for g in groups]
    cnts = [np.maximum(np.bincount(c), 1) for c in codes]
    for it in range(iters if len(codes) > 1 else 1):
        mx = 0.0
        for c, n in zip(codes, cnts):
            for j in range(A.shape[1]):
                mj = (np.bincount(c, weights=A[:, j], minlength=len(n)) / n)[c]
                A[:, j] -= mj
                mx = max(mx, float(np.abs(mj).max()))
        if mx < tol:
            break
    return A


def ols_cl(y, X, groups, cl):
    """OLS of y on X (N x K) absorbing FE groups; CR1 cluster-robust vcov. Returns b, V, N, G."""
    ok = np.isfinite(y) & np.isfinite(X).all(1)
    y, X, cl = y[ok], X[ok], np.asarray(cl)[ok]
    groups = [np.asarray(g)[ok] for g in groups]
    A = within(np.column_stack([y, X]), groups) if groups else np.column_stack([y - y.mean(), X - X.mean(0)])
    yt, Xt = A[:, 0], A[:, 1:]
    XtXi = np.linalg.pinv(Xt.T @ Xt)
    b = XtXi @ Xt.T @ yt
    u = yt - Xt @ b
    g = pd.factorize(cl)[0]
    G = g.max() + 1
    S = np.column_stack([np.bincount(g, weights=Xt[:, j] * u, minlength=G) for j in range(Xt.shape[1])])
    N, K = Xt.shape
    V = XtXi @ (S.T @ S) @ XtXi * (G / (G - 1)) * ((N - 1) / max(N - K, 1))
    return b, V, N, G


def lincomb(b, V, L):
    L = np.asarray(L, float)
    return float(L @ b), float(np.sqrt(max(L @ V @ L, 0)))


# =====================================================================================================
# SIPP: monthly event study around his job loss
# =====================================================================================================
S_MIN, S_MAX = -6, 12
REF = (-3, -2, -1)
BINS = {"pre s=-6..-4": range(-6, -3), "s=0..2": range(0, 3), "s=3..5": range(3, 6), "s=6..11": range(6, 12)}
OUTC = {"snap": "SNAP receipt, household (%)", "snap_amt": "SNAP amount, household (2000 $ a month)",
        "ui_h": "UI receipt, husband (%)", "ui_w": "UI receipt, wife (%)", "ui_any": "UI receipt, either spouse (%)",
        "tanf": "TANF receipt, either spouse (%)", "noinc": "no earner and no UI in the month (%)",
        "emp_h": "husband employed (%)", "emp_w": "wife employed (%)",
        "earn": "family earnings, his + hers (2000 $ a month)"}
PCT = {k for k in OUTC if k not in ("snap_amt", "earn")}


def sipp_outcomes(P):
    def f(c):
        return P[c].to_numpy(float) if c in P else np.full(len(P), np.nan)
    defl = np.array([CPI[2000] / CPI.get(int(y), np.nan) for y in P.year.to_numpy()])
    p14 = (P.panel == 2014).to_numpy()
    fs_any = np.fmax(np.nan_to_num(f("fs_r_h")), np.nan_to_num(f("fs_r_w")))
    fs_cov = np.fmax(np.nan_to_num(f("fs_cov_h")), np.nan_to_num(f("fs_cov_w")))
    hh_amt = np.fmax(np.nan_to_num(f("hh_fs_a_h")), np.nan_to_num(f("hh_fs_a_w")))
    own_amt = np.nan_to_num(np.clip(f("fs_a_h"), 0, None)) + np.nan_to_num(np.clip(f("fs_a_w"), 0, None))
    amt = np.where(p14, own_amt, np.fmax(hh_amt, own_amt))
    obs = np.isfinite(f("fs_r_h")) | np.isfinite(f("fs_r_w")) | np.isfinite(f("hh_fs_a_h"))
    snap = np.where(obs, ((fs_any == 1) | (fs_cov == 1) | (amt > 0)).astype(float), np.nan)
    P["snap"] = 100 * snap
    P["snap_amt"] = np.where(obs, amt * defl, np.nan)
    for s in ("h", "w"):
        r, a = f(f"ui_r_{s}"), f(f"ui_a_{s}")
        # 2014: the monthly UC items (EUCkMNYN, TUCkAMT) are asked only of persons with UC in the reference year;
        # outside that universe they are blank and mean no receipt (the person's record exists: SNAP recode present)
        rec14 = p14 & (np.isfinite(f(f"fs_r_{s}")) | np.isfinite(f(f"earn_{s}")))
        r = np.where(rec14 & ~np.isfinite(r), 0.0, r)
        ob = np.isfinite(r) | np.isfinite(a)
        P[f"ui_{s}"] = np.where(ob, 100 * ((np.nan_to_num(r) == 1) | (np.nan_to_num(a) > 0)), np.nan)
    P["ui_any"] = np.fmax(P.ui_h.to_numpy(float), P.ui_w.to_numpy(float))
    tr = np.fmax(np.nan_to_num(f("tanf_r_h")), np.nan_to_num(f("tanf_r_w")))
    ta = np.nan_to_num(np.clip(f("tanf_a_h"), 0, None)) + np.nan_to_num(np.clip(f("tanf_a_w"), 0, None))
    P["tanf"] = np.where(obs, 100 * ((tr == 1) | (ta > 0)), np.nan)
    noemp = (P.E_h.to_numpy() == 0) & (P.E_w.to_numpy() == 0)
    P["noinc"] = np.where(np.isfinite(P.ui_any), 100 * (noemp & (P.ui_any.to_numpy(float) == 0)), np.nan)
    P["emp_h"] = 100 * P.E_h.astype(float)
    P["emp_w"] = 100 * P.E_w.astype(float)
    # monthly earnings of both spouses (TPEARN, total person earnings; negative self-employment amounts set to 0)
    eh, ew = np.clip(f("earn_h"), 0, None), np.clip(f("earn_w"), 0, None)
    P["earn"] = np.where(np.isfinite(eh) & np.isfinite(ew), (eh + ew) * defl, np.nan)
    return P


def sipp_part(scratch, workers):
    M75 = _load("ige75", "75.EstablishedWifeExits.py")
    sys.modules["ige75"] = M75
    sys.modules["ige63"] = M75.M63
    P, L = M75.sipp_panel(scratch, workers)
    # codings of the 2014 SNAP coverage recode (diagnostic, aggregate)
    for c in ("fs_r_w", "fs_cov_w", "ui_r_h"):
        for pnl in (2004, 2008, 2014):
            v = P.loc[P.panel == pnl, c]
            add("SIPP", "diag", f"panel {pnl}", c, "share = 1 among non-missing (%)", 100 * v.mean(), np.nan,
                int(v.notna().sum()))
    P = sipp_outcomes(P)
    Eh = P.E_h.to_numpy(float)
    Eh1, Ew1 = L.at("E_h", -1), L.at("E_w", -1)
    inv_h, inv_w = P.INV_h.to_numpy(float), P.INV_w.to_numpy(float)
    age = P.age_w.between(25, 59).to_numpy()
    obs33 = np.ones(len(P), bool)
    joint = np.zeros(len(P), bool)
    for k in range(-3, 4):
        iw = L.at("INV_w", k)
        obs33 &= np.isfinite(iw)
        joint |= np.nan_to_num(iw) == 1
    ev = (inv_h == 1) & (Eh1 == 1) & (Ew1 == 1) & age & obs33
    P["_ev"] = ev
    first = ev & (P.groupby("cid")["_ev"].cumsum().to_numpy() == 1)
    treated_cid = set(P.cid.to_numpy()[ev])
    # clean pseudo-events
    noinvh = np.ones(len(P), bool)
    for k in range(-6, 13):
        noinvh &= np.nan_to_num(L.at("INV_h", k)) == 0
    cand = ((Eh1 == 1) & (Ew1 == 1) & (Eh == 1) & age & obs33 & ~joint & noinvh
            & ~P.cid.isin(treated_cid).to_numpy())
    rng = np.random.default_rng(78)
    ci = np.flatnonzero(cand)
    order = rng.permutation(len(ci))
    pick = pd.Series(ci[order]).groupby(P.cid.to_numpy()[ci[order]]).first().to_numpy()
    units = pd.DataFrame({"row": np.concatenate([np.flatnonzero(first), pick]),
                          "grp": np.concatenate([np.where(joint[first], "joint", "alone"),
                                                 np.full(len(pick), "control")])})
    units["uid"] = np.arange(len(units))
    log(f"SIPP: events alone {int((units.grp == 'alone').sum()):,}, joint {int((units.grp == 'joint').sum()):,}, "
        f"controls {int((units.grp == 'control').sum()):,}")
    key = L.key
    idx = L.idx
    stack = []
    for s in range(S_MIN, S_MAX + 1):
        p = idx.get_indexer(key[units.row.to_numpy()] + s)
        okp = p >= 0
        stack.append(pd.DataFrame({"uid": units.uid.to_numpy()[okp], "grp": units.grp.to_numpy()[okp], "s": s,
                                   "pos": p[okp]}))
    St = pd.concat(stack, ignore_index=True)
    wt = P.wgt_w.to_numpy(float)[units.row.to_numpy()]
    St["w"] = wt[St.uid.to_numpy()]
    St["hh"] = P.hh.to_numpy()[St.pos.to_numpy()]
    St["pm"] = P.pm.to_numpy()[St.pos.to_numpy()]
    St["black"] = (P.race_h.to_numpy()[units.row.to_numpy()] == 2)[St.uid.to_numpy()]
    for c in OUTC:
        St[c] = P[c].to_numpy(float)[St.pos.to_numpy()]
    del P
    # levels by event month
    for g in ("alone", "joint", "control"):
        G = St[St.grp == g]
        for s in range(S_MIN, S_MAX + 1):
            q = G[G.s == s]
            for c in OUTC:
                add("SIPP", "lev", f"{g}", f"s={s:+d}", OUTC[c], wmean(q[c], q.w), np.nan, int(q[c].notna().sum()))
        # post-loss bins (levels)
        for bn, rr in list(BINS.items()) + [("s=1..6", range(1, 7))]:
            q = G[G.s.isin(list(rr))]
            for c in OUTC:
                add("SIPP", "lev-bin", f"{g}", bn, OUTC[c], wmean(q[c], q.w), np.nan, int(q[c].notna().sum()))
        q = G[G.s.isin(list(REF))]
        for c in OUTC:
            add("SIPP", "lev-bin", f"{g}", "ref s=-3..-1", OUTC[c], wmean(q[c], q.w), np.nan, int(q[c].notna().sum()))
    # joint-loss months s = 1..6 in which both spouses are not employed: UI of neither, SNAP
    for g in ("alone", "joint"):
        q = St[(St.grp == g) & St.s.between(1, 6)]
        both = (q.emp_h == 0) & (q.emp_w == 0)
        hn = q.emp_h == 0
        for lab, mk in (("both spouses not employed", both), ("husband not employed", hn)):
            qq = q[mk]
            add("SIPP", "cond", f"{g}, s=1..6, {lab}", "share of couple-months (%)", "share (%)",
                100 * wmean(mk.astype(float), q.w), np.nan, len(q))
            add("SIPP", "cond", f"{g}, s=1..6, {lab}", "UI receipt of neither spouse (%)", "share (%)",
                100 - wmean(qq.ui_any, qq.w), np.nan, int(qq.ui_any.notna().sum()))
            add("SIPP", "cond", f"{g}, s=1..6, {lab}", "SNAP receipt (%)", "share (%)", wmean(qq.snap, qq.w),
                np.nan, int(qq.snap.notna().sum()))
            add("SIPP", "cond", f"{g}, s=1..6, {lab}", "no UI and no SNAP (%)", "share (%)",
                100 * wmean(((qq.ui_any == 0) & (qq.snap == 0)).astype(float), qq.w), np.nan, len(qq))
        # race split (levels, s = 1..6)
        for rlab, rmk in (("Black", q.black), ("White / other", ~q.black)):
            qq = q[rmk]
            for c in ("snap", "ui_any", "noinc"):
                add("SIPP", "race", f"{g}, s=1..6", rlab, OUTC[c], wmean(qq[c], qq.w), np.nan, int(qq[c].notna().sum()))
    # regression: unit FE + calendar FE, event-month x group dummies (reference s = -3..-1)
    ss = [s for s in range(S_MIN, S_MAX + 1) if s not in REF]
    names = [f"{g}:{s}" for g in ("alone", "joint") for s in ss]
    X = np.column_stack([((St.grp == g) & (St.s == s)).to_numpy(float) for g in ("alone", "joint") for s in ss])
    ix = {n: i for i, n in enumerate(names)}
    for c in OUTC:
        y = St[c].to_numpy(float)
        b, V, N, G = ols_cl(y, X, [St.uid.to_numpy(), St.pm.to_numpy()], St.hh.to_numpy())
        note = f"clusters={G}; unit FE + panel x rotation x month FE; ref s=-3..-1"
        for g in ("alone", "joint"):
            for s in ss:
                Lv = np.zeros(len(names))
                Lv[ix[f"{g}:{s}"]] = 1
                e, se = lincomb(b, V, Lv)
                add("SIPP", "es", g, f"s={s:+d}", OUTC[c], e, se, N, note)
        for bn, rr in BINS.items():
            Ls = {}
            for g in ("alone", "joint"):
                Lv = np.zeros(len(names))
                for s in rr:
                    Lv[ix[f"{g}:{s}"]] = 1 / len(rr)
                Ls[g] = Lv
                e, se = lincomb(b, V, Lv)
                add("SIPP", "es-bin", bn, g, OUTC[c], e, se, N, note)
            e, se = lincomb(b, V, Ls["joint"] - Ls["alone"])
            add("SIPP", "es-bin", bn, "joint - alone", OUTC[c], e, se, N, note)
        log(f"SIPP: {c} done")
    St.attrs = {}
    return St


def plot(D, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    col = {"alone": "#2a78d6", "joint": "#eb6834"}
    lab = {"alone": "his loss alone", "joint": "joint loss (her loss within 3 months)"}
    panels = [("SNAP receipt, household (%)", "SNAP receipt (%)"), ("UI receipt, husband (%)", "UI receipt, husband (%)"),
              ("UI receipt, wife (%)", "UI receipt, wife (%)"), ("no earner and no UI in the month (%)",
                                                                 "no earner and no UI (%)")]
    fig, axs = plt.subplots(1, 4, figsize=(13, 3.8))
    for ax, (out, title) in zip(axs, panels):
        for g in ("alone", "joint"):
            q = D[(D.table == "lev") & (D["sample"] == g) & (D.outcome == out)].copy()
            q["s"] = q.cell.str.replace("s=", "").astype(int)
            q = q.sort_values("s")
            ax.plot(q.s, q.coef, color=col[g], lw=2, marker="o", ms=3.5, label=lab[g])
        ax.axvline(0, color="#999999", lw=0.8, ls=":")
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("months since his job loss")
        ax.grid(axis="y", color="#e5e5e5", lw=0.6)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    h, lb = axs[0].get_legend_handles_labels()
    fig.legend(h, lb, frameon=False, fontsize=9, loc="lower center", ncol=2)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.savefig(path, dpi=160)
    plt.close(fig)


def plot_es(D, path):
    """Paper figure (Fable's figure 1, proposals/fable_event_study_figures_paperA.md): event-study coefficients by
    month (reference s = -3..-1, unit + panel x rotation x month FE, 95% CIs from household-cluster s.e.), his loss
    alone vs a joint loss. Family earnings in % of the group's weighted level in s = -3..-1."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    col = {"alone": "#2a78d6", "joint": "#eb6834"}
    lab = {"alone": "his loss alone", "joint": "joint loss (her loss within 3 months)"}
    panels = [("husband employed (%)", "(a) Husband employed (pp)", 1),
              ("wife employed (%)", "(b) Wife employed (pp)", 1),
              ("family earnings, his + hers (2000 $ a month)", "(c) Family earnings (% of pre-loss)", None),
              ("UI receipt, either spouse (%)", "(d) UI receipt, either spouse (pp)", 1),
              ("SNAP receipt, household (%)", "(e) SNAP receipt (pp)", 1),
              ("no earner and no UI in the month (%)", "(f) No earner and no UI (pp)", 1)]
    fig, axs = plt.subplots(2, 3, figsize=(12.5, 7.2))
    for ax, (out, title, scale) in zip(axs.ravel(), panels):
        for k, g in enumerate(("alone", "joint")):
            q = D[(D.table == "es") & (D["sample"] == g) & (D.outcome == out)].copy()
            q["s"] = q.cell.str.replace("s=", "").astype(int)
            q = pd.concat([q, pd.DataFrame({"s": list(REF), "coef": 0.0, "se": 0.0})]).sort_values("s")
            sc = scale
            if sc is None:
                ref = D[(D.table == "lev-bin") & (D["sample"] == g) & (D.cell == "ref s=-3..-1") & (D.outcome == out)]
                sc = 100.0 / float(ref.coef.iloc[0])
            x = q.s.to_numpy() + (k - 0.5) * 0.18
            ax.fill_between(x, sc * (q.coef - 1.96 * q.se), sc * (q.coef + 1.96 * q.se), color=col[g], alpha=0.15,
                            lw=0)
            ax.plot(x, sc * q.coef, color=col[g], lw=1.8, marker="o", ms=3, label=lab[g])
        ax.axhline(0, color="#555555", lw=0.7)
        ax.axvline(-0.5, color="#999999", lw=0.8, ls=":")
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("months since his job loss")
        ax.set_xticks(range(S_MIN, S_MAX + 1, 3))
        ax.grid(axis="y", color="#e5e5e5", lw=0.6)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    h, lb = axs[0, 0].get_legend_handles_labels()
    fig.legend(h, lb, frameon=False, fontsize=9.5, loc="lower center", ncol=2)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(path)
    fig.savefig(Path(path).with_suffix(".png"), dpi=160)
    plt.close(fig)


# =====================================================================================================
# PSID: where the EITC puts the couple; SNAP and AFDC/TANF
# =====================================================================================================
def load_eitc():
    S = {}
    for e in (1, 2, 3):
        S[e] = json.loads((SCHED / f"schedules_era{e}.json").read_text())["eitc_annual"]
    return S


def era(y):
    return np.select([y <= 1996, y <= 2008], [1, 2], 3)


REG = ["no earnings", "phase-in", "plateau", "phase-out", "above range"]


def eitc(E, k, yr, S):
    E, k, yr = np.asarray(E, float), np.clip(np.nan_to_num(np.asarray(k, float)), 0, 3).astype(int), np.asarray(yr)
    er = era(yr)
    rin, mx, rout, ps = (np.zeros(len(E)) for _ in range(4))
    for e in (1, 2, 3):
        for kk in range(4):
            s = S[e][str(kk)]
            mk = (er == e) & (k == kk)
            rin[mk], mx[mk], rout[mk], ps[mk] = s["in"], s["max"], s["out"], s["ps_mfj"]
    end = ps + mx / rout
    reg = np.select([~np.isfinite(E), E <= 0, E < mx / rin, E < ps, E < end],
                    ["missing", REG[0], REG[1], REG[2], REG[3]], REG[4])
    cr = np.clip(np.minimum(rin * np.clip(E, 0, None), mx) - rout * np.clip(E - ps, 0, None), 0, None)
    return reg, np.where(np.isfinite(E), cr, np.nan)


def psid_part():
    B = pd.read_pickle(DATA / "paperA_targets_psid.pkl")
    m, CY = B["m"], B["CY"]
    del B
    S = load_eitc()
    prev = m[["pid", "year", "hlab", "wlab", "nkid", "fs", "afdc"]].drop_duplicates(["pid", "year"])
    prev = prev.rename(columns={"year": "py", "hlab": "hlab_p", "wlab": "wlab_p", "nkid": "nkid_p", "fs": "fs_p",
                                "afdc": "afdc_p"})
    c = CY[CY.year <= 2021].merge(prev, on=["pid", "py"], how="left")
    c = c[c.hrace.isin(["Black", "White"])].reset_index(drop=True)
    c["grp"] = np.select([(c.h == 1) & (c.w == 1), c.h == 1, c.w == 1], ["joint", "his alone", "hers alone"], "neither")
    Ep, Et = c.hlab_p + c.wlab_p, c.hlab + c.wlab
    c["reg_p"], c["cr_p"] = eitc(Ep, c.nkid_p, c.py.to_numpy(), S)
    c["reg_t"], c["cr_t"] = eitc(Et, c.nkid, c.year.to_numpy(), S)
    c["dcr"] = c.cr_t - c.cr_p
    c["d_earn"] = Et - Ep
    log(f"PSID: {len(c):,} couple-years; joint {int((c.grp == 'joint').sum())}, his alone "
        f"{int((c.grp == 'his alone').sum())}")
    G4 = ["neither", "his alone", "hers alone", "joint"]
    for samp, mk0 in (("all intervals 1984-2021", np.ones(len(c), bool)),
                      ("annual intervals 1984-1996", c.annual.to_numpy(bool))):
        for race in ("all", "Black", "White"):
            mk1 = mk0 & ((c.hrace == race).to_numpy() if race != "all" else True)
            for g in G4:
                q = c[mk1 & (c.grp == g).to_numpy()]
                if len(q) < 10:
                    continue
                sname = f"{samp}; {race}; {g}"
                for when, rc, cc_, fs_, af_ in (("year before", "reg_p", "cr_p", "fs_p", "afdc_p"),
                                                 ("end of interval", "reg_t", "cr_t", "fs", "afdc")):
                    ok = q[rc] != "missing"
                    for r in REG:
                        v = (q.loc[ok, rc] == r).mean()
                        add("PSID", "eitc", sname, r, f"{when}: share (%)", 100 * v,
                            100 * np.sqrt(v * (1 - v) / max(ok.sum(), 1)), int(ok.sum()))
                    add("PSID", "eitc", sname, "schedule credit (2000 $ a year)", f"{when}: share (%)",
                        q[cc_].mean(), q[cc_].std() / np.sqrt(q[cc_].notna().sum()), int(q[cc_].notna().sum()))
                    add("PSID", "eitc", sname, "food stamps / SNAP receipt (%)", f"{when}: share (%)",
                        100 * q[fs_].mean(), 100 * q[fs_].std() / np.sqrt(q[fs_].notna().sum()),
                        int(q[fs_].notna().sum()))
                    add("PSID", "eitc", sname, "AFDC / TANF receipt (%)", f"{when}: share (%)",
                        100 * q[af_].mean(), 100 * q[af_].std() / np.sqrt(max(q[af_].notna().sum(), 1)),
                        int(q[af_].notna().sum()))
                add("PSID", "eitc", sname, "couple earnings (2000 $ a year)", "year before: share (%)",
                    Ep[q.index].mean(), np.nan, len(q))
                add("PSID", "eitc", sname, "couple earnings (2000 $ a year)", "end of interval: share (%)",
                    Et[q.index].mean(), np.nan, len(q))
    # LPMs of the changes on the group dummies, calendar-year FE, 1968-family clusters
    D = pd.DataFrame({g: (c.grp == g).to_numpy(float) for g in ("his alone", "hers alone", "joint")})
    outs = {"change in the schedule credit (2000 $)": c.dcr.to_numpy(float),
            "enters phase-in or no earnings (pp)": 100 * (c.reg_t.isin(REG[:2]) & ~c.reg_p.isin(REG[:2])).to_numpy(float),
            "end of interval in phase-in or no earnings (pp)": 100 * c.reg_t.isin(REG[:2]).to_numpy(float),
            "end of interval in plateau or phase-out (pp)": 100 * c.reg_t.isin(REG[2:4]).to_numpy(float),
            "change in SNAP receipt (pp)": 100 * (c.fs - c.fs_p).to_numpy(float),
            "change in AFDC / TANF receipt (pp)": 100 * (c.afdc - c.afdc_p).to_numpy(float),
            "change in couple earnings (2000 $)": c.d_earn.to_numpy(float)}
    valid = (c.reg_p != "missing").to_numpy() & (c.reg_t != "missing").to_numpy()
    for samp, mk0 in (("all intervals 1984-2021", valid), ("annual intervals 1984-1996", valid & c.annual.to_numpy(bool))):
        for race in ("all", "Black", "White"):
            mk = mk0 & ((c.hrace == race).to_numpy() if race != "all" else True)
            for olab, y in outs.items():
                Xv = D.to_numpy()[mk]
                b, V, N, Gc = ols_cl(y[mk], Xv, [c.year.to_numpy()[mk]], c.fam68.to_numpy()[mk])
                note = f"clusters={Gc}; calendar-year FE; base = neither displaced"
                for j, g in enumerate(D.columns):
                    add("PSID", "reg", f"{samp}; {race}", g, olab, b[j], np.sqrt(V[j, j]), N, note)
                e, se = lincomb(b, V, [-1, 0, 1])
                add("PSID", "reg", f"{samp}; {race}", "joint - his alone", olab, e, se, N, note)


# =====================================================================================================
# output
# =====================================================================================================
def cellfmt(r, nd=2):
    if not np.isfinite(r.coef):
        return "-"
    if np.isfinite(r.se) and r.table in ("es", "es-bin", "reg"):
        pv = "p<0.001" if r.p < 0.001 else f"p={r.p:.3f}"
        return f"{r.coef:.{nd}f}{r.stars} ({r.se:.{nd}f}; {pv})"
    if np.isfinite(r.se):
        return f"{r.coef:.{nd}f} ({r.se:.{nd}f})"
    return f"{r.coef:.{nd}f}"


def write_md(D):
    L = ["# The safety net around a joint loss (IGE/78.SafetyNetJointLoss.py, 2026-10-20)", "",
         "SIPP 2003-2016: dual-earner couples (wife 25-59) around the husband's involuntary separation at month s = 0; "
         "'alone' = no involuntary separation of the wife in s = -3..+3, 'joint' = one in s = -3..+3; 'control' = "
         "clean pseudo-events. PSID 1984-2021 couple-years (25's intervals; both spouses worked in the earlier year). "
         "Regression cells: coefficient, stars, (cluster s.e.; p); N = observations. *** p<0.01, ** p<0.05, * p<0.1. "
         "Level cells: weighted mean (s.e.). Associations, not causal effects. Aggregates only.", ""]

    def table(sub, title, rowkey="cell", colkey="outcome", nd=2):
        if sub.empty:
            return
        L.append(f"## {title}")
        L.append("")
        for samp, g in sub.groupby("sample", sort=False):
            cols = list(dict.fromkeys(g[colkey]))
            L.append(f"*{samp}*")
            L.append("")
            L.append("| | " + " | ".join(cols) + " | N |")
            L.append("|---" * (len(cols) + 2) + "|")
            for rk, gg in g.groupby(rowkey, sort=False):
                vals = []
                for cc in cols:
                    x = gg[gg[colkey] == cc]
                    vals.append(cellfmt(x.iloc[0], nd) if len(x) else "")
                nmax = gg.n.max()
                L.append(f"| {rk} | " + " | ".join(vals) + f" | {int(nmax) if np.isfinite(nmax) else ''} |")
            notes = [x for x in g.note.unique() if isinstance(x, str) and x]
            if notes and len(notes) <= 2:
                L.append("")
                L.append("Notes: " + "; ".join(notes))
            L.append("")

    X = D[D.dataset == "SIPP"]
    table(X[X.table == "lev-bin"], "SIPP: levels by event-month bin (weighted means)")
    table(X[X.table == "es-bin"], "SIPP: event-study bins relative to s = -3..-1 (unit + calendar FE)")
    table(X[X.table == "cond"], "SIPP: couple-months s = 1..6 by employment state")
    table(X[X.table == "race"], "SIPP: levels s = 1..6 by the husband's race")
    table(X[(X.table == "lev") & (X["sample"] != "control")], "SIPP: levels by event month (figure data)")
    table(X[X.table == "es"], "SIPP: event-study coefficients by month")
    table(X[X.table == "diag"], "SIPP: coding diagnostics")
    X = D[D.dataset == "PSID"]
    table(X[X.table == "eitc"], "PSID: EITC region, credit, SNAP and AFDC/TANF before and after (couple-years)")
    table(X[X.table == "reg"], "PSID: LPMs of the changes on displacement groups (calendar-year FE)")
    (OUT / f"{TAG}.md").write_text("\n".join(L), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="sipp,psid")
    ap.add_argument("--scratch", default=str(Path(tempfile.gettempdir()) / "ige75_scratch"))
    ap.add_argument("--workers", type=int, default=2)
    a = ap.parse_args()
    scratch = Path(a.scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    assert HERE.parent not in scratch.resolve().parents, "scratch must be outside the repository"
    for part in a.only.split(","):
        ROWS.clear()
        if part == "sipp":
            sipp_part(scratch, min(a.workers, 2))
        elif part == "psid":
            psid_part()
        pd.DataFrame(ROWS).to_pickle(scratch / f"rows78_{part}.pkl")
        log(f"{part}: {len(ROWS)} rows")
    D = pd.concat([pd.read_pickle(scratch / f"rows78_{p}.pkl") for p in ("sipp", "psid")
                   if (scratch / f"rows78_{p}.pkl").exists()], ignore_index=True)
    D.to_csv(OUT / f"{TAG}.csv", index=False)
    write_md(D)
    if (D.table == "lev").any():
        plot(D, OUT / f"{TAG}.png")
    if (D.table == "es").any():
        plot_es(D, HERE / "paperA_joint_loss" / "fig_sipp_household_months.pdf")
    log(f"wrote {len(D)} rows")


if __name__ == "__main__":
    main()
