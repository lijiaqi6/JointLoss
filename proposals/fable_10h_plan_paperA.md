# Paper A: ten hours while the HPC queue is busy (2026-10-20, 00:30-10:30)

Read only, nothing run: `results/INTAKE.md`, `extensions_20261019.md`, `diagnostics_20261018.md`, `POSTESTIMATION.md`,
`marriage_diag_20261019_092447_p18108/`, `bps_20261019_13*/bps_check.json`, `bps_reconciliation/HARNESS.md`
(Sections 6-7) and `smoke_sim_dgp.py`, `IGE/60` (wealth block), `IGE/40` (SIPP loader), the three Fable notes of
2026-10-18/19 and `wife_exit_evidence.md`, `separation_ui_evidence.md`, `her_loss_robustness.md`, the paper
(`sec2`, `sec5`, `sec6`, `sec7`, `references.bib`), `EVIDENCE.md` Sections 3-6. Terminology: search friction; human
capital level / accumulation / depreciation.

## 0. The constraint, as a file list, and the state

Joint-recovery-gn 11865966 and Joint-gn-main 11865967 are queued on a snapshot of 78a45a5 (= HEAD's parent merge; the
working tree has no later change on the model path). Until the LM -> noise -> CMA-ES chain has started its CMA-ES
stage, **no edit** to `paperA_model/{model,solve,simulate,panels,moments,params,estimate,analytic_start,
borrowing_wedge,hpc_job_a,post_common}.py`, `inputs/*`, `tests/*`, `IGE/60-62`, `IGE/66`, `output/paperA_targets*.csv`;
no `bps_check.py --apply`; no run of `IGE/60`, `62`, `66`. Everything below is new scripts (`IGE/75-79`), new
`results/` and `output/` aggregates, Stata runs on scratch, and paper text. Each package ends with its own commit
on main (explicit paths, no branches, no PSID / SIPP / CPS microdata). Risk to the queued jobs is therefore **none** in
every package; the only shared resource is the PC's CPU and RAM (Section 1).

Results land ~01:30 tomorrow, outside this window: nothing here waits for them; everything here either (a) makes the
intake decisions one reading, (b) supplies model inputs the first estimate will need, or (c) moves the paper.

## 1. WP0. The local LM run: recommended, PI decides (5 minutes to launch)

`estimate.py polish --workers 7 --threads 2 --iters 15` from the analytic start on the PC reproduces Joint-gn-main
(same code, same CRN seed 20261018, same K = 3, same objective) about 16 hours earlier (~10:30 today vs ~01:30
tomorrow), and more if the Stanage queue slips. The PC's clean build gives Q 11,733.70 against Stanage's 11,733.6, so
the two runs are also a free cross-machine reproducibility check of the whole LM path (numba binaries are not
bit-stable; the agreement criterion is Q within the noise floor, ~30, and parameters within the sandwich s.e.).

Cost: 14 of 16 threads for ~10 hours (7 workers: the 63-evaluation CRN Jacobian takes 9 rounds, ~40 min per
iteration); RAM ~7 x 1.6-3 GB. The data packages below are single-threaded pandas / Stata and fit on the remaining two
cores if the two SIPP packages (WP3, WP6) are run one after the other, not together (the SIPP monthly panel is the
largest object in memory). What the local run excludes for ten hours: every local model evaluation (the optional
WP10). Rules: the HPC run stays the one reported in the paper unless it fails; the PC run is `polish_main_pc_<stamp>`
in `results/runs/`, used for the intake rehearsal (fit table, marriage diagnostics, `bps_check.py --K 3` at the
candidate, exit-feature reading) so that the real intake tomorrow is one reading. No polling: one completion signal
(`iterations.csv` row count = 15 or `report.md` exists).

If the PI says no: WP10 (local evaluations, ~1 h of 16 threads) moves into the timeline at 06:30.

## 2. Work packages in priority order

### WP1. The BPS deficit in his transitory variance: trim artefact or real? (sub-agent, Stata + Python, 60-75 min, 1 core)

