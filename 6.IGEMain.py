r"""Main PSID IGE: the Lee-Solon age-40 design of 5.CheckPMR.py for sons and daughters, by race (2026-10-17).

Sample (from data/psid_person_year.pkl; PSID core = SRC + SEO):
  parents: the family unit the child lives in as the head's child at 13-19; ln of mean total family income over
           those years (>= 3 years); the head's age A when the child is 16 (nearest wave) between 30 and 70; the
           child's race = the race of that head (so a daughter's race does not change with her husband's).
  children: one row per child-year as head or spouse / partner ("wife") at 25-65 (Lee and Solon 2009 pooled design);
           sons and daughters separately. Daughters enter as heads (mostly single) and as wives; outcomes:
             ln total family income of the child's own household (all income years; and income years 1980-2010,
             the Palomino-Marrero-Rodriguez window), and
             ln own labor earnings (head / wife labor income, 1994+ with the labor part of business income), years
             with positive earnings only.
  yearly amounts below $100 or above $150,000 in 1967 dollars dropped (parents and children; PMR 2018).
Regression (PMR eq. 2): ln y_child on ln y_parent, quartics in (A - 45)/10 and C/10 with C = child's age - 40, and
ln y_parent x (C/10)^n, n = 1..4, so the coefficient on ln y_parent is the IGE at age 40. S.e. clustered by child.
Samples: Black, White (parental race), and pooled (all races) (i) unweighted, (ii) weighted by the core longitudinal
weight of the child's person-year (zero weights dropped), (iii) SRC only (1968 family number <= 2930), unweighted.
Writes output/ige_main.csv and output/ige_main.md.
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm

from common import DATA, OUT, CPI, fmt

LO, HI = (v * CPI[2000] / CPI[1967] for v in (100, 150_000))           # 1967 dollars -> 2000 dollars
COLS = [("lfam", None, "ln family income, all years"),
        ("lfam", (1980, 2010), "ln family income, 1980-2010"),
        ("learn", None, "ln own earnings (> 0), all years")]
SAMPLES = ["Black", "White", "Pooled, unweighted", "Pooled, weighted", "Pooled, SRC only"]


def parents(py):
    k = py[py["child"] & py["age"].between(13, 19) & py["faminc"].between(LO, HI)]
    g = k.groupby("pid")
    par = pd.DataFrame({"yp": g["faminc"].mean(), "np": g["faminc"].count()})
    k16 = k.assign(dist=(k["age"] - 16).abs()).sort_values(["pid", "dist"]).groupby("pid").first()
    par["A"], par["race"] = k16["hage"], k16["hrace"]
    return par[(par["np"] >= 3) & par["A"].between(30, 70)]


def build(py):
    s = py[(py["head"] | py["wife"]) & py["age"].between(25, 65)].join(parents(py), on="pid", how="inner")
    s["year"] = s["wave"] - 1                                            # income year
    s["lfam"] = np.log(s["faminc"].where(s["faminc"].between(LO, HI)))
    s["learn"] = np.log(s["earn"].where(s["earn"].between(LO, HI)))
    s["lyp"], s["C"] = np.log(s["yp"]), s["age"] - 40
    for n in range(1, 5):
        s[f"A{n}"], s[f"C{n}"] = ((s["A"] - 45) / 10) ** n, (s["C"] / 10) ** n
        s[f"lypC{n}"] = s["lyp"] * s[f"C{n}"]
    return s


def ige(d, y, w=None):
    xc = ["lyp"] + [f"{v}{n}" for v in ("A", "C", "lypC") for n in range(1, 5)]
    d = d.dropna(subset=[y] + xc + ([w] if w else []))
    if w:
        d = d[d[w] > 0]
    X = sm.add_constant(d[xc].astype(float))
    mod = sm.WLS(d[y], X, weights=d[w]) if w else sm.OLS(d[y], X)
    r = mod.fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d["pid"])[0]})
    return dict(beta=r.params["lyp"], se=r.bse["lyp"], p=r.pvalues["lyp"], n=int(r.nobs),
                children=d["pid"].nunique(), mean_y=np.average(d[y], weights=d[w] if w else None),
                mean_age=np.average(d["age"], weights=d[w] if w else None),
                black=np.average(d["race"].eq("Black"), weights=d[w] if w else None))


def main():
    s = build(pd.read_pickle(DATA / "psid_person_year.pkl"))
    rows = []
    for female, sex in ((0, "Sons"), (1, "Daughters")):
        x = s[s["female"] == female]
        for samp in SAMPLES:
            d, w = (x[x["race"] == samp], None) if samp in ("Black", "White") else (x, None)
            if samp == "Pooled, weighted":
                w = "wt"
            elif samp == "Pooled, SRC only":
                d = x[x["fam68"] <= 2930]
            for y, yrs, lab in COLS:
                dd = d if yrs is None else d[d["year"].between(*yrs)]
                rows.append(dict(sex=sex, sample=samp, outcome=lab, **ige(dd, y, w)))
    res = pd.DataFrame(rows)
    OUT.mkdir(exist_ok=True)
    res.to_csv(OUT / "ige_main.csv", index=False)

    lines = ["# Main PSID IGE: Lee-Solon pooled design, IGE at age 40", "",
             "One regression per column; the outcome is the column header. Rows: coefficient on ln parents' mean "
             "family income at child ages 13-19 (the IGE at child age 40) with (s.e.; p-value), then the sample size. "
             "Child-years as head or spouse at 25-65; controls: quartics in (parent's age at 16 - 45)/10 and "
             "(child's age - 40)/10, and ln parental income x the age quartic. Income years 1967-2022 unless the "
             "column says otherwise. Race = parental household head's race. Pooled = all races. Weighted = core "
             "longitudinal weight of the child's person-year. SRC only = 1968 family number <= 2930. "
             "S.e. clustered by child. *** p<0.01, ** p<0.05, * p<0.1.", ""]
    for sex in ("Sons", "Daughters"):
        lines += [f"## {sex}", "", "| | " + " | ".join(f"({i + 1}) {c[2]}" for i, c in enumerate(COLS)) + " |",
                  "|---" * (len(COLS) + 1) + "|"]
        for samp in SAMPLES:
            g = res[(res["sex"] == sex) & (res["sample"] == samp)].set_index("outcome").loc[[c[2] for c in COLS]]
            lines += [f"| **{sex}: {samp}** |" + " |" * len(COLS),
                      "| ln parental income (IGE at 40) | " + " | ".join(fmt(r.beta, r.se, r.p) for r in g.itertuples())
                      + " |",
                      "| Child-years / children | " + " | ".join(f"{r.n:,} / {r.children:,}" for r in g.itertuples())
                      + " |"]
        lines.append("")
    (OUT / "ige_main.md").write_text("\n".join(lines), encoding="utf-8")
    res["IGE"] = [fmt(b, se, p) for b, se, p in zip(res.beta, res.se, res.p)]
    pd.set_option("display.width", 250)
    print(res[["sex", "sample", "outcome", "IGE", "n", "children", "mean_y", "mean_age", "black"]].round(3)
          .to_string(index=False))


if __name__ == "__main__":
    main()
