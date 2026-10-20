#!/bin/bash
#SBATCH --job-name=IGE-model
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --mem=10G
#SBATCH --time=01:30:00
#SBATCH --output=ige_smm_%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=jiaqi.li@sheffield.ac.uk
# Paper B (IGE) structural model on Stanage: SMM of nested models A-D, post-estimation, results pushed to GitHub.
# Since 2026-10-20 Paper B lives with Paper A in their own repository (github.com/lijiaqi6/JointLoss); paper 1 stays in
# Selection-vs-risk (~/svr). Paper B keeps its own clone ~/ige (sparse: model only), its own .venv, its own scratch
# folder /mnt/parscratch/users/$USER/ige_smm_results, its own results folder model/hpc_runs/. Paper A uses ~/jointloss.
#
# One-time setup on the login node. The old ~/ige is a clone of Selection-vs-risk: move it aside first
# (mv ~/ige ~/ige_svr_old). GitHub deploy keys belong to one repository, so the key used by ~/svr does not open this
# one: use the JointLoss deploy key and its ssh Host alias 'github-jointloss' (set up once, see
# paperA_model/hpc_job_a.py), then:
#   git clone --filter=blob:none --sparse git@github-jointloss:lijiaqi6/JointLoss.git ~/ige
#   cd ~/ige && git sparse-checkout set model
#   git config user.name lijiaqi6 && git config user.email london6will@gmail.com
#   uv venv --python 3.12.13 .venv && uv pip install --python .venv numpy==2.5.3 pandas==3.0.5 scipy==1.18.1 cma==4.5.0
#   then copy the person-level input once: scp model/output/sons_types.csv to ~/ige/model/output/
#
# Submit from ~/ige (after git pull): test first (about 10 minutes), the full run only if the test passes:
#   cd ~/ige && git pull
#   jt=$(sbatch --parsable --job-name=IGE-test --time=00:40:00 model/hpc_ige.sh test)
#   sbatch --dependency=afterok:$jt --job-name=IGE-ABCD model/hpc_ige.sh full
#   squeue -u $USER -o "%.10i %.25j %.8T %.10M %R"
#
# The job runs the code of one commit (IGE_COMMIT, default the commit checked out in ~/ige when the job starts),
# extracted with git archive into node-local storage, so pulls of ~/ige do not change a running job.
#
# Settings are ARGUMENTS after the mode, IGE_NAME=value (Stanage does not pass the submission environment into the
# job: on 2026-10-18 jobs 11858549-52 and 11858625-26 given IGE_MODELS=... on the command line re-ran the default ABCD):
#   sbatch --job-name=IGE-E --time=01:30:00 model/hpc_ige.sh full IGE_MODELS=E \
#     IGE_START=hpc_runs/ige_full_20261018_125238/estimates.json:D
# Recognised: IGE_MODELS, IGE_START, IGE_MAXFEV, IGE_SIG0, IGE_SELECT, IGE_STEPS (age,rehire), IGE_FIX (muG),
# IGE_RUNS (lattice mode, space-separated run folders relative to model, quoted), IGE_LATTICE_SEEDS,
# IGE_LATTICE_R, IGE_COMMIT, IGE_R (simulated sons per son), IGE_SET (start overrides "gx=0.008"), IGE_POLISH
# (evaluations of a second CMA-ES at sigma 0.15), IGE_RUN (run-name prefix; the chain uses it so that later stages
# can name earlier ones' scratch folders: $OUT_ROOT/<IGE_RUN>_j<job>/estimates.json). Lattice (no estimation; R = 20 peaks at 15.2 GB, so --mem=20G):
#   sbatch --job-name=IGE-lattice --mem=20G --time=00:30:00 model/hpc_ige.sh lattice \
#     IGE_RUNS="hpc_runs/<run1> hpc_runs/<run2>"
# Workers = popsize = cores - 2 (one generation per parallel round). IGE_NOPUSH=1 skips the push (local dry runs).
set -euo pipefail

MODE=${1:-full}
shift || true
for arg in "$@"; do
  case "$arg" in
    IGE_MODELS=*|IGE_START=*|IGE_MAXFEV=*|IGE_SIG0=*|IGE_SELECT=*|IGE_STEPS=*|IGE_FIX=*|IGE_RUNS=*|IGE_LATTICE_SEEDS=*|\
IGE_LATTICE_R=*|IGE_COMMIT=*|IGE_NOPUSH=*|IGE_R=*|IGE_SET=*|IGE_POLISH=*|IGE_RUN=*|IGE_MOMENTS=*) export "$arg" ;;
    *) echo "unknown argument '$arg' (settings are IGE_NAME=value)"; exit 2 ;;
  esac
done
REPO=${IGE_REPO:-$HOME/ige}
PY=${IGE_PYTHON:-$REPO/.venv/bin/python}
OUT_ROOT=${IGE_SMM_OUT:-/mnt/parscratch/users/$USER/ige_smm_results}
JOB=${SLURM_JOB_ID:-local}
CPUS=${SLURM_CPUS_PER_TASK:-6}
STAMP=$(date +%Y%m%d_%H%M%S)
T0=$(date +%s)
RUN=${IGE_RUN:-ige_${MODE}_${STAMP}}_j${JOB}                                   # job id: jobs starting in the same second differ
SHA=$(git -C "$REPO" rev-parse "${IGE_COMMIT:-HEAD}")
CODE=${TMPDIR:-/tmp}/ige_code_$JOB
rm -rf "$CODE" && mkdir -p "$CODE"
git -C "$REPO" archive --format=tar "$SHA" model | tar -x -C "$CODE"
# Person-level PSID input (race, parental income, schooling, birth year per son): never in git (PSID terms), kept
# git-ignored in the clone and copied into the snapshot here. Put it there once with scp or cp (see the commit message).
TYPES=$REPO/model/output/sons_types.csv
if [ ! -f "$TYPES" ]; then
  echo "missing $TYPES (person-level PSID input, not in git): copy it into ~/ige/model/output/ first"; exit 4
