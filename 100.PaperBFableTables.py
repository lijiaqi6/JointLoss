r"""LaTeX tables for the additions of Fable's top-5 review (proposals/fable_top5_distance_paperB_20261020.md).

Reads the JSON outputs of 91-99 and writes paperB_age_profile/tab_layoff_selection.tex (A2, A3, A6: timing, timing as
the control, splits), tab_layoff_exog.tex (A1 industry shocks, A4 daughters, C1 simulated UI), tab_split_robust.tex
(B1 measurement error, B2 the rest, B3 wealth) and tab_age_period.tex (D1 NLSY97 AFQT, D2 pooled rise). Layout and
helpers of 90.PaperBRaceNeutralTables.py.

Run:  python 100.PaperBFableTables.py
"""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
_s = importlib.util.spec_from_file_location("t90", HERE / "90.PaperBRaceNeutralTables.py")
T = importlib.util.module_from_spec(_s)
_s.loader.exec_module(T)
J, cell, table, STARS = T.J, T.cell, T.table, T.STARS


def src(*scripts):
    return ("Source: " + ", ".join(rf"\texttt{{{x}}}" for x in scripts)
            + r"; table built by \texttt{100.PaperBFableTables.py}. " + STARS)


def t_layoff_selection():
    S = J("layoff_selection")
    heads = ["Pooled", "White", "Black"]
    rows_t = []
    for k, lab in (("lay_a6_xa", "Layoff share, ages 6--12, $\\times$ age"), ("f_sh_layoff_xa", "Layoff share, ages 13--19, $\\times$ age"),
                   ("lay_a20_xa", "Layoff share, ages 20--26, $\\times$ age")):
        rows_t.append((lab, [cell(S[f"A6c|{g}"]["b"][k]) for g in heads_key()]))
    rows_t.append(("13--19 minus 6--12", [cell(S[f"A6c|{g}"]["d_6"]) for g in heads_key()]))
    rows_t.append(("13--19 minus 20--26", [cell(S[f"A6c|{g}"]["d_20"]) for g in heads_key()]))
    rows_t.append(("All three equal: $\\chi^2(2)$ [$p$]", [f"{S[f'A6c|{g}']['wald'][0]:.2f} [{S[f'A6c|{g}']['wald'][2]:.3f}]"
                                                          for g in heads_key()]))
    rows_t.append(("Sons", [f"{S[f'A6c|{g}']['sons']:,}" for g in heads_key()]))
    rows_c = [("Layoff at 13--19 (T) $\\times$ age", [cell(S[f"A2|{g}"]["T"]) for g in heads_key()]),
              ("Layoff at 6--12 only (E) $\\times$ age", [cell(S[f"A2|{g}"]["E"]) for g in heads_key()]),
              ("T minus E", [cell(S[f"A2|{g}"]["T-E"]) for g in heads_key()]),
              ("Sons T / E / L", [" / ".join(f"{x:,}" for x in S[f"A2|{g}"]["sons"]) for g in heads_key()])]
    rows_s = []
    for title, parts, labs in (("income loss", ["lay_loss_small", "lay_loss_big"], ["small fall in family income", "large fall in family income"]),
                               ("unemployment (hours >= 500)", ["lay_hu_short", "lay_hu_long"], ["short unemployment (< 500 hours)", "long unemployment (500+ hours)"]),
                               ("repeat", ["lay_one", "lay_multi"], ["one teen layoff year", "two or more"]),
                               ("UI receipt", ["lay_noui", "lay_ui"], ["no UI received", "UI received"])):
        for p, lab in zip(parts, labs):
            rows_s.append((f"Layoff share, {lab}, $\\times$ age", [cell(S[f"A3|{title}|{p}"]["fe"]), "", ""]))
        W = S[f"A3|{title}|wald"]
        rows_s.append(("\\quad equal: $p$", [f"{W[2]:.3f}", "", ""]))
    base, ctl = S["A3vi|as in 88"], S["A3vi|+ ln parental income at 20-26 (and its flag)"]
    rows_s.append(("Layoff share $\\times$ age, + ln parental income at 20--26", [cell(ctl["fe"]), "", ""]))
    cnt = S["A6a|pooled"]
    rows_n = [("Treated sons at 25--29 / 45--49 (father present)",
               [f"{S[f'A6a|{g}']['treated'][0]:,} / {S[f'A6a|{g}']['treated'][4]:,}" for g in heads_key()]),
              ("Layoff minus closure change, 45--49 minus 25--29", [cell(S["A6b|pooled"]["diff"]), cell(S["A6b|White"]["diff"]), ""])]
    table("tab_layoff_selection", "Is the delayed cost of a father's layoff selection? Timing, comparison groups and splits (PSID)",
          "tab:layoff_selection", heads, [("A. Counts and the closure contrast", rows_n),
                                          ("B. Three windows of the son's age, within son", rows_t),
                                          ("C. Timing as the control: sons whose father was laid off at some time (reference: only at 20--26)", rows_c),
                                          ("D. What the layoff is and what it does: the teen layoff share split into parts (pooled)", rows_s)],
          "Son-years 25--55 with a valid wage; ln earnings. Within son: son fixed effects, single-age dummies, ln parental "
          "income, every component of Table~\\ref{tab:passed_on} panel A, the family-structure flags and five-year cohort "
          "dummies, each $\\times$ (age $-$ 40)/10; coefficients per unit share per ten years of age; standard errors "
          "clustered by 1968 family. Panel A, second row: band coefficients at equal parental income and components, "
          "common bootstrap draws (200). Panel B: sons whose father is observed as a head at their 6--12 and 20--26. "
          "Panel C: T = a layoff at 13--19, E = at 6--12 and not 13--19, L = only at 20--26. Panel D: each split replaces "
          "the layoff share by parts that add up to it (a third part, not measured, is in the regression and not shown); "
          "the fall in family income is the layoff wave against the son's layoff-free teen waves, split at the median "
          f"({S['info']['median_drop_layoff_years']:.3f}); hours unemployed are measured to 1993 and UI receipt in "
          f"{100 * S['info']['share_layoff_years_ub_measured']:.0f}\\% of layoff years. " + src("91.LayoffSelection.py"))


