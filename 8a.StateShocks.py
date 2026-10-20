r"""State x year labor-market shocks for the first stage (2026-10-17).

Writes data/state_shocks.pkl (one row per state FIPS x year) and output/state_shocks_checks.md.
Self-contained (no import from common.py) so that it can be run with `python -I`, as the BLS download is untrusted
data.

1. State unemployment rate, annual, 1976-2024
   ur_laus  BLS LAUS, series LASST{FIPS}0000000000003 (seasonally adjusted monthly rate; annual = mean of the 12
            months). Public API v1 without a key (25 series x 10 years per call). The raw JSON replies are saved in
            Dropbox/BLS/laus_state_ur_{first}_{last}_b{k}.json and re-used when present (no re-download).
   ur_ukcpr UKCPR National Welfare Data (Jan 2026 update), column 'Unemployment rate', 1980-2024: check only.
   ur       = ur_laus where present, else ur_ukcpr.
   ur_f_cps, ur_m_cps  women's / men's unemployment rate (16+) from the CPS MORG files, 1979-2019 (noisy in small
            states; supplementary).

2. Gender-specific Bartik labor-demand shocks, 1980-2019, from the CPS MORG files (Dropbox/MORG/morgYY.dta).
   Employment = employed civilians 16+ (esr 1-2 in 1979-88, lfsr89 1-2 in 1989-93, lfsr94 1-2 from 1994) with an
   industry code, weighted by the CPS final weight. Industries = 16 broad sectors, built from the 1970 Census codes
   (ind70, 1979-82), the 1980 / 1990 codes (ind80, 1983-2002) and the 2002 / 2007 / 2012 codes (ind02, 2003-19);
   crosswalk in SECTORS below (published as output/state_shocks_checks.md). Bridges: 2000-02 carry both ind80 and
   ind02, so the 2002->03 growth is computed with ind02 in both years; 1983 has no usable dual coding (ind70 in the
   1983 file is a placeholder), so the 1982->83 growth crosses the 1970 -> 1980 code change (flag `vintage_break`).
     g_{-s,k,t}^x = ln E^x_{k,t,-s} - ln E^x_{k,t-1,-s}       national growth of sex-x employment in sector k,
                                                             leaving out state s
     bartik_x[s,t] = sum_k w^x_{s,k} g_{-s,k,t}^x             w = state s's sex-x employment share of sector k
   Versions: base shares pooled over 1979-81 (bartik_f, bartik_m); rolling shares pooled over t-4..t-2
   (bartik_f_lag, bartik_m_lag; from 1983, base shares before); and the same with the growth of both sexes'
   employment in the sector (bartik_f_all, bartik_m_all), so that the women-men difference comes from the
   industry mix alone. Units: log points x 100 (percent growth).
   Also the actual state employment growth by sex (empgr_f, empgr_m), to check that the Bartik predicts it.
"""
import json
import time
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
import os
DROPBOX = Path(os.environ.get("DROPBOX", Path.home() / "Dropbox"))   # raw data, read only (Mac: export DROPBOX)

HERE = Path(__file__).resolve().parent
DATA, OUT = Path(os.environ.get("IGE_DATA", HERE / "data")), HERE / "output"
MORG = Path(DROPBOX / "MORG")
BLS = Path(DROPBOX / "BLS")
UKCPR = HERE.parent / "ExternalData" / "ukcpr_national_welfare_data_1980_2024_jan26update.xlsx"

FIPS = [1, 2, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32,
        33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48, 49, 50, 51, 53, 54, 55, 56]
