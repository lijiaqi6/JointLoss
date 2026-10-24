r"""Recall or permanent separation? And the father's job held fixed (committee memo Z1, 2026-10-24)

The costly layoffs are repeated, with small income losses, short unemployment and UI received, in fathers who are laid
off again (91, 104): the signature of a temporary layoff with recall in a cyclical job. If so, 'the father's unstable
employment' may be 'a father in a recall-layoff job', and what is passed on is the job, not the man. Two tests:
(i) split the teen layoff share into layoffs after which the father went back to an employer he had before the job
ended (recall) and layoffs after which he works for a new employer (permanent); (ii) hold the father's sector,
occupation group and union membership fixed, each interacted with the son's age, and estimate the cost by sector.

RECALL. For each father layoff record of 75's share (psid_displacement.pkl: main and not strict, dated to the calendar
year y the job ended), his employer tenure at his later interviews w' in y+1 .. y+3 (male head; first decisive one):
  recall      tenure_lo > (w' - y) + 0.3  (his present employer predates the job end; interviews are in spring)
  new         tenure_hi < (w' - y) - 0.7, or self-employed at w'  (the employer started after the job end)
  unknown     otherwise (no interview with tenure, ambiguous category, not working)
Tenure with the present employer (years; [lo, hi] bounds from the codes):
  1968 V200 (<0.5, 0.58-1.5, 1.58-3.5, 4-9, 10-19, 20+ years); 1969-73 'how long have you had this job' V642, V1281,
  V1987, V2585, V3118 and 1975 V3984 (<1, 1-1.58, 1.58-3.5, 4-9, 10-19, 20+); 1976 V4480, 1977 V5384 / V5392, 1981-83
  V7711, V8379, V9010 (months with the present employer); 1979-80 V6499, V7102 (months in the present position: a lower
  bound only); 1984+ 27.CareerWageGrowth.py's cache (years); 1974 and 1978 have no item for all heads.
  Direct item, 1981-83 (spells of 1980-82): 'did you eventually return to the same employer?' (E: V7779, V8444, V9075;
  U: V7852, V8516, V9159; 1 yes -> recall, 5 no / 7 still looking -> new), used where present and to validate the rule.
The share of the son's teen waves with a layoff is split into recall + new + unknown parts (they sum to it).
FATHER'S JOB (measured before the window where possible, as 93: earliest head-wave at the son's 10-13, else 14-19):
  sector  16 sectors of 8a (93.LayoffIndustryShocks.father_sector)
  occupation  nine major groups of his 3-digit code (1970 Census codes to 2001, 2000 / 2010 codes after;
              23's cache h_occ): professional, managers, sales, clerical, craft, operatives (incl. transport),
              laborers, farm, service
  union   member (or job covered, 1976+) in any head-wave at the son's 10-19: 1969-72 V766, V1434, V2145, V2787, 1975
          V4087; 1976+ 118's items
DESIGNS (75's baseline sample, son-years with a valid wage; 91's band_fit / fe_fit, 200 common draws):
  1. counts: the three parts; validation against the direct item.
  2. band coefficients at 25-29 and 45-49, the change, and within-son slopes of the three parts; equality of recall and new.
  3. the within-son slope and the band change with the father's sector, occupation and union (x age) held fixed.
  4. the within-son slope by the father's sector group (durable manufacturing; construction and mining; nondurable
     manufacturing, transport, utilities, communications; trade and services; public administration), one regression.
Writes output/layoff_recall.md / .json (aggregates only); caches data/layoff_recall_items.pkl (family-level).
DESCRIPTIVE.
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


R91 = _load("s91", "91.LayoffSelection.py")
R93 = _load("s93", "93.LayoffIndustryShocks.py")
R118 = _load("s118", "118.SonsEmployerType.py")
R119 = _load("s119", "119.FatherSelfEmployment.py")
R18, R75, R24 = R118.R18, R91.R75, R91.R24
c, fmt, sd, Boot = R91.c, R91.fmt, R91.sd, R91.Boot
COMPS, STRUCT = R91.COMPS, R91.STRUCT
CACHE = DATA / "layoff_recall_items.pkl"
CAT68 = {1: (0, 0.5), 2: (0.58, 1.5), 3: (1.58, 3.5), 4: (4, 10), 5: (10, 20), 6: (20, 60)}
CAT = {1: (0, 1), 2: (1, 1.58), 3: (1.58, 3.5), 4: (4, 10), 5: (10, 20), 6: (20, 60)}
TEN = {1968: (["V200"], "cat68"), 1969: (["V642"], "cat"), 1970: (["V1281"], "cat"), 1971: (["V1987"], "cat"),
       1972: (["V2585"], "cat"), 1973: (["V3118"], "cat"), 1975: (["V3984"], "cat"), 1976: (["V4480"], "mo"),
       1977: (["V5384", "V5392"], "mo"), 1979: (["V6499"], "pos"), 1980: (["V7102"], "pos"), 1981: (["V7711"], "mo"),
       1982: (["V8379"], "mo"), 1983: (["V9010"], "mo")}
SAME = {1981: ("V7779", "V7852"), 1982: ("V8444", "V8516"), 1983: ("V9075", "V9159")}
UNION = {1969: "V766", 1970: "V1434", 1971: "V2145", 1972: "V2787", 1975: "V4087"}
OCCN = ["professional", "managers", "sales", "clerical", "craft", "operatives", "laborers", "farm", "service"]
SGRP = {3: 0, 1: 1, 2: 1, 4: 2, 5: 2, 6: 2, 7: 3, 8: 3, 9: 3, 10: 3, 11: 3, 12: 3, 13: 3, 14: 3, 15: 4}
SGN = ["durable manufacturing", "construction, mining", "nondurable mfg, transport, utilities, communications",
       "trade and services", "public administration"]
RES = {}


def items():
    """wave x int: tenure bounds (years), direct same-employer answer (1 / 0), union member (1976-: none here)."""
    if CACHE.exists():
        return pd.read_pickle(CACHE)
    out = []
    for w in sorted(set(TEN) | set(SAME) | set(UNION)):
        do = next(f for f in (R18.FAM / f"fam{w}").glob("*.do") if "formats" not in f.name)
        pos, labs = R18.layout(do)
        idv = labs[1][0]
        vs = (TEN.get(w, ([], ""))[0] + list(SAME.get(w, ())) + ([UNION[w]] if w in UNION else []))
        f = R18.read(do.with_suffix(".txt"), [idv] + vs, pos)
        x = pd.DataFrame({"wave": w, "int": f[idv], "lo": np.nan, "hi": np.nan, "same": np.nan, "union": np.nan})
        if w in TEN:
            cols, kind = TEN[w]
            v = pd.to_numeric(f[cols[0]], errors="coerce")
            for extra in cols[1:]:
                v = v.where(v > 0, pd.to_numeric(f[extra], errors="coerce"))
            if kind in ("cat68", "cat"):
                B = CAT68 if kind == "cat68" else CAT
                x["lo"] = v.map({k: b[0] for k, b in B.items()})
                x["hi"] = v.map({k: b[1] for k, b in B.items()})
            else:
                m = v.where(v.between(1, 998))
                x["lo"] = (m - 0.5).clip(lower=0) / 12
                x["hi"] = np.inf if kind == "pos" else (m + 0.5) / 12
                if kind == "mo":
                    x.loc[m == 998, "hi"] = np.inf
        if w in SAME:
            e, u = (pd.to_numeric(f[k], errors="coerce") for k in SAME[w])
            s = e.where(e.isin([1, 5]), u.where(u.isin([1, 5, 7])))
            x["same"] = (s == 1).astype(float).where(s.notna())
        if w in UNION:
            un = pd.to_numeric(f[UNION[w]], errors="coerce")
            x["union"] = (un == 1).astype(float).where(un.isin([1, 5]))
        print(f"  {w}: tenure {int(x['lo'].notna().sum()):,}; same-employer {int(x['same'].notna().sum()):,}; "
              f"union {int(x['union'].notna().sum()):,}", flush=True)
        out.append(x)
    F = pd.concat(out, ignore_index=True)
    F.to_pickle(CACHE)
    return F


def tenure_all():
    F = items()
    L = pd.read_pickle(DATA / "career_wage_growth_psid.pkl")[["wave", "int", "tenure"]]
    L = L[L["wave"] >= 1984].dropna(subset=["tenure"])
    t = L["tenure"]
    L = L.assign(lo=np.where(t >= 1, t - 0.1, (t - 0.05).clip(lower=0)), hi=np.where(t >= 1, t + 1.0, t + 0.1))
    T = pd.concat([F.dropna(subset=["lo"])[["wave", "int", "lo", "hi"]], L[["wave", "int", "lo", "hi"]]],
                  ignore_index=True)
    return T, F


def classify(dp, py, T, F, X):
    """class of each layoff record: 'recall', 'new', 'unknown'; plus the validation table."""
    hd = py[py["head"]][["pid", "wave", "int"]].drop_duplicates(["pid", "wave"])
    hd = hd.merge(T, on=["wave", "int"], how="left").merge(X, on=["wave", "int"], how="left")
    hd = hd.merge(F[["wave", "int", "same"]].dropna(), on=["wave", "int"], how="left")
    H = {p: g.sort_values("wave") for p, g in hd.groupby("pid")}
    L = dp[(dp["main"] == 1) & (dp["strict"] != 1)][["pid", "year"]].drop_duplicates()
    cls, rule, direct = [], [], []
    for p, y in zip(L["pid"], L["year"]):
        g = H.get(p)
        k, kr, kd = "unknown", "unknown", np.nan
        if g is not None:
            d = g[g["wave"] == y + 1]
            if len(d) and d["same"].notna().any():
                kd = float(d["same"].dropna().iloc[0])
            for _, row in g[(g["wave"] > y) & (g["wave"] <= y + 3)].iterrows():
                gap = row["wave"] - y
                if row.get("se") == 1:
                    kr = "new"
                    break
                if np.isfinite(row["lo"]) and row["lo"] > gap + 0.3:
                    kr = "recall"
                    break
                if np.isfinite(row["hi"]) and row["hi"] < gap - 0.7:
                    kr = "new"
                    break
            k = kr if np.isnan(kd) else ("recall" if kd == 1 else "new")
        cls.append(k), rule.append(kr), direct.append(kd)
    L = L.assign(cls=cls, rule=rule, direct=direct)
    return L


def shares(r, L):
    """per son: the teen layoff share split by the class of the layoff record (75's matching: year wave-1 or wave-2)."""
    a = pd.read_pickle(R24.CACHE)
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    sons = r.drop_duplicates("pid")[["pid", "fpid", "birth_year"]]
    k = py[py["child"] & py["age"].between(13, 19) & py["faminc"].between(R24.LO, R24.HI) & py["pid"].isin(sons["pid"])][
        ["pid", "wave", "int"]]
    fa = a[a["head"] & (a["female"] == 0)][["pid", "wave"]].rename(columns={"pid": "fpid"}).drop_duplicates()
    fw = k.merge(sons[["pid", "fpid"]].dropna(), on="pid").merge(fa, on=["fpid", "wave"])
    C = dict(zip(zip(L["pid"], L["year"]), L["cls"]))
    rank = {"new": 2, "recall": 1, "unknown": 0}
    lab = []
    for p, w in zip(fw["fpid"], fw["wave"]):
        cs = [C[q] for q in ((p, w - 1), (p, w - 2)) if q in C]
        lab.append(max(cs, key=lambda s: rank[s]) if cs else "")
    fw["cls"] = lab
    n = fw.groupby("pid").size()
    out = pd.DataFrame(index=n.index)
    for k_ in ("recall", "new", "unknown"):
        out[f"lay_{k_}"] = (fw["cls"] == k_).groupby(fw["pid"]).sum() / n
    out.index.name = "pid"
    return out.reset_index(), fw


def occ_group(code, wave):
    c_ = pd.to_numeric(code, errors="coerce")
    g = pd.Series(np.nan, index=c_.index)
    old = wave <= 2001
    for lo, hi, k in ((1, 195, 0), (201, 245, 1), (260, 285, 2), (301, 395, 3), (401, 600, 4), (601, 715, 5),
                      (740, 785, 6), (801, 824, 7), (901, 984, 8)):
        g[old & c_.between(lo, hi)] = k
    n = c_.where(wave <= 2015, c_ / 10)
    for lo, hi, k in ((1, 95, 1), (100, 354, 0), (360, 465, 8), (470, 496, 2), (500, 593, 3), (600, 613, 7),
                      (620, 762, 4), (770, 975, 5)):
        g[~old & n.between(lo, hi)] = k
    return g


def father_job(r, py, F):
    """per son: father's occupation group (pre-window where possible) and union membership at the son's 10-19."""
    a = pd.read_pickle(R24.CACHE)
    fa = a[a["head"] & (a["female"] == 0)][["pid", "wave", "int"]].rename(columns={"pid": "fpid"}).drop_duplicates()
    X = pd.read_pickle(DATA / "correlated_shocks_fam.pkl")["X"][["wave", "int", "h_occ"]]
    X["occ"] = occ_group(X["h_occ"], X["wave"])
    U = R118.items()[["wave", "int", "cov", "mem"]]
    cov, mem = U["cov"].where(U["cov"].isin([1, 5])), U["mem"].where(U["mem"].isin([1, 5]))
    U["union"] = np.fmax((cov == 1).astype(float).where(cov.notna()), (mem == 1).astype(float).where(mem.notna()))
    U = pd.concat([F[["wave", "int", "union"]].dropna(), U[["wave", "int", "union"]].dropna()], ignore_index=True)
    sons = r.drop_duplicates("pid")[["pid", "fpid", "birth_year"]].dropna()
    rows = sons.merge(fa, on="fpid")
    rows["off"] = rows["wave"] - 1 - rows["birth_year"]
    rows = rows[rows["off"].between(10, 19)].merge(X[["wave", "int", "occ"]], on=["wave", "int"], how="left")
    rows = rows.merge(U.drop_duplicates(["wave", "int"]), on=["wave", "int"], how="left")
    o = rows.dropna(subset=["occ"]).sort_values("wave")
    pre = o[o["off"] <= 13].groupby("pid")["occ"].first()
    occ = pre.combine_first(o.groupby("pid")["occ"].first())
    un = rows.dropna(subset=["union"]).groupby("pid")["union"].max()
    return pd.DataFrame({"f_occ": occ, "f_union": un})


def main():
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    T, F = tenure_all()
    X = R119.head_se()
    dp = pd.read_pickle(DATA / "psid_displacement.pkl")
    L = classify(dp, py, T, F, X)
    r = R75.build()
    S, fw = shares(r, L)
    r = r.merge(S, on="pid", how="left")
    pres = r["nofa"] == 0
    parts = ["lay_recall", "lay_new", "lay_unknown"]
    for v in parts:
        r[v] = r[v].where(pres, 0.0).fillna(0.0)
    # father's job
    sec = R93.father_sector(r)[["pid", "h_sec"]]
    r = r.merge(sec, on="pid", how="left")
    r = r.merge(father_job(r, py, F), left_on="pid", right_index=True, how="left")
    r["sgrp"] = r["h_sec"].map(SGRP)
    dums = []
    for nm, col, K in (("sec", "h_sec", 16), ("occ", "f_occ", 9)):
        for k in range(1, K):
            r[f"{nm}{k}"] = (r[col] == k).astype(float)
            dums.append(f"{nm}{k}")
        r[f"{nm}_na"] = (pres & r[col].isna()).astype(float)
        dums.append(f"{nm}_na")
    r["union_na"] = (pres & r["f_union"].isna()).astype(float)
    r["f_union"] = r["f_union"].fillna(0.0).where(pres, 0.0)
    dums += ["f_union", "union_na"]
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    cohd = pd.get_dummies(r["coh5"], prefix="coh", drop_first=True).astype(float)
    r = pd.concat([r, cohd], axis=1)
    r["agec"] = (r["age"] - 40) / 10
    XB = R91.xage(r, ["lyp"] + COMPS + STRUCT + list(cohd.columns))
    XP = R91.xage(r, parts)
    XJ = R91.xage(r, dums)
    for g in range(5):
        r[f"lay_s{g}"] = r["f_sh_layoff"] * (r["sgrp"] == g)
    r["lay_sna"] = r["f_sh_layoff"] * r["sgrp"].isna() * pres
    XG = R91.xage(r, [f"lay_s{g}" for g in range(5)] + ["lay_sna"])
    v = r[r["lw"].notna()].copy()
    BT = Boot(v["fam68"].to_numpy(), v["race"].to_numpy())
    g_ = lambda f, x: (f["b"][x], float(np.sqrt(f["V"].loc[x, x])))  # noqa: E731
    md = ["# Recall or permanent separation? And the father's job held fixed (committee memo Z1)", "",
          "Built by `120.LayoffRecall.py` (2026-10-24); design in its docstring. Per unit teen layoff share; band s.e. "
          "from 200 cluster-bootstrap draws of 1968 families (common to all rows), within-son s.e. clustered by 1968 "
          "family. *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**", ""]

    # 1. counts and validation
    one = v[pres.loc[v.index]].drop_duplicates("pid")
    tw = fw[fw["cls"] != ""]
    md += ["## 1. The father's teen layoff years by what followed", "",
           "| | recall (back with a pre-layoff employer) | new employer | unknown | all |", "|---|---|---|---|---|"]
    cnt = {k: int((tw["cls"] == k).sum()) for k in ("recall", "new", "unknown")}
    md.append(f"| teen layoff years (son x wave) | {cnt['recall']:,} | {cnt['new']:,} | {cnt['unknown']:,} | "
              f"{len(tw):,} |")
    sons_k = {k: int((one[f"lay_{k}"] > 0).sum()) for k in ("recall", "new", "unknown")}
    md.append(f"| father-present sons with such a year | {sons_k['recall']:,} | {sons_k['new']:,} | "
              f"{sons_k['unknown']:,} | {int((one['f_sh_layoff'] > 0).sum()):,} |")
    t45 = {k: int(v[(v["band"] == 4) & (v[f"lay_{k}"] > 0)]["pid"].nunique()) for k in ("recall", "new", "unknown")}
    md.append(f"| ... observed at 45-49 | {t45['recall']} | {t45['new']} | {t45['unknown']} | "
              f"{int(v[(v['band'] == 4) & (v['f_sh_layoff'] > 0) & (v['nofa'] == 0)]['pid'].nunique())} |")
    RES["counts"] = {"years": cnt, "sons": sons_k, "sons45": t45}
    Lv = L.dropna(subset=["direct"])
    ct = pd.crosstab(Lv["direct"].map({1.0: "direct: same employer", 0.0: "direct: not"}), Lv["rule"])
    md += ["", "Validation on the layoff records of 1980-82 with the direct item (all male heads):", "",
           "| | rule: recall | rule: new | rule: unknown |", "|---|---|---|---|"]
    for i in ct.index:
        md.append(f"| {i} | " + " | ".join(str(int(ct.loc[i].get(k, 0))) for k in ("recall", "new", "unknown")) + " |")
    RES["validation"] = {i: {k: int(ct.loc[i].get(k, 0)) for k in ("recall", "new", "unknown")} for i in ct.index}
    allc = L["cls"].value_counts().to_dict()
    md += ["", f"All male-head layoff records: {', '.join(f'{k} {n:,}' for k, n in allc.items())}.", ""]
    print("\n".join(md), flush=True)

    # 2. recall vs new
    comps2 = [x for x in COMPS if x != "f_sh_layoff"] + parts
    XB2 = [x for x in XB if x != "f_sh_layoff_xa"] + XP
    md += ["## 2. Recall and new-employer layoffs (ln earnings, ln wage)", "",
           "| outcome | part | 25-29 | 45-49 | change | within son x age |", "|---|---|---|---|---|---|"]
    for y in ("ly", "lw"):
        g0 = R91.band_fit(v, y, 0, BT, comps2, parts)
        g4 = R91.band_fit(v, y, 4, BT, comps2, parts)
        f = R91.fe_fit(v, y, XB2)
        for p in parts:
            ch = (g4[p][0] - g0[p][0], g4[p][1] - g0[p][1])
            md.append(f"| {y} | {p[4:]} | {fmt(g0[p])} | {fmt(g4[p])} | {fmt(ch)} | {c(g_(f, p + '_xa'))} |")
            RES[f"parts|{y}|{p}"] = {"a": [float(g0[p][0]), sd(g0[p][1])], "b": [float(g4[p][0]), sd(g4[p][1])],
                                     "ch": [float(ch[0]), sd(ch[1])], "fe": list(map(float, g_(f, p + "_xa")))}
        chd = ((g4["lay_recall"][0] - g0["lay_recall"][0]) - (g4["lay_new"][0] - g0["lay_new"][0]),
               (g4["lay_recall"][1] - g0["lay_recall"][1]) - (g4["lay_new"][1] - g0["lay_new"][1]))
        W = R91.wald(f, [1, -1], ["lay_recall_xa", "lay_new_xa"])
        dfe = R91.lincom(f, {"lay_recall_xa": 1, "lay_new_xa": -1})
        md.append(f"| {y} | recall - new | | | {fmt(chd)} | {c(dfe)} (Wald p={W[2]:.3f}) |")
        RES[f"parts|{y}|diff"] = {"ch": [float(chd[0]), sd(chd[1])], "fe": list(dfe), "p": W[2]}
        print(md[-1], flush=True)
    md.append("")

    # 3. the father's job held fixed
    md += ["## 3. The layoff with the father's sector, occupation and union held fixed", "",
           "| outcome | controls | 25-29 | 45-49 | change | within son x age | sons |", "|---|---|---|---|---|---|---|"]
    secd = [d for d in dums if d.startswith("sec")]
    occd = [d for d in dums if d.startswith("occ")]
    unid = ["f_union", "union_na"]
    for y in ("ly", "lw"):
        for lab, ctrl in (("none", []), ("sector", secd), ("occupation", occd), ("union", unid),
                          ("sector + occupation + union", dums)):
            g0 = R91.band_fit(v, y, 0, BT, COMPS, ["f_sh_layoff"], ctrl)["f_sh_layoff"]
            g4 = R91.band_fit(v, y, 4, BT, COMPS, ["f_sh_layoff"], ctrl)["f_sh_layoff"]
            ch = (g4[0] - g0[0], g4[1] - g0[1])
            f = R91.fe_fit(v, y, XB + [f"{d}_xa" for d in ctrl])
            md.append(f"| {y} | {lab} | {fmt(g0)} | {fmt(g4)} | {fmt(ch)} | {c(g_(f, 'f_sh_layoff_xa'))} | "
                      f"{v['pid'].nunique():,} |")
            RES[f"job|{y}|{lab}"] = {"a": [float(g0[0]), sd(g0[1])], "b": [float(g4[0]), sd(g4[1])],
                                     "ch": [float(ch[0]), sd(ch[1])], "fe": list(map(float, g_(f, "f_sh_layoff_xa")))}
            print(md[-1], flush=True)
    md.append("")

    # 4. by sector group
    md += ["## 4. The within-son slope by the father's sector (one regression, ln earnings)", "",
           "| father's sector | layoff share x age | treated sons | treated at 45-49 | father-present sons |",
           "|---|---|---|---|---|"]
    XB4 = [x for x in XB if x != "f_sh_layoff_xa"] + XG + [f"{d}_xa" for d in secd]
    for y in ("ly", "lw"):
        f = R91.fe_fit(v, y, XB4)
        for gi, gn in enumerate(SGN + ["sector unknown"]):
            nm = f"lay_s{gi}_xa" if gi < 5 else "lay_sna_xa"
            q = one[(one["sgrp"] == gi)] if gi < 5 else one[one["sgrp"].isna()]
            tr = int((q["f_sh_layoff"] > 0).sum())
            qq = v[(v["band"] == 4) & (v["nofa"] == 0) & (v["f_sh_layoff"] > 0)]
            t4 = int(qq[(qq["sgrp"] == gi) if gi < 5 else qq["sgrp"].isna()]["pid"].nunique())
            est = g_(f, nm) if nm in f["b"] else (np.nan, np.nan)
            md.append(f"| {y}: {gn} | {c(est)} | {tr} | {t4} | {len(q):,} |")
            RES[f"sector|{y}|{gn}"] = {"fe": [float(est[0]), float(est[1])], "treated": tr, "treated45": t4}
        W = R91.wald(f, np.eye(5)[1:] - np.eye(5)[0], [f"lay_s{g}_xa" for g in range(5)])
        md.append(f"| {y}: equal across the five sectors | Wald p={W[2]:.3f} | | | |")
        RES[f"sector|{y}|equal_p"] = W[2]
    md.append("")
    (OUT / "layoff_recall.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "layoff_recall.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
