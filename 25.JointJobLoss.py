r"""Joint job loss within couples: when the husband is displaced, is the second earner hit by the same shock? (2026-10-17)

Publication version of the joint job-loss result of 23.CorrelatedShocks.py (EVIDENCE rows 3.8-3.13). Race-neutral first,
race differences second. Unweighted PSID SRC + SEO, married (wife / partner present) male heads, Black and White
(head's race). S.e. clustered by 1968 family (fam68); *** p<0.01, ** p<0.05, * p<0.1.

Reads (read only): IGE/data/psid_person_year.pkl, psid_displacement.pkl (19: the husband's displacements),
correlated_shocks_fam.pkl (23: occupation codes, retrospective industry codes and the WIFE's reason-for-job-end reports,
1984-2023 waves), correlated_shocks_units.pkl (23: sectors and state unemployment of each father x stack unit),
husband_shocks_fam.pkl (18: industry codes / 16 sectors, state), the raw PSID family files (Dropbox/PSID/Family; family
hours via 9.family() and the self-employment items below). Imports functions of 1, 9, 18, 19 and 23 via importlib (no
edits). Writes (new files only)
  IGE/data/joint_job_loss_selfemp.pkl   cache: head / wife 'work for self or others' at each interview
  IGE/output/joint_job_loss.csv         every estimate
  IGE/output/joint_job_loss.md          tables + paragraph-level summary for paperA_joint_loss/sec6_why.tex
  IGE/output/joint_job_loss_es.png      event-study figure
  IGE/paperA_joint_loss/tab_joint_job_loss.tex      three LaTeX tables (window / identification / magnitudes)

DEFINITIONS
  Husband's displacement: 19's first main displacement (job ended because the company folded / moved / went out of
    business = closure, or laid off / fired = layoff) in event year ev. Father x stack units as in 19.stacks():
    baseline = latest of ev-1, ev-2 with a child 0-17 and positive hours; treated = first displacement in ev; clean
    controls = no displacement up to ev+6. Future-displacement placebo ('pseudo-treated'): men whose first displacement
    is in ev+4..ev+6, at the same baseline rules (excluded from 19's stacks).
  Wife's job ends (her own report, 23's items, 1984-2023 waves, dated 1983-2022; reports more than two years before the
    interview dropped; de-duplicated as in 19): displaced = code 1 or 3 (or 5 = coronavirus layoff 2021-23);
    employer closed = code 1; any job end = codes 1, 2, 3, 4, 7, 8 (closure, strike, layoff, quit, other / transfer,
    job completed / temporary; 5 'first job' and 6 'promotion' of the 1984-87 E branch are not job ends; 9 NA).
  Coverage: a year y can carry a report of the baseline wife only if she is the wife in the husband's family at the
    first interview after y (wave y+1, or y+2 in the biennial years). Wife-year outcomes are missing when not covered,
    for displaced and control families alike (displaced men are observed after the event by construction).
  Wife employed at baseline: positive annual hours in the baseline year (as in 23).
DESIGNS
  1. Event study (unit x relative year k = -4..+4): 1{wife's job end of a kind dated ev+k} on displaced x 1{k}, with
     father x stack fixed effects (removing any permanent difference in the wife's job stability: assortative risk)
     and calendar year x stack fixed effects; reference window k in {-4, -3} (before the pre-event rise documented
     in 23 section 2c). Event years 1987-2018 so that k = -4..+4 lies inside 1983-2022. Robustness: reference k = -4
     only (k = -3 becomes a placebo coefficient); no father x stack effect (excess rate year by year, event-year FE).
  2. Window: W = any job end in ev-1..ev+1; placebo window PL = ev-4..ev-2; DiD = W - PL (equivalent to a two-period
     design with a couple fixed effect). Event years 1987-2021, wife employed at baseline, both windows covered (one
     common sample for every column). Future-displacement placebo: pseudo-treated men enter the same regressions.
  3. Identification (outcome W, event-year FE): closures only / layoffs only; same vs different sector (16 sectors of
     8a/18); same vs different 3-digit industry (raw codes, same coding scheme: 1970 Census codes to 2001, 2000 codes
     2003-15, 2010 codes 2017-23); same 1-digit (major) occupation group (8 harmonised groups of 23); change in the
     state unemployment rate in ev (LAUS, per s.d. among displaced); both spouses' pre-trends (husband's hours and
     labor income at ev-2, or ev-3 in biennial years, and their change over the two years before; the wife's hours
     likewise; the wife's PL);
     excluding couples in which either spouse was self-employed (work for self, or self and others) at an interview
     in ev-3..ev. Husband's industry / occupation: latest interview in [ev-3, ev]; wife's: latest in [ev-6, ev].
  4. Magnitudes (couple-years): consecutive interviews of the same couple, both spouses with positive hours in the
     earlier year; h = husband displaced in the interval since that year, w = wife displaced in the same interval
     (1 year to 1996, 2 years in the biennial survey); also w within one year either side of the interval. P(w | h),
     P(w | not h), phi coefficient and tetrachoric correlation (s.e. from 200 bootstrap draws of 1968 families).
  5. Family income: share of the family income loss attributable to the wife's joint job loss (accounting, as in 23
     section 4a): (P1 - P0) x cost, where P1 / P0 = share of displaced / control families whose baseline wife was
     displaced in ev-1..ev+1 (0 if she did not work at baseline) and cost = the change in family income (wife's labor
     income) at e = +1..+3 that comes with her displacement among control families (19's stacked design, bins, e = -2
     reference); also with the DiD excess probability of design 2 in place of P1 - P0.
Nothing here randomises the husband's job loss; closures, the future-displacement placebo, the couple fixed effect and
pre-trend controls address assortative risk and selection into layoffs, not every confounder (e.g. a common local shock
is part of the mechanism, not a confounder; the same respondent usually reports both spouses' job ends).
"""
import importlib.util
import re
import sys
import warnings

import numpy as np
import pandas as pd
from scipy import stats
from scipy.integrate import quad
from scipy.optimize import brentq

from common import DATA, OUT, HERE, stars

warnings.simplefilter("ignore", FutureWarning)
warnings.simplefilter("ignore", RuntimeWarning)
PAPER = HERE / "paperA_joint_loss"


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


P23 = _load("p23", "23.CorrelatedShocks.py")
P19, P18 = P23.P19, P23.P18
psid1, psid9 = P19.psid1, P19.psid9
WAVES = psid1.WAVES
ROWS = []
KS = list(range(-4, 5))
KALL = list(range(-6, 5))


def pv(b, se):
    return 2 * stats.norm.sf(abs(b / se)) if se > 0 else np.nan


def cell(b, se, p=None):
    if not (se > 0):
        return "n.a."
    p = pv(b, se) if p is None else p
    return f"{b:.3f}{stars(p)} ({se:.3f}; p={'<0.001' if p < 0.001 else f'{p:.3f}'})"


def big(b, se, p=None):
    p = pv(b, se) if p is None else p
    return f"{b:,.0f}{stars(p)} ({se:,.0f}; p={'<0.001' if p < 0.001 else f'{p:.3f}'})"


md_table, ols_cl = P19.md_table, P23.ols_cl


def rec(table, sample, outcome, term, b, se, p=None, **kw):
    if p is None:
        p = pv(b, se) if (se is not None and se == se and se > 0) else np.nan
    ROWS.append(dict(table=table, sample=sample, outcome=outcome, term=term, coef=b, se=se, p=p, **kw))


# ---------------------------------------------------------------- self-employment items
SE_PAT = {"h_se": [r"^(B4|C2|C4) W.*SELF.*\(HD-E\)", r"^WORK FOR SELF/OTR\?\(E\) D5", r"^D5 WORK FOR SELF/OTR \(E\)",
                   r"^WRK SOMEONEELSE/SELF\s+D5", r"^BC22 WORK SELF/OTR\?--JOB 1"],
          "w_se": [r"^(D4|F3|F5|J4) W.*SELF.*\(WF-E\)", r"^WRK FOR SELF OR\?\(E\)-WFD5", r"^DE22 WORK SELF/OTR\?--JOB 1"]}


def selfemp():
    """wave x int: head's / wife's 'work for someone else (1), both (2), self only (3)' for the current main job."""
    fn = DATA / "joint_job_loss_selfemp.pkl"
    if fn.exists():
        return pd.read_pickle(fn)
    out, found = [], []
    for w in [w for w in WAVES if w >= 1976]:
        folder = psid1.FAM / (f"fam{w}" if w < 1994 else f"fam{w}er")
        do = next(f for f in folder.glob("*.do") if "formats" not in f.name)
        pos, labs = P18.layout(do)
        labs = [(v, l) for v, l in labs if v in pos]
        idv = labs[1][0]
        sel = {k: P23.find(labs, p) for k, p in SE_PAT.items()}
        f = P18.read(do.with_suffix(".txt"), sorted({idv, *[v[0] for v in sel.values() if v]}), pos)
        x = pd.DataFrame({"wave": w, "int": f[idv]})
        for k, v in sel.items():
            x[k] = f[v[0]] if v else np.nan
        out.append(x)
        found.append(dict(wave=w, **{k: (f"{v[0]} '{v[1]}'" if v else "") for k, v in sel.items()},
                          **{f"{k}_codes": (x[k].value_counts().sort_index().to_dict() if sel[k] else {})
                             for k in sel}))
    res = dict(X=pd.concat(out, ignore_index=True), found=pd.DataFrame(found))
    pd.to_pickle(res, fn)
    return res


# ---------------------------------------------------------------- wife's job ends
KINDS = ("main", "strict", "any", "quit")
KLAB = {"main": "Wife displaced", "strict": "Wife's employer closed", "any": "Wife's job ended (any reason)",
        "quit": "Wife quit"}


def wife_events(py, R):
    wf = py[py["wife"]][["wave", "int", "pid"]].drop_duplicates(["wave", "int"])
    r = R.merge(wf, on=["wave", "int"], how="inner")
    r = r[r["year"].between(r["wave"] - 2, r["wave"])].copy()
    r["code"] = r["code"].astype(int)
    r["year"] = r["year"].astype(int)
    cov = (r["code"] == 5) & (r["wave"] >= 2021)
    flag = {"main": r["code"].isin([1, 3]) | cov, "strict": r["code"] == 1, "quit": r["code"] == 4,
            "any": r["code"].isin([1, 2, 3, 4, 7, 8]) | cov}
    out = {}
    for k, f in flag.items():
        x = r[f].sort_values(["pid", "year", "dated"], ascending=[True, True, False]).drop_duplicates(["pid", "year"])
        prev = set(zip(x["pid"], x["year"] + 1))
        drop = (~x["dated"]) & pd.Series([(p, y) in prev for p, y in zip(x["pid"], x["year"])], index=x.index)
        x = x[~drop]
        out[k] = set(zip(x["pid"].astype(np.int64), x["year"].astype(int)))
    return out


