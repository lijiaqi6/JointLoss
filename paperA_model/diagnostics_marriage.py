"""Paper A model: the two marriage diagnostics of Fable's marriage note (fable_3h_plan_paperA.md, WP3 item 2).

(A) Does separation matter for the other blocks? One evaluation with separation switched off through the existing
    model.Model test overrides sig_E = sig_N = 0 (no separation in any state; nothing else changes), against the
    evaluation at --start, on common draws (same CRN seed; the noise floor of Q is about 30 units). Reports Q by block
    and the employment, wealth, search, exits and separation moments side by side.
(B) The simulated 'still with baseline wife' path by event year after his displacement: the stacked event panel that
    panels.py builds for the targets (units(), stack_rows(), the moments' sample window), the yearly coefficients
    e = -3, -1, 0, ..., 6 (reference e = -2) of bw_present on the event dummies with unit and cell effects
    (moments.twfe, IGE/60's estimator), by race and pooled, next to the PSID event study
    (IGE/output/father_displacement.csv, 'Still with baseline wife': e.g. -0.027 / -0.037 / -0.050 pooled and -0.037 /
    -0.053 / -0.074 Black in years 1 / 3 / 6). Only years 1-3 (their mean) are targets; years 4-6 are reported only.

Run (from the repository root):
  .venv/Scripts/python.exe IGE/paperA_model/diagnostics_marriage.py [--start <best.json | run dir>] [--threads 4]
Output: results/marriage_diag_<stamp>/marriage_diag.json, marriage_diag.md, es_still_with_wife.csv,
q_by_block.csv, moments_sep_off.csv (aggregate numbers only).
"""
from __future__ import annotations

import argparse
import time

import numpy as np
import pandas as pd

import post_common as PC

FD_CSV = PC.REPO / "IGE" / "output" / "father_displacement.csv"
SHOW_BLOCKS = ("Employment levels", "Wealth", "Her search", "His search", "Her exits", "Separation", "Added work",
               "Consumption")


def es_path(res, ctx, theta):
    """Yearly event-study coefficients of bw_present from the simulated stacked panel (the targets' sample)."""
    import moments as M
    import panels as PN
    E = ctx.E
    cfg = E._W["cfg"]
    R = PN.records(res, ctx.spec["ctrl_rate"], theta, cfg.merge_s12)
    U = PN.units(R, kids=True)
    P = PN.stack_rows(R, U)
    ev = (P["ev"] >= 1984) & (P["ev"] <= 2021) & (P["Y"] <= 2021)
    P = {k: v[ev] for k, v in P.items()}
    rows = []
    for lab, mk in (("All", np.ones(len(P["e"]), bool)), ("Black", P["race"] == 0), ("White", P["race"] == 1)):
        y = P["bw_present"][mk]
        ok = np.isfinite(y)
        idx = np.nonzero(mk)[0][ok]
        X, names = M._es_dummies(P["e"][idx], P["treat"][idx])
        keep = X.std(axis=0) > 0
        b = np.full(X.shape[1], np.nan)
        b[keep] = M.twfe(P["bw_present"][idx], X[:, keep], P["unit"][idx], P["cell"][idx])
        n_tr = int(len(np.unique(P["unit"][idx][P["treat"][idx] == 1])))
        for nm, v in zip(names, b):
            rows.append(dict(sample=lab, e=int(nm[1:]), model=float(v), n_rows=int(len(idx)), treated_units=n_tr))
    return pd.DataFrame(rows)


