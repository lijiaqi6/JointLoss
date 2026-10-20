# Paper B, round 2: a QJE referee's assessment after the round-1 additions (Fable, 2026-10-20)

Read in full: `proposals/fable_top5_distance_paperB_20261020.md` (my round 1); `paperB_age_profile/main.tex`, sec1,
sec3_data, sec3_ageprofile, sec4_passedon, sec5_skill, sec6_stability, sec7_policy, sec8_conclusion, appC_entry, the
openings of appA/appB/appD_race; tables tab_passed_on, tab_four_by_four, tab_layoff_age, tab_layoff_fe,
tab_layoff_selection, tab_layoff_exog, tab_split_robust, tab_age_period, tab_eitc_age, tab_shea_spell,
tab_ui_stability, tab_father_disp_age, tab_ige_sons; `EVIDENCE.md` rows 11.28-11.51; `output/layoff_selection.md`,
`layoff_daughters.md`, `layoff_industry_shocks.md`, `nlsy97_afqt.md`, `pooled_rise_checks.md`,
`split_measurement_error.md`, `rest_identification.md`, `parental_wealth.md`, `simulated_replacement_rate.md`,
`eitc_by_age.md`, `ui_duration_weeks.md`, `layoff_cost_by_age.md`; the docstrings of scripts 91-93, 96, 98, 99, 101,
102. Nothing was run; no existing file was touched. Every number below is quoted from those files; where I derive a
number I say so. Substance only, as asked.

---

## 1. Verdict

**At the QJE, now: reject, with a letter that says what a resubmission would need. Not a major revision, because I
cannot name the revision that would close the gap with the data the authors have.** The paper moved a long way since
round 1: eight of my ten additions were run honestly (A1-A4, A6, B1-B3, C1-C2, D1-D2, F), the reporting gaps are
closed (treated counts, the closure contrast on common draws, the timing tests, leave-one-cohort-out), and three new
facts were found (daughters of the same fathers gain with age; parental wealth carries 29 percent of the IGE for the
cohorts where it is measured; the costly layoffs are the repeated, small-loss, short-unemployment ones). But the
first referee question of round 1, *is the delayed cost of a father's layoff an effect of the layoff or the rising
pay-off of what layoffs select on*, still has no answer, because the one design that could answer it (A1, demand
shocks to the father's industry) has a first stage on layoffs of 0.030\* with $F = 2.9$ (Table `tab_layoff_exog`),
and the second data set (A5) is deferred. Worse, the additions surfaced a fragility the paper now carries in a
footnote: on the 2,043 sons whose teens fall in 1976 and later, the within-son layoff slope is 0.040 (s.e. 0.113)
(`output/simulated_replacement_rate.md`; sec7_policy footnote), against $-0.236^{**}$ in the full sample. The headline
is therefore carried by sons born before about 1963, whose fathers' job-end reasons were recorded under the 1968-75
question net. Until that is understood, the paper's mechanism claim rests on roughly 2,600 sons of one era and 135
treated sons at 45-49. For JPE or REStud I would say major revision; for AEJ: Applied or JOLE the paper is
publishable now with the cuts in Section 5 below. The distance to the QJE is unchanged in kind (an identified
layoff), and the additions have made the fact more honest, not more causal.

---

## 2. The contribution as an editor would state it now

Using the PSID, the paper shows that the parental components carrying the intergenerational elasticity of earnings
change with the son's age: the parents' wage, the father's schooling and (where measured) their wealth show from the
son's mid-thirties, through skill at entry that pays more as human capital accumulates on the job (replicated across
the NLSY79 and NLSY97); a father's layoff during the son's childhood shows only after 40, in the son's hourly wage,
while plant closures and declines of the father's industry show at no age; the son's own non-employment carries the
IGE when he is young and fades. The delayed layoff cost is the only candidate for a mechanism and the only result a
top-5 referee will spend time on. The paper is **not** organised around it: the title, abstract and Section 4 are
built on the split (headline 1, which the paper itself calls accounting), the layoff is Section 6, and Section 7
(policy) reports four nulls and a marginal EITC coefficient as if they were findings. The organisation still does
not match the contribution, as in round 1.

---

## 3. What round 1's additions settled, did not settle, and changed

### Settled (the paper can now state these)

