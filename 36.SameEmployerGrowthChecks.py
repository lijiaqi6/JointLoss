r"""Same-employer wage growth by parental income: ability, measurement and sources (2026-10-17).

THE FINDING TESTED (Paper B; 27.CareerWageGrowth.py Section 3, 32.IndustryCareers.py Section 3): among PSID sons who
stay with the same employer between consecutive interviews (1-2 years apart, waves 1985-2023), annualised ln-wage
growth at 25-34 rises with ln parental income for White sons (0.021***, 0.015*** with fine-industry FE) and not for
Black sons (0.003 / 0.002). Questions:
  A. ABILITY (NLSY79): does the gradient survive the age-adjusted AFQT and education? Gelbach split.
  B. MEASUREMENT (PSID and NLSY79): occupation x industry cells, starting wage / wage relative to the cell, education,
     2-interval and spell-level growth, trimming, PSID strict stayers, NLSY79 without the self-employed.
  C. SOURCES (NLSY79): training, union coverage, firm size, tenure, job found through friends / relatives.
DESCRIPTIVE: sons select into employers; nothing here identifies a causal effect of parental income, ability or race.

DATA (raw data read only)
  PSID  32.IndustryCareers.py's son panel (27's panel = 24's child-year frame: 6.IGEMain parents, male heads 25-55,
        valid wage years; ln w = ln earnings - ln hours of income year wave - 1), loaded via importlib (no edits).
        Same-employer pair = 32 Section 3 exactly: consecutive interviews with a mapped occupation 1-2 years apart,
        waves 1985-2023, mapped industry, tenure with the present employer at the later interview >= years since the
        previous interview - 0.5 (27 'stay'); outcome g = annualised growth of ln w between the two income years.
        Education = 24's years of completed education. No ability measure in the PSID.
  NLSY79 men of the cross-sectional + supplemental samples (White: sample ids 1, 2; Black: 3, 10; Hispanic: 4, 11;
        poor-White supplement 9 and military samples excluded, as in 2.NLSY79.py) living with a parent in 1979;
        ln parental income = ln mean total net family income (TNFI_TRUNC) of the 1979-81 rounds in which a parent lives
        with the respondent (2.NLSY79.py logic re-run here so that Hispanic men can be added; the White / Black values
        reproduce data/nlsy79_kids.pkl, checked in the .md). Employer roster EMPLOYERS_ALL_<item>_<round>.<JJ>: JJ is
        the respondent's cumulative employer number, constant across rounds (slot 01 = first employer ever), so the
        same JJ in two rounds is the SAME EMPLOYER (observed directly). CPS (main) job of each round = lowest JJ with
        CPSJOB = 1 (27's rule); hourly pay HRLY_WAGE / 100 in 2000 $ ($2-$200); occupation (1970 codes to 2000, 2000
        codes from 2002 -> occ1990dd, 27) and industry (-> ind1990ddx and 33 groups, 32); TENURE (weeks at the
        interview), UNION (covered by a union or employee contract), COW (self-employed: code 3 to 1993, 4-5 from
        1994), ID (interview job number, links the roster slot to the job-specific QES items). Ages 25-55 (age = round
        - birth year), as 27. Pair = consecutive CPS-job rounds 1-2 years apart (annual rounds to 1994, biennial
        after) with the same JJ; outcome = (ln w_t - ln w_t-1) / years. Both wages are the pay rate at the interview.
        AFQT: AFQT-3 (R0618301), 'AFQT percentile score - revised 2006', from the 1980 ASVAB (respondents aged 15-23
        when tested). Age adjustment done here regardless of the NLS norming: the percentile score is standardised
        (mean 0, s.d. 1) within birth year, weighted by the 1979 sampling weight, over all civilian respondents
        (both sexes, sample ids 1-14) with a valid score. Coefficients are per 1 s.d. of age-adjusted AFQT.
        Education = highest grade completed (HGCREVyy, revised, as of May 1) at the latest round at age <= 35, 0-20.
        Training (Q8 section; reported at round t = training in the pair's interval): any = 'Q8-18' (attended any
        (other) training program or on-the-job training since the last interview; 1979-86 wording: vocational /
        technical training from any source; no 1987 item); company = any program of the round with 'Q8-20.0k' = 8
        ('company training', 1979-86; 'formal company training run by employer or military', 1988-2000) or 'Q8-20B'
        = 1 (run by employer, 2002+); hours (1988+) = sum over programs of weeks attended ('Q8-25', 0 = < 1 week ->
        0.5) x hours per week ('Q8-31'), 0 without training. Firm size: '# of employees at location' ('CPS-QES-FIRMSZ2'
        for the CPS job 1979, 1980, 1986-1993; 'QES-FIRMSZ2.0k' for job k 1994+), ln(employees) capped at 50,000
        ('number varies' -> missing), and 'employer has > 1 location' (FIRMSZ1), both averaged over the rounds in
        which the employer is the CPS job (employer-level). Job found through friends / relatives: 'QES-91CB.0k~000004'
        (the method that led to the offer was contacting friends or relatives; selected = 4 in 1994, 1 from 1996; asked 1994-2000 about the employers
        held then), = 0 for other methods or not looking ('QES-91A' answered); employer-level, carried to all rounds
        with that employer (so only employers held in 1994-2000 have it).
DESIGN
  Outcome g regressed on ln parental income with a quartic in age (later interview) and year (PSID) / round (NLSY79)
  fixed effects; by race unweighted; pooled = Black + White weighted (PSID individual weight of the year; NLSY79 1979
  weight), as 27 / 32; Hispanic NLSY79 men are a separate row. Clusters: 1968 family (PSID), 1979 household (NLSY79).
  All regressions are stored with cluster influence functions over one global cluster index, so race differences and
  the Gelbach (2016) decompositions (b_base - b_full = sum_k gamma_k delta_k, gamma from the full model, delta from
  the auxiliary regression of the mediator on the base regressors, delta-method s.e.) have proper s.e.
Every table: one regression per column (outcome / sample in the header), regressors as rows, FE and N at the bottom,
estimate (s.e.; p) with *** p<0.01, ** p<0.05, * p<0.1.
Writes output/same_employer_growth_checks.csv / .md / .png; cache data/same_employer_checks_nlsy79.pkl (one read of the
NLSY79 release: python 36.SameEmployerGrowthChecks.py build).
"""
import importlib.util
import re
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))         # allows running with python -I

import numpy as np
import pandas as pd
from scipy.stats import norm

from common import DATA, OUT, HERE, CPI, stars, to2000, nls_money
import os
DROPBOX = Path(os.environ.get("DROPBOX", Path.home() / "Dropbox"))   # raw data, read only

warnings.simplefilter("ignore", FutureWarning)
warnings.simplefilter("ignore", RuntimeWarning)
warnings.simplefilter("ignore", pd.errors.PerformanceWarning)
pd.set_option("display.width", 250)


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


NLS = Path(DROPBOX / "NLS/nlsy79_all_1979-2022")
C_X = DATA / "same_employer_checks_nlsy79.pkl"
SAMPLES = {1: "White", 2: "White", 5: "White", 6: "White", 3: "Black", 7: "Black", 10: "Black", 13: "Black",
           4: "Hispanic", 8: "Hispanic", 11: "Hispanic", 14: "Hispanic"}
PARENT = {4, 5, 37, 38, 47}
MIN_CELL = 200
BANDS = [(25, 34), (35, 55)]


# ================================================================ NLSY79 extraction (one read, cached)
def nlsy_extract():
    """one read of the full NLSY79 release (read only): every column needed here that 27 / 32 did not cache."""
    if C_X.exists():
        return pd.read_pickle(C_X)
    ix = pd.read_csv(DATA / "nlsy79_codebook.csv")
    q = ix["qname"].astype(str)
    pats = [r"^EMPLOYERS_ALL_(TENURE|UNION|ID|COW|HOURSWEEK)_\d{4}\.\d\d$", r"^HGCREV\d\d$", r"^Q8-18$",
            r"^Q8-20(\.\d\d)?$", r"^Q8-20B(\.\d\d)?$", r"^Q8-25(\.\d\d)?$", r"^Q8-31(\.\d\d)?$",
            r"^(CPS-)?QES-FIRMSZ[12](\.\d\d)?$", r"^QES-91(A|CA)(\.\d\d)?$", r"^QES-91CB\.\d\d~000004$",
            r"^TNFI_TRUNC$", r"^AGEATINT$", r"^AFQT-3$"]
    m = np.zeros(len(ix), bool)
    for p in pats:
        m |= q.str.match(p).to_numpy()
    rel = q.str.match(r"^HHI_FINAL_RELCODE\.\d\d$") & ix["year"].astype(str).isin(["1979", "1980", "1981"])
    sel = ix[m | rel.to_numpy()].copy()
    sel = sel[~(sel["qname"].isin(["TNFI_TRUNC", "AGEATINT"]) & ~sel["year"].astype(str).isin(["1979", "1980",
                                                                                             "1981"]))]
    base = {"R0000100": "pid", "R0173600": "sample_id", "R0214800": "sex", "R0000500": "birth_year",
            "R0216100": "wt79", "R0000149": "hhid"}
    cols = list(dict.fromkeys(list(base) + sel["col"].tolist()))
    print(f"NLSY79: reading {len(cols):,} columns from the full release (slow) ...", flush=True)
    d = pd.read_csv(NLS / "nlsy79_all_1979-2022.csv", usecols=cols)
    ren = dict(base)
    for c, qn, y in zip(sel["col"], sel["qname"], sel["year"]):
        ren[c] = qn if qn.startswith("EMPLOYERS") or qn.startswith("HGCREV") or qn == "AFQT-3" else f"{qn}|{y}"
    d = d.rename(columns=ren)
    d.to_pickle(C_X)
    return d


