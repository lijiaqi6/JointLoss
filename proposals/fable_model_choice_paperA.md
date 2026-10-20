# Paper A: build its own two-earner model or extend the companion model? (2026-10-17)

Read, nothing edited or run: `IGE/paperA_joint_loss/` (main.tex, sec1-sec8, appA-appC, tab_*.tex), my review
`IGE/proposals/fable_review_paperA.md`, the companion paper (`paper/sec4_model.tex`, `model_nobargaining.tex`,
`sec7_counterfactuals.tex`, `appB_family_insurance.tex`, `appD_spouse_shocks.tex`), the companion code
(`model/core.py`, `husband.py`, `bargaining.py`, `params.py`, `ages.py`, `step7_engine.py`, `steps.txt`,
`model_description.md`; `estimation/smm.py`, `data_moments.py`, `model_moments.py`, `sim_panel.py`;
`scripts/hpc_job.py`; `config/settings.yaml`, `config/params.yaml`; `docs/bargaining_design.md`),
`HPC_ReadMe.txt`, `README.md`, `IGE/EVIDENCE.md`, `IGE/PLAN.md`, the git log since 2026-10-11 and the PI's
decision notes. Facts about the companion model below are taken from these files, with the file and function named.

---

## 1. Recommendation (five lines)

1. **Build a self-contained two-earner model for Paper A (option A), on the companion's infrastructure (a hybrid of
   code, not of models).** New solver and simulator; shared parameter-profile machinery, SMM/CMA-ES/CRN engine,
   HPC job script, PSID couple panel and exogenous inputs.
2. **Why not B:** the companion model is annual, has one decision maker (the wife), integrates the husband's
   employment inside the period, has no UI/SNAP/EITC, and has already tested a correlated job loss of spouses at
   annual frequency (2026-10-12), left it at its neutral value and *removed* it from the code (commit `5ca1580`,
   2026-10-14). Paper A's fact is a monthly fact, and its policy question is a schedule question (what pays when no
   one works).
3. **Why not a pure A either:** the companion's `params.py`, `smm.py`, `hpc_job.py`, `sim_panel.py` design (PSID
   code run on simulated households) and the PSID inputs for husbands are exactly what Paper A needs and took weeks
   to make robust; rewrite the economics, not the plumbing.
4. **Referee and timeline:** a referee cannot evaluate a model that leans on an unpublished 75-parameter companion
   model that is still being restructured weekly (age-18 start 2026-10-14; bargaining tested and dropped
   2026-10-14; layoff state and search moments 2026-10-16; common-preferences test running 2026-10-17; the decided
   shared wage shock not yet coded). Paper A must state and estimate its own model, with about 18 parameters.
5. **Cost:** about 12 weeks to estimated counterfactuals (plan in Section 5); HPC load per run comparable to one
   companion run (about 8 s per evaluation, 32 cores, 32 GB); nothing in it blocks or is blocked by the companion.

---

## 2. What Paper A's model must deliver, and what the companion already has

### 2.1 Requirements (from the paper's own evidence and the review's Sec. 3.4)

