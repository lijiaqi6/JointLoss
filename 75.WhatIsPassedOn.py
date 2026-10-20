r"""What is passed on from parents to sons (Paper B primary goal, PI 2026-10-20; proposals/paperB_primary_goal_20261020.md).

THE QUESTION. The IGE bundles different things transmitted through parental income, each with a different policy:
  WAGE        the parents' hourly wage (human capital, skills, returns)            -> schooling, training
  HOURS       hours when employed and whether the mother works (labor supply)       -> tax / transfer incentives, childcare
  STABILITY   employment spells in childhood (a stable environment)                 -> UI, income smoothing for families
  GROUP       search friction the family's place faces (local labor market)         -> job-search help, place-based policy
This script splits the IGE of the son's outcomes into the parts that come through each component, pooled (PSID weights)
and by race, by the son's age, and reports the 4 x 4 table: parental component x son's outcome (wage, hours when
employed, employment, his own spells). Framing (race or race-neutral) is open (PI): every table is pooled and by race.

DATA (read only; person-level caches under data/, git-ignored)
  Son-years: 74.FrictionIGEPooled.py's build() (73's panel = 36's psid_build(); sons 25-55, PSID weights wt; father's
  and mother's window measures; family-structure flags nofa / nomo / m_un_na). x = lyp = ln parental family income,
  mean over the son's wave-ages 13-19.
  SON'S OUTCOMES: lw ln hourly wage, lh ln annual hours, ly ln annual earnings (valid years, ly = lw + lh), emp = hours > 0
  (every son-year), sb_unemp / sb_disp = his shares of band years unemployed / displaced (every son-year), lfam = ln of
  his family income.
  PARENTAL COMPONENTS (window = the son's wave-ages 13-19; income year = wave - 1; 24.IGEDecomposition.py's head-and-wife
  panel data/ige_decomposition_panel.pkl for the mother and the father's job ends):
   WAGE   f_lw   father's mean ln hourly wage over his valid window years (24's person_measures, >= 3 valid years)
          m_lw   mother's mean ln hourly wage over her valid window years (>= 2) - the woman of the son's family unit
                 (wife / partner of the head, or the female head), as in 74
   HOURS  f_lh   father's mean ln annual hours over his valid window years (hours when employed)
          m_lh   mother's mean ln annual hours over her valid window years
          m_sh_zero  mother's share of window years with zero hours (74; for mothers mostly labor supply)
          m_nowork   mother present with fewer than 2 valid window years (she does not work, or barely)
   STABILITY  f_sh_close  father's share of window years with a PLANT CLOSURE (psid_displacement 'strict'), t or t-1
          f_sh_layoff father's share with a layoff / firing (main and not strict), t or t-1
          f_sh_unemp, f_sh_zero  father's shares unemployed / zero hours (24)
          f_vtr  variance of the father's transitory ln earnings over valid window years (24; >= 3 years)
          f_na   father present but without 3 valid window years (his wage, hours, volatility are not measured)
          m_sh_unemp  mother's share of measured window years unemployed (74)
   GROUP  g_ur   mean state unemployment rate (BLS LAUS, data/state_shocks.pkl) over the son's income years at ages 12-18
                 in his state at 17 (72's state17: family-file state, waves 1976+), >= 3 years
          g_bart mean men's Bartik labor-demand shock (state_shocks 'bartik_m', 1980+) over the same years, >= 3 years
  Missing parental measures are set to their weighted mean among the sons where they are observed (missing-indicator
  rule, so a 0 fill cannot make a measure a copy of its flag); the flags of absent parents and of an unknown state are the
  STRUCTURE group (nofa, nomo, m_un_na, st_na), never counted as a component.
DESIGN: 74's exact Gelbach split, x = lyp, mediators = the components (they are COMPONENTS of parental income: d_k is the
  gradient of the component in x, g_k its partial relation to the son's outcome; the contribution of a component
  g_k d_k is the part of the IGE carried by parental-income differences that are differences in it). b0 = wage + hours
  + stability + group + structure + rest (b, parental income at equal components: other income, transfers, unmeasured).
  Each band its own regression with single-age dummies; 25-55 one regression; weighted by wt; 200 cluster-bootstrap draws
  of 1968 families stratified by race (74's Boot); shares = contribution / b0 with percentile s.e. Also the partial
  coefficients (standardised components, 25-55) and each element's contribution (closures vs layoffs, place measures).
DESCRIPTIVE ACCOUNTING: components are correlated choices and outcomes; nothing here identifies a causal effect; the
  closure share and the state measures are the handles that are not the family's choice.
Writes output/what_is_passed_on.md and .json (aggregates only).
"""
import importlib.util
import json
import os
import sys
import time
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


