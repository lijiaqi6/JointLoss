# Is the delayed cost of a father's teen layoff selection? (Fable A2, A3, A6)

Built by `91.LayoffSelection.py` (2026-10-20); design in its docstring. PSID sons 25-55, son-years with a valid wage; estimate (s.e.; p), *** p<0.01, ** p<0.05, * p<0.1. Band coefficients: at equal ln parental income and all of 75's components, single-age dummies, weighted, s.e. from 200 cluster-bootstrap draws of 1968 families (common to all rows). Within-son: son FE, single-age dummies, lyp, every component, structure flag and 5-year cohort x (age-40)/10; s.e. clustered by 1968 family. **Descriptive.**

## A6a. Treated sons: father-present sons with a teen layoff year (son-years with a valid wage)

| sample | 25-29 | 30-34 | 35-39 | 40-44 | 45-49 | 50-55 | 25-55 |
|---|---|---|---|---|---|---|---|
| pooled: treated / father-present sons | 383 / 2,999 | 324 / 2,761 | 257 / 2,218 | 196 / 1,674 | 135 / 1,165 | 85 / 851 | 430 / 3,386 |
| White: treated / father-present sons | 265 / 2,168 | 233 / 1,988 | 182 / 1,625 | 141 / 1,256 | 98 / 883 | 55 / 640 | 291 / 2,370 |
| Black: treated / father-present sons | 118 / 831 | 91 / 773 | 75 / 593 | 55 / 418 | 37 / 282 | 30 / 211 | 139 / 1,016 |

Teen layoff years: 797; median fall in ln family income in a layoff year against the son's layoff-free teen waves -0.084; hours unemployed measured in 72% of layoff years, UI receipt in 28% (received in 38%), employment status (1983+) in 58%.

## A6b. Layoff change vs closure change (45-49 minus 25-29), ln earnings, common draws

| sample | layoff change | closure change | layoff - closure |
|---|---|---|---|
| pooled | -0.914*** (0.244; p<0.001) | 0.000 (0.277; p=0.999) | -0.914*** (0.326; p=0.005) |
| White | -0.975*** (0.258; p<0.001) | -0.014 (0.294; p=0.963) | -0.962*** (0.338; p=0.004) |

## A6c. Within the same son: equality of the three timing windows (ln earnings)

