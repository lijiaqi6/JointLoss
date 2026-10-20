# Pre-built extensions, 2026-10-19: new-job exit hazard and separation after her displacement

Both are behind `estimate.py` flags that default to off (`EXT_DEFAULTS`), ready to be tested one at a time on the first
HPC estimate. Evidence: `proposals/wife_exit_evidence.md` (IGE/63) and `proposals/separation_ui_evidence.md`,
`output/her_loss_robustness.md` (IGE/64, 65). Targets: `IGE/66.PaperATargetsExt.py` ->
`output/paperA_targets_ext.csv` (+ `paperA_targets_ext_vcov_sipp.csv`), merged only when a flag is on or
`--ext-targets` names the extension.

## Design

**Extension 1, `--new-job on`** (parameter `xi_nj`, start 0.02, bounds [0, 0.2]). One more wife labor state, EN =
"employed on a job started less than about a year ago", allocated only when the flag is on (index 4 of the wife's labor
state; every other index unchanged). A wife who takes a job (job finding from non-employment, or an accepted offer at
the UI offer node) enters EN; wives employed at entry start established. On EN with positive hours, after the month's
displacement draws: the new-job exit with probability `xi_nj`; otherwise the job becomes established with probability
`nj_grad` = 1/12 a month (geometric, mean 12 months; fixed input, `--set-fixed nj_grad=...`). Choice for the exit
(fixed input `nj_ui`, default 0): treated like a quit (next month non-employed, not entitled; human capital as in a quit
month, the slice a quit already uses, so no new slice), because two thirds of the SIPP tenure gradient remains when
involuntary job ends are dropped (IGE/63: tenure 0-5 +0.77 pp*** without them vs +1.33 pp*** with them). With
`nj_ui=1` it is treated like a displacement (UI take-up q, displacement loss, recorded as her displacement). CRN slots
42 (exit) and 43 (graduation). Cost: solve 154 -> 217 s per evaluation (+41%; 5 instead of 4 wife states).

