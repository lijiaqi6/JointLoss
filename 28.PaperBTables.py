r"""LaTeX tables for Paper B (the age profile of intergenerational persistence), 2026-10-17.

Reads only the saved estimates of three scripts (nothing is re-estimated here):
  output/ige_by_age.csv          (26.IGEByAge.py)
  output/ige_decomposition.csv   (24.IGEDecomposition.py)
  output/career_wage_growth.csv  (27.CareerWageGrowth.py)
  output/industry_careers.csv    (32.IndustryCareers.py)
and writes paperB_age_profile/tab_*.tex.

Layout (PI's rules): one regression per column with the outcome in the header, regressors / groups as rows,
samples or age bands as row panels, coefficient with stars and the standard error in parentheses below, sample sizes at
the bottom of each panel. *** p<0.01, ** p<0.05, * p<0.1 (p-values as saved by the source script). Multi-line headers
use nested tabulars, never \shortstack. Every table is wrapped in \resizebox (shrunk to the text width when wider).

Run:  python IGE/28.PaperBTables.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
DEST = HERE / "paperB_age_profile"
DEST.mkdir(exist_ok=True)

A = pd.read_csv(OUT / "ige_by_age.csv")
D = pd.read_csv(OUT / "ige_decomposition.csv")
C = pd.read_csv(OUT / "career_wage_growth.csv")                  # 27.CareerWageGrowth.py

BANDS = ["25-29", "30-34", "35-39", "40-44", "45-49", "50-55", "31-37"]
GROUPS = ["Pooled (weighted)", "Black", "White", "White - Black"]
GLAB = {"Pooled (weighted)": "Pooled (weighted)", "Black": "Black", "White": "White",
        "White - Black": "White $-$ Black"}
TEST_ROWS = ["Equal in all bands (Wald chi2)", "Linear trend per 10 years", "Mean in bands < 35",
             "Mean in bands >= 35", "Mean < 35 minus mean >= 35"]
TEST_LAB = {"Equal in all bands (Wald chi2)": r"Equal in all bands: Wald $\chi^2$ [p-value]",
            "Linear trend per 10 years": "Linear trend per 10 years of age",
            "Mean in bands < 35": "Mean over bands below 35",
            "Mean in bands >= 35": "Mean over bands 35 and above",
            "Mean < 35 minus mean >= 35": "Opening: mean 35 and above minus mean below 35"}
MISSING = []


# ------------------------------------------------------------------------------------------------ formatting
def stars(p):
    if p is None or pd.isna(p):
        return ""
    return "^{***}" if p < 0.01 else "^{**}" if p < 0.05 else "^{*}" if p < 0.1 else ""


def num(x, dec=3):
    s = f"{x:.{dec}f}"
    if float(s) == 0:
        s = s.lstrip("-")                                          # no negative zero
    return s.replace("-", "$-$") if s.startswith("-") else s


def coef(est, se, p, dec=3):
    """(top line, bottom line) for a coefficient cell."""
    if est is None or pd.isna(est):
        return ("", "")
    top = f"${num(est, dec).replace('$', '')}{stars(p)}$"
    bot = f"({se:.{dec}f})" if se is not None and not pd.isna(se) else ""
    return (top, bot)


def chi2cell(est, p, note):
    df = ""
    if isinstance(note, str) and note.startswith("chi2("):
        df = note[5:note.index(")")]
    lab = f"$\\chi^2({df})={est:.2f}{stars(p)}$" if df else f"${est:.2f}{stars(p)}$"
    pv = "[$<$0.001]" if p < 0.001 else f"[{p:.3f}]"
    return (lab, pv)


def ints(x):
    return "" if x is None or pd.isna(x) else f"{int(round(x)):,}"


def head(text):
    """Multi-line column header as a nested tabular; lines separated by '|'."""
    return r"\begin{tabular}[b]{@{}c@{}}" + r"\\".join(text.split("|")) + r"\end{tabular}"


MAXLINES = 44                                                     # body lines per float before splitting


def _panel_lines(title, rows):
    n = 1 if title else 0
    for _, cells in rows:
        n += 2 if any(isinstance(c, tuple) and c[1] for c in cells) else 1
    return n


def table(name, caption, label, heads, panels, notes, first=""):
    """panels: list of (title, rows); a row is (label, [cells]) where a cell is a (top, bottom) pair or a string.
    Tables longer than MAXLINES body lines are split into consecutive floats ('continued'); the label is on the
    first part and the notes on the last. Each part is shrunk to the text width (and to 0.85 of the text height) only
    when it is larger."""
    k = len(heads)
    chunks, cur, n = [], [], 0
    for p in panels:
        m = _panel_lines(*p)
        if cur and n + m > MAXLINES:
            chunks.append(cur)
            cur, n = [], 0
        cur.append(p)
        n += m
    chunks.append(cur)
    L = []
    for c, chunk in enumerate(chunks):
        L += [r"\begin{table}[!htbp]", r"\centering"]
        if c == 0:
            L.append(r"\caption{" + caption + "}")
        else:                                                      # same table number for the continuation
            L += [r"\addtocounter{table}{-1}", r"\caption{" + caption + " (continued)}"]
        if c == 0:
            L.append(r"\label{" + label + "}")
        L += [r"\resizebox{\ifdim\width>\textwidth\textwidth\else\width\fi}{!}{%",
              r"\resizebox*{!}{\ifdim\totalheight>0.85\textheight 0.85\textheight\else\totalheight\fi}{%",
              r"\begin{tabular}{l" + "c" * k + "}", r"\toprule",
              first + " & " + " & ".join(head(h) for h in heads) + r" \\",
              " & " + " & ".join(f"({i + 1})" for i in range(k)) + r" \\", r"\midrule"]
        for j, (title, rows) in enumerate(chunk):
            if title:
                if j:
                    L.append(r"\addlinespace")
                L.append(r"\multicolumn{" + str(k + 1) + r"}{l}{\textit{" + title + r"}} \\")
            for lab, cells in rows:
                if any(isinstance(x, tuple) for x in cells):
                    tops = [x[0] if isinstance(x, tuple) else x for x in cells]
                    bots = [x[1] if isinstance(x, tuple) else "" for x in cells]
                    L.append(lab + " & " + " & ".join(tops) + r" \\")
                    if any(bots):
                        L.append(" & " + " & ".join(bots) + r" \\")
                else:
                    L.append(lab + " & " + " & ".join(cells) + r" \\")
        L += [r"\bottomrule", r"\end{tabular}}}"]
        if c == len(chunks) - 1:
            L += [r"\par\smallskip",
                  r"\begin{minipage}{\textwidth}\footnotesize \textit{Notes:} " + notes + r"\end{minipage}"]
        else:
            L += [r"\par\smallskip", r"\begin{minipage}{\textwidth}\footnotesize \textit{Continued on the next "
                                      r"table; notes below its last part.}\end{minipage}"]
        L.append(r"\end{table}")
    (DEST / f"{name}.tex").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {name}.tex ({len(chunks)} part{'s' if len(chunks) > 1 else ''})")


# ------------------------------------------------------------------------------------------------ lookups
def a_get(**kw):
    x = A
    for k, v in kw.items():
        x = x[x[k] == v]
    if len(x) == 0:
        MISSING.append(kw)
        return None
    return x.iloc[0]


FLIP = {"Black - White", "B-W change", "B-W gap 25-34", "B-W gap 35-55", "BW", "B-W change contribution",
        "Black-White", "gap", "dgap"}


def _flip(kw):
    """True when the stored estimate is Black - White (or its change) and not a ratio: the paper reports White - Black
    everywhere (2026-10-18)."""
    who = {str(kw.get(k)) for k in ("sample", "race", "group")}
    what = " ".join(str(kw.get(k, "")) for k in ("outcome", "term", "statistic")).lower()
    if "share" in what or "ratio" in what or " rr" in what:
        return False
    return bool(who & FLIP) or what.startswith("(6) b-w") or "(3) change of the b-w gap" in what


def a_coef(dec=3, **kw):
    r = a_get(**kw)
    return ("", "") if r is None else coef(r["est"], r["se"], r["p"], dec)


def d_get(**kw):
    x = D
    for k, v in kw.items():
        x = x[x[k] == v]
    if len(x) == 0:
        MISSING.append(kw)
        return None
    return x.iloc[0]


def d_coef(dec=3, **kw):
    r = d_get(**kw)
    sg = -1.0 if _flip(kw) else 1.0
    return ("", "") if r is None else coef(sg * r["estimate"], r["se"], r["p"], dec)


def test_cells(cols, **kw):
    """Rows of the band-equality tests for a list of column specs (dicts merged into kw)."""
    rows = []
    for st in TEST_ROWS:
        cells, any_ = [], False
        for c in cols:
            spec = dict(kw, **c)
            x = A
            for k, v in dict(spec, band="test", stat=st).items():
                x = x[x[k] == v]
            if len(x) == 0:
                cells.append("")
                continue
            r = x.iloc[0]
            any_ = True
            sg = -1.0 if st == "Mean < 35 minus mean >= 35" else 1.0
            cells.append(chi2cell(r["est"], r["p"], r["note"]) if "Wald" in st else coef(sg * r["est"], r["se"], r["p"]))
        if any_:
            rows.append((TEST_LAB[st], cells))
    return rows


def kids(**kw):
    """'Black / White' children (or n) of the Black and White rows."""
    out = []
    for g in ["Black", "White"]:
        r = a_get(group=g, **kw)
        out.append("" if r is None else ints(r["children"] if not pd.isna(r["children"]) else r["n"]))
    return " / ".join(out)


SRC_A = r"Source: \texttt{IGE/26.IGEByAge.py} (\texttt{output/ige\_by\_age.csv}); table built by \texttt{IGE/28.PaperBTables.py}."
SRC_D = (r"Source: \texttt{IGE/24.IGEDecomposition.py} (\texttt{output/ige\_decomposition.csv}); table built by "
         r"\texttt{IGE/28.PaperBTables.py}.")
STARS = r"$^{***}$ $p<0.01$, $^{**}$ $p<0.05$, $^{*}$ $p<0.1$."


# ================================================================================================ 26.IGEByAge
def tab_ige_age(sex, name, label):
    cols = [("log IGE, child-year", "ln own earnings"), ("log IGE, child-year", "ln family income"),
            ("log IGE, band mean", "ln own earnings"), ("log IGE, band mean", "ln family income")]
    heads = ["ln own earnings|(child-years)", "ln family income|(child-years)", "ln own earnings|(band mean)",
             "ln family income|(band mean)"]
    if sex == "Sons":                                              # main text: child-year columns only
        cols, heads = cols[:2], heads[:2]
    panels = []
    for b in BANDS:
        rows = []
        for g in GROUPS:
            rows.append((GLAB[g], [a_coef(data="PSID", analysis=an, sex=sex, sample="unbalanced", band=b, group=g,
                                          outcome=o, stat="IGE") for an, o in cols]))
        rows.append(("Children (Black / White)", [kids(data="PSID", analysis=an, sex=sex, sample="unbalanced",
                                                       band=b, outcome=o, stat="IGE") for an, o in cols]))
        title = f"Age {b.replace('-', '--')}" + (" (window of Chetty et al.)" if b == "31-37" else "")
        panels.append((title, rows))
    who = "sons" if sex == "Sons" else "daughters"
    table(name, f"Log IGE of {who}' income by age at measurement (PSID)", label, heads, panels,
          "Each cell is the coefficient on log parental family income (mean over the child's ages 13--19) from a "
          "separate regression of the outcome in the column header, within the age band of the panel. Child-year "
          "columns: child-years in the band, controls for a quartic in the parent's age and single-year age dummies; "
          "band-mean columns (daughters' table; for sons in \\texttt{output/ige\\_by\\_age.md}): one observation per "
          "child, log of the band mean ($\\geq 2$ years), quartic in the parent's age and the mean age. Black and White: unweighted; Pooled: all races, weighted by the core "
          "longitudinal weight. White $-$ Black is the difference of the two race-specific regressions, estimated "
          "jointly. Standard errors clustered by 1968 family in parentheses. Race is the race of the parental "
          "household head. " + STARS + " " + SRC_A, first="Age band / group")


def tab_age_tests():
    cols = [dict(outcome="ln own earnings"), dict(outcome="ln family income")]
    heads = ["ln own earnings", "ln family income"]
    spec = [("A. Pooled (weighted), all sons", "unbalanced", "Pooled (weighted)"),
            ("B. Black sons", "unbalanced", "Black"),
            ("C. White sons", "unbalanced", "White"),
            ("D. White $-$ Black", "unbalanced", "White - Black")]
    panels = []
    for title, smp, g in spec:
        panels.append((title, test_cells(cols, data="PSID", analysis="log IGE, child-year", sex="Sons",
                                         sample=smp, group=g)))
    table("tab_age_tests", "Does the log IGE of sons, and the racial gap in it, change with age? (PSID)",
          "tab:agetests", heads, panels,
          "Tests on the band-specific log IGEs of Table~\\ref{tab:ige_sons} (child-year design; bands 25--29 to "
          "50--55, the 31--37 window excluded), estimated jointly across bands in one stacked, fully interacted "
          "regression with standard errors clustered by 1968 family. Wald test of equality across bands "
          "(p-value in brackets); linear trend in the band midpoint per 10 years; mean of the band coefficients from 35 "
          "minus their mean below 35 (the opening). Bands 25--55 here; the robustness checks of Table~\\ref{tab:gaprobust} "
          "use bands 25--49 (opening 0.232$^{***}$ for earnings, 0.157$^{***}$ for family income). Race-specific weights "
          "and balanced panels: Table~\\ref{tab:gaprobust} and Appendix~\\ref{app:checks}. " + STARS + " " + SRC_A, first="Panel / statistic")


def tab_rank_age():
    cols = [("ln family income", "slope", 3), ("ln family income", "E[rank] p25", 1),
            ("ln family income", "E[rank] p75", 1), ("ln own earnings", "slope", 3)]
    heads = ["Rank--rank slope|family income", "Expected rank|at parental p25", "Expected rank|at parental p75",
             "Rank--rank slope|own earnings"]
    panels = []
    for b in BANDS:
        rows = []
        for g in GROUPS:
            rows.append((GLAB[g], [a_coef(dec, data="PSID", analysis="rank", sex="Sons", sample="unbalanced", band=b,
                                          group=g, outcome=o, stat=s) for o, s, dec in cols]))
        rows.append(("Children (Black / White)", [kids(data="PSID", analysis="rank", sex="Sons",
                                                       sample="unbalanced", band=b, outcome=o, stat=s)
                                                  for o, s, _ in cols]))
        panels.append((f"Age {b.replace('-', '--')}" + (" (window of Chetty et al.)" if b == "31-37" else ""), rows))
    rows = []
    for st in ["Equal in all bands (Wald chi2)", "Linear trend per 10 years"]:
        cells = []
        for o, s, _ in cols:
            if s != "slope":
                cells.append("")
                continue
            r = a_get(data="PSID", analysis="rank", sex="Sons", sample="unbalanced", band="test",
                      group="White - Black", outcome=o, stat=st)
            cells.append("" if r is None else (chi2cell(r["est"], r["p"], r["note"]) if "Wald" in st
                                               else coef(r["est"], r["se"], r["p"])))
        rows.append((TEST_LAB[st], cells))
    panels.append(("Tests on the White $-$ Black slope gap across bands 25--29 to 50--55", rows))
    table("tab_rank_age", "Rank mobility of sons by age at measurement (PSID)", "tab:rankage", heads, panels,
          "Child's band-mean family income (columns 1--3) or own earnings (column 4, zeros kept) ranked within birth "
          "year and band; parents' family income (mean at the child's ages 12--17) ranked within the child's birth "
          "year. Columns (2) and (3) evaluate the rank--rank line of column (1) at the 25th and 75th parental "
          "percentiles. All rank statistics weighted (core longitudinal weight at 16). Standard errors clustered by "
          "1968 family in parentheses. " + STARS + " " + SRC_A, first="Age band / group")


def tab_growth():
    cols = [("ln family income", "y0"), ("ln family income", "y1"), ("ln family income", "dy"),
            ("ln own earnings", "y0"), ("ln own earnings", "y1"), ("ln own earnings", "dy")]
    heads = ["ln family income|early band", "ln family income|late band", "Growth|(late $-$ early)",
             "ln own earnings|early band", "ln own earnings|late band", "Growth|(late $-$ early)"]
    panels = []
    for smp in ["25-29 -> 35-39", "25-29 -> 45-49", "30-34 -> 40-44"]:
        rows = []
        for g in GROUPS:
            rows.append((GLAB[g], [a_coef(data="PSID", analysis="growth", sex="Sons", sample=smp, group=g,
                                          outcome=o, stat=s) for o, s in cols]))
        rows.append(("Children (Black / White)", [kids(data="PSID", analysis="growth", sex="Sons", sample=smp,
                                                       outcome=o, stat=s) for o, s in cols]))
        e, l = smp.split(" -> ")
        panels.append((f"Early band {e.replace('-', '--')}, late band {l.replace('-', '--')}", rows))
    table("tab_growth", "Income growth by parental income: the same sons observed early and late (PSID)",
          "tab:growth", heads, panels,
          "One observation per son observed in both bands of the panel. Columns (1), (2), (4), (5): the band-mean "
          "outcome on log parental income; columns (3) and (6): the change in the band-mean outcome on log parental "
          "income (controls: quartic in the parent's age and the change in mean age). A positive growth coefficient "
          "means that sons of richer parents have steeper income growth between the two bands, which raises the IGE "
          "measured later in life \\citep{haider2006life}. Standard errors clustered by 1968 family. "
          + STARS + " " + SRC_A, first="Panel / group")


def tab_mechanism_tests():
    cols = [("marriage", "partnered"), ("marriage", "ln family income | partnered"), ("instability", "shock"),
            ("instability", "red"), ("instability", "zero"), ("instability", "ly_valid"),
            ("instability", "ly_clean"), ("instability", "lfam_clean")]
    heads = ["Partnered|(LPM)", "ln family income|controlling for|partnered", "Displaced or|unemployed|(LPM)",
             "Reduced|hours|(LPM)", "Zero|hours|(LPM)", "ln earnings,|all valid|years", "ln earnings,|clean|years",
             "ln family|income,|clean years"]
    panels = []
    for title, g in [("A. Pooled (weighted), all sons", "Pooled (weighted)"), ("B. White $-$ Black", "White - Black")]:
        rows = []
        for st in TEST_ROWS:
            cells = []
            for an, o in cols:
                r = a_get(data="PSID", analysis=an, sex="Sons", sample="unbalanced", band="test", group=g, outcome=o,
                          stat=st)
                sg = -1.0 if st == "Mean < 35 minus mean >= 35" else 1.0
                cells.append("" if r is None else (chi2cell(r["est"], r["p"], r["note"]) if "Wald" in st
                                                   else coef(sg * r["est"], r["se"], r["p"])))
            rows.append((TEST_LAB[st], cells))
        panels.append((title, rows))
    table("tab_mechanism_tests", "Marriage and instability across sons' ages: tests on the parental-income gradients (PSID)",
          "tab:mechtests", heads, panels,
          "Each column is a band-specific regression (bands 25--29 to 50--55, child-years, controls for a quartic in "
          "the parent's age and single-year age dummies) of the outcome in the header on log parental income; the "
          "rows summarise the band coefficients as in Table~\\ref{tab:agetests}. Partnered: spouse or partner in the "
          "son's family unit. Displaced: plant closure, layoff or firing in the year; reduced hours: below 1,500 while "
          "attached full time. Clean years exclude displaced, unemployed and (column 8) zero-hours years. Instability "
          "flags are for sons who are male heads. " + STARS + " " + SRC_A, first="Panel / statistic")


def tab_nlsy():
    cols = ["ln family income", "ln own earnings"]
    panels = []
    for b in BANDS:
        rows = [(GLAB[g], [a_coef(data="NLSY79", analysis="log IGE, child-year", sex="Sons", sample="unbalanced",
                                  band=b, group=g, outcome=o, stat="IGE") for o in cols]) for g in GROUPS]
        rows.append(("Children (Black / White)", [kids(data="NLSY79", analysis="log IGE, child-year", sex="Sons",
                                                       sample="unbalanced", band=b, outcome=o, stat="IGE")
                                                  for o in cols]))
        panels.append((f"Age {b.replace('-', '--')}", rows))
    panels.append(("Tests, White $-$ Black (bands 25--29 to 50--55)",
                   test_cells([dict(outcome=o) for o in cols], data="NLSY79", analysis="log IGE, child-year",
                              sex="Sons", sample="unbalanced", group="White - Black")))
    table("tab_nlsy_age", "Log IGE of sons by age at measurement (NLSY79, cohorts 1960--64)", "tab:nlsyage",
          ["ln family income", "ln own earnings"], panels,
          "Parents: mean family income in the 1978--80 income years, reported in the 1979--81 interviews (respondents "
          "living with a parent in 1979); "
          "child-years in the band; controls: quartic in the parent's age and single-year age dummies. Pooled = Black "
          "and non-Black non-Hispanic respondents weighted by the 1979 sampling weight. Standard errors clustered by "
          "1979 household. " + STARS + " " + SRC_A, first="Age band / group")


# ================================================================================================ 24.IGEDecomposition
S_CH = "Sons, Lee-Solon (age 40), father's childhood window"
S_WL = "Sons, Lee-Solon (age 40), father's working life 25-55"
S_LT = "Sons, lifetime mean, father's childhood window"
S_DA = "Daughters, Lee-Solon (age 40), father's childhood window"
S_35 = "Sons 35-55, Lee-Solon (age 40), father's childhood window"


def tab_price_quantity():
    st = ["ly on f_ly", "lw on f_lw", "lh on f_lh", "lw on f_ly", "lh on f_ly"]
    heads = ["ln earnings", "ln wage", "ln hours", "ln wage", "ln hours"]
    reg = {"Father's ln earnings": ["ly on f_ly", "lw on f_ly", "lh on f_ly"], "Father's ln wage": ["lw on f_lw"],
           "Father's ln hours": ["lh on f_lh"]}
    panels = []
    for smp, txt in [(S_CH, "Sons 25--55, IGE at age 40"), (S_35, "Sons 35--55, IGE at age 40"),
                     (S_LT, "Sons, lifetime mean")]:
        for race in ["Black", "White"]:
            rows = []
            for lab, which in reg.items():
                rows.append((lab, [d_coef(section="1 price-quantity", sample=smp, race=race, statistic=s)
                                   if s in which else "" for s in st]))
            r = d_get(section="1 price-quantity", sample=smp, race=race, statistic="ly on f_ly")
            rows.append(("Observations", [ints(r["n"]) if r is not None else ""] * len(st)))
            panels.append((f"{txt}: {race}", rows))
    table("tab_price_quantity", "Price versus quantity: the earnings IGE split into wage and hours (PSID, sons)",
          "tab:pricequantity", heads, panels,
          "One regression per column; the son's outcome is in the header and the father's measure in the row. "
          "Father's measures are means over his valid years when the son is 12--18. Columns (4) and (5) add up to "
          "column (1) exactly (same sample and controls), so they split the earnings IGE into the part carried by "
          "the son's hourly wage and the part carried by his annual hours. Lee--Solon panels: child-years at 25--55 "
          "(35--55 in the middle panels), quartics in the father's age at 16 and in the son's age minus 40 and their "
          "interactions with the father's measure (IGE at 40); observations are child-years. Lifetime-mean panels: "
          "one row per son, birth-year fixed effects. Father-present sons only (male head at 16). Unweighted. "
          "Standard errors clustered by 1968 family. " + STARS + " " + SRC_D, first="Panel / regressor")


def tab_wage_age():
    st = ["lfam_s on lyp", "lw on lyp", "lh on lyp", "ly on f_ly", "lw on f_lw", "lh on f_lh"]
    heads = ["ln family income|on ln parental|income", "ln wage|on ln parental|income",
             "ln hours|on ln parental|income", "ln earnings|on father's|ln earnings", "ln wage|on father's|ln wage",
             "ln hours|on father's|ln hours"]
    panels = []
    for smp in ["sons 25-34", "sons 35-44", "sons 45-55", "sons 25-55"]:
        rows, gap, nn = [], [], []
        b = [d_get(section="1b age profile", sample=smp, race="Black", statistic=s) for s in st]
        w = [d_get(section="1b age profile", sample=smp, race="White", statistic=s) for s in st]
        rows.append(("Black", [coef(r["estimate"], r["se"], r["p"]) for r in b]))
        rows.append(("White", [coef(r["estimate"], r["se"], r["p"]) for r in w]))
        for rb, rw in zip(b, w):
            g = rw["estimate"] - rb["estimate"]
            s = float(np.sqrt(rb["se"] ** 2 + rw["se"] ** 2))
            gap.append(coef(g, s, 2 * (1 - norm.cdf(abs(g / s)))))
            nn.append(f"{ints(rb['n'])} / {ints(rw['n'])}")
        rows.append(("White $-$ Black", gap))
        rows.append(("Child-years (Black / White)", nn))
        panels.append((f"Sons aged {smp.split()[1].replace('-', '--')}", rows))
    table("tab_wage_age", "Where the racial gap opens: wage and hours persistence by the son's age (PSID)",
          "tab:wageage", heads, panels,
          "One regression per cell: child-years of sons in the age band of the panel, outcome and regressor in the "
          "column header, Lee--Solon controls (quartics in the parent's age at 16 and the son's age) without the "
          "age interactions, so each coefficient is the average slope in the band. Columns (1)--(3): all sons, "
          "parental family income (mean at 13--19); columns (4)--(6): father-present sons, father's childhood-window "
          "means. White $-$ Black standard error = root sum of squared standard errors (disjoint clusters). "
          "Unweighted. Standard errors clustered by 1968 family. " + STARS + " " + SRC_D, first="Panel / group")


def tab_purging():
    st = ["earn", "earn_cs", "cleanA", "cleanB", "fpot", "pot", "fam_logs", "fam_clean"]
    heads = ["ln earnings|on father's|ln earnings", "same,|children with a|clean measure", "clean|years A",
             "clean|years B", "ln earnings|on father's|potential", "ln potential|on father's|potential",
             "ln family|income,|all years", "ln family|income,|clean years"]
    panels = []
    for smp, txt in [(S_CH, "A. Sons 25--55, IGE at age 40"), (S_35, "B. Sons 35--55, IGE at age 40")]:
        rows = []
        for race in ["Black", "White"]:
            rows.append((race, [d_coef(section="2 purging", sample=smp, race=race, statistic=s) for s in st]))
        rows.append(("White $-$ Black (bootstrap)", [d_coef(section="bootstrap", sample=smp, race="gap", statistic=s)
                                                      for s in st]))
        rows.append(("Change in the gap (bootstrap)",
                     [d_coef(section="bootstrap", sample=smp, race="dgap", statistic=s)
                      if s in ("cleanA", "cleanB", "fpot", "pot", "fam_clean") else "" for s in st]))
        nn = []
        for s in st:
            rb = d_get(section="2 purging", sample=smp, race="Black", statistic=s)
            rw = d_get(section="2 purging", sample=smp, race="White", statistic=s)
            nn.append(f"{ints(rb['n'])} / {ints(rw['n'])}" if rb is not None and rw is not None else "")
        rows.append(("Child-years (Black / White)", nn))
        panels.append((txt, rows))
    table("tab_purging", "Purging labor-market shocks does not move the racial gap (PSID, sons)", "tab:purging",
          heads, panels,
          "One regression per column (Lee--Solon design, father's childhood window). Clean years A: years without "
          "displacement or unemployment, in both generations (each person's measure is the mean over at least three "
          "clean valid years); clean years B: A and no reduced hours. Potential earnings: log hourly wage plus "
          "$\\ln 2{,}000$; column (6) is therefore the wage IGE. Change in the gap (positive = smaller gap): columns "
          "(3)--(4) relative to column (2) (same children), (5)--(6) relative to (1), (8) relative to (7). Gaps and "
          "changes: bootstrap standard errors over 200 draws of 1968 families within race. " + STARS + " " + SRC_D,
          first="Panel / row")


def tab_mediation():
    st = ["ly + none", "ly + educ", "ly + educ+s_sh_unemp+s_sh_disp+s_sh_red+s_sh_zero", "lw + none", "lw + educ",
          "lh + none", "lh + educ", "lh + educ+s_sh_unemp+s_sh_disp+s_sh_red+s_sh_zero"]
    heads = ["ln earnings"] * 3 + ["ln wage"] * 2 + ["ln hours"] * 3
    smp = "ln parental family income (13-19 mean)"
    panels = []
    for race in ["Black", "White"]:
        rr = [d_get(section="4a mediation", sample=smp, race=race, statistic=s) for s in st]
        rows = [("ln parental family income", [coef(r["estimate"], r["se"], r["p"]) for r in rr])]
        rows.append(("Son's years of education", ["No" if "none" in s else "Yes" for s in st]))
        rows.append(("Son's shares of unstable years", ["Yes" if "s_sh" in s else "No" for s in st]))
        share = []
        for s, r in zip(st, rr):
            base = rr[[x.split(" + ")[0] for x in st].index(s.split(" + ")[0])]
            share.append("" if "none" in s else f"{1 - r['estimate'] / base['estimate']:.2f}")
        rows.append(("Share of the IGE mediated", share))
        rows.append(("Child-years", [ints(r["n"]) for r in rr]))
        panels.append((f"{race} sons", rows))
    table("tab_mediation", "Education and instability as mediators of the IGE (PSID, sons)", "tab:mediation", heads,
          panels,
          "One regression per column; Lee--Solon design (IGE at 40), sons' child-years at 25--55 with a valid wage. "
          "Share mediated $= 1 - \\beta_{\\text{with controls}}/\\beta_{\\text{without}}$ relative to the first column "
          "of the same outcome. Unstable years: shares of the son's years with unemployment, displacement, reduced "
          "hours and zero hours. Education and instability are themselves outcomes of family background, so the "
          "shares are an accounting of coefficient movements, not causal mediation. Unweighted; standard errors "
          "clustered by 1968 family. " + STARS + " " + SRC_D, first="Panel / row")


def tab_instability():
    stats = [("sh_shock", "Share of years displaced or unemployed"), ("sh_disp", "Share of years displaced"),
             ("sh_unemp", "Share of years with unemployment"), ("sh_zero", "Share of years with zero hours"),
             ("vtr", "Variance of transitory ln earnings")]
    smps = ["fathers, childhood window", "fathers, working life", "sons 25-55"]
    heads = ["Fathers,|son aged 12--18", "Fathers,|aged 25--55", "Sons,|aged 25--55"]
    panels = []
    for s, lab in stats:
        rr = [d_get(section="3 instability means", sample=m, race="Black-White", statistic=s) for m in smps]
        rows = [("Black", [f"{r['black']:.3f}" for r in rr]), ("White", [f"{r['white']:.3f}" for r in rr]),
                ("White $-$ Black", [coef(r["estimate"], r["se"], r["p"]) for r in rr])]
        panels.append((lab, rows))
    table("tab_instability", "Labor-market instability of fathers and sons (PSID)", "tab:instability", heads, panels,
          "Means over the person's head-years in the window (one row per son, so a father with several sons appears once per son); "
          "father-present sons. White $-$ Black: coefficient on a Black indicator in a regression of the measure on "
          "a constant and the indicator, standard errors clustered by 1968 family. Transitory log earnings: residual "
          "after a person fixed effect, an age quartic and year fixed effects (male heads 25--60, by race). "
          + STARS + " " + SRC_D, first="Statistic / group")


def tab_decomposition():
    smps = [S_CH, S_WL, S_LT, S_35, S_DA]
    heads = ["Sons 25--55,|father's|childhood", "Sons 25--55,|father's|working life", "Sons,|lifetime|mean",
             "Sons 35--55,|father's|childhood", "Daughters 25--55,|father's|childhood"]
    comp = [("composition", "Composition (White re-weighted to Black)"),
            ("wage_trans", "Human capital (wage) transmission"),
            ("hours_all", "Hours / instability, total"),
            ("wage_share", r"\quad wage share of father's variance"),
            ("hours_trans", r"\quad hours transmission"),
            ("hours_share", r"\quad hours share of father's variance"),
            ("cross", "Wage--hours cross terms")]
    rows = [("Black earnings IGE", [d_coef(section="bootstrap", sample=s, race="B", statistic="beta") for s in smps]),
            ("White earnings IGE", [d_coef(section="bootstrap", sample=s, race="W", statistic="beta") for s in smps]),
            ("White $-$ Black gap", [d_coef(section="bootstrap", sample=s, race="gap", statistic="total")
                                     for s in smps])]
    panels = [("Earnings IGE on the father's earnings", rows),
              ("Decomposition of the gap", [(lab, [d_coef(section="bootstrap", sample=s, race="gap", statistic=c)
                                                    for s in smps]) for c, lab in comp])]
    table("tab_decomposition", "Accounting decomposition of the Black--White gap in the earnings IGE (PSID)",
          "tab:decomposition", heads, panels,
          "Each column is one decomposition. Exact identity: gap = composition + wage transmission + (wage share + "
          "hours transmission + hours share) + cross terms, where the White children are re-weighted to the Black "
          "distribution of the father's log earnings (20 quantile bins) and the shares are the shares of the "
          "partialled variance of the father's log earnings due to his log wage and log hours. Slopes over child-years "
          "without the age interactions (Lee--Solon columns) or one row per son (lifetime mean). Bootstrap standard "
          "errors over 200 draws of 1968 families within race. An accounting identity, not a causal decomposition: "
          "the hours rows mix shocks, labor supply and search frictions. " + STARS + " " + SRC_D,
          first="Row")


# ================================================================================================ 27.CareerWageGrowth
SRC_C = (r"Source: \texttt{IGE/27.CareerWageGrowth.py} (\texttt{output/career\_wage\_growth.csv}); table built by "
         r"\texttt{IGE/28.PaperBTables.py}.")
CGROUPS = ["Pooled (weighted)", "Black", "White", "Black - White"]
CGLAB = {"Pooled (weighted)": "Pooled (weighted)", "Black": "Black", "White": "White",
         "Black - White": "White $-$ Black", "Black + White": "Black and White"}
SCORE = ("Occupational wage score: mean log hourly wage of men aged 25--64 in the occupation relative to all men "
         "(CPS MORG, base 1992--2002), occupations harmonised to Dorn's occ1990dd scheme; log wage = score "
         "(between occupations) + residual (within occupation), so the score and residual columns add up to the "
         "log-wage column on the same sample. ")


def c_get(**kw):
    x = C
    for k, v in kw.items():
        x = x[x[k] == v]
    if len(x) == 0:
        MISSING.append(kw)
        return None
    return x.iloc[0]


def c_coef(dec=3, **kw):
    r = c_get(**kw)
    sg = -1.0 if _flip(kw) else 1.0
    return ("", "") if r is None else coef(sg * r["coef"], r["se"], r["p"], dec)


def tab_career_decomp():
    outs = ["lw", "os", "res", "share_between"]
    heads = ["ln wage", "Occupation|score", "Within-|occupation|residual", "Share|between|(2)/(1)"]
    panels = []
    for g in CGROUPS:
        rows = []
        for band in ["25-34", "35-44", "45-55", "35-55"]:
            cells = [c_coef(table="1 decomposition", sample=g, outcome=o, term=f"lyp, {band}") for o in outs]
            rows.append((f"Sons aged {band.replace('-', '--')}", cells))
        if g != "Black - White":
            r = [c_get(table="1 decomposition", sample=g, outcome="lw", term=f"lyp, {b}") for b in
                 ["25-34", "35-44", "45-55"]]
            rows.append(("Son-years (25--34 / 35--44 / 45--55)",
                         [" / ".join(ints(x["n"]) for x in r)] + [""] * (len(outs) - 1)))
        panels.append((CGLAB[g] + ": coefficient on log parental income", rows))
    rows = []
    for g in CGROUPS:
        for term in ["(35-55) - (25-34)", "(45-55) - (25-34)"]:
            rows.append((f"{CGLAB[g]}: {term.replace('-', '--').replace(') -- (', ') $-$ (')}",
                         [c_coef(table="1 decomposition change", sample=g, outcome=o, term=term) for o in outs]))
    panels.append(("Change in the coefficient across age bands (career divergence)", rows))
    table("tab_career_decomp", "Wage persistence by age: between and within occupations (PSID, sons)",
          "tab:careerdecomp", heads, panels,
          "One regression per cell: the son's outcome (column header) on log parental income (mean at 13--19), "
          "son-years in the age band, controls for quartics in the father's age at 16 and the son's age. " + SCORE +
          "With a time-varying score (the same relative premium in $t-1$ to $t+1$) the between share of the "
          "change of the racial gap is 0.27 (\\texttt{output/career\\_wage\\_growth.md}). Column (4) is left blank when the "
          "denominator is not different from zero. All cells are estimated as one stacked system, so differences "
          "across bands and groups have standard errors (clustered by 1968 family). Pooled: Black and White sons, "
          "weighted; Black and White: unweighted. Sons "
          "select into occupations, so the split is accounting, not causal. " + STARS + " " + SRC_C,
          first="Panel / row")


def tab_career_growth():
    outs = ["g_lw_t", "g_os_s", "g_res_s", "g_os_m", "g_res_m", "stay"]
    heads = ["Annual|ln wage|growth", "Score growth,|same|employer", "Residual growth,|same|employer",
             "Score growth,|new|employer", "Residual growth,|new|employer", "Stayed|with|employer"]
    panels = []
    for g in CGROUPS:
        rows = []
        for band in ["25-34", "35-55"]:
            rows.append((f"ln parental income, sons {band.replace('-', '--')}",
                         [c_coef(table="3 annual growth", sample=g, outcome=o, term=f"lyp, {band}") for o in outs]))
            r = c_get(table="3 annual growth", sample=g, outcome="g_lw_t", term=f"lyp, {band}")
            if g != "Black - White":
                rows.append((f"\\quad Mean of outcome / pairs, {band.replace('-', '--')}",
                             [num(c_get(table='3 annual growth', sample=g, outcome=o, term=f'lyp, {band}')['mean'])
                              for o in outs[:-1]] + [f"{ints(r['n'])} pairs"]))
        panels.append((CGLAB[g], rows))
    table("tab_career_growth", "Annual wage growth by parental income: within and across employers (PSID, sons)",
          "tab:careergrowth", heads, panels,
          "Consecutive interviews 1--2 years apart (waves 1985--2023) with a valid wage, a mapped occupation and "
          "tenure with the present employer. Annualised log-wage growth = score growth + residual growth, each split "
          "by whether the son stayed with the same employer; columns (2)--(5) add up to column (1). Column (6): share "
          "of stayers (linear probability). Controls: quartic in age and year fixed effects. Mean row: mean of the "
          "outcome in columns (1)--(5) and the number of son-year pairs. Coding noise in occupations inflates score "
          "changes in both directions. Standard errors clustered by 1968 family. " + SCORE + STARS + " " + SRC_C,
          first="Panel / row")


def tab_tenure():
    outs = ["lw", "os", "res"]
    lab = {"ten": "Tenure (per 10 years)", "ten2": "Tenure squared", "ten_lyp": "Tenure $\\times$ ln parental income"}
    panels = []
    for g in CGROUPS:
        terms = ["ten", "ten_lyp"] if g == "Black - White" else ["ten", "ten2", "ten_lyp"]
        rows = [(lab[t], [c_coef(table="7 tenure", sample=g, outcome=o, term=t) for o in outs]) for t in terms]
        if g != "Black - White":
            rows.append(("Son-years", [ints(c_get(table="7 tenure", sample=g, outcome=o, term="ten")["n"])
                                       for o in outs]))
        panels.append((CGLAB[g], rows))
    table("tab_tenure", "Wage--tenure profiles by parental income (PSID, sons, person fixed effects)", "tab:tenure",
          ["ln wage", "Occupation|score", "Within-|occupation|residual"], panels,
          "Within-son regressions (person fixed effects) of the outcome in the header on tenure with the present "
          "employer (per 10 years), its square and tenure interacted with centred log parental income, with a quartic "
          "in age and year fixed effects (waves 1984--2023). Within-son tenure slopes mix the return to seniority with "
          "the selection of good matches, so they are descriptive wage--tenure profiles. Standard errors clustered by "
          "1968 family. " + SCORE + STARS + " " + SRC_C, first="Panel / regressor")


def tab_promotion():
    outs = ["up", "sup_in", "g_os", "promo_rep", "pos_ch", "pos_up"]
    heads = ["Moved to a|higher-paying|occupation", "Entered a|supervisory or|managerial occ.",
             "Annual|change in|score", "Reported|promotion|(1976--87)", "Position change,|same employer|(1984--2001)",
             "Position change|with a|wage gain"]
    panels = []
    for g in CGROUPS:
        rows = []
        for band in ["25-34", "35-55"]:
            rows.append((f"ln parental income, sons {band.replace('-', '--')}",
                         [c_coef(table="4 promotion", sample=g, outcome=o, term=f"lyp, {band}") for o in outs]))
            if g != "Black - White":
                ms = []
                for o in outs:
                    r = c_get(table="4 promotion", sample=g, outcome=o, term=f"lyp, {band}")
                    ms.append("" if r is None or pd.isna(r["mean"]) else num(r["mean"]))
                rows.append((f"\\quad Mean of outcome, {band.replace('-', '--')}", ms))
        panels.append((CGLAB[g], rows))
    table("tab_promotion", "Promotion and occupational upgrading by parental income (PSID, sons)", "tab:promotion",
          heads, panels,
          "Son-year linear probability models (outcome in the header), male heads, controls: quartic in age and year "
          "fixed effects. Columns (1)--(3): change of the harmonised occupation between consecutive interviews; "
          "column (2) among sons not in a supervisory or managerial occupation at the previous interview. Column (4): "
          "the employed head whose job or position began within about a year reports that the previous one ended by "
          "promotion (waves 1976--1987, when most sons are under 40, hence no 35--55 estimate). Columns (5)--(6): the "
          "present position with the present employer began since the previous interview (self-reported, waves "
          "1984--2001). Coded occupation changes include coding noise. Standard errors clustered by 1968 family. "
          + STARS + " " + SRC_C, first="Panel / row")


def tab_hegde():
    outs = ["lw", "os", "res", "sup_in", "up", "pos_ch"]
    heads = ["ln wage", "Occupation|score", "Within-|occupation|residual", "Entered|supervisory or|managerial",
             "Moved to a|higher-paying|occupation", "Position change,|same|employer"]
    lab = {"lyp_c": "ln parental income (centred)", "lyp_old": "\\quad $\\times$ age 35--55", "black": "Black",
           "blk_old": "Black $\\times$ age 35--55", "lyp_blk": "ln parental income $\\times$ Black",
           "lyp_blk_old": "ln parental income $\\times$ Black $\\times$ age 35--55"}
    panels = []
    for t, title in [("6 Hegde test A", "A. Unconditional"),
                     ("6 Hegde test B", "B. Conditional on education and the wage and occupation score at 28--32")]:
        rows = [(lab[k], [c_coef(table=t, sample="Black + White", outcome=o, term=k) for o in outs]) for k in lab]
        rows.append(("Son-years", [ints(c_get(table=t, sample="Black + White", outcome=o, term="lyp_c")["n"])
                                   for o in outs]))
        panels.append((title, rows))
    table("tab_hegde", "Do Black sons from higher-income families progress less after 35? (PSID, sons)", "tab:hegde",
          heads, panels,
          "Black and White sons pooled (unweighted), son-years at 25--55; one regression per column with the full "
          "set of interactions of centred log parental income, a Black indicator and an indicator for ages 35--55; "
          "controls: quartic in age, year fixed effects. The triple interaction is the difference between Black and "
          "White sons in the after-35 change of the parental-income gradient. Standard errors clustered by 1968 "
          "family. " + SCORE + STARS + " " + SRC_C, first="Panel / regressor")


def tab_career_displacement():
    outs = ["d_lw", "d_os", "d_res", "upx", "down"]
    heads = ["Change in|ln wage", "Change in|occupation|score", "Change in|within-occupation|residual",
             "Moved up|$\\geq 0.10$", "Moved down|$\\geq 0.10$"]
    rows = []
    for g in CGROUPS:
        rows.append((f"Displaced in $t$: {CGLAB[g]}",
                     [c_coef(table="8 displacement a", sample=g, outcome=o, term="disp_t") for o in outs]))
    nn = [ints(c_get(table="8 displacement a", sample=g, outcome="d_lw", term="disp_t")["n"])
          for g in ["Pooled (weighted)", "Black", "White"]]
    rows.append(("Son-years (pooled / Black / White)", [" / ".join(nn)] + [""] * (len(outs) - 1)))
    table("tab_career_displacement", "Job loss, wages and occupational progression (PSID, sons)", "tab:careerdisp",
          heads, [("", rows)],
          "Son-years $t$ (male heads 25--52, 1970--2019) with a valid wage and occupation before ($t-2$ to $t-1$) and "
          "after ($t+2$ to $t+3$). Displaced: plant closure, layoff or firing dated $t$; non-displaced son-years with "
          "a displacement in $t-3$ to $t+3$ dropped. Outcome = after minus before. Controls: log parental income, "
          "quartic in age, year fixed effects. Standard errors clustered by 1968 family. " + SCORE + STARS + " "
          + SRC_C, first="Row")


def tab_nlsy_career():
    outs = ["lw", "os", "res"]
    panels = []
    for g in CGROUPS:
        rows = [(f"ln parental income, ages {b.replace('-', '--')}",
                 [c_coef(table="N1 NLSY79 decomposition", sample=g, outcome=o, term=f"lyp, {b}") for o in outs])
                for b in ["25-34", "35-44", "45-55"]]
        if g == "Black - White":
            x = C[(C.table == "N1 NLSY79 decomposition") & (C["sample"] == g) & (C.outcome == "lw")]
            extra = [t for t in x.term.unique() if not t.startswith("lyp")]
            for t in extra:
                tl = t.replace("gap change ", "").replace("-", "--").replace(")--(", ") $-$ (")
                rows.append((f"Change of the gap, {tl}",
                             [c_coef(table="N1 NLSY79 decomposition", sample=g, outcome=o, term=t) for o in outs]))
        panels.append((CGLAB[g], rows))
    table("tab_nlsy_career", "Wage persistence by age, between and within occupations (NLSY79, men)",
          "tab:nlsycareer", ["ln wage", "Occupation|score", "Within-|occupation|residual"], panels,
          "Men of the NLSY79 living with a parent in 1979; regressor: log mean parental family income 1979--81; "
          "outcome: hourly wage of the main (CPS) job at each interview and its occupation score; controls: quartic "
          "in age and birth-year fixed effects; standard errors clustered by 1979 household; pooled weighted by the "
          "1979 sampling weight. " + SCORE + STARS + " " + SRC_C, first="Panel / row")


# ------------------------------------------------------------------------------------------------ industry (32)
I = pd.read_csv(OUT / "industry_careers.csv")                    # 32.IndustryCareers.py
SRC_I = (r"Source: \texttt{IGE/32.IndustryCareers.py} (\texttt{output/industry\_careers.csv}); table built by "
         r"\texttt{IGE/28.PaperBTables.py}.")
IND = ("Industries harmonised to the ind1990ddx scheme (222 industries, 33 groups). Industry level $P_j$ and career "
       "slope $B_j$ from CPS MORG men aged 25--64, 1992--2002 (743,983 observations): relative log wage $= f(\\text{age}) "
       "+ P_j + B_j(\\text{age}-40)/10$, both employment-weighted mean zero. ")


def i_get(**kw):
    x = I
    for k, v in kw.items():
        x = x[x[k] == v]
    if len(x) == 0:
        MISSING.append(kw)
        return None
    return x.iloc[0]


def i_coef(dec=3, **kw):
    r = i_get(**kw)
    sg = -1.0 if _flip(kw) else 1.0
    return ("", "") if r is None else coef(sg * r["coef"], r["se"], r["p"], dec)


def tab_industry_decomp():
    outs = ["lw", "ip", "ic", "ir", "os_c", "jo", "jp", "jc", "jr"]
    heads = ["ln wage", "Industry|level $P$", "Industry|career slope|$B\\times t$", "Within-|industry|residual",
             "Occupation|score", "Joint:|occupation", "Joint:|industry level|net of occ.",
             "Joint:|industry slope|net of occ.", "Joint:|residual"]
    panels = []
    for g in CGROUPS:
        rows = [(f"Sons aged {b.replace('-', '--')}",
                 [i_coef(table="1 decomposition", sample=g, outcome=o, term=f"lyp, {b}") for o in outs])
                for b in ["25-34", "35-55"]]
        panels.append((CGLAB[g] + ": coefficient on log parental income", rows))
    rows = [(CGLAB[g], [i_coef(table="1 decomposition change", sample=g, outcome=o, term="(35-55) - (25-34)")
                        for o in outs]) for g in CGROUPS]
    panels.append(("Change in the coefficient, (35--55) $-$ (25--34)", rows))
    rows = [(lab, [("", "")] + [i_coef(table="1b shares of the change", sample=s, outcome=o, term="(35-55)-(25-34)")
                                for o in outs[1:]])
            for lab, s in [("Pooled change", "pooled share"), ("White $-$ Black change", "B-W share")]]
    panels.append(("Share of the change in column (1)", rows))
    table("tab_industry_decomp", "Wage persistence by age: industry level, industry career slope and within industry "
          "(PSID, sons)", "tab:industrydecomp", heads, panels,
          "One regression per cell: the son's outcome (column header) on log parental income, son-years in the age "
          "band, controls for quartics in the father's age at 16 and the son's age. " + IND +
          "Log wage $=P_j+B_j t+$ within-industry residual, so columns (2)--(4) add up to column (1); column (5) is "
          "the occupation score of Table~\\ref{tab:careerdecomp} on the same son-years; columns (6)--(9) split the "
          "log wage with occupation fixed effects and industry levels and slopes estimated jointly, so (7)$+$(8) is "
          "what industry adds beyond occupation. Same sample in every column: 1,822 Black sons (12,576 son-years) "
          "and 2,639 White sons (25,248). All cells are one stacked system (standard errors clustered by 1968 "
          "family); shares by the delta method. Pooled: weighted; Black and White: unweighted. Sign convention: "
          "White $-$ Black. Sons select into industries, so the split is accounting, not causal. " + STARS + " " +
          SRC_I, first="Panel / row")


def tab_industry_sorting():
    outs = ["ip", "ib", "fire", "legpro", "bussv", "steep", "highp"]
    heads = ["Industry|level $P$", "Industry|slope $B$", "Finance,|insurance,|real estate", "Legal,|professional|services",
             "Computer,|business|services", "Steep-slope|industry", "High-premium|industry"]
    panels = []
    for g in CGROUPS:
        rows = []
        for b in ["25-34", "35-55"]:
            rows.append((f"ln parental income, sons {b.replace('-', '--')}",
                         [i_coef(table="2 sorting", sample=g, outcome=o, term=f"lyp, {b}") for o in outs]))
            if g != "Black - White":
                rows.append((f"\\quad Mean of outcome, {b.replace('-', '--')}",
                             [num(i_get(table="2 sorting", sample=g, outcome=o, term=f"lyp, {b}")["mean"])
                              for o in outs]))
        rows.append(("Change, (35--55) $-$ (25--34)",
                     [i_coef(table="2 sorting change", sample=g, outcome=o, term="(35-55)-(25-34)") for o in outs]))
        panels.append((CGLAB[g], rows))
    table("tab_industry_sorting", "Sorting into industries by parental income (PSID, sons)", "tab:industrysorting",
          heads, panels,
          "Son-year regressions of the outcome in the header on log parental income with the controls of "
          "Table~\\ref{tab:industrydecomp}; columns (3)--(7) are linear probability models. " + IND +
          "Steep-slope and high-premium industries: top quartile of men's employment by $B_j$ and by $P_j$ "
          "(Table~\\ref{tab:industrygroups}). Standard errors clustered by 1968 family. Pooled: weighted; Black and "
          "White: unweighted. " + STARS + " " + SRC_I, first="Panel / row")


def tab_industry_growth():
    outs = ["g_stay base", "g_stay grpfe", "g_stay ddxfe", "g_flb base", "g_st base", "g_oth base"]
    heads = ["All|industries", "+ industry-|group FE", "+ fine-|industry FE", "Finance, legal,|professional,|business",
             "Other|steep-slope|industries", "All other|industries"]
    panels = []
    for g in CGROUPS:
        rows = []
        for b in ["25-34", "35-55"]:
            rows.append((f"ln parental income, sons {b.replace('-', '--')}",
                         [i_coef(table="3 same-employer growth", sample=g, outcome=o, term=f"lyp, {b}")
                          for o in outs]))
            if g != "Black - White":
                rs = [i_get(table="3 same-employer growth", sample=g, outcome=o, term=f"lyp, {b}") for o in outs]
                rows.append((f"\\quad Stayer pairs, {b.replace('-', '--')}",
                             [ints(r["n"]) if r is not None and not pd.isna(r["coef"]) else "" for r in rs]))
        panels.append((CGLAB[g], rows))
    table("tab_industry_growth", "Wage growth with the same employer by parental income, within industries "
          "(PSID, sons)", "tab:industrygrowth", heads, panels,
          "Outcome in every column: annualised log-wage growth between consecutive interviews 1--2 years apart "
          "(waves 1985--2023) for sons who stayed with their employer. Columns (2)--(3) add fixed effects for the "
          "industry of the later interview, so they compare sons in the same industry; columns (4)--(6) split the "
          "sample by the son's industry. Controls: quartic in age, year fixed effects. Cells with fewer than 250 "
          "pairs are left blank. Standard errors clustered by 1968 family. " + STARS + " " + SRC_I,
          first="Panel / row")


def tab_father_industry():
    pay = ["(1) ln wage, sons 25-34", "(2) ln wage, sons 35-55", "(3) annual ln wage growth, sons 30-55",
           "(4) annual ln wage growth with the same employer, sons 30-55"]
    heads = ["Son in|finance,|insurance,|real estate", "Son in|legal,|professional", "ln wage,|25--34",
             "ln wage,|35--55", "Annual|wage growth,|30--55", "Same-employer|wage growth,|30--55",
             "ln wage,|person FE"]
    panels = []
    for g in CGROUPS:
        r1 = [i_coef(table="4c son in X on father in X", sample=g, outcome=o, term="fa_x") for o in ["fire", "legpro"]]
        r2 = [i_coef(table="4d pay-off B", sample=g, outcome=o, term="f_ind") for o in pay]
        fe_main = i_coef(table="4e tenure x following", sample=g, outcome="lw", term="f_ind")
        fe_ten = i_coef(table="4e tenure x following", sample=g, outcome="lw", term="ten_f")
        rows = [("Father worked in the same industry set", r1 + [("", "")] * 5),
                ("Son in the father's industry group", [("", "")] * 2 + r2 + [fe_main]),
                ("Tenure (per 10 years) $\\times$ in father's industry", [("", "")] * 6 + [fe_ten])]
        panels.append((CGLAB[g], rows))
    table("tab_father_industry", "Following the father into his industry: how often and does it pay (PSID, sons)",
          "tab:fatherindustry", heads, panels,
          "Father: male head of the son's family at 16; his industry is the modal code over his years as head when "
          "the son was 12--18 (father-present sons: 52\\% of Black and 87\\% of White sons). The PSID has no employer "
          "identifiers, so following is measured at the industry level. Columns (1)--(2): son-years 25--55, linear "
          "probability that the son works in the industry set, on an indicator that the father did and log parental "
          "income. Columns (3)--(6): son-year regressions on an indicator that the son works in his father's industry "
          "group (33 groups), holding log parental income, years of education and the level $P_j$ and slope $B_j$ "
          "of the son's industry fixed; growth between consecutive interviews 1--2 years apart. Column (7): "
          "within-son regression on tenure, its square, tenure $\\times$ following, following and tenure $\\times$ "
          "log parental income, with a quartic in age and year fixed effects. Standard errors clustered by 1968 "
          "family. Pooled: weighted. Only 21 Black sons had a father in finance, insurance or real estate and 8 in "
          "legal or professional services. Sons who follow may differ in unobserved ways; descriptive. " + STARS +
          " " + SRC_I, first="Panel / row")


def tab_industry_groups():
    x = I[I.table == "0 MORG industry measures"]
    inds = x[x.outcome == "B"].sort_values("coef", ascending=False).term.tolist()
    cols = ["P", "B", "raw growth 25-34 -> 45-55", "return to experience 5 -> 25 years", "employment share"]
    rows = []
    for t in inds:
        cells = []
        for c in cols:
            r = x[(x.outcome == c) & (x.term == t)]
            cells.append(num(r.coef.iloc[0]) if len(r) else "")
        lab = t.replace("&", "\\&").replace("Mfg:", "Manufacturing:")
        rows.append((lab, cells))
    table("tab_industry_groups", "Industry wage levels and career slopes (CPS MORG men 25--64, 1992--2002)",
          "tab:industrygroups", ["Level $P$|at 40", "Career slope $B$|per 10 years", "Raw growth|25--34 to|45--55",
                                 "Return to|experience|5 to 25 years", "Employment|share"], [("", rows)],
          IND + "Rows sorted by $B$. Raw growth: mean relative log wage at 45--55 minus 25--34. Return to experience: "
          "predicted wage growth from 5 to 25 years of potential experience with years of schooling held fixed. "
          "Industry averages; the composition of workers is not held fixed. Across men, the standard deviation of "
          "$P$ is 0.232 and of $B$ 0.037. " + SRC_I, first="Industry group")


# ------------------------------------------------------------------------------------------------ family income vs earnings (34)
F = pd.read_csv(OUT / "income_vs_earnings_ige.csv")              # 34.IncomeVsEarningsIGE.py
SRC_F = (r"Source: \texttt{IGE/34.IncomeVsEarningsIGE.py} (\texttt{output/income\_vs\_earnings\_ige.csv}); table "
         r"built by \texttt{IGE/28.PaperBTables.py}.")
FGROUPS = ["Black", "White", "White - Black", "Pooled (weighted)"]


def f_coef(dec=3, **kw):
    x = F
    for k, v in kw.items():
        x = x[x[k] == v]
    if len(x) == 0:
        MISSING.append(kw)
        return ("", "")
    r = x.iloc[0]
    return coef(r["est"], r["se"], r["p"], dec)


def tab_income_earnings():
    heads = ["ln family|income", "ln own|earnings", "(1) $-$ (2)|(test)", "ln spouse's|earnings"]
    panels = []
    for sex, lab in [("Sons", "Sons"), ("Daughters", "Daughters")]:
        rows = []
        for g in FGROUPS:
            cells = [f_coef(data="PSID", part="1 grid log", sex=sex, measure="lyp", outcome=o, band="40", group=g,
                            stat=s) for o, s in [("lfam", "IGE"), ("learn", "IGE"), ("lfam - learn", "IGE diff"),
                                                 ("lsp", "IGE")]]
            rows.append((f"IGE at 40: {GLAB[g]}", cells))
        for g in FGROUPS:
            cells = [f_coef(data="PSID", part=pt, sex=sex, measure="lyp", outcome=o, band="test", group=g,
                            stat="change") for pt, o in [("2 age", "lfam"), ("2 age", "learn"),
                                                         ("2 age", "lfam - learn"), ("2 age couple", "lsp")]]
            rows.append((f"Change, bands $\\geq$35 $-$ $<$35: {GLAB[g]}", cells))
        panels.append((lab, rows))
    table("tab_income_earnings", "Family-income and earnings IGEs by race, sex and age (PSID)", "tab:incomeearnings",
          heads, panels,
          "One regression per cell: the child's outcome (column header) on log parental family income (mean at "
          "13--19). IGE at 40: age-interacted design of \\citet{lee2009trends} on child-years 25--65. Change: mean "
          "of the band coefficients at 35--55 minus the mean at 25--34, from the stacked band regressions. Own "
          "earnings: positive labor earnings; spouse's earnings: partnered years with positive spouse earnings. "
          "Column (3) tests (1) $-$ (2) on the same children. Standard errors clustered by 1968 family. Pooled: all "
          "races, weighted; Black and White: unweighted. " + STARS + " " + SRC_F, first="Panel / row")


def tab_income_channels():
    outs = [("lfam_cs", "IGE"), ("d_own", "IGE"), ("d_sp", "IGE"), ("d_oth", "IGE"),
            ("log spouse: marriage", "IGE"), ("log spouse: conditional", "IGE")]
    heads = ["ln family|income", "Own|earnings", "Spouse", "Other|income", "Spouse:|marriage",
             "Spouse:|earnings given|marriage"]
    panels = []
    for sex in ["Sons", "Daughters"]:
        rows = []
        for g in FGROUPS:
            rows.append((f"IGE at 40: {GLAB[g]}",
                         [f_coef(data="PSID", part="3 decomposition LS", sex=sex, outcome=o, band="40", group=g,
                                 stat=s) for o, s in outs]))
        for g in FGROUPS:
            rows.append((f"Change, bands $\\geq$35 $-$ $<$35: {GLAB[g]}",
                         [f_coef(data="PSID", part="3 decomposition", sex=sex, outcome=o, band="test", group=g,
                                 stat="change") for o, _ in outs]))
        panels.append((sex, rows))
    table("tab_income_channels", "Why family-income and earnings IGEs differ: own earnings, spouse and marriage "
          "(PSID)", "tab:incomechannels", heads, panels,
          "Common sample: child-years with family income, positive own earnings and known spouse earnings (zero if "
          "unpartnered). Exact log split: $\\ln Y=\\ln E_{own}+\\ln[(E_{own}+E_{sp})/E_{own}]+\\ln[Y/(E_{own}+E_{sp})]$, "
          "so columns (2)--(4) add up to column (1). Columns (5)--(6) split the spouse term (3) into the gradient of "
          "being partnered times the mean spouse term, and the gradient of the spouse term among the partnered "
          "times the partnership rate (remainder below 0.006). The split is sequential (own earnings first); an "
          "order-free level split gives the same picture (\\texttt{output/income\\_vs\\_earnings\\_ige.md}, "
          "Section 3d). IGE at 40 and change as in Table~\\ref{tab:incomeearnings}. Standard errors clustered by "
          "1968 family. " + STARS + " " + SRC_F, first="Panel / row")


# ------------------------------------------------------------------------------------------------ early job (35)
E = pd.read_csv(OUT / "early_industry_late_payoff.csv")          # 35.EarlyIndustryLatePayoff.py
SRC_E = (r"Source: \texttt{IGE/35.EarlyIndustryLatePayoff.py} (\texttt{output/early\_industry\_late\_payoff.csv}); "
         r"table built by \texttt{IGE/28.PaperBTables.py}.")


def e_coef(dec=3, **kw):
    x = E
    for k, v in kw.items():
        x = x[x[k] == v]
    if len(x) == 0:
        MISSING.append(kw)
        return ("", "")
    r = x.iloc[0]
    sg = -1.0 if _flip(kw) else 1.0
    return coef(sg * r["coef"], r["se"], r["p"], dec)


def tab_industry_nonlinear():
    cols = ["(1) pooled change (35-55)-(25-34)", "(2) share of the ln wage change",
            "(3) change of the B-W gap (35-55)-(25-34)", "(4) share"]
    heads = ["Pooled|change", "Share of|pooled rise", "Change of|White $-$ Black|gap", "Share of|gap change"]
    rows_a = [("32", "lwv", "Log wage (total)"), ("32", "k_lin_p", "Current industry: linear slope $B_j t$"),
              ("32", "k_q_p", "Current industry: age-band profile"),
              ("32", "k_s_p", "Current industry: piecewise profile (knots 30/35/45)")]
    rows_b = [("C", "lwv", "Log wage (total)"), ("C", "e_lin_p", "Industry at 25--34: linear slope"),
              ("C", "e_q_p", "Industry at 25--34: age-band profile"),
              ("C", "ck_p", "Current occupation $\\times$ industry cell: age-band profile"),
              ("C", "ko_p", "Current occupation group only: age-band profile"),
              ("C", "ck_ind", "\\quad What industry adds within the current cell"),
              ("C", "ce_p", "Cell at 25--34: age-band profile"),
              ("C", "eo_p", "Occupation group at 25--34 only: age-band profile"),
              ("C", "ce_ind", "\\quad What industry adds within the cell at 25--34")]
    panels = []
    for title, rows in [("A. Sample of Table~\\ref{tab:industrydecomp}", rows_a),
                        ("B. Sons with an industry and cell at 25--34", rows_b)]:
        out = []
        for s, t, lab in rows:
            cells = [e_coef(table="H headline PSID", sample=s, term=t, outcome=c) for c in cols]
            out.append((lab, cells))
        panels.append((title, out))
    table("tab_industry_nonlinear", "Industry and occupation $\\times$ industry career profiles: linear and "
          "nonlinear (PSID, sons)", "tab:industrynonlinear", heads, panels,
          "Each row is a piece of the son's log wage regressed on log parental income by age band (stacked, controls "
          "as in Table~\\ref{tab:industrydecomp}); columns (1) and (3) give the change of the coefficient from 25--34 "
          "to 35--55, pooled and for the White $-$ Black gap, and columns (2) and (4) its share of the change for the "
          "log wage. Linear: $B_j t$ as in Table~\\ref{tab:industrydecomp}. Age-band profile: the CPS MORG relative "
          "wage of the son's industry or cell in his five-year age band, around its age-weighted level (men 25--64, "
          "1992--2002). Cells: 11 occupation groups $\\times$ 33 industry groups (267 cells with at least 200 men; "
          "smaller cells take their occupation group's profile). `At 25--34': the son's modal industry or cell at "
          "25--34, evaluated at his current age. Standard errors clustered by 1968 family; shares by the delta "
          "method. Pooled: weighted. " + STARS + " " + SRC_E, first="Piece of the log wage")


def tab_early_job():
    cols = ["(1) accounted for at 25-34 (short - long)", "(2) accounted for at 35-55",
            "(3) change (35-55)-(25-34) of the part accounted for", "(5) share = (3)/(4)",
            "(6) B-W: change of the part accounted for", "(8) share = (6)/(7)"]
    heads = ["Accounted|for at|25--34", "Accounted|for at|35--55", "Change", "Share of|pooled rise",
             "Change,|White $-$ Black", "Share of|gap change"]
    terms = [("flp", "Finance, insurance, legal, professional (example; 2 groups)"),
             ("iset", "Industry groups ranked by pay and later growth (4 sets)"),
             ("grp", "Industry group (33)"),
             ("mp", "Manager or professional (2 groups)"),
             ("o11", "Occupation group (11)"),
             ("o11+grp", "Occupation group + industry group (11 + 33)"),
             ("cset", "Cells ranked by pay and later growth (4 sets)"),
             ("og", "Occupation $\\times$ industry cell (11 $\\times$ 33)"),
             ("occ", "Detailed occupation (occ1990dd)")]
    rows = [(lab, [e_coef(table="A2 Gelbach PSID", term=t, outcome=c) for c in cols]) for t, lab in terms]
    table("tab_early_job", "Where sons start: the job at 25--34 and the rise of wage persistence after 35 (PSID, "
          "sons)", "tab:earlyjob", heads, [("Fixed effects for the son's job at 25--34, by age band", rows)],
          "Short regression: the son's log wage on log parental income in each age band (25--34, 35--55), controls as "
          "in Table~\\ref{tab:industrydecomp}. Long regression: adds fixed effects for the son's job at 25--34 (row), "
          "estimated separately in each age band and race sample, so they absorb any wage profile of where he "
          "started, linear or not. Accounted for = short $-$ long. On this sample the pooled coefficient rises by "
          "0.132$^{***}$ and the White $-$ Black gap changes by 0.140$^{***}$ from 25--34 to 35--55. Ranked sets: "
          "cells (or industries) in the top quartile of men's employment by CPS wage level and by CPS wage growth "
          "after 35, and their intersection. Permuting the cell labels across sons gives shares of about 0.03. The "
          "son's early job also reflects his own skills, so the rows measure how much where a son stands at 25--34 "
          "predicts how far he pulls away, not a causal payoff. 93\\% of sons observed at 35--55 have a job at "
          "25--34. Standard errors clustered by 1968 family. " + STARS + " " + SRC_E, first="")


def tab_access():
    x = E[E.table == "D3 access LPM"]
    outs = sorted(x.outcome.unique(), key=lambda s: int(s.split(")")[0][1:]))
    outs = [o for o in outs if "AND" in o]                          # main text: well-paid AND high later growth
    heads = []
    for o in outs:
        spec = o.split(": ")[-1]
        heads.append(("Well-paid,|high later|growth" if "AND" in o else "Well-paid|(any)") + f"|{spec}")
    lab = {"lyp": "ln parental income", "white": "White", "bT2": "Black, middle tercile", "bT3": "Black, top tercile",
           "wT1": "White, bottom tercile", "wT2": "White, middle tercile", "wT3": "White, top tercile",
           "wT3 - bT3": "Rich White $-$ rich Black (top terciles)", "T2": "Middle tercile", "T3": "Top tercile",
           "fa_hh": "Father held a well-paid, high-later-growth job", "educ_c": "Years of education"}
    panels = []
    for s, title, terms in [("P", "Black and White sons (reference for terciles: Black, bottom tercile)",
                             ["lyp", "white", "bT2", "bT3", "wT1", "wT2", "wT3", "wT3 - bT3", "fa_hh", "educ_c"]),
                            ("B", "Black sons", ["lyp", "T2", "T3", "fa_hh", "educ_c"]),
                            ("W", "White sons", ["lyp", "T2", "T3", "fa_hh", "educ_c"]),
                            ("BW", "White $-$ Black", ["lyp", "T2", "T3", "fa_hh", "educ_c"])]:
        rows = []
        for t in terms:
            cells = [e_coef(table="D3 access LPM", sample=s, outcome=o, term=t) for o in outs]
            if any(c[0] for c in cells):
                rows.append((lab[t], cells))
        panels.append((title, rows))
    table("tab_access", "Access to well-paid, fast-growing starting jobs at 25--34 (PSID, sons)", "tab:access",
          heads, panels,
          "Son-level linear probability models. Outcome in columns (1)--(5): the son's job at 25--34 (modal "
          "occupation $\\times$ industry cell) is in the top quartile of men's employment by both CPS wage level and "
          "CPS wage growth after 35 (mean 0.156); the same specifications for well-paid jobs of any kind are in "
          "\\texttt{output/early\\_industry\\_late\\_payoff.md}, Section D3. Specifications "
          "(a) log parental income; (b) White; (c) both; (d) race $\\times$ parental-income tercile; (e) (c) plus the "
          "father's job and the son's years of education. Pooled: weighted; by race: unweighted. Standard errors "
          "clustered by 1968 family. " + STARS + " " + SRC_E, first="")


if __name__ == "__main__":
    tab_access()
    tab_industry_nonlinear()
    tab_early_job()
    tab_income_earnings()
    tab_income_channels()
    tab_industry_decomp()
    tab_industry_sorting()
    tab_industry_growth()
    tab_father_industry()
    tab_industry_groups()
    tab_career_decomp()
    tab_career_growth()
    tab_tenure()
    tab_promotion()
    tab_hegde()
    tab_career_displacement()
    tab_nlsy_career()
    tab_ige_age("Sons", "tab_ige_sons", "tab:ige_sons")
    tab_ige_age("Daughters", "tab_ige_daughters", "tab:ige_daughters")
    tab_age_tests()
    tab_rank_age()
    tab_growth()
    tab_mechanism_tests()
    tab_nlsy()
    tab_price_quantity()
    tab_wage_age()
    tab_purging()
    tab_mediation()
    tab_instability()
    tab_decomposition()
    if MISSING:
        print(f"{len(MISSING)} lookups found nothing; first ones:")
        for m in MISSING[:15]:
            print("  ", m)
