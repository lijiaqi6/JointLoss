# The added-worker effect by age (Bacher, Grubener and Nord 2025) and joint job loss by age: CPS couples

Built by `IGE/50.CPSAddedWorkerByAge.py` (2026-10-18; definitions in its docstring) on Paper A's CPS couples panel (30.CPSJointJobLoss.py's raw files and builder, here with both spouses aged 20-62: 7,021,875 couple-months). BGN = Bacher, Grubener and Nord (2025, JME), Section 2. **Couples:** married, spouse present, opposite sex, naming each other (BGN: married or cohabiting, any sex, both 26-65); the raw files stop at age 62, so BGN's oldest group 56-65 is 56-62 here. Probabilities weighted by the wife's composite weight. Cells: coefficient*** (s.e. clustered by household; p), in percentage points unless stated; *** p<0.01, ** p<0.05, * p<0.1. Associations, not causal effects.

Link-rate rule and dropped base months as in 30 (the 20-62 panel has the same household-ID breaks).

## 1. BGN's added-worker effect on Paper A's panel

EN couples: primary earner employed and spouse not in the labor force at m-1, both observed at m. AWE = P(spouse NE or NU | primary EU) - P(spouse NE or NU | primary EE), same month. The Elsby-Hobijn-Sahin (2015) correction recodes N-U-N to N-N-N and U-N-U to U-U-U in each spouse's status sequence where the three months are observed (it moves the spouse's status, never the primary earner's E -> U or E -> E). BGN's window: every month used up to February 2020 (their data run '1994 until early 2020').

### 1a. BGN Tables 1-2 format: main variant (sex-neutral, 1994-Feb 2020, EHS-adjusted, all EU)

