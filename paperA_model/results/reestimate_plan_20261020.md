# Fable's two unchecked claims, a correction to its weight diagnosis, and the re-estimate plan (2026-10-20)

Source: `proposals/fable_top5_distance_paperA.md`. Everything below is from the code and from the stored outputs of
Joint-gn-main 11865967 (`results/hpc_runs/polish_main_20261020_040752_j11865967/`: best.json moments, run.json
exclusions, jacobian.npz). No model was solved or simulated. Q by block reproduces the run's Q exactly (1,359.60).

## 1. Claim: the model pays the EITC monthly. Confirmed.

`model.eitc_month` (model.py:100-105) takes one month's family earnings, annualises them (x 12), applies the annual
married-filer schedule and pays 1/12 of the result in that month; `inc0` / `incS0` add it month by month
(model.py:471-480, 494-504). Earnings only (UI excluded, as in the law). Consequences:

- In a month with no earner the credit is zero; in the law it depends on the year's earnings and is paid at tax time.
- The model therefore cannot produce Section 5's finding that the annual credit rises by $196*** after a joint loss
  (annual earnings fall into the phase-in or plateau, so the credit goes up).
- The paper states the monthly rule openly (sec7_model.tex, eq. `eq:eitc`: "paid monthly on annualised family
  earnings ... zero when no one earns"), and counterfactual (iii) argues from it ("the subsidy pays only when someone
  works"). That argument is the model's assumption, and Section 5 contradicts it. The fix is year-to-date earnings
  accounting (Fable plan item 3). It is a model change and comes after the re-estimate below.

## 2. Claim: counterfactual (i) also removes ~22% of displacement risk. Confirmed; the figure is 24-26%.

A working spouse's monthly displacement probability is pi_c(s) + (1 - pi_c(s)) m_tau delta_j(r) (model.py:346-355).
Scenario `i_common_off` (counterfactuals.py:83) sets pi_c = 0 and m_H = 1 and leaves delta alone, so each
spouse's marginal hazard falls to delta. At the LM estimate (p_H 0.0214, m_H 14.93, so E[m_tau] = 1.298; workplace
shares from fixed_inputs.json; s = 1, 2 merged):

| spouse, race | delta | marginal hazard at the estimate | cut by (i) |
|---|---:|---:|---:|
| husband, Black | 0.00486 | 0.00640 | 24.0% |
| wife, Black | 0.00298 | 0.00396 | 24.6% |
| husband, White | 0.00279 | 0.00372 | 24.9% |
| wife, White | 0.00204 | 0.00275 | 25.6% |

The couple type causes 23 of those points (1 - 1/1.298); the common shock adds 1-3. These are hazards while employed.
The count of displacements falls by somewhat less, because high-type couples spend more months out of work; the
`his_losses` column of a counterfactuals run gives that count. Fable's conclusion stands: the smoke-test welfare gain of
+1.09% mixes less correlation with less risk.

Also: the paper (sec7_model.tex:610) describes (i) as pi_c = 0 only; the code also sets m_H = 1. The text and the code
must agree once the scenario is redefined.

**Marginal-preserving decorrelation.** Two versions, each needing a hook:
- (i-a) mean-preserving: pi_c = 0, m_H = 1, and delta_j(r) replaced by the marginal hazard in the table (by race and
  spouse; by (r, s) if the s gradient matters). This removes the correlation and the heterogeneity of risk across
  couples.
- (i-b) distribution-preserving: draw each spouse's type independently (tau_w, tau_h with P = p_H each) and turn the
  common shock into two independent shocks of probability pi_c(s). Each spouse keeps their hazard distribution; only
  the joint distribution changes. This is the clean experiment. It needs separate m for the wife and the husband in
  `Model` and four types per (r, s) in the simulator.

## 3. Correction: the base hazards do not carry 92% of the weight

