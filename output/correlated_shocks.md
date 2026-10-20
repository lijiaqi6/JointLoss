# Correlated shocks: can wives respond to the husband's job loss, or are they hit by the same shock?

Built by `23.CorrelatedShocks.py` (2026-10-17; variable lists in its docstring and in section 0). Unweighted PSID SRC + SEO, married (wife / partner present) male heads, Black and White (head's race). S.e. clustered by 1968 family (fam68); *** p<0.01, ** p<0.05, * p<0.1. Displacement = the husband's job ended because the company folded / moved / went out of business (closure) or he was laid off / fired (19.FatherDisplacement.py). All comparisons are descriptive or difference-in-differences comparisons with the usual assumptions; the moderators (same sector, sector growth, state slack) are not randomly assigned, so their interactions describe heterogeneity, not causal effects of demand.

## 0. Variables found by label

| Wave | Head occupation | Wife occupation | Head industry (1968-75; 18 from 1976) | Wife industry (1968-75) | Wife's status |
|---|---|---|---|---|---|
| 1968 | V197_A 'OCCUPATION OF HEAD         68' | V243_A 'OCCUPATION OF WIFE         68' | V197_B 'INDUSTRY   OF HEAD         68' | V243_B 'INDUSTRY   OF WIFE         68' |  |
| 1969 | V640_A 'OCCUPATION OF HEAD         69' | V609_A 'OCCUPATION OF WIFE         69' | V640_B 'INDUSTRY   OF HEAD         69' | V609_B 'INDUSTRY   OF WIFE         69' |  |
| 1970 | V1279_A 'OCCUPATION OF HEAD         70' | V1367_A 'OCCUPATION OF WIFE         70' | V1279_B 'INDUSTRY   OF HEAD         70' | V1367_B 'INDUSTRY   OF WIFE         70' |  |
| 1971 | V1984_A 'OCCUPATION OF HEAD         71' | V2074_A 'OCCUPATION OF WIFE         71' | V1985_A 'INDUSTRY   OF HEAD         71' | V2075_A 'INDUSTRY   OF WIFE         71' |  |
| 1972 | V2582_A 'OCCUPATION OF HEAD         72' | V2672_A 'OCCUPATION OF WIFE         72' | V2583_A 'INDUSTRY   OF HEAD         72' | V2673_A 'INDUSTRY   OF WIFE         72' |  |
| 1973 | V3115_A 'OCCUPATION OF HEAD         73' | V3183_A 'OCCUPATION OF WIFE         73' | V3116_A 'INDUSTRY   OF HEAD         73' | V3184_A 'INDUSTRY   OF WIFE         73' |  |
| 1974 | V3530_A 'OCCUPATION OF HEAD         74' | V3601_A 'OCCUPATION OF WIFE         74' | V3531_A 'INDUSTRY   OF HEAD         74' | V3602_A 'INDUSTRY   OF WIFE         74' |  |
| 1975 | V3968_A 'OCCUPATION OF HEAD         75' | V4055_A 'OCCUPATION OF WIFE         75' | V3969_A 'INDUSTRY   OF HEAD         75' | V4056_A 'INDUSTRY   OF WIFE         75' |  |
| 1976 | V4459_A 'OCCUPATION OF HEAD         76' | V4605_A 'OCCUPATION OF WIFE         76' |  |  | V4841 'EMPLOYMENT STATUS-WF  D1' |
| 1977 | V5374_A 'OCCUPATION OF HEAD         77' | V5507_A 'OCCUPATION OF WIFE         77' |  |  |  |
| 1978 | V5873_A 'OCCUPATION OF HEAD         78' | V6039_A 'OCCUPATION OF WIFE         78' |  |  |  |
| 1979 | V6497_A 'OCCUPATION OF HEAD         79' | V6596_A 'OCCUPATION OF WIFE         79' |  |  | V6591 'F2 EMP STATUS WIFE' |
| 1980 | V7100_A 'OCCUPATION OF HEAD         80' | V7198_A 'OCCUPATION OF WIFE         80' |  |  | V7193 'F2 EMP STATUS WIFE' |
| 1981 | V7712 'C7-8 MAIN OCC:3DIG(H-E)' | V7885 'F8-9 OCCUPATION  (WF-E)' |  |  | V7879 'F2 EMPLOYMENT STAT-WF' |
| 1982 | V8380 'C7-8 MAIN OCC:3DIG(H-E)' | V8544 'F8/9 OCCUPATION  (WF-E)' |  |  | V8538 'F2 EMPLOYMENT STAT-WF' |
| 1983 | V9011 'C7-8 MAIN OCC:3DIG(H-E)' | V9194 'F8-9 OCCUPATION  (WF-E)' |  |  | V9188 'F2 EMPLOYMENT STAT-WF' |
| 1984 | V10460 'C8-9 MAIN OCC:3DIGT(H-E)' | V10678 'F9/10 OCCUPATION (WF-E)' |  |  | V10671 'F2 EMPLOYMENT STAT-WF' |
| 1985 | V11651 'B15-16 MAIN OCC:3DIG H-E' | V12014 'J15-16 MAIN OCC:3DIG W-E' |  |  | V12000 'J1F EMPLMT STATUS-WIFE' |
| 1986 | V13054 'B9-10 MAIN OCC:3 DIG H-E' | V13233 'D9-10 MAIN OCC:3 DIG W-E' |  |  | V13225 'D1B EMPLMT STATUS-WIFE' |
| 1987 | V14154 'B9-10 MAIN OCC:3 DIG H-E' | V14329 'D9-10 MAIN OCC:3 DIG W-E' |  |  | V14321 'D1B EMPLMT STATUS-WIFE' |
| 1988 | V15162 'B9-10 MAIN OCC:3 DIG H-E' | V15464 'D9-10 MAIN OCC:3 DIG W-E' |  |  | V15456 'D1A EMPLOYMENT STATUS-WF' |
| 1989 | V16663 'B9-10 MAIN OCC:3 DIG H-E' | V16982 'D9-10 MAIN OCC:3 DIG W-E' |  |  | V16974 'D1A EMPLOYMENT STATUS-WF' |
| 1990 | V18101 'B9-10 MAIN OCC:3 DIG H-E' | V18403 'D9-10 MAIN OCC:3 DIG W-E' |  |  | V18395 'D1A EMPLOYMENT STATUS-WF' |
| 1991 | V19401 'B9-10 MAIN OCC:3 DIG H-E' | V19703 'D9-10 MAIN OCC:3 DIG W-E' |  |  | V19695 'D1A EMPLOYMENT STATUS-WF' |
| 1992 | V20701 'B9-10 MAIN OCC:3 DIG H-E' | V21003 'D9-10 MAIN OCC:3 DIG W-E' |  |  | V20995 'D1A EMPLOYMENT STATUS-WF' |
| 1993 | V22456 'B9-9A MAIN OCCUPATION: 3 DIGIT (HD-E)' | V22809 'D9-9A MAIN OCCUPATION:3 DIGIT (WF-E)' |  |  | V22801 'D1A WF 1993 EMPLOYMENT STATUS' |
| 1994 | ER4017 'B9-9A MAIN OCCUPATION: 3 DIGIT (HD-E)' | ER4048 'D9-9A MAIN OCCUPATION:3 DIGIT (WF-E)' |  |  | ER2562 'D1A EMPLOYMENT STATUS-WF' |
| 1995 | ER6857 'B9-9A MAIN OCCUPATION: 3 DIGIT (HD-E)' | ER6888 'D9-9A MAIN OCCUPATION:3 DIGIT (WF-E)' |  |  | ER5561 'D1A EMPLOYMENT STATUS-WF' |
| 1996 | ER9108 'B9-9A MAIN OCCUPATION: 3 DIGIT (HD-E)' | ER9139 'D9-9A MAIN OCCUPATION:3 DIGIT (WF-E)' |  |  | ER7657 'D1A EMPLOYMENT STATUS-WF' |
| 1997 | ER12085 'B9-9A MAIN OCCUPATION: 3 DIGIT (HD-E)' | ER12116 'D9-9A MAIN OCCUPATION:3 DIGIT (WF-E)' |  |  | ER10563 'D1A 1ST MENTION' |
| 1999 | ER13215 'B9-9A MAIN OCCUPATION: 3 DIGIT (HD-E)' | ER13727 'D9-9A MAIN OCCUPATION:3 DIGIT (WF-E)' |  |  | ER13717 'D1 1ST MENTION' |
| 2001 | ER17226 'B9-9A MAIN OCCUPATION: 3 DIGIT (HD-E)' | ER17796 'D9-9A MAIN OCCUPATION:3 DIGIT (WF-E)' |  |  | ER17786 'D1 1ST MENTION' |
| 2003 | ER21145 'BC20 MAIN OCC FOR JOB 1: 2000 CODE (HD)' | ER21395 'DE20 MAIN OCC FOR JOB 1: 2000 CODE (WF)' |  |  | ER21373 'DE1 EMPLOYMENT STATUS-1ST MENTION' |
| 2005 | ER25127 'BC20 MAIN OCC FOR JOB 1: 2000 CODE (HD)' | ER25385 'DE20 MAIN OCC FOR JOB 1: 2000 CODE (WF)' |  |  | ER25362 'DE1 EMPLOYMENT STATUS-1ST MENTION' |
| 2007 | ER36132 'BC20 MAIN OCC FOR JOB 1: 2000 CODE (HD)' | ER36390 'DE20 MAIN OCC FOR JOB 1: 2000 CODE (WF)' |  |  | ER36367 'DE1 EMPLOYMENT STATUS-1ST MENTION' |
| 2009 | ER42167 'BC20 MAIN OCC FOR JOB 1: 2000 CODE (HD)' | ER42419 'DE20 MAIN OCC FOR JOB 1: 2000 CODE (WF)' |  |  | ER42392 'DE1 EMPLOYMENT STATUS-1ST MENTION' |
| 2011 | ER47479 'BC20 MAIN OCC FOR JOB 1: 2000 CODE (HD)' | ER47736 'DE20 MAIN OCC FOR JOB 1: 2000 CODE (WF)' |  |  | ER47705 'DE1 EMPLOYMENT STATUS-1ST MENTION' |
| 2013 | ER53179 'BC20 MAIN OCC FOR JOB 1: 2000 CODE (HD)' | ER53442 'DE20 MAIN OCC FOR JOB 1: 2000 CODE (WF)' |  |  | ER53411 'DE1 EMPLOYMENT STATUS-1ST MENTION' |
| 2015 | ER60194 'BC20 MAIN OCC FOR JOB 1: 2000 CODE (HD)' | ER60457 'DE20 MAIN OCC FOR JOB 1: 2000 CODE (SP)' |  |  | ER60426 'DE1 EMPLOYMENT STATUS-1ST MENTION' |
| 2017 | ER66195 'BC20 MAIN OCC FOR JOB 1: 2010 CODE (RP)' | ER66470 'DE20 MAIN OCC FOR JOB 1: 2010 CODE (SP)' |  |  | ER66439 'DE1 EMPLOYMENT STATUS-1ST MENTION' |
| 2019 | ER72195 'BC20 MAIN OCC FOR JOB 1: 2010 CODE (RP)' | ER72472 'DE20 MAIN OCC FOR JOB 1: 2010 CODE (SP)' |  |  | ER72441 'DE1 EMPLOYMENT STATUS-1ST MENTION' |
| 2021 | ER78198 'BC20 MAIN OCC FOR JOB 1: 2010 CODE (RP)' | ER78512 'DE20 MAIN OCC FOR JOB 1: 2010 CODE (SP)' |  |  | ER78481 'DE1 EMPLOYMENT STATUS-1ST MENTION' |
| 2023 | ER82181 'BC20 MAIN OCC FOR JOB 1: 2010 CODE (RP)' | ER82500 'DE20 MAIN OCC FOR JOB 1: 2010 CODE (SP)' |  |  | ER82469 'DE1 EMPLOYMENT STATUS-1ST MENTION' |

Wife's reason-for-job-end reports linked to a wife (1984-2023 waves): 24,240; by branch E 7,692, J1 3,447, J2 5,601, J3 1,126, J4 255, U 5,547, U2 572. Main (closure / layoff) wife-years: 4,159 (closures 1,298); quits 14,526. Share dated by a reported end year: 0.975. Employer: no PSID public item identifies the employer or asks whether the spouses share one, so 'same employer' cannot be measured; same 3-digit industry code is the closest proxy.

## 1. How similar are spouses?

Couple-years (wave = interview year) in which both spouses worked in the previous calendar year and report an industry / occupation for the current (or, from 2003, most recent) main job. Random-match benchmark = the share expected if husbands and wives were matched at random within race x wave (sum over categories of the husbands' share x the wives' share). Black - White rows: OLS of the indicator on Black with wave fixed effects, couple-years, clustered by fam68.

| | Same sector (16) | Random-match benchmark | Same 3-digit industry | Same occupation group (8) | Random-match benchmark | Same 3-digit occupation | Same sector and occupation group | Couple-years (sector) | Couple-years (occupation) |
|---|---|---|---|---|---|---|---|---|---|
| **All married couples** | | | | | | | | | |
| Black | 0.165 | 0.068 | 0.087 | 0.227 | 0.153 | 0.031 | 0.083 | 20,201 | 20,164 |
| White | 0.194 | 0.069 | 0.130 | 0.227 | 0.135 | 0.045 | 0.086 | 59,452 | 59,642 |
| Black - White (wave FE) | -0.029*** (0.008; p=<0.001) |  | -0.042*** (0.006; p=<0.001) | 0.000 (0.009; p=0.985) |  | -0.013*** (0.003; p=<0.001) | -0.003 (0.006; p=0.612) |  |  |
| **Youngest child 0-5** | | | | | | | | | |
| Black | 0.170 | 0.071 | 0.088 | 0.228 | 0.155 | 0.032 | 0.081 | 5,826 | 5,830 |
| White | 0.182 | 0.068 | 0.114 | 0.237 | 0.140 | 0.044 | 0.092 | 13,340 | 13,423 |
| Black - White (wave FE) | -0.012 (0.011; p=0.274) |  | -0.025*** (0.008; p=0.002) | -0.009 (0.012; p=0.462) |  | -0.011** (0.005; p=0.019) | -0.010 (0.008; p=0.206) |  |  |
| **Any child 0-17** | | | | | | | | | |
| Black | 0.162 | 0.069 | 0.084 | 0.223 | 0.155 | 0.030 | 0.079 | 13,712 | 13,663 |
| White | 0.185 | 0.067 | 0.120 | 0.219 | 0.131 | 0.040 | 0.083 | 33,126 | 33,257 |
| Black - White (wave FE) | -0.022** (0.009; p=0.018) |  | -0.036*** (0.007; p=<0.001) | 0.004 (0.010; p=0.682) |  | -0.010*** (0.004; p=0.005) | -0.005 (0.007; p=0.465) |  |  |
| **1968-79** | | | | | | | | | |
| Black | 0.130 | 0.061 | 0.059 | 0.257 | 0.201 | 0.026 | 0.079 | 2,989 | 3,101 |
| White | 0.190 | 0.076 | 0.118 | 0.192 | 0.106 | 0.030 | 0.075 | 8,184 | 8,464 |
| Black - White (wave FE) | -0.060*** (0.019; p=0.001) |  | -0.059*** (0.013; p=<0.001) | 0.065*** (0.022; p=0.003) |  | -0.005 (0.007; p=0.507) | 0.003 (0.015; p=0.820) |  |  |
| **1980-99** | | | | | | | | | |
| Black | 0.174 | 0.070 | 0.094 | 0.221 | 0.144 | 0.031 | 0.084 | 9,586 | 9,416 |
| White | 0.203 | 0.067 | 0.142 | 0.222 | 0.125 | 0.048 | 0.086 | 28,968 | 28,870 |
| Black - White (wave FE) | -0.029** (0.012; p=0.017) |  | -0.049*** (0.009; p=<0.001) | -0.002 (0.012; p=0.881) |  | -0.017*** (0.004; p=<0.001) | -0.002 (0.008; p=0.772) |  |  |
| **2000-22** | | | | | | | | | |
| Black | 0.167 | 0.068 | 0.088 | 0.224 | 0.145 | 0.034 | 0.085 | 7,626 | 7,647 |
| White | 0.184 | 0.070 | 0.118 | 0.246 | 0.158 | 0.045 | 0.091 | 22,300 | 22,308 |
| Black - White (wave FE) | -0.017* (0.010; p=0.081) |  | -0.028*** (0.008; p=<0.001) | -0.023** (0.011; p=0.035) |  | -0.010** (0.004; p=0.017) | -0.006 (0.007; p=0.380) |  |  |

### 1b. Sector composition of working husbands and wives (couple-years, both working)

| | Husbands, Black | Husbands, White | Wives, Black | Wives, White |
|---|---|---|---|---|
| Agriculture, forestry, fishing | 0.021 | 0.039 | 0.006 | 0.010 |
| Mining | 0.007 | 0.008 | 0.003 | 0.002 |
| Construction | 0.099 | 0.112 | 0.004 | 0.015 |
| Durable manufacturing | 0.141 | 0.149 | 0.044 | 0.060 |
| Nondurable manufacturing (incl. printing, publishing) | 0.111 | 0.078 | 0.103 | 0.062 |
| Transportation, utilities, sanitary | 0.114 | 0.076 | 0.025 | 0.023 |
| Communications, broadcasting, telecom | 0.013 | 0.016 | 0.016 | 0.013 |
| Wholesale trade | 0.047 | 0.051 | 0.012 | 0.023 |
| Retail trade (excl. eating, drinking) | 0.076 | 0.092 | 0.080 | 0.112 |
| Eating, drinking, accommodation | 0.032 | 0.020 | 0.072 | 0.066 |
| Finance, insurance, real estate | 0.031 | 0.051 | 0.068 | 0.084 |
| Business, repair, professional services | 0.069 | 0.099 | 0.050 | 0.077 |
| Personal, household, entertainment, membership | 0.037 | 0.030 | 0.079 | 0.063 |
| Health | 0.044 | 0.035 | 0.194 | 0.157 |
| Education and social services | 0.055 | 0.067 | 0.167 | 0.185 |
| Public administration (incl. postal) | 0.102 | 0.077 | 0.075 | 0.049 |

### 1c. Do the spouses' sectors move together? (CPS MORG, 1980-2019)

Growth (log points x 100) of national employment, leaving the family's state out, of women in the wife's sector (g_w) and of men in the husband's sector (g_h), in the interview year; couple-years with both spouses working. Slope: OLS of g_w on g_h with year fixed effects (so the common business cycle is removed), clustered by fam68.

| | Raw correlation | Slope, all couples (year FE) | Slope, spouses in different sectors | N (all) | N (different sectors) |
|---|---|---|---|---|---|
| Black | 0.209 | 0.068*** (0.011; p=<0.001) | -0.009 (0.010; p=0.348) | 15,774 | 13,087 |
| White | 0.247 | 0.080*** (0.007; p=<0.001) | -0.021*** (0.006; p=<0.001) | 47,165 | 37,981 |
| All | 0.238 | 0.077*** (0.006; p=<0.001) | -0.018*** (0.005; p=<0.001) | 62,939 | 51,068 |

### 1d. The wife's labor market at the husband's displacement

Father x stack units of the stacked design (section 3), wife present at baseline. Cell: mean among displaced fathers' families / displaced - control difference (OLS with event-year fixed effects, clustered by fam68). Wife's sector = latest known in the 6 years up to the event year; growth rates in log points x 100 in the event year (1980-2019); state unemployment rate (LAUS) in percent.

| | Wife in husband's sector | Women's growth, wife's sector (national) | Men's growth, husband's sector (national) | Women's growth, wife's sector x state | State women's Bartik | Change in state unemployment rate | State unemployment rate |
|---|---|---|---|---|---|---|---|
| Black | 0.142 / -0.022 (0.015; p=0.135) | 1.346 / -0.038 (0.136; p=0.778) | 0.341 / -0.239* (0.129; p=0.064) | 1.190 / -0.380 (0.504; p=0.451) | 1.209 / -0.025 (0.016; p=0.125) | 0.128 / 0.045* (0.024; p=0.066) | 6.736 / 0.213*** (0.056; p=<0.001) |
| White | 0.138 / -0.053*** (0.013; p=<0.001) | 1.450 / -0.068 (0.129; p=0.598) | 0.214 / -0.371*** (0.113; p=0.001) | 1.904 / 0.405 (0.421; p=0.336) | 1.260 / -0.007 (0.010; p=0.481) | 0.186 / 0.043** (0.018; p=0.020) | 6.597 / 0.156*** (0.055; p=0.004) |
| Displaced: Black - White (event-year FE) | 0.014 (0.018; p=0.412) | -0.118 (0.180; p=0.513) | 0.053 (0.165; p=0.748) | -0.573 (0.658; p=0.384) | -0.060*** (0.020; p=0.003) | 0.001 (0.031; p=0.963) | 0.193** (0.078; p=0.014) |

## 2. Joint shocks: does the wife lose her job too?

Father x stack units (fathers first displaced in the event year ev vs clean controls, as in 19), wife present and employed (positive hours) at baseline, and observed in the family both at e = -1 or 0 and at e = +1 or +2 (so that her reports can exist for displaced and control families alike). Outcomes are 0/1 at the unit level; the wife's own displacement uses her reason-for-job-end reports (events dated 1983-2022, so ev 1984-2021); the zero-hours outcome uses her annual hours (all years). OLS with event-year fixed effects, clustered by fam68. The coefficient is the excess probability relative to wives of comparable non-displaced men in the same calendar years; it mixes a contemporaneous joint shock with any permanent difference in the wives' job stability (assortative risk). The placebo column (her displacement 2-4 years BEFORE his, event years 1986-2021, wife observed at e = -3 or -2) measures the permanent part; section 2b removes it with family fixed effects.

| | Wife displaced (closure / layoff), ev-1..ev+1 | Wife displaced, ev..ev+1 | Wife's employer closed, ev-1..ev+1 | Wife's hours fall to 0 (ev, ev+1) | Wife quits, ev-1..ev+1 (comparison) | Placebo: wife displaced, ev-4..ev-2 |
|---|---|---|---|---|---|---|
| **Black - A. Displaced vs controls** | | | | | | |
| Husband displaced | 0.080*** (0.022; p=<0.001) | 0.071*** (0.019; p=<0.001) | 0.014 (0.012; p=0.227) | 0.004 (0.016; p=0.802) | 0.084*** (0.028; p=0.003) | 0.011 (0.021; p=0.608) |
| Control mean | 0.090 | 0.056 | 0.028 | 0.127 | 0.248 | 0.081 |
| N (father-stacks) / clusters | 6,811 / 565 | 6,811 / 565 | 6,811 / 565 | 9,774 / 771 | 6,811 / 565 | 5,683 / 510 |
| **Black - B. By sector match (wives with a known sector)** | | | | | | |
| Husband displaced | 0.067*** (0.024; p=0.005) | 0.055*** (0.020; p=0.007) | 0.004 (0.011; p=0.746) | 0.003 (0.018; p=0.887) | 0.068** (0.030; p=0.024) | 0.004 (0.022; p=0.874) |
| Displaced x wife in his sector | 0.089 (0.065; p=0.174) | 0.074 (0.060; p=0.213) | 0.087* (0.047; p=0.065) | 0.005 (0.044; p=0.904) | 0.067 (0.074; p=0.363) | 0.039 (0.054; p=0.465) |
| Wife in his sector | -0.021* (0.011; p=0.061) | -0.009 (0.009; p=0.330) | -0.010 (0.007; p=0.143) | 0.004 (0.013; p=0.782) | -0.068*** (0.021; p=0.001) | -0.023* (0.013; p=0.087) |
| Control mean | 0.084 | 0.053 | 0.027 | 0.103 | 0.233 | 0.078 |
| N (father-stacks) / clusters | 6,515 / 549 | 6,515 / 549 | 6,515 / 549 | 8,353 / 677 | 6,515 / 549 | 5,515 / 506 |
| **Black - C. Closure vs layoff** | | | | | | |
| Husband displaced: closure | 0.071* (0.038; p=0.063) | 0.059* (0.033; p=0.077) | 0.039 (0.026; p=0.130) | -0.036 (0.025; p=0.159) | 0.048 (0.045; p=0.292) | -0.001 (0.034; p=0.979) |
| Husband displaced: layoff | 0.084*** (0.027; p=0.002) | 0.076*** (0.024; p=0.001) | 0.003 (0.012; p=0.783) | 0.020 (0.020; p=0.301) | 0.100*** (0.033; p=0.002) | 0.016 (0.024; p=0.500) |
| Control mean | 0.090 | 0.056 | 0.028 | 0.127 | 0.248 | 0.081 |
| N (father-stacks) / clusters | 6,811 / 565 | 6,811 / 565 | 6,811 / 565 | 9,774 / 771 | 6,811 / 565 | 5,683 / 510 |
| **White - A. Displaced vs controls** | | | | | | |
| Husband displaced | 0.070*** (0.015; p=<0.001) | 0.055*** (0.013; p=<0.001) | 0.015* (0.009; p=0.097) | 0.048*** (0.014; p=<0.001) | 0.117*** (0.021; p=<0.001) | 0.022* (0.013; p=0.092) |
| Control mean | 0.058 | 0.038 | 0.022 | 0.131 | 0.260 | 0.049 |
| N (father-stacks) / clusters | 20,323 / 1,202 | 20,323 / 1,202 | 20,323 / 1,202 | 27,437 / 1,483 | 20,323 / 1,202 | 18,057 / 1,135 |
| **White - B. By sector match (wives with a known sector)** | | | | | | |
| Husband displaced | 0.047*** (0.016; p=0.004) | 0.033** (0.013; p=0.013) | 0.001 (0.009; p=0.937) | 0.014 (0.014; p=0.332) | 0.099*** (0.024; p=<0.001) | 0.024* (0.015; p=0.097) |
| Displaced x wife in his sector | 0.143*** (0.052; p=0.006) | 0.142*** (0.049; p=0.004) | 0.119*** (0.042; p=0.005) | 0.100** (0.048; p=0.036) | 0.015 (0.063; p=0.812) | -0.010 (0.035; p=0.779) |
| Wife in his sector | -0.017*** (0.005; p=0.002) | -0.010** (0.004; p=0.025) | -0.006* (0.003; p=0.064) | -0.027*** (0.007; p=<0.001) | -0.090*** (0.012; p=<0.001) | -0.017*** (0.005; p=0.002) |
| Control mean | 0.057 | 0.037 | 0.021 | 0.109 | 0.252 | 0.049 |
| N (father-stacks) / clusters | 19,814 / 1,193 | 19,814 / 1,193 | 19,814 / 1,193 | 24,641 / 1,385 | 19,814 / 1,193 | 17,729 / 1,132 |
| **White - C. Closure vs layoff** | | | | | | |
| Husband displaced: closure | 0.092*** (0.028; p=0.001) | 0.106*** (0.027; p=<0.001) | 0.050** (0.020; p=0.012) | 0.024 (0.023; p=0.294) | 0.019 (0.035; p=0.593) | -0.003 (0.019; p=0.856) |
| Husband displaced: layoff | 0.059*** (0.018; p=<0.001) | 0.030** (0.013; p=0.028) | -0.002 (0.009; p=0.823) | 0.060*** (0.017; p=<0.001) | 0.165*** (0.026; p=<0.001) | 0.035** (0.017; p=0.039) |
| Control mean | 0.058 | 0.038 | 0.022 | 0.131 | 0.260 | 0.049 |
| N (father-stacks) / clusters | 20,323 / 1,202 | 20,323 / 1,202 | 20,323 / 1,202 | 27,437 / 1,483 | 20,323 / 1,202 | 18,057 / 1,135 |
| **All - A. Displaced vs controls** | | | | | | |
| Husband displaced | 0.070*** (0.015; p=<0.001) | 0.054*** (0.013; p=<0.001) | 0.016* (0.009; p=0.082) | 0.048*** (0.014; p=<0.001) | 0.118*** (0.021; p=<0.001) | 0.022* (0.013; p=0.091) |
| Displaced x Black | 0.005 (0.027; p=0.842) | 0.013 (0.023; p=0.574) | -0.004 (0.015; p=0.761) | -0.044** (0.021; p=0.042) | -0.030 (0.035; p=0.387) | -0.013 (0.025; p=0.600) |
| Black | 0.031*** (0.007; p=<0.001) | 0.018*** (0.005; p=<0.001) | 0.006* (0.004; p=0.088) | -0.010 (0.007; p=0.116) | -0.015 (0.012; p=0.234) | 0.031*** (0.007; p=<0.001) |
| Control mean | 0.066 | 0.042 | 0.023 | 0.130 | 0.257 | 0.057 |
| N (father-stacks) / clusters | 27,134 / 1,704 | 27,134 / 1,704 | 27,134 / 1,704 | 37,211 / 2,186 | 27,134 / 1,704 | 23,740 / 1,592 |
| **All - B. By sector match (wives with a known sector)** | | | | | | |
| Husband displaced | 0.056*** (0.013; p=<0.001) | 0.041*** (0.011; p=<0.001) | 0.002 (0.007; p=0.790) | 0.009 (0.011; p=0.442) | 0.086*** (0.018; p=<0.001) | 0.020 (0.012; p=0.102) |
| Displaced x wife in his sector | 0.124*** (0.041; p=0.003) | 0.117*** (0.038; p=0.002) | 0.107*** (0.031; p=<0.001) | 0.064* (0.034; p=0.058) | 0.039 (0.047; p=0.409) | 0.010 (0.030; p=0.746) |
| Wife in his sector | -0.019*** (0.005; p=<0.001) | -0.010** (0.004; p=0.012) | -0.007** (0.003; p=0.017) | -0.019*** (0.006; p=0.001) | -0.084*** (0.011; p=<0.001) | -0.019*** (0.005; p=<0.001) |
| Control mean | 0.063 | 0.041 | 0.023 | 0.107 | 0.247 | 0.056 |
| N (father-stacks) / clusters | 26,329 / 1,681 | 26,329 / 1,681 | 26,329 / 1,681 | 32,994 / 1,999 | 26,329 / 1,681 | 23,244 / 1,586 |
| **All - C. Closure vs layoff** | | | | | | |
| Husband displaced: closure | 0.086*** (0.023; p=<0.001) | 0.090*** (0.021; p=<0.001) | 0.046*** (0.016; p=0.003) | 0.003 (0.017; p=0.883) | 0.028 (0.028; p=0.304) | 0.000 (0.017; p=0.985) |
| Husband displaced: layoff | 0.071*** (0.015; p=<0.001) | 0.048*** (0.012; p=<0.001) | 0.000 (0.007; p=0.983) | 0.042*** (0.013; p=0.001) | 0.141*** (0.020; p=<0.001) | 0.031** (0.014; p=0.024) |
| Control mean | 0.066 | 0.042 | 0.023 | 0.130 | 0.257 | 0.057 |
| N (father-stacks) / clusters | 27,134 / 1,704 | 27,134 / 1,704 | 27,134 / 1,704 | 37,211 / 2,186 | 27,134 / 1,704 | 23,740 / 1,592 |
| Fixed effects | event year | event year | event year | event year | event year | event year |

### 2b. Event study of the wife's own job loss around the husband's displacement

Stacked event study as in 19 (father x stack and calendar-year x stack fixed effects, reference e = -2), wife employed at baseline; outcome = the baseline wife reports a job end of that kind since the previous observed year (event years 1985-2019 for the reason-based outcomes), or her annual hours fall to zero from positive hours in the previous observed year (at risk only if she worked then).

| | Wife displaced (closure / layoff) | Wife's employer closed | Wife's hours fall to 0 | Wife quits |
|---|---|---|---|---|
| **All fathers, wife employed at baseline** | | | | |
| e=-3 | -0.014 (0.017; p=0.388) | -0.004 (0.008; p=0.655) | n.a. | -0.032 (0.026; p=0.213) |
| e=-1 | -0.003 (0.017; p=0.846) | -0.002 (0.009; p=0.808) | -0.005 (0.009; p=0.566) | 0.018 (0.027; p=0.507) |
| e=+0 | 0.019 (0.016; p=0.226) | 0.007 (0.009; p=0.421) | 0.007 (0.013; p=0.622) | 0.020 (0.023; p=0.398) |
| e=+1 | 0.014 (0.018; p=0.444) | 0.001 (0.009; p=0.956) | 0.011 (0.014; p=0.417) | 0.000 (0.026; p=0.989) |
| e=+2 | -0.008 (0.015; p=0.600) | -0.001 (0.007; p=0.880) | 0.024 (0.015; p=0.101) | -0.024 (0.025; p=0.338) |
| e=+3 | -0.004 (0.019; p=0.837) | -0.002 (0.009; p=0.858) | 0.019 (0.015; p=0.224) | -0.002 (0.028; p=0.954) |
| e=+4 | 0.003 (0.017; p=0.865) | 0.002 (0.008; p=0.787) | 0.008 (0.014; p=0.575) | -0.024 (0.025; p=0.342) |
| e=+5 | 0.004 (0.021; p=0.851) | 0.005 (0.011; p=0.682) | 0.006 (0.014; p=0.690) | -0.024 (0.027; p=0.381) |
| e=+6 | 0.000 (0.017; p=0.996) | 0.007 (0.010; p=0.485) | -0.007 (0.014; p=0.601) | -0.016 (0.027; p=0.557) |
| mean +1..+3 | 0.001 (0.014; p=0.964) | -0.001 (0.007; p=0.912) | 0.018 (0.012; p=0.126) | -0.008 (0.020; p=0.686) |
| Treated mean at e = -2, -1 | 0.064 | 0.018 | 0.021 | 0.206 |
| N (man-years, stacked) | 161,919 | 161,919 | 199,923 | 161,919 |
| Displaced fathers / control father-stacks | 982 / 30,573 | 982 / 30,573 | 1,557 / 42,499 | 982 / 30,573 |
| Clusters (fam68) | 1,822 | 1,822 | 2,281 | 1,822 |
| **Black fathers, wife employed at baseline** | | | | |
| e=-3 | -0.025 (0.036; p=0.496) | 0.006 (0.021; p=0.788) | n.a. | 0.026 (0.045; p=0.566) |
| e=-1 | 0.001 (0.034; p=0.978) | 0.003 (0.017; p=0.867) | 0.003 (0.013; p=0.829) | 0.082* (0.043; p=0.055) |
| e=+0 | 0.022 (0.030; p=0.469) | 0.007 (0.014; p=0.601) | -0.025 (0.021; p=0.226) | 0.031 (0.037; p=0.401) |
| e=+1 | 0.065* (0.036; p=0.074) | 0.010 (0.017; p=0.539) | 0.001 (0.020; p=0.955) | 0.061 (0.045; p=0.177) |
| e=+2 | -0.010 (0.029; p=0.720) | 0.000 (0.013; p=0.989) | -0.002 (0.022; p=0.936) | 0.013 (0.041; p=0.757) |
| e=+3 | 0.011 (0.037; p=0.767) | 0.011 (0.020; p=0.574) | 0.012 (0.026; p=0.644) | 0.023 (0.046; p=0.621) |
| e=+4 | -0.022 (0.030; p=0.456) | -0.006 (0.013; p=0.615) | -0.011 (0.024; p=0.636) | -0.001 (0.041; p=0.971) |
| e=+5 | 0.021 (0.043; p=0.624) | -0.005 (0.017; p=0.753) | -0.005 (0.022; p=0.816) | 0.046 (0.050; p=0.353) |
| e=+6 | -0.001 (0.031; p=0.984) | 0.005 (0.018; p=0.779) | -0.026 (0.020; p=0.207) | -0.020 (0.046; p=0.657) |
| mean +1..+3 | 0.022 (0.028; p=0.441) | 0.007 (0.013; p=0.569) | 0.004 (0.018; p=0.833) | 0.032 (0.032; p=0.310) |
| Treated mean at e = -2, -1 | 0.076 | 0.021 | 0.024 | 0.185 |
| N (man-years, stacked) | 41,457 | 41,457 | 53,089 | 41,457 |
| Displaced fathers / control father-stacks | 392 / 8,292 | 392 / 8,292 | 626 / 11,588 | 392 / 8,292 |
| Clusters (fam68) | 628 | 628 | 825 | 628 |
| **White fathers, wife employed at baseline** | | | | |
| e=-3 | -0.009 (0.017; p=0.619) | -0.007 (0.007; p=0.306) | n.a. | -0.063** (0.032; p=0.046) |
| e=-1 | -0.005 (0.020; p=0.797) | -0.004 (0.011; p=0.697) | -0.009 (0.011; p=0.401) | -0.017 (0.034; p=0.614) |
| e=+0 | 0.017 (0.018; p=0.348) | 0.008 (0.012; p=0.521) | 0.028 (0.017; p=0.102) | 0.009 (0.029; p=0.750) |
| e=+1 | -0.009 (0.020; p=0.658) | -0.003 (0.011; p=0.763) | 0.016 (0.018; p=0.368) | -0.032 (0.033; p=0.329) |
| e=+2 | -0.008 (0.018; p=0.667) | -0.001 (0.009; p=0.879) | 0.039** (0.020; p=0.048) | -0.051* (0.031; p=0.094) |
| e=+3 | -0.009 (0.021; p=0.655) | -0.007 (0.010; p=0.477) | 0.022 (0.019; p=0.259) | -0.018 (0.034; p=0.595) |
| e=+4 | 0.015 (0.020; p=0.455) | 0.007 (0.011; p=0.491) | 0.017 (0.018; p=0.356) | -0.042 (0.032; p=0.196) |
| e=+5 | -0.001 (0.023; p=0.980) | 0.011 (0.015; p=0.444) | 0.009 (0.019; p=0.612) | -0.059* (0.033; p=0.069) |
| e=+6 | -0.000 (0.020; p=0.993) | 0.009 (0.012; p=0.473) | -0.001 (0.018; p=0.956) | -0.020 (0.033; p=0.542) |
| mean +1..+3 | -0.009 (0.016; p=0.592) | -0.004 (0.008; p=0.627) | 0.026* (0.016; p=0.097) | -0.034 (0.026; p=0.196) |
| Treated mean at e = -2, -1 | 0.057 | 0.016 | 0.018 | 0.220 |
| N (man-years, stacked) | 120,462 | 120,462 | 146,834 | 120,462 |
| Displaced fathers / control father-stacks | 590 / 22,281 | 590 / 22,281 | 931 / 30,911 | 590 / 22,281 |
| Clusters (fam68) | 1,279 | 1,279 | 1,531 | 1,279 |
| Fixed effects | father x stack, calendar year x stack | father x stack, calendar year x stack | father x stack, calendar year x stack | father x stack, calendar year x stack |

### 2c. The wife's own displacement year by year (no reference year)

Same units as section 2 (wife employed at baseline, observed before and after), event years 1987-2019 so that her reports cover ev-5..ev+3. Share of wives with a closure / layoff dated to calendar year ev + k. The wives of displaced men already have twice the control rate at k = -2 and -1 (dating error between the two spouses' reports and / or local shocks that start before his job ends), so the event study in 2b, whose reference year is k = -2, understates the joint shock; the window measure of section 2 (k = -1..+1) does not have this problem.

| | k=-5 | k=-4 | k=-3 | k=-2 | k=-1 | k=+0 | k=+1 | k=+2 | k=+3 |
|---|---|---|---|---|---|---|---|---|---|
| **Black** | | | | | | | | | |
| Displaced families: rate | 0.027 | 0.008 | 0.008 | 0.057 | 0.054 | 0.073 | 0.073 | 0.031 | 0.038 |
| Controls: rate | 0.022 | 0.024 | 0.026 | 0.028 | 0.037 | 0.029 | 0.028 | 0.026 | 0.020 |
| Excess (OLS, event-year FE) | 0.007 (0.010; p=0.515) | -0.016*** (0.006; p=0.008) | -0.016*** (0.006; p=0.008) | 0.026 (0.016; p=0.108) | 0.021 (0.014; p=0.146) | 0.043** (0.017; p=0.010) | 0.047*** (0.016; p=0.003) | 0.004 (0.011; p=0.716) | 0.020* (0.012; p=0.095) |
| N father-stacks (displaced) | 5,956 (261) | 5,956 (261) | 5,956 (261) | 5,956 (261) | 5,956 (261) | 5,956 (261) | 5,956 (261) | 5,956 (261) | 5,956 (261) |
| **White** | | | | | | | | | |
| Displaced families: rate | 0.009 | 0.020 | 0.020 | 0.040 | 0.054 | 0.063 | 0.040 | 0.029 | 0.031 |
| Controls: rate | 0.015 | 0.016 | 0.017 | 0.018 | 0.021 | 0.019 | 0.018 | 0.015 | 0.015 |
| Excess (OLS, event-year FE) | -0.005 (0.005; p=0.249) | 0.003 (0.007; p=0.661) | 0.003 (0.007; p=0.676) | 0.020** (0.009; p=0.030) | 0.032*** (0.011; p=0.002) | 0.039*** (0.011; p=<0.001) | 0.021** (0.009; p=0.022) | 0.012 (0.008; p=0.139) | 0.017** (0.008; p=0.035) |
| N father-stacks (displaced) | 17,672 (445) | 17,672 (445) | 17,672 (445) | 17,672 (445) | 17,672 (445) | 17,672 (445) | 17,672 (445) | 17,672 (445) | 17,672 (445) |

## 3. Demand-side test: is the wife's response weaker when her own market is also hit?

Stacked difference-in-differences of 19 with event-time bins (e = -3, -1, 0, +1..+3, +4..+6; reference e = -2), wife present at baseline, outcomes for the baseline wife while she is in the family unit. For a moderator M measured in the event year: bin x M for all units and displaced x bin x M; M is centred at the displaced families' mean and, if continuous, divided by its s.d. among them. Rows: 'Displaced' = response at e = +1..+3 at the average M; 'Displaced x M' = change in that response per s.d. of M (for (a): wife in his sector vs not); 'pre' rows = mean of the e = -3 and e = -1 coefficients (a pre-trend check). A demand-side constraint predicts a smaller response when her sector shrinks or local unemployment rises: Displaced x M > 0 for (b), (b'), (c) and < 0 for (c'), and < 0 for (a) if the same sector is hit. 'Wife unemployed, looking' = status 3 at the next interview (wives not asked 1968-75, 1977, 1978). output/wife_search.csv (21.WifeSearch.py) was found and is summarised in section 3f.

### 3a. (a) Wife worked in the husband's sector

| | Wife employed | Wife's hours | Wife unemployed, looking (interview) |
|---|---|---|---|
| **Black** | | | |
| Displaced, e=+1..+3 | 0.009 (0.021; p=0.668) | 19 (48; p=0.686) | -0.020 (0.018; p=0.263) |
| Displaced, pre | 0.013 (0.020; p=0.523) | -1 (40; p=0.973) | -0.014 (0.019; p=0.458) |
| Displaced x M, e=+1..+3 | 0.057 (0.060; p=0.344) | 68 (144; p=0.635) | -0.071 (0.047; p=0.131) |
| Displaced x M, pre | 0.118** (0.057; p=0.039) | 147 (114; p=0.197) | -0.035 (0.054; p=0.515) |
| Treated mean at e = -2, -1 | 0.880 | 1,378 | 0.067 |
| N (man-years, stacked) | 68,170 | 68,170 | 57,927 |
| Displaced fathers / control father-stacks | 585 / 11,961 | 585 / 11,961 | 556 / 11,570 |
| Clusters (fam68) | 762 | 762 | 711 |
| Displaced: mean of M / s.d. | 0.142 | 0.142 | 0.142 |
| **White** | | | |
| Displaced, e=+1..+3 | -0.004 (0.020; p=0.836) | 57 (38; p=0.133) | 0.003 (0.010; p=0.733) |
| Displaced, pre | -0.021 (0.016; p=0.179) | 1 (29; p=0.981) | -0.000 (0.009; p=0.996) |
| Displaced x M, e=+1..+3 | -0.152** (0.062; p=0.015) | -281** (134; p=0.035) | 0.029 (0.027; p=0.281) |
| Displaced x M, pre | -0.026 (0.042; p=0.529) | -109 (94; p=0.247) | 0.012 (0.023; p=0.594) |
| Treated mean at e = -2, -1 | 0.821 | 1,147 | 0.031 |
| N (man-years, stacked) | 204,739 | 204,739 | 177,761 |
| Displaced fathers / control father-stacks | 960 / 33,922 | 960 / 33,922 | 930 / 33,192 |
| Clusters (fam68) | 1,473 | 1,473 | 1,421 |
| Displaced: mean of M / s.d. | 0.138 | 0.138 | 0.138 |
| **Black, wife not employed at baseline** | | | |
| Displaced, e=+1..+3 | 0.020 (0.086; p=0.814) | 43 (142; p=0.764) | -0.004 (0.059; p=0.942) |
| Displaced, pre | -0.101 (0.077; p=0.190) | -68 (111; p=0.544) | 0.034 (0.073; p=0.645) |
| Displaced x M, e=+1..+3 | 0.461*** (0.140; p=0.001) | 811 (597; p=0.174) | -0.136 (0.131; p=0.298) |
| Displaced x M, pre | 0.526** (0.265; p=0.047) | 201 (151; p=0.182) | 0.007 (0.085; p=0.934) |
| Treated mean at e = -2, -1 | 0.177 | 153 | 0.088 |
| N (man-years, stacked) | 8,154 | 8,154 | 6,389 |
| Displaced fathers / control father-stacks | 62 / 1,314 | 62 / 1,314 | 59 / 1,254 |
| Clusters (fam68) | 362 | 362 | 336 |
| Displaced: mean of M / s.d. | 0.065 | 0.065 | 0.065 |
| **White, wife not employed at baseline** | | | |
| Displaced, e=+1..+3 | 0.071 (0.061; p=0.249) | 185** (79; p=0.019) | 0.017 (0.023; p=0.455) |
| Displaced, pre | -0.040 (0.051; p=0.434) | 20 (58; p=0.731) | 0.025 (0.020; p=0.196) |
| Displaced x M, e=+1..+3 | 0.176 (0.216; p=0.415) | 186 (373; p=0.617) | 0.044 (0.052; p=0.399) |
| Displaced x M, pre | 0.041 (0.158; p=0.796) | -234 (248; p=0.346) | 0.032 (0.054; p=0.551) |
| Treated mean at e = -2, -1 | 0.160 | 102 | 0.044 |
| N (man-years, stacked) | 31,667 | 31,667 | 26,052 |
| Displaced fathers / control father-stacks | 161 / 4,829 | 161 / 4,829 | 159 / 4,756 |
| Clusters (fam68) | 893 | 893 | 874 |
| Displaced: mean of M / s.d. | 0.099 | 0.099 | 0.099 |
| **Black, wife employed at baseline** | | | |
| Displaced, e=+1..+3 | 0.005 (0.019; p=0.795) | 21 (50; p=0.675) | -0.023 (0.019; p=0.236) |
| Displaced, pre | 0.023 (0.017; p=0.175) | 7 (43; p=0.866) | -0.020 (0.020; p=0.313) |
| Displaced x M, e=+1..+3 | 0.064 (0.061; p=0.297) | 77 (147; p=0.598) | -0.073 (0.050; p=0.141) |
| Displaced x M, pre | 0.091* (0.054; p=0.091) | 164 (122; p=0.178) | -0.027 (0.057; p=0.638) |
| Treated mean at e = -2, -1 | 0.969 | 1,534 | 0.064 |
| N (man-years, stacked) | 60,007 | 60,007 | 51,530 |
| Displaced fathers / control father-stacks | 523 / 10,646 | 523 / 10,646 | 497 / 10,315 |
| Clusters (fam68) | 747 | 747 | 696 |
| Displaced: mean of M / s.d. | 0.151 | 0.151 | 0.151 |
| **White, wife employed at baseline** | | | |
| Displaced, e=+1..+3 | -0.036** (0.018; p=0.044) | 12 (42; p=0.769) | 0.000 (0.011; p=0.976) |
| Displaced, pre | -0.024* (0.014; p=0.077) | -11 (33; p=0.735) | -0.006 (0.011; p=0.611) |
| Displaced x M, e=+1..+3 | -0.204*** (0.053; p=<0.001) | -370*** (133; p=0.005) | 0.031 (0.030; p=0.308) |
| Displaced x M, pre | -0.023 (0.032; p=0.465) | -71 (98; p=0.470) | 0.010 (0.025; p=0.677) |
| Treated mean at e = -2, -1 | 0.962 | 1,369 | 0.029 |
| N (man-years, stacked) | 173,072 | 173,072 | 151,709 |
| Displaced fathers / control father-stacks | 799 / 29,093 | 799 / 29,093 | 771 / 28,436 |
| Clusters (fam68) | 1,449 | 1,449 | 1,392 |
| Displaced: mean of M / s.d. | 0.145 | 0.145 | 0.145 |
| Fixed effects | father x stack, calendar year x stack | father x stack, calendar year x stack | father x stack, calendar year x stack |

### 3b. (b) Women's employment growth in the wife's sector (national, leave-one-state-out), holding the husband's sector growth fixed

| | Wife employed | Wife's hours | Wife unemployed, looking (interview) |
|---|---|---|---|
| **Black** | | | |
| Displaced, e=+1..+3 | -0.003 (0.023; p=0.900) | 2 (54; p=0.974) | -0.021 (0.018; p=0.254) |
| Displaced, pre | 0.016 (0.023; p=0.493) | 9 (50; p=0.862) | -0.015 (0.021; p=0.476) |
| Displaced x M, e=+1..+3 | -0.008 (0.025; p=0.759) | 45 (62; p=0.467) | 0.007 (0.015; p=0.653) |
| Displaced x M, pre | -0.039 (0.025; p=0.116) | -65 (48; p=0.178) | -0.011 (0.018; p=0.534) |
| Displaced x husband's sector growth, e=+1..+3 | -0.017 (0.026; p=0.519) | -27 (52; p=0.605) | 0.001 (0.017; p=0.941) |
| Treated mean at e = -2, -1 | 0.899 | 1,450 | 0.058 |
| N (man-years, stacked) | 49,952 | 49,952 | 49,815 |
| Displaced fathers / control father-stacks | 469 / 9,373 | 469 / 9,373 | 469 / 9,373 |
| Clusters (fam68) | 661 | 661 | 661 |
| Displaced: mean of M / s.d. | 1.332 / 3.063 | 1.332 / 3.063 | 1.332 / 3.063 |
| **White** | | | |
| Displaced, e=+1..+3 | 0.005 (0.022; p=0.821) | 53 (45; p=0.238) | 0.004 (0.010; p=0.683) |
| Displaced, pre | -0.014 (0.017; p=0.404) | -6 (37; p=0.871) | 0.002 (0.009; p=0.844) |
| Displaced x M, e=+1..+3 | -0.007 (0.020; p=0.736) | -14 (42; p=0.744) | -0.017 (0.011; p=0.104) |
| Displaced x M, pre | 0.005 (0.017; p=0.780) | 34 (30; p=0.263) | -0.020* (0.011; p=0.086) |
| Displaced x husband's sector growth, e=+1..+3 | -0.029 (0.021; p=0.165) | -15 (43; p=0.725) | 0.001 (0.010; p=0.958) |
| Treated mean at e = -2, -1 | 0.830 | 1,197 | 0.032 |
| N (man-years, stacked) | 152,948 | 152,948 | 152,670 |
| Displaced fathers / control father-stacks | 757 / 26,676 | 757 / 26,676 | 757 / 26,675 |
| Clusters (fam68) | 1,334 | 1,334 | 1,334 |
| Displaced: mean of M / s.d. | 1.438 / 3.866 | 1.438 / 3.866 | 1.438 / 3.866 |
| **Black, wife not employed at baseline** | | | |
| Displaced, e=+1..+3 | 0.086 (0.108; p=0.427) | 185 (158; p=0.243) | 0.002 (0.061; p=0.976) |
| Displaced, pre | -0.103 (0.104; p=0.323) | 27 (117; p=0.814) | 0.016 (0.070; p=0.824) |
| Displaced x M, e=+1..+3 | 0.023 (0.088; p=0.793) | 65 (161; p=0.685) | -0.087 (0.062; p=0.159) |
| Displaced x M, pre | -0.023 (0.100; p=0.818) | -32 (96; p=0.738) | -0.090 (0.098; p=0.358) |
| Displaced x husband's sector growth, e=+1..+3 | -0.036 (0.087; p=0.680) | -158 (101; p=0.117) | -0.002 (0.043; p=0.966) |
| Treated mean at e = -2, -1 | 0.143 | 82 | 0.048 |
| N (man-years, stacked) | 5,082 | 5,082 | 5,048 |
| Displaced fathers / control father-stacks | 44 / 898 | 44 / 898 | 44 / 898 |
| Clusters (fam68) | 273 | 273 | 273 |
| Displaced: mean of M / s.d. | 1.553 / 3.166 | 1.553 / 3.166 | 1.553 / 3.166 |
| **White, wife not employed at baseline** | | | |
| Displaced, e=+1..+3 | 0.140** (0.070; p=0.045) | 292*** (101; p=0.004) | 0.015 (0.023; p=0.523) |
| Displaced, pre | -0.007 (0.060; p=0.904) | 34 (80; p=0.667) | 0.022 (0.019; p=0.227) |
| Displaced x M, e=+1..+3 | -0.038 (0.066; p=0.567) | -14 (92; p=0.883) | -0.008 (0.020; p=0.671) |
| Displaced x M, pre | -0.056 (0.064; p=0.377) | 44 (62; p=0.481) | -0.038 (0.030; p=0.211) |
| Displaced x husband's sector growth, e=+1..+3 | -0.098 (0.070; p=0.159) | -144* (84; p=0.088) | -0.000 (0.018; p=0.993) |
| Treated mean at e = -2, -1 | 0.134 | 100 | 0.049 |
| N (man-years, stacked) | 20,896 | 20,896 | 20,841 |
| Displaced fathers / control father-stacks | 123 / 3,476 | 123 / 3,476 | 123 / 3,475 |
| Clusters (fam68) | 762 | 762 | 762 |
| Displaced: mean of M / s.d. | 1.244 / 4.339 | 1.244 / 4.339 | 1.244 / 4.339 |
| **Black, wife employed at baseline** | | | |
| Displaced, e=+1..+3 | -0.014 (0.021; p=0.504) | -14 (57; p=0.805) | -0.025 (0.019; p=0.195) |
| Displaced, pre | 0.021 (0.021; p=0.308) | 2 (55; p=0.975) | -0.021 (0.021; p=0.322) |
| Displaced x M, e=+1..+3 | -0.021 (0.022; p=0.339) | 26 (64; p=0.680) | 0.016 (0.016; p=0.295) |
| Displaced x M, pre | -0.032 (0.022; p=0.136) | -63 (53; p=0.236) | 0.001 (0.015; p=0.940) |
| Displaced x husband's sector growth, e=+1..+3 | 0.007 (0.024; p=0.770) | 16 (56; p=0.772) | -0.003 (0.020; p=0.871) |
| Treated mean at e = -2, -1 | 0.980 | 1,597 | 0.060 |
| N (man-years, stacked) | 44,870 | 44,870 | 44,767 |
| Displaced fathers / control father-stacks | 425 / 8,475 | 425 / 8,475 | 425 / 8,475 |
| Clusters (fam68) | 650 | 650 | 650 |
| Displaced: mean of M / s.d. | 1.309 / 3.055 | 1.309 / 3.055 | 1.309 / 3.055 |
| **White, wife employed at baseline** | | | |
| Displaced, e=+1..+3 | -0.040** (0.019; p=0.039) | -13 (49; p=0.785) | 0.002 (0.011; p=0.863) |
| Displaced, pre | -0.024* (0.014; p=0.092) | -24 (40; p=0.544) | -0.002 (0.011; p=0.832) |
| Displaced x M, e=+1..+3 | 0.005 (0.016; p=0.760) | -1 (42; p=0.973) | -0.020 (0.013; p=0.109) |
| Displaced x M, pre | 0.012 (0.012; p=0.331) | 27 (33; p=0.415) | -0.015 (0.011; p=0.178) |
| Displaced x husband's sector growth, e=+1..+3 | -0.010 (0.017; p=0.548) | 15 (48; p=0.756) | 0.002 (0.012; p=0.882) |
| Treated mean at e = -2, -1 | 0.970 | 1,418 | 0.029 |
| N (man-years, stacked) | 132,052 | 132,052 | 131,829 |
| Displaced fathers / control father-stacks | 634 / 23,200 | 634 / 23,200 | 634 / 23,200 |
| Clusters (fam68) | 1,307 | 1,307 | 1,307 |
| Displaced: mean of M / s.d. | 1.476 / 3.769 | 1.476 / 3.769 | 1.476 / 3.769 |
| Fixed effects | father x stack, calendar year x stack | father x stack, calendar year x stack | father x stack, calendar year x stack |

### 3c. (b') Women's employment growth in the wife's sector in the state

| | Wife employed | Wife's hours | Wife unemployed, looking (interview) |
|---|---|---|---|
| **Black** | | | |
| Displaced, e=+1..+3 | -0.001 (0.023; p=0.967) | 4 (54; p=0.938) | -0.022 (0.018; p=0.235) |
| Displaced, pre | 0.007 (0.023; p=0.752) | -4 (50; p=0.943) | -0.017 (0.020; p=0.396) |
| Displaced x M, e=+1..+3 | -0.029 (0.026; p=0.265) | -5 (59; p=0.936) | -0.001 (0.020; p=0.944) |
| Displaced x M, pre | -0.000 (0.024; p=0.990) | 11 (57; p=0.848) | -0.014 (0.023; p=0.539) |
| Treated mean at e = -2, -1 | 0.892 | 1,444 | 0.058 |
| N (man-years, stacked) | 50,489 | 50,489 | 50,251 |
| Displaced fathers / control father-stacks | 470 / 9,492 | 470 / 9,492 | 470 / 9,492 |
| Clusters (fam68) | 678 | 678 | 678 |
| Displaced: mean of M / s.d. | 1.190 / 11.331 | 1.190 / 11.331 | 1.190 / 11.331 |
| **White** | | | |
| Displaced, e=+1..+3 | 0.004 (0.022; p=0.856) | 56 (45; p=0.209) | 0.001 (0.010; p=0.892) |
| Displaced, pre | -0.017 (0.017; p=0.319) | -2 (37; p=0.951) | -0.002 (0.010; p=0.859) |
| Displaced x M, e=+1..+3 | 0.033 (0.021; p=0.121) | 86** (41; p=0.037) | -0.005 (0.007; p=0.510) |
| Displaced x M, pre | 0.029* (0.016; p=0.074) | 76** (33; p=0.022) | -0.008 (0.007; p=0.282) |
| Treated mean at e = -2, -1 | 0.829 | 1,187 | 0.034 |
| N (man-years, stacked) | 152,732 | 152,732 | 152,217 |
| Displaced fathers / control father-stacks | 754 / 26,596 | 754 / 26,596 | 754 / 26,595 |
| Clusters (fam68) | 1,340 | 1,340 | 1,340 |
| Displaced: mean of M / s.d. | 1.904 / 11.304 | 1.904 / 11.304 | 1.904 / 11.304 |
| **Black, wife not employed at baseline** | | | |
| Displaced, e=+1..+3 | 0.111 (0.106; p=0.296) | 229 (158; p=0.149) | -0.010 (0.062; p=0.876) |
| Displaced, pre | -0.092 (0.106; p=0.383) | 13 (120; p=0.913) | -0.020 (0.079; p=0.804) |
| Displaced x M, e=+1..+3 | -0.103 (0.118; p=0.385) | -236 (155; p=0.126) | 0.008 (0.088; p=0.925) |
| Displaced x M, pre | 0.000 (0.072; p=0.999) | 24 (101; p=0.812) | 0.028 (0.089; p=0.756) |
| Treated mean at e = -2, -1 | 0.132 | 76 | 0.060 |
| N (man-years, stacked) | 5,123 | 5,123 | 5,071 |
| Displaced fathers / control father-stacks | 47 / 912 | 47 / 912 | 47 / 912 |
| Clusters (fam68) | 278 | 278 | 278 |
| Displaced: mean of M / s.d. | 1.484 / 11.702 | 1.484 / 11.702 | 1.484 / 11.702 |
| **White, wife not employed at baseline** | | | |
| Displaced, e=+1..+3 | 0.131* (0.073; p=0.071) | 293*** (96; p=0.002) | 0.011 (0.024; p=0.659) |
| Displaced, pre | -0.033 (0.059; p=0.571) | 37 (73; p=0.616) | 0.012 (0.018; p=0.507) |
| Displaced x M, e=+1..+3 | 0.008 (0.066; p=0.899) | -6 (75; p=0.939) | -0.000 (0.014; p=0.984) |
| Displaced x M, pre | 0.030 (0.049; p=0.535) | 133* (71; p=0.062) | -0.001 (0.012; p=0.904) |
| Treated mean at e = -2, -1 | 0.140 | 92 | 0.043 |
| N (man-years, stacked) | 21,331 | 21,331 | 21,222 |
| Displaced fathers / control father-stacks | 123 / 3,540 | 123 / 3,540 | 123 / 3,539 |
| Clusters (fam68) | 762 | 762 | 762 |
| Displaced: mean of M / s.d. | 1.559 / 10.802 | 1.559 / 10.802 | 1.559 / 10.802 |
| **Black, wife employed at baseline** | | | |
| Displaced, e=+1..+3 | -0.017 (0.020; p=0.408) | -18 (56; p=0.746) | -0.023 (0.019; p=0.232) |
| Displaced, pre | 0.014 (0.019; p=0.480) | -7 (54; p=0.903) | -0.019 (0.021; p=0.363) |
| Displaced x M, e=+1..+3 | -0.011 (0.022; p=0.619) | 33 (59; p=0.572) | -0.004 (0.019; p=0.831) |
| Displaced x M, pre | 0.008 (0.022; p=0.722) | 14 (56; p=0.797) | -0.019 (0.022; p=0.392) |
| Treated mean at e = -2, -1 | 0.980 | 1,602 | 0.058 |
| N (man-years, stacked) | 45,366 | 45,366 | 45,180 |
| Displaced fathers / control father-stacks | 423 / 8,580 | 423 / 8,580 | 423 / 8,580 |
| Clusters (fam68) | 666 | 666 | 666 |
| Displaced: mean of M / s.d. | 1.158 / 11.303 | 1.158 / 11.303 | 1.158 / 11.303 |
| **White, wife employed at baseline** | | | |
| Displaced, e=+1..+3 | -0.037* (0.019; p=0.059) | -7 (49; p=0.892) | -0.001 (0.011; p=0.935) |
| Displaced, pre | -0.020 (0.014; p=0.169) | -16 (41; p=0.687) | -0.004 (0.012; p=0.707) |
| Displaced x M, e=+1..+3 | 0.032 (0.020; p=0.110) | 102** (47; p=0.031) | -0.004 (0.008; p=0.586) |
| Displaced x M, pre | 0.015 (0.013; p=0.267) | 55 (36; p=0.129) | -0.008 (0.008; p=0.325) |
| Treated mean at e = -2, -1 | 0.968 | 1,408 | 0.032 |
| N (man-years, stacked) | 131,401 | 131,401 | 130,995 |
| Displaced fathers / control father-stacks | 631 / 23,056 | 631 / 23,056 | 631 / 23,056 |
| Clusters (fam68) | 1,313 | 1,313 | 1,313 |
| Displaced: mean of M / s.d. | 1.971 / 11.407 | 1.971 / 11.407 | 1.971 / 11.407 |
| Fixed effects | father x stack, calendar year x stack | father x stack, calendar year x stack | father x stack, calendar year x stack |

### 3d. (c) Predicted growth of women's employment in the state (Bartik)

| | Wife employed | Wife's hours | Wife unemployed, looking (interview) |
|---|---|---|---|
| **Black** | | | |
| Displaced, e=+1..+3 | 0.001 (0.022; p=0.955) | 37 (49; p=0.451) | -0.007 (0.017; p=0.664) |
| Displaced, pre | 0.022 (0.022; p=0.307) | 42 (46; p=0.361) | -0.004 (0.019; p=0.836) |
| Displaced x M, e=+1..+3 | -0.010 (0.022; p=0.644) | -33 (51; p=0.514) | 0.002 (0.018; p=0.900) |
| Displaced x M, pre | -0.028 (0.022; p=0.197) | -82* (46; p=0.074) | -0.012 (0.021; p=0.578) |
| Treated mean at e = -2, -1 | 0.792 | 1,249 | 0.082 |
| N (man-years, stacked) | 63,459 | 63,459 | 63,088 |
| Displaced fathers / control father-stacks | 609 / 11,625 | 609 / 11,625 | 607 / 11,624 |
| Clusters (fam68) | 730 | 730 | 730 |
| Displaced: mean of M / s.d. | 1.209 / 1.645 | 1.209 / 1.645 | 1.209 / 1.645 |
| **White** | | | |
| Displaced, e=+1..+3 | 0.007 (0.021; p=0.728) | 47 (39; p=0.231) | 0.006 (0.009; p=0.525) |
| Displaced, pre | -0.021 (0.017; p=0.238) | -17 (33; p=0.598) | 0.004 (0.010; p=0.707) |
| Displaced x M, e=+1..+3 | -0.016 (0.024; p=0.500) | 36 (43; p=0.410) | -0.016 (0.011; p=0.145) |
| Displaced x M, pre | -0.017 (0.020; p=0.389) | 19 (37; p=0.609) | -0.017 (0.011; p=0.131) |
| Treated mean at e = -2, -1 | 0.735 | 1,022 | 0.036 |
| N (man-years, stacked) | 186,710 | 186,710 | 185,892 |
| Displaced fathers / control father-stacks | 959 / 31,767 | 959 / 31,767 | 958 / 31,766 |
| Clusters (fam68) | 1,417 | 1,417 | 1,417 |
| Displaced: mean of M / s.d. | 1.260 / 1.672 | 1.260 / 1.672 | 1.260 / 1.672 |
| **Black, wife not employed at baseline** | | | |
| Displaced, e=+1..+3 | 0.041 (0.065; p=0.526) | 100 (96; p=0.301) | 0.038 (0.048; p=0.430) |
| Displaced, pre | -0.027 (0.062; p=0.656) | 13 (74; p=0.855) | 0.038 (0.052; p=0.464) |
| Displaced x M, e=+1..+3 | 0.012 (0.066; p=0.858) | -51 (99; p=0.607) | -0.039 (0.061; p=0.527) |
| Displaced x M, pre | -0.020 (0.058; p=0.730) | -22 (70; p=0.755) | -0.041 (0.064; p=0.525) |
| Treated mean at e = -2, -1 | 0.082 | 53 | 0.120 |
| N (man-years, stacked) | 13,208 | 13,208 | 13,086 |
| Displaced fathers / control father-stacks | 120 / 2,217 | 120 / 2,217 | 118 / 2,216 |
| Clusters (fam68) | 405 | 405 | 404 |
| Displaced: mean of M / s.d. | 1.408 / 1.575 | 1.408 / 1.575 | 1.408 / 1.575 |
| **White, wife not employed at baseline** | | | |
| Displaced, e=+1..+3 | 0.109** (0.049; p=0.027) | 234*** (66; p=<0.001) | 0.022 (0.016; p=0.166) |
| Displaced, pre | -0.042 (0.040; p=0.298) | 5 (48; p=0.922) | 0.024 (0.016; p=0.148) |
| Displaced x M, e=+1..+3 | -0.039 (0.057; p=0.498) | -10 (69; p=0.885) | -0.009 (0.020; p=0.637) |
| Displaced x M, pre | -0.053 (0.045; p=0.244) | -0 (55; p=1.000) | -0.017 (0.020; p=0.403) |
| Treated mean at e = -2, -1 | 0.124 | 84 | 0.034 |
| N (man-years, stacked) | 43,094 | 43,094 | 42,837 |
| Displaced fathers / control father-stacks | 250 / 6,931 | 250 / 6,931 | 249 / 6,930 |
| Clusters (fam68) | 964 | 964 | 964 |
| Displaced: mean of M / s.d. | 1.347 / 1.654 | 1.347 / 1.654 | 1.347 / 1.654 |
| **Black, wife employed at baseline** | | | |
| Displaced, e=+1..+3 | -0.006 (0.021; p=0.756) | 27 (56; p=0.630) | -0.019 (0.018; p=0.307) |
| Displaced, pre | 0.033* (0.019; p=0.088) | 51 (54; p=0.344) | -0.017 (0.020; p=0.413) |
| Displaced x M, e=+1..+3 | -0.003 (0.019; p=0.877) | -17 (56; p=0.753) | 0.012 (0.017; p=0.492) |
| Displaced x M, pre | -0.020 (0.020; p=0.317) | -85 (53; p=0.110) | -0.004 (0.021; p=0.867) |
| Treated mean at e = -2, -1 | 0.968 | 1,545 | 0.073 |
| N (man-years, stacked) | 50,251 | 50,251 | 50,002 |
| Displaced fathers / control father-stacks | 489 / 9,408 | 489 / 9,408 | 489 / 9,408 |
| Clusters (fam68) | 690 | 690 | 690 |
| Displaced: mean of M / s.d. | 1.160 / 1.660 | 1.160 / 1.660 | 1.160 / 1.660 |
| **White, wife employed at baseline** | | | |
| Displaced, e=+1..+3 | -0.040** (0.020; p=0.043) | -28 (47; p=0.544) | -0.000 (0.011; p=0.996) |
| Displaced, pre | -0.015 (0.015; p=0.305) | -29 (40; p=0.471) | -0.004 (0.012; p=0.753) |
| Displaced x M, e=+1..+3 | -0.006 (0.021; p=0.771) | 51 (52; p=0.328) | -0.018 (0.013; p=0.153) |
| Displaced x M, pre | 0.003 (0.017; p=0.844) | 31 (46; p=0.493) | -0.017 (0.013; p=0.189) |
| Treated mean at e = -2, -1 | 0.962 | 1,371 | 0.037 |
| N (man-years, stacked) | 143,616 | 143,616 | 143,055 |
| Displaced fathers / control father-stacks | 709 / 24,836 | 709 / 24,836 | 709 / 24,836 |
| Clusters (fam68) | 1,350 | 1,350 | 1,350 |
| Displaced: mean of M / s.d. | 1.230 / 1.678 | 1.230 / 1.678 | 1.230 / 1.678 |
| Fixed effects | father x stack, calendar year x stack | father x stack, calendar year x stack | father x stack, calendar year x stack |

### 3e. (c') Change in the state unemployment rate in the displacement year

| | Wife employed | Wife's hours | Wife unemployed, looking (interview) |
|---|---|---|---|
| **Black** | | | |
| Displaced, e=+1..+3 | 0.018 (0.021; p=0.377) | 41 (45; p=0.370) | -0.005 (0.016; p=0.774) |
| Displaced, pre | 0.021 (0.019; p=0.275) | 2 (37; p=0.967) | -0.007 (0.017; p=0.675) |
| Displaced x M, e=+1..+3 | 0.022 (0.022; p=0.313) | 33 (45; p=0.460) | -0.004 (0.016; p=0.820) |
| Displaced x M, pre | 0.042** (0.019; p=0.028) | 84** (40; p=0.036) | 0.001 (0.017; p=0.951) |
| Treated mean at e = -2, -1 | 0.775 | 1,224 | 0.081 |
| N (man-years, stacked) | 73,646 | 73,646 | 70,952 |
| Displaced fathers / control father-stacks | 693 / 13,436 | 693 / 13,436 | 689 / 13,385 |
| Clusters (fam68) | 780 | 780 | 777 |
| Displaced: mean of M / s.d. | 0.128 / 1.348 | 0.128 / 1.348 | 0.128 / 1.348 |
| **White** | | | |
| Displaced, e=+1..+3 | 0.011 (0.020; p=0.585) | 58 (36; p=0.106) | 0.007 (0.008; p=0.427) |
| Displaced, pre | -0.019 (0.015; p=0.214) | -6 (29; p=0.847) | 0.002 (0.009; p=0.797) |
| Displaced x M, e=+1..+3 | -0.003 (0.021; p=0.894) | -29 (37; p=0.445) | 0.002 (0.010; p=0.869) |
| Displaced x M, pre | -0.010 (0.016; p=0.557) | -40 (30; p=0.184) | 0.006 (0.009; p=0.544) |
| Treated mean at e = -2, -1 | 0.719 | 999 | 0.034 |
| N (man-years, stacked) | 214,261 | 214,261 | 207,796 |
| Displaced fathers / control father-stacks | 1,074 / 36,528 | 1,074 / 36,528 | 1,072 / 36,476 |
| Clusters (fam68) | 1,477 | 1,477 | 1,473 |
| Displaced: mean of M / s.d. | 0.186 / 1.398 | 0.186 / 1.398 | 0.186 / 1.398 |
| **Black, wife not employed at baseline** | | | |
| Displaced, e=+1..+3 | 0.059 (0.055; p=0.289) | 66 (83; p=0.422) | 0.047 (0.043; p=0.273) |
| Displaced, pre | -0.024 (0.054; p=0.658) | -35 (72; p=0.621) | 0.030 (0.047; p=0.518) |
| Displaced x M, e=+1..+3 | 0.041 (0.053; p=0.446) | 98 (78; p=0.210) | -0.005 (0.044; p=0.914) |
| Displaced x M, pre | 0.013 (0.056; p=0.816) | 14 (68; p=0.843) | -0.018 (0.048; p=0.704) |
| Treated mean at e = -2, -1 | 0.081 | 66 | 0.114 |
| N (man-years, stacked) | 16,665 | 16,665 | 15,690 |
| Displaced fathers / control father-stacks | 146 / 2,757 | 146 / 2,757 | 144 / 2,739 |
| Clusters (fam68) | 476 | 476 | 472 |
| Displaced: mean of M / s.d. | 0.016 / 1.410 | 0.016 / 1.410 | 0.016 / 1.410 |
| **White, wife not employed at baseline** | | | |
| Displaced, e=+1..+3 | 0.103** (0.045; p=0.021) | 215*** (59; p=<0.001) | 0.019 (0.013; p=0.139) |
| Displaced, pre | -0.030 (0.034; p=0.368) | 15 (40; p=0.716) | 0.016 (0.013; p=0.197) |
| Displaced x M, e=+1..+3 | 0.011 (0.050; p=0.824) | 25 (58; p=0.671) | 0.014 (0.015; p=0.336) |
| Displaced x M, pre | -0.007 (0.036; p=0.842) | -38 (41; p=0.356) | 0.008 (0.012; p=0.488) |
| Treated mean at e = -2, -1 | 0.112 | 75 | 0.032 |
| N (man-years, stacked) | 52,766 | 52,766 | 50,246 |
| Displaced fathers / control father-stacks | 289 / 8,353 | 289 / 8,353 | 287 / 8,335 |
| Clusters (fam68) | 1,059 | 1,059 | 1,057 |
| Displaced: mean of M / s.d. | 0.198 / 1.248 | 0.198 / 1.248 | 0.198 / 1.248 |
| **Black, wife employed at baseline** | | | |
| Displaced, e=+1..+3 | 0.010 (0.020; p=0.592) | 39 (53; p=0.459) | -0.017 (0.017; p=0.309) |
| Displaced, pre | 0.034* (0.018; p=0.061) | 11 (43; p=0.793) | -0.018 (0.019; p=0.343) |
| Displaced x M, e=+1..+3 | 0.010 (0.019; p=0.607) | 0 (49; p=0.998) | 0.001 (0.017; p=0.962) |
| Displaced x M, pre | 0.028 (0.018; p=0.118) | 76 (47; p=0.106) | 0.009 (0.018; p=0.601) |
| Treated mean at e = -2, -1 | 0.963 | 1,537 | 0.072 |
| N (man-years, stacked) | 56,972 | 56,972 | 55,254 |
| Displaced fathers / control father-stacks | 547 / 10,678 | 547 / 10,678 | 545 / 10,645 |
| Clusters (fam68) | 732 | 732 | 729 |
| Displaced: mean of M / s.d. | 0.158 / 1.330 | 0.158 / 1.330 | 0.158 / 1.330 |
| **White, wife employed at baseline** | | | |
| Displaced, e=+1..+3 | -0.035* (0.019; p=0.062) | -10 (44; p=0.822) | 0.002 (0.010; p=0.873) |
| Displaced, pre | -0.012 (0.014; p=0.373) | -14 (37; p=0.710) | -0.003 (0.011; p=0.775) |
| Displaced x M, e=+1..+3 | -0.005 (0.019; p=0.777) | -46 (45; p=0.306) | -0.004 (0.012; p=0.758) |
| Displaced x M, pre | -0.006 (0.015; p=0.692) | -34 (37; p=0.367) | 0.004 (0.013; p=0.745) |
| Treated mean at e = -2, -1 | 0.961 | 1,366 | 0.035 |
| N (man-years, stacked) | 161,495 | 161,495 | 157,550 |
| Displaced fathers / control father-stacks | 785 / 28,175 | 785 / 28,175 | 785 / 28,141 |
| Clusters (fam68) | 1,399 | 1,399 | 1,397 |
| Displaced: mean of M / s.d. | 0.182 / 1.449 | 0.182 / 1.449 | 0.182 / 1.449 |
| Fixed effects | father x stack, calendar year x stack | father x stack, calendar year x stack | father x stack, calendar year x stack |

### 3f. Wife's search (read from output/wife_search.csv, 21.WifeSearch.py; not re-estimated)

Same stacked design; status outcomes at the spring interview (reference = interview a year before), calendar-year unemployment as in 19. Copied from that file for comparison.

| | Employed (interview) | Looking / unemployed (interview) | In labor force (interview) | Any unemployment in year | Weeks unemployed in year | Job finding (not employed before) | Employed after looking |
|---|---|---|---|---|---|---|---|
| **Black, all wives** | | | | | | | |
| Displaced, mean +1..+3 [displaced fathers] | 0.043 (0.026; p=0.103) [633] | -0.011 (0.017; p=0.495) [633] | 0.031 (0.024; p=0.198) [633] | 0.063*** (0.021; p=0.004) [715] | 1.187** (0.541; p=0.028) [715] | 0.029 (0.046; p=0.523) [329] | -0.186 (0.122; p=0.128) [140] |
| **Black, wife employed at baseline** | | | | | | | |
| Displaced, mean +1..+3 [displaced fathers] | -0.014 (0.023; p=0.544) [359] | 0.007 (0.011; p=0.532) [359] | -0.007 (0.020; p=0.717) [359] | 0.049* (0.028; p=0.082) [359] | 0.688 (0.742; p=0.354) [359] | 0.015 (0.075; p=0.839) [116] | -0.132 (0.152; p=0.386) [51] |
| **Black, wife not employed at baseline** | | | | | | | |
| Displaced, mean +1..+3 [displaced fathers] | 0.076* (0.041; p=0.065) [213] | -0.016 (0.040; p=0.681) [213] | 0.060 (0.049; p=0.224) [213] | 0.093** (0.046; p=0.042) [213] | 2.421* (1.256; p=0.054) [213] | 0.041 (0.034; p=0.220) [192] | -0.015 (0.116; p=0.898) [77] |
| **White, all wives** | | | | | | | |
| Displaced, mean +1..+3 [displaced fathers] | 0.048** (0.019; p=0.013) [1010] | 0.005 (0.008; p=0.560) [1010] | 0.053*** (0.019; p=0.006) [1010] | 0.018 (0.014; p=0.185) [1104] | 0.417 (0.296; p=0.159) [1104] | 0.058* (0.030; p=0.053) [584] | 0.383*** (0.145; p=0.008) [132] |
| **White, wife employed at baseline** | | | | | | | |
| Displaced, mean +1..+3 [displaced fathers] | -0.039** (0.018; p=0.028) [576] | 0.014** (0.006; p=0.017) [576] | -0.025 (0.017; p=0.134) [576] | 0.030* (0.018; p=0.094) [576] | 0.403 (0.361; p=0.264) [576] | 0.011 (0.044; p=0.802) [199] | 0.018 (0.235; p=0.939) [47] |
| **White, wife not employed at baseline** | | | | | | | |
| Displaced, mean +1..+3 [displaced fathers] | 0.075*** (0.027; p=0.006) [382] | -0.004 (0.017; p=0.831) [382] | 0.072** (0.030; p=0.017) [382] | 0.000 (0.025; p=0.986) [382] | 0.748 (0.493; p=0.129) [382] | 0.059*** (0.022; p=0.006) [363] | 0.213 (0.144; p=0.137) [78] |

## 4. Decomposition of the Black-White difference in the wife's response

### 4a. (i) The joint-shock channel (accounting)

Wives employed at baseline (the only ones who can lose a job). J = the wife's hours fall to zero in ev / ev+1 or she reports a closure / layoff in ev-1..ev+1. The response decomposes as r = (P1 - P0) x cost + P1 x (response | J = 1) + (1 - P1) x (response | J = 0), with P1 / P0 = share with J among displaced / control families and cost = the change in the outcome at e = +1..+3 that comes with J among controls (bin x J coefficient in the model with displaced x bin x J). The gap accounted for by the joint shock = the difference between Black and White excess probabilities (P1 - P0) times the cost: how much larger the Black response would be if Black wives' excess joint-loss probability were the White one. J is an outcome, so this is an accounting decomposition, not a causal one; s.e. of the channel treat P1 - P0 as fixed.

| | Estimate |
|---|---|
| **(i) Joint shock, wives employed at baseline: Wife's hours** | |
| Response, Black (e=+1..+3) | 34 (47; p=0.479) |
| Response, White (e=+1..+3) | 8 (39; p=0.845) |
| Gap, White - Black | -26 (61; p=0.672) |
| P(joint job loss): displaced / controls, Black | 0.222 / 0.179 |
| P(joint job loss): displaced / controls, White | 0.270 / 0.168 |
| Cost of a job loss for the wife's outcome (controls), Black | -507*** (34; p=<0.001) |
| Cost of a job loss for the wife's outcome (controls), White | -550*** (21; p=<0.001) |
| Joint-shock channel (excess P x cost), Black | -21*** (1; p=<0.001) |
| Joint-shock channel (excess P x cost), White | -56*** (2; p=<0.001) |
| Part of the White - Black gap due to the Black - White difference in excess P (Black cost / White cost) | -30.286 / -32.820 (share of gap 1.16 / 1.26) |
| Response with no joint loss (J=0), Black / White | 21 (46; p=0.645) / 81** (41; p=0.048) |
| N (man-years) Black / White | 64,495 / 183,950 |
| Displaced fathers Black / White | 510 / 807 |
| **(i) Joint shock, wives employed at baseline: Wife employed** | |
| Response, Black (e=+1..+3) | 0.018 (0.019; p=0.348) |
| Response, White (e=+1..+3) | -0.036** (0.018; p=0.045) |
| Gap, White - Black | -0.054** (0.026; p=0.039) |
| P(joint job loss): displaced / controls, Black | 0.222 / 0.179 |
| P(joint job loss): displaced / controls, White | 0.270 / 0.168 |
| Cost of a job loss for the wife's outcome (controls), Black | -0.312*** (0.018; p=<0.001) |
| Cost of a job loss for the wife's outcome (controls), White | -0.375*** (0.012; p=<0.001) |
| Joint-shock channel (excess P x cost), Black | -0.013*** (0.001; p=<0.001) |
| Joint-shock channel (excess P x cost), White | -0.038*** (0.001; p=<0.001) |
| Part of the White - Black gap due to the Black - White difference in excess P (Black cost / White cost) | -0.019 / -0.022 (share of gap 0.35 / 0.41) |
| Response with no joint loss (J=0), Black / White | -0.006 (0.017; p=0.714) / -0.016 (0.015; p=0.296) |
| N (man-years) Black / White | 64,495 / 183,950 |
| Displaced fathers Black / White | 510 / 807 |

### 4b. (ii) Demand in the wife's sector and area, and (i) the joint loss, in one pooled model

Pooled Black + White stacked DiD (event years 1980-2019, state observed), wife present at baseline: displaced x bin, displaced x bin x Black, bin x Black (race-specific responses and trends), and for each moderator M: bin x M and displaced x bin x M with slopes common to both races (M centred at the displaced mean; continuous M in s.d. units). Contribution of M to the Black - White response = (Black - White mean of M among displaced families) x slope (Oaxaca with pooled slopes; s.e. by the delta method, mean differences fixed). Wife's sector growth is set to the displaced mean when her sector is unknown (indicator 'sector unknown' included). The joint loss J enters only for wives employed at baseline (0 otherwise) and is an outcome (accounting, not causal). A negative contribution means the moderator makes the Black response smaller than the White one.

| | Estimate |
|---|---|
| **All wives: Wife's hours** | |
| Black - White response, e=+1..+3 (no moderators) | -46 (61; p=0.450) |
| Black - White response, e=+1..+3 (with moderators) | -64 (59; p=0.280) |
| White response (no moderators) | 54 (39; p=0.168) |
| Wife in husband's sector: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | 0.001 / -29 (106; p=0.788) / -0 (0; p=0.788) |
| Wife's sector unknown: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | 0.016 / 30 (77; p=0.697) / 0 (1; p=0.697) |
| Women's growth, wife's sector (national): Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.026 / -26 (31; p=0.405) / 1 (1; p=0.405) |
| State women's Bartik: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.031 / 12 (41; p=0.762) / -0 (1; p=0.762) |
| Change in state unemployment rate: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.022 / -20 (36; p=0.582) / 0 (1; p=0.582) |
| Joint job loss (wives employed at baseline): Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.033 / -85 (102; p=0.406) / 3 (3; p=0.406) |
| Total contribution of the moderators to the Black - White response | 4 (4; p=0.333) |
| Gelbach: gap without - with moderators | 17.475 |
| N (man-years) / displaced / clusters | 250,169 / 1,568 / 2,055 |
| **All wives: Wife employed** | |
| Black - White response, e=+1..+3 (no moderators) | -0.008 (0.030; p=0.797) |
| Black - White response, e=+1..+3 (with moderators) | -0.017 (0.029; p=0.569) |
| White response (no moderators) | 0.004 (0.021; p=0.852) |
| Wife in husband's sector: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | 0.001 / -0.032 (0.047; p=0.504) / -0.000 (0.000; p=0.504) |
| Wife's sector unknown: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | 0.016 / -0.011 (0.048; p=0.826) / -0.000 (0.001; p=0.826) |
| Women's growth, wife's sector (national): Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.026 / -0.016 (0.015; p=0.274) / 0.000 (0.000; p=0.274) |
| State women's Bartik: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.031 / -0.009 (0.018; p=0.625) / 0.000 (0.001; p=0.625) |
| Change in state unemployment rate: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.022 / 0.001 (0.018; p=0.935) / -0.000 (0.000; p=0.935) |
| Joint job loss (wives employed at baseline): Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.033 / -0.007 (0.050; p=0.884) / 0.000 (0.002; p=0.884) |
| Total contribution of the moderators to the Black - White response | 0.001 (0.002; p=0.734) |
| Gelbach: gap without - with moderators | 0.009 |
| N (man-years) / displaced / clusters | 250,169 / 1,568 / 2,055 |
| **All wives: Wife unemployed, looking** | |
| Black - White response, e=+1..+3 (no moderators) | -0.007 (0.019; p=0.710) |
| Black - White response, e=+1..+3 (with moderators) | -0.009 (0.019; p=0.644) |
| White response (no moderators) | 0.003 (0.009; p=0.714) |
| Wife in husband's sector: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | 0.001 / -0.009 (0.025; p=0.712) / -0.000 (0.000; p=0.712) |
| Wife's sector unknown: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | 0.016 / 0.032 (0.024; p=0.192) / 0.000 (0.000; p=0.192) |
| Women's growth, wife's sector (national): Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.026 / -0.007 (0.008; p=0.349) / 0.000 (0.000; p=0.349) |
| State women's Bartik: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.031 / -0.012 (0.011; p=0.289) / 0.000 (0.000; p=0.289) |
| Change in state unemployment rate: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.022 / -0.010 (0.011; p=0.367) / 0.000 (0.000; p=0.367) |
| Joint job loss (wives employed at baseline): Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.033 / 0.001 (0.026; p=0.972) / -0.000 (0.001; p=0.972) |
| Total contribution of the moderators to the Black - White response | 0.001 (0.001; p=0.260) |
| Gelbach: gap without - with moderators | 0.002 |
| N (man-years) / displaced / clusters | 248,980 / 1,565 / 2,055 |
| **Wife not employed at baseline: Wife's hours** | |
| Black - White response, e=+1..+3 (no moderators) | -135 (114; p=0.234) |
| Black - White response, e=+1..+3 (with moderators) | -109 (109; p=0.321) |
| White response (no moderators) | 232*** (67; p=<0.001) |
| Wife in husband's sector: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.035 / 259 (394; p=0.511) / -9 (14; p=0.511) |
| Wife's sector unknown: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | 0.116 / -136 (112; p=0.225) / -16 (13; p=0.225) |
| Women's growth, wife's sector (national): Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | 0.057 / -7 (57; p=0.895) / -0 (3; p=0.895) |
| State women's Bartik: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | 0.038 / 22 (67; p=0.739) / 1 (3; p=0.739) |
| Change in state unemployment rate: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.196 / 50 (55; p=0.365) / -10 (11; p=0.365) |
| Total contribution of the moderators to the Black - White response | -34 (22; p=0.118) |
| Gelbach: gap without - with moderators | -26.873 |
| N (man-years) / displaced / clusters | 56,302 / 370 / 1,342 |
| **Wife not employed at baseline: Wife employed** | |
| Black - White response, e=+1..+3 (no moderators) | -0.048 (0.082; p=0.557) |
| Black - White response, e=+1..+3 (with moderators) | -0.036 (0.082; p=0.660) |
| White response (no moderators) | 0.098* (0.051; p=0.056) |
| Wife in husband's sector: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.035 / 0.156 (0.210; p=0.459) / -0.005 (0.007; p=0.459) |
| Wife's sector unknown: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | 0.116 / -0.081 (0.085; p=0.339) / -0.009 (0.010; p=0.339) |
| Women's growth, wife's sector (national): Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | 0.057 / -0.028 (0.039; p=0.461) / -0.002 (0.002; p=0.461) |
| State women's Bartik: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | 0.038 / 0.009 (0.049; p=0.859) / 0.000 (0.002; p=0.859) |
| Change in state unemployment rate: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.196 / 0.024 (0.046; p=0.606) / -0.005 (0.009; p=0.606) |
| Total contribution of the moderators to the Black - White response | -0.021 (0.015; p=0.152) |
| Gelbach: gap without - with moderators | -0.012 |
| N (man-years) / displaced / clusters | 56,302 / 370 / 1,342 |
| **Wife not employed at baseline: Wife unemployed, looking** | |
| Black - White response, e=+1..+3 (no moderators) | 0.018 (0.049; p=0.712) |
| Black - White response, e=+1..+3 (with moderators) | 0.012 (0.047; p=0.791) |
| White response (no moderators) | 0.017 (0.014; p=0.217) |
| Wife in husband's sector: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.035 / 0.035 (0.045; p=0.436) / -0.001 (0.002; p=0.436) |
| Wife's sector unknown: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | 0.116 / 0.037 (0.033; p=0.255) / 0.004 (0.004; p=0.255) |
| Women's growth, wife's sector (national): Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | 0.057 / -0.012 (0.014; p=0.422) / -0.001 (0.001; p=0.422) |
| State women's Bartik: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | 0.038 / -0.021 (0.026; p=0.410) / -0.001 (0.001; p=0.410) |
| Change in state unemployment rate: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.196 / -0.009 (0.020; p=0.661) / 0.002 (0.004; p=0.661) |
| Total contribution of the moderators to the Black - White response | 0.003 (0.005; p=0.508) |
| Gelbach: gap without - with moderators | 0.005 |
| N (man-years) / displaced / clusters | 55,923 / 367 / 1,341 |
| **Wife employed at baseline: Wife's hours** | |
| Black - White response, e=+1..+3 (no moderators) | 12 (71; p=0.862) |
| Black - White response, e=+1..+3 (with moderators) | -18 (69; p=0.794) |
| White response (no moderators) | -19 (47; p=0.685) |
| Wife in husband's sector: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | 0.004 / -73 (104; p=0.486) / -0 (0; p=0.486) |
| Wife's sector unknown: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | 0.023 / 72 (145; p=0.618) / 2 (3; p=0.618) |
| Women's growth, wife's sector (national): Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.046 / -24 (35; p=0.490) / 1 (2; p=0.490) |
| State women's Bartik: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.042 / 12 (48; p=0.808) / -0 (2; p=0.808) |
| Change in state unemployment rate: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | 0.027 / -50 (43; p=0.243) / -1 (1; p=0.243) |
| Joint job loss (wives employed at baseline): Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.059 / -32 (107; p=0.762) / 2 (6; p=0.762) |
| Total contribution of the moderators to the Black - White response | 3 (8; p=0.758) |
| Gelbach: gap without - with moderators | 30.374 |
| N (man-years) / displaced / clusters | 193,867 / 1,198 / 1,955 |
| **Wife employed at baseline: Wife employed** | |
| Black - White response, e=+1..+3 (no moderators) | 0.028 (0.028; p=0.316) |
| Black - White response, e=+1..+3 (with moderators) | 0.010 (0.027; p=0.704) |
| White response (no moderators) | -0.040** (0.020; p=0.040) |
| Wife in husband's sector: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | 0.004 / -0.063 (0.041; p=0.122) / -0.000 (0.000; p=0.122) |
| Wife's sector unknown: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | 0.023 / 0.035 (0.071; p=0.624) / 0.001 (0.002; p=0.624) |
| Women's growth, wife's sector (national): Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.046 / -0.010 (0.013; p=0.413) / 0.000 (0.001; p=0.413) |
| State women's Bartik: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.042 / -0.009 (0.016; p=0.580) / 0.000 (0.001; p=0.580) |
| Change in state unemployment rate: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | 0.027 / -0.009 (0.016; p=0.577) / -0.000 (0.000; p=0.577) |
| Joint job loss (wives employed at baseline): Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.059 / 0.037 (0.049; p=0.452) / -0.002 (0.003; p=0.452) |
| Total contribution of the moderators to the Black - White response | -0.001 (0.004; p=0.783) |
| Gelbach: gap without - with moderators | 0.018 |
| N (man-years) / displaced / clusters | 193,867 / 1,198 / 1,955 |
| **Wife employed at baseline: Wife unemployed, looking** | |
| Black - White response, e=+1..+3 (no moderators) | -0.011 (0.021; p=0.599) |
| Black - White response, e=+1..+3 (with moderators) | -0.012 (0.021; p=0.574) |
| White response (no moderators) | -0.002 (0.011; p=0.861) |
| Wife in husband's sector: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | 0.004 / -0.015 (0.027; p=0.590) / -0.000 (0.000; p=0.590) |
| Wife's sector unknown: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | 0.023 / 0.026 (0.042; p=0.541) / 0.001 (0.001; p=0.541) |
| Women's growth, wife's sector (national): Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.046 / -0.007 (0.009; p=0.464) / 0.000 (0.000; p=0.464) |
| State women's Bartik: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.042 / -0.009 (0.013; p=0.493) / 0.000 (0.001; p=0.493) |
| Change in state unemployment rate: Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | 0.027 / -0.010 (0.014; p=0.473) / -0.000 (0.000; p=0.473) |
| Joint job loss (wives employed at baseline): Black - White mean among displaced (in s.d. units if continuous) / slope / contribution | -0.059 / 0.006 (0.027; p=0.818) / -0.000 (0.002; p=0.818) |
| Total contribution of the moderators to the Black - White response | 0.001 (0.002; p=0.796) |
| Gelbach: gap without - with moderators | 0.001 |
| N (man-years) / displaced / clusters | 193,057 / 1,198 / 1,955 |