def heads_key():
    return ["pooled", "White", "Black"]


def t_layoff_exog():
    I = J("layoff_industry_shocks")
    D = J("layoff_daughters")
    U = J("simulated_replacement_rate")
    heads = ["Estimate"]
    rows_i = [("First stage: father's layoff share on the decline", [cell(I["fs|f_sh_layoff|decl"])]),
              ("First stage: father's unemployment share on the decline", [cell(I["fs|f_sh_unemp|decl"])]),
              ("First stage: father's closure share on the decline", [cell(I["fs|f_sh_close|decl"])]),
              ("Reduced form: son's ln earnings, change 45--49 minus 25--29", [cell(I["rf|decl|sector FE, birth-year FE"]["ch"])]),
              ("Reduced form within son: decline at 12--18 $\\times$ age", [cell(I["fe|decl"]["three"][0])]),
              ("\\quad placebo: decline at 5--11 $\\times$ age", [cell(I["fe|decl"]["three"][1])]),
              ("\\quad placebo: decline at 19--25 $\\times$ age", [cell(I["fe|decl"]["three"][2])]),
              ("OLS within son: layoff share $\\times$ age, same sons", [cell(I["fe|ols_layoff"])])]
    rows_d = []
    for sex in ("sons", "daughters"):
        for y, lab in (("lw", "ln hourly wage"), ("ly", "ln earnings")):
            e = D[f"{sex}|{y}"]
            rows_d.append((f"{sex.capitalize()}, {lab}: layoff 45--49 minus 25--29", [cell(e["change"])]))
            rows_d.append((f"{sex.capitalize()}, {lab}: within person, layoff $\\times$ age", [cell(e["fe"])]))
    k = "rr (1 s.d.), + layoff x father's ln wage x age"
    Wk = J("ui_duration_weeks")
    rows_u = [("Layoff share $\\times$ replacement rate $\\times$ age", [cell(U["fe|rr (1 s.d.)"]["lay_rr_z_xa"])]),
              ("\\quad + layoff share $\\times$ father's ln wage $\\times$ age", [cell(U[f"fe|{k}"]["lay_rr_z_xa"])]),
              ("Placebo: father's ln wage $\\times$ replacement rate $\\times$ age", [cell(U[f"fe|{k}"]["flw_rr_z_xa"])]),
              ("Layoff share $\\times$ weeks of benefit available $\\times$ age",
               [cell(Wk["+ layoff x state unemployment rate x age"]["lay_wk_xa"])]),
              ("Placebo: father's ln wage $\\times$ weeks $\\times$ age",
               [cell(Wk["+ layoff x state unemployment rate x age"]["flw_wk_xa"])])]
    table("tab_layoff_exog", "Layoffs the father did not choose, daughters, and insurance at the father's wage (PSID)",
          "tab:layoff_exog", heads, [("A. National employment decline of the father's sector at the son's 12--18", rows_i),
                                     ("B. Sons and daughters, one reduced specification", rows_d),
                                     ("C. Unemployment insurance simulated at the father's wage, within son", rows_u)],
          f"Panel A: {I['n']['sons']:,} father-present sons; decline = share of the seven years at the son's 12--18 in which "
          "national employment (BLS CES) of the father's sector fell; sector and birth-year fixed effects; standard errors "
          f"clustered by sector $\\times$ birth year ({I['n']['clusters']} clusters); first-stage $F$ for the layoff share "
          f"{(I['fs|f_sh_layoff|decl'][0] / I['fs|f_sh_layoff|decl'][1]) ** 2:.1f}. Panel B: the outcome on ln parental "
          "income and the father's teen-window wage, hours, unemployment, zero hours, volatility, closure and layoff shares; "
          "father present; clustered by 1968 family. Panel C: the benefit the state's law would have paid the father "
          "(half his weekly earnings between the state's minimum and maximum), over his weekly earnings, mean over the "
          "son's 12--18 (1976 and later), standardised; within-son design of Table~\\ref{tab:layoff_selection}, with "
          "state-at-17 $\\times$ age. Weeks available: the state's regular maximum, 13 weeks when Extended Benefits were "
          "on (DOL ETA 539) and the federal emergency programmes with tiers approximated from the state's insured and "
          "total unemployment rates, mean over the son's 12--18 (1984 and later), standardised, with layoff share "
          "$\\times$ the state's unemployment rate $\\times$ age. " + src("93.LayoffIndustryShocks.py", "92.LayoffDaughters.py",
                                                  "99.SimulatedReplacementRate.py", "102.UIDurationWeeks.py"))


