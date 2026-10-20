"""Paper A model: BPS (2016) estimator on simulated couples (check (7) of the identification plan) and the one-time
wage-process correction (plan Section 1.2). Validation, not a target: the SMM objective does not use it.

Steps (bps_reconciliation/HARNESS.md):
 1. simulate the model at --start (default: the analytic start values), built exactly as 'estimate.py evaluate --start
    <start>' builds it (post_common.setup: estimate._init_worker and start_theta, i.e. EXT_DEFAULTS or the run's
    run.json extensions, the borrowing wedge r_wedge, --set-fixed entries, the extras as fixed inputs, the run's size
    and CRN seed), the entry couples x K;
 2. write the simulated monthly couple histories of calendar years 1995-2009 (income years 1998-2008 = PSID waves
    1999-2009, the years bps_on_sim.do accepts; the model's own calendar years, all in the 1997-2008 policy schedule
    when one era is used) in sim_panel_writer's schema: hours and earnings by month (2000 $), status (1 working; a
    non-employed spouse 3 = looking (simulate's classification; husbands always) or 6 = out of the labor force),
    consumption and assets, children under 18 (fixed_inputs n_children by bucket, wife's age group and race), married,
    displacement flags, SNAP / EITC / UI as extras; husband's age = wife's age + 2; education from the entry file
    (years, h_educ / w_educ) when present, else 12 years;
 3. sim_panel_writer.to_bps_panel -> add_measurement_error (BPS's Bound et al. shares, consumption error 0.0332, and the
    gross-error mixture --gross-rate / --gross-sd) -> write_bps_dta into a work folder outside the repository
    (--work, default %TEMP%/paperA_bps);
 4. run bps_on_sim.do in Stata batch (--stata) and read BPS Table 3 (all ages) from bps_on_sim_row.csv: hat Var_perm,j
    (T3_s_v1 husband, T3_s_v2 wife), hat Cov_perm (T3_c_v1v2), hat Var_trans,j (T3_s_u1, T3_s_u2), hat Cov_trans;
 5. the correction (plan Section 1.2; lead decision: also rescale the permanent probabilities):
        sigma_nu,j^2 (new) = max{0.5 sigma_nu,j^2(BPS), 2 sigma_nu,j^2(BPS) - hat Var_trans,j}
        p_eps_j (new)      = p_eps_j x Var_perm,j(BPS) / hat Var_perm,j
        p_c (new)          = p_c x Cov_perm(BPS) / hat Cov_perm
    printed always; written into inputs/wage_process.json (with the before / after values and the BPS numbers) only
    with --apply (one pass: the plan says once).
 --apply-from <bps_trim.json> [--trim-spec F_none_shipped]: the same rule on the Table 3 numbers of one spec of
    bps_trim_test.py (2026-10-20, INTAKE 2b: the clean spec, no measurement error in the data and BPS's correction off,
    because the harness's error layer cannot draw the husband's wage error at its target); no simulation, no Stata.
 --sigma-nu-zero: check (7) proper: the same run with the transitory shocks switched off (sigma_nu = 0); the BPS
    transitory variance then comes only from displacement, within-year human capital moves and the measurement error.
Outputs: results/bps_<stamp>/bps_check.json (aggregate numbers only; the simulated panel stays in the work folder).
Run: .venv/Scripts/python.exe paperA_model/bps_check.py [--apply] [--sigma-nu-zero] [--K 3]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
BPS_CODE = HERE.parent / "bps_reconciliation" / "code"
sys.path.insert(0, str(BPS_CODE))
STATA = os.environ.get("STATA_EXE", r"C:\Program Files\StataNow19\StataMP-64.exe")  # Mac: export STATA_EXE
BPS_T3 = {"s_v1": 0.0303, "s_v2": 0.0382, "c_v1v2": 0.0027, "s_u1": 0.0275, "s_u2": 0.0125, "c_u1u2": 0.0058}


def monthly_panel(res, cfg, fx, y0=1995, y1=2009):
    """Simulated records -> sim_panel_writer input schema (one row per couple-copy x month of y0..y1)."""
    from simulate import FIELDS_I, M0
    gi = lambda nm: res.I[FIELDS_I.index(nm)]                         # noqa: E731
    ent = res.info["entry"]
    m0, m1 = 12 * (y0 - M0), 12 * (y1 - M0 + 1)
    st = gi("status")[:, m0:m1].astype(int)
    keep = (st >= 0).any(axis=1)
    idx = np.nonzero(keep)[0]
    st = st[idx]
    n, T = st.shape
    sl = lambda A: A[idx, m0:m1]                                      # noqa: E731
    lw, lh, hrs_w, hrs_h = sl(gi("lw")), sl(gi("lh")), sl(gi("hrs_w")), sl(gi("hrs_h"))
    look = sl(gi("look"))
    H = np.array([0.0, fx["H_P"], fx["H_F"]])
    mar = st == 1
    ww = mar & (lw == 0) & (hrs_w > 0)
    wh = mar & (lh == 0)
    months = np.arange(m0, m1)
    m_off = np.asarray(res.info["m_off"])[idx]
    age_w = 25 + (months[None, :] - m_off[:, None]) / 12.0
    race = ent["race"].to_numpy()[idx]
    rcode = np.where(race == 1, 1, 2)
    k = sl(gi("k")).astype(int)
    g = np.clip(((age_w - 25) // 5).astype(int), 0, 6)
    nch = {r: np.array(fx["n_children"]["BW"[r]]) for r in (0, 1)}
    kids = np.zeros((n, T), int)
    for r in (0, 1):
        sel = race == r
        kids[sel] = nch[r][np.clip(k[sel], 0, 2), g[sel]]
    educ = lambda col: (ent[col].fillna(12).to_numpy()[idx] if col in ent else np.full(n, 12.0))   # noqa: E731
    F = lambda nm: sl(res.F[["c", "a", "yw", "yh", "bw", "bh", "eitc", "snap", "tr"].index(nm)])  # noqa: E731
    emp_w = np.where(ww, 1, np.where(look == 1, 3, 6))
    emp_h = np.where(wh, 1, 3)
    df = pd.DataFrame({
        "couple_id": np.repeat(res.info["uid"][idx] + 1, T), "year": np.tile(1984 + months // 12, n),
        "month": np.tile(months % 12 + 1, n), "age_w": age_w.ravel(), "age_h": (age_w + 2).ravel(),
        "race_h": np.repeat(rcode, T), "race_w": np.repeat(rcode, T),
        "educ_h": np.repeat(educ("h_educ"), T), "educ_w": np.repeat(educ("w_educ"), T),
        "hours_h": np.where(wh, H[np.clip(hrs_h, 0, 2)], 0.0).ravel(),
        "hours_w": np.where(ww, H[np.clip(hrs_w, 0, 2)], 0.0).ravel(),
        "earn_h": (np.where(wh, F("yh"), 0.0) * 1000).ravel(), "earn_w": (np.where(ww, F("yw"), 0.0) * 1000).ravel(),
        "emp_h": emp_h.ravel(), "emp_w": emp_w.ravel(), "cons": (F("c") * 1000).ravel(),
        "assets": (F("a") * 1000).ravel(), "kids": kids.ravel(), "married": mar.ravel().astype(int),
        "disp_h": (sl(gi("disp_h")) == 1).ravel().astype(int), "disp_w": (sl(gi("disp_w")) == 1).ravel().astype(int),
        "snap": (F("snap") * 1000).ravel(), "eitc": (F("eitc") * 1000).ravel(), "ui_h": (F("bh") * 1000).ravel(),
        "ui_w": (F("bw") * 1000).ravel()})
    return df[np.repeat(st >= 0, 1).ravel()]


def run_stata(dta, work, spec, stata):
    caller = Path(work) / f"caller_{spec}.do"
    caller.write_text("\n".join([f'global INPUT "{dta}"', f'global SPEC "{spec}"', f'global WORK "{work}"',
                                 f'global RESULTS "{work}\\bps_on_sim_results_{spec}.csv"',
                                 f'do "{BPS_CODE / "bps_on_sim.do"}"', ""]))
    t0 = time.time()
    subprocess.run([stata, "/e" if os.name == "nt" else "-b", "do", str(caller)], cwd=work, check=False)
    row = Path(work) / spec / "bps_on_sim_row.csv"
    if not row.exists():
        raise RuntimeError(f"bps_on_sim.do produced no {row} (see the Stata log in {work})")
    r = pd.read_csv(row).iloc[0].to_dict()
    r["stata_minutes"] = (time.time() - t0) / 60
    return r


def correction(wp, est):
    """Plan Section 1.2 one-time correction of the wage process from BPS's estimates on the simulated panel."""
    new = dict(wp)
    for j, su, sv in (("w", "s_u2", "s_v2"), ("h", "s_u1", "s_v1")):
        s2 = BPS_T3[su]
        new[f"sig_nu_{j}"] = float(np.sqrt(max(0.5 * s2, 2 * s2 - est[f"T3_{su}"])))
        new[f"p_eps_{j}"] = float(wp[f"p_eps_{j}"] * BPS_T3[sv] / est[f"T3_{sv}"])
    new["p_c"] = float(wp["p_c"] * BPS_T3["c_v1v2"] / est["T3_c_v1v2"]) if est["T3_c_v1v2"] > 0 else wp["p_c"]
    return new


