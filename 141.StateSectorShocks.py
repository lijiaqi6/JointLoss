r"""Layoffs the father did not choose, with state x sector demand shocks (committee re-read memo, action 12, 2026-10-24)

93 used national declines of the father's sector: first stage on his layoff share 0.030* with F = 2.9 (too weak). A
shock to his sector in his own state varies more. Employment by state x sector x year from the CPS MORG files
(8a.StateShocks.py's morg_cells(), men and women, 16 sectors, 1979-2019; cached).
SHOCK: over the son's income years 13-18 (from 1980), the share of years in which the father's sector (93's sector,
  measured before the window) lost employment in the family's state (state of the window wave, 18's cache), with the
  state x sector cell's growth = ln E_t - ln E_{t-1} (cells with >= 30 respondents in both years; otherwise missing).
DESIGN (75's sons, father present, sector known and not agriculture, >= 3 window years with the shock):
  first stage, one row per son: teen layoff share on the shock, sector, state-at-17 and birth-year FE (PSID weights,
  clusters state x sector); F; reduced form within son: ln earnings on shock x (age-40)/10, son FE, single-age dummies,
  sector x age and 5-year cohort x age.
Writes output/state_sector_shocks.md / .json (aggregates only); caches data/morg_state_sector_cells.pkl. DESCRIPTIVE.
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


R93 = _load("s93", "93.LayoffIndustryShocks.py")
R8a = _load("s8a", "8a.StateShocks.py")
R101 = _load("s101", "101.EITCByAge.py")
R75, R72 = R101.R75, R101.R72
c, ols, dummies = R101.c, R101.ols, R101.dummies
CACHE = DATA / "morg_state_sector_cells.pkl"
RES = {}


def cells():
    if CACHE.exists():
        return pd.read_pickle(CACHE)
    rows = []
    for yy in list(range(79, 100)) + list(range(0, 20)):
        d = R8a.read_morg(yy)
        e = d[d["emp"]].dropna(subset=["sec"])
        g = e.groupby(["year", "fips", "sec"]).agg(E=("weight", "sum"), n=("weight", "size")).reset_index()
        rows.append(g)
        print(f"  MORG {int(d['year'].iloc[0])}: {len(e):,}", flush=True)
    C = pd.concat(rows, ignore_index=True)
    C.to_pickle(CACHE)
    return C


def main():
    C = cells().sort_values(["fips", "sec", "year"])
    prev = C.groupby(["fips", "sec"])[["E", "n", "year"]].shift(1)
    ok = (prev["year"] == C["year"] - 1) & (C["n"] >= 30) & (prev["n"] >= 30)
    C["decl"] = (np.log(C["E"]) < np.log(prev["E"])).astype(float).where(ok)
    D = {(int(f), int(s), int(y)): v for f, s, y, v in zip(C["fips"], C["sec"], C["year"], C["decl"]) if pd.notna(v)}
    r = R75.build()
    r = R72.state17(r)
    S = R93.father_sector(r)[["pid", "h_sec"]]
    r = r.merge(S, on="pid", how="left")
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    st = pd.read_pickle(DATA / "husband_shocks_fam.pkl")[["wave", "int", "fips"]].drop_duplicates(["wave", "int"])
    one = r.drop_duplicates("pid")[["pid", "birth_year", "h_sec", "nofa"]]
    one = one[(one["nofa"] == 0) & one["h_sec"].notna() & (one["h_sec"] != 0)]
    k = py[py["child"] & py["pid"].isin(one["pid"]) & py["age"].between(14, 19)][["pid", "wave", "int"]]
    k = k.merge(st, on=["wave", "int"], how="left").merge(one, on="pid")
    k["year"] = k["wave"] - 1
    k["shock"] = [D.get((int(f), int(s), int(y))) if pd.notna(f) else None for f, s, y in zip(k["fips"], k["h_sec"], k["year"])]
    k["shock"] = pd.to_numeric(k["shock"], errors="coerce")
    g = k.groupby("pid")["shock"].agg(["mean", "count"])
    sh = g[g["count"] >= 3]["mean"].rename("ss_decl")
    r = r.merge(sh, left_on="pid", right_index=True, how="inner")
    o = r.drop_duplicates("pid").copy()
    o["st17"] = o["fips17"].fillna(-1).astype(int)
    o["cl"] = o["st17"].astype(str) + "_" + o["h_sec"].astype(int).astype(str)
    md = ["# Layoffs the father did not choose: state x sector demand shocks (committee re-read memo, action 12)", "",
          "Built by `141.StateSectorShocks.py` (2026-10-24); design in its docstring. *** p<0.01, ** p<0.05, * p<0.1. "
          "**Descriptive / quasi-experimental.**", "",
          f"Sons {len(o):,} (born {int(o['birth_year'].min())}-{int(o['birth_year'].max())}); mean share of teen years with "
          f"a decline of the father's sector in his state {o['ss_decl'].mean():.3f} (s.d. {o['ss_decl'].std():.3f}).", "",
          "## First stage (one row per son)", "", "| outcome | shock | F | sons |", "|---|---|---|---|"]
    for y in ("f_sh_layoff", "f_sh_close", "f_sh_unemp"):
        X = np.column_stack([o["ss_decl"].to_numpy(float), dummies(o["h_sec"]), dummies(o["st17"]), dummies(o["birth_year"]),
                             np.ones(len(o))])
        b, V = ols(X, o[y].to_numpy(float), o["wt"].to_numpy(float), o["cl"].to_numpy())
        F = float((b[0] / np.sqrt(V[0, 0])) ** 2)
        md.append(f"| {y} | {c((b[0], np.sqrt(V[0, 0])))} | {F:.1f} | {len(o):,} |")
        RES[f"fs|{y}"] = {"b": float(b[0]), "se": float(np.sqrt(V[0, 0])), "F": F}
    v = r[r["lw"].notna()].copy()
    v["agec"] = (v["age"] - 40) / 10
    v["coh5"] = (v["birth_year"] // 5 * 5).astype(int)
    a = v["agec"].to_numpy()[:, None]
    X = np.column_stack([(v["ss_decl"] * v["agec"]).to_numpy(float), dummies(v["h_sec"]) * a, dummies(v["coh5"]) * a,
                         dummies(v["age"])])
    b, V = ols(X, v["ly"].to_numpy(float), v["wt"].to_numpy(float), v["fam68"].to_numpy(), absorb=v["pid"].to_numpy())
    md += ["", "## Reduced form within son (ln earnings)", "",
           f"Shock x (age-40)/10: {c((b[0], np.sqrt(V[0, 0])))}; {v['pid'].nunique():,} sons, {len(v):,} son-years; "
           f"oldest son-years at age {int(v['age'].max())}.", ""]
    RES["rf"] = [float(b[0]), float(np.sqrt(V[0, 0]))]
    (OUT / "state_sector_shocks.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "state_sector_shocks.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
