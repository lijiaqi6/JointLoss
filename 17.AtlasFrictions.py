r"""Opportunity Atlas outcomes by race vs local search frictions for women, by state (2026-10-17).

Descriptive, cross-sectional (N = 51 states incl. DC). Question: do children whose parents were at the same national
income percentile do differently, by race, in states where non-employed women find jobs more slowly?

Child outcomes (Chetty, Hendren, Jones, Porter 2020 QJE; Chetty, Friedman, Hendren, Jones, Porter 2018 Opportunity
Atlas), downloaded 2026-10-17 into data/ext/opportunity_insights/ (git-ignored):
  county_outcomes.zip (county_outcomes.csv; codebook Codebook-for-Table-5.pdf), https://opportunityinsights.org/data/
  kfr_[black|white]_pooled_p[25|75] = mean household income rank (2014-15, ages 31-37) of children born 1978-83
  whose parents were at the 25th / 75th percentile of the national parental income distribution (x 100 here).
  There is no state file: state values = averages of the county predictions, weighted by OI's preferred weights
  kid_[race]_pooled_blw_p50_n (children below the parental median) for p25 and by kid_[race]_pooled_n minus that
  count (children above the median) for p75. The White-Black gap is averaged within counties where both races have
  an estimate, with Black-children weights (the gap where Black children live).
  Weights for the state regressions: kid_black_pooled_n summed by state (Black children under 18, 2000 Census).
  Share Black = kid_black_pooled_n / kid_pooled_pooled_n by state.

Search friction for women (and men), by state, three periods:
  (A) 1977-1992, March CPS (Mare-Winship uniform extracts, Dropbox/CPS/mare_winship/extracted/cpsmwYY; childhood of
      the 1978-83 cohorts): annual re-employment rate = share employed in the March survey week among those who worked
      0 weeks in the previous calendar year (wwly1 == 0); looking share = unemployed / non-employed in March;
      ages 20-45, person supplemental weight. Monthly flows cannot be built from March cross-sections.
  (B) 1994-2000 and (C) 2005-2021, CPS basic monthly from the Census API (api.census.gov/data/YYYY/cps/basic/mon;
      downloaded to data/ext/cps_basic/, ages 20-46; the Dropbox cps_flows_2005_2021 file covers ages 16-25 only,
      so it cannot give rates for women 20-45). Monthly job finding of the non-employed = P(employed at t+1 |
      not employed at t) (U->E and N->E pooled), also U->E (unemployed at t) and N->E; persons matched across adjacent
      months by household id(s) + line number + state, months-in-sample 1-3 / 5-7 -> next, same sex and race, age
      change 0-1; month pairs where < 50% of eligible persons match (household-ID breaks: Jun-Sep 1995, Jan 1997,
      May 2004) are dropped. Ages 20-45 at t; composite weight at t. Looking share = unemployed / non-employed (all rotations).
  (C) is after the children's childhood (they were 22-43); (B) covers ages 11-22 of the cohorts.
Controls: state unemployment rate (BLS LAUS via UKCPR welfare data, ExternalData/), mean over the period that matches
the friction measure (1980-1992 for A; 1994-2000 for B; 2005-2021 for C), share Black among children (2000), Census
region FE. WLS with Black-children weights, HC1 s.e. Friction measures are standardised (per 1 SD across the 51
states, unweighted).
Writes output/atlas_frictions.csv (state data + regression coefficients), output/atlas_frictions.md, and
output/atlas_frictions.png. Downloaded files are data only; run this script with `python -I`.
"""
import gzip
import json
import os
import sys
import time
import urllib.error
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))                 # -I drops the script directory from sys.path

import numpy as np                            # noqa: E402
import pandas as pd                           # noqa: E402
import statsmodels.api as sm                  # noqa: E402

from common import DATA, OUT, stars           # noqa: E402
DROPBOX = Path(os.environ.get("DROPBOX", Path.home() / "Dropbox"))   # raw data, read only (Mac: export DROPBOX)

