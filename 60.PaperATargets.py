r"""SMM target moments for Paper A's structural model, with block-bootstrap standard errors (2026-10-18). [Paper A]

Implements Part II (Table "Targets, windows and sources") of IGE/paperA_joint_loss/model_document.tex: every TARGET
of that table, each with its value, bootstrap standard error, N, data window, source script and definition, plus the
bootstrap variance-covariance matrix of the moments within each data source (SMM weighting matrix). Validation moments
are not targets; the added-worker effect by age of IGE/50 is copied (with 50's analytical s.e.) as validation.

DATA AND BUILDERS (imported read-only via importlib; no other script is edited)
  CPS   30.CPSJointJobLoss.py couples panel (IGE/data/cps_couples_panel.pkl) and 37.CPSJointLossChecks.py's event
        samples (tau-3 .. tau+3) and shift(); basic monthly 1994-2023.
  PSID  19.FatherDisplacement.py (men panel, stacks, displacement file psid_displacement.pkl), 23/25.JointJobLoss.py
        (wife's job-end reports, father x stack units, couple-years, sector match), 38's window designs (re-coded
        here), 47.PSIDConsumptionEvent.py (consumption 1999-2021 and its event panel), estimation/psid_wealth.py
        (liquid wealth, the ReducedForm/17 construction). Unweighted SRC + SEO, Black and White (head's race).
  SIPP  40.SIPPJointLoss.py couples panel (IGE/data/sipp_couples_panel.pkl) and its helpers; panels 2004, 2008, 2014
        (reference months 2003-2016). Monthly wage-job earnings are not in 40's cache: they are read here from the
        same raw core files (2004/08: TPMSUM1 + TPMSUM2 of jobs with an employer number; 2014: TJBk_MSUM of employer
        jobs held in the month) and cached in IGE/data/ext/sipp/cache_earn/.
WINDOWS
  CPS couple-months 1994-2023; PSID income years 1984-2021 (stacked designs: husband's displacement events 1984-2021,
  outcome years to 2021; couple-years: intervals ending 1984-2021; 38's two-window decomposition events 1987-2021);
  PSID consumption interview waves 1999-2021 (events 2000-2020); PSID liquid wealth waves 1984, 1989, 1994, 1999-2019;
  SIPP 2003-2016.
BOOTSTRAP
  Block bootstrap over the clustering unit: 1968 family (PSID, consumption included: one set of family draws per
  replication for all PSID moments), household (CPS: household id; SIPP: panel x sample unit). In each replication the
  clusters are drawn with replacement and every moment of that source is recomputed on the same draw: each row gets
  the number of times its cluster was drawn as a weight (equivalent to stacking the duplicated clusters; a duplicated
  father x stack unit keeps one fixed effect, which gives the same within estimate). Fixed-effect regressions are
  re-estimated in every replication (one FE: exact weighted within transformation; two FE: weighted alternating
  projections started from the full-sample within transform, which differs from the raw data by an element of the
  fixed-effect space and therefore converges to the same weighted projection). Survey weights (CPS wife's composite
  weight, SIPP wife's person weight) multiply the bootstrap weights in the descriptive probabilities, as in 30/40;
  regressions are unweighted as in the source scripts. S.e. = s.d. over replications; p-values (coefficients only)
  from the normal approximation with the bootstrap s.e.; *** p<0.01, ** p<0.05, * p<0.1.
OUTPUTS
  IGE/output/paperA_targets.csv (block, moment, value, se, n, window, source_script, definition, + id, p, stars,
  data_source, target, n_events), IGE/output/paperA_targets.md, IGE/output/paperA_targets_vcov_<source>.csv
  (cps / psid / sipp: targets only; dws: the UI take-up inputs; ids as row and column labels).
ADDED 2026-10-18 (lead; proposals/paperA_identification_plan.md Secs. 1.3-1.4, 5 items 1-2): T28 = share of husbands
  displaced twice or more among husbands observed 10+ years (PSID, by race), and the DWS UI receipt shares of displaced
  husbands and wives (39's local IPUMS extract; household bootstrap) with their difference.
Run from IGE/: ../.venv/Scripts/python.exe -I 60.PaperATargets.py [--reps 200] [--only cps,psid,sipp,dws]
Associations, not causal effects, wherever a moment is a regression coefficient (designs of the source scripts).
"""
import argparse
import importlib.util
import sys
import time
import warnings
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import numpy as np                            # noqa: E402
import pandas as pd                           # noqa: E402
import scipy.sparse as sp                     # noqa: E402
from scipy.stats import norm                  # noqa: E402

from common import DATA, OUT, stars           # noqa: E402

warnings.simplefilter("ignore", FutureWarning)
warnings.simplefilter("ignore", RuntimeWarning)
warnings.simplefilter("ignore", pd.errors.PerformanceWarning)


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


CACHE_PSID = DATA / "paperA_targets_psid.pkl"
EARN_DIR = DATA / "ext" / "sipp" / "cache_earn"
W_CPS, W_PSID, W_PSIDC, W_SIPP = "CPS 1994-2023", "PSID 1984-2021", "PSID 1999-2021", "SIPP 2003-2016"
T0 = time.time()


def log(*a):
    print(f"[{time.time() - T0:7.0f}s]", *a, flush=True)


# =====================================================================================================
# weighted estimators (bootstrap weights = cluster draw counts mapped to rows)
# =====================================================================================================
def wmean(y, w):
    y, w = np.asarray(y, float), np.asarray(w, float)
    ok = np.isfinite(y) & np.isfinite(w)
    s = w[ok].sum()
    return float((y[ok] * w[ok]).sum() / s) if s > 0 else np.nan


def fe_demean(A, g, ng, w):
    """Exact weighted within transformation for one set of fixed effects (columns of A)."""
    sw = np.bincount(g, weights=w, minlength=ng)
    inv = np.where(sw > 0, 1.0 / np.where(sw > 0, sw, 1.0), 0.0)
    if A.ndim == 1:
        return A - (np.bincount(g, weights=w * A, minlength=ng) * inv)[g]
    out = np.empty_like(A)
    for j in range(A.shape[1]):
        out[:, j] = A[:, j] - (np.bincount(g, weights=w * A[:, j], minlength=ng) * inv)[g]
    return out


def fe_ols(Y, X, g, ng, w):
    """Weighted OLS of Y on X (N x K) absorbing one FE (codes g); returns b."""
    X = X.reshape(len(Y), -1)
    Yt = fe_demean(Y, g, ng, w)
    Xt = fe_demean(X, g, ng, w)
    XtX = (Xt * w[:, None]).T @ Xt
    return np.linalg.lstsq(XtX, (Xt * w[:, None]).T @ Yt, rcond=None)[0]


def fe_slope(y, H, g, ng, w):
    """Single-regressor version of fe_ols (fast)."""
    sw = np.bincount(g, weights=w, minlength=ng)
    inv = np.where(sw > 0, 1.0 / np.where(sw > 0, sw, 1.0), 0.0)
    yt = y - (np.bincount(g, weights=w * y, minlength=ng) * inv)[g]
    Ht = H - (np.bincount(g, weights=w * H, minlength=ng) * inv)[g]
    den = (w * Ht * Ht).sum()
    return float((w * Ht * yt).sum() / den) if den > 0 else np.nan


class TWFE:
    """y on X with two sets of fixed effects (unit, cell), weighted, by alternating projections."""

    def __init__(self, Y, X, codes, tol=1e-9, maxit=3000):
        self.N = len(Y)
        self.D = []
        for g in codes:
            g = pd.factorize(g)[0]
            n = g.max() + 1
            self.D.append(sp.csr_matrix((np.ones(self.N), (np.arange(self.N), g)), shape=(self.N, n)))
        A = np.column_stack([Y, X]).astype(float)
        self.scale = np.maximum(A.std(axis=0), 1e-12)
        self.tol, self.maxit = tol, maxit
        self.A0 = self._demean(A, np.ones(self.N), tol=tol * 0.01, maxit=maxit * 3)

    def _demean(self, A, w, tol, maxit):
        A = A.copy()
        DT = [D.T.tocsr() for D in self.D]
        sws = [Dt @ w for Dt in DT]
        for _ in range(maxit):
            mx = 0.0
            for D, Dt, sw in zip(self.D, DT, sws):
                inv = np.where(sw > 0, 1.0 / np.where(sw > 0, sw, 1.0), 0.0)
                mu = (Dt @ (A * w[:, None])) * inv[:, None]
                A -= D @ mu
                mx = max(mx, float(np.max(np.abs(mu) / self.scale)))
            if mx < tol:
                break
        return A

    def fit(self, w=None):
        w = np.ones(self.N) if w is None else np.asarray(w, float)
        A = self.A0 if np.all(w == 1) else self._demean(self.A0, w, self.tol, self.maxit)
        Y, X = A[:, 0], A[:, 1:]
        XtX = (X * w[:, None]).T @ X
        return np.linalg.lstsq(XtX, (X * w[:, None]).T @ Y, rcond=None)[0]

    def fitc(self, c, cl):
        """fit with row weights c[cl]; memoised on the cluster-weight vector (one fit per replication)."""
        if getattr(self, "_lastc", None) is c:
            return self._lastb
        self._lastb, self._lastc = self.fit(c[cl]), c
        return self._lastb


