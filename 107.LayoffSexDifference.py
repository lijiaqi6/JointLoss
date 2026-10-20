r"""Sons and daughters: is the difference in what a father's childhood layoff does to them significant? (PI: make the
daughters a headline, 2026-10-20)

92 / 105: in one reduced specification a father's teen layoff lowers his son's wage profile and raises his daughter's.
A headline needs the difference tested directly. Sons and daughters of 24's children are stacked (the same reduced
specification as 92: ln parental income and the father's teen-window ln wage, ln hours, unemployment, zero-hours and
volatility measures, closure and layoff shares; single-age dummies; PSID weights; father present), every regressor and
age dummy interacted with daughter, s.e. clustered by 1968 family (sons and daughters of one family are one cluster).
  band: the layoff coefficient at 25-29 and 45-49 for each sex and the difference in the change (stacked bands, every
        regressor x band x sex);
  within person: person FE, every regressor x (age-40)/10 x sex; the difference of the layoff slopes.
Outcomes ln hourly wage and ln earnings (valid years). Layoff share (a) as in 75 / 92 and (b) 103's one job-end net in
every wave. Also the sexes' slopes by birth cohort (born before 1963 / 1963-75 / 1976+) under (a).
Writes output/layoff_sex_difference.md / .json (aggregates only). DESCRIPTIVE.
"""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import OUT  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R92 = _load("s92", "92.LayoffDaughters.py")
R103 = _load("s103", "103.LayoffCohortRegime.py")
R24 = R92.R24
c, dummies, ols_cl = R92.c, R92.dummies, R92.ols_cl
RES = {}


def frame(a, py, ch):
    ch = ch.drop(columns=[x for x in ("f_sh_close", "f_sh_layoff") if x in ch]).join(R92.layoff_shares(ch, py, a))
    wt = a[["pid", "wave", "wt"]].drop_duplicates(["pid", "wave"])
    parts = []
    for female in (0, 1):
        r, _ = R24.frames(a, ch, female)
        r = r.drop(columns=[x for x in ("f_sh_close", "f_sh_layoff") if x in r]).join(ch[["f_sh_close", "f_sh_layoff"]], on="pid")
        r = r.merge(wt, on=["pid", "wave"], how="left")
        r = r[(r["wt"] > 0) & r["fpid"].notna() & (r["f_n"] >= 3)].copy()
        r["female"] = float(female)
        parts.append(r)
    r = pd.concat(parts, ignore_index=True)
    b = R103.shares_b(r.drop_duplicates("pid")[["pid", "fpid"]])
    r = r.merge(b[["pid", "f_sh_layoff_b", "f_sh_close_b"]], on="pid", how="left")
    r["f_sh_layoff_b"] = r["f_sh_layoff_b"].fillna(0.0)
    r["f_sh_close_b"] = r["f_sh_close_b"].fillna(0.0)
    r["band"] = pd.cut(r["age"], [24, 29, 34, 39, 44, 49, 55], labels=False)
    r["agec"] = (r["age"] - 40) / 10
    r["cohort"] = np.select([r["birth_year"] < 1963, r["birth_year"] <= 1975], [0, 1], 2)
    return r


def lincom(b, V, w):
    w = np.asarray(w, float)
    return float(w @ b), float(np.sqrt(w @ V @ w))


