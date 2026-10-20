# Referee checks on the father's childhood layoff (simulated JPE round)

Built by `108.LayoffRefereeChecks.py` (2026-10-20); design in its docstring. *** p<0.01, ** p<0.05, * p<0.1.

## R2.1 The father before and after his first layoff in a son's teens (event study, father FE)

| event time (years) | -6 | -5 | -4 | -3 | -2 | 0 | +1 | +2 | +3 | +4 | +5 | +6 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| father's ln earnings | 0.106* (0.059; p=0.071) | 0.070 (0.057; p=0.218) | 0.085 (0.056; p=0.130) | 0.113** (0.050; p=0.023) | -0.005 (0.058; p=0.932) | -0.198*** (0.059; p<0.001) | -0.249*** (0.062; p<0.001) | -0.225*** (0.076; p=0.003) | -0.159*** (0.052; p=0.002) | -0.184** (0.089; p=0.039) | -0.166** (0.067; p=0.014) | -0.138** (0.060; p=0.021) |
| father employed | -0.016 (0.014; p=0.260) | -0.011 (0.012; p=0.328) | -0.003 (0.010; p=0.749) | -0.022 (0.017; p=0.189) | -0.021 (0.015; p=0.154) | 0.017** (0.008; p=0.040) | -0.073** (0.031; p=0.016) | -0.039 (0.027; p=0.150) | -0.049** (0.023; p=0.034) | -0.048 (0.030; p=0.117) | -0.039* (0.023; p=0.087) | -0.076*** (0.028; p=0.007) |

Pre-event coefficients (-6 ... -2) jointly zero, ln earnings: chi2(5) = 7.24, p = 0.203; treated fathers 212 of 1,535.

Pre-event coefficients (-6 ... -2) jointly zero, employed: chi2(5) = 5.46, p = 0.363; treated fathers 212 of 1,553.

## R2.2 Placebo: the same fathers' layoffs after the son is 26 (within son, ln earnings)

Sons whose father is observed as a head in >= 3 waves at their 27-35: 2,238 (father laid off then: 206).

| spec | teen layoff share x age | layoff share at 27-35 x age |
|---|---|---|
| teen share only | -0.120 (0.122; p=0.325) | |
| + share at 27-35 | -0.124 (0.122; p=0.307) | 0.063 (0.128; p=0.621) |

## R2.3 / R2.6 The closure bound and minimum detectable effects

Closure change 45-49 - 25-29 0.000 (s.e. 0.277); 95% interval [-0.543, 0.543]: the largest closure cost it allows is 0.543, 59% of the layoff change (-0.914).
Minimum detectable effect (80% power, 5% two-sided) for the layoff change: 0.683 (s.e. 0.244); for the closure change: 0.776; for the within-son layoff slope: 0.288 (s.e. 0.103).

## R1 The layoff profile in ranks (son's earnings percentile within age x year)

| element | 25-29 | 45-49 | change |
|---|---|---|---|
| f_sh_layoff | 2.244 (4.827; p=0.642) | -19.920** (8.081; p=0.014) | -22.163*** (7.483; p=0.003) |
| f_sh_close | 2.902 (6.716; p=0.666) | 10.383 (10.816; p=0.337) | 7.481 (10.310; p=0.468) |

