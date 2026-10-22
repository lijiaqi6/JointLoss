"""Paper A model: monthly backward induction for one problem (r, s, tau) and one era (DC-EGM with Gumbel taste shocks).

Method (Iskhakov, Jorgensen, Rust and Schjerning 2017, as in Bacher et al. 2025). For month t, given next month's
value V_{t+1} and its derivative in assets D_{t+1} on the asset grid for every married state, and V^S_{t+1}, D^S_{t+1}
for the separated wife:

 1. Separation and the transitory shock (k_tilde): next month's married value mixed with the separated wife's value at
    half the assets, with hazard sigma(r, e_h') = sigma_0 + sigma_J 1{husband non-employed}; the expectation over the
    transitory pair is degenerate within the year and the four-point sum over a new draw when t+1 is a January.
 2. Child bucket (k_child): 3 x 3 monthly chain by the wife's age group.
 3. Human capital, sequential operators. Forward, a level moves by the own step A[cat] (accumulation /
    depreciation / displacement loss), then the shared innovation, then the idiosyncratic innovation; backward, the
    expectation applies the idiosyncratic operators I_w, I_h and the shared operator J to the whole array (they do not
    depend on the month's labor events; k_hc), then A_h[cat] and A_w[cat] for the (category, next labor state) pairs
    that occur (k_husb, k_wife). This is exact: the shared shift sits between the own step and the idiosyncratic one.
 4. EGM and the discrete choice (k_egm): for every state and work configuration the expected continuation W(a') and
    its derivative D(a') are the probability-weighted sum of the slices of step 3 over the month's labor outcomes
    (displacement with the common shock and own hazards, job finding, the wife's quit, UI take-up and expiry). The
    Euler equation gives consumption at each end-of-month asset point a': u'(c / sc) / sc = beta D(a'); the
    endogenous cash-on-hand grid X = c + a' with the borrowing limit a' >= -a_bar. Cash on hand of an alternative at
    asset a is X = max{(1 + r) a + income(d), sc c_min - a_bar} (the consumption floor: the minimal transfer that lets
    the household spend c_min per equivalent adult at the borrowing limit). The value of an alternative at X is the
    upper envelope over all EGM segments containing X and the constrained choice a' = -a_bar (the upper-envelope step
    of DC-EGM, evaluated at the query point; a fast path is used when the endogenous grid is monotone). SNAP is part
    of the alternative (S = 1 feasible if the income test holds and a <= asset limit); it shifts cash on hand and
    utility only, so both S share W. The logsum over the feasible alternatives with scale sigma_eps gives V_t, and
    D_t = sum_d P(d) (1 + r) u'(c_d / sc) / sc (zero where the floor binds).

 5. Offer node (k_offer, k_offer_sep; UI and acceptance, Bacher et al. 2025, lead decision 2026-10-18): for an entitled
    non-employed wife who receives an offer, the continuation is the logsum of accepting (employed next month) and
    declining (entitlement kept unless it expires), stored as virtual wife slices nI + e of the expectation array; the
    logit index is stored (Dlt) for the simulator.

Continuation value between asset nodes (2026-10-18): cubic Hermite from the node values W and the node derivatives D
(the expected derivative the Euler step inverts; in the simulator recovered from the stored consumption,
D = u'(c / sc) / (beta sc)), monotone-limited (wval); the EGM point is polished by Newton steps on the Hermite
first-order condition where consumption changes by more than POLISH_TOL between the bracketing endogenous points
(polish); above the last endogenous point consumption is extrapolated (never below the last point) and W continues
with the top node's derivative (extrap_top). With chords (Config.w_interp = 'linear', the stage-3 code) the
brute-force check failed because the chord optimum sticks to grid nodes; see tests/test_0.

Storage for the simulator: consumption at the endogenous points C[t, cfg, ...] and W[t, cfg, ...] (float32), from
which the simulator rebuilds the value and consumption of every alternative at any cash on hand (model document:
'the simulator re-solves each couple's static monthly problem from this array'), and the offer-node index Dlt.
"""
from __future__ import annotations

import time

import numba as nb
import numpy as np
from numba import njit, prange

from model import Model, age_group

EULER = 0.5772156649015329
NEG = -1e30
# polish the EGM point (Newton on the Hermite first-order condition) when consumption changes by more than this share
# between the two endogenous points that bracket the query (linear interpolation of c in cash on hand is coarse there)
POLISH_TOL = 0.05


@njit(cache=True, inline="always")
def util(x, g):
    if g == 1.5:                      # fast path for the calibrated gamma (sqrt instead of pow)
        return 2.0 - 2.0 / np.sqrt(x)
    if g == 1.0:
        return np.log(x)
    return (x ** (1.0 - g) - 1.0) / (1.0 - g)


@njit(cache=True, inline="always")
def mutil(x, g):
    if g == 1.5:
        return 1.0 / (x * np.sqrt(x))
    return x ** (-g)


@njit(cache=True, inline="always")
def inv_mutil(m, g):
    """x with u'(x) = m."""
    if g == 1.5:
        y = np.cbrt(m)
        return 1.0 / (y * y)
    return m ** (-1.0 / g)


@njit(cache=True, inline="always")
def mutil2(x, g):
    """u''(x)."""
    if g == 1.5:
        return -1.5 / (x * x * np.sqrt(x))
    return -g * x ** (-g - 1.0)


@njit(cache=True, inline="always")
def wval(W, Dn, ag, p, s, herm):
    """Continuation value at local coordinate s in [0, 1] of asset segment p. herm: cubic Hermite interpolation from
    the node values W and node derivatives Dn (the exact expected derivative the EGM step inverts), with the
    derivatives limited to [0, 3 x chord slope] so that the cubic stays monotone (Fritsch-Carlson); otherwise linear."""
    w0 = W[p]
    w1 = W[p + 1]
    if not herm:
        return w0 + s * (w1 - w0)
    h = ag[p + 1] - ag[p]
    dl = (w1 - w0) / h
    if dl <= 0.0:
        return w0 + s * (w1 - w0)
    d0 = Dn[p]
    d1 = Dn[p + 1]
    if d0 < 0.0:
        d0 = 0.0
    if d1 < 0.0:
        d1 = 0.0
    if d0 > 3.0 * dl:
        d0 = 3.0 * dl
    if d1 > 3.0 * dl:
        d1 = 3.0 * dl
    s2 = s * s
    s3 = s2 * s
    return (2.0 * s3 - 3.0 * s2 + 1.0) * w0 + (s3 - 2.0 * s2 + s) * h * d0 + (3.0 * s2 - 2.0 * s3) * w1 + \
        (s3 - s2) * h * d1


@njit(cache=True, inline="always")
def wder(W, Dn, ag, p, s):
    """First and second derivative in a' of the (limited) Hermite continuation value on segment p at s."""
    w0 = W[p]
    w1 = W[p + 1]
    h = ag[p + 1] - ag[p]
    dl = (w1 - w0) / h
    if dl <= 0.0:
        return dl, 0.0
    d0 = Dn[p]
    d1 = Dn[p + 1]
    if d0 < 0.0:
        d0 = 0.0
    if d1 < 0.0:
        d1 = 0.0
    if d0 > 3.0 * dl:
        d0 = 3.0 * dl
    if d1 > 3.0 * dl:
        d1 = 3.0 * dl
    s2 = s * s
    f1 = (6.0 * s2 - 6.0 * s) * w0 + (3.0 * s2 - 4.0 * s + 1.0) * h * d0 + (6.0 * s - 6.0 * s2) * w1 + \
        (3.0 * s2 - 2.0 * s) * h * d1
    f2 = (12.0 * s - 6.0) * w0 + (6.0 * s - 4.0) * h * d0 + (6.0 - 12.0 * s) * w1 + (6.0 * s - 2.0) * h * d1
    return f1 / h, f2 / (h * h)


