r"""LaTeX tables and the position figure for Paper B's revision after the Fable review (2026-10-17).

Reads only saved estimates (nothing is re-estimated):
  output/age_profile_measurement.csv   (41.AgeProfileMeasurement.py)
  output/age_profile_robustness.csv    (33.AgeProfileRobustness.py)
  output/schooling_job_growth.csv      (42.SchoolingAndJobGrowth.py)
  output/same_employer_growth_checks.csv (36.SameEmployerGrowthChecks.py)
  output/father_job_selfemp.csv        (43.FatherJobSelfEmployment.py)
  output/within_cell_identification.csv (45.WithinCellIdentification.py)
  output/age_profile_round2.csv        (46.AgeProfileRound2.py)
and writes paperB_age_profile/tab_{gap_robust, three_data, schooling, growth_ladder, job_moves, father_se, lambda,
attrition}.tex and output/paperB_position.pdf / .png. Layout and helpers of 28.PaperBTables.py.
"""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("t28", HERE / "28.PaperBTables.py")
T28 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(T28)
table, coef, STARS, OUT = T28.table, T28.coef, T28.STARS, T28.OUT

M41 = pd.read_csv(OUT / "age_profile_measurement.csv", low_memory=False)
R33 = pd.read_csv(OUT / "age_profile_robustness.csv", low_memory=False)
S42 = pd.read_csv(OUT / "schooling_job_growth.csv")
S36 = pd.read_csv(OUT / "same_employer_growth_checks.csv")
F43 = pd.read_csv(OUT / "father_job_selfemp.csv")
W45 = pd.read_csv(OUT / "within_cell_identification.csv")
R46 = pd.read_csv(OUT / "age_profile_round2.csv", low_memory=False)
GC = "Mean >= 35 minus mean < 35"
FAM, ERN = "ln family income", "ln own earnings"
MISSING = []


def pick(df, **kw):
    x = df
    for k, v in kw.items():
        x = x[x[k].astype(str) == str(v)]
    if len(x) == 0:
        MISSING.append(kw)
        return None
    r = x.iloc[0].copy()
    if "Black - White" in {str(v) for v in kw.values()} and "share" not in " ".join(map(str, kw.values())):
        for c in ("est", "coef"):
            if c in r.index and pd.notna(r[c]):
                r[c] = -r[c]
    return r


def cc(r, est="est", dec=3):
    if r is None:
        return ("", "")
    return coef(r[est], r["se"], r["p"], dec)


def gapchg(df, data, block, spec, sex, outcome, bandset="25-49"):
    return pick(df, table="band", data=data, block=block, spec=spec, sex=sex, outcome=outcome, band="test",
                group="White - Black", stat=GC, bandset=bandset) if "table" in df else \
        pick(df, data=data, block=block, spec=spec, sex=sex, outcome=outcome, band="test", group="White - Black",
             stat=GC, bandset=bandset)


SRC41 = r"Source: \texttt{41.AgeProfileMeasurement.py} (\texttt{output/age\_profile\_measurement.csv})"


# ------------------------------------------------------------------------------------------------ robustness
def tab_gap_robust():
    rows41 = [
        ("Baseline", [("apc", "Baseline (33)")]),
        ("Sample and attrition", [
            ("33:sample", "SRC only"), ("33:sample", "Weighted (race-specific)"),
            ("attrition", "Observed at 25-29, unweighted"), ("attrition", "Observed at 25-29, IPW for staying")]),
        ("Age, period and cohort", [
            ("33:cohort", "All, IGE x cohort (at 1965)"), ("apc", "Income-year fixed effects in every cell"),
            ("apc", "Period-varying IGE (evaluated in 1995)"), ("apc", "Income years 1990-2010 only")]),
        ("Experience clock", [("46:experience", "Experience bands (experience dummies)"),
                              ("46:start27", "Ages 27-49 (25-26 dropped)")]),
        ("Metric", [("ppml", "PPML, level (zeros kept)")]),
        ("Position in the parental distribution", [
            ("position", "Parents below the pooled median"), ("position", "Parents in the bottom pooled tercile"),
            ("position", "White re-weighted to the Black parental distribution")]),
    ]
    lab = {"Baseline (33)": "Baseline: child-year design, bands 25--49",
           "SRC only": "SRC sample only (no SEO)", "Weighted (race-specific)": "Each race weighted",
           "Observed at 25-29, unweighted": "Sons observed at 25--29",
           "Observed at 25-29, IPW for staying": r"\quad + inverse-probability weights for staying",
           "All, IGE x cohort (at 1965)": "Cohort-varying IGE (1965 cohort)",
           "Income-year fixed effects in every cell": "Income-year fixed effects",
           "Period-varying IGE (evaluated in 1995)": "Period-varying IGE (1995)",
           "Income years 1990-2010 only": "Income years 1990--2010 only",
           "PPML, level (zeros kept)": "Dollar-weighted IGE (PPML, zeros kept)",
           "Experience bands (experience dummies)": "Potential-experience bands ($\\geq 10$ minus $<10$ years)",
           "Ages 27-49 (25-26 dropped)": "Ages 27--49 (years at 25--26 dropped)",
           "Parents below the pooled median": "Parents below the pooled median",
           "Parents in the bottom pooled tercile": "Parents in the bottom pooled tercile",
           "White re-weighted to the Black parental distribution": "White sons re-weighted to Black parents"}
    panels = []
    for title, specs in rows41:
        rws = []
        for blk, sp in specs:
            cells = []
            for o in (ERN, FAM):
                if blk.startswith("33:"):
                    r = pick(R33, data="PSID", block=blk[3:], spec=sp, sex="Sons", outcome=o, band="test",
                             group="White - Black", stat=GC, bandset="25-49")
                elif blk.startswith("46:"):
                    r = pick(R46, table="band", data="PSID", block=blk[3:], spec=sp, sex="Sons", outcome=o,
                             band="test", group="White - Black", stat=GC, bandset="25-49")
                else:
                    r = gapchg(M41, "PSID", blk, sp, "Sons", o)
                cells.append(cc(r))
            rws.append((lab[sp], cells))
        panels.append((title, rws))
    rk = [("National ranks (26)", "Rank--rank slope, national ranks"), ("Within-race ranks", "Rank--rank slope, "
                                                                                             "within-race ranks")]
    panels.append(("Ranks of family income (column 1: sons; column 2: sons and daughters)", [
        (l_, [cc(gapchg(M41, "PSID", "ranks", sp, "Sons", FAM)), cc(gapchg(M41, "PSID", "ranks", sp, "Both sexes",
                                                                            FAM))]) for sp, l_ in rk]))
    table("tab_gap_robust", "How robust is the opening of the racial gap? (PSID, sons)", "tab:gaprobust",
          ["Own earnings", "Family income"], panels,
          "Each cell is the change of the White $-$ Black gap in the IGE from the age bands below 35 to the bands "
          "from 35 (mean gap over 35--39, 40--44, 45--49 minus mean gap over 25--29, 30--34), with its clustered "
          "standard error (1968 family), from stacked band $\\times$ race regressions of the child-year design (log "
          "outcome on log parental income, quartic in the parent's age, single-year age dummies). Attrition: sons with "
          "family income observed at 25--29; weights are the inverse of the predicted probability of being observed in "
          "each later band (logit on log parental income, income at 25--29, both interacted with race, SRC, parent's "
          "age, five-year cohorts). Period-varying: log parental income $\\times$ (year $-$ 1995)/10 in every cell. "
          "Experience clock: bands of potential experience (age $-$ years of schooling $-$ 6; 0--4 to 20--24) with "
          "single-year experience dummies, opening = mean gap at 10 or more years minus mean gap below 10; or the age "
          "profile without the years at 25--26. PPML: Poisson pseudo-maximum likelihood on the income level. Position: pooled quantiles of parental income "
          "over Black and White sons; re-weighting by the ratio of Black to White shares in 20 parental-income bins, band "
          "by band. Ranks: rank--rank slope of band-mean family income (column 2: sons and daughters). " + STARS +
          " " + SRC41 + r", \texttt{46.AgeProfileRound2.py} and \texttt{33.AgeProfileRobustness.py}.")


