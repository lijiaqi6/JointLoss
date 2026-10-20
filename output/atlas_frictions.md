# Opportunity Atlas outcomes vs women's search frictions, by state

Script `IGE/17.AtlasFrictions.py` (2026-10-17). **Descriptive and cross-sectional** (51 states incl. DC): no causal claim. Outcomes: Opportunity Atlas county predictions (children born 1978-83, household income rank at 31-37 given parents at the national p25 / p75) averaged to states with OI's preferred weights; the White-Black gap is averaged within counties where Black children live. Regressions: WLS weighted by Black children (2000 Census), HC1 s.e.; friction measures standardised (per 1 SD across states). Cells: coefficient, stars (*** p<0.01, ** p<0.05, * p<0.1), (s.e.), p-value.

## Friction measures across states (percent)

| measure | mean | SD | min | max | corr. with women's 1994-2000 job finding | persons-at-risk (sum over states) |
|---|---|---|---|---|---|---|
| women: annual re-employment, 1977-92 (March CPS) | 8.13 | 1.52 | 4.66 | 11.58 | 0.54 | 127,405 |
| men: annual re-employment, 1977-92 (March CPS) | 14.26 | 3.88 | 7.31 | 25.43 | 0.22 | 27,502 |
| women: monthly job finding of non-employed, 1994-2000 | 11.38 | 1.78 | 7.30 | 16.10 | 1.00 | 365,942 |
| men: monthly job finding of non-employed, 1994-2000 | 19.95 | 3.49 | 12.07 | 27.02 | 0.66 | 153,792 |
| women: monthly job finding of non-employed, 2005-21 | 10.16 | 1.29 | 6.94 | 13.26 | 0.75 | 896,789 |
| men: monthly job finding of non-employed, 2005-21 | 15.84 | 2.08 | 11.11 | 20.74 | 0.70 | 491,944 |
| women: monthly U->E, 1994-2000 | 30.16 | 5.04 | 17.67 | 40.65 | 0.78 | 365,942 |
| men: monthly U->E, 1994-2000 | 34.57 | 5.32 | 22.98 | 45.40 | 0.56 | 153,792 |
| women: looking share of non-employed, 1977-92 | 14.13 | 2.46 | 9.95 | 22.19 | -0.04 |  |
| men: looking share of non-employed, 1977-92 | 47.12 | 5.55 | 37.04 | 57.79 | 0.27 |  |
| women: looking share of non-employed, 1994-2000 | 14.34 | 2.13 | 9.43 | 24.01 | 0.13 |  |
| men: looking share of non-employed, 1994-2000 | 32.48 | 4.18 | 25.32 | 41.70 | 0.33 |  |

Correlation of women's and men's measures across states: 1977-92 re-employment 0.46; 1994-2000 job finding 0.66; 2005-21 job finding 0.63. Women's job finding 1994-2000 vs 2005-21: 0.75; vs 1977-92 re-employment: 0.54.

## Table 1. Childhood period: annual re-employment of women not working the previous year (March CPS 1977-92)

