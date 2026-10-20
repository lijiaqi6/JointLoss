"""Check (13), 2026-10-20 (results/reestimate_plan_20261020.md):
 (a) 'block' weighting is scale-free: rescaling one moment's units (value, se and simulation sd x 1000) leaves every
     z-unit weight w_i se_i^2 unchanged, and each block's total z-unit weight sum_b w_i (se_i^2 + var_sim,i) is N / B;
 (b) the decorrelation overrides (counterfactual (i)) keep each spouse's marginal monthly hazard: 'indep' with
     tau = tau_w + 2 tau_h gives dw / dh equal to the base marginal pi_c + (1 - pi_c) m delta of that spouse's type,
     pi_c = 0, and the separated wife's hazard equal to the base m delta; 'mean' gives pi_c + (1 - pi_c) E[m] delta;
 (c) simulation (test size, 1,500 couples): 'indep' draws four types, each spouse's displacement rate per married
     working month stays within 10% of the base, and same-month joint displacements fall."""
import tempfile
from pathlib import Path

from _common import test_config, theta, entry, report
import numpy as np
import pandas as pd
import moments as M


def part_a():
    T = M.load_targets()
    ex = list(M.OBJ_EXCLUDE)
    rng = np.random.default_rng(3)
    sd = rng.uniform(0.1, 1.0, len(T)) * T["se"].to_numpy(float)
    j = int(np.nonzero(~T["id"].isin(ex).to_numpy())[0][5])
    T2 = T.copy()
    T2.loc[j, ["value", "se"]] *= 1000.0
    sd2 = sd.copy()
    sd2[j] *= 1000.0
    with tempfile.TemporaryDirectory() as d:
        p1, p2 = Path(d) / "n1.csv", Path(d) / "n2.csv"
        pd.DataFrame(dict(id=T["id"], sim_sd=sd, K=3)).to_csv(p1, index=False)
        pd.DataFrame(dict(id=T["id"], sim_sd=sd2, K=3)).to_csv(p2, index=False)
        w1 = np.diag(M.weights(T, "block", exclude=ex, noise_file=p1, K=3))
        w2 = np.diag(M.weights(T2, "block", exclude=ex, noise_file=p2, K=3))
    se1, se2 = T["se"].to_numpy(float), T2["se"].to_numpy(float)
    err = float(np.max(np.abs(w1 * se1 ** 2 - w2 * se2 ** 2)))
    keep = w1 > 0
    zt = pd.Series(w1 * (se1 ** 2 + sd ** 2), index=T["block"])[keep].groupby(level=0).sum()
    want = keep.sum() / len(zt)
    err_b = float(np.max(np.abs(zt - want)))
    ok = err < 1e-12 and err_b < 1e-9
    return ok, f"(a) block weights: z-unit change after rescaling {T['id'][j]} x1000 {err:.1e}; block totals vs N/B " \
               f"= {want:.2f}: max error {err_b:.1e}"


def part_b():
    from params import Config, load_fixed
    from model import Model
    cfg = Config(n_hc=5, n_assets=20, one_era=True, merge_s12=True)
    th = theta(p_H=0.05, m_H=8.0, pi_c1=0.002)
    fx = load_fixed()
    r, s = 0, 1
    base = {tau: Model(th, cfg, 2, r, s, tau, fixed=fx) for tau in (0, 1)}
    marg = {tau: (m.pic + (1 - m.pic) * m.dw, m.pic + (1 - m.pic) * m.dh) for tau, m in base.items()}
    errs = []
    for tw in (0, 1):
        for thh in (0, 1):
            m = Model(th, cfg, 2, r, s, tw + 2 * thh, fixed=fx, overrides={"decorr": "indep"})
            errs += [abs(m.dw - marg[tw][0]), abs(m.dh - marg[thh][1]), m.pic, abs(m.dw_S - base[tw].dw)]
    mm = Model(th, cfg, 2, r, s, 0, fixed=fx, overrides={"decorr": "mean"})
    Em = 1 + th["p_H"] * (th["m_H"] - 1)
    pic = base[0].pic
    errs += [abs(mm.dw - (pic + (1 - pic) * Em * th["delta_w_B"])), abs(mm.dh - (pic + (1 - pic) * Em * th["delta_h_B"])),
             mm.pic]
    e = float(max(errs))
    return e < 1e-15, f"(b) decorrelation hazards: max deviation from the base marginals {e:.1e}"


def rates(res):
    from simulate import FIELDS_I
    I = lambda nm: res.I[FIELDS_I.index(nm)]                         # noqa: E731
    mar = I("status") == 1
    ww = mar & (I("lw") == 0) & (I("hrs_w") > 0)
    wh = mar & (I("lh") == 0) & (I("hrs_h") > 0)
    dh = (I("disp_h") == 1) & mar
    dw = (I("disp_w") == 1) & mar
    return dh.sum() / wh.sum(), dw.sum() / ww.sum(), int((dh & dw).sum())


def part_c():
    from simulate import simulate
    th = theta(p_H=0.05, m_H=8.0)
    ent = entry(1500, seed=13)
    r0 = simulate(th, test_config(), ent, K=1)
    r1 = simulate(th, test_config(), ent, K=1, overrides={"decorr": "indep"})
    types = sorted(np.unique(r1.info["tau"]).tolist())
    (h0, w0, j0), (h1, w1, j1) = rates(r0), rates(r1)
    ok = types == [0, 1, 2, 3] and abs(h1 / h0 - 1) < 0.10 and abs(w1 / w0 - 1) < 0.10 and j1 < j0
    return ok, (f"(c) indep types {types}; his rate {h0:.5f} -> {h1:.5f}, hers {w0:.5f} -> {w1:.5f}; same-month joint "
                f"displacements {j0} -> {j1}")


def main():
    res = [part_a(), part_b(), part_c()]
    return report("13 scale-free block weights, decorrelation counterfactual", all(r[0] for r in res),
                  "; ".join(r[1] for r in res))


if __name__ == "__main__":
    main()
