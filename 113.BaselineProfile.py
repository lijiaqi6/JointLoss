r"""The IGE age profile on the paper's baseline sample (simulated JPE round, Referee 1 point 2: one baseline sample).

Section 3 reported the profile on all sons with parental income (26.IGEByAge.py; 0.276 -> 0.484 at 45-49) and its
period checks on 33's frame at 25-49 (95.PooledRiseChecks.py; 0.283 -> 0.492), while every split, layoff and policy
estimate uses 75's baseline sample (4,770 sons with parental income over >= 3 of their ages 13-19; 0.276 -> 0.443).
This script puts the profile and its checks on the baseline sample:
  A  the IGE of ln earnings (valid years) and ln family income by band 25-29 ... 50-55: pooled (PSID weights), White,
     Black and White - Black; equality across bands, the linear trend per 10 years and the change 45-49 - 25-29;
  B  the pooled change 45-49 - 25-29 within birth cohorts (1951-64, 1965-79, 1980-89 to 40-44), with income-year fixed
     effects, and in a fixed window of income years 1990-2010.
Band regressions with single-age dummies (33's Cells: separate regressions per cell, joint cluster-robust covariance by
1968 family). Writes output/baseline_profile.md / .json (aggregates only).
"""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import OUT, stars  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R75 = _load("s75", "75.WhatIsPassedOn.py")
R33 = _load("s33", "33.AgeProfileRobustness.py")
BL = ["25-29", "30-34", "35-39", "40-44", "45-49", "50-55"]
RES = {}


def c(t):
    e, se, p = t
    return f"{e:.3f}{stars(p)} ({se:.3f}; p={'<0.001' if p < 0.001 else f'{p:.3f}'})"


def fit(d, y, ctrl=(), w="wt"):
    d = d.assign(_y=d[y], cellb=d["band"].map(dict(enumerate(BL))), agei=d["age"].round().astype(int))
    if w is None:
        d = d.assign(_w1=1.0)
        w = "_w1"
    return R33.Cells(d, "_y", "lyp", "cellb", list(ctrl), "agei", w=w)


def main():
    r = R75.build()
    r["iyear"] = (r["wave"] - 1).astype(int)
    md = ["# The IGE age profile on the baseline sample (one sample for the paper)", "",
          "Built by `113.BaselineProfile.py` (2026-10-24); design in its docstring. Estimate (s.e.; p) clustered by 1968 "
          "family; *** p<0.01, ** p<0.05, * p<0.1.", ""]
    for y, ylab, sub in (("ly", "ln earnings (valid years)", r["lw"].notna()), ("lfam", "ln family income", r["lfam"].notna())):
        d = r[sub & r[y].notna()]
        P = fit(d, y)
        Wf = fit(d[d.race == "White"], y, w=None)
        Bf = fit(d[d.race == "Black"], y, w=None)
        md += [f"## A. {ylab}", "", "| band | pooled (weighted) | White | Black | White - Black | sons (pooled) |",
               "|---|---|---|---|---|---|"]
        out = {}
        for b in BL:
            if not P.has(b):
                continue
            p = P.lin([(b, "x", 1)])
            w_ = Wf.lin([(b, "x", 1)]) if Wf.has(b) else None
            k_ = Bf.lin([(b, "x", 1)]) if Bf.has(b) else None
            gap = None
            if w_ and k_:
                e, s = w_[0] - k_[0], float(np.sqrt(w_[1] ** 2 + k_[1] ** 2))
                from scipy.stats import norm
                gap = (e, s, 2 * norm.sf(abs(e / s)))
            md.append(f"| {b} | {c(p)} | {c(w_) if w_ else ''} | {c(k_) if k_ else ''} | {c(gap) if gap else ''} | "
                      f"{P.info[b]['children']:,} |")
            out[b] = {"pooled": list(map(float, p)), "white": list(map(float, w_)) if w_ else None,
                      "black": list(map(float, k_)) if k_ else None, "gap": list(map(float, gap)) if gap else None,
                      "sons": int(P.info[b]["children"])}
        bands = [b for b in BL if P.has(b)]
        ch = P.lin([("45-49", "x", 1), ("25-29", "x", -1)])
        m = np.array([27.0, 32.0, 37.0, 42.0, 47.0, 52.5])[:len(bands)]
        wts = (m - m.mean()) / ((m - m.mean()) ** 2).sum() * 10
        tr = P.lin([(b, "x", wv) for b, wv in zip(bands, wts)])
        W = P.wald([[(bands[0], "x", 1), (b, "x", -1)] for b in bands[1:]])
        md += ["", f"Pooled: change 45-49 - 25-29 {c(ch)}; trend per 10 years {c(tr)}; equal in all bands "
               f"chi2({W[1]}) = {W[0]:.1f}, p = {W[2]:.4f}.", ""]
        out["change"], out["trend"], out["wald"] = list(map(float, ch)), list(map(float, tr)), list(map(float, W))
        RES[y] = out
    # B. cohorts and calendar time, ln earnings
    d = r[r["lw"].notna() & r["ly"].notna()]
    specs = [("baseline", d, ())]
    for lab, (lo, hi) in (("born 1951-64", (1951, 1964)), ("born 1965-79", (1965, 1979)), ("born 1980-89", (1980, 1989))):
        specs.append((lab, d[d["birth_year"].between(lo, hi)], ()))
    yd = pd.get_dummies(d["iyear"], prefix="yr", drop_first=True, dtype=float)
    specs.append(("income-year fixed effects", pd.concat([d, yd], axis=1), tuple(yd.columns)))
    specs.append(("income years 1990-2010 only", d[d["iyear"].between(1990, 2010)], ()))
    md += ["## B. The pooled change in ln earnings, by cohort and net of calendar time", "",
           "| specification | 25-29 | oldest band | change | sons |", "|---|---|---|---|---|"]
    for lab, q, ctrl in specs:
        P = fit(q, "ly", ctrl)
        hi = "45-49" if P.has("45-49") else "40-44"
        a, b = P.lin([("25-29", "x", 1)]), P.lin([(hi, "x", 1)])
        ch = P.lin([(hi, "x", 1), ("25-29", "x", -1)])
        md.append(f"| {lab} | {c(a)} | {c(b)} ({hi}) | {c(ch)} | {q['pid'].nunique():,} |")
        RES[f"B|{lab}"] = {"a": list(map(float, a)), "b": list(map(float, b)), "hi": hi, "change": list(map(float, ch))}
    md.append("")
    (OUT / "baseline_profile.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "baseline_profile.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
