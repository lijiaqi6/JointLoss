# Simulated JPE decision on Paper B (2026-10-20)

**This is a simulation** written by Claude at the PI's request, for the version compiled on 2026-10-20 (commit 05ed315,
107 pages; "What Parents Pass On: Wages, Spells and Skills in the Intergenerational Elasticity of Earnings"). The
editor and the three referees are invented; their views are built from the paper, `EVIDENCE.md` (rows 11.28-11.56) and
the two Fable memos. Numbers are the paper's own.

---

## Editor's letter

Dear Author,

Thank you for submitting your paper to the *Journal of Political Economy*. I have received three reports from experts
in intergenerational mobility, job displacement, and family and labor economics. Referee 1 recommends a major revision,
Referee 2 recommends rejection, and Referee 3 recommends a major revision. After reading the paper and the reports, my
decision is **major revision, at high risk**. I want to be clear about what that means: the next version will go back
to the same referees, and I will not be able to continue with the paper unless it answers the points below.

The referees agree on what is valuable. The paper documents, with care and more robustness than is usual, that a
father's layoff during his son's childhood is unrelated to the son's earnings at 25-29 and lowers them substantially at
45-49, within the same son, in the wage, in every birth cohort, while plant closures carry no such cost. Referee 3 and I
also find the opposite movement of sons' and daughters' wages after the same layoffs striking (a difference of 0.925
per unit share in the wage change, p = 0.001). The age-of-scoring point, illustrated with the EITC, is useful for the
evaluation literature.

The referees also agree on what is not yet a JPE paper. First, the paper is three papers: an accounting split of the
IGE, a fact about layoffs and the age profile, and a policy section of mostly null results. At 107 pages, with 21 main
tables, the reader cannot tell which result the paper is about. The layoff profile and the sons-daughters contrast are
the contribution; the split should be the frame that leads to them, in a few pages, and the policy section should be one
page. Second, Referee 2's identification concern is the decisive one. Every design in the paper narrows what the layoff
can stand for; none assigns it. The industry-shock instrument has a first stage of F = 2.9 on layoffs, the timing
comparison and the bad-times split are imprecise, and the father's path shows that the treatment is a father in
chronically unstable employment. That may be the right object, but then the paper must be written about it, not about
"a layoff". Third, the daughters' result needs a mechanism or at least a disciplined set of candidate explanations; as
it stands it is a striking fact with a p-value that, given the number of splits in the paper, a reader will discount.

In revising, please (i) restructure around the layoff profile and the sons-daughters contrast, moving the split to a
short opening and the policy material to one page; (ii) address Referee 2's points 1-4, in particular pre-trends in the
father's earnings and the placebo with layoffs after the son has left home; (iii) take Referee 3's points on the
mother's response and the daughters' selection; (iv) address multiple testing (Referees 1 and 2); and (v) unify the
baseline sample. A second data set reaching 45-49 would strengthen the paper most; I understand it may not be available
and do not make it a condition.

Sincerely,
Co-editor (simulated)

---

## Referee 1 (intergenerational mobility and measurement) - recommendation: major revision

**Summary.** The paper splits the earnings IGE in the PSID into parental components by the son's age, shows that the IGE
rises with age because skill at entry and schooling pay more later (with an NLSY97 check that separates age from
period), and finds that one parental component, the father's childhood layoffs, carries a share that rises with the
son's age. It adds parental wealth for later cohorts, a measurement-error correction, and a contrast between sons and
daughters.

**Assessment.** The age profile of the IGE is known (Haider and Solon 2006; Nybom and Stuhler 2016, 2017; Mazumder
2016; Chetty et al. 2014). What is new is (a) locating the rise in components and (b) the layoff profile. I find (b)
interesting and (a) careful but limited by what a Gelbach split can say. The paper is honest about the split being
accounting; it should then claim less from it.

**Major comments.**
1. *The split.* The shares depend on which components are in, how well they are measured and which cohort is used. The
   wage share is 19.0 percent in the main split, 12.0 with the father's schooling, 28.0 in the split-half sample and 36.8
   corrected for measurement error; the rest is 47.6 percent in the full sample and 11.4 percent (n.s.) in the cohorts
   with wealth before wealth enters. A reader cannot take any one share as "what is passed on". I suggest presenting the
   split as a ranking that is stable across these versions (wage and schooling first, spells small, hours and place
   nothing) and dropping the precise shares from the abstract.
