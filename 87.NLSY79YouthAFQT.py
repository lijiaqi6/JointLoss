r"""How much of the father's-schooling channel of the NLSY79 IGE runs through the son's pre-market skill (AFQT)?
(Paper B primary goal; follows 86.NLSY79YouthWhatIsPassedOn.py, EVIDENCE 11.37)

86 found the sons' earnings IGE opening with age (0.166***, 25-29 -> 50-54) and the father's schooling carrying a share
that rises with age (0.016 -> 0.076***). Is that the son's skill when he enters the labour market (the father's
schooling raises the son's tested skill, and the market rewards tested skill more with age - Altonji-Pierret employer
learning), or something the father's schooling does beyond the son's measured skill (H4's pay-off in human capital
accumulation, Section 8)?

AFQT: AFQT-3 (2006 revision percentile of the 1980 ASVAB, taken at ages 15-23), standardised within birth year over the
  civilian sample with 1979 weights (70.RauhReplication.py's construction, from its cache data/rauh_nlsy79.pkl, read
  only). Missing (about 6%): weighted mean of the observed + a flag in the structure group (75's rule).
DESIGN: 86's son-years, components, controls, weights and bootstrap (same draws); two exact Gelbach splits on the
  same son-years: A = 86's groups; B = A + the son's AFQT as its own group. The father's schooling element and the
  parents' schooling group are compared across A and B by band (25-29 ... 55-59, 25-59) and in the opening 50-54 minus
  25-29, with A - B on common draws (the part of the father's-schooling contribution that the son's AFQT accounts for).
  AFQT is measured at 15-23, after the parents' schooling and partly after some of the son's own schooling: it is the
  son's skill at labour-market entry, not an innate endowment.
Writes output/nlsy79_youth_afqt.md / .json (aggregates only). Descriptive accounting.
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
from common import DATA, OUT  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R86 = _load("s86", "86.NLSY79YouthWhatIsPassedOn.py")
R74 = R86.R74
c, Boot = R74.c, R74.Boot
BL = R86.BL
RES = {}


def afqt():
    X = pd.read_pickle(DATA / "rauh_nlsy79.pkl")[["pid", "sample_id", "birth_year", "wt79", "afqt3"]].copy()
    X.loc[X["afqt3"] < 0, "afqt3"] = np.nan
    X["p"] = X["afqt3"] / 1000
    X["afqt"] = np.nan
    civ = X["sample_id"].between(1, 14) & X["p"].notna() & (X["wt79"] > 0)
    for by, z in X[civ].groupby("birth_year"):
        mu = np.average(z["p"], weights=z["wt79"])
        sd = np.sqrt(np.average((z["p"] - mu) ** 2, weights=z["wt79"]))
        ii = X.index[(X["birth_year"] == by) & X["p"].notna()]
        X.loc[ii, "afqt"] = (X.loc[ii, "p"] - mu) / sd
    return X[["pid", "afqt"]]


def run_both(D, BT):
    ga = dict(R86.GROUPS)
    gb = {**{k: v for k, v in R86.GROUPS.items() if k != "structure"}, "afqt": ["afqt"],
          "structure": R86.GROUPS["structure"] + ["afqt_na"]}
    out = {}
    for tag, g in (("A", ga), ("B", gb)):
        R86.GROUPS = g
        out[tag] = {b: R86.run(D if b == "25-59" else D[D["band"] == b], BT) for b in BL
                    if (D if b == "25-59" else D[D["band"] == b])["pid"].nunique() >= 150}
    R86.GROUPS = ga
    return out


def stat_of(res, b, name):
    """(point, draws) of a group ('c:...') or an element ('e:col')."""
    r = res.get(b)
    if r is None:
        return None
    if name.startswith("e:"):
        col = name[2:]
        if col not in r["cols"]:
            return None
        name = f"e:{r['cols'].index(col)}"
    if name not in r["pt"]:
        return None
    return r["pt"][name][0], r["bs"][name][:, 0]


def fmt(t):
    return "" if t is None else c((t[0], float(np.nanstd(t[1], ddof=1))))


def sub(a, b):
    return None if a is None or b is None else (a[0] - b[0], a[1] - b[1])


def main():
    t0 = time.time()
    s, k = R86.build()
    s = s.merge(afqt(), on="pid", how="left")
    one = s.drop_duplicates("pid")
    s["afqt_na"] = s["afqt"].isna().astype(float)
    q = one[one["afqt"].notna()]
    s["afqt"] = s["afqt"].fillna(float(np.average(q["afqt"], weights=q["w"])))
    BT = Boot(s["hhid"].to_numpy(), s["race"].to_numpy(), seed=R86.SEED)
    md = ["# The father's-schooling channel of the NLSY79 IGE and the son's AFQT", "",
          "Built by `87.NLSY79YouthAFQT.py` (2026-10-20); design in its docstring. Split A = 86's groups; split B = A + "
          "the son's AFQT (standardised within birth year). Same son-years and bootstrap draws; estimate (s.e.; p), "
          "*** p<0.01, ** p<0.05, * p<0.1; opening = 50-54 minus 25-29. **Descriptive accounting.**", "",
          f"AFQT observed for {int((one['afqt'].notna()).sum()):,} of {len(one):,} youths; weighted mean of the observed "
          f"(standardised) White {np.average(q.loc[q.race == 'White', 'afqt'], weights=q.loc[q.race == 'White', 'w']):.3f}, "
          f"Black {np.average(q.loc[q.race == 'Black', 'afqt'], weights=q.loc[q.race == 'Black', 'w']):.3f}.", ""]
    rows = [("IGE (b0)", "b0", "A"), ("father's schooling element, A", "e:f_hgc", "A"),
            ("father's schooling element, B (with AFQT)", "e:f_hgc", "B"),
            ("mother's schooling element, A", "e:m_hgc", "A"), ("mother's schooling element, B", "e:m_hgc", "B"),
            ("parents' schooling + reading, A", "c:resources", "A"), ("parents' schooling + reading, B", "c:resources", "B"),
            ("son's AFQT, B", "c:afqt", "B"), ("WAGE (occupation wage at 14), B", "c:wage", "B"),
            ("rest, A", "b", "A"), ("rest, B", "b", "B")]
    for samp, S in (("sons", s[s.female == 0]), ("daughters", s[s.female == 1])):
        md += [f"## ln earnings, {samp}", ""]
        for race in ("pooled", "White", "Black"):
            D = S if race == "pooled" else S[S.race == race]
            out = run_both(D, BT)
            md += [f"#### {race}", "", "| | " + " | ".join(BL) + " | opening 50-54 - 25-29 | share 25-59 |",
                   "|---" * (len(BL) + 3) + "|"]
            for lab, nm, tag in rows:
                res = out[tag]
                ent = [stat_of(res, b, nm) for b in BL]
                op = sub(stat_of(res, "50-54", nm), stat_of(res, "25-29", nm))
                tot, b0 = stat_of(res, "25-59", nm), stat_of(res, "25-59", "b0")
                sh = None if tot is None or nm == "b0" else (tot[0] / b0[0], R74.rse(tot[1] / b0[1]))
                md.append(f"| {lab} | " + " | ".join(fmt(e) for e in ent) + f" | {fmt(op)} | "
                          + (c(sh) if sh else "") + " |")
                RES[f"{samp}|{race}|{lab}"] = {"bands": [[float(e[0]), float(np.nanstd(e[1], ddof=1))] if e else None
                                                         for e in ent],
                                               "open": [float(op[0]), float(np.nanstd(op[1], ddof=1))] if op else None}
            # the part of the father's-schooling contribution accounted for by AFQT: A - B on common draws
            ent = [sub(stat_of(out["A"], b, "e:f_hgc"), stat_of(out["B"], b, "e:f_hgc")) for b in BL]
            opA = sub(stat_of(out["A"], "50-54", "e:f_hgc"), stat_of(out["A"], "25-29", "e:f_hgc"))
            opB = sub(stat_of(out["B"], "50-54", "e:f_hgc"), stat_of(out["B"], "25-29", "e:f_hgc"))
            md.append("| **father's schooling, A - B (through the son's AFQT)** | " + " | ".join(fmt(e) for e in ent)
                      + f" | **{fmt(sub(opA, opB))}** | |")
            RES[f"{samp}|{race}|f_hgc A-B"] = [[float(e[0]), float(np.nanstd(e[1], ddof=1))] if e else None for e in ent]
            oo = sub(opA, opB)
            RES[f"{samp}|{race}|f_hgc A-B open"] = [float(oo[0]), float(np.nanstd(oo[1], ddof=1))] if oo else None
            n = out["B"]["25-59"]["n"]
            md += [f"Youths / youth-years: {n[0]:,} / {n[1]:,}.", ""]
        print(f"{samp} {time.time() - t0:.0f}s", flush=True)
    (OUT / "nlsy79_youth_afqt.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "nlsy79_youth_afqt.json", "w"), indent=1)
    print(f"done {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
