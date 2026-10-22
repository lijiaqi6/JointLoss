# Code review of the Paper A model (2026-10-23)

Read-only review of `paperA_model/` (params, model, solve, simulate, panels, moments, estimate, post_common,
counterfactuals, bench, tests 0, 9, 11, 12) plus the stored outputs of this week's runs (`results/evaluate_*`,
`results/runs/polish_hcage1_*`, `results/bench_2t.json`, inputs). Nothing was run; every claim below is tied to the lines
read, and the one estimation-layer bug was confirmed from the run's own `evals.csv`. Severity: (A) wrong results,
(B) fragile or latent, (C) efficiency, (D) model advice.

## 0. Ranked findings

| # | sev | where | what | fix |
|---|---|---|---|---|
| 1 | A | `estimate.py:589-599` (`jacobian_at`) | The finite-difference step of **beta** is 5% of its value = 0.05 a month, i.e. six times its whole bound range; after clipping, the "central" difference is the secant from beta = 0.90 a year to 0.995 a year. Confirmed in `runs/polish_hcage1_20261022_200222_p3920/evals.csv`: the two beta evaluations of every Jacobian sit at 0.99125839 and 0.99958238 = LO and HI. The beta column of G, Gz, the LM step in the beta direction, the sandwich s.e. of beta (0.00009 a month) and `--cma-stds-from` are all built on it. | `hs = np.minimum(hs, 0.05 * rng_)` (or any rule in range units for parameters whose value is far from zero: beta, m_H); re-run `se` at `restr`; expect LM to need less damping. |
| 2 | B | `estimate.py:150-157, 945` + `F` at 0.6 | In logistic coordinates a parameter at a bound has `dtheta_dz ~ 1e-4 x range`, so its Gz column is ~0: LM can never bring F (or d_h, pi_dn_w) back from a bound, and `cond(G'WG)` of 1e7-1e10 is this scaling, not weak identification (the condition number jumps 4e7 <-> 1.5e10 as F touches the bound). | Report cond of the column-normalised A; replace the logistic by box-constrained Gauss-Newton (projected step, active set), or at least `--z-cap 6`. |
| 3 | B | `bench.py:81-96` | `sim_kernel` is called with 7 trailing arguments; the kernel now takes 13 (`EN_, xinj, gnj, njui, sjw, dwS` added 2026-10-19). `bench.py` raises TypeError; the timing table in README cannot be refreshed. | Pass the six extension arguments (-1, 0.0, 1/12, False, 0.0, m.dw). |
| 4 | B | `estimate.py:761-762, 731-738` | `--resume` and `--cma-stds-from` take integer `idx` from `run.json` / `jacobian.npz`. Vectors of earlier layouts (34, 36, 37 entries) are padded by name (`pad_vec`), but the indices are not remapped: in a 36-layout run index 34 was `xi_nj`, today it is `beta`. | Map by `run["free"]` / `J["names"]` (both are saved) instead of the stored integers. |
| 5 | B | `solve.py:466-477` vs `simulate.py:450, 626` | The solver values the separated wife at a'/2 (hard-coded 0.5 in `k_half`), the simulator uses `fx["sep_asset_share"]` (0.5). Consistent today; silently inconsistent if the input is ever changed. | Build `half_j/half_w` in `model.py:596-600` from `fx["sep_asset_share"]`. |
| 6 | B | `model.py:591` | The separated wife's terminal value annuitises debt at the saving rate (`af`), the married couple's at the borrowing rate (`af_b`, line 582). With `borrow_wedge` on (default) the two terminal values treat the same debt differently. Tiny (retirement debt is rare). | Use `np.where(a < 0, af_b, af)` in the VST loop too. |
| 7 | B | PC runs, `estimate.py` (cf. `hpc_job_a.py:379`) | On the PC the numba cache lives in `paperA_model/__pycache__` on Google Drive; the HPC job sets `NUMBA_CACHE_DIR` to local scratch. The 2026-10-22 crash (six processes compiling at once) is this. | `os.environ.setdefault("NUMBA_CACHE_DIR", <LOCALAPPDATA>/paperA_numba)` at the top of `estimate.py`/`post_common.py`, before numba is imported. |
| 8 | B | `inputs/moment_noise.csv` | The `diag_noise` weights use simulation variances from `noise_20261018_205236` (analytic start, pre-BPS inputs). Not a bug, but var_sim at the current estimate differs (Q band was 1,355-1,409, now 1,694-1,748 at step 2). | Re-run `noise --save-noise-input` at the reference estimate once per moment-set change (a new noise file is a new objective: re-baseline). |
| 9 | B | `panels.py:104-113` vs `simulate.py:341` | CRN slot 23 is used by the kernel with model month t and by `_post_sep_disp` with calendar month m. For couples with negative `m_off` (entered 1984 above age 25) a post-separation imputed month m can equal a pre-separation model month t of the same couple. Harmless (different years, hazards ~0.003), but a slot reuse. | Use a free slot (e.g. 45) in `_post_sep_disp`. |
| 10 | C | timing | One evaluation under load: solve 182 s of 223 s (82%), simulation 16 s, moments 23 s (`evaluate_20261022_200106`). Unloaded bench: 3.9 s per solve pre-Hermite (~6 s with it) x 8 = ~50 s; under 6-7 concurrent processes it is 23 s per solve, a 3-4x slowdown. Inside a solve: EGM 76%, expectations 17%, separated wife 6%. | See Section 4: Broyden updates + forward differences (LM iteration 37 min -> ~12-15 min), worker/thread test, local numba cache, `sol.timing` aggregated into `evaluate.json`. |