| | (1) W-B gap, p25 | (2) W-B gap, p75 | (3) Black, p25 | (4) White, p25 | (5) Black, p75 | (6) White, p75 | (7) W-B gap, p25 (women only, no controls) |
|---|---|---|---|---|---|---|---|
| Women: annual re-employment, 1977-92 (March CPS) (per SD) | -0.34 (0.47) p=0.471 | -0.26 (0.39) p=0.497 | -0.64*** (0.23) p=0.005 | -1.18** (0.60) p=0.049 | -1.20*** (0.34) p=<0.001 | -1.70*** (0.49) p=<0.001 | -0.92** (0.37) p=0.012 |
| Men: annual re-employment, 1977-92 (March CPS) (per SD) | 1.21* (0.72) p=0.093 | 0.48 (0.44) p=0.279 | 0.86** (0.34) p=0.011 | 2.37*** (0.75) p=0.002 | 0.98** (0.40) p=0.015 | 1.69*** (0.52) p=0.001 |  |
| State unemployment rate (pp) | 0.47 (0.31) p=0.134 | 0.31 (0.24) p=0.181 | -0.38* (0.22) p=0.080 | -0.02 (0.36) p=0.955 | -0.49* (0.30) p=0.099 | -0.26 (0.30) p=0.398 |  |
| Share Black among children (pp) | 0.03 (0.04) p=0.431 | 0.04 (0.03) p=0.188 | 0.01 (0.02) p=0.724 | 0.01 (0.05) p=0.869 | -0.02 (0.03) p=0.541 | 0.00 (0.04) p=0.921 |  |
| Region FE | yes | yes | yes | yes | yes | yes | no |
| Mean of outcome (weighted) | 12.6 | 15.8 | 32.6 | 44.5 | 44.3 | 59.9 | 12.6 |
| R2 | 0.47 | 0.67 | 0.61 | 0.58 | 0.56 | 0.63 | 0.14 |
| N (states) | 51 | 51 | 51 | 51 | 51 | 51 | 51 |

## Table 2. Monthly job finding of non-employed women (CPS basic monthly 1994-2000)

| | (1) W-B gap, p25 | (2) W-B gap, p75 | (3) Black, p25 | (4) White, p25 | (5) Black, p75 | (6) White, p75 | (7) W-B gap, p25 (women only, no controls) |
|---|---|---|---|---|---|---|---|
| Women: monthly job finding of non-employed, 1994-2000 (per SD) | -1.33** (0.59) p=0.023 | -1.27** (0.50) p=0.011 | 0.70 (0.71) p=0.327 | 0.39 (0.97) p=0.692 | 0.93 (0.96) p=0.332 | 0.01 (0.99) p=0.991 | -1.80*** (0.60) p=0.003 |
| Men: monthly job finding of non-employed, 1994-2000 (per SD) | 1.12*** (0.41) p=0.007 | 0.83** (0.38) p=0.027 | 0.06 (0.46) p=0.893 | 0.74 (0.77) p=0.332 | -0.62 (0.70) p=0.375 | -0.00 (0.69) p=1.000 |  |
| State unemployment rate (pp) | 1.51*** (0.26) p=<0.001 | 0.71* (0.38) p=0.061 | 0.47 (0.57) p=0.410 | 1.87** (0.82) p=0.022 | 0.27 (0.83) p=0.747 | 0.84 (0.74) p=0.259 |  |
| Share Black among children (pp) | 0.02 (0.03) p=0.531 | 0.05* (0.03) p=0.079 | -0.01 (0.03) p=0.657 | -0.03 (0.05) p=0.461 | -0.04 (0.04) p=0.337 | -0.01 (0.04) p=0.772 |  |
| Region FE | yes | yes | yes | yes | yes | yes | no |
| Mean of outcome (weighted) | 12.6 | 15.8 | 32.6 | 44.5 | 44.3 | 59.9 | 12.6 |
| R2 | 0.65 | 0.78 | 0.55 | 0.57 | 0.45 | 0.51 | 0.19 |
| N (states) | 51 | 51 | 51 | 51 | 51 | 51 | 51 |

## Table 3. Monthly job finding of non-employed women, 2005-2021 (after the children's childhood)

