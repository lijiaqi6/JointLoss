r"""Data moments and 500-draw cluster-bootstrap s.d. for the moment set named by IGE_MOMENTS (e.g. "g35", "ipw",
"g35,ipw"; Fable 10-hour plan, Blocks 3-4, 2026-10-19). "ipw" restricts to the sons of 41's attrition base and weights
rows by 41's band weights (ipw_moments.weighted_panel); "g35" adds the modal G-job shares at 35-55 by race and parental
tercile (core.moments). Writes output/data_moments_<set>.json (aggregates)."""
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_data as bd  # noqa: E402
import core  # noqa: E402
import ipw_moments  # noqa: E402

NBOOT = 500

if __name__ == "__main__":
    assert core.MOMSET, "set IGE_MOMENTS"
    tag = "_".join(sorted(core.MOMSET))
    P0 = pd.read_pickle(HERE / "output" / "data_panel.pkl")
    if "clean" in core.MOMSET:               # parental income net of the father's spells (clean_build.py)
        kid = pd.read_csv(HERE / "output" / "sons_types.csv", float_precision="round_trip")
        sons = P0.drop_duplicates("pid")["pid"].to_numpy()
        P0 = P0.assign(x=P0["pid"].map(dict(zip(sons, kid["x_clean"]))))
    C = bd.constants(P0)
    P = ipw_moments.weighted_panel() if "ipw" in core.MOMSET else P0
    A = bd.arrays(P)
    if "ipw" in core.MOMSET:
        A["w"] = P["w"].to_numpy()
    m = core.moments(A, C)
    fam = P["fam68"].to_numpy()
    fams, inv = np.unique(fam, return_inverse=True)
    order = np.argsort(inv, kind="stable")
    bounds = np.r_[0, np.cumsum(np.bincount(inv))]
    rows = [order[bounds[i]:bounds[i + 1]] for i in range(len(fams))]
    rng = np.random.default_rng(2026)
    draws = []
    for b in range(NBOOT):
        pick = rng.integers(0, len(fams), len(fams))
        idx = np.concatenate([rows[f] for f in pick])
        copy = np.repeat(np.arange(len(pick)), [len(rows[f]) for f in pick])
        Q = {c: v[idx] for c, v in A.items()}
        Q["pid"] = Q["pid"].astype(np.int64) + 10_000_000 * (copy.astype(np.int64) + 1)
        o = np.lexsort((Q["wave"], Q["pid"]))
        draws.append(core.moments({c: v[o] for c, v in Q.items()}, C))
    sd = np.nanstd(np.array(draws), axis=0, ddof=1)
    np.save(HERE / "output" / f"boot_moments_{tag}.npy", np.array(draws))   # draws for the sandwich (estimate.vcov)
    D = json.load(open(HERE / "output" / "data_moments.json"))
    json.dump({"names": core.MOMENT_NAMES, "m": m.tolist(), "sd": sd.tolist(), "set": tag,
               "C": C if "clean" in core.MOMSET else D["C"], "own_C": "clean" in core.MOMSET,
               "n_sons": int(P["pid"].nunique()), "n_rows": int(len(P))},
              open(HERE / "output" / f"data_moments_{tag}.json", "w"), indent=1)
    for n, v, s_ in zip(core.MOMENT_NAMES[-4:], m[-4:], sd[-4:]):
        print(f"{n} {v:.4f} ({s_:.4f})")
