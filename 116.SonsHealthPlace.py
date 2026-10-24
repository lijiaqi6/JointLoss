r"""What lowers the pay of sons of laid-off fathers in midlife: their health or their place? (Paper B exploration,
2026-10-24; Section 6's open question)

At equal schooling most of the delayed cost of a father's teen layoff is a lower wage within the son's occupation after
40 (106, 115). Two candidates the public PSID can measure:
  HEALTH  the son's self-rated health as head (1984+: 'HEALTH NOW-HEAD', 'STATUS OF HEALTH-HEAD', 'H1 HEALTH STATUS-HEAD
          / -RP'; 1 excellent ... 5 poor; fair or poor = 4-5) and whether health limits the type or amount of his work
          (1994+: 'H2 LIMIT TYPE/AMT WRK', yes = 1), read from the family files with 18's reader.
  PLACE   whether the son lives in the state he lived in at 17 (72's state17; family's state by wave from 18's
          husband_shocks_fam, 1976+), and the unemployment rate of the state he lives in (LAUS).
For each: the teen layoff coefficient at 25-29 and 45-49 and its change (91's band_fit, at equal ln parental income and
all of 75's components, 200 draws) and the within-son slope (91's fe_fit); then the within-son ln earnings and ln wage
slopes of the layoff share with each candidate (time-varying) added as a control, to see how much of the bend it
carries. 75's baseline sample, PSID weights. DESCRIPTIVE.
Writes output/sons_health_place.md / .json (aggregates only); caches data/sons_health_items.pkl (family-level).
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


R91 = _load("s91", "91.LayoffSelection.py")
R18 = _load("s18", "18.HusbandIndustryShocks.py")
R75, R72 = R91.R75, R91.R75.R72
c, fmt, sd, Boot = R91.c, R91.fmt, R91.sd, R91.Boot
COMPS, STRUCT = R91.COMPS, R91.STRUCT
CACHE = DATA / "sons_health_items.pkl"
HPAT = [r"HEALTH NOW-HEAD", r"STATUS OF HEALTH-HEAD", r"^H1 HEALTH STATUS-(HEAD|RP)$", r"HEALTH STATUS-(HEAD|HD|RP)"]
LPAT = [r"LIMIT TYPE/AMT WRK[- ]*H$", r"WTR LIMIT TYPE/AMT WRK-? ?(HEAD|RP)", r"LIMIT TYPE/AMT WRK.*(HD|HEAD|RP)"]
RES = {}


def items():
    if CACHE.exists():
        return pd.read_pickle(CACHE)
    out = []
    for w in [x for x in R18.FS.WAVES if x >= 1984]:
        folder = R18.FAM / (f"fam{w}" if w < 1994 else f"fam{w}er")
        do = next(f for f in folder.glob("*.do") if "formats" not in f.name)
        pos, labs = R18.layout(do)
        idv = labs[1][0]
        hv = next((v for p in HPAT for v, l in labs if re.search(p, l)), None)
        lv = next((v for p in LPAT for v, l in labs if re.search(p, l)), None) if w >= 1994 else None
        cols = [idv] + [x for x in (hv, lv) if x]
        f = R18.read(do.with_suffix(".txt"), cols, pos).rename(columns={idv: "int", **({hv: "hlth"} if hv else {}),
                                                                        **({lv: "lim"} if lv else {})})
        f["wave"] = w
        for k in ("hlth", "lim"):
            if k not in f:
                f[k] = np.nan
        print(f"  {w}: health {hv}, limit {lv}", flush=True)
        out.append(f[["wave", "int", "hlth", "lim"]])
    F = pd.concat(out, ignore_index=True)
    F.to_pickle(CACHE)
    return F


def main():
    r = R75.build()
    F = items()
    r = r.merge(F, on=["wave", "int"], how="left")
    r["fairpoor"] = r["hlth"].isin([4, 5]).astype(float).where(r["hlth"].between(1, 5))
    r["limited"] = (r["lim"] == 1).astype(float).where(r["lim"].isin([1, 5]))
    st = pd.read_pickle(DATA / "husband_shocks_fam.pkl")[["wave", "int", "fips"]].drop_duplicates(["wave", "int"])
    r = r.merge(st, on=["wave", "int"], how="left")
    r = R72.state17(r)
    r["stayer"] = (r["fips"] == r["fips17"]).astype(float).where(r["fips"].notna() & r["fips17"].notna())
    ur = pd.read_pickle(DATA / "state_shocks.pkl")[["fips", "year", "ur"]]
    r["iyear"] = (r["wave"] - 1).astype(int)
    r = r.merge(ur.rename(columns={"year": "iyear", "ur": "st_ur"}), on=["fips", "iyear"], how="left")
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    cohd = pd.get_dummies(r["coh5"], prefix="coh", drop_first=True).astype(float)
    r = pd.concat([r, cohd], axis=1)
    r["agec"] = (r["age"] - 40) / 10
    XB = R91.xage(r, ["lyp"] + COMPS + STRUCT + list(cohd.columns))
    BT = Boot(r["fam68"].to_numpy(), r["race"].to_numpy())
    md = ["# What lowers the pay of sons of laid-off fathers in midlife: health or place?", "",
          "Built by `116.SonsHealthPlace.py` (2026-10-24); design in its docstring. Coefficient of the father's teen layoff "
          "share (per unit share). *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**", "",
          "## 1. The candidates as outcomes", "",
          "| outcome | mean | 25-29 | 45-49 | change | within son x age | sons |", "|---|---|---|---|---|---|---|"]
    for y, lab in (("fairpoor", "fair or poor health (1984+)"), ("limited", "health limits his work (1994+)"),
                   ("stayer", "lives in his state at 17"), ("st_ur", "unemployment rate of his state")):
        q = r.dropna(subset=[y])
        a0 = R91.band_fit(q, y, 0, BT, COMPS, ["f_sh_layoff"]).get("f_sh_layoff")
        a4 = R91.band_fit(q, y, 4, BT, COMPS, ["f_sh_layoff"]).get("f_sh_layoff")
        ch = (a4[0] - a0[0], a4[1] - a0[1]) if a0 and a4 else None
        f = R91.fe_fit(q, y, XB)
        fe = (f["b"]["f_sh_layoff_xa"], float(np.sqrt(f["V"].loc["f_sh_layoff_xa", "f_sh_layoff_xa"])))
        md.append(f"| {lab} | {np.average(q[y], weights=q['wt']):.3f} | {fmt(a0)} | {fmt(a4)} | {fmt(ch)} | {c(fe)} | "
                  f"{q['pid'].nunique():,} |")
        RES[f"outcome|{y}"] = {"a": [float(a0[0]), sd(a0[1])] if a0 else None, "b": [float(a4[0]), sd(a4[1])] if a4 else None,
                               "ch": [float(ch[0]), sd(ch[1])] if ch else None, "fe": list(map(float, fe))}
    md.append("")
    # 2. the earnings / wage bend with each candidate held fixed (on the son-years where it is measured)
    md += ["## 2. The within-son layoff slope with each candidate held fixed (time-varying control)", "",
           "| outcome | candidate | sample: as before | + candidate | candidate's own coefficient | son-years |",
           "|---|---|---|---|---|---|"]
    for y in ("ly", "lw"):
        for cand, lab in (("fairpoor", "fair or poor health"), ("limited", "health limits work"),
                          ("stayer", "lives in his state at 17"), ("st_ur", "state unemployment rate")):
            q = r[r["lw"].notna()].dropna(subset=[cand]).copy()
            f0 = R91.fe_fit(q, y, XB)
            f1 = R91.fe_fit(q, y, XB + [cand])
            g = lambda f, x: (f["b"][x], float(np.sqrt(f["V"].loc[x, x])))  # noqa: E731
            md.append(f"| {y} | {lab} | {c(g(f0, 'f_sh_layoff_xa'))} | {c(g(f1, 'f_sh_layoff_xa'))} | {c(g(f1, cand))} | "
                      f"{f1['n']:,} |")
            RES[f"control|{y}|{cand}"] = {"base": list(g(f0, "f_sh_layoff_xa")), "with": list(g(f1, "f_sh_layoff_xa")),
                                         "own": list(g(f1, cand))}
    md.append("")
    (OUT / "sons_health_place.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "sons_health_place.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
