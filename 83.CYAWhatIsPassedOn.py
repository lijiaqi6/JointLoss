r"""What is passed on, in the NLSY79 Children and Young Adults (Paper B primary goal; the PSID split of
75.WhatIsPassedOn.py, EVIDENCE 11.29-11.32, on a second data set).

WHY THIS DATA SET. The CYA children are the children of the NLSY79 women, so the MOTHER is the respondent: her weekly
labour-force array (every week from 1978), her job roster with the reason each job ended (layoff vs plant / company
closing vs fired), her annual hours, weeks unemployed and wages, and her spouse's weeks, hours, weeks not working and
wages are all measured during the child's teens - including the children whose father is absent (the PSID's father
measures miss them). The children are followed as young adults to their mid-thirties and beyond (YA interviews 1994-
2020).

SAMPLE: CYA children of the White and Black NLSY79 women (data/cya_children.pkl, 10.CYAOutcomes.py), with earnings at
  26-35 (YA wages and salary, mean over interviews at 26-35, zeros kept; 10's earn2635) and the mother's family income
  observed in >= 2 years of the window. Sons and daughters, each and together.
WINDOW: calendar years in which the child is 13-17 (cyrb + 13 ... cyrb + 17). Income and annual work items of calendar
  year Y are from round Y + 1 (annual rounds to 1994, biennial from 1996, so from 1994 the odd years only); the weekly
  array and the job roster cover every week.
PARENTAL INCOME: lyp = ln of the mean of the mother's total net family income (TNFI_TRUNC, 2000 $) over the window
  years observed (>= 2).
COMPONENTS (as 75, with the mother as the measured parent and her spouse / partner as the father figure)
  WAGE      m_lw  mother's mean ln hourly wage = ln(wages and salary Q13-5 / hours HRSWK-PCY), valid years (hours >= 100,
                  earnings > 0, wage $2-200 of 2000)
            f_lw  spouse's mean ln hourly wage = ln(spouse wages and salary Q13-18 / (weeks worked Q2-15A x hours per
                  week Q2-15B)), same validity rule, years with a spouse present (Q2-15A answered)
  HOURS     m_lh  mother's mean ln annual hours, valid years; m_sh_zero her share of window years with 0 hours;
                  m_nowork fewer than 2 valid years
            f_lh  spouse's mean ln annual hours (weeks x hours per week), valid years
  STABILITY m_sh_unemp  mother's share of window weeks unemployed (weekly array code 4, over weeks with information)
            m_close     share of window years in which a job of hers ended because the plant / company / workplace
                        closed or the business failed (WHYLEFT)
            m_layoff    ... ended in a layoff (not a closure: layoff, temporary / seasonal end, program / project ended)
            m_fired     ... ended because she was fired / discharged
            m_vol       variance of her ln annual earnings over valid window years (>= 3)
            f_nw        spouse's share of the year not working (Q2-16 weeks not working / 52), spouse-present years
            f_na        spouse present but fewer than 2 valid years
  GROUP     g_ur        unemployment rate of the census region of residence (REGION) in the window years (mean of the
                        LAUS state rates of the region, data/state_shocks.pkl; the public NLSY79 has no state)
  STRUCTURE nofa (no spouse in any window round), m_na (no valid annual work item in the window), reg_na
  Missing measures: weighted mean of the observed (75's rule), flags in the structure group.
DESIGN: 74's exact Gelbach split (gel) on one row per child: outcome on lyp and the components; controls: child's
  birth-year dummies, mother's age at the birth and its square, female (in the sons-and-daughters sample); weighted by
  the mother's 1979 sampling weight; 200 cluster-bootstrap draws of mothers stratified by race. Outcomes: ln earnings
  at 26-35 (mean, zeros kept, log if > 0), ever attended college. Pooled and by race.
DESCRIPTIVE ACCOUNTING; aggregates only (output/cya_what_is_passed_on.md / .json); the person-level extract is cached
in data/cya_what_is_passed_on_raw.pkl (git-ignored).
"""
import importlib.util
import json
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import DATA, OUT, CPI, to2000, nls_pick as pick, nls_money  # noqa: E402
import os
DROPBOX = Path(os.environ.get("DROPBOX", Path.home() / "Dropbox"))   # raw data, read only


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R74 = _load("s74", HERE / "74.FrictionIGEPooled.py")
c, gel, Boot, rse, dummies = R74.c, R74.gel, R74.Boot, R74.rse, R74.dummies
N79 = HERE.parent / "NLSY79"
N79_CSV = Path(DROPBOX / "NLS") / "nlsy79_all_1979-2022" / "nlsy79_all_1979-2022.csv"
RAW = DATA / "cya_what_is_passed_on_raw.pkl"
NBOOT, SEED = R74.NBOOT, 20261020
WLO, WHI, HMIN = 2.0, 200.0, 100
LEFT = [("fired", r"discharged|fired|sub-par"), ("close", r"plant closed|workplace closed|business failed|company closed|"
        r"plant or company|closed down|went out of business|moved away"), ("family", r"pregnan|family|children|husband or "
        r"wife|spouse"), ("layoff", r"layoff|laid off|temporarily inactive|temporary|seasonal|program ended|project "
        r"completed|temp agency|assignments available"), ("quit", r".")]
