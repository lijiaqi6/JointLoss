"""Accuracy cost of the fallback grids (information for the size decision). Same parameters, entry couples and
draws, one era (so all three runs share the policy schedule): simulated summary statistics at 7 human capital levels x
30 asset points (spec), 5 x 30 and 5 x 20. Always PASS; the differences are printed."""
from _common import test_config, theta, entry, report
import numpy as np
from simulate import simulate


def stats(res):
    st = res.i("status")
    mar = st == 1
    ok = st >= 0
    hw_, hh_ = res.i("hrs_w"), res.i("hrs_h")
    a = res.f("a")
    return {"wife works": ((hw_ > 0) & mar).sum() / mar.sum(),
            "wife PT share": ((hw_ == 1) & mar).sum() / ((hw_ > 0) & mar).sum(),
            "husband PT share": ((hh_ == 1) & mar).sum() / ((hh_ > 0) & mar).sum(),
            "mean assets": float(a[ok].mean()), "share a<=0": float((a[ok] <= 0).mean()),
            "mean c": float(res.f("c")[ok].mean()), "SNAP": float((res.f("snap")[ok] > 0).mean()),
            "married": mar.sum() / ok.sum()}


def main():
    th = theta()
    e = entry(1500)
    out = {}
    for nm, kw in (("7 x 30 (spec)", dict(n_hc=7, n_assets=30)), ("5 x 30", dict(n_hc=5, n_assets=30)),
                   ("5 x 20", dict(n_hc=5, n_assets=20))):
        out[nm] = stats(simulate(th, test_config(**kw), e, K=1))
    keys = list(next(iter(out.values())))
    print("    " + f"{'':18s}" + "".join(f"{k:>16s}" for k in out))
    for k in keys:
        print("    " + f"{k:18s}" + "".join(f"{out[n][k]:16.4f}" for n in out))
    d = {n: max(abs(out[n][k] - out["7 x 30 (spec)"][k]) / max(abs(out["7 x 30 (spec)"][k]), 1e-9)
                for k in ("wife works", "mean assets", "mean c")) for n in out}
    return report("9 grid accuracy (information)", True,
                  "max relative difference vs 7 x 30 in (wife works, mean assets, mean c): " +
                  ", ".join(f"{n} {v:.3f}" for n, v in d.items()))


if __name__ == "__main__":
    main()