def t_eitc():
    E = J("eitc_by_age")
    heads = ["25--29", "30--34", "35--39", "40--44", "Change", "Within son"]
    rows = []
    for key, lab in (("ln earnings, all sons", "ln earnings, all sons"),
                     ("ln earnings, all sons, + ln parental income", "\\quad + ln parental income"),
                     ("ln earnings, mother with <= 12 years of schooling", "ln earnings, mother $\\le$ 12 years of schooling"),
                     ("employed, all sons", "employed, all sons"),
                     ("employed, mother with <= 12 years of schooling", "employed, mother $\\le$ 12 years of schooling")):
        e = E[key]
        rows.append((lab, [cell(b, dec=4) for b in e["bands"]] + [cell(e["change"], dec=4), cell(e["fe"], dec=4)]))
    table("tab_eitc_age", "The EITC in childhood scored at different ages of the son (PSID)", "tab:eitc_age", heads,
          [("Coefficient of exposure (thousands of 2000 dollars of maximum credit over the son's 13--18)", rows)],
          f"Exposure: the maximum federal and state EITC for the family's number of children in each year of the son's "
          f"13--18, summed (intent to treat, as \\citet{{bastian2018long}}); sons whose teens fall in 1975 and later "
          f"({E['ln earnings, all sons']['sons']:,} sons with a valid wage). Birth-year, state-at-17 and "
          "number-of-children fixed effects, single-age dummies, PSID weights; change = 40--44 minus 25--29 from one "
          "stacked regression; within son: exposure $\\times$ (age $-$ 40)/10 with son fixed effects and birth-year and "
          "children $\\times$ age. Standard errors clustered by 1968 family. " + src("101.EITCByAge.py"))