def tab_three_data_v1():
    specs = [("One year of parental income", {"PSID": ("corrected", "PSID: one year at 12-16"),
                                              "NLSY79": ("corrected", "NLSY79: 1978 one year"),
                                              "NLSY97": ("corrected", "NLSY97: 1996 one year")}, "Pooled"),
             ("One year, corrected for reliability", {"PSID": ("corrected", "PSID: one year at 12-16 / RR"),
                                                      "NLSY79": ("corrected", "NLSY79: 1978 one year / RR"),
                                                      "NLSY97": ("corrected", "NLSY97: 1996 one year / RR")},
              "Pooled / RR")]
    panels = []
    for o, olab in ((ERN, "Own earnings"), (FAM, "Family income")):
        rws = []
        for lab, d, pl in specs:
            cells = [cc(gapchg(M41, dt, blk, sp, "Sons", o, "25-44")) for dt, (blk, sp) in d.items()]
            pr = pick(M41, table="extra", block="corrected", sex="Sons", outcome=o, spec=pl)
            cells.append(cc(pr))
            rws.append((lab, cells))
        main = {"PSID": "PSID: 13-19 mean, all cohorts", "NLSY79": "NLSY79: 1978-80 mean",
                "NLSY97": "NLSY97: 1996 one year"}
        cells = [cc(pick(R33, data=dt, block="side", spec=sp, sex="Sons", outcome=o, band="test",
                         group="White - Black", stat=GC, bandset="25-44")) for dt, sp in main.items()]
        cells.append(cc(pick(R33, data="cross", spec="(a) Each data set's main definition", sex="Sons", outcome=o,
                             stat="Inverse-variance pooled")))
        rws.append(("Each data set's main parental measure", cells))
        q = [pick(M41, table="extra", block="corrected", sex="Sons", outcome=o, spec=pl) for _, _, pl in specs]
        rws.append(("Cochran $Q$ test of equal changes [p-value]", ["", "", "",
                                                                     "; ".join(r["note"].split(", ")[1].replace(
                                                                         "p=", "[") + "]" for r in q if r is not None)]))
        panels.append((olab, rws))
    table("tab_three_data", "The opening of the racial gap in three data sets (sons, ages 25--44)", "tab:threedata",
          ["PSID", "NLSY79", "NLSY97", "Pooled"], panels,
          "Change of the White $-$ Black gap in the log IGE from the bands below 35 (25--29, 30--34) to the bands "
          "from 35 (35--39, 40--44), child-year design, clustered by family. One year of parental income: PSID the "
          "wave at child age 12--16 nearest 14, NLSY79 1978 income, NLSY97 1996 income. Corrected: each race's IGE "
          "divided by the PSID reliability ratio of one year of family income (White 0.585, Black 0.565), treated as "
          "known. Main measures: PSID mean over child ages 13--19, NLSY79 1978--80 mean, NLSY97 1996. Pooled: inverse-"
          "variance weighted average of the three; the $Q$ row gives the p-value of the test that the three changes "
          "are equal (one-year and corrected rows). " + STARS + " " + SRC41 +
          r" and \texttt{33.AgeProfileRobustness.py}.")


def pool(vals):
    w = [1 / se ** 2 for _, se in vals]
    e = sum(wi * v for wi, (v, _) in zip(w, vals)) / sum(w)
    se = 1 / np.sqrt(sum(w))
    q = sum(wi * (v - e) ** 2 for wi, (v, _) in zip(w, vals))
    from scipy.stats import chi2, norm
    return dict(est=e, se=se, p=2 * norm.sf(abs(e / se)), q=q, qp=1 - chi2.cdf(q, len(vals) - 1))


