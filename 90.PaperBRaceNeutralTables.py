r"""LaTeX tables for the race-neutral Paper B (PI decision 2026-10-20; outline proposals/paperB_outline_race_neutral_20261020.md).

Reads only saved estimates (nothing is re-estimated):
  output/what_is_passed_on.json (75), what_is_passed_on_rest.json (80), cya_what_is_passed_on.json (83),
  nlsy97_what_is_passed_on.json (85), nlsy79_youth_what_is_passed_on.json (86), nlsy79_youth_afqt.json (87),
  layoff_cost_by_age.json (88), shea_contrast_by_spell.json (89), friction_ige_pooled.json (74),
  ui_stability_channel.json (82), group_friction_by_race.json (84), stability_opening_by_race.json (81)
and writes paperB_age_profile/tab_passed_on.tex, tab_passed_on_data.tex, tab_skill_entry.tex, tab_layoff_age.tex,
tab_layoff_fe.tex, tab_shea_spell.tex, tab_son_friction.tex, tab_ui_stability.tex, tab_group_race.tex,
tab_passed_on_race.tex. Layout and helpers of 28.PaperBTables.py (coefficient with stars, s.e. below; p-values from
the bootstrap s.e., normal approximation, as in the source scripts).

Run:  python IGE/90.PaperBRaceNeutralTables.py
"""
import importlib.util
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
_s = importlib.util.spec_from_file_location("t28", HERE / "28.PaperBTables.py")
T = importlib.util.module_from_spec(_s)
_s.loader.exec_module(T)
table, num, head = T.table, T.num, T.head
STARS = T.STARS


def J(name):
    return json.load(open(OUT / f"{name}.json", encoding="utf-8"))


def pv(b, s):
    if b is None or s is None or not s or not math.isfinite(s):
        return None
    return math.erfc(abs(b / s) / math.sqrt(2))


def cell(t, dec=3, pct=False):
    """[est, se] -> (top, bottom); pct: shown in percent."""
    if t is None:
        return ("", "")
    b, s = float(t[0]), float(t[1])
    k = 100.0 if pct else 1.0
    return T.coef(b * k, s * k, pv(b, s), 1 if pct else dec)


def src(*scripts):
    return ("Source: " + ", ".join(rf"\texttt{{IGE/{x}}}" for x in scripts)
            + r"; table built by \texttt{IGE/90.PaperBRaceNeutralTables.py}. " + STARS)


# ================================================================ 1. what is passed on (PSID)
def t_passed_on():
    A, B = J("what_is_passed_on"), J("what_is_passed_on_rest")
    pre = "pooled: earnings, wage and hours (valid years; earnings = wage + hours)|ly|"
    b0 = A[pre + "b0"]
    heads = ["25--29", "35--39", "45--49", "25--55", "Opening|45--49 minus|25--29", "Share of|the IGE,|25--55 (\\%)"]
    # the IGE's opening is not stored in 75's json; 74 has it on the same son-years and draws (0.167***)
    op = J("friction_ige_pooled")["1b|ly|b0"][7]
    rows_a = [("IGE", [cell(x) for x in b0] + [cell(op), ""])]
    lab_a = [("wage", "Parents' hourly wage"), ("hours", "Parents' hours"), ("stability", "Parents' spells (stability)"),
             ("group", "Place (state unemployment, labour demand)"), ("structure", "Family structure"),
             ("b", "Rest: parental income at equal components")]
    for g, lab in lab_a:
        e = A[pre + g]
        rows_a.append((lab, [cell(x) for x in e["contrib"]] + [cell(e["share"][2], pct=True)]))
    lab_b = [("wage", "Parents' hourly wage"), ("hours", "Parents' hours"), ("stability", "Parents' spells (stability)"),
             ("group", "Place"), ("parents' schooling", "Parents' schooling"),
             ("transfers", "Transfers (transfer share, AFDC/TANF years)"), ("assets", "Assets (asset income, home ownership)"),
             ("others", "Other members' income"), ("family size", "Family size"),
             ("earnings", "Parents' labour income beyond the components"), ("structure", "Family structure"),
             ("b", "Rest: parental income at equal measured resources")]
    rows_b = []
    for g, lab in lab_b:
        e = B[f"pooled|ly|{g}"]
        rows_b.append((lab, [cell(x) for x in e["B_contrib"]] + [cell(e["B_share"], pct=True)]))
    table("tab_passed_on", "What is passed on: the earnings IGE split into the parents' components (PSID sons)",
          "tab:passed_on", heads,
          [("A. The four components", rows_a), ("B. With the parents' other resources", rows_b)],
          "Contributions to the IGE of sons' ln annual earnings (valid years) on ln parental family income (mean over "
          "the son's ages 13--19): exact \\citet{gelbach2016covariates} split, each component's contribution = its "
          "gradient in parental income times its partial relation to the son's earnings; the rows of a panel sum to the "
          "IGE. Components (means over the son's ages 13--19): wage = father's and mother's mean ln hourly wage; hours = "
          "their mean ln annual hours, the mother's years without work; spells = the father's shares of years with a "
          "plant closure, a layoff or firing, unemployment, zero hours, the variance of his transitory earnings, and the "
          "mother's share of years unemployed; place = state unemployment rate and men's Bartik shock at 12--18. Panel "
          "B adds the PSID family-file income sources, home ownership, the number of children and the parents' years of "
          "schooling. Missing measures are set to the weighted mean of the observed with a flag in the family-structure "
          "row. PSID weights; 4,770 sons, 46,540 son-years; standard errors from 200 cluster-bootstrap draws of 1968 "
          "families. " + src("75.WhatIsPassedOn.py", "80.WhatIsPassedOnRest.py"))


