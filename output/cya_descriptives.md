# NLSY79 Children: mothers' work after a birth and child outcomes (descriptive)

Script `IGE/10.CYAOutcomes.py` (2026-10-17). Data: NLSY79 Children and Young Adults 1979-2020 (public release), NLSY79 women extract (`NLSY79/data/women79.pkl`, `family79.pkl`), NLSY79 TNFI_TRUNC.

**These are correlations, not effects.** A mother's work in the year after a birth is chosen jointly with unobserved traits of the family and the child (selection); the regressions below only show the raw and covariate-adjusted association.

## Variables

| measure | CYA / NLSY79 variables | definition |
|---|---|---|
| child id, mother id | CPUBID, MPUBID | mother linked to NLSY79 R0000100 |
| race of mother | NLSY79 SAMPLE_ID (R0173600) | White 5, 6 (cross-section incl. poor White); Black 7, 13 (cross-section + supplemental) - the women of IGE/2.NLSY79.py's samples |
| sex, birth month / year, birth order, mother's age at birth | CSEX, CMOB, CYRB, BTHORDR, MAGEBIR | |
| child weight | CSAMWTyyyy_REV (1986-2000) / CSAMWTyyyy | per band: weight of the assessment round; `cwt_first`: first positive weight (regressions unweighted) |
| PIAT Math | MATHZyyyy (MATHPyyyy) | NLSY-created total standard score, national norms (mean 100, sd 15); percentile in parentheses |
| PIAT Reading Recognition | RECOGZyyyy (RECOGPyyyy) | same |
| PIAT Reading Comprehension | COMPZyyyy (COMPPyyyy) | same |
| PPVT-R | PPVTZyyyy (PPVTPyyyy) | same |
| Behavior Problems Index | BPIZyyyy (BPIPyyyy) | total standard score, all-children norms; higher = more behaviour problems |
| age at assessment | CSAGEyyyy (PIAT, PPVT), MSAGEyyyy (BPI) | months; bands 5-6 = 60-83 m, 7-8 = 84-107, 9-10 = 108-131, 11-12 = 132-155, 13-14 = 156-179; the assessment inside the band (closest to its middle if two) |
| highest grade completed by 25 | HGCyyyy (2004-20); Q4-19, Q4-1/Q4-2 (1994-2002); AGEINTyy(yy) | running max up to the YA interview closest to 25 within ages 24-26 |
| college | HGCyyyy >= 13, Q4-2 in 13-20, Q4-57~Y | ever attended by the last interview (seen at 19+); `coll_by21` from interviews at <= 21 (seen at 20-21) |
| earnings | Q15-5 (1994-98), Q15-5-TOP (2000-20) | wages and salary of the previous year, 2000 $; mean over interviews at 26-35 (zeros kept), and the latest interview at 26+ |
| mother's weeks employed | NLSY79 weekly array STATUS_WK_NUM | weeks [b, b+12], [b, b+51], [b+52, b+103] after the birth week b (scaled for weeks without information, NaN if > 1/4 missing) |
| employed before the birth | weekly array | employed in some week of [b-13, b-1] |
| same employer within a year | job roster (employer index JJ) | if employed before: works for the employer of her last employed week before b in some week of [b+5, b+52] (kept or returned) |
| married at the birth | YRBGkM/MOBGkM, YRENkM/MOENkM | marriage history |
| mother's AFQT | AFQT-3 (1981) | percentile, 2006 revision |
| mother's education | highest grade completed, max over rounds | LHS / HS / College (completed schooling, may postdate the birth) |
| family income 0-5 | TNFI_TRUNC | mean over calendar years of child age 0-5 (round t+1 reports year t), 2000 $, >= 2 years |

## Sample

CYA children (all NLSY79 mothers): 11,551. Children of White / Black mothers of the cross-sectional and Black supplemental samples: 7,594 (Hispanic, supplemental poor-White and military-sample mothers dropped).

