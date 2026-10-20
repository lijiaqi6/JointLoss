# Paper B: public policies and economic shocks (Fable memo designs D1-D3)

Built by `49.PaperBPolicyShocks.py` (2026-10-18); definitions in its docstring. Every coefficient: estimate (s.e.; p), *** p<0.01, ** p<0.05, * p<0.1. **Reduced form / descriptive.**

## D1. Labor-market conditions at entry

Entry year = birth year + 18 + max(schooling - 12, 0). National rate check: correlation of the hard-coded BLS annual national rate with the mean of the LAUS state rates, 1976-2024: 0.995. Each cell: coefficient (s.e.; p); one regression per outcome x specification x sample; regressors: the shock, shock x centred ln parental income, ln parental income, quartic in parent's age, (+ years of schooling), FE in the row label. Pooled weighted (Black + White), races unweighted. The Bartik is a predicted employment growth rate (higher = tighter).

| Specification | Sample | term | access: good job at 25-34 | ln wage, 25-34 | ln wage, 35-55 |
|---|---|---|---|---|---|
| state: entry rate | Pooled | shock | 0.004 (0.008; p=0.649) | -0.002 (0.009; p=0.822) | -0.005 (0.018; p=0.784) |
| state: entry rate | Pooled | shock x ln parental income | 0.011*** (0.004; p=0.006) | 0.008 (0.009; p=0.387) | 0.019 (0.014; p=0.173) |
| | Pooled | N sons / clusters | 3,485 / 50 | 3,591 / 50 | 2,281 / 50 |
| state: entry rate | Black | shock | 0.001 (0.005; p=0.876) | -0.005 (0.012; p=0.689) | -0.035* (0.020; p=0.076) |
| state: entry rate | Black | shock x ln parental income | -0.001 (0.005; p=0.796) | -0.001 (0.011; p=0.933) | -0.002 (0.017; p=0.894) |
| | Black | N sons / clusters | 1,372 / 37 | 1,434 / 37 | 849 / 34 |
| state: entry rate | White | shock | 0.002 (0.008; p=0.777) | 0.003 (0.010; p=0.804) | 0.007 (0.016; p=0.649) |
| state: entry rate | White | shock x ln parental income | 0.009** (0.004; p=0.019) | 0.005 (0.013; p=0.735) | 0.010 (0.022; p=0.659) |
| | White | N sons / clusters | 2,116 / 48 | 2,160 / 48 | 1,433 / 47 |
| state: entry rate, no schooling control | Pooled | shock | 0.002 (0.009; p=0.793) | -0.003 (0.010; p=0.758) | -0.009 (0.018; p=0.613) |
| state: entry rate, no schooling control | Pooled | shock x ln parental income | 0.015*** (0.005; p=0.001) | 0.012 (0.009; p=0.173) | 0.024* (0.014; p=0.080) |
| | Pooled | N sons / clusters | 3,486 / 50 | 3,592 / 50 | 2,281 / 50 |
| state: entry rate, no schooling control | Black | shock | 0.001 (0.006; p=0.827) | -0.004 (0.012; p=0.760) | -0.030 (0.021; p=0.152) |
| state: entry rate, no schooling control | Black | shock x ln parental income | 0.001 (0.006; p=0.911) | 0.004 (0.012; p=0.708) | -0.000 (0.017; p=0.987) |
| | Black | N sons / clusters | 1,372 / 37 | 1,434 / 37 | 849 / 34 |
| state: entry rate, no schooling control | White | shock | 0.002 (0.009; p=0.832) | 0.003 (0.011; p=0.804) | 0.002 (0.017; p=0.896) |
| state: entry rate, no schooling control | White | shock x ln parental income | 0.013*** (0.004; p=0.002) | 0.008 (0.013; p=0.532) | 0.017 (0.023; p=0.440) |
| | White | N sons / clusters | 2,117 / 48 | 2,161 / 48 | 1,433 / 47 |
| state: mean rate over the first 10 years | Pooled | shock | 0.004 (0.010; p=0.681) | -0.011 (0.011; p=0.300) | 0.004 (0.016; p=0.816) |
| state: mean rate over the first 10 years | Pooled | shock x ln parental income | 0.014* (0.007; p=0.056) | 0.012 (0.012; p=0.300) | 0.009 (0.020; p=0.653) |
| | Pooled | N sons / clusters | 3,591 / 50 | 3,702 / 50 | 2,374 / 50 |
| state: mean rate over the first 10 years | Black | shock | 0.004 (0.010; p=0.715) | -0.025 (0.018; p=0.167) | -0.009 (0.029; p=0.749) |
| state: mean rate over the first 10 years | Black | shock x ln parental income | 0.002 (0.006; p=0.682) | 0.011 (0.015; p=0.439) | 0.022 (0.027; p=0.414) |
| | Black | N sons / clusters | 1,425 / 37 | 1,491 / 37 | 895 / 34 |
| state: mean rate over the first 10 years | White | shock | 0.005 (0.011; p=0.646) | 0.002 (0.017; p=0.898) | 0.020 (0.017; p=0.227) |
| state: mean rate over the first 10 years | White | shock x ln parental income | 0.013 (0.008; p=0.101) | 0.001 (0.014; p=0.936) | -0.008 (0.027; p=0.762) |
| | White | N sons / clusters | 2,169 / 48 | 2,214 / 48 | 1,480 / 47 |
| state: men's Bartik at entry | Pooled | shock | 0.002 (0.027; p=0.945) | 0.093*** (0.026; p=<0.001) | 0.001 (0.043; p=0.974) |
| state: men's Bartik at entry | Pooled | shock x ln parental income | -0.012* (0.007; p=0.058) | 0.007 (0.008; p=0.376) | 0.003 (0.015; p=0.854) |
| | Pooled | N sons / clusters | 3,110 / 50 | 3,199 / 50 | 1,963 / 50 |
| state: men's Bartik at entry | Black | shock | 0.029 (0.037; p=0.439) | 0.015 (0.036; p=0.677) | -0.010 (0.074; p=0.889) |
| state: men's Bartik at entry | Black | shock x ln parental income | 0.003 (0.004; p=0.459) | -0.012 (0.017; p=0.460) | -0.011 (0.024; p=0.635) |
| | Black | N sons / clusters | 1,196 / 37 | 1,243 / 37 | 695 / 34 |
| state: men's Bartik at entry | White | shock | -0.006 (0.026; p=0.803) | 0.079*** (0.028; p=0.005) | -0.017 (0.052; p=0.739) |
| state: men's Bartik at entry | White | shock x ln parental income | -0.015** (0.007; p=0.040) | 0.003 (0.009; p=0.712) | 0.006 (0.021; p=0.779) |
| | White | N sons / clusters | 1,917 / 48 | 1,959 / 48 | 1,269 / 47 |
| national: entry rate, cohort trend | Pooled | shock | 0.002 (0.005; p=0.718) | -0.013** (0.005; p=0.011) | -0.005 (0.008; p=0.511) |
| national: entry rate, cohort trend | Pooled | shock x ln parental income | 0.004 (0.007; p=0.527) | 0.004 (0.010; p=0.673) | 0.016 (0.014; p=0.260) |
| | Pooled | N sons / clusters | 4,304 / 53 | 4,437 / 53 | 3,033 / 43 |
| national: entry rate, cohort trend | Black | shock | 0.001 (0.004; p=0.732) | -0.001 (0.013; p=0.926) | 0.018 (0.014; p=0.184) |
| national: entry rate, cohort trend | Black | shock x ln parental income | -0.004 (0.008; p=0.561) | 0.008 (0.012; p=0.510) | 0.036** (0.017; p=0.039) |
| | Black | N sons / clusters | 1,722 / 52 | 1,803 / 52 | 1,147 / 43 |
| national: entry rate, cohort trend | White | shock | 0.002 (0.005; p=0.672) | -0.010* (0.006; p=0.076) | -0.008 (0.012; p=0.522) |
| national: entry rate, cohort trend | White | shock x ln parental income | 0.003 (0.008; p=0.676) | -0.001 (0.012; p=0.945) | 0.014 (0.018; p=0.456) |
| | White | N sons / clusters | 2,585 / 52 | 2,637 / 52 | 1,887 / 43 |