- **The numbers that were missing (A6).** Treated father-present sons 383 at 25-29 and 135 at 45-49 (White 265 /
  98, Black 118 / 37; Table `tab_layoff_selection`, panel A). Layoff minus closure change, on common draws,
  $-0.914^{***}$ (0.326; $p = 0.005$); White $-0.962^{***}$ ($p = 0.004$). Leave-one-five-year-cohort-out keeps the
  band change between $-0.82^{***}$ and $-0.99^{***}$ and the within-son slope between $-0.21^{*}$ and
  $-0.26^{***}$ in all eleven drops (`layoff_selection.md`, A6d). Parental income at the son's 20-26 changes nothing
  ($-0.236^{**} \to -0.232^{**}$).
- **"Only the teens" is withdrawn, correctly.** Within son, the three windows give $-0.081$ (0.109) at 6-12,
  $-0.322^{***}$ (0.124) at 13-19, 0.037 (0.102) at 20-26; 13-19 minus 6-12 is $-0.241$ (0.180; $p = 0.18$), 13-19
  minus 20-26 is $-0.359^{**}$ (0.177; $p = 0.043$), joint equality $\chi^2(2) = 4.12$ ($p = 0.128$), on 2,171 sons.
  The claim is now "childhood, not after 20", which the data support.
- **Age, not period (D1, D2).** The pooled rise of the earnings IGE from 25-29 to 45-49 is $0.216^{***}$ for sons
  born 1951-64, $0.147^{*}$ for 1965-79, $0.165^{*}$ (to 40-44) for 1980-89, $0.192^{***}$ with income-year fixed
  effects and $0.240^{***}$ in the 1990-2010 window (Table `tab_age_period`, panel A). In the NLSY97 the son's AFQT
  contribution rises from $0.033^{***}$ at 25-29 to $0.054^{***}$ at 40-44 (opening $0.021^{**}$, $p = 0.027$), a factor
  of 1.64 against 1.70 in the NLSY79 over the same ages (panel B). Objection 5 of round 1 is answered.
- **The rest is not an identity artefact (B2).** Labour income and the three income shares predict $R^2 = 0.671$ of
  log parental income, the identity term alone 0.501, all components and resources 0.834; without the income-defined
  resources the rest is $53.0^{***}$ against $47.6^{***}$ (Table `tab_split_robust`, panel B).
- **Measurement error attenuates the wage share by about a quarter (B1).** Half A instrumented by half B: wage
  share $28.0^{***} \to 36.8^{***}$, hours $3.8 \to 5.2$, spells $4.2^{**} \to 2.7$ (n.s.), rest $64.0^{***} \to
  55.2^{***}$ (panel A). The correction is a lower bound (serially correlated transitory error survives), and for
  spells the halves are different events, as the paper says.
- **The UI "headline" is dead and the paper says so.** The split by state generosity is $-4.1$ points (6.0;
  $p = 0.496$); the simulated replacement rate at the father's wage (mean 0.342, s.d. 0.144, cap binding in 75
  percent of window years, 2,043 sons, 278 treated) gives layoff $\times$ rr $\times$ age $-0.218^{*}$ (0.129) that
  becomes $-0.038$ (0.187) once layoff $\times$ father's wage is held fixed; weeks available (mean 34.3, s.d. 10.0,
  1,569 sons, 209 treated) gives $-0.191$ (0.395) (Table `tab_layoff_exog`, panel C). Conclusion in sec7: "not shown to
  weaken ... too imprecise to rule it out". Correct, and it means Section 7 has no UI finding.

### Not settled