# =====================================================================================================
# moment registry
# =====================================================================================================
class Source:
    """One data source: cluster count G and moments, each a function of the cluster-weight vector c (len G)."""

    def __init__(self, name):
        self.name, self.G, self.M = name, None, []

    def add(self, mid, block, moment, fn, n, window, script, definition, coef=False, target=True, n_events=None):
        self.M.append(dict(id=mid, block=block, moment=moment, fn=fn, n=n, window=window, source_script=script,
                           definition=definition, coef=coef, target=target, n_events=n_events))

    def run(self, reps, seed):
        c1 = np.ones(self.G)
        vals = {}
        for m in self.M:
            v = m["fn"](c1)
            vals[m["id"]] = v
            log(f"{self.name}: {m['id']} = {v:.6g}")
        rng = np.random.default_rng(seed)
        B = np.full((reps, len(self.M)), np.nan)
        for r in range(reps):
            c = np.bincount(rng.integers(0, self.G, self.G), minlength=self.G).astype(float)
            for j, m in enumerate(self.M):
                try:
                    B[r, j] = m["fn"](c)
                except Exception:                                   # noqa: BLE001
                    B[r, j] = np.nan
            if (r + 1) % 10 == 0 or r == 0:
                log(f"{self.name}: replication {r + 1}/{reps}")
        return vals, pd.DataFrame(B, columns=[m["id"] for m in self.M])


def cluster_codes(values, index):
    """Map cluster labels to positions of `index` (a pandas Index of all clusters of the source)."""
    pos = index.get_indexer(np.asarray(values))
    assert (pos >= 0).all()
    return pos


# =====================================================================================================
# CPS
# =====================================================================================================
def cps_source():
    m37 = _load("cps37", "37.CPSJointLossChecks.py")
    m30 = m37.m30
    S = Source("cps")
    log("CPS: loading panel")
    P = m30.add_vars(m30.build_panel())
    P.attrs = {}
    for k in (-2, -1):
        for c, v in m37.shift(P, ["w_dur"], k).items():
            P[c] = v.astype("int16")
    P["m_do"] = (P.same_dind & ((P.h_docc == P.w_docc) & (P.h_docc > 0)).astype("int8")).astype("int8")
    P["m_doc"] = (P.m_do & ((P.h_cow == P.w_cow) & (P.h_cow > 0)).astype("int8")).astype("int8")
    keep = ["hh", "sm", "w", "rgrp", "same_dind", "m_doc", "h_s", "w_s", "h_unt", "w_unt", "h_dur", "w_dur",
            "w_dur-2", "w_dur-1"] + [f"{v}{k:+d}" for v in ("h_s", "w_s", "h_unt", "w_unt") for k in (-2, -1, 1, 2, 3)]
    P = P[keep].copy()
    P["hhc"] = pd.factorize(P["hh"])[0].astype(np.int64)
    S.G = int(P.hhc.max() + 1)
    log(f"CPS: {len(P):,} couple-months, {S.G:,} households")

    def slim(d, y, extra=()):
        g, u = pd.factorize(d["sm"])
        out = dict(y=np.asarray(y, float), H=d["H"].to_numpy(float), g=g, ng=len(u), cl=d["hhc"].to_numpy(),
                   sw=d["w"].to_numpy(float))
        for e in extra:
            out[e] = d[e].to_numpy()
        return out

    def excess(s, mask=None):
        def f(c):
            w = c[s["cl"]]
            if mask is None:
                return fe_slope(s["y"], s["H"], s["g"], s["ng"], w)
            mk = mask
            g, ng = s["g"][mk], s["ng"]
            return fe_slope(s["y"][mk], s["H"][mk], g, ng, w[mk])
        return f

    # ---- event samples of 37 (tau-3 .. tau+3), non-temporary version
    ev = m37.event_samples(P)
    spec = {"tau-3": ("w_s-2", "w_unt-2", "h_unt+1"), "tau-2": ("w_s-1", "w_unt-1", "h_unt+1"),
            "tau-1": ("w_s", "w_unt", "h_unt+1"), "tau": ("w_s+1", "w_unt+1", "h_unt+1"),
            "tau+1": ("w_s+2", "w_unt+2", "h_unt+1"), "tau+2": ("w_s+3", "w_unt+3", "h_unt+1"),
            "tau+3": ("w_s+3", "w_unt+3", "h_unt")}
    NT = {}
    for k, (ws, wu, hu) in spec.items():
        d = ev[k]
        d = d[((d.H == 0) | d[hu].isin([2, 3])) & ~((d[ws] == 2) & (d[wu] == 1))]
        y = ((d[ws] == 2) & d[wu].isin([2, 3])).astype(float)
        NT[k] = slim(d, y, extra=("rgrp", "same_dind", "m_doc"))
    del ev
    s0 = NT["tau"]
    n0, n1 = len(s0["y"]), int(s0["H"].sum())
    dnt = ("Wife becomes a job loser other than on temporary layoff (unemployed with PRUNTYPE 2-3, after employment) "
           "in month t+1; husband's job loss other than on layoff (PRUNTYPE 2-3) vs husband employed; both employed at "
           "t; wives on layoff at t+1 dropped (37 Table 2, panel (i), column 3).")
    S.add("cps_jl_nt", "Joint loss, monthly", "Wife's same-month job-loss excess when he loses his, non-temporary "
          "losses (LPM, state x month FE)", excess(s0), n0, W_CPS, "IGE/37 (IGE/60)", dnt, coef=True, n_events=n1)
    # workplace match: three exclusive groups
    grp = {"s2": s0["m_doc"] == 1, "s1": (s0["same_dind"] == 1) & (s0["m_doc"] == 0), "s0": s0["same_dind"] == 0}
    lab = {"s2": "shared-employer cell (same detailed industry x detailed occupation x class of worker; s=2)",
           "s1": "same detailed industry, outside the shared-employer cell (s=1)",
           "s0": "different detailed industry or industry unknown (s=0)"}
    for k in ("s2", "s1", "s0"):
        mk = grp[k]
        S.add(f"cps_jl_nt_{k}", "Joint loss, monthly", f"Same, {lab[k]}", excess(s0, mk), int(mk.sum()), W_CPS,
              "IGE/37 (IGE/60)", dnt + " Spouses' main jobs at t; groups exclusive.", coef=True,
              n_events=int(s0["H"][mk].sum()))
    for k in ("s2", "s1", "s0"):
        mk = grp[k] & (s0["H"] == 0)

        def share(c, mk=mk):
            w = c[s0["cl"]] * s0["sw"]
            h0 = s0["H"] == 0
            return w[mk].sum() / w[h0].sum()
        S.add(f"cps_share_{k}", "Calibration check (not a target)", f"Share of couples, {lab[k]}", share,
              int((s0["H"] == 0).sum()), W_CPS, "IGE/37 (IGE/60)",
              "Weighted share among both-employed couples whose husband stays employed (H = 0) in the headline sample; "
              "the model uses PSID couples' s (to be coded with this definition) and these shares as a check.",
              target=False)
    # leads and lags
    for k, lab_ in (("tau-3", "-3"), ("tau-2", "-2"), ("tau-1", "-1"), ("tau+1", "+1"), ("tau+2", "+2"),
                    ("tau+3", "+3")):
        s = NT[k]
        S.add(f"cps_jl_nt_m{lab_[1]}" if lab_[0] == "-" else f"cps_jl_nt_p{lab_[1]}", "Joint loss, monthly",
              f"Wife's excess job-loss hazard in month {lab_} relative to his loss month, non-temporary losses",
              excess(s), len(s["y"]), W_CPS, "IGE/37 event samples (IGE/60)",
              f"37's Figure 1 samples (tau = his job-loss month; month {lab_}: the wife's transition into non-temporary "
              "job loss in that month; at -3 (+3) her (his) previous month is outside the rotation, so that job loss is "
              "a new job loser by duration <= 4 weeks); husband's loss other than on layoff; wives on layoff in the "
              "outcome month dropped; state x month FE of the base month.", coef=True, n_events=int(s["H"].sum()))
    # base hazards
    for r, mk in (("pooled", None), ("Black", s0["rgrp"] == "Black"), ("White", s0["rgrp"] == "White")):
        h0 = s0["H"] == 0
        mk = h0 if mk is None else (h0 & mk)

        def base(c, mk=mk):
            return wmean(s0["y"][mk], (c[s0["cl"]] * s0["sw"])[mk])
        S.add(f"cps_wife_hazard_{r.lower()}", "Base hazards", f"Wife's monthly non-temporary job-loss rate, he "
              f"employed, {r}", base, int(mk.sum()), W_CPS, "IGE/37 (IGE/60)",
              "P(wife becomes a non-temporary job loser at t+1) among both-employed couples whose husband stays employed "
              "at t+1; wife's composite weight; race = husband's race.")
    # (NT and s0 stay alive: the moment closures use them)
    # ---- her search: entry of non-employed wives, husband employed
    b = (P.h_s == 1) & P.w_s.isin([2, 3, 4]) & (P["h_s+1"] == 1) & (P["w_s+1"] >= 1)
    d = P.loc[b, ["hhc", "w", "rgrp", "w_s+1"]]
    ye = (d["w_s+1"] == 1).to_numpy(float)
    cl, sw, rg = d.hhc.to_numpy(), d.w.to_numpy(float), d.rgrp.to_numpy()
    for r, mk in (("pooled", np.ones(len(d), bool)), ("Black", rg == "Black"), ("White", rg == "White")):
        S.add(f"cps_entry_{r.lower()}", "Her search", f"Monthly employment entry of non-employed wives, husband "
              f"employed, {r}", (lambda c, mk=mk: wmean(ye[mk], (c[cl] * sw)[mk])), int(mk.sum()), W_CPS,
              "IGE/30 (IGE/60)", "P(wife employed at t+1) among wives not employed at t (unemployed or out of the labor "
              "force) whose husband is employed at t and t+1; wife's composite weight; race = husband's race.")
    # ---- her exits outside job loss
    b = (P.h_s == 1) & (P.w_s == 1) & (P["h_s+1"] == 1) & (P["w_s+1"] >= 1)
    d = P.loc[b, ["hhc", "w", "w_s+1"]]
    yx = d["w_s+1"].isin([3, 4]).to_numpy(float)
    cl2, sw2 = d.hhc.to_numpy(), d.w.to_numpy(float)
    S.add("cps_wife_exit", "Her exits", "Wives' monthly exit from employment without a job-loss reason, husband employed",
          lambda c: wmean(yx, c[cl2] * sw2), len(d), W_CPS, "IGE/30 (IGE/60)",
          "P(wife unemployed for a reason other than job loss -- job leaver, re-entrant, new entrant -- or out of the "
          "labor force at t+1) among wives employed at t whose husband is employed at t and t+1; job losers (PRUNTYPE "
          "1-3) are not exits; wife's composite weight.")
    # ---- persistent entry and exit (2026-10-19, Paper A model: the same filter is applied to the simulated monthly
    # panel in paperA_model/moments.py): a transition counts only if the status before it held for two consecutive
    # months and the status after it holds for two consecutive months (t-1, t, t+1, t+2 all in sample: one 4-month
    # rotation spell); this removes one-month status reversals, most of which are CPS response error
    hs = (P.h_s == 1) & (P["h_s+1"] == 1)
    obs = (P["w_s-1"] >= 1) & (P["w_s+1"] >= 1) & (P["w_s+2"] >= 1)
    ne = [2, 3, 4]
    b = hs & obs & P["w_s-1"].isin(ne) & P.w_s.isin(ne)
    d = P.loc[b, ["hhc", "w", "rgrp", "w_s+1", "w_s+2"]]
    yep = ((d["w_s+1"] == 1) & (d["w_s+2"] == 1)).to_numpy(float)
    clp, swp, rgp = d.hhc.to_numpy(), d.w.to_numpy(float), d.rgrp.to_numpy()
    for r, mk in (("pooled", np.ones(len(d), bool)), ("Black", rgp == "Black"), ("White", rgp == "White")):
        S.add(f"cps_entry_p_{r.lower()}", "Her search", f"Persistent monthly employment entry of non-employed wives, "
              f"husband employed, {r}", (lambda c, mk=mk: wmean(yep[mk], (c[clp] * swp)[mk])), int(mk.sum()), W_CPS,
              "IGE/60", "P(wife employed at t+1 and t+2) among wives not employed (unemployed or out of the labor force) "
              "at t-1 and t, husband employed at t and t+1, all four months in sample; wife's composite weight; race = "
              "husband's race. Filters one-month reversals (response error) identically in the model.")
    b = hs & obs & (P["w_s-1"] == 1) & (P.w_s == 1)
    d = P.loc[b, ["hhc", "w", "w_s+1", "w_s+2"]]
    yxp = (d["w_s+1"].isin([3, 4]) & d["w_s+2"].isin(ne)).to_numpy(float)
    clq, swq = d.hhc.to_numpy(), d.w.to_numpy(float)
    S.add("cps_wife_exit_p", "Her exits", "Persistent monthly exit of wives from employment without a job-loss reason, "
          "husband employed", lambda c: wmean(yxp, c[clq] * swq), len(d), W_CPS, "IGE/60",
          "P(wife unemployed for a reason other than job loss or out of the labor force at t+1, and not employed at "
          "t+2) among wives employed at t-1 and t, husband employed at t and t+1, all four months in sample; job "
          "losers at t+1 are not exits; wife's composite weight. Filters one-month reversals identically in the model.")
    del P
    return S


