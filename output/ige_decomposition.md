# Black-White IGE gap: human capital (wage) transmission vs labor-market shocks

Built by `24.IGEDecomposition.py` (2026-10-17); definitions in its docstring. PSID SRC + SEO, unweighted, race of the parental household head at child age 16. Father = male head of the child's family unit at 16. ln earnings = ln hourly wage + ln annual hours in every valid year (earnings $100-$150,000 in 1967 $, hours >= 100, wage $2-$200 in 2000 $). Analytic s.e. clustered by 1968 family; bootstrap s.e. = 200 draws of 1968 families within race. *** p<0.01, ** p<0.05, * p<0.1. **Everything below is accounting: it says where the covariance and the gap sit, not what causes them.**

## Summary

- **Benchmark.** 6.IGEMain family-income IGE of sons: Black 0.268, White 0.473; on the father-present sons used here 0.363 / 0.541. Father-earnings IGE (Lee-Solon, age 40): Black 0.220, White 0.389; lifetime-mean design 0.251 / 0.296.
- **Price vs quantity (Section 1).** Wage IGE (son's ln wage on father's ln wage): Black 0.195, White 0.402; hours elasticity: Black 0.077, White 0.061. Of the earnings IGE on the father's earnings, the son's wage carries Black 0.210 of 0.220 and White 0.378 of 0.389; the son's hours carry almost nothing in either group.
- **Father's earnings variance (Section 1c, lifetime design).** Share due to Var(ln wage): Black 0.74, White 0.82; due to Var(ln hours): Black 0.25, White 0.20. Var(y_f): Black 0.270, White 0.332 - Black fathers' earnings are not more dispersed; their wage variance is smaller and their hours variance about the same.
- **Age profile (Section 1b).** Family-income IGE, sons 25-34: Black 0.273, White 0.327; 35-44: 0.288 / 0.474; 45-55: 0.250 / 0.474. Father-earnings IGE 25-34: 0.259 / 0.258; 45-55: 0.212 / 0.403. The son's ln wage on parental income: Black 0.161 -> 0.161, White 0.255 -> 0.454 (25-34 -> 45-55); the son's ln hours on parental income, 25-55: Black 0.072, White 0.027. **The gap is absent at 25-34 and opens after 35, entirely in the wage component; the hours component works the other way.**
- **Purging shocks (Section 2, Lee-Solon childhood).** Gap, same children: all years -0.157, clean years A -0.159, clean years B -0.175; potential earnings (wage IGE) -0.207 vs earnings -0.169. Change in the gap (positive = smaller): clean A -0.002 (0.042; p=0.969), clean B -0.018 (0.044; p=0.689), potential -0.038 (0.044; p=0.397); family income, clean years vs all years 0.016 (0.051; p=0.749).
- **Instability (Section 3).** Share of years displaced or unemployed: fathers (childhood window) Black 0.186 vs White 0.141; sons Black 0.369 vs White 0.190. Transitory variance: fathers 0.140 vs 0.121, sons 0.360 vs 0.253. The race gap in instability is in the sons' generation, not among the (father-present) fathers.
- **Education (Section 4a).** Son's education mediates 34% (Black) and 25% (White) of the earnings IGE on parental family income; the wage IGE on parental income is Black 0.164, White 0.413, the hours IGE Black 0.050, White 0.034.
- **Reliability (Section 5).** Childhood-mean reliability of the father's ln earnings: Black 0.623, White 0.622; of family income Black 0.697, White 0.666. Differential attenuation is small.
- **Composition (Section 6).** Re-weighting White sons to the Black parental distribution closes 0.593 (0.653; p=0.364) of the family-income IGE gap and 0.384 (1.831; p=0.834) of the father-earnings IGE gap (ratios of noisy gaps, hence the s.e.; the composition term of Section 7, -0.035 (0.030; p=0.248) over 25-55 and -0.087* (0.049; p=0.072) at 35-55, is the better-measured version): the IGE is flatter in the lower part of the parental distribution, where Black families are concentrated.
- **Decomposition (Section 7, sons, Lee-Solon controls, childhood window, ages 25-55).** Gap -0.060 (0.049; p=0.217) = composition -0.035 (0.030; p=0.248) + wage transmission -0.085** (0.038; p=0.024) + hours / instability -0.003 (0.026; p=0.897) (of which the hours share of the father's earnings variance, the 'inflated denominator', -0.025** (0.010; p=0.015)) + cross terms 0.064 (0.042; p=0.129). Sons 35-55: gap -0.141** (0.068; p=0.039) = -0.087* (0.049; p=0.072) + -0.115** (0.054; p=0.032) + 0.016 (0.038; p=0.669) + 0.046 (0.055; p=0.409). Lifetime design: gap -0.044 (0.050; p=0.372) = -0.021 (0.027; p=0.428) + -0.054 (0.037; p=0.148) + -0.016 (0.026; p=0.544) + 0.046 (0.038; p=0.225).

**Assessment.** The Black-White IGE gap is a gap in the transmission of the price of labor - the hourly wage - and it builds up over the sons' careers. At 25-34 the IGEs are about equal; after 35 the White sons' wage keeps tracking their parents' income and the Black sons' wage does not. That is the pattern of differences in human capital accumulation, in returns to it, or in access to the jobs that pay for it - not of transitory shocks in measured income. Labor-market shocks are real and racially unequal, but they sit in the sons' generation and do not produce the gap in this accounting: (i) among father-present families, Black fathers' earnings are not noisier, their reliability ratio equals the White one, and the hours share of their earnings variance - the PI's 'inflated denominator' (wage-share + hours-share terms) - accounts for -0.022 of the -0.060 gap over ages 25-55 and -0.017 of the -0.141 gap at 35-55, against -0.085 / -0.115 for wage transmission: present, but second order; (ii) Black sons' displacement, unemployment and zero-hours years are about twice the White rates and are more tied to parental income, so the hours channel RAISES the Black IGE (the son's hours IGE on parental income is larger for Black sons) and partly hides the wage gap at young ages; (iii) dropping shock years or using potential earnings leaves the gap where it is. Composition - Black families sit where the IGE is flatter - accounts for a sizeable but imprecise share (about 0.04-0.09 log points, a third to three fifths of the decomposed gap). Son's education mediates a third of the Black IGE and a quarter of the White IGE but does not close the gap. Caveats: father-present Black sons are under half of the benchmark sample (Section 0) and have a higher family-income IGE than all Black sons; wage = earnings / hours carries division bias; hours mix shocks, labor supply and search frictions; all splits are accounting identities, not causal effects.

## 0. Benchmark and samples

6.IGEMain.py benchmark re-run (sons, ln family income, all years, s.e. by child): Black 0.268*** (0.044; p=<0.001), White 0.473*** (0.034; p=<0.001). Same regression on sons whose father's childhood-window earnings are observed: Black 0.363*** (0.076; p=<0.001) (887 sons), White 0.541*** (0.042; p=<0.001) (2,248 sons).

Sons in the 6.IGEMain parental sample: Black 4,109 (male head at 16: 2,148; father's childhood ln earnings observed, >= 3 valid years: 1,801), White 4,552 (3,962; 3,638). **The price / quantity analysis is necessarily on father-present children; for Black sons that is under half of the benchmark sample.**

## 1. Price vs quantity: earnings IGE, wage IGE, hours elasticity

One regression per column (child's outcome in the header); the regressor row says which father measure. Father measures are means over valid years (childhood window = income years when the child is 12-18; working life = his valid years at 25-55). Columns (4)+(5) = (1) exactly (same sample, same controls).

| | (1) ln earnings | (2) ln wage | (3) ln hours | (4) ln wage | (5) ln hours | (6) ln earnings | (7) ln earnings |
|---|---|---|---|---|---|---|---|
| **Sons, Lee-Solon (age 40), father's childhood window: Black** | | | | | | | |
| Father's ln earnings | 0.220*** (0.064; p=<0.001) |  |  | 0.210*** (0.049; p=<0.001) | 0.010 (0.027; p=0.718) |  |  |
| Father's ln wage |  | 0.195*** (0.057; p=<0.001) |  |  |  | 0.187** (0.074; p=0.012) |  |
| Father's ln hours |  |  | 0.077 (0.057; p=0.179) |  |  |  | 0.384*** (0.141; p=0.006) |
| N (child-years or children) / children / clusters | 7,341 / 868 / 400 | 7,341 / 868 / 400 | 7,341 / 868 / 400 | 7,341 / 868 / 400 | 7,341 / 868 / 400 | 7,341 / 868 / 400 | 7,341 / 868 / 400 |
| Controls | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic |
| **Sons, Lee-Solon (age 40), father's childhood window: White** | | | | | | | |
| Father's ln earnings | 0.389*** (0.035; p=<0.001) |  |  | 0.378*** (0.032; p=<0.001) | 0.012 (0.013; p=0.360) |  |  |
| Father's ln wage |  | 0.402*** (0.038; p=<0.001) |  |  |  | 0.402*** (0.041; p=<0.001) |  |
| Father's ln hours |  |  | 0.061* (0.032; p=0.055) |  |  |  | 0.184** (0.087; p=0.035) |
| N (child-years or children) / children / clusters | 23,396 / 2,217 / 977 | 23,396 / 2,217 / 977 | 23,396 / 2,217 / 977 | 23,396 / 2,217 / 977 | 23,396 / 2,217 / 977 | 23,396 / 2,217 / 977 | 23,396 / 2,217 / 977 |
| Controls | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic |
| **Sons, Lee-Solon (age 40), father's working life 25-55: Black** | | | | | | | |
| Father's ln earnings | 0.325*** (0.075; p=<0.001) |  |  | 0.287*** (0.061; p=<0.001) | 0.038 (0.032; p=0.242) |  |  |
| Father's ln wage |  | 0.314*** (0.068; p=<0.001) |  |  |  | 0.329*** (0.086; p=<0.001) |  |
| Father's ln hours |  |  | 0.151** (0.076; p=0.047) |  |  |  | 0.538*** (0.157; p=<0.001) |
| N (child-years or children) / children / clusters | 7,045 / 881 / 389 | 7,045 / 881 / 389 | 7,045 / 881 / 389 | 7,045 / 881 / 389 | 7,045 / 881 / 389 | 7,045 / 881 / 389 | 7,045 / 881 / 389 |
| Controls | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic |
| **Sons, Lee-Solon (age 40), father's working life 25-55: White** | | | | | | | |
| Father's ln earnings | 0.454*** (0.043; p=<0.001) |  |  | 0.431*** (0.039; p=<0.001) | 0.022 (0.015; p=0.139) |  |  |
| Father's ln wage |  | 0.449*** (0.046; p=<0.001) |  |  |  | 0.456*** (0.049; p=<0.001) |  |
| Father's ln hours |  |  | 0.093** (0.041; p=0.023) |  |  |  | 0.322*** (0.111; p=0.004) |
| N (child-years or children) / children / clusters | 22,697 / 2,228 / 967 | 22,697 / 2,228 / 967 | 22,697 / 2,228 / 967 | 22,697 / 2,228 / 967 | 22,697 / 2,228 / 967 | 22,697 / 2,228 / 967 | 22,697 / 2,228 / 967 |
| Controls | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic |
| **Sons, lifetime mean, father's childhood window: Black** | | | | | | | |
| Father's ln earnings | 0.251*** (0.045; p=<0.001) |  |  | 0.225*** (0.033; p=<0.001) | 0.027 (0.025; p=0.279) |  |  |
| Father's ln wage |  | 0.229*** (0.042; p=<0.001) |  |  |  | 0.221*** (0.059; p=<0.001) |  |
| Father's ln hours |  |  | 0.130*** (0.049; p=0.008) |  |  |  | 0.350*** (0.096; p=<0.001) |
| N (child-years or children) / children / clusters | 712 / 712 / 347 | 712 / 712 / 347 | 712 / 712 / 347 | 712 / 712 / 347 | 712 / 712 / 347 | 712 / 712 / 347 | 712 / 712 / 347 |
| Controls | one row per child; birth-year FE, quadratics in mean age and A | one row per child; birth-year FE, quadratics in mean age and A | one row per child; birth-year FE, quadratics in mean age and A | one row per child; birth-year FE, quadratics in mean age and A | one row per child; birth-year FE, quadratics in mean age and A | one row per child; birth-year FE, quadratics in mean age and A | one row per child; birth-year FE, quadratics in mean age and A |
| **Sons, lifetime mean, father's childhood window: White** | | | | | | | |
| Father's ln earnings | 0.296*** (0.024; p=<0.001) |  |  | 0.287*** (0.021; p=<0.001) | 0.009 (0.011; p=0.430) |  |  |
| Father's ln wage |  | 0.318*** (0.025; p=<0.001) |  |  |  | 0.301*** (0.029; p=<0.001) |  |
| Father's ln hours |  |  | 0.114*** (0.027; p=<0.001) |  |  |  | 0.235*** (0.057; p=<0.001) |
| N (child-years or children) / children / clusters | 1,975 / 1,975 / 930 | 1,975 / 1,975 / 930 | 1,975 / 1,975 / 930 | 1,975 / 1,975 / 930 | 1,975 / 1,975 / 930 | 1,975 / 1,975 / 930 | 1,975 / 1,975 / 930 |
| Controls | one row per child; birth-year FE, quadratics in mean age and A | one row per child; birth-year FE, quadratics in mean age and A | one row per child; birth-year FE, quadratics in mean age and A | one row per child; birth-year FE, quadratics in mean age and A | one row per child; birth-year FE, quadratics in mean age and A | one row per child; birth-year FE, quadratics in mean age and A | one row per child; birth-year FE, quadratics in mean age and A |
| **Daughters, Lee-Solon (age 40), father's childhood window: Black** | | | | | | | |
| Father's ln earnings | 0.276*** (0.053; p=<0.001) |  |  | 0.251*** (0.041; p=<0.001) | 0.025 (0.024; p=0.291) |  |  |
| Father's ln wage |  | 0.315*** (0.053; p=<0.001) |  |  |  | 0.349*** (0.071; p=<0.001) |  |
| Father's ln hours |  |  | 0.001 (0.044; p=0.976) |  |  |  | 0.109 (0.094; p=0.243) |
| N (child-years or children) / children / clusters | 9,152 / 957 / 411 | 9,152 / 957 / 411 | 9,152 / 957 / 411 | 9,152 / 957 / 411 | 9,152 / 957 / 411 | 9,152 / 957 / 411 | 9,152 / 957 / 411 |
| Controls | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic |
| **Daughters, Lee-Solon (age 40), father's childhood window: White** | | | | | | | |
| Father's ln earnings | 0.255*** (0.047; p=<0.001) |  |  | 0.329*** (0.033; p=<0.001) | -0.074*** (0.024; p=0.002) |  |  |
| Father's ln wage |  | 0.295*** (0.036; p=<0.001) |  |  |  | 0.209*** (0.051; p=<0.001) |  |
| Father's ln hours |  |  | 0.029 (0.055; p=0.601) |  |  |  | 0.378*** (0.107; p=<0.001) |
| N (child-years or children) / children / clusters | 21,343 / 2,213 / 976 | 21,343 / 2,213 / 976 | 21,343 / 2,213 / 976 | 21,343 / 2,213 / 976 | 21,343 / 2,213 / 976 | 21,343 / 2,213 / 976 | 21,343 / 2,213 / 976 |
| Controls | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic |
| **Sons 35-55, Lee-Solon (age 40), father's childhood window: Black** | | | | | | | |
| Father's ln earnings | 0.183*** (0.070; p=0.009) |  |  | 0.192*** (0.056; p=<0.001) | -0.009 (0.029; p=0.754) |  |  |
| Father's ln wage |  | 0.178*** (0.063; p=0.004) |  |  |  | 0.152* (0.080; p=0.057) |  |
| Father's ln hours |  |  | 0.050 (0.060; p=0.405) |  |  |  | 0.328** (0.155; p=0.035) |
| N (child-years or children) / children / clusters | 3,346 / 573 / 302 | 3,346 / 573 / 302 | 3,346 / 573 / 302 | 3,346 / 573 / 302 | 3,346 / 573 / 302 | 3,346 / 573 / 302 | 3,346 / 573 / 302 |
| Controls | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic |
| **Sons 35-55, Lee-Solon (age 40), father's childhood window: White** | | | | | | | |
| Father's ln earnings | 0.394*** (0.036; p=<0.001) |  |  | 0.379*** (0.033; p=<0.001) | 0.015 (0.015; p=0.318) |  |  |
| Father's ln wage |  | 0.404*** (0.040; p=<0.001) |  |  |  | 0.408*** (0.042; p=<0.001) |  |
| Father's ln hours |  |  | 0.062* (0.035; p=0.081) |  |  |  | 0.162* (0.092; p=0.078) |
| N (child-years or children) / children / clusters | 10,997 / 1,597 / 828 | 10,997 / 1,597 / 828 | 10,997 / 1,597 / 828 | 10,997 / 1,597 / 828 | 10,997 / 1,597 / 828 | 10,997 / 1,597 / 828 | 10,997 / 1,597 / 828 |
| Controls | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic | child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic |

## 1b. Age profile: where the gap opens

Sons, Lee-Solon controls (quartics in the father's age at 16 and the son's age) WITHOUT the x-age interactions, estimated within son age bands: the slope over the child-years in the band. One regression per cell (outcome and regressor in the header). Black - White s.e. = root sum of squared s.e. (races are disjoint clusters). Columns (5)+(6) = (2) and (7)+(8) = the ln earnings IGE on parental income in each band.

| | (1) ln family income on ln parental family income | (2) ln earnings on father's ln earnings | (3) ln wage on father's ln wage | (4) ln hours on father's ln hours | (5) ln wage on father's ln earnings | (6) ln hours on father's ln earnings | (7) ln wage on ln parental income | (8) ln hours on ln parental income |
|---|---|---|---|---|---|---|---|---|
| **Sons' ages 25-34** | | | | | | | | |
| Black | 0.273*** (0.033; p=<0.001) | 0.259*** (0.044; p=<0.001) | 0.187*** (0.040; p=<0.001) | 0.153*** (0.051; p=0.003) | 0.198*** (0.032; p=<0.001) | 0.061*** (0.024; p=0.010) | 0.161*** (0.020; p=<0.001) | 0.086*** (0.015; p=<0.001) |
| White | 0.327*** (0.026; p=<0.001) | 0.258*** (0.024; p=<0.001) | 0.274*** (0.022; p=<0.001) | 0.131*** (0.028; p=<0.001) | 0.247*** (0.020; p=<0.001) | 0.011 (0.012; p=0.362) | 0.255*** (0.020; p=<0.001) | 0.027** (0.012; p=0.025) |
| Black - White | -0.054 (0.042; p=0.202) | 0.002 (0.050; p=0.973) | -0.086* (0.046; p=0.060) | 0.022 (0.058; p=0.709) | -0.049 (0.038; p=0.194) | 0.051* (0.027; p=0.056) | -0.094*** (0.028; p=<0.001) | 0.058*** (0.019; p=0.003) |
| Child-years Black / White | 9,226 / 15,304 | 3,995 / 12,399 | 3,995 / 12,399 | 3,995 / 12,399 | 3,995 / 12,399 | 3,995 / 12,399 | 8,331 / 14,761 | 8,331 / 14,761 |
| **Sons' ages 35-44** | | | | | | | | |
| Black | 0.288*** (0.046; p=<0.001) | 0.260*** (0.062; p=<0.001) | 0.207*** (0.054; p=<0.001) | 0.143*** (0.056; p=0.010) | 0.219*** (0.048; p=<0.001) | 0.042 (0.027; p=0.125) | 0.163*** (0.028; p=<0.001) | 0.059*** (0.017; p=<0.001) |
| White | 0.474*** (0.036; p=<0.001) | 0.384*** (0.033; p=<0.001) | 0.393*** (0.036; p=<0.001) | 0.073** (0.031; p=0.019) | 0.369*** (0.030; p=<0.001) | 0.015 (0.012; p=0.197) | 0.403*** (0.031; p=<0.001) | 0.043*** (0.013; p=<0.001) |
| Black - White | -0.186*** (0.058; p=0.001) | -0.123* (0.070; p=0.079) | -0.186*** (0.065; p=0.004) | 0.071 (0.064; p=0.267) | -0.150*** (0.057; p=0.008) | 0.026 (0.030; p=0.373) | -0.240*** (0.042; p=<0.001) | 0.016 (0.022; p=0.463) |
| Child-years Black / White | 5,102 / 9,435 | 2,344 / 7,574 | 2,344 / 7,574 | 2,344 / 7,574 | 2,344 / 7,574 | 2,344 / 7,574 | 4,469 / 8,851 | 4,469 / 8,851 |
| **Sons' ages 45-55** | | | | | | | | |
| Black | 0.250*** (0.075; p=<0.001) | 0.212** (0.089; p=0.017) | 0.162** (0.074; p=0.029) | 0.052 (0.073; p=0.476) | 0.171** (0.068; p=0.012) | 0.042 (0.043; p=0.328) | 0.161*** (0.045; p=<0.001) | 0.045* (0.024; p=0.067) |
| White | 0.474*** (0.060; p=<0.001) | 0.403*** (0.052; p=<0.001) | 0.425*** (0.051; p=<0.001) | 0.069 (0.052; p=0.188) | 0.429*** (0.040; p=<0.001) | -0.026 (0.026; p=0.315) | 0.454*** (0.047; p=<0.001) | -0.014 (0.027; p=0.605) |
| Black - White | -0.224** (0.096; p=0.019) | -0.190* (0.103; p=0.064) | -0.262*** (0.090; p=0.004) | -0.017 (0.090; p=0.849) | -0.258*** (0.079; p=0.001) | 0.068 (0.050; p=0.175) | -0.293*** (0.065; p=<0.001) | 0.059 (0.037; p=0.108) |
| Child-years Black / White | 2,271 / 4,385 | 1,002 / 3,423 | 1,002 / 3,423 | 1,002 / 3,423 | 1,002 / 3,423 | 1,002 / 3,423 | 1,873 / 3,953 | 1,873 / 3,953 |
| **Sons' ages 25-55** | | | | | | | | |
| Black | 0.274*** (0.036; p=<0.001) | 0.255*** (0.046; p=<0.001) | 0.191*** (0.043; p=<0.001) | 0.138*** (0.039; p=<0.001) | 0.202*** (0.035; p=<0.001) | 0.053*** (0.020; p=0.007) | 0.162*** (0.021; p=<0.001) | 0.072*** (0.013; p=<0.001) |
| White | 0.391*** (0.028; p=<0.001) | 0.315*** (0.025; p=<0.001) | 0.332*** (0.026; p=<0.001) | 0.105*** (0.027; p=<0.001) | 0.307*** (0.022; p=<0.001) | 0.007 (0.010; p=0.466) | 0.324*** (0.022; p=<0.001) | 0.027** (0.011; p=0.012) |
| Black - White | -0.117** (0.046; p=0.010) | -0.060 (0.052; p=0.247) | -0.141*** (0.050; p=0.005) | 0.033 (0.048; p=0.490) | -0.106** (0.041; p=0.011) | 0.046** (0.022; p=0.040) | -0.163*** (0.031; p=<0.001) | 0.045*** (0.017; p=0.007) |
| Child-years Black / White | 16,599 / 29,124 | 7,341 / 23,396 | 7,341 / 23,396 | 7,341 / 23,396 | 7,341 / 23,396 | 7,341 / 23,396 | 14,673 / 27,565 | 14,673 / 27,565 |

## 1c. Exact covariance decomposition of the earnings IGE

beta = [Cov(w_s,w_f) + Cov(w_s,h_f) + Cov(h_s,w_f) + Cov(h_s,h_f)] / Var(y_f), father measures partialled out on the design's controls (Frisch-Waugh). Lee-Solon panels: the quartics in the father's age at 16 and the child's age, WITHOUT the y_f x age-quartic interactions (partialling y_f on its own interactions leaves a residual whose variance is a fraction of Var(y_f), and the variance shares then exceed 1), so the IGE here is the slope averaged over child-years at 25-55 rather than the IGE at 40; Section 7 reports the age-40 gap next to it. Wage / hours transmission are the identity-consistent slopes (partialled on the same controls), so they differ slightly from columns (2)-(3) of Section 1. 'White re-weighted' = White children re-weighted to the Black distribution of the father's ln earnings. Bootstrap s.e.

| | Black | White | White re-weighted to Black | Black - White |
|---|---|---|---|---|
| **Sons, Lee-Solon (age 40), father's childhood window** | | | | |
| Cov(w_s, w_f) / Var(y_f) | 0.145*** (0.029; p=<0.001) | 0.281*** (0.022; p=<0.001) | 0.228*** (0.031; p=<0.001) | -0.135*** (0.037; p=<0.001) |
| Cov(w_s, h_f) / Var(y_f) | 0.056*** (0.015; p=<0.001) | 0.027** (0.013; p=0.039) | 0.038 (0.027; p=0.167) | 0.030 (0.020; p=0.139) |
| Cov(h_s, w_f) / Var(y_f) | 0.022 (0.018; p=0.208) | -0.014 (0.010; p=0.141) | -0.023* (0.013; p=0.087) | 0.037* (0.020; p=0.070) |
| Cov(h_s, h_f) / Var(y_f) | 0.031*** (0.007; p=<0.001) | 0.022*** (0.005; p=<0.001) | 0.037** (0.015; p=0.013) | 0.009 (0.009; p=0.315) |
| Sum = earnings IGE | 0.255*** (0.041; p=<0.001) | 0.315*** (0.025; p=<0.001) | 0.280*** (0.037; p=<0.001) | -0.060 (0.048; p=0.211) |
| Share of Var(y_f): Var(w_f) | 0.760*** (0.043; p=<0.001) | 0.844*** (0.046; p=<0.001) | 0.746*** (0.079; p=<0.001) | -0.084 (0.063; p=0.186) |
| Share of Var(y_f): Var(h_f) | 0.223*** (0.024; p=<0.001) | 0.207*** (0.015; p=<0.001) | 0.403*** (0.040; p=<0.001) | 0.016 (0.028; p=0.581) |
| Share of Var(y_f): 2Cov(w_f, h_f) | 0.017 (0.045; p=0.707) | -0.051 (0.043; p=0.237) | -0.149* (0.084; p=0.078) | 0.068 (0.062; p=0.274) |
| Wage transmission Cov(w_s, w_f) / Var(w_f) | 0.191*** (0.040; p=<0.001) | 0.332*** (0.026; p=<0.001) | 0.306*** (0.037; p=<0.001) | -0.141*** (0.048; p=0.003) |
| Hours transmission Cov(h_s, h_f) / Var(h_f) | 0.138*** (0.037; p=<0.001) | 0.105*** (0.025; p=<0.001) | 0.092*** (0.035; p=0.010) | 0.033 (0.044; p=0.453) |
| Var(y_f) (partialled) | 0.302*** (0.025; p=<0.001) | 0.328*** (0.024; p=<0.001) | 0.319*** (0.036; p=<0.001) | -0.026 (0.034; p=0.446) |
| Var(w_f) (partialled) | 0.230*** (0.016; p=<0.001) | 0.277*** (0.013; p=<0.001) | 0.238*** (0.015; p=<0.001) | -0.047** (0.021; p=0.023) |
| Var(h_f) (partialled) | 0.067*** (0.008; p=<0.001) | 0.068*** (0.007; p=<0.001) | 0.129*** (0.020; p=<0.001) | -0.001 (0.011; p=0.946) |
| **Sons, Lee-Solon (age 40), father's working life 25-55** | | | | |
| Cov(w_s, w_f) / Var(y_f) | 0.197*** (0.037; p=<0.001) | 0.320*** (0.027; p=<0.001) | 0.217*** (0.037; p=<0.001) | -0.123*** (0.046; p=0.008) |
| Cov(w_s, h_f) / Var(y_f) | 0.059*** (0.014; p=<0.001) | 0.035** (0.014; p=0.015) | 0.062* (0.032; p=0.054) | 0.024 (0.020; p=0.244) |
| Cov(h_s, w_f) / Var(y_f) | 0.028 (0.017; p=0.102) | -0.013 (0.012; p=0.251) | -0.029* (0.017; p=0.080) | 0.041** (0.021; p=0.046) |
| Cov(h_s, h_f) / Var(y_f) | 0.033*** (0.009; p=<0.001) | 0.028*** (0.006; p=<0.001) | 0.043*** (0.016; p=0.008) | 0.005 (0.011; p=0.633) |
| Sum = earnings IGE | 0.316*** (0.053; p=<0.001) | 0.369*** (0.030; p=<0.001) | 0.293*** (0.048; p=<0.001) | -0.053 (0.061; p=0.383) |
| Share of Var(y_f): Var(w_f) | 0.674*** (0.046; p=<0.001) | 0.841*** (0.049; p=<0.001) | 0.693*** (0.092; p=<0.001) | -0.167** (0.067; p=0.013) |
| Share of Var(y_f): Var(h_f) | 0.197*** (0.025; p=<0.001) | 0.179*** (0.019; p=<0.001) | 0.376*** (0.056; p=<0.001) | 0.019 (0.031; p=0.553) |
| Share of Var(y_f): 2Cov(w_f, h_f) | 0.129*** (0.037; p=<0.001) | -0.019 (0.046; p=0.674) | -0.069 (0.099; p=0.487) | 0.149** (0.059; p=0.012) |
| Wage transmission Cov(w_s, w_f) / Var(w_f) | 0.293*** (0.050; p=<0.001) | 0.381*** (0.031; p=<0.001) | 0.314*** (0.051; p=<0.001) | -0.088 (0.059; p=0.135) |
| Hours transmission Cov(h_s, h_f) / Var(h_f) | 0.166*** (0.051; p=0.001) | 0.155*** (0.034; p=<0.001) | 0.115** (0.049; p=0.018) | 0.012 (0.062; p=0.850) |
| Var(y_f) (partialled) | 0.242*** (0.023; p=<0.001) | 0.268*** (0.020; p=<0.001) | 0.262*** (0.038; p=<0.001) | -0.026 (0.031; p=0.392) |
| Var(w_f) (partialled) | 0.163*** (0.012; p=<0.001) | 0.226*** (0.013; p=<0.001) | 0.181*** (0.015; p=<0.001) | -0.063*** (0.018; p=<0.001) |
| Var(h_f) (partialled) | 0.048*** (0.008; p=<0.001) | 0.048*** (0.007; p=<0.001) | 0.098*** (0.021; p=<0.001) | -0.000 (0.010; p=0.984) |
| **Sons, lifetime mean, father's childhood window** | | | | |
| Cov(w_s, w_f) / Var(y_f) | 0.169*** (0.029; p=<0.001) | 0.262*** (0.021; p=<0.001) | 0.228*** (0.025; p=<0.001) | -0.093*** (0.036; p=0.010) |
| Cov(w_s, h_f) / Var(y_f) | 0.055*** (0.015; p=<0.001) | 0.025** (0.011; p=0.025) | 0.026 (0.022; p=0.249) | 0.031* (0.018; p=0.092) |
| Cov(h_s, w_f) / Var(y_f) | -0.006 (0.022; p=0.791) | -0.014 (0.010; p=0.142) | -0.022* (0.013; p=0.093) | 0.008 (0.024; p=0.724) |
| Cov(h_s, h_f) / Var(y_f) | 0.033*** (0.012; p=0.006) | 0.023*** (0.006; p=<0.001) | 0.044*** (0.014; p=0.002) | 0.010 (0.014; p=0.480) |
| Sum = earnings IGE | 0.251*** (0.045; p=<0.001) | 0.296*** (0.024; p=<0.001) | 0.275*** (0.032; p=<0.001) | -0.044 (0.051; p=0.382) |
| Share of Var(y_f): Var(w_f) | 0.738*** (0.042; p=<0.001) | 0.824*** (0.041; p=<0.001) | 0.758*** (0.065; p=<0.001) | -0.085 (0.058; p=0.144) |
| Share of Var(y_f): Var(h_f) | 0.251*** (0.039; p=<0.001) | 0.203*** (0.016; p=<0.001) | 0.355*** (0.033; p=<0.001) | 0.048 (0.042; p=0.252) |
| Share of Var(y_f): 2Cov(w_f, h_f) | 0.010 (0.051; p=0.836) | -0.027 (0.039; p=0.497) | -0.113* (0.066; p=0.089) | 0.037 (0.064; p=0.563) |
| Wage transmission Cov(w_s, w_f) / Var(w_f) | 0.229*** (0.040; p=<0.001) | 0.318*** (0.025; p=<0.001) | 0.301*** (0.032; p=<0.001) | -0.089* (0.047; p=0.059) |
| Hours transmission Cov(h_s, h_f) / Var(h_f) | 0.130*** (0.048; p=0.007) | 0.114*** (0.030; p=<0.001) | 0.123*** (0.037; p=<0.001) | 0.016 (0.057; p=0.778) |
| Var(y_f) (partialled) | 0.270*** (0.019; p=<0.001) | 0.332*** (0.021; p=<0.001) | 0.294*** (0.028; p=<0.001) | -0.062** (0.028; p=0.028) |
| Var(w_f) (partialled) | 0.199*** (0.011; p=<0.001) | 0.273*** (0.012; p=<0.001) | 0.223*** (0.013; p=<0.001) | -0.074*** (0.017; p=<0.001) |
| Var(h_f) (partialled) | 0.068*** (0.011; p=<0.001) | 0.067*** (0.007; p=<0.001) | 0.104*** (0.013; p=<0.001) | 0.000 (0.013; p=0.972) |
| **Daughters, Lee-Solon (age 40), father's childhood window** | | | | |
| Cov(w_s, w_f) / Var(y_f) | 0.196*** (0.032; p=<0.001) | 0.259*** (0.021; p=<0.001) | 0.183*** (0.034; p=<0.001) | -0.063 (0.038; p=0.102) |
| Cov(w_s, h_f) / Var(y_f) | 0.022 (0.015; p=0.154) | 0.039*** (0.009; p=<0.001) | 0.058** (0.023; p=0.010) | -0.017 (0.018; p=0.345) |
| Cov(h_s, w_f) / Var(y_f) | 0.034** (0.017; p=0.047) | -0.002 (0.014; p=0.916) | 0.001 (0.023; p=0.981) | 0.035 (0.022; p=0.111) |
| Cov(h_s, h_f) / Var(y_f) | 0.018* (0.009; p=0.056) | 0.002 (0.007; p=0.765) | 0.006 (0.018; p=0.761) | 0.016 (0.012; p=0.175) |
| Sum = earnings IGE | 0.270*** (0.048; p=<0.001) | 0.298*** (0.028; p=<0.001) | 0.248*** (0.044; p=<0.001) | -0.029 (0.056; p=0.606) |
| Share of Var(y_f): Var(w_f) | 0.693*** (0.047; p=<0.001) | 0.902*** (0.028; p=<0.001) | 0.930*** (0.055; p=<0.001) | -0.209*** (0.054; p=<0.001) |
| Share of Var(y_f): Var(h_f) | 0.276*** (0.050; p=<0.001) | 0.168*** (0.012; p=<0.001) | 0.368*** (0.044; p=<0.001) | 0.108** (0.052; p=0.037) |
| Share of Var(y_f): 2Cov(w_f, h_f) | 0.031 (0.044; p=0.482) | -0.070** (0.028; p=0.013) | -0.298*** (0.075; p=<0.001) | 0.102* (0.053; p=0.054) |
| Wage transmission Cov(w_s, w_f) / Var(w_f) | 0.283*** (0.044; p=<0.001) | 0.287*** (0.023; p=<0.001) | 0.197*** (0.038; p=<0.001) | -0.004 (0.050; p=0.933) |
| Hours transmission Cov(h_s, h_f) / Var(h_f) | 0.065* (0.036; p=0.067) | 0.012 (0.041; p=0.762) | 0.015 (0.050; p=0.762) | 0.053 (0.054; p=0.330) |
| Var(y_f) (partialled) | 0.310*** (0.027; p=<0.001) | 0.328*** (0.015; p=<0.001) | 0.267*** (0.019; p=<0.001) | -0.018 (0.031; p=0.565) |
| Var(w_f) (partialled) | 0.215*** (0.013; p=<0.001) | 0.296*** (0.014; p=<0.001) | 0.249*** (0.017; p=<0.001) | -0.081*** (0.019; p=<0.001) |
| Var(h_f) (partialled) | 0.085*** (0.020; p=<0.001) | 0.055*** (0.004; p=<0.001) | 0.098*** (0.010; p=<0.001) | 0.030 (0.020; p=0.135) |
| **Sons 35-55, Lee-Solon (age 40), father's childhood window** | | | | |
| Cov(w_s, w_f) / Var(y_f) | 0.150*** (0.041; p=<0.001) | 0.354*** (0.034; p=<0.001) | 0.257*** (0.039; p=<0.001) | -0.204*** (0.053; p=<0.001) |
| Cov(w_s, h_f) / Var(y_f) | 0.055*** (0.021; p=0.008) | 0.032* (0.017; p=0.064) | 0.057 (0.036; p=0.115) | 0.023 (0.027; p=0.389) |
| Cov(h_s, w_f) / Var(y_f) | 0.017 (0.024; p=0.468) | -0.011 (0.012; p=0.370) | -0.030* (0.017; p=0.069) | 0.028 (0.027; p=0.290) |
| Cov(h_s, h_f) / Var(y_f) | 0.026*** (0.010; p=0.007) | 0.014** (0.006; p=0.020) | 0.018 (0.021; p=0.399) | 0.011 (0.011; p=0.322) |
| Sum = earnings IGE | 0.248*** (0.061; p=<0.001) | 0.389*** (0.033; p=<0.001) | 0.302*** (0.050; p=<0.001) | -0.141** (0.069; p=0.041) |
| Share of Var(y_f): Var(w_f) | 0.770*** (0.051; p=<0.001) | 0.879*** (0.055; p=<0.001) | 0.729*** (0.095; p=<0.001) | -0.109 (0.075; p=0.147) |
| Share of Var(y_f): Var(h_f) | 0.219*** (0.027; p=<0.001) | 0.202*** (0.020; p=<0.001) | 0.429*** (0.056; p=<0.001) | 0.017 (0.033; p=0.606) |
| Share of Var(y_f): 2Cov(w_f, h_f) | 0.010 (0.057; p=0.853) | -0.081 (0.055; p=0.138) | -0.158 (0.101; p=0.117) | 0.092 (0.079; p=0.246) |
| Wage transmission Cov(w_s, w_f) / Var(w_f) | 0.195*** (0.054; p=<0.001) | 0.403*** (0.034; p=<0.001) | 0.353*** (0.051; p=<0.001) | -0.208*** (0.064; p=0.001) |
| Hours transmission Cov(h_s, h_f) / Var(h_f) | 0.118** (0.046; p=0.011) | 0.072** (0.033; p=0.029) | 0.042 (0.051; p=0.415) | 0.046 (0.057; p=0.415) |
| Var(y_f) (partialled) | 0.290*** (0.025; p=<0.001) | 0.305*** (0.028; p=<0.001) | 0.313*** (0.039; p=<0.001) | -0.014 (0.038; p=0.705) |
| Var(w_f) (partialled) | 0.224*** (0.018; p=<0.001) | 0.268*** (0.017; p=<0.001) | 0.228*** (0.019; p=<0.001) | -0.044* (0.024; p=0.068) |
| Var(h_f) (partialled) | 0.064*** (0.008; p=<0.001) | 0.062*** (0.008; p=<0.001) | 0.134*** (0.025; p=<0.001) | 0.002 (0.012; p=0.859) |

## 2. Purging shocks: clean years and potential earnings

One regression per column; columns: (1) ln earnings on father's ln earnings (benchmark); (2) ln earnings on father's ln earnings, children with a clean-years father measure; (3) ln earnings, clean years A (no displacement / unemployment), both generations; (4) ln earnings, clean years B (A and no reduced hours), both generations; (5) ln earnings on father's ln potential earnings (ln wage + ln 2,000); (6) ln potential earnings on father's ln potential earnings (= wage IGE); (7) ln potential earnings on father's ln earnings; (8) same, father-present children; (9) ln family income on father's mean ln family income, all years (clean-measure children); (10) ln family income on father's mean ln family income, clean years both generations. Change in the gap (positive = smaller gap) and [share of the gap closed]: (3)-(4) relative to (2) (same children), (5)-(7) relative to (1), (10) relative to (9); the share is a ratio of noisy gaps, so only the change carries a bootstrap s.e. Clean years: a father's (son's) measure is the mean over his clean valid years (>= 3). Potential earnings use the observed hourly wage, which itself carries shocks (division bias, wage cuts after displacement); column (6) is the wage IGE in logs. Daughters: the displacement and unemployment flags exist for male heads only, so the daughters' own years are cleaned only for reduced hours (never, since the full-time-attachment rule is for men) and the cleaning is on the father's side.

| | (1) earn | (2) earn_cs | (3) cleanA | (4) cleanB | (5) fpot | (6) pot | (7) spot | (8) fam_fp | (9) fam_logs | (10) fam_clean |
|---|---|---|---|---|---|---|---|---|---|---|
| **Sons, Lee-Solon (age 40), father's childhood window** | | | | | | | | | | |
| Black: coefficient on the parental measure | 0.220*** (0.064; p=<0.001) | 0.231*** (0.082; p=0.005) | 0.225*** (0.067; p=<0.001) | 0.242*** (0.072; p=<0.001) | 0.187** (0.074; p=0.012) | 0.195*** (0.057; p=<0.001) | 0.210*** (0.049; p=<0.001) | 0.379*** (0.085; p=<0.001) | 0.388*** (0.077; p=<0.001) | 0.345*** (0.076; p=<0.001) |
| Black: N / children | 7,341 / 868 | 6,009 / 706 | 4,468 / 649 | 4,135 / 621 | 7,341 / 868 | 7,341 / 868 | 7,341 / 868 | 8,168 / 887 | 6,826 / 743 | 4,680 / 675 |
| White: coefficient on the parental measure | 0.389*** (0.035; p=<0.001) | 0.388*** (0.040; p=<0.001) | 0.384*** (0.038; p=<0.001) | 0.417*** (0.038; p=<0.001) | 0.402*** (0.041; p=<0.001) | 0.402*** (0.038; p=<0.001) | 0.378*** (0.032; p=<0.001) | 0.543*** (0.045; p=<0.001) | 0.488*** (0.051; p=<0.001) | 0.428*** (0.045; p=<0.001) |
| White: N / children | 23,396 / 2,217 | 20,929 / 1,939 | 17,585 / 1,902 | 16,606 / 1,841 | 23,396 / 2,217 | 23,396 / 2,217 | 23,396 / 2,217 | 24,671 / 2,241 | 22,428 / 2,005 | 18,236 / 1,952 |
| Black - White gap (bootstrap) | -0.169** (0.074; p=0.022) | -0.157* (0.089; p=0.076) | -0.159** (0.077; p=0.039) | -0.175** (0.080; p=0.028) | -0.215** (0.084; p=0.011) | -0.207*** (0.068; p=0.002) | -0.168*** (0.059; p=0.005) | -0.164* (0.096; p=0.086) | -0.099 (0.089; p=0.264) | -0.083 (0.082; p=0.313) |
| Change in the gap vs its reference column (bootstrap) [share closed] |  |  | -0.002 (0.042; p=0.969) [-1%] | -0.018 (0.044; p=0.689) [-11%] | -0.046 (0.039; p=0.246) [-27%] | -0.038 (0.044; p=0.397) [-22%] | 0.002 (0.030; p=0.952) [1%] |  |  | 0.016 (0.051; p=0.749) [16%] |
| **Sons, Lee-Solon (age 40), father's working life 25-55** | | | | | | | | | | |
| Black: coefficient on the parental measure | 0.325*** (0.075; p=<0.001) | 0.286*** (0.084; p=<0.001) | 0.297*** (0.078; p=<0.001) | 0.354*** (0.084; p=<0.001) | 0.329*** (0.086; p=<0.001) | 0.314*** (0.068; p=<0.001) | 0.287*** (0.061; p=<0.001) | 0.324*** (0.086; p=<0.001) | 0.365*** (0.095; p=<0.001) | 0.359*** (0.085; p=<0.001) |
| Black: N / children | 7,045 / 881 | 6,086 / 769 | 4,566 / 707 | 4,316 / 691 | 7,045 / 881 | 7,045 / 881 | 7,045 / 881 | 7,789 / 899 | 6,799 / 794 | 4,687 / 725 |
| White: coefficient on the parental measure | 0.454*** (0.043; p=<0.001) | 0.469*** (0.046; p=<0.001) | 0.451*** (0.045; p=<0.001) | 0.473*** (0.044; p=<0.001) | 0.456*** (0.049; p=<0.001) | 0.449*** (0.046; p=<0.001) | 0.431*** (0.039; p=<0.001) | 0.521*** (0.048; p=<0.001) | 0.575*** (0.056; p=<0.001) | 0.507*** (0.049; p=<0.001) |
| White: N / children | 22,697 / 2,228 | 21,807 / 2,134 | 18,235 / 2,081 | 17,424 / 2,060 | 22,697 / 2,228 | 22,697 / 2,228 | 22,697 / 2,228 | 23,961 / 2,250 | 23,056 / 2,162 | 18,644 / 2,095 |
| Black - White gap (bootstrap) | -0.129 (0.083; p=0.120) | -0.182* (0.100; p=0.068) | -0.154* (0.087; p=0.079) | -0.119 (0.094; p=0.206) | -0.127 (0.094; p=0.176) | -0.136* (0.080; p=0.090) | -0.145** (0.071; p=0.042) | -0.197** (0.099; p=0.046) | -0.210* (0.114; p=0.066) | -0.148* (0.090; p=0.100) |
| Change in the gap vs its reference column (bootstrap) [share closed] |  |  | 0.029 (0.048; p=0.551) [16%] | 0.063 (0.050; p=0.205) [34%] | 0.002 (0.040; p=0.959) [2%] | -0.007 (0.051; p=0.890) [-5%] | -0.016 (0.035; p=0.655) [-12%] |  |  | 0.061 (0.067; p=0.360) [29%] |
| **Sons, lifetime mean, father's childhood window** | | | | | | | | | | |
| Black: coefficient on the parental measure | 0.251*** (0.045; p=<0.001) | 0.241*** (0.062; p=<0.001) | 0.211*** (0.057; p=<0.001) | 0.212*** (0.060; p=<0.001) | 0.221*** (0.059; p=<0.001) | 0.229*** (0.042; p=<0.001) | 0.225*** (0.033; p=<0.001) | 0.346*** (0.063; p=<0.001) | 0.324*** (0.069; p=<0.001) | 0.226*** (0.064; p=<0.001) |
| Black: N / children | 712 / 712 | 588 / 588 | 492 / 492 | 459 / 459 | 712 / 712 | 712 / 712 | 712 / 712 | 741 / 741 | 622 / 622 | 515 / 515 |
| White: coefficient on the parental measure | 0.296*** (0.024; p=<0.001) | 0.288*** (0.027; p=<0.001) | 0.275*** (0.027; p=<0.001) | 0.307*** (0.028; p=<0.001) | 0.301*** (0.029; p=<0.001) | 0.318*** (0.025; p=<0.001) | 0.287*** (0.021; p=<0.001) | 0.400*** (0.032; p=<0.001) | 0.341*** (0.033; p=<0.001) | 0.309*** (0.031; p=<0.001) |
| White: N / children | 1,975 / 1,975 | 1,740 / 1,740 | 1,636 / 1,636 | 1,570 / 1,570 | 1,975 / 1,975 | 1,975 / 1,975 | 1,975 / 1,975 | 2,004 / 2,004 | 1,806 / 1,806 | 1,682 / 1,682 |
| Black - White gap (bootstrap) | -0.044 (0.050; p=0.372) | -0.047 (0.065; p=0.465) | -0.064 (0.063; p=0.307) | -0.094 (0.067; p=0.157) | -0.080 (0.063; p=0.204) | -0.089* (0.048; p=0.063) | -0.062 (0.038; p=0.102) | -0.053 (0.065; p=0.411) | -0.017 (0.071; p=0.811) | -0.083 (0.074; p=0.264) |
| Change in the gap vs its reference column (bootstrap) [share closed] |  |  | -0.017 (0.044; p=0.697) [-36%] | -0.047 (0.051; p=0.357) [-100%] | -0.035 (0.033; p=0.286) [-80%] | -0.045 (0.038; p=0.233) [-101%] | -0.018 (0.027; p=0.502) [-40%] |  |  | -0.066 (0.060; p=0.271) [-386%] |
| **Daughters, Lee-Solon (age 40), father's childhood window** | | | | | | | | | | |
| Black: coefficient on the parental measure | 0.276*** (0.053; p=<0.001) | 0.311*** (0.069; p=<0.001) | 0.312*** (0.071; p=<0.001) | 0.385*** (0.075; p=<0.001) | 0.349*** (0.071; p=<0.001) | 0.315*** (0.053; p=<0.001) | 0.251*** (0.041; p=<0.001) | 0.339*** (0.074; p=<0.001) | 0.348*** (0.081; p=<0.001) | 0.291*** (0.076; p=<0.001) |
| Black: N / children | 9,152 / 957 | 7,492 / 781 | 7,492 / 781 | 7,250 / 751 | 9,152 / 957 | 9,152 / 957 | 9,152 / 957 | 11,364 / 998 | 9,482 / 824 | 7,853 / 800 |
| White: coefficient on the parental measure | 0.255*** (0.047; p=<0.001) | 0.259*** (0.050; p=<0.001) | 0.258*** (0.051; p=<0.001) | 0.252*** (0.053; p=<0.001) | 0.209*** (0.051; p=<0.001) | 0.295*** (0.036; p=<0.001) | 0.329*** (0.033; p=<0.001) | 0.512*** (0.042; p=<0.001) | 0.473*** (0.041; p=<0.001) | 0.422*** (0.042; p=<0.001) |
| White: N / children | 21,343 / 2,213 | 19,346 / 1,951 | 19,346 / 1,951 | 18,990 / 1,900 | 21,343 / 2,213 | 21,343 / 2,213 | 21,343 / 2,213 | 26,024 / 2,270 | 23,720 / 2,027 | 20,264 / 1,990 |
| Black - White gap (bootstrap) | 0.021 (0.068; p=0.763) | 0.052 (0.088; p=0.553) | 0.055 (0.092; p=0.550) | 0.133 (0.088; p=0.132) | 0.141* (0.084; p=0.095) | 0.020 (0.062; p=0.748) | -0.079 (0.051; p=0.126) | -0.173** (0.081; p=0.033) | -0.125 (0.085; p=0.139) | -0.132 (0.083; p=0.111) |
| Change in the gap vs its reference column (bootstrap) [share closed] |  |  | 0.003 (0.020; p=0.889) [-5%] | 0.081** (0.035; p=0.020) [-156%] | 0.120** (0.049; p=0.013) [-583%] | -0.001 (0.049; p=0.987) [4%] | -0.099*** (0.032; p=0.002) [482%] |  |  | -0.006 (0.041; p=0.877) [-5%] |
| **Sons 35-55, Lee-Solon (age 40), father's childhood window** | | | | | | | | | | |
| Black: coefficient on the parental measure | 0.183*** (0.070; p=0.009) | 0.226** (0.092; p=0.014) | 0.236*** (0.075; p=0.002) | 0.232*** (0.078; p=0.003) | 0.152* (0.080; p=0.057) | 0.178*** (0.063; p=0.004) | 0.192*** (0.056; p=<0.001) | 0.366*** (0.086; p=<0.001) | 0.387*** (0.082; p=<0.001) | 0.347*** (0.086; p=<0.001) |
| Black: N / children | 3,346 / 573 | 2,738 / 464 | 2,237 / 427 | 2,079 / 407 | 3,346 / 573 | 3,346 / 573 | 3,346 / 573 | 3,840 / 596 | 3,199 / 495 | 2,352 / 444 |
| White: coefficient on the parental measure | 0.394*** (0.036; p=<0.001) | 0.392*** (0.042; p=<0.001) | 0.384*** (0.040; p=<0.001) | 0.413*** (0.038; p=<0.001) | 0.408*** (0.042; p=<0.001) | 0.404*** (0.040; p=<0.001) | 0.379*** (0.033; p=<0.001) | 0.549*** (0.048; p=<0.001) | 0.489*** (0.053; p=<0.001) | 0.422*** (0.047; p=<0.001) |
| White: N / children | 10,997 / 1,597 | 9,943 / 1,428 | 8,768 / 1,389 | 8,367 / 1,355 | 10,997 / 1,597 | 10,997 / 1,597 | 10,997 / 1,597 | 11,839 / 1,631 | 10,839 / 1,487 | 9,124 / 1,423 |
| Black - White gap (bootstrap) | -0.211*** (0.074; p=0.005) | -0.166* (0.100; p=0.097) | -0.148* (0.085; p=0.083) | -0.181** (0.091; p=0.046) | -0.256*** (0.089; p=0.004) | -0.226*** (0.070; p=0.001) | -0.187*** (0.061; p=0.002) | -0.183* (0.096; p=0.057) | -0.102 (0.096; p=0.290) | -0.076 (0.096; p=0.433) |
| Change in the gap vs its reference column (bootstrap) [share closed] |  |  | 0.018 (0.044; p=0.678) [11%] | -0.015 (0.052; p=0.774) [-9%] | -0.044 (0.043; p=0.305) [-21%] | -0.015 (0.044; p=0.736) [-7%] | 0.024 (0.031; p=0.427) [12%] |  |  | 0.026 (0.063; p=0.675) [26%] |

## 3. Instability

### 3a. Instability of fathers and sons, by race

Means over the person's head-years in the window (one row per son; fathers repeat across brothers). Black - White = coefficient on Black in a regression of the measure on a constant and a Black dummy, s.e. clustered by 1968 family. Transitory ln earnings = residual after person FE, an age quartic and year FE (male heads 25-60, by race), so it includes any deviation from the person's mean (also permanent shocks within the window). Fathers: father-present sons with father's childhood earnings.

| | Fathers (childhood): Black | White | Black - White | Fathers (25-55): Black | White | Black - White | Sons (25-55): Black | White | Black - White |
|---|---|---|---|---|---|---|---|---|---|
| Share of years displaced (closure / layoff, t or t-1) | 0.074 | 0.065 | 0.009 (0.008; p=0.265) | 0.085 | 0.068 | 0.017** (0.007; p=0.016) | 0.162 | 0.089 | 0.072*** (0.006; p=<0.001) |
| Share of years with unemployment | 0.150 | 0.110 | 0.040*** (0.013; p=0.002) | 0.174 | 0.119 | 0.054*** (0.012; p=<0.001) | 0.310 | 0.150 | 0.159*** (0.009; p=<0.001) |
| Share laid off / looking at the interview | 0.050 | 0.036 | 0.013* (0.008; p=0.079) | 0.057 | 0.038 | 0.019*** (0.007; p=0.007) | 0.179 | 0.061 | 0.118*** (0.007; p=<0.001) |
| Share of years with reduced hours (< 1,500, full-time attached) | 0.063 | 0.054 | 0.009 (0.007; p=0.201) | 0.070 | 0.058 | 0.012** (0.006; p=0.028) | 0.092 | 0.068 | 0.024*** (0.004; p=<0.001) |
| Share of years with zero hours | 0.018 | 0.009 | 0.010*** (0.003; p=0.002) | 0.035 | 0.017 | 0.018*** (0.005; p=<0.001) | 0.124 | 0.045 | 0.080*** (0.007; p=<0.001) |
| Share of years displaced or unemployed | 0.186 | 0.141 | 0.045*** (0.014; p=0.001) | 0.211 | 0.150 | 0.061*** (0.013; p=<0.001) | 0.369 | 0.190 | 0.180*** (0.010; p=<0.001) |
| Variance of transitory ln earnings | 0.140 | 0.121 | 0.019 (0.016; p=0.237) | 0.181 | 0.173 | 0.008 (0.014; p=0.559) | 0.360 | 0.253 | 0.107*** (0.015; p=<0.001) |
| Head-years observed | 5.340 | 5.431 | -0.091 (0.068; p=0.181) | 16.347 | 19.274 | -2.926*** (0.378; p=<0.001) | 8.540 | 10.642 | -2.102*** (0.204; p=<0.001) |

### 3b. Intergenerational persistence of instability

One regression per column: the son's measure (header) on the father's same measure over the childhood window; controls: son's birth-year FE, quadratics in the son's mean age and the father's age at 16. Linear in shares (not elasticities).

| | (1) son's displaced | (2) son's unemployment | (3) son's reduced hours | (4) son's zero hours | (5) son's displaced or unemployed | (6) son's ln transitory variance |
|---|---|---|---|---|---|---|
| **Black** | | | | | | |
| Father's same measure (childhood window) | 0.010 (0.038; p=0.801) | 0.103*** (0.038; p=0.006) | 0.014 (0.031; p=0.656) | 0.192** (0.097; p=0.049) | 0.075** (0.036; p=0.040) | 0.059* (0.033; p=0.069) |
| N sons / clusters | 868 / 400 | 868 / 400 | 868 / 400 | 868 / 400 | 868 / 400 | 687 / 337 |
| **White** | | | | | | |
| Father's same measure (childhood window) | 0.057*** (0.022; p=0.009) | 0.114*** (0.027; p=<0.001) | -0.003 (0.017; p=0.867) | -0.021 (0.039; p=0.595) | 0.127*** (0.024; p=<0.001) | 0.060*** (0.019; p=0.001) |
| N sons / clusters | 2,217 / 977 | 2,217 / 977 | 2,217 / 977 | 2,217 / 977 | 2,217 / 977 | 1,916 / 911 |

## 4. Human capital mediation (Palomino et al. 2018 / BFHO style)

Lee-Solon design (age 40), sons 25-55, valid years. One regression per column; the outcome is the header; the same sample within a panel. Share mediated = 1 - beta(with mediators) / beta(without). Because ln earnings = ln wage + ln hours, the ln earnings IGE on the parental measure is the sum of the ln wage and ln hours IGEs (columns (1) = (4) + (6) in 4a). Education and the son's instability shares are outcomes of the same background, so 'mediation' is an accounting of coefficient movements, order-dependent and not causal.

### 4a. Benchmark regressor (parental family income), all sons

| | (1) ln earnings | (2) ln earnings | (3) ln earnings | (4) ln wage | (5) ln wage | (6) ln hours | (7) ln hours | (8) ln hours |
|---|---|---|---|---|---|---|---|---|
| **Sons: Black** | | | | | | | | |
| ln parental family income (13-19 mean) | 0.214*** (0.039; p=<0.001) | 0.141*** (0.036; p=<0.001) | 0.117*** (0.029; p=<0.001) | 0.164*** (0.029; p=<0.001) | 0.115*** (0.026; p=<0.001) | 0.050*** (0.018; p=0.006) | 0.027 (0.019; p=0.146) | 0.013 (0.015; p=0.407) |
| Son's years of education |  | 0.122*** (0.008; p=<0.001) | 0.064*** (0.007; p=<0.001) |  | 0.084*** (0.006; p=<0.001) |  | 0.039*** (0.004; p=<0.001) | 0.005* (0.003; p=0.077) |
| Son's share of years with unemployment |  |  | -0.977*** (0.063; p=<0.001) |  |  |  |  | -0.598*** (0.036; p=<0.001) |
| Son's share of years displaced |  |  | -0.219*** (0.075; p=0.003) |  |  |  |  | -0.054 (0.047; p=0.251) |
| Son's share of years with reduced hours |  |  | -0.352*** (0.094; p=<0.001) |  |  |  |  | -0.147** (0.058; p=0.012) |
| Son's share of years with zero hours |  |  | -1.250*** (0.104; p=<0.001) |  |  |  |  | -0.711*** (0.070; p=<0.001) |
| Share of the IGE mediated (vs the first column of the same outcome) |  | 0.340 | 0.454 |  | 0.303 |  | 0.463 | 0.746 |
| Child-years / sons / clusters | 14,667 / 1,923 / 646 | 14,667 / 1,923 / 646 | 14,667 / 1,923 / 646 | 14,667 / 1,923 / 646 | 14,667 / 1,923 / 646 | 14,667 / 1,923 / 646 | 14,667 / 1,923 / 646 | 14,667 / 1,923 / 646 |
| **Sons: White** | | | | | | | | |
| ln parental family income (13-19 mean) | 0.447*** (0.036; p=<0.001) | 0.337*** (0.035; p=<0.001) | 0.303*** (0.032; p=<0.001) | 0.413*** (0.033; p=<0.001) | 0.308*** (0.032; p=<0.001) | 0.034*** (0.013; p=0.009) | 0.029** (0.014; p=0.032) | 0.012 (0.012; p=0.287) |
| Son's years of education |  | 0.074*** (0.006; p=<0.001) | 0.050*** (0.005; p=<0.001) |  | 0.070*** (0.005; p=<0.001) |  | 0.003 (0.003; p=0.221) | -0.007*** (0.002; p=<0.001) |
| Son's share of years with unemployment |  |  | -0.725*** (0.080; p=<0.001) |  |  |  |  | -0.368*** (0.034; p=<0.001) |
| Son's share of years displaced |  |  | -0.231*** (0.087; p=0.008) |  |  |  |  | 0.069* (0.038; p=0.070) |
| Son's share of years with reduced hours |  |  | -1.111*** (0.114; p=<0.001) |  |  |  |  | -0.758*** (0.043; p=<0.001) |
| Son's share of years with zero hours |  |  | -1.135*** (0.135; p=<0.001) |  |  |  |  | -0.693*** (0.075; p=<0.001) |
| Share of the IGE mediated (vs the first column of the same outcome) |  | 0.246 | 0.324 |  | 0.255 |  | 0.142 | 0.640 |
| Child-years / sons / clusters | 27,562 / 2,716 / 1,105 | 27,562 / 2,716 / 1,105 | 27,562 / 2,716 / 1,105 | 27,562 / 2,716 / 1,105 | 27,562 / 2,716 / 1,105 | 27,562 / 2,716 / 1,105 | 27,562 / 2,716 / 1,105 | 27,562 / 2,716 / 1,105 |

### 4b. Father's ln earnings, father-present sons with the father's education

| | (1) ln earnings | (2) ln earnings | (3) ln earnings | (4) ln earnings | (5) ln wage | (6) ln wage | (7) ln hours | (8) ln hours |
|---|---|---|---|---|---|---|---|---|
| **Sons: Black** | | | | | | | | |
| Father's ln earnings (childhood window) | 0.226*** (0.064; p=<0.001) | 0.135** (0.054; p=0.012) | 0.145** (0.059; p=0.013) | 0.150*** (0.049; p=0.002) | 0.216*** (0.050; p=<0.001) | 0.156*** (0.045; p=<0.001) | 0.010 (0.027; p=0.723) | -0.011 (0.027; p=0.692) |
| Son's years of education |  | 0.122*** (0.012; p=<0.001) | 0.124*** (0.012; p=<0.001) | 0.073*** (0.010; p=<0.001) |  | 0.088*** (0.009; p=<0.001) |  | 0.037*** (0.006; p=<0.001) |
| Father's years of education |  |  | -0.005 (0.008; p=0.542) | -0.002 (0.007; p=0.772) |  | -0.002 (0.006; p=0.721) |  | -0.003 (0.004; p=0.445) |
| Son's share of years with unemployment |  |  |  | -1.031*** (0.100; p=<0.001) |  |  |  |  |
| Son's share of years displaced |  |  |  | -0.157 (0.110; p=0.153) |  |  |  |  |
| Son's share of years with reduced hours |  |  |  | -0.366*** (0.131; p=0.005) |  |  |  |  |
| Son's share of years with zero hours |  |  |  | -1.200*** (0.152; p=<0.001) |  |  |  |  |
| Share of the IGE mediated (vs the first column of the same outcome) |  | 0.400 | 0.355 | 0.336 |  | 0.276 |  | 2.122 |
| Child-years / sons / clusters | 7,260 / 860 / 398 | 7,260 / 860 / 398 | 7,260 / 860 / 398 | 7,260 / 860 / 398 | 7,260 / 860 / 398 | 7,260 / 860 / 398 | 7,260 / 860 / 398 | 7,260 / 860 / 398 |
| **Sons: White** | | | | | | | | |
| Father's ln earnings (childhood window) | 0.390*** (0.035; p=<0.001) | 0.288*** (0.034; p=<0.001) | 0.279*** (0.036; p=<0.001) | 0.267*** (0.033; p=<0.001) | 0.379*** (0.032; p=<0.001) | 0.267*** (0.032; p=<0.001) | 0.011 (0.013; p=0.379) | 0.012 (0.014; p=0.402) |
| Son's years of education |  | 0.074*** (0.007; p=<0.001) | 0.073*** (0.007; p=<0.001) | 0.049*** (0.006; p=<0.001) |  | 0.067*** (0.006; p=<0.001) |  | 0.006* (0.003; p=0.053) |
| Father's years of education |  |  | 0.004 (0.006; p=0.465) | 0.003 (0.005; p=0.522) |  | 0.007 (0.005; p=0.130) |  | -0.003 (0.003; p=0.220) |
| Son's share of years with unemployment |  |  |  | -0.671*** (0.091; p=<0.001) |  |  |  |  |
| Son's share of years displaced |  |  |  | -0.314*** (0.099; p=0.001) |  |  |  |  |
| Son's share of years with reduced hours |  |  |  | -1.178*** (0.134; p=<0.001) |  |  |  |  |
| Son's share of years with zero hours |  |  |  | -1.075*** (0.156; p=<0.001) |  |  |  |  |
| Share of the IGE mediated (vs the first column of the same outcome) |  | 0.261 | 0.285 | 0.315 |  | 0.295 |  | -0.075 |
| Child-years / sons / clusters | 23,263 / 2,205 / 970 | 23,263 / 2,205 / 970 | 23,263 / 2,205 / 970 | 23,263 / 2,205 / 970 | 23,263 / 2,205 / 970 | 23,263 / 2,205 / 970 | 23,263 / 2,205 / 970 | 23,263 / 2,205 / 970 |

## 5. Reliability and attenuation of the father's measure

Reliability ratio (4.Estimates.py / BFHO Appendix B logic, in the father generation): slope of the father's mean over his valid years at 25-55 at least 3 years (one-year measure) or 6 years (childhood-window mean) away from the measurement, on the measure; controls: his age (quadratic) or his age at the child's 16 (quadratic). One row per father-present son; s.e. clustered by 1968 family. One column per regression.

| | ln earnings: one year at 16 | ln earnings: childhood mean | ln wage: one year at 16 | ln wage: childhood mean | ln hours: one year at 16 | ln hours: childhood mean | ln family income: one year at 16 | ln family income: childhood mean |
|---|---|---|---|---|---|---|---|---|
| Black: reliability ratio | 0.519*** (0.026; p=<0.001) | 0.623*** (0.031; p=<0.001) | 0.464*** (0.023; p=<0.001) | 0.593*** (0.021; p=<0.001) | 0.171*** (0.028; p=<0.001) | 0.360*** (0.048; p=<0.001) | 0.582*** (0.022; p=<0.001) | 0.697*** (0.024; p=<0.001) |
| White: reliability ratio | 0.551*** (0.019; p=<0.001) | 0.622*** (0.018; p=<0.001) | 0.519*** (0.016; p=<0.001) | 0.625*** (0.016; p=<0.001) | 0.303*** (0.023; p=<0.001) | 0.422*** (0.028; p=<0.001) | 0.546*** (0.018; p=<0.001) | 0.666*** (0.017; p=<0.001) |
| Black: N sons | 1,467 | 1,364 | 1,467 | 1,364 | 1,467 | 1,364 | 1,526 | 1,398 |
| White: N sons | 3,234 | 3,103 | 3,234 | 3,103 | 3,234 | 3,103 | 3,301 | 3,141 |

Transitory share of the variance of single-year ln earnings (fathers, valid years at 25-55, ln earnings net of an age quartic and year FE; transitory = deviation from the person mean): Black 0.432 (transitory variance 0.184 of 0.425, 15,208 father-years); White 0.422 (transitory variance 0.172 of 0.408, 39,994 father-years).

Implied attenuation (IGE / reliability ratio of the childhood-window mean; delta-method s.e. treating the two as independent). 4.Estimates.py reports family-income reliability ratios of 0.565 / 0.585 (one year) and 0.631 / 0.650 (12-17 mean) for Black / White, estimated in the child generation.

| | Black IGE | Black RR | Black corrected | White IGE | White RR | White corrected | Black / White ratio: raw -> corrected |
|---|---|---|---|---|---|---|---|
| Father-earnings IGE (sons, Lee-Solon, childhood window) | 0.220*** (0.060; p=<0.001) | 0.623 | 0.353*** (0.098; p=<0.001) | 0.389*** (0.034; p=<0.001) | 0.622 | 0.625*** (0.058; p=<0.001) | 0.565 -> 0.564 |
| Parental family-income IGE (sons, Lee-Solon, 6.IGEMain regressor) | 0.273*** (0.050; p=<0.001) | 0.697 | 0.392*** (0.072; p=<0.001) | 0.472*** (0.036; p=<0.001) | 0.666 | 0.709*** (0.057; p=<0.001) | 0.578 -> 0.553 |

## 6. Composition: the parental income distribution

Lee-Solon design, sons 25-55. One regression per cell (column = regression type, row = sample). Re-weighting: White child-years re-weighted so that the distribution of the parental measure over 20 pooled quantile bins matches the Black one (DiNardo-Fortin-Lemieux), analytic weighted s.e. Common support = between the larger of the two 5th percentiles and the smaller of the two 95th percentiles. Terciles of the pooled child-year distribution (slopes within a tercile are local and noisy).

| | (1) ln family income on ln parental family income (all sons) | (2) ln earnings on father's ln earnings (father-present sons) |
|---|---|---|
| Black | 0.273*** (0.048; p=<0.001) (N 16,599) | 0.220*** (0.064; p=<0.001) (N 7,341) |
| White | 0.472*** (0.039; p=<0.001) (N 29,124) | 0.389*** (0.035; p=<0.001) (N 23,396) |
| White re-weighted to the Black distribution | 0.354*** (0.102; p=<0.001) (N 29,124) | 0.324*** (0.047; p=<0.001) (N 23,396) |
| Black, common support | 0.507*** (0.123; p=<0.001) (N 9,503) | 0.269** (0.116; p=0.021) (N 5,875) |
| White, common support | 0.561*** (0.074; p=<0.001) (N 18,597) | 0.350*** (0.067; p=<0.001) (N 15,612) |
| Black, pooled parental tercile 1 | 0.119 (0.086; p=0.169) (N 10,497) | 0.168 (0.104; p=0.105) (N 4,420) |
| White, pooled parental tercile 1 | 0.215 (0.183; p=0.241) (N 4,744) | 0.267*** (0.090; p=0.003) (N 5,832) |
| Black, pooled parental tercile 2 | 0.632* (0.322; p=0.050) (N 4,411) | 0.629 (0.431; p=0.144) (N 2,260) |
| White, pooled parental tercile 2 | 0.636*** (0.196; p=0.001) (N 10,834) | -0.144 (0.224; p=0.522) (N 7,992) |
| Black, pooled parental tercile 3 | 0.802** (0.401; p=0.045) (N 1,691) | -0.591 (0.379; p=0.119) (N 669) |
| White, pooled parental tercile 3 | 0.266*** (0.085; p=0.002) (N 13,558) | 0.371*** (0.102; p=<0.001) (N 9,583) |
| Share of the Black-White gap due to composition (bootstrap) | 0.593 (0.653; p=0.364) | 0.384 (1.831; p=0.834) |

(1) ln family income on ln parental family income (all sons): share of child-years in the bottom / top pooled tercile: Black 0.63 / 0.10, White 0.16 / 0.47; common support = [10.10, 11.29]; (2) ln earnings on father's ln earnings (father-present sons): share of child-years in the bottom / top pooled tercile: Black 0.60 / 0.09, White 0.25 / 0.41; common support = [9.62, 10.99].

## 7. Decomposition of the Black-White gap in the father-earnings IGE

Exact identity: gap = composition + wage transmission + (wage-share + hours transmission + hours-share) + cross terms (Lee-Solon columns: slope over child-years without the age interactions, Section 1c), with W* = White children re-weighted to the Black distribution of the father's ln earnings and s = shares of the (partialled) variance of the father's ln earnings (Section 1c). Share of the gap in brackets (not shown for daughters, whose gap is about zero). Bootstrap s.e. (200 draws of 1968 families within race). Accounting, not causal: the 'hours' rows say how much of the gap sits in the hours component of measured earnings, which mixes shocks (layoffs, unemployment, short hours) with labor-supply and search-friction differences.

| | Sons, Lee-Solon (age 40), father's childhood window | Sons, Lee-Solon (age 40), father's working life 25-55 | Sons, lifetime mean, father's childhood window | Daughters, Lee-Solon (age 40), father's childhood window | Sons 35-55, Lee-Solon (age 40), father's childhood window |
|---|---|---|---|---|---|
| Reference: Black earnings IGE at age 40 (Lee-Solon with interactions; = Section 1 col. 1) | 0.220*** (0.060; p=<0.001) | 0.325*** (0.076; p=<0.001) | 0.251*** (0.045; p=<0.001) | 0.276*** (0.054; p=<0.001) | 0.183*** (0.067; p=0.006) |
| Reference: White earnings IGE at age 40 | 0.389*** (0.034; p=<0.001) | 0.454*** (0.043; p=<0.001) | 0.296*** (0.024; p=<0.001) | 0.255*** (0.044; p=<0.001) | 0.394*** (0.036; p=<0.001) |
| Reference: gap at age 40 | -0.169** (0.074; p=0.022) | -0.129 (0.083; p=0.120) | -0.044 (0.050; p=0.372) | 0.021 (0.068; p=0.763) | -0.211*** (0.074; p=0.005) |
| Black earnings IGE (decomposed) | 0.255*** (0.041; p=<0.001) | 0.316*** (0.053; p=<0.001) | 0.251*** (0.045; p=<0.001) | 0.270*** (0.048; p=<0.001) | 0.248*** (0.061; p=<0.001) |
| White earnings IGE (decomposed) | 0.315*** (0.025; p=<0.001) | 0.369*** (0.030; p=<0.001) | 0.296*** (0.024; p=<0.001) | 0.298*** (0.028; p=<0.001) | 0.389*** (0.033; p=<0.001) |
| Black - White gap (decomposed) | -0.060 (0.049; p=0.217) | -0.053 (0.059; p=0.370) | -0.044 (0.050; p=0.372) | -0.029 (0.056; p=0.605) | -0.141** (0.068; p=0.039) |
| Composition (White re-weighted to the Black father-earnings distribution) | -0.035 (0.030; p=0.248) [58%] | -0.076* (0.041; p=0.064) [144%] | -0.021 (0.027; p=0.428) [47%] | -0.051 (0.040; p=0.207) | -0.087* (0.049; p=0.072) [62%] |
| Human capital (wage) transmission: (b_w,B - b_w,W*) s_w,W* | -0.085** (0.038; p=0.024) [142%] | -0.014 (0.047; p=0.759) [27%] | -0.054 (0.037; p=0.148) [122%] | 0.079 (0.054; p=0.143) | -0.115** (0.054; p=0.032) [82%] |
| Hours / instability, total of the three rows below | -0.003 (0.026; p=0.897) [6%] | -0.016 (0.040; p=0.686) [31%] | -0.016 (0.026; p=0.544) [35%] | -0.055* (0.032; p=0.092) | 0.016 (0.038; p=0.669) [-11%] |
|   wage share of the father's earnings variance: b_w,B (s_w,B - s_w,W*) | 0.003 (0.017; p=0.869) [-5%] | -0.006 (0.028; p=0.838) [11%] | -0.005 (0.017; p=0.790) [10%] | -0.067*** (0.023; p=0.003) | 0.008 (0.022; p=0.708) [-6%] |
|   hours transmission: (b_h,B - b_h,W*) s_h,W* | 0.019 (0.022; p=0.389) [-31%] | 0.019 (0.027; p=0.476) [-36%] | 0.003 (0.020; p=0.901) [-6%] | 0.018 (0.024; p=0.437) | 0.033 (0.029; p=0.257) [-23%] |
|   hours share of the father's earnings variance: b_h,B (s_h,B - s_h,W*) | -0.025** (0.010; p=0.015) [42%] | -0.030** (0.015; p=0.041) [56%] | -0.013 (0.009; p=0.138) [30%] | -0.006 (0.006; p=0.346) | -0.025** (0.013; p=0.050) [18%] |
| Residual: wage-hours cross terms [Cov(w_s,h_f) + Cov(h_s,w_f)] / Var(y_f) | 0.064 (0.042; p=0.129) [-106%] | 0.054 (0.048; p=0.262) [-102%] | 0.046 (0.038; p=0.225) [-104%] | -0.003 (0.038; p=0.941) | 0.046 (0.055; p=0.409) [-32%] |
