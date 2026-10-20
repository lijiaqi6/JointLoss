# Paper A estimation diagnostics and model extensions, 2026-10-18 evening

Default size (`k_s2_era1_a20`), K = 3, CRN seed 20261018, real targets. Objective: the trimmed vector
(`moments.OBJ_EXCLUDE`: the three pooled CPS rates, which in the model are exact race-share averages of the Black and
White rates, and the three SIPP `_nosep` rows the model cannot produce) with `diag_noise` weights
1 / (se^2 + var_sim), var_sim from 5 CRN seeds at the pre-extension analytic start (`inputs/moment_noise.csv`). All
comparisons are on common draws. Scripts: `diagnostics_20261018/profile_sigma_ridge.py` (A, B),
`diagnostics_20261018/steps_table.py` (step table); start files of every variant in `diagnostics_20261018/`.

## Weights after the trim (analytic start, 85 moments)

| block | share of the diagonal weight: old (diag, 91) | trimmed diag (85) | trimmed diag_noise (85) |
|---|---:|---:|---:|
| Base hazards | 95.6% | 92.7% | 90.6% |
| Her exits | 3.1% | 6.0% | 8.1% |
| Her search | 0.7% | 0.6% | 0.4% |
| Separation | 0.1% | 0.3% | 0.4% |
| Joint loss, monthly | 0.1% | 0.2% | 0.3% |
| all other blocks | 0.3% | 0.1% | 0.2% |

Q at the analytic start: 75,239.1 (old objective; the new code reproduces it exactly) -> 68,106.9 (trimmed, diag) ->
50,920.3 (trimmed, diag_noise). The CPS hazards keep most of the weight because they are precise and the deltas fit
them one for one; the Levenberg-Marquardt step is indifferent to this concentration.

## A. sigma_eps profile (other values at the analytic start)

| | data (s.e.) | 0.05 | 0.10 | 0.20 | 0.30 |
|---|---:|---:|---:|---:|---:|
| Q total | | 50,920 | 44,860 | 50,652 | 57,938 |
| cps_wife_exit | 0.0261 (0.0001) | 0.0026 | 0.0035 | 0.0029 | 0.0020 |
| cps_entry_black | 0.0942 (0.0016) | 0.0844 | 0.1118 | 0.1392 | 0.1496 |
| cps_entry_white | 0.0751 (0.0003) | 0.0434 | 0.0698 | 0.1008 | 0.1130 |
| psid_wemp_none | 0.809 (0.005) | 0.948 | 0.971 | 0.987 | 0.991 |
| psid_wemp_05 | 0.754 (0.006) | 0.948 | 0.968 | 0.982 | 0.985 |
| psid_wemp_617 | 0.823 (0.004) | 0.942 | 0.966 | 0.983 | 0.988 |
| psid_es_w_emp_13_y05 (added worker, employment) | 0.042 (0.022) | 0.006 | 0.002 | -0.001 | -0.003 |
| psid_es_w_hrs_13_y05 (added worker, hours) | 87.9 (43.6) | 37.3 | 30.7 | 17.6 | 8.3 |
| psid_gross_all | 47.3 (30.4) | 59.6 | 50.1 | 34.9 | 25.0 |
| psid_offset_all | -36.0 (13.8) | -27.5 | -25.7 | -24.1 | -23.9 |
| sipp_wife_emp_s6 | 0.054 (0.010) | 0.169 | 0.151 | 0.094 | 0.040 |
| Q her exits | | 40,884 | 37,701 | 39,919 | 43,028 |
| Q her search | | 3,636 | 255 | 2,896 | 5,889 |
| Q employment levels | | 3,093 | 3,850 | 4,471 | 5,151 |
| Q safety net | | 126 | 84 | 494 | 927 |
| Q wealth | | 2,491 | 2,282 | 2,201 | 2,254 |

The exit rate does not move by the order of magnitude needed: 0.26% -> 0.35% -> 0.29% -> 0.20% a month against 2.6%.
A larger taste shock raises employment (0.95 -> 0.99) and entry, and shrinks the added-worker response. The option
value of holding a job (more alternatives than a non-employed wife) grows with sigma_eps, so wives keep their jobs.

**Recommendation: do not estimate sigma_eps; keep 0.05.** The exit target is reconciled by the CPS classification
correction instead (step 1).

## B. (p_H, m_H) ridge profile (before the extensions; delta rescaled to hold (E m) delta, pi_c unchanged)