| | White | Black |
|---|---|---|
| children | 4,488 | 3,106 |
| mothers | 1,975 | 1,225 |
| born 1978 Apr or later (weekly array covers the 13 weeks before) | 4,267 | 2,737 |
| with weeks employed months 0-12 | 4,238 | 2,712 |
| with any test score at 5-6 | 3,431 | 2,110 |
| with hgc by 25 | 2,976 | 2,220 |
| with earnings at 26-35 | 2,903 | 2,300 |
| cross-check: CRACE Black (2) | 0 | 3,106 |

## Means by race of the mother

### Mother and exposures

| variable | White mean | (sd) | N | Black mean | (sd) | N |
|---|---|---|---|---|---|---|
| weeks employed, months 0-3 (of 13) | 4.380 | (5.491) | 4,249 | 3.368 | (5.198) | 2,719 |
| weeks employed, months 0-12 (of 52) | 23.243 | (21.930) | 4,238 | 18.716 | (21.176) | 2,712 |
| weeks employed, months 13-24 (of 52) | 27.319 | (23.172) | 4,312 | 22.748 | (22.757) | 2,810 |
| employed in 13 weeks before | 0.578 | (0.494) | 4,238 | 0.393 | (0.488) | 2,693 |
| same employer within 52 weeks (if employed before) | 0.771 | (0.420) | 2,432 | 0.779 | (0.415) | 1,047 |
| married at birth | 0.878 | (0.327) | 4,485 | 0.408 | (0.492) | 3,106 |
| mother's AFQT percentile | 53.228 | (26.971) | 4,267 | 21.407 | (19.216) | 2,996 |
| mother's highest grade | 13.650 | (2.506) | 4,488 | 12.998 | (2.209) | 3,106 |
| mother's age at birth | 26.853 | (5.927) | 4,485 | 24.243 | (6.109) | 3,106 |
| family income ages 0-5 (2000 $) | 62125.335 | (73448.891) | 4,087 | 28118.710 | (32857.422) | 2,792 |
| birth order | 1.874 | (1.020) | 4,488 | 2.108 | (1.278) | 3,106 |
| child birth year | 1987.822 | (6.392) | 4,488 | 1985.333 | (6.561) | 3,106 |

### Child assessments (standard scores; BPI: higher = more problems)

| variable | White mean | (sd) | N | Black mean | (sd) | N |
|---|---|---|---|---|---|---|
| PIAT Math 5-6 | 104.112 | (13.424) | 3,167 | 95.540 | (13.540) | 2,000 |
| PIAT Math 7-8 | 105.351 | (12.144) | 3,251 | 96.148 | (12.565) | 2,116 |
| PIAT Math 9-10 | 106.959 | (14.232) | 3,207 | 95.873 | (14.324) | 2,212 |
| PIAT Math 11-12 | 106.823 | (13.763) | 3,061 | 95.599 | (13.596) | 2,193 |
| PIAT Math 13-14 | 105.412 | (14.189) | 2,371 | 93.943 | (13.094) | 1,702 |
| PIAT Read. Recog. 5-6 | 108.063 | (13.463) | 3,115 | 104.572 | (13.503) | 1,965 |
| PIAT Read. Recog. 7-8 | 108.030 | (12.779) | 3,254 | 101.223 | (13.100) | 2,116 |
| PIAT Read. Recog. 9-10 | 108.256 | (14.368) | 3,201 | 99.164 | (15.187) | 2,215 |
| PIAT Read. Recog. 11-12 | 107.253 | (14.533) | 3,065 | 97.570 | (15.238) | 2,189 |
| PIAT Read. Recog. 13-14 | 107.902 | (15.382) | 2,369 | 97.012 | (15.543) | 1,711 |
| PIAT Read. Comp. 5-6 | 111.298 | (11.870) | 1,309 | 109.569 | (10.405) | 838 |
| PIAT Read. Comp. 7-8 | 107.642 | (12.099) | 3,096 | 101.004 | (12.149) | 1,975 |
| PIAT Read. Comp. 9-10 | 104.924 | (13.119) | 3,176 | 96.169 | (13.726) | 2,162 |
| PIAT Read. Comp. 11-12 | 102.570 | (12.908) | 3,036 | 92.723 | (13.331) | 2,163 |
| PIAT Read. Comp. 13-14 | 100.816 | (12.806) | 2,353 | 90.712 | (12.369) | 1,700 |
| PPVT 5-6 | 99.410 | (18.025) | 1,409 | 81.522 | (18.027) | 939 |
| PPVT 7-8 | 98.986 | (15.738) | 947 | 80.938 | (17.133) | 731 |
| PPVT 9-10 | 102.219 | (16.696) | 2,022 | 83.432 | (18.646) | 1,501 |
| PPVT 11-12 | 102.493 | (17.472) | 1,741 | 83.595 | (18.391) | 1,252 |
| PPVT 13-14 | 97.649 | (16.957) | 251 | 82.788 | (15.576) | 306 |
| BPI total (+ = more problems) 5-6 | 102.033 | (14.907) | 3,292 | 105.266 | (15.039) | 1,973 |
| BPI total (+ = more problems) 7-8 | 103.977 | (14.777) | 3,375 | 106.775 | (15.386) | 2,109 |
| BPI total (+ = more problems) 9-10 | 104.344 | (14.715) | 3,374 | 106.760 | (15.190) | 2,217 |
| BPI total (+ = more problems) 11-12 | 104.696 | (14.857) | 3,275 | 107.129 | (15.625) | 2,228 |
| BPI total (+ = more problems) 13-14 | 105.036 | (14.593) | 2,548 | 106.425 | (15.371) | 1,742 |

