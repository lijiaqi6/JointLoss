r"""Multiple testing for the layoff and sons-daughters results (simulated JPE round, Referee 1 point 5; editor)

Families, fixed before looking at the adjustment:
  A  THE LAYOFF COST (6): band change 45-49 - 25-29 (91 A6b); within-son slope (88); layoff minus closure change (91
     A6b); band change and within-son slope with one job-end net (103 b); the rank change (108).
  B  SONS vs DAUGHTERS (4): the daughters - sons difference in the wage change, the earnings change, the within-person
     wage slope and the within-person earnings slope (107 a).
  C  EVERY TEST REPORTED IN SECTION 6's DESIGN TABLES (A + B + timing, splits, bad times, industry shocks, cohorts,
     daughters' mechanism, career mechanism, UI interactions).
Holm (family-wise error) within A and B; Benjamini-Hochberg (false discovery rate) within C. p-values from the
estimate and its s.e. (normal approximation, as in the source scripts).
Writes output/multiple_testing.md / .json.
"""
import json
from pathlib import Path

import numpy as np
from scipy import stats

OUT = Path(__file__).resolve().parent / "output"


def J(n):
    return json.load(open(OUT / f"{n}.json", encoding="utf-8"))


def p_of(t):
    b, s = float(t[0]), float(t[1])
    return float(2 * stats.norm.sf(abs(b / s)))


def holm(p):
    p = np.asarray(p)
    o = np.argsort(p)
    m = len(p)
    adj = np.empty(m)
    run = 0.0
    for i, j in enumerate(o):
        run = max(run, min(1.0, (m - i) * p[j]))
        adj[j] = run
    return adj


def bh(p):
    p = np.asarray(p)
    o = np.argsort(p)[::-1]
    m = len(p)
    adj = np.empty(m)
    run = 1.0
    for k, j in enumerate(o):
        rank = m - k
        run = min(run, p[j] * m / rank)
        adj[j] = run
    return adj


def main():
    S, L, R3, X, Q = J("layoff_selection"), J("layoff_cost_by_age"), J("layoff_cohort_regime"), J("layoff_sex_difference"), \
        J("layoff_referee_checks")
    P, D, M, I, U, W = J("father_path_recession"), J("daughters_mechanism"), J("layoff_career_mechanism"), \
        J("layoff_industry_shocks"), J("simulated_replacement_rate"), J("ui_duration_weeks")
    A = [("layoff band change (91)", S["A6b|pooled"]["layoff"]),
         ("layoff within-son slope (88)", L["fe|f_sh_layoff_xa"][4]),
         ("layoff minus closure change (91)", S["A6b|pooled"]["diff"]),
         ("band change, one job-end net (103)", R3["(b) one net in every wave | all sons"]["change"]),
         ("within-son slope, one job-end net (103)", R3["(b) one net in every wave | all sons"]["fe"]),
         ("rank change (108)", Q["rank|f_sh_layoff"]["ch"])]
    B = [("daughters - sons, wage change", X["(a) as in 75|lw"]["difference"]),
         ("daughters - sons, earnings change", X["(a) as in 75|ly"]["difference"]),
         ("daughters - sons, wage within person", X["(a) as in 75|lw"]["difference_fe"]),
         ("daughters - sons, earnings within person", X["(a) as in 75|ly"]["difference_fe"])]
    k1 = "bad|bad times (sector decline or high state unemployment)|"
    C = A + B + [("timing: teen x age (A2)", S["A2|pooled"]["T"]), ("timing: 6-12 x age (A2)", S["A2|pooled"]["E"]),
                 ("small income loss x age", S["A3|income loss|lay_loss_small"]["fe"]),
                 ("short unemployment x age", S["A3|unemployment (hours >= 500)|lay_hu_short"]["fe"]),
                 ("repeated layoffs x age", S["A3|repeat|lay_multi"]["fe"]),
                 ("bad-times layoffs, change", P[k1 + "lay_bad"]["ch"]), ("other layoffs, change", P[k1 + "lay_good"]["ch"]),
                 ("father unemployed at son's 20-24", P["path|f_sh_layoff"]["fp_unemp"]),
                 ("father laid off again at son's 20-24", P["path|f_sh_layoff"]["fp_lay"]),
                 ("industry decline, reduced form within son", I["fe|decl"]["three"][0]),
                 ("born < 1963, within son (103 a)", R3["(a) as in 75 | born < 1963"]["fe"]),
                 ("born 1963-75, within son (103 a)", R3["(a) as in 75 | born 1963-75"]["fe"]),
                 ("born 1976+, within son (103 a)", R3["(a) as in 75 | born 1976+"]["fe"]),
                 ("daughters' partner's earnings, change", D["daughters|partner's ln earnings"]["change"]),
                 ("wage within occupation, change", M["wage within the occupation (within)"]["ch"]),
                 ("occupation score, change", M["occupation wage score (between)"]["ch"]),
                 ("UI replacement rate x layoff x age", U["fe|rr (1 s.d.), + layoff x father's ln wage x age"]["lay_rr_z_xa"]),
                 ("UI weeks x layoff x age", W["+ layoff x state unemployment rate x age"]["lay_wk_xa"])]
    md = ["# Multiple testing: the layoff and sons-daughters results", "",
          "Built by `110.MultipleTesting.py` (2026-10-20); families in its docstring. Holm = family-wise; BH = false "
          "discovery rate.", ""]
    RES = {}
    for name, fam, how in (("A. The layoff cost", A, "Holm"), ("B. Sons vs daughters", B, "Holm"),
                           ("C. Every Section 6 design test", C, "BH")):
        p = [p_of(t) for _, t in fam]
        adj = holm(p) if how == "Holm" else bh(p)
        md += [f"## {name} ({how}, {len(fam)} tests)", "", "| test | estimate | p | adjusted p |", "|---|---|---|---|"]
        for (lab, t), pp, aa in zip(fam, p, adj):
            md.append(f"| {lab} | {float(t[0]):.3f} ({float(t[1]):.3f}) | {pp:.4f} | {aa:.4f} |")
            RES[f"{name}|{lab}"] = {"p": pp, "adj": float(aa)}
        md.append("")
    (OUT / "multiple_testing.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "multiple_testing.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
