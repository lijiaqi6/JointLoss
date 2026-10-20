# How far is Paper B from a top-5 submission in substance? (Fable, referee/editor view, 2026-10-20)

Read in full: `paperB_age_profile/main.tex`, sec1, sec3_data, sec3_ageprofile, sec4_passedon, sec5_skill,
sec6_stability, sec7_policy, sec8_conclusion; the main-text tables (tab_passed_on, tab_four_by_four,
tab_passed_on_data, tab_layoff_age, tab_layoff_fe, tab_shea_spell, tab_ui_stability, tab_son_friction, tab_group_race,
tab_skill_entry, tab_ige_sons, tab_three_data, tab_father_disp_age). Skimmed: appA, appC_entry, appD_race.
Background: `EVIDENCE.md` rows 11.28-11.40 and Sections 8-10; `proposals/paperB_primary_goal_20261020.md`,
`paperB_outline_race_neutral_20261020.md`, `fable_what_is_passed_on_literature.md`, `fable_policy_shocks_paperB.md`;
`output/layoff_cost_by_age.md`, `ui_stability_channel.md`, `shea_contrast_by_spell.md`, `what_is_passed_on.md`; the
docstrings of scripts 75, 80, 88 and 19. Nothing was run; no existing file was touched. Every number below is quoted from
those files; where I derive a number myself I say so. Prose, exposition and length are ignored, as asked.

---

## 1. Verdict