- **Selection (Objection 1).** A1 cannot test the layoff cost: first stage on the layoff share $0.030^{*}$ (0.017),
  $F = 2.9$; on the unemployment share $0.080^{**}$; on closures $-0.006$; 2SLS of layoff $\times$ age 10.3 (26.8)
  (`layoff_industry_shocks.md`). The reduced form within son is $+0.143^{**}$ (0.063) with placebos $-0.058$ and
  0.093, and the band change $+0.241$ (0.203). What the design shows is that demand-driven unemployment of the father
  is not passed on; it says nothing about the selected layoffs. A2 (timing as the control group, 547 sons: T 256, E
  164, L 127) is the paper's best answer: T $\times$ age $-0.157^{**}$ (0.068; $p = 0.021$), E $\times$ age $-0.110^{*}$
  (0.063), T minus E $-0.047$ ($p = 0.45$), T's band profile $-0.329^{**}$ at 45-49; Black T 0.062, E 0.072. It removes
  what all ever-laid-off fathers share; it does not remove what distinguishes fathers laid off while a child is at
  home from fathers laid off when the son is 20-26 (father's age, the father's career stage, whether the layoff is
  observed in the son's own family unit). The paper's footnote concedes this. A3's splits point the right way but at
  $p = 0.079$ (income loss), 0.064 (unemployment duration), 0.145 (repeat) and 0.095 (UI receipt), and two of them
  pull against each other (below).
- **A second data set at 45-49 (A5).** Deferred (SOEP contract; BHPS has 18 / 5 father-redundant sons at 40-44 /
  45-49). The paper still rests on one data set for its central fact.

### Changed (the results that alter the paper's reading)

- **Daughters show the opposite sign (A4).** Within person, a father's teen layoff raises the daughter's wage growth
  by $0.168^{**}$ (0.075) a decade; band change in the wage $+0.387^{*}$ (0.214), in family income $+0.560^{**}$
  (0.259), with $+0.599^{**}$ at 45-49; earnings 0.439 (0.285), within 0.200 (0.130); 145 treated daughters at 45-49
  (`layoff_daughters.md`). In the same reduced specification the sons' within-person wage slope is $-0.086$ (0.096)
  and the earnings slope $-0.180^{*}$ (0.108); only the sons' band changes ($-0.538^{**}$ wage, $-0.855^{***}$ earnings)
  are precise. The paper uses this as evidence against a trait passed to all children. A referee reads it the other
  way as well: the "layoff" variable moves the whole family's later-life outcomes in sex-specific directions,
  including the daughters' *family* income, which is mostly the husband's earnings. That is the signature of the
  comparison group differing in something that pays off late for sons and not for daughters (the father's
  occupation, union status, a job passed from father to son, assortative mating), or of selection into the wage
  sample for daughters. It is a new fact, unexplained, and it makes the "cost of unstable employment" reading less
  secure, not more.
- **Wealth changes headline 1, in a way the paper under-reports.** On the 2,828 sons born 1964 and later, the rest
  of the split is already $11.4$ (s.e. 16.6, n.s.) *before* wealth enters; with the within-birth-year wealth rank it is
  3.5, and wealth carries $29.1^{***}$ (7.0), rising from $0.062^{**}$ at 25-29 to $0.127^{***}$ at 35-39; asinh
  net worth carries $14.5^{***}$ (`parental_wealth.md`). Wealth's share comes from assets ($6.1 \to -4.5$), the wage
  ($25.6 \to 20.5$) and the small rest, not from "most of the rest" of the full-sample 47.6 percent. So the full-sample
  "half is money" is a property of the older cohorts (sons born 1950-63), whose parents are measured in the 1968-75
  family files. The honest headline 1 is: *in the cohorts where the parents are fully measured, the parents' wage,
  wealth, schooling and spells account for the IGE and nothing is left; in the older cohorts half is unmeasured.*
  That is stronger than the current sentence and it is what the data say.
- **The EITC (F) is a marginal result the paper reads as a sign reversal.** Per thousand dollars of maximum credit
  over the son's 13-18: $-0.0160^{*}$ (0.0083; $p = 0.052$) at 25-29, $-0.0025$ (0.0185) at 40-44, change $+0.0136$
  (0.0186, n.s.), within son $+0.0294^{***}$ (0.0095) (Table `tab_eitc_age`). Exposure is a year $\times$
  number-of-children schedule applied to all sons (mean 13.2, s.d. 6.9, rising from 6.6 for the 1960-64 births to
  21.4 for 1995-99), and in the families the credit reaches (mother with at most 12 years of schooling) nothing is
  significant ($-0.0112$ at 25-29, within son 0.0256, s.e. 0.0171). The intro's "The EITC shows it" is not supported
  at the precision shown.
- **The costly layoffs are the "churn" layoffs**: small income loss $-0.473^{***}$ (0.144) against large $-0.096$
  (0.132); short unemployment $-0.338^{***}$ against long 0.225 (0.265); two or more teen layoff years $-0.268^{**}$
  (0.106) against one 0.295 (0.378); UI received $-1.014^{**}$ (0.484) against none $-0.211$ (0.255) (panel D). Three
  things follow that the paper does not draw out. (i) The repeat split says the father's *persistent* layoff propensity
  carries the cost, while the half-window IV says the persistent propensity carries *less* of the spells share than
  the events do ($4.2^{**} \to 2.7$); these are different objects (a slope versus a level share) but a referee will put
  them side by side. (ii) Fired workers are in general ineligible for UI, so the UI-received split is the closest the
  PSID comes to separating layoffs from firings, and the cost sits in the UI-received, i.e. layoff, part: that is
  evidence *for* the paper and it is in the table but not in the text. (iii) A father who loses little income and is
  quickly re-employed, repeatedly, is a job-churner; the paper has no account of how a father's churn in the son's
  teens lowers the son's hourly wage at 45 and not at 30.

---

## 4. Remaining substantive objections, ranked by how fatal they are

### Objection 1 (fatal for the mechanism claim, now sharper): the layoff cost is not identified, and it is concentrated in one era and one measurement regime

Round 1's objection stands: a transmitted trait whose return rises with age (the paper's own AFQT result, $0.077^{***}$
at 25-29 to $0.181^{***}$ at 50-54) produces the profile without any causal role for the layoff, and son fixed effects
do not remove it. The additions narrow the trait to one of fathers laid off while the son is at home (A2) and one that
pays off for sons and not daughters (A4); they do not remove it. What is new is the cohort finding. Within son, on the
sons whose teens fall in 1976 and later, the slope is 0.040 (0.113) (`simulated_replacement_rate.md`; sec7 footnote);
on sons whose teens fall in 1984 and later it is $-0.291$ (0.208) and $-0.430^{*}$ (0.222) (`ui_duration_weeks.md`).
Leave-one-cohort-out shows no single five-year cohort carries it, which is consistent with the pre-1963 cohorts
carrying it together. Those are the sons whose fathers' job-end reasons were asked in 1971-75 only if the job was less
than a year old and in 1976-83 only if the present position was under twelve months (round 1, Objection 6, from script
19's docstring), and whose teen layoffs fell in 1968-81. The paper cannot currently tell apart (a) the 1970s layoffs
were different (manufacturing, permanent, the two oil recessions), (b) the 1968-75 net records a different event, (c)
chance in a $p = 0.02$ estimate. Any of the three changes the paper. **What answers it:** the band and within-son
profiles by the regime of the father's layoff years (1968-75, 1976-83, 1984+) and by the son's birth cohort (born
before 1963, 1963-75, 1976+), with the 45-49 band on the 1963-76 cohort reported explicitly (they reach 45-49 in
2008-2025, so the PSID has them); a layoff share built the same way in all regimes (restrict to job changes within
twelve months in every wave, which is what the early waves measure); and a statement of which cohorts the headline is
about.

### Objection 2 (serious): the selection designs narrow the reading but leave a comparison-group problem the daughters make visible

A2's reference group (layoff only at the son's 20-26) differs from T and E in the father's age at layoff and in whether
the son was in the household; the paper's footnote concedes it. A3's splits are at $p = 0.06$-$0.15$. The daughters'
positive wage, earnings and family-income profiles (Section 3 above) say the comparison group of sons of never-laid-off
fathers differs in something that pays off late for sons only. A referee's candidate list: the father's occupation and
industry (sons follow fathers into jobs; daughters do not), union or public-sector jobs (which the paper's Appendix D
and Section 7 touch for race, not for layoffs), selection of daughters into employment at 45-49, and assortative
mating (daughters' family income $+0.560^{**}$). **What answers it:** (i) daughters' employment, hours, marriage,
husband's earnings, schooling and occupation at 45-49 by the father's layoff, and the daughters' earnings slope with
zeros kept (Poisson); (ii) the father's own earnings and employment path after the layoff by T, E and L and by
small/large loss, so the reader sees whether the "small-loss, short-unemployment, repeated" father is a churner or a
recall worker; (iii) the layoff split by whether the layoff year was a decline year of the father's sector or a
high-unemployment year in his state (the less selected layoffs, Gibbons and Katz): if only the non-recession layoffs
carry the cost, the costly layoffs are the idiosyncratic ones and the causal reading weakens; if both do, the trait
reading weakens. All three are days of work on 91's framework.

### Objection 3 (serious): there is no mechanism for a cost that is zero at 30 and 11 log points at 45 in the wage, with no change in employment

The paper's Section 5 has the machinery (occupation score versus within-occupation residual, the early-job cell at
25-34, access to fast-growing jobs, the schooling return) and never applies it to the layoff. Without it "unstable
employment, not an income shock" is a label on a residual. **What answers it:** the layoff share in 27's and 35's
designs: do sons of laid-off fathers start in the same occupation-industry cells and fall behind within them (a
within-job story), or start in different cells (a sorting story the paper already knows how to read)? Their own job
changes, tenure, displacement and health (PSID health status, 1984 on) at 35-49. The result is convincing either way: a
within-cell cost points to something the son carries; a sorting cost points to the job the son takes at 25-34, which
is observable and testable at that age.