# ================================================================ estimation engine (influence functions)
RES, CSV = {}, []
CL = None                                                           # global cluster index


def fit(key, d, y, xs, Z, w=None):
    """WLS of y on xs + Z (controls incl. constant); stores coefficient and cluster influence vector of each x."""
    X = np.column_stack([d[x].to_numpy(float) for x in xs] + [Z])
    yv = d[y].to_numpy(float)
    wv = np.ones(len(d)) if w is None else d[w].to_numpy(float)
    Xw = X * wv[:, None]
    A = np.linalg.pinv(X.T @ Xw)
    b = A @ (Xw.T @ yv)
    e = yv - X @ b
    U = Xw * e[:, None]
    clv = CL.get_indexer(d["cl"].to_numpy(float))
    n, k = X.shape
    G = len(np.unique(clv))
    adj = np.sqrt(G / max(G - 1, 1) * (n - 1) / max(n - k, 1))
    UA = U @ A[:, :len(xs)]
    for j, x in enumerate(xs):
        RES[(key, x)] = dict(b=b[j], psi=np.bincount(clv, weights=UA[:, j], minlength=len(CL)) * adj, n=n, G=G,
                             men=d["pid"].nunique(), mean=float(np.average(yv, weights=wv)))
    return b


def E(k):
    """(estimate, influence) of a stored coefficient, or None."""
    return (RES[k]["b"], RES[k]["psi"]) if k in RES else None


def lin(terms):
    """sum c * (estimate) over [(E, c)]."""
    if any(e is None for e, _ in terms):
        return None
    return sum(c * e[0] for e, c in terms), sum(c * e[1] for e, c in terms)


def prod(e1, e2):
    if e1 is None or e2 is None:
        return None
    return e1[0] * e2[0], e2[0] * e1[1] + e1[0] * e2[1]


def ratio(e1, e2):
    if e1 is None or e2 is None:
        return None
    if abs(e2[0]) < 2 * float(np.sqrt(e2[1] @ e2[1])):              # denominator not different from zero
        return None
    return e1[0] / e2[0], e1[1] / e2[0] - e1[0] / e2[0] ** 2 * e2[1]


def tsp(e):
    """(b, se, p) of an estimate."""
    if e is None:
        return (np.nan,) * 3
    se = float(np.sqrt(e[1] @ e[1]))
    return e[0], se, (2 * norm.sf(abs(e[0] / se)) if se > 0 else np.nan)


def cell(e):
    b, se, p = tsp(e)
    if not np.isfinite(b) or not np.isfinite(se):
        return ""
    pv = "<0.001" if p < 0.001 else f"{p:.3f}"
    return f"{b:.3f}{stars(p)} ({se:.3f}; p={pv})"


def rec(tab, sample, outcome, term, e, n=np.nan, mean=np.nan, **kw):
    b, se, p = tsp(e)
    CSV.append(dict(table=tab, sample=sample, outcome=outcome, term=term, coef=b, se=se, p=p, n=n, mean=mean, **kw))


def table(header, panels):
    lines = ["| | " + " | ".join(header) + " |", "|---" * (len(header) + 1) + "|"]
    for title, rows in panels:
        if title:
            lines.append(f"| **{title}** |" + " |" * len(header))
        for lab, cells in rows:
            lines.append(f"| {lab} | " + " | ".join(cells) + " |")
    return lines + [""]


def dummies(v):
    return pd.get_dummies(pd.Series(np.asarray(v)).astype("int64"), drop_first=True, dtype=float).to_numpy()


def Zage(d, fe):
    """constant, quartic in (age - 40) / 10, dummies for each FE column."""
    C = (d["age"].to_numpy(float) - 40) / 10
    parts = [np.ones(len(d))] + [C ** k for k in range(1, 5)]
    for f in fe:
        parts.append(dummies(d[f]))
    return np.column_stack(parts)


NAME = {"P": "Pooled Black + White (weighted)", "B": "Black", "W": "White", "H": "Hispanic"}
RACE = {"B": "Black", "W": "White", "H": "Hispanic"}


def grp(d, g):
    if g == "P":
        s = d[d["race"].isin(["Black", "White"]) & (d["wpool"] > 0)]
        return s, "wpool"
    return d[d["race"] == RACE[g]], None


def run(tag, d, y, xs, fe=(), groups=("P", "B", "W"), bands=BANDS, need=(), agevar="age"):
    """y on xs + age quartic + year FE + fe in each band x group; returns {(lo, hi, g): (n, men, clusters)}."""
    info = {}
    for lo, hi in bands:
        for g in groups:
            s, w = grp(d[d[agevar].between(lo, hi)], g)
            s = s.dropna(subset=[y, *xs, *need, *fe, "yfe"] + ([w] if w else []))
            if len(s) < MIN_CELL:
                continue
            fit((tag, y, lo, hi, g), s, y, list(xs), Zage(s, ["yfe", *fe]), w)
            info[(lo, hi, g)] = (len(s), s["pid"].nunique(), s["cl"].nunique())
    return info


def K(tag, y, lo, hi, g, x="lyp"):
    return ((tag, y, lo, hi, g), x)


def G(tag, y, lo, hi, g, x="lyp"):
    """estimate for a group, or a difference ('BW' = Black - White, 'HW' = Hispanic - White)."""
    if g in ("BW", "HW"):
        return lin([(E(K(tag, y, lo, hi, g[0], x)), 1.0), (E(K(tag, y, lo, hi, "W", x)), -1.0)])
    return E(K(tag, y, lo, hi, g, x))


def nfmt(info, lo, hi, g, base=None):
    if (lo, hi, g) not in info:
        return ""
    n, men, c = info[(lo, hi, g)]
    s = f"{n:,} / {men:,} / {c:,}"
    if base is not None and (lo, hi, g) in base:
        s += f" ({100 * n / base[(lo, hi, g)][0]:.0f}%)"
    return s


def mean_of(tag, y, lo, hi, g):
    k = K(tag, y, lo, hi, g)
    return f"{RES[k]['mean']:.4f}" if k in RES else ""


# ================================================================ PSID
def psid_build():
    D32 = _load("d32", "32.IndustryCareers.py")
    D27 = D32.D27
    W = D32.ind_crosswalks()
    XWD = D27.crosswalks()
    M = D32.morg_measures(D32.morg_micro(W, XWD))
    r = D32.son_panel(W, M)
    r.attrs = {}
    return r, D32, D27, W, M, XWD


def resid_cell(d, ycol, cellcol, yearcol):
    """ycol minus its fitted value from cell FE + year FE + age quartic (OLS on the rows given)."""
    s = d.dropna(subset=[ycol, cellcol, yearcol, "age"])
    X = np.column_stack([Zage(s, [yearcol]), dummies(s[cellcol])])
    b = np.linalg.lstsq(X, s[ycol].to_numpy(float), rcond=None)[0]
    out = pd.Series(np.nan, index=d.index)
    out[s.index] = s[ycol].to_numpy(float) - X @ b
    return out


def spells(v, tcol, lwcol, same):
    """employer spells (runs of consecutive same-employer links): growth from the first to the last interview of
    spells with >= 2 links and valid wages at both ends; one row per spell."""
    v = v.copy()
    v["_new"] = (v[same] != 1).astype(int)
    v["_run"] = v.groupby("pid")["_new"].cumsum()
    n = v.groupby(["pid", "_run"]).size().rename("n")
    z = v[v[lwcol].notna()]
    f = z.groupby(["pid", "_run"]).agg(t0=(tcol, "first"), t1=(tcol, "last"), w0=(lwcol, "first"),
                                       w1=(lwcol, "last"), a0=("age", "first"), a1=("age", "last"),
                                       yfe=("yfe", "last")).join(n)
    f = f[(f["n"] >= 3) & (f["t1"] - f["t0"] >= 3)].reset_index()
    return pd.DataFrame({"pid": f["pid"], "g_sp": (f["w1"] - f["w0"]) / (f["t1"] - f["t0"]),
                         "age": (f["a0"] + f["a1"]) / 2, "yfe": f["yfe"], "years": f["t1"] - f["t0"]})


