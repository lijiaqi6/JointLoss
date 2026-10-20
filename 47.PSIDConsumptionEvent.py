r"""Paper A's own PSID consumption measure, 1999-2021, and consumption around single vs joint job loss (2026-10-18).

Plan: IGE/proposals/fable_bps2016_nextsteps.md, Sec. 2.3 (ii) and Sec. 3 "cheaper and better": port Blundell, Pistaferri
and Saporta-Eksten's (BPS 2016, AER) nondurables-plus-services construction (psid_consumption.do / psid_interview.do of
their replication package, read only) to Python for every PSID family file 1999-2021, and run 19's stacked event study
on it with event time in interview waves. Period: PSID interview waves 1999-2021 (biennial; consumption is asked from
1999; the 2023 wave is not used).

Reads (read only): the raw PSID family files (Dropbox/PSID/Family, fam1999er-fam2021er), BPS's shipped psid_cons.dta and
data4estimation.dta (checks only), IGE/data/psid_person_year.pkl, psid_displacement.pkl, correlated_shocks_fam.pkl
(through 25.JointJobLoss.py / 19.FatherDisplacement.py / 23.CorrelatedShocks.py, imported via importlib, no edits).
Writes
  IGE/data/psid_consumption_9921.pkl            household x wave consumption items (cache) + resolved crosswalk
  IGE/output/psid_consumption_event.csv         every estimate
  IGE/output/psid_consumption_event.md          tables (crosswalk, checks, event study)
  IGE/output/psid_consumption_event.png         event-study figure (four panels)
  IGE/paperA_joint_loss/fig_consumption_single_joint.pdf/.png   paper figure

1. CONSUMPTION (BPS's categories; amounts annualised; missing items count as zero in the sums, as BPS).
   Nondurables = food at home incl. delivered (F18/F22 at home, F20/F24 delivered; the food-stamp branch reports
   spending in addition to stamps) + value of food stamps (F12 amount x unit x months received, F13) + gasoline (x12).
   Services = health insurance + hospital/nursing home + doctor/dental + prescriptions (2-year totals / 2 through 2011;
   from 2013 the H64-H76 items cover the previous calendar year and are used as reported, and health insurance is the
   premium amount H61J x its time unit) + home insurance + utilities (electricity, heating fuel, water/sewer, other
   utilities; telephone added to other utilities from 2005 as BPS do) + car insurance + car repairs (F80A monthly x12
   through 2013; F80D 'repair/maintenance' is an annual amount from 2015) + parking + bus/train + taxi + other
   transportation (monthly x12) + school + other school expenses + child care + food away from home + rent (A31 x
   time unit) or, without rent, the rent equivalent 6% of the house value (A20).
   Time units: 3 week x52, 5 month x12, 6 year x1; code 4 x26 (two weeks) for rent, food, child care and health
   insurance, x26 for water 2011-2019 and x4 for water 2021, x2 (six months) for car insurance 2015+ (each code-4
   multiplier is the one the PSID's own generated expenditure variables imply, checked wave by wave); code 2 x365
   for rent and food away (BPS); other codes / DK / NA -> missing unless the amount is zero. DK/NA amounts: the two
   highest values of the field (9..98, 9..99), BPS's rule.
   Deviations from BPS, both for a consistent 1999-2021 series: (a) the combined gas/electricity bill (A42/A42C,
   asked from 2007) is added to utilities; before 2007 such households report it under electricity or heating (share
   with neither 10.6-11.7% in 1999-2003; 22-24% from 2007 without the combined item, 11-12% with it); (b) child care is
   annualised by its time unit where the unit is asked (2007+; BPS read the amount as annual). Both are switched off
   in the 'BPS-exact' variant used for the 1999-2009 checks.
   Crosswalk: each item is found in each wave by its PSID label (patterns in ITEMS below; the resolved variable names
   are written to the output); for 1999-2009 the resolved names are asserted equal to BPS's psid_interview.do.
   Excluded from the consistent series and reported separately: the categories the PSID added in 2005 (household
   repairs, furnishings, clothing, trips, other recreation; computing from 2017), from the PSID's generated variables.
   Real 2000 dollars with the CPI-U of the interview year.
2. CHECKS. (a) Household by household against BPS's shipped psid_cons.dta (1999-2009, 47,206 households); (b) BPS
   Table 1 column 1 (baseline sample, nominal means, 1999-2009) recomputed on BPS's estimation households; (c) each
   item against the PSID's generated expenditure variable, wave by wave (ratio of means where both are reported).
3. EVENT STUDY (19's stacks, as 38.PSIDJointLossChecks.py section 4). Husband's first main displacement (closure /
   layoff / firing) in calendar year ev vs clean controls (no displacement to ev+6); fathers with a child 0-17,
   positive hours at baseline, wife present at baseline. Events ev = 2000-2020 so that the consumption waves 1999-2021
   bracket them (an interview in ev-2..ev-1 and one in ev+1..ev+2). Consumption is dated to the interview (wave W);
   event time in waves k from tau = W - ev: k = -2 (tau -4, -3), -1 (tau -2, -1; reference: the last interview before
   the job-end year), 0 (tau 0: interview in the job-end year, odd-year events only), +1 (tau 1, 2: the first
   interview after the job-end year), +2 (tau 3, 4), +3 (tau 5, 6). Kept while the baseline wife is in the family.
   J = the baseline wife reports her own displacement dated ev-1..ev+1, all three years covered (25 / 38; J = 0 if she
   did not work at baseline). Interaction model with father x stack and wave x stack fixed effects: displaced x k
   (husband displaced alone, vs controls whose wife was not displaced), J x k (wife displaced alone: her displacement
   among control families) and displaced x J x k; 'both displaced' = displaced + J + displaced x J; 'both - alone' =
   J + displaced x J. Summaries: k = +1 and the mean of k = +1..+3 (the first three interviews after the job-end
   year); also the mean of k = +1..+3 minus the k = -2 coefficient (reference k = -2), because J covers ev-1 and the
   k = -1 interview (tau -2/-1) can already follow the wife's displacement, so k = -1 is partly treated for joint
   couples. Outcomes: log total consumption (nondurables + services), log food (at home + delivered + stamps + away),
   log consumption excluding housing (rent / rent equivalent). Samples: dual-earner couples (wife employed at
   baseline) and all married couples; pooled, Black, White (head's race); closures only (19's 'strict'). Units with a
   single observation are dropped (they carry no information with unit fixed effects). Unweighted SRC + SEO; s.e.
   clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1 (normal p-values).
"""
import importlib.util
import re
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from common import DATA, OUT, HERE, CPI, stars
import os
DROPBOX = Path(os.environ.get("DROPBOX", Path.home() / "Dropbox"))   # raw data, read only (Mac: export DROPBOX)

warnings.simplefilter("ignore", FutureWarning)
warnings.simplefilter("ignore", RuntimeWarning)
warnings.simplefilter("ignore", pd.errors.PerformanceWarning)
PAPER = HERE / "paperA_joint_loss"
CW = list(range(1999, 2022, 2))
PERIOD = "PSID interview waves 1999-2021"
BPSDIR = Path(DROPBOX / "ReplicationPapers/Consumption Inequality and Family Labor Supply"
              "/116142-V1/AER_2012_1549_data")


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


P25 = _load("p25", "25.JointJobLoss.py")
P23, P19 = P25.P23, P25.P19
psid1, psid9 = P19.psid1, P19.psid9
md_table = P19.md_table
ROWS = []