# =====================================================================================================
# SIPP
# =====================================================================================================
def sipp_earn_wave(m40, panel, w):
    path = EARN_DIR / f"e{panel}w{w:02d}.pkl"
    if path.exists():
        return pd.read_pickle(path)
    raw = m40.src(panel, w)[1]
    if panel == 2014:
        want = {"SSUID", "PNUM", "SWAVE", "MONTHCODE", "EMS_EHC"} | {f"{v}" for j in range(1, 8) for v in
                                                                    (f"TJB{j}_MSUM", f"EJB{j}_JBORSE", f"EJB{j}_BMONTH",
                                                                     f"EJB{j}_EMONTH")}
    else:
        want = {"ssuid", "epppnum", "rhcalyr", "rhcalmn", "ems", "eeno1", "eeno2", "tpmsum1", "tpmsum2"}
    kw = dict(chunksize=60000, dtype=str, low_memory=False)
    if panel == 2014:
        import gzip
        with gzip.open(raw, "rt") as fh:
            head = fh.readline()
        kw["sep"] = "|" if head.count("|") > head.count(",") else ","
        kw["usecols"] = lambda c: c in want
    else:
        kw["usecols"] = lambda c: c.lower() in want
    out = []
    for ch in pd.read_csv(raw, **kw):
        n = m40._num
        if panel == 2014:
            mo = n(ch, "MONTHCODE")
            earn = np.zeros(len(ch))
            for j in range(1, 8):
                held = (n(ch, f"EJB{j}_JBORSE") == 1) & (n(ch, f"EJB{j}_BMONTH") <= mo) & (mo <= n(ch, f"EJB{j}_EMONTH"))
                v = pd.to_numeric(ch.get(f"TJB{j}_MSUM"), errors="coerce").fillna(0).to_numpy(float) \
                    if f"TJB{j}_MSUM" in ch else np.zeros(len(ch))
                earn += np.where(held & (v > 0), v, 0.0)
            x = pd.DataFrame({"ssuid": ch["SSUID"].astype(str).str.strip().to_numpy(), "pnum": n(ch, "PNUM"),
                              "ym": (2012 + n(ch, "SWAVE")) * 12 + mo - 1, "ms": n(ch, "EMS_EHC"), "earn": earn})
        else:
            ch.columns = [c.lower() for c in ch.columns]
            earn = np.zeros(len(ch))
            for j in (1, 2):
                v = pd.to_numeric(ch[f"tpmsum{j}"], errors="coerce").fillna(0).to_numpy(float)
                earn += np.where((n(ch, f"eeno{j}") > 0) & (v > 0), v, 0.0)
            x = pd.DataFrame({"ssuid": ch["ssuid"].astype(str).str.strip().str.lstrip("0").to_numpy(),
                              "pnum": n(ch, "epppnum"), "ym": n(ch, "rhcalyr") * 12 + n(ch, "rhcalmn") - 1,
                              "ms": n(ch, "ems"), "earn": earn})
        out.append(x[(x.ms == 1) & (x.earn > 0)].drop(columns="ms"))
    e = pd.concat(out, ignore_index=True)
    e["panel"] = panel
    EARN_DIR.mkdir(parents=True, exist_ok=True)
    e.to_pickle(path)
    log(f"SIPP earnings extracted {panel} w{w}: {len(e):,} person-months")
    return e


