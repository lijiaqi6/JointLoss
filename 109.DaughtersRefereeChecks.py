r"""Referee 3 checks on the sons-daughters contrast (simulated JPE round, proposals/jpe_simulated_review_20261020.md)

  R3.1 THE MOTHER. In the child's teen waves (13-19), the woman of the child's family unit (wife / partner of the head
       or the female head): her employment (hours > 0) and ln hours in waves with a father's layoff (t or t-1) against
       the other window waves of the same child (child FE; the added-worker response). Then MOM_UP = the mother worked
       more (share of waves employed) in the waves from the first teen layoff on than before it (treated children with
       both); the within-person wage slope of sons and daughters by MOM_UP (layoff share x age x MOM_UP, 92's spec).
  R3.2 WHO IS OBSERVED. Among 24's children old enough to reach a band by 2022, the probability of being observed with a
       valid wage (as a head, or a wife for daughters) at 25-29 and at 45-49, on the father's teen layoff share and 92's
       controls (linear probability, clusters 1968 family); then the within-person slope of daughters and sons weighted
       by the inverse of the predicted probability of being observed in the band (logit on the same regressors, birth-year
       dummies and race), trimmed at the 1st / 99th percentile.
  R3.3 SCHOOLING. Years of schooling, one row per child, sons and daughters stacked with every regressor x daughter; the
       difference of the layoff coefficient.
Writes output/daughters_referee_checks.md / .json (aggregates only). DESCRIPTIVE.
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
from common import DATA, OUT  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R92 = _load("s92", "92.LayoffDaughters.py")
R107 = _load("s107", "107.LayoffSexDifference.py")
R24 = R92.R24
c, dummies, ols_cl, FATHER = R92.c, R92.dummies, R92.ols_cl, R92.FATHER
kL = FATHER.index("f_sh_layoff")
RES = {}


def mother_panel(a, py, ch):
    """child x teen wave: father's layoff flag in the wave, mother's employment / ln hours."""
    dp = pd.read_pickle(DATA / "psid_displacement.pkl")
    m = (dp["main"] == 1) & (dp["strict"] != 1)
    lay = set(zip(dp.loc[m, "pid"], dp.loc[m, "year"]))
    k = py[py["child"] & py["age"].between(13, 19) & py["faminc"].between(R24.LO, R24.HI) & py["pid"].isin(ch.index)][
        ["pid", "wave", "int", "fam68"]]
    k = k.merge(ch[["fpid"]].dropna().reset_index(), on="pid")
    wom = a[a["wife"] | (a["head"] & (a["female"] == 1))].drop_duplicates(["wave", "int"])[["wave", "int", "hours", "lh", "valid"]]
    k = k.merge(wom, on=["wave", "int"], how="inner")
    y = k["wave"] - 1
    k["flay"] = [float((p, t) in lay or (p, t - 1) in lay) for p, t in zip(k["fpid"], y)]
    k["m_emp"] = (k["hours"] > 0).astype(float).where(k["hours"].notna())
    k["m_lh"] = k["lh"].where(k["valid"] == True)  # noqa: E712
    return k.sort_values(["pid", "wave"])


def main():
    a, py, ch = R24.load()
    r = R107.frame(a, py, ch)
    md = ["# Referee 3 checks on the sons-daughters contrast (simulated JPE round)", "",
          "Built by `109.DaughtersRefereeChecks.py` (2026-10-20); design in its docstring. Per unit teen layoff share unless "
          "stated; clustered by 1968 family. *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**", ""]
    # ---------------- R3.1 the mother
    K = mother_panel(a, py, ch)
    md += ["## R3.1 The mother's work in the father's layoff waves (child FE, the child's teen waves)", "",
           "| outcome | father's layoff in the wave | mean | child-waves / children |", "|---|---|---|---|"]
    for y, lab in (("m_emp", "mother employed"), ("m_lh", "mother's ln annual hours (valid years)")):
        d = K.dropna(subset=[y])
        X = np.column_stack([d[["flay"]].to_numpy(float), dummies(d["wave"])])
        b, V = ols_cl(X, d[y].to_numpy(float), np.ones(len(d)), d["fam68"].to_numpy(), absorb=d["pid"].to_numpy())
        md.append(f"| {lab} | {c((b[0], np.sqrt(V[0, 0])))} | {d[y].mean():.3f} | {len(d):,} / {d['pid'].nunique():,} |")
        RES[f"mother|{y}"] = [float(b[0]), float(np.sqrt(V[0, 0]))]
    first = K[K["flay"] == 1].groupby("pid")["wave"].min().rename("w1")
    K2 = K.merge(first, on="pid")
    pre = K2[K2["wave"] < K2["w1"]].groupby("pid")["m_emp"].mean()
    post = K2[K2["wave"] >= K2["w1"]].groupby("pid")["m_emp"].mean()
    mom = (post - pre).dropna()
    up = (mom > 0).astype(float).rename("mom_up")
    r = r.merge(up.reset_index(), on="pid", how="left")
    r["mom_up"] = r["mom_up"].fillna(0.0)
    md += ["", f"Treated children with the mother observed before and after the first teen layoff: {len(mom):,}; the mother "
           f"worked more after it for {up.mean():.0%} of them.", "",
           "| children | layoff x age, mother did not work more | layoff x age x (mother worked more) | sum (mother worked more) |",
           "|---|---|---|---|"]
    for female, lab in ((1, "daughters"), (0, "sons")):
        d = r[(r["female"] == female)].dropna(subset=["lw"] + FATHER)
        ag = d["agec"].to_numpy()[:, None]
        X = np.column_stack([d[FATHER + ["lyp"]].to_numpy(float) * ag, (d["f_sh_layoff"] * d["mom_up"]).to_numpy()[:, None] * ag,
                             dummies(d["age"])])
        b, V = ols_cl(X, d["lw"].to_numpy(float), d["wt"].to_numpy(float), d["fam68"].to_numpy(), absorb=d["pid"].to_numpy())
        j = len(FATHER) + 1
        s = (b[kL] + b[j], float(np.sqrt(V[kL, kL] + V[j, j] + 2 * V[kL, j])))
        md.append(f"| {lab} | {c((b[kL], np.sqrt(V[kL, kL])))} | {c((b[j], np.sqrt(V[j, j])))} | {c(s)} |")
        RES[f"momup|{lab}"] = {"base": [float(b[kL]), float(np.sqrt(V[kL, kL]))], "inter": [float(b[j]), float(np.sqrt(V[j, j]))],
                               "sum": list(map(float, s))}
    md.append("")
    print("R3.1 done", flush=True)
    # ---------------- R3.2 who is observed
    kids = ch[ch["fpid"].notna()].copy()
    kids = kids.drop(columns=[x for x in ("f_sh_close", "f_sh_layoff") if x in kids]).join(R92.layoff_shares(kids, py, a))
    kids = kids.dropna(subset=["lyp"] + FATHER).copy()
    kids = kids[kids["f_n"] >= 3]
    obs = r[r["lw"].notna()].groupby(["pid", "band"]).size().unstack(fill_value=0)
    md += ["## R3.2 Who is observed with a wage", "",
           "| children | band | observed (mean) | layoff coefficient on being observed | eligible children |", "|---|---|---|---|---|"]
    wts = []
    for female, lab in ((1, "daughters"), (0, "sons")):
        kk = kids[kids["female"] == female].reset_index()
        for band, lo in ((0, 25), (4, 45)):
            el = kk[kk["birth_year"] + lo <= 2022].copy()
            el["obs"] = el["pid"].map(obs[band] > 0 if band in obs else pd.Series(dtype=float)).fillna(False).astype(float)
            X = np.column_stack([el[FATHER + ["lyp"]].to_numpy(float), dummies(el["birth_year"] // 5), np.ones(len(el))])
            b, V = ols_cl(X, el["obs"].to_numpy(float), np.ones(len(el)), el["fam68"].to_numpy())
            md.append(f"| {lab} | {['25-29', '', '', '', '45-49'][band]} | {el['obs'].mean():.3f} | {c((b[kL], np.sqrt(V[kL, kL])))} | {len(el):,} |")
            RES[f"observed|{lab}|{band}"] = [float(b[kL]), float(np.sqrt(V[kL, kL])), float(el["obs"].mean())]
            Xl = sm.add_constant(np.column_stack([el[FATHER + ["lyp"]].to_numpy(float), dummies(el["birth_year"] // 5),
                                                  (el["race"] == "Black").to_numpy(float)]))
            p = sm.Logit(el["obs"].to_numpy(float), Xl).fit(disp=0).predict(Xl)
            el["ipw"] = 1 / np.clip(p, np.quantile(p, 0.01), np.quantile(p, 0.99))
            wts.append(el[["pid", "ipw"]].assign(band=band))
    W = pd.concat(wts)
    md.append("")
    md += ["Within-person ln wage slope of the layoff share, PSID weights vs PSID weights x inverse probability of being "
           "observed (the band's weight applied to the child's years in that band; other bands weight 1):", "",
           "| children | PSID weights | x IPW |", "|---|---|---|"]
    for female, lab in ((1, "daughters"), (0, "sons")):
        d = r[(r["female"] == female)].dropna(subset=["lw"] + FATHER).copy()
        d = d.merge(W, on=["pid", "band"], how="left")
        d["ipw"] = d["ipw"].fillna(1.0)
        ag = d["agec"].to_numpy()[:, None]
        X = np.column_stack([d[FATHER + ["lyp"]].to_numpy(float) * ag, dummies(d["age"])])
        out = []
        for w in (d["wt"].to_numpy(float), (d["wt"] * d["ipw"]).to_numpy(float)):
            b, V = ols_cl(X, d["lw"].to_numpy(float), w, d["fam68"].to_numpy(), absorb=d["pid"].to_numpy())
            out.append((b[kL], np.sqrt(V[kL, kL])))
        md.append(f"| {lab} | {c(out[0])} | {c(out[1])} |")
        RES[f"ipw|{lab}"] = [list(map(float, x)) for x in out]
    md.append("")
    print("R3.2 done", flush=True)
    # ---------------- R3.3 schooling
    lt = []
    for female in (0, 1):
        _, l = R24.frames(a, ch, female)
        lt.append(l[["pid", "educ"]].assign(female=float(female)))
    E = pd.concat(lt)
    one = r.drop_duplicates("pid")[["pid", "fam68", "wt", "birth_year", "female"] + FATHER + ["lyp"]].merge(
        E.drop(columns="female"), on="pid", how="left")
    one = one[one["educ"].between(0, 20)].dropna(subset=FATHER + ["lyp", "wt", "fam68"])
    fe = one["female"].to_numpy(float)[:, None]
    base = np.column_stack([one[FATHER + ["lyp"]].to_numpy(float), dummies(one["birth_year"] // 5), np.ones(len(one))])
    X = np.column_stack([base, base * fe])
    b, V = ols_cl(X, one["educ"].to_numpy(float), one["wt"].to_numpy(float), one["fam68"].to_numpy())
    Kb = base.shape[1]
    son = (b[kL], np.sqrt(V[kL, kL]))
    dau = (b[kL] + b[Kb + kL], np.sqrt(V[kL, kL] + V[Kb + kL, Kb + kL] + 2 * V[kL, Kb + kL]))
    dif = (b[Kb + kL], np.sqrt(V[Kb + kL, Kb + kL]))
    md += ["## R3.3 Years of schooling (one row per child, sons and daughters stacked)", "",
           f"Sons {c(son)}; daughters {c(dau)}; daughters - sons {c(dif)}; children {len(one):,}.", ""]
    RES["schooling"] = {"sons": list(map(float, son)), "daughters": list(map(float, dau)), "diff": list(map(float, dif))}
    (OUT / "daughters_referee_checks.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "daughters_referee_checks.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
