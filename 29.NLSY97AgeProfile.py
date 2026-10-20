r"""The age profile of intergenerational persistence in the NLSY97, by race, compared with the PSID and NLSY79
(2026-10-17).

Question (Paper B's core fact, EVIDENCE.md 1.9-1.16): in the PSID the pooled log IGE rises with the child's age at
measurement, the Black-White log IGE gap is zero at 25-29 and opens after 30, rank-rank slopes are equal by race at
every age and the expected-rank gap at parental p25 is a stable 11-15 points. Does a more recent cohort (NLSY97,
born 1980-84, observed to ages ~38-44 in 2023) with parental income reported once by a parent in 1997 show the
same profile through the ages it allows (25-29, 30-34, 35-39, 40-44)?

DATA (read only). The existing extract (3.NLSY97.py, data/nlsy97_kids.pkl) codes CV_INCOME_GROSS_YR = -4 (valid
skip) as a zero income. In the 1998-2000 rounds the variable is valid-skipped for most youths still living with a
parent, so its 'pinc_av' averages false zeros into the 1996 value (and 'pinc_pt' carries ~570 false zeros). This
script therefore builds its own extract from the raw NLSY97 csv (usecols only) and saves it under new names:
  data/nlsy97_ap_kids.pkl          one row per respondent (all race / ethnicity groups) living with a parent figure
                                   in 1997 (CV_YTH_REL_HH_CURRENT 1-6);
  data/nlsy97_ap_person_year.pkl   respondent x round, all rounds.
  Parental income (2000 dollars of the income year):
    one-year   = CV_INCOME_GROSS_YR in 1997 = gross household income of 1996 (parent interview for 98% of cases);
                 -4 / -1 / -2 / -3 / -5 = missing; true zeros kept (dropped by the log, kept by the ranks);
    multi-year = mean of the 1997-2000 rounds (incomes of 1996-99) while the youth lives with a parent figure, the
                 1997 value required. CAUTION: after 1997 the household income is reported by the youth and is
                 collected mainly for youths aged 18+ (1998: 743 of 7,684 youths at home; 2000: 2,370 of 6,562),
                 it includes the youth's own income, and its log correlation with the 1996 parent report is only
                 0.54-0.60. The multi-year measure is therefore (i) available for a selected (older) subsample and
                 (ii) a noisier report, not a classical-error-reducing average of parent reports.
  Parent's age A = mother's age at the youth's birth + the youth's age in 1997 (CV_BIO_MOM_AGE_YOUTH); missing for
  ~6% (no biological-mother age): A set to 45 and a missing-A dummy added (kept, not dropped).
  Child outcomes by round (age = age at the interview, income = previous calendar year, as in the PSID scripts):
    family income CV_INCOME_FAMILY (2004+); own earnings = wages and salary (YINC-1700, -4 = no wage income = 0) +
    business income (YINC-2100), as 3.NLSY97.py; annual hours = CVC_HOURS_WK_YR_ALL of the income year (all jobs);
    hourly wage = earnings / hours; partnered = CV_MARSTAT married spouse present or cohabiting; degree =
    CV_HIGHEST_DEGREE_EVER(_EDT) of the round and CVC_HIGHEST_DEGREE_EVER (final, as of the last interview);
    child-year weight = SAMPLING_WEIGHT_CC of the round (cross-sectional, cumulative cases).
  Yearly amounts outside $100-$150,000 of 1967 (= $516-$773,413 of 2000) dropped from the logs (6.IGEMain.py).
  Race: Black / 'White' = non-Black non-Hispanic (the NLSY97 category, CV race-ethnicity code 4); Hispanic and mixed
  race enter only the pooled rows and the national ranks.

DEFINITIONS (same as 26.IGEByAge.py; its regression engine and test logic are imported).
  Bands 25-29, 30-34, 35-39, 40-44 (the 40-44 band holds ages 40-44 of the 2021 / 2023 rounds: cohorts 1980-83).
  Log IGE, child-year design: all child-years in the band, ln y on ln parental income, quartic in (A - 45)/10 (+
  missing-A dummy), single-year age dummies. Band-mean design: ln of the mean over the band's years (>= 2 rounds),
  A quartic + mean age in the band. Black / White unweighted (as 26), Pooled = all races weighted by the round
  weight (band means: mean weight); also Pooled Black + White (weighted) and race-specific weighted.
  Ranks: parents ranked within birth year on the one-year income (1997 weight, all races in the file); child band
  mean (>= 2 rounds; zeros kept) ranked within birth year and band among all children observed in that band (1997
  weight). Weighted rank-rank slope; E[rank] at parental p25 / p75 from the line (p-value against 50).
  Inference: every band x group cell is its own regression; the joint covariance is the cluster-robust sandwich of
  the stacked, fully interacted regression, clusters = 1997 household (siblings), so the same child in several bands
  is accounted for. Tests across the four bands: Wald test of equality, linear trend per 10 years of the band
  midpoint, mean at >= 35 minus mean at < 35 (written in this direction here; 26 printed < 35 minus >= 35).
  Balanced: children with the outcome in every band of 25-29 ... 35-39 ('balanced 25-39') or of 25-29 ... 40-44
  ('balanced 25-44'); ranks recomputed among them.
MECHANISM (NLSY97).
  1 Haider-Solon: children observed in both bands of a pair (25-29 -> 35-39, 30-34 -> 40-44, 25-29 -> 40-44): mean
    ln y in each band and its change regressed on ln parental income (controls: A quartic, missing-A, the change in
    mean age). Outcomes: ln earnings, ln family income; and on one common child-year sample (earnings and hours valid:
    hours >= 100, wage $2-$200 of 2000) ln earnings = ln hours + ln wage, so the earnings gradient splits exactly into
    an hours and a wage gradient.
  2 Education: final degree on ln parental income (LPM); the band IGE and the growth gradient with and without final
    degree dummies (none, GED, high school, AA, BA, graduate).
  3 Marriage: partnered (LPM) by band; family-income IGE with and without a partnered control; own earnings IGE; the
    family-income growth gradient with the partnered share in both bands as controls.
RELIABILITY. (a) One-year vs multi-year parental income on the same children (>= 2 parental years); the stacked
  regression gives the covariance of the two, so their difference is tested. (b) The reliability-corrected profile
  b / RR with RR treated as known: (i) 0.57 for every group (PSID one-year family income, EVIDENCE 1.6); (ii) the
  PSID race-specific one-year ratios of 4.Estimates.py; (iii) the NLSY97 child-generation one-year ratios of
  4.Estimates.py (output/ige_estimates.csv).
COMPARISON. The same log IGE (child-year) and rank blocks are run on the PSID and NLSY79 frames of 26.IGEByAge.py
  restricted to the same four bands, so the tests use the same bands in all three data sets. Parental income differs
  by data set (PSID: mean at child ages 13-19, >= 3 years; NLSY79: 1978-80 mean; NLSY97: 1996, one year).
Writes output/nlsy97_age_profile.csv (every estimate), output/nlsy97_age_profile.md, output/nlsy97_age_profile.png.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2, norm

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CPI, DATA, OUT, nls_pick, stars, to2000  # noqa: E402
import os
DROPBOX = Path(os.environ.get("DROPBOX", Path.home() / "Dropbox"))   # raw data, read only

_spec = importlib.util.spec_from_file_location("ige26", Path(__file__).resolve().parent / "26.IGEByAge.py")
ige26 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ige26)
Cells, cell, rank_in = ige26.Cells, ige26.cell, ige26.rank_in

SRC = Path(DROPBOX / "NLS/nlsy97_all_1997-2023")
CSV = SRC / "nlsy97_all_1997-2023.csv"
KIDS, PY = DATA / "nlsy97_ap_kids.pkl", DATA / "nlsy97_ap_person_year.pkl"
LO, HI = (v * CPI[2000] / CPI[1967] for v in (100, 150_000))
RACE = {1: "Black", 2: "Hispanic", 3: "Mixed", 4: "White"}
BL = ["25-29", "30-34", "35-39", "40-44"]
BANDS = [(25, 29), (30, 34), (35, 39), (40, 44)]
MID = dict(zip(BL, [27, 32, 37, 42]))
BAL = {"unbalanced": BL, "balanced 25-39": BL[:3], "balanced 25-44": BL}
RACES = ("Black", "White")
A4 = [f"A{n}" for n in range(1, 5)]
PAIRS = [("25-29", "35-39"), ("30-34", "40-44"), ("25-29", "40-44")]
DEG = {0: "none", 1: "GED", 2: "HS", 3: "AA", 4: "BA", 5: "grad", 6: "grad", 7: "grad"}
PG, PBW = "Pooled (weighted)", "Pooled B+W (weighted)"
GROUPS = (PG, PBW, "Black", "White", "White - Black")
FAM, ERN = "ln family income", "ln own earnings"
ROWS = []


def record(**k):
    ROWS.append(k)


# ================================================================ extract
def money(x, zero_skip):
    """NLS amounts; -4 -> 0 only where a valid skip means 'no such income' (earnings), else missing."""
    x = pd.to_numeric(x, errors="coerce").astype(float)
    return x.where(x >= 0, np.where((x == -4) & zero_skip, 0.0, np.nan))


def build_extract():
    ix = pd.read_csv(DATA / "nlsy97_codebook.csv", low_memory=False, dtype={"year": str})
    pick = lambda q: nls_pick(ix, q)  # noqa: E731
    m = {"age": pick(["CV_AGE_INT_DATE"]), "rel": pick(["CV_YTH_REL_HH_CURRENT"]),
         "gross": pick(["CV_INCOME_GROSS_YR"]), "fam": pick(["CV_INCOME_FAMILY"]), "wage": pick(["YINC-1700"]),
         "bus": pick(["YINC-2100"]), "mar": pick(["CV_MARSTAT"]),
         "deg": pick(["CV_HIGHEST_DEGREE_EVER_EDT", "CV_HIGHEST_DEGREE_EVER"]), "wt": pick(["SAMPLING_WEIGHT_CC"])}
    hrs = ix[ix["qname"].astype(str).str.startswith("CVC_HOURS_WK_YR_ALL.")].copy()
    hrs["yy"] = hrs["qname"].str[-2:].astype(int)
    hrs["cal"] = np.where(hrs["yy"] <= 30, 2000 + hrs["yy"], 1900 + hrs["yy"])
    hrs = dict(zip(hrs["cal"], hrs["col"]))
    keep = {"R0000100": "pid", "R0536300": "sex", "R0536402": "birth_year", "R1482600": "race_eth",
            "R1235800": "cross", "R1236101": "wt97", "R1193000": "hhid", "R1200200": "mom_age_birth",
            "R1204600": "inc_src97", "Z9083900": "deg_final"}
    cols = list(dict.fromkeys(list(keep) + [c for d in m.values() for c in d.values()]
                              + [hrs[y] for y in range(1996, 2023) if y in hrs]))
    print(f"reading {len(cols)} columns of the NLSY97 csv ...", flush=True)
    d = pd.read_csv(CSV, usecols=cols)
    d = d.assign(**{v: d[c] for c, v in keep.items()})          # renamed copies; raw columns kept for the rounds
    d = d[d["race_eth"].isin(list(RACE))].copy()
    rows = []
    for y in sorted(m["age"]):
        g = lambda k: d[m[k][y]] if y in m[k] else pd.Series(np.nan, index=d.index)  # noqa: E731
        x = pd.DataFrame({"pid": d["pid"].values, "round": y,
                          "age": pd.to_numeric(g("age"), errors="coerce").where(lambda s: s > 0).values})
        x["gross"] = to2000(money(g("gross"), False).values, y - 1)
        x["faminc"] = to2000(money(g("fam"), False).values, y - 1)
        x["earn"] = to2000(money(g("wage"), True).values + np.nan_to_num(money(g("bus"), True).values), y - 1)
        x["hours"] = (pd.to_numeric(d[hrs[y - 1]], errors="coerce").where(lambda s: s >= 0).values
                      if (y - 1) in hrs else np.nan)
        mar = pd.to_numeric(g("mar"), errors="coerce")
        x["partnered"] = mar.isin([1, 3, 5, 7, 9]).astype(float).where(mar > 0).values
        x["deg"] = pd.to_numeric(g("deg"), errors="coerce").where(lambda s: s >= 0).values
        x["wt_r"] = pd.to_numeric(g("wt"), errors="coerce").where(lambda s: s > 0).values
        x["with_parent"] = g("rel").between(1, 6).values
        rows.append(x)
    L = pd.concat(rows, ignore_index=True)
    k = d.set_index("pid")[["sex", "birth_year", "race_eth", "cross", "wt97", "hhid", "mom_age_birth", "inc_src97",
                            "deg_final"]].copy()
    k["race"], k["female"] = k["race_eth"].map(RACE), (k["sex"] == 2) * 1
    k["deg_final"] = k["deg_final"].where(k["deg_final"] >= 0)
    P = L[L["round"].between(1997, 2000)].pivot(index="pid", columns="round", values="gross")
    W = L[L["round"].between(1997, 2000)].pivot(index="pid", columns="round", values="with_parent").astype(bool)
    k["age97"] = L[L["round"] == 1997].set_index("pid")["age"]
    k["par1997"] = W[1997]
    for y in range(1997, 2001):
        k[f"p{y - 1}"] = P[y].where(W[y])
    pa = k[[f"p{y}" for y in range(1996, 2000)]]
    k["pinc_pt"] = k["p1996"]
    k["n_av"] = pa.notna().sum(axis=1).where(k["p1996"].notna(), 0)
    k["pinc_av"] = pa.mean(axis=1).where(k["p1996"].notna())
    k["off_av"] = pa.notna().mul(np.arange(4)).sum(axis=1) / k["n_av"].replace(0, np.nan)
    mab = k["mom_age_birth"].where(k["mom_age_birth"].between(10, 60))
    k["page_pt"] = mab + k["age97"]
    k["page_av"] = k["page_pt"] + k["off_av"].fillna(0)
    k = k[k["par1997"]].reset_index()
    L = L[L["pid"].isin(k["pid"])]
    k.to_pickle(KIDS)
    L.to_pickle(PY)
    return k, L


def load_extract(rebuild=False):
    if rebuild or not (KIDS.exists() and PY.exists()):
        return build_extract()
    return pd.read_pickle(KIDS), pd.read_pickle(PY)


def band_of(age):
    out = pd.Series(pd.NA, index=age.index, dtype="object")
    for (a, b), lab in zip(BANDS, BL):
        out[age.between(a, b)] = lab
    return out


def nlsy97_frames(k, L):
    """child-year frame s (ages 25-44) and rank frame r0 in the column conventions of 26.IGEByAge.py."""
    k = k.copy()
    k["fam68"] = k["hhid"]
    k["lyp_pt"] = np.log(k["pinc_pt"].where(k["pinc_pt"].between(LO, HI)))
    k["lyp_av"] = np.log(k["pinc_av"].where(k["pinc_av"].between(LO, HI)))
    k["Amiss"] = k["page_pt"].isna().astype(float)
    for n in range(1, 5):
        k[f"A{n}"] = ((k["page_pt"].fillna(45) - 45) / 10) ** n
    k["degc"] = k["deg_final"].map(DEG)
    k["ba"] = (k["deg_final"] >= 4).astype(float).where(k["deg_final"].notna())
    k["w"] = k["wt97"].astype(float)
    q = L[L["age"].between(25, 44)].copy()
    s = q.merge(k[["pid", "race", "female", "birth_year", "fam68", "lyp_pt", "lyp_av", "n_av", "Amiss", "degc",
                   "ba", "w", *A4]], on="pid")
    s["lyp"] = s["lyp_pt"]
    s["lfam"] = np.log(s["faminc"].where(s["faminc"].between(LO, HI)))
    s["learn"] = np.log(s["earn"].where(s["earn"].between(LO, HI)))
    wage = s["earn"] / s["hours"]
    v = s["earn"].between(LO, HI) & (s["hours"] >= 100) & wage.between(2, 200)
    s["learn_v"] = s["learn"].where(v)
    s["lhrs_v"] = np.log(s["hours"].where(v))
    s["lwage_v"] = np.log(wage.where(v))
    s["wt"] = s["wt_r"]
    s["band"], s["agei"] = band_of(s["age"]), s["age"].round().astype(int)
    s = s[s["band"].notna()]
    # rank frame
    kr = k.set_index("pid")
    kr["pinc"] = kr["pinc_pt"]
    kr["rp"] = rank_in(kr, "pinc", "birth_year")
    out = []
    for lab, (lo, hi) in zip(BL, BANDS):
        h = q[q["age"].between(lo, hi)]
        f = h.dropna(subset=["faminc"]).groupby("pid")["faminc"].agg(["mean", "count"])
        e = h.dropna(subset=["earn"]).groupby("pid")["earn"].agg(["mean", "count"])
        x = kr[["birth_year", "w", "rp", "race", "female", "fam68", "pinc"]].copy()
        x["yf"] = f.loc[f["count"] >= 2, "mean"].reindex(x.index)
        x["ye"] = e.loc[e["count"] >= 2, "mean"].reindex(x.index)
        x["band"] = lab
        out.append(x)
    r0 = pd.concat(out).rename_axis("pid").reset_index()
    return s, k, r0


# ================================================================ tests
def tests(R, bands, term, scale=None):
    """term(b) -> list of (cell, name, weight). Wald equality, trend per 10 yrs, mean >=35, <35, difference."""
    bands = [b for b in bands if all(R.has(t[0]) for t in term(b))]
    out = []
    if len(bands) >= 2:
        st, df, p = R.wald([term(b) + [(t[0], t[1], -t[2]) for t in term(bands[0])] for b in bands[1:]])
        out.append(("Equal in all bands (Wald chi2)", st, np.nan, p, f"chi2({df})={st:.2f}"))
        mm = np.array([MID[b] for b in bands], float)
        c = (mm - mm.mean()) / ((mm - mm.mean()) ** 2).sum() * 10
        e, se, p = R.lin([(t[0], t[1], t[2] * cw) for b, cw in zip(bands, c) for t in term(b)])
        out.append(("Linear trend per 10 years", e, se, p, ""))
    early, late = [b for b in bands if MID[b] < 35], [b for b in bands if MID[b] >= 35]
    if early and late:
        E = [(t[0], t[1], t[2] / len(early)) for b in early for t in term(b)]
        La = [(t[0], t[1], t[2] / len(late)) for b in late for t in term(b)]
        for nm, tt in (("Mean in bands < 35", E), ("Mean in bands >= 35", La),
                       ("Mean >= 35 minus mean < 35", La + [(t[0], t[1], -t[2]) for t in E])):
            e, se, p = R.lin(tt)
            out.append((nm, e, se, p, ""))
    return out


TESTNAMES = ["Equal in all bands (Wald chi2)", "Linear trend per 10 years", "Mean in bands < 35",
             "Mean in bands >= 35", "Mean >= 35 minus mean < 35"]


def race_term(race, scale=1.0):
    return lambda b: [((b, race), "x", scale)]


def gap_term(sW=1.0, sB=1.0, name="x"):
    return lambda b: [((b, "White"), name, sW), ((b, "Black"), name, -sB)]


def pool_term(scale=1.0):
    return lambda b: [(b, "x", scale)]


def record_tests(R, bands, term, **meta):
    for t, e, se, p, txt in tests(R, bands, term):
        record(**meta, band="test", stat=t, est=e, se=se, p=p, note=txt)


# ================================================================ blocks
def band_means(x, y, raw, bands, ctrl, extra_first=()):
    out = []
    for lab in bands:
        h = x[(x["band"] == lab) & x[y].notna()]
        g = h.groupby("pid")
        mm = pd.DataFrame({"m": g[raw].mean(), "n": g[raw].count(), "agem": g["age"].mean(), "wt": g["wt"].mean()})
        mm = mm[mm["n"] >= 2].join(g[["lyp", "race", "fam68", *ctrl, *extra_first]].first())
        mm["yy"] = np.log(mm["m"])
        mm["agec"] = mm["agem"] - MID[lab]
        mm["band"] = mm["cell"] = lab
        out.append(mm)
    return pd.concat(out).reset_index()


def race_cells(st):
    return st[st["race"].isin(RACES)].assign(rc=lambda q: list(zip(q["cell"], q["race"])))


def logige(data, s, sexes, outcomes, ctrl, designs=("child-year",), samples=BAL, label=None, store=None):
    """band log IGE by sex x outcome x sample x design; groups of GROUPS; tests."""
    for sex, fem in sexes.items():
        x0 = s[s["female"].isin(fem)]
        for yname, ylab, raw in outcomes:
            x = x0[x0[yname].notna()]
            for design in designs:
                for smp, bands in samples.items():
                    if design == "child-year":
                        st = x[x["band"].isin(bands)].assign(cell=lambda q: q["band"])
                        yy, cc, fe = yname, ctrl, "agei"
                        ok = st.groupby("pid")["band"].nunique()
                    else:
                        st = band_means(x, yname, raw, bands, ctrl)
                        yy, cc, fe = "yy", ctrl + ["agec"], None
                        ok = st.groupby("pid")["band"].nunique()
                    if smp != "unbalanced":
                        st = st[st["pid"].isin(ok[ok == len(bands)].index)]
                    an = label or f"log IGE, {design}"
                    Rr = Cells(race_cells(st), yy, "lyp", "rc", cc, fe)
                    Rw = Cells(race_cells(st), yy, "lyp", "rc", cc, fe, w="wt")
                    Rp = Cells(st, yy, "lyp", "cell", cc, fe, w="wt")
                    Rb = Cells(st[st["race"].isin(RACES)], yy, "lyp", "cell", cc, fe, w="wt")
                    if store is not None:
                        store[(data, sex, ylab, smp, design)] = (Rr, Rp)
                    meta = dict(data=data, analysis=an, sex=sex, sample=smp, outcome=ylab)
                    for b in bands:
                        for grp, R, c in ((PG, Rp, b), (PBW, Rb, b)):
                            if R.has(c):
                                e, se, p = R.lin([(c, "x", 1)])
                                record(**meta, band=b, group=grp, stat="IGE", est=e, se=se, p=p, **R.info[c])
                        for R, suf in ((Rr, ""), (Rw, " (weighted)")):
                            for g in RACES:
                                if R.has((b, g)):
                                    e, se, p = R.lin([((b, g), "x", 1)])
                                    record(**meta, band=b, group=g + suf, stat="IGE", est=e, se=se, p=p,
                                           **R.info[(b, g)])
                            if R.has((b, "White")) and R.has((b, "Black")):
                                e, se, p = R.lin(gap_term()(b))
                                record(**meta, band=b, group="White - Black" + suf, stat="IGE", est=e, se=se, p=p,
                                       n=R.info[(b, "White")]["n"] + R.info[(b, "Black")]["n"])
                    for grp, R, term in ((PG, Rp, pool_term()), (PBW, Rb, pool_term()), ("Black", Rr, race_term("Black")),
                                         ("White", Rr, race_term("White")), ("White - Black", Rr, gap_term()),
                                         ("White - Black (weighted)", Rw, gap_term())):
                        record_tests(R, bands, term, **meta, group=grp)


def rank_block(data, r0, sexes, ycols):
    for smp, bands in BAL.items():
        mem = None
        if smp != "unbalanced":
            okk = r0[r0["band"].isin(bands) & r0["yf"].notna() & r0["rp"].notna() & (r0["w"] > 0)]
            c = okk.groupby("pid")["band"].nunique()
            mem = set(c[c == len(bands)].index)
        r = r0[r0["band"].isin(bands)]
        r = r.copy() if mem is None else r[r["pid"].isin(mem)].copy()
        for y in ("yf", "ye"):
            r["r" + y] = rank_in(r, y, ["birth_year", "band"])
        for sex, fem in sexes.items():
            x = r[r["female"].isin(fem)].assign(cell=lambda q: q["band"])
            for yc, ylab in ycols:
                d = x.dropna(subset=["rp", "r" + yc])
                Rr = Cells(race_cells(d), "r" + yc, "rp", "rc", w="w")
                Rp = Cells(d, "r" + yc, "rp", "cell", w="w")
                meta = dict(data=data, analysis="rank", sex=sex, sample=smp, outcome=ylab)
                for b in bands:
                    for grp, R, c in ((PG, Rp, b), ("Black", Rr, (b, "Black")), ("White", Rr, (b, "White"))):
                        if not R.has(c):
                            continue
                        for stt, c0, cx in (("slope", 0, 1), ("E[rank] p25", 1, 25), ("E[rank] p75", 1, 75)):
                            e, se, p = R.lin([(c, "const", c0), (c, "x", cx)] if c0 else [(c, "x", cx)])
                            if c0:
                                p = 2 * (1 - norm.cdf(abs(e - 50) / se))
                            record(**meta, band=b, group=grp, stat=stt, est=e, se=se, p=p, **R.info[c])
                    if Rr.has((b, "White")) and Rr.has((b, "Black")):
                        for stt, c0, cx in (("slope", 0, 1), ("E[rank] p25", 1, 25), ("E[rank] p75", 1, 75)):
                            e, se, p = Rr.lin(ige26.gap_terms(b, c0=c0, cx=cx))
                            record(**meta, band=b, group="White - Black", stat=stt, est=e, se=se, p=p,
                                   n=Rr.info[(b, "White")]["n"] + Rr.info[(b, "Black")]["n"])
                for grp, R, term in ((PG, Rp, pool_term()), ("Black", Rr, race_term("Black")),
                                     ("White", Rr, race_term("White")), ("White - Black", Rr, gap_term())):
                    record_tests(R, bands, term, **{**meta, "outcome": ylab + " | slope"}, group=grp)
                p25 = lambda b: [((b, "White"), "const", 1), ((b, "White"), "x", 25),  # noqa: E731
                                 ((b, "Black"), "const", -1), ((b, "Black"), "x", -25)]
                record_tests(Rr, bands, p25, **{**meta, "outcome": ylab + " | E[rank] p25"}, group="White - Black")


def growth_block(data, s, outcomes, ctrl, extra=None, tag="", sample_fn=None):
    """Haider-Solon: mean ln y by band for children in both bands; (1) early, (2) late, (3) change."""
    extra = extra or {}
    for sex, fem in (("Sons", [0]), ("Daughters", [1])):
        x = s[s["female"] == fem[0]]
        for yname, ylab in outcomes:
            h = x[x[yname].notna()] if sample_fn is None else sample_fn(x)
            aggs = dict(y=(yname, "mean"), agem=("age", "mean"), wt=("wt", "mean"))
            for k_, v_ in extra.get("band_vars", {}).items():
                aggs[k_] = (v_, "mean")
            m = h.groupby(["pid", "band"]).agg(**aggs)
            ch = h.groupby("pid")[["lyp", "race", "fam68", *ctrl, *extra.get("child_vars", [])]].first()
            for e0, e1 in PAIRS:
                try:
                    a, b = m.xs(e0, level="band"), m.xs(e1, level="band")
                except KeyError:
                    continue
                d = a.join(b, lsuffix="0", rsuffix="1", how="inner").join(ch)
                d["dy"], d["dage"] = d["y1"] - d["y0"], d["agem1"] - d["agem0"]
                d["wt"] = d[["wt0", "wt1"]].mean(axis=1)
                d = d.reset_index()
                xc = list(extra.get("ctrl_cols", []))
                for col, lab in (("y0", f"IGE at {e0}"), ("y1", f"IGE at {e1}"), ("dy", "Growth gradient")):
                    cc = ctrl + (["dage"] if col == "dy" else []) + xc
                    Rr = Cells(d[d["race"].isin(RACES)], col, "lyp", "race", cc)
                    Rp = Cells(d.assign(one="all"), col, "lyp", "one", cc, w="wt")
                    meta = dict(data=data, analysis="growth" + tag, sex=sex, sample=f"{e0} -> {e1}", band=lab,
                                outcome=ylab, stat=col)
                    for grp, R, c in ((PG, Rp, "all"), ("Black", Rr, "Black"), ("White", Rr, "White")):
                        if R.has(c):
                            e, se, p = R.lin([(c, "x", 1)])
                            record(**meta, group=grp, est=e, se=se, p=p, **R.info[c])
                    if Rr.has("White") and Rr.has("Black"):
                        e, se, p = Rr.lin([("White", "x", 1), ("Black", "x", -1)])
                        record(**meta, group="White - Black", est=e, se=se, p=p,
                               n=Rr.info["White"]["n"] + Rr.info["Black"]["n"])


def degree_dummies(s):
    s = s.copy()
    for lab in ("GED", "HS", "AA", "BA", "grad"):
        s["d_" + lab] = (s["degc"] == lab).astype(float).where(s["degc"].notna())
    return s


DD = ["d_GED", "d_HS", "d_AA", "d_BA", "d_grad"]


def cross_section(data, k, ctrl):
    """final degree on ln parental income (LPM), by sex and race."""
    k = degree_dummies(k.assign(lyp=k["lyp_pt"]))
    k["hs_plus"] = (k["deg_final"] >= 2).astype(float).where(k["deg_final"].notna())
    for sex, fem in (("Sons", [0]), ("Daughters", [1])):
        x = k[k["female"].isin(fem)].assign(one="all", cellr=lambda q: q["race"])
        for y, lab in (("ba", "BA or more"), ("hs_plus", "High-school diploma or more"), ("d_GED", "GED")):
            Rr = Cells(x[x["race"].isin(RACES)], y, "lyp", "cellr", ctrl)
            Rp = Cells(x, y, "lyp", "one", ctrl, w="w")
            meta = dict(data=data, analysis="degree", sex=sex, sample="children", band="final", outcome=lab,
                        stat="coef on ln parental income")
            for grp, R, c in ((PG, Rp, "all"), ("Black", Rr, "Black"), ("White", Rr, "White")):
                e, se, p = R.lin([(c, "x", 1)])
                record(**meta, group=grp, est=e, se=se, p=p, **R.info[c])
            e, se, p = Rr.lin([("White", "x", 1), ("Black", "x", -1)])
            record(**meta, group="White - Black", est=e, se=se, p=p)
            for grp, xx in ((PG, x), ("Black", x[x["race"] == "Black"]), ("White", x[x["race"] == "White"])):
                xx = xx[xx[y].notna()]
                wv = xx["w"] if grp == PG else None
                record(**{**meta, "stat": "mean"}, group=grp, est=np.average(xx[y], weights=wv), se=np.nan,
                       p=np.nan, n=len(xx))


def reliability_block(data, s, sexes, ctrl):
    """one-year vs multi-year on the same children (n_av >= 2), stacked so the difference is tested."""
    x0 = s[(s["n_av"] >= 2) & s["lyp_pt"].notna() & s["lyp_av"].notna()]
    for sex, fem in sexes.items():
        for yname, ylab in (("lfam", FAM), ("learn", ERN)):
            x = x0[x0["female"].isin(fem) & x0[yname].notna()]
            parts = []
            for meas, col in (("1y", "lyp_pt"), ("my", "lyp_av")):
                parts.append(x.assign(lyp=x[col], cell=[(b, meas) for b in x["band"]]))
            st = pd.concat(parts, ignore_index=True)
            st["rc"] = [((b, m_), r) for (b, m_), r in zip(st["cell"], st["race"])]
            Rr = Cells(st[st["race"].isin(RACES)], yname, "lyp", "rc", ctrl, "agei")
            Rp = Cells(st, yname, "lyp", "cell", ctrl, "agei", w="wt")
            meta = dict(data=data, analysis="reliability: 1-year vs multi-year", sex=sex, sample="n_av >= 2",
                        outcome=ylab)
            for b in BL:
                for meas, mlab in (("1y", "one-year 1996"), ("my", "multi-year 1996-99")):
                    c = (b, meas)
                    if Rp.has(c):
                        e, se, p = Rp.lin([(c, "x", 1)])
                        record(**meta, band=b, group=PG, stat=mlab, est=e, se=se, p=p, **Rp.info[c])
                    for g in RACES:
                        if Rr.has((c, g)):
                            e, se, p = Rr.lin([((c, g), "x", 1)])
                            record(**meta, band=b, group=g, stat=mlab, est=e, se=se, p=p, **Rr.info[(c, g)])
                    if Rr.has((c, "White")) and Rr.has((c, "Black")):
                        e, se, p = Rr.lin([((c, "White"), "x", 1), ((c, "Black"), "x", -1)])
                        record(**meta, band=b, group="White - Black", stat=mlab, est=e, se=se, p=p)
                # difference multi - one
                if Rp.has((b, "my")) and Rp.has((b, "1y")):
                    e, se, p = Rp.lin([((b, "my"), "x", 1), ((b, "1y"), "x", -1)])
                    record(**meta, band=b, group=PG, stat="multi-year minus one-year", est=e, se=se, p=p)
                for g in RACES:
                    if Rr.has(((b, "my"), g)) and Rr.has(((b, "1y"), g)):
                        e, se, p = Rr.lin([(((b, "my"), g), "x", 1), (((b, "1y"), g), "x", -1)])
                        record(**meta, band=b, group=g, stat="multi-year minus one-year", est=e, se=se, p=p)
                if all(Rr.has(((b, m_), g)) for m_ in ("1y", "my") for g in RACES):
                    e, se, p = Rr.lin([(((b, "my"), "White"), "x", 1), (((b, "my"), "Black"), "x", -1),
                                       (((b, "1y"), "White"), "x", -1), (((b, "1y"), "Black"), "x", 1)])
                    record(**meta, band=b, group="White - Black", stat="multi-year minus one-year", est=e, se=se,
                           p=p)
            for meas, mlab in (("1y", "one-year 1996"), ("my", "multi-year 1996-99")):
                term = lambda b, m_=meas: [(((b, m_), "White"), "x", 1), (((b, m_), "Black"), "x", -1)]  # noqa: E731
                for t, e, se, p, txt in tests(Rr, BL, term):
                    record(**meta, band="test", group="White - Black", stat=f"{mlab}: {t}", est=e, se=se, p=p,
                           note=txt)
                pterm = lambda b, m_=meas: [((b, m_), "x", 1)]  # noqa: E731
                for t, e, se, p, txt in tests(Rp, BL, pterm):
                    record(**meta, band="test", group=PG, stat=f"{mlab}: {t}", est=e, se=se, p=p, note=txt)


def rr_values():
    e = pd.read_csv(OUT / "ige_estimates.csv")
    e = e[(e["parent"] == "one year at 16") & (e["sex"] == "Men") & (e["outcome"] == "Own earnings")]
    get = lambda d, r: float(e[(e["data"] == d) & (e["race"] == r)]["rr"].iloc[0])  # noqa: E731
    return {"common 0.57 (PSID one-year)": {"Black": 0.57, "White": 0.57, PG: 0.57},
            "PSID race-specific (4.Estimates)": {"Black": get("PSID", "Black"), "White": get("PSID", "White"),
                                                 PG: get("PSID", "All")},
            "NLSY97 race-specific (4.Estimates)": {"Black": get("NLSY97", "Black"), "White": get("NLSY97", "White"),
                                                   PG: get("NLSY97", "All")}}


def corrected_block(store, rrs):
    for (data, sex, ylab, smp, design), (Rr, Rp) in store.items():
        if data != "NLSY97" or smp != "unbalanced" or design != "child-year":
            continue
        for scheme, rr in rrs.items():
            meta = dict(data=data, analysis="corrected log IGE", sex=sex, sample=scheme, outcome=ylab)
            for b in BL:
                for grp, R, c in ((PG, Rp, b), ("Black", Rr, (b, "Black")), ("White", Rr, (b, "White"))):
                    if R.has(c):
                        e, se, p = R.lin([(c, "x", 1 / rr[grp])])
                        record(**meta, band=b, group=grp, stat="IGE / RR", est=e, se=se, p=p)
                if Rr.has((b, "White")) and Rr.has((b, "Black")):
                    e, se, p = Rr.lin(gap_term(1 / rr["White"], 1 / rr["Black"])(b))
                    record(**meta, band=b, group="White - Black", stat="IGE / RR", est=e, se=se, p=p)
            record_tests(Rr, BL, gap_term(1 / rr["White"], 1 / rr["Black"]), **meta, group="White - Black")
            record_tests(Rp, BL, pool_term(1 / rr[PG]), **meta, group=PG)


# ================================================================ output helpers
KEYS = ["data", "analysis", "sex", "sample", "band", "group", "outcome", "stat"]
RESD = {}


def get(*key):
    return RESD.get(key)


def c_(r, dec=3):
    return "" if r is None or not np.isfinite(r.est) else cell(r.est, r.se, r.p, dec)


def n_(r_list):
    out = []
    for g, r in r_list:
        if r is not None and np.isfinite(r.get("children", np.nan)):
            out.append(f"{g[0]} {int(r.n):,} / {int(r.children):,} / {int(r.clusters):,}")
    return "; ".join(out)


def header(cols):
    cols = [h.replace(" | ", " given ") for h in cols]
    return ["| | " + " | ".join(f"({i + 1}) {h}" for i, h in enumerate(cols)) + " |", "|---" * (len(cols) + 1) + "|"]


def prof(dt, an, sex, smp, outcome, stat, group, dec=3):
    """'b1 / b2 / b3 / b4' over the bands, stars attached."""
    out = []
    for b in BL:
        r = get(dt, an, sex, smp, b, group, outcome, stat)
        out.append("--" if r is None else f"{r.est:.{dec}f}{stars(r.p)}")
    return " / ".join(out)


def tst(dt, an, sex, smp, outcome, group, t="Mean >= 35 minus mean < 35"):
    r = get(dt, an, sex, smp, "test", group, outcome, t)
    return "--" if r is None else c_(r)


def summary():
    N, U, A = "NLSY97", "unbalanced", "log IGE, child-year"
    L = ["## Summary (numbers generated from the tables below)", "",
         "Bands 25-29 / 30-34 / 35-39 / 40-44; child-year log IGE; NLSY97 parents = 1996 one-year income.", "",
         "| Statistic | PSID | NLSY79 | NLSY97 |", "|---|---|---|---|"]
    for sex in ("Sons", "Daughters"):
        for g in (PG, "Black", "White", "White - Black"):
            L.append(f"| {sex}, ln family income, {g} | " + " | ".join(prof(dt, A, sex, U, FAM, "IGE", g)
                                                                     for dt in ("PSID", "NLSY79", N)) + " |")
        for g in (PG, "White - Black"):
            L.append(f"| {sex}, ln family income, {g}: mean >= 35 minus < 35 | " + " | ".join(
                tst(dt, A, sex, U, FAM, g) for dt in ("PSID", "NLSY79", N)) + " |")
        L.append(f"| {sex}, ln own earnings, White - Black | " + " | ".join(prof(dt, A, sex, U, ERN, "IGE",
                                                                                "White - Black")
                                                                           for dt in ("PSID", "NLSY79", N)) + " |")
        L.append(f"| {sex}, ln own earnings, White - Black: mean >= 35 minus < 35 | " + " | ".join(
            tst(dt, A, sex, U, ERN, "White - Black") for dt in ("PSID", "NLSY79", N)) + " |")
    for st, dec in (("slope", 3), ("E[rank] p25", 1)):
        L.append(f"| Both sexes, rank {st} (family income), White - Black | " + " | ".join(
            prof(dt, "rank", "Both", U, FAM, st, "White - Black", dec) for dt in ("PSID", "NLSY79", N)) + " |")
    for sex in ("Sons", "Daughters"):
        for o in (ERN, FAM):
            L.append(f"| {sex}, growth gradient 25-29 -> 35-39, {o}: W; B; W - B | " + " | ".join(
                "; ".join("--" if (r := get(dt, "growth", sex, "25-29 -> 35-39", "Growth gradient", g, o, "dy"))
                          is None else f"{r.est:.3f}{stars(r.p)}" for g in ("White", "Black", "White - Black"))
                if dt != "NLSY79" else "" for dt in ("PSID", "NLSY79", N)) + " |")
    L.append("")
    return L


def band_table(cols, bands, groups=GROUPS, rowlab="ln parental income"):
    """cols = [(key-tuple-without-band-group, header, dec)] with key = (data, analysis, sex, sample, outcome, stat)."""
    L = header([h for _, h, _ in cols])
    for b in bands:
        L.append(f"| **Age {b}** |" + " |" * len(cols))
        for g in groups:
            L.append(f"| {rowlab}: {g} | " + " | ".join(
                c_(get(k[0], k[1], k[2], k[3], b, g, k[4], k[5]), d) for k, _, d in cols) + " |")
        L.append("| N obs / children / clusters (B; W) | " + " | ".join(
            n_([(g, get(k[0], k[1], k[2], k[3], b, g, k[4], k[5])) for g in RACES]) for k, _, _ in cols) + " |")
    return L


def test_table(cols, panels):
    """cols = [(data, analysis, sex|None, sample, outcome, header)]; panels = [(label, sex, group)]."""
    L = header([c[-1] for c in cols])
    for lab, sex, g in panels:
        L.append(f"| **{lab}** |" + " |" * len(cols))
        for t in TESTNAMES:
            cells = []
            for dt, an, sx, smp, o, _ in cols:
                r = get(dt, an, sx or sex, smp, "test", g, o, t)
                if r is None:
                    cells.append("")
                elif t.startswith("Equal"):
                    pv = "<0.001" if r.p < 0.001 else f"{r.p:.3f}"
                    cells.append(f"{r.note}{stars(r.p)} (p={pv})")
                else:
                    cells.append(c_(r))
            if any(cells):
                L.append(f"| {t} | " + " | ".join(cells) + " |")
    return L


# ================================================================ markdown
def write_md(k, s, cover):
    N = "NLSY97"
    L = ["# The age profile of intergenerational persistence in the NLSY97, by race (with PSID / NLSY79 comparison)",
         "", "Generated by `29.NLSY97AgeProfile.py` (2026-10-17). Every cell: coefficient (s.e.; p-value), *** p<0.01, "
         "** p<0.05, * p<0.1; s.e. clustered by 1997 household (PSID: 1968 family; NLSY79: 1979 household), joint "
         "across bands (stacked, fully interacted), normal p-values; E[rank] p-values against 50. NLSY97 'White' = "
         "non-Black non-Hispanic. Black / White log IGE unweighted (as `26.IGEByAge.py`); Pooled = all races weighted "
         "by the round's cross-sectional weight; Pooled B+W = Black + White only, weighted; ranks always weighted "
         "(1997 weight). White - Black = difference of the two race regressions. N row: child-years (or child-bands) / "
         "children / clusters for Black (B) and White (W). Age = age at interview; income = previous calendar year. "
         "Parental income (main): 1996 gross household income (1997 parent interview), one year.", ""]
    L += summary()
    L += ["## 0. Data and samples", "",
          "Respondents living with a parent figure in 1997 (born 1980-84). **Correction to the existing extract:** "
          "`3.NLSY97.py` codes CV_INCOME_GROSS_YR = -4 (valid skip) as income 0; in 1998-2000 the variable is "
          "valid-skipped for most youths at home, so `nlsy97_kids.pkl`'s `pinc_av` averages false zeros into the "
          "1996 value (its mean is $27k vs $50k for `pinc_pt`) and `pinc_pt` carries false zeros. This script "
          "treats -4 as missing and saves its own extract (`data/nlsy97_ap_kids.pkl`, `data/nlsy97_ap_person_year.pkl`). "
          "The NLSY97 columns (2)-(3) of `ige_table.md` (parental mean at 12-17) use the contaminated `pinc_av`.", "",
          "Parental income coverage (respondents at home in 1997):", "",
          "| | Black | White | Hispanic | Mixed | All |", "|---|---|---|---|---|---|"]
    for lab, v in cover.items():
        L.append(f"| {lab} | " + " | ".join(str(v.get(g, "")) for g in ("Black", "White", "Hispanic", "Mixed", "All"))
                 + " |")
    L += ["", "Child-years (ln family income) / children by band, unbalanced (with ln parental income):", "",
          "| Band | Sons B | Sons W | Sons all | Daughters B | Daughters W | Daughters all | Rank frame (both sexes, "
          "fam. income) B | W |", "|---" * 9 + "|"]
    for b in BL:
        c = []
        for sex in ("Sons", "Daughters"):
            for g in ("Black", "White", PG):
                r = get(N, "log IGE, child-year", sex, "unbalanced", b, g, FAM, "IGE")
                c.append("" if r is None else f"{int(r.n):,} / {int(r.children):,}")
        for g in RACES:
            r = get(N, "rank", "Both", "unbalanced", b, g, FAM, "slope")
            c.append("" if r is None else f"{int(r.n):,}")
        L.append(f"| {b} | " + " | ".join(c) + " |")
    L.append("")
    an = ["log IGE, child-year", "log IGE, band mean"] * 2
    for smp in BAL:
        L += [f"## 1{'abc'[list(BAL).index(smp)]}. NLSY97 log IGE by age band, {smp}", "",
              "(1)/(3) child-year regressions within the band (A quartic, missing-A dummy, single-year age dummies); "
              "(2)/(4) one row per child, ln of the band mean (>= 2 rounds), A quartic + mean age."
              + (" Balanced: the same children in every band listed." if smp != "unbalanced" else ""), ""]
        for sex in ("Sons", "Daughters"):
            cols = [((N, a, sex, smp, o, "IGE"), h, 3) for a, o, h in
                    zip(an, (FAM, FAM, ERN, ERN), ("ln family income (child-years)", "ln family income (band mean)",
                                                    "ln own earnings (child-years)", "ln own earnings (band mean)"))]
            L += [f"### {sex}", ""] + band_table(cols, BAL[smp]) + [""]
    L += ["## 2. Tests: does the IGE, and the Black-White gap in it, change with age? (NLSY97, child-year design)", "",
          "Rows: Wald test of equality across the bands; linear trend per 10 years of the band midpoint; mean in "
          "bands < 35 (25-29, 30-34), >= 35 (35-39, 40-44), and **>= 35 minus < 35**.", ""]
    for smp in BAL:
        cols = [(N, "log IGE, child-year", None, smp, FAM, "ln family income"),
                (N, "log IGE, child-year", None, smp, ERN, "ln own earnings")]
        panels = [(f"{sx}: {g}", sx, g) for sx in ("Sons", "Daughters")
                  for g in (PG, PBW, "Black", "White", "White - Black", "White - Black (weighted)")]
        L += [f"### {smp}", ""] + test_table(cols, panels) + [""]
    L += ["## 3. NLSY97 rank mobility by age band", "",
          "Child's band-mean family income (or own earnings, zeros kept; >= 2 rounds) ranked within birth year and "
          "band; parents ranked within birth year on 1996 income. (1) rank-rank slope, family income; (2)/(3) "
          "E[rank] at parental p25 / p75; (4) rank-rank slope, own earnings.", ""]
    for smp in BAL:
        L += [f"### 3{'abc'[list(BAL).index(smp)]}. {smp}", ""]
        for sex in ("Both", "Sons", "Daughters"):
            cols = [((N, "rank", sex, smp, FAM, "slope"), "Rank slope, family income", 3),
                    ((N, "rank", sex, smp, FAM, "E[rank] p25"), "E[rank] at p25", 1),
                    ((N, "rank", sex, smp, FAM, "E[rank] p75"), "E[rank] at p75", 1),
                    ((N, "rank", sex, smp, ERN, "slope"), "Rank slope, own earnings", 3)]
            L += [f"#### {'Both sexes' if sex == 'Both' else sex}", ""]
            L += band_table(cols, BAL[smp], groups=(PG, "Black", "White", "White - Black"), rowlab="parent rank")
            L.append("")
        cols = [(N, "rank", None, smp, FAM + " | slope", "Rank slope, family income"),
                (N, "rank", None, smp, FAM + " | E[rank] p25", "E[rank] p25, family income"),
                (N, "rank", None, smp, ERN + " | slope", "Rank slope, own earnings")]
        panels = [(f"{sx}: {g}", sx, g) for sx in ("Both", "Sons", "Daughters")
                  for g in (PG, "Black", "White", "White - Black")]
        L += ["Tests:", ""] + test_table(cols, panels) + [""]
    # ---------------- mechanism
    L += ["## 4. Life-cycle mechanism (NLSY97)", "", "### 4.1 Haider-Solon: growth by parental income", "",
          "Children observed in both bands. One regression per column: (1) mean ln y in the early band, (2) in the "
          "late band, (3) late - early (controls: A quartic, missing-A; (3) also the change in mean age). (3) > 0: "
          "children of richer parents have steeper growth; (3) = the change of the IGE between the two ages in a "
          "fixed sample.", ""]
    for sex in ("Sons", "Daughters"):
        for y in (ERN, FAM):
            L += [f"#### {sex}, {y}", ""] + header(["IGE early band", "IGE late band", "Growth gradient"])
            for e0, e1 in PAIRS:
                smp = f"{e0} -> {e1}"
                keys = ((f"IGE at {e0}", "y0"), (f"IGE at {e1}", "y1"), ("Growth gradient", "dy"))
                L.append(f"| **{smp}** | | | |")
                for g in (PG, "Black", "White", "White - Black"):
                    L.append(f"| ln parental income: {g} | " + " | ".join(
                        c_(get(N, "growth", sex, smp, lab, g, y, st)) for lab, st in keys) + " |")
                L.append("| N children / clusters (B; W) | " + " | ".join(
                    "; ".join(f"{g[0]} {int(r.n):,} / {int(r.clusters):,}" for g in RACES
                              if (r := get(N, "growth", sex, smp, lab, g, y, st)) is not None) for lab, st in keys)
                         + " |")
            L.append("")
    L += ["### 4.2 Hours vs wages: decomposition of the earnings growth gradient", "",
          "Common child-year sample (earnings $516-$773k, annual hours >= 100, hourly wage $2-$200, 2000 dollars): "
          "band means of ln earnings, ln annual hours (CVC_HOURS_WK_YR_ALL, all jobs, income year) and ln hourly "
          "wage (earnings / hours); ln earnings = ln hours + ln wage row by row, so column (1) = (2) + (3) exactly. "
          "Growth gradient (late - early on ln parental income) and, in the second block, the late-band level IGE.",
          ""]
    for sex in ("Sons", "Daughters"):
        L += [f"#### {sex}", ""] + header(["ln earnings (valid hours)", "ln annual hours", "ln hourly wage"])
        for e0, e1 in PAIRS[:2]:
            smp = f"{e0} -> {e1}"
            for lab, st, nm in (("Growth gradient", "dy", "growth gradient"), (f"IGE at {e0}", "y0", f"IGE at {e0}"),
                                (f"IGE at {e1}", "y1", f"IGE at {e1}")):
                L.append(f"| **{smp}: {nm}** | | | |")
                for g in (PG, "Black", "White", "White - Black"):
                    L.append(f"| ln parental income: {g} | " + " | ".join(
                        c_(get(N, "growth (wage sample)", sex, smp, lab, g, o, st)) for o in
                        ("ln earnings (valid)", "ln hours", "ln wage")) + " |")
            r = [get(N, "growth (wage sample)", sex, smp, "Growth gradient", g, "ln wage", "dy") for g in RACES]
            if all(x is not None for x in r):
                L.append(f"| N children (B; W) | {int(r[0].n):,}; {int(r[1].n):,} | | |")
        L.append("")
    L += ["### 4.3 Education (final degree, CVC_HIGHEST_DEGREE_EVER)", "",
          "(a) Final degree on ln parental income (LPM, one row per child; controls A quartic, missing-A). Row "
          "'Mean' = share.", ""]
    L += header(["BA or more", "High-school diploma or more", "GED"])
    for sex in ("Sons", "Daughters"):
        L.append(f"| **{sex}** | | | |")
        for g in (PG, "Black", "White", "White - Black"):
            L.append(f"| ln parental income: {g} | " + " | ".join(
                c_(get(N, "degree", sex, "children", "final", g, o, "coef on ln parental income")) for o in
                ("BA or more", "High-school diploma or more", "GED")) + " |")
        L.append("| Mean (pooled; B; W) | " + " | ".join("; ".join(
            "" if (r := get(N, "degree", sex, "children", "final", g, o, "mean")) is None else f"{r.est:.3f}"
            for g in (PG, "Black", "White")) for o in ("BA or more", "High-school diploma or more", "GED")) + " |")
        r = [get(N, "degree", sex, "children", "final", g, "BA or more", "coef on ln parental income") for g in RACES]
        L.append(f"| N children (B; W) | {int(r[0].n):,}; {int(r[1].n):,} | | |")
    L += ["", "(b) Band IGE (child-years) without and with final-degree dummies (GED, HS, AA, BA, graduate; none = "
          "omitted). Same children (final degree known).", ""]
    for sex in ("Sons", "Daughters"):
        cols = [((N, "log IGE, child-year [deg sample]", sex, "unbalanced", ERN, "IGE"), "ln own earnings", 3),
                ((N, "log IGE | degree", sex, "unbalanced", ERN, "IGE"), "ln own earnings, degree dummies", 3),
                ((N, "log IGE, child-year [deg sample]", sex, "unbalanced", FAM, "IGE"), "ln family income", 3),
                ((N, "log IGE | degree", sex, "unbalanced", FAM, "IGE"), "ln family income, degree dummies", 3)]
        L += [f"#### {sex}", ""] + band_table(cols, BL, groups=(PG, "Black", "White", "White - Black")) + [""]
        cols = [(N, "log IGE, child-year [deg sample]", None, "unbalanced", ERN, "ln own earnings"),
                (N, "log IGE | degree", None, "unbalanced", ERN, "ln own earnings | degree"),
                (N, "log IGE, child-year [deg sample]", None, "unbalanced", FAM, "ln family income"),
                (N, "log IGE | degree", None, "unbalanced", FAM, "ln family income | degree")]
        L += ["Tests:", ""] + test_table(cols, [(f"{sex}: {g}", sex, g) for g in (PG, "White - Black")]) + [""]
    L += ["(c) Growth gradient (25-29 -> 35-39 and 30-34 -> 40-44) without and with final-degree dummies.", ""]
    L += header(["ln own earnings", "ln own earnings, degree dummies", "ln family income",
                 "ln family income, degree dummies"])
    for sex in ("Sons", "Daughters"):
        for e0, e1 in PAIRS[:2]:
            smp = f"{e0} -> {e1}"
            L.append(f"| **{sex}, {smp}** | | | | |")
            for g in (PG, "Black", "White", "White - Black"):
                L.append(f"| ln parental income: {g} | " + " | ".join(
                    c_(get(N, an_, sex, smp, "Growth gradient", g, o, "dy")) for an_, o in
                    (("growth [deg sample]", ERN), ("growth | degree", ERN), ("growth [deg sample]", FAM),
                     ("growth | degree", FAM))) + " |")
    L += ["", "### 4.4 Marriage / partnership", "",
          "(1) partnered (married spouse present or cohabiting; LPM); (2) ln family income IGE; (3) the same with "
          "a partnered control; (4) ln own earnings IGE. Child-years; A quartic, missing-A, single-year age dummies.",
          ""]
    for sex in ("Sons", "Daughters"):
        cols = [((N, "marriage", sex, "unbalanced", "partnered", "IGE"), "Partnered (LPM)", 3),
                ((N, "marriage", sex, "unbalanced", FAM, "IGE"), "ln family income", 3),
                ((N, "marriage", sex, "unbalanced", FAM + " | partnered", "IGE"), "ln family income, partnered control",
                 3), ((N, "marriage", sex, "unbalanced", ERN, "IGE"), "ln own earnings", 3)]
        L += [f"#### {sex}", ""] + band_table(cols, BL, groups=(PG, "Black", "White", "White - Black"))
        sh = []
        for b in BL:
            xx = s[(s["female"] == (sex == "Daughters")) & (s["band"] == b) & s["partnered"].notna()]
            sh.append(f"{b}: " + "; ".join(f"{g} {xx.loc[xx['race'] == g, 'partnered'].mean():.3f}" for g in RACES))
        L += ["", "Share partnered (unweighted) " + " | ".join(sh), ""]
        cols = [(N, "marriage", None, "unbalanced", o, h) for o, h in
                (("partnered", "Partnered"), (FAM, "ln family income"), (FAM + " | partnered", "ln fam. | partnered"),
                 (ERN, "ln own earnings"))]
        L += ["Tests:", ""] + test_table(cols, [(f"{sex}: {g}", sex, g) for g in (PG, "White - Black")]) + [""]
    L += ["(c) Family-income growth gradient without and with the partnered share in both bands as controls.", ""]
    L += header(["ln family income", "ln family income, partnered controls"])
    for sex in ("Sons", "Daughters"):
        for e0, e1 in PAIRS[:2]:
            smp = f"{e0} -> {e1}"
            L.append(f"| **{sex}, {smp}** | | |")
            for g in (PG, "Black", "White", "White - Black"):
                L.append(f"| ln parental income: {g} | " + " | ".join(
                    c_(get(N, an_, sex, smp, "Growth gradient", g, FAM, "dy")) for an_ in
                    ("growth [mar sample]", "growth | partnered")) + " |")
    L.append("")
    # ---------------- reliability
    L += ["## 5. Reliability of the parental measure", "",
          "### 5.1 One-year (1996) vs multi-year (1996-99 at home) parental income, same children", "",
          "Children with the 1996 value and >= 1 further year at home (n_av >= 2; mostly the older 1980-82 cohorts, "
          "whose later years are youth-reported household income). One stacked regression per outcome x sex: column "
          "(1) one-year, (2) multi-year, (3) difference (2) - (1) with its joint s.e. Child-year design.", ""]
    an = "reliability: 1-year vs multi-year"
    for sex in ("Sons", "Daughters"):
        for y in (FAM, ERN):
            cols = [((N, an, sex, "n_av >= 2", y, st), h, 3) for st, h in
                    (("one-year 1996", "one-year 1996"), ("multi-year 1996-99", "multi-year 1996-99"),
                     ("multi-year minus one-year", "multi-year minus one-year"))]
            L += [f"#### {sex}, {y}", ""] + band_table(cols, BL, groups=(PG, "Black", "White", "White - Black"))
            L.append("")
            L += header(["one-year: W - B gap", "multi-year: W - B gap", "one-year: pooled", "multi-year: pooled"])
            for t in TESTNAMES:
                cc = []
                for g, mlab in (("White - Black", "one-year 1996"), ("White - Black", "multi-year 1996-99"),
                                (PG, "one-year 1996"), (PG, "multi-year 1996-99")):
                    r = get(N, an, sex, "n_av >= 2", "test", g, y, f"{mlab}: {t}")
                    if r is None:
                        cc.append("")
                    elif t.startswith("Equal"):
                        cc.append(f"{r.note}{stars(r.p)} (p={'<0.001' if r.p < 0.001 else f'{r.p:.3f}'})")
                    else:
                        cc.append(c_(r))
                L.append(f"| {t} | " + " | ".join(cc) + " |")
            L.append("")
    L += ["### 5.2 Reliability-corrected profile (IGE / RR, RR treated as known)", "",
          "Main NLSY97 child-year estimates (unbalanced, one-year parental income) divided by a reliability ratio: "
          "(1) 0.57 for every group (PSID one-year family income); (2) PSID race-specific one-year ratios; (3) NLSY97 "
          "child-generation race-specific one-year ratios (both from `4.Estimates.py`, `ige_estimates.csv`). "
          "S.e. ignore the sampling error of RR. A common RR rescales the whole profile; race-specific ratios also "
          "move the gap.", ""]
    rrs = rr_values()
    L += ["RR used: " + "; ".join(f"{k_}: B {v['Black']:.3f}, W {v['White']:.3f}, pooled {v[PG]:.3f}"
                                  for k_, v in rrs.items()), ""]
    for sex in ("Sons", "Daughters"):
        for y in (FAM, ERN):
            cols = [((N, "log IGE, child-year", sex, "unbalanced", y, "IGE"), "uncorrected", 3)] + [
                ((N, "corrected log IGE", sex, sch, y, "IGE / RR"), sch, 3) for sch in rrs]
            L += [f"#### {sex}, {y}", ""] + band_table(cols, BL, groups=(PG, "Black", "White", "White - Black"))
            L.append("")
            tc = [(N, "log IGE, child-year", sex, "unbalanced", y, "uncorrected")] + [
                (N, "corrected log IGE", sex, sch, y, sch) for sch in rrs]
            L += test_table(tc, [(f"{sex}: White - Black", sex, "White - Black"), (f"{sex}: {PG}", sex, PG)]) + [""]
    # ---------------- comparison
    L += ["## 6. Comparison with the PSID and NLSY79 (same bands, same definitions)", "",
          "PSID and NLSY79 frames of `26.IGEByAge.py` re-estimated on the four bands 25-29 ... 40-44 only (so the "
          "tests use the same bands). One regression per column and cell; columns = data sets. PSID parents: mean "
          "family income at child ages 13-19 (>= 3 years); NLSY79: 1978-80 mean; NLSY97: 1996 (one year) — the "
          "NLSY97 levels are attenuated relative to the PSID by the shorter parental average (column 4 rescales the "
          "NLSY97 estimate by 1 / 0.57 as a rough bound; the PSID multi-year measure itself has RR ~0.63-0.65). "
          "Pooled: PSID all races weighted, NLSY79 Black + non-Black non-Hispanic weighted (wt79), NLSY97 all races "
          "weighted.", ""]
    for sex in ("Sons", "Daughters"):
        for y in (FAM, ERN):
            cols = [(("PSID", "log IGE, child-year", sex, "unbalanced", y, "IGE"), "PSID", 3),
                    (("NLSY79", "log IGE, child-year", sex, "unbalanced", y, "IGE"), "NLSY79", 3),
                    ((N, "log IGE, child-year", sex, "unbalanced", y, "IGE"), "NLSY97", 3),
                    ((N, "corrected log IGE", sex, "common 0.57 (PSID one-year)", y, "IGE / RR"), "NLSY97 / 0.57", 3)]
            L += [f"### Log IGE, {sex}, {y} (child-years)", ""]
            L += band_table(cols, BL, groups=(PG, "Black", "White", "White - Black")) + [""]
            tc = [("PSID", "log IGE, child-year", sex, "unbalanced", y, "PSID"),
                  ("NLSY79", "log IGE, child-year", sex, "unbalanced", y, "NLSY79"),
                  (N, "log IGE, child-year", sex, "unbalanced", y, "NLSY97"),
                  (N, "corrected log IGE", sex, "common 0.57 (PSID one-year)", y, "NLSY97 / 0.57")]
            L += ["Tests:", ""] + test_table(tc, [(f"{sex}: {g}", sex, g) for g in (PG, "Black", "White",
                                                                                    "White - Black")]) + [""]
    for sex in ("Both", "Sons", "Daughters"):
        for st, h, dec in (("slope", "rank-rank slope", 3), ("E[rank] p25", "E[rank] at parental p25", 1)):
            cols = [((dt, "rank", sex, "unbalanced", FAM, st), dt, dec) for dt in ("PSID", "NLSY79", N)]
            L += [f"### Ranks, {'both sexes' if sex == 'Both' else sex.lower()}, family income: {h}", ""]
            L += band_table(cols, BL, groups=(PG, "Black", "White", "White - Black"), rowlab="parent rank") + [""]
        tc = [(dt, "rank", sex, "unbalanced", FAM + " | slope", f"{dt} slope") for dt in ("PSID", "NLSY79", N)] + [
            (dt, "rank", sex, "unbalanced", FAM + " | E[rank] p25", f"{dt} E[rank] p25") for dt in ("PSID", "NLSY79", N)]
        L += ["Tests:", ""] + test_table(tc, [(f"{sex}: White - Black", sex, "White - Black")]) + [""]
    L += ["Growth gradient 25-29 -> 35-39 (Haider-Solon), PSID (`ige_by_age.md` 5.1) vs NLSY97:", ""]
    L += header(["PSID ln own earnings", "NLSY97 ln own earnings", "PSID ln family income", "NLSY97 ln family income"])
    for sex in ("Sons", "Daughters"):
        L.append(f"| **{sex}** | | | | |")
        for g in (PG, "Black", "White", "White - Black"):
            L.append(f"| ln parental income: {g} | " + " | ".join(
                c_(get(dt, "growth", sex, "25-29 -> 35-39", "Growth gradient", g, o, "dy")) for dt, o in
                (("PSID", ERN), (N, ERN), ("PSID", FAM), (N, FAM))) + " |")
    L.append("")
    (OUT / "nlsy97_age_profile.md").write_text("\n".join(L) + "\n", encoding="utf-8")


# ================================================================ figure
def figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    col = {"Black": "#eb6834", "White": "#2a78d6", PG: "#1baf7a"}
    off = {"Black": -0.5, "White": 0.5, PG: 0.0}
    dcol = {"PSID": "#6250d6", "NLSY79": "#eda100", "NLSY97": "#008300"}
    dmk = {"PSID": "s", "NLSY79": "^", "NLSY97": "o"}
    doff = {"PSID": -0.6, "NLSY79": 0.0, "NLSY97": 0.6}
    fig, axes = plt.subplots(2, 3, figsize=(13.5, 8.6))
    top = [("log IGE, child-year", "Sons", FAM, "IGE", "NLSY97 log IGE, family income, sons"),
           ("log IGE, child-year", "Daughters", FAM, "IGE", "NLSY97 log IGE, family income, daughters"),
           ("rank", "Both", FAM, "slope", "NLSY97 rank-rank slope, family income, both")]
    bot = [("log IGE, child-year", "Sons", FAM, "IGE", "White - Black log IGE gap, family income, sons"),
           ("log IGE, child-year", "Daughters", FAM, "IGE", "White - Black log IGE gap, family income, daughters"),
           ("rank", "Both", FAM, "E[rank] p25", "White - Black E[rank] gap at parental p25, both")]
    for j, (an, sex, y, st, title) in enumerate(top):
        ax = axes[0, j]
        for g in (PG, "Black", "White"):
            pts = [(MID[b] + off[g], get("NLSY97", an, sex, "unbalanced", b, g, y, st)) for b in BL]
            pts = [(x, r) for x, r in pts if r is not None]
            ax.errorbar([x for x, _ in pts], [r.est for _, r in pts], yerr=[1.96 * r.se for _, r in pts],
                        color=col[g], ls="--" if g == PG else "-", lw=2, marker="o", ms=7, elinewidth=1.2,
                        label=g if j == 0 else None)
        ax.set_title(title, fontsize=10.5)
    for j, (an, sex, y, st, title) in enumerate(bot):
        ax = axes[1, j]
        for dt in ("PSID", "NLSY79", "NLSY97"):
            pts = [(MID[b] + doff[dt], get(dt, an, sex, "unbalanced", b, "White - Black", y, st)) for b in BL]
            pts = [(x, r) for x, r in pts if r is not None]
            ax.errorbar([x for x, _ in pts], [r.est for _, r in pts], yerr=[1.96 * r.se for _, r in pts],
                        color=dcol[dt], lw=2, marker=dmk[dt], ms=8, elinewidth=1.2, label=dt if j == 0 else None)
        ax.set_title(title, fontsize=10.5)
    for ax in axes.ravel():
        ax.axhline(0, color="#bbbbbb", lw=0.8)
        ax.grid(axis="y", color="#e5e5e5", lw=0.6)
        ax.set_xticks([MID[b] for b in BL], BL)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    for ax in axes[1]:
        ax.set_xlabel("Child's age at measurement (band)")
    axes[0, 0].legend(frameon=False, fontsize=9, loc="upper left")
    axes[1, 0].legend(frameon=False, fontsize=9, loc="upper left")
    fig.text(0.5, 0.005, "Band estimates with 95% CI, unbalanced, child-year design (ranks: band means). Black / "
             "White unweighted log IGE; pooled and ranks weighted.\n"
             "NLSY97 'White' = non-Black non-Hispanic; parental "
             "income NLSY97 = 1996 one year, PSID = 13-19 mean, NLSY79 = 1978-80 mean.", ha="center", fontsize=8.5,
             color="#52514e")
    fig.tight_layout(rect=(0, 0.035, 1, 1))
    fig.savefig(OUT / "nlsy97_age_profile.png", dpi=150)


# ================================================================ main
def main():
    rebuild = "--rebuild" in sys.argv
    k, L = load_extract(rebuild)
    print("extract:", k.shape, L.shape, flush=True)
    s, kk, r0 = nlsy97_frames(k, L)
    # coverage table
    cover = {}
    kk2 = kk.assign(race=kk["race"])
    for lab, mask in (("At home in 1997 (N)", pd.Series(True, index=kk2.index)),
                      ("1996 income valid (incl. 0)", kk2["pinc_pt"].notna()),
                      ("ln 1996 income (in $516-$773k)", kk2["lyp_pt"].notna()),
                      ("Multi-year: >= 2 years at home", kk2["n_av"] >= 2),
                      ("Born 1980-82 among >= 2 years", (kk2["n_av"] >= 2) & kk2["birth_year"].le(1982))):
        v = kk2[mask].groupby("race").size().to_dict()
        v["All"] = int(mask.sum())
        cover[lab] = v
    med = kk2.groupby("race")["pinc_pt"].median().round(0).to_dict()
    med["All"] = round(float(kk2["pinc_pt"].median()), 0)
    cover["Median 1996 income (2000 $)"] = {g: f"{v:,.0f}" for g, v in med.items()}
    m2 = kk2[kk2["n_av"] >= 2]
    cover["Corr(ln one-year, ln multi-year) | n_av >= 2"] = {"All": f"{m2[['lyp_pt', 'lyp_av']].corr().iloc[0, 1]:.3f}"}
    sexes = {"Sons": [0], "Daughters": [1]}
    ctrl97 = A4 + ["Amiss"]
    outs = [("lfam", FAM, "faminc"), ("learn", ERN, "earn")]
    store = {}
    logige("NLSY97", s, sexes, outs, ctrl97, designs=("child-year", "band mean"), store=store)
    print("NLSY97 log IGE done", flush=True)
    rank_block("NLSY97", r0, {"Both": [0, 1], **sexes}, [("yf", FAM), ("ye", ERN)])
    print("NLSY97 ranks done", flush=True)
    # mechanism
    growth_block("NLSY97", s, [("learn", ERN), ("lfam", FAM)], ctrl97)
    sv = s[s["lwage_v"].notna()]
    for yname, ylab in (("learn_v", "ln earnings (valid)"), ("lhrs_v", "ln hours"), ("lwage_v", "ln wage")):
        growth_block("NLSY97", sv.assign(**{"_y": sv[yname]}), [("_y", ylab)], ctrl97, tag=" (wage sample)")
    sd = degree_dummies(s[s["degc"].notna()])
    logige("NLSY97", sd, sexes, outs, ctrl97, samples={"unbalanced": BL}, label="log IGE, child-year [deg sample]")
    logige("NLSY97", sd, sexes, outs, ctrl97 + DD, samples={"unbalanced": BL}, label="log IGE | degree")
    growth_block("NLSY97", sd, [("learn", ERN), ("lfam", FAM)], ctrl97, tag=" [deg sample]")
    growth_block("NLSY97", sd, [("learn", ERN), ("lfam", FAM)], ctrl97, tag=" | degree",
                 extra={"child_vars": DD, "ctrl_cols": DD})
    cross_section("NLSY97", kk, ctrl97)
    sm = s[s["partnered"].notna()].copy()
    sm["lfam_p"] = sm["lfam"]
    logige("NLSY97", sm, sexes, [("partnered", "partnered", None), ("lfam", FAM, None), ("learn", ERN, None)],
           ctrl97, samples={"unbalanced": BL}, label="marriage")
    logige("NLSY97", sm, sexes, [("lfam_p", FAM + " | partnered", None)], ctrl97 + ["partnered"],
           samples={"unbalanced": BL}, label="marriage")
    sm2 = sm[sm["lfam"].notna()]
    growth_block("NLSY97", sm2, [("lfam", FAM)], ctrl97, tag=" [mar sample]")
    growth_block("NLSY97", sm2, [("lfam", FAM)], ctrl97, tag=" | partnered",
                 extra={"band_vars": {"pp": "partnered"}, "ctrl_cols": ["pp0", "pp1"]})
    print("NLSY97 mechanism done", flush=True)
    reliability_block("NLSY97", s, sexes, ctrl97)
    corrected_block(store, rr_values())
    print("NLSY97 reliability done", flush=True)
    # ---------------- PSID and NLSY79 on the same bands
    ps, pk, phw = ige26.psid_frames()
    ps = ps[ps["band"].isin(BL)]
    logige("PSID", ps, sexes, outs, A4, samples={"unbalanced": BL})
    pr0 = ige26.rank_frame(pk.set_index("pid"), phw.set_index("pid"), idcol="pid")
    rank_block("PSID", pr0[pr0["band"].isin(BL)], {"Both": [0, 1], **sexes}, [("yf", FAM), ("ye", ERN)])
    growth_block("PSID", ps, [("learn", ERN), ("lfam", FAM)], A4)
    print("PSID done", flush=True)
    ns, nk, nq = ige26.nlsy_frames()
    ns = ns[ns["band"].isin(BL)]
    logige("NLSY79", ns, sexes, outs, A4, samples={"unbalanced": BL})
    nr0 = ige26.nlsy_rank_frame(nk, nq)
    rank_block("NLSY79", nr0[nr0["band"].isin(BL)], {"Both": [0, 1], **sexes}, [("yf", FAM), ("ye", ERN)])
    print("NLSY79 done", flush=True)
    RES = pd.DataFrame(ROWS)
    RESD.update({tuple(r[c] for c in KEYS): r for _, r in RES.iterrows()})
    OUT.mkdir(exist_ok=True)
    RES.to_csv(OUT / "nlsy97_age_profile.csv", index=False)
    write_md(kk, s, cover)
    figure()
    show = RES[(RES["sample"] == "unbalanced") & RES["stat"].isin(["IGE", "slope", "E[rank] p25"])
               & RES["analysis"].isin(["log IGE, child-year", "rank"]) & (RES["outcome"] == FAM)]
    show = show.assign(c=[cell(e, se, p) for e, se, p in zip(show.est, show.se, show.p)])
    pd.set_option("display.width", 250)
    pd.set_option("display.max_colwidth", 40)
    print(show.pivot_table(index=["data", "analysis", "stat", "sex", "group"], columns="band", values="c",
                           aggfunc="first", sort=False).to_string())


if __name__ == "__main__":
    main()