def sipp_source():
    m40 = _load("sipp40", "40.SIPPJointLoss.py")
    S = Source("sipp")
    P = m40.build_panel()
    P, L = m40.add_vars(P)
    S.G = int(P.hh.max() + 1)
    log(f"SIPP: {len(P):,} couple-months, {S.G:,} households")
    hh, pm, ww = P.hh.to_numpy(), P.pm.to_numpy(), P.wgt_w.to_numpy(float)
    # ---- wife's employment after his involuntary separation (40 section 4), s = 0, 1, 6
    base_ne, H = m40.aw_base(P, L, "ne")
    for s_ in (0, 1, 6):
        y = L.at("E_w", 1 + s_)
        ok = base_ne & ~np.isnan(y)
        g, u = pd.factorize(pm[ok])
        yy, HH, cl = y[ok], H[ok], hh[ok]
        S.add(f"sipp_wife_emp_s{s_}", "Her search", f"Employment of wives with no job the month before, relative to "
              f"wives whose husband stays employed, month {s_} after his involuntary separation",
              (lambda c, yy=yy, HH=HH, g=g, n=len(u), cl=cl: fe_slope(yy, HH, g, n, c[cl])), int(ok.sum()), W_SIPP,
              "IGE/40 (IGE/60)", "40's added-worker path: base month b = tau-1, husband employed, wife with no job all "
              "month; H = 1 husband involuntary separation at tau = b+1 vs husband employed without one; outcome wife "
              "employed at tau+s; LPM with base panel x rotation x month FE.", coef=True, n_events=int(HH.sum()))
    # ---- his employment after an involuntary separation, same sample
    for s_ in (3, 6, 12):
        y = L.at("E_h", 1 + s_)
        ok = base_ne & ~np.isnan(y)
        for hv, lab in ((1, "after an involuntary separation"), (0, "no separation (comparison)")):
            mk = ok & (H == hv)
            yy, cl, sw = y[mk], hh[mk], ww[mk]
            S.add(f"sipp_his_emp_s{s_}_{'sep' if hv else 'nosep'}", "His search",
                  f"His employment {s_} months {lab}", (lambda c, yy=yy, cl=cl, sw=sw: wmean(yy, c[cl] * sw)),
                  int(mk.sum()), W_SIPP, "IGE/40 (IGE/60)",
                  "P(husband employed at tau+s) for husbands with (H = 1) / without (H = 0) an involuntary separation "
                  "at tau, in 40's added-worker sample (husband employed and wife without a job at tau-1); wife's "
                  "person weight.")
    # ---- wives' exits outside involuntary separation
    inv_w_l1 = L.at("INV_w", -1)
    b = (P.E_w_l1 == 1).to_numpy() & (P.E_h_l1 == 1).to_numpy() & (P.E_h == 1).to_numpy() & \
        (P.INV_h == 0).to_numpy() & ~np.isnan(inv_w_l1)
    yx = ((P.E_w.to_numpy() == 0) & (inv_w_l1 == 0) & (P.INV_w.to_numpy() == 0)).astype(float)[b]
    clx, swx = hh[b], ww[b]
    S.add("sipp_wife_exit", "Her exits", "Wives' monthly exit from employment outside an involuntary separation, "
          "husband employed (SIPP counterpart)", lambda c: wmean(yx, c[clx] * swx), int(b.sum()), W_SIPP,
          "IGE/40 (IGE/60)", "P(wife with no job all month m) among wives with a job in m-1 whose husband has a job in "
          "m-1 and m without an involuntary separation in m; exits whose job ended for an involuntary reason in m-1 or "
          "m are not counted; wife's person weight. Supplementary to the CPS target.", target=False)
    # ---- earnings on re-employment by non-employment duration, involuntary separations
    E = pd.concat([sipp_earn_wave(m40, panel, w) for panel, nw in m40.PANELS.items() for w in range(1, nw + 1)
                   if m40.src(panel, w)[1].exists()], ignore_index=True)
    E = E.drop_duplicates(["panel", "ssuid", "pnum", "ym"])
    for s in ("h", "w"):
        x = P[["panel", "ssuid", f"pnum_{s}", "ym"]].rename(columns={f"pnum_{s}": "pnum"})
        P[f"earn_{s}"] = x.merge(E, on=["panel", "ssuid", "pnum", "ym"], how="left")["earn"].to_numpy()
    L = m40.Look(P)
    DUR = [(1, 3), (4, 12), (13, 24)]
    for s, who in (("h", "husbands"), ("w", "wives")):
        sep = (P[f"INV_{s}"].to_numpy() == 1) & (P[f"E_{s}_l1"].to_numpy() == 1)
        idx = np.flatnonzero(sep)
        pre = L.at(f"earn_{s}", -1)[idx]
        Ek = np.column_stack([L.at(f"E_{s}", k)[idx] for k in range(1, 27)])          # months m+1 .. m+26
        Rk = np.column_stack([L.at(f"earn_{s}", k)[idx] for k in range(1, 28)])
        d = np.full(len(idx), -1)
        for i in range(len(idx)):
            row = Ek[i]
            for k in range(26):
                if np.isnan(row[k]):
                    break
                if row[k] == 1:
                    d[i] = k                                    # k months without a job (m+1 .. m+k)
                    break
        post = np.array([Rk[i, d[i] + 1] if 1 <= d[i] <= 24 else np.nan for i in range(len(idx))])
        dl = np.log(post) - np.log(pre)
        ok = np.isfinite(dl) & (np.abs(dl) <= 3)
        for lo, hi in DUR:
            mk = ok & (d >= lo) & (d <= hi)
            yy, cl = dl[mk], hh[idx][mk]
            S.add(f"sipp_reemp_{s}_{lo}_{hi}", "Wage growth", f"Log earnings in the first full month of re-employment "
                  f"minus the last full month before an involuntary separation, {lo}-{hi} months without a job, {who}",
                  (lambda c, yy=yy, cl=cl: wmean(yy, c[cl])), int(mk.sum()), W_SIPP, "IGE/40 panel (IGE/60)",
                  "Involuntary separation (layoff, closure, discharge, temporary job ended, other involuntary) in month "
                  "m of a spouse with a job in m-1; d = consecutive months m+1.. with no job, re-employed in m+d+1; "
                  "outcome log monthly wage-job earnings in m+d+2 (the first full month of the new job) minus m-1 (the "
                  "last full month of the old one), both > 0, |change| <= 3; unweighted mean. The model's monthly "
                  "earnings have no partial months, hence full months on both sides.")
        log(f"SIPP re-employment {s}: separations {len(idx):,}, with duration 1-24 and earnings {int(ok.sum()):,}")
    return S


# =====================================================================================================
# PSID
# =====================================================================================================
def psid_build():
    if CACHE_PSID.exists():
        return pd.read_pickle(CACHE_PSID)
    P47 = _load("p47", "47.PSIDConsumptionEvent.py")
    P25, P23, P19 = P47.P25, P47.P23, P47.P19
    psid9 = P19.psid9
    log("PSID: reading inputs")
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    E = P23.extras()
    X, R = E["X"], E["R"]
    F18 = pd.read_pickle(DATA / "husband_shocks_fam.pkl")
    fam = psid9.family()
    d = pd.read_pickle(DATA / "psid_displacement.pkl")
    ev_sets = P25.wife_events(py, R)
    C = P23.couples(py, X, F18, fam)
    both = (C["hh"] > 0) & (C["wh"] > 0)
    C["s_sec"] = (C["h_sec"] == C["w_sec"]).astype(float).where(both & C["h_sec"].notna() & C["w_sec"].notna())
    m = P19.men_panel(py, fam)
    wl = py[py["head"]][["wave", "int", "wlab"]].drop_duplicates(["wave", "int"])
    m = m.merge(wl, on=["wave", "int"], how="left").drop_duplicates(["pid", "year"])
    wa = py[py["wife"]][["wave", "int", "age"]].drop_duplicates(["wave", "int"]).rename(columns={"age": "w_age"})
    m = m.merge(wa, on=["wave", "int"], how="left")
    log("PSID: units")
    U = P25.build_units(m, d)
    U = P25.add_wife_outcomes(U, m, ev_sets)
    log("PSID: couple-years")
    CY = P25.couple_years(m, d, ev_sets, C)
    Pst = P19.stacks(m, d, "main")
    Pst = Pst.merge(m[["pid", "year", "wlab"]], on=["pid", "year"], how="left")
    Pst["w_lab"] = Pst["wlab"].where(Pst["w_pid"] == Pst["w0"])
    Uj = U[U["pseudo"] == 0][["pid", "ev", "wemp0", "main_W"]].copy()
    Uj["J"] = np.where(Uj["wemp0"] == 0, 0.0, Uj["main_W"])
    Pst = Pst.merge(Uj[["pid", "ev", "J"]].drop_duplicates(["pid", "ev"]), on=["pid", "ev"], how="left")
    log("PSID: consumption panel")
    CC = P47.consumption()
    Ujc = Uj[["pid", "ev", "J"]].drop_duplicates(["pid", "ev"])
    Qc = P47.event_panel(m, d, Ujc, CC["C"], "main")
    log("PSID: liquid wealth")
    from estimation.psid_wealth import family_wealth, WAVES as WW
    Wl = family_wealth()
    lab2wave = {lab: w for w, (_, lab, *_) in WW.items()}
    Wl["wave"] = Wl["year"].map(lab2wave)
    res = dict(m=m, d=d, U=U, CY=CY, Pst=Pst, Qc=Qc, Wl=Wl[["id", "wave", "liquid"]])
    pd.to_pickle(res, CACHE_PSID)
    return res


ES_E = [-3, -1, 0, 1, 2, 3, 4, 5, 6]