EXT = DATA / "ext"
OI = EXT / "opportunity_insights"
CPSB = EXT / "cps_basic"                      # Census API CPS basic monthly, ages 20-46, one csv.gz per month
MW = Path(DROPBOX / "CPS/mare_winship/extracted")
UKCPR = HERE.parent / "ExternalData" / "ukcpr_national_welfare_data_1980_2024_jan26update.xlsx"
MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
YEARS = list(range(1994, 2022))
AGE_LO, AGE_HI = 20, 45                       # age in month t; month t+1 rows kept up to AGE_HI + 1
MIN_MATCH = 0.5                               # month pairs with fewer valid matches are ID breaks (dropped)

# Census state codes (Mare-Winship 1977+) -> FIPS
CENSUS2FIPS = {11: 23, 12: 33, 13: 50, 14: 25, 15: 44, 16: 9, 21: 36, 22: 34, 23: 42, 31: 39, 32: 18, 33: 17, 34: 26,
               35: 55, 41: 27, 42: 19, 43: 29, 44: 38, 45: 46, 46: 31, 47: 20, 51: 10, 52: 24, 53: 11, 54: 51, 55: 54,
               56: 37, 57: 45, 58: 13, 59: 12, 61: 21, 62: 47, 63: 1, 64: 28, 71: 5, 72: 22, 73: 40, 74: 48, 81: 30,
               82: 16, 83: 56, 84: 8, 85: 35, 86: 4, 87: 49, 88: 32, 91: 53, 92: 41, 93: 6, 94: 2, 95: 15}
REGION = {**{f: "Northeast" for f in (9, 23, 25, 33, 34, 36, 42, 44, 50)},
          **{f: "Midwest" for f in (17, 18, 19, 20, 26, 27, 29, 31, 38, 39, 46, 55)},
          **{f: "South" for f in (1, 5, 10, 11, 12, 13, 21, 22, 24, 28, 37, 40, 45, 47, 48, 51, 54)},
          **{f: "West" for f in (2, 4, 6, 8, 15, 16, 30, 32, 35, 41, 49, 53, 56)}}
ABBR = {1: "AL", 2: "AK", 4: "AZ", 5: "AR", 6: "CA", 8: "CO", 9: "CT", 10: "DE", 11: "DC", 12: "FL", 13: "GA", 15: "HI",
        16: "ID", 17: "IL", 18: "IN", 19: "IA", 20: "KS", 21: "KY", 22: "LA", 23: "ME", 24: "MD", 25: "MA", 26: "MI",
        27: "MN", 28: "MS", 29: "MO", 30: "MT", 31: "NE", 32: "NV", 33: "NH", 34: "NJ", 35: "NM", 36: "NY", 37: "NC",
        38: "ND", 39: "OH", 40: "OK", 41: "OR", 42: "PA", 44: "RI", 45: "SC", 46: "SD", 47: "TN", 48: "TX", 49: "UT",
        50: "VT", 51: "VA", 53: "WA", 54: "WV", 55: "WI", 56: "WY"}


# ================================================================ 1. CPS basic monthly (Census API)
def cps_vars(y, m):
    """Census API variable list: household / person IDs changed in May 2004, race variable in 2003."""
    ids = "HRHHID,HRHHID2" if (y, m) >= (2004, 5) else "HRHHID,HRSAMPLE,HRSERSUF,HUHHNUM"
    race = "PTDTRACE" if y >= 2003 else "PERACE"
    return f"GESTFIPS,PESEX,PEMLR,HRMIS,PULINENO,PWCMPWGT,{race},{ids}"


def fetch_month(ym):
    y, m = ym
    f = CPSB / f"cps_{y}_{m:02d}.csv.gz"
    if f.exists():
        return ym, "cached"
    key = os.environ.get("CENSUS_API_KEY", "")
    url = (f"https://api.census.gov/data/{y}/cps/basic/{MONTHS[m - 1]}?get={cps_vars(y, m)}"
           f"&PRTAGE={AGE_LO}:{AGE_HI + 1}" + (f"&key={key}" if key else ""))
    err = ""
    for attempt in range(4):
        try:
            rows = json.loads(urllib.request.urlopen(url, timeout=600).read())
            break
        except urllib.error.HTTPError as e:            # never print the URL (it carries the key)
            err = f"HTTP {e.code}"
        except Exception as e:                         # noqa: BLE001
            err = type(e).__name__
        time.sleep(10 * (attempt + 1))
    else:
        return ym, f"FAILED ({err})"
    tmp = f.with_suffix(".tmp")
    with gzip.open(tmp, "wt", newline="") as fh:
        for r in rows:
            fh.write(",".join(r) + "\n")
    tmp.replace(f)
    return ym, f"{len(rows) - 1} rows"


