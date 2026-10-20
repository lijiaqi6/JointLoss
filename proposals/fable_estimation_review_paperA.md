# Paper A: where the structural model and its SMM estimation stand, and what to do before spending HPC time

Independent review, 2026-10-18 evening. Read only: `paperA_joint_loss/sec7_model.tex`, `model_document.tex`
(D1-D18), `proposals/paperA_identification_plan.md`, the three earlier notes, every file of `paperA_model/`
(`params.py`, `analytic_start.py`, `model.py`, `solve.py`, `simulate.py`, `panels.py`, `moments.py`, `estimate.py`,
`hpc_job_a.py`, `tests/`), `output/paperA_targets.csv`, and the results folders named in the brief. Nothing was run
except one-line reads of CSV/JSON files. Terminology: search friction; human capital level / accumulation /
depreciation. D1-D18 are taken as settled; I raise two of them (taste-shock scale, borrowing) only because the start
evaluation shows validity problems that no estimated parameter can absorb.

## 0. Verdict in five lines

1. The model code is in good shape: eleven staged checks pass, the solver is accurate (EGM vs brute force 99th
   percentile 4.4e-5), the measurement layer reproduces IGE/60's estimators to 4e-15, all 91 targets are finite.
2. The recovery failure is mostly a budget and optimizer-design problem, not a model-identification problem, but the
   objective as weighted makes about 85 of the 91 moments nearly irrelevant: 95.6% of the total diagonal weight sits on
   four CPS hazard rates. The design must change before any 36-hour job.