def psid_source():
    B = psid_build()
    m, d, U, CY, Pst, Qc, Wl = (B[k] for k in ("m", "d", "U", "CY", "Pst", "Qc", "Wl"))
    S = Source("psid")
    fams = pd.Index(pd.unique(np.concatenate([m.fam68.to_numpy(), U.fam68.to_numpy(), CY.fam68.to_numpy(),
                                              Pst.fam68.to_numpy(), Qc.fam68.to_numpy()]).astype(np.int64)))
    S.G = len(fams)
    log(f"PSID: {S.G:,} 1968 families")
    cc = lambda v: cluster_codes(v.astype(np.int64), fams)                     # noqa: E731

    # ---------------- stacked event studies (19's design), events 1984-2021, outcome years <= 2021
    P = Pst[Pst["ev"].between(1984, 2021) & (Pst["year"] <= 2021)].copy()
    WIFE_Y = {"w_hrs", "w_emp", "bw_present", "w_lab"}

    def es_model(q, y, xs_fn):
        q = q.dropna(subset=[y]).reset_index(drop=True)
        X, names = xs_fn(q)
        mdl = TWFE(q[y].to_numpy(float), X, [q["unit"].to_numpy(), q["cell"].to_numpy()])
        return mdl, names, cc(q["fam68"].to_numpy()), q

    def es_dummies(q):
        names = [f"d{e}" for e in ES_E]
        X = np.column_stack([((q["e"] == e) & (q["treat"] == 1)).to_numpy(float) for e in ES_E])
        return X, names

    ESM = {}

    def es(q, y, key):
        if key not in ESM:
            if y in WIFE_Y:
                q = q[q["w0"].notna()]
            ESM[key] = es_model(q, y, es_dummies)
        return ESM[key]

    def comb_fn(key, wts):
        mdl, names, cl, q = ESM[key]
        L = np.array([wts.get(nm, 0.0) for nm in names])
        return lambda c: float(L @ mdl.fitc(c, cl))

    m13 = {f"d{e}": 1 / 3 for e in (1, 2, 3)}
    dES = ("19's stacked event study (Cengiz et al.): fathers (male heads with a child 0-17 and positive hours at "
           "baseline) first displaced (closure or layoff/firing) in ev vs clean controls (no displacement to ev+6); "
           "father x stack and calendar year x stack FE; reference e = -2; events 1984-2021, outcome years to 2021.")
    for race in ("Black", "White"):
        q = P[P["hrace"] == race]
        rb = race[0]
        for y, lab, blk in (("hh", "His annual hours, years 1-3 after displacement", "His search"),
                            ("hlab", "His labor income, years 1-3 after displacement (2000 $)", "His earnings"),
                            ("fs", "SNAP (food stamp) receipt after his displacement, years 1-3", "Safety net"),
                            ("bw_present", "Still with wife, years 1-3 after his displacement", "Separation")):
            key = (y, race)
            mdl, names, cl, qq = es(q, y, key)
            nev = int(qq.loc[qq.treat == 1, "unit"].nunique())
            S.add(f"psid_es_{y}_13_{rb}", blk, f"{lab}, {race}", comb_fn(key, m13), mdl.N, W_PSID,
                  "IGE/19 (IGE/60)", dES + f" Mean of e = +1..+3. Outcome {y}; head's race {race}.", coef=True,
                  n_events=nev)
        S.add(f"psid_es_hlab_6_{rb}", "His earnings", f"His labor income, year 6 after displacement (2000 $), {race}",
              comb_fn(("hlab", race), {"d6": 1.0}), ESM[("hlab", race)][0].N, W_PSID, "IGE/19 (IGE/60)",
              dES + f" Coefficient at e = +6; head's race {race}.", coef=True)
    for kid, f in (("05", lambda x: x[x["young0"] <= 5]), ("617", lambda x: x[x["young0"] >= 6])):
        for y, lab in (("w_hrs", "Wife's annual hours"), ("w_emp", "Wife employed")):
            key = (y, kid)
            mdl, names, cl, qq = es(f(P), y, key)
            S.add(f"psid_es_{y}_13_y{kid}", "Added work", f"{lab}, years 1-3 after his displacement, youngest "
                  f"{'0-5' if kid == '05' else '6-17'}", comb_fn(key, m13), mdl.N, W_PSID, "IGE/19 (IGE/60)",
                  dES + " Mean of e = +1..+3; wife present at baseline, outcome while she is the baseline wife; "
                  "youngest child at baseline.", coef=True, n_events=int(qq.loc[qq.treat == 1, "unit"].nunique()))

    # ---------------- 38: gross response and joint-loss offset (interaction model)
    Q = P[P["w0"].notna()].dropna(subset=["J", "w_hrs"]).reset_index(drop=True)

    def inter_x(q):
        cols, names = [], []
        for e in ES_E:
            ind = (q["e"] == e).to_numpy(float)
            cols += [ind * q["treat"].to_numpy(), ind * q["J"].to_numpy(), ind * q["treat"].to_numpy() * q["J"].to_numpy()]
            names += [f"d{e}", f"j{e}", f"t{e}"]
        return np.column_stack(cols), names
    d38 = ("38's interaction model on 19's stacks (events 1984-2021, outcome years to 2021, wife present at baseline, J "
           "defined): displaced x e, J x e, displaced x J x e, J = the baseline wife's own displacement dated ev-1..ev+1 "
           "(0 if she did not work at baseline); outcome wife's annual hours.")
    for kid, q in (("all", Q), ("05", Q[Q["young0"] <= 5].reset_index(drop=True))):
        mdl, names, cl, qq = es_model(q, "w_hrs", inter_x)
        uu = qq.drop_duplicates("unit")
        ucl, ut, uJ = cc(uu["fam68"].to_numpy()), uu["treat"].to_numpy(float), uu["J"].to_numpy(float)
        ix = {nm: i for i, nm in enumerate(names)}

        def gross(c, mdl=mdl, cl=cl, ix=ix):
            b = mdl.fitc(c, cl)
            return float(np.mean([b[ix[f"d{e}"]] for e in (1, 2, 3)]))
        S.add(f"psid_gross_{kid}", "Added work", "Gross response of the wife's hours (wife kept her job), years 1-3, "
              + ("all" if kid == "all" else "youngest 0-5"), gross, mdl.N, W_PSID, "IGE/38 (IGE/60)",
              d38 + " Gross = mean of displaced x e, e = +1..+3 (displaced families whose wife was not displaced vs "
              "control families whose wife was not displaced).", coef=True, n_events=int(ut.sum()))
        if kid == "all":
            def offset(c, mdl=mdl, cl=cl, ix=ix, ucl=ucl, ut=ut, uJ=uJ):
                b = mdl.fitc(c, cl)
                wu = c[ucl]
                P1 = (wu * ut * uJ).sum() / (wu * ut).sum()
                P0 = (wu * (1 - ut) * uJ).sum() / (wu * (1 - ut)).sum()
                jm = np.mean([b[ix[f"j{e}"]] for e in (1, 2, 3)])
                tm = np.mean([b[ix[f"t{e}"]] for e in (1, 2, 3)])
                return float((P1 - P0) * jm + P1 * tm)
            S.add("psid_offset_all", "Added work", "Offset of the wife's hours response from joint losses, years 1-3",
                  offset, mdl.N, W_PSID, "IGE/38 (IGE/60)",
                  d38 + " Offset = (P1 - P0) x own + P1 x triple (means over e = +1..+3), P1 / P0 = share of J among "
                  "displaced / control father-stacks; implied net = gross + offset.", coef=True)

    # ---------------- 25: cost of the wife's own displacement (her labor income)
    BINS = {"pre3": [-3], "pre1": [-1], "e0": [0], "post13": [1, 2, 3], "post46": [4, 5, 6]}
    Qb = P[P["w0"].notna()].dropna(subset=["J", "w_lab"]).reset_index(drop=True)

    def bin_x(q):
        cols, names = [], []
        for bn, es_ in BINS.items():
            ind = q["e"].isin(es_).to_numpy(float)
            cols += [ind * q["treat"].to_numpy(), ind * q["J"].to_numpy(), ind * q["treat"].to_numpy() * q["J"].to_numpy()]
            names += [f"d_{bn}", f"m_J_{bn}", f"dm_J_{bn}"]
        return np.column_stack(cols), names
    mdl, names, cl, qq = es_model(Qb, "w_lab", bin_x)
    ib = names.index("m_J_post13")
    S.add("psid_wife_own_disp_lab13", "Her earnings", "Her labor income after her own displacement, years 1-3 (2000 $)",
          (lambda c: float(mdl.fitc(c, cl)[ib])), mdl.N, W_PSID, "IGE/25 (IGE/60)",
          "25's income accounting: 19's stacks (events 1984-2021, outcome years to 2021, wife present at baseline, J "
          "defined), event-time bins (ref. e = -2) x displaced, x J and x displaced x J; the moment is bin(+1..+3) x J: "
          "the change in her labor income that comes with her own displacement in ev-1..ev+1 among control families.",
          coef=True, n_events=int(qq.loc[(qq.treat == 0) & (qq.J == 1), "unit"].nunique()))

    # ---------------- 38: permanent vs contemporaneous component (events 1987-2021)
    WS = U[U["ev"].between(1987, 2021) & (U["wemp0"] == 1)].dropna(subset=["main_W", "main_PL"])
    Ld = pd.concat([WS.assign(win=0, y=WS["main_PL"]), WS.assign(win=1, y=WS["main_W"])], ignore_index=True)
    ever = ((Ld["treat"] == 1) | (Ld["pseudo"] == 1)).to_numpy(float)
    tw = (Ld["treat"] * Ld["win"]).to_numpy(float)
    gW, uW = pd.factorize(Ld["ev"] * 10 + Ld["win"])
    Yd, cld = Ld["y"].to_numpy(float), cc(Ld["fam68"].to_numpy())
    Xd = np.column_stack([ever, tw])
    d38b = ("38's two-window design: father x stack units with the wife employed at baseline, events 1987-2021, both "
            "windows covered; two rows per couple (placebo window ev-4..ev-2, window ev-1..ev+1); y = wife displaced in "
            "the window; event year x window FE; regressors: husband ever displaced (treated or future placebo, first "
            "displacement in ev+4..ev+6) and treated x window.")
    S.add("psid_perm", "Joint loss, annual", "Permanent couple component", lambda c: float(fe_ols(Yd, Xd, gW, len(uW),
          c[cld])[0]), len(Ld), "PSID 1987-2021", "IGE/38 (IGE/60)", d38b + " Coefficient on 'ever displaced'.",
          coef=True, n_events=int(WS.treat.sum()))
    S.add("psid_contemp", "Joint loss, annual", "Contemporaneous component", lambda c: float(fe_ols(Yd, Xd, gW,
          len(uW), c[cld])[1]), len(Ld), "PSID 1987-2021", "IGE/38 (IGE/60)", d38b + " Coefficient on treated x "
          "window.", coef=True, n_events=int(WS.treat.sum()))

    # ---------------- 25: couple-years, same interval
    cy = CY[CY["year"] <= 2021].dropna(subset=["h", "w"]).reset_index(drop=True)
    hcy, wcy, clcy = cy["h"].to_numpy(float), cy["w"].to_numpy(float), cc(cy["fam68"].to_numpy())
    dcy = ("25's couple-years: consecutive interviews of the same couple, both spouses with positive annual hours in the "
           "earlier year, intervals ending 1984-2021 (one year to 1996, two years after); h / w = husband / wife "
           "displaced (closure, layoff or firing; own reports) in the interval.")
    for k, lab, mk in (("all", "all couple-years", np.ones(len(cy), bool)),
                       ("same", "same sector (16 sectors)", (cy["s_sec"] == 1).to_numpy()),
                       ("diff", "different sector", (cy["s_sec"] == 0).to_numpy())):
        def dif(c, mk=mk):
            w = c[clcy] * mk
            return wmean(wcy[hcy == 1], w[hcy == 1]) - wmean(wcy[hcy == 0], w[hcy == 0])
        S.add(f"psid_cy_diff_{k}", "Joint loss, annual", f"P(she displaced | he is) - P( | he is not), same interval, "
              f"{lab}", dif, int(mk.sum()), W_PSID, "IGE/25 (IGE/60)", dcy + " Sector match at the interview opening "
              "the interval.", coef=True, n_events=int((hcy[mk] == 1).sum()))
    for race in ("Black", "White"):
        mk = (cy["hrace"] == race).to_numpy() & (hcy == 0)
        S.add(f"psid_cy_wbase_{race[0]}", "Base hazards", f"Wife's displacement rate per interval when he is not "
              f"displaced, {race}", (lambda c, mk=mk: wmean(wcy[mk], c[clcy][mk])), int(mk.sum()), W_PSID,
              "IGE/25 (IGE/60)", dcy + " P(w | not h); identifying moment of her own hazard (parameter table).")

    # ---------------- husband's annual displacement rate (19 section 1), married male heads
    x = m[["pid", "fam68", "year", "hh", "hrace", "age", "w_pid"]].merge(
        d[["pid", "year", "main"]], on=["pid", "year"], how="left").sort_values(["pid", "year"])
    x["main"] = x["main"].fillna(0)
    x["hprev"] = x.groupby("pid")["hh"].shift(1)
    x["yprev"] = x.groupby("pid")["year"].shift(1)
    x = x[(x["hprev"] > 0) & (x["year"] - x["yprev"] <= 2) & x["age"].between(20, 60) & x["year"].between(1984, 2021)
          & x["w_pid"].notna()]
    for race in ("Black", "White"):
        q = x[x["hrace"] == race]
        yv, clv = q["main"].to_numpy(float), cc(q["fam68"].to_numpy())
        S.add(f"psid_h_disp_rate_{race[0]}", "Base hazards", f"Husband's annual displacement rate, working married "
              f"male heads, {race}", (lambda c, yv=yv, clv=clv: wmean(yv, c[clv])), len(q), W_PSID,
              "IGE/19 (IGE/60)", "19's measure (section 1): share of male heads aged 20-60 with positive hours in the "
              "previous observed year who report a main displacement (closure, layoff/firing) dated to that calendar "
              "year; restricted here to heads with a wife present (the model's husbands); observed years 1984-2021.")

    # ---------------- T28: over-dispersion of displacement counts (identification plan, Sec. 1.4)
    cnt = x.groupby("pid").agg(fam68=("fam68", "first"), hrace=("hrace", "first"), N=("main", "size"),
                               k=("main", "sum")).reset_index()
    cnt = cnt[cnt["N"] >= 10]
    for race in ("Black", "White"):
        q = cnt[cnt["hrace"] == race]
        yv, clv = (q["k"] >= 2).to_numpy(float), cc(q["fam68"].to_numpy())
        S.add(f"psid_disp2plus_{race[0]}", "Base hazards", f"Share of husbands displaced two or more times among "
              f"husbands observed 10+ years, {race} (T28)", (lambda c, yv=yv, clv=clv: wmean(yv, c[clv])), len(q),
              W_PSID, "IGE/19 (IGE/60)", "Husbands = the risk set of the annual displacement rate above (married "
              "male heads aged 20-60 with positive hours in the previous observed year), observed years 1984-2021; "
              "N = number of such observed years per husband (interview years only: one a year to 1996, every "
              "other year after), kept if N >= 10; share with two or more main displacements (19's definition: "
              f"closure or layoff/firing) dated to those years. Mean N {q['N'].mean():.1f}; T28 of "
              "proposals/paperA_identification_plan.md (over-dispersion along the (p_H, m_H) ridge).",
              n_events=int((q["k"] >= 2).sum()))

    # ---------------- couple-year levels (married couples, wife 25-59 in the income year)
    cpl = m[m["w_pid"].notna() & m["year"].between(1984, 2021)].copy()
    cpl["w_agey"] = cpl["w_age"] - 1
    cpl = cpl[cpl["w_agey"].between(25, 59)]
    clc = cc(cpl["fam68"].to_numpy())
    dlev = ("PSID married couples (male head, wife present, head Black or White), income years 1984-2021, wife aged "
            "25-59 in the income year (interview age - 1); annual hours from the family file.")
    wh, hhv = cpl["wh"].to_numpy(float), cpl["hh"].to_numpy(float)
    yg = cpl["youngest"].to_numpy(float)
    for k, lab, mk in (("none", "no child under 18", np.isnan(yg)), ("05", "youngest 0-5", yg <= 5),
                       ("617", "youngest 6-17", (yg >= 6) & (yg <= 17))):
        mk = mk & np.isfinite(wh)
        S.add(f"psid_wemp_{k}", "Employment levels", f"Wives' employment, {lab}",
              (lambda c, mk=mk: wmean((wh[mk] > 0).astype(float), c[clc][mk])), int(mk.sum()), W_PSID,
              "IGE/60", dlev + " Employed = positive annual hours; youngest child in the family unit at the interview.")
    for k, lab, hv in (("w", "employed wives", wh), ("h", "employed husbands", hhv)):
        mk = np.isfinite(hv) & (hv > 0)
        S.add(f"psid_pt_{k}", "Employment levels", f"Part-time share of {lab}",
              (lambda c, mk=mk, hv=hv: wmean((hv[mk] < 1560).astype(float), c[clc][mk])), int(mk.sum()), W_PSID,
              "IGE/60", dlev + " Part-time = annual hours below 1,560 (midway between the model's part-time 87 x 12 = "
              "1,044 and full-time 173 x 12 = 2,076 hours) among those with positive hours.")
    # husband's employment rate by race (Fable review 2026-10-18, Sections 3.6 / 5.4; PI-approved): disciplines the
    # husband's job finding and the SNAP-eligible mass together
    for race in ("Black", "White"):
        mk = (cpl["hrace"] == race).to_numpy() & np.isfinite(hhv)
        S.add(f"psid_hemp_{race[0]}", "Employment levels", f"Husbands' employment, {race}",
              (lambda c, mk=mk: wmean((hhv[mk] > 0).astype(float), c[clc][mk])), int(mk.sum()), W_PSID, "IGE/60",
              dlev + " Employed = positive annual hours of the husband (head) in the income year; same couple-years "
              "as the SNAP receipt moments.")
    fs = cpl["fs"].to_numpy(float)
    for race in ("Black", "White"):
        mk = (cpl["hrace"] == race).to_numpy() & np.isfinite(fs)
        S.add(f"psid_snap_{race[0]}", "Safety net", f"SNAP receipt of couples, {race}",
              (lambda c, mk=mk: wmean(fs[mk], c[clc][mk])), int(mk.sum()), W_PSID, "IGE/60",
              dlev + " Family received food stamps / SNAP in the income year (19's item).")
    # separation hazard
    s = m[m["w_pid"].notna()][["pid", "fam68", "year", "w_pid", "hrace", "w_age"]].copy()
    allm = m[["pid", "year", "w_pid"]].sort_values(["pid", "year"])
    nxt = allm.assign(ny=allm.groupby("pid")["year"].shift(-1), nw=allm.groupby("pid")["w_pid"].shift(-1))
    s = s.merge(nxt[["pid", "year", "ny", "nw"]], on=["pid", "year"], how="left")
    s["L"] = s["ny"] - s["year"]
    s = s[s["L"].between(1, 2) & s["year"].between(1984, 2021) & (s["ny"] <= 2021) & (s["w_age"] - 1).between(25, 59)]
    s["sep"] = (s["nw"] != s["w_pid"]).astype(float)
    for race in ("Black", "White"):
        q = s[s["hrace"] == race]
        sv, Lv, clv = q["sep"].to_numpy(), q["L"].to_numpy(float), cc(q["fam68"].to_numpy())
        S.add(f"psid_sep_rate_{race[0]}", "Separation", f"Annual separation rate of couples, {race}",
              (lambda c, sv=sv, Lv=Lv, clv=clv: float((c[clv] * sv).sum() / (c[clv] * Lv).sum())), len(q), W_PSID,
              "IGE/60", "Married couples (wife 25-59) whose husband is observed at the next interview (one year later "
              "to 1997, two years after): separations (the baseline wife is no longer his wife: divorce, separation or "
              "her death) per couple-year of exposure (sum of interval lengths); intervals ending by 2021.",
              n_events=int(q["sep"].sum()))
    # wage growth of the continuously employed
    g = cpl[["pid", "fam68", "year", "w_pid", "hh", "wh", "hlab", "wlab", "age", "w_agey"]].copy()
    g["h_agey"] = g["age"] - 1
    for sx, hc, lc in (("h", "hh", "hlab"), ("w", "wh", "wlab")):
        g[f"lw_{sx}"] = np.log((g[lc] / g[hc]).where((g[hc] >= 1000) & (g[lc] > 0)))
        g.loc[~(np.exp(g[f"lw_{sx}"]).between(2, 200)), f"lw_{sx}"] = np.nan
    gi = g.set_index(["pid", "year"])
    for k in (1, 2):
        nx = gi[["w_pid", "lw_h", "lw_w", "hh", "wh"]].rename(columns=lambda c: f"{c}_{k}")
        nx.index = nx.index.set_levels(nx.index.levels[1] - k, level=1)
        g = g.merge(nx.reset_index(), on=["pid", "year"], how="left")
    g = g[(g["w_pid_2"] == g["w_pid"]) & (g["year"] + 2 <= 2021)]
    dwg = ("Two-year change in the log hourly wage (annual labor income / annual hours, 2000 $, $2-$200) of spouses "
           "with at least 1,000 annual hours in t and t+2 and, where the PSID observes it (annual interviews to 1996), "
           "in t+1; same couple in t and t+2; age of that spouse in t (interview age - 1); t = 1984-2019.")
    for sx, who in (("w", "wives"), ("h", "husbands")):
        hc = "wh" if sx == "w" else "hh"
        cont = g[f"lw_{sx}"].notna() & g[f"lw_{sx}_2"].notna() & (g[f"{hc}_1"].isna() | (g[f"{hc}_1"] >= 1000))
        dl = (g[f"lw_{sx}_2"] - g[f"lw_{sx}"]).to_numpy(float)
        ag = g["w_agey" if sx == "w" else "h_agey"].to_numpy(float)
        clg = cc(g["fam68"].to_numpy())
        for lo, hi in ((25, 34), (35, 44), (45, 54)):
            mk = cont.to_numpy() & (ag >= lo) & (ag <= hi)
            S.add(f"psid_wg_{sx}_{lo}", "Wage growth", f"Two-year log wage growth, continuously employed {who}, ages "
                  f"{lo}-{hi}", (lambda c, mk=mk, dl=dl, clg=clg: wmean(dl[mk], c[clg][mk])), int(mk.sum()), W_PSID,
                  "IGE/60", dwg)
    # her log wage at re-entry after 12+ months out (annual interviews)
    prv = gi[["w_pid", "wh"]].rename(columns=lambda c: f"{c}_p")
    prv.index = prv.index.set_levels(prv.index.levels[1] + 1, level=1)
    r = cpl[["pid", "fam68", "year", "w_pid", "wh", "wlab", "w_agey"]].merge(prv.reset_index(), on=["pid", "year"],
                                                                              how="left")
    r = r[(r["w_pid_p"] == r["w_pid"]) & r["year"].between(1985, 1996)]
    r["lw"] = np.log((r["wlab"] / r["wh"]).where((r["wh"] >= 260) & (r["wlab"] > 0)))
    r = r[np.exp(r["lw"]).between(2, 200)]
    re_ = (r["wh_p"] == 0) & (r["wh"] > 0)
    co_ = (r["wh_p"] >= 1000) & (r["wh"] >= 1000)
    r = r[re_ | co_].reset_index(drop=True)
    r["re"] = ((r["wh_p"] == 0)).astype(float)
    agd = np.column_stack([r["w_agey"].between(35, 44).to_numpy(float), r["w_agey"].between(45, 59).to_numpy(float)])
    Xr = np.column_stack([r["re"].to_numpy(float), agd])
    gr, ur = pd.factorize(r["year"])
    Yr, clr = r["lw"].to_numpy(float), cc(r["fam68"].to_numpy())
    S.add("psid_reentry_wage", "Wage growth", "Her log wage at re-entry after 12+ months out, relative to continuously "
          "employed wives", lambda c: float(fe_ols(Yr, Xr, gr, len(ur), c[clr])[0]), len(r), "PSID 1985-1996",
          "IGE/60", "Married wives (25-59, same couple both years); re-entrants: zero annual hours in t-1 (a full "
          "calendar year out) and at least 260 hours in t; comparison: at least 1,000 hours in t-1 and t; log hourly "
          "wage in t ($2-$200, 2000 $); OLS with calendar-year FE and wife's age group (25-34 / 35-44 / 45-59); income "
          "years 1985-1996 only, because the biennial survey does not observe the year t-1.", coef=True,
          n_events=int(r["re"].sum()))
    # liquid wealth
    wl = Wl.merge(m[["pid", "fam68", "wave", "w_pid", "w_age", "hlab", "wlab"]].rename(columns={"pid": "id"}),
                  on=["id", "wave"])
    wl = wl[wl["w_pid"].notna() & wl["w_age"].between(25, 59) & wl["liquid"].notna()].copy()
    wl["liq"] = wl["liquid"] * 5.82                                     # ReducedForm/17: units x 5.82 = 2000 $
    wl["earn"] = wl["hlab"].fillna(0) + wl["wlab"].fillna(0)
    lq, ea, wa_ = wl["liq"].to_numpy(float), wl["earn"].to_numpy(float), wl["w_age"].to_numpy(float)
    clw = cc(wl["fam68"].to_numpy())
    dwl = ("Liquid wealth = checking/savings (+ bonds/CDs from 2019) + stocks - unsecured debt, PSID imputed components "
           "(estimation/psid_wealth.py, the ReducedForm/17 construction), 2000 $; married couples (husband head), "
           "wife's age at the wealth interview; waves 1984, 1989, 1994, 1999-2019 (the 2021 wave is not in "
           "psid_wealth.py). 'Above one year of earnings' = liquid wealth above the couple's labor income (head + wife) "
           "of the income year before the interview.")
    for lo, hi in ((25, 34), (35, 44), (45, 59)):
        mk = (wa_ >= lo) & (wa_ <= hi)
        S.add(f"psid_liq_le0_{lo}", "Wealth", f"Share of couples with liquid wealth <= 0, wife {lo}-{hi}",
              (lambda c, mk=mk: wmean((lq[mk] <= 0).astype(float), c[clw][mk])), int(mk.sum()),
              "PSID 1984-2019 (wealth waves)", "ReducedForm/17 (IGE/60)", dwl)
        S.add(f"psid_liq_hi_{lo}", "Wealth", f"Share of couples with liquid wealth above one year of earnings, wife "
              f"{lo}-{hi}", (lambda c, mk=mk: wmean((lq[mk] > ea[mk]).astype(float), c[clw][mk])), int(mk.sum()),
              "PSID 1984-2019 (wealth waves)", "ReducedForm/17 (IGE/60)", dwl)

    # ---------------- consumption (47), all married couples, log total consumption
    KS = [-2, 0, 1, 2, 3]
    qc0 = Qc.dropna(subset=["lc", "J"]).copy()
    qc0 = qc0[qc0.groupby("unit")["lc"].transform("size") >= 2].reset_index(drop=True)

    def cx(q):
        cols, names = [], []
        for k in KS:
            ind = (q["k"] == k).to_numpy(float)
            t, J = q["treat"].to_numpy(float), q["J"].to_numpy(float)
            cols += [ind * t, ind * J, ind * t * J]
            names += [f"d{k}", f"j{k}", f"t{k}"]
        return np.column_stack(cols), names
    dc = ("47's stacked event study on Paper A's PSID consumption measure (BPS nondurables + services, 6% rent "
          "equivalent, 2000 $): 19's stacks with events 2000-2020, married at baseline (all married couples), event "
          "time in interview waves, reference k = -1, father x stack and wave x stack FE; interaction model displaced x "
          "k, J x k, displaced x J x k; outcome log total consumption; mean of k = +1..+3 (first three interviews after "
          "the job-end year); units with >= 2 interviews.")
    for race in ("All", "Black", "White"):
        q = qc0 if race == "All" else qc0[qc0["hrace"] == race].reset_index(drop=True)
        Xc, names = cx(q)
        mdlc = TWFE(q["lc"].to_numpy(float), Xc, [q["unit"].to_numpy(), q["cell"].to_numpy()])
        clq = cc(q["fam68"].to_numpy())
        ix = {nm: i for i, nm in enumerate(names)}
        nd_ = int(q.loc[q.treat == 1, "unit"].nunique())
        nj_ = int(q.loc[(q.treat == 1) & (q.J == 1), "unit"].nunique())
        S.add(f"psid_cons_single_{race.lower()}", "Consumption", f"Change in log total consumption, first three "
              f"interviews after his single displacement, married couples, {race.lower() if race != 'All' else 'pooled'}",
              (lambda c, mdl=mdlc, clq=clq, ix=ix: _cons_comb(mdl, clq, ix, c, ("d",))), mdlc.N, W_PSIDC,
              "IGE/47 (IGE/60)", dc + " Husband displaced alone = displaced x k.", coef=True, n_events=nd_)
        if race == "All":
            S.add("psid_cons_wife_alone", "Consumption", "Same after her own displacement (he not displaced)",
                  (lambda c, mdl=mdlc, clq=clq, ix=ix: _cons_comb(mdl, clq, ix, c, ("j",))), mdlc.N, W_PSIDC,
                  "IGE/47 (IGE/60)", dc + " Wife displaced alone = J x k among control families.", coef=True)
            S.add("psid_cons_joint_minus_single", "Consumption", "Joint minus single displacement",
                  (lambda c, mdl=mdlc, clq=clq, ix=ix: _cons_comb(mdl, clq, ix, c, ("j", "t"))), mdlc.N, W_PSIDC,
                  "IGE/47 (IGE/60)", dc + " Both - husband alone = J x k + displaced x J x k.", coef=True,
                  n_events=nj_)
    return S


