"""Paper A model: pseudo-data recovery report (identification plan Section 2.4).

For a recovery run (estimate.py run --pseudo), a Jacobian at the truth (estimate.py jacobian, same --start) and the
simulation-noise runs at the truth (estimate.py noise), the simulation-noise standard error of each free parameter is
    se_noise = sqrt(diag[(G'WG)^-1 G'W Sigma_sim W G (G'WG)^-1])
with G the Jacobian columns of the run's free parameters, W the run's weighting matrix and Sigma_sim the covariance of
the simulated moments across CRN seeds; pass = |estimate - truth| < 2 se_noise for every parameter and Q at the
estimate below Q at the truth plus the noise band (the spread of Q across seeds).
Run: python IGE/paperA_model/recovery_report.py <run dir> <jacobian dir> <noise dir>
A polish run (estimate.py polish --pseudo) holds all three in its own folder (jacobian.npz at the estimate,
moments_by_seed.npy from the s.e. re-simulations) and writes this report itself.
Writes <run dir>/recovery_report.md and .csv (aggregate numbers only).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def main(run_dir, jac_dir, noise_dir):
    import moments as M
    from params import PARAM_NAMES, EXTRA_NAMES, LATE_NAMES
    NAMES = PARAM_NAMES + EXTRA_NAMES + LATE_NAMES
    run_dir, jac_dir, noise_dir = Path(run_dir), Path(jac_dir), Path(noise_dir)
    run = json.loads((run_dir / "run.json").read_text())
    best = json.loads((run_dir / "best.json").read_text())
    T = pd.read_csv(run["targets_csv"]) if run.get("targets_csv") else M.load_targets()
    W = M.weights(T, run.get("weighting", "diag"), exclude=run.get("obj_exclude"), noise_file=run.get("noise_file_arg"),
                  K=run.get("K"))
    J = np.load(jac_dir / "jacobian.npz")
    G_all, jidx = J["G"], list(J["idx"])
    free = run["free"]
    cols = [jidx.index(NAMES.index(n)) for n in free]
    G = G_all[:, cols]
    S = np.load(noise_dir / "moments_by_seed.npy")
    Vsim = np.cov(S.T)
    ok = np.isfinite(G).all(axis=1) & np.isfinite(Vsim).all(axis=1) & (np.diag(W) > 0)
    Gk, Wk, Vk = G[ok], W[np.ix_(ok, ok)], Vsim[np.ix_(ok, ok)]
    A = np.linalg.pinv(Gk.T @ Wk @ Gk)
    Vn = A @ Gk.T @ Wk @ Vk @ Wk @ Gk @ A
    se_n = np.sqrt(np.maximum(np.diag(Vn), 0))
    Vd = M.load_vcov(T["id"])
    dv = np.diag(Vd).copy()
    dv[dv <= 0] = T["se"].to_numpy(float)[dv <= 0] ** 2
    Vd[np.diag_indices_from(Vd)] = dv
    Vdat = A @ Gk.T @ Wk @ Vd[np.ix_(ok, ok)] @ Wk @ Gk @ A
    se_d = np.sqrt(np.maximum(np.diag(Vdat + Vn), 0))
    truth = np.array(run["truth"])
    start = np.array(run["theta_start"])
    est = np.array([best["theta"].get(n, np.nan) for n in NAMES])
    ix = [NAMES.index(n) for n in free]
    tab = pd.DataFrame(dict(param=free, truth=truth[ix], start=start[ix], estimate=est[ix], se_noise=se_n, se_data=se_d))
    tab["z_start"] = (tab["start"] - tab["truth"]) / tab["se_noise"]
    tab["z_est"] = (tab["estimate"] - tab["truth"]) / tab["se_noise"]
    tab["z_est_data"] = (tab["estimate"] - tab["truth"]) / tab["se_data"]
    tab["pass"] = tab["z_est"].abs() < 2
    qn = pd.read_csv(noise_dir / "q_by_seed.csv")
    if (run_dir / "generations.csv").exists():
        gens = pd.read_csv(run_dir / "generations.csv")
    else:                                                       # polish run: iterations instead of generations
        it = pd.read_csv(run_dir / "iterations.csv")
        it = it[it["accepted"] == 1]
        gens = pd.DataFrame(dict(gen=it["iter"], evals=it["evals"], best_Q=it["Q_after"], minutes=it["minutes"]))
    md = [f"# Recovery: {run_dir.name}", "",
          f"{len(free)} free parameters; truth = {run.get('start') or 'analytic start values'}; start = truth + "
          f"N(0, {run.get('start_noise')}) in logistic units (seed {run.get('pseudo_seed')}); targets = model moments at "
          f"the truth with CRN seed {run.get('target_seed')} (estimation seed {run.get('seed')}); "
          f"{int(gens['evals'].iloc[-1])} evaluations in {int(gens['gen'].iloc[-1])} generations "
          f"({gens['minutes'].iloc[-1]:.0f} min). Best Q {best['Q']:.3g} (Q at the truth = 0 when the target seed equals "
          f"the estimation seed); noise band of Q at the real targets across {len(qn)} seeds: sd {qn['Q'].std():,.1f}.",
          "", "z: (value - truth) / s.e.; noise s.e. = simulation noise only (the plan's yardstick); data s.e. = sandwich with "
          "the bootstrap covariance of the targets plus simulation noise (the precision of an estimate on real data).", "",
          "| parameter | truth | start | estimate | noise s.e. | z start | z estimate | within 2 noise s.e. | data s.e. | "
          "z estimate (data s.e.) |", "|---|---:|---:|---:|---:|---:|---:|---|---:|---:|"]
    for r in tab.rename(columns={"pass": "pass_"}).itertuples():
        md.append(f"| {r.param} | {r.truth:.4g} | {r.start:.4g} | {r.estimate:.4g} | {r.se_noise:.3g} | {r.z_start:+.1f} | "
                  f"{r.z_est:+.1f} | {'yes' if r.pass_ else 'NO'} | {r.se_data:.3g} | {r.z_est_data:+.2f} |")
    md += ["", f"Within 2 noise s.e.: {int(tab['pass'].sum())} of {len(tab)}; within 2 data s.e.: "
           f"{int((tab['z_est_data'].abs() < 2).sum())} of {len(tab)}. Q by generation (best): "
           + ", ".join(f"{g}: {q:.3g}" for g, q in zip(gens['gen'][::max(1, len(gens) // 10)],
                                                         gens['best_Q'][::max(1, len(gens) // 10)]))]
    (run_dir / "recovery_report.md").write_text("\n".join(md) + "\n")
    tab.to_csv(run_dir / "recovery_report.csv", index=False)
    print("\n".join(md))


if __name__ == "__main__":
    main(*sys.argv[1:4])
