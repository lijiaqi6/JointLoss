# Paper B: execution of the Fable reviews (round 1 2026-10-17; round 2 2026-10-18)

Round 1 below (the round-1 review is in git history of `fable_review_paperB.md`); round 2 at the end. Numbers: EVIDENCE.md 1.32-1.40,
9.21-9.25, Q13b, Q17, Q18.

| Item | Status | Where |
|---|---|---|
| 1(a) Attrition + IPW | Done. Staying is selective for White sons (0.139*** per log point at 45-49), not Black; IPW moves the opening by -0.014 / -0.012 (n.s.) | `41` A; Sec. 2; App. Table attrition; Table 4 |
| 1(b) Year effects / APC | Done. Year FE, period-varying IGE, 1990-2010 window, within-cohort SDs; earnings robust everywhere, family income weaker with period-varying IGE / fixed window | `41` B; Sec. 3.3; Table 4 |
| 1(c) Haider-Solon lambda by race | Done. White lambda rises 0.69 -> 1.22, Black 0.85 -> 1.0; diff 0.211**; kappa ~0 | `41` C; App. Table lambda |
| 1(d) Nonparametric figure, bottom tercile | Done. Earnings divergence racial (bottom tercile 0.232*, re-weighted 0.188*); family-income divergence mostly position (below median 0.023) | `41` D; Figure 2 (`44`) |
| 1(e) Within-race ranks, PPML | Done. Within-race rank opening 0.015 (sons); PPML 0.257*** / 0.145*** | `41` E; Table 4 |
| 1(f) Earnings as headline | Done (abstract, intro, Sec. 3) | paper |
| 1(g) Rewrite at true precision | Done: "concentrated among White sons", "no evidence that it closes", "a slope gap cannot be rejected" | paper |
| 2(a) Education gradient of growth by race; premium by age band | Done. Return to schooling rises with age for White sons (diff in rise -0.055*** earnings); education = 0.44 of the divergence; growth on schooling W 0.010*** vs B 0.003 (diff -0.007**), NLSY79 equal | `42` A-B; Table 10 |
| 2(b) Within vs between jobs | Done. B-W growth gap at 25-34 = 3/5 within jobs, 2/5 at moves (-0.069** gain at moves) | `42` C; Table 11 |
| 2(c) Same-employer ladder with B-W in every column | Done | Table 9 (`44` from `36`) |
| 2(d) Sec. 5 consolidated; industry / promotion / tenure / displacement to appendix | Done | Sec. 5, App. B |
| 3(a) Self-employment split | Done. Exact-cell convergence = family business (0.065*** vs 0.009); occupation-level result survives (rich W - rich B 0.117***) | `43`; Sec. 6; Table 12 |
| 3(b) Cell counts in text; "exact jobs" out of the abstract | Done | Sec. 6 |
| 3(c) Employer following unobservable | Done (one sentence) | Sec. 6 |
| 4 Estimate the model | NOT DONE (3-4 months). Sec. 7 rewritten as an estimable spec: parental income only through schooling, access and an early transfer; race in access and in the schooling pay-off of accumulation (gamma_1), a race-specific search friction only if the move moments need it; moments and counterfactuals at 30 and 45 stated; sensitivity matrix before claiming identification | Sec. 7 |
| 5 NLSY97 corrected estimate | Done: one-year + RR correction in all three data sets, pooled 0.170*** (earnings) | `41` F; Table 3 |
| 5 OI request | Dropped (PI, 2026-10-18): not feasible from the UK | - |
| 6 Administrative route (SIPP-SSA, FSRDC) | Dropped (PI, 2026-10-18): restricted US data not accessible from the UK. Only the falsifiable prediction for administrative data is kept (Sec. 7.4) | Sec. 7 |
| 7 Quasi-experiments | Not added, as advised | - |
| 8 Writing | Abstract ~210 words; intro ~5 pages with literature folded in (Sec. 2 removed); 12 main tables; main text 38 pages; missing citations added | paper |

## Open decisions for the PI

1. When to start coding the Sec. 7 model (HPC rules apply).


## Round 2 (review dated 2026-10-18, now in `fable_review_paperB.md`)

Numbers: EVIDENCE.md 1.41-1.44, 9.26-9.29. Scripts 45, 46; tables via 28 (patched) and 44.

| Item | Status | Result / where |
|---|---|---|
| A1 One opening (bands 25-49), one sign convention, 0.090 vs 0.064, no pooled main-measure cell, Table 12 note | Done. All racial differences are White - Black in every table (28 flips at the getters; 44 likewise) and text; Table 2 reports the opening as 35+ minus below 35 | paper, 28, 44 |
| A2 Rank sentence | Done: sons' rank slopes do not diverge (0.015 within race, 0.037 national); both sexes within race 0.093** stated | abstract, Sec. 3.4 |
| A3 Within-cell identification | Done. Racial difference in the rise of the return to schooling survives early-cell and current-cell FE (earnings 0.061***, 0.066*** vs 0.058***); same-employer growth by schooling does not (0.004, p=0.37) | `45`; Table 11 (tab_within_cell); App. tab_afqt_growth |
| A4 AFQT and schooling by age, NLSY79 | Done. Both returns rise (not employer learning); race difference in the schooling rise 0.021** with AFQT; AFQT rise equal by race | `45`; App. tab_afqt_growth; Sec. 5.4 |
| A5 Experience clock | Done. Gap zero at 0-9 years of experience, opens after (0.243***); start at 27: 0.212*** | `46`; App. tab_experience; Table 4 |
| A6 Own reliability ratios | Done. Pooled corrected 0.191*** (0.046), Q p=0.47 | `46`; Table 3 |
| A7 Calendar trend of the return | Done. Racial difference in the rise 0.063** (earnings) net of the calendar; 0.051*** in cohorts 1955-69 | `45`; Table 11 |
| A8 NLSY79 children | Done. No opening (-0.103, s.e. 0.106) on small, selected late samples; four-data pooled one-year 0.086*** (Q p=0.079). Fable's risk 3 stated in Sec. 3.3 | `46`; Table 3 |
| A9 "White phenomenon", rich W - poor W, level of following, lambda terciles | Done | Sec. 6; tab_lambda |
| A10 Abstract ~150 words, intro ~10 numbers, Figure 1A on earnings, "small" removed, citations (Jacome et al. 2025, Neal-Johnson, Pinkston 2006, Bowlus-Eckstein 2002) | Done; two-page tables trimmed (Table 1 child-year columns, Table 2 panels A-D, Table 6 without time-varying score, Table 8 columns 1-5) | paper, 28, 31 |
| 4.1-4.3 Model changes | Done in Sec. 7: competing-model paragraph; logit access common to entry and on-the-job offers, no race x x; no transfer; b1(r) optional; schooling exogenous, experiment renamed "equalising schooling"; mu_r fixed and explained; G/O = Table 8 cells; observation scheme; identification table; nested models A-D | Sec. 7; `proposals/paperB_model_document.md` |
| B2-B7 Simulator, Jacobian, SMM, fit, counterfactuals | NOT DONE (3-4 months). Code plan in the model document | - |

Open: coding the model (B2-B7) on the PI's timing; circulating Sections 1-6 as a working paper (Fable's advice).
