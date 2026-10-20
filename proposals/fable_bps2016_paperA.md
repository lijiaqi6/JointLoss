# Paper A and Blundell, Pistaferri and Saporta-Eksten (2016): BPS-like model, fully solved model, or hybrid? (2026-10-17)

Read, nothing edited or run outside this file: the BPS paper (AER 106(2), 387-435), the online appendix
(`20121549_app.pdf`, Appendices 1-5 and Appendix Table 1), and the replication package
(`116142-V1/AER_2012_1549_data/`: `shell.do`, `psid_interview.do`, `psid_individual.do`, `psid_consumption.do`,
`psid_sample.do`, `prepare_bootstrap.do`, `residual_measures.do`, `tax_rate_estimation_snap.do`,
`pi_s_estimation.do`, `variance_estimation.do`, `frisch_estimation.do`, `gmm_ado/gmm_age_fv4_pi5_ns_nltax_b0.ado`,
`paramfiles/T4C1.do`, `bootstrap.do`, `tables_7_8_9.do`, `insurance_extensive_margin.do`); Paper A
(`paperA_joint_loss/main.tex`, `sec1`-`sec8`, `appB_other.tex`, `appC_robust.tex`); my two earlier memos
(`fable_review_paperA.md`, `fable_model_choice_paperA.md`); the local data holdings (`Dropbox/PSID/Family/fam1999er`
to `fam2023er`, `wlth1999`-`wlth2007`, `Individual/ind2023er`; StataMP-64 installed under `C:/Program Files/Stata*`;
`IGE/19.FatherDisplacement.py`, `IGE/25.JointJobLoss.py`, `IGE/38.PSIDJointLossChecks.py`). Line numbers below are
from the do-files as shipped. Every BPS number is from their tables or appendix; every Paper A number from its text.

---

## 1. Verdict (five lines)