**Why first.** INTAKE 2b applies a one-time correction after Joint-gn-main that raises sigma_nu_h from 0.166 to
0.20-0.22 because BPS's estimator on the simulated panel returns 0.006 (K = 1) / 0.013 (K = 3) against the input 0.0275.
The synthetic smoke test (HARNESS 6.2) already shows the harness recovers an i.i.d. annual transitory variance of
0.030 on BPS's own process, so the deficit is specific to the model's panel. HARNESS 6.2 also records that BPS's
jump trim halves the measured transitory variance (0.056 -> 0.028) and that the model's wage has discrete human
capital steps of 0.46-0.49 log points and a displacement loss d_h: a trim that drops large year-to-year wage
changes removes exactly the model's transitory-looking moves. If the deficit is the trim, applying the correction
would inflate the model's true transitory variance by 50%, and the PI's approved step must be re-read before it runs.

**Method.** (a) Re-run `bps_on_sim.do` on the K = 1 panel of `results/bps_20261019_133727/` (rewrite it with
`post_common.simulate_only` + `sim_panel_writer` if the scratch .dta is gone; ~1 min simulation, no `--apply`) under
three switch sets: BPS as shipped; jump trim off (`SW_*` global of `bps_on_sim.do`); jump trim off and measurement
error off. (b) `smoke_sim_dgp.py` variant with the model's wage process: one transitory draw per calendar year with
variance 0.0275 (D6), permanent moves as discrete steps of 0.46 log points at probability p_eps_h 0.004 + pi_up, a
10% displacement loss at 2.5% a year (keep the smoke's hours and consumption rules); run as shipped and with the trim
off; `verify_harness.py smoke`. Three to five Stata runs of 2-5 minutes each, sequential.

**Deliverables.** `bps_reconciliation/code/smoke_sim_dgp_steps.py` (new, imports the smoke module),
`bps_reconciliation/HARNESS.md` Section 8 (a table: spec x {s_u1, s_v1, s_u2, c_u1u2}, N trimmed by the jump rule),
`results/bps_trim_<stamp>/` (json), and one paragraph for `results/INTAKE.md` 2b with the decision rule: if the trim
explains the deficit, the correction is not applied and the paper's Appendix D says why BPS's trim understates his
transitory variance on a process with discrete steps; if not, 2b stands. Risk to HPC: none (reads results, writes
scratch and new files).

### WP2. Established wives' exits: what moves a wife off a job she has held a year? (sub-agent, 75-90 min, 1 core; SIPP first, then PSID)

**Why.** The largest misfit at the start is the persistent exit (0.14% vs 1.0% a month; Q 4,622 of 11,734), and the
extension table shows the model already *over*-predicts exits at tenure 0-5 months (0.035 vs 0.021) and misses 12+
(0.0027 vs 0.0068), so `--new-job` cannot close it; the gap is established wives. IGE/63 pooled all tenures. The PI
decides the feature after the first estimate; this package makes it one reading.

**Method.** `IGE/75.EstablishedWifeExits.py` (imports 63's loaders read only; 63's sample: married wives 25-59, husband
employed; persistent exit). SIPP 2004/08/14, tenure >= 12 months only: (i) shares x hazards and a joint LPM
(pp, household-clustered s.e., stars and p-values) on: child aged 0 at t+1..t+9, youngest child's age, usual hours
< 20 / 20-34, his job change t-2..t+1, his earnings change > 25% up / down, own illness (ERSEND), age 55-59, education,
race, panel x rotation x month FE; (ii) the share of 12+ exits each cell accounts for; (iii) KM return within 12 / 24
months of 12+ exits by reason and birth window; (iv) repeat exits among 12+ wives (an earlier exit in the panel).
PSID 1968-1996 annual (hours > 0 in t, 0 in t+1) with the same wife employed in t-1 and t-2 as the 'established'
proxy: birth in t / t+1, his income change, her hours in t, and the repeat-exit share. (v) The arithmetic the model
needs: what fraction of the 12+ hazard (0.68%) is births (child 0 window), low hours, his income rise, illness,
and the residual; the spell length of the residual.

**Deliverables.** `output/established_wife_exits.csv/.md` (paper layout), memo
`proposals/established_exit_evidence.md`: the decomposition, the feature each part points to (birth-timed theta
jump: no state; persistent work-cost type: one state, x2 solve; health: footnote), its cost, and the recommendation,
with footnote-ready sentences (numbers + script). EVIDENCE 3.93-3.95. Paper: sec7 'Estimation' footnote next to
the exit-rate paragraph (line ~451) after the estimate; sec5 'The wife's own labor market' one sentence.

### WP3. The separated wife's state: child support, remarriage, work (sub-agent, 60-75 min, 1 core, PSID)

**Why.** Marriage diagnostic (A): switching separation off cuts Q from 11,726 to 8,651 and closes 49-93% of the wives'
employment gap (0.954 -> 0.863 with no child; data 0.809), so at the start the anticipated separation keeps wives at
work. The model's V^S has no child support and no remarriage and is the terminal state of 67% of Black and 41% of
White couples: the marriage note's Diagnostic B asks for calibrated inputs, zero parameters. These are PSID facts
that must exist before the PI can decide, and they are paper footnotes either way.

**Method.** `IGE/76.SeparatedMothers.py` (person-year file via 19's / 21's loaders read only). Women 25-59 who were
married with a child 0-17 and whose marriage ended in the PSID window (1984-2021), by race: (i) child-support income
received (the PSID 'child support' item) in the years after the separation: mean, median, share positive, as a share
of her labor income and in 2000 $ a month; (ii) remarriage / new partner hazard by year since separation (KM, by
race); (iii) her employment and hours by year since separation against the married wives' 0.81 (the untargeted check
of V^S); (iv) AFDC/TANF and SNAP receipt by year since separation (the model's single-mother safety net); (v) the
same by whether her husband had been displaced in the two years before the separation (the model's post-displacement
separations). Stars and p-values on every difference.

**Deliverables.** `output/separated_mothers.csv/.md`, memo `proposals/separated_state_inputs.md` with the
two calibrated inputs ready for Diagnostic B (monthly child support by race x child count; annual remarriage hazard by
race, treated as the end of the record) and the single-mother employment and receipt rates as untargeted validation
rows for `fit_table.py`. EVIDENCE 3.96-3.98. Paper: sec7 'Marriage and separation' footnote (line ~302, "no remarriage
... no child support") carries the numbers; `model_document.tex` Section 11 the same.

### WP4. Wealth: is the age shape a model problem or a definition problem? (sub-agent, 60 min, 1 core, PSID)

**Why.** The wealth block (Q 2,702) misfits in shape: at 45-59 the model has 0.09 at or below zero liquid wealth
against 0.38, and 0.39 above a year of earnings against 0.18. The target is liquid wealth (checking / savings + stocks
- unsecured debt, `estimation/psid_wealth.py`), while the model's single asset also holds retirement and housing
saving. If PSID couples at 45-59 hold their saving in IRAs, pensions and home equity, the model is right about total
saving and the target is the wrong object; if the shares look the same under broader definitions, the model saves too
much late (the terminal value) and too little early.

**Method.** `IGE/77.WealthDefinitions.py` on the PSID wealth waves 1984, 1989, 1994, 1999-2021 (family files, the S
wealth variables; `psid_wealth.py` imported read only for the liquid construction), couples with the wife 25-59, by
age band 25-34 / 35-44 / 45-59 and race: shares <= 0 and > one year of the couple's labor income for (a) liquid as
targeted, (b) liquid + IRA / annuities (from 1999), (c) net worth excluding home equity, (d) net worth; home ownership
and mortgage shares by band; medians in 2000 $. Bootstrap s.e. (200, 1968-family clusters) only for the two targeted
definitions' shares; the rest descriptive.

**Deliverables.** `output/wealth_definitions.csv/.md`, a half-page in `proposals/wealth_shape_note.md` with a
recommendation (keep liquid and add a terminal-value / illiquid-saving footnote; or redefine the target as (b) or (c)
after the chain, since `IGE/60` cannot change now). Paper: sec7 'Estimation' wealth-target footnote; `fit_table`
reads the misfit with this note. EVIDENCE 3.99.

### WP5. Charles and Stephens (2004) and the novelty of 'her loss' (lead, 45 min, no CPU)

**Why.** The abstract, introduction (sec1 line 127), literature table (sec2 line 175) and sec5 say the wife's own job
loss ending marriages is new. Charles and Stephens (JOLE 2004) used the PSID with displacement of *either* spouse,
and Eliason (2012, Sweden) and Doiron and Mendolia (2012, BHPS) studied both spouses' job loss; whether they report a
wife's-loss effect decides the wording. The bib entry is also incomplete ("check: Charles's first name": Kerwin Kofi
Charles; also the `lindo2018caution` note).

**Method.** WebSearch / WebFetch of the three abstracts and, where open, the tables (the PDFs are not in
`IGE/literature/`); write the precise claim each makes about the wife's displacement. Rewrite the four passages so the
contribution is what is new here: the same stacked design for both spouses on one sample, the equal magnitude, the
widening after her hours recover, the closures comparison, who leaves, and the joint loss. Fix the bib entries.
Compile `main.tex`.

**Deliverables.** `sec1_introduction.tex`, `sec2_literature.tex` (paragraph + table row), `sec5_household.tex`,
`references.bib`, `main.pdf`; one line in EVIDENCE 'PI questions' (Q6 gets the literature position). Commit.

### WP6. The safety net around a joint loss: SNAP, UI, and where the EITC puts the couple (sub-agent, 90 min, 1 core; SIPP after WP2 has released memory)

**Why.** Counterfactual (iii) ranks an EITC-type subsidy against an equal-cost transfer on the claim that the subsidy
'pays least when both spouses have lost their jobs'. Section 5's safety-net subsection has one PSID number (SNAP +4.2
/ +3.3 points after his displacement) and the two SNAP level targets; nothing monthly, nothing on UI coverage of the
two spouses, nothing placing the couple on the EITC schedule. These are the facts the policy ranking stands on.