def cover_wave(y):
    """first interview that carries reports of job ends in calendar year y (NaN outside 1983-2022)."""
    if y < 1983 or y > 2022:
        return None
    return y + 1 if (y + 1) in WAVES else y + 2


# ---------------------------------------------------------------- units (father x stack) incl. future placebo
def build_units(m, d, kids=True):
    first = {k: d[d[k] == 1].groupby("pid")["year"].min() for k in ("main",)}
    fm = m["pid"].map(first["main"]).fillna(9999)
    b = pd.concat([m.assign(ev=m["year"] + 1, pri=0), m.assign(ev=m["year"] + 2, pri=1)])
    b["fm"] = pd.concat([fm, fm]).to_numpy()
    b = b.sort_values(["pid", "ev", "pri"]).drop_duplicates(["pid", "ev"]).reset_index(drop=True)
    b = b[(b["hh"] > 0) & b["ev"].between(1968, 2022) & ((b["nkid"] > 0) if kids else True)]
    tr = b["fm"] == b["ev"]
    ps = b["fm"].between(b["ev"] + 4, b["ev"] + 6)
    ct = b["fm"] > b["ev"] + 6
    b = b[tr | ps | ct].copy()
    b["treat"] = tr[tr | ps | ct].astype(int)
    b["pseudo"] = ps[tr | ps | ct].astype(int)
    st = d[(d["main"] == 1)][["pid", "year", "strict"]].rename(columns={"year": "ev", "strict": "his_closure"})
    b = b.merge(st, on=["pid", "ev"], how="left")
    b["closure"] = ((b["his_closure"] == 1) & (b["treat"] == 1)).astype(int)
    b["layoff"] = ((b["his_closure"] != 1) & (b["treat"] == 1)).astype(int)
    U = b[["pid", "fam68", "ev", "treat", "pseudo", "closure", "layoff", "fm", "hrace", "youngest", "w_pid", "wh",
           "hh", "hlab", "age", "nkid"]].rename(columns={"w_pid": "w0", "wh": "wh0", "youngest": "young0",
                                                          "hh": "hh0", "hlab": "hlab0", "age": "age0"})
    U["black"] = (U["hrace"] == "Black").astype(int)
    U["wemp0"] = (U["wh0"] > 0).astype(float).where(U["w0"].notna() & U["wh0"].notna())
    U["unit"] = np.arange(len(U))
    return U.reset_index(drop=True)


def add_wife_outcomes(U, m, ev_sets):
    S = set(zip(m.loc[m["w_pid"].notna(), "pid"].astype(np.int64), m.loc[m["w_pid"].notna(), "wave"].astype(int),
                m.loc[m["w_pid"].notna(), "w_pid"].astype(np.int64)))
    pid = U["pid"].astype(np.int64).to_numpy()
    w0 = U["w0"].fillna(-1).astype(np.int64).to_numpy()
    ev = U["ev"].astype(int).to_numpy()
    for k in KALL:
        cov = np.array([(cw := cover_wave(e + k)) is not None and (p, cw, w) in S for p, e, w in zip(pid, ev, w0)])
        U[f"cov{k}"] = cov.astype(float)
        for kind in KINDS:
            s = ev_sets[kind]
            U[f"{kind}{k}"] = np.where(cov, [float((w, e + k) in s) for w, e in zip(w0, ev)], np.nan)
    for kind in KINDS:
        U[f"{kind}_W"] = U[[f"{kind}{k}" for k in (-1, 0, 1)]].max(axis=1, skipna=False)
        U[f"{kind}_PL"] = U[[f"{kind}{k}" for k in (-4, -3, -2)]].max(axis=1, skipna=False)
        U[f"{kind}_D"] = U[f"{kind}_W"] - U[f"{kind}_PL"]
    return U


def add_pretrends(U, m):
    """pre-event level (ev-2, else ev-3) and change from two years earlier (ev-4, else ev-5), so that the biennial
    years (odd calendar years observed) are covered; wife's hours only while she is the baseline wife."""
    mi = m.drop_duplicates(["pid", "year"]).set_index(["pid", "year"])
    for k in (2, 3, 4, 5):
        for c in ("hh", "hlab", "wh", "w_pid"):
            U[f"{c}_{k}"] = P19.lookup(mi[c], U["pid"], U["ev"] - k)
        U[f"wh_{k}"] = U[f"wh_{k}"].where(U[f"w_pid_{k}"] == U["w0"])
    for c in ("hh", "hlab", "wh"):
        lev = U[f"{c}_2"].fillna(U[f"{c}_3"])
        ear = U[f"{c}_4"].where(U[f"{c}_2"].notna(), U[f"{c}_5"])
        sc = 1000 if c == "hlab" else 100
        U[f"x_{c}_lev"] = lev / sc
        U[f"x_{c}_chg"] = (lev - ear) / sc
    HV, WV = ["x_hh_lev", "x_hh_chg", "x_hlab_lev", "x_hlab_chg"], ["x_wh_lev", "x_wh_chg"]
    U["x_h_miss"] = U[HV].isna().any(axis=1).astype(float)
    U["x_w_miss"] = U[WV].isna().any(axis=1).astype(float)
    for c in HV:
        U[c] = U[c].where(U["x_h_miss"] == 0, 0)
    for c in WV:
        U[c] = U[c].where(U["x_w_miss"] == 0, 0)
    return U, HV + WV + ["x_h_miss", "x_w_miss"]


def usable(q, cols):
    """drop controls without variation in the sample (avoids a rank-deficient design)."""
    keep = [c for c in cols if q[c].nunique() > 1]
    return list(q[keep].T.drop_duplicates().index)


def latest_code(keys, src, lo):
    """keys: unit, pid, ev; src: pid, wave, code -> (code, wave) at the latest wave in [ev - lo, ev]."""
    x = keys.merge(src, on="pid")
    x = x[(x["wave"] >= x["ev"] - lo) & (x["wave"] <= x["ev"])].sort_values(["unit", "wave"])
    g = x.groupby("unit").last()
    return g["code"], g["wave"]


def era(w):
    return np.where(w <= 2001, 0, np.where(w <= 2015, 1, 2))


def add_matches(U, C, SE, m):
    """same 3-digit industry, same occupation group, self-employment; sectors / state UR from 23's units."""
    kh = U[["unit", "pid", "ev"]]
    kw = U[U["w0"].notna()][["unit", "w0", "ev"]].rename(columns={"w0": "pid"})
    kw["pid"] = kw["pid"].astype(np.int64)
    for v, who, lo in (("icode", "h", 3), ("ogrp", "h", 3), ("icode", "w", 6), ("ogrp", "w", 6)):
        idc = "pid" if who == "h" else "w_pid"
        src = C[[idc, "wave", f"{who}_{v}"]].dropna().rename(columns={idc: "pid", f"{who}_{v}": "code"})
        src = src.drop_duplicates(["pid", "wave"])
        c, w = latest_code(kh if who == "h" else kw, src, lo)
        U[f"{who}_{v}"] = U["unit"].map(c)
        U[f"{who}_{v}_w"] = U["unit"].map(w)
    ok = U["h_icode"].notna() & U["w_icode"].notna()
    same_era = era(U["h_icode_w"].fillna(0)) == era(U["w_icode_w"].fillna(0))
    U["same_ind3"] = (U["h_icode"] == U["w_icode"]).astype(float).where(ok & same_era)
    U["same_occ"] = (U["h_ogrp"] == U["w_ogrp"]).astype(float).where(U["h_ogrp"].notna() & U["w_ogrp"].notna())
    # self-employment at an interview in [ev-3, ev]
    X = SE["X"]
    hd = m[["pid", "wave", "int", "w_pid"]].drop_duplicates(["wave", "int"]).merge(X, on=["wave", "int"], how="left")
    hd["h_self"] = hd["h_se"].isin([2, 3]).astype(float)
    hd["w_self"] = hd["w_se"].isin([2, 3]).astype(float)
    x = U[["unit", "pid", "ev", "w0"]].merge(hd[["pid", "wave", "w_pid", "h_self", "w_self"]], on="pid")
    x = x[(x["wave"] >= x["ev"] - 3) & (x["wave"] <= x["ev"])]
    x["w_self"] = x["w_self"].where(x["w_pid"] == x["w0"], 0)
    g = x.groupby("unit")[["h_self", "w_self"]].max()
    U["any_self"] = U["unit"].map(g.max(axis=1)).fillna(0)
    U["h_self"] = U["unit"].map(g["h_self"]).fillna(0)
    return U


# ---------------------------------------------------------------- event study (unit x k)
def event_study(U, kind, ref=(-4, -3), unit_fe=True):
    q = U[U["ev"].between(1987, 2018) & (U["wemp0"] == 1) & (U["pseudo"] == 0)]
    L = []
    for k in KS:
        L.append(pd.DataFrame({"unit": q["unit"].to_numpy(), "fam68": q["fam68"].to_numpy(), "ev": q["ev"].to_numpy(),
                               "treat": q["treat"].to_numpy(), "k": k, "y": q[f"{kind}{k}"].to_numpy()}))
    L = pd.concat(L, ignore_index=True).dropna(subset=["y"])
    L["cell"] = L["ev"] * 100 + L["k"] + 50
    xs = []
    for k in KS:
        if k in ref:
            continue
        L[f"d{k}"] = ((L["k"] == k) & (L["treat"] == 1)).astype(float)
        xs.append(f"d{k}")
    if not unit_fe:
        raise ValueError
    b, V, info = P19.twfe(L, "y", xs)
    out = {}
    for i, x in enumerate(xs):
        out[int(x[1:])] = (b[i], np.sqrt(V[i, i]))
    for k in ref:
        out[k] = (0.0, 0.0)
    # window (k = -1..+1) minus the reference window, and the placebo window k = -2 (if estimated)
    w = np.array([1 / 3 if int(x[1:]) in (-1, 0, 1) else 0 for x in xs])
    out["win"] = (w @ b, np.sqrt(w @ V @ w))
    for nm, ks in (("sum11", (-1, 0, 1)), ("sum21", (-2, -1, 0, 1))):
        w = np.array([1.0 if int(x[1:]) in ks else 0 for x in xs])
        out[nm] = (w @ b, np.sqrt(w @ V @ w))
    info["ref_rate_treated"] = L.loc[(L["treat"] == 1) & L["k"].isin(ref), "y"].mean()
    info["ref_rate_controls"] = L.loc[(L["treat"] == 0) & L["k"].isin(ref), "y"].mean()
    return out, info