def tab_three_data():
    """Four public data sets (PSID, NLSY79, NLSY97, NLSY79-CYA), sons' own earnings and family income."""
    one = {"PSID": ("corrected", "PSID: one year at 12-16"), "NLSY79": ("corrected", "NLSY79: 1978 one year"),
           "NLSY97": ("corrected", "NLSY97: 1996 one year")}
    main = {"PSID": "PSID: 13-19 mean, all cohorts", "NLSY79": "NLSY79: 1978-80 mean", "NLSY97": "NLSY97: 1996 one year"}
    panels = []
    for o, olab in ((ERN, "Own earnings"), (FAM, "Family income")):
        rws = []
        r1 = [gapchg(M41, dt, blk, sp, "Sons", o, "25-44") for dt, (blk, sp) in one.items()]
        cya1 = pick(R46, table="band", data="CYA", block="cya", spec="CYA: one year at 12-16", sex="Sons", outcome=o,
                    band="test", group="White - Black", stat=GC, bandset="25-44") if o == ERN else None
        vals = [(r["est"], r["se"]) for r in r1 + [cya1] if r is not None]
        pl = pool(vals)
        rws.append(("One year of parental income", [cc(r) for r in r1] + [cc(cya1), cc(pl)]))
        rr = [pick(R46, table="extra", block="rr_own", data=dt, outcome=o) for dt in one]
        rrp = pick(R46, table="extra", block="rr_own", data="Pooled", outcome=o)
        rws.append(("One year, corrected by each data set's reliability ratio", [cc(r) for r in rr] + [("", ""),
                                                                                                       cc(rrp)]))
        rm = [pick(R33, data=dt, block="side", spec=sp, sex="Sons", outcome=o, band="test", group="White - Black",
                   stat=GC, bandset="25-44") for dt, sp in main.items()]
        cyam = pick(R46, table="band", data="CYA", block="cya", spec="CYA: mother's income at 13-19", sex="Sons",
                    outcome=o, band="test", group="White - Black", stat=GC, bandset="25-44") if o == ERN else None
        rws.append(("Each data set's main parental measure", [cc(r) for r in rm] + [cc(cyam), ("", "")]))
        qs = [f"one year: {len(vals)} data sets, $Q$ p={pl['qp']:.3f}"]
        if rrp is not None:
            qs.append("corrected: " + str(rrp["note"]).replace("Q=", "$Q$=").replace(", p=", ", p="))
        rws.append(("Equality across data sets", ["", "", "", "", "; ".join(qs)]))
        panels.append((olab, rws))
    table("tab_three_data", "The opening of the racial gap in four public data sets (sons, ages 25--44)",
          "tab:threedata", ["PSID", "NLSY79", "NLSY97", "NLSY79|children", "Pooled"], panels,
          "Opening of the White $-$ Black gap in the log IGE: mean gap at 35--39 and 40--44 minus mean gap at 25--29 "
          "and 30--34, child-year design, clustered by family (CYA: mother). One year of parental income: PSID the "
          "wave at child age 12--16 nearest 14, NLSY79 1978 income, NLSY97 1996 income, NLSY79 children: the mother's "
          "family income in the year nearest the child's age 14. Corrected: each race's IGE divided by that data set's "
          "reliability ratio of one year of family income (PSID White 0.585, Black 0.565; NLSY79 0.552, 0.556; NLSY97 "
          "0.430, 0.492), with the ratios' sampling error propagated. Main measures: PSID mean at 13--19, NLSY79 "
          "1978--80 mean, NLSY97 1996, NLSY79 children the mother's mean family income at the child's 13--19; main "
          "measures are not pooled because the four differ in reliability. NLSY79 children: wage and salary income, "
          "children of NLSY79 mothers, few observed at 35--44 (93 White and 120 Black sons at 40--44, born "
          "when their mothers were 23 or younger). Pooled: inverse-variance weighted. " + STARS + " " + SRC41 +
          r", \texttt{46.AgeProfileRound2.py} and \texttt{33.AgeProfileRobustness.py}.")


def tab_within_cell():
    """A3 / A7: the rise of the return to schooling with age, within job cells and net of the calendar."""
    T = {"earn": "PSID return to schooling, ln annual earnings", "wage": "PSID return to schooling, ln hourly wage",
         "nlsy": "NLSY79 return to schooling, ln hourly rate of pay"}
    specs = ["(1) baseline (same rows)", "(2) + early-cell FE", "(3) + current-cell FE",
             "(4) + schooling x calendar trend (return in 1995)", "(5) born 1955-69 only"]
    panels = []
    for k, title in (("earn", "PSID, log annual earnings"), ("wage", "PSID, log hourly wage"),
                     ("nlsy", "NLSY79, log hourly rate of pay")):
        rws = []
        for g, gl, term, tl in (("White", "White", "change", "rise of the return, 35+ minus below 35"),
                                ("Black", "Black", "change", "rise of the return, 35+ minus below 35"),
                                ("Black - White", "White $-$ Black", "change", "rise of the return"),
                                ("Black - White", "White $-$ Black", "25-29", "return at 25--29")):
            rws.append((f"{gl}: {tl}", [cc(pick(W45, table=T[k], group=g, spec=sp, term=term), est="coef")
                                        if not (k == "nlsy" and i > 2) else ("", "") for i, sp in enumerate(specs)]))
        panels.append((title, rws))
    table("tab_within_cell", "Does the racial difference in the pay-off of schooling survive within jobs?",
          "tab:withincell", ["Baseline", "Early-cell|fixed effects", "Current-cell|fixed effects",
                             "Schooling $\\times$|calendar trend", "Born|1955--69"], panels,
          "Coefficient on years of schooling in a regression of the log outcome by age band (25--29 to 50--55) and "
          "race; rows give its rise (mean over the bands from 35 minus mean below 35) and, for the race difference, "
          "its value at 25--29. Controls: quartic in age, year (round) fixed effects. Early cell: the son's modal "
          "occupation group $\\times$ industry group (11 $\\times$ 33) at 25--34; current cell: the same at each "
          "observation. Column (4) adds schooling $\\times$ (year $-$ 1995)/10, so the return is evaluated in 1995 "
          "and the rise is net of the calendar trend of the return; column (5) keeps sons born 1955--69. The NLSY79 is "
          "one cohort, so (4)--(5) are not defined there. All columns use the same son-years (early cell known). "
          "Standard errors clustered by 1968 family (PSID) or 1979 household (NLSY79). " + STARS +
          r" Source: \texttt{45.WithinCellIdentification.py} (\texttt{output/within\_cell\_identification.csv}).")


