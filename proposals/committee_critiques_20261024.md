# Paper B against three readers: Kopczuk, Hoynes, Zwick (Fable, 2026-10-24)

**Purpose.** The PI asked what would make the research more solid if it is read by Wojciech Kopczuk (wealth
measurement, top incomes, estate taxation, long-run earnings mobility), Hilary Hoynes (EITC, Food Stamps, the safety
net's long-run effects on children, recessions) and Eric Zwick (firms, pass-through business income, business owners,
investment and tax policy). This is not an application and not a proposal; it is a list of the critiques each would
raise about the research as it stands, how damaging each is, and the public-data analysis or rewrite that answers it.

**Read.** `paperB_age_profile/main.tex` and its inputs (sec1, sec3_data, sec3_ageprofile_main, sec3_frame, sec3_race,
sec4_layoff(+_body), sec5_standsfor(+_body), sec6_career(+_body), sec7_daughters(+_body), sec7_policy, sec8_conclusion;
appA, appB_split_body, appC_skill_body, appB, appD_spells_body, appE_policy, appD_race, appC_entry); the tables
tab_split_main, tab_passed_on, tab_layoff_age, tab_layoff_selection, tab_layoff_mechanism, tab_eitc_age,
tab_ui_stability, tab_father_se; `EVIDENCE.md` rows 11.28-11.65; `proposals/fable_top5_distance_paperB_20261020.md`,
`fable_qje_round2_paperB_20261020.md`, `jpe_simulated_review_20261020.md`, `paperB_round2_plan_20261020.md`; the
docstrings of `1.PSID.py`, `6.IGEMain.py`, `19.FatherDisplacement.py`, `75.WhatIsPassedOn.py`, `80.WhatIsPassedOnRest.py`,
`82.UIStabilityChannel.py`, `12b.UIGenerosity.py`, `91.LayoffSelection.py`, `98.ParentalWealth.py`, `101.EITCByAge.py`.
Nothing was run; no existing file was touched. Every number is quoted from those files. Literature claims I could not
verify against a file are marked [?].

**Constraints honoured.** Public data only (PSID, NLSY79/97/CYA, CPS, BLS, DOL, UKCPR schedules); no restricted US
data and no requests to US teams (one line per item says where restricted data would settle a question, nothing
depends on it); no sibling designs; no long balanced panels as evidence against a finding; race as heterogeneity; no
structural model; SOEP / Understanding Society deferred.

---

## 0. The one-paragraph verdict

The paper's fact (a father's layoff in the son's teens is unrelated to the son's earnings at 25-29 and costs
0.110\*\*\* log points per layoff year at 45-49, within son, in the wage, in every cohort, surviving Holm and
Romano-Wolf) is well defended against the mobility and displacement literatures the earlier reviews simulated. It is
less well defended against these three readers, because each works on something the paper treats as a side issue:
**Kopczuk** on how wealth is measured and whether an earnings IGE is the right object for wealth transmission (the
paper's wealth share is 29.1\*\*\* as a rank and 14.5\*\*\* as asinh, from one measure at the son's 12-20, with no
wealth outcome for the son); **Hoynes** on the EITC paragraph, whose "sign reversal" rests on $-0.016^{*}$ ($p = 0.052$)
against $-0.003$ with a change of $+0.014$ ($p = 0.47$), on an intent-to-treat exposure with no first stage shown and a
null in the families the credit reaches, and on a sentence about "evaluations scored around 30" that misdescribes her
own work; **Zwick** on what a PSID "laid off / fired" is from the employer's side, and on the 21 percent of White
fathers who are self-employed, cannot be laid off, and sit in the comparison group while their sons take over the
family business after 35 (the paper's own Appendix: the gradient of holding the father's exact job rises by
0.065\*\*\* after 35 for sons of self-employed fathers, 0.009 for others). The Zwick point is the most dangerous to the
headline and the cheapest to test (one to two days). The Hoynes points are the most dangerous to the paper's
credibility with a reader who knows the designs, and most of them are rewrites. The Kopczuk points add a wealth
dimension the paper half-opens and does not finish.

---

## 1. Wojciech Kopczuk

### K1. "Your wealth share is a functional-form choice, and your wealth measure has no top." (serious)

*In his voice.* "Table 2 says parental net worth carries three tenths of the IGE. That is the within-birth-year rank
of PSID net worth entered as a mediator in a regression of log earnings on log income: a rank among sons whose parents
are mostly in the bottom nine deciles of the national wealth distribution, in a survey with no high-wealth oversample
(unlike the SCF), with the SEO adding low-income families and the top trimmed by your \$150,000-of-1967 cap. Your
own appendix says asinh(net worth) gives 14.5 percent. Which is it, and which part of net worth is it: housing
equity, business and farm equity, or financial assets? I have spent twenty years arguing that wealth estimates
depend on these choices (Kopczuk 2015 JEP; Kopczuk and Saez 2004 [?])."