def psid_path():
    D = pd.read_csv(FD_CSV)
    D = D[(D["table"] == "family_event_study") & (D["design"] == "main") & (D["subsample"].isna())
          & (D["outcome"] == "bw_present")]
    out = []
    for _, r in D.iterrows():
        t = str(r["term"])
        if t.startswith("e="):
            out.append(dict(sample=r["sample"], e=int(t[2:]), psid=float(r["coef"]), psid_se=float(r["se"])))
    return pd.DataFrame(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--start", default=None, help="best.json or run folder (default: the analytic start)")
    ap.add_argument("--size", default=None)
    ap.add_argument("--K", type=int, default=3)
    ap.add_argument("--threads", type=int, default=2)
    a = ap.parse_args()
    t0 = time.time()
    ctx = PC.setup(a.start, size=a.size, K=a.K, threads=a.threads)
    out = PC.out_dir("marriage_diag")
    print(f"marriage diagnostics at {a.start or 'the analytic start'} -> {out}", flush=True)
    base = PC.evaluate(ctx, keep_res=True)
    print(f"baseline Q {base['Q']:,.1f} ({base['seconds']:.0f}s)", flush=True)
    es = es_path(base.pop("res"), ctx, base["theta"])
    off = PC.evaluate(ctx, overrides={"sig_E": 0.0, "sig_N": 0.0})
    print(f"separation off Q {off['Q']:,.1f} ({off['seconds']:.0f}s)", flush=True)

    # (A) Q by block and moments
    bt = pd.DataFrame({"block": base["blocks"].index, "Q_start": base["blocks"]["sum"].to_numpy(),
                       "Q_sep_off": off["blocks"]["sum"].to_numpy(),
                       "in_objective": base["blocks"]["in_objective"].to_numpy()})
    bt["change"] = bt["Q_sep_off"] - bt["Q_start"]
    bt.to_csv(out / "q_by_block.csv", index=False)
    mf = PC.moments_frame(ctx, base["m"]).rename(columns={"sim": "model_start", "z": "z_start", "q": "q_start"})
    mf["model_sep_off"] = off["m"]
    mf["z_sep_off"] = (off["m"] - mf["value"]) / mf["se"]
    mf["q_sep_off"] = np.where(mf["in_objective"] == 1, (off["m"] - mf["value"]) ** 2 * np.diag(ctx.W), 0.0)
    mf.to_csv(out / "moments_sep_off.csv", index=False)

    # (B) still with baseline wife
    ps = psid_path()
    es = es.merge(ps, on=["sample", "e"], how="left")
    es["target_years"] = np.where(es["e"].between(1, 3), "1-3 (mean targeted)", np.where(es["e"] >= 4, "reported",
                                                                                          "pre / event year"))
    es.to_csv(out / "es_still_with_wife.csv", index=False)

    def mean_of(df, lo, hi, col):
        s = df[df["e"].between(lo, hi)][col]
        return float(s.mean()) if len(s) else float("nan")

    summ = {}
    for smp, g in es.groupby("sample"):
        summ[smp] = {f"{c}_{lo}_{hi}": mean_of(g, lo, hi, c) for c in ("model", "psid") for lo, hi in ((1, 3), (4, 6))}
        summ[smp].update({f"model_e{e}": float(g[g["e"] == e]["model"].iloc[0]) for e in (1, 3, 6)})
        summ[smp].update({f"psid_e{e}": float(g[g["e"] == e]["psid"].iloc[0]) for e in (1, 3, 6)})
    info = dict(start=a.start or "analytic start (inputs/start_analytic.json + start_overrides.json)",
                size=ctx.args.size, K=ctx.args.K, seed=ctx.args.seed, ext=ctx.args.ext, notes=ctx.notes,
                Q_start=base["Q"], Q_sep_off=off["Q"], Q_change=off["Q"] - base["Q"], noise_floor_Q=30.0,
                sigma0=dict(B=PC.theta_dict(ctx)["sigma0_B"], W=PC.theta_dict(ctx)["sigma0_W"]),
                sigmaJ=dict(B=PC.theta_dict(ctx)["sigmaJ_B"], W=PC.theta_dict(ctx)["sigmaJ_W"]),
                still_with_wife=summ, minutes=(time.time() - t0) / 60)
    PC.write_json(out / "marriage_diag.json", info)

    md = [f"# Marriage diagnostics: {info['start']}", "",
          f"Size {ctx.args.size}, K = {ctx.args.K}, CRN seed {ctx.args.seed}, extensions {ctx.args.ext}. "
          f"Both evaluations on common draws. {' '.join(ctx.notes)}", "",
          "## (A) Separation switched off (sig_E = sig_N = 0) against the start", "",
          f"Q: {base['Q']:,.1f} at the start, {off['Q']:,.1f} with separation off (change {off['Q'] - base['Q']:+,.1f}; "
          f"noise floor about 30).", "", "| Block | Q start | Q separation off | change |", "|---|---:|---:|---:|"]
    for r in bt.itertuples():
        md.append(f"| {r.block} | {r.Q_start:,.1f} | {r.Q_sep_off:,.1f} | {r.change:+,.1f} |")
    md += ["", "| Moment | block | data | model (start) | model (separation off) | z start | z off |",
           "|---|---|---:|---:|---:|---:|---:|"]
    for r in mf[mf["block"].isin(SHOW_BLOCKS)].itertuples():
        md.append(f"| {r.id}{'' if r.in_objective else ' (reported)'} | {r.block} | {r.value:.4g} | {r.model_start:.4g} | "
                  f"{r.model_sep_off:.4g} | {r.z_start:+.2f} | {r.z_sep_off:+.2f} |")
    md += ["", "## (B) Still with baseline wife after his displacement (event study, reference e = -2)", "",
           "Model: the targets' stacked panel (panels.units / stack_rows, events 1984-2021, outcome years to 2021), "
           "yearly coefficients with unit and cell effects. PSID: IGE/output/father_displacement.csv (IGE/19). "
           "Years 1-3: their mean is the target (psid_es_bw_present_13_B/W, IGE/60's window); years 4-6 reported only.",
           "", "| e | Pooled model | Pooled PSID | Black model | Black PSID | White model | White PSID |",
           "|---:|---:|---:|---:|---:|---:|---:|"]
    piv = es.pivot_table(index="e", columns="sample", values=["model", "psid"])
    for e in piv.index:
        cells = []
        for smp in ("All", "Black", "White"):
            mv = piv[("model", smp)].get(e, np.nan) if ("model", smp) in piv else np.nan
            pv = piv[("psid", smp)].get(e, np.nan) if ("psid", smp) in piv else np.nan
            cells += [f"{mv:+.3f}", f"{pv:+.3f}" if np.isfinite(pv) else ""]
        md.append(f"| {e:+d} | " + " | ".join(cells) + " |")
    md += ["", "Means: " + "; ".join(
        f"{k}: model 1-3 {v['model_1_3']:+.3f}, 4-6 {v['model_4_6']:+.3f}"
        + (f" vs PSID 1-3 {v['psid_1_3']:+.3f}, 4-6 {v['psid_4_6']:+.3f}" if np.isfinite(v["psid_1_3"]) else "")
        for k, v in summ.items()),
           "", "'All' = pooled over races in both. In the model the separation hazard is sigma_0 + sigma_J only in "
           "months in which the husband is non-employed (sigma_0 otherwise).",
           "", f"{info['minutes']:.1f} minutes."]
    (out / "marriage_diag.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    print(f"-> {out}")


if __name__ == "__main__":
    main()