def _cons_comb(mdl, clq, ix, c, pfx):
    b = mdl.fitc(c, clq)
    return float(np.mean([sum(b[ix[f"{p}{k}"]] for p in pfx) for k in (1, 2, 3)]))


# =====================================================================================================
# DWS: UI receipt of displaced husbands and wives (q_UI; calibration input)
# =====================================================================================================
def dws_source():
    m39 = _load("dws39", "39.CPSDisplacedWorkers.py")
    path = sorted(m39.RAW.glob("cps_*.csv.gz"))[-1]               # local IPUMS extract of 39 (no API call)
    c, _ = m39.couples(path)
    S = Source("dws")
    hhs = pd.Index(pd.unique(c["hh"]))
    S.G = len(hhs)
    log(f"DWS: {len(c):,} couples, {S.G:,} households")
    dd = ("CPS Displaced Worker Supplements 1984-2024 (39's couples: married, both 20-64, both in the supplement; 39's "
          "harmonised displacement = lost a wage job in the three calendar years before the survey to a plant closing, "
          "insufficient work or an abolished position); UI = DWBEN 'received unemployment benefits' (yes / no; missing "
          "answers dropped), received at any time between the loss and the survey; weighted by the person's "
          "supplement weight (DWSUPPWT).")
    parts = {}
    for s, who in (("h", "husbands"), ("w", "wives")):
        q = c[(c[f"{s}_disp"] == 1) & c[f"{s}_ui"].notna()]
        y, wt, cl = q[f"{s}_ui"].to_numpy(float), q[f"{s}_wt"].to_numpy(float), cluster_codes(q["hh"].to_numpy(), hhs)
        parts[s] = (y, wt, cl)
        S.add(f"dws_ui_{s}", "Calibration input (UI take-up, not a target)", f"Share of displaced {who} who received "
              "UI (q_UI)", (lambda c_, y=y, wt=wt, cl=cl: wmean(y, c_[cl] * wt)), len(q), "CPS DWS 1984-2024",
              "IGE/39 (IGE/60)", dd, target=False)
    (yh, wh_, clh), (yw, ww_, clw) = parts["h"], parts["w"]
    S.add("dws_ui_w_minus_h", "Calibration input (UI take-up, not a target)", "UI receipt share, displaced wives minus "
          "displaced husbands", lambda c_: wmean(yw, c_[clw] * ww_) - wmean(yh, c_[clh] * wh_), len(yh) + len(yw),
          "CPS DWS 1984-2024", "IGE/39 (IGE/60)", dd + " Difference of the two shares; s.e. from the household "
          "bootstrap (both spouses of a household drawn together).", coef=True, target=False)
    return S