# ================================================================ 1b. the 4 x 4 table
def t_four_by_four():
    A = J("what_is_passed_on")
    heads = ["Son's ln|hourly wage", "Son's ln hours|(employed)", "Son|employed", "Son's share|of years|unemployed",
             "Son's share|of years|displaced"]
    lab = {"lyp": "Ln parental income", "f_lw": "Father's ln hourly wage", "m_lw": "Mother's ln hourly wage",
           "f_lh": "Father's ln annual hours", "m_lh": "Mother's ln annual hours", "m_sh_zero": "Mother's years without work",
           "m_nowork": "Mother works fewer than two years", "f_sh_close": "Father's plant closures",
           "f_sh_layoff": "Father laid off or fired", "f_sh_unemp": "Father's unemployment", "f_sh_zero": "Father's zero-hours years",
           "f_vtr": "Father's transitory earnings variance", "f_na": "Father present, not measured",
           "m_sh_unemp": "Mother's unemployment", "g_ur": "State unemployment, 12--18", "g_bart": "Men's labour-demand shock, 12--18"}
    panels = []
    for title, keys in (("A. Parental income", ["lyp"]), ("B. Wage", ["f_lw", "m_lw"]),
                        ("C. Hours", ["f_lh", "m_lh", "m_sh_zero", "m_nowork"]),
                        ("D. Spells", ["f_sh_close", "f_sh_layoff", "f_sh_unemp", "f_sh_zero", "f_vtr", "f_na", "m_sh_unemp"]),
                        ("E. Place", ["g_ur", "g_bart"])):
        panels.append((title, [(lab[k], [cell(x) for x in A[f"4x4|pooled|{k}"]]) for k in keys]))
    table("tab_four_by_four", "What passes to what: each parental component and each of the son's outcomes (PSID)",
          "tab:four_by_four", heads, panels,
          "Each column is one regression of the son's outcome (son-years 25--55) on ln parental income and every "
          "component of Table~\\ref{tab:passed_on}, panel A, each standardised (one standard deviation), with the "
          "family-structure flags and single-age dummies; PSID weights; standard errors clustered by 1968 family. "
          "Columns (1)--(2): 42,225 son-years of 4,644 sons; (3)--(5): 46,540 of 4,770. " + src("75.WhatIsPassedOn.py"))


