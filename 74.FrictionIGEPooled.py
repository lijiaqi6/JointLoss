r"""Search friction of the father, the mother and the son in the IGE, pooled sons (PI question, 2026-10-19).

THE QUESTION (PI): "Even without race focus, does search friction faced by the father, the mother or the son contribute
to the IGE literature meaningfully?" This script is the DATA side: on pooled Black and White sons (PSID weights), how
much of the IGE of the son's family income, earnings, hourly wage and hours / employment runs through the measured
search friction of each of the three people, by the son's age, and how that compares with recognised mediators in the
same rows. Race is a secondary check. 73.SharedFriction.py measured the father x son part by race (unweighted); this
script adds the mother, pools the races with weights, and benchmarks the shares.

DATA (read only; nothing person-level is written to tracked files; caches under data/, git-ignored)
  Son panel: 73.SharedFriction.py's load_panel() (= 36.SameEmployerGrowthChecks.py's psid_build(), 24's child-year
  frame; cache data/shared_friction_sonpanel.pkl). Sons = male heads 25-55, Black or White parental household (race of
  the parental head at 16), every son-year.
    x = lyp      ln parental family income, mean over the son's wave-ages 13-19 (6.IGEMain.py).
    OUTCOMES (y):
    lfam         ln of the son's family income (2000 $, within 6.IGEMain.py's bounds), every son-year with it (zero-hours
                 years included).
    ly, lw, lh   ln annual earnings, ln hourly wage, ln annual hours of a VALID year (24's bounds), same rows, so
                 ln y = ln w + ln h exactly and every component below adds up: earnings = wage + hours.
    emp          1 if annual hours > 0 (every son-year with hours measured): the extensive margin.
    ly0          ln earnings with zero-hours years at the 10th percentile of ln earnings of the son's race x five-year
                 band (73's rule); rows = valid or zero-hours years.
    Weight: wt = the son's PSID individual weight in the wave (corrects the SEO over-sample; Black = 12.9% of the weighted
    son-years); son-years with wt = 0 (13) are dropped everywhere.
  FRICTION FLAGS of a person-year t (24.IGEDecomposition.py rules; t = income year = wave - 1):
    displaced    main displacement (plant closure / layoff / firing) dated t or t-1.
    unemployed   hours unemployed > 0, or unemployed at any time in t, or laid off / looking for work at the interview
                 that follows t (t >= 1978).
    zero hours   annual hours = 0.
  SON'S FRICTION (S): sb_disp, sb_unemp, sb_zero = his shares of son-years in the current five-year band displaced /
    unemployed / with zero hours (73's band shares; all his years in the band). For emp the zero-hours share is left out
    (it is the band mean of the outcome itself). Variant: his career shares 25-55 (s_sh_*).
  FATHER'S FRICTION (F): f_sh_disp, f_sh_unemp, f_sh_zero = the father's shares of the childhood-window years (income
    years when the son is 12-18) displaced / unemployed / zero hours; father = male head of the son's family unit at 16
    (24's person_measures). Sons without a father in the window: shares set to 0 and nofa = 1 (see D).
  MOTHER'S FRICTION (M): the mother = the woman of the son's family unit at each window wave (the wife / partner of the
    head, or the female head), built here from 24's head-and-wife panel (data/ige_decomposition_panel.pkl) and, for wives,
    the family-file items read below (cache data/friction_ige_wife_items.pkl):
    m_sh_zero    her share of window years with zero annual hours (wife: WH; female head: HH; every wave).
    m_sh_unemp   her share of window years with unemployment, over the years in which it is measured:
                 wives      hours unemployed > 0 ('HRS WIFE UNEMP' / 'WF UNEMP HRS yy', waves 1975-1993: V3833 V4727 V5252
                            V5751 V6356 V6954 V7548 V8246 V8848 V10139 V11265 V12664 V13816 V14872 V16372 V17781 V19081
                            V20381 V21674), or 'WTR UNEMPLOYED (WF-E)' = 1 (D72, waves 1994-2001: ER2682 ER5681 ER7777
                            ER10681 ER13842 ER17923), or 'DE8 WTR UNEMPLOYED (WF / SP)' = 1 (waves 2003-2023: ER21567
                            ER25564 ER36569 ER42590 ER47908 ER53614 ER60629 ER66644 ER72646 ER78722 ER82714); 0 / 5 = no
                            (0 = inapplicable, as 24 treats the head's item), or laid off / looking at the following
                            interview (individual file, waves 1979+).
                 female heads  the head's items of 24 (hours unemployed to 1993, B72 / BC8 from 1994) and the interview
                            status.
                 Not measured for wives in waves 1968-1974 (no item); a son whose mother has no measured window year
                 gets m_sh_unemp = 0 and m_un_na = 1 (see D).
    m_sh_disp    (variant only) her share of window years with a main job end (closure or layoff / firing, t or t-1),
                 wives in waves 1984+ (data/correlated_shocks_wife_disp.pkl of 23.CorrelatedShocks.py: the PSID asks
                 wives why a job ended only from 1984); not measured for female heads.
    m_hu_sh, f_hu_sh  (variant only) hours unemployed / (hours worked + hours unemployed) summed over the window years
                 with the hours-unemployed item (heads: waves <= 1993; wives: waves 1975-1993): the intensity of friction.
    Sons without a woman in the window: mother's shares 0 and nomo = 1.
  FAMILY STRUCTURE (D, not friction): nofa, nomo, m_un_na. It is its own group in every decomposition, so friction is
    measured among the parents who are there and the parents' absence is not counted as friction.
  BENCHMARK MEDIATORS (same rows): son's schooling (educ, years; 0 and a flag if missing); parents' schooling (f_educ of
    the father, m_educ of the mother; 0 and a flag if the parent is present but has none); son's occupation (occ11 of
    36: 11 groups, dummies, missing as its own group); son's industry (igrp of 36: 33 groups, dummies, missing group).
DESIGNS (each five-year band of the son's age is its own regression, with single-age dummies; '25-55' = all son-years
  in one regression with single-age dummies; opening = 45-49 minus 25-29; weighted least squares with wt)
  1. GELBACH (2016) DECOMPOSITION, exact on one sample. With mediators m_k grouped into G = {F, M, S, D, ...}:
       base  y = b0 x + ages;   full  y = b x + sum_k g_k m_k + ages;   aux  m_k = d_k x + ages
       b0 = b + sum_G sum_{k in G} g_k d_k  exactly.
     Contribution of group G = sum_{k in G} g_k d_k (the part of the IGE accounted for by that person's friction); share =
     contribution / b0. Elements (g_k d_k) are reported for every friction measure. The son's contribution splits further
     (73's chain, with both parents): S = a x + C'(F, M) + E'D + ages, so g_S'd_S = g_S'a (his own friction gradient in
     parental income) + g_S'C'd_(F,M) (SHARED: his friction that follows his parents' friction x the parental income their
     friction costs x what his friction costs him) + g_S'E'd_D (through family structure).
     The parental groups are COMPONENTS of parental income rather than mediators that follow it: d_F, d_M < 0 because
     friction lowers parental income; their contribution is the part of the IGE that comes from parental-income
     differences that are friction differences and that relate to the son's outcome at equal son's friction.
  2. Wage vs hours: on valid rows ly = lw + lh, so every contribution to the earnings IGE = its wage part + its hours part.
  3. Age profile: contributions and shares by band; opening of each; the 'life-cycle' ratio IGE(25-29)/IGE(45-49) with and
     without the son's friction contribution; variant with the son's career shares.
  4. Mother: her group and elements; her group alone vs with the father; two-parent sons; her displacement (sons born
     1966+); friction intensity (hours unemployed). Added-worker panel: window unit-years with the father and a woman
     present, her annual hours / zero hours / unemployment on the father's displacement and unemployment flags of the same
     year, woman FE + year FE (unweighted, s.e. clustered by 1968 family). One row per son: her window shares on the
     father's.
  5. Transmission vs noise: partial ages and D out of x, F, M; P = projection of x~ on (F~, M~) (the friction-predicted
     part of parental income), x_perp = x~ - P, R2 = Var(P)/Var(x~). y on P, x_perp, D, ages: b_P and b_perp, and exactly
     b0_D = R2 b_P + (1 - R2) b_perp (b0_D = IGE at equal family structure). b_P = 0: friction-driven parental income is
     noise for the son (it attenuates the IGE); b_P = b_perp: it transmits like the rest; b_P > b_perp: it carries more.
  6. Benchmarks: each group alone (base + that group) and all groups jointly (F, M, S, D, son's schooling, parents'
     schooling, son's occupation, son's industry) on the same rows; joint contributions add up to b0 - b exactly.
  7. NLSY79 (men of the cross-sectional + Black supplemental samples, data/nlsy79_kids.pkl of 2.NLSY79.py: x = ln
     parental income 1979-81; weeks and hours worked in each calendar year from 70.RauhReplication.py's
     data/rauh_nlsy79.pkl; earnings = wages and salary + business income and family income of the income year from
     data/nlsy79_person_year.pkl, 2000 $, rounds to 2018): the son's band share of weeks not worked (mean of 1 - weeks/52
     over his calendar years in the band) as the son's friction; Gelbach of the IGE of ln annual earnings, ln hourly wage,
     ln annual hours (24's bounds for a valid year) and ln family income, 1979 weights, clusters = 1979 household. No
     parental friction is measured in the NLSY79.
CHECKS: pooled unweighted; by race (weighted within race); father-present sons; two-parent sons.
INFERENCE: cluster bootstrap of 1968 families (NLSY79: 1979 households), stratified by race, IGE_NBOOT draws (default 200),
the same draws for every specification (differences between specifications are paired); normal p-values from the
bootstrap s.e.; for ratios (shares) the s.e. is half the 15.9-84.1 percentile range of the draws (73's rse). Regression
tables: weighted least squares with CR1 s.e. clustered by 1968 family. Every estimate: coefficient (s.e.; p), *** p<0.01,
** p<0.05, * p<0.1. DESCRIPTIVE ACCOUNTING: friction years are outcomes of skill as well as of luck and place; nothing here
identifies a causal effect. Writes output/friction_ige_pooled.md and output/friction_ige_pooled.json (aggregates only).
"""
import importlib.util
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import CPI, DATA, OUT  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R73 = _load("s73", "73.SharedFriction.py")
R24 = _load("s24", "24.IGEDecomposition.py")
c, pv, rse, wls, dummies, star = R73.c, R73.pv, R73.rse, R73.wls, R73.dummies, R73.star
BANDS = [(25, 29), (30, 34), (35, 39), (40, 44), (45, 49), (50, 55)]
CL = [f"{lo}-{hi}" for lo, hi in BANDS] + ["25-55"]
RACES = ("White", "Black")
NBOOT = int(os.environ.get("IGE_NBOOT", 200))
SEED = 20261019
RES = {}
WHU = {1975: "V3833", 1976: "V4727", 1977: "V5252", 1978: "V5751", 1979: "V6356", 1980: "V6954", 1981: "V7548",
       1982: "V8246", 1983: "V8848", 1984: "V10139", 1985: "V11265", 1986: "V12664", 1987: "V13816", 1988: "V14872",
       1989: "V16372", 1990: "V17781", 1991: "V19081", 1992: "V20381", 1993: "V21674"}
