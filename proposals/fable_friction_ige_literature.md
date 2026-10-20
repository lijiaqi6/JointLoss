# Does search friction in either generation contribute to the IGE literature without the race focus? (Fable, 2026-10-19)

PI's question (verbatim): "so even without race focus, does search friction faced by father, mother or sons will
contribute to the IGE literature meaningfully?"

Read: `EVIDENCE.md` 11.19-11.27, `sec7_model.tex` "Search frictions in two generations", `output/shared_friction.md`
(all sections), `output/friction_generations.md`, `output/father_displacement.md`, `output/income_vs_earnings_ige.md`,
`proposals/fable_search_friction_ige.md`. Nothing was run; every repo number below is from a saved output. References
were checked on the web where marked [v]; [m] = from memory, confident; [?] = unsure, check before citing.

## 0. Short answer

Yes, but as an **accounting paper**, not as a mechanism paper, and only if three things are added. What the repo has
is, to my knowledge, the first exact decomposition of the IGE (wage, hours, earnings, by age of the son) into the
paths through the father's employment instability, the son's own, and the part that runs through both. The
literature has (a) causal effects of a parent's job loss on children, (b) father-son correlations of unemployment of
about 0.10 in the UK, Norway, Canada and Germany, and (c) mediation of the IGE by the son's "labour market
attachment" at one age in one UK cohort. It does not have the IGE share by generation and by age, it does not have the
earnings-versus-wage split of that share, and it does not have the result that the friction-driven part of parental
income is at least as persistent as the rest (the opposite of Shea 2000's reading of "luck" income). Those three are
new. The shared father-to-son path (2-3% of the wage IGE, 5-6% of the earnings IGE at 25-29, 0.005*** and 0.010***)
is a precise share of the level of persistence and should be reported as such; it is not a headline on its own.

What would make it a paper rather than an appendix: (1) the friction-driven parental income result confirmed with
plant closures only and in a second data set; (2) the mother's instability added, so that the 48% of Black sons and
13% of White sons without a resident father are in the sample instead of out of it; (3) the age profile of the son's
own employment channel (13-28% of the IGE at 25-29, 2-3% at 45-49) replicated in the NLSY79's weekly arrays, which
measure spells far better than the PSID's annual flags. If (1)-(3) hold, it is a self-contained descriptive paper for a
field journal (Labour Economics, JHR, Journal of Population Economics), and it is independent of race. If they do not,
it is the current Section 8 paragraph plus an appendix table.

## 1. Literature map

### (a) Parental job loss and children's long-run outcomes

- Oreopoulos, Page and Stevens (2008), "The intergenerational effects of worker displacement", *JOLE* 26(3), 455-483
  [v]. Canadian tax data, fathers displaced by firm closures; sons' adult earnings about 9% lower, more UI and social
  assistance receipt; driven by the bottom of the family-income distribution. The benchmark causal paper.
- Hilger (2016), "Parental job loss and children's long-term outcomes: evidence from 7 million fathers' layoffs",
  *AEJ: Applied* 8(1), 247-283 [v]. US tax data; layoffs cut family income sharply but reduce college enrollment,
  college quality and early earnings only slightly; closure-based estimates larger because of selection.
- Page, Stevens and Lindo (2009), "Parental income shocks and outcomes of disadvantaged youth in the United States",
  in Gruber (ed.), *The Problems of Disadvantaged Youth*, Chicago UP, 213-235 [v]. PSID; estimates sensitive to the
  displacement definition; with the least endogenous measures, substantive long-run effects for low-income families,
  largest for young children.
- Shea (2000), "Does parents' money matter?", *JPubE* 77(2), 155-184 [v]. PSID; parental income variation from union,
  industry and job loss ("luck") has a negligible effect on children's human capital except when the father has low
  education. Directly relevant: the repo's result that friction-predicted parental income is at least as persistent
  as the rest is the opposite finding on the same data set (Section 2).
- Coelli (2011), "Parental job loss and the education enrollment of youth", *Labour Economics* 18(1), 25-35 [v].
  Canada; job loss around high-school completion lowers post-secondary enrollment.
- Stevens and Schaller (2011), "Short-run effects of parental job loss on children's academic achievement",
  *Economics of Education Review* 30(2), 289-299 [v]. SIPP; grade retention +0.8 pp (about 15%), child fixed effects.
- Rege, Telle and Votruba (2011), "Parental job loss and children's school performance", *REStud* 78(4), 1462-1489
  [v]. Norway, plant closures; the father's loss lowers school performance, the mother's does not (non-significant
  increase); the father's effect is not explained by income, employment, maternal time, divorce or moves.
- Bratberg, Nilsen and Vaage (2008), "Job losses and child outcomes", *Labour Economics* 15(4), 591-603 [v]. Norway;
  no significant effect of the father's displacement on children's earnings.
- Gregg, Macmillan and Nasim (2012), "The impact of fathers' job loss during the recession of the 1980s on their
  children's educational attainment and labour market outcomes", *Fiscal Studies* 33(2), 237-264 [v]. BCS70; half a
  GCSE at A*-C, about 2% lower adult wages.
- Lindo (2011), "Parental job loss and infant health", *JHE* 30(5), 869-879 [v] (PSID; birth weight -4.5%); Lindo
  (2010), "Are children really inferior goods?", *JHR* [m] (fertility after displacement).
- Huttunen and Kellokumpu (2016), "The effect of job displacement on couples' fertility decisions", *JOLE* 34(2) [v]
  (Finland; the mother's loss lowers fertility, the father's does not); Huttunen and Riukula, "Parental job loss and
  children's careers" (IZA/working paper) [? authorship verified only from a repository abstract]: the father's loss
  lowers the child's chance of entering the father's field or plant and lowers earnings.
- Mork, Sjogren and Svaleryd (2019 IZA DP 12559; journal version [?]) [v]: Sweden; parental job loss hurts the
  parents, not the children's health, schooling or early-adult outcomes.
- Britto, Melo and Sampaio (2022, IZA DP 15591 / CEPR DP17562), "The kids aren't alright" [v]: Brazil; dropout and
  crime rise; UI mitigates.
- Chetty, Dobbie, Goldman, Porter and Yang (2024), "Changing opportunity", NBER WP 32697 [v]: the parental employment
  rate of a child's race-by-class-by-county community predicts the child's adult outcomes, with a quasi-experimental
  design on movers; the mechanism is peers' parents' employment. This is the closest the recent US literature comes to
  "parents' employment as a cause of persistence", and it is at the community level, not the family level.

Summary of (a): causal effects of a father's job loss on children range from zero (Norway, Sweden) through small (US
tax data) to 9% of earnings (Canada), concentrated in low-income families; mothers' losses do not harm children in the
two studies that separate them. None of these papers asks what share of the IGE the father's instability carries.

