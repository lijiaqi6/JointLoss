r"""Weeks of unemployment benefit available during the son's teens and the layoff's cost (Fable optional addition C2).

99.SimulatedReplacementRate.py varied the weekly benefit; this script varies how LONG benefits last. Weeks available in
state s and year t (2026-10-20 approximation; the programmes' tiers are coded from their schedules, not from the
week-by-week DOL trigger notices):
  regular   the state's maximum weeks of regular benefits (12b's data/ui_generosity.csv, July issues)
  EB        13 weeks x the share of the year's weeks in which the state's Extended Benefits period was on (DOL ETA 539
            weekly claims and EB trigger report, oui.doleta.gov/unemploy/csv/ar539.csv, column c22 = 'B'; 1984+)
  federal   emergency programmes, by year, with tiers set by the state's annual unemployment rates (insured rate IUR =
            mean of ar539 c19; total rate TUR = LAUS, data/state_shocks.pkl):
            FSC 1984: 14 / 12 / 10 / 8 weeks for IUR >= 6 / 5 / 4 / below; 1985: a quarter of that (ended March)
            EUC 1991: 1/12 x 20; 1992: 28 if TUR >= 8 or IUR >= 4, else 22; 1993: 20 / 15; 1994: a third of 13 / 7
            TEUC 2002: 0.8 x 13; 2003: 13; 2004: a quarter of 13; + the same again (TEUC-X) where IUR >= 4
            EUC08 2008: 8; 2009: half of the 2010 schedule; 2010-11: 20 + 14 + 13 (TUR >= 6) + 6 (TUR >= 8.5);
                  2012: the mean of that and the 2013 schedule; 2013: 14 + 14 + 9 (TUR >= 7) + 10 (TUR >= 9)
  weeks_t = regular + EB + federal; exposure = mean over the son's income years at 12-18 in the family's state of
  that wave (18's husband_shocks_fam), >= 3 years, all of them 1984 or later.
DESIGN: as 99 (75's son-years, valid wage, PSID weights, father present): within son, ln earnings on son FE, single-age
  dummies, every component, lyp, structure, cohort and state-at-17 x (age-40)/10; weeks x age; layoff share x weeks x
  age (insurance offsetting the cost: positive); closure x weeks x age; placebo father's ln wage x weeks x age. Weeks
  are a function of state unemployment, so a check adds layoff share x the state's mean unemployment rate at 12-18 x
  age. weeks standardised over sons. DESCRIPTIVE.
Writes output/ui_duration_weeks.md / .json (aggregates only).
"""
import importlib.util
import json
import sys
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


R91 = _load("s91", "91.LayoffSelection.py")
R75, R72 = R91.R75, R91.R75.R72
c = R91.c
COMPS, STRUCT = R91.COMPS, R91.STRUCT
FIPS_ST = None
RES = {}


def federal(y, iur, tur):
    hi92 = (tur >= 8) or (iur >= 4)
    if y == 1984:
        return 14 if iur >= 6 else 12 if iur >= 5 else 10 if iur >= 4 else 8
    if y == 1985:
        return 0.25 * (14 if iur >= 6 else 12 if iur >= 5 else 10 if iur >= 4 else 8)
    if y == 1991:
        return 20 / 12
    if y == 1992:
        return 28 if hi92 else 22
    if y == 1993:
        return 20 if hi92 else 15
    if y == 1994:
        return (13 if hi92 else 7) / 3
    teuc = {2002: 0.8 * 13, 2003: 13, 2004: 13 / 4}
    if y in teuc:
        return teuc[y] * (2 if iur >= 4 else 1)
    s10 = 20 + 14 + 13 * (tur >= 6) + 6 * (tur >= 8.5)
    s13 = 14 + 14 + 9 * (tur >= 7) + 10 * (tur >= 9)
    return {2008: 8, 2009: 0.5 * s10, 2010: s10, 2011: s10, 2012: 0.5 * (s10 + s13), 2013: s13}.get(y, 0.0)


def weeks_panel():
    d = pd.read_csv(DATA / "ext" / "dol_ui" / "ar539.csv", usecols=["st", "rptdate", "c19", "c22"])
    d["year"] = d["rptdate"].str[:4].astype(int)
    d["eb"] = (d["c22"].astype(str).str.strip() == "B").astype(float)
    a = d.groupby(["st", "year"]).agg(iur=("c19", "mean"), eb=("eb", "mean")).reset_index()
    ui = pd.read_csv(DATA / "ui_generosity.csv")[["state", "state_fips", "year", "max_duration_weeks"]]
    a = a.merge(ui, left_on=["st", "year"], right_on=["state", "year"])
    sh = pd.read_pickle(DATA / "state_shocks.pkl")[["fips", "year", "ur"]].rename(columns={"fips": "state_fips"})
    a = a.merge(sh, on=["state_fips", "year"], how="left")
    a["fed"] = [federal(int(y), float(i), float(t) if pd.notna(t) else 0.0) for y, i, t in zip(a["year"], a["iur"], a["ur"])]
    a["weeks"] = a["max_duration_weeks"] + 13 * a["eb"] + a["fed"]
    return a[["state_fips", "year", "weeks", "eb", "fed", "ur", "iur", "max_duration_weeks"]]