REG = {1: [9, 23, 25, 33, 44, 50, 34, 36, 42], 2: [17, 18, 26, 39, 55, 19, 20, 27, 29, 31, 38, 46],
       3: [10, 11, 12, 13, 24, 37, 45, 51, 54, 1, 21, 28, 47, 5, 22, 40, 48],
       4: [4, 8, 16, 30, 32, 35, 49, 56, 2, 6, 15, 41, 53]}
GROUPS = {"wage": ["m_lw", "f_lw"], "hours": ["m_lh", "m_sh_zero", "m_nowork", "f_lh"],
          "stability": ["m_sh_unemp", "m_close", "m_layoff", "m_fired", "m_vol", "f_nw", "f_na"],
          "group": ["g_ur"], "structure": ["nofa", "m_na", "reg_na"]}
GLAB = {"wage": "WAGE (human capital)", "hours": "HOURS (labor supply)", "stability": "STABILITY (spells in the teens)",
        "group": "GROUP (regional unemployment)", "structure": "family structure / missing (not a component)",
        "b": "rest: parental income at equal components", "b0": "IGE (b0)"}
RES = {}


def raw():
    if RAW.exists():
        return pd.read_pickle(RAW)
    ix = pd.read_csv(DATA / "nlsy79_codebook.csv", dtype=str)
    items = {"hrs": ["HRSWK-PCY"], "wkun": ["WKSUEMP-PCY"], "earn": ["Q13-5_TRUNC_REVISED", "Q13-5_TRUNC", "Q13-5"],
             "searn": ["Q13-18_TRUNC_REVISED", "Q13-18_TRUNC", "Q13-18"], "swk": ["Q2-15A"], "shw": ["Q2-15B"],
             "snw": ["Q2-16"], "region": ["REGION"]}
    cols, ren = ["R0000100"], {"R0000100": "id"}
    for k, q in items.items():
        for y, col in pick(ix, q).items():
            cols.append(col)
            ren[col] = f"{k}{y}"
    print(f"reading {len(cols)} NLSY79 columns ...", flush=True)
    t = time.time()
    d = pd.read_csv(N79_CSV, usecols=cols).rename(columns=ren)
    print(f"  read in {time.time() - t:.0f}s", flush=True)
    d.to_pickle(RAW)
    return d


def label_maps(ix, stem, rules):
    """{variable: {code: category}} from the codebook labels (NLSY79/2.JobEndings.py's label_maps, copied: importing
    that script would clash with this folder's common.py)."""
    out = {}
    for _, r in ix[ix.qname.str.match(rf"^EMPLOYERS_ALL_{stem}_\d{{4}}\.\d\d")].iterrows():
        m = {}
        for x in str(r["labels"]).split(" | "):
            mm = re.match(r"^\s*(-?\d+):\s*(.+)$", x)
            if not mm or int(mm.group(1)) < 1:
                continue
            txt = mm.group(2).lower()
            m[int(mm.group(1))] = next(c_ for c_, pat in rules if re.search(pat, txt))
        out[r["qname"].replace("EMPLOYERS_ALL_", "")] = m
    return out