# =====================================================================================================
# validation copied from IGE/50
# =====================================================================================================
def awe_rows():
    f = OUT / "cps_awe_by_age.csv"
    if not f.exists():
        return []
    a = pd.read_csv(f)
    a = a[(a["table"] == "1_awe") & (a["outcome"] == "LF") & a["sample"].str.startswith("main: ")]
    out = []
    for r in a.itertuples():
        lab, reg = r.sample.replace("main: ", "").replace("All", "all ages"), r.regressor
        r = pd.Series(r._asdict())
        out.append(dict(id=f"val_awe_{reg.lower()}", block="Validation (not a target)",
                        moment=f"Added-worker effect (Bacher et al. definition), {lab}", value=r["coef"], se=r["se_hh"],
                        n=int(r["n"]), window="CPS 1994-Feb 2020", source_script="IGE/50 (in progress; copied as "
                        "found in output/cps_awe_by_age.csv)",
                        definition="IGE/50 main variant (sex-neutral, EHS-adjusted, all EU): spouse not in the labor "
                        "force at m-1 enters (NE or NU) in the month the primary earner moves E -> U, minus the same "
                        "when the primary earner stays employed; weighted LPM; s.e. clustered by household (50's "
                        "analytical s.e., not bootstrapped; not in the vcov files).",
                        p=r["p_hh"], data_source="cps", target=False, n_events=r.get("n_treat", np.nan), coef=True))
    return out