| | (1) W-B gap, p25 | (2) W-B gap, p75 | (3) Black, p25 | (4) White, p25 | (5) Black, p75 | (6) White, p75 | (7) W-B gap, p25 (women only, no controls) |
|---|---|---|---|---|---|---|---|
| Women: monthly job finding of non-employed, 2005-21 (per SD) | -1.80** (0.70) p=0.010 | -1.34*** (0.36) p=<0.001 | 0.44 (0.35) p=0.206 | -0.85 (0.71) p=0.230 | 0.03 (0.43) p=0.945 | -1.03** (0.46) p=0.025 | 0.27 (0.77) p=0.728 |
| Men: monthly job finding of non-employed, 2005-21 (per SD) | 1.96*** (0.63) p=0.002 | 1.32*** (0.31) p=<0.001 | 0.44 (0.34) p=0.186 | 2.31*** (0.78) p=0.003 | 0.56 (0.43) p=0.193 | 1.84*** (0.48) p=<0.001 |  |
| State unemployment rate (pp) | 0.79 (0.66) p=0.233 | 0.82* (0.46) p=0.078 | -0.87*** (0.29) p=0.003 | -0.92* (0.53) p=0.080 | -1.75*** (0.24) p=<0.001 | -1.27*** (0.32) p=<0.001 |  |
| Share Black among children (pp) | 0.10** (0.05) p=0.040 | 0.09*** (0.03) p=<0.001 | 0.04** (0.02) p=0.048 | 0.13** (0.06) p=0.018 | 0.07** (0.03) p=0.045 | 0.15*** (0.04) p=<0.001 |  |
| Region FE | yes | yes | yes | yes | yes | yes | no |
| Mean of outcome (weighted) | 12.6 | 15.8 | 32.6 | 44.5 | 44.3 | 59.9 | 12.6 |
| R2 | 0.53 | 0.75 | 0.74 | 0.67 | 0.78 | 0.75 | 0.00 |
| N (states) | 51 | 51 | 51 | 51 | 51 | 51 | 51 |

## Table 4. Monthly U->E of unemployed women (CPS basic monthly 1994-2000)

| | (1) W-B gap, p25 | (2) W-B gap, p75 | (3) Black, p25 | (4) White, p25 | (5) Black, p75 | (6) White, p75 | (7) W-B gap, p25 (women only, no controls) |
|---|---|---|---|---|---|---|---|
| Women: monthly U->E, 1994-2000 (per SD) | -1.76 (1.41) p=0.210 | -1.54* (0.83) p=0.062 | 0.38 (0.78) p=0.629 | 0.53 (1.42) p=0.706 | 0.14 (0.97) p=0.886 | -0.62 (1.01) p=0.539 | -1.90*** (0.46) p=<0.001 |
| Men: monthly U->E, 1994-2000 (per SD) | 0.20 (0.65) p=0.762 | 0.53 (0.56) p=0.346 | -0.64 (0.63) p=0.310 | -0.83 (0.86) p=0.338 | -1.52** (0.72) p=0.034 | -1.29* (0.74) p=0.084 |  |
| State unemployment rate (pp) | 0.85 (0.89) p=0.338 | 0.40 (0.61) p=0.518 | 0.05 (0.60) p=0.932 | 1.46 (1.05) p=0.162 | -0.69 (0.85) p=0.418 | -0.19 (0.91) p=0.834 |  |
| Share Black among children (pp) | -0.05 (0.04) p=0.227 | -0.00 (0.03) p=0.987 | -0.02 (0.03) p=0.626 | -0.06 (0.07) p=0.388 | -0.05 (0.05) p=0.315 | -0.05 (0.06) p=0.384 |  |
| Region FE | yes | yes | yes | yes | yes | yes | no |
| Mean of outcome (weighted) | 12.6 | 15.8 | 32.6 | 44.5 | 44.3 | 59.9 | 12.6 |
| R2 | 0.63 | 0.77 | 0.54 | 0.56 | 0.54 | 0.58 | 0.27 |
| N (states) | 51 | 51 | 51 | 51 | 51 | 51 | 51 |

## Table 5. Share of non-employed women looking for work (March CPS 1977-92)