Nothing else of severity A was found. The core (budget, transfers, transitions, CRN, moments, objective, sandwich) is
consistent between the solver, the simulator and the paper's equations; details in Sections 2-3.

## 1. Priority 1: this week's changes

### (a) beta as an estimated extra

Path verified: `estimate.model_moments` (251-257) pops every extra out of theta into `fx` -> `simulate(fixed=fx)` ->
`Model.__init__` reads `fx["beta"]` (model.py:131) -> `m.beta` is passed to `k_egm_sep` (solve.py:1126), `k_egm` (1145),
the terminal discount `disc = (1 - beta^Rm)/(1 - beta)` (model.py:570), `node_derivs` (1168), the simulator
(`simulate.py:625`, used at 169/205/272/298 to recover D), and `alternatives` (1182). `post_common.evaluate` and
`simulate_only` (153-189) do the same pop, so `counterfactuals.score` (147) and `fit_table` see the estimated beta.
`jacobian_at`/`se_block` perturb `th[j]` for j in idx, so beta is differentiated like any parameter. `start_theta`
(417-443): a `--start` json carrying beta wins over the fixed input, `--set-fixed beta=` wins over both; with
`--hc-age`/other flags unchanged. r_m stays the fixed input (model.py:133), so beta(1+r) = 0.979 a year at 0.95: fine.
`_init_worker` applies `set_fixed` to `fx` (244) and `start_theta` applies it to theta (432-434): consistent.

The only defect is finding 1 (step size). Note for the write-up: the LM estimate of beta (0.9498 a year at `restr`,
0.9412 at stage 1) is where damped steps left it, not an optimum in the beta direction; the profile (plan 4b) is the
evidence for ~0.948. After the fix, re-run `se` and let LM move beta.

### (b) pad_vec

`estimate.py:127-144`: lengths 33/34/36/37 map by name; 38 passes through. The 35-length layout (33 + sigma_eps + beta
without the late parameters) never existed (late parameters 10-19, beta 10-21), so the table is complete. Callers:
`model_moments` (254), `cma_stds_from` (733), `cmd_run --resume` (761), `post_common.evaluate/simulate_only` (158, 183):
all pass through `vec_dict(pad_vec(...))`. `dict_vec` (121-124) fills only the late names; a dict lacking an extra
raises KeyError, which every caller avoids (`start_theta` always carries both extras). Finding 4 is the remaining gap
(integer indices of old runs).

### (c) g_age

