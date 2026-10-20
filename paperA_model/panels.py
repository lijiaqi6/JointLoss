"""Paper A model: measurement layer. Simulated monthly couple histories (simulate.SimResult) -> data-shaped panels.

Every target of output/paperA_targets.csv is computed (moments.py) on the panel of its source, built here with the
data scripts' sample rules (IGE/60.PaperATargets.py and the builders it calls: IGE/30, 37 (CPS), IGE/40 (SIPP),
IGE/19, 23, 25, 38, 47 (PSID)), restricted to the target's calendar window. Model -> data mapping (one place):

TIMING. A displacement at the end of model month t is a job loss in month t in the data's sense (employed in t, not
  employed in t+1). Calendar month index m = 0 is January 1984 (simulate.M0).
EMPLOYMENT. A spouse is employed in month t when he / she works (positive hours). A wife who holds a job and chooses
  zero hours is not employed that month (she quits).
CPS (couple-months 1994-2023, IGE/30 / 37 / 60). Married couples observed in t and t+1 (separation ends the couple).
  'Job loser' (non-temporary; the model has no temporary layoffs) in t+1 = displaced at the end of t and looking for
  work in t+1 (simulate: a non-employed wife looks when she would accept a job with probability > 1/2; husbands always
  look). A displaced wife who does not look is out of the labor force in the CPS: she is not a job loser and counts as
  an 'exit without a job-loss reason'. Rotation: the 4-8-4 pattern taken over every possible entry month (mode 'all'),
  which weights every couple-month transition equally, i.e. the expectation of the CPS sampling; mode 'single' draws
  one 4-8-4 window per couple-copy (literal, noisy; diagnostics only). State x month fixed effects become calendar-month
  fixed effects (the model has no states); survey weights are 1.
SIPP (2003-2016, IGE/40 / 60). Three panel windows (2004: Oct 2003-Dec 2007; 2008: May 2008-Nov 2013; 2014: Jan 2013-
  Dec 2016); every couple-copy is observed in each window (the 2013 overlap is counted twice, as in the data). SIPP's
  separation month tau (the job ends during tau) = the first model month without work after a displacement at the end
  of tau - 1; base month b = tau - 1. Re-employment earnings: d = full months without a job = model non-employed
  months - 1 (the SIPP's separation and start months are partial months), pre = earnings in b (last full month),
  post = earnings in the first month worked (a full month in the model).
PSID (income years 1984-2021; interviews in April of the wave year; waves annual to 1997, biennial from 1999, so
  observed income years are 1984-1996, 1998, 2000, ..., 2022). Row (couple-copy, income year Y): annual hours and
  labor income = sums over the months of Y, food stamps = any receipt in Y; status, marriage, youngest child and age
  at the interview of wave Y + 1; wife's age = interview age - 1. A married row requires the couple married through
  all of Y and at the interview. After a separation the husband leaves the model: his rows keep only 'still with
  wife' (= 0); his hours, earnings and food stamps are missing (approximation; the PSID follows him). Displacements
  are dated to the calendar year of the model month. Wife's displacement events need coverage (the first wave
  reporting job ends of year y, with her still the wife: IGE/25 cover_wave). Same sector (16 sectors) = workplace
  match s >= 1 (PSID shares 16.8% vs CPS s >= 1 17.7%). Husband's age (wage growth, 20-60 rule) = wife's age + 2
  (approximation; the model has no husband age). Stacked designs (IGE/19 stacks, IGE/25 units): control units are a
  CRN subsample (rate ctrl_rate, slot 51) of the clean controls, which leaves the estimators unbiased and keeps the
  stacked panels near the data's size. Consumption: the interview month's flow x 12, plus BPS's measurement error
  N(0, 0.0332) in logs (CRN, slot 50), interview waves 1999-2021 only.
Liquid wealth: assets at the interview (April of the wealth wave), earnings of the calendar year before (dropped when
  that year is not observed, i.e. in the couple's entry year).
"""
from __future__ import annotations

import numpy as np
from numba import njit
from scipy.special import ndtri

from simulate import FIELDS_F, FIELDS_I, M0, _u01_vec, u01

HOURS = np.array([0.0, 87.0, 173.0])
NYEAR = 40                                         # calendar years 1984-2023 in the record arrays
OBS_YEARS = np.array(list(range(1984, 1997)) + list(range(1998, 2023, 2)))
WAVES = set(range(1968, 1998)) | set(range(1999, 2024, 2))
SIPP_WINDOWS = ((2003, 10, 2007, 12), (2008, 5, 2013, 11), (2013, 1, 2016, 12))
WEALTH_WAVES = (1984, 1989, 1994) + tuple(range(1999, 2020, 2))
CONS_WAVES = tuple(range(1999, 2022, 2))
KBIN = {-4: -2, -3: -2, -2: -1, -1: -1, 0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3}


def mi(year, month=1):
    """Calendar month index of (year, month 1-12)."""
    return 12 * (year - M0) + month - 1


def cover_wave(y):
    """First interview that carries reports of job ends in calendar year y (IGE/25), None outside 1983-2022."""
    if y < 1983 or y > 2022:
        return None
    return y + 1 if (y + 1) in WAVES else y + 2


def crn_u(seed, uid, t, slot):
    uid = np.asarray(uid, np.int64)
    return _u01_vec(np.array([seed], np.int64), uid, np.asarray(t, np.int64) + np.zeros(len(uid), np.int64),
                    np.full(len(uid), slot, np.int64))


def shift(A, k, fill=False):
    """B[:, m] = A[:, m + k] (fill outside the array)."""
    B = np.full_like(A, fill)
    if k > 0:
        B[:, :-k] = A[:, k:]
    elif k < 0:
        B[:, -k:] = A[:, :k]
    else:
        B[:] = A
    return B