| | (1) W-B gap, p25 | (2) W-B gap, p75 | (3) Black, p25 | (4) White, p25 | (5) Black, p75 | (6) White, p75 | (7) W-B gap, p25 (women only, no controls) |
|---|---|---|---|---|---|---|---|
| Women: looking share of non-employed, 1977-92 (per SD) | -0.95* (0.51) p=0.061 | -0.33 (0.35) p=0.344 | -1.05*** (0.35) p=0.003 | -2.05*** (0.56) p=<0.001 | -1.34*** (0.37) p=<0.001 | -1.75*** (0.37) p=<0.001 | -1.26*** (0.44) p=0.005 |
| Men: looking share of non-employed, 1977-92 (per SD) | -0.91 (0.73) p=0.212 | -0.46 (0.41) p=0.266 | 0.16 (0.49) p=0.739 | 1.06* (0.61) p=0.081 | 0.84** (0.38) p=0.029 | 1.10** (0.46) p=0.017 |  |
| State unemployment rate (pp) | 0.66* (0.34) p=0.054 | 0.45** (0.22) p=0.040 | -0.36* (0.21) p=0.094 | -0.28 (0.26) p=0.277 | -0.53** (0.22) p=0.016 | -0.33* (0.18) p=0.061 |  |
| Share Black among children (pp) | 0.04 (0.05) p=0.522 | 0.04 (0.03) p=0.191 | 0.05 (0.03) p=0.113 | 0.10 (0.07) p=0.144 | 0.06* (0.03) p=0.083 | 0.10** (0.05) p=0.029 |  |
| Region FE | yes | yes | yes | yes | yes | yes | no |
| Mean of outcome (weighted) | 12.6 | 15.8 | 32.6 | 44.5 | 44.3 | 59.9 | 12.6 |
| R2 | 0.49 | 0.67 | 0.65 | 0.59 | 0.61 | 0.65 | 0.17 |
| N (states) | 51 | 51 | 51 | 51 | 51 | 51 | 51 |

## Table 6. Share of non-employed women looking for work (CPS basic monthly 1994-2000)

| | (1) W-B gap, p25 | (2) W-B gap, p75 | (3) Black, p25 | (4) White, p25 | (5) Black, p75 | (6) White, p75 | (7) W-B gap, p25 (women only, no controls) |
|---|---|---|---|---|---|---|---|
| Women: looking share of non-employed, 1994-2000 (per SD) | -1.80*** (0.56) p=0.001 | -1.51*** (0.43) p=<0.001 | 0.32 (0.42) p=0.445 | -0.48 (0.68) p=0.482 | 0.67 (0.63) p=0.289 | -0.48 (0.60) p=0.420 | -0.82 (0.63) p=0.188 |
| Men: looking share of non-employed, 1994-2000 (per SD) | 1.50** (0.64) p=0.019 | 1.11*** (0.39) p=0.005 | 0.26 (0.50) p=0.600 | 1.76*** (0.50) p=<0.001 | 0.26 (0.54) p=0.637 | 1.37*** (0.46) p=0.003 |  |
| State unemployment rate (pp) | 1.57*** (0.36) p=<0.001 | 0.91*** (0.27) p=<0.001 | 0.01 (0.45) p=0.988 | 1.00 (0.61) p=0.101 | -0.18 (0.60) p=0.765 | 0.44 (0.54) p=0.420 |  |
| Share Black among children (pp) | 0.11** (0.05) p=0.021 | 0.12*** (0.04) p=0.001 | -0.02 (0.04) p=0.705 | 0.03 (0.06) p=0.593 | -0.04 (0.07) p=0.536 | 0.06 (0.06) p=0.341 |  |
| Region FE | yes | yes | yes | yes | yes | yes | no |
| Mean of outcome (weighted) | 12.6 | 15.8 | 32.6 | 44.5 | 44.3 | 59.9 | 12.6 |
| R2 | 0.70 | 0.82 | 0.54 | 0.64 | 0.47 | 0.60 | 0.06 |
| N (states) | 51 | 51 | 51 | 51 | 51 | 51 | 51 |

## Table 7. Robustness: unweighted (each state counts once), monthly job finding 1994-2000