Percent. 'Ours' = this panel; 'BGN' = their Table 1 (All) / Table 2 (by the spouse's age; their oldest group is 56-65). AWE row: EU coefficient of a weighted LPM (EE + EU sample), pp.

| | Ours: EE | Ours: EU | Ours: AWE | BGN: EE | BGN: EU | BGN: AWE |
|---|---|---|---|---|---|---|
| **All EN couples** | | | | | | |
| Primary earner's flow rate (EN 1.62%) | 97.46 | 0.92 | | 97.16 | 1.00 | |
| Spouse NE | 6.06 | 7.97 | 1.91*** (0.31; p<0.001) | 5.93 | 7.65 | 1.72 |
| Spouse NU | 1.61 | 5.33 | 3.72*** (0.26; p<0.001) | 1.61 | 5.44 | 3.83 |
| Spouse NN | 92.33 | 86.70 | | 92.46 | 86.92 | |
| **AWE (total)** | | | **5.64*** (0.39; p<0.001)** | | | **5.55** |
| N couple-months (N primary EU) | 1,100,189 (10,026) | | | 1,280,562 | | |
| **Spouse aged 26-35** | | | | | | |
| Primary earner's flow rate (EN 1.08%) | 97.79 | 1.13 | | 97.67 | 1.22 | |
| Spouse NE | 6.42 | 8.24 | 1.82*** (0.55; p=0.001) | 6.53 | 8.96 | 2.43 |
| Spouse NU | 1.82 | 6.35 | 4.53*** (0.50; p<0.001) | 1.97 | 6.66 | 4.69 |
| Spouse NN | 91.76 | 85.41 | | 91.50 | 84.37 | |
| **AWE (total)** | | | **6.35*** (0.72; p<0.001)** | | | **7.12** |
| N couple-months (N primary EU) | 282,070 (3,114) | | | 313,017 | | |
| **Spouse aged 36-45** | | | | | | |
| Primary earner's flow rate (EN 1.18%) | 97.91 | 0.91 | | 97.77 | 1.01 | |
| Spouse NE | 6.64 | 9.39 | 2.75*** (0.62; p<0.001) | 6.64 | 8.97 | 2.33 |
| Spouse NU | 1.78 | 6.20 | 4.42*** (0.50; p<0.001) | 1.86 | 6.36 | 4.50 |
| Spouse NN | 91.58 | 84.41 | | 91.50 | 84.67 | |
| **AWE (total)** | | | **7.17*** (0.77; p<0.001)** | | | **6.83** |
| N couple-months (N primary EU) | 325,712 (2,932) | | | 349,892 | | |
| **Spouse aged 46-55** | | | | | | |
| Primary earner's flow rate (EN 1.76%) | 97.40 | 0.84 | | 97.30 | 0.92 | |
| Spouse NE | 6.07 | 8.12 | 2.05*** (0.63; p=0.001) | 6.04 | 7.41 | 1.37 |
| Spouse NU | 1.57 | 4.54 | 2.98*** (0.47; p<0.001) | 1.62 | 4.82 | 3.20 |
| Spouse NN | 92.36 | 87.34 | | 92.34 | 87.77 | |
| **AWE (total)** | | | **5.02*** (0.77; p<0.001)** | | | **4.57** |
| N couple-months (N primary EU) | 299,163 (2,493) | | | 314,078 | | |
| **Spouse aged 56-62** | | | | | | |
| Primary earner's flow rate (EN 3.00%) | 96.23 | 0.77 | | 95.72 | 0.81 | |
| Spouse NE | 4.42 | 4.13 | -0.29 (0.59; p=0.631) | 4.26 | 3.77 | -0.49 |
| Spouse NU | 1.02 | 2.53 | 1.51*** (0.45; p<0.001) | 0.89 | 2.78 | 1.89 |
| Spouse NN | 94.56 | 93.34 | | 94.84 | 93.45 | |
| **AWE (total)** | | | **1.22* (0.74; p=0.097)** | | | **1.40** |
| N couple-months (N primary EU) | 193,244 (1,487) | | | 303,575 | | |

### 1b. AWE regressions, outcome: spouse enters the labor force (NE or NU), same month (pp)

One weighted LPM per column on the EE + EU sample; rows 'EU x spouse aged ...' come from one fully interacted regression per column (age-group FE); 'EU, all ages' from a separate regression.

| | (1) spouse enters the labor force (NE or NU) | (2) spouse enters the labor force (NE or NU) | (3) spouse enters the labor force (NE or NU) | (4) spouse enters the labor force (NE or NU) | (5) spouse enters the labor force (NE or NU) | (6) spouse enters the labor force (NE or NU) | (7) spouse enters the labor force (NE or NU) |
|---|---|---|---|---|---|---|---|
| Primary earner EU (vs EE), all ages | 5.64*** (0.39; p<0.001) | 7.65*** (0.42; p<0.001) | 4.53*** (0.41; p<0.001) | 5.48*** (0.37; p<0.001) | 5.58*** (0.42; p<0.001) | 6.48*** (0.45; p<0.001) | 6.22*** (0.42; p<0.001) |
| EU x spouse aged 26-35 | 6.35*** (0.72; p<0.001) | 9.18*** (0.79; p<0.001) | 5.30*** (0.75; p<0.001) | 6.27*** (0.69; p<0.001) | 6.61*** (0.73; p<0.001) | 8.03*** (0.82; p<0.001) | 7.81*** (0.81; p<0.001) |
| EU x spouse aged 36-45 | 7.17*** (0.77; p<0.001) | 9.04*** (0.81; p<0.001) | 6.11*** (0.81; p<0.001) | 6.93*** (0.73; p<0.001) | 6.39*** (0.79; p<0.001) | 7.38*** (0.84; p<0.001) | 7.83*** (0.83; p<0.001) |
| EU x spouse aged 46-55 | 5.02*** (0.77; p<0.001) | 6.75*** (0.83; p<0.001) | 3.78*** (0.80; p<0.001) | 4.72*** (0.72; p<0.001) | 4.66*** (0.86; p<0.001) | 5.32*** (0.91; p<0.001) | 4.92*** (0.81; p<0.001) |
| EU x spouse aged 56-62 | 1.22* (0.74; p=0.097) | 2.10** (0.82; p=0.010) | 0.35 (0.74; p=0.639) | 1.74** (0.72; p=0.016) | 1.26 (0.91; p=0.168) | 1.36 (0.94; p=0.145) | 1.63** (0.80; p=0.043) |
| Difference: 56-62 minus 26-35 | -5.13*** (1.03; p<0.001) | -7.08*** (1.14; p<0.001) | -4.95*** (1.06; p<0.001) | -4.52*** (1.00; p<0.001) | -5.35*** (1.17; p<0.001) | -6.67*** (1.24; p<0.001) | -6.18*** (1.14; p<0.001) |
| Wald test: equal across the four ages | chi2(3) = 37.9; p<0.001 | chi2(3) = 49.5; p<0.001 | chi2(3) = 33.7; p<0.001 | chi2(3) = 30.8; p<0.001 | chi2(3) = 24.8; p<0.001 | chi2(3) = 33.7; p<0.001 | chi2(3) = 40.0; p<0.001 |
| Couples | sex-neutral | sex-neutral | sex-neutral | sex-neutral | wife = spouse | wife = spouse | sex-neutral |
| Years | 1994-Feb 2020 | 1994-Feb 2020 | 1994-Feb 2020 | 1994-2023 | 1994-Feb 2020 | 1994-2023 | 1994-2023 |
| EHS correction | yes | no | yes | yes | yes | no | no |
| Primary earner's EU | all | all | job loser | all | all | job loser | job loser |
| Fixed effects | none (age-group FE in the age rows) | none (age-group FE in the age rows) | none (age-group FE in the age rows) | none (age-group FE in the age rows) | none (age-group FE in the age rows) | none (age-group FE in the age rows) | none (age-group FE in the age rows) |
| N (EE + EU) / clusters | 1,082,535 / 342,629 | 1,080,724 / 345,177 | 1,080,997 / 342,047 | 1,189,575 / 375,597 | 887,182 / 276,274 | 970,690 / 303,463 | 1,185,975 / 377,692 |
| Mean outcome under EE, all ages (%) | 7.67 | 8.63 | 7.67 | 7.68 | 7.17 | 7.94 | 8.61 |

### 1c. AWE regressions, outcome: spouse N -> E, same month (pp)

One weighted LPM per column on the EE + EU sample; rows 'EU x spouse aged ...' come from one fully interacted regression per column (age-group FE); 'EU, all ages' from a separate regression.

| | (1) spouse N -> E | (2) spouse N -> E | (3) spouse N -> E | (4) spouse N -> E | (5) spouse N -> E | (6) spouse N -> E | (7) spouse N -> E |
|---|---|---|---|---|---|---|---|
| Primary earner EU (vs EE), all ages | 1.91*** (0.31; p<0.001) | 1.91*** (0.31; p<0.001) | 1.23*** (0.32; p<0.001) | 1.83*** (0.30; p<0.001) | 1.67*** (0.33; p<0.001) | 1.11*** (0.33; p<0.001) | 1.18*** (0.31; p<0.001) |
| EU x spouse aged 26-35 | 1.82*** (0.55; p=0.001) | 1.83*** (0.56; p<0.001) | 0.99* (0.57; p=0.085) | 1.72*** (0.53; p=0.001) | 2.03*** (0.57; p<0.001) | 1.27** (0.57; p=0.025) | 0.90 (0.55; p=0.103) |
| EU x spouse aged 36-45 | 2.75*** (0.62; p<0.001) | 2.73*** (0.62; p<0.001) | 2.43*** (0.66; p<0.001) | 2.69*** (0.60; p<0.001) | 2.07*** (0.62; p<0.001) | 1.89*** (0.63; p=0.003) | 2.45*** (0.64; p<0.001) |
| EU x spouse aged 46-55 | 2.05*** (0.63; p=0.001) | 2.04*** (0.63; p=0.001) | 1.01 (0.64; p=0.116) | 1.84*** (0.59; p=0.002) | 1.42** (0.68; p=0.037) | 0.72 (0.67; p=0.280) | 0.78 (0.60; p=0.190) |
| EU x spouse aged 56-62 | -0.29 (0.59; p=0.631) | -0.28 (0.60; p=0.639) | -0.68 (0.61; p=0.260) | 0.01 (0.58; p=0.980) | -0.41 (0.73; p=0.578) | -0.92 (0.66; p=0.164) | -0.31 (0.60; p=0.608) |
| Difference: 56-62 minus 26-35 | -2.11*** (0.81; p=0.009) | -2.11*** (0.81; p=0.010) | -1.67** (0.83; p=0.045) | -1.71** (0.78; p=0.029) | -2.44*** (0.93; p=0.008) | -2.19** (0.87; p=0.012) | -1.21 (0.81; p=0.138) |
| Wald test: equal across the four ages | chi2(3) = 14.2; p=0.003 | chi2(3) = 13.9; p=0.003 | chi2(3) = 12.2; p=0.007 | chi2(3) = 11.1; p=0.011 | chi2(3) = 8.4; p=0.038 | chi2(3) = 10.4; p=0.015 | chi2(3) = 10.0; p=0.019 |
| Couples | sex-neutral | sex-neutral | sex-neutral | sex-neutral | wife = spouse | wife = spouse | sex-neutral |
| Years | 1994-Feb 2020 | 1994-Feb 2020 | 1994-Feb 2020 | 1994-2023 | 1994-Feb 2020 | 1994-2023 | 1994-2023 |
| EHS correction | yes | no | yes | yes | yes | no | no |
| Primary earner's EU | all | all | job loser | all | all | job loser | job loser |
| Fixed effects | none (age-group FE in the age rows) | none (age-group FE in the age rows) | none (age-group FE in the age rows) | none (age-group FE in the age rows) | none (age-group FE in the age rows) | none (age-group FE in the age rows) | none (age-group FE in the age rows) |
| N (EE + EU) / clusters | 1,082,535 / 342,629 | 1,080,724 / 345,177 | 1,080,997 / 342,047 | 1,189,575 / 375,597 | 887,182 / 276,274 | 970,690 / 303,463 | 1,185,975 / 377,692 |
| Mean outcome under EE, all ages (%) | 6.06 | 6.07 | 6.06 | 6.07 | 5.79 | 5.80 | 6.08 |

### 1d. AWE regressions, outcome: spouse N -> U, same month (pp)

One weighted LPM per column on the EE + EU sample; rows 'EU x spouse aged ...' come from one fully interacted regression per column (age-group FE); 'EU, all ages' from a separate regression.

| | (1) spouse N -> U | (2) spouse N -> U | (3) spouse N -> U | (4) spouse N -> U | (5) spouse N -> U | (6) spouse N -> U | (7) spouse N -> U |
|---|---|---|---|---|---|---|---|
| Primary earner EU (vs EE), all ages | 3.72*** (0.26; p<0.001) | 5.74*** (0.32; p<0.001) | 3.31*** (0.27; p<0.001) | 3.65*** (0.24; p<0.001) | 3.91*** (0.28; p<0.001) | 5.37*** (0.34; p<0.001) | 5.04*** (0.31; p<0.001) |
| EU x spouse aged 26-35 | 4.53*** (0.50; p<0.001) | 7.35*** (0.63; p<0.001) | 4.31*** (0.54; p<0.001) | 4.55*** (0.48; p<0.001) | 4.58*** (0.51; p<0.001) | 6.76*** (0.64; p<0.001) | 6.91*** (0.64; p<0.001) |
| EU x spouse aged 36-45 | 4.42*** (0.50; p<0.001) | 6.31*** (0.60; p<0.001) | 3.69*** (0.51; p<0.001) | 4.24*** (0.47; p<0.001) | 4.33*** (0.53; p<0.001) | 5.49*** (0.61; p<0.001) | 5.38*** (0.58; p<0.001) |
| EU x spouse aged 46-55 | 2.98*** (0.47; p<0.001) | 4.71*** (0.59; p<0.001) | 2.77*** (0.50; p<0.001) | 2.88*** (0.44; p<0.001) | 3.24*** (0.54; p<0.001) | 4.60*** (0.66; p<0.001) | 4.13*** (0.58; p<0.001) |
| EU x spouse aged 56-62 | 1.51*** (0.45; p<0.001) | 2.38*** (0.59; p<0.001) | 1.03** (0.45; p=0.022) | 1.73*** (0.46; p<0.001) | 1.67*** (0.57; p=0.003) | 2.29*** (0.68; p<0.001) | 1.93*** (0.56; p<0.001) |
| Difference: 56-62 minus 26-35 | -3.02*** (0.68; p<0.001) | -4.97*** (0.86; p<0.001) | -3.28*** (0.70; p<0.001) | -2.82*** (0.66; p<0.001) | -2.91*** (0.77; p<0.001) | -4.47*** (0.94; p<0.001) | -4.98*** (0.85; p<0.001) |
| Wald test: equal across the four ages | chi2(3) = 27.0; p<0.001 | chi2(3) = 38.9; p<0.001 | chi2(3) = 26.5; p<0.001 | chi2(3) = 23.4; p<0.001 | chi2(3) = 17.4; p<0.001 | chi2(3) = 24.2; p<0.001 | chi2(3) = 37.8; p<0.001 |
| Couples | sex-neutral | sex-neutral | sex-neutral | sex-neutral | wife = spouse | wife = spouse | sex-neutral |
| Years | 1994-Feb 2020 | 1994-Feb 2020 | 1994-Feb 2020 | 1994-2023 | 1994-Feb 2020 | 1994-2023 | 1994-2023 |
| EHS correction | yes | no | yes | yes | yes | no | no |
| Primary earner's EU | all | all | job loser | all | all | job loser | job loser |
| Fixed effects | none (age-group FE in the age rows) | none (age-group FE in the age rows) | none (age-group FE in the age rows) | none (age-group FE in the age rows) | none (age-group FE in the age rows) | none (age-group FE in the age rows) | none (age-group FE in the age rows) |
| N (EE + EU) / clusters | 1,082,535 / 342,629 | 1,080,724 / 345,177 | 1,080,997 / 342,047 | 1,189,575 / 375,597 | 887,182 / 276,274 | 970,690 / 303,463 | 1,185,975 / 377,692 |
| Mean outcome under EE, all ages (%) | 1.61 | 2.56 | 1.61 | 1.60 | 1.38 | 2.14 | 2.53 |

Husbands as the non-participating spouse (wife employed; sex-neutral sample's other half): AWE 5.87*** (0.99; p<0.001), N 195,353; by his age 26-35 2.25 (3.14; p=0.473); 36-45 10.42*** (2.46; p<0.001); 46-55 5.85*** (1.68; p<0.001); 56-62 1.24 (1.24; p=0.315). Unweighted main variant: AWE 5.21*** (0.34; p<0.001); by age 26-35 5.97*** (0.63; p<0.001); 36-45 6.75*** (0.68; p<0.001); 46-55 4.50*** (0.66; p<0.001); 56-62 1.17* (0.66; p=0.075).

### 1e. BGN Eq. (1): leads and lags (main variant; unweighted LPM; pp)

Outcome: the non-participating spouse (N at t-1) enters the labor force at t. Column j: the primary earner moves E -> U between t+j-1 and t+j (j < 0: he lost the job before her move; j > 0: he loses it after), against primary earners employed in every month of the window. One regression per cell. Spec A: BGN's controls (state FE; year and calendar-month dummies; primary earner's sex and race; education of both; number of own children; no state unemployment rate). Spec B: state x year-month FE + the same individual controls. BGN row: their Fig. 1 / Fig. 2 (56-65 for the oldest).

| | (1) spouse enters LF at t; j=-2 (lost two months ago) | (2) spouse enters LF at t; j=-1 (lost last month) | (3) spouse enters LF at t; j=+0 (this month) | (4) spouse enters LF at t; j=+1 (loses next month) | (5) spouse enters LF at t; j=+2 (loses in two months) |
|---|---|---|---|---|---|
| **All EN couples** | | | | | |
| Primary earner E->U at t+j, spec A | 3.77*** (0.60; p<0.001) | 3.15*** (0.39; p<0.001) | 5.37*** (0.34; p<0.001) | 1.69*** (0.41; p<0.001) | 1.07* (0.62; p=0.085) |
| N / N treated | 309,535 / 2,864 | 670,749 / 6,183 | 1,082,535 / 10,026 | 660,206 / 4,990 | 299,788 / 2,037 |
| Primary earner E->U at t+j, spec B | 3.66*** (0.59; p<0.001) | 3.10*** (0.39; p<0.001) | 5.37*** (0.34; p<0.001) | 1.69*** (0.41; p<0.001) | 1.03* (0.62; p=0.096) |
| BGN (Fig. 1 / 2) | 3.30 | 2.60 | 5.80 | 2.00 | 1.70 |
| **Spouse aged 26-35** | | | | | |
| Primary earner E->U at t+j, spec A | 5.07*** (1.17; p<0.001) | 4.00*** (0.76; p<0.001) | 5.97*** (0.63; p<0.001) | 0.85 (0.73; p=0.243) | 0.83 (1.12; p=0.460) |
| N / N treated | 77,547 / 837 | 170,624 / 1,859 | 279,124 / 3,114 | 168,975 / 1,535 | 76,099 / 622 |
| Primary earner E->U at t+j, spec B | 3.77*** (1.16; p=0.001) | 3.98*** (0.75; p<0.001) | 5.88*** (0.62; p<0.001) | 0.85 (0.72; p=0.238) | 0.50 (1.12; p=0.655) |
| BGN (Fig. 1 / 2) | 3.70 | 3.00 | 7.30 | 1.60 | 2.00 |
| **Spouse aged 36-45** | | | | | |
| Primary earner E->U at t+j, spec A | 3.40*** (1.14; p=0.003) | 3.08*** (0.77; p<0.001) | 6.47*** (0.67; p<0.001) | 0.70 (0.77; p=0.365) | 0.14 (1.16; p=0.906) |
| N / N treated | 92,305 / 840 | 199,957 / 1,774 | 321,943 / 2,932 | 197,247 / 1,425 | 89,863 / 610 |
| Primary earner E->U at t+j, spec B | 3.12*** (1.13; p=0.006) | 3.08*** (0.77; p<0.001) | 6.45*** (0.66; p<0.001) | 0.70 (0.77; p=0.363) | 0.54 (1.15; p=0.640) |
| **Spouse aged 46-55** | | | | | |
| Primary earner E->U at t+j, spec A | 2.92*** (1.13; p=0.010) | 2.91*** (0.76; p<0.001) | 4.72*** (0.66; p<0.001) | 2.60*** (0.85; p=0.002) | 3.27** (1.42; p=0.021) |
| N / N treated | 85,129 / 744 | 183,186 / 1,602 | 293,958 / 2,493 | 180,453 / 1,247 | 82,536 / 485 |
| Primary earner E->U at t+j, spec B | 2.75** (1.11; p=0.013) | 2.78*** (0.75; p<0.001) | 4.62*** (0.66; p<0.001) | 2.48*** (0.84; p=0.003) | 2.35* (1.42; p=0.098) |
| **Spouse aged 56-62** | | | | | |
| Primary earner E->U at t+j, spec A | 1.71 (1.19; p=0.152) | 0.39 (0.74; p=0.601) | 1.35** (0.65; p=0.038) | 2.84*** (0.97; p=0.004) | -1.22 (1.12; p=0.276) |
| N / N treated | 54,554 / 443 | 116,982 / 948 | 187,510 / 1,487 | 113,531 / 783 | 51,290 / 320 |
| Primary earner E->U at t+j, spec B | 1.54 (1.27; p=0.225) | 0.93 (0.73; p=0.205) | 1.70*** (0.65; p=0.009) | 2.96*** (0.93; p=0.001) | -0.23 (1.20; p=0.849) |
| BGN (Fig. 1 / 2) | 2.60 | -0.19 | 1.50 | 2.40 | 0.31 |
| Fixed effects | A: state + year + month; B: state x year-month | A: state + year + month; B: state x year-month | A: state + year + month; B: state x year-month | A: state + year + month; B: state x year-month | A: state + year + month; B: state x year-month |

## 2. Paper A's joint job loss by the same age groups

30's sample: both spouses employed at t; H = 1 if the husband becomes a job loser at t+1 (unemployed, reason job loser on layoff / other job loser / temporary job ended), H = 0 if he stays employed. Outcome: the wife becomes a job loser at t+1. One LPM with state x year-month FE per cell. Columns: (1) all; (2) excluding temporary layoffs as in 37 (his loss other than on layoff, wives on layoff at t+1 dropped, outcome = her loss other than on layoff); (3) (1) excluding 2020-21; (4) (1) in BGN's window (1994-Feb 2020).

| | (1) wife job loser at t+1 | (2) wife job loser not on layoff (his loss not on layoff) | (3) wife job loser at t+1, excl. 2020-21 | (4) wife job loser at t+1, 1994-Feb 2020 |
|---|---|---|---|---|
| **All couples** | | | | |
| Husband becomes job loser (t+1), pp | 4.05*** (0.15; p<0.001) | 2.60*** (0.16; p<0.001) | 3.56*** (0.15; p<0.001) | 3.48*** (0.15; p<0.001) |
| % wife job loser: H = 0 / H = 1 (weighted) | 0.54 / 5.49 (ratio 10.1) | 0.23 / 3.30 (ratio 14.5) | 0.51 / 4.50 (ratio 8.8) | 0.52 / 4.36 (ratio 8.3) |
| N / N(H = 1) / joint events | 3,021,199 / 20,618 / 990 | 3,001,702 / 10,459 / 299 | 2,897,430 / 19,440 / 800 | 2,760,815 / 18,881 / 763 |
| **Husband aged 20-25** | | | | |
| Husband becomes job loser (t+1), pp | 2.93*** (0.64; p<0.001) | 3.37*** (0.85; p<0.001) | 2.75*** (0.62; p<0.001) | 2.69*** (0.63; p<0.001) |
| % wife job loser: H = 0 / H = 1 (weighted) | 0.74 / 4.32 (ratio 5.8) | 0.41 / 4.75 (ratio 11.6) | 0.71 / 4.13 (ratio 5.8) | 0.71 / 4.12 (ratio 5.8) |
| N / N(H = 1) / joint events | 72,269 / 773 / 29 | 71,719 / 455 / 18 | 70,176 / 749 / 26 | 68,039 / 728 / 25 |
| **Husband aged 26-35** | | | | |
| Husband becomes job loser (t+1), pp | 3.35*** (0.28; p<0.001) | 2.99*** (0.36; p<0.001) | 2.91*** (0.28; p<0.001) | 2.75*** (0.27; p<0.001) |
| % wife job loser: H = 0 / H = 1 (weighted) | 0.53 / 4.95 (ratio 9.4) | 0.24 / 4.18 (ratio 17.1) | 0.50 / 4.05 (ratio 8.1) | 0.51 / 3.78 (ratio 7.4) |
| N / N(H = 1) / joint events | 614,695 / 4,585 / 187 | 610,747 / 2,395 / 79 | 591,274 / 4,358 / 151 | 565,493 / 4,260 / 141 |
| **Husband aged 36-45** | | | | |
| Husband becomes job loser (t+1), pp | 3.99*** (0.27; p<0.001) | 2.31*** (0.27; p<0.001) | 3.61*** (0.26; p<0.001) | 3.54*** (0.26; p<0.001) |
| % wife job loser: H = 0 / H = 1 (weighted) | 0.54 / 5.28 (ratio 9.8) | 0.22 / 2.62 (ratio 11.7) | 0.52 / 4.50 (ratio 8.7) | 0.53 / 4.35 (ratio 8.2) |
| N / N(H = 1) / joint events | 952,561 / 6,311 / 295 | 946,487 / 3,207 / 82 | 914,003 / 5,975 / 249 | 871,013 / 5,797 / 238 |
| **Husband aged 46-55** | | | | |
| Husband becomes job loser (t+1), pp | 4.23*** (0.28; p<0.001) | 2.35*** (0.29; p<0.001) | 3.67*** (0.27; p<0.001) | 3.65*** (0.27; p<0.001) |
| % wife job loser: H = 0 / H = 1 (weighted) | 0.54 / 5.72 (ratio 10.7) | 0.22 / 3.04 (ratio 14.1) | 0.51 / 4.50 (ratio 8.9) | 0.51 / 4.45 (ratio 8.7) |
| N / N(H = 1) / joint events | 954,569 / 6,172 / 308 | 948,571 / 3,115 / 81 | 916,631 / 5,803 / 244 | 874,265 / 5,647 / 236 |
| **Husband aged 56-62** | | | | |
| Husband becomes job loser (t+1), pp | 5.24*** (0.43; p<0.001) | 2.80*** (0.46; p<0.001) | 4.55*** (0.42; p<0.001) | 4.47*** (0.43; p<0.001) |
| % wife job loser: H = 0 / H = 1 (weighted) | 0.55 / 6.76 (ratio 12.3) | 0.20 / 3.37 (ratio 16.9) | 0.50 / 5.47 (ratio 10.9) | 0.51 / 5.35 (ratio 10.5) |
| N / N(H = 1) / joint events | 427,105 / 2,777 / 171 | 424,178 / 1,287 / 39 | 405,346 / 2,555 / 130 | 382,005 / 2,449 / 123 |
| **Wife aged 20-25** | | | | |
| Husband becomes job loser (t+1), pp | 3.26*** (0.53; p<0.001) | 3.37*** (0.67; p<0.001) | 3.07*** (0.53; p<0.001) | 3.05*** (0.53; p<0.001) |
| % wife job loser: H = 0 / H = 1 (weighted) | 0.70 / 4.57 (ratio 6.5) | 0.39 / 4.38 (ratio 11.2) | 0.68 / 4.06 (ratio 6.0) | 0.67 / 4.05 (ratio 6.0) |
| N / N(H = 1) / joint events | 122,614 / 1,206 / 51 | 121,731 / 699 / 28 | 119,447 / 1,160 / 44 | 116,183 / 1,138 / 43 |
| **Wife aged 26-35** | | | | |
| Husband becomes job loser (t+1), pp | 3.63*** (0.27; p<0.001) | 2.75*** (0.32; p<0.001) | 3.28*** (0.27; p<0.001) | 3.10*** (0.27; p<0.001) |
| % wife job loser: H = 0 / H = 1 (weighted) | 0.54 / 5.24 (ratio 9.7) | 0.24 / 3.75 (ratio 15.9) | 0.51 / 4.57 (ratio 8.9) | 0.53 / 4.25 (ratio 8.1) |
| N / N(H = 1) / joint events | 726,511 / 5,329 / 232 | 721,761 / 2,760 / 84 | 697,709 / 5,073 / 195 | 666,443 / 4,929 / 181 |
| **Wife aged 36-45** | | | | |
| Husband becomes job loser (t+1), pp | 4.08*** (0.26; p<0.001) | 2.44*** (0.27; p<0.001) | 3.59*** (0.25; p<0.001) | 3.51*** (0.26; p<0.001) |
| % wife job loser: H = 0 / H = 1 (weighted) | 0.54 / 5.27 (ratio 9.8) | 0.22 / 2.72 (ratio 12.2) | 0.51 / 4.23 (ratio 8.3) | 0.52 / 4.09 (ratio 7.8) |
| N / N(H = 1) / joint events | 1,005,220 / 6,677 / 320 | 998,818 / 3,355 / 90 | 965,137 / 6,304 / 262 | 920,145 / 6,125 / 250 |
| **Wife aged 46-55** | | | | |
| Husband becomes job loser (t+1), pp | 4.24*** (0.29; p<0.001) | 2.36*** (0.30; p<0.001) | 3.68*** (0.28; p<0.001) | 3.66*** (0.28; p<0.001) |
| % wife job loser: H = 0 / H = 1 (weighted) | 0.52 / 5.84 (ratio 11.3) | 0.21 / 3.18 (ratio 15.1) | 0.48 / 4.60 (ratio 9.5) | 0.49 / 4.58 (ratio 9.3) |
| N / N(H = 1) / joint events | 895,050 / 5,691 / 284 | 889,558 / 2,859 / 74 | 858,683 / 5,346 / 225 | 818,103 / 5,202 / 218 |
| **Wife aged 56-62** | | | | |
| Husband becomes job loser (t+1), pp | 5.00*** (0.54; p<0.001) | 2.76*** (0.59; p<0.001) | 4.25*** (0.52; p<0.001) | 4.25*** (0.53; p<0.001) |
| % wife job loser: H = 0 / H = 1 (weighted) | 0.59 / 6.71 (ratio 11.4) | 0.19 / 3.50 (ratio 18.5) | 0.53 / 5.45 (ratio 10.3) | 0.54 / 5.45 (ratio 10.1) |
| N / N(H = 1) / joint events | 271,804 / 1,715 / 103 | 269,834 / 786 / 23 | 256,454 / 1,557 / 74 | 239,941 / 1,487 / 71 |
| Fixed effects | state x year-month | state x year-month | state x year-month | state x year-month |
| Clusters | household | household | household | household |

### 2b. Does the joint-loss excess change with age? Pooled H x age-group regressions (pp)

One LPM per column: wife's outcome on H x age-group dummies (26-35 ... oldest; ages 20-25 dropped) with age-group dummies and state x year-month FE; 'H x (age - 40) / 10' from a separate regression with H, age, H x age (linear in the age of the spouse named in the header).

| | (1) wife job loser at t+1; by husband's age | (2) wife job loser not on layoff (his loss not on layoff); by husband's age | (3) wife job loser at t+1; by wife's age | (4) wife job loser not on layoff (his loss not on layoff); by wife's age |
|---|---|---|---|---|
| H x 26-35 | 3.39*** (0.29; p<0.001) | 3.02*** (0.37; p<0.001) | 3.65*** (0.28; p<0.001) | 2.77*** (0.33; p<0.001) |
| H x 36-45 | 3.95*** (0.27; p<0.001) | 2.30*** (0.28; p<0.001) | 4.07*** (0.26; p<0.001) | 2.43*** (0.28; p<0.001) |
| H x 46-55 | 4.22*** (0.28; p<0.001) | 2.36*** (0.29; p<0.001) | 4.23*** (0.29; p<0.001) | 2.35*** (0.30; p<0.001) |
| H x 56-62 | 5.32*** (0.45; p<0.001) | 2.81*** (0.48; p<0.001) | 5.10*** (0.56; p<0.001) | 2.72*** (0.60; p<0.001) |
| Difference: 56-62 minus 26-35 | 1.93*** (0.54; p<0.001) | -0.21 (0.60; p=0.726) | 1.45** (0.63; p=0.021) | -0.05 (0.68; p=0.942) |
| Wald test: equal across the four ages | chi2(3) = 13.6; p=0.003 | chi2(3) = 3.1; p=0.376 | chi2(3) = 5.9; p=0.115 | chi2(3) = 1.1; p=0.771 |
| H x (age - 40) / 10 (separate regression) | 0.54*** (0.16; p<0.001) | -0.15 (0.18; p=0.402) | 0.50*** (0.17; p=0.004) | 0.01 (0.19; p=0.961) |
| Fixed effects | state x year-month + age group | state x year-month + age group | state x year-month + age group | state x year-month + age group |
| N | 2,948,930 | 2,929,983 | 2,898,585 | 2,879,971 |

### 2c. Joint job-loss rate and couples' joint labor-market states by age

Joint rate: among couples both employed at t and both observed at t+1, % of couple-months in which both become job losers at t+1, and its ratio to the product of the two marginal rates (independence). States: all couple-months with both statuses valid, weighted; first letter = husband, second = wife; EU / UN pool both orders.

| | % both job losers at t+1 (EE couples) | Ratio to independence | % husband job loser | % wife job loser | % EE | % EN (wife N) | % NE (husband N) | % EU (either) | % UU | % UN (either) | % NN |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **By husband's age** | | | | | | | | | | | |
| Husband 20-62 | 0.0377 | 9.4 | 0.69 | 0.58 | 62.34 | 23.54 | 4.91 | 3.93 | 0.29 | 0.99 | 4.00 |
| Husband 20-25 | 0.0473 | 5.5 | 1.09 | 0.79 | 56.79 | 27.75 | 3.55 | 6.27 | 0.66 | 1.92 | 3.07 |
| Husband 26-35 | 0.0367 | 8.7 | 0.74 | 0.57 | 63.20 | 26.53 | 2.59 | 4.31 | 0.33 | 1.07 | 1.96 |
| Husband 36-45 | 0.0355 | 9.2 | 0.67 | 0.58 | 65.45 | 24.40 | 3.07 | 3.93 | 0.29 | 0.86 | 2.00 |
| Husband 46-55 | 0.0376 | 10.0 | 0.66 | 0.57 | 65.22 | 21.02 | 5.15 | 3.86 | 0.27 | 0.90 | 3.58 |
| Husband 56-62 | 0.0432 | 11.4 | 0.64 | 0.59 | 51.56 | 21.97 | 10.90 | 3.16 | 0.23 | 1.14 | 11.04 |
| **By wife's age** | | | | | | | | | | | |
| Wife 20-62 | 0.0377 | 9.4 | 0.69 | 0.58 | 62.34 | 23.54 | 4.91 | 3.93 | 0.29 | 0.99 | 4.00 |
| Wife 20-25 | 0.0467 | 6.1 | 1.02 | 0.75 | 55.01 | 31.06 | 2.94 | 5.69 | 0.60 | 1.88 | 2.81 |
| Wife 26-35 | 0.0380 | 9.1 | 0.72 | 0.58 | 63.02 | 26.64 | 2.76 | 4.22 | 0.33 | 1.06 | 1.97 |
| Wife 36-45 | 0.0356 | 9.2 | 0.68 | 0.57 | 66.26 | 22.73 | 3.73 | 3.93 | 0.27 | 0.83 | 2.25 |
| Wife 46-55 | 0.0374 | 10.5 | 0.64 | 0.56 | 64.13 | 20.02 | 6.47 | 3.74 | 0.25 | 0.88 | 4.50 |
| Wife 56-62 | 0.0418 | 10.7 | 0.62 | 0.63 | 48.83 | 24.34 | 9.84 | 2.97 | 0.21 | 1.19 | 12.61 |

## 3. Summary

- **AWE, overall:** 5.64*** (0.39; p<0.001) pp in BGN's window and definitions (BGN 5.55).
- **AWE by the spouse's age (main variant):** 26-35 6.35*** (0.72; p<0.001); 36-45 7.17*** (0.77; p<0.001); 46-55 5.02*** (0.77; p<0.001); 56-62 1.22* (0.74; p=0.097) (BGN 7.12 / 6.83 / 4.57 / 1.40). Oldest minus youngest -5.13*** (1.03; p<0.001); equality across ages p=3.01e-08.
- **Joint job loss by the wife's age (excess, state x month FE):** 26-35 3.63*** (0.27; p<0.001) (ratio 9.7); 36-45 4.08*** (0.26; p<0.001) (ratio 9.8); 46-55 4.24*** (0.29; p<0.001) (ratio 11.3); 56-62 5.00*** (0.54; p<0.001) (ratio 11.4). Oldest minus 26-35 1.45** (0.63; p=0.021); equality p=0.115.
- **By the husband's age:** 26-35 3.35*** (0.28; p<0.001) (ratio 9.4); 36-45 3.99*** (0.27; p<0.001) (ratio 9.8); 46-55 4.23*** (0.28; p<0.001) (ratio 10.7); 56-62 5.24*** (0.43; p<0.001) (ratio 12.3). Oldest minus 26-35 1.93*** (0.54; p<0.001); equality p=0.00348.
- **Excluding temporary layoffs** (his loss not on layoff, her loss not on layoff): oldest minus 26-35 by husband's age -0.21 (0.60; p=0.726), equality p=0.376; by wife's age -0.05 (0.68; p=0.942), equality p=0.771. The AWE falls with age in every variant; the joint-loss excess does not fall with age (it rises for all job losses, through losses on layoff, and is flat for losses other than on layoff).