R74 = _load("s74", "74.FrictionIGEPooled.py")
R72 = _load("s72", "72.FrictionGenerations.py")
R24 = R74.R24
c, est, cc, Boot, run_spec, wreg = R74.c, R74.est, R74.cc, R74.Boot, R74.run_spec, R74.wreg
CACHE = DATA / "what_is_passed_on_parents.pkl"
CELLS = (0, 2, 4, 6)                       # 25-29, 35-39, 45-49, 25-55
CLAB = {0: "25-29", 2: "35-39", 4: "45-49", 6: "25-55"}
GROUPS = {"wage": ["f_lw", "m_lw"], "hours": ["f_lh", "m_lh", "m_sh_zero", "m_nowork"],
          "stability": ["f_sh_close", "f_sh_layoff", "f_sh_unemp", "f_sh_zero", "f_vtr", "f_na", "m_sh_unemp"],
          "group": ["g_ur", "g_bart"], "structure": ["nofa", "nomo", "m_un_na", "st_na"]}
GLAB = {"wage": "WAGE (human capital)", "hours": "HOURS (labor supply)", "stability": "STABILITY (spells in childhood)",
        "group": "GROUP (place search friction)", "structure": "family structure (not a component)",
        "b": "rest: parental income at equal components"}
OUT_V, OUT_E, OUT_F = ["ly", "lw", "lh"], ["emp", "sb_unemp", "sb_disp"], ["lfam"]
OL = {"ly": "ln earnings", "lw": "ln hourly wage", "lh": "ln hours (employed)", "emp": "employed",
      "sb_unemp": "son's share of years unemployed", "sb_disp": "son's share of years displaced", "lfam": "ln family income"}
RES = {}


