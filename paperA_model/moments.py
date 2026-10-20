"""Paper A model: the SMM target vector on simulated data, aligned with output/paperA_targets.csv (target == 1).

compute(res) builds the data-shaped panels (panels.py) from one simulation and computes every target T1-T28 with the
definitions of IGE/60.PaperATargets.py. IGE/60's estimators are imported read-only (wmean, fe_slope, fe_ols:
importlib, module 'ige60'); its two-way fixed-effects class (alternating projections, built for bootstrap weights) is
replaced on simulated data by twfe() below, the exact least-squares solution with unit and cell effects (the unit
effects absorbed by the within transformation, the few hundred cell effects solved jointly with the regressors);
tests/test_10_measurement.py checks that both give the same coefficients. Simulated weights are 1 (no survey or
bootstrap weights).

Objective (estimate.py): Q(theta) = (m_sim - m_data)' W (m_sim - m_data) over the moments in the objective. Weightings
(weights()): 'diag_noise' (estimate.py default since 2026-10-18) = diag(1 / (se^2 + var_sim)), var_sim the simulation
variance of each moment at the run's K (from a noise file: inputs/moment_noise.csv, written by estimate.py noise
--save-noise-input, scaled by K_noise / K); 'diag' = diag(1 / se^2) (the bootstrap standard errors of the targets file:
the identification plan's inverse-variance weighting); 'block' = equal total weight per block in z^2 units: the
diag_noise weights times N / (B n_b) (robustness run, plan Section 3; scale-free since 2026-10-20); 'vcov' = the inverse of the within-source bootstrap covariance
(block-diagonal across sources; diagnostics only: 200 replications for 56 PSID moments make the inverse noisy).
Moments in OBJ_EXCLUDE (and any --drop) get zero weight: they stay in moments.csv and the fit tables, marked
in_objective = 0. A moment in the objective that the simulation cannot produce (empty sample) adds MISSING_PENALTY.
"""
from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.sparse as sp

HERE = Path(__file__).resolve().parent
IGE = HERE.parent
TARGETS = IGE / "output" / "paperA_targets.csv"
TARGETS_EXT = IGE / "output" / "paperA_targets_ext.csv"     # IGE/66: rows of the 2026-10-19 extensions (column 'ext')
VCOV = {s: IGE / "output" / f"paperA_targets_vcov_{s}.csv" for s in ("cps", "psid", "sipp")}
MISSING_PENALTY = 1000.0
ES_E = [-3, -1, 0, 1, 2, 3, 4, 5, 6]                    # IGE/60 (reference e = -2)
KS = [-2, 0, 1, 2, 3]                                    # IGE/47 (reference k = -1)

# Targets kept in the fit tables but excluded from the objective (Fable review 2026-10-18, Section 6 item 1), one reason
# each. The pooled CPS rates are, in the model, exact linear combinations of the race-specific ones (compute(): the
# pooled sample is the union of the Black and White samples, moments.py 'pooled' rows), so they add no information and
# double the weight of the CPS rates; their data counterparts also include other races (n-weighted Black/White average
# vs pooled: wife hazard 0.002246 vs 0.002279, husband hazard 0.003592 vs 0.003690, entry 0.07612 vs 0.07498), which
# the model has no couples for. The SIPP 'no separation' rows cannot be produced: the model's husbands leave a job only
# by displacement (0.989 vs 0.983 at every theta).
OBJ_EXCLUDE = {
    "cps_wife_hazard_pooled": "pooled duplicate: model value = race-share average of cps_wife_hazard_black/white",
    "cps_h_hazard_pooled": "pooled duplicate: model value = race-share average of cps_h_hazard_B/W",
    "cps_entry_pooled": "pooled duplicate: model value = race-share average of cps_entry_black/white",
    "cps_entry_p_pooled": "pooled duplicate: model value = race-share average of cps_entry_p_black/white",
    "psid_hemp_B": "not producible: husbands leave work only by displacement (model 0.999 vs data 0.882)",
    "psid_hemp_W": "not producible: husbands leave work only by displacement (model 1.000 vs data 0.943)",
    "sipp_his_emp_s3_nosep": "not producible: husbands never quit (leave a job only by displacement)",
    "sipp_his_emp_s6_nosep": "not producible: husbands never quit (leave a job only by displacement)",
    "sipp_his_emp_s12_nosep": "not producible: husbands never quit (leave a job only by displacement)",
}
NOISE_INPUT = HERE / "inputs" / "moment_noise.csv"