def mother_weekly():
    """per woman and calendar year: weeks with information, weeks unemployed; job ends by reason (NLSY79 roster)."""
    ix = pd.read_csv(N79 / "data" / "codebook_index.csv")
    d = pd.read_pickle(N79 / "data" / "women79.pkl").reset_index(drop=True)
    wy = pd.read_csv(N79 / "data" / "week_year.csv").dropna()
    year_of = np.full(int(wy.w.max()) + 1, np.nan)
    year_of[wy.w.astype(int)] = wy.y
    wcols = sorted(c_ for c_ in d.columns if re.fullmatch(r"wk\d{4}", c_))
    W = d[wcols].to_numpy()
    wk_idx = np.array([int(c_[2:]) for c_ in wcols])
    yrs = year_of[np.clip(wk_idx, 0, len(year_of) - 1)]
    known = (W >= 100) | np.isin(W, [2, 3, 4, 5])
    un = W == 4
    rows = []
    for y in np.unique(yrs[np.isfinite(yrs)]).astype(int):
        m = yrs == y
        rows.append(pd.DataFrame({"id": d["id"], "year": y, "wk_known": known[:, m].sum(1), "wk_un": un[:, m].sum(1)}))
    Wk = pd.concat(rows, ignore_index=True)
    lm = label_maps(ix, "WHYLEFT", LEFT)
    ends = []
    for v, mp in lm.items():
        rnd = v.split("_", 1)[1]
        if f"STOPWEEK_{rnd}" not in d.columns or v not in d.columns:
            continue
        code, stop = d[v].to_numpy(), d[f"STOPWEEK_{rnd}"].to_numpy()
        for i in np.flatnonzero((code > 0) & (stop > 0) & (stop < len(year_of))):
            r_ = mp.get(int(code[i]))
            if r_ in ("close", "layoff", "fired") and np.isfinite(year_of[int(stop[i])]):
                ends.append((d.at[i, "id"], int(year_of[int(stop[i])]), r_, rnd.split(".")[1]))
    E = pd.DataFrame(ends, columns=["id", "year", "why", "jj"]).drop_duplicates(["id", "year", "why", "jj"])
    E = E.assign(n=1).pivot_table(index=["id", "year"], columns="why", values="n", aggfunc="sum").reset_index()
    cats = {k: sum(1 for m_ in lm.values() for v_ in m_.values() if v_ == k) for k in ("close", "layoff", "fired")}
    return Wk, E, cats


def region_ur():
    sh = pd.read_pickle(DATA / "state_shocks.pkl")[["fips", "year", "ur"]]
    rmap = {f: r for r, fs in REG.items() for f in fs}
    sh["region"] = sh["fips"].map(rmap)
    return sh.dropna(subset=["region"]).groupby(["region", "year"])["ur"].mean().rename("g_ur").reset_index()


