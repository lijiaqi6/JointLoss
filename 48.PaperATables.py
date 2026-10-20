r"""LaTeX tables for Paper A (joint job loss of spouses), 2026-10-17.

Reads only saved estimates (nothing is re-estimated here):
  output/cps_joint_loss_checks.csv   (37.CPSJointLossChecks.py)
and writes paperA_joint_loss/tab_cps_checks.tex.

Layout (PI's rules): one regression per column with the outcome in the header, samples as rows grouped in panels,
coefficient with stars and the standard error in parentheses below; *** p<0.01, ** p<0.05, * p<0.1. Multi-line headers
use nested tabulars. The table is shrunk to the text width when wider.

Run:  python IGE/48.PaperATables.py
"""
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
DEST = HERE / "paperA_joint_loss"
C = pd.read_csv(OUT / "cps_joint_loss_checks.csv")
STARS = r"$^{***}$ $p<0.01$, $^{**}$ $p<0.05$, $^{*}$ $p<0.1$."
MISSING = []


def stars(p):
    if p is None or pd.isna(p):
        return ""
    return "^{***}" if p < 0.01 else "^{**}" if p < 0.05 else "^{*}" if p < 0.1 else ""


def num(x, dec=3):
    s = f"{x:.{dec}f}"
    if float(s) == 0:
        s = s.lstrip("-")
    return s.replace("-", "$-$") if s.startswith("-") else s


def cell(table, sample, outcome):
    x = C[(C.table == table) & (C["sample"] == sample) & (C.outcome == outcome)]
    if outcome is None or len(x) == 0:
        if outcome is not None:
            MISSING.append((table, sample, outcome))
        return ("", "")
    r = x.iloc[0]
    return (f"${num(r['coef']).replace('$', '')}{stars(r['p_hh'])}$", f"({r['se_hh']:.3f})")


def base(table, sample, outcome):
    x = C[(C.table == table) & (C["sample"] == sample) & (C.outcome == outcome)]
    return f"{100 * x.iloc[0]['p0']:.2f}" if len(x) else ""


def head(text):
    return r"\begin{tabular}[b]{@{}c@{}}" + r"\\".join(text.split("|")) + r"\end{tabular}"


OUTS_FULL = ["wife job loser", "wife job loser, excl. 2020-21", "wife job loser not on layoff",
             "wife persistent job loser"]
OUTS_T1 = ["wife job loser t+1", "wife job loser t+1, excl. 2020-21", None, None]

PANELS = [
    ("A. Who reports (month of the husband's job loss)", "1_proxy", OUTS_T1, [
        ("(a) All couples", "All couples"),
        ("A (c) Wife self-reports, husband by proxy (t+1)", "Wife reports for herself, husband by proxy"),
        ("A (c'') ... and the wife is the household respondent (she reports his job loss)",
         "\\quad and the wife reports his job loss"),
        ("A (d) Husband self-reports, wife by proxy (t+1)", "Husband reports for himself, wife by proxy"),
        ("A (d'') ... and the husband is the household respondent (he reports her job loss)",
         "\\quad and the husband reports her job loss"),
        ("B (c) Wife self, husband proxy at t and t+1", "Wife self, husband proxy in both months"),
        ("B (d) Husband self, wife proxy at t and t+1", "Husband self, wife proxy in both months"),
        ("A (e) Both by proxy (another member reports both, t+1)", "A third member reports both"),
        ("A (f) One spouse reports both ((c) or (d); third-person reports excluded)",
         "Third-member reports excluded")]),
    ("B. Temporary layoffs and the season", "2_layoff_season", OUTS_FULL, [
        ("(0) All", "All husband job losses"),
        ("(i) His job loss other than on layoff (PRUNTYPE 2-3)", "His loss not a temporary layoff"),
        ("(i') His job loss on layoff (PRUNTYPE 1) only", "His loss a temporary layoff"),
        ("(ii) Job-loss month (t+1) not June-September", "Not June--September"),
        ("(i)+(ii) Not on layoff, not June-September", "Not a temporary layoff, not June--September")]),
    ("C. Persistent job losses (both observed two months later)", "2_persistent", OUTS_FULL, [
        ("(0) All, t+2-linked sample", "All husband job losses"),
        ("(iv) His job loss persistent", "His loss persistent"),
        ("(iv)+(i) Persistent and not on layoff", "Persistent, not a temporary layoff"),
        ("(iv)+(i)+(ii) Persistent, not on layoff, not June-September",
         "Persistent, not a temporary layoff, not June--September")]),
    ("D. Class of worker", "2_class_of_worker", OUTS_FULL, [
        ("Husband private, wife private", "Both private"),
        ("Both private, his job loss other than on layoff", "Both private, his loss not a temporary layoff"),
        ("Husband government, wife government", "Both government"),
        ("Husband self-employed, wife self-employed", "Both self-employed"),
        ("Husband private, wife government", "Husband private, wife government"),
        ("Husband government, wife private", "Husband government, wife private")]),
    ("E. Shared workplace", "3_proxy_match", OUTS_T1, [
        ("Same major industry", "Same major industry"),
        ("Same detailed industry", "Same detailed industry"),
        ("Same detailed industry x same detailed occupation", "Same detailed industry and occupation"),
        ("Same detailed industry x detailed occupation x class of worker",
         "Same detailed industry, occupation and class"),
        ("Not same detailed industry x occupation x class", "All other couples")]),
    ("F. Attrition", "4_selection", OUTS_T1, [
        ("Observed in all four months", "Couples observed in all four months"),
        ("Not observed in all four months", "Couples not observed in all four months")]),
]


