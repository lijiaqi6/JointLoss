# Paper B model: what else to run on the HPC (Fable, 2026-10-18)

Read: `model/core.py`, `estimate.py`, `build_data.py`, `postestimation.py`, `hpc_ige.sh`, the run
`model/hpc_runs/ige_full_20261018_125238/` (smm_report, postestimation, estimates.json incl. the Jacobian column
norms), `paperB_age_profile/sec7_model.tex`, `model_document.tex` (estimation and validation sections), the two
Fable reviews and `proposals/paperB_model_plan.md`. Nothing was run. Jobs 11858549-52 (E, F, G, H) are assumed to
finish as planned.

**Short answer.** Yes, three things, in this order. (1) Now, in parallel with E-H: two cheap re-starts that measure
the optimiser's own resolution, because every number in the hypothesis table is a Q difference of 2-24 and nobody
yet knows whether a re-start of the same model moves Q by 1 or by 10. (2) As soon as E-H land: one short evaluation
job (no estimation) that puts the whole lattice on common draws at ten seeds and at R = 20, with Q split by moment
block. (3) The next model step, coded tomorrow and run as four jobs: age slopes in job loss and on-the-job search,
and re-employment in the year of displacement. These two changes address the five worst misfits of the current
model (t = -7.5, -5.8, +5.5, +4.6, +3.5), all in the displacement / move / zero-hours block, and that block is
tied to race (delta_0r) and parental income (delta_1), so the race tests must be redone on top of it anyway. Then the
lattice once more at the new baseline, at R = 20, and the table is written. Everything else is a robustness row for
later.

## 1. Runs, ranked

### R1-R2 (submit now, ~25 min each, 32 cores): the optimiser yardstick

| Job name | What | Change | Start | Evaluations |
|---|---|---|---|---|
| `IGE-D-cold` | D estimated from the closed-form start, not through A -> B -> C | none (`IGE_MODELS=D`, no `IGE_START`) | `theta_start.json` | 15,000 |
| `IGE-A-fromD` | A warm-started from D's estimates with a3, dg1, db1 set to 0 | none (`IGE_MODELS=A`, `IGE_START=<run>/estimates.json:D`) | D of job 11855696 | 8,000 |

Why they cannot wait: A (Q 324.3) was reached cold with 15,000 evaluations and sigma_0 = 1; B, C, D and now E-H are
warm starts with sigma_0 = 0.5 and 8,000 evaluations. The table therefore confounds "one more race parameter" with
"a different optimiser path". If Q_D(cold) differs from 300.3 by more than about 3, or Q_A(from D) from 324.3 by
more than about 3, the 3.84 rule is below the optimiser's resolution and every model in the lattice needs either
20,000 evaluations or two starts (take the better). If both differences are below 1-2, the lattice stands as run.
Judged by: |Q(cold) - Q(warm)| for the same model on the same draws, and the shift of the race parameters between
the two solutions relative to their s.e.

