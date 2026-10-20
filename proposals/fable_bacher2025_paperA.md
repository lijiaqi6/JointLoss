# Paper A and Bacher, Grübener and Nord (2025), "Joint search over the life cycle": what to take, what is new, what to change in the model document (2026-10-18)

Read, nothing edited or run except this file: Bacher, Grübener and Nord, *Journal of Monetary Economics* 150 (2025)
103696 (whole paper, `IGE/Literature/1-s2.0-S0304393224001491-main.pdf`); the README of their replication repository
(github.com/philippgruebener/JSLC_ReplicationFiles: Fortran solver `Main.f90`/`Globals.f90` with OpenMP, Stata CPS and
SIPP code, R SIPP download, Matlab post-processing; GPL-3.0); Paper A (`main.tex`, `sec1`-`sec8`, `appC_robust.tex`,
`appD_bps.tex`); the model document (`model_document.tex`, Open Decisions D1-D15); my three earlier memos
(`fable_model_choice_paperA.md`, `fable_bps2016_paperA.md`, `fable_bps2016_nextsteps.md`); and the CPS couples script
`IGE/30.CPSJointJobLoss.py` (header and the added-worker block). "BGN" below means Bacher, Grübener and Nord; their
numbers are from their tables; Paper A's from its text. Where I quote their "arrival rates" it is their term; Paper A's
object is the search friction.

---

## 0. Verdict (six lines)

1. **Complement, not competitor.** BGN measure the spouse who can *enter* (non-participating spouses of one-earner
   couples; added-worker effect 5.55 pp, 7.12 pp at 26-35, 1.40 pp at 56-65) and ask why it declines with age. Paper A
   measures the spouse who is *lost* (both-working couples; the wife's job-loss hazard ten times higher in the month
   of his). Their footnote 19 leaves correlated separations out; their model with independent separations cannot
   produce a same-month ratio above about 1.25 and puts joint EU-EU flows at about one tenth of their frequency
   (Section 2.3).
2. **Their model is the right template for Paper A's labor-market block**, and Paper A's planned model already is that
   block (monthly, two members, employment/non-employment with and without UI, human capital that accumulates at work
   and depreciates out of it, assets, taste shocks with DC-EGM, retirement). Adopt three of their devices (geometric UI
   expiry; the earnings-loss-by-duration moment; the joint-state distribution by age as validation), decline three
   (endogenous arrival rates by directed search; a search-effort state; a 12-point grid), and keep everything that is
   Paper A's own (common and permanent displacement risk, sector match, children, SNAP/EITC/progressive tax,
   separation of the couple, race, SMM).
3. **Do not build on their code.** Fortran with hand calibration, GPL-3.0, no estimation loop, no children, no sector
   match, no transfer schedules; the shared Python/numba SMM infrastructure is worth more. Read their code for two
   things: the DC-EGM upper envelope over 16 joint discrete states, and their Stata implementation of the Elsby et al.
   (2015) classification-error adjustment.
4. **One empirical tie-in, one afternoon, before the model section:** replicate their Tables 1-2 (EN couples, NE/NU/NN
   of the non-participating wife by the husband's EE/EU, by wife's age) on Paper A's CPS panel, and next to it the joint
   EU-EU excess by the same age groups. Expected result: Paper A reproduces their age-declining added-worker effect
   and shows the joint loss does *not* decline with age. That one table is the positioning of the two papers.
5. **The model document needs eleven changes** (Section 6): a UI-state simplification that halves the state space,
   five moments added (two targets, three validations), three new open decisions (D16-D18), and a paragraph placing
   the model against BGN with the exact departures.
6. **Ready to design the model section: yes**, in the order of Section 6.3, after the afternoon of Section 4 and the
   PI's answers to D1, D5, D13, D14 and D16-D18.

---

## 1. What BGN do and find, and how close their model is to Paper A's

### 1.1 Empirics (CPS 1994-early 2020, couples 26-65, monthly flows)

- **Object.** Couples with one employed ("primary earner", whichever sex) and one non-participating member ("spouse").
  The added-worker effect (AWE) is P(spouse N->E or N->U in month t | primary E->U) minus the same conditional on E->E,
  in the *same month*. Classification error between U and N is corrected as in Elsby, Hobijn and Sahin (2015). All EU
  transitions of the primary earner count (quits, permanent and temporary layoffs, temporary jobs); Online Appendix
  Table B.4 says the AWE is similar for permanent separations only.
- **Levels (Table 1, 1,280,562 EN couple-months).** NE 5.93% -> 7.65% (+1.72 pp), NU 1.61% -> 5.44% (+3.83 pp); AWE
  5.55 pp, a 74% increase on the base 7.54%. Two thirds of the AWE is entry into unemployment, not into a job: "search
  at once, jobs slowly" is their fact too.
