# Does schooling carry the layoff's delayed cost to sons and its gain to daughters?

Built by `115.LayoffSchooling.py` (2026-10-24); design in its docstring. Per unit teen layoff share (one layoff year = 1/7). *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**

## A1. Sons' schooling on the father's teen layoff and closure shares (one row per son)

| outcome | mean | layoff share | closure share | sons |
|---|---|---|---|---|
| years of schooling | 14.033 | -0.192 (0.366; p=0.600) | 0.161 (0.461; p=0.727) | 4,762 |
| college (16+ years) | 0.355 | -0.042 (0.078; p=0.588) | 0.023 (0.113; p=0.842) | 4,762 |
| some college (13+) | 0.632 | 0.003 (0.087; p=0.975) | 0.054 (0.105; p=0.610) | 4,762 |

## A2. Within the same son: the layoff share x age, without and with schooling x age

| outcome | as before | + years of schooling x age | + college x age | sons |
|---|---|---|---|---|
| ln earnings | -0.236** (0.103; p=0.022) | -0.190** (0.089; p=0.033) | -0.213** (0.091; p=0.019) | 4,636 |
| ln hourly wage | -0.109 (0.082; p=0.184) | -0.069 (0.075; p=0.357) | -0.090 (0.072; p=0.211) | 4,636 |

## A3. The band change 45-49 - 25-29 of the layoff share, without and with schooling

| outcome | as before | + years of schooling |
|---|---|---|
| ln earnings | -0.914*** (0.249; p<0.001) | -0.763*** (0.237; p=0.001) |
| ln hourly wage | -0.603*** (0.192; p=0.002) | -0.470** (0.183; p=0.010) |

## B1. Schooling by sex (one row per child, stacked, every regressor x daughter)

| outcome | sons | daughters | daughters - sons | children |
|---|---|---|---|---|
| years of schooling | -0.404 (0.386; p=0.295) | 0.490 (0.385; p=0.203) | 0.893* (0.491; p=0.069) | 6,212 |
| college (16+ years) | -0.083 (0.087; p=0.338) | 0.088 (0.091; p=0.333) | 0.172 (0.116; p=0.139) | 6,212 |

## B2. Within-person ln wage slopes of the layoff share by sex, without and with schooling x age (by sex)

| spec | sons | daughters | daughters - sons |
|---|---|---|---|
| as in 107 | -0.086 (0.096; p=0.371) | 0.168** (0.075; p=0.025) | 0.254** (0.129; p=0.049) |
| + schooling x age (by sex) | -0.051 (0.087; p=0.562) | 0.112 (0.072; p=0.121) | 0.162 (0.119; p=0.173) |

