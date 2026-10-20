# Why do wives leave employment? (IGE/63.WifeExitWhy.py, 2026-10-19)

Married wives 25-59, husband employed. CPS 1994-2023 and SIPP 2003-2016: persistent monthly exit (employed t-1, t; not employed t+1, t+2). PSID 1968-1996 (annual years): hours > 0 in t, 0 in t+1. Regression cells: coefficient in percentage points, stars, (cluster s.e.; p). *** p<0.01, ** p<0.05, * p<0.1. Hazard cells: rate (s.e.). Associations, not causal effects. Aggregates only.

## CPS: steady state (vii)

*wives 25-59, husband employed*

| | employment share (%) | persistent monthly entry (%) | persistent monthly exit (%) | N |
|---|---|---|---|---|
| all | 71.68 | 3.15 | 0.97 | 5590356 |
| race: Black |  | 3.97 |  | 12465 |
| race: White |  | 3.17 |  | 232433 |

## CPS: exit hazard by cell, share of wife-months and of exits (i)

*persistent exits*

| | share of exits (%) | N |
|---|---|---|
| destination at t+1: out of the labor force | 93.26 | 6912 |
| destination at t+1: unemployed: job leaver | 4.57 | 342 |
| destination at t+1: unemployed: re-entrant | 2.14 | 173 |
| destination at t+1: unemployed: new entrant | 0.03 | 2 |

*wives 25-59, husband employed (persistent exit)*

| | exit hazard (%) | share of wife-months (%) | share of exits (%) | N |
|---|---|---|---|---|
| all | 0.97 |  |  | 794275 |
| youngest child: 6-12 | 1.04 (0.03) | 21.44 | 22.98 | 169980 |
| youngest child: none <18 | 0.77 (0.02) | 41.86 | 33.48 | 334978 |
| youngest child: 3-5 | 1.30 (0.05) | 10.23 | 13.80 | 79298 |
| youngest child: 13-17 | 0.81 (0.03) | 14.19 | 11.96 | 114616 |
| youngest child: 1-2 | 1.26 (0.05) | 8.44 | 11.06 | 65495 |
| youngest child: 0 | 1.69 (0.09) | 3.83 | 6.71 | 29908 |
| wife's age: 40-44 | 0.88 (0.03) | 18.23 | 16.52 | 145934 |
| wife's age: 30-34 | 1.20 (0.04) | 14.52 | 18.06 | 112449 |
| wife's age: 25-29 | 1.35 (0.05) | 9.54 | 13.29 | 71548 |
| wife's age: 45-49 | 0.76 (0.03) | 17.76 | 13.96 | 142900 |
| wife's age: 50-54 | 0.78 (0.03) | 14.65 | 11.86 | 119473 |
| wife's age: 55-59 | 1.00 (0.04) | 8.32 | 8.64 | 67598 |
| wife's age: 35-39 | 1.01 (0.03) | 16.98 | 17.67 | 134373 |
| race (husband): Black | 0.82 (0.05) | 7.34 | 6.21 | 46138 |
| race (husband): White | 0.97 (0.01) | 85.98 | 86.31 | 699496 |
| race (husband): Other | 1.08 (0.05) | 6.68 | 7.48 | 48641 |
| wife's education: BA+ | 0.73 (0.02) | 42.66 | 32.43 | 327384 |
| wife's education: high school | 1.12 (0.03) | 24.63 | 28.53 | 201952 |
| wife's education: some college | 0.96 (0.02) | 28.13 | 28.02 | 231364 |
| wife's education: < high school | 2.32 (0.09) | 4.58 | 11.01 | 33575 |
| class of worker: self-employed | 1.77 (0.05) | 9.82 | 17.97 | 82625 |
| class of worker: private | 0.94 (0.01) | 69.60 | 67.73 | 543494 |
| class of worker: government | 0.64 (0.02) | 20.43 | 13.52 | 166967 |
| class of worker: unknown | 5.33 (0.75) | 0.14 | 0.78 | 1189 |
| period: 1994-2000 | 1.05 (0.03) | 22.86 | 24.88 | 195081 |
| period: 2001-07 | 1.05 (0.03) | 24.32 | 26.35 | 215143 |
| period: 2008-13 | 0.88 (0.03) | 21.06 | 19.10 | 172708 |
| period: 2014-19 | 0.92 (0.03) | 20.21 | 19.32 | 145906 |
| period: 2020-21 | 0.92 (0.06) | 5.82 | 5.56 | 34257 |
| period: 2022-23 | 0.80 (0.06) | 5.74 | 4.78 | 31180 |

## CPS: LPM of the exit on all covariates jointly (ii)

*wives 25-59, husband employed (state x year-month FE)*

| | persistent exit (pp) | N |
|---|---|---|
| youngest child: 0 | 0.95*** (0.09; p=<0.001) | 794275 |
| youngest child: 1-2 | 0.51*** (0.06; p=<0.001) | 794275 |
| youngest child: 13-17 | 0.13*** (0.04; p=<0.001) | 794275 |
| youngest child: 3-5 | 0.56*** (0.05; p=<0.001) | 794275 |
| youngest child: 6-12 | 0.35*** (0.04; p=<0.001) | 794275 |
| wife's age: 25-29 | 0.41*** (0.06; p=<0.001) | 794275 |
| wife's age: 30-34 | 0.19*** (0.05; p=<0.001) | 794275 |
| wife's age: 40-44 | -0.03 (0.04; p=0.502) | 794275 |
| wife's age: 45-49 | -0.03 (0.05; p=0.474) | 794275 |
| wife's age: 50-54 | 0.08 (0.05; p=0.118) | 794275 |
| wife's age: 55-59 | 0.33*** (0.06; p=<0.001) | 794275 |
| race (husband): Black | -0.15*** (0.05; p=0.002) | 794275 |
| race (husband): Other | 0.02 (0.06; p=0.725) | 794275 |
| wife's education: < high school | 0.90*** (0.10; p=<0.001) | 794275 |
| wife's education: BA+ | -0.44*** (0.04; p=<0.001) | 794275 |
| wife's education: some college | -0.19*** (0.04; p=<0.001) | 794275 |
| class of worker: government | -0.16*** (0.03; p=<0.001) | 794275 |
| class of worker: self-employed | 0.85*** (0.06; p=<0.001) | 794275 |
| class of worker: unknown | 4.26*** (0.77; p=<0.001) | 794275 |
| husband's education: < high school | 0.41*** (0.08; p=<0.001) | 794275 |
| husband's education: BA+ | 0.08** (0.04; p=0.022) | 794275 |
| husband's education: some college | -0.00 (0.04; p=0.931) | 794275 |