def tab_afqt_growth():
    """A3 (ii) and A4 (appendix): same-employer growth on schooling within cells; AFQT and schooling by age."""
    TG = {"PSID": "PSID same-employer growth", "NLSY79": "NLSY79 same-employer growth"}
    gs = ["(1) baseline", "(2) + cell FE, first interview", "(3) + early-cell FE"]
    panels = []
    for dt, tt in TG.items():
        rws = [(f"{gl}", [cc(pick(W45, table=tt, group=g, spec=sp, term="educ, 25-34"), est="coef") for sp in gs])
               for g, gl in (("White", "White"), ("Black", "Black"), ("Black - White", "White $-$ Black"))]
        panels.append((f"{dt}: same-employer wage growth at 25--34 on years of schooling", rws))
    TA = "NLSY79 AFQT and schooling by age"
    for x, xl in (("afqt", "AFQT (1 s.d.)"), ("educ", "years of schooling")):
        rws = []
        for g, gl in (("White", "White"), ("Black", "Black"), ("Black - White", "White $-$ Black")):
            rws.append((f"{gl}: return to {xl} at 25--29", [cc(pick(W45, table=TA, group=g, spec=sp,
                                                                     term=f"{x}, 25-29"), est="coef")
                                                             if (x == "afqt" and "AFQT" in sp or x == "educ" and
                                                                 "schooling" in sp) else ("", "") for sp in
                                                             ("(1) AFQT alone", "(2) schooling alone",
                                                              "(3) AFQT + schooling")]))
            rws.append((f"{gl}: rise of the return to {xl}", [cc(pick(W45, table=TA, group=g, spec=sp,
                                                                       term=f"{x}, change"), est="coef")
                                                               if (x == "afqt" and "AFQT" in sp or x == "educ" and
                                                                   "schooling" in sp) else ("", "") for sp in
                                                               ("(1) AFQT alone", "(2) schooling alone",
                                                                "(3) AFQT + schooling")]))
        panels.append((f"NLSY79: log hourly rate of pay on {xl}, by age", rws))
    table("tab_afqt_growth", "Schooling and ability: growth within cells and returns by age", "tab:afqtgrowth",
          ["(1)", "(2)", "(3)"], panels,
          "Top panels: same-employer pairs at 25--34 (Table~\\ref{tab:growthladder}); columns: (1) no cell controls, "
          "(2) fixed effects for the occupation group $\\times$ industry group at the first interview of the pair, (3) "
          "for the early cell. Bottom panels: NLSY79 men 25--55, log hourly rate of pay on the AFQT (standardised "
          "within birth year) alone (1), schooling alone (2) or both (3), by age band; rise = mean over bands from 35 "
          "minus mean below 35. Employer learning predicts that with both included the schooling coefficient falls "
          "and the AFQT coefficient rises with experience. Controls: quartic in age, year (round) fixed effects. "
          + STARS + r" Source: \texttt{45.WithinCellIdentification.py}.")


def tab_experience():
    """A5 (appendix): the gap by potential experience, and schooling at 25-29."""
    ex = [f"exp {a}-{b}" for a, b in ((0, 4), (5, 9), (10, 14), (15, 19), (20, 24))]
    panels = []
    for sp, sl in (("Experience bands (experience dummies)", "single-year experience dummies"),
                   ("Experience bands (age dummies)", "single-year age dummies")):
        rws = []
        for o, ol in ((ERN, "own earnings"), (FAM, "family income")):
            cells = [cc(pick(R46, table="band", data="PSID", block="experience", spec=sp, sex="Sons", outcome=o,
                             band=b, group="White - Black", stat="IGE")) for b in ex]
            cells.append(cc(pick(R46, table="band", data="PSID", block="experience", spec=sp, sex="Sons", outcome=o,
                                 band="test", group="White - Black", stat=GC, bandset="25-49")))
            rws.append((f"White $-$ Black gap, {ol}", cells))
        panels.append((f"Controls: {sl}", rws))
    table("tab_experience", "The racial gap in the log IGE by potential experience (PSID, sons)", "tab:experience",
          ["0--4", "5--9", "10--14", "15--19", "20--24", "Opening|($\\geq$10 minus $<$10)"], panels,
          "Child-years at ages 20--55 as head or spouse, bands of potential experience (age $-$ completed years of "
          "schooling $-$ 6). Each cell: White $-$ Black difference of the band-specific log IGEs (stacked, clustered "
          "by 1968 family); controls: quartic in the parent's age and single-year age or experience dummies. At "
          "25--29, sons of top-tercile White parents have 4.8 years of potential experience, other sons 6.0--7.0. "
          + STARS + r" Source: \texttt{46.AgeProfileRound2.py} (\texttt{output/age\_profile\_round2.md}).")


# ------------------------------------------------------------------------------------------------ policies and shocks
P49 = pd.read_csv(OUT / "paperB_policy_shocks.csv")
SRC49 = r" Source: \texttt{49.PaperBPolicyShocks.py} (\texttt{output/paperB\_policy\_shocks.csv})."


def p49(**kw):
    return pick(P49, **kw)


