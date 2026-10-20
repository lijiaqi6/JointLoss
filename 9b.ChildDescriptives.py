r"""Children's exposures (9.ChildExposure.py), CDS test scores (9a.CDS.py) and adult earnings (1.PSID.py):
descriptives by race and descriptive OLS (2026-10-17). Writes output/psid_child_exposure.md.

All estimates are associations, not causal effects: the exposures (mother's work after a birth, the father figure's
job loss, separation, welfare) are chosen by or happen to families that differ in many unmeasured ways.
Regressions: unweighted OLS, s.e. clustered by 1968 family (fam68); birth-year fixed effects (and CDS-wave fixed
effects for test scores, whose WJ edition changes across waves).
"""
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tools.sm_exceptions import SingularMatrixWarning

# CDS: children born 2001+ appear only in the 2014/2019 waves, so one wave dummy is collinear with the birth-year
# dummies (statsmodels uses the pseudo-inverse; the exposure coefficients are unaffected)
warnings.simplefilter("ignore", SingularMatrixWarning)

from common import DATA, OUT, fmt

X = ["mom_emp1", "fjl", "sep", "welf05"]
LAB = {"mom_emp1": "Mother employed in year +1 (hours > 0)",
       "fjl": "Father figure's job loss (0-17; CDS: before the test)",
       "sep": "Parents' separation / divorce (0-17; CDS: before the test)",
       "welf05": "Years with AFDC/TANF or food stamps at 0-5",
       "lpinc_av": "Log parental income, mean at 12-17",
       "lfinc05": "Log family income, mean at 0-5",
       "female": "Female"}


def reg(d, y, ctrl, fe):
    cols = [y, *X, *ctrl, *fe, "fam68"]
    d = d.reset_index()[["pid", *cols]].replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)
    Z = d[X + ctrl].astype(float)
    for f in fe:
        Z = Z.join(pd.get_dummies(d[f].astype(int), prefix=f, drop_first=True, dtype=float))
    Z = sm.add_constant(Z, has_constant="add")
    r = sm.OLS(d[y].astype(float), Z).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d["fam68"])[0]})
    return r, d


def table(specs, rows):
    """specs: list of (header, result). One column per regression, regressors as rows, N at the bottom."""
    hdr = "| | " + " | ".join(h for h, _ in specs) + " |"
    out = [hdr, "|" + "---|" * (len(specs) + 1)]
    for v in rows:
        cells = []
        for _, (r, _) in specs:
            cells.append(fmt(r.params[v], r.bse[v], r.pvalues[v]) if v in r.params else "")
        out.append(f"| {LAB.get(v, v)} | " + " | ".join(cells) + " |")
    for lab, key in (("Mean of outcome", "mean"), ("N", "n"), ("Children", "kids"), ("Clusters (fam68)", "cl")):
        cells = []
        for _, (r, d) in specs:
            y = r.model.endog_names
            cells.append({"mean": f"{d[y].mean():.3f}", "n": f"{int(r.nobs):,}", "kids": f"{d['pid'].nunique():,}",
                          "cl": f"{d['fam68'].nunique():,}"}[key])
        out.append(f"| {lab} | " + " | ".join(cells) + " |")
    return "\n".join(out)


