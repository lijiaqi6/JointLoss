# Career wage growth and the IGE: occupational upgrading / promotion vs within-occupation growth

Built by `27.CareerWageGrowth.py` (2026-10-17); definitions in its docstring. PSID SRC + SEO sons (24's frame: 6.IGEMain parents, male heads 25-55, valid wage years), race of the parental head at 16. Every coefficient: estimate (s.e.; p), *** p<0.01, ** p<0.05, * p<0.1, s.e. clustered by 1968 family (PSID) / 1979 household (NLSY79). **Descriptive accounting: sons select into occupations and employers; nothing here is a causal effect of parental income or race.**

## Summary

- **Measurement.** All PSID (1970 / 2000 / 2010 Census) and CPS MORG (1970 / 1980 / 1990 / 2000 / 2010) occupation codes are mapped to Dorn's occ1990dd (330 occupations). Occupational wage score = mean ln hourly wage of men 25-64 in the occupation relative to all men (CPS MORG, base 1992-2002). The score accounts for about a quarter of the variance of sons' ln wages (Section 0).
- **General pattern (pooled, weighted).** The son's ln wage on ln parental income rises from 0.259*** (0.017; p=<0.001) at 25-34 to 0.410*** (0.028; p=<0.001) at 35-55. The between-occupation part (score) is 0.158*** (0.010; p=<0.001) -> 0.176*** (0.013; p=<0.001); the within-occupation part 0.102*** (0.014; p=<0.001) -> 0.235*** (0.022; p=<0.001). Between-occupation share of the level: 0.608*** (0.038; p=<0.001) at 25-34, 0.428*** (0.026; p=<0.001) at 35-55. Of the rise of the gradient after 35 (0.151*** (0.023; p=<0.001)), occupational sorting accounts for 0.018* (0.010; p=0.080) (share 0.119* (0.062; p=0.056); time-varying score 0.029*** (0.010; p=0.005)). Within sons (Section 2), wage growth from 25-34 to 35-55 rises with parental income by 0.109*** (0.019; p=<0.001), of which the occupation score 0.002 (0.008; p=0.820). **Background buys a better occupation early; career wage growth with background is growth within the occupation.**
- **Race.** At 25-34 the Black-White difference in the wage gradient (-0.090*** (0.028; p=0.001)) is almost all between occupations (-0.082*** (0.016; p=<0.001); within -0.009 (0.024; p=0.712)). The divergence after 35 - the change of the Black-White gap from 25-34 to 35-55, -0.167*** (0.037; p=<0.001) (to 45-55: -0.206*** (0.060; p=<0.001)) - is between occupations -0.031* (0.016; p=0.061) (share 0.184** (0.087; p=0.034); time-varying score -0.044*** (0.017; p=0.008), share 0.265*** (0.087; p=0.002); 11 major groups -0.021 (0.014; p=0.135)) and within occupations -0.136*** (0.032; p=<0.001). Black sons' gradient is flat in both parts (-0.013 (0.011; p=0.229) and 0.022 (0.022; p=0.323)); White sons' rises within occupations (0.158*** (0.024; p=<0.001)) with a small occupational component (0.017 (0.012; p=0.149)). Within-son career growth on parental income: Black 0.006 (0.021; p=0.786), White 0.123*** (0.021; p=<0.001); the score part -0.010 (0.009; p=0.277) / -0.007 (0.009; p=0.417).
- **When and where the within-occupation growth happens (Sections 3, 7).** Annual wage growth at 25-34 rises with parental income for White sons (0.020*** (0.005; p=<0.001)), almost all of it residual growth with the same employer (0.018*** (0.005; p=<0.001)); not for Black sons (-0.001 (0.006; p=0.861); difference -0.021*** (0.008; p=0.009)). The level gap that is visible after 35 is built by within-job wage growth in the late twenties and early thirties; after 35 the growth gradients are small (White 0.007** (0.003; p=0.042), Black -0.002 (0.004; p=0.606)). Wage-tenure profiles (person FE) steepen with parental income for White sons (tenure x ln parental income, residual 0.068*** (0.019; p=<0.001)) but not for Black sons (0.013 (0.019; p=0.489)).
- **Promotion dynamics (Sections 4-6).** Coded moves to higher-paying occupations fall with parental income (pooled 25-34 -0.031*** (0.007; p=<0.001); more churning at the bottom). Entry into supervisory / managerial occupations rises with parental income at 25-34 and 35-55 for White sons (0.024*** (0.006; p=<0.001), 0.025*** (0.007; p=<0.001)); for Black sons only at 25-34 (0.012** (0.006; p=0.032)) and not after 35 (0.000 (0.006; p=0.954); Black - White -0.024*** (0.009; p=0.010), at 25-34 -0.012 (0.008; p=0.145)). This is the closest Hegde-type pattern in the data: Black sons from richer families are not more likely to move into supervisory / managerial jobs after 35 - but the after-35 change relative to 25-34 (the triple interaction below) is not significant, and holding the position at 28-32 fixed (Section 5) the gradients are White 0.014 (0.008; p=0.103), Black -0.010 (0.006; p=0.114). Self-reported position changes with the same employer (1984-2001) rise with parental income after 35 for both (Black 0.061*** (0.018; p=<0.001), White 0.042*** (0.013; p=0.001)), with a wage gain Black 0.022** (0.010; p=0.033), White 0.026*** (0.009; p=0.002): no Black deficit in within-employer position changes. Triple interaction ln parental income x Black x 35-55 (Section 6A): supervisory entry -0.008 (0.011; p=0.452), occupation score -0.029* (0.016; p=0.072), within-occupation residual -0.134*** (0.031; p=<0.001), ln wage -0.157*** (0.035; p=<0.001).
- **Job loss (Section 8).** Displacement lowers ln wage 2-3 years later by -0.131*** (0.020; p=<0.001) (pooled), of which the occupation score -0.028*** (0.010; p=0.005); Black -0.110*** (0.027; p=<0.001) (score -0.008 (0.011; p=0.480)), White -0.148*** (0.021; p=<0.001) (score -0.035*** (0.010; p=<0.001)). Lost occupational progression is a minor part of the displacement wage loss and is not larger for Black sons (B - W difference in the score loss 0.028* (0.015; p=0.071)); job loss raises occupational churning in both directions, more for Black sons.
- **NLSY79 check (Section 9).** Same pattern: pooled gradient 25-34 / 45-55 0.252*** (0.014; p=<0.001) / 0.381*** (0.026; p=<0.001), the score part 0.133*** (0.008; p=<0.001) / 0.105*** (0.011; p=<0.001), the residual 0.119*** (0.012; p=<0.001) / 0.276*** (0.023; p=<0.001). Change of the Black-White gap (45-55) - (25-34): ln wage -0.059* (0.036; p=0.099), score 0.019 (0.019; p=0.319), residual -0.079** (0.037; p=0.034). Reported promotions (QES-PROMO39, ages 35-55) on parental income: Black 0.014* (0.007; p=0.060), White 0.025*** (0.007; p=<0.001) (difference -0.012 (0.010; p=0.222)).

**Assessment.** Occupational upgrading / promotion is not where the post-35 divergence comes from. In the pooled data background is transmitted into occupations early (half to three fifths of the wage gradient at 25-34) and that occupational component barely grows with age; the rise of wage persistence with age is growth of wages within occupations, and in the PSID most of it accrues while staying with the same employer in the late twenties and early thirties. For the race gap the same holds: Black sons' occupational disadvantage relative to their parents' income is already in place at 25-34 and does not widen much, so the between-occupation share of the divergence is small (see the shares above); the bulk is a within-occupation (largely within-job) wage-growth gradient that White sons from richer families have and Black sons do not. The closest analogue to Hegde, Ljungqvist and Raj (2026) is the flat parental-income gradient of Black sons' entry into supervisory / managerial occupations after 35 - present, but not significantly different from the gap at 25-34 and a small part of the wage gap; self-reported within-employer position changes (PSID) and reported promotions (NLSY79) show no significant Black deficit in their parental-income gradient. For the companion structural model this points to differences in human capital accumulation on the job (or in its pay-off) by background and race rather than to occupational mobility. Caveats: descriptive; the score is an occupation-level price, so 'within occupation' includes unmeasured job titles / ranks, employer pay premia and returns to skill within the occupation (a promotion that does not change the Census code counts as within-occupation); PSID occupation codes are noisy (coded independently each wave after 1980), which inflates measured occupation changes but not the level decomposition; wage = annual earnings / hours carries division bias; samples follow 24.

## 0. Occupation harmonisation, the occupational wage score and samples

Common scheme: Dorn's occ1990dd (330 occupations with a score). CPS MORG men 25-64: 2,871,125 worker-records 1979-2019 with a wage and a mapped occupation; base period 1992-2002 cells: median 772 men per occupation. Score = mean ln wage of the occupation relative to all men of the year; s.d. of the fixed score across son-years 0.324. Var(score) / Var(ln wage) among son-years: Black 0.23, White 0.25. Share of son-years in a supervisory / managerial occupation: Black 0.108, White 0.224.

| PSID code scheme (waves) | son-years with valid wage | with an occupation code | mapped to occ1990dd |
|---|---|---|---|
| 1970 (1968-2001) | 23,846 | 22,287 | 21,790 |
| 2000 (2003-2015) | 11,891 | 11,855 | 11,624 |
| 2010 (2017-2023) | 6,501 | 6,453 | 6,290 |

Sons with a valid wage year at 25-55: Black 1,928, White 2,719 (son-years Black 14,673, White 27,565). Promotion items: reported promotion waves 1976-1987 (6,750 son-years), within-employer position change 1984-2001 (18,660), tenure 1984-2023 (32,040). NLSY79 men: 2,980 with a CPS-job wage at 25-55 (45,420 person-rounds).

PSID extra items used (wave: variables): tenure months 1984 V10519, 1985 V11668, 1986 V13068, 1987 V14166, 1988 V15181, 1989 V16682, 1990 V18120, 1991 V19420, 1992 V20720; tenure years / months / weeks 1994 ER2098+2, 1995 ER5097+2, 1996 ER7193+2, 1997 ER10117+2, 1999 ER13243+2, 2001 ER17254+2, 2003 ER21171+2, 2005 ER25160+2, 2007 ER36165+2, 2009 ER42200+2, 2011 ER47513+2, 2013 ER53213+2, 2015 ER60228+2, 2017 ER66231+2, 2019 ER72231+2, 2021 ER78236+2, 2023 ER82223+2; position (B24 B25 B26 B30 B31 B27 B32 B29 B34) 1988 V15183 V15184 V15186 V15191 V15193 V15187 V15194 V15189 V15196; 1989 V16684 V16685 V16687 V16692 V16694 V16688 V16695 V16690 V16697; 1990 V18122 V18123 V18125 V18130 V18132 V18126 V18133 V18128 V18135; 1991 V19422 V19423 V19425 V19430 V19432 V19426 V19433 V19428 V19435; 1992 V20722 V20723 V20725 V20730 V20732 V20726 V20733 V20728 V20735; 1993 V22491 V22492 V22494 V22499 V22501 V22495 V22502 V22497 V22504; 1994 ER2102 ER2103 ER2105 ER2110 ER2112 ER2106 ER2113 ER2108 ER2115; 1995 ER5101 ER5102 ER5104 ER5109 ER5111 ER5105 ER5112 ER5107 ER5114; 1996 ER7197 ER7198 ER7200 ER7205 ER7207 ER7201 ER7208 ER7203 ER7210; 1997 ER10121 ER10122 ER10124 ER10129 ER10131 ER10125 ER10132 ER10127 ER10134; 1999 ER13247 ER13248 ER13250 ER13255 ER13257 ER13251 ER13258 ER13253 ER13260; 2001 ER17258 ER17259 ER17261 ER17266 ER17268 ER17262 ER17269 ER17264 ER17271; months in present position 1984 V10520, 1985 V11669, 1986 V13069, 1987 V14167; why previous job / position ended (E branch, code 6 = promotion) 1976 V4490, 1977 V5399, 1978 V5890, 1979 V6501, 1980 V7104, 1981 V7727, 1982 V8391, 1983 V9022, 1984 V10539, 1985 V11679, 1986 V13079, 1987 V14177.

## 1. Wage persistence by age band: between occupations vs within occupation

One regression per cell: the son's outcome (column header) on ln parental income (6.IGEMain regressor), child-years in the age band, Lee-Solon controls without the x-age interactions (24 section 1b). ln wage = occupation score + within-occupation residual, so (1) = (2) + (3) = (5) + (6) = (7) + (8) on the same sample (son-years with a valid wage and a mapped occupation). All cells are estimated as one stacked system (influence functions clustered by 1968 family), so differences across bands and races and the share in (4) (delta method) have proper s.e. Pooled = Black + White sons with the son's individual weight; Black and White unweighted (as in 24). Column (4) is left blank when the denominator is not different from zero (|t| < 2). **Accounting, not causal: sons select into occupations.**

| | (1) ln wage | (2) occupation score | (3) within-occupation residual | (4) share between = (2)/(1) | (5) occupation score, time-varying | (6) residual, time-varying | (7) score, 11 major groups | (8) residual, 11 groups |
|---|---|---|---|---|---|---|---|---|
| **Pooled (weighted)** | | | | | | | | |
| ln parental income, sons 25-34 | 0.259*** (0.017; p=<0.001) | 0.158*** (0.010; p=<0.001) | 0.102*** (0.014; p=<0.001) | 0.608*** (0.038; p=<0.001) | 0.158*** (0.010; p=<0.001) | 0.102*** (0.014; p=<0.001) | 0.128*** (0.008; p=<0.001) | 0.133*** (0.015; p=<0.001) |
| ln parental income, sons 35-44 | 0.401*** (0.026; p=<0.001) | 0.174*** (0.012; p=<0.001) | 0.227*** (0.021; p=<0.001) | 0.433*** (0.027; p=<0.001) | 0.183*** (0.012; p=<0.001) | 0.218*** (0.021; p=<0.001) | 0.142*** (0.010; p=<0.001) | 0.259*** (0.023; p=<0.001) |
| ln parental income, sons 45-55 | 0.429*** (0.039; p=<0.001) | 0.179*** (0.017; p=<0.001) | 0.250*** (0.033; p=<0.001) | 0.416*** (0.037; p=<0.001) | 0.196*** (0.018; p=<0.001) | 0.233*** (0.033; p=<0.001) | 0.154*** (0.016; p=<0.001) | 0.275*** (0.037; p=<0.001) |
| ln parental income, sons 35-55 | 0.410*** (0.028; p=<0.001) | 0.176*** (0.013; p=<0.001) | 0.235*** (0.022; p=<0.001) | 0.428*** (0.026; p=<0.001) | 0.187*** (0.013; p=<0.001) | 0.223*** (0.022; p=<0.001) | 0.146*** (0.011; p=<0.001) | 0.264*** (0.025; p=<0.001) |
| ln parental income, sons 25-55 | 0.340*** (0.020; p=<0.001) | 0.167*** (0.010; p=<0.001) | 0.173*** (0.016; p=<0.001) | 0.492*** (0.026; p=<0.001) | 0.174*** (0.010; p=<0.001) | 0.166*** (0.016; p=<0.001) | 0.137*** (0.009; p=<0.001) | 0.203*** (0.018; p=<0.001) |
| N son-years / sons / clusters (cols 1-4) | 25-34: 21,315/4,314/1,686 ; 35-44: 12,648/2,916/1,399 ; 45-55: 5,728/1,511/944 |  |  |  |  |  |  |  |
| **Black** | | | | | | | | |
| ln parental income, sons 25-34 | 0.152*** (0.020; p=<0.001) | 0.073*** (0.011; p=<0.001) | 0.079*** (0.017; p=<0.001) | 0.480*** (0.064; p=<0.001) | 0.064*** (0.011; p=<0.001) | 0.088*** (0.016; p=<0.001) | 0.057*** (0.009; p=<0.001) | 0.096*** (0.018; p=<0.001) |
| ln parental income, sons 35-44 | 0.159*** (0.029; p=<0.001) | 0.056*** (0.014; p=<0.001) | 0.103*** (0.023; p=<0.001) | 0.351*** (0.069; p=<0.001) | 0.049*** (0.014; p=<0.001) | 0.111*** (0.023; p=<0.001) | 0.047*** (0.012; p=<0.001) | 0.112*** (0.024; p=<0.001) |
| ln parental income, sons 45-55 | 0.160*** (0.046; p=<0.001) | 0.067*** (0.020; p=0.001) | 0.093** (0.037; p=0.012) | 0.420*** (0.111; p=<0.001) | 0.059*** (0.021; p=0.005) | 0.101*** (0.036; p=0.005) | 0.067*** (0.018; p=<0.001) | 0.091** (0.038; p=0.017) |
| ln parental income, sons 35-55 | 0.161*** (0.030; p=<0.001) | 0.060*** (0.014; p=<0.001) | 0.101*** (0.024; p=<0.001) | 0.371*** (0.068; p=<0.001) | 0.052*** (0.014; p=<0.001) | 0.108*** (0.024; p=<0.001) | 0.053*** (0.013; p=<0.001) | 0.107*** (0.025; p=<0.001) |
| ln parental income, sons 25-55 | 0.156*** (0.022; p=<0.001) | 0.067*** (0.011; p=<0.001) | 0.089*** (0.017; p=<0.001) | 0.431*** (0.056; p=<0.001) | 0.059*** (0.011; p=<0.001) | 0.097*** (0.017; p=<0.001) | 0.055*** (0.010; p=<0.001) | 0.100*** (0.018; p=<0.001) |
| N son-years / sons / clusters (cols 1-4) | 25-34: 7,412/1,727/615 ; 35-44: 4,149/1,080/483 ; 45-55: 1,843/509/296 |  |  |  |  |  |  |  |
| **White** | | | | | | | | |
| ln parental income, sons 25-34 | 0.243*** (0.020; p=<0.001) | 0.155*** (0.012; p=<0.001) | 0.088*** (0.017; p=<0.001) | 0.638*** (0.049; p=<0.001) | 0.152*** (0.012; p=<0.001) | 0.090*** (0.016; p=<0.001) | 0.127*** (0.010; p=<0.001) | 0.116*** (0.018; p=<0.001) |
| ln parental income, sons 35-44 | 0.405*** (0.032; p=<0.001) | 0.171*** (0.014; p=<0.001) | 0.234*** (0.026; p=<0.001) | 0.423*** (0.030; p=<0.001) | 0.180*** (0.015; p=<0.001) | 0.226*** (0.025; p=<0.001) | 0.141*** (0.013; p=<0.001) | 0.264*** (0.028; p=<0.001) |
| ln parental income, sons 45-55 | 0.456*** (0.047; p=<0.001) | 0.175*** (0.022; p=<0.001) | 0.281*** (0.038; p=<0.001) | 0.383*** (0.039; p=<0.001) | 0.198*** (0.022; p=<0.001) | 0.258*** (0.037; p=<0.001) | 0.156*** (0.021; p=<0.001) | 0.301*** (0.042; p=<0.001) |
| ln parental income, sons 35-55 | 0.418*** (0.033; p=<0.001) | 0.172*** (0.015; p=<0.001) | 0.246*** (0.026; p=<0.001) | 0.411*** (0.028; p=<0.001) | 0.185*** (0.015; p=<0.001) | 0.234*** (0.025; p=<0.001) | 0.145*** (0.014; p=<0.001) | 0.274*** (0.029; p=<0.001) |
| ln parental income, sons 25-55 | 0.320*** (0.023; p=<0.001) | 0.162*** (0.012; p=<0.001) | 0.157*** (0.018; p=<0.001) | 0.508*** (0.030; p=<0.001) | 0.166*** (0.012; p=<0.001) | 0.153*** (0.017; p=<0.001) | 0.135*** (0.011; p=<0.001) | 0.185*** (0.019; p=<0.001) |
| N son-years / sons / clusters (cols 1-4) | 25-34: 13,915/2,590/1,078 ; 35-44: 8,500/1,837/921 ; 45-55: 3,885/1,002/649 |  |  |  |  |  |  |  |
| **Black - White** | | | | | | | | |
| ln parental income, sons 25-34 | -0.090*** (0.028; p=0.001) | -0.082*** (0.016; p=<0.001) | -0.009 (0.024; p=0.712) | 0.903*** (0.238; p=<0.001) | -0.088*** (0.016; p=<0.001) | -0.002 (0.023; p=0.916) | -0.070*** (0.014; p=<0.001) | -0.020 (0.025; p=0.411) |
| ln parental income, sons 35-44 | -0.246*** (0.043; p=<0.001) | -0.115*** (0.020; p=<0.001) | -0.131*** (0.035; p=<0.001) | 0.469*** (0.071; p=<0.001) | -0.131*** (0.020; p=<0.001) | -0.115*** (0.034; p=<0.001) | -0.094*** (0.017; p=<0.001) | -0.152*** (0.037; p=<0.001) |
| ln parental income, sons 45-55 | -0.296*** (0.066; p=<0.001) | -0.108*** (0.030; p=<0.001) | -0.188*** (0.053; p=<0.001) | 0.364*** (0.083; p=<0.001) | -0.139*** (0.030; p=<0.001) | -0.157*** (0.052; p=0.003) | -0.089*** (0.028; p=0.001) | -0.210*** (0.057; p=<0.001) |
| ln parental income, sons 35-55 | -0.258*** (0.045; p=<0.001) | -0.112*** (0.020; p=<0.001) | -0.145*** (0.035; p=<0.001) | 0.436*** (0.065; p=<0.001) | -0.132*** (0.021; p=<0.001) | -0.125*** (0.035; p=<0.001) | -0.092*** (0.019; p=<0.001) | -0.167*** (0.038; p=<0.001) |
| ln parental income, sons 25-55 | -0.164*** (0.032; p=<0.001) | -0.095*** (0.016; p=<0.001) | -0.069*** (0.024; p=0.005) | 0.581*** (0.089; p=<0.001) | -0.107*** (0.016; p=<0.001) | -0.057** (0.024; p=0.018) | -0.080*** (0.014; p=<0.001) | -0.085*** (0.026; p=0.001) |
| **Change in the coefficient across age bands (career divergence)** | | | | | | | | |
| Pooled (weighted): (45-55) - (25-34) | 0.169*** (0.035; p=<0.001) | 0.021 (0.015; p=0.162) | 0.148*** (0.032; p=<0.001) | 0.124 (0.081; p=0.128) | 0.038** (0.015; p=0.015) | 0.132*** (0.032; p=<0.001) | 0.026* (0.014; p=0.059) | 0.143*** (0.035; p=<0.001) |
| Pooled (weighted): (35-55) - (25-34) | 0.151*** (0.023; p=<0.001) | 0.018* (0.010; p=0.080) | 0.133*** (0.021; p=<0.001) | 0.119* (0.062; p=0.056) | 0.029*** (0.010; p=0.005) | 0.122*** (0.020; p=<0.001) | 0.018** (0.009; p=0.038) | 0.132*** (0.022; p=<0.001) |
| Black: (45-55) - (25-34) | 0.008 (0.042; p=0.850) | -0.006 (0.019; p=0.753) | 0.014 (0.036; p=0.703) |  | -0.005 (0.019; p=0.790) | 0.013 (0.036; p=0.715) | 0.010 (0.017; p=0.527) | -0.005 (0.037; p=0.903) |
| Black: (35-55) - (25-34) | 0.009 (0.025; p=0.734) | -0.013 (0.011; p=0.229) | 0.022 (0.022; p=0.323) |  | -0.012 (0.011; p=0.288) | 0.021 (0.022; p=0.350) | -0.004 (0.010; p=0.715) | 0.011 (0.023; p=0.633) |
| White: (45-55) - (25-34) | 0.213*** (0.042; p=<0.001) | 0.020 (0.020; p=0.302) | 0.193*** (0.037; p=<0.001) | 0.095 (0.084; p=0.258) | 0.046** (0.020; p=0.018) | 0.167*** (0.036; p=<0.001) | 0.029 (0.018; p=0.107) | 0.185*** (0.039; p=<0.001) |
| White: (35-55) - (25-34) | 0.176*** (0.027; p=<0.001) | 0.017 (0.012; p=0.149) | 0.158*** (0.024; p=<0.001) | 0.099 (0.063; p=0.117) | 0.032*** (0.012; p=0.009) | 0.144*** (0.023; p=<0.001) | 0.018* (0.010; p=0.084) | 0.158*** (0.025; p=<0.001) |
| Black - White: (45-55) - (25-34) | -0.206*** (0.060; p=<0.001) | -0.026 (0.027; p=0.334) | -0.179*** (0.051; p=<0.001) | 0.127 (0.117; p=0.278) | -0.051* (0.027; p=0.060) | -0.154*** (0.050; p=0.002) | -0.018 (0.024; p=0.450) | -0.190*** (0.054; p=<0.001) |
| Black - White: (35-55) - (25-34) | -0.167*** (0.037; p=<0.001) | -0.031* (0.016; p=0.061) | -0.136*** (0.032; p=<0.001) | 0.184** (0.087; p=0.034) | -0.044*** (0.017; p=0.008) | -0.123*** (0.032; p=<0.001) | -0.021 (0.014; p=0.135) | -0.147*** (0.034; p=<0.001) |

## 2. Career wage growth within sons

One row per son observed with >= 2 valid years (wage and occupation) at 25-34 and >= 2 at 35-55. Outcome = mean at 35-55 minus mean at 25-34 (column header); regressor ln parental income; controls: quadratics in the father's age at 16, the son's mean age in each window and his birth year. (1) = (2) + (3). Pooled weighted by the son's mean individual weight at 35-55; s.e. clustered by 1968 family.

| | (1) growth of ln wage | (2) growth of occupation score | (3) growth of within-occupation residual | (4) share between = (2)/(1) | (5) mean ln wage at 25-34 | (6) mean growth of ln wage |
|---|---|---|---|---|---|---|
| **Pooled (weighted)** | | | | | | |
| ln parental income | 0.109*** (0.019; p=<0.001) | 0.002 (0.008; p=0.820) | 0.108*** (0.019; p=<0.001) | 0.016 (0.070; p=0.818) |  |  |
| Mean |  |  |  |  | 2.668 | 0.281 |
| N sons / clusters | 2,293 / 1,223 | 2,293 / 1,223 | 2,293 / 1,223 | 2,293 / 1,223 |  |  |
| **Black** | | | | | | |
| ln parental income | 0.006 (0.021; p=0.786) | -0.010 (0.009; p=0.277) | 0.016 (0.021; p=0.450) |  |  |  |
| Mean |  |  |  |  | 2.389 | 0.155 |
| N sons / clusters | 750 / 396 | 750 / 396 | 750 / 396 | 750 / 396 |  |  |
| **White** | | | | | | |
| ln parental income | 0.123*** (0.021; p=<0.001) | -0.007 (0.009; p=0.417) | 0.130*** (0.022; p=<0.001) | -0.060 (0.076; p=0.429) |  |  |
| Mean |  |  |  |  | 2.702 | 0.275 |
| N sons / clusters | 1,543 / 829 | 1,543 / 829 | 1,543 / 829 | 1,543 / 829 |  |  |
| **Black - White** | | | | | | |
| ln parental income | -0.117*** (0.030; p=<0.001) | -0.003 (0.013; p=0.824) | -0.114*** (0.030; p=<0.001) | 0.025 (0.112; p=0.822) |  |  |

## 3. Annual wage growth: occupational upgrading vs within-occupation growth, within vs across employers

Consecutive interviews (1-2 years apart, waves 1985-2023) with a valid wage, a mapped occupation and tenure with the present employer at the later interview. Annualised growth of ln wage (income years w_prev - 1 -> w - 1) = growth of the occupation score + growth of the residual, each split by whether the son stayed with the same employer (tenure >= years since the previous interview - 0.5) or not: (1) = (2) + (3) + (4) + (5). (6) = share of stayers. Controls: quartic in age, year FE. Within-employer score growth is promotion into a better-paid occupation with the same employer; residual growth with the same employer is within-job (and within-occupation) wage growth. Measurement error in occupation codes inflates score changes in both directions.

| | (1) annual ln wage growth | (2) score growth, same employer | (3) residual growth, same employer | (4) score growth, new employer | (5) residual growth, new employer | (6) stayed with employer |
|---|---|---|---|---|---|---|
| **Pooled (weighted)** | | | | | | |
| ln parental income, sons 25-34 | 0.015*** (0.005; p=0.001) | 0.001 (0.002; p=0.658) | 0.010** (0.004; p=0.027) | 0.002 (0.001; p=0.121) | 0.003 (0.003; p=0.422) | 0.022** (0.009; p=0.014) |
| Mean, 25-34 | 0.0544 | 0.0094 | 0.0393 | 0.0018 | 0.0039 | 0.8119 |
| N son-year pairs / clusters, 25-34 | 11,578 / 1,500 | 11,578 / 1,500 | 11,578 / 1,500 | 11,578 / 1,500 | 11,578 / 1,500 | 11,578 / 1,500 |
| ln parental income, sons 35-55 | 0.004 (0.003; p=0.189) | -0.002* (0.001; p=0.081) | 0.003 (0.003; p=0.284) | 0.000 (0.001; p=0.603) | 0.002 (0.002; p=0.352) | 0.020** (0.008; p=0.015) |
| Mean, 35-55 | 0.0196 | 0.0019 | 0.0166 | -0.0011 | 0.0023 | 0.8648 |
| N son-year pairs / clusters, 35-55 | 14,185 / 1,296 | 14,185 / 1,296 | 14,185 / 1,296 | 14,185 / 1,296 | 14,185 / 1,296 | 14,185 / 1,296 |
| **Black** | | | | | | |
| ln parental income, sons 25-34 | -0.001 (0.006; p=0.861) | 0.004 (0.003; p=0.175) | -0.000 (0.007; p=0.987) | 0.003 (0.002; p=0.226) | -0.008 (0.005; p=0.135) | 0.018 (0.013; p=0.141) |
| Mean, 25-34 | 0.0417 | 0.0033 | 0.0405 | 0.0008 | -0.0029 | 0.7962 |
| N son-year pairs / clusters, 25-34 | 3,725 / 524 | 3,725 / 524 | 3,725 / 524 | 3,725 / 524 | 3,725 / 524 | 3,725 / 524 |
| ln parental income, sons 35-55 | -0.002 (0.004; p=0.606) | -0.001 (0.002; p=0.428) | 0.001 (0.004; p=0.849) | -0.001 (0.001; p=0.554) | -0.001 (0.003; p=0.812) | -0.011 (0.012; p=0.349) |
| Mean, 35-55 | 0.0152 | 0.0031 | 0.0132 | 0.0003 | -0.0015 | 0.8552 |
| N son-year pairs / clusters, 35-55 | 4,537 / 435 | 4,537 / 435 | 4,537 / 435 | 4,537 / 435 | 4,537 / 435 | 4,537 / 435 |
| **White** | | | | | | |
| ln parental income, sons 25-34 | 0.020*** (0.005; p=<0.001) | 0.000 (0.002; p=0.846) | 0.018*** (0.005; p=<0.001) | 0.001 (0.001; p=0.479) | 0.001 (0.003; p=0.766) | 0.020** (0.010; p=0.041) |
| Mean, 25-34 | 0.0540 | 0.0096 | 0.0375 | 0.0022 | 0.0047 | 0.8218 |
| N son-year pairs / clusters, 25-34 | 7,862 / 983 | 7,862 / 983 | 7,862 / 983 | 7,862 / 983 | 7,862 / 983 | 7,862 / 983 |
| ln parental income, sons 35-55 | 0.007** (0.003; p=0.042) | -0.001 (0.001; p=0.397) | 0.003 (0.004; p=0.421) | 0.001 (0.001; p=0.377) | 0.004** (0.002; p=0.037) | 0.025*** (0.009; p=0.006) |
| Mean, 35-55 | 0.0207 | 0.0017 | 0.0183 | -0.0009 | 0.0016 | 0.8723 |
| N son-year pairs / clusters, 35-55 | 9,649 / 867 | 9,649 / 867 | 9,649 / 867 | 9,649 / 867 | 9,649 / 867 | 9,649 / 867 |
| **Black - White** | | | | | | |
| ln parental income, sons 25-34 | -0.021*** (0.008; p=0.009) | 0.003 (0.004; p=0.335) | -0.018** (0.008; p=0.035) | 0.002 (0.003; p=0.518) | -0.009 (0.006; p=0.151) | -0.001 (0.016; p=0.936) |
| ln parental income, sons 35-55 | -0.009* (0.005; p=0.085) | -0.000 (0.002; p=0.951) | -0.002 (0.005; p=0.663) | -0.002 (0.001; p=0.303) | -0.005 (0.004; p=0.201) | -0.036** (0.015; p=0.017) |

## 4. Promotion and occupational upgrading per year, by parental income

Son-year linear probability models (column header = outcome), male heads, controls: quartic in age, year FE; s.e. clustered by 1968 family. (1)-(4), (8): change of the (consistent occ1990dd) occupation between consecutive interviews 1-2 years apart (score = fixed 1992-2002 relative wage); (3) among sons not in a supervisory / managerial occupation at the previous interview. (5) employed head whose job / position began within about a year says the previous one ended by promotion (waves 1976-1987; sons mostly < 40 then). (6) the present position with the present employer began since January of the previous calendar year (two years before in 1999 / 2001) and after the start with the employer (waves 1984-2001); (7) the same with a rise in the annual ln wage since the previous interview. Coded occupation changes include coding noise (PSID occupations are coded independently each wave after 1980), so (1)-(4) overstate true mobility; (6)-(7) are self-reported.

| | (1) moved to a higher-paying occupation | (2) ... by >= 0.10 log points | (3) entered a supervisory / managerial occupation | (4) annual change in score | (5) reported promotion (1976-87) | (6) position change, same employer (1984-2001) | (7) ... with a wage gain | (8) moved to a lower-paying occupation (>= 0.10) |
|---|---|---|---|---|---|---|---|---|
| **Pooled (weighted)** | | | | | | | | |
| ln parental income, sons 25-34 | -0.031*** (0.007; p=<0.001) | -0.021*** (0.006; p=0.001) | 0.028*** (0.005; p=<0.001) | 0.002 (0.002; p=0.161) | 0.012* (0.006; p=0.059) | 0.012 (0.009; p=0.173) | 0.004 (0.007; p=0.595) | -0.017*** (0.006; p=0.005) |
| Mean of outcome, 25-34 | 0.250 | 0.189 | 0.087 | 0.012 | 0.054 | 0.141 | 0.090 | 0.156 |
| N son-years / clusters, 25-34 | 17,198 / 1,613 | 17,198 / 1,613 | 14,660 / 1,584 | 17,198 / 1,613 | 6,547 / 907 | 11,063 / 1,368 | 8,709 / 1,224 | 17,198 / 1,613 |
| ln parental income, sons 35-55 | -0.024*** (0.006; p=<0.001) | -0.016*** (0.005; p=0.002) | 0.029*** (0.006; p=<0.001) | -0.002* (0.001; p=0.095) |  | 0.033*** (0.011; p=0.004) | 0.019** (0.008; p=0.013) | -0.006 (0.006; p=0.264) |
| Mean of outcome, 35-55 | 0.188 | 0.143 | 0.089 | -0.000 |  | 0.128 | 0.072 | 0.143 |
| N son-years / clusters, 35-55 | 18,043 / 1,395 | 18,043 / 1,395 | 14,084 / 1,343 | 18,043 / 1,395 |  | 7,587 / 952 | 6,711 / 885 | 18,043 / 1,395 |
| **Black** | | | | | | | | |
| ln parental income, sons 25-34 | -0.011 (0.010; p=0.236) | -0.012 (0.009; p=0.143) | 0.012** (0.006; p=0.032) | 0.004* (0.002; p=0.068) | 0.009 (0.010; p=0.339) | 0.041*** (0.009; p=<0.001) | 0.021** (0.009; p=0.015) | -0.018** (0.008; p=0.031) |
| Mean of outcome, 25-34 | 0.269 | 0.196 | 0.043 | 0.006 | 0.035 | 0.104 | 0.061 | 0.175 |
| N son-years / clusters, 25-34 | 5,825 / 576 | 5,825 / 576 | 5,336 / 572 | 5,825 / 576 | 2,375 / 361 | 3,735 / 479 | 2,754 / 424 | 5,825 / 576 |
| ln parental income, sons 35-55 | -0.011 (0.009; p=0.184) | -0.008 (0.007; p=0.283) | 0.000 (0.006; p=0.954) | -0.002 (0.001; p=0.186) |  | 0.061*** (0.018; p=<0.001) | 0.022** (0.010; p=0.033) | 0.000 (0.007; p=0.963) |
| Mean of outcome, 35-55 | 0.214 | 0.159 | 0.053 | 0.003 |  | 0.102 | 0.061 | 0.151 |
| N son-years / clusters, 35-55 | 5,766 / 479 | 5,766 / 479 | 5,048 / 470 | 5,766 / 479 |  | 2,423 / 340 | 2,019 / 296 | 5,766 / 479 |
| **White** | | | | | | | | |
| ln parental income, sons 25-34 | -0.024*** (0.007; p=<0.001) | -0.020*** (0.006; p=0.002) | 0.024*** (0.006; p=<0.001) | 0.001 (0.002; p=0.706) | 0.015* (0.008; p=0.052) | 0.007 (0.010; p=0.496) | 0.003 (0.008; p=0.750) | -0.010 (0.006; p=0.114) |
| Mean of outcome, 25-34 | 0.242 | 0.184 | 0.089 | 0.012 | 0.055 | 0.140 | 0.088 | 0.153 |
| N son-years / clusters, 25-34 | 11,382 / 1,043 | 11,382 / 1,043 | 9,333 / 1,018 | 11,382 / 1,043 | 4,172 / 546 | 7,338 / 890 | 5,963 / 800 | 11,382 / 1,043 |
| ln parental income, sons 35-55 | -0.019** (0.007; p=0.011) | -0.015** (0.006; p=0.017) | 0.025*** (0.007; p=<0.001) | -0.001 (0.001; p=0.449) |  | 0.042*** (0.013; p=0.001) | 0.026*** (0.009; p=0.002) | -0.006 (0.007; p=0.376) |
| Mean of outcome, 35-55 | 0.187 | 0.143 | 0.095 | 0.000 |  | 0.125 | 0.069 | 0.143 |
| N son-years / clusters, 35-55 | 12,278 / 921 | 12,278 / 921 | 9,037 / 877 | 12,278 / 921 |  | 5,164 / 612 | 4,692 / 589 | 12,278 / 921 |
| **Black - White** | | | | | | | | |
| ln parental income, sons 25-34 | 0.013 (0.012; p=0.282) | 0.008 (0.011; p=0.463) | -0.012 (0.008; p=0.145) | 0.004 (0.003; p=0.224) | -0.005 (0.012; p=0.654) | 0.034** (0.014; p=0.012) | 0.018 (0.012; p=0.120) | -0.007 (0.010; p=0.473) |
| ln parental income, sons 35-55 | 0.008 (0.011; p=0.507) | 0.008 (0.010; p=0.428) | -0.024*** (0.009; p=0.010) | -0.001 (0.002; p=0.646) |  | 0.019 (0.022; p=0.378) | -0.004 (0.013; p=0.758) | 0.006 (0.010; p=0.522) |

## 5. Upgrading after 35, conditional on education and the starting position

As Section 4, sons 35-55 who are observed at 28-32 (mean ln wage and occupation score there), adding years of education. The coefficient on ln parental income is then the gradient of progression for sons who started from the same position at 30.

| | (1) moved to a higher-paying occupation | (2) ... by >= 0.10 log points | (3) entered a supervisory / managerial occupation | (4) annual change in score | (6) position change, same employer (1984-2001) | (7) ... with a wage gain | (8) moved to a lower-paying occupation (>= 0.10) |
|---|---|---|---|---|---|---|---|
| **Pooled (weighted), sons 35-55** | | | | | | | |
| ln parental income | -0.006 (0.007; p=0.398) | -0.000 (0.006; p=0.969) | 0.015** (0.007; p=0.023) | -0.000 (0.001; p=0.835) | 0.005 (0.013; p=0.711) | 0.002 (0.009; p=0.819) | 0.003 (0.006; p=0.664) |
| years of education | -0.001 (0.002; p=0.583) | -0.001 (0.002; p=0.753) | 0.001 (0.002; p=0.634) | 0.001** (0.000; p=0.020) | 0.007** (0.004; p=0.039) | 0.004* (0.003; p=0.088) | -0.005** (0.002; p=0.024) |
| mean ln wage at 28-32 | 0.000 (0.009; p=0.976) | -0.000 (0.008; p=0.974) | 0.014* (0.008; p=0.094) | 0.003** (0.001; p=0.020) | 0.069*** (0.015; p=<0.001) | 0.035*** (0.009; p=<0.001) | -0.020** (0.008; p=0.015) |
| mean occupation score at 28-32 | -0.075*** (0.018; p=<0.001) | -0.069*** (0.016; p=<0.001) | 0.044*** (0.016; p=0.005) | -0.021*** (0.003; p=<0.001) | -0.026 (0.027; p=0.338) | -0.001 (0.021; p=0.953) | 0.029** (0.015; p=0.050) |
| N son-years / clusters | 16,367 / 1,292 | 16,367 / 1,292 | 12,692 / 1,239 | 16,367 / 1,292 | 6,728 / 846 | 6,143 / 805 | 16,367 / 1,292 |
| **Black, sons 35-55** | | | | | | | |
| ln parental income | -0.001 (0.010; p=0.931) | 0.003 (0.007; p=0.690) | -0.010 (0.006; p=0.114) | -0.001 (0.002; p=0.734) | 0.050** (0.021; p=0.020) | 0.017 (0.012; p=0.145) | 0.007 (0.008; p=0.380) |
| years of education | 0.001 (0.004; p=0.809) | 0.002 (0.003; p=0.624) | 0.007** (0.003; p=0.014) | 0.001 (0.001; p=0.410) | 0.004 (0.005; p=0.387) | 0.002 (0.003; p=0.485) | -0.001 (0.003; p=0.817) |
| mean ln wage at 28-32 | -0.034** (0.015; p=0.018) | -0.042*** (0.012; p=<0.001) | 0.013 (0.010; p=0.188) | 0.001 (0.003; p=0.623) | 0.038** (0.019; p=0.049) | 0.013 (0.017; p=0.460) | -0.052*** (0.012; p=<0.001) |
| mean occupation score at 28-32 | -0.064** (0.031; p=0.040) | -0.063** (0.026; p=0.013) | 0.028 (0.021; p=0.182) | -0.022*** (0.006; p=<0.001) | -0.002 (0.043; p=0.958) | 0.019 (0.035; p=0.595) | 0.027 (0.023; p=0.248) |
| N son-years / clusters | 4,894 / 427 | 4,894 / 427 | 4,263 / 416 | 4,894 / 427 | 1,978 / 283 | 1,742 / 257 | 4,894 / 427 |
| **White, sons 35-55** | | | | | | | |
| ln parental income | -0.002 (0.009; p=0.776) | -0.002 (0.008; p=0.841) | 0.014 (0.008; p=0.103) | 0.000 (0.002; p=0.950) | 0.011 (0.015; p=0.473) | 0.008 (0.009; p=0.400) | 0.003 (0.008; p=0.731) |
| years of education | -0.000 (0.003; p=0.897) | -0.000 (0.002; p=0.916) | 0.001 (0.002; p=0.683) | 0.001*** (0.000; p=0.001) | 0.008** (0.004; p=0.025) | 0.004* (0.003; p=0.082) | -0.005** (0.002; p=0.022) |
| mean ln wage at 28-32 | 0.009 (0.009; p=0.353) | 0.009 (0.008; p=0.283) | 0.010 (0.009; p=0.284) | 0.004** (0.002; p=0.018) | 0.070*** (0.015; p=<0.001) | 0.035*** (0.009; p=<0.001) | -0.014 (0.008; p=0.110) |
| mean occupation score at 28-32 | -0.082*** (0.019; p=<0.001) | -0.074*** (0.017; p=<0.001) | 0.048*** (0.017; p=0.006) | -0.023*** (0.003; p=<0.001) | -0.028 (0.027; p=0.312) | -0.003 (0.022; p=0.884) | 0.021 (0.016; p=0.175) |
| N son-years / clusters | 11,474 / 869 | 11,474 / 869 | 8,430 / 826 | 11,474 / 869 | 4,750 / 563 | 4,401 / 548 | 11,474 / 869 |

## 6. Do Black sons from higher-income families progress less after 35? (Hegde et al. analogue)

Black and White sons pooled (unweighted), son-years 25-55, one regression per column (outcome in the header) with the full set of interactions of ln parental income (centred at the sample mean), Black and age 35-55. The triple interaction is the difference in the after-35 change of the parental-income gradient between Black and White sons; 'Black x age 35-55' is the Black-White difference in the after-35 change at mean parental income. Hegde, Ljungqvist and Raj (2026) find that equally entitled Black examiners are promoted later, especially at senior grades; the analogue here is a negative triple interaction / Black x 35-55 term for upgrading outcomes.

| | ln wage | occupation score | within-occupation residual | moved to higher-paying occupation | entered supervisory / managerial | annual change in score | position change, same employer | position change with wage gain |
|---|---|---|---|---|---|---|---|---|
| **A. unconditional** | | | | | | | | |
| ln parental income (centred) | 0.279*** (0.019; p=<0.001) | 0.162*** (0.011; p=<0.001) | 0.109*** (0.016; p=<0.001) | -0.023*** (0.007; p=0.002) | 0.024*** (0.006; p=<0.001) | 0.001 (0.002; p=0.700) | 0.007 (0.010; p=0.484) | 0.003 (0.008; p=0.744) |
| x age 35-55 | 0.137*** (0.026; p=<0.001) | 0.013 (0.012; p=0.258) | 0.136*** (0.023; p=<0.001) | 0.003 (0.010; p=0.768) | -0.001 (0.008; p=0.905) | -0.002 (0.003; p=0.472) | 0.032** (0.015; p=0.039) | 0.022* (0.011; p=0.052) |
| Black | -0.166*** (0.020; p=<0.001) | -0.121*** (0.012; p=<0.001) | -0.039** (0.017; p=0.022) | 0.024*** (0.008; p=0.003) | -0.031*** (0.006; p=<0.001) | -0.004* (0.002; p=0.065) | -0.014 (0.010; p=0.137) | -0.015* (0.008; p=0.054) |
| Black x age 35-55 | -0.064*** (0.023; p=0.006) | -0.026** (0.012; p=0.025) | -0.035* (0.021; p=0.090) | -0.006 (0.010; p=0.580) | -0.001 (0.008; p=0.884) | 0.005* (0.003; p=0.065) | 0.037** (0.017; p=0.033) | 0.028** (0.012; p=0.017) |
| ln parental income x Black | -0.100*** (0.027; p=<0.001) | -0.085*** (0.016; p=<0.001) | -0.013 (0.023; p=0.572) | 0.014 (0.012; p=0.213) | -0.011 (0.008; p=0.168) | 0.004 (0.003; p=0.175) | 0.033** (0.014; p=0.017) | 0.017 (0.012; p=0.145) |
| ln parental income x Black x age 35-55 | -0.157*** (0.035; p=<0.001) | -0.029* (0.016; p=0.072) | -0.134*** (0.031; p=<0.001) | -0.007 (0.015; p=0.653) | -0.008 (0.011; p=0.452) | -0.005 (0.004; p=0.208) | -0.007 (0.025; p=0.766) | -0.018 (0.017; p=0.297) |
| Controls | age quartic, year FE, age 35-55 dummy | age quartic, year FE, age 35-55 dummy | age quartic, year FE, age 35-55 dummy | age quartic, year FE, age 35-55 dummy | age quartic, year FE, age 35-55 dummy | age quartic, year FE, age 35-55 dummy | age quartic, year FE, age 35-55 dummy | age quartic, year FE, age 35-55 dummy |
| N son-years / clusters | 42,238 / 1,747 | 39,704 / 1,728 | 39,704 / 1,728 | 35,251 / 1,681 | 28,754 / 1,660 | 35,251 / 1,681 | 18,660 / 1,432 | 15,428 / 1,305 |
| **B. conditional on education and the position at 28-32** | | | | | | | | |
| ln parental income (centred) | 0.006 (0.008; p=0.469) | 0.011*** (0.004; p=0.006) | -0.010 (0.008; p=0.219) | -0.004 (0.008; p=0.585) | 0.011* (0.007; p=0.087) | 0.001 (0.002; p=0.658) | -0.018* (0.010; p=0.070) | -0.016* (0.008; p=0.054) |
| x age 35-55 | 0.138*** (0.021; p=<0.001) | -0.002 (0.010; p=0.808) | 0.145*** (0.021; p=<0.001) | 0.005 (0.010; p=0.586) | -0.001 (0.009; p=0.879) | -0.002 (0.003; p=0.378) | 0.030* (0.016; p=0.061) | 0.020* (0.011; p=0.071) |
| Black | -0.015* (0.008; p=0.057) | -0.026*** (0.004; p=<0.001) | 0.011 (0.009; p=0.213) | 0.015* (0.008; p=0.068) | -0.020*** (0.006; p=<0.001) | -0.004* (0.002; p=0.094) | -0.009 (0.010; p=0.358) | -0.007 (0.008; p=0.344) |
| Black x age 35-55 | -0.049** (0.020; p=0.014) | -0.035*** (0.011; p=0.001) | -0.007 (0.020; p=0.733) | -0.007 (0.011; p=0.551) | -0.003 (0.008; p=0.693) | 0.005 (0.003; p=0.131) | 0.040** (0.019; p=0.036) | 0.030** (0.012; p=0.012) |
| ln parental income x Black | 0.023** (0.010; p=0.025) | -0.006 (0.005; p=0.260) | 0.032*** (0.011; p=0.005) | 0.007 (0.012; p=0.578) | -0.003 (0.008; p=0.762) | 0.005* (0.003; p=0.087) | 0.039*** (0.014; p=0.005) | 0.029** (0.012; p=0.012) |
| ln parental income x Black x age 35-55 | -0.117*** (0.030; p=<0.001) | -0.005 (0.014; p=0.719) | -0.120*** (0.030; p=<0.001) | -0.012 (0.016; p=0.460) | -0.011 (0.011; p=0.318) | -0.005 (0.004; p=0.196) | -0.002 (0.026; p=0.948) | -0.015 (0.017; p=0.394) |
| Controls | age quartic, year FE, age 35-55 dummy, education, ln wage and score at 28-32 | age quartic, year FE, age 35-55 dummy, education, ln wage and score at 28-32 | age quartic, year FE, age 35-55 dummy, education, ln wage and score at 28-32 | age quartic, year FE, age 35-55 dummy, education, ln wage and score at 28-32 | age quartic, year FE, age 35-55 dummy, education, ln wage and score at 28-32 | age quartic, year FE, age 35-55 dummy, education, ln wage and score at 28-32 | age quartic, year FE, age 35-55 dummy, education, ln wage and score at 28-32 | age quartic, year FE, age 35-55 dummy, education, ln wage and score at 28-32 |
| N son-years / clusters | 38,565 / 1,575 | 36,904 / 1,575 | 36,904 / 1,575 | 33,203 / 1,557 | 27,010 / 1,537 | 33,203 / 1,557 | 17,231 / 1,287 | 14,744 / 1,205 |

## 7. Returns to tenure with the employer

Son-years with tenure with the present employer (waves 1984-2023), within-son (person fixed effects) regressions of the outcome (column header) on tenure / 10, its square and tenure x ln parental income (centred), quartic in age, year FE. Within-son tenure slopes mix the return to seniority with the selection of good matches (Altonji-Shakotko), so read them as descriptive wage-tenure profiles. The score column is occupational upgrading while staying with the employer.

| | (1) ln wage | (2) occupation score | (3) within-occupation residual |
|---|---|---|---|
| **Pooled (weighted)** | | | |
| tenure (per 10 years) | 0.242*** (0.019; p=<0.001) | 0.037*** (0.009; p=<0.001) | 0.206*** (0.021; p=<0.001) |
| tenure squared | -0.076*** (0.007; p=<0.001) | -0.007** (0.003; p=0.034) | -0.068*** (0.008; p=<0.001) |
| tenure x ln parental income | 0.032** (0.014; p=0.020) | -0.015** (0.008; p=0.047) | 0.047*** (0.016; p=0.003) |
| Person FE, age quartic, year FE; N son-years / sons / clusters | 30,561 / 4,204 / 1,657 | 30,561 / 4,204 / 1,657 | 30,561 / 4,204 / 1,657 |
| **Black** | | | |
| tenure (per 10 years) | 0.268*** (0.030; p=<0.001) | 0.056*** (0.015; p=<0.001) | 0.212*** (0.032; p=<0.001) |
| tenure squared | -0.065*** (0.010; p=<0.001) | -0.012** (0.005; p=0.028) | -0.053*** (0.011; p=<0.001) |
| tenure x ln parental income | 0.003 (0.019; p=0.859) | -0.010 (0.009; p=0.274) | 0.013 (0.019; p=0.489) |
| Person FE, age quartic, year FE; N son-years / sons / clusters | 10,217 / 1,647 / 598 | 10,217 / 1,647 / 598 | 10,217 / 1,647 / 598 |
| **White** | | | |
| tenure (per 10 years) | 0.233*** (0.019; p=<0.001) | 0.037*** (0.010; p=<0.001) | 0.196*** (0.021; p=<0.001) |
| tenure squared | -0.075*** (0.007; p=<0.001) | -0.006 (0.004; p=0.104) | -0.069*** (0.008; p=<0.001) |
| tenure x ln parental income | 0.046*** (0.016; p=0.005) | -0.023*** (0.009; p=0.008) | 0.068*** (0.019; p=<0.001) |
| Person FE, age quartic, year FE; N son-years / sons / clusters | 20,357 / 2,560 / 1,067 | 20,357 / 2,560 / 1,067 | 20,357 / 2,560 / 1,067 |
| Black - White: ten | 0.035 (0.035; p=0.318) | 0.019 (0.018; p=0.277) | 0.016 (0.038; p=0.681) |
| Black - White: ten_lyp | -0.042* (0.025; p=0.089) | 0.013 (0.012; p=0.294) | -0.055** (0.027; p=0.038) |

## 8. Job loss and occupational progression

Son-years t (male heads 25-52, 1970-2019) with a valid wage and occupation in an income year t-2..t-1 (latest) and t+2..t+3 (earliest). Displaced in t = main displacement (plant closure / layoff / firing; 19.FatherDisplacement.py) dated t; non-displaced son-years with a displacement in t-3..t+3 are dropped. Outcome = post minus pre (column header). Controls: ln parental income, quartic in age, year FE; clusters 1968 family. The occupation at the interview of t (spring) is the 'pre' occupation for a son-year t-1, so a displacement early in t can contaminate it (bias towards zero).

| | (1) change in ln wage | (2) change in occupation score | (3) change in residual | (4) moved up >= 0.10 | (5) moved down >= 0.10 |
|---|---|---|---|---|---|
| **Pooled (weighted)** | | | | | |
| displaced in t | -0.131*** (0.020; p=<0.001) | -0.028*** (0.010; p=0.005) | -0.103*** (0.022; p=<0.001) | 0.050*** (0.014; p=<0.001) | 0.140*** (0.016; p=<0.001) |
| Mean of outcome | 0.094 | 0.016 | 0.078 | 0.209 | 0.174 |
| N son-years (displaced) / clusters | 23,318 (1,681) / 1,531 | 23,318 (1,681) / 1,531 | 23,318 (1,681) / 1,531 | 23,318 (1,681) / 1,531 | 23,318 (1,681) / 1,531 |
| **Pooled (weighted), with displacement x parental income** | | | | | |
| displaced in t | -0.128*** (0.020; p=<0.001) | -0.024** (0.010; p=0.017) | -0.105*** (0.023; p=<0.001) | 0.052*** (0.014; p=<0.001) | 0.134*** (0.015; p=<0.001) |
| displaced x ln parental income | -0.026 (0.032; p=0.415) | -0.042** (0.018; p=0.022) | 0.016 (0.036; p=0.666) | -0.019 (0.025; p=0.451) | 0.050* (0.028; p=0.070) |
| **Black** | | | | | |
| displaced in t | -0.110*** (0.027; p=<0.001) | -0.008 (0.011; p=0.480) | -0.103*** (0.029; p=<0.001) | 0.088*** (0.019; p=<0.001) | 0.103*** (0.019; p=<0.001) |
| Mean of outcome | 0.072 | 0.012 | 0.060 | 0.216 | 0.182 |
| N son-years (displaced) / clusters | 6,791 (728) / 540 | 6,791 (728) / 540 | 6,791 (728) / 540 | 6,791 (728) / 540 | 6,791 (728) / 540 |
| **Black, with displacement x parental income** | | | | | |
| displaced in t | -0.107*** (0.032; p=<0.001) | 0.004 (0.013; p=0.790) | -0.111*** (0.035; p=0.001) | 0.078*** (0.023; p=<0.001) | 0.083*** (0.024; p=<0.001) |
| displaced x ln parental income | 0.007 (0.044; p=0.879) | 0.024 (0.016; p=0.123) | -0.017 (0.047; p=0.710) | -0.021 (0.030; p=0.483) | -0.041 (0.028; p=0.141) |
| **White** | | | | | |
| displaced in t | -0.148*** (0.021; p=<0.001) | -0.035*** (0.010; p=<0.001) | -0.112*** (0.023; p=<0.001) | 0.039*** (0.014; p=0.006) | 0.147*** (0.017; p=<0.001) |
| Mean of outcome | 0.098 | 0.019 | 0.079 | 0.213 | 0.171 |
| N son-years (displaced) / clusters | 16,532 (953) / 996 | 16,532 (953) / 996 | 16,532 (953) / 996 | 16,532 (953) / 996 | 16,532 (953) / 996 |
| **White, with displacement x parental income** | | | | | |
| displaced in t | -0.141*** (0.022; p=<0.001) | -0.030*** (0.010; p=0.003) | -0.111*** (0.024; p=<0.001) | 0.037** (0.015; p=0.011) | 0.140*** (0.017; p=<0.001) |
| displaced x ln parental income | -0.033 (0.037; p=0.374) | -0.027 (0.019; p=0.158) | -0.006 (0.041; p=0.884) | 0.008 (0.027; p=0.762) | 0.039 (0.032; p=0.213) |
| **Black - White** | | | | | |
| displaced in t | 0.037 (0.034; p=0.279) | 0.028* (0.015; p=0.071) | 0.010 (0.037; p=0.794) | 0.049** (0.024; p=0.036) | -0.045* (0.025; p=0.079) |

## 9. NLSY79 check

### 9a. Wage persistence by age: between vs within occupation

Men of the NLSY79 (White and Black cross-sectional + supplemental samples) living with a parent in 1979; regressor = ln mean parental family income 1979-81 (2.NLSY79.py); outcome = hourly wage of the CPS (main) job at each interview and its occupation score (occ1990dd, the same CPS MORG score); controls: quartic in age, birth-year FE; clusters = 1979 household; pooled weighted by the 1979 sampling weight.

| | (1) ln wage | (2) occupation score | (3) within-occupation residual | (4) share between = (2)/(1) |
|---|---|---|---|---|
| **Pooled (weighted)** | | | | |
| ln parental income, ages 25-34 | 0.252*** (0.014; p=<0.001) | 0.133*** (0.008; p=<0.001) | 0.119*** (0.012; p=<0.001) | 0.528*** (0.030; p=<0.001) |
| ln parental income, ages 35-44 | 0.345*** (0.020; p=<0.001) | 0.128*** (0.009; p=<0.001) | 0.217*** (0.016; p=<0.001) | 0.370*** (0.022; p=<0.001) |
| ln parental income, ages 45-55 | 0.381*** (0.026; p=<0.001) | 0.105*** (0.011; p=<0.001) | 0.276*** (0.023; p=<0.001) | 0.275*** (0.026; p=<0.001) |
| N person-rounds / clusters | 25-34: 21,790/2,306 ; 35-44: 11,063/2,117 ; 45-55: 9,696/1,884 |  |  |  |
| **Black** | | | | |
| ln parental income, ages 25-34 | 0.161*** (0.017; p=<0.001) | 0.076*** (0.011; p=<0.001) | 0.085*** (0.013; p=<0.001) | 0.473*** (0.054; p=<0.001) |
| ln parental income, ages 35-44 | 0.192*** (0.023; p=<0.001) | 0.069*** (0.013; p=<0.001) | 0.123*** (0.019; p=<0.001) | 0.359*** (0.054; p=<0.001) |
| ln parental income, ages 45-55 | 0.215*** (0.029; p=<0.001) | 0.061*** (0.014; p=<0.001) | 0.153*** (0.024; p=<0.001) | 0.286*** (0.055; p=<0.001) |
| N person-rounds / clusters | 25-34: 7,498/812 ; 35-44: 3,774/742 ; 45-55: 3,280/655 |  |  |  |
| **White** | | | | |
| ln parental income, ages 25-34 | 0.241*** (0.019; p=<0.001) | 0.120*** (0.010; p=<0.001) | 0.121*** (0.015; p=<0.001) | 0.499*** (0.037; p=<0.001) |
| ln parental income, ages 35-44 | 0.329*** (0.025; p=<0.001) | 0.107*** (0.011; p=<0.001) | 0.222*** (0.020; p=<0.001) | 0.326*** (0.027; p=<0.001) |
| ln parental income, ages 45-55 | 0.354*** (0.032; p=<0.001) | 0.086*** (0.013; p=<0.001) | 0.268*** (0.028; p=<0.001) | 0.244*** (0.033; p=<0.001) |
| N person-rounds / clusters | 25-34: 14,292/1,494 ; 35-44: 7,289/1,375 ; 45-55: 6,416/1,229 |  |  |  |
| **Black - White** | | | | |
| ln parental income, ages 25-34 | -0.080*** (0.026; p=0.002) | -0.044*** (0.015; p=0.004) | -0.036* (0.020; p=0.075) | 0.551*** (0.162; p=<0.001) |
| ln parental income, ages 35-44 | -0.137*** (0.034; p=<0.001) | -0.038** (0.017; p=0.027) | -0.099*** (0.027; p=<0.001) | 0.279*** (0.100; p=0.005) |
| ln parental income, ages 45-55 | -0.140*** (0.043; p=0.001) | -0.025 (0.020; p=0.205) | -0.115*** (0.037; p=0.002) | 0.178 (0.122; p=0.143) |
| Change of the gap (45-55) - (25-34) | -0.059* (0.036; p=0.099) | 0.019 (0.019; p=0.319) | -0.079** (0.037; p=0.034) |  |

### 9b. Promotions and within-employer occupational upgrading

Person-round linear probability models, controls: quartic in age, round FE; clusters = 1979 household. (1) any promotion since the last interview at jobs #01-05: 'ES-16' rounds 1988-1990 (ages 23-33) and 'QES-PROMO39' = promotion, rounds 1996-2016 (ages 31-59); (2) any position change ('QES-PROMO38', 1996-2016); (3)-(5) CPS job of consecutive interviews (1-2 years apart): same roster employer JJ and a different occ1990dd occupation with a higher score / any employer / same employer.

| | (1) promotion since last interview | (2) position change since last interview | (3) higher-paying occupation, same employer | (4) higher-paying occupation | (5) same employer as last interview |
|---|---|---|---|---|---|
| **Pooled (weighted)** | | | | | |
| ln parental income, ages 25-34 | 0.022** (0.009; p=0.016) | 0.056*** (0.021; p=0.007) | 0.012** (0.005; p=0.012) | -0.017*** (0.005; p=0.001) | 0.068*** (0.009; p=<0.001) |
| Mean, 25-34 | 0.254 | 0.286 | 0.178 | 0.298 | 0.693 |
| N person-rounds / clusters, 25-34 | 6,495 / 2,202 | 1,464 / 1,058 | 19,551 / 2,258 | 19,551 / 2,258 | 19,739 / 2,260 |
| ln parental income, ages 35-55 | 0.021*** (0.006; p=<0.001) | 0.024*** (0.006; p=<0.001) | 0.010*** (0.004; p=0.006) | -0.008* (0.004; p=0.081) | 0.036*** (0.008; p=<0.001) |
| Mean, 35-55 | 0.130 | 0.177 | 0.086 | 0.171 | 0.762 |
| N person-rounds / clusters, 35-55 | 18,366 / 2,129 | 18,366 / 2,129 | 20,548 / 2,138 | 20,548 / 2,138 | 21,169 / 2,147 |
| **Black** | | | | | |
| ln parental income, ages 25-34 | 0.033** (0.014; p=0.014) | 0.080*** (0.031; p=0.009) | 0.007 (0.007; p=0.321) | -0.012* (0.007; p=0.076) | 0.046*** (0.013; p=<0.001) |
| Mean, 25-34 | 0.237 | 0.255 | 0.152 | 0.311 | 0.606 |
| N person-rounds / clusters, 25-34 | 2,277 / 763 | 498 / 361 | 6,631 / 789 | 6,631 / 789 | 6,721 / 790 |
| ln parental income, ages 35-55 | 0.014* (0.007; p=0.060) | 0.017* (0.009; p=0.066) | 0.005 (0.005; p=0.319) | 0.004 (0.007; p=0.513) | 0.008 (0.013; p=0.517) |
| Mean, 35-55 | 0.118 | 0.160 | 0.069 | 0.184 | 0.694 |
| N person-rounds / clusters, 35-55 | 6,462 / 755 | 6,462 / 755 | 6,893 / 749 | 6,893 / 749 | 7,128 / 753 |
| **White** | | | | | |
| ln parental income, ages 25-34 | 0.027** (0.011; p=0.017) | 0.061** (0.025; p=0.013) | 0.012** (0.006; p=0.048) | -0.013** (0.006; p=0.041) | 0.061*** (0.011; p=<0.001) |
| Mean, 25-34 | 0.257 | 0.283 | 0.181 | 0.296 | 0.702 |
| N person-rounds / clusters, 25-34 | 4,218 / 1,439 | 966 / 697 | 12,920 / 1,469 | 12,920 / 1,469 | 13,018 / 1,470 |
| ln parental income, ages 35-55 | 0.025*** (0.007; p=<0.001) | 0.028*** (0.008; p=<0.001) | 0.009** (0.004; p=0.034) | -0.005 (0.005; p=0.373) | 0.030*** (0.010; p=0.002) |
| Mean, 35-55 | 0.130 | 0.177 | 0.087 | 0.168 | 0.769 |
| N person-rounds / clusters, 35-55 | 11,904 / 1,374 | 11,904 / 1,374 | 13,655 / 1,389 | 13,655 / 1,389 | 14,041 / 1,394 |
| **Black - White** | | | | | |
| ln parental income, ages 25-34 | 0.006 (0.018; p=0.722) | 0.018 (0.040; p=0.641) | -0.005 (0.009; p=0.566) | 0.001 (0.009; p=0.870) | -0.016 (0.017; p=0.355) |
| ln parental income, ages 35-55 | -0.012 (0.010; p=0.222) | -0.011 (0.012; p=0.342) | -0.004 (0.006; p=0.499) | 0.009 (0.009; p=0.284) | -0.022 (0.016; p=0.178) |

### 9c. NLSY79: Black x parental income x after-35 interactions

As Section 6 (unweighted, controls: quartic in age, round FE, age 35-55 dummy). Promotions are observed at 23-33 (1988-90) and 31-59 (1996-2016), so the age split for (1) also separates survey eras.

| | promotion | higher-paying occupation, same employer | ln wage | occupation score |
|---|---|---|---|---|
| **Black + White men** | | | | |
| ln parental income (centred) | 0.026** (0.011; p=0.019) | 0.012** (0.006; p=0.037) | 0.240*** (0.019; p=<0.001) | 0.122*** (0.010; p=<0.001) |
| x age 35-55 | -0.001 (0.012; p=0.943) | -0.003 (0.006; p=0.578) | 0.102*** (0.020; p=<0.001) | -0.021** (0.009; p=0.030) |
| Black | 0.004 (0.014; p=0.761) | -0.024*** (0.007; p=<0.001) | -0.135*** (0.020; p=<0.001) | -0.115*** (0.012; p=<0.001) |
| Black x age 35-55 | -0.006 (0.015; p=0.705) | 0.011 (0.008; p=0.168) | -0.074*** (0.019; p=<0.001) | -0.003 (0.010; p=0.747) |
| ln parental income x Black | 0.007 (0.017; p=0.680) | -0.006 (0.009; p=0.496) | -0.080*** (0.025; p=0.002) | -0.047*** (0.015; p=0.002) |
| ln parental income x Black x age 35-55 | -0.019 (0.019; p=0.300) | 0.001 (0.009; p=0.904) | -0.054** (0.026; p=0.038) | 0.013 (0.014; p=0.332) |
| N person-rounds / clusters | 24,861 / 2,309 | 40,099 / 2,321 | 43,150 / 2,350 | 44,727 / 2,358 |
