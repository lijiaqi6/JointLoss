r"""What identifies the 'rest' of the IGE split? (Fable addition B2, 2026-10-20)

80.WhatIsPassedOnRest.py's split B leaves 47.6%*** of the earnings IGE as parental income at equal components and
equal other resources. Among those resources are the parents' ln labour income (lpl) and the shares of family income
that are asset, transfer and other members' income - which together nearly DEFINE ln parental income:
  family income = labour + asset + transfer + other   =>   lyp ~ lpl - ln(1 - s_asset - s_tr - s_oth),
up to the log of a mean versus a mean of shares, clipping of shares to [0, 1] and years without the items. Holding them
fixed, the rest is identified by that residual variation. This script measures it:
  (1) R2 of lyp on: 75's components + structure; + 80's resources; the identity term alone;
  (2) the residual s.d. of lyp in each case (how much variation identifies the rest);
  (3) the split with the INCOME-DEFINED resources left out (lpl and the three shares): resources = parents' schooling,
      home ownership, AFDC / TANF years, children in the unit; the rest is then parental income at equal components
      and equal non-income resources (pooled sons, ln earnings, 200 draws).
Writes output/rest_identification.md / .json (aggregates only).
"""
import importlib.util
import json
import sys
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


R80 = _load("s80", "80.WhatIsPassedOnRest.py")
R75, R74 = R80.R75, R80.R74
est, cc, Boot, run_spec = R74.est, R74.cc, R74.Boot, R74.run_spec
RES = {}


def r2(d, xs):
    X = np.column_stack([d[xs].to_numpy(float), np.ones(len(d))])
    w = d["wt"].to_numpy(float)
    y = d["lyp"].to_numpy(float)
    sw = np.sqrt(w)
    b = np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)[0]
    u = y - X @ b
    my = np.average(y, weights=w)
    return 1 - np.average(u ** 2, weights=w) / np.average((y - my) ** 2, weights=w), float(np.sqrt(np.average(u ** 2, weights=w)))


def main():
    r, _, _ = R80.build()
    d = r[r["lw"].notna()].copy()
    one = d.drop_duplicates("pid").copy()
    oth = (one["s_asset"] + one["s_tr"] + one["s_oth"]).clip(upper=0.95)
    one["ident"] = one["lpl"] - np.log(1 - oth)
    comps = [v for g in R75.GROUPS.values() for v in g]
    new = [v for g in R80.NEW.values() for v in g]
    sd0 = float(np.sqrt(np.average((one["lyp"] - np.average(one["lyp"], weights=one["wt"])) ** 2, weights=one["wt"])))
    md = ["# What identifies the 'rest' of the IGE split? (Fable B2)", "",
          "Built by `97.RestIdentification.py` (2026-10-20); design in its docstring. One row per son (sons with a valid "
          f"wage at 25-55), PSID weights. S.d. of ln parental income {sd0:.3f}.", "",
          "## 1. How much of ln parental income the mediators predict", "",
          "| regressors | R2 | residual s.d. |", "|---|---|---|"]
    for lab, xs in (("75's components + structure", comps),
                    ("+ 80's resources (lpl, asset / transfer / other shares, own, AFDC, children, schooling)",
                     comps + new + ["f_ed", "m_ed", "f_educ_na", "m_educ_na", "inc_na"]),
                    ("lpl alone", ["lpl"]), ("lpl + the three income shares", ["lpl", "s_asset", "s_tr", "s_oth"]),
                    ("the identity term lpl - ln(1 - shares)", ["ident"])):
        R2, s = r2(one, xs)
        md.append(f"| {lab} | {R2:.3f} | {s:.3f} |")
        RES[f"r2|{lab}"] = [float(R2), s]
    md.append("")
    # split without the income-defined resources
    keep_new = {"assets": ["own"], "transfers": ["welf"], "family size": ["nkid"], "schooling": ["f_ed", "m_ed"]}
    gb = {**{g: v for g, v in R75.GROUPS.items() if g != "structure"}, **keep_new,
          "structure": R75.GROUPS["structure"] + ["f_educ_na", "m_educ_na", "inc_na"]}
    gfull = {**{g: v for g, v in R75.GROUPS.items() if g != "structure"}, **R80.NEW,
             "schooling": ["f_ed", "m_ed"],
             "structure": R75.GROUPS["structure"] + ["f_educ_na", "m_educ_na", "inc_na"]}
    gfull = {k: [x for x in v if not (k == "parents' schooling")] for k, v in gfull.items()}
    BT = Boot(d["fam68"].to_numpy(), d["race"].to_numpy())
    md += ["## 2. The split with and without the income-defined resources (ln earnings, 25-55)", "",
           "| split | IGE | rest | rest share |", "|---|---|---|---|"]
    for lab, G in (("80's split B (with lpl and the income shares)", gfull),
                   ("without lpl and the income shares (non-income resources only)", gb)):
        G = {k: [x for x in dict.fromkeys(v)] for k, v in G.items()}
        seen, G2 = set(), {}
        for k, v in G.items():
            vv = [x for x in v if x not in seen]
            seen |= set(vv)
            if vv:
                G2[k] = vv
        res = run_spec(d, ["ly"], G2, BT, cells=(6,))
        b0, b = est(res, 6, "b0", 0), est(res, 6, "b", 0)
        sh = est(res, 6, "b", 0, share=True)
        md.append(f"| {lab} | {cc(b0)} | {cc(b)} | {cc(sh)} |")
        RES[f"split|{lab}"] = {"b0": list(b0[:2]), "b": list(b[:2]), "share": list(sh[:2])}
        for g in G2:
            if g in ("structure",):
                continue
            e = est(res, 6, f"c:{g}", 0, share=True)
            if e:
                md.append(f"| &nbsp;&nbsp;{g} share | | | {cc(e)} |")
    md.append("")
    (OUT / "rest_identification.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "rest_identification.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