2. *Three baselines.* The IGE profile appears as 0.276 to 0.484 (Table 1), 0.283 to 0.492 (Table on age and period) and
   0.443 at 45-49 in the split sample of 4,770 sons. Choose one sample for the paper and state the others as checks.
3. *Wealth.* The wealth result (29.1 percent of the IGE for sons born 1964 and later) is potentially the most important
   accounting result, and it is in a robustness table. If the later cohorts are the fully measured ones, make them the
   main split and say so; then "half is money" in earlier drafts becomes "wealth carries three tenths", which is a
   finding in the spirit of Pfeffer and Killewald (2018) and Fagereng et al.
4. *The NLSY97 sentence.* The AFQT's contribution rises by a similar factor in the NLSY79 and NLSY97 (1.70 and 1.64),
   which supports age over period; but it carries 25 percent of the NLSY97 opening against 62 percent in the NLSY79.
   The abstract's "carries three fifths of the rise ... and rises by the same factor in the NLSY97" conflates the two.
5. *Multiple testing.* The paper reports dozens of splits (by cohort, regime, timing, kind of layoff, bad times, sex,
   race). Please state which tests were planned, report a family-wise or false-discovery correction for the layoff and
   daughters results, and put the rest in an appendix.
6. *Race.* The paper is race-neutral by design but finds that the rise, the father's schooling and the layoff gradient
   are White. "Black fathers' layoffs cost their sons as much" rests on 37 treated Black sons at 45-49 and on a
   within-son estimate that falls to -0.068 with timing controls. Say "not distinguishable".

**Minor comments.** The abstract's "Unemployment insurance at the father's wage does not weaken it" now follows the
daughters sentence, so "it" is ambiguous. The Shea comparison is a Wald ratio of the layoff's reduced form; present it as
such or drop it. Report the rank-based version of the layoff profile, since the log IGE weights the bottom of the
distribution heavily.

---

## Referee 2 (job displacement and identification) - recommendation: reject

**Summary.** The central claim is that a father's layoff in the son's childhood costs the son more as he ages: zero at
25-29, -0.768 per unit share (about 11 log points per layoff year) at 45-49, within son -0.236 a decade, present in all
cohorts and larger (-0.391) with a common job-end definition. Plant closures and national declines of the father's
industry carry no cost.

**Assessment.** The fact is carefully documented and survives more checks than most papers attempt. My concern is that
the paper cannot tell whether the layoff, or the kind of father who is laid off, produces it, and its own evidence leans
toward the second.

**Major comments.**
1. *Selection on the father's trajectory.* The father's path (unemployed +0.289, laid off again +0.132 at the son's 20-24)
   shows the treated fathers are on a different employment trajectory. Show the father's earnings and employment in the
   years before the first teen layoff (an event study on the father, with never-laid-off fathers matched on earnings and
   age before). If the treated fathers are already falling before the layoff, the "layoff" is a marker of a decline that
   began earlier, and the timing results lose their bite.
2. *A placebo with later layoffs.* Layoffs at the son's 20-26 carry nothing, but those fathers are older and the sons
   have left. A cleaner placebo: the same fathers' layoffs after the son is 26, or layoffs of fathers whose sons are
   observed but grown, should predict nothing for the son's profile if the effect works through childhood exposure, and
   should predict it if the layoff marks a trait. Report it.
3. *Closures as the comparison.* The closure null is the paper's best design, but it is a null with a wide interval: the
   change for closures is 0.000 (s.e. 0.258), so a closure cost half as large as the layoff cost is not excluded. The
   layoff-minus-closure difference (-0.914, p = 0.005) is informative; report the closure cost's upper confidence bound
   explicitly and say what share of the layoff cost it allows.
4. *The instruments.* The industry-shock first stage on layoffs (F = 2.9) is too weak to identify anything about
   layoffs, and its reduced form is a significant gain (+0.143 within son), which the paper does not explain. The
   bad-times layoffs carry about half the cost, but the within-son estimate is not significant (-0.166, s.e. 0.149) and
   equality with other layoffs is not rejected (p = 0.26). These designs do not support a causal reading; the paper
   should say plainly that the result is descriptive and that the treatment is unstable paternal employment.
5. *Comparison with the displacement literature.* Oreopoulos, Page and Stevens (2008) and Hilger (2016) find small or
   short-lived effects of fathers' displacement on children's earnings. The paper's appendix finds the same for
   displacement at 0-17 scored at 25-44. The paper should reconcile its large effect at 45-49 with those estimates in the
   main text: is the difference age (they do not observe 45-49), the layoff/closure split, or selection?
6. *Power and counts.* 135 treated sons at 45-49, 21 at 40-44 among those born 1976 and later. The age profile at 45-49
   rests on the oldest cohorts' teen layoffs. The within-son design helps; still report the minimum detectable effect at
   45-49 and the number of treated sons in every table.

**Recommendation.** I would reconsider a version that states the result as the cost of growing up with a father in
unstable employment, shows pre-trends and the later-layoff placebo, and drops the causal language. In its present
framing I recommend rejection.

---

## Referee 3 (family, gender and policy) - recommendation: major revision

**Summary.** Beyond the layoff profile, the paper finds that the same paternal layoffs that lower sons' wages in midlife
raise daughters' wages, with a direct test of the difference (0.925 in the wage change, p = 0.001; 0.254 a decade within
person, p = 0.049). It evaluates policy margins (state UI generosity, a simulated replacement rate, weeks of benefits,
the EITC) and argues that evaluations scored around 30 miss components that grow with age.

