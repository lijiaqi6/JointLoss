r"""Why do married wives leave employment at ~1% a month, persistently? (2026-10-19) [Paper A; WP1 of
proposals/fable_3h_plan_paperA.md]

The CPS persistence-filtered monthly exit of wives (IGE/60 moment cps_wife_exit_p: employed at t-1 and t, unemployed
for a reason other than job loss or out of the labor force at t+1, not employed at t+2; husband employed at t, t+1)
is about 1.0% a month; the Paper A structural model produces 0.14%. This script describes the exits in three public
data sets so that the feature to add can be chosen from evidence: (a) what happens around the exit, (b) the stated
reason, (c) how long the non-employment spell lasts, and (d) whether the same wives exit repeatedly.

DATA (all read only; loaders of the source scripts imported via importlib, nothing of theirs is edited)
  CPS   30.CPSJointJobLoss.py couples panel data/cps_couples_panel.pkl (basic monthly 1994-2023; status at
        t-2..t+3 and t+12; youngest own child at t; PEIO1COW class of worker; no hours in this extract).
  SIPP  40.SIPPJointLoss.py couples panel data/sipp_couples_panel.pkl (panels 2004, 2008, 2014; reference months
        2003-2016) + the wife's job slots re-read here from the same raw core files (detailed reason the job ended:
        2004/08 ERSEND1-2, 2014 EJBk_RSEND; usual hours: 2004/08 EJBHRS, 2014 TJBk_MWKHRS; job start date: 2004/08
        TSJDATE, 2014 TJBk_STRTYR / EJBk_STRTMON / EJBk_BMONTH). The person-level job-slot extract is cached in a
        scratch folder OUTSIDE the repository (--scratch; default: the system temp folder /ige63_scratch).
  PSID  60.PaperATargets.py's cached men's panel (data/paperA_targets_psid.pkl, built by 19.men_panel: male
        heads x calendar year with wife's annual hours, his hours and labor income, youngest child in the family
        unit), data/psid_person_year.pkl (children's birth years -> births by calendar year), and the employment
        status at the interview (codes 1-8, 6 = keeping house) through 21.WifeSearch.ind_status().
COMMON SAMPLE
  Married wives aged 25-59 whose husband is employed in the base and the exit period.
  CPS / SIPP persistent exit at t+1: wife employed at t-1 and t, not employed at t+1 and t+2 (CPS: at t+1 unemployed
  for a reason other than job loss or out of the labor force, as in IGE/60; SIPP: RMESR 6-8 at t+1 and t+2, i.e. no
  job in any week of the month); husband employed at t and t+1; all four months observed. Both use the wife's weight.
  PSID annual exit: wife's annual hours > 0 in calendar year t and = 0 in t+1, same husband and wife, husband's hours
  > 0 in t and t+1; annual years only (t+1 <= 1996; the PSID is biennial afterwards), SRC + SEO, Black and White
  heads, unweighted (as in IGE/60).
ESTIMATES
  (i)   exit hazard by covariate cell with the cell's share of wife-months and of exits (shares x hazards add up to
        the pooled rate);
  (ii)  LPM of the exit on all covariates jointly (CPS: state x year-month FE, wife's weight; SIPP: panel x rotation
        x month FE, wife's weight; PSID: calendar-year FE, unweighted); s.e. clustered by household (CPS, SIPP) or
        1968 family (PSID); coefficients in percentage points;
  (iii) SIPP stated reasons for the persistent exits (detailed reason of the wife's job that ended in t+1, t, t+2
        or t-1, the first found in that order),
        by race and by the youngest child's age;
  (iv)  SIPP spell length: Kaplan-Meier probability of a return to employment within 3 / 6 / 12 / 24 months of the
        first non-employed month (censored at the end of the couple's observation), by reason and by whether a child
        aged 0 is in the household in t+1..t+9; CPS: employment 11 months after the exit month (t+12 link);
  (v)   PSID: annual exit by a birth in t+1, youngest child's age, his labor-income change, her hours and age; the
        status at the interview after the zero-hours year (keeping house, looking, retired, disabled, ...); return
        within 1, 2 and 4 years; repeat exits of the same wife;
  (vi)  persistence: does a previous exit predict the next one, controlling for the job's tenure (SIPP) / hours
        (PSID)? (persistent wife type vs a hazard of new jobs);
  (vii) steady-state arithmetic: employment share e, persistent exit x and entry n with n (1 - e) = x e.
  Associations, not causal effects. *** p<0.01, ** p<0.05, * p<0.1 (normal approximation).
OUTPUTS (aggregate only)
  output/wife_exit_why.csv  every estimate: dataset, table, sample, cell, outcome, coef, se, p, stars, n
  output/wife_exit_why.md   tables (one outcome per column, covariates as rows, samples as row panels)
Run from the repository root: .venv/Scripts/python.exe -I IGE/63.WifeExitWhy.py [--only cps,sipp,psid]
  [--scratch DIR] [--workers 6]. Each part saves its aggregate rows in the scratch folder; the outputs are written
  from all parts found there.
"""
import argparse
import importlib.util
import os
import sys
import tempfile
import time
import warnings
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import numpy as np                            # noqa: E402
import pandas as pd                           # noqa: E402
from scipy.stats import norm                  # noqa: E402

from common import DATA, OUT, stars           # noqa: E402

warnings.simplefilter("ignore", FutureWarning)
warnings.simplefilter("ignore", RuntimeWarning)
warnings.simplefilter("ignore", pd.errors.PerformanceWarning)
T0 = time.time()
SIPP_RAW = DATA / "ext" / "sipp"
ROWS = []


def log(*a):
    print(f"[{time.time() - T0:7.0f}s]", *a, flush=True)


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# =====================================================================================================
# estimators
# =====================================================================================================
def pval(b, se):
    return float(2 * norm.sf(abs(b / se))) if se > 0 else np.nan


def wmean(x, w):
    x, w = np.asarray(x, float), np.asarray(w, float)
    ok = np.isfinite(x) & np.isfinite(w)
    return float(np.sum(x[ok] * w[ok]) / np.sum(w[ok])) if ok.any() else np.nan


def wdemean(A, codes, w):
    n = codes.max() + 1
    sw = np.bincount(codes, weights=w, minlength=n)
    sw = np.where(sw > 0, sw, 1.0)
    if A.ndim == 1:
        return A - (np.bincount(codes, weights=A * w, minlength=n) / sw)[codes]
    return np.column_stack([A[:, j] - (np.bincount(codes, weights=A[:, j] * w, minlength=n) / sw)[codes]
                            for j in range(A.shape[1])])


