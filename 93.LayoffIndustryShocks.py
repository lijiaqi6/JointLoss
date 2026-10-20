r"""Layoffs the father did not choose: national employment shocks to his industry in the son's teens (Fable A1).

Memo: proposals/fable_top5_distance_paperB_20261020.md, A1. The teen layoff share (75 / 88) is selected; here the
variation is the national employment change of the father's own sector during the son's teens, with sector and
birth-year fixed effects, so it is the sector-specific TIMING of demand shocks relative to the son's age - not which
sector the father is in, and not the national cycle.

DATA
  Father's sector: his 3-digit industry (1970 Census codes; PSID retrospective _A/_B variables 1968-80, main job
    1981-2001, 2000 / 2012 codes after; 18.HusbandIndustryShocks.py's family(), extended here to the 1968-75 family
    files with the same reader) mapped to the 16 sectors of 8a.StateShocks.py. Measured BEFORE the window where
    possible: the earliest wave in which the father is the male head at the son's wave-ages 10-13; else the earliest
    teen wave (so a post-layoff industry change does not define the sector).
  National employment: BLS Current Employment Statistics, annual averages (period M13) of all employees, not
    seasonally adjusted, 1939-2025, flat files in IGE_DATA/ext/bls_ces (download.bls.gov/pub/time.series/ce).
    Sector -> series: mining CEU10, construction CEU20, durable CEU31, nondurable CEU32, transportation and utilities =
    CEU40 - CEU41 - CEU42, communications CEU50 (information), wholesale CEU41, retail CEU42, eating / accommodation
    CEU70 (leisure and hospitality), FIRE CEU55, business / professional CEU60, personal and other services CEU80,
    health CEU65 (education and health), education = state + local government education (CEU9092161101 +
    CEU9093161101), public administration = government CEU90 minus government education. Agriculture: no CES series
    (farm employment is outside CES) -> sons of farm fathers dropped.
  Shock over calendar years b+12 .. b+18 (b = son's birth year; the income years of the window waves):
    decl  = share of the seven years in which the sector's national employment fell (comparable to the layoff share);
    grow  = mean annual growth, 100 x d ln employment.
  Placebo windows: b+5 .. b+11 (ages 5-11) and b+19 .. b+25 (ages 19-25).
SAMPLE: 75's son-years (R75.build()), father present, sector known and not agriculture.
DESIGN (weights wt; s.e. clustered by sector x birth year, the level of the shock; sector-clustered in a check)
  (1) first stage, one row per son: father's teen layoff share (and closure, unemployment shares) on the shock, sector FE,
      birth-year FE;
  (2) reduced form by band: son's ln earnings on the shock, sector FE, birth-year FE, single-age dummies (+ lyp in a
      check); 25-29, 45-49 and the change (stacked, every regressor interacted with the band);
  (3) within son: ln earnings on shock x (age-40)/10, son FE, single-age dummies, sector x age and 5-year cohort x age;
      placebo windows alongside; and 2SLS of the layoff share x age instrumented by the shock x age (the exclusion
      restriction fails if the shock acts through closures, unemployment or wages: the reduced form is the object).
DESCRIPTIVE / QUASI-EXPERIMENTAL. Writes output/layoff_industry_shocks.md / .json (aggregates only).
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


R75 = _load("s75", "75.WhatIsPassedOn.py")
R18 = _load("s18", "18.HusbandIndustryShocks.py")
R24, R73 = R75.R24, R75.R74.R73
CES = DATA / "ext" / "bls_ces"
SECT_CACHE = DATA / "layoff_industry_father_sector.pkl"
SER = {1: ["CEU1000000001"], 2: ["CEU2000000001"], 3: ["CEU3100000001"], 4: ["CEU3200000001"],
       5: ["CEU4000000001", "-CEU4142000001", "-CEU4200000001"], 6: ["CEU5000000001"], 7: ["CEU4142000001"],
       8: ["CEU4200000001"], 9: ["CEU7000000001"], 10: ["CEU5500000001"], 11: ["CEU6000000001"],
       12: ["CEU8000000001"], 13: ["CEU6500000001"], 14: ["CEU9092161101", "CEU9093161101"],
       15: ["CEU9000000001", "-CEU9092161101", "-CEU9093161101"]}
BLAB = ["25-29", "30-34", "35-39", "40-44", "45-49", "50-55"]
RES = {}


def stars(p):
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""


def c(t, dec=3):
    b, s = t
    p = 2 * stats.norm.sf(abs(b / s)) if s > 0 else np.nan
    return f"{b:.{dec}f}{stars(p)} ({s:.{dec}f}; p={'<0.001' if p < 0.001 else f'{p:.3f}'})"


def dummies(s):
    return pd.get_dummies(pd.Series(s).astype(int), drop_first=True).to_numpy(float)


# ================================================================ national employment by sector
def ces_employment():
    want = {s.lstrip("-") for v in SER.values() for s in v}
    rows = []
    for f in CES.glob("ce.data.*.Employment"):
        d = pd.read_csv(f, sep="\t", dtype=str)
        d.columns = [x.strip() for x in d.columns]
        d["series_id"] = d["series_id"].str.strip()
        d = d[d["series_id"].isin(want) & (d["period"].str.strip() == "M13")]
        rows.append(d[["series_id", "year", "value"]])
    d = pd.concat(rows).drop_duplicates(["series_id", "year"])
    d["year"] = d["year"].astype(int)
    d["value"] = pd.to_numeric(d["value"], errors="coerce")
    E = d.pivot(index="year", columns="series_id", values="value")
    out = pd.DataFrame(index=E.index)
    for sec, parts in SER.items():
        v = sum((-1 if p.startswith("-") else 1) * E[p.lstrip("-")] for p in parts)
        out[sec] = v
    g = 100 * np.log(out).diff()
    return out, g


# ================================================================ the father's sector
def fam_sector_early():
    """head's sector by (wave, int) for 1968-75 with 18's reader and 1976+ from 18's cached family()."""
    out = []
    for w in range(1968, 1976):
        folder = R18.FAM / f"fam{w}"
        do = next(f for f in folder.glob("*.do") if "formats" not in f.name)
        pos, labs = R18.layout(do)
        idv = labs[1][0]
        hv = R18.find(labs, R18.IND_PAT["h_ind"], w)
        f = R18.read(do.with_suffix(".txt"), [idv, hv[0]], pos).rename(columns={idv: "int", hv[0]: "h_code"})
        f["wave"] = w
        print(f"  family {w}: {len(f):,} families; head industry {hv[0]} '{hv[1]}'", flush=True)
        out.append(f)
    F = pd.concat(out, ignore_index=True)
    F["h_sec"] = R18.industry_sector(F["h_code"], F["wave"])
    L = R18.family()[["wave", "int", "h_code", "h_sec"]]
    return pd.concat([F[["wave", "int", "h_code", "h_sec"]], L], ignore_index=True)


