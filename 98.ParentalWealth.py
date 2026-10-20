r"""Does parental wealth account for the rest of the IGE split? (Fable addition B3, 2026-10-20)

80.WhatIsPassedOnRest.py leaves about half of the earnings IGE as parental income at equal components and resources.
The one resource the split lacks is wealth. The PSID measures net worth (with home equity) in 1984, 1989, 1994, 1999 and
every wave after (18.HusbandIndustryShocks.py's wealth(): 'IMP WEALTH W/ EQUITY', 2000 dollars), which falls in the
teens of sons born about 1970 and later.
WEALTH: the mean net worth of the son's family unit over the wealth waves at his wave-ages 12-20 (>= 1), entered as
  (i) its percentile rank within the son's birth year (weighted) and (ii) asinh(net worth / 1,000); missing -> no son
  enters (the sample is the sons with a measure).
DESIGN: 80's son-years and split B (its groups + parents' schooling), on the sons with a wealth measure; the same split
  with WEALTH as an added group; rest with and without it on the same son-years; ln earnings 25-55 and by band where the
  cohort reaches it; 200 cluster-bootstrap draws (74's run_spec). Descriptive accounting.
Writes output/parental_wealth.md / .json (aggregates only).
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


R80 = _load("s80", "80.WhatIsPassedOnRest.py")
R18 = _load("s18", "18.HusbandIndustryShocks.py")
R75, R74 = R80.R75, R80.R74
est, cc, Boot, run_spec = R74.est, R74.cc, R74.Boot, R74.run_spec
CACHE = DATA / "parental_wealth_sons.pkl"
RES = {}


def son_wealth(r):
    if CACHE.exists():
        return pd.read_pickle(CACHE)
    W = R18.wealth()[["wave", "int", "wealth2"]]
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    k = py[py["child"] & py["age"].between(12, 20) & py["pid"].isin(r["pid"].unique())][["pid", "wave", "int"]]
    k = k.merge(W, on=["wave", "int"])
    g = k.groupby("pid")["wealth2"]
    out = pd.DataFrame({"nw": g.mean(), "nw_n": g.count()}).reset_index()
    out.to_pickle(CACHE)
    return out


def main():
    r, _, _ = R80.build()
    r = r.merge(son_wealth(r), on="pid", how="left")
    d = r[r["lw"].notna() & r["nw"].notna()].copy()
    one = d.drop_duplicates("pid").copy()
    one["nw_rank"] = one.groupby("birth_year")["nw"].rank(pct=True)
    one["nw_asinh"] = np.arcsinh(one["nw"] / 1000)
    d = d.merge(one[["pid", "nw_rank", "nw_asinh"]], on="pid", how="left")
    base = {**{g: v for g, v in R75.GROUPS.items() if g != "structure"}, **R80.NEW,
            "structure": R75.GROUPS["structure"] + ["f_educ_na", "m_educ_na", "inc_na"]}
    BT = Boot(d["fam68"].to_numpy(), d["race"].to_numpy())
    md = ["# Does parental wealth account for the rest of the IGE split? (Fable B3)", "",
          "Built by `98.ParentalWealth.py` (2026-10-20); design in its docstring. PSID sons with a parental net-worth "
          "measure at their 12-20 (born about 1970 and later); ln earnings, valid years; 80's split B with and without "
          "wealth; estimate (s.e.; p) from 200 cluster-bootstrap draws of 1968 families; *** p<0.01, ** p<0.05, * p<0.1.",
          "", f"Sons {one['pid'].nunique():,} (birth years {int(one['birth_year'].min())}-{int(one['birth_year'].max())}); "
          f"son-years {len(d):,}; median parental net worth ${np.median(one['nw']):,.0f} (2000 dollars); wealth waves per "
          f"son: mean {one['nw_n'].mean():.2f}.", ""]
    cells = (0, 2, 6)
    lab_c = {0: "25-29", 2: "35-39", 6: "25-55"}
    md += ["| split | cell | IGE | wealth contribution | rest | rest share | wealth share |", "|---" * 7 + "|"]
    for lab, G in (("split B (no wealth)", base), ("+ wealth: within-birth-year rank", {**base, "wealth": ["nw_rank"]}),
                   ("+ wealth: asinh(net worth)", {**base, "wealth": ["nw_asinh"]})):
        res = run_spec(d, ["ly"], G, BT, cells=cells)
        for k in cells:
            if k not in res:
                continue
            b0, b = est(res, k, "b0", 0), est(res, k, "b", 0)
            sh = est(res, k, "b", 0, share=True)
            wc = est(res, k, "c:wealth", 0) if "wealth" in G else None
            ws = est(res, k, "c:wealth", 0, share=True) if "wealth" in G else None
            md.append(f"| {lab} | {lab_c[k]} | {cc(b0)} | {cc(wc)} | {cc(b)} | {cc(sh)} | {cc(ws)} |")
            RES[f"{lab}|{lab_c[k]}"] = {"b0": list(b0[:2]), "b": list(b[:2]), "share": list(sh[:2]),
                                        "wealth": list(wc[:2]) if wc else None, "wealth_share": list(ws[:2]) if ws else None}
        RES[f"{lab}|groups"] = {g: list(est(res, 6, f"c:{g}", 0, share=True)[:2]) for g in G if g != "structure"}
        for k in cells:
            if k in res:
                st = lambda g: "b" if g == "b" else f"c:{g}"  # noqa: E731
                RES[f"{lab}|groups|{lab_c[k]}"] = {g: list(est(res, k, st(g), 0, share=True)[:2])
                                                   for g in list(G) + ["b"] if g != "structure"
                                                   and est(res, k, st(g), 0, share=True)}
    md += ["", "Group shares of the 25-55 IGE (split B / + wealth rank / + wealth asinh):", "",
           "| group | split B | + wealth rank | + asinh |", "|---|---|---|---|"]
    gl = list(RES["split B (no wealth)|groups"]) + ["wealth"]
    for g in gl:
        vals = [RES[f"{lab}|groups"].get(g) for lab in ("split B (no wealth)", "+ wealth: within-birth-year rank",
                                                         "+ wealth: asinh(net worth)")]
        md.append(f"| {g} | " + " | ".join(cc((v[0], v[1])) if v else "" for v in vals) + " |")
    md.append("")
    (OUT / "parental_wealth.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "parental_wealth.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
