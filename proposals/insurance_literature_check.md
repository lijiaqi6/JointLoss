# Literature check: husbands' job-loss risk, mothers' insurance work, the safety net and children (2026-10-17)

The candidate paper is the "insurance framing". Black husbands and fathers face higher job-loss risk. Married mothers insure
the household by working. A father's job loss is the strongest childhood correlate of children's lower adult earnings in our
PSID data, and the safety net competes with the mother as a source of insurance. The paper asks how these three shape children's
outcomes, the IGE and the Black–White gap at a given parental income. It would combine reduced-form evidence with a structural
lifecycle model (search friction, husbands' employment risk, a safety-net floor, marriage, fertility, human capital accumulation).

This note records what has and has not been done. Every paper below was checked on the source page linked next to it in this
session (publisher, NBER, IZA, RePEc/IDEAS, SSRN, author or institutional page), unless it is marked **UNVERIFIED**. Where I
read the PDF itself (via `pdftotext`), the entry says "(PDF read)". Papers already summarized in `IGE/literature_notes.md` (GGS
2015, FMR 2021, BFHO 2024, CHJP 2020, DFW 2014, Palomino et al. 2018) and in `proposals/safety_net_ige.md` §1 are only
cross-referenced here, with the URLs verified there.

Our own results used for comparison:
- **First stage** (`output/first_stage.md`). A 1 pp tighter men's-industry Bartik lowers married mothers' employment at b+2
  by 0.0247 relative to unmarried mothers (bartik_m × married = −0.0247**, s.e. 0.0112, p=0.027). In other words, married
  mothers work more after a birth when men's industries are slack. The state unemployment rate itself has the opposite sign
  (−0.0147** at b+1, p=0.014), and neither the unemployment rate nor the Bartiks interact with Black (ur × black +0.0012,
  p=0.786).
- **Childhood exposures and adult earnings** (`output/psid_child_exposure.md`, Section 3). A father figure's job loss at
  0–17 is associated with lower log lifetime earnings: −0.214*** for Black children (s.e. 0.081, p=0.009) and −0.099 for White
  children (s.e. 0.065, p=0.131). Job loss is measured as zero hours. The mother being employed at b+1 shows no association:
  Black +0.044 (p=0.440), White +0.042 (p=0.291). All of these are associations, not effects.

---

## Strand 1. Parental (especially fathers') job loss and children's outcomes

### 1a. Long-run outcomes (earnings, education, IGE)

**Oreopoulos, Page & Stevens (2008)**, "The Intergenerational Effects of Worker Displacement," *Journal of Labor Economics*
26(3): 455–483 (NBER WP 11587, 2005).
- *What it does:* Canadian administrative data, about 60,000 father–child pairs in the WP (1978–99). Fathers displaced by plant
  closures are compared with non-displaced fathers who had the same permanent income before 1982.
- *Key number:* children of displaced fathers earn about 9% less a year. They are more likely to receive UI and social
  assistance. The effects are concentrated in families at the bottom of the income distribution.
  ([NBER w11587](https://nber.org/papers/w11587))
- *Overlap:* **substantial** with our "father's job loss → child's adult earnings" fact. No race (Canada), no mother's labor
  supply, no safety-net variation, no model.

**Page, Stevens & Lindo (2009)**, "Parental Income Shocks and Outcomes of Disadvantaged Youth in the United States," in J.
Gruber (ed.), *The Problems of Disadvantaged Youth*, NBER/University of Chicago Press, pp. 213–235. (PDF read)
- *What it does:* **PSID**, head's displacement (layoffs and firm closures; also closures alone), children's adult family
  income, earnings, schooling, UI/AFDC receipt and teen pregnancy. N = 1,444 children; subgroup rows include **Black (N = 476)**.
- *Key numbers:*
  - With layoffs included, children of displaced heads earn about 9% less as adults, even after background controls.
  - The estimate is close to zero when only firm closures are used, which the authors read as selection into layoffs.
  - Closures hurt children from families below 1.5× the poverty line: 36 pp less likely to complete high school, 16 pp less
    likely to attend college.
  - For Black children the income and earnings point estimates are negative and larger than in the full sample but not
    significant. College attendance falls significantly, and UI receipt rises significantly.
  - Children under 7 at the job loss have about 18% lower adult earnings than older displaced children (imprecise).
  ([NBER chapter c0594](https://www.nber.org/chapters/c0594); PDF https://www.nber.org/system/files/chapters/c0594/c0594.pdf)
- *Overlap:* **substantial.** This is our PSID fact (father's job loss → child's adult earnings, by race) done fifteen years
  earlier on older cohorts. They also show the result depends on the displacement definition. No mothers' labor supply, no
  safety net, no IGE decomposition, no model.

**Hilger (2016)**, "Parental Job Loss and Children's Long-Term Outcomes: Evidence from 7 Million Fathers' Layoffs," *AEJ:
Applied* 8(3): 247–283.
- *What it does:* US administrative (IRS) data. Uses the timing of fathers' layoffs when children are 12–29.
- *Key result:* layoffs sharply reduce family income but have only small effects on college enrollment, college quality and
  early-career earnings. Larger effects found with firm closures look like selection.
  ([IDEAS](https://ideas.repec.org/a/aea/aejapp/v8y2016i3p247-83.html))
- *Overlap:* **partial.** It is the strongest US counter-evidence: large income shocks in adolescence, small effects on
  children. It covers ages 12–29 only, has no race, no mother's response and no early childhood.

**Bratberg, Nilsen & Vaage (2008)**, "Job Losses and Child Outcomes," *Labour Economics* 15: 591–603 (IZA DP 2895).
- Norwegian matched employer–employee data, fathers displaced in 1986–87, children's earnings in 1999–2001.
- **No significant effect on children.** ([SWoPEc / Bergen WP 07/07](https://swopec.hhs.se/bergec/abs/bergec2007_007.htm))
- *Overlap:* partial (same question, null, Norway).

**Huttunen & Riukula (2024)**, "Parental Job Loss and Children's Careers," *Labour Economics* (doi 10.1016/j.labeco.2024.102578;
IZA DP 12788, 2019).
- Finnish registers. A father's job loss lowers children's earnings and pushes them toward lower-paying fields and away from the
  father's field. No effects on school grades, inactivity or delinquency.
  ([ETLA page](https://www.etla.fi/en/publications/academic-publications/parental-job-loss-and-childrens-career-choices/))
- *Overlap:* partial (long-run earnings, mechanism = career choice and networks).

**Uguccioni (2021)**, "The Long-Run Effects of Parental Unemployment in Childhood," CLEF Working Paper 45.
- Canadian tax data, children born 1972–85, random-forest proximity matching.
- Parental job loss at ages 2–10 → about $2,500 a year lower adult earnings (3–4 rank points), 36% more likely to receive
  welfare, 4% less likely to attend post-secondary education. Larger before age 10. Mechanisms: the timing of income loss and
  moves to lower-opportunity neighbourhoods.
  ([EconPapers](https://econpapers.repec.org/paper/zbwclefwp/45.htm); [JMP PDF](https://www.economics.utoronto.ca/public/jmp/uguccioni_jmp_final.pdf))
- *Overlap:* **partial–substantial** on timing in early childhood and on rank outcomes. No race, no spousal response.

**Carneiro, Salvanes, Willage & Willén (2022)**, "The Timing of Parental Job Displacement, Child Development and Family
Adjustment," IZA DP 15630 / NHH DP 2022/12. (PDF read, pp. 1–7)
- *What it does:* Norwegian registers 1986–2018, mass layoffs and closures, base years 1989–2006. Child age at displacement in
  three bands (0–5, 6–10, 11–16). Parental adjustment (earnings, employment, fertility, mobility, education, labor force exit,
  mental health) is studied with a Jacobson–LaLonde–Sullivan difference-in-differences.
- *Key results:*
  - Early displacement has the largest effect on household income; teenage displacement has the largest effect on schooling.
  - Children are significantly more affected by **mothers'** than by fathers' displacement.
  - The age pattern is attributed to short-run maternal stress, not to differences in parental responses.
  ([IZA DP 15630](https://docs.iza.org/dp15630.pdf); [IDEAS](https://ideas.repec.org/p/hhs/nhheco/2022_012.html))
- *Overlap:* **partial.** Timing plus family adjustment is close to our design. But in their setting mothers' shocks matter
  more, the opposite of our father-centred PSID association, and there is no race and no model.

**Willage & Willén (2022)**, "Postpartum Job Loss: Transitory Effect on Mothers, Long-run Damage to Children," *European
Economic Review* 150.
- Norway, mass layoffs and closures. A mother's job loss in the first postpartum year harms children's education 15 years
  later. There is no such effect for a father's job loss, or for a mother's later job loss. The proposed mechanism is maternal
  stress. ([IDEAS](https://ideas.repec.org/p/hhs/nhheco/2020_022.html))
- *Overlap:* partial. Relevant to "mothers' first-year employment": an involuntary *loss* of the mother's job at the birth
  hurts children in Norway.

**Gregg, Macmillan & Nasim (2012)**, "The Impact of Fathers' Job Loss during the Recession of the 1980s on their Children's
Educational Attainment and Labour Market Outcomes," *Fiscal Studies* 33(2): 237–264.
- British Cohort Study, with industry contractions in 1980–83 mapped to fathers. Lower GCSE results and weaker early labour
  market attachment; no direct earnings effect at 30/34. ([UCL Discovery](https://discovery.ucl.ac.uk/id/eprint/1493639/))
- *Overlap:* partial.

**Coelli (2011)**, "Parental Job Loss and the Education Enrollment of Youth," *Labour Economics* 18(1): 25–35.
- Canadian SLID. Parental job loss (layoffs, business failures) when youth are 16–18 lowers university and community-college
  enrollment; parental income falls significantly. ([DOI](https://www.doi.org/10.1016/j.labeco.2010.04.015);
  [CRDCN](https://crdcn.ca/publication/parental-job-loss-and-the-education-enrollment-of-youth/))
- *Overlap:* partial.

**Pan & Ost (2014)**, "The Impact of Parental Layoff on Higher Education Investment," *Economics of Education Review* 42: 53–63.
- Layoff when the child is 15–17. A UIC summary reports children of laid-off parents are 10% less likely to have enrolled in
  college by 30. The data set is not confirmed on the pages read. ([IDEAS](https://ideas.repec.org/a/eee/ecoedu/v42y2014icp53-63.html);
  [UIC news](https://live.today.uic.edu/economics-of-earnings-education/))
- *Overlap:* partial.

**Stuart (2022)**, "The Long-Run Effects of Recessions on Education and Income," *AEJ: Applied* 14(1): 42–74.
- Confidential Census data, county severity of the 1980–82 recession × cohort.
- For children aged 0–10 in 1979, a 10% fall in county earnings per capita → 15% less four-year degree attainment and 5% lower
  adult earnings. ([IDEAS](https://ideas.repec.org/a/aea/aejapp/v14y2022i1p42-74.html);
  [AEA](https://www.aeaweb.org/doi/10.1257/app.20180055))
- *Overlap:* partial (community-level shock, long-run outcomes; no household mechanism).

**Kalil & Wightman (2011)**, "Parental Job Loss and Children's Educational Attainment in Black and White Middle-Class
Families," *Social Science Quarterly* 92(1): 57–78.
- **PSID**, children born into the survey 1968–79, followed to 21.
- Parental job loss is associated with lower odds of any post-secondary education. The association is **almost three times as
  strong for Black youth**.
  - Wealth, long-run income and especially parents' long-term unemployment explain a "substantial share" of the racial
    difference (abstract); a UW–Madison event page says about one third.
  - Associational design, middle-class subsample.
  ([IDEAS citation page](https://ideas.repec.org/r/bla/socsci/v92y2011i1p57-78.html);
  [UW–Madison event](https://today.wisc.edu/events/view/12258))
- *Overlap:* **substantial** with our "stronger for Black children" pattern, in the same data.

### 1b. Short-run outcomes (schooling, test scores, health)

**Rege, Telle & Votruba (2011)**, "Parental Job Loss and Children's School Performance," *Review of Economic Studies* 78(4):
1462–1489.
- Norwegian registers, plant closures. **Fathers'** job loss lowers children's grade-10 GPA; mothers' job loss has a
  non-significant positive effect.
- The paternal effect looks **largely unrelated** to father's income, father's employment, *a shift in maternal time towards
  employment*, divorce or relocation. The authors point to fathers' mental distress.
  ([IDEAS](https://ideas.repec.org/a/oup/restud/v78y2011i4p1462-1489.html))
- *Overlap:* **partial, and important.** It already tests whether the mother's shift toward market work mediates the effect of
  the father's job loss, and finds it does not (in Norway).

**Stevens & Schaller (2011)**, "Short-Run Effects of Parental Job Loss on Children's Academic Achievement," *Economics of
Education Review* 30(2): 289–299 (NBER WP 15480).
- SIPP 1996/2001/2004, child fixed effects. Grade retention rises by 0.8 pp (about 15%); concentrated among parents with high
  school or less.
- Black vs White effects are not statistically different. The point estimate for Black children is smaller (WP text, PDF
  read). ([NBER w15480](https://www.nber.org/papers/w15480))
- *Overlap:* partial (short run; race tested, no difference).

**Kalil & Ziol-Guest (2008)**, parental employment circumstances and children's academic progress.
- SIPP 1996, 4,476 children of married parents. Fathers' involuntary separations are associated with worse academic progress;
  mothers' employment experiences are not, even where mothers out-earn fathers.
  ([UChicago Knowledge record](https://knowledge.uchicago.edu/record/1303?ln=en))
- Venue: **UNVERIFIED** (believed to be *Social Science Research*, not confirmed).
- *Overlap:* partial.

**Lindo (2011)**, "Parental Job Loss and Infant Health," *Journal of Health Economics* 30(5): 869–879.
- **PSID**, mother fixed effects: children born after a husband's displacement are compared with siblings born before.
- **Husbands'** job losses lower birth weight by about 4.5%, concentrated in the lower half of the birth-weight distribution.
  ([PubMed 21798606](https://pubmed.ncbi.nlm.nih.gov/21798606/); [IZA DP 5213](https://repec.iza.org/dp5213.pdf))
- *Overlap:* partial (husbands' job loss → infant outcome in the PSID).

**Schaller & Zerpa (2019)**, "Short-Run Effects of Parental Job Loss on Child Health," *American Journal of Health Economics*
5(1): 8–41 (NBER WP 21745).
- MEPS, 16 waves, fixed effects. **Paternal** job loss worsens children's physical and mental health, most in low-SES families;
  maternal job loss does not. Public coverage replaces close to half of the lost private coverage.
  ([IDEAS](https://ideas.repec.org/a/tpr/amjhec/v5y2019i1p8-41.html); [NBER w21745](https://www.nber.org/papers/w21745))
- *Overlap:* partial. Includes a safety-net offset (Medicaid/CHIP), but no race contrast and no long-run outcome.

**Mörk, Sjögren & Svaleryd (2020)**, "Consequences of Parental Job Loss on the Family Environment and on Human Capital
Formation – Evidence from Workplace Closures," *Labour Economics* (IZA DP 12559, 2019).
- Swedish registers, propensity-score matching. **No** adverse effects on children's health, education or early adult outcomes.
  Parents' health, labor market outcomes and separations do worsen.
- Disposable income is largely protected, which the authors attribute to generous UI **and a dual-earner norm**.
  ([IZA DP 12559](https://repec.iza.org/dp12559.pdf); [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0927537120301159))
- *Overlap:* **partial, conceptually close.** It names the two insurance sources we study (public UI and the second earner) as
  the reason children are shielded. It does not separate them or vary them.

**Britto, Melo & Sampaio (2022)**, "The Kids Aren't Alright: Parental Job Loss and Children's Outcomes within and beyond
Schools," IZA DP 15591 / CEPR DP 17562. (PDF read, abstract)
- Brazil, linked administrative data, mass layoffs. Dropouts and age-grade distortion rise by up to 1.5 pp; also child labor,
  crime and early pregnancy; parents move children from private to public schools.
- An **RD in UI eligibility** shows that access to benefits mitigates teenage dropout, crime and the loss of school quality.
  ([IZA DP 15591](https://docs.iza.org/dp15591.pdf))
- *Overlap:* **partial–substantial** on "the safety net buffers children against parental job loss" (outside the US).

**Ananat, Gassman-Pines, Francis & Gibson-Davis (2011/2013)**, "Children Left Behind: The Effects of Statewide Job Loss on
Student Achievement," NBER WP 17104.
- Mass Layoff Statistics × NAEP 1996–2009. Job losses equal to 1% of the working-age population lower grade-8 math by 0.076 sd.
  The effect is far larger than the effect estimated for children whose own parent is displaced (spillovers). Mechanism: income
  and distress. ([NBER w17104](https://www.nber.org/papers/w17104.pdf); [IDEAS](https://ideas.repec.org/p/nbr/nberwo/17104.html))
- The same team (AJPH 2014, as reported on the Duke/JBHE pages) finds that statewide job losses raise suicide-related behavior
  among Black adolescents and girls. ([JBHE](https://jbhe.com/2014/09/parents-job-loss-can-increase-suicide-behaviors-among-black-adolescents-and-teenagers))
  The AJPH article itself is **UNVERIFIED**.
- *Overlap:* partial (community job loss; race in the mental-health paper).

**Not used:** Pinger, "Intergenerational Effects of Economic Distress: Paternal Unemployment and Child Secondary Schooling
Decisions" (Germany; the PDF is marked "preliminary, do not cite"; [SOLE PDF](https://www.sole-jole.org/assets/docs/15328.pdf)).

### 1c. Mechanisms documented in this strand
- **Income.** Supported by OPS 2008, PSL 2009 (low-income only), Uguccioni, Britto et al. (the UI RD) and Schaller–Zerpa.
  Hilger 2016 says the marginal propensity to spend income on college is low.
- **Divorce.** Charles & Stephens (2004), "Job Displacement, Disability, and Divorce," *JOLE* 22(2): 489–522. Divorce rises
  after layoffs, not after plant closings or disability, which suggests the layoff reveals the partner's quality.
  ([IDEAS](https://ideas.repec.org/p/nbr/nberwo/8578.html))
- **Mobility.** Uguccioni (moves to lower-opportunity neighbourhoods).
- **Maternal labor supply.** Rege et al. 2011 test it and reject it as the mediator. Carneiro et al. 2022 study parental
  adjustment and find stress, not responses, drives the timing pattern.
- **Stress / mental health.** Rege et al., Carneiro et al., Willage–Willén.
- **Race heterogeneity.** Only Kalil–Wightman (stronger for Black children), PSL 2009 (Black point estimates larger, not
  significant) and Stevens–Schaller (no difference) test it.

---

## Strand 2. Gender-specific labor-demand shocks and family outcomes

**Page, Schaller & Simon (2019)**, "The Effects of Aggregate and Gender-Specific Labor Demand Shocks on Child Health," *Journal of
Human Resources* 54(1): 37–78 (NBER WP 22394). (PDF read)
- *Design (checked):* **restricted NHIS 1997–2012** with state identifiers; outcomes are child health (costly-conditions index,
  excellent health, sick days, asthma attack, emotional difficulties).
  - Main regressor: state unemployment rate (mean of the 12 months before the interview).
  - Then a state **shift-share predicted employment growth** index (Bartik; Katz–Murphy; Blanchard–Katz): base-period industry
    shares × national industry growth.
  - Then **separate male and female predicted employment growth** indices.
  - Controls: parents' marital status, child race and sex, mother's education, state demographics, state trends in robustness.
- *Key numbers:*
  - A 1 pp increase in female predicted employment growth raises the costly-conditions index by about 0.015 sd; the same
    increase for men lowers it by about 0.009 sd (both p<0.05).
  - A 1 pp increase in male growth lowers the probability of an asthma attack by 0.2–0.3 pp (about 5%).
  - Male growth lowers cost-related delays in care by 6–8%.
  - Interpretation: both income (men) and maternal time (women) are inputs.
  ([NBER w22394](https://www.nber.org/papers/w22394); [JHR](https://jhr.uwpress.org/content/54/1/37))
- *Race:* race enters as a control and in balance checks of the indices. No race-heterogeneity results were found in the text
  read.
- *Overlap:* **substantial on design** (gender-specific Bartik shocks → children). They do not estimate the mother's or father's
  labor supply response at a birth, and they have no long-run outcomes, no race split and no safety-net interaction.

**Lindo, Schaller & Hansen (2018)**, "Caution! Men Not at Work: Gender-Specific Labor Market Conditions and Child Maltreatment,"
*Journal of Public Economics* 163: 77–98 (NBER WP 18994).
- California county data; unemployment, mass layoffs and gender-specific predicted employment. Maltreatment falls with men's
  employment and rises with women's; the interpretation is time use.
  ([Arizona experts page](https://experts.arizona.edu/en/publications/caution-men-not-at-work-gender-specific-labor-market-conditions-a/);
  [NBER w18994](https://www.nber.org/papers/w18994))
- *Overlap:* partial (gender-specific shocks → child outcome).

**Regmi & Henderson (2019)**, "Labor Demand Shocks at Birth and Cognitive Achievement during Childhood," *Economics of Education
Review* 73 (IZA DP 12521). (PDF read)
- *Design:* **NLSY79 Children and Young Adults** (children born 1978–2009, tested at 5–14) with geocoded state of birth.
  Gender-specific state predicted employment growth in the **year of birth** (industry share × national growth). State and year
  fixed effects; s.e. clustered by state of birth.
- *Key numbers:*
  - A 1 pp rise in male-specific growth raises math by 0.018–0.033 sd and reading by 0.025–0.032 sd.
  - Female-specific growth raises scores by about 0.015 and 0.019 sd, not significant.
  - Male growth also raises PPVT scores and the HOME score in the birth year, and lowers family poverty (about 1.4 pp per 1 pp).
  - First stage, own gender only (Table A1): male growth → fathers' weeks +0.425* and wages +0.035**; female growth → mothers'
    weeks +1.530**.
  - Effects are concentrated among children of **married** mothers.
  - **By race (Table 9), effects are concentrated among White children.** Black: math −0.011 (s.e. 0.073), reading −0.035
    (0.056), N ≈ 875.
  ([IDEAS](https://ideas.repec.org/p/iza/izadps/dp12521.html); [IZA PDF](https://docs.iza.org/dp12521.pdf))
- *Overlap:* **substantial.** Same data (NLSY79 CYA), same shock (gender-specific Bartik at the birth), married vs unmarried,
  race split. They do **not** estimate the cross effect (men's shock → mothers' weeks, i.e. insurance work), maternal time as a
  mediator, adult outcomes or the IGE, and they have no model. Their null for Black children is a fact we must confront.

**Schaller (2016)**, "Booms, Busts, and Fertility: Testing the Becker Model Using Gender-Specific Labor Demand," *Journal of Human
Resources* 51(1): 1–29.
- State gender-specific demand indices: better male conditions raise fertility; better female conditions have smaller negative
  effects. ([IDEAS](https://ideas.repec.org/a/uwp/jhriss/v51y2016i1p1-29.html))
- *Overlap:* partial (fertility margin in our model).

**Autor, Dorn & Hanson (2019)**, "When Work Disappears: Manufacturing Decline and the Falling Marriage Market Value of Young Men,"
*AER: Insights* 1(2): 161–178.
- China trade shocks to men's relative earnings, 1990–2014. Marriage and fertility fall, the share of unwed mothers rises, and
  more children live in poor single-parent households. ([AEA](https://www.aeaweb.org/doi/10.1257/aeri.20180010);
  [NBER w23173](https://www.nber.org/papers/w23173))
- *Overlap:* partial. Men's shocks → family structure → child poverty, through marriage rather than the mother's insurance work.

**Aizer (2010)**, "The Gender Wage Gap and Domestic Violence," *AER* 100(4): 1847–1859.
- Demand shifts in female-dominated industries narrow the wage gap and reduce violence against women (bargaining).
  ([IDEAS](https://ideas.repec.org/a/aea/aecrev/v100y2010i4p1847-59.html))
- *Overlap:* none on children directly (the WP version links violence in pregnancy to birth health).

**Shenhav (2021)**, "Lowering Standards to Wed? Spouse Quality, Marriage, and Labor Market Responses to the Gender Wage Gap,"
*REStat* 103(2): 265–279.
- Task-based demand shifts in the female/male wage ratio: husbands are more educated, marriage falls, women's hours rise.
  ([IDEAS](https://ideas.repec.org/a/tpr/restat/v103y2021i2p265-279.html))
- Her planned child-outcome stage ("The Power of the Purse", NAEd/Spencer fellowship abstract) was not found as a paper.
  ([NAEd](https://naeducation.org/awardee/naama-shenhav/))
- *Overlap:* partial (marriage margin).

**Kearney & Wilson (2018)**, "Male Earnings, Marriageable Men, and Nonmarital Fertility: Evidence from the Fracking Boom,"
*REStat* 100(4): 678–690.
- Fracking raises less-educated men's earnings; marital and nonmarital births rise, marriage does not.
  ([NBER w23408](https://nber.org/papers/w23408))
- *Overlap:* partial (fertility, marriage).

**Bertrand, Kamenica & Pan (2015)**, "Gender Identity and Relative Income within Households," *QJE* 130(2): 571–614.
- The distribution of the wife's income share drops sharply past one half. When she earns more: lower marriage rates and
  participation, lower satisfaction, more divorce. ([NBER w19023](https://www.nber.org/papers/w19023))
- *Overlap:* none directly. It is a constraint on how far wives can insure husbands.

**Searched for and not found:** a paper that uses men's-industry demand shocks to estimate **mothers' labor supply around a
birth** (the cross effect), with or without race. An extended search found none. Regmi–Henderson estimate own-gender first
stages only; PSS and LSH estimate child outcomes only.

---

## Strand 3. Added-worker effect, intra-household insurance and children

**Cullen & Gruber (2000)**, "Does Unemployment Insurance Crowd Out Spousal Labor Supply?" *JOLE* 18(3): 546–572 (NBER WP 5608,
"Spousal Labor Supply as Insurance").
- SIPP 1983–93, married couples 25–54, more than 2,500 unemployment spells.
- Up to 73 cents of wives' earnings lost per dollar of husbands' UI (67–73 cents in the Michigan release). Even without UI, the
  spousal offset covers only a small share of lost income. ([JOLE](https://www.journals.uchicago.edu/doi/10.1086/209969);
  [NBER w5608](https://www.nber.org/papers/w5608))
- *Overlap:* **substantial** on "the safety net crowds out the mother's insurance work". No children's outcomes, no race split.

**Stephens (2002)**, "Worker Displacement and the Added Worker Effect," *JOLE* 20(3): 504–537 (NBER WP 8260).
- **PSID.** Small effects on wives before the displacement, large and persistent effects after. The long-run rise in wives'
  labor supply replaces more than 25% of the husband's lost income (WP summary).
  ([IDEAS](https://ideas.repec.org/a/ucp/jlabec/v20y2002i3p504-537.html); [NBER w8260](https://www.nber.org/papers/w8260))
- *Overlap:* **substantial** on the added-worker fact in our data. No race, no children, no timing around births.

**Blundell, Pistaferri & Saporta-Eksten (2016)**, "Consumption Inequality and Family Labor Supply," *AER* 106(2): 387–435.
- PSID; a lifecycle model with two earners, correlated wage shocks, taxes and assets. Family labor supply is a major insurance
  channel against permanent wage shocks; little insurance is left beyond it.
  ([NBER w18445](https://www.nber.org/papers/w18445))
- *Overlap:* partial. It covers wage shocks, not job loss or search friction, and has no children's outcomes or race.

**Halla, Schmieder & Weber (2020)**, "Job Displacement, Family Dynamics, and Spousal Labor Supply," *AEJ: Applied* 12(4): 253–287.
- Austrian registers. Wives' labor supply rises moderately on the extensive margin, but **wives' earnings replace only a very
  small share** of the household income loss; **public transfers and taxes** do more insurance in the short run.
- Children in the household shape the response; a policy note by the authors says wives with children under 3 do not respond
  at all. ([AEA](https://www.aeaweb.org/doi/10.1257/app.20180671);
  [VoxEU](https://cepr.org/voxeu/columns/job-displacement-family-dynamics-and-spousal-labour-supply))
- *Overlap:* **substantial** on "spousal vs public insurance, conditional on young children". No children's outcomes, no race.

**Birinci (WP 2019, revised to 2026)**, "Spousal Labor Supply Response to Job Displacement and Implications for Optimal
Transfers," Federal Reserve Bank of St. Louis WP 2019-020.
- *Reduced form:* a limited spousal earnings response, explained by transfers crowding it out (cross-state variation); the
  response is smaller in recessions.
- *Model:* incomplete markets, a **frictional labor market, family labor supply** and aggregate shocks. Optimal policy has less
  generous means-tested and more generous employment-tested transfers.
  ([IDEAS](https://ideas.repec.org/p/fip/fedlwp/88548.html); [FedInPrint](https://www.fedinprint.org/item/fedlwp/88548/original))
- *Overlap:* **substantial on the parents' side of our model.** Search friction + spousal insurance + transfer crowd-out. No
  children, no race, no marriage or fertility.

**Hendren (2017)**, "Knowledge of Future Job Loss and Implications for Unemployment Insurance," *AER* 107(7): 1778–1823.
- Anticipated job loss raises spousal labor supply and lowers consumption before the loss; UI insures the risk of learning
  about it. ([NBER w21819](https://www.nber.org/papers/w21819))
- *Overlap:* partial. Supports measuring wives' responses *before* displacement in event studies.

**Mankart & Oikonomou (2017)**, "Household Search and the Aggregate Labour Market," *REStud* 84(4): 1735–1788.
- Two-member households, labor market frictions, incomplete markets; members adjust labor supply to insure unemployment risk.
  A companion *Economics Letters* (2016) paper documents a rising added-worker effect.
  ([IDEAS WP](https://ideas.repec.org/p/usg/econwp/201225.html); [Econ. Letters](https://ideas.repec.org/a/eee/ecolet/v143y2016icp48-51.html))
- *Overlap:* partial (household search model; no children, no race).

**Racial differences in husbands' risk and in wives' responses**
- **Fairlie & Kletzer (1998)**, "Jobs Lost, Jobs Regained: An Analysis of Black/White Differences in Job Displacement," *ILR
  Review*: **UNVERIFIED** (not found on a source page).
  - Verified related work by the same authors: "Race and the Shifting Burden of Job Displacement: 1982–93," *Monthly Labor
    Review* 1996. Black displacement rates converged to White rates over 1982–93.
    ([BLS](https://www.bls.gov/opub/mlr/1996/article/race-and-the-shifting-burden-of-job-displacement-1982-93.htm))
- **Couch & Fairlie (2010)**, "Last Hired, First Fired? Black-White Unemployment and the Business Cycle," *Demography* 47(1):
  227–247.
  - Matched CPS 1989–2004, prime-age men. Black men are shed first as the cycle weakens, but they are not "last hired". The gap
    narrows at peaks because Black job loss falls.
    ([IDEAS](https://ideas.repec.org/a/spr/demogr/v47y2010i1p227-247.html))
- **Hoynes, Miller & Schaller (2012)**, "Who Suffers during Recessions?" *JEP* 26(3): 27–48.
  - Cyclical losses are concentrated among men, Black and Hispanic workers, youth and the less educated. The pattern has been
    stable since the late 1970s, and much of it reflects industry and occupation exposure.
    ([NBER w17951](https://www.nber.org/papers/w17951))
- **Wrigley-Field & Seltzer (2020)**, "Unequally Insecure: Rising Black/White Disparities in Job Displacement, 1981–2017,"
  Washington Center for Equitable Growth WP.
  - Displaced Worker Survey. Black workers are nearly always more likely to be displaced; excess Black displacement doubled for
    women and tripled for men since the 1990s; occupation, industry and sector do not explain the rise.
    ([WCEG](https://equitablegrowth.org/working-papers/unequally-insecure-rising-black-white-disparities-in-job-displacement-1981-2017/))
- **Quinby & Wettstein (2025)**, "Is the Scarring from Unemployment Worse for Black Workers?" CRR WP 2025-7. (PDF read, abstract)
  - Administrative CWHS earnings, displacements in three recessions. Black displaced workers have a sharper immediate percentage
    earnings drop, but the same long-run drop as White workers.
    ([CRR](https://crr.bc.edu/is-the-scarring-from-unemployment-worse-for-black-workers/wp_2025-8))
- **Smith & Mattingly (2014)**, "Husbands' Job Loss and Wives' Labor Force Participation during Economic Downturns: Are All
  Recessions the Same?" *Monthly Labor Review*, September.
  - Matched May CPS 1981–82 and 2008–09.
  - Relative to White wives, Black non-employed wives had 67% higher odds of entering the labor force in 1981–82 (OR 1.674***),
    but no difference in 2008–09 (OR 1.059, n.s.).
  - In 2008–09 Black wives were still more likely to become **unemployed (searching)** (RRR 2.127*) but not more likely to
    become **employed** (0.848, n.s.).
    ([BLS MLR](https://www.bls.gov/opub/mlr/2014/article/husbands-job-loss-and-wives-labor-force-participation-during-economic-downturns-are-all-recessions-the-same.htm))
  - This is the only race-specific added-worker evidence found. It is descriptive and is consistent with a search friction for
    Black wives.
- **Ganong, Jones, Noel, Farrell, Greig & Wheat (2020/2023)**, "Wealth, Race, and Consumption Smoothing of Typical Income
  Shocks," NBER WP 27552.
  - Bank-account data, firm-wide pay changes as the instrument. Black and Hispanic households' consumption is about twice as
    sensitive to income shocks as White households'; nearly all of the gap is accounted for by liquid wealth.
    ([NBER w27552](https://nber.org/papers/w27552))
  - *Overlap:* partial (racial gap in self-insurance; no spouse or children).
- **Boustan & Collins (2014)**, "The Origins and Persistence of Black-White Differences in Women's Labor Force Participation,"
  in *Human Capital in History* (NBER WP 19040).
  - Black women worked more from 1870 to at least 1980. Observables explain little; the authors favor stigma and norms (Goldin
    1977) and intergenerational transmission. ([NBER w19040](https://www.nber.org/papers/w19040))
  - *Overlap:* a **competing explanation** for Black mothers' higher employment. An insurance motive must be shown, not
    assumed.

**Searched for and not found:** any paper that links the wife's insurance response to the husband's job loss with **children's
outcomes**. That covers whether her work mitigates or adds to the harm, apart from Rege et al.'s test of the maternal-time
mediator and Mörk et al.'s descriptive "dual-earner norm" argument. Also none that estimates the added-worker effect **around
births**, or **by race** with a causal design.

---

## Strand 4. The safety net as insurance against a parent's job loss, and the safety net and the IGE

**Shea (2000)**, "Does Parents' Money Matter?" *Journal of Public Economics* 77(2): 155–184 (NBER WP 6026).
- **PSID.** Parental income variation from union status, industry and **job loss** ("luck") has a negligible effect on
  children's human capital for most families, but matters when the father has low education.
  ([UMD page](https://www.econ.umd.edu/publication/does-parents-money-matter); [IDEAS WP](https://ideas.repec.org/p/nbr/nberwo/6026.html))
- *Overlap:* **substantial on method.** Father's job loss as an income instrument in the PSID. Its exclusion restriction (job
  loss affects children only through income) is exactly what Rege et al. reject.

**East & Simon (2020, rev. 2022)**, "How Well Insured are Job Losers? Efficacy of the Public Safety Net," NBER WP 28218.
- SIPP 1996–2013, individual fixed effects. UI is the largest buffer, but the lowest-income job losers are less well insured than
  middle- and higher-income ones. ([NBER w28218](https://www.nber.org/papers/w28218))
- *Overlap:* partial (safety-net insurance of job loss, by pre-loss income; no children or race result found on the page).

**Regmi (2018)**, "Examining the Externality of Unemployment Insurance on Children's Educational Achievement," *Economic Inquiry*.
- SIPP; children of job losers vs children of employed parents × state maximum weekly UI benefit. A 1% higher maximum benefit →
  about 1.1% lower probability of grade repetition, concentrated in low- and middle-income families.
  ([Montana State research brief](http://www.montana.edu/regecon/publications/childrenseducationalachievement/))
- Volume and pages, and an alternative magnitude (0.03 pp) quoted on an FGCU listing: **UNVERIFIED**.
- *Overlap:* **substantial** on "UI buffers children against parental job loss" (short run, US).

**Lindo, Regmi & Swensen (2025)**, "Stable Income, Stable Family," *REStat* 107(3): 653–667 (IZA DP 15267).
- SIPP 1993–2008 panels × state UI maximum benefits. Higher maximum benefits mitigate the effects of layoffs: smaller increases
  in divorce and smaller falls in fertility after men's layoffs. ([IZA](https://www.iza.org/publications/dp/15267))
- *Overlap:* **substantial** on "the safety net as insurance of family structure after husbands' job loss". No children's
  outcomes, no race split found.

**Dettling & Kearney (2023)**, "The Cyclicality of Births and Babies' Health, Revisited: Evidence from Unemployment Insurance,"
NBER WP 30937.
- As potential UI replacement rates approach 100%, the effects of the unemployment rate on fertility and on infant health
  disappear. ([NBER w30937](https://www.nber.org/papers/w30937))
- A secondary summary reports the low-birth-weight result is significant only for Black mothers: **UNVERIFIED** in the paper.
- *Overlap:* partial (UI as insurance at births).

**Hendren & Sprung-Keyser (2020)**, "A Unified Welfare Analysis of Government Policies," *QJE* 135(3): 1209–1318.
- 133 policies. Child health and education policies have the largest MVPFs. Adult policies have MVPFs of about 0.5–2 unless they
  spill over to children. ([Harvard page](https://hendren.scholars.harvard.edu/publications/unified-welfare-analysis-government-policies);
  [QJE PAR](https://par.nsf.gov/servlets/purl/10237586))
- *Overlap:* framework for scoring UI/floor counterfactuals with children's earnings included.

**Parolin (2021)**, *Socio-Economic Review* (online 2019, doi 10.1093/ser/mwz025).
- States with larger Black population shares spend less TANF money on cash. Equalizing would cut the Black–White child poverty
  gap by up to 15%. ([WP PDF](https://medialibrary.uantwerpen.be/oldcontent/container2601/files/CSBWP2018/CSBWP2018_04.pdf);
  [CBPP citing it](https://www.cbpp.org/research/income-security/study-shows-why-tanf-is-not-the-success-that-some-claim))
- *Overlap:* partial. Racial differences in the generosity of the competing insurance.

**Akee, Copeland, Keeler, Angold & Costello (2010)**, "Parents' Incomes and Children's Outcomes: A Quasi-Experiment Using
Transfer Payments from Casino Profits," *AEJ: Applied* 2(1): 86–115.
- Unconditional tribal transfers. For the poorest households, $4,000 a year → about one more year of schooling at 21 and 22%
  fewer minor offenses at 16–17. ([HKS](https://www.hks.harvard.edu/publications/parents-incomes-and-childrens-outcomes-quasi-experiment-using-transfer-payments-casino))
- *Overlap:* partial (money channel).

**Long-run safety-net exposure and the IGE.** See `safety_net_ige.md` §1.1–1.2 (Hoynes–Schanzenbach–Almond 2016;
Bailey–Hoynes–Rossin-Slater–Walker 2024; Bastian–Michelmore 2018; McInnis et al.; Akee–Jones–Simeonova 2022; Hartley–Lamarche–
Ziliak 2022; Chetty et al. 2014). None of them studies the safety net **as insurance against a parent's job loss**, or
interacts it with the spouse's response.

**Herbst (2017)**, "Are Parental Welfare Work Requirements Good for Disadvantaged Children? Evidence from Age-of-Youngest-Child
Exemptions," *JPAM* 36(2): 327–357 (IZA DP 8485).
- **State age-of-youngest-child exemptions instrument first-year maternal employment**, using the ECLS-B.
- Large **negative** effects of maternal employment on children's cognitive and social-emotional outcomes. Working mothers have
  more depressive symptoms, breastfeed and read less, and use non-parental care earlier.
  ([IDEAS](https://ideas.repec.org/a/wly/jpamgt/v36y2017i2p327-357.html))
- *Overlap:* **substantial with our Design B** (the exemption design).

---

## Strand 5. Structural and quantitative models linking parental labor-market risk to child investment and mobility

**Caucutt & Lochner (2020)**, "Early and Late Human Capital Investments, Borrowing Constraints, and the Family," *JPE* 128(3):
1065–1147.
- Dynastic human capital model with borrowing constraints **and uninsured labor market risk**, calibrated to NLSY79 Children.
  Removing all lifecycle borrowing limits strongly raises investment, earnings and mobility.
  ([NBER w18493](https://www.nber.org/papers/w18493))
- *Overlap:* partial. Has earnings risk and children; no spouse, no search friction, no race, no safety-net floor.

**Lee & Seshadri (2019)**, "On the Intergenerational Transmission of Economic Status," *JPE* 127(2): 855–921.
- Lifecycle and intergenerational Becker–Tomes model with incomplete markets and transfer programs; matches the IGE of earnings,
  college and wealth. Early investment by young, constrained parents drives persistence.
  ([IDEAS](https://ideas.repec.org/a/ucp/jpolec/doi10.1086-700765.html))
- *Overlap:* partial (model-implied IGE; no spouse, no race, no friction).

**Abbott, Gallipoli, Meghir & Violante (2019)**, "Education Policy and Intergenerational Transfers in Equilibrium," *JPE* 127(6):
2569–2624.
- OLG lifecycle model of education, labor supply and saving with parental transfers. Aid crowds out transfers.
  ([UCL Discovery](https://discovery.ucl.ac.uk/id/eprint/10089197/))
- *Overlap:* partial (late investments; no early childhood, no spousal risk).

**Daruich (2018; forthcoming JPE per a 2026 roundup)**, "The Macroeconomic Consequences of Early Childhood Development Policies,"
FRB St. Louis WP 2018-029.
- GE heterogeneous-agent OLG model with **earnings risk** and credit constraints, and early investments of parental time and
  money. A permanent program gives about a 10% welfare gain.
  ([IDEAS](https://ideas.repec.org/p/fip/fedlwp/2018-029.html))
- Publication status: **UNVERIFIED** beyond the National Affairs note.
- *Overlap:* partial.

**Boar (2021)**, "Dynastic Precautionary Savings," *REStud* 88(6): 2735–2765.
- PSID parent–child pairs. Parents' consumption responds to their children's permanent income risk (WP: elasticity −0.08 to
  −0.06); an OLG model with altruism and strategic interaction. ([NBER w26635](https://www.nber.org/papers/w26635))
- *Overlap:* partial. Risk across generations, the reverse direction (children's risk → parents' saving).

**Agostinelli & Sorrenti (2018, v3 2022)**, "Money vs. Time: Family Income, Maternal Labor Supply, and Child Development," HCEO WP
2018-017.
- 1990s EITC expansions. The money–time trade-off is strongest for disadvantaged mothers.
  ([HCEO PDF](https://humcap.uchicago.edu/RePEc/hka/wpaper/Agostinelli_Sorrenti_2018_money-vs-time_v3.pdf))
- The IV magnitudes (+4.4% sd per $1,000; about −6% sd per 100 hours) come from a seminar abstract
  ([CERGE](https://cz.cerge-ei.cz/applied-micro/2019-02-11/giuseppe-sorrenti)), not the paper: **UNVERIFIED in the paper**.
- *Overlap:* **substantial with the companion "Money or Time?" paper.** Partial for the insurance paper.

**Boerma & Karabarbounis (2023)**, "Reparations and Persistent Racial Wealth Gaps," *NBER Macroeconomics Annual 2022*, vol. 37,
pp. 171–221.
- A dynastic model with exclusion of Black dynasties from labor and capital markets reproduces racial gaps in wealth, income,
  entrepreneurship and mobility. One-off wealth transfers do not produce long-run convergence.
  ([NBER chapter](https://www.nber.org/books-and-chapters/nber-macroeconomics-annual-2022-volume-37/reparations-and-persistent-racial-wealth-gaps))
- *Overlap:* partial (race + dynasty; no spouse, no child investment, no labor-market search friction).

**Lo Bello (2022)**, "Like Father, Like Son: Occupational Choice, Intergenerational Persistence and Misallocation," *Quantitative
Economics*.
- Occupational choice with search frictions; parental networks account for 79% of persistence.
  ([Wiley](https://onlinelibrary.wiley.com/doi/full/10.3982/QE1375))
- *Overlap:* partial (search friction in the child's market, not the mother's).

**Birinci** (Strand 3) and **Mankart–Oikonomou** (Strand 3): parents' side with friction and spousal insurance, no children.

**From the earlier notes:** Gayle–Golan–Soytas 2015 (race, marriage, children; risk-neutral with no saving, and "ignore the
insurance aspects of marriage and divorce"), Del Boca–Flinn–Wiswall 2014, BFHO 2024 (`literature_notes.md`). Mullins (2025),
Daruich–Fernández (2024), Low–Meghir–Pistaferri–Voena (2025), Keane–Wolpin (2010), Chan (2013) (`safety_net_ige.md` §1.3).

**Searched for and not found:** a structural model that has, together, (i) a search friction for the mother, (ii) husbands'
employment risk, (iii) a safety-net floor, (iv) marriage and fertility and (v) a child outcome, estimated by race. An extended
search for "parental unemployment risk + child investment + search friction" returned no such model.

---

## Strand 6. Race-specific consequences and the racial mobility gap

- **Chetty, Hendren, Jones & Porter (2020)**, *QJE* 135(2): 711–783. See `literature_notes.md`. At a given parental income the
  gap is among men (wages and employment); local Black father presence matters for Black boys.
  ([IDEAS](https://ideas.repec.org/a/oup/qjecon/v135y2020i2p711-783..html))
- **Chetty, Dobbie, Goldman, Porter & Yang (2024)**, "Changing Opportunity: Sociological Mechanisms Underlying Growing Class Gaps
  and Shrinking Race Gaps in Economic Mobility," NBER WP 32697 (listed as forthcoming in *QJE* 2026).
  - White–Black gaps for low-income children shrank by about 30% (cohorts 1978–92).
  - Children's outcomes track **parental employment rates in their community** (race × class × county), with larger effects
    for younger movers and for peers in the same cohort.
    ([Opportunity Insights](https://opportunityinsights.org/paper/changingopportunity/);
    [WCEG](https://equitablegrowth.org/working-papers/changing-opportunity-sociological-mechanisms-underlying-growing-class-gaps-and-shrinking-race-gaps-in-economic-mobility/))
  - *Overlap:* **partial and important.** A community-level parental-employment channel competes with our household-level
    father's job loss channel.
- **Binder, Walker, Eggleston & Murray-Close**, "Race, Class, and Mobility in U.S. Marriage Markets" (Census CES WP 22-59;
  AEA 2024 session).
  - At equal childhood family income, Black women obtain 60% less income from a partner than White women; marriage-market
    dynamics account for 84–90% of the family-income mobility gap.
    ([Census CES-WP-22-59](https://www.census.gov/library/working-papers/2022/adrm/CES-WP-22-59.html);
    [AEA 2024](https://www.aeaweb.org/conference/2024/program/paper/bRQrYK33))
  - *Overlap:* partial. The next generation's Black mothers again face low and risky partner income.
- **Bayer & Charles (2018)**, "Divergent Paths: A New Perspective on Earnings Differences Between Black and White Men Since
  1940," *QJE* 133(3): 1459–1501.
  - The median Black man's rank has been flat since 1940, and the level gap is back to 1950 size. Non-workers are included.
    ([IDEAS](https://ideas.repec.org/a/oup/qjecon/v133y2018i3p1459-1501..html))
  - *Overlap:* motivates husbands' employment risk by race.
- **Derenoncourt (2022)**, "Can You Move to Opportunity? Evidence from the Great Migration," *AER* 112(2): 369–408.
  - Great Migration composition shocks explain about 27% of today's regional racial mobility gap.
    ([AEA](https://www.aeaweb.org/doi/10.1257/aer.20200002))
  - *Overlap:* none on mechanism (neighbourhood channel).
- **Hardy (2014)**, "Childhood Income Volatility and Adult Outcomes," *Demography* 51(5): 1641–1665.
  - **PSID** intergenerational links. Volatility has a small positive association with high-school dropout, driven by
    lower-income households, and matters less than permanent income.
    ([UKCPR](https://cpr.uky.edu/research/inequality/childhood-income-volatility-and-adult-outcomes))
  - *Overlap:* partial (income risk in childhood → adult outcomes in the PSID).
- **Torche, Fletcher & Brand (2024)**, "Disparate Effects of Disruptive Events on Children," *RSF* 10(1): 1–30.
  - Special-issue introduction. It reports **no** race-specific finding on parental job loss and warns that racial differences
    in estimated effects can reflect selection into job loss. ([RSF](https://www.rsfjournal.org/content/10/1/1))
- **Kalil & Wightman (2011)**, **PSL (2009)** and **Stevens & Schaller (2011)**: see Strand 1. These are the only race-split
  estimates of parental job loss found. They are mixed: stronger for Black children, larger but insignificant, and no
  difference, respectively.

---

## Closest neighbours (ranked)

1. **Page, Stevens & Lindo (2009).**
   - *What we would also do:* PSID head's displacement → children's adult income, earnings, schooling and welfare receipt, with
     a Black subgroup and a younger-child interaction.
   - *What they do not do:* mothers' labor supply response, safety-net variation, the IGE or the race gap at a given parental
     income, modern cohorts (born after the mid-1970s), a model. Their Black estimates are insignificant (N = 476), and their
     main effect disappears with closures only.
2. **Regmi & Henderson (2019, EER).**
   - *What we would also do:* gender-specific state Bartik at the birth year → children's PIAT/PPVT in the NLSY79 CYA, married
     vs unmarried, by race.
   - *What they do not do:* the **cross effect** of men's demand on mothers' weeks worked (the insurance margin), maternal time
     as a mediator, adult outcomes or the IGE, safety-net interactions, a model. Their Black estimates are null.
3. **Kalil & Wightman (2011).**
   - *What we would also do:* PSID parental job loss × race → education; wealth and long-term unemployment as explanations.
   - *What they do not do:* causal design, adult earnings or the IGE, the mother's response, the safety net, a model.
4. **Page, Schaller & Simon (2019, JHR)**, with **Lindo, Schaller & Hansen (2018)**.
   - *What we would also do:* opposite-signed child effects of men's vs women's demand shocks, interpreted as income vs maternal
     time.
   - *What they do not do:* labor supply at births, long-run outcomes, race heterogeneity, the safety net, a model.
5. **Oreopoulos, Page & Stevens (2008)**, read with **Hilger (2016)** as the US counterpoint.
   - *What we would also do:* father's displacement → children's adult earnings and transfer receipt, concentrated at low income.
   - *What they do not do:* race, the mother's response, safety-net variation, early childhood (Hilger: ages 12+), a model.
6. **Birinci (WP 2019–2026).**
   - *What we would also do:* a model with a frictional labor market, family labor supply as insurance against displacement,
     and transfers that crowd it out; optimal transfer design.
   - *What it does not do:* children, the IGE, race, marriage or fertility, births.
7. **Halla, Schmieder & Weber (2020)**, together with **Cullen & Gruber (2000)** and **Stephens (2002)**.
   - *What we would also do:* husband's displacement → wife's labor supply; public vs spousal insurance; young children
     dampening the response.
   - *What they do not do:* children's outcomes, race, a model linking insurance to the next generation.
8. **Gayle, Golan & Soytas (2015).**
   - *What we would also do:* a race-specific structural model with marriage, fertility, parental time and children's
     education, plus counterfactuals that give Black families White primitives.
   - *What they do not do:* risk, saving, search friction, the safety net. They explicitly ignore insurance.

Next tier: Regmi (2018) and Lindo–Regmi–Swensen (2025) (UI buffers job loss for children and families); Britto–Melo–Sampaio (UI
RD, Brazil); Carneiro et al. (2022) (timing and family adjustment); Rege et al. (2011) (the maternal-time mediator rejected);
Herbst (2017) (exemption IV for first-year maternal employment).

---

## What is still open

**The gap, stated precisely.** No paper (i) estimates how the **husband's job-loss risk** moves the **mother's labor supply
around a birth**, (ii) traces that insurance response, its **crowd-out by the safety net** and the **father's job loss**
itself to **children's adult outcomes, the IGE and the Black–White gap at a given parental income**, and (iii) does so in a
**structural model** that has a search friction for the mother, husbands' employment risk, a safety-net floor, marriage,
fertility and human capital accumulation, estimated by race.

The pieces exist separately:
- the effects of fathers' job loss on children (Strand 1);
- gender-specific shocks and child outcomes (Strand 2);
- spousal insurance and its crowd-out by UI and transfers, without children (Strand 3; Birinci has the friction);
- UI buffering children or families after job loss (Regmi; Lindo–Regmi–Swensen; Britto et al.);
- dynastic models with earnings risk but no spouse or race (Strand 5), and race with no risk (GGS).

**Novelty claims the paper can safely make** (conditional on the results holding):
1. The first estimate of the **cross-gender insurance margin at births**: men's-industry slack raises married mothers'
   post-birth employment. PSS, LSH and Regmi–Henderson use gender-specific shocks for child outcomes or own-gender first stages
   only; Stephens and Halla et al. study wives after displacement, not around births.
2. The first evidence on whether the **safety net crowds out mothers' insurance work at births**, for example men's Bartik ×
   married × state UI/AFDC generosity. Cullen–Gruber, Birinci and Halla et al. show crowd-out for wives in general, without
   children's outcomes.
3. The first **race-specific** analysis of the insurance chain (husband's risk → wife's response → children), with a model that
   separates husbands' employment risk, mothers' search friction and the safety net as causes of the gap at a given parental
   income.
4. The first structural model that nests spousal insurance under a search friction (Birinci's parent side) inside a
   two-generation model with race, marriage and fertility, and so can run counterfactuals such as "White husbands' risk", "White
   search friction", or "UI vs floor" on the IGE and on the steady-state racial gap.

**Claims we must NOT make**
- That we are the first to show a father's job loss lowers children's adult earnings or education (OPS 2008; PSL 2009 in the
  **PSID**; Uguccioni; Huttunen–Riukula; Gregg et al.; Coelli; Pan–Ost; Stuart for community shocks).
- That we are the first to study father's job loss **by race in the PSID** (PSL 2009; Kalil–Wightman 2011).
- That a father's job loss *causes* the −0.21 earnings loss for Black children. Ours uses zero hours, mixes layoffs, quits and
  disability, and includes stepfathers and partners. PSL show layoff-inclusive effects vanish with closures only; Hilger finds
  small US effects of layoffs; Charles–Stephens show layoffs are selected.
- That the father's job loss is "the strongest" determinant. It is the strongest *correlate* in our table, conditional on
  parental income. Chetty et al. (2024) point to community parental employment, Uguccioni to neighbourhood moves, Rege et al.
  and Carneiro et al. to stress.
- That **mothers' employment in the first year does no harm**. Ours is an association. Herbst (2017) finds sizable negative
  effects using the exemption IV, Willage–Willén find that an involuntary loss of the mother's job postpartum harms children, and
  Agostinelli–Sorrenti find a money–time trade-off.
- That the mother's insurance work mitigates the harm of the father's job loss. Rege et al. reject the maternal-time mediator
  for school performance in Norway; Halla et al. find wives replace only a tiny share of lost income.
- That we are the first to use **gender-specific labor-demand shocks** for children's outcomes (PSS 2019; LSH 2018;
  Regmi–Henderson 2019; Schaller 2016; ADH 2019).
- That we are the first to show the safety net/UI **crowds out spousal labor supply** (Cullen–Gruber 2000; Birinci) or
  **buffers children/families** after job loss (Regmi 2018; Lindo–Regmi–Swensen 2025; Britto et al. 2022; Dettling–Kearney
  2023; Schaller–Zerpa on Medicaid).
- That we are the first to use **age-of-youngest-child exemptions** to move first-year maternal employment (Herbst 2017).
- That Black mothers' higher employment *is* insurance against husbands' risk without testing it against norms (Boustan–Collins
  2014) and against the search friction (Smith–Mattingly 2014: Black wives search more but did not find work more often in
  2008–09).
- Any claim that our first stage differs by race. It does not (ur × black p=0.786; Bartik × black p ≥ 0.18).

---

## Implications for design

**Redundant with existing work** (keep only as replication, robustness or appendix):
1. *PSID father's job loss → child's adult earnings, pooled*: done by PSL (2009) and Kalil–Wightman (2011). A new version adds
   value only with (a) displacement defined by the PSID reason-for-job-loss item (plant closed vs laid off/fired), (b) cohorts
   born up to the 1990s, (c) results at fixed parental income ranks by race, and (d) an event-study on parents' income and the
   mother's hours.
2. *Gender-specific Bartik at birth → NLSY79 CYA test scores*: done by Regmi–Henderson (2019), with a null for Black children.
   Replicate it as a check on our Bartik and say so.
3. *Exemption → first-year maternal employment → child scores*: done by Herbst (2017) with the ECLS-B. Design B
   (`safety_net_ige.md`) is new only in (a) the race split, (b) single vs married mothers as a placebo or triple difference, and
   (c) its use as a validation target for the model.
4. *UI generosity buffers children's short-run outcomes after parental job loss*: Regmi (2018), SIPP. Design D adds the long
   run, the mother's response and race. Otherwise it is a replication.
5. *Average added-worker effect in the PSID*: Stephens (2002).

**New**
1. **The insurance margin at births.** Men's-industry Bartik × married → the mother's employment at b+1…b+3 (our first stage
   already shows it). Extend it to weeks and months not working in year 1 (NLSY79 weekly arrays), CPS for power, and husbands'
   own displacement in the PSID (wife's hours around births).
2. **Crowd-out at births.** Interact (1) with state UI generosity (DOL data, not on disk) and AFDC/TANF levels (UKCPR). The
   prediction is a weaker insurance response where the floor is high (Cullen–Gruber, Birinci), applied to mothers of newborns.
3. **The full chain, by race.**
   - Black husbands' displacement risk is higher (Wrigley-Field–Seltzer; Couch–Fairlie).
   - Black mothers' search friction: Smith–Mattingly show search without success. This is what the companion model's search
     friction captures.
   - Black families' safety net is less generous (Parolin).
   - Black children's outcomes respond more to the father's job loss (Kalil–Wightman, our PSID association).
   No paper puts these together.
4. **Mediation that the literature has not done in the US.** Does the mother's insurance work after the father's job loss offset
   or deepen the harm to the child? Test it in the PSID (mother's hours after the husband's displacement × child outcomes) and
   cite Rege et al. as the Norwegian null.
5. **Structural counterfactuals on the IGE and the racial gap at a given parental income**: give Black families White husbands'
   employment risk, the White search friction or White safety-net generosity; replace the floor with UI for husbands; move to
   employment-tested transfers (Birinci's optimal policy, now scored on children).

**Choices that would sharpen the contribution**
- **Displacement definition.** Report closure-only and layoff-inclusive results separately (PSL, Hilger, Charles–Stephens). Do
  not lead with "zero hours".
- **Race.** Pre-register the race contrasts (insurance response, crowd-out, child effect), with power calculations. Prior
  race-split results are mixed and small-sample.
- **Intergenerational outcomes.** Use log IGE with the reliability correction and Chetty-style ranks at p25/p75 (from
  `literature_notes.md`), not only test scores. This is where the literature is thinnest (PSL is the only US PSID attempt).
- **Combine the two insurance sources in one design**, for example men's Bartik × married × UI generosity, or the husband's
  displacement × state UI. Every existing paper varies one source at a time.
- **Separate the household channel from the community channel** (Chetty et al. 2024). Control for, or use, local parental
  employment by race; the gender-specific Bartik is itself a community shock.
- **Timing.** Exposure at 0–5 vs later (Uguccioni; PSL; Carneiro et al.). The insurance margin bites at births, and the model's
  child-penalty and human capital accumulation blocks are age-specific.
- **Model.** Keep the companion model's search friction and husbands' employment risk, and add a child outcome (the
  `literature_notes.md` Phase 4 block). Use the reduced-form estimates as untargeted validation: the cross-gender first stage,
  the exemption first stage, and the UI interaction.
