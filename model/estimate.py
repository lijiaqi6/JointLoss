r"""SMM estimation of the Paper B model (2026-10-18): nested models A-D, sensitivity matrix, standard errors, fit,
counterfactuals. Model and moments: core.py; data: build_data.py (output/data_panel.pkl, data_moments.json).

Criterion Q(theta) = sum_k ((m_k(theta) - m_k^data) / sd_k)^2 with the cluster-bootstrap s.d. of each data moment
(diagonal weighting). Simulation: R = 5 simulated sons per PSID son (the data's race, parental income, schooling and
birth year), common random numbers. Optimiser: CMA-ES (package cma, as in the companion structural code) with
per-parameter scales; models are nested and warm-started (A -> B -> C -> D). Parallel: IGE_WORKERS processes, one
thread each (6 on the shared local machine; cores - 2 on Stanage, with popsize = workers, see hpc_ige.sh). Standard errors: sandwich V = (1 + 1/R) A G'W Omega W G A, A = (G'WG)^{-1}, Omega = bootstrap covariance, G = numerical Jacobian of the moments at the
estimate (central differences). Selection: a race parameter is kept if adding it lowers Q by more than 3.84 (a
heuristic on the scale of a one-restriction test; with diagonal weighting Q differences are not exactly chi-square).
Writes output/estimates.json, output/smm_report.md and a progress log output/smm_progress.log.
"""
import json
import os
import sys
import time
from multiprocessing import Pool
from pathlib import Path

for v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[v] = "1"

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import core  # noqa: E402

INP = HERE / "output"                                             # inputs: data_moments.json, theta_start.json, sons_types.csv
OUTD = Path(os.environ.get("IGE_OUT", str(INP)))                  # outputs (the HPC job sets IGE_OUT to its scratch run folder)
R = int(os.environ.get("IGE_R", 5))                               # simulated sons per PSID son (final lattice: 20)
SEED = 7
WORKERS = int(os.environ.get("IGE_WORKERS", 6))                  # 6 on the shared local machine; the HPC job sets cores - 2
POPSIZE = int(os.environ.get("IGE_POPSIZE", 18))
MAXFEV = {"A": 9000, "B": 4000, "C": 4000, "D": 4000, "E": 8000, "F": 8000, "G": 8000, "H": 8000}
MODELS = os.environ.get("IGE_MODELS", "ABCD")                    # models estimated in this run, in order (warm-started)
START = os.environ.get("IGE_START")                               # "path/estimates.json:D": start from that run's model D;
# several candidates "f1:D,f2:C": the one with the lowest Q (after fixing the first model's restrictions) is used
SET = os.environ.get("IGE_SET")                                   # start-value overrides, e.g. "gx=0.008,dgx=-0.008"
POLISH = int(os.environ.get("IGE_POLISH", 0))                    # evaluations of a second CMA-ES from the best point
if os.environ.get("IGE_MAXFEV"):                                 # e.g. "15000,8000,8000,8000"
    MAXFEV.update(dict(zip("ABCDEFGH", map(int, os.environ["IGE_MAXFEV"].split(",")))))
if os.environ.get("SMM_TEST"):
    MAXFEV = {k: 2 * POPSIZE for k in MAXFEV}
SCALE = dict(dG=0.3, aa=0.2, dlu=0.5, da=0.2, la=0.2, muB=0.2, b0=0.3, bx=0.1, b1=0.03, db1=0.03, lsig0=0.3, a0=0.5, a1=0.3, a2=0.2, a3=0.3, llam_e=0.5,
             llam_u=0.5, muG=0.1, lsigm=0.3, d0B=0.3, d0W=0.3, d1=0.2, gO=0.03, gG=0.03, lrho=0.3, g1=0.005, dg1=0.005,
             du=0.05, lsigeta=0.3, lsigeps=0.3, gx=0.005, dgx=0.005)
G_ = {}


def log(msg):
    with open(OUTD / "smm_progress.log", "a", encoding="utf-8") as f:
        f.write(time.strftime("%H:%M:%S ") + msg + "\n")