# ================================================================ 2. the same split in four data sets
def t_passed_on_data():
    B, C, N79, N97 = J("what_is_passed_on_rest"), J("cya_what_is_passed_on"), J("nlsy79_youth_what_is_passed_on"), \
        J("nlsy97_what_is_passed_on")
    heads = ["PSID|sons|25--55", "NLSY79 CYA|children|26--35", "NLSY79 CYA|sons|26--35", "NLSY79|sons|25--59",
             "NLSY97|youths|25--44"]

    def cya(s, g):
        k = f"{s}|learn2635|{g}"
        return C[k]["pooled"] if g == "b0" else C[k + "|share"]["pooled"]

    def n79(g):
        return N79["sons|pooled|b0"]["25-59"] if g == "b0" else N79.get(f"sons|pooled|{g}|share")

    def n97(g):
        return N97["learn_v|sons and daughters|pooled|b0"]["25-44"] if g == "b0" else \
            N97.get(f"learn_v|sons and daughters|pooled|{g}|share")

    def psid(g):
        return B["pooled|ly|b0"][3] if g == "b0" else B[f"pooled|ly|{g}"]["B_share"]

    rows = [("IGE", [cell(psid("b0")), cell(cya("sons and daughters", "b0")), cell(cya("sons", "b0")), cell(n79("b0")),
                     cell(n97("b0"))])]
    spec = [("Parents' wage", "wage", "wage", "wage", "wage"), ("Parents' hours", "hours", "hours", "hours", "hours"),
            ("Parents' spells (stability)", "stability", "stability", None, "breaks"),
            ("Place", "group", "group", "group", "group"),
            ("Parents' schooling (and other resources)", "parents' schooling", None, "resources", "resources"),
            ("Family structure", "structure", "structure", "structure", "structure"),
            ("Rest", "b", "b", "b", "b")]
    for lab, gp, gc, g79, g97 in spec:
        rows.append((lab + r" (\%)", [cell(psid(gp), pct=True),
                                       cell(cya("sons and daughters", gc), pct=True) if gc else ("", ""),
                                       cell(cya("sons", gc), pct=True) if gc else ("", ""),
                                       cell(n79(g79), pct=True) if g79 else ("", ""),
                                       cell(n97(g97), pct=True) if g97 else ("", "")]))
    table("tab_passed_on_data", "What is passed on in four data sets: shares of the earnings IGE",
          "tab:passed_on_data", heads, [("", rows)],
          "First row: the IGE of the child's ln earnings on ln parental income; other rows: each component's share of it "
          "(percent; exact Gelbach split). PSID: Table~\\ref{tab:passed_on}, panel B (parents' schooling row = schooling "
          "only; transfers, assets, others' income, family size and labour income beyond the components are in the "
          "table but not here). NLSY79 Children and Young Adults: the mother is the respondent; components over the "
          "child's ages 13--17 from her weekly array and job roster (weeks unemployed, jobs ended by a closure, a "
          "layoff, a firing), her annual hours and wages and her spouse's; place = census-region unemployment (no state "
          "in the public file); outcome = mean earnings at 26--35. NLSY79 youths: the household at 14 (occupation wage "
          "of the adult man and woman from the March CPS 1977--80, whether each worked for pay, South / rural, parents' "
          "schooling and reading materials); no measure of spells. NLSY97: the 1997 parent interview (one year of "
          "wages and usual hours, employment breaks of six months or more in the youth's life without their reason, "
          "1996 transfers, parents' schooling, census region). Weights of each data set; bootstrap draws of 1968 "
          "families (PSID), mothers (CYA), 1979 / 1997 households (NLSY79 / NLSY97). "
          + src("80.WhatIsPassedOnRest.py", "83.CYAWhatIsPassedOn.py", "86.NLSY79YouthWhatIsPassedOn.py",
                "85.NLSY97WhatIsPassedOn.py"))


# ================================================================ 3. skill at entry (NLSY79, AFQT)
def t_skill_entry():
    K = J("nlsy79_youth_afqt")
    idx = [0, 2, 4, 5, 7]                                           # 25-29, 35-39, 45-49, 50-54, 25-59
    heads = ["25--29", "35--39", "45--49", "50--54", "25--59", "Opening|50--54 minus|25--29"]
    spec = [("IGE (b0)", "IGE"), ("son's AFQT, B", "The son's AFQT"),
            ("father's schooling element, A", "Father's schooling, without the son's AFQT"),
            ("father's schooling element, B (with AFQT)", "Father's schooling, with the son's AFQT"),
            ("parents' schooling + reading, A", "Parents' schooling and reading, without AFQT"),
            ("parents' schooling + reading, B", "Parents' schooling and reading, with AFQT"),
            ("rest, A", "Rest, without AFQT"), ("rest, B", "Rest, with AFQT")]
    panels = []
    for race, title in (("pooled", "A. Sons, pooled"), ("White", "B. White sons"), ("Black", "C. Black sons")):
        rows = []
        for key, lab in spec:
            e = K[f"sons|{race}|{key}"]
            rows.append((lab, [cell(e["bands"][i]) for i in idx] + [cell(e["open"])]))
        ab = K[f"sons|{race}|f_hgc A-B"]
        rows.append((r"Father's schooling through the son's AFQT", [cell(ab[i]) for i in idx]
                     + [cell(K[f"sons|{race}|f_hgc A-B open"])]))
        panels.append((title, rows))
    table("tab_skill_entry", "Why the IGE rises with age: the son's skill at entry and the parents' schooling (NLSY79)",
          "tab:skill_entry", heads, panels,
          "Contributions to the IGE of sons' ln annual earnings on ln parental income (mean 1978--80) in each age band; "
          "exact Gelbach split with the components of Table~\\ref{tab:passed_on_data}, column (4), without (A) and with "
          "(B) the son's AFQT (AFQT-3, 1980 ASVAB at ages 15--23, standardised within birth year). 'Through the son's "
          "AFQT' = the father's-schooling contribution without minus with AFQT, on common bootstrap draws. NLSY79 "
          "Black and White youths living with a parent in 1979--81; 1979 weights; 200 cluster-bootstrap draws of 1979 "
          "households. " + src("86.NLSY79YouthWhatIsPassedOn.py", "87.NLSY79YouthAFQT.py"))


