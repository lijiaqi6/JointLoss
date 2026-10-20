"""Simulator check: simulated monthly joint job-loss probabilities against the closed forms of the identification
plan (Section 1.4, forms (A)-(D)) at the analytic start values (pi_c(s), p_H, m_H, delta_j(r)).

Sample: married couple-months in which both spouses work (the CPS conditioning: both employed at t). For each race r
and match s (entry couples spread equally over s for precision; 6,000 synthetic couples x 4 copies):
  (C) P(h lost | s)            exact given the simulated type mix: sum_tau w_tau [pi_c + (1 - pi_c) m_tau delta_h]
  (A) P(w lost | h kept)       exact: sum_tau w'_tau m_tau delta_w   (w' = type mix among h-kept months)
  (B) P(w lost | h lost, s)    exact: sum_tau w''_tau [pi_c + (1 - pi_c) m^2 dw dh] / [pi_c + (1 - pi_c) m dh]
plus the plan's type-averaged approximations ((E m) delta_w etc.), and the lead/lag excess (D): her displacement in
month t + k (k = +-1..3, she works then) when he lost his job in t vs kept it, against
  L = (1 - pi_c) delta_w (m_H - 1) [P(H | h lost) - P(H | h kept)]  (exact given the simulated type posteriors)
and the plan's approximation delta_w Var m / E m. Pass: every |sim - exact| < 3 s.e. (binomial)."""
from _common import test_config, theta, entry, report
import numpy as np
from simulate import simulate


def main():
    cfg = test_config()
    th = theta()
    e = entry(6000, seed=5)
    e["s"] = np.arange(len(e)) % 3
    res = simulate(th, cfg, e, K=4)
    tau = res.info["tau"]
    ent = res.info["entry"]
    race = ent["race"].to_numpy()
    s_ = ent["s"].to_numpy()
    st, hw_, lh, hh_ = res.i("status"), res.i("hrs_w"), res.i("lh"), res.i("hrs_h")
    dW, dH = res.i("disp_w"), res.i("disp_h")
    both = (st == 1) & (hw_ > 0) & (lh == 0) & (hh_ > 0)
    TAU = np.broadcast_to(tau[:, None], st.shape)
    R_ = np.broadcast_to(race[:, None], st.shape)
    S_ = np.broadcast_to(s_[:, None], st.shape)
    m_t = np.array([1.0, th["m_H"]])
    ok_all, lines, zmax = True, [], 0.0
    for r, R in ((0, "B"), (1, "W")):
        dw, dh = th[f"delta_w_{R}"], th[f"delta_h_{R}"]
        for s in (0, 1, 2):
            pic = th[f"pi_c{s}"]
            sel = both & (R_ == r) & (S_ == s)
            n = sel.sum()
            wt = np.array([(sel & (TAU == k)).sum() / n for k in (0, 1)])
            # (C)
            pH = dH[sel].mean()
            exC = np.sum(wt * (pic + (1 - pic) * m_t * dh))
            seC = np.sqrt(exC * (1 - exC) / n)
            # (A)
            kept = sel & (dH == 0)
            wk = np.array([(kept & (TAU == k)).sum() / kept.sum() for k in (0, 1)])
            pA = dW[kept].mean()
            exA = np.sum(wk * m_t * dw)
            seA = np.sqrt(exA * (1 - exA) / kept.sum())
            # (B)
            lost = sel & (dH == 1)
            wl = np.array([(lost & (TAU == k)).sum() / max(lost.sum(), 1) for k in (0, 1)])
            pB = dW[lost].mean()
            exB = np.sum(wl * (pic + (1 - pic) * m_t ** 2 * dw * dh) / (pic + (1 - pic) * m_t * dh))
            seB = np.sqrt(exB * (1 - exB) / lost.sum())
            Em = 1 + th["p_H"] * (th["m_H"] - 1)
            kap = (1 - th["p_H"] + th["p_H"] * th["m_H"] ** 2) / Em ** 2
            Bq = Em * dh
            apB = (pic + (1 - pic) * kap * Em * dw * Bq) / (pic + (1 - pic) * Bq)
            for nm, sim, ex, se, ap in (("C P(h lost)", pH, exC, seC, pic + (1 - pic) * Em * dh),
                                        ("A P(w|h kept)", pA, exA, seA, Em * dw),
                                        ("B P(w|h lost)", pB, exB, seB, apB)):
                z = abs(sim - ex) / se
                zmax = max(zmax, z)
                ok_all &= z < 3
                lines.append(f"{R} s={s} {nm:14s} sim {sim:.5f}  exact {ex:.5f}  plan approx {ap:.5f}  (s.e. {se:.5f}, z {z:.1f})")
        # (D) leads and lags, pooled over s: base month t = husband works (married), lost vs kept his job; outcome
        # month t + k = the wife works (married) and is displaced. Exact excess: mean over the couple-months of the
        # outcome month's hazard pi_c(s) + (1 - pi_c(s)) m_tau delta_w(r), lost group minus kept group (it carries the
        # type posterior and the match-group composition).
        hwork = (st == 1) & (lh == 0) & (hh_ > 0) & (R_ == r)
        wwork = (st == 1) & (hw_ > 0)
        PIC = np.array([th[f"pi_c{q}"] for q in (0, 1, 2)])[S_]
        HAZ = PIC + (1 - PIC) * m_t[TAU] * dw
        for k in (-3, -2, -1, 1, 2, 3):
            if k > 0:
                base, out, dwk, dhb, hz = hwork[:, :-k], wwork[:, k:], dW[:, k:], dH[:, :-k], HAZ[:, k:]
            else:
                base, out, dwk, dhb, hz = hwork[:, -k:], wwork[:, :k], dW[:, :k], dH[:, -k:], HAZ[:, :k]
            g1 = base & out & (dhb == 1)
            g0 = base & out & (dhb == 0)
            p1, p0 = dwk[g1].mean(), dwk[g0].mean()
            L = p1 - p0
            se = np.sqrt(p1 * (1 - p1) / g1.sum() + p0 * (1 - p0) / g0.sum())
            exL = hz[g1].mean() - hz[g0].mean()
            Em = 1 + th["p_H"] * (th["m_H"] - 1)
            apL = dw * th["p_H"] * (1 - th["p_H"]) * (th["m_H"] - 1) ** 2 / Em
            z = abs(L - exL) / se
            zmax = max(zmax, z)
            ok_all &= z < 3
            lines.append(f"{R} lead/lag k={k:+d}  excess sim {L:.5f}  exact {exL:.5f}  plan approx {apL:.5f}  "
                         f"(s.e. {se:.5f}, z {z:.1f}; n lost {g1.sum():,})")
    for l in lines:
        print("   ", l)
    return report("7 simulated joint-loss probabilities vs closed forms", ok_all, f"max |z| = {zmax:.2f} over {len(lines)} moments")


if __name__ == "__main__":
    main()