@njit(cache=True, inline="always")
def polish(X, c, v, p, W, Dn, ag, sc, beta, g):
    """Two Newton steps from the EGM point (c, v) on the first-order condition beta W'(a') = u'((X - a') / sc) / sc
    with the Hermite W of segment p, clamped to the segment and to a' < X; returns the best of the points visited.
    Between two endogenous points EGM interpolates consumption linearly in cash on hand, which is coarse in a wide
    asset segment; the polish makes the value at X the maximum over a' to second order.
    A segment where the marginal value rises (Dn[p + 1] > Dn[p]: W convex there, e.g. to the right of the SNAP
    asset-limit drop, where spending down to the limit next month is an option) is also searched on 9 points and
    polished with up to 6 Newton steps (2026-10-18 fix of check 0)."""
    aL = ag[p]
    aR = ag[p + 1]
    hseg = aR - aL
    ub = aR if aR < X - 1e-9 else X - 1e-9
    if ub <= aL:
        return c, v
    ap = X - c
    if ap < aL:
        ap = aL
    if ap > ub:
        ap = ub
    cb, vb = c, v
    nit = 2
    if Dn[p + 1] > Dn[p]:
        nit = 6
        for q_ in range(9):
            aq = aL + (ub - aL) * q_ / 8.0
            vq = util((X - aq) / sc, g) + beta * wval(W, Dn, ag, p, (aq - aL) / hseg, True)
            if vq > vb:
                cb, vb = X - aq, vq
                ap = aq
    for _it in range(nit):
        f1, f2 = wder(W, Dn, ag, p, (ap - aL) / hseg)
        cc_ = X - ap
        fo = beta * f1 - mutil(cc_ / sc, g) / sc
        fd = beta * f2 + mutil2(cc_ / sc, g) / (sc * sc)
        if fd >= 0.0:
            break
        step = fo / fd
        if abs(step) < 1e-7 * hseg:
            break
        ap = ap - step
        if ap < aL:
            ap = aL
        if ap > ub:
            ap = ub
        cn = X - ap
        vn = util(cn / sc, g) + beta * wval(W, Dn, ag, p, (ap - aL) / hseg, True)
        if vn > vb:
            cb, vb = cn, vn
    return cb, vb


@njit(cache=True, inline="always")
def extrap_top(X, Xe, ce, W, Dn, ag, sc, beta, g, herm):
    """Cash on hand above the last endogenous point: consumption extrapolated linearly from the last two endogenous
    points but never below the last one (consumption is non-decreasing in cash on hand; a falling top segment would
    otherwise drive it negative), a' = X - c, W beyond the top node linear with the node derivative (both
    representations). The chord slope must not be used: it can exceed the node derivative, and the extrapolated value
    then feeds back month after month (W explodes at the top of the grid)."""
    n = Xe.shape[0]
    w = (X - Xe[n - 2]) / (Xe[n - 1] - Xe[n - 2])
    c = ce[n - 2] + w * (ce[n - 1] - ce[n - 2])
    if c < ce[n - 1]:
        c = ce[n - 1]
    ap = X - c
    sl = Dn[n - 1] if Dn[n - 1] > 0.0 else 0.0
    return c, util(c / sc, g) + beta * (W[n - 1] + sl * (ap - ag[n - 1]))


@njit(cache=True, fastmath=True)
def env_query(X, Xe, ce, W, Dn, ag, sc, beta, g, mono, herm, jL):
    """env_query_core plus the corner a' = ag[jL] (the SNAP asset limit, where next month's value drops; jL < 0:
    none): with a drop in W the first-order conditions miss the bunching at the limit, so the corner is compared.
    An endogenous grid that is monotone on both sides of the limit but not across it (Xe[jL + 1] < Xe[jL]: the
    drop) is handled as two monotone branches (two_branch), not by the segment search of the non-monotone case."""
    split = (not mono) and jL >= 1 and split_mono(Xe, jL)
    return env_query_k(X, Xe, ce, W, Dn, ag, sc, beta, g, mono, split, herm, jL)


@njit(cache=True, fastmath=True)
def env_query_k(X, Xe, ce, W, Dn, ag, sc, beta, g, mono, split, herm, jL):
    """env_query with the two-branch flag computed once per configuration (the EGM kernels)."""
    if split:
        c, v = two_branch(X, Xe, ce, W, Dn, ag, sc, beta, g, herm, jL)
    else:
        c, v = env_query_core(X, Xe, ce, W, Dn, ag, sc, beta, g, mono, herm)
    if jL >= 0 and ag[jL] < X:
        cc = X - ag[jL]
        vv = util(cc / sc, g) + beta * W[jL]
        if vv > v:
            return cc, vv
    return c, v


@njit(cache=True)
def split_mono(Xe, jL):
    """True if Xe increases on the branch above the asset limit (nodes jL + 1 .. n - 1); the branch below may be
    non-monotone (near the borrowing limit) and the step from jL to jL + 1 may fall (the drop)."""
    for i in range(jL + 1, Xe.shape[0] - 1):
        if Xe[i + 1] <= Xe[i]:
            return False
    return True


@njit(cache=True, inline="always")
def branch_interp(X, Xe, ce, W, Dn, ag, sc, beta, g, herm, lo, hi):
    """EGM interpolation at X on the monotone branch of endogenous points lo..hi (Xe[lo] <= X <= Xe[hi]), with the
    polish of the segment; returns (c, v)."""
    a, b = lo, hi
    while b - a > 1:
        mid = (a + b) // 2
        if Xe[mid] <= X:
            a = mid
        else:
            b = mid
    i = a
    w = (X - Xe[i]) / (Xe[i + 1] - Xe[i])
    c = ce[i] + w * (ce[i + 1] - ce[i])
    v = util(c / sc, g) + beta * wval(W, Dn, ag, i, w, herm)
    if herm and (abs(ce[i + 1] - ce[i]) > POLISH_TOL * c or Dn[i + 1] > Dn[i]):
        c, v = polish(X, c, v, i, W, Dn, ag, sc, beta, g)
    return c, v