# Census state code (MORG `state`, 1979-88) -> FIPS
CENSUS2FIPS = {11: 23, 12: 33, 13: 50, 14: 25, 15: 44, 16: 9, 21: 36, 22: 34, 23: 42, 31: 39, 32: 18, 33: 17,
               34: 26, 35: 55, 41: 27, 42: 19, 43: 29, 44: 38, 45: 46, 46: 31, 47: 20, 51: 10, 52: 24, 53: 11,
               54: 51, 55: 54, 56: 37, 57: 45, 58: 13, 59: 12, 61: 21, 62: 47, 63: 1, 64: 28, 71: 5, 72: 22, 73: 40,
               74: 48, 81: 30, 82: 16, 83: 56, 84: 8, 85: 35, 86: 4, 87: 49, 88: 32, 91: 53, 92: 41, 93: 6, 94: 2,
               95: 15}

# ---------------------------------------------------------------- industry crosswalk (inclusive code ranges)
# sector: {vintage: [(lo, hi), ...]}; vintage 70 = 1970 Census codes, 80 = 1980/1990 codes, 02 = 2002/07/12 codes.
# Conventions to keep sectors comparable across the SIC -> NAICS change: printing and publishing (incl. newspaper /
# book publishers) stay in nondurable manufacturing; the Postal Service goes to public administration; motion
# pictures / sound recording go to personal & entertainment services; libraries go to education; software
# publishing and data processing go to business services; waste management goes to transport & utilities; retail
# bakeries go to retail; child day care and residential care are with education & social services.
SECTORS = {
    "Agriculture, forestry, fishing": {70: [(17, 29)], 80: [(10, 32)], 2: [(170, 290)]},
    "Mining": {70: [(47, 58)], 80: [(40, 50)], 2: [(370, 490)]},
    "Construction": {70: [(67, 78)], 80: [(60, 60)], 2: [(770, 770)]},
    "Durable manufacturing": {70: [(107, 267)], 80: [(230, 392)], 2: [(2470, 3990)]},
    "Nondurable manufacturing (incl. printing, publishing)": {
        70: [(268, 399)], 80: [(100, 222)], 2: [(1070, 1180), (1270, 2390), (6470, 6480)]},
    "Transportation, utilities, sanitary": {
        70: [(407, 429), (467, 479), (499, 499)], 80: [(400, 411), (420, 432), (460, 472)],
        2: [(570, 690), (6070, 6290), (6380, 6390), (7790, 7790)]},
    "Communications, broadcasting, telecom": {70: [(447, 449)], 80: [(440, 442)],
                                             2: [(6670, 6692), (6780, 6780)]},
    "Wholesale trade": {70: [(507, 599)], 80: [(500, 571)], 2: [(4070, 4590)]},
    "Retail trade (excl. eating, drinking)": {70: [(607, 668), (677, 699)], 80: [(580, 640), (642, 691)],
                                              2: [(1190, 1190), (4670, 5790)]},
    "Eating, drinking, accommodation": {70: [(669, 669), (777, 778)], 80: [(641, 641), (762, 770)],
                                        2: [(8660, 8690)]},
    "Finance, insurance, real estate": {70: [(707, 719)], 80: [(700, 712)], 2: [(6870, 7190)]},
    "Business, repair, professional services": {
        70: [(727, 767), (849, 849), (888, 889), (897, 899)], 80: [(721, 760), (841, 841), (882, 893)],
        2: [(6490, 6490), (6695, 6695), (7270, 7780), (8770, 8890)]},
    "Personal, household, entertainment, membership": {
        70: [(769, 769), (779, 817), (869, 869), (877, 877), (887, 887)],
        80: [(761, 761), (771, 810), (872, 881)], 2: [(6570, 6590), (8560, 8590), (8970, 9290)]},
    "Health": {70: [(828, 848)], 80: [(812, 840)], 2: [(7970, 8270)]},
    "Education and social services": {70: [(857, 868), (878, 879)], 80: [(842, 871)],
                                      2: [(6770, 6770), (7860, 7890), (8290, 8290), (8370, 8470)]},
    "Public administration (incl. postal)": {70: [(907, 937)], 80: [(412, 412), (900, 932)],
                                             2: [(6370, 6370), (9370, 9590)]},
}
SNAMES = list(SECTORS)