*Numbers in the paper.* `tab_split_main` col. 4: wealth 29.1\*\*\* (7.0), wage 20.5\*\*\*, rest 3.5 (16.4); EVIDENCE
11.48: asinh 14.5\*\*\* (0.056\*\*\*), rank 0.062\*\* at 25-29 to 0.127\*\*\* at 35-39; 2,828 sons born 1964+, median net
worth \$51,981 (2000 dollars). The measure is `IMP WEALTH W/ EQUITY`, mean over wealth waves at the son's 12-20
(`98.ParentalWealth.py`). The abstract says "the parents' wage and, where it is measured, their wealth carry most of
the IGE" (20.5 + 29.1 = 49.6 percent, i.e. half, not most).

*How damaging.* Moderate for the frame, high for credibility with this reader: the number he will remember is the
one in the abstract, and it is the larger of two defensible numbers.

*Answer (2 days; `98.ParentalWealth.py` extended).* (i) Report rank, asinh and log(net worth | > 0) with a
non-positive flag side by side, and write the range "15-29 percent" in the text. (ii) Split net worth into housing
equity, business/farm equity, and financial net worth (the PSID wealth modules record each component: home equity,
farm/business equity, stocks, checking/savings, other debts) and run the split with the three ranks; the interesting
outcome either way: if business/farm equity carries it, this is the family-firm channel of the Appendix (sons of
self-employed fathers converging on the father's job) and it belongs with Zwick's Z2-Z3; if housing carries it, it is
the Pfeffer-Killewald (2018) pattern. (iii) SRC-only and weighted versions in a footnote. Convincing: a stable
ordering (wage and wealth first, spells a few percent) across the three functional forms and the SRC sample; the
abstract then says "half" and gives the range.

### K2. "The earnings IGE is the wrong object for wealth transmission, and the family-income IGE's rise with age is unexplained." (serious)

*In his voice.* "The fellowship is about wealth and income inequality. Your outcome is the son's labor earnings,
which excludes the asset income, business profits and the spouse's earnings through which wealth is transmitted.
Your family-income IGE rises more than the earnings IGE (0.326 to 0.521 at 40-44 against 0.276 to 0.472); what is in
that difference, and does it grow with age because bequests and inter vivos gifts arrive when the son is 40-55? In
Danish registers the child-parent wealth rank correlation is present already in childhood and stable over the life
cycle, with a jump at the parent's death (Boserup, Kopczuk and Kreiner 2016 AER P&P, 2018 EJ) [? exact statements].
You have the son's net worth from 1984 and the parents' net worth for the 1964+ cohorts, and you use the son's wealth
once, in a footnote-level check (EVIDENCE 11.65: son's rank $-0.084$, $p = 0.104$)."

*How damaging.* Moderate for the paper as written (it is an earnings paper), high for its fit to the committee's
theme; and the analysis is cheap because the data are already built.

*Answer (4-5 days).* (a) *Decompose the family-income IGE's rise* (0.326 to 0.521) into the son's own earnings, the
spouse's earnings, asset income (interest, dividends, rent, the asset part of business income), and transfers, by
age band: the PSID family files have each piece (`80.WhatIsPassedOnRest.py` already reads them for the parents). The
Gelbach machinery applies with the son's income shares as mediators; or simply report the IGE of each component's
level (PPML) by band. Convincing result: if the extra rise is asset income or business income, the earnings IGE
understates what rich parents pass on in the forties and the paper should say so; if it is the spouse (assortative
mating), it connects to the daughters' partners (+0.677\*\*\* at 45-49). (b) *A wealth age profile next to the
earnings one*: the son's net-worth rank (within birth year and wave) on the parents' net-worth rank at the son's 12-20,
by the son's age band 25-55, on the 1964+ cohort; also the son's net-worth rank on log parental income on all sons
with the son's wealth (1984+). Convincing: a flat wealth rank-rank beside a rising earnings IGE sharpens "the rise is
the pay-off of skill at entry"; a rising one says the paper has found an age profile of wealth transmission too.
(c) *Inheritances and gifts*: each wealth wave asks whether the family received an inheritance or large gift in the
last five years and its value [? item names]; regress receipt and amount at the son's 35-55 on parental wealth rank
and log parental income, by band. One line: Danish or Norwegian registers would settle the bequest timing; the plan
does not depend on them. Charles and Hurst (2003, JPE) give the PSID age-adjusted wealth elasticity (about 0.37) as
the benchmark.

### K3. "Parental income is measured at different parental ages for different cohorts; your quartic in the parent's age does not fix a life-cycle bias on the parent side." (moderate)

*In his voice.* "Nybom and Stuhler (2016, 2017) show the bias from measuring the parent's income at the wrong age is
as large as the one from measuring the child's. Your parental window is the son's ages 13-19; for the 1951-56 births
it is 17-19 only, and the fathers of sons observed at 45-49 were measured in 1968-75 when the fathers were at
different ages than the fathers of sons observed at 25-29. A quartic in the parent's age controls the mean, not the
heterogeneity of profiles. Do you get the same rise with parental income measured at a fixed parental age?"

*How damaging.* Low to moderate: the rise holds within cohorts (0.162\*\*\*, 0.160\*\*, 0.142\*), with income-year FE
(0.149\*\*\*) and in the NLSY79 and NLSY97; but he will ask, and the check is a day.

*Answer (1-2 days; `113.BaselineProfile.py`).* Report the profile on sons whose father was 40-50 throughout the window
(a fixed parental age), and the profile with parental income measured at the father's ages 40-50 whenever that is
observed, regardless of the son's age (the PSID allows it for most fathers); show both give the same rise. Also report
how many parental years and sons the \$150,000 (1967 dollars; about \$1.4 million of 2023 [?]) cap removes, and the
profile without it. State that the earnings outcome keeps zeros in the PPML version (Mitnik et al.) and that the layoff
result holds there ($-0.523^{**}$, panel D of `tab_layoff_mechanism`).

### K4. "Attrition of 42 percent of White and 60 percent of Black sons by 45-49, corrected on observables." (moderate, mostly answered)

*In his voice.* "Your inverse-probability weights use parental income and income at 25-29. The sons who leave may
be those whose earnings growth was lowest. Show the same sons: the IGE at 25-29 among those who are still there at
45-49, against the full 25-29 IGE."

*How damaging.* Low: `appA` has the panel of sons observed in every band of 25-49 (0.272 to 0.478, trend 0.100\*\*\*);
the NLSY79 (far lower attrition) gives the same opening. He will accept this if it is in the main text rather than
the appendix.

*Answer (0.5 day, writing).* Move the two sentences (balanced-panel profile; NLSY79 bound) into Section 2's attrition
paragraph, with the retention rates, and add the 25-29 IGE of the eventual stayers against all sons at 25-29 (one
number, from `26.IGEByAge.py`'s output). Do not add more balanced-panel designs (memory rule).

### K5. "A Gelbach share is accounting; do not call it 'what parents pass on'." (moderate, wording)

*In his voice.* "Wealth, the wage and schooling are joint outcomes of the parents' ability and luck; the shares say
how much of the income gradient runs along each, not what is transmitted. Your Section 3 says 'The split is
accounting' and your title and abstract say 'what parents pass on'."

*Answer (0.5 day).* Keep the split as the frame, call it "the components of the IGE" in the abstract and section
titles, and reserve "passed on" for the layoff result, where the within-son design and the sons-daughters contrast at
least rule out a trait common to all children. See Section 5 for the sentences.

---

## 2. Hilary Hoynes

### H1. "The EITC paragraph claims a sign reversal from a $p = 0.052$ estimate, an insignificant change, an intent-to-treat on all families and a null in the families the credit reaches." (most damaging for her)

*In her voice.* "Per thousand dollars of maximum credit over the son's 13-18 you find $-0.016^{*}$ at 25-29 and
$-0.003$ at 40-44; the change is $+0.014$ with s.e. 0.019. The abstract says the EITC shows an evaluation scored at 30
'can get the sign of a childhood policy wrong'. It shows no such thing at that precision. Three further problems.
First, exposure is the schedule's maximum for the family's number of children; the credit reaches families with
earnings below about \$30,000-\$40,000, mostly single mothers; in your sons of mothers with at most twelve years of
schooling nothing is significant ($-0.011$, within son 0.026 with s.e. 0.017). Second, the EITC's first-order effect
is on the mother's employment (Eissa and Liebman 1996; Meyer and Rosenbaum 2001; Hoynes and Patel 2018); you have the
mother's hours in the teen window and you do not show whether exposure moved them in these families; an
intent-to-treat without a first stage is noise with a sign. Third, Bastian and Michelmore (2018) find *higher*
earnings at 18-27 per thousand dollars of exposure, not lower [? their earnings estimate; the abstract reports gains
in schooling, employment and earnings]; your 'later entry' reading does not reconcile with that, it contradicts it."

*How damaging.* High for the policy section and the abstract's last sentence; a reader who built these designs will
stop trusting the rest of the policy section. The fix is either a real design (4-5 days) or a demotion (half a day).

*Answer, option A (4-5 days; `101.EITCByAge.py` extended).* (i) *First stage*: mother's employment, hours and the
family's earned income at the son's 13-18 on exposure, same fixed effects; by predicted eligibility. (ii) *Eligibility
weighting*: predict eligibility from parental income at the son's 6-12 (before the window), the mother's schooling,
whether the father is present and the number of children; interact exposure with predicted eligibility (or run the
design on the predicted-eligible), report the implied treatment-on-the-treated by a Wald ratio, and show the age
profile there. (iii) *The 1993-96 expansion as a difference-in-differences* by number of children (two or more against
one; the Eissa-Hoynes / Hoynes-Patel design) with the son's outcome scored by band: the cleanest version of "the same
policy scored at different ages". (iv) *Daughters*: Bastian-Michelmore's effects are larger for daughters [?]; the PSID
has them. Convincing: a first stage on mothers' employment among the predicted-eligible, an earnings effect
concentrated there, and a monotone age profile; or a clean null, stated as such. *Option B (0.5 day)*: keep one
paragraph, state the point estimates with their $p$-values, write "the change is not significant; within the same sons
earnings grow faster with exposure ($0.029^{***}$)", delete "the sign" from abstract, introduction and conclusion, and
add the Bastian-Michelmore earnings estimate next to yours.

### H2. "Your sentence about evaluations 'scored around 30' misdescribes my work, and the later work goes to the fifties." (high for credibility, trivial to fix)

*In her voice.* "Section 8 says long-run evaluations 'measure adult earnings in the late twenties or early
thirties---Food Stamps (Hoynes, Schanzenbach and Almond 2016)'. We measured adult outcomes of cohorts born 1956-81 over
1999-2009, so into the forties and fifties, and the metabolic-syndrome and self-sufficiency indices are averaged over
all adult observations [? exact ages]; Bailey, Hoynes, Rossin-Slater and Walker (2024, REStud) link the Food Stamps
rollout to Census and ACS outcomes to the mid-fifties [? exact ages]. Your point---that the components growing after 40
are missed by designs that stop at 30---is right about Chetty et al. (2016) at 26 and Bastian-Michelmore at 18-27,
and it is supported, not contradicted, by our finding that effects appear in adult health and self-sufficiency decades
later."

*How damaging.* Low for the result, high for the reading: a committee member who finds her own paper misdescribed
in the first policy paragraph reads the rest looking for errors.

*Answer (0.5 day, writing).* Rewrite the paragraph: name the designs that stop before 35 (Chetty-Hendren-Katz 2016;
Bastian-Michelmore 2018; Jackson-Johnson-Persico 2016 to about 30 [?]; Chetty et al. 2020 at 31-37), cite HSA 2016 and
Bailey et al. 2024 as the designs that reach the forties and fifties and find effects there, and state the paper's
point as "the age profile of a policy's effect is itself an object to estimate; here is one profile (the layoff) that
is zero at 30 and large at 45, and one (the EITC) whose point estimate changes sign." Cite Hendren and Sprung-Keyser
(2020) for the lifetime projections from early ages as the place where the profile matters for MVPFs.

### H3. "The UI tests have no power, the state-split has no state fixed effects, and the simulated benefit is not the state's formula." (serious, partly conceded)

*In her voice.* "The split by state generosity (panel A of `tab_ui_stability`) compares sons across states without
state fixed effects: generous states are the Northeast, Midwest and West Coast. The interactions (panel B) have state
fixed effects and within-state-and-cohort variation of 0.041; the layoff interaction is 0.021 ($p = 0.19$). The
simulated replacement rate is 'half the weekly wage between the minimum and the maximum', but states use high-quarter
and base-period formulas, dependants' allowances (your own `12b` codes the DA flag), waiting weeks, and from
1979/1987 benefits were taxed [?]. The weeks design approximates federal tiers. Your minimum detectable effects (17
points of the IGE against a share of 13; 0.52 against a cost of 0.24; 1.1 for weeks) say the designs exclude only
insurance effects larger than the cost itself. Meanwhile the one direct measure you have---whether the father
received UI---gives $-1.014^{**}$ for layoffs with UI against $-0.211$ without ($p = 0.095$), which you read as a
layoff/firing separator. Does the *amount* received, relative to the earnings lost, matter?"

*How damaging.* Moderate: the paper already says "not shown to weaken ... too imprecise to rule it out". She will
want either a sharper test or one sentence.

*Answer (4 days; `99`, `102`, `91` extended).* (i) *Realised replacement*: the PSID records the head's unemployment
compensation received each year (all waves) [? item continuity]; for each teen layoff year compute benefits received
over the fall in the father's labor income (or over his prior-year earnings); split the layoff share by terciles of the
realised replacement rate and by UI received (yes/no), within son; placebo with closures. (ii) *One pooled insurance
index* (simulated replacement rate times weeks available, at the father's wage, within state and cohort) instead of
three underpowered designs; report one interaction and one MDE. (iii) Code the actual benefit formula for the ten
largest PSID states (high-quarter fraction, minimum, maximum, DA) from the Significant Provisions already transcribed
in `12b`, and show the simulated rate is robust. (iv) State in the policy section that UI as designed does not address
the costly layoffs anyway: a waiting week and partial-benefit rules mean a repeated layoff with fewer than 500 hours of
unemployment draws little (the paper's own point, made explicit). Convincing: an interaction with the realised
replacement rate of the right sign at $p < 0.05$ with a closure placebo at zero; or a precise null, in one sentence.

### H4. "Layoffs in bad times cost the son half as much; in the father's own earnings they cost twice as much. Reconcile, and show each recession." (moderate)

*In her voice.* "Davis and von Wachter (2011) find displaced workers lose about twice as much when displaced in a
recession; your 'bad-times' layoffs cost the son about half ($-0.675^{**}$ against $-1.400^{***}$; within son $-0.166$
against $-0.408^{***}$, $p = 0.26$ for equality). That is a striking contrast for your 'not the income' reading, and you
do not draw it. Also, recessions do not fall on the same men (Hoynes, Miller and Schaller 2012): the 1980-82 layoffs
were manufacturing men in the Midwest; the 2008-09 ones were construction and finance. Which recessions carry your
bad-times result, with how many treated sons in each? Your 1976-83 regime cell has fewer than 30 treated sons at
45-49."

*Answer (2 days; `104.FatherPathRecession.py` extended).* (i) The father's own event-study loss (EVIDENCE 11.57:
$-0.198^{***}$ at 0, $-0.138^{**}$ at +6) split by bad-times and other layoffs: if bad-times layoffs cost the father
more and the son less, that is the paper's strongest evidence that the son's cost is not the father's income loss;
write it as such. (ii) A table of the layoff share by recession window (1974-75, 1980-82, 1990-91, 2001, 2008-09) and
the son's band change and within-son slope for each, with treated counts; sons whose teens fell in 2008-13 are at
25-34 only, say so. Convincing: no single recession carries the result; the father's loss and the son's cost move
in opposite directions across bad and good times.

### H5. "Your sample excludes the safety net's population, and your transfer sentence is not a test of transfer dollars." (moderate)

*In her voice.* "The layoff analysis requires the father present (3,386 of 4,770 sons; 135 treated at 45-49).
Single-mother families, the main recipients of AFDC, Food Stamps and the EITC, are out of it. The Black earnings IGE
is 60 percent family structure. Section 8 says 'Years on AFDC or TANF carry 6.6 percent ... the transfer dollars, at
equal income, do not show': at equal total income a higher transfer share is lower earnings and a different family;
holding total income fixed is not a test of what transfer dollars do. And the mother's own layoffs---the PSID asks
female heads the same job-end question---are never used."

*Answer (3-4 days).* (i) *Mother-headed families*: the female head's job ends (`19`'s codes apply to female heads; the
docstring says wives' items are unused, but heads of either sex are asked) at the child's 13-19, on the child's
earnings by band and within child; treated counts will be small, so report the estimate with its interval and stop.
(ii) *AFDC maximum benefit* (UKCPR state x year x family size, public; already read by `61.PolicySchedules.py`'s
calendar) averaged over 12-18 as a second safety-net moderator in the H3 design, with the same MDE discipline.
(iii) Rewrite the transfer sentence: "AFDC/TANF receipt during the son's teens carries 6.6\*\*\* percent of the IGE at
equal income; the split cannot separate what brought the family onto welfare from what welfare did, and holding total
income fixed does not test the transfer dollars." One line: county-level Food Stamps rollout (1961-75) would give an
instrument for the safety net in the father's layoff years, but it needs the PSID restricted geocodes; not pursued.

---

## 3. Eric Zwick

### Z1. "What is a 'layoff' from the employer's side? Your costly layoffs look like temporary layoffs with recall, which are a property of the job, not the father." (serious; changes the reading)

*In his voice.* "The PSID code is 'laid off, fired', one code in every wave. In the 1970s and 1980s most layoffs into
unemployment in manufacturing and construction were temporary layoffs with recall to the same employer (Feldstein
1976; Katz and Meyer 1990; Fujita and Moscarini 2017 put recalls at about 40 percent of separations into unemployment
[?]). Now look at which layoffs carry your cost: repeated ones ($-0.268^{**}$ against 0.295 for one), with a small fall
in family income ($-0.473^{***}$ against $-0.096$), fewer than 500 hours unemployed ($-0.338^{***}$ against 0.225), UI
received ($-1.014^{**}$), in fathers whose employment share is unchanged at the son's 20-24 (0.020) but who are 'laid
off again' ($+0.132^{***}$). That is the signature of a recall-layoff job: seasonal or cyclical, unionised, in durable
manufacturing, construction, mining. Then 'unstable employment of the father' is 'a father in a recall-layoff job',
and the thing passed on is the father's industry and job type, not his instability. Your temporary-layoff split
(employment status 'temporarily laid off' at the interview, 1983+, 58 percent of layoff years) is uninformative
($p = 0.49$), but that is the status at the interview date, not whether he went back."

*How damaging.* Serious for the interpretation and the policy section ("the margin is the stability of the father's
employment"); not for the fact. It also offers the paper something: if the cost is in recall-layoff jobs, the
father's industry gives a cleaner comparison group than "fathers never laid off".

*Answer (3-4 days; `91.LayoffSelection.py` and `88` extended).* (i) *Recall versus permanent separation*: a layoff
year is a recall if the father reports the same employer (PSID months/years with present employer do not reset; the
2003+ roster carries employer identifiers within a wave) at the next interview, permanent otherwise; split the teen
layoff share into recall, permanent and unknown parts; within-son slopes and the test of equality. (ii) *Within the
father's job*: add the father's detailed industry group (33 groups, `32.IndustryCareers.py`'s mapping) and occupation
group x age, and his union membership (the PSID asks heads whether they belong to a union in most waves from the late
1970s [? years]) x age, to the within-son design; report the cost within father's industry. (iii) *By sector*:
durable manufacturing, construction/mining, services, public, with treated counts. Convincing: if the cost survives
within father's industry and in permanent separations, the "father" reading stands and the paper says so; if it sits
in recall layoffs in cyclical industries, retitle the mechanism ("a father in a recall-layoff job") and the policy
margin becomes the job, not the man. Either answer is a result. One line: LEHD employer histories would separate recall
from permanent separation exactly; not available to the PI.

### Z2. "Self-employed fathers cannot be laid off; they are in your comparison group, and their sons' earnings rise after 35 as they take over the business." (serious; cheapest test in this memo)

*In his voice.* "Twenty-one percent of White fathers and 8 percent of Black fathers are self-employed in at least
half their interviews (your `tab_fatherse`). A business owner reports no 'laid off / fired'; if his business fails he
reports code 1, 'company folded / went out of business', which you count as a plant closure. So your never-laid-off
comparison group contains the owners, and your closure group contains failed owners. Your own Appendix shows that
among sons of self-employed fathers the gradient of holding the father's exact occupation-industry cell rises by
0.065\*\*\* after 35 (0.009 for other sons): richer sons take over the business in their forties. A comparison group
whose earnings rise late for that reason manufactures a late-appearing relative 'cost' for sons of laid-off employee
fathers. The within-son design does not remove it, because the owners' sons' profiles bend upward within son too."

*How damaging.* Potentially serious for the headline's size (the cost may shrink once owners' sons are out of the
control group), not for its existence (the sons-daughters contrast and the recall/permanent split do not run through
this). Cheap to test, so it must be done before anything else.

*Answer (1-2 days; `88`, `91`, `107` with the self-employment code of `43.FatherJobSelfEmployment.py`).* (i) Drop sons
of self-employed fathers (half or more of valid interviews from 1976; for the 1968-75 fathers use the class-of-worker
item of those waves [?]) and re-estimate the band profile, the change, the within-son slope and the sons-daughters
difference; (ii) alternatively add father self-employed x age (and x age x son's own self-employment) to the within-son
design; (iii) drop self-employed fathers from the closure contrast, since code 1 cannot be split into "employer went
out of business" and "own business folded" (the PSID bundles them in one code; say so in the paper). Convincing: a
layoff profile of the same size on employee fathers' sons (expected if the treated are employees anyway and the owners
are a small share of the control group). If the cost falls by a third or more, the paper has learned that part of
"the layoff's cost" was "no business to inherit", which is a finding about wealth transmission that Kopczuk and Zwick
would both value.

### Z3. "Is business income in earnings? For sons who become owners in their forties, your earnings IGE and your wage decomposition measure the wrong thing." (moderate)

*In his voice.* "Smith, Yagan, Zidar and Zwick (2019) show that most pass-through business income is the owner's
labor income. Your 'earnings' is PSID head labor income, which before 1994 bundled the labor part of business income
and from 1994 adds it back (`1.PSID.py`); the asset part is in family income only; the self-employed son's 'hourly
wage' is earnings over hours. Sons of rich parents are more likely to own a business in their forties. Then the rise of
the earnings IGE after 40 is partly the earnings of owners whose income is split arbitrarily into labor and capital
parts, and 'the cost is in the wage within occupation' is measured on a wage that is not a wage for them."

*Answer (2-3 days).* (i) The share of son-years self-employed by band and parental-income tercile; (ii) the IGE
profile and the layoff profile on employee son-years only, and with earnings plus the asset part of business income as
the outcome; (iii) a "business income" component on the parents' side in the split (the family files separate the
head's business income into labor and asset parts, and farm income); the row "labor income beyond wage and hours" (8.9,
s.e. 7.5) is where it hides now. Convincing: the profile and the layoff cost hold among employee sons; if the
family-income rise is business income, say so (it links to K2).

### Z4. "Your industry-shock instrument fails because PSID 'laid off' is not what a demand shock produces; the closure measure is small-firm failure; and the positive closure effect on the son's wage is composition." (moderate)

*In his voice.* "The first stage of national sector declines on the layoff share is 0.030\* with $F = 2.9$, and on
the unemployment share $0.080^{**}$: demand shocks make PSID fathers unemployed without a 'laid off' report, or push
them into code 1. Code 1 is 'company folded / changed hands / moved out of town / employer died / went out of
business', which is a small-employer event as much as a plant closure. And at equal income a closure *raises* the
son's wage ($0.021^{**}$); you read this as Gibbons-Katz; I read it as fathers in closing plants being in high-wage
unionised durable manufacturing. Show the closure and layoff effects by the father's industry and union status."

*Answer (2 days, overlaps Z1(ii)).* Closure and layoff shares by the father's sector and union status; the closure
wage effect within industry; a sentence in Section 5 that the demand-shock design identifies the cost of the father's
demand-driven unemployment, not of a layoff, and that the PSID's code 1 is not a plant-closure measure in the Jacobson-
LaLonde-Sullivan sense. Public alternatives for the first stage (state x 3-digit industry employment from QCEW/CBP;
BLS Mass Layoff Statistics 1995-2013 at state x industry) can be tried in a day and are likely still weak; report the
attempt in a footnote if so.

### Z5. "The EITC is not in PSID family income, so it is not 'part of parental income'." (minor, factual)

*In his voice.* "PSID total family income is pre-tax money income including cash transfers; a refundable credit paid
through the tax system is not in it. Your script's note that 'lyp is not controlled (the credit is part of parental
income)' is wrong, and the specification with log parental income added ($-0.0159^{**}$) is the one to report."

*Answer (0.1 day).* Report the column with log parental income as the main one and fix the comment in `101`.

---

## 4. Ranked actions (all public data; quick wins marked QW)

| rank | action | serves | days | QW |
|---|---|---|---|---|
| 1 | **Z2** Drop / control self-employed fathers (father SE x age) in the layoff profile, within-son slope, sons-daughters difference and closure contrast; say code 1 bundles own-business failures | Zwick; also the selection objection of earlier reviews | 1-2 | yes |
| 2 | **Z1** Recall vs permanent layoffs; father's industry group, occupation group and union x age in the within-son design; cost by sector | Zwick; the mechanism and the policy margin | 3-4 | |
| 3 | **H2 + Z5 + wording** Rewrite the age-of-scoring paragraph (HSA 2016 and Bailey et al. 2024 reach the forties and fifties); EITC with log parental income; the sentences in Section 5 below | Hoynes, Zwick, Kopczuk | 1 | yes |
| 4 | **K1 (+Z6)** Wealth share as rank / asinh / log; net worth split into housing, business-farm, financial; SRC-only; "half", range 15-29 | Kopczuk, Zwick | 2 | yes |
| 5 | **K2** Family-income IGE rise decomposed (own earnings, spouse, asset, business, transfers); son's wealth rank on parents' wealth rank by age band; inheritances/gifts at 35-55 | Kopczuk (the committee's theme) | 4-5 | |
| 6 | **H1** EITC: first stage on the mother's employment; eligibility-weighted design and TOT; 1993-96 DiD by number of children scored by age; daughters; the Bastian-Michelmore earnings contrast stated. Or option B (demote, 0.5 day) | Hoynes | 4-5 (or 0.5) | |
| 7 | **Z3** Self-employed sons: IGE and layoff profiles on employee son-years; earnings + asset part of business income; a business-income component for parents | Zwick, Kopczuk | 2-3 | |
| 8 | **H4** Father's own loss vs son's cost by bad/good times (the Davis-von Wachter contrast); recession-by-recession table with treated counts | Hoynes | 2 | |
| 9 | **H3** Realised UI replacement from benefits received; one pooled insurance index with one MDE; formula for the ten largest states; the "UI does not reach churn layoffs" sentence | Hoynes | 4 | |
| 10 | **H5** Female heads' layoffs by the child's age; AFDC maximum benefit as a moderator; the transfer sentence rewritten | Hoynes | 3-4 | |
| 11 | **K3 + K4** Profile with parental income at a fixed parental age; the cap's effect; attrition sentences moved to the main text with the stayers' 25-29 IGE | Kopczuk | 1-2 | yes |

Total about 30 working days; items 1, 3, 4 and 11 (five to six days) remove the critiques most likely to be voiced
first. Items 1 and 2 should run before any rewrite of Sections 5 and 8, because their answer may rename the mechanism.
Order for one week: 1 (day 1-2), 3 (day 2), 4 (day 3-4), 11 (day 5); then 2 and 5.

---

## 5. What not to claim: sentences a member would object to, and rewording

| where | current sentence | who objects, why | reword |
|---|---|---|---|
| abstract, last sentence | "the EITC shows that an evaluation scored at 30 can get the sign of a childhood policy wrong." | Hoynes: $-0.016^{*}$ ($p = 0.052$) vs $-0.003$, change $+0.014$ ($p = 0.47$); null where the credit binds | "scored at 25-29 the EITC's point estimate is negative ($p = 0.05$) and at 40-44 zero; the change is not significant, but within the same sons earnings grow faster with exposure ($p = 0.002$)." Or drop from the abstract. |
| intro, policy paragraph | "The EITC shows it: a family's maximum credit during the son's teens goes with lower earnings at 25--29 and none at 40--44, because the same sons' earnings grow faster with it." | Hoynes: "shows", "because"; intent-to-treat; BM 2018 find higher earnings | "The EITC illustrates it: ... the within-son growth is significant, the change across bands is not, and the estimates are intent to treat on all families." |
| Section 8, age of scoring | "Long-run evaluations of childhood policies measure adult earnings in the late twenties or early thirties---Food Stamps \citep{hoynes2016long}, ..." | Hoynes: HSA 2016 and Bailey et al. 2024 reach the forties and fifties [?] | "Several long-run evaluations stop before 35 (MTO at 26; the EITC at 18-27; Chetty et al. 2020 at 31-37); those that reach the forties and fifties (Hoynes, Schanzenbach and Almond 2016; Bailey et al. 2024) find effects there." |
| Section 8 | "A credit that keeps teenagers in school and delays their entry into work looks costly at 25 and pays off later; \citet{bastian2018long} find more schooling and employment at 18--27." | Hoynes: BM also find higher earnings at 18-27 [?]; the reconciliation is missing | State BM's earnings estimate next to yours and say the two differ in sample and age; offer "later entry" as one reading, not the reading. |
| abstract, intro, Section 8, conclusion | "Unemployment insurance at the father's wage does not weaken the sons' cost" / "Insurance does not weaken the cost" / "insurance ... does not weaken it" | Hoynes: MDEs exceed the cost; the designs exclude only effects larger than the cost | "is not shown to weaken the cost; the designs exclude only insurance effects larger than the cost itself." (Section 8 already says this; the abstract, intro and conclusion do not.) |
| intro | "A plant closure ... carries no cost at any age." / abstract "Plant closures and national declines of the father's industry carry no cost" | Zwick, Kopczuk: closure change 0.000 (0.258), interval allows 59 percent of the layoff's; code 1 bundles small-employer and own-business failures | "carries no detectable cost; the interval allows a closure cost up to three fifths of the layoff's, and the PSID's closure code bundles plant closures with employers going out of business." |
| Section 5 opening; conclusion | "the answer is unstable employment rather than lost income" / "The cost of a father's layoffs is not the income they take" | Zwick: the costly layoffs have the recall-layoff signature; the job, not the man, may be what is unstable | "the cost follows repeated layoffs with small income losses, in fathers who are laid off again---unstable employment, whether the father's or his job's (Section 5 tests recall against permanent separations)." |
| abstract; Section 3 | "the parents' wage and, where it is measured, their wealth carry most of the IGE" / "their net worth ... carries three tenths (29.1\%)" | Kopczuk: 20.5 + 29.1 = half; rank 29.1 vs asinh 14.5 | "about half" and "between 15 and 29 percent depending on how net worth enters (rank or asinh)". |
| Section 3 frame, title of Table 2, abstract | "What parents pass on" for the Gelbach split | Kopczuk: accounting, not transmission | "The components of the IGE"; keep "passed on" for the layoff result. |
| Section 8, Transfers | "Receipt marks the families whose sons do worse at equal income; the transfer dollars, at equal income, do not show." | Hoynes: at equal total income a higher transfer share is lower earnings; not a test of dollars | "AFDC/TANF receipt carries 6.6 percent at equal income; the split cannot separate what brought the family onto welfare from what welfare did, and holding total income fixed does not test the transfer dollars." |
| Section 8, UI subsection | "the churn of short jobs and repeated layoffs that unemployment insurance, built to replace income during a spell, does not address" | Hoynes: UI does cover short spells after a waiting week; partial benefits exist | "that unemployment insurance, with its waiting week and partial-benefit rules, replaces little of" (and show the realised replacement rate for these layoffs, H3). |
| Section 2, data | "Parental income is the mean of the parental household's family income" | Kopczuk, Zwick: say what it is | add "pre-tax money income including cash transfers and the asset part of business income, excluding tax credits and in-kind benefits". |
| `101.EITCByAge.py` docstring | "lyp is not controlled (the credit is part of parental income)" | Zwick, Hoynes: it is not | "lyp is controlled in the main column (the credit is not in PSID family income)". |
| Section 4, by race | "It is not shown that a layoff costs Black sons less." | fine; keep, but add the counts (37 treated at 45-49) in the sentence, not the footnote | — |

---

## 6. Where restricted data would settle a question (one line each; the plan does not depend on them)

- Recall vs permanent separation and the employer's size: LEHD employer histories (not available to the PI).
- Bequest timing and the son's wealth at the parent's death: Danish/Norwegian registers (the Boserup-Kopczuk-Kreiner design).
- A safety-net instrument in the father's layoff years: county Food Stamps rollout 1961-75 with the PSID restricted geocodes.
- EITC treatment at the family level: tax records; the PSID public file gives only the schedule.

## 7. Literature flags to check before any of this enters the paper

- Boserup, Kopczuk and Kreiner (2016 AER P&P; 2018 EJ): the statements about the wealth rank correlation's stability over the child's life cycle and the jump at bequest [?].
- Bastian and Michelmore (2018 JOLE): the earnings effect at 18-27 per \$1,000 and its sign; effects by sex [?].
- Hoynes, Schanzenbach and Almond (2016 AER): the ages at which adult outcomes are measured (cohorts 1956-81 observed 1999-2009) [?]; Bailey, Hoynes, Rossin-Slater and Walker (2024 REStud): outcome ages [?].
- Fujita and Moscarini (2017 AER): the recall share of separations into unemployment [?]; Katz and Meyer (1990 QJE) [?].
- Davis and von Wachter (2011 Brookings): the recession multiplier on displaced workers' losses [?].
- Smith, Yagan, Zidar and Zwick (2019 QJE): the share of pass-through income that is owners' labor income [?].
- Charles and Hurst (2003 JPE): the PSID age-adjusted wealth elasticity [?].
- PSID items: head's union membership years; unemployment compensation received (continuity across waves); inheritance/gift questions in the wealth modules; class of worker in 1968-75 [?].