WUB = {1994: "ER2682", 1995: "ER5681", 1996: "ER7777", 1997: "ER10681", 1999: "ER13842", 2001: "ER17923",
       2003: "ER21567", 2005: "ER25564", 2007: "ER36569", 2009: "ER42590", 2011: "ER47908", 2013: "ER53614",
       2015: "ER60629", 2017: "ER66644", 2019: "ER72646", 2021: "ER78722", 2023: "ER82714"}
FAT = ["f_sh_disp", "f_sh_unemp", "f_sh_zero"]
MOT = ["m_sh_unemp", "m_sh_zero"]
SON = ["sb_disp", "sb_unemp", "sb_zero"]
DST = ["nofa", "nomo", "m_un_na"]
LAB = {"lyp": "ln parental income (13-19 mean)", "f_sh_disp": "father's share of window years displaced",
       "f_sh_unemp": "father's share of window years unemployed", "f_sh_zero": "father's share of window years zero hours",
       "m_sh_unemp": "mother's share of window years unemployed", "m_sh_zero": "mother's share of window years zero hours",
       "m_sh_disp": "mother's share of window years displaced", "sb_disp": "son's share of band years displaced",
       "sb_unemp": "son's share of band years unemployed", "sb_zero": "son's share of band years zero hours",
       "s_sh_disp": "son's career share displaced", "s_sh_unemp": "son's career share unemployed",
       "s_sh_zero": "son's career share zero hours", "f_hu_sh": "father's share of window hours unemployed",
       "m_hu_sh": "mother's share of window hours unemployed", "nofa": "no father in the window",
       "nomo": "no mother in the window", "m_un_na": "mother's unemployment not measured",
       "fdisp": "father displaced in the year", "funemp": "father unemployed in the year"}
OUTL = {"lfam": "ln family income", "ly": "ln annual earnings", "lw": "ln hourly wage", "lh": "ln annual hours",
        "emp": "employed (hours > 0)", "ly0": "ln earnings incl. zero-hours years"}


# ================================================================ mother's window measures
def wife_items():
    cache = DATA / "friction_ige_wife_items.pkl"
    if cache.exists():
        return pd.read_pickle(cache)
    out = []
    for w in sorted(set(WHU) | set(WUB)):
        folder = R24.FAM / (f"fam{w}" if w < 1994 else f"fam{w}er")
        base = next(f for f in folder.glob("*.do") if "formats" not in f.name).with_suffix("")
        pos, labs = R24.layout(base.with_suffix(".do"))
        idv = labs[1][0]
        v = WHU.get(w) or WUB.get(w)
        f = R24.read(base, [idv, v], pos)
        x = pd.DataFrame({"wave": w, "int": f[idv].to_numpy()})
        if w in WHU:
            x["whu"] = f[v].where(f[v].between(0, 5840)).to_numpy()
            x["wub"] = np.nan
        else:
            x["whu"] = np.nan
            x["wub"] = (f[v] == 1).astype(float).where(f[v].isin([0, 1, 5])).to_numpy()
        out.append(x)
    e = pd.concat(out, ignore_index=True)
    e.to_pickle(cache)
    return e