Sons with all three windows measured (the father is a head at the son's 6-12 and 20-26). Coefficients per unit share x (age-40)/10.

| sample | layoff 6-12 x age | layoff 13-19 x age | layoff 20-26 x age | 13-19 minus 6-12 | 13-19 minus 20-26 | all three equal (chi2, p) | N son-years / sons |
|---|---|---|---|---|---|---|---|
| pooled | -0.081 (0.109; p=0.459) | -0.322*** (0.124; p=0.010) | 0.037 (0.102; p=0.712) | -0.241 (0.180; p=0.181) | -0.359** (0.177; p=0.043) | 4.12 (p=0.128) | 19,129 / 2,171 |
| White | -0.097 (0.117; p=0.406) | -0.338** (0.135; p=0.012) | 0.061 (0.105; p=0.563) | -0.241 (0.196; p=0.218) | -0.399** (0.188; p=0.034) | 4.52 (p=0.104) | 14,869 / 1,603 |
| Black | -0.021 (0.226; p=0.926) | -0.068 (0.186; p=0.716) | 0.073 (0.226; p=0.746) | -0.047 (0.335; p=0.889) | -0.141 (0.341; p=0.680) | 0.18 (p=0.915) | 4,260 / 568 |

## A6d. Leave one five-year birth cohort out (pooled, ln earnings)

| cohort left out | sons left | band change 45-49 - 25-29 (layoff) | within-son layoff x age |
|---|---|---|---|
| none | 4,644 | -0.914*** (0.244; p<0.001) | -0.236** (0.103; p=0.022) |
| 1950-1954 | 4,102 | -0.854*** (0.282; p=0.002) | -0.258** (0.121; p=0.032) |
| 1955-1959 | 3,936 | -0.956*** (0.263; p<0.001) | -0.257** (0.108; p=0.017) |
| 1960-1964 | 4,054 | -0.979*** (0.273; p<0.001) | -0.210* (0.116; p=0.070) |
| 1965-1969 | 4,198 | -0.821*** (0.273; p=0.003) | -0.250*** (0.095; p=0.009) |
| 1970-1974 | 4,281 | -0.849*** (0.269; p=0.002) | -0.211* (0.115; p=0.067) |
| 1975-1979 | 4,190 | -0.994*** (0.254; p<0.001) | -0.247** (0.108; p=0.022) |
| 1980-1984 | 4,114 | -0.884*** (0.242; p<0.001) | -0.214** (0.102; p=0.037) |
| 1985-1989 | 4,182 | -0.902*** (0.244; p<0.001) | -0.233** (0.104; p=0.024) |
| 1990-1994 | 4,257 | -0.880*** (0.240; p<0.001) | -0.236** (0.103; p=0.022) |
| 1995-1999 | 4,482 | -0.940*** (0.243; p<0.001) | -0.236** (0.103; p=0.022) |

## A2. Timing as the control group: sons whose father was laid off at some time (6-12, 13-19 or 20-26)

Groups: T = a layoff at the son's 13-19; E = at 6-12, not 13-19; L = only at 20-26 (reference). Son FE; single-age dummies; lyp and every component except the layoff share x (age-40)/10.

| sample | sons T / E / L | T x age | E x age | T - E | all equal (chi2, p) | N son-years |
|---|---|---|---|---|---|---|
| pooled | 256 / 164 / 127 | -0.157** (0.068; p=0.021) | -0.110* (0.063; p=0.081) | -0.047 (0.062; p=0.446) | 5.61 (p=0.061) | 4,536 |
| White | 195 / 113 / 98 | -0.167** (0.074; p=0.023) | -0.122* (0.070; p=0.083) | -0.045 (0.067; p=0.497) | 5.46 (p=0.065) | 3,545 |
| Black | 61 / 51 / 29 | 0.062 (0.113; p=0.583) | 0.072 (0.133; p=0.587) | -0.010 (0.143; p=0.942) | 0.45 (p=0.799) | 991 |

Band profile (pooled): T x band and E x band relative to 25-29 (son FE absorbs the level).

| group | 30-34 | 35-39 | 40-44 | 45-49 | 50-55 |
|---|---|---|---|---|---|
| T | -0.065 (0.078; p=0.405) | -0.136 (0.106; p=0.197) | -0.163 (0.132; p=0.216) | -0.329** (0.143; p=0.022) | -0.402** (0.191; p=0.036) |
| E | -0.051 (0.070; p=0.468) | -0.234** (0.098; p=0.017) | -0.208* (0.122; p=0.088) | -0.199 (0.129; p=0.124) | -0.228 (0.183; p=0.212) |

T and E profiles equal: chi2(5) = 5.09, p = 0.405.

## A3. What the layoff is vs what it does: the teen layoff share split into parts

Each row replaces the layoff share by its parts (they add up to it). Band columns: coefficient at equal lyp and all other components (bootstrap s.e.); within-son: part x (age-40)/10, son FE. Last column: equality of the first two parts in the within-son design.

| split | part | 25-29 | 45-49 | change | within-son x age | first two equal (within-son) |
|---|---|---|---|---|---|---|
| income loss | lay_loss_big | 0.134 (0.158; p=0.396) | -0.453 (0.364; p=0.214) | -0.587 (0.371; p=0.113) | -0.096 (0.132; p=0.466) | chi2 3.09, p=0.079 |
|  | lay_loss_small | 0.249 (0.164; p=0.129) | -1.160** (0.455; p=0.011) | -1.409*** (0.404; p<0.001) | -0.473*** (0.144; p=0.001) |  |
|  | lay_loss_na | 0.017 (0.184; p=0.925) | -0.647 (0.776; p=0.404) | -0.665 (0.672; p=0.323) | -0.121 (0.298; p=0.685) |  |
| unemployment (hours >= 500) | lay_hu_long | 0.382 (0.269; p=0.155) | -0.110 (0.644; p=0.865) | -0.492 (0.576; p=0.393) | 0.225 (0.265; p=0.397) | chi2 3.44, p=0.064 |
|  | lay_hu_short | 0.021 (0.126; p=0.866) | -1.057*** (0.327; p=0.001) | -1.079*** (0.300; p<0.001) | -0.338*** (0.119; p=0.005) |  |
|  | lay_hu_na | 0.257 (0.209; p=0.220) | 0.411 (0.823; p=0.617) | 0.154 (0.831; p=0.853) | -0.519* (0.285; p=0.068) |  |
| UI receipt | lay_ui | 0.068 (0.246; p=0.781) | -1.002 (2.186; p=0.647) | -1.070 (2.224; p=0.630) | -1.014** (0.484; p=0.036) | chi2 2.79, p=0.095 |
|  | lay_noui | 0.417 (0.306; p=0.172) | 1.098 (1.399; p=0.433) | 0.680 (1.400; p=0.627) | -0.211 (0.255; p=0.407) |  |
|  | lay_ui_na | 0.108 (0.103; p=0.293) | -0.827*** (0.265; p=0.002) | -0.936*** (0.246; p<0.001) | -0.218** (0.107; p=0.042) |  |
| repeat | lay_one | 0.154 (0.272; p=0.570) | -1.642* (0.918; p=0.074) | -1.796* (0.923; p=0.052) | 0.295 (0.378; p=0.435) | chi2 2.12, p=0.145 |
|  | lay_multi | 0.145 (0.097; p=0.136) | -0.743*** (0.265; p=0.005) | -0.888*** (0.246; p<0.001) | -0.268** (0.106; p=0.012) |  |
| temporary layoff (1983+) | lay_temp | 0.484 (0.421; p=0.250) | -0.426 (1.810; p=0.814) | -0.910 (1.694; p=0.591) | -0.715 (0.512; p=0.162) | chi2 0.47, p=0.493 |
|  | lay_perm | 0.344** (0.146; p=0.018) | -0.612* (0.371; p=0.099) | -0.956*** (0.322; p=0.003) | -0.347*** (0.123; p=0.005) |  |
|  | lay_temp_na | -0.173 (0.153; p=0.258) | -0.997*** (0.356; p=0.005) | -0.824** (0.346; p=0.017) | -0.094 (0.129; p=0.468) |  |

### A3 (vi). Parental income at the son's 20-26 as a control

| spec | layoff 25-29 | layoff 45-49 | change | within-son layoff x age |
|---|---|---|---|---|
| as in 88 | 0.146 (0.101; p=0.148) | -0.768*** (0.263; p=0.004) | -0.914*** (0.244; p<0.001) | -0.236** (0.103; p=0.022) |
| + ln parental income at 20-26 (and its flag) | 0.143 (0.104; p=0.168) | -0.754*** (0.268; p=0.005) | -0.897*** (0.246; p<0.001) | -0.232** (0.102; p=0.023) |