Notes: clusters=559130; mean=0.966

## CPS: spell length / return to work (iv)

*exiters*

| | employed at t+12 (11 months after the exit month) (%) | N |
|---|---|---|
| all | 47.45 (1.09) | 2659 |
| youngest child: 0 | 41.82 (4.15) | 185 |
| youngest child: 1-2 | 38.14 (3.32) | 277 |
| youngest child: 3-5 | 50.09 (2.88) | 381 |
| youngest child: 6-12 | 52.53 (2.24) | 631 |
| youngest child: 13-17 | 52.96 (2.98) | 355 |
| youngest child: none <18 | 44.10 (1.95) | 830 |

*stayers (no exit at t+1)*

| | employed at t+12 (11 months after the exit month) (%) | N |
|---|---|---|
| all | 93.65 (0.05) | 294536 |

*exiters with a t+12 link (period FE)*

| | employed at t+12 (pp) | N |
|---|---|---|
| youngest child: 0 | -3.69 (5.19; p=0.477) | 2659 |
| youngest child: 1-2 | -7.29 (4.47; p=0.103) | 2659 |
| youngest child: 13-17 | 7.50** (3.72; p=0.044) | 2659 |
| youngest child: 3-5 | 3.80 (4.10; p=0.355) | 2659 |
| youngest child: 6-12 | 6.29* (3.45; p=0.068) | 2659 |
| wife's age: 25-29 | -3.08 (4.33; p=0.477) | 2659 |
| wife's age: 30-34 | -6.39* (3.70; p=0.084) | 2659 |
| wife's age: 40-44 | -1.17 (3.75; p=0.755) | 2659 |
| wife's age: 45-49 | -6.32 (3.97; p=0.112) | 2659 |
| wife's age: 50-54 | -1.88 (4.55; p=0.679) | 2659 |
| wife's age: 55-59 | -12.39** (5.12; p=0.015) | 2659 |
| race (husband): Black | 4.14 (5.08; p=0.415) | 2659 |
| race (husband): Other | -8.77** (4.26; p=0.039) | 2659 |

Notes: clusters=2659; mean=47.446

## SIPP: steady state (vii)

*wives 25-59, husband employed*

| | persistent monthly exit, all reasons (%) | persistent monthly exit, no involuntary separation (%) | employment share (%) | persistent monthly entry (%) | N |
|---|---|---|---|---|---|
| all | 0.91 | 0.68 | 71.19 | 2.45 | 1353202 |

## SIPP: exit hazard by cell, share of wife-months and of exits (i)

*wives 25-59, husband employed (persistent exit)*

| | exit hazard (%) | share of wife-months (%) | share of exits (%) | N |
|---|---|---|---|---|
| all | 0.91 |  |  | 837420 |
| youngest child: 6-12 | 0.89 (0.03) | 21.30 | 21.05 | 180283 |
| youngest child: 3-5 | 1.18 (0.04) | 10.66 | 13.87 | 87443 |
| youngest child: 13-17 | 0.73 (0.03) | 13.57 | 10.95 | 119919 |
| youngest child: none <18 | 0.79 (0.02) | 41.43 | 36.07 | 347739 |
| youngest child: 0 | 1.37 (0.08) | 4.00 | 6.06 | 31098 |
| youngest child: 1-2 | 1.20 (0.05) | 9.04 | 12.00 | 70938 |
| child aged 0 in t+1..t+9: no | 0.85 (0.01) | 93.43 | 87.44 | 786186 |
| child aged 0 in t+1..t+9: yes | 1.73 (0.07) | 6.57 | 12.56 | 51234 |
| wife's age: 45-49 | 0.75 (0.03) | 17.39 | 14.49 | 149095 |
| wife's age: 30-34 | 1.20 (0.04) | 14.50 | 19.28 | 117469 |
| wife's age: 50-54 | 0.65 (0.03) | 15.32 | 10.96 | 132478 |
| wife's age: 55-59 | 0.80 (0.04) | 9.17 | 8.11 | 77438 |
| wife's age: 25-29 | 1.42 (0.05) | 10.24 | 16.10 | 78306 |
| wife's age: 35-39 | 0.91 (0.03) | 15.95 | 15.97 | 134499 |
| wife's age: 40-44 | 0.78 (0.03) | 17.43 | 15.09 | 148135 |
| race (husband): White | 0.90 (0.01) | 84.50 | 83.71 | 714268 |
| race (husband): Other | 1.00 (0.05) | 7.30 | 8.09 | 58101 |
| race (husband): Black | 0.90 (0.05) | 8.20 | 8.20 | 65051 |
| wife's education: some college | 0.93 (0.02) | 33.21 | 34.16 | 289482 |
| wife's education: high school | 1.10 (0.03) | 19.54 | 23.79 | 173877 |
| wife's education: < high school | 1.89 (0.08) | 4.40 | 9.20 | 36233 |
| wife's education: BA+ | 0.69 (0.02) | 42.85 | 32.85 | 337828 |
| usual hours (all jobs): 35+ | 0.57 (0.01) | 64.87 | 41.07 | 540436 |
| usual hours (all jobs): 20-34 | 1.22 (0.04) | 13.66 | 18.46 | 114908 |
| usual hours (all jobs): unknown | 1.39 (0.04) | 16.00 | 24.55 | 136516 |
| usual hours (all jobs): < 20 | 2.64 (0.09) | 5.46 | 15.92 | 45560 |
| job tenure (months): 36+ | 0.54 (0.01) | 56.39 | 33.63 | 489595 |
| job tenure (months): 12-35 | 1.10 (0.03) | 17.84 | 21.77 | 144897 |
| job tenure (months): 6-11 | 1.60 (0.06) | 7.25 | 12.78 | 56136 |
| job tenure (months): 0-5 | 2.06 (0.07) | 8.06 | 18.33 | 62609 |
| job tenure (months): unknown | 1.17 (0.04) | 10.46 | 13.49 | 84183 |
| husband's job change t-2..t+1: no | 0.88 (0.01) | 96.98 | 94.35 | 813157 |
| husband's job change t-2..t+1: yes | 1.69 (0.10) | 3.02 | 5.65 | 24263 |
| previous persistent exit in panel: no | 0.82 (0.01) | 93.71 | 84.62 | 791136 |
| previous persistent exit in panel: yes | 2.21 (0.08) | 6.29 | 15.38 | 46284 |
| panel: 2004 | 0.99 (0.02) | 32.18 | 35.27 | 306290 |
| panel: 2008 | 0.93 (0.02) | 38.85 | 40.13 | 375766 |
| panel: 2014 | 0.77 (0.03) | 28.98 | 24.60 | 155364 |

