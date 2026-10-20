# Paper A structural model (joint job loss of spouses) — code, stages 0-6

Self-contained folder (`model/`, `estimation/`, `scripts/` are not touched; `IGE/60.PaperATargets.py` and
`bps_reconciliation/code/sim_panel_writer.py` are imported read-only). Spec: `paperA_joint_loss/sec7_model.tex`,
`paperA_joint_loss/model_document.tex` (D1-D18), `proposals/paperA_identification_plan.md` (Sections 1-4).
Terminology: human capital level / accumulation / depreciation; search friction (job-finding probability lambda).
Nothing in this folder writes PSID individual records into `results/` or any tracked file: outputs are aggregate
moments, parameters and diagnostics only. `inputs/psid_entry_couples*.csv` (PSID microdata) are git-ignored.

## Structure

| File | Role |
|---|---|
| `params.py` | the 31 SMM parameters (name, default start, bounds, block); fixed inputs (`FIXED_DEFAULTS` overridden by `inputs/fixed_inputs.json` (IGE/62) and `inputs/wage_process.json`); era schedules; `Config` (sizes, fallback switches, `ui_accept`, `w_interp`); `SIZES`, `DEFAULT_SIZE`; `load_start()` = `start_analytic.json`, then `start_overrides.json` (IGE/62: a_bar). Inputs are re-read by every process at start |
| `analytic_start.py` | closed-form start values (plan 1.2, 1.4, 1.5) from the targets file and the IGE/62 inputs -> `inputs/start_analytic.json`, `inputs/wage_process.json` (re-run 2026-10-18 with psi_w 0.457, psi_h 0.495: p_c 0.00099, p_eps_w 0.00879, p_eps_h 0.00397) |
| `model.py` | arrays of one problem (r, s, tau) in one era (budget, configurations, end-of-month outcome tables incl. the offer node, human capital, child chain, separation, terminal value) |
| `solve.py` | numba backward induction (420 months): separated wife, married couple; sequential expectation operators; offer node (`k_offer`); DC-EGM with Gumbel taste shocks, upper envelope, Hermite continuation values, Newton polish, guarded top extrapolation; stores C, W, Dlt (float32) |
| `simulate.py` | monthly couple histories with CRN; the entitled wife's offer decision; the CPS 'looking' classification (`look`); offer outcomes (`acc`) |
| `panels.py` | **measurement layer**: monthly records -> CPS couple-month samples (4-8-4 rotation over every entry month), SIPP panel windows, PSID annual rows, stacked event panels, units with coverage rules, couple-years, consumption event panel with BPS's measurement error, wealth waves. The complete model -> data mapping is in its docstring |
| `moments.py` | **all 91 targets** (88 + T7, `target == 1` of `output/paperA_targets.csv`, same order), IGE/60's estimators (wmean, fe_slope, fe_ols) imported read-only, exact two-way FE solver `twfe` (checked against IGE/60's TWFE: identical to 4e-15); weighting (`diag` default, `block`, `vcov`); objective |
| `estimate.py` | **SMM driver**: `evaluate`, `jacobian`, `polish` (Levenberg-Marquardt in logistic units with the CRN Jacobian; `--pseudo` recovery), `run` (CMA-ES, own SafePool, checkpoint every generation, `--resume`, `--pseudo` recovery, `--cma-stds-from`, `--tolfun`, distribution mean stored), `se` (sandwich), `noise` (CRN seeds, `--save-noise-input`); objective trim (`moments.OBJ_EXCLUDE`, `--drop`), `diag_noise` weights (default), `--set-fixed`, `--free-extra sigma_eps`, `--tie`, start-bound guard |
| `recovery_report.py` | recovery vs truth in simulation-noise and data standard errors |
| `hpc_job_a.py` | Slurm launcher for Stanage in the separate clone `~/joint` (idempotent one-time setup block, entry-file check with the scp command, code snapshot, `--test`, `--push` of aggregate results) |
| `bps_check.py` | check (7): simulated couples -> `sim_panel_writer` -> `bps_on_sim.do` (Stata) and the one-time wage-process correction (`--apply`) |
| `bench.py` | runtime and memory per size |
| `tests/` | staged checks 0-12 (12: extensions of 2026-10-19 off = base model), `run_all.py` |
| `results/` | `tests_20261018.txt`, `bench_2t.json` (stage 3), `evaluate_20261018_145333/`, `jacobian_20261018_145353/`, `noise_20261018_151553/`, `runs/recovery_*/` |

## Decisions implemented (lead, 2026-10-18)

1. **UI and acceptance (Bacher, Grubener and Nord 2025).** An entitled non-employed wife who receives an offer at the
   end of the month may decline it and keep her entitlement, which then lapses only with the monthly hazard 1/6;
   accepting ends it. No new state: the offer node is a binary choice (accept = employed next month; decline =
   (1 - 1/6) entitled + 1/6 not entitled) taken after both spouses' displacement and job-finding events and before
   the human capital, child, separation and transitory draws, with mean-zero extreme-value shocks of scale sigma_eps
   (no Euler constant: an offer carries no taste-shock bonus). In the solver it is a logsum over two expectation
   slices, stored as virtual wife slices; the logit index is stored for the simulator (`Solution.Dlt`, +0.28 GB per
   problem at the default size). Wives without entitlement keep the earlier rule (an offer moves them to the employed
   state, where they choose hours). `Config.ui_accept = False` restores the old rule. Check 5 passes.