### Young adults

| variable | White mean | (sd) | N | Black mean | (sd) | N |
|---|---|---|---|---|---|---|
| highest grade completed by 25 | 13.020 | (2.374) | 2,976 | 12.479 | (2.005) | 2,220 |
| ever attended college | 0.750 | (0.433) | 3,758 | 0.655 | (0.475) | 2,754 |
| attended college by 21 | 0.671 | (0.470) | 3,008 | 0.505 | (0.500) | 2,220 |
| wages, mean at 26-35 (2000 $) | 27197.596 | (20654.488) | 2,903 | 17545.348 | (15454.484) | 2,300 |
| wages, latest interview 26+ (2000 $) | 31627.749 | (27635.252) | 2,926 | 21913.052 | (22060.848) | 2,319 |
| age at latest earnings | 32.594 | (4.598) | 2,926 | 34.194 | (5.213) | 2,319 |

### Sanity check: all children of these mothers, standard scores (norm mean 100, sd 15)

| test | band | mean | sd | N |
|---|---|---|---|---|
| PIAT Math | 5-6 | 100.8 | 14.1 | 5,167 |
| PIAT Math | 7-8 | 101.7 | 13.1 | 5,367 |
| PIAT Math | 9-10 | 102.4 | 15.3 | 5,419 |
| PIAT Math | 11-12 | 102.1 | 14.8 | 5,254 |
| PIAT Math | 13-14 | 100.6 | 14.9 | 4,073 |
| PIAT Read. Recog. | 5-6 | 106.7 | 13.6 | 5,080 |
| PIAT Read. Recog. | 7-8 | 105.3 | 13.3 | 5,370 |
| PIAT Read. Recog. | 9-10 | 104.5 | 15.4 | 5,416 |
| PIAT Read. Recog. | 11-12 | 103.2 | 15.6 | 5,254 |
| PIAT Read. Recog. | 13-14 | 103.3 | 16.4 | 4,080 |
| PIAT Read. Comp. | 5-6 | 110.6 | 11.3 | 2,147 |
| PIAT Read. Comp. | 7-8 | 105.1 | 12.5 | 5,071 |
| PIAT Read. Comp. | 9-10 | 101.4 | 14.0 | 5,338 |
| PIAT Read. Comp. | 11-12 | 98.5 | 14.0 | 5,199 |
| PIAT Read. Comp. | 13-14 | 96.6 | 13.6 | 4,053 |
| PPVT | 5-6 | 92.3 | 20.0 | 2,348 |
| PPVT | 7-8 | 91.1 | 18.6 | 1,678 |
| PPVT | 9-10 | 94.2 | 19.9 | 3,523 |
| PPVT | 11-12 | 94.6 | 20.1 | 2,993 |
| PPVT | 13-14 | 89.5 | 17.8 | 557 |
| BPI total (+ = more problems) | 5-6 | 103.2 | 15.0 | 5,265 |
| BPI total (+ = more problems) | 7-8 | 105.1 | 15.1 | 5,484 |
| BPI total (+ = more problems) | 9-10 | 105.3 | 15.0 | 5,591 |
| BPI total (+ = more problems) | 11-12 | 105.7 | 15.2 | 5,503 |
| BPI total (+ = more problems) | 13-14 | 105.6 | 14.9 | 4,290 |

