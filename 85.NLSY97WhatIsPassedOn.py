r"""What is passed on, in the NLSY97 (Paper B primary goal; the PSID split of 75.WhatIsPassedOn.py on the youngest
cohort, born 1980-84, observed to ages ~39-43).

WHAT THE 1997 PARENT INTERVIEW MEASURES (one responding parent, PR, mostly the mother; and the PR's spouse / partner)
  WAGE      p_lw, s_lw   ln(1996 wages and salary / (50 x usual hours per week at the most recent job)) of the PR
                         (P5-016, P3-120) and the spouse (P5-028, P3-094 of the highest-numbered spouse with a job): a
                         full-year hourly wage, $2-200 of 2000 (the interview has no weeks worked)
  HOURS     p_lh, s_lh   ln usual hours per week at the most recent job; p_now = PR without 1996 wages
  BREAKS    p_brk, s_brk employment breaks of 6+ months (P3-119 PR, P3-093 spouse: year the PR / spouse stopped working
                         for 6+ months) that began in the youth's lifetime (birth year to 1997), per year of the youth's
                         life. The reason is not asked, so a break may be a job loss or a choice (for mothers mostly
                         the latter): this is the NLSY97's stability measure, read with that caveat
  GROUP     g_ur         unemployment rate of the census region of residence in 1997 (CV_CENSUS_REGION; mean of the
                         LAUS state rates of the region in 1996); no state in the public file
  RESOURCES transfers (AFDC or food stamps received in 1996, P5-048 / P5-052) and the biological parents' highest
                         grade completed (CV_HGC_BIO_MOM / DAD), reported as a separate group (as 80's split B)
  STRUCTURE nosp (no spouse / partner of the PR), pr_male (the PR is a man), missing flags
  Missing measures: weighted mean of the observed (75's rule), flags in the structure group.
OUTCOMES AND DESIGN: 29.NLSY97AgeProfile.py's child-year frame (its extract, imported read only): ln own earnings in
  valid years (learn_v; earnings $516-773,413 of 2000, hours >= 100, wage $2-200) and ln hourly wage (lwage_v), ages
  25-44 in bands 25-29 / 30-34 / 35-39 / 40-44; parental income = the 1997 parent report of 1996 household income
  (lyp_pt), as in 29. Exact Gelbach split (74's gel) in each band and over 25-44: single-age dummies and 29's parental
  age quartic (+ missing flag); round weights; 200 cluster-bootstrap draws of 1997 households stratified by race.
  Black and White (= non-Black non-Hispanic, the NLSY97 category) sons and daughters; pooled = Black + White, weighted.
DESCRIPTIVE ACCOUNTING; aggregates only (output/nlsy97_what_is_passed_on.md / .json); the parent items are cached in
data/nlsy97_parent_items.pkl (git-ignored).
"""
import importlib.util
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import CPI, DATA, OUT  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R74 = _load("s74", "74.FrictionIGEPooled.py")
R29 = _load("s29", "29.NLSY97AgeProfile.py")
c, gel, Boot, rse, dummies = R74.c, R74.gel, R74.Boot, R74.rse, R74.dummies
ITEMS = DATA / "nlsy97_parent_items.pkl"
SEED = 20261020
BANDS = ["25-29", "30-34", "35-39", "40-44", "25-44"]
REG = {1: [9, 23, 25, 33, 44, 50, 34, 36, 42], 2: [17, 18, 26, 39, 55, 19, 20, 27, 29, 31, 38, 46],
       3: [10, 11, 12, 13, 24, 37, 45, 51, 54, 1, 21, 28, 47, 5, 22, 40, 48],
       4: [4, 8, 16, 30, 32, 35, 49, 56, 2, 6, 15, 41, 53]}
GROUPS = {"wage": ["p_lw", "s_lw"], "hours": ["p_lh", "s_lh", "p_now"], "breaks": ["p_brk", "s_brk"],
          "group": ["g_ur"], "resources": ["transf", "m_hgc", "f_hgc"],
          "structure": ["nosp", "pr_male", "p_na", "s_na", "hgc_na"]}
GLAB = {"wage": "WAGE (PR and spouse, 1996)", "hours": "HOURS (usual hours per week)",
        "breaks": "BREAKS of 6+ months in the youth's life (stability; reason unknown)",
        "group": "GROUP (regional unemployment)", "resources": "transfers 1996 + parents' schooling",
        "structure": "family structure / missing", "b": "rest: parental income at equal components", "b0": "IGE (b0)"}
