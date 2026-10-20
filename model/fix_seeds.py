r"""Drop in Q between two solutions over ten seeds (R = 20), for any pair of runs (Fable 3-hour plan, Block 6; generalises
h4_seeds.py, 2026-10-19). The two runs may differ in specification (a parameter fixed or added); both are evaluated
with the code switches of the richer one, so parameters the poorer run lacks are 0, exactly its restriction.

    IGE_STEPS=... python fix_seeds.py --with <run folder>:<model> --without <run folder>:<model> --label <name>

Writes output/final_x4/<label>_seeds.json (Q and gap at 45-49 by seed, drop mean / s.d. / min, passes 3.84 everywhere).
"""
import argparse
import json
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import core  # noqa: E402
import estimate as est  # noqa: E402
import lattice_q as lq  # noqa: E402

SEEDS = list(range(7, 17))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--with", dest="with_", required=True)
    ap.add_argument("--without", required=True)
    ap.add_argument("--label", required=True)
    a = ap.parse_args()
    th = {}
    for k, spec in (("with", a.with_), ("without", a.without)):
        f, m = spec.rsplit(":", 1)
        th[k] = core.theta_vec(json.load(open(Path(f) / "estimates.json"))[m]["theta"])
    est.G_.update(est.setup())
    with Pool(est.WORKERS, initializer=est.init_worker) as p:
        res = p.map(lq.q_task, [(th[k], 20, s) for k in ("with", "without") for s in SEEDS])
    n = len(SEEDS)
    Q = {"with": [r["Q"] for r in res[:n]], "without": [r["Q"] for r in res[n:]]}
    G = {"with": [r["gap_4549"] for r in res[:n]], "without": [r["gap_4549"] for r in res[n:]]}
    d = np.array(Q["without"]) - np.array(Q["with"])
    out = {"with": a.with_, "without": a.without, "steps": sorted(core.STEPS), "seeds": SEEDS, "R": 20, "Q": Q,
           "gap_4549": G, "drop": dict(mean=float(d.mean()), sd=float(d.std(ddof=1)), min=float(d.min()),
                                       pass_all=bool((d > 3.84).all()))}
    (HERE / "output" / "final_x4").mkdir(parents=True, exist_ok=True)
    json.dump(out, open(HERE / "output" / "final_x4" / f"{a.label}_seeds.json", "w"), indent=1)
    print(a.label, out["drop"])