@njit(cache=True, inline="always")
def two_branch(X, Xe, ce, W, Dn, ag, sc, beta, g, herm, jL):
    """Best of: the constrained choice a' = ag[0]; the left branch (nodes 0..jL, a' <= L): EGM interpolation if it is
    monotone and X lies in its endogenous range, otherwise env_query_core on the left nodes alone (its candidates
    above L discarded) when X is below the branch's highest endogenous point; the right branch (nodes jL+1..n-1,
    a' > L, monotone) if X lies at or above its first endogenous point (above the last point the top extrapolation).
    The corner a' = L is added by env_query_k. Splitting at the limit keeps the segment search of a non-monotone
    grid on the few nodes below L instead of every node up to the drop."""
    n = Xe.shape[0]
    a0 = ag[0]
    cb = X - a0
    vb = util(cb / sc, g) + beta * W[0]
    lmono = True
    lmax = Xe[0]
    for i in range(jL):
        if Xe[i + 1] <= Xe[i]:
            lmono = False
        if Xe[i + 1] > lmax:
            lmax = Xe[i + 1]
    if lmono:
        if Xe[0] < X <= Xe[jL] and jL >= 1:
            c, v = branch_interp(X, Xe, ce, W, Dn, ag, sc, beta, g, herm, 0, jL)
            if 0.0 < c <= X - a0 and v > vb:
                cb, vb = c, v
    elif X <= lmax:
        c, v = env_query_core(X, Xe[:jL + 1], ce[:jL + 1], W[:jL + 1], Dn[:jL + 1], ag[:jL + 1], sc, beta, g,
                              False, herm)
        if 0.0 < c <= X - a0 and X - c <= ag[jL] + 1e-12 and v > vb:
            cb, vb = c, v
    if X >= Xe[jL + 1]:
        if X > Xe[n - 1]:
            c, v = extrap_top(X, Xe, ce, W, Dn, ag, sc, beta, g, herm)
        elif jL + 1 <= n - 2:
            c, v = branch_interp(X, Xe, ce, W, Dn, ag, sc, beta, g, herm, jL + 1, n - 1)
        else:
            c, v = -1.0, -1e300
        if 0.0 < c <= X - a0 and v > vb:
            cb, vb = c, v
    return cb, vb


@njit(cache=True, fastmath=True)
def env_query_core(X, Xe, ce, W, Dn, ag, sc, beta, g, mono, herm):
    """Consumption and value (before work disutility) at cash on hand X from one configuration's EGM solution
    (endogenous grid Xe = ce + ag, continuation W on the asset grid ag, its node derivatives Dn).
    Monotone grid: linear interpolation of consumption between endogenous points (constrained below Xe[0]); the value
    is u(c / sc) + beta W(a') with W between nodes from wval (Hermite by default).
    Non-monotone grid (a non-concave continuation value, typically near the borrowing limit where next month's
    consumption floor flattens the value): the EGM interpolation is used only on the monotone tail of the endogenous
    grid above every earlier point; below it, the maximum of u((X - a') / sc) + beta W(a') over the low segments is
    computed segment by segment (closed-form stationary point of the chord, then two Newton steps on the Hermite
    first-order condition, clamped to the segment), the upper envelope over all local optima there, together with the
    constrained choice a' = ag[0]."""
    a0 = ag[0]
    ccon = X - a0
    vcon = util(ccon / sc, g) + beta * W[0]
    n = Xe.shape[0]
    if mono:
        if X <= Xe[0]:
            return ccon, vcon
        if X >= Xe[n - 1]:
            i = n - 2
        else:
            lo, hi = 0, n - 1
            while hi - lo > 1:
                mid = (lo + hi) // 2
                if Xe[mid] <= X:
                    lo = mid
                else:
                    hi = mid
            i = lo
        if X > Xe[n - 1]:                            # above the last endogenous point
            c, v = extrap_top(X, Xe, ce, W, Dn, ag, sc, beta, g, herm)
            if c > ccon or v < vcon:
                return ccon, vcon
            return c, v
        w = (X - Xe[i]) / (Xe[i + 1] - Xe[i])
        c = ce[i] + w * (ce[i + 1] - ce[i])
        if c > ccon or c <= 0.0:
            return ccon, vcon
        v = util(c / sc, g) + beta * wval(W, Dn, ag, i, w, herm)
        if herm and (abs(ce[i + 1] - ce[i]) > POLISH_TOL * c or Dn[i + 1] > Dn[i]):
            c, v = polish(X, c, v, i, W, Dn, ag, sc, beta, g)
        if v < vcon:
            return ccon, vcon
        return c, v
    # start of the monotone tail that lies above every earlier endogenous point
    t0 = n - 1
    while t0 > 0 and Xe[t0 - 1] < Xe[t0]:
        t0 -= 1
    m0 = -1e300
    for i in range(t0):
        if Xe[i] > m0:
            m0 = Xe[i]
    i0 = n - 1
    for i in range(t0, n):
        if Xe[i] > m0:
            i0 = i
            break
    cb, vb = ccon, vcon
    if i0 <= n - 2 and X >= Xe[i0]:
        if X >= Xe[n - 1]:
            i = n - 2
        else:
            lo, hi = i0, n - 1
            while hi - lo > 1:
                mid = (lo + hi) // 2
                if Xe[mid] <= X:
                    lo = mid
                else:
                    hi = mid
            i = lo
        w = (X - Xe[i]) / (Xe[i + 1] - Xe[i])
        c = ce[i] + w * (ce[i + 1] - ce[i])
        if X > Xe[n - 1]:
            c, v = extrap_top(X, Xe, ce, W, Dn, ag, sc, beta, g, herm)
            if c <= ccon and v > vb:
                cb, vb = c, v
        elif 0.0 < c <= ccon:
            v = util(c / sc, g) + beta * wval(W, Dn, ag, i, w, herm)
            if herm and (abs(ce[i + 1] - ce[i]) > POLISH_TOL * c or Dn[i + 1] > Dn[i]):
                c, v = polish(X, c, v, i, W, Dn, ag, sc, beta, g)
            if v > vb:
                cb, vb = c, v
        return cb, vb
    jmax = i0 if i0 <= n - 2 else n - 2
    for j in range(jmax + 1):
        aL = ag[j]
        aR = ag[j + 1]
        if aL >= X:
            break
        hseg = aR - aL
        s = (W[j + 1] - W[j]) / hseg
        if s > 0.0:
            ap = X - sc * inv_mutil(beta * s * sc, g)
        else:
            ap = aL
        if ap < aL:
            ap = aL
        if ap > aR:
            ap = aR
        top = X - 1e-9
        if ap > top:
            ap = top
            if ap < aL:
                continue
        c = X - ap
        v = util(c / sc, g) + beta * wval(W, Dn, ag, j, (ap - aL) / hseg, herm)
        if v > vb:
            cb, vb = c, v
        if herm:
            # Newton steps on beta W'(a') = u'((X - a') / sc) / sc within the segment; where W is convex on the segment
            # (rising marginal value, e.g. next to the SNAP asset-limit drop) started from the best of the chord point
            # and 9 points across the segment (2026-10-18: the maximum can sit far from the chord point there)
            ub = aR if aR < top else top
            nq = 9 if Dn[j + 1] > Dn[j] else 0              # scan only where W is convex (marginal value rises)
            for q_ in range(nq):
                aq = aL + (ub - aL) * q_ / 8.0
                if aq >= X:
                    continue
                vq = util((X - aq) / sc, g) + beta * wval(W, Dn, ag, j, (aq - aL) / hseg, herm)
                if vq > v:
                    ap, v = aq, vq
                    if vq > vb:
                        cb, vb = X - aq, vq
            for _it in range(6 if nq > 0 else 2):
                sl = (ap - aL) / hseg
                f1, f2 = wder(W, Dn, ag, j, sl)
                cc_ = X - ap
                fo = beta * f1 - mutil(cc_ / sc, g) / sc
                fd = beta * f2 + mutil2(cc_ / sc, g) / (sc * sc)
                if fd >= 0.0:
                    break
                if abs(fo / fd) < 1e-7 * hseg:
                    break
                ap = ap - fo / fd
                if ap < aL:
                    ap = aL
                if ap > ub:
                    ap = ub
                c = X - ap
                v = util(c / sc, g) + beta * wval(W, Dn, ag, j, (ap - aL) / hseg, herm)
                if v > vb:
                    cb, vb = c, v
    return cb, vb