# =====================================================================================================
# output
# =====================================================================================================
def finish(results, reps, runtime):
    rows = []
    for src, (S, vals, Bt) in results.items():
        for m in S.M:
            v, se = vals[m["id"]], float(np.nanstd(Bt[m["id"]].to_numpy(), ddof=1))
            p = 2 * norm.sf(abs(v / se)) if (m["coef"] and se > 0) else np.nan
            rows.append(dict(block=m["block"], moment=m["moment"], value=v, se=se, n=m["n"], window=m["window"],
                             source_script=m["source_script"], definition=m["definition"], id=m["id"], p=p,
                             stars=stars(p) if p == p else "", data_source=src, target=int(m["target"]),
                             n_events=m["n_events"], reps_ok=int(np.isfinite(Bt[m["id"]]).sum())))
        ids = [m["id"] for m in S.M if m["target"]] or [m["id"] for m in S.M]     # dws: calibration inputs only
        Bt[ids].cov().to_csv(OUT / f"paperA_targets_vcov_{src}.csv")
    for r in awe_rows():
        r["stars"] = stars(r["p"]) if r["p"] == r["p"] else ""
        r["target"] = 0
        rows.append(r)
    D = pd.DataFrame(rows)
    order = ["Joint loss, monthly", "Joint loss, annual", "Base hazards", "Her search", "Her exits", "His search",
             "His earnings", "Her earnings", "Wage growth", "Added work", "Employment levels", "Safety net",
             "Separation", "Wealth", "Consumption", "Calibration check (not a target)",
             "Calibration input (UI take-up, not a target)", "Validation (not a target)"]
    D["_o"] = D["block"].map({b: i for i, b in enumerate(order)})
    D = D.sort_values(["_o"], kind="stable").drop(columns=["_o", "coef"], errors="ignore")
    cols = ["block", "moment", "value", "se", "n", "window", "source_script", "definition", "id", "p", "stars",
            "data_source", "target", "n_events", "reps_ok"]
    D = D[[c for c in cols if c in D]]
    prev = OUT / "paperA_targets.csv"
    if prev.exists() and len(results) < 4:                    # partial run: keep the other sources' rows
        old = pd.read_csv(prev)
        old = old[~old["data_source"].isin(list(results)) & ~old["id"].str.startswith("val_")]
        D = pd.concat([old, D], ignore_index=True)
        D["_o"] = D["block"].map({b: i for i, b in enumerate(order)})
        D = D.sort_values(["_o"], kind="stable").drop(columns=["_o"])
    D = append_external_targets(D)
    D.to_csv(prev, index=False)
    write_md(D, reps, runtime)
    return D


def append_external_targets(D):
    """Targets computed by other scripts in the same row format: T7, the CPS husband's monthly non-temporary
    job-loss rate by race (IGE/62.PaperAInputs.py -> output/paperA_inputs_T7.csv). Appended once (by id); not in the
    bootstrap vcov files (diagonal weighting uses its own s.e.)."""
    f = OUT / "paperA_inputs_T7.csv"
    if f.exists():
        ext = pd.read_csv(f)
        ext = ext[~ext["id"].isin(D["id"])]
        if len(ext):
            D = pd.concat([D, ext], ignore_index=True)
    return D


def fmtv(v, se, coef, p):
    big = abs(v) >= 100 or (se == se and se >= 50)
    nd = 0 if big else (min(6, max(3, int(np.ceil(-np.log10(se))) + 1)) if (se == se and se > 0) else 3)
    f = (lambda x: f"{x:,.{nd}f}")
    s = f(v) + (stars(p) if coef and p == p else "")
    return s + (f" ({f(se)}" + (f"; p={'<0.001' if p < 0.001 else f'{p:.3f}'}" if coef and p == p else "") + ")")


def write_md(D, reps, runtime):
    md = ["# Paper A: SMM target moments with block-bootstrap standard errors", "",
          f"Built by `IGE/60.PaperATargets.py` (2026-10-18; definitions in its docstring and in the csv). Targets of "
          f"`paperA_joint_loss/model_document.tex`, Table 'Targets, windows and sources'. Standard errors: block "
          f"bootstrap, {reps} replications, clusters = 1968 family (PSID, incl. consumption), household (CPS, SIPP); "
          f"every moment of a source is recomputed on the same draw (vcov in `paperA_targets_vcov_<source>.csv`, "
          f"targets only). Coefficients: value*** (bootstrap s.e.; p, normal); *** p<0.01, ** p<0.05, * p<0.1; other "
          f"moments: value (s.e.). Runtime {runtime / 60:.0f} minutes. Associations, not causal effects.", ""]
    for blk, g in D.groupby("block", sort=False):
        md += [f"## {blk}", "", "| Moment | Value (s.e.) | N | Events | Window | Source |", "|---|---|---|---|---|---|"]
        for r in g.itertuples():
            coef = isinstance(r.stars, str) and (r.p == r.p)
            ne = f"{int(r.n_events):,}" if r.n_events == r.n_events and r.n_events is not None else ""
            mom = str(r.moment).replace("|", "\\|")
            md.append(f"| {mom} | {fmtv(r.value, r.se, coef, r.p)} | {int(r.n):,} | {ne} | {r.window} | "
                      f"{r.source_script} |")
        md.append("")
    md += ["## Definitions", ""]
    for r in D.itertuples():
        md.append(f"- `{r.id}` ({r.moment}): {r.definition}")
    (OUT / "paperA_targets.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=200)
    ap.add_argument("--only", default="cps,psid,sipp,dws")
    ap.add_argument("--build-only", action="store_true")
    ap.add_argument("--merge-external-only", action="store_true",
                    help="append T7 (IGE/62) to the existing paperA_targets.csv without re-running the bootstrap")
    a = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    if a.merge_external_only:
        prev = OUT / "paperA_targets.csv"
        D = append_external_targets(pd.read_csv(prev))
        D.to_csv(prev, index=False)
        print(f"{len(D)} rows; T7 rows: {D['id'].astype(str).str.startswith('cps_h_hazard').sum()}")
        return
    want = a.only.split(",")
    if a.build_only:
        if "psid" in want:
            psid_build()
        if "sipp" in want:
            m40 = _load("sipp40", "40.SIPPJointLoss.py")
            for panel, nw in m40.PANELS.items():
                for w in range(1, nw + 1):
                    if m40.src(panel, w)[1].exists():
                        sipp_earn_wave(m40, panel, w)
        return
    results = {}
    for i, (src, fn) in enumerate((("cps", cps_source), ("psid", psid_source), ("sipp", sipp_source),
                                   ("dws", dws_source))):
        if src not in want:
            continue
        S = fn()
        vals, Bt = S.run(a.reps, seed=6000 + i)
        results[src] = (S, vals, Bt)
        Bt.to_pickle(DATA / f"paperA_targets_boot_{src}.pkl")
    D = finish(results, a.reps, time.time() - T0)
    print(D[["block", "moment", "value", "se", "n"]].to_string())
    log("done")


if __name__ == "__main__":
    main()