def parents(r):
    """mother's wage / hours and the father's closure / layoff shares over the son's window waves; state measures."""
    if CACHE.exists():
        return pd.read_pickle(CACHE)
    a = pd.read_pickle(R24.CACHE)
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    sons = r.drop_duplicates("pid")[["pid", "fpid", "birth_year"]]
    k = py[py["child"] & py["age"].between(13, 19) & py["faminc"].between(R24.LO, R24.HI) & py["pid"].isin(sons["pid"])][
        ["pid", "wave", "int"]]
    wom = a[a["wife"] | (a["head"] & (a["female"] == 1))].drop_duplicates(["wave", "int"])
    mw = k.merge(wom[["wave", "int", "pid", "valid", "lw", "lh"]].rename(columns={"pid": "mpid"}), on=["wave", "int"],
                 how="left")
    mv = mw[mw["valid"] == True]  # noqa: E712
    g = mv.groupby("pid")
    M = pd.DataFrame(index=pd.Index(mw["pid"].unique(), name="pid"))
    M["m_lw"], M["m_lh"] = g["lw"].mean(), g["lh"].mean()
    M["m_nv"] = g["lw"].count().reindex(M.index).fillna(0)
    # father's closures and layoffs (t or t-1), window waves in which he is the male head
    dp = pd.read_pickle(DATA / "psid_displacement.pkl")
    clo = set(zip(dp.loc[dp["strict"] == 1, "pid"], dp.loc[dp["strict"] == 1, "year"]))
    lay = set(zip(dp.loc[(dp["main"] == 1) & (dp["strict"] != 1), "pid"], dp.loc[(dp["main"] == 1) & (dp["strict"] != 1),
                                                                               "year"]))
    fa = a[a["head"] & (a["female"] == 0)][["pid", "wave"]].rename(columns={"pid": "fpid"}).drop_duplicates()
    fw = k.merge(sons[["pid", "fpid"]].dropna(), on="pid").merge(fa, on=["fpid", "wave"])
    yr = fw["wave"] - 1
    fw["close"] = [float((p, y) in clo or (p, y - 1) in clo) for p, y in zip(fw["fpid"], yr)]
    fw["layoff"] = [float((p, y) in lay or (p, y - 1) in lay) for p, y in zip(fw["fpid"], yr)]
    F = fw.groupby("pid")[["close", "layoff"]].mean().rename(columns={"close": "f_sh_close", "layoff": "f_sh_layoff"})
    # state over the son's income years at 12-18 in his state at 17
    st = R72.state17(r.drop_duplicates("pid")[["pid", "birth_year"]].copy())
    sh = pd.read_pickle(DATA / "state_shocks.pkl")[["fips", "year", "ur", "bartik_m"]]
    rows = st.dropna(subset=["fips17"]).assign(key=1).merge(pd.DataFrame({"off": range(12, 19), "key": 1}), on="key")
    rows["year"] = (rows["birth_year"] + rows["off"]).astype(int)
    rows = rows.merge(sh.rename(columns={"fips": "fips17"}), on=["fips17", "year"], how="left")
    gs = rows.groupby("pid")
    S = pd.DataFrame({"g_ur": gs["ur"].mean().where(gs["ur"].count() >= 3),
                      "g_bart": gs["bartik_m"].mean().where(gs["bartik_m"].count() >= 3)})
    out = M.join(F, how="outer").join(S, how="outer")
    out.index.name = "pid"
    out = out.reset_index()
    out.to_pickle(CACHE)
    return out


def build():
    r, pan, OCC, IND = R74.build()
    P = parents(r)
    r = r.merge(P, on="pid", how="left")
    pres_f, pres_m = r["nofa"] == 0, r["nomo"] == 0
    one = r.drop_duplicates("pid")

    def fill(v, ok):
        """missing-indicator rule: where the measure is not observed, set it to its weighted mean over the sons where it
        is (one row per son), so the flag carries the level and the measure only the variation among the observed."""
        q = one[ok.loc[one.index] & one[v].notna()]
        mu = float(np.average(q[v], weights=q["wt"]))
        r[v] = r[v].where(ok & r[v].notna(), mu)

    r["f_na"] = (pres_f & (r["f_lw"].isna() | r["f_lh"].isna() | r["f_vtr"].isna())).astype(float)
    okf = pres_f & (r["f_na"] == 0)
    for v in ("f_lw", "f_lh", "f_vtr"):
        fill(v, okf)
    for v in ("f_sh_close", "f_sh_layoff"):
        fill(v, pres_f)
    r["m_nowork"] = (pres_m & (r["m_nv"].fillna(0) < 2)).astype(float)
    okm = pres_m & (r["m_nowork"] == 0)
    for v in ("m_lw", "m_lh"):
        fill(v, okm)
    r["st_na"] = (r["g_ur"].isna() | r["g_bart"].isna()).astype(float)
    oks = r["st_na"] == 0
    for v in ("g_ur", "g_bart"):
        fill(v, oks)
    return r


