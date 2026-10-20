"""Paper A model: counterfactual scenarios with the paper's scoring (sec7_model.tex, 'Counterfactuals'; plan WP3 item 3).

Each scenario re-solves and re-simulates the model on the same draws (CRN seed of the run) at --start (main model)
and, with --indep <best.json>, at the independent-shock estimate (pi_c = 0, m_H = 1). Implemented now (theta or
existing Model-override changes only; nothing on the estimation code path is touched):
  base             the estimate itself
  i_common_off     (i) pi_c0 = pi_c1 = pi_c2 = 0 and m_H = 1 (no common shock, no couple type)
  ii_ui12          (ii) UI expiry hazard 1/6 -> 1/12 (52 weeks) for both spouses: Model override ui_exp (the solver's
                   outcome tables and the simulator both read Model.ui_exp)
  ii_ui12_pic2     (ii) the same with pi_c doubled (the recession excess)
  v_haz            (v) Black couples with the White displacement hazards (delta_w_B = delta_w_W, delta_h_B = delta_h_W;
                   the common shock and the couple type are not race-specific)
  v_sep            (v) Black couples with the White separation response (sigmaJ_B = sigmaJ_W), alone
  v_haz_sep        (v) both
Not implemented (need code hooks, to be added behind flags after the CMA-ES jobs have started; see the spec at the
end of this docstring): (ii) 'both spouses entitled at a joint loss', (iii) EITC expansion vs an equal-cost transfer,
(iv) childcare subsidy, and the full-value welfare and children's outcomes.

Scoring (by race and workplace match, and overall; aggregate numbers only):
  * consumption around the husband's displacement (married at t and t+1; displaced at the end of month t): mean
    household consumption in the 6 months t-5..t (pre), in the loss month t+1 (the first month without his job), and
    over t+1..t+12 (married months); mean log change loss / pre and 12-month / pre; all his losses and joint losses
    (her displacement in the same month);
  * shares of married couple-months with no earner (neither spouse works) and with no earner and no credit (beginning-
    of-month assets within 1% of a_bar of the borrowing limit -a_bar);
  * consumption-equivalent welfare at entry, CONSUMPTION ONLY: lambda with sum_i sum_t beta^t u((1 + lambda) c_it) =
    the scenario's sum, u CRRA (gamma), over each couple-copy's simulated months (married or separated wife) from entry
    to the end of the simulation window; work costs, stigma and taste shocks are not in it (the full-value measure
    needs the hook below).

Run (from the repository root; counterfactuals are meant for the full size, the smoke test uses the default size):
  .venv/Scripts/python.exe paperA_model/counterfactuals.py --start <best.json | run dir> [--indep <best.json>]
        [--size full] [--scenarios base i_common_off ...] [--threads 4]
Output: results/counterfactuals_<stamp>/scores.csv (long: model, scenario, group, measure, value),
counterfactuals.json, counterfactuals.md (main table: scenario x measure, overall and by race).

HOOK SPEC for the scenarios not yet implemented (each a new entry of Model overrides or Config, default off, so that
the estimation path is unchanged):
  (ii-b) Both spouses entitled at a joint loss. Entitlement is drawn at displacement with take-up q_UI = Model.qui for
         each spouse independently: model.py wife_events / husb_events return [(q, entitled slice), (1 - q, not
         entitled)] for a displaced spouse, combined in the configuration loop over (ew, eh); simulate.sim_kernel draws
         slots 26-27 against qui. Hook: override 'joint_entitled' -> in the (ew, eh) = (1, 1) branch of the
         configuration loop use q = 1 for both spouses' displaced lists, and in sim_kernel use u < 1 (entitled) for
         both spouses when both are displaced in the same month (the kernel needs the flag as one more argument).
  (iii)  EITC expansion vs an equal-cost transfer. Budget: Model.inc0 / incS0 (income net of taxes + EITC, by
         configuration) are built from eitc_month(...) with the schedule dict sch['eitc_annual']; hook 1: override
         'eitc_scale' multiplying the EITC credit (eitc_month's result) in the married and separated budgets; hook 2:
         override 'transfer' (thousand 2000 $ a month) added to inc0 / incS0 for couples / mothers with k > 0. The
         equal-cost transfer is found by a 1-D search on 'transfer' so that simulated outlays equal the EITC
         expansion's (sum of res.F 'eitc' differences, discounted).
  (iv)   Childcare subsidy when the youngest child is under six. The childcare price per hour by child bucket, pcc[k],
         times her hours (ccc) is subtracted from inc0 / incS0 and deducted in the SNAP benefit (model.py budget
         loops); hook: override 'cc_mult' (default 1) multiplying pcc[1] (youngest 0-5) in both loops; outlays =
         (1 - cc_mult) pcc[1] x simulated hours of mothers with k = 1.
  Full-value welfare at entry: solution_hook in simulate() gives (problem, Model, Solution) per era; store sol.W at
         t = t0 of each entry couple's state and evaluate the expected value at entry assets (env_query with the
         stored C, W), then lambda from V(c (1 + lambda)) by bisection on a re-simulated consumption path.
  Children's adult outcomes: map the simulated parental income / joint-loss exposure by child age into the high and
         low slopes of Section 6 (a post-processing step on res, no model hook).
"""
from __future__ import annotations

