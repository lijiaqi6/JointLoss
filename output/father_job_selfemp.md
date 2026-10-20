# Fathers' jobs and self-employment (Fable review, Item 3)

Built by `43.FatherJobSelfEmployment.py` (2026-10-17); definitions in its docstring. Every coefficient: estimate (s.e.; p), *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**

## 0. Self-employment of fathers and sons

| | Black | White |
|---|---|---|
| sons with a father's self-employment code | 899 of 1,928 | 2,267 of 2,719 |
| father self-employed (>= half of his waves) | 0.083 | 0.207 |
| father ever self-employed | 0.192 | 0.360 |
| son-years self-employed, 25-34 | 0.074 | 0.106 |
| son-years self-employed, 35-55 | 0.094 | 0.151 |
| son-years in the father's cell, 25-34: N / son self-employed / father self-employed | 219 / 0.060 / 0.083 | 809 / 0.232 / 0.424 |
| son-years not in the father's cell, 25-34: son SE / father SE | 0.069 / 0.081 | 0.102 / 0.201 |
| son-years in the father's cell, 35-55: N / son self-employed / father self-employed | 167 / 0.060 / 0.127 | 620 / 0.277 / 0.399 |
| son-years not in the father's cell, 35-55: son SE / father SE | 0.097 / 0.084 | 0.146 / 0.201 |

### 0b. The father-son cells held at 35-55 (top 12 by son-years)

| occupation group x industry group code | son-years | sons | son self-employed | father self-employed | White share | mean ln parental income |
|---|---|---|---|---|---|---|
| 6 x 0 | 137 | 31 | 0.56 | 0.75 | 0.93 | 10.83 |
| 7 x 2 | 102 | 28 | 0.26 | 0.55 | 0.68 | 10.87 |
| 9 x 13 | 81 | 17 | 0.10 | 0.00 | 0.40 | 11.06 |
| 0 x 2 | 57 | 13 | 0.39 | 0.46 | 1.00 | 11.55 |
| 1 x 29 | 39 | 10 | 0.13 | 0.00 | 0.82 | 11.35 |
| 4 x 32 | 26 | 4 | 0.00 | 0.00 | 0.46 | 11.07 |
| 5 x 32 | 25 | 6 | 0.00 | 0.00 | 0.96 | 11.07 |
| 1 x 31 | 24 | 4 | 0.08 | 0.67 | 1.00 | 11.63 |
| 9 x 2 | 17 | 5 | 0.06 | 0.06 | 1.00 | 10.68 |
| 6 x 7 | 17 | 5 | 0.00 | 0.00 | 0.82 | 10.18 |
| 3 x 20 | 17 | 3 | 0.47 | 0.76 | 1.00 | 11.51 |
| 8 x 4 | 16 | 4 | 0.06 | 0.00 | 0.00 | 10.69 |

Occupation groups (27's 11 groups) and industry groups (32's 33) are numbered as in those scripts (occ11: see 27.CareerWageGrowth.group_of; igrp: 32.IGRP).

## 1. Son in the father's cell on ln parental income, by self-employment

Son-year LPMs; Lee-Solon controls; clusters 1968 family; pooled weighted, races unweighted. The change row is from one regression on 25-55 with ln parental income x (age >= 35) and the age >= 35 dummy.

