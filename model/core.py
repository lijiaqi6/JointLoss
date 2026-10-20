r"""Paper B structural model: solution, simulation and the moment function shared by data and simulation (2026-10-18).

Model: paperB_age_profile/model_document.tex (Sections 1-8). Annual career from a0(e) = 18 + max(e - 12, 0) to 55,
risk-neutral sons, two job types (G, O), one access logit for every offer, a match component, displacement,
human capital accumulation that depends on the job type and on schooling (race-specific pay-off), depreciation out of
work, a transitory wage shock. Homogeneity: payoffs are proportional to exp(mu_r + h) and h evolves additively with
shocks independent of the state, so V(h, m, j) = exp(mu_r + h) v(m, j): decisions do not depend on h, and only
v_a(m, j) and v_a^U are solved (per son type, vectorised).

The moment function `moments(P, C)` takes a long panel P (one row per observed interview; numpy arrays) built in the
same way from the PSID (build_data.py) and from the simulation (simulate_panel), and returns the moment vector in the
fixed order of MOMENT_NAMES.
"""
import os

import numpy as np

# ---------------------------------------------------------------- fixed inputs
NATUR = {1963: 5.7, 1964: 5.2, 1965: 4.5, 1966: 3.8, 1967: 3.8, 1968: 3.6, 1969: 3.5, 1970: 4.9, 1971: 5.9, 1972: 5.6,
         1973: 4.9, 1974: 5.6, 1975: 8.5, 1976: 7.7, 1977: 7.1, 1978: 6.1, 1979: 5.8, 1980: 7.1, 1981: 7.6, 1982: 9.7,
         1983: 9.6, 1984: 7.5, 1985: 7.2, 1986: 7.0, 1987: 6.2, 1988: 5.5, 1989: 5.3, 1990: 5.6, 1991: 6.8, 1992: 7.5,
         1993: 6.9, 1994: 6.1, 1995: 5.6, 1996: 5.4, 1997: 4.9, 1998: 4.5, 1999: 4.2, 2000: 4.0, 2001: 4.7, 2002: 5.8,
         2003: 6.0, 2004: 5.5, 2005: 5.1, 2006: 4.6, 2007: 4.6, 2008: 5.8, 2009: 9.3, 2010: 9.6, 2011: 8.9, 2012: 8.1,
         2013: 7.4, 2014: 6.2, 2015: 5.3, 2016: 4.9, 2017: 4.4, 2018: 3.9, 2019: 3.7, 2020: 8.1, 2021: 5.3, 2022: 3.6,
         2023: 3.6, 2024: 4.0}
UBAR = 6.0
UARR = np.array([NATUR.get(y, UBAR) for y in range(1900, 2100)])
ENTRY_SHOCK = None                                                # None in estimation; set only by postestimation.py
WAVES = list(range(1968, 1998)) + list(range(1999, 2024, 2))     # PSID interview years
CAL = dict(beta=0.95, b=0.4, phi_lam=-0.10, phi_del=0.10)        # calibrated (model document, Section 9)
AMIN, AMAX = 18, 55
NA = AMAX - AMIN                                                  # career years 18..54 (index 0..36); 55 terminal
GH_Z, GH_W = np.polynomial.hermite_e.hermegauss(9)
GH_W = GH_W / GH_W.sum()
NM = 31                                                           # match grid points

PARAMS = ["muB", "b0", "bx", "b1", "db1", "lsig0", "a0", "a1", "a2", "a3", "llam_e", "llam_u", "muG", "lsigm",
          "d0B", "d0W", "d1", "gO", "gG", "lrho", "g1", "dg1", "du", "lsigeta", "lsigeps"]
# Model steps after the first lattice (Fable memo proposals/fable_hpc_next_paperB.md, R4-R5), off by default so that
# the first-step results are reproduced exactly. IGE_STEPS="age,rehire":
#   age    - age slopes in displacement and in the on-the-job search friction: logit delta += da (a - 30)/10,
#            logit lambda_e += la (a - 30)/10 (two parameters; age is already a state)
#   rehire - a son displaced in a year can be re-employed in the same year (he draws an out-of-work offer with the
#            otherwise unused uniform); job finding out of work is then estimated off its old 0.99 cap (0.52 in the
#            2026-10-18 runs), so the cap is replaced by the probability bound 1 in the solution and the simulation
#   xacc   - step 4 (Fable memo, second round): parental income in accumulation, Delta_j(a) adds
#            [gx + dgx 1(Black)] (x - xbar) e^{-rho(a - 18)}; gx is race-neutral, dgx is the fourth race hypothesis H4
STEPS = set(filter(None, os.environ.get("IGE_STEPS", "").split(",")))
EXTRA = (["da", "la"] if "age" in STEPS else []) + (["gx", "dgx"] if "xacc" in STEPS else []) +     (["dlu"] if "ufric" in STEPS else []) + (["aa"] if "aage" in STEPS else []) + (["dG"] if "gloss" in STEPS else [])
#   gloss  - step 7 candidate (Fable 10-hour plan, Block 4): G jobs have their own displacement rate, logit delta += dG 1[j = G]
#            (PSID: G jobs are lost at half the rate of O jobs at 35-55). One parameter. No new draws.
#   aage   - step 6 (Fable 10-hour plan, Block 4): access to G jobs rises with age, logit p += aa (a - 30)/10, for every
#            offer at the son's age (entry, out of work, on the job); one parameter. No new draws.
MOMSET = set(filter(None, os.environ.get("IGE_MOMENTS", "").split(",")))   # "g35" adds the G shares at 35-55
#   ufric  - step 5 (Fable 3-hour plan, 2026-10-19): a race-specific search friction out of work, logit lambda_u += dlu
#            1(Black); one parameter aimed at the zero-hours misfit (Black too few, White too many with the displacement
#            rates fitted). The draws are used as before, so common random numbers hold.
UCAP = 1.0 if "rehire" in STEPS else 0.99
PARAMS = PARAMS + EXTRA