RES = {}


def items():
    if ITEMS.exists():
        return pd.read_pickle(ITEMS)
    ix = pd.read_csv(DATA / "nlsy97_codebook.csv", dtype=str)
    ix = ix[ix["year"].isin(["1997", "XRND"])]
    pat = {"pr_sex": r"^PARSEX$", "p_earn": r"^P5-016$", "s_earn": r"^P5-028$", "afdc": r"^P5-048$", "fs": r"^P5-052$",
           "m_hgc": r"^CV_HGC_BIO_MOM$", "f_hgc": r"^CV_HGC_BIO_DAD$", "region": r"^CV_CENSUS_REGION$",
           "p_h": r"^P3-120\.\d\d$", "s_h": r"^P3-094\.\d\d\.\d\d$", "p_stop": r"^P3-119\.\d\d_Y$",
           "s_stop": r"^P3-093\.\d\d\.\d\d_Y$"}
    cols, meta = ["R0000100"], {}
    for k, p in pat.items():
        s = ix[ix["qname"].str.match(p)].sort_values("qname")
        meta[k] = list(zip(s["col"], s["qname"]))
        cols += list(s["col"])
    print(f"reading {len(cols)} NLSY97 columns ...", flush=True)
    d = pd.read_csv(R29.CSV, usecols=list(dict.fromkeys(cols)))
    out = pd.DataFrame({"pid": d["R0000100"]})
    for k in ("pr_sex", "p_earn", "s_earn", "afdc", "fs", "m_hgc", "f_hgc", "region"):
        out[k] = pd.to_numeric(d[meta[k][0][0]], errors="coerce") if meta[k] else np.nan
    for k in ("p_h", "s_h", "p_stop", "s_stop"):
        M = d[[col for col, _ in meta[k]]].apply(pd.to_numeric, errors="coerce").to_numpy(float).copy()
        M[M < 0] = np.nan
        if k in ("p_h", "s_h"):                                       # most recent job = last answered
            last = np.full(len(M), np.nan)
            for j in range(M.shape[1]):
                last = np.where(np.isfinite(M[:, j]) & (M[:, j] > 0), M[:, j], last)
            out[k] = last
        else:
            out[k] = list(M)
    out.to_pickle(ITEMS)
    return out


def build():
    k, L = R29.load_extract()
    s, k2, _ = R29.nlsy97_frames(k, L)
    I = items()
    k2 = k2[k2["race"].isin(["Black", "White"])].merge(I, on="pid", how="left")
    by = k2["birth_year"].to_numpy(float)
    defl = CPI[2000] / CPI[1996]
    P = pd.DataFrame({"pid": k2["pid"]})
    pe = pd.to_numeric(k2["p_earn"], errors="coerce")
    se = pd.to_numeric(k2["s_earn"], errors="coerce")
    P["nosp"] = ((se == -4) | se.isna() & k2["s_h"].isna()).astype(float).to_numpy()
    pe_ = pe.where(pe >= 0, np.where(pe == -4, 0.0, np.nan)) * defl
    se_ = se.where(se >= 0, np.where(se == -4, 0.0, np.nan)) * defl
    for tag, e, h in (("p", pe_, k2["p_h"]), ("s", se_, k2["s_h"])):
        w = e / (50 * h)
        ok = (e > 0) & (h > 0) & w.between(2, 200)
        P[f"{tag}_lw"] = np.log(w.where(ok)).to_numpy()
        P[f"{tag}_lh"] = np.log(h.where(h > 0)).to_numpy()
        P[f"{tag}_na"] = (~ok).astype(float).to_numpy()
    P.loc[P["nosp"] == 1, "s_na"] = 0.0
    P["p_now"] = (pe_ == 0).astype(float).to_numpy()
    life = np.clip(1997 - by, 1, None)
    for tag in ("p", "s"):
        stops = k2[f"{tag}_stop"]
        n = [np.sum((np.asarray(v) >= b) & (np.asarray(v) <= 1997)) if isinstance(v, (list, np.ndarray)) else np.nan
             for v, b in zip(stops, by)]
        P[f"{tag}_brk"] = np.array(n, float) / life
    P.loc[P["nosp"] == 1, "s_brk"] = np.nan
    af, fs = pd.to_numeric(k2["afdc"], errors="coerce"), pd.to_numeric(k2["fs"], errors="coerce")
    P["transf"] = ((af == 1) | (fs == 1)).astype(float).where(af.notna() | fs.notna()).to_numpy()
    for v in ("m_hgc", "f_hgc"):
        x = pd.to_numeric(k2[v], errors="coerce")
        P[v] = x.where(x.between(0, 20)).to_numpy()
    P["hgc_na"] = (np.isnan(P["m_hgc"]) | np.isnan(P["f_hgc"])).astype(float)
    P["pr_male"] = (pd.to_numeric(k2["pr_sex"], errors="coerce") == 1).astype(float).to_numpy()
    sh = pd.read_pickle(DATA / "state_shocks.pkl")[["fips", "year", "ur"]]
    rmap = {f: r for r, fs_ in REG.items() for f in fs_}
    sh["region"] = sh["fips"].map(rmap)
    ru = sh[sh.year == 1996].groupby("region")["ur"].mean()
    P["g_ur"] = pd.to_numeric(k2["region"], errors="coerce").map(ru).to_numpy()
    P["wt0"] = k2["w"].to_numpy(float)
    for v in ("p_lw", "p_lh", "s_lw", "s_lh", "p_brk", "s_brk", "transf", "m_hgc", "f_hgc", "g_ur"):
        q = P[P[v].notna()]
        P[v] = P[v].fillna(float(np.average(q[v], weights=q["wt0"])))
    s = s[s["race"].isin(["Black", "White"])].merge(P.drop(columns="wt0"), on="pid", how="inner")
    s = s[s["lyp"].notna() & s["wt"].notna() & (s["wt"] > 0)]
    return s, P


