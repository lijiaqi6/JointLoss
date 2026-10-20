# Intake checklist: when the first HPC runs land

First submission 2026-10-19 ~09:05 from `~/joint` at commit 6adfd1a: Joint-test 11863423 timed out at 45 min in its LM step
(all earlier checks passed: Q 11,733.6 vs PC 11,726.0; CMA 3 generations; resume), so 11863424 / 11863425 never
started (cancelled). Resubmitted without the test with --time 10:00:00 (Stanage: ~4 min per round of 16 evaluations). Run folders are under
`/mnt/parscratch/users/cm1jil/joint_smm_results/runs/`. `--push` copies the aggregate files to
`IGE/paperA_model/results/hpc_runs/<run>/`, so a `git pull` on the PC brings them in. The test job pushes nothing.

## 1. Joint-recovery-gn (folder `recovery_gn_*`): the identification verdict

Read `recovery_report.md` / `recovery_table.py` (WP3) and the final Jacobian `report.md`.

- How many of the 31 parameters are within 2 noise s.e. of the truth, and how many within 2 data s.e.? The yardstick
  is the earlier CMA run: 3 / 19 and 8 / 19 at a 480-evaluation budget.
- Final Q against 0 at the truth. A Q far above the noise band means an optimizer failure. A low Q with parameters
  off means a flat direction.
- The weakest directions in `report.md`. Expected from the start Jacobian: sigmaJ_B/W, pi_dn_h with d_h,
  lam_h_B vs lam_h_W, F, kappa_S, a_bar. A parameter that fails here is a parsimony candidate (tie or fix) before
  CMA-ES; that is a PI decision, with the evidence.

## 2. Joint-gn-main (folder `polish_*`): the first estimate

- Q by block against the start (11,726 over 85 moments). Main blocks: her exits (persistent exit 0.0014 vs 0.0101),
  employment levels (3,537), wealth (2,702).
- Parameters at a bound (logistic z beyond about 4.6). The sandwich `se.csv` and its condition number.
- Fable's marriage diagnostics at the estimate (`diagnostics_marriage.py`, WP3): Q and moments with separation
  switched off; the simulated still-with-wife path in event years 1-6 against PSID years 4-6.
- Fit table (`fit_table.py`, WP3) for the paper.

## 2b. BPS wage-process correction (PI decision 2026-10-19: apply before the CMA-ES stage)

The first check found BPS's estimator recovering only 0.006-0.013 of the husband's transitory variance against an
input of 0.0275 (results/bps_20261019_133727, bps_20261019_134505). WP1 (results/bps_deficit_20261020.md, 2026-10-20)
shows that 0.018 of that deficit is the harness: the husband's simulated hours vary too little, so its
measurement-error layer cannot draw the wage error BPS's correction subtracts. On the clean spec (no errors in the
data, BPS's correction off, trims on), BPS recover 0.0226 (him) and 0.0070 (her) against 0.0275 / 0.0125. The real
offset (-0.005 for both spouses) is annual averaging of discrete human capital steps plus the trims. So the PI's
decision (apply the correction) stands, computed on the clean spec. At the start values that gives sig_nu_h
0.166 -> 0.180 and sig_nu_w 0.112 -> 0.134 (p_eps_h x1.13, p_eps_w x1.10, p_c x1.13), not 0.20-0.22, which would
raise his transitory variance by 52-77% and lower hers. After Joint-gn-main reports:

1. Run `bps_trim_test.py --start <gn> --K 3 --only F_none_shipped` (clean spec, about 8 min), and `bps_check.py
   --start <gn> --K 3` for the shipped-spec table.
2. Apply bps_check's rule to the clean-spec numbers. This needs a `--clean` option in `bps_check.py --apply`, or a
   wage_process.json entered from spec F; code it only after the chain allows input changes. Fix the error layer (draw
   his wage error at the target) before using it again for any Table 3 number. Commit the new inputs.
3. Rerun the baseline on the new inputs: `estimate.py evaluate` at the analytic start and at the gn best.json. This
   gives a new EXPECTED_Q and expected_start_moments.csv.
4. LM on the corrected inputs (Joint-gn-main-bps, from the gn best.json). Compare its estimates and fit with
   Joint-gn-main.
5. Then Joint-noise and CMA-ES from the preferred one.

## 3. Next submissions (the PI submits; from `~/joint` after `git pull --ff-only`)

Set `GN` to the Joint-gn-main run folder name, e.g. `GN=/mnt/parscratch/users/$USER/joint_smm_results/runs/polish_main_<stamp>_j11863425`.

```bash
cd ~/joint && git pull --ff-only
N=$(sbatch --parsable --job-name=Joint-noise --time=00:30:00 IGE/paperA_model/hpc_job_a.py noise --start $GN/best.json --reps 5 --weighting diag --push)
# after Joint-noise ends: NF = its folder's moment_noise.csv
NF=/mnt/parscratch/users/$USER/joint_smm_results/noise_<stamp>_j$N/moment_noise.csv
for s in 1 2 3; do
  L=main; [ $s -gt 1 ] && L=main_s$s
  J=Joint-smm-main; [ $s -gt 1 ] && J=Joint-smm-main-s$s
  sbatch --job-name=$J --time=12:00:00 IGE/paperA_model/hpc_job_a.py run --label $L --start $GN/best.json \
         --cma-stds-from $GN/jacobian.npz --sigma0 0.2 --maxfevals 3500 --tolfun 30 --cma-seed $s --noise-file $NF --push
done
squeue -u $USER -o "%.10i %.25j %.8T %.10M %R"
```

Restricted independent-shock model (same targets and draws), LM first:
`sbatch --job-name=Joint-gn-indep --time=05:00:00 IGE/paperA_model/hpc_job_a.py polish --label indep --fix pi_c0=0 pi_c1=0 pi_c2=0 m_H=1 --push`

All jobs: 32 cores, `--threads 2`, 64G, email at BEGIN/END/FAIL (script header). Never 64 cores without asking.

## 4. Rules

- One step at a time: code a step, run it, then add the next. A new moment set means re-running the baseline on it
  first, and specifications are compared only on one moment set.
- Do not change the model's economics, the objective or `inputs/` while a chain (LM -> noise -> CMA-ES) is running.
  Later jobs must be consistent with the LM run.
- Compare Q only on common draws (the same CRN seed and K).
