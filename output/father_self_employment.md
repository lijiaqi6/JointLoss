# Self-employed fathers and the delayed cost of a father's teen layoff (committee memo Z2)

Built by `119.FatherSelfEmployment.py` (2026-10-24); design in its docstring. Per unit teen layoff share; band s.e. from 200 cluster-bootstrap draws of 1968 families (common to all rows), within-son s.e. clustered by 1968 family. *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**

## 1. Self-employed fathers (father-present sons with a valid wage year)

| sample | sons | father self-employed (half+ of window waves) | ever self-employed in window | no valid code | mean layoff share: SE / other fathers | mean closure share: SE / other | treated sons with SE father |
|---|---|---|---|---|---|---|---|
| pooled | 3,386 | 0.185 | 0.269 | 0.026 | 0.020 / 0.051 | 0.017 / 0.028 | 34 of 430 |
| White | 2,370 | 0.199 | 0.288 | 0.019 | 0.020 / 0.050 | 0.017 / 0.029 | 25 of 291 |
| Black | 1,016 | 0.057 | 0.090 | 0.085 | 0.023 / 0.058 | 0.021 / 0.021 | 9 of 139 |

## 2. The layoff profile with and without self-employed fathers

| outcome | sample | 25-29 | 45-49 | change | closure change | layoff - closure | within son x age | sons | treated at 45-49 |
|---|---|---|---|---|---|---|---|---|---|
| ly | (a) all sons | 0.146 (0.101; p=0.148) | -0.768*** (0.263; p=0.004) | -0.914*** (0.244; p<0.001) | 0.000 (0.277; p=0.999) | -0.914*** (0.326; p=0.005) | -0.236** (0.103; p=0.022) | 4,644 | 135 |
| ly | (b) without SE fathers | 0.119 (0.103; p=0.248) | -0.760*** (0.275; p=0.006) | -0.880*** (0.253; p<0.001) | -0.026 (0.277; p=0.925) | -0.853** (0.332; p=0.010) | -0.295*** (0.091; p=0.001) | 4,097 | 127 |
| ly | (c) without fathers ever SE | 0.069 (0.109; p=0.528) | -0.843*** (0.286; p=0.003) | -0.912*** (0.266; p<0.001) | 0.190 (0.280; p=0.498) | -1.102*** (0.343; p=0.001) | -0.289*** (0.102; p=0.005) | 3,834 | 106 |
| ly | (d) all, father SE (x age) held fixed | 0.154 (0.101; p=0.128) | -0.742*** (0.256; p=0.004) | -0.896*** (0.240; p<0.001) | 0.018 (0.275; p=0.948) | -0.914*** (0.321; p=0.004) | -0.233** (0.101; p=0.020) | 4,644 | 135 |
| lw | (a) all sons | 0.046 (0.085; p=0.586) | -0.557*** (0.210; p=0.008) | -0.603*** (0.190; p=0.001) | 0.085 (0.213; p=0.688) | -0.688*** (0.264; p=0.009) | -0.109 (0.082; p=0.184) | 4,644 | 135 |
| lw | (b) without SE fathers | 0.023 (0.091; p=0.804) | -0.533** (0.217; p=0.014) | -0.555*** (0.199; p=0.005) | 0.087 (0.214; p=0.687) | -0.642** (0.270; p=0.018) | -0.134* (0.072; p=0.064) | 4,097 | 127 |
| lw | (c) without fathers ever SE | -0.019 (0.097; p=0.846) | -0.543** (0.228; p=0.017) | -0.524** (0.215; p=0.015) | 0.248 (0.217; p=0.253) | -0.773*** (0.278; p=0.005) | -0.069 (0.076; p=0.363) | 3,834 | 106 |
| lw | (d) all, father SE (x age) held fixed | 0.050 (0.085; p=0.559) | -0.542*** (0.204; p=0.008) | -0.592*** (0.186; p=0.001) | 0.100 (0.213; p=0.637) | -0.693*** (0.263; p=0.008) | -0.106 (0.080; p=0.185) | 4,644 | 135 |

## 3. Sons and daughters (107's stacked design)