| # | Requirement | Why (the fact it must carry) |
|---|---|---|
| R1 | **Two earners, both with a displacement hazard, a search friction, a human capital level that accumulates at work and depreciates out of it, and a displacement loss** | his earnings -17%/-24% over years 1-3, -$6-7k six years later (Sec. 5.1); her wage loss ~$4,600/yr (Sec. 4.5) |
| R2 | **Three-part displacement risk**: own hazard, a **common shock** hitting both spouses in the same period with a probability that is larger when they share a sector, and a **permanent couple type** (assortative risk) | CPS same-month excess 4.0 pp (14.8 pp more in the same industry); leads/lags 0.6-0.8 pp; PSID permanent 0.020** vs contemporaneous 0.033**; tetrachoric 0.24 / 0.50 (Sec. 4) |
| R3 | **Monthly period** | the headline is a same-month fact; wives search at once and employment builds over ~6 months (CPS, SIPP); UI has a 26-week duration; a joint *permanent* loss is both spouses still unemployed two months later |
| R4 | **Government as schedules**: UI (replacement, duration, eligibility per spouse), SNAP floor keyed to family income, EITC on family earnings, childcare price | "the EITC pays nothing when both lose their jobs; SNAP pays in every state" is the paper's policy sentence; SNAP +4 pp after displacement |
| R5 | **Child-age-dependent cost of her work**, children's ages exogenous | added work 97 h (youngest under 6) vs 47 h (all); employment +4.1 pp vs -3.8 pp by child age |
| R6 | **Separation hazard that responds to his job loss**, by race | still with wife -4.5 pp (Black) / -1.9 pp (White) within 3 years |
| R7 | **Savings with a borrowing limit** and a liquid-wealth distribution close to the PSID | consumption smoothing is the object; Black/White buffer gap |
| R8 | **Child block outside the estimation**: adult outcome = f(family income by childhood age, both parents present), slopes from administrative estimates; two slope scenarios | PSID associations are bounds only (Sec. 6) |
| R9 | **Estimation**: all endogenous parameters in one SMM run; an **independent-shock version estimated on the same targets** | PI rule; the review's "what the correlation buys" |
| R10 | **Five counterfactuals** (Sec. 7 of the paper): common shock off; UI for both spouses and longer in recessions; EITC-type subsidy vs equal-cost unconditional transfer; childcare subsidy under 6; Black couples with White hazards / White separation response | |
| R11 | **Race as heterogeneity in the environment, common preferences** | the fact is equal by race (Black 0.044 vs White 0.038, p = 0.31); Black men's hazard 8.0% vs 4.8%; the companion's own path review puts common preferences at the centre |

### 2.2 What the companion model has (file, function) and what it lacks

**Has, and Paper A can reuse as code or as design:**

