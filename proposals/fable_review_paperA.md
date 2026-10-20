# Referee and editor review of Paper A: "Who Insures the Children?" (2026-10-17)

Read: `IGE/paperA_joint_loss/` (main.tex, sec1-sec9, appA, tab_*.tex; main.pdf compiles to 32 pages), `IGE/EVIDENCE.md`
(Paper A rows and the PI-questions table), `IGE/PLAN.md`, `IGE/proposals/*.md`, and the output files behind the numbers
(`father_displacement.md`, `joint_job_loss.md`, `cps_joint_job_loss.md`, `correlated_shocks.md`, `wife_search.md`,
`displacement_id.md`), plus the docstring of `30.CPSJointJobLoss.py`. Every headline number listed in the brief was checked
against the tables and the output files; the checks are in Section 3.1. Nothing in the repo was edited or run.

---

## 1. Verdict

1. **Not top-5 material as it stands.** It is a well-executed PSID+CPS empirical paper with two empty sections (Sec. 8
   "RESULTS PENDING", Sec. 9 "PLANNED"), a title and introduction that promise children and the IGE, and a body whose
   only strong, new result is about the parents: when a husband loses his job his wife is ten times as likely to lose
   hers in the same month (Sec. 6, CPS 1994-2023), and the excess is carried by shared workplaces and survives state x
   month x industry fixed effects. The child and IGE results (Secs. 7-8) are, by the paper's own account, "mixed and
   imprecisely estimated".
2. **The single best version** is a structural paper on *undiversified family insurance*: a two-earner lifecycle model
   with correlated displacement risk, a search friction, savings, the safety net (UI, SNAP, EITC) and a child-outcome
   block, estimated by SMM on the PSID joint-loss and added-worker moments, validated on the CPS monthly flows, and used
   to ask what the correlation of spouses' job loss does to the insurance value of marriage, to consumption, to children
   and to the ranking of UI / SNAP / EITC / childcare. The empirical half is already 70% there; the model is 0% there.