def tab_entry():
    outs = ["access: good job at 25-34", "ln wage, 25-34", "ln wage, 35-55"]
    panels = []
    for sp, x, title in (("state: entry rate", "ur_e", "A. State unemployment rate at entry (state and entry-year FE)"),
                         ("state: mean rate over the first 10 years", "ur_10",
                          "B. Mean state unemployment rate over the first ten years"),
                         ("national: entry rate, cohort trend", "urN_e",
                          "C. National unemployment rate at entry (linear cohort trend)")):
        rws = []
        for g, gl in (("Black", "Black"), ("White", "White"), ("White - Black", "White $-$ Black")):
            rws.append((f"{gl}: unemployment rate (pp)",
                        [cc(p49(table="D1 entry conditions", sample=g, outcome=o, term=f"{sp} | {x}"), est="coef")
                         for o in outs]))
        for g in ("Black", "White"):
            rws.append((f"{g}: rate $\\times$ log parental income",
                        [cc(p49(table="D1 entry conditions", sample=g, outcome=o, term=f"{sp} | {x}_x"), est="coef")
                         for o in outs]))
        r = [p49(table="D1 entry conditions", sample=g, outcome=o, term=f"{sp} | {x}") for g in ("Black", "White")
             for o in outs[:1]]
        rws.append(("Sons (Black / White)", [" / ".join(f"{int(z['n']):,}" for z in
                                                        [p49(table="D1 entry conditions", sample=g, outcome=o,
                                                             term=f"{sp} | {x}") for g in ("Black", "White")]
                                                        if z is not None) for o in outs]))
        panels.append((title, rws))
    table("tab_entry", "Labor-market conditions at entry: access to good jobs and wages (PSID, sons)", "tab:entry",
          ["Good job|at 25--34", "Log wage|25--34", "Log wage|35--55"], panels,
          "Son-level regressions; entry year = birth year + 18 + years of schooling beyond 12. The state rate is "
          "measured in the state of the son's parental family when he was 17 (BLS LAUS, entry years from 1976); the "
          "national rate is the BLS annual average. Regressors: the rate, the rate $\\times$ centred log parental income, "
          "log parental income, years of schooling, quartic in the parent's age; panels A--B add state-at-17 and "
          "entry-year fixed effects (standard errors clustered by state), panel C a linear birth-cohort trend "
          "(clustered by entry year). Good job: the son's modal job at 25--34 is a well-paid cell with high later "
          "growth (Table~\\ref{tab:access}). White $-$ Black: difference of the separate regressions." + " " + STARS +
          SRC49)


def tab_opening_groups():
    rws_e = []
    for sp, sl in (("Slack entry (state rate above its state and year norm)", "Entered in a slack market"),
                   ("Tight entry", "Entered in a tight market")):
        rws_e.append((sl, [cc(p49(table="D1 profile by entry", sample=sp, outcome=o, term="White - Black opening"),
                              est="coef") for o in (ERN, FAM)]))
    rws_e.append(("Slack minus tight", [cc(p49(table="D1 profile by entry", sample="Slack - Tight", outcome=o,
                                               term="W - B opening"), est="coef") for o in (ERN, FAM)]))
    rws_s = []
    for sp, sl in (("All sons (33)", "All sons"), ("Sons whose 25-34 sector is private", "Private sector at 25--34"),
                   ("Sons whose 25-34 sector is government", "Government at 25--34")):
        rws_s.append((sl, [cc(p49(table="D2 sector profile", sample=sp, outcome=o, term="W - B opening"), est="coef")
                           for o in (ERN, FAM)]))
    table("tab_opening_groups", "The opening of the racial gap by entry conditions and by sector (PSID, sons)",
          "tab:openinggroups", ["Own earnings", "Family income"],
          [("A. By labor-market conditions at entry (sons entering from 1976 with a state at 17)", rws_e),
           ("B. By the son's sector at 25--34", rws_s)],
          "Opening of the White $-$ Black gap in the log IGE: mean gap at 35--49 minus mean gap at 25--34, child-year "
          "design of Table~\\ref{tab:gaprobust}, bands 25--49, clusters 1968 family. Slack entry: the state "
          "unemployment rate at entry is above what state and entry-year fixed effects predict. Sector: the son's modal "
          "sector at 25--34 (government: federal, state or local; private: private company; self-employed excluded). "
          "Slack minus tight: the groups are different sons (some share families), so its standard error is "
          "approximate." + " " + STARS + SRC49)


def tab_father_disp_age():
    terms = [("25-34", "Displaced, son at 25--34"), ("35-44", "Displaced, son at 35--44"),
             ("change", "Change, 35--44 minus 25--34")]
    panels = []
    for o, ol in (("ln own earnings", "Son's log earnings"), ("ln family income", "Son's log family income")):
        rws = []
        for g, gl in (("Pooled", "All sons"), ("Black", "Black sons"), ("White", "White sons"),
                      ("White - Black", "White $-$ Black")):
            rws.append((gl, [cc(p49(table="D3 father displacement by son's age", sample=g, outcome=o, term=t),
                                est="coef") if not (g == "White - Black" and t != "change") else ("", "")
                             for t, _ in terms]))
        panels.append((ol, rws))
    table("tab_father_disp_age", "A childhood shock re-scored by the son's age: the father's displacement (PSID, sons)",
          "tab:fatherdispage", [lab for _, lab in terms], panels,
          "Sons whose father figure was first displaced (plant closure or move, layoff or firing) at the son's 0--17, "
          "against sons never exposed (pseudo event at the treated's median exposure age), with a father figure working "
          "before the (pseudo) event. One stacked regression per row in which every regressor (displaced, log pre-event "
          "family income, parental schooling, birth-year fixed effects) is interacted with the son's age band; outcome: "
          "log of the son's mean earnings or family income over the band ($\\geq 2$ years). Clusters 1968 family. A "
          "selection-on-observables comparison." + " " + STARS + SRC49)


# ------------------------------------------------------------------------------------------------ schooling
def s42(tab, group, outcome, term):
    return pick(S42, table=tab, group=group, outcome=outcome, term=term)