| Piece | Where | Note for Paper A |
|---|---|---|
| Savings on an asset grid with a borrowing limit; curved grids (`finegrid`, `finegrid30`) after the lesson that a linear 20-point grid's first point was $84,000 | `model/core.py: asset_grid`; `config/settings.yaml` | reuse the curved-grid design and the 2026-10-14 finding that the zero-wealth share is a grid artefact on 20 points |
| Search friction and separation (offer state, `lambda_u`, `delta_u`; a "first year out" gain `fresh_gain`; a laid-off state) | `core.py: _p_offer`, `solve_vfi_step_marriage_hc` | same mechanism, re-timed to the month |
| Human capital accumulation / depreciation by education (`pi_up_f`, `pi_up_pt`, `pi_down_f`), displacement-free | `core.py`; `smm.py` PARAMS panel A | the form is right; Paper A adds a displacement loss and gives the husband a level too |
| Husband: employment with persistence (`husband_emp_rho`, state index "employment last period"), age x education earnings profile from a simulated male process, `b_m` floor when not employed | `core.py: generate_male_lifecycle_processes_by_edu`, `solve_marriage_model` (V's last index), `husband.py: divorced_man_step` | his earnings are deterministic given age and education; no human capital state of his in her problem, so no displacement scar, no wage loss on re-employment |
| Child-age work cost `theta_ak` (youngest child), childcare cost by child age from the PSID | `core.py: build_childcare_cost_age`, `smm.py` | reuse the functional form and the PSID childcare inputs |
| Household equivalence scales | `core.py: equivalence_scales` | reuse |
| Divorce as a choice with a taste shock; a collective (Voena) version built, estimated and rejected (weight unidentified) | `core.py: _marriage_ev`; `husband.py`; `bargaining.py`; `paper/sec4_model.tex` line 259 | Paper A should not repeat the bargaining exercise; an exogenous separation hazard with a job-loss elevation is enough for R6 (parsimony) |
| Transfers: `b`, `b_m`, `b_k_single` floors; optional work and asset tests (`--welfare`) | `config/params.yaml`; `smm.py` WELFARE_START | no UI duration, no EITC, no SNAP schedule |
| SMM engine: CMA-ES on a logistic transform, parallel `SafePool`, common random numbers, resume, pseudo-data recovery tests, Jacobian/profile commands, block weighting | `estimation/smm.py: cmd_run, cmd_profile, cmd_jacobian, _evaluate, SafePool` | reuse wholesale with a new `model_moments` / `data_moments` pair |
| Parameter profiles with status/source per parameter, run manifest, write guard | `model/params.py` | reuse unchanged (add a Paper A schema) |
| "PSID code on simulated households": simulate, write a PSID-shaped panel, impose each PSID unit's observation pattern, run the data code | `estimation/sim_panel.py`, `sim_panel_check.py`, `model_moments.py` (design copies) | the pattern Paper A needs to turn a monthly simulation into PSID annual moments (Sec. 2.4 below) |
| Standard errors, fit report, block comparison | `estimation/standard_errors.py`, `fit_report.py`, `block_compare.py` | reuse |
| HPC: snapshot of the committed code, memory check per worker, email, resume on time limit, push of results | `scripts/hpc_job.py`; `HPC_ReadMe.txt` | reuse; add an entry point for the Paper A estimator |
| Added-worker annual moment (wife's exit by husband's employment next year, annual waves to 1997) | `estimation/data_moments.py` item 12 (`spouse_exit`) | the same PSID variables feed Paper A's annual targets |
| Husbands' assets at marriage, husbands' process from married men | `ModelInputs/husband_assets_at_marriage.json`; `smm.py --husband-assets`, `--married-men` | initial conditions for couples |

**Lacks (each one is a structural change to the companion, not a parameter):**

| Missing for Paper A | Evidence in the files |
|---|---|
| A monthly (or any sub-annual) period | `paper/sec4_model.tex` line 6: "Time is discrete and annual"; `model/ages.py`: period = age |
| A joint displacement shock of spouses | added behind a switch 2026-10-11/12 as `husband_corr_sep`, tested 2026-10-12 and held at its neutral value (no correlation), **removed from the code 2026-10-14** (commits `562d807`, `5ca1580`; the removal was exact, "Black Q unchanged"); `smm.py` line 159; `data_moments.py` line 59; `sec4_model.tex` line 524 "tested and left out" |
| The husband as an earner with a human capital level, a displacement loss and a job-finding process in the wife's state | his employment is an intra-period draw `p_m(t, E_m)` integrated out (`sec4_model.tex` line 51; `model_nobargaining.tex` line 173); persistence only via the last-period index |
| A sector-match state and a permanent couple-risk type | none |
| UI with duration and per-spouse eligibility, an EITC schedule, a SNAP schedule, a childcare price that a subsidy lowers | only floors `b = b_m = 0.25`, `b_k_single = 0.12` (`config/params.yaml`) |
| A separation response to job loss | `pi_unemp_shock` fixed at 0 since 2026-10-02 and removed 2026-10-14 (commit `f8edda2`) |
| A shared spouse wage shock | decided 2026-10-15, not coded (`sec4_model.tex` line 754 TODO; PI note) |
| A child-outcome block | none (the companion's children are a work cost) |
| Monthly search moments of wives after the husband's loss | the companion's search blocks (`look`, `look_tr`, `look_dur`) are annual interview-week statuses of women around births |

### 2.3 Identification of the common versus the permanent component (what the model must be able to produce)

- The **common shock** produces excess joint loss *only in the month it hits*: the CPS spike of 4.0 pp at tau = 0
  against 0.6-0.8 pp at tau = +-1..3. Its sector-match dependence is identified by the same-industry interaction
  (+14.8 pp CPS; +0.203 PSID same sector; SIPP +0.22) and by the tetrachoric 0.50 vs 0.18.
- The **permanent couple type** produces a flat elevation of her hazard in every month around his loss (the CPS
  leads and lags) and the PSID placebo-window excess (0.020**); it also raises both own hazards for years, which
  is what makes it matter for saving.
- The **own hazards** come from the base rates (wife 0.54% a month in the CPS; husband 4.8% / 8.0% a year in the
  PSID by race).
- This needs a period short enough that "same month" and "months around" are different objects. In an annual
  model the two components collapse into a same-year correlation (PSID 10.2% vs 3.9%), and the CPS leads/lags
  cannot be used. That is the technical reason the companion's annual `husband_corr_sep` was left at its neutral
  value: its only annual counterpart (`spouse_exit`, the wife's exit by the husband's employment next year) is the
  net added-worker response, and averaged over a year the joint loss is 2% of the family income loss (Sec. 4.5 of
  the paper).

### 2.4 Period: monthly decisions, annual moments

- **Monthly period**, ages 25-60 of the wife (420 periods), with age-dependent inputs changing once a year. The
  solver is backward induction over 420 steps on a state space of order 10^5 points (Sec. 5.2): a few seconds per
  solve in numba, which is the companion's order of magnitude (its evaluation is ~8 s on the HPC, 13.8 s locally on
  8 threads, `docs/bargaining_design.md` "Cost").
- **Annual PSID moments from monthly simulations**: write the simulated monthly panel into a PSID-shaped
  household-year panel (annual hours = sum of months worked x hours; "displaced in year" = a displacement in any
  month of the calendar year; interview-week status = status in a spring month; family income = sum over the
  year) and run the Paper A scripts' definitions on it, as `estimation/sim_panel.py` does for the companion. This
  removes the dating ambiguities the review raised (year-0 hours mixing pre- and post-loss months).
- **EITC in a monthly model**: the credit depends on annual earnings. Carry a one-dimensional "earnings so far this
  tax year" state coarsely (3-4 bins) or pay the credit monthly on annualised current earnings; start with the
  second (standard in monthly models) and state it; the counterfactual (iii) is a comparison of schedules, so the
  approximation applies equally to both arms.
- **Quarterly fallback** if compute binds: the CPS and SIPP can be re-aggregated to same-quarter joint loss; UI
  duration becomes two quarters. Keep monthly as the plan; the fact is reported monthly.

---

## 3. Costs and risks of each option

| Dimension | (A) Own two-earner model (on shared infrastructure) | (B) Extend the companion model |
|---|---|---|
| **Coding time** | 5-6 weeks to a tested solver + simulator + moments (Sec. 5); the economics is small (no fertility, no marriage market, no types, no part-time) | monthly period = retime 7 state dimensions, fertility (monthly fecundability already exists in the companion but the child-age state is annual), marriage proposals, human capital transitions, divorce shocks; add the husband's human capital level and job search to the wife's state; add UI/EITC/SNAP; 8-12 weeks, with regression tests (`tests/test_solver_regression.py`) all failing by construction |
| **Estimation time (HPC)** | ~18 parameters; ~8 s per evaluation; 5,000-10,000 evaluations converge for this dimension: 2-3 h per run on 32 cores / 32 GB; 4-6 runs in total (correlated, independent, pooled vs by-race check, recovery test, SEs) | 75-76 parameters (`sec4_model.tex` line 524) on a 12x longer horizon: ~100 s per evaluation, 20,000 evaluations = 2+ days per run per race; memory per worker rises with the state space (now 3.4 GB; 14.5 GB with renegotiation, `hpc_job.py` line 388), so fewer workers fit in 64 GB; the PI's 32-core rule makes this a multi-week estimation cycle |
| **Identification** | the joint-loss moments identify 5 shock parameters cleanly (Sec. 2.3); the rest are standard (search friction from monthly flows, work cost from employment by child age, human capital from wage paths) | the companion's objective is already flat in several directions (asset_limit unidentified, theta_ak_rho weak: PI note 2026-10-17); adding 8-10 parameters whose moments are 2% of the family income loss at annual frequency would add noise to a 4,000-point Q with a ~500 simulation-noise band |
| **Referee perception** | self-contained: the model is stated, estimated and tested in Paper A; comparable to Birinci (2019), Mankart and Oikonomou (2017), Blundell et al. (2016); 18 parameters a referee can check against 25 moments | "the lifecycle model of the companion paper" with 75 parameters, race-specific preferences and a child-penalty objective; a referee cannot evaluate it, and the companion's fit of married Black mothers (model 17-19 vs PSID 8) would be held against Paper A |
| **Dependence on the companion's timeline** | none; Paper A can be estimated while the companion changes | total: the companion is mid-restructure (age-18 start, search moments, common-preferences test, shared wage shock pending); the PI's own path review for the companion says "cut before adding; hold new features until the married-Black penalty fits" |
| **Code reuse** | plumbing reused (params, SMM engine, HPC, sim-panel design, standard errors, PSID inputs); economics new | everything reused, but every piece must be re-timed and re-tested |
| **Consistency across papers** | by construction where it matters: same fixed preferences (beta 0.96 annual -> 0.96^(1/12), gamma 1.5, r 3%), same PSID husband inputs, same human capital mechanism (accumulation / depreciation), same search-friction form, annualised rates reported next to the companion's; a one-page consistency table in Paper A's appendix | automatic, but it binds Paper A to every later change of the companion's estimates |
| **Parsimony (PI rule)** | ~18 estimated parameters, each with a named moment; nothing the joint-loss data cannot separate | 75 + 10 parameters, most irrelevant to the question (fertility timing, proposal curve, unintended conception, types) |
| **Period length** | monthly, matching the fact | annual; the correlated loss was already found irrelevant at that frequency |
| **Risk specific to the option** | two models of husbands' risk in two papers must not contradict each other (mitigated by the consistency table and shared inputs) | the companion's agenda and Paper A's compete for the same 32 cores and the same weeks; neither paper finishes |

Birinci (2019) is the template a referee will have in mind: a two-earner search model built for the spousal
response to displacement, calibrated on SIPP/PSID moments, with transfers scored; the companion's full lifecycle
is not needed for that question (my review, Sec. 6, last-but-two row).

---

## 4. The hybrid: exactly what to share and what to build

### 4.1 Share (code modules, used as they are or lightly generalised)

| Module | Use in Paper A | Change needed |
|---|---|---|
| `model/params.py` | parameter profiles with value/status/source, validation, manifest, write guard | a Paper A schema (`REQUIRED`/`OPTIONAL` dictionaries) and a second params file, e.g. `config/params_couples.yaml`; the loader is generic |
| `estimation/smm.py` | CMA-ES loop, logistic transform, `SafePool`, CRN seeding, resume, `cmd_profile`, `cmd_jacobian`, pseudo-data recovery, block weighting | factor the model-specific parts (PARAMS table, `apply_theta`, `_moments`) behind a small interface so a `--model couples` switch (or a sibling `estimation/smm_couples.py` importing the engine) selects Paper A's parameter table, targets and simulator |
| `scripts/hpc_job.py` | code snapshot, memory check, email, time-limit resume, result push | an argument naming the estimator module; `--job-name=A-<what>` per the PI's job-name rule |
| `estimation/sim_panel.py` design | PSID-shaped simulated panel + observation masks + the data code run on it | a couples version writing household-years from monthly simulations |
| `estimation/standard_errors.py`, `fit_report.py`, `block_compare.py`, `bins.py` conventions | SEs, fit tables, block tables | moment names only |
| `model/core.py: asset_grid, equivalence_scales, build_childcare_cost_age` | grid, scales, childcare cost by child age | import as functions |
| `ReducedForm/1.PreparePanel.py` and the IGE displacement coding (`IGE/19.FatherDisplacement.py`, `25.JointJobLoss.py`) | the PSID couple panel with both spouses' job-end reasons | none; Paper A's targets already come from these |

### 4.2 Share as calibrated inputs (exogenous in both papers)

- Husbands' earnings profiles by age x education (`ModelInputs/male_labinc_age_by_race_edu_smoothed.csv`, or the
  married-men version), their employment persistence (`ModelInputs/husband_employment_persistence.csv`), husbands'
  assets at marriage (`ModelInputs/husband_assets_at_marriage.json`), education shares and the first-marriage
  mating distribution (to draw the initial couples).
