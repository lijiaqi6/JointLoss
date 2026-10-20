# Paper A model: analytic pre-estimation, identification map, targets and build plan (2026-10-18)

Companion to the signed-off model document (`paperA_joint_loss/model_document.tex`, decisions D1-D18) and to the
model section now written into the paper (`paperA_joint_loss/sec7_model.tex`). Read, nothing run: the model
document, Paper A (sec1-sec8, appB-appD), the four memos in this folder, the BPS harness (`bps_reconciliation/HARNESS.md`),
`estimation/smm.py` (CMA-ES engine, `SafePool`, `cmd_jacobian`, `cmd_profile`, recovery), `scripts/hpc_job.py`,
`IGE/12b.UIGenerosity.py` (writes `data/ui_generosity.csv`), and the output files of IGE/19, 25, 30, 37, 38, 39, 40, 50.
Numbers quoted are Paper A's data moments; where a number is an illustration of a formula and not yet computed on the
target's window it is marked "illustrative". Terminology: search friction (never offer rate), human capital level /
accumulation / depreciation.

Four parts: (a) what is set outside the SMM and how, with the algebra and the exact/approximate judgement; (b) the
identification map of the 31 SMM parameters, weak directions, cut list and the Jacobian protocol; (c) the targets with
windows and scripts; (d) the build and estimation plan with tests, pass criteria, compute and stop rules.

---

## 0. Summary

- **Set outside the SMM** (coded mappings, Section 1): 10 fixed-economics inputs; the wage process (levels, steps,
  three innovation probabilities, two transitory variances and their correlation); 3 x (tax, EITC, SNAP, UI cap,
  consumption floor) schedules by era; UI take-up; workplace-match shares; the child process and the number of
  children; the childcare price; initial conditions; the two child-block slope scenarios and the presence slope.
  Of these, the wage-innovation probabilities, the transitory variances and the tax function are approximate mappings
  and get a one-time coded correction through the BPS harness (Section 1.2); everything else is a direct data moment
  or an external schedule.
- **Closed-form start values** exist for 17 of the 31 SMM parameters (all 9 displacement parameters up to one ridge,
  sigma_0 and sigma_J by race, pi_up and pi_dn by spouse, d_j by spouse, lambda_h by race): Section 1.4 gives the
  algebra. They are start values and consistency checks, not calibrations: each depends on the measurement layer
  (CPS "job loser" classification of a displaced wife, the PSID interview-week status, SIPP earnings not wages) or on
  an endogenous object (the wife's acceptance, the husband's non-employment months). The PI's one-run rule stands:
  31 parameters, one SMM run, no hand tuning.
- **Two identification problems to flag now** (Section 2.3): (i) the couple type (p_H, m_H) is a ridge in the monthly
  moments (only Var(m)/E(m)^2 is identified by the leads and lags; the PSID placebo window gives a second reading of
  the same ratio); one over-dispersion moment (husbands displaced two or more times) would break it, and I recommend
  adding it to IGE/60 (PI decision). (ii) A constant lambda_h cannot fit the SIPP re-employment path at 3, 6 and 12
  months (0.586, 0.708, 0.791 imply monthly job finding of 0.26, 0.18, 0.12); the SMM will fit a compromise and the
  miss must be reported; the fallback (one extra job-finding rate after month 3) is listed, not adopted.
- **Compute is the binding risk** (Section 4.6): my arithmetic puts one evaluation (12 problems x 3 eras x 420 months x
  211,680 states) at 5-15 minutes on two threads, not the 20 seconds the model document hopes for; the fallback fallback sequence
  (5 human capital levels; merge s = 1, 2; one era in estimation; 20 asset points; drop the lost-hours record) can bring
  it to about 30-60 seconds. Measure at stage 1 before anything else is decided.

---

## 1. Analytic pre-estimation: parameters set outside the SMM

### 1.1 Fixed economics (external values; exact by construction)

| Parameter | Value | Source / rule | Code |
|---|---|---|---|
| beta | 0.96^(1/12) | D11; same as the lifecycle model | constant |
| gamma | 1.5 | lifecycle model | constant |
| r_m | 1.03^(1/12) - 1 | model document | constant |
| s_M, e(k) | 1.64 (= 1/0.61); McClements child shares by bucket (0-5, 6-17) | lifecycle model | `inputs/scales.json` |
| H(F), H(P) | 173, 87 hours a month | 40 and 20 hours a week x 52/12 | constant |
| sigma_eps | fixed; set at the solver stage to the smallest value for which the DC-EGM upper envelope is smooth at the median state (the practice of Iskhakov et al. 2017); profile of Q reported | solver stage | `inputs/params_fixed.json` |
| kappa_up | 0.5 | model document; profile reported | constant |
| c_min | AFDC/TANF maximum benefit, family of three, era mean in 2000 dollars, equivalised by s_M e(1) | Urban Institute Welfare Rules Database / Green Book | `IGE/61.PolicySchedules.py` (new) |
| retirement | 240 months; Social Security 40% of each spouse's final-level earnings; annuity of a | model document | constant |
| asset split at separation | 1/2 | model document | constant |

### 1.2 The wage process (BPS Table 3; closed forms with one approximate step)

**Levels.** mu_j(r) = PSID mean log hourly wage (2000 dollars) of employed wives / husbands aged 25-29, by race
(couples panel of IGE/25; `IGE/60`). Exact as a definition: it fixes the wage at level h = 4 for an entrant of that age.

**Steps.** psi_j = (q99_j - q01_j) / 6 of the persistent part of the log hourly wage residual at 40-49 (residual from
mu_j(r)), so that the seven levels span the 1st-99th percentiles. The observed cross-sectional range includes the
transitory shock and measurement error, so the range is shrunk before dividing:

    psi_j = (q99 - q01) / 6 x sqrt( (Var_total - sigma_nu,j^2 - s_me,j Var_total) / Var_total ),

with s_me,j the Bound et al. (1994) share of the wage log variance (13%) and sigma_nu,j^2 the transitory variance of
the next paragraph. Approximate (a Gaussian-shrinkage rule on quantiles); the BPS harness checks the result through the
age profile of the cross-sectional variance (BPS Table 3 by age group).

**Persistent innovations.** The three steps of the human capital block move h_j by one level with probabilities
pi_up (at work), pi_dn (out of work), d_j (at displacement), p^c (shared innovation, +-1 equally likely) and p^eps_j
(idiosyncratic). Without truncation, the annual variance and covariance of the +-1 innovations are

    Var_perm,j = 12 psi_j^2 (p^c + p^eps_j),      Cov_perm = 12 psi_w psi_h p^c,

so, from BPS Table 3 (all ages: Var 0.0303 husbands, 0.0382 wives, Cov 0.0027),

    p^c      = 0.0027 / (12 psi_w psi_h),
    p^eps_j  = Var_perm,j / (12 psi_j^2) - p^c - pi_up,j (1 - pi_up,j) x 1{employed share}   (see below).

Feasibility: p^c <= min_j Var_perm,j / (12 psi_j^2) holds by a wide margin (correlation 0.08). Illustrative: with
psi = 0.40 for both spouses, 12 psi^2 = 1.92, p^c = 0.0027 / 1.92 = 0.0014 a month, p^c + p^eps_h = 0.0303 / 1.92 =
0.0158, p^c + p^eps_w = 0.0199.

Two reasons the mapping is approximate, and the coded correction:

1. *Stochastic accumulation is itself a permanent innovation.* At work h rises with probability pi_up, a Bernoulli
   step with monthly variance pi_up (1 - pi_up) psi^2 around its mean; BPS's first-stage regression removes the mean
   age profile but not this idiosyncratic part, so BPS's Var_perm already contains it. The closed form therefore
   subtracts pi_up,j (1 - pi_up,j) (at the start value of pi_up from Section 1.4) for the months at work. Likewise the
   displacement loss d_j of workers re-employed within the year is in BPS's permanent variance (their no-work rule
   drops zero-hours years only).