| | (1) All sons (35) | (2) Father not self-employed | (3) Father self-employed | (4) Son-years not self-employed | (5) Neither father nor son self-employed | (6) Father's code known (any) |
|---|---|---|---|---|---|---|
| **Pooled (weighted)** | | | | | | |
| ln parental income, 25-34 | 0.004 (0.012; p=0.753) | -0.006 (0.012; p=0.603) | 0.009 (0.023; p=0.674) | 0.003 (0.012; p=0.782) | -0.005 (0.013; p=0.689) | 0.005 (0.011; p=0.647) |
| ln parental income, 35-55 | 0.031** (0.016; p=0.048) | 0.009 (0.016; p=0.565) | 0.072*** (0.025; p=0.004) | 0.015 (0.017; p=0.384) | 0.008 (0.018; p=0.671) | 0.036*** (0.014; p=0.009) |
| change: ln parental income x (age >= 35) | 0.023** (0.010; p=0.018) | 0.009 (0.011; p=0.412) | 0.065*** (0.021; p=0.002) | 0.005 (0.011; p=0.648) | 0.005 (0.012; p=0.711) | 0.028*** (0.010; p=0.005) |
| N son-years / sons at 35-55; mean | 13,835 / 2,166; mean 0.056 | 10,539 / 1,683; mean 0.042 | 2,399 / 373; mean 0.110 | 11,891 / 2,005; mean 0.047 | 9,324 / 1,579; mean 0.046 | 12,938 / 2,056; mean 0.057 |
| **Black** | | | | | | |
| ln parental income, 25-34 | -0.014 (0.020; p=0.484) | -0.028 (0.025; p=0.260) | -0.030 (0.049; p=0.537) | -0.014 (0.021; p=0.498) | -0.025 (0.026; p=0.332) | -0.027 (0.023; p=0.240) |
| ln parental income, 35-55 | 0.012 (0.020; p=0.557) | 0.013 (0.023; p=0.586) | -0.002 (0.058; p=0.973) | 0.004 (0.022; p=0.835) | 0.005 (0.024; p=0.827) | 0.013 (0.021; p=0.544) |
| change: ln parental income x (age >= 35) | 0.026 (0.020; p=0.187) | 0.042* (0.022; p=0.054) | 0.026 (0.064; p=0.685) | 0.018 (0.020; p=0.365) | 0.032 (0.022; p=0.142) | 0.041** (0.021; p=0.048) |
| N son-years / sons at 35-55; mean | 3,171 / 568; mean 0.053 | 2,553 / 473; mean 0.054 | 242 / 44; mean 0.083 | 2,869 / 532; mean 0.055 | 2,309 / 446; mean 0.055 | 2,795 / 517; mean 0.056 |
| **White** | | | | | | |
| ln parental income, 25-34 | -0.005 (0.014; p=0.736) | -0.011 (0.014; p=0.454) | -0.005 (0.025; p=0.855) | -0.002 (0.014; p=0.867) | -0.007 (0.015; p=0.638) | -0.003 (0.013; p=0.834) |
| ln parental income, 35-55 | 0.025 (0.020; p=0.201) | 0.006 (0.020; p=0.768) | 0.065** (0.025; p=0.010) | 0.011 (0.022; p=0.625) | 0.006 (0.023; p=0.792) | 0.033** (0.016; p=0.038) |
| change: ln parental income x (age >= 35) | 0.026** (0.012; p=0.026) | 0.009 (0.012; p=0.488) | 0.073*** (0.022; p=0.001) | 0.007 (0.014; p=0.592) | 0.004 (0.015; p=0.809) | 0.032*** (0.011; p=0.004) |
| N son-years / sons at 35-55; mean | 10,665 / 1,599; mean 0.058 | 7,986 / 1,210; mean 0.045 | 2,158 / 330; mean 0.111 | 9,023 / 1,474; mean 0.050 | 7,015 / 1,133; mean 0.049 | 10,144 / 1,540; mean 0.059 |

## 1. Son in the father's occupation group on ln parental income, by self-employment

Son-year LPMs; Lee-Solon controls; clusters 1968 family; pooled weighted, races unweighted. The change row is from one regression on 25-55 with ln parental income x (age >= 35) and the age >= 35 dummy.