Race differences (White - Black) of the shock coefficient (independent samples):

| Specification | access: good job at 25-34 | ln wage, 25-34 | ln wage, 35-55 |
|---|---|---|---|
| state: entry rate | 0.002 (0.010; p=0.875) | 0.007 (0.016; p=0.641) | 0.042* (0.025; p=0.096) |
| state: entry rate, no schooling control | 0.001 (0.011; p=0.943) | 0.006 (0.016; p=0.694) | 0.032 (0.027; p=0.230) |
| state: mean rate over the first 10 years | 0.001 (0.015; p=0.931) | 0.027 (0.025; p=0.269) | 0.030 (0.033; p=0.374) |
| state: men's Bartik at entry | -0.035 (0.045; p=0.437) | 0.064 (0.046; p=0.165) | -0.007 (0.091; p=0.937) |
| national: entry rate, cohort trend | 0.001 (0.007; p=0.915) | -0.009 (0.014; p=0.530) | -0.026 (0.018; p=0.156) |

### D1 (c). Age profile of the racial gap by entry conditions (sons entering 1976+ with a state at 17)

| | Slack: earnings | Slack: family income | Tight: earnings | Tight: family income |
|---|---|---|---|---|
| W - B gap, 25-29 | -0.056 (0.078; p=0.470) | -0.028 (0.068; p=0.679) | -0.092 (0.069; p=0.181) | -0.060 (0.063; p=0.343) |
| W - B gap, 30-34 | 0.201*** (0.075; p=0.007) | 0.278*** (0.080; p=<0.001) | -0.016 (0.069; p=0.813) | 0.009 (0.076; p=0.902) |
| W - B gap, 35-39 | 0.328*** (0.088; p=<0.001) | 0.309*** (0.091; p=<0.001) | 0.063 (0.084; p=0.450) | 0.026 (0.091; p=0.776) |
| W - B gap, 40-44 | 0.511*** (0.100; p=<0.001) | 0.493*** (0.099; p=<0.001) | 0.160 (0.106; p=0.132) | 0.169 (0.110; p=0.126) |
| W - B gap, 45-49 | 0.466*** (0.144; p=0.001) | 0.306** (0.156; p=0.050) | 0.238 (0.150; p=0.112) | 0.273* (0.143; p=0.056) |
| Black: opening | -0.112* (0.060; p=0.062) | -0.091 (0.061; p=0.135) | -0.063 (0.058; p=0.277) | -0.036 (0.062; p=0.562) |
| White: opening | 0.250*** (0.056; p=<0.001) | 0.153*** (0.059; p=0.010) | 0.145** (0.063; p=0.021) | 0.146** (0.060; p=0.015) |
| White - Black: opening | 0.362*** (0.082; p=<0.001) | 0.244*** (0.085; p=0.004) | 0.208** (0.086; p=0.015) | 0.181** (0.086; p=0.034) |
| Slack minus tight, W - B opening (earnings; family income) | 0.154 (0.119; p=0.193) ; 0.063 (0.121; p=0.604) | | | |