MOMENTS = os.environ.get("IGE_MOMENTS", "")                       # "" targets; "ipw" the attrition-weighted set


def setup():
    kid = pd.read_csv(INP / "sons_types.csv", float_precision="round_trip")   # one row per PSID son (build_data.py)
    D = json.load(open(INP / "data_moments.json"))
    if MOMENTS:                              # another moment set: data_moments_<set>.json (moments_set.py)
        tag = "_".join(sorted(core.MOMSET))
        Ds = json.load(open(INP / f"data_moments_{tag}.json"))
        D = dict(Ds, C=Ds["C"] if Ds.get("own_C") else D["C"])      # the clean set has its own terciles and mean
        assert D["names"] == core.MOMENT_NAMES, "moment set and IGE_MOMENTS differ"
    if "ipw" in core.MOMSET:                 # IPW: simulate only the sons in the attrition base
        kid = kid[kid["ipw_base"] == 1].reset_index(drop=True)
    if "clean" in core.MOMSET:               # parental income net of the father's spells (clean_build.py)
        kid = kid.assign(x=kid["x_clean"])
    T = core.Types(kid["black"], kid["x"], kid["e"], kid["byear"], D["C"]["xbar"])
    idx = np.repeat(np.arange(T.n), R)
    Dr = core.Draws(len(idx), SEED)
    return dict(T=T, idx=idx, Dr=Dr, md=np.array(D["m"]), sd=np.array(D["sd"]), C={"terc": tuple(D["C"]["terc"])},
                kid=kid)


def init_worker():
    G_.update(setup())


def sim_moments(th, T=None, idx=None, Dr=None, C=None, ushock=None):
    T = T or G_["T"]
    idx = G_["idx"] if idx is None else idx
    Dr = Dr or G_["Dr"]
    C = C or G_["C"]
    q = core.unpack(np.asarray(th, float))
    P = core.simulate_panel(q, T, idx, Dr)
    return core.moments(P, C), P


def Q_of(th):
    try:
        m, _ = sim_moments(th)
    except Exception:
        return 1e12
    r = (m - G_["md"]) / G_["sd"]
    if not np.all(np.isfinite(r)):
        return 1e12
    return float(np.sum(r ** 2))


def vcov(J, sd):
    """Sandwich covariance of the SMM estimator with the diagonal weights W = diag(1/sd^2):
    (1 + 1/R) (J'WJ)^-1 J'W Omega W J (J'WJ)^-1, Omega = covariance of the 500 cluster-bootstrap draws of the data
    moments (output/boot_moments.npy). Falls back to (1 + 1/R)(J'WJ)^-1 (valid only for optimal weights) without it."""
    W = np.diag(1 / sd ** 2)
    A = np.linalg.inv(J.T @ W @ J)
    f = INP / ("boot_moments.npy" if not MOMENTS else f"boot_moments_{'_'.join(sorted(core.MOMSET))}.npy")
    if not f.exists():
        return (1 + 1 / R) * A, "inverse (no bootstrap draws)"
    Om = np.cov(np.load(f), rowvar=False)
    return (1 + 1 / R) * A @ J.T @ W @ Om @ W @ J @ A, "sandwich"


FIX = set(filter(None, os.environ.get("IGE_FIX", "").split(",")))   # e.g. "muG": fixed at 0 in every model of the run


def free_mask(model):
    return np.array([p not in core.NESTED[model] and p not in FIX for p in core.PARAMS])


def full(th_free, base, mask):
    th = base.copy()
    th[mask] = th_free
    return th


def eval_task(args):
    th = args
    return Q_of(th)


