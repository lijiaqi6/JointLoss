r"""PSID: parents' family income in childhood and the child's adult earnings (2026-10-16).

Reads the raw PSID files in Dropbox/PSID (read only) and writes IGE/data/ (not in git):
  psid_person_year.pkl  every SRC + SEO person x wave in a family unit: interview number, sequence, relation, age,
                        sex, the family's total income, the head's race and age, and the person's own labor income
                        when head or wife (head / wife labor income; from the 1994 wave plus the labor part of
                        business income, which the PSID left out of labor income from then on). Real 2000 dollars of
                        the income year (wave - 1).
  psid_kids.pkl         one row per child: parents' family income (a) in the wave the child is 16 (nearest of 15-17),
                        (b) the mean over the waves the child is 12-17; head's age and race at (a); the child's
                        lifetime own earnings and family income (mean over the years as head / wife at ages 25-55,
                        zeros kept) and the number of years and mean age behind them.
Children = SRC + SEO sample members living as the head's child (or stepchild) at 12-17. Parents = the family unit
they live in (the same rule as Lee and Solon 2009); the Latino and immigrant samples are left out.
"""
import re
from pathlib import Path

import numpy as np
import pandas as pd

from common import DATA, AGE_LO, AGE_HI, to2000, lifetime
import os
DROPBOX = Path(os.environ.get("DROPBOX", Path.home() / "Dropbox"))   # raw data, read only (Mac: export DROPBOX)

PSID = Path(DROPBOX / "PSID")
IND = PSID / "Individual" / "ind2023er" / "IND2023ER"
FAM = PSID / "Family"

WAVES = list(range(1968, 1998)) + list(range(1999, 2024, 2))
# family file, by wave: total family income, head labor income, wife labor income, head race (first mention)
FAMINC = ["V81", "V529", "V1514", "V2226", "V2852", "V3256", "V3676", "V4154", "V5029", "V5626", "V6173", "V6766",
          "V7412", "V8065", "V8689", "V9375", "V11022", "V12371", "V13623", "V14670", "V16144", "V17533", "V18875",
          "V20175", "V21481", "V23322", "ER4153", "ER6993", "ER9244", "ER12079", "ER16462", "ER20456", "ER24099",
          "ER28037", "ER41027", "ER46935", "ER52343", "ER58152", "ER65349", "ER71426", "ER77448", "ER81775",
          "ER85629"]
HLAB = ["V74", "V514", "V1196", "V1897", "V2498", "V3051", "V3463", "V3863", "V5031", "V5627", "V6174", "V6767",
        "V7413", "V8066", "V8690", "V9376", "V11023", "V12372", "V13624", "V14671", "V16145", "V17534", "V18878",
        "V20178", "V21484", "V23323", "ER4140", "ER6980", "ER9231", "ER12080", "ER16463", "ER20443", "ER24116",
        "ER27931", "ER40921", "ER46829", "ER52237", "ER58038", "ER65216", "ER71293", "ER77315", "ER81642", "ER85496"]
# 1976-78 waves: the wife's wages (no wife labor income total in those files)
WLAB = ["V75", "V516", "V1198", "V1899", "V2500", "V3053", "V3465", "V3865", "V4379", "V5289", "V5788", "V6398",
        "V6988", "V7580", "V8273", "V8881", "V10263", "V11404", "V12803", "V13905", "V14920", "V16420", "V17836",
        "V19136", "V20436", "V23324", "ER4144", "ER6984", "ER9235", "ER12082", "ER16465", "ER20447", "ER24135",
        "ER27943", "ER40933", "ER46841", "ER52249", "ER58050", "ER65244", "ER71321", "ER77343", "ER81670", "ER85524"]
RACE = ["V181", "V801", "V1490", "V2202", "V2828", "V3300", "V3720", "V4204", "V5096", "V5662", "V6209", "V6802",
        "V7447", "V8099", "V8723", "V9408", "V11055", "V11938", "V13565", "V14612", "V16086", "V17483", "V18814",
        "V20114", "V21420", "V23276", "ER3944", "ER6814", "ER9060", "ER11848", "ER15928", "ER19989", "ER23426",
        "ER27393", "ER40565", "ER46543", "ER51904", "ER57659", "ER64810", "ER70882", "ER76897", "ER81144", "ER85121"]
# labor part of business income, head and wife, waves 1994+ (excluded from labor income from then on)
HBUS = {1994: "ER4119", 1995: "ER6959", 1996: "ER9210", 1997: "ER12193", 1999: "ER16490", 2001: "ER20422",
        2003: "ER24109", 2005: "ER27910", 2007: "ER40900", 2009: "ER46808", 2011: "ER52216", 2013: "ER58017",
        2015: "ER65197", 2017: "ER71274", 2019: "ER77296", 2021: "ER81623", 2023: "ER85477"}