def theta_vec(d):
    """parameter vector from a dict; parameters of later steps missing from an earlier run start at 0."""
    return np.array([d.get(p, 0.0) if p in EXTRA else d[p] for p in PARAMS], float)


NESTED = {"A": {"a3", "dg1", "db1"}, "B": {"dg1", "db1"}, "C": {"db1"}, "D": set(),
          "E": {"a3"}, "F": {"a3", "db1"}, "G": {"a3", "dg1"}, "H": {"dg1"}}
# parameters fixed at 0. Hypotheses: H1 access (a3), H2 pay-off of schooling in accumulation (dg1), H3 entry return to
# schooling (db1). All 8 combinations: A none, B H1, F H2, G H3, C H1+H2, H H1+H3, E H2+H3, D all (2026-10-18).


def logistic(z):
    return 1.0 / (1.0 + np.exp(-z))


def unpack(th):
    p = dict(zip(PARAMS, th))
    q = dict(p)
    q["sig0"], q["sigm"], q["sigeta"], q["sigeps"] = (np.exp(p["lsig0"]), np.exp(p["lsigm"]), np.exp(p["lsigeta"]),
                                                       np.exp(p["lsigeps"]))
    q["lam_e"], q["lam_u"], q["rho"] = logistic(p["llam_e"]), logistic(p["llam_u"]), np.exp(p["lrho"])
    return q


# ---------------------------------------------------------------- types
class Types:
    """unique son types (race, x, e, birth year) with centred covariates."""

    def __init__(self, black, x, e, byear, xbar):
        self.black = np.asarray(black, float)
        self.x = np.asarray(x, float)
        self.e = np.asarray(e, float)
        self.byear = np.asarray(byear, int)
        self.xc = self.x - xbar
        self.ec = self.e - 12.0
        self.a0 = (18 + np.clip(self.e - 12, 0, 6)).round().astype(int)
        self.n = len(self.x)


def access(q, T, a=None):
    z = q["a0"] + q["a1"] * T.xc + q["a2"] * T.ec + q["a3"] * T.black
    if a is not None and "aage" in STEPS:
        z = z + q.get("aa", 0.0) * (np.asarray(a) - 30) / 10
    return logistic(z)


def delta_bar(q, T, a=30, j=0):
    d0 = np.where(T.black == 1, q["d0B"], q["d0W"])
    return logistic(d0 + q["d1"] * T.xc + q.get("da", 0.0) * (a - 30) / 10 + q.get("dG", 0.0) * j)


def lam_u_of(q, T):
    """job finding out of work per type (n,): logistic(llam_u + dlu 1[Black])."""
    return logistic(q["llam_u"] + q.get("dlu", 0.0) * T.black)


def lam_e_at(q, a):
    return logistic(q["llam_e"] + q.get("la", 0.0) * (a - 30) / 10)


def accum(q, T, a):
    """Delta_j(a) for j = O, G: (n, 2)."""
    g1 = q["g1"] + q["dg1"] * T.black
    ga = np.exp(-q["rho"] * (a - 18))
    base = g1 * T.ec + (q.get("gx", 0.0) + q.get("dgx", 0.0) * T.black) * T.xc
    return np.column_stack([(q["gO"] + base) * ga, (q["gG"] + base) * ga])


def mgrid(q):
    lo = -4 * q["sigm"]
    hi = q["muG"] + 4 * q["sigm"]
    return np.linspace(min(lo, -0.5), max(hi, 0.5), NM)


def interp_w(grid, pts):
    pts = np.clip(pts, grid[0], grid[-1])
    i = np.clip(np.searchsorted(grid, pts) - 1, 0, len(grid) - 2)
    w = (pts - grid[i]) / (grid[i + 1] - grid[i])
    return i, w