def by_year_excess(U, kind):
    q = U[U["ev"].between(1987, 2018) & (U["wemp0"] == 1) & (U["pseudo"] == 0)]
    out = {}
    for k in KS:
        est, inf = ols_cl(q, f"{kind}{k}", ["treat"], fe=["ev"])
        out[k] = est["treat"] + (inf["n"], q.loc[q["treat"] == 1, f"{kind}{k}"].mean(),
                                 q.loc[q["treat"] == 0, f"{kind}{k}"].mean())
    return out


# ---------------------------------------------------------------- magnitudes (couple-years)
def bvn(a, b, r):
    s = np.sqrt(1 - r * r)
    return quad(lambda x: stats.norm.pdf(x) * stats.norm.cdf((b - r * x) / s), -np.inf, a, epsabs=1e-12)[0]


def tetra(n11, n10, n01, n00):
    N = n11 + n10 + n01 + n00
    ph, pw, p11 = (n11 + n10) / N, (n11 + n01) / N, n11 / N
    if n11 == 0 or min(ph, pw) <= 0:
        return np.nan
    a, b = stats.norm.ppf(ph), stats.norm.ppf(pw)
    f = lambda r: bvn(a, b, r) - p11
    try:
        return brentq(f, -0.95, 0.99, xtol=1e-6)
    except ValueError:
        return np.nan


def phi(n11, n10, n01, n00):
    num = n11 * n00 - n10 * n01
    den = np.sqrt((n11 + n10) * (n01 + n00) * (n11 + n01) * (n10 + n00))
    return num / den if den > 0 else np.nan


def joint_stats(g, h="h", w="w", reps=200, seed=25):
    g = g.dropna(subset=[h, w])
    t = g.assign(n11=(g[h] == 1) & (g[w] == 1), n10=(g[h] == 1) & (g[w] == 0), n01=(g[h] == 0) & (g[w] == 1),
                 n00=(g[h] == 0) & (g[w] == 0)).groupby("fam68")[["n11", "n10", "n01", "n00"]].sum()
    n = t.sum().to_numpy(float)
    est, inf = ols_cl(g, w, [h])
    o = dict(N=len(g), clusters=len(t), Ph=(n[0] + n[1]) / n.sum(), Pw=(n[0] + n[2]) / n.sum(), P11=n[0] / n.sum(),
             Pw_h=n[0] / (n[0] + n[1]) if n[0] + n[1] > 0 else np.nan, Pw_noh=n[2] / (n[2] + n[3]),
             n_h=int(n[0] + n[1]), diff=est[h], phi=phi(*n), tet=tetra(*n))
    o["ratio"] = o["Pw_h"] / o["Pw_noh"]
    rng = np.random.default_rng(seed)
    T = t.to_numpy(float)
    bp, bt, br = [], [], []
    for _ in range(reps):
        s = T[rng.integers(0, len(T), len(T))].sum(axis=0)
        bp.append(phi(*s))
        bt.append(tetra(*s))
        br.append((s[0] / (s[0] + s[1])) / (s[2] / (s[2] + s[3])) if s[0] + s[1] > 0 else np.nan)
    o["phi_se"], o["tet_se"], o["ratio_se"] = np.nanstd(bp), np.nanstd(bt), np.nanstd(br)
    return o


def couple_years(m, d, ev_sets, C):
    x = m[m["w_pid"].notna()].drop_duplicates(["pid", "year"]).sort_values(["pid", "year"]).copy()
    g = x.groupby("pid")
    x["py"], x["pw"], x["phh"], x["pwh"] = g["year"].shift(1), g["w_pid"].shift(1), g["hh"].shift(1), g["wh"].shift(1)
    x["pwave"] = g["wave"].shift(1)
    x["ny"], x["nw"] = g["year"].shift(-1), g["w_pid"].shift(-1)
    x = x[(x["year"] - x["py"] <= 2) & (x["pw"] == x["w_pid"]) & (x["phh"] > 0) & (x["pwh"] > 0) &
          (x["py"] >= 1983) & (x["year"] <= 2022)].copy()
    hs = set(zip(d.loc[d["main"] == 1, "pid"].astype(np.int64), d.loc[d["main"] == 1, "year"].astype(int)))
    ws = ev_sets["main"]
    pid, wp = x["pid"].astype(np.int64).to_numpy(), x["w_pid"].astype(np.int64).to_numpy()
    yr, py_ = x["year"].astype(int).to_numpy(), x["py"].astype(int).to_numpy()
    x["h"] = [float(any((p, y) in hs for y in range(a + 1, t + 1))) for p, a, t in zip(pid, py_, yr)]
    x["w"] = [float(any((p, y) in ws for y in range(a + 1, t + 1))) for p, a, t in zip(wp, py_, yr)]
    nxt_ok = ((x["ny"] - x["year"]) <= 2) & (x["nw"] == x["w_pid"]) & (x["year"] + 1 <= 2022)
    x["w_pm1"] = np.where(nxt_ok, [float(any((p, y) in ws for y in range(a, t + 2))) for p, a, t in zip(wp, py_, yr)],
                          np.nan)
    x["annual"] = ((x["year"] - x["py"]) == 1) & (x["year"] <= 1996)
    x["pwave"] = x["pwave"].astype(int)
    ss = C[["wave", "int", "s_sec"]].drop_duplicates(["wave", "int"])
    x = x.merge(m[["pid", "wave", "int"]].rename(columns={"wave": "pwave", "int": "pint"}).drop_duplicates(
        ["pid", "pwave"]), on=["pid", "pwave"], how="left")
    x = x.merge(ss.rename(columns={"wave": "pwave", "int": "pint"}), on=["pwave", "pint"], how="left")
    x["kid"] = np.where(x["youngest"].isna(), "none", np.where(x["youngest"] <= 5, "0-5", "6-17"))
    x["black"] = (x["hrace"] == "Black").astype(int)
    return x



LIT = """## 7. Literature check (2026-10-17): is joint job loss within couples documented?

Every entry was checked on the linked source page in this session; "(PDF read)" = the full text was searched.

Already documented
- Spouses' labor market outcomes are positively correlated, mostly through permanent components: Hyslop (2001), "Rising
  U.S. Earnings Inequality and Family Labor Supply: The Covariance Structure of Intrafamily Earnings", AER 91(4): 755-777
  (PSID; abstract: working couples' positively correlated outcomes are "almost entirely attributable to permanent
  factors"). https://ideas.repec.org/a/aea/aecrev/v91y2001i4p755-777.html
- The correlation moves with the cycle: Shore (2010), "For Better, For Worse: Intrahousehold Risk-Sharing over the
  Business Cycle", REStat 92(3): 536-548 (spouses' incomes more positively correlated in booms, so household risk is not
  countercyclical). https://ideas.repec.org/a/tpr/restat/v92y2010i3p536-548.html
- Spouses sort on employer, industry and occupation, and sorted couples' earnings changes are more correlated: Hyatt,
  "Co-Working Couples and the Similar Jobs of Dual-Earner Households" (Census CES WP 15-23R; Monthly Labor Review 2019):
  10-12% of dual-earner couples work at the same establishment, 11-13% for the same firm (Census 2000 linked to LEHD);
  layoffs "at similar times" and the insurance value of marriage are mentioned only in passing.
  https://www.bls.gov/opub/mlr/2019/article/coworking-couples-and-the-similar-jobs-of-dual-earner-households.htm ;
  Busch, Madera (with Groes), "Assortative Mating and Joint Income Dynamics of Couples" (Danish tax registers; sorting on
  education, occupation, industry and firm; much stronger correlation of earnings changes in sorted couples; no
  displacement events on the project page). https://bse.eu/research/assortative-mating-and-joint-income-dynamics-couples
- Displacement studies know that both spouses are sometimes displaced together and drop those couples:
  Halla, Schmieder and Weber (2020), "Job Displacement, Family Dynamics, and Spousal Labor Supply", AEJ: Applied 12(4)
  (Austrian registers; couples displaced by the same firm event = 3.47% of plant-closure and 1.13% of mass-layoff
  households, dropped; only 8% of dual-earner couples share a 4-digit industry; correlated local shocks discussed as an
  explanation of the small response) (PDF read, IZA DP 11752) https://docs.iza.org/dp11752.pdf ,
  https://www.aeaweb.org/doi/10.1257/app.20180671 ;
  Marcus (2013), "The effect of unemployment on the mental health of spouses - Evidence from plant closures in Germany",
  J. Health Econ. 32(3): 546-558 (SOEP; "the plant closure experience of one spouse is likely to be correlated with a
  plant closure experience of the other spouse since spouses might work in the same plant"; excluding them cuts the
  treatment group by 7%) (PDF read, HEDG WP 12/17) https://ideas.repec.org/a/eee/jhecon/v32y2013i3p546-558.html ,
  https://www.york.ac.uk/media/economics/documents/herc/wp/12_17.pdf ;
  Banzhaf (2013), "When It Rains, It Pours: Under What Circumstances Does Job Loss Lead to Divorce", Census CES WP 13-62
  (SIPP 2001-2008 panels; couples with both spouses displaced are about 5% of couples with any displacement, dropped)
  (PDF read) https://www2.census.gov/ces/wp/2013/CES-WP-13-62.pdf
- Closest finding: Kawano, LaLumia, Ramnath and Stevens (2025), "Who picks up the slack? Understanding spousal responses
  to unemployment spells", Labour Economics 96 (a large panel of US married households; the small added-worker response
  is explained by the non-displaced spouse being more likely to leave employment, "either through correlated
  unemployment shocks or retirement"). https://ideas.repec.org/a/eee/labeco/v96y2025ics0927537125000569.html
  (data source not stated on the pages checked; the SSRN and journal pages refused access).
- Added-worker benchmarks: Stephens (2002), JOLE 20(3) (PSID; wife's labor supply before and after the husband's
  displacement; the abstract does not mention the wife's own job loss) https://www.nber.org/papers/w8260 ; Pruitt and
  Turner (2020), "Earnings Risk in the Household: Evidence from Millions of US Tax Returns", AER: Insights 2(2): 237-254
  (spousal income lowers household earnings risk; no job-loss co-occurrence in the abstract)
  https://ideas.repec.org/a/aea/aerins/v2y2020i2p237-54.html ; Cullen and Gruber (2000), Blundell, Pistaferri and
  Saporta-Eksten (2016): see proposals/insurance_literature_check.md.

What is new here (not found in any of the above)
1. An event-study estimate, in US data and with each spouse's own stated reason for the job end, of how much the wife's
   displacement risk rises around the husband's displacement (it more than doubles), year by year, with couple fixed
   effects, a placebo window and a future-displacement placebo that rules out permanent assortative risk.
2. The channels: when he loses his job to a plant closure her employer is more likely to close; the excess is
   concentrated in same-sector and same-3-digit-industry couples; it does not vary with state unemployment.
3. The comparison by race (present in both races; at least as large for Black couples; the difference is not robust).
4. The joint probability and the tetrachoric correlation of job-loss events within couples as targets for a household
   model, by sector match, child age and race.
5. Its quantitative role for family income after the husband's displacement (small on average) and its place in a paper
   on parental insurance, children and the IGE.
What is not new: that spouses' earnings are correlated, that they sort on employer and industry, that joint
displacements by the same plant event exist (and are routinely dropped), and that correlated unemployment can mute the
added-worker effect (Kawano et al. 2025 for the US; Halla et al. 2020 discuss it). Our result should be framed as
measuring and decomposing a mechanism those papers name or exclude, not as discovering it. A rough comparison: Halla et
al.'s 3.47% of Austrian closure households (about half of whose wives work) is of the same order as our excess of about
5-8 points among wives working at baseline.
"""