def father_sector(r):
    if SECT_CACHE.exists():
        return pd.read_pickle(SECT_CACHE)
    F = fam_sector_early()
    a = pd.read_pickle(R24.CACHE)
    fa = a[a["head"] & (a["female"] == 0)][["pid", "wave", "int"]].rename(columns={"pid": "fpid"}).drop_duplicates()
    fa = fa.merge(F, on=["wave", "int"], how="left")
    sons = r.drop_duplicates("pid")[["pid", "fpid", "birth_year"]].dropna()
    rows = sons.assign(key=1).merge(pd.DataFrame({"off": range(10, 20), "key": 1}), on="key")
    rows["wave"] = (rows["birth_year"] + rows["off"] + 1).astype(int)
    rows = rows.merge(fa, on=["fpid", "wave"]).dropna(subset=["h_sec"])
    pre = rows[rows["off"] <= 13].sort_values("wave").groupby("pid").first()
    any_ = rows.sort_values("wave").groupby("pid").first()
    S = pre[["h_sec", "wave"]].rename(columns={"wave": "sec_wave"})
    S["sec_pre"] = 1.0
    rest = any_.loc[~any_.index.isin(S.index), ["h_sec", "wave"]].rename(columns={"wave": "sec_wave"})
    rest["sec_pre"] = 0.0
    S = pd.concat([S, rest])
    S.index.name = "pid"
    S = S.reset_index()
    S.to_pickle(SECT_CACHE)
    return S


