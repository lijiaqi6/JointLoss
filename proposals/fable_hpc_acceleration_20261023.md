# Which additional Stanage jobs would accelerate Paper A now (Fable, 2026-10-24)

Read-only advice from the code (`estimate.py`, `hpc_job_a.py`, `counterfactuals.py`, `post_common.py`), plan 4b to
its end, and the committed run folders. Nothing was run or edited.

## Verdict: three jobs, in this order; nothing else now

| rank | job | question it answers | code needed | cores x wall | fair-share cost |
|---|---|---|---|---|---|
| 1 | `Joint-indep-final` | the independent-shock comparator at the final specification and weights (fit-table column, `--indep` of the counterfactuals) | none | 32 x ~8 h (`--time 12:00:00`) | one LM job |
| 2 | `Joint-cf-smoke` | does the headline survive at the stage-2 point (decorrelation, UI, race scenarios) | none with `sbatch --wrap` (live clone); or 8 lines in `hpc_job_a.py` | 8 x ~1 h | small |
| 3 | `Joint-F07` | does F's upper bound 0.6 bind (profile point beyond the bound, other 29 re-optimised) | none | 32 x ~6 h (`--time 10:00:00`) | one LM job; PI's call (a point outside the bound) |

Not now: a multi-start LM (the running CMA-ES 11927760 is the local-optimum check; a second LM would duplicate it), a
theta_617 = 0 LM (the Wald at stage 2 rejects it, z = -3.3***; by the PI's rule of 2026-10-21 no LM rerun), a second
recovery, any `evaluate`-based profile on 32 cores (one 5-minute evaluation per allocation wastes fair share; profiles
with the other parameters held belong on the PC once `final1` has freed it), and the F = 0.5 profile point (only needed
for a confidence interval if job 3 shows the bound does not bind; run it then).

Every command starts from the committed stage-2 point `runs/polish_hcage2r0_20261023_200316_p800/best.json`
(commit 00c8a5a; the snapshot excludes `paperA_model/results`, so full paths) under the new noise weights, the same
objective as `final1` (PC) and `Joint-cma-final`. `final1` will move the point by a few Q; the three jobs re-optimise
their own parameters, so they do not need its end point and need not be rerun after it.

## 1. `Joint-indep-final`: the independent-shock model

**Why now.** The paper's main table and the counterfactual module compare the correlated model with the model
without correlated job loss (`fit_table.py --indep`, `counterfactuals.py --indep`). Plan step 6 puts this job
"from the preferred specification"; that specification is now fixed for the first reportable estimate (age term,
beta free, sigmaJ pooled, a_bar at its data value, new weights). The job is independent of the final polish: the
restricted model has its own optimum, and starting it from `hcage2r0` instead of `final1`'s end costs nothing but
a few LM iterations. Run after `final1` it would be sequential (~a day later).

**Restrictions.** `pi_c0 = pi_c1 = 0`, `m_H = 1` (no common shock, no couple type). With `m_H = 1` the type share
`p_H` enters nothing (it only assigns couples to a type with identical hazards), so its Jacobian column is zero:
hold it too, otherwise `lm_iterate` carries a flat column (its `Dg` floor of 1e-12 keeps the solve finite, but the
condition number is meaningless). `pi_c2` is already held at the default size. The deltas must rise ~25-30% to
restore the marginal hazards (plan section 2), which is a few LM iterations.

```
cd ~/jointloss && git pull && sbatch --job-name=Joint-indep-final --time=12:00:00 paperA_model/hpc_job_a.py polish \
  --label indep_final \
  --start $HOME/jointloss/paperA_model/results/runs/polish_hcage2r0_20261023_200316_p800/best.json \
  --noise-file $HOME/jointloss/paperA_model/results/hpc_runs/noise_20261023_160642_j11917862/moment_noise.csv \
  --hc-age on --fix a_bar=25.639 pi_c0=0 pi_c1=0 m_H=1 p_H=0.0193 --free-extra beta --tie sigmaJ_B=sigmaJ_W \
  --bound-margin 0 --iters 20 --push
```

Expected: warm-up Q well above 863 (the monthly and annual joint-loss blocks lose their fit), then a fall over
10-15 iterations; 20 iterations ~ 7 h at ~20 min each plus the final Jacobian and s.e. The result's Q minus
`final1`'s Q is the fit contribution of correlated job loss (noise band ~57 under common draws).

## 2. `Joint-cf-smoke`: counterfactuals at the stage-2 point

**Why now.** If the decorrelation scenarios (i_indep, i_mean), the UI extension and the race scenarios give a
different picture at the new estimate than at the analytic start (consumption-only CE +1.09% for (i), joint losses
534 -> 37), the modelling agenda changes now rather than after `final1` and the CMA-ES. The PC cannot run it without
slowing `final1` (14 of 16 threads busy for ~27 h).

**How.** `counterfactuals.py` is not a `hpc_job_a.py` command (choices: run, polish, jacobian, se, noise,
evaluate), so either (a) submit it directly from the live clone with `sbatch --wrap` (no code; the job reads the
clone, not a snapshot: push no code change while it runs, ~1 h), or (b) add a `counterfactuals` command to
`hpc_job_a.py`: append it to the `choices` list, and in `main()` route it to
`[sys.executable, "-u", str(code / MODEL / "counterfactuals.py"), "--threads", str(threads)] + passthrough` (no
`--workers`), with `PAPERA_OUT` left as set so the run folder lands on scratch and `--push` copies it (~8 lines).
Option (a) now; (b) before the final full-size run.

`--start` must be the run folder (not `best.json`), so `post_common.setup` reads `--hc-age on`, the ties and the
fixed parameters from its `run.json`; the run's noise-file entry is not found on Stanage and falls back to
`inputs/moment_noise.csv` (a note in the output; the weights do not enter the scores). Size: the estimation size
`k_s2_era1_a20` for this smoke test (the parameters were estimated there; `full` adds three eras and lets `pi_c2`
enter at its unestimated start value 0.00096; `full` is for the final run at `final1`'s end). One evaluation at the
default size is ~300 s alone on Stanage; 9 scenarios at 8 threads ~ 45-60 min. Memory < 8 GB.

```
cd ~/jointloss && git pull && sbatch --job-name=Joint-cf-smoke --time=03:00:00 --cpus-per-task=8 --mem=16G \
  --output=joint_%x_%j.log --mail-type=BEGIN,END,FAIL --mail-user=jiaqi.li@sheffield.ac.uk \
  --wrap="cd \$HOME/jointloss && NUMBA_CACHE_DIR=\$TMPDIR/numba_cf OMP_NUM_THREADS=1 .venv/bin/python -u paperA_model/counterfactuals.py \
  --start \$HOME/jointloss/paperA_model/results/runs/polish_hcage2r0_20261023_200316_p800 \
  --size k_s2_era1_a20 --threads 8"
```

Output: `~/jointloss/paperA_model/results/counterfactuals_<stamp>_j<job>/` (scores.csv, counterfactuals.md/.json;
aggregate numbers only) in the clone; commit and push it from the login node (`git add paperA_model/results/
counterfactuals_*; git commit; git push`). Rerun with `--indep <indep_final run folder>` and `--size full` at the
final estimate once jobs 1 and `final1` are in.

## 3. `Joint-F07`: does F's bound bind?

**Why.** F (money cost of work, $ thousand a month per working spouse) sits at its upper bound 0.6 in every run
since `restr`, and the logistic transform freezes it there (code review B2): the LM cannot tell whether the model
wants F above 0.6, and the sandwich s.e. at a bound is not valid. The paper must say which it is. The profile at
`restr` with the other parameters held (Q 1,025 at 0.6, 1,204 at 0.7) does not settle it, because the work
parameters absorbed every restriction so far (a_bar, g_age). One LM with F fixed at 0.7 and the other 29 free
answers it: if its Q is below `final1`'s by more than the noise band (~57), the bound binds and F stands in for a
missing margin (PI decision: the retirement-income formula or another feature, not a wider bound); if its Q is
above, 0.6 is an interior optimum of the profile, F is reportable with a profile interval (then run F = 0.5 for
the lower end). This is a diagnostic point outside the bound, not a widened bound; `--fix` sets the value directly
and the bound guard applies to free parameters only. Flagged as the PI's call because of the standing "do not just
widen the bound".

**Why now rather than after `final1`.** The profile re-optimises the other parameters, so a start a few Q from the
final point is as good as the final point; waiting costs a day of calendar time at the end, when the result decides
whether a model step follows.

```
cd ~/jointloss && git pull && sbatch --job-name=Joint-F07 --time=10:00:00 paperA_model/hpc_job_a.py polish \
  --label F07 \
  --start $HOME/jointloss/paperA_model/results/runs/polish_hcage2r0_20261023_200316_p800/best.json \
  --noise-file $HOME/jointloss/paperA_model/results/hpc_runs/noise_20261023_160642_j11917862/moment_noise.csv \
  --hc-age on --fix a_bar=25.639 F=0.7 --free-extra beta --tie sigmaJ_B=sigmaJ_W --bound-margin 0 --iters 15 --push
```

## Why the other ideas do not earn a job now

- **Multi-start LM.** The local-optimum check is `Joint-cma-final` (2,400 evaluations around `hcage2r0` with the
  Jacobian's stds). A second LM start (e.g. g_age 0.015, beta 0.95, eta_up 0.55) would answer the same question
  less completely; if the CMA-ES ends near the LM point the question is closed, if not, its best point is the
  second start. Also, a different g_age start needs a new committed start json (`--set-fixed` covers only the
  extras sigma_eps and beta; `--fix g_age=` would hold it), and the `restr` best.json has no g_age (pad_vec gives 0 =
  the lower bound, frozen in logistic units).
- **theta_617 = 0.** Rejected at stage 2 (-0.0187, s.e. 0.0057***). Under the PI's rule (Wald first, LM only where
  it does not settle the question) no LM rerun; the interpretation (school-age children raise participation given
  the childcare price is zero for them) is a paragraph, not a job. A one-point profile with the others held is a
  4-minute PC evaluation after `final1`.
- **Profiles on the HPC.** `estimate.py` has no profile command; `hpc_job_a.py evaluate` runs one evaluation on a
  32-core allocation. Profiles with the other parameters held are PC work; profiles with re-optimisation are LM
  jobs, of which job 3 is the one that decides something.
- **Standard errors / Jacobian.** `polish` writes `se.csv` and `report.md` at its end; `final1` and job 1 cover
  the final point and the comparator. No separate `se` job.
- **Recovery.** `Joint-rec-hcage-b` 11927759 is running; nothing to add until it reports.

## Checks behind the commands

- `--start` and `--noise-file` are full paths into the clone (the snapshot excludes `paperA_model/results`; job
  11917486 failed on a relative path). Both files are committed (00c8a5a, 05e9817); `git pull` before `sbatch`.
- One `--fix` list per command (a second `--fix` would override the first); `--hc-age on` or g_age is reset to 0.
- `--bound-margin 0`: F at 0.6 and pi_c0 near 0 would otherwise refuse the start (free parameters within 1% of a
  bound); fixed parameters are not checked.
- `--tie sigmaJ_B=sigmaJ_W`: sigmaJ_W follows sigmaJ_B and is not free (`free_index`).
- The noise file carries K = 3 (`K` column), the runs' K, so the weights are 1/(se^2 + var_sim) without rescaling.
- Timing from the `hpc_job_a.py` docstring: one LM iteration at 16 workers ~ 5 rounds x ~4 min ~ 20 min; 15
  iterations + final Jacobian + 5 s.e. seeds ~ 6.5 h -> 10 h; 20 iterations ~ 8 h -> 12 h.
- Queue with full names: `squeue -u $USER -o "%.10i %.24j %.8T %.10M %.6D %R"`.
