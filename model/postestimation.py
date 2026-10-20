r"""Post-estimation for the selected Paper B model (2026-10-18). Reads output/estimates.json; writes
output/postestimation.json and output/postestimation.md.

1. Standard errors of the counterfactuals: delta method, Var(c) = g' V g with V the sandwich covariance of estimate.vcov (J = Jacobian of the
   66 moments, W = diagonal inverse bootstrap variances) and g = central-difference gradient of the counterfactual change
   in the White - Black IGE gap (same common random numbers at every parameter value).
2. A recession at entry: national unemployment 3 points higher in the first three years after entry, for every son;
   the White - Black IGE gap at 30-34 and 45-49 and the entry wage scar (mean log wage at 25-34 per point), against the
   PSID estimate of paper Section 7 (-0.013** per point of state unemployment at entry), which is not a target.
3. Simulation noise: Q at the estimate with a different seed for the simulation draws.
"""
import json
import os
import sys
from multiprocessing import Pool
from pathlib import Path

for v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[v] = "1"

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy.stats import norm  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import core  # noqa: E402
import estimate as est  # noqa: E402

OUTD = est.OUTD                                                   # the run folder (IGE_OUT) or model/output
SHOCK = np.array([3.0, 3.0, 3.0, 0.0])
CFS = ["Baseline", "Equalising schooling", "Equal access by race (a3 = 0)", "Equal access by parental income (a1 = 0)",
       "Equal pay-off of schooling (dg1 = 0)", "Equal displacement risk (d0B = d0W)", "Depreciation out of work halved",
       "Recession at entry (+3 points, 3 years)", "Equal pay-off of parental income in accumulation (dgx = 0)",
       "No pay-off of parental income in accumulation (gx = dgx = 0)", "Equal job finding out of work (dlu = 0)"]
if os.environ.get("IGE_CFS"):                                     # run only these experiments ("|"-separated names)
    CFS = ["Baseline"] + [c for c in os.environ["IGE_CFS"].split("|") if c in CFS and c != "Baseline"]


def school_types():
    kid = est.G_["kid"]
    rng = np.random.default_rng(5)
    dec = pd.qcut(kid["x"], 10, labels=False).to_numpy()
    e = kid["e"].to_numpy()
    e_new = e.copy()
    wh = kid["black"].to_numpy() == 0
    for d in range(10):
        pool_e = e[wh & (dec == d)]
        tgt = (~wh) & (dec == d)
        if len(pool_e) and tgt.any():
            e_new[tgt] = rng.choice(pool_e, tgt.sum())
    return core.Types(kid["black"], kid["x"], e_new, kid["byear"], float(kid["x"].mean()))


def outcomes(P):
    d = dict(zip(core.MOMENT_NAMES, core.moments(P, est.G_["C"])))
    bands = ("2529", "3034", "3539", "4044", "4549", "5055")
    out = {f"gap_{b}": d[f"ige_{b}_W"] - d[f"ige_{b}_B"] for b in bands}
    out.update({f"{r}_{b}": d[f"ige_{b}_{r}"] for b in bands for r in "BW"})
    a, lw, bl, x = P["age"], P["lw"], P["black"], P["x"]
    c1, c2 = est.G_["C"]["terc"]
    tc = np.where(x <= c1, 1, np.where(x <= c2, 2, 3))
    for r, k in (("B", 1), ("W", 0)):
        s = (a >= 25) & (a <= 34) & np.isfinite(lw) & (bl == k)
        out[f"mlw2534_{r}"] = float(np.mean(lw[s]))
        for lo, hi in ((25, 34), (45, 49)):
            for t in (1, 2, 3):
                z = (a >= lo) & (a <= hi) & np.isfinite(lw) & (bl == k) & (tc == t)
                out[f"mlw{lo}{hi}_t{t}_{r}"] = float(np.mean(lw[z]))
    out.update(core.untargeted(P))                                  # validation statistics, not targets
    return out


def cf_one(args):
    th, name = args
    q = core.unpack(np.asarray(th, float))
    T, idx, Dr = est.G_["T"], est.G_["idx"], est.G_["Dr"]
    if name == "Equalising schooling":
        T = school_types()
    elif name == "Equal access by race (a3 = 0)":
        q["a3"] = 0.0
    elif name == "Equal access by parental income (a1 = 0)":
        q["a1"] = 0.0
    elif name == "Equal pay-off of schooling (dg1 = 0)":
        q["dg1"] = 0.0
    elif name == "Equal displacement risk (d0B = d0W)":
        q["d0B"] = q["d0W"]
    elif name == "Depreciation out of work halved":
        q["du"] = q["du"] / 2
    elif name == "Equal pay-off of parental income in accumulation (dgx = 0)":
        q["dgx"] = 0.0                                              # Black sons get White sons' gx
    elif name == "No pay-off of parental income in accumulation (gx = dgx = 0)":
        q["gx"], q["dgx"] = 0.0, 0.0
    elif name == "Equal job finding out of work (dlu = 0)":
        q["dlu"] = 0.0                                              # Black sons get White sons' search friction out of work
    if name.startswith("Recession"):
        core.ENTRY_SHOCK = SHOCK
    try:
        return outcomes(core.simulate_panel(q, T, idx, Dr))
    finally:
        core.ENTRY_SHOCK = None