def run(d, y, BT):
    cols = [v for g_ in GROUPS.values() for v in g_]
    d = d.dropna(subset=[y, "lyp", "agei"] + cols)
    keep = [v for v in cols if d[v].std() > 0]
    gidx, i = {}, 0
    for gname, g_ in GROUPS.items():
        g2 = [v for v in g_ if v in keep]
        gidx[gname] = list(range(i, i + len(g2)))
        i += len(g2)
    cols = [v for g_ in GROUPS.values() for v in g_ if v in keep]
    A = np.column_stack([dummies(d["agei"]), d[R29.A4 + ["Amiss"]].to_numpy(float), np.ones((len(d), 1))])
    if d["female"].std() > 0:
        A = np.column_stack([A, d["female"].to_numpy(float)])
    x, Y, Med, w0 = d["lyp"].to_numpy(float), d[[y]].to_numpy(float), d[cols].to_numpy(float), d["wt"].to_numpy(float)
    ri = BT.rows(d["fam68"].to_numpy())
    pt = gel(x, A, Y, Med, w0, gidx)
    bs = {s_: np.zeros((BT.cnt.shape[0], 1)) for s_ in pt}
    for b in range(BT.cnt.shape[0]):
        ob = gel(x, A, Y, Med, w0 * BT.cnt[b, ri], gidx)
        for s_ in pt:
            bs[s_][b] = ob[s_]
    return {"pt": pt, "bs": bs, "cols": cols, "n": (int(d["pid"].nunique()), len(d))}


def cell(res, stat, share=False):
    if res is None or stat not in res["pt"]:
        return ""
    p, dr = res["pt"][stat][0], res["bs"][stat][:, 0]
    if share:
        return c((p / res["pt"]["b0"][0], rse(dr / res["bs"]["b0"][:, 0])))
    return c((p, float(np.nanstd(dr, ddof=1))))


