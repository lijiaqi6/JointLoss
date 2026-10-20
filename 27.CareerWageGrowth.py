r"""Career wage growth and the IGE: occupational upgrading / promotion vs wage growth within occupation (2026-10-17).

Question (PI): the Black-White divergence in the IGE after age 35 (24.IGEDecomposition.py: the son's ln wage on ln
parental income is Black 0.161 -> 0.161, White 0.255 -> 0.454 from 25-34 to 45-55) comes from career wage growth. How
much of it is promotion / occupational upgrading (moving to higher-paying occupations and positions) and how much is
wage growth within occupation and within job? General pattern (pooled) first, then race. DESCRIPTIVE ACCOUNTING:
sons select into occupations and employers; nothing here identifies a causal effect of parental income or of race.

DATA (raw data read only)
  PSID  sons = 24.IGEDecomposition.py child-year frame (6.IGEMain parents; male heads 25-55; valid wage years:
        earnings in the 6.IGEMain bounds, hours >= 100, wage $2-$200 in 2000 $; ln w = ln earnings - ln hours of income
        year t = wave - 1), read through 24's cached panel (data/ige_decomposition_panel.pkl) via importlib.
        Head's occupation at the interview of wave w (current main job; from 2003 job 1 = current or most recent main
        job) from 23.CorrelatedShocks.py's cache data/correlated_shocks_fam.pkl (h_occ): 1968-1980 retrospective
        3-digit 1970 Census codes ('OCCUPATION OF HEAD yy'), 1981-2001 'MAIN OCC: 3 DIGIT (HD-E)' (1970 codes),
        2003-2015 'BC20 MAIN OCC FOR JOB 1' (2000 codes, 3 digits), 2017-2023 the same (2010 codes, 4 digits).
        The occupation at the spring interview of wave w is paired with the wage of income year w - 1 (same row).
        Extra family-file items read here (head, employed branch; the lists are in the constants below and printed
        in the .md):
          tenure with the present employer: months 1984-1992 ('#MO PRES(ENT) EMP'), 1993 from the employer start
            year, years / months / weeks 1994-2023 ('B23' / 'BC41 YRS|MOS|WKS PRES EMP').
          within-employer position changes 1984-2001: 1984-1987 months in the present position < months with the
            present employer and the position began <= 15 months before the interview ('#MO PRES POS');
            1988-2001 the year the present position began ('B26' / 'B30' / 'B31 YR BEG PRES POS'; = employer start if
            'B25 BEG WRK PRES POS' = yes) is after the employer start year ('B24 YR BEG PRES EMP') and in the window
            [w - 1, w] (annual waves) or [w - 2, w] (1999, 2001), or the head reports a further change of position
            with this employer in the previous year ('B27' / 'B32 CHGE POS' = 1).  Year codes: two digits 1988-1992
            (96 = previous or current year, DK which -> in window; 97 = before the previous year), four digits from
            1993 (9996 / 9997 likewise).
          reported promotion 1976-1987: the employed head whose present job / position began within about a year
            says the previous one ended by 'promotion' (code 6 of the why-ended item of the E branch; variables of
            19.FatherDisplacement.py).
        Sons' displacement: data/psid_displacement.pkl (19; main = plant closure / layoff / firing, dated year).
  Occupational wage score (CPS MORG, Dropbox/MORG/morgYY.dta, 1979-2019, read only): men 25-64, hourly wage =
        earnhre / 100 if paid by the hour, else earnwke / uhourse (top-coded weekly earnings x 1.4), 2000 $, $2-$200,
        earnings weights. All occupation codes are mapped to David Dorn's consistent occ1990dd scheme (Autor and Dorn
        2013 AER; Autor 2015 JEP for 2010 codes; crosswalk files downloaded from ddorn.net into
        data/ext/occ_crosswalk/, read as data): 1970 codes (MORG 1979-82, PSID 1968-2001), 1980 codes (MORG 1983-91),
        1990 codes (MORG 1992-2002), 2000 codes (PSID 2003-15; MORG 2003-10 = 4-digit 2002 codes / 10), 2010 codes
        (PSID 2017-23; MORG 2011-19). The IPUMS occ1990 crosswalk (occ1990_xwalk.xls) was also downloaded but is not
        used (no xls reader in the environment; Dorn's files are the standard harmonised version of occ1990).
          score (fixed)   mean of (ln w - mean ln w of all men in the year) in the occupation, base period 1992-2002
                          (native 1990 codes, no crosswalk on the CPS side); cells < 50 men use all years 1979-2019;
                          remaining gaps the major-group mean.
          score (t)       the same relative premium in the occupation in t-1..t+1 (>= 30 men), else the fixed score;
                          PSID income years outside 1979-2019 use the nearest year.
          score (group)   mean over 11 major occupation groups (coarse: a lower bound on the between component).
          supervisory / managerial occupation: occ1990dd 3-22 (executive, administrative and managerial), 475-476
                          (farm managers), and the supervisor codes 243, 303-307, 413-415, 433, 448, 456, 477, 485, 494,
                          503, 553-558, 613, 628, 803, 843, 864.
  NLSY79 (check; Dropbox/NLS, read only; cache data/career_wage_growth_nlsy79.pkl): White and Black men of
        data/nlsy79_kids.pkl (2.NLSY79.py; living with a parent in 1979, parental income = mean TNFI 1979-81), the
        employer roster EMPLOYERS_ALL_<item>_<round>.<JJ> (the same JJ in two rounds is the same employer): occupation
        (1970 codes to 2000, 2000 codes from 2002), hourly pay, CPS job flag; the CPS (main) job of each round.
        Promotions: 'QES-PROMO38/39' (position change since the last interview at job #01-05; 1 promotion, 2 demotion,
        3 position change), rounds 1996-2016; 'ES-16' (any promotion since the last interview), 1988-1990.
DESIGN
  Wage persistence by age band (24 section 1b): child-years in the band, ln w (and its pieces) on ln parental income,
  Lee-Solon controls without the x-age interactions (quartics in the father's age at 16 and the son's age).
  ln w = score + residual, so the coefficient on ln w = coefficient on the score (between-occupation) + coefficient on
  the residual (within-occupation), on the same sample. All cells (band x race) are estimated in one stacked,
  block-diagonal system so that differences across bands and races have a covariance (clusters = 1968 family).
  Pooled = Black + White sons with the son's PSID individual weight of the year (general pattern); by race unweighted
  as in 24. Promotion / upgrading: son-year linear probability models with an age quartic and year fixed effects.
Every table: one regression per column (outcome in the header), regressors as rows, N / clusters at the bottom,
coefficient (s.e.; p) with *** p<0.01, ** p<0.05, * p<0.1.
Writes output/career_wage_growth.csv (every estimate), output/career_wage_growth.md, output/career_wage_growth.png;
caches data/career_wage_growth_morg.pkl, data/career_wage_growth_psid.pkl, data/career_wage_growth_nlsy79.pkl.
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
import os
DROPBOX = Path(os.environ.get("DROPBOX", Path.home() / "Dropbox"))   # raw data, read only

warnings.simplefilter("ignore", FutureWarning)
warnings.simplefilter("ignore", RuntimeWarning)

pd.set_option("display.width", 250)
warnings.simplefilter("ignore", pd.errors.PerformanceWarning)


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


D24 = _load("d24", "24.IGEDecomposition.py")
psid1 = D24.psid1
FAM, layout, read = psid1.FAM, psid1.layout, psid1.read

MORG = Path(DROPBOX / "MORG")
XW = DATA / "ext" / "occ_crosswalk" / "unz"
NLS = Path(DROPBOX / "NLS/nlsy79_all_1979-2022")
C_MORG, C_PSID, C_NLS = (DATA / "career_wage_growth_morg.pkl", DATA / "career_wage_growth_psid.pkl",
                         DATA / "career_wage_growth_nlsy79.pkl")
BASE = (1992, 2002)
MAN = set(range(3, 23)) | {475, 476}
SUP = {243, 303, 304, 305, 306, 307, 413, 414, 415, 433, 448, 456, 477, 485, 494, 503, 553, 554, 555, 556, 557, 558,
       613, 628, 803, 843, 864}
GROUPS = [(3, 37, "Managerial & management related"), (43, 199, "Professional specialty"), (203, 235, "Technicians"),
          (243, 290, "Sales"), (303, 391, "Administrative support"), (403, 469, "Service"), (473, 499, "Farm"),
          (503, 699, "Craft & repair"), (703, 799, "Operators"), (803, 859, "Transport & material moving"),
          (863, 889, "Laborers")]

# ---------------------------------------------------------------- PSID extra items (verified by label, see docstring)
TEN_MO = {1984: "V10519", 1985: "V11668", 1986: "V13068", 1987: "V14166", 1988: "V15181", 1989: "V16682",
          1990: "V18120", 1991: "V19420", 1992: "V20720"}
POS_MO = {1984: "V10520", 1985: "V11669", 1986: "V13069", 1987: "V14167"}
TEN_YMW = {1994: "ER2098", 1995: "ER5097", 1996: "ER7193", 1997: "ER10117", 1999: "ER13243", 2001: "ER17254",
           2003: "ER21171", 2005: "ER25160", 2007: "ER36165", 2009: "ER42200", 2011: "ER47513", 2013: "ER53213",
           2015: "ER60228", 2017: "ER66231", 2019: "ER72231", 2021: "ER78236", 2023: "ER82223"}   # + next two
# wave: (B24 employer start yr, B25, B26 yr, B30 yr, B31 yr, B27 chg, B32 chg, B29 type, B34 type)
POS = {1988: "V15183 V15184 V15186 V15191 V15193 V15187 V15194 V15189 V15196",
       1989: "V16684 V16685 V16687 V16692 V16694 V16688 V16695 V16690 V16697",
       1990: "V18122 V18123 V18125 V18130 V18132 V18126 V18133 V18128 V18135",
       1991: "V19422 V19423 V19425 V19430 V19432 V19426 V19433 V19428 V19435",
       1992: "V20722 V20723 V20725 V20730 V20732 V20726 V20733 V20728 V20735",
       1993: "V22491 V22492 V22494 V22499 V22501 V22495 V22502 V22497 V22504",
       1994: "ER2102 ER2103 ER2105 ER2110 ER2112 ER2106 ER2113 ER2108 ER2115",
       1995: "ER5101 ER5102 ER5104 ER5109 ER5111 ER5105 ER5112 ER5107 ER5114",
       1996: "ER7197 ER7198 ER7200 ER7205 ER7207 ER7201 ER7208 ER7203 ER7210",
       1997: "ER10121 ER10122 ER10124 ER10129 ER10131 ER10125 ER10132 ER10127 ER10134",
       1999: "ER13247 ER13248 ER13250 ER13255 ER13257 ER13251 ER13258 ER13253 ER13260",
       2001: "ER17258 ER17259 ER17261 ER17266 ER17268 ER17262 ER17269 ER17264 ER17271"}
POS_K = ["empy", "b25", "p26", "p30", "p31", "c27", "c32", "t29", "t34"]
WHY_E = {1976: "V4490", 1977: "V5399", 1978: "V5890", 1979: "V6501", 1980: "V7104", 1981: "V7727", 1982: "V8391",
         1983: "V9022", 1984: "V10539", 1985: "V11679", 1986: "V13079", 1987: "V14177"}


# ================================================================ occupation crosswalks and the MORG score
def crosswalks():
    """{scheme: {code: occ1990dd}} from Dorn's files (data only)."""
    out = {}
    for s, f in (("1970", "occ1970_occ1990dd.dta"), ("1980", "occ1980_occ1990dd.dta"),
                 ("1990", "occ1990_occ1990dd.dta"), ("2000", "occ2000_occ1990dd.dta"),
                 ("2010", "occ2010_occ1990dd.dta")):
        x = pd.read_stata(XW / f)
        k = pd.to_numeric(x["occ"], errors="coerce")
        v = pd.to_numeric(x["occ1990dd"], errors="coerce")
        out[s] = {int(a): int(b) for a, b in zip(k, v) if a == a and b == b and b < 900}
    return out


