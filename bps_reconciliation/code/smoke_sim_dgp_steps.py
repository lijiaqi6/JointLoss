r"""Smoke test of the BPS harness with the Paper A model's wage process (WP1 of proposals/fable_10h_plan_paperA.md,
2026-10-20). Imports smoke_sim_dgp.py and keeps its couples, hours, job-loss spells, consumption, assets and
separation rules; only the hourly wage is replaced (earnings = hours x the new wage):

    log w_jm = mu_j(educ, age) + a_j + P_jm + u_jY        (m month, Y its calendar year)
    u_jY: one transitory draw per calendar year (model D6), (u_1, u_2) ~ N(0, [[0.0275, 0.0058], [0.0058, 0.0125]])
          (the model's sig_nu_h^2, sig_nu_w^2 and rho_nu 0.31, = BPS's published Table 3 transitory values)
    P_jm: human capital as discrete steps of psi_j log points (psi_h 0.4945, psi_w 0.4574, inputs/fixed_inputs.json),
          month by month as in the model (model.py own_step_matrix / innov_matrix, analytic start values):
            working month:      + psi_j with probability pi_up_j (h 0.00557, w 0.00695)   (accumulation)
            every month:        +- psi_j with probability p_eps_j / 2 each (h 0.00407, w 0.00905)
                                +- psi (same sign for both spouses) with probability p_c 0.00099 (shared innovation)
            displacement month: - psi_j with probability d_j (h 0.0696, w 0.0955)                (displacement loss)
            non-working month:  - psi_j with probability pi_dn_j (h 0.0290, w 0.0186)            (depreciation)
          i.e. a mean wage loss of about 9% for a displaced husband over a smoke spell (1-6 months, 10% 13-18).
Variant 'flat': the husband's hours are 2080 a year in every worked month (no hours variation apart from spells),
which makes the husband's log-hours variance small relative to his log-wage variance, as in the model panels.

Truth for BPS's Table 3: s_u1 0.0275, s_u2 0.0125, c_u1u2 0.0058; s_v = annual variance of the step sum of a
full-year worker, 12 [pi_up (1 - pi_up) + p_eps + p_c] psi^2; c_v1v2 = 12 p_c psi_h psi_w. Time aggregation of
monthly steps into annual wages adds +move_rate psi^2 / 6 to E(dw_t dw_{t-2}) (move_rate = steps per year in an
observed income year), so BPS's -E(dw_t dw_{t-2}) - s_me is expected at s_u - move_rate psi^2 / 6 (printed as
s_u1_ta, s_u2_ta).

Usage: python smoke_sim_dgp_steps.py <outdir> [n_couples] [--run] [--par 3]
   writes steps_{none,me,mix,flat_none,flat_me}.dta, steps_truth.json, steps_me_info.csv; with --run the Stata specs
   below through bps_on_sim_me.do (gmm9) and steps_results.json in <outdir>.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sim_panel_writer as spw  # noqa: E402
import smoke_sim_dgp as smoke  # noqa: E402

P = dict(psi_h=0.4945049867626991, psi_w=0.457409120420379, pi_up_h=0.005571509830074589,
         pi_up_w=0.006946687056807495, p_eps_h=0.004067533721235149, p_eps_w=0.009046461146481827,
         p_c=0.0009947341381433366, d_h=0.06962052823896311, d_w=0.0955477905273128, pi_dn_h=0.02895684667248854,
         pi_dn_w=0.018560571289512884, s_u1=0.0275, s_u2=0.0125, c_u1u2=0.0058)
# spec: (panel, BPS correction on?, jump trim, min-wage trim)
SPECS = {
    "S1_none_shipped": ("none", 0, 1, 1),
    "S2_none_notrim": ("none", 0, 0, 0),
    "S3_me_shipped": ("me", 1, 1, 1),
    "S4_mix_shipped": ("mix", 1, 1, 1),
    "S5_flat_me_shipped": ("flat_me", 1, 1, 1),
    "S6_flat_none_shipped": ("flat_none", 0, 1, 1),
}


def truth():
    t = {}
    for j, k in (("h", "1"), ("w", "2")):
        psi = P[f"psi_{j}"]
        t[f"s_v{k}"] = 12 * (P[f"pi_up_{j}"] * (1 - P[f"pi_up_{j}"]) + P[f"p_eps_{j}"] + P["p_c"]) * psi ** 2
    t["c_v1v2"] = 12 * P["p_c"] * P["psi_h"] * P["psi_w"]
    t.update(s_u1=P["s_u1"], s_u2=P["s_u2"], c_u1u2=P["c_u1u2"])
    t["rho_u1u2"] = t["c_u1u2"] / np.sqrt(t["s_u1"] * t["s_u2"])
    t["rho_v1v2"] = t["c_v1v2"] / np.sqrt(t["s_v1"] * t["s_v2"])
    return t


def add_steps(df, seed=2026, flat=False):
    """Replace the smoke wage by the model-like wage (docstring); returns the new monthly frame."""
    rng = np.random.default_rng(seed)
    df = df.sort_values(["couple_id", "year", "month"]).reset_index(drop=True)
    ids = df["couple_id"].to_numpy()
    n = ids.max()
    T = len(df) // n
    assert T * n == len(df)
    sh = lambda c: df[c].to_numpy().reshape(n, T)                     # noqa: E731
    yr = sh("year")
    y0 = yr.min()
    ny = yr.max() - y0 + 1
    U = rng.multivariate_normal([0, 0], [[P["s_u1"], P["c_u1u2"]], [P["c_u1u2"], P["s_u2"]]], size=(n, ny))
    yi = yr - y0
    shared = rng.random((n, T))
    shared_step = np.where(shared < P["p_c"] / 2, 1.0, np.where(shared < P["p_c"], -1.0, 0.0))
    out = {}
    moves = {}
    for j, hcol, dcol, ucol in (("h", "hours_h", "disp_h", 0), ("w", "hours_w", "disp_w", 1)):
        psi = P[f"psi_{j}"]
        hrs = sh(hcol)
        if j == "h" and flat:
            hrs = np.where(hrs > 0, 2080.0 / 12, 0.0)
            out["hours_h"] = hrs
        work = hrs > 0
        r1, r2, r3 = rng.random((n, T)), rng.random((n, T)), rng.random((n, T))
        up = work & (r1 < P[f"pi_up_{j}"])
        inn = np.where(r2 < P[f"p_eps_{j}"] / 2, 1.0, np.where(r2 < P[f"p_eps_{j}"], -1.0, 0.0))
        disp = sh(dcol) == 1
        dn = (disp & (r3 < P[f"d_{j}"])) | (~work & ~disp & (r3 < P[f"pi_dn_{j}"]))
        step = up.astype(float) + inn + shared_step - dn.astype(float)
        moves[j] = float(((step != 0) & work).sum() / work.sum() * 12)
        Pm = psi * np.cumsum(step, axis=1)
        u = U[:, :, ucol][np.arange(n)[:, None], yi]
        old = sh(f"wage_{j}")
        # keep the smoke's level (education, age profile, fixed effect, its permanent component at the start)
        base = np.log(old[:, :1]) + 0.0 * old                             # one constant per person
        age = sh(f"age_{j}")
        prof = (0.03 if j == "h" else 0.02) * (age - 40) - (0.0006 if j == "h" else 0.0005) * (age - 40) ** 2
        prof0 = prof[:, :1]
        w = np.exp(base - prof0 + prof + Pm + u)
        out[f"wage_{j}"] = w
        out[f"earn_{j}"] = hrs * w
    for c, v in out.items():
        df[c] = v.ravel()
    return df, moves


def raw_check(base):
    b = base[(base["marit"] == 1) & (base["seo"] == 0)].sort_values(["person", "year"]).copy()
    b["lw"] = np.log(b["ly"] / b["hours"].where(b["hours"] > 0))
    b["gap"] = b.groupby("person")["year"].diff()
    b["dlw"] = (b["lw"] - b.groupby("person")["lw"].shift(1)).where(b["gap"] == 2)
    b["dlw"] = b["dlw"] - b.groupby("year")["dlw"].transform("mean")
    b["dlw_l"] = b.groupby("person")["dlw"].shift(1).where(b["gap"] == 2)
    ok = b[["dlw", "dlw_l"]].notna().all(axis=1)
    x = b.loc[ok, "dlw"] * b.loc[ok, "dlw_l"]
    return dict(minus_E_dw_dwl=float(-x.mean()), se=float(x.std() / np.sqrt(len(x))), n=int(ok.sum()))


def main(outdir, n=10000, run=False, par=3):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    m = smoke.simulate(n)
    panels, info_all, rep = {}, [], {"params": P}
    for tag, flat in (("", False), ("flat_", True)):
        mm, moves = add_steps(m.copy(), flat=flat)
        base = spw.to_bps_panel(mm, seed=7)
        rep[f"{tag}moves_per_year"] = moves
        rep[f"{tag}raw_h_before_me"] = raw_check(base)
        rep[f"{tag}var_log_hours_h"] = float(np.log(base.loc[(base["hours"] > 0) & (base["marit"] == 1), "hours"]).var())
        panels[f"{tag}none"] = str(spw.write_bps_dta(base, out / f"steps_{tag}none.dta"))
        pA, infoA = spw.add_measurement_error(base, seed=11)
        panels[f"{tag}me"] = str(spw.write_bps_dta(pA, out / f"steps_{tag}me.dta"))
        info_all.append(infoA.assign(panel=f"{tag}me"))
        if not flat:
            pB, infoB = spw.add_measurement_error(base, gross_rate=0.01, gross_sd=0.7, seed=11)
            panels["mix"] = str(spw.write_bps_dta(pB, out / "steps_mix.dta"))
            info_all.append(infoB.assign(panel="mix"))
        print(tag or "base", "moves/yr", moves, "raw", rep[f"{tag}raw_h_before_me"], flush=True)
    info = pd.concat(info_all)
    info.to_csv(out / "steps_me_info.csv", index=False)
    t = truth()
    mv = rep["moves_per_year"]
    t["s_u1_ta"] = t["s_u1"] - mv["h"] * P["psi_h"] ** 2 / 6
    t["s_u2_ta"] = t["s_u2"] - mv["w"] * P["psi_w"] ** 2 / 6
    (out / "steps_truth.json").write_text(json.dumps(t, indent=1))
    hi = info[(info["spouse"] == "h") & info["panel"].isin(["me", "flat_me"])].copy()
    hi["shortfall"] = hi["target_var_e_w"] - hi["var_e_w"]
    rep["me_layer_h"] = {p: dict(shortfall=float(np.average(g["shortfall"], weights=g["n"])),
                                 target=float(np.average(g["target_var_e_w"], weights=g["n"])),
                                 clipped_groups=int(g["clipped"].sum()))
                         for p, g in hi.groupby("panel")}
    rep["truth"] = t
    print(json.dumps(rep, indent=1), flush=True)
    if run:
        sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "paperA_model"))
        from bps_trim_test import STATA, run_specs
        rep["bps"] = run_specs(SPECS, panels, str(out), STATA, par)
    (out / "steps_results.json").write_text(json.dumps(rep, indent=1, default=float))
    return rep


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    par = 3
    if "--par" in sys.argv:
        par = int(sys.argv[sys.argv.index("--par") + 1])
        args = [a for a in args if a != str(par)]
    main(args[0], int(args[1]) if len(args) > 1 else 10000, run="--run" in sys.argv, par=par)