# --------------------------------------------------------------------------------------------------------------------
# married problem kernels
# --------------------------------------------------------------------------------------------------------------------
@njit(cache=True, parallel=True, fastmath=True)
def k_half(VS1, DS1, hj, hw_, VSh, DSh):
    NLW, H, NK, NJ, NA = VS1.shape
    for b in prange(NLW * H):
        lw = b // H
        iw = b % H
        for k in range(NK):
            for j in range(NJ):
                for a in range(NA):
                    i = hj[a]
                    w = hw_[a]
                    VSh[lw, iw, k, j, a] = (1 - w) * VS1[lw, iw, k, j, i] + w * VS1[lw, iw, k, j, i + 1]
                    DSh[lw, iw, k, j, a] = 0.5 * ((1 - w) * DS1[lw, iw, k, j, i] + w * DS1[lw, iw, k, j, i + 1])


@njit(cache=True, parallel=True, fastmath=True)
def k_tilde(VM1, DM1, VSh, DSh, sigE, sigN, jan, pnu, TV, TD):
    NLW, NLH, H, _, NK, NNU, NA = VM1.shape
    for b in prange(NLW * NLH):
        lw = b // NLH
        lh = b % NLH
        sg = sigE if lh == 0 else sigN
        for hw in range(H):
            for hh in range(H):
                for k in range(NK):
                    for nu in range(NNU):
                        iw = nu // 2
                        for a in range(NA):
                            if jan:
                                vm = 0.0
                                dm = 0.0
                                for n2 in range(NNU):
                                    vm += pnu[n2] * VM1[lw, lh, hw, hh, k, n2, a]
                                    dm += pnu[n2] * DM1[lw, lh, hw, hh, k, n2, a]
                                vs = 0.5 * (VSh[lw, hw, k, 0, a] + VSh[lw, hw, k, 1, a])
                                ds = 0.5 * (DSh[lw, hw, k, 0, a] + DSh[lw, hw, k, 1, a])
                            else:
                                vm = VM1[lw, lh, hw, hh, k, nu, a]
                                dm = DM1[lw, lh, hw, hh, k, nu, a]
                                vs = VSh[lw, hw, k, iw, a]
                                ds = DSh[lw, hw, k, iw, a]
                            TV[lw, lh, hw, hh, k, nu, a] = (1 - sg) * vm + sg * vs
                            TD[lw, lh, hw, hh, k, nu, a] = (1 - sg) * dm + sg * ds


@njit(cache=True, parallel=True, fastmath=True)
def k_tilde_w(VM1, DM1, VSh, DSh, SG, jan, pnu, TV, TD):
    """k_tilde with the separation hazard by next month's (lw, lh), SG[lw, lh] (her-displacement extension, 2026-10-19:
    sigma_0 + sigma_J 1{he is non-employed} + sigma_Jw 1{she is UI-entitled}); the base model uses k_tilde."""
    NLW, NLH, H, _, NK, NNU, NA = VM1.shape
    for b in prange(NLW * NLH):
        lw = b // NLH
        lh = b % NLH
        sg = SG[lw, lh]
        for hw in range(H):
            for hh in range(H):
                for k in range(NK):
                    for nu in range(NNU):
                        iw = nu // 2
                        for a in range(NA):
                            if jan:
                                vm = 0.0
                                dm = 0.0
                                for n2 in range(NNU):
                                    vm += pnu[n2] * VM1[lw, lh, hw, hh, k, n2, a]
                                    dm += pnu[n2] * DM1[lw, lh, hw, hh, k, n2, a]
                                vs = 0.5 * (VSh[lw, hw, k, 0, a] + VSh[lw, hw, k, 1, a])
                                ds = 0.5 * (DSh[lw, hw, k, 0, a] + DSh[lw, hw, k, 1, a])
                            else:
                                vm = VM1[lw, lh, hw, hh, k, nu, a]
                                dm = DM1[lw, lh, hw, hh, k, nu, a]
                                vs = VSh[lw, hw, k, iw, a]
                                ds = DSh[lw, hw, k, iw, a]
                            TV[lw, lh, hw, hh, k, nu, a] = (1 - sg) * vm + sg * vs
                            TD[lw, lh, hw, hh, k, nu, a] = (1 - sg) * dm + sg * ds