**Not a top-5 submission as it stands, and not one major addition away: it is two.** In its current form the paper is
a strong field-journal paper (JOLE, JHR, Labour Economics; AEJ: Applied is a stretch): a careful descriptive
accounting of the PSID earnings IGE by the son's age, with one striking new fact (a father's layoff in the son's teens
is unrelated to the son's earnings at 25-29 and costs 0.110\*\*\* log points per layoff year at 45-49, Table
`tab_layoff_age`) and one clean quantification (the son's AFQT carries 62 percent of the NLSY79 rise, Table
`tab_skill_entry`). A top-5 referee will treat the Gelbach shares as accounting (which the paper itself concedes
five times), will note that the IGE rising with age is known, and will then ask the only question that matters for the
paper's claim to a mechanism: *is the delayed cost of a father's layoff a causal effect of the layoff, or the rising
pay-off of a paternal trait that layoffs select on?* The paper cannot answer this. **That is the single biggest
substantive gap**: the headline fact rests on a self-selected treatment (the PSID's combined `laid off / fired` code)
in one data set, with, by my estimate, on the order of 130 treated sons in the 45-49 band (the paper never reports the
count), and the two defences offered do not discriminate. The plant-closure contrast has a change of 0.000 with s.e.
0.258 (Table `tab_layoff_age`), a confidence interval that includes half the layoff change; and the timing placebos
(layoffs at the son's 6-12 and 20-26) are nulls with s.e. 0.109 and 0.102 against a teen coefficient of -0.322\*\*\*
(s.e. 0.124) on a half-sized sample (2,171 of 4,644 sons; `output/layoff_cost_by_age.md`, Section 3), and the paper
tests none of the three windows against each other. The second gap is that headline 1, which the title and abstract are
built on, is a mediation accounting whose shares are known to move with measurement error (the paper's own NLSY97
column shows it) and whose "rest" of 47.6 percent is read as "money, or what it buys" without any evidence that it is
money. Close these two and the paper has a top-5 case as a "new fact plus identified mechanism" paper on parental job
loss and the life cycle of the IGE; leave them and the paper's ceiling is a good field journal.

---

## 2. What a top-5 referee would accept as the contribution, and what is already known

### Accepted as new

1. **The delayed cost of a father's teen-year layoff** (headline 2), *if it survives a selection-robust design*. The
   parental-job-loss literature scores children in their twenties: Oreopoulos, Page and Stevens (2008, JOLE) at about
   25-33, Hilger (2016, AEJ: Applied) in the mid-twenties, Bratberg, Nilsen and Vaage (2008, Labour Econ.) twelve to
   fifteen years after the event, Page, Stevens and Lindo (2009, NBER volume; PSID) and Kalil and Wightman (2011)
   likewise. None follows the child to 45-49. A profile that is zero in the twenties and -0.11 log points per layoff
   year at 45-49, in the hourly wage, within the same son (Table `tab_layoff_fe`, -0.236\*\* per ten years per unit
   share), would reconcile Hilger's small effects with the large IGE and is the kind of fact a top-5 journal publishes.
   But as it stands it is a fact about a selected variable, not about layoffs.

2. **The parent-side split of the IGE by the son's age** (headline 1) is new in form. The precedents split the son's
   side (Blanden, Gregg and Macmillan 2007, EJ; Gregg, Macmillan and Vittori 2019; Rothstein 2019, JOLE) or model the
   joint transmission of wages and hours without an income IGE (Altonji and Dunn 2000, JHR). A referee will accept the
   novelty of the object and deny that the object identifies anything (Section 3, objection 2).

3. **The AFQT carrying 62 percent of the rise with age in the NLSY79** is a clean quantification. It is, however,
   derivable from two known facts: the return to AFQT rises with experience (Altonji and Pierret 2001, QJE; Lange
   2007, JOLE; Arcidiacono, Bayer and Hizmo 2010, AEJ: Applied, where the rise is confined to high-school graduates
   [?]), and AFQT is strongly correlated with parental income. The new piece is the magnitude and the claim that the
   schooling return rises too, which the paper reads as complementarity rather than learning. In a single cohort
   (born 1957-64, observed 1982-2018) the rise of the schooling return with age is not separable from the national rise
   of the college premium over 1980-2000 (Section 3, objection 5).

### Already known (the referee will say so)

- **The log IGE rises with the son's age until about 40.** Haider and Solon (2006, AER); Grawe (2006); Nybom and
  Stuhler (2016, 2017, JHR); Mazumder (2016, Research in Labor Economics, PSID: the IGE rises to the late thirties)
  [? exact ages]; Gregg, Macmillan and Vittori (2017, OBES) for the UK; Dahl and DeLeire (2008) with SSA records. The
  paper's 0.276\*\*\* to 0.492\*\*\* is a cleaner version of a known profile, and ranks plateauing by the early thirties
  (Chetty, Hendren, Kline and Saez 2014, QJE) is also known. The paper is right to use the profile as the frame and
  wrong to list it among its contributions.
- **The level difference in the Black and White IGE and Black downward mobility from the top**: Hertz (2005),
  Bhattacharya and Mazumder (2011, QE), Mazumder (2014), Chetty, Hendren, Jones and Porter (2020, QJE). The paper says
  the new part is the timing (flat for Black sons, rising for White sons). Correct, and under the race-neutral framing
  it is heterogeneity, not a headline.
- **Income from sources beyond the parents' control matters little** (Shea 2000, JPubE); and plant closures, unlike
  layoffs, carry no information about the worker (Gibbons and Katz 1991, JOLE). Headline 5 is a restatement of these
  two plus headline 2 (Section 3, objection 4).
- **The son's own unemployment is a large part of a young man's earnings variance** and of the intergenerational
  correlation of unemployment (Corak, Gustafsson and Osterberg 2004; Macmillan 2014; Blanden et al. 2007 "attachment"
  0.03 of 0.32). Headline 4 is a mechanical decomposition of the outcome into its own parts, as the paper's footnote
  admits.
- **UI generosity and children**: the team's memo cites Cole, Miller, Huang, Willage and Mayer (2024, AEA) with tax
  records and trigger-based variation [? version and venue; verify before citing]. Against that, a p = 0.50 split on
  3,495 sons is not evidence (Section 3, objection 3).

### Claims to check or soften

- Section 5 says the within-occupation rise, the early-job cell and the schooling results are "descriptive"; fine.
  But the introduction's "Because the returns to both schooling and measured skill rise with age, the pattern is that of
  skill complementing human capital, not of employers learning about it" is an inference that the employer-learning
  literature would dispute: under Farber and Gibbons (1996) / Altonji and Pierret (2001), the schooling return *falls*
  with experience *conditional on AFQT* when schooling is a signal; the paper reports both rising in one regression
  (Appendix `tab_afqt_growth`, +0.049\*\*\* and +0.036\*\*\*). That is informative only if the calendar is held fixed,
  which a single cohort cannot do.
- The paper reports two different pooled IGEs at 45-49: 0.484\*\*\* (Table `tab_ige_sons`) and 0.443\*\*\* (Table
  `tab_passed_on`, the 4,770-son split sample). A referee will notice and ask which sample the headlines are on.
- Hu and Taber (2011, JOLE) find the Gibbons-Katz layoff stigma for White men only [? details]; if so, the closure-layoff
  contrast means something different by race, which the race subsection of Section 6 should confront rather than read
  the Black within-son coefficient (-0.306\*\*, which falls to -0.068 with the timing controls, Table `tab_layoff_fe`
  columns 3-4) as "as much as the White one".

---

## 3. The most serious substantive objections

### Objection 1 (fatal if unanswered): the layoff is selected, and the paper's defences do not discriminate

The PSID code behind the headline is `laid off / fired` (script 19 docstring: code 3, "laid off, fired", undivided in
every wave). Fathers who are fired, and fathers laid off repeatedly (Stevens 1997, JOLE), differ in traits that are
transmitted (ability, health, temperament, conflict). The paper's own Section 5 shows that the pay-off of transmitted
skill *rises with the son's age* (AFQT 0.077\*\*\* at 25-29 to 0.181\*\*\* at 50-54). So a layoff that marks a paternal
trait would produce exactly the observed profile, zero at 25-29 and large at 45-49, with no causal role for the layoff.
The within-son fixed-effects design does not remove this: a fixed son trait whose *return* grows with age bends the
profile too, as the paper's note to Table `tab_layoff_fe` half-concedes ("what grows with age is the cost"; the
alternative is "what grows with age is the return to the trait").

The two defences:

- **Closures.** The closure change between 25-29 and 45-49 is 0.000 (s.e. 0.258); the layoff change is -0.914\*\*\*
  (s.e. 0.252). The paper never tests the difference (my rough calculation: about -0.9 with s.e. about 0.36 if the
  two were independent, so it would pass at 1 percent, but the common bootstrap draws exist and the test should be
  reported). More important, the closure confidence interval admits a closure cost of up to half the layoff cost, so
  "a plant closure carries no cost at any age" is a null with low power, not a finding. The closure share also
  *raises* the son's wage at equal income (0.021\*\*, Table `tab_four_by_four`), which the paper reads as the
  Gibbons-Katz signature; a referee will read a positive closure coefficient as a sign that the closure variable is
  itself picking up something (fathers in closing plants are in manufacturing, unionised, higher-tenure).
- **Timing.** The 6-12 and 20-26 windows are measured on the father's head-years "in any family unit" and require the
  father to be observed as a head in those years, which halves the sample (2,171 of 4,644 sons) and removes sons born
  before about 1962 from the 6-12 window (the PSID starts in 1968). The windows are never tested against each other.
  With point estimates -0.081 (s.e. 0.109), -0.322 (s.e. 0.124) and 0.037 (s.e. 0.102), the 6-12 versus 13-19
  difference is about 0.24 with s.e. roughly 0.16 (my calculation, assuming independence): not significant. "Only
  layoffs in his teens carry it" is therefore not established. And a layoff at 20-26 falling in the son's own
  labor-market entry years is not a clean placebo for a trait: Carneiro, Lopez Garcia, Salvanes and Tominey (2021,
  JPE) show that the effect of parental income is U-shaped in the child's age, so a trait that matters through
  parental resources could legitimately matter more at 13-19 than at 20-26.

**How damaging:** fatal for the paper's claim to a mechanism, not for the fact. A referee will write: "an interesting
correlation whose causal status the paper cannot establish; the authors should exploit variation in layoffs that is
not the father's choice." Section 4, additions A1-A3, are the answer.

### Objection 2 (serious): the Gelbach split is accounting, its shares move with measurement error, and the "rest" is not identified as money

- Each share is gamma_k x delta_k. Attenuation in a component measured with error shrinks gamma_k and pushes its
  share into the "rest". The paper's four-data-set table (`tab_passed_on_data`) demonstrates this: the same wage and
  spells that carry 12-19 percent and 5-8 percent in the multi-year PSID and CYA carry nothing in the one-year
  NLSY97. The paper presents the NLSY97 as a "test of measurement" that the split "fails"; a referee presents it as
  proof that the PSID shares are lower bounds of unknown size, so that "half of the IGE is parental income at equal
  measured components" has no quantitative content.
- The "rest" in panel B (47.6\*\*\*) is the coefficient on log family income holding fixed the parents' log labour
  income (`lpl`, script 80), their asset-income share, transfer share, other members' share, home ownership, family
  size, schooling and the four components. Given labour, asset, transfer and other income shares, what variation in
  log family income remains? Timing (the mean of logs versus the log of the mean), years without a valid wage,
  clipping of shares to [0, 1], and functional form. A referee will not accept "money, or what it buys, which these
  data do not measure" for a residual that, by construction, is largely the gap between a log mean and a mean of logs.
  Either show what identifies the 47.6 percent (and that it is wealth, Section 4, B3) or stop interpreting it.
- The components are means of *logs* of the father's wage and hours over 13-19, so the identity log earnings = log
  wage + log hours holds year by year but not for the window means; the wage share of 19.0 percent falling to 12.0
  percent when the father's schooling enters shows how much the attribution depends on which correlates are in. The
  policy map (wage -> schooling policy; spells -> UI) is asserted, not derived.

**How damaging:** it removes headline 1 as a top-5 contribution on its own; it survives as the frame within which
headline 2 is found. The title should not rest on it.

### Objection 3 (serious): the UI test has no power and the split design is confounded

- Panel A of `tab_ui_stability` splits sons at the median of childhood UI generosity *across states* (within cohort);
  there are no state fixed effects in the split. Generous-UI states (Northeast, Midwest, West Coast) differ from less
  generous ones (South) in everything that bears on the IGE. The difference of -4.1 points (s.e. 6.0, p = 0.496)
  cannot be read as the sign of insurance.
- Panel B has state fixed effects, and the paper reports that the within-state-and-cohort standard deviation of
  generosity is 0.041 against 0.089 overall; the layoff x UI interaction is 0.021 (p = 0.19), the closure x UI 0.034\*\*
  (p = 0.045), one placebo of four is significant in the Black panel. "Every sign is that of insurance offsetting the
  spells component" is a reading of eight noisy coefficients. A referee would want a minimum detectable effect; at
  these standard errors it is larger than any plausible insurance effect on a 6 percent share.
- Generosity is the state's maximum weekly benefit over the average weekly wage, averaged over ages 12-18; it is not
  the replacement rate the father faced at his layoff (the maximum binds only for higher earners), and it varies
  mostly across states.

**How damaging:** headline 3 should not be a headline. As a sign check in a policy section it is harmless; as "the
components point to policy" it invites the referee to say the paper tests nothing.

### Objection 4 (moderate): headline 5 is headline 2 restated, and its closure half is uninformative

b_P in `tab_shea_spell` is the coefficient on the part of parental income predicted by the father's layoff share; with
one predictor it is the reduced form of the layoff on the son's earnings divided by the layoff's gradient in parental
income, i.e. a Wald ratio whose exclusion restriction the paper's own headline 2 rejects (the layoff affects the son
beyond income). So 0.742\*\*\* is not "income tied to layoffs passes on twice as strongly"; it is the layoff's total
association rescaled. The closure instrument predicts 0.4 percent of the variance of parental income (R2 0.004) and
gives 0.074 with s.e. 0.561: the confidence interval runs from about -1.0 to +1.2 and "agrees" with any value of
Shea's elasticity. Nothing in this table is a separate finding.