**Method.** `IGE/78.SafetyNetJointLoss.py`. SIPP 2004 / 2008 (40's loader with extra columns from the raw core files:
household food-stamp receipt and amount, each spouse's UI receipt and amount, by month; 2014 if the EHC has them):
event study in months around his job loss (40's INV definition) for (a) his loss alone and (b) a joint loss (her INV
within +-3 months): SNAP receipt and amount, UI receipt of him, of her, of neither; the share of joint-loss couple-
months with no earner and no UI; household-clustered s.e., stars and p-values. PSID couple-years (60's sample, read
through 60's cached objects or 19's loaders, not by running 60): with 61's EITC schedule (`inputs/schedules_era*.json`
read only), the share of couple-years in the phase-in / plateau / phase-out / above-range regions in the year before
and the year of (a) his displacement and (b) a joint displacement, by race; the mean credit change implied by the
schedule for each group (an accounting, not a receipt measure; TAXSIM is not needed for the region shares). AFDC/TANF
receipt in the same windows.

**Deliverables.** `output/safety_net_joint_loss.csv/.md/.png`; EVIDENCE 6.6-6.9. Paper: sec5 'The safety net'
grows from one paragraph to the subsection the PI rule wants (one subsection, details in footnotes), with the monthly
SNAP / UI path and the EITC-region shares; sec7 'Counterfactuals' (iii) cites the fact. Also a validation row list for
`fit_table.py` (SNAP receipt in joint-loss months; UI coverage of neither spouse).

