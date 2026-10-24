# Why no first stage of the EITC on mothers' work? (PI question)

Built by `127.EITCMothers.py` (2026-10-24); design in its docstring. *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**

## 1. The mothers in the sons' window years (1979+)

| mothers | window years | employed (hours > 0) | working at interview | temporarily laid off | unemployed, looking | keeping house | disabled / retired / student / other | looking among not working | imputed credit (1,000 2000 $) | in the credit's range |
|---|---|---|---|---|---|---|---|---|---|---|
| all | 12,904 | 0.805 | 0.712 | 0.009 | 0.050 | 0.189 | 0.041 | 0.178 | 0.328 | 0.245 |
| married | 9,397 | 0.809 | 0.725 | 0.006 | 0.025 | 0.215 | 0.029 | 0.093 | 0.171 | 0.137 |
| single | 3,507 | 0.795 | 0.677 | 0.017 | 0.113 | 0.121 | 0.072 | 0.369 | 0.748 | 0.537 |
| married, likely eligible | 1,074 | 0.694 | 0.585 | 0.008 | 0.054 | 0.308 | 0.044 | 0.132 | 0.759 | 0.513 |
| single, likely eligible | 2,748 | 0.763 | 0.635 | 0.018 | 0.131 | 0.140 | 0.076 | 0.377 | 0.821 | 0.576 |

## 2. First stage by marital status: outcome in the window year on that year's maximum credit (1,000 2000 $)

| outcome | married | single | married, likely eligible | single, likely eligible |
|---|---|---|---|---|
| employed | -0.0315** (0.0143; p=0.028) [9,033] | 0.0161 (0.0231; p=0.484) [3,507] | -0.0185 (0.0478; p=0.698) [948] | 0.0328 (0.0279; p=0.239) [2,748] |
| annual hours | -71.4145** (34.5173; p=0.039) [9,033] | 51.0523 (52.4471; p=0.330) [3,507] | -44.8531 (102.4642; p=0.662) [948] | 92.2435 (57.5995; p=0.109) [2,748] |
| ln wage (working) | 0.0352 (0.0248; p=0.155) [6,967] | -0.0368 (0.0355; p=0.300) [2,676] | 0.0129 (0.0664; p=0.846) [613] | -0.0371 (0.0377; p=0.326) [2,003] |
| looking for work, among not working | 0.0055 (0.0208; p=0.790) [2,429] | 0.0242 (0.0515; p=0.638) [1,075] | -0.0143 (0.0596; p=0.811) [385] | 0.0257 (0.0549; p=0.640) [952] |
| imputed credit received | 0.1155*** (0.0208; p=<0.001) [9,397] | 0.4978*** (0.0667; p=<0.001) [3,507] | 0.3441*** (0.0915; p=<0.001) [1,074] | 0.4999*** (0.0689; p=<0.001) [2,748] |
| ln family earned income | -0.0353 (0.0268; p=0.188) [9,184] | 0.0320 (0.0565; p=0.571) [2,778] | -0.0622 (0.0833; p=0.455) [1,009] | 0.0818 (0.0698; p=0.242) [2,095] |

## 3. Main reason for not looking: women with a child under 18, not working and not looking (2019-2023, all PSID families, unweighted)

| reason | all | single | married | earned income in the credit's range | not in range |
|---|---|---|---|---|---|
| family / child care | 0.489 | 0.256 | 0.578 | 0.540 | 0.467 |
| labor market | 0.032 | 0.070 | 0.017 | 0.019 | 0.037 |
| disability | 0.164 | 0.330 | 0.101 | 0.123 | 0.181 |
| in school | 0.035 | 0.044 | 0.031 | 0.035 | 0.035 |
| retired | 0.057 | 0.098 | 0.041 | 0.030 | 0.068 |
| other | 0.224 | 0.202 | 0.232 | 0.253 | 0.212 |
| n | 1,554 | 430 | 1,124 | 463 | 1,091 |

Labor-market reasons in detail (codes: 1 no work available in the area, 2 couldn't find any work, 3 lack schooling / training, 4 employers think too young or old, 5 other discrimination, 7 transportation): {2: 24, 1: 13, 7: 9, 3: 2, 5: 1}; family: 8 family responsibilities 693, 9 can't arrange child care 67.

## 4. Earlier items: non-working wives in families with a child under 18

1971 (782 wives not working, under 65): 'If your wife wanted to work, would she be able to find a job easily?' yes 0.596; yes, qualified 0.051; maybe / depends 0.017; no, qualified 0.033; no 0.303. 'Will she go to work in the near future?' yes 0.223, depends 0.133, no 0.641. 'What does that depend on / why?' (first mention, 761): health, disability, age 0.114; family, children, home 0.568; education, training 0.043; job-related (pay, no jobs in the area, transport) 0.074; need (no need now) 0.095; desire, husband objects 0.080; other 0.026.

Wives out of the labor force who think of getting a job: did anything in the last four weeks to find one: 1976 0.129 (464); 1981 0.215 (410); 1982 0.199 (381); 1983 0.256 (438).

