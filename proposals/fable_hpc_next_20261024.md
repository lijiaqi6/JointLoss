# Which Stanage jobs are worth submitting tonight (Fable, 2026-10-24, evening)

Read-only assessment from the code (`estimate.py`, `post_common.py`, `counterfactuals.py`, `hpc_job_a.py`, `params.py`),
the Ffree and F07 run folders (job logs, iterations.csv, evals.csv.gz, report.md, se.csv, q_by_seed.csv, run.json), the
noise run 11917862 and the cf-smoke results. Nothing was run or edited except this file.

## Verdict

The Ffree point is a genuine LM optimum, not a stall: F = 0.700 sits at the minimum of its own 1-D profile to
within 0.005, the Jacobian is well conditioned and no free parameter is frozen at a bound. Report F = 0.70 (0.045). Two
jobs are worth submitting now, one is cheap and optional, nothing else:

| rank | job | question | cores x wall | result that changes the plan |
|---|---|---|---|---|
| 1 | `Joint-cf-F` (as specified, plus `--K 9`) | headline counterfactuals at the final point | 8 x ~0.5 h | the decorrelation / UI / race numbers at Q 616 differ from the smoke test at Q 810 |
| 2 | `Joint-F06` (PI's call) | the clean profile value at F = 0.6 with a well-conditioned LM: how much of the 225 (841 -> 616) is F and how much is the frozen-F conditioning | 32 x ~6 h | Q(0.6) near 616 = F weakly identified, the week's gain was the conditioning fix; Q(0.6) far above = the bound bound |
| 3 | `Joint-noise-F --reps 16` (optional, cheap) | simulation weights at the new point with 16 seeds instead of 5; report only, adopt at the final re-baseline | 32 x 0.3 h | weights move materially on moments with Q share -> re-baseline once, at the end |

Not now: a second CMA seed (wait for 11928515), any LM with theta_05 = 0 or sigmaJ = 0 (Wald says both are zero-
compatible; impose them in the one final LM after the CMA-ES, not tonight), a range-step `se` job (footnote-level
robustness; 32 x 0.6 h, can wait for the final point), profiles with the others held (PC), `--size full` (pi_c2 enters
at an unestimated value).

## 1. Is the Ffree point trustworthy?

**Yes, as the LM optimum of this objective; the exact 0.700 is inherited from F07 but it is also where the 1-D profile
bottoms out.** The Ffree Jacobian evaluated every parameter at +-h with the others held (evals 3-62 of
`polish_Ffree_20261024_203146_j11928459/evals.csv.gz`). Every one of the 62 perturbations raises Q except two inside the
chatter (m_H +5%: -1.0; lam_h_W +5%: -0.3). For F: Q(0.665) = 663.8, Q(0.700) = 615.6, Q(0.735) = 641.9; the parabola
through the three points has its vertex at F = 0.705. So F = 0.70 is the 1-D minimum to 0.005, and the sandwich s.e.
0.045 (of which 0.025 is simulation noise at K = 3) is the honest precision. The Wald test of F = 0.6 gives z = 2.2
(p = 0.03)**.

**Why the LM took no step.** The Gauss-Newton trial (eval 65) moved F to 0.758, m_H to 27.2, sigmaJ to 0.0069 and
lam_w_B to 0.168 and Q rose to 688: the quadratic model (cond 3.1e5) is wrong at that distance. Damped trials
(F 0.743 -> 630; 0.712 -> 617.4; 0.7015 -> 617.2) and tiny ones (1-3% moves of all parameters, eval 71: +2.4; 1e-7
moves, evals 77-85: +0.01 to +0.03) all raise Q. The objective is smooth at the 1e-7 scale (+0.03) and chatters by
~2 at 1-3% moves; the "no descent" stop is the accept-if-lower rule at a point where the gradient is already inside
that chatter. F07 itself stopped at iteration 12 with an accepted step of 1.2e-7 in z (Q -0.01), i.e. converged. This is
not the frozen-at-bound stall of the week: F at 0.35 of its range has dtheta/dz = 0.455 (at 0.6 of [0, 0.6] it was
~1e-6), and cond(G'WG) is 3.1e5 against 2e10 before.

**Bounds now.** Within 3% of a bound: pi_c0 (1.9% of its range; z = -4.0), pi_dn_w (1.1%; z = -4.5), sigmaJ_B (0.9%;
z = -4.7), p_H (2.7%; z = -3.6). In logistic units these move at ~theta per unit z (dtheta/dz = range x u(1-u) ~ theta),
so steps in them are compressed by 10-50x relative to range scaling but not frozen: their per-z column norms are 6.6,
23.6, 1.07 and 12.3 (report.md), and pi_dn_w is the most curved coordinate of all (+-0.002 moves Q by +350 / +625).
sigmaJ is the one weak column (smallest singular value 0.048, loading 0.99): Q(sigmaJ = 0) = 615.7, i.e. +0.1. It is
not identified away from zero at this point (0.00094, s.e. 0.0019). theta_05 is the second weakest (-0.0079, s.e.
0.011; +10 at +-0.015). Both are parsimony candidates under the PI's rule (Wald, not LM reruns); they should be imposed
in the one final LM after the CMA-ES verdict, together, on this moment set. theta_617 -0.033 (0.006)*** (z -5.5), d_h
0.095 (0.039)** (z 2.4), pi_dn_h 0.0157 (0.0072)** (z 2.2), eta_up 0.82 (0.21)*** and g_age 0.021 (0.003)*** stand.
Near-collinear pairs: none. beta: both Jacobian points (+-0.00042 a month = +-0.5% a year) raise Q by 76-102: beta
is pinned by the wealth block (69% of its information), s.e. 0.00012 a month.

**What does worry me: the 225.** The log reads "final1 841.14 at F = 0.6 vs F07 615.59: THE BOUND BINDS". final1 was
an LM crawling at cond 2e10 and mu 10-1,000 with F frozen; it is not the profile value at 0.6. The Wald z of 2.2 is
consistent with a profile difference of order 5-20 at the quadratic approximation, not 225. Either the re-optimised
profile at F = 0.6 is far above 616 (the bound truly bound and the quadratic approximation is poor over 0.1) or it is
close to 616 (the week's gain, including d_w 0.026 -> 0.25 and d_h 0.004 -> 0.095, came from the LM finally being
well conditioned, and F is a detail). The paper has to say which; job 2 answers it. Pending: the CMA-ES 11928515 is the
local-optimum check (sigma0 0.2 x Jacobian stds explores F around 0.7); nothing more is needed on that front.

Noise band for reading Q: across the 5 s.e. seeds Q is 612 / 628 / 656 / 615 / 714 (sd 41, 6.6% of Q; 2.2% at hcage1b),
so Q differences between runs on different draws below ~50 are not meaningful; under common draws the chatter is ~2.

## 2. Is `Joint-cf-F` right as specified?

**Yes.** `counterfactuals.py --start <run folder>` -> `post_common.setup` resolves `best.json`, reads `run.json` and
passes: `--size` (k_s2_era1_a20, also given explicitly), `--seed 20261018`, every extension flag from `run["ext"]`
(`--hc-age on`, `--borrow-wedge on`, `--hc-eta on`, `--cps-persist on`, the rest off), `--weighting diag_noise`, the
run's noise file (`noise_file_arg` is the full Stanage path and exists in the clone, so no fallback note), the extra
exclusions. `estimate.start_theta` then takes from `best.json` every name it knows: F 0.7, a_bar 25.639 (so `--fix` is
not needed), beta 0.994446 (an extra carried by the json wins over the fixed input; `start_theta` lines 431-436),
g_age 0.0211 (kept because hc_age is on; line 440-442), sigmaJ_W = sigmaJ_B 0.00094 (the tie is already in the json).
The smoke test confirms the path: `counterfactuals_20261024_133535_j11927826/counterfactuals.json` records beta
0.99486, g_age 0.0287, F 0.5999, a_bar 25.639 = hcage2r0's values. The weights do not enter the scores.

Two additions, both free:
- `--K 9`. The log flags that the i_indep joint-loss consumption numbers rest on 26 / 22 events (not readable). K = 9
  triples the copies (joint losses ~80 / 65), with the same draws across scenarios. Solve time is unchanged; the
  simulation and scoring triple (+~1 min per scenario): ~25-30 min in all. Memory ~10 GB: `--mem 24G`.
- Drop `v_sep` and `v_haz_sep` with `--scenarios` or leave them (they equal base / v_haz by construction, 3 minutes).
  `--indep <Joint-indep-F run folder>` later, when 11928460 lands: the script then runs both models (~1 h at K 9).

```
cd ~/jointloss && git pull && sbatch --job-name=Joint-cf-F --time=02:00:00 --cpus-per-task=8 --mem=24G \
  --output=joint_%x_%j.log --mail-type=BEGIN,END,FAIL --mail-user=jiaqi.li@sheffield.ac.uk \
  --wrap="cd \$HOME/jointloss && NUMBA_CACHE_DIR=\$TMPDIR/numba_cf OMP_NUM_THREADS=1 .venv/bin/python -u paperA_model/counterfactuals.py \
  --start \$HOME/jointloss/paperA_model/results/hpc_runs/polish_Ffree_20261024_203146_j11928459 \
  --size k_s2_era1_a20 --K 9 --threads 8"
```

Live clone, so no `git pull` on Stanage while it runs (it imports within the first minute; the risk is small). Output
`~/jointloss/paperA_model/results/counterfactuals_<stamp>_j<job>/` (scores.csv, .md, .json; aggregate only): commit and
push from the login node. If 11928516 was already submitted with these arguments at K 3, keep it and add only a K 9
rerun with `--indep` later.

## 3. Recompute the simulation-noise weights?

**Report only, not an objective change tonight.** The weights in use (`noise_20261023_160642_j11917862`) are the
simulation sd of each moment over 5 seeds at hcage1b_it9 (Q ~850, F at 0.6, d_w 0.026). At the Ffree point d_w is 0.25,
m_H 21.7 and the across-seed spread of Q is 6.6% against 2.2%, so var_sim has moved for some moments (re-employment
losses, joint-loss counts). Adopting a new file is a new objective: every Q this week (F07/Ffree 615.6, Joint-indep-F,
Joint-rec-F, Joint-cma-F) is on the current weights, and the comparator and recovery would have to be redone. Do that
once, at the final re-baseline (the final LM from the CMA/Ffree best with the parsimony restrictions), not in the
middle of three running jobs.

Two routes to the report:
- **PC, no job.** `polish_Ffree_.../moments_by_seed.npy` already holds the 5-seed moments at the Ffree point (seeds
  20262018-22, K 3; `se_block`, estimate.py 882-897). `sim_sd = S.std(0, ddof=1)` against the file's `sim_sd`, weight
  ratio `(se^2 + sd_old^2) / (se^2 + sd_new^2)` per moment, flag ratios outside [0.5, 2] on moments with Q share. Five
  minutes of numpy; a `noise` job with 5 seeds would duplicate it.
- **HPC, if the final weights should be less noisy.** A 5-seed sd has a ~35% sampling error (4 df); 16 seeds halve it.
  One round of 15 workers plus the warm-up: ~15 min. The warm-up seed is the run's seed, so the job also reproduces
  Q 615.59 (a free reproducibility check under the current weights).

```
cd ~/jointloss && git pull && sbatch --job-name=Joint-noise-F --time=00:45:00 paperA_model/hpc_job_a.py noise \
  --start $HOME/jointloss/paperA_model/results/hpc_runs/polish_Ffree_20261024_203146_j11928459/best.json \
  --noise-file $HOME/jointloss/paperA_model/results/hpc_runs/noise_20261023_160642_j11917862/moment_noise.csv \
  --hc-age on --fix a_bar=25.639 --reps 16 --push
```

(`cmd_noise` caps workers at reps - 1 = 15; seeds 20261018-33; `--save-noise-input` deliberately absent, so
`inputs/moment_noise.csv` is untouched.) Decision rule when the report is in: adopt at the final re-baseline if any
moment carrying more than 2% of Q changes weight by more than 2x; otherwise keep the current file and cite the check.

## 4. Other jobs worth submitting now

**`Joint-F06`: the re-optimised profile at F = 0.6 (the PI's call).** This is not a restriction test (the Wald settles
F = 0.6 at p = 0.03), it is the number the log already quotes: "the bound binds by 225". That figure compares a converged
run with a non-converged one. With F fixed at 0.6 the LM is well conditioned (F07 ran at cond 1e5-1e8, mu 0.001-1), so
one run from the Ffree best gives the true profile value. If Q(0.6) is 620-660, F is weakly identified and the paper
should say the LM, not F, produced this week's estimates (d_w, d_h, the lam_w gap 0.077 -> 0.046); if it is 750+, the
bound bound and F = 0.6 was a mis-specification worth a sentence. Start close, so ~6-10 iterations (F07 needed 12 from
hcage2r0, 285 min).

```
cd ~/jointloss && git pull && sbatch --job-name=Joint-F06 --time=08:00:00 paperA_model/hpc_job_a.py polish \
  --label F06 \
  --start $HOME/jointloss/paperA_model/results/hpc_runs/polish_Ffree_20261024_203146_j11928459/best.json \
  --noise-file $HOME/jointloss/paperA_model/results/hpc_runs/noise_20261023_160642_j11917862/moment_noise.csv \
  --hc-age on --fix a_bar=25.639 F=0.6 --free-extra beta --tie sigmaJ_B=sigmaJ_W --bound-margin 0 --iters 15 --push
```

Cost 32 x ~6 h. Independent of the three running jobs (same objective, same draws, own optimum). Compare its Q with
615.59 under common draws (chatter ~2; a difference below ~10 is "equal").

**Optional, can wait: `Joint-se-range`.** The sandwich s.e. and the Wald stars rest on the 5%-of-value central
differences; `--step range` (5% of the bound range) gives a second Jacobian in 5 rounds (~35 min, 32 x 0.6 h). It would
mainly move sigmaJ and theta_05 (where the value step is at the range floor) and worsen pi_dn_w (a range step spans its
very curved profile). A footnote, so run it at the final point, not tonight:

```
cd ~/jointloss && git pull && sbatch --job-name=Joint-se-range --time=01:30:00 paperA_model/hpc_job_a.py se \
  --start $HOME/jointloss/paperA_model/results/hpc_runs/polish_Ffree_20261024_203146_j11928459/best.json \
  --noise-file $HOME/jointloss/paperA_model/results/hpc_runs/noise_20261023_160642_j11917862/moment_noise.csv \
  --hc-age on --fix a_bar=25.639 --free-extra beta --tie sigmaJ_B=sigmaJ_W --bound-margin 0 --step range --push
```

**Not worth a job now, and why.**
- Second CMA seed: 32 x 16 h of fair share for a confirmatory answer; if 11928515 ends at the Ffree point the question
  is closed, if it finds a lower Q its best is the next LM start and a second seed is moot.
- theta_05 = 0 / sigmaJ = 0: Wald says zero-compatible (z -0.7, 0.5); under the parsimony rule they go into the one
  final LM (from the CMA/Ffree best, same weights or the re-baselined ones), one run, after the CMA-ES. Tonight it
  would be a second final run to redo later.
- Profiles with the others held (ss_rate, theta_617, F finer grid): single evaluations, PC work; the Jacobian evals
  above already give the +-5% cuts for all 31 parameters.
- `--size full` counterfactuals: pi_c2 (s = 2 group) was never estimated (merged); a 3-era, merged-s size does not exist
  in `params.SIZES`. The era question is a code change on the PC, not a job.
- Recovery variants (smaller start noise, more iterations): wait for Joint-rec-F 11928461; its truth has F interior,
  so it isolates the conditioning explanation of the two failures.

## PC work that falls out of this (no HPC)

1. The weight comparison from `moments_by_seed.npy` (Section 3).
2. `fit_table.py` at the Ffree run folder (one evaluation) for the paper's fit table; the indep column when 11928460 lands.
3. The Wald table at Ffree for the paper: F = 0.6 (z 2.2**), theta_05 = 0 (n.s.), sigmaJ = 0 (n.s.), theta_617 = 0
   (z -5.5***), eta_up = 0 (z 3.9***), g_age = 0 (z 7.0***), lam_w_B = lam_w_W (gap 0.046, p ~0.04**), lam_h_B = lam_h_W
   (gap 0.184***); the last two need the covariance from `se_inputs.npz` (G, Vsim, Vdat are saved).
4. Log entry: replace "the bound binds: 225 lower" by the Wald statement until Joint-F06 reports.