### Objection 4 (serious for headline 1): the shares are cohort-dependent and "money" is still a label

Rest $47.6^{***}$ in the full sample, 11.4 (n.s.) on the 1964+ cohort before wealth. The measurement-error correction
is a lower bound; the wage share is 28-37 percent. The abstract's "where wealth is measured, parental net worth carries
three tenths" is true; "and little rest remains" was true before wealth was added. **What answers it:** the full split
(panel B plus wealth) on the 1964+ cohort as the primary table, the full sample as robustness, and the sentence in
Section 3 above as the headline.

### Objection 5 (moderate): the industry-shock reduced form is a significant gain, not "no cost"

$+0.143^{**}$ (0.063; $p = 0.024$) within son, teen window, with the two placebo windows null. The paper reports it as
"of the wrong sign for a cost" and moves on. A referee will ask why sons of fathers in sectors that declined during
their teens do *better* with age (they avoid the father's sector? sector $\times$ age controls are too coarse at 15
sectors?). State a reading or report it as unexplained, as the daughters are.

### Objection 6 (moderate): Section 7 has no finding

UI: $p = 0.50$, $-0.038$ (0.187), $-0.191$ (0.395). EITC: marginal, intent-to-treat on all sons, null where the credit
binds. Group friction: $8.2^{***}$ pooled, 0.0 within White, $-9.1$ (14.5) within Black, "cannot be told apart from
anything else that differs by race". Transfers: receipt is selection. "The age of scoring" is an inference from the
shares. Fourteen pages for four nulls is a target; one page of nulls stated as nulls is a service.