- **Age (Table 2).** 7.12 pp (26-35), 6.83 (36-45), 4.57 (46-55), 1.40 (56-65); for the oldest the NE part is -0.49.
  The primary earner's EU rate also falls with age (1.22% young, 0.81% old).
- **Leads and lags (Figs. 1-2, Eq. 1 with month, year and state FE, controls).** Contemporaneous 5.8 pp; two months
  before 1.7, one month before 2.0; one month after 2.6, two months after 3.3. Young: 7.3 contemporaneous, 3.0 and
  3.7 after. Old: 1.5 contemporaneous, nothing else. Compare Paper A's wife's own job loss: 0.6-0.7 pp in the three
  months before, 4.0 in the month, 0.6-0.8 after. Both facts have a flat shared-risk pedestal around a same-month spike.
- **Heterogeneity (Table 3).** Stronger for college spouses (8.87 vs 5.23); by net liquid wealth in the SIPP 6.10
  (bottom half) vs 5.32 (top), not significant. Hence "need or availability?", which the model answers.

### 1.2 Model (Section 3; parameters Table 5)

- Monthly; two members of the same age; 480 months of work, 120 of retirement; CRRA 1.75; beta 0.9955 a month; a
  risk-free bond, no borrowing; flat labor tax 0.28; pension $3,500 a month.