def tab_schooling():
    T28.MAXLINES = 50
    TW = "B PSID premium and IGE by band, ln hourly wage"
    TE = "B PSID premium and IGE by band, ln annual earnings"
    TN = "B NLSY79 premium and IGE by band, ln hourly wage"
    R1, R5 = "(1) return to a year of education", "(5) accounted for by education = (3) - (4)"
    R3 = "(3) ln parental income (IGE of the outcome)"
    cols = [(TW, R1), (TE, R1), (TN, R1), (TW, R3), (TW, R5), (TN, R3), (TN, R5)]
    bands = ["25-29", "30-34", "35-39", "40-44", "45-49", "50-55", "change >= 35 minus < 35"]
    blab = {b: f"Age {b.replace('-', '--')}" for b in bands[:-1]}
    blab[bands[-1]] = r"\textbf{Change, 35+ minus below 35}"
    panels = []
    for g, gl in (("White", "White sons"), ("Black", "Black sons"), ("Black - White", "White $-$ Black")):
        rws = [(blab[b], [cc(s42(t, g, h, b), est="coef") for t, h in cols]) for b in bands]
        panels.append((gl, rws))
    table("tab_schooling", "The return to schooling by age and race, and the part of wage persistence it carries",
          "tab:schooling",
          ["PSID|ln hourly wage|on education", "PSID|ln earnings|on education", "NLSY79|ln hourly wage|on education",
           "PSID|ln hourly wage|on ln parental|income", "PSID|accounted for|by education",
           "NLSY79|ln hourly wage|on ln parental|income", "NLSY79|accounted for|by education"], panels,
          "Son-years at 25--55 with a valid wage, years of education and parental income; one regression per column "
          "and age band, controls: quartic in age and year (round) fixed effects. Columns (1)--(3): coefficient on "
          "years of completed education. Columns (4) and (6): coefficient on log parental income. Columns (5) and (7): "
          "the part of (4) and (6) that disappears when years of education are added (the return to education times "
          "the education gradient in parental income). Change row: mean over the bands from 35 minus mean over the "
          "bands below 35. White $-$ Black: difference of the separate regressions, standard errors from joint "
          "influence functions, clustered by 1968 family (PSID) or 1979 household (NLSY79). " + STARS +
          r" Source: \texttt{42.SchoolingAndJobGrowth.py} (\texttt{output/schooling\_job\_growth.csv}).")


def s36(tab, sample, outcome, term):
    return pick(S36, table=tab, sample=sample, outcome=outcome, term=term)


def tab_growth_ladder():
    P = "B PSID measurement"
    N = "A1 NLSY79 ability"
    cols = [(P, "g b01"), (P, "g b03"), (P, "g b02"), (P, "g b08"), (P, "g2 b10"), (P, "g_strict b13"),
            (N, "g a1"), (N, "g a3"), (N, "g a4"), (N, "g a5")]
    heads = ["PSID|baseline", "PSID|cell FE,|first interview", "PSID|cell FE,|later interview", "PSID|+ education",
             "PSID|two-interval|growth", "PSID|strict|stayers", "NLSY79|baseline", "NLSY79|+ AFQT", "NLSY79|+ education",
             "NLSY79|+ AFQT|+ education"]
    panels = []
    for g, gl in (("White", "White sons"), ("Black", "Black sons"), ("Black - White", "White $-$ Black")):
        rws = []
        for x, xl in (("lyp", "Log parental income"), ("educ", "Years of education"), ("afqt", "AFQT (1 s.d.)")):
            cells = [cc(s36(t, g, o, f"{x}, 25-34"), est="coef") if (x == "lyp" or o in (
                "g b08", "g a4", "g a5") and x == "educ" or o in ("g a3", "g a5") and x == "afqt") else ("", "")
                for t, o in cols]
            if any(c[0] for c in cells):
                rws.append((xl, cells))
        panels.append((gl, rws))
    table("tab_growth_ladder", "Wage growth with the same employer at 25--34: parental income, schooling and ability",
          "tab:growthladder", heads, panels,
          "Pairs of consecutive interviews one to two years apart at which the son is with the same employer (PSID: "
          "tenure covers the interval; NLSY79: the same employer in the job roster), sons aged 25--34 at the later "
          "interview. Outcome: annualised growth of the log hourly wage. One regression per column and race; "
          "controls in every column: quartic in age, year (round) fixed effects. Cell: 11 occupation groups $\\times$ "
          "33 industry groups. Two-interval growth: the same employer at three interviews. Strict stayers: tenure "
          "covers both income years. NLSY79 columns: common sample with AFQT and education known; AFQT standardised "
          "within birth year. White $-$ Black: difference of the separate regressions, joint influence functions, "
          "clustered by 1968 family (PSID) or 1979 household (NLSY79). " + STARS +
          r" Source: \texttt{36.SameEmployerGrowthChecks.py} (\texttt{output/same\_employer\_growth\_checks.csv}).")


def tab_job_moves():
    T = "C within vs between jobs"
    ys = ["(1) annual ln wage growth, all pairs", "(2) contribution: stayed", "(3) contribution: moved, not displaced",
          "(4) contribution: displaced", "(5) P(stayed)", "(7) P(displaced)", "(8) growth | stayed",
          "(9) growth | moved"]
    heads = ["Wage growth,|all pairs", "Contribution:|stayed", "Contribution:|moved", "Contribution:|displaced",
             "Stayed", "Displaced", "Growth|if stayed", "Growth|if moved"]
    panels = []
    for lo in ("25-34", "35-55"):
        rws = []
        for g, gl in (("White", "White"), ("Black", "Black"), ("Black - White", "White $-$ Black")):
            rws.append((f"{gl}: log parental income", [cc(s42(T, g, y, lo), est="coef") for y in ys]))
        panels.append((f"Sons aged {lo.replace('-', '--')}", rws))
    table("tab_job_moves", "Wage growth within and between jobs by parental income (PSID, sons)", "tab:jobmoves", heads,
          panels,
          "Consecutive interviews one to two years apart with a valid wage, a mapped occupation and tenure (waves "
          "1985--2023). Between the two wage years the son stayed with the employer, moved without displacement, or "
          "was displaced (plant closure, layoff or firing). Columns (2)--(4) are the wage growth times an indicator "
          "of the event and add up to column (1) on the same pairs (column (3) and (4) of the moved and displaced "
          "contributions); (5)--(6) linear probabilities; (7)--(8) growth conditional on the event. Each cell: "
          "coefficient on log parental income; controls: quartic in age, year fixed effects; standard errors "
          "clustered by 1968 family. " + STARS +
          r" Source: \texttt{42.SchoolingAndJobGrowth.py} (\texttt{output/schooling\_job\_growth.csv}).")