def shocks(S, birth, G):
    out = {}
    for tag, lo, hi in (("", 12, 18), ("_pre", 5, 11), ("_post", 19, 25)):
        decl, grow = [], []
        for s, b in zip(S, birth):
            if np.isnan(s) or int(s) not in G.columns:
                decl.append(np.nan), grow.append(np.nan)
                continue
            x = G.loc[int(b) + lo:int(b) + hi, int(s)].dropna()
            ok = len(x) >= 5
            decl.append(float((x < 0).mean()) if ok else np.nan)
            grow.append(float(x.mean()) if ok else np.nan)
        out[f"decl{tag}"], out[f"grow{tag}"] = decl, grow
    return pd.DataFrame(out)


# ================================================================ estimation
def ols(X, y, w, g, absorb=None, Z=None):
    """weighted OLS (or 2SLS with instruments Z: same columns as X with the endogenous ones replaced) with cluster-robust
    covariance; absorb = FE ids (weighted within)."""
    if absorb is not None:
        M = R73.demean(np.column_stack([y, X] + ([Z] if Z is not None else [])), absorb, w)
        y, X = M[:, 0], M[:, 1:1 + X.shape[1]]
        if Z is not None:
            Z = M[:, 1 + X.shape[1]:]
    if Z is not None:                                       # 2SLS: project X on Z
        Zw = Z * w[:, None]
        P = np.linalg.pinv(Z.T @ Zw) @ Zw.T @ X
        Xh = Z @ P
    else:
        Xh = X
    Xw = Xh * w[:, None]
    XtXi = np.linalg.pinv(Xh.T @ (X * w[:, None]))
    b = XtXi @ Xw.T @ y
    u = y - X @ b
    S = pd.DataFrame(Xw * u[:, None]).groupby(g).sum().to_numpy()
    G, (n, k) = S.shape[0], X.shape
    V = XtXi @ (S.T @ S) @ XtXi.T * G / (G - 1) * (n - 1) / (n - k)
    return b, V, G