def tab_cps_checks():
    heads = ["Wife loses|her job", "Wife loses her job,|excluding 2020--21", "Wife's loss not a|temporary layoff",
             "Wife still|unemployed at $t+2$", "Base rate,|\\% a month"]
    k = len(heads)
    L = [r"\begin{table}[!htbp]", r"\centering",
         r"\caption{Robustness of the same-month joint job loss (CPS basic monthly, 1994--2023)}",
         r"\label{tab:cps_checks}",
         r"\resizebox{\ifdim\width>\textwidth\textwidth\else\width\fi}{!}{%",
         r"\resizebox*{!}{\ifdim\totalheight>0.78\textheight 0.78\textheight\else\totalheight\fi}{%",
         r"\begin{tabular}{l" + "c" * k + "}", r"\toprule",
         "Sample & " + " & ".join(head(h) for h in heads) + r" \\",
         " & " + " & ".join(f"({i + 1})" for i in range(k)) + r" \\", r"\midrule"]
    for j, (title, table, outs, rows) in enumerate(PANELS):
        if j:
            L.append(r"\addlinespace")
        L.append(r"\multicolumn{" + str(k + 1) + r"}{l}{\textit{" + title + r"}} \\")
        for sample, lab in rows:
            cells = [cell(table, sample, o) for o in outs]
            b = base(table, sample, outs[0])
            L.append(lab + " & " + " & ".join(c[0] for c in cells) + f" & {b}" + r" \\")
            L.append(" & " + " & ".join(c[1] for c in cells) + r" & \\")
    L += [r"\bottomrule", r"\end{tabular}}}", r"\par\smallskip",
          r"\begin{minipage}{\textwidth}\footnotesize \textit{Notes:} Each cell is the coefficient on the husband "
          r"losing his job in a linear probability model of the outcome in the column header, among married couples "
          r"in which both spouses work in the previous month, with state $\times$ month fixed effects; standard errors "
          r"clustered by household (state clustering gives the same significance). Column (5): the wife's job-loss "
          r"rate when the husband does not lose his job. A job loser is unemployed after a layoff, a job loss or the "
          r"end of a temporary job, having been employed the month before. Persistent: still unemployed two months "
          r"later. Panel A: labor force information collected from the person (self) or from another household "
          r"member (proxy); couples in which both spouses report for themselves cannot be formed because the CPS "
          r"takes one respondent per household and month. " + STARS + r" Source: \texttt{IGE/37.CPSJointLossChecks.py} "
          r"(\texttt{output/cps\_joint\_loss\_checks.csv}); table built by \texttt{IGE/48.PaperATables.py}."
          r"\end{minipage}", r"\end{table}"]
    (DEST / "tab_cps_checks.tex").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("wrote tab_cps_checks.tex")


# ------------------------------------------------------------------------------------------------ BPS reconciliation
B = pd.read_csv(HERE / "bps_reconciliation" / "bps_reconciliation.csv")
SRC_B = (r"Source: \texttt{IGE/bps\_reconciliation/} (\texttt{bps\_reconciliation.csv}); table built by "
         r"\texttt{IGE/48.PaperATables.py}.")


def bcell(table, spec, param, dec=3, se=True):
    x = B[(B.table == table) & (B.spec == spec) & (B.parameter == param)]
    if len(x) == 0:
        MISSING.append((table, spec, param))
        return ("", "")
    r = x.iloc[0]
    top = f"${num(r['value'], dec).replace('$', '')}{stars(r['p'])}$"
    bot = f"({r['se']:.{dec}f})" if se and not pd.isna(r["se"]) else ""
    return (top, bot)


