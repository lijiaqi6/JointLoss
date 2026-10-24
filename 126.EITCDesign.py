r"""The EITC in childhood: first stage, the families it reaches, the 1993-96 expansion, daughters (committee memo H1,
2026-10-24)

101.EITCByAge.py relates the maximum EITC a family could receive over the son's 13-18 (intent to treat on all families)
to his earnings by age: -0.016* (p = 0.052) at 25-29, -0.003 at 40-44, within son +0.029***; nothing significant in
sons of mothers with <= 12 years of schooling. A reader who built these designs asks: is there a first stage (the
credit's first-order effect is on mothers' employment), do the effects sit in the families the credit reaches, does the
cleanest variation (the 1993-96 expansion for families with two or more children) give the same age profile, and what
about daughters?
PREDICTED ELIGIBILITY. A window year is eligible when the family's earned income (head + wife labor income, nominal)
  is positive and below the end of the phase-out for its number of children (61's schedule from 1984, joint filers when
  a father is present; 1975-78 $8,000, 1979-83 $10,000). Logit of eligibility on characteristics fixed before the
  window: ln mean family income at the son's 6-12, the mother's schooling, father present, number of children, year
  dummies. A son's predicted eligibility = mean predicted probability over his window years; 'likely eligible' = top
  tercile.
FIRST STAGE (son x window year, income years 1975+): mother employed (hours > 0), her annual hours, ln family earned
  income, on that year's maximum credit (1,000 2000 $), with year, state and number-of-children FE, unweighted; clusters 1968
  family; all and likely eligible. The variation left is the schedule by number of children and year and the state
  credits.
REDUCED FORM: 101's block (bands 25-29 ... 40-44, change 40-44 - 25-29, within son) in the likely-eligible tercile and
  the others, ln earnings with ln parental income held fixed.
1993-96 EXPANSION (Eissa-Hoynes / Hoynes-Patel): sons born 1970-1989; treat = two or more children (window mode);
  post = share of window income years in 1994 or later; outcome on treat x post with treat, birth-year and state-at-17
  FE and single-age dummies, by band; clusters 1968 family.
DAUGHTERS: 101's exposure and block on 107's daughters frame.
Writes output/eitc_design.md / .json (aggregates only). INTENT TO TREAT; DESCRIPTIVE.
"""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import CPI, DATA, OUT  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R101 = _load("s101", "101.EITCByAge.py")
R107 = _load("s107", "107.LayoffSexDifference.py")
R75, R61, R72 = R101.R75, R101.R61, R101.R72
R24 = R75.R24
c, ols, dummies = R101.c, R101.ols, R101.dummies
RES = {}


def phase_end(year, n, joint):
    if n <= 0:
        return 0.0
    if year < 1975:
        return 0.0
    if year < 1979:
        return 8000.0
    if year < 1984:
        return 10000.0
    r_in, mx, r_out, ps, psj = R61.EITC[min(year, max(R61.EITC))][min(n, 3)]
    return float((psj if joint else ps) + mx / r_out)


def window_years(r):
    """son x window income year (13-18): year, children, state, max credit, earned income, mother's hours."""
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    kids = py[py["age"].between(0, 17)].groupby(["wave", "int"]).size().rename("nk").reset_index()
    st = pd.read_pickle(DATA / "husband_shocks_fam.pkl")[["wave", "int", "fips"]].drop_duplicates(["wave", "int"])
    pc = pd.read_csv(DATA / "policy_calendar.csv", usecols=["state_fips", "year", "state_eitc_rate"]).rename(
        columns={"state_fips": "fips"})
    hh = py[py["head"]][["wave", "int", "hlab", "wlab"]].drop_duplicates(["wave", "int"])
    a = pd.read_pickle(R24.CACHE)
    wom = a[a["wife"] | (a["head"] & (a["female"] == 1))][["wave", "int", "hours"]].drop_duplicates(["wave", "int"])
    sons = r.drop_duplicates("pid")[["pid", "birth_year", "fam68", "nofa"]]
    k = py[py["child"] & py["pid"].isin(sons["pid"]) & py["age"].between(14, 19)][["pid", "wave", "int"]]
    k["year"] = k["wave"] - 1
    k = k.merge(kids, on=["wave", "int"], how="left").merge(st, on=["wave", "int"], how="left")
    k = k.merge(pc, on=["fips", "year"], how="left").merge(hh, on=["wave", "int"], how="left")
    k = k.merge(wom.rename(columns={"hours": "m_hours"}), on=["wave", "int"], how="left").merge(sons, on="pid")
    k = k[k["year"] >= 1975].copy()
    k["state_eitc_rate"] = k["state_eitc_rate"].fillna(0.0)
    k["nk"] = k["nk"].fillna(1).clip(upper=3).astype(int)
    k["defl"] = [CPI[2000] / CPI[int(y)] for y in k["year"]]
    k["emax"] = [R101.fed_max(int(y), int(n)) for y, n in zip(k["year"], k["nk"])] * (1 + k["state_eitc_rate"]) \
        * k["defl"] / 1000
    earn = (k["hlab"].fillna(0) + k["wlab"].fillna(0))                     # real 2000 $
    nom = earn / k["defl"]
    k["elig"] = ((nom > 0) & (nom < [phase_end(int(y), int(n), f == 0) for y, n, f in
                                     zip(k["year"], k["nk"], k["nofa"])])).astype(float)
    k["m_emp"] = (k["m_hours"] > 0).astype(float).where(k["m_hours"].notna())
    k["m_hrs"] = k["m_hours"]
    k["l_earn"] = np.log(earn.where(earn > 0))
    return k