# ---------------------------------------------------------------- solution
def solve(q, T):
    """vE[n, k, j, m] and vU[n, k] for ages a = 18 + k, k = 0..NA (NA terminal = 0), per type."""
    beta, b = CAL["beta"], CAL["b"]
    G = mgrid(q)
    n = T.n
    vE = np.zeros((n, NA + 1, 2, NM))
    vU = np.zeros((n, NA + 1))
    pG = access(q, T)[:, None]
    db = delta_bar(q, T)[:, None]
    lam_e, lam_u = q["lam_e"], (lam_u_of(q, T) if "ufric" in STEPS else q["lam_u"])
    if "rehire" in STEPS:
        lam_u = np.minimum(lam_u, UCAP)
    iG, wG = interp_w(G, q["muG"] + q["sigm"] * GH_Z)
    iO, wO = interp_w(G, q["sigm"] * GH_Z)
    flowE = np.exp(G + q["sigeps"] ** 2 / 2)[None, :]
    ceta = np.exp(q["sigeta"] ** 2 / 2)
    for k in range(NA - 1, -1, -1):
        a = AMIN + k
        v1 = vE[:, k + 1]                                         # (n, 2, M)
        u1 = vU[:, k + 1][:, None]                                # (n, 1)
        nG = v1[:, 1, iG] * (1 - wG) + v1[:, 1, iG + 1] * wG      # (n, K) value of G offers
        nO = v1[:, 0, iO] * (1 - wO) + v1[:, 0, iO + 1] * wO
        Dlt = accum(q, T, a)                                       # (n, 2)
        if "age" in STEPS:
            db, lam_e = delta_bar(q, T, a)[:, None], lam_e_at(q, a)
        if "aage" in STEPS:
            pG = access(q, T, a)[:, None]
        emu = (pG[:, 0] * (np.maximum(u1, nG) * GH_W).sum(-1) + (1 - pG[:, 0]) * (np.maximum(u1, nO) * GH_W).sum(-1))
        lost = (lam_u * emu + (1 - lam_u) * u1[:, 0])[:, None] if "rehire" in STEPS else u1
        for j in (0, 1):
            cur = v1[:, j, :]                                     # (n, M)
            emax = (pG * (np.maximum(cur[:, :, None], nG[:, None, :]) * GH_W).sum(-1)
                    + (1 - pG) * (np.maximum(cur[:, :, None], nO[:, None, :]) * GH_W).sum(-1))
            dbj = delta_bar(q, T, a if "age" in STEPS else 30, j)[:, None] if "gloss" in STEPS else db
            cont = dbj * lost + (1 - dbj) * ((1 - lam_e) * cur + lam_e * emax)
            vE[:, k, j, :] = flowE + beta * np.exp(Dlt[:, j:j + 1]) * ceta * cont
        vU[:, k] = b + beta * np.exp(-q["du"]) * ceta * (lam_u * emu + (1 - lam_u) * u1[:, 0])
    return vE, vU, G


def vE_at(vE, G, idx, k, j, m):
    """value at continuous m for sons idx (types), age index k (per son), job j (per son)."""
    i, w = interp_w(G, m)
    v = vE[idx, k, j]
    return v[np.arange(len(idx)), i] * (1 - w) + v[np.arange(len(idx)), i + 1] * w


# ---------------------------------------------------------------- simulation
class Draws:
    def __init__(self, n, seed):
        rng = np.random.default_rng(seed)
        self.nu = rng.standard_normal(n)
        self.ue = rng.random(n)                                    # entry offer type
        self.ze = rng.standard_normal(n)                           # entry match
        self.ud = rng.random((n, NA))
        self.uo = rng.random((n, NA))
        self.ut = rng.random((n, NA))
        self.zm = rng.standard_normal((n, NA))
        self.zh = rng.standard_normal((n, NA))
        self.zw = rng.standard_normal((n, NA))


def simulate(q, T, idx, D, sol=None):
    """simulate sons idx (indices into types, replicated) -> year arrays (n, NA)."""
    vE, vU, G = solve(q, T) if sol is None else sol
    n = len(idx)
    bl = T.black[idx]
    xc, ec, a0, by = T.xc[idx], T.ec[idx], T.a0[idx], T.byear[idx]
    pG = access(q, T)[idx]
    d0 = np.where(bl == 1, q["d0B"], q["d0W"])
    mu_r = q["muB"] * bl
    b1 = q["b1"] + q["db1"] * bl
    emp = np.zeros(n, bool)
    j = np.zeros(n, int)
    m = np.zeros(n)
    h = np.full(n, np.nan)
    eid = np.full(n, -1, int)
    nxt = 0
    LW = np.full((n, NA), np.nan)
    EMP = np.zeros((n, NA), bool)
    JOB = np.full((n, NA), -1, int)                               # job at the start of year k+1 (interview)
    EID = np.full((n, NA), -1, int)
    DSP = np.zeros((n, NA), bool)
    ar = np.arange(n)
    for k in range(NA):
        a = AMIN + k
        start = a0 == a
        if start.any():
            s = np.where(start)[0]
            h[s] = q["b0"] + q["bx"] * xc[s] + b1[s] * ec[s] + q["sig0"] * D.nu[s]
            pe = access(q, T, a)[idx[s]] if "aage" in STEPS else pG[s]
            jj = (D.ue[s] < pe).astype(int)
            mm = np.where(jj == 1, q["muG"], 0.0) + q["sigm"] * D.ze[s]
            acc = vE_at(vE, G, idx[s], np.full(len(s), k), jj, mm) > vU[idx[s], k]
            emp[s] = acc
            j[s] = np.where(acc, jj, 0)
            m[s] = np.where(acc, mm, 0.0)
            eid[s] = np.where(acc, nxt + np.arange(len(s)), -1)
            nxt += len(s)
        act = a >= a0
        EMP[:, k] = emp & act
        LW[:, k] = np.where(emp & act, mu_r + h + m, np.nan)
        # human capital
        Dlt = accum(q, T, a)[idx]
        gain = np.where(emp, Dlt[ar, j], -q["du"])
        h = np.where(act, h + gain + q["sigeta"] * D.zh[:, k], h)
        if k == NA - 1:
            JOB[:, k] = np.where(emp & act, j, -1)
            EID[:, k] = np.where(emp & act, eid, -1)
            break
        ut = UARR[np.clip(by + a - 1900, 0, 199)] - UBAR
        if ENTRY_SHOCK is not None:                               # counterfactual: points added in the years after entry
            ut = ut + np.where(act, ENTRY_SHOCK[np.clip(a - a0, 0, len(ENTRY_SHOCK) - 1)], 0.0)
        dl = logistic(d0 + q["d1"] * xc + q.get("da", 0.0) * (a - 30) / 10 + q.get("dG", 0.0) * j + CAL["phi_del"] * ut)
        lu = np.minimum(UCAP, (lam_u_of(q, T)[idx] if "ufric" in STEPS else q["lam_u"]) * np.exp(CAL["phi_lam"] * ut))
        disp = act & emp & (D.ud[:, k] < dl)
        DSP[:, k] = disp
        jo = (D.ut[:, k] < (access(q, T, a)[idx] if "aage" in STEPS else pG)).astype(int)
        mo = np.where(jo == 1, q["muG"], 0.0) + q["sigm"] * D.zm[:, k]
        vnew = vE_at(vE, G, idx, np.full(n, k + 1), jo, mo)
        # employed, not displaced: on-the-job offer
        oe = act & emp & ~disp & (D.uo[:, k] < lam_e_at(q, a))
        vcur = vE_at(vE, G, idx, np.full(n, k + 1), j, m)
        mv = oe & (vnew > vcur)
        # not employed: offer
        ou = act & (~emp | disp if "rehire" in STEPS else ~emp) & (D.uo[:, k] < lu)   # rehire: same-year offer
        hire = ou & (vnew > vU[idx, k + 1])
        new = mv | hire
        j = np.where(new, jo, j)
        m = np.where(new, mo, m)
        eid = np.where(new, nxt + ar, np.where(disp, -1, eid))
        nxt += n
        emp = (emp & ~disp) | hire
        JOB[:, k] = np.where(emp & act, j, -1)
        EID[:, k] = np.where(emp & act, eid, -1)
    LW = LW + q["sigeps"] * D.zw
    return dict(LW=LW, EMP=EMP, JOB=JOB, EID=EID, DSP=DSP)