1. **Build the fully solved monthly two-earner model with job loss (the earlier memo's design), not a BPS-like
   approximation; but make it nest BPS *as a measurement*, not as a solution method.** Keep what BPS's estimator
   needs to run on the model's simulated data: correlated permanent and transitory hourly-wage shocks for both
   spouses, a progressive tax-and-transfer function on annual family earnings, assets, and a work cost that produces
   their extensive-margin complementarity. Then run BPS's own do-files on a BPS-style simulated sample.
2. **Why not BPS-like:** their method assumes interior hours for both spouses (p. 394, 419), transitory shocks that
   are "fully smoothed" (fn 10, p. 395), a tax function that is log-linear in positive earnings (eq. 6; undefined at
   zero earnings), biennial two-year differences, and identification from the intensive margin. Paper A's object is
   an extensive-margin event (two employments end in the same month), in liquidity-bound households (BPS's own
   E(pi) is 0.03 at age 30, Figure 3), whose policy question is what a schedule pays at zero earnings. None of that
   is representable in the approximation; a hybrid that log-linearises around interior hours inherits the problem.
3. **Why nest BPS anyway:** the referee's question will be "BPS find no missing insurance and 63% from family
   labor supply; you find the insurer is hit too; who is right?" The only answer that settles it is one model that,
   run through BPS's estimator on BPS's sample rules, gives BPS's numbers, and on the full sample gives the joint
   loss. That is the "one model, both answers" test of Section 3 and it costs little once the model exists.
4. **The reconciliation is not a dispute.** BPS measure the transmission of a continuously employed husband's hourly
   wage innovations to his wife's hours and the household's consumption, net of both spouses' employment status.
   Paper A measures the shock their sample, trimming and residualisation remove, at a frequency they cannot observe.
   Section 2 shows this line by line in their code; four of the lead's five points are right, one needs correcting,
   and three things are missing (UI is absent from BPS's T(.); the same-period transitory wage covariance in BPS's
   Table 3 is 0.31 in correlation units and significant, the trace of Paper A's shock; BPS's own untargeted hours
   moments miss 30-40% of hours-growth variance, which is where spells live).
5. **Do the empirical reconciliation before the model** (Section 4): rerun BPS's pipeline, as shipped, on the local
   PSID 1999-2009 files (StataMP is installed; all files are on disk), then relax each restriction one at a time
   and add the displacement flags from `IGE/19` and `IGE/25`. About three weeks; it gives Paper A a table a referee
   cannot ask for twice, and it tells the model what BPS's numbers look like without the restrictions.

---

## 2. How both papers are right: what BPS's code does, point by point

### 2.1 The lead's five points, checked against the code

| # | Lead's point | Verdict | What the code says |
|---|---|---|---|
| 1 | The shock is a permanent/transitory hourly-wage innovation for continuously employed husbands, not job loss | **Correct, and stronger than stated** | Wage = annual labor earnings / annual hours (`prepare_bootstrap.do` l. 78-79; paper p. 402, 407 "division bias"). A spell of unemployment inside the year lowers hours and earnings and leaves the hourly wage roughly unchanged, so a job loss is *not a wage shock* in BPS's measurement; it is hours variation. The wage residual regressions (`residual_measures.do` l. 127-128 head, l. 176-178 wife) are the only inputs to the shock variances (`variance_estimation.do` l. 108-161 uses `duw2`, `duww2`, `duw_lag`, `duww_lag`, `duw_duww` and lags only). Two further trims remove what a job loss leaves in the data: observations with a wage below half the state minimum wage are set to missing (l. 51-52), and for every log variable the year with an extreme change followed by a reversal (bottom 0.25 percentile of Delta log x_t x Delta log x_{t-2}, by year) is set to missing (l. 85-107; paper fn 16). A one-year earnings collapse that recovers is exactly such a "jump". |
| 2 | Keeps only continuously working husbands; drops households after any family-composition change (`psid_sample.do` l. 83-91); drops SEO (l. 196) | **Correct on substance; two refinements** | (a) The continuous-employment rule is in `prepare_bootstrap.do` l. 66-69, not `psid_sample.do`: `no_work_d = (hours==0 | oly==0)`, plus `psample==0` (transfer eligibility at least twice earned income, from the tax code), then `egen todrop = max(no_work_d), by(person)` and `drop if todrop==1`: the whole history of a husband with one year of zero hours or zero earnings is dropped ("keeping households where the prime earner is always working"). It is annual: a husband unemployed for part of a year stays. BPS say it drops about 10% of male-head observations (p. 400); Table 1 cols 1 vs 3 show 10,479 vs 11,638 observations and sd(Delta log Y1) 0.513 vs 0.534. (b) The composition break (`psid_sample.do` l. 88-90: `break_d = (fchg>1)`) breaks on changes to head or wife (PSID family-change codes 2 and above: wife left or died, new wife, etc.), not on births or children leaving (code 1). So the break is on separation, which is one of Paper A's responses to the job loss (still with wife -4.5 pp Black, -1.9 pp White over years 1-3). Couples whose job loss ends the marriage are kept up to the year before the break and the later years are re-identified as a new unit (l. 127-152). SEO dropped at l. 196 (`keep if seo==0`), and the Latino and immigrant samples at `psid_individual.do` l. 34 and fn 15; so there is almost no Black sample and race enters only as control dummies. |
| 3 | `residual_measures.do` partials out levels and changes in both spouses' employment/unemployment status before estimating shocks, so a joint job loss is absorbed as an observable | **Correct for consumption and earnings; not for wages; one labelling detail** | Lines 88-90 (consumption), 101-103 (head earnings), 114-116 (total earnings), 159-161 (wife earnings) include `empl unempl retir w_empl w_unempl w_retir`, their two-year changes `dempl dunempl dretir dw_empl dw_unempl dw_retir`, and each level interacted with year (`_IempXyea_*` etc.). The PSID codes behind them (ER13205 etc.: 1 working now, 2 only temporarily laid off, 3 looking for work/unemployed) are reordered at `psid_interview.do` l. 156-187, so the code's `unempl` is "temporarily laid off" and its `retir` is "looking for work, unemployed"; the names are off but both statuses, for both spouses, levels and changes, are partialled out. Status is at the interview (spring), so a spell that ended before the interview is not captured. The two statuses enter additively, so any extra effect of the *joint* state beyond the sum of two main effects stays in the residual, but that is a few observations. The wage regressions (l. 127-128, 176-178) carry no status controls, and the wife's participation probit (l. 134-140) carries the husband's status levels. |
| 4 | Biennial first differences cannot see a monthly coincidence or the six-month build-up of added work | **Correct; add the arithmetic and the Table 7 point** | All moments are two-year differences (`l2.`), ages 30-57, waves 1999-2009, 7,295 household-year observations in the preference step (Table 4). A joint loss in 0.5% of couple-years (PSID: she is displaced in 10.2% of the years he is, he in about 5%) that halves both annual earnings adds about 0.003 x 0.25 = 0.0008 to cov(Delta y1, Delta y2); BPS's data moment is 0.0028 with s.e. 0.0042 (Appendix Table 1). It is invisible at their sample size. BPS's extensive-margin added-worker regression (Table 7; `tables_7_8_9.do` and p. 420) is the two-year change in the wife's participation on the husband's instrumented wage growth: by construction it is the *net* change (entries minus exits, including wives who lost their own job), which is Paper A's gross-versus-net point (gross +47 h, offset -35**, net about zero). |
| 5 | Most of BPS's "family labor supply insurance" is the passive second-earner share s = 0.71 (earnings fall 7.1%, not 10%), exactly the buffer a joint loss removes | **Needs correcting.** The passive share is *outside* BPS's 63/20/17 accounting | p. 425: a 10% permanent fall in the husband's wage lowers consumption by 7.1% with fixed labor supply, no savings and no transfers (that is 1 - s = 0.29 absorbed passively); 6.3% with taxes and transfers; 5.8% with his own response; 3.9% with the added-worker response; 3.2% with savings. The "39 percentage points insured" are 7.1 minus 3.2, so the 63% (25 pp) is the *behavioral* family response, driven by the wife's Marshallian cross-elasticity to his wage of -0.75*** (Table 5), with 20% (8 pp) government and 17% (7 pp) savings. The passive share (2.9 pp of the 10 pp shock) is the single largest buffer if one counts from 10 (43% of the 6.8 pp smoothed; the active family response 35%, government 12%, savings 10%), but BPS take it as the baseline. The correct statement for Paper A: a joint loss removes *both* the passive share and the behavioral response, and BPS's accounting counts only the second. |

### 2.2 What the lead's list misses

1. **UI is absent from BPS's T(.).** `tax_rate_estimation_snap.do` builds federal income tax, the EITC by number of
   children and Food Stamp eligibility (gross-income test at 130% of poverty, net-income test, 20% earned-income
   deduction, no asset or shelter deduction), then regresses log after-tax on log before-tax family earnings by year
   (non-eligible) or by number of children (eligible) to get chi and mu (eq. 6; paper p. 403-404, R^2 0.93). No
   unemployment insurance, no payroll tax, no state tax. UI is the first insurer of a job loss and the program Paper
   A's counterfactual (ii) varies. The function is also log-linear in *positive* earnings: the state in which no one
   earns, where Paper A's EITC-versus-SNAP ranking lives, is outside its domain. In BPS the EITC appears as a negative
   marginal tax rate at low earnings (Figure 1), that is, as *more* insurance for a household that still earns.
2. **Transitory shocks are assumed fully smoothed (fn 10), while BPS's own pi says the young cannot smooth.** pi is
   assets_{t-2}/(assets + human wealth) with human wealth projected to 65 at r = 2% (`pi_s_estimation.do` l. 5-7,
   337-349): E(pi) = 0.15, 0.03 at 30, 0.36 after 55 (Figure 3). pi governs the response to *permanent* shocks only;
   transitory shocks affect consumption only through nonseparability. BPS acknowledge that the negative kappa_{c,u}
   may hide liquidity constraints (p. 412-413, conclusions p. 433). A joint loss is a transitory earnings shock to a
   household with pi near zero and a borrowing limit; the approximation assumes it away.
3. **The trace of the joint shock is in BPS's Table 3.** The transitory wage-shock covariance across spouses is
   0.0058** (all ages), a correlation of 0.0058 / sqrt(0.0275 x 0.0125) = 0.31; the permanent covariance 0.0027 is a
   correlation of 0.08 and not significant. BPS read the transitory covariance as spouses "in sectors, occupations,
   or even firms subject to similar aggregate shocks" (p. 412): Paper A's channel, at annual frequency, after the
   trims. The lead's note quotes the permanent 0.0027 n.s.; the number to cite next to Paper A's contemporaneous
   component is the transitory one. (PSID: permanent couple component 0.020** vs contemporaneous 0.033**; the same
   ordering.)
4. **BPS's untargeted hours moments show what the model lacks.** Appendix Table 1 bottom: E(Delta h1^2) model
   0.0822 vs data 0.1315; E(Delta h2^2) 0.2524 vs 0.3517. The model explains 63% of husbands' and 72% of wives'
   two-year hours-growth variance. The rest is hours variation unrelated to wage innovations after the status
   controls and the ME calibration (23% of hours variance is assigned to measurement error from Bound et al. 1994,
   `T4C1.do` l. 37-39): that is where within-year spells live.
5. **The wife's extensive margin is outside the main moments.** `wife_employed = log_ww != .` (`prepare_bootstrap.do`
   l. 125): a wife with zero annual hours has no wage and no earnings residual; female moments condition on working
   in t and t-2 (`variance_estimation.do` l. 34-49). The baseline (fix_var = 10) has no selection correction; the
   Heckman version (Table 6 col 4, mortgage dummies as exclusion) changes nothing because participation is 80%.
   Wives who enter after a shock appear only in Table 7, at the two-year horizon.