@njit(cache=True)
def _next_true(A):
    """N[i, m] = smallest m' > m with A[i, m'] (or n_months if none)."""
    n, nm = A.shape
    N = np.empty((n, nm), np.int32)
    for i in range(n):
        nxt = nm
        for m in range(nm - 1, -1, -1):
            N[i, m] = nxt
            if A[i, m]:
                nxt = m
    return N


@njit(cache=True)
def _post_sep_disp(st, seed, uid, haz):
    """Husband's displacements after a separation (he leaves the model): Bernoulli(haz[i]) each month in which the
    separated wife is still in the sample (st == 0), CRN slot 23 (his own-hazard draw)."""
    n, nm = st.shape
    out = np.zeros((n, nm), np.bool_)
    for i in range(n):
        for m in range(nm):
            if st[i, m] == 0 and u01(seed, uid[i], m, 23) < haz[i]:
                out[i, m] = True
    return out


class Records:
    """Monthly arrays (couple-copy x calendar month) derived once from a SimResult."""

    def __init__(self, res, ctrl_rate=0.15, theta=None, merge_s12=True):
        I, F = res.I, res.F
        gi = lambda nm: I[FIELDS_I.index(nm)]                          # noqa: E731
        gf = lambda nm: F[FIELDS_F.index(nm)]                          # noqa: E731
        ent = res.info["entry"]
        self.n, self.nm = gi("status").shape
        self.uid = np.asarray(res.info["uid"], np.int64)
        self.seed = int(res.info.get("seed", 20261018))
        self.race = ent["race"].to_numpy().astype(int)                # 0 Black, 1 White
        self.s = ent["s"].to_numpy().astype(int)                      # entry match (0, 1, 2)
        self.year0 = ent["year0"].to_numpy().astype(int)
        self.m_off = np.asarray(res.info["m_off"], np.int64)
        self.ctrl_rate = ctrl_rate
        st = gi("status")
        self.st = st
        self.MAR = st == 1
        lw, lh = gi("lw"), gi("lh")
        hrs_w, hrs_h = gi("hrs_w"), gi("hrs_h")
        self.W = self.MAR & (lw == 0) & (hrs_w > 0)                   # married wife works
        self.EN = int(res.info.get("EN", -1))                         # new-job state (extension), -1 = none
        if self.EN >= 0:
            self.W = self.MAR & ((lw == 0) | (lw == self.EN)) & (hrs_w > 0)
        self.HW = self.MAR & (lh == 0)                                # husband works (always positive hours)
        self.DW = (gi("disp_w") == 1) & self.MAR
        self._disp_w = gi("disp_w")                                   # raw records (extension moments only)
        self.DH = (gi("disp_h") == 1) & self.MAR
        self.LK = gi("look") == 1
        self.JLW = shift(self.DW, -1) & self.LK & self.MAR            # wife job loser in m (displaced end of m-1, looks)
        self.hours_w = np.where(self.W, HOURS[np.clip(hrs_w, 0, 2)], 0.0).astype(np.float32)
        self.hours_h = np.where(self.HW, HOURS[np.clip(hrs_h, 0, 2)], 0.0).astype(np.float32)
        self.yw = np.where(self.W, gf("yw"), 0.0).astype(np.float32)  # thousand 2000 $ a month
        self.yh = np.where(self.HW, gf("yh"), 0.0).astype(np.float32)
        self.snap = gf("snap")
        self.c = gf("c")
        self.a = gf("a")
        # husband's displacements after a separation (unobserved in the model, observed in the PSID): imputed from
        # his monthly hazard pi_c(s) + (1 - pi_c(s)) m_tau delta_h(r) as if employed; used only to date his first
        # displacement (treated / clean-control status of the stacked designs), never as an outcome
        self.DHsep = np.zeros_like(self.DH)
        if theta is not None:
            # the same marginal hazard under the decorrelation counterfactuals (res.info['decorr'])
            tau_h = np.asarray(res.info.get("tau_h", res.info["tau"]))
            m_ = np.where(tau_h == 1, theta["m_H"], 1.0)
            if res.info.get("decorr") == "mean":
                m_ = np.full(len(tau_h), 1.0 + theta["p_H"] * (theta["m_H"] - 1.0))
            dh = np.where(self.race == 0, theta["delta_h_B"], theta["delta_h_W"])
            sx = np.minimum(self.s, 1) if merge_s12 else self.s
            pic = np.array([theta["pi_c0"], theta["pi_c1"], theta["pi_c1" if merge_s12 else "pi_c2"]])[sx]
            haz = np.minimum(pic + (1 - pic) * m_ * dh, 0.999)
            self.DHsep = _post_sep_disp(st, self.seed, self.uid, haz)
        self._annual()

    # ---------------- PSID annual rows ----------------
    def _annual(self):
        n = self.n
        ny = self.nm // 12
        R = lambda A: A[:, :ny * 12].reshape(n, ny, 12)               # noqa: E731
        self.full_mar = R(self.MAR).all(axis=2)
        self.hh_ann = R(self.hours_h).sum(axis=2)
        self.wh_ann = R(self.hours_w).sum(axis=2)
        self.hlab_ann = R(self.yh).sum(axis=2) * 1000.0
        self.wlab_ann = R(self.yw).sum(axis=2) * 1000.0
        self.fs_ann = (R(self.snap > 0) & R(self.MAR)).any(axis=2)
        self.dh_year = R(self.DH).any(axis=2)
        self.dw_year = R(self.DW).any(axis=2)
        self.dh_year_all = self.dh_year | R(self.DHsep).any(axis=2)
        # interview of wave Y + 1 (April) for income year Y
        mint = np.arange(ny) * 12 + 15
        okm = mint < self.nm
        self.mar_int = np.zeros((n, ny), bool)
        self.obs_int = np.zeros((n, ny), bool)
        self.k_int = np.full((n, ny), -1, np.int8)
        self.mar_int[:, okm] = self.MAR[:, mint[okm]]
        self.obs_int[:, okm] = self.st[:, mint[okm]] >= 0
        years = np.arange(M0, M0 + ny)
        self.years = years
        is_obs = np.isin(years, OBS_YEARS)
        entered = years[None, :] >= self.year0[:, None]
        self.man_obs = self.obs_int & entered & is_obs[None, :]
        self.row_mar = self.full_mar & self.mar_int & entered & is_obs[None, :]
        # wife's age in the income year: interview age - 1
        age_int = 25 + (mint[None, :] - self.m_off[:, None]) // 12
        self.w_agey = (age_int - 1).astype(np.int16)

    def set_k(self, kmat):
        ny = self.nm // 12
        mint = np.arange(ny) * 12 + 15
        okm = mint < self.nm
        self.k_int[:, okm] = kmat[:, mint[okm]]
        self.k_month = kmat

    def year_index(self, Y):
        return np.asarray(Y) - M0