def simulate_panel(q, T, idx, D, sol=None):
    """PSID observation scheme: interview W observes income year W - 1 (age index W - 1 - byear - 18); rows sorted by
    son and wave. Returns the long panel P (dict of arrays)."""
    S = simulate(q, T, idx, D, sol)
    n = len(idx)
    by = T.byear[idx]
    rows = []
    cum = np.concatenate([np.zeros((n, 1)), np.cumsum(S["DSP"], axis=1)], axis=1)   # cum[:, k] = disp in years < k
    for W in WAVES:
        age = W - by
        k = W - 1 - by - AMIN
        ok = (age >= 25) & (age <= 55) & (k >= 0) & (k < NA) & (k + AMIN >= T.a0[idx])
        s = np.where(ok)[0]
        if len(s) == 0:
            continue
        kk = k[s]
        rows.append(dict(sid=s, wave=np.full(len(s), W), age=age[s], k=kk, lw=S["LW"][s, kk],
                         zero=(~S["EMP"][s, kk]).astype(float), G=S["JOB"][s, kk].astype(float),
                         eid=S["EID"][s, kk]))
    P = {c: np.concatenate([r[c] for r in rows]) for c in rows[0]}
    o = np.lexsort((P["wave"], P["sid"]))
    P = {c: v[o] for c, v in P.items()}
    P["G"] = np.where(P["G"] < 0, np.nan, P["G"])
    sid, k = P["sid"], P["k"]
    first = np.r_[True, sid[1:] != sid[:-1]]
    prev_k = np.r_[0, k[:-1]]
    prev_eid = np.r_[-1, P["eid"][:-1]]
    gap = np.r_[0, P["wave"][1:] - P["wave"][:-1]].astype(float)
    gap[first] = np.nan
    # displacement in income years from the previous wage year to the current one (inclusive)
    nd = cum[sid, np.minimum(k + 1, NA)] - cum[sid, np.where(first, k, prev_k)]
    P["gap"] = gap
    P["disp"] = np.where(first, np.nan, (nd > 0).astype(float))
    P["stay"] = np.where(first, np.nan, ((P["eid"] >= 0) & (P["eid"] == prev_eid)).astype(float))
    P["black"] = T.black[idx][sid]
    P["x"] = T.x[idx][sid]
    P["e"] = T.e[idx][sid]
    P["pid"] = sid
    return P


# ---------------------------------------------------------------- moments
BANDS6 = [(25, 29), (30, 34), (35, 39), (40, 44), (45, 49), (50, 55)]


def _ols(y, X):
    ok = np.isfinite(y) & np.all(np.isfinite(X), axis=1)
    if ok.sum() < X.shape[1] + 5:
        return np.full(X.shape[1], np.nan)
    b = np.linalg.lstsq(X[ok], y[ok], rcond=None)[0]
    return b


def _agedum(age, lo, hi):
    return np.column_stack([(age == a).astype(float) for a in range(lo + 1, hi + 1)])


def moment_names():
    nm = []
    for r in ("B", "W"):
        nm += [f"ige_{lo}{hi}_{r}" for lo, hi in BANDS6]
    for r in ("B", "W"):
        nm += [f"rets_{lo}{hi}_{r}" for lo, hi in BANDS6]
    nm += ["mlw2529_B", "mlw2529_W"]
    for r in ("B", "W"):
        nm += [f"vlw_{b}_{r}" for b in ("2529", "3539", "4549")]
    for r in ("B", "W"):
        nm += [f"G_t{t}_{r}" for t in (1, 2, 3)]
    nm += ["G_e12", "G_e1315", "G_e16"]
    nm += ["gst_2534_O", "gst_2534_G", "gst_3555_O", "gst_3555_G", "gst_2534_B", "gst_2534_W", "gste_2534_B",
           "gste_2534_W", "vgst", "acgst"]
    for r in ("B", "W"):
        nm += [f"mov_2534_{r}", f"mov_3555_{r}", f"dsp_2534_{r}", f"dsp_3555_{r}"]
    nm += ["dsp_x", "gmv_2534_B", "gmv_2534_W", "gmv_x", "gds", "zero_B", "zero_W"]
    if "g35" in MOMSET:
        nm += ["G3555_t1_B", "G3555_t3_B", "G3555_t1_W", "G3555_t3_W"]
    return nm


