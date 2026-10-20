# Both parents present in childhood and adult outcomes (beta_P for the child block)

Built by `IGE/79.ParentsPresentOutcomes.py` (2026-10-20; WP7 of `IGE/proposals/fable_10h_plan_paperA.md`); definitions in its docstring. PSID children born 1968-1995 (SRC + SEO, unweighted), Black / White, >= 3 childhood interviews at 0-17. Both parents present = the head and wife of the child's family unit are the mother and the father at birth. Controls in every column: female, birth-year FE, parental education (max of the two parents; 5 groups), + Black in pooled rows. S.e. clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1. No sibling comparisons. Associations, not causal effects.

## 1. Children and the share of childhood with both parents

| | Children | Mean share both | Share = 1 | Share = 0 | Mean share 0-5 | Mean share 6-17 | Mean share two-adult unit | N log earnings 25-55 | N log earnings 30-40 | N schooling |
|---|---|---|---|---|---|---|---|---|---|---|
| Black | 6,176 | 0.378 | 0.243 | 0.485 | 0.456 | 0.335 | 0.540 | 2,171 | 1,856 | 3,130 |
| White | 6,927 | 0.695 | 0.550 | 0.174 | 0.835 | 0.637 | 0.866 | 2,923 | 2,502 | 3,661 |

Check: log earnings 25-55 recomputed here vs IGE/1's psid_kids.pkl: correlation 1.000 (N 4,710).

## 2. (A) Total association: share of childhood with both parents

No income controls: presence and everything that comes with it (including the income it brings).

| | Log earnings 25-55 | Log earnings 30-40 | Earnings rank | Years of schooling |
|---|---|---|---|---|
| Black: Share of childhood with both parents | 0.285*** (0.060; p=<0.001) | 0.248*** (0.066; p=<0.001) | 8.25*** (1.67; p=<0.001) | 0.606*** (0.087; p=<0.001) |
| Black: Mean of outcome / of first regressor | 9.624 / 0.412 | 9.681 / 0.429 | 41.159 / 0.412 | 13.569 / 0.388 |
| Black: N children / clusters | 2,168 / 534 | 1,854 / 507 | 2,168 / 534 | 3,125 / 612 |
| White: Share of childhood with both parents | 0.311*** (0.057; p=<0.001) | 0.319*** (0.068; p=<0.001) | 10.84*** (1.70; p=<0.001) | 0.857*** (0.110; p=<0.001) |
| White: Mean of outcome / of first regressor | 10.100 / 0.783 | 10.148 / 0.790 | 56.703 / 0.783 | 14.466 / 0.768 |
| White: N children / clusters | 2,923 / 977 | 2,502 / 915 | 2,923 / 977 | 3,660 / 1,079 |
| Pooled: Share of childhood with both parents | 0.295*** (0.041; p=<0.001) | 0.280*** (0.047; p=<0.001) | 9.46*** (1.19; p=<0.001) | 0.724*** (0.069; p=<0.001) |
| Pooled: Mean of outcome / of first regressor | 9.897 / 0.625 | 9.950 / 0.636 | 50.083 / 0.625 | 14.053 / 0.593 |
| Pooled: N children / clusters | 5,091 / 1,498 | 4,356 / 1,413 | 5,091 / 1,498 | 6,785 / 1,675 |

## 3. (B) Net of family income by childhood age: beta_P for the child block

The child block carries family income by childhood age separately; the coefficient on the share is the presence slope beta_P (whole childhood with both parents vs none).

