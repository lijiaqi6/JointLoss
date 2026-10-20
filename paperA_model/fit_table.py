"""Paper A model: LaTeX fit, objective and parameter tables in the paper's layout (plan WP3 item 1).

Inputs (each SOURCE is an 'estimate.py evaluate' folder or its moments.csv, or a run folder / its best.json from
'polish' or 'run', e.g. results/hpc_runs/<run>/; for a run the moments come from best.json and the objective's
exclusions and weights from run.json):
  fit_table.py [SOURCE] [--indep SOURCE] [--params RUN_DIR_OR_BEST_JSON [SE_CSV]] [--indep-params ...] [--compile]
SOURCE defaults to the latest results/evaluate_* folder that holds moments.csv (the analytic start).
Writes to results/fit_table_<stamp>/ (or --out):
  tab_model_fit.tex       moments as rows, blocks as row panels (\\multicolumn headers), columns: data, (s.e.), main
                          model, z = (model - data) / s.e., and with --indep the independent-shock model and its z;
                          moments outside the objective (in_objective = 0) carry the mark $^{r}$ ('reported, not
                          targeted'); longtable (needs \\usepackage{longtable})
  tab_q_by_block.tex      Q by block (sum of weighted squared deviations), moments in the objective, share of Q; main
                          and independent-shock model
  tab_params_estimates.tex (only with --params) the rows and order of tab:model_params: start, estimate, s.e., bounds
                          (and the independent-shock estimate and s.e. with --indep-params); s.e. from se.csv (the
                          sandwich); parameters not free in the run are marked 'fixed'
  fit_table.json          the numbers behind the tables; test_wrapper.tex (a scratch document that \\input's the three
                          tables; --compile runs pdflatex on it in the output folder)
--paper copies the .tex tables into IGE/paperA_joint_loss/ (off by default: the paper's tables change only when the
lead decides).
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

import post_common as PC

PAPER = PC.REPO / "IGE" / "paperA_joint_loss"

# rows and order of tab:model_params (sec7_model.tex), then the extensions
PARAM_PANELS = [
    ("Displacement risk", [("delta_w_B", r"$\delta_w(B)$"), ("delta_w_W", r"$\delta_w(W)$"),
                           ("delta_h_B", r"$\delta_h(B)$"), ("delta_h_W", r"$\delta_h(W)$"),
                           ("pi_c0", r"$\pi_c(0)$"), ("pi_c1", r"$\pi_c(1)$"), ("pi_c2", r"$\pi_c(2)$"),
                           ("p_H", r"$p_H$"), ("m_H", r"$m_H$")]),
    ("Search friction", [("lam_w_B", r"$\lambda_w(B)$"), ("lam_w_W", r"$\lambda_w(W)$"),
                         ("lam_h_B", r"$\lambda_h(B)$"), ("lam_h_W", r"$\lambda_h(W)$")]),
    ("Human capital", [("pi_up_w", r"$\pi^{up}_w$"), ("pi_up_h", r"$\pi^{up}_h$"), ("pi_dn_w", r"$\pi^{dn}_w$"),
                       ("pi_dn_h", r"$\pi^{dn}_h$"), ("d_w", r"$d_w$"), ("d_h", r"$d_h$")]),
    ("Work, safety net, marriage, credit", [("phi_F", r"$\phi_F$"), ("phi_P", r"$\phi_P$"),
                                            ("theta_05", r"$\theta_{05}$"), ("theta_617", r"$\theta_{617}$"),
                                            ("phi_h", r"$\phi_h$"), ("F", r"$F$"), ("kappa_S", r"$\kappa_S$"),
                                            ("sigma0_B", r"$\sigma_0(B)$"), ("sigma0_W", r"$\sigma_0(W)$"),
                                            ("sigmaJ_B", r"$\sigma_J(B)$"), ("sigmaJ_W", r"$\sigma_J(W)$"),
                                            ("a_bar", r"$\underline a$")]),
    ("Extensions", [("eta_up", r"$\eta^{up}$"), ("c_mem", r"$c_{mem}$"), ("sigma_eps", r"$\sigma_\varepsilon$")]),
]


def tex_escape(s: str) -> str:
    s = str(s)
    for a, b in (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"), ("_", r"\_"),
                 ("{", r"\{"), ("}", r"\}"), ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}"), ("|", r"$|$")):
        s = s.replace(a, b)
    return s.replace("<=", r"$\le$").replace(">=", r"$\ge$")


def fmt(v, se_like=False) -> str:
    if v is None or not np.isfinite(v):
        return ""
    a = abs(v)
    if a >= 1000:
        return f"{v:,.0f}"
    if a >= 100:
        return f"{v:.1f}"
    if a >= 1:
        return f"{v:.3f}"
    if a == 0:
        return "0"
    return f"{v:.3g}" if a >= 1e-3 else f"{v:.2e}"


def find_default_source() -> Path:
    cands = sorted([p for p in PC.RESULTS.glob("evaluate_*") if (p / "moments.csv").exists()],
                   key=lambda p: p.stat().st_mtime)
    if not cands:
        raise SystemExit("no results/evaluate_*/moments.csv: run estimate.py evaluate first")
    return cands[-1]


def load_fit(src) -> tuple[pd.DataFrame, dict]:
    """-> DataFrame(id, block, moment, value, se, sim, z, in_objective, q), info."""
    import moments as M
    p = Path(src)
    T_all = M.load_targets()
    if p.is_dir() and (p / "moments.csv").exists():
        p = p / "moments.csv"
    if p.suffix == ".csv":
        D = pd.read_csv(p)
        D = D.merge(T_all[["id", "moment", "window"]], on="id", how="left")
        info = dict(source=str(p), kind="evaluate")
        ej = p.parent / "evaluate.json"
        if ej.exists():
            e = json.loads(ej.read_text())
            info.update(Q=e.get("Q"), theta=e.get("theta"), weighting=e.get("weighting"))
        return D, info
    if p.is_dir():
        p = p / "best.json"
    best = json.loads(p.read_text())
    run = PC.run_json_of(p) or {}
    T = T_all
    if run.get("targets_csv"):
        tp = Path(run["targets_csv"])
        tp = tp if tp.exists() else p.parent / tp.name
        if tp.exists():
            T = M.load_targets(tp) if "target" in pd.read_csv(tp, nrows=1).columns else pd.read_csv(tp)
    nf = run.get("noise_file_arg")
    nf = nf if nf and Path(nf).exists() else None
    ex = [e for e in run.get("obj_exclude", list(M.OBJ_EXCLUDE)) if e in set(T["id"])]
    W = M.weights(T, run.get("weighting", "diag_noise"), exclude=ex, noise_file=nf, K=run.get("K", 3))
    mom = best.get("moments") or {}
    m = np.array([mom.get(k, np.nan) for k in T["id"]], float)
    w = np.diag(W)
    D = T[["id", "block", "moment", "value", "se", "window"]].assign(
        sim=m, z=(m - T["value"]) / T["se"], in_objective=(w > 0).astype(int),
        q=np.where(w > 0, (m - T["value"]) ** 2 * w, 0.0))
    info = dict(source=str(p), kind="run", Q=best.get("Q"), theta=best.get("theta"), run=run.get("label"),
                weighting=run.get("weighting"), noise_file_used=nf or "inputs/moment_noise.csv")
    return D, info


def fit_tex(D: pd.DataFrame, Di: pd.DataFrame | None, caption: str) -> str:
    ind = Di is not None
    ncol = 7 if ind else 5
    head = r"Moment & Data & (s.e.) & Main model & $z$" + (r" & Indep.\ shocks & $z$" if ind else "") + r" \\"
    L = [r"{\footnotesize", r"\begin{longtable}{p{" + ("6.4" if ind else "7.4") + "cm}rrrr" + ("rr" if ind else "") + "}",
         rf"\caption{{{caption}}}\label{{tab:model_fit}} \\", r"\toprule", head, r"\midrule", r"\endfirsthead",
         r"\toprule", head, r"\midrule", r"\endhead", r"\bottomrule", r"\endfoot"]
    if ind:
        Di = Di.set_index("id")
    for blk, g in D.groupby("block", sort=False):
        L.append(rf"\multicolumn{{{ncol}}}{{l}}{{\textit{{{tex_escape(blk)}}}}} \\")
        for r in g.itertuples():
            lab = tex_escape(r.moment if isinstance(r.moment, str) else r.id)
            if isinstance(getattr(r, "window", None), str):
                lab += f" ({tex_escape(r.window)})"
            if not r.in_objective:
                lab += r"$^{r}$"
            cells = [lab, fmt(r.value), f"({fmt(r.se)})", fmt(r.sim), f"{r.z:+.2f}" if np.isfinite(r.z) else ""]
            if ind:
                ri = Di.loc[r.id] if r.id in Di.index else None
                cells += [fmt(ri["sim"]) if ri is not None else "",
                          f"{ri['z']:+.2f}" if ri is not None and np.isfinite(ri["z"]) else ""]
            L.append(" & ".join(cells) + r" \\")
    L += [r"\end{longtable}", "}"]
    return "\n".join(L) + "\n"


def q_tex(D, Di, Qm, Qi) -> tuple[str, pd.DataFrame]:
    g = D.groupby("block", sort=False).agg(n=("id", "size"), n_obj=("in_objective", "sum"), Q=("q", "sum"))
    if Di is not None:
        g["Q_indep"] = Di.groupby("block", sort=False)["q"].sum()
    g["share"] = g["Q"] / g["Q"].sum()
    ind = Di is not None
    L = [r"\begin{table}[htbp]\centering\small", r"\caption{Objective by block of moments}\label{tab:q_by_block}",
         r"\begin{tabular}{lrrr" + ("r" if ind else "") + "r}", r"\toprule",
         r"Block & Moments & In objective & $Q$ main" + (r" & $Q$ indep.\ shocks" if ind else "") + r" & Share (main) \\",
         r"\midrule"]
    for b, r in g.iterrows():
        L.append(" & ".join([tex_escape(b), str(int(r["n"])), str(int(r["n_obj"])), f"{r['Q']:,.1f}"]
                            + ([f"{r['Q_indep']:,.1f}"] if ind else []) + [f"{r['share']:.3f}"]) + r" \\")
    L += [r"\midrule", " & ".join(["Total", str(int(g["n"].sum())), str(int(g["n_obj"].sum())), f"{g['Q'].sum():,.1f}"]
                                  + ([f"{g['Q_indep'].sum():,.1f}"] if ind else []) + ["1.000"]) + r" \\",
          r"\bottomrule", r"\end{tabular}",
          r"\begin{minipage}{0.95\textwidth}\footnotesize $Q$: sum over the moments in the objective of the weighted "
          r"squared deviation (model $-$ data)$^2 / (\mathrm{s.e.}^2 + \mathrm{var}_{sim})$ (diag\_noise weights). "
          r"Moments outside the objective have zero weight.\end{minipage}", r"\end{table}"]
    return "\n".join(L) + "\n", g


def load_params(spec):
    """spec: [run dir | best.json] [se.csv] -> (theta dict, se dict, free list, start dict)."""
    if not spec:
        return None
    p = Path(spec[0])
    best_p = p / "best.json" if p.is_dir() else p
    best = json.loads(best_p.read_text())
    se_p = Path(spec[1]) if len(spec) > 1 else best_p.parent / "se.csv"
    se = dict(pd.read_csv(se_p)[["param", "se"]].itertuples(index=False)) if se_p.exists() else {}
    run = PC.run_json_of(best_p) or {}
    names = run.get("names")
    start = {}
    if names and run.get("theta_start"):
        start = dict(zip(names, run["theta_start"]))
    else:
        from params import load_start
        start = load_start()
    return dict(theta=best.get("theta", best), se=se, free=run.get("free"), start=start,
                lo=dict(zip(names, run["lo"])) if names and run.get("lo") else None,
                hi=dict(zip(names, run["hi"])) if names and run.get("hi") else None)


def params_tex(P, Pi) -> str:
    from params import PARAMS, EXTRA_PARAMS, LATE_PARAMS
    lo = {p[0]: p[2] for p in PARAMS} | {p[0]: p[1] for p in EXTRA_PARAMS} | {p[0]: p[2] for p in LATE_PARAMS}
    hi = {p[0]: p[3] for p in PARAMS} | {p[0]: p[2] for p in EXTRA_PARAMS} | {p[0]: p[3] for p in LATE_PARAMS}
    ind = Pi is not None
    L = [r"\begin{table}[htbp]\centering\footnotesize",
         r"\caption{Parameter estimates}\label{tab:params_estimates}",
         r"\begin{tabular}{llrrrc" + ("rr" if ind else "") + "}", r"\toprule",
         r"Parameter & & Start & Estimate & (s.e.) & Bounds" + (r" & Indep.\ shocks & (s.e.)" if ind else "") + r" \\",
         r"\midrule"]

    def cell(PP, n):
        v = PP["theta"].get(n)
        free = PP["free"] is None or n in PP["free"]
        s = PP["se"].get(n)
        return [fmt(v) if v is not None else "", (f"({fmt(s)})" if s is not None and free else
                                                   ("fixed" if v is not None and not free else ""))]
    for panel, rows in PARAM_PANELS:
        L.append(rf"\multicolumn{{{8 if ind else 6}}}{{l}}{{\textit{{{panel}}}}} \\")
        for n, sym in rows:
            if n not in P["theta"]:
                continue
            lo_, hi_ = (P["lo"] or lo).get(n, lo.get(n)), (P["hi"] or hi).get(n, hi.get(n))
            c = [tex_escape(n), sym, fmt(P["start"].get(n, np.nan))] + cell(P, n) + [f"[{lo_:g}, {hi_:g}]"]
            if ind:
                c += cell(Pi, n)
            L.append(" & ".join(c) + r" \\")
    L += [r"\bottomrule", r"\end{tabular}",
          r"\begin{minipage}{0.95\textwidth}\footnotesize Standard errors: sandwich "
          r"$(G'WG)^{-1}G'W\Omega WG(G'WG)^{-1}$ with the bootstrap covariance of the targets plus the simulation "
          r"covariance ('fixed': not free in the run). Units as in Table~\ref{tab:model_params}.\end{minipage}",
          r"\end{table}"]
    return "\n".join(L) + "\n"


WRAPPER = r"""\documentclass[11pt]{article}
\usepackage[margin=2cm]{geometry}
\usepackage{booktabs,longtable,amsmath,amssymb}
\begin{document}
\input{tab_model_fit.tex}
\input{tab_q_by_block.tex}
%PARAMS%
\end{document}
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", nargs="?", default=None)
    ap.add_argument("--start", default=None, help="alias of SOURCE (best.json or run folder)")
    ap.add_argument("--indep", default=None)
    ap.add_argument("--params", nargs="+", default=None, help="run dir or best.json [se.csv]")
    ap.add_argument("--indep-params", dest="indep_params", nargs="+", default=None)
    ap.add_argument("--caption", default="Fit of the model: targeted and reported moments")
    ap.add_argument("--out", default=None)
    ap.add_argument("--compile", action="store_true")
    ap.add_argument("--paper", action="store_true", help="also copy the tables into IGE/paperA_joint_loss/")
    a = ap.parse_args()
    src = a.source or a.start or find_default_source()
    out = Path(a.out) if a.out else PC.out_dir("fit_table")
    out.mkdir(parents=True, exist_ok=True)
    D, info = load_fit(src)
    Di, info_i = load_fit(a.indep) if a.indep else (None, None)
    (out / "tab_model_fit.tex").write_text(fit_tex(D, Di, a.caption), encoding="utf-8")
    qt, g = q_tex(D, Di, info.get("Q"), (info_i or {}).get("Q"))
    (out / "tab_q_by_block.tex").write_text(qt, encoding="utf-8")
    P = load_params(a.params)
    Pi = load_params(a.indep_params)
    if P:
        (out / "tab_params_estimates.tex").write_text(params_tex(P, Pi), encoding="utf-8")
    js = dict(main=info, indep=info_i, Q_main_tables=float(D["q"].sum()),
              Q_indep_tables=float(Di["q"].sum()) if Di is not None else None,
              n_moments=int(len(D)), n_in_objective=int(D["in_objective"].sum()),
              max_abs_z=float(np.nanmax(np.abs(D["z"]))), q_by_block=g.reset_index().to_dict("records"))
    for k in ("main", "indep"):
        if js[k]:
            js[k].pop("theta", None)
    PC.write_json(out / "fit_table.json", js)
    (out / "test_wrapper.tex").write_text(WRAPPER.replace("%PARAMS%", r"\input{tab_params_estimates.tex}" if P else ""))
    print(f"Q in the tables {js['Q_main_tables']:,.1f} (source Q {info.get('Q')}); {js['n_in_objective']} of "
          f"{js['n_moments']} moments in the objective")
    if a.compile:
        exe = shutil.which("pdflatex")
        if not exe:
            print("pdflatex not found: skipped")
        else:
            for _ in range(2):
                r = subprocess.run([exe, "-interaction=nonstopmode", "-halt-on-error", "test_wrapper.tex"], cwd=out,
                                   capture_output=True, text=True)
            ok = r.returncode == 0 and (out / "test_wrapper.pdf").exists()
            print("pdflatex:", "ok" if ok else "FAILED (see test_wrapper.log)")
            for ext in ("aux", "out"):
                f = out / f"test_wrapper.{ext}"
                if f.exists():
                    f.unlink()
            if not ok:
                sys.exit(1)
    if a.paper:
        for f in ("tab_model_fit.tex", "tab_q_by_block.tex", "tab_params_estimates.tex"):
            if (out / f).exists():
                shutil.copy2(out / f, PAPER / f)
        print(f"copied into {PAPER}")
    print(f"-> {out}")


if __name__ == "__main__":
    main()
