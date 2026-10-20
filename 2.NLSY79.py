r"""NLSY79: parents' family income in 1978-80 and the respondent's adult earnings (2026-10-16).

Reads the full public NLSY79 release in Dropbox/NLS (read only; only the columns needed) and writes data/:
  nlsy79_codebook.csv   codebook index (column, question name, year, title)
  nlsy79_kids.pkl       one row per White / Black respondent (cross-sectional + Black supplemental samples; the
                        poor-White supplemental, Hispanic and military samples left out) who lives with a parent in
                        1979: the family's total net income (TNFI_TRUNC) (a) in the 1979 round (income of 1978),
                        (b) the mean over the 1979-81 rounds in which a parent still lives with the respondent; the
                        parent's age in 1979 (father if present, else mother, from the household roster); the
                        respondent's lifetime own earnings (wages and salary + farm / business income) and family
                        income (mean over the rounds at ages 25-55, zeros kept). Real 2000 dollars of the income year.
  nlsy79_person_year.pkl  respondent x round at ages 25-55: earnings, family income (the reliability-ratio sample).
"""
from pathlib import Path

import numpy as np
import pandas as pd

from common import DATA, AGE_LO, AGE_HI, to2000, nls_index, nls_pick as pick, nls_money, lifetime
import os
DROPBOX = Path(os.environ.get("DROPBOX", Path.home() / "Dropbox"))   # raw data, read only

SRC = Path(DROPBOX / "NLS/nlsy79_all_1979-2022")
CDB, CSV = SRC / "nlsy79_all_1979-2022.cdb", SRC / "nlsy79_all_1979-2022.csv"
SAMPLES = {1: "White", 2: "White", 5: "White", 6: "White", 3: "Black", 7: "Black", 10: "Black", 13: "Black"}
PARENT = {4, 5, 37, 38, 47}                     # father, mother, step-father, step-mother, parents


def main():
    DATA.mkdir(exist_ok=True)
    ix = nls_index(CDB)
    ix.to_csv(DATA / "nlsy79_codebook.csv", index=False)
    wage = pick(ix, ["Q13-5_TRUNC_REVISED", "Q13-5_TRUNC", "Q13-5"], "WAGES AND SALARY")
    bus = pick(ix, ["Q13-9_TRUNC_REVISED", "Q13-9_TRUNC", "Q13-9"], "FARM OR BUSINESS")
    tnfi = pick(ix, ["TNFI_TRUNC"])
    age = pick(ix, ["AGEATINT"])
    rounds = sorted(set(tnfi) & set(age))
    rel ={y: ix[ix.qname.str.match(r"^HHI_FINAL_RELCODE\.\d\d$", na=False) & (ix.year == str(y))].sort_values("qname")
           for y in (1979, 1980, 1981)}
    agec = ix[ix.qname.str.match(r"^HHI_FINAL_AGE\.\d\d$", na=False) & (ix.year == "1979")].sort_values("qname")
    keep = {"R0000100": "id", "R0173600": "sample_id", "R0214800": "sex", "R0000500": "birth_year",
            "R0216100": "wt79", "R0000149": "hhid"}
    cols = (list(keep) + list(wage.values()) + list(bus.values()) + list(tnfi.values()) + list(age.values())
            + [c for y in rel for c in rel[y].col] + list(agec.col))
    cols = list(dict.fromkeys(cols))
    print(f"reading {len(cols)} columns ...", flush=True)
    d = pd.read_csv(CSV, usecols=cols).rename(columns=keep)
    d = d[d["sample_id"].isin(list(SAMPLES))].copy()
    d["race"] = d["sample_id"].map(SAMPLES)
    d["female"] = (d["sex"] == 2) * 1
    d["birth_year"] = np.where(d["birth_year"] < 100, 1900 + d["birth_year"], d["birth_year"])

    # ---- parents present in the household, 1979-81 rounds; parent's age in 1979
    for y in rel:
        R = d[rel[y].col.tolist()].to_numpy()
        d[f"par{y}"] = np.isin(R, list(PARENT)).any(axis=1)
    R = d[rel[1979].col.tolist()].to_numpy()
    A = d[agec.col.tolist()].to_numpy().astype(float)
    A[A < 0] = np.nan
    fa = np.where(np.isin(R, [4, 37]), A, np.nan)
    mo = np.where(np.isin(R, [5, 38]), A, np.nan)
    with np.errstate(all="ignore"):
        d["page"] = np.where(np.isfinite(np.nanmax(fa, axis=1)), np.nanmax(fa, axis=1), np.nanmax(mo, axis=1))

    # ---- long: round x respondent
    rows = []
    for y in rounds:
        inc = y - 1
        x = pd.DataFrame({"id": d["id"].values, "round": y, "age": pd.to_numeric(d[age[y]], errors="coerce").values})
        x["age"] = x["age"].where(x["age"] > 0)
        x["faminc"] = to2000(nls_money(d[tnfi[y]]).values, inc)
        w = nls_money(d[wage[y]]).values if y in wage else np.full(len(d), np.nan)
        b = nls_money(d[bus[y]]).values if y in bus else np.zeros(len(d))
        x["earn"] = to2000(w + np.nan_to_num(b), inc)
        rows.append(x)
    L = pd.concat(rows, ignore_index=True).merge(d[["id", "race", "female", "birth_year", "hhid"]], on="id")

    # ---- parents' income
    k = d.set_index("id")[["race", "female", "birth_year", "wt79", "hhid", "page", "par1979", "par1980",
                           "par1981"]].copy()
    P = L[L["round"].isin([1979, 1980, 1981])].pivot(index="id", columns="round", values="faminc")
    k["age79"] = L[L["round"] == 1979].set_index("id")["age"]
    k["pinc_pt"] = P[1979].where(k["par1979"])
    pa = pd.concat([P[y].where(k[f"par{y}"]) for y in (1979, 1980, 1981)], axis=1)
    k["pinc_av"] = pa.mean(axis=1).where(k["par1979"])
    k["n_av"] = pa.notna().sum(axis=1)
    k["lpinc_pt"] = np.log(k["pinc_pt"].where(k["pinc_pt"] > 0))
    k["lpinc_av"] = np.log(k["pinc_av"].where(k["pinc_av"] > 0))
    k["page_pt"] = k["page"]
    k["page_av"] = k["page"] + (k["n_av"] - 1) / 2

    # ---- the respondent as an adult
    a = L[L["age"].between(AGE_LO, AGE_HI)].rename(columns={"id": "pid"})
    a.to_pickle(DATA / "nlsy79_person_year.pkl")
    e = lifetime(a.dropna(subset=["earn"]), "earn").add_suffix("_earn")
    f = lifetime(a.dropna(subset=["faminc"]), "faminc").add_suffix("_fam")
    k = k.join(e[["log_earn", "n_earn", "age_mean_earn"]]).join(f[["log_fam", "n_fam", "age_mean_fam"]])
    k = k[k["par1979"]].reset_index().rename(columns={"id": "pid"})
    k["fam68"] = k["hhid"]                      # cluster = 1979 household (siblings)
    k.to_pickle(DATA / "nlsy79_kids.pkl")
    print(k.groupby(["race", "female"])[["lpinc_pt", "lpinc_av", "log_earn", "log_fam"]].count())
    print(k.groupby("race")[["age79", "page", "n_earn", "age_mean_earn"]].mean().round(1))


if __name__ == "__main__":
    main()