6. **Extensive-margin complementarity.** Table 8 (conditional Euler equations): consumption rises with the wife's
   participation (0.388**) and falls with her hours (-0.241**); BPS explain it by fixed costs of work (p. 422). For
   Paper A this means a joint loss lowers consumption through income *and* through the end of two work-related
   expenditure flows; a work cost in consumption units in the model produces both signs.
7. **Sample period and scope.** Six waves 1999-2009 (income years 1998-2008); no advance-information effect (test
   p = 0.29); unitary household; hours freely adjustable (BPS list adjustment costs as a reason their family-insurance
   role would be "even more prominent", p. 433). Paper A's PSID joint-loss evidence runs 1984-2021 and the CPS
   1994-2023, and the PSID excess rises across periods (0.027 n.s. in 1984-89, 0.095*** in 2000-21).

### 2.3 The reconciliation in one paragraph (for the paper)

BPS and Paper A measure different objects in the same survey. BPS take married couples with a husband who has
positive hours and earnings in every year, drop the years around a change of spouse, drop the SEO, remove each
spouse's interview-week employment and layoff status (levels and changes) from consumption and earnings, drop the
observations with a collapse-and-recovery in earnings or hours, define the wage as annual earnings over annual
hours, and estimate from two-year differences how hourly-wage innovations pass to hours and consumption. In that
design a job loss is not a wage shock; what survives of it is hours variation that the model does not target and
under-predicts by 30-40%. Their conclusion, that family labor supply, taxes and transfers, and savings exhaust the
insurance against permanent wage shocks, is about the continuously employed. Paper A looks at the shock that design
removes, at monthly frequency, in the state (no earner) that BPS's tax function cannot represent, and finds that the
second earner's job ends with the first's. The two are consistent: BPS's own transitory wage-shock covariance (a
correlation of 0.31) and their result that for Food-Stamp-eligible households 71% of insurance is government (p.
426) are the annual, trimmed shadows of Paper A's joint loss and of its SNAP result.

