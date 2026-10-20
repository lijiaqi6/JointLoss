"""Check 0 (solver correctness): the DC-EGM value of an alternative at cash on hand X equals a brute-force maximisation
over a fine grid (400,001 points) of end-of-month assets of u((X - a') / sc) + beta W(a'), with W between asset nodes
represented exactly as the solver and the simulator represent it, at random states, months, configurations and
cash-on-hand levels (200 states x 7 cash-on-hand levels, sigma_eps = 0.05).

Representation (Config.w_interp): 'hermite' (default since 2026-10-18): cubic Hermite interpolation of W between the
asset nodes from the node values and the node derivatives D = u'(c / sc) / (beta sc) recovered from the stored EGM
consumption, monotone-limited. The stage-3 code used chords ('linear'); its failure of this check (99th percentile
2.1e-3) was not a solver error near the floor: the large gaps sat in the middle of the grid (a' near 4 and 17 thousand $),
where the brute-force optimum on chords sticks to a grid node because the chord slope drops there, while the EGM
policy (exact derivatives at the nodes) passes between nodes and is valued on the chord below the true W. With a
derivative-consistent W the maximisation is smooth and the EGM point is the maximum up to second-order error.
Both representations are reported; pass on the default: 99th percentile of |difference| < 1e-3 and maximum < 0.1
sigma_eps (5e-3 utility units)."""
from _common import test_config, theta, report
import numpy as np
from model import Model, age_group
from solve import solve, env_query, util, node_derivs


def w_hermite(ap, ag, W, Dn):
    """Vectorised version of solve.wval (monotone-limited Hermite) at points ap."""
    p = np.clip(np.searchsorted(ag, ap, side="right") - 1, 0, len(ag) - 2)
    h = ag[p + 1] - ag[p]
    s = (ap - ag[p]) / h
    w0, w1 = W[p], W[p + 1]
    dl = (w1 - w0) / h
    d0 = np.clip(Dn[p], 0, None)
    d1 = np.clip(Dn[p + 1], 0, None)
    d0 = np.minimum(d0, 3 * np.maximum(dl, 0))
    d1 = np.minimum(d1, 3 * np.maximum(dl, 0))
    s2, s3 = s * s, s * s * s
    v = (2 * s3 - 3 * s2 + 1) * w0 + (s3 - 2 * s2 + s) * h * d0 + (3 * s2 - 2 * s3) * w1 + (s3 - s2) * h * d1
    return np.where(dl > 0, v, w0 + s * (w1 - w0))


def gaps(interp, nstate=200, seed=0, **thkw):
    cfg = test_config(T=60, w_interp=interp)
    m = Model(theta(**thkw), cfg, 2, 1, 0, 0)
    sol = solve(m, store=True)
    herm = interp == "hermite"
    rng = np.random.default_rng(seed)
    diffs, where = [], []
    ap = np.unique(np.concatenate([np.linspace(m.agrid[0], m.agrid[-1], 400001), m.agrid]))   # incl. the nodes
    for _ in range(nstate):
        t = int(rng.integers(0, 59))
        c = int(rng.integers(0, m.ncfg))
        hw, hh, k, nu = (int(rng.integers(0, m.H)), int(rng.integers(0, m.H)), int(rng.integers(0, 3)),
                         int(rng.integers(0, 4)))
        g = age_group(t)
        sc = m.sc[g, k]
        ce = sol.C[t, c, hw, hh, k, nu].astype(float)
        W = sol.W[t, c, hw, hh, k, nu].astype(float)
        Dn = node_derivs(ce, sc, m.beta, m.gamma)
        Xe = ce + m.agrid
        mono = bool(np.all(np.diff(Xe) > 0))
        Wf = w_hermite(ap, m.agrid, W, Dn) if herm else np.interp(ap, m.agrid, W)
        for X in np.linspace(max(m.xfloor[g, k], 0.2), 40.0, 7):
            cc, vv = env_query(X, Xe, ce, W, Dn, m.agrid, sc, m.beta, m.gamma, mono, herm, m.jL)
            feas = ap < X
            vals = util((X - ap[feas]) / sc, m.gamma) + m.beta * Wf[feas]
            jb = int(np.argmax(vals))
            diffs.append(abs(vv - vals[jb]))
            where.append((X, X - cc, ap[feas][jb], mono))
    return np.array(diffs), where, m


def main():
    out = {}
    for interp in ("linear", "hermite"):
        d, where, m = gaps(interp)
        out[interp] = (d, where)
        big = [w for di, w in zip(d, where) if di > 1e-3]
        print(f"    {interp:8s}: median {np.median(d):.1e}, 99th pct {np.percentile(d, 99):.1e}, max {d.max():.1e}, "
              f"share > 1e-3 {np.mean(d > 1e-3):.3f}; large gaps at a' (EGM) = "
              + ", ".join(f"{w[1]:.2f}" for w in big[:8]))
    d = out["hermite"][0]
    dl = out["linear"][0]
    p99, mx = np.percentile(d, 99), d.max()
    # full-horizon accuracy (420 months): the value at t = 0 against a 90-point Hermite solution (interpolated to the
    # 30 nodes); the 30-point Hermite solution must be within a median 0.05 utility units of it and closer than the
    # 30-point chord solution (catches errors that build up over the horizon, e.g. feedback at the top of the grid)
    V = {}
    for interp, na in (("linear", 30), ("hermite", 30), ("hermite", 90)):
        mm = Model(theta(), test_config(w_interp=interp, n_assets=na), 2, 1, 0, 0)
        V[(interp, na)] = (mm.agrid, solve(mm, store=False).V0)
    g30, g90 = V[("hermite", 30)][0], V[("hermite", 90)][0]
    ref = np.apply_along_axis(lambda v: np.interp(g30, g90, v), -1, V[("hermite", 90)][1])
    dh = float(np.median(np.abs(V[("hermite", 30)][1] - ref)))
    dlin = float(np.median(np.abs(V[("linear", 30)][1] - ref)))
    rel = dh
    print(f"    V(t = 0) vs the 90-point Hermite solution: median |difference| Hermite-30 {dh:.4f}, linear-30 {dlin:.4f}")
    return report("0 EGM vs brute force", p99 < 1e-3 and mx < 0.1 * m.sigma_eps and dh < 0.05 and dh < dlin,
                  f"|v_EGM - v_brute| over {len(d)} points, W Hermite (default): median {np.median(d):.1e}, 99th pct "
                  f"{p99:.1e}, max {mx:.1e}, share > 1e-3 {np.mean(d > 1e-3):.3f} | W linear (stage 3): 99th pct "
                  f"{np.percentile(dl, 99):.1e}, max {dl.max():.1e}; V(t=0) vs 90-point Hermite: median |diff| Hermite-30 {dh:.3f}, linear-30 {dlin:.3f}")


if __name__ == "__main__":
    main()
