r"""LaTeX tables for the paper section on fathers' displacement (2026-10-17).

Reads output/father_displacement.csv (built by 19.FatherDisplacement.py) and writes to paperA_joint_loss/:
  tab_displacement_family.tex    stacked event study, mean of years +1..+3, by race and by age of the youngest child
  tab_displacement_children.tex  children's adult outcomes by age at the father's displacement, by race
  tab_displacement_mediation.tex total effect, effect given the mother's hours change / given family income after the
                                 displacement, and the shares mediated (bootstrap s.e.)
  tab_displacement_definitions.tex  main vs closures only vs quits vs zero hours (pooled, exposure at 0-17)
Cells: coefficient with stars (*** p<0.01, ** p<0.05, * p<0.1) and standard error in parentheses.
"""
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
RES = pd.read_csv(HERE / "output" / "father_displacement.csv")
PAPER = HERE / "paperA_joint_loss"


def star(p):
    return "^{***}" if p < 0.01 else "^{**}" if p < 0.05 else "^{*}" if p < 0.1 else ""


def cell(r, digits=3):
    if r is None or not np.isfinite(r["coef"]):
        return "", ""
    f = f"{{:,.{digits}f}}"
    return (f"${f.format(r['coef'])}{star(r['p'])}$", f"({f.format(r['se'])})")


def get(**kw):
    d = RES
    for k, v in kw.items():
        d = d[d[k].isna()] if v is None else d[d[k] == v]
    return d.iloc[0] if len(d) else None


def rows(label, cells):
    return [f"{label} & " + " & ".join(c[0] for c in cells) + r" \\",
            " & " + " & ".join(c[1] for c in cells) + r" \\"]


