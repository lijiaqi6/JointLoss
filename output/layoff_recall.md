# Recall or permanent separation? And the father's job held fixed (committee memo Z1)

Built by `120.LayoffRecall.py` (2026-10-24); design in its docstring. Per unit teen layoff share; band s.e. from 200 cluster-bootstrap draws of 1968 families (common to all rows), within-son s.e. clustered by 1968 family. *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**

## 1. The father's teen layoff years by what followed

| | recall (back with a pre-layoff employer) | new employer | unknown | all |
|---|---|---|---|---|
| teen layoff years (son x wave) | 194 | 345 | 258 | 797 |
| father-present sons with such a year | 108 | 197 | 162 | 430 |
| ... observed at 45-49 | 47 | 55 | 46 | 135 |

Validation on the layoff records of 1980-82 with the direct item (all male heads):

| | rule: recall | rule: new | rule: unknown |
|---|---|---|---|
| direct: not | 48 | 354 | 175 |
| direct: same employer | 41 | 35 | 7 |

All male-head layoff records: new 4,253, unknown 3,613, recall 1,397.

## 2. Recall and new-employer layoffs (ln earnings, ln wage)

| outcome | part | 25-29 | 45-49 | change | within son x age |
|---|---|---|---|---|---|
| ly | recall | 0.077 (0.166; p=0.645) | -1.028** (0.460; p=0.026) | -1.104** (0.441; p=0.012) | -0.251* (0.129; p=0.052) |
| ly | new | 0.365** (0.173; p=0.035) | -0.467 (0.436; p=0.283) | -0.832** (0.421; p=0.048) | -0.153 (0.183; p=0.403) |
| ly | unknown | -0.047 (0.135; p=0.728) | -0.926*** (0.356; p=0.009) | -0.878** (0.352; p=0.013) | -0.320** (0.125; p=0.010) |
| ly | recall - new | | | -0.272 (0.612; p=0.656) | -0.097 (0.227; p=0.668) (Wald p=0.668) |
| lw | recall | -0.105 (0.158; p=0.506) | -0.802* (0.421; p=0.057) | -0.697 (0.426; p=0.102) | -0.203* (0.123; p=0.099) |
| lw | new | 0.267** (0.131; p=0.042) | -0.299 (0.327; p=0.361) | -0.566* (0.318; p=0.075) | -0.131 (0.167; p=0.432) |
| lw | unknown | -0.107 (0.113; p=0.345) | -0.676*** (0.231; p=0.003) | -0.570*** (0.213; p=0.008) | -0.031 (0.086; p=0.718) |
| lw | recall - new | | | -0.131 (0.544; p=0.810) | -0.072 (0.214; p=0.737) (Wald p=0.737) |

## 3. The layoff with the father's sector, occupation and union held fixed

| outcome | controls | 25-29 | 45-49 | change | within son x age | sons |
|---|---|---|---|---|---|---|
| ly | none | 0.146 (0.101; p=0.148) | -0.768*** (0.263; p=0.004) | -0.914*** (0.244; p<0.001) | -0.236** (0.103; p=0.022) | 4,644 |
| ly | sector | 0.143 (0.101; p=0.158) | -0.739*** (0.270; p=0.006) | -0.882*** (0.249; p<0.001) | -0.223** (0.100; p=0.025) | 4,644 |
| ly | occupation | 0.146 (0.102; p=0.155) | -0.754*** (0.267; p=0.005) | -0.899*** (0.249; p<0.001) | -0.231** (0.100; p=0.020) | 4,644 |
| ly | union | 0.158 (0.100; p=0.116) | -0.739*** (0.260; p=0.004) | -0.896*** (0.244; p<0.001) | -0.234** (0.103; p=0.024) | 4,644 |
| ly | sector + occupation + union | 0.165 (0.101; p=0.102) | -0.709*** (0.273; p=0.009) | -0.874*** (0.257; p<0.001) | -0.226** (0.099; p=0.023) | 4,644 |
| lw | none | 0.046 (0.085; p=0.586) | -0.557*** (0.210; p=0.008) | -0.603*** (0.190; p=0.001) | -0.109 (0.082; p=0.184) | 4,644 |
| lw | sector | 0.039 (0.085; p=0.651) | -0.541** (0.210; p=0.010) | -0.579*** (0.190; p=0.002) | -0.092 (0.078; p=0.237) | 4,644 |
| lw | occupation | 0.052 (0.084; p=0.538) | -0.542*** (0.208; p=0.009) | -0.593*** (0.189; p=0.002) | -0.104 (0.081; p=0.195) | 4,644 |
| lw | union | 0.059 (0.085; p=0.489) | -0.531*** (0.204; p=0.009) | -0.589*** (0.184; p=0.001) | -0.104 (0.081; p=0.200) | 4,644 |
| lw | sector + occupation + union | 0.063 (0.083; p=0.448) | -0.502** (0.210; p=0.017) | -0.565*** (0.191; p=0.003) | -0.092 (0.078; p=0.238) | 4,644 |

## 4. The within-son slope by the father's sector (one regression, ln earnings)

| father's sector | layoff share x age | treated sons | treated at 45-49 | father-present sons |
|---|---|---|---|---|
| ly: durable manufacturing | -0.179 (0.131; p=0.170) | 91 | 34 | 600 |
| ly: construction, mining | -0.282* (0.150; p=0.061) | 75 | 27 | 365 |
| ly: nondurable mfg, transport, utilities, communications | -0.228 (0.239; p=0.338) | 71 | 23 | 671 |
| ly: trade and services | -0.143 (0.184; p=0.439) | 162 | 43 | 1,185 |
| ly: public administration | -0.226 (0.200; p=0.258) | 13 | 5 | 273 |
| ly: sector unknown | -0.486 (0.452; p=0.283) | 18 | 3 | 292 |
| ly: equal across the five sectors | Wald p=0.980 | | | |
| lw: durable manufacturing | -0.102 (0.118; p=0.384) | 91 | 34 | 600 |
| lw: construction, mining | -0.212 (0.131; p=0.106) | 75 | 27 | 365 |
| lw: nondurable mfg, transport, utilities, communications | -0.022 (0.150; p=0.883) | 71 | 23 | 671 |
| lw: trade and services | -0.069 (0.143; p=0.631) | 162 | 43 | 1,185 |
| lw: public administration | -0.356* (0.206; p=0.084) | 13 | 5 | 273 |
| lw: sector unknown | 0.056 (0.342; p=0.870) | 18 | 3 | 292 |
| lw: equal across the five sectors | Wald p=0.660 | | | |

