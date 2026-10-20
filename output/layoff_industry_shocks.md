# Layoffs the father did not choose: national employment shocks to his industry in the son's teens (Fable A1)

Built by `93.LayoffIndustryShocks.py` (2026-10-20); design in its docstring. Father-present PSID sons; shock = share of the seven years at the son's 12-18 in which national (CES) employment of the father's sector fell (decl), or its mean annual growth in log points x 100 (grow); sector FE and birth-year FE throughout; PSID weights; estimate (s.e.; p) clustered by sector x birth year; *** p<0.01, ** p<0.05, * p<0.1.

Sons: 3,145 (sector measured before the son's 14th wave-age: 85%); son-years 31,804; sector x birth-year clusters 632. Shock: decl mean 0.279 (s.d. 0.245), grow mean 1.23 (s.d. 1.85). Within sector and birth year the s.d. of decl is 0.143.

Sons by sector: Mining 27; Construction 344; Durable manufacturing 610; Nondurable manufacturing 326; Transportation, utilities, sanitary 306; Communications, broadcasting, telecom 50; Wholesale trade 159; Retail trade 266; Eating, drinking, accommodation 54; Finance, insurance, real estate 130; Business, repair, professional services 220; Personal, household, entertainment, membership 92; Health 89; Education and social services 194; Public administration 278

## 1. First stage: the father's teen spells on his industry's national decline (one row per son)

| outcome | decl (share of decline years) | grow (mean growth, x100) | mean of outcome |
|---|---|---|---|
| layoff share 13-19 | 0.030* (0.017; p=0.086) | -0.0030 (0.0026; p=0.249) | 0.046 |
| closure share 13-19 | -0.006 (0.014; p=0.676) | -0.0009 (0.0019; p=0.634) | 0.026 |
| unemployment share 13-19 | 0.080** (0.033; p=0.014) | -0.0045 (0.0054; p=0.404) | 0.115 |
| father's ln wage (window mean) | -0.016 (0.067; p=0.815) | 0.0165 (0.0112; p=0.140) | 3.012 |
| ln parental income | -0.019 (0.074; p=0.795) | 0.0167 (0.0112; p=0.135) | 11.138 |

Layoff first stage clustered by sector (15 clusters): 0.030 (0.019; p=0.111); F (sector x birth-year clusters) = 2.9.

## 2. Reduced form: the son's ln earnings on the shock, by band

| shock | controls | 25-29 | 45-49 | change 45-49 - 25-29 |
|---|---|---|---|---|
| decl | sector FE, birth-year FE | -0.100 (0.091; p=0.269) | 0.140 (0.206; p=0.495) | 0.241 (0.203; p=0.235) |
| decl | + ln parental income | -0.091 (0.089; p=0.305) | 0.187 (0.190; p=0.323) | 0.278 (0.191; p=0.145) |
| grow | sector FE, birth-year FE | -0.0042 (0.0144; p=0.770) | -0.0256 (0.0294; p=0.384) | -0.0214 (0.0302; p=0.479) |
| grow | + ln parental income | -0.0046 (0.0141; p=0.744) | -0.0232 (0.0268; p=0.387) | -0.0186 (0.0285; p=0.515) |

## 3. Within the same son: shock x (age-40)/10, son FE; placebo windows; 2SLS

Son FE, single-age dummies, sector x age, 5-year cohort x age (and lyp x age).

| spec | teen shock x age | pre (5-11) x age | post (19-25) x age | layoff share x age (2SLS) | N son-years / sons |
|---|---|---|---|---|---|
| decl, teen window alone | 0.115* (0.066; p=0.082) | | | 10.274 (26.803; p=0.701) | 29,442 / 3,094 |
| decl, three windows | 0.143** (0.063; p=0.024) | -0.058 (0.066; p=0.377) | 0.093 (0.061; p=0.126) | | 29,442 / 3,094 |
| grow, teen window alone | -0.0092 (0.0088; p=0.295) | | | -3.320 (5.254; p=0.527) | 29,442 / 3,094 |
| grow, three windows | -0.0115 (0.0089; p=0.197) | 0.0039 (0.0080; p=0.623) | -0.0089 (0.0089; p=0.321) | | 29,442 / 3,094 |

OLS within-son layoff share x age on the same sample and controls: -0.211** (0.096; p=0.028).

