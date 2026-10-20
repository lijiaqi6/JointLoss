r"""Attrition weights for the model's PSID sons (Fable 10-hour plan, Block 3, 2026-10-19), from the weights of
IGE/41.AgeProfileMeasurement.py (attrition_block: logit of being observed in each band on parental income x race, income
at 25-29 x race, sample source, the parent's age quartic and five-year cohorts; weight 1 / p, p clipped at 0.05; 1 at
25-29). Sons outside 41's base (no family income at 25-29) are outside the IPW sample. Rows at 50-55 take the 45-49
weight (41 stops at 45-49).

Writes (person-level, git-ignored): output/ipw_sons.pkl (pid, band, ipw) and the flag ipw_base in output/sons_types.csv
(row order unchanged). Prints the match rate with the model's sons.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
IGE = HERE.parent


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, IGE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


if __name__ == "__main__":
    R41 = _load("e41", "41.AgeProfileMeasurement.py")
    s = R41.psid_all()
    base = R41.attrition_block(s)
    b = base[(base["female"] == 0) & base["ipw"].notna()][["pid", "band", "ipw"]].drop_duplicates(["pid", "band"])
    b.to_pickle(HERE / "output" / "ipw_sons.pkl")
    P = pd.read_pickle(HERE / "output" / "data_panel.pkl")
    kid = pd.read_csv(HERE / "output" / "sons_types.csv", float_precision="round_trip")
    sons = P.drop_duplicates("pid")["pid"].to_numpy()
    assert len(sons) == len(kid), "sons_types.csv and data_panel.pkl differ in sons"
    ids41 = set(b["pid"])
    obs2529 = set(P.loc[(P["age"] >= 25) & (P["age"] <= 29) & P["lw"].notna(), "pid"])
    kid["ipw_base"] = [int(p in ids41) for p in sons]
    print(f"model sons {len(sons)}; in 41's base {kid['ipw_base'].sum()}; model sons with a wage at 25-29 "
          f"{len(obs2529)}, of whom in 41's base {len(obs2529 & ids41)} ({len(obs2529 & ids41) / len(obs2529):.3f})")
    kid.to_csv(HERE / "output" / "sons_types.csv", index=False, float_format="%.17g")
    print("weights by band:", b.groupby("band")["ipw"].describe()[["count", "mean", "max"]].round(2).to_dict())
