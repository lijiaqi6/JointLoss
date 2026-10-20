r"""Panel diagnostics of the two untargeted failures of model E (Fable 10-hour plan, Blocks 1-2, 2026-10-19):
core.routes (routes into and out of G jobs; job loss by job type; one-way vs flip type changes) and core.levels (the
wage level by age split into within-son growth and composition). PSID panel with 100 cluster-bootstrap draws (seed
2026); model E at seeds 7-16, R = 20. Run with IGE_STEPS=age,rehire,xacc IGE_FIX=muG,du IGE_R=20.
Writes output/panel_diag_psid.json, output/final_x4/panel_diag_E.json and output/panel_diag.md (aggregates)."""
import json
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import core  # noqa: E402
import estimate as est  # noqa: E402

SEEDS = list(range(7, 17))


def stats(P):
    out = core.routes(P)
    out.update(core.levels(P))
    return out


def model_task(args):
    th, seed = args
    T = est.G_["T"]
    idx = np.repeat(np.arange(T.n), 20)
    _, P = est.sim_moments(th, idx=idx, Dr=core.Draws(len(idx), seed))
    return stats(P)


def psid(nboot=100):
    P = pd.read_pickle(HERE / "output" / "data_panel.pkl")
    A = {c: P[c].to_numpy() for c in P.columns}
    base = stats(A)
    fam = P["fam68"].to_numpy()
    fams, inv = np.unique(fam, return_inverse=True)
    order = np.argsort(inv, kind="stable")
    bounds = np.r_[0, np.cumsum(np.bincount(inv))]
    rows = [order[bounds[i]:bounds[i + 1]] for i in range(len(fams))]
    rng = np.random.default_rng(2026)
    draws = []
    for _ in range(nboot):
        pick = rng.integers(0, len(fams), len(fams))
        idx = np.concatenate([rows[f] for f in pick])
        copy = np.repeat(np.arange(len(pick)), [len(rows[f]) for f in pick])
        Q = {c: v[idx] for c, v in A.items()}
        Q["pid"] = Q["pid"].astype(np.int64) + 10_000_000 * (copy.astype(np.int64) + 1)
        o = np.lexsort((Q["wave"], Q["pid"]))
        draws.append(stats({c: v[o] for c, v in Q.items()}))
    return {k: dict(value=v, se=float(np.nanstd([d[k] for d in draws], ddof=1))) for k, v in base.items()}


if __name__ == "__main__":
    ps = psid()
    json.dump(ps, open(HERE / "output" / "panel_diag_psid.json", "w"), indent=1)
    E = json.load(open(HERE / "output" / "final_x4" / "estimates_E.json"))
    th = core.theta_vec(E["E"]["theta"])
    est.G_.update(est.setup())
    with Pool(est.WORKERS, initializer=est.init_worker) as pool:
        res = pool.map(model_task, [(th, s) for s in SEEDS])
    mod = {k: dict(mean=float(np.mean([r[k] for r in res])), sd=float(np.std([r[k] for r in res], ddof=1)))
           for k in res[0]}
    json.dump({"model": "E", "seeds": SEEDS, "R": 20, "stats": mod},
              open(HERE / "output" / "final_x4" / "panel_diag_E.json", "w"), indent=1)
    L = ["# Panel diagnostics: PSID (s.e., 100 bootstrap draws) vs model E (mean, s.d. over ten seeds)", "",
         "| statistic | PSID | (s.e.) | model | (sd) |", "|---|---|---|---|---|"]
    for k in ps:
        L.append(f"| {k} | {ps[k]['value']:.4f} | ({ps[k]['se']:.4f}) | {mod[k]['mean']:.4f} | ({mod[k]['sd']:.4f}) |")
    (HERE / "output" / "panel_diag.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))