Submission (from `~/ige` after `git pull`; the env variables pass through sbatch; `IGE_MAXFEV` maps positionally to
A,B,C,D, so the fourth entry is D's):

```
cd ~/ige && git pull
IGE_MODELS=D IGE_MAXFEV=15000,15000,15000,15000 sbatch --job-name=IGE-D-cold --time=02:00:00 model/hpc_ige.sh full
IGE_MODELS=A IGE_MAXFEV=8000,8000,8000,8000 \
  IGE_START=$HOME/ige/IGE/model/hpc_runs/ige_full_20261018_125238/estimates.json:D \
  sbatch --job-name=IGE-A-fromD --time=02:00:00 model/hpc_ige.sh full
squeue -u $USER -o "%.10i %.25j %.8T %.10M %R"
```

### R3 (after E-H land; one job, ~20 min): the lattice on common draws

A 60-line script (`model/lattice_q.py`, reads every `hpc_runs/*/estimates.json` named on the command line):
for each of the 8 models plus the R1-R2 solutions, Q at seeds 7-16 for R = 5 and for R = 20 (R changes `idx` and
`Draws`; one evaluation each), and Q by moment block (IGE 12, returns 12, levels / variances 8, G shares 9, stayer
growth 10, moves / displacement 13, zero hours 2). Output: for each hypothesis the drop alone (A - B, A - F, A - G)
and given the others (E - D, H - D, C - D) as mean and s.d. over the ten seeds, at both R. Also the nesting
inequalities, which are a free optimiser check: Q_A >= Q_B, Q_F, Q_G >= Q_C, Q_H, Q_E >= Q_D (F is nested in C and E,
G in H and E, B in C and H). Any violation larger than the seed s.d. is an optimiser failure and that model is
re-run from the better neighbour's estimates.

Why: the three-seed drops already show the problem (dg1 6.2 to 17.9; a3 1.7 to 4.6 around the 3.84 line). At R = 5
the seed s.d. of a Q difference is of the order of the differences being tested. R = 20 halves it. The table should
report "drop 10.5 (s.d. 2.1 over ten seeds)" and the verdict "exceeds 3.84 at every seed", not a single number.
Decision rule for the paper: a race parameter is kept if its drop given the others exceeds 3.84 at R = 20 at every
one of the ten seeds and exceeds twice the seed s.d.; otherwise it is dropped and the counterfactual is reported as
the range between the two neighbouring models.

### R4-R5 (code first, one day; then four jobs in parallel, ~40 min each): the next model step

The worst misfits of model D are one block: displacement per interview pair falls with age in the PSID (Black
0.173 -> 0.111, White 0.102 -> 0.076) and rises or stays flat in the model (0.123 -> 0.140, 0.067 -> 0.073; t = -5.8,
+4.6, -7.5); moves fall with age in the data (0.127 -> 0.090) and not in the model (t = -2.1 to +3.5); zero-hours
years are too many for White sons (0.054 vs 0.039, t = +5.5) and too few for Black (t = -2.1); lambda_u sits at its
0.99 cap with s.e. 10.8. Two causes, both visible in `core.simulate`:

(a) `delta` and `lambda_e` have no age term. Age is already a state of the solution, so an age slope costs no state
variable (a tenure slope would: tenure is not a state and would break the match-grid-only solution).

(b) A displaced son cannot be re-employed before the next income year: `ou` requires `~emp` evaluated before the
update, so every displacement produces one full zero-hours year and `zero_W` is forced to be at least the annual
displacement rate. The data have zero_W 0.039 against a per-pair displacement rate of 0.102 over one to three
income years. The optimiser compromises: delta_W too low for dsp_2534_W, zero_W too high, and lambda_u pushed to
the cap to shorten the forced spell. The uniform `D.uo[:, k]` of a displaced son is unused in that year, so
re-employment in the displacement year can use it: common random numbers are preserved and Q stays comparable.

Step 2 (R4), two parameters, no new moments, no new draws:
delta = Lambda(delta_0r + delta_1 (x - xbar) + delta_a (a - 30)/10 + phi_delta (u_t - ubar)) and
lambda_e(a) = Lambda(llam_e + lambda_a (a - 30)/10). Starting values from the first step (add age to the displacement
logit in `build_data.first_steps`; lambda_a = 0). In `solve`, `db` and `lam_e` become age-indexed inside the loop.
Jobs: `IGE-A2` (A + step 2, warm from A), `IGE-D2` (D + step 2, warm from D), 8,000 evaluations each.

Step 3 (R5), no parameter: in `solve`, the displaced continuation becomes
`db * (lam_u * emu + (1 - lam_u) * u1) + (1 - db) * (...)` (compute `emu` before the j loop); in `simulate`, displaced
sons draw an offer with `D.uo[:, k] < lu` and the same `jo, mo` as everyone else, accept if `vnew > vU[idx, k+1]`.
Run together with step 2: `IGE-A23`, `IGE-D23`. The increment of step 3 is Q(A23) - Q(A2); of step 2, Q(A2) - Q(A).

Judged by: Q on the 66 moments at the common draws (and at the ten seeds of R3), by block; the dsp / mov / zero
t-ratios should fall below 2 in absolute value; delta_a and lambda_a each kept only if their own drop exceeds the
R3 noise band (parsimony). After step 3 lambda_u either leaves its cap (now identified by zero_B, zero_W together
with the displacement rates) or stays at it; if it stays, fix lambda_u = 1 and remove the parameter. If after step 3
zero_B is still too low while zero_W fits, the data are asking for a race difference in job finding out of work
(Black non-employment is 2.8 times the White rate while displacement is 1.7 times): that is a fourth race
hypothesis (a race-specific search friction out of work, Bowlus-Eckstein), to be tested on top of the selected
model only, not as a 16-model lattice.

Why it cannot wait for the write-up: delta carries race (delta_0r) and parental income (delta_1 < 0). A displacement
hazard that rises with age in the model makes sons of poorer parents lose matches increasingly with age, which
is a rising IGE for both races built into the misfit; the Black IGE rises in the model (0.18 -> 0.23) and is flat
in the data. The race tests H1-H3 are run against that background. The hypothesis table must therefore be produced
at the step-2/3 baseline, not only at the current one; and the one-step rule wants both baselines on the same 66
moments, which R4-R5 give.

### R6 (after R4-R5 settle; eight jobs, ~1-1.5 h each at R = 20): the final lattice

All eight models at the new baseline with `R = 20` in `estimate.py` (evaluation time roughly 3-4x; set
`--time=04:00:00`), each warm-started from its own step-2/3 neighbour, 10,000 evaluations, two starts for the two
end-points A and D (take the better). Then R3's script on the result, and `postestimation.py` on the selected
model. This is the run the paper's Section 8 is written from.

## 2. Robustness a referee will ask for

| Item | Needs HPC | When | Verdict |
|---|---|---|---|
| Sandwich standard errors. `V = (1 + 1/R)(G'WG)^{-1}` is correct only if W is the inverse of the moment covariance; W is diagonal and the IGE and return moments of adjacent bands share sons, so the correct form is `(G'WG)^{-1} G'W Omega W G (G'WG)^{-1}` with Omega the 66 x 66 bootstrap covariance (no inversion of Omega needed). `build_data.bootstrap` already produces the 500 x 66 draws; save them (`output/boot_moments.npy`, 264 KB, commit it) and change two lines in `estimate.py` and `postestimation.py`. The stars on dg1 (t = 2.9) and db1 (t = 2.2) and the delta-method p-values of the counterfactuals depend on it. | No (local data step; the Jacobian is already computed in every job) | Before the table is written; include in the R6 code | Do it |
| More simulated sons (R = 20) | Yes | R6 | Do it; it is the main defence of the Q-drop test |
| Multi-start | Yes | R1-R2 now; two starts for A and D in R6 | Do it |
| Block-balanced weights (each of the six blocks gets equal total weight, so the 12 IGE moments, whose s.e. are 3-10 times those of the career moments, are not 1/66 of the criterion each). A and D only. | Yes, 2 jobs | After R6; a robustness row | Do it later; the referee's first question will be "the fact you explain has almost no weight in Q" |
| IPW moments (attrition weights in `core.moments`: weighted means, weighted OLS). A and D only. | Yes, 2 jobs, plus the weighted moment function | After R6 | Later; IPW moved the opening by -0.014 (n.s.), so this is a row, not a decision input |
| A second estimation seed for the draws (D at seed 8) | Yes, 1 job | Only if R = 20 leaves the seed s.d. of the dg1 / db1 drops above 2 | Probably not needed |
| Full-covariance (optimal) weighting | Yes | No | Skip: a 66 x 66 inverse from 500 draws is noisy and the diagonal choice is standard; say so in a footnote |
| Andrews-Gentzkow-Shapiro sensitivity of the counterfactuals (Lambda = -(G'WG)^{-1} G'W) | No | Write-up | From the existing Jacobian; one table |
| Untargeted validation: rank-rank slopes, earnings IGE, NLSY79 profiles, entry-wage scar | No (simulation on the estimate) | Write-up | Already promised in the model document |

## 3. What could make the E-H results or the hypothesis table misleading

1. **Optimiser path.** A is a cold 15,000-evaluation solution, the rest are warm 8,000-evaluation solutions. The
   table compares optimiser paths as much as models. R1-R2 measure this; the nesting inequalities in R3 catch the
   worst cases. Also check in each E-H `smm_progress.log` whether CMA-ES stopped on `maxfevals` or `tolfun`; a
   `maxfevals` stop with Q still falling is a sign the model needs more evaluations.

2. **The 3.84 rule.** With diagonal weights the Q difference is not chi-square(1), and at R = 5 its seed s.d. is of
   the order of 3-5. Report every drop as mean (s.d.) over ten seeds at R = 20 (R3) and add the Wald t of the
   parameter with the sandwich s.e. The two tests together are the verdict; a parameter that passes one and fails
   the other is "not separable in these data" and is dropped under the parsimony rule.

3. **db1 and dg1 are nearly collinear** (Jacobian column correlation 0.92 at the start), and in D they move apart
   with opposite signs (dg1 -0.0114 against -0.0039 in C; db1 +0.033). They are separated only by the level versus
   the slope of the six return-to-schooling bands by race. F (dg1 alone) and G (db1 alone) will show this: expect
   F's dg1 near -0.004 and G's db1 positive with a smaller drop than in D. The paper should say that H2 and H3 are
   identified jointly from the age profile of the return to schooling and report their joint drop (A - E) next to
   the separate ones.

4. **lambda_u at the cap.** Its Jacobian column norm is 4.9 against 20-2,300 for the others, so (G'WG) is nearly
   singular in that direction; the reported s.e. of other parameters are affected only through their correlation
   with it, but the s.e. of lambda_u itself (10.8) is meaningless. Note also that `solve` uses the uncapped
   logistic(6.3) = 0.998 while `simulate` caps at 0.99 (harmless, but the two should be the same number). Step 3
   gives lambda_u a moment; if it still goes to the cap, fix it at 1 and remove it.

5. **mu_G is not identified** (0.10 in A, -0.16 in D, s.e. 0.16-0.19; correlations with a2 and a0 0.92 and 0.89
   through gG). With mu_G < 0 a G offer lowers the immediate gain at a move, so a3 < 0 (fewer G offers for Black
   sons) raises Black move gains in the model, the opposite of the data (gmv_2534_B -0.006 vs model +0.070,
   t = +4.0). The verdict on H1 is therefore conditional on mu_G, and the move-gain moment, listed as the stronger
   identifying moment for a3, cannot be fit by a3 in this model. Add one job to the R4-R5 batch: `IGE-D23-muG0` (D
   with mu_G fixed at 0, G jobs differ only in accumulation); if Q rises by less than the noise band, drop mu_G.

6. **The displacement / move / zero-hours misfit contaminates the race tests** (Section 1, R4-R5): delta_0r and
   delta_1 are race and background parameters, and the age profile of job loss is an age profile of the IGE in the
   model. The hypothesis table is reported at the step-2/3 baseline; the current one goes to the appendix as the
   step-1 row.

7. **Q is not the fact.** Model D reproduces half the opening (gap 0.158 vs 0.330 at 45-49) while the 12 IGE
   moments contribute little to Q because their s.e. are large. Each row of the lattice should carry, next to Q,
   the model's gap at 30-34 and 45-49 and the Q of the IGE block alone (R3 gives it). A parameter that lowers total
   Q through the career block while leaving the gap unchanged is not evidence for the hypothesis it names.

8. **Late-career Black variance.** vlw_4549_B is too high (t = +4.0) because the data's Black variance falls from
   35-39 to 45-49 (0.382 -> 0.345), which is selection into who is observed as a head with a wage at 45-49; the
   model has no exit from the sample. No run fixes this; say it, and let the IPW row (Section 2) show how much of
   it is attrition.

9. **Common random numbers.** All eight models, R1-R2 and R4-R5 use seed 7 and R = 5, so their Q are comparable;
   step 3 reuses an unused draw, so the comparison with the current baseline holds. R6 at R = 20 is a new draw set:
   compare models within R6 only, never R6 against the R = 5 runs.

## Order of work

Today: submit R1-R2. Tomorrow: code step 2, step 3 and `lattice_q.py` (one commit each), run R3 on E-H plus R1-R2,
submit R4-R5 (five jobs with the mu_G check). Day 3: read the block Q, fix the baseline, add the sandwich s.e. and
R = 20, submit R6. Day 4-5: Section 8 from R6 (puzzle, hypotheses, test with the lattice table, verdict, what
remains: the Black move gain, the late-career Black variance, half the opening unexplained).

---

# Second round (Fable, 2026-10-18, evening): first lattice, step 2, and the next runs

Read: code 20e3f5a (`core.py` steps as switches, `estimate.vcov`, `lattice_q.py`, `hpc_ige.sh` with arguments),
`output/start_step23.json`, and the results reported for jobs 1185935x. Nothing run. Answers to the four questions,
then the runs.

## Q1. The final lattice: wait for A23 / D23, prepare it now

**What the yardstick says.** A warm-started from D beats the cold A by 5.4 on the same draws, and every run stopped on
`maxfevals`, none on `tolfun`. So 8,000 evaluations at sigma_0 = 0.5 leave about 5 units of optimiser error, above the
3.84 line. The error is not symmetric noise: a warm start from a more general model is a better start (D's 22
common parameters had been polished over four chained runs), and a nested model started from its more general
neighbour can never fit worse at the estimation draws than that neighbour's solution restricted (the start is a
candidate). Use this: the final lattice is run as a chain in which every model starts from the best solution of a
neighbour, and nesting then holds by construction at the estimation draws.

**Design (R6, revised).**
- Baseline: age + rehire if Q(A23) < Q(A2) by more than 5 and |t| of zero_W falls below 2.5; age only otherwise
  (decide from A23 / D23 when they land). Plus the step-4 parameter of Q3 if it passes its own test first (see
  below); the lattice is run once, at the final baseline, not twice.
- R = 20, seed 7 (a new draw set: compare only within R6); popsize 30; sigma_0 = 0.5 for every warm start; 12,000
  evaluations, then a polish of 4,000 at sigma_0 = 0.15 from the best point (a second `run_cma` call in the same job;
  five lines). Memory: `lattice_q` reports about 1 GB per worker at R = 20, so `--mem=48G`; `--time=03:00:00`
  (evaluation 3-4x slower than at R = 5, about 1.5 h per job).
- Chain with `--dependency=afterok`: stage 1, A from two starts (A23's own solution; D23 restricted), take the
  better; stage 2, B, F, G from A; stage 3, C from the better of B and F, H from the better of B and G, E from the
  better of F and G; stage 4, D from the best of C, H, E and from D23's own solution. Eight to ten jobs, four stages,
  about 5-6 h wall. Names `IGE-L-A`, `IGE-L-B`, ..., `IGE-L-D` (L = lattice).
- Then `lattice_q.py` on the R6 folders (seeds 7-16, R = 5 and 20), `postestimation.py` on the selected model. The
  two A starts and the two D starts give the optimiser spread for the table note.
- Table columns per model: Q at the estimation draws, mean (s.d.) over ten seeds at R = 20, Q of the IGE block,
  model gap at 30-34 and 45-49, the race parameters with sandwich s.e.; then the three (or four) hypotheses with the
  drop alone and given the others, the seed s.d., "passes at every seed" and the Wald p.

Prepare now (code only): the chain submission script, the polish phase, the untargeted statistics of Q3 in
`lattice_q.py`. Submit when A23 / D23 are back and the Q3 test has run.

## Q2. Is the verdict safe to write around?

The qualitative verdict (H1 out; H2 and H3 jointly, not separately) is robust enough to build Section 8's
structure on, for three reasons: the joint drop A -> E of 17.0 is three times the optimiser error; the sandwich
p-values in E are 0.003 (dg1) and 0.014 (db1) and the two parameters have the signs of the reduced form (Black
return higher at entry, rising less: earnings 0.124 flat against 0.045 -> 0.143); and the a3 drops are at or below
the optimiser error everywhere, with a3 n.s. in D (p = 0.45) and the only "significant" a3 (H, p = 0.053) sitting
next to a db1 of the wrong sign, which is the pair compensating for the missing dg1. Note for the text: in G (db1
alone) db1 is negative, i.e. without a race difference in the pay-off of schooling the model lowers the Black
return at every age to meet the late bands and misses the early ones; with dg1 the level turns positive. That is why
H2 and H3 are one finding: for Black sons schooling is a wage level at entry, for White sons a growth rate.

What would change my view, in order of likelihood:
1. The step-4 parameter of Q3 absorbs dg1 (E + step 4 has dg1 n.s. and the H2 drop given step 4 below the seed
   band). Then the race difference is in the pay-off of background, not of schooling, and the story changes. The
   within-cell evidence (the rise of the return to schooling survives cell fixed effects, 0.061***) says it will not
   happen, but this is the one test that must run before Section 8 is written.
2. At the final baseline the joint drop A -> E falls below about 8 or fails at some seeds at R = 20.
3. The H1 drop given both exceeds 3.84 at every seed at R = 20 and a3 has p < 0.05 with the sandwich. Then H1 is in.
   On the current numbers (1.3-1.6) this needs a drop seven times larger than observed; unlikely.
Write the section's skeleton now (puzzle, the four hypotheses incl. Q3's, the lattice table, verdict, what
remains), with numbers as placeholders from R6.

## Q3. The missing half of the opening: background pays off in accumulation for White sons

**The misfit is symmetric.** At 45-49 the White IGE is too flat by 0.09 (0.379 vs 0.470) and the Black IGE too
steep by 0.095 (0.235 vs 0.140). Both races' IGE rise in the model through the race-neutral channels (access by
parental income a1 into G jobs, delta_1, schooling through g1); race enters the rise only through dg1 and the G share.
The data want the rise to be almost entirely White. Step 2 cannot touch this (it changes job loss by age, not who
grows), and it did not: gap 0.018 / 0.064 / 0.144 against 0.012 / 0.057 / 0.134.

**Where the model is straining.** The White return to schooling by age fits (rets_W, |t| <= 1.3) while the White
IGE does not (t -2 to -2.5 at 30-49): the schooling channel is right and the non-schooling channel is missing. The
model's only non-schooling channel is G access, and it is already pushed past the data: G stayers' growth at 25-34 is
0.093 in the model against 0.075 (t = +2.6), while the data's G - O growth gap is modest (0.020 early, 0.014 late).
There is no room left in the job side.

**What the data say the channel is.** Section 6 and EVIDENCE 9.2, 9.5, 9.25: career growth rises with parental
income for White sons (0.123***) and not Black (0.006); the same-employer growth gradient at 25-34 is White 0.020***,
Black -0.001 (difference -0.021***); within the early cell and net of schooling it is 0.008 (p = 0.17) in the PSID,
0.002 in the NLSY79. Section 7 reads the 0.008 as zero and lets accumulation load on schooling only. That is an
underpowered test of a parameter the IGE profile identifies much better: 0.008 per year of growth for twenty years is
0.16 of IGE, which is the missing half (the White rise is 0.27, schooling accounts for 0.44 of it = 0.12, leaving
0.15). The annual-growth regression has a standard error of about 0.006 per year; the cumulative moments have far
less. The reduced form never rejected this channel; it was too noisy to see it.

**Step 4 (the one decisive step), two parameters, no new moments, no new draws:**
Delta_j(a) = [gamma_j + gamma_1(r)(e - 12) + gamma_x(r)(x - xbar)] e^{-rho(a - 18)}, gamma_x(r) = gamma_x +
dgamma_x 1[r = B]. gamma_x is race-neutral (worker side) and goes into the baseline; dgamma_x is the fourth race
hypothesis, H4: background pays off in accumulation for White sons and not for Black sons. Identification: gamma_x
by the White IGE by age given the White return to schooling by age and the G shares (the three blocks that separate
x from e and from access); dgamma_x by the flat Black IGE given dg1 (six Black IGE bands with t about 2 each, about
15-20 units of Q available). Starting values: gamma_x = 0.008 (Table 9's within-cell, net-of-schooling coefficient),
dgamma_x = -0.008; `SCALE` 0.005 each. Untargeted validation, to add to `lattice_q.py` as a statistic (not a
moment, so the moment set and the baseline stand): the same-employer growth slope on x by race at 25-34, raw and net
of schooling, against the PSID 0.020 / -0.001 and 0.008 / about 0. If the estimated gamma_x(r) reproduces the raw
numbers, the channel is validated by a statistic it was not fit to.

Why this and not the alternatives: a race-specific gamma_G flattens the Black IGE but cannot raise the White one
(the pooled G moment is already overshot); finer job types are ruled out by the paper's own accounting (0.79 of the
divergence is within occupation x industry); late entry of professional-degree sons would help the 25-29 -> 30-34
jump (0.13 in the data, 0.07 in the model) but not the rise to 45-49; attrition moves the opening by 0.014. Step 4
also answers the referee's competing model: a background term in accumulation is the Huggett-type learning-ability
channel, nested and tested next to the job side rather than dismissed; the data can want both.

**Runs for step 4 (three jobs, R = 5 at the current draws, 8,000 evaluations, warm starts): `IGE-A4` (A23 +
gamma_x + dgamma_x), `IGE-E4` (E23 + both), `IGE-G4` (G23 + both: db1 without dg1, to see whether H2 survives
H4).** Judged by: the Q drop of each parameter at common draws against the optimiser error (5) and the seed band;
the IGE-block Q and the gap at 45-49 (the target is the data's 0.330; anything above 0.25 is the other half found);
the White and Black IGE t's; the untargeted same-employer gradient; and whether dg1 keeps its sign and p in E4. If
gamma_x passes and dgamma_x passes, both go into R6 (gamma_x in the baseline; dgamma_x tested in the lattice only on
A and on the selected model, two extra jobs, not a 16-model lattice). One caveat to state in the paper: the Black
IGE at 45-49 is measured on sons with a wage, and Black non-employment is 11 percent, so dgamma_x will absorb any
selection the model lacks; the IPW row of Section 2 is therefore the decisive robustness for H4 specifically and
moves up in priority once H4 is in.

## Q4. What was done: fine, with four notes

1. Rehire start (llam_u = 0 from a 1-D search, start only): correct under the rules; the start is a candidate and
   everything is re-estimated jointly. After the step-3 run, if lambda_u sits below 0.9, remove the 0.99 cap in both
   `solve` and `simulate` (it was a crutch for the forced spell; a bound that no longer binds should not stay in the
   code) and say in the model document that lambda_u is identified by the zero-hours shares given the displacement
   rates.
2. Rehire mechanics: `ou` with `~emp | disp`, `hire` against `vU[idx, k+1]`, and `lost = lam_u emu + (1 - lam_u) u1` in
   `solve` are mutually consistent; `DSP` still marks the year, so a same-year rehire is classed as a displaced pair
   as in the PSID. Measured displacement at D's old estimates rising to 0.197 / 0.110 (data 0.173 / 0.102) is
   expected and the re-estimation will bring delta_0r down; it also frees delta_0W to rise relative to zero_W, which is
   what A2's remaining dsp_3555_W misfit (t -3.8, worse than before) needs. Do not read that misfit as a call for a
   race-specific age slope; judge it after A23.
3. Warm starts with da = la = 0 from the first-run estimates: fine (A2 found -0.42 / -0.50 within budget). The B > A
   violation (2.45) is the old-A start: B was started from the cold A (324.3), not the warm A (318.9). The chain of Q1
   removes this by construction.
4. The 5.4 "optimiser error" is a lower bound on under-convergence of the cold run, not a noise s.d.: a cold 15,000
   run is worse than a warm 8,000 run from a polished point. Report it in the table note as "re-starts of the same
   model move Q by up to 5 at 8,000 evaluations; the final lattice uses chained starts, 16,000 evaluations and the
   nesting checks", and give the A and D two-start spreads from R6.

Minor: step 2's la = -0.50 per decade takes lambda_e from 0.42 at 25 to 0.17 at 50; da = -0.42 halves the hazard
between 25 and 45. Both are the usual magnitudes; no concern. The `EXTRA` mechanism means a run without `age` has
no da / la; `lattice_q` already refuses to mix specifications, good.

## Order of work

Now: code step 4 (`IGE_STEPS=xacc`: gamma_x in `PARAMS` when on, dgamma_x in `NESTED` as the H4 parameter for the
two extra lattice jobs), the untargeted gradient in `lattice_q.py`, the polish phase, the chain script. When A23 /
D23 return: fix the step-2/3 baseline, submit `IGE-A4`, `IGE-E4`, `IGE-G4` (about 1 h). Then R6 at the final baseline
(5-6 h), `lattice_q`, `postestimation`. Section 8 is written from R6; its skeleton can be written today.