# CPS response errors, women aged 25-59: Q[a, b] = P(recorded b | true a), a, b in (E, U, N). Poterba and Summers
# (1986, Econometrica 54(6); NBER WP 1436, Table II, reinterview surveys January-June 1981): q_EU 0.0029, q_EN 0.0168,
# q_UE 0.0380, q_UN 0.1688, q_NE 0.0106, q_NU 0.0062. Abowd and Zellner (1985, JBES) estimate errors of the same order
# from the same reinterview data. Applied to the simulated CPS entry and exit rates when the extension is on
# (estimate.py --cps-classif on): independent errors across months generate spurious E -> N -> E flows, which the
# model's true statuses do not contain.
CPS_CLASSIF_PS86_W2559 = np.array([[1 - 0.0029 - 0.0168, 0.0029, 0.0168],
                                   [0.0380, 1 - 0.0380 - 0.1688, 0.1688],
                                   [0.0106, 0.0062, 1 - 0.0106 - 0.0062]])

_I60 = None


def ige60():
    """IGE/60.PaperATargets.py imported read-only (its estimators)."""
    global _I60
    if _I60 is None:
        if str(IGE) not in sys.path:
            sys.path.insert(0, str(IGE))
        spec = importlib.util.spec_from_file_location("ige60", IGE / "60.PaperATargets.py")
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        _I60 = m
    return _I60


# ----------------------------------------------------------------------------------------------------------------------
def load_targets(path=TARGETS) -> pd.DataFrame:
    t = pd.read_csv(path)
    t = t[t["target"] == 1].reset_index(drop=True)
    return t[["id", "block", "moment", "value", "se", "n", "window", "data_source"]]


def load_targets_ext(exts, path=TARGETS_EXT) -> tuple[pd.DataFrame, list]:
    """Rows of the extension targets file (IGE/66) for the extensions in exts (e.g. ['new_job']), in the columns of
    load_targets, and the ids of the reported-only rows (target == 0: in the fit tables, outside the objective)."""
    exts = list(exts or [])
    if not exts:
        return load_targets().iloc[0:0], []
    t = pd.read_csv(path)
    t = t[t["ext"].isin(exts)].reset_index(drop=True)
    return t[["id", "block", "moment", "value", "se", "n", "window", "data_source"]], t.loc[t["target"] == 0,
                                                                                          "id"].tolist()


def load_vcov(ids) -> np.ndarray:
    """Block-diagonal covariance of the targets (within-source bootstrap vcov; zero across sources)."""
    ids = list(ids)
    V = np.zeros((len(ids), len(ids)))
    pos = {k: i for i, k in enumerate(ids)}
    for src, p in VCOV.items():
        if not p.exists():
            continue
        v = pd.read_csv(p, index_col=0)
        keep = [k for k in v.index if k in pos]
        ix = [pos[k] for k in keep]
        V[np.ix_(ix, ix)] = v.loc[keep, keep].to_numpy()
    return V


def objective_mask(targets: pd.DataFrame, exclude=None) -> np.ndarray:
    """True for the moments in the objective (exclude: ids with zero weight; None = none)."""
    ex = set(exclude or ())
    bad = ex - set(targets["id"])
    if bad:
        raise ValueError(f"excluded moments not in the targets: {sorted(bad)}")
    return ~targets["id"].isin(ex).to_numpy()