def sector_of(codes, vintage):
    out = pd.Series(np.nan, index=codes.index)
    for i, (name, d) in enumerate(SECTORS.items()):
        for lo, hi in d[vintage]:
            out[(codes >= lo) & (codes <= hi)] = i
    return out


# ---------------------------------------------------------------- 1. unemployment rates
def download_laus(first=1976, last=2025):
    assert BLS.is_dir(), "Dropbox/BLS must exist (no new Dropbox folders)"
    ids = [f"LASST{f:02d}0000000000003" for f in FIPS]
    files = []
    for k in range(0, len(ids), 25):
        for y0 in range(first, last + 1, 10):
            y1 = min(y0 + 9, last)
            fn = BLS / f"laus_state_ur_{y0}_{y1}_b{k // 25}.json"
            files.append(fn)
            if fn.exists():
                continue
            body = json.dumps({"seriesid": ids[k:k + 25], "startyear": str(y0), "endyear": str(y1)}).encode()
            req = urllib.request.Request("https://api.bls.gov/publicAPI/v1/timeseries/data/", data=body,
                                         headers={"Content-type": "application/json"})
            raw = urllib.request.urlopen(req, timeout=120).read()
            d = json.loads(raw)
            if d.get("status") != "REQUEST_SUCCEEDED":
                raise RuntimeError(f"BLS API refused: {d.get('status')} {d.get('message')}")
            fn.write_bytes(raw)
            print(f"  downloaded {fn.name}", flush=True)
            time.sleep(1)
    return files


def laus():
    try:
        files = download_laus()
    except Exception as e:                                      # documented fall-back: UKCPR only
        print(f"BLS LAUS download failed ({e}); using UKCPR only", flush=True)
        return pd.DataFrame(columns=["fips", "year", "ur_laus"])
    rows = []
    for fn in files:
        d = json.loads(fn.read_text())
        for s in d["Results"]["series"]:
            f = int(s["seriesID"][5:7])
            for o in s["data"]:
                v = pd.to_numeric(o["value"], errors="coerce")            # '-' = not available
                if o["period"].startswith("M") and o["period"] != "M13" and pd.notna(v):
                    rows.append((f, int(o["year"]), int(o["period"][1:]), float(v)))
    m = pd.DataFrame(rows, columns=["fips", "year", "month", "ur"]).drop_duplicates(["fips", "year", "month"])
    g = m.groupby(["fips", "year"])["ur"].agg(["mean", "count"]).reset_index()
    g = g[g["count"] == 12].rename(columns={"mean": "ur_laus"})
    return g[["fips", "year", "ur_laus"]]


def ukcpr():
    d = pd.read_excel(UKCPR, sheet_name="Data", usecols=["state_fips", "year", "Unemployment rate"])
    d = d.rename(columns={"state_fips": "fips", "Unemployment rate": "ur_ukcpr"}).dropna(subset=["fips", "year"])
    d[["fips", "year"]] = d[["fips", "year"]].astype(int)
    d["ur_ukcpr"] = pd.to_numeric(d["ur_ukcpr"], errors="coerce")
    if d["ur_ukcpr"].max() < 1:                                 # stored as a fraction
        d["ur_ukcpr"] *= 100
    return d[d["fips"].isin(FIPS)]


