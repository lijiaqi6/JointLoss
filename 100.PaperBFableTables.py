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
    rows_u = [("Layoff share $\\times$ replacement rate $\\times$ age", [cell(U["fe|rr (1 s.d.)"]["lay_rr_z_xa"])]),
              ("\\quad + layoff share $\\times$ father's ln wage $\\times$ age", [cell(U[f"fe|{k}"]["lay_rr_z_xa"])]),
              ("Placebo: father's ln wage $\\times$ replacement rate $\\times$ age", [cell(U[f"fe|{k}"]["flw_rr_z_xa"])])]
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
          "state-at-17 $\\times$ age. " + src("93.LayoffIndustryShocks.py", "92.LayoffDaughters.py",
                                                  "99.SimulatedReplacementRate.py"))


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


def t_age_period():
    P = J("pooled_rise_checks")
    A = J("nlsy97_afqt")
    N = J("nlsy79_youth_afqt")
    heads = ["25--29", "45--49", "Rise"]
    rows_p = []
    for lab, key in (("Baseline", "baseline"), ("Born 1951--64", "born 1951-64"), ("Born 1965--79", "born 1965-79"),
                     ("Born 1980--89 (to 40--44)", "born 1980-89"), ("Income-year fixed effects", "income-year FE"),
                     ("IGE $\\times$ cohort, at the 1965 cohort", "IGE x cohort (1965 cohort)"),
                     ("Period-varying IGE, at 1995", "period-varying IGE (at 1995)"),
                     ("Income years 1990--2010 only", "fixed window, income years 1990-2010")):
        e = P[f"learn|{key}"]
        rows_p.append((lab, [cell(e["first"][:2]), cell(e["last"][:2]), cell(e["rise"][:2])]))
    a97 = A["learn_v|B|c:afqt"]
    i97 = A["learn_v|A|b0"]
    n79 = N["sons|pooled|son's AFQT, B"]["bands"]
    rows_a = [("NLSY97 (born 1980--84): IGE", [cell(i97["25-29"]), cell(i97["40-44"]), ""]),
              ("NLSY97: son's AFQT contribution", [cell(a97["25-29"]), cell(a97["40-44"]), ""]),
              ("NLSY79 (born 1957--64): son's AFQT contribution", [cell(n79[0]), cell(n79[3]), ""])]
    table("tab_age_period", "Age or period? The pooled rise of the IGE and the son's AFQT in two cohorts",
          "tab:age_period", heads, [("A. PSID sons, ln earnings, IGE by band", rows_p),
                                    ("B. The son's AFQT in the IGE of ln earnings (columns 1--2: 25--29 and 40--44)", rows_a)],
          "Panel A: Black and White sons pooled with PSID weights, ages 25--49; single-age dummies and the parent's age "
          "quartic; rise = 45--49 minus 25--29 (40--44 for the 1980--89 cohort); standard errors clustered by 1968 family. "
          "Panel B: exact Gelbach split with the son's AFQT as its own group (NLSY97: ASVAB math-verbal percentile, "
          "standardised within birth year; parental income = the 1996 parent report; NLSY79: AFQT-3, 1979--81 parental "
          "income); 200 cluster-bootstrap draws of households. " + src("95.PooledRiseChecks.py", "94.NLSY97AFQT.py",
                                                                      "87.NLSY79YouthAFQT.py"))


if __name__ == "__main__":
    t_layoff_selection()
    t_layoff_exog()
    t_split_robust()
    t_age_period()
