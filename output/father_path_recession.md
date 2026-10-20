# The father's path after the layoff, and layoffs in bad times (Fable round 2, Objection 2)

Built by `104.FatherPathRecession.py` (2026-10-20); design in its docstring. *** p<0.01, ** p<0.05, * p<0.1.

## (i) The father's path at the son's 20-24 (one row per father-present son)

Each column: the father's outcome at the son's 20-24 on the teen layoff share (row 1) or on its parts (rows below, one regression per split), with ln parental income, the father's teen-window ln wage and ln hours and 5-year cohort dummies; PSID weights; clustered by 1968 family. Per unit share.

| regressor | ln earnings | ln earnings minus his teen mean | employed | unemployed | laid off again |
|---|---|---|---|---|---|
| teen layoff share | -0.193* (0.117; p=0.098) | -0.193* (0.117; p=0.098) | 0.020 (0.052; p=0.692) | 0.289*** (0.061; p<0.001) | 0.132*** (0.035; p<0.001) |
| income loss: lay_loss_small | -0.172 (0.157; p=0.272) | -0.172 (0.157; p=0.272) | 0.036 (0.087; p=0.676) | 0.408*** (0.107; p<0.001) | 0.220*** (0.059; p<0.001) |
| income loss: lay_loss_big | -0.203 (0.203; p=0.317) | -0.203 (0.203; p=0.317) | -0.011 (0.078; p=0.891) | 0.212*** (0.078; p=0.007) | 0.057 (0.043; p=0.178) |
| unemployment: lay_hu_short | -0.191 (0.140; p=0.171) | -0.191 (0.140; p=0.171) | 0.074 (0.082; p=0.371) | 0.277** (0.111; p=0.013) | 0.163*** (0.051; p=0.001) |
| unemployment: lay_hu_long | 0.071 (0.355; p=0.841) | 0.071 (0.355; p=0.841) | 0.140 (0.159; p=0.381) | 0.490*** (0.182; p=0.007) | 0.203* (0.107; p=0.059) |
| repeat: lay_one | -0.958** (0.428; p=0.025) | -0.958** (0.428; p=0.025) | -0.240 (0.174; p=0.168) | 0.513*** (0.138; p<0.001) | 0.134** (0.064; p=0.036) |
| repeat: lay_multi | -0.063 (0.104; p=0.548) | -0.063 (0.104; p=0.548) | 0.071 (0.051; p=0.158) | 0.246*** (0.067; p<0.001) | 0.132*** (0.041; p=0.001) |
| bad times: lay_bad | -0.240 (0.149; p=0.107) | -0.240 (0.149; p=0.107) | 0.045 (0.078; p=0.562) | 0.212*** (0.081; p=0.009) | 0.170*** (0.052; p=0.001) |
| bad times: lay_good | -0.194 (0.252; p=0.441) | -0.194 (0.252; p=0.441) | -0.040 (0.098; p=0.680) | 0.450*** (0.097; p<0.001) | 0.084 (0.052; p=0.103) |
| N fathers (ln earnings / employed) | 2,778 | | 2,995 | | |

## (ii) Layoffs in bad times vs other layoffs

Teen layoff years 797; classed in 98%; bad times (sector decline or state unemployment >= 1 point above its mean) 53% of classed layoff years (sector decline alone 44%), against 44% of all classed window years.

| split | part | 25-29 | 45-49 | change | within son x age | first two equal (within son) |
|---|---|---|---|---|---|---|
| bad times (sector decline or high state unemployment) | lay_bad | 0.122 (0.143; p=0.395) | -0.553 (0.369; p=0.134) | -0.675** (0.320; p=0.035) | -0.166 (0.149; p=0.265) | chi2 1.25, p=0.263 |
|  | lay_good | 0.248 (0.171; p=0.146) | -1.152*** (0.373; p=0.002) | -1.400*** (0.378; p<0.001) | -0.408*** (0.139; p=0.003) |  |
|  | lay_bad_na | -0.225 (0.241; p=0.350) | -1.981 (1.844; p=0.283) | -1.756 (1.829; p=0.337) | 0.038 (0.280; p=0.892) |  |
| sector decline only | lay_secdecl | 0.030 (0.140; p=0.828) | -0.634 (0.424; p=0.135) | -0.664* (0.377; p=0.078) | -0.183 (0.169; p=0.278) | chi2 0.19, p=0.662 |
|  | lay_secnot | 0.274* (0.153; p=0.072) | -0.869*** (0.333; p=0.009) | -1.143*** (0.343; p<0.001) | -0.276** (0.125; p=0.027) |  |
|  | lay_secna | 0.098 (0.278; p=0.724) | -1.809 (1.535; p=0.239) | -1.907 (1.587; p=0.229) | -0.404 (0.448; p=0.367) |  |