### Objection 7 (minor, will be raised)

- Three baselines for the same object: $0.276^{***} \to 0.484^{***}$ (Table `tab_ige_sons`, sec3), $0.283^{***} \to
  0.492^{***}$ (Table `tab_age_period`), 0.443 at 45-49 (Table `tab_passed_on`, 4,770 sons). Pick one sample and say
  so.
- The NLSY97 sentence. The AFQT carries 0.021 of the NLSY97 opening of 0.083 (25 percent), against 62 percent of the
  NLSY79 opening to 50-54. "Rises by the same factor" compares ratios of contributions (1.64 versus 1.70); it does not
  support "carries three fifths" in the younger cohort. Say which.
- The Shea contrast (Table `tab_shea_spell`) is still in the introduction as a finding. Round 1's Objection 4 stands:
  with one predictor, $b_P = 0.742^{***}$ is the layoff's reduced form divided by its gradient in parental income, and
  the closure half is 0.074 (0.561).
- The sex comparison in sec6 pairs the sons' band change ($-0.538^{**}$) with the daughters' within-person slope
  ($0.168^{**}$); the sons' within-person wage slope in that specification is $-0.086$ (0.096). Report like with like.
- Objection 7 of round 1 (the race-neutral framing against the paper's own evidence: the rise is White, the father's
  schooling is White, the layoff gradient is White, Black T and E slopes are 0.062 and 0.072) is unchanged. The defence
  the paper gives ("the cost is common, the gradient differs") rests on the Black within-son estimate $-0.306^{**}$
  that becomes $-0.068$ with timing controls and $+0.062$ in A2. Say "the cost is not distinguishable by race, on 37
  treated Black sons at 45-49", not "as much".

---

## 5. Next steps, ranked (public data only; each with design, what convinces, effort, which headline)

**1. Cohort and regime stability of the layoff cost (serves headline 2; decides the paper). Days.**
Script 88/91 with the sample split three ways: sons born before 1963 / 1963-75 / 1976+; and the father's layoff share
built (a) as now and (b) only from job changes within twelve months of the interview in every wave (the early-wave
definition applied throughout). Report the band profile (25-29, 45-49, change) and the within-son slope for each
cell, with treated counts. Convincing: a slope of the same sign and comparable size in the 1963-75 cohort (who reach
45-49 in 2008-25) under definition (b). If the cost is only in the pre-1963 sons, the paper becomes one about the
layoffs of the 1970s and must say so; that is still a paper, with a different title and a different policy section.

