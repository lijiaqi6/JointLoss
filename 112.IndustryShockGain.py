r"""Why do sons of fathers whose industry declined in their teens do BETTER with age? (Fable round 2, Objection 5;
plan proposals/paperB_round2_plan_20261020.md, step 5)

93.LayoffIndustryShocks.py: the share of the son's 12-18 in which national employment of the father's sector fell has a
positive within-son reduced form on the son's ln earnings (+0.143**, three windows). Three readings:
  (a) AVOIDANCE: sons of fathers in declining sectors do not follow them into those sectors. Son-level: the son works
      in his father's sector at 25-34 (his modal sector, 18's industry_sector on his own codes) on the decline, sector
      and birth-year FE; and the within-son slope with 'in the father's sector' x age added.
  (b) COARSE CONTROLS: 15 sectors x age may leave industry-specific age profiles; add the father's detailed (3-digit
      1970 Census) industry x age.
  (c) THE ECONOMY AT ENTRY: sons whose fathers' sectors declined in their teens may have entered work in better national
      markets; add the national unemployment rate at the son's 22-25 x age (49's NATUR).
Same sample, weights and clusters as 93 (sector x birth year). Writes output/industry_shock_gain.md / .json.
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


R93 = _load("s93", "93.LayoffIndustryShocks.py")
R49 = _load("s49", "49.PaperBPolicyShocks.py")
R75, R18, R24 = R93.R75, R93.R18, R93.R24
c, dummies, ols = R93.c, R93.dummies, R93.ols
RES = {}


def father_code(r):
    F = R93.fam_sector_early()
    a = pd.read_pickle(R24.CACHE)
    fa = a[a["head"] & (a["female"] == 0)][["pid", "wave", "int"]].rename(columns={"pid": "fpid"}).drop_duplicates()
    fa = fa.merge(F, on=["wave", "int"], how="left").dropna(subset=["h_sec"])
    sons = r.drop_duplicates("pid")[["pid", "fpid", "birth_year"]].dropna()
    rows = sons.assign(key=1).merge(pd.DataFrame({"off": range(10, 20), "key": 1}), on="key")
    rows["wave"] = (rows["birth_year"] + rows["off"] + 1).astype(int)
    rows = rows.merge(fa, on=["fpid", "wave"]).sort_values("wave")
    first = rows.groupby("pid").first()
    first["h3"] = np.where(first["wave"] <= 2001, first["h_code"], np.nan)
    return first[["h3"]].reset_index()


def main():
    r = R75.build()
    r = r[(r["nofa"] == 0) & r["fpid"].notna()].copy()
    r = r.merge(R93.father_sector(r), on="pid", how="left")
    E, G = R93.ces_employment()
    one = r.drop_duplicates("pid").copy()
    sh = R93.shocks(one["h_sec"].to_numpy(), one["birth_year"].to_numpy(), G)
    sh["pid"] = one["pid"].to_numpy()
    r = r.merge(sh, on="pid", how="left").merge(father_code(r), on="pid", how="left")
    r = r[r["decl"].notna()].copy()
    r["s_sec"] = R18.industry_sector(r["icode"], r["wave"])
    e = r[r["age"].between(25, 34) & r["s_sec"].notna()].groupby("pid")["s_sec"].agg(lambda s: s.mode().iat[0])
    r["s_sec25"] = r["pid"].map(e)
    r["in_fsec"] = (r["s_sec25"] == r["h_sec"]).astype(float).where(r["s_sec25"].notna())
    r["entry_ur"] = [np.nanmean([R49.NATUR.get(int(b) + k, np.nan) for k in range(22, 26)]) for b in r["birth_year"]]
    r["cl"] = r["h_sec"].astype(int) * 10000 + r["birth_year"].astype(int)
    r["agec"] = (r["age"] - 40) / 10
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    md = ["# Why do sons of fathers in declining sectors do better with age? (Fable round 2, Objection 5)", "",
          "Built by `112.IndustryShockGain.py` (2026-10-20); design in its docstring. Clustered by sector x birth year. "
          "*** p<0.01, ** p<0.05, * p<0.1.", ""]
    # (a) avoidance, one row per son
    s1 = r.drop_duplicates("pid").dropna(subset=["in_fsec"])
    X = np.column_stack([s1["decl"].to_numpy(float), dummies(s1["h_sec"]), dummies(s1["birth_year"]), np.ones(len(s1))])
    b, V, _ = ols(X, s1["in_fsec"].to_numpy(float), s1["wt"].to_numpy(float), s1["cl"].to_numpy())
    av = (b[0], np.sqrt(V[0, 0]))
    md += ["## (a) Do sons follow their fathers into declining sectors?", "",
           f"Son works in his father's sector at 25-34 (mean {np.average(s1['in_fsec'], weights=s1['wt']):.3f}, "
           f"{len(s1):,} sons) on the decline share: {c(av)}.", ""]
    RES["avoid"] = list(map(float, av))
    # within-son slopes under added controls
    v = r[r["lw"].notna()].copy()
    a_ = v["agec"].to_numpy()[:, None]
    base = [dummies(v["h_sec"]) * a_, dummies(v["coh5"]) * a_, (v["lyp"] * v["agec"]).to_numpy()[:, None], dummies(v["age"])]
    specs = [("as in 93", [])]
    v["in_fsec0"] = v["in_fsec"].fillna(0.0)
    v["in_na"] = v["in_fsec"].isna().astype(float)
    specs.append(("+ son in his father's sector x age", [np.column_stack([v["in_fsec0"], v["in_na"]]) * a_]))
    h3 = v["h3"].fillna(-1).astype(int)
    specs.append(("+ father's 3-digit industry x age", [dummies(h3) * a_]))
    v["entry_ur"] = v["entry_ur"].fillna(np.nanmean(v["entry_ur"]))
    specs.append(("+ national unemployment at the son's 22-25 x age", [(v["entry_ur"] * v["agec"]).to_numpy()[:, None]]))
    specs.append(("all three", [np.column_stack([v["in_fsec0"], v["in_na"]]) * a_, dummies(h3) * a_,
                                (v["entry_ur"] * v["agec"]).to_numpy()[:, None]]))
    md += ["## (b)-(c) The within-son reduced form under added controls (ln earnings; decline share x age)", "",
           "| controls | decline at 12-18 x age | N son-years / sons |", "|---|---|---|"]
    for lab, extra in specs:
        X = np.column_stack([(v["decl"] * v["agec"]).to_numpy()[:, None]] + base + extra)
        b, V, _ = ols(X, v["ly"].to_numpy(float), v["wt"].to_numpy(float), v["cl"].to_numpy(), absorb=v["pid"].to_numpy())
        md.append(f"| {lab} | {c((b[0], np.sqrt(V[0, 0])))} | {len(v):,} / {v['pid'].nunique():,} |")
        RES[lab] = [float(b[0]), float(np.sqrt(V[0, 0]))]
    md.append("")
    (OUT / "industry_shock_gain.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "industry_shock_gain.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