def run_cma(model, th0, pool):
    import cma
    mask = free_mask(model)
    th0 = th0.copy()
    th0[~mask] = 0.0
    x0 = th0[mask]
    stds = np.array([SCALE[p] for p, k in zip(core.PARAMS, mask) if k])
    sig0 = 1.0 if model == "A" else 0.5                         # warm-started models search closer to the start
    sig0 = float(os.environ.get("IGE_SIG0", sig0))               # e.g. 1.0 for a cold start of another model
    es = cma.CMAEvolutionStrategy(x0, sig0, {"CMA_stds": stds, "popsize": POPSIZE, "maxfevals": MAXFEV[model],
                                             "seed": 11, "verbose": -9, "tolfun": 1e-3})
    best, bestq, it = x0, pool.map(eval_task, [full(x0, th0, mask)])[0], 0   # the warm start is a candidate
    while not es.stop():
        X = es.ask()
        qs = pool.map(eval_task, [full(x, th0, mask) for x in X])
        es.tell(X, qs)
        i = int(np.argmin(qs))
        if qs[i] < bestq:
            best, bestq = np.array(X[i]), qs[i]
        it += 1
        if it % 10 == 0:
            log(f"model {model} iter {it} evals {es.countevals} best Q {bestq:.2f}")
    log(f"model {model} done: Q {bestq:.2f} evals {es.countevals} stop {es.stop()}")
    if POLISH:
        es = cma.CMAEvolutionStrategy(best, 0.15, {"CMA_stds": stds, "popsize": POPSIZE, "maxfevals": POLISH,
                                                   "seed": 12, "verbose": -9, "tolfun": 1e-4})
        while not es.stop():
            X = es.ask()
            qs = pool.map(eval_task, [full(x, th0, mask) for x in X])
            es.tell(X, qs)
            i = int(np.argmin(qs))
            if qs[i] < bestq:
                best, bestq = np.array(X[i]), qs[i]
        log(f"model {model} polish done: Q {bestq:.2f} evals {es.countevals} stop {es.stop()}")
    return full(best, th0, mask), bestq


def jacobian(th, pool, mask, h=None):
    """central-difference Jacobian of the moments w.r.t. the free parameters (step = 0.1 x the parameter scale)."""
    names = [p for p, k in zip(core.PARAMS, mask) if k]
    steps = np.array([0.1 * SCALE[p] for p in names])
    tasks = []
    ii = np.where(mask)[0]
    for i, s in zip(ii, steps):
        for sg in (1, -1):
            t = th.copy()
            t[i] += sg * s
            tasks.append(t)
    res = pool.map(mom_task, tasks)
    J = np.column_stack([(res[2 * c] - res[2 * c + 1]) / (2 * steps[c]) for c in range(len(ii))])
    return J, names


def mom_task(th):
    m, _ = sim_moments(th)
    return m


def ige_by_band(P):
    """W-B gap and race IGEs of log wages at 30-34 and 45-49 (the counterfactual objects)."""
    out = {}
    m = core.moments(P, G_["C"])
    d = dict(zip(core.MOMENT_NAMES, m))
    for b in ("3034", "4549"):
        out[f"B_{b}"], out[f"W_{b}"] = d[f"ige_{b}_B"], d[f"ige_{b}_W"]
        out[f"gap_{b}"] = d[f"ige_{b}_W"] - d[f"ige_{b}_B"]
    return out


def counterfactuals(th):
    """run in the main process (G_ filled)."""
    T, idx, Dr = G_["T"], G_["idx"], G_["Dr"]
    res = {}
    q = core.unpack(th)

    def run(qq, TT=T):
        P = core.simulate_panel(qq, TT, idx, Dr)
        return ige_by_band(P)
    res["Baseline"] = run(q)
    # equalising schooling: Black sons' schooling drawn from White sons' at the same parental-income decile
    kid = G_["kid"]
    rng = np.random.default_rng(5)
    dec = pd.qcut(kid["x"], 10, labels=False).to_numpy()
    e_new = kid["e"].to_numpy().copy()
    wh = kid["black"].to_numpy() == 0
    for dcl in range(10):
        pool_e = kid["e"].to_numpy()[wh & (dec == dcl)]
        tgt = (~wh) & (dec == dcl)
        if len(pool_e) and tgt.any():
            e_new[tgt] = rng.choice(pool_e, tgt.sum())
    T2 = core.Types(kid["black"], kid["x"], e_new, kid["byear"], float(kid["x"].mean()))
    res["Equalising schooling"] = run(q, T2)
    for nm_, ch in (("Equal access by race (a3 = 0)", {"a3": 0.0}),
                    ("Equal access by parental income (a1 = 0)", {"a1": 0.0}),
                    ("Equal pay-off of schooling (dg1 = 0)", {"dg1": 0.0}),
                    ("Equal displacement risk (d0B = d0W)", {"d0B": q["d0W"]}),
                    ("Depreciation out of work halved", {"du": q["du"] / 2})):
        qq = dict(q)
        qq.update(ch)
        res[nm_] = run(qq)
    return res