**Extension 2, `--her-sep on`** (parameter `sigmaJw`, start 0.01, bounds [0, 0.1]; `--her-sep-tie on` sets it to his
sigma_J(r) and holds it). The separation hazard is sigma_0(r) + sigma_J(r) 1{he is non-employed next month} + sigma_Jw
1{she is UI-entitled next month}, additive, capped at 1. Her term keys on the entitled state after her own displacement
(the memo's recommendation: most of her non-employment is quits and child-related), the only post-displacement state of
the wife in the model; it lasts while she is entitled (expiry 1/6 a month or re-employment), whereas his lasts while he
is non-employed (husbands leave work only by displacement). A displaced wife who does not take up UI (1 - q = 0.51) gets
no elevation; sigma_Jw absorbs this. Solver: a separate kernel `k_tilde_w` with the table SG[lw, lh] (`solve.sep_table`),
used only when the flag is on; no new state, no cost (solve 153 s).

**Parameters** sit in `params.LATE_PARAMS`, appended after sigma_eps in every theta vector (`NAMES` = 33 + 1 + 2), so
`PARAMS`, `N_PARAMS` = 33, the indices of earlier runs' vectors (run.json idx, jacobian.npz) and the default free set
(30 at the default size) are unchanged; `pad_vec` completes older vectors with the nested values 0.

## Targets (`output/paperA_targets_ext.csv`)

| id | ext | data | s.e. | role | source |
|---|---|---:|---:|---|---|
| sipp_wexit_ten_0_5 | new_job | 0.02058 | 0.00072 | target | IGE/66 (63's SIPP sample), cluster bootstrap 200 |
| sipp_wexit_ten_6_11 | new_job | 0.01595 | 0.00069 | target | same |
| sipp_wexit_ten_12p | new_job | 0.00676 | 0.00013 | target | same (63's 12-35 and 36+ pooled) |
| sipp_wexit_return12 | new_job | 0.530 | 0.008 | reported | 63 table iv, KM |
| psid_wexit_repeat2 | new_job | 0.324 | 0.009 | reported | 63 v-repeat (binomial s.e.) |
| psid_es_bh_present_13 | her_sep | -0.0502 | 0.0123 | target | 65 Section 5b (attrition equalised), CR1 s.e. |
| psid_es_bh_present_46 | her_sep | -0.0940 | 0.0166 | reported | same |

Model measurement (`panels.sipp_tenure_exits`, `psid_repeat_exits`, `her_stack_rows`; `moments.compute(ext_moments=)`):
tenure = months since the start of the current employment spell (the model has no job-to-job moves, so data tenure,
which restarts at every employer change, is shorter on average); spells running since the couple's entry are unknown
unless 12+ months old. Her design as 64's M3: baseline married with a child and her positive hours, treated = her
first displacement since entry at any marital status, clean controls to ev + 6 (CRN 15% subsample, slot 53), year x
stack and unit FE, e = -2 reference; the model has no attrition and no remarriage, so 65's "both observed" restriction
does not bind and the attrition-equalised estimate is the comparable target.

## Step table at the analytic start (default size, K = 3, seed 20261018, diag_noise weights; same moment set in every
row: the 85 base moments + 4 extension targets = 89 in the objective, 3 reported)

| step | Q total | her exits | her exits by tenure | separation after her loss | her search | employment levels | wealth |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0 base (both flags off, `--ext-targets new_job her_sep`) | 13,232.5 | 4,623.3 | 1,482.9 | 15.9 | 245.1 | 3,535.9 | 2,710.6 |
| 1 `--new-job on` (xi_nj 0.02) | 13,245.7 | 4,228.5 | 1,800.7 | 15.8 | 296.3 | 3,424.5 | 2,858.2 |
| 2 `--her-sep on` (sigmaJw 0.01) | 13,162.8 | 4,631.6 | 1,468.1 | 6.6 | 178.7 | 3,478.7 | 2,756.3 |

New moments, data vs model:

| id | data | base | new_job on | her_sep on |
|---|---:|---:|---:|---:|
| sipp_wexit_ten_0_5 | 0.0206 | 0.0354 | 0.0416 | 0.0351 |
| sipp_wexit_ten_6_11 | 0.0160 | 0.0096 | 0.0151 | 0.0097 |
| sipp_wexit_ten_12p | 0.0068 | 0.0027 | 0.0028 | 0.0027 |
| sipp_wexit_return12 (reported) | 0.530 | 0.683 | 0.692 | 0.677 |
| psid_wexit_repeat2 (reported) | 0.324 | 0.290 | 0.257 | 0.289 |
| psid_es_bh_present_13 | -0.050 | -0.001 | -0.002 | -0.019 |
| psid_es_bh_present_46 (reported) | -0.094 | -0.003 | -0.003 | -0.020 |
| cps_wife_exit_p | 0.0101 | 0.0014 | 0.0018 | 0.0014 |

Reading (start values, not estimates). At the start the model already has a steep tenure profile from selection (just
re-employed wives at the margin leave again: 3.5% a month at 0-5 months, above the data's 2.1%) and far too few exits
from established jobs (0.27% vs 0.68%). The new-job hazard fits 6-11 months but raises 0-5 further and cannot move 12+,
so at xi_nj = 0.02 it lowers the CPS exit misfit (her exits 4,623 -> 4,229) but worsens the tenure block (1,483 ->
1,801): its value has to be judged at re-estimated preferences (the first HPC estimate), where the 12+ level is set by
the work-cost parameters. Her-displacement separations move the right moment in the right direction (-0.001 -> -0.019
against -0.050) with no state cost; the hazard keyed on entitlement fades within months, so years 4-6 stay far from
the data (-0.020 vs -0.094), as for his displacement.

## Default path (both flags off): bit-identity check

- The new code with both flags off gives exactly the moments of the committed code (HEAD 130abcf) under the same numba
  compilation state: max |difference| 0.0 over all 91 moments, Q 11,733.70280 (both, fresh compile) and 11,733.68475
  (both, cache-loaded), runs with separate `NUMBA_CACHE_DIR`s and a scratch copy of HEAD. Model arrays identical
  (test 12a); stored solution of one problem identical by hash once compiled.
- **The committed code does not reproduce `EXPECTED_Q = 11,726.0` / `inputs/expected_start_moments.csv` from a clean
  build**: HEAD gives Q 11,733.7 (fresh) on this PC and Stanage gave 11,733.6 (`results/INTAKE.md`); the 11,726.0 came
  from the PC's numba cache of 2026-10-19 morning (the first evaluation of this session, with that cache, gave exactly
  11,726.0 and the expected moments; editing solve.py / simulate.py recompiled their kernels). A fresh compile and a
  cache-loaded run of the same source also differ (Q 11,733.703 vs 11,733.685; moments up to 9e-5): the numba
  binaries are not bit-stable across compilations. The HPC rule (Q within relative 1e-3: 6.6e-4) passes; the moment rule
  (relative 1e-6) does not, as before this change. `EXPECTED_Q` and the expected moments were not changed (task rule);
  the lead may refresh them from a clean build.
- Solve time with the flags off: 152.0 s vs 154.8 s for HEAD (cache-loaded, run side by side), 261.8 vs 267.9 s
  (fresh compile): no slowdown.
- Tests (`results/tests_20261019.txt`): 13/13 PASS, the 12 earlier checks plus the new test 12 (flags off: Model
  arrays identical; moments with xi_nj, sigmaJw set but the flags off identical to a pre-extension theta vector; Q
  11,733.68 within the HPC rule of EXPECTED_Q). Test 11 first failed (KeyError 'xi_nj': a theta dict without the new
  keys); `estimate.dict_vec` now fills them with 0, and test 11 passes when re-run.
- Smoke runs (K = 1): `--her-sep on --her-sep-tie on` and `--new-job on --set-fixed nj_ui=1` run end to end (with
  nj_ui = 1 the CPS job-loss hazard of wives rises to 0.0040 / 0.0026 against 0.0034 / 0.0022 in the data).
