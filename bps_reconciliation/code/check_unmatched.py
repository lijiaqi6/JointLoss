"""Which PSID sample do BPS rows without a head in data/psid_person_year.pkl come from? (2026-10-18)
Reads the 2023 individual file (Dropbox, read only): 1968 id, and per wave 1999-2009 the interview number, sequence and
relation of each person; finds the head (relation 10, sequence 1) of each (wave, interview number) and tabulates the
1968 family id range (SRC 1-2930, immigrant 1997 3001-3511, SEO 5001-6872) of BPS rows that build_flags.py could
not match. Usage: python check_unmatched.py <work dir with flags.csv>"""
import re
import sys
from pathlib import Path

import pandas as pd
import os
DROPBOX = Path(os.environ.get("DROPBOX", Path.home() / "Dropbox"))   # raw data, read only (Mac: export DROPBOX)

IND = Path(DROPBOX / "PSID/Individual/ind2023er/IND2023ER")
W = {1999: ("ER33501", "ER33502", "ER33503"), 2001: ("ER33601", "ER33602", "ER33603"),
     2003: ("ER33701", "ER33702", "ER33703"), 2005: ("ER33801", "ER33802", "ER33803"),
     2007: ("ER33901", "ER33902", "ER33903"), 2009: ("ER34001", "ER34002", "ER34003")}


def layout(do):
    pos = {}
    for line in open(do, encoding="latin-1"):
        for v, a, b in re.findall(r"(ER\d+)\s+(\d+)\s*-\s*(\d+)", line):
            pos[v] = (int(a) - 1, int(b))
    return pos


def main(work):
    pos = layout(IND.with_suffix(".do"))
    cols = ["ER30001", "ER30002"] + [v for t in W.values() for v in t]
    d = pd.read_fwf(IND.with_suffix(".txt"), colspecs=[pos[c] for c in cols], names=cols, header=None,
                    encoding="latin-1")
    rows = []
    for w, (i, s, r) in W.items():
        x = d[(d[i] > 0) & (d[s] == 1) & (d[r] == 10)][["ER30001", i]].rename(columns={i: "id"})
        x["year"] = w - 1901
        rows.append(x)
    h = pd.concat(rows).drop_duplicates(["year", "id"])
    f = pd.read_csv(Path(work) / "flags.csv")
    f = f.merge(h, on=["year", "id"], how="left")
    f["sample"] = pd.cut(f["ER30001"], [0, 2930, 3511, 4851, 6872, 9308],
                         labels=["SRC", "Immigrant 1997", "Immigrant 2017", "SEO", "Latino"])
    print(pd.crosstab(f["sample"], f["h_match"], dropna=False))
    f[["year", "id", "ER30001", "sample"]].to_csv(Path(work) / "bps_row_sample.csv", index=False)


if __name__ == "__main__":
    main(sys.argv[1])