def main():
    OUTD.mkdir(parents=True, exist_ok=True)
    (OUTD / "smm_progress.log").write_text("", encoding="utf-8")
    log(f"steps {sorted(core.STEPS) or 'none'}, fixed at 0 {sorted(FIX) or 'none'}")
    log(f"workers {WORKERS}, popsize {POPSIZE}, maxfevals {MAXFEV}, output {OUTD}")
    G_.update(setup())
    cands = [("theta_start", core.theta_vec(json.load(open(INP / "theta_start.json"))))]
    if START:
        cands = []
        for c in START.split(","):
            f, mdl = c.rsplit(":", 1)
            cands.append((c, core.theta_vec(json.load(open(f))[mdl]["theta"])))
    if SET:
        for kv in SET.split(","):
            k, v = kv.split("=")
            for _, t in cands:
                t[core.PARAMS.index(k)] = float(v)
    names = core.PARAMS
    results = {"steps": sorted(core.STEPS), "fixed": sorted(FIX), "R": R, "start": START, "set": SET,
               "moments": MOMENTS or "targets"}
    with Pool(WORKERS, initializer=init_worker) as pool:
        m0 = free_mask(MODELS[0])
        qc = pool.map(eval_task, [np.where(m0, t, 0.0) for _, t in cands])
        th0 = cands[int(np.argmin(qc))][1]
        log("start candidates: " + "; ".join(f"{c} Q {q:.2f}" for (c, _), q in zip(cands, qc))
            + f" -> {cands[int(np.argmin(qc))][0]}")
        # 1. sensitivity at the starting point (model D, all parameters free)
        J0, nm0 = jacobian(th0, pool, free_mask("D"))
        Js = J0 / G_["sd"][:, None]
        sv = np.linalg.svd(Js, compute_uv=False)
        corr = np.corrcoef(Js.T)
        np.fill_diagonal(corr, 0)
        pairs = sorted([(abs(corr[i, j]), nm0[i], nm0[j]) for i in range(len(nm0)) for j in range(i + 1, len(nm0))],
                       reverse=True)[:8]
        results["sensitivity_start"] = dict(cond=float(sv[0] / sv[-1]), sv_min=float(sv[-1]),
                                            col_norm=dict(zip(nm0, np.linalg.norm(Js, axis=0).tolist())),
                                            top_corr=[(float(a), b, c) for a, b, c in pairs])
        log(f"sensitivity at start: condition number {sv[0] / sv[-1]:.1f}")
        # 2. nested models
        th = th0.copy()
        for model in MODELS:
            th, qv = run_cma(model, th, pool)
            mask = free_mask(model)
            J, nmJ = jacobian(th, pool, mask)
            try:
                V, vkind = vcov(J, G_["sd"])
                se = np.sqrt(np.diag(V))
            except np.linalg.LinAlgError:
                se, vkind = np.full(len(nmJ), np.nan), "singular"
            m, Pm = sim_moments(th)
            results[model] = dict(theta=dict(zip(names, th.tolist())), Q=qv, se=dict(zip(nmJ, se.tolist())),
                                  moments=m.tolist(), vcov=vkind, jacobian=J.tolist(), jac_names=nmJ,
                                  untargeted=core.untargeted(Pm))
            json.dump(results, open(OUTD / "estimates.json", "w"), indent=1)
            log(f"model {model}: Q {qv:.2f}")
    # 3. selection and counterfactuals
    # The model is chosen after the runs, step by step: a race parameter is kept if adding it lowers Q by more than
    # 3.84 at the estimation draws and at two other simulation seeds; a parameter that fails is left out of the later
    # models (2026-10-18: the first ABCD run kept stopping at A because a3 failed, discarding dg1 and db1). Here the
    # counterfactuals use IGE_SELECT or the last model of the run.
    sel = os.environ.get("IGE_SELECT", MODELS[-1])
    results["selected"] = sel
    ths = np.array([results[sel]["theta"][p] for p in names])
    results["counterfactuals"] = counterfactuals(ths)
    json.dump(results, open(OUTD / "estimates.json", "w"), indent=1)
    write_report(results)
    log("ALL DONE")