def records(res, ctrl_rate=0.15, theta=None, merge_s12=True):
    r = Records(res, ctrl_rate, theta, merge_s12)
    r.set_k(res.I[FIELDS_I.index("k")])
    return r


# ======================================================================================================================
# CPS
# ======================================================================================================================
def cps_samples(R, mode="all", y0=1994, y1=2023, classif=None):
    """Samples of IGE/60's CPS moments (IGE/37 event samples, IGE/30 entry / exit). Each sample: dict of arrays
    y, H (0/1 or None), g (calendar month code of the base month), race, s. mode 'all': every rotation offset.
    classif: 3 x 3 CPS classification-error matrix (true E, U, N -> recorded); entry / exit then carry row weights wt
    and expected recorded outcomes y (see below)."""
    lo, hi = mi(y0, 1), mi(y1, 12)
    nm = R.nm
    obs = np.zeros((R.n, nm), bool)
    obs[:, lo:hi + 1] = True
    if mode == "single":
        # one 4-8-4 window per couple-copy: months-in-sample 1-4 and 13-16 from a CRN start month
        u = crn_u(R.seed, R.uid, 0, 52)
        start = lo + (u * (hi - lo - 15)).astype(int)
        mm = np.arange(nm)[None, :] - start[:, None]
        obs &= ((mm >= 0) & (mm < 4)) | ((mm >= 12) & (mm < 16))
    MAR, W, HW, DH, JLW = R.MAR & obs, R.W, R.HW, R.DH, R.JLW
    S = lambda A, k: shift(A, k)                                     # noqa: E731
    marall = lambda ks: np.logical_and.reduce([S(MAR, k) for k in ks])  # noqa: E731
    base_h = HW & (DH | S(HW, 1))                                    # husband employed in b; H defined in b + 1
    out = {}

    def pack(mask, y, H):
        ii, mm = np.nonzero(mask)
        return dict(y=y[ii, mm].astype(float), H=None if H is None else H[ii, mm].astype(float), g=mm,
                    race=R.race[ii], s=R.s[ii], i=ii)

    # tau (T1, T2, T6): wife works in b, his loss at the end of b vs he works in b + 1
    m_tau = marall((0, 1)) & base_h & W
    out["tau"] = pack(m_tau, S(JLW, 1), DH)
    # leads and lags (37's event samples; tau = b + 1)
    spec = {
        -3: dict(mar=(-3, -2, -1, 0, 1), hw=(-2, -1, 0), w=-3, y=-2, extra=lambda: S(W, -2) | S(JLW, -2)),
        -2: dict(mar=(-3, -2, -1, 0, 1), hw=(-2, -1, 0), w=-2, y=-1, extra=None),
        -1: dict(mar=(-2, -1, 0, 1), hw=(-1, 0), w=-1, y=0, extra=None),
        1: dict(mar=(0, 1, 2), hw=(0,), w=1, y=2, extra=None, ctrl=(2,)),
        2: dict(mar=(0, 1, 2, 3), hw=(0,), w=2, y=3, extra=None, ctrl=(2, 3)),
        3: dict(mar=(0, 1, 2, 3, 4), hw=(0,), w=3, y=4, extra=None, ctrl=(1, 2, 3, 4)),
    }
    for k, sp in spec.items():
        mk = marall(sp["mar"]) & base_h & S(W, sp["w"])
        for h in sp["hw"]:
            mk &= S(HW, h)
        if sp.get("extra") is not None:
            mk &= sp["extra"]()
        if sp.get("ctrl"):
            c_ok = np.logical_and.reduce([S(HW, h) for h in sp["ctrl"]])
            mk &= DH | c_ok
        out[f"lag{k:+d}"] = pack(mk, S(JLW, sp["y"]), DH)
    # persistent entry / exit (IGE/60 cps_entry_p_*, cps_wife_exit_p, 2026-10-19): status before the transition held in
    # t-1 and t, status after it holds in t+1 and t+2 (married t-1 .. t+2), husband employed t and t+1
    base_p = marall((-1, 0, 1, 2)) & HW & S(HW, 1)
    out["entry_p"] = pack(base_p & ~S(W, -1) & ~W, S(W, 1) & S(W, 2), None)
    out["exit_p"] = pack(base_p & S(W, -1) & W, ~S(W, 1) & ~S(JLW, 1) & ~S(W, 2), None)
    # entry of non-employed wives (husband employed t, t + 1); exits without a job-loss reason
    if classif is None:
        m_ent = marall((0, 1)) & ~W & HW & S(HW, 1)
        out["entry"] = pack(m_ent, S(W, 1), None)
        m_ex = marall((0, 1)) & W & HW & S(HW, 1)
        out["exit"] = pack(m_ex, ~S(W, 1) & ~S(JLW, 1), None)
        return out
    # CPS classification error (Poterba and Summers 1986; Abowd and Zellner 1985): the CPS records the wife's true
    # status a in {E, U, N} as b with probability Q[a, b], independently across months. Over all couple-months with
    # the husband employed in t and t + 1, the measured entry / exit rates are ratios of expected recorded flows
    # (Poterba-Summers eq. 9, F = Q'F*Q, evaluated row by row, no extra draws): exit weight Q[a_t, E], outcome
    # Q[b, N] + Q[b, U] x (1 - true job loser in t + 1) (a recorded U that is not a true job loss carries a non-job-loss
    # reason; a true job loser recorded N counts as an exit); entry weight Q[a_t, U] + Q[a_t, N], outcome Q[b, E].
    # Q = identity reproduces the samples above exactly.
    Q = np.asarray(classif, float)
    LK = R.LK
    st = np.where(W, 0, np.where(LK, 1, 2)).astype(np.int8)          # true status: 0 E, 1 U (looking), 2 N
    st1 = S(st, 1)
    m_all = marall((0, 1)) & HW & S(HW, 1)
    ii, mm = np.nonzero(m_all)
    a0 = st[ii, mm]
    b1 = st1[ii, mm]
    jl1 = S(JLW, 1)[ii, mm]
    w_ex = Q[a0, 0]
    y_ex = Q[b1, 2] + Q[b1, 1] * (~jl1)
    w_en = Q[a0, 1] + Q[a0, 2]
    y_en = Q[b1, 0]
    base = dict(g=mm, race=R.race[ii], s=R.s[ii], i=ii, H=None)
    out["entry"] = dict(base, y=y_en, wt=w_en)
    out["exit"] = dict(base, y=y_ex, wt=w_ex)
    return out


