"""Paper A model: SMM estimation (identification plan Sections 2.4 and 4.2, stages 3-6).

Commands (python IGE/paperA_model/estimate.py <command> [options]):
  evaluate   Q at --start, by block, with the simulated and data moments (results/evaluate_<stamp>/; moments.csv marks
             the moments outside the objective, in_objective = 0)
  jacobian   CRN central-difference Jacobian at --start: S[i, j] = change of moment i in weighted units (sqrt of the
             objective's diagonal weight; 1 / se for --weighting diag) per 10% move of parameter j, two scalings (plan:
             per 10% of the bound range; and per 10% of the value), norms, top block of each column, singular values
             and condition number, loadings of the five weakest directions, near-collinear pairs, over the moments in
             the objective (results/jacobian_<stamp>/)
  run        CMA-ES on the logistic transform theta = lo + (hi - lo) / (1 + exp(-z)) of the free parameters; parallel
             evaluation (own SafePool: a lost or overdue evaluation gets Q = 1e12 and the pool restarts); the search
             state es.pkl, evals.csv, best.json (best evaluation) and mean.json / means.csv (the distribution mean
             es.mean, the better estimate under CRN chatter) are written every generation; --resume <run dir>
             continues a run (also one copied from another machine); --pseudo: pseudo-data recovery (targets = the
             model's moments at --truth with CRN seed --target-seed, start = truth perturbed by --start-noise in z
             units, --pseudo-seed); --cma-stds-from <jacobian.npz>: per-coordinate initial standard deviations
             1 / (weighted Jacobian column norm in z units), median 1; --tolfun; --cma-seed (default: distinct per run,
             recorded in run.json); --perturb: perturb a real-data start like a pseudo start
  polish     Levenberg-Marquardt (Gauss-Newton with Marquardt damping) in the logistic z units: each iteration a CRN
             central-difference Jacobian (jacobian_at, chain rule to z), steps delta = -(G'WG + mu diag(G'WG))^-1 G'W d
             for mu x --lm-mults evaluated in parallel, the best accepted if Q falls (mu moves to it), otherwise mu x 1e4
             and new trial steps (at most --lm-retries times); stops after --iters iterations or when Q falls by less than
             max(--ftol-abs, --ftol-rel x Q) over two iterations. Writes best.json, iterations.csv, evals.csv every
             iteration; at the end the Jacobian at the best point (jacobian.npz, report.md) and the sandwich s.e.
             (se.csv, with --se-reps CRN re-simulations, moments_by_seed.npy). --pseudo as in run (and the recovery
             report at the end)
  se         sandwich standard errors at --start: (G'WG)^-1 G'W Omega W G (G'WG)^-1 with G the central-difference
             Jacobian, Omega = bootstrap covariance of the targets (block-diagonal across sources) + simulation
             covariance of the moments across --se-reps CRN seeds (results/se_<stamp>/)
  noise      Q and the moments at --start under --reps different CRN seeds (parallel): the simulation-noise band of Q
             (memory rule: compare Q only on common draws) and the moments' simulation standard errors
             (results/noise_<stamp>/); --save-noise-input also writes inputs/moment_noise.csv (the diag_noise weights)

Objective: moments.OBJ_EXCLUDE (pooled CPS duplicates, SIPP 'no separation' rows) and --drop ids get zero weight
(kept in the fit tables); --no-default-exclude restores the full vector.
Weighting (--weighting): 'diag_noise' (default) = 1 / (se^2 + var_sim), var_sim = the simulation variance of each moment
at the run's K (--noise-file, default inputs/moment_noise.csv, scaled by K_noise / K); 'diag' = 1 / se^2 of the
bootstrap standard errors in IGE/output/paperA_targets.csv (the within-source bootstrap covariances are used only in
Omega of the sandwich); 'block' = equal total weight per block (robustness run); 'vcov' = inverse of the block-diagonal
bootstrap covariance (diagnostics).
Parameters: the 31 of params.PARAMS plus the optional params.EXTRA_PARAMS (sigma_eps), carried in every theta vector
(32 entries); sigma_eps is fixed at its input value unless --free-extra sigma_eps. --set-fixed name=value changes a
FIXED_DEFAULTS entry (e.g. sigma_eps=0.1); --fix name=value holds an estimated parameter; --tie a=b sets b = a (b not
free; not used by default). A start within 1% of the bound range of a free parameter is refused (--bound-margin).
Extensions of 2026-10-19 (off by default): --new-job on (wife state 'new job', parameter xi_nj), --her-sep on
(separation hazard while she is UI-entitled after her displacement, sigmaJw; --her-sep-tie on: = his sigma_J(r)); their
parameters (params.LATE_PARAMS) follow the extras in every theta vector; their targets (IGE/66,
IGE/output/paperA_targets_ext.csv) enter when the flag is on or with --ext-targets new_job her_sep.
Size: --size (params.SIZES; default params.DEFAULT_SIZE = k_s2_era1_a20: 7 human capital levels, workplace match s = 1,
2 merged, the 1997-2008 schedule in estimation, 20 asset points). With s = 1, 2 merged, pi_c2 does not enter the model
and is held fixed (not free). Inputs (inputs/*.json, the entry couples) are re-read when each process starts.
Outputs contain aggregate moments only (never PSID individual records).

Local runs (8 workers x 2 threads):
  .venv/Scripts/python.exe IGE/paperA_model/estimate.py polish --workers 7 --threads 2 --iters 15
  .venv/Scripts/python.exe IGE/paperA_model/estimate.py run --workers 8 --threads 2 --maxfevals 3500 \
        --start <polish dir>/best.json --cma-stds-from <polish dir>/jacobian.npz --sigma0 0.2 --tolfun 30
  .venv/Scripts/python.exe IGE/paperA_model/estimate.py run --resume IGE/paperA_model/results/runs/<run dir>
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):     # one BLAS thread per process
    os.environ.setdefault(_v, "1")

import argparse                                                                # noqa: E402
import json                                                                    # noqa: E402
import pickle                                                                  # noqa: E402
import sys                                                                     # noqa: E402
import time                                                                    # noqa: E402
import zlib                                                                    # noqa: E402
from datetime import datetime                                                  # noqa: E402
from pathlib import Path                                                       # noqa: E402

import numpy as np                                                             # noqa: E402
import pandas as pd                                                            # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
RESULTS = Path(os.environ.get("PAPERA_OUT", str(HERE / "results")))

from params import (PARAM_NAMES, PARAMS, EXTRA_PARAMS, EXTRA_NAMES, FIXED_DEFAULTS, SIZES, DEFAULT_SIZE,  # noqa: E402
                    Config, bounds, load_start, load_fixed, LATE_PARAMS, LATE_NAMES)

# every theta vector: the 33 parameters, then the extras (sigma_eps), then the parameters of the 2026-10-19 extensions
# (params.LATE_PARAMS; appended last so that the indices of earlier runs' vectors stay valid)
NAMES = PARAM_NAMES + EXTRA_NAMES + LATE_NAMES
_lo, _hi = bounds()
LO = np.concatenate([_lo, [p[1] for p in EXTRA_PARAMS], [p[2] for p in LATE_PARAMS]])
HI = np.concatenate([_hi, [p[2] for p in EXTRA_PARAMS], [p[3] for p in LATE_PARAMS]])
LOST = (1e12, -1, float("nan"), "worker crashed or timed out", None)
TIES: list = []                                      # (index of a, index of b): theta_b = theta_a (--tie a=b)
# Model extensions (PI-approved Fable decisions, 2026-10-18), each behind a flag --<name> on|off; defaults set by the
# step-by-step evidence in results/diagnostics_20261018.md. An extension's parameter (EXT_PARAM) is free when the
# extension is on and held at its nested value when it is off.
EXT_DEFAULTS = {"cps_persist": True, "cps_classif": False, "cs_memory": False, "borrow_wedge": True, "hc_eta": True,
                "new_job": False, "her_sep": False, "her_sep_tie": False}
# Extensions pre-built 2026-10-19 (README 'Extensions 2026-10-19'), off by default: new_job = a wife labor state
# 'employed on a job started less than ~a year ago' with an extra exit hazard xi_nj; her_sep = separation hazard
# sigma_Jw while she is UI-entitled after her own displacement (her_sep_tie on: sigma_Jw = his sigma_J(r)). Their
# targets (IGE/output/paperA_targets_ext.csv, IGE/66) enter only when the extension is on or --ext-targets names it.
EXT_TARGETS = ("new_job", "her_sep")
# CPS entry / exit definitions in the objective: cps_persist on (default since 2026-10-19) = the persistent flows
# (cps_entry_p_*, cps_wife_exit_p; one-month reversals filtered identically in data and model); off = the one-month
# flows (cps_entry_*, cps_wife_exit), with the Poterba-Summers response-error correction if cps_classif is on
CPS_FLOW_IDS = {True: ["cps_entry_p_black", "cps_entry_p_white", "cps_wife_exit_p"],
                False: ["cps_entry_black", "cps_entry_white", "cps_wife_exit"]}
EXT_PARAM = {"cs_memory": ("c_mem", 0.0), "hc_eta": ("eta_up", 0.0), "new_job": ("xi_nj", 0.0),
             "her_sep": ("sigmaJw", 0.0)}
EXT_REPORT_REASON = "reported only (extension check, target = 0 in paperA_targets_ext.csv)"


def vec_dict(x) -> dict:
    return {n: float(v) for n, v in zip(NAMES, x)}


def dict_vec(d: dict) -> np.ndarray:
    """theta dict -> vector; a dict without the 2026-10-19 extension parameters gets their nested values (0)."""
    late = {n: v for n, v in EXT_PARAM.values() if n in LATE_NAMES}
    return np.array([d[n] if (n in d or n not in late) else late[n] for n in NAMES], dtype=float)


def pad_vec(x, fx=None) -> np.ndarray:
    """A theta vector of an earlier run completed: without the extras (PARAMS only) by the extras' fixed values; without
    the 2026-10-19 extension parameters by their nested values (EXT_PARAM)."""
    x = np.asarray(x, float)
    if len(x) == len(NAMES):
        return x
    parts = [x]
    if len(x) == len(PARAM_NAMES):
        fx = fx if fx is not None else load_fixed()
        parts.append([float(fx[n]) for n in EXTRA_NAMES])
    nested = {n: v for n, v in EXT_PARAM.values()}
    parts.append([nested[n] for n in LATE_NAMES])
    out = np.concatenate(parts)
    if len(out) != len(NAMES):
        raise ValueError(f"theta vector of length {len(x)} does not match {len(NAMES)} parameters")
    return out


# ----------------------------------------------------------------------------------------------------------------------
# transforms, ties, bounds
# ----------------------------------------------------------------------------------------------------------------------
def to_z(theta, idx):
    u = np.clip((theta[idx] - LO[idx]) / (HI[idx] - LO[idx]), 1e-6, 1 - 1e-6)
    return np.log(u / (1 - u))


def dtheta_dz(theta, idx):
    u = np.clip((theta[idx] - LO[idx]) / (HI[idx] - LO[idx]), 1e-12, 1 - 1e-12)
    return (HI[idx] - LO[idx]) * u * (1 - u)


def apply_ties(th):
    for a, b in TIES:
        th[b] = th[a]
    return th


def full_theta(z, base, idx):
    th = np.array(base, float).copy()
    th[idx] = LO[idx] + (HI[idx] - LO[idx]) / (1.0 + np.exp(-np.asarray(z)))
    return apply_ties(th)


def setup_ties(pairs):
    TIES.clear()
    for t in pairs or []:
        a, b = t.split("=")
        if a not in NAMES or b not in NAMES or a == b:
            raise SystemExit(f"--tie {t}: both names must be parameters and differ")
        TIES.append((NAMES.index(a), NAMES.index(b)))
    srcs, dsts = {a for a, _ in TIES}, [b for _, b in TIES]
    if srcs & set(dsts) or len(dsts) != len(set(dsts)):
        raise SystemExit(f"--tie {pairs}: chained or repeated ties")


def check_start_bounds(th, idx, margin):
    """Refuse a start within margin x (bound range) of a bound for a free parameter: in logistic units such a start
    (z beyond +-4.6 at 1%) hardly moves under CMA-ES steps, and a start at a bound (z = +-13.8) does not move at all."""
    u = (th[idx] - LO[idx]) / (HI[idx] - LO[idx])
    bad = [(NAMES[j], th[j], LO[j], HI[j], uu) for j, uu in zip(idx, u) if uu < margin or uu > 1 - margin]
    if bad:
        lines = "\n".join(f"  {n}: start {v:.6g}, bounds [{lo:g}, {hi:g}], at {100 * uu:.2f}% of the range"
                          for n, v, lo, hi, uu in bad)
        raise SystemExit(f"START REFUSED: free parameter(s) within {100 * margin:g}% of a bound:\n{lines}\n"
                         f"Hold them with --fix name=value, give another --start, or change the bounds in params.py.")


# ----------------------------------------------------------------------------------------------------------------------
# worker state and one evaluation
# ----------------------------------------------------------------------------------------------------------------------
_W = {}


def borrowing_wedge():
    """Monthly borrowing wedge (borrowing rate - saving rate) from inputs/borrowing_wedge.json (borrowing_wedge.py)."""
    p = HERE / "inputs" / "borrowing_wedge.json"
    if not p.exists():
        raise FileNotFoundError(f"{p} missing: run IGE/paperA_model/borrowing_wedge.py")
    return float(json.loads(p.read_text())["wedge_monthly"])


def targets_for(spec):
    """Targets of a run: the pseudo targets csv, or IGE/60's targets plus the rows of the extensions in
    spec['ext_targets'] (IGE/66), appended in that order."""
    import moments as M
    if spec.get("targets_csv"):
        return pd.read_csv(spec["targets_csv"])
    T = M.load_targets()
    if spec.get("ext_targets"):
        X, _ = M.load_targets_ext(spec["ext_targets"])
        T = pd.concat([T, X], ignore_index=True)
    return T


def make_weights(T, spec):
    import moments as M
    return M.weights(T, spec["weighting"], exclude=spec.get("exclude"), noise_file=spec.get("noise_file"), K=spec["K"])


def _init_worker(spec):
    """spec: dict(size, threads, K, seed, weighting, ctrl_rate, targets_csv (optional pseudo targets), exclude,
    noise_file, set_fixed)."""
    os.environ["NUMBA_NUM_THREADS"] = str(spec["threads"])
    import moments as M
    from simulate import load_entry
    cfg = Config(**SIZES[spec["size"]], threads=spec["threads"])
    T = targets_for(spec)
    fx = load_fixed()
    ext = spec.get("ext") or {}
    fx["r_wedge"] = borrowing_wedge() if ext.get("borrow_wedge") else 0.0
    if ext.get("new_job"):                                      # extensions read by model.Model (absent when off)
        fx["new_job"] = True
    if ext.get("her_sep"):
        fx["her_sep"] = True
        fx["her_sep_tie"] = bool(ext.get("her_sep_tie"))
    fx.update(spec.get("set_fixed") or {})
    _W.update(spec=spec, cfg=cfg, targets=T, W=make_weights(T, spec), M=M, fx=fx,
              classif=M.CPS_CLASSIF_PS86_W2559 if ext.get("cps_classif") else None,
              ext_moments=tuple(spec.get("ext_targets") or ()))
    _W["entry"], _W["entry_src"] = load_entry()


def model_moments(theta_vec, seed=None):
    from simulate import simulate
    M, cfg, spec = _W["M"], _W["cfg"], _W["spec"]
    th = vec_dict(pad_vec(theta_vec, _W["fx"]))
    fx = dict(_W["fx"])
    for n in EXTRA_NAMES:                                       # extras enter the model as fixed inputs
        fx[n] = th.pop(n)
    tim = {}
    res = simulate(th, cfg, _W["entry"], K=spec["K"], seed=spec["seed"] if seed is None else seed, fixed=fx,
                   timing=tim)
    t0 = time.perf_counter()
    md = M.compute(res, theta=th, merge_s12=cfg.merge_s12, ctrl_rate=spec["ctrl_rate"], timing=tim,
                   cps_classif=_W.get("classif"), ext_moments=_W.get("ext_moments"))
    tim["moments"] = time.perf_counter() - t0
    del res
    return M.vector(md, _W["targets"]), tim


def _evaluate(theta_vec, seed=None):
    t0 = time.time()
    try:
        m, tim = model_moments(np.asarray(theta_vec, float), seed=seed)
        q, miss = _W["M"].objective(m, _W["targets"], _W["W"])
    except Exception as exc:                                    # a failed solve must not kill the run
        import traceback
        return 1e12, -1, time.time() - t0, repr(exc) + " " + traceback.format_exc()[-400:].replace("\n", " | "), None
    return q, miss, time.time() - t0, "", m


class SafePool:
    """Crash-tolerant worker pool (the pattern of estimation/smm.py's SafePool, re-implemented: estimation/ is not
    imported because its module sets lifecycle-model environment switches). A lost or overdue evaluation gets
    Q = 1e12 and the pool is restarted. Overdue: the round takes longer than --eval-timeout seconds (first generation),
    then 5 x the longest evaluation so far (at least 10 minutes). warm: one evaluation in the parent first, so that
    numba compiles into the cache once before the workers start (its result is kept in warm_result)."""

    def __init__(self, ctx, workers, spec, timeout, warm=None):
        self.ctx, self.workers, self.spec, self.timeout = ctx, workers, spec, timeout
        self.longest = 0.0
        self.warm_result = None
        if warm is not None:
            _init_worker(spec)
            self.warm_result = _evaluate(warm)
            q, miss, dt, err, _ = self.warm_result
            print(f"warm-up evaluation (compiles before the workers start): Q {q:,.1f}  missing {miss}  {dt:.0f}s {err}",
                  flush=True)
            self.longest = dt if np.isfinite(dt) and not err else 0.0
        self._start()

    def _start(self):
        self.pool = self.ctx.Pool(self.workers, initializer=_init_worker, initargs=(self.spec,))

    def _pids(self):
        return {p.pid for p in self.pool._pool}

    def map(self, thetas, seeds=None):
        seen = self._pids()
        seeds = seeds if seeds is not None else [None] * len(thetas)
        rs = [self.pool.apply_async(_evaluate, (th, sd)) for th, sd in zip(thetas, seeds)]
        per_round = self.timeout if self.longest == 0 else max(600.0, 5.0 * self.longest)
        deadline = time.time() + per_round * -(-len(thetas) // self.workers)
        broken = False
        while True:
            pending = sum(not r.ready() for r in rs)
            if pending == 0:
                break
            now = self._pids()
            seen |= now
            if len(seen - now) >= pending or time.time() > deadline:
                broken = True
                break
            time.sleep(1.0)
        out = [r.get() if r.ready() and r.successful() else LOST for r in rs]
        if broken:
            n = sum(o is LOST for o in out)
            print(f"{n} evaluation(s) lost (worker crashed or timed out); restarting the worker pool", flush=True)
            self.pool.terminate()
            self.pool.join()
            self._start()
        else:
            self.longest = max([self.longest] + [o[2] for o in out if np.isfinite(o[2])])
        return out

    def close(self):
        self.pool.close()
        self.pool.join()


def _pool(args, spec, warm=None):
    from multiprocessing import get_context
    return SafePool(get_context("spawn"), args.workers, spec, args.eval_timeout, warm=warm)


# ----------------------------------------------------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------------------------------------------------
def resolve(args):
    """Objective exclusions, fixed-input changes and ties from the command line (a resumed run takes them from its
    run.json instead)."""
    import moments as M
    ex = [] if args.no_default_exclude else list(M.OBJ_EXCLUDE)
    ex += [d for d in (args.drop or []) if d not in ex]
    args.obj_exclude = ex
    sf = {}
    for f in args.set_fixed or []:
        k, v = f.split("=", 1)
        if k not in FIXED_DEFAULTS:
            raise SystemExit(f"--set-fixed {k}: not a FIXED_DEFAULTS entry")
        sf[k] = json.loads(v)
    args.set_fixed_dict = sf
    setup_ties(args.tie)
    args.ext = {k: (getattr(args, k) == "on") if getattr(args, k, None) is not None else v
                for k, v in EXT_DEFAULTS.items()}
    other = CPS_FLOW_IDS[not args.ext["cps_persist"]]           # the definition not in use: fit table only
    args.obj_exclude += [k for k in other if k not in args.obj_exclude]
    if args.ext.get("her_sep_tie") and not args.ext.get("her_sep"):
        raise SystemExit("--her-sep-tie on needs --her-sep on")
    # extension targets: those of every extension that is on, plus --ext-targets (e.g. the base model on the extended
    # moment set); their reported-only rows are outside the objective
    et = list(getattr(args, "ext_targets", None) or [])
    bad = [e for e in et if e not in EXT_TARGETS]
    if bad:
        raise SystemExit(f"--ext-targets {bad}: choose from {list(EXT_TARGETS)}")
    args.ext_targets = [e for e in EXT_TARGETS if e in et or args.ext.get(e)]
    if args.ext_targets:
        import moments as M
        _, rep_only = M.load_targets_ext(args.ext_targets)
        args.obj_exclude += [k for k in rep_only if k not in args.obj_exclude]


def spec_of(args, targets_csv=None):
    return dict(size=args.size, threads=args.threads, K=args.K, seed=args.seed, weighting=args.weighting,
                ctrl_rate=args.ctrl_rate, targets_csv=targets_csv, exclude=list(args.obj_exclude),
                noise_file=args.noise_file, set_fixed=dict(args.set_fixed_dict), ext=dict(args.ext),
                ext_targets=list(getattr(args, "ext_targets", None) or []))


def objective_info(T, W, args):
    """What run.json / evaluate.json record about the objective."""
    import moments as M
    ro = rep_only_ids(args)
    info = dict(weighting=args.weighting, obj_exclude=list(args.obj_exclude),
                obj_exclude_reasons={k: (EXT_REPORT_REASON if k in ro else
                                         M.OBJ_EXCLUDE.get(k, "CPS flow definition not in use (--cps-persist)"
                                         if k in CPS_FLOW_IDS[True] + CPS_FLOW_IDS[False] else "--drop"))
                                     for k in args.obj_exclude},
                n_in_objective=int((np.diag(W) > 0).sum()), set_fixed=dict(args.set_fixed_dict),
                ties=[f"{NAMES[a]}={NAMES[b]}" for a, b in TIES], ext=dict(args.ext))
    if getattr(args, "ext_targets", None):
        info["ext_targets"] = list(args.ext_targets)
    if args.weighting == "diag_noise":
        p = Path(args.noise_file) if args.noise_file else M.NOISE_INPUT
        _, kn = M.load_sim_noise(p, args.K)
        info.update(noise_file=str(p.name), K_noise=kn)
    info["weight_shares"] = {b: round(float(s), 6) for b, s in M.weight_shares(T, W)["share"].items()}
    return info


def rep_only_ids(args):
    """Reported-only extension moments of this run (target = 0 rows of paperA_targets_ext.csv)."""
    if not getattr(args, "ext_targets", None):
        return set()
    import moments as M
    return set(M.load_targets_ext(args.ext_targets)[1])


def start_theta(args):
    """Start vector (31 parameters + extras): inputs/start_analytic.json (+ overrides) or --start json; the extras from
    the fixed inputs (a --start json that carries them, e.g. a best.json with sigma_eps estimated, wins over the
    inputs; --set-fixed wins over both); then --fix and the ties."""
    th = load_start()
    fx = load_fixed()
    for n in EXTRA_NAMES:
        th[n] = float(fx[n])
    th.update({p[0]: float(p[1]) for p in LATE_PARAMS})        # 2026-10-19 extensions: default starts
    if args.start:
        d = json.loads(Path(args.start).read_text())
        th0 = load_start(None)
        th0.update({n: th[n] for n in EXTRA_NAMES + LATE_NAMES})
        th0.update({k: float(v) for k, v in d.get("theta", d).items() if k in th0})
        th = th0
    for n in EXTRA_NAMES:
        if n in args.set_fixed_dict:
            th[n] = float(args.set_fixed_dict[n])
    for e, (n, v0) in EXT_PARAM.items():                        # extension off: its parameter at the nested value
        if n in th and not args.ext.get(e):
            th[n] = v0
    for f in args.fix or []:
        k, v = f.split("=")
        if k not in th:
            raise SystemExit(f"--fix {k}: unknown parameter")
        th[k] = float(v)
    return apply_ties(dict_vec(th))


def free_index(args):
    fixed = {f.split("=")[0] for f in (args.fix or [])}
    cfg = Config(**SIZES[args.size])
    if cfg.merge_s12:
        fixed.add("pi_c2")                                      # does not enter the model with s = 1, 2 merged
    names = list(args.free) if args.free else list(PARAM_NAMES) + list(LATE_NAMES)   # late: free only when on
    if args.free_set == "closed":
        names = [n for n in CLOSED if n != "p_H"]
    for n in args.free_extra or []:
        if n not in EXTRA_NAMES:
            raise SystemExit(f"--free-extra {n}: not one of {EXTRA_NAMES}")
        if n not in names:
            names.append(n)
    bad = [n for n in names if n not in NAMES]
    if bad:
        raise SystemExit(f"unknown parameters {bad}")
    fixed |= {NAMES[b] for _, b in TIES}                        # a tied parameter follows its source
    fixed |= {n for e, (n, _v) in EXT_PARAM.items() if not args.ext.get(e)}
    if args.ext.get("her_sep_tie"):
        fixed.add("sigmaJw")                                    # her term = his sigma_J(r)
    free = [n for n in names if n not in fixed]
    return np.array([NAMES.index(n) for n in free], dtype=int), free


# parameters with closed-form start values (plan Sections 1.4-1.5): displacement (9), sigma_0, sigma_J, pi_up, pi_dn,
# d, lambda_h (2 each) = 21; in the closed-form recovery p_H is held at the truth (ridge point: only kappa has a closed
# form) and pi_c2 drops when s = 1, 2 are merged, so 19 are free at the default size
CLOSED = ["delta_w_B", "delta_w_W", "delta_h_B", "delta_h_W", "pi_c0", "pi_c1", "pi_c2", "p_H", "m_H",
          "sigma0_B", "sigma0_W", "sigmaJ_B", "sigmaJ_W", "pi_up_w", "pi_up_h", "pi_dn_w", "pi_dn_h", "d_w", "d_h",
          "lam_h_B", "lam_h_W"]


def stamp():
    job = os.environ.get("SLURM_JOB_ID")
    return f"{datetime.now():%Y%m%d_%H%M%S}" + (f"_j{job}" if job else f"_p{os.getpid()}")   # pid: parallel local runs


def block_table(m, T, W):
    d = m - T["value"].to_numpy(float)
    w = np.diag(W)
    q = np.where(np.isfinite(d), d * d * w, np.nan)
    return pd.DataFrame({"block": T["block"], "q": q, "in_obj": w > 0}).groupby("block", sort=False).agg(
        sum=("q", "sum"), size=("q", "size"), in_objective=("in_obj", "sum"))


def run_dir_file(out):
    if os.environ.get("PAPERA_RUN_DIR_FILE"):
        Path(os.environ["PAPERA_RUN_DIR_FILE"]).write_text(str(out))


def prepare_pseudo(args, base, out):
    """Pseudo-data recovery: truth (= the start, or --truth), targets = the model's moments at the truth under CRN seed
    --target-seed. Returns (base, truth, targets_csv)."""
    truth = base.copy()
    if args.truth:
        d = json.loads(Path(args.truth).read_text())
        tt = vec_dict(truth)
        tt.update({k: float(v) for k, v in d.get("theta", d).items() if k in tt})
        truth = apply_ties(dict_vec(tt))
    return truth.copy(), truth, str(pseudo_targets(args, truth, out))


def start_z(args, base, idx):
    check_start_bounds(base, idx, args.bound_margin)
    z0 = to_z(base, idx)
    if args.pseudo or args.perturb:
        z0 = z0 + np.random.default_rng(args.pseudo_seed).normal(0.0, args.start_noise, len(z0))
    return z0


def eval_logger(out, new):
    log_path = out / "evals.csv"
    fresh = new or not log_path.exists()
    logf = open(log_path, "a", buffering=1)
    if fresh:
        logf.write("eval,gen,Q,missing,seconds,error," + ",".join(NAMES) + "\n")
    return logf


def log_evals(logf, counter, gen, thetas, res):
    for th, (q, miss, dt, err, _m) in zip(thetas, res):
        counter += 1
        logf.write(f"{counter},{gen},{q},{miss},{dt:.1f},{err[:300].replace(',', ';')},"
                   + ",".join(f"{v:.8g}" for v in th) + "\n")
    return counter


def best_record(q, miss, th, m, **kw):
    return dict(Q=q, missing=miss, **kw, theta=vec_dict(th),
                moments=None if m is None else dict(zip(_W["targets"]["id"] if "targets" in _W else [], map(float, m))))


# ----------------------------------------------------------------------------------------------------------------------
# commands
# ----------------------------------------------------------------------------------------------------------------------
def cmd_evaluate(args):
    import moments as M
    spec = spec_of(args)
    _init_worker(spec)
    th = start_theta(args)
    t0 = time.time()
    m, tim = model_moments(th)
    q, miss = M.objective(m, _W["targets"], _W["W"])
    dt = time.time() - t0
    T = _W["targets"]
    w = np.diag(_W["W"])
    out = RESULTS / f"evaluate_{stamp()}"
    out.mkdir(parents=True, exist_ok=True)
    tab = T[["id", "block", "value", "se"]].assign(sim=m, z=(m - T["value"]) / T["se"], in_objective=(w > 0).astype(int),
                                                     weight=w, q=np.where(w > 0, (m - T["value"]) ** 2 * w, 0.0))
    ro = rep_only_ids(args)
    tab["note"] = [(EXT_REPORT_REASON if k in ro else M.OBJ_EXCLUDE.get(k, "CPS flow definition not in use" if k in
                    CPS_FLOW_IDS[True] + CPS_FLOW_IDS[False] else "--drop")) if not ok else ""
                   for k, ok in zip(T["id"], w > 0)]
    tab.to_csv(out / "moments.csv", index=False)
    bt = block_table(m, T, _W["W"])
    bt.to_csv(out / "q_by_block.csv")
    info = dict(Q=q, missing=miss, seconds=dt, timing=tim, size=args.size, K=args.K, seed=args.seed,
                entry_source=Path(_W["entry_src"]).name if os.path.exists(str(_W["entry_src"])) else _W["entry_src"],
                theta=vec_dict(th), **objective_info(T, _W["W"], args))
    (out / "evaluate.json").write_text(json.dumps(info, indent=1, default=float))
    pd.set_option("display.width", 220)
    pd.set_option("display.max_rows", 300)
    print(tab.drop(columns=["note"]).to_string())
    print(bt.to_string())
    print("weight shares by block:", json.dumps(info["weight_shares"]))
    print(f"Q(start) = {q:,.1f}  (missing {miss}; {info['n_in_objective']} moments in the objective, weighting "
          f"{args.weighting})  {dt:.0f}s  timing {json.dumps({k: round(v, 1) for k, v in tim.items()})}")
    print(f"-> {out}")


def jacobian_at(args, th, idx, pool):
    """Central differences with CRN: step h_j (args.step 'value': 5% of |theta_j|, at least 1% of the range if theta_j
    is near 0; 'range': 5% of the bound range, the plan's protocol), clipped inside the bounds; tied parameters follow
    their source. Returns m0, dM/dtheta (n_mom x len(idx)), the steps actually used, Q at th."""
    rng_ = HI - LO
    hs = np.where(args.step == "range", 0.05 * rng_, np.maximum(0.05 * np.abs(th), 0.01 * rng_))
    thetas, steps = [th.copy()], []
    for j in idx:
        h = hs[j]
        up = min(th[j] + h, HI[j])
        dn = max(th[j] - h, LO[j])
        a, b = th.copy(), th.copy()
        a[j], b[j] = up, dn
        thetas += [apply_ties(a), apply_ties(b)]
        steps.append(up - dn)
    res = pool.map(thetas)
    bad = [k for k, r in enumerate(res) if r[4] is None]
    if bad:
        print(f"WARNING {len(bad)} failed evaluations in the Jacobian: {[res[k][3][:200] for k in bad[:3]]}")
    m0 = res[0][4]
    G = np.column_stack([(res[1 + 2 * q][4] - res[2 + 2 * q][4]) / steps[q] if res[1 + 2 * q][4] is not None and
                         res[2 + 2 * q][4] is not None else np.full(len(m0), np.nan) for q in range(len(idx))])
    jacobian_at.last = (thetas, res)
    return m0, G, np.array(steps), res[0][0]


def save_jacobian(path, G, m0, th, idx, steps, free):
    np.savez(path, G=G, m0=m0, theta=th, idx=idx, steps=steps, names=np.array(free),
             Gz=G * dtheta_dz(th, idx)[None, :])


def cmd_jacobian(args):
    spec = spec_of(args)
    th = start_theta(args)
    idx, free = free_index(args)
    out = RESULTS / f"jacobian_{stamp()}"
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    pool = _pool(args, spec, warm=th)
    try:
        m0, G, steps, q0 = jacobian_at(args, th, idx, pool)
    finally:
        pool.close()
    T, W = _W["targets"], _W["W"]
    save_jacobian(out / "jacobian.npz", G, m0, th, idx, steps, free)
    report = jacobian_report(G, T, th, idx, free, m0, W=W)
    report["Q_start"] = q0
    report["minutes"] = (time.time() - t0) / 60
    report["objective"] = objective_info(T, W, args)
    (out / "report.json").write_text(json.dumps(report, indent=1, default=float))
    (out / "report.md").write_text(report["md"])
    print(report["md"])
    print(f"-> {out}")


def _svd_summary(S, free):
    U_, s, Vt = np.linalg.svd(S, full_matrices=False)
    cond = float(s[0] / s[-1]) if s[-1] > 0 else float("inf")
    weak = []
    for k in range(1, min(5, len(s)) + 1):
        v = Vt[-k]
        order = np.argsort(-np.abs(v))[:4]
        weak.append(dict(sv=float(s[-k]), loadings={free[o]: round(float(v[o]), 3) for o in order}))
    return s, cond, weak


def jacobian_report(G, T, th, idx, free, m0=None, W=None):
    """Sensitivities in weighted units: rows scaled by sqrt(w_i) (w = the objective's diagonal weight; 1 / se when W is
    None) over the moments in the objective with a finite row."""
    se = T["se"].to_numpy(float)
    blocks = T["block"].to_numpy()
    rng_ = (HI - LO)[idx]
    sw = 1.0 / se if W is None else np.sqrt(np.diag(W))
    ok = np.isfinite(G).all(axis=1) & (sw > 0)
    S_rng = G[ok] * (0.1 * rng_)[None, :] * sw[ok, None]          # per 10% of the bound range (plan)
    S_val = G[ok] * np.where(th[idx] != 0, 0.1 * np.abs(th[idx]), 0.1 * rng_)[None, :] * sw[ok, None]
    S_z = G[ok] * dtheta_dz(th, idx)[None, :] * sw[ok, None]       # per unit of z (the optimisers' coordinates)
    bl = blocks[ok]
    rows = []
    for q, nm in enumerate(free):
        col = S_val[:, q]
        ss = pd.Series(col ** 2).groupby(bl).sum()
        top = ss.idxmax() if ss.sum() > 0 else ""
        rows.append(dict(param=nm, theta=th[idx[q]], norm_range=float(np.linalg.norm(S_rng[:, q])),
                         norm_value=float(np.linalg.norm(col)), norm_z=float(np.linalg.norm(S_z[:, q])), top_block=top,
                         top_share=float(ss.max() / ss.sum()) if ss.sum() > 0 else 0.0))
    tab = pd.DataFrame(rows)
    s, cond, weak = _svd_summary(S_val, free)
    s_r, cond_r, weak_r = _svd_summary(S_rng, free)
    Cn = S_val / np.maximum(np.linalg.norm(S_val, axis=0), 1e-300)
    corr = Cn.T @ Cn
    pairs = [(free[a], free[b], float(corr[a, b])) for a in range(len(free)) for b in range(a + 1, len(free))
             if abs(corr[a, b]) > 0.9]
    unit = "1 / se" if W is None else "sqrt of the objective weight"
    md = ["# Jacobian", "",
          f"S = change of each moment in weighted units ({unit}) per 10% move of a parameter (value scaling: 10% of "
          f"|theta|; range scaling: 10% of the bound range, the plan's protocol; z: per unit of the logistic "
          f"coordinate). Moments in the objective with finite rows: {int(ok.sum())} of {len(ok)}.", "",
          "| parameter | theta | norm (10% of value) | norm (10% of range) | norm (per z) | top block | share |",
          "|---|---:|---:|---:|---:|---|---:|"]
    for r in rows:
        md.append(f"| {r['param']} | {r['theta']:.4g} | {r['norm_value']:.2f} | {r['norm_range']:.2f} | "
                  f"{r['norm_z']:.2f} | {r['top_block']} | {r['top_share']:.2f} |")
    md += ["", f"Singular values (value scaling): {', '.join(f'{x:.3g}' for x in s)}",
           f"Condition number (value scaling): {cond:.3g}; (range scaling): {cond_r:.3g}",
           "", "Weakest directions, value scaling (smallest singular values, largest loadings):"]
    md += [f"- sv {w['sv']:.3g}: {w['loadings']}" for w in weak]
    md += ["", "Weakest directions, range scaling:"] + [f"- sv {w['sv']:.3g}: {w['loadings']}" for w in weak_r]
    md += ["", "Near-collinear pairs (|corr| of columns > 0.9):"] + [f"- {a} / {b}: {c:+.3f}" for a, b, c in pairs] + \
        (["- none"] if not pairs else [])
    weak_norm = tab[tab["norm_value"] < 3]["param"].tolist()
    md += ["", f"Parameters with norm < 3 (value scaling): {weak_norm if weak_norm else 'none'}"]
    return dict(table=rows, singular_values=s.tolist(), condition=cond, condition_range=cond_r, weak=weak,
                weak_range=weak_r, pairs=pairs, weak_norm=weak_norm, md="\n".join(md))


def pseudo_targets(args, truth, out):
    """Targets = the model's moments at truth under CRN seed --target-seed (se unchanged, i.e. the data weights)."""
    import moments as M
    spec = spec_of(args)
    spec_t = dict(spec, seed=args.target_seed)
    _init_worker(spec_t)
    m, _ = model_moments(truth)
    T = targets_for(spec).copy()
    T["data_value"] = T["value"]
    T["value"] = m
    p = out / "pseudo_targets.csv"
    T.to_csv(p, index=False)
    return p


def cma_stds_from(path, idx, W, T):
    """Per-coordinate initial standard deviations for CMA-ES: 1 / (column norm of the weighted Jacobian in z units),
    normalised to a median of 1 over the parameters found in the file, clipped to [0.05, 20]; 1 for parameters that
    are not in the file."""
    J = np.load(path, allow_pickle=True)
    G, jidx = J["G"], [int(i) for i in J["idx"]]
    th = pad_vec(J["theta"])
    w = np.diag(W)
    ok = np.isfinite(G).all(axis=1) & (w > 0)
    Gz = G[ok] * dtheta_dz(th, np.array(jidx))[None, :] * np.sqrt(w[ok])[:, None]
    nrm = dict(zip(jidx, np.linalg.norm(Gz, axis=0)))
    raw = np.array([1.0 / nrm[j] if nrm.get(j, 0) > 0 else np.nan for j in idx])
    found = np.isfinite(raw)
    if not found.any():
        raise SystemExit(f"--cma-stds-from {path}: no free parameter in the file")
    stds = np.ones(len(idx))
    stds[found] = np.clip(raw[found] / np.median(raw[found]), 0.05, 20.0)
    return stds


def cmd_run(args):
    import cma
    if args.resume:
        out = Path(args.resume)
        run = json.loads((out / "run.json").read_text())
        es = pickle.loads((out / "es.pkl").read_bytes())
        for k in ("size", "K", "seed", "weighting", "ctrl_rate"):
            setattr(args, k, run[k])
        args.obj_exclude = run.get("obj_exclude", [])               # runs before 2026-10-18 evening: full vector
        args.noise_file = run.get("noise_file_arg", None)
        args.set_fixed_dict = run.get("set_fixed_dict", {})
        args.ext = run.get("ext", {k: False for k in EXT_DEFAULTS})
        args.ext_targets = run.get("ext_targets", [])
        setup_ties(run.get("tie") or [])
        base = pad_vec(run["theta_base"], {**load_fixed(), **args.set_fixed_dict})
        idx = np.array(run["idx"])
        targets_csv = run.get("targets_csv")
        if args.extend_to:
            es.opts["maxfevals"] = args.extend_to
            es.stop(check_in_same_iteration=True)
        print(f"resuming {out} at {es.countevals} evaluations", flush=True)
    else:
        base = start_theta(args)
        idx, free = free_index(args)
        tag = "recovery_" if args.pseudo else "smm_"
        out = RESULTS / "runs" / f"{tag}{args.label + '_' if args.label else ''}{stamp()}"
        out.mkdir(parents=True, exist_ok=True)
        run_dir_file(out)
        targets_csv, truth = None, None
        if args.pseudo:
            base, truth, targets_csv = prepare_pseudo(args, base, out)
        z0 = start_z(args, base, idx)
        if args.cma_seed is None:                                   # distinct per run, recorded in run.json
            args.cma_seed = zlib.crc32(f"{args.label}|{time.time_ns()}|{os.getpid()}".encode()) % 2_000_000_000 + 1
        opts = {"popsize": args.popsize, "maxfevals": args.maxfevals, "seed": args.cma_seed, "verbose": -9}
        stds = None
        if args.cma_stds_from:
            import moments as M
            T0 = targets_for(spec_of(args, targets_csv))
            stds = cma_stds_from(args.cma_stds_from, idx, make_weights(T0, spec_of(args, targets_csv)), T0)
            opts["CMA_stds"] = stds.tolist()
        if args.tolfun:
            opts["tolfun"] = args.tolfun
            opts["tolfunhist"] = args.tolfun
        es = cma.CMAEvolutionStrategy(z0, args.sigma0, opts)
        run = dict(vars(args), names=NAMES, lo=LO.tolist(), hi=HI.tolist(), free=[NAMES[i] for i in idx],
                   idx=[int(i) for i in idx], theta_base=base.tolist(), theta_start=full_theta(z0, base, idx).tolist(),
                   truth=None if truth is None else truth.tolist(), targets_csv=targets_csv,
                   noise_file_arg=args.noise_file, cma_stds=None if stds is None else dict(zip(free, stds.tolist())),
                   started=datetime.now().isoformat())
        _init_worker(spec_of(args, targets_csv))
        run.update(objective_info(_W["targets"], _W["W"], args))
        (out / "run.json").write_text(json.dumps(run, indent=1, default=str))
        print(f"{len(idx)} free parameters, CMA seed {args.cma_seed} -> {out}", flush=True)
        print("weight shares by block:", json.dumps(run["weight_shares"]), flush=True)
    spec = spec_of(args, targets_csv)
    new_log = not (out / "evals.csv").exists()
    logf = eval_logger(out, new_log)
    best = json.loads((out / "best.json").read_text()) if (out / "best.json").exists() else {"Q": float("inf")}
    genlog = open(out / "generations.csv", "a", buffering=1)
    if new_log:
        genlog.write("gen,evals,best_Q,gen_min_Q,gen_median_Q,sigma,minutes\n")
    meanlog_new = not (out / "means.csv").exists()
    meanlog = open(out / "means.csv", "a", buffering=1)
    if meanlog_new:
        meanlog.write("gen,evals,sigma," + ",".join(NAMES) + "\n")
    t_start = time.time()
    pool = _pool(args, spec, warm=full_theta(es.mean, base, idx))
    try:
        while not es.stop():
            Z = es.ask()
            thetas = [full_theta(z, base, idx) for z in Z]
            res = pool.map(thetas)
            es.tell(Z, [r[0] for r in res])
            log_evals(logf, es.countevals - len(Z), es.countiter, thetas, res)
            for th, (q, miss, dt, err, m) in zip(thetas, res):
                if q < best["Q"]:
                    best = best_record(q, miss, th, m, eval=es.countevals, gen=es.countiter)
                    (out / "best.json").write_text(json.dumps(best, indent=1, default=float))
            th_mean = full_theta(es.mean, base, idx)
            (out / "mean.json").write_text(json.dumps(dict(gen=es.countiter, evals=es.countevals, sigma=es.sigma,
                                                           theta=vec_dict(th_mean)), indent=1, default=float))
            meanlog.write(f"{es.countiter},{es.countevals},{es.sigma:.6g}," + ",".join(f"{v:.8g}" for v in th_mean)
                          + "\n")
            (out / "es.pkl").write_bytes(pickle.dumps(es))
            qs = [r[0] for r in res]
            genlog.write(f"{es.countiter},{es.countevals},{best['Q']:.6g},{min(qs):.6g},{np.median(qs):.6g},"
                         f"{es.sigma:.4g},{(time.time() - t_start) / 60:.1f}\n")
            print(f"gen {es.countiter:4d}  evals {es.countevals:5d}  best Q {best['Q']:,.2f}  gen median "
                  f"{np.median(qs):,.1f}  sigma {es.sigma:.3f}  {(time.time() - t_start) / 60:.0f} min", flush=True)
        # Q at the final distribution mean (one evaluation)
        th_mean = full_theta(es.mean, base, idx)
        q, miss, dt, err, m = pool.map([th_mean])[0]
        (out / "mean.json").write_text(json.dumps(dict(best_record(q, miss, th_mean, m), gen=es.countiter,
                                                       evals=es.countevals, sigma=es.sigma, final=True),
                                                  indent=1, default=float))
        print(f"Q at the final distribution mean {q:,.2f}", flush=True)
    finally:
        pool.close()
    print("stop:", es.stop())
    print("best Q", best["Q"])


def sandwich(G, T, W, Vsim):
    """(G'WG)^-1 G'W Omega W G (G'WG)^-1, Omega = bootstrap covariance (block-diagonal across sources) + Vsim, over the
    moments in the objective with finite rows. Returns the total and the simulation-noise-only covariance."""
    import moments as M
    Vdat = M.load_vcov(T["id"])
    dv = np.diag(Vdat).copy()
    dv[dv <= 0] = T["se"].to_numpy(float)[dv <= 0] ** 2
    Vdat[np.diag_indices_from(Vdat)] = dv
    ok = np.isfinite(G).all(axis=1) & np.isfinite(Vsim).all(axis=1) & (np.diag(W) > 0)
    Gk, Wk = G[ok], W[np.ix_(ok, ok)]
    Om = (Vdat + Vsim)[np.ix_(ok, ok)]
    A = np.linalg.pinv(Gk.T @ Wk @ Gk)
    V = A @ Gk.T @ Wk @ Om @ Wk @ Gk @ A
    Vn = A @ Gk.T @ Wk @ Vsim[np.ix_(ok, ok)] @ Wk @ Gk @ A
    return V, Vn, Vdat


def se_block(args, th, idx, free, pool, G, out):
    """Simulation covariance from --se-reps CRN seeds (parallel), the sandwich, se.csv, moments_by_seed.npy and
    q_by_seed.csv (Q at the run's targets for each seed)."""
    seeds = [args.seed + 1000 + r for r in range(args.se_reps)]
    res = pool.map([th] * len(seeds), seeds=seeds)
    S = np.array([r[4] for r in res if r[4] is not None])
    T, W = _W["targets"], _W["W"]
    Vsim = np.cov(S.T)
    V, Vn, Vdat = sandwich(G, T, W, Vsim)
    tab = pd.DataFrame(dict(param=free, estimate=th[idx], se=np.sqrt(np.maximum(np.diag(V), 0)),
                            se_sim_noise=np.sqrt(np.maximum(np.diag(Vn), 0))))
    tab.to_csv(out / "se.csv", index=False)
    np.savez(out / "se_inputs.npz", G=G, Vsim=Vsim, Vdat=Vdat, theta=th, idx=idx)
    np.save(out / "moments_by_seed.npy", S)
    pd.DataFrame(dict(seed=[sd for sd, r in zip(seeds, res) if r[4] is not None],
                      Q=[r[0] for r in res if r[4] is not None])).to_csv(out / "q_by_seed.csv", index=False)
    return tab


def cmd_se(args):
    spec = spec_of(args)
    th = start_theta(args)
    idx, free = free_index(args)
    out = RESULTS / f"se_{stamp()}"
    out.mkdir(parents=True, exist_ok=True)
    pool = _pool(args, spec, warm=th)
    try:
        m0, G, steps, q0 = jacobian_at(args, th, idx, pool)
        tab = se_block(args, th, idx, free, pool, G, out)
    finally:
        pool.close()
    print(tab.to_string())
    print(f"-> {out}")


def lm_iterate(z, q_cur, m_cur, jac, batch, tv, Wm, mults, mu0=0.01, iters=15, retries=2, max_step=3.0, z_cap=9.0,
               ftol_abs=1.0, ftol_rel=1e-3, xtol=1e-4, on_jac=None, on_accept=None, on_iter=None, log=print):
    """Levenberg-Marquardt on Q(z) = d' W d, d = m(z) - tv, with an expensive Jacobian.
    jac(z) -> (m0, Gz): moments and dm/dz at z (Gz columns may be NaN: no step in that coordinate);
    batch(list of z) -> list of (Q, m) (m None if the evaluation failed);
    each iteration: trial steps dz(mu x mult) = -(A + mu mult diag(A))^-1 g, A = Gz'WGz, g = Gz'W d, capped at max_step
    in max-abs and |z| <= z_cap, evaluated together; the best is accepted if Q falls (mu moves to it), else mu x 1e4 and
    new trials (at most retries more times). Stops after iters iterations, when Q falls by less than
    max(ftol_abs, ftol_rel Q) over two iterations, when the accepted step is below xtol, or without descent.
    Returns dict(z, Q, m, mu, iters, stop, z_jac) (z_jac: z of the last Jacobian)."""
    w_in = np.diag(Wm) > 0
    mu, q_hist, z_jac = mu0, [q_cur], None
    stop, it = f"{iters} iterations", 0
    for it in range(1, iters + 1):
        m0, Gz = jac(z)
        z_jac = z.copy()
        if on_jac is not None:
            on_jac(it, z)
        okc = np.isfinite(Gz).all(axis=0)
        rows = w_in & np.isfinite(m0) & np.isfinite(tv) & np.isfinite(Gz[:, okc]).all(axis=1)
        r = (m0 - tv)[rows]
        Gk = Gz[np.ix_(rows, okc)]
        Wk = Wm[np.ix_(rows, rows)]
        A = Gk.T @ Wk @ Gk
        g = Gk.T @ Wk @ r
        Dg = np.maximum(np.diag(A), 1e-12 * max(float(np.diag(A).max()), 1e-300))
        try:
            cond_A = float(np.linalg.cond(A))
        except np.linalg.LinAlgError:
            cond_A = float("inf")
        q_before, accepted, dz_acc = q_cur, False, None
        for attempt in range(retries + 1):
            Zt, mus = [], []
            for mm in mults:
                dz = np.zeros(len(z))
                M_ = A + mu * mm * np.diag(Dg)
                try:
                    dz[okc] = -np.linalg.solve(M_, g)
                except np.linalg.LinAlgError:
                    dz[okc] = -np.linalg.lstsq(M_, g, rcond=None)[0]
                big = np.abs(dz).max()
                if big > max_step:
                    dz *= max_step / big
                Zt.append(np.clip(z + dz, -z_cap, z_cap))
                mus.append(mu * mm)
            res = batch(Zt)
            qs = np.array([rr[0] for rr in res])
            k = int(np.argmin(qs))
            if qs[k] < q_cur:
                dz_acc = Zt[k] - z
                z, q_cur, m_cur, mu = Zt[k], float(qs[k]), res[k][1], mus[k]
                accepted = True
                if on_accept is not None:
                    on_accept(it, z, q_cur, m_cur, mu, float(mults[k]), float(np.abs(dz_acc).max()), cond_A, q_before)
                break
            log(f"  iter {it} attempt {attempt}: no trial lowered Q (best {qs[k]:,.4g} vs {q_cur:,.4g}); "
                f"mu {mu:.3g} -> {mu * 1e4:.3g}")
            mu *= 1e4
        if on_iter is not None:
            on_iter(it, q_before, q_cur, mu, cond_A, accepted)
        if not accepted:
            stop = f"no descent after {retries + 1} attempts at iteration {it}"
            break
        q_hist.append(q_cur)
        if len(q_hist) >= 3 and q_hist[-3] - q_cur < max(ftol_abs, ftol_rel * q_cur):
            stop = f"Q fell by {q_hist[-3] - q_cur:.3g} over two iterations (iteration {it})"
            break
        if np.abs(dz_acc).max() < xtol:
            stop = f"step below {xtol} in z (iteration {it})"
            break
    return dict(z=z, Q=q_cur, m=m_cur, mu=mu, iters=it, stop=stop, z_jac=z_jac)


def cmd_polish(args):
    """Levenberg-Marquardt in z units (see the module docstring and lm_iterate)."""
    base = start_theta(args)
    idx, free = free_index(args)
    tag = "recovery_gn_" if args.pseudo else "polish_"
    out = RESULTS / "runs" / f"{tag}{args.label + '_' if args.label else ''}{stamp()}"
    out.mkdir(parents=True, exist_ok=True)
    run_dir_file(out)
    targets_csv, truth = None, None
    if args.pseudo:
        base, truth, targets_csv = prepare_pseudo(args, base, out)
    z = start_z(args, base, idx)
    spec = spec_of(args, targets_csv)
    _init_worker(spec)
    T, Wm = _W["targets"], _W["W"]
    tv = T["value"].to_numpy(float)
    mults = np.array(args.lm_mults if args.lm_mults else
                     ([1e-3, 1e-2, 1e-1, 1.0, 10.0, 1e2, 1e3] if args.workers >= 7 else [0.1, 1.0, 10.0]), float)
    run = dict(vars(args), command="polish", names=NAMES, lo=LO.tolist(), hi=HI.tolist(), free=free,
               idx=[int(i) for i in idx], theta_base=base.tolist(), theta_start=full_theta(z, base, idx).tolist(),
               truth=None if truth is None else truth.tolist(), targets_csv=targets_csv, noise_file_arg=args.noise_file,
               lm_mults_used=mults.tolist(), started=datetime.now().isoformat(), **objective_info(T, Wm, args))
    (out / "run.json").write_text(json.dumps(run, indent=1, default=str))
    print(f"polish: {len(idx)} free parameters, LM multipliers {mults.tolist()} -> {out}", flush=True)
    print("weight shares by block:", json.dumps(run["weight_shares"]), flush=True)
    logf = eval_logger(out, True)
    itlog = open(out / "iterations.csv", "w", buffering=1)
    itlog.write("iter,evals,Q_before,Q_after,accepted,mu,mult,max_abs_dz,cond_A,minutes," + ",".join(NAMES) + "\n")
    t0 = time.time()
    th0 = full_theta(z, base, idx)
    pool = _pool(args, spec, warm=th0)
    st = dict(nev=0, G=None, m0=None, it=0, z=z)

    def jac(zz):
        th_c = full_theta(zz, base, idx)
        m0, G, steps, _q = jacobian_at(args, th_c, idx, pool)
        st["nev"] = log_evals(logf, st["nev"], st["it"] + 1, *jacobian_at.last)
        save_jacobian(out / "jacobian.npz", G, m0, th_c, idx, steps, free)
        st.update(G=G, m0=m0)
        return m0, G * dtheta_dz(th_c, idx)[None, :]

    def batch(Zs):
        thetas = [full_theta(zz, base, idx) for zz in Zs]
        res = pool.map(thetas)
        st["nev"] = log_evals(logf, st["nev"], st["it"] + 1, thetas, res)
        st["last_batch"] = (thetas, res)
        return [(rr[0], rr[4]) for rr in res]

    def on_accept(it, zz, q, m, mu, mult, step, cond_A, q_before):
        th = full_theta(zz, base, idx)
        st["z"] = zz
        miss = next((r[1] for t, r in zip(*st["last_batch"]) if np.array_equal(t, th)), 0)
        best = best_record(q, miss, th, m, iter=it, evals=st["nev"], mu=mu)
        (out / "best.json").write_text(json.dumps(best, indent=1, default=float))
        itlog.write(f"{it},{st['nev']},{q_before:.6g},{q:.6g},1,{mu:.3g},{mult:.3g},{step:.4g},{cond_A:.4g},"
                    f"{(time.time() - t0) / 60:.1f}," + ",".join(f"{v:.8g}" for v in th) + "\n")

    def on_iter(it, q_before, q, mu, cond_A, accepted):
        st["it"] = it
        if not accepted:
            itlog.write(f"{it},{st['nev']},{q_before:.6g},{q:.6g},0,{mu:.3g},,0,{cond_A:.4g},"
                        f"{(time.time() - t0) / 60:.1f}," + ",".join(f"{v:.8g}" for v in full_theta(st["z"], base, idx))
                        + "\n")
        print(f"iter {it}  Q {q_before:,.2f} -> {q:,.2f}  mu {mu:.3g}  cond(G'WG) {cond_A:.3g}  evals {st['nev']}  "
              f"{(time.time() - t0) / 60:.0f} min", flush=True)

    try:
        q0, miss, _dt, err, m_start = pool.warm_result
        st["nev"] = log_evals(logf, 0, 0, [th0], [pool.warm_result])
        if m_start is None:
            raise SystemExit(f"the start evaluation failed: {err}")
        (out / "best.json").write_text(json.dumps(best_record(q0, miss, th0, m_start, iter=0, evals=st["nev"]),
                                                  indent=1, default=float))
        itlog.write(f"0,{st['nev']},{q0:.6g},{q0:.6g},1,{args.lm_mu0:.3g},,0,,0," +
                    ",".join(f"{v:.8g}" for v in th0) + "\n")
        print(f"iter 0  Q {q0:,.2f}", flush=True)
        R = lm_iterate(z, q0, m_start, jac, batch, tv, Wm, mults, mu0=args.lm_mu0, iters=args.iters,
                       retries=args.lm_retries, max_step=args.max_step, z_cap=args.z_cap, ftol_abs=args.ftol_abs,
                       ftol_rel=args.ftol_rel, xtol=args.xtol, on_accept=on_accept, on_iter=on_iter,
                       log=lambda s: print(s, flush=True))
        z, q_cur = R["z"], R["Q"]
        print(f"polish stopped: {R['stop']}; best Q {q_cur:,.2f}", flush=True)
        # final Jacobian at the best point (unless the last one was computed there), report and sandwich s.e.
        th_b = full_theta(z, base, idx)
        if R["z_jac"] is None or not np.array_equal(R["z_jac"], z):
            st["it"] = -2
            jac(z)
        rep = jacobian_report(st["G"], T, th_b, idx, free, st["m0"], W=Wm)
        rep["Q"] = q_cur
        (out / "report.json").write_text(json.dumps(rep, indent=1, default=float))
        (out / "report.md").write_text(rep["md"])
        tab = se_block(args, th_b, idx, free, pool, st["G"], out)
    finally:
        pool.close()
    summ = dict(json.loads((out / "best.json").read_text()), stop=R["stop"], evals=st["nev"],
                minutes=(time.time() - t0) / 60)
    (out / "best.json").write_text(json.dumps(summ, indent=1, default=float))
    print(tab.to_string())
    if args.pseudo:
        try:
            import recovery_report
            recovery_report.main(out, out, out)
        except Exception as exc:                                # the report must not lose the run
            print(f"recovery report failed: {exc!r}")
    print(f"-> {out}")


def cmd_noise(args):
    import moments as M
    if args.weighting == "diag_noise" and not (Path(args.noise_file) if args.noise_file else M.NOISE_INPUT).exists():
        print("noise file missing: Q reported with --weighting diag")
        args.weighting = "diag"
    spec = spec_of(args)
    th = start_theta(args)
    out = RESULTS / f"noise_{stamp()}"
    out.mkdir(parents=True, exist_ok=True)
    seeds = [args.seed + r for r in range(args.reps)]
    args.workers = max(1, min(args.workers, args.reps - 1))
    pool = _pool(args, spec, warm=th)                          # the warm-up evaluation is the first seed
    try:
        res = [pool.warm_result] + (pool.map([th] * (len(seeds) - 1), seeds=seeds[1:]) if len(seeds) > 1 else [])
    finally:
        pool.close()
    rows = [dict(seed=sd, Q=r[0], missing=r[1], seconds=r[2]) for sd, r in zip(seeds, res) if r[4] is not None]
    S = np.array([r[4] for r in res if r[4] is not None])
    D = pd.DataFrame(rows)
    D.to_csv(out / "q_by_seed.csv", index=False)
    T = _W["targets"]
    tab = pd.DataFrame(dict(id=T["id"], data=T["value"], se_data=T["se"], sim_mean=S.mean(0), sim_sd=S.std(0, ddof=1),
                            ratio_sd_se=S.std(0, ddof=1) / T["se"], K=args.K, n_seeds=len(S)))
    tab.to_csv(out / "moment_noise.csv", index=False)
    np.save(out / "moments_by_seed.npy", S)
    if args.save_noise_input:
        tab[["id", "sim_sd", "K", "n_seeds"]].assign(source=out.name).to_csv(M.NOISE_INPUT, index=False)
        print(f"wrote {M.NOISE_INPUT}")
    print(D.to_string())
    print(f"Q mean {D.Q.mean():,.1f} sd {D.Q.std():,.1f} ({100 * D.Q.std() / D.Q.mean():.1f}%) -> {out}")


# ----------------------------------------------------------------------------------------------------------------------
def build_parser():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["evaluate", "jacobian", "run", "polish", "se", "noise"])
    ap.add_argument("--size", default=DEFAULT_SIZE, choices=list(SIZES))
    ap.add_argument("--K", type=int, default=3, help="copies of each entry couple")
    ap.add_argument("--seed", type=int, default=20261018, help="CRN seed of the simulation")
    ap.add_argument("--threads", type=int, default=2)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--weighting", default="diag_noise", choices=["diag_noise", "diag", "block", "vcov"])
    ap.add_argument("--noise-file", dest="noise_file", default=None,
                    help="moment noise csv for diag_noise (default inputs/moment_noise.csv)")
    ap.add_argument("--drop", nargs="*", default=None, help="further moment ids excluded from the objective")
    ap.add_argument("--no-default-exclude", dest="no_default_exclude", action="store_true",
                    help="keep the moments of moments.OBJ_EXCLUDE in the objective")
    ap.add_argument("--ctrl-rate", dest="ctrl_rate", type=float, default=0.15)
    ap.add_argument("--start", default=None, help="json with theta (best.json, start_analytic.json, ...)")
    ap.add_argument("--fix", nargs="*", default=None, help="name=value held fixed (e.g. pi_c0=0 pi_c1=0 pi_c2=0 m_H=1)")
    ap.add_argument("--set-fixed", dest="set_fixed", nargs="*", default=None,
                    help="name=value for FIXED_DEFAULTS entries (e.g. sigma_eps=0.1)")
    ap.add_argument("--free", nargs="*", default=None, help="only these parameters free")
    ap.add_argument("--free-set", dest="free_set", default=None, choices=[None, "closed"])
    ap.add_argument("--free-extra", dest="free_extra", nargs="*", default=None,
                    help=f"optional parameters added to the free set: {EXTRA_NAMES}")
    ap.add_argument("--tie", nargs="*", default=None, help="a=b: theta_b = theta_a, b not free (e.g. lam_h_W=lam_h_B)")
    for e in EXT_DEFAULTS:
        ap.add_argument(f"--{e.replace('_', '-')}", dest=e, choices=["on", "off"], default=None,
                        help=f"model extension {e} (default {'on' if EXT_DEFAULTS[e] else 'off'})")
    ap.add_argument("--ext-targets", dest="ext_targets", nargs="*", default=None,
                    help=f"also target the moments of these extensions without turning them on: {list(EXT_TARGETS)}")
    ap.add_argument("--bound-margin", dest="bound_margin", type=float, default=0.01,
                    help="refuse a start within this share of the bound range of a free parameter")
    ap.add_argument("--step", default="value", choices=["value", "range"])
    ap.add_argument("--eval-timeout", dest="eval_timeout", type=float, default=1800.0)
    # run
    ap.add_argument("--popsize", type=int, default=16)
    ap.add_argument("--maxfevals", type=int, default=8000)
    ap.add_argument("--sigma0", type=float, default=0.3)
    ap.add_argument("--cma-seed", dest="cma_seed", type=int, default=None,
                    help="CMA-ES seed (default: distinct per run, from the label, time and pid; recorded in run.json)")
    ap.add_argument("--cma-stds-from", dest="cma_stds_from", default=None,
                    help="jacobian.npz: per-coordinate CMA stds from the weighted column norms in z units")
    ap.add_argument("--tolfun", type=float, default=None, help="CMA tolfun and tolfunhist (e.g. 30, the noise floor)")
    ap.add_argument("--resume", default=None)
    ap.add_argument("--extend-to", dest="extend_to", type=int, default=None)
    ap.add_argument("--label", default="")
    ap.add_argument("--pseudo", action="store_true", help="pseudo-data recovery")
    ap.add_argument("--perturb", action="store_true", help="perturb a real-data start by --start-noise (--pseudo-seed)")
    ap.add_argument("--truth", default=None, help="json with the true theta for --pseudo (default: --start)")
    ap.add_argument("--target-seed", dest="target_seed", type=int, default=20261018,
                    help="CRN seed of the pseudo targets (equal to --seed: optimiser / identification test only)")
    ap.add_argument("--pseudo-seed", dest="pseudo_seed", type=int, default=99, help="seed of the start perturbation")
    ap.add_argument("--start-noise", dest="start_noise", type=float, default=0.5)
    # polish
    ap.add_argument("--iters", type=int, default=15)
    ap.add_argument("--lm-mu0", dest="lm_mu0", type=float, default=0.01)
    ap.add_argument("--lm-mults", dest="lm_mults", type=float, nargs="*", default=None,
                    help="trial multipliers of mu per iteration (default 1e-3 ... 1e3 with >= 7 workers, else 0.1 1 10)")
    ap.add_argument("--lm-retries", dest="lm_retries", type=int, default=2)
    ap.add_argument("--max-step", dest="max_step", type=float, default=3.0, help="largest step in z units")
    ap.add_argument("--z-cap", dest="z_cap", type=float, default=9.0, help="|z| cap (9: within 1.2e-4 of a bound)")
    ap.add_argument("--ftol-abs", dest="ftol_abs", type=float, default=1.0)
    ap.add_argument("--ftol-rel", dest="ftol_rel", type=float, default=1e-3)
    ap.add_argument("--xtol", type=float, default=1e-4)
    # se / noise
    ap.add_argument("--se-reps", dest="se_reps", type=int, default=5)
    ap.add_argument("--reps", type=int, default=5)
    ap.add_argument("--save-noise-input", dest="save_noise_input", action="store_true",
                    help="noise: also write inputs/moment_noise.csv (the diag_noise weights)")
    return ap


def main():
    args = build_parser().parse_args()
    resolve(args)
    RESULTS.mkdir(parents=True, exist_ok=True)
    {"evaluate": cmd_evaluate, "jacobian": cmd_jacobian, "run": cmd_run, "polish": cmd_polish, "se": cmd_se,
     "noise": cmd_noise}[args.command](args)


if __name__ == "__main__":
    main()