Notes. PIAT and BPI standard scores sit near the norms (means 97-111, sd 11-16). PIAT Reading Comprehension at 5-6 is selected: it is given only to children whose Reading Recognition raw score is high enough, hence the small N and high mean. PPVT-R standard scores are well below the norm (about 92 overall, 81-84 for children of Black mothers, sd 18-20), as is known for the NLSY79 children; PPVT is mostly given at 3-5 and 10-11 in later rounds, hence the thin 7-8 and 13-14 cells. Children born before April 1978 have no exposure measures (the weekly array starts in January 1978). `college_any` counts attendance without a completed year (enrolled in year 1 of college, or a date first attended), so it exceeds the share with 13+ completed grades.


## Descriptive OLS: test scores on the mother's weeks employed in the first year

Each column one OLS regression (outcome in the header: standard score at that age band), by race of the mother; unweighted; s.e. clustered by mother; *** p<0.01, ** p<0.05, * p<0.1. Regressor of interest: weeks employed in weeks 0-51 after the birth divided by 13 (one unit = one quarter of the year at work). Controls: AFQT, education, age at birth, married at birth, log family income at 0-5, child sex, birth-year fixed effects. BPI: a positive coefficient means more behaviour problems. **Descriptive (selection), not causal.**

**White mothers**