# ---------------------------------------------------------------- LaTeX helpers (20's style)
def star(p):
    return "^{***}" if p < 0.01 else "^{**}" if p < 0.05 else "^{*}" if p < 0.1 else ""


def tcell(b, se, digits=3):
    if b is None or not np.isfinite(b) or not (se > 0):
        return "", ""
    f = f"{{:,.{digits}f}}"
    return f"${f.format(b)}{star(pv(b, se))}$", f"({f.format(se)})"


def trows(label, cells):
    return [f"{label} & " + " & ".join(c[0] for c in cells) + r" \\",
            " & " + " & ".join(c[1] for c in cells) + r" \\"]


def thdr(i, lines):
    return r"\begin{tabular}[b]{@{}c@{}}(" + str(i) + ") " + r"\\".join(lines) + r"\end{tabular}"


def ttable(caption, label, head, body, note, cols):
    return "\n".join([r"\begin{table}[htbp]\centering\small", rf"\caption{{{caption}}}\label{{{label}}}",
                      r"\resizebox{\textwidth}{!}{%", r"\begin{tabular}{l" + "c" * cols + "}", r"\toprule", *head,
                      r"\midrule", *body, r"\bottomrule", r"\end{tabular}}",
                      r"\begin{minipage}{0.95\textwidth}\footnotesize " + note + r"\end{minipage}",
                      r"\end{table}", ""])


def es_figure(ES):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    col = {"All": "#3d3c39", "Black": "#2a78d6", "White": "#eb6834"}
    mk = {"All": "D", "Black": "o", "White": "s"}
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.4), sharey=False)
    for ax, kind in zip(axes, ("main", "any", "strict")):
        for j, race in enumerate(("All", "Black", "White")):
            o = ES[(race, kind)]
            e = np.array(KS)
            b = np.array([o[k][0] for k in KS])
            s = np.array([o[k][1] for k in KS])
            sh = (j - 1) * 0.14
            ax.errorbar(e + sh, b, yerr=1.96 * s, color=col[race], marker=mk[race], markersize=5, linewidth=1.8,
                        elinewidth=1.0, capsize=0, label=race)
        ax.axhline(0, color="#52514e", linewidth=0.8)
        ax.axvspan(-4.4, -2.6, color="#e6e5e0", alpha=0.6, linewidth=0)
        ax.axvline(-0.5, color="#b0afa8", linewidth=0.8, linestyle=":")
        ax.set_title(KLAB[kind], fontsize=11, color="#0b0b0b")
        ax.set_xticks(KS)
        ax.tick_params(labelsize=8, colors="#52514e")
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        ax.grid(axis="y", color="#e6e5e0", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=9, loc="upper left")
    axes[0].set_ylabel("Change in annual probability (vs. years -4, -3)", fontsize=9, color="#52514e")
    fig.supxlabel("Years since the husband's displacement (shaded = reference years -4, -3)", fontsize=10)
    fig.suptitle("The wife's own job loss around her husband's displacement (couple and calendar-year fixed effects, "
                 "95% CI)", fontsize=12)
    fig.tight_layout()
    fig.savefig(OUT / "joint_job_loss_es.png", dpi=150, facecolor="#fcfcfb")
    plt.close(fig)


