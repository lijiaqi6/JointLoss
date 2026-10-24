r"""Are we sure the EITC has no effect on the IGE? Placebo windows, income bands, scaling, calibration (PI, 2026-10-24)

128: exposure x parental income is ~0 at every age, but the design detects only large effects, tests a linear shape
while the credit is hump-shaped in income, and is diluted intent to treat. And 101 / 126's within-son growth with
exposure (0.029*** a decade per $1,000; 0.064*** in likely-eligible families) is implausibly large, which suggests it
picks up something else that varies with the schedule.
SCHEDULE EXPOSURE (one definition for all windows): sum over calendar years of [federal maximum for the family's
  teen-window modal number of children x (1 + the state-at-17's EITC rate)], 2000 dollars, scaled to six years, for
  the son's ages 13-18 (teen), 6-11 (pre; before the credit can reach his teens) and 19-24 (post; after). The teen
  version is 101's exposure with the children and state held at their window values.
DESIGNS (101's sample and FE: birth-year, state-at-17, number-of-children; PSID weights; clusters 1968 family):
  1. within son: ln earnings on exposure x (age-40)/10 for each window, alone and jointly, with birth-year x age,
     children x age and single-age dummies; all sons and the likely-eligible tercile (126's logit).
  2. by parental-income tercile (pooled, within birth year): exposure x tercile by band 25-29 and 40-44 and within son;
     rank-rank: son's earnings rank (within birth year and band) on parents' rank with exposure x parents' rank and
     exposure x bottom tercile.
  3. scaling: share of window years in the credit's range by tercile; calibration: if the credit passed on like other
     parental income with elasticity e = the IGE at the band, the son's gain is e x ln(1 + credit / family income) and
     its slope on ln parental income is the IGE change the credit could produce.
Writes output/eitc_checks.md / .json (aggregates only). DESCRIPTIVE.
"""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import CPI, DATA, OUT  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R127 = _load("s127", "127.EITCMothers.py")
R126, R101 = R127.R126, R127.R101
R75, R72 = R101.R75, R101.R72
c, ols, dummies, BL = R101.c, R101.ols, R101.dummies, R101.BL
RES = {}


def sched(one, lo, hi):
    pc = pd.read_csv(DATA / "policy_calendar.csv", usecols=["state_fips", "year", "state_eitc_rate"])
    rate = {(int(f), int(y)): float(x) for f, y, x in zip(pc["state_fips"], pc["year"], pc["state_eitc_rate"].fillna(0))}
    out = []
    for b, n, f in zip(one["birth_year"], one["nk_mode"], one["st17"]):
        tot = 0.0
        ys = range(int(b) + lo, int(b) + hi + 1)
        for y in ys:
            if y not in CPI:
                continue
            tot += R101.fed_max(y, int(n)) * (1 + rate.get((int(f), y), 0.0)) * CPI[2000] / CPI[y] / 1000
        out.append(tot * 6 / len(ys))
    return np.array(out)


def fe_growth(d, xs):
    a = d["agec"].to_numpy()[:, None]
    X = np.column_stack([d[xs].to_numpy(float) * a, dummies(d["birth_year"]) * a, dummies(d["nk_mode"]) * a,
                         dummies(d["age"])])
    b, V = ols(X, d["ly"].to_numpy(float), d["wt"].to_numpy(float), d["fam68"].to_numpy(), absorb=d["pid"].to_numpy())
    return [(b[i], float(np.sqrt(V[i, i]))) for i in range(len(xs))]


def band_reg(q, xs):
    X = np.column_stack([q[xs].to_numpy(float), dummies(q["birth_year"]), dummies(q["st17"]), dummies(q["nk_mode"]),
                         dummies(q["age"]), np.ones(len(q))])
    b, V = ols(X, q["ly"].to_numpy(float), q["wt"].to_numpy(float), q["fam68"].to_numpy())
    return b, V


