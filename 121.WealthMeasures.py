r"""How parents' wealth enters the IGE split: functional form, components, sample (committee memo K1, 2026-10-24)

98.ParentalWealth.py: parental net worth carries 29.1*** percent of the 25-55 earnings IGE as a within-birth-year rank
and 14.5*** as asinh. A reader of wealth data asks which number, which part of net worth, and whether the SEO
oversample of low-income families drives it. Same sons, son-years, split B and bootstrap draws as 98.
WEALTH (mean over the wealth waves at the son's wave-ages 12-20, 2000 dollars; 18's wealth files, 'IMP' values):
  total     'IMP WEALTH W/ EQUITY' (as 98)
  housing   'IMP VALUE HOME EQUITY' + 'IMP VAL OTH REAL ESTATE' (2013+: asset - debt)
  business  'IMP VALUE FARM/BUS' (2013+: asset - debt)
  other     total - housing - business: checking and savings, stocks, bonds, IRAs, vehicles, other assets, less other
            debts (the residual, so the three add up to the total)
FORMS: within-birth-year percentile rank (ties averaged, as 98); asinh(x / 1,000); ln(x / 1,000) for x > 0 with a
  non-positive flag (x <= 0 -> 0 and flag 1).
SPECS: (1) total as rank / asinh / log + flag; (2) the SRC (original 1968 Survey Research Center) sample only, 1968
  family number < 3000, rank re-computed within it, and asinh; (3) the three components as three groups, as ranks and as
  asinh. Shares of the IGE at 25-29, 35-39 and 25-55, with the parents' wage share alongside.
Writes output/wealth_measures.md / .json (aggregates only); caches data/parental_wealth_components.pkl (family-level).
DESCRIPTIVE ACCOUNTING.
"""
import importlib.util
import json
import re
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


R98 = _load("s98", "98.ParentalWealth.py")
R80, R75, R74, R18 = R98.R80, R98.R75, R98.R74, R98.R18
est, cc, Boot, run_spec = R74.est, R74.cc, R74.Boot, R74.run_spec
CACHE = DATA / "parental_wealth_components.pkl"
PAT = {"total": [r"IMP WEALTH W/ EQUITY"], "home": [r"IMP VALUE HOME EQUITY"],
       "ore": [r"IMP VAL OTH REAL ESTATE \(", r"IMP VAL OTH REAL ESTATE ASSET"],
       "ore_d": [r"IMP VAL OTH REAL ESTATE DEBT"],
       "bus": [r"IMP VALUE FARM/BUS \(", r"IMP VALUE FARM/BUS ASSET"], "bus_d": [r"IMP VALUE FARM/BUS DEBT"]}
CELLS = (0, 2, 6)
LAB = {0: "25-29", 2: "35-39", 6: "25-55"}
RES = {}


def components():
    """wave x int: total, housing, business, other net worth (2000 dollars)."""
    if CACHE.exists():
        return pd.read_pickle(CACHE)
    rows = []
    for w in R18.WEALTH_WAVES:
        if w <= 2007:
            do = R18.FAM / f"wlth{w}" / f"WLTH{w}.do"
        else:
            do = next(f for f in (R18.FAM / f"fam{w}er").glob("*.do") if "formats" not in f.name)
        pos, labs = R18.layout(do)
        idv = labs[1][0]
        sel = {}
        for k, pats in PAT.items():
            hit = next((v for p in pats for v, l in labs if re.match(p, l)), None)
            if hit:
                sel[k] = hit
        d = R18.read(do.with_suffix(".txt"), [idv] + list(sel.values()), pos)
        g = lambda k: pd.to_numeric(d[sel[k]], errors="coerce") if k in sel else 0.0  # noqa: E731
        x = pd.DataFrame({"wave": w, "int": d[idv]})
        x["total"] = R18.to2000(g("total"), w)
        x["home"] = R18.to2000(g("home") + g("ore") - g("ore_d"), w)
        x["bus"] = R18.to2000(g("bus") - g("bus_d"), w)
        x["other"] = x["total"] - x["home"] - x["bus"]
        print(f"  {w}: " + ", ".join(f"{k}={v}" for k, v in sel.items()), flush=True)
        rows.append(x)
    C = pd.concat(rows, ignore_index=True)
    C.to_pickle(CACHE)
    return C


def son_means(r, C):
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    k = py[py["child"] & py["age"].between(12, 20) & py["pid"].isin(r["pid"].unique())][["pid", "wave", "int"]]
    k = k.merge(C, on=["wave", "int"])
    return k.groupby("pid")[["total", "home", "bus", "other"]].mean().reset_index()


def forms(one, cols, by="birth_year"):
    for v in cols:
        one[f"{v}_rank"] = one.groupby(by)[v].rank(pct=True)
        one[f"{v}_asinh"] = np.arcsinh(one[v] / 1000)
        pos = one[v] > 0
        one[f"{v}_log"] = np.where(pos, np.log(one[v].where(pos) / 1000), 0.0)
        one[f"{v}_np"] = (~pos).astype(float)
    return one