# ================================================================ 4. the cost of a childhood layoff by age
def t_layoff_age():
    L = J("layoff_cost_by_age")
    heads = ["25--29", "30--34", "35--39", "40--44", "45--49", "50--55", "Change|45--49 minus|25--29"]
    panels = []
    for spec, title in (("single-age dummies", "A. Ln earnings, single-age dummies"),
                        ("+ 5-year birth-cohort dummies", "B. Ln earnings, with five-year birth-cohort dummies")):
        rows = []
        for race, v, lab in (("pooled", "f_sh_layoff", "Father laid off or fired, all sons"),
                             ("pooled", "f_sh_close", "Father's plant closed, all sons"),
                             ("White", "f_sh_layoff", "Father laid off or fired, White sons"),
                             ("Black", "f_sh_layoff", "Father laid off or fired, Black sons")):
            e = L[f"bands|{spec}|{race}|{v}"]
            rows.append((lab, [cell(x) for x in e["g"]] + [cell(e["change"])]))
        panels.append((title, rows))
    rows = []
    for y, lab in (("ly", "ln annual earnings"), ("lw", "ln hourly wage"), ("lh", "ln annual hours (employed)"),
                   ("emp", "employed"), ("sb_unemp", "his share of years unemployed")):
        e = L[f"outcome|pooled|{y}"]
        rows.append(("All sons: " + lab, [cell(e["a"]), "", "", "", cell(e["b"]), "", cell(e["ch"])]))
    panels.append(("C. Which outcome: father laid off or fired (columns 25--29, 45--49 and the change)", rows))
    table("tab_layoff_age", "A childhood layoff costs the son more as he ages (PSID)", "tab:layoff_age", heads, panels,
          "Coefficient of the father's share of the son's ages 13--19 with a layoff or firing (PSID 'laid off / fired') "
          "or a plant closure ('plant closed / moved') on the son's outcome in each age band, holding ln parental income "
          "and every component of Table~\\ref{tab:passed_on}, panel A, fixed; single-age dummies; PSID weights. The share "
          "is over seven years, so one year with a layoff is one seventh of the coefficient. Father present; mean "
          "layoff share 0.044, 12 percent of sons have a layoff year. Standard errors from 200 cluster-bootstrap draws "
          "of 1968 families. " + src("88.LayoffCostByAge.py"))
    F = L
    heads = ["White", "White,|with timing", "Black", "Black,|with timing", "All", "All,|with timing"]
    rows = []
    for v, lab in (("f_sh_layoff_xa", "Layoff share, ages 13--19, $\\times$ age"),
                   ("f_sh_close_xa", "Closure share, ages 13--19, $\\times$ age"),
                   ("lay_a6_xa", "Layoff share, ages 6--12, $\\times$ age"),
                   ("lay_a20_xa", "Layoff share, ages 20--26, $\\times$ age"),
                   ("clo_a6_xa", "Closure share, ages 6--12, $\\times$ age"),
                   ("clo_a20_xa", "Closure share, ages 20--26, $\\times$ age"),
                   ("lyp_xa", "Ln parental income $\\times$ age")):
        rows.append((lab, [cell(x) if x else ("", "") for x in F[f"fe|{v}"]]))
    table("tab_layoff_fe", "Within the same son: the earnings profile and the father's childhood layoffs (PSID)",
          "tab:layoff_fe", heads, [("", rows)],
          "Son-years 25--55, ln annual earnings (valid years) with son fixed effects; single-age dummies; every "
          "component of Table~\\ref{tab:passed_on}, panel A, ln parental income, the family-structure flags and "
          "five-year cohort dummies, each interacted with (age $-$ 40)/10. A coefficient is the change per ten years of "
          "age in the same son's ln earnings per unit share (one layoff year = one seventh). 'With timing' adds the "
          "father's layoff and closure shares at the son's ages 6--12 and 20--26 (his own head-years in the PSID) "
          "$\\times$ age. PSID weights; standard errors clustered by 1968 family. " + src("88.LayoffCostByAge.py"))