def parent_windows(sons):
    """one row per son: mother-figure window measures (and the father's hours-unemployed intensity); plus the
    window unit-year panel of father and mother (added-worker regressions)."""
    cache = DATA / "friction_ige_parent_windows.pkl"
    if cache.exists():
        return pd.read_pickle(cache)
    a = pd.read_pickle(R24.CACHE)
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    a["unemp"] = pd.to_numeric(a["unemp"], errors="coerce")
    # women of each family unit
    wom = a[a["wife"] | (a["head"] & (a["female"] == 1))].drop_duplicates(["wave", "int"]).reset_index(drop=True)
    wom = wom.merge(wife_items(), on=["wave", "int"], how="left")
    isw = wom["wife"].astype(bool).to_numpy()
    hu = pd.Series(np.where(isw, wom["whu"], wom["hu"]))
    hu = hu.where(wom["wave"] <= 1993)
    ub = pd.Series(np.where(isw, wom["wub"], wom["ub"]))
    u = pd.concat([(hu > 0).astype(float).where(hu.notna()), ub, wom["est23"]], axis=1)
    wom["m_unemp"] = u.max(axis=1).where(u.notna().any(axis=1))
    wom["m_zero"] = (wom["hours"] == 0).astype(float).where(wom["hours"].notna())
    wd = pd.read_pickle(DATA / "correlated_shocks_wife_disp.pkl")
    dm = set(zip(wd.loc[wd["main"] == 1, "pid"], wd.loc[wd["main"] == 1, "year"]))
    wom["m_disp"] = pd.Series([float((p, y) in dm or (p, y - 1) in dm) for p, y in zip(wom["pid"], wom["year"])]).where(
        pd.Series(isw) & (wom["wave"] >= 1984))
    hh = wom["hours"].where(wom["hours"].notna())
    wom["m_hu"], wom["m_hpot"] = hu, (hh + hu).where(hu.notna() & hh.notna())
    wom = wom.rename(columns={"pid": "mpid", "educ": "m_educ_i", "hours": "m_hours", "head": "m_head"})
    # sons' window waves (24's children(): wave-ages 13-19, family income in bounds)
    k = py[py["child"] & py["age"].between(13, 19) & py["faminc"].between(R24.LO, R24.HI) & py["pid"].isin(sons["pid"])][
        ["pid", "wave", "int"]]
    mw = k.merge(wom[["wave", "int", "mpid", "m_unemp", "m_zero", "m_disp", "m_hu", "m_hpot", "m_educ_i", "m_hours",
                      "m_head"]], on=["wave", "int"], how="left")
    g = mw.groupby("pid")
    m = pd.DataFrame({"win_n": g["wave"].count(), "m_nyrs": g["mpid"].count(), "m_sh_zero": g["m_zero"].mean(),
                      "m_sh_unemp": g["m_unemp"].mean(), "m_n_unemp": g["m_unemp"].count(),
                      "m_sh_disp": g["m_disp"].mean(), "m_n_disp": g["m_disp"].count(),
                      "m_fhead": g["m_head"].mean(), "m_educ": g["m_educ_i"].mean()})
    hs = mw.dropna(subset=["m_hpot"]).groupby("pid")[["m_hu", "m_hpot"]].sum()
    m["m_hu_sh"] = (hs["m_hu"] / hs["m_hpot"].where(hs["m_hpot"] > 0))
    # the father's hours-unemployed intensity (fpid = male head at 16; waves <= 1993)
    fa = a[a["head"] & (a["female"] == 0) & (a["wave"] <= 1993)][["pid", "wave", "hu", "hours"]].dropna()
    fp = sons.drop_duplicates("pid")[["pid", "fpid"]].dropna()
    fw = k.merge(fp, on="pid").merge(fa.rename(columns={"pid": "fpid"}), on=["fpid", "wave"])
    fs = fw.groupby("pid")[["hu", "hours"]].sum()
    m["f_hu_sh"] = fs["hu"] / (fs["hu"] + fs["hours"]).where((fs["hu"] + fs["hours"]) > 0)
    # unit-year panel for the added-worker regressions: window waves with the father as head and a woman present
    fa2 = a[a["head"] & (a["female"] == 0)][["pid", "wave", "int", "disp", "unemp", "hours"]].rename(
        columns={"pid": "fpid", "disp": "fdisp", "unemp": "funemp", "hours": "f_hours"})
    pan = k.merge(fp, on="pid").merge(fa2, on=["fpid", "wave", "int"]).merge(
        wom[["wave", "int", "mpid", "m_unemp", "m_zero", "m_hours", "year", "fam68"]], on=["wave", "int"])
    pan = pan.drop_duplicates(["mpid", "wave"])
    m = m.reset_index()
    pd.to_pickle((m, pan), cache)
    return m, pan


# ================================================================ son panel and analysis frame
def build():
    r = R73.load_panel()
    r = r[r["wt"] > 0].copy()
    m, pan = parent_windows(r)
    r = r.merge(m, on="pid", how="left")
    r["nofa"] = r[FAT].isna().any(axis=1).astype(float)
    for v in FAT:
        r[v] = r[v].fillna(0.0)
    r["nomo"] = (r["m_nyrs"].fillna(0) == 0).astype(float)
    r["m_un_na"] = ((r["nomo"] == 0) & (r["m_n_unemp"].fillna(0) == 0)).astype(float)
    r["m_sh_zero"] = r["m_sh_zero"].where(r["nomo"] == 0, 0.0).fillna(0.0)
    r["m_sh_unemp"] = r["m_sh_unemp"].where((r["nomo"] == 0) & (r["m_un_na"] == 0), 0.0).fillna(0.0)
    r["emp"] = (1 - r["zero"]).where(r["zero"].notna())
    r["lfam"] = pd.to_numeric(r["lfam"], errors="coerce")
    # benchmark mediators
    r["educ_na"] = r["educ"].isna().astype(float)
    r["educ0"] = r["educ"].fillna(0.0)
    fe = pd.to_numeric(r["f_educ"], errors="coerce").where(lambda s: s.between(0, 20))
    r["f_educ_na"] = ((r["nofa"] == 0) & fe.isna()).astype(float)
    r["f_educ0"] = fe.where(r["nofa"] == 0).fillna(0.0)
    me = r["m_educ"].where(r["m_educ"].between(0, 20))
    r["m_educ_na"] = ((r["nomo"] == 0) & me.isna()).astype(float)
    r["m_educ0"] = me.where(r["nomo"] == 0).fillna(0.0)
    occ = r["occ11"].fillna(-1).astype(int)
    ind = r["igrp"].fillna(-1).astype(int)
    OCC = []
    for v in sorted(occ.unique())[1:]:
        r[f"occ_{v}"] = (occ == v).astype(float)
        OCC.append(f"occ_{v}")
    IND = []
    for v in sorted(ind.unique())[1:]:
        r[f"ind_{v}"] = (ind == v).astype(float)
        IND.append(f"ind_{v}")
    r["mo2"] = ((r["nofa"] == 0) & (r["nomo"] == 0)).astype(float)
    return r, pan, OCC, IND


# ================================================================ bootstrap engine
class Boot:
    """stratified (race) cluster-bootstrap counts of 1968 families, shared by all specifications."""

    def __init__(self, fam, strat, nboot=NBOOT, seed=SEED):
        f = pd.Series(fam).drop_duplicates()
        self.idx = {v: i for i, v in enumerate(f)}
        st = pd.Series(strat, index=pd.Series(fam).index).groupby(pd.Series(fam).values).first()
        G = len(f)
        rng = np.random.default_rng(seed)
        self.cnt = np.zeros((nboot, G))
        for s in st.unique():
            ids = np.array([self.idx[v] for v in st.index[st == s]])
            for b in range(nboot):
                self.cnt[b, ids] = np.bincount(rng.integers(0, len(ids), len(ids)), minlength=len(ids))

    def rows(self, fam):
        return np.array([self.idx[v] for v in fam])


def gel(x, A, Y, Med, w, groups, ex=None):
    """exact Gelbach split (weighted) for every outcome column of Y; ex = indices for the shared split and design 5."""
    keep = w > 0
    x, A, Y, Med, w = x[keep], A[keep], Y[keep], Med[keep], w[keep]
    sw = np.sqrt(w)
    m, K = Y.shape[1], Med.shape[1]
    B0 = wls(np.column_stack([x, A]), np.column_stack([Y, Med]), sw)
    b0, d = B0[0, :m], B0[0, m:]
    o = {"b0": b0}
    if K:
        B1 = wls(np.column_stack([x, Med, A]), Y, sw)
        b, gam = B1[0], B1[1:1 + K]
        el = gam * d[:, None]
        o["b"] = b
        for gname, ii in groups.items():
            o["c:" + gname] = el[ii].sum(0)
        for kk in range(K):
            o[f"e:{kk}"] = el[kk]
        if ex:
            S, P, D = ex["S"], ex["P"], ex["D"]
            Z = np.column_stack([x, Med[:, P], Med[:, D], A])
            Bs = wls(Z, Med[:, S], sw)
            a_, C = Bs[0], Bs[1:1 + len(P)]
            o["shared"] = (gam[S] * (C.T @ d[P])[:, None]).sum(0)
            o["own"] = (gam[S] * a_[:, None]).sum(0)
            ZD = np.column_stack([Med[:, D], A])
            xt = x - ZD @ wls(ZD, x[:, None], sw)[:, 0]
            Pt = Med[:, P] - ZD @ wls(ZD, Med[:, P], sw)
            pr = Pt @ wls(Pt, xt[:, None], sw)[:, 0]
            xp = xt - pr
            R2 = np.sum(w * pr ** 2) / np.sum(w * xt ** 2)
            Bq = wls(np.column_stack([pr, xp, ZD]), Y, sw)
            b0D = wls(np.column_stack([x, ZD]), Y, sw)[0]
            o["R2"] = np.full(m, R2)
            o["bP"], o["bperp"], o["b0D"] = Bq[0], Bq[1], b0D
            o["bP-bperp"] = Bq[0] - Bq[1]
            o["R2bP"] = R2 * Bq[0]
    return o