def to_dd(code, scheme, XWD):
    m = XWD[scheme]
    c = pd.to_numeric(pd.Series(code), errors="coerce")
    return c.map(lambda x: m.get(int(x), np.nan) if x == x else np.nan).to_numpy(float)


def group_of(dd):
    g = np.full(len(dd), np.nan)
    for k, (lo, hi, _) in enumerate(GROUPS):
        g[(dd >= lo) & (dd <= hi)] = k
    return g


def morg_cells(XWD):
    """occ1990dd x year: n, sum of weights, weighted mean of the relative ln wage (men 25-64)."""
    if C_MORG.exists():
        return pd.read_pickle(C_MORG)
    rows = []
    for y in range(1979, 2020):
        f = MORG / f"morg{y % 100:02d}.dta"
        cols = list(pd.read_stata(f, iterator=True).variable_labels())
        if y <= 1982:
            oc, sch = "occ70", "1970"
        elif y <= 1991:
            oc, sch = "occ80", "1980"
        elif y <= 2002:
            oc, sch = "occ80", "1990"
        elif y <= 2010:
            oc, sch = "occ00", "2000"
        else:
            oc, sch = ("occ2012" if "occ2012" in cols else "occ2011"), "2010"
        want = [c for c in ("age", "sex", "earnwt", "paidhre", "earnhre", "earnwke", "uhourse", oc, "occ2011")
                if c in cols]
        d = pd.read_stata(f, columns=list(dict.fromkeys(want)), convert_categoricals=False)
        for c in d.columns:
            d[c] = pd.to_numeric(d[c], errors="coerce")
        d = d[(d["sex"] == 1) & d["age"].between(25, 64)].copy()
        code = d[oc]
        if y == 2012 and "occ2011" in d:
            code = code.fillna(d["occ2011"])
        if sch == "2000":
            code = code // 10
        d["dd"] = to_dd(code, sch, XWD)
        top = 999 if y <= 1988 else 1923 if y <= 1997 else 2884.61
        wk = d["earnwke"].where(d["earnwke"] > 0)
        wk = np.where(wk >= top - 0.5, wk * 1.4, wk)
        hr = d["uhourse"].where(d["uhourse"] > 0)
        w = np.where((d["paidhre"] == 1) & (d["earnhre"] > 0), d["earnhre"] / 100, wk / hr)
        w = pd.Series(w, index=d.index) * CPI[2000] / CPI[y]
        d["lw"] = np.log(w.where(w.between(2, 200)))
        d["wt"] = d["earnwt"].where(d["earnwt"] > 0)
        d = d.dropna(subset=["lw", "wt"])
        mu = np.average(d["lw"], weights=d["wt"])
        d["rel"] = d["lw"] - mu
        d = d.dropna(subset=["dd"])
        g = d.assign(wr=d["wt"] * d["rel"]).groupby("dd").agg(n=("rel", "size"), sw=("wt", "sum"), swr=("wr", "sum"))
        g["year"] = y
        rows.append(g.reset_index())
        print(f"  MORG {y}: {oc} ({sch}) {len(d):,} men with wage and occupation, {g.shape[0]} occupations",
              flush=True)
    c = pd.concat(rows, ignore_index=True)
    c.to_pickle(C_MORG)
    return c


def scores(cells):
    """fixed score by occupation, time-varying score by (occupation, year), group score; supervisory set."""
    def agg(x):
        return pd.DataFrame({"n": x.groupby("dd")["n"].sum(), "s": x.groupby("dd")["swr"].sum()
                             / x.groupby("dd")["sw"].sum()})
    base = agg(cells[cells["year"].between(*BASE)])
    allyr = agg(cells)
    fx = base["s"].where(base["n"] >= 50)
    fx = fx.reindex(allyr.index.union(base.index)).fillna(allyr["s"].where(allyr["n"] >= 50))
    gw = pd.DataFrame({"dd": allyr.index, "g": group_of(allyr.index.to_numpy(float)), "s": allyr["s"].to_numpy(),
                       "n": allyr["n"].to_numpy()}).dropna()
    gs = gw.groupby("g").apply(lambda z: np.average(z["s"], weights=z["n"]))
    allcodes = pd.Index(sorted(set(fx.index) | set(cells["dd"])))
    fx = fx.reindex(allcodes)
    grp = pd.Series(group_of(allcodes.to_numpy(float)), index=allcodes).map(gs)
    fx = fx.fillna(grp)
    tv = {}
    for y in range(1979, 2020):
        z = agg(cells[cells["year"].between(y - 1, y + 1)])
        tv[y] = z["s"].where(z["n"] >= 30)
    tv = pd.DataFrame(tv).reindex(allcodes)
    for y in tv.columns:
        tv[y] = tv[y].fillna(fx)
    return dict(fixed=fx, tv=tv, group=grp, nbase=base["n"].reindex(allcodes))


# ================================================================ PSID extra items
def yr(v, wave):
    """PSID year codes -> (year, flag): flag 'pw' = previous or current year DK which, 'early' = before window."""
    v = pd.to_numeric(v, errors="coerce")
    out = pd.Series(np.nan, index=v.index)
    early = pd.Series(False, index=v.index)
    if wave <= 1992 or wave == 1994:             # two-digit years (1994 too)
        ok = v.between(1, 95) & (v <= wave - 1900)
        out[ok] = 1900 + v[ok]
        out[v == 96] = wave - 1
        early[v == 97] = True
    else:
        ok = v.between(1901, wave)
        out[ok] = v[ok]
        out[v == 9996] = wave - 1
        early[v == 9997] = True
    return out, early


def psid_items():
    """wave x interview number: tenure (years), within-employer position change, reported promotion."""
    if C_PSID.exists():
        return pd.read_pickle(C_PSID)
    out = []
    for w in psid1.WAVES:
        if w < 1976:
            continue
        folder = FAM / (f"fam{w}" if w < 1994 else f"fam{w}er")
        base = next(f for f in folder.glob("*.do") if "formats" not in f.name).with_suffix("")
        pos, labs = layout(base.with_suffix(".do"))
        idv = labs[1][0]
        cols = [idv]
        if w in TEN_MO:
            cols.append(TEN_MO[w])
        if w in POS_MO:
            cols.append(POS_MO[w])
        if w in TEN_YMW:
            v = TEN_YMW[w]
            pre, num = re.match(r"([A-Z]+)(\d+)", v).groups()
            ymw = [v, f"{pre}{int(num) + 1}", f"{pre}{int(num) + 2}"]
            cols += ymw
        if w in POS:
            cols += POS[w].split()
        if w in WHY_E:
            cols.append(WHY_E[w])
        lab = dict(labs)
        f = read(base, cols, pos)
        x = pd.DataFrame({"wave": w, "int": f[idv]})
        ten = pd.Series(np.nan, index=f.index)
        if w in TEN_MO:
            m = pd.to_numeric(f[TEN_MO[w]], errors="coerce")
            ten = (m.where(m.between(1, 997)) / 12)
        if w in TEN_YMW:
            yv, mv, wv = (pd.to_numeric(f[c], errors="coerce") for c in ymw)
            ten = yv.where(yv.between(1, 75)).astype(float)
            ten = ten.fillna(mv.where(mv.between(0.01, 900)) / 12).fillna(wv.where(wv.between(0.01, 900)) / 52)
        x["pos_ch"] = np.nan
        if w in POS:
            P = dict(zip(POS_K, POS[w].split()))
            ye, ee = yr(f[P["empy"]], w)
            if w == 1993:
                ten = (w - ye + 0.5).where(ye.notna())
            yp = pd.Series(np.nan, index=f.index)
            for k in ("p26", "p30", "p31"):
                a, _ = yr(f[P[k]], w)
                yp = yp.fillna(a)
            b25 = pd.to_numeric(f[P["b25"]], errors="coerce")
            yp = yp.where(~((b25 == 1) & ye.notna()), ye)
            lo = w - (2 if w >= 1999 else 1)
            inwin = yp.between(lo, w)
            after = (ye < yp) | (ee & yp.notna())
            chg = (pd.to_numeric(f[P["c27"]], errors="coerce") == 1) | (pd.to_numeric(f[P["c32"]], errors="coerce") == 1)
            known = ye.notna() | ee
            x["pos_ch"] = ((inwin & after) | chg).astype(float).where(known)
            t = pd.concat([pd.to_numeric(f[P["t29"]], errors="coerce"), pd.to_numeric(f[P["t34"]], errors="coerce")],
                          axis=1)
            x["pos_type"] = t.where(t.isin([1, 5, 7])).max(axis=1)          # 1 promotion with higher pay
            x["empy"] = ye
        if w in POS_MO:
            pm = pd.to_numeric(f[POS_MO[w]], errors="coerce")
            tm = pd.to_numeric(f[TEN_MO[w]], errors="coerce")
            ok = pm.between(1, 997) & tm.between(1, 997)
            x["pos_ch"] = ((pm < tm - 1) & (pm <= 15)).astype(float).where(ok)
        if w in WHY_E:
            c = pd.to_numeric(f[WHY_E[w]], errors="coerce")
            x["why_e"] = c
        x["tenure"] = ten
        out.append(x)
        print(f"  PSID {w}: tenure {int(ten.notna().sum()):,}; position-change known "
              f"{int(x['pos_ch'].notna().sum()):,} (rate {x['pos_ch'].mean():.3f}); "
              + (f"why_e code 6 share among coded {((x['why_e'] == 6).sum() / max(1, x['why_e'].between(1, 8).sum())):.3f}"
                 if w in WHY_E else ""), flush=True)
    res = pd.concat(out, ignore_index=True)
    res.to_pickle(C_PSID)
    return res


# ================================================================ NLSY79 extraction
def nlsy_extract():
    if C_NLS.exists():
        return pd.read_pickle(C_NLS)
    ix = pd.read_csv(DATA / "nlsy79_codebook.csv")
    q = ix["qname"].astype(str)
    m = q.str.match(r"^EMPLOYERS_ALL_(OCC|HRLY_WAGE|CPSJOB|CURWK)_\d{4}\.\d\d$")
    p = q.str.match(r"^(QES-PROMO3[89]\.0[1-5]|ES-16_[1-5])$")
    sel = ix[m | p].copy()
    cols = ["R0000100"] + sel["col"].tolist()
    print(f"NLSY79: reading {len(cols):,} columns from the full release (slow) ...", flush=True)
    d = pd.read_csv(NLS / "nlsy79_all_1979-2022.csv", usecols=cols)
    ren = {"R0000100": "pid"}
    for c, qn, y in zip(sel["col"], sel["qname"], sel["year"]):
        ren[c] = f"{qn}|{y}" if not qn.startswith("EMPLOYERS") else qn
    d = d.rename(columns=ren)
    d.to_pickle(C_NLS)
    return d


# ================================================================ PSID son panel
def occ_scheme(wave):
    return "1970" if wave <= 2001 else "2000" if wave <= 2015 else "2010"


def attach_scores(d, code_col, scheme_col, year_col, XWD, S):
    """occ1990dd, fixed / time-varying / group scores, supervisory-managerial indicator."""
    dd = np.full(len(d), np.nan)
    for sch in d[scheme_col].dropna().unique():
        m = (d[scheme_col] == sch).to_numpy()
        dd[m] = to_dd(d.loc[m, code_col].to_numpy(), sch, XWD)
    d["dd"] = dd
    d["os"] = d["dd"].map(S["fixed"])
    d["os_g"] = d["dd"].map(S["group"])
    yy = d[year_col].clip(1979, 2019).astype(int)
    tv = S["tv"]
    d["os_t"] = [tv.at[o, y] if o == o and o in tv.index else np.nan for o, y in zip(d["dd"], yy)]
    d["os_t"] = d["os_t"].astype(float)
    d["supm"] = d["dd"].isin(MAN | SUP).astype(float).where(d["dd"].notna())
    d["man"] = d["dd"].isin(MAN).astype(float).where(d["dd"].notna())
    return d