### (b) Intergenerational transmission of unemployment / worklessness

- O'Neill and Sweetman (1998), "Intergenerational mobility in Britain: evidence from unemployment patterns", *Oxford
  Bulletin of Economics and Statistics* [m]. NCDS; sons of unemployed fathers are more often unemployed.
- Corak, Gustafsson and Osterberg (2004), "Intergenerational influences on the receipt of unemployment insurance in
  Canada and Sweden", in Corak (ed.), *Generational Income Mobility in North America and Europe*, CUP (IZA DP 184,
  2000) [v]. Father-son UI-claim correlations of about 0.10; the parental history matters in Canada, not Sweden.
- Ekhaugen (2009), "Extracting the causal component from the intergenerational correlation in unemployment",
  *Journal of Population Economics* 22(1), 97-113 [v]. Norway, sibling differences; a substantial correlation, half
  of it observed family background; the causal part is non-significantly negative.
- Macmillan (2014), "Intergenerational worklessness in the UK and the role of local labour markets", *Oxford Economic
  Papers* 66(3), 871-889 [v]. Sons of workless fathers spend 7-11% more of their time out of work to age 23; the
  link is not shared local conditions but is stronger where the son's labour market is weak.
- Mader, Muller, Riphahn and Schwientek (2015), "Intergenerational transmission of unemployment: evidence for German
  sons", *Jahrbucher fur Nationalokonomie und Statistik* 235(4-5), 355-375 [v]. Positive correlations; IV (mass
  layoffs) and Gottschalk's method give no causal effect.
- Dahl, Kostol and Mogstad (2014), "Family welfare cultures", *QJE* [m]; Hartley, Lamarche and Ziliak (2022),
  "Welfare reform and the intergenerational transmission of dependence", *JPE* 130(3), 523-565 [v]: the adjacent
  programme-participation literature; HLZ is on the PSID (mother-daughter AFDC/TANF; +25 pp, halved by reform).

