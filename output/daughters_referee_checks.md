# Referee 3 checks on the sons-daughters contrast (simulated JPE round)

Built by `109.DaughtersRefereeChecks.py` (2026-10-20); design in its docstring. Per unit teen layoff share unless stated; clustered by 1968 family. *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**

## R3.1 The mother's work in the father's layoff waves (child FE, the child's teen waves)

| outcome | father's layoff in the wave | mean | child-waves / children |
|---|---|---|---|
| mother employed | 0.011 (0.010; p=0.268) | 0.712 | 57,363 / 11,631 |
| mother's ln annual hours (valid years) | -0.019 (0.023; p=0.393) | 7.223 | 38,712 / 9,749 |

Treated children with the mother observed before and after the first teen layoff: 958; the mother worked more after it for 18% of them.

| children | layoff x age, mother did not work more | layoff x age x (mother worked more) | sum (mother worked more) |
|---|---|---|---|
| daughters | 0.163* (0.084; p=0.052) | 0.024 (0.113; p=0.831) | 0.187* (0.101; p=0.063) |
| sons | -0.083 (0.101; p=0.414) | -0.029 (0.219; p=0.895) | -0.111 (0.207; p=0.590) |

## R3.2 Who is observed with a wage

| children | band | observed (mean) | layoff coefficient on being observed | eligible children |
|---|---|---|---|---|
| daughters | 25-29 | 0.610 | 0.068 (0.070; p=0.333) | 4,437 |
| daughters | 45-49 | 0.392 | 0.058 (0.083; p=0.481) | 2,857 |
| sons | 25-29 | 0.555 | -0.029 (0.066; p=0.664) | 4,777 |
| sons | 45-49 | 0.346 | 0.031 (0.072; p=0.663) | 3,032 |

Within-person ln wage slope of the layoff share, PSID weights vs PSID weights x inverse probability of being observed (the band's weight applied to the child's years in that band; other bands weight 1):

| children | PSID weights | x IPW |
|---|---|---|
| daughters | 0.168** (0.075; p=0.025) | 0.176** (0.076; p=0.021) |
| sons | -0.086 (0.096; p=0.371) | -0.134 (0.095; p=0.159) |

## R3.3 Years of schooling (one row per child, sons and daughters stacked)

Sons -0.404 (0.386; p=0.295); daughters 0.490 (0.385; p=0.203); daughters - sons 0.893* (0.491; p=0.069); children 6,212.