# ======================================================================================================================
# SIPP
# ======================================================================================================================
def sipp_samples(R):
    """Samples of IGE/60's SIPP moments in the three panel windows."""
    MAR, W, HW, DH, DW = R.MAR, R.W, R.HW, R.DH, R.DW
    nm = R.nm
    S = lambda A, k: shift(A, k)                                     # noqa: E731
    # couple observed (married) from b through b + k
    nxt_nonmar = _next_true(~MAR)
    aw = {f"wife_s{s}": [] for s in (0, 1, 6)}
    aw.update({f"his_s{s}": [] for s in (3, 6, 12)})
    ree = {"h": [], "w": []}
    nwork_h = _next_true(HW)
    nwork_w = _next_true(W)
    for wi, (ya, ma, yb, mb) in enumerate(SIPP_WINDOWS):
        lo, hi = mi(ya, ma), mi(yb, mb)
        inwin = np.zeros((R.n, nm), bool)
        inwin[:, lo:hi + 1] = True
        base = inwin & MAR & HW & ~W & (DH | S(HW, 1)) & S(MAR, 1)
        for s_, key, outc in [(s, f"wife_s{s}", W) for s in (0, 1, 6)] + [(s, f"his_s{s}", HW) for s in (3, 6, 12)]:
            k = 1 + s_
            ok = base & (np.arange(nm)[None, :] + k <= hi) & (nxt_nonmar > (np.arange(nm)[None, :] + k))
            ii, mm = np.nonzero(ok)
            aw[key].append(dict(y=S(outc, k)[ii, mm].astype(float), H=DH[ii, mm].astype(float),
                                g=wi * 100000 + mm, i=ii))
        # re-employment earnings by months without a job (involuntary separation = displacement)
        for sp, D, NW, earn in (("h", DH, nwork_h, R.yh), ("w", DW, nwork_w, R.yw)):
            ok = inwin & D & MAR
            ii, mm = np.nonzero(ok)
            r = NW[ii, mm]                                           # first month worked again
            nmon = r - mm - 1                                        # model months without work
            d = nmon - 1                                             # SIPP full months without a job
            keep = (r <= hi) & (nxt_nonmar[ii, mm] > r) & (d >= 1) & (d <= 24)
            ii, mm, r, d = ii[keep], mm[keep], r[keep], d[keep]
            pre = earn[ii, mm].astype(float)
            post = earn[ii, r].astype(float)
            with np.errstate(divide="ignore", invalid="ignore"):
                dl = np.log(post) - np.log(pre)
            ok2 = np.isfinite(dl) & (np.abs(dl) <= 3)
            ree[sp].append(dict(dl=dl[ok2], d=d[ok2], i=ii[ok2]))
    cat = lambda L: {k: np.concatenate([x[k] for x in L]) for k in L[0]}   # noqa: E731
    return {k: cat(v) for k, v in aw.items()}, {k: cat(v) for k, v in ree.items()}


# ======================================================================================================================
# PSID
# ======================================================================================================================
def _yidx(Y):
    return np.asarray(Y, int) - M0


def psid_rows(R):
    """Married couple-year rows (income years in OBS_YEARS) as flat arrays."""
    ii, yy = np.nonzero(R.row_mar)
    Y = R.years[yy]
    return dict(i=ii, Y=Y, yi=yy, race=R.race[ii], s=R.s[ii], hh=R.hh_ann[ii, yy], wh=R.wh_ann[ii, yy],
                hlab=R.hlab_ann[ii, yy], wlab=R.wlab_ann[ii, yy], fs=R.fs_ann[ii, yy].astype(float),
                k=R.k_int[ii, yy], age=R.w_agey[ii, yy])


def _prev_obs(Y):
    """Previous observed income year (PSID waves): Y - 1 to 1996, 1996 for 1998, Y - 2 after."""
    Y = np.asarray(Y)
    return np.where(Y <= 1996, Y - 1, np.where(Y == 1998, 1996, Y - 2))


def _next_obs(Y):
    Y = np.asarray(Y)
    return np.where(Y <= 1995, Y + 1, np.where(Y == 1996, 1998, Y + 2))


def coverage(R, ii, y):
    """Wife's job-end reports for calendar year y covered (IGE/25 cover_wave): the first wave reporting year y exists
    and the couple is still married at its interview; y not before the couple's entry."""
    out = np.zeros(len(ii), bool)
    y = np.asarray(y)
    for yv in np.unique(y):
        cw = cover_wave(int(yv))
        sel = y == yv
        if cw is None or mi(cw, 4) >= R.nm:
            continue
        out[sel] = R.MAR[ii[sel], mi(cw, 4)] & (yv >= R.year0[ii[sel]])
    return out


