r"""Displacement flags for BPS's household-year panel (IGE/bps_reconciliation, 2026-10-18).

Keys: BPS's psid_cons.dta rows (year = income year - 1900, 98..108; id = interview number of wave year + 1901).
Husband's displacements: IGE/data/psid_displacement.pkl (saved output of IGE/19.FatherDisplacement.py; flags main /
strict / quit by male head pid x calendar year). Wife's job ends: IGE/25.JointJobLoss.wife_events() called on
IGE/data/psid_person_year.pkl and the wife's reason-for-job-end reports R of IGE/23.CorrelatedShocks.extras()
(cached in IGE/data/correlated_shocks_fam.pkl). Nothing in IGE/ is edited; the modules are imported via importlib.

For a BPS row with income year Y (wave Y + 1), the two-year difference x_Y - x_{Y-2} spans calendar years Y-1 and Y.
  hd / wd   husband / wife displaced (code 1 closure or 3 layoff) in calendar year Y-1 or Y
  hs / ws   closures only;  hq / wq quits;  wa wife any job end (codes 1,2,3,4,7,8)
  jd        joint displacement: hd & wd in the same interval;  jd_sy: both in the same calendar year
  *_n / *_p same flags for the next interval (Y+1, Y+2) and the previous one (Y-3, Y-2), same couple (pids)
Output: <work>/flags.dta and <work>/flags.csv (work dir given as argv[1]).
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import os
DROPBOX = Path(os.environ.get("DROPBOX", Path.home() / "Dropbox"))   # raw data, read only (Mac: export DROPBOX)

IGE = Path(__file__).resolve().parents[2]                    # repository root
SHIP = Path(DROPBOX / "ReplicationPapers/Consumption Inequality and Family Labor Supply"
            "/116142-V1/AER_2012_1549_data/output")
sys.path.insert(0, str(IGE))
DATA = Path(os.environ.get("JOINTLOSS_DATA", IGE / "data"))


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, IGE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main(work):
    work = Path(work)
    P25 = _load("p25", "25.JointJobLoss.py")
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    R = P25.P23.extras()["R"]
    ev = P25.wife_events(py, R)                       # {'main','strict','any','quit'}: set of (wife pid, year)
    d = pd.read_pickle(DATA / "psid_displacement.pkl")
    hs = {k: set(zip(d.loc[d[k] == 1, "pid"].astype(np.int64), d.loc[d[k] == 1, "year"].astype(int)))
          for k in ("main", "strict", "quit")}

    b = pd.read_stata(SHIP / "psid_cons.dta", columns=["year", "id"], convert_categoricals=False)
    b["wave"] = (b["year"].astype(int) + 1901)
    b["id"] = b["id"].astype(int)
    hd = py[py["head"]][["wave", "int", "pid"]].drop_duplicates(["wave", "int"]).rename(
        columns={"int": "id", "pid": "h_pid"})
    wf = py[py["wife"]][["wave", "int", "pid"]].drop_duplicates(["wave", "int"]).rename(
        columns={"int": "id", "pid": "w_pid"})
    b = b.merge(hd, on=["wave", "id"], how="left").merge(wf, on=["wave", "id"], how="left")
    Y = b["wave"].to_numpy() - 1
    hp = b["h_pid"].fillna(-1).astype(np.int64).to_numpy()
    wp = b["w_pid"].fillna(-1).astype(np.int64).to_numpy()

    def anyin(S, p, lo, hi):
        return np.array([float(q >= 0 and any((q, y) in S for y in range(a, z + 1))) for q, a, z in zip(p, lo, hi)])

    def same_year(S1, p1, S2, p2, lo, hi):
        return np.array([float(a1 >= 0 and a2 >= 0 and any((a1, y) in S1 and (a2, y) in S2 for y in range(a, z + 1)))
                         for a1, a2, a, z in zip(p1, p2, lo, hi)])

    for suf, sh in (("", 0), ("_n", 2), ("_p", -2)):
        lo, hi = Y - 1 + sh, Y + sh
        b["hd" + suf] = anyin(hs["main"], hp, lo, hi)
        b["hs" + suf] = anyin(hs["strict"], hp, lo, hi)
        b["hq" + suf] = anyin(hs["quit"], hp, lo, hi)
        b["wd" + suf] = anyin(ev["main"], wp, lo, hi)
        b["ws" + suf] = anyin(ev["strict"], wp, lo, hi)
        b["wq" + suf] = anyin(ev["quit"], wp, lo, hi)
        b["wa" + suf] = anyin(ev["any"], wp, lo, hi)
        b["jd" + suf] = b["hd" + suf] * b["wd" + suf]
        b["jd_sy" + suf] = same_year(hs["main"], hp, ev["main"], wp, lo, hi)
    b["h_match"] = (hp >= 0).astype(int)
    b["w_match"] = (wp >= 0).astype(int)
    b["h_pid"] = b["h_pid"].fillna(-1).astype(np.int64).astype(float)
    b["w_pid"] = b["w_pid"].fillna(-1).astype(np.int64).astype(float)
    b = b.drop(columns=["wave"])
    b["year"] = b["year"].astype(int)
    b.to_csv(work / "flags.csv", index=False)
    b.to_stata(work / "flags.dta", write_index=False, version=118)
    print(b.describe().T.to_string())
    print("rows", len(b), "head matched", b["h_match"].mean(), "wife matched", b["w_match"].mean())


if __name__ == "__main__":
    main(sys.argv[1])
