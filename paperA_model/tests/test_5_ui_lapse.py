"""Check (5): the wife's exits from non-employment rise when her UI entitlement lapses.

Rule (lead decision 2026-10-18, Bacher, Grubener and Nord 2025): an entitled non-employed wife who receives an offer
may decline it and keep her entitlement (which lapses only with the monthly hazard 1/6); accepting ends it. Before this
rule the check failed by construction (an offer always moved her to employment).

Simulated displaced married wives (delta_w raised to 0.01 for precision; 2,000 synthetic couples), months d = 1..6
after her displacement while she is still non-employed and married. Entitlement is assigned by CRN draws independent
of the state (take-up q_UI at displacement, expiry 1/6 each month), so comparisons at equal d are like-for-like:
  (a) exit to work next month, entitled vs not entitled, pooled over d = 1..6 (duration-matched by reweighting the
      not-entitled months to the entitled months' distribution of d);
  (b) at the lapse: wives entitled in month d - 1 whose entitlement expired at the end of d - 1 (no offer accepted)
      vs wives still entitled in month d: exit to work at the end of month d;
  (c) a CRN counterfactual with q_UI = 0 (no entitlement at all): exits in months 1..6 after displacement rise
      (mean over d of the monthly exit rate, same couples and draws).
Run at the analytic start values (where a wife with a job works in ~93% of months, so offers are almost always
accepted) and at the interior point of check (3) (work costs + 0.537). Pass at the interior point: (a), (b), (c)
all positive."""
from _common import test_config, theta, entry, report
import numpy as np
from simulate import simulate


def spells(res):
    st, lw, hrs, dsp = res.i("status"), res.i("lw"), res.i("hrs_w"), res.i("disp_w")
    acc = res.i("acc")
    works = (lw == 0) & (hrs > 0)
    n, nm = st.shape
    rows = []                                            # (d, entitled, just_lapsed, exit next month, declined)
    ii, mm = np.nonzero((dsp == 1) & (st == 1))
    for i, m in zip(ii, mm):
        prev_ent = None
        for d in range(1, 7):
            t = m + d
            if t + 1 >= nm or st[i, t] != 1 or st[i, t + 1] != 1 or works[i, t]:
                break
            ent = lw[i, t] in (1, 2)
            lapsed = (prev_ent is True) and not ent
            rows.append((d, ent, lapsed, bool(works[i, t + 1]), acc[i, t]))
            prev_ent = ent
    return np.array(rows, dtype=float).reshape(-1, 5)


def stats(R):
    d, ent, lap, ex, dec = R.T
    e1 = ex[ent == 1].mean()
    # not-entitled months reweighted to the entitled months' duration distribution
    w = np.zeros(len(d))
    for k in range(1, 7):
        nk1 = ((ent == 1) & (d == k)).sum()
        nk0 = ((ent == 0) & (d == k)).sum()
        if nk0 > 0:
            w[(ent == 0) & (d == k)] = nk1 / nk0
    e0 = (ex * w).sum() / w.sum()
    still = (ent == 1) & (d >= 2)
    lap_ = lap == 1
    byd = np.mean([ex[d == k].mean() for k in range(1, 7) if (d == k).any()])   # equal weight per month since loss
    return dict(exit_byd=byd, exit_ent=e1, exit_noent=e0, n_ent=int((ent == 1).sum()), n_noent=int((ent == 0).sum()),
                exit_lapsed=ex[lap_].mean() if lap_.any() else np.nan, exit_still=ex[still].mean(),
                n_lapsed=int(lap_.sum()), decline_share=((dec == 0) & (ent == 1)).sum() / max(((dec >= 0) & (ent == 1)).sum(), 1))


def main():
    cfg = test_config()
    e = entry(2000)
    lines, ok_int = [], False
    for nm, shift in (("start values", 0.0), ("interior (+0.537)", 0.537)):
        # no couple type (m_H = 1): the check is about UI entitlement; with delta_w = 0.01 the start's type (p_H 0.02,
        # m_H 15.95 since 2026-10-18) would give 16% monthly hazards to a few wives and dominate the small lapse groups
        base = theta(delta_w_W=0.01, delta_w_B=0.01, m_H=1.0)
        base["phi_F"] += shift
        base["phi_P"] += shift
        s1 = stats(spells(simulate(base, cfg, e, K=1)))
        s0 = stats(spells(simulate(base, cfg, e, K=1, overrides={"qui": 0.0})))
        da = s1["exit_noent"] - s1["exit_ent"]
        db = s1["exit_lapsed"] - s1["exit_still"]
        dc = s0["exit_byd"] - s1["exit_byd"]
        lines.append(f"{nm}: (a) exit entitled {s1['exit_ent']:.3f} (n={s1['n_ent']:,}) vs not {s1['exit_noent']:.3f} "
                     f"(n={s1['n_noent']:,}): {da:+.3f}; (b) just lapsed {s1['exit_lapsed']:.3f} (n={s1['n_lapsed']:,}) "
                     f"vs still entitled {s1['exit_still']:.3f}: {db:+.3f}; (c) exit months 1-6, q_UI = 0 {s0['exit_byd']:.3f} vs "
                     f"baseline {s1['exit_byd']:.3f}: {dc:+.3f}; offers declined by entitled wives {s1['decline_share']:.3f}")
        if shift > 0:
            ok_int = da > 0 and db > 0 and dc > 0
    for l in lines:
        print("   ", l)
    return report("5 exits rise when UI lapses", ok_int, " | ".join(lines))


if __name__ == "__main__":
    main()