**2. The father's own path and the recession split (serves headline 2, Objection 2). Days.**
On 91's framework: (i) the father's log earnings, employment and layoff count in the five years after the window by
T/E/L and by the A3 parts, to show what kind of father a "small-loss, short-unemployment, repeated" layoff marks;
(ii) the teen layoff share split into layoff years in which the father's sector's national employment fell (93's
measure) or the state unemployment rate exceeded its trend, versus other years; within-son slope of each part and the
test of equality. Convincing: the cost present in the recession-year layoffs (less selected) at a size comparable to
the others.

**3. Daughters: selection and marriage (Objection 2). Days.**
Script 92 extended: employment, hours, married, husband's log earnings, years of schooling and occupation score at
45-49 on the father's layoff share; daughters' earnings slope with zeros kept (PPML). Convincing: a within-daughter
wage gain that survives employment and marriage controls is a real asymmetry and deserves its own paragraph (the
literature on mothers' work and daughters' attachment is the place to look [?]); a gain that is marriage or selection
removes the daughters from the sons' argument and should be reported as such.

**4. Mechanism through the career toolkit (Objection 3; makes headline 2 a story). One week.**
The layoff share in 27's occupation-score decomposition (between versus within occupation at 25-34 and 45-49), in 35's
early-job-cell and access regressions, and in the same-employer growth design (36). Add the son's own displacement,
tenure and health at 35-49 as outcomes. Convincing: either a within-cell wage shortfall appearing after 40 (then look
at health and job changes), or a lower probability of starting in the fast-growing cells at 25-34 that Section 5
already shows predicts the gap after 35. Either closes the "label on a residual" objection.

**5. Headline 1 restated on the fully measured cohort (Objection 4). Days.**
Script 98's split (panel B plus wealth rank) on the 1964+ cohort by band as the primary Table 4, the full sample as a
robustness panel, the IV-corrected shares beside the OLS. Drop "half is money"; write the sentence in Section 3 above.

**6. Restructure around the strongest finding, and the cuts the PI deferred (two weeks of writing, after 1-4).**
Order: the IGE rises with age (fact; one table) $\to$ what rises: skill at entry and schooling (NLSY79/97; one table),
wealth and the wage (PSID 1964+ cohort; one table) $\to$ the one component whose share rises, the father's layoff:
profile, within son, timing, what kind of layoff, daughters, the father's path, mechanism (three tables) $\to$ what the
layoff is not: closures, industry declines, income (one table) $\to$ policy in one page (UI null, EITC marginal, the
age of scoring as a corollary) $\to$ race as a subsection in each section. Title around the age profile of what is
passed on, not the split. Cuts now, in this order: the Shea contrast to one paragraph in the layoff section stating the
Wald-ratio reading (or the appendix); the son's own spells to a short subsection ending Section 3 (it is a life-cycle
bias result, not a transmission result); group friction and transfers to the appendix; the UI tables to the appendix
with two sentences in the policy page; the EITC to one paragraph with its $p$-values; Appendix D halved to what the
race subsections cite; Appendix B dropped (no main-text claim depends on it); the "same factor" sentence corrected.
Nothing of substance is lost by these cuts; the paper is at 103 pages with 14 pages of nulls in Section 7.

**7. What I would not plan on.** A second data set at 45-49 with firings separated (SOEP) is the single addition that
would most change a QJE referee's mind, and the plan cannot depend on it. The structural model is not needed for any of
the above and would not substitute for step 1 or 2.

---

## 6. If I were the author: the next two weeks

**Week 1.** Day 1-2: step 1 (cohort and regime split; definition (b) of the layoff share). Day 3-4: step 2 (father's
path by T/E/L and by A3 part; recession-year split). Day 5: step 3 (daughters' employment, marriage, husband's
earnings, PPML). End of week: decide which paper this is. If the within-son cost holds in the 1963-75 cohort under the
common definition, it is the layoff paper and the restructure goes ahead. If it does not, it is the age-profile
accounting paper with the layoff as a 1970s fact, aimed at JOLE/JHR, written in two weeks without further runs.

**Week 2.** Day 1-4: step 4 (the layoff through the career toolkit; health and own displacement). Day 5: step 5 (the
1964+ split as the primary Table 4). Rewrite the abstract and introduction around the order in step 6; apply the cut
list; unify the baseline sample; replace "as much" and "the same factor" with the tested statements. Then the paper is
ready for JPE/REStud/AEJ: Applied with the Week-1 answer in hand; it is ready for the QJE only if a second data set at
45-49 arrives.
