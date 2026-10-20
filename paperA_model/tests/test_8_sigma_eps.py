"""Solver-stage choice of the taste-shock scale (plan Section 1.1: the smallest sigma_eps for which the DC-EGM upper
envelope is smooth at the median state). For sigma_eps in a grid, solve (White, s = 0, low type, era 2, test size) and
report the share of non-monotone endogenous grids (upper-envelope activity) at the median state (middle human capital
levels, no child, transitory (-, -)) and over all states, and the solve time. Information (always PASS); the work-cost
start values scale with sigma_eps in analytic_start.py, so they are recomputed for each value."""
import time
from _common import test_config, report
import json
import numpy as np
from params import load_fixed, default_start, wage_process_closed_form
from model import Model
from solve import solve
import analytic_start


def main():
    cfg = test_config()
    lines = []
    for sig in (0.01, 0.02, 0.05, 0.10):
        fx = load_fixed()
        fx["sigma_eps"] = sig
        th, _, _ = analytic_start.main(write=False, verbose=False)
        from analytic_start import static_preferences
        th.update(static_preferences(th, fx, sig))
        m = Model(th, cfg, 2, 1, 0, 0, fixed=fx)
        t0 = time.perf_counter()
        sol = solve(m, store=True)
        dt = time.perf_counter() - t0
        Xe = sol.C.astype(np.float64) + m.agrid
        nonmono = np.any(np.diff(Xe, axis=-1) <= 0, axis=-1)          # (T, cfg, hw, hh, k, nu)
        c = (m.H - 1) // 2
        med = nonmono[:, :, c, c, 0, 0]
        lines.append(f"sigma_eps {sig:.2f}: non-monotone EGM grids, median state {med.mean():.3f}, all states "
                     f"{nonmono.mean():.3f}; solve {dt:.1f}s")
    for l in lines:
        print("   ", l)
    return report("8 sigma_eps smoothness profile (information)", True, " | ".join(lines))


if __name__ == "__main__":
    main()