### Objection 5 (moderate): age versus period in a single cohort, and in the pooled profile

- The NLSY79 cohort is observed at 25-29 in 1982-93 and at 50-54 in 2007-18. The return to schooling and to measured
  skill rose nationally over 1980-2000. "The return to schooling rises by 0.049\*\*\* ... and to the AFQT by 0.036\*\*\*"
  across the bands is age + period. Appendix D nets a calendar trend for the *racial difference* (EVIDENCE 9.27) but
  not for the pooled rise, and the NLSY79 cannot do it alone.
- The pooled PSID profile is defended against period effects only through the racial opening (Appendix D: cohorts
  1951-64, 1965-79, 1980-89 each show the *gap* opening; year fixed effects in each band). The same checks for the
  pooled IGE rise and for the AFQT share should be in the paper; and the NLSY97 (born 1980-84, now 37-43, with the
  1997-99 ASVAB) is the second cohort that separates age from period for the AFQT result at no cost.

### Objection 6 (moderate): measurement of the layoff share across cohorts, and the treated count

Script 19's docstring records that the job-end reason was asked in 1971-75 only if the job was less than a year old
and in 1976-83 only if the present position was under 12 months, with different branches in 1988-2001. The father's
layoff share at the son's 13-19 is therefore measured with a wave-dependent net; sons at 45-49 (teens in the 1970s)
carry a different measure than sons at 25-29 (teens in the 1990s-2000s). Cohort dummies within a band do not fix a
cross-band comparison. The within-son design does, which is why it should be the primary estimate (Section 4, A6).
The paper also never reports the number of father-present sons with a layoff year in each band; by my calculation
from Table `tab_ige_sons` (1,497 sons at 45-49), the father-present rate (about 72 percent; 3,449 of 4,770) and the
12.4 percent any-layoff rate, it is on the order of 130. A -0.768 coefficient with s.e. 0.272 on 130 treated sons in
an unbalanced band is exactly the kind of estimate a referee asks to see leave-one-cohort-out.