- Fixed preferences: beta, gamma, r, equivalence scales. Same values in both papers.
- Policy schedules: UI replacement and maximum benefit by state and year (`IGE/12b.UIGenerosity.py`), EITC
  parameters by year and number of children (IRS), SNAP maximum allotment and gross-income test, childcare cost
  shares (companion's PSID inputs).
- Children's arrival: youngest-child age process drawn from PSID couples (exogenous in Paper A).

**Do not share the companion's SMM estimates** (women's work cost, human capital rates, search friction) as fixed
inputs: they are annual, come from a woman-only model with race-specific preferences, and are still moving
(round 6/7 of HPC runs this week). Importing them would also break the PI's one-run rule for Paper A. Paper A
estimates its own and reports the companion's annualised counterparts in the consistency table.

### 4.3 Share as data moments

The PSID couple-year sample and the displacement coding are the same; Paper A's targets are the ones already in
`IGE/output/joint_job_loss.md`, `cps_joint_job_loss.md`, `cps_joint_loss_checks.md`, `sipp_joint_loss.md`,
`psid_joint_loss_checks.md`, `father_displacement.md`. The companion's `spouse_exit` block (annual wife's exit by
husband's employment next year) is the annual version of Paper A's added-worker target and should agree with it.

### 4.4 Build new (the economics)

