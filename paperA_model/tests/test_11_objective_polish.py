"""Check (11), estimation layer (2026-10-18 evening, Fable review Section 6):
 (a) objective trim: every moments.OBJ_EXCLUDE id is a target; excluded moments get zero weight under every weighting
     and do not count as missing; on a small simulation each pooled CPS moment equals the n-weighted average of its
     race-specific moments (the reason the pooled rows are duplicates in the model);
 (b) diag_noise weights equal 1 / (se^2 + sd_sim^2 x K_noise / K) for a noise file at K_noise = 3 and a run at K = 6;
 (c) Levenberg-Marquardt (estimate.lm_iterate) on a small nonlinear least-squares problem with a finite-difference
     Jacobian returns to the truth (Q < 1e-10, |z - z*| < 1e-5) from a distant start;
 (d) ties and the bound guard: --tie a=b makes b follow a and drops b from the free set; a start within 1% of a bound
     is refused;
 (e) the extensions nest: with c_mem = 0, eta_up = 0 and no borrowing wedge the Model arrays equal those built without
     the keys; c_mem > 0 changes only the configurations with one spouse non-employed and entitled; a wedge changes
     the terminal value only at negative assets and puts a grid node at 0; eta_up > 0 makes accumulation fall with the
     level; the CPS classification correction with Q = identity reproduces the uncorrected entry and exit rates."""
import argparse
import tempfile
from pathlib import Path

from _common import test_config, theta, entry, report
import numpy as np
import pandas as pd
import moments as M
import estimate as E
from simulate import simulate


def part_a():
    T = M.load_targets()
    ex = list(M.OBJ_EXCLUDE)
    ok_ids = all(k in set(T["id"]) for k in ex)
    zero = all((np.diag(M.weights(T, kind, exclude=ex))[T["id"].isin(ex).to_numpy()] == 0).all()
               for kind in ("diag", "block", "vcov"))
    W = M.weights(T, "diag", exclude=ex)
    m = T["value"].to_numpy(float).copy()
    m[T["id"].isin(ex).to_numpy()] = np.nan
    q, miss = M.objective(m, T, W)
    th = theta()
    res = simulate(th, test_config(), entry(1500, seed=5), K=1)
    out, N = M.compute(res, theta=th, merge_s12=False, return_n=True)
    dup = {}
    for pooled, parts in (("cps_wife_hazard_pooled", ("cps_wife_hazard_black", "cps_wife_hazard_white")),
                          ("cps_h_hazard_pooled", ("cps_h_hazard_B", "cps_h_hazard_W")),
                          ("cps_entry_pooled", ("cps_entry_black", "cps_entry_white"))):
        avg = sum(out[p] * N[p] for p in parts) / sum(N[p] for p in parts)
        dup[pooled] = abs(out[pooled] - avg)
    ok_dup = max(dup.values()) < 1e-12
    ok = ok_ids and zero and q == 0.0 and miss == 0 and ok_dup
    return ok, (f"(a) {len(ex)} excluded ids in targets {ok_ids}, zero weight {zero}, Q with excluded NaN {q} "
                f"(missing {miss}); pooled - n-weighted race average max {max(dup.values()):.1e}")


def part_b():
    T = M.load_targets()
    rng = np.random.default_rng(1)
    sd = rng.uniform(0.1, 2.0, len(T)) * T["se"].to_numpy(float)
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "noise.csv"
        pd.DataFrame(dict(id=T["id"], sim_sd=sd, K=3)).to_csv(p, index=False)
        W = M.weights(T, "diag_noise", exclude=list(M.OBJ_EXCLUDE), noise_file=p, K=6)
    se = T["se"].to_numpy(float)
    want = np.where(T["id"].isin(list(M.OBJ_EXCLUDE)).to_numpy(), 0.0, 1.0 / (se ** 2 + sd ** 2 * 3 / 6))
    err = float(np.max(np.abs(np.diag(W) - want) / np.maximum(want, 1e-300)))
    return err < 1e-12, f"(b) diag_noise weights max relative error {err:.1e}"


def part_c():
    zs = np.array([0.5, -1.0, 0.2])

    def mom(z):
        return np.array([z[0], z[1], z[0] * z[1], np.exp(0.3 * z[0]), z[2] + 0.1 * z[2] ** 3, z[1] * z[2], z[0] ** 2])

    tv = mom(zs)
    Wm = np.diag(np.array([1.0, 2.0, 0.5, 4.0, 1.0, 1.0, 0.0]))      # last moment outside the objective
    q = lambda z: float((mom(z) - tv) @ Wm @ (mom(z) - tv))          # noqa: E731

    def jac(z):
        h = 1e-6
        return mom(z), np.column_stack([(mom(z + h * e) - mom(z - h * e)) / (2 * h) for e in np.eye(3)])

    def batch(Zs):
        return [(q(z), mom(z)) for z in Zs]

    z0 = np.array([2.5, 1.5, -2.0])
    R = E.lm_iterate(z0, q(z0), mom(z0), jac, batch, tv, Wm, np.array([1e-3, 1e-2, 0.1, 1.0, 10.0]), iters=40,
                     ftol_abs=1e-14, ftol_rel=0.0, xtol=1e-10, log=lambda s: None)
    dz = float(np.max(np.abs(R["z"] - zs)))
    return R["Q"] < 1e-10 and dz < 1e-5, f"(c) LM from {z0.tolist()}: Q {R['Q']:.1e}, max |z - z*| {dz:.1e}, " \
                                         f"{R['iters']} iterations ({R['stop']})"