# ---------------------------------------------------------------- main
def main():
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    E = P23.extras()
    X, R = E["X"], E["R"]
    F18 = pd.read_pickle(DATA / "husband_shocks_fam.pkl")
    fam = psid9.family()
    d = pd.read_pickle(DATA / "psid_displacement.pkl")
    SE = selfemp()
    ev_sets = wife_events(py, R)
    C = P23.couples(py, X, F18, fam)
    both = (C["hh"] > 0) & (C["wh"] > 0)
    C["s_sec"] = (C["h_sec"] == C["w_sec"]).astype(float).where(both & C["h_sec"].notna() & C["w_sec"].notna())
    m = P19.men_panel(py, fam)
    wl = py[py["head"]][["wave", "int", "wlab"]].drop_duplicates(["wave", "int"])
    m = m.merge(wl, on=["wave", "int"], how="left").drop_duplicates(["pid", "year"])
    U = build_units(m, d)
    U = add_wife_outcomes(U, m, ev_sets)
    U, PRE = add_pretrends(U, m)
    U = add_matches(U, C, SE, m)
    U23 = pd.read_pickle(DATA / "correlated_shocks_units.pkl")[["pid", "ev", "same_sec", "h_sec", "w_sec", "d_ur",
                                                                  "ur", "J_disp", "observed"]]
    U = U.merge(U23, on=["pid", "ev"], how="left")
    print("units", len(U), "treated", int(U["treat"].sum()), "pseudo", int(U["pseudo"].sum()), flush=True)
    if len(sys.argv) > 1 and sys.argv[1] == "dump":          # debugging only: python 25.JointJobLoss.py dump <file>
        U.to_pickle(sys.argv[2])
        return

    md = ["# Joint job loss within couples", "",
          "Built by `25.JointJobLoss.py` (2026-10-17; definitions and designs in its docstring). Unweighted PSID SRC + "
          "SEO, married male heads with a child 0-17 at baseline, Black and White (head's race). Husband's "
          "displacement = 19's first closure / layoff; the wife's job ends are her own reason-for-job-end reports "
          "(23's items, 1984-2023 waves). S.e. clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1. Every cell: "
          "coefficient*** (s.e.; p).", ""]
    found = SE["found"]
    md += ["## 0. Data checks", "",
           "Self-employment items found by label (head / wife, current main job; 1 someone else, 2 both, 3 self "
           "only), used only for the exclusion check in section 3:", "",
           "| Wave | Head item | Wife item |", "|---|---|---|"]
    for _, r in found.iterrows():
        md.append(f"| {r['wave']} | {r['h_se']} | {r['w_se']} |")
    nrep = {k: len(v) for k, v in ev_sets.items()}
    md += ["", "Wife-years with a job end of each kind (de-duplicated): " +
           ", ".join(f"{KLAB[k]} {v:,}" for k, v in nrep.items()) + ".", ""]

    # replication of 23's window estimate (its sample: ev 1984-2021, observed, wife employed) with this code
    rp = U[(U["pseudo"] == 0) & (U["wemp0"] == 1) & U["ev"].between(1984, 2021) & (U["observed"] == 1)]
    est, inf = ols_cl(rp, "J_disp", ["treat"], fe=["ev"])
    est2, inf2 = ols_cl(rp.dropna(subset=["main_W"]), "main_W", ["treat"], fe=["ev"])
    md += [f"Check against 23 (its window variable, its sample): husband displaced {cell(*est['treat'])}, N {inf['n']:,}; "
           f"with this script's coverage rule (all three years covered): {cell(*est2['treat'])}, N {inf2['n']:,}.", ""]
    rec("check_23", "All", "J_disp (23)", "treat", *est["treat"], n=inf["n"])
    rec("check_23", "All", "main_W (25 coverage)", "treat", *est2["treat"], n=inf2["n"])

    # ============================================================ 1. event study
    RACES = [("All", lambda q: q), ("Black", lambda q: q[q["hrace"] == "Black"]),
             ("White", lambda q: q[q["hrace"] == "White"])]
    ES, ESI, ES4, BY = {}, {}, {}, {}
    for race, f in RACES:
        for kind in ("main", "any", "strict", "quit"):
            ES[(race, kind)], ESI[(race, kind)] = event_study(f(U), kind)
            ES4[(race, kind)], _ = event_study(f(U), kind, ref=(-4,))
            BY[(race, kind)] = by_year_excess(f(U), kind)
            inf = ESI[(race, kind)]
            for k in KS + ["win", "sum11", "sum21"]:
                rec("event_study_ref_-4_-3", race, kind, f"k={k}" if isinstance(k, int) else k,
                    *ES[(race, kind)][k], n=inf["n"], treated=inf["units"], controls=inf["controls"],
                    clusters=inf["clusters"])
                rec("event_study_ref_-4", race, kind, f"k={k}" if isinstance(k, int) else k,
                    *ES4[(race, kind)][k], n=inf["n"])
            for k in KS:
                b, se, p, n, mt, mc = BY[(race, kind)][k]
                rec("by_year_excess_evFE", race, kind, f"k={k}", b, se, p, n=n, mean_treated=mt, mean_controls=mc)
    es_figure(ES)
    # Black - White difference of the event-study summaries (clusters = 1968 families, disjoint by head's race up to
    # a few split-offs, so the two estimates are treated as independent)
    ESD = {}
    for kind in ("main", "any", "strict", "quit"):
        for t in ("win", "sum11", "sum21"):
            b1, s1 = ES[("Black", kind)][t]
            b2, s2 = ES[("White", kind)][t]
            ESD[(kind, t)] = (b1 - b2, np.sqrt(s1 ** 2 + s2 ** 2))
            rec("event_study_ref_-4_-3", "Black - White", kind, t, *ESD[(kind, t)])
    panels = []
    for race, _ in RACES:
        rows = [(f"k = {k:+d}" + (" (ref.)" if k in (-4, -3) else ""),
                 [cell(*ES[(race, kd)][k]) if k not in (-4, -3) else "0" for kd in ("main", "any", "strict", "quit")])
                for k in KS]
        rows.append(("Mean k = -1..+1", [cell(*ES[(race, kd)]["win"]) for kd in ("main", "any", "strict", "quit")]))
        rows.append(("Sum k = -1..+1", [cell(*ES[(race, kd)]["sum11"]) for kd in ("main", "any", "strict", "quit")]))
        rows.append(("Sum k = -2..+1", [cell(*ES[(race, kd)]["sum21"]) for kd in ("main", "any", "strict", "quit")]))
        rows.append(("Ref. k = -4 only: k = -3", [cell(*ES4[(race, kd)][-3]) for kd in ("main", "any", "strict",
                                                                                      "quit")]))
        rows.append(("Rate in ref. years: displaced / controls",
                     [f"{ESI[(race, kd)]['ref_rate_treated']:.3f} / {ESI[(race, kd)]['ref_rate_controls']:.3f}"
                      for kd in ("main", "any", "strict", "quit")]))
        rows.append(("N wife-years / displaced / control units / clusters",
                     [f"{ESI[(race, kd)]['n']:,} / {ESI[(race, kd)]['units']:,} / {ESI[(race, kd)]['controls']:,} / "
                      f"{ESI[(race, kd)]['clusters']:,}" for kd in ("main", "any", "strict", "quit")]))
        panels.append((race, rows))
    panels.append(("Black - White (separate regressions, independent clusters)",
                   [(lab, [cell(*ESD[(kd, t)]) for kd in ("main", "any", "strict", "quit")])
                    for t, lab in (("win", "Mean k = -1..+1"), ("sum11", "Sum k = -1..+1"),
                                   ("sum21", "Sum k = -2..+1"))]))
    md += ["## 1. Event study of the wife's own job loss", "",
           "Unit x relative-year panel, k = -4..+4, wives employed at baseline, event years 1987-2018. Outcome: the "
           "baseline wife reports a job end of the kind in the column dated ev + k (missing if year not covered). "
           "Father x stack and calendar year x stack fixed effects; reference years k = -4, -3. 'Mean k = -1..+1' is "
           "the average of the three coefficients. Figure: `output/joint_job_loss_es.png`.", "",
           md_table([KLAB[k] for k in ("main", "any", "strict", "quit")], panels), ""]
    panels = []
    for race, _ in RACES:
        rows = []
        for kd in ("main", "strict"):
            rows.append((f"{KLAB[kd]}: displaced / control rate",
                         [f"{BY[(race, kd)][k][4]:.3f} / {BY[(race, kd)][k][5]:.3f}" for k in KS]))
            rows.append((f"{KLAB[kd]}: excess (event-year FE)", [cell(*BY[(race, kd)][k][:3]) for k in KS]))
        panels.append((race, rows))
    md += ["### 1b. Year by year without the couple fixed effect (no reference year)", "",
           "Same units; for each k a cross-section OLS of the indicator on displaced with event-year fixed effects.",
           "", md_table([f"k={k:+d}" for k in KS], panels), ""]
    print("event study done", flush=True)

    # ============================================================ 2. window + placebos
    WS = U[U["ev"].between(1987, 2021) & (U["wemp0"] == 1)].dropna(subset=["main_W", "main_PL"]).copy()
    WS["t_black"] = WS["treat"] * WS["black"]
    WS["p_black"] = WS["pseudo"] * WS["black"]
    WCOLS = [("main_W", "Wife displaced, ev-1..ev+1"), ("main_PL", "Wife displaced, ev-4..ev-2 (placebo window)"),
             ("main_D", "Difference (couple FE)"), ("any_W", "Any job end, ev-1..ev+1"),
             ("any_D", "Any job end, difference"), ("strict_W", "Employer closed, ev-1..ev+1"),
             ("strict_D", "Employer closed, difference")]
    WIN = {}
    for race, f in RACES + [("Pooled with race interactions", lambda q: q)]:
        q = f(WS)
        xs = ["treat", "pseudo"] + (["t_black", "p_black", "black"] if race.startswith("Pooled") else [])
        for y, _ in WCOLS:
            est, inf = ols_cl(q, y, xs, fe=["ev"])
            inf["ctrl"] = q.loc[(q["treat"] == 0) & (q["pseudo"] == 0), y].mean()
            inf["n_t"], inf["n_p"] = int(q["treat"].sum()), int(q["pseudo"].sum())
            WIN[(race, y)] = (est, inf)
            for x, (b, se, p) in est.items():
                rec("window", race, y, x, b, se, p, n=inf["n"], clusters=inf["clusters"], control_mean=inf["ctrl"],
                    treated=inf["n_t"], pseudo=inf["n_p"])
    # broader sample for the window outcomes: only the window ev-1..ev+1 must be covered
    WB = U[U["ev"].between(1987, 2021) & (U["wemp0"] == 1)].dropna(subset=["main_W"]).copy()
    WINB = {}
    for race, f in RACES:
        q = f(WB)
        for y in ("main_W", "any_W", "strict_W"):
            est, inf = ols_cl(q, y, ["treat", "pseudo"], fe=["ev"])
            inf["ctrl"] = q.loc[(q["treat"] == 0) & (q["pseudo"] == 0), y].mean()
            inf["n_t"] = int(q["treat"].sum())
            WINB[(race, y)] = (est, inf)
            for x, (b, se, p) in est.items():
                rec("window_broad", race, y, x, b, se, p, n=inf["n"], clusters=inf["clusters"],
                    control_mean=inf["ctrl"], treated=inf["n_t"])
    LX = {"treat": "Husband displaced in ev", "pseudo": "Husband displaced in ev+4..ev+6 (future placebo)",
          "t_black": "Displaced in ev x Black", "p_black": "Future placebo x Black", "black": "Black"}
    panels = []
    for race, _ in RACES + [("Pooled with race interactions", None)]:
        e0 = WIN[(race, "main_W")][0]
        rows = [(LX[x], [cell(*WIN[(race, y)][0][x]) for y, _ in WCOLS]) for x in e0]
        rows.append(("Control mean", [f"{WIN[(race, y)][1]['ctrl']:.3f}" for y, _ in WCOLS]))
        if (race, "main_W") in WINB:
            for x, lab in (("treat", "Broader sample (window covered only): husband displaced in ev"),
                           ("pseudo", "Broader sample: future placebo")):
                rows.append((lab, [cell(*WINB[(race, y)][0][x]) if (race, y) in WINB else "" for y, _ in WCOLS]))
            rows.append(("Broader sample: control mean / N / displaced",
                         [f"{WINB[(race, y)][1]['ctrl']:.3f} / {WINB[(race, y)][1]['n']:,} / "
                          f"{WINB[(race, y)][1]['n_t']:,}" if (race, y) in WINB else "" for y, _ in WCOLS]))
        rows.append(("N couples / displaced / future placebo / clusters",
                     [f"{WIN[(race, y)][1]['n']:,} / {WIN[(race, y)][1]['n_t']:,} / {WIN[(race, y)][1]['n_p']:,} / "
                      f"{WIN[(race, y)][1]['clusters']:,}" for y, _ in WCOLS]))
        panels.append((race, rows))
    md += ["## 2. Window estimates with a placebo window and a future-displacement placebo", "",
           "Father x stack units, wife employed at baseline, event years 1987-2021, both windows covered (one sample "
           "for all columns). OLS with event-year fixed effects. The future placebo compares men who will be "
           "displaced 4-6 years after ev with the same clean controls: if the excess reflected riskier couples "
           "(assortative risk) rather than a common shock, it would appear for them too. 'Difference' = W - PL, "
           "a design with a couple fixed effect.", "",
           md_table([lab for _, lab in WCOLS], panels, [("Fixed effects", ["event year"] * len(WCOLS))]), ""]
    print("window done", flush=True)

    # 2b. sample sensitivity of the window estimate (cross-section, treated vs clean controls)
    UA = add_wife_outcomes(build_units(m, d, kids=False), m, ev_sets)
    base = lambda X_: X_[(X_["pseudo"] == 0) & (X_["wemp0"] == 1)]
    SENS = [("23's window variable and sample (ev 1984-2021, wife seen before and after)", "J_disp",
             lambda X_: base(X_)[base(X_)["ev"].between(1984, 2021) & (base(X_)["observed"] == 1)], U),
            ("ev 1984-2021, all three window years covered", "main_W",
             lambda X_: base(X_)[base(X_)["ev"].between(1984, 2021)], U),
            ("ev 1984-1989", "main_W", lambda X_: base(X_)[base(X_)["ev"].between(1984, 1989)], U),
            ("ev 1990-1999", "main_W", lambda X_: base(X_)[base(X_)["ev"].between(1990, 1999)], U),
            ("ev 2000-2021", "main_W", lambda X_: base(X_)[base(X_)["ev"].between(2000, 2021)], U),
            ("ev 1987-2021, window covered", "main_W", lambda X_: base(X_)[base(X_)["ev"].between(1987, 2021)], U),
            ("ev 1987-2021, window and placebo window covered (main sample)", "main_W",
             lambda X_: base(X_)[base(X_)["ev"].between(1987, 2021) & base(X_)["main_PL"].notna()], U),
            ("All married men, with or without children (main-sample rules)", "main_W",
             lambda X_: base(X_)[base(X_)["ev"].between(1987, 2021) & base(X_)["main_PL"].notna()], UA)]
    rows = []
    for lab, y, sf, src in SENS:
        r = []
        for race, f in RACES:
            q = f(sf(src)).dropna(subset=[y])
            est, inf = ols_cl(q, y, ["treat"], fe=["ev"])
            cm = q.loc[q["treat"] == 0, y].mean()
            r.append(cell(*est["treat"]) + f" [ctrl {cm:.3f}; {int(q['treat'].sum())} / {inf['n']:,}]")
            rec("window_sensitivity", f"{race}: {lab}", y, "treat", *est["treat"], n=inf["n"], control_mean=cm,
                treated=int(q["treat"].sum()))
        rows.append((lab, r))
    md += ["### 2b. Sample sensitivity of the window estimate", "",
           "Wife displaced in ev-1..ev+1 on husband displaced, event-year FE, wives employed at baseline, treated vs "
           "clean controls. Cell: coefficient (s.e.; p) [control mean; displaced / N].", "",
           md_table(["All", "Black", "White"], [("", rows)]), ""]

    # ============================================================ 3. identification
    I = WS[WS["pseudo"] == 0].copy()
    I["t_same_sec"] = I["treat"] * I["same_sec"]
    I["t_same_ind3"] = I["treat"] * I["same_ind3"]
    I["t_same_occ"] = I["treat"] * I["same_occ"]
    sd_ur = I.loc[I["treat"] == 1, "d_ur"].std()
    mu_ur = I.loc[I["treat"] == 1, "d_ur"].mean()
    I["d_ur_z"] = (I["d_ur"] - mu_ur) / sd_ur
    I["t_d_ur"] = I["treat"] * I["d_ur_z"]
    ICOLS = [("cl_main", "Closures only", "Wife displaced", "main_W", ["treat"], lambda q: q[q["layoff"] == 0], []),
             ("cl_strict", "Closures only", "Wife's employer closed", "strict_W", ["treat"],
              lambda q: q[q["layoff"] == 0], []),
             ("lo_main", "Layoffs only", "Wife displaced", "main_W", ["treat"], lambda q: q[q["closure"] == 0], []),
             ("sec", "Sector match", "Wife displaced", "main_W", ["treat", "t_same_sec", "same_sec"],
              lambda q: q.dropna(subset=["same_sec"]), []),
             ("ind3", "3-digit industry match", "Wife displaced", "main_W", ["treat", "t_same_ind3", "same_ind3"],
              lambda q: q.dropna(subset=["same_ind3"]), []),
             ("occ", "Occupation-group match", "Wife displaced", "main_W", ["treat", "t_same_occ", "same_occ"],
              lambda q: q.dropna(subset=["same_occ"]), []),
             ("ur", "State unemployment", "Wife displaced", "main_W", ["treat", "t_d_ur", "d_ur_z"],
              lambda q: q.dropna(subset=["d_ur_z"]), []),
             ("pre", "Pre-trend controls", "Wife displaced", "main_W", ["treat", "main_PL"], lambda q: q, PRE),
             ("noself", "No self-employed spouse", "Wife displaced", "main_W", ["treat"],
              lambda q: q[q["any_self"] == 0], [])]
    IL = {"treat": "Husband displaced", "t_same_sec": "Displaced x wife in his sector", "same_sec": "Wife in his sector",
          "t_same_ind3": "Displaced x same 3-digit industry", "same_ind3": "Same 3-digit industry",
          "t_same_occ": "Displaced x same occupation group", "same_occ": "Same occupation group",
          "t_d_ur": "Displaced x state unemployment change (s.d.)", "d_ur_z": "State unemployment change (s.d.)",
          "main_PL": "Wife displaced in ev-4..ev-2"}
    IROW = ["treat", "t_same_sec", "same_sec", "t_same_ind3", "same_ind3", "t_same_occ", "same_occ", "t_d_ur", "d_ur_z",
            "main_PL"]
    IDR = {}
    for race, f in RACES:
        for key, _, _, y, xs, sf, ctrl in ICOLS:
            q = sf(f(I))
            est, inf = ols_cl(q, y, xs + usable(q, ctrl), fe=["ev"])
            inf["ctrl"] = q.loc[q["treat"] == 0, y].mean()
            inf["n_t"] = int(q["treat"].sum())
            inf["share"] = q.loc[q["treat"] == 1, xs[2]].mean() if key in ("sec", "ind3", "occ") else np.nan
            IDR[(race, key)] = (est, inf)
            for x in xs:
                rec("identification", race, f"{key}: {y}", x, *est[x], n=inf["n"], clusters=inf["clusters"],
                    control_mean=inf["ctrl"], treated=inf["n_t"])
    panels = []
    for race, _ in RACES:
        rows = []
        for x in IROW:
            rows.append((IL[x], [cell(*IDR[(race, k)][0][x]) if x in IDR[(race, k)][0] else ""
                                 for k, *_ in ICOLS]))
        rows.append(("Control mean", [f"{IDR[(race, k)][1]['ctrl']:.3f}" for k, *_ in ICOLS]))
        rows.append(("Share of displaced with the match", [f"{IDR[(race, k)][1]['share']:.3f}"
                                                          if IDR[(race, k)][1]['share'] == IDR[(race, k)][1]['share']
                                                          else "" for k, *_ in ICOLS]))
        rows.append(("N couples / displaced", [f"{IDR[(race, k)][1]['n']:,} / {IDR[(race, k)][1]['n_t']:,}"
                                               for k, *_ in ICOLS]))
        panels.append((race, rows))
    md += ["## 3. Identification checks", "",
           "Sample of section 2 without the future placebo. Outcome: wife displaced in ev-1..ev+1 (column 2: her "
           "employer closed). OLS with event-year fixed effects. Closures only: displaced men whose first job loss "
           "was a closure vs controls (layoffs dropped), and vice versa. Matches are measured before the event "
           "(husband: latest interview in [ev-3, ev]; wife: latest in [ev-6, ev]); the state unemployment change is "
           "in ev, in s.d. among displaced (s.d. " + f"{sd_ur:.2f} pp). Pre-trend controls: husband's hours and labor "
           "income at ev-2 (ev-3 in biennial years) and their change over the two years before, the wife's hours "
           "likewise, missing indicators, "
           "and the wife's own displacement in ev-4..ev-2. Self-employment: either spouse works for self (or self "
           "and others) at an interview in ev-3..ev.", "",
           md_table([f"{a}: {b}" for _, a, b, *_ in ICOLS], panels, [("Fixed effects", ["event year"] * len(ICOLS))]),
           ""]
    print("identification done", flush=True)

    # ============================================================ 4. magnitudes
    CY = couple_years(m, d, ev_sets, C)
    MAG = {}
    CYS = [("All couple-years", lambda q: q), ("Black", lambda q: q[q["black"] == 1]),
           ("White", lambda q: q[q["black"] == 0]),
           ("Same sector", lambda q: q[q["s_sec"] == 1]), ("Different sector", lambda q: q[q["s_sec"] == 0]),
           ("Black, same sector", lambda q: q[(q["black"] == 1) & (q["s_sec"] == 1)]),
           ("White, same sector", lambda q: q[(q["black"] == 0) & (q["s_sec"] == 1)]),
           ("Youngest child 0-5", lambda q: q[q["kid"] == "0-5"]), ("Youngest child 6-17", lambda q: q[q["kid"] == "6-17"]),
           ("No child under 18", lambda q: q[q["kid"] == "none"]),
           ("Annual survey years (to 1996)", lambda q: q[q["annual"]]),
           ("Annual, Black", lambda q: q[q["annual"] & (q["black"] == 1)]),
           ("Annual, White", lambda q: q[q["annual"] & (q["black"] == 0)])]
    for wv, wlab in (("w", "same interval"), ("w_pm1", "interval +- 1 year")):
        for sname, f in CYS:
            o = joint_stats(f(CY), "h", wv)
            MAG[(wv, sname)] = o
            for k, v in o.items():
                if k in ("diff",):
                    rec("magnitudes", sname, wv, "P(w|h) - P(w|not h) (OLS)", *v, n=o["N"], clusters=o["clusters"])
                elif not k.endswith("_se"):
                    rec("magnitudes", sname, wv, k, v, o.get(f"{k}_se", np.nan), n=o["N"])
        print("magnitudes", wv, flush=True)
    panels = []
    for wv, wlab in (("w", "Wife displaced in the same interval as the husband's displacement"),
                     ("w_pm1", "Wife displaced in the interval or within one year of it")):
        rows = []
        for sname, _ in CYS:
            o = MAG[(wv, sname)]
            rows.append((sname, [f"{o['N']:,}", f"{o['Ph']:.4f}", f"{o['Pw']:.4f}", f"{o['Pw_h']:.3f} ({o['n_h']:,})",
                                 f"{o['Pw_noh']:.4f}", f"{o['ratio']:.2f} ({o['ratio_se']:.2f})", cell(*o["diff"]),
                                 cell(o["phi"], o["phi_se"]), cell(o["tet"], o["tet_se"])]))
        panels.append((wlab, rows))
    md += ["## 4. Magnitudes for the model: joint job-loss probabilities within couples", "",
           "Couple-years: consecutive interviews of the same couple, both spouses with positive annual hours in the "
           "earlier year, intervals ending 1984-2022. h = husband displaced (closure / layoff) in the interval; w = "
           "wife displaced in the same interval (one year to 1996, two years in the biennial survey; 'annual' rows "
           "keep one-year intervals 1984-1996, the model's period). Sector match: both spouses' sectors at the "
           "interview opening the interval. Difference: OLS of w on h, clustered by 1968 family. Ratio, phi and "
           "tetrachoric correlation: s.e. from 200 bootstrap draws of 1968 families (p-values from the normal "
           "approximation).", "",
           md_table(["Couple-years", "P(h)", "P(w)", "P(w | h) (N h)", "P(w | not h)", "Ratio (s.e.)",
                     "P(w|h) - P(w|not h)", "Phi", "Tetrachoric"], panels), ""]

    # ============================================================ 5. family income accounting
    P = P19.stacks(m, d, "main")
    P = P.merge(m[["pid", "year", "wlab"]], on=["pid", "year"], how="left")
    P["w_lab"] = P["wlab"].where(P["w_pid"] == P["w0"])
    J = U[(U["pseudo"] == 0)][["pid", "ev", "wemp0", "main_W"]].copy()
    J["J"] = np.where(J["wemp0"] == 0, 0.0, J["main_W"])
    P = P.merge(J[["pid", "ev", "J", "wemp0"]], on=["pid", "ev"], how="left")
    fall = P19.event_study(P, "faminc")
    tot19 = next(r for r in fall if r["term"] == "mean +1..+3")
    q = P[P["ev"].between(1984, 2021) & P["w0"].notna() & P["J"].notna()].copy()
    u = q.drop_duplicates("unit")
    share_wife = P[P["treat"] == 1].drop_duplicates("unit")["w0"].notna().mean()
    P1, P0 = u.loc[u["treat"] == 1, "J"].mean(), u.loc[u["treat"] == 0, "J"].mean()
    semp = u.loc[u["treat"] == 1, "wemp0"].mean()
    dd = WIN[("All", "main_D")][0]["treat"]
    bt, bp = WINB[("All", "main_W")][0]["treat"], WINB[("All", "main_W")][0]["pseudo"]
    net = (bt[0] - bp[0], np.sqrt(bt[1] ** 2 + bp[1] ** 2))
    INC = {}
    for y in ("faminc", "w_lab", "hlab"):
        est0, inf0, _ = P23.binned(q, y)
        est, inf, _ = P23.binned(q, y, mods=["J"])
        cost = est["m_J_post13"]
        ch = (P1 - P0) * cost[0]
        ch_dd = semp * dd[0] * cost[0]
        ch_dd_se = np.sqrt((semp * dd[0] * cost[1]) ** 2 + (semp * cost[0] * dd[1]) ** 2)
        ch_n = semp * net[0] * cost[0]
        ch_n_se = np.sqrt((semp * net[0] * cost[1]) ** 2 + (semp * cost[0] * net[1]) ** 2)
        INC[y] = dict(tot=est0["d_post13"], cost=cost, ch=(ch, abs(P1 - P0) * cost[1]), ch_dd=(ch_dd, ch_dd_se),
                      ch_n=(ch_n, ch_n_se),
                      n=inf0["n"], units=inf0["units"])
        rec("income_accounting", "married, ev 1984-2021", y, "total response +1..+3", *est0["d_post13"], n=inf0["n"])
        rec("income_accounting", "married, ev 1984-2021", y, "cost of wife's displacement (controls)", *cost)
        rec("income_accounting", "married, ev 1984-2021", y, "channel (P1-P0) x cost", ch, abs(P1 - P0) * cost[1])
        rec("income_accounting", "married, ev 1984-2021", y, "channel (DiD excess x share employed) x cost", ch_dd,
            ch_dd_se)
        rec("income_accounting", "married, ev 1984-2021", y,
            "channel (window excess net of future placebo x share employed) x cost", ch_n, ch_n_se)
    rec("income_accounting", "all fathers (19)", "faminc", "total response +1..+3", tot19["coef"], tot19["se"],
        n=tot19["n"])
    fi = INC["faminc"]
    rows = [("Family income response, all fathers (19's design, re-estimated)", big(tot19["coef"], tot19["se"])),
            ("Family income response, married, ev 1984-2021", big(*fi["tot"])),
            ("Wife's labor income response, same sample", big(*INC["w_lab"]["tot"])),
            ("Husband's labor income response, same sample", big(*INC["hlab"]["tot"])),
            ("P(wife displaced ev-1..ev+1): displaced / control families (0 if not working at baseline)",
             f"{P1:.3f} / {P0:.3f}"),
            ("Share of displaced families with the wife employed at baseline", f"{semp:.3f}"),
            ("Cost of the wife's displacement, family income (control families, +1..+3)", big(*fi["cost"])),
            ("Cost of the wife's displacement, her labor income", big(*INC["w_lab"]["cost"])),
            ("Joint-loss channel, family income: (P1 - P0) x cost", big(*fi["ch"])),
            ("Joint-loss channel, family income: DiD excess x share employed x cost", big(*fi["ch_dd"])),
            ("Joint-loss channel, family income: (window excess - future placebo, " + f"{net[0]:.3f}" +
             ") x share employed x cost", big(*fi["ch_n"])),
            ("Joint-loss channel, wife's labor income: same, net version", big(*INC["w_lab"]["ch_n"])),
            ("Share of the married-sample family income loss: (P1-P0) / DiD version",
             f"{fi['ch'][0] / fi['tot'][0]:.3f} / {fi['ch_dd'][0] / fi['tot'][0]:.3f}"),
            ("Share of 19's pooled loss (x share of displaced fathers with a wife, "
             f"{share_wife:.3f}): (P1-P0) / DiD version",
             f"{fi['ch'][0] * share_wife / tot19['coef']:.3f} / {fi['ch_dd'][0] * share_wife / tot19['coef']:.3f}"),
            ("Family income loss beyond the husband's labor income loss (married sample)",
             f"{fi['tot'][0] - INC['hlab']['tot'][0]:,.0f}"),
            ("Joint-loss channel (wife's labor income) as a share of that gap",
             f"{INC['w_lab']['ch'][0] / (fi['tot'][0] - INC['hlab']['tot'][0]):.2f}"),
            ("Joint-loss channel, wife's labor income: (P1 - P0) x cost / share of her response",
             big(*INC["w_lab"]["ch"]) + f" / {INC['w_lab']['ch'][0] / INC['w_lab']['tot'][0]:.2f}"),
            ("N man-years / displaced fathers (married sample)", f"{fi['n']:,} / {fi['units']:,}")]
    for k, v in (("share_married_P1P0", fi['ch'][0] / fi['tot'][0]), ("share_married_DiD", fi['ch_dd'][0] / fi['tot'][0]),
                 ("share_19_P1P0", fi['ch'][0] * share_wife / tot19['coef']),
                 ("share_19_DiD", fi['ch_dd'][0] * share_wife / tot19['coef'])):
        rec("income_accounting", "shares", "faminc", k, v, np.nan)
    md += ["## 5. How much of the family income loss is the wife's joint job loss?", "",
           "19's stacked design (father x stack and calendar year x stack fixed effects, mean of e = +1..+3 relative "
           "to e = -2; 2000 dollars). Married fathers, event years 1984-2021 (window measurable). Accounting, not "
           "causal: the wife's job loss is an outcome; the cost is the change that comes with her displacement among "
           "control families (bin x J coefficient in the model with displaced x bin x J). The DiD version replaces "
           "P1 - P0 by the window difference-in-differences of section 2 (pooled) times the share of displaced "
           "families whose wife worked at baseline, which removes assortative risk.", "",
           md_table(["Estimate"], [("", [(a, [b]) for a, b in rows])]), ""]
    print("income done", flush=True)

    # ============================================================ LaTeX
    tex = []
    # Table 1: window
    cols = [("main_W", ["Wife displaced", "$ev-1$ to $ev+1$"]), ("main_PL", ["Wife displaced", "$ev-4$ to $ev-2$"]),
            ("main_D", ["Wife displaced", "difference"]), ("any_W", ["Any job end", "$ev-1$ to $ev+1$"]),
            ("any_D", ["Any job end", "difference"]), ("strict_W", ["Employer closed", "$ev-1$ to $ev+1$"]),
            ("strict_D", ["Employer closed", "difference"])]
    head = [" & " + " & ".join(thdr(i + 1, l) for i, (_, l) in enumerate(cols)) + r" \\"]
    body = []
    for title, race in (("A. All couples", "All"), ("B. Black couples", "Black"), ("C. White couples", "White")):
        body.append(rf"\multicolumn{{{len(cols) + 1}}}{{l}}{{\textit{{{title}}}}} \\")
        for x, lab in (("treat", r"Husband displaced in $ev$"), ("pseudo", r"Husband displaced in $ev+4$ to $ev+6$")):
            body += trows(lab, [tcell(*WIN[(race, y)][0][x][:2]) for y, _ in cols])
        esmap = {"main_W": "main", "any_W": "any", "strict_W": "strict"}
        body += trows(r"Husband displaced in $ev$, window-only sample",
                      [tcell(*WINB[(race, y)][0]["treat"][:2]) if y in esmap else ("", "") for y, _ in cols])
        body += trows(r"Event study, sum of years $-1$ to $+1$",
                      [tcell(*ES[(race, esmap[y])]["sum11"]) if y in esmap else ("", "") for y, _ in cols])
        body.append("Control mean & " + " & ".join(f"{WIN[(race, y)][1]['ctrl']:.3f}" for y, _ in cols) + r" \\")
        body.append("Couples & " + " & ".join(f"{WIN[(race, y)][1]['n']:,}" for y, _ in cols) + r" \\")
    body.append(rf"\multicolumn{{{len(cols) + 1}}}{{l}}{{\textit{{D. Black $-$ White (pooled, interactions)}}}} \\")
    body += trows(r"Husband displaced in $ev$ $\times$ Black",
                  [tcell(*WIN[("Pooled with race interactions", y)][0]["t_black"][:2]) for y, _ in cols])
    note = (r"Unit: a father $\times$ event year $ev$ with his wife employed at baseline; the treated are fathers first "
            r"displaced (plant closed or moved, laid off or fired) in $ev$, the controls fathers not displaced up to "
            r"$ev+6$, and the future placebo fathers first displaced in $ev+4$ to $ev+6$. Outcomes: the wife's own "
            r"report that a job of hers ended because she was laid off or fired or her employer closed (displaced), "
            r"for any reason (any job end), or because her employer closed, dated in the window of the column; "
            r"``difference'' is the window $ev-1$ to $ev+1$ minus the window $ev-4$ to $ev-2$, which removes any "
            r"permanent difference in the wife's job stability. Event years 1987--2021, both windows observed. OLS "
            r"with event-year fixed effects. ``Window-only sample'': the same regression among all couples whose "
            r"window $ev-1$ to $ev+1$ is observed (the placebo window need not be; "
            + f"{WINB[('All', 'main_W')][1]['n']:,} couples, {WINB[('All', 'main_W')][1]['n_t']:,} displaced"
            + r"). ``Event study'': sum of the coefficients for years $-1$, $0$ and $+1$ "
            r"from a regression of the wife's annual job-loss indicator in years $-4$ to $+4$ on displaced $\times$ "
            r"year dummies with couple and calendar-year fixed effects, reference years $-4$ and $-3$ (event years "
            r"1987--2018; figure \texttt{IGE/output/joint\_job\_loss\_es.png}). PSID SRC and SEO, unweighted. Standard errors clustered by 1968 family "
            r"in parentheses. *** $p<0.01$, ** $p<0.05$, * $p<0.1$. Source: \texttt{IGE/25.JointJobLoss.py}.")
    tex.append(ttable("The wife's own job loss around her husband's displacement", "tab:joint_job_loss", head, body,
                      note, len(cols)))
    # Table 2: identification
    SHORT = {"cl_main": ["Closures", "only"], "cl_strict": ["Closures only:", "her employer", "closed"],
             "lo_main": ["Layoffs", "only"], "sec": ["Same", "sector"], "ind3": ["Same 3-digit", "industry"],
             "occ": ["Same", "occupation"], "ur": ["State", "unemployment"], "pre": ["Pre-trend", "controls"],
             "noself": ["No self-", "employed"]}
    icols = [(k, SHORT[k]) for k, *_ in ICOLS]
    head = [" & " + " & ".join(thdr(i + 1, l) for i, (_, l) in enumerate(icols)) + r" \\"]
    ILT = dict(IL, t_d_ur=r"Displaced $\times$ $\Delta$ state unemployment (s.d.)",
               d_ur_z=r"$\Delta$ state unemployment (s.d.)",
               t_same_sec=r"Displaced $\times$ wife in his sector", t_same_ind3=r"Displaced $\times$ same 3-digit industry",
               t_same_occ=r"Displaced $\times$ same occupation group", main_PL=r"Wife displaced in $ev-4$ to $ev-2$")
    body = []
    for title, race in (("A. All couples", "All"), ("B. Black couples", "Black"), ("C. White couples", "White")):
        body.append(rf"\multicolumn{{{len(icols) + 1}}}{{l}}{{\textit{{{title}}}}} \\")
        for x in IROW:
            if race != "All" and x in ("same_sec", "same_ind3", "same_occ", "d_ur_z"):
                continue
            body += trows(ILT[x], [tcell(*IDR[(race, k)][0][x][:2]) if x in IDR[(race, k)][0] else ("", "")
                                   for k, *_ in ICOLS])
        body.append("Control mean & " + " & ".join(f"{IDR[(race, k)][1]['ctrl']:.3f}" for k, *_ in ICOLS) + r" \\")
        body.append("Couples & " + " & ".join(f"{IDR[(race, k)][1]['n']:,}" for k, *_ in ICOLS) + r" \\")
    note = (r"Sample of Table~\ref{tab:joint_job_loss} without the future placebo; outcome: the wife displaced in "
            r"$ev-1$ to $ev+1$ (column 2: her employer closed). Columns 1--2 keep displaced husbands whose job loss "
            r"was a plant closure, column 3 those laid off or fired. Columns 4--6 interact the displacement with the "
            r"spouses working in the same of 16 sectors, the same 3-digit Census industry, or the same of 8 major "
            r"occupation groups (husband: latest interview in $ev-3$ to $ev$; wife: $ev-6$ to $ev$). Column 7: change "
            r"in the state unemployment rate in $ev$ (LAUS), in standard deviations among the displaced. Column 8 "
            r"controls for the husband's hours and labor income at $ev-2$ ($ev-3$ in biennial years) and their change "
            r"over the two years before, the wife's hours likewise, and her displacement in $ev-4$ to $ev-2$. Column 9 drops couples in "
            r"which either spouse was self-employed at an interview in $ev-3$ to $ev$. Main effects of the match "
            r"variables are included in every panel (shown in panel A). OLS with event-year fixed effects; standard "
            r"errors clustered by 1968 family. *** $p<0.01$, ** $p<0.05$, * $p<0.1$. Source: "
            r"\texttt{IGE/25.JointJobLoss.py}.")
    tex.append(ttable("Joint job loss: closures, shared labor markets and pre-trends", "tab:joint_job_loss_id", head,
                      body, note, len(icols)))
    # Table 3: magnitudes (one column per statistic; rows = samples)
    mcols = [["P(she is displaced", "$\\mid$ he is)"], ["P(she is displaced", "$\\mid$ he is not)"],
             ["Difference", ""], ["Phi", "coefficient"], ["Tetrachoric", "correlation"]]
    head = [" & " + " & ".join(thdr(i + 1, l) for i, l in enumerate(mcols)) + r" \\"]
    body = []
    for wv, title in (("w", "A. Same year (interval)"), ("w_pm1", "B. Within one year")):
        body.append(rf"\multicolumn{{{len(mcols) + 1}}}{{l}}{{\textit{{{title}}}}} \\")
        for sname in ("All couple-years", "Black", "White", "Same sector", "Different sector", "Youngest child 0-5",
                      "Youngest child 6-17", "No child under 18", "Annual survey years (to 1996)"):
            o = MAG[(wv, sname)]
            body += [f"{sname.replace('0-5', '0--5').replace('6-17', '6--17')} & {o['Pw_h']:.3f} & {o['Pw_noh']:.3f} & " + " & ".join(
                c[0] for c in (tcell(*o["diff"][:2]), tcell(o["phi"], o["phi_se"]), tcell(o["tet"], o["tet_se"])))
                     + r" \\", " & & & " + " & ".join(c[1] for c in (tcell(*o["diff"][:2]), tcell(o["phi"], o["phi_se"]),
                                                                    tcell(o["tet"], o["tet_se"]))) + r" \\"]
    note = (r"Couple-years: consecutive interviews of the same married couple, both spouses with positive hours in "
            r"the earlier year, intervals ending 1984--2022 (one year to 1996, two years in the biennial survey; the "
            r"last row keeps one-year intervals). Panel A: both spouses displaced (closure, layoff or firing) in the "
            r"same interval; panel B: her displacement within one year either side of the interval. Column 3: OLS of "
            r"her displacement on his, standard error clustered by 1968 family; columns 4--5: standard errors from 200 "
            r"bootstrap draws of 1968 families. *** $p<0.01$, ** $p<0.05$, * $p<0.1$. Source: "
            r"\texttt{IGE/25.JointJobLoss.py}.")
    tex.append(ttable("How often both spouses lose their jobs", "tab:joint_job_loss_magnitudes", head, body, note,
                      len(mcols)))
    (PAPER / "tab_joint_job_loss.tex").write_text("\n".join(tex), encoding="utf-8")

    # ============================================================ summary + write
    md += summary(ES, ESD, WIN, WINB, IDR, MAG, INC, net, P1, P0, semp)
    md += LIT.splitlines()
    pd.DataFrame(ROWS).to_csv(OUT / "joint_job_loss.csv", index=False)
    (OUT / "joint_job_loss.md").write_text("\n".join(md), encoding="utf-8")
    print("written", flush=True)