Summary of (b): the father-son correlation of unemployment or worklessness is about 0.10 wherever it is measured, and
the causal part is small or zero once family background is held fixed. The repo's 0.103*** (White) and 0.114***
(Black) for the son's unemployment share on the father's are in line, and I know of no published US (PSID) estimate
of this correlation for sons' careers; that alone is a usable descriptive fact [? check Mazumder's and Corak's surveys
before claiming it is the first].

### (c) Decompositions of the IGE; earnings vs wages vs employment; life-cycle bias

- Blanden, Gregg and Macmillan (2007), "Accounting for intergenerational income persistence: noncognitive skills,
  ability and education", *EJ* 117(519), C43-C60 [v]. BCS70 at age 30; mediators are cognitive and non-cognitive
  skills, education and labour market attachment (months unemployed / out of work); the mediators account for over
  80% of the rise in persistence between the 1958 and 1970 cohorts. I do not have the share attributed to attachment
  alone [? read the paper's Table before stating a number]. This is the one precedent for "the son's own friction as a
  mediator of the IGE"; it is one age, one cohort, and the mediator is in levels, not by age.
- Gregg, Jonsson, Macmillan and Mood (2017), "The role of education for intergenerational income mobility: a
  comparison of the United States, Great Britain, and Sweden", *Social Forces* [m, ? on whether attachment is in it].
- Bowles and Gintis (2002), "The inheritance of inequality", *JEP* [m]; Rothstein (2019), "Inequality of educational
  opportunity? Schools as mediators of the intergenerational transmission of income", *JOLE* [m]: the US mediation
  literature works through skills, schooling and places, not through employment instability.
- Haider and Solon (2006), *AER*; Lee and Solon (2009), *REStat*; Mazumder (2005), *REStat*; Nybom and Stuhler (2016),
  "Heterogeneous income profiles and lifecycle bias in intergenerational mobility estimation", *JHR* [m, all]. The
  IGE rises with the son's age because early wages understate lifetime differences. The repo's finding that the
  son's own friction carries 13% of the wage IGE and 28% of the earnings IGE at 25-29 and 2-3% at 45-49 says that the
  young IGE is partly an employment-instability statistic; the ages used by Chetty, Hendren, Kline and Saez (2014,
  *QJE*; children at 29-32) [m] and most administrative-data studies are inside that range.
- Mitnik, Bryant, Weber and Grusky (2015), *New Estimates of Intergenerational Mobility Using Administrative Data*,
  IRS SOI working paper [v]; Mitnik and Grusky (2020), "The intergenerational elasticity of what? The case for
  redefining the IGE", *Demography* [m]: the choice of outcome (family income, earnings, with or without zeros) moves
  the IGE; they do not decompose the difference into employment and wages. Chetty, Hendren, Jones and Porter (2020),
  *QJE* [m]: Black-White gaps are in men's employment as much as in wages.
- Carneiro, Garcia, Salvanes and Tominey (2021), "Intergenerational mobility and the timing of parental income",
  *JPE* [m]: the timing of parental income within childhood matters; the repo's windowed father shares speak to the
  same object.

Summary of (c): the IGE has been decomposed into skills, schooling, places and outcome definitions; the
wage-times-hours split by age of the son, with the son's instability as the hours part, is not in this list.

### (d) Search frictions, networks, employers and intergenerational mobility

- Corak and Piraino (2011), "The intergenerational transmission of employers", *JOLE* 29(1), 37-68 [v]: 40% of
  Canadian sons have worked for their father's employer, 6-9% in adulthood; rises with the father's earnings and
  drives the top nonlinearity of the IGE. Bingley, Corak and Westergard-Nielsen (2012), in Ermisch, Jantti and
  Smeeding (eds.), *From Parents to Children* [m, ? exact chapter]: Denmark 30-40%, same pattern.
- Kramarz and Nordstrom Skans (2014), "When strong ties are strong: networks and youth labour market entry", *REStud*
  81(3), 1164-1200 [v]: parents' plants are where young Swedes with weak positions find first jobs.
- Staiger (2020-2024), "The intergenerational transmission of employers and the earnings of young workers", Census /
  Opportunity Insights working paper [v; versions differ: 7% / +31% in 2020, 29% by age 30 / +19% in 2022].
- Plug, van der Klaauw and Ziegler (2018), "Do parental networks pay off?", *SJE* 120(1), 268-295 [v]: WLS; parents'
  high-school friends do not help children's earnings (null).
- Magruder (2010), "Intergenerational networks, unemployment, and persistent inequality in South Africa", *AEJ:
  Applied* 2(1), 62-85 [v]: fathers help sons find work (about a third more employment), mothers do not.
- Calvo-Armengol and Jackson (2004), *AER* [m]: theory in which network-based job finding makes unemployment
  persistent within families and across generations; Loury (2006), *JOLE* [m]; Bayer, Ross and Topa (2008), *JPE*
  [m]; Hellerstein, McInerney and Neumark (2011), *JOLE* [m]: referral and neighbourhood networks in the US.
- Repo (Section 8, NLSY79): jobs found through friends or relatives grow more slowly (-0.014***, s.e. 0.004) and carry
  0.001** of the parental-income gradient.

Summary of (d): this literature is about access (employers, referrals) and it is where "search friction" and the IGE
already meet. It says parents transmit employers and first jobs; it does not say parents transmit the friction itself
(the spells), which is what the repo measures.

### (e) Mothers' labour supply as a channel

- Added-worker effect: Lundberg (1985), *JOLE* [m]; Stephens (2002), "Worker displacement and the added worker
  effect", *JOLE* [m] (PSID; wives' hours rise after the husband's displacement, mostly later and modestly); Blundell,
  Pistaferri and Saporta-Eksten (2016), *AER* [m]; Halla, Schmieder and Weber (2020), "Job displacement, family
  dynamics, and spousal labor supply", *AEJ: Applied* 12(4), 253-287 [v] (Austria; wives' response modest, through
  participation, strongest for mothers planning a return). Repo (`19.FatherDisplacement.py`): wife's hours +54**
  (s.e. 26, p=0.036) at e=+1 after the husband's displacement, against the head's -238*** (26).