Solver and simulator for the couple's problem (Sec. 5.2), the three-part shock, the two human capital levels with a
displacement loss, UI/SNAP/EITC/childcare schedules, the separation hazard with its job-loss elevation, the child
block, Paper A's `data_moments` / `model_moments` pair (monthly and annual), and the five counterfactual scripts.

### 4.5 How to present it in Paper A

- Section 6 states the model in full (environment, timing, shocks, government, estimation) as Paper A's own
  model; the appendix carries the economics-style model document (PI's model-docs rule, simulator order).
- One footnote in the estimation section: "The parameter-profile, estimation and HPC code is shared with the
  author's lifecycle model of women's careers; the husbands' earnings and employment inputs are the same PSID
  profiles (scripts named)." No citation of the companion paper as a source of estimates (PI rule on
  self-citation); cite sections of Paper A for the moments.
- A consistency table in the appendix: for each shared object (beta, gamma, r, husband inputs, search friction
  form, human capital form), the value or form in Paper A and the annualised equivalent in the companion.
- The independent-shock model estimated on the same targets is reported next to the main model (fit table and
  counterfactual table), per R9.

---

## 5. Build plan

### 5.1 Milestones (weeks from the start; one person, HPC per the PI's rules: 32 cores, --threads 2, email, job names)