def pre_income(r):
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    k = py[py["child"] & py["age"].between(7, 13) & py["faminc"].between(R24.LO, R24.HI) & py["pid"].isin(r["pid"])]
    g = k.groupby("pid")["faminc"]
    return np.log(g.mean().where(g.count() >= 2)).rename("lyp612")


def fs_reg(d, y):
    d = d.dropna(subset=[y, "emax", "fam68"])
    X = np.column_stack([d["emax"].to_numpy(float), dummies(d["year"]), dummies(d["fips"].fillna(-1)),
                         dummies(d["nk"]), np.ones(len(d))])
    b, V = ols(X, d[y].to_numpy(float), np.ones(len(d)), d["fam68"].to_numpy())
    return (b[0], float(np.sqrt(V[0, 0]))), len(d)


def did(d, y):
    out = {}
    for k in range(4):
        q = d[d["band"] == k].dropna(subset=[y])
        if q["pid"].nunique() < 150:
            continue
        X = np.column_stack([(q["treat"] * q["post"]).to_numpy(float), q["treat"].to_numpy(float), q["post"].to_numpy(float),
                             dummies(q["birth_year"]), dummies(q["st17"]), dummies(q["age"]), np.ones(len(q))])
        b, V = ols(X, q[y].to_numpy(float), q["wt"].to_numpy(float), q["fam68"].to_numpy())
        out[R101.BL[k]] = ((b[0], float(np.sqrt(V[0, 0]))), int(q["pid"].nunique()))
    return out


