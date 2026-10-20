# The BPS deficit in his transitory variance: harness artefact, not the model (WP1, 2026-10-20)

**Question.** BPS's estimator on the simulated panel returns sigma2_u1 = 0.006 (K = 1) / 0.013 (K = 3) against the
model input sig_nu_h^2 = 0.0275 (`bps_20261019_133727`, `_134505`). INTAKE 2b (PI-approved) would therefore raise
sig_nu_h from 0.166 to 0.20-0.22. Is the deficit real, or does it come from the harness?

**Answer.** Mostly the harness. About 0.018 of the deficit comes from the measurement-error layer: BPS's correction
subtracts more wage error than the harness put into the husband's wage. A further 0.005 is a genuine feature of
BPS's estimator on a wage with discrete human capital steps: annual averaging of steps that fall within the year
(0.003), plus BPS's trims (0.002). This part is the same for the wife. The jump trim is a minor factor (0.002).

## Mechanism 1: the measurement-error layer cannot give him the wage error BPS subtract

`sim_panel_writer.add_measurement_error` draws classical errors in log earnings and log hours with Bound et al.'s
shares of the measured variance: 4% of the earnings variance, 23% of the hours variance and 13% of the wage
variance. The covariance is set to cov(e_y, e_h) = (E_y + E_h - E_w)/2 and is clipped to keep the matrix positive
semi-definite. BPS's `variance_estimation.do` then subtracts s_me_w = 0.13 x var(measured log wage) in the moment
E(dw_t dw_{t-2}) = -s_u1 - s_me_w.

In the model, the husband's log hours barely vary (variance 0.028, against 0.150 for the wife), while his log wage
varies a lot. The wage-error target, E_w = 0.083, exceeds the most the two errors can give,
(sqrt E_y + sqrt E_h)^2 = 0.065. The covariance is clipped in all 5 age groups, and the drawn wage error is 0.018
short of what BPS subtract. The wife is never clipped, because her hours vary between part time and full time.
This is why only *his* variance is low, and why it is low by about 0.018.

## Mechanism 2: the human capital steps (a real property of BPS's estimator, the same for both spouses)

A level step of psi = 0.49 log points in month m of an observed income year splits across two biennial
differences. This adds +move rate x psi^2 / 6 to E(dw_t dw_{t-2}), i.e. it looks like negative transitory variance.
The exact split of the simulated husbands' annual log wage (no errors, no trims, no residual regressions; K = 3;
50,154 pairs) is:

| -E(dw_t dw_{t-2}) | total | transitory part | human capital part | cross |
|---|---|---|---|---|
| husband (input 0.0275) | 0.0244 (0.0004) | 0.0276 | -0.0032 | -0.0001 |
| wife (input 0.0125) | 0.0083 (0.0004) | 0.0125 | -0.0040 | -0.0002 |

The transitory draw is aligned with calendar years (m_off mod 12 = 0 for 100% of couples), so it passes through
intact.

## Table: BPS Table 3 (all ages, T4C41) on the model panel, K = 3, analytic start

Panel = 115,698 head-waves (26,442 couple-copies). GMM s.e. in parentheses. Stars and p-values test the estimate
against the input (sigma2_u1 0.0275, sigma2_u2 0.0125). *** p<0.01, ** p<0.05, * p<0.1.

