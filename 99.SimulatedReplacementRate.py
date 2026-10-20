r"""Does unemployment insurance offset the delayed cost of a teen layoff? A replacement rate simulated at the father's
own wage (Fable addition C1, 2026-10-20).

82.UIStabilityChannel.py measured generosity as the state's maximum weekly benefit over its average weekly wage at the
son's 12-18; most of its variation is across states and it is not what a given father would have received. Here, in
the spirit of Gruber (1997) and East and Kuka (2015), each father gets the benefit his state's law would have paid him:
  weekly earnings  w = exp(f_lw + f_lh) / 52, the father's mean ln wage and ln annual hours over his valid teen-window
                   years (75's components; 2000 dollars)
  benefit          WBA_t = min(max_WBA_st, max(min_WBA_st, 0.5 w)) in each income year t of the son's 12-18, s = the
                   family's state in that wave (family files, 18's husband_shocks_fam fips; laws 1976+, 12b's
                   data/ui_generosity.csv, 2000 dollars). Half of the weekly wage is the typical statutory replacement
                   (high-quarter formulas of 1/23-1/26); dependants' allowances and the exact formulas are not coded.
  rr               mean over the window years of WBA_t / w (>= 3 years); rr_dur = rr x min(max weeks, 26) / 26.
Variation: the state x year laws and the father's wage relative to the cap (his wage is controlled through f_lw).
DESIGN: 75's son-years (sons 25-55, valid wage, PSID weights), father present, rr measured (teens from 1976: sons born
  about 1963 and later). Within son (91's fe_fit): ln earnings on son FE, single-age dummies, every component, lyp,
  structure flag and 5-year cohort x (age-40)/10, state-at-17 x age, rr x age, and the interactions
  layoff share x rr x age (insurance offsetting the cost: positive), closure share x rr x age and the father's ln wage
  x rr x age (placebo). rr standardised over sons (weighted). Also the band split: the layoff coefficient at 25-29 and
  45-49 in sons above vs below the median rr (91's band_fit with 200 draws).
Writes output/simulated_replacement_rate.md / .json (aggregates only). DESCRIPTIVE.
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
R75, R24, R72 = R91.R75, R91.R24, R91.R75.R72
c, Boot, dummies = R91.c, R91.Boot, R91.dummies
COMPS, STRUCT = R91.COMPS, R91.STRUCT
RES = {}


def sim_rr(r):
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    st = pd.read_pickle(DATA / "husband_shocks_fam.pkl")[["wave", "int", "fips"]].drop_duplicates(["wave", "int"])
    ui = pd.read_csv(DATA / "ui_generosity.csv")[["state_fips", "year", "max_wba_2000", "min_wba_2000",
                                                    "max_duration_weeks"]]
    one = r.drop_duplicates("pid")[["pid", "f_lw", "f_lh", "nofa", "f_na"]]
    one = one[(one["nofa"] == 0) & (one["f_na"] == 0)].copy()
    one["w"] = np.exp(one["f_lw"] + one["f_lh"]) / 52
    k = py[py["child"] & py["age"].between(12, 18) & py["pid"].isin(one["pid"])][["pid", "wave", "int"]]
    k = k.merge(st, on=["wave", "int"]).dropna(subset=["fips"])
    k["year"] = k["wave"] - 1
    k = k.merge(ui.rename(columns={"state_fips": "fips"}), on=["fips", "year"]).merge(one[["pid", "w"]], on="pid")
    k["wba"] = np.minimum(k["max_wba_2000"], np.maximum(k["min_wba_2000"], 0.5 * k["w"]))
    k["rr"] = k["wba"] / k["w"]
    k["rr_dur"] = k["rr"] * np.minimum(k["max_duration_weeks"], 26) / 26
    k["capped"] = (0.5 * k["w"] > k["max_wba_2000"]).astype(float)
    g = k.groupby("pid")
    out = pd.DataFrame({"rr": g["rr"].mean(), "rr_dur": g["rr_dur"].mean(), "capped": g["capped"].mean(),
                        "rr_n": g.size()})
    return out[out["rr_n"] >= 3].reset_index()


def main():
    r = R75.build()
    r = r.merge(sim_rr(r), on="pid", how="left")
    r = R72.state17(r)
    r = r[r["rr"].notna() & r["lw"].notna()].copy()
    one = r.drop_duplicates("pid")
    for v in ("rr", "rr_dur"):
        m = np.average(one[v], weights=one["wt"])
        s = np.sqrt(np.average((one[v] - m) ** 2, weights=one["wt"]))
        r[f"{v}_z"] = (r[v] - m) / s
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    cohd = pd.get_dummies(r["coh5"], prefix="coh", drop_first=True).astype(float)
    std = pd.get_dummies(r["fips17"].fillna(-1).astype(int), prefix="st", drop_first=True).astype(float)
    r = pd.concat([r, cohd, std], axis=1)
    r["agec"] = (r["age"] - 40) / 10
    base = ["lyp"] + COMPS + STRUCT + list(cohd.columns) + list(std.columns)
    XB = R91.xage(r, base)
    md = ["# Does unemployment insurance offset the delayed cost of a teen layoff? Simulated replacement rate (Fable C1)",
          "", "Built by `99.SimulatedReplacementRate.py` (2026-10-20); design in its docstring. PSID sons 25-55 whose "
          "father's teen-window years fall in 1976+ (state UI laws), valid wage, PSID weights; within-son design, s.e. "
          "clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**", "",
          f"Sons {one['pid'].nunique():,}; son-years {len(r):,}; simulated replacement rate mean "
          f"{np.average(one['rr'], weights=one['wt']):.3f} (s.d. {one['rr'].std():.3f}; share of window years with the "
          f"cap binding {np.average(one['capped'], weights=one['wt']):.2f}); with duration "
          f"{np.average(one['rr_dur'], weights=one['wt']):.3f}. Treated sons (teen layoff year): "
          f"{int((one['f_sh_layoff'] > 0).sum()):,}.", ""]
    md += ["## Within son: the layoff cost x the replacement rate", "",
           "| measure | layoff x age | layoff x rr x age | closure x rr x age | father's ln wage x rr x age (placebo) | "
           "rr x age | N son-years / sons |", "|---" * 7 + "|"]
    v = "rr_z"
    r[f"{v}_xa"] = r[v] * r["agec"]
    r[f"lay_{v}_xa"] = r["f_sh_layoff"] * r[v] * r["agec"]
    r[f"clo_{v}_xa"] = r["f_sh_close"] * r[v] * r["agec"]
    r[f"flw_{v}_xa"] = r["f_lw"] * r[v] * r["agec"]
    r["lay_flw_xa"] = r["f_sh_layoff"] * (r["f_lw"] - np.average(one["f_lw"], weights=one["wt"])) * r["agec"]
    for lab, extra in (("rr (1 s.d.)", []), ("rr (1 s.d.), + layoff x father's ln wage x age", ["lay_flw_xa"])):
        xs = XB + [f"{v}_xa", f"lay_{v}_xa", f"clo_{v}_xa", f"flw_{v}_xa"] + extra
        f = R91.fe_fit(r, "ly", xs)
        g = lambda x: (f["b"][x], float(np.sqrt(f["V"].loc[x, x])))  # noqa: E731
        md.append(f"| {lab} | {c(g('f_sh_layoff_xa'))} | {c(g(f'lay_{v}_xa'))} | "
                  f"{c(g(f'clo_{v}_xa'))} | {c(g(f'flw_{v}_xa'))} | {c(g(f'{v}_xa'))} | {f['n']:,} / {f['sons']:,} |")
        RES[f"fe|{lab}"] = {k: list(g(k)) for k in ["f_sh_layoff_xa", f"lay_{v}_xa", f"clo_{v}_xa", f"flw_{v}_xa",
                                                   f"{v}_xa"] + extra}
    md.append("")
    # band split by median rr
    BT = Boot(r["fam68"].to_numpy(), r["race"].to_numpy())
    med = float(np.median(one["rr"]))
    md += [f"## Layoff coefficient by band, sons above vs below the median simulated rr ({med:.3f})", "",
           "| sample | 25-29 | 45-49 | change |", "|---|---|---|---|"]
    for lab, q in (("rr above the median", r[r["rr"] >= med]), ("rr below the median", r[r["rr"] < med])):
        a = R91.band_fit(q, "ly", 0, BT, COMPS, ["f_sh_layoff"]).get("f_sh_layoff")
        b = R91.band_fit(q, "ly", 4, BT, COMPS, ["f_sh_layoff"]).get("f_sh_layoff")
        ch = (b[0] - a[0], b[1] - a[1]) if a and b else None
        md.append(f"| {lab} | {R91.fmt(a)} | {R91.fmt(b)} | {R91.fmt(ch)} |")
        RES[f"band|{lab}"] = {"a": [float(a[0]), R91.sd(a[1])] if a else None,
                              "b": [float(b[0]), R91.sd(b[1])] if b else None,
                              "ch": [float(ch[0]), R91.sd(ch[1])] if ch else None}
    md.append("")
    (OUT / "simulated_replacement_rate.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "simulated_replacement_rate.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