def download_cps(workers=4):
    CPSB.mkdir(parents=True, exist_ok=True)
    todo = [(y, m) for y in YEARS for m in range(1, 13)]
    with ThreadPoolExecutor(workers) as ex:
        for ym, msg in ex.map(fetch_month, todo):
            print(ym, msg, flush=True)


def read_month(y, m):
    f = CPSB / f"cps_{y}_{m:02d}.csv.gz"
    if not f.exists():
        return None
    d = pd.read_csv(f, dtype=str, keep_default_na=False)
    d = d.loc[:, ~d.columns.duplicated()]
    race = "PTDTRACE" if "PTDTRACE" in d else "PERACE"
    idc = ["HRHHID", "HRHHID2"] if "HRHHID2" in d else ["HRHHID", "HRSAMPLE", "HRSERSUF", "HUHHNUM"]
    out = pd.DataFrame({
        "key": d[idc + ["PULINENO", "GESTFIPS"]].agg("|".join, axis=1),
        "state": pd.to_numeric(d["GESTFIPS"]), "sex": pd.to_numeric(d["PESEX"]),
        "age": pd.to_numeric(d["PRTAGE"]), "mis": pd.to_numeric(d["HRMIS"]),
        "lfs": pd.to_numeric(d["PEMLR"]), "w": pd.to_numeric(d["PWCMPWGT"], errors="coerce"),
        "black": (pd.to_numeric(d[race]) == 2).astype(int)})       # PERACE 2 / PTDTRACE 2 = Black (alone)
    out = out[out["lfs"].between(1, 7) & (out["w"] > 0)]
    out["emp"] = out["lfs"].isin([1, 2]).astype(int)
    out["unemp"] = out["lfs"].isin([3, 4]).astype(int)
    return out


def cps_aggregates():
    """Monthly state x sex x black aggregates: stocks (all rotations) and matched t -> t+1 flows."""
    cache = DATA / "atlas_cps_monthly.pkl"
    if cache.exists():
        return pd.read_pickle(cache)
    rows, prev, prev_ym = [], None, None
    for y in YEARS:
        for m in range(1, 13):
            cur = read_month(y, m)
            if cur is None:
                prev = None
                continue
            c = cur[cur["age"].between(AGE_LO, AGE_HI)]
            g = c.assign(wE=c.w * c.emp, wU=c.w * c.unemp, wN=c.w * (1 - c.emp - c.unemp)).groupby(
                ["state", "sex", "black"])[["w", "wE", "wU", "wN"]].sum()
            g["ym"] = y * 100 + m
            g["n_match"] = 0
            if prev is not None:
                p = prev[prev["age"].between(AGE_LO, AGE_HI) & prev["mis"].isin([1, 2, 3, 5, 6, 7])]
                mm = p.merge(cur[["key", "sex", "black", "age", "mis", "emp"]], on="key", suffixes=("", "_1"))
                mm = mm[(mm.mis_1 == mm.mis + 1) & (mm.sex_1 == mm.sex) & (mm.black_1 == mm.black)
                        & (mm.age_1 - mm.age).between(0, 1)]
                rate = len(mm) / max(len(p), 1)
                ne = mm[mm.emp == 0] if rate >= MIN_MATCH else mm.iloc[:0]      # ID breaks: no flows that month
                f = ne.assign(fNE=ne.w, fNE_E=ne.w * ne.emp_1, fU=ne.w * ne.unemp, fU_E=ne.w * ne.unemp * ne.emp_1,
                              fN=ne.w * (1 - ne.unemp), fN_E=ne.w * (1 - ne.unemp) * ne.emp_1, nNE=1,
                              nU=ne.unemp).groupby(["state", "sex", "black"])[
                    ["fNE", "fNE_E", "fU", "fU_E", "fN", "fN_E", "nNE", "nU"]].sum()
                g = g.join(f, how="left")
                g["n_match"] = len(mm) if rate >= MIN_MATCH else 0
                g["match_rate"] = rate
            rows.append(g.reset_index())
            prev = cur
    out = pd.concat(rows, ignore_index=True).fillna({c: 0 for c in ["fNE", "fNE_E", "fU", "fU_E", "fN", "fN_E",
                                                                    "nNE", "nU"]})
    out.to_pickle(cache)
    return out


