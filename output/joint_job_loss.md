# Joint job loss within couples

Built by `25.JointJobLoss.py` (2026-10-17; definitions and designs in its docstring). Unweighted PSID SRC + SEO, married male heads with a child 0-17 at baseline, Black and White (head's race). Husband's displacement = 19's first closure / layoff; the wife's job ends are her own reason-for-job-end reports (23's items, 1984-2023 waves). S.e. clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1. Every cell: coefficient*** (s.e.; p).

## 0. Data checks

Self-employment items found by label (head / wife, current main job; 1 someone else, 2 both, 3 self only), used only for the exclusion check in section 3:

| Wave | Head item | Wife item |
|---|---|---|
| 1976 | V4461 'WRK SOMEONEELSE/SELF  D5' | V4844 'WRK FOR SELF OR?(E)-WFD5' |
| 1977 | V5376 'WORK FOR SELF/OTR?(E) D5' |  |
| 1978 | V5875 'D5 WORK FOR SELF/OTR (E)' |  |
| 1979 | V6493 'C2 WORK SELF/OTR (HD-E)' | V6592 'F3 WRK SELF/OTR (WF-E)' |
| 1980 | V7096 'C2 WORK SELF/OTR (HD-E)' | V7194 'F3 WRK SELF/OTR (WF-E)' |
| 1981 | V7707 'C2 WORK SELF/OTR?(HD-E)' | V7880 'F3 WORK FOR SELF?(WF-E)' |
| 1982 | V8375 'C2 WORK SELF/OTR?(HD-E)' | V8539 'F3 WORK FOR SELF?(WF-E)' |
| 1983 | V9006 'C2 WORK SELF/OTR?(HD-E)' | V9189 'F3 WORK FOR SELF?(WF-E)' |
| 1984 | V10456 'C4 WORK SELF/OTR?(HD-E)' | V10674 'F5 WORK FOR SELF?(WF-E)' |
| 1985 | V11640 'B4 WORK SELF/OTR? (HD-E)' | V12003 'J4 WORK SELF/OTR? (WF-E)' |
| 1986 | V13049 'B4 WORK SELF/OTR? (HD-E)' | V13228 'D4 WORK SELF/OTR? (WF-E)' |
| 1987 | V14149 'B4 WORK SELF/OTR? (HD-E)' | V14324 'D4 WORK SELF/OTR? (WF-E)' |
| 1988 | V15157 'B4 WORK SELF/OTR? (HD-E)' | V15459 'D4 WORK SELF/OTR? (WF-E)' |
| 1989 | V16658 'B4 WORK SELF/OTR? (HD-E)' | V16977 'D4 WORK SELF/OTR? (WF-E)' |
| 1990 | V18096 'B4 WORK SELF/OTR? (HD-E)' | V18398 'D4 WORK SELF/OTR? (WF-E)' |
| 1991 | V19396 'B4 WORK SELF/OTR? (HD-E)' | V19698 'D4 WORK SELF/OTR? (WF-E)' |
| 1992 | V20696 'B4 WORK SELF/OTR? (HD-E)' | V20998 'D4 WORK SELF/OTR? (WF-E)' |
| 1993 | V22451 'B4 WTR WORK FOR SELF/SOMEONE ELSE (HD-E)' | V22804 'D4 WTR WORK FOR SELF/SOMEONE ELSE (WF-E)' |
| 1994 | ER2074 'B4 WORK SELF/OTR? (HD-E)' | ER2568 'D4 WORK SELF/OTR? (WF-E)' |
| 1995 | ER5073 'B4 WORK SELF/OTR? (HD-E)' | ER5567 'D4 WORK SELF/OTR? (WF-E)' |
| 1996 | ER7169 'B4 WORK SELF/OTR? (HD-E)' | ER7663 'D4 WORK SELF/OTR? (WF-E)' |
| 1997 | ER10086 'B4 WORK SELF/OTR? (HD-E)' | ER10568 'D4 WORK SELF/OTR? (WF-E)' |
| 1999 | ER13210 'B4 WORK SELF/OTR? (HD-E)' | ER13722 'D4 WORK SELF/OTR? (WF-E)' |
| 2001 | ER17221 'B4 WORK SELF/OTR? (HD-E)' | ER17791 'D4 WORK SELF/OTR? (WF-E)' |
| 2003 | ER21147 'BC22 WORK SELF/OTR?--JOB 1' | ER21397 'DE22 WORK SELF/OTR?--JOB 1' |
| 2005 | ER25129 'BC22 WORK SELF/OTR?--JOB 1' | ER25387 'DE22 WORK SELF/OTR?--JOB 1' |
| 2007 | ER36134 'BC22 WORK SELF/OTR?--JOB 1' | ER36392 'DE22 WORK SELF/OTR?--JOB 1' |
| 2009 | ER42169 'BC22 WORK SELF/OTR?--JOB 1' | ER42421 'DE22 WORK SELF/OTR?--JOB 1' |
| 2011 | ER47482 'BC22 WORK SELF/OTR?--JOB 1' | ER47739 'DE22 WORK SELF/OTR?--JOB 1' |
| 2013 | ER53182 'BC22 WORK SELF/OTR?--JOB 1' | ER53445 'DE22 WORK SELF/OTR?--JOB 1' |
| 2015 | ER60197 'BC22 WORK SELF/OTR?--JOB 1' | ER60460 'DE22 WORK SELF/OTR?--JOB 1' |
| 2017 | ER66198 'BC22 WORK SELF/OTR?--JOB 1' | ER66473 'DE22 WORK SELF/OTR?--JOB 1' |
| 2019 | ER72198 'BC22 WORK SELF/OTR?--JOB 1' | ER72475 'DE22 WORK SELF/OTR?--JOB 1' |
| 2021 | ER78203 'BC22 WORK SELF/OTR?--JOB 1' | ER78517 'DE22 WORK SELF/OTR?--JOB 1' |
| 2023 | ER82186 'BC22 WORK SELF/OTR?--JOB 1' | ER82505 'DE22 WORK SELF/OTR?--JOB 1' |

Wife-years with a job end of each kind (de-duplicated): Wife displaced 4,159, Wife's employer closed 1,298, Wife quit 14,526, Wife's job ended (any reason) 20,279.

Check against 23 (its window variable, its sample): husband displaced 0.076*** (0.012; p=<0.001), N 27,134; with this script's coverage rule (all three years covered): 0.075*** (0.012; p=<0.001), N 27,022.

## 1. Event study of the wife's own job loss

Unit x relative-year panel, k = -4..+4, wives employed at baseline, event years 1987-2018. Outcome: the baseline wife reports a job end of the kind in the column dated ev + k (missing if year not covered). Father x stack and calendar year x stack fixed effects; reference years k = -4, -3. 'Mean k = -1..+1' is the average of the three coefficients. Figure: `output/joint_job_loss_es.png`.

| | Wife displaced | Wife's job ended (any reason) | Wife's employer closed | Wife quit |
|---|---|---|---|---|
| **All** | | | | |
| k = -4 (ref.) | 0 | 0 | 0 | 0 |
| k = -3 (ref.) | 0 | 0 | 0 | 0 |
| k = -2 | 0.018* (0.010; p=0.069) | 0.018 (0.018; p=0.297) | 0.003 (0.005; p=0.538) | 0.008 (0.016; p=0.612) |
| k = -1 | 0.021** (0.010; p=0.025) | 0.051*** (0.018; p=0.004) | 0.003 (0.005; p=0.525) | 0.024 (0.016; p=0.119) |
| k = +0 | 0.036*** (0.011; p=<0.001) | 0.061*** (0.019; p=0.002) | 0.015** (0.007; p=0.029) | 0.025 (0.017; p=0.132) |
| k = +1 | 0.024** (0.010; p=0.018) | 0.041** (0.019; p=0.030) | 0.002 (0.005; p=0.633) | 0.011 (0.017; p=0.495) |
| k = +2 | 0.003 (0.009; p=0.754) | -0.014 (0.018; p=0.462) | 0.000 (0.004; p=0.933) | -0.009 (0.016; p=0.583) |
| k = +3 | 0.019* (0.010; p=0.072) | 0.024 (0.021; p=0.239) | 0.002 (0.005; p=0.739) | -0.001 (0.016; p=0.925) |
| k = +4 | 0.012 (0.011; p=0.258) | -0.005 (0.020; p=0.802) | 0.005 (0.006; p=0.421) | -0.016 (0.016; p=0.307) |
| Mean k = -1..+1 | 0.027*** (0.007; p=<0.001) | 0.051*** (0.014; p=<0.001) | 0.007 (0.004; p=0.107) | 0.020* (0.012; p=0.094) |
| Sum k = -1..+1 | 0.081*** (0.022; p=<0.001) | 0.153*** (0.043; p=<0.001) | 0.021 (0.013; p=0.107) | 0.061* (0.036; p=0.094) |
| Sum k = -2..+1 | 0.099*** (0.027; p=<0.001) | 0.171*** (0.053; p=0.001) | 0.024 (0.016; p=0.121) | 0.069 (0.045; p=0.129) |
| Ref. k = -4 only: k = -3 | 0.010 (0.009; p=0.269) | -0.004 (0.022; p=0.852) | 0.008 (0.005; p=0.166) | -0.032 (0.021; p=0.120) |
| Rate in ref. years: displaced / controls | 0.024 / 0.022 | 0.149 / 0.130 | 0.008 / 0.008 | 0.115 / 0.099 |
| N wife-years / displaced / control units / clusters | 212,723 / 894 / 28,021 / 1,762 | 212,723 / 894 / 28,021 / 1,762 | 212,723 / 894 / 28,021 / 1,762 | 212,723 / 894 / 28,021 / 1,762 |
| **Black** | | | | |
| k = -4 (ref.) | 0 | 0 | 0 | 0 |
| k = -3 (ref.) | 0 | 0 | 0 | 0 |
| k = -2 | 0.031* (0.018; p=0.086) | 0.015 (0.028; p=0.592) | -0.002 (0.009; p=0.826) | -0.002 (0.023; p=0.920) |
| k = -1 | 0.026* (0.015; p=0.080) | 0.038 (0.027; p=0.152) | 0.004 (0.009; p=0.647) | 0.026 (0.023; p=0.264) |
| k = +0 | 0.055*** (0.019; p=0.005) | 0.064* (0.033; p=0.052) | 0.013 (0.011; p=0.257) | 0.004 (0.027; p=0.867) |
| k = +1 | 0.059*** (0.018; p=<0.001) | 0.064** (0.032; p=0.046) | 0.001 (0.008; p=0.889) | 0.020 (0.029; p=0.501) |
| k = +2 | 0.012 (0.014; p=0.408) | -0.018 (0.030; p=0.561) | 0.002 (0.008; p=0.790) | -0.008 (0.025; p=0.755) |
| k = +3 | 0.040** (0.019; p=0.033) | 0.027 (0.035; p=0.439) | 0.009 (0.010; p=0.394) | -0.012 (0.025; p=0.621) |
| k = +4 | 0.013 (0.015; p=0.378) | -0.014 (0.032; p=0.662) | -0.006 (0.005; p=0.198) | -0.012 (0.028; p=0.653) |
| Mean k = -1..+1 | 0.047*** (0.012; p=<0.001) | 0.055** (0.023; p=0.016) | 0.006 (0.007; p=0.382) | 0.017 (0.020; p=0.411) |
| Sum k = -1..+1 | 0.140*** (0.036; p=<0.001) | 0.166** (0.069; p=0.016) | 0.018 (0.021; p=0.382) | 0.050 (0.061; p=0.411) |
| Sum k = -2..+1 | 0.171*** (0.045; p=<0.001) | 0.181** (0.085; p=0.032) | 0.016 (0.026; p=0.538) | 0.048 (0.073; p=0.510) |
| Ref. k = -4 only: k = -3 | 0.016 (0.015; p=0.272) | -0.011 (0.038; p=0.770) | 0.016 (0.010; p=0.107) | -0.045 (0.036; p=0.202) |
| Rate in ref. years: displaced / controls | 0.020 / 0.033 | 0.136 / 0.136 | 0.011 / 0.010 | 0.098 / 0.094 |
| N wife-years / displaced / control units / clusters | 54,190 / 361 / 7,596 / 604 | 54,190 / 361 / 7,596 / 604 | 54,190 / 361 / 7,596 / 604 | 54,190 / 361 / 7,596 / 604 |
| **White** | | | | |
| k = -4 (ref.) | 0 | 0 | 0 | 0 |
| k = -3 (ref.) | 0 | 0 | 0 | 0 |
| k = -2 | 0.010 (0.012; p=0.389) | 0.020 (0.023; p=0.373) | 0.006 (0.006; p=0.319) | 0.015 (0.021; p=0.480) |
| k = -1 | 0.018 (0.012; p=0.148) | 0.059** (0.024; p=0.014) | 0.003 (0.006; p=0.678) | 0.023 (0.021; p=0.270) |
| k = +0 | 0.025* (0.013; p=0.054) | 0.057** (0.024; p=0.017) | 0.017* (0.009; p=0.059) | 0.036* (0.021; p=0.092) |
| k = +1 | 0.004 (0.012; p=0.743) | 0.027 (0.024; p=0.262) | 0.004 (0.007; p=0.588) | 0.005 (0.020; p=0.818) |
| k = +2 | -0.002 (0.011; p=0.846) | -0.016 (0.023; p=0.509) | -0.000 (0.005; p=0.954) | -0.013 (0.021; p=0.535) |
| k = +3 | 0.007 (0.013; p=0.561) | 0.019 (0.026; p=0.452) | -0.002 (0.005; p=0.614) | 0.002 (0.021; p=0.926) |
| k = +4 | 0.012 (0.015; p=0.398) | -0.000 (0.025; p=0.986) | 0.012 (0.009; p=0.159) | -0.019 (0.020; p=0.332) |
| Mean k = -1..+1 | 0.016* (0.009; p=0.089) | 0.047*** (0.018; p=0.009) | 0.008 (0.006; p=0.172) | 0.021 (0.015; p=0.165) |
| Sum k = -1..+1 | 0.047* (0.028; p=0.089) | 0.142*** (0.055; p=0.009) | 0.023 (0.017; p=0.172) | 0.064 (0.046; p=0.165) |
| Sum k = -2..+1 | 0.058* (0.034; p=0.093) | 0.163** (0.068; p=0.016) | 0.029 (0.019; p=0.129) | 0.079 (0.058; p=0.178) |
| Ref. k = -4 only: k = -3 | 0.007 (0.011; p=0.519) | -0.002 (0.026; p=0.940) | 0.003 (0.006; p=0.634) | -0.027 (0.025; p=0.285) |
| Rate in ref. years: displaced / controls | 0.026 / 0.019 | 0.156 / 0.129 | 0.006 / 0.007 | 0.125 / 0.100 |
| N wife-years / displaced / control units / clusters | 158,533 / 533 / 20,425 / 1,235 | 158,533 / 533 / 20,425 / 1,235 | 158,533 / 533 / 20,425 / 1,235 | 158,533 / 533 / 20,425 / 1,235 |
| **Black - White (separate regressions, independent clusters)** | | | | |
| Mean k = -1..+1 | 0.031** (0.015; p=0.041) | 0.008 (0.029; p=0.788) | -0.002 (0.009; p=0.853) | -0.005 (0.025; p=0.858) |
| Sum k = -1..+1 | 0.093** (0.045; p=0.041) | 0.024 (0.088; p=0.788) | -0.005 (0.027; p=0.853) | -0.014 (0.076; p=0.858) |
| Sum k = -2..+1 | 0.113** (0.056; p=0.044) | 0.018 (0.108; p=0.866) | -0.013 (0.033; p=0.686) | -0.031 (0.093; p=0.740) |

### 1b. Year by year without the couple fixed effect (no reference year)

Same units; for each k a cross-section OLS of the indicator on displaced with event-year fixed effects.

| | k=-4 | k=-3 | k=-2 | k=-1 | k=+0 | k=+1 | k=+2 | k=+3 | k=+4 |
|---|---|---|---|---|---|---|---|---|---|
| **All** | | | | | | | | | |
| Wife displaced: displaced / control rate | 0.020 / 0.023 | 0.026 / 0.022 | 0.049 / 0.024 | 0.056 / 0.027 | 0.071 / 0.023 | 0.052 / 0.020 | 0.028 / 0.018 | 0.040 / 0.017 | 0.035 / 0.017 |
| Wife displaced: excess (event-year FE) | -0.004 (0.006; p=0.542) | 0.006 (0.006; p=0.311) | 0.023*** (0.008; p=0.003) | 0.029*** (0.008; p=<0.001) | 0.044*** (0.010; p=<0.001) | 0.031*** (0.008; p=<0.001) | 0.008 (0.007; p=0.235) | 0.023*** (0.008; p=0.004) | 0.017** (0.008; p=0.036) |
| Wife's employer closed: displaced / control rate | 0.005 / 0.008 | 0.010 / 0.007 | 0.014 / 0.008 | 0.014 / 0.009 | 0.026 / 0.008 | 0.010 / 0.007 | 0.008 / 0.006 | 0.007 / 0.006 | 0.011 / 0.006 |
| Wife's employer closed: excess (event-year FE) | -0.003 (0.003; p=0.361) | 0.003 (0.004; p=0.383) | 0.005 (0.004; p=0.260) | 0.005 (0.004; p=0.189) | 0.017*** (0.006; p=0.004) | 0.003 (0.004; p=0.385) | 0.001 (0.004; p=0.707) | 0.001 (0.004; p=0.720) | 0.005 (0.005; p=0.301) |
| **Black** | | | | | | | | | |
| Wife displaced: displaced / control rate | 0.016 / 0.034 | 0.023 / 0.031 | 0.057 / 0.035 | 0.055 / 0.040 | 0.080 / 0.032 | 0.074 / 0.028 | 0.026 / 0.026 | 0.048 / 0.023 | 0.026 / 0.021 |
| Wife displaced: excess (event-year FE) | -0.018* (0.009; p=0.057) | -0.004 (0.009; p=0.689) | 0.021 (0.014; p=0.134) | 0.018 (0.013; p=0.162) | 0.046*** (0.017; p=0.005) | 0.048*** (0.016; p=0.003) | -0.002 (0.011; p=0.873) | 0.028* (0.015; p=0.058) | 0.004 (0.012; p=0.763) |
| Wife's employer closed: displaced / control rate | 0.005 / 0.011 | 0.015 / 0.009 | 0.012 / 0.011 | 0.017 / 0.012 | 0.024 / 0.010 | 0.008 / 0.009 | 0.009 / 0.008 | 0.014 / 0.007 | 0.000 / 0.007 |
| Wife's employer closed: excess (event-year FE) | -0.007 (0.006; p=0.220) | 0.008 (0.008; p=0.288) | 0.001 (0.006; p=0.831) | 0.008 (0.007; p=0.292) | 0.014 (0.009; p=0.113) | 0.001 (0.006; p=0.916) | 0.001 (0.006; p=0.868) | 0.008 (0.008; p=0.339) | -0.006*** (0.001; p=<0.001) |
| **White** | | | | | | | | | |
| Wife displaced: displaced / control rate | 0.022 / 0.019 | 0.028 / 0.018 | 0.044 / 0.020 | 0.057 / 0.022 | 0.066 / 0.020 | 0.039 / 0.018 | 0.030 / 0.015 | 0.035 / 0.016 | 0.041 / 0.015 |
| Wife displaced: excess (event-year FE) | 0.002 (0.008; p=0.787) | 0.010 (0.008; p=0.199) | 0.022** (0.009; p=0.019) | 0.034*** (0.010; p=<0.001) | 0.041*** (0.012; p=<0.001) | 0.020** (0.009; p=0.031) | 0.012 (0.008; p=0.164) | 0.020** (0.009; p=0.039) | 0.023** (0.011; p=0.027) |
| Wife's employer closed: displaced / control rate | 0.006 / 0.007 | 0.007 / 0.007 | 0.015 / 0.007 | 0.012 / 0.008 | 0.027 / 0.007 | 0.011 / 0.006 | 0.007 / 0.005 | 0.003 / 0.006 | 0.017 / 0.005 |
| Wife's employer closed: excess (event-year FE) | -0.002 (0.004; p=0.652) | 0.000 (0.004; p=0.965) | 0.006 (0.005; p=0.250) | 0.003 (0.005; p=0.494) | 0.018** (0.008; p=0.019) | 0.005 (0.005; p=0.339) | 0.001 (0.004; p=0.755) | -0.003 (0.003; p=0.311) | 0.011 (0.007; p=0.107) |

## 2. Window estimates with a placebo window and a future-displacement placebo

Father x stack units, wife employed at baseline, event years 1987-2021, both windows covered (one sample for all columns). OLS with event-year fixed effects. The future placebo compares men who will be displaced 4-6 years after ev with the same clean controls: if the excess reflected riskier couples (assortative risk) rather than a common shock, it would appear for them too. 'Difference' = W - PL, a design with a couple fixed effect.

| | Wife displaced, ev-1..ev+1 | Wife displaced, ev-4..ev-2 (placebo window) | Difference (couple FE) | Any job end, ev-1..ev+1 | Any job end, difference | Employer closed, ev-1..ev+1 | Employer closed, difference |
|---|---|---|---|---|---|---|---|
| **All** | | | | | | | |
| Husband displaced in ev | 0.052*** (0.014; p=<0.001) | 0.021* (0.013; p=0.093) | 0.031* (0.017; p=0.077) | 0.122*** (0.022; p=<0.001) | 0.073** (0.029; p=0.010) | 0.015* (0.009; p=0.079) | 0.008 (0.011; p=0.451) |
| Husband displaced in ev+4..ev+6 (future placebo) | 0.007 (0.012; p=0.553) | 0.033** (0.013; p=0.012) | -0.026 (0.016; p=0.114) | 0.051** (0.022; p=0.020) | -0.016 (0.023; p=0.481) | -0.010** (0.005; p=0.047) | -0.008 (0.007; p=0.252) |
| Control mean | 0.058 | 0.056 | 0.001 | 0.289 | -0.012 | 0.021 | 0.001 |
| Broader sample (window covered only): husband displaced in ev | 0.083*** (0.013; p=<0.001) |  |  | 0.170*** (0.018; p=<0.001) |  | 0.019** (0.008; p=0.013) |  |
| Broader sample: future placebo | 0.016 (0.011; p=0.161) |  |  | 0.067*** (0.020; p=0.001) |  | -0.006 (0.005; p=0.264) |  |
| Broader sample: control mean / N / displaced | 0.063 / 26,024 / 738 |  |  | 0.316 / 26,024 / 738 |  | 0.022 / 26,024 / 738 |  |
| N couples / displaced / future placebo / clusters | 21,584 / 486 / 861 / 1,495 | 21,584 / 486 / 861 / 1,495 | 21,584 / 486 / 861 / 1,495 | 21,584 / 486 / 861 / 1,495 | 21,584 / 486 / 861 / 1,495 | 21,584 / 486 / 861 / 1,495 | 21,584 / 486 / 861 / 1,495 |
| **Black** | | | | | | | |
| Husband displaced in ev | 0.081*** (0.029; p=0.005) | 0.022 (0.026; p=0.392) | 0.059* (0.034; p=0.082) | 0.111*** (0.040; p=0.005) | 0.090* (0.050; p=0.072) | 0.015 (0.016; p=0.346) | 0.010 (0.019; p=0.587) |
| Husband displaced in ev+4..ev+6 (future placebo) | -0.008 (0.025; p=0.741) | 0.051* (0.029; p=0.078) | -0.059 (0.039; p=0.126) | 0.033 (0.045; p=0.466) | -0.060 (0.047; p=0.201) | -0.020** (0.009; p=0.024) | -0.020 (0.017; p=0.250) |
| Control mean | 0.078 | 0.080 | -0.001 | 0.291 | -0.013 | 0.027 | 0.000 |
| Broader sample (window covered only): husband displaced in ev | 0.088*** (0.024; p=<0.001) |  |  | 0.151*** (0.031; p=<0.001) |  | 0.017 (0.012; p=0.176) |  |
| Broader sample: future placebo | -0.008 (0.022; p=0.712) |  |  | 0.057 (0.040; p=0.154) |  | -0.021** (0.009; p=0.021) |  |
| Broader sample: control mean / N / displaced | 0.087 / 6,576 / 267 |  |  | 0.328 / 6,576 / 267 |  | 0.028 / 6,576 / 267 |  |
| N couples / displaced / future placebo / clusters | 4,920 / 158 / 249 / 464 | 4,920 / 158 / 249 / 464 | 4,920 / 158 / 249 / 464 | 4,920 / 158 / 249 / 464 | 4,920 / 158 / 249 / 464 | 4,920 / 158 / 249 / 464 | 4,920 / 158 / 249 / 464 |
| **White** | | | | | | | |
| Husband displaced in ev | 0.036** (0.016; p=0.023) | 0.017 (0.014; p=0.246) | 0.019 (0.020; p=0.334) | 0.125*** (0.027; p=<0.001) | 0.065* (0.034; p=0.060) | 0.015 (0.010; p=0.158) | 0.008 (0.013; p=0.525) |
| Husband displaced in ev+4..ev+6 (future placebo) | 0.010 (0.013; p=0.418) | 0.022 (0.014; p=0.117) | -0.012 (0.017; p=0.478) | 0.060** (0.025; p=0.018) | 0.003 (0.026; p=0.920) | -0.006 (0.006; p=0.292) | -0.003 (0.006; p=0.675) |
| Control mean | 0.052 | 0.050 | 0.002 | 0.289 | -0.012 | 0.020 | 0.001 |
| Broader sample (window covered only): husband displaced in ev | 0.077*** (0.016; p=<0.001) |  |  | 0.176*** (0.023; p=<0.001) |  | 0.020** (0.010; p=0.041) |  |
| Broader sample: future placebo | 0.024* (0.013; p=0.066) |  |  | 0.070*** (0.023; p=0.002) |  | 0.000 (0.007; p=0.952) |  |
| Broader sample: control mean / N / displaced | 0.056 / 19,448 / 471 |  |  | 0.312 / 19,448 / 471 |  | 0.020 / 19,448 / 471 |  |
| N couples / displaced / future placebo / clusters | 16,664 / 328 / 612 / 1,077 | 16,664 / 328 / 612 / 1,077 | 16,664 / 328 / 612 / 1,077 | 16,664 / 328 / 612 / 1,077 | 16,664 / 328 / 612 / 1,077 | 16,664 / 328 / 612 / 1,077 | 16,664 / 328 / 612 / 1,077 |
| **Pooled with race interactions** | | | | | | | |
| Husband displaced in ev | 0.036** (0.016; p=0.023) | 0.017 (0.014; p=0.232) | 0.019 (0.020; p=0.345) | 0.124*** (0.027; p=<0.001) | 0.063* (0.034; p=0.066) | 0.015 (0.010; p=0.145) | 0.009 (0.013; p=0.511) |
| Husband displaced in ev+4..ev+6 (future placebo) | 0.009 (0.013; p=0.474) | 0.021 (0.014; p=0.138) | -0.012 (0.017; p=0.480) | 0.060** (0.025; p=0.018) | 0.001 (0.026; p=0.963) | -0.007 (0.006; p=0.253) | -0.003 (0.006; p=0.677) |
| Displaced in ev x Black | 0.042 (0.033; p=0.201) | 0.004 (0.029; p=0.894) | 0.038 (0.039; p=0.339) | -0.007 (0.048; p=0.877) | 0.032 (0.061; p=0.602) | -0.002 (0.019; p=0.913) | -0.001 (0.023; p=0.956) |
| Future placebo x Black | -0.013 (0.028; p=0.627) | 0.035 (0.032; p=0.284) | -0.048 (0.042; p=0.257) | -0.031 (0.051; p=0.545) | -0.060 (0.054; p=0.263) | -0.012 (0.011; p=0.259) | -0.018 (0.019; p=0.342) |
| Black | 0.026*** (0.008; p=<0.001) | 0.029*** (0.007; p=<0.001) | -0.003 (0.006; p=0.592) | 0.000 (0.015; p=0.984) | -0.001 (0.009; p=0.885) | 0.006 (0.004; p=0.144) | -0.001 (0.003; p=0.774) |
| Control mean | 0.058 | 0.056 | 0.001 | 0.289 | -0.012 | 0.021 | 0.001 |
| N couples / displaced / future placebo / clusters | 21,584 / 486 / 861 / 1,495 | 21,584 / 486 / 861 / 1,495 | 21,584 / 486 / 861 / 1,495 | 21,584 / 486 / 861 / 1,495 | 21,584 / 486 / 861 / 1,495 | 21,584 / 486 / 861 / 1,495 | 21,584 / 486 / 861 / 1,495 |
| Fixed effects | event year | event year | event year | event year | event year | event year | event year |

### 2b. Sample sensitivity of the window estimate

Wife displaced in ev-1..ev+1 on husband displaced, event-year FE, wives employed at baseline, treated vs clean controls. Cell: coefficient (s.e.; p) [control mean; displaced / N].

| | All | Black | White |
|---|---|---|---|
| 23's window variable and sample (ev 1984-2021, wife seen before and after) | 0.076*** (0.012; p=<0.001) [ctrl 0.066; 833 / 27,134] | 0.080*** (0.022; p=<0.001) [ctrl 0.090; 304 / 6,811] | 0.070*** (0.015; p=<0.001) [ctrl 0.058; 529 / 20,323] |
| ev 1984-2021, all three window years covered | 0.075*** (0.012; p=<0.001) [ctrl 0.066; 826 / 27,022] | 0.077*** (0.022; p=<0.001) [ctrl 0.089; 299 / 6,757] | 0.070*** (0.015; p=<0.001) [ctrl 0.058; 527 / 20,265] |
| ev 1984-1989 | 0.027 (0.025; p=0.282) [ctrl 0.088; 175 / 4,335] | 0.017 (0.047; p=0.710) [ctrl 0.112; 55 / 1,104] | 0.029 (0.029; p=0.322) [ctrl 0.080; 120 / 3,231] |
| ev 1990-1999 | 0.073*** (0.025; p=0.003) [ctrl 0.075; 230 / 7,715] | 0.071 (0.051; p=0.163) [ctrl 0.103; 68 / 2,076] | 0.073** (0.029; p=0.010) [ctrl 0.066; 162 / 5,639] |
| ev 2000-2021 | 0.095*** (0.017; p=<0.001) [ctrl 0.055; 421 / 14,972] | 0.098*** (0.028; p=<0.001) [ctrl 0.075; 176 / 3,577] | 0.089*** (0.021; p=<0.001) [ctrl 0.049; 245 / 11,395] |
| ev 1987-2021, window covered | 0.083*** (0.013; p=<0.001) [ctrl 0.063; 738 / 24,879] | 0.088*** (0.024; p=<0.001) [ctrl 0.087; 267 / 6,213] | 0.077*** (0.016; p=<0.001) [ctrl 0.056; 471 / 18,666] |
| ev 1987-2021, window and placebo window covered (main sample) | 0.052*** (0.014; p=<0.001) [ctrl 0.058; 486 / 20,723] | 0.080*** (0.029; p=0.005) [ctrl 0.078; 158 / 4,671] | 0.036** (0.016; p=0.023) [ctrl 0.052; 328 / 16,052] |
| All married men, with or without children (main-sample rules) | 0.073*** (0.012; p=<0.001) [ctrl 0.055; 775 / 35,117] | 0.059*** (0.022; p=0.008) [ctrl 0.073; 219 / 7,090] | 0.076*** (0.015; p=<0.001) [ctrl 0.050; 556 / 28,027] |

## 3. Identification checks

Sample of section 2 without the future placebo. Outcome: wife displaced in ev-1..ev+1 (column 2: her employer closed). OLS with event-year fixed effects. Closures only: displaced men whose first job loss was a closure vs controls (layoffs dropped), and vice versa. Matches are measured before the event (husband: latest interview in [ev-3, ev]; wife: latest in [ev-6, ev]); the state unemployment change is in ev, in s.d. among displaced (s.d. 1.43 pp). Pre-trend controls: husband's hours and labor income at ev-2 (ev-3 in biennial years) and their change over the two years before, the wife's hours likewise, missing indicators, and the wife's own displacement in ev-4..ev-2. Self-employment: either spouse works for self (or self and others) at an interview in ev-3..ev.

| | Closures only: Wife displaced | Closures only: Wife's employer closed | Layoffs only: Wife displaced | Sector match: Wife displaced | 3-digit industry match: Wife displaced | Occupation-group match: Wife displaced | State unemployment: Wife displaced | Pre-trend controls: Wife displaced | No self-employed spouse: Wife displaced |
|---|---|---|---|---|---|---|---|---|---|
| **All** | | | | | | | | | |
| Husband displaced | 0.068** (0.027; p=0.010) | 0.054** (0.021; p=0.012) | 0.044*** (0.016; p=0.007) | 0.023* (0.014; p=0.095) | 0.030** (0.014; p=0.031) | 0.039** (0.015; p=0.012) | 0.053*** (0.014; p=<0.001) | 0.048*** (0.014; p=<0.001) | 0.038** (0.016; p=0.017) |
| Displaced x wife in his sector |  |  |  | 0.203*** (0.055; p=<0.001) |  |  |  |  |  |
| Wife in his sector |  |  |  | -0.016*** (0.005; p=0.003) |  |  |  |  |  |
| Displaced x same 3-digit industry |  |  |  |  | 0.282*** (0.078; p=<0.001) |  |  |  |  |
| Same 3-digit industry |  |  |  |  | -0.032*** (0.005; p=<0.001) |  |  |  |  |
| Displaced x same occupation group |  |  |  |  |  | 0.083** (0.042; p=0.048) |  |  |  |
| Same occupation group |  |  |  |  |  | -0.015*** (0.005; p=0.001) |  |  |  |
| Displaced x state unemployment change (s.d.) |  |  |  |  |  |  | 0.020 (0.017; p=0.246) |  |  |
| State unemployment change (s.d.) |  |  |  |  |  |  | 0.004 (0.005; p=0.503) |  |  |
| Wife displaced in ev-4..ev-2 |  |  |  |  |  |  |  | 0.086*** (0.014; p=<0.001) |  |
| Control mean | 0.058 | 0.021 | 0.058 | 0.057 | 0.057 | 0.057 | 0.057 | 0.058 | 0.060 |
| Share of displaced with the match |  |  |  | 0.148 | 0.079 | 0.190 |  |  |  |
| N couples / displaced | 20,394 / 157 | 20,394 / 157 | 20,566 / 329 | 20,401 / 481 | 20,567 / 482 | 20,198 / 478 | 20,614 / 485 | 20,723 / 486 | 15,106 / 363 |
| **Black** | | | | | | | | | |
| Husband displaced | 0.110* (0.058; p=0.056) | 0.066 (0.044; p=0.130) | 0.067** (0.033; p=0.040) | 0.045 (0.030; p=0.136) | 0.064** (0.029; p=0.029) | 0.058* (0.030; p=0.058) | 0.081*** (0.029; p=0.005) | 0.078*** (0.028; p=0.005) | 0.059* (0.031; p=0.056) |
| Displaced x wife in his sector |  |  |  | 0.196** (0.089; p=0.028) |  |  |  |  |  |
| Wife in his sector |  |  |  | -0.014 (0.014; p=0.340) |  |  |  |  |  |
| Displaced x same 3-digit industry |  |  |  |  | 0.201 (0.129; p=0.119) |  |  |  |  |
| Same 3-digit industry |  |  |  |  | -0.037** (0.016; p=0.019) |  |  |  |  |
| Displaced x same occupation group |  |  |  |  |  | 0.147* (0.087; p=0.092) |  |  |  |
| Same occupation group |  |  |  |  |  | 0.001 (0.012; p=0.940) |  |  |  |
| Displaced x state unemployment change (s.d.) |  |  |  |  |  |  | 0.002 (0.038; p=0.954) |  |  |
| State unemployment change (s.d.) |  |  |  |  |  |  | 0.000 (0.012; p=0.969) |  |  |
| Wife displaced in ev-4..ev-2 |  |  |  |  |  |  |  | 0.058** (0.024; p=0.016) |  |
| Control mean | 0.078 | 0.027 | 0.078 | 0.077 | 0.078 | 0.077 | 0.079 | 0.078 | 0.082 |
| Share of displaced with the match |  |  |  | 0.192 | 0.083 | 0.188 |  |  |  |
| N couples / displaced | 4,557 / 44 | 4,557 / 44 | 4,627 / 114 | 4,576 / 156 | 4,605 / 157 | 4,489 / 154 | 4,655 / 157 | 4,671 / 158 | 3,907 / 127 |
| **White** | | | | | | | | | |
| Husband displaced | 0.051* (0.029; p=0.080) | 0.048** (0.024; p=0.048) | 0.028 (0.018; p=0.124) | 0.012 (0.015; p=0.422) | 0.011 (0.015; p=0.448) | 0.028 (0.017; p=0.109) | 0.037** (0.016; p=0.020) | 0.033** (0.016; p=0.036) | 0.023 (0.018; p=0.196) |
| Displaced x wife in his sector |  |  |  | 0.190*** (0.070; p=0.006) |  |  |  |  |  |
| Wife in his sector |  |  |  | -0.016*** (0.006; p=0.006) |  |  |  |  |  |
| Displaced x same 3-digit industry |  |  |  |  | 0.318*** (0.097; p=0.001) |  |  |  |  |
| Same 3-digit industry |  |  |  |  | -0.029*** (0.005; p=<0.001) |  |  |  |  |
| Displaced x same occupation group |  |  |  |  |  | 0.047 (0.044; p=0.286) |  |  |  |
| Same occupation group |  |  |  |  |  | -0.018*** (0.005; p=<0.001) |  |  |  |
| Displaced x state unemployment change (s.d.) |  |  |  |  |  |  | 0.028 (0.019; p=0.147) |  |  |
| State unemployment change (s.d.) |  |  |  |  |  |  | 0.005 (0.006; p=0.452) |  |  |
| Wife displaced in ev-4..ev-2 |  |  |  |  |  |  |  | 0.093*** (0.017; p=<0.001) |  |
| Control mean | 0.052 | 0.020 | 0.052 | 0.051 | 0.051 | 0.051 | 0.051 | 0.052 | 0.053 |
| Share of displaced with the match |  |  |  | 0.126 | 0.077 | 0.191 |  |  |  |
| N couples / displaced | 15,837 / 113 | 15,837 / 113 | 15,939 / 215 | 15,825 / 325 | 15,962 / 325 | 15,709 / 324 | 15,959 / 328 | 16,052 / 328 | 11,199 / 236 |
| Fixed effects | event year | event year | event year | event year | event year | event year | event year | event year | event year |

## 4. Magnitudes for the model: joint job-loss probabilities within couples

Couple-years: consecutive interviews of the same couple, both spouses with positive annual hours in the earlier year, intervals ending 1984-2022. h = husband displaced (closure / layoff) in the interval; w = wife displaced in the same interval (one year to 1996, two years in the biennial survey; 'annual' rows keep one-year intervals 1984-1996, the model's period). Sector match: both spouses' sectors at the interview opening the interval. Difference: OLS of w on h, clustered by 1968 family. Ratio, phi and tetrachoric correlation: s.e. from 200 bootstrap draws of 1968 families (p-values from the normal approximation).

| | Couple-years | P(h) | P(w) | P(w | h) (N h) | P(w | not h) | Ratio (s.e.) | P(w|h) - P(w|not h) | Phi | Tetrachoric |
|---|---|---|---|---|---|---|---|---|---|
| **Wife displaced in the same interval as the husband's displacement** | | | | | | | | | |
| All couple-years | 62,069 | 0.0529 | 0.0423 | 0.102 (3,285) | 0.0390 | 2.61 (0.15) | 0.063*** (0.005; p=<0.001) | 0.070*** (0.006; p=<0.001) | 0.237*** (0.016; p=<0.001) |
| Black | 15,160 | 0.0702 | 0.0531 | 0.105 (1,064) | 0.0492 | 2.14 (0.19) | 0.056*** (0.009; p=<0.001) | 0.064*** (0.010; p=<0.001) | 0.201*** (0.025; p=<0.001) |
| White | 46,909 | 0.0473 | 0.0388 | 0.100 (2,221) | 0.0358 | 2.80 (0.19) | 0.064*** (0.006; p=<0.001) | 0.071*** (0.007; p=<0.001) | 0.248*** (0.018; p=<0.001) |
| Same sector | 10,420 | 0.0364 | 0.0349 | 0.211 (379) | 0.0283 | 7.46 (0.89) | 0.183*** (0.022; p=<0.001) | 0.186*** (0.020; p=<0.001) | 0.504*** (0.032; p=<0.001) |
| Different sector | 44,683 | 0.0481 | 0.0368 | 0.076 (2,149) | 0.0348 | 2.19 (0.17) | 0.041*** (0.006; p=<0.001) | 0.047*** (0.006; p=<0.001) | 0.182*** (0.020; p=<0.001) |
| Black, same sector | 2,258 | 0.0558 | 0.0368 | 0.159 (126) | 0.0295 | 5.37 (1.41) | 0.129*** (0.035; p=<0.001) | 0.158*** (0.041; p=<0.001) | 0.434*** (0.075; p=<0.001) |
| White, same sector | 8,162 | 0.0310 | 0.0344 | 0.237 (253) | 0.0279 | 8.49 (1.14) | 0.209*** (0.027; p=<0.001) | 0.199*** (0.024; p=<0.001) | 0.532*** (0.036; p=<0.001) |
| Youngest child 0-5 | 15,903 | 0.0647 | 0.0446 | 0.105 (1,029) | 0.0404 | 2.60 (0.25) | 0.065*** (0.009; p=<0.001) | 0.077*** (0.010; p=<0.001) | 0.245*** (0.026; p=<0.001) |
| Youngest child 6-17 | 20,304 | 0.0525 | 0.0432 | 0.091 (1,066) | 0.0406 | 2.24 (0.24) | 0.050*** (0.009; p=<0.001) | 0.055*** (0.010; p=<0.001) | 0.197*** (0.028; p=<0.001) |
| No child under 18 | 25,862 | 0.0460 | 0.0401 | 0.108 (1,190) | 0.0368 | 2.94 (0.27) | 0.072*** (0.009; p=<0.001) | 0.076*** (0.010; p=<0.001) | 0.263*** (0.025; p=<0.001) |
| Annual survey years (to 1996) | 32,386 | 0.0492 | 0.0419 | 0.090 (1,593) | 0.0394 | 2.29 (0.19) | 0.051*** (0.007; p=<0.001) | 0.055*** (0.008; p=<0.001) | 0.200*** (0.023; p=<0.001) |
| Annual, Black | 7,936 | 0.0600 | 0.0514 | 0.088 (476) | 0.0491 | 1.80 (0.28) | 0.039*** (0.013; p=0.002) | 0.042*** (0.014; p=0.003) | 0.147*** (0.043; p=<0.001) |
| Annual, White | 24,450 | 0.0457 | 0.0389 | 0.091 (1,117) | 0.0363 | 2.51 (0.24) | 0.055*** (0.008; p=<0.001) | 0.059*** (0.009; p=<0.001) | 0.219*** (0.026; p=<0.001) |
| **Wife displaced in the interval or within one year of it** | | | | | | | | | |
| All couple-years | 54,422 | 0.0511 | 0.0954 | 0.181 (2,783) | 0.0908 | 1.99 (0.09) | 0.090*** (0.008; p=<0.001) | 0.067*** (0.006; p=<0.001) | 0.201*** (0.015; p=<0.001) |
| Black | 12,789 | 0.0671 | 0.1174 | 0.183 (858) | 0.1127 | 1.62 (0.14) | 0.070*** (0.015; p=<0.001) | 0.055*** (0.012; p=<0.001) | 0.151*** (0.030; p=<0.001) |
| White | 41,633 | 0.0462 | 0.0886 | 0.180 (1,925) | 0.0842 | 2.13 (0.10) | 0.096*** (0.009; p=<0.001) | 0.071*** (0.006; p=<0.001) | 0.216*** (0.016; p=<0.001) |
| Same sector | 9,136 | 0.0350 | 0.0713 | 0.275 (320) | 0.0639 | 4.31 (0.42) | 0.211*** (0.024; p=<0.001) | 0.151*** (0.017; p=<0.001) | 0.415*** (0.031; p=<0.001) |
| Different sector | 39,181 | 0.0464 | 0.0830 | 0.148 (1,819) | 0.0799 | 1.85 (0.11) | 0.068*** (0.009; p=<0.001) | 0.052*** (0.006; p=<0.001) | 0.168*** (0.017; p=<0.001) |
| Black, same sector | 1,900 | 0.0542 | 0.0789 | 0.194 (103) | 0.0723 | 2.68 (0.59) | 0.122*** (0.040; p=0.002) | 0.102*** (0.031; p=0.001) | 0.286*** (0.071; p=<0.001) |
| White, same sector | 7,236 | 0.0300 | 0.0692 | 0.313 (217) | 0.0617 | 5.08 (0.60) | 0.252*** (0.030; p=<0.001) | 0.169*** (0.022; p=<0.001) | 0.460*** (0.039; p=<0.001) |
| Youngest child 0-5 | 13,945 | 0.0626 | 0.1035 | 0.206 (873) | 0.0967 | 2.13 (0.16) | 0.109*** (0.015; p=<0.001) | 0.087*** (0.012; p=<0.001) | 0.235*** (0.026; p=<0.001) |
| Youngest child 6-17 | 17,754 | 0.0509 | 0.0987 | 0.164 (903) | 0.0952 | 1.72 (0.14) | 0.069*** (0.013; p=<0.001) | 0.051*** (0.009; p=<0.001) | 0.156*** (0.025; p=<0.001) |
| No child under 18 | 22,723 | 0.0443 | 0.0878 | 0.174 (1,007) | 0.0838 | 2.07 (0.17) | 0.090*** (0.013; p=<0.001) | 0.065*** (0.010; p=<0.001) | 0.205*** (0.025; p=<0.001) |
| Annual survey years (to 1996) | 29,820 | 0.0471 | 0.1079 | 0.190 (1,404) | 0.1039 | 1.83 (0.12) | 0.086*** (0.012; p=<0.001) | 0.059*** (0.008; p=<0.001) | 0.178*** (0.021; p=<0.001) |
| Annual, Black | 7,064 | 0.0559 | 0.1287 | 0.185 (395) | 0.1254 | 1.47 (0.18) | 0.059*** (0.023; p=0.009) | 0.041*** (0.015; p=0.007) | 0.120*** (0.041; p=0.003) |
| Annual, White | 22,756 | 0.0443 | 0.1015 | 0.192 (1,009) | 0.0973 | 1.98 (0.14) | 0.095*** (0.013; p=<0.001) | 0.065*** (0.009; p=<0.001) | 0.198*** (0.024; p=<0.001) |

## 5. How much of the family income loss is the wife's joint job loss?

19's stacked design (father x stack and calendar year x stack fixed effects, mean of e = +1..+3 relative to e = -2; 2000 dollars). Married fathers, event years 1984-2021 (window measurable). Accounting, not causal: the wife's job loss is an outcome; the cost is the change that comes with her displacement among control families (bin x J coefficient in the model with displaced x bin x J). The DiD version replaces P1 - P0 by the window difference-in-differences of section 2 (pooled) times the share of displaced families whose wife worked at baseline, which removes assortative risk.

| | Estimate |
|---|---|
| Family income response, all fathers (19's design, re-estimated) | -9,345*** (960; p=<0.001) |
| Family income response, married, ev 1984-2021 | -11,631*** (1,783; p=<0.001) |
| Wife's labor income response, same sample | -686 (546; p=0.209) |
| Husband's labor income response, same sample | -10,171*** (1,454; p=<0.001) |
| P(wife displaced ev-1..ev+1): displaced / control families (0 if not working at baseline) | 0.106 / 0.050 |
| Share of displaced families with the wife employed at baseline | 0.734 |
| Cost of the wife's displacement, family income (control families, +1..+3) | -3,471 (3,682; p=0.346) |
| Cost of the wife's displacement, her labor income | -4,611*** (822; p=<0.001) |
| Joint-loss channel, family income: (P1 - P0) x cost | -193 (205; p=0.346) |
| Joint-loss channel, family income: DiD excess x share employed x cost | -78 (94; p=0.405) |
| Joint-loss channel, family income: (window excess - future placebo, 0.067) x share employed x cost | -170 (186; p=0.360) |
| Joint-loss channel, wife's labor income: same, net version | -226*** (72; p=0.002) |
| Share of the married-sample family income loss: (P1-P0) / DiD version | 0.017 / 0.007 |
| Share of 19's pooled loss (x share of displaced fathers with a wife, 0.950): (P1-P0) / DiD version | 0.020 / 0.008 |
| Family income loss beyond the husband's labor income loss (married sample) | -1,460 |
| Joint-loss channel (wife's labor income) as a share of that gap | 0.18 |
| Joint-loss channel, wife's labor income: (P1 - P0) x cost / share of her response | -256*** (46; p=<0.001) / 0.37 |
| N man-years / displaced fathers (married sample) | 207,954 / 1,126 |

## 6. Summary paragraphs for paper/sec6_why.tex (not inserted; numbers generated by this script)

When a husband is displaced, the household's second earner is often hit by the same shock. I measure the wife's own job losses from her answers to the PSID question on why a job ended (asked of wives from 1984), and compare the wives of men displaced in a given year with the wives of men not displaced in the following six years, among wives working before the event. Over the three years around the husband's displacement (the year before to the year after), the probability that the wife is herself laid off, fired or loses her job to a closure is higher by 8.3*** (s.e. 1.3; p<0.001) percentage points, from a base of 6.3%: her risk of a job loss more than doubles. Year by year, with couple and calendar-year fixed effects and the fourth and third years before the event as the reference, the excess appears two years before the husband's job loss (0.018* (s.e. 0.010; p=0.069)), peaks in the year of his job loss (0.036*** (s.e. 0.011; p<0.001)) and is gone by the second year after it (0.003 (s.e. 0.009; p=0.754)); the closure of her employer rises only in the year of his job loss (0.015** (s.e. 0.007; p=0.029)). The early start is consistent with the two spouses' reports dating the same events a year apart and with shocks that reach a workplace before they reach a particular worker. It is not a permanent difference between couples: the wives of men who will be displaced four to six years later have no excess risk in the same window (1.6 (s.e. 1.1; p=0.161) points), and the excess survives controls for both spouses' hours and earnings before the event (4.8*** (s.e. 1.4; p<0.001) points, in the subsample that also observes the earlier window) and the exclusion of self-employed spouses (3.8** (s.e. 1.6; p=0.017)).

The joint losses come from shared workplaces and industries rather than from the local business cycle. When the husband's job loss is a plant closure, the wife's risk rises by 6.8** (s.e. 2.7; p=0.010) points and the probability that her own employer closes by 5.4** (s.e. 2.1; p=0.012). The excess is concentrated among couples who work in the same sector (15% of displaced couples; interaction 20.3*** (s.e. 5.5; p<0.001) points) and especially in the same three-digit industry (8%; 28.2*** (s.e. 7.8; p<0.001)), the closest proxy the public PSID offers for a common employer. It does not vary with the change in the state unemployment rate (2.0 (s.e. 1.7; p=0.246) points per standard deviation).

For the model, the relevant object is the joint probability of the two job losses. Among couple-years in which both spouses worked, the wife is displaced in the same interval in 10.2% of the cases in which the husband is displaced and in 3.9% of the others (difference 6.3*** (s.e. 0.5; p<0.001) points; ratio 2.6); in the annual survey years the figures are 9.0% and 3.9%. The implied tetrachoric correlation of the two job-loss events is 0.24*** (s.e. 0.02; p<0.001) (0.20 in the annual years; phi 0.070): 0.50 for couples in the same sector and 0.18 for the others, 0.20 for Black and 0.25 for White couples. Joint job loss is a general feature of family insurance; the racial difference is second order. Black wives' baseline risk is higher, and the excess around the husband's job loss is at least as large for Black as for White couples (window 8.8*** (s.e. 2.4; p<0.001) against 7.7*** (s.e. 1.6; p<0.001) points). Whether it is larger depends on the design: in the couple fixed-effects event study the Black-White difference in the mean of years -1 to +1 is 3.1** (s.e. 1.5; p=0.041) points a year, in the window design on the subsample that also observes the earlier window it is 4.2 (s.e. 3.3; p=0.201).

The joint losses cost the wife earnings but account for little of the family's income loss. Among control families a wife's displacement lowers her labor income by 4,611*** (s.e. 822; p<0.001) dollars a year over the next three years. With an excess probability of 0.056 among all married fathers (her displacement is zero if she did not work), the joint loss lowers the average wife's labor income after the husband's displacement by 256*** (s.e. 46; p<0.001) dollars (226*** (s.e. 72; p=0.002) with the window excess net of the future-displacement placebo, 0.067, times the 73% of wives working at baseline): about 18% of the 1,460 dollars by which family income falls beyond the husband's own labor income, and 2% of the family income loss (11,631*** (s.e. 1,783; p<0.001) dollars). The joint loss matters for insurance less through its average cost than through its timing: it removes the second earner in the states in which she is needed, so a model in which the second earner's job loss is independent of the first earner's overstates the insurance the family can provide.

Footnote: Code: IGE/25.JointJobLoss.py; tables tab:joint_job_loss, tab:joint_job_loss_id, tab:joint_job_loss_magnitudes in paper/tab_joint_job_loss.tex; figure output/joint_job_loss_es.png. Wives' reasons for a job ending are asked from the 1984 wave; event years 1987-2021; standard errors clustered by 1968 family. (In LaTeX: escape % as \%.)

## 7. Literature check (2026-10-17): is joint job loss within couples documented?

Every entry was checked on the linked source page in this session; "(PDF read)" = the full text was searched.

Already documented
- Spouses' labor market outcomes are positively correlated, mostly through permanent components: Hyslop (2001), "Rising
  U.S. Earnings Inequality and Family Labor Supply: The Covariance Structure of Intrafamily Earnings", AER 91(4): 755-777
  (PSID; abstract: working couples' positively correlated outcomes are "almost entirely attributable to permanent
  factors"). https://ideas.repec.org/a/aea/aecrev/v91y2001i4p755-777.html
- The correlation moves with the cycle: Shore (2010), "For Better, For Worse: Intrahousehold Risk-Sharing over the
  Business Cycle", REStat 92(3): 536-548 (spouses' incomes more positively correlated in booms, so household risk is not
  countercyclical). https://ideas.repec.org/a/tpr/restat/v92y2010i3p536-548.html
- Spouses sort on employer, industry and occupation, and sorted couples' earnings changes are more correlated: Hyatt,
  "Co-Working Couples and the Similar Jobs of Dual-Earner Households" (Census CES WP 15-23R; Monthly Labor Review 2019):
  10-12% of dual-earner couples work at the same establishment, 11-13% for the same firm (Census 2000 linked to LEHD);
  layoffs "at similar times" and the insurance value of marriage are mentioned only in passing.
  https://www.bls.gov/opub/mlr/2019/article/coworking-couples-and-the-similar-jobs-of-dual-earner-households.htm ;
  Busch, Madera (with Groes), "Assortative Mating and Joint Income Dynamics of Couples" (Danish tax registers; sorting on
  education, occupation, industry and firm; much stronger correlation of earnings changes in sorted couples; no
  displacement events on the project page). https://bse.eu/research/assortative-mating-and-joint-income-dynamics-couples
- Displacement studies know that both spouses are sometimes displaced together and drop those couples:
  Halla, Schmieder and Weber (2020), "Job Displacement, Family Dynamics, and Spousal Labor Supply", AEJ: Applied 12(4)
  (Austrian registers; couples displaced by the same firm event = 3.47% of plant-closure and 1.13% of mass-layoff
  households, dropped; only 8% of dual-earner couples share a 4-digit industry; correlated local shocks discussed as an
  explanation of the small response) (PDF read, IZA DP 11752) https://docs.iza.org/dp11752.pdf ,
  https://www.aeaweb.org/doi/10.1257/app.20180671 ;
  Marcus (2013), "The effect of unemployment on the mental health of spouses - Evidence from plant closures in Germany",
  J. Health Econ. 32(3): 546-558 (SOEP; "the plant closure experience of one spouse is likely to be correlated with a
  plant closure experience of the other spouse since spouses might work in the same plant"; excluding them cuts the
  treatment group by 7%) (PDF read, HEDG WP 12/17) https://ideas.repec.org/a/eee/jhecon/v32y2013i3p546-558.html ,
  https://www.york.ac.uk/media/economics/documents/herc/wp/12_17.pdf ;
  Banzhaf (2013), "When It Rains, It Pours: Under What Circumstances Does Job Loss Lead to Divorce", Census CES WP 13-62
  (SIPP 2001-2008 panels; couples with both spouses displaced are about 5% of couples with any displacement, dropped)
  (PDF read) https://www2.census.gov/ces/wp/2013/CES-WP-13-62.pdf
- Closest finding: Kawano, LaLumia, Ramnath and Stevens (2025), "Who picks up the slack? Understanding spousal responses
  to unemployment spells", Labour Economics 96 (a large panel of US married households; the small added-worker response
  is explained by the non-displaced spouse being more likely to leave employment, "either through correlated
  unemployment shocks or retirement"). https://ideas.repec.org/a/eee/labeco/v96y2025ics0927537125000569.html
  (data source not stated on the pages checked; the SSRN and journal pages refused access).
- Added-worker benchmarks: Stephens (2002), JOLE 20(3) (PSID; wife's labor supply before and after the husband's
  displacement; the abstract does not mention the wife's own job loss) https://www.nber.org/papers/w8260 ; Pruitt and
  Turner (2020), "Earnings Risk in the Household: Evidence from Millions of US Tax Returns", AER: Insights 2(2): 237-254
  (spousal income lowers household earnings risk; no job-loss co-occurrence in the abstract)
  https://ideas.repec.org/a/aea/aerins/v2y2020i2p237-54.html ; Cullen and Gruber (2000), Blundell, Pistaferri and
  Saporta-Eksten (2016): see proposals/insurance_literature_check.md.

What is new here (not found in any of the above)
1. An event-study estimate, in US data and with each spouse's own stated reason for the job end, of how much the wife's
   displacement risk rises around the husband's displacement (it more than doubles), year by year, with couple fixed
   effects, a placebo window and a future-displacement placebo that rules out permanent assortative risk.
2. The channels: when he loses his job to a plant closure her employer is more likely to close; the excess is
   concentrated in same-sector and same-3-digit-industry couples; it does not vary with state unemployment.
3. The comparison by race (present in both races; at least as large for Black couples; the difference is not robust).
4. The joint probability and the tetrachoric correlation of job-loss events within couples as targets for a household
   model, by sector match, child age and race.
5. Its quantitative role for family income after the husband's displacement (small on average) and its place in a paper
   on parental insurance, children and the IGE.
What is not new: that spouses' earnings are correlated, that they sort on employer and industry, that joint
displacements by the same plant event exist (and are routinely dropped), and that correlated unemployment can mute the
added-worker effect (Kawano et al. 2025 for the US; Halla et al. 2020 discuss it). Our result should be framed as
measuring and decomposing a mechanism those papers name or exclude, not as discovering it. A rough comparison: Halla et
al.'s 3.47% of Austrian closure households (about half of whose wives work) is of the same order as our excess of about
5-8 points among wives working at baseline.