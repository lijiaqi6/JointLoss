r"""The EITC in childhood re-scored by the son's age (Fable optional addition F, 2026-10-20).

Long-run evaluations of childhood policies score adult outcomes in the late twenties or early thirties. Bastian and
Michelmore (2018, JOLE) relate the maximum EITC a family could receive during a child's teens to adult outcomes at
18-27 in the PSID. With the PSID to 2023 the same exposure can be scored at 25-29 and again at 35-39 and 40-44: does
its relation to sons' earnings grow or fade with age?

EXPOSURE (intent to treat, as Bastian and Michelmore): over the son's income years at ages 13-18,
  sum of [federal maximum credit for the family's number of children (1, 2, 3+; 0 -> no credit) x (1 + the state EITC
  rate as a share of the federal credit)], in thousands of 2000 dollars.
  Federal maxima: 61.PolicySchedules.py's EITC table (1984-2023; CRS RL31768 / R44825, IRS); 1975-78 $400 and 1979-83
  $500 (the same sources; policy_calendar.csv's eitc_max1 agrees from 1980). State rates: data/policy_calendar.csv
  (UKCPR, 1980+; 0 before a state's credit). Children = members aged under 18 of the son's family unit in the wave
  (psid_person_year); state = the family's state in the wave (18's husband_shocks_fam, 1976+; no state credit existed
  before 1986, so earlier waves need no state). Deflator: common.CPI.
  The variation is the federal schedule by year and number of children (differentiated from 1991, large 1993-96) and
  the state credits; birth-year FE, state-at-17 FE and number-of-children FE (the window's modal count) absorb the
  levels.
SAMPLE: 75's sons (R75.build(): PSID sons 25-55 with parental income at 13-19), window years 1975 and later (born 1962+),
  PSID weights. Outcomes: ln earnings (valid years) and employment (hours > 0).
DESIGN: (1) by band: the outcome on exposure, the fixed effects and single-age dummies, clustered by 1968 family; the
  change 40-44 minus 25-29 from one stacked regression (every regressor x band); (2) within son: exposure x (age-40)/10
  with son FE, birth-year and children FE x age, single-age dummies; (3) the same in sons whose mother had at most 12
  years of schooling (the families the credit reaches). lyp is not controlled in the main rows; a check adds it, and
  that is the column to report: the credit is NOT in PSID family income (pre-tax money income), so lyp is not a
  mediator of it (committee memo Z5, 2026-10-24).
Writes output/eitc_by_age.md / .json (aggregates only). DESCRIPTIVE.
"""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import CPI, DATA, OUT  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R75 = _load("s75", "75.WhatIsPassedOn.py")
R61 = _load("s61", "61.PolicySchedules.py")
R72, R73 = R75.R72, R75.R74.R73
BL = ["25-29", "30-34", "35-39", "40-44", "45-49", "50-55"]
RES = {}


def stars(p):
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""


def c(t):
    b, s = t
    p = 2 * stats.norm.sf(abs(b / s)) if s > 0 else np.nan
    return f"{b:.4f}{stars(p)} ({s:.4f}; p={'<0.001' if p < 0.001 else f'{p:.3f}'})"


def dummies(s):
    return pd.get_dummies(pd.Series(s).astype(int), drop_first=True).to_numpy(float)


def fed_max(year, n):
    if n <= 0:
        return 0.0
    if year < 1975:
        return 0.0
    if year < 1979:
        return 400.0
    if year < 1984:
        return 500.0
    return float(R61.EITC[min(year, max(R61.EITC))][min(n, 3)][1])


def exposure(r):
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    kids = py[py["age"].between(0, 17)].groupby(["wave", "int"]).size().rename("nk").reset_index()
    st = pd.read_pickle(DATA / "husband_shocks_fam.pkl")[["wave", "int", "fips"]].drop_duplicates(["wave", "int"])
    pc = pd.read_csv(DATA / "policy_calendar.csv", usecols=["state_fips", "year", "state_eitc_rate"]).rename(
        columns={"state_fips": "fips"})
    sons = r.drop_duplicates("pid")[["pid", "birth_year"]]
    k = py[py["child"] & py["pid"].isin(sons["pid"])][["pid", "wave", "int", "age"]]
    k = k[k["age"].between(14, 19)]                     # wave-ages 14-19 = income years at 13-18
    k["year"] = k["wave"] - 1
    k = k.merge(kids, on=["wave", "int"], how="left").merge(st, on=["wave", "int"], how="left")
    k = k.merge(pc, on=["fips", "year"], how="left")
    k["state_eitc_rate"] = k["state_eitc_rate"].fillna(0.0)
    k["nk"] = k["nk"].fillna(1).clip(upper=3).astype(int)
    k["fmax"] = [fed_max(int(y), int(n)) for y, n in zip(k["year"], k["nk"])]
    k["defl"] = [CPI[2000] / CPI[int(y)] if int(y) in CPI else np.nan for y in k["year"]]
    k["emax"] = k["fmax"] * (1 + k["state_eitc_rate"]) * k["defl"] / 1000
    g = k.groupby("pid")
    out = pd.DataFrame({"eitc": g["emax"].sum() * 6 / g["emax"].count(),        # scaled to six years
                        "eitc_n": g.size(), "nk_mode": g["nk"].agg(lambda s: s.mode().iat[0]),
                        "win0": g["year"].min()})
    return out[(out["eitc_n"] >= 3)].reset_index()