# ================================================================ crosswalk: label patterns
MON = "(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)"
ITEMS = {
    "house": r"^A20 HOUSE VALUE$", "homeinsure": r"ANNUAL OWNR INSURANC$",
    "hins2y": r"^H63 TOTAL PAID FOR HLTH INS", "hins": r"^H61J AMT OF FU INSURANCE PREMIUMS$",
    "hins_per": r"^H61J PER FU INSURANCE PREMIUMS$",
    "nurse": r"^H64 TOT", "doctor": r"^H70 TOT", "prescription": r"^H76 TOT",
    "electric": r"ELECTRICITY EXPENSE$", "electric_per": r"ELECTRICITY PER$",
    "heating": r"^A\w+ (HEATING (FUEL )?EXPENSE|FUEL EXPENSE)$",
    "heating_per": r"^A\w+ (HEATING (FUEL )?EXPENSE|FUEL EXPENSE) PER$",
    "gaselec": r"COMBINED GAS/ELECT EXPENSE$", "gaselec_per": r"COMBINED GAS/ELECT EXPENSE PER$",
    "water": r"WATER/SEWER EXPENSE$", "water_per": r"WATER/SEWER EXPENSE PER$",
    "miscutils": r"TOTAL OTR UTILITIES$", "miscutils_per": r"OTR UTILIT(Y|IES) PER$",
    "telephone": r"^A\w+ TELEPHONE EXPENSE$", "telephone_per": r"^A\w+ TELEPHONE EXPENSE PER$",
    "carins": r"CAR INSURANCE EXPENSE$", "carins_per": r"CAR INSURANCE PER$",
    "carrepair": r"CAR REPAIR(/MAINTENANCE)? EXPENSES$", "gasoline": r"GASOLINE EXPENSES$",
    "parking": r"PARKING EXPENSES$", "busfare": r"BUS/TRAIN FARES$", "taxifare": r"CAB FARE EXPENSES$",
    "othertrans": r"OTR TRANSP EXPENSES$", "tuition": r"^\w+ TOTAL SCHOOL EXPENSES$",
    "otherschool": r"TOTAL OTR SCHOOL EXPENSES$",
    "childcare": r"^F\w+ COST CHILD CARE", "childcare_per": r"CHILD CARE COST PER$",
    "fs": r"^F12 VALUE OF FOOD STAMPS (IN \d{4}|LAST YEAR)$",
    "fs_per": r"^F12 TIME UNIT-VALUE FOOD STAMPS (IN \d{4}|LAST YR)$",
    "fdhm1": r"^F18 REPORTED COST OF FOOD AT HOME$", "fdhmper1": r"^F18 COST OF FOOD AT HOME PER$",
    "fddel1": r"^F20 COST OF DELIVERED FOOD$", "fddelper1": r"^F20 COST OF DELIVERED FOOD PER$",
    "fout1": r"^F21 COST OF FOOD EATEN OUT$", "foutper1": r"^F21 COST OF FOOD EATEN OUT PER$",
    "fdhm2": r"^F22 REPORTED COST OF FOOD AT HOME$", "fdhmper2": r"^F22 COST OF FOOD AT HOME PER$",
    "fddel2": r"^F24 COST OF DELIVERED FOOD$", "fddelper2": r"^F24 COST OF DELIVERED FOOD PER$",
    "fout2": r"^F25 COST OF FOOD EATEN OUT$", "foutper2": r"^F25 COST OF FOOD EATEN OUT PER$",
    "rent": r"^A31 DOLLARS RENT$", "rent_per": r"^A31 DOLL+ARS PER WHAT$",
}
FS_MONTHS = rf"^F13 WTR RECE?I?VE?D FOOD STAMPS {MON} (\d{{4}}|LAST YEAR)$"
# PSID generated expenditure variables (validation) and the 2005+ categories (reported separately)
GEN = {"g_fhome": r"^FOOD AT HOME EXPENDITURE", "g_fout": r"^FOOD AWAY FROM HOME EXPENDITURE",
       "g_fdel": r"^FOOD DELIVERED EXPENDITURE", "g_rent": r"^RENT EXPENDITURE", "g_homeins": r"^HOME INSURANCE EXPENDITURE",
       "g_heat": r"^GAS FOR HOME EXPENDITURE", "g_elec": r"^ELECTRICITY EXPENDITURE", "g_water": r"^WATER/SEWER EXPENDITURE",
       "g_othut": r"^OTHER UTILITY +EXPENDITURE", "g_tel": r"^TELEPHONE/INTERNET EXPENDITURE",
       "g_carins": r"^AUTO INSURANCE EXPENDITURE", "g_carrep": r"^VEHICLE REPAIR EXPENDITURE",
       "g_gas": r"^GASOLINE EXPENDITURE", "g_park": r"^PARKING EXPENDITURE", "g_bus": r"^BUS/TRAIN EXPENDITURE",
       "g_taxi": r"^TAXICAB EXPENDITURE", "g_othtr": r"^OTHER TRANSPORTATION EXPENDITURE",
       "g_educ": r"^EDUCATION EXPENDITURE", "g_child": r"^CHILDCARE EXPENDITURE",
       "g_hosp": r"^HOSPITAL/NURSING HOME EXPENDITURE", "g_doc": r"^DOCTOR EXPENDITURE",
       "g_presc": r"^PRESCRIPTIONS/OTHER EXPENDITURE", "g_hins": r"^HEALTH INSURANCE EXPENDITURE",
       "x_hrep": r"^HOUSEHOLD REPAIRS EXPENDITURE", "x_furn": r"^HOUSEHOLD FURNISHING EXPENDITURE",
       "x_cloth": r"^CLOTHING EXPENDITURE", "x_trips": r"^TRIPS EXPENDITURE", "x_rec": r"^OTHER RECREATION EXPENDITURE",
       "x_comp": r"^COMPUTING EXPENDITURE"}
XLAB = {"x_hrep": "Household repairs", "x_furn": "Furnishings", "x_cloth": "Clothing", "x_trips": "Trips",
        "x_rec": "Other recreation", "x_comp": "Computing (2017+)"}
# BPS's variable names (psid_interview.do), 1999-2009: the crosswalk must reproduce them
BPS_NAMES = {
    1999: "house ER13041 homeinsure ER13043 hins2y ER15780 nurse ER15781 doctor ER15787 prescription ER15793 electric ER13086 "
          "heating ER13088 water ER13090 miscutils ER13097 carins ER13191 carrepair ER13195 gasoline ER13196 parking ER13197 "
          "busfare ER13198 taxifare ER13199 othertrans ER13200 tuition ER13202 otherschool ER13204 childcare ER14232 fs ER14256 "
          "fdhm1 ER14288 fdhm2 ER14295 fddel1 ER14291 fout1 ER14293 fout2 ER14300 rent ER13065",
    2001: "house ER17044 homeinsure ER17048 hins2y ER19841 nurse ER19842 doctor ER19848 prescription ER19854 electric ER17097 "
          "heating ER17099 water ER17101 miscutils ER17108 carins ER17202 carrepair ER17206 gasoline ER17207 parking ER17208 "
          "busfare ER17209 taxifare ER17210 othertrans ER17211 tuition ER17213 otherschool ER17215 childcare ER18362 fs ER18387 "
          "fdhm1 ER18421 fdhm2 ER18431 fddel1 ER18425 fout1 ER18428 fout2 ER18438 rent ER17074",
    2003: "house ER21043 homeinsure ER21047 hins2y ER23278 nurse ER23279 doctor ER23285 prescription ER23291 electric ER21086 "
          "heating ER21088 water ER21090 miscutils ER21097 carins ER21838 carrepair ER21842 gasoline ER21843 parking ER21844 "
          "busfare ER21845 taxifare ER21846 othertrans ER21847 tuition ER21849 otherschool ER21851 childcare ER21628 fs ER21653 "
          "fdhm1 ER21686 fdhm2 ER21696 fddel1 ER21690 fout1 ER21693 fout2 ER21703 rent ER21072",
    2005: "house ER25029 homeinsure ER25038 hins2y ER27238 nurse ER27239 doctor ER27245 prescription ER27251 electric ER25082 "
          "heating ER25080 water ER25084 miscutils ER25090 telephone ER25086 carins ER25794 carrepair ER25798 gasoline ER25799 "
          "parking ER25800 busfare ER25801 taxifare ER25802 othertrans ER25803 tuition ER25805 otherschool ER25807 "
          "childcare ER25628 fs ER25655 fdhm1 ER25688 fdhm2 ER25698 fddel1 ER25692 fout1 ER25695 fout2 ER25705 rent ER25063",
    2007: "house ER36029 homeinsure ER36038 hins2y ER40410 nurse ER40414 doctor ER40420 prescription ER40426 electric ER36085 "
          "heating ER36083 water ER36089 miscutils ER36095 telephone ER36091 carins ER36812 carrepair ER36816 gasoline ER36817 "
          "parking ER36818 busfare ER36819 taxifare ER36820 othertrans ER36821 tuition ER36823 otherschool ER36825 "
          "childcare ER36633 fs ER36673 fdhm1 ER36706 fdhm2 ER36716 fddel1 ER36710 fout1 ER36713 fout2 ER36723 rent ER36065",
    2009: "house ER42030 homeinsure ER42039 hins2y ER46383 nurse ER46387 doctor ER46393 prescription ER46399 electric ER42114 "
          "heating ER42112 water ER42118 miscutils ER42124 telephone ER42120 carins ER42803 carrepair ER42807 gasoline ER42808 "
          "parking ER42809 busfare ER42810 taxifare ER42811 othertrans ER42812 tuition ER42814 otherschool ER42816 "
          "childcare ER42652 fs ER42692 fdhm1 ER42712 fdhm2 ER42722 fddel1 ER42716 fout1 ER42719 fout2 ER42729 rent ER42080"}