MOMENT_NAMES = moment_names()


def _prank(v):
    """percentile rank in (0, 1] among finite values (ties get the mean rank)."""
    out = np.full(len(v), np.nan)
    ok = np.isfinite(v)
    order = np.argsort(v[ok], kind="stable")
    r = np.empty(ok.sum())
    r[order] = np.arange(1, ok.sum() + 1)
    vals = v[ok]
    _, inv, cnt = np.unique(vals, return_inverse=True, return_counts=True)
    sums = np.bincount(inv, weights=r)
    out[ok] = (sums / cnt)[inv] / ok.sum()
    return out


def validation(P, C):
    """Untargeted statistics of the paper, computed with the same code on the PSID and the simulated panel (Fable
    3-hour plan, Block 3, 2026-10-19): (a) mean log wage at 35-39 and 45-49 by race; (b) rank-rank slopes of the son's
    log-wage percentile (both races, within the band) on parental-income percentile, by band and race; (c) share whose
    modal job at 35-55 is G, by race and parental tercile; (d) log-wage IGE among sons below the median of parental
    income, by race, at 25-29 and 45-49; (e) the x coefficient at 25-34 and 35-55 with and without a dummy for a G job,
    by race (between/within job types)."""
    out = {}
    age, lw, bl, x, pid, G = P["age"], P["lw"], P["black"], P["x"], P["pid"], P["G"]
    for r, rv in (("B", 1), ("W", 0)):
        for lo, hi in ((35, 39), (45, 49)):
            s = (bl == rv) & (age >= lo) & (age <= hi)
            out[f"mlw_{lo}{hi}_{r}"] = float(np.nanmean(lw[s]))
    for lo, hi in ((25, 29), (30, 34), (45, 49)):
        s = (age >= lo) & (age <= hi) & np.isfinite(lw)
        rk_s, rk_p = _prank(np.where(s, lw, np.nan)), _prank(np.where(s, x, np.nan))
        for r, rv in (("B", 1), ("W", 0)):
            z = s & (bl == rv)
            out[f"rank_{lo}{hi}_{r}"] = float(_ols(rk_s[z], np.column_stack([np.ones(z.sum()), rk_p[z]]))[1])
    s = (age >= 35) & (age <= 55) & np.isfinite(G)
    ids, inv = np.unique(pid[s], return_inverse=True)
    eG = (np.bincount(inv, weights=G[s]) / np.bincount(inv)) > 0.5
    _, fi = np.unique(pid, return_index=True)
    lookup = dict(zip(pid[fi], fi))
    rr = np.array([lookup[i] for i in ids])
    xb, bb = x[rr], bl[rr]
    c1, c2 = C["terc"]
    tc = np.where(xb <= c1, 1, np.where(xb <= c2, 2, 3))
    for r, rv in (("B", 1), ("W", 0)):
        for t in (1, 3):
            z = (bb == rv) & (tc == t)
            out[f"G3555_t{t}_{r}"] = float(eG[z].mean()) if z.any() else float("nan")
    xmed = float(np.median(x[fi]))
    for r, rv in (("B", 1), ("W", 0)):
        for lo, hi in ((25, 29), (45, 49)):
            s = (bl == rv) & (age >= lo) & (age <= hi) & (x <= xmed)
            X = np.column_stack([np.ones(s.sum()), x[s], _agedum(age[s], lo, hi)])
            out[f"igebelow_{lo}{hi}_{r}"] = float(_ols(lw[s], X)[1])
    for r, rv in (("B", 1), ("W", 0)):
        for lo, hi in ((25, 34), (35, 55)):
            s = (bl == rv) & (age >= lo) & (age <= hi) & np.isfinite(G)
            base = [np.ones(s.sum()), x[s]]
            b0 = _ols(lw[s], np.column_stack(base))[1]
            b1 = _ols(lw[s], np.column_stack(base + [G[s]]))[1]
            out[f"ige_{lo}{hi}_{r}"] = float(b0)
            out[f"igewithinG_{lo}{hi}_{r}"] = float(b1)
    return out


def _pairs(P):
    """consecutive interview pairs as in the targets (1-2 years apart, from 1985, stay and disp defined), plus the job
    type at both interviews; returns masks and the previous type."""
    pid, G = P["pid"], P["G"]
    newp = np.r_[True, pid[1:] != pid[:-1]]
    prevG = np.r_[np.nan, G[:-1]]
    prevG[newp] = np.nan
    pair = ((P["gap"] >= 1) & (P["gap"] <= 2) & (P["wave"] >= 1985) & np.isfinite(P["stay"]) & np.isfinite(P["disp"])
            & np.isfinite(G) & np.isfinite(prevG))
    route = np.where(P["disp"] == 1, 2, np.where(P["stay"] == 1, 0, 1))          # 0 stay, 1 move, 2 displaced
    return pair, route, prevG, newp