`model.py:246-267`: `up_age[g] = exp(-g_age x 5 x g)`, step matrices `(G, 4, H, H)` for both spouses from the wife's
group (intended), capped at 1; `Aw/Ah = AwG[0]` keeps test 11's `me.Aw[0][h, h+1]` meaningful (CAT_F matrix of
group 0). Sparse rows `(G, 4, H, 3)`. Timing: the solver at month t forms E_t[V_{t+1}] with `g = age_group(t)`
(solve.py:1116, 1121, 1138-1139) = the transition drawn at the end of month t; the simulator draws at the end of month t
with `gq = min(t // 60, 6)` (simulate.py:146, 425-427) = `age_group(t)`. Identical. Child process `Pk[g]` and income
tables `inc0[g]` follow the same convention (both sides). Separated wife: `k_sep_expect(... Aw_idx[g] ...)` and the
simulator's `Aw_idx[gq, cat_w, hw]` for mar = 0 too. With g_age = 0 all G slices are equal, which is why on/off give
Q 1,025.0406 bit for bit. `counterfactuals.py` touches only theta and Model overrides, never these arrays; `bench.py`
passes the 4-d arrays correctly but is broken for another reason (finding 3). Tests 0/9/12 build `Model` through the
same constructor, fine.

One design remark (Section 5): the husband's accumulation now falls with the wife's age, consistent with the panel's
convention "husband's age = wife's age + 2" (panels.py docstring), so the 2-year offset is absorbed in g_age.

### (d) log_evals retry

`estimate.py:525-538`: on OSError re-opens by `logf.name` in append mode and writes the line; a second failure prints
and continues. The original handle is kept for later lines (each later write retries the same way). Correct; the
counter is advanced before the write, so a dropped line leaves a gap in `eval` numbers, not a duplicate.

## 2. Priority 2: the core, what was checked and found consistent

- **Budget** (model.py:450-542, paper eq. `eq:budget`): gross = earnings + UI; HSV tax on annualised gross incl. UI
  (taxable, correct), floored at 0; EITC on earnings only, monthly on annualised earnings (as the paper states; the
  annual-accounting issue is already logged); SNAP: gross test, 20% earned deduction, standard deduction, dependent-care
  deduction = her childcare, 30% reduction, asset test on beginning-of-month assets (both solver 730 and simulator
  175); household size 2 + n (married) / 1 + n (separated); F per working spouse (500, 526); childcare only when she
  works; consumption floor `X = max(X_pre, sc c_min - a_bar)` with a zero derivative where it binds (767); borrowing
  wedge on negative beginning-of-month assets (734, simulator 177). UI: rho x base wage x lost hours, capped; the base
  wage is the *current* level's wage, so a displaced wife whose level fell by d_w draws a lower benefit than the law's
  base-period rule gives (small, noted for the paper, not a bug).
- **Separation**: hazard on next month's husband state (k_tilde 486; simulator 444 uses `lh2`), assets halved
  (finding 5), wife keeps k, level, labor state and transitory sign (k_tilde 504 / simulator 152, 159).
- **Human capital**: forward order own step -> shared -> idiosyncratic (simulator 425-440); backward order I_h, I_w, J
  then A_h, A_w (k_hc 571-618, k_husb, k_wife); separated wife A then Is (k_sep_expect) = simulator 440. CAT_D loss
  floor(d) + Bernoulli (own_step_matrix 59-63). Exact.
- **Displacement**: common shock then own hazards with m_tau (model 378-389; simulator 328-342 incl. the memory term
  c_mem on the entitled spouse, both sides); separated wife own hazard only (dwS, 422 / 630).
- **Search friction, UI**: offer -> accept/decline logit with the solver's index at end-of-month assets and the
  husband's realised slice (simulator 400-416 vs k_offer 964-997); expiry with 1/6 whether or not an offer came
  (model 353-356 vs simulator 416, 419); quit = not entitled (349 / 395-397); husband's events (358-365 / 347-368).
  Slot 28 and slot 26 are each used in two mutually exclusive branches; no slot serves two events in one month.
- **Taste shocks**: logsum + sigma x Euler in k_egm (781) = E[max] of the simulator's Gumbel draws (181); the offer
  node is mean-zero on both sides (988-992 / 410). DM = sum_d P(d) dv_d (782).