INF = re.compile(r"(?:long\s+)?([A-Z]+\d+[A-Z0-9]*)\s+(\d+)\s*-\s*(\d+)")
LAB = re.compile(r'label variable\s+(\S+)\s+"(.*)"')


def code4(item, w):
    """multiplier of time-unit code 4 (from the PSID's generated variables, wave by wave)."""
    return {"rent": 26, "water": 26 if w < 2021 else 4, "carins": 2, "childcare": 26,
            "hins": 4 if w == 2013 else 26}.get(item)


def build_wave(w):
    folder = psid1.FAM / f"fam{w}er"
    do = next(f for f in folder.glob("*.do") if "formats" not in f.name)
    t = do.read_text(encoding="latin-1")
    pos = {v: (int(a) - 1, int(b)) for v, a, b in INF.findall(re.search(r"\binfix\b(.*?)\busing\b", t, re.S).group(1))}
    labs = [(v, l.strip()) for v, l in LAB.findall(t) if v in pos]
    d = {"id": labs[1][0]}
    for k, p in {**ITEMS, **GEN}.items():
        hit = [v for v, l in labs if re.search(p, l)]
        if hit:
            d[k] = hit[0]
    months = [v for v, l in labs if re.search(FS_MONTHS, l)]
    assert len(months) == 12, (w, months)
    if w in BPS_NAMES:
        exp = dict(zip(*[iter(BPS_NAMES[w].split())] * 2))
        bad = {k: (v, d.get(k)) for k, v in exp.items() if d.get(k) != v}
        assert not bad, (w, bad)
    cols = sorted(set(d.values()) | set(months))
    f = pd.read_fwf(do.with_suffix(".txt"), colspecs=[pos[c] for c in cols], names=cols, header=None,
                    encoding="latin-1")
    wd = {c: pos[c][1] - pos[c][0] for c in cols}
    lab = dict(labs)
    xw = [dict(wave=w, item=k, var=v, label=lab[v]) for k, v in d.items() if k != "id"]

    def num(c):
        return pd.to_numeric(f[c], errors="coerce").astype(float)

    def amt(k):
        v = num(d[k])
        return v.where((v >= 0) & (v < 10 ** wd[d[k]] - 2))

    def per(k, item, allowed=(3, 4, 5, 6), two=None):
        a, u = amt(k), num(d[k + "_per"])
        mult = {3: 52.0, 5: 12.0, 6: 1.0}
        if 4 in allowed and code4(item, w):
            mult[4] = float(code4(item, w))
        if two:
            mult[2] = two
        mm = u.map(mult)
        return (a * mm).where(mm.notna(), np.where(a == 0, 0.0, np.nan))

    o = {"wave": np.full(len(f), w), "int": f[d["id"]].to_numpy()}
    o["house"] = amt("house")
    o["homeinsure"] = amt("homeinsure")
    o["hinsurance"] = amt("hins2y") / 2 if "hins2y" in d else per("hins", "hins")
    hdiv = 2.0 if w <= 2011 else 1.0
    for k in ("nurse", "doctor", "prescription"):
        o[k] = amt(k) / hdiv
    o["electric"] = per("electric", "electric", (3, 5, 6))
    o["heating"] = per("heating", "heating", (3, 5, 6))
    o["water"] = per("water", "water")
    mu = per("miscutils", "miscutils", (3, 5, 6))
    if "telephone" in d:
        mu = pd.concat([mu, per("telephone", "telephone", (3, 5, 6))], axis=1).sum(axis=1, min_count=1)
    o["miscutils"] = mu
    o["gaselec"] = per("gaselec", "gaselec", (3, 5, 6)) if "gaselec" in d else pd.Series(np.nan, index=f.index)
    o["carins"] = per("carins", "carins", (4, 5, 6))
    o["carrepair"] = amt("carrepair") * (12.0 if w <= 2013 else 1.0)
    for k in ("gasoline", "parking", "busfare", "taxifare", "othertrans"):
        o[k] = amt(k) * 12
    o["tuition"], o["otherschool"] = amt("tuition"), amt("otherschool")
    o["childcare_bps"] = amt("childcare")
    o["childcare"] = per("childcare", "childcare") if "childcare_per" in d else amt("childcare")
    nm = sum(num(c).where(lambda s: s <= 1).fillna(0) for c in months)
    fa, fu = num(d["fs"]), num(d["fs_per"])
    fs = pd.Series(0.0, index=f.index)
    fs = fs.mask(fu == 6, fa).mask(fu == 5, fa * nm).mask(fu == 4, fa * 26 / 12 * nm).mask(fu == 3, fa * 52 / 12 * nm)
    o["fstmp"] = fs.where(~((fa > 999997) | (fu > 6) | ((fu == 1) & (w >= 2007))))

    def food(a1, a2, p1, p2, out=False):
        A1, A2 = num(d[a1]), num(d[a2])
        A1, A2 = A1.where(A1 < 99998), A2.where(A2 < 99998)
        P1, P2 = num(d[p1]), num(d[p2])
        use1 = A1.notna() & (A2 == 0)
        a, p = A1.where(use1, A2), P1.where(use1, P2)
        if out:
            return a.where(p < 7) * p.map({2: 365.0, 3: 52.0, 4: 26.0, 5: 12.0}).fillna(1.0)
        return a.where(~((p == 2) | (p >= 7))) * p.map({3: 52.0, 4: 26.0, 5: 12.0}).fillna(1.0)
    fdhm = food("fdhm1", "fdhm2", "fdhmper1", "fdhmper2")
    fddel = food("fddel1", "fddel2", "fddelper1", "fddelper2")
    o["food"] = pd.concat([fdhm, fddel], axis=1).sum(axis=1, min_count=1)
    o["fout"] = food("fout1", "fout2", "foutper1", "foutper2", out=True)
    ra, ru = num(d["rent"]), num(d["rent_per"])
    o["rent"] = (ra * ru.map({2: 365.0, 3: 52.0, 4: 26.0, 5: 12.0, 6: 1.0})).where(ra <= 99997)
    o["renteq"] = np.where(o["rent"].isna(), 0.06 * o["house"].fillna(0), 0.0)
    for k in GEN:
        o[k] = amt(k) if k in d else pd.Series(np.nan, index=f.index)      # 9..98 / 9..99 codes -> missing
    o = pd.DataFrame({k: np.asarray(v) for k, v in o.items()})
    print(f"  consumption {w}: {len(o):,} families", flush=True)
    return o, xw


