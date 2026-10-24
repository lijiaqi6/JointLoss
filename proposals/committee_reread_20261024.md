# Paper B re-read cold by Kopczuk, Hoynes and Zwick (2026-10-24, after the revision)

**What was read.** `paperB_age_profile/main.tex` and every main-text input (sec1, sec3_data, sec3_ageprofile_main,
sec3_frame, sec3_race, sec4_layoff + body, sec5_standsfor + body, sec6_career + body, sec7_daughters + body,
sec7_policy, sec8_conclusion), the appendices enough to check claims (appA, appB_split_body, appC_skill_body, appB,
appD_spells_body, appE_policy, appD_race first part, appC_entry first part), the tables the text leans on
(tab_ige_baseline, tab_age_period, tab_split_main, tab_layoff_age, tab_layoff_fe, tab_layoff_selection,
tab_layoff_exog, tab_layoff_mechanism, tab_layoff_referee, tab_eitc_age, tab_ui_stability), `EVIDENCE.md` rows
11.28-11.79, and `output/what_is_passed_on.md`, `what_is_passed_on_rest.md`, `sons_business_income.md`,
`wealth_transmission.md`, `eitc_checks.md`. The earlier memo `proposals/committee_critiques_20261024.md` was read
only after Sections 1-3 below were drafted. Nothing was run; no other file was touched.

**Conventions.** Every estimate carries the stars or p-value the paper (or the EVIDENCE row named) gives it. "Unit
share" = the father's share of the son's seven teen years with a layoff; one layoff year = one seventh. Literature
not in `references.bib`, and PSID item facts I could not check in the files, are marked [?].

**Constraints respected.** Public US data only (PSID, NLSY79/97/CYA, CPS, BLS/DOL/UKCPR, CBP/QCEW public files); no
sibling controls; no long balanced panels as evidence against a finding; race as heterogeneity; no structural model;
no cross-country work; no section cuts proposed (only moves of emphasis and wording).

---

## 1. Verdict

The paper is now a careful, heavily robustness-checked descriptive paper, and in substance it is still two to three
steps from a top general-interest journal. Its new fact---a father's teen layoff is unrelated to the son's earnings
at 25-29 (0.146, p = 0.19) and goes with earnings lower by 0.768\*\*\* per unit share at 45-49, change
$-0.914$\*\*\*---survives cohorts, one job-end rule, self-employed fathers, the father's sector, occupation and union,
and Holm and Romano-Wolf. But it rests on 135 treated sons at 45-49 (98 White, 37 Black). No design separates what
the layoff does from what it reveals about the father (the paper says so). And the bridge from the IGE to the
layoff is thin: the layoff element is 0.025\*\* of an IGE of 0.443\*\*\* at 45-49. **The single most damaging
remaining problem is that the revision has moved the result without the text following it.** Within the same son,
the earnings bend is $-0.885$\*\*\* in self-employed son-years and $-0.084$ (p = 0.41) in employee years (`sec6_career_body`;
`output/sons_business_income.md`). Self-employed years are about 11 percent of son-years (4,386 of about 38,750).
Outside them, the within-son hourly-wage bend is not significant: $-0.004$ (p = 0.96) in employee years, and for sons
overall $-0.086$ (s.e. 0.096) in the reduced specification and $-0.134$ (p = 0.159) inverse-probability weighted. Yet
the abstract and introduction still say "in the wage, within the same son". Self-employment income is the most
error-ridden income item in household surveys [?, Hurst-Li-Pugsley 2014], and the paper's "self-employed" category
includes men who work "for themselves and for others". So the headline is currently "sons of fathers laid off or
fired more often become low-earning self-employed men in midlife", measured on survey self-employment income. That
can be tested with public PSID data within a week (actions 1-2 in Section 5), and the paper has to be rewritten
around whatever the tests show.

---

## 2. The three readers

### Wojciech Kopczuk

**K1. "Your bridge from the IGE to the layoff is not there in your own preferred split." (serious)**

*In his voice.* "Section 3 says 'One component's share rises with age: the parents' spells out of work, from
0.017\*\* of the IGE at 25-29 to 0.060\*\*\* at 45-49, 13.5%\*\*\* of it. It is the father's layoffs.' Those numbers
come from the four-component split (split A). Your Table 2 (`tab_split_main`, column 1) reports split B, which adds
the parents' schooling and other resources. In split B the spells opening is 0.025 (p = 0.263), not significant,
while the parents' schooling opening is 0.057\*\* (p = 0.016) (`output/what_is_passed_on_rest.md`). Correct the
components for measurement error, as Appendix B does, and spells fall from 4.2%\*\* to 2.7% (n.s.) over 25-55 and
from 8.0%\* to 2.8% at 45-49 (EVIDENCE 11.46). In the cohorts with wealth, spells carry 8.9%\* at 25-29 and 4.9 at
35-39: falling, not rising. Your appendix says the spells are 'the one component whose contribution rises
significantly' (`appB_split_body`), but Section 8 lists the wage component rising from 0.035 to 0.097\*\*\* and the
father's schooling from 0.014 to 0.075\*\*\*. The title says '... and the IGE', but at 45-49 the layoff element is
0.025\*\* of 0.443\*\*\*. And the life-cycle story you do tell, skill at entry, carries three fifths of the rise in
one cohort (NLSY79) and a quarter in the other (NLSY97: 0.021\*\* of 0.083\*\*\*), so 'most of its rise' is one
cohort's result."

