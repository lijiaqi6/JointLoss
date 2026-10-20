r"""H4 (racial difference in the pay-off of parental income in accumulation) over ten seeds, Paper B final lattice
(2026-10-19). The lattice job compares models within one specification; the two H4 tests fix dgx, so their drops are
computed here on the same draws (seeds 7-16, R = 20) as lattice_q.py. Run with IGE_STEPS=age,rehire,xacc:

    python h4_seeds.py <folder with the run folders>     (e.g. a copy of model/hpc_runs from origin/main)

Writes output/final_x4/h4_seeds.json.
"""
import json
import os
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import core  # noqa: E402
import estimate as est  # noqa: E402
import lattice_q as lq  # noqa: E402

RUNS = {"A": ("Lx4_A_j11861506", "A"), "A without H4": ("ige_full_20261018_224720_j11861515", "A"),
        "E": ("Lx4_E_j11861512", "E"), "E without H4": ("ige_full_20261018_224720_j11861516", "E")}
SEEDS = list(range(7, 17))

if __name__ == "__main__":
    root = Path(sys.argv[1])
    th = {k: core.theta_vec(json.load(open(root / d / "estimates.json"))[m]["theta"]) for k, (d, m) in RUNS.items()}
    est.G_.update(est.setup())
    with Pool(est.WORKERS, initializer=est.init_worker) as p:
        res = p.map(lq.q_task, [(th[k], 20, s) for k in RUNS for s in SEEDS])
    Q = {k: [r["Q"] for r in res[i * len(SEEDS):(i + 1) * len(SEEDS)]] for i, k in enumerate(RUNS)}
    G = {k: [r["gap_4549"] for r in res[i * len(SEEDS):(i + 1) * len(SEEDS)]] for i, k in enumerate(RUNS)}
    out = {"seeds": SEEDS, "R": 20, "Q": Q, "gap_4549": G, "drops": {}}
    for a, b, lab in (("A without H4", "A", "alone"), ("E without H4", "E", "given dg1 + db1")):
        d = np.array(Q[a]) - np.array(Q[b])
        out["drops"][lab] = dict(without=a, with_=b, mean=float(d.mean()), sd=float(d.std(ddof=1)), min=float(d.min()),
                                 pass_all=bool((d > 3.84).all()))
        print(lab, out["drops"][lab])
    (HERE / "output" / "final_x4").mkdir(parents=True, exist_ok=True)
    json.dump(out, open(HERE / "output" / "final_x4" / "h4_seeds.json", "w"), indent=1)
