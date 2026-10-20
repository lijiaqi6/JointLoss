r"""Rank mobility by race and sex, PSID and NLSY79: Chetty-comparable statistics (2026-10-17).

Definitions follow Chetty, Hendren, Jones and Porter (2020, QJE 135(2); Literature/qjz042.pdf, Table I and Section
IV.A) as far as the surveys allow:
  parents' income = mean family income while the child lives at home at 12-17 (PSID: >= 3 waves, psid_kids
           pinc_av; NLSY79: 1978-80 rounds, nlsy79_kids pinc_av). Parents are ranked (0-100, weighted mid-ranks)
           relative to all parents with children in the same birth year, all races in the file (PSID: SRC + SEO,
           weight wt_pt = core longitudinal weight in the wave the child is 16, zero weights dropped; NLSY79:
           cross-sectional + Black supplemental samples living with a parent in 1979, born 1960-64, weight wt79).
  child's income = mean family income of the child's own household (years as head / wife in the PSID; all rounds in
           the NLSY79) at ages 31-37 (Chetty: 2014-15 household income at 31-37), >= 2 years, zeros and negatives
           kept; robustness: the mean over 25-55 (>= 3 years; the lifetime measure of psid_kids / nlsy79_kids, but
           keeping means <= 0). Children are ranked relative to all children of the same birth year in the file,
           with the same weights.
Statistics by race x sex (and both sexes), weighted: rank-rank slope and intercept (WLS of child rank on parent
rank), expected child rank at parental p25 and p75 from that line, mean child rank, P(child top quintile | parents
top quintile), P(child bottom quintile | parents top quintile), P(child top quintile | parents bottom quintile)
(quintile = rank above 80 / at most 20). White - Black gaps. S.e.: 200 bootstrap draws of families (PSID 1968 family
number; NLSY79 1979 household), ranks held at their full-sample values. p-values (normal) against: 0 for slopes and
gaps; 50 for ranks; 20 for quintile probabilities (independence).
Writes output/rank_mobility.csv and output/rank_mobility.md.
"""
import numpy as np
import pandas as pd
from scipy.stats import norm

from common import DATA, OUT, stars

REPS, SEED = 200, 20261017
STATS = [("slope", "Rank-rank slope", 0), ("e25", "E[rank] at p25", 50), ("e75", "E[rank] at p75", 50),
         ("mean", "Mean child rank", 50), ("q55", "P(Q5 given parents Q5)", 20), ("q15", "P(Q1 given parents Q5)", 20),
         ("q51", "P(Q5 given parents Q1)", 20)]
GROUPS = [(r, s) for s in ("Men", "Women", "Both") for r in ("Black", "White")]
# Chetty et al. (2020) Table I Panel B and Section IV.A: household income, cohorts 1978-83, both sexes
CHETTY = {("White", "slope"): 0.32, ("Black", "slope"): 0.28, ("White", "e25"): 45.2, ("Black", "e25"): 32.6,
          ("White", "mean"): 55.7, ("Black", "mean"): 34.8, ("White", "q55"): 41.1, ("Black", "q55"): 18.0,
          ("White", "q15"): 8.7, ("Black", "q15"): 16.7, ("White", "q51"): 10.6, ("Black", "q51"): 2.5}


def wrank(v, w):
    """weighted mid-rank (0-100) of v, ties averaged."""
    o = np.argsort(v, kind="stable")
    cw = np.cumsum(w[o])
    mid = pd.Series((cw - w[o] / 2) / cw[-1] * 100).groupby(v[o]).transform("mean").to_numpy()
    r = np.empty(len(v))
    r[o] = mid
    return r


def rank_within(d, col, by="birth_year"):
    d = d[d[col].notna() & (d["w"] > 0)]
    return pd.concat([pd.Series(wrank(g[col].to_numpy(), g["w"].to_numpy()), index=g.index)
                      for _, g in d.groupby(by)])


def child_income(p, lo, hi, nmin):
    a = p[p["age"].between(lo, hi)].dropna(subset=["faminc"]).groupby("pid")["faminc"].agg(["mean", "count"])
    return a.loc[a["count"] >= nmin, "mean"]