def build():
    K = pd.read_pickle(DATA / "cya_children.pkl")
    K = K[K["race"].isin(["White", "Black"]) & K["cyrb"].notna()].copy()
    K["cyrb"] = K["cyrb"].astype(int)
    inc = pd.read_pickle(DATA / "cya_mother_tnfi_raw.pkl")
    R = raw()
    Wk, E, cats = mother_weekly()
    RU = region_ur()
    # long: child x window year
    L = K[["cid", "mid", "cyrb"]].assign(key=1).merge(pd.DataFrame({"off": range(13, 18), "key": 1}), on="key")
    L["year"] = L["cyrb"] + L["off"]
    L = L.drop(columns="key")
    rnd = L["year"] + 1
    I = inc.set_index("id")
    Rr = R.set_index("id")

    def get(frame, prefix, ids, rounds):
        out = np.full(len(ids), np.nan)
        for rr in np.unique(rounds):
            col = f"{prefix}{rr}"
            if col in frame.columns:
                m = (rounds == rr).to_numpy()
                out[m] = pd.to_numeric(frame[col].reindex(ids[m]), errors="coerce").to_numpy()
        return out

    ids = L["mid"].to_numpy()
    L["tnfi"] = get(I, "tnfi", ids, rnd)
    L["tnfi"] = nls_money(pd.Series(L["tnfi"])).to_numpy()
    defl = np.array([CPI[2000] / CPI[int(y)] if int(y) in CPI else np.nan for y in L["year"]])
    L["fi"] = L["tnfi"] * defl
    hrs, earn = get(Rr, "hrs", ids, rnd), get(Rr, "earn", ids, rnd)
    L["hrs"] = np.where(hrs >= 0, hrs, np.nan)
    L["earn"] = nls_money(pd.Series(earn)).to_numpy() * defl
    sw, shw, snw, se = (get(Rr, k, ids, rnd) for k in ("swk", "shw", "snw", "searn"))
    L["sp"] = (sw >= 0).astype(float)
    L.loc[~np.isfinite(sw) | (sw < -3), "sp"] = np.nan             # -4 = valid skip (no spouse): 0; other neg: NaN
    L.loc[sw == -4, "sp"] = 0.0
    L["swk"], L["shw"] = np.where(sw >= 0, sw, np.nan), np.where(shw >= 0, shw, np.nan)
    L["snw"] = np.where(snw >= 0, snw, np.nan)
    L["searn"] = nls_money(pd.Series(se)).to_numpy() * defl
    reg = get(Rr, "region", ids, L["year"])                          # residence at the year-Y interview
    reg2 = get(Rr, "region", ids, rnd)
    L["region"] = np.where(np.isin(reg, [1, 2, 3, 4]), reg, np.where(np.isin(reg2, [1, 2, 3, 4]), reg2, np.nan))
    L = L.merge(RU, on=["region", "year"], how="left")
    L = L.merge(Wk.rename(columns={"id": "mid"}), on=["mid", "year"], how="left")
    L = L.merge(E.rename(columns={"id": "mid"}), on=["mid", "year"], how="left")
    for k in ("close", "layoff", "fired"):
        L[k] = (L.get(k, 0).fillna(0) > 0).astype(float).where(L["wk_known"] > 0)
    # validity
    L["m_valid"] = (L["hrs"] >= HMIN) & (L["earn"] > 0) & ((L["earn"] / L["hrs"]).between(WLO, WHI))
    L["m_lw_y"] = np.log(L["earn"] / L["hrs"]).where(L["m_valid"])
    L["m_lh_y"] = np.log(L["hrs"]).where(L["m_valid"])
    L["m_le_y"] = np.log(L["earn"]).where(L["m_valid"])
    L["m_zero_y"] = (L["hrs"] == 0).astype(float).where(L["hrs"].notna())
    sh = L["swk"] * L["shw"]
    L["f_valid"] = (L["sp"] == 1) & (sh >= HMIN) & (L["searn"] > 0) & ((L["searn"] / sh).between(WLO, WHI))
    L["f_lw_y"] = np.log(L["searn"] / sh).where(L["f_valid"])
    L["f_lh_y"] = np.log(sh).where(L["f_valid"])
    L["f_nw_y"] = (L["snw"].clip(0, 52) / 52).where(L["sp"] == 1)
    g = L.groupby("cid")
    C = pd.DataFrame(index=g.size().index)
    C["n_fi"] = g["fi"].count()
    C["lyp"] = np.log(g["fi"].mean().where((C["n_fi"] >= 2) & (g["fi"].mean() > 0)))
    nv = g["m_valid"].sum()
    C["m_lw"], C["m_lh"] = g["m_lw_y"].mean().where(nv >= 1), g["m_lh_y"].mean().where(nv >= 1)
    C["m_vol"] = g["m_le_y"].var().where(nv >= 3)
    C["m_sh_zero"] = g["m_zero_y"].mean()
    C["m_nowork"] = (nv < 2).astype(float)
    C["m_na"] = g["hrs"].count().eq(0).astype(float)
    C["m_sh_unemp"] = (g["wk_un"].sum() / g["wk_known"].sum().where(g["wk_known"].sum() > 0))
    for k in ("close", "layoff", "fired"):
        C[f"m_{k}"] = g[k].mean()
    nsp, nfv = g["sp"].sum(), g["f_valid"].sum()
    C["nofa"] = (nsp.fillna(0) == 0).astype(float)
    C["f_lw"], C["f_lh"] = g["f_lw_y"].mean().where(nfv >= 1), g["f_lh_y"].mean().where(nfv >= 1)
    C["f_nw"] = g["f_nw_y"].mean()
    C["f_na"] = ((C["nofa"] == 0) & (nfv < 2)).astype(float)
    C["g_ur"] = g["g_ur"].mean()
    C["reg_na"] = C["g_ur"].isna().astype(float)
    K = K.merge(C.reset_index(), on="cid", how="left")
    K = K[K["lyp"].notna() & K["learn2635"].notna()].copy()
    K["female"] = (K["csex"] == 2).astype(float)
    K["wt"] = K["m_wt79"].astype(float)
    one = K
    # missing-indicator rule: weighted mean among the observed (parent present for the father's measures)
    for v in ("m_lw", "m_lh", "m_vol", "m_sh_zero", "m_sh_unemp", "m_close", "m_layoff", "m_fired", "g_ur"):
        q = one[one[v].notna()]
        K[v] = K[v].fillna(float(np.average(q[v], weights=q["wt"])))
    for v in ("f_lw", "f_lh", "f_nw"):
        ok = (K["nofa"] == 0) & K[v].notna()
        q = K[ok]
        K[v] = K[v].where(ok, float(np.average(q[v], weights=q["wt"])))
    K["college"] = K["college_any"].astype(float)
    return K, cats