def routes(P):
    """Routes into and out of G jobs (Fable 10-hour plan, Block 1, 2026-10-19), by race and band of the later
    interview (25-34, 35-55): G share by five-year band; per route (stay / move / displaced) its share of pairs, the
    inflow P(G | O before) and outflow P(O | G before), and its contribution to the change of the G share between the
    two interviews, (1 - s_r) in_r - s_r out_r weighted by the route's share (the three contributions sum to the change);
    displacement and move rates by job type at the earlier interview; and, among stayers at three consecutive interviews,
    one-way type changes (O,O,G and G,G,O) against flips (O,G,O and G,O,G)."""
    out = {}
    age, bl, G = P["age"], P["black"], P["G"]
    pair, route, prevG, newp = _pairs(P)
    for r, rv in (("B", 1), ("W", 0)):
        R = bl == rv
        for lo, hi in ((25, 29), (30, 34), (35, 39), (40, 44), (45, 49), (50, 55)):
            s = R & (age >= lo) & (age <= hi) & np.isfinite(G)
            out[f"Gshare_{lo}{hi}_{r}"] = float(G[s].mean()) if s.any() else float("nan")
        for band, (lo, hi) in (("2534", (25, 34)), ("3555", (35, 55))):
            base = pair & R & (age >= lo) & (age <= hi)
            n = base.sum()
            tot = 0.0
            for k, nm in ((0, "stay"), (1, "move"), (2, "disp")):
                z = base & (route == k)
                sh = z.sum() / n if n else float("nan")
                fromO, fromG = z & (prevG == 0), z & (prevG == 1)
                inn = float(G[fromO].mean()) if fromO.any() else 0.0
                outr = float((G[fromG] == 0).mean()) if fromG.any() else 0.0
                s_r = float(prevG[z].mean()) if z.any() else 0.0
                contrib = sh * ((1 - s_r) * inn - s_r * outr)
                tot += contrib
                out[f"share_{nm}_{band}_{r}"] = float(sh)
                out[f"in_{nm}_{band}_{r}"] = inn
                out[f"out_{nm}_{band}_{r}"] = outr
                out[f"net_{nm}_{band}_{r}"] = float(contrib)
            out[f"net_total_{band}_{r}"] = float(tot)
            out[f"dG_{band}_{r}"] = float(G[base].mean() - prevG[base].mean()) if n else float("nan")
            for jv, jn in ((0, "O"), (1, "G")):
                z = base & (prevG == jv)
                out[f"dsp_from{jn}_{band}_{r}"] = float((route[z] == 2).mean()) if z.any() else float("nan")
                out[f"mov_from{jn}_{band}_{r}"] = float((route[z] == 1).mean()) if z.any() else float("nan")
    # three consecutive stayer interviews
    st = pair & (route == 0)
    st_prev = np.r_[False, st[:-1]] & ~newp
    G2 = np.r_[np.nan, np.nan, G[:-2]]
    z = st & st_prev & np.isfinite(G2) & (age >= 35)
    for r, rv in (("B", 1), ("W", 0)):
        zz = z & (bl == rv)
        a, b, c = G2[zz], prevG[zz], G[zz]
        out[f"oneway_3555_{r}"] = float(np.mean(((a == 0) & (b == 0) & (c == 1)) | ((a == 1) & (b == 1) & (c == 0))))
        out[f"flip_3555_{r}"] = float(np.mean(((a == 0) & (b == 1) & (c == 0)) | ((a == 1) & (b == 0) & (c == 1))))
        out[f"n3_3555_{r}"] = float(zz.sum())
    return out


def levels(P):
    """The wage level by age and its change split into within-son growth and composition (Fable 10-hour plan, Block 2):
    for bands b1 -> b2, with son-level band means, m2 - m1 = (m2_both - m1_both) + (m2 - m2_both) - (m1 - m1_both),
    'both' = sons with a wage in both bands."""
    out = {}
    age, lw, bl, pid = P["age"], P["lw"], P["black"], P["pid"]
    bands = {"2529": (25, 29), "3539": (35, 39), "4549": (45, 49)}
    for r, rv in (("B", 1), ("W", 0)):
        sm = {}
        for b, (lo, hi) in bands.items():
            s = (bl == rv) & (age >= lo) & (age <= hi) & np.isfinite(lw)
            ids, inv = np.unique(pid[s], return_inverse=True)
            sm[b] = dict(zip(ids, np.bincount(inv, weights=lw[s]) / np.bincount(inv)))
            out[f"mlw_son_{b}_{r}"] = float(np.mean(list(sm[b].values())))
        for b1, b2 in (("2529", "3539"), ("3539", "4549"), ("2529", "4549")):
            both = sorted(set(sm[b1]) & set(sm[b2]))
            m1 = np.mean(list(sm[b1].values()))
            m2 = np.mean(list(sm[b2].values()))
            m1b = np.mean([sm[b1][i] for i in both])
            m2b = np.mean([sm[b2][i] for i in both])
            out[f"chg_{b1}_{b2}_{r}"] = float(m2 - m1)
            out[f"within_{b1}_{b2}_{r}"] = float(m2b - m1b)
            out[f"comp2_{b1}_{b2}_{r}"] = float(m2 - m2b)
            out[f"comp1_{b1}_{b2}_{r}"] = float(-(m1 - m1b))
            out[f"nboth_{b1}_{b2}_{r}"] = float(len(both))
            out[f"share_both_{b1}_{b2}_{r}"] = float(len(both) / len(sm[b1])) if sm[b1] else float("nan")
    return out