- Each member in E, U (unemployed with benefits), S (unemployed without benefits, costly search), or N
  (non-participating); 16 joint states. Benefits: replacement 0.5, cap $2,500 a month, lost with probability 1/6 a
  month (expected six months). From N, offers arrive without search at a lower rate ("to capture that individuals in
  the data directly transition from out of the labor force into employment"). Quits allowed. Fn 10: a separated
  member cannot receive an offer in the separation period.
- Human capital on a 12-point equidistant grid spanning the 5th-95th percentiles of SIPP monthly earnings; earnings
  equal the level (y(h) = h, linear in levels); moves up one point while employed with probability 0.1 x i^(-1.8)
  (decreasing in the level), down one point while non-employed with probability 0.05 (constant). Separation hazard
  0.05 x i^(-0.65), from 5.0% at the bottom to 1.0% at the top. Earnings losses on re-employment are matched by spell
  length (Table 8: -1%, -7%, -20% after 1-3, 4-12, 13-24 months of non-employment; model -2, -8, -25).
- "Arrival rates" are endogenous: firms post vacancies in submarkets indexed by the whole household state
  (age, both human capital levels, next-period assets, joint state, the spouse's separation indicator), free entry
  with posting cost 8 and a Cobb-Douglas matching function (elasticity 0.5), because the firm's expected profit
  depends on the worker's future quits and acceptances, which depend on the spouse. Exogenous shifters: 0.3 for U and
  S, 0.2 for N. The resulting average rate for non-employed EN spouses falls from 0.16 at 26 to about 0.01 at 64 (Fig.
  10), mostly through the age distribution of assets and both human capital levels.
- Preferences: disutility by joint state, symmetric across members; the EN/NE and UN/SN/NU/NS disutilities are
  age-dependent (logistic in months) to match the share of one-earner couples by age, "capturing child-care needs of
  young households in a parsimonious way" (fn 15). No children, no marriage dissolution, no SNAP or EITC, no
  aggregate state, no correlated shocks (fn 19).
- Solution: Iskhakov et al. (2017) DC-EGM with Gumbel taste shocks (scale 0.1), the firm's problem nested inside each
  period; Carroll EGM for retirement. 160,000 simulated households. Calibrated ("all parameters determined jointly",
  but no objective function, no standard errors): targets are individual E/U/N transition rates, separation rates by
  income, the joint-state distribution by age (Fig. 5), median net liquid wealth and earnings by age, earnings losses
  by spell length. Untargeted: transitions by age (Table 9; the model underpredicts N->E, 2.6 vs 5.7%).

### 1.3 Results

- The model gives an AWE of 5.16 pp (data 5.55), 9.35 for the young (7.12) and 1.22 for the old (1.40), mostly through
  entry into search (their NS); the leads and lags of Fig. 6 reproduce the lagged responses of the young.
- Decomposition (Table 11): giving the young the old's assets, employed member's human capital, or non-participating
  member's human capital cuts their AWE by 66%, 65%, 24%; all three plus the induced change in arrival rates by 109%;
  the old's AWE barely rises from any one margin alone and rises strongly only when all are set to the young's
  values: *complementarity of need and availability*. Age itself (proximity to retirement, age-dependent disutility)
  is also large: an old couple with the young's states still has a small AWE (column 5).
- UI duration (Table 12): six to twelve months lowers the AWE from 5.16 to 3.68 pp (young 9.35 -> 6.93), i.e. public
  insurance crowds out the *spouse's* labor supply, most among the young.

### 1.4 Distance from Paper A's planned model

| Block | BGN | Paper A model document | Verdict |
|---|---|---|---|
| Period, horizon | monthly; 480 + 120 months; both members same age | monthly; wife 25-60 (420 months); terminal value with Social Security | same device; D1 is settled by precedent |
| Labor states per member | E, U, S, N (search effort a choice) | employed / non-employed with a UI clock; "looking" is a measurement | Paper A coarser; see D16 |
| UI | expiry 1/6 a month; replacement 0.5; cap $2,500 | clock 6 -> 3 -> 0 with 1/3 hazards; 0.5; era cap; the wife's clock records lost hours | adopt their geometric expiry (Section 3) |
| Separations | exogenous, level-dependent, independent across members | own hazards x couple type + common shock by sector match + displacement loss | Paper A's whole contribution lives here |
| Job finding | endogenous "arrival rates", directed search, free entry | exogenous search friction lambda_j(r) | keep exogenous (Section 3) |
| Human capital | 12 points, level-dependent accumulation, constant depreciation, linear earnings | 7 points in log wage, constant accumulation by hours, depreciation, displacement loss, shared and own persistent innovations (BPS) | keep 7; borrow their by-duration moment |
| Preferences | joint-state disutilities, age-dependent | work costs by hours and youngest child's age; fixed cost of work; SNAP stigma | Paper A's children replace their age-dependence |
| Government | flat tax, UI, pension | progressive tax, UI, EITC, SNAP, childcare price, floor | Paper A's policy question needs it |
| Marriage | none | exogenous separation hazard elevated after his loss | Paper A's |
| Solution | DC-EGM + Gumbel shocks, Fortran/OpenMP | DC-EGM + Gumbel shocks, numba | same method; their state space is of the same order (16 joint states x 12 x 12 x assets x age, vs 423,360 x 420) |
| Estimation | calibration, no SEs | one joint SMM run, SEs, independent-shock model on the same targets | PI rule; Paper A is stronger here |

The labor-market block of Paper A is BGN's with the search-effort state removed and the separation process replaced.
That is the right relation to state in the paper: Paper A is not re-inventing the two-member search model; it is
putting correlated separations and the safety net into the standard one.

---

## 2. How Paper A relates: complement or competitor?

### 2.1 Complement, on both the fact and the model

- **Different couples.** BGN's AWE is defined on EN couples (one earner). By their Fig. 5, EN couples are about a
  quarter of couples at 26-45 and a third at 56-65; EE couples are about two thirds at 26-55. Paper A's fact is in EE
  couples. The spouse who can enter and the spouse who can be lost are different people in different households.
- **Different margins of the same mechanism.** BGN: the second earner is *available* when young (high human capital
  relative to the first earner, high arrival rates) and *needed* when poor. Paper A: the second earner is *lost* exactly
  when needed. Both say that spousal insurance is weakest where the household is most exposed: for the old in BGN, in
  the month of a shared shock in Paper A.
- **Same fact, two readings, both already in Paper A.** Paper A's CPS numbers for wives who were not working
  (unemployed and looking +8.8 pp the month after his loss; employed +2.2 pp after one month, +4.2 after three) are
  BGN's AWE under a wider definition (Paper A pools U and N wives at baseline, conditions on job-loss reasons rather
  than all EU, and does not apply the Elsby adjustment). Their 3.83 pp into unemployment against 1.72 into employment
  is Paper A's "search at once, jobs slowly". Section 4 says how to make the two numbers the same number.

### 2.2 What is new in Paper A relative to BGN

| Paper A | BGN | Status |
|---|---|---|
| Correlated separations: same-month common shock by sector match, permanent couple type, their monthly traces | fn 19: "the model does not incorporate correlated shocks across spouses"; only an endogenous correlation through the initial distribution of human capital | new; the central mechanism |
| EE couples' joint EU-EU: the tenfold same-month hazard, 13x for permanent losses, a third carried by same industry x occupation x class | EN couples' NE/NU of the non-participant | new object |
| Gross vs net added work: +47 h gross, -35** offset, net ~0 (PSID 1984-2021); SIPP net change in all wives' employment ~0 for a year because working wives lose their jobs | the AWE is measured on spouses who have no job to lose, so the offset is outside their design | new |
| Timing: her job loss peaks in his loss month; her entry builds over six months | the AWE's timing (search first, jobs later; lags among the young) | complementary |
| BPS reconciliation (one model, both answers) | not addressed | new |
| Safety net as schedules: UI per spouse, EITC zero at zero earnings, SNAP in every state; the no-earner state | UI duration only; flat tax; no transfers at zero earnings | new |
| Race as environment heterogeneity, common preferences | none | new |
| Children explicit (youngest child's age), separation of the couple, consumption targets 1999-2021 | age-dependent disutility; no dissolution; no consumption moment | new |
| SMM with standard errors, independent-shock model on the same targets | calibration | stronger |
| The age gradient of the AWE and its need/availability decomposition; endogenous arrival rates; UI crowd-out of the spouse by age | their contribution | **do not redo**; cite and validate against it |

### 2.3 Could their model, with independent separations, reproduce the tenfold joint hazard?

No, and the bound is easy to state. In BGN the only link between the members' separations is that the hazard
delta(h) = 0.05 x i^(-0.65) depends on the level, and levels are correlated across spouses through assortative initial
conditions. The same-month ratio P(wife separated | husband separated) / P(wife separated | husband not separated) is
then E[delta_w delta_h] / (E[delta_w] E[delta_h]) = 1 + cov(delta_w, delta_h) / (E delta_w E delta_h). With delta between
1.0% and 5.0% across the grid and a mean near 2% (their E->U+E->N is 2.1%), even perfectly correlated levels give a
covariance of order 1e-4 against a product of means of 4e-4: a ratio of at most about 1.25, against 10 in the CPS (9.4
times what independence implies), 11-14 for permanent losses, 7.7 in the SIPP and 4.3 within the year in the DWS. A
monthly model with independent separations is therefore not an approximation to the joint loss; it is off by an order
of magnitude.

What that implies for joint EU-EU flows: with independent hazards of about 0.5-1% a month per spouse (job losses
excluding quits, Paper A's base 0.54% for wives), a both-lost month occurs in about 0.004% of EE couple-months; the CPS
has about 0.04%. Independent separations put the joint-loss state at one tenth of its frequency and, because the
state is where consumption falls most and the EITC pays nothing, they understate the welfare cost of displacement risk
and the value of unconditional transfers by construction. BGN's Fig. 5 shows the joint UU share of couples as a
non-targeted stock; it is small in both the data and the model and the figure does not resolve the difference. Paper A
should report the UU share by age from the CPS as the stock counterpart of its flow (Section 4).

Two further implications for their results that Paper A can state without redoing their model: (i) with a common
shock the precautionary motive of EE couples is larger than their model implies, which is their "need" margin; (ii) if
the common shock also lowers her job finding (CPS: already-unemployed wives find work less often after his loss,
-0.020* after one month, -0.050** after three), it hits their "availability" margin too. Both are reasons the AWE
should be read as an upper bound on what the family can do, which is Paper A's reading.

### 2.4 Competitor only on one counterfactual

Their Section 5.3 (UI duration 6 -> 12 months lowers the spouse's AWE) overlaps with Paper A's counterfactual (ii)(b).
Paper A's version differs in two ways that should be said explicitly: eligibility of *both* spouses at a joint loss
(their model never has two eligible members in the same month except by independent coincidence), and the recession
comparative static (pi_c doubled). Report the AWE crowd-out among EN couples alongside, so that the two papers'
numbers are on the same scale (their 5.16 -> 3.68 pp).

---

## 3. Design implications, decision by decision

### 3.1 The structure of the labor-market block

| Question | BGN | Recommendation for Paper A | Why |
|---|---|---|---|
| **E/U/S/N with a search-effort choice** | yes; S vs N is the choice; N receives offers at a lower rate; NU is two thirds of the AWE | **No search-effort state (default stands).** Keep employed / non-employed with the acceptance margin; "looking" = would accept with probability above one half. Add D16: a two-state version (non-employed with and without search, one extra cost parameter, lambda_N = kappa_N lambda_S) as the *fallback* if the model cannot fit both the low entry rate of non-employed wives whose husband is employed (0.075 a month) and the SIPP build-up (0.019 -> 0.054 at six months) | Parsimony; the acceptance margin produces the jump in "looking" and the differential entry; the PI's search-moments plan (looking among the not employed) belongs to the companion, not Paper A. BGN themselves say the NE/NU split is sensitive to within-period timing (Section 5.1) and fit the sum, which is what Paper A validates |
| **UI eligibility** | one state per member, lost with probability 1/6 a month | **Adopt the geometric expiry (1/6 a month, expected six months) in place of the 6 -> 3 -> 0 clock.** Wife's labor state: employed; non-employed with UI at lost hours P or F; non-employed without UI (4 values instead of 6); husband 3 instead of 4. State space 423,360 -> 211,680 per month per race | Halves the solve for nothing the targets can see: the SIPP paths at 3, 6, 12 months and the PSID annual moments cannot distinguish an Erlang-2 from a geometric exhaustion. The lost-hours record stays (the benefit depends on it) but is a D14 cut candidate (benefit on full-time-equivalent earnings times a part-time factor) |
| **Quits** | allowed from E to U, S or N | the wife can leave a job (no UI); the husband works whenever he has a job | keep; but **target the wife's monthly exit from employment outside job loss** (CPS), so the quit margin is not free (Section 4) |
| **Timing of offers after a separation** | fn 10: no offer in the separation period | the same (displaced at the end of t, can find from the end of t+1) | consistent; cite fn 10 in the timing section |
| **Arrival rates endogenous by directed search** | yes: firms price the spouse's effect on quits and acceptances; needed for their "availability" counterfactuals | **Exogenous search friction lambda_j(r), as planned.** Two cautions from BGN: (a) their average rate for non-employed EN spouses falls from 0.16 at 26 to 0.01 at 64 (Fig. 10), mostly through the age distribution of assets and human capital; a constant lambda_w will overstate re-entry of older wives, so validate the CPS entry rate of non-employed wives by age and, only if it fails, allow one age slope in lambda_w (D13 extended); (b) their endogenous machinery did not buy fit on the margin Paper A targets (N->E 2.6 model vs 5.7 data, Table 9) | Parsimony rule; Paper A's question is the joint loss and the schedules, not why availability declines with age; the free-entry block is five parameters (kappa, alpha, chi, two shifters) for a mechanism Paper A does not test |
| **Human capital grid** | 12 points, level-dependent accumulation 0.1 i^(-1.8), constant depreciation 0.05 | **Keep 7 points in log wage** with the BPS innovations. Two borrowings: (a) add BGN's Table 8 moment, earnings on re-employment relative to the last month employed by non-employment duration (1-3, 4-12, 13-24 months), computed from Paper A's SIPP panel (IGE/40) for involuntary separations, by spouse; (b) if constant pi^up cannot fit two-year wage growth at 25-34 / 35-44 / 45-54, a one-parameter concavity pi^up(h) = pi^up h^(-eta) is the BGN form, not a separate age profile | (a) is the clean identification of depreciation against the displacement loss: BGN's -1% after 1-3 months says the loss on fast re-employment is small; if Paper A's SIPP number for involuntary separations agrees, d_j is a parsimony cut (losses are depreciation, growing with duration) and the PSID years 1-3 loss is reproduced by duration alone; if it does not (the displacement literature's lump), d_j stays. Either way the test is cheap and decides a parameter |
| **Separation hazard by level** | 0.05 i^(-0.65): the low-paid lose jobs five times as often | Paper A: delta_j(r) m_tau, no level dependence | keep; the couple type tau is Paper A's version of persistent heterogeneity in risk, identified from the leads/lags and the placebo; report BGN's level gradient as what tau stands in for. If the Jacobian shows p_H, m_H weak, delta_j(h) with one curvature parameter (BGN's form) is the alternative to a type |
| **Taste shocks + DC-EGM** | Gumbel scale 0.1, Iskhakov et al. 2017, firm problem nested | the same, scale calibrated, no firm problem | identical; cite them as precedent for solving a 480-month two-member DC-EGM. Their note that taste shocks are "for computational purposes" supports keeping sigma_eps calibrated (not estimated) and reporting the profile |
| **Preferences** | joint-state disutilities, age-dependent to match the EN share by age (fn 15) | work costs by hours and child age; fixed cost; no age dependence | keep; Paper A's k state is the explicit version of their fn 15. **Validate the joint-state distribution (EE, EN, EU, UU) by wife's age** (their Fig. 5) so that the children block does the work their age-dependence does |
| **Calibration vs SMM** | calibration, no objective, no SEs | one joint SMM run (PI rule) | keep. BGN's parameter count in the labor-market block is about 14 (two separation, two accumulation, one depreciation, two bounds, three arrival shifters, posting cost, four disutility levels); Paper A's 30 includes race-specific hazards and frictions and the BPS additions. BGN impose symmetry across members and a constant depreciation: supports D14's cut candidates (common pi^dn, common delta_w across races) |
| **Age range, life cycle** | 26-65 working, retirement to 75, both members the same age; the horizon is a large part of the old's small AWE (Table 11 column 5) | wife 25-60, PSID couple's own ages, terminal value with Social Security | keep 25-60 (the PSID copies need it). Two consequences: Paper A's AWE validation by age covers 26-35, 36-45, 46-55 and 56-60 only, and the terminal value matters for the 46-60 response; if the model's AWE at 46-55 is far from 4.57 pp the terminal value (240 months, 40% replacement) is the first suspect. D18 asks whether to extend to 64 for the AWE check alone |
| **Borrowing** | none | borrowing limit estimated (D11) | keep D11; BGN underpredict assets of the middle-aged and overpredict the young's, with no borrowing. Not informative for D11 |
| **Build on their code?** | Fortran/OpenMP solver, Matlab outputs, Stata data code; GPL-3.0; no estimation loop | **No.** Own numba solver on the companion infrastructure (params, SMM engine, HPC script, sim-panel design), as decided 2026-10-17 | (i) GPL-3.0 would bind any derived code; (ii) Fortran cannot plug into `smm.py`/`hpc_job.py`; (iii) the state space (sector match, couple type, children, UI by lost hours, SNAP, EITC, separation, race, eras) is not theirs; (iv) they have no estimator to inherit. Use it as a reading reference for the upper-envelope step with 16 discrete joint states and for `cps_main.do`'s Elsby adjustment |

### 3.2 D1-D15 in order

| Decision | BGN's precedent | Recommendation |
|---|---|---|
| D1 period | monthly, 480 months, solved and simulated for 160,000 households | confirm monthly; the quarterly fallback is unlikely to be needed |
| D2 preferences by race | none | unchanged (common preferences); BGN's symmetry across members is the same spirit |
| D3 child block | none | unchanged |
| D4 HPC | Fortran/OpenMP, hardware not stated | unchanged; the smaller state space after the UI change helps the 4 GB per worker |
| D5 temporary layoffs | all EU counted; Appendix B.4: AWE similar for permanent separations | supports the default (permanent displacement only, non-temporary CPS targets); the recall state stays an alternative |
| D6 transitory shocks | none | no implication |
| D7 wage-process parameters | none | no implication |
| D8 policy eras | one stationary schedule | no implication; eras are a Paper A need (PSID 1984-2021) |
| D9 education | initial distribution by joint education of the couple (SIPP, ages 26-30) | the same as Paper A's default (education through initial human capital and wealth); keep |
| D10 separation trigger | no dissolution | unchanged |
| D11 precautionary saving | beta 0.9955 a month calibrated to assets by age; no borrowing | unchanged (beta fixed, limit estimated) |
| D12 consumption targets | none | unchanged |
| D13 husband's search friction | endogenous and age-declining | estimated in the SMM (default); validate his re-employment path by age (SIPP); one age slope only if it fails |
| D14 parameter count | symmetric disutility across members, constant depreciation | add to the cut list: d_j if the by-duration moment is fit by depreciation (Section 3.1); the wife's lost-hours UI record |
| D15 welfare after separation | none | unchanged |

### 3.3 New open decisions

- **D16 Search-effort state.** Default: none (acceptance margin only; "looking" is a measurement). Fallback: non-employed
  with/without search, one cost and one ratio parameter, if the entry rate of non-employed wives with employed husbands
  and the SIPP build-up cannot both be fit. Decide after the solver's staged check (3).
- **D17 Added-worker effect by age.** Default: BGN's definition replicated on Paper A's CPS panel and used as untargeted
  validation by age (overall and the NE/NU split). Alternative: the overall contemporaneous AWE as a target in place of
  the SIPP month-0 moment. I recommend validation: the model has no age-specific parameters, so an age gradient it
  produces is a genuine test of the human capital, assets and horizon channels BGN identify.
- **D18 Age range for the AWE check.** Default: wife 25-60, AWE validated at 26-35, 36-45, 46-55, 56-60. Alternative:
  extend the solve to 64 to compare with BGN's 56-65 group. Not worth 10% more compute unless the referee asks.

---

## 4. Empirical tie-ins

### 4.1 Replicate BGN's Tables 1-2 on Paper A's CPS panel (one script, one afternoon, no new data)

`IGE/30.CPSJointJobLoss.py` already holds PEMLR for both spouses (1-2 employed, 3 on layoff, 4 looking, 5-7 not in
the labor force), PRUNTYPE, PRTAGE 20-62, state, race, education and the youngest child's age, and its item 5 computes
the response of wives *not employed* at m (U and N pooled) to the husband becoming a *job loser* (unemployed with a
job-loss reason) at m+1. BGN's object differs in four ways, each a filter:

1. the wife is N at m (PEMLR 5-7), not U;
2. the husband's transition is any E->U (PEMLR 1-2 -> 3-4), with the job-loser subset as Paper A's variant;
3. the outcome is the same month (her status at m+1 against his at m+1), with NE and NU reported separately;
4. the Elsby-Hobijn-Sahin (2015) correction for N/U classification error (their `cps_main.do` implements it); report
   with and without, since Paper A's other CPS numbers are uncorrected.

Report: all couples (primary earner of either sex, as BGN) and wives only (the model's object); by wife's age 26-35,
36-45, 46-55, 56-62 (the API predicate in `IGE/30` line 116 stops at 62; a re-pull to 65 is a one-line change if the
56-65 group is wanted). Expected: close to 5.55 pp overall and 7.1 -> 1.4 across age, with Paper A's wider definition
(+8.8 pp into unemployment) reconciled by the conditioning. Script: `IGE/50.CPSAddedWorkerByAge.py` (49 is the planned
targets script), writing `output/cps_awe_by_age.md`; the simulated-panel counterpart goes into the measurement layer.

### 4.2 Joint EU-EU by the same age groups (same script)

The wife's same-month job-loss excess (state x month FE, all and non-temporary losses) by wife's age 26-35, 36-45,
46-55, 56-62, and the EE, EN, EU and UU shares of couples by age (BGN Fig. 5's data bars). Prediction to test: the
joint-loss excess does not fall with age (shared workplaces do not retire early) while the AWE does. If so, the two
facts fit on one figure (two panels: her entry if not working, her loss if working, by age) and give the paper its
sentence: "the spouse who could enter is available only when the couple is young; the spouse who is lost is lost at
every age." If the joint loss also declines with age, that is worth knowing before the model's validation by age is
designed. The UU share by age is the stock that independent separations understate (Section 2.3).

### 4.3 Other BGN moments for the targets table

| Moment | BGN | Paper A source | Use |
|---|---|---|---|
| Earnings on re-employment relative to the last employed month, by non-employment duration 1-3 / 4-12 / 13-24 months, involuntary separations, by spouse | Table 8 (SIPP 1995-2016: -1, -7, -20%) | SIPP panel, `IGE/40` | **target** for pi^dn_j and the d_j cut (Section 3.1) |
| Wife's monthly exit from employment outside job loss (E -> N or U without a job-loss reason), husband employed | Table 6 (E->N 1.8%, E->U 0.9% pooled) | CPS, `IGE/30` | **target** for the quit margin (phi_F, phi_P, theta) |
| Joint labor-market state shares EE/EN/EU/UU by wife's age | Fig. 5 | CPS, `IGE/50` | validation of the children block and lambda_w |
| Individual E/U/N transition matrix of wives and husbands | Tables 6, 9 | CPS, `IGE/30` | validation (the model's N/U is a measurement) |
| AWE by age, NE and NU parts | Tables 1-2 | `IGE/50` | validation (D17) |
| AWE crowd-out from UI duration | Table 12 (5.16 -> 3.68 pp) | model | report with counterfactual (ii) |

Not worth importing: their median net liquid wealth by age (Paper A targets the PSID wealth shares, same purpose),
their separation rate by income (the couple type and the base hazards cover Paper A's needs), their earnings by age
(a validation Paper A already has through the married men's profile).

---

## 5. How to cite and position BGN in Paper A

**Literature paragraph (`sec2_literature.tex`, "Insurance within the household").** The current sentence is accurate
but undersells the relation. Replace with: "\citet{bacher2025joint} measure, in monthly CPS flows of one-earner couples,
that a non-participating spouse is 5.6 percentage points more likely to enter the labor force in the month the earner
loses his job, two thirds of it into unemployment rather than a job, 7.1 points at ages 26--35 and 1.4 at 56--65; in a
monthly life-cycle model of joint search with assets, human capital, unemployment insurance and endogenous job-finding
rates they attribute the decline to a complementarity between the need for and the availability of spousal insurance.
Their separation shocks are independent across spouses, which they note leaves out the correlation from shared
industries and occupations. This paper measures that correlation in two-earner couples, where the spouse is not an
entrant but a second job at risk, and finds it an order of magnitude larger than independence implies." Add
\citet{bacher2025joint} to the added-worker citations in the introduction's second contribution (next to
\citet{cullen2000does, stephens2002worker, halla2020job}); their monthly AWE is the modern version of that literature.

**Table 1 row.** Replace "Known; the separation shocks are correlated here" with: "Known for one-earner couples (the
spouse who can enter), by age. New: the two-earner couples' joint loss (the spouse who is lost), measured in the same
CPS panel with their added-worker effect by age; independent separations put it at one tenth of its frequency."

**Section 4 (new figure or table panel).** The AWE-by-age replication and the joint loss by age from Section 4.1-4.2,
with the one sentence of Section 4.2.

**Model section (`sec7_model.tex` and the model document).** Keep "the closest model is \citet{bacher2025joint}" and
make the departures exact: "The labor-market block follows theirs: a monthly period, employment and non-employment
with and without unemployment insurance that expires at a constant hazard, a human capital level for each spouse that
accumulates at work and depreciates out of it, savings, and extreme-value taste shocks with the endogenous grid method
for discrete-continuous choice. It departs in three ways. The spouses' displacement risk has a common and a permanent
component, which their model leaves out (their footnote 19). The search friction is exogenous and race-specific, where
their job-finding rates are set by firms' vacancy posting; their question, why spousal insurance is available to the
young and not the old, needs that block, and ours does not. And the government is a set of schedules with the Earned
Income Tax Credit and food stamps, the couple has children whose ages set the cost of the wife's work, and the marriage
can end." In the counterfactual section, next to (ii): "\citet{bacher2025joint} find that extending benefit duration
from six to twelve months lowers the added-worker effect from 5.2 to 3.7 points; the experiment here differs in that
both spouses can be eligible in the same month and the common shock is doubled."

**Also to check (from their reference list, not read here):** Guner, Kulikova and Valladares-Esteban (2024, "Does the
added worker effect matter?", CPS 1976-2019, AWE 6-7 pp per BGN) and Haan and Prowse (2024, *AEJ: Macro*, social
assistance versus unemployment insurance in a life-cycle model of family labor supply). The second is close to Paper A's
EITC-versus-SNAP ranking and should be read before the counterfactual section is written.

Terminology in all of the above: "search friction" and "job finding" for Paper A; "arrival rates" only in quotation
when describing BGN.

---

## 6. Changes to the model document, and the verdict

### 6.1 Changes (eleven)

1. **Section 1 (Environment), new paragraph "Relation to Bacher, Grübener and Nord (2025)"**: the three departures of
   Section 5, with fn 19 and fn 10 cited; one sentence that their 480-month two-member DC-EGM is the precedent for D1.
2. **Section 4 (UI)**: replace the 6 -> 3 -> 0 clock with a single UI state per spouse lost with probability 1/6 a month
   (expected 26 weeks); keep the wife's lost-hours record for now. Update Table 2 (state space): wife's labor state 4,
   husband's 3, total 211,680; update the storage and compute paragraphs (0.35 GB per race; evaluation target unchanged).
3. **Section 3.3 (search friction)**: say that job finding does not depend on age or the level, name BGN's Fig. 10 as the
   known risk, and name the validation by age that guards it.
4. **Section 3.1 (human capital)**: add the by-duration earnings-loss moment and the rule for cutting d_j; note BGN's
   level-dependent accumulation as the one-parameter alternative to a constant pi^up if wage growth by age fails.
5. **Section 6 (timing)**: cite BGN fn 10 for the no-offer-in-the-separation-month convention.
6. **Targets table**: add (a) SIPP earnings loss by non-employment duration, by spouse, involuntary separations (target);
   (b) wives' monthly exit from employment outside job loss (target); both with windows and the script.
7. **Untargeted validation list**: add (c) the AWE by age under BGN's definition with its NE/NU split; (d) the joint-loss
   excess by age; (e) the joint-state shares EE/EN/EU/UU by wife's age; (f) the wives' and husbands' E/U/N transition
   matrix; all from `IGE/50`.
8. **Counterfactuals (ii)**: add the AWE crowd-out among EN couples as a reported outcome, for comparability with BGN
   Table 12.
9. **Identification**: one paragraph on what the AWE by age tests (human capital of both spouses, assets, the terminal
   value) given that no parameter is age-specific.
10. **Open decisions**: D5 note BGN Appendix B.4 as support; D13 add "validate by age; one age slope only on failure";
    D14 add d_j and the lost-hours record to the cut list; add D16-D18 (Section 3.3).
11. **Build sequence**: week 0 gains "AWE replication and joint loss by age (`IGE/50`)"; the measurement layer gains the
    BGN AWE constructor (EN couples, same month, with the Elsby adjustment applied to simulated data in the same way).

### 6.2 What not to change

The three-part displacement risk, the sector match and couple type, the children state, the government as schedules,
the separation hazard, the BPS nesting, the consumption targets, the SMM design and the five counterfactuals: BGN
give no reason to touch any of them, and their fn 19 is the reason the first exists.

### 6.3 Verdict and order

The PI is ready to start designing the model section. The design is already BGN's labor-market block plus Paper A's
shocks and schedules; what remains is to say so, trim the UI state, and fix the validation moments that make the
comparison with BGN a test rather than a citation. Order:

1. **This week, no HPC:** `IGE/50` (Sections 4.1-4.2) so that the AWE-by-age and joint-loss-by-age numbers exist before
   the model section is written; they decide D17 and the positioning sentence.
2. **Model document revision** per 6.1 (one day), then PI sign-off on D1, D5, D13, D14, D16, D17, D18 (the others are
   unaffected by BGN).
3. **Model section of the paper**, written from the revised document in this order: environment and the labor-market
   block (with the BGN paragraph); displacement risk in three parts; the government; marriage and children; timing;
   the household's problem; estimation (targets with windows, the independent-shock model); validation (AWE by age,
   joint loss by age, BPS on simulated data); counterfactuals (with the BGN comparison on UI duration).
4. **Code** per the build table, with the solver's staged check (3) deciding D16.