import argparse
import time

import numpy as np
import pandas as pd

import post_common as PC

SCENARIOS = ["base", "i_common_off", "ii_ui12", "ii_ui12_pic2", "v_haz", "v_sep", "v_haz_sep"]
NOT_IMPLEMENTED = {"ii_both_entitled": "hook (ii-b)", "iii_eitc_vs_transfer": "hook (iii)",
                   "iv_childcare": "hook (iv)"}


def scenario(name, th: dict):
    """-> (theta dict, Model overrides or None)."""
    t = dict(th)
    ov = None
    if name == "base":
        pass
    elif name == "i_common_off":
        t.update(pi_c0=0.0, pi_c1=0.0, pi_c2=0.0, m_H=1.0)
    elif name == "ii_ui12":
        ov = {"ui_exp": 1.0 / 12.0}
    elif name == "ii_ui12_pic2":
        ov = {"ui_exp": 1.0 / 12.0}
        t.update(pi_c0=2 * th["pi_c0"], pi_c1=2 * th["pi_c1"], pi_c2=2 * th["pi_c2"])
    elif name in ("v_haz", "v_haz_sep"):
        t.update(delta_w_B=th["delta_w_W"], delta_h_B=th["delta_h_W"])
        if name == "v_haz_sep":
            t.update(sigmaJ_B=th["sigmaJ_W"])
    elif name == "v_sep":
        t.update(sigmaJ_B=th["sigmaJ_W"])
    elif name in NOT_IMPLEMENTED:
        raise SystemExit(f"scenario {name} needs {NOT_IMPLEMENTED[name]} (see the docstring): not implemented yet")
    else:
        raise SystemExit(f"unknown scenario {name}")
    return t, ov