| | Log earnings 25-55 | Log earnings 30-40 | Earnings rank | Years of schooling |
|---|---|---|---|---|
| Black: Share of childhood with both parents | -0.031 (0.069; p=0.649) | -0.129* (0.074; p=0.082) | -0.68 (1.91; p=0.720) | 0.213* (0.110; p=0.054) |
| Black: Log family income, ages 0-5 | 0.130** (0.051; p=0.011) | 0.173*** (0.056; p=0.002) | 4.00*** (1.13; p=<0.001) | 0.150** (0.066; p=0.023) |
| Black: Log family income, ages 6-17 | 0.307*** (0.055; p=<0.001) | 0.332*** (0.058; p=<0.001) | 8.62*** (1.28; p=<0.001) | 0.468*** (0.073; p=<0.001) |
| Black: Mean of outcome / of first regressor | 9.621 / 0.414 | 9.682 / 0.430 | 41.205 / 0.414 | 13.565 / 0.395 |
| Black: N children / clusters | 1,951 / 511 | 1,659 / 483 | 1,951 / 511 | 2,794 / 593 |
| White: Share of childhood with both parents | 0.069 (0.058; p=0.239) | 0.118* (0.072; p=0.099) | 2.49 (1.72; p=0.147) | 0.476*** (0.118; p=<0.001) |
| White: Log family income, ages 0-5 | 0.195*** (0.048; p=<0.001) | 0.178*** (0.065; p=0.006) | 6.84*** (1.38; p=<0.001) | 0.236*** (0.091; p=0.010) |
| White: Log family income, ages 6-17 | 0.332*** (0.047; p=<0.001) | 0.344*** (0.062; p=<0.001) | 10.55*** (1.39; p=<0.001) | 0.720*** (0.088; p=<0.001) |
| White: Mean of outcome / of first regressor | 10.109 / 0.793 | 10.162 / 0.801 | 57.087 / 0.793 | 14.510 / 0.785 |
| White: N children / clusters | 2,750 / 943 | 2,352 / 883 | 2,750 / 943 | 3,419 / 1,039 |
| Pooled: Share of childhood with both parents | 0.011 (0.045; p=0.801) | -0.012 (0.053; p=0.825) | 0.46 (1.28; p=0.722) | 0.299*** (0.081; p=<0.001) |
| Pooled: Log family income, ages 0-5 | 0.148*** (0.036; p=<0.001) | 0.166*** (0.042; p=<0.001) | 5.04*** (0.86; p=<0.001) | 0.180*** (0.054; p=<0.001) |
| Pooled: Log family income, ages 6-17 | 0.320*** (0.037; p=<0.001) | 0.334*** (0.042; p=<0.001) | 9.60*** (0.93; p=<0.001) | 0.592*** (0.058; p=<0.001) |
| Pooled: Mean of outcome / of first regressor | 9.907 / 0.636 | 9.963 / 0.648 | 50.495 / 0.636 | 14.085 / 0.609 |
| Pooled: N children / clusters | 4,701 / 1,445 | 4,011 / 1,359 | 4,701 / 1,445 | 6,213 / 1,622 |

## 4. (C) Absence by childhood age (0-5 vs 6-17), net of income