def tab_father_se():
    smp = ["All sons (35)", "Father not self-employed", "Father self-employed", "Neither father nor son self-employed"]
    panels = []
    for y, yl in (("son in the father's cell", "Son in the father's occupation $\\times$ industry cell"),
                  ("son in the father's occupation group", "Son in the father's occupation group")):
        rws = []
        for g, gl in (("Pooled (weighted)", "All"), ("White", "White")):
            for t, tl in (("25-34", "log parental income, 25--34"), ("35-55", "log parental income, 35--55"),
                          ("change", r"log parental income $\times$ (age $\geq$ 35)")):
                rws.append((f"{gl}: {tl}", [cc(pick(F43, table=f"1 {y} on ln parental income", sample=s, group=g,
                                                    term=t), est="coef") for s in smp]))
        r0 = [pick(F43, table=f"1 {y} on ln parental income", sample=s, group="Pooled (weighted)", term="35-55")
              for s in smp]
        rws.append(("Son-years / sons at 35--55", [f"{int(r['n']):,} / {int(r['sons']):,}" if r is not None else ""
                                                   for r in r0]))
        panels.append((yl, rws))
    rws = []
    for y, yl in (("father's occupation group", "occupation group"), ("father's cell", "cell")):
        rws.append((f"Rich White $-$ rich Black, father's {yl}, 35--55",
                    [cc(pick(F43, table=f"2 rich White vs rich Black, {y}", sample=s, term="wT3 - bT3"), est="coef")
                     for s in smp]))
    rr = [pick(F43, table="2 rich White vs rich Black, father's occupation group", sample=s, term="wT3 - bT3")
          for s in smp]
    rws.append(("Black sons in the top tercile", [f"{int(r['black_t3']):,}" if r is not None else "" for r in rr]))
    lv = {"All sons (35)": "All", "Father not self-employed": "Father not self-employed",
          "Father self-employed": "Father self-employed", "Neither father nor son self-employed": "Neither self-employed"}
    rl = [pick(F43, table="3 leave on ln parental income", sample=lv[s], term="leave") for s in smp]
    rws.append(("Leaving the father's cell (in at 25--34) on log parental income", [cc(r, est="coef") for r in rl]))
    rws.append(("Sons in the father's cell at 25--34", [f"{int(r['n']):,}" if r is not None else "" for r in rl]))
    panels.append(("Race, class and keeping the father's job", rws))
    table("tab_father_se", "Fathers' jobs and self-employment (PSID, sons)", "tab:fatherse",
          ["All sons", "Father not|self-employed", "Father|self-employed", "Neither father|nor son|self-employed"],
          panels,
          "Son-year linear probability models, Lee--Solon controls (quartics in the parent's age and the son's age), "
          "clusters 1968 family; all sons weighted, White sons unweighted. The father's cell is his modal 11 occupation "
          "groups $\\times$ 33 industry groups when the son is 12--18; the father is self-employed when at least half "
          "of his valid interviews from 1976 on, with the son aged 10--25, report working for himself (alone or also "
          "for someone else). The change row is from one regression on 25--55 with log parental income $\\times$ "
          "(age $\\geq$ 35). Rich White $-$ rich Black: sons in the top pooled tercile of parental income, race $\\times$ "
          "tercile cells with log parental income, weighted. Leaving: sons in the father's cell in their modal 25--34 "
          "job, out of it in their modal 35--55 job, on log parental income and a quadratic in birth cohort. These estimates "
          "use sons with a father's self-employment code (and, for leaving, a cohort quadratic and no weights); on all "
          "sons with a father's cell the same contrasts are 0.131$^{***}$ (0.038) for rich White $-$ rich Black and "
          "$-0.167^{**}$ (0.067) for leaving (\texttt{35.EarlyIndustryLatePayoff.py}, Section F). " + STARS +
          r" Source: \texttt{43.FatherJobSelfEmployment.py} (\texttt{output/father\_job\_selfemp.csv}).")


# ------------------------------------------------------------------------------------------------ appendix
def tab_lambda():
    bands = ["25-29", "30-34", "35-39", "40-44", "45-49", "50-55", "change"]
    panels = []
    for o, ol in ((ERN, "Own earnings"), (FAM, "Family income")):
        rws = []
        for g, gl in (("Black", "Black"), ("White", "White"), ("White - Black", "White $-$ Black")):
            cells = []
            for b in bands:
                st = "lambda: mean >= 35 minus mean < 35" if b == "change" else "lambda"
                cells.append(cc(pick(M41, table="extra", block="lambda", outcome=o, spec="All: lambda", band=b,
                                     group=g, stat=st)))
            rws.append((gl, cells))
        for t in (1, 2, 3):
            cells = []
            for b in bands:
                st = "lambda: mean >= 35 minus mean < 35" if b == "change" else "lambda"
                cells.append(cc(pick(M41, table="extra", block="lambda", outcome=o,
                                     spec=f"Parental tercile {t}: lambda", band=b, group="White - Black", stat=st)))
            rws.append((f"White $-$ Black, parental tercile {t}", cells))
        n = pick(M41, table="extra", block="lambda", outcome=o, spec="sample")
        rws.append(("Sons (Black / White)", [f"{int(n['est']):,} / {int(n['se']):,}"] + [""] * 6))
        panels.append((ol, rws))
    table("tab_lambda", "Current and lifetime income by age: Haider--Solon $\\lambda$ by race (PSID, sons)",
          "tab:lambda", ["25--29", "30--34", "35--39", "40--44", "45--49", "50--55", "Change, 35+|minus below 35"],
          panels,
          "Sons with at least three valid years in each of 25--34, 35--44 and 45--55. $\\lambda$: slope of the log "
          "outcome in the band (net of race-specific single-age means) on the son's mean of the same net log outcome "
          "over 25--55, by race, with single-age dummies; standard errors clustered by 1968 family. Adding log parental "
          "income to these regressions leaves $\\lambda$ unchanged and its coefficient is not different from zero in "
          "any band (\\texttt{output/age\\_profile\\_measurement.md}, Section C). " + STARS + " " + SRC41 + ".")