def score(res, th, fx, merge_s12):
    """Aggregate scores by group (all, race B/W, match s0/s1(+), race x match)."""
    from simulate import FIELDS_F, FIELDS_I
    I = lambda nm: res.I[FIELDS_I.index(nm)]                         # noqa: E731
    F = lambda nm: res.F[FIELDS_F.index(nm)]                         # noqa: E731
    ent = res.info["entry"]
    race = ent["race"].to_numpy()
    s = ent["s"].to_numpy()
    if merge_s12:
        s = np.minimum(s, 1)
    st = I("status")
    mar = st == 1
    c = F("c").astype(float)
    a = F("a").astype(float)
    ww = mar & (I("lw") == 0) & (I("hrs_w") > 0)
    wh = mar & (I("lh") == 0) & (I("hrs_h") > 0)
    noearn = mar & ~ww & ~wh
    nocred = noearn & (a <= -th["a_bar"] + 0.01 * max(th["a_bar"], 1e-6))
    n, nm = st.shape
    # displacement events
    dh = (I("disp_h") == 1) & mar
    dwj = I("disp_w") == 1
    ii, tt = np.nonzero(dh)
    ok = (tt >= 5) & (tt + 12 < nm)
    ii, tt = ii[ok], tt[ok]
    ok = mar[ii, tt + 1] & np.all(np.stack([mar[ii, tt - k] for k in range(6)]), axis=0)
    ii, tt = ii[ok], tt[ok]
    pre = np.mean(np.stack([c[ii, tt - k] for k in range(6)]), axis=0)
    loss = c[ii, tt + 1]
    post = np.stack([np.where(mar[ii, tt + k], c[ii, tt + k], np.nan) for k in range(1, 13)])
    c12 = np.nanmean(post, axis=0)
    joint = dwj[ii, tt]
    # welfare (consumption only)
    beta, gam = fx["beta"], fx["gamma"]
    inn = st >= 0
    first = np.where(inn.any(axis=1), np.argmax(inn, axis=1), 0)
    k = np.arange(nm)[None, :] - first[:, None]
    disc = np.where(inn & (k >= 0), beta ** np.maximum(k, 0), 0.0)
    u = np.where(inn, np.maximum(c, 1e-6) ** (1 - gam) / (1 - gam), 0.0)
    U = (disc * u).sum(axis=1)

    groups = {"all": np.ones(n, bool), "B": race == 0, "W": race == 1}
    for sv in sorted(np.unique(s)):
        lab = f"s{sv}" + ("+" if merge_s12 and sv == 1 else "")
        groups[lab] = s == sv
        for r, rl in ((0, "B"), (1, "W")):
            groups[f"{rl}_{lab}"] = (s == sv) & (race == r)
    rows = []
    for g, gm in groups.items():
        ev = gm[ii]
        ej = ev & joint
        mm = mar[gm]
        rec = {"couple_months_married": int(mm.sum()),
               "share_no_earner": float(noearn[gm].sum() / max(mm.sum(), 1)),
               "share_no_earner_no_credit": float(nocred[gm].sum() / max(mm.sum(), 1)),
               "U_cons": float(U[gm].sum()), "n_couples": int(gm.sum()),
               "his_losses": int(ev.sum()), "joint_losses": int(ej.sum())}
        for lab, e_ in (("his", ev), ("joint", ej)):
            if e_.sum() > 0:
                rec[f"c_pre_{lab}"] = float(pre[e_].mean())
                rec[f"c_loss_{lab}"] = float(loss[e_].mean())
                rec[f"c_12m_{lab}"] = float(np.nanmean(c12[e_]))
                rec[f"dlog_c_loss_{lab}"] = float(np.mean(np.log(np.maximum(loss[e_], 1e-6) / pre[e_])))
                rec[f"dlog_c_12m_{lab}"] = float(np.nanmean(np.log(np.maximum(c12[e_], 1e-6) / pre[e_])))
        rows.append((g, rec))
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--start", default=None, help="main model: best.json or run folder (default: the analytic start)")
    ap.add_argument("--indep", default=None, help="independent-shock model: best.json or run folder")
    ap.add_argument("--size", default="full", help="params.SIZES key (default full; the estimation default for smoke tests)")
    ap.add_argument("--K", type=int, default=3)
    ap.add_argument("--threads", type=int, default=2)
    ap.add_argument("--scenarios", nargs="*", default=SCENARIOS)
    a = ap.parse_args()
    t0 = time.time()
    out = PC.out_dir("counterfactuals")
    models = [("main", a.start)] + ([("indep", a.indep)] if a.indep else [])
    long, info = [], dict(size=a.size, K=a.K, scenarios=a.scenarios, models={}, minutes={})
    for mlab, start in models:
        ctx = PC.setup(start, size=a.size, K=a.K, threads=a.threads)
        cfg = ctx.E._W["cfg"]
        th0 = PC.theta_dict(ctx)
        info["models"][mlab] = dict(start=start or "analytic start", ext=ctx.args.ext, seed=ctx.args.seed,
                                    notes=ctx.notes, theta=th0)
        base_U = {}
        for sc in a.scenarios:
            ts = time.time()
            t, ov = scenario(sc, th0)
            res, thd, fx = PC.simulate_only(ctx, ctx.E.dict_vec(t), overrides=ov)
            rows = score(res, thd, fx, cfg.merge_s12)
            del res
            for g, rec in rows:
                if sc == "base":
                    base_U[g] = rec["U_cons"]
                if g in base_U:
                    rec["ce_cons_pct"] = 100 * ((rec["U_cons"] / base_U[g]) ** (1 / (1 - fx["gamma"])) - 1)
                for k, v in rec.items():
                    long.append(dict(model=mlab, scenario=sc, group=g, measure=k, value=v))
            info["minutes"][f"{mlab}/{sc}"] = (time.time() - ts) / 60
            print(f"{mlab} {sc}: {(time.time() - ts) / 60:.1f} min", flush=True)
            pd.DataFrame(long).to_csv(out / "scores.csv", index=False)
    L = pd.DataFrame(long)
    L.to_csv(out / "scores.csv", index=False)
    info["total_minutes"] = (time.time() - t0) / 60
    PC.write_json(out / "counterfactuals.json", info)
    show = ["dlog_c_loss_his", "dlog_c_12m_his", "dlog_c_loss_joint", "dlog_c_12m_joint", "share_no_earner",
            "share_no_earner_no_credit", "ce_cons_pct", "his_losses", "joint_losses"]
    md = [f"# Counterfactuals ({a.size}, K = {a.K})", "",
          "Consumption: household consumption, mean log change from the 6 months before his displacement to the loss "
          "month and to the mean of the 12 months after (married couples). Shares: of married couple-months. "
          "ce_cons_pct: consumption-only consumption-equivalent at entry relative to base, percent (not the full-value "
          "welfare measure). Same CRN draws in every scenario.", ""]
    for mlab, _ in models:
        for g in ("all", "B", "W"):
            sub = L[(L["model"] == mlab) & (L["group"] == g) & (L["measure"].isin(show))]
            if sub.empty:
                continue
            piv = sub.pivot_table(index="scenario", columns="measure", values="value").reindex(
                [s for s in a.scenarios if s in set(sub["scenario"])])
            cols = [c for c in show if c in piv.columns]
            md += [f"## {mlab} model, group {g}", "", "| scenario | " + " | ".join(cols) + " |",
                   "|---|" + "---:|" * len(cols)]
            for sc, r in piv.iterrows():
                md.append(f"| {sc} | " + " | ".join(f"{r[c]:.4g}" for c in cols) + " |")
            md.append("")
    md.append(f"{info['total_minutes']:.1f} minutes. Not implemented (hooks in the docstring): "
              + ", ".join(f"{k} ({v})" for k, v in NOT_IMPLEMENTED.items()) + ".")
    (out / "counterfactuals.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    print(f"-> {out}")


if __name__ == "__main__":
    main()