def wife_disp(R, ii, y):
    """Her displacement in calendar year y (covered), NaN if not covered."""
    y = np.asarray(y)
    yi = np.clip(_yidx(y), 0, R.dw_year.shape[1] - 1)
    val = R.dw_year[ii, yi].astype(float)
    val[(y < M0) | (y >= M0 + R.dw_year.shape[1])] = np.nan
    val[~coverage(R, ii, y)] = np.nan
    return val


def units(R, ev_lo=1968, ev_hi=2022, kids=True):
    """Father x stack units of IGE/19 stacks / IGE/25 build_units: for every event year ev, the baseline row is the
    man's row of ev - 1 if that income year is observed, else ev - 2; it must be a married row with a child under 18
    (kids) and his positive hours. treat = first displacement in ev; pseudo = first in ev + 4 .. ev + 6; control =
    none to ev + 6 (CRN subsample at ctrl_rate). Returns flat arrays per unit."""
    ny = R.dh_year.shape[1]
    years = R.years
    has = R.dh_year_all & (years[None, :] >= R.year0[:, None])
    fm = np.where(has.any(axis=1), years[np.argmax(has, axis=1)], 9999)
    out = []
    for ev in range(max(ev_lo, M0 + 1), min(ev_hi, M0 + ny) + 1):
        b1, b2 = ev - 1, ev - 2
        c1 = (b1 in OBS_YEARS) and (b1 - M0 < ny)
        y1i = b1 - M0
        y2i = b2 - M0
        if c1:
            obs1 = R.man_obs[:, y1i]
        else:
            obs1 = np.zeros(R.n, bool)
        obs2 = R.man_obs[:, y2i] if (b2 in OBS_YEARS and y2i >= 0) else np.zeros(R.n, bool)
        by = np.where(obs1, b1, np.where(obs2, b2, -1))
        ok = by > 0
        byi = np.clip(by - M0, 0, ny - 1)
        ii = np.nonzero(ok)[0]
        bi = byi[ii]
        elig = R.row_mar[ii, bi] & (R.hh_ann[ii, bi] > 0)
        if kids:
            elig &= R.k_int[ii, bi] > 0
        ii, bi = ii[elig], bi[elig]
        tr = fm[ii] == ev
        ps = (fm[ii] >= ev + 4) & (fm[ii] <= ev + 6)
        ct = fm[ii] > ev + 6
        keep_ct = crn_u(R.seed, R.uid[ii] * 64 + (ev - 1960), 0, 51) < R.ctrl_rate
        sel = tr | ps | (ct & keep_ct)
        ii, bi, tr, ps = ii[sel], bi[sel], tr[sel], ps[sel]
        if len(ii) == 0:
            continue
        evv = np.full(len(ii), ev)
        mW = np.column_stack([wife_disp(R, ii, evv + k) for k in (-1, 0, 1)])
        mPL = np.column_stack([wife_disp(R, ii, evv + k) for k in (-4, -3, -2)])
        main_W = np.where(np.isnan(mW).any(axis=1), np.nan, np.nanmax(np.nan_to_num(mW, nan=0), axis=1))
        main_PL = np.where(np.isnan(mPL).any(axis=1), np.nan, np.nanmax(np.nan_to_num(mPL, nan=0), axis=1))
        wh0 = R.wh_ann[ii, bi]
        wemp0 = (wh0 > 0).astype(float)
        J = np.where(wemp0 == 0, 0.0, main_W)
        out.append(dict(i=ii, ev=evv, treat=tr.astype(float), pseudo=ps.astype(float), young0=R.k_int[ii, bi],
                        wh0=wh0, wemp0=wemp0, main_W=main_W, main_PL=main_PL, J=J, race=R.race[ii]))
    return {k: np.concatenate([o[k] for o in out]) for k in out[0]}


def stack_rows(R, U, e_lo=-3, e_hi=6, y_max=2021):
    """Rows of the stacked event panel (IGE/19 stacks) for the units U with pseudo == 0: every observed income year
    ev + e, e = e_lo..e_hi, Y <= y_max, in which the man is observed. Outcomes: hh, hlab, fs (married rows only),
    bw_present (married at the interview), w_hrs, w_emp, w_lab (while married)."""
    sel = U["pseudo"] == 0
    ui = np.nonzero(sel)[0]
    rows = []
    ny = R.dh_year.shape[1]
    for e in range(e_lo, e_hi + 1):
        Y = U["ev"][ui] + e
        ok = np.isin(Y, OBS_YEARS) & (Y <= y_max) & (Y >= M0) & (Y - M0 < ny)
        u2 = ui[ok]
        yi = (Y[ok] - M0)
        ii = U["i"][u2]
        mobs = R.man_obs[ii, yi]
        u2, yi, ii = u2[mobs], yi[mobs], ii[mobs]
        rm = R.row_mar[ii, yi]
        nanw = lambda v: np.where(rm, v, np.nan)                     # noqa: E731
        rows.append(dict(u=u2, e=np.full(len(u2), e), Y=yi + M0, hh=nanw(R.hh_ann[ii, yi]),
                         hlab=nanw(R.hlab_ann[ii, yi]), fs=nanw(R.fs_ann[ii, yi].astype(float)),
                         bw_present=R.mar_int[ii, yi].astype(float), w_hrs=nanw(R.wh_ann[ii, yi]),
                         w_emp=nanw((R.wh_ann[ii, yi] > 0).astype(float)), w_lab=nanw(R.wlab_ann[ii, yi])))
    P = {k: np.concatenate([r[k] for r in rows]) for k in rows[0]}
    for k in ("treat", "J", "young0", "race", "ev", "wemp0"):
        P[k] = U[k][P["u"]]
    P["unit"] = P["u"]
    P["cell"] = P["Y"].astype(np.int64) * 10000 + P["ev"].astype(np.int64)
    return P