def ols(X, y, w, g, absorb=None):
    if absorb is not None:
        M = R73.demean(np.column_stack([y, X]), absorb, w)
        y, X = M[:, 0], M[:, 1:]
    Xw = X * w[:, None]
    XtXi = np.linalg.pinv(X.T @ Xw)
    b = XtXi @ Xw.T @ y
    u = y - X @ b
    S = pd.DataFrame(Xw * u[:, None]).groupby(g).sum().to_numpy()
    G, (n, k) = S.shape[0], X.shape
    V = XtXi @ (S.T @ S) @ XtXi * G / (G - 1) * (n - 1) / (n - k)
    return b, V


def block(md, d, y, lab, ctrl=()):
    md += [f"### {lab}", "", "| | " + " | ".join(BL[:4]) + " | change 40-44 - 25-29 | within son x age | sons |",
           "|---" * 8 + "|"]
    fe = lambda q: [dummies(q["birth_year"]), dummies(q["st17"]), dummies(q["nk_mode"]), dummies(q["age"])]  # noqa: E731
    cells = []
    for k in range(4):
        q = d[d["band"] == k]
        X = np.column_stack([q[["eitc"] + list(ctrl)].to_numpy(float)] + fe(q) + [np.ones(len(q))])
        b, V = ols(X, q[y].to_numpy(float), q["wt"].to_numpy(float), q["fam68"].to_numpy())
        cells.append((b[0], np.sqrt(V[0, 0])))
    s = d[d["band"].isin([0, 3])]
    b3 = (s["band"] == 3).to_numpy(float)
    base = np.column_stack([s[["eitc"] + list(ctrl)].to_numpy(float)] + fe(s) + [np.ones(len(s))])
    b, V = ols(np.column_stack([base, base * b3[:, None]]), s[y].to_numpy(float), s["wt"].to_numpy(float),
               s["fam68"].to_numpy())
    K = base.shape[1]
    ch = (b[K], np.sqrt(V[K, K]))
    a = d["agec"].to_numpy()[:, None]
    Xf = np.column_stack([d[["eitc"] + list(ctrl)].to_numpy(float) * a, dummies(d["birth_year"]) * a,
                          dummies(d["nk_mode"]) * a, dummies(d["age"])])
    bf, Vf = ols(Xf, d[y].to_numpy(float), d["wt"].to_numpy(float), d["fam68"].to_numpy(), absorb=d["pid"].to_numpy())
    fe_ = (bf[0], np.sqrt(Vf[0, 0]))
    md.append(f"| exposure (1,000 2000 $ over 13-18) | " + " | ".join(c(x) for x in cells) + f" | {c(ch)} | {c(fe_)} | "
              f"{d['pid'].nunique():,} |")
    md.append("")
    RES[lab] = {"bands": [list(map(float, x)) for x in cells], "change": list(map(float, ch)),
                "fe": list(map(float, fe_)), "sons": int(d["pid"].nunique())}


def main():
    r = R75.build()
    r = r.merge(exposure(r), on="pid", how="inner")
    r = r[r["win0"] >= 1975].copy()
    r = R72.state17(r)
    r["st17"] = r["fips17"].fillna(-1).astype(int)
    r["agec"] = (r["age"] - 40) / 10
    one = r.drop_duplicates("pid")
    md = ["# The EITC in childhood re-scored by the son's age (Fable F)", "",
          "Built by `101.EITCByAge.py` (2026-10-20); design in its docstring. PSID sons whose income years at 13-18 fall in "
          "1975+; exposure = maximum federal + state EITC for the family's number of children, summed over 13-18 "
          "(thousands of 2000 dollars); birth-year, state-at-17 and number-of-children FE, single-age dummies; PSID "
          "weights; s.e. clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1. **Intent to treat; descriptive.**",
          "", f"Sons {len(one):,} (born {int(one['birth_year'].min())}-{int(one['birth_year'].max())}); exposure mean "
          f"{np.average(one['eitc'], weights=one['wt']):.2f} (s.d. {one['eitc'].std():.2f}); by birth cohort: "
          + "; ".join(f"{b}-{b + 4} {np.average(q['eitc'], weights=q['wt']):.2f}"
                      for b, q in one.groupby(one['birth_year'] // 5 * 5)) + ".", ""]
    v = r[r["lw"].notna()]
    e = r[r["emp"].notna()]
    low = lambda q: q[(q["nomo"] == 0) & (q["m_educ_na"] == 0) & (q["m_educ0"] <= 12)]  # noqa: E731
    md.append("## ln earnings")
    block(md, v, "ly", "ln earnings, all sons")
    block(md, v, "ly", "ln earnings, all sons, + ln parental income", ctrl=("lyp",))
    block(md, low(v), "ly", "ln earnings, mother with <= 12 years of schooling")
    md.append("## employment")
    block(md, e, "emp", "employed, all sons")
    block(md, low(e), "emp", "employed, mother with <= 12 years of schooling")
    (OUT / "eitc_by_age.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "eitc_by_age.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