2. **Default size** `k_s2_era1_a20` (7 human capital levels, s = 1, 2 merged, the 1997-2008 schedule in estimation, 20
   asset points); counterfactuals use `full` and the era schedules. With s = 1, 2 merged pi_c2 does not enter the
   model: `estimate.py` holds it fixed (30 free parameters). With the real inputs, test 9 now shows 5 levels moving
   simulated mean assets by 34% against 7 (10% with the placeholders), which supports keeping 7.
3. **Solver accuracy.** Diagnosis: the stage-3 failure (99th pct 2.1e-3) was not at the consumption-floor kink. The
   large gaps sat in the middle of the asset grid (a' near -2, 4 and 17 thousand $): with W linear between nodes the
   brute-force optimum sticks to a node (the chord slope drops there), while EGM's policy passes between nodes and is
   valued on the chord, below the true W. The grid near the borrowing limit is already dense (4 nodes within $800),
   so densifying it would not help. Fix: W between nodes is a monotone-limited cubic Hermite interpolant of the node
   values and the exact node derivatives (the derivative the Euler step inverts; in the simulator recovered from the
   stored consumption, D = u'(c / sc) / (beta sc)); the EGM point is polished by Newton steps on the Hermite
   first-order condition where consumption changes by more than 5% between the bracketing endogenous points; above
   the top endogenous point consumption never falls below the last point and W continues with the node derivative
   (with the chord slope the top values fed back and exploded — found by the new full-horizon check). **Result at
   sigma_eps = 0.05: 99th percentile 4.4e-5, maximum 5.1e-4 (target < 1e-3); V at t = 0 within a median 0.021 utility
   units of a 90-point solution (chords at 30 points: 0.448).** Cost: about +40-60% per solve (3.9 -> 6.1-6.7 s).

## Estimation layer changes (2026-10-18 evening; Fable review `proposals/fable_estimation_review_paperA.md`, Section 6)

1. **Objective trim** (`moments.OBJ_EXCLUDE`, one reason each; `--drop` adds ids, `--no-default-exclude` restores the
   full vector): `cps_wife_hazard_pooled`, `cps_h_hazard_pooled`, `cps_entry_pooled` (in the model each is exactly the
   n-weighted average of its Black and White moments, checked in test 11; the data's pooled rates also contain other
   races) and the three `sipp_his_emp_s*_nosep` rows (husbands never quit). They stay in `moments.csv`
   (`in_objective = 0`) and the fit tables. 85 of 91 moments are in the objective.
2. **Weights** `--weighting diag_noise` (default): 1 / (se^2 + var_sim), var_sim from `inputs/moment_noise.csv` (5 CRN
   seeds at the analytic start, K = 3; written by `estimate.py noise --weighting diag --save-noise-input`), scaled by
   K_noise / K. `run.json` / `evaluate.json` record the weighting, the noise file, the exclusions and the weight shares
   by block (`results/diagnostics_20261018.md`).
3. **`estimate.py polish`**: Levenberg-Marquardt in z units (`lm_iterate`): CRN central-difference Jacobian
   (`jacobian_at`, chain rule to z), trial steps for mu x {1e-3 ... 1e3} in one parallel round, accept if Q falls,
   otherwise mu x 1e4 (two retries); writes `best.json`, `iterations.csv`, `evals.csv`, `jacobian.npz` every
   iteration and at the end `report.md` (Jacobian at the best point) and `se.csv` (sandwich); `--pseudo` as in `run`
   (and `recovery_report.md` at the end).
4. **CMA-ES**: `--cma-stds-from <jacobian.npz>` (1 / weighted column norm in z units, median 1, clipped to
   [0.05, 20]); `--tolfun` (also tolfunhist); `mean.json` / `means.csv` (es.mean every generation, Q at the final mean);
   `--cma-seed` default distinct per run (recorded in `run.json`); `--perturb` for real-data restarts.
5. **Start guard**: a free parameter within 1% of its bound range refuses the start (`--bound-margin`). The old code
   silently clipped to that margin: pi_c0 (start 3.4e-5, bounds [0, 0.01]) was moved to 1e-4, three times its start,
   in both earlier recoveries. pi_c0's upper bound is now 0.002 (start at 1.7% of the range).
6. **`--set-fixed name=value`** for `FIXED_DEFAULTS` entries (recorded); **`--free-extra sigma_eps`** (bounds
   [0.02, 0.5], `params.EXTRA_PARAMS`; every theta vector carries sigma_eps after the 33 parameters, fixed unless
   freed). Diagnostic A shows that the exit rate does not respond to sigma_eps: it stays fixed at 0.05.
7. **`--tie a=b`** (b = a, b not free); kept as an option only, not applied (PI: race heterogeneity is reported).
8. `hpc_job_a.py`: reproducibility = moments within relative 1e-6 (`inputs/expected_start_moments.csv`) or Q within
   relative 1e-3; `EXPECTED_Q = 11,726.0` (2026-10-19: the extended start, persistent CPS flows, solver fix at the
   SNAP asset limit, husband's employment reported only); one LM iteration in `--test` (45 minutes); new submission
   lines.

## Follow-ups 2026-10-19 (details in `results/diagnostics_20261018.md`, section 'Follow-ups')

1. **Solver at the SNAP asset limit** (check 0 failed after the kappa_S start fix): grid nodes at L and L + 1e-5
   (`model.ASSET_EPS`, `Model.jL`), the corner a' = L in `env_query` and the EGM kernels, a two-branch EGM where the
   endogenous grid falls only at the drop, a 9-point search with up to 6 Newton steps where the marginal value rises.
   Check 0 passes at the start and at kappa_S = 0 and 2.64; check 3 excludes the asset-test notch.
2. **Persistent CPS flows** (default `--cps-persist on`): `cps_entry_p_*`, `cps_wife_exit_p` from IGE/60 and the
   same filter in `panels.cps_samples` (two months of the old status before the transition, two of the new status
   after it). The Poterba-Summers correction stays as `--cps-persist off --cps-classif on`.
3. **Husband's employment** `psid_hemp_B/W` in `moments.OBJ_EXCLUDE` (husbands leave work only by displacement).

## Model extensions (PI-approved Fable decisions, 2026-10-18 evening; evidence in `results/diagnostics_20261018.md`)

Each behind a flag of `estimate.py` (`--<name> on|off`, defaults `estimate.EXT_DEFAULTS`), added one at a time and
evaluated at the analytic start on the same trimmed moment set and weights (step table in the note):

| Extension | Flag (default) | Parameter | Code | Step result at the start |
|---|---|---|---|---|
| CPS classification error in the entry and exit rates (Poterba-Summers 1986 Table II, women 25-59; chosen because sigma_eps does not move exits) | `--cps-classif` (on) | none (coded input `moments.CPS_CLASSIF_PS86_W2559`) | `panels.cps_samples(classif=)`, `moments.compute(cps_classif=)` | exit 0.0026 -> 0.0243 (data 0.0261), her exits Q 40,884 -> 259; entry overshoots (0.043 -> 0.193 White) while employment is 0.95 at the start |
| Memory of displacement: a spouse's hazard x (1 + c_mem) while the other is non-employed and UI-entitled | `--cs-memory` (off) | `c_mem` [0, 50] | `model.py` outcome tables, `simulate.py` kernel | joint-loss Q (monthly + annual) 177 against 62 for the type moved along the CPS ridge to p_H = 0.02 (no new parameter): not adopted |
| Couple type on the CPS ridge at p_H = 0.02 (start value) | (start) | p_H, m_H (estimated) | `analytic_start.P_H_START` | annual excess 0.118 -> 0.071 (data 0.063), joint-loss Q 236 -> 62 |
| Borrowing wedge 8.4 points a year (G.19 real credit-card rate 11.4% 1995-2021 - 3%) | `--borrow-wedge` (on) | none (`inputs/borrowing_wedge.json`, `borrowing_wedge.py`) | `solve.py` (EGM cash on hand and marginal value), `simulate.py`, `model.py` (terminal value, grid node at 0) | Q 68,086 -> 64,657; young debt share 0.80 -> 0.48 (data 0.57); 45-59 still too few at or below zero |
| Accumulation falling in the level, pi_up x (level/4)^(-eta_up) | `--hc-eta` (on) | `eta_up` [0, 3], start 0.5 | `model.py` | wage-growth block 158 -> 150 at 0.5 (109 at 2.5 with pi_up rescaled); raises employment at given preferences |
| Husband's employment rate by race (target) | (targets file) | none | `IGE/60` (`psid_hemp_B/W`), `moments.py` | data 0.882 / 0.943, model 0.999 / 1.000: z 22-23, Q +1,036 |
| Race ties | `--tie` (not applied) | | | |

New start (`analytic_start.py --ext hc_eta --eta-start 0.5`): p_H 0.02 / m_H 15.95 on the ridge (deltas rescaled),
eta_up 0.5 with pi_up divided by the entry-level mean of (level/4)^(-0.5) (1.051 wives, 1.019 husbands), the wage
process re-mapped at these pi_up (p_eps_w 0.00879 -> 0.00905, p_eps_h 0.00397 -> 0.00407). Q at the new start
90,377.5 over 87 moments (her search 82,169: the classification-corrected entry rates at 95% employment), 31 free
parameters. Weights: `inputs/moment_noise.csv` keeps the simulation noise of the pre-extension start (the noise at the
extended start inflates the entry rates' simulation s.d. sevenfold because spurious entries dominate when true
non-employment is 5%); recompute it at the LM estimate before CMA-ES (`Joint-noise` line in `hpc_job_a.py`).
Test 0 (EGM vs brute force) now fails at the current start values (99th pct 3.4e-3, max 0.16): the cause is the
kappa_S start fix of 20:16 (SNAP take-up kink), not these changes; with kappa_S = 2.64 it passes as before (4.5e-5).
Test 5 now sets m_H = 1 (its delta_w = 0.01 override gave the new start's rare type 16% monthly hazards) and passes
marginally at the interior point (just lapsed minus still entitled +0.000, n = 265).

## Extensions 2026-10-19 (pre-built, OFF by default; step table and design in `results/extensions_20261019.md`)

| Extension | Turn on | Parameter (start, bounds) | Targets (IGE/66 -> `output/paperA_targets_ext.csv`) | Start: Q on the same 89-moment set |
|---|---|---|---|---|
| New-job exit hazard: wife state EN (job < ~1 year, graduation 1/12 a month, `--set-fixed nj_grad=`); exit = quit, or displacement with UI if `--set-fixed nj_ui=1` | `--new-job on` | `xi_nj` (0.02, [0, 0.2]) | SIPP persistent exit by tenure 0-5 / 6-11 / 12+ months (0.0206 / 0.0160 / 0.0068, bootstrap s.e.); reported: SIPP 12-month return 0.530, PSID repeat-exit share 0.324 | 13,232.5 -> 13,245.7 (solve +41%) |
| Separation after HER displacement: + sigma_Jw while she is UI-entitled | `--her-sep on` (`--her-sep-tie on`: sigma_Jw = his sigma_J(r)) | `sigmaJw` (0.01, [0, 0.1]) | still with baseline husband, years 1-3 after her displacement, attrition-equalised (IGE/65 5b): -0.050 (0.012); reported: years 4-6 -0.094 | 13,232.5 -> 13,162.8 (no cost) |

- A flag on adds its parameter to the free set and merges its rows of the extension targets file (target = 0 rows are
  reported only, outside the objective). `--ext-targets new_job her_sep` adds the targets without the model feature (the
  base model on the extended moment set: compare steps on one moment set). Run e.g.
  `estimate.py polish --start <gn>/best.json --new-job on --ext-targets her_sep ...`; on the HPC the same flags go
  after `hpc_job_a.py polish`. The noise file has no rows for the new moments (var_sim = 0, weights 1 / se^2) until a
  noise run with the flag on is saved.
- The parameters live in `params.LATE_PARAMS`, after sigma_eps in every theta vector (`estimate.NAMES`, 36 entries);
  `PARAMS` / `N_PARAMS` (33), the default free set and the indices of earlier vectors are unchanged; `pad_vec`
  completes old 33- or 34-entry vectors with the nested values 0.
- Flags off = the committed base model bit for bit under the same numba compilation (test 12; note: a clean build of
  the committed code gives Q 11,733.7, not `EXPECTED_Q` 11,726.0, which came from this PC's earlier numba cache;
  Stanage gave 11,733.6; details in the note).

## Results (2026-10-18, real inputs: IGE/62 entry couples 12,360 x K = 3, fixed inputs, verified IGE/61 schedules)

### Evaluation time and the objective at the analytic start (`results/evaluate_20261018_145333/`)

One evaluation at the default size: **78 s on 2 threads** (solve 55 s for 8 problem-solves, simulation 8.5 s for
37,080 couple-copies, moments 13 s); 42 s on 8 threads. Under full load on this PC (8 workers x 2 threads) a CMA-ES
generation of 16 takes ~4.7 minutes (~140 s per evaluation). Worker memory ~1.6-3 GB.
**Q(start) = 76,113** with all 91 moments finite. By block: her exits 51,403 (CPS exit 0.0025 vs 0.026: at the start
values a wife with a job almost never leaves it), her search 16,500 (CPS entry 0.051 vs 0.075; SIPP build-up too
fast), employment levels 3,307 (wives' employment 0.95 vs 0.81; part-time share 0.22 vs 0.34), wealth 2,529, his
search 932, safety net 674 (no food-stamp take-up: kappa_S start 2.64), joint loss annual 283, base hazards 205,
wage growth 185; the monthly joint-loss block (32), separation (3.5) and consumption (15) fit at the start.
Simulation noise (`results/noise_20261018_151553/`): Q across 5 CRN seeds 76,381 +- 398 (0.5%; below the plan's 2%
rule, so K = 3 suffices).

### Staged tests (`results/tests_20261018.txt`; test size: 5 levels, 30 assets, one era; ~20 minutes)

| # | Check | Result | Numbers |
|---|---|---|---|
| 0 | EGM vs brute force over a' with the same W representation | PASS | Hermite: median 1.2e-7, 99th pct 4.4e-5, max 5.1e-4; chords (stage 3): 99th pct 1.4e-3, max 3.0e-3; V(t = 0) vs 90-point Hermite: median 0.021 (chords 0.448) |
| 1 | flat consumption, no risk, beta(1+r) = 1 | PASS | max relative deviation 1.2e-7 over 420 months |
| 2 | precautionary buffer rises with hazards | PASS | mean assets 34.6 / 44.4 / 49.6 thousand $ (no risk / start / x2) |
| 3 | wife's work falls with assets, rises after his loss | PASS (interior point) | work-cost shift 0.572; no monotonicity violation; response +0.06 to +0.95 |
| 4 | search friction lengthens non-employment | PASS | mean spell 4.87 (1/lambda 5), 9.71 (10) |
| 5 | exits rise when UI lapses (new rule) | PASS | interior point: exit to work entitled 0.088 vs not 0.126; just lapsed 0.106 vs still entitled 0.078; q_UI = 0 raises exits in months 1-6 from 0.110 to 0.120; entitled wives decline 33% of offers (10% at the start values, where wives almost always work) |
| 6 | independence with pi_c = 0, m_H = 1 | PASS | ratio 0.987 (s.e. 0.040) |
| 7 | joint-loss probabilities vs closed forms | PASS | max abs z 2.25 over 30 moments |
| 8 | sigma_eps smoothness profile | information | non-monotone EGM grids 0.21 at the median state for every sigma_eps (the floor kink) |
| 9 | grid accuracy | information | 5 levels move mean assets 34%, 20 assets ~1% (vs 7 x 30) |
| 10 | measurement layer (new) | PASS | twfe = IGE/60 TWFE to 4.4e-15; 91 / 91 targets finite, no empty sample; CPS entry rate all rotation offsets 0.0459 vs one literal 4-8-4 window 0.0303 (z = -1.6) |

### Jacobian at the analytic start (`results/jacobian_20261018_145353/`, 61 CRN evaluations, 21 minutes)

Central differences, step 5% of the value (5% of the bound range would cross the bound for parameters like
pi_c0 = 3.5e-5 with range 0.01); S reported per 10% of the value and per 10% of the bound range (the plan's units).
- **Condition number on the plan's range scaling 2.5e4, entirely from kappa_S**: with the start value 2.64 there is
  no food-stamp take-up at all, so its column is flat (norm 0.02). **Without kappa_S the condition number is 162**
  (criterion < 1e4). kappa_S's start value must come down before the HPC run (e.g. to give positive take-up among
  eligibles); this is a start-value problem, not an identification failure.
- Range-scaled weakest directions after kappa_S: pi_dn_h with d_h (sv 1.9), lam_h_B with lam_h_W (2.2), sigmaJ_B
  (2.5), F (3.5); all others above 4.9 (largest 308).
- Near-collinear pairs (|corr| > 0.9): lam_w_W with theta_05 (-0.95), theta_617 (-0.94), F (-0.90); theta_05 /
  theta_617 (+0.97); theta_05 / F, theta_617 / F (+0.94, +0.92). All of them move one moment most:
  `cps_entry_pooled` (s.e. 0.0003). This is plan item 2.3.4 (search friction vs acceptance); the SIPP build-up and the
  employment levels by child age are the separating moments, but under diagonal weights the CPS entry rates
  dominate the columns.
- Primary moments as the plan expects: delta_w -> CPS wife's hazard (by race), delta_h -> CPS husband's hazard (T7),
  pi_c0 / pi_c1 -> CPS same-month excess by match, lambda_w -> CPS entry by race, lambda_h -> SIPP re-employment,
  phi_F / phi_h -> part-time shares, a_bar -> liquid-wealth shares. pi_up, theta, F, sigma_0 load most on the CPS
  entry rates (diagonal weights).
- Norm < 3 per 10% of the value: pi_c0 (0.8), pi_c1 (1.1), lam_h_B (2.0), pi_dn_w, pi_dn_h, d_w, d_h (0.5-1.7),
  theta_05 (start value 2e-4), theta_617, F, kappa_S, sigmaJ_B, sigmaJ_W (0.5). On the range scaling every column but
  kappa_S has norm > 5.

### Pseudo-data recovery (targets = the model's moments at the analytic start, same CRN seed; start = truth + N(0, 0.5) in logistic units; popsize 16, 8 workers x 2 threads)

- **Closed-form set** (`results/runs/recovery_closed_20261018_151959/recovery_report.md`): 19 free (the 21
  closed-form parameters less pi_c2, which is inactive at the default size, and p_H, held at the ridge point), 31
  generations (496 evaluations, 152 minutes). Q fell from 2,907 to 482 (0 at the truth) and was still falling; the
  search had not converged. Within 2 simulation-noise s.e. of the truth: 3 of 19 (sigmaJ_B, lam_h_B, lam_h_W); within
  2 data s.e. (sandwich with the bootstrap covariance): 8 of 19. Largest misses: sigma0_B (-10 data s.e., with
  sigmaJ_W +4: the separation block trades baseline against response), pi_up_w (+8), delta_w_B (+7), d_w (+7),
  delta_h_W (+6), m_H (-4).
- **All free parameters** (`results/runs/recovery_all_20261018_181911/`): **superseded, do not resume or cite**. It was started at an obsolete start (kappa_S = 2.64, above its upper bound 1.0, so the pseudo targets had zero SNAP receipt; delta_h from the PSID annual rates) and stopped after 352 evaluations (best Q 3,179).
- Reading: 30 generations are far too few for 19-30 parameters (CMA-ES needs a few thousand evaluations here); the
  recovery now runs by Levenberg-Marquardt (`Joint-recovery-gn`, below). The simulation-noise
  s.e. are very small (37,080 simulated couples), so 'within 2 noise s.e.' is a strict criterion that only a
  converged search can meet.

### BPS check (7) and the wage-process correction

`bps_check.py` wires the simulated couples (income years 1998-2008) through `sim_panel_writer` (with the gross-error
mixture) and `bps_on_sim.do`, reads BPS Table 3, and computes the plan's one-time correction (sigma_nu^2 = max{0.5 s2,
2 s2 - hat}, p_eps and p_c rescaled by target / recovered permanent (co)variance; the lead's choice to rescale the
permanent probabilities). It writes `inputs/wage_process.json` only with `--apply` (re-running `analytic_start.py`
afterwards overwrites the correction). BPS_RUN_PLACEHOLDER

## How to run (PC)

```
.venv/Scripts/python.exe paperA_model/analytic_start.py              # start values + wage process from the inputs
.venv/Scripts/python.exe paperA_model/tests/run_all.py               # staged checks (~20 min)
.venv/Scripts/python.exe paperA_model/estimate.py evaluate           # Q at the start, by block (78 s)
.venv/Scripts/python.exe paperA_model/estimate.py jacobian --workers 8 --threads 2      # ~21 min
.venv/Scripts/python.exe paperA_model/estimate.py noise --reps 5 --workers 4 --weighting diag --save-noise-input
.venv/Scripts/python.exe paperA_model/estimate.py polish --workers 7 --threads 2 --iters 15   # LM from the start
.venv/Scripts/python.exe paperA_model/estimate.py run --pseudo --free-set closed --workers 8 --threads 2 --maxfevals 480
.venv/Scripts/python.exe paperA_model/recovery_report.py <run dir> <jacobian dir> <noise dir>
.venv/Scripts/python.exe paperA_model/bps_check.py [--apply] [--sigma-nu-zero]      # needs Stata
```
**Local SMM (8 workers x 2 threads, resume-able):**
```
.venv/Scripts/python.exe paperA_model/estimate.py run --workers 8 --threads 2 --maxfevals 8000
.venv/Scripts/python.exe paperA_model/estimate.py run --resume paperA_model/results/runs/smm_<stamp> --workers 8 --threads 2
```
`es.pkl`, `evals.csv`, `generations.csv` and `best.json` are written every generation. At ~4.7 minutes per
generation, 500 generations take ~39 hours on the PC: the main runs belong on the HPC.

## HPC (Stanage): Paper A's own environment `~/joint`

PI decision: a separate clone `~/joint` of the same repository (next to `~/svr` and `~/ige`), its own `.venv`, results
in `/mnt/parscratch/users/$USER/joint_smm_results`; nothing under `~/svr`. The PI submits (password + Duo).
1. **One-time setup, idempotent**: paste the block at the top of `hpc_job_a.py` on the login node. It checks whether
   `~/joint` is already a clone of the repository (`git -C ~/joint remote -v`; then it pulls), clones into it if it is
   missing or empty, stops with a message if it is non-empty and not a clone, creates `.venv` (uv, Python 3.12.13) only
   if missing, installs `requirements.txt` (numba, cma, scipy, pandas, statsmodels), and creates the results folder.
2. **Entry couples** (git-ignored, PSID terms): copy once, and whenever IGE/62 rewrites them, from Git Bash or
   PowerShell on the PC (your Stanage username in place of cm1jil); every job checks the file and stops with this
   command if it is missing:
   `scp "G:/My Drive/JointLoss/paperA_model/inputs/psid_entry_couples.csv" cm1jil@stanage.shef.ac.uk:~/joint/IGE/paperA_model/inputs/`
3. **Jobs** (from `~/joint` after `git pull`; job names `Joint-*`; 32 cores, `--threads 2` = 16 workers, 64G, email
   at begin / end / failure in the `#SBATCH` header):

| Job | Command |
|---|---|
| 0 test (45 min) | `sbatch --job-name=Joint-test --time=00:45:00 paperA_model/hpc_job_a.py --test` |
| 1 LM recovery, all free | `sbatch --job-name=Joint-recovery-gn --time=05:00:00 paperA_model/hpc_job_a.py polish --pseudo --label all --start-noise 0.5 --iters 15 --push` |
| 2 LM on the data | `sbatch --job-name=Joint-gn-main --time=05:00:00 paperA_model/hpc_job_a.py polish --label main --iters 15 --push` |
| 2b noise at the LM candidate | `sbatch --job-name=Joint-noise --time=00:30:00 paperA_model/hpc_job_a.py noise --start <gn>/best.json --reps 5 --weighting diag --push` (then `--noise-file <noise dir>/moment_noise.csv` in 3 and the final polish) |
| 3 CMA-ES around the LM candidate | `sbatch --job-name=Joint-smm-main --time=12:00:00 paperA_model/hpc_job_a.py run --label main --start <gn>/best.json --cma-stds-from <gn>/jacobian.npz --sigma0 0.2 --maxfevals 3500 --tolfun 30 --cma-seed 1 --push` |
| 3b restart 2 | same with `--job-name=Joint-smm-main-s2 ... --label main_s2 ... --cma-seed 2` |
| 3c restart 3 | same with `--job-name=Joint-smm-main-s3 ... --label main_s3 ... --cma-seed 3` |
| independent shocks | `sbatch --job-name=Joint-gn-indep --time=05:00:00 paperA_model/hpc_job_a.py polish --label indep --fix pi_c0=0 pi_c1=0 pi_c2=0 m_H=1 --push` |
| resume (CMA) | `sbatch --job-name=Joint-smm-main-r --time=12:00:00 paperA_model/hpc_job_a.py --push --resume /mnt/parscratch/users/$USER/joint_smm_results/runs/<run dir>` |
| Jacobian | `sbatch --job-name=Joint-jacobian --time=01:00:00 paperA_model/hpc_job_a.py jacobian --start <best.json> --push` |
| standard errors | `sbatch --job-name=Joint-se --time=01:30:00 paperA_model/hpc_job_a.py se --start <best.json> --push` |
| block weights | `sbatch --job-name=Joint-smm-block --time=12:00:00 paperA_model/hpc_job_a.py run --label block --weighting block --start <gn>/best.json --sigma0 0.2 --maxfevals 3500 --push` |
| push only | `sbatch --job-name=Joint-push --dependency=afterany:<job> --time=00:10:00 --cpus-per-task=1 --mem=2G paperA_model/hpc_job_a.py --push-only <run dir>` |
| queue | `squeue -u $USER -o "%.10i %.24j %.8T %.10M %.6D %R"` |

`<gn>` is the `Joint-gn-main` run folder under `/mnt/parscratch/users/$USER/joint_smm_results/runs/`. `--time`
sizing: LM: per iteration one Jacobian (61 evaluations = 4 rounds of 16) + one round of trial steps, 15 iterations +
final Jacobian + s.e. ~ 80 rounds x ~2.3 min ~ 3.1 h -> 5 h; CMA-ES: one round per generation, 3,500 evaluations =
219 generations ~ 8.4 h -> 12 h (the job stops itself 15 minutes before the limit and pushes; a CMA run resumes with
`--resume`, an LM run restarts with `--start <run>/best.json`). Memory ~1.6-3 GB per worker x 16 + the parent < 64 GB
(`PEAK_GB` guard). The `--test` reproducibility values (`EXPECTED_Q = 11,726.0` and
`inputs/expected_start_moments.csv`: the extended analytic start with the default extensions and persistent CPS flows,
the trimmed 85-moment objective and diag_noise weights, inputs and targets of 2026-10-19 06:40) must be updated when
the code, the inputs or the targets change. Results come back through `--push`
(aggregate files of each run into `paperA_model/results/hpc_runs/<run>/`, committed on main and pushed from
`~/joint`; `git pull` on the PC) or by scp of the run folder. The changed files (`estimate.py`, `moments.py`,
`params.py`, `model.py`, `solve.py`, `simulate.py`, `panels.py`, `analytic_start.py`, `borrowing_wedge.py`,
`bench.py`, `hpc_job_a.py`, `recovery_report.py`, `tests/`, `inputs/start_analytic.json`, `inputs/wage_process.json`,
`inputs/moment_noise.csv`, `inputs/expected_start_moments.csv`, `inputs/borrowing_wedge.json`, and
`IGE/60.PaperATargets.py` with `output/paperA_targets*.csv`) must be committed before the first job.

## Measurement layer: approximations to know (details in `panels.py`)

- After a separation the husband leaves the model: his hours, earnings and food stamps are missing in the PSID rows
  after the separation ('still with wife' = 0 stays). His displacements after the separation are imputed from his
  hazard (CRN), only to date his first displacement, so that separated couples are not mistaken for clean controls
  (without this the separation response came out with the wrong sign).
- Husband's age = wife's age + 2 (wage growth by his age); same sector (16 sectors, PSID) = workplace match s >= 1.
- CPS: the 4-8-4 rotation is taken over every entry month (all couple-month transitions, equal weights): the
  expectation of the CPS sampling; state x month FE -> calendar-month FE; a displaced wife who does not look is out
  of the labor force (not a job loser; an exit).
- SIPP: separation month = the first model month without work after a displacement; full months without a job =
  model non-employed months - 1; the three panel windows applied to every couple-copy.
- PSID consumption: the interview month's flow x 12 plus BPS's measurement error (variance 0.0332), waves 1999-2021.
- Stacked designs: control units are a CRN subsample (15%) of the clean controls (unbiased; keeps the panels near
  the data's size).

## Open issues for the lead

1. **Pooled CPS moments double count**: resolved 2026-10-18 evening (excluded from the objective, kept in the fit
   tables; `moments.OBJ_EXCLUDE`).
2. **kappa_S start value**: resolved 2026-10-18 (the analytic start now values the benefit at u'(c_ref) like the other
   start values: 0.104 instead of 2.64, which gave zero SNAP receipt and a flat Jacobian column).
3. **SIPP 'no separation' comparison moments** (`sipp_his_emp_s*_nosep`): excluded from the objective
   2026-10-18 evening (husbands never quit; the model gives 0.989 against 0.983 at every theta); kept in the fit
   tables.
4. **Wives' exits**: the target is now the persistence-filtered CPS exit (0.0101 a month; the one-month 0.026 is
   in the fit table only). The model gives 0.0014 at the start (z -69, Q 4,622 of 11,726) and is the largest miss,
   followed by employment levels. Evidence on why wives exit: proposals/wife_exit_evidence.md (WP1, 2026-10-19).
   The model feature it points to is a PI decision after the first estimate. Intake: results/INTAKE.md.
5. Recovery needs the HPC (above). The BPS correction should be applied (`bps_check.py --apply`) before the main run
   if the lead wants the corrected wage process in estimation.

## Sizes, runtime and memory (stage 3 benchmark, 2 threads, this PC; synthetic population)

`bench.py` (results in `results/bench_2t.json`): one problem-era solved over 420 months on 2 threads with storage, then
5,000 synthetic entry couples x 3 copies simulated. Since stage 4 the default solve takes 6.1-7.7 s instead of 3.9 s
(Hermite values and polish, offer node) and the stored solution is 1.24 GB (offer index added); with the real entry
file and the moments one evaluation is 78 s (above).

| Size | Switches (plan 4.4) | States / month | s per solve (sep / expect / EGM) | Solves | Sim s | **s per evaluation** | Stored GB | Peak RSS GB |
|---|---|---:|---|---:|---:|---:|---:|---:|
| full | spec: 7 levels, s = 0/1/2, 3 eras, 30 assets, lost hours | 211,680 | 6.17 (0.36 / 1.07 / 4.73) | 36 | 2.8 | **226** | 1.45 | 2.07 |
| a_hc5 | (a) 5 levels | 108,000 | 2.82 | 36 | 2.4 | **105** | 0.74 | 1.26 |
| b_hc5_s2 | (a)+(b) merge s = 1, 2 | 108,000 | 2.81 | 24 | 2.5 | **70** | 0.74 | 1.26 |
| c_hc5_s2_era1 | (a)+(b)+(c) one era | 108,000 | 2.84 | 8 | 2.4 | **25** | 0.74 | 1.25 |
| d_hc5_s2_era1_a20 | (a)-(d) 20 assets | 72,000 | 1.79 | 8 | 1.7 | **16** | 0.50 | 1.00 |
| e_all | (a)-(e) no lost hours | 54,000 | 1.49 | 8 | 1.8 | **14** | 0.41 | 0.92 |
| j_hc5_s2_a20 | (a)+(b)+(d), 3 eras | 72,000 | 1.83 | 24 | 1.8 | **46** | 0.50 | 1.01 |
| **k_s2_era1_a20 (default)** | 7 levels, (b)+(c)+(d) | 141,120 | 3.88 (stage 4: 6.1-7.7) | 8 | 2.3 | **33 (stage 4 with moments: 78)** | 0.97 (1.24) | 1.48 (1.9) |

Full model at stage 4: 14 s per solve, ~510 s per evaluation (36 solves).

## Specification issues resolved in the code

1. (Stage 3: UI could not affect acceptance.) **Resolved by the lead's decision 1 above.**
2. **Common shock and a wife who holds a job but chooses zero hours**: she quits that month and is not hit by the
   common shock, so she gets no UI.
3. **Consumption floor with borrowing**: cash on hand is max{X_pre, sc c_min - a_bar} (the floor pays interest on debt
   at the limit; it does not repay debt).
4. **HSV tax floored at zero** (EITC and SNAP enter separately).
5. **Equivalence scales** e(k) = 1 + n(k, age, r) x share(k); c_min = AFDC-3 / (s_M e(1)) with n = 2.
6. **Child chain**: P(0-5 -> 6-17) = (1/72)(1 - b_2); P(6-17 -> none) = (1/144)(1 - b_2).
7. **Terminal value**: Social Security 40% of each spouse's full-time earnings at the final level.
8. **SNAP asset test** on beginning-of-month assets.
9. **Separation timing**: hazard on the husband's status next month, after the other transitions; assets halved.
10. **Human capital** steps and truncation as listed in the stage-3 notes (displaced: loss only; quitter:
    depreciation; shared before idiosyncratic innovation).
11-13. Fallback sizes: five levels rescale psi and grid-unit parameters; no lost-hours record uses a 0.835 factor;
    merged s = 1, 2 uses pi_c1 for both.
14. **Eras**: switch in January 1997 and 2009 (unexpected); one-era mode uses 1997-2008 everywhere.
15. **Transitory pair** drawn at entry; separated wife +-sigma with probability 1/2.
16. **Couple type** tau = 1{CRN uniform < p_H}.
17. **Money units**: thousands of 2000 $ a month; sigma_eps = 0.05.
18. **q_UI** = 0.493 for both spouses.
19. **Start values for preferences** ignore human capital and job-loss risk (wives with a job work in ~95% of months at
    the start); start values only.
20. **T7** is in the targets file (CPS husband's hazard, Black 0.0063, White 0.0034, pooled 0.0037) and is a target
    in `moments.py` (the 'tau' sample's husband job-loss rate). `analytic_start.py` reads `cps_h_hazard_{B,W}` for the
    delta_h start values when present (it was appended after the start values used by the Jacobian and the
    recoveries above, which therefore start delta_h from the PSID annual rates).
21. **Offer node timing** (new): the entitled wife decides after both spouses' end-of-month labor events, before the
    human capital, child, separation and transitory draws, at her end-of-month assets.
22. **'Looking for work'** (new): entitled wife: offer-node index > 0 at her end-of-month assets with the husband's
    status unchanged; otherwise P(positive hours | she had a job this month) > 1/2.

## Placeholders remaining

- IGE/62 inputs are in (entry couples, wage levels and steps, child process, n(k, age, r), childcare price, match
  shares, a_bar start); IGE/61 schedules verified. Remaining: the wage process is the plan's closed forms at the new
  psi (the BPS correction not yet applied); sigma_J uses D_r = 5 months; lambda_w uses an assumed acceptance of 0.6.