- Maternal employment and children: Ruhm (2004), *JHR* [m]; Bernal (2008), *IER* [m]; Carneiro, Loken and Salvanes
  (2015), *JPE* [m]; Del Boca, Flinn and Wiswall (2014), *REStud* (in the repo's notes).
- Mothers and the next generation's labour supply: Fernandez, Fogli and Olivetti (2004), "Mothers and sons", *QJE*
  [m]; Morrill and Morrill (2013), "Intergenerational links in female labor force participation", *Labour Economics*
  20(1), 38-47 [v venue only].
- Hoynes, Miller and Schaller (2012), "Who suffers during recessions?", *JEP* [m]: men, the young, Black and Hispanic
  workers and the less educated bear cyclical job loss; Cajner, Radler, Ratner and Vidangos (2017), FEDS [? exact
  title] on racial gaps over the cycle.

Summary of (e): the mother's job loss does not harm children where it has been measured (Rege et al.; Huttunen and
Kellokumpu on fertility), the added-worker response is modest, and mothers are weaker job contacts (Magruder). No
paper puts the mother's instability into an IGE accounting; for father-absent families she is the only parent in
parental income, and those families are 48% of Black sons and 13% of White sons in the PSID (EVIDENCE 8.10).

## 2. Verdict

**Is it a meaningful contribution without race? Yes, as an accounting, with three results that are new; and no, as a
mechanism, because the literature already shows that the causal part of father-son unemployment is small and the repo's
own numbers say the same (the father's direct path at equal parental income is 0.000 to 0.024 for White sons, none
significant; -0.180** (s.e. 0.077, p=0.019) for the father's displacement share on Black sons' wages).**

What is new:

1. **The accounting itself.** An exact split of the IGE at each age band of the son into (i) the father's friction
   given income, (ii) the son's friction beyond his father's, (iii) the shared path, (iv) the rest, for wages, hours,
   earnings and earnings with zero-hours years, with cluster-bootstrap s.e. (`73.SharedFriction.py`). No paper in
   (a)-(e) has this. The numbers: son's own friction (all sons) carries 0.026*** (s.e. 0.005) of the White wage IGE of
   0.205*** at 25-29 (13%) and 0.008 (0.009, p=0.37) of 0.470*** at 45-49 (2%); in earnings 0.060*** (0.010) of
   0.218*** (28%) and 0.012 (0.015, p=0.42) of 0.457*** (3%). Black: 0.033*** (0.007) of 0.149*** (22%) and 0.007
   (0.012) of 0.140***; earnings 0.093*** (0.018) of 0.240*** (39%) and 0.011 (0.025). The channel fades by 45 for both
   races, and it is twice as large in earnings as in wages.
