"""Check (1): flat consumption with no risk and beta (1 + r) = 1. No displacement, separation, human capital moves,
transitory shocks, children or SNAP; the wife is not employed and never finds a job; the husband always works full
time (phi_h very negative); one era; the couple enters at 25 in 1984 and is followed to 60. With these settings the
Euler equation and the terminal (annuity) value imply the same consumption in every month, including retirement.
Pass: max |c_t / mean(c) - 1| < 1e-3 over the 420 months."""
from _common import test_config, theta, entry, report
import numpy as np
from params import load_fixed
from simulate import simulate


def main():
    fx = load_fixed()
    ov = dict(r_m=1 / fx["beta"] - 1, dw=0.0, dh=0.0, pic=0.0, sig_E=0.0, sig_N=0.0, no_hc=1, sig_nu_w=0.0,
              sig_nu_h=0.0, no_child=1, no_snap=1, lw_=0.0)
    th = theta(phi_h=-5.0, p_H=0.0)
    e = entry(1, year0=1984, age0=25, race=1, s=0, a0=10.0, ew0=0, eh0=1, k0=0, hw0=4, hh0=4)
    cfg = test_config(sim_end_year=2030)
    res = simulate(th, cfg, e, K=1, overrides=ov)
    st = res.i("status")[0]
    c = res.f("c")[0][st >= 0].astype(float)
    hrs = res.i("hrs_h")[0][st >= 0]
    a = res.f("a")[0][st >= 0]
    dev = np.max(np.abs(c / c.mean() - 1))
    return report("1 flat consumption (beta(1+r)=1, no risk)", dev < 1e-3 and bool(np.all(hrs == 2)) and len(c) == 420,
                  f"{len(c)} months, mean c {c.mean():.4f}, max rel. deviation {dev:.2e}, husband full time in every "
                  f"month: {bool(np.all(hrs == 2))}, assets {a[0]:.1f} -> {a[-1]:.1f} (thousand $)")


if __name__ == "__main__":
    main()
