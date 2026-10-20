# BPS reconciliation, Steps 0-2 done: what the results say, what to change in Paper A, next steps (2026-10-18)

Read, nothing edited or run except this file: `IGE/bps_reconciliation/bps_reconciliation.md` (all tables S0-S2),
`README.md` (edits and caveats), `tables/`, Paper A as now written (`sec1_introduction.tex` par. 2,
`sec2_literature.tex` "Why another paper after BPS", `appD_bps.tex`), my two earlier memos
(`fable_bps2016_paperA.md`, `fable_model_choice_paperA.md`). Numbers below are from the results file unless marked
BPS (their paper).

---

## 0. What the results establish (and what they do not)

| Claim | Status after Steps 0-2 | Evidence |
|---|---|---|
| BPS replicate | Established, exactly | Table 3 all 36 cells; Table 4 cols 1/4/5 to the third decimal; chain 7.09/6.33/5.79/3.88/3.16; split 19.4/62.3/18.3; FS group 70.6% government |
| Status controls absorb the joint loss (my memo, point 3; the lead's point 3) | Right at the event, irrelevant for the accounting | Wife-only displacement, wife's earnings residual at k=0: -0.101 (p=0.10) with the controls, -0.202*** without; joint: -0.186 vs -0.299*. The split moves by less than one point because the events are 3-4% of couple-years |
| The continuous-employment rule overstates the family share | Established, modest | 0.62 -> 0.56 (government 0.22, savings 0.22); BPS themselves flag this risk (BPS p. 403) |
| SEO / low-income sample | Established: family share rises (0.68; 0.70 weighted), E(pi) 0.14; White couples 0.52/0.21/0.27; Black preference step not identified (N = 1,625) | Table S1 |
| Composition break | Changes nothing (8 household-years); separation after a wife's displacement +2.9 pp** (p = 0.033), after a joint one +6.5 pp (4 events, p = 0.15), after the husband's +1.0 pp (p = 0.26) | Tables S1, S1e |
| The trims | The estimator is fragile to them, but they do not remove job-loss years | Jump trim off: sigma2_u1 0.028 -> 0.056, preference step collapses; min-wage trim off: family 0.70. Attrition Table S2.2: the two trims remove 7 husband-displacement rows, 1 wife, 0 joint, out of 414 / 288 / 28 |
| The transitory wage covariance is the shadow of the joint shock (my memo, point 2.2.3) | Wrong; correctly dropped from the paper | 0.0063** without displacement years, 0.0054** without joint ones; joint years raise the *earnings*-residual covariance instead (+0.193**, p = 0.019) |
| Joint displacement is rare and attrits | Established | 0.30% of couple-years (28); 57 -> 28 -> 17 with a wage moment; SEO drop 14, missing t-2 11, no-work rule 5, education 4, composition 5, trims 0 |
| Consumption falls more after a joint than a single displacement | Suggestive only | Same interval: +0.071 (p = 0.43), wrong sign. Next interval, joint minus single: -0.071 (p = 0.19) BPS sample; -0.138** (p = 0.027) SEO in; -0.134** all relaxations; raw log change -0.088 (p = 0.11) / -0.124** / -0.122**. 17-23 events |
| BPS's added worker is entries | Established and useful | theta_1: entries -0.159** (0.064), exits -0.009 (0.058) |
| A joint displacement lowers entries (-0.115**) | Partly mechanical; do not headline | BPS's participation is positive annual earnings; a wife displaced mid-year still "participates" that year, and the "minus exits" coefficient on joint years is positive (+0.049; +0.082** with SEO), i.e. fewer exits, which shows the annual indicator cannot represent a job loss |

The two corrections to my earlier memo: the transitory wage covariance is not the trace of the joint shock, and the
status controls matter at the event but not for the accounting. Both strengthen the reconciliation's real content:
the joint loss lives in hours and earnings, not hourly wages, it is rare in a biennial panel of stable, continuously
employed couples, and BPS's averages cannot see it.

---

## 1. Is the reconciliation as written correct and convincing? What to change

**Substance: correct, with four places where the text goes beyond the tables and one where it invites a rebuttal.**

1. **The trims sentence invites BPS's reply and is contradicted by the appendix's own attrition table.** The intro
   says the result "is robust to most of their sample restrictions"; sec2 then says "It rests on the trims of wage
   and earnings observations: without the trim of years of collapse and recovery ... the preference step breaks
   down", and the appendix says "The estimates rest on the two trims". A reader infers that the trims remove the
   job-loss years. Table S2.2 shows they remove 7 husband and 0 joint displacement rows. BPS would reply, correctly,
   that the 0.25-percentile trim is a standard treatment of measurement error (their fn 16; BPP 2008 do the same)
   and that any second-moment estimator in two-year wage growth needs it. What the trim result shows is that BPS's
   estimator is fragile to a handful of extreme observations, which is a property of covariance-based estimators,
   not of job loss. Change: delete the trims from the intro; in sec2 reduce to one clause ("the estimates are
   sensitive to their trimming of extreme wage and earnings changes, which affects a tenth of a percent of
   observations and none of the displacement years"); keep the full result in the appendix with that framing.
2. **The consumption result is in the intro as "13.8 log points, p < 0.05" and cannot carry that weight.** It is
   the next two-year interval only (the same-interval estimate has the wrong sign), one of five samples (p = 0.19 in
   BPS's own sample), on 17-23 events. Change: in the intro, one clause ("and the few joint displacements in their
   panel show consumption falling more than after a single displacement in the following interval, imprecisely");
   in sec2 and the appendix report k=0 and k=+1 side by side for all samples with the event counts, and say
   "suggestive" explicitly. Better: get the number from Paper A's own data (Section 4, step 2 below), where the
   events are three times as many.
3. **The Marshallian comparison (-0.75 -> 190-250 hours vs 51-97) needs its caveats and its extensive-margin
   counterpart.** BPS's -0.75 is the response of hours of wives who work in both years to a permanent change in
   the husband's hourly wage with his employment continuous; Paper A's +51 is all wives, with the husband's hours
   also falling temporarily. Say "an order-of-magnitude comparison" and add BPS's own extensive-margin number,
   which is comparable to Paper A's monthly flows: BPS predict 8.4% of non-working wives entering after a 10%
   permanent fall (BPS p. 428), so 13-17% after a displacement's 15-20% permanent loss; the CPS and SIPP show
   +4.2 pp after three months and +5.4 pp after six, i.e. about a third of that.
4. **The separation point is conceptual, not quantitative, and the intro presents it as a driver.** Variant (e)
   changes nothing; 38 of 327 separating couples had a prior displacement; the husband's displacement does not
   raise separation significantly in their panel (+1.0 pp, p = 0.26), only the wife's (+2.9 pp**). Change: keep
   one sentence in sec2 ("their design ends a couple's record at a separation, so the marriage channel of
   Section 5 is outside it; in their panel a separation follows a wife's displacement 2.9 points more often"),
   drop it from the intro.
5. **Three tellings.** The intro's second paragraph (35 lines on another paper), sec2's "Why another paper after
   BPS" (60 lines) and Appendix D repeat each other. PI rule: one subsection per topic, details in footnotes. Cut
   the intro to 6-8 lines: BPS's finding; what their design measures (wage innovations of continuously employed
   husbands, two-year changes, positive-earnings tax function, no UI); the one-sentence reconciliation; the model
   promise. Keep sec2 as the one full telling, corrected as above, and move the sentences that use Paper A's own
   numbers (the hours comparison, the marriage channel, EITC at zero earnings) there. Appendix D becomes tables.
6. **Appendix D has no table.** A referee wants three: D1 relaxations (rows: baseline, no immigrants, (a), (b),
   (c) jump, (c) min-wage, (d) SEO, (d) White, (e); columns: sigma_u1u2 and its correlation, sigma_v1v2, E(pi),
   eta_c,p, kappa_c,v1, the three shares, beta, N; stars and p-values); D2 the displacement event study (joint vs
   single, k=0 and k=+1, husband's earnings, wife's earnings arc, consumption residual and raw, for the BPS
   sample, SEO in and all relaxations, with event counts); D3 attrition of the 57 joint and 692 husband
   displacements by restriction. All exist in `bps_reconciliation.md`; it is formatting.
7. **Quote BPS's own caveat.** BPS p. 403: dropping males with long unemployment spells "may understate the
   importance of added worker effects ... or overstate it". Paper A quantifies it (0.62 -> 0.56). Writing it this
   way turns the reconciliation from a critique into a measurement, which is how a referee who knows BPS will
   read it most favourably.
8. **Small accuracy points.** (i) "half of the joint displacements never reach it": 28 of 57 reach, 17 carry a
   wage moment; say both. (ii) The 1997 immigrant refresher: keep in the appendix footnote only. (iii) Standard
   errors: say where the dagger (second-step GMM) applies. (iv) "Black preference step not identified": say the
   sample is 1,625 household-years and leave it. (v) The sec2 sentence "Read at face value, the wife is the
   household's main insurer; this paper finds that, against job loss, she largely is not" is fine; the next
   sentence should say in what sense ("in the month of the shock and for couples who share a workplace"), since
   Section 5 also reports +97 hours for mothers of young children.

**Convincing to a referee once changed:** yes. The strong parts are the exact replication, the no-work and SEO
variants, the attrition of joint displacements through their restrictions, the earnings-not-wages finding (+0.19 on
the earnings covariance, nothing on the wage covariance) and theta_1 as entries. These make the point that the two
papers measure different objects without claiming BPS are wrong about theirs.

---

## 2. Does this change the model plan?

The design in `fable_model_choice_paperA.md` and the BPS-nesting additions in `fable_bps2016_paperA.md` Section 3
stand. Six changes to the test, one addition to the model's measurement layer.

### 2.1 Measurement error must be in the simulated data, and it must have a fat tail

The trims are part of BPS's estimator and the estimator is fragile to them (jump trim off doubles sigma2_u1). In
the PSID the trimmed observations are measurement-error outliers, not displacement years (Table S2.2). In a
simulation without measurement error the 0.25-percentile tail of Delta log x_t x Delta log x_{t-2} would be the
genuine collapse-and-recovery years, i.e. the displacements, and the trim would remove exactly the events the
test is about. So: (i) add measurement error to earnings, hours and consumption as a two-component mixture (a
common small error with Bound et al.'s shares, 4/23/13% of the log variance, plus a rare gross error, a few percent
of observations, large enough that the trimmed set is dominated by it); (ii) calibrate the mixture so that the
simulated panel reproduces two diagnostics from the PSID: the share of displacement rows among trimmed rows (about
the base rate, 7 of about 113 min-wage trimmed rows, 1 of about 41 jump-trimmed rows) and the ratio of the
transitory variance without and with the jump trim (0.056 / 0.028). Without (ii) the BPS-on-simulated-data
comparison is not like for like.

### 2.2 Pass criteria, revised

Keep: BPS's wage variances and covariances within their s.e.; the 63/20/17 split within about 10 pp; beta within
its s.e.; theta_1 within its s.e.; signs of the own and consumption-wage elasticities. Add, because the real data
now give the derivatives of BPS's estimates with respect to their restrictions, which a model that only matched the
baseline could miss:

| Derivative in the PSID | The model's BPS-style simulation must give |
|---|---|
| (a) no-work rule relaxed: family share 0.62 -> 0.56, government 0.19 -> 0.22, savings 0.18 -> 0.22 | the same direction and roughly the same size (this is the husband's long spells entering the moments) |
| (b) status controls removed: nothing in the accounting; wife's earnings residual at her displacement doubles | the same (a check that the model's job losses are rare enough) |
| (d) low-wealth / SEO-type couples in: E(pi) 0.15 -> 0.14, family share up | the model's Black and low-asset couples added to a White-SRC-type sample give the same direction |
| trims off: transitory variance doubles | reproduced through the measurement-error mixture (Section 2.1) |
| attrition: 57 joint displacements -> 28 in the sample -> 17 with a wage moment; BPS's no-work rule drops about 10% of male head observations | the simulated couples pass through the same filters with similar shares; the 10% requires husbands' spells that span a calendar year, a check on his search friction |
| P(wife displaced in the interval | husband displaced) 6.8% vs 2.9% in BPS's panel; 10.2% vs 3.9% per couple-year with both working (Paper A) | both, from the same shock process |
| joint displacement years raise E(du_y1 du_y2) by +0.19 and the wage covariance by nothing | the same: the joint loss is hours and earnings, the hourly wage moves only through the displacement loss of human capital |
| theta_1 is entries (-0.159), not exits (-0.009) | the same split on the simulated BPS sample |

Drop from the pass list: anything about the transitory wage covariance being carried by displacement years.

### 2.3 Consumption: target or validation, and how to align the years

The PI's rule (corrected 2026-10-18) is not "no consumption target" but "state the period and compare only with
simulated households of the same years": PSID expenditure covers 1999-2021, while displacement and hours moments
run from 1968/1984. On that basis:

**(i) The BPS-panel result (-0.138**, SEO in, 1999-2009, next interval, 17-23 events): validation only.** Its
same-interval estimate has the wrong sign, its significance depends on the sample (p = 0.19 in BPS's own), and a
moment with s.e. 0.06 on an effect of 0.14 would carry almost no weight in an inverse-variance SMM while making the
fit hostage to one specification. Keep it as the "in their own data" check, computed on the simulated BPS-style
panel with BPS's residualisation, as a sign-and-band check (about zero in the same interval, -0.07 to -0.14 in the
next).

**(ii) Paper A's own PSID 1999-2021 consumption event study: target it, in two parts.** (a) The fall in log
consumption after the husband's displacement (single), years 1-3 relative to the pre-displacement waves, pooled and
by race: hundreds of events, well powered, and the one moment that identifies how much of a job loss reaches
consumption, which is what every counterfactual is scored on; without it that response rests on the wealth
distribution target alone. No new parameter is needed (it disciplines the borrowing limit, the asset distribution
and the work cost), so the parsimony rule is met. (b) The joint-minus-single difference, with its own variance
weight, if its standard error is below about 0.08 (about 60-80 joint displacements in 1999-2021 should give
0.05-0.07); if larger, report it as validation next to the fit table. Inverse-variance weighting makes an imprecise
target nearly harmless, so the decision rule is about what the paper claims to fit, not about estimation risk.
(c) The wife's own displacement, as a third row, for the same reason as (a).

**Aligning the model with the years.** One simulation, moment-specific windows:
- Simulated couples carry a calendar year and a birth cohort, drawn as copies of the PSID couples (the companion's
  `sim_panel.py` design: every PSID couple with its wave pattern, observed as it is), with age-by-year inputs
  (husbands' earnings profiles, UI generosity by state and year from `IGE/12b`, EITC and SNAP parameters by year).
  The displacement and hours moments are then computed on simulated couple-years of 1984-2021 (annual waves to
  1997, biennial after), the consumption moments on simulated couple-years of 1999-2021 only, each moment's window
  written in the targets table. Cohorts take care of themselves: a couple observed in 2005 at 40 is born in 1965 in
  both data and simulation.
- Event time in waves, dated as in the PSID: a displacement is placed in the calendar year the job ended;
  consumption is what the household reports at the interview (spring of wave t+1 for income year t), so "year 1
  after" is the first interview after the job-end year. Apply the same rule to the simulated monthly panel
  (consumption in the interview month, annualised as the PSID items are) rather than the model's month-of-shock
  consumption. The monthly model will show the fall in the month of the joint loss; the biennial interview sees it
  one wave later, which is what Step 2's "next interval" result looks like. State this in the paper.
- The measure: BPS's nondurables plus services with the 6% rent equivalent (about 70% of CEX nondurables and
  services); use log changes in the event study so the coverage ratio cancels, and report the level ratio of model
  to PSID consumption once as a check.
- Measurement error in consumption: BPS identify it from E(Delta c_t Delta c_{t-2}) = -0.033; add the same
  variance to the simulated consumption before computing either moment, so the event-study s.e. and the
  attenuation match.

### 2.4 What else the model must contain (unchanged from the earlier memos, confirmed)

Discrete hours for both spouses (BPS's identification is intensive-margin; the Marshallian -0.75 on their sample
versus +50-100 hours after a displacement on the full sample is the central reconciliation number); stochastic
shared innovations to both human capital levels (so BPS's wage moments are not zero); a work cost in consumption
units (Table 8's extensive-margin complementarity); UI, SNAP, EITC schedules; the attrition filters as code. No
race-specific preferences; Black couples enter through hazards, inputs and wealth, and the BPS test runs on the
pooled non-SEO-type sample as BPS do, with the White-only subsample compared with the "(d) White" column
(0.52/0.21/0.27).

---

## 3. Is the 1999-2021 extension worth doing, and how

**Worth doing for Step 2 only (residuals, event study, attrition), not for re-estimating BPS's preference step.**
The gain is power on joint displacements (28 couple-years in 1999-2009; about 60-80 with the 2011-2021 waves), two
recessions (the CPS excess is 6.7 vs 3.6 pp in recessions), and overlap with Paper A's own displacement sample. The
preference step over 1999-2021 would be a different estimate (BPS assume year-stationary variances, which they
already call "not strong" for 1999-2009; 2008-09 and 2020 break it), would invite the objection that the comparison
no longer matches BPS, and needs the tax function for every year. Step 2 needs none of the tax parameters: the
residual regressions use consumption, earnings, hours, status, demographics, state and prices; the half-minimum-wage
rule needs state minimum wages; pi and the tax function are not used.

**Inputs for the Step 2 extension (1-2 weeks).**
- ER-variable mapping for `fam2011er`-`fam2021er`: consumption items as in `psid_consumption.do` (keep BPS's 1999
  item set so the measure is consistent; the 2005+ additions are excluded by BPS), rent and house value, hours,
  earnings, the three status mentions, `fchg`, state, age, education, race, family size, kids, mortgages, assets
  (for completeness). The repo already reads family files through the PSID setup do-files (`IGE/1.PSID.py`,
  `ReducedForm/1.PreparePanel.py`), so the mapping can be built in Python and written as the Stata variables BPS's
  code expects.
- Prices: CPI-U (BLS) to extend `price_indices.dta`; CPI detailed series only for Table 9, not needed.
- State minimum wages 2011-2021: the Vaghul-Zipperer state and sub-state minimum wage data set is already in
  `Dropbox/VaghulZipperer` (EPI, updated through the present); DOL's historical table "Changes in basic minimum
  wages in non-farm employment under state law" is the alternative.
- `psample` (transfer eligibility at least twice earnings) drops 7 observations in BPS; skip it in the extension
  and say so.

**If the preference step is ever extended (not recommended now), the additional inputs are:** federal brackets
and EITC parameters by year (Tax Policy Center's "EITC parameters 1975-2024" table; IRS brackets; or NBER TAXSIM
through `taxsim35` from Stata or Python, which also gives state taxes and would replace BPS's hand-coded
calculator), SNAP parameters by fiscal year (USDA FNS COLA memos: maximum allotments, standard deduction, gross
and net income limits by household size; the USDA SNAP Policy Database for state options), and poverty lines by
year, family size and number of children (Census historical poverty thresholds). Allow year-group-specific
variances (1999-2007, 2009-2013, 2015-2021) rather than one stationary block.

**Cheaper and better for the paper's own claim (do this first):** port `psid_consumption.do` to Python for
1999-2021 (items plus the 6% rent equivalent; two to three days), and run Paper A's existing displacement event
study (`IGE/38.PSIDJointLossChecks.py`, which now has only food) on log total consumption around single and joint
displacements, with Paper A's own event-time dating. That gives the joint-versus-single consumption comparison on
Paper A's sample and definitions, as validation, without BPS's pipeline; the BPS-residualised version for
1999-2009 stays in Appendix D as the "in their own data" check.

---

## 4. Next five steps, in order

| # | Step | Time | Output |
|---|---|---|---|
| 1 | **Rewrite the three tellings** (Section 1 above): intro paragraph to 6-8 lines; sec2 as the single full telling with the trims clause, the consumption result as suggestive with timing, the hours comparison with caveats and the extensive-margin counterpart, the separation sentence, BPS's p. 403 caveat quoted; Appendix D as Tables D1-D3 with two paragraphs of text | 2-3 days | `sec1`, `sec2`, `appD_bps.tex` |
| 2 | **Paper A's own consumption measure and event study, 1999-2021** (port of `psid_consumption.do`; log total consumption and its components around the husband's, the wife's and joint displacements in the stacked event study; by race; period stated). Targets: the single-displacement fall (years 1-3) and, if its s.e. is below about 0.08, the joint-minus-single difference; otherwise the latter is validation (Section 2.3) | 1 week | `IGE/45.ConsumptionDisplacement.py`, a figure and a table for Section 5; rows in the targets file with their 1999-2021 window |
| 3 | **Model document update and PI sign-off** before code: the BPS-nesting additions (discrete hours for both, shared stochastic human capital innovations, work cost), the measurement-error mixture and its two diagnostics, the BPS-sample constructor (filters as code), the revised pass criteria of Section 2.2, the consumption targets and their 1999-2021 window with the wave-dated event time of 2.3, the attrition shares; one page in the PI's model-docs style | 2-3 days | `model/couples_description.md` section "BPS test" |
| 4 | **BPS test harness now, from the real-data pipeline**: `code/run_spec.do` already runs one specification end to end from a `psid_cons.dta`-shaped file; write `bps_on_sim.do` that takes a simulated panel with BPS's variable names and runs the same chain, plus the Step 2 event study; test it on BPS's own panel (must reproduce Step 0) | 2 days now; runs in minutes once the simulator exists | `IGE/bps_reconciliation/code/bps_on_sim.do`, `sim_to_bps.py` (panel writer) |
| 5 | **Build** per the earlier plan: targets file (week 0-1), solver with the staged tests (weeks 1-3), simulator and monthly-to-annual panel (3-4), SMM wiring and recovery (4-5), HPC estimation of the main and independent-shock models (5-8), BPS test and counterfactuals (8-10), writing (10-12). The 1999-2021 BPS Step 2 extension (Section 3) runs in parallel in weeks 2-4 only if step 2 above shows the consumption result deserves the BPS-residualised confirmation | 12 weeks | Paper A complete |

What not to do: re-estimate BPS's preference step on 1999-2021; put the trims, the -0.138** or the entries
coefficient on joint years in the introduction; add the transitory wage covariance back as evidence of the joint
shock; target the BPS-panel -0.138** itself (17-23 events, one interval, one of five samples) rather than Paper A's
own 1999-2021 event study.