# ---------------------------------------------------------------- 2. MORG
def read_morg(yy):
    fn = MORG / f"morg{yy:02d}.dta"
    with pd.io.stata.StataReader(fn) as r:
        have = set(r.variable_labels())
    st = "stfips" if "stfips" in have else "state"
    lf = next(v for v in ("lfsr94", "lfsr89", "esr") if v in have)
    inds = [v for v in ("ind70", "ind80", "ind02") if v in have]
    d = pd.read_stata(fn, columns=[st, lf, "sex", "age", "weight", "intmonth"] + inds, convert_categoricals=False)
    year = 1900 + yy if yy >= 79 else 2000 + yy
    d["fips"] = d[st].map(CENSUS2FIPS) if st == "state" else d[st]
    d = d[d["age"] >= 16]
    if lf == "esr":                                             # 1 at work, 2 job not at work, 3 unemployed
        d["emp"], d["unemp"] = d[lf].isin([1, 2]), d[lf] == 3
    else:                                                       # 1-2 employed, 3 layoff, 4 looking
        d["emp"], d["unemp"] = d[lf].isin([1, 2]), d[lf].isin([3, 4])
    d["female"] = (d["sex"] == 2).astype(int)
    if year <= 1982:
        d["sec"] = sector_of(d["ind70"], 70)
    elif year <= 2002:
        d["sec"] = sector_of(d["ind80"], 80)
    else:
        d["sec"] = sector_of(d["ind02"], 2)
    d["sec02"] = sector_of(d["ind02"], 2) if "ind02" in d and year <= 2002 else np.nan
    d["half"] = (d["intmonth"] % 2).astype(int)                 # odd / even interview months (split-sample check)
    d["year"] = year
    return d[["year", "fips", "female", "emp", "unemp", "sec", "sec02", "half", "weight"]]


def morg_cells():
    emp, lfs, alt, cover = [], [], [], []
    for yy in list(range(79, 100)) + list(range(0, 20)):
        d = read_morg(yy)
        y = int(d["year"].iloc[0])
        e = d[d["emp"]]
        cover.append((y, len(d), len(e), e["sec"].notna().mean(), e["fips"].nunique()))
        emp.append(e.dropna(subset=["sec"]).groupby(["year", "fips", "female", "sec", "half"])["weight"].sum())
        if y == 2002:
            alt.append(e.dropna(subset=["sec02"]).groupby(["year", "fips", "female", "sec02", "half"])["weight"]
                       .sum().rename_axis(["year", "fips", "female", "sec", "half"]))
        lf = d[d["emp"] | d["unemp"]]
        lfs.append(lf.groupby(["year", "fips", "female"]).apply(
            lambda x: 100 * np.average(x["unemp"], weights=x["weight"]), include_groups=False).rename("ur_cps"))
        print(f"  MORG {y}: {len(d):,} persons 16+, {len(e):,} employed, sector coded {cover[-1][3]:.3f}",
              flush=True)
    E = pd.concat(emp).rename("E").reset_index()
    E2002 = pd.concat(alt).rename("E").reset_index()
    U = pd.concat(lfs).reset_index()
    return E, E2002, U, pd.DataFrame(cover, columns=["year", "n16", "n_emp", "share_sector_coded", "n_states"])


def cells(E, half=None):
    """employment by year x state x sex x sector, from both halves of the sample or from one."""
    x = E if half is None else E[E["half"] == half]
    return x.groupby(["year", "fips", "female", "sec"], as_index=False)["E"].sum()


def full_grid(E):
    idx = pd.MultiIndex.from_product([sorted(E["year"].unique()), FIPS, [0, 1], range(len(SNAMES))],
                                     names=["year", "fips", "female", "sec"])
    return E.set_index(["year", "fips", "female", "sec"])["E"].reindex(idx, fill_value=0.0)


def nat_growth(E, E2002, pooled=False, loo=True):
    """g[year, fips, female, sec]: growth (x100) of national employment in sec (own sex, or both sexes if
    pooled), leaving out the state if loo."""
    G = full_grid(E)
    A = full_grid(E2002)
    if pooled:                                                  # both sexes' employment in the sector
        G = G.groupby(["year", "fips", "sec"]).transform("sum")
        A = A.groupby(["year", "fips", "sec"]).transform("sum")
    nat = G.groupby(["year", "female", "sec"]).transform("sum")
    nat_a = A.groupby(["year", "female", "sec"]).transform("sum")
    L = nat - G if loo else nat                                 # national minus own state
    L_a = ((nat_a - A) if loo else nat_a).droplevel("year")
    out = []
    years = sorted(E["year"].unique())
    for t in years[1:]:
        cur = L.xs(t, level="year")
        prev = L_a if t == 2003 else L.xs(t - 1, level="year")         # 2002->03: ind02 in both years
        g = 100 * (np.log(cur) - np.log(prev.reindex(cur.index)))
        out.append(g.rename("g").reset_index().assign(year=t))
    return pd.concat(out, ignore_index=True).set_index(["year", "fips", "female", "sec"])["g"]