def son_panel(XWD, S):
    a, py, ch = D24.load()
    r, _ = D24.frames(a, ch, 0)
    ids = a[a["head"] & (a["female"] == 0)][["pid", "wave", "int", "wt", "est"]].drop_duplicates(["pid", "wave"])
    r = r.merge(ids, on=["pid", "wave"], how="left")
    X = pd.read_pickle(DATA / "correlated_shocks_fam.pkl")["X"][["wave", "int", "h_occ"]]
    r = r.merge(X, on=["wave", "int"], how="left")
    c = pd.to_numeric(r["h_occ"], errors="coerce")
    r["occ_raw"] = c.where(((r["wave"] < 2017) & c.between(1, 998)) | ((r["wave"] >= 2017) & c.between(1, 9998)))
    r["scheme"] = r["wave"].map(occ_scheme)
    r = attach_scores(r, "occ_raw", "scheme", "year", XWD, S)
    r["os"] = r["os"].where(r["valid"])
    for k in ("os_t", "os_g"):
        r[k] = r[k].where(r["valid"])
    r["res"], r["res_t"], r["res_g"] = r["lw"] - r["os"], r["lw"] - r["os_t"], r["lw"] - r["os_g"]
    it = psid_items()
    r = r.merge(it[["wave", "int", "tenure", "pos_ch", "pos_type", "why_e"]], on=["wave", "int"], how="left")
    work = r["occ_raw"].notna() & ((r["est"] == 1) | r["est"].isna())
    r["promo_rep"] = np.where(r["wave"].between(1976, 1987) & work, (r["why_e"] == 6).astype(float), np.nan)
    r["pos_ch"] = r["pos_ch"].where(work)
    r["tenure"] = r["tenure"].where(work).clip(upper=40)
    dp = pd.read_pickle(DATA / "psid_displacement.pkl")
    dm = dp[dp["main"] == 1][["pid", "year"]].drop_duplicates().assign(disp_t=1.0)
    r = r.merge(dm, on=["pid", "year"], how="left")
    r["disp_t"] = r["disp_t"].fillna(0.0).where(r["year"].between(1968, 2022))
    r["black"] = (r["race"] == "Black").astype(float)
    r["wpool"] = r["wt"].where(r["wt"] > 0)
    # starting position: education, mean ln wage and score at 28-32
    s30 = r[r["age"].between(28, 32)].groupby("pid")
    r["lw30"] = r["pid"].map(s30["lw"].mean())
    r["os30"] = r["pid"].map(s30["os"].mean())
    r["lyp_c"] = r["lyp"] - r["lyp"].mean()
    return transitions(r.sort_values(["pid", "wave"]).reset_index(drop=True))


def transitions(r):
    """Changes from the previous interview with a valid occupation (<= 2 years back)."""
    v = r[r["dd"].notna()][["pid", "wave", "dd", "os", "supm", "lw", "res", "occ_raw"]].copy()
    v["os_all"] = v["dd"].map(SCORES["fixed"])
    p = v.groupby("pid").shift(1)
    v["gap"] = v["wave"] - p["wave"]
    ok = v["gap"].between(1, 2)
    v["occ_ch"] = (v["dd"] != p["dd"]).astype(float).where(ok)
    v["d_os"] = (v["os_all"] - p["os_all"]).where(ok)
    v["up"] = ((v["occ_ch"] == 1) & (v["d_os"] > 0)).astype(float).where(ok)
    v["up10"] = ((v["occ_ch"] == 1) & (v["d_os"] >= 0.10)).astype(float).where(ok)
    v["down10"] = ((v["occ_ch"] == 1) & (v["d_os"] <= -0.10)).astype(float).where(ok)
    v["sup_in"] = (v["supm"] == 1).astype(float).where(ok & (p["supm"] == 0))
    v["g_os"] = v["d_os"] / v["gap"]
    v["d_lw"] = (v["lw"] - p["lw"]).where(ok)
    v["g_lw"] = v["d_lw"] / v["gap"]
    v["g_osv"] = ((v["os"] - p["os"]) / v["gap"]).where(ok & v["d_lw"].notna())
    v["g_res"] = v["g_lw"] - v["g_osv"]
    keep = ["occ_ch", "d_os", "up", "up10", "down10", "sup_in", "g_os", "d_lw", "g_lw", "g_osv", "g_res", "gap"]
    r = r.merge(v[["pid", "wave"] + keep], on=["pid", "wave"], how="left")
    r["pos_up"] = ((r["pos_ch"] == 1) & (r["d_lw"] > 0)).astype(float).where(r["pos_ch"].notna() & r["d_lw"].notna())
    r["pos_upo"] = ((r["pos_ch"] == 1) & (r["d_os"] > 0)).astype(float).where(r["pos_ch"].notna() & r["d_os"].notna())
    # within-job split (tenure observed at this interview): stayer = with the employer since the previous interview
    st = (r["tenure"] >= r["gap"] - 0.5).astype(float).where(r["tenure"].notna() & r["g_lw"].notna() &
                                                             r["g_osv"].notna())
    r["stay"] = st
    for k, s in (("s", 1.0), ("m", 0.0)):
        r[f"g_os_{k}"] = r["g_osv"].where(st.notna()) * (st == s)
        r[f"g_res_{k}"] = r["g_res"].where(st.notna()) * (st == s)
    r["g_lw_t"] = r["g_lw"].where(st.notna())
    return r


# ================================================================ estimation with cluster influence functions
RES = {}


def est(key, d, y, X, cl, w=None, names=("x",), extra=None):
    """WLS; stores coefficient, CR1-ready influence vector over global clusters for the first len(names) columns."""
    yv = d[y].to_numpy(float)
    wv = np.ones(len(d)) if w is None else w
    Xw = X * wv[:, None]
    A = np.linalg.pinv(X.T @ Xw)
    b = A @ (Xw.T @ yv)
    e = yv - X @ b
    U = Xw * e[:, None]
    n, k = X.shape
    G = len(np.unique(cl))
    adj = G / max(G - 1, 1) * (n - 1) / max(n - k, 1)
    for j, nm in enumerate(names):
        psi = np.bincount(cl, weights=U @ A[:, j], minlength=NCL)
        RES[(key, nm)] = dict(b=b[j], psi=psi * np.sqrt(adj), n=n, G=G,
                              mean=float(np.average(yv, weights=wv)), **(extra or {}))
    RES[(key, "x")] = RES[(key, names[0])]                          # alias of the first regressor
    return b


def comb(terms):
    """sum_c coef_c * b_c with its s.e. from the stacked influence vectors."""
    b = sum(c * RES[k]["b"] for k, c in terms)
    psi = sum(c * RES[k]["psi"] for k, c in terms)
    se = float(np.sqrt(psi @ psi))
    return b, se, (2 * norm.sf(abs(b / se)) if se > 0 else np.nan)


def ratio(num, den):
    """ratio of two linear combinations (delta method)."""
    bn, _, _ = comb(num)
    bd, _, _ = comb(den)
    psi_n = sum(c * RES[k]["psi"] for k, c in num)
    psi_d = sum(c * RES[k]["psi"] for k, c in den)
    g = psi_n / bd - bn / bd ** 2 * psi_d
    rr, se = bn / bd, float(np.sqrt(g @ g))
    if abs(bd) < 2 * float(np.sqrt(psi_d @ psi_d)):                 # denominator not different from zero
        return np.nan, np.nan, np.nan
    return rr, se, (2 * norm.sf(abs(rr / se)) if se > 0 else np.nan)


def cell(t):
    b, se, p = t
    if not np.isfinite(b) or not np.isfinite(se):
        return ""
    pv = "<0.001" if p < 0.001 else f"{p:.3f}"
    return f"{b:.3f}{stars(p)} ({se:.3f}; p={pv})"


def one(key):
    return comb([(key, 1.0)])


CSV = []


def rec(table, sample, outcome, term, t, n=np.nan, clusters=np.nan, mean=np.nan, **kw):
    b, se, p = t
    CSV.append(dict(table=table, sample=sample, outcome=outcome, term=term, coef=b, se=se, p=p, n=n,
                    clusters=clusters, mean=mean, **kw))


def table(header, panels):
    return D24.table(header, panels)


def ctrl_lsn(d):
    return D24.controls(d, "lyp", "LSN")


def ctrl_ageyr(d, fe="year"):
    C = d["C"].to_numpy(float) / 10
    fx = pd.get_dummies(d[fe].astype(int), drop_first=True, dtype=float).to_numpy()
    return np.column_stack([np.ones(len(d))] + [C ** k for k in range(1, 5)] + [fx])


GROUPS3 = [("P", "Pooled (weighted)"), ("B", "Black"), ("W", "White")]
MIN_CELL = 250                                                      # smallest estimation cell (observations)
BANDS = [(25, 34), (35, 44), (45, 55), (35, 55), (25, 55)]


def subset(d, g):
    if g == "P":
        return d[d["wpool"].notna()], "wpool"
    if g == "all":
        return d[d["race"].isin(["Black", "White"])], None
    return d[d["race"] == ("Black" if g == "B" else "White")], None


def run_cells(tag, d, ys, xcols, ctrl, need, bands=BANDS, groups=("P", "B", "W"), cl="fam68"):
    """estimate y on xcols + ctrl(d) in each band x group on a common sample; store influence vectors."""
    info = {}
    for lo, hi in bands:
        for g in groups:
            dd, wc = subset(d[d["age"].between(lo, hi)], g)
            dd = dd.dropna(subset=list(ys) + list(xcols) + list(need) + ([wc] if wc else []))
            if len(dd) < MIN_CELL:
                continue
            X = np.column_stack([dd[x].to_numpy(float) for x in xcols] + [ctrl(dd)])
            clv = CLIDX.get_indexer(dd[cl].to_numpy())
            w = dd[wc].to_numpy(float) if wc else None
            for y in ys:
                est((tag, y, lo, hi, g), dd, y, X, clv, w, names=xcols,
                    extra=dict(children=dd["pid"].nunique()))
            info[(lo, hi, g)] = (len(dd), dd["pid"].nunique(), len(np.unique(clv)))
    return info


