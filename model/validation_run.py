r"""Untargeted validation of the selected model E (Fable 3-hour plan, Block 3, 2026-10-19): core.validation on the PSID
panel (value and 300 cluster-bootstrap draws, seed 2026) and on the simulated panel of model E at seeds 7-16 (R = 20).
Run with IGE_STEPS=age,rehire,xacc IGE_FIX=muG,du IGE_R=20. Needs output/data_panel.pkl (local, git-ignored).
Writes output/validation_psid.json and output/final_x4/validation_E.json (aggregates)."""
import json
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_data as bd  # noqa: E402
import core  # noqa: E402
import estimate as est  # noqa: E402

SEEDS = list(range(7, 17))


def model_task(args):
    th, seed = args
    T = est.G_["T"]
    idx = np.repeat(np.arange(T.n), 20)
    Dr = core.Draws(len(idx), seed)
    _, P = est.sim_moments(th, idx=idx, Dr=Dr)
    return core.validation(P, est.G_["C"])


def psid():
    P = pd.read_pickle(HERE / "output" / "data_panel.pkl")
    C = bd.constants(P)
    A = bd.arrays(P)
    base = core.validation(A, C)
    fam = P["fam68"].to_numpy()
    fams, inv = np.unique(fam, return_inverse=True)
    order = np.argsort(inv, kind="stable")
    bounds = np.r_[0, np.cumsum(np.bincount(inv))]
    rows = [order[bounds[i]:bounds[i + 1]] for i in range(len(fams))]
    rng = np.random.default_rng(2026)
    draws = []
    for _ in range(300):
        pick = rng.integers(0, len(fams), len(fams))
        idx = np.concatenate([rows[f] for f in pick])
        copy = np.repeat(np.arange(len(pick)), [len(rows[f]) for f in pick])
        Q = {c: v[idx] for c, v in A.items()}
        Q["pid"] = Q["pid"].astype(np.int64) + 10_000_000 * (copy.astype(np.int64) + 1)
        o = np.lexsort((Q["wave"], Q["pid"]))
        Q = {c: v[o] for c, v in Q.items()}
        draws.append(core.validation(Q, C))
    out = {}
    for k, v in base.items():
        d = np.array([x[k] for x in draws])
        se = float(np.nanstd(d, ddof=1))
        out[k] = dict(value=v, se=se, p=float(2 * (1 - norm.cdf(abs(v) / se))) if se > 0 else float("nan"))
    # derived: W - B differences, the opening below the median, the between-G share
    for k in ("mlw_3539", "mlw_4549", "rank_2529", "rank_3034", "rank_4549"):
        d = np.array([x[f"{k}_W"] - x[f"{k}_B"] for x in draws])
        out[f"{k}_gap"] = dict(value=base[f"{k}_W"] - base[f"{k}_B"], se=float(np.nanstd(d, ddof=1)))
    return out


if __name__ == "__main__":
    ps = psid()
    json.dump(ps, open(HERE / "output" / "validation_psid.json", "w"), indent=1)
    E = json.load(open(HERE / "output" / "final_x4" / "estimates_E.json"))
    th = core.theta_vec(E["E"]["theta"])
    est.G_.update(est.setup())
    with Pool(est.WORKERS, initializer=est.init_worker) as pool:
        res = pool.map(model_task, [(th, s) for s in SEEDS])
    mod = {k: dict(mean=float(np.mean([r[k] for r in res])), sd=float(np.std([r[k] for r in res], ddof=1)))
           for k in res[0]}
    for k in ("mlw_3539", "mlw_4549", "rank_2529", "rank_3034", "rank_4549"):
        g = [r[f"{k}_W"] - r[f"{k}_B"] for r in res]
        mod[f"{k}_gap"] = dict(mean=float(np.mean(g)), sd=float(np.std(g, ddof=1)))
    json.dump({"model": "E", "seeds": SEEDS, "R": 20, "stats": mod}, open(HERE / "output" / "final_x4" /
                                                                          "validation_E.json", "w"), indent=1)
    for k in mod:
        p_ = ps[k]
        print(f"{k:20s} PSID {p_['value']:.4f} ({p_['se']:.4f})  model {mod[k]['mean']:.4f} (sd {mod[k]['sd']:.4f})  "
              f"t {(mod[k]['mean'] - p_['value']) / p_['se']:.1f}")