def q_seed(args):
    th, seed = args
    Dr = core.Draws(len(est.G_["idx"]), seed)
    m, _ = est.sim_moments(th, Dr=Dr)
    return float(np.sum(((m - est.G_["md"]) / est.G_["sd"]) ** 2))


def stars(p):
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""


def main():
    E = json.load(open(OUTD / "estimates.json"))
    sel = os.environ.get("IGE_SELECT") or E["selected"]
    th = core.theta_vec(E[sel]["theta"])
    mask = est.free_mask(sel)
    names = [p for p, k in zip(core.PARAMS, mask) if k]
    ii = np.where(mask)[0]
    steps = np.array([0.1 * est.SCALE[p] for p in names])
    if "dg1" in core.NESTED[sel]:                                  # experiments on parameters fixed at 0 change nothing
        if "Equal pay-off of schooling (dg1 = 0)" in CFS:
            CFS.remove("Equal pay-off of schooling (dg1 = 0)")
    if "a3" in core.NESTED[sel]:
        if "Equal access by race (a3 = 0)" in CFS:
            CFS.remove("Equal access by race (a3 = 0)")
    if "du" in est.FIX:
        if "Depreciation out of work halved" in CFS:
            CFS.remove("Depreciation out of work halved")
    for c, par in (("Equal pay-off of parental income in accumulation (dgx = 0)", "dgx"),
                   ("No pay-off of parental income in accumulation (gx = dgx = 0)", "gx"),
                   ("Equal job finding out of work (dlu = 0)", "dlu")):
        if c in CFS and (par not in core.PARAMS or par in est.FIX):
            CFS.remove(c)
    est.G_.update(est.setup())
    with Pool(est.WORKERS, initializer=est.init_worker) as pool:
        J, _ = est.jacobian(th, pool, mask)
        V, vkind = est.vcov(J, est.G_["sd"])
        tasks = [(th, c) for c in CFS]
        for i, s in zip(ii, steps):
            for sg in (1, -1):
                t = th.copy()
                t[i] += sg * s
                tasks += [(t, c) for c in CFS]
        res = pool.map(cf_one, tasks)
        qs = pool.map(q_seed, [(th, 8), (th, 9)])
    nc = len(CFS)
    point = dict(zip(CFS, res[:nc]))
    out = {"vcov": vkind, "selected": sel, "Q_estimate": E[sel]["Q"], "Q_other_seeds": qs, "shock": SHOCK.tolist(), "cf": {}}
    keys = list(point["Baseline"])                               # every outcome, with its gradient (Block 5 sensitivity)
    out["grad_names"] = names
    for c_i, c in enumerate(CFS):
        rec = {"level": point[c]}
        for k in keys:
            def chg(r):
                return r[c][k] - r["Baseline"][k]
            grad = []
            for col in range(len(ii)):
                up = dict(zip(CFS, res[nc * (1 + 2 * col): nc * (2 + 2 * col)]))
                dn = dict(zip(CFS, res[nc * (2 + 2 * col): nc * (3 + 2 * col)]))
                grad.append((chg(up) - chg(dn)) / (2 * steps[col]) if c != "Baseline" else
                            (up[c][k] - dn[c][k]) / (2 * steps[col]))
            g = np.array(grad)
            val = point[c][k] - point["Baseline"][k] if c != "Baseline" else point[c][k]
            se = float(np.sqrt(max(g @ V @ g, 0.0)))
            p = float(2 * (1 - norm.cdf(abs(val) / se))) if se > 0 else float("nan")
            rec[k] = dict(value=float(val), se=se, p=p, grad=g.tolist())
        out["cf"][c] = rec
    rc = out["cf"].get("Recession at entry (+3 points, 3 years)")
    out["entry_scar_per_point"] = {r: rc[f"mlw2534_{r}"]["value"] / 3 for r in "BW"} if rc else {"B": float("nan"),
                                                                                              "W": float("nan")}
    json.dump(out, open(OUTD / "postestimation.json", "w"), indent=1)
    L = [f"# Post-estimation, model {sel}", "",
         f"Q at the estimate {E[sel]['Q']:.1f}; at other simulation seeds {qs[0]:.1f}, {qs[1]:.1f}.", "",
         "| Experiment | gap 30-34 (level or change) | p | gap 45-49 | p | mean log wage 25-34 B | W |",
         "|---|---|---|---|---|---|---|"]
    for c, rec in out["cf"].items():
        L.append(f"| {c} | {rec['gap_3034']['value']:.3f}{stars(rec['gap_3034']['p'])} ({rec['gap_3034']['se']:.3f}) | "
                 f"{rec['gap_3034']['p']:.3f} | {rec['gap_4549']['value']:.3f}{stars(rec['gap_4549']['p'])} "
                 f"({rec['gap_4549']['se']:.3f}) | {rec['gap_4549']['p']:.3f} | {rec['mlw2534_B']['value']:.3f} | "
                 f"{rec['mlw2534_W']['value']:.3f} |")
    L += ["", "Entry wage scar per point (recession / 3): Black {:.4f}, White {:.4f}; PSID (paper Section 7) "
          "-0.013** per point of state unemployment at entry.".format(out["entry_scar_per_point"]["B"],
                                                                         out["entry_scar_per_point"]["W"])]
    (OUTD / "postestimation.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
