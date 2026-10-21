r"""The added-worker effect by age (Bacher, Grubener and Nord 2025) and joint job loss by age, CPS couples panel.
(2026-10-18) [Paper A; race-neutral]

Reference: Bacher, Grubener and Nord (2025), "Joint search over the life cycle", Journal of Monetary Economics 150,
103696 (Literature/1-s2.0-S0304393224001491-main.pdf; "BGN"), Section 2, Tables 1-2, Figs. 1-2, Eq. (1). Design:
proposals/fable_bacher2025_paperA.md, Section 4.1-4.2.

DATA
  The raw CPS basic monthly files of 30.CPSJointJobLoss.py (data/ext/cps_couples/, Census API 1994-2023, persons
  with PEMARITL = 1 and PRTAGE 20-62); no new download. Script 30's couples panel keeps couples with both spouses 20-60;
  here the same builder (30's read_month / build_panel, imported read-only) is run with the upper age bound at 62, the
  bound of the raw files, and cached as data/cps_couples_panel_2062.pkl (git-ignored). Everything else (couple
  definition, person links, link-rate rule, status codes) is 30's. Status s: 1 employed (PEMLR 1-2), 2 job loser
  (PEMLR 3-4 with PRUNTYPE 1-3), 3 other unemployed, 4 not in the labor force (PEMLR 5-7), 0 status missing, -1 not
  linked. E = 1, U = 2-3, N = 4.
COUPLES
  Married, spouse present, opposite-sex couples who name each other (30's definition); both spouses 26-62 at the base
  month for part (1) (BGN: both 26-65, married or cohabiting, any sex; the raw files stop at 62 and hold no cohabiting
  partners, so 56-62 stands in for BGN's 56-65). "Sex-neutral" = BGN's assignment: the employed member is the primary
  earner, whichever sex; "wives" = husband employed, wife not in the labor force (the model's object).
PART (1): BGN's added-worker effect (AWE)
  EN couple-months: primary earner E and spouse N at m-1, both observed at m. Primary earner's transition EE, EU, EN;
  spouse's NE, NU, NN. AWE = P(NE or NU | EU) - P(NE or NU | EE), same month. Weighted by the wife's composite weight
  (30's couple weight). Estimated as the coefficient of EU in a weighted LPM on the EE + EU sample (= the difference of
  weighted means), s.e. clustered by household; by the spouse's age (26-35, 36-45, 46-55, 56-62) from one fully
  interacted regression (age-group FE, EU x age group), with a Wald test of equal AWEs across ages.
  Variants: (a) the Elsby, Hobijn and Sahin (2015) correction for U/N classification error, which recodes the middle
  month of N-U-N to N and of U-N-U to U ("de-NUN-ification") wherever the three months are observed for the person
  (applied to each spouse's statuses at m-3 .. m+2, from the original codes), vs unadjusted; (b) all EU of the primary
  earner vs job-loser EU only (EU with PRUNTYPE 1-3; other EU dropped); (c) BGN's window (all months used, including
  the correction's look-ahead month, up to February 2020) vs the full 1994-2023; (d) sex-neutral vs wives only (and
  husbands only, csv).
  Eq. (1) leads and lags: spouse N at t-1; outcome = spouse enters the labor force (E or U) at t; regressor = primary
  earner moves E -> U between t+j-1 and t+j (j = -2..2), against primary earners employed in every month of the window
  (from min(t-1, t+j-1) to max(t, t+j)); primary earners who move to N are dropped; the treated earner's status after
  the EU month is unrestricted. One regression per j; unweighted LPM; controls as BGN (state FE, year FE, calendar-month
  FE, primary earner's sex and race, education of both, number of own children 1 / 2 / 3+; BGN's quarterly state
  unemployment rate is not in the panel) and, as a second specification, state x year-month FE (which absorbs it).
PART (2): Paper A's joint job loss by age
  30's sample (both employed at t; husband becomes a job loser at t+1, H = 1, vs stays employed, H = 0); wife's
  same-month job loss; LPM with state x year-month FE by husband's and by wife's age group (20-25 added), excluding
  temporary layoffs as in 37 (husband's loss other than on layoff, wife's loss not on layoff), excluding 2020-21, and in
  BGN's window; pooled H x age-group regressions with Wald tests; the joint EU-EU rate and its ratio to independence;
  shares of couple-months in EE / EN / NE / EU / UU / UN / NN by age (all couple-months, weighted).
Every regression: *** p<0.01, ** p<0.05, * p<0.1; s.e. clustered by household. Associations, not causal effects.
Writes output/cps_awe_by_age.md, .csv (every estimate), .png.
Run from IGE/: ../.venv/Scripts/python.exe -I 50.CPSAddedWorkerByAge.py [--panel60 = use 30's 20-60 cache]
"""
import importlib.util
import inspect
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))                 # -I drops the script directory from sys.path

import numpy as np                            # noqa: E402
import pandas as pd                           # noqa: E402
from scipy.stats import chi2, norm            # noqa: E402

from common import DATA, OUT, stars           # noqa: E402


