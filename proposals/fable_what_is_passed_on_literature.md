# What is passed on through parental income: closest precedents for the wage / hours / stability / group split (Fable, 2026-10-20)

PI's primary question (2026-10-20): what is passed on from parents to sons through parental income, and which policy each
part points to. This memo checks the literature so that the contribution of the four-component split can be stated
against its closest precedents. It builds on `proposals/fable_friction_ige_literature.md` (2026-10-19) and does not
repeat it; papers verified there are carried over with their tags.

Read: `proposals/paperB_primary_goal_20261020.md`; `output/what_is_passed_on.md` (script 75, all sections, pooled,
White, Black, the 4 x 4 partials); `output/stability_opening_by_race.md` (script 81); `output/ui_stability_channel.md`
(script 82); `output/what_is_passed_on_rest.md` (script 80; see the caveat in Section 5); `EVIDENCE.md` rows
11.29-11.31; the 2026-10-19 memo. Nothing was run. Every repo number is quoted from a saved output with its s.e. and p.
References: [v] = checked on the web this session (journal, year, volume, pages); [v, earlier memo] = checked on
2026-10-19; [m] = from memory, confident; [?] = unsure, check before citing.

## 0. Short answer

The parent-side four-component split of the US earnings IGE by the son's age and race has no precedent; the closest
papers split the IGE on the son's side (his skills, schooling and early unemployment) or estimate the causal effect of
one parental job loss on one outcome at one age. Three things in the repo are new after this check: (1) the share of
the earnings IGE carried by the parents' employment spells in the son's childhood (6.1%***, s.e. 2.1, p=0.004, over
25-55) and its growth with the son's age (6.0%** at 25-29 to 13.5%*** at 45-49, opening 0.043**, s.e. 0.020, p=0.026);
(2) the contrast, inside one accounting, between plant closures (contribution -0.002, s.e. 0.002, p=0.314; at equal
parental income a closure raises the son's wage, 0.021** per s.d., p=0.043) and layoffs (0.025**, s.e. 0.011, p=0.024,
at 45-49); (3) the White-Black difference in the stability opening (0.107**, s.e. 0.046, p=0.018) located in the
parental-income gradient of Black fathers' layoffs, not in their cost. The UI-generosity test of an IGE share is also
new in form, but it is under-powered (within state-and-cohort s.d. 0.041 of a total 0.089) and one tax-data paper
(Cole, Miller, Huang, Willage and Mayer, AEA 2024) answers the underlying causal question better. The 63% "rest" is
where the literature puts most of the IGE (endowments, parents' schooling, wealth, neighbourhoods); script 80's split
should be reported once its rerun lands.

## 1. Who decomposes what the IGE transmits into wage, hours and stability

Nobody decomposes the IGE on the parent side into wage, hours and employment stability; the precedents are a 2 x 2 of
intergenerational correlations (wage, hours) without parental income, and son-side mediation studies. The candidates,
checked:

- **Altonji and Dunn (2000)**, JHR 35(2), 221-258 [v]. NLS parent-child and sibling pairs. Intergenerational
  correlations of wages, hours and earnings with a model that separates preferences from wage responses. Findings:
  wage correlations overstate the direct influence of the father's and especially the mother's wage; hours
  similarities run along gender lines and are preferences, not labour-supply responses to correlated wages; the effect
  of wages on earnings is direct. This is the closest precedent to the repo's diagonal (father's wage -> son's wage
  0.083*** per s.d., s.e. 0.016; father's hours -> son's hours 0.018***, s.e. 0.007, p=0.006; script 75, 4 x 4
  pooled). It has no parental-income IGE, no stability, no age profile and no race split. Altonji and Dunn (1991),
  Research in Labor Economics [m], report the raw hours correlation of 0.19 [v, via secondary sources].
- **The hours-IGE strand.** Toledo (2006, SED meeting paper 226) [v, working paper only; ? never published]: PSID
  father-son permanent hours correlation about 0.20, explained by correlated leisure preferences in a human-capital and
  wealth model; Mulligan (1997) 0.25 and Couch and Dunn (1997) 0.14 [?, cited from Toledo]. Galassi, Koll and Mayr
  (2021, CRC TR 224 DP 309) [v]: NLSY79 mothers and their CYA offspring; an always-employed mother raises the child's
  employment probability by 11% a year at equal ability, schooling, fertility and wealth; stronger to daughters and in
  low-income families; role-model channel; networks and local conditions ruled out. **Fernandez, Fogli and Olivetti
  (2004)**, QJE 119(4), 1249-1299 [v]: the son's wife works if his mother worked (preference formation). Repo: the
  mother's own hours carry 0.001 (s.e. 0.002, p=0.518) of the earnings IGE and the mother's zero-hours years 0.013**
  (s.e. 0.006, p=0.040) (script 75, pooled elements), so the mother's channel in the PSID is participation, not hours,
  which is Galassi et al.'s object.
