# Business income of self-employed sons (committee memo Z3)

Built by `123.SonsBusinessIncome.py` (2026-10-24); design in its docstring. 75's son-years with a valid wage, son as head, 1976+. *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**

## 1. Self-employment and business income

| band | self-employed: tercile 1 | tercile 2 | tercile 3 | business labor share of earnings, self-employed years | asset part > 0, self-employed years | son-years |
|---|---|---|---|---|---|---|
| 25-29 | 0.068 | 0.085 | 0.098 | 0.266 | 0.342 | 10,655 |
| 30-34 | 0.102 | 0.111 | 0.119 | 0.258 | 0.342 | 10,000 |
| 35-39 | 0.115 | 0.135 | 0.148 | 0.313 | 0.391 | 7,379 |
| 40-44 | 0.122 | 0.136 | 0.153 | 0.287 | 0.376 | 4,923 |
| 45-49 | 0.151 | 0.149 | 0.178 | 0.296 | 0.374 | 3,158 |
| 50-55 | 0.120 | 0.140 | 0.173 | 0.250 | 0.314 | 2,636 |

Business labor share of earnings in employee years: 0.005.

## 2. The IGE by band: all son-years, employee years, earnings + business asset income

| sample / outcome | 25-29 | 45-49 | change | sons |
|---|---|---|---|---|
| all son-years, ln earnings | 0.276*** (0.022; p<0.001) | 0.443*** (0.048; p<0.001) | 0.167*** (0.048; p<0.001) | 4,284 |
| all son-years with a self-employment code | 0.255*** (0.021; p<0.001) | 0.441*** (0.048; p<0.001) | 0.186*** (0.048; p<0.001) | 4,198 |
| employee years only, ln earnings | 0.265*** (0.020; p<0.001) | 0.441*** (0.047; p<0.001) | 0.176*** (0.047; p<0.001) | 4,010 |
| all son-years, ln(earnings + business asset income) | 0.280*** (0.022; p<0.001) | 0.436*** (0.047; p<0.001) | 0.156*** (0.047; p<0.001) | 4,284 |

## 3. The within-son layoff slope in self-employed and employee years

| sample | outcome | employee years | self-employed years | all years: layoff x age x self-employed | son-years (SE) / sons (SE) |
|---|---|---|---|---|---|
| all sons | ln earnings | -0.084 (0.103; p=0.413) | -0.885*** (0.264; p<0.001) | -0.427** (0.175; p=0.015) | 4,386 / 1,317 |
| all sons | ln(earnings + business asset income) | -0.081 (0.103; p=0.431) | -0.812*** (0.256; p=0.002) | -0.315 (0.194; p=0.105) | 4,386 / 1,317 |
| all sons | ln hourly wage | -0.004 (0.082; p=0.963) | -0.609** (0.253; p=0.016) | -0.348** (0.146; p=0.017) | 4,386 / 1,317 |
| all sons | ln hours | -0.081 (0.051; p=0.115) | -0.275 (0.255; p=0.280) | -0.079 (0.168; p=0.638) | 4,386 / 1,317 |
| all sons | asinh business labor income | 0.025 (0.039; p=0.517) | 0.079 (0.468; p=0.866) | 0.322 (0.299; p=0.281) | 4,386 / 1,317 |
| all sons | asinh other labor income | -0.074 (0.105; p=0.482) | -0.790 (0.607; p=0.193) | -0.804** (0.353; p=0.023) | 4,386 / 1,317 |
| without self-employed fathers | ln earnings | -0.174* (0.096; p=0.069) | -1.024*** (0.293; p<0.001) | -0.331* (0.179; p=0.065) | 3,357 / 1,117 |
| without self-employed fathers | ln(earnings + business asset income) | -0.171* (0.097; p=0.077) | -1.009*** (0.264; p<0.001) | -0.249 (0.194; p=0.200) | 3,357 / 1,117 |
| without self-employed fathers | ln hourly wage | -0.061 (0.072; p=0.397) | -0.733** (0.304; p=0.016) | -0.276* (0.143; p=0.055) | 3,357 / 1,117 |
| without self-employed fathers | ln hours | -0.113* (0.059; p=0.056) | -0.291 (0.238; p=0.222) | -0.055 (0.171; p=0.747) | 3,357 / 1,117 |
| without self-employed fathers | asinh business labor income | 0.021 (0.046; p=0.647) | -0.285 (0.544; p=0.600) | 0.165 (0.305; p=0.587) | 3,357 / 1,117 |
| without self-employed fathers | asinh other labor income | -0.162* (0.098; p=0.098) | -0.523 (0.727; p=0.472) | -0.569 (0.363; p=0.117) | 3,357 / 1,117 |

