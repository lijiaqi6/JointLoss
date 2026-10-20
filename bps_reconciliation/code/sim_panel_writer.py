r"""Simulated monthly couple panel -> PSID-shaped biennial household-year panel in the layout of BPS's psid_cons.dta
(IGE/bps_reconciliation, 2026-10-18). The output is the input of bps_on_sim.do (BPS (2016)'s own estimator).
Documentation: IGE/bps_reconciliation/HARNESS.md.

Main entry points
    to_bps_panel(monthly, ...)          -> DataFrame, one row per head x PSID wave, BPS variable names
    add_measurement_error(panel, ...)   -> (DataFrame, info): two-component mixture (Bound et al. shares + gross errors)
    write_bps_dta(panel, path)          -> checks the layout and writes the Stata file read by bps_on_sim.do
    write_sim_panel(monthly, path, ...) -> the three in sequence

INPUT SCHEMA (pandas DataFrame, one row per couple x calendar month; amounts in real dollars of `base_year`)
  required
    couple_id      int     couple (household) identifier
    year, month    int     calendar year (e.g. 1995-2009) and month 1-12
    age_h, age_w   float   ages of husband and wife in that month (years)
    race_h, race_w int     1 White, 2 Black, 3 other
    educ_h, educ_w int     1 = <12 years, 2 = 12 years, 3 = >12 years  (or years of schooling if educ_in_years=True)
    hours_h, hours_w float hours worked in the month (0 if not employed)
    earn_h, earn_w float   labor earnings in the month
    emp_h, emp_w   int     status in the month, PSID codes: 1 working, 2 temporarily laid off, 3 looking for work /
                           unemployed, 4 retired, 5 disabled, 6 keeping house / out of the labor force, 7 student
    cons           float   consumption in the month, BPS's definition (nondurables + services incl. rent equivalent)
    assets         float   net worth at the end of the month
    kids           int     persons under 18 in the family unit
    married        int     1 if the couple is married (living together) in the month
  optional (defaults in brackets)
    head_id        identity of the head [couple_id]; output rows are head x wave
    wife_id        identity of the wife [couple_id while married, missing otherwise]
    fsize          family size [1 + married + kids]
    disp_h, disp_w 1 in the month a displacement (closure or layoff) ends the spouse's job [0]
    closure_h/_w, quit_h/_w   closures only / quits, same timing [0];  jobend_w  any job end of the wife [disp_w|quit_w]
    wage_h, wage_w hourly wage (diagnostics only: BPS use annual earnings / annual hours)
    cons_housing   housing part of cons (totcons_nh = totcons - housing) [0]
    snap, eitc, ui_h, ui_w, other_inc   monthly transfers / other family income (carried as x_* extras; BPS's
                   pipeline recomputes taxes and Food Stamps from earnings and does not read them) [0]
    seo            1 = SEO-type (low-income oversample) couple [0]
    state          PSID state code 1-51 [default_state]
    mortgage       remaining mortgage principal (the exclusion restriction of BPS's participation probit) [0]
    smsa, outkid, weight   PSID codes / weight [1, 5, 1]

TIMING (PSID): wave W is interviewed in `interview_month` of calendar year W (spring); income year Y = W - 1;
BPS's `year` = Y - 1900 (98, 100, ..., 108 for waves 1999-2009). Annual hours and earnings are sums over calendar
year Y; status, family composition, marital status, assets, mortgage and age are taken in the interview month;
consumption is the interview month's flow annualised (x12), or the average of the `cons_months` months up to the
interview, or the calendar-year-Y sum (cons_timing='calendar'). All amounts are converted to nominal dollars with
BPS's own price index p_totcons of income year Y (price_indices.dta), so that BPS's deflation returns the model's
real values exactly. Displacement flags follow build_flags.py: hd / wd = event in calendar years Y-1 or Y (the
row's two-year difference), *_n the next interval (Y+1, Y+2), *_p the previous one (Y-3, Y-2); jd = hd & wd;
jd_sy = both in the same calendar year.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

CODE = Path(__file__).resolve().parent

# columns bps_on_sim.do requires (order of the output file), then flags and extras
BPS_COLS = ["year", "id", "person", "seo", "state", "fsize", "age", "sex", "agew", "kids", "marit",
            "mortgage1", "mortgage2", "outkid", "race1", "race2", "race3", "race4",
            "wrace1", "wrace2", "wrace3", "wrace4", "smsa", "hours", "hourw", "educ", "weduc", "educ_ind",
            "weduc_ind", "weight", "empst", "wempst", "ly", "wly", "fchg", "totcons", "totcons_nh",
            "tot_assets3", "tyoth"]
FLAG_BASE = ["hd", "hs", "hq", "wd", "ws", "wq", "wa", "jd", "jd_sy"]
FLAG_COLS = ["h_pid", "w_pid"] + FLAG_BASE + [f + "_n" for f in FLAG_BASE] + [f + "_p" for f in FLAG_BASE] \
    + ["h_match", "w_match"]
INT_COLS = {"year": "int16", "id": "int32", "person": "int32", "seo": "int8", "sex": "int8", "fsize": "int8",
            "kids": "int8", "hours": "int32"}
EDUC_YEARS = {1: 10, 2: 12, 3: 16}
BPS_WAVES = tuple(range(1999, 2010, 2))
# age groups of BPS's measurement-error calibration (variance_estimation.do, age_cat on age at income year)
AGE_CUTS = (38, 43, 48, 53)


def bps_price_index(base_year: int = 2000) -> dict:
    """BPS's p_totcons (price_indices.dta), calendar year -> index relative to base_year."""
    p = pd.read_stata(CODE / "price_indices.dta", convert_categoricals=False)
    p = dict(zip(p["year"].astype(int) + 1900, p["p_totcons"].astype(float)))
    return {y: v / p[base_year] for y, v in p.items()}