## SIPP: LPM of the exit on all covariates jointly (ii)

*wives 25-59, husband employed (panel x rotation x month FE)*

| | persistent exit (pp) | persistent exit, no involuntary separation (pp) | N |
|---|---|---|---|
| youngest child: 0 | -0.51*** (0.12; p=<0.001) | -0.42*** (0.11; p=<0.001) | 837349 |
| youngest child: 1-2 | 0.11* (0.06; p=0.070) | 0.07 (0.05; p=0.142) | 837349 |
| youngest child: 13-17 | -0.03 (0.04; p=0.378) | -0.01 (0.03; p=0.697) | 837349 |
| youngest child: 3-5 | 0.15*** (0.06; p=0.006) | 0.12** (0.05; p=0.011) | 837349 |
| youngest child: 6-12 | 0.01 (0.04; p=0.848) | 0.01 (0.03; p=0.754) | 837349 |
| child aged 0 in t+1..t+9: yes | 1.04*** (0.11; p=<0.001) | 0.97*** (0.10; p=<0.001) | 837349 |
| wife's age: 25-29 | 0.33*** (0.06; p=<0.001) | 0.32*** (0.05; p=<0.001) | 837349 |
| wife's age: 30-34 | 0.21*** (0.05; p=<0.001) | 0.18*** (0.04; p=<0.001) | 837349 |
| wife's age: 40-44 | -0.03 (0.04; p=0.505) | -0.01 (0.04; p=0.881) | 837349 |
| wife's age: 45-49 | 0.01 (0.05; p=0.760) | 0.01 (0.04; p=0.884) | 837349 |
| wife's age: 50-54 | -0.06 (0.05; p=0.186) | -0.06 (0.04; p=0.119) | 837349 |
| wife's age: 55-59 | 0.07 (0.06; p=0.214) | 0.07 (0.05; p=0.159) | 837349 |
| race (husband): Black | 0.11** (0.05; p=0.017) | 0.09** (0.04; p=0.021) | 837349 |
| race (husband): Other | 0.13** (0.05; p=0.013) | 0.11** (0.05; p=0.016) | 837349 |
| wife's education: < high school | 0.65*** (0.10; p=<0.001) | 0.45*** (0.08; p=<0.001) | 837349 |
| wife's education: BA+ | -0.45*** (0.04; p=<0.001) | -0.28*** (0.03; p=<0.001) | 837349 |
| wife's education: some college | -0.22*** (0.04; p=<0.001) | -0.13*** (0.03; p=<0.001) | 837349 |
| usual hours (all jobs): 20-34 | 0.53*** (0.04; p=<0.001) | 0.40*** (0.03; p=<0.001) | 837349 |
| usual hours (all jobs): < 20 | 1.85*** (0.10; p=<0.001) | 1.39*** (0.08; p=<0.001) | 837349 |
| usual hours (all jobs): unknown | 1.09*** (0.07; p=<0.001) | 0.97*** (0.06; p=<0.001) | 837349 |
| job tenure (months): 0-5 | 1.33*** (0.07; p=<0.001) | 0.77*** (0.05; p=<0.001) | 837349 |
| job tenure (months): 12-35 | 0.42*** (0.04; p=<0.001) | 0.28*** (0.03; p=<0.001) | 837349 |
| job tenure (months): 6-11 | 0.91*** (0.07; p=<0.001) | 0.59*** (0.06; p=<0.001) | 837349 |
| job tenure (months): unknown | -0.21** (0.08; p=0.013) | -0.06 (0.08; p=0.415) | 837349 |
| husband's job change t-2..t+1: yes | 0.70*** (0.10; p=<0.001) | 0.57*** (0.09; p=<0.001) | 837349 |

Notes: clusters=34645; mean=0.905; clusters=34645; mean=0.677

## SIPP: stated reason for the persistent exits, grouped (iii)

*persistent exits: all*

| | persistent exits: all | N |
|---|---|---|
| unsatisfactory arrangements / other quit | 17.62 (0.52) | 1327 |
| no job end recorded | 34.46 (0.64) | 2807 |
| childcare / family | 11.49 (0.43) | 865 |
| involuntary | 25.15 (0.59) | 1970 |
| quit to another job | 4.25 (0.27) | 268 |
| own illness / injury | 3.84 (0.26) | 298 |
| school | 1.69 (0.17) | 127 |
| retirement | 1.51 (0.17) | 119 |

*persistent exits: race: Black*

| | persistent exits: race: Black | N |
|---|---|---|
| own illness / injury | 5.22 (1.10) | 37 |
| involuntary | 26.21 (2.17) | 170 |
| quit to another job | 4.93 (1.07) | 23 |
| no job end recorded | 35.51 (2.37) | 240 |
| retirement | 1.73 (0.64) | 13 |
| unsatisfactory arrangements / other quit | 16.07 (1.82) | 90 |
| childcare / family | 9.18 (1.43) | 50 |
| school | 1.16 (0.53) | 9 |

*persistent exits: race: White*

| | persistent exits: race: White | N |
|---|---|---|
| unsatisfactory arrangements / other quit | 17.68 (0.56) | 1133 |
| no job end recorded | 34.09 (0.70) | 2322 |
| childcare / family | 11.80 (0.47) | 744 |
| involuntary | 25.18 (0.64) | 1638 |
| quit to another job | 4.34 (0.30) | 233 |
| own illness / injury | 3.63 (0.28) | 238 |
| retirement | 1.60 (0.18) | 103 |
| school | 1.69 (0.19) | 108 |

