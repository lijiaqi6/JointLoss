# Paper B: three unattended hours, 09:10-12:10 (Fable, 2026-10-19)

Read: `sec7_model.tex` and the five model tables, `sec1`, `sec4`-`sec6c`, `sec8`, `model_document.tex` (targets,
lattice, validation, counterfactuals), `EVIDENCE.md` 11, `core.py`, `estimate.py`, `postestimation.py`,
`lattice_q.py`, `h4_seeds.py`, `tables.py`, `build_data.py`, `hpc_ige.sh`, `hpc_ige_chain.sh`, `output/final_x4/`
(lattice.md, h4_seeds.json, estimates_E.json), `postestimation_Lx4_E.md`, the smm_progress logs of all ten Lx4 jobs
and the E fit table of job 11861512. Nothing was run.

**Short answer.** Six blocks, about 15 minutes of local compute in all, every block a committed deliverable. In
order of value: (1) a 30-second check of whether model H (and G) were estimated at all, because H's log shows Q
unchanged over 12,000 evaluations; (2) the referee read of Section 8, which found one wrong-sample comparison, one
model/data ratio stated as if it were the data, and about ten smaller things, listed below with the fix for each;
(3) an untargeted-validation table from simulation at the estimate (racial wage gap by age, rank-rank slopes,
late-career access, the below-median opening, the between/within job-type split), computed by one function on the
PSID panel and on the simulated panel; (4) the H4 counterfactual by age band and parental tercile, plus the
counterfactual that replaces the back-of-envelope "0.21 of the 0.27" sentence with a model number; (5) the
Andrews-Gentzkow-Shapiro sensitivity of the four race parameters from the saved Jacobians (no simulation);
(6) prepared HPC work: a polish round for the ten lattice solutions (the fix for H and G), and the next model step
(race-specific search friction out of work) as tested code with the exact sbatch lines. Skipped: NLSY79 cohort
simulation, earnings IGE, private-sector opening, IPW moments, block-balanced weights (reasons in Section 4).

Rules that bind every block: numbers in tables come from json through `tables.py`, never typed; stars and p-values
on every estimate; "human capital accumulation", "search friction"; no person-level files in git (only aggregates
under `output/final_x4/`); commit and push (merge-tree, no rebase) at the end of every block; compile `main.tex`
before each paper commit; nulls go in the text.

## 0. Timetable

| Time | Block | Local compute | Deliverable |
|---|---|---|---|
| 09:10-09:20 | 0. Setup: `git pull`, confirm the tree is clean, `pdflatex main.tex` compiles as is | none | a known-good starting point |
| 09:20-09:35 | 1. Were H and G estimated? One-dimensional profiles of Q | 18 evaluations (about 30 s wall with 6 workers) | `output/final_x4/profile_q.json`, one sentence in the hypothesis-table note |
| 09:35-10:15 | 2. Referee read of Section 8 against the paper: the fixes in Section 2 below | none | edits to `sec7_model.tex`, `sec1`, `sec8`, `tables.py` notes |
| 10:15-10:50 | 3. Untargeted validation table | 300 bootstrap draws of a cheap statistic on the PSID panel (1-2 min) + 10 simulations (20 s) | `core.validation`, `output/validation_psid.json`, `output/final_x4/validation_E.json`, `tab_model_untargeted.tex`, a paragraph after "Fit", EVIDENCE 11.9 |
| 10:50-11:25 | 4. H4 counterfactual by age and tercile; gamma_x = 0 for both races | about 165 simulations (5 min) + Jacobian (1.5 min) | `postestimation.py` extended, `output/postestimation_Lx4_E_h4.json`, `tab_model_cf_h4.tex`, two paragraphs, EVIDENCE 11.10 |
| 11:25-11:45 | 5. AGS sensitivity from the saved Jacobians | none | `sensitivity.py`, `output/final_x4/sensitivity.json`, `tab_model_sens.tex` (appendix), three sentences in "Identification", EVIDENCE 11.11 |
| 11:45-12:05 | 6. HPC preparation: polish round, the `ufric` step, `fix_seeds.py` | 1 invariance evaluation + a 2-3 min SMM_TEST | code committed, commands in Section 5 verified against `hpc_ige.sh` |
| 12:05-12:10 | 7. Compile, commit, push; status note for the PI | none | |

If a block overruns: drop 5 first, then cut 3 to statistics (a) and (d). Never cut 1 or 6: they decide what the PI
submits at 12:10.

## 1. Block 1: were models H and G estimated? (09:20-09:35)