@njit(cache=True, parallel=True, fastmath=True)
def k_child(TV, TD, P):
    NLW, NLH, H, _, NK, NNU, NA = TV.shape
    for b in prange(NLW * NLH * H):
        lw = b // (NLH * H)
        lh = (b // H) % NLH
        hw = b % H
        tv = np.empty((NK, NA))
        td = np.empty((NK, NA))
        for hh in range(H):
            for nu in range(NNU):
                for k in range(NK):
                    for a in range(NA):
                        sv = 0.0
                        sd = 0.0
                        for k2 in range(NK):
                            p = P[k, k2]
                            if p != 0.0:
                                sv += p * TV[lw, lh, hw, hh, k2, nu, a]
                                sd += p * TD[lw, lh, hw, hh, k2, nu, a]
                        tv[k, a] = sv
                        td[k, a] = sd
                for k in range(NK):
                    for a in range(NA):
                        TV[lw, lh, hw, hh, k, nu, a] = tv[k, a]
                        TD[lw, lh, hw, hh, k, nu, a] = td[k, a]


@njit(cache=True, parallel=True, fastmath=True)
def k_hc(TV, TD, Iw, Ih, pc):
    """Idiosyncratic operators on both levels, then the shared innovation J (backward order)."""
    NLW, NLH, H, _, NK, NNU, NA = TV.shape
    for b in prange(NLW * NLH * NK * NNU):
        lw = b // (NLH * NK * NNU)
        lh = (b // (NK * NNU)) % NLH
        k = (b // NNU) % NK
        nu = b % NNU
        av = np.empty((H, H, NA))
        ad = np.empty((H, H, NA))
        bv = np.empty((H, H, NA))
        bd = np.empty((H, H, NA))
        # I_h along hh
        for hw in range(H):
            for hh in range(H):
                for a in range(NA):
                    sv = 0.0
                    sd = 0.0
                    for h2 in range(H):
                        p = Ih[hh, h2]
                        if p != 0.0:
                            sv += p * TV[lw, lh, hw, h2, k, nu, a]
                            sd += p * TD[lw, lh, hw, h2, k, nu, a]
                    av[hw, hh, a] = sv
                    ad[hw, hh, a] = sd
        # I_w along hw
        for hw in range(H):
            for hh in range(H):
                for a in range(NA):
                    sv = 0.0
                    sd = 0.0
                    for h2 in range(H):
                        p = Iw[hw, h2]
                        if p != 0.0:
                            sv += p * av[h2, hh, a]
                            sd += p * ad[h2, hh, a]
                    bv[hw, hh, a] = sv
                    bd[hw, hh, a] = sd
        # J: shared +-1 shift of both levels with prob pc
        for hw in range(H):
            up_w = min(hw + 1, H - 1)
            dn_w = max(hw - 1, 0)
            for hh in range(H):
                up_h = min(hh + 1, H - 1)
                dn_h = max(hh - 1, 0)
                for a in range(NA):
                    TV[lw, lh, hw, hh, k, nu, a] = (1 - pc) * bv[hw, hh, a] + 0.5 * pc * (bv[up_w, up_h, a] + bv[dn_w, dn_h, a])
                    TD[lw, lh, hw, hh, k, nu, a] = (1 - pc) * bd[hw, hh, a] + 0.5 * pc * (bd[up_w, up_h, a] + bd[dn_w, dn_h, a])


@njit(cache=True, parallel=True, fastmath=True)
def k_husb(TV, TD, hs_cat, hs_lh, A_idx, A_p, A_n, YV, YD):
    NLW, NLH, H, _, NK, NNU, NA = TV.shape
    NJ = hs_cat.shape[0]
    for b in prange(NJ * NLW):
        j = b // NLW
        lw = b % NLW
        cat = hs_cat[j]
        lh2 = hs_lh[j]
        for hw in range(H):
            for hh in range(H):
                for k in range(NK):
                    for nu in range(NNU):
                        for a in range(NA):
                            sv = 0.0
                            sd = 0.0
                            for q in range(A_n[cat, hh]):
                                h2 = A_idx[cat, hh, q]
                                p = A_p[cat, hh, q]
                                sv += p * TV[lw, lh2, hw, h2, k, nu, a]
                                sd += p * TD[lw, lh2, hw, h2, k, nu, a]
                            YV[j, lw, hw, hh, k, nu, a] = sv
                            YD[j, lw, hw, hh, k, nu, a] = sd


@njit(cache=True, parallel=True, fastmath=True)
def k_wife(YV, YD, ws_cat, ws_lw, A_idx, A_p, A_n, GV, GD):
    NJ, NLW, H, _, NK, NNU, NA = YV.shape
    NI = ws_cat.shape[0]
    for b in prange(NI * NJ):
        i = b // NJ
        j = b % NJ
        cat = ws_cat[i]
        lw2 = ws_lw[i]
        for hw in range(H):
            for hh in range(H):
                for k in range(NK):
                    for nu in range(NNU):
                        for a in range(NA):
                            sv = 0.0
                            sd = 0.0
                            for q in range(A_n[cat, hw]):
                                h2 = A_idx[cat, hw, q]
                                p = A_p[cat, hw, q]
                                sv += p * YV[j, lw2, h2, hh, k, nu, a]
                                sd += p * YD[j, lw2, h2, hh, k, nu, a]
                            GV[i, j, hw, hh, k, nu, a] = sv
                            GD[i, j, hw, hh, k, nu, a] = sd


@njit(cache=True, parallel=True, fastmath=True)
def k_egm(GV, GD, state_cfg, state_n, out_p, out_ws, out_hs, out_n, inc0, snapB, disu, sc_k, xf_k, agrid,
          asset_limit, beta, g, rm, sig, kappaS, store, Cst, Wst, VM, DM, nchunks, herm, rw, jL):
    NI, NJ, H, _, NK, NNU, NA = GV.shape
    NLW, NLH = state_n.shape
    NS = NLW * NLH * H * H * NK * NNU
    a0 = agrid[0]
    R = 1.0 + rm
    for ch in prange(nchunks):
        W = np.empty(NA)
        D = np.empty(NA)
        Xe = np.empty(NA)
        ce = np.empty(NA)
        vals = np.empty((12, NA))
        dvs = np.empty((12, NA))
        for st in range(ch, NS, nchunks):       # interleaved: states differ in cost (employed vs not), balance threads
            nu = st % NNU
            k = (st // NNU) % NK
            hh = (st // (NNU * NK)) % H
            hw = (st // (NNU * NK * H)) % H
            lh = (st // (NNU * NK * H * H)) % NLH
            lw = st // (NNU * NK * H * H * NLH)
            sc = sc_k[k]
            xf = xf_k[k]
            nalt = 0
            for ci in range(state_n[lw, lh]):
                c = state_cfg[lw, lh, ci]
                for a in range(NA):
                    W[a] = 0.0
                    D[a] = 0.0
                for o in range(out_n[c]):
                    p = out_p[c, o]
                    i = out_ws[c, o]
                    j = out_hs[c, o]
                    for a in range(NA):
                        W[a] += p * GV[i, j, hw, hh, k, nu, a]
                        D[a] += p * GD[i, j, hw, hh, k, nu, a]
                mono = True
                for a in range(NA):
                    dd = D[a]
                    if dd < 1e-12:
                        dd = 1e-12
                    ce[a] = sc * inv_mutil(beta * dd * sc, g)
                    Xe[a] = ce[a] + agrid[a]
                    if a > 0 and Xe[a] <= Xe[a - 1]:
                        mono = False
                split = (not mono) and jL >= 1 and split_mono(Xe, jL)
                if store:
                    for a in range(NA):
                        Cst[c, hw, hh, k, nu, a] = ce[a]
                        Wst[c, hw, hh, k, nu, a] = W[a]
                for S in range(2):
                    B = snapB[c, hw, hh, k, nu]
                    if S == 1 and B < 0.0:
                        continue
                    inc = inc0[c, hw, hh, k, nu] + (B if S == 1 else 0.0)
                    dis = disu[c, k] + (kappaS if S == 1 else 0.0)
                    ptr = 0
                    for a in range(NA):
                        if S == 1 and agrid[a] > asset_limit:
                            vals[nalt, a] = NEG
                            dvs[nalt, a] = 0.0
                            continue
                        Ra = R + rw if agrid[a] < 0.0 else R            # borrowing wedge on debt
                        xp = Ra * agrid[a] + inc
                        X = xp if xp > xf else xf
                        if mono:
                            # queries ascend in a: merge scan along the monotone endogenous grid
                            if X <= Xe[0]:
                                cc = X - a0
                                vv = util(cc / sc, g) + beta * W[0]
                            else:
                                while ptr < NA - 2 and Xe[ptr + 1] <= X:
                                    ptr += 1
                                w = (X - Xe[ptr]) / (Xe[ptr + 1] - Xe[ptr])
                                cc = ce[ptr] + w * (ce[ptr + 1] - ce[ptr])
                                if cc > X - a0:
                                    cc = X - a0
                                    vv = util(cc / sc, g) + beta * W[0]
                                elif X > Xe[NA - 1]:
                                    cc, vv = extrap_top(X, Xe, ce, W, D, agrid, sc, beta, g, herm)
                                    if cc > X - a0:
                                        cc = X - a0
                                        vv = util(cc / sc, g) + beta * W[0]
                                else:
                                    vv = util(cc / sc, g) + beta * wval(W, D, agrid, ptr, w, herm)
                                    if herm and (abs(ce[ptr + 1] - ce[ptr]) > POLISH_TOL * cc or D[ptr + 1] > D[ptr]):
                                        cc, vv = polish(X, cc, vv, ptr, W, D, agrid, sc, beta, g)
                        else:
                            cc, vv = env_query_k(X, Xe, ce, W, D, agrid, sc, beta, g, mono, split, herm, jL)
                        if mono and jL >= 0 and agrid[jL] < X:      # corner at the SNAP asset limit
                            ccr = X - agrid[jL]
                            vcr = util(ccr / sc, g) + beta * W[jL]
                            if vcr > vv:
                                cc, vv = ccr, vcr
                        vals[nalt, a] = vv - dis
                        dvs[nalt, a] = Ra * mutil(cc / sc, g) / sc if xp >= xf else 0.0
                    nalt += 1
            for a in range(NA):
                m = NEG
                for q in range(nalt):
                    if vals[q, a] > m:
                        m = vals[q, a]
                se = 0.0
                sd = 0.0
                for q in range(nalt):
                    if vals[q, a] > NEG * 0.5:
                        e = np.exp((vals[q, a] - m) / sig)
                        se += e
                        sd += e * dvs[q, a]
                VM[lw, lh, hw, hh, k, nu, a] = m + sig * np.log(se) + sig * EULER
                DM[lw, lh, hw, hh, k, nu, a] = sd / se


# --------------------------------------------------------------------------------------------------------------------
# separated wife kernels
# --------------------------------------------------------------------------------------------------------------------
@njit(cache=True, fastmath=True)
def k_sep_expect(VS1, DS1, jan, P, Is, ws_cat, ws_lw, A_idx, A_p, A_n, GSV, GSD):
    NLW, H, NK, NJ, NA = VS1.shape
    tv = np.empty((NLW, H, NK, NJ, NA))
    td = np.empty((NLW, H, NK, NJ, NA))
    for lw in range(NLW):
        for hw in range(H):
            for k in range(NK):
                for j in range(NJ):
                    for a in range(NA):
                        if jan:
                            tv[lw, hw, k, j, a] = 0.5 * (VS1[lw, hw, k, 0, a] + VS1[lw, hw, k, 1, a])
                            td[lw, hw, k, j, a] = 0.5 * (DS1[lw, hw, k, 0, a] + DS1[lw, hw, k, 1, a])
                        else:
                            tv[lw, hw, k, j, a] = VS1[lw, hw, k, j, a]
                            td[lw, hw, k, j, a] = DS1[lw, hw, k, j, a]
    # child
    uv = np.zeros((NLW, H, NK, NJ, NA))
    ud = np.zeros((NLW, H, NK, NJ, NA))
    for lw in range(NLW):
        for hw in range(H):
            for k in range(NK):
                for k2 in range(NK):
                    p = P[k, k2]
                    if p != 0.0:
                        for j in range(NJ):
                            for a in range(NA):
                                uv[lw, hw, k, j, a] += p * tv[lw, hw, k2, j, a]
                                ud[lw, hw, k, j, a] += p * td[lw, hw, k2, j, a]
    # innovation
    tv[:] = 0.0
    td[:] = 0.0
    for lw in range(NLW):
        for hw in range(H):
            for h2 in range(H):
                p = Is[hw, h2]
                if p != 0.0:
                    for k in range(NK):
                        for j in range(NJ):
                            for a in range(NA):
                                tv[lw, hw, k, j, a] += p * uv[lw, h2, k, j, a]
                                td[lw, hw, k, j, a] += p * ud[lw, h2, k, j, a]
    # own step per (category, next labor state)
    NI = ws_cat.shape[0]
    for i in range(NI):
        cat = ws_cat[i]
        lw2 = ws_lw[i]
        for hw in range(H):
            for k in range(NK):
                for j in range(NJ):
                    for a in range(NA):
                        sv = 0.0
                        sd = 0.0
                        for q in range(A_n[cat, hw]):
                            h2 = A_idx[cat, hw, q]
                            p = A_p[cat, hw, q]
                            sv += p * tv[lw2, h2, k, j, a]
                            sd += p * td[lw2, h2, k, j, a]
                        GSV[i, hw, k, j, a] = sv
                        GSD[i, hw, k, j, a] = sd


@njit(cache=True, fastmath=True)
def k_egm_sep(GSV, GSD, stS_cfg, stS_n, outS_p, outS_ws, outS_n, inc0, snapB, disu, sc_k, xf_k, agrid,
              asset_limit, beta, g, rm, sig, kappaS, store, Cst, Wst, VS, DS, herm, rw, jL):
    NI, H, NK, NJ, NA = GSV.shape
    NLW = stS_n.shape[0]
    a0 = agrid[0]
    R = 1.0 + rm
    W = np.empty(NA)
    D = np.empty(NA)
    Xe = np.empty(NA)
    ce = np.empty(NA)
    vals = np.empty((6, NA))
    dvs = np.empty((6, NA))
    for lw in range(NLW):
        for hw in range(H):
            for k in range(NK):
                sc = sc_k[k]
                xf = xf_k[k]
                for j in range(NJ):
                    nalt = 0
                    for ci in range(stS_n[lw]):
                        c = stS_cfg[lw, ci]
                        for a in range(NA):
                            W[a] = 0.0
                            D[a] = 0.0
                        for o in range(outS_n[c]):
                            p = outS_p[c, o]
                            i = outS_ws[c, o]
                            for a in range(NA):
                                W[a] += p * GSV[i, hw, k, j, a]
                                D[a] += p * GSD[i, hw, k, j, a]
                        mono = True
                        for a in range(NA):
                            dd = D[a]
                            if dd < 1e-12:
                                dd = 1e-12
                            ce[a] = sc * inv_mutil(beta * dd * sc, g)
                            Xe[a] = ce[a] + agrid[a]
                            if a > 0 and Xe[a] <= Xe[a - 1]:
                                mono = False
                        split = (not mono) and jL >= 1 and split_mono(Xe, jL)
                        if store:
                            for a in range(NA):
                                Cst[c, hw, k, j, a] = ce[a]
                                Wst[c, hw, k, j, a] = W[a]
                        for S in range(2):
                            B = snapB[c, hw, k, j]
                            if S == 1 and B < 0.0:
                                continue
                            inc = inc0[c, hw, k, j] + (B if S == 1 else 0.0)
                            dis = disu[c, k] + (kappaS if S == 1 else 0.0)
                            ptr = 0
                            for a in range(NA):
                                if S == 1 and agrid[a] > asset_limit:
                                    vals[nalt, a] = NEG
                                    dvs[nalt, a] = 0.0
                                    continue
                                Ra = R + rw if agrid[a] < 0.0 else R    # borrowing wedge on debt
                                xp = Ra * agrid[a] + inc
                                X = xp if xp > xf else xf
                                if mono:
                                    # queries ascend in a: merge scan along the monotone endogenous grid
                                    if X <= Xe[0]:
                                        cc = X - a0
                                        vv = util(cc / sc, g) + beta * W[0]
                                    else:
                                        while ptr < NA - 2 and Xe[ptr + 1] <= X:
                                            ptr += 1
                                        w = (X - Xe[ptr]) / (Xe[ptr + 1] - Xe[ptr])
                                        cc = ce[ptr] + w * (ce[ptr + 1] - ce[ptr])
                                        if cc > X - a0:
                                            cc = X - a0
                                            vv = util(cc / sc, g) + beta * W[0]
                                        elif X > Xe[NA - 1]:
                                            cc, vv = extrap_top(X, Xe, ce, W, D, agrid, sc, beta, g, herm)
                                            if cc > X - a0:
                                                cc = X - a0
                                                vv = util(cc / sc, g) + beta * W[0]
                                        else:
                                            vv = util(cc / sc, g) + beta * wval(W, D, agrid, ptr, w, herm)
                                            if herm and (abs(ce[ptr + 1] - ce[ptr]) > POLISH_TOL * cc or
                                                         D[ptr + 1] > D[ptr]):
                                                cc, vv = polish(X, cc, vv, ptr, W, D, agrid, sc, beta, g)
                                else:
                                    cc, vv = env_query_k(X, Xe, ce, W, D, agrid, sc, beta, g, mono, split, herm,
                                                         jL)
                                if mono and jL >= 0 and agrid[jL] < X:      # corner at the SNAP asset limit
                                    ccr = X - agrid[jL]
                                    vcr = util(ccr / sc, g) + beta * W[jL]
                                    if vcr > vv:
                                        cc, vv = ccr, vcr
                                vals[nalt, a] = vv - dis
                                dvs[nalt, a] = Ra * mutil(cc / sc, g) / sc if xp >= xf else 0.0
                            nalt += 1
                    for a in range(NA):
                        m = NEG
                        for q in range(nalt):
                            if vals[q, a] > m:
                                m = vals[q, a]
                        se = 0.0
                        sd = 0.0
                        for q in range(nalt):
                            if vals[q, a] > NEG * 0.5:
                                e = np.exp((vals[q, a] - m) / sig)
                                se += e
                                sd += e * dvs[q, a]
                        VS[lw, hw, k, j, a] = m + sig * np.log(se) + sig * EULER
                        DS[lw, hw, k, j, a] = sd / se


# --------------------------------------------------------------------------------------------------------------------
# offer node (UI and acceptance, Bacher et al. 2025): accept vs keep entitlement
# --------------------------------------------------------------------------------------------------------------------
@njit(cache=True, parallel=True, fastmath=True)
def k_offer(GV, GD, nI, iE, iU, iN, ex, sig, store, Dlt):
    """Virtual wife slices nI + e (e = entitled state iU[e]): value of an offer at the end of the month,
    sigma ln(exp(v_acc / sigma) + exp(v_dec / sigma)) with v_acc = G[iE] (employed next month) and v_dec =
    (1 - ex) G[iU[e]] + ex G[iN] (keeps entitlement unless it expires); derivative = P(accept) G'_acc + (1 - P) G'_dec.
    Mean-zero extreme-value shocks: no Euler constant (getting an offer carries no taste-shock bonus).
    store: Dlt[e, j, hw, hh, k, nu, a] = (v_acc - v_dec) / sigma, the logit index the simulator uses."""
    NT, NJ, H, _, NK, NNU, NA = GV.shape
    ne = iU.shape[0]
    for b in prange(ne * NJ * H):
        e = b // (NJ * H)
        j = (b // H) % NJ
        hw = b % H
        u = iU[e]
        o = nI + e
        for hh in range(H):
            for k in range(NK):
                for nu in range(NNU):
                    for a in range(NA):
                        va = GV[iE, j, hw, hh, k, nu, a]
                        vd = (1.0 - ex) * GV[u, j, hw, hh, k, nu, a] + ex * GV[iN, j, hw, hh, k, nu, a]
                        dl = (va - vd) / sig
                        if dl > 0.0:
                            ee = np.exp(-dl)
                            p = 1.0 / (1.0 + ee)
                            V = va + sig * np.log1p(ee)
                        else:
                            ee = np.exp(dl)
                            p = ee / (1.0 + ee)
                            V = vd + sig * np.log1p(ee)
                        GV[o, j, hw, hh, k, nu, a] = V
                        GD[o, j, hw, hh, k, nu, a] = p * GD[iE, j, hw, hh, k, nu, a] + (1.0 - p) * (
                            (1.0 - ex) * GD[u, j, hw, hh, k, nu, a] + ex * GD[iN, j, hw, hh, k, nu, a])
                        if store:
                            Dlt[e, j, hw, hh, k, nu, a] = dl


@njit(cache=True, fastmath=True)
def k_offer_sep(GSV, GSD, nI, iE, iU, iN, ex, sig, store, DltS):
    """Separated wife's offer node (same rule; no husband)."""
    NT, H, NK, NJ, NA = GSV.shape
    ne = iU.shape[0]
    for e in range(ne):
        u = iU[e]
        o = nI + e
        for hw in range(H):
            for k in range(NK):
                for j in range(NJ):
                    for a in range(NA):
                        va = GSV[iE, hw, k, j, a]
                        vd = (1.0 - ex) * GSV[u, hw, k, j, a] + ex * GSV[iN, hw, k, j, a]
                        dl = (va - vd) / sig
                        if dl > 0.0:
                            ee = np.exp(-dl)
                            p = 1.0 / (1.0 + ee)
                            V = va + sig * np.log1p(ee)
                        else:
                            ee = np.exp(dl)
                            p = ee / (1.0 + ee)
                            V = vd + sig * np.log1p(ee)
                        GSV[o, hw, k, j, a] = V
                        GSD[o, hw, k, j, a] = p * GSD[iE, hw, k, j, a] + (1.0 - p) * (
                            (1.0 - ex) * GSD[u, hw, k, j, a] + ex * GSD[iN, hw, k, j, a])
                        if store:
                            DltS[e, hw, k, j, a] = dl


# --------------------------------------------------------------------------------------------------------------------
class Solution:
    """Stored policy inputs of one problem-era, float32, by month: C, W (married) and CS, WS (separated) at the
    endogenous points; Dlt, DltS the offer-node logit index (UI and acceptance)."""

    def __init__(self, m: Model, store: bool):
        T = m.cfg.T
        H, NA = m.H, m.NA
        shp = (T, m.ncfg, H, H, 3, 4, NA) if store else (1, 1, 1, 1, 1, 1, 1)
        self.C = np.zeros(shp, np.float32)
        self.W = np.zeros(shp, np.float32)
        shpS = (T, m.ncfgS, H, 3, 2, NA) if store else (1, 1, 1, 1, 1, 1)
        self.CS = np.zeros(shpS, np.float32)
        self.WS = np.zeros(shpS, np.float32)
        if store and m.ui_accept:
            self.Dlt = np.zeros((T, m.n_ent, len(m.hs_cat), H, H, 3, 4, NA), np.float32)
            self.DltS = np.zeros((T, m.n_ent, H, 3, 2, NA), np.float32)
        else:
            self.Dlt = np.zeros((1, 1, 1, 1, 1, 1, 1, 1), np.float32)
            self.DltS = np.zeros((1, 1, 1, 1, 1, 1), np.float32)
        self.V0 = None
        self.timing = {}

    def nbytes(self):
        return self.C.nbytes + self.W.nbytes + self.CS.nbytes + self.WS.nbytes + self.Dlt.nbytes + self.DltS.nbytes


def sep_table(m: Model):
    """Separation hazard by next month's (lw, lh) for the her-displacement extension (None when it is off): sigma_0 +
    sigma_J 1{lh != 0} + sigma_Jw 1{lw entitled}, capped at 1."""
    if not getattr(m, "her_sep", False):
        return None
    SG = np.empty((m.NLW, 3))
    for lw in range(m.NLW):
        for lh in range(3):
            v = m.sig_E if lh == 0 else m.sig_N
            if lw in tuple(int(u) for u in m.u_states):
                v += m.sig_Jw
            SG[lw, lh] = min(v, 1.0)
    return SG


def solve(m: Model, store: bool = True, t_stop: int = 0, keep_values=False) -> Solution:
    """Backward induction from month T-1 to t_stop. keep_values: also keep V_t, D_t of every month (tests only)."""
    cfg = m.cfg
    nb.set_num_threads(cfg.threads)
    T, H, NA, NLW = cfg.T, m.H, m.NA, m.NLW
    NK, NNU, NLH = 3, 4, 3
    herm = getattr(cfg, "w_interp", "hermite") == "hermite"
    sol = Solution(m, store)
    # terminal values
    VM1 = np.empty((NLW, NLH, H, H, NK, NNU, NA))
    DM1 = np.empty_like(VM1)
    VM1[:] = m.VT[None, None, :, :, None, None, :]
    DM1[:] = m.DT[None, None, :, :, None, None, :]
    VS1 = np.empty((NLW, H, NK, 2, NA))
    DS1 = np.empty_like(VS1)
    VS1[:] = m.VST[None, :, None, None, :]
    DS1[:] = m.DST[None, :, None, None, :]
    VM = np.empty_like(VM1)
    DM = np.empty_like(VM1)
    VS = np.empty_like(VS1)
    DS = np.empty_like(VS1)
    VSh = np.empty_like(VS1)
    DSh = np.empty_like(VS1)
    TV = np.empty_like(VM1)
    TD = np.empty_like(VM1)
    nI, nJ = len(m.ws_cat), len(m.hs_cat)
    nIt = nI + (m.n_ent if m.ui_accept else 0)         # real + virtual (offer-node) wife slices
    YV = np.empty((nJ, NLW, H, H, NK, NNU, NA))
    YD = np.empty_like(YV)
    GV = np.empty((nIt, nJ, H, H, NK, NNU, NA))
    GD = np.empty_like(GV)
    GSV = np.empty((nIt, H, NK, 2, NA))
    GSD = np.empty_like(GSV)
    dumC = np.zeros((1, 1, 1, 1, 1, 1), np.float32)
    dumCS = np.zeros((1, 1, 1, 1, 1), np.float32)
    dumD = np.zeros((1, 1, 1, 1, 1, 1, 1), np.float32)
    dumDS = np.zeros((1, 1, 1, 1, 1), np.float32)
    nchunks = 8 * cfg.threads
    tt = {"expect": 0.0, "egm": 0.0, "sep": 0.0}
    if keep_values:
        sol.VM_all, sol.DM_all, sol.VS_all = {}, {}, {}
    st_off = store and m.ui_accept
    sig_tab = sep_table(m)
    for t in range(T - 1, t_stop - 1, -1):
        g = age_group(t)
        jan = (t + 1) % 12 == 0
        P = m.Pk[g]
        t0 = time.perf_counter()
        # separated wife at t (uses V^S_{t+1})
        k_sep_expect(VS1, DS1, jan, P, m.Is, m.ws_cat, m.ws_lw, m.Aw_idx[g], m.Aw_p[g], m.Aw_n[g], GSV, GSD)
        if m.ui_accept:
            k_offer_sep(GSV, GSD, nI, m.off_iE, m.off_iU, m.off_iN, m.ui_exp, m.sigma_eps, st_off,
                        sol.DltS[t] if st_off else dumDS)
        k_egm_sep(GSV, GSD, m.stateS_cfg, m.stateS_n, m.outS_p, m.outS_ws, m.outS_n, m.incS0[g], m.snapBS[g],
                  m.disuS, m.scS[g], m.xfloorS[g], m.agrid, m.asset_limit, m.beta, m.gamma, m.rm, m.sigma_eps,
                  m.kappa_S, store, sol.CS[t] if store else dumCS, sol.WS[t] if store else dumCS, VS, DS, herm,
                  m.r_wedge, m.jL)
        t1 = time.perf_counter()
        # married at t (uses V^M_{t+1} and V^S_{t+1})
        k_half(VS1, DS1, m.half_j, m.half_w, VSh, DSh)
        if sig_tab is None:
            k_tilde(VM1, DM1, VSh, DSh, m.sig_E, m.sig_N, jan, m.pnu, TV, TD)
        else:
            k_tilde_w(VM1, DM1, VSh, DSh, sig_tab, jan, m.pnu, TV, TD)
        k_child(TV, TD, P)
        k_hc(TV, TD, m.Iw, m.Ih, m.p_c)
        k_husb(TV, TD, m.hs_cat, m.hs_lh, m.Ah_idx[g], m.Ah_p[g], m.Ah_n[g], YV, YD)     # age group g (g_age)
        k_wife(YV, YD, m.ws_cat, m.ws_lw, m.Aw_idx[g], m.Aw_p[g], m.Aw_n[g], GV, GD)
        if m.ui_accept:
            k_offer(GV, GD, nI, m.off_iE, m.off_iU, m.off_iN, m.ui_exp, m.sigma_eps, st_off,
                    sol.Dlt[t] if st_off else dumD)
        t2 = time.perf_counter()
        k_egm(GV, GD, m.state_cfg, m.state_n, m.out_p, m.out_ws, m.out_hs, m.out_n, m.inc0[g], m.snapB[g], m.disu,
              m.sc[g], m.xfloor[g], m.agrid, m.asset_limit, m.beta, m.gamma, m.rm, m.sigma_eps, m.kappa_S, store,
              sol.C[t] if store else dumC, sol.W[t] if store else dumC, VM, DM, nchunks, herm, m.r_wedge, m.jL)
        t3 = time.perf_counter()
        tt["sep"] += t1 - t0
        tt["expect"] += t2 - t1
        tt["egm"] += t3 - t2
        if keep_values:
            sol.VM_all[t] = VM.copy()
            sol.DM_all[t] = DM.copy()
            sol.VS_all[t] = VS.copy()
        VM1, VM = VM, VM1
        DM1, DM = DM, DM1
        VS1, VS = VS, VS1
        DS1, DS = DS, DS1
    sol.V0, sol.D0, sol.VS0 = VM1, DM1, VS1
    sol.timing = tt
    return sol


# --------------------------------------------------------------------------------------------------------------------
def node_derivs(ce, sc, beta, g):
    """Node derivatives of the continuation value recovered from the stored EGM consumption:
    u'(c / sc) / sc = beta D  =>  D = u'(c / sc) / (beta sc) (exact up to float32 rounding)."""
    return (ce / sc) ** (-g) / (beta * sc)


def alternatives(m: Model, sol: Solution, t: int, lw: int, lh: int, hw: int, hh: int, k: int, nu: int, a: float):
    """Value (before taste shocks) and consumption of every feasible alternative of a married state at assets a, from
    the stored solution (what the simulator does). Returns (list of (cfg, S, hours_w, hours_h, c, v), probabilities)."""
    g = age_group(t)
    sc, xf = m.sc[g, k], m.xfloor[g, k]
    herm = getattr(m.cfg, "w_interp", "hermite") == "hermite"
    out = []
    for ci in range(m.state_n[lw, lh]):
        c = m.state_cfg[lw, lh, ci]
        ce = sol.C[t, c, hw, hh, k, nu].astype(np.float64)
        W = sol.W[t, c, hw, hh, k, nu].astype(np.float64)
        Dn = node_derivs(ce, sc, m.beta, m.gamma)
        Xe = ce + m.agrid
        mono = bool(np.all(np.diff(Xe) > 0))
        for S in (0, 1):
            B = m.snapB[g, c, hw, hh, k, nu]
            if S == 1 and (B < 0 or a > m.asset_limit):
                continue
            xp = (1 + m.rm + (m.r_wedge if a < 0 else 0.0)) * a + m.inc0[g, c, hw, hh, k, nu] + (B if S else 0.0)
            X = max(xp, xf)
            cc, vv = env_query(X, Xe, ce, W, Dn, m.agrid, sc, m.beta, m.gamma, mono, herm, m.jL)
            out.append((c, S, int(m.cfg_hw[c]), int(m.cfg_hh[c]), cc, vv - m.disu[c, k] - (m.kappa_S if S else 0.0)))
    v = np.array([o[-1] for o in out])
    p = np.exp((v - v.max()) / m.sigma_eps)
    return out, p / p.sum()