def run(d, ys, BT):
    cols = [v for g_ in GROUPS.values() for v in g_]
    gidx, i = {}, 0
    for gname, g_ in GROUPS.items():
        gidx[gname] = list(range(i, i + len(g_)))
        i += len(g_)
    d = d.dropna(subset=ys + ["lyp", "wt", "magebir", "cyrb"] + cols)
    cols_ok = [v for v in cols if d[v].std() > 0]
    if len(cols_ok) < len(cols):                                       # drop constant columns (keep the group map)
        keep = [cols.index(v) for v in cols_ok]
        gidx = {k: [keep.index(j) for j in v if j in keep] for k, v in gidx.items()}
        cols = cols_ok
    mb = d["magebir"].to_numpy(float)
    parts = [dummies(d["cyrb"]), np.column_stack([mb, mb ** 2])]
    if d["female"].std() > 0:
        parts.append(d[["female"]].to_numpy(float))
    A = np.column_stack(parts + [np.ones((len(d), 1))])
    x, Y, Med, w0 = d["lyp"].to_numpy(float), d[ys].to_numpy(float), d[cols].to_numpy(float), d["wt"].to_numpy(float)
    ri = BT.rows(d["mid"].to_numpy())
    pt = gel(x, A, Y, Med, w0, gidx)
    bs = {s: np.zeros((BT.cnt.shape[0], len(ys))) for s in pt}
    for b in range(BT.cnt.shape[0]):
        ob = gel(x, A, Y, Med, w0 * BT.cnt[b, ri], gidx)
        for s in pt:
            bs[s][b] = ob[s]
    return {"pt": pt, "bs": bs, "cols": cols, "n": (len(d), int(d["mid"].nunique()))}


def cell(res, stat, j, share=False):
    if stat not in res["pt"]:
        return ""
    p, dr = res["pt"][stat][j], res["bs"][stat][:, j]
    if share:
        p0, d0 = res["pt"]["b0"][j], res["bs"]["b0"][:, j]
        return c((p / p0, rse(dr / d0)))
    return c((p, float(np.nanstd(dr, ddof=1))))


