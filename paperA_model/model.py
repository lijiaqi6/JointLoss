"""Paper A model: arrays for one problem (r, s, tau) and one policy era, consumed by solve.py and simulate.py.

Everything here is plain numpy and follows sec7_model.tex / model_document.tex in simulator order:
  state indices  wife labor state lw: 0 = employed, 1 = non-employed entitled after a part-time job, 2 = entitled after
                 a full-time job, 3 = not entitled (lost_hours = False: 0 = E, 1 = entitled, 2 = not entitled);
                 husband lh: 0 = E, 1 = entitled, 2 = not entitled; human capital level 0..H-1 (level 4 of 7 = index 3);
                 youngest child k: 0 none, 1 aged 0-5, 2 aged 6-17; transitory pair nu = 2 iw + ih (i = 0: -sigma,
                 1: +sigma); assets on a curved grid from -a_bar.
  configs        a 'work configuration' (lw, lh, hours_w, hours_h) fixes the transition of the state; the SNAP choice
                 does not move the state (it only shifts cash on hand and utility), so a discrete alternative d =
                 (config, S). Hours index 0 = none, 1 = part time (87 h), 2 = full time (173 h).
  transitions    end-of-month events (model document Section 6): displacement (common shock pi_c(s), then own hazards
                 m_tau delta_j(r) for spouses who worked), job finding lambda_j(r) for spouses non-employed this month,
                 the wife's quit when hours = 0 with a job, UI take-up q_UI and geometric expiry 1/6; then human capital
                 (accumulation / depreciation, displacement loss, shared and idiosyncratic innovations), the child
                 bucket, and the separation hazard sigma_0(r) + sigma_J(r) 1{husband non-employed next month}.
"""
from __future__ import annotations

import numpy as np

from params import Config, load_fixed, load_schedule

NK, NNU, NLH = 3, 4, 3
CAT_F, CAT_P, CAT_NW, CAT_D = 0, 1, 2, 3          # human capital categories: worked F / worked P (not displaced),
                                                  # did not work, displaced
N_AGE_GROUPS = 7                                  # wife 25-29, ..., 55-59


ASSET_EPS = 1e-5                 # width (thousand $) of the asset segment that holds the SNAP asset-test drop


def asset_grid(a_bar: float, cfg: Config) -> np.ndarray:
    u = np.linspace(0.0, 1.0, cfg.n_assets)
    return -a_bar + (cfg.a_max + a_bar) * u ** cfg.a_curv