def wlpm(y, X, w=None, fe=None, cl=None):
    """WLS of y on the columns of DataFrame X (one absorbed FE: integer codes), CR1 s.e. clustered by cl."""
    names = list(X.columns)
    Y = np.asarray(y, float)
    Xm = X.to_numpy(float)
    w = np.ones(len(Y)) if w is None else np.asarray(w, float)
    ok = np.isfinite(Y) & np.isfinite(w) & (w > 0) & np.isfinite(Xm).all(1)
    Y, Xm, w = Y[ok], Xm[ok], w[ok]
    cl = np.asarray(cl)[ok]
    ymean = float(np.sum(Y * w) / np.sum(w))
    if fe is not None:
        codes = pd.factorize(np.asarray(fe)[ok])[0]
        Y, Xm = wdemean(Y, codes, w), wdemean(Xm, codes, w)
    else:
        Xm = np.column_stack([Xm, np.ones(len(Y))])
        names = names + ["const"]
    XtX = (Xm * w[:, None]).T @ Xm
    keep = np.abs(np.diag(XtX)) > 1e-10
    Xm, names = Xm[:, keep], [n for n, k in zip(names, keep) if k]
    XtXi = np.linalg.pinv((Xm * w[:, None]).T @ Xm)
    b = XtXi @ ((Xm * w[:, None]).T @ Y)
    u = Y - Xm @ b
    N, K = Xm.shape
    g = pd.factorize(cl)[0]
    G = g.max() + 1
    S = np.column_stack([np.bincount(g, weights=Xm[:, j] * u * w, minlength=G) for j in range(K)])
    V = XtXi @ (S.T @ S) @ XtXi * (G / (G - 1)) * ((N - 1) / max(N - K, 1))
    se = np.sqrt(np.maximum(np.diag(V), 0))
    return dict(b=dict(zip(names, b)), se=dict(zip(names, se)), N=N, G=G, ymean=ymean)


def add(dataset, table, sample, cell, outcome, coef, se=np.nan, n=np.nan, note=""):
    p = pval(coef, se) if np.isfinite(se) else np.nan
    ROWS.append(dict(dataset=dataset, table=table, sample=sample, cell=cell, outcome=outcome, coef=float(coef),
                     se=float(se) if np.isfinite(se) else np.nan, p=p, stars=stars(p) if np.isfinite(p) else "",
                     n=n, note=note))


def add_reg(dataset, table, sample, outcome, r, scale=100.0, terms=None):
    for t in (terms or [k for k in r["b"] if k != "const"]):
        if t in r["b"]:
            add(dataset, table, sample, t, outcome, r["b"][t] * scale, r["se"][t] * scale, r["N"],
                note=f"clusters={r['G']}; mean={r['ymean'] * scale:.3f}")


def decompose(dataset, sample, y, w, cells, outcome="exit hazard (%)"):
    """(i) hazard by cell + share of wife-months + share of exits; cells: dict name -> array of labels."""
    y, w = np.asarray(y, float), np.asarray(w, float)
    w = np.where(np.isfinite(w) & np.isfinite(y), w, 0.0)
    tot = wmean(y, w)
    add(dataset, "i", sample, "all", outcome, 100 * tot, np.nan, len(y))
    for dim, lab in cells.items():
        lab = np.asarray(lab).astype(str)
        W = w.sum()
        for c in pd.unique(lab):
            mk = lab == c
            if mk.sum() < 30:
                continue
            h = wmean(y[mk], w[mk])
            sh = w[mk].sum() / W
            # s.e. of the hazard: binomial with Kish effective n
            neff = w[mk].sum() ** 2 / np.sum(w[mk] ** 2)
            se = np.sqrt(h * (1 - h) / neff)
            add(dataset, "i", sample, f"{dim}: {c}", outcome, 100 * h, 100 * se, int(mk.sum()))
            add(dataset, "i", sample, f"{dim}: {c}", "share of wife-months (%)", 100 * sh, np.nan, int(mk.sum()))
            add(dataset, "i", sample, f"{dim}: {c}", "share of exits (%)", 100 * sh * h / tot, np.nan, int(mk.sum()))
    return tot


def dummies(lab, prefix, base):
    lab = pd.Series(np.asarray(lab).astype(str))
    D = pd.get_dummies(lab, prefix=prefix, prefix_sep=": ", dtype=float)
    return D.drop(columns=[f"{prefix}: {base}"], errors="ignore")


def km(status, w, H):
    """Weighted Kaplan-Meier of the first return to employment. status: n x H array (1 employed, 0 not, nan unobs.)
    for months s = 1..H after the first non-employed month. Returns 1 - S(s), s = 1..H, and the at-risk counts."""
    n = status.shape[0]
    alive = np.ones(n, bool)
    S, out, risk = 1.0, [], []
    for s in range(H):
        st = status[:, s]
        obs = alive & np.isfinite(st)
        ev = obs & (st == 1)
        den = w[obs].sum()
        h = w[ev].sum() / den if den > 0 else 0.0
        S *= (1 - h)
        out.append(1 - S)
        risk.append(int(obs.sum()))
        alive = obs & ~ev                           # censored at the first unobserved month
    return np.array(out), np.array(risk)


def km_se(status, w, H, cl, reps=100, seed=63):
    """Cluster bootstrap s.e. of the KM return probabilities."""
    rng = np.random.default_rng(seed)
    g, gu = pd.factorize(cl)
    G = len(gu)
    draws = []
    for _ in range(reps):
        cnt = np.bincount(rng.integers(0, G, G), minlength=G)
        ww = w * cnt[g]
        draws.append(km(status, ww, H)[0])
    return np.std(np.array(draws), axis=0, ddof=1)


def age_lab(a):
    a = np.asarray(a, float)
    return np.select([a < 30, a < 35, a < 40, a < 45, a < 50, a < 55], ["25-29", "30-34", "35-39", "40-44", "45-49",
                                                                      "50-54"], "55-59")


def kid_lab(yk, none_val):
    yk = np.asarray(yk, float)
    return np.select([~np.isfinite(yk) | (yk == none_val), yk == 0, yk <= 2, yk <= 5, yk <= 12],
                     ["none <18", "0", "1-2", "3-5", "6-12"], "13-17")


