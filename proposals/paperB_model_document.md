# Paper B model document: careers, schooling and the age profile of persistence (pre-code specification, 2026-10-18)

The specification Paper B's Section 7 describes, written in the order the simulator will run, so that the code can be
built from it and checked against it. It follows Fable's round-2 review (`fable_review_paperB.md`, Section 4) and the
within-job tests of `45.WithinCellIdentification.py`. No results. Every modelling choice is stated with the evidence that
motivates it (PSID-motivated choices also get a paper footnote with the number and the script).

## 1. Population and exogenous inputs

- A son is born into a family with log parental income `x` (13-19 mean, the PSID measure) and race `r` in {Black, White}.
  The joint distribution of (x, r) is the PSID's (sons of the benchmark sample, by race; empirical draws, not a
  parametric form).
- One-year parental income `x1 = x + u`, with `u` drawn so that the reliability ratio of `x1` equals the PSID's (W 0.585,
  B 0.565). Used only to compute the one-year moments exactly as in the data.
- Schooling `e = e(x, r) + nu_e`: years of completed schooling, drawn from the PSID conditional distribution of schooling
  given x and race (linear in x by race plus an empirical residual). Exogenous; the counterfactual "equalising schooling"
  is a shift of this distribution, not a priced policy. Motivation: no schooling choice fits in four months, and the
  paper's mechanism is after school.
- Initial human capital level `h0 = b0 + b1(r) * e + nu_0`, `nu_0 ~ N(0, s0^2)`. `b1(r)` is optional (model D): Black
  sons' return to schooling at 25-29 exceeds White sons' by 0.061*** within the early job (PSID, earnings), not in the
  NLSY79 (0.008).
- Career starts at the end of schooling (age 18 + max(e - 12, 0)), runs annually to 55: about 30 periods.

## 2. Within-period order (simulator order)

For each son and year t (age a):

1. **Offer.** If employed in job type j: with probability `lambda_j` an outside offer arrives. If not employed: with
   probability `lambda_u`. At career start: an offer with probability 1.
