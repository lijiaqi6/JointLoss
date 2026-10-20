# Paper A model: post-estimation tooling (WP3, 2026-10-19)

New scripts only; nothing on the estimation code path (`model, solve, simulate, panels, moments, params, estimate,
analytic_start, borrowing_wedge, hpc_job_a`, `inputs/`, `tests/`) was changed, and none of them writes into `inputs/`.
Every script takes `--start <best.json | run folder>` (default: the analytic start, exactly as `estimate.py evaluate`),
writes to `results/<name>_<stamp>/` and writes aggregate numbers only. Run from the repository root with
`.venv/Scripts/python.exe` (PC) or `.venv/bin/python` (Stanage, `cd ~/joint`).

`post_common.py` is the shared layer: `setup()` reproduces `estimate.py evaluate --start <start>` in-process
(`estimate._init_worker`, `start_theta`); when `<start>` sits in a run folder, the run's extensions, `--set-fixed`
entries, weighting, extra `--drop` ids, size and CRN seed are read from its `run.json` (a noise file with an HPC path
that does not exist locally falls back to `inputs/moment_noise.csv`, noted in the output). `evaluate()` is
`estimate.model_moments` with `model.Model` test overrides passed to `simulate()`. Check: at the analytic start it
returns Q = 11,726.0, the `hpc_job_a.EXPECTED_Q`.

## When `results/hpc_runs/<run>/` arrives

Polish (LM) folders hold `best.json` (theta + moments), `run.json`, `se.csv`, `report.md`, `iterations.csv`,
`jacobian.npz`, `evals.csv.gz`, and for `--pseudo` `recovery_report.md/.csv`. Below `<gn>` = the `Joint-gn-main`
folder, `<ind>` = `Joint-gn-indep`, `<rec>` = `Joint-recovery-gn`, `<cma>` = the best of the `Joint-smm-main*` runs.

| Step | Command | Output |
|---|---|---|
| fit, Q by block, parameters | `python paperA_model/fit_table.py results/hpc_runs/<gn> --indep results/hpc_runs/<ind> --params results/hpc_runs/<gn> --indep-params results/hpc_runs/<ind> --compile` | `results/fit_table_<stamp>/tab_model_fit.tex`, `tab_q_by_block.tex`, `tab_params_estimates.tex`, `fit_table.json`, `test_wrapper.pdf`; `--paper` copies the three tables into `paperA_joint_loss/` |
| recovery | `python paperA_model/recovery_table.py results/hpc_runs/<rec> --compile` | `results/recovery_table_<stamp>/tab_recovery.tex` (truth, start, recovered, noise s.e., z, data s.e., z; order of `tab:model_params`) |
| marriage diagnostics | `python paperA_model/diagnostics_marriage.py --start results/hpc_runs/<gn> --threads 4` (2 evaluations, ~5 min) | `results/marriage_diag_<stamp>/marriage_diag.md/.json`, `q_by_block.csv`, `moments_sep_off.csv`, `es_still_with_wife.csv` |
| counterfactuals | `python paperA_model/counterfactuals.py --start results/hpc_runs/<gn> --indep results/hpc_runs/<ind> --size full --threads 8` (7 scenarios x 2 models x ~8 min at full size) | `results/counterfactuals_<stamp>/scores.csv` (long), `counterfactuals.md/.json` |
| BPS check (7) | `python paperA_model/bps_check.py --start results/hpc_runs/<gn>/best.json --K 3 --threads 8` (**never `--apply`** while the HPC chain runs: it rewrites `inputs/wage_process.json`) | `results/bps_<stamp>/bps_check.json` (BPS Table 3 next to the published values; ~6 min at K = 1, ~17 min at K = 3 on the PC) |

Use the CMA-ES folder in place of `<gn>` once it has finished (`best.json` or `mean.json`; a CMA folder has no
`se.csv` until `estimate.py se --start <cma>/best.json` has run: give that `se.csv` as the second `--params` item).

### fit_table.py