2. **The young IGE is partly an instability statistic.** Read with Haider-Solon and Lee-Solon: the IGE measured at
   25-34 (the age range of most administrative-data IGEs) contains an employment-instability component that lifetime
   measures do not. That is a concrete, quantified addition to the life-cycle-bias literature, independent of race.
3. **Friction-driven parental income is at least as persistent as the rest (the Shea contrast).** The father's three
   window shares explain 13.4%*** (s.e. 1.9) of the variance of White parental income and 18.6%*** (3.2) of Black
   (R2 at 25-29); the IGE on the friction-predicted part of parental income, b_P = (R2 b_P)/R2, is 0.033/0.134 = 0.25
   at 25-29 and 0.075/0.112 = 0.67 at 45-49 for White sons, against b_clean of 0.213*** and 0.452*** (R2 b_P
   0.033***, s.e. 0.009, and 0.075***, 0.021). For Black sons 0.056/0.186 = 0.30 at 25-29 (0.056***, 0.012) and
   0.047/0.245 = 0.19 at 45-49 (0.047, 0.030, p=0.12) against 0.152*** and 0.247***. Shea (2000) read job-loss-driven
   income variation as luck that does not transmit; on the same data with a windowed, multi-year measure it transmits
   fully for White sons and more with age. Whether that is because the father's instability acts on the son (OPS 2008)
   or because it marks the family (Ekhaugen 2009; Mader et al. 2015) is the identification question in Section 3; the
   fact is new either way.
4. **Father-to-son transmission of the friction, on US data, over the son's whole career.** Son in the top third of
   career friction if the father had a friction year in the window: +0.131*** (s.e. 0.020, White) and +0.123*** (0.031,
   Black); at equal parental income +0.092*** and +0.063** (p=0.048); son's unemployment share on the father's
   0.103*** and 0.114***; it survives state-at-17 FE and current state-by-year FE (White father's unemployment share
   0.096***, s.e. 0.037, p=0.009, in C1 column 4). This matches the 0.10 of the UK, Norway and Canada and, as far as I
   know, has no published PSID counterpart for careers to 55.

What is known and should be cited, not claimed: the parental-income gradient of the son's job finding out of work
(the PSID -0.022*** / -0.027***, NLSY79 -0.056*** / -0.061***) is the employment-rate gradient in parental income that
Chetty et al. (2014, 2020) show; the father-son correlation of about 0.10; the small causal effects of the father's job
loss (Hilger; Bratberg et al.; Mork et al.); the modest added-worker response.

What makes it a contribution rather than a footnote: the shared path alone (0.005***, p=0.005, 2% of the White wage
IGE; 0.010***, p=0.010, 5% of the earnings IGE; 3-9% with zero-hours years; no growth with age) is a precisely
estimated share of the level of persistence and belongs in a table, not an abstract. The abstract-level numbers are
(1)-(3): 13-28% of the young IGE is the son's instability and it is gone by 45; friction-driven parental income has an
IGE of 0.25-0.67 rather than zero. If (3) survives the closure-only and second-data-set checks below, it is the
headline.

## 3. Positioning

**Now:** keep the Section 8 paragraph in Paper B (it answers the race question: shared friction is a level, not the
racial rise; 5% of the gap in the opening, p=0.38) and move the full accounting table (A2 wage / hours / earnings,
E identity) to an appendix of Paper B. Paper B's question is the racial opening; the friction accounting is not about
race and should not grow inside it.

**Separate paper, conditional on Section 4's results:** "Employment instability in two generations and the
intergenerational elasticity of earnings."