# ================================================================ PSID analyses
def sec_decomp(r, md):
    """Table 1: wage persistence by age band = between-occupation (score) + within-occupation (residual)."""
    VARS = [("lw", "os", "res", "fixed 1992-2002 score"), ("lw", "os_t", "res_t", "time-varying score"),
            ("lw", "os_g", "res_g", "11 major groups")]
    out = {}
    for lw, os_, res, lab in VARS:
        info = run_cells(("dec", lab), r, (lw, os_, res), ("lyp",), ctrl_lsn, ("A", "C"))
        out[lab] = info
    lab0 = VARS[0][3]
    K = lambda y, lo, hi, g, lab=lab0: (("dec", lab), y, lo, hi, g)
    hdr = ["(1) ln wage", "(2) occupation score", "(3) within-occupation residual",
           "(4) share between = (2)/(1)", "(5) occupation score, time-varying", "(6) residual, time-varying",
           "(7) score, 11 major groups", "(8) residual, 11 groups"]
    panels = []
    for g, gname in GROUPS3 + [("BW", "Black - White")]:
        rows = []
        for lo, hi in BANDS:
            def L(y, lab=lab0):
                if g == "BW":
                    return [((K(y, lo, hi, "B", lab), "x"), 1.0), ((K(y, lo, hi, "W", lab), "x"), -1.0)]
                return [((K(y, lo, hi, g, lab), "x"), 1.0)]
            t = [comb(L("lw")), comb(L("os")), comb(L("res")), ratio(L("os"), L("lw")),
                 comb(L("os_t", VARS[1][3])), comb(L("res_t", VARS[1][3])), comb(L("os_g", VARS[2][3])),
                 comb(L("res_g", VARS[2][3]))]
            rows.append((f"ln parental income, sons {lo}-{hi}", [cell(x) for x in t]))
            for y, x in zip(["lw", "os", "res", "share_between", "os_t", "res_t", "os_g", "res_g"], t):
                rec("1 decomposition", gname, y, f"lyp, {lo}-{hi}", x,
                    n=out[lab0].get((lo, hi, g), (np.nan,))[0] if g != "BW" else np.nan)
        if g != "BW":
            rows.append(("N son-years / sons / clusters (cols 1-4)",
                         [" ; ".join(f"{lo}-{hi}: {out[lab0][(lo, hi, g)][0]:,}/{out[lab0][(lo, hi, g)][1]:,}/"
                                     f"{out[lab0][(lo, hi, g)][2]:,}" for lo, hi in BANDS[:3])] + [""] * 7))
        panels.append((gname, rows))
    # changes across bands (career divergence)
    rows = []
    for g, gname in GROUPS3 + [("BW", "Black - White")]:
        for (a0, a1), (b0, b1) in (((25, 34), (45, 55)), ((25, 34), (35, 55))):
            def D(y, lab=lab0):
                gs = [("B", 1.0), ("W", -1.0)] if g == "BW" else [(g, 1.0)]
                return ([((K(y, b0, b1, gg, lab), "x"), s) for gg, s in gs] +
                        [((K(y, a0, a1, gg, lab), "x"), -s) for gg, s in gs])
            t = [comb(D("lw")), comb(D("os")), comb(D("res")), ratio(D("os"), D("lw")),
                 comb(D("os_t", VARS[1][3])), comb(D("res_t", VARS[1][3])), comb(D("os_g", VARS[2][3])),
                 comb(D("res_g", VARS[2][3]))]
            rows.append((f"{gname}: ({b0}-{b1}) - ({a0}-{a1})", [cell(x) for x in t]))
            for y, x in zip(["lw", "os", "res", "share_between", "os_t", "res_t", "os_g", "res_g"], t):
                rec("1 decomposition change", gname, y, f"({b0}-{b1}) - ({a0}-{a1})", x)
    panels.append(("Change in the coefficient across age bands (career divergence)", rows))
    md += ["## 1. Wage persistence by age band: between occupations vs within occupation", "",
           "One regression per cell: the son's outcome (column header) on ln parental income (6.IGEMain regressor), "
           "child-years in the age band, Lee-Solon controls without the x-age interactions (24 section 1b). "
           "ln wage = occupation score + within-occupation residual, so (1) = (2) + (3) = (5) + (6) = (7) + (8) on the "
           "same sample (son-years with a valid wage and a mapped occupation). All cells are estimated as one stacked "
           "system (influence functions clustered by 1968 family), so differences across bands and races and the "
           "share in (4) (delta method) have proper s.e. Pooled = Black + White sons with the son's individual weight; "
           "Black and White unweighted (as in 24). Column (4) is left blank when the denominator is not different from "
           "zero (|t| < 2). **Accounting, not causal: sons select into occupations.**", ""]
    md += table(hdr, panels)
    return out


def sec_career(r, md):
    """Table 2: within-son career growth (mean 35-55 minus mean 25-34) on parental income."""
    v = r[r["os"].notna()]
    y = v[v["age"].between(25, 34)].groupby("pid").agg(lw0=("lw", "mean"), os0=("os", "mean"), a0=("age", "mean"),
                                                        n0=("lw", "size"))
    o = v[v["age"].between(35, 55)].groupby("pid").agg(lw1=("lw", "mean"), os1=("os", "mean"), a1=("age", "mean"),
                                                       n1=("lw", "size"), wpool=("wpool", "mean"))
    p = y.join(o, how="inner")
    p = p[(p["n0"] >= 2) & (p["n1"] >= 2)]
    first = r.drop_duplicates("pid").set_index("pid")
    p = p.join(first[["race", "lyp", "A", "birth_year", "fam68", "educ"]])
    p["d_lw"], p["d_os"] = p["lw1"] - p["lw0"], p["os1"] - p["os0"]
    p["d_res"] = p["d_lw"] - p["d_os"]
    p["age"] = 40
    p["pid"] = p.index

    def ctrl(d):
        A = (d["A"].to_numpy(float) - 45) / 10
        a0, a1 = (d["a0"].to_numpy(float) - 30) / 10, (d["a1"].to_numpy(float) - 42) / 10
        by = (d["birth_year"].to_numpy(float) - 1960) / 10
        return np.column_stack([np.ones(len(d)), A, A ** 2, a0, a0 ** 2, a1, a1 ** 2, by, by ** 2])
    info = run_cells("career", p, ("d_lw", "d_os", "d_res"), ("lyp",), ctrl, ("A", "birth_year"), bands=[(40, 40)])
    hdr = ["(1) growth of ln wage", "(2) growth of occupation score", "(3) growth of within-occupation residual",
           "(4) share between = (2)/(1)", "(5) mean ln wage at 25-34", "(6) mean growth of ln wage"]
    panels = []
    for g, gname in GROUPS3 + [("BW", "Black - White")]:
        L = (lambda y: [((("career", y, 40, 40, "B"), "x"), 1.0), ((("career", y, 40, 40, "W"), "x"), -1.0)]) \
            if g == "BW" else (lambda y: [((("career", y, 40, 40, g), "x"), 1.0)])
        t = [comb(L("d_lw")), comb(L("d_os")), comb(L("d_res")), ratio(L("d_os"), L("d_lw"))]
        for yv, x in zip(["d_lw", "d_os", "d_res", "share_between"], t):
            rec("2 career growth", gname, yv, "lyp", x, n=info.get((40, 40, g), (np.nan,))[0])
        if g != "BW":
            sub = p if g == "P" else p[p["race"] == ("Black" if g == "B" else "White")]
            ww = sub["wpool"].fillna(0) if g == "P" else None
            m0 = np.average(sub["lw0"], weights=ww) if g == "P" and ww.sum() > 0 else sub["lw0"].mean()
            m1 = np.average(sub["d_lw"], weights=ww) if g == "P" and ww.sum() > 0 else sub["d_lw"].mean()
            rows = [("ln parental income", [cell(x) for x in t] + ["", ""]),
                    ("Mean", ["", "", "", "", f"{m0:.3f}", f"{m1:.3f}"]),
                    ("N sons / clusters", [f"{info[(40, 40, g)][0]:,} / {info[(40, 40, g)][2]:,}"] * 4 + ["", ""])]
        else:
            rows = [("ln parental income", [cell(x) for x in t] + ["", ""])]
        panels.append((gname, rows))
    md += ["## 2. Career wage growth within sons", "",
           "One row per son observed with >= 2 valid years (wage and occupation) at 25-34 and >= 2 at 35-55. Outcome = "
           "mean at 35-55 minus mean at 25-34 (column header); regressor ln parental income; controls: quadratics in "
           "the father's age at 16, the son's mean age in each window and his birth year. (1) = (2) + (3). Pooled "
           "weighted by the son's mean individual weight at 35-55; s.e. clustered by 1968 family.", ""]
    md += table(hdr, panels)
    return p


def sec_growth(r, md):
    """Table 3: annual wage growth split into occupation-score and residual growth, stayers vs employer changers."""
    d = r[r["g_lw_t"].notna() & r["wave"].ge(1985)].copy()
    ys = ("g_lw_t", "g_os_s", "g_res_s", "g_os_m", "g_res_m", "stay")
    info = run_cells("growth", d, ys, ("lyp",), ctrl_ageyr, ("C",), bands=[(25, 34), (35, 55)])
    hdr = ["(1) annual ln wage growth", "(2) score growth, same employer", "(3) residual growth, same employer",
           "(4) score growth, new employer", "(5) residual growth, new employer", "(6) stayed with employer"]
    panels = []
    for g, gname in GROUPS3 + [("BW", "Black - White")]:
        rows = []
        for lo, hi in ((25, 34), (35, 55)):
            L = (lambda y: [((("growth", y, lo, hi, "B"), "x"), 1.0), ((("growth", y, lo, hi, "W"), "x"), -1.0)]) \
                if g == "BW" else (lambda y: [((("growth", y, lo, hi, g), "x"), 1.0)])
            t = [comb(L(y)) for y in ys]
            rows.append((f"ln parental income, sons {lo}-{hi}", [cell(x) for x in t]))
            for yv, x in zip(ys, t):
                rec("3 annual growth", gname, yv, f"lyp, {lo}-{hi}", x,
                    n=info.get((lo, hi, g), (np.nan,))[0], mean=RES.get((("growth", yv, lo, hi, g), "x"),
                                                                       {}).get("mean", np.nan))
            if g != "BW":
                rows.append((f"Mean, {lo}-{hi}", [f"{RES[(('growth', y, lo, hi, g), 'x')]['mean']:.4f}" for y in ys]))
                rows.append((f"N son-year pairs / clusters, {lo}-{hi}",
                             [f"{info[(lo, hi, g)][0]:,} / {info[(lo, hi, g)][2]:,}"] * len(ys)))
        panels.append((gname, rows))
    md += ["## 3. Annual wage growth: occupational upgrading vs within-occupation growth, within vs across employers",
           "", "Consecutive interviews (1-2 years apart, waves 1985-2023) with a valid wage, a mapped occupation and "
           "tenure with the present employer at the later interview. Annualised growth of ln wage (income years "
           "w_prev - 1 -> w - 1) = growth of the occupation score + growth of the residual, each split by whether the "
           "son stayed with the same employer (tenure >= years since the previous interview - 0.5) or not: (1) = (2) + "
           "(3) + (4) + (5). (6) = share of stayers. Controls: quartic in age, year FE. Within-employer score growth is "
           "promotion into a better-paid occupation with the same employer; residual growth with the same employer is "
           "within-job (and within-occupation) wage growth. Measurement error in occupation codes inflates score "
           "changes in both directions.", ""]
    md += table(hdr, panels)


PROMO_Y = [("up", "(1) moved to a higher-paying occupation"), ("up10", "(2) ... by >= 0.10 log points"),
           ("sup_in", "(3) entered a supervisory / managerial occupation"), ("g_os", "(4) annual change in score"),
           ("promo_rep", "(5) reported promotion (1976-87)"), ("pos_ch", "(6) position change, same employer (1984-2001)"),
           ("pos_up", "(7) ... with a wage gain"), ("down10", "(8) moved to a lower-paying occupation (>= 0.10)")]