def main():
    r = R75.build()
    W = window_years(r)
    r = r.merge(pre_income(r), left_on="pid", right_index=True, how="left")
    # predicted eligibility
    one = r.drop_duplicates("pid")[["pid", "lyp612", "m_educ0", "m_educ_na", "nomo"]]
    W = W.merge(one, on="pid", how="left")
    Z = W.dropna(subset=["lyp612"]).copy()
    Z["m_ed"] = Z["m_educ0"].where(Z["m_educ_na"] == 0, Z["m_educ0"].mean())
    X = pd.concat([Z[["lyp612", "m_ed", "m_educ_na", "nofa"]].astype(float),
                   pd.get_dummies(Z["nk"], prefix="nk", drop_first=True, dtype=float),
                   pd.get_dummies(Z["year"], prefix="y", drop_first=True, dtype=float)], axis=1)
    lg = sm.Logit(Z["elig"], sm.add_constant(X)).fit(disp=0)
    Z["p_elig"] = lg.predict(sm.add_constant(X))
    pe = Z.groupby("pid")["p_elig"].mean().rename("pelig")
    W = W.merge(pe, on="pid", how="left")
    cut = pe.quantile(2 / 3)
    W["likely"] = (W["pelig"] >= cut).astype(float).where(W["pelig"].notna())
    md = ["# The EITC in childhood: first stage, eligibility, the 1993-96 expansion, daughters (committee memo H1)", "",
          "Built by `126.EITCDesign.py` (2026-10-24); design in its docstring. Exposure in thousands of 2000 dollars; "
          "s.e. clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1. **Intent to treat; descriptive.**", "",
          f"Window years 1975+: {len(W):,} (sons {W['pid'].nunique():,}); eligible (earned income in the credit's "
          f"range) {W['elig'].mean():.3f}; predicted eligibility: mean {pe.mean():.3f}, top-tercile cut {cut:.3f}; "
          f"eligible share in the top tercile {W.loc[W['likely'] == 1, 'elig'].mean():.3f} vs others "
          f"{W.loc[W['likely'] == 0, 'elig'].mean():.3f}; logit pseudo-R2 {lg.prsquared:.3f}.", "",
          "## 1. First stage: the mother's work and the family's earnings in the window year on that year's maximum credit",
          "", "| outcome | all window years | likely eligible | others |", "|---|---|---|---|"]
    for y, lab in (("m_emp", "mother employed"), ("m_hrs", "mother's annual hours"),
                   ("l_earn", "ln family earned income"), ("elig", "earned income in the credit's range")):
        cells = []
        for q in (W, W[W["likely"] == 1], W[W["likely"] == 0]):
            t, n = fs_reg(q, y)
            cells.append(f"{c(t)} [{n:,}]")
            RES[f"fs|{y}|{len(q)}"] = list(map(float, t))
        md.append(f"| {lab} | " + " | ".join(cells) + " |")
        print(md[-1], flush=True)
    md.append("")
    # reduced form by eligibility
    r = r.merge(R101.exposure(r), on="pid", how="inner")
    r = r[r["win0"] >= 1975].copy()
    r = R72.state17(r)
    r["st17"] = r["fips17"].fillna(-1).astype(int)
    r["agec"] = (r["age"] - 40) / 10
    r = r.merge(pe, on="pid", how="left")
    r["likely"] = (r["pelig"] >= cut).astype(float).where(r["pelig"].notna())
    v = r[r["lw"].notna()]
    md.append("## 2. Reduced form by predicted eligibility (ln earnings, ln parental income held fixed)")
    R101.block(md, v[v["likely"] == 1], "ly", "likely eligible (top tercile)", ctrl=("lyp",))
    R101.block(md, v[v["likely"] == 0], "ly", "others", ctrl=("lyp",))
    R101.block(md, r[(r["likely"] == 1) & r["emp"].notna()], "emp", "employed, likely eligible")
    # 1993-96 expansion
    d = r[r["birth_year"].between(1970, 1989)].copy()
    d["treat"] = (d["nk_mode"] >= 2).astype(float)
    wy = W.assign(post=(W["year"] >= 1994).astype(float)).groupby("pid")["post"].mean()
    d["post"] = d["pid"].map(wy)
    md += ["## 3. The 1993-96 expansion: two or more children vs one, by the share of the window from 1994", "",
           "| outcome | " + " | ".join(R101.BL[:4]) + " |", "|---|---|---|---|---|"]
    for y, lab, q in (("ly", "ln earnings", d[d["lw"].notna()]), ("emp", "employed", d[d["emp"].notna()])):
        o = did(q.dropna(subset=["post"]), y)
        md.append(f"| {lab} | " + " | ".join(f"{c(o[b][0])} [{o[b][1]:,}]" if b in o else "" for b in R101.BL[:4]) + " |")
        RES[f"did|{y}"] = {b: [list(map(float, o[b][0])), o[b][1]] for b in o}
        print(md[-1], flush=True)
    md.append("")
    # daughters
    a, py24, ch = R24.load()
    rr = R107.frame(a, py24, ch)
    dd = rr[rr["female"] == 1].copy()
    dd = dd.merge(R101.exposure(dd), on="pid", how="inner")
    dd = dd[dd["win0"] >= 1975].copy()
    dd = R72.state17(dd)
    dd["st17"] = dd["fips17"].fillna(-1).astype(int)
    md.append("## 4. Daughters (107's frame)")
    R101.block(md, dd[dd["lw"].notna()], "ly", "daughters, ln earnings", ctrl=("lyp",))
    R101.block(md, dd[dd["lw"].notna()], "lw", "daughters, ln hourly wage", ctrl=("lyp",))
    RES.update({f"rf|{k}": v_ for k, v_ in R101.RES.items()})
    (OUT / "eitc_design.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "eitc_design.json", "w"), indent=1, default=float)
    print("\n".join(md))


if __name__ == "__main__":
    main()