def _load30():
    spec = importlib.util.spec_from_file_location("cps30", HERE / "30.CPSJointJobLoss.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


m30 = _load30()
AGE_MAX = 62
CACHE62 = DATA / "cps_couples_panel_2062.pkl"
T_FEB2020 = (2020 - 1994) * 12 + 1            # last month used in BGN's window ("1994 until early 2020")
OFFS = [-2, -1, 0, 1, 2, 3]
AGEG = [(26, 35), (36, 45), (46, 55), (56, AGE_MAX)]
AGEG2 = [(20, 25)] + AGEG
ROWS = []

# BGN Tables 1-2 and Figs. 1-2 (percent / pp); age 56-65 in BGN
BGN = {"All": dict(EE=97.16, EU=1.00, NE=(5.93, 7.65), NU=(1.61, 5.44), NN=(92.46, 86.92), AWE=5.55, N=1280562),
       "26-35": dict(EE=97.67, EU=1.22, NE=(6.53, 8.96), NU=(1.97, 6.66), NN=(91.50, 84.37), AWE=7.12, N=313017),
       "36-45": dict(EE=97.77, EU=1.01, NE=(6.64, 8.97), NU=(1.86, 6.36), NN=(91.50, 84.67), AWE=6.83, N=349892),
       "46-55": dict(EE=97.30, EU=0.92, NE=(6.04, 7.41), NU=(1.62, 4.82), NN=(92.34, 87.77), AWE=4.57, N=314078),
       "56-62": dict(EE=95.72, EU=0.81, NE=(4.26, 3.77), NU=(0.89, 2.78), NN=(94.84, 93.45), AWE=1.40, N=303575)}
BGN_FIG = {"All": {-2: 3.3, -1: 2.6, 0: 5.8, 1: 2.0, 2: 1.7}, "26-35": {-2: 3.7, -1: 3.0, 0: 7.3, 1: 1.6, 2: 2.0},
           "56-62": {-2: 2.6, -1: -0.19, 0: 1.5, 1: 2.4, 2: 0.31}}


# ================================================================ panel (30's builder, ages 20-62)
def build_panel62():
    if CACHE62.exists():
        return pd.read_pickle(CACHE62)
    src = inspect.getsource(m30.read_month)
    old = "p.age.between(20, 60)"
    assert src.count(old) == 1, "30's read_month changed: age filter not found"
    orig = m30.read_month
    exec(src.replace(old, f"p.age.between(20, {AGE_MAX})"), m30.__dict__)   # same function, upper bound 62
    try:
        return m30.build_panel(m30.YEARS, CACHE62)
    finally:
        m30.read_month = orig


def col(sp, o):
    return f"{sp}_s" if o == 0 else f"{sp}_s{o:+d}"


def lab(s):
    s = np.asarray(s)
    return np.select([s == 1, (s == 2) | (s == 3), s == 4], [1, 2, 4], 0)


def ehs(P, sp):
    """Elsby-Hobijn-Sahin (2015) recode of each person's status window: NUN -> NNN, UNU -> UUU (from original codes,
    middle months -1..+2 where both neighbours are observed). Recoded U carries code 3 (reason unknown)."""
    raw = {o: P[col(sp, o)].to_numpy() for o in OFFS}
    L = {o: lab(raw[o]) for o in OFFS}
    out = {}
    for o in OFFS:
        x = raw[o].copy()
        if o - 1 in L and o + 1 in L:
            nun = (L[o - 1] == 4) & (L[o] == 2) & (L[o + 1] == 4)
            unu = (L[o - 1] == 2) & (L[o] == 4) & (L[o + 1] == 2)
            x[nun], x[unu] = 4, 3
        out[o] = x.astype("int8")
    return out


# ================================================================ estimator (weighted, FE, full vcov)
def reg(d, y, xs, fe=None, extra=None, w=None, cl="hh"):
    """(W)LS of y on xs (+ dummy frame `extra`), absorbing one FE (weighted demeaning); household-clustered vcov."""
    Y = d[y].to_numpy(float)
    X = d[xs].to_numpy(float)
    names = list(xs)
    if extra is not None:
        X = np.column_stack([X, extra.to_numpy(float)])
        names += list(extra.columns)
    W = np.ones(len(d)) if w is None else d[w].to_numpy(float)
    if fe:
        codes, uniq = pd.factorize(pd.MultiIndex.from_frame(d[fe]) if len(fe) > 1 else d[fe[0]])
        G0 = len(uniq)
        sw = np.bincount(codes, weights=W, minlength=G0)

        def dm(a):
            return a - (np.bincount(codes, weights=W * a, minlength=G0) / np.maximum(sw, 1e-300))[codes]
        Y = dm(Y)
        X = np.column_stack([dm(X[:, j]) for j in range(X.shape[1])])
        nfe = G0
    else:
        X = np.column_stack([X, np.ones(len(X))])
        names += ["const"]
        nfe = 0
    keep = (W[:, None] * X * X).sum(0) > 1e-9
    X, names = X[:, keep], [n for n, k in zip(names, keep) if k]
    XtWX = X.T @ (W[:, None] * X)
    A = np.linalg.pinv(XtWX)
    b = A @ (X.T @ (W * Y))
    u = Y - X @ b
    N, K = X.shape
    g, gu = pd.factorize(d[cl])
    G = len(gu)
    S = np.column_stack([np.bincount(g, weights=W * X[:, j] * u, minlength=G) for j in range(K)])
    V = A @ (S.T @ S) @ A * (G / (G - 1)) * ((N - 1) / max(N - K, 1))
    return dict(b=pd.Series(b, names), V=pd.DataFrame(V, names, names), N=N, G=G, nfe=nfe)


def pval(b, se):
    return 2 * norm.sf(abs(b / se)) if se > 0 else np.nan


def se_(r, x):
    return float(np.sqrt(max(r["V"].loc[x, x], 0)))


def cell(b, se, scale=100, nd=2):
    """coef*** (s.e.; p), in percentage points by default."""
    p = pval(b, se)
    pv = "p<0.001" if p < 0.001 else f"p={p:.3f}"
    return f"{scale * b:.{nd}f}{stars(p)} ({scale * se:.{nd}f}; {pv})"


def cellx(r, x, scale=100, nd=2):
    return cell(r["b"][x], se_(r, x), scale, nd) if x in r["b"] else ""


def lincom(r, wts):
    """sum_k w_k b_k with s.e."""
    names = [k for k in wts if k in r["b"]]
    a = np.array([wts[k] for k in names])
    b = float(a @ r["b"][names].to_numpy())
    se = float(np.sqrt(max(a @ r["V"].loc[names, names].to_numpy() @ a, 0)))
    return b, se


def wald_equal(r, xs):
    """Wald test that the coefficients xs are equal: chi2 statistic, df, p."""
    xs = [x for x in xs if x in r["b"]]
    if len(xs) < 2:
        return np.nan, 0, np.nan
    R = np.zeros((len(xs) - 1, len(xs)))
    for i in range(len(xs) - 1):
        R[i, 0], R[i, i + 1] = 1, -1
    bb = R @ r["b"][xs].to_numpy()
    VV = R @ r["V"].loc[xs, xs].to_numpy() @ R.T
    st = float(bb @ np.linalg.pinv(VV) @ bb)
    return st, len(xs) - 1, float(chi2.sf(st, len(xs) - 1))


def wmean(x, w):
    x, w = np.asarray(x, float), np.asarray(w, float)
    ok = ~np.isnan(x) & ~np.isnan(w)
    return float(np.sum(x[ok] * w[ok]) / np.sum(w[ok])) if ok.any() else np.nan


def record(table, sample, outcome, spec, r, x, **extra):
    se = se_(r, x)
    ROWS.append(dict(table=table, sample=sample, outcome=outcome, spec=spec, regressor=x, coef=float(r["b"][x]),
                     se_hh=se, p_hh=pval(float(r["b"][x]), se), n=r["N"], clusters_hh=r["G"], n_fe=r["nfe"], **extra))


def agelab(a, b):
    return f"{a}-{b}"


def agegroup(age, groups):
    return pd.Series(np.select([(age >= a) & (age <= b) for a, b in groups], [agelab(a, b) for a, b in groups],
                               ""), index=age.index)


# ================================================================ part (1): EN couples
def en_frame(P):
    """Long frame, one row per couple-month with one spouse not employed at the base month b, in both orientations
    (p = primary earner candidate, q = spouse). Raw (_s) and EHS-adjusted (_a) statuses at offsets -2..+3."""
    m = (P.h_s.isin([2, 3, 4]) | P.w_s.isin([2, 3, 4])).to_numpy()
    Q = P.loc[m].reset_index(drop=True)
    adj = {sp: ehs(Q, sp) for sp in ("h", "w")}
    base = pd.DataFrame({"t": Q.t.values, "hh": Q.hh.values, "state": Q.state.values, "sm": Q.sm.values,
                         "w": Q.w.values, "year": Q.year.values, "nkid": Q.nkid.values,
                         "black": (Q.h_race == 2).astype("int8").values,
                         "orace": (~Q.h_race.isin([1, 2])).astype("int8").values})
    parts = []
    for p, q, fem in (("h", "w", 0), ("w", "h", 1)):
        d = base.copy()
        d["orient"] = "wife spouse" if q == "w" else "husband spouse"
        d["p_female"] = np.int8(fem)
        for v in ("age", "edg"):
            d[f"p_{v}"], d[f"q_{v}"] = Q[f"{p}_{v}"].values, Q[f"{q}_{v}"].values
        for o in OFFS:
            d[f"p_s{o}"], d[f"q_s{o}"] = Q[col(p, o)].values, Q[col(q, o)].values
            d[f"p_a{o}"], d[f"q_a{o}"] = adj[p][o], adj[q][o]
        keep = (d["q_s0"] == 4) | (d["q_a0"] == 4)
        parts.append(d[keep])
    L = pd.concat(parts, ignore_index=True)
    L["q_ageg"] = agegroup(L.q_age, AGEG)
    return L


def awe_sample(L, adj=True, bgn=True, orient="all", eu="all"):
    s = "a" if adj else "s"
    p0, q0, p1, q1 = L[f"p_{s}0"], L[f"q_{s}0"], L[f"p_{s}1"], L[f"q_{s}1"]
    m = (p0 == 1) & (q0 == 4) & (p1 >= 1) & (q1 >= 1)
    m &= L.p_age.between(26, AGE_MAX) & L.q_age.between(26, AGE_MAX)
    if bgn:
        m &= (L.t + 2) <= T_FEB2020
    if orient != "all":
        m &= L.orient == orient
    d = L.loc[m, ["t", "hh", "state", "sm", "w", "q_ageg", "q_age"]].copy()
    pp, qq = p1[m].to_numpy(), q1[m].to_numpy()
    d["pEE"], d["pEN"] = (pp == 1).astype("int8"), (pp == 4).astype("int8")
    d["pEU"] = (pp == 2).astype("int8") if eu == "jl" else np.isin(pp, [2, 3]).astype("int8")
    d["pEUo"] = ((pp == 3) if eu == "jl" else np.zeros(len(pp), bool)).astype("int8")   # other EU (dropped if jl)
    d["NE"], d["NU"], d["NN"] = (qq == 1).astype("int8"), np.isin(qq, [2, 3]).astype("int8"), (qq == 4).astype("int8")
    d["LF"] = (d.NE + d.NU).astype("int8")
    return d


def awe_cells(d):
    """BGN-format table cells (weighted, percent)."""
    w = d.w.to_numpy()
    out = dict(EE=100 * wmean(d.pEE, w), EU=100 * wmean(d.pEU, w), EN=100 * wmean(d.pEN, w), N=len(d),
               nEU=int(d.pEU.sum()))
    for g, sel in (("ee", d.pEE == 1), ("eu", d.pEU == 1)):
        for o in ("NE", "NU", "NN", "LF"):
            out[f"{o}_{g}"] = 100 * wmean(d.loc[sel, o], d.loc[sel, "w"])
    return out


def awe_regs(d, weighted=True):
    """Overall AWE (EU coefficient) and the fully interacted age version, for LF, NE, NU."""
    e = d[(d.pEE == 1) | (d.pEU == 1)].copy()
    e = e[e.q_ageg != ""]
    for a, b in AGEG:
        e[f"EU_{a}"] = (e.pEU * (e.q_ageg == agelab(a, b))).astype("int8")
    w = "w" if weighted else None
    res = {}
    for o in ("LF", "NE", "NU"):
        res[(o, "all")] = reg(e, o, ["pEU"], w=w)
        res[(o, "age")] = reg(e, o, [f"EU_{a}" for a, _ in AGEG], fe=["q_ageg"], w=w)
    return res


VARIANTS = [  # key, label, kwargs
    ("main", "BGN replication: sex-neutral, 1994-Feb 2020, EHS-adjusted, all EU",
     dict(adj=True, bgn=True, orient="all", eu="all")),
    ("unadj", "(1) unadjusted", dict(adj=False, bgn=True, orient="all", eu="all")),
    ("jl", "(1) job-loser EU only", dict(adj=True, bgn=True, orient="all", eu="jl")),
    ("full", "(1) 1994-2023", dict(adj=True, bgn=False, orient="all", eu="all")),
    ("wives", "Wives as spouse, 1994-Feb 2020, EHS, all EU", dict(adj=True, bgn=True, orient="wife spouse", eu="all")),
    ("wives_pa", "Wives, 1994-2023, unadjusted, job-loser EU (Paper A's definitions)",
     dict(adj=False, bgn=False, orient="wife spouse", eu="jl")),
    ("sn_pa", "Sex-neutral, 1994-2023, unadjusted, job-loser EU", dict(adj=False, bgn=False, orient="all", eu="jl")),
    ("husb", "Husbands as spouse, 1994-Feb 2020, EHS, all EU",
     dict(adj=True, bgn=True, orient="husband spouse", eu="all")),
]


def short(kw):
    return (f"{'sex-neutral' if kw['orient'] == 'all' else kw['orient']}; "
            f"{'1994-Feb 2020' if kw['bgn'] else '1994-2023'}; {'EHS' if kw['adj'] else 'unadjusted'}; "
            f"{'job-loser EU' if kw['eu'] == 'jl' else 'all EU'}")


# ---------------------------------------------------------------- Eq. (1) leads and lags
def eq1_sample(L, j, adj=True, bgn=True, orient="all", eu="all"):
    s = "a" if adj else "s"
    q0, q1 = L[f"q_{s}0"], L[f"q_{s}1"]
    m = (q0 == 4) & (q1 >= 1) & L.p_age.between(26, AGE_MAX) & L.q_age.between(26, AGE_MAX)
    lo, hi = min(j, 0), max(j + 1, 1)
    for o in range(lo, j + 1):                                  # employed up to the month before the transition
        m &= L[f"p_{s}{o}"] == 1
    tr = L[f"p_{s}{j + 1}"]
    treat = (tr == 2) if eu == "jl" else tr.isin([2, 3])
    ctrl = pd.Series(True, index=L.index)
    for o in range(j + 1, hi + 1):
        ctrl &= L[f"p_{s}{o}"] == 1
    m &= treat | ctrl
    if bgn:
        m &= (L.t + max(hi, 2)) <= T_FEB2020
    if orient != "all":
        m &= L.orient == orient
    d = L[m].copy()
    d["D"] = treat[m].astype("int8")
    d["LF"] = q1[m].isin([1, 2, 3]).astype("int8")
    return d


def eq1_controls(d):
    c = {"p_female": d.p_female, "black": d.black, "orace": d.orace}
    for sp in ("p", "q"):
        for k in (1, 2, 3):
            c[f"{sp}_ed{k}"] = (d[f"{sp}_edg"] == k).astype("int8")
    for k, lo in ((1, 1), (2, 2), (3, 3)):
        c[f"kid{k}"] = ((d.nkid == lo) if k < 3 else (d.nkid >= 3)).astype("int8")
    return pd.DataFrame(c, index=d.index)


def eq1_fe_dummies(d):
    yr = pd.get_dummies(d.year, prefix="y", drop_first=True, dtype="int8")
    mo = pd.get_dummies(((d.t + 1) % 12 + 1).astype(int), prefix="m", drop_first=True, dtype="int8")
    return pd.concat([yr, mo], axis=1)


# ================================================================ main
def main(panel60=False):
    OUT.mkdir(exist_ok=True)
    global AGE_MAX, AGEG, AGEG2
    if panel60:
        P = m30.build_panel()
        AGE_MAX = 60
        AGEG = [(26, 35), (36, 45), (46, 55), (56, 60)]
        AGEG2 = [(20, 25)] + AGEG
    else:
        P = build_panel62()
    rates = P.attrs.get("rates")
    P.attrs = {}
    P = m30.add_vars(P)
    oldest = agelab(*AGEG[-1])
    md = ["# The added-worker effect by age (Bacher, Grubener and Nord 2025) and joint job loss by age: CPS couples\n",
          f"Built by `IGE/50.CPSAddedWorkerByAge.py` (2026-10-18; definitions in its docstring) on Paper A's CPS couples "
          f"panel (30.CPSJointJobLoss.py's raw files and builder, here with both spouses aged 20-{AGE_MAX}: "
          f"{len(P):,} couple-months). BGN = Bacher, Grubener and Nord (2025, JME), Section 2. **Couples:** married, "
          "spouse present, opposite sex, naming each other (BGN: married or cohabiting, any sex, both 26-65); the raw "
          f"files stop at age 62, so BGN's oldest group 56-65 is {oldest} here. Probabilities weighted by the wife's "
          "composite weight. Cells: coefficient*** (s.e. clustered by household; p), in percentage points unless "
          "stated; *** p<0.01, ** p<0.05, * p<0.1. Associations, not causal effects.\n"]
    if rates is not None:
        md.append("Link-rate rule and dropped base months as in 30 (the 20-62 panel has the same household-ID breaks).\n")

    # ---------------------------------------------------------- (1) AWE
    L = en_frame(P)
    md.append("## 1. BGN's added-worker effect on Paper A's panel\n")
    md.append("EN couples: primary earner employed and spouse not in the labor force at m-1, both observed at m. "
              "AWE = P(spouse NE or NU | primary EU) - P(spouse NE or NU | primary EE), same month. The Elsby-Hobijn-"
              "Sahin (2015) correction recodes N-U-N to N-N-N and U-N-U to U-U-U in each spouse's status sequence where "
              "the three months are observed (it moves the spouse's status, never the primary earner's E -> U or "
              "E -> E). BGN's window: every month used up to February 2020 (their data run '1994 until early 2020').\n")
    samples, cells_, regs = {}, {}, {}
    for key, labl, kw in VARIANTS:
        d = awe_sample(L, **kw)
        samples[key] = d
        cells_[key] = {"All": awe_cells(d)}
        for a, b in AGEG:
            cells_[key][agelab(a, b)] = awe_cells(d[d.q_ageg == agelab(a, b)])
        regs[key] = awe_regs(d)
        for o in ("LF", "NE", "NU"):
            r = regs[key][(o, "all")]
            record("1_awe", f"{key}: All", o, short(kw), r, "pEU", **{f"cell_{k}": v for k, v in
                                                                       cells_[key]["All"].items()})
            ra = regs[key][(o, "age")]
            for a, b in AGEG:
                x = f"EU_{a}"
                if x in ra["b"]:
                    record("1_awe", f"{key}: spouse {agelab(a, b)}", o, short(kw), ra, x,
                           **{f"cell_{k}": v for k, v in cells_[key][agelab(a, b)].items()})
    # unweighted check of the main variant
    ru = awe_regs(samples["main"], weighted=False)
    for o in ("LF", "NE", "NU"):
        record("1_awe_unweighted", "main: All", o, "unweighted", ru[(o, "all")], "pEU")
        for a, _ in AGEG:
            if f"EU_{a}" in ru[(o, "age")]["b"]:
                record("1_awe_unweighted", f"main: spouse {a}", o, "unweighted", ru[(o, "age")], f"EU_{a}")

    # Table 1a: BGN format, main variant, with BGN's numbers
    md.append("### 1a. BGN Tables 1-2 format: main variant (sex-neutral, 1994-Feb 2020, EHS-adjusted, all EU)\n")
    md.append("Percent. 'Ours' = this panel; 'BGN' = their Table 1 (All) / Table 2 (by the spouse's age; their oldest "
              "group is 56-65). AWE row: EU coefficient of a weighted LPM (EE + EU sample), pp.\n")
    md.append("| | Ours: EE | Ours: EU | Ours: AWE | BGN: EE | BGN: EU | BGN: AWE |\n|---|---|---|---|---|---|---|")
    c = cells_["main"]
    for g in ["All"] + [agelab(a, b) for a, b in AGEG]:
        cg, bg = c[g], BGN.get(g if g != oldest else "56-62")
        if g == "All":
            rL, rE, rU = (regs["main"][(o, "all")] for o in ("LF", "NE", "NU"))
            xL = xE = xU = "pEU"
        else:
            rL, rE, rU = (regs["main"][(o, "age")] for o in ("LF", "NE", "NU"))
            xL = xE = xU = f"EU_{g.split('-')[0]}"
        md.append(f"| **{'All EN couples' if g == 'All' else 'Spouse aged ' + g}** | | | | | | |")
        md.append(f"| Primary earner's flow rate (EN {cg['EN']:.2f}%) | {cg['EE']:.2f} | {cg['EU']:.2f} | | "
                  f"{bg['EE']:.2f} | {bg['EU']:.2f} | |")
        md.append(f"| Spouse NE | {cg['NE_ee']:.2f} | {cg['NE_eu']:.2f} | {cellx(rE, xE)} | {bg['NE'][0]:.2f} | "
                  f"{bg['NE'][1]:.2f} | {bg['NE'][1] - bg['NE'][0]:.2f} |")
        md.append(f"| Spouse NU | {cg['NU_ee']:.2f} | {cg['NU_eu']:.2f} | {cellx(rU, xU)} | {bg['NU'][0]:.2f} | "
                  f"{bg['NU'][1]:.2f} | {bg['NU'][1] - bg['NU'][0]:.2f} |")
        md.append(f"| Spouse NN | {cg['NN_ee']:.2f} | {cg['NN_eu']:.2f} | | {bg['NN'][0]:.2f} | {bg['NN'][1]:.2f} | |")
        md.append(f"| **AWE (total)** | | | **{cellx(rL, xL)}** | | | **{bg['AWE']:.2f}** |")
        md.append(f"| N couple-months (N primary EU) | {cg['N']:,} ({cg['nEU']:,}) | | | {bg['N']:,} | | |")
    md.append("")

    # Tables 1b-1d: AWE regressions across variants
    shown = ["main", "unadj", "jl", "full", "wives", "wives_pa", "sn_pa"]
    olab = {"LF": "spouse enters the labor force (NE or NU)", "NE": "spouse N -> E", "NU": "spouse N -> U"}
    for tab, o in (("1b", "LF"), ("1c", "NE"), ("1d", "NU")):
        md.append(f"### {tab}. AWE regressions, outcome: {olab[o]}, same month (pp)\n")
        md.append("One weighted LPM per column on the EE + EU sample; rows 'EU x spouse aged ...' come from one fully "
                  "interacted regression per column (age-group FE); 'EU, all ages' from a separate regression.\n")
        md.append("| | " + " | ".join(f"({i + 1}) {olab[o]}" for i in range(len(shown))) + " |")
        md.append("|---" * (len(shown) + 1) + "|")
        md.append("| Primary earner EU (vs EE), all ages | " + " | ".join(
            cellx(regs[k][(o, "all")], "pEU") for k in shown) + " |")
        for a, b in AGEG:
            md.append(f"| EU x spouse aged {agelab(a, b)} | " + " | ".join(
                cellx(regs[k][(o, "age")], f"EU_{a}") for k in shown) + " |")
        diffs, walds = [], []
        for k in shown:
            ra = regs[k][(o, "age")]
            bd, sd = lincom(ra, {f"EU_{AGEG[-1][0]}": 1, f"EU_{AGEG[0][0]}": -1})
            diffs.append(cell(bd, sd))
            st, df, pw = wald_equal(ra, [f"EU_{a}" for a, _ in AGEG])
            walds.append(f"chi2({df}) = {st:.1f}; {'p<0.001' if pw < 0.001 else f'p={pw:.3f}'}")
            ROWS.append(dict(table=f"{tab}_age_tests", sample=k, outcome=o, regressor=f"EU {oldest} - EU 26-35",
                             coef=bd, se_hh=sd, p_hh=pval(bd, sd), wald_chi2=st, wald_df=df, wald_p=pw))
        md.append(f"| Difference: {oldest} minus 26-35 | " + " | ".join(diffs) + " |")
        md.append("| Wald test: equal across the four ages | " + " | ".join(walds) + " |")
        md.append("| Couples | " + " | ".join(
            "sex-neutral" if dict(VARIANTS_KW[k])["orient"] == "all" else "wife = spouse" for k in shown) + " |")
        md.append("| Years | " + " | ".join("1994-Feb 2020" if dict(VARIANTS_KW[k])["bgn"] else "1994-2023"
                                            for k in shown) + " |")
        md.append("| EHS correction | " + " | ".join("yes" if dict(VARIANTS_KW[k])["adj"] else "no" for k in shown)
                  + " |")
        md.append("| Primary earner's EU | " + " | ".join("job loser" if dict(VARIANTS_KW[k])["eu"] == "jl"
                                                         else "all" for k in shown) + " |")
        md.append("| Fixed effects | " + " | ".join("none (age-group FE in the age rows)" for _ in shown) + " |")
        md.append("| N (EE + EU) / clusters | " + " | ".join(
            f"{regs[k][(o, 'all')]['N']:,} / {regs[k][(o, 'all')]['G']:,}" for k in shown) + " |")
        md.append("| Mean outcome under EE, all ages (%) | " + " | ".join(
            f"{cells_[k]['All'][o + '_ee']:.2f}" for k in shown) + " |\n")
    # husbands-as-spouse and unweighted, briefly
    rh = regs["husb"][("LF", "all")]
    md.append(f"Husbands as the non-participating spouse (wife employed; sex-neutral sample's other half): AWE "
              f"{cellx(rh, 'pEU')}, N {rh['N']:,}; by his age " + "; ".join(
                  f"{agelab(a, b)} {cellx(regs['husb'][('LF', 'age')], f'EU_{a}')}" for a, b in AGEG) +
              f". Unweighted main variant: AWE {cellx(ru[('LF', 'all')], 'pEU')}; by age " + "; ".join(
                  f"{agelab(a, b)} {cellx(ru[('LF', 'age')], f'EU_{a}')}" for a, b in AGEG) + ".\n")

    # Eq. (1)
    md.append("### 1e. BGN Eq. (1): leads and lags (main variant; unweighted LPM; pp)\n")
    md.append("Outcome: the non-participating spouse (N at t-1) enters the labor force at t. Column j: the primary earner "
              "moves E -> U between t+j-1 and t+j (j < 0: he lost the job before her move; j > 0: he loses it after), "
              "against primary earners employed in every month of the window. One regression per cell. Spec A: BGN's "
              "controls (state FE; year and calendar-month dummies; primary earner's sex and race; education of both; "
              "number of own children; no state unemployment rate). Spec B: state x year-month FE + the same "
              "individual controls. BGN row: their Fig. 1 / Fig. 2 (56-65 for the oldest).\n")
    js = [-2, -1, 0, 1, 2]
    jl_ = {-2: "lost two months ago", -1: "lost last month", 0: "this month", 1: "loses next month",
           2: "loses in two months"}
    md.append("| | " + " | ".join(f"({i + 1}) spouse enters LF at t; j={j:+d} ({jl_[j]})" for i, j in enumerate(js))
              + " |")
    md.append("|---" * (len(js) + 1) + "|")
    E1 = {j: eq1_sample(L, j) for j in js}
    eq1res = {}
    for g in ["All"] + [agelab(a, b) for a, b in AGEG]:
        md.append(f"| **{'All EN couples' if g == 'All' else 'Spouse aged ' + g}** |" + " |" * len(js))
        for spn, spec in (("A", "state FE + year + month + controls"), ("B", "state x year-month FE + controls")):
            cl, nn = [], []
            for j in js:
                d = E1[j] if g == "All" else E1[j][E1[j].q_ageg == g]
                if d.D.sum() < 20:
                    cl.append("n/a"), nn.append(f"{len(d):,}")
                    continue
                ctl = eq1_controls(d)
                if spn == "A":
                    r = reg(d, "LF", ["D"], fe=["state"], extra=pd.concat([ctl, eq1_fe_dummies(d)], axis=1))
                else:
                    r = reg(d, "LF", ["D"], fe=["sm"], extra=ctl)
                eq1res[(g, spn, j)] = r
                record("1e_eq1", g, f"spouse enters LF at t (j={j:+d})", spec, r, "D",
                       mean_ctrl=float(d.loc[d.D == 0, "LF"].mean()), n_treat=int(d.D.sum()))
                cl.append(cellx(r, "D"))
                nn.append(f"{r['N']:,} / {int(d.D.sum()):,}")
            md.append(f"| Primary earner E->U at t+j, spec {spn} | " + " | ".join(cl) + " |")
            if spn == "A":
                md.append("| N / N treated | " + " | ".join(nn) + " |")
        bg = BGN_FIG.get(g if g != oldest else "56-62")
        if bg:
            md.append("| BGN (Fig. 1 / 2) | " + " | ".join(f"{bg[j]:.2f}" for j in js) + " |")
    md.append("| Fixed effects | " + " | ".join("A: state + year + month; B: state x year-month" for _ in js) + " |\n")

    # ---------------------------------------------------------- (2) joint job loss by age
    md.append("## 2. Paper A's joint job loss by the same age groups\n")
    md.append("30's sample: both spouses employed at t; H = 1 if the husband becomes a job loser at t+1 (unemployed, "
              "reason job loser on layoff / other job loser / temporary job ended), H = 0 if he stays employed. Outcome: "
              "the wife becomes a job loser at t+1. One LPM with state x year-month FE per cell. Columns: (1) all; (2) "
              "excluding temporary layoffs as in 37 (his loss other than on layoff, wives on layoff at t+1 dropped, "
              "outcome = her loss other than on layoff); (3) (1) excluding 2020-21; (4) (1) in BGN's window "
              "(1994-Feb 2020).\n")
    W0 = m30.jl_sample(P, 0)
    W0["y"] = (W0["w_s+1"] == 2).astype("int8")
    W0["ynl"] = ((W0["w_s+1"] == 2) & W0["w_unt+1"].isin([2, 3])).astype("int8")
    W0["hage"], W0["wage"] = agegroup(W0.h_age, AGEG2), agegroup(W0.w_age, AGEG2)
    notlay = (W0.H == 0) | W0["h_unt+1"].isin([2, 3])
    wnl = ~((W0["w_s+1"] == 2) & (W0["w_unt+1"] == 1))
    cols = [("wife job loser at t+1", W0, "y"), ("wife job loser not on layoff (his loss not on layoff)",
                                                  W0[notlay & wnl], "ynl"),
            ("wife job loser at t+1, excl. 2020-21", W0[W0.covid == 0], "y"),
            ("wife job loser at t+1, 1994-Feb 2020", W0[(W0.t + 1) <= T_FEB2020], "y")]
    md.append("| | " + " | ".join(f"({i + 1}) {h}" for i, (h, _, _) in enumerate(cols)) + " |")
    md.append("|---" * (len(cols) + 1) + "|")
    jlres = {}
    panels = [("All couples", None, None)]
    panels += [(f"Husband aged {agelab(a, b)}", "hage", agelab(a, b)) for a, b in AGEG2]
    panels += [(f"Wife aged {agelab(a, b)}", "wage", agelab(a, b)) for a, b in AGEG2]
    for pn, gv, gl in panels:
        cl, mn, nn = [], [], []
        for h, d, yv in cols:
            dd = d if gv is None else d[d[gv] == gl]
            if dd.H.sum() < 20 or dd.loc[dd.H == 1, yv].sum() == 0:
                cl.append("n/a"), mn.append(""), nn.append(f"{len(dd):,}")
                continue
            r = reg(dd, yv, ["H"], fe=["sm"])
            a0, a1 = dd[dd.H == 0], dd[dd.H == 1]
            p0, p1 = wmean(a0[yv], a0.w), wmean(a1[yv], a1.w)
            ph = wmean(dd.H, dd.w)
            jlres[(pn, h)] = dict(r=r, p0=p0, p1=p1, ph=ph)
            record("2_joint_loss_age", pn, h, "state x ym FE", r, "H", p0=p0, p1=p1, ratio=p1 / p0, p_h=ph,
                   n_h1=int(dd.H.sum()), n_joint=int(a1[yv].sum()))
            cl.append(cellx(r, "H", 100, 2))
            mn.append(f"{100 * p0:.2f} / {100 * p1:.2f} (ratio {p1 / p0:.1f})")
            nn.append(f"{r['N']:,} / {int(dd.H.sum()):,} / {int(a1[yv].sum()):,}")
        md.append(f"| **{pn}** |" + " |" * len(cols))
        md.append("| Husband becomes job loser (t+1), pp | " + " | ".join(cl) + " |")
        md.append("| % wife job loser: H = 0 / H = 1 (weighted) | " + " | ".join(mn) + " |")
        md.append("| N / N(H = 1) / joint events | " + " | ".join(nn) + " |")
    md.append("| Fixed effects | " + " | ".join("state x year-month" for _ in cols) + " |")
    md.append("| Clusters | " + " | ".join("household" for _ in cols) + " |\n")

    # pooled interaction tests
    md.append("### 2b. Does the joint-loss excess change with age? Pooled H x age-group regressions (pp)\n")
    md.append("One LPM per column: wife's outcome on H x age-group dummies (26-35 ... oldest; ages 20-25 dropped) with "
              "age-group dummies and state x year-month FE; 'H x (age - 40) / 10' from a separate regression with H, "
              "age, H x age (linear in the age of the spouse named in the header).\n")
    pc = []
    for who, gv, av in (("husband's", "hage", "h_age"), ("wife's", "wage", "w_age")):
        for h, d, yv in cols[:2]:
            pc.append((f"{h}; by {who} age", d, yv, gv, av))
    md.append("| | " + " | ".join(f"({i + 1}) {h}" for i, (h, _, _, _, _) in enumerate(pc)) + " |")
    md.append("|---" * (len(pc) + 1) + "|")
    rows_ = {f"H x {agelab(a, b)}": [] for a, b in AGEG}
    dif, wal, lin, nn = [], [], [], []
    for h, d, yv, gv, av in pc:
        dd = d[d[gv].isin([agelab(a, b) for a, b in AGEG])].copy()
        xs, gd = [], {}
        for a, b in AGEG:
            dd[f"H_{a}"] = (dd.H * (dd[gv] == agelab(a, b))).astype("int8")
            xs.append(f"H_{a}")
            if (a, b) != AGEG[0]:
                gd[f"g_{a}"] = (dd[gv] == agelab(a, b)).astype("int8")
        r = reg(dd, yv, xs, fe=["sm"], extra=pd.DataFrame(gd, index=dd.index))
        for (a, b), x in zip(AGEG, xs):
            rows_[f"H x {agelab(a, b)}"].append(cellx(r, x))
            record("2b_age_interactions", h, yv, "state x ym FE", r, x)
        bd, sd = lincom(r, {xs[-1]: 1, xs[0]: -1})
        dif.append(cell(bd, sd))
        st, df, pw = wald_equal(r, xs)
        wal.append(f"chi2({df}) = {st:.1f}; {'p<0.001' if pw < 0.001 else f'p={pw:.3f}'}")
        ROWS.append(dict(table="2b_age_tests", sample=h, outcome=yv, regressor=f"H x {oldest} - H x 26-35", coef=bd,
                         se_hh=sd, p_hh=pval(bd, sd), wald_chi2=st, wald_df=df, wald_p=pw))
        dd["A10"] = (dd[av] - 40) / 10
        dd["HA"] = dd.H * dd.A10
        rl = reg(dd, yv, ["H", "HA", "A10"], fe=["sm"])
        record("2b_age_linear", h, yv, "state x ym FE", rl, "HA")
        lin.append(cellx(rl, "HA"))
        nn.append(f"{r['N']:,}")
    for k, v in rows_.items():
        md.append(f"| {k} | " + " | ".join(v) + " |")
    md.append(f"| Difference: {oldest} minus 26-35 | " + " | ".join(dif) + " |")
    md.append("| Wald test: equal across the four ages | " + " | ".join(wal) + " |")
    md.append("| H x (age - 40) / 10 (separate regression) | " + " | ".join(lin) + " |")
    md.append("| Fixed effects | " + " | ".join("state x year-month + age group" for _ in pc) + " |")
    md.append("| N | " + " | ".join(nn) + " |\n")

    # joint EU-EU rate and joint states by age
    md.append("### 2c. Joint job-loss rate and couples' joint labor-market states by age\n")
    md.append("Joint rate: among couples both employed at t and both observed at t+1, % of couple-months in which both "
              "become job losers at t+1, and its ratio to the product of the two marginal rates (independence). States: "
              "all couple-months with both statuses valid, weighted; first letter = husband, second = wife; EU / UN pool "
              "both orders.\n")
    A = P[(P.h_s >= 1) & (P.w_s >= 1)]
    hl, wl = lab(A.h_s), lab(A.w_s)
    st_ = {"EE": (hl == 1) & (wl == 1), "EN (wife N)": (hl == 1) & (wl == 4), "NE (husband N)": (hl == 4) & (wl == 1),
           "EU (either)": ((hl == 1) & (wl == 2)) | ((hl == 2) & (wl == 1)), "UU": (hl == 2) & (wl == 2),
           "UN (either)": ((hl == 2) & (wl == 4)) | ((hl == 4) & (wl == 2)), "NN": (hl == 4) & (wl == 4)}
    J = P[(P.h_s == 1) & (P.w_s == 1) & (P["h_s+1"] >= 1) & (P["w_s+1"] >= 1)]
    hj, wj = (J["h_s+1"] == 2).to_numpy(), (J["w_s+1"] == 2).to_numpy()
    md.append("| | " + " | ".join(["% both job losers at t+1 (EE couples)", "Ratio to independence",
                                    "% husband job loser", "% wife job loser"] + [f"% {k}" for k in st_]) + " |")
    md.append("|---" * (len(st_) + 5) + "|")
    for who, av in (("husband", "h_age"), ("wife", "w_age")):
        md.append(f"| **By {who}'s age** |" + " |" * (len(st_) + 4))
        for a, b in [(20, AGE_MAX)] + AGEG2:
            gj = J[av].between(a, b).to_numpy()
            ww = J.w.to_numpy()[gj]
            pb, ph, pw = wmean(hj[gj] & wj[gj], ww), wmean(hj[gj], ww), wmean(wj[gj], ww)
            ga = A[av].between(a, b).to_numpy()
            shares = {k: 100 * wmean(v[ga], A.w.to_numpy()[ga]) for k, v in st_.items()}
            ROWS.append(dict(table="2c_states", sample=f"{who} {a}-{b}", outcome="joint rate / states",
                             p_both=pb, p_h=ph, p_w=pw, ratio_indep=pb / (ph * pw), n_ee=int(gj.sum()),
                             n_both=int((hj[gj] & wj[gj]).sum()), n_all=int(ga.sum()),
                             **{f"share_{k}": v for k, v in shares.items()}))
            md.append(f"| {who.capitalize()} {a}-{b} | {100 * pb:.4f} | {pb / (ph * pw):.1f} | {100 * ph:.2f} | "
                      f"{100 * pw:.2f} | " + " | ".join(f"{v:.2f}" for v in shares.values()) + " |")
    md.append("")

    # ---------------------------------------------------------- (3) summary
    def awe_age(k):
        ra = regs[k][("LF", "age")]
        return [(float(ra["b"][f"EU_{a}"]), se_(ra, f"EU_{a}")) for a, _ in AGEG]
    mm = awe_age("main")
    rmain = regs["main"][("LF", "all")]
    jw = [jlres.get((f"Wife aged {agelab(a, b)}", cols[0][0])) for a, b in AGEG]
    jh = [jlres.get((f"Husband aged {agelab(a, b)}", cols[0][0])) for a, b in AGEG]
    t_awe = [r for r in ROWS if r["table"] == "1b_age_tests" and r["sample"] == "main"][0]
    t_jw = [r for r in ROWS if r["table"] == "2b_age_tests" and r["sample"].endswith("wife's age")
            and r["outcome"] == "y"][0]
    t_jh = [r for r in ROWS if r["table"] == "2b_age_tests" and r["sample"].endswith("husband's age")
            and r["outcome"] == "y"][0]
    md.append("## 3. Summary\n")
    md.append(f"- **AWE, overall:** {cell(float(rmain['b']['pEU']), se_(rmain, 'pEU'))} pp in BGN's window and "
              f"definitions (BGN 5.55).")
    md.append("- **AWE by the spouse's age (main variant):** " + "; ".join(
        f"{agelab(a, b)} {cell(*mm[i])}" for i, (a, b) in enumerate(AGEG)) + " (BGN 7.12 / 6.83 / 4.57 / 1.40). "
        f"Oldest minus youngest {cell(t_awe['coef'], t_awe['se_hh'])}; equality across ages p="
        f"{t_awe['wald_p']:.3g}.")
    md.append("- **Joint job loss by the wife's age (excess, state x month FE):** " + "; ".join(
        f"{agelab(a, b)} {cellx(x['r'], 'H')} (ratio {x['p1'] / x['p0']:.1f})" for (a, b), x in zip(AGEG, jw) if x)
        + f". Oldest minus 26-35 {cell(t_jw['coef'], t_jw['se_hh'])}; equality p={t_jw['wald_p']:.3g}.")
    md.append("- **By the husband's age:** " + "; ".join(
        f"{agelab(a, b)} {cellx(x['r'], 'H')} (ratio {x['p1'] / x['p0']:.1f})" for (a, b), x in zip(AGEG, jh) if x)
        + f". Oldest minus 26-35 {cell(t_jh['coef'], t_jh['se_hh'])}; equality p={t_jh['wald_p']:.3g}.")
    nl = {who: [r for r in ROWS if r["table"] == "2b_age_tests" and r["sample"].endswith(f"{who} age")
                and r["outcome"] == "ynl"][0] for who in ("husband's", "wife's")}
    md.append("- **Excluding temporary layoffs** (his loss not on layoff, her loss not on layoff): oldest minus 26-35 "
              + "; ".join(f"by {who} age {cell(r['coef'], r['se_hh'])}, equality p={r['wald_p']:.3g}"
                          for who, r in nl.items())
              + ". The AWE falls with age in every variant; the joint-loss excess does not fall with age (it rises "
              "for all job losses, through losses on layoff, and is flat for losses other than on layoff).\n")
    (OUT / "cps_awe_by_age.md").write_text("\n".join(md), encoding="utf-8")
    out = pd.DataFrame(ROWS)
    out["stars"] = out["p_hh"].map(lambda p: stars(p) if pd.notna(p) else "")
    out.to_csv(OUT / "cps_awe_by_age.csv", index=False)
    plot(mm, jw, jh, oldest, OUT / "cps_awe_by_age.png")
    print("\n".join(md))


VARIANTS_KW = {k: kw for k, _, kw in VARIANTS}


# ================================================================ figure
def plot(mm, jw, jh, oldest, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ink, ink2, grid, surf = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    blue, orange = "#2a78d6", "#eb6834"
    labs = [agelab(a, b) for a, b in AGEG]
    x = np.arange(len(labs))
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.8), facecolor=surf)
    for ax in axs:
        ax.set_facecolor(surf)
        ax.grid(axis="y", color=grid, lw=0.8)
        ax.set_axisbelow(True)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        for sp in ("left", "bottom"):
            ax.spines[sp].set_color(grid)
        ax.tick_params(colors=ink2, labelsize=9)
        ax.axhline(0, color=ink2, lw=0.8)
        ax.set_xticks(x)
    ax = axs[0]
    b = np.array([100 * v[0] for v in mm])
    s = np.array([100 * v[1] for v in mm])
    ax.errorbar(x - 0.08, b, yerr=1.96 * s, color=blue, lw=2, marker="o", ms=8, capsize=0,
                label="Paper A's CPS panel (EHS-adjusted, 1994-Feb 2020)")
    ax.plot(x + 0.08, [7.12, 6.83, 4.57, 1.40], color=orange, lw=2, marker="s", ms=8, ls="--",
            label="Bacher, Grubener and Nord (2025), Table 2")
    ax.set_xticklabels(labs[:-1] + [f"{oldest}\n(BGN 56-65)"])
    ax.set_xlabel("age of the non-participating spouse", color=ink2)
    ax.set_ylabel("added-worker effect, pp (95% CI)", color=ink2)
    ax.set_title("A. Non-participating spouse: entry when the earner loses the job", fontsize=10, color=ink, loc="left")
    ax.legend(frameon=False, fontsize=8, labelcolor=ink2)
    ax = axs[1]
    for sh, dat, colr, mk, nm in ((-0.08, jw, blue, "o", "by the wife's age"),
                                  (0.08, jh, orange, "s", "by the husband's age")):
        ok = [i for i, v in enumerate(dat) if v]
        bb = [100 * dat[i]["r"]["b"]["H"] for i in ok]
        ss = [100 * se_(dat[i]["r"], "H") for i in ok]
        ax.errorbar(x[ok] + sh, bb, yerr=1.96 * np.array(ss), color=colr, lw=2, marker=mk, ms=8, capsize=0, label=nm)
    ax.set_xticklabels(labs)
    ax.set_xlabel("age group", color=ink2)
    ax.set_ylabel("excess same-month job loss of the wife, pp (95% CI)", color=ink2)
    ax.set_title("B. Working wife: same-month job loss when he loses his", fontsize=10, color=ink, loc="left")
    ax.legend(frameon=False, fontsize=8, labelcolor=ink2, loc="upper left")
    fig.text(0.01, 0.005, "CPS basic monthly (Census API), married couples aged 20-62. A: EN couples, AWE = P(spouse "
             "enters LF | primary EU) - P(... | EE). B: both employed; LPM with state x year-month FE, 1994-2023. "
             "Household-clustered CIs.", fontsize=7.5, color=ink2)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(path, dpi=160, facecolor=surf)
    plt.close(fig)


