"""Diagnostics A and B of results/diagnostics_20261018.md (2026-10-18): Q and selected moments at the analytic start
(trimmed objective, diag_noise weights, default size, K 3, seed 20261018) under
  A. sigma_eps in {0.05, 0.10, 0.20, 0.30} (the other values at the analytic start);
  B. the (p_H, m_H) ridge p(1-p)(m-1)^2 = (kappa-1)(1+p(m-1))^2 with kappa - 1 = 2.5965 (CPS leads/lags) at p_H in
     {0.03, 0.05, 0.10, 0.15, 0.20, 0.25}, and m_H in {4, 8, 12.6, 18} at p_H = 0.10; in both, delta_w and delta_h are
     rescaled by E m(start) / E m(new) so that the base hazards (E m) delta stay at the start's values; pi_c unchanged.
Run from the repo root: .venv/Scripts/python.exe IGE/paperA_model/results/diagnostics_20261018/profile_sigma_ridge.py
Writes moments_by_variant.csv, q_by_block_by_variant.csv, variants.csv here (aggregate numbers only)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import estimate as E  # noqa: E402
from analytic_start import ridge_m  # noqa: E402

KAP1 = 2.5965003601004977          # inputs/start_analytic.json check_section_1_4 kappa_minus_1_cps


def main():
    args = E.build_parser().parse_args(["evaluate", "--workers", "6", "--threads", "2"])
    E.resolve(args)
    base = E.start_theta(args)
    ix = {n: E.NAMES.index(n) for n in E.NAMES}
    p0, m0 = base[ix["p_H"]], base[ix["m_H"]]
    Em0 = 1 + p0 * (m0 - 1)
    variants = [("start", base.copy(), "A,B")]
    for s in (0.10, 0.20, 0.30):
        th = base.copy()
        th[ix["sigma_eps"]] = s
        variants.append((f"sigma_eps={s:.2f}", th, "A"))

    def hm(p, m):
        th = base.copy()
        Em = 1 + p * (m - 1)
        th[ix["p_H"]], th[ix["m_H"]] = p, m
        for n in ("delta_w_B", "delta_w_W", "delta_h_B", "delta_h_W"):
            th[ix[n]] = base[ix[n]] * Em0 / Em
        return th

    for p in (0.03, 0.05, 0.15, 0.20, 0.25):
        variants.append((f"ridge p_H={p:.2f}", hm(p, ridge_m(p, KAP1)), "B"))
    for m in (4.0, 8.0, 18.0):
        variants.append((f"p_H=0.10 m_H={m:g}", hm(p0, m), "B"))
    spec = E.spec_of(args)
    pool = E._pool(args, spec, warm=base)
    try:
        res = [pool.warm_result] + pool.map([v[1] for v in variants[1:]])
    finally:
        pool.close()
    T, W = E._W["targets"], E._W["W"]
    w = np.diag(W)
    mom = pd.DataFrame({"id": T["id"], "block": T["block"], "data": T["value"], "se": T["se"], "in_objective": w > 0})
    qb, rows = {}, []
    for (name, th, grp), r in zip(variants, res):
        mom[name] = r[4]
        qb[name] = E.block_table(r[4], T, W)["sum"]
        rows.append(dict(variant=name, group=grp, Q=r[0], missing=r[1], seconds=r[2], p_H=th[ix["p_H"]],
                         m_H=th[ix["m_H"]], sigma_eps=th[ix["sigma_eps"]], delta_w_W=th[ix["delta_w_W"]],
                         delta_h_W=th[ix["delta_h_W"]], kappa_minus_1=th[ix["p_H"]] * (1 - th[ix["p_H"]]) *
                         (th[ix["m_H"]] - 1) ** 2 / (1 + th[ix["p_H"]] * (th[ix["m_H"]] - 1)) ** 2))
    mom.to_csv(HERE / "moments_by_variant.csv", index=False)
    pd.DataFrame(qb).to_csv(HERE / "q_by_block_by_variant.csv")
    V = pd.DataFrame(rows)
    V.to_csv(HERE / "variants.csv", index=False)
    pd.set_option("display.width", 250)
    print(V.to_string())
    print(pd.DataFrame(qb).round(1).to_string())


if __name__ == "__main__":
    main()
