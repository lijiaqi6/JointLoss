# Paper A hand-over (2026-10-20)

Paper A, "The Insurer Is Hit Too: Joint Job Loss of Spouses and the Limits of Family Insurance", is worked on from
the Windows PC in `G:\My Drive\JointLoss` (this repository; Paper B uses its own working copy `G:\My Drive\IGE-B`).
A new Claude session starts here: read this file, then `proposals/fable_top5_distance_paperA.md`,
`paperA_model/results/INTAKE.md`, `paperA_model/README.md`, `paperA_model/POSTESTIMATION.md`. Layout, paths and the
environment variables are in `README.md`.

## 1. On this PC

- Python: `G:\My Drive\Selection vs risk\.venv\Scripts\python.exe` (Python 3.12, the versions of `requirements.txt`).
- Checks (run 2026-10-20 from this repository): `paperA_model/tests/run_all.py` 13/13 pass;
  `paperA_model/estimate.py evaluate` gives Q 11,733.7 at the analytic start (Stanage 11,733.6).
- Stata 19 (`C:\Program Files\StataNow19\StataMP-64.exe`): the BPS harness (`bps_check.py`, `bps_trim_test.py`,
  `bps_reconciliation/`) runs as before. No Fortran compiler.
- Git-ignored person-level inputs are in place: `paperA_model/inputs/psid_entry_couples.csv`, `_25_30.csv`.
- Data caches through `IGE_DATA` (Windows user variable, `G:\My Drive\IGE_data` since 2026-10-20).
- Exchange with GitHub only: commit on main (no branches), push after every commit, `git fetch` +
  `git merge origin/main` when a push is rejected (HPC jobs push results), never rebase.

## 2. Where Paper A stands

HPC results (in `paperA_model/results/hpc_runs/`), from the old `~/joint` clone of Selection-vs-risk:

- **Joint-recovery-gn 11865966: pass.** Pseudo-data from the analytic start, start perturbed N(0, 0.5) in
  logistic units: 31 of 31 parameters within 2 noise s.e. and 2 data s.e.; Q 23,674 -> 0.67 in 8 LM iterations.
- **Joint-gn-main 11865967: Q 11,734 -> 1,359.6** (10 LM iterations, 4.3 h); fresh seeds 1,355-1,409.
  Condition number (range scaling) 300; no pair above 0.9. Flags: `a_bar` at its upper bound 60 (zero slope);
  `F` 0.10 -> 0.57 (bound 0.6); `sigmaJ_B/W` 0.008/0.005 -> 0.0012/0.0007 (s.e. ~0.003); `d_h` and `pi_dn_w` ~0
  (weakest directions). Search frictions: `lam_w_B` 0.157 -> 0.088, `lam_h_B` 0.26 -> 0.12, `lam_h_W` 0.30.
- **Fable's top-5 review** (`proposals/fable_top5_distance_paperA.md`): the estimate is not reportable. The base
  hazards carry 92% of the weight, so the earnings loss, consumption, wealth and separation blocks misfit. Its plan,
  item 1: re-estimate with block-balanced weights, F fixed, sigmaJ pooled, a data-based borrowing limit, three
  workplace groups. Also needed: annual EITC timing in the model, and the counterfactuals (marginal-preserving
  decorrelation; EITC against an unconditional transfer at equal cost).
- **Checked 2026-10-20** (`paperA_model/results/reestimate_plan_20261020.md`): EITC paid monthly, confirmed;
  counterfactual (i) cuts each spouse's hazard by 24-26% (23 points from m_H = 1), confirmed. But Fable's "92% of
  the weight" is a units artifact (raw 1/se^2 summed across units): in z^2 terms base hazards are 3% of Q, wealth
  57%. The note holds the step plan (0-6), approved by the PI, and its progress (section 4b): steps 0-1 done (block
  weights fixed, decorrelation hooks), step 2 inputs and baseline done (BPS correction applied; EXPECTED_Q 11,866.0);
  next Joint-gn-bps.
- **Not yet done: the intake** (`paperA_model/results/INTAKE.md`): fit table and Q by block at the estimate,
  marriage diagnostics; the clean-spec BPS correction (sig_nu_h 0.166 -> 0.180, sig_nu_w 0.112 -> 0.134), baseline
  rerun and LM again.

- **Event-study figures (2026-10-21 night, PI request; Fable's advice in
  `proposals/fable_event_study_figures_paperA.md`):** all six added to the paper (66 pages, compiles): SIPP household
  month by month (5.8), the wife's monthly response (5.2), AWE and joint loss by age (4), still together after his /
  her / joint loss (5.6), the wife's displacement and the family (new 5.5), wealth around his displacement (Appendix B
  + paragraph in 5.7 'Consumption and wealth'). EVIDENCE 3.100-3.103. Fable's redesigns of the existing figures
  (cut father_displacement_es to four panels, joint_job_loss_es pooled, gross_net hours only) are NOT done: PI to decide.
  The step-3 LM chain is paused (sigJ, abar, lamh to rerun; fixF rejected, F free).

Proposed next step (PI to confirm): verify Fable's two claims (reading code only), then design the re-estimate,
one change at a time on one moment set, with the HPC commands for the PI.