- **Blanden, Gregg and Macmillan (2007)**, EJ 117(519), C43-C60 [v; full text read as IZA DP 2554]. BCS70 sons,
  earnings at age 30 on parental income averaged at ages 10 and 16; elasticity 0.32. Sequential decomposition (their
  eq. 3-6 is the Gelbach logic by hand): the full model accounts for 0.17 of 0.32 (54%); education 0.10; early labour
  market attachment, the share of months from 16 to 30 out of education and not employed, 0.03 (about 9%);
  cognitive and noncognitive skills 0.09 and 0.06 unconditionally, 7% and 6% conditional on education and attachment.
  Of the rise in persistence from 0.205 (NCDS 1958) to 0.291 (BCS 1970), attachment carries 0.015 (19%), entirely
  through a stronger income gradient of unemployment. This is the one published share for "labour market attachment"
  in an IGE accounting, and it is the son's own attachment, at one age, in one cohort. The repo's counterpart is
  script 74 (son's own friction 30.9%*** of the earnings IGE at 25-29, 8.7%*** at 45-49; EVIDENCE 11.28); script 75 is
  the parent side, which Blanden et al. do not have.
- **Gregg, Macmillan and Vittori (2019)**, JPopE 32(2), 501-528 [v]. BCS70, unconditional quantile regression: a
  J-shaped parental-income gradient of sons' earnings; early spells out of work have lasting effects at the bottom;
  education does not remove the gradient. Son-side again. **Gregg, Macmillan and Vittori (2017)**, OBES 79(1), 79-100
  [v]: lifetime-earnings estimates for the UK (life-cycle correction). **Gregg, Jonsson, Macmillan and Mood (2017)**,
  Social Forces 96(1), 121-152 [v]: education's mediation of the IGE in the US, GB and Sweden; educational inequality
  and returns do not explain the cross-country differences [? whether attachment is a mediator there].
- **Bowles and Gintis (2002)**, JEP 16(3), 3-30 [v]: an accounting of the 0.4 parent-child income correlation into
  IQ (the heritable IQ channel is a few percent), schooling, wealth, race and personality; **Bowles, Gintis and
  Osborne Groves (eds., 2005)**, Unequal Chances, Princeton UP [v, book; Hertz's chapter 165-191]. Bowles, Gintis and
  Osborne (2001), JEL 39(4), 1137-1176, "The determinants of earnings: a behavioral approach" [m; the "2001" the PI
  mentions is probably this]. No labour-supply or stability channel.
- **Cardak, Johnston and Martin (2013)**, Labour Economics 24, 39-47 [v]: PSID father-son 1968-2005; a structural
  split of the IGE into investment (one third) and endowment (two thirds); investment matters more at low incomes.
  **Vosters and Nybom (2017)**, JOLE 35(3), 869-901 [v]: combining income, education and occupation as proxies raises
  US persistence only from 0.44 to 0.47 (against Clark's 0.75).
- **Shea (2000)**, JPubE 77(2), 155-184 [v, earlier memo]: parental income variation from union, industry and job
  loss has a negligible effect on children's outcomes except for low-education fathers. The repo's script 74
  (friction-predicted parental income transmits more than the rest, difference 0.168***, p=0.007) is the opposite on
  the same data; script 75 sharpens it: the part that transmits is layoffs and the mother's unemployment, not closures.
- **Measurement and life-cycle papers that define the IGE but do not split it**: Mazumder (2005), REStat 87(2),
  235-255 [v]; Lee and Solon (2009), REStat 91(4), 766-772 [v]; Chadwick and Solon (2002), AER 92(1), 335-344 [v];
  Mazumder (2016), Research in Labor Economics 43 [v, chapter in Inequality: Causes and Consequences, Emerald]: the
  family-income IGE is above 0.6 with long averages centred at 40; Mitnik and Grusky (2020) is in Sociological
  Methodology 50(1), 47-95, not Demography [v]: the conventional IGE is the elasticity of the geometric mean;
  Mitnik, Bryant, Weber and Grusky (2015), IRS SOI WP [v, earlier memo]. None decomposes the earnings-vs-income
  difference into employment and wages.
- **Surveys**: Black and Devereux (2011), Handbook of Labor Economics 4B [v, volume; pages 1487-1541 ?]; Bjorklund
  and Jantti (1997), AER 87(5), 1009-1018 [v]; Bjorklund and Jantti (2009), Oxford Handbook of Economic Inequality
  [m]; Corak (2013), JEP 27(3), 79-102 [v]; Landerso and Heckman (2017), SJE 119(1), 178-230 [m; search did not
  return the page]. They organise the literature by skills, schooling, place and institutions; employment stability
  of the parents is not a category in any of them.
- **Place**: Chetty, Hendren, Kline and Saez (2014), QJE 129(4), 1553-1623 [v]; Chetty and Hendren (2018), QJE
  133(3), 1107-1162 and 1163-1228 [v]; **Rothstein (2019)**, JOLE 37(S1), S85-S123 [v]: across commuting zones,
  marriage patterns explain two fifths of the variation in income transmission, human capital accumulation and its
  returns one ninth each, and a third is earnings differences not mediated by human capital (he names job networks and
  local labour markets). Rothstein's is the nearest US decomposition of "what the IGE transmits", at the place level
  and on the son's side; the repo's group component (state unemployment and Bartik shocks at 12-18) carries 0.4%
  (0.002, s.e. 0.002, p=0.442) of the earnings IGE, with state FE moving nothing (EVIDENCE 11.27), which says the
  repo's place measures are too coarse to see Chetty-Hendren exposure effects, not that place is absent.
- **Race**: Hertz (2005), in Unequal Chances, 165-191 [v]: PSID transition matrices, first Black-White mobility
  comparison; **Bhattacharya and Mazumder (2011)**, Quantitative Economics 2(3), 335-379 [v]: NLSY79; Black sons have
  much less upward mobility and most of the gap is accounted for by adolescent cognitive skills (AFQT); Mazumder
  (2014), Economic Perspectives 38(1) [v, exists; pages ?]; Davis and Mazumder, "The decline in intergenerational
  mobility after 1980", Chicago Fed WP 2017-05 rev. 2022 [v WP; ? journal version, not found]: rank-rank 0.25 to
  0.36 across the 1950 and early-1960s cohorts, part through returns to schooling and the marriage gradient;
  **Card, Domnisoru and Taylor (2022)**, JOLE 40(S1), S39-S95 [v]: 1940 Census, children born in the 1920s; lower
  Black mobility, schooling responsive to school quality, Southern teacher pay; **Rauh and Valladares-Esteban
  (2023)**, RED 51, 424-449 [v]: Black men's wage gap widens over working life while employment and hours gaps are
  constant; test scores at 17-22 plus experience account for the gap and its growth; an on-the-job human capital
  model with endogenous labour supply closes 84% of the hourly-earnings gap by equalising pre-market conditions;
  Chetty, Hendren, Jones and Porter (2020), QJE 135(2), 711-783 [v]: the Black-White gap is in men, in employment as
  much as in wages. Kalil and Wightman (2011), SSQ 92(1), 57-78 [v]: PSID, parental job loss lowers any post-secondary
  education, three times as strongly for Black youth, and the gap is explained by wealth, long-run income and
  especially parental long-term unemployment. None splits the racial IGE gap by parental component; Rauh and
  Valladares-Esteban's "wage gap opens with age, employment gap does not" is the same shape as the repo's racial
  opening sitting in the wage component (script 24) and should be cited beside it.
- Not IGE papers: Altonji, Cattan and Ware (2017), JHR 52(1), 1-47 [v] is on sibling influence on teenage substance
  use; drop it from the list.

## 2. Is "employment stability in childhood" studied as a transmitted component, and is the closure-layoff contrast consistent with the displacement literature

Employment stability in childhood is studied only as a one-off shock (one displacement, one outcome, one age) or as
the father-son correlation of unemployment; no paper measures the parents' spells over the son's whole childhood and
asks what share of the IGE they carry. The two strands and what they find:

**Shock studies.** Closures as the instrument: Oreopoulos, Page and Stevens (2008), JOLE 26(3), 455-483 [v, earlier
memo] (Canada; sons' earnings about 9% lower, more UI and social assistance, concentrated at the bottom of parental
income); Bratberg, Nilsen and Vaage (2008), Labour Economics 15(4), 591-603 [v, earlier memo] (Norway; no effect on
children's earnings 1999-2001 after fathers' 1986-87 displacement); Rege, Telle and Votruba (2011), REStud 78(4),
1462-1489 [v, earlier memo] (Norway; the father's closure lowers GPA, not via income, employment, divorce or moves);
Mork, Sjogren and Svaleryd (2019, IZA DP 12559) [v WP; Labour Economics 2020 ?] (Sweden; children unharmed, parents
harmed; they credit UI and dual earning); Carneiro, Salvanes, Willage and Willen (2022, IZA DP 15630) [v WP] (Norway,
mass layoffs and closures; displacement in the teens has the largest effect on human capital accumulation, early
childhood the largest on income; maternal stress). Layoffs or all job losses: Hilger (2016), AEJ: Applied 8(1),
247-283 [v, earlier memo] (US tax data, firm mass layoffs; income falls sharply, college and early earnings fall only
slightly; closure- and self-report-based estimates larger because of selection); Stevens and Schaller (2011), EER
30(2), 289-299 [v, earlier memo] (SIPP, all job losses; grade retention +15%); Kalil and Ziol-Guest (2008), Social
Science Research 37 [v, DOI; pages ?] (SIPP; fathers' involuntary separations raise grade repetition and suspension,
mothers' do not; family dynamics, not income); Page, Stevens and Lindo (2009) [v, earlier memo] (PSID; results depend
on the displacement definition); Coelli (2011) [v, earlier memo]; Brand and Thomas (2014), AJS 119(4), 955-1001 [v]
(PSID, single mothers' displacement; lower educational attainment and well-being in young adulthood, strongest for
older children); Kalil and Wightman (2011) [v, above]; Huttunen and Riukula (2019, IZA DP 12788; Labour Economics
2024 [v; volume ?]) (Finland; the father's loss lowers the child's earnings and entry into the father's field or
plant); Lindo (2011), JHE 30(5), 869-879 [v, earlier memo]; Schaller and Zerpa, AJHE [v, exists; volume ?]. All
observe the child once, between the late teens and the mid-thirties.

**Transmission-of-worklessness studies.** Father-son unemployment correlations of about 0.10 in the UK, Norway,
Canada and Germany, with the causal part near zero once family background is fixed (O'Neill and Sweetman 1998 [m];
Corak, Gustafsson and Osterberg 2004; Ekhaugen 2009; Macmillan 2014; Mader et al. 2015 [all v, earlier memo]);
mother-child employment 11% in the US (Galassi et al. 2021 [v]). These measure spells in both generations but never
put them inside the IGE.

**Who finds that layoffs (not closures) matter.** Hilger's layoffs matter little; Kalil and Ziol-Guest's involuntary
separations, Stevens and Schaller's and Brand and Thomas's job losses, and Kalil and Wightman's parental long-term
unemployment matter for schooling; OPS's closures matter for earnings at the bottom. Stevens (1997), JOLE 15(1),
165-188 [v], is the key fact behind the repo's contrast: a worker's own displacement loss persists (earnings and wages
about 9% below expectation six years on) mostly because of further job losses; workers who avoid repeat losses lose
1% and 4%. A layoff share over a seven-year window measures exactly this repeat-loss trait.

**Is the repo's 4 x 4 consistent with the displacement literature? Yes, once the accounting is read correctly, and
the selection argument runs as follows.**

1. The Gelbach split conditions on parental income, so a closure's effect through the income it destroys sits in the
   "rest" (parental income at equal components), not in the stability component. The closure element therefore
   measures what a closure does beyond its income effect. The displacement papers estimate the total effect, income
   included, and find it concentrated where income matters (OPS: the bottom of the distribution; Hilger: small when
   income falls sharply; Bratberg, Mork: zero where insurance replaces income). "Closures carry nothing beyond
   income" (contribution -0.002, s.e. 0.002, p=0.314, pooled 25-55; -0.001, s.e. 0.001, p=0.317, in the wage IGE) is
   what those papers predict for a linear accounting at equal parental income. It is at odds only with Rege et al.'s
   father effect "not via income", and that is on GPA at 16, not on adult earnings.
2. At equal parental income, a closure flags a family whose measured income lies below its permanent standing. A
   father whose seven-year income was pulled down by an event unrelated to his productivity has a higher permanent
   wage than his income says; his son's wage is therefore above that of sons with the same parental income and no
   closure. The positive partial (0.021** per s.d., s.e. 0.010, p=0.043, pooled; 0.023**, s.e. 0.011, p=0.040,
   White) is the signature of the closure's exogeneity, the "lemon-free" displacement of Gibbons and Katz (1991), JOLE
   9(4), 351-380 [v]: closures carry no signal about the worker, layoffs do, and laid-off workers have longer
   unemployment and larger wage losses. This is the same reason the displacement literature chose closures.
3. Layoffs are subject to the same mechanical sign (income below permanent standing) but they also carry the lemons
   signal and the repeat-loss trait (Stevens 1997), and they are graded in parental income: for White sons the layoff
   gradient d is -0.040*** (s.e. 0.006) at 25-29 and -0.046*** (0.010) at 45-49, flat with age, while the earnings cost
   g moves from 0.158 (s.e. 0.118, p=0.182) to -0.818*** (0.297, p=0.006), change -0.975*** (0.274, p<0.001) (script
   81). The product g d is the stability share, so the stability component is a "marking" statistic (Ekhaugen 2009;
   Mader et al. 2015), not the causal effect of a shock. For Black sons the layoff gradient is flat (-0.002, s.e. 0.009,
   p=0.832 at 25-29; -0.010*, 0.006, p=0.087 at 45-49): Black fathers' layoffs are not graded by family income (cf.
   Hoynes, Miller and Schaller 2012 [m]; Chetty et al. 2020 [v]), so they carry no IGE share whatever their cost
   (g -0.218 and -0.351, both n.s.). The White-Black opening of 0.107** (s.e. 0.046, p=0.018; 0.120***, 0.044,
   p=0.006, with cohort dummies) is in d, not g; that is the sentence for the paper.
4. Consequence for the policy row: the stability share is the upper bound of what insurance could remove (it includes
   the family trait), and the causal part is bounded by the closure element (zero beyond income) plus the closure's
   income effect inside the rest. The two handles that separate them are the UI interaction (Section 4) and the
   closure-only 2SLS proposed in the 2026-10-19 memo (Section 4A there), which the literature's own choice of
   instrument supports.
5. One inconsistency to flag honestly: OPS's effect is a nonlinearity (bottom of parental income) that a linear Gelbach
   split averages away. A by-tercile split of the closure element is cheap and would show whether the repo's zero is a
   zero or an average of a negative at the bottom and a positive above.

## 3. Precedent for the stability share growing with the son's age

There is no precedent for a childhood component of the IGE whose share rises with the son's age; the life-cycle-bias
literature explains why the whole IGE rises and supplies the mechanism that fits the repo's pattern, and the
displacement literature stops observing children before 40.

- **Life-cycle bias.** Haider and Solon (2006), AER 96(4), 1308-1320 [v]: the slope of current on lifetime earnings is
  below one before about age 32 and the IGE from young sons is biased down; Grawe (2006), Labour Economics 13(5),
  551-570 [v]: the father's age at measurement and the estimator explain about 40% of the cross-study variance of
  published IGEs; Bohlmark and Lindquist (2006), JOLE 24(4), 879-900 [v]: Swedish replication, same shape as the US;
  Nybom and Stuhler (2016), JHR 51(1), 239-268 [v]: heterogeneous income profiles make the bias large and the usual
  corrections incomplete; Nybom and Stuhler (2017), JHR 52(3), 800-825 [v]: rank measures suffer less. Mazumder
  (2005) and Lee and Solon (2009) [v] are the US applications. These papers say that sons of richer parents have
  steeper age-earnings profiles, so the IGE measured at 25-29 understates lifetime persistence.
- **How the repo's result fits.** The stability share rises because g (the earnings cost of the father's layoffs and
  the mother's unemployment) grows with the son's age while d (their gradient in parental income) is flat (script 81).
  That is Nybom and Stuhler's heterogeneous profiles applied to one childhood circumstance: sons of fathers with
  layoff years have flatter profiles. The repo already has the within-job counterpart (same-employer growth rises with
  parental income for White sons, 0.019***, script 24), and the model's human capital accumulation pay-off of parental
  income (H4) is the structural statement of the same thing. The paper should say so and show, in one row, the band
  IGE, the stability contribution and its share, so that a reader sees that the share grows faster than the IGE (share
  0.060** at 25-29, s.e. 0.027, p=0.024; 0.135*** at 45-49, s.e. 0.047, p=0.004; IGE 0.276*** to 0.443***).
- **Why no paper has it.** OPS observe sons in their late twenties and early thirties [m, ages 25-33]; Hilger in the
  mid-twenties [m]; Bratberg et al. in 1999-2001, twelve to fifteen years after displacement [v]; Huttunen and Riukula
  and Carneiro et al. at similar ages; Blanden et al. at 30 [v]; Chetty et al. (2014) at 29-32 [m]. At those ages the
  repo's share is 6%, not 13.5%. The administrative-data IGE literature therefore sees the stability channel at a
  third of its mid-career size.
- **Late-emerging effects of childhood circumstances.** Case, Fertig and Paxson (2005), JHE 24(2), 365-389 [v]: NCDS
  childhood health and circumstance lower earnings in adulthood through schooling and early-adult health; Brand and
  Thomas (2014) [v]: the mother's displacement hurts older children more (age at the shock, not age at the outcome);
  Stevens (1997) [v]: the father's own loss compounds through repeat losses. None follows the child to 45-49. The
  honest statement is "no study has followed the children of unstable fathers past 40; our PSID sons reach 55".
- **Caveat to pre-empt.** The age profile in the PSID is partly a cohort profile (sons at 45-49 were children in the
  1970s-80s). The cohort-dummy version keeps the White opening (0.065***, s.e. 0.025, p=0.009) and the W-B difference
  (0.120***, p=0.006), which answers the referee; say it in the text.

## 4. Has anyone tested whether UI generosity mitigates the intergenerational effect of parental job loss

Yes, in five papers, one of them on US tax data with a design that dominates ours on power; none tests the effect on
an IGE share, which is what script 82 does.

- **Cole, Miller, Huang, Willage and Mayer (2024)**, "Intergenerational effects of unemployment insurance: evidence
  from tax data", AEA 2024 session paper [v, conference abstract; ? working paper version]. US administrative tax
  records; variation in UI generosity from state policy and from trigger-based extensions when unemployment exceeds
  thresholds; a $10,000 rise in the parents' maximum total UI benefits raises the child's earnings at 26 by $224 and
  tax paid by $44, about two thirds of the cost recouped. This is the direct precedent for the policy row and the
  paper to cite first; it has the event (a parent's job loss), the generosity at the event, and N in the millions.
- **Britto, Melo and Sampaio (2022)**, IZA DP 15591 [v WP; ? journal]: Brazil, mass layoffs; dropout, informal work
  and crime rise; UI eligibility mitigates, which they read as income being the channel.
- **Lindemann and Gangl (2020)**, Social Forces 99(2), 616-647 [v]: five panels, 21 countries, multilevel LPM of entry
  into post-secondary education; short- and long-term net replacement rates; more generous replacement reduces the
  adverse effect of parental unemployment, most where the main earner is unemployed and no other parent works.
- **Mari, Keizer and van Gaalen (2024)**, European Societies 26(3), 602-638 [v]: Dutch registers, students born
  1992-98; paternal unemployment in 6th grade lowers track placement only in lower-wealth families; larger benefit
  amounts reduce the effect, especially above the median benefit; no maternal effect.
- **Hansen and Stutzer (2020)**, IZA DP 13752; JEBO 2022 [v WP; ? volume]: cross-country child life satisfaction;
  a higher replacement rate buffers the father's unemployment, not the mother's.
- **Adult-outcome UI papers that set the design template**: East and Kuka (2015), JPubE 132, 32-50 [v]
  (consumption smoothing from UI over forty years of PSID, using simulated benefit eligibility; effects larger when
  state unemployment and generosity are high); Kuka (2020), REStat 102(3), 490-505 [v] (state UI law changes; health
  insurance coverage and self-reported health improve, more in high-unemployment periods); Hsu, Matsa and Melzer
  (2018), AER 108(1), 49-81 [v] (UI generosity cuts mortgage delinquency after job loss). Schaller and Zerpa [v] show
  public health insurance offsetting the loss of private coverage after a father's job loss. Mork et al. [v WP] credit
  Swedish UI for the Nordic nulls, as interpretation only.

**How the repo's design compares.** Script 82 uses the state's statutory maximum weekly benefit over the average
weekly wage, averaged over the son's ages 12-18 in the state at 17 (DOL, script 12b), state-at-17 FE, five-year cohort
and age dummies, and interacts UI with each parental spell element at equal parental income and components, with the
parents' wages x UI as placebos. Relative to the literature: (a) ours is the only test on an IGE share rather than on
an outcome (split by generosity: stability contribution 0.035**, s.e. 0.016, p=0.028, 9.3%**, in more generous states
vs 0.050***, s.e. 0.015, p=0.001, 13.3%***, in less generous, difference -0.015, s.e. 0.023, p=0.516); (b) East-Kuka,
Kuka and Cole et al. measure generosity at the event for the person who lost the job (simulated or actual benefit),
whereas ours is a childhood average that does not know when the spell happened or what the father's replacement rate
was; (c) Kuka's and East-Kuka's result that UI bites in high-unemployment periods suggests interacting the spell x UI
term with the state unemployment rate in the spell year; (d) power: within state and cohort the UI s.d. is 0.041 of a
total 0.089, and the sample is 3,495 sons, against millions in Cole et al. The signs all point the insurance way
(closure x UI 0.034**, s.e. 0.017, p=0.045, pooled; 0.057**, s.e. 0.025, p=0.024, at 40-55; mother's unemployment x
UI on the son's unemployment share -0.010**, s.e. 0.005, p=0.037, pooled, -0.020**, 0.008, p=0.011, Black; layoff x UI
0.021, s.e. 0.016, p=0.188), with placebos at -0.004 (p=0.791) and -0.015 (p=0.308), but one Black placebo is
significant (father's wage x UI on employment 0.034**, s.e. 0.014, p=0.017), so the Black panel cannot be read. The
paper should present script 82 as a sign check that agrees with Cole et al., Lindemann-Gangl and Mari et al., not as
an estimate of the offset.

## 5. The 63% "rest": what the literature attributes the residual IGE to, and a sensible split

The literature puts most of the IGE in endowments and parents' schooling, with wealth, neighbourhoods and marriage
as the other named parts; a parent-side labour-market accounting like script 75 is expected to leave a majority
residual, and the repo's 62.9%*** (s.e. 8.4, p<0.001) is in line with Blanden et al.'s 46% unexplained after skills,
schooling and attachment on the son's side.

- **Endowments vs investments.** Cardak, Johnston and Martin (2013) [v]: two thirds endowment on PSID fathers and
  sons. Bjorklund, Lindahl and Plug (2006), QJE 121(3), 999-1028 [v]: Swedish adoptees; both pre-birth and post-birth
  factors matter, pre-birth more for mothers' education and less for fathers' income, with a positive interaction.
  Sacerdote (2007), QJE 122(1), 119-157 [v]: Korean-American adoptees; adoptive-family effects on schooling and income
  exist but are smaller than biological transmission. Bowles and Gintis (2002) [v]: the heritable-IQ channel is a few
  percent; personality, schooling and wealth carry more.
- **Parents' schooling.** Black, Devereux and Salvanes (2005), AER 95(1), 437-449 [v]: little causal effect of
  parents' schooling on children's schooling (Norwegian reform), only mothers to sons; Holmlund, Lindahl and Plug
  (2011), JEL 49(3), 615-651 [v]: the intergenerational schooling association is mostly selection. So a parents'
  schooling row is a proxy for ability and investments, not a lever.
- **Wealth.** Pfeffer and Killewald (2018), Social Forces 96(4), 1411-1442 [v]: PSID; a decile of parental wealth is
  four percentiles of the child's; grandparents matter beyond parents; direct transfers explain part, college more.
- **Place and marriage.** Chetty and Hendren (2018) [v]: causal exposure effects of counties; Rothstein (2019) [v]:
  marriage two fifths, human capital two ninths, a third not via human capital, across CZs. Carneiro, Lopez Garcia,
  Salvanes and Tominey (2021), JPE 129(3), 757-788 [v]: the timing of parental income matters (early and late
  childhood productive, middle less so).
- **Skills by race.** Bhattacharya and Mazumder (2011) [v] and Rauh and Valladares-Esteban (2023) [v]: adolescent
  test scores account for most of the Black-White mobility gap and of the growth of the wage gap with age.

**What script 80 adds and what to report.** Split B (provisional, see caveat) moves 0.155*** (s.e. 0.033, p<0.001;
39.3%*** of the earnings IGE) into parents' schooling, almost all the father's (0.158***, s.e. 0.035; mother -0.003,
s.e. 0.013, p=0.832), 0.026* (s.e. 0.015, p=0.087) into transfers (AFDC years 0.026**, s.e. 0.011, p=0.015), 0.001
(s.e. 0.012, p=0.965) into assets and home ownership, 0.035 (s.e. 0.029, p=0.231) into parental labour earnings beyond
the components, and leaves a rest of 0.188*** (s.e. 0.046, p<0.001; 47.6%***). The wage component falls from 19.0%***
to 12.0%** (s.e. 5.9, p=0.042) and stability from 6.1%*** to 4.9%** (s.e. 2.2, p=0.029), so a third of the wage
component and a fifth of the stability component are "explained" by the father's schooling, which is what Blanden et
al. find for the son's skills behind his education. A sensible split to report, in this order: (i) parents' schooling
(read with Black-Devereux-Salvanes and Holmlund et al. as an endowment-and-investment proxy, not a policy lever);
(ii) wealth (asset income share, home ownership; cite Pfeffer-Killewald for why it is thin in the PSID's income
measure); (iii) transfers and welfare years; (iv) family size and others' income; (v) the residual, with the NLSY79's
AFQT as the test of how much of it is the son's pre-market skill (Bhattacharya-Mazumder; Rauh-Valladares-Esteban).
Place should be stated as "not separable with state-level measures" rather than as absent.

**Caveat on `output/what_is_passed_on_rest.md`.** Its section 0 gives the father's schooling as 10.85 years pooled but
6.12 for Black fathers (mothers 12.40), 2.3 years below the mothers overall; by the PI's rule (a father's schooling
mean below 9 years marks the pre-fix version) the Black rows at least are the old version, and the sign flip of
family structure in split B (-0.083***, s.e. 0.027, p=0.002, from +0.035**) is what a schooling variable that is
missing or imputed for father-absent sons would produce (11.2% of measures missing). Quote the schooling rows only
after the rerun; the assets, transfers and labour-earnings rows are not affected by the bug as described but should be
re-read too.

*Note added after the memo (2026-10-20): the caveat was right. Absent parents had a schooling of 0 that the fill kept;
fixed and rerun (EVIDENCE 11.32). Corrected means: fathers 13.32 / mothers 13.30 pooled, Black fathers 11.78. Corrected
split B, pooled earnings IGE 0.396\*\*\*: rest 47.6%\*\*\* (from 62.9%), parents' schooling 0.051\*\*\* (12.9%\*\*\*),
all of it the father's (0.054\*\*\*, rising 0.014 -> 0.075\*\*\* from 25-29 to 45-49), AFDC/TANF years 0.026\*\*
(p=0.015), assets / others' income / family size 0.001 / 0.001 / 0.000, family structure +0.021 (p=0.206).*

## 6. Bottom line: the contribution, and the two analyses that most strengthen it

Paper B's "what is passed on" question is new in form and in two results. In form: it is, after this check, the
first exact decomposition of the US earnings IGE on the parent side into the parents' hourly wage, hours when
employed, employment spells in the son's childhood and the local labour market, by the son's five-year age band and
by race, with bootstrap standard errors on every share; the precedents split the IGE on the son's side (Blanden,
Gregg and Macmillan 2007; Gregg, Macmillan and Vittori 2019; Rothstein 2019) or estimate one parental shock at one age
(Oreopoulos, Page and Stevens 2008; Hilger 2016). In results: the parents' spells carry 6.1%*** of the earnings IGE
over 25-55 and 13.5%*** at 45-49, a share that no study could see because none follows the children of unstable
fathers past their thirties; and the same accounting shows that closures carry nothing beyond their income effect
while layoffs and the mother's unemployment carry the share, which is the Gibbons-Katz selection logic appearing in
the next generation and the reason the stability share is a marking statistic, with the UI interaction and a
closure-only 2SLS as the handles on its causal part. The racial result, that the White-Black difference in the
stability opening (0.107**, p=0.018) is the parental-income gradient of Black fathers' layoffs and not their cost, is
first evidence of its kind as far as I can verify, and it belongs beside Kalil and Wightman (2011) and Rauh and
Valladares-Esteban (2023). The policy sentence the paper can defend is: schooling and training act on the wage
component (19%***), insurance on at most the stability component (6-13%), and the evidence on insurance (Cole et al.
2024; Lindemann and Gangl 2020; Mari et al. 2024; script 82's signs) says it offsets part of that component, with the
size still open.

The two analyses that most strengthen it: (1) the father's simulated UI replacement rate at each spell (his
earnings, state and year; the East-Kuka / Kuka construction), interacted with the spell and with the state
unemployment rate in that year, pooled with AFDC and EITC generosity, so the policy row has an event-level test with
the right identifying variation instead of a childhood average; (2) the NLSY79 replication of the age profile of the
layoff cost g with AFQT and schooling held fixed (sons now 45-60; weekly arrays measure spells better), which decides
between "a stable environment" and "a marked family" and, with the closure-only 2SLS, bounds the causal part of the
13.5%. A cheap third is the by-tercile closure element (Section 2, point 5), which answers OPS's nonlinearity.

## Closest precedents

| paper | data | what it decomposes / estimates | result | how Paper B differs |
|---|---|---|---|---|
| Altonji and Dunn (2000) JHR [v] | NLS parent-child, sibling pairs | Intergenerational correlations of wages, hours, earnings; preferences vs wage responses | Hours similarity = preferences, by gender; wage correlations overstate direct influence | Parent-side split of the IGE on parental income, adds spells and place, by age and race |
| Blanden, Gregg and Macmillan (2007) EJ [v] | BCS70 sons at 30 | Son's cognitive, noncognitive, education, attachment (months 16-30 not employed) in the 0.32 elasticity | 54% accounted; education 0.10, attachment 0.03 (9%); attachment 19% of the 1958-70 rise | Parent side, not son side; six age bands to 55; PSID; race |
| Gregg, Macmillan and Vittori (2019) JPopE [v] | BCS70 | UQR of sons' earnings on parental income; early spells out of work | J-shape; early spells lasting at the bottom | Spells of the parents; shares with s.e. |
| Shea (2000) JPubE [v] | PSID | Children's outcomes on "luck" parental income (union, industry, job loss) | Negligible except low-education fathers | Windowed shares; layoffs transmit, closures do not; contra Shea |
| Oreopoulos, Page and Stevens (2008) JOLE [v] | Canadian tax data | Sons' earnings after the father's closure | -9%, bottom of parental income | Closure as a component at equal income (zero beyond income, +0.021** on the wage); sons to 55 |
| Hilger (2016) AEJ:Applied [v] | US tax data, 7m layoffs | College, earnings after the father's layoff | Small; closures/self-reports overstate via selection | Layoffs graded in income carry the stability share; the selection is the result, not the nuisance |
| Kalil and Wightman (2011) SSQ [v] | PSID | Post-secondary entry after parental job loss, Black vs White | 3x stronger for Black youth; wealth, long-run income, long-term unemployment explain the gap | IGE shares by race; the Black difference is the gradient d of layoffs, not their cost |
| Stevens (1997) JOLE [v] | PSID | Own displacement loss over time | Persistence via repeat losses | The father's repeat-loss trait is what the layoff share measures |
| Gibbons and Katz (1991) JOLE [v] | Displaced Worker Survey | Layoffs vs closures as signals | Layoffs signal low ability; longer unemployment, larger losses | The sign pattern of closure vs layoff partials in the son's generation |
| Rothstein (2019) JOLE [v] | US tax data by CZ | Variation of income transmission across places | Marriage 2/5, human capital 2/9, 1/3 not via HC | Family-level components; place measured only at the state level (0.4%) |
| Cardak, Johnston and Martin (2013) LE [v] | PSID fathers-sons | Investment vs endowment in the IGE | 1/3 investment, 2/3 endowment | Observable parent components; the 63% rest is where their endowments sit |
| Nybom and Stuhler (2016) JHR [v] | Swedish registers | Life-cycle bias from heterogeneous profiles | IGE rises with the son's age; corrections incomplete | A component whose share rises because its cost g grows with age while its gradient d is flat |
| Bhattacharya and Mazumder (2011) QE; Rauh and Valladares-Esteban (2023) RED [v] | NLSY79 | Black-White mobility gap; wage gap over the life cycle | AFQT accounts for most; wage gap opens with age, employment gap does not | Racial opening of the IGE in the wage component; stability opening White only |
| Cole, Miller, Huang, Willage and Mayer (2024) AEA [v, abstract] | US tax data | Children's earnings at 26 on parents' max UI benefits | +$224 per $10,000; 2/3 recouped | UI on an IGE share; childhood-average generosity; under-powered but same sign |
| Lindemann and Gangl (2020) SF; Mari, Keizer and van Gaalen (2024) ES [v] | 21-country panels; Dutch registers | Replacement rates / benefit amounts x parental unemployment on education | Generosity reduces the effect, most for single-earner / low-wealth families | Earnings to 55; the interaction placed inside the IGE accounting |

## References

[v] checked this session; [v, earlier memo] checked 2026-10-19; [m] memory, confident; [?] unsure, check before citing.

- Altonji, J. G. and T. A. Dunn (2000). An intergenerational model of wages, hours, and earnings. JHR 35(2), 221-258. [v]
- Altonji, J. G. and T. A. Dunn (1991). Relationships among the family incomes and labor market outcomes of relatives. Research in Labor Economics 12. [m; ? pages]
- Altonji, J. G., S. Cattan and I. Ware (2017). Identifying sibling influence on teenage substance use. JHR 52(1), 1-47. [v; not an IGE paper]
- Bhattacharya, D. and B. Mazumder (2011). A nonparametric analysis of black-white differences in intergenerational income mobility in the United States. Quantitative Economics 2(3), 335-379. [v]
- Bjorklund, A. and M. Jantti (1997). Intergenerational income mobility in Sweden compared to the United States. AER 87(5), 1009-1018. [v]
- Bjorklund, A. and M. Jantti (2009). Intergenerational income mobility and the role of family background. Oxford Handbook of Economic Inequality. [m]
- Bjorklund, A., M. Lindahl and E. Plug (2006). The origins of intergenerational associations: lessons from Swedish adoption data. QJE 121(3), 999-1028. [v]
- Black, S. E. and P. J. Devereux (2011). Recent developments in intergenerational mobility. Handbook of Labor Economics 4B. [v volume; ? pages 1487-1541]
- Black, S. E., P. J. Devereux and K. G. Salvanes (2005). Why the apple doesn't fall far: understanding intergenerational transmission of human capital. AER 95(1), 437-449. [v]
- Blanden, J., P. Gregg and L. Macmillan (2007). Accounting for intergenerational income persistence: noncognitive skills, ability and education. EJ 117(519), C43-C60. [v; numbers from IZA DP 2554]
- Bohlmark, A. and M. J. Lindquist (2006). Life-cycle variations in the association between current and lifetime income: replication and extension for Sweden. JOLE 24(4), 879-900. [v; one CV says 879-896]
- Bowles, S. and H. Gintis (2002). The inheritance of inequality. JEP 16(3), 3-30. [v]
- Bowles, S., H. Gintis and M. Osborne (2001). The determinants of earnings: a behavioral approach. JEL 39(4), 1137-1176. [m]
- Bowles, S., H. Gintis and M. Osborne Groves, eds. (2005). Unequal Chances: Family Background and Economic Success. Princeton UP. [v]
- Brand, J. E. and J. Simon Thomas (2014). Job displacement among single mothers: effects on children's outcomes in young adulthood. AJS 119(4), 955-1001. [v]
- Bratberg, E., O. A. Nilsen and K. Vaage (2008). Job losses and child outcomes. Labour Economics 15(4), 591-603. [v, earlier memo]
- Britto, D., C. Melo and B. Sampaio (2022). The kids aren't alright: parental job loss and children's outcomes within and beyond schools. IZA DP 15591. [v WP; ? journal]
- Card, D., C. Domnisoru and L. Taylor (2022). The intergenerational transmission of human capital: evidence from the golden age of upward mobility. JOLE 40(S1), S39-S95. [v]
- Cardak, B. A., D. W. Johnston and V. L. Martin (2013). Intergenerational earnings mobility: a new decomposition of investment and endowment effects. Labour Economics 24, 39-47. [v]
- Carneiro, P., I. Lopez Garcia, K. G. Salvanes and E. Tominey (2021). Intergenerational mobility and the timing of parental income. JPE 129(3), 757-788. [v]
- Carneiro, P., K. G. Salvanes, B. Willage and A. Willen (2022). The timing of parental job displacement, child development and family adjustment. IZA DP 15630. [v WP; ? journal]
- Case, A., A. Fertig and C. Paxson (2005). The lasting impact of childhood health and circumstance. JHE 24(2), 365-389. [v]
- Chadwick, L. and G. Solon (2002). Intergenerational income mobility among daughters. AER 92(1), 335-344. [v]
- Chetty, R. and N. Hendren (2018). The impacts of neighborhoods on intergenerational mobility I and II. QJE 133(3), 1107-1162 and 1163-1228. [v]
- Chetty, R., N. Hendren, M. R. Jones and S. R. Porter (2020). Race and economic opportunity in the United States: an intergenerational perspective. QJE 135(2), 711-783. [v]
- Chetty, R., N. Hendren, P. Kline and E. Saez (2014). Where is the land of opportunity? The geography of intergenerational mobility in the United States. QJE 129(4), 1553-1623. [v]
- Coelli, M. B. (2011). Parental job loss and the education enrollment of youth. Labour Economics 18(1), 25-35. [v, earlier memo]
- Cole, C., C. Miller, R. Huang, B. Willage and E. Mayer (2024). Intergenerational effects of unemployment insurance: evidence from tax data. AEA Annual Meeting 2024 session paper. [v, conference abstract; ? working-paper version and date]
- Corak, M. (2013). Income inequality, equality of opportunity, and intergenerational mobility. JEP 27(3), 79-102. [v]
- Corak, M., B. Gustafsson and T. Osterberg (2004). Intergenerational influences on the receipt of unemployment insurance in Canada and Sweden. In Corak (ed.), Generational Income Mobility in North America and Europe, CUP. [v, earlier memo]
- Couch, K. A. and T. A. Dunn (1997). Intergenerational correlations in labor market status: a comparison of the United States and Germany. JHR 32(1). [? cited via Toledo; pages]
- Davis, J. M. V. and B. Mazumder (2022). The decline in intergenerational mobility after 1980. Chicago Fed WP 2017-05, rev. January 2022. [v WP; ? journal version]
- East, C. N. and E. Kuka (2015). Reexamining the consumption smoothing benefits of unemployment insurance. JPubE 132, 32-50. [v]
- Ekhaugen, T. (2009). Extracting the causal component from the intergenerational correlation in unemployment. JPopE 22(1), 97-113. [v, earlier memo]
- Fernandez, R., A. Fogli and C. Olivetti (2004). Mothers and sons: preference formation and female labor force dynamics. QJE 119(4), 1249-1299. [v]
- Galassi, G., D. Koll and L. Mayr (2021). The intergenerational correlation of employment. CRC TR 224 DP 309, Bonn/Mannheim. [v WP]
- Gelbach, J. B. (2016). When do covariates matter? And which ones, and how much? JOLE 34(2), 509-543. [v]
- Gibbons, R. and L. F. Katz (1991). Layoffs and lemons. JOLE 9(4), 351-380. [v]
- Grawe, N. D. (2006). Lifecycle bias in estimates of intergenerational earnings persistence. Labour Economics 13(5), 551-570. [v]
- Gregg, P., J. O. Jonsson, L. Macmillan and C. Mood (2017). The role of education for intergenerational income mobility: a comparison of the United States, Great Britain, and Sweden. Social Forces 96(1), 121-152. [v]
- Gregg, P., L. Macmillan and C. Vittori (2017). Moving towards estimating sons' lifetime intergenerational economic mobility in the UK. OBES 79(1), 79-100. [v]
- Gregg, P., L. Macmillan and C. Vittori (2019). Intergenerational income mobility: access to top jobs, the low-pay no-pay cycle and the role of education in a common framework. JPopE 32(2), 501-528. [v]
- Haider, S. and G. Solon (2006). Life-cycle variation in the association between current and lifetime earnings. AER 96(4), 1308-1320. [v]
- Hansen, K. F. and A. Stutzer (2020). Parental unemployment, social insurance and child well-being across countries. IZA DP 13752; JEBO 2022. [v WP; ? JEBO volume and pages]
- Hertz, T. (2005). Rags, riches, and race: the intergenerational economic mobility of black and white families in the United States. In Bowles, Gintis and Osborne Groves (eds.), Unequal Chances, Princeton UP, 165-191. [v]
- Hilger, N. G. (2016). Parental job loss and children's long-term outcomes: evidence from 7 million fathers' layoffs. AEJ: Applied 8(1), 247-283. [v, earlier memo]
- Holmlund, H., M. Lindahl and E. Plug (2011). The causal effect of parents' schooling on children's schooling: a comparison of estimation methods. JEL 49(3), 615-651. [v]
- Hoynes, H., D. L. Miller and J. Schaller (2012). Who suffers during recessions? JEP 26(3), 27-48. [m]
- Hsu, J. W., D. A. Matsa and B. T. Melzer (2018). Unemployment insurance as a housing market stabilizer. AER 108(1), 49-81. [v]
- Huttunen, K. and K. Riukula (2019). Parental job loss and children's careers. IZA DP 12788; published as Parental job loss and children's career choices, Labour Economics 2024, article 102578. [v; ? volume]
- Kalil, A. and K. M. Ziol-Guest (2008). Parental employment circumstances and children's academic progress. Social Science Research 37. [v, DOI 10.1016/j.ssresearch.2007.08.007; ? pages 500-515]
- Kalil, A. and P. Wightman (2011). Parental job loss and children's educational attainment in Black and White middle-class families. SSQ 92(1), 57-78. [v]
- Kuka, E. (2020). Quantifying the benefits of social insurance: unemployment insurance and health. REStat 102(3), 490-505. [v]
- Landerso, R. and J. J. Heckman (2017). The Scandinavian fantasy: the sources of intergenerational mobility in Denmark and the US. SJE 119(1), 178-230. [m; search did not confirm pages]
- Lee, C.-I. and G. Solon (2009). Trends in intergenerational income mobility. REStat 91(4), 766-772. [v]
- Lindemann, K. and M. Gangl (2020). Parental unemployment and the transition into tertiary education: can institutions moderate the adverse effects? Social Forces 99(2), 616-647. [v]
- Lindo, J. M. (2011). Parental job loss and infant health. JHE 30(5), 869-879. [v, earlier memo]
- Macmillan, L. (2014). Intergenerational worklessness in the UK and the role of local labour markets. OEP 66(3), 871-889. [v, earlier memo]
- Mader, M., S. Muller, R. T. Riphahn and C. Schwientek (2015). Intergenerational transmission of unemployment: evidence for German sons. JNS 235(4-5), 355-375. [v, earlier memo]
- Mari, G., R. Keizer and R. van Gaalen (2024). The timing of parental unemployment, insurance and children's education. European Societies 26(3), 602-638. [v]
- Mazumder, B. (2005). Fortunate sons: new estimates of intergenerational mobility in the United States using Social Security earnings data. REStat 87(2), 235-255. [v]
- Mazumder, B. (2014). Black-white differences in intergenerational economic mobility in the United States. Economic Perspectives (Chicago Fed) 38(1). [v exists; ? pages]
- Mazumder, B. (2016). Estimating the intergenerational elasticity and rank association in the United States: overcoming the current limitations of tax data. Research in Labor Economics 43 (Inequality: Causes and Consequences), Emerald. [v; ? pages]
- Mitnik, P. A. and D. B. Grusky (2020). The intergenerational elasticity of what? The case for redefining the workhorse measure of economic mobility. Sociological Methodology 50(1), 47-95. [v; not Demography]
- Mork, E., A. Sjogren and H. Svaleryd (2019). Consequences of parental job loss on the family environment and on human capital formation: evidence from workplace closures. IZA DP 12559. [v WP; ? Labour Economics 2020 version]
- Mulligan, C. B. (1997). Parental Priorities and Economic Inequality. U. Chicago Press. [? cited via Toledo]
- Nybom, M. and J. Stuhler (2016). Heterogeneous income profiles and lifecycle bias in intergenerational mobility estimation. JHR 51(1), 239-268. [v]
- Nybom, M. and J. Stuhler (2017). Biases in standard measures of intergenerational income dependence. JHR 52(3), 800-825. [v]
- O'Neill, D. and O. Sweetman (1998). Intergenerational mobility in Britain: evidence from unemployment patterns. OBES 60(4). [m; ? pages]
- Oreopoulos, P., M. Page and A. H. Stevens (2008). The intergenerational effects of worker displacement. JOLE 26(3), 455-483. [v, earlier memo]
- Page, M., A. H. Stevens and J. Lindo (2009). Parental income shocks and outcomes of disadvantaged youth in the United States. In Gruber (ed.), The Problems of Disadvantaged Youth, Chicago UP, 213-235. [v, earlier memo]
- Pfeffer, F. T. and A. Killewald (2018). Generations of advantage: multigenerational correlations in family wealth. Social Forces 96(4), 1411-1442. [v]
- Rauh, C. and A. Valladares-Esteban (2023). On the black-white gaps in labor supply and earnings over the lifecycle in the US. RED 51, 424-449. [v]
- Rege, M., K. Telle and M. Votruba (2011). Parental job loss and children's school performance. REStud 78(4), 1462-1489. [v, earlier memo]
- Rothstein, J. (2019). Inequality of educational opportunity? Schools as mediators of the intergenerational transmission of income. JOLE 37(S1), S85-S123. [v]
- Sacerdote, B. (2007). How large are the effects from changes in family environment? A study of Korean American adoptees. QJE 122(1), 119-157. [v]
- Schaller, J. and M. Zerpa. Short-run effects of parental job loss on child health. AJHE (NBER WP 21745). [v exists; ? year, volume, pages]
- Shea, J. (2000). Does parents' money matter? JPubE 77(2), 155-184. [v, earlier memo]
- Stevens, A. H. (1997). Persistent effects of job displacement: the importance of multiple job losses. JOLE 15(1), 165-188. [v]
- Stevens, A. H. and J. Schaller (2011). Short-run effects of parental job loss on children's academic achievement. EER 30(2), 289-299. [v, earlier memo]
- Toledo, M. (2006). On the intergenerational persistence of work hours. SED 2006 Meeting Paper 226. [v WP; ? ever published]
- Vosters, K. and M. Nybom (2017). Intergenerational persistence in latent socioeconomic status: evidence from Sweden and the United States. JOLE 35(3), 869-901. [v]