One-paragraph pitch: The IGE is usually read as the persistence of pay. We decompose it, exactly and by the son's
age, into the paths that run through employment instability (years displaced, unemployed or without work) in the
father's generation, in the son's, and in both. In the PSID the son's own instability carries 13% of the wage IGE and
28% of the earnings IGE at 25-29 and 2-3% at 45-49, so the IGE measured in the late twenties, the age of most
administrative-data estimates, is in part an instability statistic that disappears over the career. The father's
instability during the son's childhood explains 13-19% of the variance of parental income, and the part of parental
income it predicts is at least as persistent as the rest (IGE 0.25 at 25-29, 0.67 at 45-49), the opposite of the
reading of job-loss income as non-transmitted luck. Instability passes from father to son (0.10-0.13), as in the UK,
Norway and Canada, but the path through both generations is 2-6% of the IGE and does not grow with age: fathers'
instability marks families more than it transmits spells. The mother's instability [result of C below] for the
families in which she is the only parent. The NLSY79's weekly work histories replicate the age profile [result of B].

Main figure: the IGE of earnings (and wages) by five-year band of the son, as a stacked area: rest; son's own
instability; shared; father's direct; with the hours IGE as a second panel. Main table: the E identity (b0 = (1-R2)
b_clean + R2 b_P) by band, with b_P and b_clean side by side, for wages and earnings.

Referee concerns and public-data answers:

1. *Friction is an outcome of skill, not a friction.* The accounting is descriptive and should say so (the repo
   already labels it). The answers: (i) separate the father's closures (the strict PSID measure: company folded /
   moved / went out of business; 3,269 closures) from layoffs, unemployment and zero hours, and show the b_P on
   closure-driven income alone; (ii) in the NLSY79, show that the son's friction share and its parental-income gradient
   survive AFQT and schooling (the repo's rule: if a control accounts for it, say so and stop); (iii) report the
   father's direct effect given income as the upper bound of "marking".
2. *Selection into wages.* Done: imputing zero-hours years at the last wage or at the race-band 10th percentile
   leaves the profiles within 0.03 (0.255*** / 0.283*** vs 0.274*** for the racial opening); earnings including
   zero-hours years are in A3. Report both outcomes throughout.
3. *Father-absent families are excluded.* The father-side results are on father-present sons (87% of White, 52% of
   Black); the son-only results are on all sons. The fix is C below: the resident parent's instability (mother or
   father), all sons, with father-presence as a split.
4. *The PSID measures mothers' unemployment badly.* The wife's annual hours unemployed and out of the labour force
   exist from 1976 [? verify the first wave], the job-end reason is asked of wives later than of heads [? verify],
   and a mother who becomes head at divorce changes variable. Two answers: measure the mother's instability as zero-
   hours and unemployment-hours years (not displacement), which are consistent for heads and wives; and run the
   mother's channel in the NLSY79 Children and Young Adults file, where the mother's weekly work history from 1978 is
   complete and the children are now 25-40 (the repo already has CYA, `10.CYAOutcomes.py`).
5. *Shared local labour markets.* Done: the son's friction on the father's survives state-at-17 FE and current
   state-by-year FE (C1); the IGE profiles move by about 0.03 with state FE (T5, C3).
6. *Measurement of parental income.* Done: clean-year income changes nothing (corr 0.997; opening gap change -0.006,
   s.e. 0.016, p=0.69).
7. *Life-cycle bias and the age profile of the friction share are the same thing.* They are not: the friction share is
   computed within band on the same sons as the IGE; what rises with age is the rest (0.154*** to 0.437*** in White
   earnings). State it and show the friction share with the band IGE in the same row.

## 4. Three analyses to run (public data only)

**A. Friction-driven parental income: closures only, and 2SLS (PSID; extend `73.SharedFriction.py`).**
Statistic: for sons 35-49 (and 25-29), the IGE of the son's log earnings and log wage on parental income instrumented
by the father's share of window years ending in a plant closure (strict measure), with the father's age at the son's
16 and his schooling as controls; alongside, b_P from the three-share prediction (current) and b_clean. Clustered by
1968 family; report the first-stage F.
Prediction under "instability marks the family" (Ekhaugen; Mader et al.): the closure-only 2SLS IGE is below b_clean
(closures are the least selected part of the variation) and the layoff/unemployment-driven b_P is above it.
Prediction under "the father's loss acts on the son" (OPS 2008): the closure 2SLS IGE is at or above b_clean (0.45 at
45-49 for White sons), as the current all-shares b_P = 0.67 is. Either answer is worth a paragraph; the second is the
headline. Cost: under an hour; the closure variable exists in `psid_displacement.pkl`.