# ================================================================ 5. which spells pass on (Shea)
def t_shea():
    S = J("shea_contrast_by_spell")
    sets = [("(A) 74's set: father displaced / unemployed / zero hours, mother unemployed / zero hours",
             "All spells (father displaced, unemployed, zero hours; mother unemployed, zero hours)"),
            ("(B) father's plant closures only", "Father's plant closures"),
            ("(C) father's layoffs / firings only", "Father laid off or fired"),
            ("(D) father's unemployment share only", "Father's unemployment"),
            ("(E) mother's unemployment share only", "Mother's unemployment"),
            ("(F) father's closures + layoffs", "Father's closures and layoffs")]
    heads = ["$R^2$", "Predicted|part", "Rest", "Difference"]
    panels = []
    for y, title in (("ly", "A. Sons' ln earnings"), ("lw", "B. Sons' ln hourly wage")):
        rows = []
        for k, lab in sets:
            e = S[f"{y}|{k}"]
            rows.append((lab, [f"{e['R2']:.3f}", cell(e["bP"]), cell(e["bperp"]), cell(e["diff"])]))
        panels.append((title, rows))
    table("tab_shea_spell", "Parental income tied to spells: which spells pass on more strongly (PSID)",
          "tab:shea_spell", heads, panels,
          "Ln parental income (net of the family-structure flags and age dummies) is split into the part predicted by "
          "the spell measures in the row and the rest; the son's outcome is regressed on both parts. $R^2$ = share of the "
          "variance of ln parental income explained by the spells. Spell shares over the son's ages 13--19. Pooled sons "
          "25--55; PSID weights; 200 cluster-bootstrap draws of 1968 families. " + src("74.FrictionIGEPooled.py",
                                                                                         "89.SheaContrastBySpell.py"))


# ================================================================ 6. the son's own spells
def t_son_friction():
    F = J("friction_ige_pooled")
    heads = ["25--29", "30--34", "35--39", "40--44", "45--49", "50--55", "25--55", "Opening|45--49 minus|25--29"]
    rows = [("IGE", [cell(x) for x in F["1b|ly|b0"]]),
            ("The son's own spells", [cell(x) for x in F["1b|ly|c:son"]]),
            (r"\quad share of the IGE (\%)", [cell(x, pct=True) for x in F["1b|ly|share|c:son"]]),
            (r"\quad of which shared with the parents' spells", [cell(x) for x in F["1b|ly|shared"]]),
            ("The father's spells", [cell(x) for x in F["1b|ly|c:father"]]),
            ("The mother's spells", [cell(x) for x in F["1b|ly|c:mother"]]),
            ("Rest", [cell(x) for x in F["1b|ly|b"]])]
    rows_w = [("IGE", [cell(x) for x in F["1b|lw|b0"]]),
              ("The son's own spells", [cell(x) for x in F["1b|lw|c:son"]]),
              (r"\quad share of the IGE (\%)", [cell(x, pct=True) for x in F["1b|lw|share|c:son"]])]
    table("tab_son_friction", "The son's own search friction in the IGE, by age (PSID)", "tab:son_friction", heads,
          [("A. Sons' ln annual earnings", rows), ("B. Sons' ln hourly wage", rows_w)],
          "Exact Gelbach split of the IGE in each band into the son's own spells (his shares of the band's years "
          "unemployed, displaced and with zero hours), the father's and the mother's spells at the son's ages 13--19, "
          "family structure (not shown) and the rest. The son's spells are part of his own outcome: a year unemployed "
          "lowers that year's earnings. PSID weights; 200 cluster-bootstrap draws of 1968 families. "
          + src("74.FrictionIGEPooled.py"))