def shares(E, years):
    G = full_grid(E)
    G = G[G.index.get_level_values("year").isin(years)].groupby(["fips", "female", "sec"]).sum()
    return (G / G.groupby(["fips", "female"]).transform("sum")).rename("w")


def shift_share(g, E_shares, lag=False):
    """sum_k w_{s,k} g_{s,k,t} by state x sex x year; base shares 1979-81, or rolling t-4..t-2 if lag."""
    wb = shares(E_shares, [1979, 1980, 1981])
    rows = []
    for t in range(1980, 2020):
        w = shares(E_shares, [t - 4, t - 3, t - 2]) if (lag and t >= 1983) else wb
        b = (w * g.xs(t, level="year").reindex(w.index)).groupby(["fips", "female"]).sum(min_count=1)
        rows.append(b.rename("b").reset_index().assign(year=t))
    return pd.concat(rows, ignore_index=True)


# suffix: (both sexes' sector growth?, leave own state out?, rolling lagged shares?)
SPECS = {"": (False, True, False), "_lag": (False, True, True), "_all": (True, True, False),
         "_nat": (False, False, False)}


def bartik(E, E2002):
    out = []
    for suf, (pooled, loo, lag) in SPECS.items():
        b = shift_share(nat_growth(E, E2002, pooled, loo), E, lag)
        b["variable"] = np.where(b["female"] == 1, "bartik_f", "bartik_m") + suf
        out.append(b)
    B = pd.concat(out)
    return B.pivot_table(index=["fips", "year"], columns="variable", values="b").reset_index()


def actual_growth(E, names=("empgr_m", "empgr_f")):
    S = full_grid(E).groupby(["year", "fips", "female"]).sum().unstack("female")
    g = 100 * np.log(S).groupby(level="fips").diff()
    g.columns = list(names)
    return g.reset_index()


def split_sample(E, E2002):
    """Bartik built from the even-month half (national growth) vs actual state growth in the odd-month half:
    the two CPS samples are independent, so CPS sampling noise in the state's own cells cannot create a mechanical
    correlation (it does in the full sample: + with own state included, - with it left out)."""
    E0, E1 = cells(E, 0), cells(E, 1)
    A02 = cells(E2002, 0)
    out = actual_growth(E1, ("empgr_m_odd", "empgr_f_odd"))
    for suf, loo in (("_nat_even", False), ("_loo_even", True)):
        b = shift_share(nat_growth(E0, A02, False, loo), cells(E), False)
        b = b.pivot_table(index=["fips", "year"], columns="female", values="b").reset_index()
        b.columns = ["fips", "year", "bartik_m" + suf, "bartik_f" + suf]
        out = out.merge(b, on=["fips", "year"], how="left")
    return out


def fe_resid_reg(df, y, xs):
    """OLS of y on xs with state and year FE (two-way demeaning by dummies), state-clustered s.e."""
    import statsmodels.api as sm
    d = df[[y, *xs, "fips", "year"]].dropna()
    X = pd.concat([d[xs], pd.get_dummies(d["fips"], prefix="s", drop_first=True, dtype=float),
                   pd.get_dummies(d["year"], prefix="y", drop_first=True, dtype=float)], axis=1)
    r = sm.OLS(d[y], sm.add_constant(X)).fit(cov_type="cluster", cov_kwds={"groups": d["fips"]})
    return r, len(d)