WBUS = {1994: "ER4141", 1995: "ER6981", 1996: "ER9232", 1997: "ER12214", 1999: "ER16511", 2001: "ER20444",
        2003: "ER24111", 2005: "ER27940", 2007: "ER40930", 2009: "ER46838", 2011: "ER52246", 2013: "ER58047",
        2015: "ER65225", 2017: "ER71302", 2019: "ER77324", 2021: "ER81651", 2023: "ER85505"}
assert len(FAMINC) == len(HLAB) == len(WLAB) == len(RACE) == len(WAVES)

INFIX = re.compile(r"(?:long\s+)?([A-Z]+\d+[A-Z]?)\s+(\d+)\s*-\s*(\d+)")
LABEL = re.compile(r'label variable\s+(\S+)\s+"(.*)"')


def layout(do):
    t = do.read_text(encoding="latin-1")
    block = re.search(r"\binfix\b(.*?)\busing\b", t, re.S).group(1)
    pos = {v: (int(a) - 1, int(b)) for v, a, b in INFIX.findall(block)}
    labs = [(v, l.strip()) for v, l in LABEL.findall(t)]
    return pos, labs


def read(base, cols, pos):
    return pd.read_fwf(base.with_suffix(".txt"), colspecs=[pos[c] for c in cols], names=cols, header=None,
                       encoding="latin-1")


def individual():
    pos, labs = layout(IND.with_suffix(".do"))
    per = {}                                                   # wave -> {int, seq, rel, age, wt}
    for v, l in labs:
        m = re.search(r"(\d\d)$", l)
        if l.endswith("INTERVIEW NUMBER") and l[:4].isdigit():
            w = int(l[:4])
            per.setdefault(w, {})["int"] = v
            continue
        if not m:
            continue
        yy = int(m.group(1))
        w = 1900 + yy if yy >= 68 else 2000 + yy
        key = ("seq" if l.startswith("SEQUENCE NUMBER") else
               "rel" if re.match(r"RELATION(SHIP)? TO (HEAD|REFERENCE PERSON)", l) else
               "age" if l.startswith("AGE OF INDIVIDUAL") else
               "wt" if re.match(r"(INDIVIDUAL WEIGHT|CORE IND WEIGHT|CORE INDIVIDUAL LONGITUDINAL WEIGHT|"
                                r"CORE/IMM INDIVIDUAL LONGITUDINAL WT)", l) else None)
        if key and key not in per.get(w, {}):
            per.setdefault(w, {})[key] = v
    per[1968]["int"] = "ER30001"
    byr = [v for v, l in labs if re.match(r"YEAR IND(IVIDUAL)? BORN", l)]
    cols = (["ER30001", "ER30002", "ER32000"] + byr
            + [c for w in WAVES for c in per[w].values() if c != "ER30001"])
    print(f"individual file: {len(cols)} columns ...", flush=True)
    d = read(IND, cols, pos)
    d = d[(d.ER30001 <= 2930) | d.ER30001.between(5001, 6872)]             # SRC + SEO
    # birth year: the latest valid report (1983+); otherwise the median of wave - age. Reported ages in the early
    # waves are sometimes inconsistent (e.g. 16 in 1972, 9 in 1973), so age is wave - birth year throughout.
    b = d[byr].where((d[byr] >= 1880) & (d[byr] <= 2023))
    by_rep = b.ffill(axis=1).iloc[:, -1]
    implied = pd.concat([w - d[per[w]["age"]].where(d[per[w]["age"]].between(1, 120)) for w in WAVES], axis=1)
    d["byr"] = by_rep.fillna(implied.median(axis=1).round())
    rows = []
    for w in WAVES:
        p = per[w]
        x = pd.DataFrame({"pid": d.ER30001 * 1000 + d.ER30002, "fam68": d.ER30001, "female": (d.ER32000 == 2) * 1,
                          "wave": w, "int": d[p["int"]], "rel": d[p["rel"]], "age": w - d["byr"],
                          "seq": d[p["seq"]] if "seq" in p else np.where(d[p["rel"]] > 0, 1, 0),
                          "wt": d[p["wt"]] if "wt" in p else np.nan})
        x = x[(x["int"] > 0) & x["seq"].between(1, 20)]
        rows.append(x)
    return pd.concat(rows, ignore_index=True)


