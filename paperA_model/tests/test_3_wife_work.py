"""Check (3): the wife's work rises with lower assets and after the husband's loss. At the analytic start values a
wife who holds a job works with probability 1.000 in every state (quitting loses the job and her human capital
accumulation), so the check is run at an interior point: a constant is added to phi_F and phi_P (bisection) so that
P(works) = 0.6 at the reference state (t = 60, no child, husband employed, assets 5). From the stored solution (White,
s = 0, low type, era 2) at the wife's age 30 (t = 60) and 40 (t = 180), both spouses at the middle human capital level,
no child and youngest 0-5, transitory pair (-, -): P(wife works | she has a job) is non-increasing in assets over the
grid up to $100k, and P(works | husband non-employed, entitled or not) > P(works | husband employed) at assets 0, 5 and
20 thousand. Pass: no monotonicity violation above 1e-6 and every response positive. The step across the SNAP asset
limit (grid nodes L and L + 1e-5 since 2026-10-19) is excluded: losing eligibility raises P(works) there (the notch),
by 0.0002-0.002 at the interior point; its size is reported.
(The D16 fallback decision -- can the base entry rate and the SIPP build-up both be fit -- needs the moments, stage 3.)"""
from _common import test_config, theta, report
import numpy as np
from model import Model
from solve import solve, alternatives


def p_work(m, sol, t, lh, k, a):
    c = (m.H - 1) // 2
    alts, p = alternatives(m, sol, t, 0, lh, c, c, k, 0, a)
    return float(sum(pi for alt, pi in zip(alts, p) if alt[2] > 0))


def main():
    cfg = test_config()
    base = theta()

    def at(shift, t_stop):
        th = dict(base, phi_F=base["phi_F"] + shift, phi_P=base["phi_P"] + shift)
        m = Model(th, cfg, 2, 1, 0, 0)
        return m, solve(m, store=True, t_stop=t_stop)

    lo, hi = 0.0, 2.0
    for _ in range(9):
        mid = 0.5 * (lo + hi)
        m, sol = at(mid, 60)
        if p_work(m, sol, 60, 0, 0, 5.0) > 0.6:
            lo = mid
        else:
            hi = mid
    shift = 0.5 * (lo + hi)
    m, sol = at(shift, 0)
    viol, resp, lines = 0, [], [f"work-cost shift {shift:.3f} (utility units)"]
    for t in (60, 180):
        for k in (0, 1):
            grid = m.agrid[m.agrid <= 100]
            pw = np.array([p_work(m, sol, t, 0, k, a) for a in grid])
            dpw = np.diff(pw)
            notch = (grid[:-1] == m.asset_limit)                  # step from L (eligible) to L + eps (not)
            viol += int(np.sum((dpw > 1e-6) & ~notch))
            if notch.any():
                lines.append(f"t={t} k={k}: P(work) step across the SNAP asset limit {float(dpw[notch][0]):+.4f}")
            lines.append(f"t={t} k={k}: P(work) from a = {grid[0]:.1f} to {grid[-1]:.0f}: {pw[0]:.3f} -> {pw[-1]:.3f}")
            for a in (0.0, 5.0, 20.0):
                pe, pu, pn = (p_work(m, sol, t, lh, k, a) for lh in (0, 1, 2))
                resp += [pu - pe, pn - pe]
                lines.append(f"   a={a:4.0f}: P(work) husband employed {pe:.3f}, entitled {pu:.3f}, not entitled {pn:.3f}")
    for l in lines:
        print("   ", l)
    return report("3 wife's work: lower assets and his loss", viol == 0 and min(resp) > 0,
                  f"interior point (shift {shift:.3f}); monotonicity violations {viol}; response to his loss min "
                  f"{min(resp):+.4f}, max {max(resp):+.4f}")


if __name__ == "__main__":
    main()