**What the logs say.** `hpc_runs/Lx4_H_j11861511/smm_progress_log.txt`: start Q 134.98 (model B's solution), best
Q 134.98 at 300, 3,000, 6,000, 9,000 and 12,000 evaluations; stop on `maxfevals`. Twelve thousand CMA-ES
evaluations with sigma_0 = 0.5 found no point better than the start. `Lx4_G`: 138.35 at the start, 138.35 until
6,000, 138.22 at 12,000. Every other model moved by 0.5 to 8.8. The explanation is the warm start: sigma_0 = 0.5
times the parameter scales perturbs 24 polished parameters by several standard errors in every sample (b_0 by
0.15 against a s.e. of 0.05, mu_B by 0.1 against 0.025), so every candidate is worse than the start until CMA-ES
has shrunk its step, and the budget ran out first. All ten Lx4 jobs ran with `IGE_POLISH=0` (summary.txt), so the
4,000-evaluation polish at sigma 0.15 of the chain design was not applied. This is an optimiser problem, not a
model result, and the hypothesis-table note currently presents it as a result ("12,000 evaluations found no better
point").

**What depends on it.** Rows B -> H (H3 given H1: 0.0), G -> H (H1 given H3: 2.9) and H -> D (H2 given H1 and H3:
8.5) in `tab_model_hyp`, and the sentence "8.5 and 7.5 given H1 as well" in the verdict. The selected model and the
verdict do not: F -> E (9.9), G -> E (8.5), E -> D (1.4) and the H4 rows do not pass through H. But G is the
"without" model of G -> E, and if G is under-converged the H2-given-H3 drop of 9.9 is an upper bound.

**Do.** A 25-line `model/profile_q.py`: for (run, model, parameter, grid) evaluate Q at the estimation draws
(seed 7, `IGE_R=20`, `IGE_STEPS=age,rehire,xacc`, `IGE_FIX=muG,du`) with that parameter set to each grid value and
the rest at the run's estimate; `Pool(6)` over `est.eval_task`. Three profiles:
- H at B's theta, `db1` in {-0.04, -0.02, -0.01, 0.01, 0.02, 0.04} (the "without" model's solution is the point
  CMA-ES never left);
- G at A's theta, `db1` on the same grid;
- D at E's theta, `a3` in {-0.4, -0.2, -0.1, 0.1, 0.2, 0.4} (E -> D found 0.5; is there more?).
Write `output/final_x4/profile_q.json` (grid, Q, the base Q). Commit.

**Verify.** The base Q must reproduce the json values (134.98, 138.35, 127.62) to 0.01: same draws, same code.
Reading: if any grid point is below the base by more than 0.5, H (or G, D) is under-converged and the polish jobs in
Section 5 are not optional; put one sentence in the `tab_model_hyp` note through `tables.py`: "Models G and H
moved by 0.1 and 0.0 from their starting points in 12,000 evaluations; the one-dimensional profile of Q in
b_1(B) - b_1(W) at H's start falls by [x] at [value], so the rows through H are upper bounds on the drops until the
polish re-estimation (pending)". If no grid point is lower, the note says that instead, with the numbers, and the
rows stand.

## 2. Block 2: referee read of Section 8 (09:35-10:15)

Ordered by what a referee would hit first. Each item: the problem, where, the fix. Items 1-6 are substantive;
7-14 are consistency; 15-17 are wording.

1. **Model H not estimated** (Block 1). Fix the note as above; keep the text's "8.5 and 7.5 given H1 as well" only
   with "(upper bounds, see the table note)" until the polish lands.

2. **"A policy scored at 30 sees 60% of the gap that a policy scored at 45 must close"** (end of Counterfactuals).
   0.169 / 0.282 = 0.60 is the model's ratio; the PSID's is 0.153 / 0.330 = 0.46, and the model's 30-34 gap is above
   the data and its 45-49 gap below. Write: "In the model a policy scored at 30 sees 60 percent of the gap at 45; in
   the PSID 46 percent (0.153 of 0.330), because the model opens the gap earlier than the data and closes it less
   by 45-49 (Table modelfit)". The abstract and conclusion do not quote the 60 percent; check `sec6c` ("overstates
   its effect at 45") is unaffected.

3. **Three values for the same-employer gradient of White sons and two for Black sons, no reconciliation.**
   Section 6 (Table growthladder, with age quartic and year effects): White 0.021*** (0.006), Black 0.003 (0.008),
   net of schooling 0.008 (p = 0.17). Section 8 hypothesis list: "White 0.020***, almost all of it with the same
   employer; Black -0.001" (Table jobmoves, all pairs). Section 8 Fit: 0.019*** (0.006) / 0.007 (0.008), net of
   schooling 0.006 (0.006) / 0.005 (0.009) (`untargeted_psid.json`, the model's stayer sample, no controls). A
   referee reads 0.003 and 0.007 for the Black gradient two sections apart. Fix: one footnote at the Fit sentence:
   "The model's stayer statistic is computed on the model's pairs (consecutive interviews one to two years apart
   from 1985, same employer, no displacement, valid wages at both, ages 25-34), without the age and year controls of
   Table growthladder, whose values on its own sample are 0.021*** (0.006) and 0.003 (0.008); the difference is the
   sample and the controls, and the model is compared with the statistic computed the same way on its own sample".
   And in the hypothesis list, say "(Table jobmoves, all pairs)" after the 0.020 / -0.001.

4. **The 0.21 back-of-envelope.** "Cumulated over the career ... the White pay-off adds about 0.21 to the log wage
   at 45 per log point of parental income, most of the rise of the White IGE between 25-29 and 45-49 (0.27 in the
   PSID)". The sum assumes employment every year from 18, ignores the regression's partialling by age and the
   model's own White rise (0.461 - 0.222 = 0.24, not 0.27), and mixes a model calculation with a data rise. Block 4
   replaces it with the counterfactual gamma_x = 0 for both races: "switching off the pay-off of parental income in
   accumulation for both races lowers the White IGE at 45-49 from 0.461 to [x] (change [d]***, s.e. [s]), [share] of
   its rise from 25-29 in the model". Until then, change "0.27 in the PSID" to "0.24 in the model, 0.27 in the
   PSID" and "most of" to the number.

5. **alpha_3 is marginally significant alone** (-0.274*, s.e. 0.153, p = 0.07 in B; the same in H; `lattice.md`'s
   fresh R = 5 Jacobian gives p = 0.05). The text reports only the richest model (p = 0.44). A referee will say
   "H1 is rejected by a Q rule but the Wald test says otherwise in half the models". Add to the H1 paragraph: "Alone,
   alpha_3 = -0.27 (s.e. 0.15, p = 0.07) with a drop of 3.2; it shrinks to -0.14 (p = 0.44) and 1.4 once the
   schooling parameters are in, because without them a lower Black access is the model's only way to flatten the
   Black return to schooling with age; the Q rule and the Wald test agree in the models that contain H2 and H3".

6. **"Why a job side" lists a fact the model does not reproduce.** The fourth fact, "Black sons of richer parents
   gain less when they change employers (Table jobmoves)", is a misfit of the selected model: wage growth at a
   move for Black sons is +0.060 against -0.006 (t = +3.5) and its parental-income slope +0.012 against -0.016
   (t = +2.1); the model has no race x parental-income term at moves. Rephrase: "...and the model with a job side
   can be asked to reproduce them; it reproduces the first three and not the fourth (Section 'What the model
   leaves open')". The paragraph should promise what the model is asked, not what it achieves.

7. **The opening sentence's numbers are wage gaps on the model sample**; Section 4's headline is earnings (-0.041 at
   25-29, 0.299 at 45-49) and Section 5's is the wage gradient 25-34 / 35-44 (0.094 -> 0.240). "0.056 at 25-29" next
   to "zero at 25-29" in the abstract needs the half-sentence: "in the hourly wage, on the model's sample of male
   heads with a wage (Table modelid); the earnings gap is zero at 25-29 because hours raise the Black elasticity at
   young ages (Section 5)".

8. **"estimates every combination of them"** (Section 8 intro; Section 1, "estimates every combination of them on
   the same 66 moments"). H4 is tested at A and E only (ten models, not sixteen). Say "every combination of H1-H3,
   with and without H4 at the two ends of the lattice" in both places.

9. **The intro and conclusion say access is unequal "by race at equal parental income" and that the model
   "rejects a racial difference in access".** Both are true and a referee will call it a contradiction unless the
   bridge is there: the 4.2-point gap is a fact the race-neutral access function reproduces (model W - B share at
   equal tercile: 0.015 in the bottom, 0.082 in the top tercile, against 0.035 and 0.063 in the PSID) through
   schooling, acceptance and job loss. Add one clause in the intro (line 70-72) and the conclusion (line 9 and 26):
   "a racial difference in offers of good jobs is rejected: the lower Black share at equal parental income is
   reproduced without one".

10. **Lattice-table note**: the gaps and the IGE-block Q are at the estimation draws (E: 0.169 / 0.282 / 4.9) while
    `lattice.md`'s seed means are 0.164 / 0.282 / 4.7; add "at the estimation draws" to the note in `tables.py`.

11. **"Standard errors ... \citep{andrews2017measuring}"** in the Estimation paragraph: AGS is the sensitivity
    paper, not the source of sandwich SMM standard errors. Cite \citet{gourieroux1993indirect} or Newey-McFadden
    (check `references.bib`; if neither is there, drop the citation and keep the formula in the table note). Keep
    the AGS citation for Block 5.

12. **Closed-form starting values versus estimates**: gamma_1 = 0.023*** by NLS on stayers' growth against
    0.0126*** (W) in the SMM; gamma_O 0.123 vs 0.092, gamma_G 0.145 vs 0.172. A referee asks why the "check" is
    off by a factor of two. One footnote: the NLS pools races and uses the pair's mid-age; the SMM's gamma_1 must
    also fit the six return-to-schooling bands and the stayer slope on schooling (data 0.009, model 0.007), and the
    starting values are starts, not estimates. If time is short, leave for the model document.

13. **"widens the gap slightly (0.006**, p = 0.047)"** for equal displacement risk: house rule, never qualify a
    precise estimate as small. "widens the gap by 0.006** at 45-49, two percent of it, while raising Black wages
    by 0.033".

14. **The hypothesis table's last column uses the R = 20 estimation Jacobian; `lattice.md` uses a fresh R = 5
    Jacobian** (db1 in E: 0.0138 vs 0.0147). The paper is consistent (R = 20 everywhere) and the note says so;
    nothing to change, but EVIDENCE 11.2 quotes p = 0.007 and lattice.md p = 0.012: add "(R = 20 Jacobian)" to
    EVIDENCE 11.2.

15. The identification paragraph's one-liner ("H4 the rise of the IGE with age at a given return to schooling")
    is replaced by Block 5's three sentences with the sensitivity numbers (rule: explain identification fully).

16. "What the model leaves open": the variance misfit sentence "probably through attrition" is one hedge too
    many for the house rule; "which falls in the data between 35-39 and 45-49 (0.382 to 0.345), a fall the model,
    which has no exit from the sample of heads with a wage, cannot produce" states the mechanism without hedging.

17. Terminology sweep of `sec7_model.tex` for "offer rate", "arrival", "rung", "ladder", "promotion": none found
    in the model prose; `tab:growthladder` is a label only. Nothing to do.

Compile after the edits; commit as "Paper B Section 8: referee fixes (H under-convergence note, model/data ratio,
stayer-sample footnote, alpha_3 alone, job-side facts, wage-gap sample, lattice note)".

## 3. Blocks 3-5: what needs only the estimate

### Block 3: untargeted validation from simulation at E (10:15-10:50)

One function `core.validation(P, C)` next to `core.untargeted`, applied to the PSID panel (`output/data_panel.pkl`,
local, git-ignored) and to the simulated panel, so the comparison is on the same sample and code. Statistics
(each by race):
- (a) mean log wage at 35-39 and 45-49 (the racial wage gap by age; targeted only at 25-29, 0.279). The Black-White
  gap widening with experience is the Lang-Manove / Oettinger fact and the model's mu_B is a level; whether the gap
  widens in the model comes from the accumulation parameters.
- (b) rank-rank slope of the son's within-band percentile rank of the log wage (ranks over both races in the band,
  valid wages) on the percentile rank of parental income among sons in the band, at 25-29, 30-34 and 45-49. The
  paper's claim is that ranks register a smaller part of the opening (Section 4, Table rankage); does the model
  reproduce that with its log parameters? Expect a partial pass: the data's own-earnings rank gap does open at
  40-44 (0.150*).
- (c) share whose modal job at 35-55 is G, by race and parental tercile (the late access gradient; targeted only at
  25-34).
- (d) the log-wage gradient among sons below the pooled median of parental income, by race, at 25-29 and 45-49: the
  "race or position" question of Section 4. The model is linear in x, so its below-median opening should match its
  full-sample opening; the PSID's below-median earnings opening is 0.13-0.23 against 0.23. If the model fails here,
  say so in the text: it is a null that bounds H4's linearity.
- (e) the between/within job-type split of the gradient: the drop in the x coefficient when a G dummy is added, by
  race, at 25-34 and 35-55. Compare only with the same G/O split on the PSID panel, not with Table careerdecomp's
  occupation scores (finer classification, different object); one sentence relates the two.

Data side: a 30-line `model/validation_psid.py` reusing `build_data.bootstrap` with the moment function
parametrised (add a `fn=core.moments` argument; 300 draws, seed 2026); writes `output/validation_psid.json`
(aggregates: value, s.e., p; commit it). Model side: `lattice_q.q_task`-style evaluation of model E at seeds 7-16,
R = 20, mean and seed s.d.; `output/final_x4/validation_E.json`. `tables.py` gains `tab_untargeted()` ->
`tab_model_untargeted.tex` (PSID (s.e.) | model (seed s.d.) | t). Paper: a paragraph after "Fit" that reports every
row, passes and failures alike, and EVIDENCE 11.9.

Verify: on the PSID panel the function's mean log wage at 25-29 must equal `data_moments.json` (2.3154 / 2.5947) and
its G shares at 25-34 (if computed as a check) the G_t moments; on the model at seed 7 the same checks against
`estimates_E.json`'s moments. Compute: 300 x (a cheap statistic on 46,540 rows) + 10 simulations.

### Block 4: the H4 counterfactual a policy reader can use (10:50-11:25)

`postestimation.py`: (i) `outcomes()` adds the IGE by race and the W - B gap at all six bands, and the mean log
wage of Black and White sons by parental tercile (C["terc"]) at 25-34 and 45-49; (ii) `CFS` adds "No pay-off of
parental income in accumulation (gx = dgx = 0)"; (iii) an env `IGE_CFS` (comma-separated names) restricts the
experiments run, so this block runs three (Baseline, H4 off, gx = 0) and not nine; (iv) the gradient vectors `g`
are saved per experiment and key (needed for the AGS sensitivity of the counterfactuals in Block 5 and free).
Run with `IGE_STEPS=age,rehire,xacc IGE_FIX=muG,du IGE_R=20 IGE_SELECT=E IGE_OUT=<scratch folder>` where the
scratch folder holds a copy of `final_x4/estimates_E.json` named `estimates.json` (the file has no "selected" key,
hence `IGE_SELECT=E`). Copy the result to `output/postestimation_Lx4_E_h4.json`; `tables.py` gains
`tab_cf_h4()` -> `tab_model_cf_h4.tex`: panel A, by age band: Black IGE baseline, change with H4 off (s.e.), W - B
gap baseline, change; panel B, mean log wage of Black sons by tercile at 25-34 and 45-49: baseline, change with H4
off (s.e.) (expect bottom tercile down, top tercile up, since x is centred at the pooled mean); panel C, gamma_x = 0
for both races: White IGE by band, change (s.e.).

Paper: replace the 0.21 sentence (item 4) with panel C's number; add a paragraph "Which sons, which ages" after
the counterfactual table: the H4 decomposition raises the Black IGE at every band from 30-34 on, closes [x] of the
gap at 35-39 and [y] at 50-55; it raises the wage of Black sons from the top tercile at 45-49 by [a] and lowers that
of the bottom tercile by [b]; the sons it moves are the sons of richer Black parents, which is where the data's
downward mobility is (Section 4). EVIDENCE 11.10.

Verify: the Baseline and H4-off rows must reproduce `postestimation_Lx4_E.json` exactly (0.169 / 0.282; -0.124 /
-0.171; s.e. 0.033 / 0.046): same draws, same Jacobian steps. Compute: 3 experiments x (1 + 2 x 27) = 165
simulations plus the 54 Jacobian simulations, about 7 minutes with 6 workers.

### Block 5: AGS sensitivity from the saved Jacobians (11:25-11:45)

`model/sensitivity.py`: for E (and D for alpha_3) read `jacobian`, `jac_names`, `se` from
`final_x4/estimates_<M>.json`, `sd` from `data_moments.json`; Lambda = -(G'WG)^{-1} G'W with W = diag(1/sd^2);
S_jk = Lambda_jk sd_k / se_j, the shift of parameter j in its own standard errors when moment k moves by one data
standard error. Report for dgx, gx, dg1, db1 (E) and a3 (D): the share of sum_k S_jk^2 in each of the seven moment
blocks (`lattice_q.BLOCKS`), and the six moments with the largest |S_jk| with sign. With the Block 4 gradients,
also the sensitivity of the H4-off gap change at 45-49: g' Lambda (1 x 66), same scaling. Writes
`output/final_x4/sensitivity.json`; `tables.py` gains `tab_sens()` -> `tab_model_sens.tex` (appendix, with the
\input in `appB.tex` or a new model appendix).

Paper, in "Identification and estimation", replacing the one-liner (item 15): which moments move each race
parameter and why that is the right moment: dgx should load on the Black IGE at 35-55 (negatively: a higher
late Black IGE in the data would mean a less negative dgx) and on gx through the White IGE; db1 and dg1 on the
level and slope of the Black return-to-schooling bands (Jacobian column correlation 0.92 at the start, the paper's
"identified jointly" claim, now with its numbers); gx separated from bx (correlation 0.92) by the age profile: bx
moves every IGE band equally, gx the slope. EVIDENCE 11.11. Verify: Lambda G = -I to 1e-8; the signs above.

## 4. Candidates skipped, and why

- NLSY79 / NLSY97 cohort profiles: the model simulates each PSID son with his own characteristics; an NLSY79
  simulation needs an NLSY79 types file (race, parental income on the NLSY's three-year measure, schooling, birth
  year) and a reliability adjustment for its parental measure. Half a day of data work, not three hours; and the
  NLSY79 opening is 0.04-0.09 against the PSID's 0.21, so the comparison would need the measurement correction of
  Section 4 built in. Later, as a model-document item.
- Earnings IGE: the model has no hours; Section 5 shows hours carry 0.010-0.012 of the elasticity at 40. Nothing
  to validate that the wage IGE does not already.
- Opening among private-sector starters: no sector in the model; the data say the sector does not carry the
  divergence; there is nothing for the model to predict.
- IPW moments: the attrition weights are not in `data_panel.pkl` (no script in `IGE/` builds a per-son-year weight
  under that name; Section 4's IPW result lives in `33.AgeProfileRobustness.py`); merging them is data work, and a
  new moment set means the baseline is re-estimated first (one-step rule). It is the decisive robustness for H4
  (the Black 45-49 variance misfit is attrition-shaped), so it is the HPC step after the one prepared today.
- Block-balanced weights: the referee's worry ("the fact you explain has almost no weight in Q") is answered
  already: the twelve IGE moments contribute 4.9 to Q of 127.6 because they are fitted within their standard
  errors, and their low weight is their imprecision, not a choice. One sentence in the Estimation paragraph says
  this; a re-estimation with block weights would be a robustness row later, not today.
- Any local re-estimation: 12,000 evaluations at R = 20 on 6 cores is five hours. No.
- Full-covariance weighting: as before, no (a 66 x 66 inverse from 500 draws).

## 5. Block 6: HPC preparation (11:45-12:05) and the commands for 12:10

### 6a. Code: the polish round needs no code

`estimate.py` already takes `IGE_SIG0` and `IGE_START` with several candidates (the best after restriction is
used). Nothing to change. The chain script's polish (`IGE_POLISH=4000`) was not applied in Lx4; the jobs below
apply it as a separate stage, each model from its own solution plus the restricted solutions of the models above
it (a candidate from above can only help; nesting from below already holds).

### 6b. Code: the next model step, `ufric` (race-specific search friction out of work)

Why this step: the two largest remaining misfits are the zero-hours shares (Black too few, t = -3.8; White too
many, +3.4) with the displacement rates fitted (|t| < 2), so the model cannot reach the data's ratio of
non-employment (2.8) with its ratio of displacement (1.7) through a common job-finding rate. One parameter, no new
moments, no new draws:
- `core.py`: `EXTRA += ["dlu"] if "ufric" in STEPS`; a helper `lam_u_of(q, T)` returning
  `logistic(q["llam_u"] + q.get("dlu", 0.0) * T.black)` (shape n); in `solve`, `lam_u` becomes that vector
  (`np.minimum(lam_u, UCAP)`; the `lost` and `vU` lines broadcast as written); in `simulate`,
  `lu = np.minimum(UCAP, lam_u_of(q, T)[idx] * np.exp(CAL["phi_lam"] * ut))`. The draws `D.uo` are used exactly as
  before, so common random numbers are preserved.
- `estimate.py`: `SCALE["dlu"] = 0.5`. `theta_vec` already fills missing EXTRA parameters with 0, so E's
  `estimates.json` is a valid start.
- `fix_seeds.py`, a generalisation of `h4_seeds.py` taking `--with <run>:<M> --without <run>:<M> --label <text>`
  on the command line (ten seeds, R = 20, Q and gap at 45-49, drop mean / s.d. / min / pass_all), writing
  `output/final_x4/<label>_seeds.json`. Re-running it on the four H4 runs must reproduce `h4_seeds.json`
  (40 simulations, about 70 s; optional if time is short, mandatory before `tables.py` reads the new file).
- `hpc_ige.sh` needs no change (`IGE_STEPS` is passed through as a string).

Local tests, in this order: (1) invariance: Q at E's theta with `IGE_STEPS=age,rehire,xacc,ufric` and dlu = 0 must
equal 127.6226 to 1e-6 (one evaluation); (2) `SMM_TEST=1 IGE_STEPS=age,rehire,xacc,ufric IGE_FIX=muG,du IGE_R=5
IGE_MODELS=E IGE_START=output/final_x4/estimates_E.json:E IGE_OUT=<scratch> python estimate.py` runs end to end
(36 evaluations plus the Jacobian, 2-3 minutes) and `postestimation.py` after it. Commit as "IGE model step 5
(ufric): race-specific search friction out of work, dlu; fix_seeds.py".

### 6c. Commands for the PI at 12:10 (from `~/ige`, after `git pull`)

Stage 1, the polish round (ten jobs, about 25 minutes each at 32 cores; sigma 0.15, 4,000 evaluations, R = 20,
from each model's own solution plus the restricted solutions of its neighbours above). Job names `IGE-P-<model>`.

```
cd ~/ige && git pull
R=hpc_runs
S="IGE_STEPS=age,rehire,xacc IGE_FIX=muG,du IGE_R=20 IGE_SIG0=0.15 IGE_MAXFEV=4000,4000,4000,4000,4000,4000,4000,4000"
C="--time=01:00:00 --mem=24G"
sbatch $C --job-name=IGE-P-A model/hpc_ige.sh full IGE_MODELS=A IGE_RUN=P_A IGE_START=$R/Lx4_A_j11861506/estimates.json:A,$R/Lx4_E_j11861512/estimates.json:E $S
sbatch $C --job-name=IGE-P-B model/hpc_ige.sh full IGE_MODELS=B IGE_RUN=P_B IGE_START=$R/Lx4_B_j11861507/estimates.json:B,$R/Lx4_D_j11861513/estimates.json:D $S
sbatch $C --job-name=IGE-P-F model/hpc_ige.sh full IGE_MODELS=F IGE_RUN=P_F IGE_START=$R/Lx4_F_j11861508/estimates.json:F,$R/Lx4_E_j11861512/estimates.json:E $S
sbatch $C --job-name=IGE-P-G model/hpc_ige.sh full IGE_MODELS=G IGE_RUN=P_G IGE_START=$R/Lx4_G_j11861509/estimates.json:G,$R/Lx4_E_j11861512/estimates.json:E $S
sbatch $C --job-name=IGE-P-C model/hpc_ige.sh full IGE_MODELS=C IGE_RUN=P_C IGE_START=$R/Lx4_C_j11861510/estimates.json:C,$R/Lx4_D_j11861513/estimates.json:D $S
sbatch $C --job-name=IGE-P-H model/hpc_ige.sh full IGE_MODELS=H IGE_RUN=P_H IGE_START=$R/Lx4_H_j11861511/estimates.json:H,$R/Lx4_D_j11861513/estimates.json:D,$R/Lx4_G_j11861509/estimates.json:G $S
sbatch $C --job-name=IGE-P-E model/hpc_ige.sh full IGE_MODELS=E IGE_RUN=P_E IGE_START=$R/Lx4_E_j11861512/estimates.json:E,$R/Lx4_D_j11861513/estimates.json:D $S
sbatch $C --job-name=IGE-P-D model/hpc_ige.sh full IGE_MODELS=D IGE_RUN=P_D IGE_START=$R/Lx4_D_j11861513/estimates.json:D $S
sbatch $C --job-name=IGE-P-AnoH4 model/hpc_ige.sh full IGE_MODELS=A IGE_RUN=P_AnoH4 IGE_START=$R/ige_full_20261018_224720_j11861515/estimates.json:A IGE_STEPS=age,rehire,xacc IGE_FIX=muG,du,dgx IGE_R=20 IGE_SIG0=0.15 IGE_MAXFEV=4000,4000,4000,4000,4000,4000,4000,4000
sbatch $C --job-name=IGE-P-EnoH4 model/hpc_ige.sh full IGE_MODELS=E IGE_RUN=P_EnoH4 IGE_START=$R/ige_full_20261018_224720_j11861516/estimates.json:E IGE_STEPS=age,rehire,xacc IGE_FIX=muG,du,dgx IGE_R=20 IGE_SIG0=0.15 IGE_MAXFEV=4000,4000,4000,4000,4000,4000,4000,4000
squeue -u $USER -o "%.10i %.25j %.8T %.10M %R"
```

(The `IGE_START` candidates from D for B, C, H and E, and from E for A, F, G, are restricted by `estimate.py` to the
model's own free set before Q is compared, so they are legitimate starts; the one with the lower Q is used. The
`IGE_MAXFEV` list is positional over A-H, hence eight entries. Each estimation job runs `postestimation.py` at the
end, so P_E delivers the Block 4 decomposition on the polished estimate for free if Block 4 is committed first.)

Stage 2, when all ten have pushed: the lattice on common draws (one job) and, locally, the H4 seeds with
`fix_seeds.py`, then `tables.py` and the Section 8 numbers. The polished folders are named `P_<model>_j<job>`:

```
cd ~/ige && git pull
L=""; for m in A B F G C H E D; do L="$L hpc_runs/$(ls hpc_runs | grep ^P_${m}_j)"; done
sbatch --job-name=IGE-P-lattice --mem=32G --time=02:00:00 model/hpc_ige.sh lattice IGE_RUNS="${L# }" IGE_STEPS=age,rehire,xacc IGE_FIX=muG,du
```

Locally afterwards: `python fix_seeds.py --with hpc_runs/P_A_j...:A --without hpc_runs/P_AnoH4_j...:A --label h4_alone`
and the E pair; copy the eight polished `estimates.json` into `output/final_x4/` (aggregates only), rerun
`tables.py`, re-read the verdict numbers in `sec7_model.tex`.

Stage 3, the next model step (two jobs, submit after P_E and P_A have pushed, or chain with
`--dependency=afterok`): E and A with the race-specific search friction out of work, from the polished solutions,
sigma 0.15 because the start is polished and only `dlu` is new.

```
cd ~/ige && git pull
PE=hpc_runs/$(ls hpc_runs | grep ^P_E_j); PA=hpc_runs/$(ls hpc_runs | grep ^P_A_j)
sbatch --time=02:00:00 --mem=24G --job-name=IGE-E5 model/hpc_ige.sh full IGE_MODELS=E IGE_RUN=E5 IGE_START=$PE/estimates.json:E IGE_STEPS=age,rehire,xacc,ufric IGE_FIX=muG,du IGE_R=20 IGE_SIG0=0.15 IGE_MAXFEV=8000,8000,8000,8000,8000,8000,8000,8000
sbatch --time=02:00:00 --mem=24G --job-name=IGE-A5 model/hpc_ige.sh full IGE_MODELS=A IGE_RUN=A5 IGE_START=$PA/estimates.json:A IGE_STEPS=age,rehire,xacc,ufric IGE_FIX=muG,du IGE_R=20 IGE_SIG0=0.15 IGE_MAXFEV=8000,8000,8000,8000,8000,8000,8000,8000
```

Judged by `fix_seeds.py` (E5 against P_E, A5 against P_A: drop > 3.84 at every seed and |t| of dlu with the
sandwich s.e.), the zero_B / zero_W t-ratios, and whether dgx, dg1, db1 keep their signs and p-values with dlu in
(the one thing that could change the verdict: a race difference in the search friction out of work that absorbs
part of H4 through the selection of who has a wage at 45-49). If dlu passes it becomes the fifth race hypothesis,
reported in the text as a step, not as a sixteen-model lattice; if it fails, the sentence in "What the model
leaves open" becomes "tested and rejected (drop [x], p = [y])", a null in the text.

### 6d. What the PI gets at 12:10

- Section 8 with the referee fixes compiled and pushed; the hypothesis-table note honest about H and G.
- Three new tables (untargeted validation, the H4 counterfactual by age and tercile, the sensitivity matrix) with
  their paragraphs, each generated from json by `tables.py`, each logged in EVIDENCE 11.9-11.11.
- The `ufric` step and `fix_seeds.py` tested locally and committed.
- The commands above; stage 1 first, nothing else until the ten polish jobs have pushed.

---

# Second read (after execution), Fable, 2026-10-19 10:05

Read at 28ee562: `sec7_model.tex`, the eight model tables, the abstract, `sec1` 55-80, `sec8`, `sec4` (Ranks),
`final_x4/` (profile_q, sensitivity, validation_E), `validation_psid.json`, `postestimation_Lx4_E_h4` (through the
table), EVIDENCE 11. Every number quoted in the text matches its table or json except where an item below says so.
Ordered by what a referee hits first; the first two are substantive, the rest are consistency and wording.

1. **The paper now contradicts itself on ranks.** Abstract: "while sons' rank-rank slopes do not diverge";
   Section 4 (Ranks): "For sons the rank evidence does not change with age"; prediction paragraph: "while
   rank-rank slopes should change little". The new Table modeluntargeted shows PSID hourly-wage rank slopes of
   White sons 0.251 -> 0.379 and Black 0.199 -> 0.192 between 25-29 and 45-49 (a gap of 0.19 at 45-49, s.e.
   about 0.06 if the two are independent), and Table rankage column (4) already had own-earnings rank slopes
   0.253 -> 0.352 (W) against 0.261 -> 0.202 (B), gap 0.150* at 40-44. The non-diverging ranks are family-income
   ranks (column (1)). The model reproduces the wage-rank divergence, which is a validation success, but the
   framing "logs diverge, ranks do not" has to become "family-income ranks do not; wage and earnings ranks do".
   This is the PI's call because it touches the abstract. Replacements:
   - Abstract: "while sons' rank-rank slopes do not diverge" -> "while rank-rank slopes of family income do not
     diverge".
   - Section 4, Ranks paragraph: "For sons the rank evidence does not change with age" -> "For sons' family
     income the rank evidence does not change with age"; and add after "(Appendix Table rankage)": "In sons' own
     earnings the rank slopes do diverge after 40 (0.150$^{*}$ at 40-44, column (4)), and in hourly wages on the
     model's sample by 0.19 at 45-49 (Table modeluntargeted): ranks normalise away the dispersion of family
     income, not the racial divergence of sons' wages."
   - Section 8, validation item 2, replace the last sentence: "On this sample and in hourly wages the PSID's rank
     slopes diverge by race by 0.19 at 45-49, as own-earnings ranks do at 40-44 (Table rankage, 0.150$^{*}$); the
     non-diverging ranks of Section 4 are family-income ranks."
   - Prediction paragraph: "while rank-rank slopes should change little" -> "while family-income rank-rank slopes
     should change less".
   - Add the two W $-$ B rows (rank slope gap at 25-29 and 45-49) with bootstrap s.e. to the validation table
     (`core.validation` differences on the same 300 draws; two minutes), so the 0.19 carries a standard error.

2. **"H4 carries the opening" is a level share, and Table modelcfh4 lets a referee compute the opening share.**
   H4 off closes 0.171 of the 0.282 gap at 45-49 (61%) but also 0.090 of the 0.083 gap at 25-29, so of the
   model's opening between 25-29 and 45-49 (0.282 - 0.083 = 0.199) the racial difference in the pay-off carries
   0.171 - 0.090 = 0.081, two fifths; the other three fifths of the opening is H2 and the race-neutral channels,
   which raise the White IGE by 0.145 and the Black IGE by 0.039 between those bands (Table modelcfh4, baseline
   columns net of the no-pay-off column). Say it before the referee does. Insert in "Which sons, which ages"
   after the first sentence: "The gap it carries is a level as much as an opening: at 25-29 the model's gap is
   0.083 and H4 off closes 0.090 of it, so of the opening between 25-29 and 45-49 (0.199) the racial difference in
   the pay-off of parental income carries 0.081, two fifths, and the pay-off of schooling with the race-neutral
   channels---schooling, access to $G$ jobs, job loss---carries the rest, because they raise the White IGE by 0.145
   and the Black IGE by 0.039 over the same ages." Change the paragraph heading in the verdict from "H4 carries the
   opening" to "H4 carries the gap". Abstract and introduction ("three fifths of the gap at 45-49") are level
   statements and stay correct; the PI may want "three fifths of the gap at 45-49 and two fifths of its opening".

3. **Verdict, H4 paragraph, last sentence is misreadable.** "removes 0.168*** (s.e. 0.058, p = 0.004) of the
   White IGE at 45-49, 39% of its rise from 25-29" reads as 0.168 = 39% of the rise (it is 70% of the rise and
   36% of the level; the 39% is 0.094 of 0.239). Replace: "Switched off for both races, the pay-off of parental
   income in accumulation lowers the White IGE by 0.074$^{***}$ (s.e. 0.026) at 25-29 and by 0.168$^{***}$ (0.058,
   $p = 0.004$) at 45-49: 36% of its level at 45-49 and, net of what is already there at 25-29, 0.094 of its rise
   of 0.239 in the model, 39% (Table modelcfh4)."

4. **Identification paragraph, one sign wrong and one range short** (against `sensitivity.json`): "H3 moves with
   the Black and White returns at 25-29" -> "H3 moves with the Black return at 25-29 ($+0.60$) and against the
   White return at 25-29 ($-0.41$), that is with the racial difference in the entry return"; "a higher White IGE
   at 40-55 raises it" -> "a higher White IGE at 35-55 raises it" (35-39 W $+0.23$ is among the top six).

5. **House rule, "little" for precise shares (three places).** Estimation paragraph: "The twelve IGE moments
   carry little weight in $Q$ (4.9 of 127.6 at the selected model)" -> "The twelve IGE moments contribute 4.9 of
   the 127.6 of $Q$ at the selected model, 4 percent of the criterion for 18 percent of the moments,". Validation
   item 3: "changes little when a dummy for a $G$ job is added, in the model as in the PSID (White at 35-55: 0.429
   to 0.409 in the model, 0.421 to 0.387 in the PSID)" -> "falls by 0.034 (8%) in the PSID and 0.020 (5%) in the
   model when a dummy for a $G$ job is added (White at 35-55: 0.421 to 0.387 and 0.429 to 0.409), and by
   0.011-0.017 for Black sons in both". Prediction paragraph: covered by item 1. ("changes little with age" about
   the literature's models in "Why a job side" is not a precise share; leave it.)

6. **Validation item 1 names no source for the level failure.** The one career moment the model overshoots in
   the right direction is the wage gain at a move (Black $+0.060$ against $-0.006$, White $0.072$ against $0.052$,
   $t = 3.5$ and $2.0$); with 13 percent of pairs moving, that is 0.01-0.02 a decade of the 0.11-0.15. Replace the
   last sentence of item 1: "The levels fail: the model's wages at 35-49 are 0.11-0.15 log points above the PSID
   for both races ($t$ between 3.9 and 6.5), so the model's wage growth from 25-29 to 35-39 is too fast by 0.11
   for both; the wage gain at a move, which the model overstates for both races (Table modelfit, $t = 3.5$ and
   $2.0$), is the one targeted moment pointing the same way, and it accounts for at most 0.02 of it." Then list
   the level misfit in "What the model leaves open" (item 11).

7. **Validation item 5 hedges with "either ... or"; the data say which.** In the PSID the $G$ share rises from
   25-34 to 35-55 (White top tercile 0.180 to 0.227, bottom 0.066 to 0.088; Black 0.117 to 0.122, 0.031 to 0.044),
   in the model it falls (0.181 to 0.134, 0.047 to 0.031; 0.099 to 0.073, 0.032 to 0.021). Replace the last
   sentence: "In the PSID the share in $G$ jobs rises between 25-34 and 35-55 (White top tercile 0.180 to 0.227);
   in the model it falls (0.181 to 0.134), because access does not depend on age and $G$ jobs are lost at the same
   displacement rate as $O$ jobs. An access probability that rises with age, or a lower job-loss rate in $G$ jobs,
   is the model step this statistic asks for, after the search friction out of work."

8. **Wrong table in the $\gamma_x$ footnote.** "0.008 ($p = 0.17$) in the PSID and 0.002 ($p = 0.73$) in the
   NLSY79 (Table withincell)" -> "(Table growthladder, columns (4) and (9))"; Table withincell holds the return to
   schooling, not the same-employer gradient.

9. **Table modelcfh4, panel B: "$0.001^{***}$ (0.000)" and "$-0.009^{***}$ (0.003)" for the middle tercile.**
   Stars on a change that rounds to zero with a standard error that rounds to zero read as an artefact. In
   `tables.py` print panel B with four decimals for the change and the s.e. (0.0011$^{***}$ (0.0003)), or drop the
   two middle-tercile rows and say in the note that the middle tercile sits at the centring point. Four decimals
   is the smaller change.

10. **"The $Q$ rule and the Wald test agree in every model that contains H2 and H3"** is one model. Replace: "In
    the one model that contains both schooling parameters (D) the $Q$ rule and the Wald test agree (1.4,
    $p = 0.44$); given H2 alone (C) $\alpha_3 = -0.24$ ($p = 0.11$)." And the sentence before repeats "with a
    drop of 3.2" from the paragraph's first sentence; delete the repeat.

11. **"What the model leaves open" does not list the three validation failures** and still calls the search
    friction out of work "the natural next test" although step 5 is coded. Add after the entry-scar sentence:
    "Of the untargeted statistics, the model misses the level of wages after 35 (0.11-0.15 too high, both races),
    the share in good jobs after 35 (too low by 0.05-0.09) and the White IGE below the median of parental income
    at 25-29 (0.26 against 0.11)." Replace the last sentence: "Non-employment by race and the gain at a move are
    where a racial difference in the search friction out of work \citep{bowlus2002discrimination} would act; it is
    coded as the next step and estimated next. The share in good jobs after 35 asks for access that rises with
    age, the step after."

12. **Lattice-table note.** Rows B and H are identical (135.0, 134.7 (2.1), 0.169, 0.271, 6.8) and the note does not
    say why; add to the `tables.py` note: "Model H's solution is model B's (see the note to Table modelhyp)."

13. **Counterfactual closing paragraph, wording.** "because the model opens the gap earlier than the data and
    closes less of the distance to it by 45-49" -> "because the model's gap at 30-34 is above the PSID's (0.169
    against 0.153) and its gap at 45-49 below (0.282 against 0.330)".

14. **Table modelid, $\alpha_3$ row: "share in $G$ by race at equal tercile; gain at a move".** The sensitivity
    table gives 96% to the $G$ shares and 3% to moves; delete "; gain at a move" and the move-gain values in the
    last column of that row (keep them in the $\sigma_m$ row).

15. **Duplicate sentences.** The Fit paragraph's "the twelve IGE moments contribute 4.9 to $Q$" repeats the
    Estimation paragraph; keep it in Estimation only. The Fit paragraph's same-employer sentence with its footnote
    repeats validation item 6; keep the footnote (it carries the sample reconciliation) and shorten item 6 to "The
    same-employer growth gradient in parental income passes (Fit, above)". Optional.

16. **Hypothesis-table note, add the third profile.** "at E, $Q$ falls by 0.3 at $\alpha_3 = -0.1$, consistent
    with the 0.5 that D finds" closes the question for E -> D too.

17. **EVIDENCE 11.** 11.6 policy column: "a policy scored at 30 sees 60% of the gap at 45" -> "(model; PSID 46%)".
    11.1: add "carries 0.081 of the model's 0.199 opening between 25-29 and 45-49 (two fifths), 0.171 of the 0.282
    level at 45-49 (three fifths)". 11.9: add the W $-$ B wage-rank gap with its s.e. once computed (item 1) and the
    sentence that the framing changes to family-income ranks.

18. **Checked and correct, no change**: the opening footnote (wages, model sample); the H4 bullet (Table
    jobmoves); the H2/H3 numbers (9.9, 8.5, 8.5, 7.5; 0.037***, $-0.0085$***); the H1 drops and p-values; the
    estimates sentence (0.172, 0.092, $-0.154$, $-0.177$, $-0.413$, 0.61 -> 0.22); the Fit numbers; validation
    items 2 and 4 against `validation_E.json`; the counterfactual shares (73%, 61%, 7%, 8%, 2%); "Which sons"
    numbers (0.090, 0.178, 0.090, $-0.145$, 36%, 39%); the sensitivity shares (77, 77, 63, 73, 96, 87); the
    profile base values; terminology ("search friction", "accumulation"; no "rung", "ladder", "promotion",
    "slightly", "small" in Section 8).