def main():
    DATA.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    print("1. unemployment rates", flush=True)
    L, U = laus(), ukcpr()
    print("2. MORG", flush=True)
    E_h, E2002_h, Ucps, cover = morg_cells()
    E, E2002 = cells(E_h), cells(E2002_h)
    B = bartik(E, E2002)
    A = actual_growth(E)
    SS = split_sample(E_h, E2002_h)
    Uc = Ucps.pivot_table(index=["year", "fips"], columns="female", values="ur_cps").reset_index()
    Uc.columns = ["year", "fips", "ur_m_cps", "ur_f_cps"]

    grid = pd.DataFrame([(f, y) for f in FIPS for y in range(1976, 2025)], columns=["fips", "year"])
    S = (grid.merge(L, on=["fips", "year"], how="left").merge(U, on=["fips", "year"], how="left")
         .merge(Uc, on=["fips", "year"], how="left").merge(B, on=["fips", "year"], how="left")
         .merge(A, on=["fips", "year"], how="left").merge(SS, on=["fips", "year"], how="left"))
    S["ur"] = S["ur_laus"].fillna(S["ur_ukcpr"])
    S["ur_src"] = np.where(S["ur_laus"].notna(), "LAUS", np.where(S["ur_ukcpr"].notna(), "UKCPR", ""))
    S["vintage_break"] = (S["year"] == 1983).astype(int)
    S = S.sort_values(["fips", "year"]).reset_index(drop=True)
    S.to_pickle(DATA / "state_shocks.pkl")

    # ---------------------------------------------------------------- checks
    lines = ["# State shocks: checks (8a.StateShocks.py)", ""]
    lines += ["## Unemployment rate sources", "",
              f"- LAUS rows: {S['ur_laus'].notna().sum()} (years {S.loc[S.ur_laus.notna(), 'year'].min()}-"
              f"{S.loc[S.ur_laus.notna(), 'year'].max()}); UKCPR rows: {S['ur_ukcpr'].notna().sum()}.",
              f"- corr(LAUS, UKCPR) = {S[['ur_laus', 'ur_ukcpr']].corr().iloc[0, 1]:.4f}; "
              f"mean abs diff = {(S.ur_laus - S.ur_ukcpr).abs().mean():.3f} pp.",
              f"- corr(LAUS, CPS women) = {S[['ur_laus', 'ur_f_cps']].corr().iloc[0, 1]:.3f}; "
              f"corr(LAUS, CPS men) = {S[['ur_laus', 'ur_m_cps']].corr().iloc[0, 1]:.3f}.",
              f"- ur range {S['ur'].min():.1f}-{S['ur'].max():.1f}; share outside 2-15%: "
              f"{((S['ur'] < 2) | (S['ur'] > 15)).mean():.4f}.", ""]
    yr = S.groupby("year").agg(ur_mean=("ur", "mean"), ur_min=("ur", "min"), ur_max=("ur", "max"),
                               bartik_f=("bartik_f", "mean"), bartik_m=("bartik_m", "mean"),
                               sd_bf=("bartik_f", "std"), sd_bm=("bartik_m", "std"),
                               corr_fm=("bartik_f", lambda s: s.corr(S.loc[s.index, "bartik_m"])))
    lines += ["## By year (means across 51 states; Bartik in % growth)", "", yr.round(3).to_markdown(), ""]
    lines += ["## MORG coverage", "", cover.round(3).to_markdown(index=False), ""]
    # first stage of the Bartik on actual employment growth, two-way FE
    lines += ["## Do the Bartik shocks predict actual state employment growth? (state + year FE, state-clustered)",
              "", "Full-sample rows are contaminated by CPS sampling noise in the state's own cells: negatively for "
              "the leave-one-out versions, positively for `_nat` (own state included). The split-sample rows "
              "(national growth from even interview months, actual growth from odd months: independent samples) "
              "are the clean check.", "",
              "| outcome | regressor(s) | coef | s.e. | p | N |", "|---|---|---|---|---|---|"]
    specs = [("empgr_f", ["bartik_f"]), ("empgr_m", ["bartik_m"]), ("empgr_f", ["bartik_f", "bartik_m"]),
             ("empgr_m", ["bartik_f", "bartik_m"]), ("empgr_f", ["bartik_f_lag"]), ("empgr_m", ["bartik_m_lag"]),
             ("empgr_f", ["bartik_f_nat"]), ("empgr_m", ["bartik_m_nat"]),
             ("empgr_f_odd", ["bartik_f_nat_even"]), ("empgr_m_odd", ["bartik_m_nat_even"]),
             ("empgr_f_odd", ["bartik_f_nat_even", "bartik_m_nat_even"]),
             ("empgr_f_odd", ["bartik_f_loo_even"]), ("empgr_m_odd", ["bartik_m_loo_even"]),
             ("ur", ["bartik_f", "bartik_m"]), ("ur_f_cps", ["bartik_f", "bartik_m"]),
             ("ur_m_cps", ["bartik_f", "bartik_m"])]
    for y, xs in specs:
        yrs = (1983, 2019) if y.endswith("_odd") else (1980, 2019)
        r, n = fe_resid_reg(S[S.year.between(*yrs)], y, xs)
        for x in xs:
            lines.append(f"| {y} | {x} (with {', '.join(xs)}) | {r.params[x]:.3f} | {r.bse[x]:.3f} | "
                         f"{r.pvalues[x]:.3g} | {n} |")
    d = S[S.year.between(1980, 2019)].dropna(subset=["bartik_f", "bartik_m"]).copy()
    for v in ("bartik_f", "bartik_m"):
        d[v + "_r"] = d[v] - d.groupby("fips")[v].transform("mean") - d.groupby("year")[v].transform("mean") \
            + d[v].mean()
    lines += ["", f"corr(bartik_f, bartik_m) raw = {d[['bartik_f', 'bartik_m']].corr().iloc[0, 1]:.3f}; after "
              f"removing state and year means = {d[['bartik_f_r', 'bartik_m_r']].corr().iloc[0, 1]:.3f}; "
              f"s.d. of the two-way residuals: f {d['bartik_f_r'].std():.3f}, m {d['bartik_m_r'].std():.3f}.", ""]
    w = shares(E, [1979, 1980, 1981]).groupby(["female", "sec"]).mean().unstack("female")
    w.index = [SNAMES[int(i)] for i in w.index]
    w.columns = ["men (mean state share)", "women (mean state share)"]
    lines += ["## Base-period (1979-81) sector shares, mean across states", "", w.round(3).to_markdown(), ""]
    xw = []
    for name, d_ in SECTORS.items():
        f = lambda rs: ", ".join(f"{a}-{b}" if a != b else f"{a}" for a, b in rs)
        xw.append((name, f(d_[70]), f(d_[80]), f(d_[2])))
    lines += ["## Industry crosswalk (Census industry codes, inclusive ranges)", "",
              pd.DataFrame(xw, columns=["sector", "1970 codes (1979-82)", "1980/1990 codes (1983-2002)",
                                        "2002/2007/2012 codes (2003-19)"]).to_markdown(index=False), ""]
    gn = nat_growth(E, E2002).reset_index()
    gn = gn[gn.fips == 6].groupby(["year", "female", "sec"])["g"].first().unstack(["female", "sec"])
    jump = gn.loc[[1981, 1982, 1983, 1984, 1985, 2002, 2003, 2004]].T.groupby(level=0).apply(
        lambda x: x.abs().mean()).T
    lines += ["## Mean |national sector growth| (excl. CA) around code changes, by sex (0 men, 1 women)", "",
              jump.round(2).to_markdown(), ""]
    (OUT / "state_shocks_checks.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[:12]))
    print(yr.round(2).to_string())


if __name__ == "__main__":
    main()