def write_report(res):
    md, sd = G_["md"], G_["sd"]
    L = ["# Paper B model: SMM estimates", "", "Built by `model/estimate.py` (2026-10-18). Model: "
         "`paperB_age_profile/model_document.tex`. Q = sum of squared t-ratios of the moment deviations (diagonal "
         "weights, cluster-bootstrap s.d.); R = 5 simulated sons per PSID son; s.e. from the numerical Jacobian. "
         f"Selected model: **{res['selected']}** (a race parameter kept if it lowers Q by more than 3.84).", "",
         "## Nested models", "", "| Model | race parameters | Q | number of moments | free parameters |",
         "|---|---|---|---|---|"]
    desc = {"A": "mu_B, delta_0B", "B": "+ a3 (access)", "C": "+ dg1 (pay-off of schooling)", "D": "+ db1 (entry return)",
            "E": "H2 + H3 (no a3)", "F": "H2 only (dg1)", "G": "H3 only (db1)", "H": "H1 + H3 (a3, db1)"}
    mods = [m for m in "ABCDEFGH" if m in res]
    for mdl in mods:
        L.append(f"| {mdl} | {desc[mdl]} | {res[mdl]['Q']:.1f} | {len(md)} | {int(free_mask(mdl).sum())} |")
    L += ["", "## Parameter estimates (s.e.)", "", "| Parameter | " + " | ".join(f"Model {m}" for m in mods) + " |",
          "|---" * (len(mods) + 1) + "|"]
    for p in core.PARAMS:
        cells = []
        for mdl in mods:
            v = res[mdl]["theta"][p]
            s = res[mdl]["se"].get(p)
            cells.append("" if (p in core.NESTED[mdl]) else (f"{v:.4f} ({s:.4f})" if s is not None and np.isfinite(s)
                                                              else f"{v:.4f}"))
        L.append(f"| {p} | " + " | ".join(cells) + " |")
    sel = res["selected"]
    L += ["", f"## Fit of model {sel}", "", "| Moment | data | s.e. | model | t |", "|---|---|---|---|---|"]
    for n, a, s, b in zip(core.MOMENT_NAMES, md, sd, res[sel]["moments"]):
        L.append(f"| {n} | {a:.4f} | {s:.4f} | {b:.4f} | {(b - a) / s:.1f} |")
    L += ["", "## Sensitivity at the starting point", "",
          f"Condition number of the scaled Jacobian: {res['sensitivity_start']['cond']:.1f}. Most collinear parameter "
          "pairs (|corr| of scaled Jacobian columns): " + "; ".join(f"{b}-{c} {a:.2f}" for a, b, c in
                                                                   res["sensitivity_start"]["top_corr"]), ""]
    L += ["## Counterfactuals (selected model; log-wage IGE at 30-34 and 45-49)", "",
          "| Experiment | Black 30-34 | White 30-34 | gap 30-34 | Black 45-49 | White 45-49 | gap 45-49 |",
          "|---|---|---|---|---|---|---|"]
    for k, v in res["counterfactuals"].items():
        L.append(f"| {k} | {v['B_3034']:.3f} | {v['W_3034']:.3f} | {v['gap_3034']:.3f} | {v['B_4549']:.3f} | "
                 f"{v['W_4549']:.3f} | {v['gap_4549']:.3f} |")
    (OUTD / "smm_report.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