def _age_group(age):
    a = np.asarray(age, dtype=float)
    return 1 + sum((a >= c).astype(int) for c in AGE_CUTS)


def to_bps_panel(monthly: pd.DataFrame, waves=BPS_WAVES, interview_month=4, cons_timing: str = "interview",
                 cons_months: int = 1, price_index: dict | None = None, base_year: int = 2000,
                 educ_in_years: bool = False, default_state: int = 31, require_full_year: bool = True,
                 keep_unmarried: bool = True, seed: int = 0) -> pd.DataFrame:
    """Aggregate a monthly couple panel (schema in the module docstring) to BPS's household-year layout.

    waves             PSID waves (interview years) to write; BPS's estimator needs a subset of 1999-2009 (odd)
    interview_month   int, or a sequence of months drawn at random per head x wave (e.g. (3, 4, 5))
    cons_timing       'interview' (cons_months months up to and incl. the interview month, annualised) | 'calendar'
    require_full_year drop a head-wave if the head is not observed in all 12 months of income year Y
    keep_unmarried    write head-waves without a wife (marit 4, agew 0), which BPS's code drops itself
    """
    m = monthly.copy()
    rng = np.random.default_rng(seed)
    if "head_id" not in m:
        m["head_id"] = m["couple_id"]
    if "wife_id" not in m:
        m["wife_id"] = np.where(m["married"] == 1, m["couple_id"], np.nan)
    m.loc[m["married"] != 1, "wife_id"] = np.nan
    defaults = {"disp_h": 0, "disp_w": 0, "closure_h": 0, "closure_w": 0, "quit_h": 0, "quit_w": 0,
                "cons_housing": 0.0, "snap": 0.0, "eitc": 0.0, "ui_h": 0.0, "ui_w": 0.0, "other_inc": 0.0,
                "seo": 0, "state": default_state, "mortgage": 0.0, "smsa": 1, "outkid": 5, "weight": 1.0}
    for k, v in defaults.items():
        if k not in m:
            m[k] = v
    if "fsize" not in m:
        m["fsize"] = 1 + (m["married"] == 1).astype(int) + m["kids"]
    if "jobend_w" not in m:
        m["jobend_w"] = ((m["disp_w"] == 1) | (m["quit_w"] == 1)).astype(int)
    if m.duplicated(["head_id", "year", "month"]).any():
        raise ValueError("monthly panel must be unique by (head_id, year, month)")
    pidx = price_index if price_index is not None else bps_price_index(base_year)

    # ordinal identities (PSID-like positive integers)
    heads = pd.Index(np.sort(m["head_id"].unique()))
    m["_h"] = heads.get_indexer(m["head_id"]) + 1
    wives = pd.Index(np.sort(m["wife_id"].dropna().unique()))
    m["_w"] = np.where(m["wife_id"].notna(), wives.get_indexer(m["wife_id"].fillna(wives[0] if len(wives) else 0)) + 1, -1)

    # annual sums over the income year (calendar year Y)
    ann_cols = ["hours_h", "hours_w", "earn_h", "earn_w", "cons", "cons_housing", "snap", "eitc", "ui_h", "ui_w",
                "other_inc"]
    A = m.groupby(["_h", "year"])[ann_cols].sum()
    A["n_months"] = m.groupby(["_h", "year"]).size()
    A = A.reset_index()

    # interview-month records
    rows = []
    for W in waves:
        h = np.sort(m.loc[m["year"] == W, "_h"].unique())
        im = np.asarray(interview_month) if np.ndim(interview_month) else np.array([interview_month])
        mon = rng.choice(im, size=len(h)) if len(im) > 1 else np.full(len(h), im[0])
        rows.append(pd.DataFrame({"_h": h, "year": W, "month": mon, "wave": W}))
    K = pd.concat(rows, ignore_index=True)
    I = K.merge(m, on=["_h", "year", "month"], how="inner")          # head present in the interview month
    I["Y"] = I["wave"] - 1
    I = I.merge(A.rename(columns={"year": "Y"}), on=["_h", "Y"], how="left", suffixes=("", "_ann"))
    if require_full_year:
        I = I[I["n_months"] == 12].copy()
    else:
        I = I[I["n_months"].fillna(0) > 0].copy()

    # consumption measure
    if cons_timing == "calendar":
        I["c_real"] = I["cons_ann"]
        I["ch_real"] = I["cons_housing_ann"]
    elif cons_timing == "interview":
        m["_t"] = m["year"] * 12 + m["month"] - 1
        I["_t"] = I["year"] * 12 + I["month"] - 1
        cm = m[["_h", "_t", "cons", "cons_housing"]]
        acc_c = np.zeros(len(I))
        acc_h = np.zeros(len(I))
        cnt = np.zeros(len(I))
        for lag in range(cons_months):
            q = I[["_h", "_t"]].assign(_t=I["_t"] - lag).merge(cm, on=["_h", "_t"], how="left")
            ok = q["cons"].notna().to_numpy()
            acc_c += np.where(ok, q["cons"].to_numpy(), 0)
            acc_h += np.where(ok, q["cons_housing"].to_numpy(), 0)
            cnt += ok
        I["c_real"] = 12 * acc_c / np.maximum(cnt, 1)
        I["ch_real"] = 12 * acc_h / np.maximum(cnt, 1)
    else:
        raise ValueError("cons_timing must be 'interview' or 'calendar'")

    married = I["married"] == 1
    P = I["Y"].map(pidx).to_numpy()
    if np.isnan(P).any():
        raise ValueError("price index lacks some income years")
    if educ_in_years:
        eh, ew = I["educ_h"], I["educ_w"]
    else:
        eh, ew = I["educ_h"].map(EDUC_YEARS), I["educ_w"].map(EDUC_YEARS)
    out = pd.DataFrame({
        "year": (I["Y"] - 1900).astype(int),
        "person": I["_h"].astype(int),
        "seo": I.groupby("_h")["seo"].transform("max").astype(int),
        "state": I["state"].astype(float),
        "fsize": I["fsize"].astype(int),
        "age": np.floor(I["age_h"]).astype(float),
        "sex": 1,
        "agew": np.where(married, np.floor(I["age_w"]), 0.0),
        "kids": I["kids"].astype(int),
        "marit": np.where(married, 1.0, 4.0),
        "mortgage1": I["mortgage"] * P,
        "mortgage2": 0.0,
        "outkid": I["outkid"].astype(float),
        "race1": I["race_h"].astype(float), "race2": np.nan, "race3": np.nan, "race4": np.nan,
        "wrace1": np.where(married, I["race_w"], np.nan), "wrace2": np.nan, "wrace3": np.nan, "wrace4": np.nan,
        "smsa": I["smsa"].astype(int),
        "hours": np.rint(I["hours_h_ann"]).astype(int),
        "hourw": np.where(married, np.rint(I["hours_w_ann"]), np.nan),
        "educ": eh.astype(float),
        "weduc": np.where(married, ew, np.nan),
        "weight": I["weight"].astype(float),
        "empst": I["emp_h"].astype(float),
        "wempst": np.where(married, I["emp_w"], np.nan),
        "ly": I["earn_h_ann"] * P,
        "wly": np.where(married, I["earn_w_ann"] * P, 0.0),
        "totcons": I["c_real"] * P,
        "totcons_nh": (I["c_real"] - I["ch_real"]) * P,
        "tot_assets3": I["assets"] * P,
        "tyoth": 0.0,
        "w_pid": np.where(married, I["_w"], -1).astype(float),
        "x_snap": I["snap_ann"] * P, "x_eitc": I["eitc_ann"] * P,
        "x_ui_h": I["ui_h_ann"] * P, "x_ui_w": I["ui_w_ann"] * P,
        "x_faminc": (I["earn_h_ann"] + np.where(married, I["earn_w_ann"], 0) + I["snap_ann"] + I["eitc_ann"]
                     + I["ui_h_ann"] + I["ui_w_ann"] + I["other_inc_ann"]) * P,
        "x_wage_h": I["earn_h_ann"] / I["hours_h_ann"].where(I["hours_h_ann"] > 0),
        "x_interview_month": I["month"].astype(int),
    })
    out["educ_ind"] = out["educ"]
    out["weduc_ind"] = out["weduc"]
    out["h_pid"] = out["person"].astype(float)
    out = out.sort_values(["year", "person"]).reset_index(drop=True)
    out["id"] = out.groupby("year").cumcount() + 1                  # interview number within the wave

    # family composition change since the previous wave of the same head (PSID fchg; BPS break at fchg > 1)
    out = out.sort_values(["person", "year"]).reset_index(drop=True)
    prev = out.groupby("person")[["year", "w_pid", "fsize", "kids"]].shift(1)
    has_prev = prev["year"].notna()
    wife_chg = has_prev & (out["w_pid"] != prev["w_pid"])
    oth_chg = has_prev & ((out["fsize"] != prev["fsize"]) | (out["kids"] != prev["kids"]))
    out["fchg"] = np.where(wife_chg, 2.0, np.where(oth_chg, 1.0, 0.0))

    # displacement flags (build_flags.py definitions)
    def events(col, who):
        e = m.loc[m[col] == 1, [who, "year"]]
        e = e[e[who] > 0]
        return set(zip(e[who].astype(int), e["year"].astype(int)))
    S = {"hd": events("disp_h", "_h"), "hs": events("closure_h", "_h"), "hq": events("quit_h", "_h"),
         "wd": events("disp_w", "_w"), "ws": events("closure_w", "_w"), "wq": events("quit_w", "_w"),
         "wa": events("jobend_w", "_w")}
    Yc = out["year"].to_numpy() + 1900
    hp = out["h_pid"].astype(int).to_numpy()
    wp = out["w_pid"].astype(int).to_numpy()

    def anyin(s, p, lo, hi):
        return np.array([float(q > 0 and any((q, y) in s for y in range(a, z + 1))) for q, a, z in zip(p, lo, hi)])

    for suf, sh in (("", 0), ("_n", 2), ("_p", -2)):
        lo, hi = Yc - 1 + sh, Yc + sh
        for f in ("hd", "hs", "hq"):
            out[f + suf] = anyin(S[f], hp, lo, hi)
        for f in ("wd", "ws", "wq", "wa"):
            out[f + suf] = anyin(S[f], wp, lo, hi)
        out["jd" + suf] = out["hd" + suf] * out["wd" + suf]
        out["jd_sy" + suf] = np.array([float(a > 0 and b > 0 and any((a, y) in S["hd"] and (b, y) in S["wd"]
                                                                     for y in range(l, z + 1)))
                                       for a, b, l, z in zip(hp, wp, lo, hi)])
    out["h_match"] = 1
    out["w_match"] = (out["w_pid"] > 0).astype(int)
    extras = [c for c in out.columns if c.startswith("x_")]
    return out[BPS_COLS + FLAG_COLS + extras].sort_values(["year", "id"]).reset_index(drop=True)


