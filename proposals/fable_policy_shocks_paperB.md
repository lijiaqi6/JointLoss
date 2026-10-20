# Connecting Paper B to the effect of public policies and economic shocks on disparities

Memo from Fable (editor / strategic adviser), 2026-10-18. Question from the PI: *"How can we connect the entire paper
with the effect of public policies and economic shocks on disparities?"* Read for this memo: Paper B (main.tex,
sec1-sec8, appA, appB, the main-text tables), `fable_review_paperB.md` (round 2), `paperB_review_execution.md`,
`paperB_model_document.md`, `EVIDENCE.md` (sections 1-9 and the PI-question table), `PLAN.md`,
`proposals/safety_net_ige.md`, the docstrings of scripts 8, 8a, 12, 12a, 12b, 17, 18, 19, 22, and the contents of
`data/policy_calendar.csv`, `data/ui_generosity.csv`, `data/state_shocks.pkl`. Nothing was run; no other file was
edited. Every estimate quoted carries the paper's stars and a standard error or p-value. Estimates are White minus Black
unless stated. References I could not re-check in this session are marked (verify).

The PI's constraints are respected throughout: public files only (no FSRDC, SIPP-SSA, IRS/LEHD, restricted geocodes,
no requests to US teams); one joint SMM run with parsimony; no duplication of Paper A; no region x year fixed effects
in state-policy designs; no sibling controls; "human capital level / accumulation" and "search friction"; no result
dismissed because it is equal by race; no precise share called "small".

---

## 1. Framing: partial connection, not a reframe

### 1.1 The honest answer

The paper should **not** be reframed as "the effect of public policies and economic shocks on disparities". Three
reasons.

1. **Its identification is not policy variation.** The paper's strength is a measurement fact (the log IGE of sons'
   earnings rises from 0.276\*\*\* (0.024) at 25-29 to 0.492\*\*\* at 40-44; the White-Black gap is -0.041 (0.045) at
   25-29 and 0.294\*\*\* (0.067) at 40-44; opening 0.232\*\*\* (0.052) on bands 25-49; 0.086\*\*\* (0.024) with one year
   of parental income in four data sets, 0.191\*\*\* (0.046) corrected) plus a descriptive mechanism (the job at 25-34
   accounts for 0.493\*\*\* (p=0.004) of the divergence; access to G jobs 20.2 vs 4.7 percent by parental tercile and
   0.042\*\*\* (0.016) by race at equal parental income; the rise of the return to schooling differs by 0.055\*\*\*
   (0.014), 0.061\*\*\* (0.018) within the early job cell) plus a structural model. A title that promises causal effects
   of policies invites the question "where is the policy variation?", and the PI's own power check
   (`safety_net_ige.md`, Section 3.4: the state-year variation in AFDC+FS left after fixed effects has a standard
   deviation of 0.03 log points; EVIDENCE 6.3) already says the public PSID cannot answer it for the safety net. The
   same arithmetic holds for most state policies: 500-1,700 Black sons per age band, spread over 51 states and
   forty entry years.
2. **The racial gap is a structural, not a cyclical, fact.** The opening is 0.17-0.28 and significant in every cohort
   born 1951-64, 1965-79 and 1980-89 (EVIDENCE 1.25, 1.33), which entered the labor market in different recessions,
   different trade regimes and different policy eras. No single policy or shock in the PI's list produces a gap that is
   this stable across forty years of entry cohorts. A paper framed around a policy would have to explain why the
   policy's removal did not change the fact.
3. **The paper already contains its policy contribution, and it is a general one.** Section 7's point that a policy
   scored at 30 looks different from the same policy scored at 45, and differently so by race, applies to every
   long-run evaluation of a childhood or entry policy that measures earnings in the late twenties or thirties: the PSID
   studies of Food Stamps (Hoynes, Schanzenbach and Almond 2016), school finance (Jackson, Johnson and Persico 2016),
   the EITC (Bastian and Michelmore 2018), the administrative studies that stop at 31-37 (Chetty, Hendren, Jones and
   Porter 2020; the Opportunity Atlas used for place-based policy), the MTO adult outcomes measured in the mid-twenties
   (Chetty, Hendren and Katz 2016), and the MVPF calculations that project earnings from those ages (Hendren and
   Sprung-Keyser 2020). The paper's fact says the racial comparison of all these estimates depends on the age of
   measurement. That is a contribution to the policy-evaluation literature that needs no new causal design, and the
   paper under-sells it: it is one sentence in the conclusion.

So: a **partial connection** that strengthens the paper, built from four pieces, each of which touches the paper's
mechanism (the first decade; access to good starting jobs; the pay-off of schooling; the age of measurement):