# ================================================================ 7. UI generosity
def t_ui():
    U = J("ui_stability_channel")
    heads = ["25--29", "35--39", "45--49", "25--55", "Share of|the IGE,|25--55 (\\%)"]
    rows = []
    for g, lab in (("b0", "IGE"), ("stability", "Parents' spells (stability)")):
        for hl, l2 in (("more generous", "more generous states"), ("less generous", "less generous states"),
                       ("diff", "difference")):
            e = U[f"split|{g}|{hl}"]
            sh = U.get(f"split|{g}|{hl}|share")
            rows.append((f"{lab}, {l2}", [cell(x) if x else ("", "") for x in e] + [cell(sh, pct=True) if sh else ""]))
    heads2 = heads
    rows2 = []
    for panel, plab in (("Pooled", "sons 25--55"), ("Pooled, ages 40-55", "sons 40--55")):
        for v, y, lab in (("f_sh_close_x_ui_z", "ly", "closure share $\\times$ UI, ln earnings"),
                          ("f_sh_layoff_x_ui_z", "ly", "layoff share $\\times$ UI, ln earnings"),
                          ("m_sh_unemp_x_ui_z", "sb_unemp", "mother's unemployment $\\times$ UI, son's years unemployed"),
                          ("f_lw_x_ui_z", "ly", "placebo: father's wage $\\times$ UI, ln earnings")):
            e = U.get(f"inter|ui_z|{panel}|{y}|{v}")
            rows2.append((f"{lab}, {plab}", [cell(e) if e else ("", "")] + ["", "", "", ""]))
    table("tab_ui_stability", "State unemployment insurance in childhood and the stability channel (PSID)",
          "tab:ui_stability", heads, [("A. Split by UI generosity relative to the son's cohort", rows),
                                      ("B. Interactions (first column; per standard deviation of each)", rows2)],
          "UI generosity = the state's maximum weekly benefit over its average weekly wage, mean over the son's ages "
          "12--18 in his state at 17 (DOL Significant Provisions; IGE/12b). Panel A: sons above and below the median of "
          "generosity net of five-year cohort means, Table~\\ref{tab:passed_on} panel A split in each half, common "
          "bootstrap draws. Panel B: the son's outcome on all components (one s.d.), ln parental income, UI and UI "
          "$\\times$ each element, with state fixed effects, five-year cohort and single-age dummies; standard errors "
          "clustered by 1968 family. Sons born 1958 and later (3,495). " + src("82.UIStabilityChannel.py"))


# ================================================================ 8. group friction
def t_group():
    G = J("group_friction_by_race")
    heads = ["Pooled", "White", "Black"]
    m = G["measure|g_jf"]
    rows_m = [("Men's monthly job finding, own race, state (White / Black mean)",
               [f"{m['means'][0]:.3f} / {m['means'][1]:.3f}", "", ""])]
    rows_m.append(("Black $-$ White", [cell(m["gap"], dec=4), "", ""]))
    rows_m.append(("Gradient in ln parental income", ["", cell(m["grad_W"], dec=4), cell(m["grad_B"], dec=4)]))
    rows = []
    for title_key, lab in (("75's group on the same sons", "State unemployment and labour demand"),
                           ("group with g_jf_z, g_jf_f_z", "+ job finding of men and women of the son's race")):
        cells = []
        for samp in ("pooled", "White", "Black"):
            e = G.get(f"{samp}, ln earnings, {title_key}|group")
            cells.append(cell(e["share"], pct=True) if e and e.get("share") else ("", ""))
        rows.append((lab + r" (\% of the IGE)", cells))
    table("tab_group_race", "Group search friction: job finding of the son's race in his state (CPS) and the IGE",
          "tab:group_race", heads, [("A. The measure (sons' childhood, 1994--2021)", rows_m),
                                    ("B. Share of the earnings IGE carried by the place component", rows)],
          "Job finding = monthly probability that a non-employed man (woman) aged 20--45 of the son's race in his state "
          "at 17 is employed the next month, CPS basic monthly 1994--2021 matched across months, pooled over the son's "
          "ages 12--18 (IGE/17). Panel A, first row: White / Black means. Panel B: the place component's share of the "
          "IGE in Table~\\ref{tab:passed_on} panel A's split, on the sons with the measure (born 1976 and later, 1,752). "
          + src("84.GroupFrictionByRace.py"))


def main():
    t_passed_on()
    t_four_by_four()
    t_passed_on_data()
    t_skill_entry()
    t_layoff_age()
    t_shea()
    t_son_friction()
    t_ui()
    t_group()


if __name__ == "__main__":
    main()