2. **Offer type.** An offer is of type G with probability
   `p(x, e, r) = logistic(a0 + a1 * x + a2 * e + a3 * 1[Black])`, otherwise O. Same function at entry, out of work and on
   the job. No race x x term (the racial difference in the parental-income gradient of access is -0.022 (0.024) once
   schooling and the father's job are held fixed; `35`, D3).
3. **Match draw.** An offer carries a match component `m' ~ N(mu_m(j'), s_m^2)`.
4. **Move decision.** Accept if the offered log wage exceeds the current one (employed) or always (not employed).
   Myopic acceptance in the baseline (no forward-looking valuation of job type); the sensitivity check values G offers
   at the present value of faster accumulation.
5. **Displacement.** An employed son is displaced with probability `delta_r(x) = delta0_r + delta1 * x` (slope common:
   -0.037*** W, -0.038*** B; `42` C). Displaced: loses m, not employed next period.
6. **Human capital.** Employed in j: `h' = h + (gamma_j + gamma1(r) * e) * acc(a) + eta`, `acc(a)` declining in age
   (two parameters: level normalised to gamma, decline rate `rho_a`). Not employed: `h' = (1 - kappa) * h + eta`.
   `eta ~ N(0, s_eta^2)`.
7. **Wage.** `ln w = mu_r + h + m + eps`, `eps ~ N(0, s_eps^2)` transitory (measurement and transitory shocks).
   Annual earnings = w x hours, hours not modelled (the son's hours carry ~0 of the IGE); earnings = wage when employed
   the whole year; a displacement year uses a fraction of the year employed drawn from the PSID distribution.

## 3. Parameters

| Block | Parameters | Count | Race-specific |
|---|---|---|---|
| Level | mu_r | 1 (Black - White) | yes |
| Initial human capital | b0, b1, (b1_Black - b1_White), s0 | 3 (+1 in D) | D only |
| Access | a0, a1, a2, a3 | 4 | a3 (models B-D) |
| Search frictions | lambda_G, lambda_O, lambda_u | 3 | no |
| Matches | mu_m(G) - mu_m(O), s_m | 2 | no |
| Displacement | delta0_B, delta0_W, delta1 | 3 | delta0 |
| Accumulation | gamma_G, gamma_O, gamma1, (gamma1_Black - gamma1_White), rho_a | 4 (+1 in C) | C-D |
| Depreciation | kappa | 1 | no |
| Shocks | s_eta, s_eps | 2 | no |

Not in the model, with the reason: early-career transfer (no moment identifies it; parental labor income reproduces the
earnings opening, 0.134***); race-specific search friction (move rates 0.125 B vs 0.130 W at 25-34; added only if the
move moments fail, as Bowlus-Eckstein 2002); parental income in accumulation (post-schooling gradient 0.008, p=0.17
PSID; 0.002, p=0.73 NLSY79); accumulation on AFQT (AFQT return rise equal by race, -0.031 (0.025), `45` A4).

## 4. Nested models (parsimony rule)

- A: race in mu_r, delta0_r, e(x, r).
- B: A + a3 (race in access).
- C: B + gamma1 race difference (within-job evidence: 0.061*** PSID earnings within early cell; 0.017*-0.021** NLSY79).
- D: C + b1 race difference.
Each estimated by one joint SMM run (all endogenous parameters, no hand tuning). A parameter is kept only if the next
model improves the fit to its own moments. Before the first HPC run: sensitivity (Jacobian) matrix at a calibrated start;
drop collinear columns.

## 5. Simulated observation scheme (computed with the same code as the data)

- Interview years: annual to 1997, biennial after (cohort-specific, matched to the PSID's birth-year distribution).
- Wage = annual earnings / hours of the previous calendar year (with hours fixed, the PSID's division structure is kept by
  adding the PSID's hours measurement error to the simulated hours).
- Same-employer pair: two interviews 1-2 years apart with no move or displacement between them (Table 9 definition).
- Job type observed as in Table 8 (G = top quartile of men's employment by CPS level AND later growth); the early job =
  modal type at 25-34.
- Parental income: 13-19 mean and one year.
- Attrition: none in the baseline; the IPW-weighted PSID moments are the targets' robustness version.

## 6. Targets (about 60) and validation

Targets, by race unless stated:
1. Log IGE of earnings by age band 25-29 ... 50-55 (Table 1) and its opening (Table 2), on the 13-19 mean; the one-year
   version (Table 3, PSID column).
2. Rank-rank slope and expected rank at parental p25 by band (App. Table rank_age).
3. Return to schooling by age band, and its rise, within early job (Tables 10-11).
4. Schooling gradient in parental income (calibration of e(x, r), checked).
5. Share of sons in G at 25-34 by parental-income tercile; G access on x, e, race (Table 8 col. 5).
6. Early-job share of the rise of persistence and of the racial divergence (Table 7, G/O version recomputed in the data).
7. Same-employer annual wage growth at 25-34 and 35-55 and its gradient in parental income (Table 9 col. 1).
8. Rates of staying, moving and displacement at 25-34 and 35-55; growth at a move and its gradient in parental income;
   wage loss after displacement (Table 11; App. Table career_displacement).
9. Variance of log earnings by age band (within cohort, by race; `41` B(iv)).

Validation (not targeted): same-employer growth by schooling and race (not established within cells, `45`); the NLSY79,
NLSY97 and NLSY79-children age profiles; the between/within-occupation split (Table 6).

## 7. Counterfactuals (log IGE and rank intercept gap at 30 and 45, by race; mu_r fixed)

1. Equalising schooling (Black e distribution = White at the same x).
2. Equal access (a3 = 0).
3. Equal pay-off of schooling in accumulation (gamma1 equal) - only if model C is selected.
4. Insurance against job loss (kappa and match loss halved).

## 8. Code plan (to be built under the HPC rules: 32 cores, --threads 2, job names, email flags, git-archive snapshot)

| Step | File | Content |
|---|---|---|
| 1 | `model/inputs.py` | PSID draws of (x, r, e), observation calendar, CPS G/O cell list, reliability noise |
| 2 | `model/simulate.py` | the within-period order of Section 2, vectorised over sons, common random numbers |
| 3 | `model/moments.py` | one moment function applied to the PSID panel and to the simulated panel |
| 4 | `model/jacobian.py` | numerical sensitivity matrix at the calibrated start |
| 5 | `model/smm.py` | joint SMM, diagonal weights (inverse bootstrap variances), nested models A-D |
| 6 | `model/counterfactuals.py` | Section 7 experiments, tables for the paper |