def table(md, title, res, ys, note=""):
    """rows = components, cells = contribution (and share of b0) by band, for each outcome."""
    md += [f"#### {title}", ""] + ([note, ""] if note else [])
    md += ["| son's outcome | component | " + " | ".join(f"{CLAB[k]}" for k in CELLS) + " | opening 45-49 - 25-29 |"
           " share 25-29 | share 45-49 | share 25-55 |", "|---" * 10 + "|"]
    for j, y in enumerate(ys):
        md.append(f"| **{OL[y]}** | IGE (b0) | " + " | ".join(cc(est(res, k, 'b0', j)) for k in CELLS)
                  + f" | {cc(est(res, 'open', 'b0', j))} | | | |")
        RES[f"{title}|{y}|b0"] = [list(e[:2]) if e else None for e in [est(res, k, "b0", j) for k in CELLS]]
        for gname in list(GROUPS) + ["b"]:
            stat = "b" if gname == "b" else f"c:{gname}"
            ent = [est(res, k, stat, j) for k in CELLS] + [est(res, "open", stat, j)]
            shr = [est(res, k, stat, j, share=True) for k in (0, 4, 6)]
            md.append(f"| {OL[y]} | {GLAB[gname]} | " + " | ".join(cc(e) for e in ent) + " | "
                      + " | ".join(cc(e) for e in shr) + " |")
            RES[f"{title}|{y}|{gname}"] = {"contrib": [list(e[:2]) if e else None for e in ent],
                                          "share": [list(e[:2]) if e else None for e in shr]}
    n = res["n"]
    md += [f"Sons / son-years / 1968 families: {n[0]:,} / {n[1]:,} / {n[2]:,}.", ""]


def elements(md, title, res, ys):
    md += [f"#### {title}", "", "| son's outcome | element | " + " | ".join(CLAB[k] for k in CELLS) + " |",
           "|---" * 6 + "|"]
    for j, y in enumerate(ys):
        for kk, col in enumerate(res["cols"]):
            if col in GROUPS["structure"]:
                continue
            ent = [est(res, k, f"e:{kk}", j) for k in CELLS]
            md.append(f"| {OL[y]} | {col} | " + " | ".join(cc(e) for e in ent) + " |")
            RES[f"{title}|{y}|{col}"] = [list(e[:2]) if e else None for e in ent]
    md.append("")


def four_by_four(md, d, label):
    """partial coefficients: each son's outcome on all standardised components + lyp, 25-55, weighted, CR1."""
    comps = [v for g in ("wage", "hours", "stability", "group") for v in GROUPS[g]]
    z = d.copy()
    for v in comps:
        s = np.sqrt(np.cov(z[v], aweights=z["wt"]))
        z[v] = (z[v] - np.average(z[v], weights=z["wt"])) / s if s > 0 else 0.0
    xs = [v for v in ["lyp"] + comps + GROUPS["structure"] if z[v].std() > 0]      # wreg drops constant columns
    comps = [v for v in comps if v in xs]
    md += [f"#### 4 x 4 partial coefficients, {label}: son's outcome on all components (1 s.d.) and ln parental income, "
           "ages 25-55, single-age dummies, weighted, s.e. clustered by 1968 family", "",
           "| component | " + " | ".join(OL[y] for y in ("lw", "lh", "emp", "sb_unemp", "sb_disp")) + " |", "|---" * 6 + "|"]
    outs = [wreg(z[z["lw"].notna()], "lw", xs), wreg(z[z["lh"].notna() & z["lw"].notna()], "lh", xs),
            wreg(z[z["emp"].notna()], "emp", xs), wreg(z[z["sb_unemp"].notna()], "sb_unemp", xs),
            wreg(z[z["sb_disp"].notna()], "sb_disp", xs)]
    for v in ["lyp"] + comps:
        md.append(f"| {v} | " + " | ".join(c(o[0][v]) for o in outs) + " |")
        RES[f"4x4|{label}|{v}"] = [list(o[0][v]) for o in outs]
    md.append("| N son-years / sons / clusters | " + " | ".join(f"{o[1]:,} / {o[2]:,} / {o[3]:,}" for o in outs) + " |")
    md.append("")