def run_spec(d, ys, groups, BT, ex=False, weight=True, cells=range(7), ctrl=()):
    """groups: dict name -> list of columns (order kept). Returns {cell: {'pt': {stat: arr}, 'bs': {stat: (NB, m)}}}."""
    cols = [v for g in groups.values() for v in g]
    gidx, i = {}, 0
    for gname, g in groups.items():
        gidx[gname] = list(range(i, i + len(g)))
        i += len(g)
    exi = None
    if ex:
        exi = {"S": gidx["son"], "P": gidx["father"] + gidx["mother"], "D": gidx["structure"]}
    need = ys + ["lyp", "age", "fam68", "wt"] + cols + list(ctrl)
    d = d.dropna(subset=need)
    res = {"n": (int(d["pid"].nunique()), int(len(d)), int(d["fam68"].nunique())), "cols": cols}
    for k in cells:
        z = d if k == 6 else d[d["band"] == k]
        if len(z) < 100:
            continue
        A = np.column_stack([dummies(z["age"])] + ([z[list(ctrl)].to_numpy(float)] if ctrl else [])
                            + [np.ones((len(z), 1))])
        x, Y, Med = z["lyp"].to_numpy(float), z[ys].to_numpy(float), z[cols].to_numpy(float)
        w0 = z["wt"].to_numpy(float) if weight else np.ones(len(z))
        ri = BT.rows(z["fam68"].to_numpy())
        pt = gel(x, A, Y, Med, w0, gidx, exi)
        bs = {s: np.zeros((BT.cnt.shape[0], len(ys))) for s in pt}
        for b in range(BT.cnt.shape[0]):
            ob = gel(x, A, Y, Med, w0 * BT.cnt[b, ri], gidx, exi)
            for s in pt:
                bs[s][b] = ob[s]
        res[k] = {"pt": pt, "bs": bs}
    # derived group sums
    for k in [kk for kk in res if isinstance(kk, int)]:
        for tag, parts in (("c:parents", ("c:father", "c:mother")), ("c:friction", ("c:father", "c:mother", "c:son"))):
            if all(p in res[k]["pt"] for p in parts):
                res[k]["pt"][tag] = sum(res[k]["pt"][p] for p in parts)
                res[k]["bs"][tag] = sum(res[k]["bs"][p] for p in parts)
        if "b" in res[k]["pt"]:
            res[k]["pt"]["b0-son"] = res[k]["pt"]["b0"] - res[k]["pt"].get("c:son", 0)
            res[k]["bs"]["b0-son"] = res[k]["bs"]["b0"] - res[k]["bs"].get("c:son", 0)
    return res


def est(res, k, stat, j, share=False):
    """(point, s.e., draws) of a stat (or its share of b0) in cell k; k = 'open' -> cell 4 minus cell 0."""
    if k == "open":
        a, b = est(res, 4, stat, j, share), est(res, 0, stat, j, share)
        if a is None or b is None:
            return None
        dr = a[2] - b[2]
        return (a[0] - b[0], rse(dr) if share else float(np.nanstd(dr, ddof=1)), dr)
    if k not in res or stat not in res[k]["pt"]:
        return None
    p, dr = res[k]["pt"][stat][j], res[k]["bs"][stat][:, j]
    if share:
        p0, d0 = res[k]["pt"]["b0"][j], res[k]["bs"]["b0"][:, j]
        return (p / p0, rse(dr / d0), dr / d0)
    return (p, float(np.nanstd(dr, ddof=1)), dr)


def cc(t):
    return c(t[:2]) if t is not None else ""


def comp_table(md, title, res, ys, rows, note="", store="", share_rows=()):
    md += [f"#### {title}", ""] + ([note, ""] if note else [])
    md += ["| outcome | component | " + " | ".join(CL) + " | opening 45-49 - 25-29 |", "|---" * 10 + "|"]
    for j, y in enumerate(ys):
        for stat, lab in rows:
            ent = [est(res, k, stat, j) for k in list(range(7)) + ["open"]]
            md.append(f"| {OUTL.get(y, y)} | {lab} | " + " | ".join(cc(e) for e in ent) + " |")
            RES[f"{store}|{y}|{stat}"] = [list(e[:2]) if e else None for e in ent]
        for stat, lab in share_rows:
            ent = [est(res, k, stat, j, share=True) for k in list(range(7)) + ["open"]]
            md.append(f"| {OUTL.get(y, y)} | share: {lab} | " + " | ".join(cc(e) for e in ent) + " |")
            RES[f"{store}|{y}|share|{stat}"] = [list(e[:2]) if e else None for e in ent]
    n = res["n"]
    md += [f"Sons / son-years / 1968 families: {n[0]:,} / {n[1]:,} / {n[2]:,}.", ""]


# ================================================================ weighted regressions with CR1 clustered s.e.
def wreg(d, y, xs, cl="fam68", w="wt", age_dummies=True, absorb=None, fe=()):
    z = d.dropna(subset=[y] + list(xs) + [cl] + ([w] if w else []) + ([absorb] if absorb else []) + list(fe))
    parts = [z[list(xs)].to_numpy(float)]
    if age_dummies:
        parts.append(dummies(z["age"]))
    for f in fe:
        parts.append(dummies(z[f]))
    X = np.column_stack(parts)
    yv = z[y].to_numpy(float)
    ww = z[w].to_numpy(float) if w else np.ones(len(z))
    if absorb:
        M = R73.demean(np.column_stack([yv, X]), z[absorb].to_numpy(), ww)
        yv, X = M[:, 0], M[:, 1:]
    else:
        X = np.column_stack([X, np.ones(len(z))])
    keepc = np.abs(X).sum(axis=0) > 1e-9
    X = X[:, keepc]
    Xw = X * ww[:, None]
    XtXi = np.linalg.pinv(X.T @ Xw)
    b = XtXi @ Xw.T @ yv
    u = yv - X @ b
    S = pd.DataFrame(Xw * u[:, None]).groupby(z[cl].to_numpy()).sum().to_numpy()
    G, (n, kk) = S.shape[0], X.shape
    V = XtXi @ (S.T @ S) @ XtXi * G / (G - 1) * (n - 1) / (n - kk)
    return ({v: (float(b[i]), float(np.sqrt(V[i, i]))) for i, v in enumerate(xs)}, len(z),
            int(z["pid"].nunique()) if "pid" in z else len(z), int(z[cl].nunique()))


def reg_table(md, title, cols, rows, panels, note=""):
    md += [f"#### {title}", ""] + ([note, ""] if note else [])
    md += ["| | " + " | ".join(f"({i + 1}) {h}" for i, (h, _) in enumerate(cols)) + " |", "|---" * (len(cols) + 1) + "|"]
    for plab, samp in panels:
        md.append(f"| **{plab}** |" + " |" * len(cols))
        out = [fn(samp) for _, fn in cols]
        for v, lab in rows:
            md.append(f"| {lab} | " + " | ".join(c(o[0].get(v)) if v in o[0] else "" for o in out) + " |")
        md.append("| N obs / sons / clusters | " + " | ".join(f"{o[1]:,} / {o[2]:,} / {o[3]:,}" for o in out) + " |")
        for i, (h, _) in enumerate(cols):
            RES[f"{title}|{plab}|({i + 1}) {h}"] = {k: list(v) for k, v in out[i][0].items()}
    md.append("")


