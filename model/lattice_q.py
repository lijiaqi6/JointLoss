r"""The hypothesis lattice on common draws (Paper B, 2026-10-18; Fable memo proposals/fable_hpc_next_paperB.md, R3).

    python lattice_q.py hpc_runs/<run1> hpc_runs/<run2> ...

Reads estimates.json of every run folder given; for each model letter (core.NESTED) keeps the solution with the lowest Q
at the estimation draws. No estimation. For every model: Q at seeds 7-16 with R = 5 and R = 20 simulated sons per PSID
son, Q by moment block, the White - Black IGE gap at 30-34 and 45-49, and sandwich standard errors (estimate.vcov) from
a fresh Jacobian at the estimation draws (seed 7, R = 5). Then, per seed, the drop in Q of each race hypothesis (H1 a3,
H2 dg1, H3 db1) alone, given each other one and given both, and the nesting checks (a more general model must not fit
worse). Writes $IGE_OUT (default output/lattice)/lattice.json and lattice.md.
"""
import json
import os
import sys
from multiprocessing import Pool
from pathlib import Path

for v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[v] = "1"

import numpy as np  # noqa: E402
from scipy.stats import norm  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import core  # noqa: E402
import estimate as est  # noqa: E402

SEEDS = [int(x) for x in os.environ.get("IGE_LATTICE_SEEDS", ",".join(map(str, range(7, 17)))).split(",")]
RS = tuple(int(x) for x in os.environ.get("IGE_LATTICE_R", "5,20").split(","))   # R = 20: ~1 GB per worker
BLOCKS = {"IGE": ("ige_",), "returns": ("rets_",), "levels and variances": ("mlw", "vlw"), "G shares": ("G_",),
          "stayer growth": ("gst", "vgst", "acgst"), "moves and displacement": ("mov", "dsp", "gmv", "gds"),
          "zero hours": ("zero",)}
HYP = {"H1 access (a3)": "a3", "H2 pay-off of schooling in accumulation (dg1)": "dg1",
       "H3 entry return to schooling (db1)": "db1"}
OUTD = Path(os.environ.get("IGE_OUT", str(HERE / "output" / "lattice")))


def letter(free):
    """model letter whose fixed-at-zero set equals the race parameters not in `free`."""
    fixed = {"a3", "dg1", "db1"} - set(free)
    return next(k for k, v in core.NESTED.items() if v == fixed)


def q_task(args):
    th, R, seed = args
    T = est.G_["T"]
    idx = np.repeat(np.arange(T.n), R)
    Dr = core.Draws(len(idx), seed)
    m, Pm = est.sim_moments(th, idx=idx, Dr=Dr)
    r = ((m - est.G_["md"]) / est.G_["sd"]) ** 2
    d = dict(zip(core.MOMENT_NAMES, m))
    out = {"Q": float(np.sum(r)), "gap_3034": d["ige_3034_W"] - d["ige_3034_B"],
           "gap_4549": d["ige_4549_W"] - d["ige_4549_B"]}
    for b, pre in BLOCKS.items():
        out["Q " + b] = float(sum(ri for n, ri in zip(core.MOMENT_NAMES, r) if n.startswith(pre)))
    out.update(core.untargeted(Pm))                                # validation, not targets
    return out


def stars(p):
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""