def sec_promo(r, md):
    """Table 4: promotion / upgrading per year by parental income; Table 5 conditional on the starting position."""
    ys = [y for y, _ in PROMO_Y]
    info = {}
    for y in ys:
        info[y] = run_cells("promo", r, (y,), ("lyp",), ctrl_ageyr, ("C",), bands=[(25, 34), (35, 55)])
    panels = []
    for g, gname in GROUPS3 + [("BW", "Black - White")]:
        rows = []
        for lo, hi in ((25, 34), (35, 55)):
            t = []
            for y in ys:
                if g == "BW":
                    k1, k2 = (("promo", y, lo, hi, "B"), "x"), (("promo", y, lo, hi, "W"), "x")
                    t.append(comb([(k1, 1.0), (k2, -1.0)]) if k1 in RES and k2 in RES else (np.nan,) * 3)
                else:
                    k = (("promo", y, lo, hi, g), "x")
                    t.append(one(k) if k in RES else (np.nan,) * 3)
            rows.append((f"ln parental income, sons {lo}-{hi}", [cell(x) for x in t]))
            for y, x in zip(ys, t):
                k = (("promo", y, lo, hi, g if g != "BW" else "B"), "x")
                rec("4 promotion", gname, y, f"lyp, {lo}-{hi}", x, n=info[y].get((lo, hi, g), (np.nan,))[0],
                    mean=RES[k]["mean"] if (g != "BW" and k in RES) else np.nan)
            if g != "BW":
                rows.append((f"Mean of outcome, {lo}-{hi}",
                             [f"{RES[(('promo', y, lo, hi, g), 'x')]['mean']:.3f}" if (("promo", y, lo, hi, g), "x")
                              in RES else "" for y in ys]))
                rows.append((f"N son-years / clusters, {lo}-{hi}",
                             [f"{info[y][(lo, hi, g)][0]:,} / {info[y][(lo, hi, g)][2]:,}" if (lo, hi, g) in info[y]
                              else "" for y in ys]))
        panels.append((gname, rows))
    md += ["## 4. Promotion and occupational upgrading per year, by parental income", "",
           "Son-year linear probability models (column header = outcome), male heads, controls: quartic in age, year "
           "FE; s.e. clustered by 1968 family. (1)-(4), (8): change of the (consistent occ1990dd) occupation between "
           "consecutive interviews 1-2 years apart (score = fixed 1992-2002 relative wage); (3) among sons not in a "
           "supervisory / managerial occupation at the previous interview. (5) employed head whose job / position began "
           "within about a year says the previous one ended by promotion (waves 1976-1987; sons mostly < 40 then). (6) "
           "the present position with the present employer began since January of the previous calendar year (two "
           "years before in 1999 / 2001) and after the start with the employer (waves 1984-2001); (7) the same with "
           "a rise in the annual ln wage since the previous interview. Coded occupation changes include coding noise "
           "(PSID occupations are coded independently each wave after 1980), so (1)-(4) overstate true mobility; "
           "(6)-(7) are self-reported.", ""]
    md += table([h for _, h in PROMO_Y], panels)
    # ---- Table 5: conditional on education and the starting position (35-55)
    hdr = [h for _, h in PROMO_Y if not h.startswith("(5)")]
    ys5 = [y for y, h in PROMO_Y if not h.startswith("(5)")]
    XC = ("lyp", "educ", "lw30", "os30")
    panels = []
    for g, gname in GROUPS3:
        res = {}
        for y in ys5:
            res[y] = run_cells("promo_c", r, (y,), XC, ctrl_ageyr, ("C",), bands=[(35, 55)], groups=(g,))
        rows = []
        for x, lab in zip(XC, ("ln parental income", "years of education", "mean ln wage at 28-32",
                               "mean occupation score at 28-32")):
            t = [one((("promo_c", y, 35, 55, g), x)) if (("promo_c", y, 35, 55, g), x) in RES else (np.nan,) * 3
                 for y in ys5]
            rows.append((lab, [cell(z) for z in t]))
            for y, z in zip(ys5, t):
                rec("5 promotion | start", gname, y, x, z, n=res[y].get((35, 55, g), (np.nan,))[0])
        rows.append(("N son-years / clusters", [f"{res[y][(35, 55, g)][0]:,} / {res[y][(35, 55, g)][2]:,}"
                                               if (35, 55, g) in res[y] else "" for y in ys5]))
        panels.append((f"{gname}, sons 35-55", rows))
    md += ["## 5. Upgrading after 35, conditional on education and the starting position", "",
           "As Section 4, sons 35-55 who are observed at 28-32 (mean ln wage and occupation score there), adding years "
           "of education. The coefficient on ln parental income is then the gradient of progression for sons who "
           "started from the same position at 30.", ""]
    md += table(hdr, panels)


def sec_hegde(r, md):
    """Table 6: Black x high-parental-income x after-35 test (pooled, unweighted, with interactions)."""
    d = r[r["race"].isin(["Black", "White"])].copy()
    d["old"] = (d["age"] >= 35).astype(float)
    d["lyp_old"], d["blk_old"] = d["lyp_c"] * d["old"], d["black"] * d["old"]
    d["lyp_blk"], d["lyp_blk_old"] = d["lyp_c"] * d["black"], d["lyp_c"] * d["black"] * d["old"]
    XS = ("lyp_c", "lyp_old", "black", "blk_old", "lyp_blk", "lyp_blk_old")
    LAB = ("ln parental income (centred)", "x age 35-55", "Black", "Black x age 35-55", "ln parental income x Black",
           "ln parental income x Black x age 35-55")
    ys = [("lw", "ln wage"), ("os", "occupation score"), ("res", "within-occupation residual"),
          ("up", "moved to higher-paying occupation"), ("sup_in", "entered supervisory / managerial"),
          ("g_os", "annual change in score"), ("pos_ch", "position change, same employer"),
          ("pos_up", "position change with wage gain")]
    panels = []
    for spec, extra in (("A", ()), ("B", ("educ", "lw30", "os30"))):
        info = {}
        for y, _ in ys:
            dd = d.copy()
            dd["age"] = 40
            info[y] = run_cells(f"hegde{spec}", dd, (y,), XS + extra,
                                lambda z: np.column_stack([ctrl_ageyr(z), z["old"].to_numpy(float)]), ("C",),
                                bands=[(40, 40)], groups=("all",))
        rows = []
        for x, lab in zip(XS, LAB):
            t = [one(((f"hegde{spec}", y, 40, 40, "all"), x)) for y, _ in ys]
            rows.append((lab, [cell(z) for z in t]))
            for (y, _), z in zip(ys, t):
                rec(f"6 Hegde test {spec}", "Black + White", y, x, z, n=info[y][(40, 40, "all")][0])
        rows.append(("Controls", ["age quartic, year FE, age 35-55 dummy" + (", education, ln wage and score at "
                                                                            "28-32" if extra else "")] * len(ys)))
        rows.append(("N son-years / clusters", [f"{info[y][(40, 40, 'all')][0]:,} / {info[y][(40, 40, 'all')][2]:,}"
                                               for y, _ in ys]))
        panels.append(("A. unconditional" if spec == "A" else "B. conditional on education and the position at 28-32",
                       rows))
    md += ["## 6. Do Black sons from higher-income families progress less after 35? (Hegde et al. analogue)", "",
           "Black and White sons pooled (unweighted), son-years 25-55, one regression per column (outcome in the "
           "header) with the full set of interactions of ln parental income (centred at the sample mean), Black and "
           "age 35-55. The triple interaction is the difference in the after-35 change of the parental-income "
           "gradient between Black and White sons; 'Black x age 35-55' is the Black-White difference in the after-35 "
           "change at mean parental income. Hegde, Ljungqvist and Raj (2026) find that equally entitled Black "
           "examiners are promoted later, especially at senior grades; the analogue here is a negative triple "
           "interaction / Black x 35-55 term for upgrading outcomes.", ""]
    md += table([h for _, h in ys], panels)


def sec_tenure(r, md):
    """Table 7: returns to tenure (person FE) by parental income."""
    d = r[r["tenure"].notna() & r["lw"].notna() & r["os"].notna()].copy()
    d["ten"] = d["tenure"] / 10
    d["ten2"] = d["ten"] ** 2
    d["ten_lyp"] = d["ten"] * d["lyp_c"]
    ys = [("lw", "(1) ln wage"), ("os", "(2) occupation score"), ("res", "(3) within-occupation residual")]
    panels = []
    for g, gname in GROUPS3:
        sub, wc = subset(d[d["age"].between(25, 55)], g)
        sub = sub.copy()
        wv = sub.groupby("pid")["wpool"].transform("mean").to_numpy(float) if wc else np.ones(len(sub))
        Z = ctrl_ageyr(sub)[:, 1:]
        cols = ["ten", "ten2", "ten_lyp"]
        M = np.column_stack([sub[c].to_numpy(float) for c in cols] + [Z])
        gi = pd.factorize(sub["pid"])[0]
        cnt = np.bincount(gi, weights=wv)

        def dm(v):
            return v - (np.bincount(gi, weights=v * wv) / cnt)[gi]
        Md = np.column_stack([dm(M[:, j]) for j in range(M.shape[1])])
        clv = CLIDX.get_indexer(sub["fam68"].to_numpy())
        rows_b = {}
        for y, _ in ys:
            yy = sub.assign(_y=dm(sub[y].to_numpy(float)))
            est(("ten", y, g), yy, "_y", Md, clv, wv, names=tuple(cols), extra=dict(children=sub["pid"].nunique()))
        rows = []
        for c, lab in zip(cols, ("tenure (per 10 years)", "tenure squared", "tenure x ln parental income")):
            t = [one((("ten", y, g), c)) for y, _ in ys]
            rows.append((lab, [cell(z) for z in t]))
            for (y, _), z in zip(ys, t):
                rec("7 tenure", gname, y, c, z, n=len(sub))
        rows.append(("Person FE, age quartic, year FE; N son-years / sons / clusters",
                     [f"{len(sub):,} / {sub['pid'].nunique():,} / {len(np.unique(clv)):,}"] * 3))
        panels.append((gname, rows))
    for c in ("ten", "ten_lyp"):
        t = [comb([((("ten", y, "B"), c), 1.0), ((("ten", y, "W"), c), -1.0)]) for y, _ in ys]
        panels[-1][1].append((f"Black - White: {c}", [cell(z) for z in t]))
        for (y, _), z in zip(ys, t):
            rec("7 tenure", "Black - White", y, c, z)
    md += ["## 7. Returns to tenure with the employer", "",
           "Son-years with tenure with the present employer (waves 1984-2023), within-son (person fixed effects) "
           "regressions of the outcome (column header) on tenure / 10, its square and tenure x ln parental income "
           "(centred), quartic in age, year FE. Within-son tenure slopes mix the return to seniority with the selection "
           "of good matches (Altonji-Shakotko), so read them as descriptive wage-tenure profiles. The score column is "
           "occupational upgrading while staying with the employer.", ""]
    md += table([h for _, h in ys], panels)