def run(d, G, BT, lab, groups_show):
    res = run_spec(d, ["ly"], G, BT, cells=CELLS)
    out = {}
    for k in CELLS:
        if k not in res:
            continue
        row = {"b0": est(res, k, "b0", 0)}
        for g in groups_show:
            if g in G:
                row[g] = est(res, k, f"c:{g}", 0, share=True)
        row["rest"] = est(res, k, "b", 0, share=True)
        out[LAB[k]] = row
        RES[f"{lab}|{LAB[k]}"] = {g: (list(map(float, v[:2])) if v else None) for g, v in row.items()}
    return out


def main():
    r, _, _ = R80.build()
    S = son_means(r, components())
    r = r.merge(S, on="pid", how="left")
    d = r[r["lw"].notna() & r["total"].notna()].copy()
    one = d.drop_duplicates("pid")[["pid", "birth_year", "fam68", "total", "home", "bus", "other"]].copy()
    one = forms(one, ["total", "home", "bus", "other"])
    one["src"] = (one["fam68"] < 3000).astype(float)
    src = forms(one[one["src"] == 1][["pid", "birth_year", "total"]].copy(), ["total"]).rename(
        columns={"total_rank": "total_rank_src"})[["pid", "total_rank_src"]]
    one = one.merge(src, on="pid", how="left")
    keep = [c for c in one.columns if c.endswith(("_rank", "_asinh", "_log", "_np", "_src"))] + ["src"]
    d = d.merge(one[["pid"] + keep], on="pid", how="left")
    base = {**{g: v for g, v in R75.GROUPS.items() if g != "structure"}, **R80.NEW,
            "structure": R75.GROUPS["structure"] + ["f_educ_na", "m_educ_na", "inc_na"]}
    BT = Boot(d["fam68"].to_numpy(), d["race"].to_numpy())
    show = ["wage", "wealth", "w_home", "w_bus", "w_other"]
    o1 = one
    md = ["# How parents' wealth enters the IGE split: functional form, components, sample (committee memo K1)", "",
          "Built by `121.WealthMeasures.py` (2026-10-24); design in its docstring. 98's sons, son-years and split B; "
          "share of the IGE of ln earnings (percent; s.e.; p) from 200 cluster-bootstrap draws of 1968 families; "
          "*** p<0.01, ** p<0.05, * p<0.1. **Descriptive accounting.**", "",
          f"Sons {len(o1):,} (SRC {int(o1['src'].sum()):,}). Parental net worth (2000 dollars): median "
          f"{o1['total'].median():,.0f}; p90 {o1['total'].quantile(0.9):,.0f}; p99 {o1['total'].quantile(0.99):,.0f}; "
          f"share <= 0 {(o1['total'] <= 0).mean():.3f}. Housing median {o1['home'].median():,.0f}; business > 0 "
          f"{(o1['bus'] > 0).mean():.3f}; other median {o1['other'].median():,.0f}. Means: total "
          f"{o1['total'].mean():,.0f} = housing {o1['home'].mean():,.0f} + business {o1['bus'].mean():,.0f} + other "
          f"{o1['other'].mean():,.0f}.", ""]
    specs = [("no wealth (split B)", d, base),
             ("total: rank (98)", d, {**base, "wealth": ["total_rank"]}),
             ("total: asinh", d, {**base, "wealth": ["total_asinh"]}),
             ("total: ln + non-positive flag", d, {**base, "wealth": ["total_log", "total_np"]}),
             ("components: ranks", d, {**base, "w_home": ["home_rank"], "w_bus": ["bus_rank"],
                                       "w_other": ["other_rank"]}),
             ("components: asinh", d, {**base, "w_home": ["home_asinh"], "w_bus": ["bus_asinh"],
                                       "w_other": ["other_asinh"]})]
    ds = d[d["src"] == 1].copy()
    BTs = Boot(ds["fam68"].to_numpy(), ds["race"].to_numpy())
    md += ["| specification | cell | IGE | parents' wage share | wealth share | housing | business | other | rest |",
           "|---" * 9 + "|"]

    def emit(lab, out):
        for cell, row in out.items():
            md.append(f"| {lab} | {cell} | {cc(row['b0'])} | {cc(row.get('wage'))} | {cc(row.get('wealth'))} | "
                      f"{cc(row.get('w_home'))} | {cc(row.get('w_bus'))} | {cc(row.get('w_other'))} | "
                      f"{cc(row['rest'])} |")
        print("\n".join(md[-len(out):]), flush=True)

    for lab, q, G in specs:
        emit(lab, run(q, G, BT, lab, show))
    for lab, G in (("SRC only: no wealth", base), ("SRC only: total rank (within SRC)", {**base, "wealth": ["total_rank_src"]}),
                   ("SRC only: total asinh", {**base, "wealth": ["total_asinh"]})):
        emit(lab, run(ds, G, BTs, lab, show))
    md.append("")
    (OUT / "wealth_measures.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "wealth_measures.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
