r"""Industry careers and the IGE: do sons of richer parents sort into industries with steep career wage growth, and
do sons follow their fathers into industries? (2026-10-17)

Question (PI): 27.CareerWageGrowth.py showed that the post-35 Black-White divergence in wage persistence is ~1/5
occupational upgrading and ~4/5 within-occupation wage growth (largely with the same employer at 25-34). What about
INDUSTRY? Do sons of richer (White) parents sort into industries with steep wage growth later in the career (finance,
law / professional services), so that industry explains the post-30s divergence? Extension (PI): do sons follow the
FATHER into his industry / occupation (a parental-network / social-capital channel), and does following pay off in
career wage growth? General pattern (pooled) first, then race. DESCRIPTIVE ACCOUNTING: sons select into industries,
occupations and employers; nothing here identifies a causal effect of parental income, race or the father's industry.

DATA (raw and downloaded data read only)
  PSID  sons = 27.CareerWageGrowth.py's son panel (24's child-year frame: 6.IGEMain parents, male heads 25-55, valid
        wage years), loaded read-only via importlib (27 -> 24 caches), with 27's occupation (occ1990dd), occupational
        wage score, tenure and the interview-to-interview growth / same-employer split.
        Head's industry at the interview of wave w (paired with the wage of income year w - 1, as the occupation in 27):
          1968-1975 'INDUSTRY OF HEAD yy' (retrospective 1970 Census codes; 23.CorrelatedShocks.py cache
                    data/correlated_shocks_fam.pkl, h_ind_r);
          1976-2023 18.HusbandIndustryShocks.py cache data/husband_shocks_fam.pkl, h_code = main industry of the
                    employed head, else industry of the last job of the unemployed head: 1970 codes to 2001, 3-digit 2000
                    codes 2003-2015, 4-digit 2012 codes 2017-2023.
        Father = 24's fpid (male head of the son's family at the wave closest to age 16); his industry / occupation =
        modal code over his head-waves in which the son was 12-18 (wave - son's birth year).
  Industry harmonisation (downloaded into data/ext/ind_crosswalk/, treated as data):
        common fine scheme = Autor-Dorn-Hanson ind1990ddx (balanced 1990-Census-based industries; Dorn's crosswalks
        cw_ind1980_ind1990ddx, cw_ind1990_ind1990ddx, cw_ind2000_ind1990ddx (weighted), ddorn.net/data.htm [C5]-[C7];
        Autor, Dorn and Hanson 2019 AER: Insights).
        1970 codes -> 1980 codes: Census Bureau Technical Paper table 'The 1980 Industry Categories As Derived From
        The 1970 Industry Classification System' (IPUMS USA, usa.ipums.org/usa/resources/chapter4/ind_70-80.xls;
        converted verbatim to ind_70-80.csv with xlrd 2.0.1 because the project environment has no .xls reader);
        weights = MALE experienced civilian labor force in each 1970 x 1980 cell, then 1980 -> ind1990ddx (Dorn).
        2012 4-digit codes (PSID 2017-23) and CPS 4-digit 2002 codes: code // 10 = 2000 3-digit code (the convention of
        18 / 27); codes without a match are recoded to the nearest lower 2000 code within the same hundred (listed in
        the .md).
        A source code that maps to several ind1990ddx industries gets the WEIGHTED mean of their measures and the modal
        industry / group for classification ('same industry as the father' compares modal codes).
        INDUSTRY GROUPS (33, defined on 1990 / ind1990ddx code ranges, list in IGRP below): separate finance (banking,
        credit, securities), insurance, real estate, legal services, engineering / accounting / research / management
        consulting (professional services), computer and data processing, other business services, hospitals, other
        health, education, public administration, nine manufacturing groups, etc.
  Industry measures (CPS MORG, Dropbox/MORG/morgYY.dta, read only, base 1992-2002 = native 1990 codes, men 25-64, hourly
        wage as in 27: earnhre/100 if paid by the hour, else earnwke (x1.4 if top-coded) / uhourse, 2000 $, $2-$200,
        earnings weights; rel = ln w - weighted mean ln w of all men 25-64 in the year; t = (age - 40) / 10):
          rel = f(t) + P_j + B_j t + e,   f = common quartic,
        P_j = industry wage level (premium at age 40 relative to all men), B_j = industry-specific slope of the age-wage
        profile (log points per 10 years of age relative to the employment-weighted average industry; both normalised to
        weighted mean 0). Estimated exactly by Frisch-Waugh (industry-specific intercepts and slopes partialled out).
        Fine level ind1990ddx (cells < 200 men take their group's values) and group level. Also per group: raw wage
        growth (mean rel at 45-55 minus 25-34) and the return to potential experience (growth from 5 to 25 years,
        within-group regression with years of schooling from grade92).
        Joint occupation x industry model: rel = f(t) + O_o + P_j + B_j t (occ1990dd fixed effects + industry intercepts
        and slopes, alternating projections) -> occupation premium net of industry, industry premium and slope net of
        occupation.
  NLSY79 (check; Dropbox/NLS, read only): 27's CPS-job panel (men living with a parent in 1979), industry of the CPS job
        from the employer roster EMPLOYERS_ALL_IND_<round>.<JJ> (1970 codes to 2000, 2000 codes from 2002); cache
        data/industry_careers_nlsy79.pkl. No father's industry in this check.
DESIGN
  ln w = P (industry level) + B x t (industry-specific career-slope component) + residual (within industry). As in 27,
  the son's outcome is regressed on ln parental income by age band with Lee-Solon controls; the coefficient on ln w is
  the sum of the coefficients on the pieces (same sample: valid wage, mapped industry AND mapped occupation, so the
  occupation-only split of 27 is reproduced on the same son-years). All cells are stacked (influence functions,
  clusters = 1968 family) so differences across bands / races and shares have s.e. Pooled = Black + White weighted;
  by race unweighted (24 / 27). The PSID has no employer identifiers: 'same employer as the father' is not observable.
Every table: one regression per column (outcome in the header), regressors as rows, N / clusters at the bottom,
coefficient (s.e.; p) with *** p<0.01, ** p<0.05, * p<0.1.
Writes output/industry_careers.csv, output/industry_careers.md, output/industry_careers.png; caches
data/industry_careers_morg.pkl, data/industry_careers_nlsy79.pkl.
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

from common import DATA, OUT, HERE, CPI, stars

warnings.simplefilter("ignore", FutureWarning)
warnings.simplefilter("ignore", RuntimeWarning)
warnings.simplefilter("ignore", pd.errors.PerformanceWarning)
pd.set_option("display.width", 250)


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


D27 = _load("d27", "27.CareerWageGrowth.py")
D24 = D27.D24
MORG = D27.MORG
XWI = DATA / "ext" / "ind_crosswalk"
NLS = D27.NLS
C_MORG, C_NLS = DATA / "industry_careers_morg.pkl", DATA / "industry_careers_nlsy79.pkl"
BASE = (1992, 2002)
MIN_FINE = 200

# ---------------------------------------------------------------- 33 industry groups on 1990 / ind1990ddx codes
IGRP = [
    ("Agriculture, forestry, fishing", [(10, 32)]),
    ("Mining", [(40, 50)]),
    ("Construction", [(60, 60)]),
    ("Mfg: food, tobacco", [(100, 130)]),
    ("Mfg: textiles, apparel, leather", [(132, 152), (220, 222)]),
    ("Mfg: paper, printing, publishing", [(160, 172)]),
    ("Mfg: chemicals, petroleum, rubber, plastics", [(180, 212)]),
    ("Mfg: wood, furniture, stone, glass", [(230, 262)]),
    ("Mfg: primary and fabricated metals", [(270, 301)]),
    ("Mfg: machinery and computers", [(310, 332)]),
    ("Mfg: electrical equipment", [(340, 350)]),
    ("Mfg: motor vehicles, aircraft, other transport eq.", [(351, 370)]),
    ("Mfg: instruments, misc. manufacturing", [(371, 392)]),
    ("Transportation (excl. postal)", [(400, 411), (420, 432)]),
    ("Communications", [(440, 442)]),
    ("Utilities and sanitary services", [(450, 472)]),
    ("Wholesale trade", [(500, 571)]),
    ("Retail trade (excl. eating, drinking)", [(580, 640), (642, 691)]),
    ("Eating, drinking, hotels", [(641, 641), (762, 770)]),
    ("Finance: banking, credit, securities", [(700, 710)]),
    ("Insurance", [(711, 711)]),
    ("Real estate", [(712, 712)]),
    ("Computer and data processing services", [(732, 732)]),
    ("Other business services", [(721, 731), (740, 741)]),
    ("Automotive and repair services", [(742, 760)]),
    ("Personal services, entertainment", [(761, 761), (771, 810)]),
    ("Hospitals", [(831, 831)]),
    ("Other health services", [(812, 830), (832, 840)]),
    ("Legal services", [(841, 841)]),
    ("Education", [(842, 860)]),
    ("Social services, religious, membership", [(861, 881)]),
    ("Professional services (engineering, accounting, research, consulting)", [(882, 893)]),
    ("Public administration (incl. postal)", [(412, 412), (900, 932)]),
]
GNAMES = [g for g, _ in IGRP]
FIRE = {GNAMES.index(g) for g in ("Finance: banking, credit, securities", "Insurance", "Real estate")}
LEGPRO = {GNAMES.index(g) for g in ("Legal services",
                                    "Professional services (engineering, accounting, research, consulting)")}
BUSSV = {GNAMES.index(g) for g in ("Computer and data processing services", "Other business services")}


def group_of(code):
    c = np.asarray(code, float)
    g = np.full(len(c), np.nan)
    for k, (_, rr) in enumerate(IGRP):
        for lo, hi in rr:
            g[(c >= lo) & (c <= hi)] = k
    return g


# ================================================================ industry crosswalks
def ind_crosswalks():
    """{scheme: {code: [(ind1990ddx, weight), ...]}} for schemes 1970, 1980, 1990, 2000 (weights sum to 1)."""
    U = XWI / "unz"
    x80 = pd.read_stata(U / "cw_ind1980_ind1990ddx.dta")
    m80 = {int(a): int(b) for a, b in zip(pd.to_numeric(x80["ind1980"], errors="coerce"),
                                          pd.to_numeric(x80["ind1990ddx"], errors="coerce")) if a == a and b == b}
    x90 = pd.read_stata(U / "cw_ind1990_ind1990ddx.dta")
    m90 = {int(a): int(b) for a, b in zip(pd.to_numeric(x90["ind1990"], errors="coerce"),
                                          pd.to_numeric(x90["ind1990ddx"], errors="coerce")) if a == a and b == b}
    x00 = pd.read_stata(U / "cw_ind2000_ind1990ddx.dta")
    W = {"1980": {k: [(v, 1.0)] for k, v in m80.items()}, "1990": {k: [(v, 1.0)] for k, v in m90.items()}, "2000": {}}
    for a, b, w in zip(pd.to_numeric(x00["ind2000"], errors="coerce"), pd.to_numeric(x00["ind1990ddx"], errors="coerce"),
                       pd.to_numeric(x00["weight"], errors="coerce")):
        if a == a and b == b and w == w and w > 0:
            W["2000"].setdefault(int(a), []).append((int(b), float(w)))
    # 1970 -> 1980 from the Census Bureau table (male experienced civilian labor force), then 1980 -> ddx
    t = pd.read_csv(XWI / "ind_70-80.csv", header=None, dtype=str, keep_default_na=False)
    cur, pairs = None, []
    for _, row in t.iterrows():
        c0, c1 = row[0].strip(), row[1].strip()
        if re.fullmatch(r"\d{1,3}", c0) and not c1:
            cur = int(c0)
        elif cur is not None and re.fullmatch(r"\d{1,3}", c1):
            try:
                male = float(row[5])
            except ValueError:
                continue
            if male > 0:
                pairs.append((int(c1), cur, male))
    p = pd.DataFrame(pairs, columns=["i70", "i80", "male"])
    p["ddx"] = p["i80"].map(m80)
    nomap = sorted(p.loc[p["ddx"].isna(), "i80"].unique())
    p = p.dropna(subset=["ddx"]).groupby(["i70", "ddx"])["male"].sum().reset_index()
    p["w"] = p["male"] / p.groupby("i70")["male"].transform("sum")
    W["1970"] = {int(k): [(int(a), float(b)) for a, b in zip(g["ddx"], g["w"])] for k, g in p.groupby("i70")}
    W["_nomap80"] = nomap
    W["_pairs70"] = len(pairs)
    return W


def code2000(c):
    """4-digit 2002 / 2007 / 2012 code -> 3-digit 2000 code (// 10)."""
    return np.floor(np.asarray(c, float) / 10)


def map_codes(code, scheme, W, meas=None, recode=None):
    """modal ind1990ddx, modal group and (if meas = {ddx: (P, B, ...)}) the weighted measures of each code."""
    code = np.asarray(code, float)
    sch = np.asarray(scheme, object)
    out_dd = np.full(len(code), np.nan)
    out_g = np.full(len(code), np.nan)
    K = 0 if meas is None else len(next(iter(meas.values())))
    out_m = np.full((len(code), K), np.nan)
    cache = {}
    for i, (c, s) in enumerate(zip(code, sch)):
        if c != c or s is None:
            continue
        key = (s, int(c))
        if key not in cache:
            ss, cc = s, int(c)
            if s == "2012":
                ss, cc = "2000", int(cc // 10)
            if ss == "2000" and recode is not None:
                cc = recode.get(cc, cc)
            lst = W[ss].get(cc)
            if not lst:
                cache[key] = None
            else:
                dd = pd.Series({}, dtype=float)
                for d, w in lst:
                    dd[d] = dd.get(d, 0.0) + w
                gg = pd.Series(dd.values, index=group_of(dd.index.to_numpy())).groupby(level=0).sum()
                m = None
                if meas is not None:
                    ok = [(meas[d], w) for d, w in lst if d in meas]
                    if ok:
                        ws = sum(w for _, w in ok)
                        m = np.sum([np.asarray(v) * w for v, w in ok], axis=0) / ws
                cache[key] = (float(dd.idxmax()), float(gg.idxmax()) if len(gg.dropna()) else np.nan, m)
        r = cache[key]
        if r is None:
            continue
        out_dd[i], out_g[i] = r[0], r[1]
        if r[2] is not None:
            out_m[i] = r[2]
    return out_dd, out_g, out_m


def recode2000(W, codes):
    """unmatched 3-digit 2000 codes -> nearest lower matched code in the same hundred."""
    have = np.array(sorted(W["2000"]))
    rc = {}
    for c in sorted(set(int(x) for x in codes if x == x)):
        if c in W["2000"] or c >= 960:                          # 967-987: armed forces (left unmapped)
            continue
        cand = have[(have <= c) & (have // 100 == c // 100)]
        if len(cand):
            rc[c] = int(cand.max())
    return rc


# ================================================================ CPS MORG base-period microdata
EDUC92 = {31: 0, 32: 2.5, 33: 5.5, 34: 7.5, 35: 9, 36: 10, 37: 11, 38: 11.5, 39: 12, 40: 13, 41: 14, 42: 14, 43: 16,
          44: 18, 45: 19, 46: 20}


def morg_micro(W, XWD):
    if C_MORG.exists():
        return pd.read_pickle(C_MORG)
    rows = []
    for y in range(BASE[0], BASE[1] + 1):
        f = MORG / f"morg{y % 100:02d}.dta"
        cols = list(pd.read_stata(f, iterator=True).variable_labels())
        want = [c for c in ("age", "sex", "race", "earnwt", "paidhre", "earnhre", "earnwke", "uhourse", "ind80", "occ80",
                            "grade92") if c in cols]
        d = pd.read_stata(f, columns=want, convert_categoricals=False)
        for c in d.columns:
            d[c] = pd.to_numeric(d[c], errors="coerce")
        d = d[(d["sex"] == 1) & d["age"].between(25, 64)].copy()
        top = 999 if y <= 1988 else 1923 if y <= 1997 else 2884.61
        wk = d["earnwke"].where(d["earnwke"] > 0)
        wk = np.where(wk >= top - 0.5, wk * 1.4, wk)
        hr = d["uhourse"].where(d["uhourse"] > 0)
        w = np.where((d["paidhre"] == 1) & (d["earnhre"] > 0), d["earnhre"] / 100, wk / hr)
        w = pd.Series(w, index=d.index) * CPI[2000] / CPI[y]
        d["lw"] = np.log(w.where(w.between(2, 200)))
        d["wt"] = d["earnwt"].where(d["earnwt"] > 0)
        d = d.dropna(subset=["lw", "wt"])
        d["rel"] = d["lw"] - np.average(d["lw"], weights=d["wt"])
        d["ddx"] = d["ind80"].map(lambda c: W["1990"][int(c)][0][0] if c == c and int(c) in W["1990"] else np.nan)
        d["occ"] = D27.to_dd(d["occ80"].to_numpy(), "1990", XWD)
        d["educ"] = d["grade92"].map(EDUC92) if "grade92" in d else np.nan
        d["year"] = y
        d = d[d["ddx"].notna() & (d["ddx"] < 940)]
        rows.append(d[["year", "age", "race", "wt", "lw", "rel", "ddx", "occ", "educ"]].astype(float))
        print(f"  MORG {y}: {len(d):,} men 25-64 with wage and industry", flush=True)
    m = pd.concat(rows, ignore_index=True)
    m.to_pickle(C_MORG)
    return m


def fwl_profiles(y, t, g, w, P=None):
    """y = f(t) + a_g + b_g t, f quartic without constant / linear term: exact FWL. Returns a, b (by g), gamma."""
    gi, gu = pd.factorize(g)
    G = len(gu)

    def within(v):
        s0 = np.bincount(gi, w, G)
        s1 = np.bincount(gi, w * t, G)
        s2 = np.bincount(gi, w * t * t, G)
        r0 = np.bincount(gi, w * v, G)
        r1 = np.bincount(gi, w * t * v, G)
        det = s0 * s2 - s1 ** 2
        det = np.where(np.abs(det) < 1e-12, np.nan, det)
        a = (s2 * r0 - s1 * r1) / det
        b = (s0 * r1 - s1 * r0) / det
        return v - np.nan_to_num(a[gi]) - np.nan_to_num(b[gi]) * t, a, b
    Z = np.column_stack([t ** 2, t ** 3, t ** 4])
    Zr = np.column_stack([within(Z[:, k])[0] for k in range(3)])
    yr = within(y)[0]
    gam = np.linalg.solve(Zr.T @ (Zr * w[:, None]), Zr.T @ (yr * w))
    _, a, b = within(y - Z @ gam)
    return pd.Series(a, index=gu), pd.Series(b, index=gu), gam


def morg_measures(m):
    """industry level P and slope B (fine ddx and 33 groups), group descriptives, joint occupation x industry model."""
    m = m.copy()
    m["t"] = (m["age"] - 40) / 10
    m["grp"] = group_of(m["ddx"].to_numpy())
    m = m[m["grp"].notna()].copy()
    w, t, y = m["wt"].to_numpy(), m["t"].to_numpy(), m["rel"].to_numpy()
    out = {}
    for lev in ("ddx", "grp"):
        a, b, gam = fwl_profiles(y, t, m[lev].to_numpy(), w)
        sh = m.groupby(lev)["wt"].sum()
        sh = sh / sh.sum()
        a = a - (a * sh).sum()
        b = b - (b * sh).sum()
        n = m.groupby(lev).size()
        out[lev] = pd.DataFrame({"P": a, "B": b, "n": n, "share": sh})
        out[f"gam_{lev}"] = gam
    F, Gd = out["ddx"], out["grp"]
    F["grp"] = group_of(F.index.to_numpy())
    small = F["n"] < MIN_FINE
    F.loc[small, "P"] = F.loc[small, "grp"].map(Gd["P"])
    F.loc[small, "B"] = F.loc[small, "grp"].map(Gd["B"])
    F["small"] = small
    # group descriptives: raw growth 25-34 -> 45-55, return to potential experience 5 -> 25 years (schooling held fixed)
    desc = []
    for g, z in m.groupby("grp"):
        r0 = np.average(z.loc[z["age"].between(25, 34), "rel"], weights=z.loc[z["age"].between(25, 34), "wt"])
        r1 = np.average(z.loc[z["age"].between(45, 55), "rel"], weights=z.loc[z["age"].between(45, 55), "wt"])
        zz = z.dropna(subset=["educ"])
        x = ((zz["age"] - zz["educ"] - 6).clip(lower=0) / 10).to_numpy()
        X = np.column_stack([np.ones(len(zz)), x, x ** 2, zz["educ"].to_numpy(),
                             pd.get_dummies(zz["year"].astype(int), drop_first=True, dtype=float).to_numpy()])
        ww = zz["wt"].to_numpy()
        bb = np.linalg.lstsq(X * np.sqrt(ww)[:, None], zz["rel"].to_numpy() * np.sqrt(ww), rcond=None)[0]
        desc.append(dict(grp=g, raw_growth=r1 - r0, exp_return=2 * bb[1] + 6 * bb[2], ret_school=bb[3],
                         mean_educ=np.average(zz["educ"], weights=ww), black=np.average(z["race"] == 2, weights=z["wt"])))
    Gd = Gd.join(pd.DataFrame(desc).set_index("grp"))
    out["grp"] = Gd
    # steep / high-premium groups: top quartile of men's employment distribution
    def topq(col):
        s = Gd.sort_values(col, ascending=False)
        cum = s["share"].cumsum()
        return set(s.index[(cum - s["share"]) < 0.25].astype(int))
    out["steep"] = topq("B")
    out["highP"] = topq("P")
    # joint occupation x industry (fine) model by alternating projections
    j = m[m["occ"].notna()].copy()
    wj, tj, yj = j["wt"].to_numpy(), j["t"].to_numpy(), j["rel"].to_numpy()
    oi, ou = pd.factorize(j["occ"])
    O = np.zeros(len(ou))
    for it in range(400):
        a, b, gam = fwl_profiles(yj - O[oi], tj, j["ddx"].to_numpy(), wj)
        ai = j["ddx"].map(a).to_numpy()
        bi = j["ddx"].map(b).to_numpy()
        Zg = np.column_stack([tj ** 2, tj ** 3, tj ** 4]) @ gam
        rr = yj - ai - bi * tj - Zg
        O_new = np.bincount(oi, wj * rr, len(ou)) / np.bincount(oi, wj, len(ou))
        dlt = np.max(np.abs(O_new - O))
        O = O_new
        if dlt < 1e-5:
            break
    so = pd.Series(np.bincount(oi, wj, len(ou)), index=ou)
    O = pd.Series(O, index=ou)
    c = (O * so).sum() / so.sum()
    O = O - c
    sh = j.groupby("ddx")["wt"].sum()
    sh = sh / sh.sum()
    a = a + c
    a = a - (a * sh).sum()
    b = b - (b * sh).sum()
    nj = j.groupby("ddx").size()
    a[nj.reindex(a.index).fillna(0) < MIN_FINE] = np.nan
    b[nj.reindex(b.index).fillna(0) < MIN_FINE] = np.nan
    out["joint"] = pd.DataFrame({"PJ": a, "BJ": b})
    out["jointO"] = O
    out["joint_iter"] = it + 1
    # variance shares in MORG
    out["var"] = dict(var_rel=np.average((y - np.average(y, weights=w)) ** 2, weights=w))
    out["N"] = len(m)
    out["Nfine"] = int((F["n"] >= MIN_FINE).sum())
    return out


# ================================================================ NLSY79 industry of roster jobs
def nlsy_ind_extract():
    if C_NLS.exists():
        return pd.read_pickle(C_NLS)
    ix = pd.read_csv(DATA / "nlsy79_codebook.csv")
    q = ix["qname"].astype(str)
    sel = ix[q.str.match(r"^EMPLOYERS_ALL_IND_\d{4}\.\d\d$")]
    cols = ["R0000100"] + sel["col"].tolist()
    print(f"NLSY79: reading {len(cols):,} industry columns from the full release (slow) ...", flush=True)
    d = pd.read_csv(NLS / "nlsy79_all_1979-2022.csv", usecols=cols)
    d = d.rename(columns={"R0000100": "pid", **dict(zip(sel["col"], sel["qname"]))})
    d.to_pickle(C_NLS)
    return d




# ================================================================ estimation helpers (27's stacked machinery)
RES, comb, ratio, cell, one = D27.RES, D27.comb, D27.ratio, D27.cell, D27.one
run_cells, table, ctrl_lsn, ctrl_ageyr = D27.run_cells, D27.table, D27.ctrl_lsn, D27.ctrl_ageyr
GROUPS3 = D27.GROUPS3
GROUPS4 = GROUPS3 + [("BW", "Black - White")]
CSV = []


def rec(tab, sample, outcome, term, t, n=np.nan, mean=np.nan, **kw):
    b, se, p = t
    CSV.append(dict(table=tab, sample=sample, outcome=outcome, term=term, coef=b, se=se, p=p, n=n, mean=mean, **kw))


def K(tag, y, lo, hi, g, x="x"):
    return ((tag, y, lo, hi, g), x)


def L(tag, y, lo, hi, g, x="x"):
    """linear combination for a group or the Black - White difference."""
    if g == "BW":
        return [(K(tag, y, lo, hi, "B", x), 1.0), (K(tag, y, lo, hi, "W", x), -1.0)]
    return [(K(tag, y, lo, hi, g, x), 1.0)]


def Dch(tag, y, g, b=(35, 55), a=(25, 34), x="x"):
    """(band b) - (band a) for a group or for the Black - White difference."""
    return [(k, c) for k, c in L(tag, y, *b, g, x)] + [(k, -c) for k, c in L(tag, y, *a, g, x)]


def safe(terms):
    return comb(terms) if all(k in RES for k, _ in terms) else (np.nan, np.nan, np.nan)


def sc(terms):
    return cell(safe(terms))


def dummies(v):
    return pd.get_dummies(pd.Series(v).astype(int), drop_first=True, dtype=float).to_numpy()


def mode(s):
    s = s.dropna()
    return s.value_counts().idxmax() if len(s) else np.nan


# ================================================================ PSID son panel with industries and fathers
def industry_codes():
    """wave x int: head's industry code and code scheme (1968-2023)."""
    F18 = pd.read_pickle(DATA / "husband_shocks_fam.pkl")[["wave", "int", "h_code"]]
    X = pd.read_pickle(DATA / "correlated_shocks_fam.pkl")["X"][["wave", "int", "h_ind_r", "h_occ"]]
    I = X.merge(F18, on=["wave", "int"], how="outer")
    c = pd.to_numeric(np.where(I["wave"] < 1976, I["h_ind_r"], I["h_code"]), errors="coerce")
    w = I["wave"].to_numpy()
    I["icode"] = pd.Series(c).where(((w < 2017) & pd.Series(c).between(1, 998)) |
                                    ((w >= 2017) & pd.Series(c).between(1, 9998))).to_numpy()
    I["isch"] = np.where(w <= 2001, "1970", np.where(w <= 2015, "2000", "2012"))
    return I.drop_duplicates(["wave", "int"])


def attach_industry(d, code_col, sch_col, W, M, rc, prefix=""):
    meas = {int(k): (v["P"], v["B"], M["joint"]["PJ"].get(k, np.nan), M["joint"]["BJ"].get(k, np.nan))
            for k, v in M["ddx"].iterrows()}
    dd, g, mm = map_codes(d[code_col].to_numpy(), d[sch_col].to_numpy(), W, meas, rc)
    dd[dd >= 940] = np.nan
    g[np.isnan(dd)] = np.nan
    d[prefix + "ddx"], d[prefix + "igrp"] = dd, g
    d[prefix + "P"], d[prefix + "B"], d[prefix + "PJ"], d[prefix + "BJ"] = (np.where(np.isnan(dd), np.nan, mm[:, k])
                                                                             for k in range(4))
    return d


def son_panel(W, M):
    XWD = D27.crosswalks()
    S = D27.SCORES = D27.scores(D27.morg_cells(XWD))
    r = D27.son_panel(XWD, S)
    I = industry_codes()
    rc = recode2000(W, np.concatenate([I.loc[I["isch"] == "2000", "icode"].dropna().to_numpy(),
                                       code2000(I.loc[I["isch"] == "2012", "icode"].dropna().to_numpy())]))
    r = r.merge(I[["wave", "int", "icode", "isch"]], on=["wave", "int"], how="left")
    r = attach_industry(r, "icode", "isch", W, M, rc)
    r["t"] = r["C"] / 10
    r["occ11"] = D27.group_of(r["dd"].to_numpy(float))
    r["jo"] = r["dd"].map(M["jointO"])
    ok = r["valid"] & r["lw"].notna() & r["P"].notna() & r["os"].notna() & r["jo"].notna() & r["PJ"].notna()
    r["dec"] = ok
    r["ip"] = r["P"].where(ok)
    r["ic"] = (r["B"] * r["t"]).where(ok)
    r["ipc"] = r["ip"] + r["ic"]
    r["ir"] = r["lw"].where(ok) - r["ipc"]
    r["os_c"] = r["os"].where(ok)
    r["ores"] = r["lw"].where(ok) - r["os_c"]
    r["jo"] = r["jo"].where(ok)
    r["jp"] = r["PJ"].where(ok)
    r["jc"] = (r["BJ"] * r["t"]).where(ok)
    r["jpc"] = r["jp"] + r["jc"]
    r["jr"] = r["lw"].where(ok) - r["jo"] - r["jpc"]
    for nm, st in (("fire", FIRE), ("legpro", LEGPRO), ("bussv", BUSSV), ("steep", M["steep"]), ("highp", M["highP"])):
        r[nm] = r["igrp"].isin(st).astype(float).where(r["igrp"].notna() & r["valid"])
    r["flb"] = ((r["fire"] == 1) | (r["legpro"] == 1) | (r["bussv"] == 1)).astype(float).where(r["fire"].notna())
    r["g_stay"] = r["g_lw_t"].where(r["stay"] == 1)
    # ---- fathers: modal industry / occupation over head-waves with the son aged 12-18
    a, _, _ = D24.load()
    fa = a[a["head"] & (a["female"] == 0)][["pid", "wave", "int"]].rename(columns={"pid": "fpid"})
    sons = r[["pid", "fpid", "birth_year"]].drop_duplicates("pid").dropna(subset=["fpid"])
    f = sons.merge(fa, on="fpid")
    f = f[(f["wave"] - f["birth_year"]).between(12, 18)].merge(I, on=["wave", "int"], how="left")
    f = attach_industry(f, "icode", "isch", W, M, rc, prefix="f_")
    oc = pd.to_numeric(f["h_occ"], errors="coerce")
    f["ocode"] = oc.where(((f["wave"] < 2017) & oc.between(1, 998)) | ((f["wave"] >= 2017) & oc.between(1, 9998)))
    f["osch"] = f["wave"].map(D27.occ_scheme)
    f = D27.attach_scores(f, "ocode", "osch", "wave", XWD, S)
    f["occ11"] = D27.group_of(f["dd"].to_numpy(float))
    fg = f.groupby("pid")
    fm = pd.DataFrame({"fgrp": fg["f_igrp"].agg(mode), "fddx": fg["f_ddx"].agg(mode), "fdd": fg["dd"].agg(mode),
                       "focc11": fg["occ11"].agg(mode), "fP": fg["f_P"].mean(), "fB": fg["f_B"].mean(),
                       "f_nw": fg["wave"].size(), "f_ni": fg["f_igrp"].count()})
    r = r.join(fm, on="pid")
    v = r["valid"]
    r["f_ind"] = (r["igrp"] == r["fgrp"]).astype(float).where(v & r["igrp"].notna() & r["fgrp"].notna())
    r["f_ddx"] = (r["ddx"] == r["fddx"]).astype(float).where(v & r["ddx"].notna() & r["fddx"].notna())
    r["f_occ"] = (r["occ11"] == r["focc11"]).astype(float).where(v & r["occ11"].notna() & r["focc11"].notna())
    r["f_occ3"] = (r["dd"] == r["fdd"]).astype(float).where(v & r["dd"].notna() & r["fdd"].notna())
    for nm, st in (("fire", FIRE), ("legpro", LEGPRO), ("bussv", BUSSV), ("steep", M["steep"]), ("highp", M["highP"])):
        r["fa_" + nm] = r["fgrp"].isin(st).astype(float).where(r["fgrp"].notna())
    r["fa_flb"] = ((r["fa_fire"] == 1) | (r["fa_legpro"] == 1) | (r["fa_bussv"] == 1)).astype(float).where(
        r["fgrp"].notna())
    # parental-income terciles (pooled Black + White sons, one value per son)
    s1 = r.drop_duplicates("pid")
    q = s1["lyp"].quantile([1 / 3, 2 / 3]).to_numpy()
    r["terc"] = np.where(r["lyp"] <= q[0], 1, np.where(r["lyp"] <= q[1], 2, 3)).astype(float)
    r.loc[r["lyp"].isna(), "terc"] = np.nan
    r.attrs["rc"] = rc
    r.attrs["fathers"] = f
    return r


# ================================================================ sections
BANDS = [(25, 34), (35, 44), (45, 55), (35, 55)]
DEC_Y = ("lw", "ip", "ic", "ir", "ipc", "os_c", "ores", "jo", "jp", "jc", "jpc", "jr")


def sec_morg(M, md, W, r):
    G = M["grp"].copy()
    rows = []
    for g, z in G.sort_values("B", ascending=False).iterrows():
        tag = (" (steep)" if int(g) in M["steep"] else "") + (" (high premium)" if int(g) in M["highP"] else "")
        rows.append(f"| {GNAMES[int(g)]}{tag} | {z['P']:.3f} | {z['B']:.3f} | {z['raw_growth']:.3f} | "
                    f"{z['exp_return']:.3f} | {z['ret_school']:.3f} | {z['mean_educ']:.1f} | {z['black']:.3f} | "
                    f"{z['share']:.3f} | {int(z['n']):,} |")
        for k, c in (("P", "P"), ("B", "B"), ("raw_growth", "raw growth 25-34 -> 45-55"),
                     ("exp_return", "return to experience 5 -> 25 years"), ("share", "employment share")):
            CSV.append(dict(table="0 MORG industry measures", sample="men 25-64, 1992-2002", outcome=c,
                            term=GNAMES[int(g)], coef=z[k], n=z["n"]))
    F = M["ddx"]

    def wsd(c):
        m_ = np.average(F[c], weights=F["share"])
        return float(np.sqrt(np.average((F[c] - m_) ** 2, weights=F["share"])))
    v = r[r["dec"]]
    cov = r[r["valid"]].groupby("isch").apply(lambda z: pd.Series({"sy": len(z), "code": z["icode"].notna().sum(),
                                                                   "mapped": z["ddx"].notna().sum(),
                                                                   "all": z["dec"].sum()}))
    rc = r.attrs["rc"]
    md += ["## 0. Industry harmonisation, the MORG industry measures and samples", "",
           f"Common fine scheme: Autor-Dorn-Hanson ind1990ddx ({len(F)} industries in the CPS MORG base period, "
           f"{M['Nfine']} with >= {MIN_FINE} men; smaller cells take their group's values), grouped into "
           f"{len(GNAMES)} industry groups. 1970 Census codes are bridged to 1980 codes with the Census Bureau's "
           f"1970 -> 1980 table ({W['_pairs70']} 1970 x 1980 cells, weights = male experienced civilian labor force; "
           f"{len(W['1970'])} 1970 codes mapped); 2000 codes with Dorn's weighted crosswalk; 4-digit 2002 / 2012 codes "
           "via code // 10, unmatched 3-digit 2000 codes recoded to the nearest lower code in the same hundred: "
           + (", ".join(f"{k}->{v_}" for k, v_ in sorted(rc.items())) or "none") + ".", "",
           f"CPS MORG men 25-64 with a wage and an industry, 1992-2002: {M['N']:,}. Model: rel = f(age) + P_j + B_j x "
           "(age - 40)/10; P = wage level at 40 relative to all men, B = industry-specific age slope per 10 years "
           "relative to the average industry (both employment-weighted mean 0). Across men (fine level) the s.d. of "
           f"P is {wsd('P'):.3f} and of B {wsd('B'):.3f}, i.e. moving from a -1 s.d. to a +1 s.d. slope industry adds "
           f"{4 * wsd('B'):.3f} log points of wage growth between ages 30 and 50. Joint occupation x industry model "
           f"(occ1990dd effects + industry intercepts and slopes) converged in {M['joint_iter']} iterations.", "",
           "Table 0. Industry groups (CPS MORG men 25-64, 1992-2002), sorted by the career slope B. 'Steep' / 'high "
           "premium' = top quartile of men's employment by B / P. Raw growth = mean relative ln wage at 45-55 minus "
           "25-34; return to experience = predicted wage growth from 5 to 25 years of potential experience with "
           "years of schooling held fixed (within-group regression, year FE). Descriptive industry averages "
           "(the composition of workers is not held fixed in P, B or raw growth).", "",
           "| Industry group | P (level at 40) | B (slope per 10 yrs) | raw growth 25-34 -> 45-55 | return to "
           "experience 5 -> 25 yrs | return to schooling | mean years of schooling | share Black | employment share | "
           "N men |", "|---|---|---|---|---|---|---|---|---|---|"] + rows
    md += ["", "| PSID industry code scheme (waves) | son-years with valid wage | with an industry code | mapped "
           "to ind1990ddx | in the decomposition sample (industry and occupation mapped) |", "|---|---|---|---|---|"]
    for s_, z in cov.iterrows():
        md.append(f"| {s_} ({'1968-2001' if s_ == '1970' else '2003-2015' if s_ == '2000' else '2017-2023'}) | "
                  f"{int(z['sy']):,} | {int(z['code']):,} | {int(z['mapped']):,} | {int(z['all']):,} |")
    ns = v.groupby("race")["pid"].nunique()
    md += ["", f"Decomposition sample: Black {ns.get('Black', 0):,} sons ({int((v['race'] == 'Black').sum()):,} "
           f"son-years), White {ns.get('White', 0):,} ({int((v['race'] == 'White').sum()):,}). Var(industry level P) "
           f"/ Var(ln wage) among son-years {np.var(v['ip']) / np.var(v['lw']):.3f}; Var(occupation score) / "
           f"Var(ln wage) {np.var(v['os_c']) / np.var(v['lw']):.3f}; corr(P, occupation score) "
           f"{np.corrcoef(v['ip'], v['os_c'])[0, 1]:.3f}; corr(B, occupation score) "
           f"{np.corrcoef(v['B'], v['os_c'])[0, 1]:.3f}.", ""]


def sec_decomp(r, md):
    info = run_cells("dec", r, DEC_Y, ("lyp",), ctrl_lsn, ("A", "C"), bands=BANDS)
    hdr = ["(1) ln wage", "(2) industry level P", "(3) industry career slope B x t", "(4) within-industry residual",
           "(5) industry share = [(2)+(3)]/(1)", "(6) occupation score (27)", "(7) joint: occupation part",
           "(8) joint: industry level", "(9) joint: industry slope part", "(10) joint: residual"]
    YS = ["lw", "ip", "ic", "ir", "share_ind", "os_c", "jo", "jp", "jc", "jr"]
    panels = []
    for g, gname in GROUPS4:
        rows = []
        for lo, hi in BANDS:
            t = [safe(L("dec", y, lo, hi, g)) for y in ("lw", "ip", "ic", "ir")]
            t.append(ratio(L("dec", "ipc", lo, hi, g), L("dec", "lw", lo, hi, g)))
            t += [safe(L("dec", y, lo, hi, g)) for y in ("os_c", "jo", "jp", "jc", "jr")]
            rows.append((f"ln parental income, sons {lo}-{hi}", [cell(x) for x in t]))
            for y, x in zip(YS, t):
                rec("1 decomposition", gname, y, f"lyp, {lo}-{hi}", x,
                    n=info.get((lo, hi, g), (np.nan,))[0] if g != "BW" else np.nan)
        if g != "BW":
            rows.append(("N son-years / sons / clusters", [" ; ".join(
                f"{lo}-{hi}: {info[(lo, hi, g)][0]:,}/{info[(lo, hi, g)][1]:,}/{info[(lo, hi, g)][2]:,}"
                for lo, hi in BANDS[:3])] + [""] * 9))
        panels.append((gname, rows))
    rows = []
    for g, gname in GROUPS4:
        for b in ((35, 55), (45, 55)):
            t = [safe(Dch("dec", y, g, b=b)) for y in ("lw", "ip", "ic", "ir")]
            t.append(ratio(Dch("dec", "ipc", g, b=b), Dch("dec", "lw", g, b=b)))
            t += [safe(Dch("dec", y, g, b=b)) for y in ("os_c", "jo", "jp", "jc", "jr")]
            rows.append((f"{gname}: ({b[0]}-{b[1]}) - (25-34)", [cell(x) for x in t]))
            for y, x in zip(YS, t):
                rec("1 decomposition change", gname, y, f"({b[0]}-{b[1]}) - (25-34)", x)
    panels.append(("Change in the coefficient across age bands (career divergence)", rows))
    md += ["## 1. Wage persistence by age band: industry level, industry career slope, within industry", "",
           "One regression per cell: the son's outcome (column header) on ln parental income, son-years in the band, "
           "Lee-Solon controls (as 24 / 27). ln wage = P + B x t + residual, so (1) = (2) + (3) + (4); (6) is 27's "
           "occupation score on the same son-years; (7)-(10) split ln wage with the joint occupation x industry model "
           "((1) = (7) + (8) + (9) + (10)), so (8) + (9) is what industry adds beyond occupation. Same sample in every "
           "column (valid wage, industry and occupation mapped); all cells stacked (clusters = 1968 family). Pooled "
           "weighted, by race unweighted. Column (5) blank when its denominator is not different from zero. "
           "**Accounting, not causal: sons select into industries.**", ""]
    md += table(hdr, panels)
    comp = [("ln wage (total)", "lw"), ("industry level P", "ip"), ("industry career slope B x t", "ic"),
            ("industry total (level + slope)", "ipc"), ("within industry", "ir"),
            ("occupation score (27, same sample)", "os_c"), ("within occupation (27, same sample)", "ores"),
            ("joint model: occupation part", "jo"), ("joint model: industry level net of occupation", "jp"),
            ("joint model: industry slope net of occupation", "jc"),
            ("joint model: industry total net of occupation (what industry adds)", "jpc"),
            ("joint model: residual (within occupation x industry)", "jr")]
    rows = []
    nan3 = (np.nan,) * 3
    for lab, y in comp:
        t = [safe(Dch("dec", y, "P")), ratio(Dch("dec", y, "P"), Dch("dec", "lw", "P")) if y != "lw" else nan3,
             safe(Dch("dec", y, "BW")), ratio(Dch("dec", y, "BW"), Dch("dec", "lw", "BW")) if y != "lw" else nan3,
             safe(L("dec", y, 25, 34, "BW")), safe(L("dec", y, 35, 55, "BW"))]
        rows.append((lab, [cell(x) for x in t]))
        for c, x in zip(["pooled change", "pooled share", "B-W change", "B-W share", "B-W gap 25-34", "B-W gap 35-55"],
                        t):
            rec("1b shares of the change", c, y, "(35-55)-(25-34)", x)
    md += ["### 1b. Headline: what accounts for the rise of wage persistence after 35 and for the Black-White "
           "divergence", "",
           "Rows = pieces of the son's ln wage; columns = (1) pooled change of the coefficient on ln parental "
           "income from 25-34 to 35-55, (2) its share of the ln wage change, (3) change of the Black - White "
           "difference in the coefficient from 25-34 to 35-55, (4) its share, (5)-(6) the Black - White difference "
           "at 25-34 and 35-55. Shares by the delta method from the stacked system (blank if the denominator is not "
           "different from zero).", ""]
    md += table(["(1) pooled change (35-55)-(25-34)", "(2) share of (1) for ln wage",
                 "(3) change of B-W gap (35-55)-(25-34)", "(4) share of (3) for ln wage", "(5) B-W gap at 25-34",
                 "(6) B-W gap at 35-55"], [("Pieces of ln wage (regressor: ln parental income)", rows)])
    return info


SORT_Y = [("ip", "(1) industry level P"), ("ib", "(2) industry slope B"),
          ("fire", "(3) finance / insurance / real estate"), ("legpro", "(4) legal / professional services"),
          ("bussv", "(5) computer / business services"), ("steep", "(6) steep-slope industry (top quartile)"),
          ("highp", "(7) high-premium industry (top quartile)")]


def sec_sort(r, md, M):
    d = r[r["dec"]].copy()
    d["ib"] = d["B"]
    ys = tuple(y for y, _ in SORT_Y)
    info = run_cells("sort", d, ys, ("lyp",), ctrl_lsn, ("A", "C"), bands=[(25, 34), (35, 55)])
    panels = []
    for g, gname in GROUPS4:
        rows = []
        for lo, hi in ((25, 34), (35, 55)):
            t = [safe(L("sort", y, lo, hi, g)) for y in ys]
            rows.append((f"ln parental income, sons {lo}-{hi}", [cell(x) for x in t]))
            for y, x in zip(ys, t):
                rec("2 sorting", gname, y, f"lyp, {lo}-{hi}", x,
                    mean=RES[K("sort", y, lo, hi, g)]["mean"] if g != "BW" else np.nan)
            if g != "BW":
                rows.append((f"Mean of outcome, {lo}-{hi}", [f"{RES[K('sort', y, lo, hi, g)]['mean']:.3f}"
                                                             for y in ys]))
                rows.append((f"N son-years / clusters, {lo}-{hi}",
                             [f"{info[(lo, hi, g)][0]:,} / {info[(lo, hi, g)][2]:,}"] * len(ys)))
        t = [safe(Dch("sort", y, g)) for y in ys]
        rows.append(("Change (35-55) - (25-34)", [cell(x) for x in t]))
        for y, x in zip(ys, t):
            rec("2 sorting change", gname, y, "(35-55)-(25-34)", x)
        panels.append((gname, rows))
    md += ["## 2. Sorting into industries by parental income", "",
           "### 2a. Industry measures and industry shares on ln parental income", "",
           "Son-year regressions (outcome in the column header) on ln parental income with Lee-Solon controls, "
           "decomposition sample. (1)-(2) the MORG level / slope of the son's industry; (3)-(7) linear probability "
           "models. Steep-slope industries: " + ", ".join(GNAMES[i] for i in sorted(M["steep"])) + ". High-premium: "
           + ", ".join(GNAMES[i] for i in sorted(M["highP"])) + ".", ""]
    md += table([h for _, h in SORT_Y], panels)
    rows_md = ["| Race / parental-income tercile | sons' ages | finance / insurance / real estate | legal / "
               "professional services | computer / business services | steep-slope industries | high-premium "
               "industries | mean P | mean B | son-years / sons |", "|---|---|---|---|---|---|---|---|---|---|"]
    TB = {}
    for race in ("Black", "White"):
        for tq in (1, 2, 3):
            for lo, hi in ((25, 34), (35, 55)):
                z = d[(d["race"] == race) & (d["terc"] == tq) & d["age"].between(lo, hi)]
                if len(z) == 0:
                    continue
                vals = [z[c].mean() for c in ("fire", "legpro", "bussv", "steep", "highp", "ip", "ib")]
                TB[(race, tq, lo)] = vals
                rows_md.append(f"| {race}, tercile {tq} | {lo}-{hi} | " + " | ".join(f"{x:.3f}" for x in vals) +
                               f" | {len(z):,} / {z['pid'].nunique():,} |")
                for c, x in zip(("fire", "legpro", "bussv", "steep", "highp", "ip", "ib"), vals):
                    CSV.append(dict(table="2b shares by tercile", sample=f"{race} T{tq}", outcome=c,
                                    term=f"{lo}-{hi}", coef=x, n=len(z)))
    md += ["", "### 2b. Shares by parental-income tercile and race", "",
           "Unweighted son-year means, decomposition sample; terciles of ln parental income over all Black and "
           "White sons (one value per son), so Black sons are concentrated in tercile 1. Descriptive.", ""]
    md += rows_md + [""]
    return TB


def sec_within(r, md, M):
    d = r[r["g_lw_t"].notna() & r["wave"].ge(1985) & r["igrp"].notna()].copy()
    flb = d["flb"] == 1
    st = d["igrp"].isin(M["steep"]) & ~flb
    d["g_flb"] = d["g_stay"].where(flb)
    d["g_st"] = d["g_stay"].where(st)
    d["g_oth"] = d["g_stay"].where(~flb & ~st)
    specs = [("g_stay", "base", "(1) same-employer annual ln wage growth, all industries"),
             ("g_stay", "grpfe", "(2) ... + industry-group FE"),
             ("g_stay", "ddxfe", "(3) ... + fine-industry FE"),
             ("g_flb", "base", "(4) ... sons in finance / insurance / real estate, legal / professional, computer / "
                               "business services"),
             ("g_st", "base", "(5) ... sons in other steep-slope industries"),
             ("g_oth", "base", "(6) ... sons in all other industries")]
    ctrl = {"base": ctrl_ageyr,
            "grpfe": lambda z: np.column_stack([ctrl_ageyr(z), dummies(z["igrp"])]),
            "ddxfe": lambda z: np.column_stack([ctrl_ageyr(z), dummies(z["ddx"])])}
    info = {}
    for y, s_, _ in specs:
        info[(y, s_)] = run_cells(f"win_{s_}", d, (y,), ("lyp",), ctrl[s_], ("C",), bands=[(25, 34), (35, 55)])
    panels = []
    for g, gname in GROUPS4:
        rows = []
        for lo, hi in ((25, 34), (35, 55)):
            t = [safe(L(f"win_{s_}", y, lo, hi, g)) for y, s_, _ in specs]
            rows.append((f"ln parental income, sons {lo}-{hi}", [cell(x) for x in t]))
            for (y, s_, h), x in zip(specs, t):
                rec("3 same-employer growth", gname, f"{y} {s_}", f"lyp, {lo}-{hi}", x,
                    n=info[(y, s_)].get((lo, hi, g), (np.nan,))[0] if g != "BW" else np.nan)
            if g != "BW":
                rows.append((f"Mean, {lo}-{hi}", [f"{RES[K(f'win_{s_}', y, lo, hi, g)]['mean']:.4f}"
                                                  if K(f'win_{s_}', y, lo, hi, g) in RES else ""
                                                  for y, s_, _ in specs]))
                rows.append((f"N stayer pairs / clusters, {lo}-{hi}",
                             [f"{info[(y, s_)][(lo, hi, g)][0]:,} / {info[(y, s_)][(lo, hi, g)][2]:,}"
                              if (lo, hi, g) in info[(y, s_)] else "" for y, s_, _ in specs]))
        panels.append((gname, rows))
    md += ["## 3. Wage growth with the same employer by parental income, within industry", "",
           "Consecutive interviews 1-2 years apart (waves 1985-2023, 27 Section 3) where the son stayed with his "
           "employer (tenure >= years since the previous interview - 0.5); outcome = annualised growth of ln wage "
           "(column header gives the sample / fixed effects). Controls: quartic in age, year FE; (2)-(3) add "
           "industry fixed effects of the later interview, so the coefficient compares sons in the same industry; "
           "(4)-(6) split the sample by the son's industry. Clusters 1968 family. Cells with < 250 pairs are left "
           "blank.", ""]
    md += table([h for _, _, h in specs], panels)


# ================================================================ fathers: following and its pay-off
FOL = [("f_ind", "igrp", "fgrp", "same industry group (33)"), ("f_ddx", "ddx", "fddx", "same fine industry (ind1990ddx)"),
       ("f_occ", "occ11", "focc11", "same occupation group (11)"), ("f_occ3", "dd", "fdd", "same occupation (occ1990dd)")]


def bench(z, sc_, fc_):
    """random-matching benchmark: sum_j p_son(j) p_father(j) within the cell."""
    zz = z.dropna(subset=[sc_, fc_])
    if len(zz) == 0:
        return np.nan
    ps = zz[sc_].value_counts(normalize=True)
    pf = zz[fc_].value_counts(normalize=True)
    return float((ps * pf.reindex(ps.index).fillna(0)).sum())


def sec_follow_desc(r, md):
    d = r[r["valid"] & r["fgrp"].notna()]
    rows_md = ["| Race | sons' ages | parental-income tercile | " + " | ".join(
        f"{lab}: observed | benchmark | ratio" for _, _, _, lab in FOL) + " | son-years / sons |",
        "|---|---|---|" + "---|---|---|" * len(FOL) + "---|"]
    OUTD = {}
    for race in ("Black + White", "Black", "White"):
        dr = d if race == "Black + White" else d[d["race"] == race]
        for lo, hi in ((25, 34), (35, 55)):
            for tq in (None, 1, 2, 3):
                z = dr[dr["age"].between(lo, hi)]
                z = z if tq is None else z[z["terc"] == tq]
                if len(z) < 50:
                    continue
                cells = []
                for fv, sc_, fc_, lab in FOL:
                    obs = z[fv].mean()
                    # benchmark within race x tercile cells (then averaged with the son-year counts)
                    parts = []
                    for (_, _), zz in z.groupby(["race", "terc"]):
                        if zz[fv].notna().sum() > 0:
                            parts.append((bench(zz[zz[fv].notna()], sc_, fc_), zz[fv].notna().sum()))
                    bm = sum(a * n for a, n in parts) / max(1, sum(n for _, n in parts))
                    cells += [f"{obs:.3f}", f"{bm:.3f}", f"{obs / bm:.2f}" if bm > 0 else ""]
                    OUTD[(race, lo, tq, fv)] = (obs, bm)
                    CSV.append(dict(table="4a following, descriptive", sample=race, outcome=fv,
                                    term=f"{lo}-{hi} T{tq if tq else 'all'}", coef=obs, mean=bm, n=z[fv].notna().sum()))
                rows_md.append(f"| {race} | {lo}-{hi} | {'all' if tq is None else tq} | " + " | ".join(cells) +
                               f" | {len(z):,} / {z['pid'].nunique():,} |")
    md += ["## 4. Following the father into his industry / occupation (parental-network channel)", "",
           "Father = male head of the son's family at 16 (24's fpid); his industry / occupation = modal code over his "
           "head-waves when the son was 12-18. **The PSID has no employer identifiers, so 'same employer as the "
           "father' (Corak and Piraino 2011; Staiger 2022) cannot be observed; following is measured at the industry "
           "and occupation level only.** Same industry / occupation compares modal harmonised codes (fathers coded "
           "mostly in 1970 codes, sons also in 2000 / 2012 codes after 2001, so some measured non-following is coding "
           "drift, more so at the fine level).", "",
           "### 4a. How often do sons work in the father's industry / occupation?", "",
           "Unweighted share of son-years (valid wage) in the father's industry / occupation; benchmark = share "
           "expected under random matching of sons to fathers within race x parental-income tercile, "
           "sum_j p_son(j) p_father(j); ratio = observed / benchmark.", ""] + rows_md + [""]
    return OUTD


def sec_follow_reg(r, md, M):
    d = r[r["valid"]].copy()
    # (b-a) gradient of following in parental income
    ys = [("f_ind", "(1) same industry group"), ("f_ddx", "(2) same fine industry"),
          ("f_occ", "(3) same occupation group"), ("f_occ3", "(4) same occupation (3-digit)")]
    info = {}
    for y, _ in ys:
        info[y] = run_cells("fol", d, (y,), ("lyp",), ctrl_lsn, ("A", "C"), bands=[(25, 34), (35, 55)])
    panels = []
    for g, gname in GROUPS4:
        rows = []
        for lo, hi in ((25, 34), (35, 55)):
            t = [safe(L("fol", y, lo, hi, g)) for y, _ in ys]
            rows.append((f"ln parental income, sons {lo}-{hi}", [cell(x) for x in t]))
            for (y, _), x in zip(ys, t):
                rec("4b following on parental income", gname, y, f"lyp, {lo}-{hi}", x)
            if g != "BW":
                rows.append((f"Mean, {lo}-{hi}", [f"{RES[K('fol', y, lo, hi, g)]['mean']:.3f}" for y, _ in ys]))
                rows.append((f"N son-years / clusters, {lo}-{hi}", [f"{info[y][(lo, hi, g)][0]:,} / "
                                                                    f"{info[y][(lo, hi, g)][2]:,}" for y, _ in ys]))
        panels.append((gname, rows))
    md += ["### 4b. Following by parental income", "",
           "Son-year linear probability models (outcome in the column header) on ln parental income, Lee-Solon "
           "controls, sons with a father's code.", ""]
    md += table([h for _, h in ys], panels)
    # (b-c) son in X given father in X
    xs = [("fire", "finance / insurance / real estate"), ("legpro", "legal / professional services"),
          ("bussv", "computer / business services"), ("flb", "any of the three"), ("steep", "steep-slope industries"),
          ("highp", "high-premium industries")]
    info = {}
    for x, _ in xs:
        info[x] = run_cells(f"fx_{x}", d, (x,), (f"fa_{x}", "lyp"), ctrl_lsn, ("A", "C"), bands=[(25, 55)],
                            groups=("P", "B", "W"))
    panels = []
    for g, gname in GROUPS4:
        t = [safe(L(f"fx_{x}", x, 25, 55, g, f"fa_{x}")) for x, _ in xs]
        t2 = [safe(L(f"fx_{x}", x, 25, 55, g, "lyp")) for x, _ in xs]
        rows = [("father in the same industry set", [cell(z) for z in t]),
                ("ln parental income", [cell(z) for z in t2])]
        for (x, _), z in zip(xs, t):
            rec("4c son in X on father in X", gname, x, "fa_x", z)
        if g != "BW":
            sub = D27.subset(d[d["age"].between(25, 55)], g)[0]
            rows.append(("Mean of outcome (son in the set)", [f"{RES[K(f'fx_{x}', x, 25, 55, g, f'fa_{x}')]['mean']:.3f}"
                                                              for x, _ in xs]))
            rows.append(("Share of son-years whose father is in the set",
                         [f"{sub[f'fa_{x}'].mean():.3f}" for x, _ in xs]))
            ss = sub.dropna(subset=[x, f"fa_{x}", "lyp"])
            rows.append(("Sons whose father is in the set (son-years)",
                         [f"{ss.loc[ss[f'fa_{x}'] == 1, 'pid'].nunique():,} ({int((ss[f'fa_{x}'] == 1).sum()):,})"
                          for x, _ in xs]))
            rows.append(("N son-years / clusters", [f"{info[x][(25, 55, g)][0]:,} / {info[x][(25, 55, g)][2]:,}"
                                                    for x, _ in xs]))
        panels.append((gname, rows))
    md += ["### 4c. Is the son in an industry set when the father was? (industry-specific following)", "",
           "Son-years 25-55; outcome = the son works in the industry set of the column header; regressors: the "
           "father worked there (modal industry at 12-18) and ln parental income; Lee-Solon controls.", ""]
    md += table([f"({k + 1}) son in {lab}" for k, (_, lab) in enumerate(xs)], panels)


def sec_payoff(r, md):
    d = r[r["valid"] & r["f_ind"].notna()].copy()
    d["g30"] = d["g_lw"]
    d["gs30"] = d["g_stay"]
    cols = [("lw", (25, 34), "(1) ln wage, sons 25-34"), ("lw", (35, 55), "(2) ln wage, sons 35-55"),
            ("g30", (30, 55), "(3) annual ln wage growth, sons 30-55"),
            ("gs30", (30, 55), "(4) annual ln wage growth with the same employer, sons 30-55"),
            ("g30", (25, 29), "(5) annual ln wage growth, sons 25-29")]
    specs = [("A", ("f_ind", "lyp"), "A. following + ln parental income (age quartic, year FE)"),
             ("B", ("f_ind", "lyp", "educ", "P", "ict"), "B. + years of education, industry level P and slope B x t")]
    d["ict"] = d["B"] * d["t"]
    panels = []
    for sp, xs, title in specs:
        info = {}
        for y, (lo, hi), _ in cols:
            info[(y, lo)] = run_cells(f"pay{sp}", d, (y,), xs, ctrl_ageyr, ("C",), bands=[(lo, hi)])
        for g, gname in GROUPS4:
            t = [safe(L(f"pay{sp}", y, lo, hi, g, "f_ind")) for y, (lo, hi), _ in cols]
            rows = [("son in the father's industry group", [cell(z) for z in t])]
            for (y, (lo, hi), h), z in zip(cols, t):
                rec(f"4d pay-off {sp}", gname, h, "f_ind", z)
            if g != "BW":
                rows.append(("N son-years / clusters", [f"{info[(y, lo)][(lo, hi, g)][0]:,} / "
                                                        f"{info[(y, lo)][(lo, hi, g)][2]:,}"
                                                        if (lo, hi, g) in info[(y, lo)] else ""
                                                        for y, (lo, hi), _ in cols]))
            panels.append((f"{title}: {gname}", rows))
    md += ["### 4d. Does following pay off? Wage level and wage growth", "",
           "Son-year regressions (outcome in the column header; growth = annualised change between consecutive "
           "interviews 1-2 years apart, (4) for sons who stayed with the employer). Regressor of interest: the son "
           "works in his father's industry group (33). Spec B holds the son's education and the MORG level / slope "
           "of his industry fixed, so the coefficient is the wage advantage of following relative to other sons in "
           "equally paid industries. Clusters 1968 family; pooled weighted. Selection: sons who follow may differ in "
           "unobserved ways (descriptive).", ""]
    md += table([h for _, _, h in cols], panels)
    # tenure profiles with person FE
    dt = d[d["tenure"].notna()].copy()
    dt["ten"] = dt["tenure"] / 10
    dt["ten2"] = dt["ten"] ** 2
    dt["ten_f"] = dt["ten"] * dt["f_ind"]
    dt["ten_lyp"] = dt["ten"] * dt["lyp_c"]
    ysT = [("lw", "(1) ln wage"), ("irr", "(2) ln wage net of industry level and slope")]
    dt["irr"] = dt["lw"] - dt["P"] - dt["B"] * dt["t"]
    cols_t = ["ten", "ten2", "ten_f", "f_ind", "ten_lyp"]
    labs_t = ["tenure (per 10 years)", "tenure squared", "tenure x in father's industry", "in father's industry",
              "tenure x ln parental income"]
    panels = []
    for g, gname in GROUPS3:
        sub, wc = D27.subset(dt[dt["age"].between(25, 55)], g)
        sub = sub.dropna(subset=["irr"]).copy()
        wv = sub.groupby("pid")["wpool"].transform("mean").to_numpy(float) if wc else np.ones(len(sub))
        Z = ctrl_ageyr(sub)[:, 1:]
        Mx = np.column_stack([sub[c].to_numpy(float) for c in cols_t] + [Z])
        gi = pd.factorize(sub["pid"])[0]
        cnt = np.bincount(gi, weights=wv)

        def dm(v):
            return v - (np.bincount(gi, weights=v * wv) / cnt)[gi]
        Md = np.column_stack([dm(Mx[:, j]) for j in range(Mx.shape[1])])
        clv = D27.CLIDX.get_indexer(sub["fam68"].to_numpy())
        for y, _ in ysT:
            yy = sub.assign(_y=dm(sub[y].to_numpy(float)))
            D27.est(("tenf", y, g), yy, "_y", Md, clv, wv, names=tuple(cols_t))
        rows = []
        for c, lab in zip(cols_t, labs_t):
            t = [one((("tenf", y, g), c)) for y, _ in ysT]
            rows.append((lab, [cell(z) for z in t]))
            for (y, _), z in zip(ysT, t):
                rec("4e tenure x following", gname, y, c, z, n=len(sub))
        rows.append(("Person FE, age quartic, year FE; N son-years / sons / clusters",
                     [f"{len(sub):,} / {sub['pid'].nunique():,} / {len(np.unique(clv)):,}"] * len(ysT)))
        panels.append((gname, rows))
    t = [comb([((("tenf", y, "B"), "ten_f"), 1.0), ((("tenf", y, "W"), "ten_f"), -1.0)]) for y, _ in ysT]
    panels.append(("Black - White", [("tenure x in father's industry", [cell(z) for z in t])]))
    for (y, _), z in zip(ysT, t):
        rec("4e tenure x following", "Black - White", y, "ten_f", z)
    md += ["### 4e. Wage-tenure profiles of sons in the father's industry (person FE)", "",
           "As 27 Section 7: within-son regressions on tenure with the employer, its square, tenure x following "
           "(son in the father's industry group), following, tenure x ln parental income (centred), quartic in age, "
           "year FE (waves 1984-2023). Descriptive wage-tenure profiles.", ""]
    md += table([h for _, h in ysT], panels)


def sec_contrib(r, md):
    out = {}
    hdr = ["(1) ln wage on ln parental income (short)", "(2) ... controlling following (long)",
           "(3) accounted for by following = (1) - (2)", "(4) following on ln parental income (pi)",
           "(5) ln wage on following (delta, long)"]
    panels = []
    for fv, lab in (("f_ind", "son in the father's industry group"), ("f_occ", "son in the father's occupation group"),
                    ("f_ddx", "son in the father's fine industry")):
        d = r[r["valid"] & r["lw"].notna() & r[fv].notna()].copy()
        d["fol"] = d[fv]
        run_cells(f"gs_{fv}", d, ("lw",), ("lyp",), ctrl_lsn, ("A", "C", "fol"), bands=[(25, 34), (35, 55)])
        run_cells(f"gl_{fv}", d, ("lw",), ("lyp", "fol"), ctrl_lsn, ("A", "C"), bands=[(25, 34), (35, 55)])
        run_cells(f"gp_{fv}", d, ("fol",), ("lyp",), ctrl_lsn, ("A", "C"), bands=[(25, 34), (35, 55)])
        rows = []
        for g, gname in GROUPS4:
            for lo, hi in ((25, 34), (35, 55)):
                s_ = L(f"gs_{fv}", "lw", lo, hi, g)
                l_ = L(f"gl_{fv}", "lw", lo, hi, g, "lyp")
                t = [safe(s_), safe(l_), safe(s_ + [(k, -c) for k, c in l_]), safe(L(f"gp_{fv}", "fol", lo, hi, g)),
                     safe(L(f"gl_{fv}", "lw", lo, hi, g, "fol"))]
                rows.append((f"{gname}, sons {lo}-{hi}", [cell(x) for x in t]))
                for c, x in zip(["short", "long", "contribution", "pi", "delta"], t):
                    rec(f"4f contribution of following ({fv})", gname, c, f"{lo}-{hi}", x)
        # change of the Black - White gap
        s_ = Dch(f"gs_{fv}", "lw", "BW")
        l_ = Dch(f"gl_{fv}", "lw", "BW", x="lyp")
        con = s_ + [(k, -c) for k, c in l_]
        t = [safe(s_), safe(l_), safe(con), safe(Dch(f"gp_{fv}", "fol", "BW")), safe(Dch(f"gl_{fv}", "lw", "BW",
                                                                                         x="fol"))]
        rows.append(("Change of the Black - White gap (35-55) - (25-34)", [cell(x) for x in t]))
        sh = ratio(con, s_)
        rows.append(("Share of the change accounted for by following = (3) / (1)", [cell(sh)] + [""] * 4))
        sP = Dch(f"gs_{fv}", "lw", "P")
        conP = sP + [(k, -c) for k, c in Dch(f"gl_{fv}", "lw", "P", x="lyp")]
        rows.append(("Pooled change (35-55) - (25-34)", [cell(safe(sP)), "", cell(safe(conP)), "", ""]))
        for c, x in zip(["short", "long", "contribution", "pi", "delta", "share"], t + [sh]):
            rec(f"4f contribution of following ({fv})", "B-W change", c, "(35-55)-(25-34)", x)
        out[fv] = (safe(con), sh, safe(s_))
        panels.append((f"Following = {lab}", rows))
    md += ["### 4f. How much of the divergence is following the father? (frequency x pay-off)", "",
           "Omitted-variable (Gelbach) accounting on a common sample: (1) the son's ln wage on ln parental income "
           "with Lee-Solon controls; (2) adding the following indicator; (3) = (1) - (2) = pi x delta, the part of "
           "the wage gradient that runs through following (pi = how much more often sons of richer parents follow, "
           "delta = the wage gap of followers holding parental income fixed). All cells stacked; clusters 1968 "
           "family.", ""]
    md += table(hdr, panels)
    return out


# ================================================================ NLSY79 check
def nlsy_panel(W, M, XWD, S):
    J = D27.nlsy_panel(XWD, S)
    X = nlsy_ind_extract()
    rx = re.compile(r"EMPLOYERS_ALL_IND_(\d{4})\.(\d\d)$")
    long = []
    for c in X.columns:
        m_ = rx.match(c)
        if m_:
            long.append(pd.DataFrame({"pid": X["pid"], "round": int(m_.group(1)), "jj": int(m_.group(2)),
                                      "icode": X[c]}))
    I = pd.concat(long, ignore_index=True)
    I = I[I["icode"] > 0]
    J = J.merge(I, on=["pid", "round", "jj"], how="left")
    J["isch"] = np.where(J["round"] <= 2000, "1970", np.where(J["icode"] >= 1000, "2012", "2000"))
    rc = recode2000(W, np.concatenate([J.loc[J["isch"] == "2000", "icode"].dropna().to_numpy(),
                                       code2000(J.loc[J["isch"] == "2012", "icode"].dropna().to_numpy())]))
    J = attach_industry(J, "icode", "isch", W, M, rc)
    J["t"] = J["C"] / 10
    ok = J["lw"].notna() & J["P"].notna() & J["os"].notna()
    J["ip"] = J["P"].where(ok)
    J["ic"] = (J["B"] * J["t"]).where(ok)
    J["ipc"] = J["ip"] + J["ic"]
    J["ir"] = J["lw"].where(ok) - J["ipc"]
    J["os_c"] = J["os"].where(ok)
    J["lw_c"] = J["lw"].where(ok)
    for nm, st in (("fire", FIRE), ("legpro", LEGPRO), ("steep", M["steep"])):
        J[nm] = J["igrp"].isin(st).astype(float).where(ok)
    return J


def sec_nlsy(J, md):
    ys = ("lw_c", "ip", "ic", "ir", "ipc", "os_c", "fire", "legpro", "steep")
    NB = [(25, 34), (35, 44), (45, 55)]
    info = run_cells("nl", J, ys, ("lyp",), lambda z: ctrl_ageyr(z, "birth_year"), ("C",), bands=NB)
    hdr = ["(1) ln wage", "(2) industry level P", "(3) industry slope B x t", "(4) within-industry residual",
           "(5) occupation score", "(6) in finance / insurance / real estate", "(7) in legal / professional services",
           "(8) in a steep-slope industry"]
    YS = ["lw_c", "ip", "ic", "ir", "os_c", "fire", "legpro", "steep"]
    panels = []
    for g, gname in GROUPS4:
        rows = []
        for lo, hi in NB:
            t = [safe(L("nl", y, lo, hi, g)) for y in YS]
            rows.append((f"ln parental income, ages {lo}-{hi}", [cell(x) for x in t]))
            for y, x in zip(YS, t):
                rec("5 NLSY79", gname, y, f"lyp, {lo}-{hi}", x)
        if g != "BW":
            rows.append(("N person-rounds / clusters", [" ; ".join(f"{lo}-{hi}: {info[(lo, hi, g)][0]:,}/"
                                                                   f"{info[(lo, hi, g)][2]:,}" for lo, hi in NB)]
                         + [""] * 7))
        t = [safe(Dch("nl", y, g, b=(45, 55))) for y in YS]
        rows.append(("Change (45-55) - (25-34)", [cell(x) for x in t]))
        for y, x in zip(YS, t):
            rec("5 NLSY79 change", gname, y, "(45-55)-(25-34)", x)
        panels.append((gname, rows))
    md += ["## 5. NLSY79 check", "",
           "Men of the NLSY79 living with a parent in 1979 (27 Section 9): hourly wage of the CPS (main) job at each "
           "interview, its industry (roster, 1970 codes to 2000, 2000 codes from 2002, harmonised as above) and "
           "occupation; regressor ln mean parental income 1979-81; controls quartic in age, birth-year FE; clusters "
           "1979 household; pooled weighted by the 1979 weight. (1) = (2) + (3) + (4) on a common sample (industry "
           "and occupation mapped).", ""]
    md += table(hdr, panels)


# ================================================================ figure
def figure(TB):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ink, muted, grid, bg = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    col = {"lw": "#52514e", "ip": "#2a78d6", "ic": "#1baf7a", "ir": "#eb6834"}
    lab = {"lw": "ln wage (total)", "ip": "Industry level P", "ic": "Industry career slope B x t",
           "ir": "Within industry (residual)"}
    fig, ax = plt.subplots(1, 4, figsize=(17, 4.8), gridspec_kw=dict(width_ratios=[1, 1, 1, 1.05]))
    fig.patch.set_facecolor(bg)
    bands = [(25, 34), (35, 44), (45, 55)]
    x = np.arange(3)
    for a_, (g, gname) in zip(ax[:3], GROUPS3):
        for j, y in enumerate(("lw", "ip", "ic", "ir")):
            b, s = zip(*[comb([(K("dec", y, lo, hi, g), 1.0)])[:2] for lo, hi in bands])
            xx = x + (j - 1.5) * 0.1
            a_.errorbar(xx, b, yerr=1.96 * np.array(s), fmt="o-", ms=8, lw=2, color=col[y], ecolor=col[y],
                        elinewidth=1.5, capsize=0, label=lab[y], mec=bg, mew=1.5)
        a_.axhline(0, color=muted, lw=1)
        a_.set_xticks(x, [f"{lo}-{hi}" for lo, hi in bands], color=ink)
        a_.set_title(f"{gname} sons", color=ink, loc="left", fontsize=12)
        a_.set_xlabel("Son's age band", color=muted)
        a_.set_ylim(-0.12, 0.62)
    ax[0].set_ylabel("Coefficient on ln parental income (95% CI)", color=muted)
    ax[0].legend(frameon=False, loc="upper left", fontsize=9)
    # shares in finance / insurance / real estate + legal / professional at 35-55 by tercile and race
    a_ = ax[3]
    cr = {"Black": "#6250d6", "White": "#eda100"}
    for k, race in enumerate(("Black", "White")):
        vals = [TB.get((race, tq, 35), [np.nan] * 7) for tq in (1, 2, 3)]
        v = [z[0] + z[1] for z in vals]
        xx = np.arange(3) + (k - 0.5) * 0.38
        a_.bar(xx, v, width=0.36, color=cr[race], label=f"{race} sons", edgecolor=bg, linewidth=2)
        for xi, vi in zip(xx, v):
            if vi == vi:
                a_.text(xi, vi + 0.004, f"{vi:.2f}", ha="center", va="bottom", fontsize=8, color=muted)
    a_.set_xticks(np.arange(3), ["Bottom", "Middle", "Top"], color=ink)
    a_.set_xlabel("Parental-income tercile (pooled)", color=muted)
    a_.set_title("Share in finance / insurance / real estate\nor legal / professional services, ages 35-55",
                 color=ink, loc="left", fontsize=11)
    a_.legend(frameon=False, loc="upper left", fontsize=9)
    for a_ in ax:
        a_.set_facecolor(bg)
        a_.grid(axis="y", color=grid, lw=0.8)
        a_.set_axisbelow(True)
        for sp in ("top", "right", "left"):
            a_.spines[sp].set_visible(False)
        a_.spines["bottom"].set_color(muted)
        a_.tick_params(colors=muted, length=0)
    fig.tight_layout()
    fig.savefig(OUT / "industry_careers.png", dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)


# ================================================================ literature (verified on the source pages, 2026-10-17)
LIT = [
    "Corak, M. and P. Piraino (2011), 'The Intergenerational Transmission of Employers', Journal of Labor Economics "
    "29(1): 37-68 (Canada: about 40% of young men had at some point worked for an employer their father also worked "
    "for, 6-9% still had that employer as adults; transmission rises with paternal earnings, especially at the top). "
    "https://stonecenter.gc.cuny.edu/files/2011/08/corak-the-intergenerational-transmission-of-employers-2011.pdf ; "
    "IZA DP 4876 'About 6% of young Canadian men have the same main employer as their fathers': "
    "https://econpapers.repec.org/paper/izaizadps/dp4876.htm",
    "Kramarz, F. and O. Nordstrom Skans (2014), 'When Strong Ties are Strong: Networks and Youth Labour Market "
    "Entry', Review of Economic Studies 81(3): 1164-1200 (Sweden, linked employer-employee data: parents' workplaces "
    "are an important determinant of where graduates find their first job, more so for the low-educated and in "
    "high unemployment; larger when the parent's position is strong). "
    "https://www.ifau.se/en/Press/Abstracts/When-strong-ties-are-strong--networks-and-youth-labor-market-entry/",
    "Staiger, M. (2022), 'The Intergenerational Transmission of Employers and the Earnings of Young Workers', "
    "working paper, Opportunity Insights, December 2022 (US LEHD + 2000 Census: 29% work for a parent's employer at "
    "least once by age 30, 5% at the first job; working there raises initial earnings by 19%; children of "
    "higher-earning parents are more likely to do so and gain more; the elasticity of initial earnings with respect "
    "to parental earnings would be 7.2% lower without these jobs). "
    "https://conference.nber.org/conf_papers/f179912/f179912.pdf ; earlier version (2020: 7% of first stable jobs, "
    "31% premium) https://equitablegrowth.org/working-papers/the-intergenerational-transmission-of-employers-and-the-"
    "earnings-of-young-workers/",
    "Chetty, R., M. O. Jackson, T. Kuchler, J. Stroebel, N. Hendren et al. (2022), 'Social capital I: measurement and "
    "associations with economic mobility', Nature 608: 108-121 (economic connectedness - the share of high-SES "
    "friends among low-SES people - is among the strongest predictors of upward mobility). "
    "https://ideas.repec.org/a/nat/nature/v608y2022i7921d10.1038_s41586-022-04996-4.html",
    "Okumura, T. and E. Usui (2016), 'Intergenerational Transmission of Skills and Differences in Labor Market "
    "Outcomes for Blacks and Whites', Research in Labor Economics 43: 227-286 (NLSY79: White sons earn more in "
    "occupations requiring skills similar to their fathers', Black sons in such occupations earn less). "
    "https://ideas.repec.org/h/eme/rleczz/s0147-912120160000043015.html",
    "Laband, D. N. and B. F. Lentz (1992), 'Self-Recruitment in the Legal Profession', Journal of Labor Economics "
    "10(2): 182-201 (lawyers' sons who receive transferred legal knowledge earn more). "
    "https://ideas.repec.org/a/ucp/jlabec/v10y1992i2p182-201.html",
    "Chen, L., J. Gordanier and O. Ozturk (2016), 'Following (Not Quite) in Your Father's Footsteps: Task Followers "
    "and Labor Market Outcomes', MPRA Paper 76041 (Journal of Labor Research 2019) (task following carries a wage "
    "premium of about 5%). https://ideas.repec.org/p/pra/mprapa/76041.html",
]


# ================================================================ summary
def summary(OUTD, CON, M):
    def c(t):
        return cell(t) if t is not None else "n.a."

    def ch(y, g):
        return sc(Dch("dec", y, g))

    def shr(y, g):
        x = cell(ratio(Dch("dec", y, g), Dch("dec", "lw", g)))
        return x if x else "n.a. (denominator ~ 0)"

    def lv(tag, y, lo, hi, g, x="x"):
        return sc(L(tag, y, lo, hi, g, x))
    out = ["## Summary", ""]
    out.append("- **Measurement.** Industry codes of all PSID eras (1970 / 2000 / 2012 Census) and CPS MORG harmonised "
               "to ind1990ddx (Autor-Dorn-Hanson) and 33 groups. Industry level P and industry-specific career slope "
               "B estimated in CPS MORG 1992-2002 (men 25-64). Steepest career slopes: education, legal services, "
               "professional services, chemicals, health, finance and insurance; flattest: agriculture, personal, "
               "business and repair services, real estate, retail (Table 0).")
    out.append("- **General pattern (pooled, weighted).** The son's ln wage on ln parental income rises by "
               f"{ch('lw', 'P')} from 25-34 to 35-55. The industry level accounts for {ch('ip', 'P')} of that rise "
               f"(share {shr('ip', 'P')}), the industry career slope for {ch('ic', 'P')} (share {shr('ic', 'P')}); "
               f"together {ch('ipc', 'P')} (share {shr('ipc', 'P')}); within industry {ch('ir', 'P')}. The industry "
               f"level part of the gradient is already {lv('dec', 'ip', 25, 34, 'P')} at 25-34 "
               f"({lv('dec', 'ip', 35, 55, 'P')} at 35-55). Sons of richer parents are in steeper industries "
               f"(industry slope B on ln parental income at 35-55: {lv('sort', 'ib', 35, 55, 'P')}; finance / "
               f"insurance / real estate {lv('sort', 'fire', 35, 55, 'P')}; legal / professional "
               f"{lv('sort', 'legpro', 35, 55, 'P')}), but the slope differences across industries are small.")
    out.append("- **Race.** The change of the Black-White gap in the gradient from 25-34 to 35-55 is "
               f"{ch('lw', 'BW')}; industry level {ch('ip', 'BW')} (share {shr('ip', 'BW')}), industry career slope "
               f"{ch('ic', 'BW')} (share {shr('ic', 'BW')}), industry total {ch('ipc', 'BW')} (share "
               f"{shr('ipc', 'BW')}), within industry {ch('ir', 'BW')}. Occupation score on the same son-years "
               f"{ch('os_c', 'BW')} (share {shr('os_c', 'BW')}). Joint occupation x industry model: occupation part "
               f"{ch('jo', 'BW')}, industry net of occupation {ch('jpc', 'BW')} (share {shr('jpc', 'BW')}), residual "
               f"{ch('jr', 'BW')} (share {shr('jr', 'BW')}).")
    out.append("- **Within industry, same employer (Section 3).** Same-employer annual wage growth at 25-34 on ln "
               f"parental income: White {lv('win_base', 'g_stay', 25, 34, 'W')}, with fine-industry FE "
               f"{lv('win_ddxfe', 'g_stay', 25, 34, 'W')}; Black {lv('win_base', 'g_stay', 25, 34, 'B')} / "
               f"{lv('win_ddxfe', 'g_stay', 25, 34, 'B')}; pooled in finance / legal / professional / business "
               f"services {lv('win_base', 'g_flb', 25, 34, 'P')}, in all other non-steep industries "
               f"{lv('win_base', 'g_oth', 25, 34, 'P')}.")
    fo = OUTD
    out.append("- **Following the father (Section 4).** Share of son-years in the father's industry group: Black "
               f"{fo[('Black', 35, None, 'f_ind')][0]:.3f} (random-matching benchmark "
               f"{fo[('Black', 35, None, 'f_ind')][1]:.3f}), White {fo[('White', 35, None, 'f_ind')][0]:.3f} "
               f"({fo[('White', 35, None, 'f_ind')][1]:.3f}) at 35-55; same occupation group Black "
               f"{fo[('Black', 35, None, 'f_occ')][0]:.3f} ({fo[('Black', 35, None, 'f_occ')][1]:.3f}), White "
               f"{fo[('White', 35, None, 'f_occ')][0]:.3f} ({fo[('White', 35, None, 'f_occ')][1]:.3f}). Following "
               f"on ln parental income at 35-55: Black {lv('fol', 'f_ind', 35, 55, 'B')}, White "
               f"{lv('fol', 'f_ind', 35, 55, 'W')}. Son in finance / insurance / real estate when the father was: "
               f"Black {lv('fx_fire', 'fire', 25, 55, 'B', 'fa_fire')}, White "
               f"{lv('fx_fire', 'fire', 25, 55, 'W', 'fa_fire')}. Pay-off (spec B, education and the industry's "
               f"level / slope held fixed): ln wage at 35-55 Black {lv('payB', 'lw', 35, 55, 'B', 'f_ind')}, White "
               f"{lv('payB', 'lw', 35, 55, 'W', 'f_ind')}; annual wage growth at 30-55 Black "
               f"{lv('payB', 'g30', 30, 55, 'B', 'f_ind')}, White {lv('payB', 'g30', 30, 55, 'W', 'f_ind')}; "
               f"tenure x following (person FE) Black {cell(one((('tenf', 'lw', 'B'), 'ten_f')))}, White "
               f"{cell(one((('tenf', 'lw', 'W'), 'ten_f')))}. Accounted for by following (industry group) in the "
               f"change of the Black-White gap: {c(CON['f_ind'][0])} of {c(CON['f_ind'][2])} (share "
               f"{c(CON['f_ind'][1]) or 'n.a.'}); occupation-group following {c(CON['f_occ'][0])} (share "
               f"{c(CON['f_occ'][1]) or 'n.a.'}).")
    out.append("- **NLSY79 (Section 5).** Change (45-55) - (25-34) of the Black-White gap: ln wage "
               f"{sc(Dch('nl', 'lw_c', 'BW', b=(45, 55)))}, industry level {sc(Dch('nl', 'ip', 'BW', b=(45, 55)))}, "
               f"industry slope {sc(Dch('nl', 'ic', 'BW', b=(45, 55)))}, within industry "
               f"{sc(Dch('nl', 'ir', 'BW', b=(45, 55)))}; pooled change of the gradient: ln wage "
               f"{sc(Dch('nl', 'lw_c', 'P', b=(45, 55)))}, industry level {sc(Dch('nl', 'ip', 'P', b=(45, 55)))}, "
               f"slope {sc(Dch('nl', 'ic', 'P', b=(45, 55)))}.")
    return "\n".join(out)


ASSESS = (
    "**Assessment.** Industry is a small part of the post-35 divergence. (i) Sons of richer parents do sort into "
    "better-paid and steeper industries: shares in finance / insurance / real estate and legal / professional "
    "services rise with parental income (at 35-55: White top tercile 0.128 vs bottom 0.027; Black top tercile only "
    "0.044), and the industry level carries 0.077 of the pooled wage gradient at 25-34 (the occupation score 0.16). "
    "(ii) But that industry component is in place by 25-34 and does not grow, and industry career slopes differ "
    "little (s.d. 0.037 log points per 10 years across men), so sorting into steep industries accounts for about 8% "
    "of the pooled rise of wage persistence after 35 and about 5% of the change of the Black-White gap (precisely "
    "estimated but small); level + slope about 8% of the divergence, not significant. (iii) Net of occupation, "
    "industry adds about 3% (n.s.) to the divergence and 6% to the pooled rise (all through slopes); with "
    "occupation and industry together, about 4/5 of the divergence remains within occupation x industry cells. "
    "(iv) The same-employer wage-growth gradient of White sons at 25-34 survives fine-industry fixed effects "
    "(0.021 -> 0.015); it is steepest inside finance / legal / professional / business services (0.040**) but is not "
    "confined to them, and Black sons show no gradient in any industry set. (v) Following the father: sons work in "
    "the father's industry group 2-3 times as often as random matching implies (White 0.142, Black 0.101 at "
    "35-55); following in industry barely rises with parental income (following in occupation group does, for "
    "White sons). White sons whose fathers were in finance / insurance / real estate are 12 points more likely to "
    "be there; Black fathers were rarely in these industries (21 Black sons with a father in finance / insurance / "
    "real estate, 8 in legal / professional services), so Black industry-specific following cannot be estimated "
    "and the race difference is mainly in where fathers worked. Following carries a wage-level premium given "
    "education and the industry's pay (pooled 0.08*** at 25-34, 0.05* at 35-55) but no steeper wage growth or "
    "wage-tenure profile, and it accounts for essentially none of the divergence (0.002 of -0.107). A parental-"
    "network channel visible at the industry level therefore looks like an entry / level effect (in line with "
    "Staiger 2022 and Kramarz and Skans 2014 for employers), not career-stage growth. For the companion model this "
    "strengthens 27's reading: the divergence is differential human capital accumulation on the job (or its "
    "pay-off) by background and race within occupations, industries and employers; industry choice adds little. "
    "The NLSY79 shows the same small, flat industry components (its Black-White divergence is itself small and "
    "not significant). Caveats: descriptive; P and B are industry-average prices without holding worker "
    "composition fixed (education's steep slope partly reflects public pay scales), B is linear in age and fixed "
    "at 1992-2002; codes are noisy and bridged across classifications by modal / weighted crosswalks; the father's "
    "industry is his modal code at 12-18 among father-present sons (52% of Black, 87% of White sons, 24); employer "
    "transmission is not observable in the PSID.")


# ================================================================ main
def main():
    OUT.mkdir(exist_ok=True)
    W = ind_crosswalks()
    XWD = D27.crosswalks()
    M = morg_measures(morg_micro(W, XWD))
    r = son_panel(W, M)
    S = D27.SCORES
    J = nlsy_panel(W, M, XWD, S)
    D27.CLIDX = pd.Index(np.unique(np.concatenate([r["fam68"].dropna().unique().astype(float),
                                                   J["fam68"].dropna().unique().astype(float) + 1e7])))
    J["fam68"] = J["fam68"].astype(float) + 1e7
    r["fam68"] = r["fam68"].astype(float)
    D27.NCL = len(D27.CLIDX)
    md = ["# Industry careers and the IGE: sorting into steep-growth industries, and following the father", "",
          "Built by `32.IndustryCareers.py` (2026-10-17); definitions in its docstring. PSID SRC + SEO sons (27's "
          "panel = 24's frame: 6.IGEMain parents, male heads 25-55, valid wage years), race of the parental head at "
          "16. Every coefficient: estimate (s.e.; p), *** p<0.01, ** p<0.05, * p<0.1, s.e. clustered by 1968 family "
          "(PSID) / 1979 household (NLSY79). **Descriptive accounting: sons select into industries, occupations and "
          "employers; nothing here is a causal effect of parental income, race or the father's industry.**", "",
          "SUMMARY_PLACEHOLDER", "", ASSESS, ""]
    print("measures ...", flush=True)
    sec_morg(M, md, W, r)
    print("decomposition ...", flush=True)
    sec_decomp(r, md)
    print("sorting ...", flush=True)
    TB = sec_sort(r, md, M)
    print("within ...", flush=True)
    sec_within(r, md, M)
    print("following ...", flush=True)
    OUTD = sec_follow_desc(r, md)
    sec_follow_reg(r, md, M)
    sec_payoff(r, md)
    CON = sec_contrib(r, md)
    print("nlsy ...", flush=True)
    sec_nlsy(J, md)
    md += ["## 6. Literature on parental networks and following (verified on the source pages, 2026-10-17)", ""]
    md += [f"- {x}" for x in LIT]
    md += ["", "What is new here relative to these papers: they measure transmission of the employer itself at labour "
           "market entry (first stable job, initial earnings) in administrative data (Canada, Sweden, US LEHD) or the "
           "wage return to occupational / task following without the career profile. This file asks whether "
           "following the father's industry or occupation contributes to career-stage wage growth after 30 and to "
           "the Black-White divergence in wage persistence, in US survey data with parental income measured in "
           "childhood; it cannot see employers.", ""]
    figure(TB)
    pd.DataFrame(CSV).to_csv(OUT / "industry_careers.csv", index=False)
    summ = summary(OUTD, CON, M)
    md = [summ if x == "SUMMARY_PLACEHOLDER" else x for x in md]
    (OUT / "industry_careers.md").write_text("\n".join(md), encoding="utf-8")
    print(summ)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        W = ind_crosswalks()
        XWD = D27.crosswalks()
        morg_micro(W, XWD)
        if len(sys.argv) > 2:
            nlsy_ind_extract()
    else:
        main()