def main():
    kx = pd.read_pickle(DATA / "psid_child_exposure.pkl")
    cds = pd.read_pickle(DATA / "cds_scores.pkl")
    kids = pd.read_pickle(DATA / "psid_kids.pkl")
    kx = kx[kx["race"].isin(["White", "Black"])].copy()

    # ---- adult sample
    a = kx.merge(kids[["pid", "lpinc_av", "log_earn", "n_earn"]], on="pid", how="inner")
    a["fjl"], a["sep"] = a["fjl0"], a["div"]
    a = a.set_index("pid")

    # ---- CDS sample: ages 5-12; job loss and separation before the test year
    c = cds[cds["age"].between(5, 12)].merge(kx, on="pid", how="inner", suffixes=("", "_k"))
    c["fjl"] = (c["fjl0_age1"] < c["age"]).astype(float)
    c["sep"] = (c["div_age1"] < c["age"]).astype(float)
    c = c.set_index("pid")

    md = ["# PSID children: mother's work at the birth, father's job loss, separation, welfare - descriptives",
          "",
          "Built by `9.ChildExposure.py` (exposures), `9a.CDS.py` (CDS scores), `9b.ChildDescriptives.py` (this file), "
          "2026-10-17. **All numbers below are associations, not causal effects.** Unweighted; race = head's race in "
          "the first family unit the child is seen in.", ""]

    # ---- descriptives
    dcols = [("mom_emp0", "Mother employed, birth year"), ("mom_emp1", "Mother employed, year +1"),
             ("mom_emp2", "Mother employed, year +2"), ("mom_hrs1", "Mother's hours, year +1"),
             ("fjl0", "Father figure's job loss 0-17 (zero hours)"),
             ("fjl_u", "Father figure's job loss 0-17 (zero hours or unemployment; unemp. to 1992 only)"),
             ("ff_years", "Years with a male head observed (0-17)"),
             ("div_mh", "Separation/divorce 0-17, marriage history"), ("div_rel", "Separation 0-17, relation change"),
             ("div", "Separation/divorce 0-17, either"), ("welf05", "Years with AFDC/TANF or food stamps, 0-5"),
             ("afdc05", "Years with AFDC/TANF, 0-5"), ("fs05", "Years with food stamps, 0-5"),
             ("welf05_obs", "Years observed for welfare, 0-5"), ("finc05", "Family income 0-5 (2000$)"),
             ("finc617", "Family income 6-17 (2000$)"), ("mom_educ", "Mother's years of education"),
             ("mom_married_birth", "Mother married at the birth"), ("mom_age_birth", "Mother's age at the birth")]
    md += ["## 1. Descriptives by race", "",
           "Children born 1968-2020 (all), the adult-earnings sample (also in `psid_kids.pkl` with log lifetime "
           "earnings: head's child at 12-17, 3+ years as head/wife at 25-55) and the CDS sample (child x wave "
           "assessments at 5-12). Cells: mean (N non-missing).", ""]
    samples = [("All", kx), ("Adult earnings", a[a.log_earn.notna()]), ("CDS 5-12", c)]
    hdr = "| | " + " | ".join(f"{s} {r}" for s, _ in samples for r in ("White", "Black")) + " |"
    md += [hdr, "|" + "---|" * 7]
    md.append("| Children | " + " | ".join(f"{d[d.race == r].index.nunique() if s != 'All' else (d.race == r).sum():,}"
                                            for s, d in samples for r in ("White", "Black")) + " |")
    for v, lab in dcols + [("log_earn", "Log lifetime earnings"), ("lpinc_av", "Log parental income 12-17"),
                           ("lw", "WJ Letter-Word (std score)"), ("ap", "WJ Applied Problems (std score)"),
                           ("pc", "WJ Passage Comprehension (std score)"), ("bpi_z", "BPI total (z within wave x age)")]:
        cells = []
        for s, d in samples:
            for r in ("White", "Black"):
                if v not in d:
                    cells.append("")
                    continue
                x = d.loc[d.race == r, v]
                cells.append(f"{x.mean():,.3f} ({x.notna().sum():,})" if x.notna().any() else "")
        md.append(f"| {lab} | " + " | ".join(cells) + " |")

    # ---- regressions: CDS
    specs = []
    for y, yl in (("lw", "Letter-Word"), ("ap", "Applied Problems"), ("bpi_z", "BPI (z)")):
        for r in ("White", "Black"):
            specs.append((f"{yl}, {r}", reg(c[c.race == r], y, ["lfinc05", "female"], ["birth_year", "wave"])))
    md += ["", "## 2. CDS test scores at ages 5-12 on early-childhood exposures", "",
           "One regression per column (outcome and race in the header). WJ standard scores (population mean 100, sd "
           "15); BPI = behaviour problems, higher = worse, z-scored within CDS wave x age. A child assessed in two "
           "waves contributes two rows. Controls: log family income at 0-5, female; fixed effects: birth year, CDS "
           "wave. Job loss and separation count only if they happened before the test year. S.e. clustered by fam68 "
           "in parentheses; *** p<0.01, ** p<0.05, * p<0.1.", "",
           table(specs, X + ["lfinc05", "female"]), "",
           "Fixed effects in every column: birth year, CDS wave."]

    # ---- regressions: adult earnings
    specs = []
    for ctrl in ("lpinc_av", "lfinc05"):
        for r in ("White", "Black"):
            specs.append((f"Log earnings, {r} ({'income 12-17' if ctrl == 'lpinc_av' else 'income 0-5'})",
                          reg(a[a.race == r], "log_earn", [ctrl, "female"], ["birth_year"])))
    md += ["", "## 3. Child's log lifetime earnings on childhood exposures", "",
           "Children born 1968-1997 in `psid_kids.pkl` (log of mean annual own labour earnings as head or wife at "
           "25-55, zeros kept, 3+ years). One regression per column. Controls: log parental income (mean at 12-17, "
           "or at 0-5), female; birth-year fixed effects. S.e. clustered by fam68; *** p<0.01, ** p<0.05, * p<0.1.",
           "", table(specs, X + ["lpinc_av", "lfinc05", "female"]), "",
           "Fixed effects in every column: birth year."]

    md += ["", "## Notes", "",
           "- Associations only. Mothers who work in the year after a birth, families hit by job loss or separation, "
           "and welfare recipients differ in unobserved ways; nothing here identifies the time-vs-money trade-off.",
           "- Mother's hours: family-file head/wife hours, else individual-file hours (1967-1992), else "
           "year-before-last weeks x hours/week (1997, 1999, 2001). After 1996 the survey is biennial and hours "
           "refer to even years only, so year +1 is missing for even-year births from 2002 on; children whose "
           "mother is not head or wife after 1993 have no hours.",
           "- Father figure = male head of the child's family unit (biological father, stepfather or partner); "
           "children never living with one have job loss = 0. In the biennial era job loss compares hours two years "
           "apart.",
           "- Welfare counts only head/wife AFDC/TANF (1967: head only) and family food stamps; no food stamp item "
           "for 1972. Years observed at 0-5 fall in the biennial era (partly offset by the 'two years ago' items).",
           "- CDS: WJ-R (1997-2007), WJ-III (2014), WJ-IV (2019) - CDS-wave fixed effects absorb level differences; "
           "2019 scores average about 5 points lower. CDS-2020/2021/2024 have no WJ assessment or BPI. Children "
           "born 2001+ are tested only in 2014/2019, so the birth-year fixed effects also absorb the WJ-III/IV vs "
           "WJ-R level shift; and since mother's year +1 hours exist only for odd birth years after 2000, the "
           "2014/2019 rows are odd-year births only.",
           "- Later birth cohorts are censored for the 0-17 measures (job loss, separation)."]
    OUT.mkdir(exist_ok=True)
    (OUT / "psid_child_exposure.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
