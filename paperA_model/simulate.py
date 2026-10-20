"""Paper A model: monthly simulation of couples with common random numbers.

Each simulated couple is a copy of an entry couple (inputs/psid_entry_couples.csv from IGE/62 when it exists; until
then a SYNTHETIC PLACEHOLDER population, synthetic_entry()). The entry file is re-read at every call of simulate()
(load_entry), so inputs produced while a run is set up are picked up. Couples are simulated problem by problem
(r, s, tau) and, within a problem, era by era: the era's solution is solved and stored, the couples' months that fall
in that era's calendar years are simulated, and the next era continues from their states (couples re-optimise at era
boundaries, D8). Months are simulated from the entry January to December of Config.sim_end_year (or the wife's 60th
birthday).

Common random numbers: every draw is a deterministic function of (seed, couple-copy id, month t, slot) through a
counter-based hash (splitmix64), so draws are identical across evaluations, parameter values and counterfactuals
without storing them. Slots: 0-17 taste shocks of the 18 canonical alternatives (hours_w, hours_h, S), 20 transitory
pair, 21 common displacement shock, 22-23 own hazards, 24-25 job finding, 26-27 UI take-up, 28-29 UI expiry,
30-31 own human capital step, 32 shared innovation, 33-34 idiosyncratic innovations, 35 child bucket, 36 separation,
40 couple type (t = 0), 41 the entitled wife's offer decision (accept / keep UI); measurement layer (panels.py):
50 consumption measurement error, 51 control-unit subsample of the PSID stacks.

Within the month (model document Section 6): January transitory draw; taste shocks; choice of (hours, SNAP) and
consumption from the stored EGM solution (the simulator re-solves the static monthly problem at the couple's own
assets); income; end-of-month displacement (common shock pi_c(s) hits every spouse who worked, otherwise own hazards
m_tau delta_j(r)), the husband's job finding and UI, then the wife's: job finding, and for an entitled wife the offer
decision (Bacher et al. 2025: decline and keep entitlement, which then expires with 1/6; accept ends it; logit with
the solver's index Dlt at her end-of-month assets and the husband's realised outcome), quit, human capital (sampled
from the same matrices the solver integrates over), child bucket, separation (assets halved, the wife continues
alone).

'Looking for work' (the CPS classification, sec7_model.tex footnote): a non-employed wife is looking in month t when
she would accept a job in her current state with probability above one half: an entitled wife if the offer-node
index at her end-of-month assets (husband's status unchanged) is positive; a wife without entitlement if the
probability of positive hours, had she a job this month (the employed state's alternatives at her state and assets),
exceeds 1/2. Husbands always look.

Records (one row per couple-copy, one column per calendar month from January 1984): FIELDS_F (float32), FIELDS_I
(int8; -1 = not in the sample that month). look: 1 looking / 0 not / -1 wife employed; acc: 1 accepted an offer at the
end of the month, 0 declined (kept entitlement), -1 no offer decision.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from numba import njit, prange

from model import Model, age_group
from params import Config, INPUTS, era_of_year, load_fixed
from solve import env_query, solve, util, mutil

FIELDS_F = ("c", "a", "yw", "yh", "bw", "bh", "eitc", "snap", "tr")
FIELDS_I = ("status", "lw", "lh", "hrs_w", "hrs_h", "hw", "hh", "k", "disp_w", "disp_h", "common", "sep", "look",
            "acc")
SEED = 20261018
M0 = 1984                                       # first calendar year of the record arrays


# --------------------------------------------------------------------------------------------------------------------
# counter-based uniforms (CRN)
# --------------------------------------------------------------------------------------------------------------------
@njit(cache=True, inline="always")
def u01(seed, uid, t, slot):
    x = np.uint64(seed) * np.uint64(0x9E3779B97F4A7C15)
    x ^= np.uint64(uid) * np.uint64(0xBF58476D1CE4E5B9)
    x ^= np.uint64(t + 7) * np.uint64(0x94D049BB133111EB)
    x ^= np.uint64(slot + 13) * np.uint64(0x2545F4914F6CDD1D)
    z = x + np.uint64(0x9E3779B97F4A7C15)
    z = (z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
    z = (z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
    z = z ^ (z >> np.uint64(31))
    return (np.float64(z >> np.uint64(11)) + 0.5) * (1.0 / 9007199254740992.0)


@njit(cache=True, inline="always")
def draw_row(idx, pr, n, u):
    c = 0.0
    for q in range(n):
        c += pr[q]
        if u < c:
            return idx[q]
    return idx[n - 1]


@njit(cache=True, inline="always")
def draw_dense(row, u):
    c = 0.0
    for q in range(row.shape[0]):
        c += row[q]
        if u < c:
            return q
    return row.shape[0] - 1


@njit(cache=True, inline="always")
def interp_grid(ag, y, x):
    """Linear interpolation of y on the asset grid ag at x (clamped to the grid)."""
    n = ag.shape[0]
    if x <= ag[0]:
        return y[0]
    if x >= ag[n - 1]:
        return y[n - 1]
    lo, hi = 0, n - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ag[mid] <= x:
            lo = mid
        else:
            hi = mid
    w = (x - ag[lo]) / (ag[lo + 1] - ag[lo])
    return y[lo] + w * (y[lo + 1] - y[lo])


# --------------------------------------------------------------------------------------------------------------------
@njit(cache=True, parallel=True)
def sim_kernel(seed, uid, row, t_beg, t_end, m_off, st_a, st_lw, st_lh, st_hw, st_hh, st_k, st_nu, st_mar, st_t,
               C, Wv, CS, WS, agrid, state_cfg, state_n, cfg_hw, cfg_hh, inc0, snapB, disu, sc, xfl, stS_cfg, stS_n,
               cfgS_hw, incS0, snapBS, disuS, scS, xflS, earn, ui, eitc_t, eitcS_t, uiS, asset_limit, beta, g, rm, sig,
               kappaS, pnu, pic, dw, dh, lamw, lamh, q, ex, sigE, sigN, sep_share, Aw_idx, Aw_p, Aw_n, Ah_idx, Ah_p,
               Ah_n, Iw, Ih, Is, pc, Pk, E_, UP_, UF_, N_, sigw, recF, recI, Dlt, DltS, ui_acc, herm, rwedge, cmem, jL,
               EN_, xinj, gnj, njui, sjw):
    """Simulate couples i from month t_beg[i] to t_end[i] (inclusive) with this era's stored solution; records go to
    row row[i] of the record arrays. Extensions (2026-10-19; inactive with EN_ = -1, sjw = 0): EN_ = the new-job
    state (exit hazard xinj after the displacement draws, CRN slot 42; established with gnj, slot 43; njui: the exit is a
    displacement with UI take-up); sjw = separation hazard added while she is UI-entitled next month."""
    NC = uid.shape[0]
    E_in = EN_ if EN_ >= 0 else E_                        # state a wife enters when she takes a job
    NA = agrid.shape[0]
    R = 1.0 + rm
    H = Iw.shape[0]
    for i in prange(NC):
        Xe = np.empty(NA)
        ce = np.empty(NA)
        Wl = np.empty(NA)
        Dn = np.empty(NA)
        dlt = np.empty(NA)
        a = st_a[i]
        lw = st_lw[i]
        lh = st_lh[i]
        hw = st_hw[i]
        hh = st_hh[i]
        k = st_k[i]
        nu = st_nu[i]
        mar = st_mar[i]
        u_ = uid[i]
        rw = row[i]
        for t in range(t_beg[i], t_end[i] + 1):
            m = m_off[i] + t
            gq = min(t // 60, 6)
            if t % 12 == 0:                                   # January: new transitory pair
                uu = u01(seed, u_, t, 20)
                if mar == 1:
                    nu = draw_dense(pnu, uu)
                else:
                    nu = 2 * (1 if uu < 0.5 else 0) + (nu % 2)
            best = -1e300
            bc = 0.0
            bX = 0.0
            bxp = 0.0
            bcfg = -1
            bS = 0
            jn = nu // 2
            if mar == 1:
                s_c = sc[gq, k]
                xf = xfl[gq, k]
                for ci in range(state_n[lw, lh]):
                    c = state_cfg[lw, lh, ci]
                    mono = True
                    for j in range(NA):
                        ce[j] = C[t, c, hw, hh, k, nu, j]
                        Wl[j] = Wv[t, c, hw, hh, k, nu, j]
                        Dn[j] = mutil(ce[j] / s_c, g) / (beta * s_c)
                        Xe[j] = ce[j] + agrid[j]
                        if j > 0 and Xe[j] <= Xe[j - 1]:
                            mono = False
                    for S in range(2):
                        B = snapB[gq, c, hw, hh, k, nu]
                        if S == 1 and (B < 0.0 or a > asset_limit):
                            continue
                        xp = (R + rwedge if a < 0.0 else R) * a + inc0[gq, c, hw, hh, k, nu] + (B if S == 1 else 0.0)
                        X = xp if xp > xf else xf
                        cc, vv = env_query(X, Xe, ce, Wl, Dn, agrid, s_c, beta, g, mono, herm, jL)
                        slot = (cfg_hw[c] * 3 + cfg_hh[c]) * 2 + S
                        e = -np.log(-np.log(u01(seed, u_, t, slot)))
                        val = vv - disu[c, k] - (kappaS if S == 1 else 0.0) + sig * e
                        if val > best:
                            best, bc, bX, bxp, bcfg, bS = val, cc, X, xp, c, S
                hrs_w = cfg_hw[bcfg]
                hrs_h = cfg_hh[bcfg]
                recF[0, rw, m] = bc
                recF[1, rw, m] = a
                recF[2, rw, m] = earn[bcfg, hw, hh, nu, 0]
                recF[3, rw, m] = earn[bcfg, hw, hh, nu, 1]
                recF[4, rw, m] = ui[bcfg, hw, hh, 0]
                recF[5, rw, m] = ui[bcfg, hw, hh, 1]
                recF[6, rw, m] = eitc_t[gq, bcfg, hw, hh, k, nu]
                recF[7, rw, m] = snapB[gq, bcfg, hw, hh, k, nu] if bS == 1 else 0.0
                recF[8, rw, m] = bX - bxp if bX > bxp else 0.0
            else:
                s_c = scS[gq, k]
                xf = xflS[gq, k]
                for ci in range(stS_n[lw]):
                    c = stS_cfg[lw, ci]
                    mono = True
                    for j in range(NA):
                        ce[j] = CS[t, c, hw, k, jn, j]
                        Wl[j] = WS[t, c, hw, k, jn, j]
                        Dn[j] = mutil(ce[j] / s_c, g) / (beta * s_c)
                        Xe[j] = ce[j] + agrid[j]
                        if j > 0 and Xe[j] <= Xe[j - 1]:
                            mono = False
                    for S in range(2):
                        B = snapBS[gq, c, hw, k, jn]
                        if S == 1 and (B < 0.0 or a > asset_limit):
                            continue
                        xp = (R + rwedge if a < 0.0 else R) * a + incS0[gq, c, hw, k, jn] + (B if S == 1 else 0.0)
                        X = xp if xp > xf else xf
                        cc, vv = env_query(X, Xe, ce, Wl, Dn, agrid, s_c, beta, g, mono, herm, jL)
                        slot = (cfgS_hw[c] * 3) * 2 + S
                        e = -np.log(-np.log(u01(seed, u_, t, slot)))
                        val = vv - disuS[c, k] - (kappaS if S == 1 else 0.0) + sig * e
                        if val > best:
                            best, bc, bX, bxp, bcfg, bS = val, cc, X, xp, c, S
                hrs_w = cfgS_hw[bcfg]
                hrs_h = 0
                recF[0, rw, m] = bc
                recF[1, rw, m] = a
                recF[2, rw, m] = 0.0                       # filled by _fill_sep_earnings
                recF[3, rw, m] = 0.0
                recF[4, rw, m] = uiS[bcfg, hw]
                recF[5, rw, m] = 0.0
                recF[6, rw, m] = eitcS_t[gq, bcfg, hw, k, jn]
                recF[7, rw, m] = snapBS[gq, bcfg, hw, k, jn] if bS == 1 else 0.0
                recF[8, rw, m] = bX - bxp if bX > bxp else 0.0
            recI[0, rw, m] = mar
            recI[1, rw, m] = lw
            recI[2, rw, m] = lh if mar == 1 else -1
            recI[3, rw, m] = hrs_w
            recI[4, rw, m] = hrs_h
            recI[5, rw, m] = hw
            recI[6, rw, m] = hh
            recI[7, rw, m] = k
            a_next = bX - bc
            # ---------------- 'looking for work' of a non-employed wife (CPS classification) ----------------
            look = -1
            works_w = (lw == E_ or lw == EN_) and hrs_w > 0
            if not works_w:
                if lw == E_ or lw == EN_:
                    look = 0                                       # holds a job and chose not to work this month
                elif ui_acc and lw != N_ and lw != EN_:
                    ee = lw - 1                                    # entitled state index (u_states start at 1)
                    if mar == 1:
                        j0 = (0 if hrs_h == 2 else 1) if lh == 0 else 2 + lh
                        for j in range(NA):
                            dlt[j] = Dlt[t, ee, j0, hw, hh, k, nu, j]
                    else:
                        for j in range(NA):
                            dlt[j] = DltS[t, ee, hw, k, jn, j]
                    look = 1 if interp_grid(agrid, dlt, a_next) > 0.0 else 0
                else:
                    # P(positive hours | she had a job this month) from the employed state's alternatives
                    mx = -1e300
                    nalt = 0
                    vbuf = np.empty(12)
                    wbuf = np.empty(12)
                    if mar == 1:
                        s_c = sc[gq, k]
                        xf = xfl[gq, k]
                        for ci in range(state_n[E_in, lh]):
                            c = state_cfg[E_in, lh, ci]
                            mono = True
                            for j in range(NA):
                                ce[j] = C[t, c, hw, hh, k, nu, j]
                                Wl[j] = Wv[t, c, hw, hh, k, nu, j]
                                Dn[j] = mutil(ce[j] / s_c, g) / (beta * s_c)
                                Xe[j] = ce[j] + agrid[j]
                                if j > 0 and Xe[j] <= Xe[j - 1]:
                                    mono = False
                            for S in range(2):
                                B = snapB[gq, c, hw, hh, k, nu]
                                if S == 1 and (B < 0.0 or a > asset_limit):
                                    continue
                                xp = (R + rwedge if a < 0.0 else R) * a + inc0[gq, c, hw, hh, k, nu] + \
                                    (B if S == 1 else 0.0)
                                X = xp if xp > xf else xf
                                cc, vv = env_query(X, Xe, ce, Wl, Dn, agrid, s_c, beta, g, mono, herm, jL)
                                vbuf[nalt] = vv - disu[c, k] - (kappaS if S == 1 else 0.0)
                                wbuf[nalt] = 1.0 if cfg_hw[c] > 0 else 0.0
                                if vbuf[nalt] > mx:
                                    mx = vbuf[nalt]
                                nalt += 1
                    else:
                        s_c = scS[gq, k]
                        xf = xflS[gq, k]
                        for ci in range(stS_n[E_in]):
                            c = stS_cfg[E_in, ci]
                            mono = True
                            for j in range(NA):
                                ce[j] = CS[t, c, hw, k, jn, j]
                                Wl[j] = WS[t, c, hw, k, jn, j]
                                Dn[j] = mutil(ce[j] / s_c, g) / (beta * s_c)
                                Xe[j] = ce[j] + agrid[j]
                                if j > 0 and Xe[j] <= Xe[j - 1]:
                                    mono = False
                            for S in range(2):
                                B = snapBS[gq, c, hw, k, jn]
                                if S == 1 and (B < 0.0 or a > asset_limit):
                                    continue
                                xp = (R + rwedge if a < 0.0 else R) * a + incS0[gq, c, hw, k, jn] + \
                                    (B if S == 1 else 0.0)
                                X = xp if xp > xf else xf
                                cc, vv = env_query(X, Xe, ce, Wl, Dn, agrid, s_c, beta, g, mono, herm, jL)
                                vbuf[nalt] = vv - disuS[c, k] - (kappaS if S == 1 else 0.0)
                                wbuf[nalt] = 1.0 if cfgS_hw[c] > 0 else 0.0
                                if vbuf[nalt] > mx:
                                    mx = vbuf[nalt]
                                nalt += 1
                    sa = 0.0
                    sw_ = 0.0
                    for q_ in range(nalt):
                        ev_ = np.exp((vbuf[q_] - mx) / sig)
                        sa += ev_
                        sw_ += ev_ * wbuf[q_]
                    look = 1 if sw_ > 0.5 * sa else 0
            recI[12, rw, m] = look
            # ---------------- end-of-month labor-market events ----------------
            works_h = mar == 1 and lh == 0
            dsp_w = False
            dsp_h = False
            com = False
            if mar == 1 and (works_w or works_h) and u01(seed, u_, t, 21) < pic:
                com = True
                dsp_w = works_w
                dsp_h = works_h
            else:
                dw_t = dw
                dh_t = dh
                if mar == 1 and lh == 1:                       # memory: he is non-employed and UI-entitled
                    dw_t = min(dw * (1.0 + cmem), 0.999)
                if lw != E_ and lw != N_ and lw != EN_:       # memory: she is non-employed and UI-entitled
                    dh_t = min(dh * (1.0 + cmem), 0.999)
                if works_w and u01(seed, u_, t, 22) < dw_t:
                    dsp_w = True
                if works_h and u01(seed, u_, t, 23) < dh_t:
                    dsp_h = True
            # husband first (the wife's offer decision is taken knowing his outcome)
            lh2 = lh
            cat_h = 2
            jh = 0
            if mar == 1:
                if works_h:
                    if dsp_h:
                        cat_h = 3
                        lh2 = 1 if u01(seed, u_, t, 27) < q else 2
                    else:
                        cat_h = 0 if hrs_h == 2 else 1
                        lh2 = 0
                else:
                    if u01(seed, u_, t, 25) < lamh:
                        lh2 = 0
                    elif lh == 1 and u01(seed, u_, t, 29) < ex:
                        lh2 = 2
                # husband slice index (model.hsl order: F, P, NW-0, NW-1, NW-2, D-1, D-2)
                if cat_h == 0:
                    jh = 0
                elif cat_h == 1:
                    jh = 1
                elif cat_h == 2:
                    jh = 2 + lh2
                else:
                    jh = 4 + lh2
            # wife's next labor state and human capital category
            acc = -1
            if works_w:
                if dsp_w:
                    cat_w = 3
                    if u01(seed, u_, t, 26) < q:
                        lw2 = UF_ if hrs_w == 2 else UP_
                    else:
                        lw2 = N_
                else:
                    cat_w = 0 if hrs_w == 2 else 1
                    lw2 = E_
                    if lw == EN_:                                  # new job: exit, or established with gnj
                        if u01(seed, u_, t, 42) < xinj:
                            if njui:                               # exit treated as a displacement
                                dsp_w = True
                                cat_w = 3
                                if u01(seed, u_, t, 26) < q:
                                    lw2 = UF_ if hrs_w == 2 else UP_
                                else:
                                    lw2 = N_
                            else:                                  # exit treated as a quit
                                cat_w = 2
                                lw2 = N_
                        elif u01(seed, u_, t, 43) >= gnj:
                            lw2 = EN_
            elif lw == E_ or lw == EN_:
                cat_w = 2
                lw2 = N_                                           # quits a job: not entitled
            else:
                cat_w = 2
                if u01(seed, u_, t, 24) < lamw:
                    if ui_acc and lw != N_:
                        ee = lw - 1
                        if mar == 1:
                            for j in range(NA):
                                dlt[j] = Dlt[t, ee, jh, hw, hh, k, nu, j]
                        else:
                            for j in range(NA):
                                dlt[j] = DltS[t, ee, hw, k, jn, j]
                        x_ = interp_grid(agrid, dlt, a_next)
                        pa = 1.0 / (1.0 + np.exp(-x_)) if x_ > -700.0 else 0.0
                        if u01(seed, u_, t, 41) < pa:
                            lw2 = E_in
                            acc = 1
                        else:
                            acc = 0
                            lw2 = N_ if u01(seed, u_, t, 28) < ex else lw
                    else:
                        lw2 = E_in
                elif lw != N_ and u01(seed, u_, t, 28) < ex:
                    lw2 = N_
                else:
                    lw2 = lw
            recI[13, rw, m] = acc
            # human capital: own step, shared innovation, idiosyncratic innovation
            hw2 = draw_row(Aw_idx[cat_w, hw], Aw_p[cat_w, hw], Aw_n[cat_w, hw], u01(seed, u_, t, 30))
            if mar == 1:
                hh2 = draw_row(Ah_idx[cat_h, hh], Ah_p[cat_h, hh], Ah_n[cat_h, hh], u01(seed, u_, t, 31))
                us = u01(seed, u_, t, 32)
                if us < pc:
                    if us < 0.5 * pc:
                        hw2 = min(hw2 + 1, H - 1)
                        hh2 = min(hh2 + 1, H - 1)
                    else:
                        hw2 = max(hw2 - 1, 0)
                        hh2 = max(hh2 - 1, 0)
                hw2 = draw_dense(Iw[hw2], u01(seed, u_, t, 33))
                hh2 = draw_dense(Ih[hh2], u01(seed, u_, t, 34))
            else:
                hh2 = hh
                hw2 = draw_dense(Is[hw2], u01(seed, u_, t, 33))
            k2 = draw_dense(Pk[gq, k], u01(seed, u_, t, 35))
            sep = 0
            if mar == 1:
                ps = sigE if lh2 == 0 else sigN
                if sjw > 0.0 and lw2 != E_ and lw2 != N_ and lw2 != EN_:   # she is UI-entitled (extension)
                    ps = min(ps + sjw, 1.0)
                if u01(seed, u_, t, 36) < ps:
                    sep = 1
                    mar = 0
                    a_next = a_next * sep_share
            recI[8, rw, m] = 1 if dsp_w else 0
            recI[9, rw, m] = 1 if dsp_h else 0
            recI[10, rw, m] = 1 if com else 0
            recI[11, rw, m] = sep
            a = a_next
            lw, lh, hw, hh, k = lw2, lh2, hw2, hh2, k2
        st_a[i] = a
        st_lw[i] = lw
        st_lh[i] = lh
        st_hw[i] = hw
        st_hh[i] = hh
        st_k[i] = k
        st_nu[i] = nu
        st_mar[i] = mar


# --------------------------------------------------------------------------------------------------------------------
# entry population
# --------------------------------------------------------------------------------------------------------------------
def synthetic_entry(n=5000, seed=7) -> pd.DataFrame:
    """SYNTHETIC PLACEHOLDER for inputs/psid_entry_couples.csv (IGE/62): calendar entry year, wife's age, race, match,
    liquid wealth (thousand 2000 $), employment, youngest-child bucket, human capital levels 1-7, UI flags."""
    rng = np.random.default_rng(seed)
    first = rng.random(n) < 0.4
    year0 = np.where(first, 1984, rng.integers(1985, 2022, n))
    age0 = np.where(first, rng.integers(25, 56, n), rng.integers(25, 36, n))
    race = (rng.random(n) >= 0.26).astype(int)                 # 0 = Black, 1 = White
    s = rng.choice(3, n, p=[0.823, 0.114, 0.063])
    neg = rng.random(n) < 0.5
    a0 = np.where(neg, -rng.uniform(0, 3, n), np.exp(rng.normal(np.log(5), 1.2, n)))
    ew0 = (rng.random(n) < 0.75).astype(int)
    eh0 = (rng.random(n) < 0.95).astype(int)
    k0 = np.where(age0 < 35, rng.choice(3, n, p=[0.3, 0.6, 0.1]),
                  np.where(age0 < 45, rng.choice(3, n, p=[0.25, 0.25, 0.5]), rng.choice(3, n, p=[0.6, 0.0, 0.4])))
    hw0 = np.clip(4 + np.round(rng.normal(0, 1, n)), 1, 7).astype(int)
    hh0 = np.clip(4 + np.round(rng.normal(0, 1, n)), 1, 7).astype(int)
    return pd.DataFrame(dict(id=np.arange(n), year0=year0, age0=age0, race=race, s=s, a0=a0, ew0=ew0, eh0=eh0, k0=k0,
                             hw0=hw0, hh0=hh0, uw0=0, uh0=0))


ENTRY_COLS = ("id", "year0", "age0", "race", "s", "a0", "ew0", "eh0", "k0", "hw0", "hh0", "uw0", "uh0")


def load_entry() -> tuple[pd.DataFrame, str]:
    """inputs/psid_entry_couples.csv (IGE/62) if it exists and has the required columns, else the synthetic
    placeholder. Read at every call (no caching), so a file written while runs are being set up is used."""
    p = INPUTS / "psid_entry_couples.csv"
    if p.exists():
        e = pd.read_csv(p)
        miss = [c for c in ENTRY_COLS if c not in e]
        for c in ("uw0", "uh0"):
            if c in miss:
                e[c] = 0
                miss.remove(c)
        if not miss:
            return e, str(p)
        print(f"WARNING {p} lacks columns {miss}: using the synthetic placeholder population")
    return synthetic_entry(), "SYNTHETIC PLACEHOLDER (synthetic_entry)"


def level_to_index(lev, H):
    """PSID level 1..7 -> grid index on an H-level grid spanning the same range."""
    return np.clip(np.round((np.asarray(lev) - 4) * (H - 1) / 6.0 + (H - 1) / 2.0), 0, H - 1).astype(np.int64)


# --------------------------------------------------------------------------------------------------------------------
class SimResult:
    def __init__(self, n, nm):
        self.F = np.zeros((len(FIELDS_F), n, nm), np.float32)
        self.I = np.full((len(FIELDS_I), n, nm), -1, np.int8)
        self.info = {}

    def f(self, name):
        return self.F[FIELDS_F.index(name)]

    def i(self, name):
        return self.I[FIELDS_I.index(name)]


def simulate(theta: dict, cfg: Config, entry: pd.DataFrame | None = None, K: int = 3, seed: int = SEED,
             overrides: dict | None = None, problems=None, fixed=None, timing: dict | None = None,
             solution_hook=None) -> SimResult:
    """Solve and simulate every problem; returns monthly records for all couple-copies.
    problems: optional subset of (r, s, tau); overrides: test switches passed to Model."""
    import time
    fx = load_fixed() if fixed is None else fixed
    if entry is None:
        entry, src = load_entry()
    else:
        src = "given"
    ent = entry.loc[entry.index.repeat(K)].reset_index(drop=True)
    ent["copy"] = np.tile(np.arange(K), len(entry))
    n = len(ent)
    uid = (ent["id"].to_numpy() * K + ent["copy"].to_numpy()).astype(np.int64)
    # couple type from a CRN uniform (slot 40)
    ut = _u01_vec(np.array([seed]), uid, np.zeros(n, np.int64), np.full(n, 40, np.int64))
    tau = (ut < theta["p_H"]).astype(int)
    s_eff = ent["s"].to_numpy().copy()
    if cfg.merge_s12:
        s_eff = np.minimum(s_eff, 1)
    nm = (cfg.sim_end_year - M0 + 1) * 12
    res = SimResult(n, nm)
    res.info["tau"] = tau
    res.info["entry"] = ent
    res.info["entry_source"] = src
    res.info["uid"] = uid
    res.info["seed"] = seed
    res.info["EN"] = cfg.n_lw if fx.get("new_job", False) else -1     # new-job state index (extension; -1 = none)
    H = cfg.n_hc
    t0 = 12 * (ent["age0"].to_numpy() - 25)
    m_off = ((ent["year0"].to_numpy() - M0) * 12 - t0).astype(np.int64)     # calendar index m = m_off + t
    res.info["m_off"] = m_off
    t_last = np.minimum(cfg.T - 1, (cfg.sim_end_year - M0 + 1) * 12 - 1 - m_off)
    ok = t_last >= t0
    tim = timing if timing is not None else {}
    tim.setdefault("solve", 0.0)
    tim.setdefault("sim", 0.0)
    herm = getattr(cfg, "w_interp", "hermite") == "hermite"
    probs = problems if problems is not None else cfg.problems()
    for (r, s, tp) in probs:
        sel = np.nonzero((ent["race"].to_numpy() == r) & (s_eff == s) & (tau == tp) & ok)[0]
        if len(sel) == 0:
            continue
        # states
        st_a = ent["a0"].to_numpy()[sel].astype(float)
        st_hw = level_to_index(ent["hw0"].to_numpy()[sel], H)
        st_hh = level_to_index(ent["hh0"].to_numpy()[sel], H)
        st_k = ent["k0"].to_numpy()[sel].astype(np.int64)
        st_t = t0[sel].astype(np.int64)
        st_mar = np.ones(len(sel), np.int64)
        st_nu = np.zeros(len(sel), np.int64)
        lwE, lwU, lwN = 0, (2 if cfg.lost_hours else 1), (3 if cfg.lost_hours else 2)
        ew, uw = ent["ew0"].to_numpy()[sel], ent["uw0"].to_numpy()[sel]
        eh, uh = ent["eh0"].to_numpy()[sel], ent["uh0"].to_numpy()[sel]
        st_lw = np.where(ew == 1, lwE, np.where(uw == 1, lwU, lwN)).astype(np.int64)
        st_lh = np.where(eh == 1, 0, np.where(uh == 1, 1, 2)).astype(np.int64)
        eras = cfg.eras()
        for e in eras:
            ts = time.perf_counter()
            mdl = Model(theta, cfg, e, r, s, tp, fixed=fx, overrides=overrides)
            st_a = np.clip(st_a, mdl.agrid[0], mdl.agrid[-1])
            sol = solve(mdl, store=True)
            if solution_hook is not None:
                solution_hook((r, s, tp, e), mdl, sol)
            tim["solve"] += time.perf_counter() - ts
            ts = time.perf_counter()
            # months of this era for each couple: calendar years inside the era (all years if one era)
            if cfg.one_era:
                y_lo, y_hi = 0, 9999
            else:
                y_lo, y_hi = {1: (0, 1996), 2: (1997, 2008), 3: (2009, 9999)}[e]
            m_lo = (y_lo - M0) * 12 if y_lo > 0 else -10 ** 9
            m_hi = (y_hi - M0 + 1) * 12 - 1 if y_hi < 9999 else 10 ** 9
            moff = m_off[sel]
            tb = np.maximum(st_t, m_lo - moff)
            te = np.minimum(t_last[sel], m_hi - moff)
            sim_kernel(seed, uid[sel], sel.astype(np.int64), tb.astype(np.int64), te.astype(np.int64), moff, st_a,
                       st_lw, st_lh, st_hw, st_hh, st_k, st_nu, st_mar, st_t, sol.C, sol.W, sol.CS, sol.WS, mdl.agrid,
                       mdl.state_cfg, mdl.state_n, mdl.cfg_hw, mdl.cfg_hh, mdl.inc0, mdl.snapB, mdl.disu, mdl.sc,
                       mdl.xfloor, mdl.stateS_cfg, mdl.stateS_n, mdl.cfgS_hw, mdl.incS0, mdl.snapBS, mdl.disuS,
                       mdl.scS, mdl.xfloorS, mdl.earn, mdl.ui, mdl.eitc_tab, mdl.eitcS_tab, mdl.uiS, mdl.asset_limit,
                       mdl.beta, mdl.gamma, mdl.rm, mdl.sigma_eps, mdl.kappa_S, mdl.pnu, mdl.pic, mdl.dw, mdl.dh,
                       mdl.lw_, mdl.lh_, mdl.qui, mdl.ui_exp, mdl.sig_E, mdl.sig_N, fx["sep_asset_share"],
                       mdl.Aw_idx, mdl.Aw_p, mdl.Aw_n, mdl.Ah_idx, mdl.Ah_p, mdl.Ah_n, mdl.Iw, mdl.Ih, mdl.Is,
                       mdl.p_c, mdl.Pk, mdl.E_, mdl.UP_, mdl.UF_, mdl.N_, 0.0, res.F, res.I, sol.Dlt, sol.DltS,
                       bool(mdl.ui_accept), herm, mdl.r_wedge, mdl.c_mem, mdl.jL, mdl.EN_, mdl.xi_nj, mdl.g_nj,
                       bool(mdl.nj_ui), mdl.sig_Jw)
            # separated wife's earnings (the kernel leaves a placeholder): her wage x hours of the chosen config
            _fill_sep_earnings(res, sel, tb, te, moff, mdl)
            # couples whose era window was empty keep their state; st_t moved only where te >= tb
            st_t = np.where(te >= tb, te + 1, st_t)
            tim["sim"] += time.perf_counter() - ts
            del sol
    return res


def _fill_sep_earnings(res, sel, tb, te, moff, mdl):
    """Separated wives' monthly earnings yw = wbar_w(h) exp(nu_w) x hours (the married records carry the earnings
    table of the chosen configuration; the separated wife's is computed here from her records)."""
    st = res.I[0]
    hrs = res.I[3]
    hwi = res.I[5]
    yw = res.F[2]
    for q, i in enumerate(sel):
        if te[q] < tb[q]:
            continue
        m0, m1 = moff[q] + tb[q], moff[q] + te[q] + 1
        s_ = st[i, m0:m1]
        mk = s_ == 0
        if not mk.any():
            continue
        hcode = hrs[i, m0:m1][mk].astype(int)
        lev = hwi[i, m0:m1][mk].astype(int)
        hours = mdl.hours[np.clip(hcode, 0, 2)]
        # transitory component of a separated wife: sign from her January draw is not recorded; use nu = 0
        # (her earnings enter no target: every earnings moment is on married couples)
        yw[i, m0:m1][mk] = (mdl.wbar_w[lev] * hours).astype(np.float32)


def _u01_py(seed, uid, t, slot):
    return float(_u01_vec(np.array([seed]), np.array([uid]), np.array([t]), np.array([slot]))[0])


@njit(cache=True)
def _u01_vec(seed, uid, t, slot):
    out = np.empty(uid.shape[0])
    for i in range(uid.shape[0]):
        out[i] = u01(seed[0], uid[i], t[i], slot[i])
    return out