| spec | errors in data | BPS ME correction | jump / min-wage trim | s_u1 (his transitory) | s_u2 (her transitory) | s_v1 | s_v2 | c_u1u2 | N jump-trimmed (of which displaced) |
|---|---|---|---|---|---|---|---|---|---|
| A (= bps_check) | Bound + gross 1% x 0.7 | on | on / on | 0.0131*** (0.0013) p=0.000 | 0.0137 (0.0013) p=0.357 | 0.0277 | 0.0354 | 0.0046 | 485 (164) |
| B | Bound + gross | on | off / on | 0.0204*** (0.0015) p=0.000 | 0.0196*** (0.0015) p=0.000 | 0.0252 | 0.0331 | 0.0050 | 0 |
| C | Bound + gross | on | off / off | 0.0177*** (0.0016) p=0.000 | 0.0153* (0.0015) p=0.061 | 0.0261 | 0.0345 | 0.0054 | 0 |
| D | Bound only | on | on / on | 0.0064*** (0.0012) p=0.000 | 0.0077*** (0.0012) p=0.000 | 0.0274 | 0.0353 | 0.0039 | 509 (193) |
| E | Bound only | on | off / on | 0.0118*** (0.0013) p=0.000 | 0.0124 (0.0013) p=0.912 | 0.0250 | 0.0331 | 0.0045 | 0 |
| **F (clean)** | none | off | on / on | **0.0226*** (0.0005) p=0.000** | **0.0070*** (0.0004) p=0.000** | 0.0268 | 0.0347 | 0.0052 | 510 (242) |
| G | none | off | off / on | 0.0244*** (0.0005) p=0.000 | 0.0085*** (0.0004) p=0.000 | 0.0262 | 0.0343 | 0.0057 | 0 |
| H | none | off | off / off | 0.0243*** (0.0005) p=0.000 | 0.0083*** (0.0004) p=0.000 | 0.0266 | 0.0347 | 0.0056 | 0 |
| N (sig_nu = 0) | none | off | on / on | -0.0040*** (0.0002) | -0.0049*** (0.0003) | 0.0262 | 0.0345 | -0.0003 | 528 (242) |
| O (sig_nu = 0) | none | off | off / off | -0.0031*** (0.0002) | -0.0040*** (0.0003) | 0.0263 | 0.0346 | -0.0002 | 0 |

(N and O are tested against 0 for the transitory variances; their stars refer to that.)

Reading:
- H reproduces the exact decomposition (0.0243 vs 0.0244): BPS's residual regressions and sample rules do not
  matter.
- F - N = 0.0266 (his) and 0.0119 (hers): the input transitory variance passes through at 0.97 / 0.95. The clean
  deficit is an *additive* offset (-0.004 / -0.005) that does not depend on sig_nu. The additive form of the
  bps_check rule is therefore right.
- The jump trim costs 0.002 on clean data (F vs G). On the error panels it costs 0.005-0.007 (A vs B, D vs E),
  because it then removes genuine reversals.
- A sits 0.009 below F only because two biases roughly offset: the clipped wage error pulls down by 0.018, and the
  gross errors push up by about 0.007 (A vs D). The wife's "good" 0.0137 in A is the same accident: gross errors
  (+0.006) offset the step bias (-0.005).

## Smoke DGP with the model's wage process (`smoke_sim_dgp_steps.py`, 10,000 couples, known truth)