# ================================================================ NLSY79
def nlsy79(md):
    R70 = _load("s70", "70.RauhReplication.py")
    P, _ = R70.build(R70.extract())
    k = pd.read_pickle(DATA / "nlsy79_kids.pkl")
    k = k[(k["female"] == 0) & k["race"].isin(RACES)][["pid", "race", "lpinc_av", "hhid", "wt79"]]
    P = P.drop(columns=[x for x in ("wt79",) if x in P.columns]).merge(k, on="pid")
    P = P[P["wk"].between(0, 52) & P["age"].between(25, 55) & P["lpinc_av"].notna() & (P["wt79"] > 0)].copy()
    P["nonemp"] = 1 - P["wk"] / 52
    P["band"] = pd.cut(P["age"], [24, 29, 34, 39, 44, 49, 55], labels=False).astype(int)
    P["nb_nonemp"] = P.groupby(["pid", "band"])["nonemp"].transform("mean")
    # earnings and family income of the income year (2.NLSY79.py, 2000 $; round t -> calendar year t - 1): they cover
    # the rounds to 2018, where 70's wage-and-salary item stops in 2000
    q = pd.read_pickle(DATA / "nlsy79_person_year.pkl")[["pid", "round", "earn", "faminc"]]
    q["cal"] = q["round"] - 1
    P = P.drop(columns=["earn"]).merge(q.drop(columns="round"), on=["pid", "cal"], how="left")
    e2000 = P["earn"]
    valid = e2000.between(R24.LO, R24.HI) & (P["hrs"] >= 100) & (e2000 / P["hrs"]).between(2, 200)
    P["ly"] = np.log(e2000.where(valid))
    P["lh"] = np.log(P["hrs"].where(valid))
    P["lw"] = P["ly"] - P["lh"]
    P["lfam"] = np.log(P["faminc"].where(P["faminc"].between(R24.LO, R24.HI)))
    P = P.rename(columns={"lpinc_av": "lyp", "wt79": "wt"})
    P["fam68"] = P["hhid"]
    BT = Boot(P["hhid"].to_numpy(), P["race"].to_numpy(), seed=SEED + 7)
    md += ["## 7. NLSY79 check: the son's weeks not worked and the IGE", "",
           "Men of the cross-sectional + Black supplemental samples (2.NLSY79.py), calendar years at 25-55; x = ln parental "
           "income (1979-81 mean); son's friction = his band share of weeks not worked (mean of 1 - weeks/52 over his "
           "calendar years in the band); earnings = wages and salary + business income of the income year (2000 $, rounds "
           "to 2018), valid years for ln earnings / wage / hours by 24's bounds; ln family income in bounds. 1979 weights; "
           f"{NBOOT} bootstrap draws of 1979 households within race. No parental friction is measured in the NLSY79.", ""]
    v = P[P["ly"].notna()]
    o = run_spec(v, ["ly", "lw", "lh"], {"son": ["nb_nonemp"]}, BT)
    comp_table(md, "7a. Pooled, weighted: IGE, son's weeks-not-worked contribution, IGE at equal son's friction", o,
               ["ly", "lw", "lh"], [("b0", "IGE (base)"), ("c:son", "son's weeks not worked"), ("b", "rest (b)")],
               share_rows=[("c:son", "son's weeks not worked")], store="7a")
    of = run_spec(P[P["lfam"].notna()], ["lfam"], {"son": ["nb_nonemp"]}, BT)
    comp_table(md, "7a'. Pooled, weighted: ln family income (all calendar years with it)", of, ["lfam"],
               [("b0", "IGE (base)"), ("c:son", "son's weeks not worked"), ("b", "rest (b)")],
               share_rows=[("c:son", "son's weeks not worked")], store="7a2")
    o2 = run_spec(P, ["nonemp"], {}, BT)
    md += ["#### 7b. The son's share of weeks not worked in the calendar year on ln parental income (pooled, weighted)",
           "", "| outcome | " + " | ".join(CL) + " | opening |", "|---" * 9 + "|",
           "| share of weeks not worked | " + " | ".join(cc(est(o2, k, "b0", 0)) for k in list(range(7)) + ["open"])
           + " |", ""]
    RES["7b"] = [list(est(o2, k, "b0", 0)[:2]) for k in range(7)]
    for race in RACES:
        orc = run_spec(v[v["race"] == race], ["ly", "lw"], {"son": ["nb_nonemp"]}, BT)
        comp_table(md, f"7c. {race} men (weighted)", orc, ["ly", "lw"],
                   [("b0", "IGE (base)"), ("c:son", "son's weeks not worked")],
                   share_rows=[("c:son", "son's weeks not worked")], store=f"7c{race}")