def apply_from(path, spec, inputs):
    """The correction on one spec of a bps_trim_test.py run, written into inputs/wage_process.json."""
    tr = json.loads(Path(path).read_text())
    est = tr["bps"][spec]
    wp = json.loads((inputs / "wage_process.json").read_text())
    if "bps_correction" in wp:
        raise SystemExit("inputs/wage_process.json already carries a bps_correction (the plan applies it once)")
    base = {k: wp[k] for k in ("p_c", "p_eps_w", "p_eps_h", "sig_nu_w", "sig_nu_h", "rho_nu")}
    new = correction(base, est)
    wp.update(new)
    wp["bps_correction"] = dict(date=datetime.now().isoformat(), before=base, source=str(Path(path).as_posix()),
                                spec=spec, start=tr.get("start"), K=tr.get("K"),
                                bps_on_sim={k: float(v) for k, v in est.items() if k.startswith("T3_")},
                                bps_published=BPS_T3, rule="plan Section 1.2: sigma^2 = max(0.5 s2, 2 s2 - hat); p_eps, "
                                "p_c rescaled by target / recovered permanent (co)variance")
    wp["status"] = (f"closed forms + one-time BPS-harness correction on bps_trim_test spec {spec} "
                    f"(bps_check.py --apply-from)")
    (inputs / "wage_process.json").write_text(json.dumps(wp, indent=1))
    print(json.dumps(dict(before=base, after=new), indent=1))
    print("inputs/wage_process.json updated")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--start", default=None, help="best.json / mean.json or a run folder (default: analytic start)")
    ap.add_argument("--K", type=int, default=3)
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--gross-rate", dest="gross_rate", type=float, default=0.01)
    ap.add_argument("--gross-sd", dest="gross_sd", type=float, default=0.7)
    ap.add_argument("--work", default=str(Path(tempfile.gettempdir()) / "paperA_bps"))
    ap.add_argument("--stata", default=STATA)
    ap.add_argument("--sigma-nu-zero", dest="nu0", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--no-stata", dest="no_stata", action="store_true", help="write the panel only")
    ap.add_argument("--apply-from", dest="apply_from", default=None, help="bps_trim.json of bps_trim_test.py")
    ap.add_argument("--trim-spec", dest="trim_spec", default="F_none_shipped")
    a = ap.parse_args()
    t_all = time.time()
    from params import INPUTS
    if a.apply_from:
        apply_from(a.apply_from, a.trim_spec, INPUTS)
        return
    import post_common as pc
    import sim_panel_writer as spw
    # the estimated model exactly as 'estimate.py evaluate --start <start>' builds it (post_common.setup ->
    # estimate._init_worker / start_theta): extensions (EXT_DEFAULTS or the run's run.json, incl. the borrowing
    # wedge r_wedge), --set-fixed entries, the extras as fixed inputs, size and CRN seed
    ctx = pc.setup(a.start, K=a.K, threads=a.threads)
    fx = ctx.E._W["fx"]
    ov = {"sig_nu_w": 0.0, "sig_nu_h": 0.0} if a.nu0 else None
    t0 = time.time()
    res, th, fx_sim = pc.simulate_only(ctx, overrides=ov)
    t_sim = time.time() - t0
    mp = monthly_panel(res, ctx.E._W["cfg"], fx)
    del res
    work = Path(a.work)
    work.mkdir(parents=True, exist_ok=True)
    spec = ("paperA_nu0" if a.nu0 else "paperA_base") + f"_K{a.K}"
    panel = spw.to_bps_panel(mp, seed=7, educ_in_years=True)       # entry-file education is in years
    panel, info = spw.add_measurement_error(panel, gross_rate=a.gross_rate, gross_sd=a.gross_sd, seed=11)
    dta = spw.write_bps_dta(panel, work / f"{spec}.dta")
    print(f"BPS panel: {len(panel):,} head-waves from {mp['couple_id'].nunique():,} couples ({time.time() - t0:.0f}s) "
          f"-> {dta}", flush=True)
    out = HERE / "results" / f"bps_{datetime.now():%Y%m%d_%H%M%S}"
    out.mkdir(parents=True, exist_ok=True)
    rep = dict(spec=spec, start=a.start or "analytic start (inputs/start_analytic.json)", K=a.K,
               size=ctx.spec["size"], seed=ctx.spec["seed"], ext=ctx.spec["ext"], set_fixed=ctx.spec["set_fixed"],
               r_wedge=float(fx_sim.get("r_wedge", 0.0)), entry_source=ctx.E._W["entry_src"], notes=ctx.notes,
               rows=len(panel), couples=int(mp["couple_id"].nunique()), gross_rate=a.gross_rate,
               gross_sd=a.gross_sd, sigma_nu_zero=a.nu0, simulate_seconds=t_sim, bps_published=BPS_T3)
    if not a.no_stata:
        est = run_stata(str(dta), str(work), spec, a.stata)
        keys = ["T3_s_u1", "T3_s_v1", "T3_s_u2", "T3_s_v2", "T3_c_u1u2", "T3_c_v1v2", "rho_u1u2", "rho_v1v2",
                "N_input", "N_sample", "N_duw", "N_duww", "N_gmm", "n_hd", "n_wd", "n_jd", "n_trim_minw",
                "n_trim_jump", "E_pi", "E_s", "s_omega", "M_h2v1", "M_cv1", "ch_tot", "ch_gov", "ch_fam", "ch_sav",
                "beta", "stata_minutes"]
        keys += [f"T3_{c}_se" for c in BPS_T3]
        rep["bps_on_sim"] = {k: float(est[k]) for k in keys if k in est}
        rep["table3_vs_published"] = {c: dict(sim=float(est.get(f"T3_{c}", np.nan)),
                                              se=float(est.get(f"T3_{c}_se", np.nan)), bps=BPS_T3[c])
                                      for c in BPS_T3}
        rep["total_minutes"] = (time.time() - t_all) / 60
        wp = json.loads((INPUTS / "wage_process.json").read_text())
        base = {k: wp[k] for k in ("p_c", "p_eps_w", "p_eps_h", "sig_nu_w", "sig_nu_h", "rho_nu")}
        new = correction(base, est)
        rep["wage_process_before"], rep["wage_process_after"] = base, new
        print(json.dumps(rep, indent=1))
        if a.apply and not a.nu0:
            wp.update(new)
            wp["bps_correction"] = dict(date=datetime.now().isoformat(), before=base, bps_on_sim=rep["bps_on_sim"],
                                        bps_published=BPS_T3, rule="plan Section 1.2: sigma^2 = max(0.5 s2, 2 s2 - "
                                        "hat); p_eps, p_c rescaled by target / recovered permanent (co)variance")
            wp["status"] = "closed forms + one-time BPS-harness correction (bps_check.py --apply)"
            (INPUTS / "wage_process.json").write_text(json.dumps(wp, indent=1))
            print("inputs/wage_process.json updated")
    (out / "bps_check.json").write_text(json.dumps(rep, indent=1, default=float))
    print(f"-> {out}")


if __name__ == "__main__":
    main()
