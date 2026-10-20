"""Collect Q, Q by block and key moments of estimate.py evaluate runs for the step table of diagnostics_20261018.md.
Run: python steps_table.py <label>=<evaluate dir> ... [--ids id1,id2,...] [--csv out.csv]
Aggregate numbers only."""
import json
import sys
from pathlib import Path

import pandas as pd


def main(argv):
    ids, out = None, None
    pairs = []
    it = iter(argv)
    for a in it:
        if a == "--ids":
            ids = next(it).split(",")
        elif a == "--csv":
            out = next(it)
        else:
            k, v = a.split("=", 1)
            pairs.append((k, Path(v)))
    Q, B, Mo = {}, {}, {}
    data = None
    for lab, d in pairs:
        ev = json.loads((d / "evaluate.json").read_text())
        Q[lab] = ev["Q"]
        B[lab] = pd.read_csv(d / "q_by_block.csv", index_col=0)["sum"]
        m = pd.read_csv(d / "moments.csv").set_index("id")
        Mo[lab] = m["sim"]
        data = m[["value", "se", "in_objective"]]
    Bt = pd.DataFrame(B)
    Bt.loc["Q total"] = pd.Series(Q)
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 30)
    print(Bt.round(1).to_string())
    if ids:
        T = pd.concat([data.loc[ids, ["value", "se"]], pd.DataFrame(Mo).loc[ids]], axis=1)
        print(T.to_string(float_format=lambda x: f"{x:.4g}"))
    if out:
        Bt.to_csv(out)


if __name__ == "__main__":
    main(sys.argv[1:])