Fable's figure (91.9% base hazards, 0% earnings) is the `weight shares by block` line of the job log
(`moments.weight_shares`). That line adds the raw diagonal weights 1/(se^2 + var_sim) across moments in different
units: a hazard with se 4e-5 gets weight ~6e8, an earnings moment in dollars with se 1,750 gets ~3e-7. The shares
measure units, not importance. The earlier review (`proposals/fable_estimation_review_paperA.md`, "four moments carry
92%") used the same table. Under inverse-variance weights every moment enters Q as z^2, whatever its units.

**Where the misfit is (Q by block at the LM estimate, z units):**

| block | moments | Q | share of Q | largest abs z |
|---|---:|---:|---:|---:|
| Wealth | 6 | 775 | 57% | 22.9 (liquid wealth <= 0 at 45-59: 0.38 data, 0.18 model) |
| Wage growth | 13 | 192 | 14% | 6.7 (her wage growth at 45-54: 0.027 data, 0.051 model) |
| Employment levels | 5 | 65 | 5% | 7.5 |
| Safety net | 4 | 55 | 4% | 6.7 (SNAP, Black: 0.150 data, 0.103 model) |
| His search | 5 | 53 | 4% | 4.8 |
| His earnings | 4 | 51 | 4% | 4.7 (loss years 1-3, White: -12,054 data, -3,739 model) |
| Base hazards | 10 | 45 | 3% | 4.7 |
| Joint loss, monthly | 10 | 28 | 2% | 4.1 |
| Her search | 5 | 24 | 2% | 3.4 |
| Separation | 4 | 24 | 2% | 3.9 |
| Joint loss, annual | 5 | 21 | 2% | 3.2 |
| Consumption | 5 | 14 | 1% | 2.3 |
| Added work | 7 | 13 | 1% | 2.1 |
| Her exits | 1 | 1 | 0% | 1.0 |
| Her earnings | 1 | 0 | 0% | 0.1 |
| total | 85 | 1,360 | | |

**Which blocks pin which parameter** (share of each parameter's information, sum over moments of
(dm/dtheta x 0.1 theta x sqrt(w))^2, from the final Jacobian): each parameter is pinned by the block it was designed
for. Base hazards give 90-97% for the deltas; the monthly joint loss gives 89-94% for pi_c; employment levels give
70-94% for the disutilities; wealth gives 98% for a_bar; separation 33-79% for sigma0 / sigmaJ. Averaged over the 31
parameters: employment levels 25%, base hazards 18%, her exits 14%, joint loss monthly 8%; consumption 0.6%, his
earnings 1.3%, added work 0.7%.

**What follows.**
1. The weights did not cause the misfit. Base hazards contribute 3% of Q at the estimate. The consumption, earnings-loss
   and added-work moments carry little information because no parameter moves them much (d_h gets 9% of its
   information from his earnings), not because they are under-weighted. Moving their weight up would buy little fit and
   cost precision elsewhere. Their misfit points to missing model features: Fable's items 2 (smoothing technology) and
   5 (displacement scarring, husbands' exits).
2. The largest single misfit is liquid wealth at 45-59 (39% of Q from one moment). The model holds too much liquid
   wealth late in working life (too few couples at or below zero), and a_bar rises to its bound of 60 to push more of
   them below zero. Wage growth at 35-54 is also too fast in the model (z 5-7), which raises late-career income and
   saving. An illiquid or retirement asset, or the net-worth target (script 77), is where the fit will move.
3. The coded `--weighting block` (moments.py:155-164) has the same units problem. It sets each block's raw weights to
   sum to the same constant. At the LM estimate that gives Q = 1.9e8 from his earnings (dollar deviations) and ~0 from
   everything else. **The `Joint-smm-block` command in README.md and hpc_job_a.py must not be run until this is fixed.**
   The scale-free version is w_i = (1/(se_i^2 + var_sim,i)) x N / (B n_b), which gives each block the same weight in
   z^2 terms.
4. `weight shares by block` in run.json and the job logs should be replaced by Q share and information share, the two
   tables above.

## 4. The re-estimate, one step at a time

Every step is an LM polish (`polish`, ~4.5 h, `--time 10:00:00`) on one moment set and one input set, compared on
common draws (seed 20261018, K = 3). The noise band for Q is about 50 (fresh seeds at the LM estimate: 1,355-1,409).
Under diag_noise weights ΔQ is not a chi-square statistic; a restriction passes when ΔQ stays within the band and no
block's fit worsens by more than its own noise.

**Step 0 (PI, on Stanage): the new clone.** Deploy key, `~/jointloss`, scp the entry couples, `Joint-test` (steps in
the `hpc_job_a.py` docstring). No estimation job runs before Joint-test passes.

**Step 1 (code, PC; no change to the economics or the objective of the main spec):**
- (a) fix `--weighting block` to the scale-free form; replace `weight_shares` with Q share and information share;
  extend test 11 to check that rescaling one moment's units leaves the block weighting unchanged.
- (b) counterfactual hook (i-a), and the m_w / m_h split needed for (i-b).
- Run `tests/run_all.py`; `estimate.py evaluate` must still give 11,733.7 at the analytic start.

**Step 2: the BPS wage-process correction (PI decision 2026-10-19), INTAKE 2b items 1-4.** New `wage_process.json`
(sig_nu_h 0.166 -> 0.180, sig_nu_w 0.112 -> 0.134, from the clean spec), new baseline (`evaluate` at the analytic start
and at the gn best.json, new EXPECTED_Q), then `Joint-gn-bps` from the gn best.json. **This estimate is the reference
point for every comparison below.**

**Step 3: parsimony restrictions, each its own LM from the step-2 estimate (four jobs, can run at the same time):**

| job | change | why | command (after `cd ~/jointloss && git pull`) |
|---|---|---|---|
| Joint-gn-fixF | F fixed at 0.101 (the analytic start: 10% of her part-time earnings at level 4) | F's moments are within 1.5 se of zero; F rose 0.10 -> 0.57 next to phi_F | `... polish --label fixF --start <bps>/best.json --fix F=0.10116 --push` |
| Joint-gn-sigJ | sigmaJ_W = sigmaJ_B | race-specific sigmaJ not separable (s.e. ~0.003 around 0.001) | `... polish --label sigJ --start <bps>/best.json --tie sigmaJ_B=sigmaJ_W --push` |
| Joint-gn-abar | a_bar fixed at 25.64 (minus P10 of liquid wealth, wife 25-34; IGE/62) | a_bar at its bound of 60 | `... polish --label abar --start <bps>/best.json --fix a_bar=25.639 --push` |
| Joint-gn-lamh | lam_h_W = lam_h_B | test, not assert (Fable section 4) | `... polish --label lamh --start <bps>/best.json --tie lam_h_B=lam_h_W --push` |

(`...` = `sbatch --job-name=<job> --time=10:00:00 paperA_model/hpc_job_a.py`.) Expected: fixF and sigJ pass, since
they drop directions the data cannot separate. abar will worsen the wealth fit, because a_bar is the only parameter
that moves it (98% of its information). If so, a_bar stays free until step 5 adds the asset feature. That result is
still informative. The restrictions that pass are combined in one LM (`Joint-gn-restr`), and that becomes the new
reference.

**Step 4: three workplace groups.** A new size with `merge_s12=False` (7 levels, one era, 20 asset points; ~1.5 x the
evaluation time). A new size means a new baseline: `evaluate` at the step-3 reference with the new size, then LM with
pi_c2 free (`Joint-gn-s3`). Judge it on the shared-employer cell (0.10 model vs 0.19 data at s = 1, 2 merged) and on
the same-sector excess (0.126 vs 0.184).

**Step 5 (model features, each one step): Fable items 2 and 5 before item 3.** Ordered by the Q they target:
the smoothing technology (wealth, 57% of Q; illiquid or retirement asset, or the net-worth target of script 77,
which is a PI decision), late-career wage growth (14%), the husbands' non-displacement exit (lets the three excluded
SIPP `_nosep` and `psid_hemp` moments back in), then displacement scarring (d_h, re-employment losses). Annual EITC
accounting (item 3) changes the budget and the state space, so it comes after these.

**Step 6: the independent-shock model and CMA-ES**, from the preferred step-5 specification: `Joint-gn-indep`
(`--fix pi_c0=0 pi_c1=0 pi_c2=0 m_H=1`), Joint-noise, then three CMA-ES seeds (INTAKE section 3 commands, with the
paths of `~/jointloss`).

**Block-balanced weights: a robustness run, not the main specification.** Only after step 1(a). Section 3 shows the
inverse-variance weights already let every block pin its own parameters, and that the blocks Fable wants to up-weight
carry little information. This departs from Fable's item 1 and is the PI's decision.

## 4b. Progress (2026-10-20)

PI approved the order 0-6, the step-1 code, F fixed at 0.101 and the open items of HANDOVER section 2 for step 5.

- Step 0: done by the PI. `~/jointloss` cloned with its own deploy key; Joint-test 11875253 queued (snapshot from before
  steps 1-2, so its check uses the old EXPECTED_Q 11,733.7).
- Step 1: done (commit fcf5356). Scale-free block weights, z-unit weight shares, an information table in the Jacobian
  report, decorrelation hooks `decorr` = indep / mean and scenarios i_indep / i_mean. Tests 14/14 pass (new test 13:
  marginal hazards preserved exactly; simulated rates within 1%, same-month joint losses 33 -> 4); Q at the analytic
  start unchanged.
- Step 2: inputs and baseline done. Clean-spec BPS at the LM estimate (`bps_trim_20261020_120418`): him transitory
  0.0227, her 0.0073, permanent 0.0253 / 0.0318, covariance 0.0027. Applied (`bps_check.py --apply-from`):
  sig_nu_h 0.166 -> 0.180, sig_nu_w 0.112 -> 0.133, p_eps_w and p_eps_h x1.20, p_c x0.99. New baseline: Q 11,866.0 at
  the analytic start (EXPECTED_Q), 1,692.5 at the LM estimate (was 1,359.6). The rise is wealth (775 -> 1,103): more
  transitory risk means more precautionary saving, so even fewer couples hold liquid wealth <= 0 (45-59: 0.167 model vs
  0.381 data). Joint-test 11875253 reproduced Q 11,733.6 on the old inputs (new clone and .venv fine). Joint-gn-bps
  11876676 submitted 2026-10-20 ~13:30 from the LM estimate 11865967 (a first submission, 11876602, had a broken
  --start and was cancelled). Its warm-up Q should be 1,692.5. Its best.json starts step 3.
- Still open from INTAKE 2b: fix the harness's measurement-error layer before any Table 3 number is reported again.

## 5. PI decisions this note needs

1. Approve the step order (0 -> 6) and the move of block-balanced weights from the main specification to robustness.
2. Approve the step-1 code changes (block-weight fix, diagnostics, counterfactual hooks (i-a) / (i-b)).
3. The value at which F is fixed (proposed: the analytic start 0.101, or 0 to drop it).
4. Still open from HANDOVER section 2: the wealth target (script 77, net worth without home and vehicles), separated
   wives' inputs (76), the exit feature for established wives (75), `--her-sep`.
