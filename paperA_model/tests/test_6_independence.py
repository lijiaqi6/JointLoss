"""Check (6): with pi_c(.) = 0 and m_H = 1 the spouses' job losses are independent in the simulated monthly panel:
P(wife displaced | husband displaced) / P(wife displaced | husband not displaced), among married couple-months in which
both work, within 5% of 1. Hazards raised to 0.03 for both spouses (precision), 2,000 synthetic couples x 3 copies."""
from _common import test_config, theta, entry, report
import numpy as np
from simulate import simulate


def main():
    cfg = test_config()
    th = theta(pi_c0=0.0, pi_c1=0.0, pi_c2=0.0, m_H=1.0, p_H=0.0, delta_w_B=0.03, delta_w_W=0.03, delta_h_B=0.03,
               delta_h_W=0.03)
    res = simulate(th, cfg, entry(2000), K=3)
    st, hw_, lh, hh_ = res.i("status"), res.i("hrs_w"), res.i("lh"), res.i("hrs_h")
    both = (st == 1) & (hw_ > 0) & (lh == 0) & (hh_ > 0)
    dw, dh = res.i("disp_w")[both], res.i("disp_h")[both]
    p1, p0 = dw[dh == 1].mean(), dw[dh == 0].mean()
    n1, n0 = (dh == 1).sum(), (dh == 0).sum()
    ratio = p1 / p0
    se = ratio * np.sqrt((1 - p1) / (p1 * n1) + (1 - p0) / (p0 * n0))
    return report("6 independence without common shock and type", abs(ratio - 1) < 0.05,
                  f"P(w|h lost) {p1:.4f} (n={n1:,}), P(w|h kept) {p0:.4f} (n={n0:,}), ratio {ratio:.3f} (s.e. {se:.3f})")


if __name__ == "__main__":
    main()