def psid_pairs(r):
    r = r.sort_values(["pid", "wave"]).reset_index(drop=True)
    r["cell"] = (r["occ11"] * 100 + r["igrp"]).where(r["occ11"].notna() & r["igrp"].notna())
    v0 = r[r["valid"] & r["race"].isin(["Black", "White"])]
    r["lwrel"] = resid_cell(v0, "lw", "cell", "year").reindex(r.index)
    v = r[r["dd"].notna()][["pid", "wave", "lw", "lwrel", "stay", "tenure", "age", "cell", "dd", "ddx"]].copy()   # 27's transition rows
    g = v.groupby("pid")
    for k in (1, 2):
        v[f"lw_l{k}"] = g["lw"].shift(k)
        v[f"wave_l{k}"] = g["wave"].shift(k)
        v[f"lwrel_l{k}"] = g["lwrel"].shift(k)
    for c in ("cell", "dd", "ddx"):
        v[f"{c}0"] = g[c].shift(1)
    r = r.merge(v[["pid", "wave", "lw_l1", "lw_l2", "wave_l1", "wave_l2", "lwrel_l1", "cell0", "dd0", "ddx0"]],
                on=["pid", "wave"], how="left")
    d = r[r["g_lw_t"].notna() & r["wave"].ge(1985) & r["igrp"].notna()].copy()        # 32 Section 3 sample
    d["yfe"] = d["year"]
    d["cl"] = d["fam68"].astype(float)
    d["g"] = d["g_stay"]
    s = d[d["stay"] == 1].copy()
    s["lw0"] = s["lw_l1"]
    s["rel0"] = s["lwrel_l1"]
    s["lwm2"] = s["lw_l2"].where((s["wave"] - s["wave_l2"]) <= 4)
    span = s["wave"] - s["wave_l2"]
    ok2 = (s["wave_l1"] - s["wave_l2"]).between(1, 2) & (s["tenure"] >= span - 0.5)
    s["g2"] = ((s["lw"] - s["lw_l2"]) / span).where(ok2)
    s["g_strict"] = s["g"].where(s["tenure"] >= s["gap"] + 1)
    s["ddx_i"] = s["ddx"]
    s["dd_i"] = s["dd"]
    lo_, hi_ = s["g"].quantile([0.01, 0.99])
    s["g_trim"] = s["g"].where(s["g"].between(lo_, hi_))
    s.attrs["trim"] = (lo_, hi_)
    # spells: runs of consecutive stayer interviews (no employer id in the PSID: the run is held together by tenure)
    v2 = r[r["dd"].notna() & r["wave"].ge(1984)][["pid", "wave", "lw", "stay", "age", "year", "race", "lyp", "fam68",
                                                    "wpool", "gap"]].copy()
    v2["same"] = ((v2["stay"] == 1) & v2["gap"].between(1, 2)).astype(int)
    v2["yfe"] = v2["year"]
    sp = spells(v2, "wave", "lw", "same")
    first = r.drop_duplicates("pid").set_index("pid")
    sp = sp.join(first[["race", "lyp", "fam68"]], on="pid")
    sp["wpool"] = sp["pid"].map(r.groupby("pid")["wpool"].mean())
    sp["cl"] = sp["fam68"].astype(float)
    return s, sp