- **(i) The age of scoring** as the paper's stated policy contribution (Section 1.3 below), demonstrated on the
  paper's own objects and on one shock the PI has already estimated (fathers' displacement in childhood, Paper A's
  scripts 19 and 22), re-scored by the son's age and race.
- **(ii) One shock design that acts on the mechanism**: labor-market conditions at entry and over the first decade
  (state unemployment at the parental state when the son leaves school; the mean over experience 0-9), with access to G
  jobs, the wage at 25-34 and 35-44, and the IGE at 30 vs 45 as outcomes, by race and parental income (Section 2,
  design D1). It is the one shock in the PI's list for which the paper's mechanism makes a sharp prediction, for which
  the public data have the geography (PSID state of residence from the family files; ACS state of birth), and for
  which the literature gives magnitudes to compare with (Kahn 2010; Oreopoulos, von Wachter and Heisz 2012; Schwandt
  and von Wachter 2019; Altonji, Kahn and Speer 2016; Rothstein 2023).
- **(iii) One policy decomposition that is also a mechanism check**: the public sector as the employer of Black men
  (Section 2, D2). It is a policy (public employment), it is observable in the PSID (class of worker), and it bears
  directly on the paper's puzzle of a Black return to schooling that is high at 25-29 and flat afterwards.
- **(iv) The model as the policy instrument**, with every counterfactual named after the policy or shock that moves
  the parameter, one minimal shock block (one parameter), and the entry-conditions design used as external validation
  in the Voena / BPS style (Section 3).

Everything in the PI's list that acts on childhood resources (EITC, school finance, safety net) or on the parents'
generation (joint job loss, UI as family insurance, SNAP) stays with Paper A; the division is stated in Section 1.4.

### 1.2 Pitch and titles

**One-sentence pitch.** The racial gap in intergenerational persistence is built in the first decade of the career
and is invisible before 35, so policies and shocks that act on the start of careers, entry conditions, access to good
jobs and schooling, have effects on racial disparities that evaluations at 30 misstate; this paper measures when the
gap is built and where, and uses an estimated career model to score policies and shocks at 45.

**Title options** (keep the fact in the title; the policy connection goes in the subtitle or the abstract's last
sentence):

