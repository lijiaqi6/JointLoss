r"""The model's development, step by step, read from the HPC run folders on origin/main (Fable 10-hour plan, Block 7,
2026-10-19). Each row: the step, the model, its Q at the step's draws, the comparison run on the same draws, and the
change in Q. Writes output/final_x4/steps.json (aggregates) for tables.py (tab_steps)."""
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                                   # repository root


def est(run, m):
    txt = subprocess.run(["git", "show", f"origin/main:model/hpc_runs/{run}/estimates.json"], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout
    return json.loads(txt)[m]["Q"]


R1 = "ige_full_20261018_125238"
# (step, what changed, model, run, draws, comparison (run, model) or None)
STEPS = [
    ("1", "first lattice: race in wage level and job loss only", "A", (R1, "A"), "R = 5", None),
    ("1", "first lattice: H2 + H3 (selected)", "E", ("ige_full_20261018_194444_j11859353", "E"), "R = 5",
     ("ige_full_20261018_194443_j11859358", "A")),
    ("2", "age slopes of job loss and of the on-the-job search friction", "A",
     ("ige_full_20261018_194443_j11859359", "A"), "R = 5", ("ige_full_20261018_194443_j11859358", "A")),
    ("2", "same, model D", "D", ("ige_full_20261018_195922_j11859360", "D"), "R = 5", (R1, "D")),
    ("3", "re-employment in the year of a displacement", "A", ("ige_full_20261018_200455_j11859361", "A"), "R = 5",
     ("ige_full_20261018_194443_j11859359", "A")),
    ("3", "same, model D", "D", ("ige_full_20261018_200456_j11859362", "D"), "R = 5",
     ("ige_full_20261018_195922_j11859360", "D")),
    ("3a", "match premium of $G$ jobs fixed at 0", "D", ("ige_full_20261018_200456_j11859363", "D"), "R = 5",
     ("ige_full_20261018_200456_j11859362", "D")),
    ("3b", "depreciation out of work fixed at 0 (and $\\mu_G = 0$)", "A",
     ("ige_full_20261018_212217_j11860451", "A"), "R = 5", ("ige_full_20261018_200455_j11859361", "A")),
    ("4", "race-neutral pay-off of parental income in accumulation", "A",
     ("ige_full_20261018_213123_j11860453", "A"), "R = 5", ("ige_full_20261018_212217_j11860451", "A")),
    ("4", "its racial difference (H4)", "A", ("ige_full_20261018_213123_j11860454", "A"), "R = 5",
     ("ige_full_20261018_213123_j11860453", "A")),
    ("4", "H4 given H2 + H3", "E", ("ige_full_20261018_215612_j11860456", "E"), "R = 5",
     ("ige_full_20261018_214332_j11860455", "E")),
    ("5", "final lattice, H4 alone", "A", ("Lx4_A_j11861506", "A"), "R = 20",
     ("ige_full_20261018_224720_j11861515", "A")),
    ("5", "final lattice, selected model (H2 + H3 + H4)", "E", ("Lx4_E_j11861512", "E"), "R = 20",
     ("ige_full_20261018_224720_j11861516", "E")),
]

if __name__ == "__main__":
    out = []
    for step, what, m, (run, mm), draws, cmp_ in STEPS:
        q = est(run, mm)
        q0 = est(*cmp_) if cmp_ else None
        out.append(dict(step=step, what=what, model=m, run=run, draws=draws, Q=q,
                        comparison=cmp_[0] if cmp_ else None, Q_comparison=q0, dQ=(q - q0) if q0 is not None else None))
        print(step, m, round(q, 2), None if q0 is None else round(q - q0, 2), what)
    json.dump(out, open(HERE / "output" / "final_x4" / "steps.json", "w"), indent=1)
