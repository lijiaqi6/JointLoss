r"""NLSY97: parents' household income in 1996-99 and the respondent's adult earnings (2026-10-16).

Reads the full public NLSY97 release in Dropbox/NLS (read only; only the columns needed) and writes data/:
  nlsy97_kids.pkl         one row per Black / non-Black non-Hispanic respondent (cross-sectional + oversample;
                          'White' below = non-Black non-Hispanic, the NLSY97 category) living with a parent figure in
                          1997 (CV_YTH_REL_HH_CURRENT 1-6): gross household income (CV_INCOME_GROSS_YR, from the
                          parent interview in 1997) (a) in 1997 (income of 1996), (b) the mean over the 1997-2000
                          rounds while the respondent still lives with a parent; the mother's age in 1997 (her age at
                          the respondent's birth + his / her age); lifetime own earnings (wages + business income,
                          YINC-1700 + YINC-2100) and family income (CV_INCOME_FAMILY) at ages 25-55 (here 25-43).
  nlsy97_person_year.pkl  respondent x round at ages 25-55 (the reliability-ratio sample).
"""
from pathlib import Path

import numpy as np
import pandas as pd

from common import DATA, AGE_LO, AGE_HI, to2000, nls_index, nls_pick, nls_money, lifetime
import os
DROPBOX = Path(os.environ.get("DROPBOX", Path.home() / "Dropbox"))   # raw data, read only

SRC = Path(DROPBOX / "NLS/nlsy97_all_1997-2023")
CDB, CSV = SRC / "nlsy97_all_1997-2023.cdb", SRC / "nlsy97_all_1997-2023.csv"
RACE = {1: "Black", 4: "White"}


def main():
    DATA.mkdir(exist_ok=True)
    ix = nls_index(CDB)
    wage, bus = nls_pick(ix, ["YINC-1700"]), nls_pick(ix, ["YINC-2100"])
    pinc, finc = nls_pick(ix, ["CV_INCOME_GROSS_YR"]), nls_pick(ix, ["CV_INCOME_FAMILY"])
    inc = {**pinc, **finc}
    rel, age = nls_pick(ix, ["CV_YTH_REL_HH_CURRENT"]), nls_pick(ix, ["CV_AGE_INT_DATE"])
    keep = {"R0000100": "pid", "R0536300": "sex", "R0536402": "birth_year", "R1482600": "race_eth",
            "R1235800": "cross", "R1236101": "wt97", "R1193000": "hhid", "R1200200": "mom_age_birth"}
    cols = list(dict.fromkeys(list(keep) + [c for m in (wage, bus, inc, rel, age) for c in m.values()]))
    print(f"reading {len(cols)} columns ...", flush=True)
    d = pd.read_csv(CSV, usecols=cols).rename(columns=keep)
    d = d[d["race_eth"].isin(list(RACE))].copy()
    d["race"] = d["race_eth"].map(RACE)
    d["female"] = (d["sex"] == 2) * 1

    rows = []
    for y in sorted(age):
        x = pd.DataFrame({"pid": d["pid"].values, "round": y,
                          "age": pd.to_numeric(d[age[y]], errors="coerce").where(lambda s: s > 0).values})
        # household income: -4 (valid skip) means 'not asked', not zero income - in 1998-2000 it is skipped for most
        # youths still living at home - so every negative code is missing (unlike earnings components, nls_money)
        if y in inc:
            hh = pd.to_numeric(d[inc[y]], errors="coerce").astype(float)
            x["faminc"] = to2000(hh.where(hh >= 0).values, y - 1)
        else:
            x["faminc"] = np.nan
        x["earn"] = (to2000(nls_money(d[wage[y]]).values + np.nan_to_num(nls_money(d[bus[y]]).values), y - 1)
                     if y in wage else np.nan)
        x["with_parent"] = d[rel[y]].between(1, 6).values if y in rel else False
        rows.append(x)
    L = pd.concat(rows, ignore_index=True).merge(d[["pid", "race", "female", "birth_year", "hhid"]], on="pid")

    k = d.set_index("pid")[["race", "female", "birth_year", "wt97", "hhid", "mom_age_birth"]].copy()
    P = L[L["round"].between(1997, 2000)].pivot(index="pid", columns="round", values="faminc")
    W = L[L["round"].between(1997, 2000)].pivot(index="pid", columns="round", values="with_parent").astype(bool)
    k["age97"] = L[L["round"] == 1997].set_index("pid")["age"]
    k["par1997"] = W[1997]
    k["pinc_pt"] = P[1997].where(W[1997])
    pa = P.where(W)
    k["pinc_av"] = pa.mean(axis=1).where(W[1997])
    k["n_av"] = pa.notna().sum(axis=1)
    k["lpinc_pt"] = np.log(k["pinc_pt"].where(k["pinc_pt"] > 0))
    k["lpinc_av"] = np.log(k["pinc_av"].where(k["pinc_av"] > 0))
    mab = k["mom_age_birth"].where(k["mom_age_birth"].between(10, 60))
    k["page_pt"] = mab + k["age97"]
    k["page_av"] = k["page_pt"] + (k["n_av"] - 1) / 2

    a = L[L["age"].between(AGE_LO, AGE_HI)]
    a.to_pickle(DATA / "nlsy97_person_year.pkl")
    e = lifetime(a.dropna(subset=["earn"]), "earn").add_suffix("_earn")
    f = lifetime(a.dropna(subset=["faminc"]), "faminc").add_suffix("_fam")
    k = k.join(e[["log_earn", "n_earn", "age_mean_earn"]]).join(f[["log_fam", "n_fam", "age_mean_fam"]])
    k = k[k["par1997"]].reset_index()
    k["fam68"] = k["hhid"]                      # cluster = 1997 household (siblings)
    k.to_pickle(DATA / "nlsy97_kids.pkl")
    print(k.groupby(["race", "female"])[["lpinc_pt", "lpinc_av", "log_earn", "log_fam"]].count())
    print(k.groupby("race")[["age97", "page_pt", "n_earn", "age_mean_earn"]].mean().round(1))
    print(a.groupby("round").agg(age=("age", "median"), earn=("earn", "median"),
                                 zero=("earn", lambda s: (s == 0).mean()), fam=("faminc", "median")).round(2))


if __name__ == "__main__":
    main()