def main():
    t0 = time.time()
    r = build()
    BT = Boot(r["fam68"].to_numpy(), r["race"].to_numpy())
    md = ["# What is passed on from parents to sons: wage, hours, stability, place", "",
          "Built by `75.WhatIsPassedOn.py` (2026-10-20); definitions in its docstring. PSID sons 25-55, PSID weights; "
          "contributions from an exact Gelbach split of the IGE on ln parental income into the parental components; "
          f"{R74.NBOOT} cluster-bootstrap draws of 1968 families (stratified by race); estimate (s.e.; p), *** p<0.01, "
          "** p<0.05, * p<0.1. b0 = wage + hours + stability + group + structure + rest exactly. **Descriptive "
          "accounting.**", ""]
    one = r.drop_duplicates("pid")
    md += ["## 0. Components (weighted means over sons with the parent present)", "",
           "| sample | sons | father: ln wage / ln hours / closure share / layoff share / unemployed / zero hours / transitory var "
           "| mother: works (>= 2 valid years) / ln wage / ln hours | state at 17 known | state unemployment 12-18 |",
           "|---|---|---|---|---|---|"]
    for lab, s in (("pooled", one), ("White", one[one.race == "White"]), ("Black", one[one.race == "Black"])):
        f = s[(s.nofa == 0) & (s.f_na == 0)]
        m = s[s.nomo == 0]
        mw_ = m[m.m_nowork == 0]
        st = s[s.st_na == 0]
        wa = lambda q, v: np.average(q[v], weights=q["wt"]) if len(q) else np.nan  # noqa: E731
        md.append(f"| {lab} | {len(s):,} | {wa(f, 'f_lw'):.3f} / {wa(f, 'f_lh'):.3f} / {wa(f, 'f_sh_close'):.3f} / "
                  f"{wa(f, 'f_sh_layoff'):.3f} / {wa(f, 'f_sh_unemp'):.3f} / {wa(f, 'f_sh_zero'):.3f} / {wa(f, 'f_vtr'):.3f} | "
                  f"{1 - wa(m, 'm_nowork'):.3f} / {wa(mw_, 'm_lw'):.3f} / {wa(mw_, 'm_lh'):.3f} | {1 - wa(s, 'st_na'):.3f} | "
                  f"{wa(st, 'g_ur'):.2f} |")
    md.append("")
    for lab, d in (("pooled", r), ("White", r[r.race == "White"]), ("Black", r[r.race == "Black"])):
        print(f"{lab} ...", flush=True)
        BTd = Boot(d["fam68"].to_numpy(), d["race"].to_numpy(), seed=R74.SEED + (0 if lab == "pooled" else 11))
        oV = run_spec(d[d["lw"].notna()], OUT_V, GROUPS, BTd, cells=CELLS)
        oE = run_spec(d[d["emp"].notna() & d["sb_unemp"].notna() & d["sb_disp"].notna()], OUT_E, GROUPS, BTd, cells=CELLS)
        oF = run_spec(d[d["lfam"].notna()], OUT_F, GROUPS, BTd, cells=CELLS)
        md += [f"## {lab}", ""]
        table(md, f"{lab}: earnings, wage and hours (valid years; earnings = wage + hours)", oV, OUT_V)
        table(md, f"{lab}: employment and the son's own spells (every son-year)", oE, OUT_E)
        table(md, f"{lab}: family income", oF, OUT_F)
        if lab == "pooled":
            elements(md, "pooled: contribution of each element (closures vs layoffs; place measures)", oV, OUT_V)
            elements(md, "pooled: contribution of each element, employment and spells", oE, OUT_E)
        four_by_four(md, d, lab)
        print(f"  {lab} done {time.time() - t0:.0f}s", flush=True)
    (OUT / "what_is_passed_on.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "what_is_passed_on.json", "w"), indent=1, default=str)
    print(f"done {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
