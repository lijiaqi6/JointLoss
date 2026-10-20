r"""Replication of Rauh and Valladares-Esteban (2023, RED 51), Table 2 and Table B.1, on the NLSY79 (2026-10-19).

Their claim: within AFQT deciles 1-5 the Black dummy and Black x experience are insignificant in a regression of hourly
earnings on race and accumulated experience, so accumulation is race-neutral given the AFQT; deciles 6-10 show negative
Black x experience but are set aside for small cells (308 Black men in their sample). This script reruns the regression
(i) on the cross-sectional sample (their likely sample) and (ii) adding the supplemental Black sample, and adds a pooled
within-decile estimate (decile effects and decile x experience, one Black x experience slope) that has the power the
decile cells lack.

DATA (read only): Dropbox/NLS/nlsy79_all_1979-2022.csv, one read of the columns below, cached in
data/rauh_nlsy79.pkl (git-ignored: person-level).
SAMPLE (their Section 2): men, non-Hispanic Black or White (SAMPLE_RACE), born in the US (FAM-2A = 1), calendar years
1978-2021, ages 23-54, not enrolled in school or college on 1 May of the year (ENROLLMTREV of that year, else of the
interview year). Cross-sectional sample ids 1-3 (male White, male White poor, male Black); full adds 10 (supplemental
male Black). Employed: >= 500 hours and >= 25 weeks in the calendar year (WKSWK-PCY, HRSWK-PCY).
HOURLY EARNINGS: wage and salary income of the calendar year (Q13-5, Q13-5_TRUNC_REVISED from 1982) / annual hours,
2018 dollars (CPI-U), kept between $1 and $500.
EXPERIENCE: weeks worked accumulated from 1 January 1978 to the start of the year, / 52. Weeks per calendar year: the
PCY report when the year is a report year; in the unreported years of the biennial survey (1994-2020 even years), weeks
since the last interview minus the PCY weeks, clipped to [0, 52]. (They use the weekly arrays; the two agree up to the
weeks between interviews.)
AFQT: AFQT-3 (revised 2006 percentile, 1980 ASVAB), standardised within birth year on 1979 weights over civilian
respondents of both sexes (as in 36.SameEmployerGrowthChecks.py; they use Altonji et al. 2012); deciles across the Black
and White men of the cross-sectional sample, 1979 weights; the same cut-offs for the full sample.
REGRESSION: OLS, hourly earnings on Black, experience, experience x Black, constant, region (4) fixed effects; robust
(HC1, theirs) and person-clustered standard errors. Also log hourly earnings.
Writes output/rauh_replication.md and .json.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import CPI, DATA, OUT  # noqa: E402
import os
DROPBOX = Path(os.environ.get("DROPBOX", Path.home() / "Dropbox"))   # raw data, read only

NLS = Path(DROPBOX / "NLS/nlsy79_all_1979-2022")
CACHE = DATA / "rauh_nlsy79.pkl"
BASE = {"R0000100": "pid", "R0173600": "sample_id", "R0214800": "sex", "R0000500": "birth_year",
        "R0216100": "wt79", "R0214700": "sample_race", "R0000700": "born_us"}
FAMS = {"WKSWK-PCY": "wk", "WKSWK-SLI": "sli", "HRSWK-PCY": "hrs", "Q13-5": "earn0", "Q13-5_TRUNC_REVISED": "earn1",
        "REGION": "region"}


def extract():
    if CACHE.exists():
        return pd.read_pickle(CACHE)
    ix = pd.read_csv(DATA / "nlsy79_codebook.csv")
    q = ix["qname"].astype(str)
    sel = ix[q.isin(FAMS) | q.str.match(r"^ENROLLMTREV\d\d$") | (q == "AFQT-3")].copy()
    cols = list(dict.fromkeys(list(BASE) + sel["col"].tolist()))
    print(f"NLSY79: reading {len(cols)} columns from the full release (slow) ...", flush=True)
    d = pd.read_csv(NLS / "nlsy79_all_1979-2022.csv", usecols=cols)
    ren = dict(BASE)
    for c, qn, y in zip(sel["col"], sel["qname"], sel["year"]):
        if qn == "AFQT-3":
            ren[c] = "afqt3"
        elif qn.startswith("ENROLLMTREV"):
            ren[c] = f"enr|{int(qn[-2:]) + (1900 if int(qn[-2:]) > 50 else 2000)}"
        else:
            ren[c] = f"{FAMS[qn]}|{y}"
    d = d.rename(columns=ren)
    d.to_pickle(CACHE)
    return d


def build(X):
    X = X.copy()
    for c in X.columns:
        if c != "pid":
            X[c] = pd.to_numeric(X[c], errors="coerce")
            if c not in ("wt79",):
                X.loc[X[c] < 0, c] = np.nan
    k = X[["pid", "sample_id", "sex", "birth_year", "wt79", "sample_race", "born_us", "afqt3"]].copy()
    # AFQT, standardised within birth year (civilians, both sexes, 1979 weights)
    k["afqt_pct"] = k["afqt3"] / 1000
    k["afqt"] = np.nan
    civ = k["sample_id"].between(1, 14) & k["afqt_pct"].notna() & (k["wt79"] > 0)
    for by, z in k[civ].groupby("birth_year"):
        mu = np.average(z["afqt_pct"], weights=z["wt79"])
        sd = np.sqrt(np.average((z["afqt_pct"] - mu) ** 2, weights=z["wt79"]))
        ii = k.index[(k["birth_year"] == by) & k["afqt_pct"].notna()]
        k.loc[ii, "afqt"] = (k.loc[ii, "afqt_pct"] - mu) / sd
    # calendar-year panel: report year y gives calendar year y - 1
    years = sorted({int(c.split("|")[1]) for c in X.columns if c.startswith("wk|")})
    rows = []
    for y in years:
        c = y - 1
        nan = pd.Series(np.nan, index=X.index)
        earn = X.get(f"earn1|{y}", nan).fillna(X.get(f"earn0|{y}", nan))
        enr = X.get(f"enr|{c}", nan).fillna(X.get(f"enr|{y}", nan))
        rows.append(pd.DataFrame({"pid": X["pid"], "cal": c, "wk": X[f"wk|{y}"], "sli": X.get(f"sli|{y}", nan),
                                  "hrs": X.get(f"hrs|{y}", nan), "earn": earn, "region": X.get(f"region|{y}", nan),
                                  "enr": enr}))
    P = pd.concat(rows, ignore_index=True)
    # weeks per calendar year 1978-2021, imputing the unreported years of the biennial survey
    W = P.pivot(index="pid", columns="cal", values="wk").reindex(columns=range(1978, 2022))
    S = P.pivot(index="pid", columns="cal", values="sli").reindex(columns=range(1978, 2022))
    for c in range(1978, 2022):
        if c not in set(P["cal"]):                                  # unreported year c: next report covers c + 1
            if c + 1 in S.columns:
                W[c] = (S[c + 1] - W[c + 1]).clip(0, 52)
    exp_start = W.fillna(0).cumsum(axis=1).shift(1, axis=1).fillna(0) / 52   # years worked before the year
    E = exp_start.stack().rename("exper").reset_index().rename(columns={"level_1": "cal"})
    P = P.merge(E, on=["pid", "cal"], how="left").merge(k, on="pid")
    P["age"] = P["cal"] - (1900 + P["birth_year"])
    P["black"] = (P["sample_race"] == 2).astype(int)
    P["hourly"] = P["earn"] / P["hrs"] * CPI[2018] / P["cal"].map(CPI)
    return P, k


def ols(d, y, xs, fe, cl):
    Z = pd.get_dummies(d[fe].astype(int), prefix=fe, drop_first=True).astype(float) if fe else pd.DataFrame(index=d.index)
    Xm = np.column_stack([d[xs].to_numpy(float), Z.to_numpy(float), np.ones(len(d))])
    yv = d[y].to_numpy(float)
    XtXi = np.linalg.pinv(Xm.T @ Xm)
    b = XtXi @ Xm.T @ yv
    u = yv - Xm @ b
    n, kk = Xm.shape
    hc1 = XtXi @ (Xm.T * u ** 2) @ Xm @ XtXi * n / (n - kk)
    S = pd.DataFrame(u[:, None] * Xm).groupby(d[cl].to_numpy()).sum().to_numpy()
    G = S.shape[0]
    clu = XtXi @ (S.T @ S) @ XtXi * G / (G - 1) * (n - 1) / (n - kk)
    out = {}
    for i, x in enumerate(xs + ["const"]):
        j = i if x != "const" else kk - 1
        out[x] = {"b": float(b[j]), "se_hc1": float(np.sqrt(hc1[j, j])), "se_cl": float(np.sqrt(clu[j, j]))}
        for s in ("hc1", "cl"):
            out[x][f"p_{s}"] = float(2 * (1 - norm.cdf(abs(b[j]) / out[x][f"se_{s}"])))
    out["_n"] = int(n)
    out["_mean"] = float(np.mean(yv))
    out["_share_black"] = float(d["black"].mean())
    out["_n_black_men"] = int(d.loc[d["black"] == 1, "pid"].nunique())
    return out


def star(p):
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""


if __name__ == "__main__":
    P, k = build(extract())
    men = (P["sex"] == 1) & P["sample_race"].isin([2, 3]) & (P["born_us"] == 1)
    base = men & P["age"].between(23, 54) & ~P["enr"].isin([2, 3])
    emp = (P["hrs"] >= 500) & (P["wk"] >= 25) & P["hourly"].between(1, 500) & P["exper"].notna() & P["region"].notna()
    samples = {"cross": P["sample_id"].isin([1, 2, 3]), "full": P["sample_id"].isin([1, 2, 3, 10])}
    # AFQT deciles over the Black and White men of the cross-sectional sample, 1979 weights
    km = k[(k["sex"] == 1) & k["sample_race"].isin([2, 3]) & (k["born_us"] == 1) & k["sample_id"].isin([1, 2, 3])
           & k["afqt"].notna()].sort_values("afqt")
    cw = km["wt79"].cumsum() / km["wt79"].sum()
    cuts = [km["afqt"].to_numpy()[np.searchsorted(cw.to_numpy(), q)] for q in np.arange(0.1, 1.0, 0.1)]
    P["dec"] = np.where(P["afqt"].notna(), np.searchsorted(cuts, P["afqt"], side="right") + 1, np.nan)
    P["lhourly"] = np.log(P["hourly"])
    P["exb"] = P["exper"] * P["black"]
    res = {"cuts": [float(c) for c in cuts]}
    lines = ["# Rauh and Valladares-Esteban (2023) Table 2 / B.1 on the NLSY79", "",
             "Hourly earnings (2018 $) on Black, experience (years), experience x Black, region FE; OLS. Robust (HC1) "
             "s.e. as in the paper; person-clustered s.e. in brackets with its p-value. Code: `IGE/70.RauhReplication.py`.", ""]
    for sname, sm in samples.items():
        D = P[base & emp & sm & P["dec"].notna()].copy()
        nb = D.loc[D["black"] == 1, "pid"].nunique()
        nw = D.loc[D["black"] == 0, "pid"].nunique()
        lines += [f"## Sample: {sname} (sample ids {'1-3' if sname == 'cross' else '1-3, 10'}): {nb} Black men, "
                  f"{nw} White men, {len(D):,} person-years", ""]
        for yv in ("hourly", "lhourly"):
            R = {}
            for d_ in range(1, 11):
                z = D[D["dec"] == d_]
                if z["black"].sum() >= 2 and (1 - z["black"]).sum() >= 2:
                    R[str(d_)] = ols(z, yv, ["black", "exper", "exb"], "region", "pid")
            # pooled within decile: decile FE x experience, one Black and Black x experience
            for tag, lo, hi in (("pooled 1-5", 1, 5), ("pooled 6-10", 6, 10), ("pooled 1-10", 1, 10)):
                z = D[D["dec"].between(lo, hi)].copy()
                ds = [f"d{j}" for j in range(lo + 1, hi + 1)]
                for j in range(lo + 1, hi + 1):
                    z[f"d{j}"] = (z["dec"] == j).astype(float)
                    z[f"dx{j}"] = z[f"d{j}"] * z["exper"]
                R[tag] = ols(z, yv, ["black", "exper", "exb"] + ds + [f"dx{j}" for j in range(lo + 1, hi + 1)],
                             "region", "pid")
            res[f"{sname}|{yv}"] = R
            cols = list(R)
            lines += [f"### {'Hourly earnings, 2018 $' if yv == 'hourly' else 'Log hourly earnings'}", "",
                      "| | " + " | ".join(f"decile {c}" if c.isdigit() else c for c in cols) + " |",
                      "|---" * (len(cols) + 1) + "|"]
            for x, lab in (("black", "Black"), ("exper", "Experience (years)"), ("exb", "Experience x Black")):
                lines.append(f"| {lab} | " + " | ".join(
                    f"{R[c][x]['b']:.4f}{star(R[c][x]['p_hc1'])} ({R[c][x]['se_hc1']:.4f}) "
                    f"[{R[c][x]['se_cl']:.4f}, p={R[c][x]['p_cl']:.3f}]" for c in cols) + " |")
            for key, lab, f in (("_mean", "Mean", "{:.2f}"), ("_share_black", "Share Black (obs.)", "{:.3f}"),
                                ("_n_black_men", "Black men", "{:d}"), ("_n", "Observations", "{:,}")):
                lines.append(f"| {lab} | " + " | ".join(f.format(R[c][key]) for c in cols) + " |")
            lines.append("")
    (OUT / "rauh_replication.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    json.dump(res, open(OUT / "rauh_replication.json", "w"), indent=1)
    print("\n".join(lines))