### Objection 7 (minor but will be raised): the race-neutral framing contradicts the paper's own evidence

The abstract ends "The rise is White". The opening of the IGE (0.232\*\*\*), the spells opening (White 0.066\*\*,
Black -0.042), the father's schooling share (0.065\*\*\* versus 0.002) and the layoff gradient (-0.046\*\*\* versus
-0.010\*) all differ by race, and for Black sons "the rest" is nothing and family structure is 60 percent. A referee
will ask why a paper whose every mechanism is White pools, and whether the pooled "what parents pass on" is a
weighted average of two different processes. The PI has decided the framing; the defence must then be explicit: the
mechanism (layoff cost) is common, the gradient (who is laid off) differs, and the paper says so in each section.
That is a sound position, but the Black within-son result that supports "the cost is common" is -0.306\*\* without
and -0.068 with the timing controls (568 sons). Report the common-cost claim with its fragility.

---

## 4. Concrete additions that would close the gap, ranked (public data only)

### A. Make the teen-layoff cost selection-robust (serves headline 2; this is the paper)

**A1. Predicted layoffs from industry demand shocks (an instrument the father did not choose).** PSID, father-present
sons, father's 3-digit industry in the first window year (available 1968-). Build, for each father, the national
employment change of his industry over the son's ages 13-19 (CPS or BLS CES industry employment; the Bartik logic
already in `8a.StateShocks.py`, but at the father's own industry, nationally, not the state aggregate). First stage:
father's layoff share on the industry employment decline (and its interaction with the father's tenure at the start of
the window, since low-tenure workers are laid off first). Second stage (or reduced form, which is the honest
object): son's log earnings by band, and the within-son layoff x age slope, with the father's industry *level* fixed
effects (so the variation is the shock to his industry during the son's teens, not which industry he is in), log
parental income and the components as now. Convincing result: the reduced form of the industry shock on the son's
earnings profile is zero at 25-29 and negative at 45-49 with the same shape as the OLS; a Hausman-type comparison
of IV and OLS slopes; a placebo with the shock timed at the son's 20-26. A zero IV slope with a precise standard
error would also be a result: the headline would then be about selection, and the paper would change (Section 6).
Effort: moderate (two weeks: industry crosswalk exists in script 32 for sons; apply to fathers).

**A2. Timing as the control group (Hilger's design).** Restrict to sons whose father was *ever* laid off or fired
(any window: 6-12, 13-19, 20-26), so that every father in the sample has the layoff trait, and compare sons by
*when* it fell. Estimating equation, son-years 25-55, son fixed effects:
y_it = a_i + sum_a d_a 1[age=a] + sum_a b_a 1[age=a] x Teen_i + (components, lyp, cohort) x age + e_it, Teen_i = the
layoff fell at 13-19 rather than only at 20-26 (and separately only at 6-12). Convincing result: b_a for the teen
group becomes negative after 40 while the 20-26-only group's profile is flat; a joint test of equality of the three
timing profiles, which the current Table `tab_layoff_fe` lacks. This design is the paper's own timing argument made
into a comparison of like fathers, and it is cheap. Report the N in each timing group; expect a few hundred sons each.
Effort: one week.

**A3. Separate what the layoff is from what it does.** Three cheap splits that a referee will ask for:
(i) layoffs followed by *recall* to the same employer versus permanent separations (PSID tenure / same-employer
flags; a recall carries no lemons signal, Gibbons and Katz); (ii) layoffs with a large versus a small fall in family
income in the layoff year (if the cost is money or turmoil, the large-loss layoffs carry it; if a trait, both do);
(iii) single versus repeated layoffs in the window (Stevens 1997: the repeat-loss trait). Also control for parental
income at the son's 20-26 (available for most of the sample) to close the "money after the teens" channel the paper
cannot currently rule out: a father's layoff at 15 lowers family income during the son's college years, and that is
not in the 13-19 parental-income measure. Effort: one week in total.

**A4. Daughters.** The same profile on daughters' hourly wage and earnings (father's layoff at 13-19; the PSID has
them). An independent sample of the same size that either shows the delayed cost or does not; either way it belongs
in the paper. Effort: days.

**A5. A second data set for the age profile of the layoff cost.** None of the listed US public files can do 45-49
with a father's job-end reason (CYA children are 26-35; NLSY97 parents' breaks have no reason). Two options, both
outside the PI's listed data but neither restricted US data: the German SOEP (1984-, job-end reasons since 1985 with
"plant closure" and "dismissal by employer" as separate codes; children of 1984 households are now 50-58; scientific
use file by standard contract with DIW, open to UK academics) [verify codes and access]; and the UK BHPS/UKHLS
(1991-, "made redundant" versus "dismissed or sacked"; children of 1991 households born 1975-85 are now 40-50, so the
45-49 band is only just reachable). I would run the SOEP: a replication of the delayed cost with layoffs and
closures separated from firings is the single result that would most reassure a top-5 referee. Effort: a month
including the contract. If the PI rules this out, say in the paper that no US public file can replicate the 45-49
band and show the CYA at 36-44 (EVIDENCE 11.33 flags `earn_last` for the 1970-84 births) with its honest standard
errors.