- (a) Targets: the abstract ("one thing parents do carries a share of it that rises with age"; "The son's skill at
  entry carries most of the earnings IGE's rise with age"); `sec3_frame` ("One component's share rises with age");
  `appB_split_body` ("the one component whose contribution rises significantly"); conclusion ("The result is the
  one component of the IGE that is passed on and whose weight grows with the child's age"; "the son's skill at entry
  carries most of its rise with age, in two cohorts twenty years apart").
- (b) Serious. It does not threaten the layoff fact. It does threaten the paper's architecture, because the layoff
  is introduced as the explanation of a rising IGE component.
- (c) Answer (1 day, mostly writing; `75`/`80` outputs already exist). Report the spells and layoff-element openings
  in split B and under the instrumented split next to split A. Report the layoff element's contribution to the
  IGE's rise (out of 0.167\*\*\*). Then re-motivate the layoff on its own terms: "the IGE splits into components
  whose weights change with age; one of them, a parental shock, has a delayed partial effect." Do not motivate it as
  "the component that rises". Write "in the NLSY79 three fifths, in the NLSY97 a quarter" wherever skill at entry is
  claimed.

**K2. "Net worth is a better measure of permanent income than a 13-19 income average, so a 'wealth share' is partly
a measurement-error correction." (serious)**

*In his voice.* "You put parental net worth on the right-hand side of a regression of the son's log earnings on log
parental income averaged over at least three teen years, with a reliability you put at 0.63-0.65 for a six-year
mean. Wealth is accumulated permanent income. When you add it, the coefficient on the noisy income average falls,
and you call the fall 'what wealth carries'. Your own juxtaposition misleads: 'With wealth in, little of the IGE is
left as parental income at equal measures (3.5 percent); on all sons, without wealth, half is.' On the same 2,828
sons without wealth the rest is already 11.4% (n.s.) (`appB_split_body`). Most of the fall from half to 3.5 percent
is the sample, not wealth."

- (a) Targets: abstract ("the parents' wage and, where it is measured, their wealth carry between two fifths and a
  half of the IGE"); `sec3_frame` (the 3.5-versus-half sentence); `tab_split_main` cols. 2-4 (wealth 23.0%\*\*\*,
  31.2%\*\*\*, 29.1%\*\*\*).
- (b) Serious for the wealth headline. The housing result inherits it.
- (c) Answer (2 days; `98`, `121`, `125`). Run a horse race. Re-run split B with wealth when parental income is
  measured with less error: at the father's ages 40-50 (already built for K3 of the earlier memo, IGE 0.267\*\*\* to
  0.526\*\*\*), and as the longest available average of family income. If the wealth share holds at that
  permanent-income measure, the result stands; if it halves, write it as "wealth and a better income measure carry
  the same thing". In the 3.5-percent sentence, give the 11.4 percent of the same sons without wealth.

**K3. "Your wealth age profile is across cohorts, and your 'not gifts or inheritances' test cannot see the
mechanism." (serious)**

*In his voice.* "The rank-rank slope of the son's net worth on his parents' rises from 0.228\*\*\* at 25-29 to
0.408\*\*\* at 35-39, trend 0.089\*\*\* a decade. But your sons are born 1964 and later. The 45-49 band (566 sons)
holds only the 1964-76 births, and for the earliest of them the parents' wealth is one wave at the son's 20 (1984).
The 25-29 band holds births to the 1990s. Show me the rise for the same sons. Then gifts. You test whether a
family's chance of receiving a gift or inheritance rises with the parents' wealth rank by age. It does not
(0.084\*\*\* at 25-34, 0.041\*\*\* at 35-44, 0.073\*\*\* at 45-55). But the gradient is largest at 25-34. That is the
down-payment age, and a gift that buys a house at 30 compounds into home equity at 40, which is exactly a wealth
correlation that rises into the late thirties. Inheritances arrive at the parent's death, mostly after your sample
ends (parents of sons born 1964+ are in their seventies in 2021). In Danish registers the parent-child wealth
correlation jumps at the parent's death [?, Boserup-Kopczuk-Kreiner 2016/2018]. And Charles and Hurst (2003)
[?, not in the bibliography] estimated the PSID's age-adjusted parent-child wealth elasticity twenty years ago; it
is the benchmark."

- (a) Targets: abstract ("wealth has its own age profile ... from 0.23 to 0.41, after earnings ranks have stopped
  rising, and not through gifts or inheritances"); intro paragraph 4; `sec3_ageprofile_main` (Ranks subsection,
  last paragraph).
- (b) Serious for the "not gifts" clause, moderate for the profile.
- (c) Answer (3 days; `122.WealthTransmission.py`). (i) The profile within fixed birth cohorts (1964-71, 1972-79),
  and with son fixed effects in a stacked rank regression (slope × age). (ii) Cumulative gifts and inheritances
  received to date, extensive margin and asinh value (the value is already in `output/wealth_transmission.md`:
  0.317\*\*\* at 25-34), entered as a control in the rank-rank-by-age regression. If the rise survives, "not gifts"
  is earned. (iii) Home equity and non-housing net worth of the son as separate outcomes: if the rise is housing,
  say "early help into housing" is a candidate. (iv) Write "not through gifts or inheritances received so far;
  inheritances largely fall after the sample ends." Cite Charles-Hurst and Boserup-Kopczuk-Kreiner [?]. One line:
  Nordic registers with parental death dates would settle bequest timing.

**K4. "'The wealth is housing' is partly a property of ranks, and 'the family home' is not what you measured."
(moderate)**

*In his voice.* "Your housing component is home equity plus other real estate. Business and farm equity is zero for
83 percent of parents (17.3 percent hold any), so its within-birth-year rank is mostly ties and carries little
variance. A 2.0 percent share (s.e. 1.9) is close to built in. In asinh form your own split gives business
3.7%\* (p = 0.096) against housing 11.6%\*\*: a third of housing, not a tenth. The PSID has no high-wealth
oversample (p99 \$1.48 million, 2000 dollars), so the family-firm channel, which lives at the top, cannot show up
here. 'Business equity 2 percent' is a statement about the PSID's middle, not about the US."

- (a) Targets: abstract ("The wealth is housing: the family home carries 21 percent of the IGE and business equity 2
  percent"); intro paragraph 3; `appB_split_body` ("not through a family business").
- (b) Moderate.
- (c) Answer (0.5 day, writing plus one table row). Say "housing (home and other real estate)". Report rank and asinh
  component shares side by side. Add one sentence that the PSID's thin top means the business-equity share describes
  families below about the 99th percentile. One line: SCF-linked or register data would test the top.

**K5. "Your accounting language still says 'what parents do'." (minor; the earlier K5, partly fixed)**

- (a) Intro paragraph 2: "Splitting it into what parents do shows ..."; "One parental component's share rises with
  age, the parents' spells out of work, and it is the father's layoffs." `sec3_ageprofile_main`: "What rises is
  mostly the pay-off of what sons bring". The title of Section 3.4: "What rises: the parents' wage, their wealth and
  the son's skill".
- (b) Minor.
- (c) Half a day of wording. "The components of the IGE" throughout; reserve "passed on" for statements about the
  layoff's partial coefficient, and even there say "goes with".

### Hilary Hoynes

**H1. "Your insurance section says more than your tests can, and your two UI-receipt splits contradict each other."
(serious)**

*In her voice.* "Section 8 opens: 'the data say that insurance as legislated does not reach it.' Look at what you
have. (i) Simulated replacement rate: the layoff interaction is $-0.038$ (s.e. 0.187). A 95 percent interval of
about [$-0.40$, 0.33] contains +0.24, a full offset of your cost (0.236\*\*) per standard deviation. On that sample
your footnote says the layoff's within-son cost is itself 0.040 (s.e. 0.113): there is no cost to offset, so the
test is uninformative by construction. (ii) Weeks available: $-0.191$ (s.e. 0.395), interval about [$-0.96$, 0.58].
Your sentence 'They exclude only insurance effects larger than the cost itself' is false for both designs: they do
not exclude a full offset. (iii) Realised UI: within son, $-0.446$\*\*\* (p = 0.001) after layoffs with no benefits,
$-0.067$ (p = 0.65) low replacement, $-0.361$ (p = 0.19) high. The band changes you do not report go the other way:
high replacement $-2.095$\*\*\* (p = 0.002) against low 0.051 (EVIDENCE 11.78). And Table 7 panel D
(`tab_layoff_selection`) has a different receipt split: UI received $-1.014$\*\* against no UI $-0.211$
(p = 0.095). One table says no-benefit layoffs are the costly ones; another says benefit layoffs are. Receipt is not
random either: take-up, monetary eligibility and disqualification for misconduct all sort it, and your layoff code
includes firings."

- (a) Targets: `sec7_policy` first sentence; the intro ("these tests can exclude only effects larger than the cost
  itself"); `sec7_policy` UI subsection (the MDE paragraph and the realised-UI paragraph); conclusion ("insurance
  ... is not shown to weaken it").
- (b) Serious for the policy section's credibility. It is not fatal, because the paper's own wording elsewhere is
  "not shown".
- (c) Answer (2-3 days; `91`, `99`, `102`, `130`). Reconcile the two receipt splits: same definition, same years,
  same treated counts, and report band changes and within-son slopes together. Report every insurance interaction
  as an interval in units of the cost ("the interval runs from an X-fold amplification to a Y-fold offset"). Say
  plainly that the simulated-rate design runs on a sample with no detectable cost. Then either (i) build one pooled
  insurance index (simulated rate × weeks, at the father's wage, within state and cohort) on the full 1968+ window,
  with DOL Significant Provisions back to 1968 [? coverage of `12b` before 1976], and one interval; or (ii) move the
  UI tests to the appendix and keep one sentence in the text: "the designs are too imprecise to say whether
  insurance offsets the cost." Change the policy section's first sentence to match.

**H2. "'Laid off or fired' is two things, and your own NLSY data say the second carries it." (serious)**

*In her voice.* "Your treatment is the PSID's 'laid off or fired' code. A firing is a statement about the worker,
and fired workers are often disqualified from UI. In the one data set where you can separate them, the NLSY79
children's mothers, the stability component is carried by 'her jobs ending in a firing' (0.008\*, p = 0.065), and
her layoffs carry $-0.005$\*\* (p = 0.023), the opposite sign (EVIDENCE 11.33; `appB_split_body`, 'Four data sets').
Your 'no-benefit' layoffs, which your realised-UI split finds costly ($-0.446$\*\*\*), are where firings would
sit. So 'unstable employment' may be 'dismissal', and the father-or-event question tilts toward the father."

- (a) Targets: the word "layoff" in the title, abstract and every section; intro ("What the layoff stands for ... the
  answer is unstable employment rather than lost income"); `sec5_standsfor_body` ("What kind of father").
- (b) Serious for interpretation and for the policy margin; not for the fact.
- (c) Answer (2-3 days; `83.CYAWhatIsPassedOn.py` + `131`). (i) In the CYA, the mother's teen-window firings and
  layoffs as separate shares, on the child's earnings by band (to the early forties) and within child, with treated
  counts. (ii) In the PSID, use benefit receipt in the layoff year as an eligibility marker, a partial
  layoff-versus-firing proxy, once H1's reconciliation is done. (iii) Check whether any PSID wave codes the two
  separately [?]. (iv) Write "a layoff or firing" in the definitions and at first use in the abstract. One line:
  state UI administrative separation reasons would separate them exactly; not available.

**H3. "Your EITC 'caution' buries the design that points the other way." (moderate to serious)**

*In her voice.* "You show that intent-to-treat exposure goes with faster within-son growth even in the top third of
parental income (0.032\*\*\*), where the credit averages \$33 a year, and conclude the design is confounded. Fine:
number-of-children × cohort profiles contaminate a schedule-only exposure. The standard response is to difference
them out, and you did, in a footnote. Among families predicted eligible from pre-window characteristics the within-son
growth is 0.064\*\*\* a decade, against 0.017 in the others (EVIDENCE 11.74: 0.017, p = 0.110). That
triple difference is exactly the check 'where the policy does not bind', and it does not support your 'caution'. You
report neither the difference nor its p-value. You also never state what Bastian and Michelmore (2018) found at
18-27 [? their earnings sign and size], although your $-0.016$\* (p = 0.052) at 25-29 is the same design."

- (a) Targets: abstract ("the EITC is too small to move the IGE detectably"); intro ("The EITC is a caution, not an
  example ... the same profile appears in families the credit barely reaches"); `sec7_policy` (The age of scoring,
  EITC paragraph and footnote); conclusion ("a warning about schedule-based designs scored at one age").
- (b) Moderate to serious with this reader. She built these designs and will read the footnote.
- (c) Answer (2 days; `126`, `129`). (i) In the main text, report the likely-eligible minus other difference in the
  within-son growth with its p-value, with number-of-children × birth-year × age controls, and the 1993-96 DiD by
  band ($-0.079$ at 25-29, +0.046 at 40-44, both n.s.). (ii) If the triple difference is significant, the paragraph
  becomes "an eligibility-concentrated later-growth pattern that the IGE calibration says is too small to move the
  IGE (0.007-0.011 against MDEs of 0.08-0.14)". If it is not, the caution stands and is stated with that number.
  (iii) State the Bastian-Michelmore estimate next to the paper's. (iv) Cut the 1971 and 2019+ "why not looking"
  material to a footnote; it does not bear on 1975-2005 EITC responses.

**H4. "You condition on a mediator, and your pre-trend is a dip." (moderate)**

*In her voice.* "Every layoff and closure coefficient is 'at equal ln parental income' measured over the son's 13-19,
the same years in which the layoffs and closures cut that income. At equal realised income, a family hit by a
closure had higher income potential. That alone can make 'at equal parental income even raise the son's wage'
(0.021\*\* per s.d.) and can flatter the closure null your contrast leans on. Use parental income from before the
window. Separately, your event study has the father's earnings 0.106\* above the reference year at $-6$ and 0.113\*\*
at $-3$, and $-0.005$ at $-2$. Jointly p = 0.203, but a fall of about 0.11 in the two years before a 'first layoff'
is half the layoff-year drop ($-0.198$\*\*\*). That is a pre-trend in level, and 'no significant pre-trend' in the
introduction oversells it."

- (a) Targets: `sec4_layoff_body` ("The closure is the contrast that disciplines the reading"); `appB_split_body`
  ("What passes to what"); intro ("before the first layoff the father's earnings and employment show no significant
  pre-trend"); `tab_layoff_referee` panel A.
- (b) Moderate.
- (c) Answer (1-2 days; `88`, `91`, `108`). Re-estimate the band profile, the within-son slope and the
  layoff-minus-closure contrast with parental income at the son's 6-12 (or the father's earnings before the son's
  13) in place of the 13-19 mean, and with both. Plot the event study and write "earnings about 0.1 higher three to
  six years before, falling to the reference two years before".

**H5. "Mothers who head families: your new result is a same-sex pattern, and you read it as the opposite." (moderate)**

*In her voice.* "A mother's teen layoffs cost her sons nothing detectable ($-0.079$, p = 0.64) and her daughters
$-0.561$\*\* (p = 0.027) a decade. A father's teen layoffs cost his sons and raise his daughters' wages (+0.168\*\*).
Put together: the same-sex parent's layoff goes with a delayed cost, the other parent's with none or a gain. Your
text uses the mothers to say 'nor is it that a parent's layoff helps daughters', and calls the mothers' estimate
'the size of the father's cost for sons'. But the mothers' families are 74 percent Black and mother-headed, the
mothers' band comparison is imprecise ($-0.215$, s.e. 0.275), and in the 1990s these mothers' layoffs interact with
AFDC and its reform. A same-sex reading (role models, occupational following, the son's self-employment) would
change what the daughters section says."

- (a) Targets: `sec4_layoff_body` ("Mothers who head their families", "the size of the father's cost for sons");
  `sec7_daughters_body` ("Nor is it that a parent's layoff helps daughters").
- (b) Moderate.
- (c) Answer (2 days; `131` + `61.PolicySchedules.py`). State the same-sex pattern as a candidate reading. Add the
  state AFDC/TANF maximum benefit for the family size (UKCPR, public), averaged over 12-18, as a moderator of the
  mother's layoff. If the PSID asks wives the job-end question in any waves [?], estimate the mother's layoff in
  two-parent families too: that would put both parents and both sexes in one sample, the only design that separates
  "same-sex" from "mother-headed families differ".

**H6. "Your mechanism sentences are built on differences you cannot reject." (moderate)**

*In her voice.* "The abstract says layoffs in bad times 'cost the son about half as much, though they cost the father
at least as much earnings and no work, so the son's cost follows the father's employment, not his income loss'.
Three differences, none significant. The son's equality test has p = 0.263. The father's earnings difference is
$-0.099$ (p = 0.25). The father's employment difference is 0.062 (p = 0.113, EVIDENCE 11.72; not reported in the
paper). Your 'bad times' are 53 percent of layoff years against 44 percent of all window years, a weak
Gibbons-Katz separation. The same holds for 'the costly layoffs are repeated ones with small income losses':
equality p = 0.079, 0.064 and 0.145. These are patterns of point estimates."

- (a) Targets: abstract (bad times; "the costly layoffs are repeated ones with small income losses"); intro paragraph
  6 ("What bad-times layoffs don't cost the father is work ..."); conclusion paragraph 1; `sec5_standsfor_body` ("The
  cost is therefore not selection alone").
- (b) Moderate. Wording, plus one sharper split.
- (c) Answer (1 day of wording; 2 more days for a sharper classification). Write "point estimates suggest ...; the
  differences are not significant (p = ...)". Remove the "so" causal chain from the abstract. A sharper bad-times
  split: state × 2-digit-industry employment declines of at least 5 percent from County Business Patterns (state
  files public from the 1970s [? first year]), which classify fewer years as bad and so separate better.

### Eric Zwick

**Z1. "Your cost lives in self-employed son-years, and survey self-employment income is the weakest number you
have." (fatal for the headline as worded; serious for the fact)**

*In his voice.* "Within the same son, a unit share bends earnings by $-0.885$\*\*\* (p < 0.001) in self-employed
years and $-0.084$ (p = 0.41) in employee years. The hourly wage: $-0.609$\*\* against $-0.004$ (p = 0.96). Those are
4,386 of about 38,750 son-years. How many treated sons are self-employed at two or more ages, which is what
identifies a within-son slope there? You do not say. Outside those years there is no significant within-son wage
bend, yet the abstract says 'in the wage, within the same son'. Three measurement problems. First, your
'self-employed' is 'works for himself, alone or also for others', and your own text says 'many of [them] work for
themselves and for others': the falling 'wages and salaries' may be from the employee job of a moonlighter. Second,
households underreport self-employment income in surveys by a quarter or more [?, Hurst-Li-Pugsley 2014 use the PSID
itself]. If underreporting rises with business age, or differs for these sons, it shows up as your 'cost'. Third,
with the asset part of business income added, the self-employed-versus-employee interaction is $-0.315$
(p = 0.105), not significant, and you report only the level in self-employed years ($-0.812$\*\*\*). Without
self-employed fathers the employee-year cost is $-0.174$\* (p = 0.069). So it is not cleanly 'not in employee years'
either."

- (a) Targets: abstract ("in the wage, within the same son"; "self-employment pays them less with age: their earnings
  and hourly wage fall behind in their self-employed years and not in their years as employees"); intro paragraphs 1,
  8, 9; `sec6_career_body` paragraph 2; conclusion paragraph 1.
- (b) Fatal for the current wording of the headline. Serious for the fact's interpretation: the result is either a
  self-employment selection-and-measurement phenomenon or a real midlife wage cost, and the paper cannot yet say
  which.
- (c) Answer (3-4 days; `118`, `123`, `88`). (i) Report the treated counts behind the self-employed-years slope.
  (ii) Split "self only" from "self and others" (the PSID class-of-worker codes separate them [? in every wave]),
  and put the moonlighters' main job in the employee years. (iii) A Hurst-Li-Pugsley test [?]: food expenditure
  (most waves) and total consumption (1999+) on reported income, for self-employed sons of laid-off and other
  fathers. If sons of laid-off fathers consume as if their income were not lower, the "cost" is reporting. Also the
  son's net worth at 45-55 by father's layoff and own self-employment (wealth is already built, `117`). (iv) Report
  the interaction with the asset part (p = 0.105) and the no-self-employed-fathers employee-year estimate in the
  text. (v) Rewrite the abstract and introduction: "within the same son, the bend is in his self-employed years".
  If (iii) kills it, the paper's fact is the band profile and the self-employment entry (0.271\*\* at 45-49), not a
  wage cost.

**Z2. "Pass-through owners choose their salary." (moderate)**

*In his voice.* "You say the cost is 'in the wages and salaries of these sons, many of whom ... pay themselves a
salary' (interaction $-0.804$\*\*, p = 0.023, on asinh other labor income; the self-employed-years level is $-0.790$,
p = 0.19). An S-corporation owner splits his return between a salary and distributions, and the split responds to
payroll-tax incentives [?, Smith-Yagan-Zidar-Zwick 2019]. Distributions show up in a survey as dividends or other
asset income, not as the asset part of unincorporated business income, which is all you add back. A falling salary
with age, and no fall in hours ($-0.275$, p = 0.28), is what reclassification looks like."

- (a) Targets: `sec6_career_body` ("Nor is it business income moved out of earnings ...").
- (b) Moderate.
- (c) Answer (1-2 days; `123`). Add the head's dividends, interest and rent to the outcome (total head income, all
  sources) in self-employed years. Split by whether the business is incorporated, if the PSID asks [?]. If the cost
  survives in total income, say so; if it vanishes, the "cost" is a salary-distribution split.

**Z3. "Your employer-side facts are large and you wave them away." (serious)**

*In his voice.* "Sons of laid-off fathers work in much smaller workplaces at 45-49: log workplace size change
$-4.095$\*\*\* per unit share, 2003+ (EVIDENCE 11.66). They are more often in government: change +0.231\*\*
(p = 0.050). The text says these 'do not move with the father's layoffs in a way that carries the cost', and
'holding the size of the son's workplace fixed leaves it unchanged'. But size exists only from 2003, on a subsample.
And your 'within-occupation' wage cost ($-0.392$\*\*, two thirds of $-0.603$\*\*\*) is exactly where employer wage
premia live [?, Card-Heining-Kline 2013; Lachowska-Mas-Woodbury 2020]. Small employers and self-employment pay
less. If the son's cost is that he works for small or no employers, the mechanism is employer sorting, not 'skills
acquired after school, effort'."

- (a) Targets: `sec6_career_body` (footnote on union, government and size; last sentence "the data here do not
  separate"); intro ("In the son's career the cost is a lower wage within his occupation").
- (b) Serious for the mechanism paragraph; it also links Z1 to the career section.
- (c) Answer (2 days; `106`, `118`). (i) Report the government and workplace-size estimates in the text. (ii) Split
  the within-occupation wage into an industry wage premium (CPS ORG industry × period mean log wage relative to
  occupation; public) and a residual. Hold the son's own industry × age fixed in the within-son design, not only
  his early job. (iii) Run the occupation decomposition on employee years only. If the within-occupation cost
  disappears there, Z1 and Z3 are one finding. One line: LEHD firm effects would settle employer premia; not
  available.

**Z4. "Recall versus new employer is measured with error large enough to make 'as much as' empty." (moderate)**

*In his voice.* "Your recall classification, validated on 1980-82, labels 41 of 76 true returns as recalls and 48
of 402 non-returns as recalls. Recall $-0.251$\* (p = 0.052), new $-0.153$ (p = 0.40), difference p = 0.67. With
that misclassification the difference is attenuated toward zero by construction, so 'follows recalls as much as
moves' says nothing. Likewise, 'the same in every sector' ($p = 0.98$) on five sector estimates, from $-0.143$ to
$-0.282$\*, has no power."

- (a) Targets: intro ("follows layoffs after which he returned to a former employer as much as those after which he
  moved to a new one"; "is the same in every sector"); `sec5_standsfor_body` ("The father or his job").
- (b) Moderate.
- (c) Answer (1 day). Correct the recall-new difference for the validated misclassification (a simple
  Hausman-style correction using the 1980-82 rates), report the corrected interval, and write "not distinguishable"
  instead of "as much as". The sector-equality claim becomes "no sector carries it; the test has little power".

**Z5. "Your demand-shock design is too coarse to be informative, and its wrong sign is a warning." (moderate)**

*In his voice.* "National employment of 15 sectors gives a layoff first stage of 0.030\* (F = 2.9) and a within-son
reduced form of +0.143\*\*, the wrong sign, which halves to 0.067 (s.e. 0.076) with detailed industry × age. The
introduction turns this into 'Shocks the father did not choose carry no cost: neither plant closures nor national
declines of his industry'. The design cannot say that about layoffs. Your own text concedes the implied cost is a
tenth of the reduced form's s.e."

- (a) Targets: intro paragraph 5; `sec5_standsfor_body` ("Shocks the father did not choose").
- (b) Moderate.
- (c) Answer (3 days; `93`, `112`). A state × detailed-industry shock from County Business Patterns (public, by state
  and SIC/NAICS) or QCEW (1975+). The father's state is public in the PSID; industry at 3 digits is there. Report the
  first-stage F. If it is still weak, keep the design in an appendix and change the introduction to "national
  declines of his industry raise his unemployment (0.080\*\*) and are not followed by a cost to the son; they barely
  move his layoffs."

---

## 3. Internal consistency audit

Each item quotes the text (file), then what it conflicts with.

**Numbers and units**

1. "lowers them by 0.110$^{***}$ log points per layoff year" (`sec1_introduction.tex`), "by 0.110 log points"
   (`sec4_layoff_body.tex`), "his earnings are still 0.14 log points lower" (intro), "a difference from sons of 0.93
   log points per unit share" (abstract, `main.tex`). These are 0.110, 0.14 and 0.93 in logs, i.e. 11, 14 and 93 log
   points. The abstract and conclusion say "11 log points" correctly.
2. "lowers them by 0.110$^{***}$ ... as shown in Figure~\ref{fig:layoffbands}" (intro). Figure 1 plots the **hourly
   wage** in the **reduced** specification (father's wage, hours, unemployment, zero hours, volatility only), not
   earnings in the full-component specification (`sec4_layoff.tex` figure notes).
3. "The cost is in the son's hourly wage, it grows within the same son ($-0.236^{**}$ ...)" (intro) and "in the
   wage, within the same son" (abstract). $-0.236$\*\* is **earnings**. The paper never reports the main-spec
   within-son wage slope for sons. The reduced spec gives $-0.086$ (s.e. 0.096) (`tab_layoff_exog` B), IPW $-0.134$
   (p = 0.159) (`tab_layoff_referee` C), main spec $-0.109$ (EVIDENCE 11.63, no star). The band change in the wage
   is significant ($-0.603$\*\*\*); the within-son wage bend is significant only in self-employed years ($-0.609$\*\*).
4. "their partners' earnings rise by 0.677$^{***}$ at 45--49 ... (panel D of Table~\ref{tab:layoff_mechanism})"
   (`sec7_daughters_body.tex`). The table row is "partner's ln earnings, change 0.764$^{***}$". 0.677 is the 45-49
   level (EVIDENCE 11.54).
5. "A son whose father was laid off in his teens works as much as other sons at 45--49 and is paid less per hour"
   (`sec4_layoff_body.tex`), two sentences after "that on his annual hours when employed by $-0.311^{**}$
   ($p = 0.025$)". "Works as much" holds for employment (0.033), not hours.
6. "daughters of laid-off fathers get 0.89 more years than sons ($p = 0.069$)" (intro). This is the difference of
   the layoff coefficients per **unit share** (seven layoff years). It reads as a raw gap; one layoff year is about
   0.13 years.
7. "the size of the father's cost for sons" (`sec4_layoff_body.tex`, mothers). The mothers' cost for **sons** is
   $-0.079$ (p = 0.64). The pooled $-0.368$\*\* is driven by daughters ($-0.561$\*\*). "A mother's layoffs ... go
   with a similar delayed cost" also rests on within-child slopes; the band comparison is $-0.215$ (s.e. 0.275).
8. NLSY79 cohort: "respondents born 1960--64 who lived with a parent in 1979" (`sec3_data.tex`) against "sons born
   1957--64" (`sec3_ageprofile_main.tex`, `tab_age_period.tex`, `appC_skill_body.tex`).
9. "for those born 1963--75, who reach 45--49 in 2008--25" (`sec4_layoff_body.tex`). The last PSID wave is 2023; a
   son born 1975 is 45-48 in 2020-23.
10. Within-son baselines differ across subsamples without comment: $-0.236$\*\* (main), $-0.240$\*\* (early-job
    sample, `sec6`), $-0.268$/$-0.270$\*\* (health), $-0.300$\*\* (stayer), $-0.175$ (p = 0.154, wealth sample),
    0.040 (s.e. 0.113, simulated-UI sample), $-0.124$ (s.e. 0.122, later-layoff placebo sample). Three
    "leaves it unchanged" claims are made on samples where the base itself is not significant (wealth:
    `sec5_standsfor_body` "holding their later net worth fixed leaves the son's within-son cost unchanged";
    simulated UI; the later-layoff placebo, which the text does call weak).
11. Sample denominators: "2,171 of the 4,644 sons" (`sec4_layoff_body.tex` footnote; the timing design is
    father-present, and EVIDENCE 11.41 gives 3,386 father-present sons). The "benchmark sample" of 1,995 Black +
    2,758 White sons (`sec3_data`) against the "baseline sample" of 4,770: two names, two counts.

**One component, "most", "a fifth or more"**

12. "One component's share rises with age: the parents' spells" (`sec3_frame.tex`); "they are the one component
    whose contribution rises significantly with the son's age" (`appB_split_body.tex`); "The result is the one
    component of the IGE that is passed on and whose weight grows with the child's age" (`sec8_conclusion.tex`).
    Against: "the parents' wage component rises from 0.035 to 0.097$^{***}$ (at 35--39), the father's schooling from
    0.014 to 0.075$^{***}$" (`sec7_policy.tex`); "The IGE rises with age because the components that grow, among
    them the father's layoffs, ..." (conclusion); and, in split B, the spells opening 0.025 (p = 0.263) against the
    parents' schooling opening 0.057\*\* (p = 0.016) (`output/what_is_passed_on_rest.md`).
13. "the parents' wage and wealth carry most of the level" (`sec3_ageprofile_main.tex`, opening) and "The parents'
    wage and wealth carry most of what is measured in the IGE" (`sec3_frame.tex`) against the abstract's "between two
    fifths and a half" (38.6 to 49.6 percent). 38.6 is itself just under two fifths.
14. "the parents' hourly wage carries a fifth or more of the IGE" in "every version of the split" (`sec3_frame.tex`;
    `tab_split_main` notes) against `tab_split_main` column 1: 12.0%\*\*.
15. `appB_split_body.tex` opening: "The parents' hourly wage carries a fifth of it, their spells a sixteenth ...
    and half of the IGE is parental income at equal values of everything the data measure". This mixes split A (wage
    19.0%, spells 6.1%, rest 62.9%) and split B (rest 47.6%).
16. "With wealth in, little of the IGE is left as parental income at equal measures (3.5 percent); on all sons,
    without wealth, half is" (`sec3_frame.tex`). On the same sons without wealth the rest is 11.4% (n.s.)
    (`appB_split_body.tex`).
17. "The wealth is housing: the family home carries 21 percent" (abstract); "it is the family home: housing equity
    carries 20.9\%" (intro). The component is home equity **and other real estate** (`appB_split_body.tex`).
18. "The son's skill at entry carries most of the earnings IGE's rise with age" (abstract); "carries most of its rise
    with age, in two cohorts twenty years apart" (conclusion). The NLSY97 share is a quarter (0.021\*\* of
    0.083\*\*\*) (`appC_skill_body.tex`). Also "his AFQT, measured before he enters the labor market"
    (`sec3_ageprofile_main.tex`; `sec3_data.tex` "measures his skill before he enters the labor market") against
    "measured in 1980 at ages 15--23 ... not an endowment" (`appC_skill_body.tex`).

**Claims stronger than the estimate**

19. Causal verbs on a design the paper calls descriptive ("Everything is descriptive: a layoff is not assigned at
    random", `sec4_layoff.tex`): "A father's layoff ... costs the son nothing in his late twenties and a great deal in
    his forties" (intro, first sentence); "lowers them by" (abstract, intro, Section 4); "The same layoffs pull
    daughters the other way" (abstract, intro); "self-employment pays them less with age" (abstract, intro); "so the
    son's cost follows the father's employment" (abstract, intro, conclusion). Use "goes with", "is associated
    with", "is followed by".
20. "Shocks the father did not choose carry no cost" (intro paragraph 5) against the abstract's "carry no detectable
    cost", the closure interval admitting 59 percent of the layoff's cost, and an industry first stage of F = 2.9.
21. "the costly layoffs are repeated ones with small income losses" (abstract); "The costly layoffs are repeated ones
    with small income losses and short unemployment" (intro). Equality p = 0.145, 0.079, 0.064 (`tab_layoff_selection`
    D). There is also a tension with the instrumented split: keeping only the father's persistent layoff propensity,
    the spells share falls to 2.7% (n.s.) (`appB_split_body`), while "repeated" layoffs are said to carry the cost.
22. Bad times (abstract; intro paragraph 6; conclusion; `sec5_standsfor_body` "The cost is therefore not selection
    alone"): son p = 0.263; father earnings difference p = 0.25; father employment difference p = 0.113 (EVIDENCE
    11.72, not in the paper).
23. "it holds in every birth cohort" (abstract, intro, Section 4, conclusion): within son 1963-75 $-0.248$
    (p = 0.14); band change 1976+ $-0.686$ (p = 0.120, to 40-44). Write "is negative in every cohort, and the
    cohorts do not differ (p = 0.73)".
24. "these tests can exclude only effects larger than the cost itself" (intro), "They exclude only insurance effects
    larger than the cost itself" (`sec7_policy.tex`). False for the simulated rate (interval about [$-0.40$, 0.33]
    against a cost of 0.236 per s.d.) and the weeks (about [$-0.96$, 0.58]); MDEs 0.52 and 1.1 (H1). And "the data
    say that insurance as legislated does not reach it" (`sec7_policy.tex`, first sentence) contradicts the paper's
    own "not shown".
25. "the income that layoffs predict passes on twice as strongly as other parental income ... the contrast
    \citet{shea2000does} draws" (intro) against the body: "it is not a separate finding" (`sec5_standsfor_body.tex`).
26. "Nor is it business income moved out of earnings ... $-0.812^{***}$" and "the labor part of it does not move with
    the father's layoffs (0.079, s.e. 0.468)" (`sec6_career_body.tex`). The interaction with the asset part is
    $-0.315$ (p = 0.105), not reported; s.e. 0.468 in asinh units is "not detected", not "does not move".
27. "Union coverage and government employment do not move with the father's layoffs in a way that carries the cost"
    (`sec6_career_body.tex`, footnote) against government change +0.231\*\* (p = 0.050) and workplace-size change
    $-4.095$\*\*\* (EVIDENCE 11.66).
28. "Whatever the layoff marks or does, it is not a trait passed on to all of a father's children alike" (intro);
    "A trait of the father passed on to all his children alike would lower both profiles" (`sec7_daughters_body`).
    This is right as far as it goes, but it does not exclude a trait passed on by sex (H5).
29. "before the first layoff the father's earnings and employment show no significant pre-trend" (intro): leads of
    0.106\* ($-6$) and 0.113\*\* ($-3$), $-0.005$ at $-2$; joint p = 0.203 (H4).
30. "evaluations that score them early ... or pool them across ages \citep{hoynes2016long, jackson2016effects},
    weight lightly the components that appear after 40" (intro; `sec7_policy`). Pooling over ages that include the
    forties does not weight them lightly unless the age mix is young; give each study's age range or drop "pool".

**Stale text and references**

31. "the comparison below the median of Section~\ref{sec:ageprofile} use the whole profile" (`appA.tex`, "Re-weighting
    ratios"). Section 3 no longer has a below-median comparison.
32. `sec3_ageprofile_main.tex` race paragraph: "in the PSID these are points on rank profiles that are flat in age for
    both races". `tab_rank_age` contradicts it for White sons: their family-income rank-rank slope is 0.287\*\*\* at
    25-29, 0.392\*\*\* at 30-34 and 0.400\*\*\* at 35-39 (Black 0.339\*\*\*, 0.329\*\*\*, 0.346\*\*\*). Write "flat after
    the early thirties for White sons and flat throughout for Black sons".
33. "Wealth passes through the family home, as \citet{pfeffer2018generations} find for educational attainment"
    (`appB_split_body.tex`). The bibliography entry is "Generations of Advantage. Multigenerational Correlations in
    Family Wealth" (Social Forces 2018), which is about wealth correlations; the "educational attainment" attribution
    looks wrong [?].
34. "hegde2026racial" is cited in `appB.tex`; check that its year and venue are final [?].
35. EVIDENCE 11.35 lists Cole, Miller, Huang, Willage and Mayer (2024) as the UI-and-children precedent; it is not
    in the paper or the bibliography [?]. Bailey, Hoynes, Rossin-Slater and Walker (2024), which the earlier memo
    asked for, is still missing [?].
36. Title footnote: "the tables are generated by 28, 44, 90 and 100". The tables now cite many more source scripts
    (103-131); fine as "built by", but the footnote's "Each number in the text comes from the table or the code named
    next to it" fails where the text quotes numbers that appear in neither (items 4, 26, 27).

---

## 4. The earlier memo: what the revision answers

| earlier item | status | what was done / what is left |
|---|---|---|
| K1 wealth functional form, components, SRC | **answered** | rank / log / asinh (29.1, 26.4, 14.5), three-part split, SRC-only; abstract says "between two fifths and a half". Left: "family home" includes other real estate; rank-of-zeros point (K4 here); the permanent-income horse race (K2 here) is new. |
| K2 family-income rise, wealth age profile, gifts | **answered, with a new problem** | own earnings carry the family-income rise (0.276\*\*\* to 0.492\*\*\*; spouse 0.008, other $-0.010$); wealth rank profile 0.228\*\*\* to 0.408\*\*\*; gift receipt by age. Left: cross-cohort profile, early-gift compounding, inheritance truncation, Charles-Hurst benchmark (K3 here). |
| K3 parental age, cap | **answered** | father's 40-50 income (0.267\*\*\* to 0.526\*\*\*), fixed-age fathers (change 0.125\*), cap removes 0.04 percent. |
| K4 attrition | **answered** | stayers' 25-29 IGE 0.257\*\*\* vs 0.275\*\*\* (p = 0.67), NLSY79 bound in Section 2. |
| K5 accounting language | **partly** | tables say "components"; intro and Section 3 still say "what parents do" and "what rises". |
| H1 EITC | **partly** | first stage, eligibility, DiD, daughters, calibration done; "sign" claim removed. Left: the eligibility triple difference (0.064\*\*\* vs 0.017) contradicts the "caution" and is in a footnote; Bastian-Michelmore's estimate is still not stated (H3 here). |
| H2 age of scoring | **partly** | rewritten as "score early or pool"; Hendren cited. Left: Bailey et al. (2024) [?] absent; "pool ... weight lightly" unsupported (item 30). |
| H3 UI power and realised UI | **partly, with a new problem** | realised UI added; waiting-week sentence added; MDEs stated. Left: no pooled index, formulas not coded (said so), two receipt splits contradict, unreported band change $-2.095$\*\*\*, false "exclude only effects larger than the cost" (H1 here). |
| H4 bad times, recessions | **answered, then over-read** | father's loss by bad/good times and recession-by-recession table done. The abstract now builds a causal chain on three insignificant differences (H6 here). |
| H5 mother-headed families, transfers | **partly** | mothers' layoffs added; transfer sentence rewritten. Left: AFDC maximum-benefit moderator not done; the same-sex reading of the new result (H5 here). |
| Z1 recall, father's job | **answered** | recall/new/unknown, sector + occupation + union × age ($-0.226$\*\*), by sector. Left: misclassification makes the comparison uninformative (Z4 here). |
| Z2 self-employed fathers | **answered** | profile without SE fathers $-0.880$\*\*\*, within son $-0.295$\*\*\*; controlled $-0.896$\*\*\* / $-0.233$\*\*. The earlier memo's "most dangerous" point is closed. |
| Z3 self-employed sons, business income | **answered, and it opened the new main problem** | employee-year IGE 0.265\*\*\* to 0.441\*\*\*; asset part added; but the layoff cost now sits in self-employed years (Z1 here). |
| Z4 industry shock, closure code | **partly** | the "code 1 bundles owners' failures" sentence and the "demand-driven unemployment" reading are added. Left: closure and layoff by father's industry/union not shown; CBP/QCEW first stage not tried (Z5 here). |
| Z5 EITC not in family income | **answered** | specification with log parental income reported; text says the credit is not in PSID income. |
| Sentence table (earlier §5) | **mostly answered** | Left: intro "Shocks the father did not choose carry no cost"; Section 3 "most"; Section 8 first sentence on insurance; intro Shea sentence. |

**New in this memo** (not in the earlier one): the cost's concentration in self-employed son-years and the
insignificant within-son wage bend outside them (Z1); moonlighters inside "self-employed", survey underreporting, the
salary-distribution split (Z1, Z2); employer-size and government shifts (Z3); layoffs versus firings and the CYA
evidence that firings carry the component (H2); contradictory UI-receipt splits and a test run where there is no
cost (H1); mediator conditioning in the closure contrast and the pre-layoff dip (H4); the same-sex pattern of the
mothers' result (H5); inference from insignificant mechanism differences (H6); the spells opening's insignificance in
split B and under the IV correction (K1); wealth as a permanent-income proxy and the 3.5-versus-half comparison
across samples (K2); the cross-cohort wealth profile and early-gift compounding (K3); the rank-of-zeros business
share (K4); and the 36-item consistency list in Section 3.

---

## 5. Ranked actions

| rank | action | answers | days |
|---|---|---|---|
| 1 | **Pin down the self-employment result.** Treated counts behind the SE-years slope; "self only" vs "self and others"; consumption- and wealth-based underreporting check (Hurst-Li-Pugsley [?]: food 1968+, total consumption 1999+, net worth 1984+); total head income incl. dividends/interest/rent; incorporated split if asked [?]; occupation decomposition on employee years only; report the $-0.315$ (p = 0.105) and $-0.174$\* employee-year numbers. Then rewrite the headline to whatever survives. | Z1, Z2, Z3(iii) | 3-4 |
| 2 | **Consistency and wording pass** (Section 3 items 1-36): log-point units; Figure 1 vs the 0.110; "in the wage, within the same son"; "one component"; "most"; "a fifth or more"; 0.677 vs 0.764; NLSY79 cohort; AFQT "before entry"; "every cohort"; causal verbs; insurance sentences; mothers "size of the father's cost"; 0.89 per unit share; stale `appA` reference; Pfeffer-Killewald attribution. | all three readers; credibility | 1.5 |
| 3 | **Layoff or firing.** CYA mothers' firings vs layoffs by the child's age and within child; reconcile the two PSID UI-receipt splits (one definition, band + within-son, treated counts); "layoff or firing" in definitions and abstract. | H2, H1 | 2-3 |
| 4 | **Re-anchor the IGE bridge.** Report split-B and IV openings of spells and of the layoff element; the layoff element's share of the IGE rise; rewrite the abstract's first sentence and Section 3.4's last paragraph; NLSY97 "a quarter" wherever skill at entry is claimed. | K1 | 1 |
| 5 | **Insurance, honestly sized.** Intervals in units of the cost; state that the simulated-rate sample has no cost; one pooled insurance index on the full window, or move UI to the appendix with one sentence in the text; change Section 8's first sentence. | H1 | 2-3 |
| 6 | **Pre-window parental income** in place of (and next to) the 13-19 mean for the band profile, within-son slope and closure contrast; plot and describe the event-study leads. | H4 | 1-2 |
| 7 | **Wealth horse race and the wealth age profile.** Wealth share with parental income at the father's 40-50 or the longest average; profile within fixed cohorts and with son FE; cumulative gift/inheritance value as control; housing vs non-housing outcomes; cite Charles-Hurst and Boserup-Kopczuk-Kreiner [?]; asinh component shares in the text. | K2, K3, K4 | 3 |
| 8 | **Employer side.** Government and size estimates in the text; CPS industry wage premium split of the within-occupation cost; son's own industry × age in the within-son design. | Z3 | 2 |
| 9 | **EITC triple difference** in the text with its p-value and number-of-children × birth-year × age controls; Bastian-Michelmore estimate stated; "why not looking" to a footnote. | H3 | 2 |
| 10 | **Mothers and the same-sex reading.** AFDC/TANF maximum-benefit moderator (UKCPR); wives' job-end reports in two-parent families if the PSID asks them [?]; rewrite the "nor is it that a parent's layoff helps daughters" sentence. | H5 | 2 |
| 11 | **Mechanism sentences as point-estimate patterns** (bad times, small loss, repeated) with their p-values; optional CBP state × industry bad-times classification. | H6 | 1 (+2) |
| 12 | **Recall misclassification correction** and "not distinguishable" wording; CBP/QCEW state × industry demand shock with its first-stage F. | Z4, Z5 | 1 + 3 |

About 25-30 working days in all. Actions 1-4 (8-10 days) decide what the headline is and remove the errors a
reader would find first. Do them before any further section rewrite: action 1 can rename the result, and action 3
can rename the treatment.

**Where restricted data would settle a question (one line each; nothing above depends on them).** Employer premia
and firm size for the sons: LEHD. Layoff versus firing and UI disqualification: state UI administrative records.
Self-employment income as reported to the IRS: tax records. Bequest timing: Nordic registers with parental death
dates.