### WP7. The children: the parents-present slope the child block needs, and the 'bounds' paragraph (sub-agent, 60 min, 1 core, PSID)

**Why.** Section 6 says the model's child block maps family income by childhood age and the presence of both parents
into adult outcomes with slopes from administrative estimates, high and low. The identification plan (line 259) lists
beta_P = the PSID association of the share of childhood with both parents present with adult log earnings, "to add" in
IGE/20; it does not exist. Without it counterfactual scoring on children cannot run when the estimate lands.

**Method.** `IGE/79.ParentsPresentOutcomes.py` (20's / 22's loaders read only). Children born 1968-1995 observed as
adults (25+): adult log earnings (mean 30-40 where available), rank, schooling on the share of childhood years 0-17
with both parents in the family unit, with Section 6's controls (pre-displacement parental income, sex, birth year,
race; no sibling comparisons), by race; a version splitting the years of absence by child age 0-5 / 6-17; the same
on the father's displacement sample so the two channels (income, presence) sit in one regression. Stars and
p-values; 1968-family clusters. Also read Hilger's (2016) earnings effect from the paper (WebFetch the AEJ:Applied
abstract / table if the PDF is not local) for the low slope.

**Deliverables.** `output/parents_present_outcomes.csv/.md`; the high / low slope numbers (beta_05, beta_617,
beta_P) written into `counterfactuals.py`'s docstring section 'Children's adult outcomes' (documentation, not code) and
into `proposals/paperA_identification_plan.md` line 259; sec6 'What the model takes from this' gets the numbers and
a footnote; EVIDENCE 5.11-5.12.