Sons with a state entry rate: Black 1,516, White 2,204. Shared families across the two groups make the slack-minus-tight standard error approximate.

## D2. The public sector

Government item codes (all waves, head): {4: 119694, 0: 89006, 1: 11335, 3: 11265, 2: 10891, 5: 9965}; items by wave: {1980: 'V7097', 1981: 'V7708', 1982: 'V8376', 1983: 'V9007', 1984: 'V10457', 1985: 'V11648', 1986: 'V13051', 1987: 'V14151', 1988: 'V15159', 1989: 'V16660', 1990: 'V18098', 1991: 'V19398', 1992: 'V20698', 1993: 'V22453', 1994: 'ER2078', 1995: 'ER5077', 1996: 'ER7173', 1997: 'ER10088', 1999: 'ER13212', 2001: 'ER17223', 2003: 'ER21149', 2005: 'ER25131', 2007: 'ER36136', 2009: 'ER42171', 2011: 'ER47484', 2013: 'ER53184', 2015: 'ER60199', 2017: 'ER66200', 2019: 'ER72200', 2021: 'ER78205', 2023: 'ER82188'}. Son-years as head with a valid wage; sector = self-employed (codes 2-3 of 'work for self or others'), government (1980-84: 1 = yes; 1985+: federal, state or local government, codes 1-3), private (1980-84: 5 = no; 1985+: private company, code 4).

| Race | parental tercile | sons with a 25-34 sector | government | private | self-employed | good job at 25-34, government starters | good job, private starters |
|---|---|---|---|---|---|---|---|
| Black | 1 | 965 | 0.173 | 0.746 | 0.081 | 0.102 | 0.022 |
| Black | 2 | 535 | 0.219 | 0.701 | 0.080 | 0.184 | 0.024 |
| Black | 3 | 234 | 0.201 | 0.692 | 0.107 | 0.385 | 0.093 |
| Black | all | 1,734 | 0.191 | 0.725 | 0.084 | 0.167 | 0.032 |
| White | 1 | 389 | 0.105 | 0.815 | 0.080 | 0.235 | 0.057 |
| White | 2 | 937 | 0.117 | 0.793 | 0.090 | 0.368 | 0.092 |
| White | 3 | 1,289 | 0.134 | 0.781 | 0.085 | 0.490 | 0.177 |
| White | all | 2,615 | 0.124 | 0.790 | 0.086 | 0.418 | 0.128 |

Government at 25-34 on White (weighted, clusters 1968 family): with ln parental income -0.059** (0.025; p=0.019); + schooling -0.057** (0.025; p=0.020) (N 4,346).

Access to good jobs on White at equal parental income: all sons with a sector 0.044*** (0.016; p=0.007) (N 4,264); private starters 0.048*** (0.014; p=<0.001) (N 3,314).

