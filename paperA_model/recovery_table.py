"""Paper A model: LaTeX recovery table from a pseudo-data recovery run (plan WP3 item 1).

Input: a run folder of 'estimate.py polish --pseudo' (or 'run --pseudo') that holds recovery_report.csv (written by
recovery_report.py at the end of the polish; for a CMA run, run recovery_report.py <run> <jacobian> <noise> first),
e.g. results/hpc_runs/recovery_gn_all_<stamp>/. Rows in the order of tab:model_params (fit_table.PARAM_PANELS);
columns: truth, start, recovered, noise s.e., z (noise), data s.e., z (data); 'yes' when the estimate is within 2
noise s.e. of the truth.
  .venv/Scripts/python.exe paperA_model/recovery_table.py <run dir> [--compile] [--paper]
  (--start <run dir> is accepted as an alias of the positional argument)
Output: results/recovery_table_<stamp>/tab_recovery.tex, recovery_table.json, test_wrapper.tex (--compile: pdflatex);
--paper copies tab_recovery.tex into paperA_joint_loss/.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd

import post_common as PC
from fit_table import PARAM_PANELS, PAPER, fmt, tex_escape


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run", nargs="?", default=None)
    ap.add_argument("--start", default=None, help="alias of the run folder")
    ap.add_argument("--out", default=None)
    ap.add_argument("--compile", action="store_true")
    ap.add_argument("--paper", action="store_true")
    a = ap.parse_args()
    rd = Path(a.run or a.start or "")
    if not rd.is_dir():
        rd = rd.parent
    f = rd / "recovery_report.csv"
    if not f.exists():
        raise SystemExit(f"{f} missing: run recovery_report.py on the run first")
    R = pd.read_csv(f).set_index("param")
    run = PC.run_json_of(rd) or {}
    best = json.loads((rd / "best.json").read_text()) if (rd / "best.json").exists() else {}
    out = Path(a.out) if a.out else PC.out_dir("recovery_table")
    out.mkdir(parents=True, exist_ok=True)
    L = [r"\begin{table}[htbp]\centering\footnotesize",
         r"\caption{Recovery of known parameters from pseudo-data}\label{tab:recovery}",
         r"\begin{tabular}{llrrrrrrrc}", r"\toprule",
         r"Parameter & & Truth & Start & Recovered & Noise s.e. & $z$ (noise) & Data s.e. & $z$ (data) & Within 2 \\",
         r"\midrule"]
    done = set()
    for panel, rows in PARAM_PANELS:
        rows = [(n, s) for n, s in rows if n in R.index]
        if not rows:
            continue
        L.append(rf"\multicolumn{{10}}{{l}}{{\textit{{{panel}}}}} \\")
        for n, sym in rows:
            r = R.loc[n]
            done.add(n)
            L.append(" & ".join([tex_escape(n), sym, fmt(r["truth"]), fmt(r["start"]), fmt(r["estimate"]),
                                 fmt(r["se_noise"]), f"{r['z_est']:+.1f}", fmt(r["se_data"]),
                                 f"{r['z_est_data']:+.2f}", "yes" if abs(r["z_est"]) < 2 else "no"]) + r" \\")
    for n in R.index:                                           # anything not in the paper's list
        if n not in done:
            r = R.loc[n]
            L.append(" & ".join([tex_escape(n), "", fmt(r["truth"]), fmt(r["start"]), fmt(r["estimate"]),
                                 fmt(r["se_noise"]), f"{r['z_est']:+.1f}", fmt(r["se_data"]),
                                 f"{r['z_est_data']:+.2f}", "yes" if abs(r["z_est"]) < 2 else "no"]) + r" \\")
    n2n = int((R["z_est"].abs() < 2).sum())
    n2d = int((R["z_est_data"].abs() < 2).sum())
    L += [r"\bottomrule", r"\end{tabular}",
          r"\begin{minipage}{0.95\textwidth}\footnotesize Targets: the model's moments at the truth (CRN seed "
          + f"{run.get('target_seed', '')}" + r"); start: truth perturbed by $N(0, "
          + f"{run.get('start_noise', '')}" + r")$ in logistic units. $z$ = (recovered $-$ truth) / s.e.; noise s.e. = "
          r"simulation noise only, data s.e. = sandwich with the bootstrap covariance of the targets plus simulation "
          rf"noise. Within 2 noise s.e.: {n2n} of {len(R)}; within 2 data s.e.: {n2d} of {len(R)}. "
          rf"Best $Q$ {fmt(best.get('Q', np.nan))}. Run \texttt{{{tex_escape(rd.name)}}}.\end{{minipage}}",
          r"\end{table}"]
    (out / "tab_recovery.tex").write_text("\n".join(L) + "\n", encoding="utf-8")
    PC.write_json(out / "recovery_table.json", dict(run=str(rd), n_params=len(R), within2_noise=n2n, within2_data=n2d,
                                                     best_Q=best.get("Q"), max_abs_z_noise=float(R["z_est"].abs().max()),
                                                     max_abs_z_data=float(R["z_est_data"].abs().max())))
    (out / "test_wrapper.tex").write_text("\\documentclass[11pt]{article}\n\\usepackage[margin=2cm]{geometry}\n"
                                          "\\usepackage{booktabs,amsmath,amssymb}\n\\begin{document}\n"
                                          "\\input{tab_recovery.tex}\n\\end{document}\n")
    print(f"{rd.name}: within 2 noise s.e. {n2n} of {len(R)}; within 2 data s.e. {n2d} of {len(R)}")
    if a.compile and shutil.which("pdflatex"):
        r = subprocess.run([shutil.which("pdflatex"), "-interaction=nonstopmode", "-halt-on-error", "test_wrapper.tex"],
                           cwd=out, capture_output=True, text=True)
        print("pdflatex:", "ok" if r.returncode == 0 else "FAILED (see test_wrapper.log)")
    if a.paper:
        shutil.copy2(out / "tab_recovery.tex", PAPER / "tab_recovery.tex")
    print(f"-> {out}")


if __name__ == "__main__":
    main()