def rsum(df, cols):
    return df[cols].sum(axis=1, min_count=1)


def consumption():
    fn = DATA / "psid_consumption_9921.pkl"
    if fn.exists():
        return pd.read_pickle(fn)
    parts = [build_wave(w) for w in CW]
    C = pd.concat([p[0] for p in parts], ignore_index=True)
    XW = pd.DataFrame([r for p in parts for r in p[1]])
    C["utilities_bps"] = rsum(C, ["electric", "heating", "water", "miscutils"])
    C["utilities"] = rsum(C, ["electric", "heating", "water", "miscutils", "gaselec"])
    C["health_ser"] = rsum(C, ["nurse", "doctor", "prescription"])
    C["transport"] = rsum(C, ["carins", "carrepair", "parking", "busfare", "taxifare", "othertrans"])
    C["educ_ser"] = rsum(C, ["tuition", "otherschool"])
    C["housing"] = rsum(C, ["rent", "renteq"])
    C["ndcons"] = rsum(C, ["food", "fstmp", "gasoline"])
    for v, ut, cc in (("", "utilities", "childcare"), ("_bps", "utilities_bps", "childcare_bps")):
        C["services" + v] = rsum(C, ["hinsurance", "health_ser", "homeinsure", ut, "transport", "educ_ser", cc,
                                     "housing", "fout"])
        C["totcons" + v] = rsum(C, ["ndcons", "services" + v])
    C["totcons_nh"] = C["totcons"] - C["housing"].fillna(0)
    C["foodall"] = rsum(C, ["food", "fstmp", "fout"])
    C["excluded"] = rsum(C, list(XLAB))
    defl = C["wave"].map(lambda w: CPI[2000] / CPI[w])
    for c in ("totcons", "totcons_nh", "foodall", "ndcons", "services", "housing", "food", "fout", "excluded"):
        C["r_" + c] = C[c] * defl
    for c in ("r_totcons", "r_totcons_nh", "r_foodall"):          # trimming flags (robustness): 0.5 / 99.5 pct by wave
        pos = C[c].where(C[c] > 0)
        lo, hi = pos.groupby(C["wave"]).transform(lambda s: s.quantile(0.005)), \
            pos.groupby(C["wave"]).transform(lambda s: s.quantile(0.995))
        C[c + "_t"] = pos.where((pos >= lo) & (pos <= hi))
    res = dict(C=C, XW=XW)
    pd.to_pickle(res, fn)
    return res


# ================================================================ helpers
def pv(b, se):
    return 2 * stats.norm.sf(abs(b / se)) if (se == se and se > 0) else np.nan


def cell(b, se, p=None, d=3):
    if not (se == se and se > 0):
        return "n.a."
    p = pv(b, se) if p is None else p
    return f"{b:,.{d}f}{stars(p)} ({se:,.{d}f}; p={'<0.001' if p < 0.001 else f'{p:.3f}'})"


def rec(item, table, sample, outcome, term, b, se, **kw):
    ROWS.append(dict(item=item, table=table, period="1999-2021 waves", sample=sample, outcome=outcome, term=term,
                     coef=b, se=se, p=pv(b, se), **kw))


def comb(b, V, xs, w):
    L = np.array([w.get(x, 0.0) for x in xs])
    e, s = L @ b, np.sqrt(L @ V @ L)
    return e, s


KS = [-2, 0, 1, 2, 3]                                  # reference k = -1
KBIN = {-4: -2, -3: -2, -2: -1, -1: -1, 0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3}
KLAB = {-2: "k=-2 (tau -4/-3)", -1: "k=-1 (tau -2/-1, ref.)", 0: "k=0 (tau 0)", 1: "k=+1 (tau 1/2)",
        2: "k=+2 (tau 3/4)", 3: "k=+3 (tau 5/6)"}
YS = [("lc", "Log total consumption"), ("lfood", "Log food"), ("lcnh", "Log consumption excl. housing")]
SUMS = [("k=+1", [1]), ("mean k=+1..+3", [1, 2, 3]), ("mean k=+1..+2", [1, 2])]


def event_panel(m, d, Uj, C, kind):
    P = P19.stacks(m, d, kind)
    u = P.drop_duplicates(["pid", "ev"])[["pid", "ev", "treat", "hrace", "young0", "w0", "wh0", "fam68"]]
    u = u[u["ev"].between(2000, 2020) & u["w0"].notna()]
    u = u.merge(Uj, on=["pid", "ev"], how="left")
    u["wemp0"] = (u["wh0"] > 0).astype(float)
    mm = m[m["wave"].isin(CW)][["pid", "wave", "int", "w_pid"]].drop_duplicates(["pid", "wave"])
    src = ["r_totcons", "r_totcons_nh", "r_foodall"]
    cc = C[["wave", "int"] + src + [s + "_t" for s in src]]
    q = u.merge(mm, on="pid").merge(cc, on=["wave", "int"], how="left")
    q["tau"] = q["wave"] - q["ev"]
    q = q[q["tau"].between(-4, 6) & (q["w_pid"] == q["w0"])].copy()
    q["k"] = q["tau"].map(KBIN)
    for y, s in (("lc", "r_totcons"), ("lfood", "r_foodall"), ("lcnh", "r_totcons_nh")):
        q[y] = np.log(q[s].where(q[s] > 0))
        q[y + "_t"] = np.log(q[s + "_t"])
    q["unit"] = pd.factorize(q["pid"].astype(np.int64) * 10000 + q["ev"].astype(np.int64))[0]
    q["cell"] = pd.factorize(q["wave"].astype(np.int64) * 10000 + q["ev"].astype(np.int64))[0]
    return q.reset_index(drop=True)


def regress(q, y, inter=True):
    q = q.dropna(subset=[y, "J"]).copy()
    q = q[q.groupby("unit")[y].transform("size") >= 2].reset_index(drop=True)
    xs = []
    for k in KS:
        ind = (q["k"] == k).astype(float)
        q[f"d{k}"] = ind * q["treat"]
        xs.append(f"d{k}")
        if inter:
            q[f"j{k}"], q[f"t{k}"] = ind * q["J"], ind * q["treat"] * q["J"]
            xs += [f"j{k}", f"t{k}"]
    b, V, info = P19.twfe(q, y, xs)
    u = q.drop_duplicates("unit")
    info.update(n_disp=int((u["treat"] == 1).sum()), n_joint=int(((u["treat"] == 1) & (u["J"] == 1)).sum()),
                n_wife=int(((u["treat"] == 0) & (u["J"] == 1)).sum()), n_ctrl=int((u["treat"] == 0).sum()))
    ref = q[q["k"] == -1]
    info["pre_single"] = np.exp(ref.loc[(ref["treat"] == 1) & (ref["J"] == 0), y]).mean()
    info["pre_joint"] = np.exp(ref.loc[(ref["treat"] == 1) & (ref["J"] == 1), y]).mean()
    info["n_joint_ref"] = int(ref.loc[(ref["treat"] == 1) & (ref["J"] == 1), "unit"].nunique())
    info["n_joint_km2"] = int(q.loc[(q["treat"] == 1) & (q["J"] == 1) & (q["k"] == -2), "unit"].nunique())
    info["n_joint_post"] =int(q.loc[(q["treat"] == 1) & (q["J"] == 1) & q["k"].isin([1, 2, 3]), "unit"].nunique())
    return b, V, xs, info