**A6. Report what is missing from the current tables.** The number of treated sons by band; the test of equality of
the layoff and closure changes on the common draws; the test of equality of the three timing windows; a
leave-one-five-year-cohort-out profile; the within-son estimate as the primary number (it is immune to the
wave-dependent measurement of the layoff share, Objection 6); and the Black within-son result with and without
timing controls side by side. Effort: days.

### B. Make headline 1 measurement-robust and the "rest" interpretable (serves headline 1)

**B1. Errors-in-variables-corrected shares.** Split each parent's window into odd and even wave-years; measure each
component on the odd years and instrument with the even years (Solon 1992 logic), so gamma_k is purged of
attenuation; run the Gelbach split with the IV gammas (the delta_k are gradients in parental income and need the
same treatment). Report the corrected shares next to the raw ones and show that the NLSY97 one-year columns, once
corrected by their reliability ratios (which Section 2 already computes for income), line up. Convincing result: the
wage and spells shares rise and the "rest" falls by an amount the paper can state. Effort: two weeks.

**B2. Show what identifies the rest.** With parents' log labour income, the asset, transfer and other-member shares
all held fixed, state in a footnote (and verify by simulation on the PSID) how much of the remaining variance of log
family income is the log-of-mean versus mean-of-logs gap and years without a valid wage. If most of it is, drop
"money or what it buys". Effort: days.

