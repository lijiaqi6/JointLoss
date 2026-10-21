# Fable: event-study figures for Paper A (2026-10-21)

Asked by the PI ("ask Fable's advice if there is any event study figure that you can plot which may be useful for
us and add them into the paper"). Read-only review of the paper, EVIDENCE.md, HANDOVER.md, the re-estimate plan,
scripts 19/25/30/37/38/40/47/50/63/64/77/78 and paperA_model/panels.py. Fable's report, verbatim below.

## Event-study figures for Paper A: ranked advice

General points that apply to every figure below. (a) Estimator: keep the scripts' stacked design (Cengiz et al.; clean
controls never displaced to ev+6; unit x stack and calendar x stack FE; reference e = -2 in the PSID, s = -3..-1 in
the SIPP). No Sun-Abraham is needed: with never-treated clean controls and stacking there are no forbidden
comparisons. Clustering: 1968 family (PSID), household (CPS, SIPP). (b) PI rule: every figure note lists the key
coefficients with s.e., stars and p (the scripts already write every estimate to output/*.csv; the note cites the
rows). (c) Model overlay: paperA_model/panels.py already builds the data-shaped panels for each design (cps_samples,
sipp_samples, stack_rows, her_stack_rows, cons_rows, wealth_rows), and diagnostics_marriage.py already overlays a
simulated event study (es_still_with_wife.csv) on IGE/19's. So every figure below can take a "model at the estimate"
line later with ~no new infrastructure; plot data only now (the estimate is not reportable: wealth 65% of Q). When
overlaying, use non-temporary losses in the CPS (the model has no temporary layoffs) and the SIPP INV definition.

### 1. The household month by month after a single and a joint loss (SIPP) -- best
- Question / place: what the family loses in the month of the shock and who pays. Section 5 (opens "What the household
  loses"; also carries 5.6 "safety net"). Replaces the two giant footnotes of 5.6 and the unused
  output/safety_net_joint_loss.png (raw means, no CIs).
- Design: 78.SafetyNetJointLoss.py's SIPP event study as coded (husband's involuntary separation at tau, both employed
  at tau-1, wife 25-59; joint = her INV in tau-3..tau+3, 206 events vs 2,644 alone; clean pseudo-event controls; unit
  FE + panel x rotation x month FE; s = -6..+12; reference s = -3..-1; household clusters). Five panels, two lines
  (alone, joint), 95% CIs: his employment; her employment; family monthly earnings (his + hers, as a share of the
  pre-period mean; 60's earnings extract already in the panel); UI receipt of either spouse and SNAP receipt; no earner
  and no UI. Pooled only.
- Extend: 78 already estimates the regressions by bins; change to month-by-month dummies and add the earnings outcome
  and the figure call (its plotting code draws weighted means now).
- Model moment: yes, the closest of all. The counterfactuals are scored on "consumption in the month of the loss and
  over 12 months, share of couple-months with no earner and with no earner and no credit"; sipp_samples gives the same
  window. Also shows the SIPP his-search targets (3, 6, 12 months) as a path.
- Risks: no race split (6 Black joint same-month events); the -5.9 pre-trend at s = -6..-4 from conditioning on both
  employed at s = -1 must be shown, not hidden; SNAP after a joint loss is imprecise (p = 0.14).
- Informative either way: shows the "no-earner, no-benefit" months the EITC cannot reach (the policy argument) and the
  family-earnings trough that Section 5.2 claims ("the month in which income falls most") but never plots.

### 2. The wife's response in months: search at once, jobs slowly, net of her own loss (SIPP + CPS)
- Question / place: the paper's reinterpretation of the added-worker effect. Section 5.2-5.3. The present evidence is
  annual (fig_gross_net_awe, net +12-16 hours n.s.); the monthly version carries the argument. Two panels: (A)
  non-employed wives at tau-1: looking and employed, s = 0..36 (40's design) with the CPS t+1, t+2, t+3, t+12
  estimates (30; already drawn in paperA_joint_loss/fig_cps_monthly_hazard_awe.png panel B) as markers; (B) change in
  employment since tau-1 for all wives (net), wives without a job (gross) and wives employed at tau-1 (their own loss),
  s = 0..36 -- panel D of output/sipp_joint_loss.png, which exists and is not in the paper.
- Extend: 40.SIPPJointLoss.py (figure only; estimates exist, EVIDENCE 3.61, 3.63) plus the CPS points from 37's figure
  routine.
- Model: direct. SIPP s = 0, 1, 6 employment and CPS entry are targets; CPS "looking" at t+1 (8.8 points) and SIPP
  months 12-36 are the paper's named validations. The gross/net split is the counterfactual (i) mechanism.
- Risks: Black wives' SIPP path (s = 12: -0.023 vs +0.052 White, p = 0.078) is too noisy for a race panel; put race in
  a footnote. Pre-period +0.03 at s = -6 (recent leavers) must be shown.
- Either way: if the model's employment build-up is faster or slower, that pins lambda_w; a flat "looking" line in the
  model would reveal the simulated search rule.

### 3. Separation after his, her and a joint loss on one figure (PSID)
- Question / place: Section 5.5 is 1,000 words of text and footnote with no figure. "Still together" by year -3..+6
  for: his displacement alone, hers alone, joint (both within a year); pooled, from one stacked regression (65's joint
  design, 1,205 displaced wives, 174/244 joint events); race in an appendix version.
- Extend: 64.SeparationUIAndHerLoss.py / 65.HerLossRobustness.py (output/bw_present_by_year.csv already holds his path
  by year; add hers and the joint line to the same regression and plot).
- Model: yes; diagnostics_marriage.py already produces the simulated path, and the known shape mismatch (model gap stops
  widening after year 3, PSID keeps widening, most for Black couples) is the kind of thing this figure should show at
  the estimate.
- Risks: outcome is 1 by construction before the event (state this in the note; no pre-period test); joint-loss CI is
  wide (that is the finding: 9.5 vs 4.1 points, p = 0.15).

### 4. Her displacement as the event: what the husband and the family do (PSID)
- Question / place: the paper now treats her loss only through the marriage; the model's F is identified by
  consumption after her loss, and the husband block assumes he does not add work. Six panels, stacked design with roles
  reversed (64's M3 sample: wives of male heads with children, worked at baseline, events 1984-2021), e = -3..+6,
  pooled with race lines: her hours, her labor income, his hours, his labor income, family income, food stamps. Goes
  in Section 5 as a short subsection "The wife's job loss" (or Appendix B).
- Extend: 64 (her_stack design) with 19's outcome list.
- Model: yes, panels.her_stack_rows exists; her earnings loss years 1-3 (-4,608) is a target; his hours after her loss
  is an untargeted test of the husband block.
- Risks: Black displaced wives are a few hundred; his hours response may be a precise zero -- still informative
  (justifies the husband-as-given modelling, husband-side-inputs rule).

### 5. Liquid wealth and debt around his displacement (PSID wealth waves)
- Question / place: wealth is 65% of the objective and the pending PI decision is the net-worth target (script 77); the
  paper says families draw on savings but never shows it. Section 5.4 becomes "Consumption and wealth". Outcomes by
  wealth interview relative to the job-end year (47's wave-time design: k = -1 last wave before, +1, +2): share with
  liquid wealth <= 0, IHS liquid wealth, share with unsecured debt, net worth without home and vehicles (77's
  definition c'); single displacements only, pooled and by race.
- Extend: 47.PSIDConsumptionEvent.py's stack-by-wave code with 77's definitions and 60's wealth sample.
- Model: yes (panels.wealth_rows; the borrowing limit a_bar and the "smoothing technology" step 5 are exactly what this
  disciplines).
- Risks: wealth waves are 1984/89/94 then biennial, so events are effectively 1999-2017 and the bracketed sample is a
  few hundred displaced husbands; wealth is skewed (use shares and IHS, not dollar means); no joint-loss split (63
  events). Either way informative: a fall in liquid wealth means savings insure; no fall means credit, transfers or
  illiquid assets do, which is what the misfit suggests.

### 6. Joint loss and the added-worker effect by age (CPS)
- Question / place: the "By age" paragraph of Section 4 (the contrast with Bacher et al.: the spouse who can enter is
  available when young, the spouse who is lost is lost at every age) has no figure. Two panels by spouse's age group
  20-25...56-62: (A) AWE, Bacher definition, with their published values as hollow markers; (B) wife's same-month
  excess, with and without temporary layoffs. 95% CIs, Wald p for equality in the note.
- Extend: 50.CPSAddedWorkerByAge.py (estimates in output/cps_awe_by_age.csv; the png exists).
- Model: validation (AWE by age is a named untargeted check; no parameter depends on age).
- Risk: none material; cheapest of the six.

### Existing figures: what to change
- father_displacement_es.png (8 panels): cut to four (his hours, his labor income, family income, food stamps) by race;
  the AFDC/TANF panel is flat and in the text, the wife panels duplicate fig_gross_net, and "still with wife" moves to
  figure 3. Add the model line later via stack_rows.
- joint_job_loss_es.png (PSID, 3 panels, 3 lines each): the "any reason" panel is not discussed; the race lines have
  CIs wider than the effect. Redesign as pooled only, two panels (displaced; employer closed), shading the placebo
  window, or move to Appendix C since the CPS figure is the headline and Table 1 carries the PSID numbers.
- fig_gross_net_awe: keep the hours panel only (hours are the targeted added-work moments) and pair it with figure 2;
  the employment panel is redundant.
- fig_cps_monthly_hazard and fig_consumption_single_joint: keep as they are (for consumption add the reference k = -2
  estimates as hollow markers, since her loss can precede the k = -1 interview).

### Do not plot
- Any joint-loss path by race in the SIPP (6 Black joint events) or consumption joint-vs-single by race (29/34
  events): CIs would swallow the point estimates and invite a race reading the data cannot support.
- PSID "looking for work" event study (wife_search_es.png) or the NLSY79 quarterly paths: the annual snapshot misses
  the search spell by construction (the text already explains this), and the NLSY has no spouse job-loss reason; a
  figure would read as a null against the CPS.
- Children's adult outcomes as event studies: they are bounds, not event-time objects, and the pre-displacement
  differences (income -24 log points, behaviour problems) would dominate the picture.
- The EITC schedule position: it is accounting on a schedule, not receipt; keep it as text.
- Separation by UI generosity (64's M2b): state-year variation only, no region x year allowed, and no result in the
  evidence ledger; not figure material.
