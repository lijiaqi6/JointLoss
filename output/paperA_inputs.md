# Paper A model inputs from data (IGE/62.PaperAInputs.py)

Run 2026-10-18 14:24. Every value below is a coded mapping from data (no hand tuning); files written: `paperA_model/inputs/fixed_inputs.json` (read by `params.load_fixed()`), `paperA_model/inputs/psid_entry_couples.csv` (read by `simulate.load_entry()`), `paperA_model/inputs/psid_entry_couples_25_30.csv`, `paperA_model/inputs/start_overrides.json`, `output/paperA_inputs_T7.csv`, `output/cps_couple_state_shares.csv`. Regression estimates carry *** p<0.01, ** p<0.05, * p<0.1.

## Values written to fixed_inputs.json

```json
{
 "mu_w": {
  "B": 2.290202863530899,
  "W": 2.4533790186127375
 },
 "mu_h": {
  "B": 2.3833470135487893,
  "W": 2.637718675246132
 },
 "psi_w": 0.457409120420379,
 "psi_h": 0.4945049867626991,
 "b0_annual": {
  "B": [
   0.15015641293013557,
   0.11585365853658537,
   0.05742574257425743,
   0.009603841536614645,
   0.0,
   0.0,
   0.0
  ],
  "W": [
   0.15041443198439786,
   0.14680685358255452,
   0.07244582043343653,
   0.006793478260869565,
   0.0,
   0.0,
   0.0
  ]
 },
 "b2_annual": {
  "B": [
   0.1468682505399568,
   0.07270323859881031,
   0.021435228331780055,
   0.005336179295624333,
   0.0009407337723424271,
   0.0,
   0.0
  ],
  "W": [
   0.11377245508982035,
   0.04568744662681469,
   0.01437632135306554,
   0.004042348411934553,
   0.0,
   0.0,
   0.0
  ]
 },
 "n_children": {
  "B": [
   [
    0,
    0,
    0,
    0,
    0,
    0,
    0
   ],
   [
    2,
    2,
    3,
    2,
    2,
    2,
    2
   ],
   [
    2,
    2,
    2,
    2,
    1,
    1,
    1
   ]
  ],
  "W": [
   [
    0,
    0,
    0,
    0,
    0,
    0,
    0
   ],
   [
    2,
    2,
    2,
    2,
    2,
    2,
    2
   ],
   [
    2,
    2,
    2,
    2,
    2,
    1,
    1
   ]
  ]
 },
 "p_cc": [
  0.0,
  1.6322023871952152,
  0.24728582103414176
 ],
 "share_s": {
  "B": [
   0.8725281411621539,
   0.08487982963188317,
   0.04259202920596288
  ],
  "W": [
   0.8323627287853578,
   0.12035496394897394,
   0.04728230726566833
  ]
 }
}
```

## CPS husband hazard (T7)

| Item | Race | Value | s.e. | p | N | Note | Window | Source |
|---|---|---:|---:|---:|---:|---|---|---|
| cps_h_hazard (monthly), both employed | B | 0.0063038 | 0.000204 |  | 175,325 |  | CPS 1994-2023 | IGE/62 (IGE/30, 37 panel) |
| check: all employed husbands (wife in any state) | B | 0.007187 | 0.000207 |  | 229,684 |  | CPS 1994-2023 | IGE/62 (IGE/30 panel) |
| cps_h_hazard (monthly), both employed | W | 0.0034042 | 4.15e-05 |  | 2,536,255 |  | CPS 1994-2023 | IGE/62 (IGE/30, 37 panel) |
| check: all employed husbands (wife in any state) | W | 0.003857 | 3.77e-05 |  | 3,477,537 |  | CPS 1994-2023 | IGE/62 (IGE/30 panel) |
| cps_h_hazard (monthly), both employed | pooled | 0.0036904 | 4.19e-05 |  | 2,893,414 |  | CPS 1994-2023 | IGE/62 (IGE/30, 37 panel) |
| check: all employed husbands (wife in any state) | pooled | 0.0041338 | 3.68e-05 |  | 3,977,518 |  | CPS 1994-2023 | IGE/62 (IGE/30 panel) |

Definitions:

- P(husband becomes a job loser other than on temporary layoff -- unemployed, PRUNTYPE 2-3 -- at t+1) among couples with both spouses employed at t and the husband employed or a job loser at t+1 (37's 'tau' sample; husbands on temporary layoff at t+1 and wives on layoff at t+1 dropped, as in the cps_jl_nt target); wife's composite weight; race = husband's race; household block bootstrap (Poisson weights).
- Same transition among all married husbands employed at t (wife in any labor-force state), husband employed or a non-temporary job loser at t+1; wife's composite weight.

## Wage levels

| Item | Race | Value | s.e. | p | N | Note | Window | Source |
|---|---|---:|---:|---:|---:|---|---|---|
| mu_w (mean log wage of employed wives 25-29) | B | 2.2902 | 0.0158 |  | 2,985 |  | PSID 1984-2021 | IGE/62 |
| mu_w (mean log wage of employed wives 25-29) | W | 2.4534 | 0.0129 |  | 7,026 |  | PSID 1984-2021 | IGE/62 |
| psi_w (grid step, 7 levels span q01-q99 of the persistent part) |  | 0.45741 |  |  | 16,431 |  | PSID 1984-2021 | IGE/62 |
| mu_h (mean log wage of employed husbands 25-29) | B | 2.3833 | 0.0161 |  | 2,888 |  | PSID 1984-2021 | IGE/62 |
| mu_h (mean log wage of employed husbands 25-29) | W | 2.6377 | 0.0107 |  | 7,419 |  | PSID 1984-2021 | IGE/62 |
| psi_h (grid step, 7 levels span q01-q99 of the persistent part) |  | 0.4945 |  |  | 20,351 |  | PSID 1984-2021 | IGE/62 |

Definitions:

- PSID married couples (male head, wife present, Black / White head), income years 1984-2021; log hourly wage = annual labor income / annual hours (2000 $), spouses with at least 260 annual hours and a wage of $2-$200; that spouse's age 25-29 in the income year; unweighted; s.e. clustered by 1968 family.
- Residual e = log wage minus its race x income-year mean, wives aged 40-49 in the income year (same sample rules as mu); psi = (q99 - q01)/6 x sqrt((V - sigma_nu^2 - 0.13 V)/V) with V = Var(e) = 0.3973, q01 = -1.546, q99 = 1.451, sigma_nu^2 = 0.0125 (BPS Table 3 transitory variance, params.FIXED_DEFAULTS), 0.13 = Bound et al. (1994) measurement-error share; shrink factor 0.916. Check without the year demeaning (race means only): psi = 0.4707.
- Residual e = log wage minus its race x income-year mean, husbands aged 40-49 in the income year (same sample rules as mu); psi = (q99 - q01)/6 x sqrt((V - sigma_nu^2 - 0.13 V)/V) with V = Var(e) = 0.4061, q01 = -1.724, q99 = 1.589, sigma_nu^2 = 0.0275 (BPS Table 3 transitory variance, params.FIXED_DEFAULTS), 0.13 = Bound et al. (1994) measurement-error share; shrink factor 0.896. Check without the year demeaning (race means only): psi = 0.4975.

## Wage prediction (regression)

| Item | Race | Value | s.e. | p | N | Note | Window | Source |
|---|---|---:|---:|---:|---:|---|---|---|
| h: const |  | 2.4372*** | 0.0121 | 0 | 70,407 |  | PSID 1984-2021 | IGE/62 |
| h: edu_13_15 |  | 0.18691*** | 0.0132 | 1.15e-45 | 70,407 |  | PSID 1984-2021 | IGE/62 |
| h: edu_16plus |  | 0.50144*** | 0.0157 | 1.17e-224 | 70,407 |  | PSID 1984-2021 | IGE/62 |
| h: black |  | -0.2148*** | 0.0145 | 2.01e-49 | 70,407 |  | PSID 1984-2021 | IGE/62 |
| h: age_30_34 |  | 0.16648*** | 0.0079 | 1.49e-98 | 70,407 |  | PSID 1984-2021 | IGE/62 |
| h: age_35_39 |  | 0.26491*** | 0.0101 | 4.99e-152 | 70,407 |  | PSID 1984-2021 | IGE/62 |
| h: age_40_44 |  | 0.33512*** | 0.0109 | 4.47e-206 | 70,407 |  | PSID 1984-2021 | IGE/62 |
| h: age_45_49 |  | 0.36272*** | 0.0118 | 3.16e-206 | 70,407 |  | PSID 1984-2021 | IGE/62 |
| h: age_50_54 |  | 0.3637*** | 0.0136 | 2.26e-158 | 70,407 |  | PSID 1984-2021 | IGE/62 |
| h: age_55_59 |  | 0.35228*** | 0.015 | 1.43e-122 | 70,407 |  | PSID 1984-2021 | IGE/62 |
| w: const |  | 2.1455*** | 0.0138 | 0 | 58,433 |  | PSID 1984-2021 | IGE/62 |
| w: edu_13_15 |  | 0.19699*** | 0.0144 | 7.33e-43 | 58,433 |  | PSID 1984-2021 | IGE/62 |
| w: edu_16plus |  | 0.5937*** | 0.0154 | 0 | 58,433 |  | PSID 1984-2021 | IGE/62 |
| w: black |  | -0.086307*** | 0.0145 | 2.59e-09 | 58,433 |  | PSID 1984-2021 | IGE/62 |
| w: age_30_34 |  | 0.11085*** | 0.0085 | 6.47e-39 | 58,433 |  | PSID 1984-2021 | IGE/62 |
| w: age_35_39 |  | 0.16829*** | 0.0106 | 1.27e-56 | 58,433 |  | PSID 1984-2021 | IGE/62 |
| w: age_40_44 |  | 0.21173*** | 0.0116 | 5.96e-75 | 58,433 |  | PSID 1984-2021 | IGE/62 |
| w: age_45_49 |  | 0.22087*** | 0.0122 | 1.04e-72 | 58,433 |  | PSID 1984-2021 | IGE/62 |
| w: age_50_54 |  | 0.24062*** | 0.0128 | 8.79e-79 | 58,433 |  | PSID 1984-2021 | IGE/62 |
| w: age_55_59 |  | 0.23026*** | 0.0147 | 1.4e-55 | 58,433 |  | PSID 1984-2021 | IGE/62 |

Definitions:

- OLS of the log hourly wage on education (base <= 12 years), age group (base 25-29) and Black, husbands (h) 25-59 employed (>= 260 hours), income years 1984-2021; s.e. clustered by 1968 family; R^2 = 0.198.
- OLS of the log hourly wage on education (base <= 12 years), age group (base 25-29) and Black, wives (w) 25-59 employed (>= 260 hours), income years 1984-2021; s.e. clustered by 1968 family; R^2 = 0.182.

## Child process

| Item | Race | Value | s.e. | p | N | Note | Window | Source |
|---|---|---:|---:|---:|---:|---|---|---|
| b0_annual age 25-29 | B | 0.15016 | 0.0115 |  | 959 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b0_annual age 30-34 | B | 0.11585 | 0.0125 |  | 656 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b0_annual age 35-39 | B | 0.057426 | 0.0104 |  | 505 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b0_annual age 40-44 | B | 0.0096038 | 0.00338 |  | 833 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b0_annual age 45-49 | B | 0 | 0 |  | 1,230 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b0_annual age 50-54 | B | 0 | 0 |  | 1,460 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b0_annual age 55-59 | B | 0 | 0 |  | 1,389 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b2_annual age 25-29 | B | 0.14687 | 0.0165 |  | 463 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b2_annual age 30-34 | B | 0.072703 | 0.00668 |  | 1,513 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b2_annual age 35-39 | B | 0.021435 | 0.00313 |  | 2,146 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b2_annual age 40-44 | B | 0.0053362 | 0.00168 |  | 1,874 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b2_annual age 45-49 | B | 0.00094073 | 0.00094 |  | 1,063 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b2_annual age 50-54 | B | 0 | 0 |  | 418 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b2_annual age 55-59 | B | 0 | 0 |  | 119 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b0_annual age 25-29 | W | 0.15041 | 0.00558 |  | 4,102 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b0_annual age 30-34 | W | 0.14681 | 0.00698 |  | 2,568 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b0_annual age 35-39 | W | 0.072446 | 0.00645 |  | 1,615 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b0_annual age 40-44 | W | 0.0067935 | 0.00175 |  | 2,208 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b0_annual age 45-49 | W | 0 | 0 |  | 3,432 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b0_annual age 50-54 | W | 0 | 0 |  | 4,341 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b0_annual age 55-59 | W | 0 | 0 |  | 4,779 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b2_annual age 25-29 | W | 0.11377 | 0.0142 |  | 501 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b2_annual age 30-34 | W | 0.045687 | 0.00431 |  | 2,342 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b2_annual age 35-39 | W | 0.014376 | 0.00173 |  | 4,730 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b2_annual age 40-44 | W | 0.0040423 | 0.00088 |  | 5,195 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b2_annual age 45-49 | W | 0 | 0 |  | 3,304 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b2_annual age 50-54 | W | 0 | 0 |  | 1,197 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |
| b2_annual age 55-59 | W | 0 | 0 |  | 284 |  | PSID 1984-2021 | IGE/62 (CAH 1985-2023) |

Definitions:

- Annual probability that the wife gives birth in calendar year y (CAH birth records, multiple births once) among married couple-years (income years 1984-2021, wife observed as the head's wife at the wave reporting year y, wife's age 25-59 in y, wife in the CAH) with no own child under 18 at the start of y (from her own births); set to 0 when the cell has fewer than 30 couple-years; unweighted.
- Annual probability that the wife gives birth in calendar year y (CAH birth records, multiple births once) among married couple-years (income years 1984-2021, wife observed as the head's wife at the wave reporting year y, wife's age 25-59 in y, wife in the CAH) with own youngest child aged 6-17 at the start of y (from her own births); set to 0 when the cell has fewer than 30 couple-years; unweighted.

## Number of children

| Item | Race | Value | s.e. | p | N | Note | Window | Source |
|---|---|---:|---:|---:|---:|---|---|---|
| n(k=1, age 25-29) | B | 2 |  |  | 2,238 | unrounded 2.13 | PSID 1984-2021 | IGE/62 |
| n(k=1, age 30-34) | B | 2 |  |  | 2,086 | unrounded 2.43 | PSID 1984-2021 | IGE/62 |
| n(k=1, age 35-39) | B | 3 |  |  | 1,175 | unrounded 2.51 | PSID 1984-2021 | IGE/62 |
| n(k=1, age 40-44) | B | 2 |  |  | 351 | unrounded 2.40 | PSID 1984-2021 | IGE/62 |
| n(k=1, age 45-49) | B | 2 |  |  | 63 | unrounded 2.03 | PSID 1984-2021 | IGE/62 |
| n(k=1, age 50-54) | B | 2 |  |  | 9 | unrounded 2.03 (nearest age group) | PSID 1984-2021 | IGE/62 |
| n(k=1, age 55-59) | B | 2 |  |  | 3 | unrounded 2.03 (nearest age group) | PSID 1984-2021 | IGE/62 |
| n(k=2, age 25-29) | B | 2 |  |  | 611 | unrounded 1.62 | PSID 1984-2021 | IGE/62 |
| n(k=2, age 30-34) | B | 2 |  |  | 1,736 | unrounded 2.13 | PSID 1984-2021 | IGE/62 |
| n(k=2, age 35-39) | B | 2 |  |  | 2,420 | unrounded 2.06 | PSID 1984-2021 | IGE/62 |
| n(k=2, age 40-44) | B | 2 |  |  | 1,940 | unrounded 1.72 | PSID 1984-2021 | IGE/62 |
| n(k=2, age 45-49) | B | 1 |  |  | 1,057 | unrounded 1.39 | PSID 1984-2021 | IGE/62 |
| n(k=2, age 50-54) | B | 1 |  |  | 371 | unrounded 1.20 | PSID 1984-2021 | IGE/62 |
| n(k=2, age 55-59) | B | 1 |  |  | 121 | unrounded 1.11 | PSID 1984-2021 | IGE/62 |
| n(k=1, age 25-29) | W | 2 |  |  | 4,446 | unrounded 1.79 | PSID 1984-2021 | IGE/62 |
| n(k=1, age 30-34) | W | 2 |  |  | 5,565 | unrounded 2.12 | PSID 1984-2021 | IGE/62 |
| n(k=1, age 35-39) | W | 2 |  |  | 3,672 | unrounded 2.35 | PSID 1984-2021 | IGE/62 |
| n(k=1, age 40-44) | W | 2 |  |  | 1,103 | unrounded 2.34 | PSID 1984-2021 | IGE/62 |
| n(k=1, age 45-49) | W | 2 |  |  | 139 | unrounded 2.14 | PSID 1984-2021 | IGE/62 |
| n(k=1, age 50-54) | W | 2 |  |  | 8 | unrounded 2.14 (nearest age group) | PSID 1984-2021 | IGE/62 |
| n(k=1, age 55-59) | W | 2 |  |  | 4 | unrounded 2.14 (nearest age group) | PSID 1984-2021 | IGE/62 |
| n(k=2, age 25-29) | W | 2 |  |  | 775 | unrounded 1.63 | PSID 1984-2021 | IGE/62 |
| n(k=2, age 30-34) | W | 2 |  |  | 2,783 | unrounded 2.02 | PSID 1984-2021 | IGE/62 |
| n(k=2, age 35-39) | W | 2 |  |  | 5,333 | unrounded 2.01 | PSID 1984-2021 | IGE/62 |
| n(k=2, age 40-44) | W | 2 |  |  | 5,469 | unrounded 1.82 | PSID 1984-2021 | IGE/62 |
| n(k=2, age 45-49) | W | 2 |  |  | 3,273 | unrounded 1.57 | PSID 1984-2021 | IGE/62 |
| n(k=2, age 50-54) | W | 1 |  |  | 1,097 | unrounded 1.30 | PSID 1984-2021 | IGE/62 |
| n(k=2, age 55-59) | W | 1 |  |  | 243 | unrounded 1.13 | PSID 1984-2021 | IGE/62 |

Definitions:

- Rounded mean number of children 0-17 in the family unit (roster) of married couples, by wife's interview age group and youngest child's bucket (0-5 / 6-17), interviews 1985-2022 (income years 1984-2021); k = 0 has n = 0 by definition; cells with fewer than 30 couple-years take the nearest age group.

## Childcare price

| Item | Race | Value | s.e. | p | N | Note | Window | Source |
|---|---|---:|---:|---:|---:|---|---|---|
| p_cc(k=1) (2000 $ per hour of the wife's work) |  | 1.6322 | 0.0475 |  | 8,255 |  | PSID 1999-2021 | IGE/62 (IGE/47 consumption module) |
| p_cc(k=2) (2000 $ per hour of the wife's work) |  | 0.24729 | 0.015 |  | 8,373 |  | PSID 1999-2021 | IGE/62 (IGE/47 consumption module) |

Definitions:

- Ratio of means: total annual child-care spending (47's 'childcare', per-period amounts annualised, nominal -> 2000 $ with the CPI-U of the income year) over total annual hours of wives with >= 260 hours, married couples, waves 1999-2021 (income years 1998-2020), youngest child in the income year 0-5 (roster age - 1); zeros included; share with positive spending 0.585; mean of individual ratios 1.668; s.e. clustered by 1968 family (delta method).
- Ratio of means: total annual child-care spending (47's 'childcare', per-period amounts annualised, nominal -> 2000 $ with the CPI-U of the income year) over total annual hours of wives with >= 260 hours, married couples, waves 1999-2021 (income years 1998-2020), youngest child in the income year 6-17 (roster age - 1); zeros included; share with positive spending 0.190; mean of individual ratios 0.242; s.e. clustered by 1968 family (delta method).

## Borrowing limit (start value)

| Item | Race | Value | s.e. | p | N | Note | Window | Source |
|---|---|---:|---:|---:|---:|---|---|---|
| a_bar start (thousand 2000 $) |  | 25.639 |  |  | 14,261 |  | PSID 1984-2019 wealth waves | IGE/62 (estimation/psid_wealth.py, ReducedForm/17) |

Definitions:

- Plan 1.5: a_bar starts at minus the 10th percentile of liquid wealth (checking/savings + bonds/CDs from 2019 + stocks - unsecured debt, 2000 $) of married couples with the wife aged 25-34 at the wealth interview; P10 = -25,639 2000 $; share <= 0 = 0.568; unweighted. An SMM parameter: start value only.

## Workplace match shares

| Item | Race | Value | s.e. | p | N | Note | Window | Source |
|---|---|---:|---:|---:|---:|---|---|---|
| P(s=0 | r), entry couples with s observed | B | 0.87253 |  |  | 3,287 |  | PSID 1984-2023 entries | IGE/62 |
| P(s=1 | r), entry couples with s observed | B | 0.08488 |  |  | 3,287 |  | PSID 1984-2023 entries | IGE/62 |
| P(s=2 | r), entry couples with s observed | B | 0.042592 |  |  | 3,287 |  | PSID 1984-2023 entries | IGE/62 |
| check: P(s=0 | r), both-employed couple-years | B | 0.87373 |  |  | 14,152 |  | PSID 1984-2021 | IGE/62 |
| check: P(s=1 | r), both-employed couple-years | B | 0.083239 |  |  | 14,152 |  | PSID 1984-2021 | IGE/62 |
| check: P(s=2 | r), both-employed couple-years | B | 0.043033 |  |  | 14,152 |  | PSID 1984-2021 | IGE/62 |
| P(s=0 | r), entry couples with s observed | W | 0.83236 |  |  | 7,212 |  | PSID 1984-2023 entries | IGE/62 |
| P(s=1 | r), entry couples with s observed | W | 0.12035 |  |  | 7,212 |  | PSID 1984-2023 entries | IGE/62 |
| P(s=2 | r), entry couples with s observed | W | 0.047282 |  |  | 7,212 |  | PSID 1984-2023 entries | IGE/62 |
| check: P(s=0 | r), both-employed couple-years | W | 0.83521 |  |  | 41,047 |  | PSID 1984-2021 | IGE/62 |
| check: P(s=1 | r), both-employed couple-years | W | 0.11231 |  |  | 41,047 |  | PSID 1984-2021 | IGE/62 |
| check: P(s=2 | r), both-employed couple-years | W | 0.052476 |  |  | 41,047 |  | PSID 1984-2021 | IGE/62 |

Definitions:

- Share of entry couples by workplace match, among couples with both spouses' codes at entry or later (couples never observed with both employed get s = 0 in the entry file and are excluded here).
- Share among married couple-years with both spouses employed and coded (CPS-comparable check; CPS pooled shares 0.823 / 0.114 / 0.063 among both-employed couples, IGE/60 cps_share_s0-s2).

## Entry population (psid_entry_couples.csv)

Definition: every PSID couple (male head with a wife present, head Black or White) enters at its first interview from 1984 on at which the wife's interview age is 25-59 (couples together before 1984 enter in 1984; couples formed before the wife is 25 enter at the first wave with her aged 25+), the model's 'January of the year of first observation' (sec7_model.tex). year0 = interview year; age0 = wife's interview age. Employment = interview status working or temporarily laid off (head: family-file status item; wife: 23's status item), else >= 260 annual hours if the item is missing. UI state = not employed and an own displacement (closure, layoff / firing; 19's / 23's dating) in the interview year or the year before. Human capital level h = 4 + round((ln w - mu_j(r)) / psi_j) truncated to 1-7, with ln w the log hourly wage of the income year before the interview (>= 260 hours, $2-$200), else the same person's last wage in the previous five years, else the regression prediction above (transitory shock ignored). k0 = youngest child in the family unit at the interview (none / 0-5 / 6-17). a0 = liquid wealth (thousand 2000 $) at the entry wave if a wealth wave, else the couple's own value within +-2 waves-years, else the median of its cell (wife's age 25-34 / 35-44 / 45-59 x race x the higher spouse's education <= 12 / 13-15 / 16+) at the nearest wealth wave (wealth waves 1984, 1989, 1994, 1999-2019). s = workplace match at entry (below), else at the couple's first later wave with both spouses' codes, else 0. The file `psid_entry_couples_25_30.csv` keeps the couples entering at the wife's age 25-30.

- Couples: 12,360 (4,134 Black, 8,226 White); entering in 1984: 2,956; entering at wife's age 25-30: 6,090.
- Share of entry couples with a0 below the start borrowing limit -a_bar = -25.6 (the simulator clips a0 to the asset grid): 0.063; a0 percentiles 10/50/90: -16.0/0.0/27.3 thousand 2000 $.
- s source: entry wave 0.693; later wave 0.157; never both employed: 0 0.151
- a0 source: own, entry wave 0.706; cell median, nearest wealth wave 0.111; own, wave +2 0.050; own, wave +1 0.046; own, wave -2 0.046; own, wave -1 0.042
- wife's wage source: entry year 0.764; prediction 0.162; previous 5 years 0.074
- husband's wage source: entry year 0.905; prediction 0.057; previous 5 years 0.038

| | Black | White |
|---|---:|---:|
| mean age0 | 33.500 | 33.512 |
| share s = 0 / 1 / 2 | 0.899/0.067/0.034 | 0.853/0.106/0.041 |
| wife employed | 0.679 | 0.710 |
| husband employed | 0.809 | 0.902 |
| wife UI state | 0.046 | 0.026 |
| husband UI state | 0.053 | 0.024 |
| k0 = 0 / 1 / 2 | 0.322/0.408/0.270 | 0.472/0.302/0.226 |
| median a0 (thousand 2000 $) | 0.000 | 0.580 |
| share a0 <= 0 | 0.709 | 0.445 |
| mean hw0 | 4.006 | 3.969 |
| mean hh0 | 4.160 | 4.196 |
| hw0 = 1 / 7 shares | 0.023/0.019 | 0.033/0.024 |
| hh0 = 1 / 7 shares | 0.018/0.022 | 0.022/0.029 |

## Workplace match coding (CPS analog)

CPS (IGE/37): s = 2 if the spouses share the detailed industry recode (PRDTIND1), the detailed occupation recode (PRDTOCC1) and the class of worker (PEIO1COW, 8 codes); s = 1 same detailed industry only. PSID analog coded here on both spouses' main jobs at the interview: industry = the CPS 2003+ detailed industry recode (51 groups + armed forces) mapped from the PSID 3-digit Census codes (1970 codes in waves to 2001, 2000 codes x 10 in 2003-2015, 2012 codes from 2017; code ranges in IND70 / IND4); occupation = the CPS 1994-2002 detailed occupation recode (46 groups of the 1990 classification) on 1970 codes (waves to 2001) and the CPS 2003+ recode (23 SOC major groups) on 2000 / 2010 codes (2003+), as the CPS panel itself switches recodes in 2003; class of worker = private / government / self-employed from 'work for self or others' and 'work for government' (the PSID does not separate federal / state / local or for-profit / nonprofit, so s = 2 is coarser than the CPS cell: the plan's 'approximate'). Defined when both spouses are employed with valid codes.

Family-file items read here (per wave):

|   wave | h_stat                                      | h_self                                            | h_govt                               | w_self                                            | w_govt                               |
|-------:|:--------------------------------------------|:--------------------------------------------------|:-------------------------------------|:--------------------------------------------------|:-------------------------------------|
|   1984 | V10453 'C1 EMPLOYMENT STATUS-HD'            | V10456 'C4 WORK SELF/OTR?(HD-E)'                  | V10457 'C5 WORK FOR GOVT?(HD-E)'     | V10674 'F5 WORK FOR SELF?(WF-E)'                  | V10675 'F6 WRK FOR GOVT? (WF-E)'     |
|   1985 | V11637 'B1 EMPLMT STATUS-HEAD'              | V11640 'B4 WORK SELF/OTR? (HD-E)'                 | V11648 'B12 WORK FOR GOVT?(HD-E)'    | V12003 'J4 WORK SELF/OTR? (WF-E)'                 | V12011 'J12 WORK FOR GOVT?(WF-E)'    |
|   1986 | V13046 'B1 EMPLMT STATUS-HEAD'              | V13049 'B4 WORK SELF/OTR? (HD-E)'                 | V13051 'B6 WORK FOR GOVT? (HD-E)'    | V13228 'D4 WORK SELF/OTR? (WF-E)'                 | V13230 'D6 WORK FOR GOVT? (WF-E)'    |
|   1987 | V14146 'B1 EMPLMT STATUS-HEAD'              | V14149 'B4 WORK SELF/OTR? (HD-E)'                 | V14151 'B6 WORK FOR GOVT? (HD-E)'    | V14324 'D4 WORK SELF/OTR? (WF-E)'                 | V14326 'D6 WORK FOR GOVT? (WF-E)'    |
|   1988 | V15154 'B1 EMPLOYMENT STATUS-HD'            | V15157 'B4 WORK SELF/OTR? (HD-E)'                 | V15159 'B6 WORK FOR GOVT? (HD-E)'    | V15459 'D4 WORK SELF/OTR? (WF-E)'                 | V15461 'D6 WORK FOR GOVT? (WF-E)'    |
|   1989 | V16655 'B1 EMPLOYMENT STATUS-HD'            | V16658 'B4 WORK SELF/OTR? (HD-E)'                 | V16660 'B6 WORK FOR GOVT? (HD-E)'    | V16977 'D4 WORK SELF/OTR? (WF-E)'                 | V16979 'D6 WORK FOR GOVT? (WF-E)'    |
|   1990 | V18093 'B1 EMPLOYMENT STATUS-HD'            | V18096 'B4 WORK SELF/OTR? (HD-E)'                 | V18098 'B6 WORK FOR GOVT? (HD-E)'    | V18398 'D4 WORK SELF/OTR? (WF-E)'                 | V18400 'D6 WORK FOR GOVT? (WF-E)'    |
|   1991 | V19393 'B1 EMPLOYMENT STATUS-HD'            | V19396 'B4 WORK SELF/OTR? (HD-E)'                 | V19398 'B6 WORK FOR GOVT? (HD-E)'    | V19698 'D4 WORK SELF/OTR? (WF-E)'                 | V19700 'D6 WORK FOR GOVT? (WF-E)'    |
|   1992 | V20693 'B1 EMPLOYMENT STATUS-HD'            | V20696 'B4 WORK SELF/OTR? (HD-E)'                 | V20698 'B6 WORK FOR GOVT? (HD-E)'    | V20998 'D4 WORK SELF/OTR? (WF-E)'                 | V21000 'D6 WORK FOR GOVT? (WF-E)'    |
|   1993 | V22448 'B1 HEAD 1993 EMPLOYMENT STATUS'     | V22451 'B4 WTR WORK FOR SELF/SOMEONE ELSE (HD-E)' | V22453 'B6 WTR WORK FOR GOVT (HD-E)' | V22804 'D4 WTR WORK FOR SELF/SOMEONE ELSE (WF-E)' | V22806 'D6 WTR WORK FOR GOVT (WF-E)' |
|   1994 | ER2068 'B1 EMPLOYMENT STATUS-HD'            | ER2074 'B4 WORK SELF/OTR? (HD-E)'                 | ER2078 'B6 WORK FOR GOVT? (HD-E)'    | ER2568 'D4 WORK SELF/OTR? (WF-E)'                 | ER2572 'D6 WORK FOR GOVT? (WF-E)'    |
|   1995 | ER5067 'B1 EMPLOYMENT STATUS-HD'            | ER5073 'B4 WORK SELF/OTR? (HD-E)'                 | ER5077 'B6 WORK FOR GOVT? (HD-E)'    | ER5567 'D4 WORK SELF/OTR? (WF-E)'                 | ER5571 'D6 WORK FOR GOVT? (WF-E)'    |
|   1996 | ER7163 'B1 EMPLOYMENT STATUS-HD'            | ER7169 'B4 WORK SELF/OTR? (HD-E)'                 | ER7173 'B6 WORK FOR GOVT? (HD-E)'    | ER7663 'D4 WORK SELF/OTR? (WF-E)'                 | ER7667 'D6 WORK FOR GOVT? (WF-E)'    |
|   1997 | ER10081 'B1 1ST MENTION'                    | ER10086 'B4 WORK SELF/OTR? (HD-E)'                | ER10088 'B6 WORK FOR GOVT? (HD-E)'   | ER10568 'D4 WORK SELF/OTR? (WF-E)'                | ER10570 'D6 WORK FOR GOVT? (WF-E)'   |
|   1999 | ER13205 'B1 1ST MENTION'                    | ER13210 'B4 WORK SELF/OTR? (HD-E)'                | ER13212 'B6 WORK FOR GOVT? (HD-E)'   | ER13722 'D4 WORK SELF/OTR? (WF-E)'                | ER13724 'D6 WORK FOR GOVT? (WF-E)'   |
|   2001 | ER17216 'B1 1ST MENTION'                    | ER17221 'B4 WORK SELF/OTR? (HD-E)'                | ER17223 'B6 WORK FOR GOVT? (HD-E)'   | ER17791 'D4 WORK SELF/OTR? (WF-E)'                | ER17793 'D6 WORK FOR GOVT? (WF-E)'   |
|   2003 | ER21123 'BC1 EMPLOYMENT STATUS-1ST MENTION' | ER21147 'BC22 WORK SELF/OTR?--JOB 1'              | ER21149 'BC24 WORK FOR GOVT?--JOB 1' | ER21397 'DE22 WORK SELF/OTR?--JOB 1'              | ER21399 'DE24 WORK FOR GOVT?--JOB 1' |
|   2005 | ER25104 'BC1 EMPLOYMENT STATUS-1ST MENTION' | ER25129 'BC22 WORK SELF/OTR?--JOB 1'              | ER25131 'BC24 WORK FOR GOVT?--JOB 1' | ER25387 'DE22 WORK SELF/OTR?--JOB 1'              | ER25389 'DE24 WORK FOR GOVT?--JOB 1' |
|   2007 | ER36109 'BC1 EMPLOYMENT STATUS-1ST MENTION' | ER36134 'BC22 WORK SELF/OTR?--JOB 1'              | ER36136 'BC24 WORK FOR GOVT?--JOB 1' | ER36392 'DE22 WORK SELF/OTR?--JOB 1'              | ER36394 'DE24 WORK FOR GOVT?--JOB 1' |
|   2009 | ER42140 'BC1 EMPLOYMENT STATUS-1ST MENTION' | ER42169 'BC22 WORK SELF/OTR?--JOB 1'              | ER42171 'BC24 WORK FOR GOVT?--JOB 1' | ER42421 'DE22 WORK SELF/OTR?--JOB 1'              | ER42423 'DE24 WORK FOR GOVT?--JOB 1' |
|   2011 | ER47448 'BC1 EMPLOYMENT STATUS-1ST MENTION' | ER47482 'BC22 WORK SELF/OTR?--JOB 1'              | ER47484 'BC24 WORK FOR GOVT?--JOB 1' | ER47739 'DE22 WORK SELF/OTR?--JOB 1'              | ER47741 'DE24 WORK FOR GOVT?--JOB 1' |
|   2013 | ER53148 'BC1 EMPLOYMENT STATUS-1ST MENTION' | ER53182 'BC22 WORK SELF/OTR?--JOB 1'              | ER53184 'BC24 WORK FOR GOVT?--JOB 1' | ER53445 'DE22 WORK SELF/OTR?--JOB 1'              | ER53447 'DE24 WORK FOR GOVT?--JOB 1' |
|   2015 | ER60163 'BC1 EMPLOYMENT STATUS-1ST MENTION' | ER60197 'BC22 WORK SELF/OTR?--JOB 1'              | ER60199 'BC24 WORK FOR GOVT?--JOB 1' | ER60460 'DE22 WORK SELF/OTR?--JOB 1'              | ER60462 'DE24 WORK FOR GOVT?--JOB 1' |
|   2017 | ER66164 'BC1 EMPLOYMENT STATUS-1ST MENTION' | ER66198 'BC22 WORK SELF/OTR?--JOB 1'              | ER66200 'BC24 WORK FOR GOVT?--JOB 1' | ER66473 'DE22 WORK SELF/OTR?--JOB 1'              | ER66475 'DE24 WORK FOR GOVT?--JOB 1' |
|   2019 | ER72164 'BC1 EMPLOYMENT STATUS-1ST MENTION' | ER72198 'BC22 WORK SELF/OTR?--JOB 1'              | ER72200 'BC24 WORK FOR GOVT?--JOB 1' | ER72475 'DE22 WORK SELF/OTR?--JOB 1'              | ER72477 'DE24 WORK FOR GOVT?--JOB 1' |
|   2021 | ER78167 'BC1 EMPLOYMENT STATUS-1ST MENTION' | ER78203 'BC22 WORK SELF/OTR?--JOB 1'              | ER78205 'BC24 WORK FOR GOVT?--JOB 1' | ER78517 'DE22 WORK SELF/OTR?--JOB 1'              | ER78519 'DE24 WORK FOR GOVT?--JOB 1' |
|   2023 | ER82150 'BC1 EMPLOYMENT STATUS-1ST MENTION' | ER82186 'BC22 WORK SELF/OTR?--JOB 1'              | ER82188 'BC24 WORK FOR GOVT?--JOB 1' | ER82505 'DE22 WORK SELF/OTR?--JOB 1'              | ER82507 'DE24 WORK FOR GOVT?--JOB 1' |
