"""WP1 (proposals/fable_10h_plan_paperA.md, 2026-10-20): is the BPS deficit in the husband's transitory variance
(BPS's estimator on the simulated panel: 0.006 at K = 1, 0.013 at K = 3, against the model input sig_nu_h^2 = 0.0275)
an artefact of the harness (BPS's trims, the measurement-error layer and BPS's correction for it) or real?

Read only on the model path: builds the model exactly as bps_check.py (post_common.setup at the analytic start,
simulate_only, bps_check.monthly_panel), never writes inputs/ (no --apply). Panels and Stata files stay in --work
(outside the repository); the repo gets results/bps_trim_<stamp>/bps_trim.json (aggregates only).

Steps
 1. simulate K copies at --start (default analytic start); optionally a second simulation with sig_nu = 0 (--nu0);
 2. direct decomposition on the simulated records (no measurement error, no trims, no residual regressions): the
    husband's annual log wage of income years 1998-2008 (BPS's wage: annual earnings / annual hours) split exactly into
    the human capital part (hours-weighted mean of psi_h x level within the year) and the transitory part (one draw per
    calendar year, D6); biennial differences demeaned by year; -E(dw_t dw_{t-2}) and its parts;
 3. the measurement-error layer of the harness (sim_panel_writer.add_measurement_error): the wage error it actually
    draws (var e_y + var e_h - 2 cov) against the Bound et al. target 0.13 x var(measured log wage) that BPS's
    correction subtracts (variance_estimation.do), by spouse x age group (clipping of cov(e_y, e_h));
 4. bps_on_sim_me.do (= bps_on_sim.do + the OVRX hook; ovr_me0.do switches BPS's correction off) on the panels under
    the switch sets of SPECS, gmm9 only (BPS Table 3, all ages), up to --par Stata instances in parallel.
Run: .venv/Scripts/python.exe paperA_model/bps_trim_test.py [--K 3] [--nu0] [--par 3]
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
KEYS = ["T3_s_u1", "T3_s_v1", "T3_s_u2", "T3_s_v2", "T3_c_u1u2", "T3_c_v1v2", "T3_s_u1_se", "T3_s_v1_se",
        "T3_s_u2_se", "T3_s_v2_se", "T3_c_u1u2_se", "T3_c_v1v2_se", "N_sample", "N_duw", "N_duww", "n_trim_minw",
        "n_trim_minw_disp", "n_trim_jump", "n_trim_jump_disp", "n_hd", "n_wd"]
# spec: (panel, BPS correction on?, jump trim, min-wage trim)
SPECS = {
    "A_mix_shipped": ("mix", 1, 1, 1),      # = bps_check.py (Bound et al. + gross errors 1% x 0.7), BPS as shipped
    "B_mix_nojump": ("mix", 1, 0, 1),
    "C_mix_notrim": ("mix", 1, 0, 0),
    "D_me_shipped": ("me", 1, 1, 1),        # Bound et al. shares only (no gross errors)
    "E_me_nojump": ("me", 1, 0, 1),
    "F_none_shipped": ("none", 0, 1, 1),    # no measurement error in the data and BPS's correction off
    "G_none_nojump": ("none", 0, 0, 1),
    "H_none_notrim": ("none", 0, 0, 0),
}
SPECS_NU0 = {"N_none_shipped": ("none_nu0", 0, 1, 1), "O_none_notrim": ("none_nu0", 0, 0, 0)}


def wage_decomposition(res, fx, y_lo=1998, y_hi=2008):
    """Exact split of the husband's (and wife's) annual log wage on the records; BPS-style raw biennial moments."""
    from simulate import FIELDS_I, M0
    gi = lambda nm: res.I[FIELDS_I.index(nm)]                         # noqa: E731
    H = np.array([0.0, fx["H_P"], fx["H_F"]])
    out = {"m_off_mod12_zero_share": float(np.mean(np.asarray(res.info["m_off"]) % 12 == 0))}
    years = list(range(y_lo, y_hi + 1, 2))
    for sp, lv, hv, yv, psi in (("h", "lh", "hrs_h", "yh", fx["psi_h"]), ("w", "lw", "hrs_w", "yw", fx["psi_w"])):
        rows = {}
        for Y in years:
            m0, m1 = 12 * (Y - M0), 12 * (Y - M0 + 1)
            st = gi("status")[:, m0:m1].astype(int)
            work = (st == 1) & (gi(lv)[:, m0:m1] == 0)
            hrs = np.where(work, H[np.clip(gi(hv)[:, m0:m1], 0, 2)], 0.0)
            y = np.where(work, res.F[["c", "a", "yw", "yh"].index(yv)][:, m0:m1], 0.0)
            lev = gi("hh" if sp == "h" else "hw")[:, m0:m1].astype(float)
            sh, sy = hrs.sum(1), y.sum(1)
            ok = (st == 1).all(1) & (sh > 0) & (sy > 0)
            with np.errstate(divide="ignore", invalid="ignore"):
                lw = np.log(sy / sh)
                hc = np.log((hrs * np.exp(psi * lev)).sum(1) / sh)
            rows[Y] = (np.where(ok, lw, np.nan), np.where(ok, hc, np.nan), sh, (hrs > 0).sum(1))
        d = {}
        for Y in years[1:]:
            lw1, hc1 = rows[Y][0], rows[Y][1]
            lw0, hc0 = rows[Y - 2][0], rows[Y - 2][1]
            dw, dh = lw1 - lw0, hc1 - hc0
            dw = dw - np.nanmean(dw)
            dh = dh - np.nanmean(dh)
            d[Y] = (dw, dh, dw - dh)
        acc = {k: [] for k in ("dw2", "dwl", "dhl", "dnl", "x1", "x2", "dh2", "dn2")}
        for Y in years[2:]:
            dw, dh, dn = d[Y]
            dwl, dhl, dnl = d[Y - 2]
            ok = np.isfinite(dw) & np.isfinite(dwl)
            acc["dwl"].append(dw[ok] * dwl[ok])
            acc["dhl"].append(dh[ok] * dhl[ok])
            acc["dnl"].append(dn[ok] * dnl[ok])
            acc["x1"].append(dh[ok] * dnl[ok])
            acc["x2"].append(dn[ok] * dhl[ok])
        for Y in years[1:]:
            dw, dh, dn = d[Y]
            ok = np.isfinite(dw)
            acc["dw2"].append(dw[ok] ** 2)
            acc["dh2"].append(dh[ok] ** 2)
            acc["dn2"].append(dn[ok] ** 2)
        m = {k: float(np.mean(np.concatenate(v))) for k, v in acc.items()}
        n_l = int(sum(len(v) for v in acc["dwl"]))
        se = float(np.std(np.concatenate(acc["dwl"])) / np.sqrt(n_l))
        # move rate of the human capital level among full-year workers (months with a level change / months)
        mv = []
        for Y in years:
            m0, m1 = 12 * (Y - M0), 12 * (Y - M0 + 1)
            lev = gi("hh" if sp == "h" else "hw")[:, m0 - 1:m1].astype(int)
            st = gi("status")[:, m0 - 1:m1].astype(int)
            ok = (st[:, 1:] == 1) & (st[:, :-1] == 1)
            mv.append(((np.diff(lev, axis=1) != 0) & ok).sum() / max(ok.sum(), 1))
        out[sp] = dict(
            n_pairs=n_l, minus_E_dw_dwl=-m["dwl"], minus_E_dw_dwl_se=se, minus_E_dhc_dhcl=-m["dhl"],
            minus_E_dnu_dnul=-m["dnl"], minus_cross=-(m["x1"] + m["x2"]), E_dw2_half=m["dw2"] / 2,
            E_dhc2_half=m["dh2"] / 2, E_dnu2_half=m["dn2"] / 2, level_move_rate_month=float(np.mean(mv)),
            step_log=float(psi), time_aggregation_prediction=float(np.mean(mv)) * 12 * psi ** 2 / 6)
    return out


def me_layer_table(info):
    t = info[info["spouse"].isin(["h", "w"])].copy()
    t["shortfall"] = t["target_var_e_w"] - t["var_e_w"]
    agg = {}
    for sp, g in t.groupby("spouse"):
        w = g["n"] / g["n"].sum()
        agg[sp] = dict(target_var_e_w=float((w * g["target_var_e_w"]).sum()), drawn_var_e_w=float((w * g["var_e_w"]).sum()),
                       shortfall=float((w * g["shortfall"]).sum()), var_e_y=float((w * g["var_e_y"]).sum()),
                       var_e_h=float((w * g["var_e_h"]).sum()), clipped_groups=int(g["clipped"].sum()),
                       groups=int(len(g)))
    return agg, t[["spouse", "age_group", "n", "var_e_y", "var_e_h", "cov_e_yh", "var_e_w", "target_var_e_w",
                   "clipped", "shortfall"]].to_dict(orient="records")


def caller(work, spec, dta, corr, jump, minw):
    lines = [f'global INPUT "{dta}"', f'global SPEC "{spec}"', f'global WORK "{work}"',
             f'global RESULTS "{work}\\res_{spec}.csv"', 'global RUNS "gmm9"', f"global SW_jump {jump}",
             f"global SW_minw {minw}"]
    if not corr:
        lines.append(f'global OVRX "{BPS_CODE / "ovr_me0.do"}"')
    lines += [f'do "{BPS_CODE / "bps_on_sim_me.do"}"', ""]
    p = Path(work) / f"caller_{spec}.do"
    p.write_text("\n".join(lines))
    return p


def run_specs(specs, panels, work, stata, par):
    todo = list(specs.items())
    running, done = [], {}
    while todo or running:
        while todo and len(running) < par:
            spec, (pan, corr, jump, minw) = todo.pop(0)
            c = caller(work, spec, panels[pan], corr, jump, minw)
            running.append((spec, subprocess.Popen([stata, "/e" if os.name == "nt" else "-b", "do", str(c)], cwd=work), time.time()))
        time.sleep(5)
        for item in list(running):
            spec, pr, t0 = item
            if pr.poll() is not None:
                running.remove(item)
                row = Path(work) / spec / "bps_on_sim_row.csv"
                r = pd.read_csv(row).iloc[0].to_dict() if row.exists() else {}
                done[spec] = {k: float(r[k]) for k in KEYS if k in r and pd.notna(r[k])}
                done[spec].update(panel=specs[spec][0], bps_me_correction=specs[spec][1], jump_trim=specs[spec][2],
                                  minw_trim=specs[spec][3], stata_minutes=(time.time() - t0) / 60)
                print(spec, {k: round(v, 4) for k, v in done[spec].items() if isinstance(v, float)}, flush=True)
    return done


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--start", default=None)
    ap.add_argument("--K", type=int, default=3)
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--work", default=str(Path(tempfile.gettempdir()) / "paperA_bps_wp1"))
    ap.add_argument("--stata", default=STATA)
    ap.add_argument("--nu0", action="store_true", help="also simulate with sig_nu_w = sig_nu_h = 0")
    ap.add_argument("--par", type=int, default=3)
    ap.add_argument("--only", default=None, help="comma list of specs to run")
    a = ap.parse_args()
    import post_common as pc
    import sim_panel_writer as spw
    from bps_check import monthly_panel
    work = Path(a.work)
    work.mkdir(parents=True, exist_ok=True)
    ctx = pc.setup(a.start, K=a.K, threads=a.threads)
    fx = ctx.E._W["fx"]
    rep = dict(start=a.start or "analytic start", K=a.K, size=ctx.spec["size"], seed=ctx.spec["seed"],
               ext=ctx.spec["ext"], sig_nu_h=fx["sig_nu_h"], sig_nu_w=fx["sig_nu_w"], rho_nu=fx["rho_nu"],
               psi_h=fx["psi_h"], psi_w=fx["psi_w"], work=str(work))
    panels, specs = {}, dict(SPECS)
    sims = [("", None)] + ([("_nu0", {"sig_nu_w": 0.0, "sig_nu_h": 0.0})] if a.nu0 else [])
    for tag, ov in sims:
        t0 = time.time()
        res, th, fx_sim = pc.simulate_only(ctx, overrides=ov)
        rep["decomp" + tag] = wage_decomposition(res, fx)
        print("decomp" + tag, json.dumps(rep["decomp" + tag], indent=1), flush=True)
        mp = monthly_panel(res, ctx.E._W["cfg"], fx)
        del res
        base = spw.to_bps_panel(mp, seed=7, educ_in_years=True)
        del mp
        lh = np.log(base.loc[(base["hours"] > 0) & (base["marit"] == 1), "hours"])
        lhw = np.log(base.loc[(base["hourw"] > 0) & (base["marit"] == 1), "hourw"])
        rep["var_log_hours" + tag] = dict(h=float(lh.var()), w=float(lhw.var()))
        panels["none" + tag] = str(spw.write_bps_dta(base, work / f"wp1_none{tag}.dta"))
        if not tag:
            pm, info_m = spw.add_measurement_error(base, seed=11)
            panels["me"] = str(spw.write_bps_dta(pm, work / "wp1_me.dta"))
            px, info_x = spw.add_measurement_error(base, gross_rate=0.01, gross_sd=0.7, seed=11)
            panels["mix"] = str(spw.write_bps_dta(px, work / "wp1_mix.dta"))
            rep["me_layer"], rep["me_layer_groups"] = me_layer_table(info_m)
            del pm, px
        rep["rows" + tag] = len(base)
        print(f"panels{tag} written ({time.time() - t0:.0f}s)", flush=True)
    if a.nu0:
        specs.update(SPECS_NU0)
    if a.only:
        specs = {k: v for k, v in specs.items() if k in a.only.split(",")}
    rep["bps"] = run_specs(specs, panels, str(work), a.stata, a.par)
    out = HERE / "results" / f"bps_trim_{datetime.now():%Y%m%d_%H%M%S}"
    out.mkdir(parents=True, exist_ok=True)
    (out / "bps_trim.json").write_text(json.dumps(rep, indent=1, default=float))
    print(f"-> {out}")


if __name__ == "__main__":
    main()