**B. The age profile of the son's instability channel in the NLSY79 (extend `36.SameEmployerGrowthChecks.py` /
`2.NLSY79.py`).** Statistic: the Gelbach share of the earnings and wage IGE (parental income 1979-81; bands 25-29 to
50-55; cross-sectional plus supplemental samples; clustered by 1979 household) carried by the son's share of weeks
unemployed and weeks out of the labour force in the band, from the weekly arrays; then the same with AFQT and
schooling held fixed. Prediction from the PSID: 20-30% at 25-29 in earnings (PSID 28% White, 39% Black), 10-15% in
wages, under 5% by 45-49; the gradient of weeks not worked in parental income is already -0.056*** (s.e. 0.009) and
-0.061*** (0.014) at 25-34 and -0.074*** / -0.075*** at 35-55. If AFQT halves the share, the channel is skill and the
paper says so. The NLSY79's measure (weeks) is better than the PSID's (annual flags), so this is the replication a
referee will ask for first.

**C. The mother's instability, all sons (PSID; extend `73`).** Statistic: define the resident parent's window shares
(father if present, else mother; and the mother's own shares for all sons with a mother in the family unit) of years
unemployed (hours unemployed > 0) and with zero hours; (i) the son's career friction share on the mother's window
share, by father presence and race; (ii) the Gelbach share of the earnings IGE at 25-29 and 35-55 through the
mother's path and the shared mother-son path; (iii) the same for the father-absent sons alone (Black 48%, White 13%).
Predictions: in father-present families the mother's share adds under 0.03 to the son's friction (Magruder; Rege et
al.: mothers are not the channel); in father-absent families the mother's share predicts the son's at about 0.10, as
the father's does, and the mother's path carries 5-10% of the Black earnings IGE at 25-29 (where the father-present
shared path is 5.8%, p=0.21). Second version in the NLSY79-CYA: the child's share of weeks not worked at 25-34 and log
earnings on the mother's share of weeks unemployed or out of work over the child's ages 0-17, with the mother's AFQT
and schooling fixed; prediction 0.05-0.10 (s.e. about 0.02 with 5,000+ children). The CYA version is the one that
answers concern 4 cleanly.

Not proposed: a race-specific or parental-income-specific friction parameter in the model (rejected by the data,
p=0.59 / 0.76; EVIDENCE 11.23), or a family friction type (parsimony; EVIDENCE 11.27). The paper is an accounting
with public data; the model stays as it is.

## 5. References verified on the web in this note (title, authors, year, venue)

Oreopoulos-Page-Stevens 2008 JOLE 26(3) 455-483; Hilger 2016 AEJ:Applied 8(1) 247-283; Page-Stevens-Lindo 2009
Gruber volume 213-235; Shea 2000 JPubE 77(2) 155-184; Coelli 2011 Labour Economics 18(1) 25-35; Stevens-Schaller 2011
EER 30(2) 289-299; Rege-Telle-Votruba 2011 REStud 78(4) 1462-1489; Bratberg-Nilsen-Vaage 2008 Labour Economics 15(4)
591-603; Gregg-Macmillan-Nasim 2012 Fiscal Studies 33(2) 237-264; Lindo 2011 JHE 30(5) 869-879; Huttunen-Kellokumpu
2016 JOLE; Mork-Sjogren-Svaleryd 2019 IZA DP 12559; Britto-Melo-Sampaio 2022 IZA DP 15591; Chetty-Dobbie-Goldman-
Porter-Yang 2024 NBER WP 32697; Corak-Gustafsson-Osterberg 2004 (IZA DP 184); Ekhaugen 2009 JPopE 22(1) 97-113;
Macmillan 2014 OEP 66(3) 871-889; Mader-Muller-Riphahn-Schwientek 2015 JNS 235(4-5) 355-375; Hartley-Lamarche-Ziliak
2022 JPE 130(3) 523-565; Blanden-Gregg-Macmillan 2007 EJ 117(519) C43-C60; Mitnik-Bryant-Weber-Grusky 2015 IRS SOI;
Corak-Piraino 2011 JOLE 29(1) 37-68; Kramarz-Nordstrom Skans 2014 REStud 81(3) 1164-1200; Staiger 2020/2022 WP;
Plug-van der Klaauw-Ziegler 2018 SJE 120(1) 268-295; Magruder 2010 AEJ:Applied 2(1) 62-85; Halla-Schmieder-Weber 2020
AEJ:Applied 12(4) 253-287; Morrill-Morrill 2013 Labour Economics 20(1) 38-47 (venue only).