def main():
    t0 = time.time()
    s, P = build()
    one = s.drop_duplicates("pid")
    BT = Boot(s["fam68"].to_numpy(), s["race"].to_numpy(), seed=SEED)
    md = ["# What is passed on, NLSY97", "",
          "Built by `85.NLSY97WhatIsPassedOn.py` (2026-10-20); definitions in its docstring. Black and White NLSY97 "
          "youths (born 1980-84), parental measures from the 1997 parent interview; exact Gelbach split by age band; "
          f"round weights; {R74.NBOOT} cluster-bootstrap draws of 1997 households stratified by race; estimate (s.e.; p), "
          "*** p<0.01, ** p<0.05, * p<0.1; opening = 35-39 minus 25-29. **Descriptive accounting.**", "",
          "## 0. Components (weighted, one row per youth)", "",
          "| sample | youths | PR is a man | spouse present | PR ln wage / ln hours / no 1996 wages / breaks per year | "
          "spouse ln wage / ln hours / breaks per year | transfers 1996 | mother's / father's schooling |",
          "|---" * 8 + "|"]
    wa = lambda q, v: np.average(q[v], weights=q["w"])  # noqa: E731
    for lab, q in (("all", one), ("White", one[one.race == "White"]), ("Black", one[one.race == "Black"])):
        f = q[q.nosp == 0]
        md.append(f"| {lab} | {len(q):,} | {wa(q, 'pr_male'):.3f} | {1 - wa(q, 'nosp'):.3f} | {wa(q, 'p_lw'):.3f} / "
                  f"{wa(q, 'p_lh'):.3f} / {wa(q, 'p_now'):.3f} / {wa(q, 'p_brk'):.4f} | {wa(f, 's_lw'):.3f} / "
                  f"{wa(f, 's_lh'):.3f} / {wa(f, 's_brk'):.4f} | {wa(q, 'transf'):.3f} | {wa(q, 'm_hgc'):.2f} / "
                  f"{wa(q, 'f_hgc'):.2f} |")
    md.append("")
    for y, ylab in (("learn_v", "ln own earnings"), ("lwage_v", "ln hourly wage")):
        for samp, S in (("sons and daughters", s), ("sons", s[s.female == 0])):
            md += [f"## {ylab}, {samp}", ""]
            for race in ("pooled", "White", "Black"):
                D = S if race == "pooled" else S[S.race == race]
                res = {}
                for b in BANDS:
                    z = D if b == "25-44" else D[D["band"] == b]
                    res[b] = run(z, y, BT) if z["pid"].nunique() >= 150 else None
                md += [f"#### {race}", "", "| component | " + " | ".join(BANDS) + " | opening 35-39 - 25-29 | share 25-44 |",
                       "|---" * 8 + "|"]
                for gname in ["b0"] + list(GROUPS) + ["b"]:
                    stat = gname if gname in ("b0", "b") else f"c:{gname}"
                    op = ""
                    if res["35-39"] and res["25-29"] and stat in res["35-39"]["pt"]:
                        dd = res["35-39"]["bs"][stat][:, 0] - res["25-29"]["bs"][stat][:, 0]
                        op = c((res["35-39"]["pt"][stat][0] - res["25-29"]["pt"][stat][0], float(np.nanstd(dd, ddof=1))))
                    md.append(f"| {GLAB[gname]} | " + " | ".join(cell(res[b], stat) for b in BANDS) + f" | {op} | "
                              + ("" if gname == "b0" else cell(res["25-44"], stat, share=True)) + " |")
                    RES[f"{y}|{samp}|{race}|{gname}"] = {b: ([float(res[b]["pt"][stat][0]),
                                                              float(np.nanstd(res[b]["bs"][stat][:, 0], ddof=1))]
                                                             if res[b] and stat in res[b]["pt"] else None) for b in BANDS}
                    r6_ = res["25-44"]
                    if gname != "b0" and r6_ and stat in r6_["pt"]:
                        RES[f"{y}|{samp}|{race}|{gname}|share"] = [
                            float(r6_["pt"][stat][0] / r6_["pt"]["b0"][0]),
                            float(rse(r6_["bs"][stat][:, 0] / r6_["bs"]["b0"][:, 0]))]
                r6 = res["25-44"]
                for kk, col in enumerate(r6["cols"]):
                    if col in ("p_brk", "s_brk", "p_lw", "s_lw", "transf", "m_hgc", "f_hgc"):
                        md.append(f"| element {col} | " + " | ".join(cell(res[b], f"e:{res[b]['cols'].index(col)}")
                                                                    if res[b] and col in res[b]["cols"] else ""
                                                                    for b in BANDS) + " | | |")
                md += [f"Youths / youth-years 25-44: {r6['n'][0]:,} / {r6['n'][1]:,}.", ""]
        print(f"{y} {time.time() - t0:.0f}s", flush=True)
    (OUT / "nlsy97_what_is_passed_on.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "nlsy97_what_is_passed_on.json", "w"), indent=1)
    print(f"done {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