def t_split_robust():
    M = J("split_measurement_error")
    R = J("rest_identification")
    W = J("parental_wealth")
    heads = ["Wage", "Hours", "Spells", "Rest"]
    rows_m = []
    for lab, key in (("Whole teen window, OLS", "whole window, OLS"), ("Half A, OLS", "half A, OLS"),
                     ("Half A instrumented by half B", "half A instrumented by half B")):
        s = M[f"25-55|{key}|shares"]
        rows_m.append((lab, [cell(s[k], pct=True) for k in ("wage", "hours", "spells", "rest")]))
    for lab, key in (("At 45--49, whole window", "whole window, OLS"), ("At 45--49, half A instrumented", "half A instrumented by half B")):
        s = M[f"45-49|{key}|shares"]
        rows_m.append((lab, [cell(s[k], pct=True) for k in ("wage", "hours", "spells", "rest")]))
    r2 = R
    rows_r = [("$R^2$ of ln parental income on the components and resources", [f"{r2['r2|+ 80' + chr(39) + 's resources (lpl, asset / transfer / other shares, own, AFDC, children, schooling)'][0]:.3f}", "", "", ""]),
              ("$R^2$ on parental labor income and the income shares", [f"{r2['r2|lpl + the three income shares'][0]:.3f}", "", "", ""]),
              ("Rest share, with labor income and income shares (Table~\\ref{tab:passed_on}, panel B)",
               ["", "", "", cell(R["split|80's split B (with lpl and the income shares)"]["share"], pct=True)]),
              ("Rest share, non-income resources only", ["", "", "", cell(R["split|without lpl and the income shares (non-income resources only)"]["share"], pct=True)])]
    rows_w = [("Without wealth: rest share", ["", "", "", cell(W["split B (no wealth)|25-55"]["share"], pct=True)]),
              ("+ wealth (rank within birth year): wealth share", [cell(W["+ wealth: within-birth-year rank|25-55"]["wealth_share"], pct=True), "", "", cell(W["+ wealth: within-birth-year rank|25-55"]["share"], pct=True)]),
              ("\\quad wealth contribution at 25--29 / 35--39", [cell(W["+ wealth: within-birth-year rank|25-29"]["wealth"]), cell(W["+ wealth: within-birth-year rank|35-39"]["wealth"]), "", ""]),
              ("+ wealth (asinh of net worth): wealth share", [cell(W["+ wealth: asinh(net worth)|25-55"]["wealth_share"], pct=True), "", "", cell(W["+ wealth: asinh(net worth)|25-55"]["share"], pct=True)])]
    table("tab_split_robust", "What is passed on: measurement error, the rest and parental wealth (PSID)",
          "tab:split_robust", heads, [("A. Shares of the earnings IGE (\\%), components measured on two halves of the teen window", rows_m),
                                      ("B. What identifies the rest (25--55)", rows_r),
                                      ("C. Parental wealth: sons born 1964 and later (wealth column = wealth's share; first two cells of the third row = its contribution at 25--29 and 35--39)", rows_w)],
          "Panel A: the teen waves alternate between half A (1st, 3rd, ...) and half B; components: wage (father's and "
          "mother's ln wage), hours (their ln hours, mother's zero-hours share), spells (closures, layoffs, the father's "
          "unemployment and zero hours); the IV row instruments the half-A measures with the half-B measures; for spells "
          "the halves are different events, so the IV keeps the father's persistent propensity. Panel B: one row per son. "
          "Panel C: net worth with home equity, PSID 1984, 1989, 1994 and 1999 on, mean over the wealth waves at the son's "
          "12--20; split of Table~\\ref{tab:passed_on} panel B with and without wealth on the same 2,828 sons. 200 "
          "cluster-bootstrap draws of 1968 families. " + src("96.SplitMeasurementError.py", "97.RestIdentification.py",
                                                            "98.ParentalWealth.py"))