| | PIAT Math 5-6 | PIAT Read. Recog. 5-6 | PIAT Read. Comp. 5-6 | PPVT 5-6 | BPI total (+ = more problems) 5-6 | PIAT Math 7-8 | PIAT Read. Recog. 7-8 | PIAT Read. Comp. 7-8 | PPVT 7-8 | BPI total (+ = more problems) 7-8 |
|---|---|---|---|---|---|---|---|---|---|---|
| Mother's weeks employed, months 0-12 (per 13 weeks) | 0.048 | -0.131 | -0.054 | 0.208 | 0.256 | 0.123 | -0.067 | -0.174 | -0.549 | 0.259 |
| | (0.154) p=0.753 | (0.153) p=0.392 | (0.208) p=0.794 | (0.301) p=0.490 | (0.185) p=0.167 | (0.138) p=0.371 | (0.148) p=0.652 | (0.147) p=0.236 | (0.342) p=0.109 | (0.185) p=0.161 |
| Mother's AFQT (per 10 pctile) | 1.059*** | 1.118*** | 0.799*** | 1.428*** | -0.128 | 1.058*** | 0.992*** | 0.948*** | 1.547*** | 0.136 |
| | (0.124) p=<0.001 | (0.120) p=<0.001 | (0.149) p=<0.001 | (0.214) p=<0.001 | (0.141) p=0.363 | (0.115) p=<0.001 | (0.122) p=<0.001 | (0.117) p=<0.001 | (0.257) p=<0.001 | (0.142) p=0.339 |
| Mother HS (vs < HS) | 1.527 | 2.634* | -2.016 | 3.724 | -4.126** | 1.567 | 4.578*** | 4.069*** | 3.516 | -4.356** |
| | (1.338) p=0.254 | (1.421) p=0.064 | (1.603) p=0.209 | (2.296) p=0.105 | (1.779) p=0.020 | (1.306) p=0.230 | (1.464) p=0.002 | (1.330) p=0.002 | (2.897) p=0.225 | (1.706) p=0.011 |
| Mother College (vs < HS) | 3.774** | 4.805*** | -0.625 | 5.955** | -4.838** | 4.712*** | 6.164*** | 5.165*** | 5.180 | -5.778*** |
| | (1.513) p=0.013 | (1.610) p=0.003 | (1.858) p=0.737 | (2.749) p=0.030 | (1.943) p=0.013 | (1.470) p=0.001 | (1.608) p=<0.001 | (1.505) p=<0.001 | (3.297) p=0.116 | (1.858) p=0.002 |
| Mother's age at birth | 0.066 | -0.216* | 0.009 | -0.109 | -0.174 | 0.068 | -0.056 | 0.048 | 0.238 | -0.197 |
| | (0.127) p=0.606 | (0.124) p=0.081 | (0.157) p=0.955 | (0.255) p=0.669 | (0.150) p=0.245 | (0.115) p=0.555 | (0.126) p=0.660 | (0.123) p=0.697 | (0.276) p=0.388 | (0.152) p=0.195 |
| Married at birth | -0.236 | 0.769 | -0.117 | 1.768 | -2.663** | 1.412* | 0.391 | 1.513* | 1.346 | -2.402** |
| | (0.888) p=0.791 | (0.847) p=0.364 | (1.002) p=0.907 | (1.694) p=0.297 | (1.076) p=0.013 | (0.739) p=0.056 | (0.860) p=0.649 | (0.827) p=0.067 | (1.763) p=0.445 | (1.072) p=0.025 |
| Log family income, ages 0-5 | 1.869*** | 1.933*** | 0.784 | 0.960 | -2.740*** | 1.105*** | 2.052*** | 1.338*** | 2.507** | -2.976*** |
| | (0.412) p=<0.001 | (0.438) p=<0.001 | (0.544) p=0.149 | (0.816) p=0.239 | (0.505) p=<0.001 | (0.392) p=0.005 | (0.430) p=<0.001 | (0.428) p=0.002 | (1.039) p=0.016 | (0.501) p=<0.001 |
| Child female | 1.218*** | 2.820*** | 1.821*** | 0.425 | -2.049*** | -0.197 | 3.121*** | 2.553*** | 0.898 | -2.427*** |
| | (0.447) p=0.006 | (0.444) p=<0.001 | (0.640) p=0.004 | (0.966) p=0.660 | (0.511) p=<0.001 | (0.413) p=0.634 | (0.442) p=<0.001 | (0.430) p=<0.001 | (1.040) p=0.388 | (0.512) p=<0.001 |
| Birth-year FE | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes |
| Mean of outcome | 104.1 | 107.9 | 111.1 | 99.2 | 102.3 | 105.3 | 107.9 | 107.5 | 99.4 | 104.0 |
| N children | 2,931 | 2,881 | 1,204 | 1,288 | 3,007 | 2,945 | 2,947 | 2,805 | 832 | 3,024 |
| N mothers (clusters) | 1,520 | 1,511 | 914 | 972 | 1,557 | 1,507 | 1,508 | 1,472 | 689 | 1,558 |

**Black mothers**