def sec_disp(r, md):
    """Table 8: displacement and occupational progression (pre = income year t-2..t-1, post = t+2..t+3)."""
    v = r[r["lw"].notna() & r["os"].notna()][["pid", "year", "lw", "os", "res", "dd", "supm"]]
    base = r[r["year"].between(1970, 2019)][["pid", "year", "age", "C", "race", "lyp", "lyp_c", "fam68", "wpool",
                                              "disp_t", "black"]].copy()
    pre = None
    for k in (1, 2):
        x = v.assign(year=v["year"] + k).add_suffix("_pre").rename(columns={"pid_pre": "pid", "year_pre": "year"})
        pre = x if pre is None else pre.combine_first(x) if False else pd.concat([pre, x]).drop_duplicates(
            ["pid", "year"], keep="first")
    post = None
    for k in (2, 3):
        x = v.assign(year=v["year"] - k).add_suffix("_post").rename(columns={"pid_post": "pid", "year_post": "year"})
        post = x if post is None else pd.concat([post, x]).drop_duplicates(["pid", "year"], keep="first")
    d = base.merge(pre, on=["pid", "year"]).merge(post, on=["pid", "year"])
    dsets = set(zip(r.loc[r["disp_t"] == 1, "pid"], r.loc[r["disp_t"] == 1, "year"]))
    near = np.array([any((p, y + k) in dsets for k in (-3, -2, -1, 1, 2, 3)) for p, y in zip(d["pid"], d["year"])])
    d = d[(d["disp_t"] == 1) | ~near].copy()
    d["d_lw"], d["d_os"], d["d_res"] = d["lw_post"] - d["lw_pre"], d["os_post"] - d["os_pre"], d["res_post"] - d["res_pre"]
    d["down"] = ((d["dd_post"] != d["dd_pre"]) & (d["d_os"] <= -0.10)).astype(float)
    d["upx"] = ((d["dd_post"] != d["dd_pre"]) & (d["d_os"] >= 0.10)).astype(float)
    d["d_lyp"] = d["disp_t"] * d["lyp_c"]
    d["d_blk"] = d["disp_t"] * d["black"]
    ys = [("d_lw", "(1) change in ln wage"), ("d_os", "(2) change in occupation score"),
          ("d_res", "(3) change in residual"), ("upx", "(4) moved up >= 0.10"), ("down", "(5) moved down >= 0.10")]
    panels = []
    for g, gname in GROUPS3:
        for spec, xs in (("a", ("disp_t",)), ("b", ("disp_t", "d_lyp"))):
            info = run_cells(f"disp{spec}", d, tuple(y for y, _ in ys), xs + ("lyp",), ctrl_ageyr, ("C",),
                             bands=[(25, 52)], groups=(g,))
            rows = []
            for x, lab in zip(xs, ("displaced in t", "displaced x ln parental income")):
                t = [one(((f"disp{spec}", y, 25, 52, g), x)) for y, _ in ys]
                rows.append((lab, [cell(z) for z in t]))
                for (y, _), z in zip(ys, t):
                    rec(f"8 displacement {spec}", gname, y, x, z, n=info[(25, 52, g)][0],
                        mean=RES[((f"disp{spec}", y, 25, 52, g), x)]["mean"])
            if spec == "a":
                nd = int(d.loc[subset(d[d["age"].between(25, 52)], g)[0].index, "disp_t"].sum())
                rows.append(("Mean of outcome", [f"{RES[((f'dispa', y, 25, 52, g), 'disp_t')]['mean']:.3f}"
                                                 for y, _ in ys]))
                rows.append(("N son-years (displaced) / clusters",
                             [f"{info[(25, 52, g)][0]:,} ({nd:,}) / {info[(25, 52, g)][2]:,}"] * len(ys)))
            panels.append((f"{gname}" + (", with displacement x parental income" if spec == "b" else ""), rows))
    t = [comb([((("dispa", y, 25, 52, "B"), "disp_t"), 1.0), ((("dispa", y, 25, 52, "W"), "disp_t"), -1.0)])
         for y, _ in ys]
    panels.append(("Black - White", [("displaced in t", [cell(z) for z in t])]))
    for (y, _), z in zip(ys, t):
        rec("8 displacement a", "Black - White", y, "disp_t", z)
    md += ["## 8. Job loss and occupational progression", "",
           "Son-years t (male heads 25-52, 1970-2019) with a valid wage and occupation in an income year t-2..t-1 "
           "(latest) and t+2..t+3 (earliest). Displaced in t = main displacement (plant closure / layoff / firing; "
           "19.FatherDisplacement.py) dated t; non-displaced son-years with a displacement in t-3..t+3 are dropped. "
           "Outcome = post minus pre (column header). Controls: ln parental income, quartic in age, year FE; clusters "
           "1968 family. The occupation at the interview of t (spring) is the 'pre' occupation for a son-year t-1, so "
           "a displacement early in t can contaminate it (bias towards zero).", ""]
    md += table([h for _, h in ys], panels)
    return d