def load():
    """{data set: (kids with weight w, birth_year, race, female, fam68, pinc; person-year with pid, age, faminc)}"""
    k = pd.read_pickle(DATA / "psid_kids.pkl")
    k = k.assign(w=k["wt_pt"], pinc=k["pinc_av"].where(k["n_av"] >= 3)).set_index("pid")
    p = pd.read_pickle(DATA / "psid_person_year.pkl")
    p = p[p["head"] | p["wife"]]
    n = pd.read_pickle(DATA / "nlsy79_kids.pkl")
    n = n[n["age79"] <= 18].assign(w=lambda x: x["wt79"].astype(float), pinc=lambda x: x["pinc_av"]).set_index("pid")
    q = pd.read_pickle(DATA / "nlsy79_person_year.pkl")
    return {"PSID": (k, p), "NLSY79": (n, q)}


def stats(rp, rc, w):
    m = np.average(rp, weights=w)
    b = np.average((rp - m) * rc, weights=w) / np.average((rp - m) ** 2, weights=w)
    mc = np.average(rc, weights=w)
    a = mc - b * m
    top, bot = rp > 80, rp <= 20
    pr = lambda cond, base: 100 * np.sum(w * cond * base) / np.sum(w * base)
    return dict(slope=b, e25=a + 25 * b, e75=a + 75 * b, mean=mc, q55=pr(rc > 80, top), q15=pr(rc <= 20, top),
                q51=pr(rc > 80, bot))


def all_stats(d):
    out = {}
    for race, sex in GROUPS:
        g = d[(d["race"] == race) & ((d["female"] == (sex == "Women")) | (sex == "Both"))]
        out[(race, sex)] = stats(g["rp"].to_numpy(), g["rc"].to_numpy(), g["w"].to_numpy())
    for sex in ("Men", "Women", "Both"):
        out[("White - Black", sex)] = {s: out[("White", sex)][s] - out[("Black", sex)][s] for s, _, _ in STATS}
    return out


def bootstrap(d, rng):
    d = d.reset_index(drop=True)
    fam = pd.factorize(d["fam68"])[0]
    rows = pd.Series(np.arange(len(d))).groupby(fam).apply(np.array).to_list()
    draws = []
    for _ in range(REPS):
        pick = rng.integers(0, len(rows), len(rows))
        draws.append(all_stats(d.iloc[np.concatenate([rows[i] for i in pick])]))
    return draws


def main():
    rng = np.random.default_rng(SEED)
    sets = load()
    res = []
    for name, (k, p) in sets.items():
        k = k.copy()
        k["rp"] = rank_within(k, "pinc")
        for lab, (lo, hi, nmin), cohorts in (("child 31-37", (31, 37, 2), None),
                                             ("child 31-37, cohorts 1978-83", (31, 37, 2), (1978, 1983)),
                                             ("child lifetime 25-55", (25, 55, 3), None)):
            if name == "NLSY79" and cohorts:
                continue
            k["yc"] = child_income(p, lo, hi, nmin)
            k["rc"] = rank_within(k, "yc")
            d = k[k["race"].isin(["Black", "White"])].dropna(subset=["rp", "rc"])
            if cohorts:
                d = d[d["birth_year"].between(*cohorts)]
            est, draws = all_stats(d), bootstrap(d, rng)
            for grp, e in est.items():
                for s, slab, h0 in STATS:
                    se = np.std([b[grp][s] for b in draws], ddof=1)
                    h = 0 if grp[0] == "White - Black" else h0
                    sub = d if grp[0] == "White - Black" else d[d["race"] == grp[0]]
                    sub = sub if grp[1] == "Both" else sub[sub["female"] == (grp[1] == "Women")]
                    res.append(dict(data=name, measure=lab, race=grp[0], sex=grp[1], stat=s, label=slab, est=e[s],
                                    se=se, h0=h, p=2 * (1 - norm.cdf(abs(e[s] - h) / se)), n=len(sub),
                                    n_pq1=int((sub["rp"] <= 20).sum()), n_pq5=int((sub["rp"] > 80).sum()),
                                    families=sub["fam68"].nunique(),
                                    cohorts=f"{int(d['birth_year'].min())}-{int(d['birth_year'].max())}"))
            print(f"{name}, {lab}: {len(d):,} children, cohorts {d['birth_year'].min():.0f}-"
                  f"{d['birth_year'].max():.0f}", flush=True)
    res = pd.DataFrame(res)
    OUT.mkdir(exist_ok=True)
    res.to_csv(OUT / "rank_mobility.csv", index=False)
    write_md(res)
    res["cell"] = [cell(e, se, p, s) for e, se, p, s in zip(res.est, res.se, res.p, res.stat)]
    tab = res.pivot_table(index=["data", "measure", "sex", "race"], columns="stat", values="cell", aggfunc="first",
                          sort=False)
    pd.set_option("display.width", 300)
    print(tab[[s for s, _, _ in STATS]].to_string())


