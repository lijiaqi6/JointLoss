r"""IPW moment set (Fable 10-hour plan, Block 3, 2026-10-19): the 66 moments on the sons in the attrition base of
IGE/41.AgeProfileMeasurement.py, each son-year weighted by 41's weight for its age band (ipw_build.py), with 500
cluster-bootstrap draws of the 1968 families (weights held at their full-sample values). Also the same moments on the
same sons unweighted, to separate the sample restriction from the weighting. Writes output/data_moments_ipw.json and
output/ipw_moments.md (aggregates)."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_data as bd  # noqa: E402
import core  # noqa: E402

NBOOT = 500


def band_of(a):
    return np.select([a <= 29, a <= 34, a <= 39, a <= 44], ["25-29", "30-34", "35-39", "40-44"], "45-49")


def weighted_panel():
    P = pd.read_pickle(HERE / "output" / "data_panel.pkl")
    W = pd.read_pickle(HERE / "output" / "ipw_sons.pkl")
    base = set(W["pid"])
    P = P[P["pid"].isin(base)].copy()
    P["band"] = band_of(P["age"].to_numpy())
    P = P.merge(W, on=["pid", "band"], how="left")
    P["w"] = P["ipw"].fillna(1.0)          # a son in the base without a weight for a band: not modelled by 41 (rare)
    return P.sort_values(["pid", "wave"]).reset_index(drop=True)


if __name__ == "__main__":
    P0 = pd.read_pickle(HERE / "output" / "data_panel.pkl")
    C = bd.constants(P0)                    # terciles and x-bar of the full sample, as in the targets
    P = weighted_panel()
    A = bd.arrays(P)
    A["w"] = P["w"].to_numpy()
    m_ipw = core.moments(A, C)
    Au = {k: v for k, v in A.items() if k != "w"}
    m_res = core.moments(Au, C)
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
        if b % 100 == 0:
            print("boot", b, flush=True)
    sd = np.nanstd(np.array(draws), axis=0, ddof=1)
    D = json.load(open(HERE / "output" / "data_moments.json"))
    json.dump({"names": core.MOMENT_NAMES, "m": m_ipw.tolist(), "sd": sd.tolist(), "C": D["C"],
               "m_restricted_unweighted": m_res.tolist(), "n_sons": int(P["pid"].nunique()), "n_rows": int(len(P)),
               "note": "IPW: sons in 41's attrition base, rows weighted by 41's band weight; bootstrap with fixed weights"},
              open(HERE / "output" / "data_moments_ipw.json", "w"), indent=1)
    L = ["# IPW moment set vs the targets", "", f"Sons {P['pid'].nunique()}, rows {len(P)}.", "",
         "| moment | targets | (s.e.) | same sons, unweighted | IPW | (s.e.) | IPW - targets in target s.e. |",
         "|---|---|---|---|---|---|---|"]
    for n, a, s0, r_, w_, s1 in zip(core.MOMENT_NAMES, D["m"], D["sd"], m_res, m_ipw, sd):
        L.append(f"| {n} | {a:.4f} | ({s0:.4f}) | {r_:.4f} | {w_:.4f} | ({s1:.4f}) | {(w_ - a) / s0:+.1f} |")
    (HERE / "output" / "ipw_moments.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))
