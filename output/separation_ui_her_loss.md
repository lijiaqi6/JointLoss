# Separation hazard: UI generosity (M2b) and her displacement (M3), PSID

Built by `64.SeparationUIAndHerLoss.py` (2026-10-19); design in its docstring. 19's stacked event study (person x stack and calendar year x stack FE; reference e = -2; clean controls not displaced to ev+6; baseline with a child 0-17 and positive own hours). Unweighted PSID SRC + SEO, Black and White (head's race). S.e. clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1; every cell: coefficient*** (s.e.; p). Main sample = Paper A target sample (IGE/60): events 1984-2021, outcome years <= 2021.

**Caveat.** The marriage outcome is 1 by construction at baseline, so the pre-period coefficients are mechanical (no placebo test for this outcome); identification rests on the post-period against clean controls with person fixed effects.

## 1. M2b: his displacement x state UI generosity

State found for 0.972 of father x stack units and UI parameters for 0.828 (all events 1968-2022; 12b starts in 1976). Distribution over units with UI data (target sample events): cap_rel mean 0.465 / sd 0.096, dur mean 25.650 / sd 2.202, lmaxben mean 8.901 / sd 0.288, repl mean 0.343 / sd 0.055.

### 1a. Interaction model, Target sample (events 1984-2021)