# ================================================================ NLSY79
def nlsy_panel(XWD, S):
    d = nlsy_extract()
    kids = pd.read_pickle(DATA / "nlsy79_kids.pkl")
    kids = kids[(kids["female"] == 0) & kids["lpinc_av"].notna()][["pid", "race", "birth_year", "wt79", "hhid",
                                                                    "lpinc_av"]]
    d = d[d["pid"].isin(kids["pid"])].reset_index(drop=True)
    rx = re.compile(r"EMPLOYERS_ALL_(OCC|HRLY_WAGE|CPSJOB|CURWK)_(\d{4})\.(\d\d)$")
    recs = {}
    for c in d.columns:
        m = rx.match(c)
        if m:
            recs.setdefault((int(m.group(2)), m.group(3)), {})[m.group(1)] = c
    rows = []
    for (y, jj), cs in recs.items():
        if not {"OCC", "HRLY_WAGE", "CPSJOB"} <= set(cs):
            continue
        x = pd.DataFrame({"pid": d["pid"], "round": y, "jj": int(jj), "occ": d[cs["OCC"]], "hw": d[cs["HRLY_WAGE"]],
                          "cps": d[cs["CPSJOB"]], "cur": d[cs["CURWK"]] if "CURWK" in cs else np.nan})
        rows.append(x[x["cps"] == 1])
    J = pd.concat(rows, ignore_index=True).sort_values(["pid", "round", "jj"]).drop_duplicates(["pid", "round"])
    J = J.merge(kids, on="pid")
    J["age"] = J["round"] - J["birth_year"]
    J = J[J["age"].between(25, 55)].copy()
    J["occ"] = J["occ"].where(J["occ"] > 0)
    J["scheme"] = np.where(J["round"] <= 2000, "1970", "2000")
    J["occ2"] = np.where((J["scheme"] == "2000") & (J["occ"] >= 1000), J["occ"] // 10, J["occ"])
    J = attach_scores(J, "occ2", "scheme", "round", XWD, S)
    w = J["hw"].where(J["hw"] > 0) / 100
    w = w * J["round"].map(lambda y: CPI[2000] / CPI[min(int(y), 2022)])
    J["lw"] = np.log(w.where(w.between(2, 200)))
    J["res"] = J["lw"] - J["os"]
    J["C"] = J["age"] - 40
    J["fam68"] = J["hhid"]
    J["lyp"] = J["lpinc_av"]
    J["wpool"] = J["wt79"].where(J["wt79"] > 0)
    J = J.sort_values(["pid", "round"])
    p = J.groupby("pid").shift(1)
    ok = (J["round"] - p["round"]).between(1, 2)
    same = ok & (J["jj"] == p["jj"])
    J["same_emp"] = same.astype(float).where(ok)
    dos = (J["os"] - p["os"]).where(ok)
    J["up_within"] = (same & (J["dd"] != p["dd"]) & (dos > 0)).astype(float).where(ok & J["dd"].notna() &
                                                                                 p["dd"].notna())
    J["up_any"] = ((J["dd"] != p["dd"]) & (dos > 0)).astype(float).where(ok & J["dd"].notna() & p["dd"].notna())
    # promotions since the last interview
    pr = []
    for c in d.columns:
        m = re.match(r"(QES-PROMO3[89])\.0(\d)\|(\d{4})$", c) or re.match(r"(ES-16)_(\d)\|(\d{4})$", c)
        if m:
            pr.append((m.group(1), int(m.group(3)), c))
    P = []
    for y in sorted({y for _, y, _ in pr}):
        c38 = [c for q, yy, c in pr if yy == y and q == "QES-PROMO38"]
        c39 = [c for q, yy, c in pr if yy == y and q == "QES-PROMO39"]
        c16 = [c for q, yy, c in pr if yy == y and q == "ES-16"]
        x = pd.DataFrame({"pid": d["pid"], "round": y})
        if c38:
            a38 = d[c38].where(d[c38] >= 0)
            a39 = d[c39].where(d[c39] > 0) if c39 else pd.DataFrame(index=d.index)
            x["promo"] = (a39 == 1).any(axis=1).astype(float).where(a38.notna().any(axis=1))
            x["poschg"] = (a38 == 1).any(axis=1).astype(float).where(a38.notna().any(axis=1))
        if c16:
            a16 = d[c16].where(d[c16] >= 0)
            x["promo"] = (a16 == 1).any(axis=1).astype(float).where(a16.notna().any(axis=1))
        P.append(x)
    P = pd.concat(P, ignore_index=True)
    J = J.merge(P, on=["pid", "round"], how="left")
    return J


def sec_nlsy(J, md):
    hdr = ["(1) ln wage", "(2) occupation score", "(3) within-occupation residual", "(4) share between = (2)/(1)"]
    ctrl = lambda z: ctrl_ageyr(z, "birth_year")
    info = run_cells("nl_dec", J, ("lw", "os", "res"), ("lyp",), ctrl, ("C",), bands=[(25, 34), (35, 44), (45, 55)],
                     cl="fam68")
    panels = []
    for g, gname in GROUPS3 + [("BW", "Black - White")]:
        rows = []
        for lo, hi in ((25, 34), (35, 44), (45, 55)):
            def L(y):
                if g == "BW":
                    return [((("nl_dec", y, lo, hi, "B"), "x"), 1.0), ((("nl_dec", y, lo, hi, "W"), "x"), -1.0)]
                return [((("nl_dec", y, lo, hi, g), "x"), 1.0)]
            t = [comb(L("lw")), comb(L("os")), comb(L("res")), ratio(L("os"), L("lw"))]
            rows.append((f"ln parental income, ages {lo}-{hi}", [cell(x) for x in t]))
            for y, x in zip(["lw", "os", "res", "share_between"], t):
                rec("N1 NLSY79 decomposition", gname, y, f"lyp, {lo}-{hi}", x,
                    n=info.get((lo, hi, g), (np.nan,))[0])
        if g != "BW":
            rows.append(("N person-rounds / clusters", [" ; ".join(f"{lo}-{hi}: {info[(lo, hi, g)][0]:,}/"
                                                                   f"{info[(lo, hi, g)][2]:,}"
                                                                   for lo, hi in ((25, 34), (35, 44), (45, 55)))]
                         + [""] * 3))
        else:
            for (a0, a1) in ((25, 34),):
                def D(y):
                    return ([((("nl_dec", y, 45, 55, gg), "x"), s) for gg, s in (("B", 1.0), ("W", -1.0))] +
                            [((("nl_dec", y, a0, a1, gg), "x"), -s) for gg, s in (("B", 1.0), ("W", -1.0))])
                t = [comb(D("lw")), comb(D("os")), comb(D("res")), ratio(D("os"), D("lw"))]
                rows.append(("Change of the gap (45-55) - (25-34)", [cell(x) for x in t]))
                for y, x in zip(["lw", "os", "res", "share_between"], t):
                    rec("N1 NLSY79 decomposition", gname, y, "gap change (45-55)-(25-34)", x)
        panels.append((gname, rows))
    md += ["## 9. NLSY79 check", "",
           "### 9a. Wage persistence by age: between vs within occupation", "",
           "Men of the NLSY79 (White and Black cross-sectional + supplemental samples) living with a parent in 1979; "
           "regressor = ln mean parental family income 1979-81 (2.NLSY79.py); outcome = hourly wage of the CPS (main) "
           "job at each interview and its occupation score (occ1990dd, the same CPS MORG score); controls: quartic in "
           "age, birth-year FE; clusters = 1979 household; pooled weighted by the 1979 sampling weight.", ""]
    md += table(hdr, panels)
    ys = [("promo", "(1) promotion since last interview"), ("poschg", "(2) position change since last interview"),
          ("up_within", "(3) higher-paying occupation, same employer"), ("up_any", "(4) higher-paying occupation"),
          ("same_emp", "(5) same employer as last interview")]
    info = {y: run_cells("nl_pro", J, (y,), ("lyp",), lambda z: ctrl_ageyr(z, "round"), ("C",),
                         bands=[(25, 34), (35, 55)]) for y, _ in ys}
    panels = []
    for g, gname in GROUPS3 + [("BW", "Black - White")]:
        rows = []
        for lo, hi in ((25, 34), (35, 55)):
            t = []
            for y, _ in ys:
                if g == "BW":
                    k1, k2 = (("nl_pro", y, lo, hi, "B"), "x"), (("nl_pro", y, lo, hi, "W"), "x")
                    t.append(comb([(k1, 1.0), (k2, -1.0)]) if k1 in RES and k2 in RES else (np.nan,) * 3)
                else:
                    k = (("nl_pro", y, lo, hi, g), "x")
                    t.append(one(k) if k in RES else (np.nan,) * 3)
            rows.append((f"ln parental income, ages {lo}-{hi}", [cell(x) for x in t]))
            for (y, _), x in zip(ys, t):
                rec("N2 NLSY79 promotion", gname, y, f"lyp, {lo}-{hi}", x,
                    n=info[y].get((lo, hi, g), (np.nan,))[0])
            if g != "BW":
                rows.append((f"Mean, {lo}-{hi}", [f"{RES[(('nl_pro', y, lo, hi, g), 'x')]['mean']:.3f}"
                                                  if (("nl_pro", y, lo, hi, g), "x") in RES else "" for y, _ in ys]))
                rows.append((f"N person-rounds / clusters, {lo}-{hi}",
                             [f"{info[y][(lo, hi, g)][0]:,} / {info[y][(lo, hi, g)][2]:,}" if (lo, hi, g) in info[y]
                              else "" for y, _ in ys]))
        panels.append((gname, rows))
    md += ["### 9b. Promotions and within-employer occupational upgrading", "",
           "Person-round linear probability models, controls: quartic in age, round FE; clusters = 1979 household. "
           "(1) any promotion since the last interview at jobs #01-05: 'ES-16' rounds 1988-1990 (ages 23-33) and "
           "'QES-PROMO39' = promotion, rounds 1996-2016 (ages 31-59); (2) any position change ('QES-PROMO38', "
           "1996-2016); (3)-(5) CPS job of consecutive interviews (1-2 years apart): same roster employer JJ and a "
           "different occ1990dd occupation with a higher score / any employer / same employer.", ""]
    md += table([h for _, h in ys], panels)
    # Hegde-style test in NLSY79 promotions
    d = J.copy()
    d["black"] = (d["race"] == "Black").astype(float)
    d["lyp_c"] = d["lyp"] - d["lyp"].mean()
    d["old"] = (d["age"] >= 35).astype(float)
    d["lyp_old"], d["blk_old"] = d["lyp_c"] * d["old"], d["black"] * d["old"]
    d["lyp_blk"], d["lyp_blk_old"] = d["lyp_c"] * d["black"], d["lyp_c"] * d["black"] * d["old"]
    XS = ("lyp_c", "lyp_old", "black", "blk_old", "lyp_blk", "lyp_blk_old")
    d["age"] = 40
    yy = [("promo", "promotion"), ("up_within", "higher-paying occupation, same employer"), ("lw", "ln wage"),
          ("os", "occupation score")]
    inf = {y: run_cells("nl_heg", d, (y,), XS, lambda z: np.column_stack([ctrl_ageyr(z, "round"),
                                                                          z["old"].to_numpy(float)]),
                        ("C",), bands=[(40, 40)], groups=("all",)) for y, _ in yy}
    rows = []
    for x, lab in zip(XS, ("ln parental income (centred)", "x age 35-55", "Black", "Black x age 35-55",
                           "ln parental income x Black", "ln parental income x Black x age 35-55")):
        t = [one((("nl_heg", y, 40, 40, "all"), x)) for y, _ in yy]
        rows.append((lab, [cell(z) for z in t]))
        for (y, _), z in zip(yy, t):
            rec("N3 NLSY79 Hegde test", "Black + White", y, x, z, n=inf[y][(40, 40, "all")][0])
    rows.append(("N person-rounds / clusters", [f"{inf[y][(40, 40, 'all')][0]:,} / {inf[y][(40, 40, 'all')][2]:,}"
                                                 for y, _ in yy]))
    md += ["### 9c. NLSY79: Black x parental income x after-35 interactions", "",
           "As Section 6 (unweighted, controls: quartic in age, round FE, age 35-55 dummy). Promotions are observed "
           "at 23-33 (1988-90) and 31-59 (1996-2016), so the age split for (1) also separates survey eras.", ""]
    md += table([h for _, h in yy], [("Black + White men", rows)])


# ================================================================ figure
def figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ink, muted, grid, bg = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    col = {"lw": "#52514e", "os": "#2a78d6", "res": "#eb6834"}
    lab = {"lw": "ln wage (total)", "os": "Between occupations (score)", "res": "Within occupation (residual)"}
    fig, ax = plt.subplots(1, 3, figsize=(13, 4.6), sharey=True)
    fig.patch.set_facecolor(bg)
    bands = [(25, 34), (35, 44), (45, 55)]
    x = np.arange(3)
    for a_, (g, gname) in zip(ax, GROUPS3):
        for j, y in enumerate(("lw", "os", "res")):
            b, s = zip(*[comb([(((("dec", "fixed 1992-2002 score"), y, lo, hi, g), "x"), 1.0)])[:2]
                         for lo, hi in bands])
            xx = x + (j - 1) * 0.12
            a_.errorbar(xx, b, yerr=1.96 * np.array(s), fmt="o-", ms=8, lw=2, color=col[y], ecolor=col[y],
                        elinewidth=1.5, capsize=0, label=lab[y], mec=bg, mew=1.5)
        a_.axhline(0, color=muted, lw=1)
        a_.set_xticks(x, [f"{lo}-{hi}" for lo, hi in bands], color=ink)
        a_.set_title(f"{gname} sons", color=ink, loc="left", fontsize=12)
        a_.set_xlabel("Son's age band", color=muted)
        a_.set_facecolor(bg)
        a_.grid(axis="y", color=grid, lw=0.8)
        a_.set_axisbelow(True)
        for sp in ("top", "right", "left"):
            a_.spines[sp].set_visible(False)
        a_.spines["bottom"].set_color(muted)
        a_.tick_params(colors=muted, length=0)
    ax[0].set_ylabel("Coefficient on ln parental income (95% CI)", color=muted)
    ax[0].legend(frameon=False, loc="upper left", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / "career_wage_growth.png", dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)


# ================================================================ main
def main():
    global SCORES, CLIDX, NCL
    OUT.mkdir(exist_ok=True)
    XWD = crosswalks()
    cells = morg_cells(XWD)
    S = SCORES = scores(cells)
    r = son_panel(XWD, S)
    J = nlsy_panel(XWD, S)
    CLIDX = pd.Index(np.unique(np.concatenate([r["fam68"].dropna().unique().astype(float),
                                               J["fam68"].dropna().unique().astype(float) + 1e7])))
    J["fam68"] = J["fam68"].astype(float) + 1e7
    r["fam68"] = r["fam68"].astype(float)
    NCL = len(CLIDX)
    md = ["# Career wage growth and the IGE: occupational upgrading / promotion vs within-occupation growth", "",
          "Built by `27.CareerWageGrowth.py` (2026-10-17); definitions in its docstring. PSID SRC + SEO sons (24's "
          "frame: 6.IGEMain parents, male heads 25-55, valid wage years), race of the parental head at 16. Every "
          "coefficient: estimate (s.e.; p), *** p<0.01, ** p<0.05, * p<0.1, s.e. clustered by 1968 family (PSID) / "
          "1979 household (NLSY79). **Descriptive accounting: sons select into occupations and employers; nothing "
          "here is a causal effect of parental income or race.**", "", "SUMMARY_PLACEHOLDER", ""]
    # ---- section 0: harmonisation and samples
    v = r[r["valid"] & r["age"].between(25, 55)]
    cov = v.groupby("scheme").apply(lambda z: pd.Series({"son-years": len(z), "with code": z["occ_raw"].notna().sum(),
                                                          "mapped": z["dd"].notna().sum()}))
    ncodes = len(S["fixed"].dropna())
    nb = S["nbase"]
    sd_os = float(v["os"].std())
    vb = v.dropna(subset=["os"])
    shares = {g: float(np.var(vb.loc[vb["race"] == g, "os"]) / np.var(vb.loc[vb["race"] == g, "lw"]))
              for g in ("Black", "White")}
    supm = v.groupby("race")["supm"].mean()
    md += ["## 0. Occupation harmonisation, the occupational wage score and samples", "",
           f"Common scheme: Dorn's occ1990dd ({ncodes} occupations with a score). CPS MORG men 25-64: "
           f"{int(cells['n'].sum()):,} worker-records 1979-2019 with a wage and a mapped occupation; base period "
           f"{BASE[0]}-{BASE[1]} cells: median {int(nb.median())} men per occupation. Score = mean ln wage of the "
           f"occupation relative to all men of the year; s.d. of the fixed score across son-years {sd_os:.3f}. "
           f"Var(score) / Var(ln wage) among son-years: Black {shares['Black']:.2f}, White {shares['White']:.2f}. "
           f"Share of son-years in a supervisory / managerial occupation: Black {supm.get('Black', np.nan):.3f}, "
           f"White {supm.get('White', np.nan):.3f}.", "",
           "| PSID code scheme (waves) | son-years with valid wage | with an occupation code | mapped to occ1990dd |",
           "|---|---|---|---|"]
    for sch, row in cov.iterrows():
        md.append(f"| {sch} ({'1968-2001' if sch == '1970' else '2003-2015' if sch == '2000' else '2017-2023'}) | "
                  f"{int(row['son-years']):,} | {int(row['with code']):,} | {int(row['mapped']):,} |")
    nsons = v.groupby("race")["pid"].nunique()
    md += ["", f"Sons with a valid wage year at 25-55: Black {nsons.get('Black', 0):,}, White {nsons.get('White', 0):,}"
           f" (son-years Black {int((v['race'] == 'Black').sum()):,}, White {int((v['race'] == 'White').sum()):,}). "
           f"Promotion items: reported promotion waves 1976-1987 ({int(r['promo_rep'].notna().sum()):,} son-years), "
           f"within-employer position change 1984-2001 ({int(r['pos_ch'].notna().sum()):,}), tenure 1984-2023 "
           f"({int(r['tenure'].notna().sum()):,}). NLSY79 men: {J['pid'].nunique():,} with a CPS-job wage at 25-55 "
           f"({len(J):,} person-rounds).", "",
           "PSID extra items used (wave: variables): tenure months " + ", ".join(f"{w} {v}" for w, v in TEN_MO.items())
           + "; tenure years / months / weeks " + ", ".join(f"{w} {v}+2" for w, v in TEN_YMW.items())
           + "; position (B24 B25 B26 B30 B31 B27 B32 B29 B34) " + "; ".join(f"{w} {v}" for w, v in POS.items())
           + "; months in present position " + ", ".join(f"{w} {v}" for w, v in POS_MO.items())
           + "; why previous job / position ended (E branch, code 6 = promotion) "
           + ", ".join(f"{w} {v}" for w, v in WHY_E.items()) + ".", ""]
    print("decomposition ...", flush=True)
    sec_decomp(r, md)
    print("career ...", flush=True)
    sec_career(r, md)
    print("growth ...", flush=True)
    sec_growth(r, md)
    print("promotion ...", flush=True)
    sec_promo(r, md)
    print("hegde ...", flush=True)
    sec_hegde(r, md)
    print("tenure ...", flush=True)
    sec_tenure(r, md)
    print("displacement ...", flush=True)
    sec_disp(r, md)
    print("nlsy ...", flush=True)
    sec_nlsy(J, md)
    figure()
    pd.DataFrame(CSV).to_csv(OUT / "career_wage_growth.csv", index=False)
    summ = summary()
    md = [summ if x == "SUMMARY_PLACEHOLDER" else x for x in md]
    (OUT / "career_wage_growth.md").write_text("\n".join(md), encoding="utf-8")
    print(summ)


def summary():
    F = "fixed 1992-2002 score"
    T = "time-varying score"
    Gp = "11 major groups"

    def dk(y, lo, hi, g, lab=F):
        return (("dec", lab), y, lo, hi, g), "x"

    def c(terms):
        return cell(comb(terms))

    def lvl(y, lo, hi, g, lab=F):
        return c([(dk(y, lo, hi, g, lab), 1.0)])

    def chg(y, g, lab=F, b=(35, 55), a=(25, 34)):
        gs = [("B", 1.0), ("W", -1.0)] if g == "BW" else [(g, 1.0)]
        return ([(dk(y, *b, gg, lab), sg) for gg, sg in gs] + [(dk(y, *a, gg, lab), -sg) for gg, sg in gs])

    def gap(y, lo, hi, lab=F):
        return [(dk(y, lo, hi, "B", lab), 1.0), (dk(y, lo, hi, "W", lab), -1.0)]

    def sh(num, den):
        x = cell(ratio(num, den))
        return x if x else "n.a. (denominator ~ 0)"

    def k(tag, y, lo, hi, g, x="x"):
        return ((tag, y, lo, hi, g), x)

    def one_(key):
        return cell(one(key)) if key in RES else "n.a."

    def bw(tag, y, lo, hi, x="x"):
        a, b_ = k(tag, y, lo, hi, "B", x), k(tag, y, lo, hi, "W", x)
        return c([(a, 1.0), (b_, -1.0)]) if a in RES and b_ in RES else "n.a."

    def nlg(y):
        return c([(k("nl_dec", y, 45, 55, "B"), 1), (k("nl_dec", y, 45, 55, "W"), -1),
                  (k("nl_dec", y, 25, 34, "B"), -1), (k("nl_dec", y, 25, 34, "W"), 1)])
    L = ["## Summary", ""]
    L.append("- **Measurement.** All PSID (1970 / 2000 / 2010 Census) and CPS MORG (1970 / 1980 / 1990 / 2000 / 2010) "
             "occupation codes are mapped to Dorn's occ1990dd (330 occupations). Occupational wage score = mean ln "
             "hourly wage of men 25-64 in the occupation relative to all men (CPS MORG, base 1992-2002). The score "
             "accounts for about a quarter of the variance of sons' ln wages (Section 0).")
    L.append("- **General pattern (pooled, weighted).** The son's ln wage on ln parental income rises from "
             f"{lvl('lw', 25, 34, 'P')} at 25-34 to {lvl('lw', 35, 55, 'P')} at 35-55. The between-occupation part "
             f"(score) is {lvl('os', 25, 34, 'P')} -> {lvl('os', 35, 55, 'P')}; the within-occupation part "
             f"{lvl('res', 25, 34, 'P')} -> {lvl('res', 35, 55, 'P')}. Between-occupation share of the level: "
             f"{sh([(dk('os', 25, 34, 'P'), 1.0)], [(dk('lw', 25, 34, 'P'), 1.0)])} at 25-34, "
             f"{sh([(dk('os', 35, 55, 'P'), 1.0)], [(dk('lw', 35, 55, 'P'), 1.0)])} at 35-55. Of the rise of the "
             f"gradient after 35 ({c(chg('lw', 'P'))}), occupational sorting accounts for {c(chg('os', 'P'))} (share "
             f"{sh(chg('os', 'P'), chg('lw', 'P'))}; time-varying score {c(chg('os_t', 'P', T))}). Within sons "
             f"(Section 2), wage growth from 25-34 to 35-55 rises with parental income by "
             f"{one_(k('career', 'd_lw', 40, 40, 'P'))}, of which the occupation score "
             f"{one_(k('career', 'd_os', 40, 40, 'P'))}. **Background buys a better occupation early; career wage "
             "growth with background is growth within the occupation.**")
    L.append("- **Race.** At 25-34 the Black-White difference in the wage gradient "
             f"({c(gap('lw', 25, 34))}) is almost all between occupations ({c(gap('os', 25, 34))}; within "
             f"{c(gap('res', 25, 34))}). The divergence after 35 - the change of the Black-White gap from 25-34 to "
             f"35-55, {c(chg('lw', 'BW'))} (to 45-55: {c(chg('lw', 'BW', b=(45, 55)))}) - is between occupations "
             f"{c(chg('os', 'BW'))} (share {sh(chg('os', 'BW'), chg('lw', 'BW'))}; time-varying score "
             f"{c(chg('os_t', 'BW', T))}, share {sh(chg('os_t', 'BW', T), chg('lw', 'BW'))}; 11 major groups "
             f"{c(chg('os_g', 'BW', Gp))}) and within occupations {c(chg('res', 'BW'))}. Black sons' gradient is flat "
             f"in both parts ({c(chg('os', 'B'))} and {c(chg('res', 'B'))}); White sons' rises within occupations "
             f"({c(chg('res', 'W'))}) with a small occupational component ({c(chg('os', 'W'))}). Within-son career "
             f"growth on parental income: Black {one_(k('career', 'd_lw', 40, 40, 'B'))}, White "
             f"{one_(k('career', 'd_lw', 40, 40, 'W'))}; the score part {one_(k('career', 'd_os', 40, 40, 'B'))} / "
             f"{one_(k('career', 'd_os', 40, 40, 'W'))}.")
    L.append("- **When and where the within-occupation growth happens (Sections 3, 7).** Annual wage growth at 25-34 "
             f"rises with parental income for White sons ({one_(k('growth', 'g_lw_t', 25, 34, 'W'))}), almost all of "
             f"it residual growth with the same employer ({one_(k('growth', 'g_res_s', 25, 34, 'W'))}); not for Black "
             f"sons ({one_(k('growth', 'g_lw_t', 25, 34, 'B'))}; difference {bw('growth', 'g_lw_t', 25, 34)}). The "
             "level gap that is visible after 35 is built by within-job wage growth in the late twenties and early "
             "thirties; after 35 the growth gradients are small "
             f"(White {one_(k('growth', 'g_lw_t', 35, 55, 'W'))}, Black {one_(k('growth', 'g_lw_t', 35, 55, 'B'))}). "
             "Wage-tenure profiles (person FE) steepen with parental income for White sons (tenure x ln parental "
             f"income, residual {one_((('ten', 'res', 'W'), 'ten_lyp'))}) but not for Black sons "
             f"({one_((('ten', 'res', 'B'), 'ten_lyp'))}).")
    L.append("- **Promotion dynamics (Sections 4-6).** Coded moves to higher-paying occupations fall with parental "
             f"income (pooled 25-34 {one_(k('promo', 'up', 25, 34, 'P'))}; more churning at the bottom). Entry into "
             "supervisory / managerial occupations rises with parental income at 25-34 and 35-55 for White sons "
             f"({one_(k('promo', 'sup_in', 25, 34, 'W'))}, {one_(k('promo', 'sup_in', 35, 55, 'W'))}); for Black sons "
             f"only at 25-34 ({one_(k('promo', 'sup_in', 25, 34, 'B'))}) and not after 35 "
             f"({one_(k('promo', 'sup_in', 35, 55, 'B'))}; Black - White {bw('promo', 'sup_in', 35, 55)}, at 25-34 "
             f"{bw('promo', 'sup_in', 25, 34)}). This is the closest Hegde-type pattern in the data: Black sons from "
             "richer families are not more likely to move into supervisory / managerial jobs after 35 - but the "
             "after-35 change relative to 25-34 (the triple interaction below) is not significant, and holding the "
             "position at 28-32 fixed (Section 5) the gradients are White "
             f"{one_(k('promo_c', 'sup_in', 35, 55, 'W', 'lyp'))}, Black {one_(k('promo_c', 'sup_in', 35, 55, 'B', 'lyp'))}."
             " Self-reported position "
             "changes with the same employer "
             f"(1984-2001) rise with parental income after 35 for both (Black {one_(k('promo', 'pos_ch', 35, 55, 'B'))}, "
             f"White {one_(k('promo', 'pos_ch', 35, 55, 'W'))}), with a wage gain Black "
             f"{one_(k('promo', 'pos_up', 35, 55, 'B'))}, White {one_(k('promo', 'pos_up', 35, 55, 'W'))}: no Black "
             "deficit in within-employer position changes. Triple interaction ln parental income x Black x 35-55 "
             f"(Section 6A): supervisory entry {one_(k('hegdeA', 'sup_in', 40, 40, 'all', 'lyp_blk_old'))}, "
             f"occupation score {one_(k('hegdeA', 'os', 40, 40, 'all', 'lyp_blk_old'))}, within-occupation residual "
             f"{one_(k('hegdeA', 'res', 40, 40, 'all', 'lyp_blk_old'))}, ln wage "
             f"{one_(k('hegdeA', 'lw', 40, 40, 'all', 'lyp_blk_old'))}.")
    L.append("- **Job loss (Section 8).** Displacement lowers ln wage 2-3 years later by "
             f"{one_(k('dispa', 'd_lw', 25, 52, 'P', 'disp_t'))} (pooled), of which the occupation score "
             f"{one_(k('dispa', 'd_os', 25, 52, 'P', 'disp_t'))}; Black {one_(k('dispa', 'd_lw', 25, 52, 'B', 'disp_t'))} "
             f"(score {one_(k('dispa', 'd_os', 25, 52, 'B', 'disp_t'))}), White "
             f"{one_(k('dispa', 'd_lw', 25, 52, 'W', 'disp_t'))} (score {one_(k('dispa', 'd_os', 25, 52, 'W', 'disp_t'))}). "
             "Lost occupational progression is a minor part of the displacement wage loss and is not larger for Black "
             f"sons (B - W difference in the score loss {bw('dispa', 'd_os', 25, 52, 'disp_t')}); job loss raises "
             "occupational churning in both directions, more for Black sons.")
    L.append("- **NLSY79 check (Section 9).** Same pattern: pooled gradient 25-34 / 45-55 "
             f"{one_(k('nl_dec', 'lw', 25, 34, 'P'))} / {one_(k('nl_dec', 'lw', 45, 55, 'P'))}, the score part "
             f"{one_(k('nl_dec', 'os', 25, 34, 'P'))} / {one_(k('nl_dec', 'os', 45, 55, 'P'))}, the residual "
             f"{one_(k('nl_dec', 'res', 25, 34, 'P'))} / {one_(k('nl_dec', 'res', 45, 55, 'P'))}. Change of the "
             f"Black-White gap (45-55) - (25-34): ln wage {nlg('lw')}, score {nlg('os')}, residual {nlg('res')}. "
             "Reported promotions (QES-PROMO39, ages 35-55) on parental income: Black "
             f"{one_(k('nl_pro', 'promo', 35, 55, 'B'))}, White {one_(k('nl_pro', 'promo', 35, 55, 'W'))} "
             f"(difference {bw('nl_pro', 'promo', 35, 55)}).")
    L += ["", "**Assessment.** Occupational upgrading / promotion is not where the post-35 divergence comes from. In "
          "the pooled data background is transmitted into occupations early (half to three fifths of the wage "
          "gradient at 25-34) and that occupational component barely grows with age; the rise of wage persistence "
          "with age is growth of wages within occupations, and in the PSID most of it accrues while staying with the "
          "same employer in the late twenties and early thirties. For the race gap the same holds: Black sons' "
          "occupational disadvantage relative to their parents' income is already in place at 25-34 and does not "
          "widen much, so the between-occupation share of the divergence is small (see the shares above); the bulk is "
          "a within-occupation (largely within-job) wage-growth gradient that White sons from richer families have and "
          "Black sons do not. The closest analogue to Hegde, Ljungqvist and Raj (2026) is the flat parental-income "
          "gradient of Black sons' entry into supervisory / managerial occupations after 35 - present, but not "
          "significantly different from the gap at 25-34 and a small part of the wage gap; self-reported "
          "within-employer position changes (PSID) and reported promotions (NLSY79) show no significant Black deficit "
          "in their parental-income gradient. For the "
          "companion structural model this points to differences in human capital accumulation on the job (or in its "
          "pay-off) by background and race rather than to occupational mobility. Caveats: descriptive; the score is an "
          "occupation-level price, so 'within occupation' includes unmeasured job titles / ranks, employer pay premia "
          "and returns to skill within the occupation (a promotion that does not change the Census code counts as "
          "within-occupation); PSID occupation codes are noisy (coded independently each wave after 1980), which "
          "inflates measured occupation changes but not the level decomposition; wage = annual earnings / hours "
          "carries division bias; samples follow 24."]
    return "\n".join(L)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        XWD = crosswalks()
        print({k: len(v) for k, v in XWD.items()})
        morg_cells(XWD)
        psid_items()
        if len(sys.argv) > 2:
            nlsy_extract()
    else:
        main()
