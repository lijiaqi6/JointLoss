# The EITC in childhood: first stage, eligibility, the 1993-96 expansion, daughters (committee memo H1)

Built by `126.EITCDesign.py` (2026-10-24); design in its docstring. Exposure in thousands of 2000 dollars; s.e. clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1. **Intent to treat; descriptive.**

Window years 1975+: 15,729 (sons 3,879); eligible (earned income in the credit's range) 0.243; predicted eligibility: mean 0.251, top-tercile cut 0.264; eligible share in the top tercile 0.544 vs others 0.102; logit pseudo-R2 0.209.

## 1. First stage: the mother's work and the family's earnings in the window year on that year's maximum credit

| outcome | all window years | likely eligible | others |
|---|---|---|---|
| mother employed | -0.0089 (0.0114; p=0.438) [15,311] | 0.0154 (0.0234; p=0.511) [4,585] | -0.0198 (0.0130; p=0.128) [10,331] |
| mother's annual hours | -28.7586 (27.1203; p=0.289) [15,311] | 39.5224 (49.3193; p=0.423) [4,585] | -58.0503* (32.5767; p=0.075) [10,331] |
| ln family earned income | -0.0408 (0.0296; p=0.168) [14,456] | 0.0623 (0.0538; p=0.248) [3,724] | 0.0061 (0.0259; p=0.814) [10,351] |
| earned income in the credit's range | 0.0624*** (0.0118; p=<0.001) [15,729] | 0.0773*** (0.0245; p=0.002) [4,715] | 0.0241** (0.0100; p=0.015) [10,601] |

## 2. Reduced form by predicted eligibility (ln earnings, ln parental income held fixed)
### likely eligible (top tercile)

| | 25-29 | 30-34 | 35-39 | 40-44 | change 40-44 - 25-29 | within son x age | sons |
|---|---|---|---|---|---|---|---|
| exposure (1,000 2000 $ over 13-18) | -0.0052 (0.0132; p=0.692) | -0.0100 (0.0176; p=0.571) | 0.0079 (0.0220; p=0.721) | 0.0269 (0.0365; p=0.461) | 0.0321 (0.0362; p=0.375) | 0.0637*** (0.0172; p=<0.001) | 900 |

### others

| | 25-29 | 30-34 | 35-39 | 40-44 | change 40-44 - 25-29 | within son x age | sons |
|---|---|---|---|---|---|---|---|
| exposure (1,000 2000 $ over 13-18) | -0.0098 (0.0088; p=0.267) | -0.0061 (0.0096; p=0.523) | -0.0047 (0.0136; p=0.729) | -0.0002 (0.0185; p=0.993) | 0.0096 (0.0190; p=0.614) | 0.0173 (0.0108; p=0.110) | 1,933 |

### employed, likely eligible

| | 25-29 | 30-34 | 35-39 | 40-44 | change 40-44 - 25-29 | within son x age | sons |
|---|---|---|---|---|---|---|---|
| exposure (1,000 2000 $ over 13-18) | -0.0011 (0.0040; p=0.780) | -0.0088 (0.0076; p=0.245) | -0.0032 (0.0061; p=0.600) | -0.0284 (0.0188; p=0.131) | -0.0273 (0.0185; p=0.140) | -0.0095* (0.0056; p=0.088) | 948 |

## 3. The 1993-96 expansion: two or more children vs one, by the share of the window from 1994

| outcome | 25-29 | 30-34 | 35-39 | 40-44 |
|---|---|---|---|---|
| ln earnings | -0.0789 (0.0905; p=0.383) [1,455] | -0.0621 (0.0947; p=0.512) [1,469] | -0.0179 (0.1228; p=0.884) [1,253] | 0.0457 (0.1649; p=0.782) [824] |
| employed | -0.0232 (0.0200; p=0.247) [1,521] | -0.0081 (0.0236; p=0.730) [1,543] | 0.0308 (0.0292; p=0.290) [1,336] | 0.0283 (0.0580; p=0.626) [905] |

## 4. Daughters (107's frame)
### daughters, ln earnings

| | 25-29 | 30-34 | 35-39 | 40-44 | change 40-44 - 25-29 | within son x age | sons |
|---|---|---|---|---|---|---|---|
| exposure (1,000 2000 $ over 13-18) | 0.0278*** (0.0096; p=0.004) | -0.0036 (0.0111; p=0.744) | 0.0055 (0.0143; p=0.703) | 0.0138 (0.0243; p=0.569) | -0.0140 (0.0247; p=0.572) | -0.0156 (0.0099; p=0.114) | 1,976 |

### daughters, ln hourly wage

| | 25-29 | 30-34 | 35-39 | 40-44 | change 40-44 - 25-29 | within son x age | sons |
|---|---|---|---|---|---|---|---|
| exposure (1,000 2000 $ over 13-18) | 0.0123** (0.0063; p=0.049) | -0.0025 (0.0079; p=0.751) | -0.0071 (0.0103; p=0.488) | 0.0125 (0.0152; p=0.412) | 0.0001 (0.0155; p=0.993) | -0.0022 (0.0072; p=0.762) | 1,976 |