| | data (s.e.) | p_H 0.03 | 0.05 | **0.10 (start)** | 0.15 | 0.20 | 0.25 | m_H 4 | m_H 8 | m_H 18 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| m_H | | 14.2 | 12.7 | 12.6 | 15.0 | 21.7 | 54.4 | 4 | 8 | 18 |
| kappa - 1 | | 2.60 | 2.60 | 2.60 | 2.60 | 2.60 | 2.60 | 0.48 | 1.53 | 3.57 |
| psid_cy_diff_all | 0.063 (0.005) | 0.081 | 0.097 | 0.118 | 0.132 | 0.143 | 0.152 | 0.041 | 0.080 | 0.154 |
| psid_cy_diff_diff | 0.041 (0.005) | 0.072 | 0.088 | 0.108 | 0.123 | 0.135 | 0.144 | 0.032 | 0.072 | 0.144 |
| psid_cy_diff_same | 0.184 (0.022) | 0.140 | 0.152 | 0.183 | 0.190 | 0.198 | 0.204 | 0.098 | 0.136 | 0.217 |
| psid_perm | 0.020 (0.009) | 0.010 | 0.014 | 0.024 | 0.046 | 0.080 | 0.143 | 0.021 | 0.023 | 0.026 |
| psid_contemp | 0.033 (0.015) | 0.025 | 0.035 | 0.060 | 0.082 | 0.100 | 0.116 | 0.018 | 0.042 | 0.076 |
| cps_jl_nt_m3 | 0.0067 (0.0021) | 0.0054 | 0.0058 | 0.0066 | 0.0070 | 0.0076 | 0.0072 | 0.0018 | 0.0040 | 0.0097 |
| cps_jl_nt_m1 | 0.0064 (0.0012) | 0.0053 | 0.0059 | 0.0067 | 0.0076 | 0.0075 | 0.0077 | 0.0017 | 0.0046 | 0.0091 |
| cps_jl_nt_p1 | 0.0056 (0.0011) | 0.0044 | 0.0049 | 0.0056 | 0.0064 | 0.0074 | 0.0081 | 0.0015 | 0.0037 | 0.0077 |
| cps_jl_nt_p3 | 0.0061 (0.0016) | 0.0067 | 0.0069 | 0.0077 | 0.0068 | 0.0072 | 0.0080 | 0.0014 | 0.0038 | 0.0104 |
| psid_disp2plus_B | 0.151 (0.014) | 0.205 | 0.189 | 0.177 | 0.174 | 0.190 | 0.205 | 0.260 | 0.211 | 0.151 |
| psid_disp2plus_W | 0.133 (0.008) | 0.097 | 0.099 | 0.114 | 0.128 | 0.142 | 0.156 | 0.131 | 0.124 | 0.108 |
| Q joint loss, monthly | | 33.6 | 26.9 | 25.2 | 27.2 | 31.1 | 38.0 | 112.7 | 48.9 | 44.2 |
| Q joint loss, annual | | 37.6 | 92.1 | 211.1 | 337.6 | 483.1 | 724.7 | 29.9 | 36.8 | 539.7 |
| Q base hazards | | 127.3 | 154.9 | 164.9 | 201.4 | 237.2 | 277.6 | 79.9 | 72.6 | 308.9 |
| Q total | | 50,683 | 50,790 | 50,920 | 51,089 | 51,339 | 51,704 | 50,533 | 50,515 | 51,625 |

Along the CPS ridge the monthly leads and lags stay near the data while the PSID annual excess falls with p_H: a
rarer, riskier type gives the CPS short-horizon elevation without the doubled annual excess. Off the ridge (fixed
p_H 0.10) a smaller m_H fits the annual excess only by losing the leads and lags (m_H 4: lags 0.0015 against 0.006).
With the classification correction on (step 2 below) the ridge continues: p_H 0.02 gives 0.071, p_H 0.015 gives 0.063.

**Recommendation: keep p_H and m_H estimated; start on the ridge at p_H = 0.02 (m_H 15.95), not at 0.10.** The
annual excess and T28 separate p_H along the ridge (joint-loss and base-hazard Q 401 at p_H 0.10, 185 at 0.02, 183 at
0.015), so fixing p_H is not needed; the memory alternative (step 2) fits worse with one more parameter.

## C. Jacobian at the analytic start (trimmed objective, diag_noise weights; `jacobian_20261018_210500_p11844`)