def estimates(r, y, lay, clo):
    X0 = ["lyp", "f_lw", "f_lh", "f_sh_unemp", "f_sh_zero", "f_vtr", clo, lay]
    kL = X0.index(lay)
    d = r.dropna(subset=[y] + X0)
    out = {}
    # band: stacked 25-29 / 45-49, every regressor x band x sex
    s = d[d["band"].isin([0, 4])]
    b4 = (s["band"] == 4).to_numpy(float)
    fe = s["female"].to_numpy(float)
    base = np.column_stack([s[X0].to_numpy(float), dummies(s["age"]), np.ones(len(s))])
    K = base.shape[1]
    X = np.column_stack([base, base * b4[:, None], base * fe[:, None], base * (b4 * fe)[:, None]])
    bb, V = ols_cl(X, s[y].to_numpy(float), s["wt"].to_numpy(float), s["fam68"].to_numpy())
    e = np.zeros(len(bb))
    for name, idx in (("son_change", [K + kL]), ("daughter_change", [K + kL, 3 * K + kL]), ("difference", [3 * K + kL])):
        w = e.copy()
        w[idx] = 1
        out[name] = lincom(bb, V, w)
    # within person: every regressor x age x sex
    a_ = d["agec"].to_numpy()[:, None]
    fd = d["female"].to_numpy()[:, None]
    Xw = np.column_stack([d[X0].to_numpy(float) * a_, d[X0].to_numpy(float) * a_ * fd, dummies(d["age"]),
                          dummies(d["age"]) * fd])
    bf, Vf = ols_cl(Xw, d[y].to_numpy(float), d["wt"].to_numpy(float), d["fam68"].to_numpy(), absorb=d["pid"].to_numpy())
    n0 = len(X0)
    e = np.zeros(len(bf))
    for name, idx in (("son_fe", [kL]), ("daughter_fe", [kL, n0 + kL]), ("difference_fe", [n0 + kL])):
        w = e.copy()
        w[idx] = 1
        out[name] = lincom(bf, Vf, w)
    out["n"] = {"sons": int(d.loc[d["female"] == 0, "pid"].nunique()), "daughters": int(d.loc[d["female"] == 1, "pid"].nunique())}
    return out


def main():
    a, py, ch = R24.load()
    r = frame(a, py, ch)
    md = ["# Sons and daughters: the difference in what a father's childhood layoff does (PSID)", "",
          "Built by `107.LayoffSexDifference.py` (2026-10-20); design in its docstring. Sons and daughters stacked, every "
          "regressor interacted with daughter; clustered by 1968 family; per unit teen layoff share. *** p<0.01, ** p<0.05, "
          "* p<0.1. **Descriptive.**", "",
          "| layoff share | outcome | sons: change 45-49 - 25-29 | daughters: change | daughters - sons | sons: within "
          "person x age | daughters: within person x age | daughters - sons (within) | sons / daughters |",
          "|---" * 9 + "|"]
    for defn, lay, clo in (("(a) as in 75", "f_sh_layoff", "f_sh_close"), ("(b) one net in every wave", "f_sh_layoff_b",
                                                                           "f_sh_close_b")):
        for y, ylab in (("lw", "ln hourly wage"), ("ly", "ln earnings")):
            o = estimates(r, y, lay, clo)
            md.append(f"| {defn} | {ylab} | {c(o['son_change'])} | {c(o['daughter_change'])} | {c(o['difference'])} | "
                      f"{c(o['son_fe'])} | {c(o['daughter_fe'])} | {c(o['difference_fe'])} | {o['n']['sons']:,} / "
                      f"{o['n']['daughters']:,} |")
            RES[f"{defn}|{y}"] = {k: (list(v) if isinstance(v, tuple) else v) for k, v in o.items()}
    md += ["", "## By birth cohort, layoff share (a), ln hourly wage, within person", "",
           "| cohort | sons | daughters | daughters - sons |", "|---|---|---|---|"]
    for k, lab in ((0, "born < 1963"), (1, "born 1963-75"), (2, "born 1976+")):
        o = estimates(r[r["cohort"] == k], "lw", "f_sh_layoff", "f_sh_close")
        md.append(f"| {lab} | {c(o['son_fe'])} | {c(o['daughter_fe'])} | {c(o['difference_fe'])} |")
        RES[f"cohort|{lab}"] = {k2: list(o[k2]) for k2 in ("son_fe", "daughter_fe", "difference_fe")}
    md.append("")
    (OUT / "layoff_sex_difference.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "layoff_sex_difference.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
