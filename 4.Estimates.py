r"""IGE estimates, PSID / NLSY79 / NLSY97, by sex and race, with the BFHO errors-in-variables correction (2026-10-16).

Regression (BFHO eq. 1), one per sample x outcome x parental-income measure:
    ln Y_child = rho0 + rho ln Y_parent + birth-year FE + quadratic in the parent's age at measurement
                 + quadratic in the child's mean age over the years averaged,
s.e. clustered by family (PSID 1968 family; NLSY household of the first round, i.e. siblings).
  Y_child: lifetime own earnings or family income = mean over the years observed at 25-55 (zeros kept, >= 3 years).
  Y_parent: (pt) one year, the child aged 16 (NLSY79: 1978 income; NLSY97: 1996 income), or
            (av) the mean over the years the child is 12-17 (NLSY79: 1978-80; NLSY97: 1996-99) while at home.
  Amounts below $1,000 (2000 dollars) are dropped on both sides.
Correction (BFHO Appendix B): rho = rho* / RR, RR = slope of log lifetime family income on the log of the same
point-in-time (or few-year mean) measure at the parents' age, estimated in the child generation of the same data set
(adults at 25-55; lifetime = mean over the years at least 3 years away from the measurement), race by race.
Pooled rows: "All" (Black + White, unweighted) and "All, weighted" (2026-10-17): the same regression weighted by the
child's sampling weight (PSID: core longitudinal weight in the wave the child is 16, wt_pt, zero weights dropped;
NLSY79: 1979 sampling weight wt79; NLSY97: 1997 sampling weight wt97), which undoes the SEO / Black oversamples;
the weighted rows are corrected with the unweighted pooled RR.
Writes output/ige_estimates.csv and output/ige_table.md.
"""
import numpy as np
import pandas as pd
from scipy.stats import norm

from common import DATA, OUT, AGE_LO, AGE_HI, ols, corrected, fmt

FLOOR = np.log(1000)
SETS = {"PSID": ("psid_kids.pkl", "psid_person_year.pkl"),
        "NLSY79": ("nlsy79_kids.pkl", "nlsy79_person_year.pkl"),
        "NLSY97": ("nlsy97_kids.pkl", "nlsy97_person_year.pkl")}
COLS = [("log_earn", "lpinc_pt", "Own earnings", "one year at 16"),
        ("log_earn", "lpinc_av", "Own earnings", "mean at 12-17"),
        ("log_fam", "lpinc_av", "Family income", "mean at 12-17")]
WEIGHT = {"PSID": "wt_pt", "NLSY79": "wt79", "NLSY97": "wt97"}


def load(name):
    k, p = (pd.read_pickle(DATA / f) for f in SETS[name])
    if name == "PSID":
        p = p[(p["head"] | p["wife"]) & p["age"].between(AGE_LO, AGE_HI)].rename(columns={"hrace": "race"})
    else:
        p = p.rename(columns={"hhid": "fam68"})
    if name == "NLSY79":
        k = k[k["age79"] <= 18]                     # at home in 1979 and born 1961-64 (age 14-18)
    for c in ("lpinc_pt", "lpinc_av", "log_earn", "log_fam"):
        k[c] = k[c].where(k[c] >= FLOOR)
    k = k[k["race"].isin(["White", "Black"])]
    k["w"] = k[WEIGHT[name]].astype(float).where(k[WEIGHT[name]] > 0)
    return k, p.dropna(subset=["faminc", "age"])


def reliability(p, center, window):
    """RR: lifetime log family income on log family income at age `center` (one year) or at center-3..center+2."""
    p = p.copy()
    if window:
        p["in"] = p["age"].between(center - 3, center + 2)
        p["out"] = ~p["age"].between(center - 6, center + 5)
        g_in = p[p["in"]].groupby("pid")
        x = pd.DataFrame({"x": g_in["faminc"].mean(), "nx": g_in["faminc"].count(), "age_x": g_in["age"].mean(),
                          "race": g_in["race"].agg(lambda s: s.mode().iat[0] if s.notna().any() else np.nan)})
        x = x[x["nx"] >= 2]
    else:
        p["dist"] = (p["age"] - center).abs()
        x = p[p["dist"] <= 2].sort_values(["pid", "dist"]).groupby("pid").first()
        x = x.rename(columns={"faminc": "x", "age": "age_x"})[["x", "age_x", "race"]]
        p = p.merge(x[["age_x"]], left_on="pid", right_index=True)
        p["out"] = (p["age"] - p["age_x"]).abs() >= 3
    g = p[p["out"]].groupby("pid")
    lt = pd.DataFrame({"lt": g["faminc"].mean(), "n_lt": g["faminc"].count()})
    info = p.groupby("pid")[["birth_year", "fam68"]].first()
    d = x.join(lt, how="inner").join(info)
    d = d[(d["n_lt"] >= 3) & (d["x"] >= 1000) & (d["lt"] >= 1000)]
    d["lx"], d["llt"] = np.log(d["x"]), np.log(d["lt"])
    d["age_x2"] = d["age_x"] ** 2
    out = {}
    for race in ("Black", "White", "All"):
        s = d if race == "All" else d[d["race"] == race]
        s = s[s["race"].isin(["Black", "White"])]
        b, se, pv, n, _ = ols(s, "llt", "lx", controls=["age_x", "age_x2"], fe=["birth_year"], cluster="fam68")
        out[race] = (b, se, n)
    return out