### D2 (c). Opening of the racial gap by sector at 25-34 (bands 25-49)

| Sample | W - B opening, earnings | W - B opening, family income | minus all sons (earnings; family) |
|---|---|---|---|
| All sons (33) | 0.232*** (0.052; p=<0.001) | 0.157*** (0.055; p=0.004) |  |
| Sons whose 25-34 sector is private | 0.213*** (0.058; p=<0.001) | 0.154** (0.064; p=0.016) | -0.019 (0.035; p=0.581); -0.003 (0.038; p=0.944) |
| Sons whose 25-34 sector is government | 0.215* (0.130; p=0.097) | 0.104 (0.124; p=0.403) |  |

### D2 (d). Return to a year of schooling (ln hourly wage) by age band and race, within the current sector

| Sector | group | 25-29 | 30-34 | 35-39 | 40-44 | 45-49 | 50-55 | rise (>= 35 minus < 35) |
|---|---|---|---|---|---|---|---|---|
| private | White | 0.056*** (0.005; p=<0.001) | 0.104*** (0.006; p=<0.001) | 0.127*** (0.007; p=<0.001) | 0.144*** (0.010; p=<0.001) | 0.138*** (0.012; p=<0.001) | 0.145*** (0.014; p=<0.001) | 0.058*** (0.008; p=<0.001) |
| private | Black | 0.078*** (0.009; p=<0.001) | 0.095*** (0.010; p=<0.001) | 0.104*** (0.013; p=<0.001) | 0.100*** (0.014; p=<0.001) | 0.121*** (0.015; p=<0.001) | 0.127*** (0.019; p=<0.001) | 0.027** (0.011; p=0.015) |
| private | White - Black | -0.022** (0.010; p=0.037) | 0.009 (0.011; p=0.429) | 0.023 (0.014; p=0.113) | 0.044** (0.017; p=0.011) | 0.017 (0.019; p=0.370) | 0.018 (0.024; p=0.449) | 0.032** (0.013; p=0.016) |
| gov | White | 0.033*** (0.012; p=0.004) | 0.044*** (0.012; p=<0.001) | 0.053*** (0.014; p=<0.001) | 0.070*** (0.014; p=<0.001) | 0.068*** (0.019; p=<0.001) | 0.036* (0.020; p=0.070) | 0.018 (0.014; p=0.181) |
| gov | Black | 0.060*** (0.013; p=<0.001) | 0.074*** (0.014; p=<0.001) | 0.099*** (0.016; p=<0.001) | 0.050** (0.021; p=0.016) | 0.080*** (0.027; p=0.003) |  |  |
| gov | White - Black | -0.028 (0.017; p=0.115) | -0.029 (0.019; p=0.118) | -0.046** (0.021; p=0.030) | 0.020 (0.025; p=0.422) | -0.012 (0.033; p=0.709) |  |  |

## D3. The father's displacement at the son's 0-17, re-scored at the son's 25-34 and 35-44

19's child design, sons only; controls' pseudo event age 5. Each cell: displacement coefficient (s.e.; p) from one stacked regression in which every regressor (displaced, log pre-event family income, parental schooling, birth-year FE) is interacted with the band; clusters 1968 family.

| Outcome | Sample | displaced, 25-34 | displaced, 35-44 | change (35-44 minus 25-34) | sons (25-34 / 35-44) | displaced sons |
|---|---|---|---|---|---|---|
| ln own earnings | Pooled | -0.079*** (0.029; p=0.007) | -0.053 (0.043; p=0.218) | 0.026 (0.037; p=0.477) | 2,141 / 1,298 | 1,049 |
| ln own earnings | Black | -0.106* (0.061; p=0.084) | -0.124 (0.080; p=0.121) | -0.019 (0.080; p=0.814) | 612 / 354 | 338 |
| ln own earnings | White | -0.070** (0.034; p=0.038) | -0.023 (0.051; p=0.656) | 0.047 (0.042; p=0.262) | 1,529 / 944 | 711 |
| ln own earnings | White - Black change | | | 0.066 (0.090; p=0.465) | | |
| ln family income | Pooled | -0.065** (0.029; p=0.028) | -0.090** (0.043; p=0.037) | -0.025 (0.037; p=0.494) | 2,190 / 1,361 | 1,075 |
| ln family income | Black | -0.032 (0.058; p=0.583) | -0.084 (0.083; p=0.314) | -0.052 (0.088; p=0.558) | 634 / 377 | 350 |
| ln family income | White | -0.076** (0.035; p=0.030) | -0.087* (0.051; p=0.089) | -0.011 (0.040; p=0.777) | 1,556 / 984 | 725 |
| ln family income | White - Black change | | | 0.040 (0.097; p=0.678) | | |