*persistent exits: youngest child 0-2*

| | persistent exits: youngest child 0-2 | N |
|---|---|---|
| unsatisfactory arrangements / other quit | 17.10 (1.22) | 196 |
| childcare / family | 22.65 (1.36) | 313 |
| no job end recorded | 31.99 (1.51) | 484 |
| involuntary | 20.53 (1.31) | 282 |
| quit to another job | 4.68 (0.68) | 47 |
| school | 1.03 (0.33) | 16 |
| own illness / injury | 1.75 (0.43) | 18 |
| retirement | 0.27 (0.17) | 3 |

*persistent exits: youngest child 3-5*

| | persistent exits: youngest child 3-5 | N |
|---|---|---|
| unsatisfactory arrangements / other quit | 17.47 (1.42) | 180 |
| involuntary | 24.57 (1.61) | 263 |
| childcare / family | 15.13 (1.34) | 153 |
| no job end recorded | 32.74 (1.76) | 361 |
| own illness / injury | 3.43 (0.68) | 34 |
| school | 2.40 (0.57) | 25 |
| quit to another job | 4.20 (0.75) | 34 |
| retirement | 0.06 (0.09) | 1 |

*persistent exits: youngest child 6-17*

| | persistent exits: youngest child 6-17 | N |
|---|---|---|
| no job end recorded | 36.93 (1.13) | 961 |
| unsatisfactory arrangements / other quit | 18.44 (0.91) | 453 |
| quit to another job | 4.14 (0.47) | 89 |
| involuntary | 26.20 (1.03) | 693 |
| school | 1.48 (0.28) | 39 |
| own illness / injury | 3.55 (0.43) | 102 |
| childcare / family | 8.73 (0.66) | 215 |
| retirement | 0.54 (0.17) | 15 |

*persistent exits: no child <18*

| | persistent exits: no child <18 | N |
|---|---|---|
| unsatisfactory arrangements / other quit | 17.22 (0.85) | 498 |
| no job end recorded | 34.16 (1.07) | 1001 |
| involuntary | 26.74 (1.00) | 732 |
| childcare / family | 6.96 (0.57) | 184 |
| own illness / injury | 5.29 (0.50) | 144 |
| retirement | 3.54 (0.42) | 100 |
| quit to another job | 4.15 (0.45) | 98 |
| school | 1.95 (0.31) | 47 |

*persistent exits: child aged 0 in t+1..t+9*

| | persistent exits: child aged 0 in t+1..t+9 | N |
|---|---|---|
| unsatisfactory arrangements / other quit | 20.14 (1.58) | 164 |
| childcare / family | 30.97 (1.83) | 286 |
| no job end recorded | 28.67 (1.79) | 280 |
| involuntary | 14.19 (1.38) | 134 |
| own illness / injury | 1.75 (0.52) | 20 |
| quit to another job | 3.38 (0.71) | 20 |
| school | 0.73 (0.34) | 7 |
| retirement | 0.17 (0.16) | 2 |

*persistent exits: wife 55-59*

| | persistent exits: wife 55-59 | N |
|---|---|---|
| no job end recorded | 43.14 (2.30) | 274 |
| unsatisfactory arrangements / other quit | 12.07 (1.51) | 83 |
| retirement | 11.10 (1.46) | 71 |
| own illness / injury | 4.08 (0.92) | 30 |
| school | 0.30 (0.25) | 2 |
| involuntary | 25.22 (2.01) | 151 |
| childcare / family | 2.09 (0.66) | 14 |
| quit to another job | 2.00 (0.65) | 10 |

## SIPP: stated reason, detailed (iii)

*persistent exits: all*

| | persistent exits: all | N |
|---|---|---|
| quit for another reason / other personal | 13.44 (0.46) | 1004 |
| no job end recorded in t-1..t+2 | 34.46 (0.64) | 2807 |
| childcare problems | 2.61 (0.22) | 199 |
| layoff / slack work / position abolished | 12.00 (0.44) | 1016 |
| other family / personal obligations | 8.88 (0.39) | 666 |
| quit to take another job | 4.25 (0.27) | 268 |
| own illness / injury | 3.84 (0.26) | 298 |
| unsatisfactory work arrangements | 4.19 (0.27) | 323 |
| temporary job ended | 6.56 (0.34) | 477 |
| discharged / fired | 3.33 (0.24) | 267 |
| school / training | 1.69 (0.17) | 127 |
| plant closed / employer bankrupt or sold | 1.73 (0.18) | 133 |
| retirement / old age | 1.51 (0.17) | 119 |
| other involuntary (2014) | 1.52 (0.17) | 77 |

*persistent exits: race: Black*

| | persistent exits: race: Black | N |
|---|---|---|
| own illness / injury | 5.22 (1.10) | 37 |
| discharged / fired | 4.40 (1.01) | 28 |
| quit to take another job | 4.93 (1.07) | 23 |
| no job end recorded in t-1..t+2 | 35.51 (2.37) | 240 |
| layoff / slack work / position abolished | 13.79 (1.70) | 90 |
| retirement / old age | 1.73 (0.64) | 13 |
| quit for another reason / other personal | 15.12 (1.77) | 83 |
| other family / personal obligations | 6.75 (1.24) | 38 |
| temporary job ended | 4.83 (1.06) | 32 |
| school / training | 1.16 (0.53) | 9 |
| unsatisfactory work arrangements | 0.95 (0.48) | 7 |
| plant closed / employer bankrupt or sold | 1.47 (0.59) | 10 |
| childcare problems | 2.43 (0.76) | 12 |
| other involuntary (2014) | 1.72 (0.64) | 10 |

*persistent exits: race: White*

| | persistent exits: race: White | N |
|---|---|---|
| quit for another reason / other personal | 13.19 (0.50) | 842 |
| no job end recorded in t-1..t+2 | 34.09 (0.70) | 2322 |
| childcare problems | 2.64 (0.24) | 168 |
| layoff / slack work / position abolished | 11.78 (0.47) | 830 |
| other family / personal obligations | 9.16 (0.42) | 576 |
| quit to take another job | 4.34 (0.30) | 233 |
| unsatisfactory work arrangements | 4.49 (0.30) | 291 |
| temporary job ended | 6.83 (0.37) | 413 |
| discharged / fired | 3.38 (0.27) | 225 |
| own illness / injury | 3.63 (0.28) | 238 |
| plant closed / employer bankrupt or sold | 1.73 (0.19) | 111 |
| retirement / old age | 1.60 (0.18) | 103 |
| school / training | 1.69 (0.19) | 108 |
| other involuntary (2014) | 1.46 (0.18) | 59 |