def load_sim_noise(path=None, K=None):
    """Simulation variance of each moment at K copies: (id -> var) from a noise file (columns id, sim_sd and optionally
    K; without a K column the file is taken to be at K = 3, the default of estimate.py noise). The variance of a
    simulated mean scales with 1 / K, so var(K) = sd^2 x K_noise / K."""
    path = Path(path) if path else NOISE_INPUT
    if not path.exists():
        raise FileNotFoundError(f"{path} missing: run estimate.py noise --weighting diag --save-noise-input (or pass "
                                f"--noise-file / --weighting diag)")
    d = pd.read_csv(path)
    k_noise = float(d["K"].iloc[0]) if "K" in d.columns else 3.0
    scale = k_noise / float(K) if K else 1.0
    return dict(zip(d["id"], d["sim_sd"].to_numpy(float) ** 2 * scale)), k_noise


def weights(targets: pd.DataFrame, kind="diag", exclude=None, noise_file=None, K=None) -> np.ndarray:
    """Weighting matrix (n_mom x n_mom); rows and columns of excluded moments are zero."""
    se = targets["se"].to_numpy(float)
    keep = objective_mask(targets, exclude)
    if kind == "diag_noise":
        var, _ = load_sim_noise(noise_file, K)
        vs = np.array([var.get(k, 0.0) for k in targets["id"]], float)
        vs = np.where(np.isfinite(vs), vs, 0.0)
        return np.diag(np.where(keep, 1.0 / (se ** 2 + vs), 0.0))
    if kind == "diag":
        return np.diag(np.where(keep, 1.0 / se ** 2, 0.0))
    if kind == "block":
        # equal weight per block in z^2 units (2026-10-20 fix; the earlier version equalised raw 1/se^2 sums, which
        # depend on each moment's units): the diag_noise weights times N / (B n_b), so a block of n_b moments counts
        # as N / B moments whatever its units and size
        w = np.diag(weights(targets, "diag_noise", exclude, noise_file, K))
        blocks = targets["block"].to_numpy()
        ub = np.unique(blocks[keep])
        out = np.zeros_like(w)
        for b in ub:
            mk = (blocks == b) & keep
            out[mk] = w[mk] * keep.sum() / (len(ub) * mk.sum())
        return np.diag(out)
    if kind == "vcov":
        V = load_vcov(targets["id"])
        d = np.diag(V).copy()
        d[d <= 0] = se[d <= 0] ** 2
        V[np.diag_indices_from(V)] = d
        out = np.zeros_like(V)
        ix = np.nonzero(keep)[0]
        out[np.ix_(ix, ix)] = np.linalg.pinv(V[np.ix_(ix, ix)])
        return out
    raise ValueError(kind)


def weight_shares(targets: pd.DataFrame, W) -> pd.DataFrame:
    """Share of the total weight by block in z units, w_i se_i^2 (unit-free: 1 per moment under 'diag', a little less
    under 'diag_noise', N / (B n_b) under 'block'), and the number of moments in the objective. Raw diagonal weights
    are not summed: they carry each moment's units (2026-10-20)."""
    w = np.diag(W) * targets["se"].to_numpy(float) ** 2
    d = pd.DataFrame({"block": targets["block"], "w": w, "in_obj": w > 0})
    g = d.groupby("block", sort=False).agg(moments=("in_obj", "size"), in_objective=("in_obj", "sum"), w=("w", "sum"))
    g["share"] = g["w"] / g["w"].sum()
    return g.drop(columns="w").sort_values("share", ascending=False)


def objective(m_sim, targets, W):
    """Q and the number of missing moments among those in the objective (non-zero diagonal weight)."""
    d = m_sim - targets["value"].to_numpy(float)
    miss = ~np.isfinite(d) & (np.diag(W) > 0)
    d = np.where(np.diag(W) > 0, d, 0.0)
    d0 = np.where(miss, 0.0, d)
    return float(d0 @ W @ d0 + MISSING_PENALTY * miss.sum()), int(miss.sum())