**B3. Parental wealth.** The PSID wealth supplements (1984, 1989, 1994, 1999 and biennially after) fall in the teen
window of sons born 1970 and later. Add net worth (and home equity) at the son's 13-19 as a mediator for that cohort
and report whether the rest falls; Pfeffer and Killewald (2018) [?] give the wealth-mobility benchmark. This is the
one measured resource that could make "money" a finding rather than a label. Effort: one week.

### C. Make the UI test a test or demote it (serves headline 3)

**C1. Simulated replacement rate at the father's wage** (Gruber 1997, AER; East and Kuka 2015, JPubE; Kuka 2020,
REStat; Chetty 2008, JPE). From the DOL "Significant Provisions" schedules, code each state-year's weekly benefit
formula (fraction of high-quarter wages), minimum, maximum and maximum duration; apply it to the father's pre-layoff
earnings to get the benefit he would have received; the identifying variation is the state x year x father's-wage
interaction within state and cohort, which is far larger than the 0.041 the current measure has. Interact with the
layoff share in the within-son design; placebo with the father's wage x generosity and the closure share x
generosity. Convincing result: a positive layoff x replacement-rate slope on the son's profile with a precise s.e.
and a null placebo. The PSID also records the head's unemployment compensation received each year (1970s on), so the
actual replacement rate at each layoff year is a second measure. Effort: three weeks (the formula coding is the
work; the team has the maximum already in `12b.UIGenerosity.py`).