| | (1) W-B gap, p25 | (2) W-B gap, p75 | (3) Black, p25 | (4) White, p25 | (5) Black, p75 | (6) White, p75 | (7) W-B gap, p25 (women only, no controls) |
|---|---|---|---|---|---|---|---|
| Women: monthly job finding of non-employed, 1994-2000 (per SD) | -1.15** (0.54) p=0.033 | -1.16** (0.48) p=0.015 | 1.82*** (0.54) p=<0.001 | 1.89** (0.86) p=0.028 | 1.81*** (0.55) p=0.001 | 0.97 (0.65) p=0.136 | -0.29 (0.41) p=0.483 |
| Men: monthly job finding of non-employed, 1994-2000 (per SD) | 0.76 (0.68) p=0.261 | 0.57 (0.74) p=0.441 | -0.94 (0.61) p=0.127 | -0.75 (0.78) p=0.339 | -1.11* (0.67) p=0.096 | -0.67 (0.66) p=0.307 |  |
| State unemployment rate (pp) | 0.07 (0.41) p=0.857 | 0.01 (0.50) p=0.981 | 0.04 (0.47) p=0.940 | -0.00 (0.70) p=0.995 | -0.31 (0.53) p=0.557 | -0.39 (0.68) p=0.565 |  |
| Share Black among children (pp) | 0.09*** (0.03) p=<0.001 | 0.08*** (0.03) p=0.001 | -0.03 (0.03) p=0.257 | 0.02 (0.05) p=0.719 | -0.04 (0.03) p=0.175 | 0.03 (0.04) p=0.467 |  |
| Region FE | yes | yes | yes | yes | yes | yes | no |
| Mean of outcome | 11.2 | 14.2 | 33.9 | 45.6 | 45.7 | 60.1 | 11.2 |
| R2 | 0.36 | 0.54 | 0.58 | 0.41 | 0.50 | 0.40 | 0.01 |
| N (states) | 51 | 51 | 51 | 51 | 51 | 51 | 51 |

## Black women's own monthly job finding (1994-2000), states with >= 200 matched non-employed Black women: N = 31

| | (1) W-B gap, p25 | (2) W-B gap, p75 | (3) Black, p25 | (4) White, p25 | (5) Black, p75 | (6) White, p75 |
|---|---|---|---|---|---|---|
| Black women: monthly job finding (per SD) | -0.41 (0.29) p=0.160 | -0.14 (0.22) p=0.532 | 0.54 (0.50) p=0.281 | 0.41 (0.63) p=0.520 | 0.13 (0.69) p=0.853 | 0.10 (0.71) p=0.890 |
| State unemployment rate (pp) | 1.88*** (0.47) p=<0.001 | 1.12*** (0.41) p=0.007 | 0.52 (0.57) p=0.369 | 2.12*** (0.82) p=0.010 | 0.26 (0.74) p=0.725 | 1.15 (0.73) p=0.115 |
| Share Black among children (pp) | -0.04 (0.04) p=0.322 | 0.01 (0.03) p=0.803 | 0.01 (0.03) p=0.842 | -0.04 (0.05) p=0.397 | -0.01 (0.05) p=0.753 | -0.01 (0.05) p=0.819 |
| Region FE | yes | yes | yes | yes | yes | yes |
| N (states) | 31 | 31 | 31 | 31 | 31 | 31 |

## Notes

- CPS basic monthly months used: 336 (1994-2021); month pairs used for flows: 329; median share of rotation-1-3/5-7 persons validly matched to the next month 0.93; pairs dropped (valid match share < 0.5; household-ID breaks), listed by the later month: 199506, 199507, 199508, 199509, 199701, 200405.
- 1977-92 measure is annual (not monthly): employed in the March survey week among those with zero weeks worked in the previous calendar year; it mixes the search friction with the choice to stay out (as do all the rates here). 1981 March file lacks Alaska, Hawaii and much of California (NBER errata).
- Opportunity Atlas has no state file; state values are weighted averages of county predictions (counties without an estimate for a race are dropped from that race's average).
- Unemployment rate: BLS LAUS (via UKCPR National Welfare Data), mean over 1980-92 / 1994-2000 / 2005-21 matching the friction period.