def son_bands(P, bands=((25, 29), (35, 39), (45, 49))):
    """son-level mean log wage in each band (NaN without a wage in the band); returns pid, x, e, black, and the means."""
    age, lw, pid = P["age"], P["lw"], P["pid"]
    ids, first = np.unique(pid, return_index=True)
    out = {"pid": ids, "x": P["x"][first], "e": P["e"][first], "black": P["black"][first]}
    for lo, hi in bands:
        s = (age >= lo) & (age <= hi) & np.isfinite(lw)
        u, inv = np.unique(pid[s], return_inverse=True)
        m = np.bincount(inv, weights=lw[s]) / np.bincount(inv)
        v = np.full(len(ids), np.nan)
        v[np.searchsorted(ids, u)] = m
        out[f"m{lo}{hi}"] = v
    return out


def longdiff(P):
    """H4 in long differences (Fable 10-hour plan, Block 5): the change of a son's own mean log wage from 25-29 to
    35-39 and to 45-49 on log parental income, by race, raw and net of years of schooling; sons with a wage in both
    bands. Same code for the PSID and the simulated panel."""
    S = son_bands(P)
    out = {}
    for r, rv in (("B", 1), ("W", 0)):
        for lab, b2 in (("10", "m3539"), ("20", "m4549")):
            d = S[b2] - S["m2529"]
            z = (S["black"] == rv) & np.isfinite(d)
            one = np.ones(z.sum())
            out[f"ld{lab}_x_{r}"] = float(_ols(d[z], np.column_stack([one, S["x"][z]]))[1])
            out[f"ld{lab}_x_net_e_{r}"] = float(_ols(d[z], np.column_stack([one, S["x"][z], S["e"][z]]))[1])
            out[f"ld{lab}_n_{r}"] = float(z.sum())
    return out


def untargeted(P):
    """Validation statistics, not targets: same-employer annual wage growth at 25-34 on log parental income by race,
    raw and net of years of schooling (PSID, output/untargeted_psid.json: White 0.019***, Black 0.007; net of
    schooling 0.006 and 0.005, racial difference 0.001). Same stayer pairs as the targets."""
    age, lw, bl, x, e, pid, gap = P["age"], P["lw"], P["black"], P["x"], P["e"], P["pid"], P["gap"]
    prev_lw = np.r_[np.nan, lw[:-1]]
    prev_lw[np.r_[True, pid[1:] != pid[:-1]]] = np.nan
    pair = (np.isfinite(lw) & np.isfinite(prev_lw) & (gap >= 1) & (gap <= 2) & (P["wave"] >= 1985)
            & np.isfinite(P["stay"]) & np.isfinite(P["disp"]))
    g = (lw - prev_lw) / gap
    st = pair & (P["stay"] == 1) & (P["disp"] == 0) & (age >= 25) & (age <= 34)
    out = {}
    for r, rv in (("B", 1), ("W", 0)):
        z = st & (bl == rv)
        one = np.ones(z.sum())
        out[f"gst_x_{r}"] = float(_ols(g[z], np.column_stack([one, x[z]]))[1])
        out[f"gst_x_net_e_{r}"] = float(_ols(g[z], np.column_stack([one, x[z], e[z]]))[1])
    return out


def _wm(v, w):
    return v.mean() if w is None else float(np.average(v, weights=w))


def _wols(y, X, w):
    if w is None:
        return _ols(y, X)
    ok = np.isfinite(y) & np.all(np.isfinite(X), axis=1) & np.isfinite(w)
    if ok.sum() < X.shape[1] + 5:
        return np.full(X.shape[1], np.nan)
    r = np.sqrt(w[ok])
    return np.linalg.lstsq(X[ok] * r[:, None], y[ok] * r, rcond=None)[0]


def _wvar(v, w):
    if w is None:
        return np.var(v)
    m = np.average(v, weights=w)
    return float(np.average((v - m) ** 2, weights=w))


def _wcov(a, b, w):
    if w is None:
        return np.cov(a, b)[0, 1]
    n = len(a)
    ma, mb = np.average(a, weights=w), np.average(b, weights=w)
    return float(np.average((a - ma) * (b - mb), weights=w) * n / (n - 1))