- Condition number: range scaling 81.5 (162 before the trim, without kappa_S); value scaling 3.4e3, entirely from
  theta_05 (start value -0.0014, so 10% of its value is no move; its range norm is 21.9).
- No pair of columns with |corr| > 0.9. The lam_w_W / theta_05 / theta_617 / F cluster of the old weighting (all
  through `cps_entry_pooled`) is gone with the trim.
- Weakest directions (range scaling): pi_dn_h 0.84 / sigmaJ_B 0.42 / d_h -0.28 (sv 1.96); lam_h_B -0.71 / sigmaJ_B
  0.56 / lam_h_W 0.33 (2.15); sigmaJ_B / lam_h_B / pi_dn_h (2.43); F -0.95 (2.78); sigmaJ_W -0.82 / p_H / d_w / m_H
  (3.84).
- Smallest range norms: sigmaJ_B 4.3, pi_dn_h 4.6, lam_h_B 5.9, sigmaJ_W 7.0, a_bar 7.0, F 7.4, kappa_S 7.8 (largest:
  delta_w_W 146, phi_P 125).

At the extended start (`jacobian_20261018_220519_p3092`, 31 free, report with the final weights in
`report_final_weights.md`): range condition number 529; weakest directions m_H 0.77 / eta_up 0.49 (sv 1.14), pi_dn_h
0.91 / d_h -0.33 (1.29), lam_h_B / sigmaJ_B / lam_h_W (2.12), F (2.17); 48 column pairs above |corr| 0.9, all through
the classification-corrected CPS entry rates, which at 95-96% employment react to every parameter that moves the
employment level (Her search is the top block of 21 of 31 columns). This collinearity is a start-value artefact; the
Jacobian has to be re-read at the LM candidate.

**Weakly identified (both starts): sigmaJ_B and sigmaJ_W, pi_dn_h with d_h, lam_h_B against lam_h_W, F, kappa_S,
a_bar; at the extended start also m_H with eta_up.** The ties remain an option only (`--tie`), not applied.

## Step-by-step extensions (each evaluated at the analytic start, same 85-moment set and weights; step 5 adds 2 moments)

| step | change | Q total | her exits | her search | employment levels | joint loss monthly + annual | base hazards | wage growth | wealth | key moments |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 | baseline (trimmed, diag_noise) | 50,920.3 | 40,884 | 3,636 | 3,093 | 236.3 | 164.9 | 161.9 | 2,491 | exit 0.0026 (0.0261); entry W 0.043 (0.075) |
| 1 | + CPS classification error (Poterba-Summers 1986, women 25-59) in entry and exit | 68,612.4 | 259 | 61,954 | 3,093 | 236.3 | 164.9 | 161.9 | 2,491 | exit 0.0243; entry W 0.193, B 0.311 (0.094) |
| 2a | + memory c_mem = 5.82 (coded), type on the PSID permanent part (m_H 4.33 at p_H 0.10) | 64,855.7 | 223 | 58,436 | 3,037 | 177.3 | 80.7 | 161.1 | 2,468 | annual excess 0.092; lags +-1 0.013-0.014 (0.006) |
| **2** | **instead: type on the CPS ridge, p_H 0.02, m_H 15.95 (no new parameter)** | **68,086.0** | 252 | 61,651 | 3,094 | **61.6** | 123.3 | 161.3 | 2,494 | annual excess 0.071 (0.063); lags 0.0034-0.0061 |
| 3 | + borrowing wedge (8.4 points, coded) | 64,657.3 | 229 | 58,103 | 3,050 | 60.9 | 124.1 | 158.2 | 2,672 | liq<=0 25-34 0.477 (0.568), 45-59 0.085 (0.381); top 45-59 0.388 (0.177) |
| 4 | + eta_up 0.5 (pi_up rescaled to hold 25-34 growth) | 92,874.7 | 373 | 85,691 | 3,589 | 62.5 | 122.4 | 150.5 | 2,599 | wage growth W 45-54 0.045 (0.027), H 0.037 (0.013); wemp 0.955 |
| 5 | + husband's employment target (87 moments) | 93,910.3 | 373 | 85,691 | 4,625 | 62.5 | 122.4 | 150.5 | 2,599 | hemp B 0.999 (0.882), W 1.000 (0.943) |
| 6 | race ties | not applied | | | | | | | | |
| new start | analytic_start --ext hc_eta --eta-start 0.5 (pi_up closed-form rescale; wage process re-mapped) | **90,377.5** | 351 | 82,169 | 4,570 | 62.8 | 122.9 | 149.4 | 2,668 | EXPECTED_Q |

