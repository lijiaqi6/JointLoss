# WP10: local model evaluations (2026-10-20, WP0 declined)

All evaluations are at the analytic start, size k_s2_era1_a20, K = 3, CRN seed 20261018 (same draws in every
evaluation, noise floor of Q about 30), 14 threads. No model-path file was touched.

## (a) Profile of the tenure-exit moments in the work-cost parameters (89-moment set, `--ext-targets new_job her_sep`)

`estimate.py evaluate --ext-targets new_job her_sep [--fix ...]`. theta_05 is -0.0014 at the start, so x0.5 / x2
is a null change. Two additive moves of +-0.06 (about phi_F's +-20%) were added to make the profile informative.

| evaluation | Q (89) | her exit, tenure 0-5 | 6-11 | **12+** | CPS persistent exit | PSID wife emp., youngest 0-5 | youngest 6-17 | folder |
|---|---|---|---|---|---|---|---|---|
| data (s.e.) | | 0.0206 (0.0007) | 0.0160 (0.0007) | **0.0068 (0.0001)** | 0.0101 (0.0001) | | | |
| start | 13,232.5 | 0.0354 | 0.0096 | **0.0027** | 0.0014 | 0.962 | 0.950 | evaluate_20261020_011116_p26952 |
| phi_F x 0.8 (0.246) | 16,759.9 | 0.0276 | 0.0079 | **0.0025** | 0.0010 | 0.975 | 0.966 | evaluate_20261020_011235_p27532 |
| phi_F x 1.2 (0.369) | 12,094.0 | 0.0409 | 0.0109 | **0.0029** | 0.0017 | 0.950 | 0.939 | evaluate_20261020_011355_p9316 |
| theta_05 x 0.5 | 13,224.2 | 0.0354 | 0.0096 | **0.0027** | 0.0014 | 0.961 | 0.950 | evaluate_20261020_011516_p14308 |
| theta_05 x 2 | 13,231.4 | 0.0353 | 0.0097 | **0.0027** | 0.0014 | 0.962 | 0.950 | evaluate_20261020_011643_p25656 |
| theta_05 = +0.06 | 12,830.8 | 0.0335 | 0.0085 | **0.0027** | 0.0014 | 0.938 | 0.945 | evaluate_20261020_011803_p6236 |
| theta_05 = -0.06 | 13,667.7 | 0.0330 | 0.0085 | **0.0027** | 0.0013 | 0.979 | 0.954 | evaluate_20261020_011921_p31196 |

Reading: **the 12+ exit rate is structurally pinned.**
- A +-20% change in the cost of full-time work moves the 0-5-month exit rate by +-0.006 (+-17%) and the employment
  of mothers by about 1.2 points. It moves the 12+ rate by only +-0.0002 (0.0025-0.0029), which is 13-14 data s.e.
  but a fraction of the 0.0041 gap.
- The child-related disutility of labor (theta_05) moves the employment of mothers of young children by 4 points
  and leaves the 12+ rate at 0.0027 in every case.
- So the work-cost parameters act on new matches and early exits, not on wives established in a job. Closing the
  12+ gap at intake needs a feature that reaches established wives: the birth jump or a type. WP2's residual
  decides between them, as the plan says. Re-estimating the preferences alone will not do it.

## (b) Separated wives' employment in the model vs the PSID (WP3, `output/separated_mothers.md`)

`sep_state_sim.py` (new), one simulation at the start, `results/sep_state_20261020_012047_p16664/`. The model has no
child support and no remarriage. Employment there is the monthly share of wife-months with positive hours, wives
25-59. The PSID rate is the annual share with hours > 0 (an annual rate is higher than a monthly one for the same
women).

| | model, separated | model, married | model step | PSID single mothers k = 1-5 (annual) | PSID married mothers | PSID step |
|---|---|---|---|---|---|---|
| all / pooled | 0.978 | 0.916 | +0.062 | 0.85-0.91 | 0.79-0.80 | +0.100*** (0.009; p<0.001); within mother +0.084*** (0.010; p<0.001) |
| youngest 0-5 / 6-17 | 0.976 / 0.977 | 0.915 / 0.914 | +0.06 | | | |
| Black | 0.978 | 0.948 | +0.030 | 0.85 | 0.797 | +0.052*** (0.016; p=0.001); within +0.035** (0.014; p=0.016) |
| White | 0.979 | 0.903 | +0.076 | 0.89 | 0.787 | +0.135*** (0.010; p<0.001); within +0.118*** (0.014; p<0.001) |
| by time since separation | 0-11 months 0.953; 12-35 months 0.978; 36+ months 0.980; 12 months before 0.919 | | | | | |

Reading:
- The model gets the sign of the step at separation and the race ordering right (larger for White women).
- Both levels are about 10 points too high. This is the married wives' employment problem at the start values
  (0.92 vs 0.81), not a separate one.
- The separated level sits at a ceiling (0.98), so the step cannot reach the PSID's +0.10 / +0.135 (White) without
  the married level coming down first.
- Child support would lower the separated wife's employment; the model has none and is still at 0.98. This
  supports the plan's position that child support is not needed as a model feature before the married level is
  fixed at the estimate.
- Re-read at the gn estimate before any footnote is written.

## (c) Counterfactual smoke: `counterfactuals.py --scenarios base ii_ui12 --size k_s2_era1_a20`

`results/counterfactuals_20261020_012051_p32416/` (1.8 min). It runs. Raising the UI expiry from 6 to 12 months
changes the following:
- Consumption in his loss month: -0.0539 -> -0.0529 (all).
- Joint loss month: -0.153 -> -0.150; 12 months after: -0.131 -> -0.128.
- No-earner share: unchanged (0.00227).
- Consumption-only CE: +0.073% (Black +0.089%, White +0.064%).
- Loss counts are identical across scenarios (CRN): 24,930 his losses, 534 joint.
Start values, not estimates: the numbers are for the plumbing only.
