"""Check (10), measurement layer (plan stage 2):
 (a) moments.twfe (exact unit + cell fixed effects) equals IGE/60's TWFE class (alternating projections) on a random
     unbalanced stacked panel (max |difference| of the coefficients < 1e-6);
 (b) every target is finite on a simulation of 2,000 synthetic couples (test size) and each sample has observations;
 (c) the CPS rotation: the literal 4-8-4 sample (one window per couple-copy) gives the same entry rate as all rotation
     offsets within 3 binomial standard errors (the default 'all' mode is the expectation of the CPS sampling)."""
from _common import test_config, theta, entry, report
import numpy as np
import moments as M
import panels as PN
from simulate import simulate


def main():
    rng = np.random.default_rng(3)
    N = 4000
    unit = rng.integers(0, 600, N)
    cell = rng.integers(0, 40, N)
    X = np.column_stack([rng.random(N) < 0.3, rng.normal(size=N)]).astype(float)
    y = X @ np.array([1.5, -0.7]) + rng.normal(size=600)[unit] + rng.normal(size=40)[cell] + rng.normal(size=N)
    b1 = M.twfe(y, X, unit, cell)
    I6 = M.ige60()
    b2 = I6.TWFE(y, X, [unit, cell], tol=1e-12, maxit=20000).fit()
    da = float(np.max(np.abs(b1 - b2)))
    th = theta()
    res = simulate(th, test_config(), entry(2000), K=1)
    out, Nn = M.compute(res, theta=th, merge_s12=False, return_n=True)
    T = M.load_targets()
    m = M.vector(out, T)
    nfin = int(np.isfinite(m).sum())
    empty = [k for k in T["id"] if Nn.get(k, 0) == 0]
    R = PN.records(res, theta=th, merge_s12=False)
    ea = PN.cps_samples(R, "all")["entry"]["y"]
    es = PN.cps_samples(R, "single")["entry"]["y"]
    p = ea.mean()
    z = (es.mean() - p) / np.sqrt(p * (1 - p) / max(len(es), 1))
    ok = da < 1e-6 and nfin == len(T) and not empty and abs(z) < 3
    return report("10 measurement layer", ok,
                  f"(a) twfe vs IGE/60 TWFE max |db| {da:.1e}; (b) finite targets {nfin}/{len(T)}, empty samples "
                  f"{empty if empty else 'none'}; (c) CPS entry rate all offsets {p:.4f} (n={len(ea):,}) vs one 4-8-4 "
                  f"window {es.mean():.4f} (n={len(es):,}), z {z:+.2f}")


if __name__ == "__main__":
    main()