# =====================================================================================================
# CPS
# =====================================================================================================
def cps_part():
    m30 = _load("cps30", "30.CPSJointJobLoss.py")
    log("CPS: loading panel")
    P = m30.add_vars(m30.build_panel())
    P.attrs = {}
    hs = (P.h_s == 1) & (P["h_s+1"] == 1)
    obs = (P["w_s-1"] >= 1) & (P["w_s+1"] >= 1) & (P["w_s+2"] >= 1)
    ne = [2, 3, 4]
    age = P.w_age.between(25, 59)
    # employment share and persistent entry for the steady state (same filters)
    b_all = (P.h_s == 1) & age & (P.w_s >= 1)
    e_rate = wmean((P.w_s[b_all] == 1).to_numpy(float), P.w[b_all])
    add("CPS", "vii", "wives 25-59, husband employed", "all", "employment share (%)", 100 * e_rate, np.nan,
        int(b_all.sum()))
    b = hs & obs & age & P["w_s-1"].isin(ne) & P.w_s.isin(ne)
    d = P.loc[b]
    yen = ((d["w_s+1"] == 1) & (d["w_s+2"] == 1)).to_numpy(float)
    add("CPS", "vii", "wives 25-59, husband employed", "all", "persistent monthly entry (%)",
        100 * wmean(yen, d.w), np.nan, len(d))
    for r in ("Black", "White"):
        mk = (d.rgrp == r).to_numpy()
        add("CPS", "vii", "wives 25-59, husband employed", f"race: {r}", "persistent monthly entry (%)",
            100 * wmean(yen[mk], d.w[mk]), np.nan, int(mk.sum()))
    # exit sample (IGE/60 definition, wives 25-59)
    b = hs & obs & age & (P["w_s-1"] == 1) & (P.w_s == 1)
    keep = ["hh", "sm", "t", "mis", "w", "rgrp", "w_age", "h_age", "w_edg", "h_edg", "ykid", "nkid", "w_cow",
            "period", "w_s+1", "w_s+2", "w_s+3", "w_s+12", "w_unt+1", "h_s+12"]
    d = P.loc[b, keep].copy()
    del P
    d["y"] = (d["w_s+1"].isin([3, 4]) & d["w_s+2"].isin(ne)).astype(float)
    log(f"CPS: {len(d):,} wife-months, persistent exit {100 * wmean(d.y, d.w):.3f}%")
    add("CPS", "vii", "wives 25-59, husband employed", "all", "persistent monthly exit (%)", 100 * wmean(d.y, d.w),
        np.nan, len(d))
    # destination of the exit
    ex = d.y == 1
    dest = np.select([d["w_s+1"] == 4, d["w_unt+1"] == 4, d["w_unt+1"] == 5, d["w_unt+1"] == 6],
                     ["out of the labor force", "unemployed: job leaver", "unemployed: re-entrant",
                      "unemployed: new entrant"], "unemployed: other")
    for c in pd.unique(dest[ex.to_numpy()]):
        mk = ex.to_numpy() & (dest == c)
        add("CPS", "i", "persistent exits", f"destination at t+1: {c}", "share of exits (%)",
            100 * d.w[mk].sum() / d.w[ex].sum(), np.nan, int(mk.sum()))
    cells = {
        "youngest child": kid_lab(d.ykid, -1),
        "wife's age": age_lab(d.w_age),
        "race (husband)": d.rgrp.to_numpy(),
        "wife's education": np.array(["< high school", "high school", "some college", "BA+"])[d.w_edg.to_numpy()],
        "class of worker": np.select([d.w_cow.isin([1, 2, 3]), d.w_cow.isin([4, 5]), d.w_cow.isin([6, 7])],
                                     ["government", "private", "self-employed"], "unknown"),
        "period": d.period.to_numpy(),
    }
    tot = decompose("CPS", "wives 25-59, husband employed (persistent exit)", d.y, d.w, cells)
    # LPM jointly, state x year-month FE
    X = pd.concat([dummies(cells["youngest child"], "youngest child", "none <18"),
                   dummies(cells["wife's age"], "wife's age", "35-39"),
                   dummies(cells["race (husband)"], "race (husband)", "White"),
                   dummies(cells["wife's education"], "wife's education", "high school"),
                   dummies(cells["class of worker"], "class of worker", "private"),
                   dummies(np.array(["< high school", "high school", "some college", "BA+"])[d.h_edg.to_numpy()],
                           "husband's education", "high school")], axis=1)
    r = wlpm(d.y.to_numpy(), X, d.w.to_numpy(), fe=d.sm.to_numpy(), cl=d.hh.to_numpy())
    add_reg("CPS", "ii", "wives 25-59, husband employed (state x year-month FE)", "persistent exit (pp)", r)
    # churn: status 11 months after the exit month (t+12 link; t+3 is outside the rotation spell for persistent exits)
    for k, lab in (("w_s+12", "employed at t+12 (11 months after the exit month)"),):
        ob = d[k] >= 1
        for grp, mk in (("exiters", ex & ob), ("stayers (no exit at t+1)", (~ex) & ob)):
            yy = (d.loc[mk, k] == 1).to_numpy(float)
            v = wmean(yy, d.w[mk])
            neff = d.w[mk].sum() ** 2 / np.sum(d.w[mk] ** 2)
            add("CPS", "iv", grp, "all", lab + " (%)", 100 * v, 100 * np.sqrt(v * (1 - v) / neff), int(mk.sum()))
        # by youngest child among exiters
        for c in ("0", "1-2", "3-5", "6-12", "13-17", "none <18"):
            mk = ex & ob & (cells["youngest child"] == c)
            if mk.sum() >= 30:
                yy = (d.loc[mk, k] == 1).to_numpy(float)
                v = wmean(yy, d.w[mk])
                neff = d.w[mk].sum() ** 2 / np.sum(d.w[mk] ** 2)
                add("CPS", "iv", "exiters", f"youngest child: {c}", lab + " (%)", 100 * v,
                    100 * np.sqrt(v * (1 - v) / neff), int(mk.sum()))
    # LPM: return by t+12 among exiters on cells (infant vs not)
    mk = (ex & (d["w_s+12"] >= 1)).to_numpy()
    if mk.sum() > 200:
        dd = d.loc[mk]
        y12 = (dd["w_s+12"] == 1).to_numpy(float)
        X2 = pd.concat([dummies(cells["youngest child"][mk], "youngest child", "none <18"),
                        dummies(cells["wife's age"][mk], "wife's age", "35-39"),
                        dummies(cells["race (husband)"][mk], "race (husband)", "White")], axis=1)
        r = wlpm(y12, X2, dd.w.to_numpy(), fe=dd.period.to_numpy(), cl=dd.hh.to_numpy())
        add_reg("CPS", "iv", "exiters with a t+12 link (period FE)", "employed at t+12 (pp)", r)
    return tot


# =====================================================================================================
# SIPP: wife's job slots re-read from the raw core files (scratch cache outside the repository)
# =====================================================================================================
# common detailed reason codes
RSD = {1: "layoff / slack work / position abolished", 2: "plant closed / employer bankrupt or sold",
       3: "discharged / fired", 4: "temporary job ended", 5: "other involuntary (2014)", 6: "quit to take another job",
       7: "retirement / old age", 8: "childcare problems", 9: "other family / personal obligations",
       10: "own illness / injury", 11: "school / training", 12: "unsatisfactory work arrangements",
       13: "quit for another reason / other personal"}
MAP0408 = {1: 1, 13: 1, 9: 2, 10: 2, 8: 3, 11: 4, 12: 6, 2: 7, 3: 8, 4: 9, 5: 10, 6: 10, 7: 11, 14: 12, 15: 13}
MAP14 = {1: 2, 2: 1, 3: 1, 4: 4, 5: 3, 6: 5, 7: 6, 8: 12, 9: 13, 10: 7, 11: 8, 12: 9, 13: 10, 14: 10, 15: 11, 16: 13}
RGROUP = {1: "involuntary", 2: "involuntary", 3: "involuntary", 4: "involuntary", 5: "involuntary",
          6: "quit to another job", 7: "retirement", 8: "childcare / family", 9: "childcare / family",
          10: "own illness / injury", 11: "school", 12: "unsatisfactory arrangements / other quit",
          13: "unsatisfactory arrangements / other quit"}