def main(runs):
    best = {}
    for rd in runs:
        E = json.load(open(Path(rd) / "estimates.json"))
        if (sorted(E.get("steps", [])) != sorted(core.STEPS) or E.get("fixed", []) != sorted(est.FIX)
                or E.get("moments", "targets") != (est.MOMENTS or "targets")):
            print(f"skip {rd}: steps {E.get('steps', [])} / fixed {E.get('fixed', [])} differ from this run "
                  f"({sorted(core.STEPS)} / {sorted(est.FIX)}); compare models only within one specification")
            continue
        for k in core.NESTED:
            if k in E and (k not in best or E[k]["Q"] < best[k]["Q"]):
                best[k] = dict(E[k], run=Path(rd).name)
    models = [k for k in "ABFGCHED" if k in best]
    th = {k: core.theta_vec(best[k]["theta"]) for k in models}
    est.G_.update(est.setup())
    tasks = [(th[k], R, s) for k in models for R in RS for s in SEEDS]
    with Pool(est.WORKERS, initializer=est.init_worker) as pool:
        res = pool.map(q_task, tasks)
        se = {}
        for k in models:
            mask = est.free_mask(k)
            J, nm = est.jacobian(th[k], pool, mask)
            V, kind = est.vcov(J, est.G_["sd"])
            se[k] = dict(zip(nm, np.sqrt(np.diag(V)).tolist()))
    it = iter(res)
    Qs = {k: {R: [next(it) for _ in SEEDS] for R in RS} for k in models}
    out = {"runs": [Path(r).name for r in runs], "seeds": SEEDS, "vcov": kind, "models": {}, "hypotheses": {},
           "nesting": []}
    for k in models:
        out["models"][k] = {"run": best[k]["run"], "Q_estimation": best[k]["Q"], "theta": best[k]["theta"], "se": se[k],
                            **{f"R{R}": {key: [d[key] for d in Qs[k][R]] for key in Qs[k][R][0]} for R in RS}}
    # nesting: a model with fewer parameters fixed at zero must not fit worse (per seed, R = 5 and 20)
    for g in models:
        for r_ in models:
            if core.NESTED[g] < core.NESTED[r_]:
                for R in RS:
                    diff = np.array(out["models"][r_][f"R{R}"]["Q"]) - np.array(out["models"][g][f"R{R}"]["Q"])
                    out["nesting"].append(dict(general=g, restricted=r_, R=R, mean=float(diff.mean()),
                                               min=float(diff.min()), violations=int((diff < 0).sum())))
    # hypotheses: drop = Q(without the parameter) - Q(with it), with the other race parameters as in the pair
    for h, p in HYP.items():
        rows = {}
        for g in models:
            r_ = letter(({"a3", "dg1", "db1"} - core.NESTED[g]) - {p})
            if p in core.NESTED[g] or r_ not in models:
                continue
            others = sorted({"a3", "dg1", "db1"} - core.NESTED[g] - {p})
            lab = "alone" if not others else "given " + " + ".join(others)
            rows[lab] = {"with": g, "without": r_}
            for R in RS:
                d = np.array(out["models"][r_][f"R{R}"]["Q"]) - np.array(out["models"][g][f"R{R}"]["Q"])
                rows[lab][f"R{R}"] = dict(mean=float(d.mean()), sd=float(d.std(ddof=1)), min=float(d.min()),
                                          pass_all=bool((d > 3.84).all()))
            v, s = best[g]["theta"][p], se[g].get(p, np.nan)
            rows[lab]["estimate"] = dict(value=v, se=s, p=float(2 * (1 - norm.cdf(abs(v) / s))))
        out["hypotheses"][h] = rows
    OUTD.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(OUTD / "lattice.json", "w"), indent=1)
    L = ["# Hypothesis lattice on common draws", "", f"Runs: {', '.join(out['runs'])}. Seeds {SEEDS[0]}-{SEEDS[-1]}; "
         f"Q on the 66 moments; standard errors: {kind}.", "", "## Models", "",
         f"| Model | fixed at 0 | Q (estimation) | Q R={RS[0]} mean (sd) | Q R={RS[-1]} mean (sd) | gap 30-34 | "
         f"gap 45-49 | Q IGE block R={RS[-1]} |", "|---|---|---|---|---|---|---|---|"]
    for k in models:
        a, b = np.array(out["models"][k][f"R{RS[0]}"]["Q"]), np.array(out["models"][k][f"R{RS[-1]}"]["Q"])
        mm = out["models"][k][f"R{RS[-1]}"]
        L.append(f"| {k} | {', '.join(sorted(core.NESTED[k])) or '-'} | {best[k]['Q']:.1f} | {a.mean():.1f} "
                 f"({a.std(ddof=1):.1f}) | {b.mean():.1f} ({b.std(ddof=1):.1f}) | {np.mean(mm['gap_3034']):.3f} | "
                 f"{np.mean(mm['gap_4549']):.3f} | {np.mean(mm['Q IGE']):.1f} |")
    L += ["", "## Hypotheses: drop in Q when the parameter is added (mean, sd and min over seeds)", "",
          f"| Hypothesis | test | models | R={RS[0]} | R={RS[-1]} | > 3.84 at every seed (R={RS[-1]}) | estimate (sandwich s.e.) |",
          "|---|---|---|---|---|---|---|"]
    for h, rows in out["hypotheses"].items():
        for lab, r in rows.items():
            e = r["estimate"]
            a_, b_ = r[f"R{RS[0]}"], r[f"R{RS[-1]}"]
            L.append(f"| {h} | {lab} | {r['without']} -> {r['with']} | {a_['mean']:.1f} ({a_['sd']:.1f}; min "
                     f"{a_['min']:.1f}) | {b_['mean']:.1f} ({b_['sd']:.1f}; min {b_['min']:.1f}) | "
                     f"{'yes' if b_['pass_all'] else 'no'} | {e['value']:.4f}{stars(e['p'])} ({e['se']:.4f}), "
                     f"p = {e['p']:.3f} |")
    U = json.load(open(HERE / "output" / "untargeted_psid.json"))
    L += ["", "## Untargeted: same-employer growth at 25-34 on log parental income (mean over seeds)", "",
          "| Model | White raw | Black raw | White net of schooling | Black net of schooling |", "|---|---|---|---|---|",
          f"| PSID | {U['gst_x_W']['value']:.4f} ({U['gst_x_W']['se']:.4f}) | {U['gst_x_B']['value']:.4f} "
          f"({U['gst_x_B']['se']:.4f}) | {U['gst_x_net_e_W']['value']:.4f} ({U['gst_x_net_e_W']['se']:.4f}) | "
          f"{U['gst_x_net_e_B']['value']:.4f} ({U['gst_x_net_e_B']['se']:.4f}) |"]
    for k in models:
        mm = out["models"][k][f"R{RS[-1]}"]
        L.append(f"| {k} | " + " | ".join(f"{np.mean(mm[c]):.4f}" for c in ("gst_x_W", "gst_x_B", "gst_x_net_e_W",
                                                                          "gst_x_net_e_B")) + " |")
    bad = [n for n in out["nesting"] if n["violations"]]
    L += ["", "## Nesting checks (a more general model must not fit worse)", "",
          f"{len(out['nesting'])} pairs x seeds checked; pairs with a violation at some seed:"]
    L += [f"- {n['general']} vs {n['restricted']} (R={n['R']}): mean margin {n['mean']:.1f}, min {n['min']:.1f}, "
          f"{n['violations']} of {len(SEEDS)} seeds" for n in bad] or ["- none"]
    (OUTD / "lattice.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main(sys.argv[1:])