def t_ige_baseline():
    B = J("baseline_profile")
    heads = ["Pooled", "White", "Black", "White $-$ Black", "Pooled, family income"]
    rows = []
    for b in ("25-29", "30-34", "35-39", "40-44", "45-49", "50-55"):
        e, f = B["ly"][b], B["lfam"][b]
        rows.append((b.replace("-", "--"), [cell(e["pooled"]), cell(e["white"]), cell(e["black"]), cell(e["gap"]),
                                            cell(f["pooled"])]))
    rows.append(("Change 45--49 minus 25--29", [cell(B["ly"]["change"]), "", "", "", cell(B["lfam"]["change"])]))
    rows.append(("Sons at 25--29 / 45--49", [f"{B['ly']['25-29']['sons']:,} / {B['ly']['45-49']['sons']:,}", "", "", "", ""]))
    rows_b = []
    for lab, key in (("Born 1951--64", "born 1951-64"), ("Born 1965--79", "born 1965-79"),
                     ("Born 1980--89 (to 40--44)", "born 1980-89"), ("Income-year fixed effects", "income-year fixed effects"),
                     ("Income years 1990--2010 only", "income years 1990-2010 only")):
        e = B[f"B|{key}"]
        rows_b.append((lab, [cell(e["change"]), "", "", "", ""]))
    table("tab_ige_baseline", "The IGE of sons' earnings by age at measurement, baseline sample (PSID)", "tab:ige_baseline",
          heads, [("A. IGE of ln earnings by age band (column 5: ln family income)", rows),
                  ("B. Change 45--49 minus 25--29 in the pooled earnings IGE, by cohort and net of calendar time", rows_b)],
          "The paper's baseline sample: 4,770 sons with parental income over at least three of their ages 13--19, son-years "
          "at 25--55 (earnings: valid years). Band regressions with single-age dummies; pooled estimates use PSID weights, "
          "race-specific ones are unweighted; standard errors clustered by 1968 family. Appendix Table~\\ref{tab:ige_sons} "
          "reports the profile on all sons with a measured parental income. " + src("113.BaselineProfile.py"))


def t_age_period():
    A = J("nlsy97_afqt")
    N = J("nlsy79_youth_afqt")
    heads = ["25--29", "40--44", ""]
    a97 = A["learn_v|B|c:afqt"]
    i97 = A["learn_v|A|b0"]
    n79 = N["sons|pooled|son's AFQT, B"]["bands"]
    rows_a = [("NLSY97 (born 1980--84): IGE", [cell(i97["25-29"]), cell(i97["40-44"]), ""]),
              ("NLSY97: son's AFQT contribution", [cell(a97["25-29"]), cell(a97["40-44"]), ""]),
              ("NLSY79 (born 1957--64): son's AFQT contribution", [cell(n79[0]), cell(n79[3]), ""])]
    table("tab_age_period", "Age or period? The son's AFQT in the IGE in two cohorts twenty years apart",
          "tab:age_period", heads[:2], [("The son's AFQT in the IGE of ln earnings, at 25--29 and 40--44",
                                         [(lab, cells[:2]) for lab, cells in rows_a])],
          "Exact Gelbach split with the son's AFQT as its own group (NLSY97: ASVAB math-verbal percentile, standardised "
          "within birth year; parental income = the 1996 parent report; NLSY79: AFQT-3, 1979--81 parental income); 200 "
          "cluster-bootstrap draws of households. " + src("94.NLSY97AFQT.py", "87.NLSY79YouthAFQT.py"))