def summary(ES, ESD, WIN, WINB, IDR, MAG, INC, net, P1, P0, semp):
    """paragraph-level text for paperA_joint_loss/sec6_why.tex; every number is read from the estimates above."""
    def c(t, d=3, pct=False):
        b, se = t[0], t[1]
        p = pv(b, se)
        k = 100 if pct else 1
        dd = 1 if pct else d
        pp = "p<0.001" if p < 0.001 else f"p={p:.3f}"
        return f"{k * b:.{dd}f}{stars(p)} (s.e. {k * se:.{dd}f}; {pp})"
    def neg(t):
        p = pv(t[0], t[1])
        pp = "p<0.001" if p < 0.001 else f"p={p:.3f}"
        return f"{-t[0]:,.0f}{stars(p)} (s.e. {t[1]:,.0f}; {pp})"
    wb = {r: WINB[(r, "main_W")][0] for r in ("All", "Black", "White")}
    cm = {r: WINB[(r, "main_W")][1]["ctrl"] for r in ("All", "Black", "White")}
    e = ES[("All", "main")]
    idr = lambda k, x="treat": IDR[("All", k)][0][x]
    sh = {k: IDR[("All", k)][1]["share"] for k in ("sec", "ind3")}
    M, Ma = MAG[("w", "All couple-years")], MAG[("w", "Annual survey years (to 1996)")]
    Ms, Md = MAG[("w", "Same sector")], MAG[("w", "Different sector")]
    Mb, Mw = MAG[("w", "Black")], MAG[("w", "White")]
    gap = INC["faminc"]["tot"][0] - INC["hlab"]["tot"][0]
    rise = 100 * wb["All"]["treat"][0] / cm["All"]
    p1 = (
        "When a husband is displaced, the household's second earner is often hit by the same shock. I measure the "
        "wife's own job losses from her answers to the PSID question on why a job ended (asked of wives from 1984), "
        "and compare the wives of men displaced in a given year with the wives of men not displaced in the following "
        "six years, among wives working before the event. Over the three years around the husband's displacement "
        "(the year before to the year after), the probability that the wife is herself laid off, fired or loses her "
        f"job to a closure is higher by {c(wb['All']['treat'], pct=True)} percentage points, from a base of "
        f"{100 * cm['All']:.1f}%: her risk of a job loss more than doubles. "
        "Year by year, with couple and calendar-year fixed effects and the fourth and third years before the event "
        f"as the reference, the excess appears two years before the husband's job loss ({c(e[-2])}), peaks in the "
        f"year of his job loss ({c(e[0])}) and is gone by the second year after it ({c(e[2])}); the closure of her "
        f"employer rises only in the year of his job loss ({c(ES[('All', 'strict')][0])}). The early start is "
        "consistent with the two spouses' reports dating the same events a year apart and with shocks that reach a "
        "workplace before they reach a particular worker. It is not a permanent difference between couples: the "
        "wives of men who will be displaced four to six years later have no excess risk in the same window "
        f"({c(wb['All']['pseudo'], pct=True)} points), and the excess survives controls for both spouses' hours and "
        f"earnings before the event ({c(idr('pre'), pct=True)} points, in the subsample that also observes the "
        f"earlier window) and the exclusion of self-employed spouses ({c(idr('noself'), pct=True)})."
    )
    p2 = (
        "The joint losses come from shared workplaces and industries rather than from the local business cycle. When "
        f"the husband's job loss is a plant closure, the wife's risk rises by {c(idr('cl_main'), pct=True)} points and "
        f"the probability that her own employer closes by {c(idr('cl_strict'), pct=True)}. The excess is concentrated "
        f"among couples who work in the same sector ({100 * sh['sec']:.0f}% of displaced couples; interaction "
        f"{c(idr('sec', 't_same_sec'), pct=True)} points) and especially in the same three-digit industry "
        f"({100 * sh['ind3']:.0f}%; {c(idr('ind3', 't_same_ind3'), pct=True)}), the closest proxy the public PSID "
        "offers for a common employer. It does not vary with the change in the state unemployment rate "
        f"({c(idr('ur', 't_d_ur'), pct=True)} points per standard deviation)."
    )
    p3 = (
        "For the model, the relevant object is the joint probability of the two job losses. Among couple-years in "
        "which both spouses worked, the wife is displaced in the same interval in "
        f"{100 * M['Pw_h']:.1f}% of the cases in which the husband is displaced and in {100 * M['Pw_noh']:.1f}% of the "
        f"others (difference {c(M['diff'], pct=True)} points; ratio {M['ratio']:.1f}); in the annual survey years "
        f"the figures are {100 * Ma['Pw_h']:.1f}% and {100 * Ma['Pw_noh']:.1f}%. The implied tetrachoric correlation of "
        f"the two job-loss events is {c((M['tet'], M['tet_se']), d=2)} ({Ma['tet']:.2f} in the annual years; phi "
        f"{M['phi']:.3f}): {Ms['tet']:.2f} for couples in the same sector and {Md['tet']:.2f} for the others, "
        f"{Mb['tet']:.2f} for Black and {Mw['tet']:.2f} for White couples. Joint job loss is a general feature of "
        "family insurance; the racial difference is second order. Black wives' baseline risk is higher, and the "
        "excess around the husband's job loss is at least as large for Black as for White couples (window "
        f"{c(wb['Black']['treat'], pct=True)} against {c(wb['White']['treat'], pct=True)} points). Whether it is "
        "larger depends on the design: in the couple fixed-effects event study the Black-White difference in the "
        f"mean of years -1 to +1 is {c(ESD[('main', 'win')], pct=True)} points a year, in the window design on the "
        "subsample that also observes the earlier window it is "
        f"{c(WIN[('Pooled with race interactions', 'main_W')][0]['t_black'], pct=True)}."
    )
    p4 = (
        "The joint losses cost the wife earnings but account for little of the family's income loss. Among control "
        f"families a wife's displacement lowers her labor income by {neg(INC['w_lab']['cost'])} dollars a year over "
        f"the next three years. With an excess probability of {P1 - P0:.3f} among all married fathers (her "
        f"displacement is zero if she did not work), the joint loss lowers the average wife's labor income after the "
        f"husband's displacement by {neg(INC['w_lab']['ch'])} dollars ({neg(INC['w_lab']['ch_n'])} with the window "
        f"excess net of the future-displacement placebo, {net[0]:.3f}, times the {100 * semp:.0f}% of wives working at "
        f"baseline): about {INC['w_lab']['ch'][0] / gap:.0%} of the {-gap:,.0f} dollars by which family income falls "
        f"beyond the husband's own labor income, and {INC['faminc']['ch'][0] / INC['faminc']['tot'][0]:.0%} of the "
        f"family income loss ({neg(INC['faminc']['tot'])} dollars). The joint loss matters for insurance less through its "
        "average cost than through its timing: it removes the second earner in the states in which she is needed, so "
        "a model in which the second earner's job loss is independent of the first earner's overstates the "
        "insurance the family can provide."
    )
    return ["## 6. Summary paragraphs for paperA_joint_loss/sec6_why.tex (not inserted; numbers generated by this script)", "",
            p1, "", p2, "", p3, "", p4, "",
            "Footnote: Code: IGE/25.JointJobLoss.py; tables tab:joint_job_loss, tab:joint_job_loss_id, "
            "tab:joint_job_loss_magnitudes in paperA_joint_loss/tab_joint_job_loss.tex; figure output/joint_job_loss_es.png. "
            "Wives' reasons for a job ending are asked from the 1984 wave; event years 1987-2021; standard errors "
            "clustered by 1968 family. (In LaTeX: escape % as \\%.)", ""]


if __name__ == "__main__":
    main()