Supporting evaluations (same draws): the wedge with a_bar 15 / 25.6 / 40 / 55: Q 65,618 / 64,657 / 63,529 / 64,413,
wealth 3,079 / 2,672 / 2,419 / 2,317; without the wedge a_bar 15 / 25.6 / 40: Q 66,522 / 68,086 / 69,845, wealth
2,046 / 2,494 / 2,953. eta_up with pi_up rescaled, 0.5 / 1 / 1.5 / 2 / 2.5: wage-growth Q 150.5 / 144.6 / 136.3 /
123.2 / 109.4, total Q 92,875 / 117,131 / 139,040 / 155,365 / 159,422 (employment rises at given preferences).

Decisions and reasons:
1. **sigma_eps vs classification:** classification correction chosen (A: sigma_eps cannot move exits). It closes the
   exit miss (z -226 -> -18). With Poterba-Summers' 1981 error rates the measured entry of married wives is at least
   0.083 at the data's employment level of 0.81 (spurious entries of misrecorded employed wives alone), above the
   White target 0.075: solving the 2 x 2 system for the true flows gives a negative true entry rate. Poterba and
   Summers note that serially uncorrelated errors overstate the adjustment, and the CPS targets start in 1994, after
   the redesign with dependent interviewing. The entry rate will therefore be missed from above; scaling the error
   rates for the post-1994 CPS is a PI decision. At the start the entry overshoot is large because employment is
   0.95 (her search Q 61,954).
2. **memory vs type on the ridge:** the ridge wins on the criterion (CPS leads/lags and PSID annual excess) with no
   new parameter (61.6 against 177.3); the memory start overshoots the +-1-month lags (0.013 against 0.006). Memory
   lowers total Q at the start (64,856 against 68,086) through her search and the base hazards, side effects of its
   different m_H and delta that the preference parameters re-fit. Kept as `--cs-memory on`, off by default.
3. **borrowing wedge:** on. It lowers Q at every a_bar tried (63.5-65.6 thousand against 66.5-69.8 thousand) and lets
   the young debt share match at a credit limit of 40-55 thousand dollars; it does not fix the 45-59 shape (too few
   at or below zero, too many above one year of earnings, with or without the wedge).
4. **eta_up:** on, estimated, start 0.5. The wage-growth block falls monotonically in eta (158 -> 109), the 45-54
   growth falls (husbands 0.038 -> 0.032), but even at 2.5 the gap to the data (0.013) stays mostly open; the
   closed form from mean levels by age needs 6 (wives) to 16 (husbands), outside the bounds. The age profile of
   accumulation needs more than level dependence.
5. **husband's employment target:** in the objective. The model's husbands have positive hours in 99.9% of
   couple-years against 88.2% (Black) and 94.3% (White): they leave jobs only by displacement and find one at 0.26 a
   month, so full-year non-employment does not occur. No parameter of the current model reaches the target; it will
   pull lam_h down against the SIPP re-employment path. `--drop psid_hemp_B psid_hemp_W` removes it.
6. **ties:** not applied.

Weights at the new start: the 5-seed noise at the extended start inflates the simulation s.d. of the entry rates
sevenfold (0.0004 -> 0.0030: with 5% true non-employment the corrected entry rate is a ratio dominated by spurious
entries and very sensitive to the employment share), which would cut her-search weight to 0.01%. `inputs/moment_noise.csv`
therefore keeps the pre-extension noise (plus the husband-employment rows from the new run); the noise should be
recomputed at the LM candidate (`Joint-noise`) before CMA-ES.

Test status: tests 1-4 and 6-11 pass. Test 0 (EGM vs brute force) fails at the current start values (99th percentile
3.4e-3, max 0.16) because of the kappa_S start fix (20:16; SNAP take-up adds the asset-test kink); with kappa_S = 2.64
the same code passes as before (99th percentile 4.5e-5). The solver near the SNAP asset limit needs a look before the
main run. Test 5 (exits rise when UI lapses) failed at the new start because its delta_w = 0.01 override gave the
start's rare type (p_H 0.02, m_H 15.95) 16% monthly hazards; it now sets m_H = 1 and passes, but only marginally at the
interior point (just lapsed minus still entitled +0.000 with n = 265, against +0.027 at the old start; entitled vs not
+0.007, UI removed +0.007). Smoke runs on the PC (two free parameters): polish 2 iterations Q 90,378 -> 61,800 with the
final Jacobian, report and sandwich s.e.; CMA-ES with --cma-stds-from (stds 1.29 / 0.71), --tolfun 30, mean.json,
recorded seed, and --resume. pycma runs the generation in which the evaluation count reaches maxfevals (32 / 16 -> 48);
the HPC test now checks counts accordingly.

