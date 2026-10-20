r"""Judge one model step (Fable second plan, Block 4, 2026-10-19): a run with the step against a run without it, on the
same moment set and draws.

    python judge_step.py --with <run folder>:<model> --without <run folder>:<model> --label <name>

The code switches (IGE_STEPS, IGE_FIX, IGE_MOMENTS) are taken from the WITH run's estimates.json, so the poorer run is
evaluated with the richer run's code and its missing parameters at 0 (exactly its restriction). Reports: the drop in Q
over seeds 7-16 at R = 20 (mean, s.d., min, passes 3.84 at every seed); the new parameters with sandwich s.e. and p;
Q by moment block in both runs; the targeted moments whose |t| changes by more than 1; the race parameters a3, dg1,
db1, dgx in both; the White - Black IGE gap at 30-34 and 45-49; and a verdict (kept / rejected / not separable).
Writes output/final_x4/judge_<label>.json and .md.
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def spec_of(folder):
    E = json.load(open(Path(folder) / "estimates.json"))
    return E.get("steps", []), E.get("fixed", []), E.get("moments", "targets")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--with", dest="with_", required=True)
    ap.add_argument("--without", required=True)
    ap.add_argument("--label", required=True)
    a = ap.parse_args()
    fw, mw = a.with_.rsplit(":", 1)
    steps, fixed, moments = spec_of(fw)
    env = dict(os.environ, IGE_STEPS=",".join(steps), IGE_FIX=",".join(fixed), IGE_R="20",
               IGE_MOMENTS="" if moments == "targets" else moments)
    if os.environ.get("_JUDGE_CHILD") != "1":                     # re-run self with the WITH run's switches set
        env["_JUDGE_CHILD"] = "1"
        sys.exit(subprocess.run([sys.executable, __file__] + sys.argv[1:], env=env).returncode)

    import numpy as np
    from multiprocessing import Pool
    from scipy.stats import norm
    sys.path.insert(0, str(HERE))
    import core
    import estimate as est
    import lattice_q as lq

    fo, mo = a.without.rsplit(":", 1)
    Ew = json.load(open(Path(fw) / "estimates.json"))[mw]
    Eo = json.load(open(Path(fo) / "estimates.json"))[mo]
    th = {"with": core.theta_vec(Ew["theta"]), "without": core.theta_vec(Eo["theta"])}
    est.G_.update(est.setup())
    seeds = list(range(7, 17))
    with Pool(est.WORKERS, initializer=est.init_worker) as pool:
        res = pool.map(lq.q_task, [(th[k], 20, s) for k in ("with", "without") for s in seeds])
        mom = pool.map(est.mom_task, [th["with"], th["without"]])
    n = len(seeds)
    qw, qo = np.array([r["Q"] for r in res[:n]]), np.array([r["Q"] for r in res[n:]])
    d = qo - qw
    new = [p for p in core.PARAMS if p in Ew["se"] and p not in Eo.get("se", {})]
    newp = {}
    for p in new:
        v, s = Ew["theta"][p], Ew["se"][p]
        newp[p] = dict(value=v, se=s, p=float(2 * (1 - norm.cdf(abs(v) / s))))
    md, sd = est.G_["md"], est.G_["sd"]
    tw, to = (mom[0] - md) / sd, (mom[1] - md) / sd
    moved = [(nm, float(b), float(c)) for nm, b, c in zip(core.MOMENT_NAMES, to, tw) if abs(abs(c) - abs(b)) > 1]
    blocks = {b: (float(np.mean([r["Q " + b] for r in res[n:]])), float(np.mean([r["Q " + b] for r in res[:n]])))
              for b in lq.BLOCKS}
    race = {p: (Eo["theta"].get(p, 0.0), Eo.get("se", {}).get(p), Ew["theta"].get(p, 0.0), Ew["se"].get(p))
            for p in ("a3", "dg1", "db1", "dgx")}
    gaps = {k: (float(np.mean([r[k] for r in res[n:]])), float(np.mean([r[k] for r in res[:n]])))
            for k in ("gap_3034", "gap_4549")}
    passes_q = bool((d > 3.84).all())
    passes_w = all(v["p"] < 0.05 for v in newp.values()) if newp else False
    verdict = "kept" if passes_q and passes_w else ("rejected" if not passes_q and not passes_w else "not separable")
    out = dict(label=a.label, with_=a.with_, without=a.without, steps=steps, fixed=fixed, moments=moments,
               drop=dict(mean=float(d.mean()), sd=float(d.std(ddof=1)), min=float(d.min()), pass_all=passes_q),
               new_parameters=newp, blocks=blocks, moved=moved, race=race, gaps=gaps, verdict=verdict)
    (HERE / "output" / "final_x4").mkdir(exist_ok=True)
    json.dump(out, open(HERE / "output" / "final_x4" / f"judge_{a.label}.json", "w"), indent=1)
    L = [f"# Step {a.label}: {a.with_} against {a.without}", "",
         f"Drop in Q over ten seeds: mean {d.mean():.1f} (s.d. {d.std(ddof=1):.1f}; min {d.min():.1f}); passes 3.84 at "
         f"every seed: {passes_q}. Verdict: **{verdict}**.", "", "New parameters: " + "; ".join(
             f"{p} {v['value']:.4f} ({v['se']:.4f}), p = {v['p']:.3f}" for p, v in newp.items()), "",
         "| block | Q without | Q with |", "|---|---|---|"]
    L += [f"| {b} | {x:.1f} | {y:.1f} |" for b, (x, y) in blocks.items()]
    L += ["", "Moments whose |t| changes by more than 1 (t without -> t with): " + "; ".join(
        f"{nm} {b:+.1f} -> {c:+.1f}" for nm, b, c in moved), "",
          "Race parameters (without -> with): " + "; ".join(
              f"{p} {x:.4f} -> {z:.4f}" for p, (x, y, z, w) in race.items()),
          "Gaps (without -> with): " + "; ".join(f"{k} {x:.3f} -> {y:.3f}" for k, (x, y) in gaps.items())]
    (HERE / "output" / "final_x4" / f"judge_{a.label}.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))