def tab_attrition():
    bands = ["30-34", "35-39", "40-44", "45-49"]
    panels = []
    for sex in ("Sons", "Daughters"):
        rws = []
        for g in ("White", "Black"):
            rws.append((f"Share observed, {g}", [f"{pick(M41, table='extra', block='attrition', sex=sex, band=b, spec='share observed', group=g)['est']:.3f}" for b in bands]))
        for g, gl in (("White", "White"), ("Black", "Black"), ("Black - White", "White $-$ Black")):
            rws.append((f"{gl}: log parental income", [cc(pick(M41, table="extra", block="attrition", sex=sex, band=b,
                                                               spec="lyp + early income", group=g,
                                                               stat="P(observed) on ln parental income"))
                                                       for b in bands]))
        rws.append(("Children at risk", [f"{int(pick(M41, table='extra', block='attrition', sex=sex, band=b, spec='lyp', group='White', stat='P(observed) on ln parental income')['children']):,}" for b in bands]))
        panels.append((sex, rws))
    table("tab_attrition", "Who stays in the panel? Probability of being observed in a later age band (PSID)",
          "tab:attrition", ["30--34", "35--39", "40--44", "45--49"], panels,
          "Children with family income observed at 25--29 and born early enough to reach the band. Linear probability "
          "of being observed as a household head or spouse with valid family income in the band, on log parental "
          "income interacted with race, log family income at 25--29 interacted with race, a quartic in the parent's "
          "age and five-year birth-cohort dummies; standard errors clustered by 1968 family. " + STARS + " " + SRC41 +
          ".")


# ------------------------------------------------------------------------------------------------ figure
def figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    col = {"Black": "#eb6834", "White": "#2a78d6"}
    ex = M41[M41["table"] == "extra"]
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    for j, (o, ol) in enumerate(((ERN, "own earnings"), (FAM, "family income"))):
        ax = axes[0, j]
        for g in ("Black", "White"):
            for b0, ls, mk in (("25-29", "--", "o"), ("40-49", "-", "s")):
                z = ex[(ex["block"] == "bins") & (ex["outcome"] == o) & (ex["spec"] == b0) & (ex["group"] == g)
                       & (ex["children"] >= 20)].copy()
                z = z.sort_values("lp")
                ax.plot(z["lp"], z["est"], ls=ls, marker=mk, ms=4.5, lw=1.6, color=col[g], label=f"{g}, ages {b0}")
        ax.set_xlabel("Log parental income (mean of the pooled vigintile)")
        ax.set_ylabel(f"Mean log {ol}")
        ax.set_title(f"{'AB'[j]}. Sons' {ol} by parental-income vigintile", fontsize=11, loc="left")
        ax.grid(color="#e5e5e5", lw=0.6)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        if j == 0:
            ax.legend(frameon=False, fontsize=9)
        ax = axes[1, j]
        specs = [("All parents (33)", "All sons", "#52514e"), ("Parents below the pooled median",
                                                                "Parents below the median", "#6250d6"),
                 ("White re-weighted to the Black parental distribution", "White sons re-weighted to Black parents",
                  "#008300")]
        bl = ["25-29", "30-34", "35-39", "40-44", "45-49"]
        mid = dict(zip(bl, [27, 32, 37, 42, 47]))
        for i, (sp, lab, c) in enumerate(specs):
            pts = []
            for b in bl:
                r = pick(M41, table="band", data="PSID", block="position", spec=sp, sex="Sons", outcome=o, band=b,
                         group="White - Black", stat="IGE")
                if r is not None:
                    pts.append((mid[b] + (i - 1) * 0.6, r))
            ax.errorbar([x for x, _ in pts], [r["est"] for _, r in pts], yerr=[1.96 * r["se"] for _, r in pts],
                        color=c, marker="o", ms=5, lw=1.6, elinewidth=1, capsize=0, label=lab)
        ax.axhline(0, color="#bbbbbb", lw=0.8)
        ax.set_xticks(list(mid.values()), bl)
        ax.set_xlabel("Son's age (band)")
        ax.set_ylabel("White $-$ Black log IGE gap")
        ax.set_title(f"{'CD'[j]}. Racial gap in the log IGE of {ol}", fontsize=11, loc="left")
        ax.grid(axis="y", color="#e5e5e5", lw=0.6)
        for sp_ in ("top", "right"):
            ax.spines[sp_].set_visible(False)
        if j == 0:
            ax.legend(frameon=False, fontsize=9, loc="upper left")
    fig.tight_layout()
    fig.savefig(OUT / "paperB_position.pdf")
    fig.savefig(OUT / "paperB_position.png", dpi=150)


if __name__ == "__main__":
    tab_gap_robust()
    tab_three_data()
    tab_schooling()
    tab_growth_ladder()
    tab_job_moves()
    tab_father_se()
    tab_lambda()
    tab_attrition()
    tab_within_cell()
    tab_afqt_growth()
    tab_experience()
    tab_entry()
    tab_opening_groups()
    tab_father_disp_age()
    figure()
    if MISSING:
        print(f"{len(MISSING)} lookups found nothing:")
        for m in MISSING[:20]:
            print("  ", m)
