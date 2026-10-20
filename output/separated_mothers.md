# The separated wife's state in the PSID: child support, remarriage, work, program receipt

Built by `IGE/76.SeparatedMothers.py` (2026-10-20; WP3 of `proposals/fable_10h_plan_paperA.md`); definitions in its docstring. Mothers whose marriage ended (marital history: separation, else divorce year s) in 1984-2020, observed as that husband's wife at an interview in s-3..s+1 with a child 0-17 in the family unit, aged 25-59 at s, Black / White (head's race). Event time k = income year - s (income years <= 2021; all observed years, no balanced panel). Amounts in 2000 dollars. Unweighted SRC + SEO. Means with s.e. in parentheses; differences with stars and p-values; s.e. clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1.

## 1. Sample

| | Mothers | Age at s | Children 0-17 at baseline | Status 'divorced' | Ex-husband displaced s-2..s | Observed after s | Woman-years k>=0 |
|---|---|---|---|---|---|---|---|
| Black | 570 | 34.4 | 2.16 | 0.809 | 0.172 | 562 | 2,884 |
| White | 924 | 35.0 | 1.96 | 0.931 | 0.122 | 914 | 4,608 |

## 2. Where she is, by year since the separation

Shares of woman-years at each k (status at the interview of income year s + k).

| | k=0 | k=1 | k=2 | k=3 | k=4 | k=5 | k=6 | k=7 | k=8 | k=9 | k=10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Black: single (female head) | 0.860 | 0.882 | 0.862 | 0.840 | 0.827 | 0.807 | 0.786 | 0.765 | 0.774 | 0.770 | 0.739 |
| Black: new partner (wife / 'wife') | 0.003 | 0.027 | 0.064 | 0.099 | 0.120 | 0.154 | 0.177 | 0.208 | 0.184 | 0.215 | 0.228 |
| Black: with the ex-husband | 0.121 | 0.080 | 0.051 | 0.044 | 0.018 | 0.023 | 0.016 | 0.005 | 0.014 | 0.005 | 0.011 |
| Black: in another person's unit | 0.017 | 0.012 | 0.024 | 0.017 | 0.035 | 0.015 | 0.020 | 0.023 | 0.028 | 0.010 | 0.022 |
| Black: remarried (marital history) | 0.003 | 0.006 | 0.054 | 0.089 | 0.127 | 0.174 | 0.202 | 0.240 | 0.235 | 0.267 | 0.300 |
| Black: N | 356 | 338 | 297 | 293 | 284 | 259 | 248 | 221 | 217 | 191 | 180 |
| White: single (female head) | 0.874 | 0.830 | 0.713 | 0.638 | 0.612 | 0.601 | 0.572 | 0.524 | 0.479 | 0.508 | 0.473 |
| White: new partner (wife / 'wife') | 0.041 | 0.134 | 0.249 | 0.331 | 0.335 | 0.365 | 0.386 | 0.443 | 0.467 | 0.450 | 0.484 |
| White: with the ex-husband | 0.076 | 0.030 | 0.024 | 0.025 | 0.040 | 0.027 | 0.029 | 0.024 | 0.034 | 0.023 | 0.032 |
| White: in another person's unit | 0.009 | 0.006 | 0.014 | 0.006 | 0.014 | 0.007 | 0.013 | 0.008 | 0.020 | 0.019 | 0.011 |
| White: remarried (marital history) | 0.018 | 0.071 | 0.176 | 0.245 | 0.281 | 0.343 | 0.381 | 0.424 | 0.481 | 0.476 | 0.544 |
| White: N | 564 | 536 | 494 | 481 | 430 | 411 | 383 | 368 | 349 | 309 | 283 |

## 3. Remarriage and new partners

Kaplan-Meier cumulative share (1 - survival) by the end of year k after the separation year (k = 0 is the separation year itself); annual hazard = events / woman-years at risk over years 0-9 (mean of the event indicator, s.e. clustered by 1968 family). Differences: LPM on the woman-years at risk.