def part_d():
    ns = argparse.Namespace(fix=None, size="k_s2_era1_a20", free=None, free_set=None, free_extra=["sigma_eps"], ext={})
    E.setup_ties(["lam_h_B=lam_h_W"])
    idx, free = E.free_index(ns)
    th = E.dict_vec({**theta(), "sigma_eps": 0.05})
    th[E.NAMES.index("lam_h_B")] = 0.3
    th = E.apply_ties(th)
    ok_tie = "lam_h_W" not in free and "sigma_eps" in free and th[E.NAMES.index("lam_h_W")] == 0.3
    E.setup_ties([])
    th2 = th.copy()
    j = E.NAMES.index("kappa_S")
    th2[j] = E.HI[j] - 0.001 * (E.HI[j] - E.LO[j])
    try:
        E.check_start_bounds(th2, np.array([j]), 0.01)
        refused = False
    except SystemExit:
        refused = True
    return ok_tie and refused, f"(d) tie lam_h_B=lam_h_W and free sigma_eps {ok_tie}; start at 99.9% of the range " \
                               f"refused {refused}"


def part_e():
    from params import Config, load_fixed
    from model import Model
    cfg = Config(n_hc=5, n_assets=20, one_era=True, merge_s12=True)
    th = theta()
    th.pop("c_mem", None)
    th.pop("eta_up", None)
    fx = load_fixed()
    m0 = Model(th, cfg, 2, 1, 0, 1, fixed=fx)
    m1 = Model({**th, "c_mem": 0.0, "eta_up": 0.0}, cfg, 2, 1, 0, 1, fixed={**fx, "r_wedge": 0.0})
    same = all(np.array_equal(getattr(m0, k), getattr(m1, k)) for k in ("out_p", "Aw", "Ah", "VT", "agrid", "inc0"))
    mc = Model({**th, "c_mem": 2.0}, cfg, 2, 1, 0, 1, fixed=fx)
    chg = np.nonzero(np.abs(mc.out_p - m0.out_p).sum(axis=1) > 0)[0]
    lw, lh = mc.cfg_lw[chg], mc.cfg_lh[chg]
    ok_mem = len(chg) > 0 and bool(np.all(((lw == mc.E_) & (lh == 1)) | ((lh == 0) & (lw != mc.E_) & (lw != mc.N_))))
    mw = Model(th, cfg, 2, 1, 0, 1, fixed={**fx, "r_wedge": 0.006})
    m_nw = Model(th, cfg, 2, 1, 0, 1, fixed={**fx, "r_wedge": 1e-12})        # same grid (node at 0), no wedge
    neg = mw.agrid < 0
    ok_w = (0.0 in mw.agrid) and np.allclose(mw.VT[:, :, ~neg], m_nw.VT[:, :, ~neg]) and         bool(np.all(mw.VT[:, :, neg] <= m_nw.VT[:, :, neg] + 1e-12)) and bool(np.any(mw.VT[:, :, neg] < m_nw.VT[:, :, neg]))
    me = Model({**th, "eta_up": 1.0}, cfg, 2, 1, 0, 1, fixed=fx)
    up = np.array([me.Aw[0][h, min(h + 1, me.H - 1)] for h in range(me.H - 1)])
    ok_eta = bool(np.all(np.diff(up) < 0))
    import panels as PN
    from simulate import simulate
    res = simulate(th, test_config(), entry(400, seed=8), K=1)
    R = PN.records(res, theta=th, merge_s12=False)
    a = PN.cps_samples(R)
    b = PN.cps_samples(R, classif=np.eye(3))
    ex_a, ex_b = a["exit"]["y"].mean(), np.average(b["exit"]["y"], weights=b["exit"]["wt"])
    en_a, en_b = a["entry"]["y"].mean(), np.average(b["entry"]["y"], weights=b["entry"]["wt"])
    ok_cl = abs(ex_a - ex_b) < 1e-12 and abs(en_a - en_b) < 1e-12
    ok = same and ok_mem and ok_w and ok_eta and ok_cl
    return ok, (f"(e) nested arrays equal {same}; memory changes {len(chg)} configurations, all with one spouse "
                f"non-employed and entitled {ok_mem}; wedge: node at 0, terminal value lower only at negative assets {ok_w}; accumulation falls with the level "
                f"{ok_eta}; classification with Q = I exit {ex_a:.5f} / {ex_b:.5f}, entry {en_a:.5f} / {en_b:.5f}")


def main():
    res = [part_a(), part_b(), part_c(), part_d(), part_e()]
    return report("11 objective trim, weights, LM polish, ties", all(r[0] for r in res), "; ".join(r[1] for r in res))


if __name__ == "__main__":
    main()
