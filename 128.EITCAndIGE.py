r"""Does the EITC in childhood change the IGE, and differently by the son's age? (PI question, 2026-10-24)

101 / 126 / 127: exposure to the EITC over the son's 13-18 (maximum federal + state credit for the family's number of
children, thousands of 2000 dollars, intent to treat) goes with faster within-son earnings growth, concentrated in the
families the credit reaches; it reaches them as income. Those families are low-income, so the credit could flatten
the parent-son gradient, more at older ages.
SAMPLE: 101's (75's sons, window income years 1975+, born 1962+), son-years with a valid wage, bands 25-29 ... 40-44.
DESIGNS (PSID weights; clusters 1968 family; birth-year, state-at-17 and number-of-children FE; single-age dummies):
  1. by band: ln earnings on lyp, exposure and exposure x (lyp - mean lyp); the interaction is the change in the IGE per
     $1,000 of exposure; the change 40-44 minus 25-29 of the interaction from one stacked regression; within son:
     exposure x lyp x (age-40)/10 with son FE, lyp x age, exposure x age and the FE x age.
  2. the IGE by band in sons with exposure above and below the median of its residual on the three FE.
  3. the IGE by band without and with the family's imputed credit over the son's 13-18 (127's imputation at the
     family's actual earned income; thousands of 2000 dollars, summed and scaled to six years) as a control: the change
     in the IGE is what the credit income carries.
Writes output/eitc_ige.md / .json (aggregates only). INTENT TO TREAT; DESCRIPTIVE.
"""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import DATA, OUT  # noqa: E402


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


def fe(q):
    return [dummies(q["birth_year"]), dummies(q["st17"]), dummies(q["nk_mode"]), dummies(q["age"])]


def lin(b, V, w):
    w = np.asarray(w, float)
    return float(w @ b), float(np.sqrt(w @ V @ w))