*persistent exits: youngest child 0-2*

| | persistent exits: youngest child 0-2 | N |
|---|---|---|
| quit for another reason / other personal | 14.36 (1.14) | 165 |
| childcare problems | 7.41 (0.85) | 101 |
| no job end recorded in t-1..t+2 | 31.99 (1.51) | 484 |
| other family / personal obligations | 15.23 (1.16) | 212 |
| discharged / fired | 2.33 (0.49) | 32 |
| quit to take another job | 4.68 (0.68) | 47 |
| layoff / slack work / position abolished | 8.97 (0.93) | 133 |
| temporary job ended | 7.44 (0.85) | 90 |
| unsatisfactory work arrangements | 2.74 (0.53) | 31 |
| school / training | 1.03 (0.33) | 16 |
| own illness / injury | 1.75 (0.43) | 18 |
| retirement / old age | 0.27 (0.17) | 3 |
| plant closed / employer bankrupt or sold | 0.99 (0.32) | 13 |
| other involuntary (2014) | 0.79 (0.29) | 14 |

*persistent exits: youngest child 3-5*

| | persistent exits: youngest child 3-5 | N |
|---|---|---|
| quit for another reason / other personal | 12.97 (1.26) | 136 |
| layoff / slack work / position abolished | 9.20 (1.08) | 112 |
| discharged / fired | 3.98 (0.73) | 47 |
| other family / personal obligations | 10.46 (1.15) | 101 |
| no job end recorded in t-1..t+2 | 32.74 (1.76) | 361 |
| childcare problems | 4.67 (0.79) | 52 |
| temporary job ended | 8.16 (1.03) | 77 |
| own illness / injury | 3.43 (0.68) | 34 |
| school / training | 2.40 (0.57) | 25 |
| quit to take another job | 4.20 (0.75) | 34 |
| unsatisfactory work arrangements | 4.50 (0.78) | 44 |
| plant closed / employer bankrupt or sold | 2.13 (0.54) | 19 |
| retirement / old age | 0.06 (0.09) | 1 |
| other involuntary (2014) | 1.10 (0.39) | 8 |

*persistent exits: youngest child 6-17*

| | persistent exits: youngest child 6-17 | N |
|---|---|---|
| no job end recorded in t-1..t+2 | 36.93 (1.13) | 961 |
| quit for another reason / other personal | 13.78 (0.81) | 335 |
| quit to take another job | 4.14 (0.47) | 89 |
| layoff / slack work / position abolished | 12.99 (0.79) | 369 |
| unsatisfactory work arrangements | 4.66 (0.49) | 118 |
| temporary job ended | 6.53 (0.58) | 164 |
| school / training | 1.48 (0.28) | 39 |
| own illness / injury | 3.55 (0.43) | 102 |
| other family / personal obligations | 7.54 (0.62) | 187 |
| discharged / fired | 3.59 (0.44) | 91 |
| childcare problems | 1.19 (0.25) | 28 |
| plant closed / employer bankrupt or sold | 1.74 (0.31) | 44 |
| retirement / old age | 0.54 (0.17) | 15 |
| other involuntary (2014) | 1.34 (0.27) | 25 |

*persistent exits: no child <18*

| | persistent exits: no child <18 | N |
|---|---|---|
| quit for another reason / other personal | 12.85 (0.75) | 368 |
| no job end recorded in t-1..t+2 | 34.16 (1.07) | 1001 |
| layoff / slack work / position abolished | 13.71 (0.78) | 402 |
| other family / personal obligations | 6.29 (0.55) | 166 |
| own illness / injury | 5.29 (0.50) | 144 |
| unsatisfactory work arrangements | 4.37 (0.46) | 130 |
| plant closed / employer bankrupt or sold | 1.94 (0.31) | 57 |
| retirement / old age | 3.54 (0.42) | 100 |
| childcare problems | 0.67 (0.18) | 18 |
| quit to take another job | 4.15 (0.45) | 98 |
| school / training | 1.95 (0.31) | 47 |
| temporary job ended | 5.54 (0.52) | 146 |
| discharged / fired | 3.34 (0.41) | 97 |
| other involuntary (2014) | 2.21 (0.33) | 30 |

*persistent exits: child aged 0 in t+1..t+9*

| | persistent exits: child aged 0 in t+1..t+9 | N |
|---|---|---|
| quit for another reason / other personal | 17.98 (1.52) | 148 |
| other family / personal obligations | 23.66 (1.68) | 215 |
| no job end recorded in t-1..t+2 | 28.67 (1.79) | 280 |
| discharged / fired | 2.19 (0.58) | 17 |
| childcare problems | 7.31 (1.03) | 71 |
| own illness / injury | 1.75 (0.52) | 20 |
| layoff / slack work / position abolished | 6.45 (0.97) | 72 |
| temporary job ended | 4.22 (0.79) | 34 |
| quit to take another job | 3.38 (0.71) | 20 |
| plant closed / employer bankrupt or sold | 0.85 (0.36) | 7 |
| unsatisfactory work arrangements | 2.15 (0.57) | 16 |
| school / training | 0.73 (0.34) | 7 |
| retirement / old age | 0.17 (0.16) | 2 |
| other involuntary (2014) | 0.49 (0.27) | 4 |

*persistent exits: wife 55-59*

| | persistent exits: wife 55-59 | N |
|---|---|---|
| no job end recorded in t-1..t+2 | 43.14 (2.30) | 274 |
| quit for another reason / other personal | 8.68 (1.30) | 61 |
| retirement / old age | 11.10 (1.46) | 71 |
| unsatisfactory work arrangements | 3.39 (0.84) | 22 |
| own illness / injury | 4.08 (0.92) | 30 |
| school / training | 0.30 (0.25) | 2 |
| layoff / slack work / position abolished | 12.41 (1.53) | 80 |
| other family / personal obligations | 2.09 (0.66) | 14 |
| temporary job ended | 5.72 (1.08) | 32 |
| plant closed / employer bankrupt or sold | 2.41 (0.71) | 16 |
| discharged / fired | 1.94 (0.64) | 13 |
| quit to take another job | 2.00 (0.65) | 10 |
| other involuntary (2014) | 2.74 (0.76) | 10 |