# ================================================================ main
def main():
    t0 = time.time()
    r, pan, OCC, IND = build()
    BT = Boot(r["fam68"].to_numpy(), r["race"].to_numpy())
    md = ["# Search friction of the father, the mother and the son in the IGE: pooled sons", "",
          "Built by `74.FrictionIGEPooled.py` (2026-10-19); every variable and design is defined in its docstring. PSID "
          "sons 25-55, Black and White pooled with PSID individual weights (race is a secondary check). Estimate (s.e.; "
          "p), *** p<0.01, ** p<0.05, * p<0.1; s.e. clustered by 1968 family (CR1 for regressions; "
          f"{NBOOT} cluster-bootstrap draws of 1968 families, stratified by race, for decompositions, shares, openings "
          "and differences). Each band is its own regression with single-age dummies; '25-55' = all son-years in one "
          "regression; opening = 45-49 minus 25-29. **Descriptive accounting**: friction years are outcomes of skill "
          "as well as of luck and place.", ""]
    one = r.drop_duplicates("pid")
    # ------------------------------------------------ 0. samples
    md += ["## 0. Samples and friction rates (weighted means)", "",
           "| sample | sons | son-years | valid son-years | weighted Black share of son-years | father in the window | "
           "mother in the window | mother's unemployment measured (if present) | son: displaced / unemployed / zero "
           "hours (share of son-years) | father: displaced / unemployed / zero hours (window shares, if present) | "
           "mother: unemployed / zero hours (window shares, if present) | mother is a female head (share of her window "
           "years) |", "|---" * 12 + "|"]

    def wm(s, v, cond=None):
        s = s if cond is None else s[cond(s)]
        s = s.dropna(subset=[v])
        return float(np.average(s[v], weights=s["wt"])) if len(s) else np.nan
    for lab, s in (("pooled", r), ("White", r[r.race == "White"]), ("Black", r[r.race == "Black"])):
        so = s.drop_duplicates("pid")
        fp = lambda q: q["nofa"] == 0  # noqa: E731
        mp = lambda q: q["nomo"] == 0  # noqa: E731
        mu = lambda q: (q["nomo"] == 0) & (q["m_un_na"] == 0)  # noqa: E731
        s2 = s.assign(blk=(s.race == "Black").astype(float), fpres=1 - s.nofa, mpres=1 - s.nomo,
                      munm=1 - s.m_un_na)
        md.append(f"| {lab} | {len(so):,} | {len(s):,} | {int(s['lw'].notna().sum()):,} | {wm(s2, 'blk'):.3f} | "
                  f"{wm(s2, 'fpres'):.3f} | {wm(s2, 'mpres'):.3f} | {wm(s2, 'munm', mp):.3f} | "
                  f"{wm(s, 'disp'):.3f} / {wm(s, 'unemp'):.3f} / {wm(s, 'zero'):.3f} | "
                  f"{wm(s, 'f_sh_disp', fp):.3f} / {wm(s, 'f_sh_unemp', fp):.3f} / {wm(s, 'f_sh_zero', fp):.3f} | "
                  f"{wm(s, 'm_sh_unemp', mu):.3f} / {wm(s, 'm_sh_zero', mp):.3f} | {wm(s, 'm_fhead', mp):.3f} |")
        RES[f"0|{lab}"] = {"sons": len(so), "son_years": len(s)}
    md += ["", "<<SUMMARY>>"]
    G_MAIN = {"father": FAT, "mother": MOT, "son": SON, "structure": DST}
    ROWS = [("b0", "IGE (base)"), ("c:father", "father's friction"), ("c:mother", "mother's friction"),
            ("c:son", "son's friction"), ("shared", "  of which shared with the parents' friction"),
            ("own", "  of which his own gradient in parental income"), ("c:structure", "family structure (not friction)"),
            ("b", "rest: IGE at equal friction (b)")]
    SHR = [("c:father", "father"), ("c:mother", "mother"), ("c:son", "son"), ("shared", "son, shared with parents"),
           ("c:parents", "parents (father + mother)"), ("c:friction", "all friction (father + mother + son)")]
    # ------------------------------------------------ 1. main decomposition
    print("1 ...", flush=True)
    v = r[r["lw"].notna()]
    oV = run_spec(v, ["ly", "lw", "lh"], G_MAIN, BT, ex=True)
    print(f"  valid done {time.time() - t0:.0f}s", flush=True)
    oF = run_spec(r[r["lfam"].notna()], ["lfam"], G_MAIN, BT, ex=True)
    oE = run_spec(r[r["emp"].notna()], ["emp"], {"father": FAT, "mother": MOT, "son": ["sb_disp", "sb_unemp"],
                                                 "structure": DST}, BT, ex=True)
    oZ = run_spec(r[r["ly0"].notna()], ["ly0"], G_MAIN, BT, ex=True)
    md += ["## 1. How much of the pooled IGE runs through each person's search friction (Gelbach, weighted)", "",
           "b0 = father's + mother's + son's friction + family structure + rest, exactly. Son's friction = shared with "
           "the parents' friction + his own gradient + a part through family structure (not shown). Shares = "
           "contribution / b0 (bootstrap percentile s.e.).", ""]
    comp_table(md, "1a. ln family income of the son (all son-years with it)", oF, ["lfam"], ROWS, store="1a",
               share_rows=SHR)
    comp_table(md, "1b. ln annual earnings, ln hourly wage, ln annual hours (valid years; earnings = wage + hours in "
                   "every row)", oV, ["ly", "lw", "lh"], ROWS, store="1b", share_rows=SHR)
    comp_table(md, "1c. Employment (hours > 0), every son-year; son's friction = displaced and unemployed shares only",
               oE, ["emp"], ROWS, store="1c", share_rows=SHR[:3] + SHR[4:])
    comp_table(md, "1d. ln earnings including zero-hours years (10th-percentile rule)", oZ, ["ly0"], ROWS, store="1d",
               share_rows=SHR)
    # element-level contributions
    md += ["#### 1e. Contribution of each friction measure (g_k d_k), 25-29, 35-39, 45-49 and 25-55", "",
           "| outcome | measure | 25-29 | 35-39 | 45-49 | 25-55 |", "|---|---|---|---|---|---|"]
    for oo, ys in ((oF, ["lfam"]), (oV, ["ly", "lw", "lh"])):
        for j, y in enumerate(ys):
            for kk, col in enumerate(oo["cols"]):
                if col in DST:
                    continue
                ent = [est(oo, k, f"e:{kk}", j) for k in (0, 2, 4, 6)]
                md.append(f"| {OUTL[y]} | {LAB[col]} | " + " | ".join(cc(e) for e in ent) + " |")
                RES[f"1e|{y}|{col}"] = [list(e[:2]) if e else None for e in ent]
    md.append("")
    # links of the chain (regressions)
    md += ["### 1f. The links (pooled, weighted, single-age dummies, son-years 25-55 with a valid wage)", ""]
    allx = ["lyp"] + FAT + MOT + DST
    cl_ = lambda y, xs: (lambda s: wreg(s, y, xs))  # noqa: E731
    reg_table(md, "1f-i. Parental friction and parental income: d_k (friction on x) and x on all parental friction",
              [(LAB[f], cl_(f, ["lyp", "nofa"] if f.startswith("f_") else ["lyp", "nomo", "m_un_na"]))
               for f in FAT + MOT] + [("ln parental income", cl_("lyp", FAT + MOT + DST))],
              [(x_, LAB[x_]) for x_ in allx], [("pooled", v)],
              note="Columns (1)-(5): the friction share on parental income (with the family-structure flags of that "
                   "parent); column (6): parental income on all parental friction (person-year weighted, as the IGE).")
    reg_table(md, "1f-ii. The son's friction on his parents' friction at equal parental income (C) and the son's "
                  "outcomes on all friction (g)",
              [(LAB[s_], cl_(s_, allx)) for s_ in SON] + [("ln earnings", cl_("ly", allx + SON)),
                                                         ("ln hourly wage", cl_("lw", allx + SON)),
                                                         ("ln annual hours", cl_("lh", allx + SON))],
              [(x_, LAB[x_]) for x_ in allx + SON], [("pooled", v)])
    print(f"  1 done {time.time() - t0:.0f}s", flush=True)
    # ------------------------------------------------ 2. wage vs hours
    md += ["## 2. The hours part and the wage part of the earnings IGE: how much of each is friction", "",
           "On valid years ln earnings = ln wage + ln hours, so each contribution to the earnings IGE splits exactly into "
           "a wage part and an hours part (1b). 'Hours share' = hours part / earnings contribution.", "",
           "| quantity | " + " | ".join(CL) + " | opening |", "|---" * 9 + "|"]
    for stat, lab in (("b0", "IGE"), ("c:friction", "all friction"), ("c:son", "son's friction"),
                      ("c:parents", "parents' friction")):
        for j, y in ((0, "ly"), (1, "lw"), (2, "lh")):
            md.append(f"| {lab}: {OUTL[y]} | " + " | ".join(cc(est(oV, k, stat, j)) for k in list(range(7)) + ["open"])
                      + " |")
        ent = []
        for k in range(7):
            a_, b_ = est(oV, k, stat, 2), est(oV, k, stat, 0)
            ent.append((a_[0] / b_[0], rse(a_[2] / b_[2])))
        md.append(f"| {lab}: hours share of the earnings figure | " + " | ".join(c(e) for e in ent) + " | |")
        RES[f"2|{stat}|hours_share"] = ent
        if stat != "b0":
            ent2 = [est(oV, k, stat, 1, share=True)[:2] for k in range(7)]
            md.append(f"| {lab}: share of the wage IGE | " + " | ".join(c(e) for e in ent2) + " | |")
            RES[f"2|{stat}|wage_share"] = ent2
    md.append("")
    # ------------------------------------------------ 3. age profile / life-cycle
    print("3 ...", flush=True)
    md += ["## 3. Does the friction share change with the son's age?", "",
           "Openings are in 1a-1d (last column). Here: the IGE net of the son's friction contribution by band, and the "
           "life-cycle ratio IGE(25-29) / IGE(45-49) with and without it; then the son's friction measured over his "
           "career (25-55) instead of the band.", "",
           "| outcome | quantity | " + " | ".join(CL) + " | opening |", "|---" * 10 + "|"]
    for oo, ys in ((oF, ["lfam"]), (oV, ["ly", "lw", "lh"]), (oZ, ["ly0"])):
        for j, y in enumerate(ys):
            md.append(f"| {OUTL[y]} | IGE | " + " | ".join(cc(est(oo, k, "b0", j)) for k in list(range(7)) + ["open"])
                      + " |")
            md.append(f"| {OUTL[y]} | IGE net of the son's friction | " + " | ".join(
                cc(est(oo, k, "b0-son", j)) for k in list(range(7)) + ["open"]) + " |")
            for stat, lab in (("b0", "IGE"), ("b0-son", "IGE net of son's friction")):
                a_, b_ = est(oo, 0, stat, j), est(oo, 4, stat, j)
                rr = (a_[0] / b_[0], rse(a_[2] / b_[2]))
                md.append(f"| {OUTL[y]} | ratio 25-29 / 45-49: {lab} | {c(rr)} |" + " |" * 7)
                RES[f"3|{y}|ratio|{stat}"] = rr
            a_, b_ = est(oo, 0, "b0", j), est(oo, 4, "b0", j)
            a2, b2 = est(oo, 0, "b0-son", j), est(oo, 4, "b0-son", j)
            dr = a2[2] / b2[2] - a_[2] / b_[2]
            md.append(f"| {OUTL[y]} | change in the ratio from netting out the son's friction | "
                      f"{c((a2[0] / b2[0] - a_[0] / b_[0], rse(dr)))} |" + " |" * 7)
    md.append("")
    G_CAR = {"father": FAT, "mother": MOT, "son": ["s_sh_disp", "s_sh_unemp", "s_sh_zero"], "structure": DST}
    oC = run_spec(v, ["ly", "lw", "lh"], G_CAR, BT, ex=True)
    comp_table(md, "3b. Son's friction = his career shares 25-55 (valid years)", oC, ["ly", "lw", "lh"],
               [("b0", "IGE (base)"), ("c:son", "son's friction (career)"), ("c:parents", "parents' friction"),
                ("b", "rest (b)")], store="3b", share_rows=[("c:son", "son (career)"), ("c:parents", "parents"),
                                                            ("c:friction", "all friction")])
    print(f"  3 done {time.time() - t0:.0f}s", flush=True)
    # ------------------------------------------------ 4. mother
    print("4 ...", flush=True)
    md += ["## 4. The mother: a separate channel?", ""]
    oMa = run_spec(v, ["ly", "lw", "lh"], {"mother": MOT, "structure": DST}, BT)
    oFa = run_spec(v, ["ly", "lw", "lh"], {"father": FAT, "structure": DST}, BT)
    oFM = run_spec(v, ["ly", "lw", "lh"], {"father": FAT, "mother": MOT, "structure": DST}, BT)
    md += ["#### 4a. Parents' friction alone (no son's friction): mother alone, father alone, both (valid years)", "",
           "| outcome | contribution | 25-29 | 35-39 | 45-49 | 25-55 | share 25-55 |", "|---|---|---|---|---|---|---|"]
    for j, y in enumerate(["ly", "lw", "lh"]):
        for oo, stat, lab in ((oMa, "c:mother", "mother alone"), (oFa, "c:father", "father alone"),
                              (oFM, "c:mother", "mother, with the father"), (oFM, "c:father", "father, with the mother")):
            md.append(f"| {OUTL[y]} | {lab} | " + " | ".join(cc(est(oo, k, stat, j)) for k in (0, 2, 4, 6))
                      + f" | {cc(est(oo, 6, stat, j, share=True))} |")
            RES[f"4a|{y}|{lab}"] = [list(est(oo, k, stat, j)[:2]) for k in (0, 2, 4, 6)]
    md.append("")
    # two-parent sons
    tp = v[v["mo2"] == 1]
    oT = run_spec(tp, ["ly", "lw", "lh"], {"father": FAT, "mother": MOT, "son": SON, "structure": ["m_un_na"]}, BT,
                  ex=True)
    comp_table(md, "4b. Two-parent sons (father and a woman in the window), valid years", oT, ["ly", "lw", "lh"], ROWS,
               store="4b", share_rows=SHR)
    oT2 = run_spec(r[(r["mo2"] == 1) & r["lfam"].notna()], ["lfam"],
                   {"father": FAT, "mother": MOT, "son": SON, "structure": ["m_un_na"]}, BT, ex=True)
    comp_table(md, "4b'. Two-parent sons, ln family income", oT2, ["lfam"], ROWS, store="4b2", share_rows=SHR)
    # mother's displacement (sons born 1966+)
    lt = r[(r["birth_year"] >= 1966)].copy()
    lt["m_dis_na"] = ((lt["nomo"] == 0) & (lt["m_n_disp"].fillna(0) == 0)).astype(float)
    lt["m_sh_disp"] = lt["m_sh_disp"].where(lt["m_dis_na"] == 0, 0.0).fillna(0.0)
    vl = lt[lt["lw"].notna()]
    oD = run_spec(vl, ["ly", "lw", "lh"], {"father": FAT, "mother": MOT + ["m_sh_disp"], "son": SON,
                                           "structure": DST + ["m_dis_na"]}, BT, ex=True)
    comp_table(md, "4c. Sons born 1966+: the mother's friction includes her job losses (wives, waves 1984+)", oD,
               ["ly", "lw", "lh"], ROWS, store="4c", share_rows=SHR)
    md += ["Contribution of the mother's displacement share alone (element): " + "; ".join(
        f"{OUTL[y]} 25-55 {cc(est(oD, 6, 'e:' + str(oD['cols'].index('m_sh_disp')), j))}"
        for j, y in enumerate(["ly", "lw", "lh"])), ""]
    # intensity: hours unemployed
    it = r[r["f_hu_sh"].notna() | (r["nofa"] == 1)].copy()
    it["f_hu_sh"] = it["f_hu_sh"].fillna(0.0)
    it["m_hu_na"] = ((it["nomo"] == 0) & it["m_hu_sh"].isna()).astype(float)
    it["m_hu_sh"] = it["m_hu_sh"].fillna(0.0)
    vi = it[it["lw"].notna()]
    oI = run_spec(vi, ["ly", "lw", "lh"], {"father": ["f_sh_disp", "f_hu_sh", "f_sh_zero"],
                                           "mother": ["m_hu_sh", "m_sh_zero"], "son": SON,
                                           "structure": ["nofa", "nomo", "m_hu_na"]}, BT, ex=True)
    comp_table(md, "4d. Friction intensity: unemployment measured as the share of the window's potential hours "
                   "unemployed (windows with the hours-unemployed item, waves <= 1993)", oI, ["ly", "lw", "lh"], ROWS,
               store="4d", share_rows=SHR)
    # added worker
    pan = pan.copy()
    for vv in ("fdisp", "funemp", "m_unemp", "m_zero", "m_hours"):
        pan[vv] = pd.to_numeric(pan[vv], errors="coerce")
    pan["m_hk"] = pan["m_hours"] / 1000
    pan["pid"] = pan["mpid"]
    pan["age"] = 40
    aw = lambda y: (lambda s: wreg(s, y, ["fdisp", "funemp"], w=None, age_dummies=False, absorb="mpid",  # noqa: E731
                                   fe=("year",)))
    reg_table(md, "4e. Added worker: the mother's labor supply in a window year on the father's friction that year "
                  "(woman FE + year FE; unit-years with the father as head and a woman present; unweighted)",
              [("mother's annual hours (1000s)", aw("m_hk")), ("mother zero hours", aw("m_zero")),
               ("mother unemployed", aw("m_unemp"))],
              [("fdisp", LAB["fdisp"]), ("funemp", LAB["funemp"])], [("pooled", pan)],
              note="19.FatherDisplacement.py's event study (output/father_displacement.md, 2a): after the father's "
                   "displacement his hours fall by 145*** a year (+1..+3) and the wife's rise by 51** (s.e. 23).")
    sl = lambda y, xs: (lambda s: wreg(s, y, xs, age_dummies=False))  # noqa: E731
    o1 = r[(r["mo2"] == 1)].drop_duplicates("pid")
    reg_table(md, "4f. One row per two-parent son: the mother's window friction on the father's (weighted)",
              [("mother's share unemployed", sl("m_sh_unemp", FAT + ["lyp"])),
               ("mother's share zero hours", sl("m_sh_zero", FAT + ["lyp"]))],
              [(x_, LAB[x_]) for x_ in FAT + ["lyp"]], [("pooled", o1[o1["m_un_na"] == 0])])
    print(f"  4 done {time.time() - t0:.0f}s", flush=True)
    # ------------------------------------------------ 5. transmission vs noise
    md += ["## 5. Is the friction-driven part of parental income transmission or noise?", "",
           "P = the part of ln parental income (net of ages and family structure) predicted by the father's and the "
           "mother's window friction; R2 = Var(P)/Var(x). y on P and the residual x_perp: b_P, b_perp; exactly IGE (at "
           "equal family structure) = R2 b_P + (1 - R2) b_perp. Same rows as section 1.", ""]
    rows5 = [("b0D", "IGE at equal family structure"), ("R2", "R2 = Var(P)/Var(x)"),
             ("bP", "b_P: IGE on friction-predicted parental income"), ("bperp", "b_perp: IGE on the rest"),
             ("bP-bperp", "b_P - b_perp"), ("R2bP", "R2 b_P: part of the IGE through friction-predicted income")]
    comp_table(md, "5a. ln family income", oF, ["lfam"], rows5, store="5a")
    comp_table(md, "5b. ln earnings, wage, hours (valid years)", oV, ["ly", "lw", "lh"], rows5, store="5b")
    comp_table(md, "5c. Employment", oE, ["emp"], rows5, store="5c")
    # ------------------------------------------------ 6. benchmarks
    print("6 ...", flush=True)
    md += ["## 6. Benchmark: friction vs recognised mediators on the same rows", "",
           "Alone = base + that group only (its own Gelbach contribution); joint = every group in one full regression "
           "(contributions add up to b0 - b exactly). Valid years (wage, earnings, hours) and son-years with family "
           "income.", ""]
    BEN = {"son's schooling": ["educ0", "educ_na"], "parents' schooling": ["f_educ0", "f_educ_na", "m_educ0", "m_educ_na"],
           "son's occupation (11 groups)": OCC, "son's industry (33 groups)": IND}
    GJ = dict(G_MAIN)
    GJ.update(BEN)
    for yset, frame, tag in ((["ly", "lw", "lh"], v, "v"), (["lfam"], r[r["lfam"].notna()], "f")):
        alone = {g: run_spec(frame, yset, {g: cols, "structure": DST} if g in ("father", "mother") else {g: cols}, BT)
                 for g, cols in list(BEN.items()) + [("father", FAT), ("mother", MOT), ("son", SON)]}
        alone["friction"] = oV if tag == "v" else oF
        oJ = run_spec(frame, yset, GJ, BT)
        md += [f"#### 6{tag}. " + ", ".join(OUTL[y] for y in yset), "",
               "| outcome | group | alone 25-29 | alone 45-49 | alone 25-55 | share alone 25-55 | joint 25-29 | joint "
               "45-49 | joint 25-55 | share joint 25-55 |", "|---" * 10 + "|"]
        for j, y in enumerate(yset):
            md.append(f"| {OUTL[y]} | IGE (base) | {cc(est(oJ, 0, 'b0', j))} | {cc(est(oJ, 4, 'b0', j))} | "
                      f"{cc(est(oJ, 6, 'b0', j))} | | | | | |")
            for g in ["father", "mother", "son", "friction"] + list(BEN):
                stat = "c:friction" if g == "friction" else "c:" + g
                ao = alone[g]
                aa = [est(ao, k, stat, j) for k in (0, 4, 6)] + [est(ao, 6, stat, j, share=True)]
                jj = [est(oJ, k, stat, j) for k in (0, 4, 6)] + [est(oJ, 6, stat, j, share=True)]
                lab = "all friction (father + mother + son)" if g == "friction" else g
                md.append(f"| {OUTL[y]} | {lab} | " + " | ".join(cc(e) for e in aa + jj) + " |")
                RES[f"6|{y}|{g}"] = {"alone": [list(e[:2]) for e in aa], "joint": [list(e[:2]) for e in jj]}
            md.append(f"| {OUTL[y]} | rest (b), joint | | | | | {cc(est(oJ, 0, 'b', j))} | {cc(est(oJ, 4, 'b', j))} | "
                      f"{cc(est(oJ, 6, 'b', j))} | {cc(est(oJ, 6, 'b', j, share=True))} |")
            # differences friction vs schooling (alone, 25-55), paired draws
            for g in BEN:
                a1, a2 = est(alone["friction"], 6, "c:friction", j), est(alone[g], 6, "c:" + g, j)
                dd = a1[2] - a2[2]
                md.append(f"| {OUTL[y]} | all friction minus {g}, alone, 25-55 | | | {c((a1[0] - a2[0], float(np.std(dd, ddof=1))))} |"
                          + " |" * 6)
        md.append("")
    print(f"  6 done {time.time() - t0:.0f}s", flush=True)
    # ------------------------------------------------ checks: unweighted, by race, father-present
    print("checks ...", flush=True)
    md += ["## 8. Checks: unweighted pooled; by race (weighted within race); father-present sons", ""]
    chk = {}
    chk["pooled, unweighted"] = (run_spec(v, ["ly", "lw", "lh"], G_MAIN, BT, ex=True, weight=False),
                                 run_spec(r[r["lfam"].notna()], ["lfam"], G_MAIN, BT, ex=True, weight=False))
    for race in RACES:
        chk[f"{race}, weighted"] = (run_spec(v[v.race == race], ["ly", "lw", "lh"], G_MAIN, BT, ex=True),
                                    run_spec(r[(r.race == race) & r["lfam"].notna()], ["lfam"], G_MAIN, BT, ex=True))
    fpv = v[v["nofa"] == 0]
    chk["father-present, weighted"] = (run_spec(fpv, ["ly", "lw", "lh"], G_MAIN, BT, ex=True),
                                       run_spec(r[(r["nofa"] == 0) & r["lfam"].notna()], ["lfam"], G_MAIN, BT, ex=True))
    chk["pooled, weighted (main)"] = (oV, oF)
    md += ["| sample | outcome | IGE 25-29 | IGE 45-49 | IGE 25-55 | share father 25-55 | share mother 25-55 | share son "
           "25-29 | share son 45-49 | share son 25-55 | share all friction 25-55 | R2 | b_P - b_perp 25-55 |",
           "|---" * 13 + "|"]
    for lab, (o1_, o2_) in chk.items():
        for oo, ys in ((o2_, ["lfam"]), (o1_, ["ly", "lw", "lh"])):
            for j, y in enumerate(ys):
                ent = [est(oo, 0, "b0", j), est(oo, 4, "b0", j), est(oo, 6, "b0", j),
                       est(oo, 6, "c:father", j, True), est(oo, 6, "c:mother", j, True), est(oo, 0, "c:son", j, True),
                       est(oo, 4, "c:son", j, True), est(oo, 6, "c:son", j, True), est(oo, 6, "c:friction", j, True),
                       est(oo, 6, "R2", j), est(oo, 6, "bP-bperp", j)]
                md.append(f"| {lab} | {OUTL[y]} | " + " | ".join(cc(e) for e in ent) + " |")
                RES[f"8|{lab}|{y}"] = [list(e[:2]) if e else None for e in ent]
    md.append("")
    # ------------------------------------------------ 7. NLSY79
    print("7 ...", flush=True)
    try:
        nlsy79(md)
    except Exception as ex_:  # optional block
        md += [f"## 7. NLSY79: not run ({ex_!r})", ""]
    # ------------------------------------------------ summary at the top
    sm = ["## Summary: shares of the pooled IGE accounted for by each person's search friction (weighted, Gelbach)", "",
          "Share = contribution / IGE in the band (bootstrap percentile s.e.). Parents = father + mother; all = father + "
          "mother + son. Shared = the son's friction that follows his parents' friction.", "",
          "| outcome | IGE 25-29 | IGE 45-49 | IGE 25-55 | father 25-55 | mother 25-55 | son 25-29 | son 45-49 | son "
          "25-55 | son: shared with parents 25-55 | parents 25-55 | all friction 25-29 | all friction 45-49 | all "
          "friction 25-55 | opening of the all-friction share |", "|---" * 15 + "|"]
    for oo, ys in ((oF, ["lfam"]), (oV, ["ly", "lw", "lh"]), (oE, ["emp"]), (oZ, ["ly0"])):
        for j, y in enumerate(ys):
            ent = [est(oo, 0, "b0", j), est(oo, 4, "b0", j), est(oo, 6, "b0", j), est(oo, 6, "c:father", j, True),
                   est(oo, 6, "c:mother", j, True), est(oo, 0, "c:son", j, True), est(oo, 4, "c:son", j, True),
                   est(oo, 6, "c:son", j, True), est(oo, 6, "shared", j, True), est(oo, 6, "c:parents", j, True),
                   est(oo, 0, "c:friction", j, True), est(oo, 4, "c:friction", j, True),
                   est(oo, 6, "c:friction", j, True), est(oo, "open", "c:friction", j, True)]
            sm.append(f"| {OUTL[y]} | " + " | ".join(cc(e) for e in ent) + " |")
            RES[f"summary|{y}"] = [list(e[:2]) if e else None for e in ent]
    sm.append("")
    i_ = md.index("<<SUMMARY>>")
    md[i_:i_ + 1] = sm
    (OUT / "friction_ige_pooled.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "friction_ige_pooled.json", "w"), indent=1,
              default=lambda o: None if isinstance(o, np.ndarray) else (float(o) if isinstance(o, np.floating) else str(o)))
    print(f"done {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