def add_measurement_error(panel: pd.DataFrame, shares=None, var_c: float = 0.0332, gross_rate: float = 0.0,
                          gross_sd: float = 1.0, gross_vars=("ly", "wly", "hours", "hourw", "totcons"),
                          basis: str = "measured", calib=None, seed: int = 1):
    """Two-component measurement error in logs, applied to positive annual earnings, hours and consumption.

    Component 1 (classical, every observation): log errors e_y, e_h for each spouse, bivariate normal by age group
      (BPS's age_cat on age at the income year; wives: wife's age, working wives), with variances such that the
      error is shares['y'], shares['h'] and shares['w'] of the log variance of earnings, hours and the hourly wage
      (= earnings / hours, error e_y - e_h) -- BPS's calibration from Bound et al. (1994), T4C1.do: 0.04 / 0.23 /
      0.13. basis='measured' makes the share a share of the *measured* variance (what BPS's correction assumes:
      s_me = share * var(measured log x)), i.e. error variance = share/(1-share) * true variance; basis='true' uses
      share * true variance. cov(e_y, e_h) = (E_y + E_h - E_w)/2, clipped to keep the matrix positive semi-definite.
      The true variances are computed on the calibration rows `calib` (boolean Series; default: married couples with
      the husband aged 30-57 at the income year, BPS's age window), by age group; the errors are drawn for all rows.
      Consumption: iid log error with variance var_c (BPS's s_omega = -E(dc_t dc_{t-2}) = 0.0332).
    Component 2 (gross errors): each listed variable independently, with probability gross_rate, gets an extra
      N(0, gross_sd^2) log error (the rare large errors that BPS's trims are meant to remove).
    Returns (panel with errors, info DataFrame of the error variances by spouse x age group).
    """
    sh = {"y": 0.04, "h": 0.23, "w": 0.13}
    if shares:
        sh.update(shares)
    rng = np.random.default_rng(seed)
    p = panel.copy()
    info = []
    k = (lambda s: s / (1 - s)) if basis == "measured" else (lambda s: s)
    if calib is None:
        calib = (p["marit"] == 1) & (p["age"] - 1 >= 30) & (p["age"] - 1 <= 57)
    calib = pd.Series(calib, index=p.index).astype(bool)
    for y, h, agev in (("ly", "hours", "age"), ("wly", "hourw", "agew")):
        ok = (p[y] > 0) & (p[h] > 0)
        g = pd.Series(_age_group(p[agev] - 1), index=p.index)
        ey = np.zeros(len(p))
        eh = np.zeros(len(p))
        for a in range(1, 6):
            sel = (ok & (g == a)).to_numpy()
            cal = (ok & (g == a) & calib).to_numpy()
            if cal.sum() < 10:
                cal = sel
            if sel.sum() < 10:
                continue
            ly = np.log(p.loc[cal, y].to_numpy())
            lh = np.log(p.loc[cal, h].to_numpy())
            Ey, Eh, Ew = k(sh["y"]) * ly.var(), k(sh["h"]) * lh.var(), k(sh["w"]) * (ly - lh).var()
            C = 0.5 * (Ey + Eh - Ew)
            lim = np.sqrt(Ey * Eh)
            clipped = abs(C) > lim
            C = float(np.clip(C, -lim, lim))
            z = rng.multivariate_normal([0, 0], [[Ey, C], [C, Eh]], size=sel.sum())
            ey[sel], eh[sel] = z[:, 0], z[:, 1]
            info.append({"spouse": "h" if y == "ly" else "w", "age_group": a, "n": int(sel.sum()),
                         "var_e_y": Ey, "var_e_h": Eh, "cov_e_yh": C, "var_e_w": Ey + Eh - 2 * C,
                         "target_var_e_w": Ew, "clipped": bool(clipped)})
        sel = ok.to_numpy()
        p.loc[sel, y] = p.loc[sel, y] * np.exp(ey[sel])
        hrs = p.loc[sel, h].to_numpy() * np.exp(eh[sel])
        p.loc[sel, h] = np.maximum(np.rint(hrs), 1)
    okc = p["totcons"] > 0
    ec = rng.normal(0, np.sqrt(var_c), okc.sum())
    p.loc[okc, "totcons_nh"] = p.loc[okc, "totcons_nh"] * np.exp(ec)
    p.loc[okc, "totcons"] = p.loc[okc, "totcons"] * np.exp(ec)
    info.append({"spouse": "c", "age_group": 0, "n": int(okc.sum()), "var_e_c": var_c})
    if gross_rate > 0:
        for v in gross_vars:
            okv = (p[v] > 0).to_numpy()
            hit = okv & (rng.random(len(p)) < gross_rate)
            e = rng.normal(0, gross_sd, hit.sum())
            vals = p.loc[hit, v].to_numpy() * np.exp(e)
            p.loc[hit, v] = np.maximum(np.rint(vals), 1) if v in ("hours", "hourw") else vals
            if v == "totcons":
                p.loc[hit, "totcons_nh"] = p.loc[hit, "totcons_nh"].to_numpy() * np.exp(e)
            info.append({"spouse": "gross", "age_group": 0, "n": int(hit.sum()), "var": v,
                         "gross_rate": gross_rate, "gross_sd": gross_sd})
    p["hours"] = p["hours"].astype(int)
    return p, pd.DataFrame(info)