# ================================================================ NLSY79
def nlsy_build(D32, D27, W, M, XWD):
    X = nlsy_extract()
    k = X[["pid", "sample_id", "sex", "birth_year", "wt79", "hhid"]].copy()
    k["race"] = k["sample_id"].map(SAMPLES)
    k["birth_year"] = np.where(k["birth_year"] < 100, 1900 + k["birth_year"], k["birth_year"])
    # ---- AFQT-3, standardised within birth year (1979 weights, civilian respondents of both sexes)
    a = pd.to_numeric(X["AFQT-3"], errors="coerce")
    k["afqt_pct"] = (a.where(a >= 0) / 1000).to_numpy()
    k["afqt"] = np.nan
    civ = k["sample_id"].between(1, 14) & k["afqt_pct"].notna() & (k["wt79"] > 0)
    for by, z in k[civ].groupby("birth_year"):
        mu = np.average(z["afqt_pct"], weights=z["wt79"])
        sd = np.sqrt(np.average((z["afqt_pct"] - mu) ** 2, weights=z["wt79"]))
        idx = k.index[(k["birth_year"] == by) & k["afqt_pct"].notna()]
        k.loc[idx, "afqt"] = (k.loc[idx, "afqt_pct"] - mu) / sd
    # ---- education: highest grade completed at the latest round at age <= 35
    hg = {int(c[-2:]) + (1900 if int(c[-2:]) > 50 else 2000): c for c in X.columns if re.fullmatch(r"HGCREV\d\d", c)}
    edu = pd.Series(np.nan, index=X.index)
    for y in sorted(hg):
        v = pd.to_numeric(X[hg[y]], errors="coerce")
        v = v.where(v.between(0, 20))
        edu = v.where(v.notna() & ((y - k["birth_year"]) <= 35), edu)
    k["educ"] = edu.to_numpy()
    # ---- parental income: 2.NLSY79.py logic (1979-81 rounds with a parent in the household)
    inc, par = {}, {}
    for y in (1979, 1980, 1981):
        rc = [c for c in X.columns if re.fullmatch(rf"HHI_FINAL_RELCODE\.\d\d\|{y}", c)]
        par[y] = np.isin(X[rc].to_numpy(), list(PARENT)).any(axis=1)
        inc[y] = to2000(nls_money(X[f"TNFI_TRUNC|{y}"]).to_numpy(), y - 1)
    pa = np.column_stack([np.where(par[y], inc[y], np.nan) for y in (1979, 1980, 1981)])
    with np.errstate(all="ignore"):
        pav = np.where(par[1979], np.nanmean(pa, axis=1), np.nan)
    k["lpinc"] = np.log(np.where(pav > 0, pav, np.nan))
    k = k[(k["sex"] == 1) & k["race"].notna() & k["lpinc"].notna()].copy()
    chk = pd.read_pickle(DATA / "nlsy79_kids.pkl")
    chk = chk[chk["female"] == 0].set_index("pid")["lpinc_av"]
    cmp_ = k.set_index("pid")["lpinc"].reindex(chk.index)
    k.attrs["check"] = (int(chk.notna().sum()), int(cmp_.notna().sum()),
                        float(np.nanmax(np.abs(cmp_ - chk))) if cmp_.notna().any() else np.nan)
    ids = set(k["pid"])
    # ---- employer roster: CPS job of each round
    R27 = D27.nlsy_extract()
    RI = D32.nlsy_ind_extract()
    R27 = R27[R27["pid"].isin(ids)].set_index("pid")
    RI = RI[RI["pid"].isin(ids)].set_index("pid").reindex(R27.index)
    Xs = X[X["pid"].isin(ids)].set_index("pid").reindex(R27.index)
    rx = re.compile(r"EMPLOYERS_ALL_CPSJOB_(\d{4})\.(\d\d)$")
    slots = {}
    for c in R27.columns:
        m_ = rx.match(c)
        if m_:
            slots.setdefault(int(m_.group(1)), []).append(m_.group(2))
    pids = R27.index.to_numpy()
    rows = []

    def col(frame, item, y, jj):
        c = f"EMPLOYERS_ALL_{item}_{y}.{jj}"
        return pd.to_numeric(frame[c], errors="coerce").to_numpy(float) if c in frame.columns else \
            np.full(len(frame), np.nan)
    for y, jjs in sorted(slots.items()):
        jjs = sorted(jjs)
        C = np.column_stack([col(R27, "CPSJOB", y, jj) == 1 for jj in jjs])
        has = C.any(axis=1)
        first = C.argmax(axis=1)
        x = pd.DataFrame({"pid": pids, "round": y, "jj": np.array([int(j) for j in jjs])[first]})
        for item, frame in (("OCC", R27), ("HRLY_WAGE", R27), ("IND", RI), ("TENURE", Xs), ("UNION", Xs),
                            ("ID", Xs), ("COW", Xs)):
            Mx = np.column_stack([col(frame, item, y, jj) for jj in jjs])
            x[item.lower()] = Mx[np.arange(len(x)), first]
        rows.append(x[has])
    J = pd.concat(rows, ignore_index=True)
    J = J.merge(k[["pid", "race", "birth_year", "wt79", "hhid", "lpinc", "afqt", "afqt_pct", "educ"]], on="pid")
    J["age"] = J["round"] - J["birth_year"]
    J = J[J["age"].between(25, 55)].copy()
    # ---- occupation (27) and industry (32)
    J["occ"] = J["occ"].where(J["occ"] > 0)
    J["scheme"] = np.where(J["round"] <= 2000, "1970", "2000")
    J["occ2"] = np.where((J["scheme"] == "2000") & (J["occ"] >= 1000), J["occ"] // 10, J["occ"])
    J = D27.attach_scores(J, "occ2", "scheme", "round", XWD, D27.SCORES)
    J["icode"] = J["ind"].where(J["ind"] > 0)
    J["isch"] = np.where(J["round"] <= 2000, "1970", np.where(J["icode"] >= 1000, "2012", "2000"))
    rc = D32.recode2000(W, np.concatenate([J.loc[J["isch"] == "2000", "icode"].dropna().to_numpy(),
                                           D32.code2000(J.loc[J["isch"] == "2012", "icode"].dropna().to_numpy())]))
    J = D32.attach_industry(J, "icode", "isch", W, M, rc)
    J["occ11"] = D27.group_of(J["dd"].to_numpy(float))
    J["cell"] = (J["occ11"] * 100 + J["igrp"]).where(J["occ11"].notna() & J["igrp"].notna())
    w = J["hw"].where(J["hw"] > 0) / 100 if "hw" in J else J["hrly_wage"].where(J["hrly_wage"] > 0) / 100
    w = w * J["round"].map(lambda yy: CPI[2000] / CPI[min(int(yy), 2022)])
    J["lw"] = np.log(w.where(w.between(2, 200)))
    J["ten_y"] = (J["tenure"].where(J["tenure"] >= 0) / 52).clip(upper=40)
    J["union"] = J["union"].where(J["union"].isin([0, 1]))
    J["selfemp"] = np.where(J["round"] <= 1993, J["cow"] == 3, J["cow"].isin([4, 5])).astype(float)
    J.loc[J["cow"].isna() | (J["cow"] < 0), "selfemp"] = np.nan
    J["idnum"] = J["id"].where(J["id"] > 0)
    # ---- round-level items: training, firm size, job finding (job-specific QES items via the interview job number)
    T = round_items(Xs, J)
    J = J.merge(T, on=["pid", "round"], how="left")
    emp = J.groupby(["pid", "jj"]).agg(lnemp_e=("lnemp", "mean"), multi_e=("multi", "mean"), netw_e=("netw", "max"))
    J = J.join(emp, on=["pid", "jj"])
    J["race"] = J["race"].astype(str)
    J["wpool"] = J["wt79"].where(J["wt79"] > 0)
    J["cl"] = J["hhid"].astype(float) + 1e7
    J["yfe"] = J["round"]
    J["lyp"] = J["lpinc"]
    J = J.sort_values(["pid", "round"]).reset_index(drop=True)
    # wage relative to the occupation x industry cell (age quartic, round FE), all NLSY79 men in the panel
    J["lwrel"] = resid_cell(J, "lw", "cell", "round")
    g = J.groupby("pid")
    for c in ("round", "jj", "lw", "lwrel", "ten_y", "union"):
        J[f"{c}_l1"] = g[c].shift(1)
    for c in ("cell", "dd", "ddx"):
        J[f"{c}0"] = g[c].shift(1)
    for c in ("round", "jj", "lw"):
        J[f"{c}_l2"] = g[c].shift(2)
    J["gap"] = J["round"] - J["round_l1"]
    ok = J["gap"].between(1, 2)
    J["same"] = (ok & (J["jj"] == J["jj_l1"])).astype(float).where(ok)
    J["g"] = ((J["lw"] - J["lw_l1"]) / J["gap"]).where(J["same"] == 1)
    return J, k


def round_items(Xs, J):
    """pid x round: any / company training since the last interview, training hours, firm size, network job."""
    pids = Xs.index.to_numpy()
    cols = set(Xs.columns)

    def num(c):
        return pd.to_numeric(Xs[c], errors="coerce").to_numpy(float) if c in cols else np.full(len(Xs), np.nan)
    out = []
    years = sorted({int(c.split("|")[1]) for c in cols if c.startswith("Q8-18|")} |
                   {int(c.split("|")[1]) for c in cols if "FIRMSZ" in c or c.startswith("QES-91")})
    cps = J[["pid", "round", "idnum"]]
    for y in years:
        x = pd.DataFrame({"pid": pids, "round": y})
        q18 = num(f"Q8-18|{y}")
        anyt = np.where(q18 == 1, 1.0, np.where(q18 == 0, 0.0, np.nan))
        x["train_any"] = anyt
        typ = [num(c) for c in cols if re.fullmatch(rf"Q8-20(\.\d\d)?\|{y}", c)]
        typb = [num(c) for c in cols if re.fullmatch(rf"Q8-20B(\.\d\d)?\|{y}", c)]
        comp = np.zeros(len(x), bool)
        for t_ in typ:
            comp |= (t_ == 8)
        for t_ in typb:
            comp |= (t_ == 1)
        x["train_comp"] = np.where(anyt == 1, comp.astype(float), np.where(anyt == 0, 0.0, np.nan))
        if y >= 1988:
            hrs = np.zeros(len(x))
            okh = np.zeros(len(x), bool)
            for j in range(1, 6):
                wk = num(f"Q8-25.0{j}|{y}")
                hw = num(f"Q8-31.0{j}|{y}")
                wk = np.where(wk == 0, 0.5, wk)
                good = (wk >= 0) & (hw >= 0)
                hrs += np.where(good, wk * hw, 0)
                okh |= good
            x["train_hrs"] = np.where(anyt == 0, 0.0, np.where((anyt == 1) & okh, np.minimum(hrs, 2000) / 100,
                                                                  np.nan))
        else:
            x["train_hrs"] = np.nan
        # firm size / multi-location and job finding of the CPS job (job number idnum)
        c_ = cps[cps["round"] == y].set_index("pid")["idnum"].reindex(pids).to_numpy()
        emp_n = np.full(len(x), np.nan)
        multi = np.full(len(x), np.nan)
        netw = np.full(len(x), np.nan)
        if f"CPS-QES-FIRMSZ2|{y}" in cols:
            emp_n = num(f"CPS-QES-FIRMSZ2|{y}")
            multi = num(f"CPS-QES-FIRMSZ1|{y}")
        else:
            for j in range(1, 6):
                sel = c_ == j
                e2, e1 = num(f"QES-FIRMSZ2.0{j}|{y}"), num(f"QES-FIRMSZ1.0{j}|{y}")
                emp_n = np.where(sel, e2, emp_n)
                multi = np.where(sel, e1, multi)
                if f"QES-91A.0{j}|{y}" in cols:
                    a91 = num(f"QES-91A.0{j}|{y}")
                    cb4 = num(f"QES-91CB.0{j}~000004|{y}")
                    nv = np.where(cb4 > 0, 1.0, np.where(np.isin(a91, [0, 1]), 0.0, np.nan))
                    netw = np.where(sel, nv, netw)
        emp_n = np.where((emp_n >= 0) & (emp_n < 99990), np.minimum(emp_n, 50000), np.nan)
        x["lnemp"] = np.log(np.maximum(emp_n, 1))
        x["multi"] = np.where(np.isin(multi, [0, 1]), multi, np.nan)
        x["netw"] = netw
        out.append(x)
    T = pd.concat(out, ignore_index=True)
    return T.groupby(["pid", "round"]).first().reset_index()


def nlsy_samples(J):
    s = J[J["same"] == 1].copy()
    s = s[s["g"].notna()]
    s["lw0"] = s["lw_l1"]
    s["rel0"] = s["lwrel_l1"]
    s["lwm2"] = s["lw_l2"].where((s["round"] - s["round_l2"]) <= 4)
    span = s["round"] - s["round_l2"]
    ok2 = (s["round_l1"] - s["round_l2"]).between(1, 2) & (s["jj_l2"] == s["jj"])
    s["g2"] = ((s["lw"] - s["lw_l2"]) / span).where(ok2)
    s["g_nose"] = s["g"].where(s["selfemp"] == 0)
    lo_, hi_ = s["g"].quantile([0.01, 0.99])
    s["g_trim"] = s["g"].where(s["g"].between(lo_, hi_))
    s.attrs["trim"] = (lo_, hi_)
    s["ten0"] = s["ten_y_l1"]
    s["ten0sq"] = s["ten0"] ** 2 / 10
    s["ddx_i"] = s["ddx"]
    s["dd_i"] = s["dd"]
    v = J[["pid", "round", "lw", "same", "age", "yfe"]].copy()
    v["same"] = v["same"].fillna(0)
    sp = spells(v, "round", "lw", "same")
    first = J.drop_duplicates("pid").set_index("pid")
    sp = sp.join(first[["race", "lyp", "cl", "wpool"]], on="pid")
    return s, sp


# ================================================================ sections
GROUPS_P = [("P", NAME["P"]), ("B", "Black"), ("W", "White"), ("BW", "Black - White")]
GROUPS_N = [("P", NAME["P"]), ("B", "Black"), ("W", "White"), ("H", "Hispanic"), ("BW", "Black - White"),
            ("HW", "Hispanic - White")]
GN = ("P", "B", "W", "H")


def sec_baseline_psid(s, md):
    """reproduce 32 Section 3 (cols 1 and 3)."""
    i1 = run("p_base", s, "g", ["lyp"])
    i3 = run("p_ddx", s, "g", ["lyp"], fe=["ddx_i"])
    return i1, i3


def sec_A(s, md):
    """NLSY79: AFQT and education."""
    need = ["afqt", "educ", "ddx0", "cell0"]
    info_full = run("a1", s, "g", ["lyp"], groups=GN)
    specs = [("a2", ["lyp"], ()), ("a3", ["lyp", "afqt"], ()), ("a4", ["lyp", "educ"], ()),
             ("a5", ["lyp", "afqt", "educ"], ()), ("a6", ["lyp", "afqt", "educ"], ("ddx0",)),
             ("a7", ["lyp", "afqt", "educ"], ("cell0",))]
    info = {}
    for tag, xs, fe in specs:
        info[tag] = run(tag, s, "g", xs, fe=fe, groups=GN, need=need)
    # auxiliary regressions for Gelbach (mediator on the base regressors, common sample)
    for med in ("afqt", "educ"):
        run(f"aux_{med}", s, med, ["lyp"], groups=GN, need=need + ["g"])
    hdr = ["(1) same-employer annual ln wage growth, all pairs", "(2) same, common sample (AFQT, education, "
           "industry, occupation known)", "(3) + AFQT", "(4) + education", "(5) + AFQT + education",
           "(6) (5) + fine-industry FE (first interview)", "(7) (5) + occupation-group x industry-group FE (first interview)"]
    tags = ["a1", "a2", "a3", "a4", "a5", "a6", "a7"]
    panels = []
    for g, gname in GROUPS_N:
        rows = []
        for lo, hi in BANDS:
            for x, lab in (("lyp", "ln parental income"), ("afqt", "AFQT (1 s.d., age-adjusted)"),
                           ("educ", "years of education")):
                es = [G(t, "g", lo, hi, g, x) for t in tags]
                if all(e is None for e in es):
                    continue
                rows.append((f"{lab}, {lo}-{hi}", [cell(e) for e in es]))
                for t, e in zip(tags, es):
                    rec("A1 NLSY79 ability", gname, f"g {t}", f"{x}, {lo}-{hi}", e)
            if g not in ("BW", "HW"):
                rows.append((f"Mean growth, {lo}-{hi}", [mean_of(t, "g", lo, hi, g) for t in tags]))
                base = info_full
                rows.append((f"N pairs / men / clusters, {lo}-{hi} (% of col 1)",
                             [nfmt(info_full, lo, hi, g)] + [nfmt(info[t], lo, hi, g, base) for t in tags[1:]]))
        panels.append((gname, rows))
    panels.append(("Fixed effects / controls", [("all columns", ["quartic in age, round FE"] * 5 +
                                                  ["+ ind1990ddx FE of the first round", "+ 11 occupation groups x 33 industry groups FE of the first round"])]))
    md += ["## A. Ability: NLSY79 same-employer wage growth, ln parental income, AFQT and education", "",
           "Men living with a parent in 1979; consecutive CPS-job rounds 1-2 years apart with the SAME roster employer "
           "(JJ); outcome = annualised growth of the ln hourly pay rate; age band = age at the later round. One "
           "regression per column; controls in every column: quartic in age, round FE. AFQT = AFQT-3 (2006 revision) "
           "percentile standardised within birth year (1 s.d.). Education = highest grade completed at the latest "
           "round at age <= 35. Pooled = Black + White men weighted by the 1979 weight; groups unweighted. "
           "Black - White / Hispanic - White = difference of the coefficients from the separate regressions (= the "
           "race interaction of a fully interacted model). Clusters = 1979 household.", ""]
    md += table(hdr, panels)
    # ---- A2: the AFQT gradient itself
    for tag, xs in (("b1", ["afqt"]), ("b2", ["afqt", "lyp"]), ("b3", ["afqt", "lyp", "educ"])):
        run(tag, s, "g", xs, groups=GN, need=["afqt", "educ"])
    hdr2 = ["(1) growth on AFQT", "(2) growth on AFQT + ln parental income", "(3) (2) + education"]
    panels = []
    for g, gname in GROUPS_N:
        rows = []
        for lo, hi in BANDS:
            for x, lab in (("afqt", "AFQT (1 s.d.)" + (" x race difference" if g in ("BW", "HW") else "")),
                           ("lyp", "ln parental income"), ("educ", "years of education")):
                es = [G(t, "g", lo, hi, g, x) for t in ("b1", "b2", "b3")]
                rows.append((f"{lab}, {lo}-{hi}", [cell(e) for e in es]))
                for t, e in zip(("b1", "b2", "b3"), es):
                    rec("A2 NLSY79 AFQT gradient", gname, f"g {t}", f"{x}, {lo}-{hi}", e)
            if g not in ("BW", "HW"):
                k_ = K("b1", "g", lo, hi, g, "afqt")
                rows.append((f"N pairs / men / clusters, {lo}-{hi}",
                             [f"{RES[k_]['n']:,} / {RES[k_]['men']:,} / {RES[k_]['G']:,}" if k_ in RES else ""] * 3))
        panels.append((gname, rows))
    md += ["### A2. Does ability raise same-employer wage growth? (AFQT gradient by race)", "",
           "Sample: pairs with AFQT and education known (no industry / occupation requirement (AFQT and education known). "
           "Controls: quartic in age, round FE. In the difference panels the AFQT row is the AFQT x Black (AFQT x "
           "Hispanic) interaction of a fully interacted model.", ""]
    md += table(hdr2, panels)
    # ---- A3: Gelbach
    hdr3 = ["(1) ln parental income, base (col 2)", "(2) + AFQT + education (col 5)", "(3) explained = (1) - (2)",
            "(4) via AFQT", "(5) via education", "(6) share via AFQT = (4)/(1)", "(7) share via education = (5)/(1)",
            "(8) AFQT on ln parental income (delta)", "(9) education on ln parental income (delta)"]
    panels = []
    for g, gname in GROUPS_N:
        rows = []
        for lo, hi in BANDS:
            bb, bf = G("a2", "g", lo, hi, g), G("a5", "g", lo, hi, g)
            comp = {}
            for med in ("afqt", "educ"):
                if g in ("BW", "HW"):
                    c1 = prod(E(K("a5", "g", lo, hi, g[0], med)), E(K(f"aux_{med}", med, lo, hi, g[0])))
                    c2 = prod(E(K("a5", "g", lo, hi, "W", med)), E(K(f"aux_{med}", med, lo, hi, "W")))
                    comp[med] = lin([(c1, 1.0), (c2, -1.0)]) if c1 and c2 else None
                else:
                    comp[med] = prod(E(K("a5", "g", lo, hi, g, med)), E(K(f"aux_{med}", med, lo, hi, g)))
            ex = lin([(bb, 1.0), (bf, -1.0)]) if bb and bf else None
            es = [bb, bf, ex, comp["afqt"], comp["educ"], ratio(comp["afqt"], bb), ratio(comp["educ"], bb),
                  G("aux_afqt", "afqt", lo, hi, g), G("aux_educ", "educ", lo, hi, g)]
            rows.append((f"Sons {lo}-{hi}", [cell(e) for e in es]))
            for h, e in zip(hdr3, es):
                rec("A3 NLSY79 Gelbach AFQT / education", gname, h, f"{lo}-{hi}", e)
        panels.append((gname, rows))
    md += ["### A3. Gelbach decomposition: how much of the parental-income gradient runs through AFQT and education",
           "", "b_base - b_full = gamma_AFQT x delta_AFQT + gamma_educ x delta_educ (Gelbach 2016): gamma = "
           "coefficient of the mediator in column (5) of Table A, delta = coefficient of ln parental income in the "
           "regression of the mediator on ln parental income + age quartic + round FE on the same sample. Shares "
           "(delta method) are left blank when the base coefficient is not different from zero (|t| < 2), since a "
           "share of an imprecise zero is not informative.", ""]
    md += table(hdr3, panels)
    return info_full, info


def sec_B(s, sp, md, data, groups_def, tagp, educ_col="educ"):
    """measurement checks; data = 'PSID' or 'NLSY79'."""
    groups = ("P", "B", "W") if data == "PSID" else GN
    GR = GROUPS_P if data == "PSID" else GROUPS_N
    last = (("b13", "g_strict", ["lyp"], (), "s", "(13) strict stayers: tenure >= years between interviews + 1 "
                                                   "(both income years with the employer)") if data == "PSID" else
            ("b13", "g_nose", ["lyp"], (), "s", "(13) excluding the self-employed"))
    specs = [("b01", "g", ["lyp"], (), "s", "(1) baseline"),
             ("b02", "g", ["lyp"], ("cell",), "s", "(2) + occupation-group x industry-group FE, later interview"),
             ("b03", "g", ["lyp"], ("cell0",), "s", "(3) + occupation-group x industry-group FE, first interview"),
             ("b04", "g", ["lyp"], ("dd0", "ddx0"), "s", "(4) + detailed occupation FE + fine-industry FE, first "
                                                         "interview"),
             ("b05", "g", ["lyp", "lw0"], (), "s", "(5) + ln wage at the first interview of the pair"),
             ("b06", "g", ["lyp", "rel0"], (), "s", "(6) + ln wage relative to the cell, first interview"),
             ("b07", "g", ["lyp", "lwm2"], (), "s", "(7) + ln wage one interview earlier (t-2)"),
             ("b08", "g", ["lyp", educ_col], (), "s", "(8) + years of education"),
             ("b09", "g", ["lyp", educ_col, "lwm2"], ("cell0",), "s", "(9) + education + ln wage at t-2 + cell FE "
                                                                      "(first interview)"),
             ("b10", "g2", ["lyp"], (), "s", "(10) 2-interval growth, same employer over 3 interviews"),
             ("b11", "g_sp", ["lyp"], (), "sp", "(11) spell-level growth (first to last interview of employer spells "
                                                "with >= 3 interviews)"),
             ("b12", "g_trim", ["lyp"], (), "s", "(12) growth trimmed at the 1st / 99th percentiles"), last]
    info = {}
    for tag, y, xs, fe, src, _ in specs:
        info[tag] = run(f"{tagp}{tag}", s if src == "s" else sp, y, xs, fe=fe, groups=groups)
    hdr = [h for *_, h in specs]
    panels = []
    for g, gname in GR:
        rows = []
        for lo, hi in BANDS:
            es = [G(f"{tagp}{t}", y, lo, hi, g) for t, y, *_ in specs]
            rows.append((f"ln parental income, sons {lo}-{hi}", [cell(e) for e in es]))
            for (t, y, *_), e in zip(specs, es):
                rec(f"B {data} measurement", gname, f"{y} {t}", f"lyp, {lo}-{hi}", e)
            e0 = es[0]
            dif = [lin([(e, 1.0), (e0, -1.0)]) if (j > 0 and e is not None and e0 is not None) else None
                   for j, e in enumerate(es)]
            rows.append((f"change vs (1), {lo}-{hi}", [cell(d_) for d_ in dif]))
            for (t, y, *_), d_ in zip(specs, dif):
                if d_ is not None:
                    rec(f"B {data} measurement", gname, f"{y} {t}", f"change vs (1), {lo}-{hi}", d_)
            for pos, lab in ((1, "first added control"), (2, "second added control")):
                ctl = [cell(G(f"{tagp}{t}", y, lo, hi, g, xs[pos])) if len(xs) > pos else ""
                       for t, y, xs, *_ in specs]
                if any(ctl):
                    rows.append((f"{lab} (see header), {lo}-{hi}", ctl))
                for t, y, xs, *_ in specs:
                    if len(xs) > pos:
                        rec(f"B {data} measurement", gname, f"{y} {t}", f"{xs[pos]}, {lo}-{hi}",
                            G(f"{tagp}{t}", y, lo, hi, g, xs[pos]))
            if g not in ("BW", "HW"):
                rows.append((f"Mean of outcome, {lo}-{hi}", [mean_of(f"{tagp}{t}", y, lo, hi, g)
                                                              for t, y, *_ in specs]))
                rows.append((f"N obs / men / clusters, {lo}-{hi} (% of col 1)",
                             [nfmt(info[t], lo, hi, g, info["b01"] if t != "b01" else None)
                              for t, *_ in specs]))
        panels.append((gname, rows))
    yr = "year" if data == "PSID" else "round"
    panels.append(("Fixed effects / controls", [("all columns", [f"quartic in age, {yr} FE"] * len(specs))]))
    return hdr, panels, info


def sec_C(s, md):
    """NLSY79 sources: training, union, firm size, tenure, network job."""
    srcs = [("train_any", "(1) any training since last interview"), ("train_comp", "(2) company training"),
            ("train_hrs", "(3) training hours / 100 (1988+)"), ("union", "(4) union / contract coverage"),
            ("lnemp_e", "(5) ln employees at location (employer)"), ("multi_e", "(6) employer has > 1 location"),
            ("netw_e", "(7) job found through friends / relatives (employers held 1994-2000)"),
            ("ten0", "(8) tenure at the first interview (years)")]
    info = {}
    for y, _ in srcs:
        info[y] = run("c1", s, y, ["lyp"], groups=GN)
    panels = []
    for g, gname in GROUPS_N:
        rows = []
        for lo, hi in BANDS:
            es = [G("c1", y, lo, hi, g) for y, _ in srcs]
            rows.append((f"ln parental income, sons {lo}-{hi}", [cell(e) for e in es]))
            for (y, _), e in zip(srcs, es):
                rec("C1 NLSY79 sources on parental income", gname, y, f"lyp, {lo}-{hi}", e)
            if g not in ("BW", "HW"):
                rows.append((f"Mean, {lo}-{hi}", [mean_of("c1", y, lo, hi, g) for y, _ in srcs]))
                rows.append((f"N pairs / men / clusters, {lo}-{hi}", [nfmt(info[y], lo, hi, g) for y, _ in srcs]))
        panels.append((gname, rows))
    md += ["## C. Sources of same-employer growth (NLSY79)", "",
           "### C1. Gradient of each candidate source in ln parental income (same-employer pairs)", "",
           "One regression per column (outcome in the header) on the same-employer pair sample of Table A column (1); "
           "controls: quartic in age, round FE. Training is reported at the later round of the pair (training in the "
           "pair's interval). Employer-level items are means over the rounds in which the employer is the CPS job.",
           ""]
    md += table([h for _, h in srcs], panels)
    # ---- C2: adding sources to the growth regression on a common sample
    M_ = {"train": ["train_any", "train_comp"], "union": ["union"], "size": ["lnemp_e", "multi_e"],
          "tenure": ["ten0", "ten0sq"]}
    allm = sum(M_.values(), [])
    specs = [("c2_0", []), ("c2_t", M_["train"]), ("c2_u", M_["union"]), ("c2_s", M_["size"]),
             ("c2_n", M_["tenure"]), ("c2_all", allm)]
    inf2 = {}
    for tag, ms in specs:
        inf2[tag] = run(tag, s, "g", ["lyp"] + ms, groups=GN, need=allm)
    for m in allm:
        run("c2_aux", s, m, ["lyp"], groups=GN, need=allm + ["g"])
    hdr = ["(1) growth, common sample", "(2) + training", "(3) + union", "(4) + firm size", "(5) + tenure",
           "(6) + all"]
    labs = {"train_any": "any training", "train_comp": "company training", "union": "union coverage",
            "lnemp_e": "ln employees", "multi_e": "> 1 location", "ten0": "tenure (years)", "ten0sq": "tenure^2 / 10"}
    panels = []
    for g, gname in GROUPS_N:
        rows = []
        for lo, hi in BANDS:
            for x in ["lyp"] + allm:
                es = [G(t, "g", lo, hi, g, x) if (x == "lyp" or x in ms) else None for t, ms in specs]
                rows.append((f"{'ln parental income' if x == 'lyp' else labs[x]}, {lo}-{hi}", [cell(e) for e in es]))
                for (t, _), e in zip(specs, es):
                    if e is not None:
                        rec("C2 NLSY79 growth with sources", gname, f"g {t}", f"{x}, {lo}-{hi}", e)
            if g not in ("BW", "HW"):
                rows.append((f"N pairs / men / clusters, {lo}-{hi}",
                             [nfmt(inf2[t], lo, hi, g) for t, _ in specs]))
        panels.append((gname, rows))
    md += ["### C2. Does controlling for the sources shrink the parental-income gradient of same-employer growth?", "",
           "Common sample: training (no 1987 item), union, firm size and tenure known. Controls: quartic in age, round "
           "FE. One regression per column.", ""]
    md += table(hdr, panels)
    # ---- C3: Gelbach by source group
    hdr3 = ["(1) base", "(2) all sources", "(3) explained", "(4) via training", "(5) via union", "(6) via firm size",
            "(7) via tenure", "(8) share explained = (3)/(1)"]
    panels = []
    for g, gname in GROUPS_N:
        rows = []
        for lo, hi in BANDS:
            bb, bf = G("c2_0", "g", lo, hi, g), G("c2_all", "g", lo, hi, g)
            parts = []
            for grp_, ms in M_.items():
                terms = []
                for m in ms:
                    if g in ("BW", "HW"):
                        c1 = prod(E(K("c2_all", "g", lo, hi, g[0], m)), E(K("c2_aux", m, lo, hi, g[0])))
                        c2 = prod(E(K("c2_all", "g", lo, hi, "W", m)), E(K("c2_aux", m, lo, hi, "W")))
                        terms += [(c1, 1.0), (c2, -1.0)]
                    else:
                        terms.append((prod(E(K("c2_all", "g", lo, hi, g, m)), E(K("c2_aux", m, lo, hi, g))), 1.0))
                parts.append(lin(terms))
            ex = lin([(bb, 1.0), (bf, -1.0)]) if bb and bf else None
            es = [bb, bf, ex] + parts + [ratio(ex, bb)]
            rows.append((f"Sons {lo}-{hi}", [cell(e) for e in es]))
            for h, e in zip(hdr3, es):
                rec("C3 NLSY79 Gelbach sources", gname, h, f"{lo}-{hi}", e)
        panels.append((gname, rows))
    md += ["### C3. Gelbach decomposition of the parental-income gradient by source", "",
           "As A3, with the mediators of Table C2 column (6) grouped (training = any + company; firm size = ln "
           "employees + > 1 location; tenure = tenure + tenure^2). Share blank when the base is not different from "
           "zero.", ""]
    md += table(hdr3, panels)
    # ---- C4: network job (subsample)
    for tag, xs in (("c4_0", ["lyp"]), ("c4_1", ["lyp", "netw_e"])):
        run(tag, s, "g", xs, groups=GN, need=["netw_e"])
    run("c4_aux", s, "netw_e", ["lyp"], groups=GN, need=["g"])
    hdr4 = ["(1) growth, employers with job-finding method known", "(2) + found through friends / relatives",
            "(3) explained = gamma x delta"]
    panels = []
    for g, gname in GROUPS_N:
        rows = []
        for lo, hi in BANDS:
            if g in ("BW", "HW"):
                c1 = prod(E(K("c4_1", "g", lo, hi, g[0], "netw_e")), E(K("c4_aux", "netw_e", lo, hi, g[0])))
                c2 = prod(E(K("c4_1", "g", lo, hi, "W", "netw_e")), E(K("c4_aux", "netw_e", lo, hi, "W")))
                comp = lin([(c1, 1.0), (c2, -1.0)]) if c1 and c2 else None
            else:
                comp = prod(E(K("c4_1", "g", lo, hi, g, "netw_e")), E(K("c4_aux", "netw_e", lo, hi, g)))
            es = [G("c4_0", "g", lo, hi, g), G("c4_1", "g", lo, hi, g), comp]
            rows.append((f"ln parental income, sons {lo}-{hi}", [cell(e) for e in es]))
            rows.append((f"found through friends / relatives, {lo}-{hi}", ["", cell(G("c4_1", "g", lo, hi, g,
                                                                                   "netw_e")), ""]))
            for h, e in zip(hdr4, es):
                rec("C4 NLSY79 network job", gname, h, f"{lo}-{hi}", e)
            if g not in ("BW", "HW"):
                k_ = K("c4_0", "g", lo, hi, g)
                k0 = K("a1", "g", lo, hi, g)
                sh = f" ({100 * RES[k_]['n'] / RES[k0]['n']:.0f}% of all pairs)" if k_ in RES and k0 in RES else ""
                rows.append((f"N pairs / men / clusters, {lo}-{hi}",
                             [f"{RES[k_]['n']:,} / {RES[k_]['men']:,} / {RES[k_]['G']:,}{sh}" if k_ in RES else ""]
                             * 3))
        panels.append((gname, rows))
    md += ["### C4. Job found through friends / relatives (parental / social network)", "",
           "Only employers held at an interview in 1994-2000 have the job-finding questions, so this is a subsample "
           "(share in the N row); at 25-34 it covers mainly the youngest cohorts. Controls: quartic in age, round FE.",
           ""]
    md += table(hdr4, panels)


# ================================================================ figure
def figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ink, muted, grid, bg = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    col = {"W": "#2a78d6", "B": "#eb6834"}
    items = [("PSID: baseline", "pB_b01", "g"), ("PSID: occ x ind cell FE (first interview)", "pB_b03", "g"),
             ("PSID: + start wage", "pB_b05", "g"), ("PSID: + wage at t-2", "pB_b07", "g"),
             ("PSID: + education", "pB_b08", "g"), ("PSID: + educ + wage t-2 + cell FE", "pB_b09", "g"),
             ("PSID: 2-interval growth", "pB_b10", "g2"), ("PSID: strict stayers", "pB_b13", "g_strict"),
             ("PSID: trimmed 1%", "pB_b12", "g_trim"),
             ("NLSY79: baseline", "a1", "g"), ("NLSY79: common sample", "a2", "g"), ("NLSY79: + AFQT", "a3", "g"),
             ("NLSY79: + education", "a4", "g"), ("NLSY79: + AFQT + education", "a5", "g"),
             ("NLSY79: + AFQT + educ + cell FE", "a7", "g"), ("NLSY79: + wage at t-2", "nB_b07", "g"),
             ("NLSY79: 2-interval growth", "nB_b10", "g2")]
    fig, ax = plt.subplots(figsize=(10, 7.6))
    fig.patch.set_facecolor(bg)
    yy = np.arange(len(items))[::-1]
    for j, g in enumerate(("W", "B")):
        for y0, (lab, tag, outc) in zip(yy, items):
            b, se, p = tsp(E(K(tag, outc, 25, 34, g)))
            if not np.isfinite(b):
                continue
            ax.errorbar(b, y0 + (0.15 if g == "W" else -0.15), xerr=1.96 * se, fmt="o", ms=6, color=col[g],
                        ecolor=col[g], elinewidth=1.5, capsize=0, mec=bg, mew=1.2,
                        label=("White sons" if g == "W" else "Black sons") if y0 == yy[0] else None)
    ax.axvline(0, color=muted, lw=1)
    ax.set_yticks(yy, [lab for lab, *_ in items], color=ink, fontsize=9)
    ax.set_xlabel("Coefficient on ln parental income: annual same-employer ln wage growth, ages 25-34 (95% CI)",
                  color=muted)
    ax.set_facecolor(bg)
    ax.grid(axis="x", color=grid, lw=0.8)
    ax.set_axisbelow(True)
    for sp_ in ("top", "right", "left"):
        ax.spines[sp_].set_visible(False)
    ax.spines["bottom"].set_color(muted)
    ax.tick_params(colors=muted, length=0)
    ax.axhline(yy[8] - 0.5, color=muted, lw=0.8)
    ax.legend(frameon=False, loc="lower right", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / "same_employer_growth_checks.png", dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)


# ================================================================ main
def main():
    global CL
    OUT.mkdir(exist_ok=True)
    print("PSID ...", flush=True)
    r, D32, D27, W, M, XWD = psid_build()
    s, sp = psid_pairs(r)
    print("NLSY79 ...", flush=True)
    J, kids = nlsy_build(D32, D27, W, M, XWD)
    n_s, n_sp = nlsy_samples(J)
    CL = pd.Index(np.unique(np.concatenate([r["fam68"].dropna().unique().astype(float),
                                            J["cl"].dropna().unique().astype(float)])))
    md = ["# Same-employer wage growth by parental income: ability, measurement and sources", "",
          "Built by `36.SameEmployerGrowthChecks.py` (2026-10-17); definitions in its docstring. Every coefficient: "
          "estimate (s.e.; p), *** p<0.01, ** p<0.05, * p<0.1; s.e. clustered by 1968 family (PSID) / 1979 household "
          "(NLSY79). **Descriptive: sons select into employers; nothing here is a causal effect of parental income, "
          "ability or race.**", "", "SUMMARY_PLACEHOLDER", ""]
    # ---- samples
    chk = kids.attrs["check"]
    afq = kids.dropna(subset=["afqt"])
    md += ["## 0. Samples and variables", "",
           f"- PSID same-employer pairs (32 Section 3): {len(s):,} pairs of {s['pid'].nunique():,} Black and White "
           f"sons; trimming bounds for (10): {s.attrs['trim'][0]:.3f} / {s.attrs['trim'][1]:.3f}.",
           f"- NLSY79 men living with a parent in 1979 with parental income: {len(kids):,} (Black "
           f"{(kids['race'] == 'Black').sum():,}, White {(kids['race'] == 'White').sum():,}, Hispanic "
           f"{(kids['race'] == 'Hispanic').sum():,}). Parental income re-built here: White / Black men in "
           f"data/nlsy79_kids.pkl {chk[0]:,}, matched {chk[1]:,}, max |difference| {chk[2]:.2e}.",
           f"- NLSY79 CPS-job person-rounds at 25-55: {len(J):,}; consecutive pairs 1-2 years apart: "
           f"{int(J['same'].notna().sum()):,}, of which same employer {int((J['same'] == 1).sum()):,} "
           f"({100 * (J['same'] == 1).sum() / J['same'].notna().sum():.0f}%); with valid wages at both rounds: "
           f"{len(n_s):,} pairs of {n_s['pid'].nunique():,} men. Trimming bounds: {n_s.attrs['trim'][0]:.3f} / "
           f"{n_s.attrs['trim'][1]:.3f}.",
           f"- AFQT-3 (R0618301) known for {len(afq):,} of the {len(kids):,} men; age-adjusted score: mean (s.d.) by "
           "race " + ", ".join(f"{g_} {z['afqt'].mean():.2f} ({z['afqt'].std():.2f})"
                               for g_, z in afq.groupby("race")) + ". Education known for "
           f"{int(kids['educ'].notna().sum()):,}; mean years " + ", ".join(
               f"{g_} {z['educ'].mean():.1f}" for g_, z in kids.groupby("race")) + ".",
           "- Coverage among NLSY79 same-employer pairs at 25-34 (share non-missing): " + ", ".join(
               f"{c} {100 * n_s.loc[n_s['age'].between(25, 34), c].notna().mean():.0f}%"
               for c in ("afqt", "educ", "ddx", "cell", "train_any", "train_hrs", "union", "lnemp_e", "multi_e",
                         "netw_e", "ten0", "lwm2", "g2")) + ".", ""]
    # ---- baseline reproduction
    sec_baseline_psid(s, md)
    rows = []
    for g, gname in GROUPS_P:
        rows.append((gname, [cell(G(t, "g", lo, hi, g)) for t in ("p_base", "p_ddx") for lo, hi in BANDS]))
    md += ["### 0a. PSID baseline reproduced (32 Section 3, columns 1 and 3)", ""]
    md += table(["(1) growth 25-34", "(1) growth 35-55", "(3) + fine-industry FE, 25-34",
                 "(3) + fine-industry FE, 35-55"], [("", rows)])
    print("A ...", flush=True)
    sec_A(n_s, md)
    print("B ...", flush=True)
    hdr, panels, infoP = sec_B(s, sp, md, "PSID", None, "pB_")
    md += ["## B. Measurement checks", "", "### B1. PSID", "",
           "Same-employer pairs of 32 Section 3. (2) fixed effects of the cell (11 occupation groups x 33 industry "
           "groups) at the later interview, which can be an outcome of within-employer upgrading; (3)-(4) codes at the "
           "first interview of the pair (predetermined). (5) ln wage of the earlier income year of the pair; (6) the "
           "same relative to the son's cell, net of an age quartic and year FE, estimated on all Black and White "
           "son-years; (7) ln wage at the interview before the pair (any employer, <= 4 years earlier), which is not "
           "mechanically related to transitory error in the first wage of the pair. (9) joint. (10) growth over two "
           "consecutive pairs when tenure covers both (same employer at three interviews). (11) one observation per "
           "run of consecutive stayer interviews (>= 3 interviews, >= 3 years), age band by the midpoint age. (13) "
           "PSID wages are annual earnings / hours of the calendar year before the interview, so a son who joined his "
           "employer shortly before the first interview of a pair has a first-year wage partly from the previous job; "
           "strict stayers have tenure covering both income years. 'change vs (1)' = difference from column (1) with "
           "s.e. from the joint influence functions (samples differ in (7), (9)-(13): see N).", ""]
    md += table(hdr, panels)
    hdr, panels, infoN = sec_B(n_s, n_sp, md, "NLSY79", None, "nB_")
    md += ["### B2. NLSY79", "",
           "Same-employer pairs of Table A column (1) (employer observed directly). (4)-(6) as B1 with the hourly pay "
           "rate at the interview; (10) the same roster employer at three consecutive CPS-job rounds; (11) runs of "
           "consecutive same-employer links (>= 3 rounds, >= 3 years); (13) without self-employed jobs.", ""]
    md += table(hdr, panels)
    md += ["**Conditioning on the starting wage.** Columns (5)-(6) condition on the first wage of the pair. If that "
           "wage contains transitory error or a transitory component, growth is mechanically negatively related to it "
           "(regression to the mean), and conditioning on it also conditions on an outcome of parental income (sons "
           "of richer parents start higher), so the coefficient on parental income is then a within-starting-level "
           "comparison that can be biased in either direction. Column (7) uses the wage one interview earlier, which "
           "shares no transitory error with the growth outcome if the error is serially uncorrelated. Because sons of "
           "richer parents have higher wages and growth is strongly negatively related to the starting wage (the "
           "'added control' rows), conditioning on the start RAISES the parental-income coefficient: catch-up after a "
           "low start or regression to the mean would work against, not for, the gradient. (5)-(6) mix this with the "
           "mechanical error term; (7) is the cleaner version.", ""]
    print("C ...", flush=True)
    sec_C(n_s, md)
    figure()
    pd.DataFrame(CSV).dropna(axis=1, how="all").to_csv(OUT / "same_employer_growth_checks.csv", index=False)
    summ = summary()
    md = [summ if x == "SUMMARY_PLACEHOLDER" else x for x in md]
    (OUT / "same_employer_growth_checks.md").write_text("\n".join(md), encoding="utf-8")
    print(summ)


def summary():
    def c(e):
        return cell(e) or "n/a"

    def g_(tag, y, g, lo=25, hi=34, x="lyp"):
        return c(G(tag, y, lo, hi, g, x))
    L = ["## Summary", ""]
    L.append("- **PSID baseline (25-34)**: White " + g_("pB_b01", "g", "W") + ", Black " + g_("pB_b01", "g", "B")
             + ", Black - White " + g_("pB_b01", "g", "BW") + "; pooled " + g_("pB_b01", "g", "P") + ".")
    L.append("- **NLSY79 analogue (same roster employer, 25-34)**: White " + g_("a1", "g", "W") + ", Black "
             + g_("a1", "g", "B") + ", Hispanic " + g_("a1", "g", "H") + ", pooled " + g_("a1", "g", "P")
             + "; 35-55: White " + g_("a1", "g", "W", 35, 55) + ", Black " + g_("a1", "g", "B", 35, 55) + ".")
    L.append("- **A. Ability (NLSY79, 25-34)**: common sample White " + g_("a2", "g", "W") + " -> + AFQT "
             + g_("a3", "g", "W") + " -> + AFQT + education " + g_("a5", "g", "W") + " -> + cell FE "
             + g_("a7", "g", "W") + "; Black " + g_("a2", "g", "B") + " -> " + g_("a3", "g", "B") + " -> "
             + g_("a5", "g", "B") + " -> " + g_("a7", "g", "B") + "; pooled " + g_("a2", "g", "P") + " -> "
             + g_("a5", "g", "P") + ". AFQT gradient of growth (AFQT alone): White " + g_("b1", "g", "W", x="afqt")
             + ", Black " + g_("b1", "g", "B", x="afqt") + ", Hispanic " + g_("b1", "g", "H", x="afqt")
             + ", AFQT x Black " + g_("b1", "g", "BW", x="afqt") + ".")
    for g, nm in (("W", "White"), ("B", "Black"), ("BW", "Black - White")):
        L.append(f"- **B. Measurement (PSID, {nm} 25-34)**: baseline " + g_("pB_b01", "g", g) + "; cell FE later "
                 "interview " + g_("pB_b02", "g", g) + "; cell FE first interview " + g_("pB_b03", "g", g)
                 + "; detailed occ + industry FE (first) " + g_("pB_b04", "g", g) + "; + start wage "
                 + g_("pB_b05", "g", g) + "; + relative wage " + g_("pB_b06", "g", g) + "; + wage at t-2 "
                 + g_("pB_b07", "g", g) + "; + education " + g_("pB_b08", "g", g) + "; + education + wage t-2 + "
                 "cell FE " + g_("pB_b09", "g", g) + "; 2-interval " + g_("pB_b10", "g2", g) + "; spells "
                 + g_("pB_b11", "g_sp", g) + "; trimmed " + g_("pB_b12", "g_trim", g) + "; strict stayers "
                 + g_("pB_b13", "g_strict", g) + ".")
    L.append("- **B. Measurement (NLSY79, White 25-34)**: cell FE first " + g_("nB_b03", "g", "W") + "; + education "
             + g_("nB_b08", "g", "W") + "; + wage at t-2 " + g_("nB_b07", "g", "W") + "; 2-interval "
             + g_("nB_b10", "g2", "W") + "; trimmed " + g_("nB_b12", "g_trim", "W") + "; no self-employed "
             + g_("nB_b13", "g_nose", "W") + ".")
    L.append("- **C. Sources (NLSY79, 25-34, White)**: base " + g_("c2_0", "g", "W") + " -> all sources "
             + g_("c2_all", "g", "W") + "; company training on parental income " + g_("c1", "train_comp", "W")
             + ", union " + g_("c1", "union", "W") + ", ln employees " + g_("c1", "lnemp_e", "W") + ".")
    L.append("- (Numbers above are generated; the lead's interpretation goes in the paper.)")
    return "\n".join(L)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        x = nlsy_extract()
        print(x.shape)
    else:
        main()
