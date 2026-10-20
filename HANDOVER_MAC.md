# Paper A hand-over: Windows PC -> MacBook, Selection-vs-risk -> JointLoss (2026-10-20)

Paper A ("The Insurer Is Hit Too: Joint Job Loss of Spouses and the Limits of Family Insurance") now has its own
private repository, github.com/lijiaqi6/JointLoss, and moves to the PI's MacBook. Paper 1 and Paper B stay in
Selection-vs-risk on the Windows PC. The Claude session on the Mac starts cold: read this file, then `README.md`,
`paperA_model/results/INTAKE.md`, `paperA_model/README.md`, `paperA_model/POSTESTIMATION.md`.

## 1. Set up the Mac (once)

**Clone into a folder that Google Drive does not sync.** The PC keeps a working copy in `G:\My Drive\JointLoss`,
which Google Drive also shows on the Mac. Never run git in that synced copy from the Mac: two machines writing one
synced `.git` corrupt it.

```sh
git clone https://github.com/lijiaqi6/JointLoss.git ~/JointLoss
cd ~/JointLoss
git config user.name "Jiaqi Li (Mac)"
python3.12 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

**Environment** (add to `~/.zshrc`; the Google Drive account folder name differs per machine):

```sh
export DROPBOX="$HOME/Library/CloudStorage/Dropbox"            # or ~/Dropbox, wherever Dropbox syncs
export JOINTLOSS_DATA="$HOME/Library/CloudStorage/GoogleDrive-<account>/My Drive/Selection vs risk/IGE/data"
```

`JOINTLOSS_DATA` is the PC's person-level cache folder seen through Google Drive (6.7 GB; files stream on demand).
The data scripts read it and also write new caches into it.

**Git-ignored model inputs** (person-level; never commit): copy
`paperA_model/inputs/psid_entry_couples.csv` and `psid_entry_couples_25_30.csv` from
`.../My Drive/JointLoss/paperA_model/inputs/` (the PC copy, synced) into `~/JointLoss/paperA_model/inputs/`.

**Check:**

```sh
.venv/bin/python paperA_model/tests/run_all.py      # 13/13 pass on the PC
.venv/bin/python paperA_model/estimate.py evaluate   # Q at the analytic start 11,733.7 on the PC and Stanage
```

On Apple silicon numba compiles for a different CPU, so a small difference in Q (well under 1) is expected; a
larger one means an input file is missing or differs (compare `inputs/` with the PC). Record the Mac value.

**Exchange with the PC and the HPC only through GitHub:** commit on main (no branches), push after every commit,
`git fetch origin && git merge origin/main` when a push is rejected (HPC jobs push results), never rebase.

## 2. Where Paper A stands

HPC results (in `paperA_model/results/hpc_runs/`), from the old `~/joint` clone of Selection-vs-risk:

- **Joint-recovery-gn 11865966: pass.** Pseudo-data from the analytic start, start perturbed N(0, 0.5) in
  logistic units: 31 of 31 parameters within 2 noise s.e. and 2 data s.e.; Q 23,674 -> 0.67 in 8 LM iterations.
- **Joint-gn-main 11865967: Q 11,734 -> 1,359.6** (10 LM iterations, 4.3 h); fresh seeds 1,355-1,409.
  Condition number (range scaling) 300; no pair above 0.9. Flags: `a_bar` at its upper bound 60 (zero slope);
  `F` 0.10 -> 0.57 (bound 0.6); `sigmaJ_B/W` 0.008/0.005 -> 0.0012/0.0007 (s.e. ~0.003); `d_h` and `pi_dn_w` ~0
  (weakest directions). Search frictions: `lam_w_B` 0.157 -> 0.088, `lam_h_B` 0.26 -> 0.12, `lam_h_W` 0.30.
- **Not yet done: the intake** (`paperA_model/results/INTAKE.md`): fit table and Q by block at the estimate,
  marriage diagnostics; the clean-spec BPS correction (sig_nu_h 0.166 -> 0.180, sig_nu_w 0.112 -> 0.134; an input
  change, no Stata needed), baseline rerun and LM again; then the Joint-noise and 3-seed Joint-smm-main commands for
  the PI.

PI decisions waiting until after the intake: separated-wife inputs (child support, remarriage; script 76); wealth
targets to net worth without home and vehicles (77); an exit feature for established wives (transitory work-cost
state + birth jump; 75); `--her-sep`; the BPS correction. `--new-job`: likely not.

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
github-jointloss` entry in `~/.ssh/config`). The PI runs these on Stanage (password + Duo). Then scp the entry
couples to `~/jointloss/paperA_model/inputs/` and run the 90-minute `Joint-test` before any estimation job.

## 4. Next tasks, all in Python (the Mac has no Stata; it has gfortran)

Decision 2026-10-20: no Stata dependence. Stata is used once more, on the PC, only to validate the Python ports.

1. **Bacher, Grubener and Nord (2025, JME), check 1: the CPS added-worker effect.** Their package:
   github.com/philippgruebener/JSLC_ReplicationFiles (GPL-3.0), stored in `Dropbox/ReplicationPapers/Bacher2025/`
   (not in this repo). Read their Stata CPS code and extend `50.CPSAddedWorkerByAge.py` (which already gives 5.64 vs
   their 5.55; by age 6.4/7.2 -> 1.2 at 56-62) with their sample rules and the Elsby, Hobijn and Sahin (2015) U/N
   classification-error correction. Pass mark: their published Tables 1-2 (AWE 5.55; 7.12 at 26-35, 1.40 at 56-65).
   Then the joint loss by age with and without the correction.
2. **Bacher check 2: nesting (Fortran, on the Mac).** Run their model (`Main.f90`/`Globals.f90`, OpenMP) at their
   calibration; set Paper A's model to their special case (correlation off: `pi_c*` = 0, p_H = 0; no children; UI
   only; no separation; their parameters) and compare moments. Goal: a table showing Paper A's model nests theirs,
   with the remaining departures. Background: `proposals/fable_bacher2025_paperA.md`.
3. **Port the BPS harness to Python.** `bps_check.py` / `bps_trim_test.py` call BPS's Stata/Mata code
   (`bps_reconciliation/code/`: `residual_measures.do` 271 lines, `variance_estimation.do` 644, `pi_s_estimation.do`
   345; ~1,400 lines with helpers). Write a Python version of the estimator, then validate: (a) on BPS's own panel
   (shipped in `Dropbox/ReplicationPapers/Consumption Inequality and Family Labor Supply/`) it must reproduce their
   Table 3 and the 63/20/17 insurance split to the third decimal; (b) on one simulated panel it must match the
   Stata output. (b) and the Stata side of (a) run on the PC (Stata 19 there): hand the PC session the exact
   commands. After that, Stata is not needed. The paper's statement that BPS's code reproduces their estimates
   exactly was made with their Stata code and stays true.

Write results to `output/` (aggregates only) and a note in `paperA_model/results/`, add `EVIDENCE.md` rows, and a
footnote in the model section (rule: every data-backed modelling choice gets a footnote with numbers and script).

## 5. Rules (the PI's standing instructions; a copy of the PC's Claude memory is in `G:\My Drive\claude_memory_export`)

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
