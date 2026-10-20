r"""Which spells make friction-predicted parental income pass on more strongly? (Paper B headline 5; 74's Shea contrast)

74.FrictionIGEPooled.py (EVIDENCE 11.28): the part of ln parental income predicted by the parents' friction shares
(father displaced / unemployed / zero hours, mother unemployed / zero hours) passes on more strongly than the rest:
earnings b_P 0.528 vs b_perp 0.360, difference 0.168*** (p=0.007). Shea (2000) predicted parental income from plausibly
exogenous sources (union status, industry, job loss) and found it passed on weakly. The headline can be stated against
Shea only if we know which spells carry our contrast: plant closures (Shea-like, not the family's choice) or layoffs /
fired and unemployment (selected).

DESIGN (74's construction, gel's 'ex' block): x = lyp residualised on the structure flags and single-age dummies;
  pr = its projection on the chosen spell measures P (also residualised); xp = x - pr. ln son's outcome on pr, xp,
  structure flags and age dummies: b_P (passing on of the spell-predicted part), b_perp (the rest), b_P - b_perp,
  R2 = share of the variance of lyp explained by P. P sets: (A) 74's set (reproduction); (B) closures only (the father's
  closure share, 75's f_sh_close); (C) layoffs only (f_sh_layoff); (D) the father's unemployment share; (E) the mother's
  unemployment share; (F) closures + layoffs. Son-years 25-55, valid years (75's frame), weighted; 200 cluster-bootstrap
  draws of 1968 families stratified by race. Outcomes ln earnings, ln wage, ln family income. Pooled (race-neutral).
Writes output/shea_contrast_by_spell.md / .json (aggregates only). Descriptive.
"""
import importlib.util
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import OUT  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R75 = _load("s75", "75.WhatIsPassedOn.py")
R74 = R75.R74
c, wls, dummies, Boot = R74.c, R74.wls, R74.dummies, R74.Boot
D_COLS = R74.DST
SETS = [("(A) 74's set: father displaced / unemployed / zero hours, mother unemployed / zero hours", R74.FAT + R74.MOT),
        ("(B) father's plant closures only", ["f_sh_close"]), ("(C) father's layoffs / firings only", ["f_sh_layoff"]),
        ("(D) father's unemployment share only", ["f_sh_unemp"]), ("(E) mother's unemployment share only", ["m_sh_unemp"]),
        ("(F) father's closures + layoffs", ["f_sh_close", "f_sh_layoff"])]
YS = [("ly", "ln earnings"), ("lw", "ln hourly wage"), ("lfam", "ln family income")]
RES = {}


def shea(x, Y, P, ZD, w):
    sw = np.sqrt(w)
    xt = x - ZD @ wls(ZD, x[:, None], sw)[:, 0]
    Pt = P - ZD @ wls(ZD, P, sw)
    pr = Pt @ wls(Pt, xt[:, None], sw)[:, 0]
    xp = xt - pr
    R2 = np.sum(w * pr ** 2) / np.sum(w * xt ** 2)
    B = wls(np.column_stack([pr, xp, ZD]), Y, sw)
    return np.array([B[0, 0], B[1, 0], B[0, 0] - B[1, 0], R2])


def main():
    t0 = time.time()
    r = R75.build()
    BT = Boot(r["fam68"].to_numpy(), r["race"].to_numpy())
    md = ["# Which spells make friction-predicted parental income pass on more strongly (Shea contrast)", "",
          "Built by `89.SheaContrastBySpell.py` (2026-10-20); design in its docstring. Pooled PSID sons 25-55, weighted; "
          f"{R74.NBOOT} cluster-bootstrap draws of 1968 families; estimate (s.e.; p), *** p<0.01, ** p<0.05, * p<0.1. "
          "b_P = passing on of the part of ln parental income predicted by the spell measures; b_perp = of the rest.", "",
          "| outcome | spells predicting parental income | R2 | b_P | b_perp | b_P - b_perp |", "|---" * 6 + "|"]
    for y, ylab in YS:
        d = r[r[y].notna() & r["lw"].notna()] if y != "lfam" else r[r["lfam"].notna()]
        for lab, P in SETS:
            z = d.dropna(subset=[y, "lyp"] + P + D_COLS)
            ZD = np.column_stack([z[D_COLS].to_numpy(float), dummies(z["age"]), np.ones((len(z), 1))])
            x, Y, Pm, w0 = (z["lyp"].to_numpy(float), z[[y]].to_numpy(float), z[P].to_numpy(float),
                            z["wt"].to_numpy(float))
            pt = shea(x, Y, Pm, ZD, w0)
            ri = BT.rows(z["fam68"].to_numpy())
            dr = np.zeros((BT.cnt.shape[0], 4))
            for b in range(BT.cnt.shape[0]):
                w = w0 * BT.cnt[b, ri]
                k = w > 0
                dr[b] = shea(x[k], Y[k], Pm[k], ZD[k], w[k])
            se = np.nanstd(dr, axis=0, ddof=1)
            md.append(f"| {ylab} | {lab} | {pt[3]:.3f} | {c((pt[0], se[0]))} | {c((pt[1], se[1]))} | "
                      f"{c((pt[2], se[2]))} |")
            RES[f"{y}|{lab}"] = {"bP": [pt[0], se[0]], "bperp": [pt[1], se[1]], "diff": [pt[2], se[2]], "R2": pt[3]}
        print(f"{y} {time.time() - t0:.0f}s", flush=True)
    md.append("")
    (OUT / "shea_contrast_by_spell.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "shea_contrast_by_spell.json", "w"), indent=1, default=float)
    print(f"done {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
