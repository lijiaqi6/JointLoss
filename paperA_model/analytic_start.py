"""Paper A model: closed-form start values (identification plan Sections 1.2, 1.4, 1.5).

Reads output/paperA_targets.csv (IGE/60.PaperATargets.py) and writes
  inputs/start_analytic.json   theta (31 parameters) + the source / status of each start value
  inputs/wage_process.json     p_c, p_eps_w, p_eps_h, sigma_nu, rho_nu (closed forms before the BPS-harness correction)
and prints the over-identification check of Section 1.4 (annual excess implied by the monthly closed forms vs T5).

These are start values and consistency checks, not calibrations: all 31 parameters stay in the one SMM run.
Where a target the closed form needs is not yet in the targets file, the fallback is named in 'status' ('FALLBACK').

Run: .venv/Scripts/python.exe paperA_model/analytic_start.py [--ext cs_memory,hc_eta] [--out <json>]
--ext: coded start values of the model extensions (2026-10-18): cs_memory splits the couples' excess job-loss risk
between the permanent type (kappa - 1 from the PSID two-window permanent component, psid_perm / psid_cy_wbase_W) and the
memory multiplier c_mem (the rest of the CPS short-horizon excess, divided by the mean probability that the displaced
spouse is still non-employed and UI-entitled 1-3 months later); hc_eta takes eta_up from --eta-start (a value chosen by
the documented one-dimensional profile, results/diagnostics_20261018.md). Without --ext the extensions' parameters
stay at their nested value 0. --out writes the start to another file (default inputs/start_analytic.json).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from params import (INPUTS, Config, FIXED_DEFAULTS, default_start, load_fixed,  # noqa: E402
                    wage_process_closed_form)

TARGETS = HERE.parent / "output" / "paperA_targets.csv"
# ridge point of the couple type (2026-10-18): the profile along the CPS ridge p(1-p)(m-1)^2 = (kappa-1)(1+p(m-1))^2
# (results/diagnostics_20261018.md, diagnostic B and step 2) gives the PSID annual joint-loss excess 0.118 at p_H 0.10,
# 0.081 at 0.03, 0.071 at 0.02, 0.063 at 0.015 (data 0.063) with the CPS leads and lags close to the data; 0.02 keeps
# the start 2% of the range above the lower bound 0.01
P_H_START = 0.02


def tget(tab, key, default=None):
    if tab is not None and key in tab.index and np.isfinite(tab.loc[key, "value"]):
        return float(tab.loc[key, "value"]), "IGE/60 " + key
    return default, "FALLBACK (plan / model document number; target not in paperA_targets.csv)"


def ridge_m(p_H, kap1):
    """m_H on the ridge p(1-p)(m-1)^2 = (kappa-1)(1 + p(m-1))^2 (plan Section 1.4); requires p_H < 1/kappa."""
    a = p_H * (1 - p_H) - kap1 * p_H ** 2
    if a <= 0:
        raise ValueError("p_H >= 1/kappa: no solution on the ridge")
    b, c = -2 * kap1 * p_H, -kap1
    x = (-b + np.sqrt(b * b - 4 * a * c)) / (2 * a)
    return 1 + x


def static_preferences(th, fx, sigma):
    """Work costs, child costs, the husband's full-time cost and the SNAP stigma from logits at a median state (White
    couple, s = 0, low type, era 2, wife 30-34, both at human capital level 4, transitory shocks averaged). A coded
    start-value mapping, not a calibration. Income differences between alternatives are valued at the marginal
    utility of the reference consumption (u'(c_ref / sc) / sc x delta income), i.e. as if spending were smoothed, which
    is what the household with savings does; a static (hand-to-mouth) valuation overstates the utility gain of work by
    a factor of about two at these incomes. The value of human capital accumulation is ignored."""
    from model import Model                         # local import: needs the schedules
    cfg = Config(T=12)
    m = Model(th, cfg, 2, 1, 0, 0, fixed=fx)
    g, ctr = 1, (m.H - 1) // 2
    mu_ = lambda x: x ** (-m.gamma)

    def inc(c, k, iw=ctr, ih=ctr, S=0):
        v = float(np.dot(m.pnu, m.inc0[g, c, iw, ih, k, :]))
        if S:
            v += float(np.dot(m.pnu, np.maximum(m.snapB[g, c, iw, ih, k, :], 0)))
        return v

    sc = m.sc[g]
    cfg_of = {(int(m.cfg_lw[c]), int(m.cfg_lh[c]), int(m.cfg_hw[c]), int(m.cfg_hh[c])): c for c in range(m.ncfg)}
    E = 0
    emp0, pt = 0.809, 0.337
    P0, PP, PF = 1 - emp0, emp0 * pt, emp0 * (1 - pt)
    out = {}
    lam = {}
    dy = {}
    for k in range(3):
        y = {h: inc(cfg_of[(E, 0, h, 2)], k) for h in (0, 1, 2)}
        c_ref = P0 * y[0] + PP * y[1] + PF * y[2]
        lam[k] = mu_(c_ref / sc[k]) / sc[k]
        dy[k] = y
    out["phi_F"] = lam[0] * (dy[0][2] - dy[0][0]) - sigma * np.log(PF / P0)
    out["phi_P"] = lam[0] * (dy[0][1] - dy[0][0]) - sigma * np.log(PP / P0)
    for k, emp, nm in ((1, 0.754, "theta_05"), (2, 0.823, "theta_617")):
        A = np.exp((lam[k] * (dy[k][2] - dy[k][0]) - out["phi_F"]) / sigma) +             np.exp((lam[k] * (dy[k][1] - dy[k][0]) - out["phi_P"]) / sigma)
        out[nm] = sigma * np.log(A * (1 - emp) / emp)
    # husband: part-time share 0.106 (wife's choice averaged as above, no child)
    yhF = inc(cfg_of[(E, 0, 1, 2)], 0)
    yhP = inc(cfg_of[(E, 0, 1, 1)], 0)
    out["phi_h"] = lam[0] * (yhF - yhP) - sigma * np.log(0.894 / 0.106)
    # SNAP stigma: take-up 60% at the first eligible working state (wife not employed, husband part time). The benefit
    # is valued at u'(c_ref) like every other income difference above: valuing it at the household's own income
    # (2026-10-18 first version) gave kappa_S = 2.64, above the upper bound 1, and zero simulated SNAP receipt, so the
    # SNAP moments had no slope in kappa_S (Jacobian norm 0.02; receipt B / W 10.4 / 5.4% at kappa_S = 0, 7.2 / 3.5%
    # at 0.1, 2.3 / 1.0% at 0.3, 0 at 2.64)
    kap = None
    c = cfg_of[(m.N_, 0, 0, 1)]
    for ih in range(m.H):
        if np.all(m.snapB[g, c, 0, ih, 1, :] > 0):
            B = inc(c, 1, iw=0, ih=ih, S=1) - inc(c, 1, iw=0, ih=ih)
            kap = lam[1] * B - sigma * np.log(0.6 / 0.4)
            break
    out["kappa_S"] = max(kap, 0.0) if kap is not None else th["kappa_S"]
    return out


def main(write=True, verbose=True, ext=(), eta_start=None, out=None):
    tab = pd.read_csv(TARGETS).set_index("id") if TARGETS.exists() else None
    th = default_start()
    src = {k: "default (params.py)" for k in th}
    fx = json.loads(json.dumps(FIXED_DEFAULTS))
    fx.update(load_fixed())

    # ---------------- displacement risk (Section 1.4) --------------------------------------------------------------
    bw = {}
    for r, key in (("B", "black"), ("W", "white")):
        bw[r], s_ = tget(tab, f"cps_wife_hazard_{key}", {"B": 0.0034, "W": 0.0022}[r])
    bw_pool, _ = tget(tab, "cps_wife_hazard_pooled", 0.0023)
    bh, bh_src = {}, {}
    for r in ("B", "W"):
        v, s_ = tget(tab, f"cps_h_hazard_{r}", None)                 # T7 (CPS monthly), not yet in IGE/60
        if v is None:
            a, s2 = tget(tab, f"psid_h_disp_rate_{r}", {"B": 0.080, "W": 0.048}[r])
            v, s_ = -np.log(1 - a) / 12, f"FALLBACK: PSID annual {a:.3f} -> -ln(1-a)/12 ({s2}); CPS T7 missing"
        bh[r], bh_src[r] = v, s_
    bh_pool = 0.26 * bh["B"] + 0.74 * bh["W"]                         # PSID couple-year shares (26% Black)
    X = {s: tget(tab, f"cps_jl_nt_s{s}", d)[0] for s, d in ((0, 0.026), (1, 0.211), (2, 0.337))}
    lags = [tget(tab, f"cps_jl_nt_{k}", 0.006)[0] for k in ("m3", "m2", "m1", "p1", "p2", "p3")]
    L = float(np.mean(lags))
    kap1 = L / bw_pool
    kap1_psid = tget(tab, "psid_perm", 0.020)[0] / tget(tab, "psid_cy_wbase_W", 0.039)[0]
    kap1_type = kap1_psid if "cs_memory" in ext else kap1          # memory: the type carries the permanent part only
    p_H = P_H_START
    m_H = ridge_m(p_H, kap1_type)
    Em = 1 + p_H * (m_H - 1)
    kappa = 1 + kap1_type
    pic = {}
    for s in (0, 1, 2):
        A = X[s] + bw_pool
        pic[s] = max(bh_pool * (A - kappa * bw_pool) / ((1 - A) + bh_pool * (A - kappa * bw_pool)), 0.0)
    for r in ("B", "W"):
        th[f"delta_w_{r}"] = bw[r] / Em
        src[f"delta_w_{r}"] = f"b_w(r)/E m; b_w = {bw[r]:.5f} (IGE/60 CPS)"
        Bq = (bh[r] - pic[0]) / (1 - pic[0])                           # one fixed-point step
        th[f"delta_h_{r}"] = Bq / Em
        src[f"delta_h_{r}"] = f"(b_h - pi_c(0))/(1 - pi_c(0)) / E m; b_h = {bh[r]:.5f}: {bh_src[r]}"
    for s in (0, 1, 2):
        th[f"pi_c{s}"] = pic[s]
        src[f"pi_c{s}"] = f"B [A - kappa b_w]/[(1-A) + B(A - kappa b_w)], A = X({s}) + b_w, X = {X[s]:.4f} (IGE/60 CPS, non-temporary)"
    th["p_H"], th["m_H"] = p_H, m_H
    src["p_H"] = (f"ridge point p_H = {P_H_START} (only kappa is pinned by the monthly moments, plan Section 2.3; the point "
                  "from the profile of the PSID annual excess along the ridge, results/diagnostics_20261018.md)")
    src["m_H"] = f"ridge: kappa - 1 = L / b_w = {L:.4f} / {bw_pool:.4f} = {kap1:.2f} (CPS leads/lags)"
    if "cs_memory" in ext:
        # memory: c_mem = (CPS kappa - 1 - PSID kappa - 1) / mean S, S(k) = q_UI ((1 - lambda)(1 - lapse))^(k - 1) the
        # probability that the displaced spouse is non-employed and UI-entitled k = 1..3 months later, averaged over
        # the husband (lambda_h, lags) and the wife (lambda_w, leads)
        sch = json.loads((INPUTS / "schedules_era2.json").read_text())["ui"]
        qui, lapse = sch["q_ui"], sch["expiry"]
        e3, _ = tget(tab, "sipp_his_emp_s3_sep", 0.586)
        n3, _ = tget(tab, "sipp_his_emp_s3_nosep", 0.983)
        lam_h0 = 1 - (1 - e3 / n3) ** (1 / 3)
        lam_w0 = tget(tab, "cps_entry_white", 0.075)[0] / 0.6
        Sbar = np.mean([qui * ((1 - lam) * (1 - lapse)) ** (k - 1) for lam in (lam_h0, lam_w0) for k in (1, 2, 3)])
        th["c_mem"] = max(kap1 - kap1_type, 0.0) / Sbar
        src["c_mem"] = (f"(kappa-1 CPS {kap1:.3f} - kappa-1 PSID {kap1_type:.3f}) / mean S {Sbar:.3f} (q_UI {qui:.3f}, "
                        f"lapse {lapse:.3f}, lambda_h {lam_h0:.3f}, lambda_w {lam_w0:.3f}, k = 1..3)")
        src["m_H"] = f"ridge with the PSID permanent component: kappa - 1 = {kap1_type:.3f} (memory carries the rest)"
    if "hc_eta" in ext:
        th["eta_up"] = float(eta_start) if eta_start is not None else 0.0
        src["eta_up"] = (f"{th['eta_up']:g}: one-dimensional profile of the wage-growth block at the analytic start "
                         f"(results/diagnostics_20261018.md); the closed form from mean levels by age exceeds the upper "
                         f"bound 3 (wives 6.0, husbands 16.5)")

    # over-identification check (annual, Section 1.4)
    Bp = bh_pool
    p_both = 12 * pic[0] + 144 * kappa * bw_pool * Bp
    p_h_y = 12 * (pic[0] + Bp)
    p_w_noth = 12 * bw_pool
    exc_model = p_both / p_h_y - p_w_noth
    exc_data, _ = tget(tab, "psid_cy_diff_all", 0.063)
    check = {"annual_excess_closed_form": exc_model, "annual_excess_psid_T5": exc_data,
             "P_both_year": p_both, "P_h_year": p_h_y, "kappa_minus_1_cps": kap1,
             "kappa_minus_1_psid": tget(tab, "psid_perm", 0.020)[0] / tget(tab, "psid_cy_wbase_W", 0.039)[0]}

    # ---------------- other closed forms (Section 1.5) -------------------------------------------------------------
    for r in ("B", "W"):
        s_r, s_ = tget(tab, f"psid_sep_rate_{r}", {"B": 0.032, "W": 0.015}[r])
        th[f"sigma0_{r}"] = -np.log(1 - s_r) / 12
        src[f"sigma0_{r}"] = f"-ln(1 - s_r)/12, s_r = {s_r:.4f} ({s_})"
        dlt, s_ = tget(tab, f"psid_es_bw_present_13_{r}", {"B": -0.045, "W": -0.019}[r])
        D_r = 5.0
        th[f"sigmaJ_{r}"] = abs(dlt) / D_r
        src[f"sigmaJ_{r}"] = f"Delta_r / D_r, Delta = {abs(dlt):.3f} ({s_}); D_r = 5 months (SIPP-based, plan: FALLBACK until IGE/40 D_r)"
    psi_w, psi_h = fx["psi_w"], fx["psi_h"]
    gw, s1 = tget(tab, "psid_wg_w_25", 0.08)
    gh, s2 = tget(tab, "psid_wg_h_25", 0.067)
    th["pi_up_w"], th["pi_up_h"] = gw / (24 * psi_w), gh / (24 * psi_h)
    src["pi_up_w"] = f"g2/(24 psi_w), g2 = {gw:.4f} ({s1}); psi_w = {psi_w} (PLACEHOLDER)"
    src["pi_up_h"] = f"g2/(24 psi_h), g2 = {gh:.4f} ({s2}); psi_h = {psi_h} (PLACEHOLDER)"
    if "hc_eta" in ext:
        # pi_up is the rate at level 4; the 25-34 growth averages (level / 4)^(-eta) over the entry couples' levels
        ent = pd.read_csv(INPUTS / "psid_entry_couples.csv", usecols=["hw0", "hh0"])     # aggregate means only
        for j, col in (("w", "hw0"), ("h", "hh0")):
            Ej = float(np.mean((ent[col].to_numpy(float) / 4.0) ** (-th["eta_up"])))
            th[f"pi_up_{j}"] = th[f"pi_up_{j}"] / Ej
            src[f"pi_up_{j}"] += f" / E[(level/4)^-eta] = {Ej:.4f} over the entry couples' levels (eta_up start)"
    # depreciation / displacement loss (plan Section 1.5): loss(n) ~ psi (d_j + pi_dn,j n), fitted by inverse-variance
    # weighted least squares on the SIPP re-employment earnings losses after 1-3, 4-12, 13-24 months of
    # non-employment (involuntary separations, by spouse; spell midpoints 2, 8, 18.5 months)
    n_mid = np.array([2.0, 8.0, 18.5])
    for j, psi, fb in (("w", psi_w, (-0.060, -0.112, -0.199)), ("h", psi_h, (-0.058, -0.162, -0.276))):
        keys = [f"sipp_reemp_{j}_1_3", f"sipp_reemp_{j}_4_12", f"sipp_reemp_{j}_13_24"]
        vals, ses, ok = [], [], True
        for kk, f in zip(keys, fb):
            v, s_ = tget(tab, kk, f)
            vals.append(-v)
            ses.append(float(tab.loc[kk, "se"]) if tab is not None and kk in tab.index else 0.03)
            ok &= not s_.startswith("FALLBACK")
        w = 1 / np.array(ses) ** 2
        X = np.column_stack([np.ones(3), n_mid])
        b = np.linalg.solve(X.T @ (X * w[:, None]), X.T @ (w * np.array(vals)))
        icpt, slope = float(b[0]), float(b[1])
        th[f"pi_dn_{j}"] = max(slope / psi, 0.0)
        th[f"d_{j}"] = max(icpt / psi, 0.0)
        tag = "IGE/60 SIPP" if ok else "FALLBACK"
        src[f"pi_dn_{j}"] = f"slope {slope:.4f}/month / psi of the WLS fit of SIPP losses {np.round(vals, 3).tolist()} ({tag})"
        src[f"d_{j}"] = f"intercept {icpt:.3f} / psi of the same fit ({tag}; the intercept is not near zero, so d_j stays)"
    for r in ("B", "W"):
        e3, s_ = tget(tab, "sipp_his_emp_s3_sep", 0.586)
        n3, _ = tget(tab, "sipp_his_emp_s3_nosep", 0.983)
        th[f"lam_h_{r}"] = 1 - (1 - e3 / n3) ** (1 / 3)
        src[f"lam_h_{r}"] = (f"1 - (1 - {e3:.3f}/{n3:.3f})^(1/3), SIPP 3-month re-employment ({s_}); not by race; the 6- "
                             "and 12-month points imply lower rates (plan Section 2.3, tension A)")
        ent, s_ = tget(tab, f"cps_entry_{'black' if r == 'B' else 'white'}", {"B": 0.094, "W": 0.075}[r])
        th[f"lam_w_{r}"] = ent / 0.6
        src[f"lam_w_{r}"] = f"entry / acceptance, entry = {ent:.4f} ({s_}), acceptance 0.6 assumed (lower bound = entry)"
    # T28 (over-dispersion, now in IGE/60): implied share of husbands displaced >= 2 times at the start values, for
    # assumed numbers of observed years N (the file does not give N): information only, p_H stays at the ridge point
    t28 = {}
    for r in ("B", "W"):
        A_r, _ = tget(tab, f"psid_h_disp_rate_{r}", {"B": 0.065, "W": 0.044}[r])
        for N in (10, 15, 20):
            sh = 0.0
            for p_t, m_t in ((1 - p_H, 1.0), (p_H, m_H)):
                a_t = min(A_r * m_t / Em, 0.99)
                sh += p_t * (1 - (1 - a_t) ** N - N * a_t * (1 - a_t) ** (N - 1))
            t28[f"{r}_N{N}"] = sh
        t28[f"{r}_data"] = tget(tab, f"psid_disp2plus_{r}", float("nan"))[0]
    check["T28_disp2plus_implied"] = t28
    th["a_bar"] = 5.0
    src["a_bar"] = "PLACEHOLDER $5,000 (10th percentile of couples' liquid wealth at 25-34 not yet in IGE/60)"
    ovp = INPUTS / "start_overrides.json"                         # data-based start values from IGE/62 (a_bar)
    if ovp.exists():
        ov = json.loads(ovp.read_text())
        for k, v in ov.get("theta", {}).items():
            if k in th:
                th[k] = float(v)
                src[k] = "IGE/62 start_overrides.json: " + ov.get("source", {}).get(k, "")
    th["F"] = 0.10 * np.exp(fx["mu_w"]["W"]) * fx["H_P"] / 1000.0
    src["F"] = "10% of the wife's part-time earnings at level 4 (plan Section 1.5)"

    # wage process closed forms at these pi_up
    wp = wage_process_closed_form(fx, th)
    fx.update(wp)
    # preferences: static logits at the median state (given F, a_bar, wage process)
    sigma = fx["sigma_eps"]
    pref = static_preferences(th, fx, sigma)
    for k, v in pref.items():
        th[k] = float(v)
        src[k] = f"logit at the median state, income valued at u'(c_ref), sigma_eps = {sigma} (start value only)"

    # start values inside the SMM bounds (a closed form outside them is clipped, recorded in the source)
    from params import PARAMS
    for nm, _, lo, hi, _b in PARAMS:
        v = th[nm]
        if v < lo or v > hi:
            th[nm] = float(min(max(v, lo), hi))
            src[nm] += f" | closed form {v:.4g} outside the bounds [{lo}, {hi}]: clipped to {th[nm]:.4g}"
    if verbose:
        print("start values (31):")
        for k in th:
            print(f"  {k:10s} {th[k]: .6g}   {src[k]}")
        print("\nover-identification check (plan Section 1.4):")
        for k, v in check.items():
            print(f"  {k:28s} {v if isinstance(v, dict) else round(v, 4)}")
        print("\nwage process (closed forms, before the BPS-harness correction):", {k: round(v, 5) for k, v in wp.items()})
    if write:
        INPUTS.mkdir(exist_ok=True)
        (Path(out) if out else INPUTS / "start_analytic.json").write_text(json.dumps(
            {"theta": th, "source": src, "check_section_1_4": check, "ext": list(ext),
             "targets_file": str(TARGETS.relative_to(HERE.parent.parent)) if TARGETS.exists() else None}, indent=1))
        if out is None:                                         # a start written elsewhere leaves the wage process
            (INPUTS / "wage_process.json").write_text(json.dumps(
                {**wp, "status": "closed forms (plan Section 1.2) at the analytic pi_up and PLACEHOLDER psi; the one-time "
                                 "BPS-harness correction is not yet applied", "psi_w": psi_w, "psi_h": psi_h}, indent=1))
    return th, src, check


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--ext", default="", help="comma-separated extensions: cs_memory, hc_eta")
    ap.add_argument("--eta-start", dest="eta_start", type=float, default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    main(ext=tuple(x for x in a.ext.split(",") if x), eta_start=a.eta_start, out=a.out)