def cps_period(agg, y0, y1, tag):
    """Women's and men's rates by state over [y0, y1] (all races; Black women separately)."""
    a = agg[(agg.ym // 100).between(y0, y1)]
    res = {}
    for sex, s in ((2, "w"), (1, "m")):
        g = a[a.sex == sex].groupby("state")[["wE", "wU", "wN", "fNE", "fNE_E", "fU", "fU_E", "fN", "fN_E",
                                               "nNE", "nU"]].sum()
        res[f"jf_{s}_{tag}"] = 100 * g.fNE_E / g.fNE
        res[f"ue_{s}_{tag}"] = 100 * g.fU_E / g.fU
        res[f"ne_{s}_{tag}"] = 100 * g.fN_E / g.fN
        res[f"look_{s}_{tag}"] = 100 * g.wU / (g.wU + g.wN)
        res[f"nNE_{s}_{tag}"] = g.nNE
        res[f"nU_{s}_{tag}"] = g.nU
    g = a[(a.sex == 2) & (a.black == 1)].groupby("state")[["fNE", "fNE_E", "nNE"]].sum()
    res[f"jf_wb_{tag}"] = (100 * g.fNE_E / g.fNE).where(g.nNE >= 200)
    res[f"nNE_wb_{tag}"] = g.nNE
    return pd.DataFrame(res)


# ================================================================ 2. March CPS 1977-92 (Mare-Winship)
def march_cps():
    cache = DATA / "atlas_mare_winship.pkl"
    if cache.exists():
        return pd.read_pickle(cache)
    cs = [(12, 14), (77, 79), (92, 95), (106, 107), (178, 179), (182, 183), (204, 206), (280, 292)]
    nm = ["year", "state", "age", "esr", "race", "sex", "ww", "w"]
    out = []
    for yy in range(77, 93):
        d = pd.read_fwf(MW / f"cpsmw{yy}", colspecs=cs, names=nm)
        d = d[d.age.between(AGE_LO, AGE_HI) & d.esr.between(1, 7) & (d.w > 0)]
        unemp = d.esr.isin([3, 4]) if yy >= 89 else (d.esr == 3)     # 1989+: 3 looking, 4 layoff
        d = d.assign(emp=d.esr.isin([1, 2]).astype(int), unemp=unemp.astype(int), nowork=(d.ww == 0).astype(int),
                     black=(d.race == 2).astype(int), fips=d.state.map(CENSUS2FIPS), year=1900 + yy)
        d["w"] = d.w / 100
        g = d.assign(wNW=d.w * d.nowork, wNW_E=d.w * d.nowork * d.emp, wU=d.w * d.unemp,
                     wN=d.w * (1 - d.emp - d.unemp), nNW=d.nowork).groupby(["year", "fips", "sex", "black"])[
            ["wNW", "wNW_E", "wU", "wN", "nNW"]].sum()
        out.append(g.reset_index())
    out = pd.concat(out, ignore_index=True)
    out.to_pickle(cache)
    return out


def march_period(mw):
    res = {}
    for sex, s in ((2, "w"), (1, "m")):
        g = mw[mw.sex == sex].groupby("fips")[["wNW", "wNW_E", "wU", "wN", "nNW"]].sum()
        res[f"jf_{s}_7792"] = 100 * g.wNW_E / g.wNW
        res[f"look_{s}_7792"] = 100 * g.wU / (g.wU + g.wN)
        res[f"nNE_{s}_7792"] = g.nNW
    return pd.DataFrame(res).rename_axis("state")


# ================================================================ 3. Opportunity Atlas by state
def atlas_states():
    races = ["black", "white"]
    cols = ["state", "county", "kid_pooled_pooled_n"]
    for r in races:
        cols += [f"kfr_{r}_pooled_p25", f"kfr_{r}_pooled_p75", f"kid_{r}_pooled_n", f"kid_{r}_pooled_blw_p50_n"]
    with zipfile.ZipFile(OI / "county_outcomes.zip") as z:
        with z.open("county_outcomes.csv") as fh:
            c = pd.read_csv(fh, usecols=cols)
    for r in races:
        for p in ("p25", "p75"):
            c[f"kfr_{r}_pooled_{p}"] *= 100
        c[f"w25_{r}"] = c[f"kid_{r}_pooled_blw_p50_n"]
        c[f"w75_{r}"] = (c[f"kid_{r}_pooled_n"] - c[f"kid_{r}_pooled_blw_p50_n"]).clip(lower=0)
    rows = {}
    for s, g in c.groupby("state"):
        d = {"n_counties": len(g), "kids_black": g.kid_black_pooled_n.sum(), "kids_all": g.kid_pooled_pooled_n.sum()}
        for r in races:
            for p in ("25", "75"):
                v, w = g[f"kfr_{r}_pooled_p{p}"], g[f"w{p}_{r}"]
                ok = v.notna() & (w > 0)
                d[f"{r}_p{p}"] = np.average(v[ok], weights=w[ok]) if ok.any() else np.nan
                d[f"ncty_{r}_p{p}"] = int(ok.sum())
        for p in ("25", "75"):
            gap = g[f"kfr_white_pooled_p{p}"] - g[f"kfr_black_pooled_p{p}"]
            w = g[f"w{p}_black"]
            ok = gap.notna() & (w > 0)
            d[f"gap_p{p}"] = np.average(gap[ok], weights=w[ok]) if ok.any() else np.nan
        rows[s] = d
    st = pd.DataFrame(rows).T.rename_axis("state")
    st.index = st.index.astype(int)
    st["share_black"] = 100 * st.kids_black / st.kids_all
    return st


def laus():
    u = pd.read_excel(UKCPR, sheet_name="Data", usecols=["state_fips", "year", "Unemployment rate"])
    u = u.rename(columns={"state_fips": "state", "Unemployment rate": "ur"}).dropna()
    u["state"] = u.state.astype(int)
    out = {}
    for tag, (a, b) in {"7792": (1980, 1992), "9400": (1994, 2000), "0521": (2005, 2021)}.items():
        out[f"ur_{tag}"] = u[u.year.between(a, b)].groupby("state").ur.mean()
    return pd.DataFrame(out)


# ================================================================ 4. regressions
def wls(df, y, xs, fe="region", weight="kids_black"):
    d = df[[y, *xs, weight] + ([fe] if fe else [])].dropna()
    X = d[xs].astype(float)
    if fe:
        X = X.join(pd.get_dummies(d[fe], prefix=fe, drop_first=True, dtype=float))
    X = sm.add_constant(X)
    w = d[weight] if weight else None
    r = (sm.WLS(d[y].astype(float), X, weights=w) if weight else sm.OLS(d[y].astype(float), X)).fit(cov_type="HC1")
    return r


def cell(r, x):
    if x not in r.params:
        return ""
    b, se, p = r.params[x], r.bse[x], r.pvalues[x]
    pv = "<0.001" if p < 0.001 else f"{p:.3f}"
    return f"{b:.2f}{stars(p)} ({se:.2f}) p={pv}"


OUTCOMES = [("gap_p25", "W-B gap, p25"), ("gap_p75", "W-B gap, p75"), ("black_p25", "Black, p25"),
            ("white_p25", "White, p25"), ("black_p75", "Black, p75"), ("white_p75", "White, p75")]


def table(df, tag, wvar, mvar, label, regs_out, weight="kids_black"):
    xs = [wvar, mvar, f"ur_{tag}", "share_black"]
    names = {wvar: f"Women: {label} (per SD)", mvar: f"Men: {label} (per SD)",
             f"ur_{tag}": "State unemployment rate (pp)", "share_black": "Share Black among children (pp)"}
    res = {o: wls(df, o, xs, weight=weight) for o, _ in OUTCOMES}
    res["gap_p25_biv"] = wls(df, "gap_p25", [wvar], fe=None, weight=weight)
    heads = [h for _, h in OUTCOMES] + ["W-B gap, p25 (women only, no controls)"]
    keys = [o for o, _ in OUTCOMES] + ["gap_p25_biv"]
    lines = ["| | " + " | ".join(f"({i + 1}) {h}" for i, h in enumerate(heads)) + " |",
             "|---" * (len(heads) + 1) + "|"]
    for x in xs:
        lines.append(f"| {names[x]} | " + " | ".join(cell(res[k], x) for k in keys) + " |")
    lines.append("| Region FE | " + " | ".join("yes" if k != "gap_p25_biv" else "no" for k in keys) + " |")
    means = []
    for k in keys:
        d = df.dropna(subset=[k.replace("_biv", "")])
        means.append(f"{np.average(d[k.replace('_biv', '')], weights=d[weight]):.1f}")
    lines.append("| Mean of outcome (weighted) | " + " | ".join(means) + " |")
    lines.append("| R2 | " + " | ".join(f"{res[k].rsquared:.2f}" for k in keys) + " |")
    lines.append("| N (states) | " + " | ".join(str(int(res[k].nobs)) for k in keys) + " |")
    for k in keys:
        for x in res[k].params.index:
            if x == "const" or x.startswith("region_"):
                continue
            regs_out.append(dict(table=f"{tag}_{wvar.split('_')[0]}" + ("" if weight else "_unweighted"),
                                 outcome=k, regressor=names.get(x, x), coef=res[k].params[x], se=res[k].bse[x],
                                 p=res[k].pvalues[x], n=int(res[k].nobs), r2=res[k].rsquared))
    return "\n".join(lines)


# ================================================================ 5. plot
def plot(df, x, xlabel, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ink, ink2, grid, surf = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    blue, orange = "#2a78d6", "#eb6834"
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.8), facecolor=surf)
    panels = [("gap_p25", "White-Black gap in child income rank, parents at p25", None),
              ("levels", "Child income rank, parents at p25", None)]
    s = 12 + 400 * df.kids_black / df.kids_black.max()
    for ax, (y, title, _) in zip(axs, panels):
        ax.set_facecolor(surf)
        if y == "gap_p25":
            ax.scatter(df[x], df[y], s=s, color=blue, alpha=0.55, edgecolor=surf, linewidth=1.5)
            b = np.polyfit(df[x], df[y], 1, w=np.sqrt(df.kids_black))
            xx = np.linspace(df[x].min(), df[x].max(), 10)
            ax.plot(xx, np.polyval(b, xx), color=blue, lw=2)
            big = df.nlargest(12, "kids_black")
            for st, r in big.iterrows():
                ax.annotate(ABBR.get(st, st), (r[x], r[y]), fontsize=7.5, color=ink2, xytext=(4, 3),
                            textcoords="offset points")
            ax.set_ylabel("rank points (White minus Black)", color=ink2)
        else:
            for col, c, lab in (("black_p25", blue, "Black children"), ("white_p25", orange, "White children")):
                ax.scatter(df[x], df[col], s=s, color=c, alpha=0.5, edgecolor=surf, linewidth=1.5, label=lab)
                b = np.polyfit(df[x], df[col], 1, w=np.sqrt(df.kids_black))
                xx = np.linspace(df[x].min(), df[x].max(), 10)
                ax.plot(xx, np.polyval(b, xx), color=c, lw=2)
            ax.legend(frameon=False, fontsize=8.5, labelcolor=ink2, loc="best")
            ax.set_ylabel("mean household income rank (0-100)", color=ink2)
        ax.set_title(title, fontsize=10, color=ink, loc="left")
        ax.set_xlabel(xlabel, color=ink2)
        ax.grid(color=grid, lw=0.8)
        ax.set_axisbelow(True)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        for sp in ("left", "bottom"):
            ax.spines[sp].set_color(grid)
        ax.tick_params(colors=ink2, labelsize=8)
    fig.text(0.01, 0.005, "States (incl. DC); bubble size = Black children (2000 Census); lines = WLS fits with "
             "Black-children weights. Children born 1978-83 (Opportunity Atlas). Descriptive, cross-sectional.",
             fontsize=7.5, color=ink2)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(path, dpi=160, facecolor=surf)
    plt.close(fig)


# ================================================================ main
def main():
    OUT.mkdir(exist_ok=True)
    st = atlas_states()
    agg = cps_aggregates()
    fr = march_period(march_cps()).join(cps_period(agg, 1994, 2000, "9400"), how="outer").join(
        cps_period(agg, 2005, 2021, "0521"), how="outer")
    df = st.join(fr, how="left").join(laus(), how="left")
    df["region"] = df.index.map(REGION)
    df["abbr"] = df.index.map(ABBR)
    df = df[df.index.isin(ABBR)]
    specs = [("7792", "jf", "annual re-employment, 1977-92 (March CPS)"),
             ("9400", "jf", "monthly job finding of non-employed, 1994-2000"),
             ("0521", "jf", "monthly job finding of non-employed, 2005-21"),
             ("9400", "ue", "monthly U->E, 1994-2000"),
             ("7792", "look", "looking share of non-employed, 1977-92"),
             ("9400", "look", "looking share of non-employed, 1994-2000")]
    for tag, v, _ in specs:
        for s in ("w", "m"):
            c = f"{v}_{s}_{tag}"
            df[f"z_{c}"] = (df[c] - df[c].mean()) / df[c].std()
    regs, md = [], []
    md.append("# Opportunity Atlas outcomes vs women's search frictions, by state\n")
    md.append("Script `IGE/17.AtlasFrictions.py` (2026-10-17). **Descriptive and cross-sectional** (51 states incl. DC): "
              "no causal claim. Outcomes: Opportunity Atlas county predictions (children born 1978-83, household "
              "income rank at 31-37 given parents at the national p25 / p75) averaged to states with OI's preferred "
              "weights; the White-Black gap is averaged within counties where Black children live. Regressions: WLS "
              "weighted by Black children (2000 Census), HC1 s.e.; friction measures standardised (per 1 SD across "
              "states). Cells: coefficient, stars (*** p<0.01, ** p<0.05, * p<0.1), (s.e.), p-value.\n")
    # descriptive table of frictions
    dcols = []
    for tag, v, lab in specs:
        for s, who in (("w", "women"), ("m", "men")):
            c = f"{v}_{s}_{tag}"
            dcols.append((c, f"{who}: {lab}"))
    md.append("## Friction measures across states (percent)\n")
    md.append("| measure | mean | SD | min | max | corr. with women's 1994-2000 job finding | persons-at-risk (sum over states) |")
    md.append("|---|---|---|---|---|---|---|")
    for c, lab in dcols:
        tag = c.split("_")[-1]
        sx = c.split("_")[1]
        ncol = f"nNE_{sx}_{tag}"
        nn = f"{int(df[ncol].sum()):,}" if ncol in df and not c.startswith("look") else ""
        md.append(f"| {lab} | {df[c].mean():.2f} | {df[c].std():.2f} | {df[c].min():.2f} | {df[c].max():.2f} | "
                  f"{df[c].corr(df['jf_w_9400']):.2f} | {nn} |")
    md.append("")
    md.append(f"Correlation of women's and men's measures across states: 1977-92 re-employment "
              f"{df.jf_w_7792.corr(df.jf_m_7792):.2f}; 1994-2000 job finding {df.jf_w_9400.corr(df.jf_m_9400):.2f}; "
              f"2005-21 job finding {df.jf_w_0521.corr(df.jf_m_0521):.2f}. Women's job finding 1994-2000 vs 2005-21: "
              f"{df.jf_w_9400.corr(df.jf_w_0521):.2f}; vs 1977-92 re-employment: {df.jf_w_9400.corr(df.jf_w_7792):.2f}.\n")
    titles = {("7792", "jf"): "Table 1. Childhood period: annual re-employment of women not working the previous year "
                              "(March CPS 1977-92)",
              ("9400", "jf"): "Table 2. Monthly job finding of non-employed women (CPS basic monthly 1994-2000)",
              ("0521", "jf"): "Table 3. Monthly job finding of non-employed women, 2005-2021 (after the children's "
                              "childhood)",
              ("9400", "ue"): "Table 4. Monthly U->E of unemployed women (CPS basic monthly 1994-2000)",
              ("7792", "look"): "Table 5. Share of non-employed women looking for work (March CPS 1977-92)",
              ("9400", "look"): "Table 6. Share of non-employed women looking for work (CPS basic monthly 1994-2000)"}
    for tag, v, lab in specs:
        md.append(f"## {titles[(tag, v)]}\n")
        md.append(table(df, tag, f"z_{v}_w_{tag}", f"z_{v}_m_{tag}", lab, regs))
        md.append("")
    md.append("## Table 7. Robustness: unweighted (each state counts once), monthly job finding 1994-2000\n")
    df["one"] = 1.0
    md.append(table(df, "9400", "z_jf_w_9400", "z_jf_m_9400", "monthly job finding of non-employed, 1994-2000",
                    regs, weight="one").replace("Mean of outcome (weighted)", "Mean of outcome"))
    md.append("")
    # Black women's own job finding, where the sample allows
    sub = df.dropna(subset=["jf_wb_9400"])
    md.append(f"## Black women's own monthly job finding (1994-2000), states with >= 200 matched non-employed Black "
              f"women: N = {len(sub)}\n")
    sub = sub.assign(z_jf_wb_9400=(sub.jf_wb_9400 - sub.jf_wb_9400.mean()) / sub.jf_wb_9400.std())
    lines = ["| | " + " | ".join(f"({i + 1}) {h}" for i, (_, h) in enumerate(OUTCOMES)) + " |",
             "|---" * (len(OUTCOMES) + 1) + "|"]
    rr = {o: wls(sub, o, ["z_jf_wb_9400", "ur_9400", "share_black"]) for o, _ in OUTCOMES}
    for x, nm_ in (("z_jf_wb_9400", "Black women: monthly job finding (per SD)"), ("ur_9400", "State unemployment rate (pp)"),
                   ("share_black", "Share Black among children (pp)")):
        lines.append(f"| {nm_} | " + " | ".join(cell(rr[o], x) for o, _ in OUTCOMES) + " |")
        for o, _ in OUTCOMES:
            regs.append(dict(table="9400_jf_blackwomen", outcome=o, regressor=nm_, coef=rr[o].params[x],
                             se=rr[o].bse[x], p=rr[o].pvalues[x], n=int(rr[o].nobs), r2=rr[o].rsquared))
    lines.append("| Region FE | " + " | ".join("yes" for _ in OUTCOMES) + " |")
    lines.append("| N (states) | " + " | ".join(str(int(rr[o].nobs)) for o, _ in OUTCOMES) + " |")
    md.append("\n".join(lines) + "\n")
    m = agg.dropna(subset=["match_rate"]).groupby("ym").match_rate.first()
    md.append("## Notes\n")
    md.append(f"- CPS basic monthly months used: {agg.ym.nunique()} (1994-2021); month pairs used for flows: "
              f"{(m >= MIN_MATCH).sum()}; median share of rotation-1-3/5-7 persons validly matched to the next month "
              f"{m.median():.2f}; pairs dropped (valid match share < {MIN_MATCH}; household-ID breaks), listed by "
              f"the later month: {', '.join(str(k) for k in m[m < MIN_MATCH].index) or 'none'}.")
    md.append("- 1977-92 measure is annual (not monthly): employed in the March survey week among those with zero weeks "
              "worked in the previous calendar year; it mixes the search friction with the choice to stay out "
              "(as do all the rates here). 1981 March file lacks Alaska, Hawaii and much of California (NBER errata).")
    md.append("- Opportunity Atlas has no state file; state values are weighted averages of county predictions "
              "(counties without an estimate for a race are dropped from that race's average).")
    md.append("- Unemployment rate: BLS LAUS (via UKCPR National Welfare Data), mean over 1980-92 / 1994-2000 / "
              "2005-21 matching the friction period.")
    (OUT / "atlas_frictions.md").write_text("\n".join(md), encoding="utf-8")
    # csv: state data then regression rows
    keep = ["abbr", "region", "kids_black", "share_black", "black_p25", "white_p25", "black_p75", "white_p75",
            "gap_p25", "gap_p75", "ur_7792", "ur_9400", "ur_0521"] + [c for c, _ in dcols] + ["jf_wb_9400",
                                                                                            "nNE_wb_9400"]
    sdf = df[keep].reset_index().assign(kind="state")
    rdf = pd.DataFrame(regs).assign(kind="regression")
    rdf["stars"] = rdf.p.map(stars)
    pd.concat([sdf, rdf], ignore_index=True).to_csv(OUT / "atlas_frictions.csv", index=False)
    plot(df, "jf_w_9400", "Women's monthly job-finding rate of the non-employed, 1994-2000 (%)",
         OUT / "atlas_frictions.png")
    print((OUT / "atlas_frictions.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    if "--download-only" in sys.argv:
        download_cps()
    else:
        if not CPSB.exists() or len(list(CPSB.glob("*.csv.gz"))) < 12 * len(YEARS):
            download_cps()
        main()