def family():
    out = []
    for i, w in enumerate(WAVES):
        folder = FAM / (f"fam{w}" if w < 1994 else f"fam{w}er")
        base = next(f for f in folder.glob("*.do") if "formats" not in f.name).with_suffix("")
        pos, labs = layout(base.with_suffix(".do"))
        idv = "V3" if w == 1968 else labs[1][0]        # 1968: V2 is the interview number x 10; V3 = ER30001
        cols = [idv, FAMINC[i], HLAB[i], WLAB[i], RACE[i]] + [c for c in (HBUS.get(w), WBUS.get(w)) if c]
        f = read(base, cols, pos)
        f = f.rename(columns={idv: "int", FAMINC[i]: "faminc", HLAB[i]: "hlab", WLAB[i]: "wlab", RACE[i]: "hrace"})
        if w in HBUS:
            f["hlab"] = f["hlab"] + f[HBUS[w]].clip(lower=0)
            f["wlab"] = f["wlab"] + f[WBUS[w]].clip(lower=0)
        f["wave"] = w
        out.append(f[["wave", "int", "faminc", "hlab", "wlab", "hrace"]])
        print(f"  family {w}: {len(f)} families", flush=True)
    return pd.concat(out, ignore_index=True)


def main():
    DATA.mkdir(exist_ok=True)
    py = individual().merge(family(), on=["wave", "int"], how="left", validate="m:1")
    py["age"] = py["age"].where(py["age"].between(0, 120))
    py["head"] = py["rel"].isin([1, 10]) & (py["seq"] == 1)
    py["wife"] = py["rel"].isin([2, 20, 22]) & ~py["head"]
    py["child"] = py["rel"].isin([3, 30, 33, 35]) & ~py["head"]
    hd = py[py["head"]][["wave", "int", "age"]].rename(columns={"age": "hage"}).drop_duplicates(["wave", "int"])
    py = py.merge(hd, on=["wave", "int"], how="left")
    py["hrace"] = py["hrace"].map({1: "White", 2: "Black"})
    yr = py["wave"] - 1
    for c in ("faminc", "hlab", "wlab"):
        py[c] = [to2000(v, y) for v, y in zip(py[c], yr)]
    py["earn"] = np.where(py["head"], py["hlab"], np.where(py["wife"], py["wlab"], np.nan))
    py["birth_year"] = py["wave"] - py["age"]
    py.to_pickle(DATA / "psid_person_year.pkl")
    print(f"person-years: {len(py):,}", flush=True)

    # ---- parents: the family unit the child lives in at 12-17
    k = py[py["child"] & py["age"].between(12, 17)].copy()
    k["dist"] = (k["age"] - 16).abs() + (k["age"] > 16) * 0.5                 # 16, then 15, then 17
    pt = k[k["age"].between(15, 17)].sort_values(["pid", "dist"]).groupby("pid").first()
    pt = pt[["fam68", "female", "wave", "age", "faminc", "hage", "hrace", "wt"]].rename(
        columns={"wave": "wave_pt", "age": "age_pt", "faminc": "pinc_pt", "hage": "page_pt", "hrace": "race",
                 "wt": "wt_pt"})
    g = k.groupby("pid")
    av = pd.DataFrame({"pinc_av": g["faminc"].mean(), "n_av": g["faminc"].count(), "page_av": g["hage"].mean()})
    kids = pt.join(av, how="left")
    kids["lpinc_pt"] = np.log(kids["pinc_pt"].where(kids["pinc_pt"] > 0))
    kids["lpinc_av"] = np.log(kids["pinc_av"].where((kids["pinc_av"] > 0) & (kids["n_av"] >= 3)))
    kids["birth_year"] = kids["wave_pt"] - kids["age_pt"]

    # ---- the child as an adult: head or wife at 25-55
    a = py[(py["head"] | py["wife"]) & py["age"].between(AGE_LO, AGE_HI) & py["pid"].isin(kids.index)]
    e = lifetime(a.dropna(subset=["earn"]), "earn").add_suffix("_earn")
    f = lifetime(a.dropna(subset=["faminc"]), "faminc").add_suffix("_fam")
    kids = kids.join(e[["log_earn", "n_earn", "age_mean_earn"]]).join(f[["log_fam", "n_fam", "age_mean_fam"]])
    kids.index.name = "pid"
    kids = kids.reset_index()
    kids.to_pickle(DATA / "psid_kids.pkl")
    print(kids[["lpinc_pt", "lpinc_av", "log_earn", "log_fam"]].notna().groupby(kids["race"]).sum())


if __name__ == "__main__":
    main()