| | Log earnings 25-55 | Log earnings 30-40 | Earnings rank | Years of schooling |
|---|---|---|---|---|
| Black: Share with both parents, ages 0-5 | -0.101 (0.087; p=0.246) | -0.136 (0.096; p=0.157) | -2.80 (2.12; p=0.188) | -0.109 (0.124; p=0.379) |
| Black: Share with both parents, ages 6-17 | 0.056 (0.090; p=0.533) | 0.009 (0.098; p=0.930) | 1.90 (2.22; p=0.391) | 0.314** (0.134; p=0.019) |
| Black: Log family income, ages 0-5 | 0.144*** (0.053; p=0.007) | 0.185*** (0.059; p=0.002) | 4.40*** (1.15; p=<0.001) | 0.175** (0.069; p=0.011) |
| Black: Log family income, ages 6-17 | 0.298*** (0.056; p=<0.001) | 0.319*** (0.059; p=<0.001) | 8.33*** (1.27; p=<0.001) | 0.447*** (0.076; p=<0.001) |
| Black: Mean of outcome / of first regressor | 9.621 / 0.487 | 9.682 / 0.502 | 41.205 / 0.487 | 13.565 / 0.462 |
| Black: N children / clusters | 1,951 / 511 | 1,659 / 483 | 1,951 / 511 | 2,794 / 593 |
| White: Share with both parents, ages 0-5 | -0.109 (0.083; p=0.185) | -0.124 (0.109; p=0.253) | -3.60 (2.36; p=0.127) | 0.218 (0.164; p=0.184) |
| White: Share with both parents, ages 6-17 | 0.121** (0.058; p=0.036) | 0.169** (0.071; p=0.018) | 4.25** (1.69; p=0.012) | 0.286** (0.117; p=0.015) |
| White: Log family income, ages 0-5 | 0.206*** (0.049; p=<0.001) | 0.195*** (0.067; p=0.003) | 7.21*** (1.40; p=<0.001) | 0.231** (0.092; p=0.012) |
| White: Log family income, ages 6-17 | 0.323*** (0.048; p=<0.001) | 0.330*** (0.063; p=<0.001) | 10.23*** (1.40; p=<0.001) | 0.721*** (0.089; p=<0.001) |
| White: Mean of outcome / of first regressor | 10.109 / 0.890 | 10.162 / 0.898 | 57.087 / 0.890 | 14.510 / 0.881 |
| White: N children / clusters | 2,750 / 943 | 2,352 / 883 | 2,750 / 943 | 3,419 / 1,039 |
| Pooled: Share with both parents, ages 0-5 | -0.126** (0.059; p=0.032) | -0.159** (0.069; p=0.021) | -4.18*** (1.56; p=0.008) | -0.080 (0.098; p=0.414) |
| Pooled: Share with both parents, ages 6-17 | 0.102** (0.049; p=0.038) | 0.111* (0.057; p=0.052) | 3.60*** (1.35; p=0.008) | 0.342*** (0.089; p=<0.001) |
| Pooled: Log family income, ages 0-5 | 0.165*** (0.037; p=<0.001) | 0.187*** (0.044; p=<0.001) | 5.60*** (0.88; p=<0.001) | 0.202*** (0.056; p=<0.001) |
| Pooled: Log family income, ages 6-17 | 0.309*** (0.037; p=<0.001) | 0.320*** (0.043; p=<0.001) | 9.21*** (0.94; p=<0.001) | 0.574*** (0.059; p=<0.001) |
| Pooled: Mean of outcome / of first regressor | 9.907 / 0.723 | 9.963 / 0.734 | 50.495 / 0.723 | 14.085 / 0.692 |
| Pooled: N children / clusters | 4,701 / 1,445 | 4,011 / 1,359 | 4,701 / 1,445 | 6,213 / 1,622 |

## 5. (D) Alternative: any two-adult unit (step-parents included), net of income

| | Log earnings 25-55 | Log earnings 30-40 | Earnings rank | Years of schooling |
|---|---|---|---|---|
| Black: Share in a two-adult unit | -0.140* (0.081; p=0.086) | -0.258*** (0.090; p=0.004) | -4.12* (2.11; p=0.051) | 0.077 (0.133; p=0.563) |
| Black: Log family income, ages 0-5 | 0.144*** (0.051; p=0.005) | 0.189*** (0.056; p=<0.001) | 4.45*** (1.14; p=<0.001) | 0.167** (0.067; p=0.013) |
| Black: Log family income, ages 6-17 | 0.336*** (0.057; p=<0.001) | 0.369*** (0.060; p=<0.001) | 9.55*** (1.30; p=<0.001) | 0.497*** (0.079; p=<0.001) |
| Black: Mean of outcome / of first regressor | 9.621 / 0.519 | 9.682 / 0.530 | 41.205 / 0.519 | 13.565 / 0.506 |
| Black: N children / clusters | 1,951 / 511 | 1,659 / 483 | 1,951 / 511 | 2,794 / 593 |
| White: Share in a two-adult unit | -0.023 (0.085; p=0.784) | -0.005 (0.105; p=0.964) | -1.54 (2.50; p=0.540) | 0.270 (0.169; p=0.110) |
| White: Log family income, ages 0-5 | 0.198*** (0.048; p=<0.001) | 0.185*** (0.065; p=0.004) | 6.96*** (1.36; p=<0.001) | 0.268*** (0.091; p=0.003) |
| White: Log family income, ages 6-17 | 0.347*** (0.049; p=<0.001) | 0.361*** (0.064; p=<0.001) | 11.22*** (1.45; p=<0.001) | 0.744*** (0.090; p=<0.001) |
| White: Mean of outcome / of first regressor | 10.109 / 0.876 | 10.162 / 0.883 | 57.087 / 0.876 | 14.510 / 0.871 |
| White: N children / clusters | 2,750 / 943 | 2,352 / 883 | 2,750 / 943 | 3,419 / 1,039 |
| Pooled: Share in a two-adult unit | -0.122** (0.057; p=0.034) | -0.186*** (0.068; p=0.006) | -4.44*** (1.58; p=0.005) | 0.011 (0.102; p=0.911) |
| Pooled: Log family income, ages 0-5 | 0.158*** (0.036; p=<0.001) | 0.179*** (0.042; p=<0.001) | 5.41*** (0.86; p=<0.001) | 0.212*** (0.054; p=<0.001) |
| Pooled: Log family income, ages 6-17 | 0.349*** (0.038; p=<0.001) | 0.372*** (0.043; p=<0.001) | 10.67*** (0.96; p=<0.001) | 0.646*** (0.060; p=<0.001) |
| Pooled: Mean of outcome / of first regressor | 9.907 / 0.728 | 9.963 / 0.737 | 50.495 / 0.728 | 14.085 / 0.707 |
| Pooled: N children / clusters | 4,701 / 1,445 | 4,011 / 1,359 | 4,701 / 1,445 | 6,213 / 1,622 |

