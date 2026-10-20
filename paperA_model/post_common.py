"""Paper A model: shared helpers of the post-estimation scripts (fit_table, recovery_table, diagnostics_marriage,
counterfactuals). Read-only use of estimate.py, moments.py, panels.py, simulate.py: nothing on the estimation code
path is changed, and every evaluation here uses the same settings as the SMM objective (estimate._init_worker).

setup(start, ...) reproduces 'estimate.py evaluate --start <start>' exactly: the run's extensions, --set-fixed entries,
weighting and objective exclusions are taken from run.json when <start> sits in a run folder (best.json next to
run.json), else the defaults (estimate.EXT_DEFAULTS, diag_noise, moments.OBJ_EXCLUDE). evaluate(ctx, theta,
overrides) is estimate.model_moments with model.Model test overrides passed through to simulate() (e.g.
{"sig_E": 0, "sig_N": 0} or {"ui_exp": 1/12}); with overrides=None it equals the objective's evaluation.
Outputs of the scripts go to results/<name>_<stamp>/ (aggregate numbers only).
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import json                                                                    # noqa: E402
import sys                                                                     # noqa: E402
import time                                                                    # noqa: E402
from dataclasses import dataclass, field                                       # noqa: E402
from datetime import datetime                                                  # noqa: E402
from pathlib import Path                                                       # noqa: E402

import numpy as np                                                             # noqa: E402
import pandas as pd                                                            # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
RESULTS = Path(os.environ.get("PAPERA_OUT", str(HERE / "results")))
REPO = HERE.parent.parent
ANALYTIC_START = HERE / "inputs" / "start_analytic.json"


def stamp() -> str:
    job = os.environ.get("SLURM_JOB_ID")
    return f"{datetime.now():%Y%m%d_%H%M%S}" + (f"_j{job}" if job else f"_p{os.getpid()}")


def out_dir(name: str) -> Path:
    d = RESULTS / f"{name}_{stamp()}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def run_json_of(start) -> dict | None:
    """run.json of the run folder that holds <start> (best.json / mean.json), if any."""
    if not start:
        return None
    p = Path(start)
    p = p if p.is_dir() else p.parent
    f = p / "run.json"
    return json.loads(f.read_text()) if f.exists() else None


def resolve_start(start) -> str | None:
    """A run folder -> its best.json; a file -> itself; None -> the analytic start (inputs, as estimate.py)."""
    if not start:
        return None
    p = Path(start)
    if p.is_dir():
        p = p / "best.json"
    if not p.exists():
        raise SystemExit(f"--start {start}: not found")
    return str(p)


@dataclass
class Ctx:
    E: object
    args: object
    spec: dict
    theta: np.ndarray
    run: dict | None = None
    notes: list = field(default_factory=list)

    @property
    def T(self):
        return self.E._W["targets"]

    @property
    def W(self):
        return self.E._W["W"]


def setup(start=None, size=None, K=3, seed=None, threads=2, weighting=None, noise_file=None) -> Ctx:
    """Initialise estimate.py's worker state in this process and return the start theta (32-vector)."""
    import estimate as E
    start = resolve_start(start)
    run = run_json_of(start)
    argv = ["evaluate", "--threads", str(threads), "--K", str(K), "--workers", "1"]
    notes = []
    if size:
        argv += ["--size", size]
    elif run and run.get("size"):
        argv += ["--size", run["size"]]
    if seed is not None:
        argv += ["--seed", str(seed)]
    elif run and run.get("seed"):
        argv += ["--seed", str(run["seed"])]
    if start:
        argv += ["--start", start]
    if run:
        for e, on in (run.get("ext") or {}).items():
            if e in E.EXT_DEFAULTS:
                argv += [f"--{e.replace('_', '-')}", "on" if on else "off"]
        sf = run.get("set_fixed") or {}
        if sf:
            argv += ["--set-fixed"] + [f"{k}={json.dumps(v)}" for k, v in sf.items()]
        if run.get("weighting") and not weighting:
            weighting = run["weighting"]
        nf = run.get("noise_file_arg")
        if nf and not noise_file:
            if Path(nf).exists():
                noise_file = nf
            else:
                notes.append(f"run's noise file {nf} not found here: default inputs/moment_noise.csv used for the weights")
        import moments as M
        extra_drop = [d for d in (run.get("obj_exclude") or []) if d not in M.OBJ_EXCLUDE
                      and d not in E.CPS_FLOW_IDS[True] + E.CPS_FLOW_IDS[False]]
        if extra_drop:
            argv += ["--drop"] + extra_drop
        if run.get("no_default_exclude"):
            argv += ["--no-default-exclude"]
        if run.get("ext_targets"):
            argv += ["--ext-targets"] + list(run["ext_targets"])
    if weighting:
        argv += ["--weighting", weighting]
    if noise_file:
        argv += ["--noise-file", noise_file]
    args = E.build_parser().parse_args(argv)
    E.resolve(args)
    spec = E.spec_of(args)
    E._init_worker(spec)
    th = E.start_theta(args)
    return Ctx(E=E, args=args, spec=spec, theta=th, run=run, notes=notes)


