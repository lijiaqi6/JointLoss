r"""One pooled insurance index, honestly sized (committee re-read memo, action 5, 2026-10-24)

The paper's UI tests are three underpowered designs (state schedule, simulated replacement rate at the father's wage,
weeks available) plus realised benefits. Here one index, two versions:
  INDEX A (full window, 1976+): 99's rr_dur = simulated weekly replacement at the father's wage x min(regular maximum
          duration, 26) / 26, mean over the son's 12-18 - the level and the duration of benefits in one number;
  INDEX B (1984+): the mean of the standardised simulated replacement rate (99's rr) and the standardised weeks
          available including Extended Benefits and the federal programmes (102's weeks).
DESIGN (75's son-years with a valid wage, father present with a measured wage; within son, 91's fe_fit with 75's
  controls): ln earnings on layoff x age, layoff x age x index (standardised), closure x age x index, index x age and
  the layoff x father's-wage x age control (the cap makes the replacement rate fall with the wage, 99). The layoff's
  own cost on the same sample is reported, and the minimum detectable effect (2.8 s.e.) of the index interaction is
  set against it.
Writes output/insurance_index.md / .json (aggregates only). DESCRIPTIVE.
"""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import OUT  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R99 = _load("s99", "99.SimulatedReplacementRate.py")
R102 = _load("s102", "102.UIDurationWeeks.py")
R91 = _load("s91", "91.LayoffSelection.py")
R75 = R91.R75
c, COMPS, STRUCT = R91.c, R91.COMPS, R91.STRUCT
RES = {}


def z(s):
    return (s - s.mean()) / s.std()


def main():
    r = R75.build()
    rr = R99.sim_rr(r)
    wk, _ = R102.son_weeks(r)
    r = r.merge(rr[["pid", "rr", "rr_dur"]], on="pid", how="left").merge(wk[["pid", "weeks"]], on="pid", how="left")
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    cohd = pd.get_dummies(r["coh5"], prefix="coh", drop_first=True).astype(float)
    r = pd.concat([r, cohd], axis=1)
    r["agec"] = (r["age"] - 40) / 10
    g = lambda f, x: (f["b"][x], float(np.sqrt(f["V"].loc[x, x])))  # noqa: E731
    md = ["# One pooled insurance index, honestly sized (committee re-read memo, action 5)", "",
          "Built by `140.InsuranceIndex.py` (2026-10-24); design in its docstring. Within-son slopes x (age-40)/10; index "
          "per standard deviation; s.e. clustered by 1968 family; MDE = 2.8 s.e. (80% power, 5% test). *** p<0.01, "
          "** p<0.05, * p<0.1. **Descriptive.**", "",
          "| index | sons | layoff's own cost on this sample | layoff x age x index | MDE of the interaction | closure x age x index |",
          "|---|---|---|---|---|---|"]
    for lab, build in (("A: replacement x duration (1976+)", lambda q: z(q["rr_dur"])),
                       ("B: replacement and total weeks (1984+)", lambda q: (z(q["rr"]) + z(q["weeks"])) / 2)):
        q = r[r["lw"].notna()].copy()
        need = ["rr_dur"] if lab.startswith("A") else ["rr", "weeks"]
        q = q.dropna(subset=need)
        one = q.drop_duplicates("pid").copy()
        one["idx"] = build(one)
        q = q.merge(one[["pid", "idx"]], on="pid", how="left")
        q["idx"] = z(q["idx"])
        XB = R91.xage(q, ["lyp"] + COMPS + STRUCT + list(cohd.columns) + ["idx"])
        flw = q["f_lw"] - np.average(one["f_lw"], weights=one["wt"])
        q["lay_idx_xa"] = q["f_sh_layoff"] * q["idx"] * q["agec"]
        q["clo_idx_xa"] = q["f_sh_close"] * q["idx"] * q["agec"]
        q["lay_flw_xa"] = q["f_sh_layoff"] * flw * q["agec"]
        f0 = R91.fe_fit(q, "ly", XB)
        f = R91.fe_fit(q, "ly", XB + ["lay_idx_xa", "clo_idx_xa", "lay_flw_xa"])
        own, it, cl = g(f0, "f_sh_layoff_xa"), g(f, "lay_idx_xa"), g(f, "clo_idx_xa")
        md.append(f"| {lab} | {q['pid'].nunique():,} | {c(own)} | {c(it)} | {2.8 * it[1]:.3f} | {c(cl)} |")
        RES[lab] = {"own": list(own), "inter": list(it), "mde": 2.8 * it[1], "closure": list(cl), "sons": int(q["pid"].nunique())}
        print(md[-1], flush=True)
    md.append("")
    (OUT / "insurance_index.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "insurance_index.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