| | by end of year 0 | by end of year 1 | by end of year 2 | by end of year 4 | by end of year 9 | Annual hazard, years 0-9 | Mothers / woman-years |
|---|---|---|---|---|---|---|---|
| Remarriage (marital history): Black | 0.002 | 0.009 | 0.040 | 0.110 | 0.244 | 0.0262 (0.0023) | 570 / 4,348 |
| Remarriage (marital history): White | 0.015 | 0.067 | 0.154 | 0.275 | 0.473 | 0.0608 (0.0029) | 924 / 6,036 |
| Remarriage (marital history): Black - White |  |  |  |  |  | -0.035*** (0.004; p=<0.001) | 10,384 |
| Remarriage (marital history): ex-husband displaced - not (race FE) |  |  |  |  |  | 0.000 (0.005; p=0.935) | 10,384 |
| New partner (remarriage or cohabiting 'wife'): Black | 0.002 | 0.023 | 0.056 | 0.130 | 0.277 | 0.0307 (0.0024) | 570 / 4,274 |
| New partner (remarriage or cohabiting 'wife'): White | 0.034 | 0.114 | 0.225 | 0.383 | 0.576 | 0.0836 (0.0037) | 924 / 5,493 |
| New partner (remarriage or cohabiting 'wife'): Black - White |  |  |  |  |  | -0.053*** (0.004; p=<0.001) | 9,767 |
| New partner (remarriage or cohabiting 'wife'): ex-husband displaced - not (race FE) |  |  |  |  |  | 0.000 (0.006; p=0.954) | 9,767 |

## 4. Child support received after the separation