1. *Built in the First Decade of the Career: The Age Profile of Intergenerational Persistence and the Black-White Gap*
   (current; add to the abstract: "Policies and shocks that act on the start of the career are therefore mis-scored
   at 30: a recession at entry / equal access to good jobs ... at 45.")
2. *Scored Too Early: When Intergenerational Persistence Is Measured, and What It Does to the Racial Comparison of
   Policies*. Sharper on the policy contribution; weaker on the fact.
3. *The First Decade: Entry Conditions, Access to Good Jobs and the Racial Gap in Intergenerational Persistence*.
   Right if design D1 delivers a clear result; premature now.

My recommendation: option 1 now; revisit option 3 after D1.

### 1.3 How each part of the paper connects

| Paper part | Current content | Connection to policies and shocks | What to add |
|---|---|---|---|
| Sec. 1 (intro) | the fact, the mechanism, the model's policy question | the age-of-scoring lesson for the long-run policy-evaluation literature (list above); the shocks that act on the first decade | one paragraph with the pitch; one sentence per piece (i)-(iv); cite the PSID-based evaluations whose racial comparisons the fact re-weights |
| Sec. 3 (age profile) | fact and precision | the opening is stable across entry cohorts that faced different recessions and policy eras (EVIDENCE 1.25: 0.195\*\* (0.082), 0.093 (0.092), 0.160 (0.099), differences n.s.; earnings 0.17-0.28, all p<0.05) | re-read the cohort rows as "no single shock or reform produces the fact"; add the 1980-82 and 1990-91 and 2001 entry cohorts explicitly in the footnote |
| Sec. 4 (what opens) | wages, not hours, shocks or marriage | sons' own shocks do not carry the divergence: instability gradient equal by race (p=0.524), purging shock years moves the gap by 0.002 (0.042) | say it as a policy statement: insurance against the son's own job loss acts on levels and instability, not on the slope; displacement falls with parental income equally by race (-0.037\*\*\* (0.009) W, -0.038\*\*\* (0.014) B), so family background buys the same protection in both races (a finding, not a null) |
| Sec. 5 (careers) | the job at 25-34, access, schooling | **D1**: do entry conditions move access to G and the wage gradient, by race and parental income? **D2**: the public sector's role in Black sons' starting jobs and flat returns; **D4**: UI at the son's displacement and the human-capital cost of job loss | one subsection "Shocks to the start of the career" (D1, D2 as a paragraph each, details in footnotes); D4 one paragraph in 5.5 |
| Sec. 6 (fathers) | networks, family business | the inheritance of a family business is a transfer of assets, a tax / estate policy object, with 21 vs 8 percent of sons having a self-employed father; following the father's industry pays 0.079\*\*\* at 25-34 | one sentence each; nothing new |
| Sec. 7 (model) | parameters, nested models, four experiments | each parameter mapped to the policy or shock that moves it; one entry-shock parameter; validation against D1; counterfactuals scored at 30 and 45 | Section 3 of this memo |
| Sec. 8 (conclusion) | measurement and policy implications | the demonstration (D3): the father's displacement in childhood re-scored at the son's 25-34 vs 35-44 by race | two paragraphs |

### 1.4 The division with Paper A

| Question | Paper A | Paper B |
|---|---|---|
| Generation hit by the shock | the parents (father's and joint job loss) | the son, after entry |
| Timing | childhood exposure; family insurance in the year of the loss | entry year and the first decade of the career |
| Safety net | UI, SNAP, EITC, TANF as insurance for the family and resources for children | none, except UI at the son's own displacement as insurance of his human capital (D4), stated as Paper B's only safety-net object |
| Macro shocks | state unemployment at a birth (8.FirstStage: -0.0147\*\* (0.0060) per pp on mothers' employment, equal by race: ur x Black 0.0012 (0.0045)) | state unemployment at the son's entry and over experience 0-9 (D1) |
| Policy levers in the model | floor vs work-conditioned transfers; UI; childcare | access to good jobs; the pay-off of schooling; displacement risk and depreciation; schooling; entry conditions |
| The age of measurement | takes the son's earnings at the ages Paper B says (35+) | supplies the rule |

Write this table (as a paragraph) into both papers' introductions. One rule to prevent drift: a shock to the son's
career is Paper B's; a shock to the household he grew up in is Paper A's; the father's displacement re-scored by the
son's age (D3) is the one shared object and is reported in both with the same numbers.

---

## 2. Reduced-form designs that fit the mechanism

Ranked by credibility x feasibility x relevance to the mechanism. Times are working days for one person with the
existing scripts. Geography available in public files: PSID state of residence in every family-file wave (the mapping
to FIPS exists in `8.FirstStage.py`); NLSY79 and NLSY97 public files have region only (`12.FMLA.py` docstring), so NLSY
designs use national conditions by cohort; CPS MORG has current state; the ACS (IPUMS `usa 1` extract) has state of
birth.

### D1. Labor-market conditions at entry and over the first decade (rank 1)

- **Variation.** (a) The state unemployment rate in the year the son leaves school (age 18 + max(e-12, 0), the model's
  entry age), measured in the *parental family's state of residence when the son was 17* (intent to treat, as Schwandt
  and von Wachter 2019 use state of birth), from BLS LAUS 1976-2024 (`state_shocks.pkl`, `ur`); (b) the mean of the
  same rate over the son's first ten years of potential experience; (c) the men's Bartik (`bartik_m`, leave-one-out)
  as the demand-side variant. Sons entering before 1976 (born before about 1958, a quarter of the sample) get the
  national rate only or are dropped in the state version.
- **Data and identifying assumption.** PSID sons of the benchmark sample (1,995 Black, 2,758 White). State FE and
  entry-year FE; identification from state deviations from the national cycle at entry, conditional on the son's
  schooling, parental income and race. No region x year FE (they would absorb the Southern recessions that identify
  the Black effect). Complementary specification: national unemployment at entry with a linear cohort trend, which
  uses the 1975, 1980-82, 1990-91, 2001 and 2008-09 entry cohorts and is the only version the NLSY79 (born 1957-64,
  entering 1975-86) and NLSY97 (born 1980-84, entering 1998-2008) can run. The ACS 2000-2023 by state of birth x
  cohort x race x education gives the scar on wages and on the return to schooling to 20 years of experience with
  millions of observations and no parental income; it is the well-powered leg for the schooling part of the
  mechanism.
- **Outcomes in the paper's objects.** (1) Access: P(G at 25-34), the Table 8 definition; (2) the log wage at 25-34
  and 35-44; (3) the IGE at 25-34 and 35-44 by race for sons who entered in slack vs tight markets (above / below the
  within-state median of the entry rate), i.e. the opening of the gap by entry conditions; (4) the return to schooling
  by experience band by race in the ACS, interacted with the entry rate.
- **Predictions of the mechanism.** A slack entry lowers the probability that the first offer is G (the model's
  p(x, e, r) with an entry shifter). If sons of richer White parents are insured against it (they get G jobs through
  networks and schooling anyway, consistent with "a father who held such a job raises his son's chance by 0.064\*\*
  (0.025)") and sons of poorer parents and Black sons are not, a recession at entry *steepens* the White IGE at 45 and
  leaves the Black one flat: it widens the racial gap in persistence measured at 45 while being invisible at 30. If
  the scar fades through job mobility, as Oreopoulos et al. find in Canada, it fades faster for those who can reach G
  jobs later (the search friction lambda_G and the access function), which is again White sons of richer parents. The
  literature already says the scar is larger and more persistent for nonwhites and the less educated (Schwandt and von
  Wachter 2019) and that it operates through job quality for college graduates (Kahn 2010; Altonji, Kahn and Speer
  2016); none of it has parental income.
- **Power.** Within state and year FE the entry rate has a standard deviation of about 1.5 pp. With 2,758 White sons
  and a binary G outcome (s.d. 0.37) the standard error of the main effect is about 0.5 pp per pp of unemployment; a
  Kahn-sized effect on job quality (several percent per pp) is detectable, a 2-percent-per-pp effect is not. For the
  log wage at 25-34 (son means, s.d. about 0.8) the standard error is about 0.010 per pp, so the -2 to -6 percent per
  pp of the literature is detectable by race. The interaction with log parental income (s.d. about 0.8) has a standard
  error of about 0.013 per pp per log point: a parental-insurance interaction of 0.02-0.03 is at the margin. **The
  triple interaction with race is underpowered** (s.e. about 0.02): report it, and let the model produce it (Section
  3.3). The ACS leg is powered for every race x education x experience cell.
- **Informative either way.** If entry conditions lower G access and the scar at 35-44 is larger for Black sons and
  for sons of poorer parents, entry shocks are a cause of the opening, the model needs the shock block, and macro
  policy (running the economy hot when a cohort enters) is a lever on the racial gap at 45. If entry conditions do not
  move G access, access is determined by persistent factors (networks, race, schooling), the gap is structural, the
  block is dropped under parsimony, and the paper says that cyclical policy cannot close the gap; that null is a
  finding and is written in the text, not the appendix.
- **Time.** 7 days PSID (state at 17 from the family files, entry year, the three outcomes, by race; one script,
  `47.EntryConditions.py` or next free number), 3 days NLSY national version, 4 days ACS. Total about three weeks with
  tables.

### D2. The public sector as the employer of Black men (rank 2)

- **Variation and data.** Class of worker (government vs private vs self-employed) of the son at 25-34 in the PSID
  family files (heads from 1976, wives later), and the CPS MORG class of worker to split every occupation x industry
  cell's wage level and later growth into public and private. Policy content: public employment has been the main
  route of Black men into well-paid, stable jobs since the 1960s (Donohue and Heckman 1991 on the South; Miller 2017 on
  affirmative-action regulation of federal contractors); its pay scales compress growth after 35; it contracted in
  the 1980s and in 2009-12 (Laird 2017, verify).
- **Why it bears on the mechanism.** The paper's Black profile, a return to schooling of 0.124\*\*\* at 25-29 that
  does not rise, and a parental-income gradient of same-employer growth that is a precise zero (0.003 (0.008)), is
  what a sector with high entry pay given schooling and flat scales produces. The within-cell test (0.061\*\*\*
  (0.018)) holds the 11 x 33 cell fixed, and public administration is an industry group, but teachers, health workers,
  postal and transit workers sit in cells that mix public and private employers. The test is cheap: the opening of the
  racial gap among private-sector starters only; the return to schooling by age within sector by race; the share of
  Black sons of top-tercile parents who start in government (my expectation from the CPS: well above the White share).
- **Outcomes in the paper's objects.** The G/O split by sector; access to G by race within the private sector; the
  rise of the return to schooling within sector; the opening among private starters.
- **Power.** Sector is observed for most son-years; the sector x race x band cells hold hundreds of sons. The opening
  among private starters has a standard error of about 0.06-0.07, enough to say whether it is the full-sample 0.232.
- **Informative either way.** If the racial difference in the schooling rise is as large within the private sector,
  public employment is not the explanation and the model's gamma_1(r) stands. If it halves, public employment is a
  third job type (high entry pay, low displacement, flat accumulation) that Black sons of richer parents choose, which
  is a policy (public-sector pay compression and hiring) and changes the model (Section 3.4). Either way it is a
  policy fact worth a table.
- **Shock variant (optional, 2 days).** State x year government employment growth (CPS MORG, 1979-2019) at the son's
  entry, as a second shifter of access to public jobs by race. Weak; report only if D1's state version works.
- **Time.** 5 days.

### D3. A childhood shock re-scored by the son's age: the father's displacement (rank 3; the demonstration of the age-of-scoring lesson)

- **Variation and data.** The father figure's displacement at the son's ages 0-17 (scripts 19 and 22; closures and
  layoffs; about 740 Black and 1,390 White exposed children with adult earnings, from the UI-receipt split cells of
  `displacement_id.md`, Section 4). No new data.
- **Design.** The 22 design (controls: pre-event family income, parental education, birth-year FE), with the son's
  outcome split into 25-34 and 35-44 and the treatment interacted with the band and with race. The cross-family
  association is an upper bound (EVIDENCE 5.1-5.7); the question here is not its level but its *age profile*.
- **Prediction.** If the shock works through schooling and access to G (EVIDENCE 5.1: schooling -0.3\*\*\*), its
  measured effect on White sons' earnings should grow from 25-34 to 35-44 as the return to schooling and the G
  premium build, and stay flat for Black sons.
- **Power.** Effects of about -0.10 per band per race with standard errors of about 0.05; the change across bands by
  race has a standard error near 0.07: the pooled change is testable, the race difference in the change is a bound.
- **Informative either way.** A growing measured effect shows the paper's fact at work in a shock evaluation and gives
  Paper A its measurement age. A flat profile says the childhood-shock channel runs through levels (h_0), which the
  model carries anyway. Both go in the conclusion.
- **Time.** 3 days.

### D4. UI generosity at the son's own displacement and the human-capital cost of job loss (rank 4)

- **Variation and data.** State x year maximum weekly benefit, replacement rate and maximum duration
  (`ui_generosity.csv`, 1976-2024) at the state and year of the son's displacement; PSID displacement events of sons
  (the 37 percent of Black and 19 percent of White son-years with displacement or unemployment give several thousand
  events). State and year FE.
- **Outcomes.** The wage loss two to three years after displacement (0.131\*\*\* in the paper, of which 0.028\*\*\* is a
  lower occupational score), the probability of re-employment in a G cell, and the loss by race. The model objects are
  kappa (depreciation out of work) and the match component lost at displacement, and counterfactual 4 ("insurance
  against job loss").
- **Identifying assumption.** The standard UI-generosity one (Cullen and Gruber 2000 for the PSID): state benefit
  schedules are not set in response to the fortunes of individual PSID families. The literature is split on sign:
  longer UI lowers re-employment wages in Germany (Schmieder, von Wachter and Bender 2016) and raises match quality
  in Austria (Nekoei and Weber 2017) and, with SIPP state variation, in the US (Farooq, Kugler and Muratori, NBER WP,
  verify).
- **Power.** With about 3,000 events and a one-standard-deviation difference in generosity, a 0.03-0.05 effect on the
  log re-employment wage is detectable pooled; by race, about 0.05-0.07.
- **Why Paper B and not A.** Paper A's UI is household insurance (consumption, the spouse's response, the safety net
  after a joint loss). Paper B's UI is insurance of the son's own human capital: whether a better-insured search ends
  in a G job. State it that way in both papers.
- **Informative either way.** An effect gives counterfactual 4 an empirical scale (the kappa reduction equivalent to
  one s.d. of generosity). A null says UI generosity does not change where displaced sons land, and the insurance
  counterfactual is reported as a bound on kappa, not as a UI policy. The paper's existing result that displacement
  falls equally with parental income in both races stays in the text either way.
- **Time.** 5 days.

### D5. Industry shocks to the son's early job and to the father's industry (rank 5; appendix check)

- **Variation.** National leave-one-out employment growth of men in the son's industry group at 25-34 and in the
  father's industry (the 16-sector shocks of `8a.StateShocks.py`; the ADH import-exposure measures at the industry
  level for 1991-2007). The PSID has both industries; deindustrialisation hit Black men's manufacturing jobs in the
  1980s (Bound and Freeman 1992; Bound and Holzer 1993).
- **Why only an appendix check.** Industry explains 0.081 (n.s.) of the divergence (EVIDENCE 9.15), following the
  father's industry pays at entry (0.079\*\*\*) and accounts for -0.002 of the change in the gap, and the cohorts that
  entered after the manufacturing decline show the same opening. The check is: the opening among sons whose early
  industry group grew vs shrank nationally over their first decade. A triple interaction with race and parental income
  is beyond the data.
- **Time.** 2 days on scripts 32 and 35.

### Candidates rejected, with reasons

| Candidate | Reason | What to say in the paper |
|---|---|---|
| Minimum wage | acts on the bottom of young men's wage distribution, not on access to G or on the schooling pay-off; the zero gap at 25-29 is already shown not to be a bottom-of-the-distribution artefact (PPML opening 0.257\*\*\* (0.061)); state MW variation is mostly post-1990 (Cengiz et al. 2019) | one robustness row at most (opening by the state Kaitz index at 25-29, half a day, from `policy_calendar.csv`); not a design |
| State affirmative-action bans (CA 1996, WA 1998, FL 2000, MI 2006, NE 2008, AZ 2010, NH/OK 2012) | cohorts exposed are born after 1978; few Black PSID sons entered in ban states after a ban and are observed at 35-44; the mechanism in the literature is college quality (Bleemer 2022: Prop 209 lowered URM applicants' wages by about 5 percent with no fade-out; Hinrichs 2012), which the model's schooling in years does not carry | cite as external evidence that the access channel is policy-sensitive; no design |
| State higher-education funding / tuition / merit aid (Georgia HOPE 1993 and about a dozen Southern programs) | the lever the model's "equalising schooling" experiment represents, and the SEO's Southern families give unusual Black coverage; but first stages on completed schooling are modest (Dynarski 2000) and ACS studies find no long-run earnings effects (Sjoquist and Winters 2015, verify); an IV in the PSID would be weak (round-one rule: no weak IV) | one sentence in the model section: the schooling experiment is the ceiling for what tuition policy can do |
| EITC expansions | act on parental income in childhood (Bastian and Michelmore 2018, PSID: +2.2 percent earnings per $1,000 of exposure at 13-18); the childless EITC is negligible for sons | Paper A |
| Anti-discrimination enforcement (Title VII thresholds, EEOC activity, the 1991 Act) | state fair-employment laws predate the cohorts; employer size is unobserved in the PSID; EEOC charge data by state are public only from about 2009 | the model's a_3 is the object enforcement moves; the counterfactual a_3 = 0 is the perfect-enforcement bound and is labelled so |
| Occupational licensing | licenses reduce the racial wage gap (Blair and Chung 2019), consistent with a credential substituting for an under-rewarded schooling signal; but state x occupation licensing data exist only from the 2010s and the PSID has no licensing item | one sentence next to gamma_1(r) |
| School finance reforms (Jackson, Johnson and Persico 2016; Lafortune, Rothstein and Schanzenbach 2018) | act on h_0 and e; the PSID-based estimates used restricted district geocodes; a state-event version with a few hundred exposed Black sons cannot carry an age interaction | cite in the age-of-scoring paragraph: these evaluations measured earnings before the age at which the racial gap opens |
| End of the draft (1973) / draft lottery | lottery numbers need exact birth dates (not in the public PSID); the volunteer force is a single national date; military service is part of D2's public-employment question (Angrist 1998) | descriptive sentence in D2 |
| Opportunity Atlas x county entry conditions | 31-37 ranks, which the paper shows are flat in age; 17.AtlasFrictions found fragile cross-state associations (EVIDENCE 6.4) | no |
| Great Recession as the NLSY97 cohort's entry shock | one national event for one cohort; not identified | ask the model (Section 3.3): with the entry block estimated on the PSID, does a 2008-09 entry reproduce the NLSY97's smaller opening (0.058 (0.040))? A validation, not a design |

---

## 3. The model side

### 3.1 Parameters mapped to policies and shocks

| Parameter | What moves it in the world | Counterfactual (scored at 30 and 45, by race, mu_r fixed) | Status |
|---|---|---|---|
| e(x, r) | tuition, merit aid, school finance (pre-entry; taken as given) | 1. equalising schooling | in Sec. 7 |
| a_3 (race in access) | anti-discrimination enforcement, affirmative action in hiring, public-sector hiring | 2. equal access, a_3 = 0 (perfect-enforcement bound); a_3 halved | in Sec. 7; add the half |
| a_1 (parental income in access) | referral and network channels; job-search assistance for entrants | 2b. **equal access by parental income** at the same mean: a_1 = 0 | **add**: it is the counterfactual that says how much of the IGE at 45 (not only the racial gap) is access; the paper's findings are not only about the gap |
| gamma_1(r) | credentials, training, employer practices (licensing is the closest policy) | 3. equal pay-off of schooling (only if model C is selected) | in Sec. 7 |
| delta_0r, delta_1 | job security; the displacement gap 0.176 vs 0.103 at 25-34 | 4a. **equal displacement risk**, delta_0B = delta_0W | **add**: the paper says instability does not produce the divergence (purging 0.002 (0.042)); the model should show the same, and the effect on levels and on the rank intercept is a result in its own right |
| kappa, match loss | UI, re-employment services | 4b. insurance against job loss, scaled by D4 | in Sec. 7; scale from D4 |
| theta (new, entry shock) | the state of the labor market at entry: macro policy | 5. **a recession at entry** (+3 pp for one cohort) and **a tight first decade** (-2 pp over experience 0-9) | **add**, Section 3.2 |

Add to Table modelid one column, "policy or shock", with the entries above; it costs nothing and changes how an
editor reads the section.

### 3.2 The minimal shock block, and parsimony

Add one parameter. The entry-year labor-market state z (the state unemployment rate at the parental state in the
entry year, demeaned by state and year, or the national rate demeaned by a trend) enters the access logit:

  p(x, e, r, z) = Lambda(a_0 + a_1 x + a_2 e + a_3 1[Black] + theta z),

for every offer drawn in the first K years of the career (K = the number of years the D1 scar is visible in G access;
K is fixed from D1, not estimated). Nothing else changes: the same friction, the same accumulation. Reasons for this
form and not another: (i) the paper's mechanism is that the first decade builds the gradient through G access, so a
shock to G access is the shock the model can speak to; (ii) one parameter, one moment (the D1 coefficient of P(G at
25-34) on z, pooled), so it is identified by construction and the Jacobian column is not collinear with a_0-a_3,
which are identified by levels and gradients at z = 0; (iii) a shock to lambda_u at entry instead would act on
employment, which carries almost none of the IGE (hours 0.010 of 0.220), and would need a second parameter for its
race incidence. The simulation needs the PSID's actual z path by state and entry year (an input file from
`state_shocks.pkl`; pre-1976 entrants get the national rate) so that the simulated and real D1 regressions are the
same object.

Parsimony test: estimate the selected nested model (B or C) with theta, and report the fit to the D1 wage and IGE
moments with theta = 0 and with theta at its estimate. If the D1 first stage on G access is a precise zero (D1's
"informative either way"), theta is not estimated and Section 7 says why in one footnote (PSID footnote rule: the
number and `47.EntryConditions.py`).

Not to add: a race-specific theta (its moment is the underpowered triple interaction); a shock to gamma; period
effects on the college premium (the calendar check already leaves the racial difference at 0.063\*\* (0.027), EVIDENCE
9.27); a transfer that insures entrants (no moment; dropped in round 2).

### 3.3 Targets vs validation (Voena / BPS style)

- **Target** (one moment): the D1 coefficient of P(G at 25-34) on z, pooled across race. It identifies theta.
- **Validation, untargeted**: the D1 coefficients of the log wage at 25-34 and 35-44 on z, by race and interacted
  with parental income; the opening of the racial gap for slack vs tight entry cohorts; the NLSY79 (1980-82 entrants)
  and NLSY97 (2001 and 2008 entrants) age profiles with their national z paths. The model, estimated on the PSID's
  stationary moments plus the one access moment, produces these regressions on simulated data with the real z path;
  the comparison table is the paper's answer to "reduced-form heterogeneity with labels". This is exactly how Voena
  (2015) uses divorce-law changes and BPS (2016) their policy variation: a policy or shock that was not used in
  estimation reproduced by the estimated model.
- **Validation for kappa**: D4's effect of UI generosity on the re-employment loss by race, compared with the model's
  loss when kappa is lowered by the D4-implied amount. The model has no UI, so this is a scale check, labelled so.
- **Validation for the age-of-scoring lesson (D3)**: the model's own childhood shock is a shift of x; simulate a
  10-percent fall in x and report the son's earnings effect at 30 and 45 by race; compare the ratio of the two with
  D3's ratio.
- **Not a target**: anything by race x parental income x z.

### 3.4 If D2 finds the public sector matters

Then a third job type P (high entry pay given e, lower delta, gamma_P below gamma_O) with its own access share by
race, three or four parameters, justified by D2's numbers and a PSID footnote. Do not add it before D2. If added,
counterfactual 2 splits into "equal access to G" and "the public sector's pay scale equal to the private sector's",
which is a public-sector pay policy scored at 30 and 45. Parsimony rule: keep P only if the nested model with P
improves the fit to the sector moments and to the Black return-to-schooling profile.

---

## 4. Prioritised plan, time, risks

### 4.1 Before coding the model (4 weeks, parallel with the writing items of the round-2 review that are done)

| # | Item | Days | Output |
|---|---|---|---|
| 1 | D1 PSID: state at 17, entry year, z; P(G at 25-34), log wage at 25-34 and 35-44, IGE by entry condition; by race; main effects, x interaction, race interaction, triple as a bound; national-z version | 7 | new script; table in Sec. 5; EVIDENCE rows |
| 2 | D1 ACS: state of birth x cohort x race x education; wage and return to schooling by experience band x z | 4 | appendix table; the schooling leg |
| 3 | D1 NLSY79 / NLSY97 national z | 3 | footnote |
| 4 | D2 public sector: class of worker; G/O by sector; opening among private starters; return to schooling by age within sector | 5 | table in Sec. 5 |
| 5 | D3 father's displacement re-scored by the son's band x race | 3 | conclusion paragraph; shared with Paper A |
| 6 | D4 UI at the son's displacement | 5 | paragraph in Sec. 5.5; scale for counterfactual 4b |
| 7 | D5 industry shocks, appendix check; MW Kaitz robustness row | 2.5 | appendix |
| 8 | Writing: intro paragraph with the pitch and the age-of-scoring list; division-of-labour paragraph in both papers; Table modelid's policy column; cohort rows re-read as shocks | 3 | text |

Order: 1, 4, 5 first (they decide the model's blocks); 2, 3, 6, 7 while 1 is being written up; 8 last.

### 4.2 In the model (adds about two weeks to B1-B7 of the round-2 plan)

| Item | Days |
|---|---|
| z input path by state and entry year; theta in the access logit for the first K years; K from D1 | 3 |
| Jacobian with theta; collinearity check against a_0-a_3 | 1 (inside B3) |
| Counterfactuals 2b, 4a, 5 (recession at entry; tight first decade) at 30 and 45 | 2 (inside B6) |
| Validation table: simulated vs PSID D1 regressions; NLSY79 / NLSY97 profiles with their z paths; D3 ratio; D4 scale | 4 |
| Model P (only if D2 says so) | 10 |

HPC rules apply as standing (32 cores, --threads 2, 64G default, job names, email flags, git-archive snapshot).

### 4.3 What to skip

Affirmative-action bans, tuition / merit aid, EITC, anti-discrimination enforcement, licensing, school finance, the
draft, Atlas x county conditions: cited where they belong, no design. No weak IV, no sibling controls, no restricted
data.

### 4.4 Risks and fallbacks

| Risk | Likelihood | Fallback |
|---|---|---|
| D1's state version is underpowered on G access (first stage t < 2) | high for the state version, moderate for the national one | report the pooled first stage with its confidence interval; identify theta from the national-z version; use the ACS for the schooling leg; if both are null, drop theta, write the null in Sec. 5 as "access to good starting jobs does not respond to entry conditions; the gap is structural", and keep the policy counterfactuals (1-4) |
| D1 finds a scar that is equal by race and by parental income | moderate (Schwandt and von Wachter find larger nonwhite scars, but with no parental income) | that is a finding: entry shocks lower everyone's start and the gradient is rebuilt by 35; the model reproduces it through lambda_G; the racial gap at 45 is then not cyclical; do not dismiss it |
| D2 finds the public sector carries much of the Black flat profile | moderate | model P; the paper gains a policy result (public-sector pay compression lowers the measured Black IGE at 45 while raising Black levels at 25-29); the schooling pay-off counterfactual becomes conditional on sector |
| D4 null or wrong-signed | moderate | counterfactual 4b reported as a kappa bound, not a UI policy; Paper A keeps UI |
| theta's Jacobian column collinear with a_0 | low (a_0 is identified at z = 0 across all cohorts) | fix K shorter; or identify theta from the national-z moment only |
| The reviewer reads the shock block as a bolt-on | moderate | the one-parameter, one-moment structure and the validation table are the answer; say in Sec. 7 that the block is the only non-stationary element and why |
| Time: the four weeks delay the working paper | real | circulate Sections 1-6 now (round-2 advice stands); D1-D4 go into the next version with the model |

---

## 5. Journals

The partial connection raises the paper's ceiling and does not lower its floor; a full reframe would do the opposite.

- **As is (facts plus specified model)**: JOLE / JHR / EJ likely; AEJ: Applied about one in three (round-2 numbers
  unchanged).
- **With D1-D4 and the estimated model with the shock block and the validation table**: AEJ: Applied or JEEA remain
  the modal outcome (about one in two), and **AEJ: Policy** becomes a second realistic home at the same odds (the
  age-of-scoring lesson for long-run evaluations, the named-policy counterfactuals and the entry-shock results are
  what that journal publishes). REStud or JPE about one in four, slightly up from round 2 because the model now has an
  out-of-sample test with real variation (the Voena / BPS standard those editors apply) and a general lesson for
  program evaluation. AER / QJE still about one in ten: the binding constraint remains public-data replication of a
  PSID fact, and the falsifiable prediction for the 1978-83 administrative cohorts (a gap of 0.25-0.30 at 43-47
  against 0.10 at 31-37) remains the paper's answer.
- **If the paper were retitled around policy effects without the designs**: AEJ: Policy would reject on
  identification, REStud / JPE on the same ground, and the fact would be read as background. Do not do it.

Submit to REStud or JPE first with the model, D1 validation and the counterfactual table; AEJ: Policy or AEJ: Applied
second depending on which of D1 (shock) or D2 (public employment) delivered the sharper result.