**C2. Extended-benefit variation.** Federal and extended-benefit programs (1975-77, 1982-85, 1991-94, 2002-04,
2008-13) and state EB triggers change the *duration* available at the father's layoff date within state; weeks
available at the layoff is a second within-state instrument (DOL trigger notices are public). Effort: two weeks.

**C3. If neither is run,** report a minimum detectable effect for the current design and move the UI result to a
footnote in Section 6. A headline with p = 0.50 is a target for the referee.

### D. Separate age from period (serves the age-profile frame and the AFQT result)

**D1. NLSY97 ASVAB age profile.** Repeat Table `tab_skill_entry` on the NLSY97 (ASVAB 1997-99 percentile, parental
income 1996 and the youth-reported later years) at 25-29, 30-34, 35-39, 40-44. The cohort is 20 years younger, so
the same AFQT share rising with age in both cohorts is age, not period. Effort: days (scripts 85 and 87 exist).

**D2. Pooled rise within cohorts and with year fixed effects**, for the IGE itself and for the components' shares:
the appendix does this for the racial gap only. Effort: days.

### E. Headline 4 (son's own spells) and the policy section

Nothing to add; demote (Section 5). If kept, the only addition that makes it more than arithmetic is the share of the
*parents'* spells that runs through the son's spells (the paper has it: 0.016\*\*\* at 25-29, 0.004 at 45-49), which
belongs in Section 6 as the first mechanism tested and rejected.

### F. Optional, high-value demonstration for "the age of scoring"