def theta_dict(ctx: Ctx, th=None) -> dict:
    return ctx.E.vec_dict(th if th is not None else ctx.theta)


def with_theta(ctx: Ctx, **changes) -> np.ndarray:
    d = theta_dict(ctx)
    for k, v in changes.items():
        if k not in d:
            raise KeyError(k)
        d[k] = float(v)
    return ctx.E.dict_vec(d)


def evaluate(ctx: Ctx, theta_vec=None, overrides=None, seed=None, keep_res=False):
    """estimate.model_moments with Model overrides. Returns dict(m, Q, missing, blocks, seconds, res (optional))."""
    from simulate import simulate
    E = ctx.E
    M, cfg, spec = E._W["M"], E._W["cfg"], E._W["spec"]
    th = E.vec_dict(E.pad_vec(ctx.theta if theta_vec is None else theta_vec, E._W["fx"]))
    fx = dict(E._W["fx"])
    for n in E.EXTRA_NAMES:
        fx[n] = th.pop(n)
    t0 = time.time()
    tim = {}
    res = simulate(th, cfg, E._W["entry"], K=spec["K"], seed=spec["seed"] if seed is None else seed, fixed=fx,
                   overrides=overrides, timing=tim)
    md = M.compute(res, theta=th, merge_s12=cfg.merge_s12, ctrl_rate=spec["ctrl_rate"], timing=tim,
                   cps_classif=E._W.get("classif"), ext_moments=E._W.get("ext_moments"))
    m = M.vector(md, E._W["targets"])
    q, miss = M.objective(m, E._W["targets"], E._W["W"])
    out = dict(m=m, Q=float(q), missing=int(miss), blocks=E.block_table(m, E._W["targets"], E._W["W"]),
               seconds=time.time() - t0, theta=th)
    if keep_res:
        out["res"] = res
    else:
        del res
    return out


def simulate_only(ctx: Ctx, theta_vec=None, overrides=None, seed=None, cfg=None):
    """simulate() at theta with the run's fixed inputs (no moments). Returns (res, theta dict without extras, fx)."""
    from simulate import simulate
    E = ctx.E
    th = E.vec_dict(E.pad_vec(ctx.theta if theta_vec is None else theta_vec, E._W["fx"]))
    fx = dict(E._W["fx"])
    for n in E.EXTRA_NAMES:
        fx[n] = th.pop(n)
    res = simulate(th, cfg or E._W["cfg"], E._W["entry"], K=ctx.spec["K"],
                   seed=ctx.spec["seed"] if seed is None else seed, fixed=fx, overrides=overrides)
    return res, th, fx


def moments_frame(ctx: Ctx, m) -> pd.DataFrame:
    T, W = ctx.T, ctx.W
    w = np.diag(W)
    return T[["id", "block", "value", "se"]].assign(sim=m, z=(m - T["value"]) / T["se"],
                                                     in_objective=(w > 0).astype(int),
                                                     q=np.where(w > 0, (m - T["value"]) ** 2 * w, 0.0))


def write_json(path: Path, obj):
    path.write_text(json.dumps(obj, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o)))