def age_group(t: int) -> int:
    return min(t // 60, N_AGE_GROUPS - 1)


def hc_scale(cfg: Config) -> float:
    """Ratio of the 7-level step to the n_hc-level step: parameters in grid units are multiplied by it (levels) or its
    square (innovation probabilities) so that the n_hc grid spans the same log-wage range."""
    return (cfg.n_hc - 1) / 6.0


def own_step_matrix(H: int, cat: int, up: float, dn: float, d: float):
    """Forward transition of one spouse's level in step (i)-(ii) by category, as sparse rows (idx, prob)."""
    M = np.zeros((H, H))
    upv = np.broadcast_to(np.asarray(up, float), (H,))             # up: scalar or one value per level
    for h in range(H):
        if cat in (CAT_F, CAT_P):
            M[h, min(h + 1, H - 1)] += upv[h]
            M[h, h] += 1 - upv[h]
        elif cat == CAT_NW:
            M[h, max(h - 1, 0)] += dn
            M[h, h] += 1 - dn
        else:
            fl = int(np.floor(d))
            fr = d - fl
            M[h, max(h - fl, 0)] += 1 - fr
            M[h, max(h - fl - 1, 0)] += fr
    return M


def innov_matrix(H: int, p: float):
    """Idiosyncratic innovation: +-1 with probability p/2 each, truncated."""
    M = np.zeros((H, H))
    for h in range(H):
        M[h, min(h + 1, H - 1)] += p / 2
        M[h, max(h - 1, 0)] += p / 2
        M[h, h] += 1 - p
    return M


def sparse_rows(M, width=3):
    H = M.shape[0]
    idx = np.zeros((H, width), np.int64)
    pr = np.zeros((H, width))
    n = np.zeros(H, np.int64)
    for h in range(H):
        nz = np.nonzero(M[h] > 0)[0]
        assert len(nz) <= width
        n[h] = len(nz)
        idx[h, :len(nz)] = nz
        pr[h, :len(nz)] = M[h, nz]
    return idx, pr, n


def hsv_tax(Ya_k, chi, mu):
    """Monthly tax (thousand $) on annualised income Ya_k (thousand $): BPS form fitted on annual dollars; floored
    at zero (EITC and SNAP enter separately)."""
    Y = np.maximum(Ya_k * 1000.0, 0.0)
    keep = (1.0 - chi) * np.power(np.maximum(Y, 1e-9), 1.0 - mu)
    T = np.where(Y > 0, Y - keep, 0.0)
    return np.maximum(T, 0.0) / 12.0 / 1000.0


def eitc_month(earn_month_k, n, sch, joint=True):
    p = sch["eitc_annual"][str(min(int(n), 3))]
    Y = 12.0 * earn_month_k * 1000.0
    ps = p["ps_mfj"] if joint else p["ps_single"]
    e = np.minimum(p["in"] * Y, p["max"]) - p["out"] * np.maximum(0.0, Y - ps)
    return np.maximum(e, 0.0) / 12.0 / 1000.0


class Model:
    """Arrays of one problem (r, s, tau) in one era. theta: dict of the 31 parameters."""

    def __init__(self, theta: dict, cfg: Config, era: int, r: int, s: int, tau: int, fixed: dict | None = None,
                 overrides: dict | None = None):
        fx = load_fixed() if fixed is None else fixed
        ov = overrides or {}
        self.cfg, self.era, self.r, self.s, self.tau = cfg, era, r, s, tau
        R = ("B", "W")[r]
        sch = load_schedule(era)
        H = cfg.n_hc
        self.H, self.NLW, self.NA = H, cfg.n_lw, cfg.n_assets
        # new-job extension (2026-10-19, estimate.py --new-job on; fx['new_job']): one more wife labor state EN_ =
        # employed on a job started less than ~a year ago (index NLW of the base model, appended so that every other
        # index is unchanged); allocated only when the extension is on (EN_ = -1 otherwise)
        self.new_job = bool(fx.get("new_job", False))
        self.EN_ = cfg.n_lw if self.new_job else -1
        if self.new_job:
            self.NLW = cfg.n_lw + 1
        sc_hc = hc_scale(cfg)
        th = dict(theta)

        # ---------------- fixed economics -------------------------------------------------------------------------
        self.beta = ov.get("beta", fx["beta"])
        self.gamma = fx["gamma"]
        self.rm = ov.get("r_m", fx["r_m"])
        self.sigma_eps = ov.get("sigma_eps", fx["sigma_eps"])
        self.kappa_S = th["kappa_S"]
        self.a_bar = th["a_bar"]
        self.agrid = asset_grid(self.a_bar, cfg)
        # borrowing wedge (2026-10-18, coded input inputs/borrowing_wedge.json; 0 = one interest rate): the monthly
        # rate on negative beginning-of-month assets is r_m + r_wedge; with a wedge the grid node nearest 0 is moved
        # to 0 so that the kink of the budget sits on a node
        self.r_wedge = float(fx.get("r_wedge", 0.0))
        if self.r_wedge > 0 and self.agrid[0] < 0:
            j0 = int(np.argmin(np.abs(self.agrid)))
            if 0 < j0 < len(self.agrid) - 1:
                self.agrid[j0] = 0.0
        # SNAP asset test (2026-10-18 fix of check 0): next month's value drops where assets cross the limit L (the
        # SNAP alternative disappears from the logsum). Two nodes, L (eligible: assets <= L) and L + ASSET_EPS (not
        # eligible), put the drop inside a segment of width ASSET_EPS, so that W is smooth on every other segment; the
        # solver and the simulator add the corner a' = L as a candidate (jL = index of the node L).
        L = -1e9 if "no_snap" in ov else sch["snap"]["asset_limit"] / 1000.0
        self.jL = -1
        if self.agrid[0] < L < self.agrid[-1] - 2 * ASSET_EPS:
            g_ = self.agrid
            g_ = g_[(np.abs(g_ - L) > 1e-9) & (np.abs(g_ - L - ASSET_EPS) > 1e-9)]
            self.agrid = np.sort(np.concatenate([g_, [L, L + ASSET_EPS]]))
            self.jL = int(np.nonzero(self.agrid == L)[0][0])
        self.NA = len(self.agrid)
        HF, HP = fx["H_F"], fx["H_P"]
        hours = np.array([0.0, HP, HF])

        # ---------------- wages: levels on the grid, centre index -------------------------------------------------
        psi_w = fx["psi_w"] / sc_hc
        psi_h = fx["psi_h"] / sc_hc
        ctr = (H - 1) / 2.0
        lev = np.arange(H) - ctr
        sig_nw = ov.get("sig_nu_w", fx["sig_nu_w"])
        sig_nh = ov.get("sig_nu_h", fx["sig_nu_h"])
        rho = fx["rho_nu"]
        nu_w = np.array([-sig_nw, -sig_nw, sig_nw, sig_nw])
        nu_h = np.array([-sig_nh, sig_nh, -sig_nh, sig_nh])
        self.pnu = np.array([(1 + rho) / 4, (1 - rho) / 4, (1 - rho) / 4, (1 + rho) / 4])
        wbar_w = np.exp(fx["mu_w"][R] + psi_w * lev) / 1000.0      # thousand $ per hour, nu = 0
        wbar_h = np.exp(fx["mu_h"][R] + psi_h * lev) / 1000.0
        self.wbar_w, self.wbar_h, self.nu_w, self.nu_h = wbar_w, wbar_h, nu_w, nu_h
        self.hours = hours

        # ---------------- hazards (monthly) -----------------------------------------------------------------------
        m = th["m_H"] if tau == 1 else 1.0
        self.dw = min(m * th[f"delta_w_{R}"], 0.999)
        self.dh = min(m * th[f"delta_h_{R}"], 0.999)
        if cfg.merge_s12 and s >= 1:
            self.pic = th["pi_c1"]
        else:
            self.pic = th[f"pi_c{s}"]
        self.lw_ = th[f"lam_w_{R}"]
        self.lh_ = th[f"lam_h_{R}"]
        self.qui = sch["ui"]["q_ui"]
        self.ui_exp = sch["ui"]["expiry"]
        # memory of displacement (2026-10-18; c_mem = 0: none): a spouse's hazard x (1 + c_mem) while the other spouse
        # is non-employed and UI-entitled after a displacement (the state already in the problem)
        self.c_mem = float(th.get("c_mem", 0.0))
        self.sig_E = th[f"sigma0_{R}"]
        self.sig_N = th[f"sigma0_{R}"] + th[f"sigmaJ_{R}"]
        # her-displacement separation extension (2026-10-19, fx['her_sep']): sigma_Jw is added to the hazard while she
        # is UI-entitled after her own displacement next month (her_sep_tie: sigma_Jw = his sigma_J(r)); additive with
        # his term; the solver then uses the (lw, lh) table sig_tab (None when off: the base kernel)
        self.her_sep = bool(fx.get("her_sep", False))
        self.sig_Jw = 0.0
        if self.her_sep:
            self.sig_Jw = float(th[f"sigmaJ_{R}"] if fx.get("her_sep_tie", False) else th.get("sigmaJw", 0.0))
        # new-job extension: extra exit hazard on a new job, graduation probability, UI rule of a new-job exit
        self.xi_nj = float(th.get("xi_nj", 0.0)) if self.new_job else 0.0
        self.g_nj = float(fx.get("nj_grad", 1.0 / 12.0))
        self.nj_ui = bool(fx.get("nj_ui", 0))
        for k_, v_ in ov.items():                       # test overrides of hazards
            if k_ in ("dw", "dh", "pic", "lw_", "lh_", "qui", "ui_exp", "sig_E", "sig_N"):
                setattr(self, k_, v_)

        # ---------------- human capital transitions ---------------------------------------------------------------
        # grid-unit parameters keep their log-wage meaning on an n_hc grid: steps are 1/sc_hc as large in log wage
        # per 7-grid step, so probabilities of one-level moves scale by sc_hc (growth = prob x psi).
        up_w, up_h = th["pi_up_w"] * sc_hc, th["pi_up_h"] * sc_hc
        # accumulation declining in the level (2026-10-18; eta_up = 0: constant): pi_up x (level / 4)^(-eta_up) with
        # the level on the 7-level scale (1 ... 7), capped at 1
        eta = float(th.get("eta_up", 0.0))
        lev7 = 1.0 + np.arange(H) * 6.0 / (H - 1)
        up_shape = (lev7 / 4.0) ** (-eta)
        dn_w, dn_h = th["pi_dn_w"] * sc_hc, th["pi_dn_h"] * sc_hc
        d_w, d_h = th["d_w"] * sc_hc, th["d_h"] * sc_hc
        ku = fx["kappa_up"]
        p_c = ov.get("p_c", fx["p_c"] * sc_hc ** 2)
        p_ew = ov.get("p_eps_w", fx["p_eps_w"] * sc_hc ** 2)
        p_eh = ov.get("p_eps_h", fx["p_eps_h"] * sc_hc ** 2)
        if "no_hc" in ov:                               # tests: freeze human capital
            up_w = up_h = dn_w = dn_h = d_w = d_h = p_c = p_ew = p_eh = 0.0
        self.p_c = p_c
        self.Aw = np.stack([own_step_matrix(H, c, np.minimum(up_w * up_shape * (1 if c == CAT_F else ku), 1.0), dn_w,
                                            d_w) for c in range(4)])
        self.Ah = np.stack([own_step_matrix(H, c, np.minimum(up_h * up_shape * (1 if c == CAT_F else ku), 1.0), dn_h,
                                            d_h) for c in range(4)])
        self.Iw = innov_matrix(H, p_ew)
        self.Ih = innov_matrix(H, p_eh)
        self.Is = innov_matrix(H, min(p_c + p_ew, 1.0))      # separated wife: one innovation, prob p_c + p_eps_w
        self.Aw_idx, self.Aw_p, self.Aw_n = map(np.stack, zip(*[sparse_rows(self.Aw[c]) for c in range(4)]))
        self.Ah_idx, self.Ah_p, self.Ah_n = map(np.stack, zip(*[sparse_rows(self.Ah[c]) for c in range(4)]))

        # ---------------- child process ---------------------------------------------------------------------------
        b0 = np.array(fx["b0_annual"][R]) / 12.0
        b2 = np.array(fx["b2_annual"][R]) / 12.0
        if "no_child" in ov:
            b0 = b0 * 0
            b2 = b2 * 0
        P = np.zeros((N_AGE_GROUPS, NK, NK))
        for g in range(N_AGE_GROUPS):
            age1 = 0.0 if "no_child" in ov else 1 / 72
            age2 = 0.0 if "no_child" in ov else 1 / 144
            P[g, 0, 1] = b0[g]
            P[g, 0, 0] = 1 - b0[g]
            P[g, 1, 2] = age1 * (1 - b2[g])                  # ages out of 0-5 unless a birth occurs
            P[g, 1, 1] = 1 - P[g, 1, 2]
            P[g, 2, 1] = b2[g]
            P[g, 2, 0] = age2 * (1 - b2[g])
            P[g, 2, 2] = 1 - P[g, 2, 1] - P[g, 2, 0]
        self.Pk = P

        # ---------------- configurations and transition outcomes --------------------------------------------------
        NLW = self.NLW
        if cfg.lost_hours:
            E_, UP_, UF_, N_ = 0, 1, 2, 3
            u_states = (UP_, UF_)
        else:
            E_, UP_, UF_, N_ = 0, 1, 1, 2
            u_states = (UP_,)
        self.E_, self.UP_, self.UF_, self.N_ = E_, UP_, UF_, N_
        wsl = [(CAT_F, E_), (CAT_P, E_), (CAT_NW, E_)] + [(CAT_NW, u) for u in u_states] + [(CAT_NW, N_)] + \
              [(CAT_D, u) for u in u_states] + [(CAT_D, N_)]
        EN_ = self.EN_
        if self.new_job:                                # new-job slices appended (earlier indices unchanged)
            wsl += [(CAT_F, EN_), (CAT_P, EN_), (CAT_NW, EN_)]
        E_in = EN_ if self.new_job else E_              # state a wife enters when she takes a job
        hsl = [(CAT_F, 0), (CAT_P, 0), (CAT_NW, 0), (CAT_NW, 1), (CAT_NW, 2), (CAT_D, 1), (CAT_D, 2)]
        self.ws_cat = np.array([c for c, _ in wsl], np.int64)
        self.ws_lw = np.array([l for _, l in wsl], np.int64)
        self.hs_cat = np.array([c for c, _ in hsl], np.int64)
        self.hs_lh = np.array([l for _, l in hsl], np.int64)
        wix = {p: i for i, p in enumerate(wsl)}
        hix = {p: i for i, p in enumerate(hsl)}
        lam_w, lam_h, q, ex = self.lw_, self.lh_, self.qui, self.ui_exp
        # UI and acceptance (Bacher, Grubener and Nord 2025; lead decision 2026-10-18): an entitled non-employed wife
        # who receives an offer at the end of the month may decline it and keep her entitlement (which then lapses
        # only with the monthly expiry hazard); accepting ends it. No new state: the offer node is a binary choice
        # (accept = next month employed; decline = (1 - ex) entitled + ex not entitled) taken after the month's
        # displacement and job-finding events of both spouses and before the human capital, child, separation and
        # transitory draws, with extreme-value taste shocks of scale sigma_eps (mean zero). Its value is a 'virtual'
        # wife slice nI + e of the solver's expectation array (e = index of the entitled state), filled by
        # solve.k_offer; Config.ui_accept = False restores the earlier rule (an offer always moves her to employment).
        self.ui_accept = bool(getattr(cfg, "ui_accept", True))
        self.herm = getattr(cfg, "w_interp", "hermite") == "hermite"
        self.nI = len(wsl)
        self.n_ent = len(u_states)
        self.u_states = np.array(u_states, np.int64)
        self.off_iE = wix[(CAT_NW, E_in)]
        self.off_iN = wix[(CAT_NW, N_)]
        self.off_iU = np.array([wix[(CAT_NW, u)] for u in u_states], np.int64)
        off_slice = {u: self.nI + e for e, u in enumerate(u_states)}
        xi, gnj = self.xi_nj, self.g_nj

        def wife_events(lw, hw_):
            """list of (works?, [(prob, slice)] if not displaced, [(prob, slice)] if displaced) for the wife."""
            if lw == E_ and hw_ > 0:
                lost = UF_ if hw_ == 2 else UP_
                return True, [(1.0, wix[(CAT_F if hw_ == 2 else CAT_P, E_)])], \
                    [(q, wix[(CAT_D, lost)]), (1 - q, wix[(CAT_D, N_)])]
            if lw == EN_ and hw_ > 0:
                # new job (extension): if not displaced, the new-job exit with probability xi, else the job becomes
                # established with probability g_nj; the exit is a quit (not entitled; human capital as in a quit
                # month) or, with nj_ui, a displacement (UI take-up q, displacement loss)
                lost = UF_ if hw_ == 2 else UP_
                cw = CAT_F if hw_ == 2 else CAT_P
                stay = [((1 - xi) * (1 - gnj), wix[(cw, EN_)]), ((1 - xi) * gnj, wix[(cw, E_)])]
                if self.nj_ui:
                    stay += [(xi * q, wix[(CAT_D, lost)]), (xi * (1 - q), wix[(CAT_D, N_)])]
                else:
                    stay += [(xi, wix[(CAT_NW, N_)])]
                return True, stay, [(q, wix[(CAT_D, lost)]), (1 - q, wix[(CAT_D, N_)])]
            if lw == E_ or lw == EN_:
                return False, [(1.0, wix[(CAT_NW, N_)])], None          # quits a job: not entitled
            if lw == N_:
                return False, [(lam_w, wix[(CAT_NW, E_in)]), (1 - lam_w, wix[(CAT_NW, N_)])], None
            if self.ui_accept:                                           # offer node: accept or keep entitlement
                return False, [(lam_w, off_slice[lw]), ((1 - lam_w) * (1 - ex), wix[(CAT_NW, lw)]),
                               ((1 - lam_w) * ex, wix[(CAT_NW, N_)])], None
            return False, [(lam_w, wix[(CAT_NW, E_in)]), ((1 - lam_w) * (1 - ex), wix[(CAT_NW, lw)]),
                           ((1 - lam_w) * ex, wix[(CAT_NW, N_)])], None

        def husb_events(lh, hh_):
            if lh == 0:
                return True, [(1.0, hix[(CAT_F if hh_ == 2 else CAT_P, 0)])], \
                    [(q, hix[(CAT_D, 1)]), (1 - q, hix[(CAT_D, 2)])]
            if lh == 2:
                return False, [(lam_h, hix[(CAT_NW, 0)]), (1 - lam_h, hix[(CAT_NW, 2)])], None
            return False, [(lam_h, hix[(CAT_NW, 0)]), ((1 - lam_h) * (1 - ex), hix[(CAT_NW, 1)]),
                           ((1 - lam_h) * ex, hix[(CAT_NW, 2)])], None

        cfgs, outs = [], []
        state_cfg = -np.ones((NLW, NLH, 6), np.int64)
        state_n = np.zeros((NLW, NLH), np.int64)
        pic, dw, dh = self.pic, self.dw, self.dh
        for lw in range(NLW):
            for lh in range(NLH):
                for hw_ in ((0, 1, 2) if lw in (E_, EN_) else (0,)):
                    for hh_ in ((1, 2) if lh == 0 else (0,)):
                        ww, wnd, wd = wife_events(lw, hw_)
                        hw2, hnd, hd = husb_events(lh, hh_)
                        if ww and hw2:
                            pj = {(0, 0): (1 - pic) * (1 - dw) * (1 - dh), (1, 0): (1 - pic) * dw * (1 - dh),
                                  (0, 1): (1 - pic) * (1 - dw) * dh, (1, 1): pic + (1 - pic) * dw * dh}
                        elif ww:
                            dwe = min(dw * (1 + self.c_mem), 0.999) if lh == 1 else dw     # memory: he is entitled
                            pd = pic + (1 - pic) * dwe
                            pj = {(0, 0): 1 - pd, (1, 0): pd}
                        elif hw2:
                            dhe = min(dh * (1 + self.c_mem), 0.999) if lw in u_states else dh   # she is entitled
                            pd = pic + (1 - pic) * dhe
                            pj = {(0, 0): 1 - pd, (0, 1): pd}
                        else:
                            pj = {(0, 0): 1.0}
                        lst = []
                        for (ew, eh), pe in pj.items():
                            wl = wd if ew else wnd
                            hl = hd if eh else hnd
                            for pw_, si in wl:
                                for ph_, hj in hl:
                                    if pe * pw_ * ph_ > 0:
                                        lst.append((pe * pw_ * ph_, si, hj))
                        state_cfg[lw, lh, state_n[lw, lh]] = len(cfgs)
                        state_n[lw, lh] += 1
                        cfgs.append((lw, lh, hw_, hh_))
                        outs.append(lst)
        nc = len(cfgs)
        self.ncfg = nc
        self.cfg_lw = np.array([c[0] for c in cfgs], np.int64)
        self.cfg_lh = np.array([c[1] for c in cfgs], np.int64)
        self.cfg_hw = np.array([c[2] for c in cfgs], np.int64)
        self.cfg_hh = np.array([c[3] for c in cfgs], np.int64)
        self.state_cfg, self.state_n = state_cfg, state_n
        mo = max(len(o) for o in outs)
        self.out_p = np.zeros((nc, mo))
        self.out_ws = np.zeros((nc, mo), np.int64)
        self.out_hs = np.zeros((nc, mo), np.int64)
        self.out_n = np.zeros(nc, np.int64)
        for i, o in enumerate(outs):
            self.out_n[i] = len(o)
            for j, (p_, a_, b_) in enumerate(o):
                self.out_p[i, j], self.out_ws[i, j], self.out_hs[i, j] = p_, a_, b_
            assert abs(sum(p_ for p_, _, _ in o) - 1) < 1e-12

        # separated wife: configs (lw, hours), own hazard dw only (no common shock), no husband
        cfgS, outS = [], []
        stS = -np.ones((NLW, 3), np.int64)
        stSn = np.zeros(NLW, np.int64)
        for lw in range(NLW):
            for hw_ in ((0, 1, 2) if lw in (E_, EN_) else (0,)):
                ww, wnd, wd = wife_events(lw, hw_)
                lst = []
                if ww:
                    lst += [((1 - dw) * p_, si) for p_, si in wnd] + [(dw * p_, si) for p_, si in wd]
                else:
                    lst += list(wnd)
                stS[lw, stSn[lw]] = len(cfgS)
                stSn[lw] += 1
                cfgS.append((lw, hw_))
                outS.append([x for x in lst if x[0] > 0])
        self.ncfgS = len(cfgS)
        self.cfgS_lw = np.array([c[0] for c in cfgS], np.int64)
        self.cfgS_hw = np.array([c[1] for c in cfgS], np.int64)
        self.stateS_cfg, self.stateS_n = stS, stSn
        mo = max(len(o) for o in outS)
        self.outS_p = np.zeros((self.ncfgS, mo))
        self.outS_ws = np.zeros((self.ncfgS, mo), np.int64)
        self.outS_n = np.zeros(self.ncfgS, np.int64)
        for i, o in enumerate(outS):
            self.outS_n[i] = len(o)
            for j, (p_, a_) in enumerate(o):
                self.outS_p[i, j], self.outS_ws[i, j] = p_, a_

        # ---------------- budget: income tables by age group --------------------------------------------------------
        chi, mu = sch["tax"]["chi"], sch["tax"]["mu"]
        cap = sch["ui"]["cap_month"] / 1000.0
        rho_ui = sch["ui"]["rho"]
        snapA = np.array(sch["snap"]["A"]) / 1000.0
        snapD = np.array(sch["snap"]["D"]) / 1000.0
        snapG = np.array(sch["snap"]["gross_limit"]) / 1000.0
        self.asset_limit = sch["snap"]["asset_limit"] / 1000.0
        if "no_snap" in ov:
            self.asset_limit = -1e9
        nch = np.array(fx["n_children"][R], dtype=float)              # (3 k, 7 g)
        share = np.array(fx["child_share"])
        s_M = fx["s_M"]
        F = th["F"]
        pcc = np.array(fx["p_cc"]) / 1000.0
        e1 = 1.0 + 2.0 * share[1]                                      # family of three: one adult and two children
        c_min_eq = sch["c_min_family3"] / 1000.0 / (s_M * e1)
        if "c_min" in ov:
            c_min_eq = ov["c_min"]
        self.c_min_eq = c_min_eq
        # equivalence scales and floors
        self.sc = np.zeros((N_AGE_GROUPS, NK))
        self.scS = np.zeros((N_AGE_GROUPS, NK))
        for g in range(N_AGE_GROUPS):
            for k in range(NK):
                e = 1.0 + nch[k, g] * share[k]
                self.sc[g, k] = s_M * e
                self.scS[g, k] = e
        self.xfloor = self.sc * c_min_eq - self.a_bar
        self.xfloorS = self.scS * c_min_eq - self.a_bar
        ui_lost_h = np.zeros(NLW)
        if cfg.lost_hours:
            ui_lost_h[UP_], ui_lost_h[UF_] = HP, HF
        else:
            ui_lost_h[UP_] = HF * fx["ui_pt_factor"]
        G = N_AGE_GROUPS
        ncarr = np.array(nch, dtype=int)                                # n children (3 k, 7 g)
        # married: arrays over (config, h_w, h_h, nu)
        cl_w, cl_h = self.cfg_lw, self.cfg_lh
        hrs_w, hrs_h = hours[self.cfg_hw], hours[self.cfg_hh]
        is_uw = np.isin(cl_w, u_states)
        bw = np.where(is_uw[:, None], np.minimum(rho_ui * wbar_w[None, :] * ui_lost_h[cl_w][:, None], cap), 0.0)
        bh = np.where((cl_h == 1)[:, None], np.minimum(rho_ui * wbar_h[None, :] * HF, cap), 0.0)
        yw = wbar_w[None, :, None] * np.exp(nu_w)[None, None, :] * hrs_w[:, None, None]      # (nc, H, NNU)
        yh = wbar_h[None, :, None] * np.exp(nu_h)[None, None, :] * hrs_h[:, None, None]
        YW, YH = yw[:, :, None, :], yh[:, None, :, :]
        BW, BH = bw[:, :, None, None], bh[:, None, :, None]
        earn = YW + YH
        gross = earn + BW + BH                                                                # (nc, H, H, NNU)
        tax = hsv_tax(12 * gross, chi, mu)
        fc = F * ((self.cfg_hw > 0).astype(float) + (self.cfg_hh > 0))
        base = gross - tax - fc[:, None, None, None]
        self.earn = np.stack(np.broadcast_arrays(YW, YH), axis=-1)                           # (nc, H, H, NNU, 2)
        self.ui = np.stack(np.broadcast_arrays(bw[:, :, None], bh[:, None, :]), axis=-1)     # (nc, H, H, 2)
        E_n = [eitc_month(earn, n, sch, True) for n in range(4)]
        self.inc0 = np.zeros((G, nc, H, H, NK, NNU))
        self.snapB = -np.ones((G, nc, H, H, NK, NNU))
        self.eitc_tab = np.zeros((G, nc, H, H, NK, NNU))
        for g in range(G):
            for k in range(NK):
                n = ncarr[k, g]
                ccc = (pcc[k] * hrs_w)[:, None, None, None]
                self.inc0[g, :, :, :, k, :] = base + E_n[min(n, 3)] - ccc
                self.eitc_tab[g, :, :, :, k, :] = E_n[min(n, 3)]
                nhh = int(2 + n)
                B = np.maximum(0.0, snapA[nhh - 1] - 0.3 * np.maximum(0.0, gross - 0.2 * earn - snapD[nhh - 1] - ccc))
                self.snapB[g, :, :, :, k, :] = np.where((gross <= snapG[nhh - 1]) & (B > 0), B, -1.0)
        if "no_snap" in ov:
            self.snapB[:] = -1.0
        # separated wife: arrays over (config, h_w, nu_w)
        clS = self.cfgS_lw
        hrsS = hours[self.cfgS_hw]
        bwS = np.where(np.isin(clS, u_states)[:, None],
                       np.minimum(rho_ui * wbar_w[None, :] * ui_lost_h[clS][:, None], cap), 0.0)[:, :, None]
        ywS = wbar_w[None, :, None] * np.exp(sig_nw * np.array([-1.0, 1.0]))[None, None, :] * hrsS[:, None, None]
        grossS = ywS + bwS
        baseS = grossS - hsv_tax(12 * grossS, chi, mu) - (F * (self.cfgS_hw > 0))[:, None, None]
        ES_n = [eitc_month(ywS, n, sch, False) for n in range(4)]
        self.incS0 = np.zeros((G, self.ncfgS, H, NK, 2))
        self.snapBS = -np.ones((G, self.ncfgS, H, NK, 2))
        self.eitcS_tab = np.zeros((G, self.ncfgS, H, NK, 2))
        self.uiS = bwS[:, :, 0].copy()
        for g in range(G):
            for k in range(NK):
                n = ncarr[k, g]
                ccc = (pcc[k] * hrsS)[:, None, None]
                self.incS0[g, :, :, k, :] = baseS + ES_n[min(n, 3)] - ccc
                self.eitcS_tab[g, :, :, k, :] = ES_n[min(n, 3)]
                nhh = int(1 + n)
                B = np.maximum(0.0, snapA[nhh - 1] - 0.3 * np.maximum(0.0, grossS - 0.2 * ywS - snapD[nhh - 1] - ccc))
                self.snapBS[g, :, :, k, :] = np.where((grossS <= snapG[nhh - 1]) & (B > 0), B, -1.0)
        if "no_snap" in ov:
            self.snapBS[:] = -1.0
        # disutility of work by config and child bucket
        theta_k = np.array([0.0, th["theta_05"], th["theta_617"]])
        self.disu = np.zeros((nc, NK))
        for c in range(nc):
            _, _, hw_, hh_ = cfgs[c]
            for k in range(NK):
                v = 0.0
                if hw_ == 2:
                    v += th["phi_F"] + theta_k[k]
                elif hw_ == 1:
                    v += th["phi_P"] + theta_k[k]
                if hh_ == 2:
                    v += th["phi_h"]
                self.disu[c, k] = v
        self.disuS = np.zeros((self.ncfgS, NK))
        for c in range(self.ncfgS):
            _, hw_ = cfgS[c]
            for k in range(NK):
                self.disuS[c, k] = (th["phi_F"] if hw_ == 2 else (th["phi_P"] if hw_ == 1 else 0.0)) + \
                    (theta_k[k] if hw_ > 0 else 0.0)

        # ---------------- terminal value (retirement at the wife's 60) ---------------------------------------------
        Rm = fx["ret_months"]
        r_ = self.rm
        af = r_ / (1 - (1 + r_) ** -Rm) if r_ > 0 else 1.0 / Rm
        rb_ = r_ + self.r_wedge                                      # debt at retirement annuitised at the borrowing rate
        af_b = rb_ / (1 - (1 + rb_) ** -Rm) if rb_ > 0 else 1.0 / Rm
        disc = (1 - self.beta ** Rm) / (1 - self.beta)
        ss = fx["ss_rate"]
        self.ret_af, self.ret_disc = af, disc
        a = self.agrid
        g_ = self.gamma
        u = (lambda x: np.log(x)) if g_ == 1 else (lambda x: (x ** (1 - g_) - 1) / (1 - g_))
        up = lambda x: x ** (-g_)
        self.VT = np.zeros((H, H, self.NA))
        self.DT = np.zeros((H, H, self.NA))
        cfl = s_M * c_min_eq
        for iw in range(H):
            for ih in range(H):
                afa = np.where(a < 0, af_b, af)
                c = afa * a + ss * (wbar_w[iw] + wbar_h[ih]) * HF
                fl = c < cfl
                c = np.maximum(c, cfl)
                self.VT[iw, ih] = disc * u(c / s_M)
                self.DT[iw, ih] = np.where(fl, 0.0, disc * afa * up(c / s_M) / s_M)
        self.VST = np.zeros((H, self.NA))
        self.DST = np.zeros((H, self.NA))
        for iw in range(H):
            c = af * a + ss * wbar_w[iw] * HF
            fl = c < c_min_eq
            c = np.maximum(c, c_min_eq)
            self.VST[iw] = disc * u(c)
            self.DST[iw] = np.where(fl, 0.0, disc * af * up(c))
        # separated assets at a'/2: interpolation of next month's V^S on the grid
        half = a / 2.0
        j = np.clip(np.searchsorted(a, half) - 1, 0, self.NA - 2)
        self.half_j = j.astype(np.int64)
        self.half_w = (half - a[j]) / (a[j + 1] - a[j])
        self.fixed = fx
        self.theta = th