def t_layoff_mechanism():
    P = J("father_path_recession")
    D = J("daughters_mechanism")
    M = J("layoff_career_mechanism")
    heads = ["Estimate"]
    rows_p = [("Father unemployed (share of years)", [cell(P["path|f_sh_layoff"]["fp_unemp"])]),
              ("Father laid off again (share of years)", [cell(P["path|f_sh_layoff"]["fp_lay"])]),
              ("Father's ln earnings", [cell(P["path|f_sh_layoff"]["fp_ly"])]),
              ("Father employed (share of years)", [cell(P["path|f_sh_layoff"]["fp_emp"])])]
    k1 = "bad|bad times (sector decline or high state unemployment)|"
    rows_b = [("Bad-times layoffs: change 45--49 minus 25--29", [cell(P[k1 + "lay_bad"]["ch"])]),
              ("Other layoffs: change 45--49 minus 25--29", [cell(P[k1 + "lay_good"]["ch"])]),
              ("Bad-times layoffs: within son $\\times$ age", [cell(P[k1 + "lay_bad"]["fe"])]),
              ("Other layoffs: within son $\\times$ age", [cell(P[k1 + "lay_good"]["fe"])]),
              ("\\quad equal within son: $p$", [f"{P[k1 + 'wald'][2]:.3f}"])]
    rows_m = [("ln hourly wage", [cell(M["ln hourly wage"]["ch"])]),
              ("\\quad occupation wage score (between occupations)", [cell(M["occupation wage score (between)"]["ch"])]),
              ("\\quad wage within the occupation", [cell(M["wage within the occupation (within)"]["ch"])]),
              ("Same-employer annual wage growth", [cell(M["same-employer annual wage growth"]["ch"])]),
              ("Displaced in the year", [cell(M["displaced (closure / layoff) in the year"]["ch"])]),
              ("Tenure with the employer (years), at 45--49", [cell(M["tenure with the employer (years)"]["b"])]),
              ("Good job at 25--34 (one row per son)", [cell(M["G25"])]),
              ("Within-son ln earnings slope, early job held fixed", [cell(M["fe_early"]["early_fixed"])])]
    rows_d = [("Daughters: ln wage within person, + partnered and full year", [cell(D["daughters|ln hourly wage | partnered, full year"]["fe"])]),
              ("Daughters: employed, within person", [cell(D["daughters|employed"]["fe"])]),
              ("Daughters: partner's ln earnings, change", [cell(D["daughters|partner's ln earnings"]["change"])]),
              ("Daughters: earnings with zeros (Poisson), change", [cell(D["daughters|ppml"]["change"])]),
              ("Sons: earnings with zeros (Poisson), change", [cell(D["sons|ppml"]["change"])])]
    table("tab_layoff_mechanism", "What kind of father, which layoffs, where in the son's career, and the daughters (PSID)",
          "tab:layoff_mechanism", heads,
          [("A. The father at the son's 20--24, on the teen layoff share", rows_p),
           ("B. Layoffs in bad times (sector decline or high state unemployment) and other layoffs, son's ln earnings", rows_b),
           ("C. The son's career: change 45--49 minus 25--29 unless stated", rows_m),
           ("D. Daughters and sons, one reduced specification", rows_d)],
          "Coefficients of the father's teen layoff share (per unit share; one layoff year = one seventh). Panel A: one "
          "row per father-present son, with ln parental income, the father's teen-window ln wage and ln hours and "
          "cohort dummies. Panels B--C: at equal ln parental income and every component of Table~\\ref{tab:passed_on} "
          "panel A; band changes with 200 common bootstrap draws, within-son slopes clustered by 1968 family. Panel B: "
          "a bad-times layoff year is one in which national employment of the father's sector fell or his state's "
          "unemployment rate was at least a point above its 1976--2023 mean. Panel C: the son's ln wage is his "
          "occupation's CPS wage score plus his wage within it; a good job is a modal occupation $\\times$ industry cell "
          "at 25--34 in the well-paid, fast-growing set. Panel D: the specification of Table~\\ref{tab:layoff_exog} "
          "panel B. " + src("104.FatherPathRecession.py", "105.DaughtersMechanism.py", "106.LayoffCareerMechanism.py"))