3. **Realistic journals.** Empirical paper alone (Secs. 3-7 cut to the joint-loss story): *AEJ: Applied*, *JOLE*,
   *Journal of Public Economics*, or a short *AER: Insights* on the CPS fact. With a convincing model and the policy
   counterfactuals: *REStud*, *AEJ: Macro*, *JEEA*, *Journal of Political Economy: Macro*; a top-5 general-interest
   journal only if the model delivers a sharp quantitative statement (e.g. "correlated job loss removes X% of the
   insurance value of a second earner and reverses the EITC-vs-SNAP ranking for Y% of couples") and the children block is
   disciplined by administrative estimates rather than PSID associations.
4. **Probability-weighted path.** Best version executed well: top-5 15%, REStud/AEJ:Macro/JEEA 45%, AEJ:Applied/JOLE 35%,
   lower 5%. Current version as is: top-5 <5%, field journal after a major revision 60%.
5. **What to do first** (details in Section 5): (i) fix the two internal contradictions and the one over-claim in
   Section 3 below; (ii) cut Secs. 4 and 8 and the birth-margin framing of Sec. 2; (iii) add the two cheap data checks
   that kill the main alternative explanations of the CPS fact (proxy reporting; temporary layoffs); (iv) replicate the
   fact in the CPS Displaced Worker Supplement and the SIPP; (v) build the model with the joint-loss moments as targets.

---

## 2. The contribution as an editor would state it

**One-sentence pitch.** "Family insurance is undiversified: a wife's job-loss hazard rises tenfold in the month her husband
loses his job, the excess is carried by shared workplaces rather than the local cycle, and because the second earner is
lost exactly when she is needed, average added-worker estimates understate what wives do and overstate what families can
absorb; a two-earner model with correlated displacement risk shows what this does to consumption, children and the
ranking of work-conditioned versus unconditional transfers."

**What is genuinely new** (checked against the literature review in `output/joint_job_loss.md` Sec. 7 and
`proposals/insurance_literature_check.md`):

| Claim | Prior art | Status |
|---|---|---|
| Spouses' earnings covary, mostly permanently | Hyslop 2001 (AER), Shore 2010 (REStat) | known |
| Couples sort on employer / industry; ~10-12% share an establishment | Hyatt 2019 (MLR, LEHD); Busch-Madera | known |
| Joint displacements by the same plant event exist and are dropped | Halla-Schmieder-Weber 2020 (3.5% of closure households), Marcus 2013, Banzhaf 2013 | known, named, not measured |
| Correlated unemployment mutes the US added-worker effect | Kawano-LaLumia-Ramnath-Stevens 2025 (Labour Econ.) | stated as one of two explanations, not decomposed |
| **Monthly within-couple job-loss hazard: 10x spike in the same month, 0.6-0.8 pp in the leads/lags, 30 years, 1.3m couples, within state x month x industry** | none | **new** (Sec. 6, CPS) |
| **Event-study excess with each spouse's own reason for the job end, future-displacement placebo, closure channel (her employer closes when his does), same-3-digit-industry concentration, tetrachoric 0.24 / 0.50** | none at this level | **new** (Sec. 6, PSID) |
| Timing: her loss peaks when the household's loss peaks; added work arrives later | Stephens 2002 shows the AWE build-up; nobody puts her own loss next to it | new framing, partly mechanical (see 3.1) |
| Net vs gross added-worker effect | Kawano et al. gesture at it | new decomposition, currently back-of-envelope |
| Race: equal excess in both races | none | new, and a general finding (keep; the PI's rule applies) |
| Father's displacement -> children, PSID | Page-Stevens-Lindo 2009, Kalil-Wightman 2011, Oreopoulos et al. 2008, Hilger 2016 | replication with a better displacement measure; not new |
| Divorce after displacement, larger for Black families | Charles-Stephens 2004 (divorce after layoffs) | race contrast is new; mechanism not identified |
| Mothers' time at a birth does not harm children; slack does not hold mothers at work | Herbst 2017, Willage-Willen 2022 find harm | informative nulls, but they belong to the companion paper's question, not this one |

**Is the headline strong enough?** The CPS fact is strong: it is big (10x; 23% of wives in the same detailed industry lose
their job in the month their husband does), precisely estimated (s.e. 0.002 on 0.040), robust to the obvious fixed
effects, present in all 51 states, and stronger in recessions. It is the kind of fact a general-interest journal
publishes when it changes how a literature thinks, and here it changes how one reads the added-worker literature and how
one should model family insurance (Blundell-Pistaferri-Saporta-Eksten 2016 and Birinci 2019 both treat the second earner's
job as independent of the first's). What it is *not* is a result about children or the IGE. The current title and the
first two pages of the introduction set up a question (what stands between the father's risk and the children) that the
paper does not answer; the referee reads 12 pages before reaching the result that matters. The headline should be the
joint loss; children and the IGE are the stakes, delivered by the model.

---

## 3. Main weaknesses a top-5 referee would raise

### 3.1 Checks of the numbers in the brief, and three things the text gets wrong

All headline numbers reproduce from the tables and output files: displacement 8.0% / 4.8% (`father_displacement.md`
Sec. 1); father's labor income -4,160 (-16.7% of 24,934) and -9,622 (-23.9% of 40,186) (Tab. 1 B-C); wife's hours +51**
and +112*** (Tab. 1 A, D); wife's displacement +0.083*** on 0.063 (Tab. 2 "window-only sample"); same sector +0.203***,
same 3-digit industry +0.282*** (Tab. 3 col. 4-5); tetrachoric 0.237*** (Tab. 4); CPS 5.45% vs 0.54%, +0.040*** state x
month, +0.037*** state x month x industry, Black 0.044*** vs White 0.038*** (p=0.309) (`cps_joint_job_loss.md` Secs.
1-3); still with wife -0.045*** (Black) (Tab. 1 B); food stamps +0.042** / +0.033*** (Tab. 1). Three problems:

1. **The PSID headline uses the sample without the placebo window.** Sec. 6.1 reports "8.3 points from a base of 6.3%". In
   the main sample of Tab. 2 (both windows observed) the excess is 0.052*** and the *placebo window* (her displacement in
   ev-4..ev-2) is 0.021* (p=0.093), so the couple-FE difference is **0.031* (p=0.077)**. Worse, in the same table the
   future-displacement placebo (husband displaced in ev+4..ev+6) predicts her displacement in ev-4..ev-2 at
   **0.033** (p=0.012)**: wives of men who will be displaced six to ten years later already have a 3-point higher
   displacement rate. That is assortative risk, and the text's sentence "the excess is not a permanent trait of couples
   who face more risk" (Sec. 6.1) overstates what the table shows. The honest statement, which the CPS supports: in the
   PSID about 2 points of the 5-8 point excess is a permanent couple trait and 3-5 points is contemporaneous; in the
   CPS the leads are 0.55-0.7 pp against a 4.0 pp spike, so the contemporaneous part dominates when timing is measured to
   the month. Lead with the CPS, report the PSID with its placebo window, and drop the "not a permanent trait" sentence.
2. **"Wives do not compensate by searching" (Sec. 1, p. 2; Sec. 6.2) contradicts Sec. 6.1.** The CPS paragraph in Sec.
   6.1 reports that non-employed wives' probability of being unemployed and looking rises by **8.8 points in the month
   after** his job loss (0.088***, base 6.0%) and that employment rises slowly (2.2, 3.3, 4.2 points at t+1..t+3). That is
   an immediate search response that is slow to turn into jobs, the opposite of the PSID statement that "the share
   looking for work does not rise after the husband's job loss in any group". The PSID measures status at one spring
   interview a year later (`wife_search.md`); the CPS measures it monthly. The two are reconcilable (search is short and
   over by the next PSID interview), but the paper currently asserts both. Rewrite Sec. 6.2 around the CPS result: wives
   search at once, find work slowly, and the PSID annual snapshot misses the search spell. This also changes the
   classification table in `wife_search.md` Sec. 3 ("no response" for most Black cells) and the sentence about the
   "constant search friction" that the model is supposed to separate.
3. **The "most important answer" claim (Sec. 1, par. 6; Sec. 6 opening) is not supported by the paper's own magnitudes.**
   `joint_job_loss.md` Sec. 5 and Sec. 6.1 of the paper: the joint loss lowers wives' earnings by about $256 a year on
   average, 18% of the $1,460 by which family income falls beyond the husband's own loss and about 2% of the family
   income loss. The gross added-worker response is 85-90 hours against a net 51 (back of the envelope): both are small
   next to an $8,000-10,000 loss. The joint loss therefore does **not** explain why mothers insure so little on average; it
   explains why insurance fails in the tail (same-sector couples: 21% joint loss, tetrachoric 0.50) and in the month it is
   needed. Reframe Sec. 6: the main reasons wives insure little are the ones the literature has (low responsiveness,
   childcare, UI crowd-out, wage levels), and the paper's contribution is a mechanism that is small on average, large
   in the state and the subgroup where it bites, and absent from every model of family insurance.

Two further points of accuracy. (a) The "timing" argument that wives' hours do not rise in the displacement year (Sec. 6.1,
"3.8 hours") is partly mechanical: year 0 is a calendar year in which the job ended at some unknown month, so year-0 hours
mix pre- and post-loss months. The CPS flows carry the timing argument; say so and drop the PSID year-0 hours from the
argument. (b) The contributions paragraph of Sec. 2.7 ("the insurance margin at the birth of a child and its crowding out by
the safety net") describes a null result (Sec. 5.1: -0.0004, s.e. 0.0018) as the first contribution; Sec. 1 lists four
contributions in a different order with different content. One list, in one place.

### 3.2 Identification

- **Displacement exogeneity (PSID).** Layoffs and firings are selected (Charles-Stephens 2004, Page-Stevens-Lindo 2009, Hilger
  2016). The paper handles this well for the *parents* (closures-only columns, future-displacement placebo, pre-trend
  controls, self-employment excluded) and honestly for the children (Sec. 7.4: closures kill the Black associations). A
  referee will still ask for the family event study (Tab. 1) with closures only as a parallel table, not a footnote
  (`father_displacement.md` Sec. 2c has it), and for the pre-displacement earnings dip at e=-1 (-2,821***) to be discussed
  as Jacobson-LaLonde-Sullivan selection, not left to a footnote in the output file.
- **The PSID reason-for-job-end measure.** Three waves regimes (pre-1984, 1984-2001, 2003+), 25% of reports undated and
  placed in the year before the interview, calendar 1997 and 1999 undercounted (`father_displacement.md` Sec. 1). The
  2-year-early excess (k=-2, 0.018*) is attributed to "spouses' reports dating the same events a year apart". A referee
  will ask for the whole joint-loss analysis restricted to 2003+ waves (employer-level histories with dated end years) and
  to 1984-1996 (annual interviews). Tab. 2b of `joint_job_loss.md` shows the excess is 0.027 (n.s.) in 1984-89, 0.073***
  in 1990-99, 0.095*** in 2000-21: report this and explain it (measurement, or the rise of dual-earner couples?).
- **Correlated reporting.** In both data sets one household respondent usually reports for both spouses. In the CPS this is
  testable: `PUSLFPRX` (self / proxy / both) is on the basic monthly file. Show the same-month excess among couples in
  which each spouse self-reports (or in which the *wife* is the respondent and reports the husband's loss). This is the
  single most important robustness check missing from Sec. 6.1 and it costs a day.
- **Temporary layoffs in the CPS.** Half of the husband job-loss events are `PRUNTYPE 1` "on layoff" (9,704 of 19,881,
  `cps_joint_job_loss.md` Sec. 3), and the excess is largest for them (0.054*** vs 0.026*** for other job losers). Couples
  who both work at a plant with a seasonal or recall shutdown, or both in school-year jobs, produce joint "job loss" that is
  not displacement. Show the excess (i) excluding PRUNTYPE 1, (ii) excluding June-September, (iii) by major industry of the
  husband, and (iv) for spells that last more than one month (the person is still unemployed at t+2). If the permanent
  job-loser excess is 2.6 points rather than 4.0, say so; it is still 5x the base.
- **Same employer vs same local industry.** The public PSID cannot identify the employer; the CPS "same detailed industry"
  (23% joint loss) is the closest proxy. Hyatt (2019) gives the share of dual-earner couples at the same establishment
  (10-12%). Use it to bound the same-employer channel: if all same-establishment couples lose jobs together with
  probability p and the rest with the base rate, what p reproduces 0.040? Report that bound. The definitive answer needs
  LEHD (Section 5, item 9).
- **Selection into couples and out of marriage.** The joint-loss sample conditions on both spouses working at baseline and on
  the marriage lasting through the window; separation rises after displacement (Tab. 1 col. 6). State the direction of the
  bias (couples that split are dropped, so wives' later outcomes are selected) and show the CPS excess for couples
  observed in all four months.
- **The marriage response (Sec. 5.3).** "Still with baseline wife" falls more for Black fathers (-0.045*** vs -0.019**). With
  closures only? Charles-Stephens find divorce rises after layoffs, not closures, which they read as revealed quality. If
  the Black-White difference survives closures only it is a finding about the fragility of marriage under income risk; if
  not, it is about selection into layoffs. `father_displacement.md` Sec. 2c has the closures-only event study; report
  column 6 of it by race in the paper.

### 3.3 The link to children and the IGE

- The pass-through to children is not credible as a causal estimate and the paper says so (Sec. 7.4). The problem is that the
  title, abstract and introduction still promise it. In Table 5 the Black estimates are null at 0-5 and 6-11 and
  significant only at 12-17; with closures only the Black associations vanish and even turn positive (+0.085); quits
  predict less schooling as well (Tab. 7, -0.296***). A referee will conclude that the PSID cannot identify the child
  effect by race and will ask why 8 pages are spent on it.
- The mediation table (Tab. 6) regresses adult outcomes on post-displacement family income and the mother's hours, both
  endogenous; the paper labels it descriptive, but the introduction uses it ("runs through family income, not the
  mother's hours"). Either drop the causal language or replace the design: the credible version is the *model's* mapping
  from income loss to child outcomes, disciplined by administrative estimates (Oreopoulos-Page-Stevens 2008: -9%; Hilger
  2016: small at 12-29; Uguccioni 2021: -3 to -4 rank points at ages 2-10; Carneiro et al. 2022 on timing).
- Sec. 8 is empty and, according to `EVIDENCE.md` Sec. 8, its content (the wage/hours decomposition of the IGE) now belongs
  to Paper B. Remove it from Paper A entirely.
- The "IGE" in the title. The paper measures the IGE (Sec. 3) and never uses it again except as a promised model output. If
  the model delivers a model-implied IGE and the share of it attributable to fathers' displacement risk, keep the word;
  otherwise the paper is about family insurance and the IGE should go.

### 3.4 The structural model (what it must deliver to carry a top-5 submission)

Sec. 9 is a paragraph. What a referee needs to see:

1. **Household.** Two earners with heterogeneous human capital, each facing a displacement hazard with a *common component*
   calibrated to the tetrachoric 0.24 (0.50 for same-sector couples, 0.18 otherwise; Tab. 4), a search friction (job
   finding of non-employed wives: CPS 7.5% a month, raised to 9.5% after his loss), a wage loss on re-employment (his
   -$6-7k six years out, Fig. 1), savings with a borrowing limit, a child-age-dependent cost of her work (hours response
   +112 when the youngest is 0-5, -26 when 6-17), and a marriage that can end with a hazard that responds to his job loss.
2. **Government.** UI (replacement, duration, eligibility of both spouses), SNAP as a floor keyed to family income, an EITC
   schedule on family earnings, and a childcare price or subsidy. The sharp policy point is already in the data: the EITC
   pays only when someone works, so it is worst exactly in joint-loss states; SNAP rises after displacement (+4 points)
   and is the automatic stabiliser (Tab. 1 col. 8); UI covers only the earner who qualifies.
3. **Children.** Adult outcome as a function of family income by childhood age and of parental presence, with the slopes
   taken from administrative estimates and the PSID associations used as a bound (Tab. 5 is an upper bound on the total
   association). The model's job is to translate the parents' outcomes into the child's, not to estimate the technology.
4. **Estimation.** All endogenous parameters in one SMM run (the PI's rule), targets: joint-loss probabilities by sector
   match and child age (Tab. 4), the annual added-worker response by child age and baseline status (Tab. 1 D-E;
   `father_displacement.md` 2b), the husband's earnings path (Fig. 1), SNAP take-up after displacement, separation after
   displacement by closure/layoff, and the monthly CPS flows of non-employed wives as **untargeted validation** (3.33-3.34
   in `EVIDENCE.md`). Report a model with independent shocks estimated on the same targets so the reader sees what the
   correlation buys.
5. **Counterfactuals the data cannot give.** (i) Set the common shock to zero: how much consumption smoothing and child
   outcome does the correlation cost, by sector match? (ii) UI for both spouses vs the current rules; UI duration in
   recessions (the excess is 6.7 vs 3.6 points). (iii) Replace SNAP with an equal-cost EITC and vice versa, scored on
   consumption in joint-loss states and on children. (iv) A childcare subsidy that lowers the cost of her work when the
   youngest is 0-5. (v) The racial decomposition, if kept: give Black couples the White displacement hazard, the White
   separation response and the White safety-net generosity, one at a time.
6. **Consumption.** The PI has decided against a consumption target (PSID expenditure only 1999-2021). A referee of an
   insurance paper will ask for the consumption drop at a joint vs a single job loss. The minimal answer that respects the
   decision: a food-consumption event study (PSID food at home and away, available in almost every wave 1968-2021) around
   single and joint job losses, reported as a validation check, not a target.

### 3.5 Scope and framing

- Too many threads: IGE measurement (Sec. 3), mothers' time (Sec. 4), birth-margin shocks (Sec. 5.1), displacement and the
  family (Sec. 5.2-5.3), joint loss (Sec. 6.1), search (6.2), the wife's labor market (6.3), earnings comovement (6.4),
  children (Sec. 7), IGE decomposition (Sec. 8), model (Sec. 9), three failed designs (App. A). The PI's "journey" rule is
  about the *order* of the argument, not about including every leg. A journey has one destination.
- Secs. 4 and 5.1 answer the companion paper's question (does a friction hold mothers at work at a birth?) and refer to the
  companion paper five times without a citation. A referee cannot evaluate a paper that leans on another unpublished paper's
  model and estimates (Sec. 9 "the lifecycle model of the companion paper"). The model must be stated in this paper.
- Race. The equal-by-race joint loss is a general finding and the paper treats it as such (good). But the race framing of
  the introduction (racial gap at p25, Chetty et al. 2020) sets up a question the paper's key result does not speak to. Either
  make race a secondary dimension of heterogeneity (my recommendation) or make the paper about race and accept that the
  joint loss is then a side result.
- Terminology: no "offer rate", "rung" or "promotion" in the text (checked). "Search friction" is used correctly.

---

## 4. What to cut, keep, move; the ideal structure

**Cut from the main text**
- Sec. 3 (IGE measurement by race): keep two sentences in the data section; the numbers belong to Paper B.
- Sec. 4 (mothers' time): cut. Both tests are about the companion paper's mechanism. One footnote in the model section
  ("the model's child technology puts no weight on the mother's time because ...").
- Sec. 5.1 (husbands' industry shocks at a birth): to an appendix as a precise null that justifies the model's absence of an
  anticipatory insurance margin.
- Sec. 6.4 (earnings comovement, Black only): appendix; it is from the companion paper's code and is a wage-shock fact, not a
  job-loss fact.
- Sec. 8: delete (Paper B).
- Sec. 2: cut to one third. Six literature subsections is a survey; a top-5 paper has one paragraph per literature with the
  gap stated.
- Sec. 7.2 (mediation table): cut the table; one sentence with the share and the caveat.

**Keep and promote**
- Sec. 6.1 (joint loss, PSID and CPS) becomes Sec. 2-3 of the paper, with the CPS first.
- Sec. 5.2-5.3 (father's displacement and the family, marriage) becomes the "what the household loses" section, with
  closures-only columns in the main table.
- The gross vs net added-worker decomposition, done properly (Section 5, item 3).
- App. A (designs that failed): keep, it is good practice and the PI's rule.

**Ideal structure (journey logic: fact -> what it means for the household -> why it matters for children -> model -> policy)**

1. Introduction (4 pages): the CPS fact in the first paragraph; the household stakes; what the model does; contributions.
2. Data and measurement (3 pages): PSID reason-for-job-end, CPS monthly linkage, definitions, what proxy reporting and
   temporary layoffs can do (with the checks).
3. Joint job loss within couples (6 pages): CPS monthly hazard and timing (Fig. 1 = the monthly event study); PSID event
   study with couple FE and placebo windows; channels (closure, same industry, not the local cycle); magnitudes for the
   model (Tab. 4); heterogeneity (recession, children, race, period).
4. What the household loses and what it does (5 pages): his earnings and the family's income (Fig. 2); her hours by child
   age; gross vs net added work; search at once, jobs slowly (CPS flows); separation; SNAP, UI, AFDC/TANF take-up.
5. The children (3 pages): the PSID associations as bounds, honestly; the administrative estimates the model will use.
6. A two-earner model of undiversified insurance (8 pages): environment, estimation, fit, the independent-shock
   comparison.
7. What correlated job loss does to consumption, children and policy (5 pages): the five counterfactuals.
8. Conclusion (1 page).
Appendices: the birth-margin null; failed designs; the full PSID identification tables; CPS data construction and link
rates; race splits of every table.

Title candidates: "The Insurer Is Hit Too: Joint Job Loss of Spouses and the Limits of Family Insurance"; "Undiversified:
Correlated Job Loss within Couples, Family Insurance and the Safety Net". Keep "children" out of the title unless the
model delivers them.

---

## 5. Prioritised plan

Each item: what, why a top-5 referee needs it, feasibility with data on hand, time.

| # | Item | Why | Feasibility | Time |
|---|---|---|---|---|
| 1 | **CPS self/proxy check** (`PUSLFPRX`); excess among self-reporting couples and among wife-respondent households | Kills the correlated-reporting objection to the headline fact; without it the 10x is contestable | Variable is on the basic monthly files already downloaded (re-request if not in `req_vars()`); one regression per sample | 1-2 days |
| 2 | **Temporary layoffs, seasonality, duration** in the CPS: excess excluding PRUNTYPE 1, excluding Jun-Sep, for spells still unemployed at t+2, by husband's major industry; also by both spouses' class of worker (private / public / self-employed) | Separates displacement from recall layoffs and school-year shutdowns; the "same detailed industry 23%" number may be partly this | All variables in the cached panel | 2 days |
| 3 | **Gross vs net added-worker effect, done in the event study**: wives' hours and employment after his displacement, split by whether she herself reports a displacement in ev-1..ev+1 (descriptive split) and, in the CPS, employment paths of wives who did not lose their job | Replaces the back-of-envelope in Sec. 6.1 with an estimate; this is the paper's reinterpretation of Stephens (2002) and must be shown, not inferred | `19` + `25` samples; one extra interaction | 3 days |
| 4 | **CPS Displaced Worker Supplement 1984-2024 (IPUMS CPS, DW* variables)**: both spouses' displacements in the last 3 years with the *reason* (plant closed, slack work, position abolished); joint plant closings; same-industry concentration | The direct large-sample analogue of the PSID reason-based measure; ~60-80k households per supplement; a referee will ask why it was not used | IPUMS extract via the API (`IPUMS_API_KEY`); the Dropbox CPS folder may already hold the DWS | 1-2 weeks |
| 5 | **SIPP (1984-2008 panels; 2014+ panels), public use**: monthly employment and reason for leaving for both spouses over 3-4 years; joint-loss hazard with longer windows than the CPS's 4 months and the added-worker path over 36 months | Fills the gap between CPS months and PSID years; Banzhaf (2013) and Stevens-Schaller (2011) used it; gives the AWE build-up Stephens found, monthly | Public; NBER/Census downloads; new folder per the PI's one-folder-per-data-set rule | 3-4 weeks |
| 6 | **PSID closures-only versions** of Tab. 1 (family) and of the marriage response by race in the main text; period splits (1984-96 annual, 2003+ employer histories) of the joint loss | Addresses selection into layoffs where it matters (marriage, Black-White differences) and the measurement regime | Already in `father_displacement.md` 2c and `joint_job_loss.md` 2b; writing only | 2 days |
| 7 | **Same-employer bound** using Hyatt's 10-12% establishment-sharing share; plus CPS "same detailed industry x same detailed occupation x same class of worker" as the tightest proxy | Tells the reader how much of the excess is one employer vs one local industry; shapes the model's shock structure | Arithmetic + one CPS regression | 1 day |
| 8 | **Model** (Sec. 3.4 above): code the two-earner model with the common displacement shock, estimate by SMM on the PSID moments, validate on CPS flows, run the five counterfactuals; independent-shock comparison | This is what makes the paper structural and the only route to a top-5 or REStud | Builds on the companion model's code and HPC setup (32 cores, --threads 2, memory per worker, snapshot rules); the child block uses administrative slopes | 3-4 months |
| 9 | **Administrative data application**: Census FSRDC proposal for LEHD (employer-employee links: same-establishment couples, mass layoffs and closures by employer, both spouses' earnings) linked to the CPS/ACS; or the Census-IRS infrastructure | The definitive test of the same-employer channel and of the child pass-through (W-2 earnings of children); referees at top-5 journals will ask whether it was attempted | 12-24 months lead; sponsor and proposal needed; do not condition the paper on it | 2 weeks to write; long wait |
| 10 | **Mass layoffs / WARN**: BLS Mass Layoff Statistics (state-month, 1995-2013) and state WARN notices as an instrument for the local incidence of closures, interacted with the couple's sector match | A referee will ask for a shock that is not the husband's own layoff; with state-only geography in the public PSID the power is low, so this is a CPS exercise (state x month x industry) | LAUS/MLS public; WARN scraping is messy | 2-3 weeks; moderate value |
| 11 | **Food-consumption event study** around single vs joint job loss (PSID food at home/away, most waves) as validation, not target | Insurance papers are judged on consumption; this is the minimal answer consistent with the no-consumption-target decision | PSID family files on disk | 3 days |
| 12 | **Writing**: restructure per Section 4; one contributions list; remove the two contradictions and the over-claim (3.1); state the model in this paper; cite the companion paper properly or not at all; PSID-motivated choices footnoted with numbers and scripts (PI rule) | A referee reads the introduction and Sec. 6 first; both currently misstate what the tables show | — | 2 weeks |

Lower priority / not recommended: Opportunity Insights county data (no couple information; `6.4` in EVIDENCE is fragile);
UKCPR/DOL UI generosity interactions on child outcomes (Sec. 7.4 already shows null and wrong-signed; power is the
problem, and `displacement_id.md` Sec. 5 confirms it); NLSY79 for joint loss (spouse's reason for job end is not
recorded); long balanced panels (the PI's rule, correctly).

Order: 1, 2, 3, 6, 7 (three weeks, all cheap, all needed before anyone outside sees the paper) -> 12 (rewrite) -> 4 and 5
in parallel with 8 -> 11 -> 9 submitted early and run in the background -> 10 only if a referee asks.

---

## 6. Risks and fallbacks

| Risk | Signal | Fallback |
|---|---|---|
| The proxy-respondent check halves the CPS excess | Self-reporting couples show 0.02 rather than 0.04 | The fact survives at 4-5x; report both; the DWS (item 4) uses the same respondent structure, so the PSID 2003+ employer histories and the SIPP become the independent confirmation |
| Excluding temporary layoffs and summer months removes most of the excess | PRUNTYPE 2-3 excess near the base | The paper becomes about recall layoffs hitting both spouses, which is still a joint shock to income, but the "displacement" language must go; UI design (short-time compensation, work-sharing) becomes the policy angle |
| The PSID permanent component (assortative risk) is as large as the contemporaneous one | Couple-FE difference stays at 0.03 with p>0.05 | Lead with the CPS and SIPP; model the correlation as two parts (permanent couple type and common shock), both of which matter for insurance |
| The model with correlated shocks does not fit the added-worker moments better than the independent model | SMM criterion equal or worse | The paper's point becomes that correlation matters for the *distribution* (same-sector couples) and for policy incidence (EITC vs SNAP in joint-loss states), not for the average; report it as such; the PI's parsimony rule then says drop the correlation only if it does not help fit *and* does not change the counterfactuals |
| Children cannot be disciplined (PSID null, administrative estimates disagree: Oreopoulos -9% vs Hilger ~0) | Model child effects span zero | Report counterfactuals in two child-technology scenarios (Canada/Norway slopes vs US tax-data slopes); the parents' consumption and the policy ranking do not depend on the child block; drop "children" from the title |
| The model cannot be estimated before the companion paper's estimates are frozen | Sec. 9 depends on the companion model | Estimate a smaller, self-contained two-earner model for this paper (no fertility, no bargaining), as Birinci (2019) does; the companion paper's full model is not needed for the joint-loss question |
| A referee insists on administrative data | Standard at top-5 for a fact about employers | Apply now (item 9), say so in the paper, and make the CPS+DWS+SIPP+PSID quadruple replication the answer in the meantime |
| Timing/scope: the empirical half is ready but the model is a year away | — | Split: a short fact paper (AER: Insights / AEJ: Applied length, Secs. 2-4 of the ideal structure) submitted now, and the structural paper later citing it; the PI's preference for one structural paper is better served by having the fact established in print before the model is judged |

---

## Summary for the PI

The paper has one result that top journals would care about, the within-couple joint job loss, and it is buried under a
title, an introduction and six sections about a different question. The CPS fact (10x same-month, within state x month x
industry, 1.3m couples, 30 years) is new, large and robust; the PSID evidence is honest but weaker than the text says
(the placebo-window design gives 3.1 points, p=0.077, and future-displaced husbands' wives already show a 3-point excess).
Two sentences in the introduction contradict the paper's own CPS table (wives do search, immediately) and one over-claims
(the joint loss is not why wives insure little on average; it is 2% of the family income loss). The children and IGE
sections cannot carry a causal claim and the model does not yet exist. The route to a top-5 or REStud paper is: establish
the fact beyond reasonable objection (proxy reporting, temporary layoffs, DWS and SIPP replications), reframe the paper
around undiversified family insurance, and build a two-earner model with a common displacement shock whose
counterfactuals (independent vs correlated shocks; UI for both spouses; SNAP vs EITC; childcare) are the paper's
conclusion. Children enter as stakes delivered by the model with administrative slopes, not as PSID estimates.