PI decisions waiting: separated-wife inputs (child support, remarriage; script 76); an exit feature for established wives (transitory work-cost state + birth jump; 75);
`--her-sep`; the BPS correction. `--new-job`: likely not.

PI decision 2026-10-23: the wealth targets stay liquid (net worth excl. home and vehicles misfits the shares above
one year's earnings badly: data 0.12 / 0.24 / 0.40 vs model 0.02 / 0.06 / 0.15); it is reported untargeted.

Paper: `paperA_joint_loss/`. EITC wording: it pays nothing in the MONTHS without an earner; over the year the credit
rises by $196*** after a joint loss. Charles and Stephens (2004) already show that either spouse's job loss raises
divorce; the new claim is the joint loss (9.5 vs 4.1 points, p = 0.15). An unrequested Fable review of the
introduction (2026-10-20, not acted on): better framing than the previous version, but 2,463 words with repetition
(ten times x5, the BPS material in four paragraphs) and the two claims above stated more strongly than Section 5;
it proposed 7-8 paragraphs, 1,400-1,600 words. Act only if the PI asks.

## 3. HPC: a new clone `~/jointloss`

The old `~/joint` is a clone of Selection-vs-risk: retire it (keep its results folder). `hpc_job_a.py` now expects
`~/jointloss` and pushes results to JointLoss. GitHub deploy keys belong to one repository, so Stanage needs a new
key for JointLoss (steps in the `hpc_job_a.py` docstring: ssh-keygen, add the .pub as a write deploy key, a `Host
github-jointloss` entry in `~/.ssh/config`; the same key serves Paper B's `~/ige`). The PI runs these on Stanage
(password + Duo). Then scp the entry couples to `~/jointloss/paperA_model/inputs/` and run the 90-minute `Joint-test`
before any estimation job.

## 4. Further tasks

1. **Bacher, Grubener and Nord (2025, JME), check 1: the CPS added-worker effect.** Their package:
   github.com/philippgruebener/JSLC_ReplicationFiles (GPL-3.0), stored in `Dropbox/ReplicationPapers/Bacher2025/`
   (not in this repo). Run their Stata CPS code on their sample and line it up with `50.CPSAddedWorkerByAge.py`
   (5.64 vs their 5.55; by age 6.4/7.2 -> 1.2 at 56-62), including their Elsby, Hobijn and Sahin (2015) U/N
   classification-error correction. Pass mark: their published Tables 1-2 (AWE 5.55; 7.12 at 26-35, 1.40 at
   56-65). Then the joint loss by age with and without the correction.
2. **Bacher check 2: nesting (Fortran; needs a compiler installed first, PI's decision).** Run their model
   (`Main.f90`/`Globals.f90`, OpenMP) at their calibration; set Paper A's model to their special case (correlation
   off: `pi_c*` = 0, p_H = 0; no children; UI only; no separation; their parameters) and compare moments: a table
   showing Paper A's model nests theirs, with the remaining departures. Background:
   `proposals/fable_bacher2025_paperA.md`.

Write results to `output/` (aggregates only) and a note in `paperA_model/results/`, add `EVIDENCE.md` rows, and a
footnote in the model section (rule: every data-backed modelling choice gets a footnote with numbers and script).

## 5. Rules (the PI's standing instructions; also in the Claude memory of this folder)

- Commit each change at once; never create branches; fetch + merge, never rebase; commit messages end with
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- Never commit person-level microdata (PSID/NLSY/CPS/SIPP rows); aggregates only. Never write API key values
  (CENSUS_API_KEY / IPUMS_API_KEY are env vars). No US restricted data (FSRDC, SIPP-SSA, IRS/LEHD).
- Raw data in Dropbox are read only; no new top-level Dropbox folders (replication packages go in
  `Dropbox/ReplicationPapers/<AuthorYear>/`).
- Joint estimation: every endogenous parameter from one coded SMM run, no hand tuning; one step at a time on one
  moment set; parsimony (drop what the data cannot separate).
- HPC (Stanage): Paper A runs only in `~/jointloss`; 32 cores, `--threads 2`, 64G unless measured otherwise, never 64
  cores without asking; job names start `Joint-`; `--mail-type=BEGIN,END,FAIL --mail-user=jiaqi.li@sheffield.ac.uk`;
  the PI submits (password + Duo); do not poll running jobs; give the squeue command with full job names.
- Every regression estimate shown to the PI carries *** / ** / * and its p-value; tables: one regression per column.
- Words: "search friction" (never "offer rate"); "human capital level / accumulation / depreciation" (never "rung",
  "ladder", "promotion"). Never call a precisely estimated share "small". No self-citations of older project versions.
- No sibling comparisons; no over-restrictive balanced panels; no region x year FE in policy designs.
- Writing: conclusion first in every paragraph; empirical sections say what the model needs; LaTeX patches with the
  Edit tool or Python raw strings, never shell heredocs; compile before committing.
- "Check / examine" requests: read code only, run nothing unless asked. Explain identification arguments in full.
- "Ask Fable" = spawn an agent with model `fable`.