def plot_paper(path):
    """Paper A figure (Fable's figure 6, proposals/fable_event_study_figures_paperA.md), drawn from the saved
    output/cps_awe_by_age.csv (no re-estimation): A, AWE by the spouse's age (main variant) with BGN's Table 2;
    B, the wife's excess same-month job loss by her age, all losses and losses not on layoff. 95% CIs (household)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    d = pd.read_csv(OUT / "cps_awe_by_age.csv")
    blue, orange = "#2a78d6", "#eb6834"
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.2))
    q = d[(d.table == "1_awe") & (d.outcome == "LF") & d["sample"].str.startswith("main: spouse")]
    q = q.drop_duplicates("sample")
    x = np.arange(len(q))
    ax = axs[0]
    ax.errorbar(x - 0.06, 100 * q.coef, yerr=196 * q.se_hh, color=blue, lw=1.8, marker="o", ms=6, capsize=0,
                label="CPS couples, this paper")
    ax.plot(x + 0.06, [7.12, 6.83, 4.57, 1.40], color=orange, lw=1.5, marker="s", ms=6, ls="--", mfc="white",
            label="Bacher, Grubener and Nord (2025), Table 2")
    ax.set_xticks(x)
    ax.set_xticklabels([s.split("spouse ")[1] for s in q["sample"]])
    ax.set_xlabel("age of the non-participating spouse")
    ax.set_title("(a) Added-worker effect (pp)", fontsize=10)
    ax.legend(frameon=False, fontsize=8)
    ax = axs[1]
    for sh, outc, colr, mk, nm in ((-0.06, "wife job loser at t+1", blue, "o", "all job losses"),
                                   (0.06, "wife job loser not on layoff (his loss not on layoff)", orange, "s",
                                    "losses not on temporary layoff")):
        r = d[(d.table == "2_joint_loss_age") & (d.outcome == outc) & d["sample"].str.startswith("Wife aged")]
        r = r.drop_duplicates("sample")
        xx = np.arange(len(r))
        ax.errorbar(xx + sh, 100 * r.coef, yerr=196 * r.se_hh, color=colr, lw=1.8, marker=mk, ms=6, capsize=0,
                    label=nm, mfc="white" if mk == "s" else colr)
    ax.set_xticks(xx)
    ax.set_xticklabels([s.split("aged ")[1] for s in r["sample"]])
    ax.set_xlabel("age of the wife")
    ax.set_title("(b) Wife's excess same-month job loss (pp)", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    for ax in axs:
        ax.axhline(0, color="#555555", lw=0.7)
        ax.grid(axis="y", color="#e5e5e5", lw=0.6)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    fig.tight_layout()
    fig.savefig(path)
    fig.savefig(Path(path).with_suffix(".png"), dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    if "--plot-paper" in sys.argv:
        plot_paper(HERE / "paperA_joint_loss" / "fig_cps_age_awe_jointloss.pdf")
    elif "--build-only" in sys.argv:
        build_panel62()
    else:
        main(panel60="--panel60" in sys.argv)