def cons_rows(R, U, ev_lo=2000, ev_hi=2020, var_me=0.0332):
    """IGE/47 event panel: units (pseudo == 0) with events 2000-2020, married at baseline; interview waves 1999-2021
    with tau = wave - ev in -4..6, still married at the interview; log consumption (interview month's flow x 12, 2000
    $) plus BPS's measurement error; k = KBIN[tau]; units with >= 2 interviews."""
    sel = (U["pseudo"] == 0) & (U["ev"] >= ev_lo) & (U["ev"] <= ev_hi)
    ui = np.nonzero(sel)[0]
    rows = []
    for W_ in CONS_WAVES:
        m = mi(W_, 4)
        if m >= R.nm:
            continue
        tau = W_ - U["ev"][ui]
        ok = (tau >= -4) & (tau <= 6)
        u2 = ui[ok]
        ii = U["i"][u2]
        okm = R.MAR[ii, m] & (W_ >= R.year0[ii])
        u2, ii, tau2 = u2[okm], ii[okm], tau[ok][okm]
        if len(u2) == 0:
            continue
        cval = R.c[ii, m].astype(float) * 12000.0
        eps = ndtri(crn_u(R.seed, R.uid[ii], m, 50)) * np.sqrt(var_me)
        lc = np.log(np.where(cval > 0, cval, np.nan)) + eps
        rows.append(dict(u=u2, wave=np.full(len(u2), W_), k=np.array([KBIN[int(t)] for t in tau2]), lc=lc))
    P = {k: np.concatenate([r[k] for r in rows]) for k in rows[0]}
    ok = np.isfinite(P["lc"]) & np.isfinite(U["J"][P["u"]])
    P = {k: v[ok] for k, v in P.items()}
    cnt = np.bincount(P["u"], minlength=len(U["i"]))
    ok = cnt[P["u"]] >= 2
    P = {k: v[ok] for k, v in P.items()}
    for k in ("treat", "J", "race"):
        P[k] = U[k][P["u"]]
    P["unit"] = P["u"]
    P["cell"] = P["wave"].astype(np.int64) * 10000 + U["ev"][P["u"]].astype(np.int64)
    return P


def couple_years(R, y_max=2021):
    """IGE/25 couple-years: consecutive interviews of the same couple, both spouses with positive annual hours in the
    earlier year; h / w = displaced in the interval (calendar years py + 1 .. Y)."""
    ny = R.dh_year.shape[1]
    out = []
    for Y in OBS_YEARS:
        if Y > y_max or Y - M0 >= ny:
            continue
        py = int(_prev_obs(Y))
        if py < M0:
            continue
        yi, pi = Y - M0, py - M0
        ok = R.row_mar[:, yi] & R.row_mar[:, pi] & (R.hh_ann[:, pi] > 0) & (R.wh_ann[:, pi] > 0)
        ii = np.nonzero(ok)[0]
        h = R.dh_year[ii, pi + 1:yi + 1].any(axis=1).astype(float)
        w = R.dw_year[ii, pi + 1:yi + 1].any(axis=1).astype(float)
        out.append(dict(i=ii, Y=np.full(len(ii), Y), h=h, w=w, same=(R.s[ii] >= 1).astype(float), race=R.race[ii]))
    return {k: np.concatenate([o[k] for o in out]) for k in out[0]}


def husband_risk_rows(R, y_lo=1984, y_max=2021):
    """IGE/19 annual displacement measure: married husbands (wife present at the interview) with positive hours in
    the previous observed year (within two years); y = main displacement dated to the year."""
    ny = R.dh_year.shape[1]
    out = []
    for Y in OBS_YEARS:
        if Y < y_lo or Y > y_max or Y - M0 >= ny:
            continue
        py = int(_prev_obs(Y))
        if py < M0:
            continue
        yi, pi = Y - M0, py - M0
        ok = R.row_mar[:, yi] & R.row_mar[:, pi] & (R.hh_ann[:, pi] > 0)
        ii = np.nonzero(ok)[0]
        out.append(dict(i=ii, Y=np.full(len(ii), Y), y=R.dh_year[ii, yi].astype(float), race=R.race[ii]))
    return {k: np.concatenate([o[k] for o in out]) for k in out[0]}


def sep_rows(R, y_lo=1984, y_max=2021):
    """Married couples (wife 25-59) at the interview of Y whose husband is observed at the next interview; sep = the
    wife is no longer his wife there; L = years between the interviews."""
    ny = R.dh_year.shape[1]
    out = []
    for Y in OBS_YEARS:
        ny_ = int(_next_obs(Y))
        if Y < y_lo or ny_ > y_max or ny_ - M0 >= ny:
            continue
        yi, ni = Y - M0, ny_ - M0
        ok = R.mar_int[:, yi] & (R.years[yi] >= R.year0) & R.obs_int[:, ni] & (R.w_agey[:, yi] >= 25) & \
            (R.w_agey[:, yi] <= 59)
        ii = np.nonzero(ok)[0]
        out.append(dict(i=ii, sep=(~R.mar_int[ii, ni]).astype(float), L=np.full(len(ii), float(ny_ - Y)),
                        race=R.race[ii]))
    return {k: np.concatenate([o[k] for o in out]) for k in out[0]}