Her own child-support income (2000 dollars per month = annual / 12). 'Single' = she is the female head of her unit (the model's separated state) with at least one child 0-17 in it.

| | Share receiving | Mean per month | Median per month | Mean if receiving | Median if receiving | Child support / her labor income (ratio of means) | Woman-years / mothers |
|---|---|---|---|---|---|---|---|
| Black: single, children in unit, k = 0-10 | 0.380 (0.020) | 132 (10) | 0 | 347 | 287 | 0.076 | 2,004 / 510 |
| Black: single, children in unit, k = 1-5 | 0.392 (0.022) | 140 (11) | 0 | 359 | 300 | 0.084 | 1,098 / 444 |
| Black: any status (head or wife), k = 0-10 | 0.326 (0.017) | 111 (8) | 0 | 340 | 280 | 0.063 | 2,801 / 556 |
| White: single, children in unit, k = 0-10 | 0.643 (0.018) | 327 (17) | 207 | 509 | 418 | 0.165 | 2,209 / 718 |
| White: single, children in unit, k = 1-5 | 0.674 (0.020) | 375 (20) | 274 | 556 | 456 | 0.187 | 1,264 / 578 |
| White: any status (head or wife), k = 0-10 | 0.496 (0.015) | 234 (11) | 0 | 472 | 390 | 0.121 | 4,529 / 902 |

| | Raw | Children / k / calendar-year FE | N (woman-years) |
|---|---|---|---|
| Black - White, share positive | -0.264*** (0.026; p=<0.001) | -0.277*** (0.026; p=<0.001) | 4,213 |
| Black - White, monthly amount | -195.6*** (20.1; p=<0.001) | -210.3*** (21.0; p=<0.001) | 4,213 |

### 4b. Diagnostic-B input: monthly child support of single mothers by race and number of children

Mean per month (2000 dollars, s.e.), zeros included; share receiving; woman-years (k = 0-10).

| | 1 child | 2 children | 3+ children | All |
|---|---|---|---|---|
| Black | 102 (11); share 0.346; N 736 | 159 (16); share 0.412; N 748 | 134 (17); share 0.381; N 520 | 132 (10) |
| White | 253 (20); share 0.592; N 926 | 362 (23); share 0.682; N 894 | 424 (51); share 0.676; N 389 | 327 (17) |

By years since the separation:

| | k = 0-1 | k = 2-4 | k = 5-10 |
|---|---|---|---|
| Black | 102 (10); share 0.347 | 140 (13); share 0.395 | 146 (14); share 0.390 |
| White | 272 (16); share 0.603 | 377 (21); share 0.667 | 339 (25); share 0.666 |

By calendar income year:

| | 1984-1995 | 1996-2007 | 2008-2021 |
|---|---|---|---|
| Black | 120 (15); share 0.350; N 797 | 146 (14); share 0.420; N 645 | 133 (17); share 0.375; N 562 |
| White | 335 (25); share 0.687; N 952 | 406 (31); share 0.714; N 612 | 242 (22); share 0.512; N 645 |

## 5. Her employment and hours by year since the separation

Woman-years in which she is a head or a wife (family-file hours). k < 0: she is still the ex-husband's wife (her hours as a wife). Benchmark: all married mothers 25-59 with a child 0-17, income years 1984-2021 (the model's married wives' employment is about 0.81 in the data).

| | k=-3 | k=-2 | k=-1 | k=0 | k=1 | k=2 | k=3 | k=4 | k=5 | k=6 | k=7 | k=8 | k=9 | k=10 | Married mothers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Black: employed (hours > 0) | 0.804 | 0.836 | 0.806 | 0.857 | 0.847 | 0.859 | 0.847 | 0.850 | 0.839 | 0.848 | 0.856 | 0.858 | 0.836 | 0.852 | 0.797 |
| Black: annual hours | 1,316 | 1,334 | 1,342 | 1,500 | 1,496 | 1,572 | 1,511 | 1,553 | 1,515 | 1,623 | 1,575 | 1,604 | 1,562 | 1,596 | 1,371 |
| Black: N (head or wife) | 403 | 402 | 376 | 350 | 334 | 290 | 288 | 274 | 255 | 243 | 216 | 211 | 189 | 176 | 15,074 |
| White: employed (hours > 0) | 0.797 | 0.795 | 0.821 | 0.898 | 0.914 | 0.891 | 0.893 | 0.901 | 0.887 | 0.892 | 0.863 | 0.889 | 0.875 | 0.886 | 0.787 |
| White: annual hours | 1,206 | 1,262 | 1,313 | 1,516 | 1,588 | 1,577 | 1,645 | 1,595 | 1,596 | 1,670 | 1,578 | 1,691 | 1,605 | 1,741 | 1,220 |
| White: N (head or wife) | 689 | 669 | 660 | 559 | 533 | 487 | 478 | 424 | 408 | 378 | 365 | 342 | 303 | 280 | 34,541 |

Differences (OLS, s.e. clustered by 1968 family):

| | Single mothers k=1-5 - married mothers (raw) | ... with age-group and year FE | Within mother: single k=1-5 - married k=-3..-1 (mother FE) | Ex-husband displaced s-2..s - not (single, k=1-5) |
|---|---|---|---|---|
| Black: employed (hours > 0) | 0.052*** (0.016; p=0.001) [N 16,318] | 0.036** (0.016; p=0.030) | 0.035** (0.014; p=0.016) [N 2,249] | -0.090* (0.047; p=0.055) [N 1,244] |
| Black: annual hours | 167*** (43; p=<0.001) [N 16,318] | 106** (44; p=0.015) | 204*** (36; p=<0.001) [N 2,249] | -151 (126; p=0.229) [N 1,244] |
| White: employed (hours > 0) | 0.135*** (0.010; p=<0.001) [N 36,155] | 0.126*** (0.010; p=<0.001) | 0.118*** (0.014; p=<0.001) [N 3,385] | -0.013 (0.029; p=0.654) [N 1,614] |
| White: annual hours | 453*** (31; p=<0.001) [N 36,155] | 413*** (31; p=<0.001) | 407*** (34; p=<0.001) [N 3,385] | -76 (95; p=0.423) [N 1,614] |
| Pooled: employed (hours > 0) | 0.100*** (0.009; p=<0.001) [N 52,473] | 0.089*** (0.009; p=<0.001) | 0.084*** (0.010; p=<0.001) [N 5,634] | -0.053* (0.029; p=0.061) [N 2,858] |
| Pooled: annual hours | 348*** (26; p=<0.001) [N 52,473] | 287*** (27; p=<0.001) | 324*** (25; p=<0.001) [N 5,634] | -115 (80; p=0.149) [N 2,858] |

## 6. AFDC/TANF and food stamp receipt by year since the separation

Same woman-years. AFDC/TANF = head or wife received last year; food stamps = the family received last year (biennial era: last-year item only).

| | k=-3 | k=-2 | k=-1 | k=0 | k=1 | k=2 | k=3 | k=4 | k=5 | k=6 | k=7 | k=8 | k=9 | k=10 | Married mothers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Black: AFDC/TANF (head or wife) | 0.097 | 0.070 | 0.070 | 0.122 | 0.162 | 0.121 | 0.122 | 0.113 | 0.105 | 0.088 | 0.071 | 0.065 | 0.078 | 0.039 | 0.039 |
| Black: food stamps / SNAP (family) | 0.261 | 0.242 | 0.221 | 0.323 | 0.341 | 0.363 | 0.323 | 0.319 | 0.322 | 0.300 | 0.296 | 0.267 | 0.254 | 0.253 | 0.179 |
| Black: N (head or wife) | 403 | 402 | 376 | 350 | 334 | 290 | 288 | 274 | 255 | 243 | 216 | 211 | 189 | 176 | 15,074 |
| White: AFDC/TANF (head or wife) | 0.033 | 0.026 | 0.037 | 0.067 | 0.079 | 0.059 | 0.046 | 0.023 | 0.034 | 0.024 | 0.026 | 0.026 | 0.018 | 0.021 | 0.011 |
| White: food stamps / SNAP (family) | 0.103 | 0.091 | 0.103 | 0.193 | 0.210 | 0.193 | 0.165 | 0.146 | 0.140 | 0.122 | 0.123 | 0.094 | 0.102 | 0.093 | 0.052 |
| White: N (head or wife) | 689 | 669 | 660 | 559 | 533 | 487 | 478 | 424 | 408 | 378 | 365 | 342 | 303 | 280 | 34,541 |

Differences (OLS, s.e. clustered by 1968 family):

| | Single mothers k=1-5 - married mothers (raw) | ... with age-group and year FE | Within mother: single k=1-5 - married k=-3..-1 (mother FE) | Ex-husband displaced s-2..s - not (single, k=1-5) |
|---|---|---|---|---|
| Black: AFDC/TANF (head or wife) | 0.100*** (0.016; p=<0.001) [N 15,431] | 0.111*** (0.016; p=<0.001) | 0.075*** (0.014; p=<0.001) [N 2,116] | 0.095* (0.052; p=0.070) [N 1,148] |
| Black: food stamps / SNAP (family) | 0.174*** (0.020; p=<0.001) [N 16,289] | 0.187*** (0.021; p=<0.001) | 0.101*** (0.020; p=<0.001) [N 2,247] | 0.129** (0.055; p=0.020) [N 1,244] |
| White: AFDC/TANF (head or wife) | 0.050*** (0.010; p=<0.001) [N 33,756] | 0.051*** (0.010; p=<0.001) | 0.030*** (0.008; p=<0.001) [N 3,192] | 0.047 (0.037; p=0.201) [N 1,480] |
| White: food stamps / SNAP (family) | 0.150*** (0.015; p=<0.001) [N 36,147] | 0.156*** (0.015; p=<0.001) | 0.106*** (0.014; p=<0.001) [N 3,384] | 0.098* (0.054; p=0.066) [N 1,614] |
| Pooled: AFDC/TANF (head or wife) | 0.076*** (0.009; p=<0.001) [N 49,187] | 0.076*** (0.009; p=<0.001) | 0.049*** (0.008; p=<0.001) [N 5,308] | 0.072** (0.033; p=0.027) [N 2,628] |
| Pooled: food stamps / SNAP (family) | 0.177*** (0.013; p=<0.001) [N 52,436] | 0.169*** (0.012; p=<0.001) | 0.104*** (0.012; p=<0.001) [N 5,631] | 0.114*** (0.039; p=0.003) [N 2,858] |

## 7. Child support when the ex-husband had been displaced (s-2..s)

Single mothers with children, k = 0-10. Difference displaced - not displaced (pooled: race FE).

| | Share receiving | Monthly amount | N (woman-years) |
|---|---|---|---|
| Black | -0.166*** (0.040; p=<0.001) | -88.0*** (15.9; p=<0.001) | 2,004 (90 mothers with a displaced ex-husband) |
| White | -0.095* (0.057; p=0.093) | -154.7*** (35.5; p=<0.001) | 2,209 (86 mothers with a displaced ex-husband) |
| Pooled | -0.136*** (0.034; p=<0.001) | -115.8*** (17.6; p=<0.001) | 4,213 (176 mothers with a displaced ex-husband) |