def terms(b, V, xs, ks, inter=True, minus=None):
    """equal-weight mean over event times ks (minus the coefficient at event time `minus`, if given)."""
    w = 1.0 / len(ks)
    if minus is not None:
        wt = {**{k: w for k in ks}, minus: -1.0}
        L = {p: {f"{p}{k}": v for k, v in wt.items()} for p in "djt"}
        return {"single": comb(b, V, xs, L["d"]), "wife": comb(b, V, xs, L["j"]), "trip": comb(b, V, xs, L["t"]),
                "joint": comb(b, V, xs, {**L["d"], **L["j"], **L["t"]}), "diff": comb(b, V, xs, {**L["j"], **L["t"]})}
    D = {f"d{k}": w for k in ks}
    if not inter:
        return {"all": comb(b, V, xs, D)}
    Jw = {f"j{k}": w for k in ks}
    T = {f"t{k}": w for k in ks}
    return {"single": comb(b, V, xs, D), "wife": comb(b, V, xs, Jw), "trip": comb(b, V, xs, T),
            "joint": comb(b, V, xs, {**D, **Jw, **T}), "diff": comb(b, V, xs, {**Jw, **T})}


TLAB = [("single", "Husband displaced alone"), ("joint", "Both spouses displaced"),
        ("diff", "Both - husband alone"), ("wife", "Wife displaced alone (husband not displaced)")]