## SIPP: spell length / return to work (iv)

*persistent exits: all*

| | KM probability (%) | N |
|---|---|---|
| return within 3 months | 18.41 (0.60) | 7781 |
| return within 6 months | 37.01 (0.67) | 7781 |
| return within 12 months | 52.98 (0.78) | 7781 |
| return within 24 months | 66.20 (0.80) | 7781 |

*persistent exits: child aged 0 in t+1..t+9*

| | KM probability (%) | N |
|---|---|---|
| return within 3 months | 13.23 (1.52) | 913 |
| return within 6 months | 26.01 (2.15) | 913 |
| return within 12 months | 39.58 (2.21) | 913 |
| return within 24 months | 59.05 (2.64) | 913 |

*persistent exits: no child aged 0 in t+1..t+9*

| | KM probability (%) | N |
|---|---|---|
| return within 3 months | 19.16 (0.66) | 6868 |
| return within 6 months | 38.67 (0.85) | 6868 |
| return within 12 months | 55.07 (0.86) | 6868 |
| return within 24 months | 67.25 (0.95) | 6868 |

*persistent exits: race: Black*

| | KM probability (%) | N |
|---|---|---|
| return within 3 months | 17.00 (1.80) | 632 |
| return within 6 months | 39.22 (2.52) | 632 |
| return within 12 months | 58.43 (2.96) | 632 |
| return within 24 months | 72.97 (2.90) | 632 |

*persistent exits: race: White*

| | KM probability (%) | N |
|---|---|---|
| return within 3 months | 18.90 (0.63) | 6519 |
| return within 6 months | 37.03 (0.88) | 6519 |
| return within 12 months | 52.67 (0.93) | 6519 |
| return within 24 months | 66.06 (1.01) | 6519 |

*persistent exits: tenure 0-11 months*

| | KM probability (%) | N |
|---|---|---|
| return within 3 months | 23.05 (0.97) | 2412 |
| return within 6 months | 41.20 (1.36) | 2412 |
| return within 12 months | 56.93 (1.41) | 2412 |
| return within 24 months | 69.27 (1.45) | 2412 |

*persistent exits: tenure 12+ months*

| | KM probability (%) | N |
|---|---|---|
| return within 3 months | 17.26 (0.71) | 4359 |
| return within 6 months | 36.75 (0.93) | 4359 |
| return within 12 months | 52.68 (1.03) | 4359 |
| return within 24 months | 66.14 (1.13) | 4359 |

*persistent exits: previous exit in panel*

| | KM probability (%) | N |
|---|---|---|
| return within 3 months | 19.54 (1.53) | 1074 |
| return within 6 months | 39.16 (1.93) | 1074 |
| return within 12 months | 57.50 (2.09) | 1074 |
| return within 24 months | 73.14 (2.65) | 1074 |

*persistent exits: reason: unsatisfactory arrangements / other quit*

| | KM probability (%) | N |
|---|---|---|
| return within 3 months | 23.37 (1.26) | 1327 |
| return within 6 months | 38.17 (1.74) | 1327 |
| return within 12 months | 52.80 (1.79) | 1327 |
| return within 24 months | 64.12 (2.01) | 1327 |

*persistent exits: reason: no job end recorded*

| | KM probability (%) | N |
|---|---|---|
| return within 3 months | 11.58 (0.77) | 2807 |
| return within 6 months | 36.62 (1.17) | 2807 |
| return within 12 months | 53.54 (1.12) | 2807 |
| return within 24 months | 64.77 (1.34) | 2807 |

*persistent exits: reason: childcare / family*

| | KM probability (%) | N |
|---|---|---|
| return within 3 months | 13.70 (1.37) | 865 |
| return within 6 months | 25.98 (1.97) | 865 |
| return within 12 months | 38.88 (2.27) | 865 |
| return within 24 months | 58.84 (2.95) | 865 |

*persistent exits: reason: involuntary*

| | KM probability (%) | N |
|---|---|---|
| return within 3 months | 24.07 (1.17) | 1970 |
| return within 6 months | 42.78 (1.53) | 1970 |
| return within 12 months | 60.14 (1.53) | 1970 |
| return within 24 months | 73.99 (1.48) | 1970 |

*persistent exits: reason: quit to another job*

| | KM probability (%) | N |
|---|---|---|
| return within 3 months | 44.56 (4.53) | 268 |
| return within 6 months | 58.85 (4.78) | 268 |
| return within 12 months | 70.46 (5.04) | 268 |
| return within 24 months | 88.16 (5.95) | 268 |

*persistent exits: reason: own illness / injury*

| | KM probability (%) | N |
|---|---|---|
| return within 3 months | 13.25 (2.27) | 298 |
| return within 6 months | 20.05 (2.63) | 298 |
| return within 12 months | 36.75 (3.70) | 298 |
| return within 24 months | 47.11 (4.55) | 298 |

*persistent exits: reason: school*

| | KM probability (%) | N |
|---|---|---|
| return within 3 months | 13.02 (3.42) | 127 |
| return within 6 months | 23.64 (4.32) | 127 |
| return within 12 months | 49.12 (6.02) | 127 |
| return within 24 months | 65.77 (8.03) | 127 |

*persistent exits: reason: retirement*

| | KM probability (%) | N |
|---|---|---|
| return within 3 months | 12.22 (3.29) | 119 |
| return within 6 months | 28.01 (5.23) | 119 |
| return within 12 months | 36.91 (6.47) | 119 |
| return within 24 months | 48.54 (7.28) | 119 |

*persistent exits observed 12 months after (panel FE)*

