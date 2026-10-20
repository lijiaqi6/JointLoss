r"""What is passed on, NLSY79 youths (Paper B primary goal; the PSID split of 75.WhatIsPassedOn.py on a cohort born
1957-64 and followed to its late fifties / sixties - the longest age range of the three NLS cohorts).

WHAT THE 1979 INTERVIEW MEASURES ABOUT THE PARENTS (the youth reports the household at age 14)
  WAGE      f_occw   mean ln weekly wage of men 25-55 in the occupation of the adult man in the household at 14
                     (FAM-11A, 1970 Census 3-digit), from the March CPS 1977-80 (Mare-Winship extracts: wage and salary
                     income / weeks worked last year, occupation last year, 1970 codes; 2000 $; supplemental weight;
                     cells with >= 20 men, else missing); for men who worked for pay at 14
            m_occw   the same for the adult woman (women's wages in her occupation)
  HOURS     f_work, m_work   the adult man / woman worked for pay when the youth was 14 (FAM-11, FAM-9)
  GROUP     south14, rural14 lived in the South / outside a town or city at 14 (FAM-RES, FAM-6)
  RESOURCES f_hgc, m_hgc     father's / mother's highest grade completed (HGC-FATHER, HGC-MOTHER);
            reading          number of {magazines, newspapers, library card} at 14 (FAM-13A-C)
  STRUCTURE no man / no woman in the household at 14 (FAM-7), not both biological parents (FAM-7 != 11), flags
  There is no stability measure: the 1979 interview does not ask about the parents' spells.
PARENTAL INCOME AND OUTCOMES: 2.NLSY79.py's frames (data/nlsy79_kids.pkl, nlsy79_person_year.pkl): ln of the mean
  1979-81 family income in the rounds the youth lives with a parent (lpinc_av); outcome = ln annual earnings (wages +
  business income, 2000 $, $516-773,413) of the youth at 25-59, by band 25-29 ... 55-59. Exact Gelbach split (74's gel)
  per band and over 25-59: single-age dummies and a quartic in the parent's age (2.NLSY79.py's page, missing flag);
  1979 weight; 200 cluster-bootstrap draws of 1979 households stratified by race. Black and White (NLSY79 samples) sons
  and daughters; pooled = Black + White, weighted.
DESCRIPTIVE ACCOUNTING; aggregates only (output/nlsy79_youth_what_is_passed_on.md / .json); person-level items cached in
data/nlsy79_youth_parent_items.pkl, the CPS occupation index in data/cps_occ1970_wage.pkl (aggregates).
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
import os
DROPBOX = Path(os.environ.get("DROPBOX", Path.home() / "Dropbox"))   # raw data, read only


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R74 = _load("s74", "74.FrictionIGEPooled.py")
c, gel, Boot, rse, dummies = R74.c, R74.gel, R74.Boot, R74.rse, R74.dummies
N79_CSV = Path(DROPBOX / "NLS") / "nlsy79_all_1979-2022" / "nlsy79_all_1979-2022.csv"
MW = Path(DROPBOX / "CPS/mare_winship/extracted")
ITEMS, OCC = DATA / "nlsy79_youth_parent_items.pkl", DATA / "cps_occ1970_wage.pkl"
SEED = 20261020
LO, HI = (v * CPI[2000] / CPI[1967] for v in (100, 150_000))
BANDS = [(25, 29), (30, 34), (35, 39), (40, 44), (45, 49), (50, 54), (55, 59)]
BL = [f"{a}-{b}" for a, b in BANDS] + ["25-59"]
COLS = {"R0000100": "id", "R0001900": "fam7", "R0002100": "m_work", "R0002200": "m_occ", "R0002400": "f_work",
        "R0002500": "f_occ", "R0001610": "south14", "R0001800": "res14", "R0002700": "mag", "R0002800": "news",
        "R0002900": "lib", "R0006500": "m_hgc", "R0007900": "f_hgc"}
GROUPS = {"wage": ["f_occw", "m_occw"], "hours": ["f_work", "m_work"], "group": ["south14", "rural14"],
          "resources": ["f_hgc", "m_hgc", "reading"], "structure": ["noman", "nowoman", "notboth", "occ_na", "hgc_na"]}
GLAB = {"wage": "WAGE (occupation wage of the man / woman at 14)", "hours": "HOURS (man / woman worked for pay at 14)",
        "group": "GROUP (South, rural at 14)", "resources": "parents' schooling + reading materials",
        "structure": "family structure / missing", "b": "rest: parental income at equal components", "b0": "IGE (b0)"}
RES = {}


def occ_index():
    if OCC.exists():
        return pd.read_pickle(OCC)
    cs = [(12, 14), (92, 95), (182, 183), (186, 193), (204, 206), (232, 235), (280, 292)]
    nm = ["year", "age", "sex", "wag", "ww", "occ", "w"]
    out = []
    for yy in (77, 78, 79, 80):
        d = pd.read_fwf(MW / f"cpsmw{yy}", colspecs=cs, names=nm)
        d = d[d.age.between(25, 55) & (d.ww >= 1) & (d.ww <= 52) & (d.wag > 0) & (d.w > 0) & (d.occ > 0)]
        d["lw"] = np.log(d.wag / d.ww * CPI[2000] / CPI[1900 + yy - 1])
        out.append(d)
    d = pd.concat(out)
    g = d.groupby(["sex", "occ"])
    O = pd.DataFrame({"occw": g.apply(lambda z: np.average(z.lw, weights=z.w)), "n": g.size()}).reset_index()
    O.to_pickle(OCC)
    return O


def items():
    if ITEMS.exists():
        return pd.read_pickle(ITEMS)
    d = pd.read_csv(N79_CSV, usecols=list(COLS)).rename(columns=COLS)
    d.to_pickle(ITEMS)
    return d


def build():
    k = pd.read_pickle(DATA / "nlsy79_kids.pkl")
    L = pd.read_pickle(DATA / "nlsy79_person_year.pkl")
    I = items().rename(columns={"id": "pid"})
    O = occ_index()
    k = k[k["race"].isin(["Black", "White"]) & k["lpinc_av"].notna()].merge(I, on="pid", how="left")
    for v in I.columns:
        if v != "pid":
            k[v] = pd.to_numeric(k[v], errors="coerce").where(lambda s: s >= 0)
    t, u = k["fam7"] // 10, k["fam7"] % 10
    k["noman"] = (t == 5).astype(float)
    k["nowoman"] = (u == 5).astype(float)
    k["notboth"] = (k["fam7"] != 11).astype(float)
    for tag, sex, work in (("f", 1, "f_work"), ("m", 2, "m_work")):
        o = O[(O.sex == sex) & (O.n >= 20)].set_index("occ")["occw"]
        k[f"{tag}_occw"] = k[f"{tag}_occ"].map(o).where(k[work] == 1)
    k["occ_na"] = (((k["f_work"] == 1) & k["f_occw"].isna()) | ((k["m_work"] == 1) & k["m_occw"].isna())).astype(float)
    k["rural14"] = (k["res14"] >= 2).astype(float).where(k["res14"].notna())
    k["reading"] = k[["mag", "news", "lib"]].sum(axis=1, min_count=1)
    for v in ("f_hgc", "m_hgc"):
        k[v] = k[v].where(k[v] <= 20)
    k["hgc_na"] = (k["f_hgc"].isna() | k["m_hgc"].isna()).astype(float)
    k["wt0"] = k["wt79"].astype(float)
    for v in ("f_work", "m_work", "south14", "rural14", "reading", "f_hgc", "m_hgc", "f_occw", "m_occw"):
        q = k[k[v].notna()]
        k[v] = k[v].fillna(float(np.average(q[v], weights=q["wt0"])))
    k["Amiss"] = k["page"].isna().astype(float)
    for n in range(1, 5):
        k[f"A{n}"] = ((k["page"].fillna(45) - 45) / 10) ** n
    s = L[L["age"].between(25, 59)].merge(k.drop(columns=["race", "female", "birth_year", "hhid"]), on="pid")
    s["ly"] = np.log(s["earn"].where(s["earn"].between(LO, HI)))
    s["agei"] = s["age"].round().astype(int)
    s["band"] = pd.cut(s["age"], [24, 29, 34, 39, 44, 49, 54, 59], labels=BL[:-1]).astype(str)
    s["w"] = s["wt0"]
    return s[s["ly"].notna()], k


def run(d, BT):
    cols = [v for g_ in GROUPS.values() for v in g_]
    keep = [v for v in cols if d[v].std() > 0]
    gidx, i = {}, 0
    for gname, g_ in GROUPS.items():
        g2 = [v for v in g_ if v in keep]
        gidx[gname] = list(range(i, i + len(g2)))
        i += len(g2)
    cols = [v for g_ in GROUPS.values() for v in g_ if v in keep]
    parts = [dummies(d["agei"]), d[["A1", "A2", "A3", "A4", "Amiss"]].to_numpy(float), np.ones((len(d), 1))]
    if d["female"].std() > 0:
        parts.append(d[["female"]].to_numpy(float))
    A = np.column_stack(parts)
    x, Y, Med, w0 = d["lpinc_av"].to_numpy(float), d[["ly"]].to_numpy(float), d[cols].to_numpy(float), d["w"].to_numpy(float)
    ri = BT.rows(d["hhid"].to_numpy())
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


def diff(a, b, stat):
    if not a or not b or stat not in a["pt"] or stat not in b["pt"]:
        return ""
    return c((a["pt"][stat][0] - b["pt"][stat][0], float(np.nanstd(a["bs"][stat][:, 0] - b["bs"][stat][:, 0], ddof=1))))


def main():
    t0 = time.time()
    s, k = build()
    O = occ_index()
    BT = Boot(s["hhid"].to_numpy(), s["race"].to_numpy(), seed=SEED)
    md = ["# What is passed on, NLSY79 youths", "",
          "Built by `86.NLSY79YouthWhatIsPassedOn.py` (2026-10-20); definitions in its docstring. Black and White NLSY79 "
          "youths living with a parent in 1979-81; household at 14; earnings at 25-59; exact Gelbach split by age band; "
          f"1979 weight; {R74.NBOOT} cluster-bootstrap draws of 1979 households stratified by race; estimate (s.e.; p), "
          "*** p<0.01, ** p<0.05, * p<0.1; opening = 50-54 minus 25-29. **Descriptive accounting.**", "",
          f"CPS occupation index: {int((O.n >= 20).sum())} occupation x sex cells with >= 20 workers (1977-80 March CPS).",
          "", "## 0. Components (weighted, one row per youth)", "",
          "| sample | youths | man / woman worked at 14 | occupation wage man / woman | South / rural at 14 | father's / "
          "mother's schooling | reading items | no man / no woman / not both parents |", "|---" * 8 + "|"]
    one = s.drop_duplicates("pid")
    wa = lambda q, v: np.average(q[v], weights=q["w"])  # noqa: E731
    for lab, q in (("all", one), ("White", one[one.race == "White"]), ("Black", one[one.race == "Black"])):
        md.append(f"| {lab} | {len(q):,} | {wa(q, 'f_work'):.3f} / {wa(q, 'm_work'):.3f} | {wa(q, 'f_occw'):.3f} / "
                  f"{wa(q, 'm_occw'):.3f} | {wa(q, 'south14'):.3f} / {wa(q, 'rural14'):.3f} | {wa(q, 'f_hgc'):.2f} / "
                  f"{wa(q, 'm_hgc'):.2f} | {wa(q, 'reading'):.2f} | {wa(q, 'noman'):.3f} / {wa(q, 'nowoman'):.3f} / "
                  f"{wa(q, 'notboth'):.3f} |")
    md.append("")
    for samp, S in (("sons", s[s.female == 0]), ("daughters", s[s.female == 1])):
        md += [f"## ln earnings, {samp}", ""]
        for race in ("pooled", "White", "Black"):
            D = S if race == "pooled" else S[S.race == race]
            res = {b: run(D if b == "25-59" else D[D["band"] == b], BT) for b in BL
                   if (D if b == "25-59" else D[D["band"] == b])["pid"].nunique() >= 150}
            md += [f"#### {race}", "", "| component | " + " | ".join(BL) + " | opening 50-54 - 25-29 | share 25-59 |",
                   "|---" * (len(BL) + 3) + "|"]
            for gname in ["b0"] + list(GROUPS) + ["b"]:
                stat = gname if gname in ("b0", "b") else f"c:{gname}"
                md.append(f"| {GLAB[gname]} | " + " | ".join(cell(res.get(b), stat) for b in BL) + " | "
                          + diff(res.get("50-54"), res.get("25-29"), stat) + " | "
                          + ("" if gname == "b0" else cell(res.get("25-59"), stat, share=True)) + " |")
                RES[f"{samp}|{race}|{gname}"] = {b: ([float(res[b]["pt"][stat][0]),
                                                      float(np.nanstd(res[b]["bs"][stat][:, 0], ddof=1))]
                                                     if b in res and stat in res[b]["pt"] else None) for b in BL}
                r6_ = res.get("25-59")
                if gname != "b0" and r6_ and stat in r6_["pt"]:
                    RES[f"{samp}|{race}|{gname}|share"] = [float(r6_["pt"][stat][0] / r6_["pt"]["b0"][0]),
                                                           float(rse(r6_["bs"][stat][:, 0] / r6_["bs"]["b0"][:, 0]))]
            for col in ("f_occw", "m_occw", "f_work", "m_work", "f_hgc", "m_hgc", "reading"):
                md.append(f"| element {col} | " + " | ".join(cell(res[b], f"e:{res[b]['cols'].index(col)}")
                                                            if b in res and col in res[b]["cols"] else "" for b in BL)
                          + " | | |")
            r6 = res["25-59"]
            md += [f"Youths / youth-years: {r6['n'][0]:,} / {r6['n'][1]:,}.", ""]
        print(f"{samp} {time.time() - t0:.0f}s", flush=True)
    (OUT / "nlsy79_youth_what_is_passed_on.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "nlsy79_youth_what_is_passed_on.json", "w"), indent=1)
    print(f"done {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