def hdr(i, name):
    """column header on two lines: (i) first half of the words / second half"""
    w = name.split()
    k = max(1, len(w) // 2)
    return (r"\begin{tabular}[b]{@{}c@{}}(" + str(i) + ") " + " ".join(w[:k]) + r"\\" + " ".join(w[k:])
            + r"\end{tabular}")


def table(caption, label, head, body, note, cols):
    return "\n".join([r"\begin{table}[htbp]\centering\small", rf"\caption{{{caption}}}\label{{{label}}}",
                      r"\resizebox{\textwidth}{!}{%", r"\begin{tabular}{l" + "c" * cols + "}", r"\toprule", head,
                      r"\midrule", *body, r"\bottomrule", r"\end{tabular}}",
                      r"\begin{minipage}{0.95\textwidth}\footnotesize " + note + r"\end{minipage}",
                      r"\end{table}", ""])


def family():
    outs = [("hh", "Father's hours", 0), ("hlab", "Father's labor income", 0), ("faminc", "Family income", 0),
            ("w_hrs", "Wife's hours", 0), ("w_emp", "Wife employed", 3), ("bw_present", "Still with wife", 3),
            ("afdc", "AFDC/TANF", 3), ("fs", "Food stamps", 3)]
    head = " & " + " & ".join(hdr(i + 1, o[1]) for i, o in enumerate(outs)) + r" \\"
    body = []
    panels = [("A. All fathers", "All", None), ("B. Black fathers", "Black", None), ("C. White fathers", "White", None),
              ("D. Youngest child aged 0--5", "All", "young05"), ("E. Youngest child aged 6--17", "All", "young617")]
    for title, smp, sub in panels:
        body.append(rf"\multicolumn{{{len(outs) + 1}}}{{l}}{{\textit{{{title}}}}} \\")
        cs = [cell(get(table="family_event_study", design="main", sample=smp, subsample=sub, outcome=o,
                       term="mean +1..+3"), d) for o, _, d in outs]
        body += rows("Displaced, years 1--3", cs)
        r0 = get(table="family_event_study", design="main", sample=smp, subsample=sub, outcome="hlab",
                 term="mean +1..+3")
        if r0 is not None and sub is None:
            body.append(rf"Displaced / control fathers & \multicolumn{{{len(outs)}}}{{l}}{{{int(r0['treated']):,} / "
                        rf"{int(r0['controls']):,}}} \\")
    note = (r"Stacked event study of a father's first displacement (plant closed or moved, laid off or fired, from the "
            r"PSID question on why the last job ended), with clean controls (fathers not displaced up to six years "
            r"after the event year). Coefficient: mean of the event-time effects at years $+1$ to $+3$, relative to "
            r"year $-2$. Fathers are male heads with a child aged 0--17 and positive hours at baseline; SRC and SEO "
            r"samples, Black and White, unweighted. Incomes in 2000 dollars; wife's outcomes for the wife present at "
            r"baseline. Standard errors clustered by 1968 family. *** $p<0.01$, ** $p<0.05$, * $p<0.1$. Source: "
            r"\texttt{IGE/19.FatherDisplacement.py}.")
    return table("The father's displacement and the family", "tab:displacement_family", head, body, note, len(outs))


def children():
    outs = [("log_earn", "Log lifetime earnings", 3), ("log_fam", "Log lifetime family income", 3),
            ("rank_fam", "Family income rank", 2), ("educ_self", "Years of schooling", 3)]
    head = " & " + " & ".join(hdr(i + 1, o[1]) for i, o in enumerate(outs)) + r" \\"
    body = []
    for title, smp in (("A. All children", "Pooled"), ("B. Black children", "Black"), ("C. White children", "White")):
        body.append(rf"\multicolumn{{{len(outs) + 1}}}{{l}}{{\textit{{{title}}}}} \\")
        for band in ("0-5", "6-11", "12-17"):
            cs = [cell(get(table=f"child_adult_ages {band}", sample=smp, outcome=o, term="treat"), d)
                  for o, _, d in outs]
            body += rows(f"Father displaced at {band.replace('-', '--')}", cs)
    note = (r"Each coefficient is from a separate regression of the outcome in the column on an indicator that the "
            r"child's father figure (the male head of the child's family) had his first displacement when the child "
            r"was in the age band of the row, against children whose father figure was not displaced; children first "
            r"exposed in another band are dropped. Controls: log parental income before the displacement, child sex, "
            r"Black (pooled panel) and birth-year fixed effects. Adult outcomes are means over ages 25--55 (ranks "
            r"within birth cohort). Associations, not causal effects. Standard errors clustered by 1968 family. "
            r"*** $p<0.01$, ** $p<0.05$, * $p<0.1$.")
    return table("The father's displacement and children's adult outcomes", "tab:displacement_children", head, body,
                 note, len(outs))


def mediation():
    outs = [("log_earn", "Log lifetime earnings", 3), ("log_fam", "Log lifetime family income", 3),
            ("rank_earn", "Earnings rank", 2), ("educ_self", "Years of schooling", 3)]
    terms = [("b_total", "Total association"), ("b_dmom", "Given the mother's change in hours"),
             ("b_lpost", "Given family income after the displacement"),
             ("share_dmom", "Share through the mother's hours"), ("share_lpost", "Share through family income")]
    head = " & " + " & ".join(hdr(i + 1, o[1]) for i, o in enumerate(outs)) + r" \\"
    body = []
    for title, smp in (("A. All children", "Pooled"), ("B. Black children", "Black"), ("C. White children", "White")):
        body.append(rf"\multicolumn{{{len(outs) + 1}}}{{l}}{{\textit{{{title}}}}} \\")
        for t, lab in terms:
            cs = [cell(get(table="mediation", sample=smp, outcome=o, term=t), 2 if t.startswith("share") else d)
                  for o, _, d in outs]
            body += rows(lab, cs)
    note = (r"Displacement at child ages 0--17. ``Given'' rows add the mediator to the regression of Table "
            r"\ref{tab:displacement_children}; shares are one minus the ratio of the conditional to the total "
            r"coefficient, with standard errors from 500 bootstrap draws of families. The mediators are outcomes of the "
            r"displacement and of family choices, so the decomposition is descriptive. *** $p<0.01$, ** $p<0.05$, "
            r"* $p<0.1$.")
    return table("What carries the association: the mother's hours or family income", "tab:displacement_mediation",
                 head, body, note, len(outs))


def definitions():
    outs = [("log_earn", "Log lifetime earnings", 3), ("log_fam", "Log lifetime family income", 3),
            ("educ_self", "Years of schooling", 3)]
    head = " & " + " & ".join(hdr(i + 1, o[1]) for i, o in enumerate(outs)) + r" \\"
    body = []
    for key, lab in (("main", "Closure or layoff (main)"), ("strict", "Closures only"), ("quit", "Quits (placebo)"),
                     ("zh", "Year without hours (earlier measure)")):
        cs = [cell(get(table=f"definitions_adult_{key}", sample="Pooled", outcome=o, term="treat"), d)
              for o, _, d in outs]
        body += rows(lab, cs)
    note = (r"Exposure at child ages 0--17, all children; controls as in Table \ref{tab:displacement_children}. "
            r"*** $p<0.01$, ** $p<0.05$, * $p<0.1$.")
    return table("Definitions of the father's job loss", "tab:displacement_definitions", head, body, note, len(outs))


def main():
    for name, f in (("family", family), ("children", children), ("mediation", mediation),
                    ("definitions", definitions)):
        (PAPER / f"tab_displacement_{name}.tex").write_text(f(), encoding="utf-8")
        print("wrote", f"tab_displacement_{name}.tex")


if __name__ == "__main__":
    main()