| | returned within 12 months (pp) | N |
|---|---|---|
| reason: involuntary | 17.10*** (3.04; p=<0.001) | 4593 |
| reason: no job end recorded | 12.95*** (3.01; p=<0.001) | 4593 |
| reason: own illness / injury | -8.31 (5.18; p=0.108) | 4593 |
| reason: quit to another job | 32.78*** (5.23; p=<0.001) | 4593 |
| reason: retirement | -4.23 (8.11; p=0.602) | 4593 |
| reason: school | 3.95 (7.00; p=0.572) | 4593 |
| reason: unsatisfactory arrangements / other quit | 11.14*** (3.28; p=<0.001) | 4593 |
| child aged 0 in t+1..t+9: yes | -12.54*** (2.80; p=<0.001) | 4593 |
| race (husband): Black | 6.94** (3.25; p=0.033) | 4593 |
| race (husband): Other | -0.91 (3.19; p=0.776) | 4593 |
| wife's age: 25-29 | -2.67 (3.07; p=0.385) | 4593 |
| wife's age: 30-34 | 1.44 (2.81; p=0.610) | 4593 |
| wife's age: 40-44 | 0.97 (2.94; p=0.742) | 4593 |
| wife's age: 45-49 | -2.93 (3.07; p=0.340) | 4593 |
| wife's age: 50-54 | 0.37 (3.26; p=0.910) | 4593 |
| wife's age: 55-59 | -6.52* (3.90; p=0.094) | 4593 |
| job tenure (months): 0-5 | 3.52 (2.36; p=0.136) | 4593 |
| job tenure (months): 12-35 | -2.00 (2.34; p=0.393) | 4593 |
| job tenure (months): 6-11 | 0.59 (2.91; p=0.839) | 4593 |
| job tenure (months): unknown | -7.76*** (2.91; p=0.008) | 4593 |

Notes: clusters=4067; mean=54.553

## SIPP: persistence (vi)

*persistence, no tenure / hours controls*

| | persistent exit (pp) | N |
|---|---|---|
| previous persistent exit in panel: yes | 1.39*** (0.09; p=<0.001) | 837349 |

Notes: clusters=34645; mean=0.905

*persistence, with tenure and hours controls*

| | persistent exit (pp) | N |
|---|---|---|
| previous persistent exit in panel: yes | 0.91*** (0.09; p=<0.001) | 837349 |
| job tenure (months): 0-5 | 1.17*** (0.07; p=<0.001) | 837349 |
| job tenure (months): 12-35 | 0.35*** (0.04; p=<0.001) | 837349 |
| job tenure (months): 6-11 | 0.78*** (0.07; p=<0.001) | 837349 |
| job tenure (months): unknown | -0.24*** (0.08; p=0.004) | 837349 |

Notes: clusters=34645; mean=0.905

## PSID: steady state (vii)

*wives 25-59, husband working both years (annual years 1968-1996)*

| | annual exit: hours > 0 in t, 0 in t+1 (%) | N |
|---|---|---|
| all | 8.29 | 48325 |

## PSID: exit hazard by cell, share of wife-months and of exits (i)

*wives 25-59, husband working (annual exit)*

| | annual exit (%) | share of wife-months (%) | share of exits (%) | N |
|---|---|---|---|---|
| all | 8.29 |  |  | 48325 |
| birth in t+1: no | 7.71 (0.13) | 93.66 | 87.16 | 45259 |
| birth in t+1: yes | 16.76 (0.67) | 6.34 | 12.84 | 3066 |
| birth in t: no | 7.65 (0.12) | 94.01 | 86.74 | 45428 |
| birth in t: yes | 18.33 (0.72) | 5.99 | 13.26 | 2897 |
| youngest child (interview of t+1): 1-2 | 15.08 (0.48) | 11.42 | 20.78 | 5517 |
| youngest child (interview of t+1): 3-5 | 9.77 (0.36) | 14.15 | 16.68 | 6839 |
| youngest child (interview of t+1): 6-12 | 7.86 (0.24) | 25.86 | 24.55 | 12499 |
| youngest child (interview of t+1): 13-17 | 6.12 (0.30) | 13.59 | 10.04 | 6565 |
| youngest child (interview of t+1): none <18 | 5.84 (0.19) | 33.02 | 23.28 | 15957 |
| youngest child (interview of t+1): 0 | 19.73 (1.29) | 1.96 | 4.67 | 948 |
| her hours in t: 1750+ | 2.03 (0.09) | 47.98 | 11.74 | 23187 |
| her hours in t: 1000-1749 | 6.47 (0.22) | 26.71 | 20.85 | 12909 |
| her hours in t: 1-499 | 28.15 (0.57) | 12.92 | 43.88 | 6242 |
| her hours in t: 500-999 | 15.73 (0.47) | 12.39 | 23.53 | 5987 |
| his labor income t -> t+1: within +-25% | 7.89 (0.15) | 68.25 | 64.99 | 32982 |
| his labor income t -> t+1: zero / missing | 7.93 (0.98) | 1.57 | 1.50 | 757 |
| his labor income t -> t+1: rise > 25% | 9.89 (0.34) | 16.09 | 19.21 | 7774 |
| his labor income t -> t+1: fall > 25% | 8.41 (0.34) | 14.10 | 14.31 | 6812 |
| wife's age: 25-29 | 11.16 (0.31) | 22.04 | 29.67 | 10649 |
| wife's age: 50-54 | 8.12 (0.47) | 7.11 | 6.97 | 3436 |
| wife's age: 30-34 | 8.95 (0.28) | 21.73 | 23.48 | 10502 |
| wife's age: 35-39 | 6.54 (0.26) | 18.53 | 14.64 | 8954 |
| wife's age: 40-44 | 6.28 (0.29) | 14.99 | 11.36 | 7243 |
| wife's age: 45-49 | 6.71 (0.34) | 10.98 | 8.89 | 5306 |
| wife's age: 55-59 | 8.95 (0.60) | 4.62 | 5.00 | 2235 |
| race (head): White | 8.35 (0.15) | 74.22 | 74.78 | 35867 |
| race (head): Black | 8.11 (0.24) | 25.78 | 25.22 | 12458 |
| decade: 1968-79 | 11.79 (0.27) | 30.07 | 42.81 | 14532 |
| decade: 1980-89 | 7.27 (0.18) | 41.38 | 36.29 | 19995 |
| decade: 1990-95 | 6.07 (0.20) | 28.55 | 20.90 | 13798 |

## PSID: LPM of the exit on all covariates jointly (ii)

*wives 25-59, husband working (calendar-year FE)*

