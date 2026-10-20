r"""Regenerate every Section 8 output from a selected-model run (Fable second plan, Block 4, 2026-10-19).

    python regen.py --run <run folder> --model E            # make that run the paper's selected model
    python regen.py --check                                  # rerun on the current final_x4 model E; tables must not change

Steps, with the code switches (IGE_STEPS, IGE_FIX, IGE_MOMENTS) taken from the run's estimates.json and R = 20:
copy the run's estimates into output/final_x4/estimates_E.json; postestimation.py (all experiments, and the H4
experiments for the age and tercile table); validation_run.py; sensitivity.py; panel_diag.py; figure_fit.py; tables.py.
Reports which paper tables changed (byte comparison with the versions before the run). The lattice, H4 seeds and
step tables are not touched (they belong to the lattice, not to the selected model).
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent / "paperB_age_profile"
F = HERE / "output" / "final_x4"
KEEP = ("theta", "Q", "se", "moments", "untargeted", "vcov", "jacobian", "jac_names")
H4CFS = "Equal pay-off of parental income in accumulation (dgx = 0)|No pay-off of parental income in accumulation (gx = dgx = 0)"


def run(cmd, env, cwd=HERE):
    print(">", " ".join(cmd), flush=True)
    r = subprocess.run(cmd, env=env, cwd=cwd, capture_output=True, text=True)
    if r.returncode:
        print(r.stdout[-2000:], r.stderr[-3000:])
        sys.exit(f"failed: {' '.join(cmd)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--run")
    ap.add_argument("--model", default="E")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.check:
        E = json.load(open(F / "estimates_E.json"))
        src = {"steps": E["steps"], "fixed": E["fixed"], "R": E.get("R", 20), "moments": E.get("moments", "targets"),
               "E": E["E"], "run": E.get("run")}
    else:
        R = json.load(open(Path(a.run) / "estimates.json"))
        e = R[a.model]
        src = {"run": Path(a.run).name, "steps": R["steps"], "fixed": R["fixed"], "R": R.get("R"),
               "moments": R.get("moments", "targets"), "E": {k: e[k] for k in KEEP if k in e}}
        json.dump(src, open(F / "estimates_E.json", "w"), indent=1)
    env = dict(os.environ, IGE_STEPS=",".join(src["steps"]), IGE_FIX=",".join(src["fixed"]), IGE_R="20",
               IGE_MOMENTS="" if src["moments"] == "targets" else src["moments"], IGE_SELECT="E")
    before = {p.name: p.read_bytes() for p in PAPER.glob("tab_model_*.tex")}
    before.update({p.name: p.read_bytes() for p in PAPER.glob("fig_model_fit.png")})
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(F / "estimates_E.json", Path(tmp) / "estimates.json")
        run([sys.executable, "postestimation.py"], dict(env, IGE_OUT=tmp))
        shutil.copy(Path(tmp) / "postestimation.json", HERE / "output" / "postestimation_Lx4_E.json")
        shutil.copy(Path(tmp) / "postestimation.md", HERE / "output" / "postestimation_Lx4_E.md")
        run([sys.executable, "postestimation.py"], dict(env, IGE_OUT=tmp, IGE_CFS=H4CFS))
        shutil.copy(Path(tmp) / "postestimation.json", HERE / "output" / "postestimation_Lx4_E_h4.json")
    for script in ("validation_run.py", "sensitivity.py", "panel_diag.py", "figure_fit.py", "tables.py"):
        run([sys.executable, script], env)
    after = {p.name: p.read_bytes() for p in PAPER.glob("tab_model_*.tex")}
    after.update({p.name: p.read_bytes() for p in PAPER.glob("fig_model_fit.png")})
    changed = sorted(k for k in after if before.get(k) != after[k])
    print("changed:", changed or "none")