| | (1) All sons (35) | (2) Father not self-employed | (3) Father self-employed | (4) Son-years not self-employed | (5) Neither father nor son self-employed | (6) Father's code known (any) |
|---|---|---|---|---|---|---|
| **Pooled (weighted)** | | | | | | |
| ln parental income, 25-34 | 0.051*** (0.016; p=0.001) | 0.040** (0.019; p=0.035) | 0.067** (0.030; p=0.026) | 0.046*** (0.016; p=0.004) | 0.037* (0.019; p=0.057) | 0.053*** (0.016; p=<0.001) |
| ln parental income, 35-55 | 0.099*** (0.020; p=<0.001) | 0.071*** (0.026; p=0.006) | 0.163*** (0.027; p=<0.001) | 0.091*** (0.022; p=<0.001) | 0.072*** (0.027; p=0.008) | 0.104*** (0.020; p=<0.001) |
| change: ln parental income x (age >= 35) | 0.052*** (0.016; p=<0.001) | 0.037* (0.021; p=0.075) | 0.104*** (0.026; p=<0.001) | 0.046*** (0.018; p=0.009) | 0.038* (0.022; p=0.090) | 0.056*** (0.016; p=<0.001) |
| N son-years / sons at 35-55; mean | 13,908 / 2,174; mean 0.219 | 10,604 / 1,691; mean 0.216 | 2,404 / 373; mean 0.229 | 11,958 / 2,014; mean 0.205 | 9,383 / 1,588; mean 0.209 | 13,008 / 2,064; mean 0.218 |
| **Black** | | | | | | |
| ln parental income, 25-34 | -0.013 (0.024; p=0.590) | -0.039 (0.028; p=0.163) | 0.111 (0.089; p=0.210) | -0.016 (0.025; p=0.527) | -0.036 (0.029; p=0.219) | -0.027 (0.026; p=0.305) |
| ln parental income, 35-55 | 0.024 (0.025; p=0.332) | -0.004 (0.028; p=0.892) | 0.188 (0.138; p=0.174) | 0.021 (0.026; p=0.422) | 0.000 (0.028; p=0.989) | 0.015 (0.026; p=0.574) |
| change: ln parental income x (age >= 35) | 0.036 (0.028; p=0.200) | 0.040 (0.032; p=0.209) | 0.082 (0.105; p=0.436) | 0.037 (0.030; p=0.210) | 0.043 (0.032; p=0.180) | 0.044 (0.031; p=0.154) |
| N son-years / sons at 35-55; mean | 3,194 / 570; mean 0.153 | 2,575 / 475; mean 0.158 | 242 / 44; mean 0.178 | 2,890 / 535; mean 0.150 | 2,329 / 449; mean 0.152 | 2,817 / 519; mean 0.160 |
| **White** | | | | | | |
| ln parental income, 25-34 | 0.040** (0.018; p=0.025) | 0.035 (0.022; p=0.109) | 0.042 (0.032; p=0.186) | 0.038** (0.018; p=0.040) | 0.033 (0.022; p=0.136) | 0.042** (0.018; p=0.017) |
| ln parental income, 35-55 | 0.099*** (0.023; p=<0.001) | 0.073** (0.029; p=0.011) | 0.161*** (0.027; p=<0.001) | 0.095*** (0.026; p=<0.001) | 0.076** (0.029; p=0.010) | 0.107*** (0.021; p=<0.001) |
| change: ln parental income x (age >= 35) | 0.060*** (0.017; p=<0.001) | 0.039* (0.022; p=0.078) | 0.124*** (0.028; p=<0.001) | 0.054*** (0.020; p=0.007) | 0.041* (0.024; p=0.091) | 0.067*** (0.017; p=<0.001) |
| N son-years / sons at 35-55; mean | 10,715 / 1,605; mean 0.224 | 8,029 / 1,216; mean 0.220 | 2,163 / 330; mean 0.233 | 9,069 / 1,480; mean 0.210 | 7,054 / 1,139; mean 0.215 | 10,192 / 1,546; mean 0.223 |

## 2. Rich White vs rich Black sons in the father's occupation / cell at 35-55, by self-employment

As 35 F7(b): race x pooled parental-income tercile cells (reference Black tercile 1) + ln parental income, Lee-Solon controls, pooled weighted, clusters 1968 family.