# ----------------------------------------------------------------------------------------------------------------------
def twfe(Y, X, unit, cell):
    """OLS of Y on X with unit and cell fixed effects (unweighted), exact: unit effects by the within transformation,
    cell effects jointly with X in the reduced normal equations (cells are few: year x stack)."""
    Y = np.asarray(Y, float)
    X = np.asarray(X, float).reshape(len(Y), -1)
    K = X.shape[1]
    uc, ui = np.unique(unit, return_inverse=True)
    cc, ci = np.unique(cell, return_inverse=True)
    nu, nc = len(uc), len(cc)
    cu = np.bincount(ui, minlength=nu).astype(float)
    dm = lambda v: v - (np.bincount(ui, weights=v, minlength=nu) / cu)[ui]       # noqa: E731
    Yw = dm(Y)
    Xw = np.column_stack([dm(X[:, j]) for j in range(K)])
    DX = np.column_stack([np.bincount(ci, weights=Xw[:, j], minlength=nc) for j in range(K)])
    DY = np.bincount(ci, weights=Yw, minlength=nc)
    M = sp.csr_matrix((np.ones(len(Y)), (ui, ci)), shape=(nu, nc))
    DD = np.diag(np.bincount(ci, minlength=nc).astype(float)) - (M.T @ sp.diags(1.0 / cu) @ M).toarray()
    A = np.block([[Xw.T @ Xw, DX.T], [DX, DD]])
    b = np.concatenate([Xw.T @ Yw, DY])
    return np.linalg.lstsq(A, b, rcond=None)[0][:K]


def _es_dummies(e, treat):
    return np.column_stack([((e == k) & (treat == 1)).astype(float) for k in ES_E]), [f"d{k}" for k in ES_E]


def _ok(*arrs):
    return all(len(a) > 0 for a in arrs)