- **EGM**: Euler inversion `c = sc u'^-1(beta D sc)` (713) with D in beginning-of-month units (R inside dvs, 767);
  Hermite with Fritsch-Carlson limiting (97-122), Newton polish, top extrapolation, two-branch at the SNAP notch;
  simulator recovers D from stored c (169). Test 0 covers this against brute force.
- **CRN**: `u01` = splitmix64 finaliser of XOR-mixed products; slots 0-17 (alternatives: `(hw*3+hh)*2+S`, separated
  `hw*6+S` = the married alternative with hh = 0), 20-36, 40-44, 50-53. Unique per event except finding 9.
- **Moments vs data definitions** (panels.py): CPS job loser = displaced end of m-1 and looking in m (146); tau sample
  wife works in b, his loss at end of b (250-251); leads/lags, persistent flows (273-275); SIPP added-worker base
  (328), re-employment earnings with d = months without a job - 1 (336-349); PSID annual rows, interview April of
  wave Y+1, biennial after 1997, events dated by calendar year, control subsample by CRN (437); wealth at the April
  interview with the previous year's earnings (619-632); wage growth 2-year on the continuously employed (577-598);
  consumption with BPS measurement error (505). All as described in the docstrings.
- **Objective/weights**: diag_noise = 1/(se^2 + var_sim x K_noise/K) (moments.py:148-152), excluded ids zero weight,
  missing penalty 1,000 (190-196); block weighting scale-free (155-166). `psid_hemp_B/W` and the three SIPP `_nosep`
  rows are in `OBJ_EXCLUDE` (53-57): the husbands' employment level (model 0.99 vs 0.88/0.94) is **not targeted**.