# ================================================================ main
def main():
    md = ["# Paper A's PSID consumption measure, 1999-2021, and consumption around single vs joint job loss", "",
          f"Built by `47.PSIDConsumptionEvent.py` (2026-10-18); definitions in its docstring. **Period: {PERIOD}** "
          "(consumption is asked from 1999; displacement events 2000-2020 so that the waves bracket them). Plan: "
          "`proposals/fable_bps2016_nextsteps.md` Sec. 2.3 (ii) and Sec. 3. Unweighted PSID SRC + SEO. S.e. clustered by "
          "1968 family; *** p<0.01, ** p<0.05, * p<0.1. Every cell: coefficient*** (s.e.; p).", ""]
    CC = consumption()
    C, XW = CC["C"], CC["XW"]

    # ------------------------------------------------ crosswalk table
    md += ["## 0. Data built: BPS's consumption measure ported to the PSID family files 1999-2021", "",
           f"{len(C):,} family-interviews in {len(CW)} biennial waves 1999-2021 ("
           + ", ".join(f"{w} {n:,}" for w, n in C.groupby('wave').size().items()) + "). Each item is located in "
           "each wave by its PSID label; for 1999-2009 the names equal BPS's `psid_interview.do` (asserted in the code). "
           "Rows = items, columns = waves; '-' = not asked.", ""]
    show = [k for k in ITEMS] + list(XLAB)
    piv = XW.pivot_table(index="item", columns="wave", values="var", aggfunc="first").reindex(show)
    md += ["| Item | " + " | ".join(str(w) for w in CW) + " |", "|---|" + "---|" * len(CW)]
    for k, r in piv.iterrows():
        md.append(f"| {k} | " + " | ".join(r.get(w) if isinstance(r.get(w), str) else "-" for w in CW) + " |")
    md += ["", "Questionnaire changes handled: heating 'A41 heating fuel' -> 'A42A fuel' (2011); combined gas/electric "
           "bill asked from 2007 (added to utilities, see docstring; not in BPS); telephone separate from 2005 (added to "
           "other utilities, as BPS); health insurance 'H63 paid last 2 years' (1999-2011, / 2) -> 'H61J premiums x time "
           "unit' (2013+); hospital / doctor / prescriptions 2-year totals (/ 2) to 2011, previous calendar year from "
           "2013; car repairs 'F80A' monthly (x 12) to 2013 -> 'F80D repair/maintenance' annual from 2015; child care "
           "'F6D' -> 'F7' (2019) and a time unit from 2007. The 2015 car-repair and 2013 health redesigns change levels "
           "in all families alike; the event study's wave x stack fixed effects absorb such common shifts.", ""]

    # ------------------------------------------------ checks
    B = pd.read_stata(BPSDIR / "output" / "psid_cons.dta", convert_categoricals=False)
    B["wave"], B["int"] = (B["year"] + 1901).astype(int), B["id"].astype(int)
    Mb = B.merge(C, on=["wave", "int"], how="left", suffixes=("_b", ""))
    items = ["house", "homeinsure", "hinsurance", "nurse", "doctor", "prescription", "electric", "heating", "water",
             "miscutils", "carins", "carrepair", "gasoline", "parking", "busfare", "taxifare", "othertrans", "tuition",
             "otherschool", "childcare_bps", "fstmp", "food", "fout", "rent", "renteq"]
    agree = []
    for k in items:
        kb = "childcare_b" if k == "childcare_bps" else k + "_b"
        kb = kb if kb in Mb else ("childcare" if k == "childcare_bps" else k)
        a, b_ = Mb[kb].fillna(0), Mb[k].fillna(0)
        agree.append((k, ((a - b_).abs() < 0.51).mean(), Mb[kb].mean(), Mb[k].mean()))
        rec(1, "bps_household_agreement", "BPS psid_cons 1999-2009", k, "share equal", ((a - b_).abs() < 0.51).mean(),
            np.nan, n=len(Mb))
    tot_agree = ((B["totcons"].fillna(0).to_numpy() - Mb["totcons_bps"].fillna(0).to_numpy()) / B["totcons"].clip(lower=1)
                 ).abs().lt(0.001).mean()
    md += ["## 1. Checks (BPS's own data, BPS Table 1, the PSID's generated variables)", "",
           f"### 1a. Household by household against BPS's shipped `psid_cons.dta` (waves 1999-2009, {len(Mb):,} families; "
           f"all merged)", "",
           "BPS-exact variant (no combined gas/electric bill, child care read as annual). Share of families with the "
           "same amount (within $0.5; missing = 0, as in BPS's sums).", "",
           "| Item | Share equal | Mean, BPS | Mean, this script |", "|---|---|---|---|"]
    for k, s, mb, mm in agree:
        md.append(f"| {k} | {s:.4f} | {mb:,.0f} | {mm:,.0f} |")
    md += [f"| **Total (nondurables + services)** | {tot_agree:.4f} (within 0.1%) | {B['totcons'].mean():,.0f} | "
           f"{Mb['totcons_bps'].mean():,.0f} |", "",
           "The rent-equivalent row differs only where BPS leave it missing (house value missing) and this script "
           "writes 0; both count as zero in the totals. The few remaining differences are 2005-2007 edits in BPS's file.",
           ""]

    D = pd.read_stata(BPSDIR / "output" / "data4estimation.dta", convert_categoricals=False)
    D["wave"], D["int"] = (D["year"] + 1901).astype(int), D["id"].astype(int)
    D["rent_all"] = D["rent"].where(D["rent"].notna(), D["renteq"])
    D["health_ser"] = D[["nurse", "doctor", "prescription"]].sum(axis=1, min_count=1)
    D["utilities"] = D[["electric", "heating", "water", "miscutils"]].sum(axis=1, min_count=1)
    D["transport"] = D[["carins", "carrepair", "parking", "busfare", "taxifare", "othertrans"]].sum(axis=1, min_count=1)
    D["educ_ser"] = D[["tuition", "otherschool"]].sum(axis=1, min_count=1)
    Md = D[["wave", "int"]].merge(C, on=["wave", "int"], how="left")
    T1 = [("Total", "totcons", "totcons_bps", "totcons", 39257), ("Nondurable cons.", "ndcons", "ndcons", "ndcons", 8552),
          ("Food at home", "food", "food", "food", 6165), ("Gasoline", "gasoline", "gasoline", "gasoline", 2339),
          ("Services", "services", "services_bps", "services", 30705), ("Food out", "fout", "fout", "fout", 2816),
          ("Health ins.", "hinsurance", "hinsurance", "hinsurance", 1572),
          ("Health serv.", "health_ser", "health_ser", "health_ser", 1317),
          ("Utilities", "utilities", "utilities_bps", "utilities", 3856),
          ("Transportation", "transport", "transport", "transport", 3896),
          ("Education", "educ_ser", "educ_ser", "educ_ser", 2589),
          ("Child care", "childcare", "childcare_bps", "childcare", 714),
          ("Home ins.", "homeinsure", "homeinsure", "homeinsure", 581),
          ("Rent (or rent eq.)", "rent_all", "housing", "housing", 13364)]
    md += ["### 1b. BPS Table 1, column 1 (baseline sample, mean, nominal dollars, waves 1999-2009)", "",
           f"Same {len(D):,} household-years as BPS's estimation file (`data4estimation.dta`); missing = 0 as in BPS's "
           "Table 1 code. Columns: published value; recomputed from BPS's shipped file; this script, BPS-exact items; "
           "this script, Paper A items (with the combined gas/electric bill and child care by its time unit).", "",
           "| Category | BPS Table 1 (published) | BPS shipped file | This script, BPS-exact | This script, Paper A | "
           "Paper A / published |", "|---|---|---|---|---|---|"]
    for lab, cb, cm_bps, cm, pub in T1:
        vb = D[cb].fillna(0).mean()
        v1, v2 = Md[cm_bps].fillna(0).mean(), Md[cm].fillna(0).mean()
        md.append(f"| {lab} | {pub:,} | {vb:,.0f} | {v1:,.0f} | {v2:,.0f} | {v2 / pub:.3f} |")
        rec(1, "bps_table1", "BPS baseline sample 1999-2009", lab, "mean (published / BPS-exact / Paper A)", v2, np.nan,
            published=pub, bps_file=vb, bps_exact=v1)
    md += [f"| Median total | 32,920 | {D['totcons'].median():,.0f} | {Md['totcons_bps'].median():,.0f} | "
           f"{Md['totcons'].median():,.0f} | {Md['totcons'].median() / 32920:.3f} |", ""]

    GV = [("Food at home + delivered", ["food"], ["g_fhome", "g_fdel"]), ("Food away", ["fout"], ["g_fout"]),
          ("Rent (renters)", ["rent"], ["g_rent"]), ("Home insurance", ["homeinsure"], ["g_homeins"]),
          ("Electricity + heating + water + other (+ phone)", ["electric", "heating", "water", "miscutils"],
           ["g_elec", "g_heat", "g_water", "g_othut", "g_tel"]),
          ("Car insurance", ["carins"], ["g_carins"]), ("Car repairs", ["carrepair"], ["g_carrep"]),
          ("Gasoline", ["gasoline"], ["g_gas"]), ("Parking, bus, taxi, other", ["parking", "busfare", "taxifare", "othertrans"],
                                                  ["g_park", "g_bus", "g_taxi", "g_othtr"]),
          ("Education", ["tuition", "otherschool"], ["g_educ"]), ("Child care", ["childcare"], ["g_child"]),
          ("Health services", ["nurse", "doctor", "prescription"], ["g_hosp", "g_doc", "g_presc"]),
          ("Health insurance", ["hinsurance"], ["g_hins"])]
    md += ["### 1c. Each category against the PSID's generated expenditure variable, wave by wave", "",
           "Cell: share of families whose amount equals the PSID's generated amount within 1% / median ratio (this "
           "script / PSID), over families with both positive; the PSID imputes missing items and edits outliers, this "
           "script follows BPS (no imputation, no edits). A median ratio of 1 confirms the annualisation (units, "
           "2-year health totals, monthly transport items). Utilities: the PSID's generated variables also leave out "
           "the combined gas/electric bill, so the comparison uses the items without it.", "",
           "| Category | " + " | ".join(str(w) for w in CW) + " |", "|---|" + "---|" * len(CW)]
    for lab, mine, gen in GV:
        cells = []
        for w in CW:
            x = C[C["wave"] == w]
            a = x[mine].sum(axis=1, min_count=1)
            g = x[gen].sum(axis=1, min_count=1)
            ok = a.notna() & g.notna() & (a > 0) & (g > 0)
            rr = (a / g)[ok]
            sh, r = (((rr - 1).abs() < 0.01).mean(), rr.median()) if ok.sum() > 20 else (np.nan, np.nan)
            cells.append(f"{sh:.2f} / {r:.2f}" if r == r else "-")
            rec(1, "generated_check", f"wave {w}", lab, "share within 1%", sh, np.nan, n=int(ok.sum()), median_ratio=r)
        md.append(f"| {lab} | " + " | ".join(cells) + " |")
    md += [""]

    # ------------------------------------------------ descriptives by wave
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    hd = py[py["head"] & (py["female"] == 0)][["wave", "int"]].drop_duplicates()
    wf = py[py["wife"]][["wave", "int"]].drop_duplicates()
    cpl = hd.merge(wf, on=["wave", "int"])
    C["couple"] = C.set_index(["wave", "int"]).index.isin(pd.MultiIndex.from_frame(cpl)).astype(int)
    md += ["### 1d. Consumption by wave, 1999-2021 (real 2000 dollars, CPI-U of the interview year; all families "
           "and married couples)", "",
           "| Wave | Families | Total, mean | Total, median | Nondurables | Services | Food (incl. stamps, away) | "
           "Housing (rent / rent eq.) | Couples: N | Couples: total, mean | Excluded 2005+ categories, mean (share of "
           "total) |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for w, x in C.groupby("wave"):
        cp = x[x["couple"] == 1]
        ex = x["r_excluded"].mean()
        md.append(f"| {w} | {len(x):,} | {x['r_totcons'].mean():,.0f} | {x['r_totcons'].median():,.0f} | "
                  f"{(x['r_ndcons']).mean():,.0f} | {x['r_services'].mean():,.0f} | {x['r_foodall'].mean():,.0f} | "
                  f"{x['r_housing'].mean():,.0f} | {len(cp):,} | {cp['r_totcons'].mean():,.0f} | "
                  + (f"{ex:,.0f} ({ex / x['r_totcons'].mean():.2f})" if ex == ex else "-") + " |")
        rec(1, "by_wave", f"wave {w}", "real total consumption", "mean", x["r_totcons"].mean(), np.nan, n=len(x))
    ex = C[C["wave"] >= 2005]
    md += ["", "Excluded categories (PSID generated, waves 2005-2021, real 2000 $ means; not in the consistent series): "
           + "; ".join(f"{lab} {ex[k].mul(CPI[2000] / ex['wave'].map(CPI)).mean():,.0f}" for k, lab in XLAB.items())
           + ". Also outside BPS's definition throughout: mortgage payments, property tax, vehicle loan / lease / down "
           "payments.", ""]

    # ------------------------------------------------ event study
    E = P23.extras()
    R = E["R"]
    fam = psid9.family()
    d = pd.read_pickle(DATA / "psid_displacement.pkl")
    ev_sets = P25.wife_events(py, R)
    m = P19.men_panel(py, fam)
    U = P25.build_units(m, d)
    U = P25.add_wife_outcomes(U, m, ev_sets)
    U = U[U["pseudo"] == 0]
    Uj = U[["pid", "ev", "wemp0", "main_W"]].copy()
    Uj["J"] = np.where(Uj["wemp0"] == 0, 0.0, Uj["main_W"])
    Uj = Uj[["pid", "ev", "J"]].drop_duplicates(["pid", "ev"])
    Q = {kind: event_panel(m, d, Uj, C, kind) for kind in ("main", "strict")}
    print("event panels", {k: len(v) for k, v in Q.items()}, flush=True)

    SAMP = [("Dual-earner couples (wife employed at baseline)", lambda q: q[q["wemp0"] == 1]),
            ("All married couples", lambda q: q)]
    RACE = [("All", lambda q: q), ("Black", lambda q: q[q["hrace"] == "Black"]),
            ("White", lambda q: q[q["hrace"] == "White"])]
    RES = {}
    for kind, dlab in (("main", "Main (closures + layoffs)"), ("strict", "Closures only")):
        for sname, fs in SAMP:
            for race, fr in RACE:
                if kind == "strict" and race != "All":
                    continue
                q = fr(fs(Q[kind]))
                for y, _ in YS:
                    b, V, xs, info = regress(q, y)
                    bp, Vp, xsp, infp = regress(q, y, inter=False)
                    S = {lab: terms(b, V, xs, ks) for lab, ks in SUMS}
                    S["mean k=+1..+3 minus k=-2"] = terms(b, V, xs, [1, 2, 3], minus=-2)
                    Sp ={lab: terms(bp, Vp, xsp, ks, inter=False) for lab, ks in SUMS}
                    BK = {k: terms(b, V, xs, [k]) for k in KS}
                    RES[(kind, sname, race, y)] = dict(S=S, Sp=Sp, BK=BK, info=info)
                    for lab, T in S.items():
                        for t, (bb, se) in T.items():
                            rec(2, "interaction_" + lab, f"{dlab} | {sname} | {race}", y, t, bb, se, n=info["n"],
                                displaced=info["n_disp"], joint_events=info["n_joint"], wife_alone=info["n_wife"],
                                controls=info["n_ctrl"], clusters=info["clusters"])
                        if lab in Sp:
                            rec(2, "plain_" + lab, f"{dlab} | {sname} | {race}", y, "all displaced",
                                *Sp[lab]["all"], n=infp["n"], displaced=infp["n_disp"])
                    for k, T in BK.items():
                        for t, (bb, se) in T.items():
                            rec(2, "by_k", f"{dlab} | {sname} | {race}", y, f"{KLAB[k]}:{t}", bb, se)
                print("es", kind, sname, race, flush=True)
    for sname, fs in SAMP:                               # robustness: trimmed outcomes (0.5 / 99.5 pct by wave)
        q = fs(Q["main"])
        for y, _ in YS:
            b, V, xs, info = regress(q, y + "_t")
            S = {lab: terms(b, V, xs, ks) for lab, ks in SUMS}
            RES[("trim", sname, "All", y)] = dict(S=S, info=info)
            for lab, T in S.items():
                for t, (bb, se) in T.items():
                    rec(2, "trimmed_" + lab, f"Main, trimmed | {sname} | All", y, t, bb, se, n=info["n"],
                        displaced=info["n_disp"], joint_events=info["n_joint"])

    def fmt_counts(i):
        return (f"{i['n_disp']:,} ({i['n_joint']:,}) / {i['n_wife']:,} / {i['n_ctrl']:,} / {i['n']:,} / "
                f"{i['clusters']:,}")

    def main_table(kind, keys):
        panels = []
        for sname, race in keys:
            rows = []
            for lab, _ in SUMS[:2]:
                for t, tl in TLAB:
                    rows.append((f"{tl}, {lab}", [cell(*RES[(kind, sname, race, y)]["S"][lab][t]) for y, _ in YS]))
            rows.append(("All displaced (plain event study), mean k=+1..+3",
                         [cell(*RES[(kind, sname, race, y)]["Sp"]["mean k=+1..+3"]["all"]) for y, _ in YS]))
            for t, tl in TLAB[:3]:
                rows.append((f"{tl}, mean k=+1..+3 minus k=-2 (reference k=-2)",
                             [cell(*RES[(kind, sname, race, y)]["S"]["mean k=+1..+3 minus k=-2"][t]) for y, _ in YS]))
            rows.append(("Joint events observed at k=-2",
                         [f"{RES[(kind, sname, race, y)]['info']['n_joint_km2']:,}" for y, _ in YS]))
            if kind == "main" and race == "All":
                for t, tl in TLAB[:3]:
                    rows.append((f"Trimmed (0.5 / 99.5 pct by wave): {tl.lower()}, mean k=+1..+3",
                                 [cell(*RES[("trim", sname, "All", y)]["S"]["mean k=+1..+3"][t]) for y, _ in YS]))
                rows.append(("Trimmed: displaced (joint events) / N",
                             [f"{RES[('trim', sname, 'All', y)]['info']['n_disp']:,} "
                              f"({RES[('trim', sname, 'All', y)]['info']['n_joint']:,}) / "
                              f"{RES[('trim', sname, 'All', y)]['info']['n']:,}" for y, _ in YS]))
            rows.append(("Pre-event level at k=-1, 2000 $: husband alone / both",
                         [f"{RES[(kind, sname, race, y)]['info']['pre_single']:,.0f} / "
                          f"{RES[(kind, sname, race, y)]['info']['pre_joint']:,.0f}" for y, _ in YS]))
            rows.append(("Displaced (joint events) / wife-alone events / control stacks / N / clusters",
                         [fmt_counts(RES[(kind, sname, race, y)]["info"]) for y, _ in YS]))
            rows.append(("Joint events observed at k=-1 / at k=+1..+3",
                         [f"{RES[(kind, sname, race, y)]['info']['n_joint_ref']:,} / "
                          f"{RES[(kind, sname, race, y)]['info']['n_joint_post']:,}" for y, _ in YS]))
            panels.append((f"{sname}: {race}", rows))
        return md_table([lab for _, lab in YS], panels,
                        [("Fixed effects", ["father x stack, wave x stack"] * len(YS)),
                         ("Period", ["waves 1999-2021, events 2000-2020"] * len(YS))])

    md += ["## 2. Consumption around single and joint job loss (stacked event study, waves 1999-2021)", "",
           "19's stacks restricted to displacement events 2000-2020 (the consumption waves 1999-2021 bracket each "
           "event), married at baseline; J = the baseline wife's own displacement dated ev-1..ev+1 (38). Event time in "
           "interview waves relative to the job-end year: k=+1 is the first interview after it (tau = 1-2 years), "
           "k=-1 (tau = -2/-1) the reference. One regression per column (interaction model); rows are linear "
           "combinations of its coefficients: husband alone = displaced x k; both = displaced + J + displaced x J; "
           "both - alone = J + displaced x J; wife alone = J x k among control families. 'All displaced' is a separate "
           "plain event study on the same sample. Counts are units with at least two interviews in the regression. "
           "Rows 'minus k=-2' re-reference to k=-2 (same regression): J covers ev-1, so for joint couples the k=-1 "
           "interview (1-2 years before his job-end year) can already follow her displacement; these rows rest on the "
           "joint events observed at k=-2 (shown).", "",
           "### 2a. Main design, pooled", "",
           main_table("main", [(s, "All") for s, _ in SAMP]), "",
           "### 2b. By race (head's race)", "",
           main_table("main", [(s, r) for s, _ in SAMP for r in ("Black", "White")]), "",
           "### 2c. Closures only (husband's first displacement is a plant closure)", "",
           main_table("strict", [(s, "All") for s, _ in SAMP]), ""]
    # event-time coefficients
    panels = []
    for sname, _ in SAMP:
        rows = []
        for t, tl in TLAB[:3]:
            for k in KS:
                rows.append((f"{tl}, {KLAB[k]}", [cell(*RES[("main", sname, "All", y)]["BK"][k][t]) for y, _ in YS]))
        rows.append(("Displaced (joint events) / wife-alone events / control stacks / N / clusters",
                     [fmt_counts(RES[("main", sname, "All", y)]["info"]) for y, _ in YS]))
        panels.append((sname, rows))
    md += ["### 2d. Event-time coefficients (main design, pooled; reference k=-1)", "",
           md_table([lab for _, lab in YS], panels, [("Fixed effects", ["father x stack, wave x stack"] * len(YS)),
                                                     ("Period", ["waves 1999-2021, events 2000-2020"] * len(YS))]),
           "", "![event study](psid_consumption_event.png)", ""]

    # ------------------------------------------------ target decision
    lines = []
    for sname, _ in SAMP:
        for lab in ("mean k=+1..+3", "k=+1"):
            for src, tag in (("main", ""), ("trim", ", trimmed")):
                lines.append((sname, lab + tag, RES[(src, sname, "All", "lc")]["S"][lab]["diff"]))
        lab = "mean k=+1..+3 minus k=-2"
        lines.append((sname, lab, RES[("main", sname, "All", "lc")]["S"][lab]["diff"]))
    md += ["## 3. Is the joint-minus-single difference precise enough to be a target? (rule: s.e. < 0.08)", "",
           "| Sample | Summary | Both - husband alone, log total consumption | s.e. < 0.08? | Joint events |",
           "|---|---|---|---|---|"]
    for sname, lab, dd in lines:
        md.append(f"| {sname} | {lab} | {cell(*dd)} | {'yes' if dd[1] < 0.08 else 'no'} | "
                  f"{RES[('main', sname, 'All', 'lc')]['info']['n_joint']:,} |")
    md += [""]
    figures(RES)
    md += summary(RES, agree, tot_agree, Md)
    pd.DataFrame(ROWS).to_csv(OUT / "psid_consumption_event.csv", index=False)
    (OUT / "psid_consumption_event.md").write_text("\n".join(md), encoding="utf-8")
    print("written", flush=True)


def figures(RES):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ink, mut, grid = "#1f1e1c", "#52514e", "#e6e5e0"
    C_S, C_J = "#2a78d6", "#eb6834"
    kk = np.array([-2, -1, 0, 1, 2, 3])
    ticks = ["-2\n(-4/-3)", "-1\n(-2/-1)", "0\n(0)", "+1\n(1/2)", "+2\n(3/4)", "+3\n(5/6)"]

    def series(r, t):
        b = np.array([0.0 if k == -1 else r["BK"][k][t][0] for k in kk])
        s = np.array([0.0 if k == -1 else r["BK"][k][t][1] for k in kk])
        return b, s

    def panel(ax, r, ylab):
        for t, col, mk, ls, lab, sh in (("single", C_S, "o", "-", "Husband displaced alone", -0.07),
                                        ("joint", C_J, "s", "--", "Both spouses displaced", 0.07)):
            b, s = series(r, t)
            ax.fill_between(kk + sh, b - 1.96 * s, b + 1.96 * s, color=col, alpha=0.10, linewidth=0)
            ax.plot(kk + sh, b, color=col, marker=mk, markersize=6, linewidth=2, linestyle=ls, label=lab)
        ax.axhline(0, color=mut, linewidth=0.8)
        ax.axvline(-0.5, color="#b0afa8", linewidth=0.8, linestyle=":")
        ax.set_xticks(kk)
        ax.set_xticklabels(ticks)
        ax.tick_params(labelsize=8.5, colors=mut)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        ax.grid(axis="y", color=grid, linewidth=0.6)
        ax.set_ylabel(ylab, fontsize=9.5, color=mut)
        ax.set_xlabel("Interview relative to the job-end year: k (years tau)", fontsize=9.5, color=mut)

    S1, S2 = "Dual-earner couples (wife employed at baseline)", "All married couples"
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    for i, sname in enumerate((S1, S2)):
        for j, (y, ylab) in enumerate((("lc", "Log total consumption"), ("lfood", "Log food"))):
            panel(axes[i, j], RES[("main", sname, "All", y)], ylab)
            axes[i, j].set_title(f"{sname}: {ylab.lower()}", fontsize=9.5, color=ink)
    axes[0, 0].legend(frameon=False, fontsize=9, loc="lower left")
    fig.suptitle("Consumption around single and joint job loss, PSID waves 1999-2021 (events 2000-2020; 95% CI; "
                 "reference = last interview before the job-end year)", fontsize=10.5, color=ink)
    fig.tight_layout()
    fig.savefig(OUT / "psid_consumption_event.png", dpi=150, facecolor="white")
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    for ax, (y, ylab) in zip(axes, (("lc", "Log total consumption (nondurables + services)"), ("lfood", "Log food spending"))):
        panel(ax, RES[("main", S1, "All", y)], ylab)
    axes[0].legend(frameon=False, fontsize=9, loc="lower left")
    fig.tight_layout()
    fig.savefig(PAPER / "fig_consumption_single_joint.pdf", facecolor="white")
    fig.savefig(PAPER / "fig_consumption_single_joint.png", dpi=200, facecolor="white")
    plt.close(fig)


def summary(RES, agree, tot_agree, Md):
    c = lambda t: cell(*t)
    out = ["## 4. Summary (period: PSID waves 1999-2021; events 2000-2020)", ""]
    for sname in ("Dual-earner couples (wife employed at baseline)", "All married couples"):
        r = {y: RES[("main", sname, "All", y)] for y, _ in YS}
        i = r["lc"]["info"]
        out.append(
            f"- {sname} ({i['n_disp']:,} displaced husbands, {i['n_joint']:,} joint events, {i['n_wife']:,} wife-alone "
            f"events): log total consumption, mean of the first three interviews after the job-end year: husband alone "
            f"{c(r['lc']['S']['mean k=+1..+3']['single'])}, both {c(r['lc']['S']['mean k=+1..+3']['joint'])}, both - "
            f"alone {c(r['lc']['S']['mean k=+1..+3']['diff'])}, wife alone {c(r['lc']['S']['mean k=+1..+3']['wife'])}; "
            f"first interview (k=+1): alone {c(r['lc']['S']['k=+1']['single'])}, both {c(r['lc']['S']['k=+1']['joint'])}, "
            f"difference {c(r['lc']['S']['k=+1']['diff'])}; relative to k=-2 instead of k=-1 (k=+1..+3 minus k=-2): "
            f"alone {c(r['lc']['S']['mean k=+1..+3 minus k=-2']['single'])}, both "
            f"{c(r['lc']['S']['mean k=+1..+3 minus k=-2']['joint'])}, difference "
            f"{c(r['lc']['S']['mean k=+1..+3 minus k=-2']['diff'])}. Log food, k=+1..+3: alone "
            f"{c(r['lfood']['S']['mean k=+1..+3']['single'])}, both {c(r['lfood']['S']['mean k=+1..+3']['joint'])}, "
            f"difference {c(r['lfood']['S']['mean k=+1..+3']['diff'])}. Excluding housing, k=+1..+3: alone "
            f"{c(r['lcnh']['S']['mean k=+1..+3']['single'])}, difference {c(r['lcnh']['S']['mean k=+1..+3']['diff'])}.")
    for race in ("Black", "White"):
        r = RES[("main", "All married couples", race, "lc")]
        out.append(f"- {race}, all married couples, log total consumption k=+1..+3: alone "
                   f"{c(r['S']['mean k=+1..+3']['single'])}, both - alone {c(r['S']['mean k=+1..+3']['diff'])} "
                   f"({r['info']['n_disp']:,} displaced, {r['info']['n_joint']:,} joint events).")
    r = RES[("strict", "All married couples", "All", "lc")]
    out.append(f"- Closures only, all married couples, log total consumption k=+1..+3: alone "
               f"{c(r['S']['mean k=+1..+3']['single'])}, both - alone {c(r['S']['mean k=+1..+3']['diff'])} "
               f"({r['info']['n_disp']:,} displaced, {r['info']['n_joint']:,} joint events).")
    out.append(f"- Data: BPS's items reproduced household by household (total within 0.1% for {tot_agree:.1%} of "
               f"47,206 families, 1999-2009); BPS Table 1 total {Md['totcons_bps'].fillna(0).mean():,.0f} (BPS-exact) / "
               f"{Md['totcons'].fillna(0).mean():,.0f} (Paper A) vs 39,257 published.")
    out.append("")
    return out


if __name__ == "__main__":
    main()