| Week | Milestone | Deliverable / test |
|---|---|---|
| 0-1 | **Targets file.** Paper A's moments with bootstrap SEs from the existing scripts (25, 30, 37, 38, 40, 19), one `EstimationMoments/couples_*.csv`; sample definitions written down | the targets table of Sec. 5.3 reproduces the paper's numbers |
| 0-1 (parallel) | **Model document** in the PI's style (economics, simulator order, every choice visible, no results): `model/couples_description.md` or `IGE/paperA_joint_loss/model_description.tex` | PI sign-off on state space, timing and schedules before code |
| 1-3 | **Solver** (`model/couples.py`, numba): backward induction over 420 months; staged checks in the spirit of `model/steps.txt`: (1) flat consumption with no risk, (2) precautionary buffer with risk, (3) her work choice rises with lower assets / his loss, (4) search friction lengthens non-employment, (5) UI duration shows in the hazard of her exit | unit tests under `tests/test_couples_*.py` |
| 3-4 | **Simulator with CRN** and the **monthly -> annual panel** (`estimation/couples_panel.py` after `sim_panel.py`); model moments at monthly (CPS/SIPP) and annual (PSID) frequency | the paper's definitions run unchanged on simulated couples |
| 4-5 | **SMM wiring**: Paper A parameter table with bounds, `apply_theta`, reuse of the CMA-ES engine and `hpc_job.py`; **pseudo-data recovery** (`--pseudo-seed`) and a Jacobian on the start values | every parameter has a non-flat profile and a named moment block; recovery within noise |
| 5-8 | **HPC estimation**: (a) main model, pooled preferences, race-specific hazards and husband inputs; (b) independent-shock model on the same targets; (c) recovery; (d) standard errors | fit tables; the two models' Q by block |
| 8-10 | **Counterfactuals** (i)-(v); **child block** with two slope scenarios; untargeted validation (CPS looking +8.8 pp; SIPP 36-month path; DWS same-year ratio 4.3; food spending joint vs single) | the counterfactual table and figures of Sec. 7 |
| 10-12 | **Writing**: Sec. 6 (model, estimation, fit, independent-shock comparison), Sec. 7 (results), appendix model document, consistency table; PSID-motivated choices footnoted with numbers and scripts | Paper A complete |