# ----------------------------------------------------------------------------------------------------------------------
def compute(res, theta=None, merge_s12=True, ctrl_rate=0.15, cps_mode="all", timing=None, return_n=False,
            cps_classif=None, ext_moments=()):
    """Simulated counterparts of every target (dict id -> value; NaN when a sample is empty). cps_classif: 3 x 3 CPS
    classification-error matrix applied to the entry and exit rates (panels.cps_samples; None = none). ext_moments:
    extensions whose moments (IGE/66 targets) are also computed: 'new_job' (SIPP exit by job tenure, KM return within
    12 months, PSID repeat exits), 'her_sep' (still with the baseline husband after her displacement)."""
    import panels as PN
    I6 = ige60()
    wmean, fe_slope, fe_ols = I6.wmean, I6.fe_slope, I6.fe_ols
    t0 = time.perf_counter()
    R = PN.records(res, ctrl_rate, theta, merge_s12)
    out, N = {}, {}

    def put(k, v, n):
        out[k] = float(v) if v is not None and np.isfinite(v) else np.nan
        N[k] = int(n)

    def slope(s, mk=None):
        if mk is None:
            mk = np.ones(len(s["y"]), bool)
        y, H, g = s["y"][mk], s["H"][mk], s["g"][mk]
        if len(y) == 0 or H.sum() == 0 or H.sum() == len(H):
            return np.nan, len(y)
        gc, gu = pd.factorize(g)
        return fe_slope(y, H, gc, len(gu), np.ones(len(y))), len(y)

    # ---------------- CPS ----------------
    C = PN.cps_samples(R, mode=cps_mode, classif=cps_classif)
    s0 = C["tau"]
    v, n = slope(s0)
    put("cps_jl_nt", v, n)
    for k in (2, 1, 0):
        v, n = slope(s0, s0["s"] == k)
        put(f"cps_jl_nt_s{k}", v, n)
    for k, nm in ((-3, "m3"), (-2, "m2"), (-1, "m1"), (1, "p1"), (2, "p2"), (3, "p3")):
        v, n = slope(C[f"lag{k:+d}"])
        put(f"cps_jl_nt_{nm}", v, n)
    h0 = s0["H"] == 0
    for nm, mk in (("pooled", h0), ("black", h0 & (s0["race"] == 0)), ("white", h0 & (s0["race"] == 1))):
        put(f"cps_wife_hazard_{nm}", wmean(s0["y"][mk], np.ones(mk.sum())) if mk.any() else np.nan, mk.sum())
    for nm, mk in (("B", s0["race"] == 0), ("W", s0["race"] == 1), ("pooled", np.ones(len(s0["H"]), bool))):
        put(f"cps_h_hazard_{nm}", s0["H"][mk].mean() if mk.any() else np.nan, mk.sum())     # T7
    se_ = C["entry"]
    wt_en = se_.get("wt", np.ones(len(se_["y"])))
    for nm, mk in (("pooled", np.ones(len(se_["y"]), bool)), ("black", se_["race"] == 0), ("white", se_["race"] == 1)):
        put(f"cps_entry_{nm}", wmean(se_["y"][mk], wt_en[mk]) if mk.any() else np.nan, mk.sum())
    sx = C["exit"]
    put("cps_wife_exit", wmean(sx["y"], sx.get("wt", np.ones(len(sx["y"])))) if len(sx["y"]) else np.nan, len(sx["y"]))
    sp_ = C["entry_p"]                                     # persistent flows (two months before and after)
    for nm, mk in (("pooled", np.ones(len(sp_["y"]), bool)), ("black", sp_["race"] == 0), ("white", sp_["race"] == 1)):
        put(f"cps_entry_p_{nm}", sp_["y"][mk].mean() if mk.any() else np.nan, mk.sum())
    sx = C["exit_p"]
    put("cps_wife_exit_p", sx["y"].mean() if len(sx["y"]) else np.nan, len(sx["y"]))
    del C
    t_cps = time.perf_counter()

    # ---------------- SIPP ----------------
    AW, REE = PN.sipp_samples(R)
    for s_ in (0, 1, 6):
        v, n = slope(AW[f"wife_s{s_}"])
        put(f"sipp_wife_emp_s{s_}", v, n)
    for s_ in (3, 6, 12):
        a = AW[f"his_s{s_}"]
        for hv, lab in ((1, "sep"), (0, "nosep")):
            mk = a["H"] == hv
            put(f"sipp_his_emp_s{s_}_{lab}", a["y"][mk].mean() if mk.any() else np.nan, mk.sum())
    for sp_ in ("h", "w"):
        r = REE[sp_]
        for lo, hi in ((1, 3), (4, 12), (13, 24)):
            mk = (r["d"] >= lo) & (r["d"] <= hi)
            put(f"sipp_reemp_{sp_}_{lo}_{hi}", r["dl"][mk].mean() if mk.any() else np.nan, mk.sum())
    t_sipp = time.perf_counter()

    # ---------------- PSID ----------------
    U = PN.units(R, kids=True)
    P = PN.stack_rows(R, U)
    evmask = (P["ev"] >= 1984) & (P["ev"] <= 2021) & (P["Y"] <= 2021)
    P = {k: v[evmask] for k, v in P.items()}
    cache = {}

    def es_fit(mask, y, key, xs_fn=None):
        if key in cache:
            return cache[key]
        yy = P[y][mask]
        ok = np.isfinite(yy)
        idx = np.nonzero(mask)[0][ok]
        if len(idx) < 50:
            cache[key] = (None, None, 0)
            return cache[key]
        e, tr = P["e"][idx], P["treat"][idx]
        if xs_fn is None:
            X, names = _es_dummies(e, tr)
        else:
            X, names = xs_fn(idx)
        keepc = X.std(axis=0) > 0
        b = np.full(X.shape[1], np.nan)
        if keepc.any():
            b[keepc] = twfe(P[y][idx], X[:, keepc], P["unit"][idx], P["cell"][idx])
        cache[key] = (b, names, len(idx))
        return cache[key]

    def comb(fit, wts):
        b, names, n = fit
        if b is None:
            return np.nan, 0
        return float(sum(b[names.index(k)] * w for k, w in wts.items())), n

    m13 = {f"d{e}": 1 / 3 for e in (1, 2, 3)}
    for r, rb in ((0, "B"), (1, "W")):
        mk = P["race"] == r
        for y in ("hh", "hlab", "fs", "bw_present"):
            v, n = comb(es_fit(mk, y, (y, r)), m13)
            put(f"psid_es_{y}_13_{rb}", v, n)
        v, n = comb(es_fit(mk, "hlab", ("hlab", r)), {"d6": 1.0})
        put(f"psid_es_hlab_6_{rb}", v, n)
    for kid, mk in (("05", P["young0"] == 1), ("617", P["young0"] == 2)):
        for y in ("w_hrs", "w_emp"):
            v, n = comb(es_fit(mk, y, (y, kid)), m13)
            put(f"psid_es_{y}_13_y{kid}", v, n)

    # 38: gross response and joint-loss offset (interaction model), on rows with J and w_hrs
    def inter_x(idx):
        cols, names = [], []
        e, tr, J = P["e"][idx], P["treat"][idx], P["J"][idx]
        for k in ES_E:
            ind = (e == k).astype(float)
            cols += [ind * tr, ind * J, ind * tr * J]
            names += [f"d{k}", f"j{k}", f"t{k}"]
        return np.column_stack(cols), names

    hasJ = np.isfinite(P["J"])
    for kid, mk in (("all", hasJ), ("05", hasJ & (P["young0"] == 1))):
        fit = es_fit(mk, "w_hrs", ("inter", kid), inter_x)
        b, names, n = fit
        if b is None:
            put(f"psid_gross_{kid}", np.nan, 0)
            if kid == "all":
                put("psid_offset_all", np.nan, 0)
            continue
        ix = {nm: i for i, nm in enumerate(names)}
        put(f"psid_gross_{kid}", np.mean([b[ix[f"d{e}"]] for e in (1, 2, 3)]), n)
        if kid == "all":
            rows = np.nonzero(mk & np.isfinite(P["w_hrs"]))[0]
            uu, first = np.unique(P["unit"][rows], return_index=True)
            ut, uJ = P["treat"][rows][first], P["J"][rows][first]
            P1 = (ut * uJ).sum() / max(ut.sum(), 1)
            P0 = ((1 - ut) * uJ).sum() / max((1 - ut).sum(), 1)
            jm = np.mean([b[ix[f"j{e}"]] for e in (1, 2, 3)])
            tm = np.mean([b[ix[f"t{e}"]] for e in (1, 2, 3)])
            put("psid_offset_all", (P1 - P0) * jm + P1 * tm, n)

    # 25: cost of her own displacement (bins model, her labor income)
    BINS = {"pre3": [-3], "pre1": [-1], "e0": [0], "post13": [1, 2, 3], "post46": [4, 5, 6]}

    def bin_x(idx):
        cols, names = [], []
        e, tr, J = P["e"][idx], P["treat"][idx], P["J"][idx]
        for bn, es_ in BINS.items():
            ind = np.isin(e, es_).astype(float)
            cols += [ind * tr, ind * J, ind * tr * J]
            names += [f"d_{bn}", f"m_J_{bn}", f"dm_J_{bn}"]
        return np.column_stack(cols), names

    v, n = comb(es_fit(hasJ, "w_lab", ("bins",), bin_x), {"m_J_post13": 1.0})
    put("psid_wife_own_disp_lab13", v, n)

    # 38: permanent vs contemporaneous component (two windows), events 1987-2021, wife employed at baseline
    ws = (U["ev"] >= 1987) & (U["ev"] <= 2021) & (U["wemp0"] == 1) & np.isfinite(U["main_W"]) & \
        np.isfinite(U["main_PL"])
    if ws.sum() > 50:
        ev_ = np.concatenate([U["ev"][ws], U["ev"][ws]])
        win = np.concatenate([np.zeros(ws.sum()), np.ones(ws.sum())])
        Yd = np.concatenate([U["main_PL"][ws], U["main_W"][ws]])
        tr2 = np.concatenate([U["treat"][ws], U["treat"][ws]])
        ps2 = np.concatenate([U["pseudo"][ws], U["pseudo"][ws]])
        ever = ((tr2 == 1) | (ps2 == 1)).astype(float)
        tw = tr2 * win
        gW, uW = pd.factorize(ev_ * 10 + win)
        b = fe_ols(Yd, np.column_stack([ever, tw]), gW, len(uW), np.ones(len(Yd)))
        put("psid_perm", b[0], len(Yd))
        put("psid_contemp", b[1], len(Yd))
    else:
        put("psid_perm", np.nan, 0)
        put("psid_contemp", np.nan, 0)

    # 25: couple-years
    CY = PN.couple_years(R)
    h, w_ = CY["h"], CY["w"]
    for k, mk in (("all", np.ones(len(h), bool)), ("same", CY["same"] == 1), ("diff", CY["same"] == 0)):
        a1, a0 = mk & (h == 1), mk & (h == 0)
        put(f"psid_cy_diff_{k}", (w_[a1].mean() - w_[a0].mean()) if a1.any() and a0.any() else np.nan, mk.sum())
    for r, rb in ((0, "B"), (1, "W")):
        mk = (CY["race"] == r) & (h == 0)
        put(f"psid_cy_wbase_{rb}", w_[mk].mean() if mk.any() else np.nan, mk.sum())

    # 19: husband's annual displacement rate; T28 over-dispersion
    HR = PN.husband_risk_rows(R)
    for r, rb in ((0, "B"), (1, "W")):
        mk = HR["race"] == r
        put(f"psid_h_disp_rate_{rb}", HR["y"][mk].mean() if mk.any() else np.nan, mk.sum())
    ui, inv = np.unique(HR["i"], return_inverse=True)
    Nh = np.bincount(inv)
    Kh = np.bincount(inv, weights=HR["y"])
    rh = R.race[ui]
    for r, rb in ((0, "B"), (1, "W")):
        mk = (Nh >= 10) & (rh == r)
        put(f"psid_disp2plus_{rb}", (Kh[mk] >= 2).mean() if mk.any() else np.nan, mk.sum())

    # couple-year levels: employment by youngest child, part-time shares, SNAP receipt
    L = PN.psid_rows(R)
    lv = (L["Y"] >= 1984) & (L["Y"] <= 2021) & (L["age"] >= 25) & (L["age"] <= 59)
    for k, kv in (("none", 0), ("05", 1), ("617", 2)):
        mk = lv & (L["k"] == kv)
        put(f"psid_wemp_{k}", (L["wh"][mk] > 0).mean() if mk.any() else np.nan, mk.sum())
    for k, hv in (("w", L["wh"]), ("h", L["hh"])):
        mk = lv & (hv > 0)
        put(f"psid_pt_{k}", (hv[mk] < 1560).mean() if mk.any() else np.nan, mk.sum())
    for r, rb in ((0, "B"), (1, "W")):
        mk = lv & (L["race"] == r)
        put(f"psid_snap_{rb}", L["fs"][mk].mean() if mk.any() else np.nan, mk.sum())
        mh = mk & np.isfinite(L["hh"])                       # husband present in the income year (same rows as SNAP)
        put(f"psid_hemp_{rb}", (L["hh"][mh] > 0).mean() if mh.any() else np.nan, mh.sum())
    # separation rate
    SR = PN.sep_rows(R)
    for r, rb in ((0, "B"), (1, "W")):
        mk = SR["race"] == r
        put(f"psid_sep_rate_{rb}", SR["sep"][mk].sum() / SR["L"][mk].sum() if mk.any() else np.nan, mk.sum())
    # wage growth
    WG = PN.wage_growth_rows(R)
    for sp_ in ("w", "h"):
        g = WG[sp_]
        for lo, hi in ((25, 34), (35, 44), (45, 54)):
            mk = (g["age"] >= lo) & (g["age"] <= hi)
            put(f"psid_wg_{sp_}_{lo}", g["dl"][mk].mean() if mk.any() else np.nan, mk.sum())
    # re-entry wage
    RE = PN.reentry_rows(R)
    if RE["re"].sum() >= 5:
        agd = np.column_stack([((RE["age"] >= 35) & (RE["age"] <= 44)).astype(float),
                               ((RE["age"] >= 45) & (RE["age"] <= 59)).astype(float)])
        gr, ur = pd.factorize(RE["Y"])
        b = fe_ols(RE["lw"], np.column_stack([RE["re"], agd]), gr, len(ur), np.ones(len(RE["lw"])))
        put("psid_reentry_wage", b[0], len(RE["lw"]))
    else:
        put("psid_reentry_wage", np.nan, 0)
    # liquid wealth
    WL = PN.wealth_rows(R)
    for lo, hi in ((25, 34), (35, 44), (45, 59)):
        mk = (WL["age"] >= lo) & (WL["age"] <= hi)
        put(f"psid_liq_le0_{lo}", (WL["liq"][mk] <= 0).mean() if mk.any() else np.nan, mk.sum())
        put(f"psid_liq_hi_{lo}", (WL["liq"][mk] > WL["earn"][mk]).mean() if mk.any() else np.nan, mk.sum())
    # consumption (47): interaction model, log total consumption, waves 1999-2021
    Qc = PN.cons_rows(R, U)

    def cons_fit(mask):
        idx = np.nonzero(mask)[0]
        if len(idx) < 50:
            return None, None
        k, tr, J = Qc["k"][idx], Qc["treat"][idx], Qc["J"][idx]
        cols, names = [], []
        for kk in KS:
            ind = (k == kk).astype(float)
            cols += [ind * tr, ind * J, ind * tr * J]
            names += [f"d{kk}", f"j{kk}", f"t{kk}"]
        X = np.column_stack(cols)
        keepc = X.std(axis=0) > 0
        b = np.full(X.shape[1], np.nan)
        b[keepc] = twfe(Qc["lc"][idx], X[:, keepc], Qc["unit"][idx], Qc["cell"][idx])
        return b, names

    for race, nm in ((None, "all"), (0, "black"), (1, "white")):
        mk = np.ones(len(Qc["lc"]), bool) if race is None else (Qc["race"] == race)
        b, names = cons_fit(mk)
        n = int(mk.sum())
        if b is None:
            put(f"psid_cons_single_{nm}", np.nan, 0)
            if race is None:
                put("psid_cons_wife_alone", np.nan, 0)
                put("psid_cons_joint_minus_single", np.nan, 0)
            continue
        ix = {s: i for i, s in enumerate(names)}
        c3 = lambda pf: float(np.mean([sum(b[ix[f"{p}{k}"]] for p in pf) for k in (1, 2, 3)]))   # noqa: E731
        put(f"psid_cons_single_{nm}", c3(("d",)), n)
        if race is None:
            put("psid_cons_wife_alone", c3(("j",)), n)
            put("psid_cons_joint_minus_single", c3(("j", "t")), n)
    t_psid = time.perf_counter()
    ext_moments = tuple(ext_moments or ())
    if "new_job" in ext_moments:
        TE = PN.sipp_tenure_exits(R)
        ten, y = TE["ten"], TE["y"]
        for k, mk in (("0_5", ten < 6), ("6_11", (ten >= 6) & (ten < 12)), ("12p", ten >= 12)):
            put(f"sipp_wexit_ten_{k}", y[mk].mean() if mk.any() else np.nan, mk.sum())
        put("sipp_wexit_return12", TE["ret"][11], TE["n_exits"])
        v, n = PN.psid_repeat_exits(R)
        put("psid_wexit_repeat2", v, n)
    if "her_sep" in ext_moments:
        HP = PN.her_stack_rows(R)
        X, names = _es_dummies(HP["e"], HP["treat"])
        keepc = X.std(axis=0) > 0
        b = np.full(X.shape[1], np.nan)
        if keepc.any() and len(HP["e"]) >= 50:
            b[keepc] = twfe(HP["bh_present"], X[:, keepc], HP["unit"], HP["cell"])
        nt = int(np.unique(HP["unit"][HP["treat"] == 1]).size)
        put("psid_es_bh_present_13", np.mean([b[names.index(f"d{e}")] for e in (1, 2, 3)]), nt)
        put("psid_es_bh_present_46", np.mean([b[names.index(f"d{e}")] for e in (4, 5, 6)]), nt)
    if timing is not None:
        timing["moments_cps"] = t_cps - t0
        timing["moments_sipp"] = t_sipp - t_cps
        timing["moments_psid"] = t_psid - t_sipp
    return (out, N) if return_n else out


def vector(mdict, targets):
    return np.array([mdict.get(k, np.nan) for k in targets["id"]], float)