Each cell of a row is one regression (outcome 'still with baseline wife'): coefficient on displaced x event time x z (z = UI measure standardised over the sample's units, 1 sd), mean of e = +1..+3; below it the mean of +4..+6 and the (mechanical) pre-period terms. Event-time x z for all families included. A positive coefficient = more generous UI, smaller fall in the probability of still being with the baseline wife.

| | All | Black | White |
|---|---:|---:|---:|
| Displaced x z(Max weekly benefit / state avg weekly wage), mean +1..+3 | 0.009 (0.011; p=0.382)<br>+4..+6: 0.005 (0.014; p=0.689)<br>pre e=-3: 0.005 (0.012; p=0.694); e=-1: 0.009 (0.010; p=0.356) | 0.006 (0.020; p=0.778)<br>+4..+6: 0.023 (0.026; p=0.373)<br>pre e=-3: 0.033 (0.028; p=0.240); e=-1: 0.026 (0.021; p=0.228) | 0.007 (0.013; p=0.593)<br>+4..+6: -0.011 (0.016; p=0.493)<br>pre e=-3: -0.012 (0.012; p=0.326); e=-1: 0.002 (0.010; p=0.843) |
| Displaced x z(Max weeks of regular benefits), mean +1..+3 | -0.005 (0.021; p=0.825)<br>+4..+6: -0.006 (0.017; p=0.730)<br>pre e=-3: -0.008 (0.033; p=0.809); e=-1: -0.010 (0.027; p=0.717) | -0.018 (0.027; p=0.514)<br>+4..+6: -0.011 (0.029; p=0.719)<br>pre e=-3: -0.003 (0.042; p=0.936); e=-1: -0.014 (0.020; p=0.487) | 0.004 (0.023; p=0.859)<br>+4..+6: -0.012 (0.016; p=0.443)<br>pre e=-3: -0.008 (0.024; p=0.729); e=-1: 0.002 (0.026; p=0.926) |
| Displaced x z(Log max potential benefit (max WBA x weeks, 2000 $)), mean +1..+3 | 0.006 (0.012; p=0.620)<br>+4..+6: -0.009 (0.015; p=0.546)<br>pre e=-3: 0.007 (0.015; p=0.654); e=-1: 0.006 (0.010; p=0.589) | 0.020 (0.023; p=0.378)<br>+4..+6: 0.025 (0.029; p=0.397)<br>pre e=-3: 0.036 (0.036; p=0.318); e=-1: 0.024 (0.021; p=0.241) | -0.002 (0.014; p=0.867)<br>+4..+6: -0.031* (0.017; p=0.074)<br>pre e=-3: -0.010 (0.013; p=0.423); e=-1: -0.001 (0.011; p=0.933) |
| Displaced x z(Avg weekly benefit / avg weekly wage), mean +1..+3 | 0.005 (0.011; p=0.640)<br>+4..+6: 0.005 (0.014; p=0.686)<br>pre e=-3: -0.005 (0.012; p=0.694); e=-1: 0.010 (0.010; p=0.325) | -0.012 (0.020; p=0.568)<br>+4..+6: 0.004 (0.027; p=0.879)<br>pre e=-3: 0.026 (0.026; p=0.320); e=-1: 0.019 (0.018; p=0.292) | 0.007 (0.013; p=0.589)<br>+4..+6: -0.006 (0.016; p=0.699)<br>pre e=-3: -0.022* (0.012; p=0.071); e=-1: 0.008 (0.012; p=0.460) |
| Displaced (at mean generosity), mean +1..+3 | -0.036*** (0.011; p=0.002) | -0.039* (0.023; p=0.090) | -0.028** (0.012; p=0.025) |
| N person-years / displaced fathers / control stacks / clusters | 223,731 / 1,366 / 41,176 / 1,929 | 57,284 / 526 / 10,883 / 679 | 166,447 / 840 / 30,293 / 1,348 |

### 1b. Interaction model, Events 1977-2021

Each cell of a row is one regression (outcome 'still with baseline wife'): coefficient on displaced x event time x z (z = UI measure standardised over the sample's units, 1 sd), mean of e = +1..+3; below it the mean of +4..+6 and the (mechanical) pre-period terms. Event-time x z for all families included. A positive coefficient = more generous UI, smaller fall in the probability of still being with the baseline wife.

| | All | Black | White |
|---|---:|---:|---:|
| Displaced x z(Log max potential benefit (max WBA x weeks, 2000 $)), mean +1..+3 | 0.005 (0.010; p=0.637)<br>+4..+6: -0.001 (0.012; p=0.905)<br>pre e=-3: 0.011 (0.011; p=0.327); e=-1: 0.004 (0.008; p=0.567) | 0.011 (0.018; p=0.568)<br>+4..+6: 0.007 (0.023; p=0.748)<br>pre e=-3: 0.043* (0.022; p=0.052); e=-1: 0.020 (0.014; p=0.162) | 0.003 (0.012; p=0.799)<br>+4..+6: -0.008 (0.015; p=0.600)<br>pre e=-3: -0.010 (0.010; p=0.348); e=-1: -0.001 (0.009; p=0.942) |
| Displaced (at mean generosity), mean +1..+3 | -0.030*** (0.010; p=0.002) | -0.033* (0.019; p=0.074) | -0.022** (0.011; p=0.046) |
| N person-years / displaced fathers / control stacks / clusters | 296,058 / 1,754 / 49,224 / 2,159 | 77,060 / 688 / 13,271 / 781 | 218,998 / 1,066 / 35,953 / 1,477 |

### 1c. Median split by the maximum potential benefit (target sample)

Separate event studies for displaced fathers (and control stacks) in state-years at or below / above the median log real maximum potential benefit among displaced fathers of the race; the difference treats the two regressions as independent.

| | All | Black | White |
|---|---:|---:|---:|
| Mean +1..+3, below median generosity | -0.036** (0.016; p=0.025) | -0.064** (0.032; p=0.050) | -0.024 (0.017; p=0.149) |
| Mean +1..+3, above median generosity | -0.034** (0.016; p=0.031) | -0.015 (0.033; p=0.647) | -0.029 (0.018; p=0.106) |
| Mean +1..+3: above - below | 0.002 (0.023; p=0.926) | 0.049 (0.046; p=0.290) | -0.004 (0.024; p=0.857) |
| Mean +4..+6, below median generosity | -0.041** (0.020; p=0.038) | -0.083** (0.040; p=0.039) | -0.011 (0.021; p=0.588) |
| Mean +4..+6, above median generosity | -0.062*** (0.020; p=0.002) | -0.056 (0.037; p=0.127) | -0.056** (0.023; p=0.016) |
| Mean +4..+6: above - below | -0.021 (0.028; p=0.441) | 0.027 (0.054; p=0.622) | -0.045 (0.031; p=0.151) |
| Displaced fathers below / above median | 684 / 682 | 263 / 263 | 422 / 418 |
| Median real max potential benefit (2000 $) | 7,525 | 7,109 | 7,734 |

## 2. M3: her displacement as the event

Her job-end reports (closure / layoff / fired): 4,159 wife-years from the wife's items (1984-2023 waves) and 5,611 report rows from female heads' own items; 4,978 women with a first displacement in 1983+ (1,914 first closure). Baseline: wife of a male head, a child 0-17, positive own hours. Race = the head's race at baseline.

| | All | Black | White |
|---|---:|---:|---:|
| Still with baseline husband: e=-3 | -0.022** (0.010; p=0.035) | -0.007 (0.019; p=0.709) | -0.026** (0.012; p=0.034) |
| Still with baseline husband: e=-1 | 0.011 (0.009; p=0.250) | 0.010 (0.018; p=0.597) | 0.010 (0.010; p=0.307) |
| Still with baseline husband: e=+0 | -0.019* (0.010; p=0.069) | -0.024 (0.021; p=0.252) | -0.013 (0.011; p=0.231) |
| Still with baseline husband: e=+1 | -0.014 (0.012; p=0.214) | -0.018 (0.023; p=0.424) | -0.008 (0.013; p=0.519) |
| Still with baseline husband: e=+2 | -0.057*** (0.014; p=<0.001) | -0.069** (0.028; p=0.014) | -0.046*** (0.016; p=0.003) |
| Still with baseline husband: e=+3 | -0.066*** (0.016; p=<0.001) | -0.055** (0.028; p=0.045) | -0.064*** (0.019; p=<0.001) |
| Still with baseline husband: e=+4 | -0.079*** (0.017; p=<0.001) | -0.076** (0.031; p=0.014) | -0.072*** (0.020; p=<0.001) |
| Still with baseline husband: e=+5 | -0.090*** (0.019; p=<0.001) | -0.090*** (0.034; p=0.008) | -0.079*** (0.022; p=<0.001) |
| Still with baseline husband: e=+6 | -0.100*** (0.019; p=<0.001) | -0.083** (0.035; p=0.019) | -0.098*** (0.023; p=<0.001) |
| Still with baseline husband: mean +1..+3 | -0.046*** (0.012; p=<0.001) | -0.048** (0.023; p=0.037) | -0.040*** (0.014; p=0.005) |
| Still with baseline husband: mean +4..+6 | -0.090*** (0.016; p=<0.001) | -0.083*** (0.030; p=0.006) | -0.083*** (0.020; p=<0.001) |
| Still with baseline husband: N person-years / displaced wives / control stacks / clusters; treated mean e=-2,-1 | 236,761 / 1,205 / 41,623 / 2,037; 0.986 | 64,722 / 442 / 11,779 / 721; 0.982 | 172,039 / 763 / 29,844 / 1,397; 0.988 |
| Her annual hours: e=+0 | -135*** (34; p=<0.001) | -225*** (60; p=<0.001) | -89** (41; p=0.028) |
| Her annual hours: mean +1..+3 | -127*** (38; p=<0.001) | -211*** (60; p=<0.001) | -85* (48; p=0.074) |
| Her annual hours: mean +4..+6 | -36 (41; p=0.379) | 14 (71; p=0.838) | -58 (50; p=0.246) |
| Her annual hours: N person-years / displaced wives / control stacks / clusters; treated mean e=-2,-1 | 236,756 / 1,205 / 41,623 / 2,037; 1436.387 | 64,722 / 442 / 11,779 / 721; 1511.266 | 172,034 / 763 / 29,844 / 1,397; 1395.182 |
| Husband's annual hours (while with her): e=+0 | 30 (32; p=0.354) | 48 (59; p=0.411) | 18 (39; p=0.648) |
| Husband's annual hours (while with her): mean +1..+3 | 61* (32; p=0.061) | 100* (57; p=0.082) | 43 (39; p=0.276) |
| Husband's annual hours (while with her): mean +4..+6 | 65* (37; p=0.076) | 93 (63; p=0.139) | 55 (45; p=0.221) |
| Husband's annual hours (while with her): N person-years / displaced wives / control stacks / clusters; treated mean e=-2,-1 | 221,919 / 1,205 / 41,623 / 2,037; 2039.148 | 58,721 / 442 / 11,779 / 721; 1883.922 | 163,198 / 763 / 29,844 / 1,397; 2123.998 |
| Closures only, still with baseline husband: mean +1..+3 | -0.027 (0.021; p=0.194) | -0.037 (0.046; p=0.421) | -0.024 (0.023; p=0.305) |
| Closures only, still with baseline husband: mean +4..+6 | -0.044 (0.027; p=0.107) | -0.021 (0.055; p=0.703) | -0.052* (0.031; p=0.099) |
| Closures only: displaced wives | 376 | 105 | 271 |
| For comparison, HIS displacement, still with baseline wife: mean +1..+3 | -0.036*** (0.011; p=0.002) | -0.040* (0.023; p=0.084) | -0.027** (0.012; p=0.028) |
| For comparison, HIS displacement, still with baseline wife: mean +4..+6 | -0.051*** (0.014; p=<0.001) | -0.069** (0.027; p=0.010) | -0.033** (0.016; p=0.035) |

## 3. Still with baseline wife by event year after his displacement (target sample; for WP3.2)

Same numbers in `bw_present_by_year.csv`, which also carries IGE/19's full-sample path (events 1968-2022) copied from `father_displacement.csv`.

| | All | Black | White |
|---|---:|---:|---:|
| e=-3 | -0.029*** (0.011; p=0.007) | -0.028 (0.023; p=0.215) | -0.024** (0.012; p=0.036) |
| e=-1 | 0.015 (0.010; p=0.126) | 0.047** (0.019; p=0.014) | -0.002 (0.011; p=0.871) |
| e=+0 | -0.023** (0.010; p=0.014) | -0.019 (0.018; p=0.289) | -0.021* (0.011; p=0.050) |
| e=+1 | -0.033*** (0.012; p=0.005) | -0.030 (0.024; p=0.213) | -0.029** (0.012; p=0.017) |
| e=+2 | -0.036*** (0.012; p=0.002) | -0.035 (0.023; p=0.134) | -0.031** (0.014; p=0.024) |
| e=+3 | -0.038*** (0.014; p=0.005) | -0.056* (0.029; p=0.057) | -0.020 (0.014; p=0.140) |
| e=+4 | -0.049*** (0.014; p=<0.001) | -0.060** (0.026; p=0.023) | -0.035** (0.016; p=0.031) |
| e=+5 | -0.054*** (0.016; p=<0.001) | -0.081** (0.033; p=0.014) | -0.030* (0.017; p=0.077) |
| e=+6 | -0.051*** (0.016; p=0.002) | -0.067** (0.031; p=0.029) | -0.033* (0.019; p=0.077) |
| mean +1..+3 | -0.036*** (0.011; p=0.002) | -0.040* (0.023; p=0.084) | -0.027** (0.012; p=0.028) |
| mean +4..+6 | -0.051*** (0.014; p=<0.001) | -0.069** (0.027; p=0.010) | -0.033** (0.016; p=0.035) |
