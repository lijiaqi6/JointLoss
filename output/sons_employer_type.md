# Does the kind of employer carry the delayed cost of a father's teen layoff?

Built by `118.SonsEmployerType.py` (2026-10-24); design in its docstring. Coefficient of the father's teen layoff share (per unit share). *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**

## 1. The son's employer as an outcome

| outcome | mean | 25-29 | 45-49 | change | within son x age | sons |
|---|---|---|---|---|---|---|
| union-covered or member | 0.195 | -0.000 (0.072; p=0.995) | -0.111 (0.113; p=0.325) | -0.111 (0.122; p=0.362) | -0.008 (0.045; p=0.852) | 4,342 |
| works for government | 0.170 | -0.089 (0.062; p=0.151) | 0.142 (0.117; p=0.227) | 0.231** (0.118; p=0.050) | 0.009 (0.039; p=0.818) | 4,493 |
| self-employed | 0.138 | 0.097** (0.049; p=0.048) | 0.271** (0.121; p=0.026) | 0.174 (0.116; p=0.132) | 0.045 (0.042; p=0.292) | 4,648 |
| ln employed at his workplace (2003+) | 3.800 | 1.398* (0.768; p=0.069) | -2.697*** (0.875; p=0.002) | -4.095*** (1.113; p<0.001) | -0.354 (0.518; p=0.494) | 3,312 |

## 2. The within-son layoff slope with each held fixed (time-varying control)

| outcome | control | sample: as before | + control | control's own coefficient | son-years |
|---|---|---|---|---|---|
| ly | union-covered or member | -0.037 (0.095; p=0.695) | -0.036 (0.094; p=0.699) | 0.138*** (0.021; p<0.001) | 30,830 |
| ly | works for government | -0.097 (0.108; p=0.370) | -0.096 (0.107; p=0.371) | -0.057* (0.031; p=0.072) | 33,862 |
| ly | self-employed | -0.246** (0.106; p=0.020) | -0.237** (0.104; p=0.023) | -0.217*** (0.027; p<0.001) | 38,751 |
| ly | all three | -0.046 (0.100; p=0.642) | -0.042 (0.098; p=0.665) | | 29,630 |
| lw | union-covered or member | 0.004 (0.088; p=0.963) | 0.005 (0.087; p=0.954) | 0.124*** (0.019; p<0.001) | 30,830 |
| lw | works for government | -0.029 (0.089; p=0.750) | -0.028 (0.089; p=0.755) | -0.088*** (0.027; p=0.001) | 33,862 |
| lw | self-employed | -0.100 (0.081; p=0.218) | -0.093 (0.079; p=0.241) | -0.179*** (0.023; p<0.001) | 38,751 |
| lw | all three | -0.010 (0.094; p=0.911) | -0.006 (0.092; p=0.949) | | 29,630 |

## 3. Where the cost sits: employee years and self-employed years; workplace size (2003+)

| outcome | spec | layoff share x age | interaction / control | son-years / sons |
|---|---|---|---|---|
| ly | employee years only | -0.084 (0.103; p=0.413) | | 34,365 / 4,429 |
| ly | self-employed years only | -0.885*** (0.264; p<0.001) | | 4,386 / 1,317 |
| ly | all years, layoff x age x self-employed | -0.159 (0.101; p=0.115) | -0.427** (0.175; p=0.015) | 38,751 / 4,573 |
| ly | 2003+, as before -> + ln workplace size | -0.442*** (0.169; p=0.009) -> -0.426*** (0.164; p=0.009) | 0.036*** (0.005; p<0.001) | 15,068 / 3,260 |
| lw | employee years only | -0.004 (0.082; p=0.963) | | 34,365 / 4,429 |
| lw | self-employed years only | -0.609** (0.253; p=0.016) | | 4,386 / 1,317 |
| lw | all years, layoff x age x self-employed | -0.034 (0.079; p=0.666) | -0.348** (0.146; p=0.017) | 38,751 / 4,573 |
| lw | 2003+, as before -> + ln workplace size | -0.318** (0.137; p=0.020) -> -0.309** (0.136; p=0.023) | 0.020*** (0.004; p<0.001) | 15,068 / 3,260 |