## 6. (E) Father's displacement sample: the income and presence channels in one regression

19's design: children whose father figure was first displaced (closure or layoff) at 0-17 vs never displaced at 0-17 (controls' pseudo event age 5); father figure working before the (pseudo) event; children of section 1 only. E1: treat + share of childhood with both parents + log family income in the 3 years before the (pseudo) event; E2: + log family income in the 3 years after.

| | Log earnings 25-55 | Log earnings 30-40 | Earnings rank | Years of schooling |
|---|---|---|---|---|
| Black, E1: Father figure displaced at 0-17 | -0.002 (0.064; p=0.980) | -0.106 (0.070; p=0.128) | -2.47 (1.77; p=0.161) | -0.116 (0.103; p=0.262) |
| Black, E1: Share of childhood with both parents | 0.260*** (0.085; p=0.002) | 0.201** (0.096; p=0.036) | 7.71*** (2.35; p=0.001) | 0.562*** (0.129; p=<0.001) |
| Black, E1: Log family income before (pseudo) event | 0.331*** (0.061; p=<0.001) | 0.320*** (0.061; p=<0.001) | 9.81*** (1.52; p=<0.001) | 0.386*** (0.093; p=<0.001) |
| Black, E1: Mean of outcome / of first regressor | 9.748 / 0.507 | 9.783 / 0.513 | 44.521 / 0.507 | 13.830 / 0.510 |
| Black, E1: N children / clusters | 1,133 / 408 | 979 / 367 | 1,133 / 408 | 1,573 / 483 |
| Black, E2: Father figure displaced at 0-17 | 0.046 (0.066; p=0.484) | -0.050 (0.071; p=0.484) | -1.12 (1.80; p=0.532) | -0.059 (0.105; p=0.573) |
| Black, E2: Share of childhood with both parents | 0.178** (0.085; p=0.037) | 0.083 (0.095; p=0.383) | 5.07** (2.42; p=0.036) | 0.447*** (0.137; p=0.001) |
| Black, E2: Log family income before (pseudo) event | 0.192** (0.083; p=0.020) | 0.153** (0.076; p=0.043) | 5.58*** (1.76; p=0.002) | 0.184* (0.103; p=0.076) |
| Black, E2: Log family income after (pseudo) event | 0.250*** (0.068; p=<0.001) | 0.294*** (0.069; p=<0.001) | 7.46*** (1.52; p=<0.001) | 0.353*** (0.088; p=<0.001) |
| Black, E2: Mean of outcome / of first regressor | 9.754 / 0.502 | 9.794 / 0.508 | 44.816 / 0.502 | 13.835 / 0.505 |
| Black, E2: N children / clusters | 1,092 / 401 | 941 / 358 | 1,092 / 401 | 1,520 / 476 |
| White, E1: Father figure displaced at 0-17 | -0.122*** (0.041; p=0.003) | -0.100** (0.046; p=0.029) | -3.83*** (1.22; p=0.002) | -0.399*** (0.080; p=<0.001) |
| White, E1: Share of childhood with both parents | 0.218*** (0.069; p=0.002) | 0.229*** (0.081; p=0.005) | 7.21*** (1.99; p=<0.001) | 0.780*** (0.134; p=<0.001) |
| White, E1: Log family income before (pseudo) event | 0.289*** (0.055; p=<0.001) | 0.264*** (0.059; p=<0.001) | 9.51*** (1.76; p=<0.001) | 0.480*** (0.081; p=<0.001) |
| White, E1: Mean of outcome / of first regressor | 10.150 / 0.421 | 10.208 / 0.423 | 58.379 / 0.421 | 14.605 / 0.423 |
| White, E1: N children / clusters | 2,475 / 894 | 2,132 / 841 | 2,475 / 894 | 3,057 / 987 |
| White, E2: Father figure displaced at 0-17 | -0.082** (0.040; p=0.043) | -0.065 (0.047; p=0.167) | -2.68** (1.24; p=0.030) | -0.349*** (0.082; p=<0.001) |
| White, E2: Share of childhood with both parents | 0.175** (0.071; p=0.013) | 0.189** (0.082; p=0.022) | 5.49*** (2.04; p=0.007) | 0.727*** (0.137; p=<0.001) |
| White, E2: Log family income before (pseudo) event | 0.175*** (0.061; p=0.004) | 0.143** (0.058; p=0.014) | 5.47*** (1.90; p=0.004) | 0.279*** (0.092; p=0.003) |
| White, E2: Log family income after (pseudo) event | 0.190*** (0.051; p=<0.001) | 0.189*** (0.053; p=<0.001) | 6.60*** (1.64; p=<0.001) | 0.308*** (0.088; p=<0.001) |
| White, E2: Mean of outcome / of first regressor | 10.155 / 0.418 | 10.215 / 0.420 | 58.516 / 0.418 | 14.617 / 0.420 |
| White, E2: N children / clusters | 2,428 / 884 | 2,093 / 832 | 2,428 / 884 | 2,997 / 979 |
| Pooled, E1: Father figure displaced at 0-17 | -0.084** (0.035; p=0.016) | -0.101*** (0.039; p=0.009) | -3.36*** (1.02; p=<0.001) | -0.298*** (0.064; p=<0.001) |
| Pooled, E1: Share of childhood with both parents | 0.242*** (0.054; p=<0.001) | 0.227*** (0.062; p=<0.001) | 7.62*** (1.51; p=<0.001) | 0.675*** (0.092; p=<0.001) |
| Pooled, E1: Log family income before (pseudo) event | 0.300*** (0.043; p=<0.001) | 0.285*** (0.046; p=<0.001) | 9.56*** (1.29; p=<0.001) | 0.460*** (0.061; p=<0.001) |
| Pooled, E1: Mean of outcome / of first regressor | 10.024 / 0.448 | 10.074 / 0.451 | 54.027 / 0.448 | 14.342 / 0.453 |
| Pooled, E1: N children / clusters | 3,608 / 1,294 | 3,111 / 1,202 | 3,608 / 1,294 | 4,630 / 1,459 |
| Pooled, E2: Father figure displaced at 0-17 | -0.040 (0.035; p=0.252) | -0.056 (0.039; p=0.152) | -2.14** (1.04; p=0.040) | -0.248*** (0.065; p=<0.001) |
| Pooled, E2: Share of childhood with both parents | 0.187*** (0.054; p=<0.001) | 0.161*** (0.062; p=0.010) | 5.62*** (1.55; p=<0.001) | 0.594*** (0.096; p=<0.001) |
| Pooled, E2: Log family income before (pseudo) event | 0.179*** (0.050; p=<0.001) | 0.145*** (0.048; p=0.002) | 5.49*** (1.38; p=<0.001) | 0.254*** (0.068; p=<0.001) |
| Pooled, E2: Log family income after (pseudo) event | 0.209*** (0.042; p=<0.001) | 0.230*** (0.043; p=<0.001) | 6.83*** (1.16; p=<0.001) | 0.328*** (0.063; p=<0.001) |
| Pooled, E2: Mean of outcome / of first regressor | 10.030 / 0.444 | 10.085 / 0.448 | 54.266 / 0.444 | 14.354 / 0.449 |
| Pooled, E2: N children / clusters | 3,520 / 1,278 | 3,034 / 1,185 | 3,520 / 1,278 | 4,517 / 1,445 |
