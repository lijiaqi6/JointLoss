r"""Is the pooled rise of the IGE with age a period or cohort effect? (Fable addition D2, 2026-10-20)

Appendix D tests the RACIAL opening against cohorts and calendar time (33.AgeProfileRobustness.py); the pooled rise of
the IGE, the paper's frame, was not tested. This script reruns those checks on Black and White sons pooled with PSID
weights (33's psid_frames(): sons' ln own earnings and ln family income at 25-49, parental income = 13-19 mean).
Specifications (each a separate set of band regressions, joint cluster-robust covariance by 1968 family, 33's Cells):
  baseline            single-age dummies + the parent's age quartic (33's A4)
  cohorts             sons born 1951-64, 1965-79, 1980-89 (each observed in different decades)
  IGE x cohort        + c, c^2, lyp x c, c = (birth year - 1965)/10: the band IGE of the 1965 cohort
  year FE             + income-year fixed effects in every band
  period-varying IGE  + lyp x (income year - 1995)/10 and the year itself: the band IGE evaluated in 1995
  fixed window        income years 1990-2010 only (the bands then hold different cohorts)
Statistics: the IGE at 25-29 and 45-49, the rise 45-49 minus 25-29, the mean of the bands from 35 minus the mean below
35 (33's opening), and the linear trend per 10 years.
Writes output/pooled_rise_checks.md / .json (aggregates only).
"""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import OUT, stars  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R33 = _load("s33", "33.AgeProfileRobustness.py")
BL = R33.BL
MID = {b: (int(b[:2]) + int(b[3:])) / 2 for b in BL}
RES = {}


def c(t):
    e, se, p = t
    return f"{e:.3f}{stars(p)} ({se:.3f}; p={'<0.001' if p < 0.001 else f'{p:.3f}'})"


def fit(d, y, ctrl=(), fe="agei"):
    d = d.assign(_y=d[y], cellb=d["band"])
    return R33.Cells(d, "_y", "lyp", "cellb", list(ctrl), fe, w="wt")


def stats_(R):
    bands = [b for b in BL if R.has(b)]
    lo, hi = [b for b in bands if int(b[:2]) < 35], [b for b in bands if int(b[:2]) >= 35]
    out = {"bands": bands}
    out["first"] = R.lin([(bands[0], "x", 1)])
    out["last"] = R.lin([(bands[-1], "x", 1)])
    out["rise"] = R.lin([(bands[-1], "x", 1), (bands[0], "x", -1)])
    out["open"] = R.lin([(b, "x", 1 / len(hi)) for b in hi] + [(b, "x", -1 / len(lo)) for b in lo]) if lo and hi else None
    m = np.array([MID[b] for b in bands])
    wts = (m - m.mean()) / ((m - m.mean()) ** 2).sum() * 10
    out["trend"] = R.lin([(b, "x", w) for b, w in zip(bands, wts)])
    return out


def main():
    s = R33.psid_frames()
    s = s[(s["female"] == 0) & s["race"].isin(["Black", "White"]) & s["wt"].gt(0)].copy()
    yr = s["year"] if "year" in s else s["wave"] - 1
    s["iyear"] = yr.astype(int)
    s["per"] = (s["iyear"] - 1995) / 10
    s["lypper"] = s["lyp"] * s["per"]
    A4 = list(R33.A4)
    md = ["# Is the pooled rise of the IGE with age a period or cohort effect? (Fable D2)", "",
          "Built by `95.PooledRiseChecks.py` (2026-10-20); design in its docstring. PSID sons 25-49, Black and White pooled "
          "with PSID weights; band IGEs with single-age dummies and the parent's age quartic; estimate (s.e.; p) "
          "clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1.", ""]
    for y, ylab in (("learn", "ln own earnings"), ("lfam", "ln family income")):
        specs = [("baseline", s, A4, "agei")]
        for lab, (a, b) in (("born 1951-64", (1951, 1964)), ("born 1965-79", (1965, 1979)), ("born 1980-89", (1980, 1989))):
            specs.append((lab, s[s["birth_year"].between(a, b)], A4, "agei"))
        specs.append(("IGE x cohort (1965 cohort)", s, A4 + ["coh", "coh2", "lypcoh"], "agei"))
        yd = pd.get_dummies(s["iyear"], prefix="yr", drop_first=True, dtype=float)
        sy = pd.concat([s, yd], axis=1)
        specs.append(("income-year FE", sy, A4 + list(yd.columns), "agei"))
        specs.append(("period-varying IGE (at 1995)", s, A4 + ["per", "lypper"], "agei"))
        specs.append(("fixed window, income years 1990-2010", s[s["iyear"].between(1990, 2010)], A4, "agei"))
        md += [f"## {ylab}", "", "| specification | bands | first band | last band | rise last - first | "
               "mean >= 35 minus mean < 35 | trend per 10 years | children |", "|---" * 8 + "|"]
        for lab, d, ctrl, fe in specs:
            R = fit(d, y, ctrl, fe)
            st = stats_(R)
            nch = int(d.loc[d[y].notna(), "pid"].nunique())
            md.append(f"| {lab} | {st['bands'][0]} .. {st['bands'][-1]} | {c(st['first'])} | {c(st['last'])} | "
                      f"{c(st['rise'])} | {c(st['open']) if st['open'] else ''} | {c(st['trend'])} | {nch:,} |")
            RES[f"{y}|{lab}"] = {k: (list(map(float, v)) if isinstance(v, tuple) else v) for k, v in st.items()}
        md.append("")
        print(ylab, "done", flush=True)
    (OUT / "pooled_rise_checks.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "pooled_rise_checks.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