### WP8. Paper and model document in sync with the code (lead, 75 min, no CPU)

Items (all from committed results, nothing to run): (1) `EXPECTED_Q` is 11,733.7 from a clean build (d7f2d12); sec7
lines 451 and 460 and `model_document.tex` lines 881 and 1215 say 11,726 (also 12,761 -> re-check the comparison
figure's basis); footnote that numba binaries differ at 1e-3 relative across compilations and that Stanage gives
11,733.6. (2) The two pre-built extensions (`--new-job`, `--her-sep`) and their four targets (IGE/66): the model
document gets D25-D26 as *pending options* with the step-table numbers (base 13,232.5; new-job 13,245.7 with the
tenure block worsening 1,483 -> 1,801; her-sep 13,162.8, -0.001 -> -0.019 against -0.050) and the rule that they are
judged at the first estimate on the 89-moment set; sec7 gets one footnote in 'Marriage and separation' (her
displacement term, IGE/64-65) and one in 'Estimation' (tenure profile). (3) Marriage diagnostics at the start: the
sentence that the simulated separation gap flattens after year 3 while the PSID keeps widening (model -0.029 / -0.029 /
-0.039 vs -0.027 / -0.037 / -0.050 pooled) goes into 'Validation' as the stated untargeted test, with the M2a
alternative named. (4) 'Validation': add the single-mother rows (WP3) and the safety-net rows (WP6) as planned
untargeted checks. (5) sec6: WP7's numbers. (6) sec5 'The safety net': WP6's paragraph. (7) `tab:model_params`:
re-count against `params.py` (31 free + the two pending). Compile `main.tex` and `model_document.tex`; commit with
PDFs. Edits with the Edit tool only (no heredocs for LaTeX).

### WP9. Intake, EVIDENCE and housekeeping (lead, 30 min, no CPU)

(1) `results/INTAKE.md`: WP1's 2b decision rule; the exit-feature decision tree (new-job vs birth jump vs type, with
WP2's shares); Diagnostic B inputs from WP3; the WP4 wealth note; the local-run comparison protocol (Section 1).
(2) EVIDENCE.md: entries from WP2-WP7 (3.93-3.99, 5.11-5.12, 6.6-6.9) and the 'PI questions' table (Q6 position;
new Q9 'does the EITC pay in joint-loss months?'). (3) `.gitignore`: `output/log*.txt`; the other untracked
by-products (`cps_couple_state_shares.csv`, `policy_schedules_memory_version.json`, `rauh_replication*`,
`test_wrapper.*`, `paperB_age_profile/model_document.pdf`, `scripts/redraw_emp_event_by_edu.py`, the five modified
files under `paper/`, `ReducedForm/`, `TargetMoments/` belong to the other sessions) are listed for the PI, not
touched. (4) Summary to the PI.

### WP10 (only if WP0 is declined). Local model evaluations, 16 threads, 60 min

(a) Tenure-exit profile at the start on the 89-moment set: `estimate.py evaluate --ext-targets new_job her_sep` at
phi_F x {0.8, 1.0, 1.2} and theta_05 x {0.5, 1, 2} (6 evaluations, ~2.5 min each on 8 threads): does the 12+ exit
rate move with the work-cost parameters at all, or is it structurally pinned (then WP2's residual decides between the
birth jump and a type)? (b) Separated wives' employment, child-support-free, from one stored simulation
(`post_common.simulate_only`, new `results/sep_state_<stamp>/`) against WP3's PSID rate. (c) `counterfactuals.py
--scenarios base ii_ui12 --size k_s2_era1_a20` smoke (not yet run for (ii)). All write new `results/` folders only.

## 3. Timeline (10 hours; sub-agents A-D; the lead on WP5, WP8, WP9)

| when | lead | agent A | agent B | agent C | agent D |
|---|---|---|---|---|---|
| 00:30-00:40 | WP0 to the PI; launch the local LM if yes; brief A-D with Section 0 verbatim | WP1 starts (Stata) | WP2 starts (SIPP) | WP3 starts (PSID) | WP4 starts (PSID) |
| 00:40-02:15 | WP5 (literature check, rewrite, bib, compile, commit) | WP1 switch runs | WP2 SIPP tables | WP3 child support, remarriage | WP4 definitions table |
| 02:15-03:30 | WP8 items 1-3 (Q numbers, D25-D26, validation sentence) | WP1 smoke variant, HARNESS 8, INTAKE paragraph, commit ~02:30 | WP2 PSID, memo, commit ~03:00 | WP3 memo, commit ~02:45 | WP4 note, commit ~02:30 |
| 03:30-05:30 | read WP2-WP4 memos; WP8 items 4, 7; compile | WP7 (children slopes) | WP6 starts after WP2 has released memory (SIPP program variables) | - | - |
| 05:30-07:00 | WP8 items 5-6 from WP6-WP7 drafts as they land; compile both PDFs; commit | WP7 commit ~05:00 | WP6 PSID / EITC regions | - | - |
| 07:00-08:30 | WP9 INTAKE, EVIDENCE, .gitignore; commit | - | WP6 memo, commit ~07:30 | - | - |
| 08:30-10:30 | if WP0 yes: wait for the single completion signal (~10:30), then the intake rehearsal (`fit_table.py`, `diagnostics_marriage.py`, `bps_check.py --K 3` at the PC candidate, 40 min of 16 threads); if WP0 no: WP10 at 06:30 and the summary here | - | - | - | - |

RAM: WP2 then WP6 hold the SIPP panel (one at a time); WP3, WP4, WP7 hold the PSID person-year file (shared, light);
WP1 is one Stata instance. With the local LM at 7 x 2 threads the four agents share two cores: expect the SIPP
packages to take 1.3x the times above; the ordering absorbs it.

## 4. Where the results go

| result | paper location | also |
|---|---|---|
| WP1 trim test | Appendix D (BPS reconciliation): why the estimator understates his transitory variance on a process with discrete human capital steps, or confirmation that the correction is needed | `INTAKE.md` 2b decision; HARNESS 8 |
| WP2 established exits | sec7 'Estimation', the exit-rate paragraph (footnote with the 12+ decomposition and the feature chosen); sec5 'The wife's own labor market' one sentence | the exit-feature decision at intake; EVIDENCE 3.93-95 |
| WP3 separated state | sec7 'Marriage and separation' footnote (child support, remarriage, single-mother work); model document Section 11; 'Validation' untargeted rows | Diagnostic B inputs; EVIDENCE 3.96-98 |
| WP4 wealth definitions | sec7 'Estimation' wealth-target footnote; the fit discussion after the estimate | a target redefinition proposal for after the chain |
| WP5 literature | abstract (if the claim changes), sec1 contribution 4, sec2 paragraph + table row, sec5 'The marriage' | bib fixed |
| WP6 safety net | sec5 'The safety net' (full subsection with footnotes); sec7 'Counterfactuals' (iii) motivation; 'Validation' rows | EVIDENCE 6.6-9; Q9 |
| WP7 children | sec6 'What the model takes from this' (slopes with numbers); counterfactual child scoring spec | identification plan line 259; EVIDENCE 5.11-12 |
| WP8 sync | sec7 throughout; model document D25-D26, Q numbers | - |
| WP0 local LM (if run) | nothing in the paper; intake rehearsal | cross-machine LM reproducibility line in README |

## 5. PI rules checked against each package

Stars and p-values on every estimate (WP2, 3, 4, 6, 7); nulls stay in the text, failed designs in Appendix A; every
model choice from these facts gets a footnote with numbers and script (WP8 carries them); no sibling comparisons
(WP7); no balanced-panel restrictions (WP2-WP4 use all observed years); no region x year FE in WP6's policy facts (none
needed: event studies with household / family clusters); no restricted data (SIPP and PSID public files; Hilger and
the three divorce papers read from published tables); consumption moments untouched; one step at a time: the model
path and the moment set are not changed by any package, the pending extensions are judged at the first estimate on
one 89-moment set; parsimony: WP2-WP4 produce evidence for or against adding anything, not code.