def main():
    OUT.mkdir(exist_ok=True)
    rows = []
    for name in SETS:
        k, p = load(name)
        c_pt, c_av = round(k["page_pt"].median()), round(k["page_av"].median())
        RR = {"lpinc_pt": reliability(p, c_pt, False), "lpinc_av": reliability(p, c_av + 0.5, True)}
        print(f"{name}: parents' median age {c_pt} (one year), {c_av} (mean);  RR one year "
              + ", ".join(f"{r} {v[0]:.3f}" for r, v in RR["lpinc_pt"].items()) + ";  RR mean "
              + ", ".join(f"{r} {v[0]:.3f}" for r, v in RR["lpinc_av"].items()), flush=True)
        for female, sex in ((0, "Men"), (1, "Women")):
            for race in ("Black", "White", "All", "All, weighted"):
                s = k[k["female"] == female]
                if race in ("Black", "White"):
                    s = s[s["race"] == race]
                for y, x, ylab, xlab in COLS:
                    am = "age_mean_earn" if y == "log_earn" else "age_mean_fam"
                    pa = "page_pt" if x == "lpinc_pt" else "page_av"
                    s = s.assign(am2=s[am] ** 2, pa2=s[pa] ** 2)
                    b, se, pv, n, _ = ols(s, y, x, controls=[am, "am2", pa, "pa2"], fe=["birth_year"],
                                          cluster="fam68", weight="w" if race == "All, weighted" else None)
                    rr, rr_se, rr_n = RR[x][race.split(",")[0]]
                    bc, sec = corrected(b, se, rr, rr_se)
                    rows.append(dict(data=name, sex=sex, race=race, outcome=ylab, parent=xlab, rho=b, se=se, p=pv,
                                     n=n, rr=rr, rr_se=rr_se, rr_n=rr_n, rho_c=bc, se_c=sec,
                                     p_c=2 * (1 - norm.cdf(abs(bc / sec)))))
    res = pd.DataFrame(rows)
    res.to_csv(OUT / "ige_estimates.csv", index=False)

    # markdown: one regression per column; samples as row panels
    lines = ["# Intergenerational elasticity of earnings (BFHO 2024 definition)", "",
             "Columns: (1) child's log lifetime own earnings on log parental family income in one year (child 16); "
             "(2) same outcome, parental income averaged over child ages 12-17; (3) child's log lifetime family "
             "income, parental mean. Child lifetime = mean over ages 25-55 (zeros kept). Controls: child birth-year "
             "FE, quadratics in parent's age and child's mean age. S.e. clustered by family. Corrected = rho / RR "
             "(BFHO Appendix B), RR estimated in the child generation of the same data set, race by race. "
             "All = Black + White, unweighted; All, weighted = weighted by the child's sampling weight (PSID wt_pt, "
             "NLSY79 wt79, NLSY97 wt97), corrected with the unweighted pooled RR. "
             "*** p<0.01, ** p<0.05, * p<0.1.", ""]
    head = "| | " + " | ".join(f"({i + 1}) {c[2]} / parents {c[3]}" for i, c in enumerate(COLS)) + " |"
    for (name, sex, race), g in res.groupby(["data", "sex", "race"], sort=False):
        g = g.set_index(["outcome", "parent"]).loc[[(c[2], c[3]) for c in COLS]]
        lines += [f"**{name} - {sex} - {race}**", "", head, "|---" * (len(COLS) + 1) + "|",
                  "| IGE, uncorrected | " + " | ".join(fmt(r.rho, r.se, r.p) for r in g.itertuples()) + " |",
                  "| Reliability ratio | " + " | ".join(f"{r.rr:.3f} ({r.rr_se:.3f})" for r in g.itertuples()) + " |",
                  "| IGE, corrected | " + " | ".join(fmt(r.rho_c, r.se_c, r.p_c) for r in g.itertuples()) + " |",
                  "| N | " + " | ".join(f"{r.n:,}" for r in g.itertuples()) + " |", ""]
    (OUT / "ige_table.md").write_text("\n".join(lines), encoding="utf-8")
    show = res[res.outcome.eq("Own earnings")].copy()
    show["IGE"] = [fmt(a, b, c) for a, b, c in zip(show.rho, show.se, show.p)]
    show["IGE corrected"] = [fmt(a, b, c) for a, b, c in zip(show.rho_c, show.se_c, show.p_c)]
    print(show[["data", "sex", "race", "parent", "IGE", "rr", "IGE corrected", "n"]].to_string(index=False))


if __name__ == "__main__":
    main()