def t_referee():
    Q = J("layoff_referee_checks")
    D = J("daughters_referee_checks")
    MT = J("multiple_testing")
    heads = ["Estimate"]
    E = Q["event"]
    rows_e = [(f"Father's ln earnings, event time {k}", [cell(E["ly"]["coef"][str(k)])]) for k in (-6, -4, -3, -2, 0, 1, 3, 6)]
    rows_e.append(("\\quad pre-event coefficients jointly zero: $p$", [f"{E['ly']['pre_wald'][2]:.3f}"]))
    rows_e.append(("Father employed, event time +1", [cell(E["emp"]["coef"]["1"])]))
    rows_e.append(("\\quad pre-event coefficients jointly zero: $p$", [f"{E['emp']['pre_wald'][2]:.3f}"]))
    P = Q["placebo27"]
    cb = Q["closure_bound"]
    rows_p = [("Layoff share at the son's 27--35 $\\times$ age", [cell(P["later"])]),
              ("\\quad teen layoff share $\\times$ age, same sons", [cell(P["teen"])]),
              ("Largest closure cost in the 95\\% interval, as a share of the layoff change", [f"{cb['share_of_layoff']:.0%}".replace("%", "\\%")]),
              ("Minimum detectable layoff change / within-son slope", [f"{cb['mde_layoff']:.3f} / {cb['mde_fe']:.3f}"]),
              ("Rank change (percentiles), 45--49 minus 25--29", [cell(Q["rank|f_sh_layoff"]["ch"])])]
    rows_d = [("Mother employed in the father's layoff waves (child FE)", [cell(D["mother|m_emp"])]),
              ("Daughters' slope $\\times$ (mother worked more after the layoff)", [cell(D["momup|daughters"]["inter"])]),
              ("Daughters observed with a wage at 45--49, on the layoff share", [cell(D["observed|daughters|4"][:2])]),
              ("Daughters' within-person wage slope, inverse-probability weighted", [cell(D["ipw|daughters"][1])]),
              ("Sons' within-person wage slope, inverse-probability weighted", [cell(D["ipw|sons"][1])]),
              ("Years of schooling, daughters minus sons", [cell(D["schooling"]["diff"])])]
    RW = J("romano_wolf")
    rows_m = []
    for k, kr, lab in (("A. The layoff cost|layoff band change (91)", "A. The layoff cost|layoff band change",
                        "Layoff change (family of 6)"),
                       ("A. The layoff cost|layoff within-son slope (88)", "A. The layoff cost|within-son slope",
                        "Within-son slope (family of 6)"),
                       ("B. Sons vs daughters|daughters - sons, wage change", "B. Sons vs daughters|daughters - sons, wage change",
                        "Daughters $-$ sons, wage change (family of 4)"),
                       ("B. Sons vs daughters|daughters - sons, wage within person",
                        "B. Sons vs daughters|daughters - sons, wage within person", "Daughters $-$ sons, wage within person")):
        rows_m.append((lab, [f"{MT[k]['p']:.4f} $\\to$ {MT[k]['adj']:.4f} / {RW[kr]['rw']:.4f}"]))
    table("tab_layoff_referee", "Pre-trends, a later-layoff placebo, bounds, ranks, the daughters' selection and multiple testing (PSID)",
          "tab:layoff_referee", heads,
          [("A. The father around his first layoff in a son's teens (event study; reference: one year before)", rows_e),
           ("B. Placebo, bounds and ranks", rows_p),
           ("C. The daughters: the mother, who is observed, schooling", rows_d),
           ("D. Multiple testing: $p$ $\\to$ adjusted $p$ (Holm / Romano--Wolf)", rows_m)],
          "Panel A: father-years at 25--64 of the fathers of father-present sons; father and calendar-year fixed effects and "
          "single-age dummies; event time binned at $-6$ and $+6$; treated = the 212 fathers with a layoff in a son's "
          "teen window. Panel B: within-son design of Table~\\ref{tab:layoff_selection}; minimum detectable effects for 80\\% "
          "power at 5\\%; ranks are weighted percentiles within single year of age $\\times$ calendar year. Panel C: the "
          "reduced specification of Table~\\ref{tab:layoff_exog} panel B; inverse-probability weights from a logit of being "
          "observed with a wage in the band. Panel D: families fixed before adjusting (six tests of the layoff cost; four "
          "of the sons--daughters difference); Romano--Wolf step-down from 1,000 joint cluster-bootstrap draws of 1968 "
          "families. Clustered by 1968 family. " + src("108.LayoffRefereeChecks.py", "109.DaughtersRefereeChecks.py",
                                                     "110.MultipleTesting.py", "114.RomanoWolf.py"))