**Assessment.** The sons-daughters contrast is the most novel result and could carry the paper, but it is presented as a
fact without a mechanism, and part of its robustness is weak (the within-person difference under the common job-end
definition is 0.314, p = 0.128; the daughters' own gain is nil for those born 1963-75).

**Major comments.**
1. *The mother.* The most natural channel is the mother's response to the father's layoff: the added-worker effect, a
   shift in household roles, a model of a working mother for daughters (Fernández, Fogli and Olivetti 2004; Olivetti,
   Patacchini and Zenou on role models [?]). The paper has the mother's employment in the PSID. Show the mother's hours
   and employment after the father's teen layoffs, and whether the daughters' gain is concentrated where the mother
   increased her work.
2. *Who is observed.* Daughters' outcomes are measured as heads or wives. Sample selection into headship, marriage and
   staying in the panel may differ by the father's layoff. Show attrition and headship by layoff status, and the
   daughters' result with inverse-probability weights.
3. *Schooling and occupation.* Daughters' schooling rises (+0.49 years) and sons' falls (-0.40); each is insignificant but
   the difference may not be. Test it, and show daughters' occupation scores, since the sons' cost is within
   occupation.
4. *Assortative mating.* Daughters' partners earn more at 45-49 (+0.677). Is this a consequence of the daughters' own
   attachment (they marry later and better), or a separate channel? Order the facts.
5. *Policy section.* Four nulls and a marginal EITC result take many pages. The UI tests cannot exclude effects of the
   relevant size (weeks: -0.191, s.e. 0.395); the EITC result is intent to treat, 0.016 lower earnings at 25-29 per
   $1,000 (p = 0.052) and null in the sample where the credit binds. Keep the age-of-scoring argument, with the EITC as an
   illustration and its p-values, in one page.

**Minor comments.** Use one specification for sons and daughters throughout the daughters section (the band change and
within-person slopes are compared in places). Discuss the cohort pattern of the daughters' gain (largest for those born
1976 and later), which may relate to the rising return to women's work.

---

## What the simulated decision asks for (for the PI)

| request | referee | feasible with our data | effort |
|---|---|---|---|
| restructure: layoff profile + sons-daughters as the paper, split as a short frame, policy one page | editor, R1, R3 | yes (writing; the PI's deferred cuts) | 1-2 weeks |
| pre-trends of the father's earnings and employment before the first teen layoff (event study) | R2.1 | yes, PSID | 2-3 days |
| placebo: the same fathers' layoffs after the son is 26 | R2.2 | yes, PSID | 1 day |
| closure cost upper bound; MDEs and treated counts in every table | R2.3, R2.6 | yes | 1 day |
| reconcile with Oreopoulos-Page-Stevens / Hilger in the main text | R2.5 | yes (writing + appendix result) | 1 day |
| multiple-testing correction for the layoff and daughters results | R1.5, editor | yes | 1 day |
| the mother's response and the daughters' gain | R3.1 | yes, PSID | 2 days |
| daughters' selection (headship, attrition, IPW) | R3.2 | yes | 1-2 days |
| daughters' schooling and occupation, sex difference tested | R3.3 | yes | 1 day |
| one baseline sample; NLSY97 and race wording; abstract "it" | R1.2, R1.4, R1.6 | yes | 1 day |
| rank-based layoff profile | R1 minor | yes | 1 day |
| a second data set at 45-49 | editor (not a condition) | SOEP deferred by the PI | - |