def main():
    t0 = time.time()
    K, cats = build()
    BT = Boot(K["mid"].to_numpy(), K["race"].to_numpy(), seed=SEED)
    md = ["# What is passed on, NLSY79 Children and Young Adults", "",
          "Built by `83.CYAWhatIsPassedOn.py` (2026-10-20); definitions in its docstring. CYA children of White and Black "
          "NLSY79 mothers, outcomes at 26-35; parental income and components over the child's ages 13-17; exact Gelbach "
          f"split (74's gel); mother's 1979 weight; {NBOOT} cluster-bootstrap draws of mothers stratified by race; "
          "estimate (s.e.; p), *** p<0.01, ** p<0.05, * p<0.1; shares = contribution / IGE. **Descriptive accounting.**",
          "", f"Job-end reason codes classified (WHYLEFT label maps): closure {cats['close']}, layoff {cats['layoff']}, "
          f"fired {cats['fired']}.", ""]
    md += ["## 0. Components (weighted means)", "",
           "| sample | children | ln parental income | mother: ln wage / ln hours / zero-hours years / weeks unemployed / "
           "closure years / layoff years / fired years | spouse present | spouse: ln wage / ln hours / not working | "
           "regional unemployment |", "|---" * 7 + "|"]
    wa = lambda q, v: np.average(q[v], weights=q["wt"])  # noqa: E731
    for lab, s in (("all", K), ("White", K[K.race == "White"]), ("Black", K[K.race == "Black"]),
                   ("sons", K[K.female == 0]), ("daughters", K[K.female == 1])):
        f = s[s.nofa == 0]
        md.append(f"| {lab} | {len(s):,} | {wa(s, 'lyp'):.3f} | {wa(s, 'm_lw'):.3f} / {wa(s, 'm_lh'):.3f} / "
                  f"{wa(s, 'm_sh_zero'):.3f} / {wa(s, 'm_sh_unemp'):.3f} / {wa(s, 'm_close'):.3f} / {wa(s, 'm_layoff'):.3f} / "
                  f"{wa(s, 'm_fired'):.3f} | {1 - wa(s, 'nofa'):.3f} | {wa(f, 'f_lw'):.3f} / {wa(f, 'f_lh'):.3f} / "
                  f"{wa(f, 'f_nw'):.3f} | {wa(s, 'g_ur'):.2f} |")
    md.append("")
    ys = ["learn2635", "college"]
    YL = {"learn2635": "ln earnings 26-35", "college": "ever attended college"}
    for samp, S in (("sons and daughters", K), ("sons", K[K.female == 0]), ("daughters", K[K.female == 1])):
        md += [f"## {samp}", "", "| outcome | component | pooled | share | White | share | Black | share | "
               "White - Black |", "|---" * 9 + "|"]
        res = {lab: run(d, ys, BT) for lab, d in (("pooled", S), ("White", S[S.race == "White"]),
                                                   ("Black", S[S.race == "Black"]))}
        for j, y in enumerate(ys):
            for gname in ["b0"] + list(GROUPS) + ["b"]:
                stat = gname if gname in ("b0", "b") else f"c:{gname}"
                row = []
                for lab in ("pooled", "White", "Black"):
                    row += [cell(res[lab], stat, j), "" if gname == "b0" else cell(res[lab], stat, j, share=True)]
                dw = res["White"]["bs"].get(stat)
                dd = ""
                if dw is not None and stat in res["Black"]["bs"]:
                    pdif = res["White"]["pt"][stat][j] - res["Black"]["pt"][stat][j]
                    dd = c((pdif, float(np.nanstd(dw[:, j] - res["Black"]["bs"][stat][:, j], ddof=1))))
                md.append(f"| {YL[y]} | {GLAB.get(gname, gname)} | " + " | ".join(row) + f" | {dd} |")
                RES[f"{samp}|{y}|{gname}"] = {lab: [float(res[lab]["pt"][stat][j]),
                                                    float(np.nanstd(res[lab]["bs"][stat][:, j], ddof=1))]
                                              for lab in res if stat in res[lab]["pt"]}
                RES[f"{samp}|{y}|{gname}|share"] = {
                    lab: [float(res[lab]["pt"][stat][j] / res[lab]["pt"]["b0"][j]),
                          float(rse(res[lab]["bs"][stat][:, j] / res[lab]["bs"]["b0"][:, j]))]
                    for lab in res if stat in res[lab]["pt"]}
            # elements
            for kk, col in enumerate(res["pooled"]["cols"]):
                if col in GROUPS["structure"]:
                    continue
                row = []
                for lab in ("pooled", "White", "Black"):
                    cl = res[lab]["cols"]
                    row += [cell(res[lab], f"e:{cl.index(col)}", j) if col in cl else "", ""]
                md.append(f"| {YL[y]} | element: {col} | " + " | ".join(row) + " | |")
        md.append("| N children / mothers | " + " | ".join(f"{res[l_]['n'][0]:,} / {res[l_]['n'][1]:,} | "
                                                      for l_ in ("pooled", "White", "Black")) + " |")
        md.append("")
        print(f"{samp} done {time.time() - t0:.0f}s", flush=True)
    (OUT / "cya_what_is_passed_on.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "cya_what_is_passed_on.json", "w"), indent=1)
    print(f"done {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