def main():
    r = R75.build()
    W = R126.window_years(r)
    nom = (W["hlab"].fillna(0) + W["wlab"].fillna(0)) / W["defl"]
    W["credit"] = [R127.credit(e, int(n), int(y), f == 0) for e, n, y, f in zip(nom, W["nk"], W["year"], W["nofa"])]
    W["credit"] = W["credit"] * (1 + W["state_eitc_rate"]) * W["defl"] / 1000
    g = W.groupby("pid")["credit"]
    cr = (g.sum() * 6 / g.count()).rename("credit6")
    r = r.merge(R101.exposure(r), on="pid", how="inner")
    r = r[r["win0"] >= 1975].copy()
    r = R72.state17(r)
    r["st17"] = r["fips17"].fillna(-1).astype(int)
    r["agec"] = (r["age"] - 40) / 10
    r = r.merge(cr, left_on="pid", right_index=True, how="left")
    v = r[r["lw"].notna() & r["band"].between(0, 3)].copy()
    one = v.drop_duplicates("pid")
    mu = float(np.average(one["lyp"], weights=one["wt"]))
    v["lypc"] = v["lyp"] - mu
    v["ex_lyp"] = v["eitc"] * v["lypc"]
    md = ["# Does the EITC in childhood change the IGE, by the son's age? (PI question)", "",
          "Built by `128.EITCAndIGE.py` (2026-10-24); design in its docstring. Exposure in thousands of 2000 dollars over "
          "13-18; s.e. clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1. **Intent to treat; descriptive.**", "",
          f"Sons {one['pid'].nunique():,}; exposure mean {np.average(one['eitc'], weights=one['wt']):.2f} (s.d. "
          f"{one['eitc'].std():.2f}); imputed credit over 13-18 mean {np.average(one['credit6'].fillna(0), weights=one['wt']):.2f} "
          f"(s.d. {one['credit6'].std():.2f}); corr(exposure, lyp) {np.corrcoef(one['eitc'], one['lyp'])[0, 1]:.3f}.", "",
          "## 1. Exposure x parental income: the change in the IGE per $1,000 of exposure", "",
          "| | " + " | ".join(BL[:4]) + " | change 40-44 - 25-29 | within son x age |", "|---" * 7 + "|"]
    cells, ige = [], []
    for k in range(4):
        q = v[v["band"] == k]
        X = np.column_stack([q[["ex_lyp", "lypc", "eitc"]].to_numpy(float)] + fe(q) + [np.ones(len(q))])
        b, V = ols(X, q["ly"].to_numpy(float), q["wt"].to_numpy(float), q["fam68"].to_numpy())
        cells.append((b[0], np.sqrt(V[0, 0])))
        ige.append((b[1], np.sqrt(V[1, 1])))
    s = v[v["band"].isin([0, 3])]
    b3 = (s["band"] == 3).to_numpy(float)
    base = np.column_stack([s[["ex_lyp", "lypc", "eitc"]].to_numpy(float)] + fe(s) + [np.ones(len(s))])
    b, V = ols(np.column_stack([base, base * b3[:, None]]), s["ly"].to_numpy(float), s["wt"].to_numpy(float),
               s["fam68"].to_numpy())
    K = base.shape[1]
    ch = (b[K], np.sqrt(V[K, K]))
    a = v["agec"].to_numpy()[:, None]
    Xf = np.column_stack([v[["ex_lyp", "lypc", "eitc"]].to_numpy(float) * a, dummies(v["birth_year"]) * a,
                          dummies(v["nk_mode"]) * a, dummies(v["age"])])
    bf, Vf = ols(Xf, v["ly"].to_numpy(float), v["wt"].to_numpy(float), v["fam68"].to_numpy(), absorb=v["pid"].to_numpy())
    fe_ = (bf[0], np.sqrt(Vf[0, 0]))
    md.append("| exposure x ln parental income | " + " | ".join(c(x) for x in cells) + f" | {c(ch)} | {c(fe_)} |")
    md.append("| IGE at mean exposure (same regression) | " + " | ".join(c(x) for x in ige) + " | | |")
    sdx = float(one["eitc"].std())
    md += ["", f"One s.d. of exposure ({sdx:.2f}) times the interaction: " + ", ".join(
        f"{BL[k]} {cells[k][0] * sdx:+.3f}" for k in range(4)) + ".", ""]
    RES["interaction"] = {"bands": [list(map(float, x)) for x in cells], "ige": [list(map(float, x)) for x in ige],
                          "change": list(map(float, ch)), "fe": list(map(float, fe_)), "sd_exposure": sdx}
    print("\n".join(md[-4:]), flush=True)
    # 2. IGE by residual exposure
    o = one.copy()
    Xr = np.column_stack([dummies(o["birth_year"]), dummies(o["st17"]), dummies(o["nk_mode"]), np.ones(len(o))])
    br = np.linalg.lstsq(Xr, o["eitc"].to_numpy(float), rcond=None)[0]
    o["res"] = o["eitc"].to_numpy(float) - Xr @ br
    hi = set(o.loc[o["res"] >= o["res"].median(), "pid"])
    v["hi"] = v["pid"].isin(hi)
    md += ["## 2. The IGE by band, sons with more and less exposure than expected from their birth year, state and "
           "number of children", "", "| | " + " | ".join(BL[:4]) + " | change 40-44 - 25-29 | sons |", "|---" * 7 + "|"]
    res2 = {}
    for lab, q0 in (("more exposure", v[v["hi"]]), ("less exposure", v[~v["hi"]])):
        out = []
        for k in range(4):
            q = q0[q0["band"] == k]
            X = np.column_stack([q[["lypc"]].to_numpy(float)] + fe(q) + [np.ones(len(q))])
            b, V = ols(X, q["ly"].to_numpy(float), q["wt"].to_numpy(float), q["fam68"].to_numpy())
            out.append((b[0], np.sqrt(V[0, 0])))
        s = q0[q0["band"].isin([0, 3])]
        b3 = (s["band"] == 3).to_numpy(float)
        base = np.column_stack([s[["lypc"]].to_numpy(float)] + fe(s) + [np.ones(len(s))])
        b, V = ols(np.column_stack([base, base * b3[:, None]]), s["ly"].to_numpy(float), s["wt"].to_numpy(float),
                   s["fam68"].to_numpy())
        chg = (b[base.shape[1]], np.sqrt(V[base.shape[1], base.shape[1]]))
        md.append(f"| {lab} | " + " | ".join(c(x) for x in out) + f" | {c(chg)} | {q0['pid'].nunique():,} |")
        res2[lab] = {"bands": [list(map(float, x)) for x in out], "change": list(map(float, chg))}
    RES["split"] = res2
    md.append("")
    # 3. the imputed credit as a control
    md += ["## 3. The IGE by band without and with the family's imputed credit over 13-18", "",
           "| | " + " | ".join(BL[:4]) + " |", "|---" * 5 + "|"]
    q0 = v.dropna(subset=["credit6"])
    rows = {"without": [], "with": [], "diff": [], "credit coef": []}
    for k in range(4):
        q = q0[q0["band"] == k]
        X0 = np.column_stack([q[["lypc"]].to_numpy(float)] + fe(q) + [np.ones(len(q))])
        X1 = np.column_stack([q[["lypc", "credit6"]].to_numpy(float)] + fe(q) + [np.ones(len(q))])
        b0, V0 = ols(X0, q["ly"].to_numpy(float), q["wt"].to_numpy(float), q["fam68"].to_numpy())
        b1, V1 = ols(X1, q["ly"].to_numpy(float), q["wt"].to_numpy(float), q["fam68"].to_numpy())
        rows["without"].append((b0[0], np.sqrt(V0[0, 0])))
        rows["with"].append((b1[0], np.sqrt(V1[0, 0])))
        rows["credit coef"].append((b1[1], np.sqrt(V1[1, 1])))
        rows["diff"].append(b0[0] - b1[0])
    for lab in ("without", "with", "credit coef"):
        md.append(f"| IGE {lab} | " if lab != "credit coef" else "| credit (per $1,000 over 13-18) | ")
        md[-1] += " | ".join(c(x) for x in rows[lab]) + " |"
    md.append("| IGE carried by the credit (without - with) | " + " | ".join(f"{x:+.4f}" for x in rows["diff"]) + " |")
    RES["credit"] = {k: [list(map(float, x)) if isinstance(x, tuple) else float(x) for x in vv] for k, vv in rows.items()}
    md.append("")
    (OUT / "eitc_ige.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "eitc_ige.json", "w"), indent=1, default=float)
    print("\n".join(md))


if __name__ == "__main__":
    main()
