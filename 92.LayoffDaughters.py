r"""Does a father's teen layoff cost DAUGHTERS more as they age? Fable's addition A4 (2026-10-20).

The headline (88.LayoffCostByAge.py, 91.LayoffSelection.py) is on sons with 75's full set of components, which
exists for sons only. This script runs ONE reduced specification on sons and daughters alike, so the two can be
compared: 24.IGEDecomposition.py's children (both sexes; father = the male head of the child's unit at 16) and their
adult years at 25-55 (sons: male heads; daughters: heads or wives), with
  x      lyp = ln parental family income, mean over the child's wave-ages 13-19 (24 / 6.IGEMain.py);
  father f_lw, f_lh (means over his valid window years), f_sh_unemp, f_sh_zero, f_vtr (24's person_measures over the
         window), and his shares of window waves with a PLANT CLOSURE and with a LAYOFF / FIRING (psid_displacement
         'strict' and 'main and not strict', t or t-1, as in 75), in the waves in which he is the male head.
  sample father present with >= 3 valid window years; child-years with the outcome; PSID weights (wt of the
         child-year); single-age dummies.
Outcomes: ln earnings and ln hourly wage (valid years), ln family income (every year in bounds).
Estimates: the layoff coefficient in 25-29 and 45-49 and its change (one stacked regression, every regressor and age
dummy interacted with the band, s.e. clustered by 1968 family), and the within-person slope: person FE, single-age
dummies, every regressor x (age-40)/10. Closure rows alongside. DESCRIPTIVE.
Writes output/layoff_daughters.md / .json (aggregates only).
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
from common import DATA, OUT  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R24 = _load("s24", "24.IGEDecomposition.py")
R73 = _load("s73", "73.SharedFriction.py")
FATHER = ["f_lw", "f_lh", "f_sh_unemp", "f_sh_zero", "f_vtr", "f_sh_close", "f_sh_layoff"]
OUTC = {"ly": "ln earnings", "lw": "ln hourly wage", "lfam": "ln family income"}
RES = {}


def stars(p):
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""


def c(t):
    b, s = t
    p = 2 * stats.norm.sf(abs(b / s))
    return f"{b:.3f}{stars(p)} ({s:.3f}; p={'<0.001' if p < 0.001 else f'{p:.3f}'})"


def dummies(s):
    return pd.get_dummies(s.astype(int), drop_first=True).to_numpy(float)


def ols_cl(X, y, w, g, absorb=None):
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


def layoff_shares(ch, py, a):
    dp = pd.read_pickle(DATA / "psid_displacement.pkl")
    clo = set(zip(dp.loc[dp["strict"] == 1, "pid"], dp.loc[dp["strict"] == 1, "year"]))
    m = (dp["main"] == 1) & (dp["strict"] != 1)
    lay = set(zip(dp.loc[m, "pid"], dp.loc[m, "year"]))
    k = py[py["child"] & py["age"].between(13, 19) & py["faminc"].between(R24.LO, R24.HI) & py["pid"].isin(ch.index)][
        ["pid", "wave"]]
    fa = a[a["head"] & (a["female"] == 0)][["pid", "wave"]].rename(columns={"pid": "fpid"}).drop_duplicates()
    fw = k.merge(ch[["fpid"]].dropna().reset_index(), on="pid").merge(fa, on=["fpid", "wave"])
    yr = fw["wave"] - 1
    fw["f_sh_close"] = [float((p, y) in clo or (p, y - 1) in clo) for p, y in zip(fw["fpid"], yr)]
    fw["f_sh_layoff"] = [float((p, y) in lay or (p, y - 1) in lay) for p, y in zip(fw["fpid"], yr)]
    return fw.groupby("pid")[["f_sh_close", "f_sh_layoff"]].mean()


def main():
    a, py, ch = R24.load()
    ch = ch.drop(columns=[x for x in ("f_sh_close", "f_sh_layoff") if x in ch]).join(layoff_shares(ch, py, a))
    wt = a[["pid", "wave", "wt"]].drop_duplicates(["pid", "wave"])
    md = ["# A father's teen layoff and daughters' outcomes by age (Fable A4)", "",
          "Built by `92.LayoffDaughters.py` (2026-10-20); design in its docstring. One reduced specification for sons "
          "and daughters: the outcome on lyp and the father's window measures (wage, hours, unemployment, zero hours, "
          "volatility, closure share, layoff share), single-age dummies, PSID weights, father present. Estimate (s.e.; "
          "p) clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**", ""]
    md += ["| children | outcome | layoff 25-29 | layoff 45-49 | change | within-person layoff x age | closure change | "
           "within-person closure x age | treated at 45-49 / N children |", "|---" * 9 + "|"]
    for female, lab in ((0, "sons"), (1, "daughters")):
        r, _ = R24.frames(a, ch, female)
        r = r.drop(columns=[x for x in ("f_sh_close", "f_sh_layoff") if x in r]).join(
            ch[["f_sh_close", "f_sh_layoff"]], on="pid")
        r = r.merge(wt, on=["pid", "wave"], how="left")
        r = r[(r["wt"] > 0) & r["fpid"].notna() & (r["f_n"] >= 3)]
        r["band"] = pd.cut(r["age"], [24, 29, 34, 39, 44, 49, 55], labels=False)
        r["agec"] = (r["age"] - 40) / 10
        r["lfam"] = r["lfam"].where(r["lfam"].notna())
        for y, ylab in OUTC.items():
            d = r.dropna(subset=[y, "lyp"] + FATHER).copy()
            d["one"] = 1.0
            # stacked 25-29 and 45-49
            s = d[d["band"].isin([0, 4])].copy()
            b4 = (s["band"] == 4).to_numpy(float)
            base = np.column_stack([s[["lyp"] + FATHER].to_numpy(float), dummies(s["age"]), np.ones(len(s))])
            X = np.column_stack([base, base * b4[:, None]])
            bb, V = ols_cl(X, s[y].to_numpy(float), s["wt"].to_numpy(float), s["fam68"].to_numpy())
            kL, kC, K = 1 + FATHER.index("f_sh_layoff"), 1 + FATHER.index("f_sh_close"), base.shape[1]
            g0 = (bb[kL], np.sqrt(V[kL, kL]))
            g4 = (bb[kL] + bb[K + kL], np.sqrt(V[kL, kL] + V[K + kL, K + kL] + 2 * V[kL, K + kL]))
            ch_l = (bb[K + kL], np.sqrt(V[K + kL, K + kL]))
            ch_c = (bb[K + kC], np.sqrt(V[K + kC, K + kC]))
            # within person
            xs = np.column_stack([d[["lyp"] + FATHER].to_numpy(float) * d["agec"].to_numpy()[:, None],
                                  dummies(d["age"])])
            bf, Vf = ols_cl(xs, d[y].to_numpy(float), d["wt"].to_numpy(float), d["fam68"].to_numpy(),
                            absorb=d["pid"].to_numpy())
            fl = (bf[kL], np.sqrt(Vf[kL, kL]))
            fc = (bf[kC], np.sqrt(Vf[kC, kC]))
            tr = int(d[(d["band"] == 4) & (d["f_sh_layoff"] > 0)]["pid"].nunique())
            md.append(f"| {lab} | {ylab} | {c(g0)} | {c(g4)} | {c(ch_l)} | {c(fl)} | {c(ch_c)} | {c(fc)} | "
                      f"{tr:,} / {d['pid'].nunique():,} |")
            RES[f"{lab}|{y}"] = {"g0": list(map(float, g0)), "g4": list(map(float, g4)), "change": list(map(float, ch_l)),
                                 "fe": list(map(float, fl)), "closure_change": list(map(float, ch_c)),
                                 "closure_fe": list(map(float, fc)), "treated_45_49": tr, "children": int(d["pid"].nunique())}
        print(lab, "done", flush=True)
    md.append("")
    (OUT / "layoff_daughters.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "layoff_daughters.json", "w"), indent=1)


if __name__ == "__main__":
    main()