def wage_growth_rows(R, t_max=2019):
    """Two-year log wage growth of the continuously employed (IGE/60): hours >= 1000 in t and t + 2 (and in t + 1 when
    observed), wage = annual labor income / annual hours in [2, 200] 2000 $, same couple in t and t + 2."""
    ny = R.dh_year.shape[1]
    out = {"w": [], "h": []}
    for t in OBS_YEARS:
        if t > t_max or (t + 2) not in OBS_YEARS or t + 2 - M0 >= ny:
            continue
        ti, t2 = t - M0, t + 2 - M0
        both = R.row_mar[:, ti] & R.row_mar[:, t2]
        mid = (t + 1) in OBS_YEARS
        for sp, hrs, lab, agoff in (("w", R.wh_ann, R.wlab_ann, 0), ("h", R.hh_ann, R.hlab_ann, 2)):
            ok = both & (hrs[:, ti] >= 1000) & (hrs[:, t2] >= 1000)
            if mid:
                ok &= ~R.row_mar[:, ti + 1] | (hrs[:, ti + 1] >= 1000)
            ii = np.nonzero(ok)[0]
            w0 = lab[ii, ti] / hrs[ii, ti]
            w2 = lab[ii, t2] / hrs[ii, t2]
            ok2 = (w0 >= 2) & (w0 <= 200) & (w2 >= 2) & (w2 <= 200)
            ii, w0, w2 = ii[ok2], w0[ok2], w2[ok2]
            out[sp].append(dict(dl=np.log(w2) - np.log(w0), age=R.w_agey[ii, ti].astype(int) + agoff))
    return {k: {kk: np.concatenate([o[kk] for o in v]) for kk in v[0]} for k, v in out.items()}


def reentry_rows(R, t_lo=1985, t_hi=1996):
    """Her log wage at re-entry after a full calendar year out (annual interviews only, 1985-1996)."""
    out = []
    for t in range(t_lo, t_hi + 1):
        ti = t - M0
        ok = R.row_mar[:, ti] & R.row_mar[:, ti - 1] & (R.w_agey[:, ti] >= 25) & (R.w_agey[:, ti] <= 59)
        whp, wh, wl = R.wh_ann[:, ti - 1], R.wh_ann[:, ti], R.wlab_ann[:, ti]
        re_ = (whp == 0) & (wh >= 260)
        co_ = (whp >= 1000) & (wh >= 1000)
        ii = np.nonzero(ok & (re_ | co_))[0]
        w = wl[ii] / wh[ii]
        ok2 = (w >= 2) & (w <= 200)
        ii, w = ii[ok2], w[ok2]
        out.append(dict(lw=np.log(w), re=re_[ii].astype(float), age=R.w_agey[ii, ti].astype(int),
                        Y=np.full(len(ii), t)))
    return {k: np.concatenate([o[k] for o in out]) for k in out[0]}


def wealth_rows(R):
    """Liquid wealth at the interview of the wealth waves; earnings of the calendar year before."""
    out = []
    for W_ in WEALTH_WAVES:
        m = mi(W_, 4)
        yi = W_ - 1 - M0
        if m >= R.nm or yi < 0:
            continue
        age = 25 + (m - R.m_off) // 12
        ok = R.MAR[:, m] & (age >= 25) & (age <= 59) & R.full_mar[:, yi] & (W_ - 1 >= R.year0)
        ii = np.nonzero(ok)[0]
        out.append(dict(liq=R.a[ii, m].astype(float) * 1000.0, earn=R.hlab_ann[ii, yi] + R.wlab_ann[ii, yi],
                        age=age[ii]))
    return {k: np.concatenate([o[k] for o in out]) for k in out[0]}


# ======================================================================================================================
# Extension moments (2026-10-19; computed only when requested: moments.compute(ext_moments=...))
# ======================================================================================================================
@njit(cache=True)
def _run_start(W, st):
    """S[i, m] = first month of the current run of W (married wife works) if W[i, m], else -1; C[i, m] = the run began
    in the couple-copy's first month in the sample (left-censored: tenure unknown below the run's length)."""
    n, nm = W.shape
    S = np.full((n, nm), -1, np.int32)
    C = np.zeros((n, nm), np.bool_)
    for i in range(n):
        first = -1
        cur = -1
        for m in range(nm):
            if first < 0 and st[i, m] >= 0:
                first = m
            if W[i, m]:
                if cur < 0:
                    cur = m
                S[i, m] = cur
                C[i, m] = cur == first
            else:
                cur = -1
    return S, C


def sipp_tenure_exits(R, H=12):
    """New-job extension, SIPP (IGE/66 from IGE/63's sample): wife-months t in the three panel windows with t-1 .. t+2
    inside the window, married t-1 .. t+2, wife works t-1 and t, husband works t and t+1, wife 25-59; y = not working
    t+1 and t+2 (all reasons); tenure = t - first month of the current employment spell (a spell that began in the
    couple-copy's first simulated month is left-censored: 12+ if at least 12 months old, else unknown and dropped).
    Also the Kaplan-Meier return to work within H months of the first non-working month t+1 (W at t+2 .. t+1+H,
    censored when the window ends or the couple separates). Returns dict(y, ten, ret) with ret the KM curve."""
    MAR, W, HW = R.MAR, R.W, R.HW
    S = lambda A, k: shift(A, k)                                     # noqa: E731
    St, Cn = _run_start(W, R.st)
    nm = R.nm
    age = 25 + (np.arange(nm)[None, :] - R.m_off[:, None]) // 12
    ys, tens, stat = [], [], []
    for (ya, ma, yb, mb) in SIPP_WINDOWS:
        lo, hi = mi(ya, ma), mi(yb, mb)
        mm = np.arange(nm)[None, :]
        inwin = (mm - 1 >= lo) & (mm + 2 <= hi)
        base = inwin & S(MAR, -1) & MAR & S(MAR, 1) & S(MAR, 2) & S(W, -1) & W & HW & S(HW, 1) & (age >= 25) &             (age <= 59)
        ii, tt = np.nonzero(base)
        y = (~S(W, 1)[ii, tt] & ~S(W, 2)[ii, tt]).astype(float)
        ten = (tt - St[ii, tt]).astype(float)
        cen = Cn[ii, tt]
        ten = np.where(cen & (ten < 12), np.nan, ten)
        ys.append(y)
        tens.append(ten)
        ex = y == 1
        ie, te = ii[ex], tt[ex]
        stt = np.full((len(ie), H), np.nan)
        for s_ in range(1, H + 1):
            m2 = te + 1 + s_
            ok = (m2 <= hi) & (m2 < nm)
            m2c = np.minimum(m2, nm - 1)
            obs = ok & MAR[ie, m2c]
            stt[:, s_ - 1] = np.where(obs, W[ie, m2c].astype(float), np.nan)
        stat.append(stt)
    y, ten, stt = np.concatenate(ys), np.concatenate(tens), np.concatenate(stat)
    alive = np.ones(len(stt), bool)
    Sv, ret = 1.0, []
    for s_ in range(H):
        st_ = stt[:, s_]
        obs = alive & np.isfinite(st_)
        ev = obs & (st_ == 1)
        h = ev.sum() / obs.sum() if obs.sum() > 0 else 0.0
        Sv *= 1 - h
        ret.append(1 - Sv)
        alive = obs & ~ev
    return dict(y=y, ten=ten, ret=np.array(ret), n_exits=len(stt))