3. The misfit at the start (Q = 75,239) is 68% one moment (the wife's exit from employment, 0.0026 vs 0.0261, z = -226)
   and 21% two more (CPS entry of non-employed wives, z = -79 and -97). The exit miss cannot be closed by any of the 30
   free parameters without breaking the employment level and the added-worker response: the taste-shock scale
   sigma_eps = 0.05 is fixed (`model.py:123`) and is the only object that governs monthly churn.
4. Three further validity tensions are visible already at the start and will shape the counterfactuals: the couple type
   needed for the CPS leads and lags (kappa - 1 = 2.6) doubles the PSID annual joint-loss excess (0.118 vs 0.063, z = 11);
   the wealth profile has the wrong shape in age (too many in debt young, too many rich old) at any single borrowing
   limit; SNAP receipt of Black couples cannot reach 15% even at zero stigma (10.4%).
5. Replace "CMA-ES for 8,000 evaluations" by "Gauss-Newton from the analytic start, then CMA-ES around it with
   Jacobian-based scaling, then Gauss-Newton polish", with a trimmed and re-weighted moment vector and 25-26 free
   parameters. The first HPC job is the Gauss-Newton pseudo-data recovery: it decides in three hours whether anything
   is unidentified.

## 1. What the evidence says about the recovery failure (question 1)

### 1.1 Budget

The closed-form recovery (`results/runs/recovery_closed_20261018_151959/recovery_report.md`) stopped after 496
evaluations with Q = 482 and sigma = 0.14 (from 0.3): CMA-ES had barely begun to adapt its covariance. Q by generation
(2,907, 1,900, 1,780, 926, 708, 655, 505, 505, 505, 505, 482) shows the classic plateau-then-escape of a search whose
step distribution is still learning the valley's orientation. The all-parameter run
(`results/runs/recovery_all_20261018_181911/generations.csv`) is worse: after 352 evaluations the best Q is 3,179, the
generation median 8,000-12,000, sigma 0.265 (from 0.3). Both are far from converged. In 19-30 dimensions CMA-ES needs a
few thousand evaluations even on a well-scaled quadratic; the plan's 3,200 is a lower bound, not a budget.

The all-parameter run is also obsolete and should be discarded, not resumed: its truth is the old start
(`run.json`: kappa_S = 2.6386, above the upper bound 1.0, so the pseudo targets were produced with zero SNAP receipt and
the search is bounded at 0.99; delta_h from the PSID annual rates, not the CPS T7 hazards). Its best point has
d_w -81%, sigmaJ_B +167%, a_bar +57%, p_H -50% against truth, which says nothing about identification at the current
start.

### 1.2 Optimizer design

Three design features multiply the budget CMA-ES needs.

**Weighting.** `moments.py:74-78` uses W = diag(1/se^2). Shares of the total weight by block (from
`output/paperA_targets.csv`):

| block | moments | share of total weight |
|---|---:|---:|
| Base hazards (CPS wife and husband hazards, PSID annual rates) | 12 | 95.6% |
| Her exits (one CPS moment) | 1 | 3.1% |
| Her search (CPS entry, SIPP build-up) | 6 | 0.7% |
| all other 12 blocks | 72 | 0.6% |

Four moments carry 92%: `cps_wife_hazard_pooled` 28%, `cps_wife_hazard_white` 26%, `cps_h_hazard_W` 20%,
`cps_h_hazard_pooled` 19%. Inverse-variance weighting is correct in theory, but with a 2.9-million-row CPS next to a
20,000-row PSID it turns the SMM into "fit four hazards, then the exit rate, then the entry rate"; the joint-loss,
wealth, consumption, separation and safety-net blocks that the counterfactuals rest on are tie-breakers. In the
recovery this shows as the deltas being off by 6-7 data s.e. while Q is 482: the hazards pin (E m) delta_j, not delta_j,
so delta_w_B (+32%) and m_H (-15%) moved together along that product while the moments that would separate them
(T28 over-dispersion, se 0.014 and 0.008; leads and lags, se 0.001-0.002) carry 0.1% of the weight.

Two of the four dominant moments are exact duplicates: the pooled CPS rates are race-share averages of the race-specific
ones (`cps_wife_hazard_pooled`, `cps_h_hazard_pooled`, `cps_entry_pooled`; README open issue 1). The three SIPP
`_nosep` comparison rows (se 0.0004-0.001) cannot be matched by a model in which husbands leave jobs only by
displacement (0.989 vs 0.983, z = 15-19; README open issue 3) and add 894 to Q at every theta.

**Scaling of the search space.** `estimate.py:417` starts CMA-ES isotropic in logistic units (sigma0 = 0.3 in every
coordinate, no `CMA_stds`). The Jacobian (`results/jacobian_20261018_145353/report.md`) shows sensitivities per 10% move
from 0.45 (sigmaJ_B) to 24 (phi_F) in value units: the Hessian CMA-ES must learn has an eigenvalue spread of order
(24/0.45)^2 ~ 3,000 before the correlations. CMA-ES learns this in O(n^2) evaluations; a Gauss-Newton step uses it in
one.

**Simulation noise relative to the weights.** `results/noise_20261018_151553/moment_noise.csv`: for the most heavily
weighted search moments the simulation s.d. across CRN seeds exceeds the data s.e. (`cps_entry_pooled` 1.16,
`cps_entry_white` 1.03, `sipp_wife_emp_s6` 1.61, `sipp_his_emp_s6_sep` 1.28, `sipp_his_emp_s3_nosep` 1.06). The noise
floor of Q at a perfect fit is sum(ratio^2) = 26.6 — small against 75,239 but not against the Q = 482 at which the
closed-form recovery stalled, and it means that with K = 3 the entry rate is measured less precisely in the model than
in the data. The 2% rule in the plan (Q spread / Q at the start) is satisfied only because Q at the start is huge; the
rule should be per moment (simulation s.d. below half the data s.e. for every targeted moment), which needs K ~ 6 for
the CPS search block or a weight that includes the simulation variance.

### 1.3 Genuine identification weaknesses

Reading the Jacobian on the range scaling (the plan's protocol; the value scaling makes theta_05 look flat only
because its start value is 2e-4) and the two recoveries together:

| parameter(s) | evidence | reading |
|---|---|---|
| lam_h_B vs lam_h_W | range norm 6.8 / 15.2; the only race-specific husband-search moments are `psid_es_hh_13_B/W` with se 46 and 34 hours; the SIPP path is pooled; the analytic start already sets them equal | not separately identified by the targets: merge |
| sigmaJ_B vs sigmaJ_W | range norm 5.5 / 11.0; the targets are -0.040 (se 0.021) and -0.027 (se 0.012): a race difference of 0.5 s.e.; recovery sigmaJ_W +4.2 data s.e. with sigma0_B -10.5 (baseline traded against response) | one common sigma_J |
| d_h vs pi_dn_h (and d_w vs pi_dn_w) | weakest direction after kappa_S/theta_05 (sv 0.149, loadings -0.89 / +0.44); three SIPP spell groups with se 0.023-0.065 identify level and slope per spouse; recovery d_w +6.7, pi_dn_h +2.3 data s.e. | one common d (or d = 0 if the 1-3-month loss is read as within 2 s.e. of zero: -0.058 (0.023) and -0.060 (0.030) are at 2.0-2.5 s.e.) |
| p_H vs m_H | T28 is now a target (`psid_disp2plus_B/W`) and the pair no longer appears among the collinear columns; but the implied T28 moves from 0.125 to 0.207 as the assumed panel length goes from 10 to 20 years (`start_analytic.json`, `check_section_1_4`), so the moment is as much about the measurement layer as about p_H; recovery m_H -4.4 data s.e. with p_H fixed, p_H -50% in the all run | profile Q along the ridge before the main run; fixing p_H at 0.1 (the plan's robustness alternative) is defensible under the parsimony rule |
| a_bar | range norm 7.2, value norm 3.1, 99% of its sensitivity in the wealth block, which the model misfits in shape (Section 5) | identified only through a block the model cannot fit; the estimate will be a compromise, not a credit limit |
| lam_w_W / theta_05 / theta_617 / F | corr -0.95, -0.94, -0.90; +0.97, +0.94, +0.92 | an artefact of the weighting: all four move `cps_entry_pooled` (se 0.0003) most; the levels of employment by child age (se 0.004-0.006; 0-5 vs 6-17 differ by 12 s.e.) separate theta_05 from theta_617 once they count. F is the exception (next row) |
| F | range norm 15, but 88% of it in Her search, i.e. F acts as a work cost; its own moments (consumption after her displacement -0.031 (0.020), joint minus single -0.059 (0.065)) are within 1.5 s.e. of zero | F and phi_F cannot be separated by these targets; fix F at its coded mapping (10% of part-time earnings, `analytic_start.py:226`) or drop it |
| kappa_S | now has slope (0.104 -> receipt 7.2% / 3.5%), but even kappa_S = 0 gives 10.4% Black receipt against 15.0% | interior identification requires the eligible mass to be right (Section 5.4); otherwise the estimate sits at the bound |

Everything else (delta_w, delta_h by race, pi_c0, pi_c1, lam_w by race, pi_up by spouse, phi_F, phi_P, phi_h, sigma_0 by
race, theta_05, theta_617) is identified by precise moments with the expected primary block.

### 1.4 The experiment that separates the three explanations

A Gauss-Newton (Levenberg-Marquardt) recovery from truth + N(0, 0.5) in logistic units, pseudo targets with the same
CRN seed as the estimation (so Q = 0 at truth). One iteration is a CRN central-difference Jacobian (61 evaluations, four
rounds of 16 workers) plus two or three trial steps: about 12 minutes on the HPC; fifteen iterations, three hours.
Outcomes: (i) it returns to truth with Q near 0 -> the CMA-ES failure was budget and design; (ii) it converges to Q near
0 at a different theta -> that direction is unidentified (the Jacobian at the end point names it); (iii) it stalls at
Q far above 0 -> the simulated moments are not smooth enough for derivative methods at this K and step, and the remedy
is K or the step size, not the model. The plan's "within 2 noise s.e." criterion is extremely strict (37,080 simulated
couples; noise s.e. of delta_w_W 1.8e-5); "within 2 data s.e." is the criterion that matters for the paper.

## 2. What the HPC runs should look like (question 2)

Arithmetic: 100-140 s per evaluation under load, 16 workers, popsize 16 -> one generation per round, 2-2.5 minutes; a
36-hour job holds 850-1,000 generations (14,000-16,000 evaluations); a 61-evaluation Jacobian is 10 minutes; a
Gauss-Newton iteration 12 minutes.

| step | job | evaluations | wall time | purpose |
|---|---|---:|---:|---|
| 0 | `Joint-test` | 3 + 32 | 30 min | reproducibility of Q at the start (see Section 5.9 on the tolerance) |
| 1 | `Joint-jacobian` at the corrected start, `--step range`, trimmed moment vector | 61 (or 51 with 25 free) | 15 min | re-read the collinear pairs after the weighting change; feeds the CMA scaling |
| 2 | `Joint-recovery-gn` (new `polish` command, pseudo data, 25-26 free) | ~900 | 3 h | Section 1.4; decides the cut list |
| 3 | `Joint-gn-main` on real data from the analytic start | ~900 | 3-4 h | candidate estimate; the final Jacobian comes free |
| 4 | `Joint-smm-main`: CMA-ES from the GN candidate, `CMA_stds` from the Jacobian, sigma0 0.2, popsize 16, 3,000-4,000 evaluations, `tolfun` ~ 30 (the noise floor) | 3,000-4,000 | 8-10 h | global check around the candidate |
| 5 | two restarts from perturbed starts (start noise 0.5, different `--cma-seed`), 2,000 each, then GN polish of each | ~5,000 | 12 h | local-minimum check; report the spread |
| 6 | `Joint-smm-indep` (pi_c = 0, m_H = 1) by the same GN + CMA route | ~4,000 | 10 h | the restricted model on the same draws |
| 7 | `Joint-se` at the best point (Jacobian + 5 CRN re-simulations) | 61 + 5 | 20 min | sandwich s.e. |
| 8 | `Joint-smm-block` (block weights) by the same route | ~4,000 | 10 h | robustness, as planned |

Total about three 36-hour jobs instead of the four to five implied by 8,000-evaluation CMA-ES runs with resumes, and
each stage produces a usable intermediate result. Settings in detail:

- **Gauss-Newton / Levenberg-Marquardt** (`estimate.py polish --start ... --iters 15`): G from CRN central differences
  in logistic units with step 5% of the value (the Jacobian code `jacobian_at`, `estimate.py:265-287`, already does
  this); step delta = -(G'WG + mu D)^-1 G'W d with D = diag(G'WG); try mu in {0.1, 1, 10} x the previous accepted mu as
  three parallel evaluations; accept the best if Q falls, else multiply mu by 10. Stop when the relative fall in Q over
  two iterations is below the noise floor (about 30 units) or 15 iterations. Every iteration writes `best.json` and a
  Jacobian report, so stage 7 is a by-product.
- **CMA-ES scaling**: pass `CMA_stds` = (1 / range-scaled column norm_j), normalised to a median of 1, so that sigma0 is
  the same number of "moment standard errors" in every direction; keep popsize 16 (one round per generation); sigma0 0.2
  around a GN candidate, 0.3 from a cold start; `tolfun` and `tolfunhist` around 30; `cma_seed` varied across restarts
  (`estimate.py:550` fixes it at 1 for every run). Use `es.result.xfavorite` (the distribution mean) as well as the
  best-ever point: with CRN chatter the mean is the better estimate of the minimum.
- **Weighting for the main run**: diagonal inverse variance after (a) removing the three pooled CPS duplicates and the
  three SIPP `_nosep` rows from the objective (keep them in the fit table as checks), (b) adding the simulation
  variance: W = diag(1 / (se^2 + sim_var)) with sim_var from the noise run at the start (the sandwich already uses
  Omega = Vdat + Vsim, `estimate.py:492`; using the same object in W is coherent). Weight concentration on the hazards
  will remain (they are precise and the model fits them nearly one for one through the deltas); the GN step is
  indifferent to it, which is the main reason to use GN.
- **K**: 6 copies for the main runs if the evaluation stays under ~110 s alone (simulation 8.5 s -> 17 s, moments 13 s
  -> 26 s on 78 s); otherwise K = 3 with the noise-inclusive weights.
- **Staging**: the PI's one-run rule is respected by the final joint GN + CMA + GN estimate on all free parameters. The
  closed forms and the start-value fixed point (Section 3) are start values, not stages of estimation. I would not run
  block-wise estimations as separate stages; the GN route makes them unnecessary.
- **Fixed, merged and dropped parameters** (Section 4): pi_c2 (inactive at the default size), lam_h common, sigma_J
  common, d common, F fixed at its coded mapping; p_H fixed at 0.1 if the ridge profile is flat within the noise
  floor. 30 -> 25 or 26 free.

## 3. Closed-form and coded-mapping opportunities the pipeline misses (question 3)

All of these are coded mappings that improve start values or hold a calibrated input consistent with the current
theta; none removes an endogenous parameter from the joint SMM.

1. **Start-value fixed point on the simulation's own nuisance rates (one or two evaluations).** The closed forms use
   assumed values for three endogenous rates that the simulation reports directly: the wife's acceptance (assumed 0.6,
   `analytic_start.py:202`; at the start the simulated entry 0.043 with lam_w_W 0.125 implies acceptance 0.35, so
   lam_w_W should start near 0.21), P(looking | displaced) in the CPS job-loser classification (the wife's hazard is
   0.0019 vs 0.0022 White, z = -7, because a displaced wife who does not look is an exit, not a job loser), and the
   husband's expected non-employed months in the separation window (D_r = 5 assumed, `analytic_start.py:165`;
   `sigmaJ` start gives -0.025 / -0.017 vs -0.040 / -0.027). A `--from-sim <evaluate dir>` option in `analytic_start.py`
   that reads these rates from the stored simulation and re-solves the eight closed forms would cut several blocks of
   Q(start) at the cost of two evaluations, and it keeps the mapping coded.
2. **Preference start values by one-dimensional roots instead of the static logit.** `static_preferences`
   (`analytic_start.py:46-100`) ignores the continuation value of holding a job and human capital accumulation, so
   wives work in 95% of months (0.809 in the data) and the part-time share is 0.22 (0.337); theta_617 > theta_05 at the
   start although employment is lower with a child 0-5. Three bisection roots on simulated moments (phi_F on
   `psid_wemp_none`, phi_P on `psid_pt_w`, theta_05 on `psid_wemp_05`), four evaluations each, give a start where
   the employment block is within a few s.e. These are monotone one-dimensional problems; the GN run then starts in
   the right basin.
3. **Wage-process probabilities as a live mapping of pi_up.** `wage_process_closed_form` (`params.py:184-194`) already
   computes p_eps_j = Var_j / (12 psi_j^2) - p_c - pi_up_j (1 - pi_up_j) x employed share as a function of theta, but
   `load_fixed` (`params.py:172-177`) freezes the values written at the start's pi_up. When the SMM moves pi_up
   (recovery: +34 noise s.e.), BPS's permanent variance is no longer held. Evaluating the closed form inside each
   evaluation at the current pi_up (one line in `Model.__init__`) keeps D7 exactly at every theta; the one-time BPS
   correction factor then multiplies it. The correction itself (`bps_check.py --apply`) has not been applied
   (`inputs/wage_process.json`, status line); it should be, before the main run, as the plan says.
4. **Hazard check at the default size.** For husbands the closed form is exact up to type selection out of employment
   (H types are non-employed 7% of months against 0.6%, which lowers E m among the employed by about 3%), yet the
   simulated White husband hazard is 9% below the target at the closed-form start (0.00309 vs 0.00340). Test 7 passes
   at the test size (5 levels, 30 assets, z up to 2.25 over 30 moments); the same comparison at the default size, by
   type, from a stored simulation would show whether the remaining 6% is the CPS layer (which husbands are "employed at
   t and observed at t+1") or something to fix. This is a read of existing output, not a run.
5. **Separation baseline.** sigma_0 = -ln(1 - s_r) / 12 reproduces the annual rate within 1 s.e. at the start (0.0327 vs
   0.0316; 0.0157 vs 0.0152); it stays in the SMM but will not move. Nothing to do.
6. **Husband's employment rate by race** is not a target although EITC, SNAP and the insurer-is-hit mechanism all run
   through it, and the model's husbands are non-employed in only about 2-3% of months (displacement at (E m) delta_h
   against job finding 0.26). Adding the PSID husband's employment rate (or non-employment months) by race as a target
   is an IGE/60 change; it is the moment that would discipline lambda_h and the SNAP eligible mass together.

## 4. Parsimony (question 4)

Applying the PI's rule (drop what the data cannot separate) to the evidence of Section 1.3:

| action | parameters | basis | count |
|---|---|---|---:|
| already inactive | pi_c2 | s = 1, 2 merged at the default size (`estimate.py:203-204`) | 30 |
| merge | lam_h_B = lam_h_W | no race-specific husband-search target with precision; start already equal | 29 |
| merge | sigmaJ_B = sigmaJ_W | race difference in the response is 0.5 s.e.; the Black column is the weakest after kappa_S | 28 |
| merge | d_w = d_h | level vs slope from three noisy SIPP points per spouse; the weakest direction of the Jacobian | 27 |
| fix at the coded mapping | F | inseparable from phi_F with these targets; its own moments within 1.5 s.e. of zero | 26 |
| fix after the ridge profile | p_H = 0.1 | the ridge is pinned by kappa; T28 depends on the panel-length composition; the plan's own robustness alternative | 25 |
| keep (re-check after re-weighting) | theta_05, theta_617 | the collinearity is through `cps_entry`; the levels by child age differ by 12 s.e. | |
| keep | delta by race, pi_c0, pi_c1, lam_w by race, pi_up by spouse, pi_dn by spouse, phi_F, phi_P, phi_h, kappa_S, sigma_0 by race, m_H, a_bar | precise primary moments | |

A common pi_dn across spouses (on the cut list) is not supported by the evidence: the SIPP slopes differ (0.0085 vs
0.0143 per month) and both columns have the expected block. phi_h is one for one with the husbands' part-time share and
harmless to keep.

## 5. Model-validity and coding flags from the start evaluation (question 5)

Q = 75,239 by moment (`results/evaluate_20261018_202220_p37396/moments.csv`), the top of the list:

| moment | data | model | z | share of Q |
|---|---:|---:|---:|---:|
| cps_wife_exit | 0.0261 | 0.0026 | -226 | 68.1% |
| cps_entry_white / pooled | 0.0751 / 0.0750 | 0.0434 / 0.0512 | -97 / -79 | 20.9% |
| psid_wemp_05 / 617 / none | 0.754 / 0.823 / 0.809 | 0.948 / 0.942 / 0.948 | +34 / +27 / +26 | 3.4% |
| psid_pt_w | 0.337 | 0.215 | -27 | 0.9% |
| psid_liq_le0_25 / 35 / 45 | 0.568 / 0.462 / 0.381 | 0.797 / 0.659 / 0.241 | +31 / +24 / -17 | 2.4% |
| psid_liq_hi_45 | 0.177 | 0.353 | +30 | 1.2% |
| sipp_his_emp_s3/6/12_nosep | 0.983 / 0.972 / 0.960 | 0.989 / 0.984 / 0.982 | +15 / +17 / +19 | 1.2% |
| psid_cy_diff_all / diff | 0.063 / 0.041 | 0.118 / 0.108 | +11 / +12 | 0.4% |
| sipp_wife_emp_s0/1/6 | 0.019 / 0.037 / 0.054 | 0.047 / 0.086 / 0.169 | +6 / +7 / +11 | 0.3% |
| psid_snap_B | 0.150 | 0.072 | -11 | 0.2% |
| psid_wg_w_45, psid_wg_h_35, psid_wg_h_45 | 0.027 / 0.029 / 0.013 | 0.046 / 0.046 / 0.039 | +5 / +6 / +7 | 0.2% |

Most of the employment-level and entry misses are start-value problems (Section 3.2) that the SMM will remove. Five
items are not.

### 5.1 The wife's exit rate: a parameter is missing for the moment (validity)

The data target is the CPS monthly transition of an employed wife to unemployment for a non-job-loss reason or out of
the labor force, husband employed (`paperA_targets.csv`, definition of `cps_wife_exit`): 2.6% a month, 31% a year. In
the model this transition is a quit: a wife who holds a job and chooses zero hours loses the job and is not entitled to
UI (`simulate.py:368-370`), and with a search friction of 0.13-0.16 a month a quit costs about six months of
non-employment. With i.i.d. extreme-value taste shocks of scale 0.05 in utility units (`model.py:123`, from
`FIXED_DEFAULTS["sigma_eps"]`) and a full-time work cost of 0.31, the probability of that choice is 0.26% a month. The
state variables that could move a wife across the margin change slowly (children, assets, human capital) or rarely (his
displacement, one transitory draw a year), so monthly churn is governed by sigma_eps alone, and sigma_eps is fixed.

The SMM can raise exits only by pushing wives toward indifference (phi_F and theta up), which also lowers employment and
raises the added-worker response; the data want 81% employment, 2.6% monthly exits and a small response (5.4 points at
six months). A representative wife with small taste shocks cannot produce all three; persistent heterogeneity in work
costs plus larger transitory shocks can. Two readings, for the PI:

- Estimate sigma_eps (one parameter; its natural moment is the exit rate, which otherwise has no parameter). Bacher et
  al. use 0.1 and call their shocks computational; here the exit target makes the scale a behavioral object. The plan
  already promises a Q profile in sigma_eps (D-table "profile of Q reported"); run it first: four evaluations at
  sigma_eps in {0.05, 0.10, 0.20, 0.30} (about 12 minutes on the PC when free) tell whether the exit rate moves by the
  order of magnitude needed. If it does, estimate it; if it does not, the margin is structural and a persistent taste
  type is the next candidate (a D-level decision; parsimony says not yet).
- Treat part of the 2.6% as CPS classification error. Matched-CPS gross flows out of employment are known to be inflated
  by response error (Poterba and Summers 1986; Abowd and Zellner 1985 put spurious E -> N flows at the order of one
  point a month). The model's CPS layer has no classification error. If the PI accepts this reading, the target should
  carry a coded correction or a wider standard error, not a weight of 9e7.

Either way, this one moment should not be allowed to be 68% of Q in a 36-hour job.

### 5.2 The couple type is too persistent for the PSID (validity)

The CPS leads and lags give kappa - 1 = 2.6 (`start_analytic.json`, `kappa_minus_1_cps`), the PSID placebo window
0.56. With p_H = 0.10 and m_H = 12.6 the H-type husband's annual displacement probability is 0.26 (White) to 0.39
(Black), so P(H | he is displaced this year) = 0.58 and the wife's annual displacement excess given his is 0.115 — the
model's 0.118 against the PSID's 0.063 (z = 11), and 0.108 against 0.041 for couples in different sectors (z = 12).
The monthly leads and lags (z within 1) and the two-window permanent component (0.024 vs 0.020) fit at the same time. A
permanent type gives the same elevation at every horizon; the data's elevation falls from 2.6 times the base at one to
three months to about 0.5 at one to two years. That is the signature of a correlated shock that is transitory in time
(closures and mass layoffs that span a few months, or timing error in the CPS's month of his loss), not of a permanent
type. Under the current weights the SMM will fit the CPS and miss the PSID annual excess by about 2 s.d. of the
cross-section, and the type-driven precautionary saving in the counterfactuals will be too strong. Options for the PI:
(a) report the tension and let the SMM compromise (the current plan); (b) give the common shock a short memory (the
wife's hazard elevated for k months after his common-shock displacement; one parameter), which fits the leads and lags
without a permanent type of this size; (c) fix p_H and let m_H fall. A profile of Q along the ridge and across m_H is the
cheap first look (five to seven evaluations).

### 5.3 The wealth profile has the wrong shape in age (validity)

Too many couples at or below zero liquid wealth at 25-34 (0.80 vs 0.57) and 35-44 (0.66 vs 0.46), too few at 45-59
(0.24 vs 0.38), and twice the data's share above one year of earnings at 45-59 (0.35 vs 0.18). The borrowing limit is
a_bar = 25.6 thousand (the data's P10 of liquid wealth, `start_overrides.json`) at the saving rate: `model.py:122`
has one interest rate r_m, so borrowing to the limit when young is nearly free, and the terminal value (Social
Security at 40% of final earnings) then makes retirement saving in liquid assets strong. a_bar cannot fix both ends; the
SMM will lower it (fewer in debt young, even fewer at 45-59) and the estimate will not mean a credit limit. D11 fixes
beta and estimates the limit; it does not speak to a borrowing wedge. A coded calibrated wedge (the real credit-card
rate from the Fed's G.19, which ReducedForm/62 already documents for the debt facts) is one line in the budget and would
let a_bar be what it is meant to be. PI decision; until then the wealth block should be read as a compromise.

### 5.4 SNAP receipt of Black couples cannot be reached (validity)

At kappa_S = 0 the model gives 10.4% against 15.0% (and 5.4% vs 3.8% White). SNAP eligibility in the model arises almost
only when the husband is non-employed, and husbands are non-employed in 2-3% of months because they leave jobs only by
displacement. In the PSID 1984-2021 married Black men aged 25-60 are out of work far more often, and the target also
spans the pre-1997 food-stamp era while the default size solves with the 1997-2008 schedule only (fallback (c)). The
estimate of kappa_S will sit at its bound for the Black moment and the "stigma" will be unidentified in the interior.
The remedy is the husband's employment level as a target (Section 3.6) and, for the paper, a statement that the SNAP
moments are matched for White couples and under-predicted for Black couples by the husband's non-employment, not by
stigma.

### 5.5 The wage-growth age profile (known tension B, now quantified)

Two-year growth at 35-44 and 45-54 is missed by 4-7 s.e. at the start (wives 0.058 / 0.046 vs 0.046 / 0.027; husbands
0.046 / 0.039 vs 0.029 / 0.013), because a constant pi_up flattens only through the top level and psi = 0.46-0.49 log
points per level makes the top rarely binding. The plan's trigger ("missed by more than 2 s.e. at 45-54 -> pi_up
h^(-eta) to the PI") fires already at the start; it will fire at the estimate too, since no other parameter moves this
profile. One parameter (eta), decided now rather than after the HPC run.

### 5.6 Husband's earnings loss by race

White husbands' loss is half the data (-6,100 vs -12,054 in years 1-3, z = 3.4; year 6 -6,300 vs -12,100), Black
husbands' slightly above (-4,800 vs -3,700). d_h and pi_dn_h are common across races and set from pooled SIPP earnings
losses; the PSID's larger log loss for White husbands (-24% vs -17%, plan Section 2.1) is not in the model's reach. Not
a bug; a tension between the SIPP (pooled, by spouse) and the PSID (by race) that the fit table should state.

### 5.7 Simulation noise and K

Section 1.2: five moments have simulation s.d. above the data s.e. at K = 3. For the entry rate (the paper's "search at
once" fact) the model's own measurement is noisier than the CPS. K = 6 or the noise-inclusive weight.

### 5.8 Things that look right

The joint-loss monthly block fits at the start (Q = 33 over 10 moments), the closed forms for pi_c(s) work (s = 0 and
the leads and lags within 1 s.e.; s = 2 at -5 s.e. because s = 1, 2 are merged, as expected), the separation block fits
(Q = 2.8), consumption fits within 2.4 s.e., the measurement layer produces every sample. The husband's pooled hazard
is the race-share average of the race-specific ones (0.00382 vs 0.26 x 0.00555 + 0.74 x 0.00309 = 0.00373), so the CPS
layer is internally consistent.

### 5.9 Small code points

- `hpc_job_a.py:118, 259`: the reproducibility test accepts |Q - 75,239.1| <= 0.75 (1e-5 relative). Numba reductions
  on a different CPU (AVX-512 vs AVX2) can differ by more than that at Q = 75,000 without anything being wrong; compare
  the 91 moments to a relative 1e-6 each, or loosen Q to 1e-3 relative, so that the first HPC job does not fail on a
  floating-point verdict.
- `estimate.py:412-413, 65-67`: the 1% margin and the 1e-6 clip in `to_z` are fine now that kappa_S starts at 0.104;
  a start at a bound (kappa_S = 1.0 in the all-parameter recovery) puts z at 13.8, where a sigma 0.3 step does nothing.
  A guard that refuses a start within 1% of a bound would have caught this.
- `estimate.py:550`: `--cma-seed` defaults to 1 for every run; restarts need different seeds.
- `estimate.py:447-450`: `best.json` is the best-ever evaluation; with CRN chatter also store `es.mean` each generation.
- README line 175 says "recovery (31)"; 30 are free at the default size (pi_c2 inactive) and 25-26 after Section 4.
- The all-parameter recovery (`results/runs/recovery_all_20261018_181911`) was started on the obsolete start values;
  its folder should be marked superseded in the README, not resumed.

## 6. Prioritised plan (question 6)

**Fix in code first (PC, no long runs):**

1. Objective: drop the three pooled CPS duplicates and the three SIPP `_nosep` rows from the objective (a `target_obj`
   flag or a `--drop` list; keep them in the fit table); add the noise-inclusive diagonal weight option
   (`--weighting diag_noise`, reading `moment_noise.csv`).
2. `estimate.py polish`: Levenberg-Marquardt with the CRN Jacobian (Section 2), writing `best.json`, the Jacobian report
   and the sandwich s.e. at every iteration.
3. CMA-ES: `CMA_stds` from a Jacobian file, `tolfun`, `--cma-seed` per restart, store the distribution mean.
4. Ties and fixes: a `--tie lam_h_W=lam_h_B sigmaJ_W=sigmaJ_B d_h=d_w` option; `--fix F=<coded value>`; the live
   wage-process mapping p_eps(pi_up) in `Model.__init__`; apply the BPS correction (`bps_check.py --apply`, one Stata
   run).
5. `analytic_start.py --from-sim`: the start-value fixed point on simulated acceptance, P(looking | displaced) and D_r;
   the three one-dimensional roots for phi_F, phi_P, theta_05.
6. `hpc_job_a.py`: the reproducibility tolerance; `EXPECTED_Q` after items 1 and 5.

**Check locally when the PC is free (each a handful of evaluations, 10-20 minutes):**

7. Q and the exit rate at sigma_eps in {0.05, 0.10, 0.20, 0.30} (Section 5.1). This decides whether sigma_eps becomes a
   parameter before the HPC runs; it is the single most consequential check.
8. Q along the (p_H, m_H) ridge and across m_H at fixed p_H (Section 5.2), with the annual joint-loss block and the
   leads and lags reported separately.
9. The husband's hazard by type at the default size against the closed form (Section 3.4), from a stored simulation.
10. Re-run `evaluate` and `jacobian` (21 minutes) at the new start with the trimmed objective; re-read the collinear
    pairs; write `decisions.md` for the cut list as the plan requires.

**Then on the HPC, in this order (Section 2 table):** `Joint-test`; `Joint-recovery-gn` (3 h; the identification
verdict); `Joint-gn-main` (3-4 h; the candidate); `Joint-smm-main` CMA-ES around it with scaling (8-10 h) and two
restarts; `Joint-smm-indep` by the same route; `Joint-se`; `Joint-smm-block`. The old `--maxfevals 8000` CMA-ES runs
from the analytic start should not be submitted: at the current weighting they would spend 36 hours fitting four
hazards and one exit rate.

**Decisions for the PI, with the evidence in this note:** sigma_eps estimated or the exit target corrected (5.1); the
common shock's memory or a fixed p_H (5.2); a coded borrowing wedge (5.3); the husband's employment rate as a target
(3.6, 5.4); pi_up h^(-eta) now (5.5); the five merges and fixes of Section 4.