A SOURCE is an `evaluate` folder / its `moments.csv`, or a run folder / its `best.json`. For a run, moments come from
`best.json`, and `in_objective` and the weights from `run.json` (`obj_exclude`, `weighting`, `K`; pseudo runs use
their `pseudo_targets.csv`). Layout (as `tab_joint_job_loss.tex`): one specification per column (data, (s.e.), main
model, z, independent-shock model, z), moments as rows with the targets file's description and window, blocks as row
panels; moments outside the objective carry $^{r}$ ('reported'). `tab_model_fit.tex` is a `longtable` (main.tex needs
`\usepackage{longtable}`). `tab_params_estimates.tex` follows the rows and order of `tab:model_params` (then the
extensions eta_up, c_mem, sigma_eps): start (`run.json` `theta_start`), estimate, sandwich s.e. (`se.csv`), bounds;
parameters not free in the run are marked 'fixed'.
Test (2026-10-19): source `results/evaluate_20261019_064228_p27000` (the start; Q in the tables 11,726.0 = the
evaluation's Q; 85 of 97 moments in the objective), indep column filled from the old closed-form recovery run as a
stand-in; compiles without overfull boxes.

### recovery_table.py

Reads `recovery_report.csv` of the run (written by `recovery_report.py` at the end of `polish --pseudo`).
Test: `results/runs/recovery_closed_20261018_151959` gives 3 of 19 within 2 noise s.e. and 8 of 19 within 2 data
s.e., as in the README.

### diagnostics_marriage.py (Fable's two checks)

(A) one evaluation with separation switched off through the existing Model overrides `sig_E = sig_N = 0`, against
the evaluation at `--start`, same CRN draws (noise floor of Q about 30); Q by block and the employment, wealth,
search, exits, added-work, consumption and separation moments side by side. (B) the simulated 'still with baseline
wife' coefficients by event year -3 ... +6 (reference -2), by race and pooled, from the targets' own stacked panel
(`panels.units`, `stack_rows`, the moments' event window; `moments.twfe` with unit and cell effects), next to the PSID
event study `output/father_displacement.csv` (IGE/19). Only the mean of years 1-3 is targeted.

Pre-estimate reference at the analytic start (`results/marriage_diag_20261019_092447_p18108/`):
- (A) Q 11,726.0 -> 8,650.6 with separation off (-3,075). Employment levels 3,537 -> 1,088 (wives' employment with no
  child 0.954 -> 0.863, youngest 0-5 0.962 -> 0.860, youngest 6-17 0.950 -> 0.832; data 0.809 / 0.754 / 0.823); her
  exits 4,622 -> 3,297; wealth 2,702 -> 1,810; her search 246 -> 598 (persistent CPS entry Black 0.089 -> 0.027, White
  0.036 -> 0.017; data 0.040 / 0.032); separation 3 -> 1,221 (the separation moments themselves). At the start values
  the separation risk keeps wives at work: without it their employment closes 49-93% of the gap to the data
  (63% with no child, 49% with a child 0-5, 93% with a child 6-17).
- (B) still with baseline wife, model vs PSID: pooled -0.029 / -0.029 / -0.039 vs -0.027 / -0.037 / -0.050 in years
  1 / 3 / 6 (mean 1-3 -0.029 vs -0.031; 4-6 -0.033 vs -0.048); Black -0.028 / -0.014 / -0.026 vs -0.037 / -0.053 /
  -0.074 (1-3 -0.019 vs -0.045; 4-6 -0.018 vs -0.070); White -0.018 / -0.018 / -0.014 vs -0.017 / -0.022 / -0.030
  (1-3 -0.020 vs -0.019; 4-6 -0.014 vs -0.029). The simulated gap does not keep widening after year 3 (in the model
  the response sigma_J applies only in months in which the husband is non-employed); the PSID gap does, most for Black
  couples.

### counterfactuals.py

Implemented (theta or existing Model overrides only): `base`; (i) `i_common_off` pi_c = 0, m_H = 1; (ii) `ii_ui12`
UI expiry hazard 1/6 -> 1/12 (Model override `ui_exp`, read by the solver's outcome tables and the simulator) and
`ii_ui12_pic2` with pi_c doubled; (v) `v_haz` Black couples with the White displacement hazards, `v_sep` with the White
separation response, `v_haz_sep` both. Scores by race, workplace match and race x match: consumption around his
displacement (log change from the 6 months before to the loss month and to the 12-month mean; all his losses and joint
losses), shares of married couple-months with no earner and with no earner and no credit (assets within 1% of a_bar
of the limit), and a consumption-only consumption-equivalent at entry (no work costs or taste shocks; labelled as
such). The hook spec for the scenarios that need code (both spouses entitled at a joint loss: the take-up draw in the
(1, 1) configuration and in `sim_kernel`; EITC expansion vs equal-cost transfer: `eitc_scale` and `transfer`
overrides in `inc0` / `incS0`; childcare subsidy: `cc_mult` on `pcc[1]`; full-value welfare and children's outcomes)
is in the module docstring, to be coded behind default-off flags after the CMA-ES jobs have started.
Smoke test at the analytic start, default size (`results/counterfactuals_20261019_092627_p1536/`, `--size
k_s2_era1_a20 --scenarios base i_common_off v_haz v_sep --threads 4`, 1.5-2.3 min per scenario; start values, not
estimates): log consumption change at his loss, loss month / 12-month mean, all couples: base -0.054 / -0.040 (joint
losses -0.154 / -0.131); (i) -0.058 / -0.042 (joint losses fall from 534 to 37); couple-months with no earner 0.23%
-> 0.15%; consumption-only CE +1.09%. (v) Black couples with White hazards: Black displacements of husbands 10,350 ->
6,061, no-earner share 0.30% -> 0.24%, CE +2.38% for Black couples; with the White separation response alone +0.43%.
White couples are unchanged to the last digit in (v) (common draws).

### bps_check.py (BPS's estimator on the simulated couples; never `--apply`)

Fixed 2026-10-19 (the WP3 smoke runs `results/bps_20261019_093701/`, `_093959/` had every Table 3 value missing):
1. Education: the entry file's `h_educ` / `w_educ` are years, now passed with `educ_in_years=True` (before, every row
   had missing education and BPS's sample was empty).
2. The model: `bps_check.py` now builds it through `post_common.setup` exactly as `estimate.py evaluate --start
   <start>` (EXT_DEFAULTS or the run's `run.json` extensions, the borrowing wedge `r_wedge` = 0.0066 per month,
   `--set-fixed`, the extras as fixed inputs, size, CRN seed) and simulates with `post_common.simulate_only`; the json
   records start, K, size, seed, extensions and `r_wedge`. `--start` takes a run folder or its `best.json`.
3. The r(3200) in BPS's `pi_s_estimation.do` was our shim, not the data: `_bpsfix` placeholders for the dummies the
   simulated panel lacks (no 'other race' couples, no wife born before 1941) survived into BPS's joint `xi` call,
   which renamed the wife's stubs, so the hard-coded Mata lists no longer conformed. The placeholders are now
   registered in `xi`'s own drop list (`bps_reconciliation/HARNESS.md` Section 7). Round trip on BPS's PSID panel
   after the fix: identical to the reference runs to the last digit (full sample, Black and White heads), 73 of 74
   published cells as before.

Test at the analytic start (start values, not estimates), BPS's default switches, measurement error = Bound et al.
shares + consumption 0.0332 + gross errors 1% x s.d. 0.7. BPS Table 3, all ages (T4C41), GMM s.e.:

| | BPS published (PSID) | model K = 1 | model K = 3 |
|---|---|---|---|
| sigma2_v1 his permanent | 0.0303 | 0.0320 (0.0016) | 0.0277 (0.0010) |
| sigma2_v2 her permanent | 0.0382 | 0.0368 (0.0019) | 0.0354 (0.0010) |
| sigma_v1v2 | 0.0027 | 0.0020 (0.0013) | 0.0032 (0.0007) |
| sigma2_u1 his transitory | 0.0275 | 0.0062 (0.0022) | 0.0131 (0.0013) |
| sigma2_u2 her transitory | 0.0125 | 0.0132 (0.0024) | 0.0137 (0.0013) |
| sigma_u1u2 | 0.0058 | 0.0048 (0.0017) | 0.0046 (0.0010) |
| rho_u1u2 / rho_v1v2 | 0.312 / 0.079 | 0.529 / 0.058 | 0.340 / 0.103 |
| BPS sample (head-waves) / GMM N | 10,479 / 7,295 | 26,088 / 19,412 | 78,602 / 58,485 |
| displacement couple-years his / hers / joint | 414 / 288 / 28 | 2,210 / 1,306 / 258 | 6,706 / 3,997 / 792 |
| Table 4: E(pi), E(s) | 0.150 / 0.708 | 0.041 / 0.587 | 0.039 / 0.585 |
| wife's hours to his permanent wage (M_h2v1); consumption (M_cv1) | -0.752 / 0.316 | -0.208 / 0.443 | -0.357 / 0.408 |
| chain `ch_tot` (10% fall in his permanent wage, %; harness on PSID 3.93); split gov / family / savings | 3.9; 0.20 / 0.63 / 0.17 | 1.45; 0.36 / 0.49 / 0.15 | 1.78; 0.30 / 0.60 / 0.11 |

Folders: `results/bps_20261019_133727/` (K = 1: 38,566 head-waves written from 8,814 couples; simulation 53 s, Stata
5.0 min, total 5.9 min) and `results/bps_20261019_134505/` (K = 3: 115,698 from 26,442; 124 s, 15.0 min, 17.2 min).
Reading at the start values: the permanent variances, both covariances and her transitory variance are within
about 1-3 s.e. of BPS's; his transitory variance is half (K = 3) to a quarter (K = 1) of BPS's 0.0275, although the
model's sigma_nu_h^2 is set to that 0.0275 (the K = 1 and K = 3 draws differ, so the gap between them is noise plus
the jump trim's sensitivity, HARNESS.md 6.2). The printed plan-1.2 correction (not applied) would raise sig_nu_h
from 0.166 to 0.20-0.22. E(pi) is a quarter of BPS's and the chain total about 40% of it. These are start values; the comparison that matters is at the estimate:
`bps_check.py --start results/hpc_runs/<gn> --K 3 --threads 8` (and `--sigma-nu-zero` for check (7) proper).
