"""Check (2): a precautionary buffer with risk. Mean simulated assets rise with the displacement hazards: no
displacement risk < start values < hazards doubled (same draws, one era, test size, 1,500 synthetic couples).
Pass: the ordering holds and mean assets are positive."""
from _common import test_config, theta, entry, report
from simulate import simulate

HAZ = ("delta_w_B", "delta_w_W", "delta_h_B", "delta_h_W", "pi_c0", "pi_c1", "pi_c2")


def mean_assets(th, e, cfg):
    res = simulate(th, cfg, e, K=1)
    st = res.i("status")
    a = res.f("a")
    return float(a[st >= 0].mean()), float((a[st >= 0] <= 0).mean())


def main():
    cfg = test_config()
    e = entry(1500)
    base = theta()
    out = {}
    for nm, f in (("no risk", 0.0), ("start", 1.0), ("x2", 2.0)):
        th = dict(base)
        for k in HAZ:
            th[k] = base[k] * f
        out[nm] = mean_assets(th, e, cfg)
    a0, a1, a2 = out["no risk"][0], out["start"][0], out["x2"][0]
    return report("2 precautionary buffer", 0 < a0 < a1 < a2,
                  "mean assets (thousand $) / share <= 0: " + ", ".join(f"{k} {v[0]:.2f} / {v[1]:.3f}"
                                                                         for k, v in out.items()))


if __name__ == "__main__":
    main()
