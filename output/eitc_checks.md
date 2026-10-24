# Are we sure the EITC has no effect on the IGE? (PI question)

Built by `129.EITCChecks.py` (2026-10-24); design in its docstring. Exposure in thousands of 2000 dollars, scaled to six years; s.e. clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**

Sons 3,017. Schedule exposure means: teen 13.83, pre (6-11) 9.51, post (19-24) 16.46; corr(teen, 101's exposure) 0.963; corr(teen, pre) 0.813, corr(teen, post) 0.880.

## 1. Placebo windows: within-son growth of ln earnings per $1,000 x (age-40)/10

| sample | specification | teen (13-18) | pre (6-11) | post (19-24) | sons |
|---|---|---|---|---|---|
| all sons | 101's exposure | 0.0274*** (0.0098; p=0.005) |  |  | 2,922 |
| all sons | teen alone | 0.0187** (0.0078; p=0.017) |  |  | 2,922 |
| all sons | pre alone |  | 0.0144 (0.0146; p=0.324) |  | 2,922 |
| all sons | post alone |  |  | 0.0056 (0.0056; p=0.317) | 2,922 |
| all sons | all three | 0.0341** (0.0137; p=0.013) | -0.0236 (0.0184; p=0.198) | -0.0092 (0.0083; p=0.268) | 2,922 |
| likely eligible | 101's exposure | 0.0446*** (0.0169; p=0.008) |  |  | 925 |
| likely eligible | teen alone | 0.0298* (0.0159; p=0.062) |  |  | 925 |
| likely eligible | pre alone |  | -0.0086 (0.0251; p=0.732) |  | 925 |
| likely eligible | post alone |  |  | 0.0073 (0.0112; p=0.515) | 925 |
| likely eligible | all three | 0.0873*** (0.0317; p=0.006) | -0.0856** (0.0369; p=0.020) | -0.0307* (0.0179; p=0.087) | 925 |

## 2. By parental-income tercile (within birth year)

| | bottom | middle | top | bottom - top |
|---|---|---|---|---|
| ln earnings at 25-29, per $1,000 | -0.0240*** (0.0090; p=0.007) | -0.0170** (0.0077; p=0.028) | -0.0127 (0.0079; p=0.107) | -0.0113* (0.0058; p=0.050) |
| ln earnings at 45-49, per $1,000 | -0.0789 (0.0639; p=0.216) | -0.0414 (0.0703; p=0.556) | -0.0431 (0.0678; p=0.526) | -0.0359 (0.0396; p=0.364) |
| within son x age, per $1,000 | 0.0200** (0.0096; p=0.036) | 0.0244** (0.0098; p=0.012) | 0.0323*** (0.0096; p=<0.001) | |

Rank-rank (son's earnings rank within birth year and band on parents' rank), per $1,000 of exposure:

| band | rank-rank at mean exposure | exposure x parents' rank | exposure x bottom tercile |
|---|---|---|---|
| 25-29 | 0.2657*** (0.0494; p=<0.001) | -0.0004 (0.0036; p=0.923) | -0.0004 (0.0015; p=0.810) |
| 35-39 | 0.3104*** (0.0648; p=<0.001) | 0.0028 (0.0050; p=0.570) | -0.0006 (0.0020; p=0.765) |
| 45-49 | 0.1393 (0.1524; p=0.361) | 0.0223 (0.0191; p=0.242) | 0.0016 (0.0054; p=0.771) |

## 3. Scaling and calibration

| parental-income tercile | window years in the credit's range | imputed credit per year (2000 $) | family income per year |
|---|---|---|---|
| bottom | 0.547 | 700 | 24,126 |
| middle | 0.148 | 165 | 52,903 |
| top | 0.029 | 33 | 108,862 |

The credit raises the family's log income by ln(1 + credit / income); its slope on ln parental income is -0.0257. If the credit passed on like other parental income with the IGE as the pass-through (0.28 at 25-29, 0.44 at 45-49; an upper bound, since not all of the IGE is causal), it would change the IGE by -0.0072 at 25-29 and -0.0113 at 45-49, against detectable effects of 0.08 and 0.14 per standard deviation of exposure (128).