def cell(e, se, p, s):
    pv = "<0.001" if p < 0.001 else f"{p:.3f}"
    return (f"{e:.3f}{stars(p)} ({se:.3f}; p={pv})" if s == "slope" else f"{e:.1f}{stars(p)} ({se:.1f}; p={pv})")


def write_md(res):
    lines = ["# Rank mobility by race and sex (Chetty-comparable statistics)", "",
             "Child's household (family) income rank within birth year on parents' family income rank within the "
             "child's birth year; weighted (PSID core longitudinal weight at child age 16; NLSY79 1979 sampling "
             "weight); ranks among all children in the file (PSID SRC + SEO; NLSY79 Black + non-Black non-Hispanic). "
             "Parents: mean family income at child ages 12-17 (NLSY79: 1978-80). Child: mean family income of own "
             "household at 31-37 (>= 2 years) or 25-55 (>= 3 years). E[rank] at parental percentile p from the rank-rank line. "
             "Q1 / Q5 = bottom / top quintile. Ranks and probabilities in percent. Bootstrap s.e. (200 draws of "
             "families) in parentheses with the p-value; nulls: slope = 0, ranks = 50, probabilities = 20 "
             "(independence), White - Black gaps = 0. *** p<0.01, ** p<0.05, * p<0.1.", ""]
    for (name, lab), g in res.groupby(["data", "measure"], sort=False):
        lines += [f"## {name}, {lab} (cohorts {g['cohorts'].iat[0]})", "",
                  "| | " + " | ".join(s[1] for s in STATS) + " | N children (parents Q1 / Q5) |",
                  "|---" * (len(STATS) + 2) + "|"]
        for sex in ("Men", "Women", "Both"):
            lines.append(f"| **{'Sons' if sex == 'Men' else 'Daughters' if sex == 'Women' else 'Both sexes'}** |"
                         + " |" * (len(STATS) + 1))
            for race in ("Black", "White", "White - Black"):
                h = g[(g["sex"] == sex) & (g["race"] == race)].set_index("stat").loc[[s[0] for s in STATS]]
                n = f"{h['n'].iat[0]:,} ({h['n_pq1'].iat[0]:,} / {h['n_pq5'].iat[0]:,})"
                lines.append(f"| {race} | " + " | ".join(cell(r.est, r.se, r.p, s) for s, r in
                                                          zip(h.index, h.itertuples())) + f" | {n} |")
        lines.append("")
    # comparison with Chetty et al. (2020), verified against the published article
    lines += ["## Comparison with Chetty, Hendren, Jones and Porter (2020, QJE), both sexes", "",
              "Theirs: Table I Panel B (household income: mean child rank, quintile transitions) and Section IV.A "
              "(rank-rank slopes 0.32 White / 0.28 Black; E[rank] at p25 = 32.6 Black, 12.6 below White). Cohorts "
              "1978-83, child household income 2014-15 at ages 31-37, parents' household income 1994-95 and "
              "1998-2000, ranks among all US children / parents (all races). E[rank] at p75 and the by-sex numbers "
              "(their Online Appendix Table V) are not in the article text and are not compared. Ours: PSID, child "
              "31-37, both sexes.", "",
              "| | Chetty et al. White | PSID White, all cohorts | PSID White, 1978-83 | Chetty et al. Black | "
              "PSID Black, all cohorts | PSID Black, 1978-83 |", "|---" * 7 + "|"]
    ps = res[(res["data"] == "PSID") & (res["sex"] == "Both")]
    for s, slab, _ in STATS:
        if ("White", s) not in CHETTY:
            continue
        c = []
        for race in ("White", "Black"):
            c.append(f"{CHETTY[(race, s)]:.2f}" if s == "slope" else f"{CHETTY[(race, s)]:.1f}")
            for m in ("child 31-37", "child 31-37, cohorts 1978-83"):
                r = ps[(ps["measure"] == m) & (ps["race"] == race) & (ps["stat"] == s)].iloc[0]
                c.append(cell(r.est, r.se, r.p, s))
        lines.append(f"| {slab} | " + " | ".join(c) + " |")
    (OUT / "rank_mobility.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