def ltable(name, caption, label, heads, panels, notes, first=""):
    k = len(heads)
    L = [r"\begin{table}[!htbp]", r"\centering", r"\caption{" + caption + "}", r"\label{" + label + "}",
         r"\resizebox{\ifdim\width>\textwidth\textwidth\else\width\fi}{!}{%",
         r"\begin{tabular}{l" + "c" * k + "}", r"\toprule",
         first + " & " + " & ".join(head(h) for h in heads) + r" \\",
         " & " + " & ".join(f"({i + 1})" for i in range(k)) + r" \\", r"\midrule"]
    for j, (title, rows) in enumerate(panels):
        if title:
            if j:
                L.append(r"\addlinespace")
            L.append(r"\multicolumn{" + str(k + 1) + r"}{l}{\textit{" + title + r"}} \\")
        for lab, cells in rows:
            if any(isinstance(c, tuple) for c in cells):
                L.append(lab + " & " + " & ".join(c[0] if isinstance(c, tuple) else c for c in cells) + r" \\")
                bots = [c[1] if isinstance(c, tuple) else "" for c in cells]
                if any(bots):
                    L.append(" & " + " & ".join(bots) + r" \\")
            else:
                L.append(lab + " & " + " & ".join(cells) + r" \\")
    L += [r"\bottomrule", r"\end{tabular}}", r"\par\smallskip",
          r"\begin{minipage}{\textwidth}\footnotesize \textit{Notes:} " + notes + r"\end{minipage}", r"\end{table}"]
    (DEST / f"{name}.tex").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {name}.tex")


def tab_bps_relax():
    specs = [("base", "Baseline|(their|sample)"), ("a_nowork", "Drop only|the year|without work"),
             ("b_nostatus", "No|status|controls"), ("c1_nojump", "No jump|trim"), ("c2_nominw", "No|minimum-|wage trim"),
             ("d_seo", "Low-income|sample in"), ("d_seo_w", "Low-income|sample in,|weighted"),
             ("d_white", "White|couples|(low-income in)")]
    rows = [("r_u1u2", "Cov., transitory wage shocks"), ("r_v1v2", "Cov., permanent wage shocks"),
            ("pi", "$E(\\pi)$, partial insurance"), ("eta_c_p", "$\\eta_{c,p}$"), ("eta_h1_w1", "$\\eta_{h_1,w_1}$"),
            ("eta_h2_w2", "$\\eta_{h_2,w_2}$"), ("ch_m_h2v1", "Wife's hours / husband's permanent wage"),
            ("ch_m_cv1", "Consumption / husband's permanent wage"), ("ch_gov", "Share of insurance: government"),
            ("ch_fam", "Share of insurance: family labor supply"), ("ch_sav", "Share of insurance: savings"),
            ("beta", "Outside insurance $\\beta$")]
    body = [(lab, [bcell("S1", s, p) for s, _ in specs]) for p, lab in rows]
    corr = []
    for p, lab in [("corr_u", "\\quad correlation, transitory"), ("corr_v", "\\quad correlation, permanent")]:
        corr.append((lab, [bcell("S1", s, p, dec=2, se=False)[0] for s, _ in specs]))
    nobs = [("Observations", [f"{int(v):,}" if not pd.isna(v) else "" for v in
                              [B[(B.table == 'S1') & (B.spec == s) & (B.parameter == 'observations')]['value'].iloc[0]
                               if len(B[(B.table == 'S1') & (B.spec == s) & (B.parameter == 'observations')]) else float('nan')
                               for s, _ in specs]])]
    panels = [("Wage process", body[:2] + corr), ("Preferences and elasticities", body[2:8]),
              ("Insurance against a permanent fall in the husband's wage", body[8:]), ("", nobs)]
    ltable("tab_bps_relax", "Blundell, Pistaferri and Saporta-Eksten (2016) under their restrictions and without them",
           "tab:bps_relax", [h for _, h in specs], panels,
           "Their code run on their constructed PSID panel, 1999--2009. Column (1) reproduces their Tables 3--5 and "
           "their insurance accounting. Each further column relaxes one restriction: (2) drops only the year in which "
           "the husband has no hours or earnings instead of his whole record; (3) removes both spouses' employment-status "
           "controls from the residual regressions; (4) removes the trim of years of collapse and recovery; (5) removes the "
           "trim of wages below half the state minimum wage; (6)--(7) include the PSID's low-income sample; (8) White "
           "couples with the low-income sample. Wage process: GMM standard errors clustered by household; preferences, "
           "elasticities and insurance: block bootstrap over households (50 replications). " + STARS + " " + SRC_B,
           first="Parameter")


