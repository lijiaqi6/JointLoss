r"""The EITC eligibility contrast as one triple difference (committee re-read memo, action 9, 2026-10-24)

126: within the same son, exposure goes with faster earnings growth in the likely-eligible third (0.064***) than in the
others (0.017), estimated in separate samples; 129: the growth is as large in the top third of parental income, where
the credit barely reaches. Here the contrast is one regression: ln earnings on exposure x a, exposure x likely x a and
likely x a (a = (age-40)/10), with son FE, single-age dummies and number-of-children x birth-year cells x a (the
schedule's own variation absorbed except by state and year within cells), and the same with parental-income thirds in
place of likely eligibility.
Writes output/eitc_triple_diff.md / .json (aggregates only). INTENT TO TREAT; DESCRIPTIVE.
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


R129 = _load("s129", "129.EITCChecks.py")
R126, R101 = R129.R126, R129.R101
R75, R72 = R101.R75, R101.R72
c, ols, dummies = R101.c, R101.ols, R101.dummies
RES = {}


def main():
    r = R75.build()
    W = R126.window_years(r)
    r = r.merge(R101.exposure(r), on="pid", how="inner")
    r = r[r["win0"] >= 1975].copy()
    r = R72.state17(r)
    r["agec"] = (r["age"] - 40) / 10
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
    r["likely"] = r["pid"].map((pe >= pe.quantile(2 / 3)).astype(float))
    one = r.drop_duplicates("pid")
    terc = one.set_index("pid")["lyp"].groupby(one.set_index("pid")["birth_year"]).transform(
        lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    r["pterc"] = r["pid"].map(terc)
    v = r[r["lw"].notna()].dropna(subset=["likely"]).copy()
    a = v["agec"].to_numpy()[:, None]
    cell = (v["birth_year"].astype(int).astype(str) + "_" + v["nk_mode"].astype(int).astype(str))
    Dc = dummies(pd.factorize(cell)[0]) * a
    md = ["# The EITC eligibility contrast as one triple difference (committee re-read memo, action 9)", "",
          "Built by `136.EITCTripleDiff.py` (2026-10-24); design in its docstring. Per $1,000 of exposure x (age-40)/10; "
          "son FE; s.e. clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1. **Intent to treat; descriptive.**", "",
          f"Sons {v['pid'].nunique():,}; likely eligible {int(v.drop_duplicates('pid')['likely'].sum()):,}.", "",
          "| specification | exposure x age (reference group) | exposure x age x likely eligible | exposure x age x middle third | "
          "exposure x age x top third |", "|---|---|---|---|---|"]
    for lab, cells_ in (("birth-year and children x age (as 101)", np.column_stack([dummies(v["birth_year"]) * a,
                                                                                     dummies(v["nk_mode"]) * a])),
                        ("children x birth-year cells x age", Dc)):
        X1 = np.column_stack([(v["eitc"] * v["agec"]).to_numpy(), (v["eitc"] * v["likely"] * v["agec"]).to_numpy(),
                              (v["likely"] * v["agec"]).to_numpy(), cells_, dummies(v["age"])])
        b, V = ols(X1, v["ly"].to_numpy(float), v["wt"].to_numpy(float), v["fam68"].to_numpy(), absorb=v["pid"].to_numpy())
        e0, e1 = (b[0], np.sqrt(V[0, 0])), (b[1], np.sqrt(V[1, 1]))
        t1 = (v["pterc"] == 1).astype(float)
        t2 = (v["pterc"] == 2).astype(float)
        X2 = np.column_stack([(v["eitc"] * v["agec"]).to_numpy(), (v["eitc"] * t1 * v["agec"]).to_numpy(),
                              (v["eitc"] * t2 * v["agec"]).to_numpy(), (t1 * v["agec"]).to_numpy(),
                              (t2 * v["agec"]).to_numpy(), cells_, dummies(v["age"])])
        b2, V2 = ols(X2, v["ly"].to_numpy(float), v["wt"].to_numpy(float), v["fam68"].to_numpy(), absorb=v["pid"].to_numpy())
        md.append(f"| {lab}: likely eligible | {c(e0)} (others) | {c(e1)} | | |")
        md.append(f"| {lab}: parental-income thirds | {c((b2[0], np.sqrt(V2[0, 0])))} (bottom third) | | "
                  f"{c((b2[1], np.sqrt(V2[1, 1])))} | {c((b2[2], np.sqrt(V2[2, 2])))} |")
        RES[lab] = {"others": list(map(float, e0)), "likely_minus_others": list(map(float, e1)),
                    "bottom": [float(b2[0]), float(np.sqrt(V2[0, 0]))], "mid_minus_bottom": [float(b2[1]), float(np.sqrt(V2[1, 1]))],
                    "top_minus_bottom": [float(b2[2]), float(np.sqrt(V2[2, 2]))]}
        print("\n".join(md[-2:]), flush=True)
    md.append("")
    (OUT / "eitc_triple_diff.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "eitc_triple_diff.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
