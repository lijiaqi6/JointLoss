r"""One-dimensional profiles of Q at the final-lattice solutions (Fable 3-hour plan, Block 1, 2026-10-19). Models H and
G moved by 0.0 and 0.1 from their starting points in 12,000 CMA-ES evaluations; if Q falls along one parameter from
the start, the solution is under-converged. Run with IGE_STEPS=age,rehire,xacc IGE_FIX=muG,du IGE_R=20.
Writes output/final_x4/profile_q.json."""
import json
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import core  # noqa: E402
import estimate as est  # noqa: E402

F = HERE / "output" / "final_x4"
PROFILES = [("H from B's solution", "B", "db1", [-0.04, -0.02, -0.01, 0.01, 0.02, 0.04]),
            ("G from A's solution", "A", "db1", [-0.04, -0.02, -0.01, 0.01, 0.02, 0.04]),
            ("D from E's solution", "E", "a3", [-0.4, -0.2, -0.1, 0.1, 0.2, 0.4])]

if __name__ == "__main__":
    tasks, meta = [], []
    for lab, m, p, grid in PROFILES:
        th = core.theta_vec(json.load(open(F / f"estimates_{m}.json"))[m]["theta"])
        for v in [0.0] + grid:
            t = th.copy()
            t[core.PARAMS.index(p)] = v
            tasks.append(t)
            meta.append((lab, p, v))
    est.G_.update(est.setup())
    with Pool(est.WORKERS, initializer=est.init_worker) as pool:
        qs = pool.map(est.eval_task, tasks)
    out = {}
    for (lab, p, v), q in zip(meta, qs):
        out.setdefault(lab, {"parameter": p, "grid": [], "Q": []})
        out[lab]["grid"].append(v)
        out[lab]["Q"].append(q)
    for lab, d in out.items():
        base = d["Q"][0]
        d["base_Q"], d["best_Q"] = base, min(d["Q"])
        d["best_value"] = d["grid"][int(np.argmin(d["Q"]))]
        print(f"{lab}: base Q {base:.2f}; best {d['best_Q']:.2f} at {d['parameter']} = {d['best_value']}; "
              + ", ".join(f"{g:+.2f}: {q:.2f}" for g, q in zip(d["grid"], d["Q"])))
    json.dump(out, open(F / "profile_q.json", "w"), indent=1)