### 2.4 A quantitative tension the model must resolve

BPS's Marshallian cross-elasticity of the wife's hours to a permanent fall in the husband's wage is -0.75*** (Table
5). The permanent part of a displacement in Paper A is a wage loss of about $6-7k a year six years on (15-20% of
pre-displacement labor income). Applied literally, BPS predict wives' hours up 11-15%, about 190-250 hours on a base
of 1,700; Paper A measures +51 (all), +97 gross for mothers of children under six, with the joint losses offsetting
35. BPS over-predict the added work after a displacement by a factor of two to four. Candidates, all in Paper A's
model: the joint loss itself (removes a third of the gross response), the search friction (employment of
non-employed wives builds over six months), UI crowd-out (Cullen and Gruber 2000), and the transitory part of his
loss (hours recover in four to five years), to which BPS find no extensive-margin response (Table 7, theta_0 =
0.002). The "one model, both answers" test should show the model giving about -0.75 on BPS's sample (interior hours
of continuously working wives responding to permanent wage changes) and +50-100 hours after a displacement on the
full sample.

---

## 3. What Paper A's model must contain for "one model, both answers"

The earlier memo's design (monthly, two earners, three-part displacement risk, search friction, human capital levels
with accumulation, depreciation and a displacement loss, UI/SNAP/EITC, separation hazard, savings) stands. Four
additions make BPS's estimator runnable on the simulated data; nothing else changes.