| | annual exit (pp) | N |
|---|---|---|
| birth in t+1: yes | 6.77*** (0.76; p=<0.001) | 48325 |
| birth in t: yes | 5.64*** (0.88; p=<0.001) | 48325 |
| youngest child (interview of t+1): 0 | 4.48*** (1.46; p=0.002) | 48325 |
| youngest child (interview of t+1): 1-2 | 0.81 (0.64; p=0.207) | 48325 |
| youngest child (interview of t+1): 13-17 | 0.25 (0.37; p=0.499) | 48325 |
| youngest child (interview of t+1): 3-5 | 0.69 (0.43; p=0.108) | 48325 |
| youngest child (interview of t+1): 6-12 | 0.31 (0.34; p=0.365) | 48325 |
| her hours in t: 1-499 | 24.99*** (0.66; p=<0.001) | 48325 |
| her hours in t: 1000-1749 | 3.93*** (0.26; p=<0.001) | 48325 |
| her hours in t: 500-999 | 12.99*** (0.52; p=<0.001) | 48325 |
| his labor income t -> t+1: fall > 25% | 0.59* (0.36; p=0.095) | 48325 |
| his labor income t -> t+1: rise > 25% | 1.96*** (0.36; p=<0.001) | 48325 |
| his labor income t -> t+1: zero / missing | 1.99* (1.05; p=0.057) | 48325 |
| wife's age: 25-29 | 2.39*** (0.43; p=<0.001) | 48325 |
| wife's age: 30-34 | 1.09*** (0.38; p=0.004) | 48325 |
| wife's age: 40-44 | 0.45 (0.38; p=0.232) | 48325 |
| wife's age: 45-49 | 0.94** (0.45; p=0.036) | 48325 |
| wife's age: 50-54 | 2.17*** (0.56; p=<0.001) | 48325 |
| wife's age: 55-59 | 2.90*** (0.73; p=<0.001) | 48325 |
| race (head): Black | 1.19*** (0.33; p=<0.001) | 48325 |

Notes: clusters=2646; mean=8.286

*husband's labor income > 0 in t and t+1 (calendar-year FE)*

| | annual exit (pp) | N |
|---|---|---|
| d log his labor income (x0.1) | 0.07** (0.03; p=0.027) | 47568 |

Notes: clusters=2642; mean=8.291

## PSID: status at the interview after the zero-hours year (v)

*all exits*

| | all exits | N |
|---|---|---|
| working | 11.49 (0.61) | 2734 |
| temporarily laid off | 0.44 (0.13) | 2734 |
| looking for work / unemployed | 4.65 (0.40) | 2734 |
| retired | 1.50 (0.23) | 2734 |
| disabled | 2.16 (0.28) | 2734 |
| keeping house | 75.60 (0.82) | 2734 |
| student | 3.99 (0.37) | 2734 |
| other | 0.18 (0.08) | 2734 |

*exits with a birth in t+1*

| | exits with a birth in t+1 | N |
|---|---|---|
| working | 6.11 (1.26) | 360 |
| temporarily laid off | 0.28 (0.28) | 360 |
| looking for work / unemployed | 2.50 (0.82) | 360 |
| retired | 0.28 (0.28) | 360 |
| disabled | 0.00 (0.00) | 360 |
| keeping house | 87.78 (1.73) | 360 |
| student | 3.06 (0.91) | 360 |
| other | 0.00 (0.00) | 360 |

*exits without a birth in t or t+1*

| | exits without a birth in t or t+1 | N |
|---|---|---|
| working | 12.28 (0.73) | 2027 |
| temporarily laid off | 0.39 (0.14) | 2027 |
| looking for work / unemployed | 5.03 (0.49) | 2027 |
| retired | 1.97 (0.31) | 2027 |
| disabled | 2.86 (0.37) | 2027 |
| keeping house | 72.62 (0.99) | 2027 |
| student | 4.59 (0.46) | 2027 |
| other | 0.25 (0.11) | 2027 |

*exits, wife 55-59*

| | exits, wife 55-59 | N |
|---|---|---|
| working | 3.60 (1.58) | 139 |
| temporarily laid off | 0.00 (0.00) | 139 |
| looking for work / unemployed | 3.60 (1.58) | 139 |
| retired | 15.11 (3.04) | 139 |
| disabled | 4.32 (1.72) | 139 |
| keeping house | 71.22 (3.84) | 139 |
| student | 1.44 (1.01) | 139 |
| other | 0.72 (0.72) | 139 |

## PSID: return to work (v)

*all exits*

| | share (%) | N |
|---|---|---|
| return within 1 year (hours > 0 in t+2) | 38.48 (0.81) | 3646 |
| return within 2 years (t+2..t+3) | 53.97 (0.86) | 3337 |
| return within 4 years (t+2..t+5) | 68.88 (0.88) | 2783 |

*exits with a birth in t+1*

| | share (%) | N |
|---|---|---|
| return within 1 year (hours > 0 in t+2) | 33.20 (2.14) | 485 |
| return within 2 years (t+2..t+3) | 51.60 (2.39) | 438 |
| return within 4 years (t+2..t+5) | 68.01 (2.42) | 372 |

*exits without a birth in t or t+1*

| | share (%) | N |
|---|---|---|
| return within 1 year (hours > 0 in t+2) | 40.05 (0.94) | 2714 |
| return within 2 years (t+2..t+3) | 55.23 (1.00) | 2488 |
| return within 4 years (t+2..t+5) | 68.89 (1.02) | 2051 |

## PSID: repeat exits (v)

*couples with at least one exit*

| | share with 2+ exits (%) | N |
|---|---|---|
| all | 32.36 | 2713 |

*all exits*

| | share of exits by wives with 2+ exits (%) | N |
|---|---|---|
| all | 54.17 | 4004 |

*couples*

| | mean eligible wife-years per couple | N |
|---|---|---|
| all | 7.15 | 6763 |

## PSID: persistence (vi)

*persistence, no hours controls (wife-years after the first)*

| | annual exit (pp) | N |
|---|---|---|
| previous exit of the same wife | 8.13*** (0.41; p=<0.001) | 41562 |

Notes: clusters=2468; mean=7.305

*persistence, with her hours in t (wife-years after the first)*

| | annual exit (pp) | N |
|---|---|---|
| previous exit of the same wife | 3.84*** (0.38; p=<0.001) | 41562 |

Notes: clusters=2468; mean=7.305