| | PIAT Math 5-6 | PIAT Read. Recog. 5-6 | PIAT Read. Comp. 5-6 | PPVT 5-6 | BPI total (+ = more problems) 5-6 | PIAT Math 7-8 | PIAT Read. Recog. 7-8 | PIAT Read. Comp. 7-8 | PPVT 7-8 | BPI total (+ = more problems) 7-8 |
|---|---|---|---|---|---|---|---|---|---|---|
| Mother's weeks employed, months 0-12 (per 13 weeks) | 0.598** | 0.488** | 0.270 | 0.214 | 0.259 | 0.436** | 0.617*** | 0.208 | 0.381 | -0.106 |
| | (0.232) p=0.010 | (0.230) p=0.034 | (0.232) p=0.244 | (0.409) p=0.601 | (0.271) p=0.339 | (0.220) p=0.048 | (0.208) p=0.003 | (0.198) p=0.294 | (0.577) p=0.509 | (0.280) p=0.706 |
| Mother's AFQT (per 10 pctile) | 1.093*** | 1.407*** | 1.036*** | 2.491*** | -0.498* | 1.509*** | 1.658*** | 1.580*** | 2.628*** | -0.311 |
| | (0.222) p=<0.001 | (0.202) p=<0.001 | (0.212) p=<0.001 | (0.383) p=<0.001 | (0.270) p=0.066 | (0.208) p=<0.001 | (0.203) p=<0.001 | (0.193) p=<0.001 | (0.431) p=<0.001 | (0.256) p=0.223 |
| Mother HS (vs < HS) | 2.711** | 3.528*** | 2.543** | 8.305*** | -5.453*** | 3.510*** | 3.679*** | 3.561*** | 6.739*** | -4.043** |
| | (1.169) p=0.020 | (1.082) p=0.001 | (1.269) p=0.045 | (2.229) p=<0.001 | (1.581) p=<0.001 | (1.105) p=0.001 | (1.161) p=0.002 | (1.090) p=0.001 | (1.844) p=<0.001 | (1.791) p=0.024 |
| Mother College (vs < HS) | 5.708*** | 6.549*** | 4.078** | 12.283*** | -5.496** | 5.507*** | 5.709*** | 4.143*** | 11.005*** | -4.865** |
| | (1.575) p=<0.001 | (1.469) p=<0.001 | (1.681) p=0.015 | (2.812) p=<0.001 | (2.157) p=0.011 | (1.501) p=<0.001 | (1.489) p=<0.001 | (1.463) p=0.005 | (2.654) p=<0.001 | (2.215) p=0.028 |
| Mother's age at birth | 0.359** | 0.387** | 0.404** | 0.431 | 0.259 | 0.137 | 0.103 | 0.295** | 0.913*** | 0.510** |
| | (0.159) p=0.024 | (0.163) p=0.018 | (0.170) p=0.017 | (0.299) p=0.150 | (0.206) p=0.207 | (0.151) p=0.364 | (0.160) p=0.520 | (0.145) p=0.041 | (0.348) p=0.009 | (0.207) p=0.014 |
| Married at birth | -0.247 | -0.398 | 0.553 | -0.069 | -0.018 | -0.946 | -0.596 | -0.059 | -3.223** | 1.075 |
| | (0.728) p=0.735 | (0.732) p=0.587 | (0.811) p=0.495 | (1.365) p=0.959 | (0.959) p=0.985 | (0.711) p=0.184 | (0.687) p=0.386 | (0.635) p=0.926 | (1.534) p=0.036 | (0.971) p=0.269 |
| Log family income, ages 0-5 | 0.491 | 1.567*** | 0.169 | 0.296 | -1.863*** | 1.039* | 1.582*** | 1.367*** | 2.615** | -2.677*** |
| | (0.570) p=0.389 | (0.548) p=0.004 | (0.538) p=0.753 | (1.084) p=0.785 | (0.664) p=0.005 | (0.553) p=0.060 | (0.504) p=0.002 | (0.524) p=0.009 | (1.095) p=0.017 | (0.639) p=<0.001 |
| Child female | 2.415*** | 2.567*** | 1.028 | 4.918*** | -2.798*** | 0.967* | 3.590*** | 2.671*** | -2.890** | -2.836*** |
| | (0.615) p=<0.001 | (0.593) p=<0.001 | (0.668) p=0.124 | (1.142) p=<0.001 | (0.691) p=<0.001 | (0.538) p=0.072 | (0.564) p=<0.001 | (0.539) p=<0.001 | (1.286) p=0.025 | (0.721) p=<0.001 |
| Birth-year FE | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes |
| Mean of outcome | 95.4 | 104.3 | 109.5 | 81.2 | 105.4 | 96.1 | 101.2 | 101.0 | 81.1 | 106.7 |
| N children | 1,818 | 1,784 | 759 | 839 | 1,784 | 1,861 | 1,859 | 1,734 | 609 | 1,832 |
| N mothers (clusters) | 929 | 919 | 565 | 617 | 933 | 927 | 924 | 901 | 482 | 932 |