def check_layout(panel: pd.DataFrame) -> None:
    """The checks bps_on_sim.do makes, in Python (fails early)."""
    miss = [c for c in BPS_COLS if c not in panel]
    if miss:
        raise ValueError(f"missing BPS columns: {miss}")
    if not panel["year"].isin([98, 100, 102, 104, 106, 108]).all():
        raise ValueError("year must be income year - 1900 in {98,...,108}")
    if panel.duplicated(["year", "id"]).any() or panel.duplicated(["person", "year"]).any():
        raise ValueError("panel must be unique by (year, id) and by (person, year)")
    if panel["hours"].isna().any():
        raise ValueError("hours must not be missing")
    bad = [c for c in panel.columns if c.startswith(("fd", "edd", "wedd", "chd", "dfd", "dchd", "yrd", "ybd",
                                                     "w_ybd", "stated", "_I", "log_", "d_", "p_", "tot_assets"))
           and c != "tot_assets3"]
    if bad:
        raise ValueError(f"column names that BPS's wildcards would pick up: {bad}")


def write_bps_dta(panel: pd.DataFrame, path) -> Path:
    """Check the layout and write the Stata file for bps_on_sim.do (version 118)."""
    check_layout(panel)
    p = panel.copy()
    for c, t in INT_COLS.items():
        if c in p:
            p[c] = p[c].astype(t)
    for c in p.columns:
        if c not in INT_COLS and p[c].dtype != object:
            p[c] = p[c].astype("float64")
    path = Path(path)
    p.to_stata(path, write_index=False, version=118)
    return path


def write_sim_panel(monthly: pd.DataFrame, path, me: dict | None = None, **kw):
    """to_bps_panel -> add_measurement_error (if me is a dict of its arguments) -> write_bps_dta."""
    panel = to_bps_panel(monthly, **kw)
    info = None
    if me is not None:
        panel, info = add_measurement_error(panel, **me)
    write_bps_dta(panel, path)
    return panel, info