What the model section must say (not edited here): the CPS layer applies Poterba-Summers response errors to the
wife's monthly status in the entry and exit rates; the borrowing rate is the saving rate plus a calibrated 8.4-point
wedge (G.19, 1995-2021); accumulation pi_up_j (h/4)^(-eta); the couple type starts at p_H 0.02 on the CPS ridge; the
husband's employment rate by race is a target that the model misses because husbands leave jobs only by
displacement; sigma_eps stays a fixed scale (profile in A).

## Follow-ups 2026-10-19 (one at a time, at the extended start)

| step | change | Q total | her exits | her search | employment levels | moments in the objective |
|---|---|---:|---:|---:|---:|---:|
| start (2026-10-18) | as committed in 7c9bb3a | 90,377.5 | 351 | 82,169 | 4,570 | 87 |
| 1 | solver fix at the SNAP asset limit | 90,295.9 | 351 | 82,052 | 4,572 | 87 |
| 2 | persistent CPS entry / exit replace the Poterba-Summers one-month flows | 12,761.1 | 4,622 | 246 | 4,572 | 87 |
| 3 | husband's employment reported, not targeted | **11,726.0** | 4,622 | 246 | 3,537 | 85 |

**1. Check 0.** The SNAP asset test makes next month's value drop where assets cross L = 1.884 thousand dollars (the
SNAP alternative leaves the logsum). The drop lay inside the asset segment [-2.57, 3.70]; the Hermite continuation
value smeared it and the first-order conditions missed the bunching at a' = L. The large gaps sat at low cash on hand
with a' between -1.5 and -0.4 (up to 0.15). Fix: nodes at L and L + 1e-5, the corner a' = L as a candidate in every
query, a two-branch EGM where the endogenous grid falls only at the drop (79% of states are monotone or monotone on
both sides of L, as before the fix), a 9-point search with up to 6 Newton steps where the marginal value rises.
Check 0 (99th percentile / maximum of |EGM - brute force|): start 1.7e-4 / 2.6e-3; kappa_S = 0: 7.0e-4 / 2.4e-3;
kappa_S = 2.64: 3.7e-5 / 1.2e-4 (criterion 1e-3 / 5e-3). Check 3 now samples the node at L: losing eligibility raises
P(works) by 0.0002-0.0018 there (the asset-test notch, excluded from the monotonicity count). All 12 checks pass.

**2. CPS flows.** Same filter in IGE/60 and the simulated panel: a transition counts if the old status held in t-1 and
t and the new one holds in t+1 and t+2 (all four months in one CPS rotation spell; husband employed in t and t+1).

| moment | data (s.e.) | model, one-month raw | model, Poterba-Summers | model, persistent |
|---|---:|---:|---:|---:|
| exit, one-month | 0.0261 (0.0001) | 0.0023 | 0.0240 | |
| entry White, one-month | 0.0751 (0.0003) | 0.047 | 0.208 | |
| entry Black, one-month | 0.0942 (0.0016) | 0.099 | 0.364 | |
| exit, persistent | 0.0101 (0.0001) | | | 0.0014 |
| entry White, persistent | 0.0320 (0.0004) | | | 0.0358 |
| entry Black, persistent | 0.0404 (0.0019) | | | 0.0885 |
| Q total (87 moments) | | 52,380 | 90,296 | 12,761 |

The filter cuts the data's exit rate from 2.6% to 1.0% a month and the entry rates by about 60%; the model's flows
are almost all persistent already. The persistent exit rate is the largest misfit at the start (z -69; 4,622 of
11,726): wives in the model still leave jobs about seven times less often than the data's filtered rate.

**3.** `psid_hemp_B/W` (data 0.882 / 0.943, model 0.999 / 1.000) are in `OBJ_EXCLUDE` with the reason that husbands
leave work only by displacement; they stay in the fit table.