The smoke DGP keeps smoke_sim_dgp.py's couples, hours, spells and consumption. The wage is
transitory (one draw per calendar year, 0.0275 / 0.0125, cov 0.0058) + monthly steps of 0.49 / 0.46 log points at
the model's analytic rates (accumulation, innovation, shared innovation, displacement loss d, depreciation pi_dn).
Moves per year: 0.126 (him) and 0.201 (her). Time-aggregation benchmark: s_u1 0.0223, s_u2 0.0055. 'flat' = his
hours 2080 a year when working (log-hours variance 0.010, against 0.052 for the smoke's own hours).

| spec | s_u1 (truth 0.0275) | s_u2 (truth 0.0125) | ME shortfall, his wage |
|---|---|---|---|
| S2 none, no correction, no trims | 0.0214*** (0.0007) p=0.000 | 0.0069*** (0.0007) p=0.000 | - |
| S1 none, no correction, BPS trims | 0.0196*** (0.0007) p=0.000 | 0.0054*** (0.0007) p=0.000 | - |
| S3 Bound, shipped | 0.0105*** (0.0018) p=0.000 | 0.0061*** (0.0022) p=0.003 | 0.004 |
| S4 Bound + gross, shipped | 0.0173*** (0.0019) p=0.000 | 0.0129 (0.0024) p=0.855 | 0.004 |
| S6 flat, none, no correction, BPS trims | 0.0197*** (0.0007) p=0.000 | 0.0054*** (0.0007) p=0.000 | - |
| S5 flat, Bound, shipped | -0.0196*** (0.0012) p=0.000 | 0.0061*** (0.0022) p=0.003 | 0.041 |

S2 recovers the time-aggregation benchmark (0.0214 vs 0.0223). Flat hours alone change nothing (S6 = S1). Flat
hours combined with the error layer drive s_u1 negative (S5): the clipping mechanism, reproduced on a known DGP.

## Recommendation: change the INTAKE 2b correction, do not apply it as approved

1. **Do not apply 0.166 -> 0.20-0.22.** That step corrects the harness's error layer, not the model. Applied as is,
   it would raise his true transitory variance by 52-77% (0.0275 -> 0.042-0.049). It would also *lower* hers
   (sigma_nu_w 0.112 -> 0.106, because the gross-error accident makes her look recovered).
2. **Do apply the correction, computed on the clean spec F.** The data carry no measurement error and BPS's
   correction is off. That is what BPS's estimator returns when its error correction is exact, so it is the
   like-for-like comparison with BPS's PSID numbers. The deficit that remains is BPS's own estimator meeting a
   step process (the PSID's within-year raises and job changes face the same averaging). The same rule
   sigma^2 = 2 s2(BPS) - hat gives, at the analytic start:
   **sig_nu_h 0.166 -> 0.180** (sig_nu_h^2 0.0275 -> 0.0324) and **sig_nu_w 0.112 -> 0.134** (0.0125 -> 0.0180).
   The permanent rescaling gives p_eps_h x 1.13 (0.00407 -> 0.00460), p_eps_w x 1.10 (0.00905 -> 0.00996) and
   p_c x 1.13 (0.00099 -> 0.00112).
3. At intake, rerun spec F at the gn estimate (`bps_trim_test.py --start <gn> --K 3 --only F_none_shipped`, about
   8 min). Apply the rule to its numbers. This needs a `--clean` option in `bps_check.py --apply`, or a hand-entered
   wage_process.json from F, coded only after the CMA-ES stage has started (Section 0 freeze). The error layer
   should be fixed before it is used again for any Table 3 number: draw his wage error at the target (relax the
   23% hours share), or report Table 3 from the clean spec.

**Paragraph for INTAKE 2b (replaces step 2).** WP1 (`results/bps_deficit_20261020.md`) shows that 0.018 of the
0.015-0.021 deficit is the harness. The husband's model hours vary too little for the Bound et al. error shares, so
the drawn wage error is clipped 0.018 below the 13% that BPS's correction subtracts. On the clean spec (no errors
in the data, BPS's correction off, BPS's trims on), BPS recover 0.0226 for him and 0.0070 for her, against inputs
of 0.0275 / 0.0125. The remaining offset (-0.005 for both spouses) is annual averaging of the discrete human
capital steps, plus the trims. Decision rule: apply bps_check's rule to the clean-spec numbers at the estimate
(sig_nu_h about 0.18, sig_nu_w about 0.13 at the start values), not to the shipped-spec numbers.

**Appendix D sentence (paper).** BPS's estimator understates the transitory variance on a wage process with
discrete human capital steps. A step taken within an income year is split across two biennial wage growths and
shows up as a positive autocovariance: in our simulated panel this removes 0.003-0.004 of each spouse's transitory
variance, and BPS's trims remove a further 0.001-0.002. We therefore set the model's transitory variances so that
BPS's estimator on the simulated data, with its measurement-error correction exact, returns BPS's published
0.0275 and 0.0125.

Files: `paperA_model/bps_trim_test.py`, `bps_reconciliation/code/{bps_on_sim_me.do, ovr_me0.do,
smoke_sim_dgp_steps.py}`; numbers in `results/bps_trim_20261020_010756/{bps_trim.json, smoke_steps_results.json}`;
panels in `%TEMP%/paperA_bps_wp1*` (not in the repo). No model-path file, input or target was touched; no `--apply`.