- **LM**: Marquardt with diag scaling, 7 multipliers per round, accept-if-lower, mu x 1e4 on failure, stop rules
  (902-972); the Jacobian of an accepted point is recomputed at the end when needed (1059-1061); CRN seed shared
  across the Jacobian (600). **Sandwich**: (G'WG)^-1 G'W (V_data + V_sim) W G (G'WG)^-1 on the in-objective rows
  (850-864); V_sim from 5 seeds (rank 4, noisy but only inside Omega). Tied parameters follow their source in the
  perturbations (598).

## 3. Smaller latent points (B/C, no action needed now)

- `Solution.__init__` zeroes ~1.35 GB (C, W, Dlt) per problem-era with `np.zeros`, 8 times per evaluation; every
  month is written, so `np.empty` is safe (saves ~10 GB of memset per evaluation; a few seconds).
- `k_sep_expect` (solve.py:789) is serial; 6% of a solve. `prange` over `lw` would halve it on 2 threads.
- `simulate()` accumulates only `tim["solve"]`; `sol.timing` (sep/expect/egm) is dropped. Summing it into `tim`
  would put the split in `evaluate.json` under real load, where the bench numbers do not apply.
- `moments.compute`: `timing["moments"]` 23 s of which CPS+SIPP+PSID = 11 s; the other 12 s is `panels.records`
  (`_annual`, `_post_sep_disp`, the shift-based masks). Not worth touching before the solver.
- `SafePool.map` per-round deadline 5 x longest evaluation: fine; with 61 Jacobian evaluations on 7 workers the
  Jacobian takes 9 rounds, as observed (40 min per iteration).
- The 78/65/47/50/40/77 scripts: only skimmed. `78.ols_cl` (122-137) is a standard CR1 (G/(G-1) x (N-1)/(N-K)) with
  alternating-projection within transformation; nothing wrong seen. Not reviewed line by line.

## 4. Efficiency (C): where the 37-40 minutes per LM iteration go and what would cut them

Per iteration: 1 base + 2 x 30 Jacobian + 7 trial evaluations = 68, on 7 workers = 10 rounds x ~3.5 min. Under load
one evaluation is 223 s: solve 182 s (8 problem-eras x 23 s), simulation 16 s, moments 23 s. Unloaded, a solve is
~6 s (bench 3.9 s before the Hermite fix, +40-60%): the PC's 7 x 2 threads deliver about 2 unloaded processes' worth
of throughput. In order of payoff per hour of work:

1. **Fix the beta step** (finding 1). The beta column is the one LM distrusts most; the damping it forces (mu 10, steps
   of 0.006-0.01 in z, gains of 1-3 per iteration at hcage1 iterations 5-7) slows every other parameter.
2. **Broyden rank-one updates between full Jacobians.** After an accepted step dz with moment change dm, set
   G <- G + ((dm - G dz) dz') / (dz'dz) and take the next LM step from it; recompute the full Jacobian every third
   iteration or after a rejected round. Cost per iteration falls from 68 to 7 evaluations (one round, ~4 min) for two of
   every three iterations: a 15-iteration polish in ~3.5 h instead of ~9.5 h.
3. **Forward differences for the full Jacobian** (31 evaluations, 5 rounds instead of 9): with CRN the O(h) bias is
   small next to the step sizes used (5% of value); keep central differences for the final Jacobian that feeds the
   sandwich.
4. **Worker/thread configuration test** (one Jacobian round each): 7 x 2 vs 4 x 2 vs 7 x 1 vs 14 x 1 on the 16-thread
   PC. The 3-4x per-solve slowdown under load says the machine is oversubscribed or memory-bound (each worker streams
   ~1.4 GB of stored solution plus the 8 MB expectation arrays per month); fewer, fatter workers may finish a round
   sooner. Also set `NUMBA_CACHE_DIR` to a local disk (finding 7): the first compile and every cache load now go through
   Google Drive.
5. **Reuse solutions for parameters that enter a subset of problems** (bigger change). Of the 30 free parameters, 10
   are race-specific (4 of the 8 solves), pi_c0 / pi_c1 / m_H each touch half, p_H touches none (it only reassigns
   couples to tau): 180 instead of 240 solves per central Jacobian (25%). It needs the base evaluation's per-problem
   records kept (in a local-disk cache, ~0.9 GB) and a `simulate(problems=...)` that merges them; the moments then run
   on the merged records. Worth it only after 1-4.
6. **Smaller K for the Jacobian**: not recommended; under CRN the differences are already noise-free at the same
   seed, and a smaller K changes the sampled population (and var_sim in the weights).
7. **Cond(G'WG) 1e10** is the logistic scaling of F at its bound (finding 2), not a numerical problem for the
   Marquardt step (the diagonal scaling absorbs it). Reporting the column-normalised condition number would stop it
   from alarming the log reader.

## 5. Model opinion (D), given plan 4b and the settled decisions

Respecting: one common beta, no patience types; lambda_h estimated for both races; every parameter from one coded run;
parsimony; F stays free (PI 2026-10-21); one step at a time on one moment set.

**D1. Older couples' wealth is a retirement-motive and a target-definition problem; F at its bound is the symptom, not
the lever.** Three facts from this week point the same way. (i) F profile: Q falls as F rises because a money cost of
work lowers saving (plan 4b). (ii) g_age profile: flatter late wage growth *raises* liquid wealth (le0 at 45-59
0.235 -> 0.145), the opposite of the conjecture: with less expected growth, couples save more in the only asset for a
retirement that the terminal value funds from the annuity of a plus Social Security at 40% of the final level
(model.py:564-595). (iii) Script 77 (paper footnote at `eq:budget`): measured as net worth without home equity and
vehicles, the data's shares at or below zero are 0.476 / 0.354 / 0.264 by age band, against the model's 0.476 / 0.340
at 25-44 already at the old estimate, and 0.234 at 45-59 at `restr`. So the wealth block would be close to fit at the
current estimate if the target matched the asset the model has. The model's single asset funds retirement; liquid
wealth excludes exactly the saving that does. Recommendation, in order: (1) switch the six wealth targets to the
script-77 (c') definition (net worth less home equity and vehicles) -- a target change, no new parameter, then
re-baseline and re-estimate; F should come off its bound by itself; (2) if a gap at 45-59 remains, scan `ss_rate`
(0.4 -> 0.5, 0.6; employer pensions are in none of the PSID definitions, so the terminal value is the only place they
can enter) with `evaluate` before adding anything estimated. I would not add an illiquid asset: two assets double
the state space and the parsimony rule argues against it when (1)-(2) are untested.

**D2. g_age and eta_up: keep one.** Both are now "accumulation falls" terms (with the level: eta_up 0.55 free; with
age: g_age). The profiles say the age term fits the wage-growth block (195 -> 68 at g_age 0.03-0.04) and the level term
does not (eta_up profile flat). When g_age is freed in stage 2, test eta_up = 0 by Wald and drop it if not rejected.
Identification caveat for the paper: g_age and pi_up are separated only by the age shape of the three wage-growth
moments per spouse (6 moments, s.e. 0.003), and the continuously-employed sample is the same in model and data (no
selection bias between them).

**D3. theta_05 and theta_617 near or below zero are a finding to report, not a defect to repair.** The budget already
charges childcare at p_cc(k) x her hours (model.py:511-512; $2.5 an hour under six), so the child penalty in employment
is carried by a money cost; theta_05 ~ 0 says the utility cost adds nothing. theta_617 = -0.016 at stage 1 would say
school-age children raise participation (plausible: their expenses). Under the parsimony rule: Wald-test theta_617 = 0
at the stage-2 estimate and fix it if not rejected; do not constrain the sign. Note the employment-levels block that
pins these (`psid_wemp_none/05/617`, `psid_pt_w/h`) has about as many moments as the work parameters (phi_F, phi_P,
theta_05, theta_617, phi_h, F); the block is close to just-identified, which is why the work parameters absorb every
restriction elsewhere (a_bar, g_age).

**D4. Husbands' non-displacement exits before scarring.** Husbands leave work only by displacement, so 5 moments are
excluded (`psid_hemp_B/W`, three SIPP `_nosep` rows) and the model's husbands are employed 0.99-1.00 against 0.88/0.94.
The joint-loss and added-worker moments condition on his employment at t and t+1, so the conditioning population is
wrong by that margin. One common monthly exit hazard without UI (a quit/other separation: not entitled, no displacement
loss, depreciation as usual) is one parameter, lets the five moments back in, and is in the model's spirit (the
wife already has it). I would do it before the re-employment-loss work (step 5 of the plan lists it; I would move it
first).

**D5. Her re-employment wage loss ~ 0 vs SIPP -6 / -11 / -20% by months out.** psi_w = 0.46 log points per level
(fixed_inputs), so a sure 6-10% loss is not representable; d_w = 0.045 means a 4.5% chance of a 46% drop (2% in
expectation), and pi_dn_w ~ 0 removes the duration gradient. The six SIPP moments (s.e. 0.03-0.08) are outweighed by
the thirteen wage-growth moments (s.e. 0.003), so LM lets them go. Options: report as a misfit now; if scarring is to
be a result, a finer wife's grid (9 levels, ~1.65x solve time) is the honest fix. Not now.

**D6. Bacher, Grubener and Nord nesting.** The nesting is clean: pi_c = 0, m_H = 1 (independent shocks), no children
(`no_child`), no separation (`sig_E = sig_N = 0`), UI only. Two differences to state in the paper rather than close:
their households choose search effort, here the search friction lambda is exogenous and the wife's margin is
acceptance; their beta is calibrated to liquid wealth by age with one asset and no terminal annuity of this form, so
their 0.947 and our 0.948-0.95 agree for different reasons (D1).

**D7. Beta.** Common and estimated is right; with finding 1 fixed, the LM can actually move it and the s.e. becomes
meaningful. With r_m fixed at 3% a year, beta(1 + r) = 0.98 a year; worth one sentence in the paper (impatient
households borrow at the wedge rate, which is what the le0 shares at 25-34 need).

**D8. Small inconsistencies worth a footnote, not a change:** UI on the current level's wage (Section 2); the separated
wife's single innovation at p_c + p_eps_w approximates the married couple's two-step innovation; the husband's age is
the wife's + 2 everywhere (panels and, via g_age, accumulation).

## 6. Not verified

- Runtime behaviour, memory under 7 workers, the numba threading layer on Windows (nothing was run).
- The reduced-form scripts beyond the CR1 helper of 78 (not read in full).
- Whether the hcage1 LM would have converged faster with finding 1 fixed (inference from the evals, not a test).
