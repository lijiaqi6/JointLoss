"""Check (4): the search friction lengthens non-employment. No-choice test on husbands (who always take a job): the
mean completed non-employment spell after a displacement equals 1 / lambda_h within 5%, for lambda_h = 0.2 and 0.1
(delta_h raised to 0.02 for many spells, no separation, White couples, 1,500 synthetic couples)."""
from _common import test_config, theta, entry, report
import numpy as np
from simulate import simulate


def spells(res):
    lh, st = res.i("lh"), res.i("status")
    out = []
    for i in range(lh.shape[0]):
        x = np.where(st[i] == 1, lh[i], -9)
        run = 0
        for v in x:
            if v in (1, 2):
                run += 1
            else:
                if v == 0 and run > 0:
                    out.append(run)
                run = 0
    return np.array(out)


def main():
    cfg = test_config()
    e = entry(1500, race=1, s=0)
    ok_all, txt = True, []
    for lam in (0.2, 0.1):
        th = theta(delta_h_W=0.02, lam_h_W=lam, sigma0_W=0.0, sigmaJ_W=0.0, p_H=0.0)
        sp = spells(simulate(th, cfg, e, K=1))
        ok = abs(sp.mean() * lam - 1) < 0.05
        ok_all &= ok
        txt.append(f"lambda {lam}: mean spell {sp.mean():.2f} months (1/lambda = {1 / lam:.1f}; {len(sp):,} spells)")
    return report("4 search friction lengthens non-employment", ok_all, "; ".join(txt))


if __name__ == "__main__":
    main()