def t_split_main():
    F = J("what_is_passed_on_rest")
    W = J("parental_wealth")
    k = "+ wealth: within-birth-year rank|groups|"
    rows_def = [("wage", "Parents' hourly wage"), ("parents' schooling", "Parents' schooling"), ("wealth", "Parents' net worth"),
                ("stability", "Parents' spells out of work"), ("hours", "Parents' hours"), ("group", "State labor market"),
                ("transfers", "Transfers (AFDC/TANF years, transfer share)"), ("assets", "Asset income, home ownership"),
                ("earnings", "Labor income beyond wage and hours"), ("others", "Other members' income"),
                ("family size", "Family size"), ("b", "Rest: parental income at equal measures")]
    heads = ["All sons, 25--55", "Born 1964+, 25--29", "Born 1964+, 35--39", "Born 1964+, 25--55"]
    rows = []
    for g, lab in rows_def:
        full = F.get(f"pooled|ly|{g}", {}).get("B_share") if g != "wealth" else None
        cells = [cell(full, pct=True) if full else "---"]
        for c_ in ("25-29", "35-39", "25-55"):
            v = W[k + c_].get(g)
            cells.append(cell(v, pct=True) if v else "")
        rows.append((lab, cells))
    rows.append(("IGE of ln earnings", [cell(F["pooled|ly|b0"][3])] +
                 [cell(W[f"+ wealth: within-birth-year rank|{c_}"]["b0"]) for c_ in ("25-29", "35-39", "25-55")]))
    table("tab_split_main", "The components of the IGE: shares of the IGE of sons' earnings (PSID)", "tab:split_main", heads,
          [("Share of the IGE (\\%)", rows)],
          "Exact Gelbach split of the IGE of sons' ln earnings into parental components (means over the son's ages "
          "13--19) and the rest, parental income at equal measures. Column 1: all sons, without wealth (the PSID measures "
          "net worth only from 1984). Columns 2--4: sons born 1964 and later, whose teens fall in the wealth waves, with "
          "parental net worth (rank within the son's birth year, mean over the wealth waves at 12--20). What holds in every "
          "version (Appendix~B: the original split, the measurement-error correction, four data sets): the parents' wage "
          "carries a fifth or more, wealth between a seventh (inverse hyperbolic sine) and three tenths (rank) where it is measured, mostly housing, the parents' schooling an eighth without "
          "wealth and less with it, spells a few percent, hours and place nothing. PSID weights; "
          "200 cluster-bootstrap draws of 1968 families. " + src("80.WhatIsPassedOnRest.py", "98.ParentalWealth.py"))


if __name__ == "__main__":
    t_layoff_selection()
    t_layoff_exog()
    t_split_robust()
    t_age_period()
    t_eitc()
    t_layoff_mechanism()
    t_referee()
    t_split_main()
    t_ige_baseline()