2. *Grid truncation* at levels 1 and 7 lowers the realised variance at the ends of the grid.

   **Coded correction (once, before the SMM, D6/D7):** simulate the model at the analytic start values with
   (p^c, p^eps, sigma_nu, rho_nu) at the closed forms above; write the BPS-shaped panel with the measurement-error
   mixture (`bps_reconciliation/code/sim_panel_writer.py`); run BPS's estimator (`bps_on_sim.do`); read back
   the six Table 3 numbers (hat Var_perm,j, hat Cov_perm, hat Var_trans,j, hat Cov_trans). Then set

       sigma_nu,j^2 (new) = max{ 0.5 sigma_nu,j^2(BPS),  2 sigma_nu,j^2(BPS) - hat Var_trans,j },
       p^eps_j (new)      = p^eps_j x Var_perm,j(BPS) / hat Var_perm,j     (same ratio rule for p^c with the covariance),

   i.e. remove the part of the transitory variance that the estimator attributes to the model's other within-year
   sources (displacement, human capital moves inside a year, the mixture), and rescale the permanent probabilities by
   the ratio of target to recovered variance. One pass (the model document says once); the result is a fixed input
   with its derivation recorded in `inputs/wage_process.json`. The floor at half of BPS's value guards against the
   trim fragility documented in HARNESS.md Section 6.2 (BPS's transitory variances move by +-20% with the trims).

**Transitory shocks.** Two points +-sigma_nu,j per spouse, held for the calendar year; pair probabilities
(1 + rho)/4 for equal signs, (1 - rho)/4 for opposite signs, so Var = sigma^2 and Corr = rho exactly. Start values:
sigma_nu,h^2 = 0.0275, sigma_nu,w^2 = 0.0125 (BPS, already net of measurement error), rho_nu = 0.31; then the one-time
reduction above. A separated wife keeps her own component (marginal unchanged).

### 1.3 Policy schedules by era (external tables; era = 1984-96, 1997-2008, 2009-21; 2022-23 with the last)

All in 2000 dollars; for each era the parameter is the mean over the era's calendar years of the deflated statutory
value (CPI-U-RS), so that a stationary schedule per era is a coded average, not a chosen year. New script
`IGE/61.PolicySchedules.py` writes `paperA_model/inputs/schedules_<era>.json` and a check table
(`output/policy_schedules.md`: each parameter by year and the era mean). `IGE/12a.PolicyCalendar.py` (a state x year
calendar of leave and related policies, 1980-2024) is read first for anything reusable (download cache, deflators);
nothing in it is changed.

| Object | Mapping | Source | Exact / approximate |
|---|---|---|---|
| Tax (chi_e, mu_e) | OLS of ln(Y^a - T(Y^a)) on ln Y^a over a grid of Y^a from $5,000 to $300,000 (2000 dollars), married filing jointly, two children, wage income only, federal income tax + employee payroll tax (no EITC, no credits other than the child tax credit from 1998), for each year of the era, then the era mean of the fitted (chi, mu). T from NBER TAXSIM (taxsim35, `taxsim` Python package or the web API; CENSUS/IPUMS keys not needed). | NBER TAXSIM | approximate (BPS's log-linear form; annualised current monthly income in place of annual income; one family size) |
| EITC (eps_in, E_bar, eps_out, Y_out) by n in {0,1,2,3+} | statutory parameters by year, married filers (phase-out start with the marriage-penalty relief from 2002), deflated, era mean | IRS Rev. Proc. tables; Tax Policy Center "EITC parameters 1975-present" | exact within an era up to the era averaging (era 1 spans the 1993 expansion: the era mean understates the 1994-96 credit and overstates 1984-93; reported) |
| SNAP A_e(n_hh), D_e(n_hh), gross-income test 130% of poverty, asset limit | USDA FNS maximum allotments and standard deduction by fiscal year and household size (48 states); HHS poverty guidelines by year and size; asset limit $2,000 (nominal) deflated; era means | USDA FNS COLA tables; HHS | exact up to era averaging; the 20% earned-income deduction and 30% benefit reduction are statutory constants |
| UI cap b_bar_e | mean over states (weighted by the CPS couples' state distribution, 1994-2023) of max_wba_2000 x 52/12, era mean | `data/ui_generosity.csv` (`IGE/12b.UIGenerosity.py`), column `max_wba_2000` | exact as a national mean; approximate in that the model has no state |
| UI replacement rho_UI | 0.5 | statute (about half of the weekly wage up to the cap) | exact |
| UI expiry | 1/6 a month | D-geometric (Bacher et al.); 26 weeks | approximate by design (the model document's footnote) |
| UI take-up q_UI | share of displaced husbands who received UI: 0.523 (DWS, displaced husbands with a known year, mean when the wife is not displaced; `output/cps_dws_joint_loss.md`, Section 7) | `IGE/39.CPSDisplacedWorkers.py` (add the wife's share; if the two differ by more than 10 points, q_UI by spouse: PI decision) | approximate (receipt by the survey date, any time since the displacement) |
| c_min | AFDC/TANF maximum, family of three, era mean | as in 1.1 | exact |

### 1.4 Displacement risk: the algebra, what it pins exactly, and why the parameters stay in the SMM

Notation (month, both spouses employed at the start, type tau, match s): pi_c = pi_c(s), delta_j = delta_j(r),
m_L = 1, m_H > 1, P(tau = H) = p_H, E m = 1 + p_H (m_H - 1), Var m = p_H (1 - p_H)(m_H - 1)^2,
kappa = E[m^2] / (E m)^2 = 1 + Var m / (E m)^2.

**Joint and marginal probabilities, given (tau, s):**

    P(both)         = pi_c + (1 - pi_c) m^2 delta_w delta_h
    P(w only)       = (1 - pi_c) m delta_w (1 - m delta_h)
    P(h only)       = (1 - pi_c) m delta_h (1 - m delta_w)
    P(h lost)       = pi_c + (1 - pi_c) m delta_h
    P(w | h kept)   = m delta_w                                      (exact: the common shock drops out)
    P(w | h lost)   = [pi_c + (1 - pi_c) m^2 delta_w delta_h] / [pi_c + (1 - pi_c) m delta_h]

**Averaging over the unobserved type.** Given he kept his job the type weights are p_tau (1 - m_tau delta_h) /
sum(.), equal to p_tau up to O(delta_h (m_H - 1)) (a relative error below 2% for delta_h ~ 0.004, m_H ~ 5), so

    (A)  b_w := P(w lost | h kept)  =  (E m) delta_w            [CPS target: 0.0023 pooled, non-temporary; by race to compute]
    (B)  P(w lost | h lost, s)      =  [pi_c(s) + (1 - pi_c(s)) kappa b_w B] / [pi_c(s) + (1 - pi_c(s)) B],   B := (E m) delta_h
    (C)  b_h(s) := P(h lost | s)    =  pi_c(s) + (1 - pi_c(s)) B

**Leads and lags (the flat elevation).** In month 0 +- k (k = 1, 2, 3) her hazard is pi_c + (1 - pi_c) m delta_w
whether or not he still has a job (the common shock hits every employed spouse), so her excess relative to couples in
which he kept his job in month 0 is

    L = (1 - pi_c) delta_w (m_H - 1) [P(H | h lost at 0) - P(H | h kept at 0)]
      = delta_w (m_H - 1) p_H (1 - p_H)(m_H - 1) / (E m)  x  (1 - pi_c) B / (pi_c + (1 - pi_c) B)
      ~ delta_w Var m / (E m)                                                  (pi_c << B, i.e. outside the shared-employer cell)

so that

    (D)  L / b_w  =  Var m / (E m)^2  =  kappa - 1.

(D) is the one monthly moment that sees the couple type, and it sees only the squared coefficient of variation of the
multiplier. The PSID placebo-window excess measures the same ratio on annual windows (Section 2.3). Hence the ridge:
(p_H, m_H) move together along p_H (1 - p_H)(m_H - 1)^2 = (kappa - 1)(1 + p_H (m_H - 1))^2, which has a solution
only for p_H < 1 / kappa.

    kappa - 1 = 1.3 (illustrative, CPS all losses: L ~ 0.0065 on b_w = 0.0054):  p_H = 0.10 -> m_H = 7.1;  0.20 -> 7.6;  0.30 -> 10.8
    kappa - 1 = 0.5 (illustrative, PSID: permanent 0.020 on base 0.039):          p_H = 0.10 -> m_H = 3.3;  0.20 -> 3.7;  0.30 -> 4.7

The two sources do not agree on kappa, which is itself informative (the CPS leads and lags may also carry a common
shock spread over neighbouring months, which the model attributes to the type); the SMM weighs both. What separates
p_H from m_H is over-dispersion of displacement counts within couples: with annual hazards a_tau = 12 m_tau delta_h,
the share of husbands displaced at least twice in N observed years is sum_tau p_tau [1 - (1 - a_tau)^N - N a_tau
(1 - a_tau)^(N-1)], which for given kappa is increasing in m_H. **Recommendation:** add to IGE/60 the share of husbands
with two or more displacements among those observed at least ten years (PSID 1984-2021), by race, with its bootstrap
s.e.; one moment, directly on the ridge (PI decision; not in the signed-off targets).

**Solving for the own hazards and the common shock (closed forms given kappa):**

    delta_w(r) = b_w(r) / (E m)
    B          = (b_h(0) - pi_c(0)) / (1 - pi_c(0))          -> first pass B = b_h(0) (pi_c(0) ~ 1e-4 against B ~ 4e-3), one fixed-point step
    delta_h(r) = B(r) / (E m)
    pi_c(s)    = B [A(s) - kappa b_w] / [(1 - A(s)) + B (A(s) - kappa b_w)],     A(s) := X(s) + b_w = P(w lost | h lost, s)

where X(s) is the same-month excess in group s. Illustrative with non-temporary CPS numbers (b_w = 0.0023,
X(0) = 0.026, B ~ 0.004 from the SIPP's 0.4-0.6% involuntary separations per employed husband-month, kappa = 2.3):
pi_c(0) ~ 0.004 x (0.0283 - 0.0053) / 0.972 ~ 1.0e-4 a month; for the shared-employer cell with X(2) = 0.337 (all
losses; to recompute non-temporary and as an exclusive group): pi_c(2) ~ 0.004 x 0.33 / 0.66 ~ 2.0e-3, so about a
third of husbands' job losses in that cell are common shocks (pi_c / (pi_c + B)). Annual implication of these numbers
as an over-identification check: P(both displaced in the same year) ~ 12 pi_c(0) + 144 kappa b_w B = 0.0011 + 0.0030 =
0.0041 against P(h in year) ~ 0.048, so P(w | h) - P(w | not h) ~ 0.087 - 0.027 ~ 0.06, against the PSID's 0.063
(0.102 - 0.039), of which the common shock contributes about 0.024 and the type 0.036 (PSID decomposition: 0.033
contemporaneous, 0.020 permanent). The closed forms are therefore consistent with the annual facts to first order, and
they are the SMM start values (`inputs/start_analytic.json`, written by `paperA_model/analytic_start.py` from the
IGE/60 targets file, so that the mapping is coded).

**Why the nine displacement parameters stay inside the SMM (exact vs approximate):**

1. *The CPS "job loss" is a measurement of the model.* A job loser is employed in m-1 and unemployed for a job-loss
   reason in m; a displaced wife who would not accept a job (classified as not looking) is not a CPS job loser, so the
   observed b_w is (E m) delta_w x P(looking | displaced), with the acceptance probability endogenous (phi_F, theta,
   lambda_w, assets). Husbands always look, so (C) is exact for them up to the E -> E transitions that the CPS cannot
   see within a month (a displaced husband re-employed within the month: zero in the model by construction, D-timing).
2. *State x month fixed effects.* The CPS excess nets out the local cycle; the model has no aggregate state and its
   raw simulated difference is compared with the FE estimate (model document, Section 9). The leads and lags are
   affected most: a part of L is a common shock spread over months (closures take months), which the model's
   same-month common shock cannot produce and which the type then absorbs.
3. *PSID annual rates are among working heads at the interview,* with the wife "working at baseline"; both are
   endogenous selections reproduced only by the measurement layer. The husband's 8.0% / 4.8% also includes an
   entry-year effect (couples enter in their first observed year).
4. *By race, the CPS base rates are precise, the excess by race x match is not* (the shared-employer cell holds 6.3%
   of couples; Black couples are 8% of the panel). The cut list's "common delta_w across races" is the guard.

So: exact algebra for start values and for the Jacobian's expected pattern (delta_w from b_w, B from b_h, pi_c(s)
from X(s), kappa from L), approximate as calibrations; the SMM keeps them, the Jacobian confirms that they are pinned
"almost one for one" as the paper says.

### 1.5 Other parameters with closed-form start values (kept in the SMM)

| Parameter | Closed form (start value) | Data moment | Why it stays in the SMM |
|---|---|---|---|
| sigma_0(r) | -ln(1 - s_r) / 12 - sigma_J(r) f_r, with s_r the annual separation rate and f_r the share of couple-months with the husband non-employed after a displacement (f_r ~ 0.01-0.02, so the second term is negligible at the start) | PSID annual separation rate of couples by race (`IGE/60`) | the PSID rate is between interviews (attrition, biennial after 1997); the simulated rate runs through the same wave structure |
| sigma_J(r) | Delta_r / D_r, with Delta_r the fall in "still with wife" over years 1-3 (0.045 B, 0.019 W) and D_r the expected non-employed months of a displaced husband within the window (SIPP: sum over months of 1 - re-employment probability; about 5 months) -> sigma_J(B) ~ 0.009, sigma_J(W) ~ 0.004 a month | `IGE/19` (response), `IGE/40` (D_r) | D_r depends on lambda_h; the response is measured at interviews |
| pi_up,j | g2_j / (24 psi_j), with g2_j the two-year log wage growth of the continuously employed at 25-34 | `IGE/60` (PSID wage growth by age group) | truncation at level 7 and the age-group pattern (a constant pi_up gives the same growth at 45-54; the fallback is Bacher et al.'s level-dependent pi_up h^(-eta), D-text) |
| pi_dn,j | slope / psi_j of the re-employment earnings loss in the length of non-employment, loss(n) ~ psi (d_j + pi_dn n) fitted on the three SIPP spell groups (1-3, 4-12, 13-24 months) | `IGE/40` / `IGE/60` (involuntary separations, by spouse) | earnings, not wages (hours at re-employment differ); the model's measurement layer uses earnings too |
| d_j | intercept / psi_j of the same fit, truncated at 0 | same | cut if the 1-3 month loss is near zero (Bacher et al.'s all-separation numbers 1% / 7% / 20% give an intercept near zero) |
| lambda_h(r) | from the 3-month re-employment: 1 - (1 - lambda)^3 = 0.586 (relative to 0.983) -> lambda_h ~ 0.26; the 6- and 12-month points imply 0.18 and 0.12 | `IGE/40` | the path is not geometric (Section 2.3); SMM compromise, miss reported |
| lambda_w(r) | lower bound: the CPS monthly entry of non-employed wives (0.094 B, 0.075 W) divided by an acceptance probability < 1 | `IGE/30` | acceptance is endogenous (phi, theta, assets): the SIPP build-up separates it |
| phi_h | the husband's part-time share is a logit in (y_h(F) - y_h(P) - phi_h-equivalent) at the taste scale: calibratable one-for-one (cut list item) | `IGE/60` | kept for the one-run rule; first to be calibrated if the count must fall |

Everything else (phi_F, phi_P, theta_05, theta_617, F, kappa_S, a_bar) has no closed form: start values from the
lifecycle model's analogues where they exist (phi, theta) and from the data's levels otherwise (a_bar at the 10th
percentile of liquid wealth of couples at 25-34; F at 10% of the wife's part-time earnings; kappa_S such that the
static take-up among eligible couples is about 60%).

### 1.6 Remaining calibrated inputs (direct data moments; exact as definitions)

| Input | Mapping | Script |
|---|---|---|
| Workplace-match shares P(s | r) | coded on each PSID couple at entry from both spouses' three-digit industry, occupation and class of worker (CPS definition); the PSID distinguishes private / government / self-employment coarsely, so s = 2 is approximate; CPS shares 6.3 / 11.4 / 82.3% as the check | `IGE/60` |
| Child process b_0(age_w, r), b_2(age_w, r) | annual birth probability of PSID couples with no child under 18 (resp. youngest 6-17), by wife's five-year age group and race, divided by 12; ageing 1/72 and 1/144 are the bucket lengths | `IGE/60` |
| n(k, age_w, r) | PSID mean number of children under 18 by bucket, age group and race, rounded | `IGE/60` |
| Childcare price p_cc(k) | PSID annual childcare spending / mother's annual hours, couples with the mother working, by youngest-child bucket (waves with the childcare item: 1988, 1999-2021), 2000 dollars; p_cc(0) = 0 | `IGE/47` (consumption module) or `IGE/60` |
| Initial conditions | copies of PSID couples at first observation from 1984: calendar year, wife's age, race, s, liquid wealth (imputed in non-wealth waves by age x race x education cell medians from 1984, 1989, 1994, 1999-2021), each spouse's employment, youngest-child bucket, human capital level h_j = 4 + round((ln w_j - mu_j(r)) / psi_j) truncated to 1-7 (last observed wage, or the education-and-age prediction, for a non-employed spouse; the transitory shock at entry is ignored: approximate), UI state (entitled if a job loss is reported in the entry year and not employed), K copies | `IGE/60` writes `inputs/psid_entry_couples.csv` |
| Child-block slopes | high: beta_05 = beta_617 = -0.09 / Delta ln y_bar(sim), where Delta ln y_bar(sim) is the simulated mean log family-income loss over the remaining childhood of a child whose father is displaced at the mean displacement age in the baseline (Oreopoulos et al. 2008 and Page et al. 2009: about -9% in adult earnings); low: the same with Hilger's (2016) earnings effect (an order of magnitude smaller; read the number from his earnings table before coding); beta_P: PSID association of the share of childhood months with both parents present with adult log earnings, with the controls of Paper A Section 6 (high), 0 (low) | counterfactual script (post-estimation); `IGE/20` (beta_P, to add) |

---

## 2. Identification map for the 31 SMM parameters

### 2.1 Parameter x moment table

"Primary" = the block whose Jacobian column should dominate; "secondary" = over-identifying moments. The economic
argument states the sign and the mechanism the Jacobian must show.

| # | Parameter | Primary moments (window, script) | Secondary | Economic argument |
|---|---|---|---|---|
| 1-2 | delta_w(B), delta_w(W) | wife's monthly non-temporary job-loss rate, husband employed, by race (CPS 94-23, IGE/37, 60) | her annual displacement rate (PSID 84-21, IGE/25) | base rate = (E m) delta_w x P(looking); one for one |
| 3-4 | delta_h(B), delta_h(W) | his monthly non-temporary job-loss rate by race (CPS, IGE/60); his annual displacement rate 8.0 / 4.8% (PSID, IGE/19) | his hours in year 0 | base rate; exact for husbands |
| 5-7 | pi_c(0), pi_c(1), pi_c(2) | same-month excess by exclusive match group, non-temporary (CPS, IGE/60) | same-year joint displacement by sector and three-digit industry (PSID, IGE/25); DWS same-year ratio (validation) | the spike only; pi_c(s) ~ B X(s) / (1 - X(s)) |
| 8-9 | p_H, m_H | her excess in months -3..-1 and +1..+3 (CPS, IGE/30, 60); permanent component 0.020 and placebo-window 0.033 (PSID, IGE/38) | base rates; wealth moments (type risk raises precautionary saving) | flat elevation = delta_w Var m / E m; ridge along the CV (Section 2.3) |
| 10-11 | lambda_w(B), lambda_w(W) | monthly employment entry of non-employed wives by race (CPS, IGE/30) | her employment at months 0, 1, 6 after his separation (SIPP, IGE/40); looking jump (validation) | entry = lambda_w x acceptance; the build-up speed is lambda_w, its level the acceptance |
| 12-13 | lambda_h(B), lambda_h(W) | his employment 3, 6, 12 months after an involuntary separation (SIPP, IGE/40) | his annual hours years 1-3 (PSID, IGE/19) | geometric re-employment; the hours path checks the annual aggregation |
| 14-15 | pi_up,w, pi_up,h | two-year log wage growth of the continuously employed at 25-34, 35-44, 45-54 (PSID, IGE/46 / 60) | level of the married men's earnings profile (validation) | growth = 24 pi_up psi; flattening only through the grid top |
| 16-17 | pi_dn,w, pi_dn,h | re-employment earnings by spell length 1-3 / 4-12 / 13-24 months, by spouse (SIPP, IGE/60) | her wage at re-entry after 12+ months (PSID); his year-6 loss relative to years 1-3 (PSID) | slope of the loss in the spell |
| 18-19 | d_w, d_h | labor income loss years 1-3 after own displacement (PSID: -17% / -24% his; about -$4,600 hers) | re-employment loss after 1-3 months (SIPP) | level of the loss after a short spell; cut if ~0 |
| 20 | phi_F | employment of wives with no child under 18 (PSID, IGE/60); wives' monthly exit from employment outside job loss (CPS, IGE/60) | gross added work of wives who kept their job (PSID, IGE/38) | level of participation; exits pin the quit margin |
| 21 | phi_P | part-time share of employed wives (PSID) | - | intensive margin |
| 22-23 | theta_05, theta_617 | employment of wives by youngest child (PSID); her added hours and employment after his displacement by child age (+112 / -26 hours; +0.041 / -0.038) | SIPP build-up by child age (validation) | the level by child age and the response by child age: two readings of each theta |
| 24 | phi_h | part-time share of employed husbands (PSID) | - | one for one (cut list) |
| 25 | F | consumption change after her own displacement (-0.031, PSID 99-21, IGE/47); joint minus single (-0.059) | BPS extensive-margin complementarity (validation) | spending falls less than income when her work ends; two work flows end at a joint loss |
| 26 | kappa_S | SNAP receipt of couples by race (PSID); its rise after his displacement +0.042 / +0.033 | - | static take-up among eligibles and its response |
| 27-28 | sigma_0(B), sigma_0(W) | annual separation rate by race (PSID) | - | baseline hazard |
| 29-30 | sigma_J(B), sigma_J(W) | still with wife, years 1-3: -0.045 / -0.019 (PSID, IGE/19) | year-6 response (-0.074 / -0.030; validation) | hazard while non-employed x months non-employed |
| 31 | a_bar | share of couples with liquid wealth <= 0 by wife's age group (PSID wealth waves, ReducedForm/17 for couples); consumption change after his single displacement (-0.013, PSID 99-21) | share above one year of earnings; assets / human wealth (validation) | the limit sets the mass at the constraint and the fall in spending at a shock |

### 2.2 Which moments inform which parameters (block view)

| Moment block | Parameters it moves (expected Jacobian pattern) |
|---|---|
| CPS same-month excess by match | pi_c(s) (dominant), delta_h (denominator), p_H, m_H (kappa term), phi/theta/lambda_w (through P(looking)) |
| CPS leads and lags | p_H, m_H (dominant), delta_w |
| CPS base rates | delta_w (through acceptance: phi_F, theta), delta_h |
| PSID annual joint loss, permanent / contemporaneous | pi_c (contemporaneous), p_H, m_H (permanent), lambda_w (wife "working at baseline") |
| CPS entry of non-employed wives; SIPP wife path 0-6 | lambda_w (speed), phi_F, theta (acceptance), a_bar (poorer wives accept more) |
| SIPP husband path; PSID his hours years 1-3 | lambda_h; (sigma_J through months non-employed) |
| PSID wage growth; SIPP re-employment loss; PSID year-6 loss | pi_up, pi_dn, d |
| PSID employment by child age, part-time shares | phi_F, phi_P, theta_05, theta_617, phi_h |
| PSID added work by child age | theta_05, theta_617 (response), lambda_w, a_bar |
| PSID SNAP receipt and response | kappa_S; (a_bar and c_min fixed: the eligible mass) |
| PSID separation rate and response | sigma_0, sigma_J; (lambda_h) |
| PSID wealth shares; consumption after his / her / joint displacement | a_bar, F; (lambda_w, theta: how much she adds) |

### 2.3 Weak directions, the cut list, and two known tensions

1. **(p_H, m_H) ridge.** Only kappa - 1 = Var m / (E m)^2 is seen by the monthly leads and lags, and the PSID placebo
   window sees the same ratio on annual windows (approximately; three-year windows make it 1 - (1 - 12 m delta)^3 and
   therefore slightly convex in m). Jacobian expectation: the two columns are near-collinear (|corr| > 0.9) along
   p_H (1 - p_H)(m_H - 1)^2 / (1 + p_H (m_H - 1))^2 = const. Remedy: the over-dispersion moment of Section 1.4 (PI
   decision). If it is not added, the SMM reports the ridge (the profile of Q along it) and fixes p_H at 0.2 in a
   robustness run; the counterfactuals that depend on the type (saving) are reported along the ridge.
2. **pi_c(1) vs pi_c(2).** Separated by the two exclusive CPS groups; weak only if the non-temporary excess in the
   shared-employer cell (6.3% of couples) is imprecise. Rule (D14): merge if |corr| > 0.95 in the Jacobian or if the
   recovery test cannot return them within 2 s.e.
3. **delta_w(B) vs delta_w(W).** Base rates by race are precise in the CPS (1.3 million couples), so this should not be
   weak; cut-list item only if the Black cells of the PSID annual moments pull against the CPS.
4. **lambda_w vs (phi_F, theta).** Entry = lambda_w x acceptance; the SIPP build-up (0.019, 0.037, 0.054 at months 0, 1,
   6) gives the speed, the levels the acceptance. Expected to be identified; if the Jacobian shows |corr| > 0.9 between
   lambda_w and phi_F, the fallback of D16 (a searching / not-searching state) is the structural answer, not a cut.
5. **d_j vs pi_dn,j.** Level vs slope in the SIPP spell groups; three groups, two parameters per spouse, plus the PSID
   over-identification. Cut d_j if the 1-3 month loss is within 2 s.e. of zero (D14).
6. **F vs a_bar.** Both lower spending after a displacement. Separated by whose displacement (F acts at hers and at
   joint losses, a_bar at his, which is the larger income loss) and by the wealth shares, which F does not move.
7. **sigma_0 vs sigma_J.** Baseline vs response: not weak.
8. **kappa_S.** Identified only if the eligible mass is right, which depends on the fixed schedules and on a_bar
   (the asset test); check the simulated eligible share against the PSID's before reading the Jacobian column.
9. **Known tension A: lambda_h constant.** SIPP re-employment 0.586, 0.708, 0.791 at 3, 6, 12 months (against
   0.983, 0.972, 0.960 for the non-separated) implies monthly job finding of 0.26, 0.18 and 0.12 under a geometric
   model: duration dependence or heterogeneity that a constant lambda_h cannot produce (the type tau does not enter
   lambda). The SMM will fit a compromise around 0.17 and miss the 3-month point from below and the 12-month point
   from above. Report the miss; the fallback (lambda_h for months 1-3 and after month 3: +2 parameters) goes to the
   PI only if the miss exceeds 3 s.e. on two of the three points.
10. **Known tension B: pi_up constant.** The two-year wage growth of the continuously employed falls with age in
    every data set; with a constant pi_up the model flattens only through the grid top (level 7). If the 45-54 growth
    is missed by more than 2 s.e., the one-parameter alternative is pi_up h^(-eta) (Bacher et al.), decided at the
    recovery stage, not an age profile.

**Cut list in order (D14):** pi_c(2) merged with pi_c(1); common delta_w across races; phi_h calibrated to the
husbands' part-time share; common pi_dn for both spouses; d_j cut if the 1-3 month loss is near zero; the wife's
lost-hours record in the UI state (benefit on full-time-equivalent earnings times a part-time factor). Each cut is
decided by a named Jacobian / recovery criterion below, applied once, before the HPC run.

### 2.4 Numerical Jacobian and local identification protocol

Adapt `estimation/smm.py: cmd_jacobian` (read-only import of its logic into `paperA_model/jacobian.py`; the
engine's parameter list is the lifecycle model's, so the function is re-implemented over Paper A's names):

- At the analytic start values theta_0, move each parameter up and down by h = 5% of its bound range (two-sided),
  common random numbers, 2 x 31 + 1 = 63 evaluations (8 workers x 2 threads on the PC: 8 rounds; at 60 s an
  evaluation about 10 minutes, at 600 s about 1.5 hours).
- S[i, j] = change in moment i in standard-error units per 10% move of parameter j's range. Report: sensitivity
  ||S_j||; the block holding the largest share of each column's sum of squares (must be the "primary" block of
  Section 2.1); the singular values of S and the parameter loadings of the five smallest; near-collinear pairs
  (|corr of columns| > 0.9).
- **Pass criteria:** (i) ||S_j|| >= 3 for every parameter (a 10% move shifts the moments by at least three standard
  errors in norm) and the primary block is the top block; (ii) no pair with |corr| > 0.95 except (p_H, m_H), which is
  expected (Section 2.3 item 1); (iii) condition number of S below 1e4; (iv) the smallest singular vector loads on at
  most two parameters, and they are on the cut list or the ridge. A failure on (i) cuts or ties the parameter per
  the list; on (ii) merges the pair.
- **Profiles:** Q along each parameter on 21 points over +-25% of its range at theta_0 (`cmd_profile` logic):
  unimodal within the window, minimum within 10% of the range of the start (for parameters with closed forms).
- **Pseudo-data recovery:** targets replaced by the model's moments at theta_true (= theta_0 perturbed), start
  perturbed by 0.5 s.d. in transformed units (`--pseudo-seed`, `--start-noise` logic), CMA-ES with popsize 16; first
  on the 17 closed-form parameters (others fixed at truth), then all 31. Pass: each estimate within 2 simulation-noise
  s.e. of truth (the noise s.e. from 5 re-simulations at theta_true with different CRN seeds), Q at the estimate
  below Q at truth plus the noise band.
- **Simulation noise** (memory rule: compare Q only on common draws): fix the CRN seed for the whole project and
  report Q's spread across 5 seeds once, at theta_0, so that fit differences smaller than it are not read.

---

## 3. Targets: windows and scripts

Windows: PSID couple-years 1984-2021 (displacement, hours, employment, wages, SNAP, separation); PSID consumption
1999-2021 (events 2000-2020); CPS basic monthly 1994-2023 (couples panel of IGE/30); SIPP 2004, 2008, 2014 panels =
2003-2016; DWS 1984-2024 (validation); BPS test years 1998-2008 (simulated labels). One targets file,
`IGE/60.PaperATargets.py` (being written), produces every target with 200 bootstrap draws (1968 families; households
in CPS and SIPP) and writes `EstimationMoments/couples_targets.csv` (block, name, race, window, value, se, N) plus
`couples_bootstrap.npz`; consumption from `IGE/47.PSIDConsumptionEvent.py` (done, s.e. clustered by 1968 family). The
simulated counterparts are computed by the same functions (imported from IGE/60) on the measurement-layer panels.

| # | Block | Moment | Window | Script (status) |
|---|---|---|---|---|
| T1 | Joint loss, monthly | wife's same-month non-temporary job-loss excess, he loses vs keeps (state x month FE in the data; raw difference in the model) | CPS 94-23 | IGE/37 -> IGE/60 (s.e. to report) |
| T2 | | same, three exclusive match groups (shared-employer cell / same detailed industry / other), non-temporary | CPS 94-23 | IGE/60 (recompute; IGE/37 has the non-exclusive all-loss versions) |
| T3 | | wife's excess in months -3, -2, -1 and +1, +2, +3, non-temporary | CPS 94-23 | IGE/30 -> IGE/60 |
| T4 | Joint loss, annual | permanent component (0.020) and contemporaneous component (0.033) | PSID 87-21 | IGE/38 (s.e. implied by p) |
| T5 | | P(w displaced | h displaced) - P(| not), all / same sector / different sector (0.063; 0.183; 0.041) | PSID 84-21 | IGE/25 |
| T6 | Base hazards | wife's monthly non-temporary job-loss rate, husband employed, by race (pooled 0.0023) | CPS 94-23 | IGE/37 -> IGE/60 |
| T7 | | husband's monthly non-temporary job-loss rate, by race | CPS 94-23 | IGE/60 (new) |
| T8 | | husband's annual displacement rate, working male heads, by race (0.080 / 0.048) | PSID 84-21 | IGE/19 -> IGE/60 |
| T9 | Her search | monthly employment entry of non-employed wives, husband employed, by race (0.094 / 0.075) | CPS 94-23 | IGE/30 |
| T10 | | employment of wives with no job the month before, months 0, 1, 6 after his involuntary separation (0.019, 0.037, 0.054) | SIPP 03-16 | IGE/40 |
| T11 | Her exits | wives' monthly exit from employment without a job-loss reason, husband employed | CPS 94-23 | IGE/60 (new) |
| T12 | His search | his employment 3, 6, 12 months after an involuntary separation vs none (0.586, 0.708, 0.791 vs 0.983, 0.972, 0.960) | SIPP 03-16 | IGE/40 (s.e. to report) |
| T13 | | his annual hours, years 1-3 after displacement, by race (-146 / -130) | PSID 84-21 | IGE/19 -> IGE/60 |
| T14 | His earnings | labor income years 1-3 by race (-4,160 / -9,622); year 6 (about -6,000 to -7,000) | PSID 84-21 | IGE/19 -> IGE/60 |
| T15 | Her earnings | labor income after her own displacement, years 1-3 (about -4,600) | PSID 84-21 | IGE/25 -> IGE/60 |
| T16 | Wage growth | two-year log wage growth, continuously employed wives and husbands, 25-34 / 35-44 / 45-54 | PSID 84-21 | IGE/46 / IGE/60 |
| T17 | | her log wage at re-entry after 12+ months out, relative to continuously employed | PSID 84-21 | IGE/60 |
| T18 | | earnings in the first month of re-employment relative to the last month of the previous job, 1-3 / 4-12 / 13-24 months, involuntary, by spouse | SIPP 03-16 | IGE/40 -> IGE/60 |
| T19 | Added work | wife's hours and employment, years 1-3, youngest 0-5 / 6-17 (+112 / -26; +0.041 / -0.038) | PSID 84-21 | IGE/19 -> IGE/60 (from 1984) |
| T20 | | gross response of wives who kept their job, all / youngest 0-5 (+47 / +97); offset from joint losses (-35) | PSID 84-21 | IGE/38 |
| T21 | Employment levels | wives' employment by youngest child (none, 0-5, 6-17); part-time share of employed wives; of employed husbands | PSID 84-21 | IGE/60 |
| T22 | Safety net | SNAP receipt after his displacement, years 1-3, by race (+0.042 / +0.033); SNAP receipt of couples by race | PSID 84-21 | IGE/19 -> IGE/60 |
| T23 | Separation | still with wife, years 1-3, by race (-0.045 / -0.019); annual separation rate by race | PSID 84-21 | IGE/19 -> IGE/60 |
| T24 | Wealth | share of couples with liquid wealth <= 0 and above one year of earnings, by wife's age (25-34, 35-44, 45-59) | PSID 1984, 89, 94, 99-2021 | ReducedForm/17 logic for couples -> IGE/60 |
| T25 | Consumption | change in log consumption, first three interviews after his single displacement: pooled (-0.013), B / W (-0.005 / -0.005) | PSID 99-21 | IGE/47 (done) |
| T26 | | same after her own displacement (-0.031) | PSID 99-21 | IGE/47 |
| T27 | | joint minus single (-0.059, s.e. 0.073) | PSID 99-21 | IGE/47 |
| T28 (proposed) | Over-dispersion | share of husbands displaced two or more times among those observed >= 10 years, by race | PSID 84-21 | IGE/60 (PI decision; Section 1.4) |

Validation (not targeted; same scripts): CPS looking jump and 12-month employment path (IGE/30); SIPP months 12-36
(IGE/40); DWS same-year ratio (IGE/39); family income years 1-3 (IGE/19); already-unemployed wives' job finding (IGE/30);
excess by child age and race (IGE/30, 25); assets / human wealth (BPS Figure 3); married men's earnings profile
(ModelInputs); AWE by age, joint loss by age, joint labor-market states by age, transition matrices (IGE/50, in progress;
IGE/30); job finding by age (IGE/30, 40); BPS on simulated data (harness, Section 4 stage 7).

Consumption moments are matched only on 1999-2021 simulated couple-years (memory rule), with BPS's measurement-error
variance (E(dc_t dc_{t-2}) = -0.0332) added to simulated consumption before the moment is computed.

---

## 4. Build and estimation plan

### 4.1 Code location and rules

New self-contained folder `paperA_model/` (nothing in `model/` or `estimation/` is touched; both are used by
running HPC jobs). Read-only imports allowed: `estimation.smm.SafePool` (crash-tolerant worker pool) and the logistic
transform idea (three lines, copied), `bps_reconciliation/code/sim_panel_writer.py` (BPS shape), the moment
functions of `IGE/60.PaperATargets.py`. Proposed files:

| File | Role |
|---|---|
| `params.py` | the 31 estimated parameters (name, bounds, block), the fixed inputs loader (`inputs/*.json`), the era schedules |
| `analytic_start.py` | Section 1.4-1.5 closed forms from `EstimationMoments/couples_targets.csv` -> `inputs/start_analytic.json` |
| `solve.py` | numba solver for one problem (r, s, tau) and one era: backward induction, DC-EGM with the upper envelope, the sequential expectation operators; stores W_{t+1}(a'; .) float32 |
| `simulate.py` | monthly histories for the PSID copies of one problem, CRN; re-solves the static monthly problem from W |
| `panels.py` | measurement layer: PSID household-years (waves observed), CPS couple-months (4-8-4, weights), SIPP paths, DWS recall window, BPS shape (via `sim_panel_writer`) |
| `moments.py` | the target vector on simulated panels through IGE/60's functions; Q with inverse-variance or block weights |
| `estimate.py` | CLI: `evaluate`, `jacobian`, `profile`, `run` (CMA-ES, resume, pseudo-data recovery), `se` (sandwich (G'WG)^-1 G'W Omega W G (G'WG)^-1 with G the central-difference Jacobian at the estimate and Omega the bootstrap covariance of the targets plus the simulation covariance across re-simulation seeds: the `estimation/standard_errors.py` pattern re-implemented) |
| `checks.py` | staged checks (1)-(7) of the model document, timing and peak-memory report |
| `counterfactuals.py`, `children.py`, `validate.py`, `bps_test.py` | stage 7 |
| `hpc_job_a.py` | Slurm launcher modelled on `scripts/hpc_job.py` (code snapshot by git archive, `--commit`, email, resume, push of results into `paperA_model/results/hpc_runs/`), job names `Joint-<what>`; written new, `scripts/hpc_job.py` untouched |
| `inputs/`, `results/` | fixed inputs with their derivation; run outputs (final estimates committed, run folders off Google Drive) |

Rules carried into the code: all 31 parameters free in one run (`--fix` only for the restricted independent-shock
model: pi_c(.) = 0, m_H = 1, and for recovery tests); every fixed input is produced by a script named in
`inputs/README.md`; CRN seeds fixed project-wide; consumption moments only on 1999-2021 simulated years.

### 4.2 Stages, tests, pass criteria

**Stage 0 - inputs (week 0-1; no model code).**
- `IGE/60.PaperATargets.py` (in progress): targets T1-T27 (T28 if approved) with bootstrap s.e.; pass: reproduces
  Paper A's published numbers on their windows to the published digit, and the new windows are documented.
- `IGE/61.PolicySchedules.py` (new): Section 1.3 schedules by era; pass: a check table against published values for
  three years per era (e.g. 1990, 2003, 2015), TAXSIM fit R^2 > 0.99 within each year, EITC maxima by n to the dollar.
- `IGE/39` addition: UI receipt share of displaced wives; `IGE/60`: match shares, child process, n(k, age, r),
  childcare price, entry couples file, wealth imputation. Pass: CPS match shares 6.3 / 11.4 / 82.3% reproduced within
  1 point when the CPS definition is coded on the CPS itself; PSID shares reported next to them.
- `analytic_start.py`: start values and the over-identification check of Section 1.4 printed (annual excess implied
  by the monthly closed forms against T5).

**Stage 1 - solver (weeks 1-3).**
- Single problem, single era, 420 months. Staged checks in order: (1) flat consumption with no risk and beta(1+r) = 1
  (max deviation < 1e-3 of mean consumption); (2) a buffer stock with risk (mean assets > 0 and rising with the
  hazards); (3) the wife's work rises with lower assets and after the husband's loss (monotone in a at the median
  state; the response positive in the month after his loss); (4) the search friction lengthens non-employment (mean
  spell = 1/lambda +- 5% in a no-choice test); (5) the wife's exits from non-employment rise when entitlement lapses;
  (6) with pi_c(.) = 0 and m_H = 1 the spouses' job losses are independent in the simulated CPS panel (same-month
  ratio within 1.05 of 1); (7) with sigma_nu = 0 the simulated BPS transitory variance comes only from displacement and
  within-year human capital moves. Check (3) also decides the D16 fallback.
- **Timing and memory, measured here, before anything else** (Section 4.6): seconds per problem-era on 2 threads;
  peak RSS of one worker (solver arrays + one problem's simulated couples). Decision point with the PI if an
  evaluation exceeds 120 s: fallback fallback sequence.

**Stage 2 - simulator and measurement layer (weeks 3-4).**
- CRN draws per couple-copy for every shock; each simulated couple carries its calendar month; copies K (start 3,
  raise until Q's CRN spread at theta_0 is below 2% of Q).
- `panels.py`: pass when IGE/60's functions run unchanged on the simulated PSID panel and produce every target
  (no NaN; N per cell within 50% of the data's, scaled by K), the CPS panel reproduces the 4-8-4 observation
  pattern and the data's age distribution of wives by year, the SIPP panel the 36-month window, the BPS writer passes
  `check_layout()`.
- The one-time wage-process correction (Section 1.2) runs here (Stata on the PI's PC: a point-estimate run is 2-4
  minutes; `bps_on_sim.do`). Output: `inputs/wage_process.json` with before / after.

**Stage 3 - moments, objective, Jacobian, recovery (weeks 4-5; PC).**
- `evaluate` at theta_0: Q by block printed; every block finite; the pre-set mappings' consistency (Section 1.4
  check) within 2 s.e. on T5.
- `jacobian` (Section 2.4): pass criteria (i)-(iv); apply the cut list where a criterion fails; record the decision
  in `results/jacobian_<stamp>/decisions.md`.
- `profile` on the 17 closed-form parameters (unimodal, minimum near the start).
- Pseudo-data recovery, 17 then 31 parameters, popsize 16, maxfevals 1,600 (100 generations) for the 17 and 3,200
  for the 31: within 2 noise-s.e. of truth. On the PC with 8 workers x 2 threads: at 60 s per evaluation about 3.5 h
  and 7 h; at 300 s, 17 h and 34 h (then the 31-parameter recovery goes to the HPC as `A-recovery`).

**Stage 4 - local SMM on the PC (week 5).**
- Short real-data run (50 generations, 800 evaluations) from theta_0: Q falls monotonically in the generation
  minimum; no block dominates Q by more than 10x the next after 50 generations (otherwise check the block's s.e.
  and the measurement layer before the HPC run); the worker peak memory below 3.5 GB (8 x 3.5 = 28 GB of 31).
- Hardware: 16 cores, 31 GB. Default `--workers 8 --threads 2`. If the peak memory per worker exceeds 3.5 GB:
  `--workers 6 --threads 2` (12 cores), never swap.

**Stage 5 - HPC main runs (weeks 5-8; the PI submits: Stanage needs the PI's password and Duo, so no unattended
submission).** Settings per the standing rules: 32 cores, `--threads 2` (16 workers), 64 GB, sized `--time`, email at
begin, end and failure, job names `Joint-<what>`. Commands (from `~/svr`, after `git pull` of the committed code and
inputs):

    # 20-minute test (every step: inputs, reproducibility of Q at theta_0 against the PC value, 2 generations, resume)
    sbatch --job-name=Joint-test --time=00:30:00 --cpus-per-task=16 --mem=32G --mail-type=BEGIN,END,FAIL \
           --mail-user=jiaqi.li@sheffield.ac.uk paperA_model/hpc_job_a.py --test

    # main model (31 parameters), analytic start, 8,000 evaluations (500 generations)
    sbatch --job-name=Joint-smm-main --time=48:00:00 --cpus-per-task=32 --mem=64G --mail-type=BEGIN,END,FAIL \
           --mail-user=jiaqi.li@sheffield.ac.uk paperA_model/hpc_job_a.py run \
           --start paperA_model/inputs/start_analytic.json --workers 16 --threads 2 --maxfevals 8000

    # independent-shock model on the same targets and draws
    sbatch --job-name=Joint-smm-indep --time=48:00:00 --cpus-per-task=32 --mem=64G --mail-type=BEGIN,END,FAIL \
           --mail-user=jiaqi.li@sheffield.ac.uk paperA_model/hpc_job_a.py run \
           --start paperA_model/inputs/start_analytic.json --fix pi_c0=0 pi_c1=0 pi_c2=0 m_H=1 \
           --workers 16 --threads 2 --maxfevals 8000

    # resume (state saved every generation), standard errors, block-weighting robustness
    sbatch --job-name=Joint-smm-main-r --time=24:00:00 --cpus-per-task=32 --mem=64G ... hpc_job_a.py --resume <run dir>
    sbatch --job-name=Joint-se        --time=04:00:00 --cpus-per-task=32 --mem=64G ... hpc_job_a.py se --start <best.json>
    sbatch --job-name=Joint-smm-block --time=48:00:00 --cpus-per-task=32 --mem=64G ... hpc_job_a.py run --weighting block ...

  squeue format with full names: `squeue -u $USER -o "%.10i %.20j %.8T %.10M %.6D %R"`.
  `--time` is sized from the measured evaluation time: generations x (popsize / workers) x seconds per evaluation
  x 1.3, capped at 48 h with resume. Results come back through `--push` into `paperA_model/results/hpc_runs/`.
  Pass: Q at the HPC start equals the PC value (reproducibility step of `--test`); the main run's best Q stable over
  the last 50 generations (change < 1%); every block's contribution reported; the independent-shock model's Q and
  the difference by block.

**Stage 6 - fit, standard errors, cut-list confirmation (week 8).**
- Sandwich standard errors from the Jacobian at the estimate and the bootstrap covariance of the targets; the
  Jacobian re-run at the estimate (the identification check reported at the estimate, not only at the start).
- Fit table by block; the model document's Table 2 filled; the ridge (if T28 was not added) reported as a profile.

**Stage 7 - counterfactuals, child block, validation, BPS test (weeks 8-10).**
- Counterfactuals (i)-(v) with the same draws, main and independent-shock models.
- Child block: beta scenarios computed from the baseline simulation (Section 1.6).
- Validation list (Section 3); AWE by age against IGE/50's data table (its data side is done: 5.94 overall, 6.37 /
  7.21 / 4.95 / 2.52 by age on Paper A's panel).
- BPS test per the harness: 50,000 couples labelled 1998-2008, mixture calibrated to the PSID's trim composition
  (iterate `gross_rate`, `gross_sd` until the displacement share among jump-trimmed rows is within 3 points of the
  PSID's 6.7% and the without / with-trim transitory ratio within 0.3 of 2.0), `bps_on_sim.do` as shipped and with
  each switch; pass table of the model document (Section 12). The central comparison is the model's own simulated
  response of her hours to his permanent wage against what BPS's estimator returns on the model's data (HARNESS.md
  6.2: the estimator gave -0.76 to -0.86 for a true -0.3).

**Stage 8 - writing (weeks 10-12):** results into `sec7_model.tex` (fit, counterfactual, pass tables); the model
document's "no results" sections stay as the pre-registration.

### 4.3 Memory budget per worker

- Solver: W_{t+1}(a'; .) for one problem-era: 211,680 x 420 x 4 B = 0.36 GB (float32); two months of V and the
  intermediate expectation arrays: < 0.05 GB; the separated wife's problem 5,040 x 420 x 4 B, negligible.
- Simulation: process one problem at a time; keep per couple-month only the fields the measurement layer needs
  (12 int16 / float32 fields): with about 5,000 PSID entry couples x K = 3 copies x 420 months x 12 x 4 B = 0.3 GB,
  aggregated to the data-shaped panels before the next problem. Peak target: < 2.5 GB per worker on the PC
  (8 workers), < 3.5 GB on the HPC (16 workers in 64 GB).
- numba compile cache warmed by one evaluation in the parent before the pool starts (`SafePool(warm=...)`).

### 4.4 Stop and fallback rules

| Trigger | Action |
|---|---|
| Evaluation > 120 s on 2 threads after profiling (stage 1) | to the PI with measured numbers and the fallback sequence: (a) 5 human capital levels (-49% states), (b) merge s = 1, 2 (-33% problems), (c) one era in estimation, era schedules only in simulation and counterfactuals (-67% solves), (d) 20 asset points (-33%), (e) drop the lost-hours record (wife states 4 -> 3, -25%); apply in that order until < 60 s |
| A staged check (1)-(7) fails | fix before stage 2; check (3) failing on the SIPP build-up triggers the D16 fallback (searching state), PI decision |
| Jacobian ||S_j|| < 3 or pair |corr| > 0.95 | cut-list action for that parameter (Section 2.3); recorded |
| Recovery misses a parameter by > 2 noise-s.e. | profile it; if flat, fix at the start value and report (counts as a cut); if bimodal, widen the start noise and re-run once |
| Q by block: one block > 10x the next at the end of a run | check its s.e. and measurement layer; block-weighting run; report both |
| HPC run not converged at the time limit | `--resume` (one generation lost at most); after two resumes without a 1% improvement, stop and report |
| lambda_h misses two of three SIPP points by > 3 s.e. | report; fallback (+2 parameters) to the PI |
| Wage growth at 45-54 missed by > 2 s.e. | pi_up h^(-eta) alternative to the PI |
| Peak memory > 3.5 GB per worker | fewer workers (PC: 6; HPC: 12 workers x 2 threads, 24 cores requested) before any 128 GB request (needs the PI's approval) |

### 4.5 Runtime estimates (to be replaced by measurements at stage 1)

- Evaluation: 12 problems x 3 eras = 36 solves of 420 months; plus simulation. See 4.6: 5-15 minutes on 2 threads
  before the fallback sequence; 30-60 s after it.
- Jacobian (63 evaluations): 8 rounds on the PC: 8-16 min at 60 s, 40-120 min at 300-900 s.
- Recovery 31 parameters (3,200 evaluations): PC 8 workers: 400 rounds -> 6.7 h at 60 s; HPC 16 workers: 200 rounds
  -> 3.3 h at 60 s, 17 h at 300 s.
- Main SMM (8,000 evaluations): HPC 16 workers: 500 rounds -> 8.3 h at 60 s, 42 h at 300 s (resume); PC: 1,000 rounds
  -> 17 h at 60 s (a PC main run is feasible only after the fallback sequence).
- Counterfactuals: 6 re-solves x 2 models; BPS test: one simulation of 50,000 couples (about 10 evaluations' worth
  of simulation) plus Stata runs of 2-4 minutes each.

### 4.6 Compute arithmetic behind the warning

Per month and problem-era, with sequential expectation operators: the continuation array has 211,680 entries; the
exogenous transitions are applied dimension by dimension for each of the 6 work configurations (l_w in {0, P, F} x
l_h in {P, F}; SNAP does not move the state), with fan-outs of about 3 (each spouse's human capital step) x 3
(innovations) + 4 (displacement outcomes) + 2 + 2 (job finding) + 2 + 2 (UI) + 2 (child) + 2 (separation, with the
wife's problem), roughly 25 multiply-adds per entry per configuration: 6 x 211,680 x 25 ~ 3e7. The DC-EGM step: 7,056
non-asset states x up to 12 alternatives x 30 grid points x about 20 operations ~ 5e7. About 1e8 operations per
month, 4e10 per problem-era, 1.5e12 per evaluation, at 1-2 GFLOP/s effective per thread in numba (memory-bound
gathers): 750-1,500 s single-threaded, 400-750 s on two threads, before simulation. The model document's 20-second
target would need a 30x gain; the fallback sequence gives about 20x (0.51 x 0.67 x 0.33 x 0.67 x 0.75 ~ 0.06). Item (c), one era
in estimation, is the largest single saving and the only one that changes no economics in the counterfactuals
(which are re-solved with the era schedules); it changes the estimation by giving every couple the 1997-2008
schedule while the data span three eras, which matters most for the SNAP and EITC moments. Measure first; then the
PI decides the fallback sequence's depth.

---

## 5. What the lead needs to decide

1. T28 (over-dispersion moment) in or out (Section 1.4).
2. q_UI by spouse if the DWS shares differ by more than 10 points (Section 1.3).
3. The fallback sequence's depth once stage 1 timing is measured (Section 4.6), in particular item (c).
4. Whether the one-time wage-process correction (Section 1.2) also rescales the permanent probabilities (my
   recommendation: yes, same rule as the transitory) or leaves them at the closed form.
