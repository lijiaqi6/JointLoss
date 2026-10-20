r"""H4 in long differences in the NLSY97 (Paper B, Fable second ten-hour plan, Block 2, 2026-10-19).

Men of the NLSY97 (born 1980-84; 29.NLSY97AgeProfile.py's frames: hourly wage = earnings / hours of the income year,
valid if earnings in range, hours >= 100 and the wage 2-200 dollars of 2000). Change of the son's mean log hourly wage
between 25-29 and 35-39 on log parental income, by race (Black; "White" = non-Black non-Hispanic as in 29), raw and net
of final-degree dummies (GED, high school, AA, BA, graduate), with parental income measured in 1996 (one year) or as
the 1997-2000 mean; errors-in-variables corrections by the NLSY97 one-year reliability ratio (W 0.430, B 0.492;
age_profile_round2.md A6) for the one-year measure. 200 cluster-bootstrap draws (1997 household).
Writes output/long_difference_nlsy97.json / .md."""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

IGE = Path(__file__).resolve().parent
OUT = IGE / "output"


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, IGE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


if __name__ == "__main__":
    R29 = _load("e29", "29.NLSY97AgeProfile.py")
    L68 = _load("e68", "68.LongDifferenceMeasurement.py")
    k, L = R29.load_extract()
    s, kk, _ = R29.nlsy97_frames(k, L)
    s = R29.degree_dummies(s)
    s = s[(s["female"] == 0) & s["race"].isin(["Black", "White"])]
    print("races:", s.drop_duplicates("pid")["race"].value_counts().to_dict())
    g = s.dropna(subset=["lwage_v"])
    t = pd.DataFrame({
        "m2529": g[g["age"].between(25, 29)].groupby("pid")["lwage_v"].mean(),
        "m3539": g[g["age"].between(35, 39)].groupby("pid")["lwage_v"].mean()})
    first = s.drop_duplicates("pid").set_index("pid")
    for c in ("lyp_pt", "lyp_av", "fam68", "race", *R29.DD):
        t[c] = first[c].reindex(t.index)
    t["black"] = (t["race"] == "Black").astype(float)
    t = t.rename(columns={"fam68": "cl"})
    t["x"], t["xav"] = t["lyp_pt"], t["lyp_av"]
    rng = np.random.default_rng(2026)
    R = {}
    for ctrl, cl in (([], "raw"), (list(R29.DD), "net")):
        R[f"one year 1996|{cl}"] = L68.est_group(t, "3539", "x", ctrl, (0.430, 0.492), rng)
        R[f"1997-2000 mean|{cl}"] = L68.est_group(t, "3539", "xav", ctrl, (1.0, 1.0), rng)
    json.dump(R, open(OUT / "long_difference_nlsy97.json", "w"), indent=1)
    Lines = ["# NLSY97 long differences (25-29 -> 35-39), men", "",
             "| measure | controls | group | raw | (s.e.) | corrected | (s.e.) | n |", "|---|---|---|---|---|---|---|---|"]
    for key, v in R.items():
        meas, cl = key.split("|")
        for grp in ("White", "Black", "White - Black"):
            r = v[grp]
            Lines.append(f"| {meas} | {cl} | {grp} | {r['raw']:.4f} | ({r['raw_se']:.4f}) | {r['cor']:.4f} | "
                         f"({r['cor_se']:.4f}) | {r.get('n', '')} |")
    (OUT / "long_difference_nlsy97.md").write_text("\n".join(Lines) + "\n", encoding="utf-8")
    print("\n".join(Lines))