def son_weeks(r):
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    st = pd.read_pickle(DATA / "husband_shocks_fam.pkl")[["wave", "int", "fips"]].drop_duplicates(["wave", "int"])
    W = weeks_panel().rename(columns={"state_fips": "fips"})
    k = py[py["child"] & py["age"].between(13, 19) & py["pid"].isin(r["pid"].unique())][["pid", "wave", "int"]]
    k["year"] = k["wave"] - 1
    k = k.merge(st, on=["wave", "int"]).dropna(subset=["fips"]).merge(W, on=["fips", "year"], how="left")
    g = k.groupby("pid")
    out = pd.DataFrame({"weeks": g["weeks"].mean(), "w_n": g["weeks"].count(), "y0": g["year"].min(),
                        "ur_win": g["ur"].mean(), "fed_win": g["fed"].mean(), "eb_win": g["eb"].mean()})
    return out[(out["w_n"] >= 3) & (out["y0"] >= 1984)].reset_index(), W


def main():
    r = R75.build()
    sw, W = son_weeks(r)
    r = r.merge(sw, on="pid", how="inner")
    r = R72.state17(r)
    r = r[r["lw"].notna() & (r["nofa"] == 0)].copy()
    one = r.drop_duplicates("pid")
    m = np.average(one["weeks"], weights=one["wt"])
    s = np.sqrt(np.average((one["weeks"] - m) ** 2, weights=one["wt"]))
    r["wk_z"] = (r["weeks"] - m) / s
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    cohd = pd.get_dummies(r["coh5"], prefix="coh", drop_first=True).astype(float)
    std = pd.get_dummies(r["fips17"].fillna(-1).astype(int), prefix="st", drop_first=True).astype(float)
    r = pd.concat([r, cohd, std], axis=1)
    r["agec"] = (r["age"] - 40) / 10
    XB = R91.xage(r, ["lyp"] + COMPS + STRUCT + list(cohd.columns) + list(std.columns))
    r["wk_xa"] = r["wk_z"] * r["agec"]
    r["lay_wk_xa"] = r["f_sh_layoff"] * r["wk_z"] * r["agec"]
    r["clo_wk_xa"] = r["f_sh_close"] * r["wk_z"] * r["agec"]
    r["flw_wk_xa"] = r["f_lw"] * r["wk_z"] * r["agec"]
    urm = np.average(one["ur_win"], weights=one["wt"])
    r["lay_ur_xa"] = r["f_sh_layoff"] * (r["ur_win"] - urm) * r["agec"]
    md = ["# Weeks of unemployment benefit available in the son's teens and the layoff's cost (Fable C2)", "",
          "Built by `102.UIDurationWeeks.py` (2026-10-20); design in its docstring. PSID sons with a father present, "
          "teen-window years 1984 and later; within-son design of 91 / 99; s.e. clustered by 1968 family; *** p<0.01, "
          "** p<0.05, * p<0.1. **Descriptive; programme tiers approximated.**", "",
          f"Sons {one['pid'].nunique():,} (born {int(one['birth_year'].min())}-{int(one['birth_year'].max())}); treated "
          f"(teen layoff year) {int((one['f_sh_layoff'] > 0).sum()):,}; weeks available, mean over 12-18: "
          f"{m:.1f} (s.d. {s:.1f}; regular {np.average(W['max_duration_weeks']):.1f}, federal share of window years "
          f"with a programme {np.average(one['fed_win'] > 0, weights=one['wt']):.2f}, EB on {np.average(one['eb_win'], weights=one['wt']):.2f}).",
          "", "| spec | layoff x age | layoff x weeks x age | closure x weeks x age | father's ln wage x weeks x age "
          "(placebo) | weeks x age | layoff x state UR x age | N son-years / sons |", "|---" * 8 + "|"]
    for lab, extra in (("weeks (1 s.d.)", []), ("+ layoff x state unemployment rate x age", ["lay_ur_xa"])):
        xs = XB + ["wk_xa", "lay_wk_xa", "clo_wk_xa", "flw_wk_xa"] + extra
        f = R91.fe_fit(r, "ly", xs)
        g = lambda x: (f["b"][x], float(np.sqrt(f["V"].loc[x, x])))  # noqa: E731
        md.append(f"| {lab} | {c(g('f_sh_layoff_xa'))} | {c(g('lay_wk_xa'))} | {c(g('clo_wk_xa'))} | "
                  f"{c(g('flw_wk_xa'))} | {c(g('wk_xa'))} | {c(g('lay_ur_xa')) if extra else ''} | "
                  f"{f['n']:,} / {f['sons']:,} |")
        RES[lab] = {k: list(g(k)) for k in ["f_sh_layoff_xa", "lay_wk_xa", "clo_wk_xa", "flw_wk_xa", "wk_xa"] + extra}
    md.append("")
    (OUT / "ui_duration_weeks.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "ui_duration_weeks.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