def moments(P, C):
    """C: constants {terc: (c1, c2)}. P: dict of arrays with pid, wave, age, lw, zero, G, gap, disp, stay, black, x, e;
    optional row weights P['w'] (attrition weights of the IPW moment set; absent = the original unweighted moments)."""
    out = {}
    age, lw, bl, x, e = P["age"], P["lw"], P["black"], P["x"], P["e"]
    W = P.get("w")
    sub = (lambda m: None) if W is None else (lambda m: W[m])
    for r, rv in (("B", 1), ("W", 0)):
        R = bl == rv
        for lo, hi in BANDS6:
            s = R & (age >= lo) & (age <= hi)
            X = np.column_stack([np.ones(s.sum()), x[s], _agedum(age[s], lo, hi)])
            out[f"ige_{lo}{hi}_{r}"] = _wols(lw[s], X, sub(s))[1]
            X = np.column_stack([np.ones(s.sum()), e[s], _agedum(age[s], lo, hi)])
            out[f"rets_{lo}{hi}_{r}"] = _wols(lw[s], X, sub(s))[1]
        s = R & (age >= 25) & (age <= 29)
        if W is None:
            out[f"mlw2529_{r}"] = np.nanmean(lw[s])
        else:
            s2 = s & np.isfinite(lw)
            out[f"mlw2529_{r}"] = _wm(lw[s2], W[s2])
        for b, (lo, hi) in (("2529", (25, 29)), ("3539", (35, 39)), ("4549", (45, 49))):
            s = R & (age >= lo) & (age <= hi) & np.isfinite(lw)
            X = np.column_stack([np.ones(s.sum()), _agedum(age[s], lo, hi)])
            res = lw[s] - X @ _wols(lw[s], X, sub(s))
            out[f"vlw_{b}_{r}"] = _wvar(res, sub(s))
    # early job type: modal G at 25-34 per son (son weight: mean of its row weights at 25-34)
    pid = P["pid"]
    s = (age >= 25) & (age <= 34) & np.isfinite(P["G"])
    ids, inv = np.unique(pid[s], return_inverse=True)
    gm = np.bincount(inv, weights=P["G"][s]) / np.bincount(inv)
    eG = (gm > 0.5).astype(float)
    ws = None if W is None else np.bincount(inv, weights=W[s]) / np.bincount(inv)
    _, fi = np.unique(pid, return_index=True)
    pid_first = pid[fi]
    lookup = dict(zip(pid_first, fi))
    rr = np.array([lookup[i] for i in ids])
    xb, eb, bb = x[rr], e[rr], bl[rr]
    c1, c2 = C["terc"]
    tc = np.where(xb <= c1, 1, np.where(xb <= c2, 2, 3))
    for r, rv in (("B", 1), ("W", 0)):
        for t in (1, 2, 3):
            z = (bb == rv) & (tc == t)
            out[f"G_t{t}_{r}"] = _wm(eG[z], None if ws is None else ws[z]) if z.any() else np.nan
    for nm_, cond in (("G_e12", eb <= 12), ("G_e1315", (eb >= 13) & (eb <= 15)), ("G_e16", eb >= 16)):
        out[nm_] = _wm(eG[cond], None if ws is None else ws[cond]) if cond.any() else np.nan
    # pairs (weight of the later interview)
    prev_lw = np.r_[np.nan, lw[:-1]]
    newp = np.r_[True, pid[1:] != pid[:-1]]
    prev_lw[newp] = np.nan
    gap = P["gap"]
    pair = (np.isfinite(lw) & np.isfinite(prev_lw) & (gap >= 1) & (gap <= 2) & (P["wave"] >= 1985)
            & np.isfinite(P["stay"]) & np.isfinite(P["disp"]))
    g = (lw - prev_lw) / gap
    st = pair & (P["stay"] == 1) & (P["disp"] == 0)
    mv = pair & (P["stay"] == 0) & (P["disp"] == 0)
    ds = pair & (P["disp"] == 1)
    a2534 = (age >= 25) & (age <= 34)
    a3555 = (age >= 35) & (age <= 55)
    for band, A in (("2534", a2534), ("3555", a3555)):
        for jn, jv in (("O", 0), ("G", 1)):
            z = st & A & (P["G"] == jv)
            out[f"gst_{band}_{jn}"] = _wm(g[z], sub(z)) if z.any() else np.nan
    for r, rv in (("B", 1), ("W", 0)):
        z = st & a2534 & (bl == rv)
        out[f"gst_2534_{r}"] = _wm(g[z], sub(z))
        out[f"gste_2534_{r}"] = _wols(g[z], np.column_stack([np.ones(z.sum()), e[z]]), sub(z))[1]
    z = st & (gap == 1)
    out["vgst"] = _wvar(g[z], sub(z))
    prev_g = np.r_[np.nan, g[:-1]]
    prev_z = np.r_[False, z[:-1]]
    zz = z & prev_z & ~newp
    out["acgst"] = _wcov(g[zz], prev_g[zz], sub(zz)) if zz.sum() > 10 else np.nan
    for r, rv in (("B", 1), ("W", 0)):
        R = bl == rv
        for band, A in (("2534", a2534), ("3555", a3555)):
            base = pair & A & R
            out[f"mov_{band}_{r}"] = _wm(mv[base].astype(float), sub(base)) if W is not None else mv[base].mean()
            out[f"dsp_{band}_{r}"] = _wm(ds[base].astype(float), sub(base)) if W is not None else ds[base].mean()
    base = pair & (age >= 25)
    out["dsp_x"] = _wols(ds[base].astype(float), np.column_stack([np.ones(base.sum()), x[base], bl[base]]), sub(base))[1]
    for r, rv in (("B", 1), ("W", 0)):
        z = mv & a2534 & (bl == rv)
        out[f"gmv_2534_{r}"] = _wm(g[z], sub(z))
    z = mv & a2534
    out["gmv_x"] = _wols(g[z], np.column_stack([np.ones(z.sum()), x[z], bl[z]]), sub(z))[1]
    out["gds"] = _wm(g[ds], sub(ds))
    for r, rv in (("B", 1), ("W", 0)):
        z = (bl == rv) & np.isfinite(P["zero"])
        out[f"zero_{r}"] = _wm(P["zero"][z], sub(z))
    if "g35" in MOMSET:                       # modal job type at 35-55 by race and parental tercile (son weights)
        s = (age >= 35) & (age <= 55) & np.isfinite(P["G"])
        ids, inv = np.unique(pid[s], return_inverse=True)
        eG3 = ((np.bincount(inv, weights=P["G"][s]) / np.bincount(inv)) > 0.5).astype(float)
        ws3 = None if W is None else np.bincount(inv, weights=W[s]) / np.bincount(inv)
        rr = np.array([lookup[i] for i in ids])
        xb3, bb3 = x[rr], bl[rr]
        tc3 = np.where(xb3 <= c1, 1, np.where(xb3 <= c2, 2, 3))
        for r, rv in (("B", 1), ("W", 0)):
            for t in (1, 3):
                z = (bb3 == rv) & (tc3 == t)
                out[f"G3555_t{t}_{r}"] = _wm(eG3[z], None if ws3 is None else ws3[z]) if z.any() else np.nan
    return np.array([out[k] for k in MOMENT_NAMES])