The paper asserts that policies scored at 30 miss the components that grow. The one public-data design that can show
it is the EITC expansion of 1993-96 re-scored by age in the PSID (Bastian and Michelmore 2018, JOLE, used the public
PSID through 2013; the 2015-21 waves add ages up to the early forties). Whether the EITC effect on children's earnings
grows or fades with the child's age is a finding either way. Effort: three weeks; not required for the core.

---

## 5. What to cut or demote because it dilutes the contribution

1. **Headline 5 (the Shea contrast)**: demote to a paragraph in Section 6 that states the Wald-ratio reading
   honestly, or drop. Its closure half has s.e. 0.56.
2. **Headline 4 (the son's own spells)**: a footnote on life-cycle bias. It is arithmetic on the outcome, and the
   paper says so.
3. **Headline 3 (UI)**: a footnote unless C1 or C2 is run.
4. **Section 7 "Group search friction"**: it carries the IGE only between races and the paper admits it "cannot be
   told apart from anything else that differs by race". In a race-neutral paper it has no content; the CPS job-finding
   measure may return in a race appendix.
5. **Section 7 "Transfers"** (AFDC years 6.6\*\*): the paper cannot say whether receipt marks selection or what welfare
   did; one sentence in Section 4.
6. **Section 7 "The age of scoring"**: an assertion drawn from the shares; keep one paragraph in the conclusion unless
   F is run.
7. **Section 5.2 "Where in the career"** (occupation score, early-job cell, access): three tables of descriptive
   mediation that duplicate the message of 5.1 ("the rise is within occupations and runs through schooling"). One
   paragraph and one table.
8. **Appendix D (343 lines of racial robustness)**: under the race-neutral decision it should shrink to what the race
   subsections cite. Appendix B (industries, tenure, promotion) is from the earlier paper and no main-text claim
   depends on it.
9. **The "half is money" sentence** in the abstract, introduction and conclusion, until B1-B3 are done.
10. **"Only layoffs in his teens carry it"** and **"a plant closure carries no cost at any age"**: replace with
    statements that carry the tests of equality and their confidence intervals (A6).

The structural model: the PI dropped it. A model is not what a top-5 referee will ask for here; an identified source of
variation in the father's layoff is. A model without that would not help, and with it the paper does not need one.

---

## 6. Recommended path to submission

1. **Decide the paper's fate on A1 and A2 first** (three to four weeks). If the industry-shock reduced form and the
   timing-control design both show the delayed cost, the paper is a "new fact and mechanism" paper on parental job
   loss over the son's life cycle, with the split as its frame; aim at JPE or REStud, with AEJ: Applied as the
   fallback. If they show nothing, the honest paper is: the IGE's components by age, with the layoff profile as a
   selection result (what layoffs reveal pays more with age, as AFQT does), which is a JOLE/JHR paper and should be
   written as such without delay.
2. **A3-A6 in parallel** (two weeks): recall/permanent, income-loss, repeat splits; parental income at 20-26 as a
   control; daughters; the missing tests and counts; the within-son estimate as primary.
3. **B1-B3** (three weeks): measurement-corrected shares, the identification of the rest, wealth for the post-1970
   cohort. Then decide whether "half is money" survives.
4. **D1-D2** (one week): NLSY97 ASVAB profile; within-cohort and year-FE pooled profiles.
5. **C1 or C3** (three weeks or one day): the simulated replacement rate, or demote the UI test.
6. **A5 if the PI will go outside the US files** (one month, can run alongside 2-5): SOEP replication of the delayed
   cost with firings separated.
7. **Restructure around two or three headlines**: (i) the split by the son's age as the frame, measurement-robust;
   (ii) the delayed cost of a father's layoff, selection-robust, with closures and timing as tests reported with
   their power; (iii) the AFQT and schooling pay-off rising with age in two cohorts. Race as a subsection in each.
   Cut Section 7 to one page.
8. **Then** decide the venue by what A1-A2 returned. Do not submit to a top-5 journal on the current evidence: the
   first referee question (Objection 1) has no answer in the paper, and the second (Objection 2) is answered only by
   conceding it.
