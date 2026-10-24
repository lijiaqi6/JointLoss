r"""Wealth transmission by the son's age: rank-rank of net worth, and gifts and inheritances (committee memo K2, 2026-10-24)

The paper's outcome is the son's labor earnings. A reader of wealth data asks two things: is there an age profile of
wealth transmission next to the earnings one, and do gifts and inheritances arrive when the son is 40-55? (The family-
income IGE's rise with age is the son's own earnings on the same son-years: 34.IncomeVsEarningsIGE.py Section 3a, own
earnings 0.276 -> 0.492 at 25-29 -> 40-44, spouse trend 0.008, other income -0.010.)
SONS: 80's sons (male children of the PSID families at 13-19; R80.build()), as head or wife of their own family unit at
  25-55 in a wealth wave (1984, 1989, 1994, 1999-2021), core longitudinal weight of the year.
MEASURES
  son's net worth   'IMP WEALTH W/ EQUITY' of his family unit (121's cache, 2000 dollars), percentile rank within
                    wave x birth year among the sons observed (ties averaged)
  son's earnings    his labor income in the same wave (head or wife labor income), same rank, zeros kept
  parents' wealth   121's mean parental net worth at the son's 12-20, rank within birth year (sons born about 1964+)
  parental income   rank of 80's ln parental income within birth year (all sons)
  gift/inheritance  W123 'received a gift or inheritance' (1999-2021; since the last interview, last 5 years in 1999):
                    receipt (LPM) and asinh of the summed value of up to three (2000 dollars, codes >= 9,999,997 out)
DESIGN: son-years, weighted; by band 25-29 ... 45-49 (and 50-55); rank-rank slopes with clusters by 1968 family; the
  linear trend over band midpoints from one stacked regression (slope x (mid - 40)/10); gifts at 25-34 / 35-44 / 45-55.
Writes output/wealth_transmission.md / .json (aggregates only); caches data/son_gifts.pkl (family-level).
DESCRIPTIVE.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import DATA, OUT, stars  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R121 = _load("s121", "121.WealthMeasures.py")
R80, R18 = R121.R80, R121.R18
CACHE = DATA / "son_gifts.pkl"
BANDS = [(25, 29), (30, 34), (35, 39), (40, 44), (45, 49), (50, 55)]
RES = {}


def c(t):
    if t is None or not np.isfinite(t[0]):
        return ""
    b, s = t[0], t[1]
    p = 2 * norm.sf(abs(b / s)) if s > 0 else np.nan
    return f"{b:.3f}{stars(p)} ({s:.3f}; p={'<0.001' if p < 0.001 else f'{p:.3f}'})"


def gifts():
    if CACHE.exists():
        return pd.read_pickle(CACHE)
    out = []
    for w in [x for x in R18.WEALTH_WAVES if x >= 1999]:
        do = next(f for f in (R18.FAM / f"fam{w}er").glob("*.do") if "formats" not in f.name)
        pos, labs = R18.layout(do)
        idv = labs[1][0]
        rec = next(v for v, l in labs if re.match(r"W123 WTR (RECD )?GIFT/INHERITANCE", l))
        vals = [v for v, l in labs if re.match(r"W125 VALUE GIFT/INHERIT", l)][:3]
        f = R18.read(do.with_suffix(".txt"), [idv, rec] + vals, pos)
        x = pd.DataFrame({"wave": w, "int": f[idv]})
        r_ = pd.to_numeric(f[rec], errors="coerce")
        x["gift"] = (r_ == 1).astype(float).where(r_.isin([1, 5]))
        V = sum(pd.to_numeric(f[v], errors="coerce").where(lambda s: s.between(1, 9_999_996), 0.0) for v in vals)
        x["gift_val"] = R18.to2000(V, w).where(x["gift"].notna())
        x.loc[x["gift"] == 0, "gift_val"] = 0.0
        print(f"  {w}: {rec}, values {vals}; received {x['gift'].mean():.3f}", flush=True)
        out.append(x)
    G = pd.concat(out, ignore_index=True)
    G.to_pickle(CACHE)
    return G


def wls(d, y, x, extra=()):
    d = d.dropna(subset=[y, x, "wt", "fam68", *extra])
    d = d[d["wt"] > 0]
    X = sm.add_constant(d[[x, *extra]].astype(float))
    r = sm.WLS(d[y].astype(float), X, weights=d["wt"]).fit(cov_type="cluster",
                                                          cov_kwds={"groups": pd.factorize(d["fam68"])[0]})
    return (float(r.params[x]), float(r.bse[x])), len(d), int(d["pid"].nunique())


def main():
    r, _, _ = R80.build()
    sons = r.drop_duplicates("pid")[["pid", "birth_year", "fam68", "lyp"]].copy()
    sons["inc_rank"] = sons.groupby("birth_year")["lyp"].rank(pct=True)
    C = R121.components()
    pw = R121.son_means(r, C)[["pid", "total"]].rename(columns={"total": "pnw"})
    sons = sons.merge(pw, on="pid", how="left")
    sons["pw_rank"] = sons.groupby("birth_year")["pnw"].rank(pct=True)
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    y = py[(py["head"] | py["wife"]) & py["pid"].isin(sons["pid"]) & py["age"].between(25, 55)
           & py["wave"].isin(R18.WEALTH_WAVES)][["pid", "wave", "int", "age", "wt", "head", "hlab", "wlab"]]
    y = y.merge(C[["wave", "int", "total"]], on=["wave", "int"], how="inner").merge(gifts(), on=["wave", "int"],
                                                                                    how="left")
    y = y.merge(sons.drop(columns=["lyp"]), on="pid", how="left")
    y["earn_own"] = np.where(y["head"], y["hlab"], y["wlab"])
    y["nw_rank"] = y.groupby(["wave", "birth_year"])["total"].rank(pct=True)
    y["er_rank"] = y.groupby(["wave", "birth_year"])["earn_own"].rank(pct=True)
    y["band"] = pd.cut(y["age"], [24, 29, 34, 39, 44, 49, 55], labels=False)
    y["gift_asinh"] = np.arcsinh(y["gift_val"] / 1000)
    md = ["# Wealth transmission by the son's age (committee memo K2)", "",
          "Built by `122.WealthTransmission.py` (2026-10-24); design in its docstring. Weighted son-years; s.e. "
          "clustered by 1968 family. *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**", "",
          f"Son-years in wealth waves {len(y):,} of {y['pid'].nunique():,} sons; with parents' wealth "
          f"{int(y['pw_rank'].notna().sum()):,} of {int(y.loc[y['pw_rank'].notna(), 'pid'].nunique()):,} sons.", "",
          "## 1. Rank-rank slopes by the son's age", "",
          "| son's age | son's net worth on parents' wealth | son's earnings on parents' wealth (same son-years) | "
          "son's net worth on parental income (all sons) | son's earnings on parental income (all sons) | "
          "son-years (wealth / all) |", "|---|---|---|---|---|---|"]
    for k, (lo, hi) in enumerate(BANDS):
        q = y[y["band"] == k]
        qw = q.dropna(subset=["pw_rank"])
        a, n1, s1 = wls(qw, "nw_rank", "pw_rank") if len(qw) > 200 else ((np.nan, np.nan), 0, 0)
        b, _, _ = wls(qw, "er_rank", "pw_rank") if len(qw) > 200 else ((np.nan, np.nan), 0, 0)
        e, n2, s2 = wls(q, "nw_rank", "inc_rank")
        f, _, _ = wls(q, "er_rank", "inc_rank")
        md.append(f"| {lo}-{hi} | {c(a)} | {c(b)} | {c(e)} | {c(f)} | {n1:,} ({s1:,}) / {n2:,} ({s2:,}) |")
        RES[f"rr|{lo}-{hi}"] = {"nw_pw": list(a), "er_pw": list(b), "nw_inc": list(e), "er_inc": list(f),
                                "n_w": n1, "n": n2}
    # trend over bands: slope x (mid - 40)/10, band intercepts
    md += ["", "Linear trend of the slope per ten years of age (one stacked regression, band intercepts):", ""]
    for lab, q, yv, xv in (("net worth on parents' wealth", y.dropna(subset=["pw_rank"]), "nw_rank", "pw_rank"),
                           ("earnings on parents' wealth", y.dropna(subset=["pw_rank"]), "er_rank", "pw_rank"),
                           ("net worth on parental income", y, "nw_rank", "inc_rank"),
                           ("earnings on parental income", y, "er_rank", "inc_rank")):
        q = q.dropna(subset=["band"]).copy()
        mid = q["band"].map({k: (lo + hi) / 2 for k, (lo, hi) in enumerate(BANDS)})
        q["xt"] = q[xv] * (mid - 40) / 10
        bd = pd.get_dummies(q["band"], prefix="b", drop_first=True).astype(float)
        q = pd.concat([q, bd], axis=1)
        t, n, s = wls(q, yv, "xt", [xv] + list(bd.columns))
        md.append(f"- {lab}: {c(t)} ({n:,} son-years)")
        RES[f"trend|{lab}"] = list(t)
    # 2. gifts and inheritances
    md += ["", "## 2. Gifts and inheritances received by the son's family (1999-2021)", "",
           "| son's age | received (mean) | received on parents' wealth rank | asinh value on parents' wealth rank | "
           "received on parental income rank | son-years |", "|---|---|---|---|---|---|"]
    gy = y.dropna(subset=["gift"])
    for lo, hi in ((25, 34), (35, 44), (45, 55)):
        q = gy[gy["age"].between(lo, hi)]
        qw = q.dropna(subset=["pw_rank"])
        a, n1, _ = wls(qw, "gift", "pw_rank") if len(qw) > 200 else ((np.nan, np.nan), 0, 0)
        b, _, _ = wls(qw, "gift_asinh", "pw_rank") if len(qw) > 200 else ((np.nan, np.nan), 0, 0)
        e, n2, _ = wls(q, "gift", "inc_rank")
        mu = float(np.average(q["gift"], weights=q["wt"].clip(lower=1e-9)))
        md.append(f"| {lo}-{hi} | {mu:.3f} | {c(a)} | {c(b)} | {c(e)} | {n1:,} / {n2:,} |")
        RES[f"gift|{lo}-{hi}"] = {"mean": mu, "rec_pw": list(a), "val_pw": list(b), "rec_inc": list(e)}
    md.append("")
    (OUT / "wealth_transmission.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "wealth_transmission.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
