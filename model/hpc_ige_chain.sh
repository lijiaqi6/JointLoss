#!/bin/bash
# Final hypothesis lattice for Paper B as a chain of Stanage jobs (Fable memo, second round, R6), run from ~/ige:
#   bash model/hpc_ige_chain.sh TAG "IGE_STEPS=age,rehire" "IGE_FIX=muG,du" START_A START_D [extra settings...]
# e.g.
#   bash model/hpc_ige_chain.sh f1 IGE_STEPS=age,rehire IGE_FIX=muG,du \
#     hpc_runs/ige_full_20261018_200455_j11859361/estimates.json:A hpc_runs/ige_full_20261018_200456_j11859362/estimates.json:D
# Every model starts from the best solution of its nested neighbours, so a more general model never starts worse than
# a model nested in it (nesting holds by construction at the estimation draws):
#   stage 1  A  from START_A and START_D (restricted)
#   stage 2  B, F, G  from A
#   stage 3  C from B and F; H from B and G; E from F and G
#   stage 4  D from C, H, E and START_D
#   then     lattice_q on the eight folders (seeds 7-16, R = 5 and 20)
# Each estimation: R = 20 simulated sons per son, popsize 30, 12,000 evaluations + 4,000 polish at sigma 0.15, 32 cores,
# --mem=24G (peak 18.6-19.8 GB at R = 20 with 31 processes). Job names IGE-L<TAG>-<model>. Scratch folders
# $OUT_ROOT/L<TAG>_<model>_j<job>; results pushed to model/hpc_runs/ like every IGE job.
set -euo pipefail
TAG=$1; STEPS=$2; FIX=$3; SA=$4; SD=$5; shift 5
EXTRA=("$@")
OUT_ROOT=${IGE_SMM_OUT:-/mnt/parscratch/users/${USER:-$(whoami)}/ige_smm_results}
J=model/hpc_ige.sh
COMMON=(--time=01:30:00 --mem=24G)
SET=(IGE_R=20 IGE_MAXFEV=12000,12000,12000,12000,12000,12000,12000,12000 IGE_POLISH=4000 "$STEPS" "$FIX" "${EXTRA[@]}")
declare -A JOB
sub() {                                     # sub MODEL "START candidates" [dependency job ids...]
  local m=$1 st=$2; shift 2
  local dep=()
  [ $# -gt 0 ] && dep=(--dependency=afterok:$(IFS=:; echo "$*"))
  JOB[$m]=$(sbatch --parsable "${COMMON[@]}" "${dep[@]}" --job-name=IGE-L$TAG-$m $J full IGE_MODELS=$m \
            IGE_RUN=L${TAG}_$m IGE_START=$st "${SET[@]}")
  echo "model $m: job ${JOB[$m]} (start $st)"
}
res() { echo "$OUT_ROOT/L${TAG}_$1_j${JOB[$1]}/estimates.json:$1"; }
sub A "$SA,$SD"
for m in B F G; do sub $m "$(res A)" ${JOB[A]}; done
sub C "$(res B),$(res F)" ${JOB[B]} ${JOB[F]}
sub H "$(res B),$(res G)" ${JOB[B]} ${JOB[G]}
sub E "$(res F),$(res G)" ${JOB[F]} ${JOB[G]}
sub D "$(res C),$(res H),$(res E),$SD" ${JOB[C]} ${JOB[H]} ${JOB[E]}
RUNS=""
for m in A B F G C H E D; do RUNS="$RUNS $OUT_ROOT/L${TAG}_${m}_j${JOB[$m]}"; done
JL=$(sbatch --parsable --time=00:30:00 --mem=20G --dependency=afterok:${JOB[D]}:${JOB[C]}:${JOB[H]}:${JOB[E]} \
     --job-name=IGE-L$TAG-lattice $J lattice IGE_RUNS="${RUNS# }" "$STEPS" "$FIX" "${EXTRA[@]}")
echo "lattice: job $JL"
squeue -u "${USER:-$(whoami)}" -o "%.10i %.25j %.8T %.10M %R" | grep "IGE-L$TAG" || true