| | (1) All sons (35) | (2) Father not self-employed | (3) Father self-employed | (4) Son-years not self-employed | (5) Neither father nor son self-employed | (6) Father's code known (any) |
|---|---|---|---|---|---|---|
| **Outcome: son in the father's occupation group, 35-55** | | | | | | |
| rich White - rich Black (tercile 3) | 0.117*** (0.038; p=0.002) | 0.117*** (0.040; p=0.003) | -0.019 (0.143; p=0.897) | 0.103** (0.041; p=0.012) | 0.113*** (0.043; p=0.008) | 0.116*** (0.039; p=0.003) |
| rich White - poor White (tercile 3 - tercile 1) | -0.086 (0.061; p=0.158) | -0.151* (0.079; p=0.056) | 0.052 (0.090; p=0.564) | -0.082 (0.066; p=0.218) | -0.145* (0.084; p=0.086) | -0.090 (0.062; p=0.146) |
| N son-years / sons | 13,908 / 2,174 | 10,604 / 1,691 | 2,404 / 373 | 11,958 / 2,014 | 9,383 / 1,588 | 13,008 / 2,064 |
| Black sons in tercile 3 | 121 | 112 | 9 | 112 | 105 | 121 |
| **Outcome: son in the father's cell, 35-55** | | | | | | |
| rich White - rich Black (tercile 3) | 0.011 (0.029; p=0.707) | -0.008 (0.030; p=0.789) | 0.131*** (0.033; p=<0.001) | 0.003 (0.031; p=0.932) | -0.004 (0.033; p=0.893) | 0.011 (0.029; p=0.702) |
| rich White - poor White (tercile 3 - tercile 1) | -0.055 (0.047; p=0.236) | -0.060 (0.057; p=0.291) | 0.066 (0.088; p=0.451) | -0.039 (0.050; p=0.443) | -0.072 (0.066; p=0.282) | -0.053 (0.047; p=0.255) |
| N son-years / sons | 13,835 / 2,166 | 10,539 / 1,683 | 2,399 / 373 | 11,891 / 2,005 | 9,324 / 1,579 | 12,938 / 2,056 |
| Black sons in tercile 3 | 120 | 111 | 9 | 111 | 104 | 120 |

## 3. Within sons: keeping the father's cell, by self-employment (35 F8)

Sons with a modal cell in both 25-34 and 35-55 and a father's cell. Counts, then LPMs of leaving (in at 25-34, out at 35-55) and entering on ln parental income with a quadratic in birth cohort; clusters 1968 family; unweighted.

| Group | sons | in at both (stay) | leave | enter | stayers: son self-employed at 35-55 | stayers: father self-employed | all sons: son SE / father SE |
|---|---|---|---|---|---|---|---|
| All | 2,029 | 84 | 53 | 39 | 0.29 (n=84) | 0.41 (n=83) | 0.15 / 0.18 |
| Black | 502 | 9 | 16 | 12 | 0.00 (n=9) | 0.11 (n=9) | 0.12 / 0.08 |
| White | 1,527 | 75 | 37 | 27 | 0.32 (n=75) | 0.45 (n=74) | 0.16 / 0.22 |

| Sample | (1) leave on ln parental income | N sons (in at 25-34) | (2) enter on ln parental income | N sons (out at 25-34) |
|---|---|---|---|---|
| All | -0.206*** (0.066; p=0.002) | 137 | 0.003 (0.008; p=0.677) | 1,892 |
| Father not self-employed | -0.183** (0.080; p=0.023) | 90 | -0.007 (0.010; p=0.468) | 1,489 |
| Father self-employed | -0.223* (0.126; p=0.076) | 46 | 0.025 (0.020; p=0.198) | 309 |
| Son not self-employed at 35-55 | -0.131* (0.079; p=0.096) | 100 | -0.007 (0.008; p=0.413) | 1,620 |
| Neither self-employed | -0.163** (0.079; p=0.040) | 82 | -0.009 (0.012; p=0.420) | 1,289 |