### 3.1 Keep from BPS (so their moments are not zero by construction)

| BPS feature | Form in Paper A's model | Cost | Why |
|---|---|---|---|
| Correlated permanent and transitory hourly-wage shocks for both spouses (eqs. 1-3) | The human capital level of each spouse already carries the persistent component; make its innovations stochastic (a 7-point grid per spouse instead of 4) with a shared innovation across spouses (the companion's 2026-10-15 decision: shared, persistent plus transitory). Transitory shocks iid, drawn each month, not a state. | State space from 1.4 x 10^5 to about 4 x 10^5 points per month; still seconds per solve | Without wage innovations BPS's wage-variance step returns zeros and nothing downstream runs. A bounded grid is not a unit root; at a 30-57 horizon it is close enough if the grid is wide; say so. |
| Intensive margin for both spouses | Her hours: 0 / part-time / full-time (the companion's own part-time code shows the form). His: full-time / part-time / none with employment exogenous given a job but a hours choice when employed, or a 2-point hours choice. | Choice set 2x-3x; fine | BPS identify everything from the intensive margin; a binary her and an exogenous him produce no Frisch elasticities. Discrete hours give the signs and the decomposition, not the exact elasticities; promise the former. |
| Progressive T(.) with EITC and SNAP on annual family earnings (eq. 6) | Already planned as schedules; pay the EITC on annualised earnings (earlier memo, Sec. 2.4) and report the chi, mu fit of the simulated schedule as BPS do (their R^2 is 0.93) | none | Needed for the 20% government share and for BPS's tax-adjusted Frisch step; the UI counterfactual then shows what BPS's T(.) leaves out |
| Nonseparability | Minimal: a fixed cost of work in consumption units per employed spouse (produces Table 8's extensive-margin complementarity) and nothing else at first (parsimony). Leisure complementarity of spouses (eta_{h1,w2} = 0.16, eta_{h2,w1} = 0.33) is a known BPS feature the model does not target; report the miss. | none | |
| Assets with a borrowing limit; pi by age | Already planned; the untargeted check is pi(age) = assets/(assets + human wealth) against Figure 3 (0.03 at 30, 0.15 mean, 0.36 after 55) | none | pi is what makes the young unable to smooth; the model must get it right to produce both BPS's permanent-shock response and the joint-loss consumption drop |

### 3.2 Add (Paper A's own objects; already in the earlier memo)

Displacement hazard with an individual part, a common same-month part larger for same-sector couples, and a
permanent couple type; a search friction for both spouses (his job finding calibrated from CPS/SIPP male flows, hers
estimated); a human capital loss at displacement; UI with duration and per-spouse eligibility; SNAP floor; EITC
schedule; a separation hazard elevated after his job loss; child-age work cost; the child block outside the
estimation.

### 3.3 Period

Monthly, as in the earlier memo. BPS's two-year differences are produced by aggregation; nothing about their
estimator needs a longer period. Quarterly remains the fallback if compute binds.

### 3.4 Running BPS's estimator on simulated data (protocol)

1. Simulate the estimated model: about 50,000 couples, monthly, wife's ages 25-60, husband's age from the PSID
   couple distribution; calendar years labelled 1998-2008 so BPS's hard-coded tax schedules and year dummies apply.
2. Aggregate to a PSID-shaped household-year panel with BPS's variable names: `ly`, `wly` (annual earnings), `hours`,
   `hourw` (annual hours), `totcons` (annual consumption), `tot_assets3` (start-of-year assets), `empst`, `wempst`
   (status in a spring month: working now / temporarily laid off / looking for work), `fsize`, `kids`, `educ`,
   `weduc`, `race`, `state` (random or single), `marit`, `age`, `agew`, `fchg` (2 or more in the year of a
   separation), `year` in BPS's 98-108 coding, `seo = 0`, `mortgage1`, `mortgage2` (for the selection probit's
   exclusion; can be zero), `tyoth`, `outkid`, `smsa`.
3. Add measurement error with BPS's calibrated shares (earnings 4%, hours 23%, wages 13% of the log variance, with
   the earnings-hours error covariance they imply; `T4C1.do` l. 37-39, Appendix 3) and a consumption error whose
   variance reproduces E(Delta c_t Delta c_{t-2}) = -0.0332. Without the error, BPS's ME correction over-corrects.
4. Keep odd waves only (biennial), then run, unchanged, `psid_sample.do` (from line 80), `prepare_bootstrap.do`,
   `residual_measures.do`, and `bootstrap.do` with `bn = 0` (point estimates; it calls
   `tax_rate_estimation_snap.do`, `pi_s_estimation.do`, `variance_estimation.do`, `frisch_estimation.do`), then the
   decomposition of eq. (11) and `tables_7_8_9.do` Table 7 regressions. StataMP is installed; a run is minutes.
5. Compare with BPS: Table 3 (variances and covariances by age group; the all-ages transitory covariance 0.0058 and
   permanent 0.0027), Table 4 col 1 (E(pi) 0.150, E(s) 0.708, eta_{c,p} 0.42, eta_{h1,w1} 0.68, eta_{h2,w2} 0.96,
   signs of the cross-elasticities), Table 5 (Marshallian: male own -0.08, female own 0.42, female hours/male wage
   -0.75, consumption/male wage 0.32), the insurance accounting (63/20/17; beta = -0.14, s.e. 0.27), Table 7 (theta_1
   = -0.168, theta_0 = 0.002), and the untargeted hours moments.
6. On the full monthly simulated sample compute Paper A's moments through the same definitions as the data scripts
   (earlier memo, Sec. 2.4) and reproduce the joint-loss facts.

**Pass criterion.** BPS's wage variances and covariances within their standard errors; the decomposition shares
within about 10 pp; beta within its standard error; Table 7's theta_1 within its standard error; signs of the
own and consumption-wage elasticities. State in advance what is not expected to match (spousal leisure
complementarity; exact Frisch magnitudes with discrete hours).

**What the test buys.** If the model passes, Paper A can write: "estimated on the joint-loss moments, the model
reproduces BPS's estimates on a BPS-style sample of its own simulated households; the difference between the two
papers is the sample, the residualisation and the frequency, not the economics". If it fails on a named moment, the
failure is informative (for example, a 63% family share that the model cannot produce without BPS's trims).

---

## 4. Empirical reconciliation to do before the model

All data are on disk: `Dropbox/PSID/Family/fam1999er` to `fam2009er` (and to `fam2023er`), `wlth1999`-`wlth2007`
(wealth is inside the family file from 2009), `Individual/ind2023er`. BPS's `psid_interview.do` expects Stata family
files named `f99`, `f01`, ..., `f09`, `faminc99` and `ind6809`; the local folders hold the PSID text files with their
setup do-files, which produce the .dta in minutes. StataMP-64 is installed, and the GMM step needs only Stata 11+
and BPS's ado files (`ivreg2` only for Table 8). The replication package is the AEA's public one; the PSID public
files are the licence the repo already uses. Write outputs to a repo folder (`bps_reconciliation/` with the
do-files copied and edited, logs and a results markdown), nothing to Dropbox.

### 4.1 Step 0: replicate BPS as shipped (1999-2009)

Run `shell.do` end to end with `bn = 0`. Target: Table 3 and Table 4 col 1 to the third decimal; the 7.1 / 6.3 / 5.8
/ 3.9 / 3.2 chain; N = 7,295. This validates the pipeline before anything is changed. 2-3 days (file conversion,
paths, one or two Stata-version fixes).

### 4.2 Step 1: relax one restriction at a time (1999-2009, no new variables)

| Variant | Edit | Prediction (to be tested, not assumed) | Report |
|---|---|---|---|
| A. Husbands with a year of zero hours kept (observation-level drop instead of person-level) | `prepare_bootstrap.do` l. 68-69: drop the year, not the person | Wage moments unchanged (no wage without hours); earnings and consumption residual variances rise; cov(Delta c, Delta y1) rises; the family-labor-supply share falls, the government share rises | wage covariances; eta's; the 63/20/17 split; beta |
| B. Employment and layoff status controls removed from the residual regressions | `residual_measures.do` l. 88-90, 101-103, 114-116, 159-161: drop `empl ... dw_retir` and the `_IempXyea_*` etc. terms | E(Delta y_j^2) and cov(Delta y1, Delta y2) rise; cov(Delta c, Delta y) rises; the estimated consumption response to "transitory" shocks rises; beta moves toward "less insurance" | same |
| C. Jump trim off | `prepare_bootstrap.do` l. 85-107 skipped (keep the half-minimum-wage rule) | Transitory variances and the transitory covariance rise; permanent covariance unchanged | Table 3 |
| D. Composition breaks off except divorce | `psid_sample.do` l. 88-90: break only on `fchg` codes that change the spouse (already the case; check) or keep the break year | Small | Table 3-4 |
| E. SEO in, with and without weights; by race | `psid_sample.do` l. 196 | Higher transitory variances, lower pi, larger government share (BPS's Food-Stamp group: 71%) | Table 3-4 by race, the split |
| F. All of A-E | | | the "BPS without restrictions" column |

Each variant is a one-line edit and a rerun: about one day each including checks; one week for the block.

### 4.3 Step 2: displacement and joint displacement inside BPS's panel (1999-2009)

Merge the husband's and the wife's displacement flags from `IGE/19.FatherDisplacement.py` and
`IGE/25.JointJobLoss.py` by (wave, interview number) into `data4estimation` (BPS's `id` is the interview number of
the wave; the repo scripts key on the same pair). Then:

1. Means of BPS's residuals (`uc`, `uy`, `uyw`, `uw`, `uww`) in the two-year difference containing a husband's
   displacement, a wife's displacement, and a joint displacement, with and without the status controls (variant B).
   This is Paper A's food event study (single -$419, joint -$699, difference n.s. on 119 events) redone with BPS's
   full consumption measure and their residualisation.
2. BPS's wage and earnings covariances with displacement couple-years excluded, then included: how much of the
   transitory covariance (0.0058) is carried by displacement years.
3. Table 7's theta_1 split into entries and exits (gross and net), the BPS-metric version of Paper A's Section 5.3.

About one week.

### 4.4 Step 3 (optional, more power): extend to 2011-2021

`psid_interview.do` hard-codes about 100 ER variable names per wave; six new waves need the mapping (consumption
items, assets, hours, earnings, status mentions, `fchg`, state, demographics) and the tax schedules for 2010-2020 in
`tax_rate_estimation_snap.do`. One to two weeks. It roughly doubles the displacement events and overlaps with Paper
A's displacement sample; it also tests BPS's year-stationarity assumption, which they note was "not strong" for
1999-2009 (p. 392). Do it after Steps 0-2, if the joint-displacement cells in Step 2 are too thin.

### 4.5 What to report (one table in Paper A, Section 5 or the reconciliation subsection)

Rows: BPS baseline (replicated), A, B, C, E, F, F + displacement years excluded. Columns: sigma_{u1u2} and
sigma_{v1v2} (with correlations), E(pi), eta_{c,p}, the consumption response to a 10% permanent male wage shock, the
family / government / savings shares, beta, N. Stars and p-values on every estimate; bootstrap SEs from BPS's own
block bootstrap (`bn = 200`) only for the final two columns, to save time.

---

## 5. How to write it in Paper A

### 5.1 Introduction (one paragraph, after the added-worker paragraph)

"Blundell, Pistaferri and Saporta-Eksten (2016) find that family labor supply is the main insurance against a
husband's permanent wage shocks and that, with taxes, transfers and savings, little insurance is missing. Their
estimates are for continuously employed husbands, from hourly-wage innovations, net of both spouses' employment
status, at two-year frequency; a job loss is not a wage shock in that design, and the state in which no one earns
is outside its tax function. This paper measures the shock that design removes and the state it cannot represent.
Section [reconciliation] shows that the two sets of findings are consistent: reproducing their estimates on their
sample rules and ours on the full sample from one model."

### 5.2 Literature table (`sec2_literature.tex`, Table 1): one new row

| Finding | Prior evidence | This paper |
|---|---|---|
| Family labor supply insures permanent wage shocks of continuously employed husbands (63% of the behavioral insurance); no missing insurance; spouses' transitory wage shocks correlated (0.31) | BPS (2016), PSID 1999-2009 | Known. New: the job loss their sample, trims and residualisation remove, measured monthly; the no-earner state; one model that reproduces their estimates on their rules and the joint loss on the full sample |

And in the "Insurance within the household" paragraph, replace "family labor supply is a main channel of insurance
against permanent wage shocks" with the one-sentence version of Section 2.3 above, and move the detailed comparison
to the reconciliation subsection (one subsection per topic; details in footnotes).

### 5.3 A reconciliation subsection (in Section 5, after the gross-and-net subsection, or as Section 5.7)

Title: "Why this differs from estimates of family insurance against wage shocks". Content: the one-paragraph
reconciliation (2.3), the table of Section 4.5, and footnotes carrying the code references (file and line) for each
of the five design features, the UI omission, the transitory covariance (0.31), and the untargeted hours moments.
Keep it to one page; the footnotes carry the detail (PI rule).

### 5.4 What the model section should promise (`sec7_model.tex`)

Add one paragraph under Estimation: "Validation against BPS. The estimated model is simulated, aggregated to
biennial household-years, trimmed and residualised with BPS's own code, and their estimator is run on it. The model
is expected to reproduce their wage-shock variances and covariances, the signs of their elasticities, their
insurance accounting and their extensive-margin added-worker effect within their standard errors; on the full
sample it reproduces the joint-loss facts. Spousal leisure complementarity is not modelled and is reported as the
known difference." Promise the decomposition and the covariances, not exact Frisch elasticities.

### 5.5 Three sentences not to write

- "BPS treat the second earner's job as given" is true but incomplete; write what their design does (status
  controls, continuous employment, trims) and that their transitory covariance already contains the shadow of the
  joint shock.
- "Most of BPS's family insurance is the passive share" is wrong in their accounting (Section 2.1, point 5).
- "BPS find no role for the government" is wrong: 20% overall, 71% for Food-Stamp-eligible households, which is
  Paper A's SNAP point in their words; cite it.

---

## 6. Numbers to carry (BPS, for the paper and the test)

Sample: PSID 1999-2009, non-SEO, no immigrant or Latino samples, married male heads 30-57, continuous positive
hours and earnings, assets below $20M, transfers below twice earnings, jumps trimmed; 10,479 household-years
(Table 1), 7,295 in the preference GMM (Table 4). Wage shocks (all ages, Table 3): males sigma_u^2 0.0275***,
sigma_v^2 0.0303***; females 0.0125**, 0.0382***; covariances transitory 0.0058** (rho 0.31), permanent 0.0027
(rho 0.08, n.s.). Preferences (Table 4 col 1): E(pi) 0.150, E(s) 0.708, eta_{c,p} 0.417, eta_{h1,w1} 0.681,
eta_{h2,w2} 0.958, eta_{c,w1} -0.162**, eta_{h1,w2} 0.159**, eta_{h2,w1} 0.325**; outside insurance beta -0.137
(0.270). Marshallian (Table 5): male own -0.08, female own 0.42***, female hours to male wage -0.75***, consumption
to male wage 0.32***. Insurance accounting (p. 425): 10% permanent male wage fall, consumption 7.1 / 6.3 / 5.8 / 3.9
/ 3.2%; of 39 pp, 20% government, 63% family labor supply, 17% savings; Food-Stamp-eligible group 7.2 / 3.6 / 2.3 /
2.1%, 71% government. Extensive margin (Table 7): +1.68 pp participation per 10% permanent fall (theta_1 -0.168*,
s.e. 0.087); no response to transitory shocks (0.002, s.e. 0.030); earnings fall 8.9% instead of 10%, consumption
6.5% (p. 428). Conditional Euler (Table 8): wife's participation +0.388**, wife's hours -0.241**. Untargeted
(Appendix Table 1): E(Delta h1^2) 0.082 model vs 0.132 data; E(Delta h2^2) 0.252 vs 0.352; cov(Delta y1, Delta y2)
0.0025 vs 0.0028 (s.e. 0.0042). Measurement-error shares: earnings 4%, hours 23%, wages 13%. pi: 0.03 at 30, 0.36
after 55; r = 2%, retirement 65. No advance information (p = 0.29).
