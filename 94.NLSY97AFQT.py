r"""Age or period? The son's tested skill in the NLSY97 IGE by age band (Fable addition D1, 2026-10-20).

87.NLSY79YouthAFQT.py found that the son's AFQT carries 62% of the rise of the NLSY79 earnings IGE between 25-29 and
50-54 (sons born 1957-64, observed 1982-2018). The rise could be age (skill pays more with experience) or period (the
return to skill rose nationally over 1980-2000). The NLSY97 cohort (born 1980-84) reaches 25-29 in 2005-13 and 35-39
in 2015-23, after the rise of the skill premium: if the AFQT's contribution rises with age here too, over the same
ages, it is age.

AFQT: ASVAB_MATH_VERBAL_SCORE_PCT (R9829600; the NLSY97's AFQT-like percentile of the 1997-99 CAT-ASVAB), standardised
  within birth year over the Black and White youths with the 1997 weight; missing -> weighted mean + a flag in the
  structure group (75's rule).
DESIGN: 85.NLSY97WhatIsPassedOn.py's sons (son-years, components, parental income = the 1996 parent report, controls,
  round weights, 200 bootstrap draws of 1997 households); two exact Gelbach splits on the same son-years: A = 85's groups,
  B = A + the son's AFQT as its own group; by band 25-29 ... 40-44 and 25-44; openings 35-39 minus 25-29 on common draws.
  The NLSY79 contributions at the same bands come from output/nlsy79_youth_afqt.json (87). The NLSY97 parental
  measure is one year, so the IGE is attenuated (Section 2's reliability ratios); the AFQT row is the son's own measure
  and is not.
Writes output/nlsy97_afqt.md / .json (aggregates only). Descriptive accounting.
"""
import importlib.util
import json
import sys
import time
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


R85 = _load("s85", "85.NLSY97WhatIsPassedOn.py")
R29, c, Boot, rse = R85.R29, R85.c, R85.Boot, R85.rse
BANDS = ["25-29", "30-34", "35-39", "40-44", "25-44"]
RES = {}


def afqt():
    d = pd.read_csv(R29.CSV, usecols=["R0000100", "R9829600"]).rename(columns={"R0000100": "pid", "R9829600": "pct"})
    d["pct"] = pd.to_numeric(d["pct"], errors="coerce").where(lambda s: s >= 0)
    return d


def main():
    t0 = time.time()
    s, P = R85.build()
    A = afqt()
    one = s.drop_duplicates("pid")[["pid", "birth_year", "w"]].merge(A, on="pid", how="left")
    z = []
    for b, q in one.groupby("birth_year"):
        ok = q["pct"].notna()
        m = np.average(q.loc[ok, "pct"], weights=q.loc[ok, "w"])
        sdv = np.sqrt(np.average((q.loc[ok, "pct"] - m) ** 2, weights=q.loc[ok, "w"]))
        z.append(pd.DataFrame({"pid": q["pid"], "afqt": (q["pct"] - m) / sdv}))
    Z = pd.concat(z)
    Z["afqt_na"] = Z["afqt"].isna().astype(float)
    Z["afqt"] = Z["afqt"].fillna(0.0)                       # standardised: weighted mean of the observed is 0
    s = s.merge(Z, on="pid", how="left")
    s = s[s["female"] == 0].copy()
    BT = Boot(s["fam68"].to_numpy(), s["race"].to_numpy(), seed=R85.SEED)
    G0 = dict(R85.GROUPS)
    GB = dict(G0)
    GB["afqt"] = ["afqt"]
    GB["structure"] = G0["structure"] + ["afqt_na"]
    n79 = json.load(open(OUT / "nlsy79_youth_afqt.json"))
    md = ["# Age or period? The son's tested skill in the NLSY97 IGE (Fable D1)", "",
          "Built by `94.NLSY97AFQT.py` (2026-10-20); design in its docstring. NLSY97 sons born 1980-84, Black and White "
          "pooled with round weights; exact Gelbach split of the earnings IGE by band, A = 85's groups, B = A + the son's "
          "AFQT (ASVAB math-verbal percentile, standardised within birth year); estimate (s.e.; p) from 200 cluster-"
          "bootstrap draws of 1997 households; *** p<0.01, ** p<0.05, * p<0.1. **Descriptive accounting.**", "",
          f"AFQT observed for {1 - one['pct'].isna().mean():.0%} of the youths.", ""]
    for y, ylab in (("learn_v", "ln own earnings"), ("lwage_v", "ln hourly wage")):
        out = {}
        for tag, G in (("A", G0), ("B", GB)):
            R85.GROUPS = G
            out[tag] = {b: R85.run(s if b == "25-44" else s[s["band"] == b], y, BT) for b in BANDS}
        R85.GROUPS = G0
        md += [f"## {ylab}, sons", "", "| row | " + " | ".join(BANDS) + " | opening 35-39 - 25-29 | opening 40-44 - 25-29 |",
               "|---" * 8 + "|"]
        rows = [("A", "b0", "IGE"), ("B", "c:afqt", "son's AFQT (split B)"), ("A", "c:resources", "transfers + parents' "
                "schooling, split A"), ("B", "c:resources", "transfers + parents' schooling, split B"),
                ("A", "b", "rest, split A"), ("B", "b", "rest, split B")]
        for tag, stat, lab in rows:
            R = out[tag]
            cells = [R85.cell(R[b], stat) for b in BANDS]
            ops = []
            for hi in ("35-39", "40-44"):
                if stat in R[hi]["pt"] and stat in R["25-29"]["pt"]:
                    dd = R[hi]["bs"][stat][:, 0] - R["25-29"]["bs"][stat][:, 0]
                    ops.append(c((R[hi]["pt"][stat][0] - R["25-29"]["pt"][stat][0], float(np.nanstd(dd, ddof=1)))))
                else:
                    ops.append("")
            md.append(f"| {lab} | " + " | ".join(cells) + f" | {ops[0]} | {ops[1]} |")
            RES[f"{y}|{tag}|{stat}"] = {b: ([float(R[b]["pt"][stat][0]), float(np.nanstd(R[b]["bs"][stat][:, 0], ddof=1))]
                                         if stat in R[b]["pt"] else None) for b in BANDS}
        sh = out["B"]["25-44"]
        md += ["", f"Share of the 25-44 IGE carried by the son's AFQT: "
               f"{R85.cell(sh, 'c:afqt', share=True)}. Sons / son-years 25-44: {sh['n'][0]:,} / {sh['n'][1]:,}.", ""]
        print(f"{y} {time.time() - t0:.0f}s", flush=True)
    # NLSY79 at the same bands, for the comparison (from 87's json)
    keys = [k for k in n79 if "afqt" in k.lower()]
    md += ["## NLSY79 (87) keys holding the AFQT contribution, for the same-band comparison", "",
           "; ".join(keys[:12]), ""]
    RES["n79_keys"] = keys
    (OUT / "nlsy97_afqt.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "nlsy97_afqt.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