def main():
    r = R75.build()
    r = r[(r["nofa"] == 0) & r["fpid"].notna()].copy()
    S = father_sector(r)
    r = r.merge(S, on="pid", how="left")
    E, G = ces_employment()
    one = r.drop_duplicates("pid").copy()
    sh = shocks(one["h_sec"].to_numpy(), one["birth_year"].to_numpy(), G)
    sh["pid"] = one["pid"].to_numpy()
    r = r.merge(sh, on="pid", how="left")
    r = r[r["decl"].notna()].copy()
    r["cl"] = r["h_sec"].astype(int) * 10000 + r["birth_year"].astype(int)
    r["agec"] = (r["age"] - 40) / 10
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    one = r.drop_duplicates("pid").copy()
    n_sec = one.groupby("h_sec").size()
    md = ["# Layoffs the father did not choose: national employment shocks to his industry in the son's teens (Fable A1)",
          "", "Built by `93.LayoffIndustryShocks.py` (2026-10-20); design in its docstring. Father-present PSID sons; "
          "shock = share of the seven years at the son's 12-18 in which national (CES) employment of the father's sector "
          "fell (decl), or its mean annual growth in log points x 100 (grow); sector FE and birth-year FE throughout; "
          "PSID weights; estimate (s.e.; p) clustered by sector x birth year; *** p<0.01, ** p<0.05, * p<0.1.", "",
          f"Sons: {len(one):,} (sector measured before the son's 14th wave-age: {one['sec_pre'].mean():.0%}); "
          f"son-years {len(r):,}; sector x birth-year clusters {r['cl'].nunique():,}. Shock: decl mean "
          f"{np.average(one['decl'], weights=one['wt']):.3f} (s.d. {one['decl'].std():.3f}), grow mean "
          f"{np.average(one['grow'], weights=one['wt']):.2f} (s.d. {one['grow'].std():.2f}). Within sector and birth "
          f"year the s.d. of decl is {(one['decl'] - one.groupby('h_sec')['decl'].transform('mean') - one.groupby('birth_year')['decl'].transform('mean') + one['decl'].mean()).std():.3f}.",
          "", "Sons by sector: " + "; ".join(f"{R18.SNAMES[int(k)].split(' (')[0]} {v}" for k, v in n_sec.items()), ""]
    RES["n"] = {"sons": len(one), "son_years": len(r), "clusters": int(r["cl"].nunique())}
    secd = dummies(one["h_sec"])
    byd = dummies(one["birth_year"])
    # (1) first stage
    md += ["## 1. First stage: the father's teen spells on his industry's national decline (one row per son)", "",
           "| outcome | decl (share of decline years) | grow (mean growth, x100) | mean of outcome |", "|---|---|---|---|"]
    for y, lab in (("f_sh_layoff", "layoff share 13-19"), ("f_sh_close", "closure share 13-19"),
                   ("f_sh_unemp", "unemployment share 13-19"), ("f_lw", "father's ln wage (window mean)"),
                   ("lyp", "ln parental income")):
        cells = []
        for sv in ("decl", "grow"):
            X = np.column_stack([one[sv].to_numpy(float), secd, byd, np.ones(len(one))])
            b, V, _ = ols(X, one[y].to_numpy(float), one["wt"].to_numpy(float), one["cl"].to_numpy())
            cells.append((b[0], np.sqrt(V[0, 0])))
            RES[f"fs|{y}|{sv}"] = [float(b[0]), float(np.sqrt(V[0, 0]))]
        md.append(f"| {lab} | {c(cells[0])} | {c(cells[1], 4)} | {np.average(one[y], weights=one['wt']):.3f} |")
    # sector-clustered check of the layoff first stage
    X = np.column_stack([one["decl"].to_numpy(float), secd, byd, np.ones(len(one))])
    b, V, Gs = ols(X, one["f_sh_layoff"].to_numpy(float), one["wt"].to_numpy(float), one["h_sec"].to_numpy())
    md += ["", f"Layoff first stage clustered by sector ({Gs} clusters): {c((b[0], np.sqrt(V[0, 0])))}; "
           f"F (sector x birth-year clusters) = {(RES['fs|f_sh_layoff|decl'][0] / RES['fs|f_sh_layoff|decl'][1]) ** 2:.1f}.", ""]
    RES["fs|layoff|sector_cl"] = [float(b[0]), float(np.sqrt(V[0, 0]))]
    # (2) reduced form by band, stacked
    md += ["## 2. Reduced form: the son's ln earnings on the shock, by band", "",
           "| shock | controls | 25-29 | 45-49 | change 45-49 - 25-29 |", "|---|---|---|---|---|"]
    v = r[r["lw"].notna()].copy()
    s2 = v[v["band"].isin([0, 4])].copy()
    b4 = (s2["band"] == 4).to_numpy(float)
    for sv in ("decl", "grow"):
        for ctrl, clab in (((), "sector FE, birth-year FE"), (("lyp",), "+ ln parental income")):
            base = np.column_stack([s2[[sv] + list(ctrl)].to_numpy(float), dummies(s2["h_sec"]),
                                    dummies(s2["birth_year"]), dummies(s2["age"]), np.ones(len(s2))])
            X = np.column_stack([base, base * b4[:, None]])
            b, V, _ = ols(X, s2["ly"].to_numpy(float), s2["wt"].to_numpy(float), s2["cl"].to_numpy())
            K = base.shape[1]
            g0 = (b[0], np.sqrt(V[0, 0]))
            g4 = (b[0] + b[K], np.sqrt(V[0, 0] + V[K, K] + 2 * V[0, K]))
            ch = (b[K], np.sqrt(V[K, K]))
            dec = 3 if sv == "decl" else 4
            md.append(f"| {sv} | {clab} | {c(g0, dec)} | {c(g4, dec)} | {c(ch, dec)} |")
            RES[f"rf|{sv}|{clab}"] = {"g0": list(map(float, g0)), "g4": list(map(float, g4)), "ch": list(map(float, ch))}
    md.append("")
    # (3) within son, placebo windows, 2SLS
    md += ["## 3. Within the same son: shock x (age-40)/10, son FE; placebo windows; 2SLS", "",
           "Son FE, single-age dummies, sector x age, 5-year cohort x age (and lyp x age).", "",
           "| spec | teen shock x age | pre (5-11) x age | post (19-25) x age | layoff share x age (2SLS) | N son-years / sons |",
           "|---|---|---|---|---|---|"]
    ctl = np.column_stack([dummies(v["h_sec"]) * v["agec"].to_numpy()[:, None],
                           dummies(v["coh5"]) * v["agec"].to_numpy()[:, None],
                           (v["lyp"] * v["agec"]).to_numpy()[:, None], dummies(v["age"])])
    for sv in ("decl", "grow"):
        dec = 3 if sv == "decl" else 4
        z = v[f"{sv}"].to_numpy() * v["agec"].to_numpy()
        X = np.column_stack([z, ctl])
        b, V, _ = ols(X, v["ly"].to_numpy(float), v["wt"].to_numpy(float), v["cl"].to_numpy(), absorb=v["pid"].to_numpy())
        main_ = (b[0], np.sqrt(V[0, 0]))
        q = v.dropna(subset=[f"{sv}_pre", f"{sv}_post"])
        ctlq = ctl[v.index.get_indexer(q.index)] if False else np.column_stack(
            [dummies(q["h_sec"]) * q["agec"].to_numpy()[:, None], dummies(q["coh5"]) * q["agec"].to_numpy()[:, None],
             (q["lyp"] * q["agec"]).to_numpy()[:, None], dummies(q["age"])])
        Xp = np.column_stack([q[[sv, f"{sv}_pre", f"{sv}_post"]].to_numpy(float) * q["agec"].to_numpy()[:, None], ctlq])
        bp, Vp, _ = ols(Xp, q["ly"].to_numpy(float), q["wt"].to_numpy(float), q["cl"].to_numpy(), absorb=q["pid"].to_numpy())
        # 2SLS: layoff x age instrumented by shock x age
        Xe = np.column_stack([(v["f_sh_layoff"] * v["agec"]).to_numpy(), ctl])
        Ze = np.column_stack([z, ctl])
        bi, Vi, _ = ols(Xe, v["ly"].to_numpy(float), v["wt"].to_numpy(float), v["cl"].to_numpy(),
                        absorb=v["pid"].to_numpy(), Z=Ze)
        md.append(f"| {sv}, teen window alone | {c(main_, dec)} | | | {c((bi[0], np.sqrt(Vi[0, 0])))} | "
                  f"{len(v):,} / {v['pid'].nunique():,} |")
        md.append(f"| {sv}, three windows | {c((bp[0], np.sqrt(Vp[0, 0])), dec)} | {c((bp[1], np.sqrt(Vp[1, 1])), dec)} | "
                  f"{c((bp[2], np.sqrt(Vp[2, 2])), dec)} | | {len(q):,} / {q['pid'].nunique():,} |")
        RES[f"fe|{sv}"] = {"teen": list(map(float, main_)), "iv": [float(bi[0]), float(np.sqrt(Vi[0, 0]))],
                          "three": [[float(bp[j]), float(np.sqrt(Vp[j, j]))] for j in range(3)]}
    # OLS within-son layoff slope on the same sample for comparison
    Xo = np.column_stack([(v["f_sh_layoff"] * v["agec"]).to_numpy(), ctl])
    bo, Vo, _ = ols(Xo, v["ly"].to_numpy(float), v["wt"].to_numpy(float), v["cl"].to_numpy(), absorb=v["pid"].to_numpy())
    md += ["", f"OLS within-son layoff share x age on the same sample and controls: {c((bo[0], np.sqrt(Vo[0, 0])))}.", ""]
    RES["fe|ols_layoff"] = [float(bo[0]), float(np.sqrt(Vo[0, 0]))]
    (OUT / "layoff_industry_shocks.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "layoff_industry_shocks.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