def _n(d, c):
    if c not in d:
        return np.full(len(d), -1, dtype=np.int64)
    return pd.to_numeric(d[c], errors="coerce").fillna(-1).astype(np.int64).to_numpy()


def slot_extract(args):
    """One raw wave -> long table of the married women's job slots held or ended in each month (person-level:
    written only to the scratch folder)."""
    panel, w, raw, out = args
    out = Path(out)
    if out.exists():
        return str(out)
    if panel == 2014:
        base = ["SSUID", "PNUM", "SWAVE", "MONTHCODE", "ESEX", "EMS_EHC", "TAGE_EHC"]
        slot = ["EJB{j}_JOBID", "EJB{j}_BMONTH", "EJB{j}_EMONTH", "EJB{j}_RSEND", "EJB{j}_JBORSE", "TJB{j}_MWKHRS",
                "TJB{j}_STRTYR", "EJB{j}_STRTMON", "EJB{j}_STRTJAN"]
        js = range(1, 8)
    else:
        base = ["ssuid", "epppnum", "rhcalyr", "rhcalmn", "esex", "ems", "tage"]
        slot = ["eeno{j}", "tsjdate{j}", "tejdate{j}", "ersend{j}", "ejbhrs{j}"]
        js = (1, 2)
    want = set(base) | {s.format(j=j) for s in slot for j in js}
    kw = dict(usecols=lambda c: (c if panel == 2014 else c.lower()) in want, chunksize=60000, dtype=str,
              low_memory=False)
    if panel == 2014:
        import gzip
        with gzip.open(raw, "rt") as fh:
            head = fh.readline()
        kw["sep"] = "|" if head.count("|") > head.count(",") else ","
    parts = []
    for d in pd.read_csv(raw, **kw):
        if panel != 2014:
            d.columns = [c.lower() for c in d.columns]
        sex = _n(d, base[4])
        ms = _n(d, base[5])
        age = _n(d, base[6])
        keepr = (sex == 2) & (ms == 1) & (age >= 20) & (age <= 62)
        d = d[keepr]
        if not len(d):
            continue
        if panel == 2014:
            ssuid = d["SSUID"].astype(str).str.strip().to_numpy()
            pnum = _n(d, "PNUM")
            year = 2012 + _n(d, "SWAVE")
            month = _n(d, "MONTHCODE")
        else:
            ssuid = d["ssuid"].astype(str).str.strip().str.lstrip("0").to_numpy()
            pnum = _n(d, "epppnum")
            year, month = _n(d, "rhcalyr"), _n(d, "rhcalmn")
        ym = year * 12 + month - 1
        for j in js:
            if panel == 2014:
                jid, bm, em = _n(d, f"EJB{j}_JOBID"), _n(d, f"EJB{j}_BMONTH"), _n(d, f"EJB{j}_EMONTH")
                rsr, jb = _n(d, f"EJB{j}_RSEND"), _n(d, f"EJB{j}_JBORSE")
                hrs = _n(d, f"TJB{j}_MWKHRS")
                sy, smn, sjan = _n(d, f"TJB{j}_STRTYR"), _n(d, f"EJB{j}_STRTMON"), _n(d, f"EJB{j}_STRTJAN")
                present = (jid > 0) & (jb == 1) & (bm > 0) & (em > 0)
                held = present & (bm <= month) & (month <= em)
                end = present & (em == month) & (rsr > 0)
                rsd = np.where(end, pd.Series(rsr).map(MAP14).fillna(0).astype(int).to_numpy(), 0)
                st_before = np.where((sjan == 2) & (sy > 1900), sy * 12 + np.where(smn > 0, smn, 7) - 1, -1)
                st_in = np.where(bm > 0, year * 12 + bm - 1, -1)
                start = np.where(st_before > 0, st_before, st_in)
            else:
                jid, sj, ej, rsr = _n(d, f"eeno{j}"), _n(d, f"tsjdate{j}"), _n(d, f"tejdate{j}"), _n(d, f"ersend{j}")
                hrs = _n(d, f"ejbhrs{j}")
                yyyymm = year * 100 + month
                present = jid > 0
                held = present & ((sj <= 0) | (sj <= yyyymm * 100 + 31)) & ((ej <= 0) | (ej >= yyyymm * 100 + 1))
                end = present & (ej > 0) & (ej // 100 == yyyymm)
                rsd = np.where(end, pd.Series(rsr).map(MAP0408).fillna(0).astype(int).to_numpy(), 0)
                start = np.where(sj > 19000000, (sj // 10000) * 12 + (sj // 100) % 100 - 1, -1)
            mk = held | end
            if mk.any():
                parts.append(pd.DataFrame({"panel": panel, "ssuid": ssuid[mk], "pnum": pnum[mk].astype(np.int32),
                                           "ym": ym[mk].astype(np.int32), "jid": jid[mk].astype(np.int32),
                                           "held": held[mk].astype(np.int8), "end": end[mk].astype(np.int8),
                                           "rsd": rsd[mk].astype(np.int8), "hrs": hrs[mk].astype(np.int16),
                                           "start": start[mk].astype(np.int32)}))
    res = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame()
    res.to_pickle(out)
    return str(out)


def sipp_slots(scratch, workers):
    m40 = _load("sipp40", "40.SIPPJointLoss.py")
    sd = scratch / "sipp_slots"
    sd.mkdir(parents=True, exist_ok=True)
    jobs = []
    for panel, nw in m40.PANELS.items():
        for w in range(1, nw + 1):
            raw = m40.src(panel, w)[1]
            if raw.exists():
                jobs.append((panel, w, str(raw), str(sd / f"slots_{panel}_{w:02d}.pkl")))
    log(f"SIPP: extracting job slots from {len(jobs)} waves with {workers} workers")
    with ProcessPoolExecutor(max_workers=workers) as ex:
        files = list(ex.map(slot_extract, jobs))
    S = pd.concat([pd.read_pickle(f) for f in files], ignore_index=True)
    S = S.drop_duplicates(["panel", "ssuid", "pnum", "ym", "jid"])
    # job start: earliest start reported for the person x employer across waves; else first month seen held
    S["start"] = S["start"].where(S["start"] > 0)
    first_seen = S[S.held == 1].groupby(["panel", "ssuid", "pnum", "jid"])["ym"].min().rename("first_seen")
    st = S.groupby(["panel", "ssuid", "pnum", "jid"])["start"].min()
    S = S.merge(st.rename("start_m"), on=["panel", "ssuid", "pnum", "jid"], how="left")
    S = S.merge(first_seen, on=["panel", "ssuid", "pnum", "jid"], how="left")
    S["start_m"] = S["start_m"].fillna(S["first_seen"])
    H = S[S.held == 1].copy()
    H["hrs"] = H["hrs"].where(H["hrs"] > 0)
    H = H.sort_values(["panel", "ssuid", "pnum", "ym", "hrs"], ascending=[True, True, True, True, False])
    M = H.drop_duplicates(["panel", "ssuid", "pnum", "ym"])[["panel", "ssuid", "pnum", "ym", "hrs", "start_m", "jid"]]
    M["tenure"] = M["ym"] - M["start_m"]
    tot_h = H.groupby(["panel", "ssuid", "pnum", "ym"])["hrs"].sum(min_count=1).rename("hrs_tot")
    M = M.merge(tot_h, on=["panel", "ssuid", "pnum", "ym"], how="left")
    E = S[(S.end == 1) & (S.rsd > 0)].sort_values(["panel", "ssuid", "pnum", "ym", "rsd"])
    E = E.drop_duplicates(["panel", "ssuid", "pnum", "ym"])[["panel", "ssuid", "pnum", "ym", "rsd"]]
    out = M.merge(E, on=["panel", "ssuid", "pnum", "ym"], how="outer")
    return out


def sipp_part(scratch, workers):
    m40 = _load("sipp40", "40.SIPPJointLoss.py")
    cache = scratch / "sipp_wife_jobs.pkl"
    if cache.exists():
        J = pd.read_pickle(cache)
    else:
        J = sipp_slots(scratch, workers)
        J.to_pickle(cache)
    log(f"SIPP: {len(J):,} wife job-months from the slots")
    P = m40.build_panel()
    P, L = m40.add_vars(P)
    J = J.rename(columns={"pnum": "pnum_w"})
    J["ssuid"] = J["ssuid"].astype(str)
    P["ssuid"] = P["ssuid"].astype(str)
    P = P.merge(J, on=["panel", "ssuid", "pnum_w", "ym"], how="left")
    assert P.duplicated(["cid", "ym"]).sum() == 0
    L = m40.Look(P)
    for c in ("hrs", "tenure", "rsd", "SEP_h", "INV_w", "yc"):
        P[c] = P[c].astype(float)
    E = {k: L.at("E_w", k) for k in range(-1, 3)}
    Eh = {k: L.at("E_h", k) for k in (0, 1)}
    age = P.age_w.between(25, 59).to_numpy()
    base = (E[-1] == 1) & (E[0] == 1) & (Eh[0] == 1) & (Eh[1] == 1) & np.isfinite(E[1]) & np.isfinite(E[2]) & age
    y = ((E[1] == 0) & (E[2] == 0)).astype(float)
    # reason: detailed reason of a job of the wife ending at t+1, t, t+2 or t-1 (first found in that order; the job
    # that ends in the exit month t+1 or the last employed month t, allowing one month of dating error)
    rsd = np.zeros(len(P), int)
    for k in (1, 0, 2, -1):
        rk = np.nan_to_num(L.at("rsd", k)).astype(int)
        rsd = np.where((rsd == 0) & (rk > 0), rk, rsd)
    inv = np.isin(rsd, [1, 2, 3, 4, 5]) | ((np.nan_to_num(L.at("INV_w", 1)) + np.nan_to_num(L.at("INV_w", 0))) > 0)
    # child aged 0 in the household at some month t+1..t+9 (births from ~11 months before to 9 months after)
    inf_win = np.zeros(len(P), bool)
    for k in range(1, 10):
        inf_win |= (L.at("yc", k) == 0)
    # husband's job change around the exit: a separation of his at t-2..t+1 (he stays employed at t, t+1)
    hsep = np.zeros(len(P), bool)
    for k in (-2, -1, 0, 1):
        hsep |= (np.nan_to_num(L.at("SEP_h", k)) > 0)
    # previous persistent exit of the same wife within the panel (any earlier month)
    yall = np.where(base, y, 0.0)
    P["_ex"] = yall
    P["_prev"] = P.groupby("cid")["_ex"].cumsum() - P["_ex"]
    prev = (P["_prev"].to_numpy() > 0)
    d = P.loc[base].copy()
    d["y"] = y[base]
    d["rsd_x"] = rsd[base]
    d["inv_x"] = inv[base]
    d["inf_win"] = inf_win[base]
    d["hsep"] = hsep[base]
    d["prev_exit"] = prev[base]
    w = np.nan_to_num(d.wgt_w.to_numpy(float))
    log(f"SIPP: {len(d):,} wife-months, persistent exit {100 * wmean(d.y, w):.3f}%")
    add("SIPP", "vii", "wives 25-59, husband employed", "all", "persistent monthly exit, all reasons (%)",
        100 * wmean(d.y, w), np.nan, len(d))
    ynv = (d.y.to_numpy() == 1) & ~d.inv_x.to_numpy()
    add("SIPP", "vii", "wives 25-59, husband employed", "all",
        "persistent monthly exit, no involuntary separation (%)", 100 * wmean(ynv, w), np.nan, len(d))
    bE = (L.at("E_h", 0) == 1) & age & np.isfinite(P.E_w.to_numpy(float))
    add("SIPP", "vii", "wives 25-59, husband employed", "all", "employment share (%)",
        100 * wmean(P.E_w.to_numpy(float)[bE], P.wgt_w.to_numpy(float)[bE]), np.nan, int(bE.sum()))
    bN = (E[-1] == 0) & (E[0] == 0) & (Eh[0] == 1) & (Eh[1] == 1) & np.isfinite(E[1]) & np.isfinite(E[2]) & age
    yN = ((E[1] == 1) & (E[2] == 1)).astype(float)
    add("SIPP", "vii", "wives 25-59, husband employed", "all", "persistent monthly entry (%)",
        100 * wmean(yN[bN], P.wgt_w.to_numpy(float)[bN]), np.nan, int(bN.sum()))
    hrs = d.hrs_tot.to_numpy(float)
    ten = d.tenure.to_numpy(float)
    cells = {
        "youngest child": kid_lab(d.yc, -99),
        "child aged 0 in t+1..t+9": np.where(d.inf_win, "yes", "no"),
        "wife's age": age_lab(d.age_w),
        "race (husband)": np.select([d.race_h == 2, d.race_h == 1], ["Black", "White"], "Other"),
        "wife's education": np.select([d.educ_w <= 1, d.educ_w == 2, d.educ_w == 3], ["< high school",
                                       "high school", "some college"], "BA+"),
        "usual hours (all jobs)": np.select([~np.isfinite(hrs), hrs < 20, hrs < 35], ["unknown", "< 20", "20-34"],
                                            "35+"),
        "job tenure (months)": np.select([~np.isfinite(ten) | (ten < 0), ten < 6, ten < 12, ten < 36],
                                         ["unknown", "0-5", "6-11", "12-35"], "36+"),
        "husband's job change t-2..t+1": np.where(d.hsep, "yes", "no"),
        "previous persistent exit in panel": np.where(d.prev_exit, "yes", "no"),
        "panel": d.panel.astype(str).to_numpy(),
    }
    decompose("SIPP", "wives 25-59, husband employed (persistent exit)", d.y, w, cells)
    X = pd.concat([dummies(cells["youngest child"], "youngest child", "none <18"),
                   dummies(cells["child aged 0 in t+1..t+9"], "child aged 0 in t+1..t+9", "no"),
                   dummies(cells["wife's age"], "wife's age", "35-39"),
                   dummies(cells["race (husband)"], "race (husband)", "White"),
                   dummies(cells["wife's education"], "wife's education", "high school"),
                   dummies(cells["usual hours (all jobs)"], "usual hours (all jobs)", "35+"),
                   dummies(cells["job tenure (months)"], "job tenure (months)", "36+"),
                   dummies(cells["husband's job change t-2..t+1"], "husband's job change t-2..t+1", "no")], axis=1)
    for yy, lab in ((d.y.to_numpy(float), "persistent exit (pp)"), (ynv.astype(float), "persistent exit, no "
                                                                    "involuntary separation (pp)")):
        r = wlpm(yy, X, w, fe=d.pm.to_numpy(), cl=d.hh.to_numpy())
        add_reg("SIPP", "ii", "wives 25-59, husband employed (panel x rotation x month FE)", lab, r)
    # (vi) persistence: previous exit, with and without tenure / hours controls
    Xp = pd.concat([dummies(cells["previous persistent exit in panel"], "previous persistent exit in panel", "no"),
                    X.drop(columns=[c for c in X.columns if c.startswith(("job tenure", "usual hours"))])], axis=1)
    r = wlpm(d.y.to_numpy(float), Xp, w, fe=d.pm.to_numpy(), cl=d.hh.to_numpy())
    add_reg("SIPP", "vi", "persistence, no tenure / hours controls", "persistent exit (pp)", r,
            terms=["previous persistent exit in panel: yes"])
    Xp2 = pd.concat([dummies(cells["previous persistent exit in panel"], "previous persistent exit in panel", "no"), X],
                    axis=1)
    r = wlpm(d.y.to_numpy(float), Xp2, w, fe=d.pm.to_numpy(), cl=d.hh.to_numpy())
    add_reg("SIPP", "vi", "persistence, with tenure and hours controls", "persistent exit (pp)", r,
            terms=["previous persistent exit in panel: yes"] + [c for c in X.columns if c.startswith("job tenure")])
    # (iii) reasons among persistent exits
    ex = d.y.to_numpy() == 1
    rs = d.rsd_x.to_numpy()
    rlab = np.array([RSD.get(int(k), "no job end recorded in t-1..t+2") for k in rs])
    rgrp = np.array([RGROUP.get(int(k), "no job end recorded") for k in rs])
    subs = {"all": np.ones(len(d), bool),
            "race: Black": cells["race (husband)"] == "Black", "race: White": cells["race (husband)"] == "White",
            "youngest child 0-2": np.isin(cells["youngest child"], ["0", "1-2"]),
            "youngest child 3-5": cells["youngest child"] == "3-5",
            "youngest child 6-17": np.isin(cells["youngest child"], ["6-12", "13-17"]),
            "no child <18": cells["youngest child"] == "none <18",
            "child aged 0 in t+1..t+9": d.inf_win.to_numpy(),
            "wife 55-59": cells["wife's age"] == "55-59"}
    for sname, smk in subs.items():
        mk = ex & smk
        if mk.sum() < 20:
            continue
        for labs, tab in ((rgrp, "iii-group"), (rlab, "iii-detail")):
            for c in pd.unique(labs[mk]):
                m2 = mk & (labs == c)
                v = w[m2].sum() / w[mk].sum()
                neff = w[mk].sum() ** 2 / np.sum(w[mk] ** 2)
                add("SIPP", tab, f"persistent exits: {sname}", c, "share of exits (%)", 100 * v,
                    100 * np.sqrt(v * (1 - v) / neff), int(m2.sum()))
    # (iv) spell length: KM of the return to employment after the first non-employed month (t+1)
    H = 36
    st = np.column_stack([L.at("E_w", 1 + s) for s in range(1, H + 1)])[base][ex]
    we, cle = w[ex], d.hh.to_numpy()[ex]
    groups = {"all": np.ones(ex.sum(), bool),
              "child aged 0 in t+1..t+9": d.inf_win.to_numpy()[ex],
              "no child aged 0 in t+1..t+9": ~d.inf_win.to_numpy()[ex],
              "race: Black": cells["race (husband)"][ex] == "Black",
              "race: White": cells["race (husband)"][ex] == "White",
              "tenure 0-11 months": np.isin(cells["job tenure (months)"][ex], ["0-5", "6-11"]),
              "tenure 12+ months": np.isin(cells["job tenure (months)"][ex], ["12-35", "36+"]),
              "previous exit in panel": d.prev_exit.to_numpy()[ex]}
    for g in pd.unique(rgrp[ex]):
        groups[f"reason: {g}"] = rgrp[ex] == g
    for g, mk in groups.items():
        if mk.sum() < 30:
            continue
        ret, risk = km(st[mk], we[mk], H)
        se = km_se(st[mk], we[mk], H, cle[mk], reps=100)
        for h in (3, 6, 12, 24):
            add("SIPP", "iv", f"persistent exits: {g}", f"return within {h} months", "KM probability (%)",
                100 * ret[h - 1], 100 * se[h - 1], int(mk.sum()), note=f"at risk at month {h}: {risk[h - 1]}")
    # LPM of the return within 12 months among exits with 12 months observed (no censoring), on cells
    obs12 = np.isfinite(st[:, :12]).all(1)
    if obs12.sum() > 200:
        ret12 = (np.nan_to_num(st[:, :12]) == 1).any(1).astype(float)
        dd = d.loc[ex]
        X3 = pd.concat([dummies(rgrp[ex], "reason", "childcare / family"),
                        dummies(cells["child aged 0 in t+1..t+9"][ex], "child aged 0 in t+1..t+9", "no"),
                        dummies(cells["race (husband)"][ex], "race (husband)", "White"),
                        dummies(cells["wife's age"][ex], "wife's age", "35-39"),
                        dummies(cells["job tenure (months)"][ex], "job tenure (months)", "36+")], axis=1)
        X3 = X3.reset_index(drop=True)
        r = wlpm(ret12[obs12], X3[obs12], we[obs12], fe=dd.panel.to_numpy()[obs12], cl=cle[obs12])
        add_reg("SIPP", "iv", "persistent exits observed 12 months after (panel FE)", "returned within 12 months (pp)",
                r)


# =====================================================================================================
# PSID
# =====================================================================================================
def psid_part():
    cache = DATA / "paperA_targets_psid.pkl"
    if cache.exists():
        m = pd.read_pickle(cache)["m"]
    else:
        m19 = _load("fd19", "19.FatherDisplacement.py")
        m = m19.men_panel(pd.read_pickle(DATA / "psid_person_year.pkl"), m19.psid9.family())
        m = m.merge(pd.read_pickle(DATA / "psid_person_year.pkl").query("wife")[["wave", "int", "age"]]
                    .drop_duplicates(["wave", "int"]).rename(columns={"age": "w_age"}), on=["wave", "int"], how="left")
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    # births by calendar year: a child in the family unit at wave y+1 born in y (or y+1 before the interview)
    k = py[py["child"] & py["birth_year"].notna()][["wave", "int", "birth_year"]]
    by = k.assign(b=1).groupby(["wave", "int", "birth_year"])["b"].max().reset_index()
    m = m[m.w_pid.notna()].copy()
    m["w_pid"] = m["w_pid"].astype(np.int64)
    bt = by[by.birth_year == by.wave - 1][["wave", "int"]].drop_duplicates().assign(birth_t=1)
    m = m.merge(bt, on=["wave", "int"], how="left")
    m["birth_t"] = m["birth_t"].fillna(0)
    log("PSID: reading interview status (21.ind_status)")
    m21 = _load("ws21", "21.WifeSearch.py")
    S = m21.ind_status()
    m = m.sort_values(["pid", "year"])
    nxt = m[["pid", "year", "w_pid", "wh", "hh", "hlab", "birth_t", "youngest", "wave"]].copy()
    cols = {}
    for k_ in (1, 2, 3, 4, 5):
        z = nxt.copy()
        z["year"] = z["year"] - k_
        z = z.rename(columns={c: f"{c}_p{k_}" for c in ("w_pid", "wh", "hh", "hlab", "birth_t", "youngest", "wave")})
        cols[k_] = z
    q = m.copy()
    for k_ in (1, 2, 3, 4, 5):
        q = q.merge(cols[k_], on=["pid", "year"], how="left")
    # annual years only: t+1 <= 1996
    q = q[(q.year >= 1968) & (q.year + 1 <= 1996)]
    same1 = q.w_pid_p1 == q.w_pid
    base = (q.wh > 0) & same1 & (q.hh > 0) & (q.hh_p1 > 0) & q.w_age.between(25, 59) & q.wh_p1.notna()
    d = q[base].copy()
    d["y"] = (d.wh_p1 == 0).astype(float)
    log(f"PSID: {len(d):,} wife-years, annual exit {100 * d.y.mean():.2f}%")
    add("PSID", "vii", "wives 25-59, husband working both years (annual years 1968-1996)", "all",
        "annual exit: hours > 0 in t, 0 in t+1 (%)", 100 * d.y.mean(), np.nan, len(d))
    dl = np.log(d.hlab_p1.clip(lower=1)) - np.log(d.hlab.clip(lower=1))
    dl = np.where((d.hlab > 0) & (d.hlab_p1 > 0), dl, np.nan)
    cells = {
        "birth in t+1": np.where(d.birth_t_p1 == 1, "yes", "no"),
        "birth in t": np.where(d.birth_t == 1, "yes", "no"),
        "youngest child (interview of t+1)": kid_lab(d.youngest, -99),
        "her hours in t": np.select([d.wh < 500, d.wh < 1000, d.wh < 1750], ["1-499", "500-999", "1000-1749"],
                                    "1750+"),
        "his labor income t -> t+1": np.select([~np.isfinite(dl), dl < -0.25, dl > 0.25], ["zero / missing",
                                                "fall > 25%", "rise > 25%"], "within +-25%"),
        "wife's age": age_lab(d.w_age),
        "race (head)": d.hrace.to_numpy(),
        "decade": np.select([d.year < 1980, d.year < 1990], ["1968-79", "1980-89"], "1990-95"),
    }
    decompose("PSID", "wives 25-59, husband working (annual exit)", d.y, np.ones(len(d)), cells,
              outcome="annual exit (%)")
    X = pd.concat([dummies(cells["birth in t+1"], "birth in t+1", "no"),
                   dummies(cells["birth in t"], "birth in t", "no"),
                   dummies(cells["youngest child (interview of t+1)"], "youngest child (interview of t+1)", "none <18"),
                   dummies(cells["her hours in t"], "her hours in t", "1750+"),
                   dummies(cells["his labor income t -> t+1"], "his labor income t -> t+1", "within +-25%"),
                   dummies(cells["wife's age"], "wife's age", "35-39"),
                   dummies(cells["race (head)"], "race (head)", "White")], axis=1)
    X.index = d.index
    r = wlpm(d.y.to_numpy(), X.reset_index(drop=True), None, fe=d.year.to_numpy(), cl=d.fam68.to_numpy())
    add_reg("PSID", "ii", "wives 25-59, husband working (calendar-year FE)", "annual exit (pp)", r)
    # continuous income change
    okc = np.isfinite(dl)
    Xc = pd.concat([pd.DataFrame({"d log his labor income (x0.1)": np.clip(dl, -1.5, 1.5) * 10}),
                    X.drop(columns=[c for c in X.columns if c.startswith("his labor")]).reset_index(drop=True)], axis=1)
    r = wlpm(d.y.to_numpy()[okc], Xc[okc], None, fe=d.year.to_numpy()[okc], cl=d.fam68.to_numpy()[okc])
    add_reg("PSID", "ii", "husband's labor income > 0 in t and t+1 (calendar-year FE)", "annual exit (pp)", r,
            terms=["d log his labor income (x0.1)"])
    # status at the interview after the zero-hours year (wave t+2): codes 1-8
    ex = d.y.to_numpy() == 1
    wpid = d.w_pid.to_numpy(np.int64)
    st = S.reindex(pd.MultiIndex.from_arrays([wpid, (d.year + 2).to_numpy(np.int64)])).to_numpy()
    SL = {1: "working", 2: "temporarily laid off", 3: "looking for work / unemployed", 4: "retired", 5: "disabled",
          6: "keeping house", 7: "student", 8: "other"}
    for sname, smk in (("all exits", ex), ("exits with a birth in t+1", ex & (d.birth_t_p1 == 1).to_numpy()),
                       ("exits without a birth in t or t+1", ex & (d.birth_t_p1 == 0).to_numpy()
                        & (d.birth_t == 0).to_numpy()),
                       ("exits, wife 55-59", ex & (cells["wife's age"] == "55-59"))):
        mk = smk & np.isfinite(st)
        for c, labc in SL.items():
            v = np.mean(st[mk] == c) if mk.sum() else np.nan
            add("PSID", "v-status", sname, labc, "status at the interview after the zero-hours year (%)", 100 * v,
                100 * np.sqrt(v * (1 - v) / max(mk.sum(), 1)), int(mk.sum()))
    # return within 1, 2, 4 years (positive hours in t+2.., same husband and wife, annual years observed)
    for h, lab in ((1, "return within 1 year (hours > 0 in t+2)"), (2, "return within 2 years (t+2..t+3)"),
                   (4, "return within 4 years (t+2..t+5)")):
        okh = np.ones(len(d), bool)
        anyr = np.zeros(len(d), bool)
        for j in range(2, 2 + h):
            if j > 5:
                break
            wj = d[f"wh_p{j}"].to_numpy(float)
            okh &= np.isfinite(wj) & (d[f"w_pid_p{j}"].to_numpy(float) == wpid) & (d.year.to_numpy() + j <= 1996)
            anyr |= np.nan_to_num(wj) > 0
        for sname, smk in (("all exits", ex), ("exits with a birth in t+1", ex & (d.birth_t_p1 == 1).to_numpy()),
                           ("exits without a birth in t or t+1",
                            ex & (d.birth_t_p1 == 0).to_numpy() & (d.birth_t == 0).to_numpy())):
            mk = smk & okh
            if mk.sum() < 20:
                continue
            v = anyr[mk].mean()
            add("PSID", "v-return", sname, lab, "share (%)", 100 * v, 100 * np.sqrt(v * (1 - v) / mk.sum()),
                int(mk.sum()))
    # repeat exits: number of exits per wife within the annual window (same couple)
    d["couple"] = d.pid.astype(np.int64) * 10 ** 7 + d.w_pid.astype(np.int64)
    ne_ = d.groupby("couple")["y"].sum()
    nobs = d.groupby("couple")["y"].size()
    exiters = ne_[ne_ > 0]
    add("PSID", "v-repeat", "couples with at least one exit", "all", "share with 2+ exits (%)",
        100 * (exiters >= 2).mean(), np.nan, len(exiters))
    add("PSID", "v-repeat", "all exits", "all", "share of exits by wives with 2+ exits (%)",
        100 * exiters[exiters >= 2].sum() / exiters.sum(), np.nan, int(exiters.sum()))
    add("PSID", "v-repeat", "couples", "all", "mean eligible wife-years per couple", nobs.mean(), np.nan, len(nobs))
    # (vi) persistence: previous exit of the same couple (earlier year in the window) predicts the next exit?
    d = d.sort_values(["couple", "year"])
    d["prev_exit"] = (d.groupby("couple")["y"].cumsum() - d["y"] > 0).astype(float)
    d["nprior"] = d.groupby("couple").cumcount()
    mk = (d.nprior >= 1).to_numpy()                 # wife-years with at least one earlier eligible year
    Xp = pd.concat([pd.DataFrame({"previous exit of the same wife": d.prev_exit.to_numpy()}),
                    X.loc[d.index].reset_index(drop=True)], axis=1)
    noh = [c for c in Xp.columns if not c.startswith("her hours")]
    r = wlpm(d.y.to_numpy()[mk], Xp[noh][mk], None, fe=d.year.to_numpy()[mk], cl=d.fam68.to_numpy()[mk])
    add_reg("PSID", "vi", "persistence, no hours controls (wife-years after the first)", "annual exit (pp)", r,
            terms=["previous exit of the same wife"])
    r = wlpm(d.y.to_numpy()[mk], Xp[mk], None, fe=d.year.to_numpy()[mk], cl=d.fam68.to_numpy()[mk])
    add_reg("PSID", "vi", "persistence, with her hours in t (wife-years after the first)", "annual exit (pp)", r,
            terms=["previous exit of the same wife"])


# =====================================================================================================
# output
# =====================================================================================================
def cellfmt(r, nd=2):
    if not np.isfinite(r.coef):
        return "-"
    if np.isfinite(r.se) and r.table in ("ii", "vi") or (r.table == "iv" and "pp" in r.outcome):
        pv = "<0.001" if r.p < 0.001 else f"{r.p:.3f}"
        return f"{r.coef:.{nd}f}{r.stars} ({r.se:.{nd}f}; p={pv})"
    if np.isfinite(r.se):
        return f"{r.coef:.{nd}f} ({r.se:.{nd}f})"
    return f"{r.coef:.{nd}f}"


def write_md(D):
    L = ["# Why do wives leave employment? (IGE/63.WifeExitWhy.py, 2026-10-19)", "",
         "Married wives 25-59, husband employed. CPS 1994-2023 and SIPP 2003-2016: persistent monthly exit (employed "
         "t-1, t; not employed t+1, t+2). PSID 1968-1996 (annual years): hours > 0 in t, 0 in t+1. Regression cells: "
         "coefficient in percentage points, stars, (cluster s.e.; p). *** p<0.01, ** p<0.05, * p<0.1. Hazard cells: "
         "rate (s.e.). Associations, not causal effects. Aggregates only.", ""]

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
                for c in cols:
                    x = gg[gg[colkey] == c]
                    vals.append(cellfmt(x.iloc[0], nd) if len(x) else "")
                L.append(f"| {rk} | " + " | ".join(vals) + f" | {int(gg.n.max()) if np.isfinite(gg.n.max()) else ''} |")
            notes = [x for x in g.note.unique() if x]
            if notes and len(notes) <= 3:
                L.append("")
                L.append("Notes: " + "; ".join(notes))
            L.append("")

    for ds in ("CPS", "SIPP", "PSID"):
        X = D[D.dataset == ds]
        table(X[X.table == "vii"], f"{ds}: steady state (vii)")
        table(X[X.table == "i"], f"{ds}: exit hazard by cell, share of wife-months and of exits (i)")
        table(X[X.table == "ii"], f"{ds}: LPM of the exit on all covariates jointly (ii)")
        table(X[X.table == "iii-group"], f"{ds}: stated reason for the persistent exits, grouped (iii)",
              rowkey="cell", colkey="sample")
        table(X[X.table == "iii-detail"], f"{ds}: stated reason, detailed (iii)", rowkey="cell", colkey="sample")
        table(X[X.table == "iv"], f"{ds}: spell length / return to work (iv)")
        table(X[X.table == "v-status"], f"{ds}: status at the interview after the zero-hours year (v)",
              rowkey="cell", colkey="sample")
        table(X[X.table == "v-return"], f"{ds}: return to work (v)")
        table(X[X.table == "v-repeat"], f"{ds}: repeat exits (v)")
        table(X[X.table == "vi"], f"{ds}: persistence (vi)")
    (OUT / "wife_exit_why.md").write_text("\n".join(L), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="cps,sipp,psid")
    ap.add_argument("--scratch", default=str(Path(tempfile.gettempdir()) / "ige63_scratch"))
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()
    scratch = Path(a.scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    assert HERE.parent not in scratch.resolve().parents, "scratch must be outside the repository"
    for part in a.only.split(","):
        ROWS.clear()
        if part == "cps":
            cps_part()
        elif part == "sipp":
            sipp_part(scratch, min(a.workers, 6))
        elif part == "psid":
            psid_part()
        pd.DataFrame(ROWS).to_pickle(scratch / f"rows_{part}.pkl")
        log(f"{part}: {len(ROWS)} rows")
    D = pd.concat([pd.read_pickle(scratch / f"rows_{p}.pkl") for p in ("cps", "sipp", "psid")
                   if (scratch / f"rows_{p}.pkl").exists()], ignore_index=True)
    D.to_csv(OUT / "wife_exit_why.csv", index=False)
    write_md(D)
    log(f"wrote {len(D)} rows")


if __name__ == "__main__":
    main()