def tab_bps_event():
    specs = [("base", "Their|sample"), ("d_seo", "Low-income|sample in"), ("f_all", "All|relaxations")]
    def ev(fam, key):
        return [bcell("S2_event", s, f"{fam}|{key}") for s, _ in specs]
    def nev(fam, key):
        out = []
        for s, _ in specs:
            x = B[(B.table == "S2_event") & (B.spec == s) & (B.parameter == f"{fam}|{key}")]
            n = x["note"].iloc[0].split("events=")[-1] if len(x) else ""
            out.append(str(int(float(n))) if n not in ("", "nan") else "")
        return out
    panels = [
        ("Consumption residual, interval of the displacement", [
            ("Husband displaced alone", ev("uc", "ho")), ("Both displaced", ev("uc", "jt")),
            ("Both $-$ husband alone", ev("uc", "jt-ho")), ("\\quad joint events", nev("uc", "jt"))]),
        ("Consumption residual, next interval", [
            ("Husband displaced alone", ev("uc", "ho_p")), ("Both displaced", ev("uc", "jt_p")),
            ("Both $-$ husband alone", ev("uc", "jt_p-ho_p")), ("\\quad joint events", nev("uc", "jt_p"))]),
        ("Husband's earnings residual, interval of the displacement", [
            ("Husband displaced alone", ev("uy", "ho")), ("Both displaced", ev("uy", "jt"))]),
        ("Wife's earnings, arc change, interval of the displacement", [
            ("Both $-$ husband alone", ev("arc_yw", "jt-ho"))]),
    ]
    ltable("tab_bps_event", "Single and joint displacements in the panel of Blundell, Pistaferri and Saporta-Eksten (2016)",
           "tab:bps_event", [h for _, h in specs], panels,
           "Biennial event study on their residuals (consumption and earnings growth net of their observables), PSID "
           "1999--2009, with the PSID reason-for-job-end flags of Section~\\ref{sec:data}: husband displaced alone, both "
           "spouses displaced, relative to couples without a displacement. Interval of the displacement: the two-year "
           "change that contains the job-end year; next interval: the following two-year change. Wife's earnings: arc "
           "change including zeros. Column (3) applies all relaxations of Table~\\ref{tab:bps_relax} that leave the "
           "estimator defined. Standard errors clustered by household. Associations, with few joint events. " + STARS +
           " " + SRC_B, first="")


def tab_bps_attrition():
    x = B[B.table == "S2_attrition"]
    labels = {0: "Married couples, husband 30--57, SRC and low-income samples",
              1: "Drop the year of a change in family composition", 2: "Drop if not married", 3: "Drop if state missing",
              4: "Drop female heads, age always missing", 5: "Drop net worth of \\$20 million or more",
              6: "Keep ages 30--57", 7: "Drop the low-income (SEO) sample", 8: "Drop if education missing",
              9: "Merge minimum wages and prices", 10: "Drop husbands with any year without work (estimation file)",
              11: "Keep rows with a husband's wage-growth moment", 12: "Keep rows with both spouses' wage-growth moments"}
    rows = []
    for k in sorted(labels):
        def g(v):
            y = x[x.parameter == f"step{k}|{v}"]
            return f"{int(y['value'].iloc[0]):,}" if len(y) else ""
        rows.append((labels[k], [g("rows"), g("hd"), g("wd"), g("jd")]))
    ltable("tab_bps_attrition", "Where the displaced couples leave the sample of Blundell, Pistaferri and Saporta-Eksten (2016)",
           "tab:bps_attrition", ["Couple-|years", "Husband|displaced", "Wife|displaced", "Both|displaced"],
           [("", rows)],
           "Universe: married couples with husbands aged 30--57 in the PSID's SRC and low-income samples, waves 1999--2009. "
           "Their restrictions applied in their order; each row counts the couple-years left after the step. The last rows "
           "keep couple-years with a husband's wage-growth moment and with both spouses' wage-growth moments. " + SRC_B,
           first="Step")


if __name__ == "__main__":
    tab_bps_relax()
    tab_bps_event()
    tab_bps_attrition()
    tab_cps_checks()
    if MISSING:
        print(f"{len(MISSING)} lookups found nothing:", MISSING[:10])
