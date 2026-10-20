# Paper A: what the lead can do in the next three hours without the PI (2026-10-19, 09:30-12:30)

Read only, nothing run: `paperA_model/README.md`, `results/diagnostics_20261018.md` (with 'Follow-ups 2026-10-19'),
`results/evaluate_20261019_064228_p27000/`, `estimate.py` (CLI, `EXT_DEFAULTS`), `model.py` (hazard block),
`params.py` (`Config`, `SIZES`, schedules), `bps_check.py`, `hpc_job_a.py` (`--push` into `results/hpc_runs/`),
`paperA_joint_loss/sec7_model.tex`, `model_document.tex`, `main.tex`, `tab_joint_job_loss.tex`,
`output/paperA_targets.csv`, `IGE/30`, `39`, `40`, `21`, `60`, and my notes `fable_estimation_review_paperA.md`,
`fable_marriage_divorce_paperA.md`. Terminology: search friction; human capital level / accumulation / depreciation.

## 0. The constraint, stated as a file list

The HPC chain (`Joint-test` -> `Joint-recovery-gn` -> `Joint-gn-main` -> `Joint-noise` -> `Joint-smm-main` + 2 restarts)
runs a snapshot of commit 6adfd1a and the later jobs must be consistent with the LM run. Until the CMA-ES jobs have
started, **no edit** to any of these: `paperA_model/{model,solve,simulate,panels,moments,params,estimate,
analytic_start,borrowing_wedge,hpc_job_a}.py`, `paperA_model/inputs/*` (start, wage process, noise, expected
moments, schedules, wedge), `paperA_model/tests/*`, `IGE/60.PaperATargets.py`, `output/paperA_targets*.csv`,
`IGE/61.PolicySchedules.py`, `IGE/62.PaperAInputs.py`. Running `IGE/60` or `62` is also out (they rewrite targets and
inputs). `bps_check.py --apply` is out (it rewrites `inputs/wage_process.json`). Everything below is new scripts, new
outputs under `output/` or `results/`, data work, and paper text. Local evaluations of the model (new
`results/evaluate_*` folders) are harmless. Each package ends with its own commit on main (shared working tree; no
branches; no PSID/SIPP/CPS microdata in git, aggregates only).

Order of priority: WP1 (evidence the PI needs for the next decision) > WP2 (paper rule: every modelling choice
footnoted, the section is a day behind the code) > WP3 (same-day write-up once `hpc_runs/` arrives) > WP4 > WP5.
WP1, WP3 and WP4 go to sub-agents at once; the lead does WP2 and closes with WP5. 16 cores: WP3's local test
evaluations take 8 workers x 2 threads; WP1/WP4 are single-threaded pandas.

## WP1. Why do wives leave employment at 1% a month, persistently? (sub-agent, 75-90 min, risk to HPC: none)

**Goal.** The persistent exit rate is the main unexplained margin (model 0.14% a month against 1.0%, z -69, Q 4,622
of 11,726; `sigma_eps` cannot move it, diagnostic A). The PI will decide after the first estimate which feature to
add; prepare the evidence now so the decision is one reading. The question has three parts the data can answer and
the model cannot: (a) *what happens around the exit* (a birth, a child reaching an age, his income or job change, her
job tenure, part-time status, age 55+, race, education); (b) *the stated reason* (SIPP `ERSEND`: layoff / discharge,
quit to care for children or family, pregnancy or childbirth, own illness, school, retirement, other); (c) *how long
the spell lasts* (return to work within 3, 6, 12, 24 months). Each maps to one candidate model feature:

| finding | model feature it points to |
|---|---|
| exits concentrated in the months around a birth or a child aged 0 in the household, and reversed within 12-24 months | a transitory work-cost shock at births (a jump in theta_05 for k months), fertility timing already in the child chain |
| exits spread across child ages, long spells (no return within 24 months), the same wives repeatedly | persistent work-cost heterogeneity (a wife type), or a two-state taste process |
| exits concentrated in short job tenures (first 6-12 months of a job) | a match-quality or probation hazard on new jobs, not preferences |
| exits rising with his earnings growth or his job change, or at a move of state | income effect on her participation; nothing to add if the model's wealth effect already carries it |
| exits at 55-59 | a retirement margin (report; probably outside the paper's question) |
| SIPP reasons: a large 'own illness / disability' share | a health shock to the work cost (one state; probably not for this paper, but it belongs in the footnote) |

**Inputs (all public files already local, read only).** SIPP: `IGE/40.SIPPJointLoss.py`'s cached monthly panel
(`PANEL_PKL` under `data/`; 2004 and 2008 panels carry `ersend{j}`, `tsjdate{j}`, `tejdate{j}`, `ejbind{j}`,
`rmesr`, children through `epnmom`; the 2014 panel `RMESR`, `RPNPAR1/2_EHC`, `TAGE_EHC`). CPS: `IGE/30`'s cached
couples panel `data/cps_couples_panel.pkl` (PEMLR, PRUNTYPE job leaver vs loser, PRCHLD and children's ages from
the kids file, PEEDUCA, PRTAGE, race, industry PRDTIND1; no hours variable in this extract: part-time is not
observable here without a new API pull, which is not for these three hours). PSID: `data/psid_person_year.pkl`
(annual hours, employment-status codes 1-8 incl. 'keeping house', child ages, spouse's labor income, state), through
the loaders of `IGE/21.WifeSearch.py` / `IGE/19` imported read only.

**Method.** One new script `IGE/63.WifeExitWhy.py` (the next free number; `IGE/60-62` are Paper A inputs and must
not be re-run). Sample everywhere: married wives 25-59, husband employed, as in `cps_wife_exit_p` (employed in t-1
and t, not employed in t+1 and t+2). Report (i) the exit hazard by covariate cell with the share of all exits each
cell accounts for (shares x hazards add up to the 1.0%); (ii) weighted LPM of the exit on the covariates jointly
(s.e. clustered by household / 1968 family), stars and p-values on every coefficient; (iii) SIPP reasons for the
persistent exits (`ERSEND` of the job that ended in t+1), by race and child age; (iv) SIPP spell length: return to a
job within 3 / 6 / 12 / 24 months, by reason and by whether a child aged 0 appears; (v) PSID: annual exit (positive
hours in t, zero in t+1) by a birth in t+1, youngest child's age, his labor-income change, her age; share of exits
coded 'keeping house'; return within 2 and 4 years; repeat exits of the same wife (persistence). (vi) The steady-state
arithmetic for the paper: with 81% employment, a 1.0% monthly persistent exit implies about 4.3% monthly persistent
entry, which is what the CPS shows (3.2% White, 4.0% Black): the data describe a high-churn equilibrium with short
spells, the model a low-churn one; the spell-length distribution in (iv) is the statistic that decides between a
transitory shock and persistent types.

**Deliverables.** `output/wife_exit_why.csv` (every estimate: dataset, sample, cell, outcome, coef, se, p, stars,
n), `output/wife_exit_why.md` (tables in the paper's layout: one outcome per column, covariates as rows, samples
as row panels), and a two-page memo `proposals/wife_exit_evidence.md`: findings, the decomposition, the feature
each finding points to, the cost in states and parameters of each (none for a birth-timed theta jump: the child
state is there; one state for a persistent type, doubling solve time), and a recommendation for the PI. Footnote-ready
sentences with numbers and the script name (PI rule). Commit script + outputs + memo. Risk to the HPC: none (no file
of Section 0 touched; no PSID/SIPP microdata written anywhere tracked).

## WP2. The model section and the model document catch up with the code (lead, 60-75 min, risk: none)

**Goal.** `sec7_model.tex` and `model_document.tex` describe the model of 2026-10-17. The PI rules: every
data-motivated choice (added, tested-and-dropped, calibrated) gets a footnote with numbers and the script; the
document is written from the code in simulator order (Voena template); the paper is the journey (nulls in text, failed
designs in an appendix). Numbers below are in `results/diagnostics_20261018.md` and `README.md`; nothing needs running.

**Edits in `sec7_model.tex`** (Edit tool, never heredocs for LaTeX; compile `main.tex` before the commit):
1. Wages and human capital (after eq. `eq:wage`): accumulation pi_up_j (h/4)^(-eta_up), eta_up estimated (start 0.5).
   Footnote: wage-growth block 158 -> 150 at 0.5, 109 at 2.5 with pi_up rescaled; the closed form from mean levels by
   age would need eta 6 (wives) to 16 (husbands); the age profile of accumulation needs more than level dependence
   (`diagnostics_20261018.md`, step 4; `analytic_start.py --ext hc_eta`).
2. Budget constraint (eq. `eq:budget`): borrowing at r + 8.4 points (G.19 real credit-card rate 11.4% 1995-2021 minus
   3%; `borrowing_wedge.py`, `inputs/borrowing_wedge.json`). Footnote: Q 68,086 -> 64,657; young debt share 0.80 ->
   0.48 (data 0.57); a_bar 15 / 25.6 / 40 / 55 -> wealth Q 3,079 / 2,672 / 2,419 / 2,317; the 45-59 shape stays
   (too few at or below zero, too many above a year of earnings), stated as an open misfit.
3. Displacement risk: the couple type is started on the CPS ridge (p_H 0.02, m_H 15.95). Footnote: the ridge profile
   (annual excess 0.118 at p_H 0.10 -> 0.071 at 0.02, data 0.063; monthly leads and lags kept) and the tested and
   rejected alternative, a short memory of the common shock (c_mem, one parameter: joint-loss Q 177 against 62; lags
   0.013 against 0.006), kept as `--cs-memory`.
4. Marriage (eq. `eq:sep`): one sentence from the marriage note's recommendation 1: the hazard is a reduced form for
   the marital surplus; its time path after his re-employment (PSID -0.027 / -0.037 / -0.050 at years 1 / 3 / 6, Black
   -0.037 / -0.053 / -0.074) is an untargeted test of the form; the husband's welfare after separation is not counted.
5. Solution paragraph (before `sec:estimation`): the SNAP asset test puts a notch in next month's value at the asset
   limit (1.884 thousand); the solver carries grid nodes at the limit, the corner a' = L as a candidate, a two-branch
   endogenous grid; footnote with check 0 (99th percentile 1.7e-4, max 2.6e-3 against 1e-3 / 5e-3) and `tests/`.
6. Estimation: (a) targets: the CPS entry and exit rates are persistence-filtered (old status in t-1 and t, new in
   t+1 and t+2, one rotation spell, husband employed in t and t+1), identical in data (`IGE/60`) and model; data exit
   0.0261 -> 0.0101, entry W 0.0751 -> 0.0320, B 0.0942 -> 0.0404. Footnote: the Poterba-Summers (1986) response-error
   correction was coded and tested (`--cps-classif`): exit 0.0243 against 0.0261 but entry 0.193 / 0.364 against
   0.075 / 0.094, and at the data's employment level the implied true entry rate is negative, so the filter replaces
   it. (b) `sigma_eps` fixed at 0.05: footnote with the profile (exit 0.26% -> 0.35% -> 0.29% -> 0.20% at 0.05 / 0.10
   / 0.20 / 0.30 against 2.6%; employment rises 0.95 -> 0.99). (c) The husband's employment rate by race is reported,
   not targeted (0.999 / 1.000 against 0.882 / 0.943; husbands leave work only by displacement) and the three pooled
   CPS rates and the three SIPP no-separation rows are in the fit table but not the objective (one reason each):
   85 of 91 moments. (d) Weights 1 / (se^2 + var_sim), var_sim from 5 CRN seeds. (e) Procedure: closed-form start,
   Jacobian, Levenberg-Marquardt polish, simulation noise at the candidate, CMA-ES around it with Jacobian-scaled
   steps and three seeds, pseudo-data recovery by the same route (`estimate.py polish --pseudo`); sandwich s.e.
   (f) Table `tab:model_params`: add eta_up under human capital (7); note that pi_c(2) is held at pi_c(1) at the
   estimation size (s = 1, 2 merged); re-check the count in the caption against `params.py` (31 free).
   Replace the sentence that still presents the exit rate as pinned by phi_F / phi_P alone with the current reading:
   the start misses it sevenfold; WP1's evidence decides the feature.

**Edits in `model_document.tex`** (same items in simulator order: `sec:labor` wages (eta_up), `sec:gov` budget
(wedge), `sec:labor` displacement (ridge start, c_mem option), `sec:marriage` (sentence), `sec:solution` (notch,
Hermite already there?), `sec:targets` (persistent flows; hemp and the six excluded rows marked), `sec:ident` /
`sec:build` (trim, weights, LM then CMA-ES, HPC job list with `Joint-` names), `sec:decisions` D19-D24: persistent
CPS flows; borrowing wedge; eta_up; ridge start / memory rejected; hemp reported only; sigma_eps fixed). Compile
`model_document.tex`. Commit both with their PDFs.

Deliverables: `paperA_joint_loss/sec7_model.tex`, `model_document.tex`, `main.pdf`, `model_document.pdf`.

## WP3. Post-estimation tooling, tested at the analytic start (sub-agent, 60-75 min, risk: none if Section 0 is obeyed)

**Goal.** When `paperA_model/results/hpc_runs/<run>/` arrives (`best.json`, `report.md`, `se.csv`, `moments.csv`,
`q_by_block.csv`, `iterations.csv`, `jacobian.npz`, `recovery_report.md`, `evals.csv.gz`), the tables and the two
marriage diagnostics should be one command each. All new files; nothing in Section 0 is edited; `inputs/` is never
written; `--apply` is never passed.

1. `paperA_model/fit_table.py <moments.csv> [--indep <moments.csv>] [--params best.json se.csv]` -> LaTeX in the
   paper's layout (one specification per column: data (s.e.), main model, independent-shock model, z; moments as rows;
   blocks as row panels; `in_objective = 0` rows marked 'reported'): `paperA_joint_loss/tab_model_fit.tex`,
   `tab_q_by_block.tex`, `tab_params_estimates.tex` (rows and order of `tab:model_params`: start, estimate, s.e.,
   bounds). Test on `results/evaluate_20261019_064228_p27000/moments.csv` (the start), compile a scratch wrapper.
   Also `recovery_table.py` from `recovery_report.md` -> `tab_recovery.tex` (parameter, truth, recovered, in noise
   s.e., in data s.e.).
2. `paperA_model/diagnostics_marriage.py --start <best.json>`: (A) one evaluation with sig_E = sig_N = 0 through
   the existing test override (`ov` in `model.py`), Q by block against the start on common draws (noise floor about
   30 units); (B) the simulated 'still with baseline wife' path by event year 1-6 by race from the stacked event panel
   `panels.py` already builds (no change to `moments.py`: compute the yearly coefficients from the returned panel),
   next to the PSID -0.027 / -0.037 / -0.050 (pooled) and -0.037 / -0.053 / -0.074 (Black) from `father_displacement.md`.
   Output `results/marriage_diag_<stamp>/` (json + md). Run once at the analytic start now (two evaluations, ~3 min)
   to debug; keep the output as the pre-estimate reference.
3. `paperA_model/counterfactuals.py --start <best.json> --size full`: scenario runner with the paper's scoring
   (consumption in the loss month and over 12 months, couple-months with no earner and with no earner and no credit,
   consumption-equivalent welfare at entry, by workplace match and race; main vs independent shocks). Implement now the
   scenarios that need only theta or schedule overrides: (i) pi_c = 0, m_H = 1; (ii) UI expiry 1/6 -> 1/12 and both
   spouses entitled at a joint loss, at estimated and doubled pi_c (schedule dict copy with `ui.expiry` changed; check
   in `model.py` which fields the entitlement rule reads before promising 'both entitled' without a code hook); (v)
   Black couples with White hazards, then the White separation response. Write (iii) EITC expansion vs equal-cost
   transfer and (iv) childcare subsidy as a documented scenario spec with the exact `model.py` hooks they need (a
   transfer term in the budget, a childcare price multiplier), to be coded behind flags after the CMA-ES jobs start.
   Smoke-test (i) and (v) at the analytic start at the default size (3-4 evaluations, ~5 min).
4. `bps_check.py` readiness: read `bps_reconciliation/HARNESS.md`, confirm `bps_on_sim.do` and the Stata path, then
   one smoke run at the analytic start with `--K 1` and **without `--apply`** (writes `results/bps_<stamp>/` only). Fill
   `BPS_RUN_PLACEHOLDER` in the README with the smoke numbers, flagged as 'start values, not estimates'.

Deliverables: the four scripts, `tab_*.tex` test outputs, `results/marriage_diag_*`, `results/bps_*`, README lines
under 'How to run' (the README is documentation, not code; editing it is fine). Commit.

## WP4. Two reduced-form checks the marriage note asked for (sub-agent, 30-40 min, risk: none)

M2b: the separation response ('still with baseline wife', years 1-3) interacted with state UI generosity (schedule
from `IGE/12b.UIGenerosity.py`: replacement cap and duration in the father's state-year) in `IGE/19`'s stacked design,
by race; M3: her displacement as the event in the same design, outcome 'still with baseline husband'. One new script
`IGE/64.SeparationUIAndHerLoss.py` importing `IGE/19` read only; outputs `output/separation_ui_her_loss.csv/.md`
with stars and p-values; plus the PSID path by event year 1-6 copied into one small csv for WP3.2 (`output/
bw_present_by_year.csv`). Deliverable: footnote sentences for sec7 (marriage paragraph) either way: if the UI
interaction is not significant, 'one sigma_J' stays with the number; if her displacement moves separations, M3 goes
on the PI's list. Commit.

## WP5. Housekeeping and the intake checklist (lead, 20-30 min, risk: none)

1. `paperA_model/results/INTAKE.md`: what to read first when `hpc_runs/` lands (recovery: count within 2 noise
   s.e. and 2 data s.e., the weakest directions in `report.md`; main: Q by block against 11,726, the exit rate, the
   employment level, `se.csv`), the exact next sbatch lines with `<gn>` filled from the run folder name
   (`Joint-noise`, then `Joint-smm-main` / `-s2` / `-s3` with `--noise-file`), the squeue format with full names,
   and the one-step-at-a-time rule (new moment set -> baseline first).
2. README: 'Open issues' item 2 (kappa_S) is resolved; item 4 points to WP1's memo; `BPS_RUN_PLACEHOLDER` from WP3.4.
3. Untracked files in `output/` (`log41-60.txt`, `cps_couple_state_shares.csv`,
   `policy_schedules_memory_version.json`) and `paperA_age_profile/model_document.pdf`: logs are scratch (git-ignore
   pattern `output/log*.txt`), the csv and json are Paper B / 61 by-products: leave them for the PI, list them in
   the summary. Commit the ignore rule only.
4. Final summary to the PI: Q state, what each WP produced, the decisions waiting (exit-rate feature from WP1; M2a/M2b
   from WP3.2 and WP4; counterfactual hooks (iii)-(iv) to code after CMA-ES starts).

## Timeline

| when | lead | sub-agent A | sub-agent B | sub-agent C |
|---|---|---|---|---|
| 0:00-0:10 | brief the three agents with Section 0 verbatim | WP1 starts | WP3 starts | WP4 starts |
| 0:10-1:30 | WP2 sec7 edits, compile, commit | WP1 SIPP + CPS | WP3.1-3.2, smoke runs | WP4, commit at ~0:45 |
| 1:30-2:30 | WP2 model document, compile, commit; read WP4 result into the marriage footnote | WP1 PSID, memo, commit | WP3.3-3.4, commit | |
| 2:30-3:00 | WP5; read WP1 memo and WP3 outputs; summary | | | |

If `hpc_runs/` arrives early (the test job pushes nothing; the first push is `Joint-recovery-gn` after ~4 h), the
intake checklist applies; do not start `Joint-noise` or CMA-ES lines without the PI (the PI submits).