def main():
    r = R75.build()
    W = R126.window_years(r)
    r = r.merge(R101.exposure(r), on="pid", how="inner")
    r = r[r["win0"] >= 1975].copy()
    r = R72.state17(r)
    r["st17"] = r["fips17"].fillna(-1).astype(int)
    r["agec"] = (r["age"] - 40) / 10
    one = r.drop_duplicates("pid")[["pid", "birth_year", "nk_mode", "st17", "lyp", "wt"]].copy()
    for lab, lo, hi in (("ex_teen", 13, 18), ("ex_pre", 6, 11), ("ex_post", 19, 24)):
        one[lab] = sched(one, lo, hi)
    one["pterc"] = one.groupby("birth_year")["lyp"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    one["prk"] = one.groupby("birth_year")["lyp"].rank(pct=True)
    # likely eligible (126's logit, re-fit)
    import statsmodels.api as sm
    o2 = r.drop_duplicates("pid")[["pid", "m_educ0", "m_educ_na"]]
    Z = W.merge(o2, on="pid", how="left").merge(R126.pre_income(r), left_on="pid", right_index=True, how="left")
    Z = Z.dropna(subset=["lyp612"]).copy()
    Z["m_ed"] = Z["m_educ0"].where(Z["m_educ_na"] == 0, Z["m_educ0"].mean())
    X = pd.concat([Z[["lyp612", "m_ed", "m_educ_na", "nofa"]].astype(float),
                   pd.get_dummies(Z["nk"], prefix="nk", drop_first=True, dtype=float),
                   pd.get_dummies(Z["year"], prefix="y", drop_first=True, dtype=float)], axis=1)
    Z["p"] = sm.Logit(Z["elig"], sm.add_constant(X)).fit(disp=0).predict(sm.add_constant(X))
    pe = Z.groupby("pid")["p"].mean()
    one["likely"] = one["pid"].map((pe >= pe.quantile(2 / 3)).astype(float))
    r = r.merge(one[["pid", "ex_teen", "ex_pre", "ex_post", "pterc", "prk", "likely"]], on="pid", how="left")
    v = r[r["lw"].notna() & r["band"].between(0, 4)].copy()
    md = ["# Are we sure the EITC has no effect on the IGE? (PI question)", "",
          "Built by `129.EITCChecks.py` (2026-10-24); design in its docstring. Exposure in thousands of 2000 dollars, "
          "scaled to six years; s.e. clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**", "",
          f"Sons {one['pid'].nunique():,}. Schedule exposure means: teen {one['ex_teen'].mean():.2f}, pre (6-11) "
          f"{one['ex_pre'].mean():.2f}, post (19-24) {one['ex_post'].mean():.2f}; corr(teen, 101's exposure) "
          f"{np.corrcoef(one['ex_teen'], r.drop_duplicates('pid')['eitc'])[0, 1]:.3f}; corr(teen, pre) "
          f"{np.corrcoef(one['ex_teen'], one['ex_pre'])[0, 1]:.3f}, corr(teen, post) "
          f"{np.corrcoef(one['ex_teen'], one['ex_post'])[0, 1]:.3f}.", "",
          "## 1. Placebo windows: within-son growth of ln earnings per $1,000 x (age-40)/10", "",
          "| sample | specification | teen (13-18) | pre (6-11) | post (19-24) | sons |", "|---|---|---|---|---|---|"]
    for slab, q in (("all sons", v), ("likely eligible", v[v["likely"] == 1])):
        for spec, xs in (("101's exposure", ["eitc"]), ("teen alone", ["ex_teen"]), ("pre alone", ["ex_pre"]),
                         ("post alone", ["ex_post"]), ("all three", ["ex_teen", "ex_pre", "ex_post"])):
            est = dict(zip(xs, fe_growth(q, xs)))
            cell = lambda k: c(est[k]) if k in est else ""  # noqa: E731
            t = cell("eitc") if "eitc" in est else cell("ex_teen")
            md.append(f"| {slab} | {spec} | {t} | {cell('ex_pre')} | {cell('ex_post')} | {q['pid'].nunique():,} |")
            RES[f"placebo|{slab}|{spec}"] = {k: list(map(float, x)) for k, x in est.items()}
            print(md[-1], flush=True)
    md.append("")
    # 2. by tercile
    for t in range(3):
        v[f"ex_t{t}"] = v["eitc"] * (v["pterc"] == t)
        v[f"t{t}"] = (v["pterc"] == t).astype(float)
    md += ["## 2. By parental-income tercile (within birth year)", "",
           "| | bottom | middle | top | bottom - top |", "|---|---|---|---|---|"]
    for k in (0, 4):
        q = v[v["band"] == k]
        b, V = band_reg(q, ["ex_t0", "ex_t1", "ex_t2", "t1", "t2"])
        d0 = (b[0] - b[2], float(np.sqrt(V[0, 0] + V[2, 2] - 2 * V[0, 2])))
        md.append(f"| ln earnings at {BL[k]}, per $1,000 | " + " | ".join(c((b[i], np.sqrt(V[i, i]))) for i in range(3))
                  + f" | {c(d0)} |")
        RES[f"terc|{BL[k]}"] = [[float(b[i]), float(np.sqrt(V[i, i]))] for i in range(3)] + [list(d0)]
    g = fe_growth(v, ["ex_t0", "ex_t1", "ex_t2"])
    md.append("| within son x age, per $1,000 | " + " | ".join(c(x) for x in g) + " | |")
    RES["terc|fe"] = [list(map(float, x)) for x in g]
    # rank-rank
    v["srank"] = v.groupby(["birth_year", "band"])["ly"].rank(pct=True)
    v["ex_pr"] = v["eitc"] * (v["prk"] - 0.5)
    v["ex_bot"] = v["eitc"] * (v["pterc"] == 0)
    v["pr"] = v["prk"]
    md += ["", "Rank-rank (son's earnings rank within birth year and band on parents' rank), per $1,000 of exposure:", "",
           "| band | rank-rank at mean exposure | exposure x parents' rank | exposure x bottom tercile |", "|---|---|---|---|"]
    for k in (0, 2, 4):
        q = v[v["band"] == k].copy()
        q["ly"] = q["srank"]
        b, V = band_reg(q, ["pr", "ex_pr", "ex_bot", "eitc"])
        md.append(f"| {BL[k]} | {c((b[0], np.sqrt(V[0, 0])))} | {c((b[1], np.sqrt(V[1, 1])))} | "
                  f"{c((b[2], np.sqrt(V[2, 2])))} |")
        RES[f"rank|{BL[k]}"] = [[float(b[i]), float(np.sqrt(V[i, i]))] for i in range(3)]
    md.append("")
    # 3. scaling and calibration
    Wt = W.merge(one[["pid", "pterc", "lyp"]], on="pid", how="inner")
    nom = (Wt["hlab"].fillna(0) + Wt["wlab"].fillna(0)) / Wt["defl"]
    Wt["credit"] = [R127.credit(e, int(n), int(y), f == 0) for e, n, y, f in zip(nom, Wt["nk"], Wt["year"], Wt["nofa"])]
    Wt["credit"] = Wt["credit"] * (1 + Wt["state_eitc_rate"]) * Wt["defl"]
    py = pd.read_pickle(DATA / "psid_person_year.pkl")[["wave", "int", "faminc"]].drop_duplicates(["wave", "int"])
    Wt = Wt.merge(py, on=["wave", "int"], how="left")
    sh = Wt.groupby("pterc").agg(elig=("elig", "mean"), credit=("credit", "mean"), faminc=("faminc", "mean"))
    per = Wt.groupby("pid").agg(cr=("credit", "mean"), inc=("faminc", "mean"), lyp=("lyp", "first"))
    per = per[per["inc"] > 0]
    per["dl"] = np.log1p(per["cr"] / per["inc"])
    slope = float(np.polyfit(per["lyp"], per["dl"], 1)[0])
    md += ["## 3. Scaling and calibration", "",
           "| parental-income tercile | window years in the credit's range | imputed credit per year (2000 $) | family "
           "income per year |", "|---|---|---|---|"]
    for t, lab in enumerate(("bottom", "middle", "top")):
        md.append(f"| {lab} | {sh.loc[t, 'elig']:.3f} | {sh.loc[t, 'credit']:,.0f} | {sh.loc[t, 'faminc']:,.0f} |")
    ige = {k: RES.get(f"ige{k}") for k in (0, 4)}
    md += ["", f"The credit raises the family's log income by ln(1 + credit / income); its slope on ln parental income is "
           f"{slope:.4f}. If the credit passed on like other parental income with the IGE as the pass-through (0.28 at "
           f"25-29, 0.44 at 45-49; an upper bound, since not all of the IGE is causal), it would change the IGE by "
           f"{0.28 * slope:+.4f} at 25-29 and {0.44 * slope:+.4f} at 45-49, against detectable effects of 0.08 and 0.14 "
           "per standard deviation of exposure (128).", ""]
    RES["calib"] = {"slope": slope, "ige_change_2529": 0.28 * slope, "ige_change_4549": 0.44 * slope,
                    "by_tercile": sh.reset_index().to_dict(orient="records")}
    (OUT / "eitc_checks.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "eitc_checks.json", "w"), indent=1, default=float)
    print("\n".join(md))


if __name__ == "__main__":
    main()
