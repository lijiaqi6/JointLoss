"""WP10 (b) of IGE/proposals/fable_10h_plan_paperA.md (2026-10-20): separated wives' employment in the model, from one
stored simulation at --start (default: the analytic start), built as 'estimate.py evaluate --start' builds it
(post_common.setup / simulate_only). The model has no child support and no remarriage, so the simulated rate is the
child-support-free, never-remarried benchmark that WP3's PSID rate is compared with.

Records (simulate.py): status 1 married / 0 separated (the wife continues alone) / -1 outside the sample; lw = 0
employed; hrs_w > 0 positive hours; k = youngest child (0 none, 1 aged 0-5, 2 aged 6-17). Employment = lw == 0 and
hrs_w > 0 (as bps_check.monthly_panel). Wife's age 25 + (t from entry) / 12. Calendar years 1984-2008 (the simulation
window; the PSID comparison window is set by WP3).
Output: results/sep_state_<stamp>/sep_state.json and sep_state.csv (aggregates only).
Run: .venv/Scripts/python.exe IGE/paperA_model/sep_state_sim.py [--start <best.json>] [--K 3] [--threads 14]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--start", default=None)
    ap.add_argument("--K", type=int, default=3)
    ap.add_argument("--threads", type=int, default=14)
    a = ap.parse_args()
    import post_common as pc
    from simulate import FIELDS_I
    ctx = pc.setup(a.start, K=a.K, threads=a.threads)
    res, th, fx = pc.simulate_only(ctx)
    gi = lambda nm: res.I[FIELDS_I.index(nm)]                         # noqa: E731
    st = gi("status").astype(int)
    n, T = st.shape
    emp = (gi("lw") == 0) & (gi("hrs_w") > 0)
    ft = emp & (gi("hrs_w") == 2)
    k = gi("k").astype(int)
    m_off = np.asarray(res.info["m_off"])
    age = 25 + (np.arange(T)[None, :] - m_off[:, None]) / 12.0
    race = res.info["entry"]["race"].to_numpy()                      # 1 White (bps_check: race == 1 -> White)
    sep = st == 0
    first = np.where(sep.any(1), sep.argmax(1), T)
    since = np.arange(T)[None, :] - first[:, None]
    ok_age = (age >= 25) & (age < 60)
    rows = []

    def add(group, mask, state):
        sel = mask & ok_age & state
        nn = int(sel.sum())
        rows.append(dict(group=group, state="separated" if state is sep else "married", n_months=nn,
                         n_women=int(sel.any(1).sum()), emp=float(emp[sel].mean()) if nn else np.nan,
                         ft_share_of_emp=float(ft[sel].sum() / max(emp[sel].sum(), 1)) if nn else np.nan))

    mar = st == 1
    allm = np.ones_like(sep)
    for state in (sep, mar):
        add("all", allm, state)
        for kk, nm in ((0, "no child"), (1, "youngest 0-5"), (2, "youngest 6-17")):
            add(nm, k == kk, state)
        for rr, nm in ((1, "White"), (0, "Black")):
            add(nm, np.repeat((race == rr)[:, None], T, 1), state)
    for lo, hi, nm in ((0, 12, "months 0-11 since separation"), (12, 36, "months 12-35"), (36, 10 ** 6, "months 36+")):
        add(nm, (since >= lo) & (since < hi), sep)
    # employment in the 12 months before separation (married) for the women who separate: the change at separation
    pre = (since >= -12) & (since < 0)
    add("12 months before separation (women who separate)", pre, mar)
    out = pc.out_dir("sep_state")
    tab = pd.DataFrame(rows)
    tab.to_csv(out / "sep_state.csv", index=False)
    rep = dict(start=a.start or "analytic start", K=a.K, size=ctx.spec["size"], seed=ctx.spec["seed"],
               couples=int(n), ever_separated_share=float(sep.any(1).mean()), table=rows,
               note="model: no child support, no remarriage; employment = lw == 0 and hrs_w > 0; wife 25-59")
    (out / "sep_state.json").write_text(json.dumps(rep, indent=1, default=float))
    pd.set_option("display.width", 200)
    print(tab.to_string(index=False))
    print(f"-> {out}")


if __name__ == "__main__":
    main()