| outcome | sample | sons: change | daughters: change | daughters - sons | sons: within x age | daughters: within x age | daughters - sons (within) | sons / daughters |
|---|---|---|---|---|---|---|---|---|
| lw | all | -0.538** (0.213; p=0.012) | 0.387* (0.214; p=0.070) | 0.925*** (0.290; p=0.001) | -0.086 (0.096; p=0.371) | 0.168** (0.075; p=0.025) | 0.254** (0.129; p=0.049) | 3,013 / 3,062 |
| lw | without SE fathers | -0.472** (0.214; p=0.027) | 0.301 (0.217; p=0.166) | 0.773** (0.301; p=0.010) | -0.088 (0.087; p=0.312) | 0.171** (0.082; p=0.037) | 0.259** (0.121; p=0.033) | 2,561 / 2,575 |
| lw | all, father SE held fixed | -0.510** (0.210; p=0.015) | 0.390* (0.215; p=0.069) | 0.901*** (0.291; p=0.002) | -0.095 (0.095; p=0.318) | 0.167** (0.075; p=0.026) | 0.262** (0.128; p=0.040) | 3,013 / 3,062 |
| ly | all | -0.855*** (0.257; p<0.001) | 0.439 (0.285; p=0.123) | 1.294*** (0.378; p<0.001) | -0.180* (0.108; p=0.096) | 0.200 (0.130; p=0.123) | 0.380** (0.176; p=0.030) | 3,013 / 3,062 |
| ly | without SE fathers | -0.792*** (0.263; p=0.003) | 0.323 (0.295; p=0.275) | 1.114*** (0.399; p=0.005) | -0.212** (0.099; p=0.032) | 0.210 (0.147; p=0.154) | 0.422** (0.178; p=0.018) | 2,561 / 2,575 |
| ly | all, father SE held fixed | -0.811*** (0.254; p=0.001) | 0.443 (0.286; p=0.122) | 1.255*** (0.379; p<0.001) | -0.187* (0.107; p=0.082) | 0.200 (0.130; p=0.123) | 0.387** (0.175; p=0.027) | 3,013 / 3,062 |

## 4. The son's self-employment

### 4a. Self-employment by the father's (son-years with a valid code)

| father | son self-employed 25-34 | 35-44 | 45-55 | sons |
|---|---|---|---|---|
| self-employed | 0.184 | 0.252 | 0.316 | 553 |
| employee | 0.092 | 0.133 | 0.145 | 2,726 |

### 4b. The layoff profile of the son's self-employment

| sample | 25-29 | 45-49 | change | within son x age | sons |
|---|---|---|---|---|---|
| (a) all sons | 0.097** (0.049; p=0.048) | 0.271** (0.121; p=0.026) | 0.174 (0.116; p=0.132) | 0.045 (0.042; p=0.292) | 4,648 |
| (b) without SE fathers | 0.118** (0.050; p=0.018) | 0.314** (0.136; p=0.021) | 0.196 (0.132; p=0.138) | 0.044 (0.048; p=0.360) | 4,095 |
| (c) without fathers ever SE | 0.111** (0.055; p=0.042) | 0.231 (0.158; p=0.143) | 0.120 (0.146; p=0.413) | 0.040 (0.056; p=0.475) | 3,833 |
| (d) all, father SE (x age) held fixed | 0.104** (0.050; p=0.038) | 0.288** (0.125; p=0.021) | 0.185 (0.117; p=0.114) | 0.048 (0.042; p=0.257) | 4,648 |

### 4c. Where the cost sits, without sons of self-employed fathers (as 118 section 3)

| outcome | spec | layoff share x age | interaction | son-years / sons |
|---|---|---|---|---|
| ly | employee years only | -0.174* (0.096; p=0.069) | | 30,193 / 3,918 |
| ly | self-employed years only | -1.024*** (0.293; p<0.001) | | 3,357 / 1,117 |
| ly | all years, layoff x age x self-employed | -0.215** (0.091; p=0.018) | -0.331* (0.179; p=0.065) | 33,550 / 4,028 |
| lw | employee years only | -0.061 (0.072; p=0.397) | | 30,193 / 3,918 |
| lw | self-employed years only | -0.733** (0.304; p=0.016) | | 3,357 / 1,117 |
| lw | all years, layoff x age x self-employed | -0.057 (0.071; p=0.420) | -0.276* (0.143; p=0.055) | 33,550 / 4,028 |