### 5.2 Minimal state space (monthly; one couple)

| State | Values | Why |
|---|---|---|
| assets `a` | 30 points, curved near zero (the companion's `finegrid30` lesson) | R7 |
| her employment `e_w` | employed / non-employed | R1 |
| his employment `e_h` and UI clock | employed / unemployed with k months of UI left (k bucketed 6, 3, 0) / exhausted | R1, R4 |
| her UI clock | same bucketing when non-employed after a job loss (not after a quit) | R4 |
| her human capital `h_w` | 4 levels; accumulates while employed, depreciates while not; falls one level at a displacement | R1 |
| his human capital `h_h` | 4 levels, same mechanism | R1 (his -17/-24% and the slow recovery) |
| youngest child | none / 0-5 / 6-17 (exogenous arrival and ageing, yearly) | R5, child block |
| sector match `s` | same / different (permanent, PSID 15% same sector) | R2 |
| couple risk type `tau` | low / high (permanent, known to the couple) | R2 |
| marital status | married / separated (absorbing; the separated wife continues alone with the child) | R6 |
| age | 420 months, inputs change yearly | |

Order 30 x 2 x 4 x 3 x 4 x 4 x 3 x 2 x 2 x 2 = about 1.4 x 10^5 points per month in the married state (fewer when
separated); with 30 saving choices and 2 work choices, a solve is of the order of 10^9-10^10 operations: seconds in
numba on two threads. Choices: saving, her work (accept / keep a job or not; no search-effort choice, as the
companion decided for parsimony; "looking" = non-employed and would accept), SNAP take-up (a utility cost; take-up
identified by the +4 pp), UI taken up when eligible. His employment is exogenous (he works whenever he has a job;
married men's employment 0.94-0.98), which keeps the model about the paper's shock and is the companion's
assumption too; say so and give the husbands' employment rate as the reason.

Shocks per month: own displacement hazards delta_w(tau), delta_h(tau, race); common shock pi_c(s) hitting both;
job finding lambda_w, lambda_h (his calibrated from CPS/SIPP male flows, hers estimated); human capital
transitions; separation hazard sigma_0 + sigma_J x (his job loss in the last 12 months); child ageing.

### 5.3 SMM targets (about 25 moments, inverse-variance weights, block weighting as a robustness run)

| Block | Moments | Source | Identifies |
|---|---|---|---|
| Joint loss, monthly | her job-loss probability in his loss month vs other months; same by sector match; her excess at tau = -2, -1, +1, +2 | CPS (30, 37) | pi_c(s), couple-type share and multiplier |
| Joint loss, annual | permanent 0.020 and contemporaneous 0.033 components; same-year P(she | he) 0.102 vs 0.039 | PSID (38, 25) | over-identification of the two components |
| Base hazards | her monthly job-loss rate 0.54%; his annual displacement 4.8% / 8.0% by race | CPS, PSID | delta_w, delta_h(race) |
| Her search | monthly job finding of non-employed wives; employment of previously non-employed wives +1.9 pp (month 0) -> +5.4 pp (month 6) after his separation | CPS, SIPP (40) | lambda_w and the search-at-once response (value of a job when his income is gone) |
| Added work, annual | her hours years 1-3 after his displacement, by youngest child (97 h under 6; 47 h all), gross (she kept her job) and net | PSID (38) | work cost by child age, income effect |
| Her employment levels | employment of wives by youngest child age (none / 0-5 / 6-17) | PSID | phi_0, phi_k |
| His earnings path | labor income years 1-3 (-17% / -24%) and year 6 (-$6-7k) after displacement; the year -1 dip reported, not targeted | PSID (19) | his human capital depreciation and displacement loss |
| Her wage loss | her earnings loss after her own displacement (~$4,600) | PSID (25) | her displacement loss |
| Safety net | SNAP receipt +4 pp after displacement | PSID (19) | take-up cost |
| Separation | still with wife -1.9 / -4.5 pp by race, years 1-3 | PSID (19) | sigma_0, sigma_J(race) |
| Wealth | share of couples with liquid wealth below a quarter of annual earnings, by wife's age group | PSID (ReducedForm/17) | precautionary motive given beta fixed |

Untargeted validation: CPS "unemployed and looking" +8.8 pp in the month after his loss; SIPP 36-month paths; DWS
same-year ratio 4.3; food spending after single vs joint loss (PSID, 38); the companion's `spouse_exit` moment.

### 5.4 The five counterfactuals (as in Paper A Sec. 7, with the measurement each needs)

1. **Common shock off** (pi_c = 0, re-solved, same draws): consumption fall in the month of his loss and over 12
   months; share of couples with no earner; child-outcome change via the child block; by sector match.
2. **UI for both spouses / longer duration**: eligibility of the second spouse at a joint loss; duration 26 -> 52
   weeks with pi_c doubled (the recession excess 6.7 vs 3.6 pp), as a comparative static without an aggregate state.
3. **EITC-type subsidy vs equal-cost unconditional transfer**: scored on consumption in joint-loss months, on the
   share of months with no earner and no credit, and on children; the budget equalised in the simulation.
4. **Childcare subsidy** when the youngest child is under 6: her employment and added work; children via income.
5. **Black couples with White displacement hazards, then with the White separation response**, one at a time.

Each reported for the main and the independent-shock model: the difference is "what the correlation buys".

### 5.5 What can start now (this week, no HPC)

- The targets file and SEs (all scripts exist; one new script `IGE/45.PaperATargets.py`).
- The model document for PI sign-off (state space, timing, schedules, parameter list with the moment that
  identifies each; PI's model-docs style).
- Policy schedule inputs: UI from `IGE/12b.UIGenerosity.py`; EITC and SNAP parameters by year as small CSVs in
  `ModelInputs/`.
- The solver skeleton and its staged tests (weeks 1-3) need nothing from the companion's running jobs.

---

## Risks of the recommended path and their answers

| Risk | Answer |
|---|---|
| Two husband-risk models in two papers that disagree | shared husband inputs, shared fixed preferences, the consistency table; Paper A's annualised search friction and human capital rates reported next to the companion's |
| The monthly solver is slower than expected | quarterly fallback (Sec. 2.4); or coarser UI clocks and 3 human capital levels; the companion's bargaining experience shows a 5-10x slower solve is still estimable |
| The independent-shock model fits as well | then the paper's point is distributional and policy incidence (same-sector couples, EITC vs SNAP in joint-loss months), as my review's fallback says; the correlation stays because it changes the counterfactuals, not the average fit |
| A referee asks why the two papers do not use one model | the honest answer is in Sec. 3: different questions, different frequencies, different parsimony; one footnote |
| The companion later adds the shared wage shock and a husband earner | Paper A's model is the natural place to test those mechanisms at the month first; results transfer as design knowledge, not as parameters |