def psid_repeat_exits(R, t_lo=1984, t_hi=1995):
    """New-job extension, PSID (IGE/63 v-repeat): couple-years t (t + 1 <= 1996) married through t and t + 1, her and
    his hours > 0 in t, his > 0 in t + 1, wife 25-59; exit = her hours 0 in t + 1. Returns the share of couple-copies
    with at least one exit that have two or more, and the number of such couples."""
    ny = R.dh_year.shape[1]
    ii_, yy_ = [], []
    for t in range(t_lo, t_hi + 1):
        ti = t - M0
        if ti + 1 >= ny:
            continue
        ok = R.row_mar[:, ti] & R.row_mar[:, ti + 1] & (R.wh_ann[:, ti] > 0) & (R.hh_ann[:, ti] > 0) &             (R.hh_ann[:, ti + 1] > 0) & (R.w_agey[:, ti] >= 25) & (R.w_agey[:, ti] <= 59)
        ii = np.nonzero(ok)[0]
        ii_.append(ii)
        yy_.append((R.wh_ann[ii, ti + 1] == 0).astype(float))
    ii, y = np.concatenate(ii_), np.concatenate(yy_)
    ne = np.bincount(ii, weights=y, minlength=R.n)
    ex = ne > 0
    return ((ne[ex] >= 2).mean() if ex.any() else np.nan), int(ex.sum())


def her_stack_rows(R, ev_lo=1984, ev_hi=2021, y_max=2021, e_lo=-3, e_hi=6):
    """Her-displacement extension (IGE/64 M3, IGE/65 5b): wife x stack units; baseline = her row of ev - 1 if that
    income year is observed, else ev - 2: married through the year and at the interview, a child under 18, her positive
    hours; treated = her first displacement since entry (any marital status: separated wives keep their records) in ev;
    clean controls = none to ev + 6 (CRN subsample at ctrl_rate, slot 53). Rows: observed income years ev + e, e =
    -3..6, Y <= y_max; outcome bh_present = married to the baseline husband at the interview of wave Y + 1 (the model has
    no remarriage and no attrition, so 65's 'both observed at the first interview' restriction does not bind)."""
    ny = R.dh_year.shape[1]
    n = R.n
    years = R.years
    dwa = (R._disp_w == 1) & (R.st >= 0)
    dwy = dwa[:, :ny * 12].reshape(n, ny, 12).any(axis=2)
    has = dwy & (years[None, :] >= R.year0[:, None])
    fm = np.where(has.any(axis=1), years[np.argmax(has, axis=1)], 9999)
    units = []
    for ev in range(max(ev_lo, M0 + 1), min(ev_hi, M0 + ny) + 1):
        b1, b2 = ev - 1, ev - 2
        y1i, y2i = b1 - M0, b2 - M0
        obs1 = R.man_obs[:, y1i] if (b1 in OBS_YEARS and y1i < ny) else np.zeros(n, bool)
        obs2 = R.man_obs[:, y2i] if (b2 in OBS_YEARS and y2i >= 0) else np.zeros(n, bool)
        by = np.where(obs1, b1, np.where(obs2, b2, -1))
        ii = np.nonzero(by > 0)[0]
        bi = by[ii] - M0
        elig = R.row_mar[ii, bi] & (R.wh_ann[ii, bi] > 0) & (R.k_int[ii, bi] > 0)
        ii = ii[elig]
        tr = fm[ii] == ev
        ct = fm[ii] > ev + 6
        keep_ct = crn_u(R.seed, R.uid[ii] * 64 + (ev - 1960), 0, 53) < R.ctrl_rate
        sel = tr | (ct & keep_ct)
        units.append((ii[sel], np.full(sel.sum(), ev), tr[sel].astype(float)))
    ui = np.concatenate([u[0] for u in units])
    uev = np.concatenate([u[1] for u in units])
    utr = np.concatenate([u[2] for u in units])
    rows = []
    for e in range(e_lo, e_hi + 1):
        Y = uev + e
        ok = np.isin(Y, OBS_YEARS) & (Y <= y_max) & (Y >= M0) & (Y - M0 < ny)
        k = np.nonzero(ok)[0]
        yi = Y[k] - M0
        mobs = R.man_obs[ui[k], yi]
        k, yi = k[mobs], yi[mobs]
        rows.append(dict(u=k, e=np.full(len(k), e), Y=yi + M0, bh_present=R.mar_int[ui[k], yi].astype(float)))
    P = {kk: np.concatenate([r[kk] for r in rows]) for kk in rows[0]}
    P["treat"] = utr[P["u"]]
    P["ev"] = uev[P["u"]]
    P["unit"] = P["u"]
    P["cell"] = P["Y"].astype(np.int64) * 10000 + P["ev"].astype(np.int64)
    return P