fi
cp "$TYPES" "$CODE/model/output/sons_types.csv"
echo "job $JOB mode $MODE code snapshot $SHA run $RUN on $(hostname) with $CPUS cores"
echo "settings: $(env | grep -E '^IGE_(MODELS|START|MAXFEV|SIG0|SELECT|STEPS|FIX|RUNS|LATTICE_SEEDS|LATTICE_R|COMMIT|R|SET|POLISH|RUN|MOMENTS)=' | tr '\n' ' ')"

export IGE_OUT=$OUT_ROOT/$RUN
export IGE_WORKERS=$((CPUS > 3 ? CPUS - 2 : 1))
export IGE_POPSIZE=$((IGE_WORKERS > 18 ? IGE_WORKERS : 18))
export IGE_MAXFEV=${IGE_MAXFEV:-15000,8000,8000,8000}
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
[ "$MODE" = test ] && export SMM_TEST=1
mkdir -p "$IGE_OUT"
cd "$CODE/model"

STATUS=0
# 1. checks: package versions and the objective at the starting values against the local machine (22,856.15), always
#    with the model steps off (a check of the machine and environment, not of the specification)
IGE_STEPS= IGE_FIX= IGE_R=5 IGE_SET= IGE_MOMENTS= "$PY" - <<'EOF' || STATUS=1
import json, sys, numpy, pandas, scipy, cma
import numpy as np
import core, estimate as est
want = {"numpy": "2.5.3", "pandas": "3.0.5", "scipy": "1.18.1", "cma": "4.5.0"}
have = {"numpy": numpy.__version__, "pandas": pandas.__version__, "scipy": scipy.__version__, "cma": cma.__version__}
print("python", sys.version.split()[0], have, "PASS" if have == want else f"WARN (local: {want})")
est.G_.update(est.setup())
th = np.array([json.load(open(est.INP / "theta_start.json"))[p] for p in core.PARAMS])
q = est.Q_of(th)
ok = abs(q - 22856.15413388641) < 1.0
print(f"Q at the starting values {q:.2f} (local 22856.15): {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
EOF
# 2. estimation and post-estimation; or (mode lattice) only the lattice on common draws of the runs in IGE_RUNS
if [ "$MODE" = lattice ]; then
  [ $STATUS -eq 0 ] && { "$PY" lattice_q.py $IGE_RUNS || STATUS=2; }
else
  if [ $STATUS -eq 0 ]; then
    "$PY" estimate.py || STATUS=2
  fi
  if [ $STATUS -eq 0 ]; then
    "$PY" postestimation.py || STATUS=3
  fi
fi
echo "status $STATUS (0 ok, 1 checks failed, 2 estimation failed, 3 post-estimation failed)"

# 3. results back through GitHub: model/hpc_runs/<run>/ (tests under hpc_runs/tests/)
if [ -z "${IGE_NOPUSH:-}" ]; then
  SUB=$([ "$MODE" = test ] && echo "hpc_runs/tests" || echo "hpc_runs")
  DEST=$REPO/model/$SUB/$RUN
  mkdir -p "$DEST"
  for f in estimates.json smm_report.md postestimation.json postestimation.md smm_progress.log lattice.json lattice.md; do
    [ -f "$IGE_OUT/$f" ] && cp "$IGE_OUT/$f" "$DEST/${f%.log}$([ "${f##*.}" = log ] && echo _log.txt)"
  done
  LOG=${SLURM_SUBMIT_DIR:-$REPO}/ige_smm_$JOB.log
  [ -f "$LOG" ] && cp "$LOG" "$DEST/job_log.txt"            # .txt: *.log is git-ignored
  printf "run %s\njob %s\ncode %s\nmode %s\nstatus %s\ncores %s workers %s popsize %s maxfevals %s\n" \
    "$RUN" "$JOB" "$SHA" "$MODE" "$STATUS" "$CPUS" "$IGE_WORKERS" "$IGE_POPSIZE" "$IGE_MAXFEV" > "$DEST/summary.txt"
  echo "settings $(env | grep -E '^IGE_(MODELS|START|SIG0|SELECT|STEPS|FIX|RUNS|LATTICE_SEEDS|LATTICE_R|R|SET|POLISH|RUN|MOMENTS)=' | sort | tr '\n' ' ')" \
    >> "$DEST/summary.txt"
  # resources, for sizing later requests: wall time so far, peak memory of the batch step (Slurm accounting; empty
  # outside Slurm), and what was requested
  echo "elapsed_min $(( ($(date +%s) - T0) / 60 ))" >> "$DEST/summary.txt"
  echo "maxrss $(sstat -n -j "${SLURM_JOB_ID:-0}.batch" -o MaxRSS 2>/dev/null | xargs || true)" >> "$DEST/summary.txt"
  echo "requested $(scontrol show job "${SLURM_JOB_ID:-0}" 2>/dev/null | grep -o 'TimeLimit=[^ ]*\|mem=[^,]*' | tr '\n' ' ' || true)" \
    >> "$DEST/summary.txt"
  cd "$REPO"
  git add "model/$SUB/$RUN"
  git commit -q -m "IGE HPC results: $RUN (job $JOB, status $STATUS)" || true
  for i in 1 2 3 4 5; do
    if git pull -q --rebase origin main && git push -q origin HEAD:main; then echo "push: $RUN pushed"; break; fi
    echo "push attempt $i failed"; sleep 20
  done
fi
rm -rf "$CODE"
exit $STATUS
