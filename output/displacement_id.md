# Identifying the father's displacement -> children link: closures, siblings, pre-trends, severity

Built by `22.DisplacementID.py` (2026-10-17) on top of `19.FatherDisplacement.py` (same displacement measure, children, father figures, controls and outcomes). Unweighted PSID SRC + SEO, Black and White (child's race). Cells: coefficient, stars, (s.e. clustered by 1968 family; p-value); *** p<0.01, ** p<0.05, * p<0.1. Every design below is a comparison of children whose father figure was displaced with children whose father figure was not (or not yet, or not during their childhood). None of them is an experiment; each removes one source of bias and keeps others, as noted under each table.

## 1. Closures only (closure-first definition)

Treated = the father figure's first displacement during the child's childhood (CDS: before the test) is a plant closure / move and falls in the age band; children whose first displacement was a layoff / firing are dropped; controls = children never displaced (closure or layoff) at 0-17 (CDS: before the test), with a pseudo event year at the treated's median exposure age; both need a father figure who worked in the year(s) before the (pseudo) event. Controls: log family income over the 3 years before the (pseudo) event, parental education (5 groups), female, birth-year FE (+ CDS-wave FE; + Black in pooled rows). Closures are the definition least driven by the worker's own performance (Page, Stevens and Lindo 2009; Oreopoulos, Page and Stevens 2008), but who works at a plant that closes is not random either (industry, region, firm quality).

### 1a. Adult outcomes

| | Log lifetime earnings | Log lifetime family income | Earnings rank (0-100) | Family income rank (0-100) | Years of schooling |
|---|---|---|---|---|---|
| **Black, first closure at ages 0-5 (controls' pseudo age 2)** | | | | | |
| Father figure displaced | 0.021 (0.117; p=0.855) | -0.037 (0.093; p=0.690) | -0.011 (2.788; p=0.997) | -0.114 (2.732; p=0.967) | 0.186 (0.185; p=0.314) |
| Mean of outcome | 9.771 | 10.333 | 45.728 | 40.784 | 13.368 |
| N (children) | 688 | 695 | 688 | 695 | 1,307 |
|   of which father figure displaced | 92 | 93 | 92 | 93 | 154 |
| Clusters (fam68) | 330 | 331 | 330 | 331 | 482 |
| **White, first closure at ages 0-5 (controls' pseudo age 2)** | | | | | |
| Father figure displaced | -0.043 (0.073; p=0.556) | -0.043 (0.056; p=0.436) | -1.760 (2.312; p=0.447) | -2.525 (2.249; p=0.261) | -0.160 (0.146; p=0.275) |
| Mean of outcome | 10.207 | 10.966 | 60.072 | 64.662 | 14.335 |
| N (children) | 1,727 | 1,743 | 1,727 | 1,743 | 2,698 |
|   of which father figure displaced | 171 | 175 | 171 | 175 | 280 |
| Clusters (fam68) | 747 | 754 | 747 | 754 | 998 |
| **Pooled, first closure at ages 0-5 (controls' pseudo age 2)** | | | | | |
| Father figure displaced | -0.023 (0.062; p=0.717) | -0.040 (0.048; p=0.412) | -1.276 (1.803; p=0.479) | -1.722 (1.743; p=0.323) | -0.024 (0.116; p=0.836) |
| Mean of outcome | 10.083 | 10.786 | 55.986 | 57.855 | 14.020 |
| N (children) | 2,415 | 2,438 | 2,415 | 2,438 | 4,005 |
|   of which father figure displaced | 263 | 268 | 263 | 268 | 434 |
| Clusters (fam68) | 1,074 | 1,082 | 1,074 | 1,082 | 1,476 |
| **Black, first closure at ages 6-11 (controls' pseudo age 8)** | | | | | |
| Father figure displaced | 0.192 (0.122; p=0.114) | 0.126 (0.101; p=0.212) | 1.061 (3.938; p=0.787) | 1.174 (3.950; p=0.766) | 0.182 (0.231; p=0.432) |
| Mean of outcome | 9.741 | 10.331 | 47.306 | 41.752 | 13.335 |
| N (children) | 826 | 835 | 826 | 835 | 1,560 |
|   of which father figure displaced | 59 | 60 | 59 | 60 | 115 |
| Clusters (fam68) | 349 | 354 | 349 | 354 | 518 |
| **White, first closure at ages 6-11 (controls' pseudo age 8)** | | | | | |
| Father figure displaced | -0.103 (0.093; p=0.271) | -0.002 (0.063; p=0.974) | -5.379* (2.770; p=0.052) | -0.916 (2.492; p=0.713) | -0.525*** (0.158; p=<0.001) |
| Mean of outcome | 10.210 | 10.982 | 61.223 | 66.094 | 14.171 |
| N (children) | 2,078 | 2,095 | 2,078 | 2,095 | 3,149 |
|   of which father figure displaced | 129 | 130 | 129 | 130 | 232 |
| Clusters (fam68) | 840 | 845 | 840 | 845 | 1,062 |
| **Pooled, first closure at ages 6-11 (controls' pseudo age 8)** | | | | | |
| Father figure displaced | -0.008 (0.076; p=0.913) | 0.038 (0.053; p=0.471) | -3.070 (2.297; p=0.181) | -0.089 (2.081; p=0.966) | -0.261* (0.134; p=0.051) |
| Mean of outcome | 10.077 | 10.796 | 57.264 | 59.157 | 13.894 |
| N (children) | 2,904 | 2,930 | 2,904 | 2,930 | 4,709 |
|   of which father figure displaced | 188 | 190 | 188 | 190 | 347 |
| Clusters (fam68) | 1,187 | 1,197 | 1,187 | 1,197 | 1,577 |
| **Black, first closure at ages 12-17 (controls' pseudo age 14)** | | | | | |
| Father figure displaced | -0.056 (0.122; p=0.645) | -0.024 (0.078; p=0.758) | -3.253 (3.034; p=0.284) | -2.351 (2.673; p=0.379) | -0.307 (0.198; p=0.122) |
| Mean of outcome | 9.695 | 10.303 | 46.620 | 40.644 | 13.083 |
| N (children) | 1,079 | 1,094 | 1,079 | 1,094 | 1,969 |
|   of which father figure displaced | 69 | 70 | 69 | 70 | 137 |
| Clusters (fam68) | 398 | 402 | 398 | 402 | 570 |
| **White, first closure at ages 12-17 (controls' pseudo age 14)** | | | | | |
| Father figure displaced | -0.123 (0.092; p=0.181) | -0.027 (0.046; p=0.559) | -1.698 (2.079; p=0.414) | -1.701 (1.846; p=0.357) | -0.314** (0.148; p=0.034) |
| Mean of outcome | 10.154 | 10.963 | 60.831 | 65.796 | 13.975 |
| N (children) | 2,750 | 2,767 | 2,750 | 2,767 | 4,103 |
|   of which father figure displaced | 180 | 181 | 180 | 181 | 276 |
| Clusters (fam68) | 967 | 970 | 967 | 970 | 1,195 |
| **Pooled, first closure at ages 12-17 (controls' pseudo age 14)** | | | | | |
| Father figure displaced | -0.090 (0.074; p=0.223) | -0.020 (0.039; p=0.612) | -1.634 (1.750; p=0.350) | -1.548 (1.512; p=0.306) | -0.293** (0.119; p=0.014) |
| Mean of outcome | 10.024 | 10.776 | 56.827 | 58.669 | 13.686 |
| N (children) | 3,829 | 3,861 | 3,829 | 3,861 | 6,072 |
|   of which father figure displaced | 249 | 251 | 249 | 251 | 413 |
| Clusters (fam68) | 1,362 | 1,369 | 1,362 | 1,369 | 1,756 |
| **Black, first closure at ages 0-17 (controls' pseudo age 7)** | | | | | |
| Father figure displaced | 0.085 (0.078; p=0.278) | 0.008 (0.063; p=0.893) | -0.531 (2.123; p=0.802) | -1.148 (2.126; p=0.589) | 0.025 (0.135; p=0.852) |
| Mean of outcome | 9.730 | 10.317 | 46.425 | 40.939 | 13.296 |
| N (children) | 961 | 971 | 961 | 971 | 1,786 |
|   of which father figure displaced | 220 | 223 | 220 | 223 | 406 |
| Clusters (fam68) | 388 | 390 | 388 | 390 | 541 |
| **White, first closure at ages 0-17 (controls' pseudo age 7)** | | | | | |
| Father figure displaced | -0.078 (0.053; p=0.139) | -0.030 (0.038; p=0.434) | -3.297** (1.612; p=0.041) | -1.880 (1.522; p=0.217) | -0.398*** (0.109; p=<0.001) |
| Mean of outcome | 10.176 | 10.960 | 60.332 | 65.011 | 14.125 |
| N (children) | 2,346 | 2,367 | 2,346 | 2,367 | 3,601 |
|   of which father figure displaced | 480 | 486 | 480 | 486 | 788 |
| Clusters (fam68) | 899 | 906 | 899 | 906 | 1,129 |
| **Pooled, first closure at ages 0-17 (controls' pseudo age 7)** | | | | | |
| Father figure displaced | -0.028 (0.044; p=0.530) | -0.014 (0.032; p=0.661) | -2.315* (1.318; p=0.079) | -1.467 (1.236; p=0.236) | -0.240*** (0.087; p=0.006) |
| Mean of outcome | 10.047 | 10.773 | 56.291 | 58.009 | 13.850 |
| N (children) | 3,307 | 3,338 | 3,307 | 3,338 | 5,387 |
|   of which father figure displaced | 700 | 709 | 700 | 709 | 1,194 |
| Clusters (fam68) | 1,284 | 1,293 | 1,284 | 1,293 | 1,665 |
| Fixed effects | birth year | birth year | birth year | birth year | birth year |
| Other controls | log pre-event family income, parental education, female | log pre-event family income, parental education, female | log pre-event family income, parental education, female | log pre-event family income, parental education, female | log pre-event family income, parental education, female |

### 1b. CDS test scores and behaviour

| | WJ Letter-Word | WJ Applied Problems | WJ Passage Comp. | BPI (z, higher = worse) |
|---|---|---|---|---|
| **Black, first closure at ages 0-5 (controls' pseudo age 2)** | | | | |
| Father figure displaced | -0.230 (1.799; p=0.898) | -2.182 (1.898; p=0.250) | 0.208 (1.880; p=0.912) | 0.008 (0.115; p=0.947) |
| Mean of outcome | 100.219 | 96.164 | 99.129 | -0.155 |
| N (children x tests) | 1,144 | 1,138 | 957 | 1,686 |
|   of which father figure displaced | 105 | 103 | 98 | 157 |
| Clusters (fam68) | 332 | 330 | 310 | 402 |
| **White, first closure at ages 0-5 (controls' pseudo age 2)** | | | | |
| Father figure displaced | 0.243 (1.628; p=0.881) | 0.722 (1.579; p=0.648) | 0.905 (1.466; p=0.537) | -0.031 (0.083; p=0.713) |
| Mean of outcome | 108.064 | 108.949 | 107.364 | -0.015 |
| N (children x tests) | 2,717 | 2,707 | 2,305 | 4,444 |
|   of which father figure displaced | 170 | 170 | 154 | 253 |
| Clusters (fam68) | 650 | 649 | 617 | 817 |
| **Pooled, first closure at ages 0-5 (controls' pseudo age 2)** | | | | |
| Father figure displaced | 0.112 (1.201; p=0.926) | 0.016 (1.222; p=0.989) | 0.783 (1.109; p=0.480) | -0.030 (0.068; p=0.658) |
| Mean of outcome | 105.740 | 105.165 | 104.948 | -0.053 |
| N (children x tests) | 3,861 | 3,845 | 3,262 | 6,130 |
|   of which father figure displaced | 275 | 273 | 252 | 410 |
| Clusters (fam68) | 969 | 967 | 917 | 1,191 |
| **Black, first closure at ages 6-11 (controls' pseudo age 8)** | | | | |
| Father figure displaced | 2.136 (4.189; p=0.610) | 2.747 (2.674; p=0.304) | 4.854 (3.009; p=0.107) | -0.103 (0.169; p=0.540) |
| Mean of outcome | 99.244 | 97.239 | 97.716 | -0.145 |
| N (children x tests) | 623 | 620 | 620 | 880 |
|   of which father figure displaced | 31 | 30 | 30 | 52 |
| Clusters (fam68) | 259 | 258 | 258 | 312 |
| **White, first closure at ages 6-11 (controls' pseudo age 8)** | | | | |
| Father figure displaced | -0.436 (2.507; p=0.862) | -1.837 (2.346; p=0.434) | 0.054 (1.847; p=0.977) | -0.018 (0.114; p=0.871) |
| Mean of outcome | 108.901 | 110.389 | 106.461 | -0.038 |
| N (children x tests) | 1,599 | 1,592 | 1,595 | 2,460 |
|   of which father figure displaced | 67 | 67 | 67 | 94 |
| Clusters (fam68) | 526 | 524 | 524 | 680 |
| **Pooled, first closure at ages 6-11 (controls' pseudo age 8)** | | | | |
| Father figure displaced | 0.320 (2.151; p=0.882) | -0.378 (1.879; p=0.841) | 1.549 (1.636; p=0.344) | -0.049 (0.094; p=0.600) |
| Mean of outcome | 106.194 | 106.703 | 104.014 | -0.066 |
| N (children x tests) | 2,222 | 2,212 | 2,215 | 3,340 |
|   of which father figure displaced | 98 | 97 | 97 | 146 |
| Clusters (fam68) | 783 | 780 | 780 | 984 |
| **Black, first closure at ages 12-17 (controls' pseudo age 13)** | | | | |
| Father figure displaced | -6.949 (5.289; p=0.189) | -17.094** (8.164; p=0.036) | -0.974 (6.539; p=0.882) | 0.096 (0.296; p=0.745) |
| Mean of outcome | 98.101 | 95.051 | 94.619 | -0.130 |
| N (children x tests) | 237 | 237 | 236 | 336 |
|   of which father figure displaced | 7 | 7 | 7 | 15 |
| Clusters (fam68) | 158 | 158 | 158 | 203 |
| **White, first closure at ages 12-17 (controls' pseudo age 13)** | | | | |
| Father figure displaced | 2.384 (4.407; p=0.588) | -0.022 (2.789; p=0.994) | 8.666 (6.232; p=0.164) | -0.378*** (0.103; p=<0.001) |
| Mean of outcome | 108.158 | 108.220 | 104.084 | -0.051 |
| N (children x tests) | 558 | 554 | 557 | 833 |
|   of which father figure displaced | 14 | 14 | 14 | 16 |
| Clusters (fam68) | 342 | 341 | 341 | 464 |
| **Pooled, first closure at ages 12-17 (controls' pseudo age 13)** | | | | |
| Father figure displaced | -0.342 (3.575; p=0.924) | -5.581 (4.206; p=0.185) | 6.414 (4.914; p=0.192) | -0.152 (0.196; p=0.437) |
| Mean of outcome | 105.160 | 104.274 | 101.267 | -0.074 |
| N (children x tests) | 795 | 791 | 793 | 1,169 |
|   of which father figure displaced | 21 | 21 | 21 | 31 |
| Clusters (fam68) | 500 | 499 | 499 | 664 |
| **Black, first closure at ages 0-17 (controls' pseudo age 4)** | | | | |
| Father figure displaced | -0.336 (1.771; p=0.850) | -2.300 (1.922; p=0.231) | 0.953 (1.670; p=0.568) | 0.036 (0.106; p=0.732) |
| Mean of outcome | 100.195 | 96.431 | 99.361 | -0.192 |
| N (children x tests) | 1,069 | 1,063 | 973 | 1,531 |
|   of which father figure displaced | 143 | 140 | 135 | 224 |
| Clusters (fam68) | 324 | 324 | 318 | 386 |
| **White, first closure at ages 0-17 (controls' pseudo age 4)** | | | | |
| Father figure displaced | -0.299 (1.412; p=0.832) | -0.213 (1.320; p=0.872) | 0.951 (1.227; p=0.438) | -0.025 (0.073; p=0.728) |
| Mean of outcome | 108.613 | 109.290 | 107.447 | -0.040 |
| N (children x tests) | 2,536 | 2,528 | 2,317 | 4,005 |
|   of which father figure displaced | 251 | 251 | 235 | 363 |
| Clusters (fam68) | 617 | 616 | 600 | 788 |
| **Pooled, first closure at ages 0-17 (controls' pseudo age 4)** | | | | |
| Father figure displaced | -0.215 (1.090; p=0.843) | -0.607 (1.092; p=0.578) | 1.134 (0.968; p=0.241) | -0.014 (0.060; p=0.818) |
| Mean of outcome | 106.117 | 105.483 | 105.055 | -0.082 |
| N (children x tests) | 3,605 | 3,591 | 3,290 | 5,536 |
|   of which father figure displaced | 394 | 391 | 370 | 587 |
| Clusters (fam68) | 933 | 932 | 911 | 1,157 |
| Fixed effects | birth year, CDS wave | birth year, CDS wave | birth year, CDS wave | birth year, CDS wave |
| Other controls | log pre-event family income, parental education, female | log pre-event family income, parental education, female | log pre-event family income, parental education, female | log pre-event family income, parental education, female |

## 2. Sibling design (mother fixed effects)

Family = mother (CAH mother; for children born 1951-67, the wife / female head of the unit where the child is first seen as a child). Father figure at birth (fb) = the earliest father figure observed; D = his first displacement, closure or layoff (observed from 1967; earlier ones are unobserved, so for the 1951-67 cohorts D may be a second displacement); a = D - birth year. Categories: exposed = 0 <= a <= 17 and living with fb in D; older sibling = a >= 18 (the reference group); later-born = a < 0 (born after the displacement; whatever happens later); never = fb never displaced (a half-sibling under mother FE; own dummy, shown). Exposed and older siblings must have lived with fb in >= 80% of their observed childhood years before D, so that both groups grew up with the same father figure up to the event (only children living with a father figure can be 'exposed'). Children whose own childhood exposure comes from another father figure, or precedes fb's first displacement, are dropped. OLS with mother FE (absorbed, singletons dropped), birth-year FE, female, birth order (2, 3+). The comparison removes what siblings share (the mother, the household's permanent traits, the father's type when he is common). It does not remove differences tied to birth order and cohort within the family (age at the event and the older / later-born status are functions of birth year given D): older siblings (born 18+ years before the father's first displacement) are the mother's earliest births, and every younger group (exposed and later-born alike) has more schooling than they do, which points to a within-family birth-order / cohort gradient rather than an effect of displacement. The exposed vs later-born contrast (both younger) is the less contaminated one, but later-born children grow up with the father's permanent earnings loss, so it identifies the effect of experiencing the job loss during childhood relative to being born after it, not the level effect. An older sibling can also be affected through the family (e.g. less help with college).

### 2a. Mother FE

| | Log lifetime earnings | Log lifetime family income | Earnings rank (0-100) | Family income rank (0-100) | Years of schooling |
|---|---|---|---|---|---|
| **Black: exposed at 0-17 vs older siblings** | | | | | |
| Exposed at 0-17 (father's first displacement) | 0.071 (0.175; p=0.684) | 0.046 (0.114; p=0.688) | 3.063 (3.718; p=0.410) | 1.459 (3.214; p=0.650) | 0.298* (0.172; p=0.083) |
| Later-born sibling (born after the displacement) | -0.190 (0.201; p=0.346) | -0.131 (0.137; p=0.338) | -3.592 (4.431; p=0.417) | -3.253 (4.133; p=0.431) | 0.285 (0.199; p=0.153) |
| Father figure never displaced (half-sibling) | -0.251 (0.171; p=0.143) | -0.039 (0.118; p=0.742) | -5.695 (3.615; p=0.115) | -0.327 (3.621; p=0.928) | -0.039 (0.179; p=0.829) |
| Difference: Exposed at 0-17 (father's first displacement) minus Later-born sibling (born after the displacement) | 0.261** (0.125; p=0.037) | 0.177** (0.078; p=0.023) | 6.656** (2.862; p=0.020) | 4.712* (2.625; p=0.073) | 0.013 (0.138; p=0.927) |
| Mean of outcome | 9.508 | 10.180 | 41.436 | 36.100 | 12.958 |
| N (children) | 2,368 | 2,436 | 2,368 | 2,436 | 4,712 |
|   of which exposed at 0-17 (father's first displacement) | 577 | 600 | 577 | 600 | 1,143 |
|   of which later-born sibling (born after the displacement) | 218 | 224 | 218 | 224 | 595 |
| Families (FE groups, 2+ children) | 785 | 805 | 785 | 805 | 1,495 |
| Families with an exposed and an older sibling (a >= 18) | 54 | 56 | 54 | 56 | 112 |
| Families with an exposed and a later-born sibling | 74 | 77 | 74 | 77 | 170 |
| Families with an exposed and a never-displaced (half-)sibling | 12 | 15 | 12 | 15 | 33 |
| Families with siblings exposed in different age bands | 99 | 100 | 99 | 100 | 190 |
| Clusters (fam68) | 482 | 487 | 482 | 487 | 689 |
| **Black: by age at the displacement** | | | | | |
| Exposed at 0-5 | -0.106 (0.196; p=0.590) | 0.027 (0.137; p=0.841) | -2.025 (4.777; p=0.672) | 0.236 (4.279; p=0.956) | 0.412* (0.210; p=0.050) |
| Exposed at 6-11 | 0.042 (0.194; p=0.831) | 0.206 (0.136; p=0.129) | 4.365 (4.639; p=0.347) | 5.963 (4.100; p=0.146) | 0.487** (0.213; p=0.022) |
| Exposed at 12-17 | 0.110 (0.184; p=0.552) | 0.010 (0.121; p=0.937) | 3.664 (3.816; p=0.337) | 0.564 (3.327; p=0.865) | 0.218 (0.188; p=0.246) |
| Later-born sibling (born after the displacement) | -0.334 (0.216; p=0.122) | -0.128 (0.152; p=0.399) | -7.503 (5.188; p=0.148) | -3.719 (4.762; p=0.435) | 0.391* (0.221; p=0.077) |
| Difference: Exposed at 0-5 minus Exposed at 12-17 | -0.215 (0.153; p=0.159) | 0.018 (0.108; p=0.868) | -5.689 (3.820; p=0.136) | -0.329 (3.411; p=0.923) | 0.194 (0.197; p=0.325) |
| Mean of outcome | 9.508 | 10.180 | 41.436 | 36.100 | 12.958 |
| N (children) | 2,368 | 2,436 | 2,368 | 2,436 | 4,712 |
|   of which exposed at 0-5 | 233 | 242 | 233 | 242 | 464 |
|   of which exposed at 6-11 | 166 | 175 | 166 | 175 | 342 |
|   of which exposed at 12-17 | 178 | 183 | 178 | 183 | 337 |
| Families (FE groups, 2+ children) | 785 | 805 | 785 | 805 | 1,495 |
| Families with siblings exposed in different age bands | 99 | 100 | 99 | 100 | 190 |
| Clusters (fam68) | 482 | 487 | 482 | 487 | 689 |
| **Black: exposure duration** | | | | | |
| Exposed at 0-17 (father's first displacement) | 0.131 (0.202; p=0.516) | 0.066 (0.128; p=0.607) | 5.660 (4.141; p=0.172) | 3.279 (3.578; p=0.359) | 0.217 (0.205; p=0.290) |
| Exposed x years of childhood after the displacement (18 - age) | -0.011 (0.013; p=0.417) | -0.003 (0.009; p=0.696) | -0.467 (0.320; p=0.145) | -0.320 (0.288; p=0.267) | 0.013 (0.015; p=0.381) |
| Later-born sibling (born after the displacement) | -0.288 (0.225; p=0.202) | -0.162 (0.155; p=0.296) | -7.822 (5.401; p=0.148) | -6.102 (4.825; p=0.206) | 0.394* (0.225; p=0.081) |
| Mean of outcome | 9.508 | 10.180 | 41.436 | 36.100 | 12.958 |
| N (children) | 2,368 | 2,436 | 2,368 | 2,436 | 4,712 |
|   of which exposed at 0-17 (father's first displacement) | 577 | 600 | 577 | 600 | 1,143 |
|   of which later-born sibling (born after the displacement) | 218 | 224 | 218 | 224 | 595 |
| Families (FE groups, 2+ children) | 785 | 805 | 785 | 805 | 1,495 |
| Clusters (fam68) | 482 | 487 | 482 | 487 | 689 |
| **Black: later-born siblings as controls (exposed vs later-born only)** | | | | | |
| Exposed at 0-17 (father's first displacement) | 0.054 (0.154; p=0.727) | -0.001 (0.102; p=0.993) | -0.993 (3.470; p=0.775) | -1.429 (3.248; p=0.660) | 0.098 (0.151; p=0.516) |
| Mean of outcome | 9.494 | 10.146 | 38.937 | 34.012 | 12.881 |
| N (children) | 751 | 775 | 751 | 775 | 1,643 |
|   of which exposed at 0-17 (father's first displacement) | 544 | 562 | 544 | 562 | 1,071 |
| Families (FE groups, 2+ children) | 267 | 274 | 267 | 274 | 553 |
| Families with an exposed and a later-born sibling | 74 | 77 | 74 | 77 | 170 |
| Clusters (fam68) | 219 | 222 | 219 | 222 | 367 |
| **White: exposed at 0-17 vs older siblings** | | | | | |
| Exposed at 0-17 (father's first displacement) | 0.006 (0.120; p=0.960) | 0.051 (0.068; p=0.456) | 0.087 (3.010; p=0.977) | 1.882 (2.834; p=0.507) | 0.262 (0.191; p=0.171) |
| Later-born sibling (born after the displacement) | -0.051 (0.153; p=0.739) | 0.024 (0.096; p=0.800) | -2.509 (4.106; p=0.541) | 0.934 (3.927; p=0.812) | 0.073 (0.233; p=0.753) |
| Father figure never displaced (half-sibling) | 0.123 (0.226; p=0.585) | 0.129 (0.158; p=0.414) | 1.074 (6.339; p=0.865) | 4.832 (7.237; p=0.504) | -0.300 (0.309; p=0.331) |
| Difference: Exposed at 0-17 (father's first displacement) minus Later-born sibling (born after the displacement) | 0.057 (0.100; p=0.568) | 0.027 (0.068; p=0.697) | 2.597 (2.796; p=0.353) | 0.948 (2.679; p=0.723) | 0.189 (0.128; p=0.141) |
| Mean of outcome | 10.069 | 10.898 | 58.080 | 62.724 | 13.795 |
| N (children) | 3,927 | 3,983 | 3,927 | 3,983 | 6,410 |
|   of which exposed at 0-17 (father's first displacement) | 946 | 967 | 946 | 967 | 1,539 |
|   of which later-born sibling (born after the displacement) | 431 | 439 | 431 | 439 | 898 |
| Families (FE groups, 2+ children) | 1,476 | 1,491 | 1,476 | 1,491 | 2,349 |
| Families with an exposed and an older sibling (a >= 18) | 79 | 79 | 79 | 79 | 119 |
| Families with an exposed and a later-born sibling | 112 | 114 | 112 | 114 | 229 |
| Families with an exposed and a never-displaced (half-)sibling | 9 | 9 | 9 | 9 | 36 |
| Families with siblings exposed in different age bands | 169 | 171 | 169 | 171 | 259 |
| Clusters (fam68) | 966 | 973 | 966 | 973 | 1,246 |
| **White: by age at the displacement** | | | | | |
| Exposed at 0-5 | 0.235 (0.187; p=0.208) | 0.092 (0.112; p=0.414) | 5.401 (4.709; p=0.251) | 4.028 (4.695; p=0.391) | 0.495* (0.267; p=0.064) |
| Exposed at 6-11 | 0.097 (0.158; p=0.541) | 0.042 (0.092; p=0.652) | -1.334 (4.079; p=0.744) | 1.931 (3.957; p=0.625) | 0.249 (0.252; p=0.323) |
| Exposed at 12-17 | 0.004 (0.121; p=0.974) | 0.053 (0.068; p=0.433) | 0.455 (3.011; p=0.880) | 1.959 (2.824; p=0.488) | 0.257 (0.188; p=0.172) |
| Later-born sibling (born after the displacement) | 0.167 (0.215; p=0.438) | 0.061 (0.128; p=0.630) | 2.262 (5.529; p=0.682) | 2.918 (5.374; p=0.587) | 0.269 (0.295; p=0.362) |
| Difference: Exposed at 0-5 minus Exposed at 12-17 | 0.231 (0.155; p=0.136) | 0.038 (0.089; p=0.667) | 4.946 (3.729; p=0.185) | 2.068 (3.668; p=0.573) | 0.238 (0.192; p=0.215) |
| Mean of outcome | 10.069 | 10.898 | 58.080 | 62.724 | 13.795 |
| N (children) | 3,927 | 3,983 | 3,927 | 3,983 | 6,410 |
|   of which exposed at 0-5 | 355 | 364 | 355 | 364 | 625 |
|   of which exposed at 6-11 | 280 | 286 | 280 | 286 | 448 |
|   of which exposed at 12-17 | 311 | 317 | 311 | 317 | 466 |
| Families (FE groups, 2+ children) | 1,476 | 1,491 | 1,476 | 1,491 | 2,349 |
| Families with siblings exposed in different age bands | 169 | 171 | 169 | 171 | 259 |
| Clusters (fam68) | 966 | 973 | 966 | 973 | 1,246 |
| **White: exposure duration** | | | | | |
| Exposed at 0-17 (father's first displacement) | -0.059 (0.132; p=0.657) | 0.040 (0.071; p=0.570) | -0.744 (3.192; p=0.816) | 1.270 (2.950; p=0.667) | 0.188 (0.195; p=0.335) |
| Exposed x years of childhood after the displacement (18 - age) | 0.020 (0.013; p=0.131) | 0.003 (0.007; p=0.660) | 0.259 (0.319; p=0.417) | 0.192 (0.319; p=0.548) | 0.018 (0.017; p=0.306) |
| Later-born sibling (born after the displacement) | 0.212 (0.232; p=0.360) | 0.067 (0.140; p=0.634) | 0.885 (6.017; p=0.883) | 3.448 (6.011; p=0.566) | 0.272 (0.326; p=0.405) |
| Mean of outcome | 10.069 | 10.898 | 58.080 | 62.724 | 13.795 |
| N (children) | 3,927 | 3,983 | 3,927 | 3,983 | 6,410 |
|   of which exposed at 0-17 (father's first displacement) | 946 | 967 | 946 | 967 | 1,539 |
|   of which later-born sibling (born after the displacement) | 431 | 439 | 431 | 439 | 898 |
| Families (FE groups, 2+ children) | 1,476 | 1,491 | 1,476 | 1,491 | 2,349 |
| Clusters (fam68) | 966 | 973 | 966 | 973 | 1,246 |
| **White: later-born siblings as controls (exposed vs later-born only)** | | | | | |
| Exposed at 0-17 (father's first displacement) | 0.128 (0.111; p=0.247) | 0.069 (0.081; p=0.393) | 5.072 (3.165; p=0.109) | 2.883 (3.131; p=0.357) | 0.187 (0.141; p=0.184) |
| Mean of outcome | 10.003 | 10.811 | 54.568 | 58.431 | 13.598 |
| N (children) | 1,314 | 1,343 | 1,314 | 1,343 | 2,335 |
|   of which exposed at 0-17 (father's first displacement) | 890 | 911 | 890 | 911 | 1,457 |
| Families (FE groups, 2+ children) | 515 | 524 | 515 | 524 | 897 |
| Families with an exposed and a later-born sibling | 112 | 114 | 112 | 114 | 229 |
| Clusters (fam68) | 409 | 414 | 409 | 414 | 633 |
| **Pooled: exposed at 0-17 vs older siblings** | | | | | |
| Exposed at 0-17 (father's first displacement) | 0.022 (0.103; p=0.828) | 0.030 (0.064; p=0.637) | 1.075 (2.348; p=0.647) | 1.300 (2.076; p=0.531) | 0.323** (0.126; p=0.010) |
| Later-born sibling (born after the displacement) | -0.170 (0.125; p=0.173) | -0.079 (0.083; p=0.339) | -4.233 (3.028; p=0.162) | -1.804 (2.807; p=0.520) | 0.186 (0.150; p=0.213) |
| Father figure never displaced (half-sibling) | -0.213 (0.146; p=0.146) | -0.035 (0.101; p=0.729) | -4.700 (3.155; p=0.136) | 0.082 (3.213; p=0.980) | -0.095 (0.160; p=0.553) |
| Difference: Exposed at 0-17 (father's first displacement) minus Later-born sibling (born after the displacement) | 0.193** (0.078; p=0.014) | 0.109** (0.052; p=0.034) | 5.308*** (2.052; p=0.010) | 3.104 (1.898; p=0.102) | 0.137 (0.094; p=0.144) |
| Mean of outcome | 9.856 | 10.624 | 51.761 | 52.563 | 13.438 |
| N (children) | 6,310 | 6,434 | 6,310 | 6,434 | 11,141 |
|   of which exposed at 0-17 (father's first displacement) | 1,526 | 1,570 | 1,526 | 1,570 | 2,686 |
|   of which later-born sibling (born after the displacement) | 651 | 665 | 651 | 665 | 1,497 |
| Families (FE groups, 2+ children) | 2,267 | 2,302 | 2,267 | 2,302 | 3,849 |
| Families with an exposed and an older sibling (a >= 18) | 133 | 135 | 133 | 135 | 231 |
| Families with an exposed and a later-born sibling | 187 | 192 | 187 | 192 | 400 |
| Families with an exposed and a never-displaced (half-)sibling | 21 | 24 | 21 | 24 | 71 |
| Families with siblings exposed in different age bands | 268 | 271 | 268 | 271 | 449 |
| Clusters (fam68) | 1,449 | 1,461 | 1,449 | 1,461 | 1,930 |
| **Pooled: by age at the displacement** | | | | | |
| Exposed at 0-5 | 0.024 (0.135; p=0.857) | 0.032 (0.089; p=0.718) | 0.871 (3.380; p=0.797) | 1.626 (3.097; p=0.600) | 0.507*** (0.162; p=0.002) |
| Exposed at 6-11 | 0.034 (0.122; p=0.783) | 0.079 (0.080; p=0.323) | 0.392 (3.072; p=0.899) | 2.778 (2.770; p=0.316) | 0.416*** (0.160; p=0.009) |
| Exposed at 12-17 | 0.020 (0.106; p=0.849) | 0.021 (0.065; p=0.745) | 1.210 (2.368; p=0.609) | 1.006 (2.086; p=0.630) | 0.275** (0.129; p=0.033) |
| Later-born sibling (born after the displacement) | -0.167 (0.151; p=0.268) | -0.073 (0.101; p=0.467) | -4.469 (3.788; p=0.238) | -1.393 (3.519; p=0.692) | 0.343** (0.174; p=0.049) |
| Difference: Exposed at 0-5 minus Exposed at 12-17 | 0.004 (0.109; p=0.969) | 0.011 (0.069; p=0.872) | -0.339 (2.737; p=0.901) | 0.620 (2.506; p=0.805) | 0.231* (0.133; p=0.083) |
| Mean of outcome | 9.856 | 10.624 | 51.761 | 52.563 | 13.438 |
| N (children) | 6,310 | 6,434 | 6,310 | 6,434 | 11,141 |
|   of which exposed at 0-5 | 591 | 609 | 591 | 609 | 1,093 |
|   of which exposed at 6-11 | 446 | 461 | 446 | 461 | 790 |
|   of which exposed at 12-17 | 489 | 500 | 489 | 500 | 803 |
| Families (FE groups, 2+ children) | 2,267 | 2,302 | 2,267 | 2,302 | 3,849 |
| Families with siblings exposed in different age bands | 268 | 271 | 268 | 271 | 449 |
| Clusters (fam68) | 1,449 | 1,461 | 1,449 | 1,461 | 1,930 |
| **Pooled: exposure duration** | | | | | |
| Exposed at 0-17 (father's first displacement) | 0.010 (0.116; p=0.931) | 0.035 (0.068; p=0.608) | 1.596 (2.557; p=0.532) | 1.579 (2.252; p=0.483) | 0.237* (0.140; p=0.090) |
| Exposed x years of childhood after the displacement (18 - age) | 0.003 (0.009; p=0.769) | -0.001 (0.006; p=0.853) | -0.115 (0.229; p=0.615) | -0.061 (0.212; p=0.774) | 0.016 (0.011; p=0.150) |
| Later-born sibling (born after the displacement) | -0.140 (0.159; p=0.379) | -0.091 (0.105; p=0.390) | -5.499 (4.023; p=0.172) | -2.467 (3.712; p=0.506) | 0.338* (0.184; p=0.067) |
| Mean of outcome | 9.856 | 10.624 | 51.761 | 52.563 | 13.438 |
| N (children) | 6,310 | 6,434 | 6,310 | 6,434 | 11,141 |
|   of which exposed at 0-17 (father's first displacement) | 1,526 | 1,570 | 1,526 | 1,570 | 2,686 |
|   of which later-born sibling (born after the displacement) | 651 | 665 | 651 | 665 | 1,497 |
| Families (FE groups, 2+ children) | 2,267 | 2,302 | 2,267 | 2,302 | 3,849 |
| Clusters (fam68) | 1,449 | 1,461 | 1,449 | 1,461 | 1,930 |
| **Pooled: later-born siblings as controls (exposed vs later-born only)** | | | | | |
| Exposed at 0-17 (father's first displacement) | 0.151* (0.090; p=0.094) | 0.054 (0.061; p=0.380) | 4.237* (2.392; p=0.077) | 1.559 (2.242; p=0.487) | 0.153 (0.105; p=0.143) |
| Mean of outcome | 9.817 | 10.567 | 48.843 | 49.464 | 13.299 |
| N (children) | 2,070 | 2,123 | 2,070 | 2,123 | 3,983 |
|   of which exposed at 0-17 (father's first displacement) | 1,437 | 1,476 | 1,437 | 1,476 | 2,531 |
| Families (FE groups, 2+ children) | 784 | 800 | 784 | 800 | 1,452 |
| Families with an exposed and a later-born sibling | 187 | 192 | 187 | 192 | 400 |
| Clusters (fam68) | 630 | 638 | 630 | 638 | 999 |
| Fixed effects | mother fe, birth year | mother fe, birth year | mother fe, birth year | mother fe, birth year | mother fe, birth year |
| Other controls | female, birth order (2, 3+), never-displaced dummy; Black in pooled rows | female, birth order (2, 3+), never-displaced dummy; Black in pooled rows | female, birth order (2, 3+), never-displaced dummy; Black in pooled rows | female, birth order (2, 3+), never-displaced dummy; Black in pooled rows | female, birth order (2, 3+), never-displaced dummy; Black in pooled rows |

### 2b. Parents FE (mother x father figure at birth)

| | Log lifetime earnings | Log lifetime family income | Earnings rank (0-100) | Family income rank (0-100) | Years of schooling |
|---|---|---|---|---|---|
| **Black: exposed at 0-17 vs older siblings** | | | | | |
| Exposed at 0-17 (father's first displacement) | 0.130 (0.209; p=0.534) | 0.127 (0.136; p=0.349) | 2.911 (4.240; p=0.492) | 4.026 (3.604; p=0.264) | 0.327 (0.209; p=0.118) |
| Later-born sibling (born after the displacement) | -0.068 (0.262; p=0.797) | -0.004 (0.174; p=0.984) | -2.345 (5.334; p=0.660) | 0.756 (4.987; p=0.880) | 0.335 (0.264; p=0.205) |
| Difference: Exposed at 0-17 (father's first displacement) minus Later-born sibling (born after the displacement) | 0.197 (0.149; p=0.187) | 0.131 (0.090; p=0.147) | 5.256 (3.223; p=0.103) | 3.270 (2.982; p=0.273) | -0.008 (0.159; p=0.961) |
| Mean of outcome | 9.521 | 10.182 | 41.932 | 36.204 | 12.943 |
| N (children) | 2,111 | 2,159 | 2,111 | 2,159 | 4,280 |
|   of which exposed at 0-17 (father's first displacement) | 551 | 570 | 551 | 570 | 1,104 |
|   of which later-born sibling (born after the displacement) | 204 | 209 | 204 | 209 | 561 |
| Families (FE groups, 2+ children) | 689 | 702 | 689 | 702 | 1,370 |
| Families with an exposed and an older sibling (a >= 18) | 51 | 53 | 51 | 53 | 106 |
| Families with an exposed and a later-born sibling | 70 | 72 | 70 | 72 | 160 |
| Families with an exposed and a never-displaced (half-)sibling | 0 | 0 | 0 | 0 | 0 |
| Families with siblings exposed in different age bands | 97 | 98 | 97 | 98 | 188 |
| Clusters (fam68) | 451 | 455 | 451 | 455 | 672 |
| **Black: by age at the displacement** | | | | | |
| Exposed at 0-5 | -0.084 (0.271; p=0.757) | 0.140 (0.181; p=0.440) | -4.479 (6.116; p=0.464) | 3.028 (5.345; p=0.571) | 0.645** (0.299; p=0.031) |
| Exposed at 6-11 | 0.070 (0.231; p=0.762) | 0.290* (0.159; p=0.069) | 2.716 (5.288; p=0.608) | 8.261* (4.603; p=0.073) | 0.585** (0.269; p=0.030) |
| Exposed at 12-17 | 0.128 (0.212; p=0.547) | 0.090 (0.138; p=0.513) | 2.435 (4.276; p=0.569) | 2.956 (3.671; p=0.421) | 0.291 (0.212; p=0.170) |
| Later-born sibling (born after the displacement) | -0.277 (0.324; p=0.392) | 0.030 (0.215; p=0.890) | -9.372 (7.053; p=0.184) | 0.377 (6.473; p=0.954) | 0.661* (0.345; p=0.055) |
| Difference: Exposed at 0-5 minus Exposed at 12-17 | -0.211 (0.181; p=0.243) | 0.049 (0.123; p=0.690) | -6.914 (4.370; p=0.114) | 0.072 (3.866; p=0.985) | 0.354 (0.230; p=0.124) |
| Mean of outcome | 9.521 | 10.182 | 41.932 | 36.204 | 12.943 |
| N (children) | 2,111 | 2,159 | 2,111 | 2,159 | 4,280 |
|   of which exposed at 0-5 | 212 | 218 | 212 | 218 | 435 |
|   of which exposed at 6-11 | 166 | 175 | 166 | 175 | 340 |
|   of which exposed at 12-17 | 173 | 177 | 173 | 177 | 329 |
| Families (FE groups, 2+ children) | 689 | 702 | 689 | 702 | 1,370 |
| Families with siblings exposed in different age bands | 97 | 98 | 97 | 98 | 188 |
| Clusters (fam68) | 451 | 455 | 451 | 455 | 672 |
| **White: exposed at 0-17 vs older siblings** | | | | | |
| Exposed at 0-17 (father's first displacement) | 0.010 (0.124; p=0.937) | 0.051 (0.071; p=0.471) | 0.308 (3.138; p=0.922) | 1.893 (2.930; p=0.518) | 0.113 (0.204; p=0.579) |
| Later-born sibling (born after the displacement) | -0.056 (0.164; p=0.733) | -0.013 (0.098; p=0.895) | -2.973 (4.412; p=0.500) | -0.463 (4.013; p=0.908) | -0.195 (0.248; p=0.432) |
| Difference: Exposed at 0-17 (father's first displacement) minus Later-born sibling (born after the displacement) | 0.066 (0.109; p=0.547) | 0.064 (0.070; p=0.361) | 3.281 (3.041; p=0.281) | 2.356 (2.772; p=0.395) | 0.309** (0.133; p=0.021) |
| Mean of outcome | 10.082 | 10.905 | 58.518 | 63.008 | 13.822 |
| N (children) | 3,814 | 3,866 | 3,814 | 3,866 | 6,153 |
|   of which exposed at 0-17 (father's first displacement) | 929 | 950 | 929 | 950 | 1,504 |
|   of which later-born sibling (born after the displacement) | 415 | 423 | 415 | 423 | 857 |
| Families (FE groups, 2+ children) | 1,433 | 1,446 | 1,433 | 1,446 | 2,289 |
| Families with an exposed and an older sibling (a >= 18) | 77 | 77 | 77 | 77 | 116 |
| Families with an exposed and a later-born sibling | 104 | 106 | 104 | 106 | 212 |
| Families with an exposed and a never-displaced (half-)sibling | 0 | 0 | 0 | 0 | 0 |
| Families with siblings exposed in different age bands | 169 | 171 | 169 | 171 | 258 |
| Clusters (fam68) | 949 | 955 | 949 | 955 | 1,230 |
| **White: by age at the displacement** | | | | | |
| Exposed at 0-5 | 0.273 (0.203; p=0.177) | 0.095 (0.120; p=0.428) | 6.018 (5.125; p=0.240) | 4.174 (4.981; p=0.402) | 0.103 (0.302; p=0.732) |
| Exposed at 6-11 | 0.123 (0.165; p=0.458) | 0.042 (0.096; p=0.662) | -0.792 (4.307; p=0.854) | 1.929 (4.098; p=0.638) | 0.070 (0.278; p=0.800) |
| Exposed at 12-17 | 0.017 (0.124; p=0.890) | 0.055 (0.071; p=0.434) | 0.864 (3.134; p=0.783) | 2.064 (2.929; p=0.481) | 0.119 (0.203; p=0.556) |
| Later-born sibling (born after the displacement) | 0.209 (0.243; p=0.389) | 0.030 (0.136; p=0.826) | 2.576 (6.230; p=0.679) | 1.789 (5.697; p=0.754) | -0.209 (0.336; p=0.534) |
| Difference: Exposed at 0-5 minus Exposed at 12-17 | 0.256 (0.166; p=0.124) | 0.040 (0.094; p=0.672) | 5.154 (3.999; p=0.197) | 2.110 (3.841; p=0.583) | -0.016 (0.207; p=0.939) |
| Mean of outcome | 10.082 | 10.905 | 58.518 | 63.008 | 13.822 |
| N (children) | 3,814 | 3,866 | 3,814 | 3,866 | 6,153 |
|   of which exposed at 0-5 | 345 | 354 | 345 | 354 | 609 |
|   of which exposed at 6-11 | 278 | 284 | 278 | 284 | 440 |
|   of which exposed at 12-17 | 306 | 312 | 306 | 312 | 455 |
| Families (FE groups, 2+ children) | 1,433 | 1,446 | 1,433 | 1,446 | 2,289 |
| Families with siblings exposed in different age bands | 169 | 171 | 169 | 171 | 258 |
| Clusters (fam68) | 949 | 955 | 949 | 955 | 1,230 |
| **Pooled: exposed at 0-17 vs older siblings** | | | | | |
| Exposed at 0-17 (father's first displacement) | 0.080 (0.115; p=0.486) | 0.077 (0.070; p=0.269) | 1.647 (2.558; p=0.520) | 2.734 (2.241; p=0.222) | 0.254* (0.147; p=0.085) |
| Later-born sibling (born after the displacement) | -0.067 (0.145; p=0.643) | -0.022 (0.093; p=0.814) | -3.077 (3.425; p=0.369) | -0.222 (3.132; p=0.944) | 0.073 (0.183; p=0.691) |
| Difference: Exposed at 0-17 (father's first displacement) minus Later-born sibling (born after the displacement) | 0.147* (0.087; p=0.092) | 0.099* (0.056; p=0.076) | 4.724** (2.238; p=0.035) | 2.956 (2.065; p=0.152) | 0.181* (0.103; p=0.080) |
| Mean of outcome | 9.881 | 10.645 | 52.559 | 53.348 | 13.460 |
| N (children) | 5,937 | 6,037 | 5,937 | 6,037 | 10,442 |
|   of which exposed at 0-17 (father's first displacement) | 1,482 | 1,522 | 1,482 | 1,522 | 2,610 |
|   of which later-born sibling (born after the displacement) | 620 | 633 | 620 | 633 | 1,419 |
| Families (FE groups, 2+ children) | 2,127 | 2,153 | 2,127 | 2,153 | 3,661 |
| Families with an exposed and an older sibling (a >= 18) | 128 | 130 | 128 | 130 | 222 |
| Families with an exposed and a later-born sibling | 174 | 178 | 174 | 178 | 372 |
| Families with an exposed and a never-displaced (half-)sibling | 0 | 0 | 0 | 0 | 0 |
| Families with siblings exposed in different age bands | 266 | 269 | 266 | 269 | 446 |
| Clusters (fam68) | 1,400 | 1,410 | 1,400 | 1,410 | 1,896 |
| **Pooled: by age at the displacement** | | | | | |
| Exposed at 0-5 | 0.153 (0.166; p=0.356) | 0.109 (0.104; p=0.297) | 1.967 (4.043; p=0.627) | 3.846 (3.620; p=0.288) | 0.434** (0.212; p=0.041) |
| Exposed at 6-11 | 0.128 (0.140; p=0.360) | 0.134 (0.089; p=0.132) | 1.248 (3.433; p=0.716) | 4.394 (3.042; p=0.149) | 0.381** (0.194; p=0.050) |
| Exposed at 12-17 | 0.078 (0.116; p=0.502) | 0.070 (0.070; p=0.317) | 1.736 (2.562; p=0.498) | 2.544 (2.246; p=0.257) | 0.243* (0.147; p=0.098) |
| Later-born sibling (born after the displacement) | 0.008 (0.195; p=0.968) | 0.013 (0.121; p=0.913) | -2.800 (4.735; p=0.554) | 0.997 (4.271; p=0.815) | 0.256 (0.241; p=0.289) |
| Difference: Exposed at 0-5 minus Exposed at 12-17 | 0.075 (0.124; p=0.543) | 0.038 (0.076; p=0.616) | 0.231 (3.080; p=0.940) | 1.302 (2.767; p=0.638) | 0.191 (0.152; p=0.210) |
| Mean of outcome | 9.881 | 10.645 | 52.559 | 53.348 | 13.460 |
| N (children) | 5,937 | 6,037 | 5,937 | 6,037 | 10,442 |
|   of which exposed at 0-5 | 559 | 574 | 559 | 574 | 1,046 |
|   of which exposed at 6-11 | 444 | 459 | 444 | 459 | 780 |
|   of which exposed at 12-17 | 479 | 489 | 479 | 489 | 784 |
| Families (FE groups, 2+ children) | 2,127 | 2,153 | 2,127 | 2,153 | 3,661 |
| Families with siblings exposed in different age bands | 266 | 269 | 266 | 269 | 446 |
| Clusters (fam68) | 1,400 | 1,410 | 1,400 | 1,410 | 1,896 |
| Fixed effects | parents fe, birth year | parents fe, birth year | parents fe, birth year | parents fe, birth year | parents fe, birth year |
| Other controls | female, birth order (2, 3+), never-displaced dummy; Black in pooled rows | female, birth order (2, 3+), never-displaced dummy; Black in pooled rows | female, birth order (2, 3+), never-displaced dummy; Black in pooled rows | female, birth order (2, 3+), never-displaced dummy; Black in pooled rows | female, birth order (2, 3+), never-displaced dummy; Black in pooled rows |

### 2c. Mother FE, closures only

Families whose father figure's first displacement is a closure / move, plus families whose father figure was never displaced (families with a first layoff are dropped).

| | Log lifetime earnings | Log lifetime family income | Earnings rank (0-100) | Family income rank (0-100) | Years of schooling |
|---|---|---|---|---|---|
| **Black: father's first displacement a closure (vs older siblings)** | | | | | |
| Exposed at 0-17 (father's first displacement) | 0.196 (0.329; p=0.551) | -0.183 (0.209; p=0.383) | 1.501 (6.910; p=0.828) | -2.069 (5.404; p=0.702) | 0.331 (0.293; p=0.259) |
| Later-born sibling (born after the displacement) | -0.273 (0.393; p=0.487) | -0.134 (0.262; p=0.607) | -11.218 (8.493; p=0.187) | -2.736 (8.024; p=0.733) | 0.455 (0.405; p=0.261) |
| Father figure never displaced (half-sibling) | -0.495 (0.451; p=0.272) | -0.625** (0.283; p=0.027) | -16.840** (7.287; p=0.021) | -21.050*** (7.135; p=0.003) | -0.340 (0.392; p=0.386) |
| Difference: Exposed at 0-17 (father's first displacement) minus Later-born sibling (born after the displacement) | 0.469* (0.258; p=0.069) | -0.048 (0.185; p=0.794) | 12.718* (6.500; p=0.050) | 0.667 (6.018; p=0.912) | -0.124 (0.347; p=0.721) |
| Mean of outcome | 9.546 | 10.207 | 42.915 | 37.252 | 12.990 |
| N (children) | 1,562 | 1,596 | 1,562 | 1,596 | 3,027 |
|   of which exposed at 0-17 (father's first displacement) | 167 | 171 | 167 | 171 | 311 |
|   of which later-born sibling (born after the displacement) | 43 | 44 | 43 | 44 | 114 |
| Families (FE groups, 2+ children) | 498 | 508 | 498 | 508 | 950 |
| Families with an exposed and an older sibling (a >= 18) | 14 | 15 | 14 | 15 | 38 |
| Families with an exposed and a later-born sibling | 16 | 17 | 16 | 17 | 33 |
| Families with an exposed and a never-displaced (half-)sibling | 3 | 3 | 3 | 3 | 10 |
| Families with siblings exposed in different age bands | 36 | 36 | 36 | 36 | 59 |
| Clusters (fam68) | 352 | 357 | 352 | 357 | 540 |
| **White: father's first displacement a closure (vs older siblings)** | | | | | |
| Exposed at 0-17 (father's first displacement) | 0.065 (0.143; p=0.652) | 0.071 (0.096; p=0.459) | 2.739 (3.856; p=0.478) | 3.217 (3.828; p=0.401) | 0.258 (0.257; p=0.317) |
| Later-born sibling (born after the displacement) | -0.300 (0.264; p=0.255) | -0.098 (0.195; p=0.614) | -8.718 (8.081; p=0.281) | -3.491 (8.013; p=0.663) | -0.027 (0.384; p=0.945) |
| Father figure never displaced (half-sibling) | 0.272 (0.460; p=0.553) | -0.228 (0.368; p=0.536) | -2.383 (12.435; p=0.848) | -11.306 (16.733; p=0.499) | -0.191 (0.460; p=0.678) |
| Difference: Exposed at 0-17 (father's first displacement) minus Later-born sibling (born after the displacement) | 0.365* (0.218; p=0.095) | 0.169 (0.171; p=0.322) | 11.456 (7.063; p=0.105) | 6.708 (7.077; p=0.343) | 0.284 (0.284; p=0.317) |
| Mean of outcome | 10.111 | 10.938 | 59.784 | 64.602 | 13.916 |
| N (children) | 2,719 | 2,750 | 2,719 | 2,750 | 4,324 |
|   of which exposed at 0-17 (father's first displacement) | 337 | 344 | 337 | 344 | 555 |
|   of which later-born sibling (born after the displacement) | 117 | 118 | 117 | 118 | 230 |
| Families (FE groups, 2+ children) | 1,017 | 1,024 | 1,017 | 1,024 | 1,581 |
| Families with an exposed and an older sibling (a >= 18) | 38 | 38 | 38 | 38 | 58 |
| Families with an exposed and a later-born sibling | 28 | 28 | 28 | 28 | 58 |
| Families with an exposed and a never-displaced (half-)sibling | 1 | 1 | 1 | 1 | 9 |
| Families with siblings exposed in different age bands | 63 | 63 | 63 | 63 | 95 |
| Clusters (fam68) | 759 | 764 | 759 | 764 | 1,004 |
| **Pooled: father's first displacement a closure (vs older siblings)** | | | | | |
| Exposed at 0-17 (father's first displacement) | 0.112 (0.141; p=0.427) | -0.015 (0.093; p=0.876) | 2.797 (3.308; p=0.398) | 1.315 (3.018; p=0.663) | 0.299 (0.193; p=0.122) |
| Later-born sibling (born after the displacement) | -0.343* (0.207; p=0.098) | -0.136 (0.151; p=0.367) | -10.764* (5.647; p=0.057) | -4.704 (5.525; p=0.395) | 0.132 (0.280; p=0.638) |
| Father figure never displaced (half-sibling) | -0.298 (0.356; p=0.402) | -0.504** (0.233; p=0.031) | -10.822* (6.567; p=0.099) | -18.400*** (6.536; p=0.005) | -0.210 (0.292; p=0.472) |
| Difference: Exposed at 0-17 (father's first displacement) minus Later-born sibling (born after the displacement) | 0.455*** (0.156; p=0.004) | 0.121 (0.122; p=0.318) | 13.560*** (4.787; p=0.005) | 6.019 (4.745; p=0.205) | 0.167 (0.219; p=0.445) |
| Mean of outcome | 9.903 | 10.668 | 53.568 | 54.492 | 13.534 |
| N (children) | 4,291 | 4,356 | 4,291 | 4,356 | 7,359 |
|   of which exposed at 0-17 (father's first displacement) | 505 | 516 | 505 | 516 | 867 |
|   of which later-born sibling (born after the displacement) | 161 | 163 | 161 | 163 | 345 |
| Families (FE groups, 2+ children) | 1,519 | 1,536 | 1,519 | 1,536 | 2,532 |
| Families with an exposed and an older sibling (a >= 18) | 52 | 53 | 52 | 53 | 96 |
| Families with an exposed and a later-born sibling | 45 | 46 | 45 | 46 | 92 |
| Families with an exposed and a never-displaced (half-)sibling | 4 | 4 | 4 | 4 | 19 |
| Families with siblings exposed in different age bands | 99 | 99 | 99 | 99 | 154 |
| Clusters (fam68) | 1,113 | 1,123 | 1,113 | 1,123 | 1,542 |
| Fixed effects | mother, birth year | mother, birth year | mother, birth year | mother, birth year | mother, birth year |
| Other controls | female, birth order (2, 3+), never-displaced dummy; Black in pooled rows | female, birth order (2, 3+), never-displaced dummy; Black in pooled rows | female, birth order (2, 3+), never-displaced dummy; Black in pooled rows | female, birth order (2, 3+), never-displaced dummy; Black in pooled rows | female, birth order (2, 3+), never-displaced dummy; Black in pooled rows |

### 2d. Sibling samples (mother FE, families with 2+ children with the outcome)

| | Children | Families | Exposed children | Fam.: exposed + older (a >= 18) | Fam.: exposed + later-born | Fam.: exposed + never-displaced half-sibling | Fam.: exposed in different bands | Share mother from CAH |
|---|---|---|---|---|---|---|---|---|
| Black, Log lifetime earnings sample | 2,368 | 785 | 577 | 54 | 74 | 12 | 99 | 0.46 |
| Black, Years of schooling sample | 4,712 | 1,495 | 1,143 | 112 | 170 | 33 | 190 | 0.58 |
| White, Log lifetime earnings sample | 3,927 | 1,476 | 946 | 79 | 112 | 9 | 169 | 0.51 |
| White, Years of schooling sample | 6,410 | 2,349 | 1,539 | 119 | 229 | 36 | 259 | 0.61 |

## 3. Pre-trends and selection

### 3a. Future displacement: does a displacement after childhood 'predict' the child's outcomes?

Children born 1956-1997 with a father figure at 12-17 (the last one observed) who worked at child age 12-14 and is observed in 2+ years when the child is 18-25. Groups: first displaced at 12-17 (childhood); never displaced at 0-17 but the father figure displaced when the child is 18-25 (after childhood); neither (reference). Children first displaced at 0-11 are dropped. Controls: log family income at ages 9-12, parental education, female, birth-year FE (+ Black). A displacement after childhood can still matter (college funding, a later transfer), so the 22-25 window is shown too; if the after-childhood coefficient is as large as the childhood one, the childhood association is likely selection on family traits.

| | Log lifetime earnings | Log lifetime family income | Earnings rank (0-100) | Family income rank (0-100) | Years of schooling |
|---|---|---|---|---|---|
| **Black: closure or layoff, after-childhood window 18-25** | | | | | |
| Displaced first at 12-17 (childhood) | -0.233* (0.120; p=0.052) | -0.104 (0.069; p=0.132) | -5.109** (2.306; p=0.027) | -3.511 (2.206; p=0.111) | -0.368*** (0.136; p=0.007) |
| Displaced at 18-25 only (after childhood) | -0.101 (0.127; p=0.424) | 0.044 (0.071; p=0.534) | -0.365 (2.675; p=0.891) | 0.276 (2.487; p=0.912) | -0.106 (0.137; p=0.437) |
| Difference: Displaced first at 12-17 (childhood) minus Displaced at 18-25 only (after childhood) | -0.132 (0.170; p=0.438) | -0.149* (0.087; p=0.089) | -4.744 (2.983; p=0.112) | -3.788 (2.816; p=0.179) | -0.262 (0.164; p=0.110) |
| Mean of outcome | 9.663 | 10.283 | 46.326 | 40.341 | 13.274 |
| N (children) | 986 | 1,001 | 986 | 1,001 | 1,709 |
|   of which displaced first at 12-17 (childhood) | 141 | 145 | 141 | 145 | 274 |
|   of which displaced at 18-25 only (after childhood) | 145 | 147 | 145 | 147 | 235 |
| Clusters (fam68) | 388 | 393 | 388 | 393 | 512 |
| **White: closure or layoff, after-childhood window 18-25** | | | | | |
| Displaced first at 12-17 (childhood) | -0.073 (0.060; p=0.225) | -0.060* (0.034; p=0.082) | -1.929 (1.564; p=0.217) | -2.756** (1.387; p=0.047) | -0.232** (0.105; p=0.028) |
| Displaced at 18-25 only (after childhood) | -0.005 (0.063; p=0.931) | -0.014 (0.040; p=0.730) | -0.006 (1.717; p=0.997) | -1.056 (1.640; p=0.520) | -0.062 (0.113; p=0.581) |
| Difference: Displaced first at 12-17 (childhood) minus Displaced at 18-25 only (after childhood) | -0.067 (0.076; p=0.376) | -0.046 (0.047; p=0.331) | -1.923 (2.018; p=0.341) | -1.700 (1.908; p=0.373) | -0.170 (0.135; p=0.208) |
| Mean of outcome | 10.173 | 10.972 | 61.176 | 66.114 | 14.231 |
| N (children) | 2,525 | 2,539 | 2,525 | 2,539 | 3,603 |
|   of which displaced first at 12-17 (childhood) | 331 | 334 | 331 | 334 | 485 |
|   of which displaced at 18-25 only (after childhood) | 293 | 294 | 293 | 294 | 408 |
| Clusters (fam68) | 933 | 937 | 933 | 937 | 1,125 |
| **Pooled: closure or layoff, after-childhood window 18-25** | | | | | |
| Displaced first at 12-17 (childhood) | -0.120** (0.055; p=0.030) | -0.075** (0.032; p=0.021) | -2.772** (1.317; p=0.035) | -2.855** (1.164; p=0.014) | -0.273*** (0.084; p=0.001) |
| Displaced at 18-25 only (after childhood) | -0.033 (0.060; p=0.585) | 0.001 (0.035; p=0.972) | 0.032 (1.448; p=0.982) | -0.665 (1.356; p=0.624) | -0.075 (0.089; p=0.398) |
| Difference: Displaced first at 12-17 (childhood) minus Displaced at 18-25 only (after childhood) | -0.087 (0.074; p=0.239) | -0.076* (0.042; p=0.073) | -2.804* (1.675; p=0.094) | -2.190 (1.560; p=0.160) | -0.198* (0.105; p=0.060) |
| Mean of outcome | 10.030 | 10.777 | 57.006 | 58.826 | 13.923 |
| N (children) | 3,511 | 3,540 | 3,511 | 3,540 | 5,312 |
|   of which displaced first at 12-17 (childhood) | 472 | 479 | 472 | 479 | 759 |
|   of which displaced at 18-25 only (after childhood) | 438 | 441 | 438 | 441 | 643 |
| Clusters (fam68) | 1,318 | 1,327 | 1,318 | 1,327 | 1,632 |
| **Black: closure or layoff, after-childhood window 22-25 (children displaced at 18-21 dropped)** | | | | | |
| Displaced first at 12-17 (childhood) | -0.273** (0.131; p=0.037) | -0.131* (0.076; p=0.084) | -5.206** (2.544; p=0.041) | -3.936* (2.334; p=0.092) | -0.440*** (0.144; p=0.002) |
| Displaced at 22-25 only (after childhood) | 0.066 (0.130; p=0.610) | 0.098 (0.089; p=0.267) | -0.270 (3.789; p=0.943) | 1.872 (3.443; p=0.587) | -0.249 (0.183; p=0.175) |
| Difference: Displaced first at 12-17 (childhood) minus Displaced at 22-25 only (after childhood) | -0.339* (0.173; p=0.050) | -0.229** (0.104; p=0.028) | -4.936 (4.131; p=0.232) | -5.809 (3.760; p=0.122) | -0.191 (0.210; p=0.362) |
| Mean of outcome | 9.690 | 10.293 | 46.693 | 40.771 | 13.350 |
| N (children) | 840 | 854 | 840 | 854 | 1,394 |
|   of which displaced first at 12-17 (childhood) | 125 | 129 | 125 | 129 | 238 |
|   of which displaced at 22-25 only (after childhood) | 62 | 64 | 62 | 64 | 92 |
| Clusters (fam68) | 356 | 360 | 356 | 360 | 464 |
| **White: closure or layoff, after-childhood window 22-25 (children displaced at 18-21 dropped)** | | | | | |
| Displaced first at 12-17 (childhood) | -0.082 (0.063; p=0.191) | -0.063* (0.035; p=0.077) | -2.159 (1.611; p=0.180) | -2.792* (1.436; p=0.052) | -0.257** (0.110; p=0.020) |
| Displaced at 22-25 only (after childhood) | -0.014 (0.095; p=0.882) | -0.044 (0.057; p=0.441) | -0.352 (2.448; p=0.886) | -2.562 (2.272; p=0.259) | -0.064 (0.149; p=0.668) |
| Difference: Displaced first at 12-17 (childhood) minus Displaced at 22-25 only (after childhood) | -0.068 (0.103; p=0.510) | -0.019 (0.061; p=0.754) | -1.807 (2.644; p=0.494) | -0.230 (2.443; p=0.925) | -0.193 (0.172; p=0.263) |
| Mean of outcome | 10.174 | 10.978 | 61.247 | 66.339 | 14.318 |
| N (children) | 2,266 | 2,277 | 2,266 | 2,277 | 3,137 |
|   of which displaced first at 12-17 (childhood) | 317 | 320 | 317 | 320 | 454 |
|   of which displaced at 22-25 only (after childhood) | 134 | 134 | 134 | 134 | 177 |
| Clusters (fam68) | 874 | 878 | 874 | 878 | 1,044 |
| **Pooled: closure or layoff, after-childhood window 22-25 (children displaced at 18-21 dropped)** | | | | | |
| Displaced first at 12-17 (childhood) | -0.130** (0.059; p=0.026) | -0.085** (0.034; p=0.012) | -2.859** (1.380; p=0.038) | -3.081** (1.215; p=0.011) | -0.306*** (0.089; p=<0.001) |
| Displaced at 22-25 only (after childhood) | 0.023 (0.076; p=0.767) | 0.007 (0.047; p=0.876) | -0.135 (1.993; p=0.946) | -0.943 (1.845; p=0.609) | -0.110 (0.118; p=0.350) |
| Difference: Displaced first at 12-17 (childhood) minus Displaced at 22-25 only (after childhood) | -0.153* (0.087; p=0.079) | -0.093* (0.052; p=0.074) | -2.725 (2.179; p=0.211) | -2.139 (1.994; p=0.283) | -0.196 (0.135; p=0.148) |
| Mean of outcome | 10.043 | 10.791 | 57.311 | 59.365 | 14.021 |
| N (children) | 3,106 | 3,131 | 3,106 | 3,131 | 4,531 |
|   of which displaced first at 12-17 (childhood) | 442 | 449 | 442 | 449 | 692 |
|   of which displaced at 22-25 only (after childhood) | 196 | 198 | 196 | 198 | 269 |
| Clusters (fam68) | 1,227 | 1,235 | 1,227 | 1,235 | 1,504 |
| **Black: closures only (first displacement in the window a closure), window 18-25** | | | | | |
| Displaced first at 12-17 (childhood) | 0.019 (0.136; p=0.891) | -0.106 (0.114; p=0.353) | -1.744 (3.732; p=0.640) | -2.598 (3.423; p=0.448) | -0.164 (0.231; p=0.476) |
| Displaced at 18-25 only (after childhood) | -0.194 (0.191; p=0.310) | 0.010 (0.102; p=0.921) | -2.199 (3.967; p=0.579) | -1.116 (3.586; p=0.756) | 0.031 (0.173; p=0.859) |
| Difference: Displaced first at 12-17 (childhood) minus Displaced at 18-25 only (after childhood) | 0.213 (0.240; p=0.375) | -0.116 (0.151; p=0.440) | 0.455 (5.248; p=0.931) | -1.482 (4.687; p=0.752) | -0.195 (0.254; p=0.441) |
| Mean of outcome | 9.730 | 10.311 | 47.467 | 41.187 | 13.376 |
| N (children) | 819 | 831 | 819 | 831 | 1,402 |
|   of which displaced first at 12-17 (childhood) | 50 | 52 | 50 | 52 | 91 |
|   of which displaced at 18-25 only (after childhood) | 69 | 70 | 69 | 70 | 111 |
| Clusters (fam68) | 331 | 335 | 331 | 335 | 447 |
| **White: closures only (first displacement in the window a closure), window 18-25** | | | | | |
| Displaced first at 12-17 (childhood) | -0.053 (0.090; p=0.551) | -0.000 (0.048; p=1.000) | -0.258 (2.218; p=0.907) | -0.893 (1.932; p=0.644) | -0.120 (0.148; p=0.418) |
| Displaced at 18-25 only (after childhood) | -0.067 (0.088; p=0.450) | -0.032 (0.054; p=0.551) | -2.390 (2.265; p=0.291) | -1.790 (2.254; p=0.427) | -0.198 (0.158; p=0.210) |
| Difference: Displaced first at 12-17 (childhood) minus Displaced at 18-25 only (after childhood) | 0.013 (0.107; p=0.903) | 0.032 (0.066; p=0.629) | 2.132 (2.785; p=0.444) | 0.898 (2.766; p=0.746) | 0.079 (0.192; p=0.682) |
| Mean of outcome | 10.185 | 10.988 | 61.556 | 66.768 | 14.291 |
| N (children) | 2,200 | 2,211 | 2,200 | 2,211 | 3,126 |
|   of which displaced first at 12-17 (childhood) | 146 | 147 | 146 | 147 | 213 |
|   of which displaced at 18-25 only (after childhood) | 153 | 153 | 153 | 153 | 203 |
| Clusters (fam68) | 835 | 837 | 835 | 837 | 1,023 |
| **Pooled: closures only (first displacement in the window a closure), window 18-25** | | | | | |
| Displaced first at 12-17 (childhood) | -0.023 (0.076; p=0.759) | -0.032 (0.050; p=0.523) | -0.176 (1.961; p=0.929) | -1.252 (1.676; p=0.455) | -0.125 (0.125; p=0.315) |
| Displaced at 18-25 only (after childhood) | -0.097 (0.085; p=0.250) | -0.023 (0.048; p=0.636) | -2.084 (1.977; p=0.292) | -1.612 (1.874; p=0.390) | -0.101 (0.121; p=0.403) |
| Difference: Displaced first at 12-17 (childhood) minus Displaced at 18-25 only (after childhood) | 0.074 (0.103; p=0.471) | -0.009 (0.064; p=0.883) | 1.908 (2.494; p=0.444) | 0.360 (2.315; p=0.876) | -0.024 (0.153; p=0.877) |
| Mean of outcome | 10.062 | 10.803 | 57.734 | 59.780 | 14.008 |
| N (children) | 3,019 | 3,042 | 3,019 | 3,042 | 4,528 |
|   of which displaced first at 12-17 (childhood) | 196 | 199 | 196 | 199 | 304 |
|   of which displaced at 18-25 only (after childhood) | 222 | 223 | 222 | 223 | 314 |
| Clusters (fam68) | 1,163 | 1,169 | 1,163 | 1,169 | 1,465 |
| Fixed effects | birth year | birth year | birth year | birth year | birth year |
| Other controls | log family income at 9-12, parental education, female | log family income at 9-12, parental education, female | log family income at 9-12, parental education, female | log family income at 9-12, parental education, female | log family income at 9-12, parental education, female |

### 3b. CDS: displacement after the test (lead) vs before

CDS child-tests at 3-17 whose father figure at the test worked in the year(s) before it and is observed in 2+ years of test year + 1..+4. Before = first displaced before the test year; lead = not displaced before the test, father figure displaced in test year + 1..+4; reference = neither. Controls: log family income over the 3 years before the test, parental education, female, birth-year and CDS-wave FE (+ Black). A lead 'effect' as large as the 'before' coefficient points to selection; a lead coefficient can also pick up anticipation (a declining firm).

| | WJ Letter-Word | WJ Applied Problems | WJ Passage Comp. | BPI (z, higher = worse) |
|---|---|---|---|---|
| **Black: closure or layoff** | | | | |
| Displaced before the test | -0.755 (1.481; p=0.610) | -1.938 (1.427; p=0.174) | -0.890 (1.389; p=0.521) | 0.017 (0.072; p=0.815) |
| Displaced 1-4 years after the test (lead) | 0.033 (1.771; p=0.985) | -1.390 (2.277; p=0.542) | -0.728 (1.687; p=0.666) | -0.016 (0.103; p=0.876) |
| Difference: Displaced before the test minus Displaced 1-4 years after the test (lead) | -0.787 (1.897; p=0.678) | -0.548 (2.220; p=0.805) | -0.163 (1.708; p=0.924) | 0.033 (0.108; p=0.762) |
| Mean of outcome | 100.295 | 95.614 | 98.828 | -0.142 |
| N (children x tests) | 1,166 | 1,163 | 970 | 1,774 |
|   of which displaced before the test | 335 | 333 | 295 | 543 |
|   of which displaced 1-4 years after the test (lead) | 89 | 89 | 71 | 148 |
| Clusters (fam68) | 340 | 339 | 314 | 410 |
| **White: closure or layoff** | | | | |
| Displaced before the test | -0.430 (1.015; p=0.672) | 0.076 (0.930; p=0.935) | -0.160 (0.962; p=0.868) | 0.118** (0.049; p=0.017) |
| Displaced 1-4 years after the test (lead) | 2.141 (1.575; p=0.174) | 1.031 (1.442; p=0.475) | 1.440 (1.546; p=0.352) | 0.225*** (0.078; p=0.004) |
| Difference: Displaced before the test minus Displaced 1-4 years after the test (lead) | -2.570 (1.685; p=0.127) | -0.955 (1.551; p=0.538) | -1.599 (1.644; p=0.331) | -0.108 (0.084; p=0.201) |
| Mean of outcome | 107.726 | 108.666 | 107.136 | -0.007 |
| N (children x tests) | 2,842 | 2,826 | 2,410 | 4,507 |
|   of which displaced before the test | 611 | 611 | 550 | 952 |
|   of which displaced 1-4 years after the test (lead) | 151 | 151 | 129 | 235 |
| Clusters (fam68) | 655 | 655 | 631 | 803 |
| **Pooled: closure or layoff** | | | | |
| Displaced before the test | -0.481 (0.829; p=0.562) | -0.647 (0.780; p=0.407) | -0.382 (0.781; p=0.624) | 0.077* (0.040; p=0.055) |
| Displaced 1-4 years after the test (lead) | 1.656 (1.201; p=0.168) | 0.344 (1.234; p=0.780) | 0.789 (1.152; p=0.494) | 0.127** (0.063; p=0.044) |
| Difference: Displaced before the test minus Displaced 1-4 years after the test (lead) | -2.137* (1.278; p=0.095) | -0.991 (1.265; p=0.433) | -1.171 (1.209; p=0.333) | -0.050 (0.066; p=0.456) |
| Mean of outcome | 105.564 | 104.860 | 104.751 | -0.045 |
| N (children x tests) | 4,008 | 3,989 | 3,380 | 6,281 |
|   of which displaced before the test | 946 | 944 | 845 | 1,495 |
|   of which displaced 1-4 years after the test (lead) | 240 | 240 | 200 | 383 |
| Clusters (fam68) | 982 | 982 | 935 | 1,188 |
| **Black: closures only** | | | | |
| Displaced before the test | 2.626 (2.315; p=0.257) | -2.556 (2.428; p=0.293) | 1.351 (2.152; p=0.530) | -0.120 (0.114; p=0.293) |
| Displaced 1-4 years after the test (lead) | -0.130 (3.561; p=0.971) | -2.820 (4.757; p=0.553) | -1.749 (3.124; p=0.576) | 0.076 (0.185; p=0.682) |
| Difference: Displaced before the test minus Displaced 1-4 years after the test (lead) | 2.756 (3.732; p=0.460) | 0.264 (4.054; p=0.948) | 3.099 (3.142; p=0.324) | -0.195 (0.194; p=0.313) |
| Mean of outcome | 100.927 | 96.327 | 99.855 | -0.162 |
| N (children x tests) | 839 | 836 | 689 | 1,254 |
|   of which displaced before the test | 76 | 74 | 68 | 132 |
|   of which displaced 1-4 years after the test (lead) | 21 | 21 | 17 | 39 |
| Clusters (fam68) | 285 | 284 | 258 | 347 |
| **White: closures only** | | | | |
| Displaced before the test | -0.347 (1.498; p=0.817) | 0.325 (1.492; p=0.828) | 1.180 (1.355; p=0.384) | -0.010 (0.081; p=0.905) |
| Displaced 1-4 years after the test (lead) | 1.877 (2.812; p=0.504) | -1.796 (2.313; p=0.437) | -1.644 (2.940; p=0.576) | 0.129 (0.127; p=0.312) |
| Difference: Displaced before the test minus Displaced 1-4 years after the test (lead) | -2.225 (3.034; p=0.463) | 2.120 (2.437; p=0.384) | 2.823 (3.175; p=0.374) | -0.138 (0.139; p=0.321) |
| Mean of outcome | 107.995 | 108.947 | 107.479 | -0.052 |
| N (children x tests) | 2,334 | 2,318 | 1,962 | 3,681 |
|   of which displaced before the test | 198 | 198 | 184 | 285 |
|   of which displaced 1-4 years after the test (lead) | 56 | 56 | 47 | 76 |
| Clusters (fam68) | 587 | 585 | 559 | 744 |
| **Pooled: closures only** | | | | |
| Displaced before the test | 0.403 (1.251; p=0.747) | -0.549 (1.297; p=0.672) | 1.247 (1.154; p=0.280) | -0.046 (0.065; p=0.483) |
| Displaced 1-4 years after the test (lead) | 1.608 (2.270; p=0.479) | -1.869 (2.225; p=0.401) | -1.555 (2.251; p=0.490) | 0.094 (0.104; p=0.368) |
| Difference: Displaced before the test minus Displaced 1-4 years after the test (lead) | -1.205 (2.422; p=0.619) | 1.320 (2.166; p=0.542) | 2.801 (2.412; p=0.246) | -0.140 (0.112; p=0.214) |
| Mean of outcome | 106.126 | 105.601 | 105.497 | -0.080 |
| N (children x tests) | 3,173 | 3,154 | 2,651 | 4,935 |
|   of which displaced before the test | 274 | 272 | 252 | 417 |
|   of which displaced 1-4 years after the test (lead) | 77 | 77 | 64 | 115 |
| Clusters (fam68) | 862 | 860 | 810 | 1,072 |
| Fixed effects | birth year, CDS wave | birth year, CDS wave | birth year, CDS wave | birth year, CDS wave |
| Other controls | log family income 3 yrs before the test, parental education, female | log family income 3 yrs before the test, parental education, female | log family income 3 yrs before the test, parental education, female | log family income 3 yrs before the test, parental education, female |

### 3c. Balance: pre-event characteristics of displaced vs control children

Each column regresses a pre-event characteristic on 'displaced' with birth-year FE (+ CDS-wave FE; + Black in pooled rows), in the 0-17 exposure designs of Section 1 / 19 (adult sample: children with log earnings or schooling). Growth = log change from the earliest of d-4/d-5 to the latest of d-1/d-2, scaled to 3 years (d = the (pseudo) event year). The family-income and labor-income growth columns are the pre-trend test of the father's trajectory: d-1 contains part of the Jacobson-LaLonde-Sullivan dip (and dating error), so a negative growth gap partly reflects the displacement itself.

| | Log pre-event family income | Parental education (years) | Family-income growth, 3 yrs before | Father's labor-income growth, 3 yrs before | Log father's labor income, d-2/d-3 | Mother figure employed year before | Father's age | Father white-collar (occupation) | Father in manufacturing |
|---|---|---|---|---|---|---|---|---|---|
| **Black: closure or layoff, adult-outcome sample** | | | | | | | | | |
| Father figure displaced | -0.244*** (0.033; p=<0.001) | -0.300** (0.131; p=0.022) | -0.016 (0.054; p=0.765) | -0.081 (0.055; p=0.138) | -0.329*** (0.041; p=<0.001) | 0.022 (0.028; p=0.422) | -1.873*** (0.525; p=<0.001) | -0.082*** (0.022; p=<0.001) | -0.000 (0.031; p=0.996) |
| Mean among controls | 10.539 | 13.230 | 0.151 | 0.094 | 10.214 | 0.660 | 35.900 | 0.221 | 0.335 |
| N (children) | 2,836 | 2,837 | 1,913 | 1,890 | 2,473 | 2,662 | 2,838 | 2,506 | 2,492 |
|   of which father figure displaced | 1,571 | 1,572 | 999 | 986 | 1,347 | 1,439 | 1,573 | 1,383 | 1,371 |
| Clusters (fam68) | 651 | 651 | 542 | 538 | 610 | 633 | 651 | 617 | 616 |
| **White: closure or layoff, adult-outcome sample** | | | | | | | | | |
| Father figure displaced | -0.235*** (0.024; p=<0.001) | -0.818*** (0.089; p=<0.001) | -0.080** (0.040; p=0.046) | -0.074** (0.030; p=0.016) | -0.269*** (0.029; p=<0.001) | 0.068*** (0.019; p=<0.001) | -0.170 (0.296; p=0.564) | -0.153*** (0.021; p=<0.001) | 0.079*** (0.019; p=<0.001) |
| Mean among controls | 10.951 | 14.717 | 0.143 | 0.113 | 10.649 | 0.605 | 34.623 | 0.533 | 0.240 |
| N (children) | 4,895 | 4,895 | 3,843 | 3,803 | 4,480 | 4,820 | 4,895 | 4,511 | 4,502 |
|   of which father figure displaced | 2,274 | 2,274 | 1,627 | 1,601 | 2,037 | 2,225 | 2,274 | 2,081 | 2,074 |
| Clusters (fam68) | 1,303 | 1,303 | 1,160 | 1,158 | 1,259 | 1,298 | 1,303 | 1,252 | 1,251 |
| **Pooled: closure or layoff, adult-outcome sample** | | | | | | | | | |
| Father figure displaced | -0.239*** (0.020; p=<0.001) | -0.620*** (0.075; p=<0.001) | -0.061* (0.032; p=0.060) | -0.079*** (0.027; p=0.004) | -0.293*** (0.024; p=<0.001) | 0.052*** (0.016; p=0.001) | -0.813*** (0.270; p=0.003) | -0.129*** (0.016; p=<0.001) | 0.052*** (0.017; p=0.002) |
| Mean among controls | 10.817 | 14.233 | 0.146 | 0.108 | 10.511 | 0.623 | 35.039 | 0.435 | 0.270 |
| N (children) | 7,731 | 7,732 | 5,756 | 5,693 | 6,953 | 7,482 | 7,733 | 7,017 | 6,994 |
|   of which father figure displaced | 3,845 | 3,846 | 2,626 | 2,587 | 3,384 | 3,664 | 3,847 | 3,464 | 3,445 |
| Clusters (fam68) | 1,940 | 1,940 | 1,691 | 1,685 | 1,856 | 1,917 | 1,940 | 1,856 | 1,854 |
| **Black: closures only, adult-outcome sample** | | | | | | | | | |
| Father figure displaced | -0.175*** (0.049; p=<0.001) | -0.384** (0.185; p=0.038) | -0.095 (0.065; p=0.143) | -0.119* (0.068; p=0.079) | -0.220*** (0.049; p=<0.001) | 0.042 (0.041; p=0.305) | -1.032 (0.811; p=0.203) | -0.011 (0.039; p=0.785) | 0.005 (0.044; p=0.907) |
| Mean among controls | 10.580 | 13.061 | 0.122 | 0.082 | 10.246 | 0.666 | 37.620 | 0.230 | 0.301 |
| N (children) | 1,786 | 1,787 | 1,290 | 1,275 | 1,588 | 1,723 | 1,787 | 1,638 | 1,630 |
|   of which father figure displaced | 406 | 406 | 286 | 286 | 362 | 384 | 406 | 371 | 368 |
| Clusters (fam68) | 541 | 541 | 457 | 453 | 507 | 531 | 541 | 519 | 517 |
| **White: closures only, adult-outcome sample** | | | | | | | | | |
| Father figure displaced | -0.159*** (0.038; p=<0.001) | -0.465*** (0.132; p=<0.001) | -0.207*** (0.080; p=0.010) | -0.113*** (0.042; p=0.007) | -0.193*** (0.042; p=<0.001) | 0.035 (0.028; p=0.209) | 0.087 (0.439; p=0.843) | -0.052 (0.033; p=0.110) | 0.046 (0.030; p=0.122) |
| Mean among controls | 11.007 | 14.640 | 0.109 | 0.062 | 10.699 | 0.622 | 36.557 | 0.547 | 0.249 |
| N (children) | 3,601 | 3,601 | 2,945 | 2,920 | 3,356 | 3,547 | 3,601 | 3,405 | 3,401 |
|   of which father figure displaced | 788 | 788 | 589 | 581 | 716 | 771 | 788 | 730 | 729 |
| Clusters (fam68) | 1,129 | 1,129 | 1,017 | 1,014 | 1,095 | 1,119 | 1,129 | 1,094 | 1,094 |
| **Pooled: closures only, adult-outcome sample** | | | | | | | | | |
| Father figure displaced | -0.163*** (0.030; p=<0.001) | -0.420*** (0.108; p=<0.001) | -0.170*** (0.059; p=0.004) | -0.113*** (0.035; p=0.001) | -0.200*** (0.033; p=<0.001) | 0.038* (0.023; p=0.098) | -0.329 (0.400; p=0.411) | -0.037 (0.025; p=0.141) | 0.032 (0.025; p=0.196) |
| Mean among controls | 10.867 | 14.120 | 0.113 | 0.068 | 10.556 | 0.636 | 36.907 | 0.445 | 0.265 |
| N (children) | 5,387 | 5,388 | 4,235 | 4,195 | 4,944 | 5,270 | 5,388 | 5,043 | 5,031 |
|   of which father figure displaced | 1,194 | 1,194 | 875 | 867 | 1,078 | 1,155 | 1,194 | 1,101 | 1,097 |
| Clusters (fam68) | 1,665 | 1,665 | 1,470 | 1,463 | 1,597 | 1,645 | 1,665 | 1,608 | 1,606 |
| **Black: closure or layoff, CDS sample** | | | | | | | | | |
| Father figure displaced | -0.307*** (0.053; p=<0.001) | -0.589*** (0.137; p=<0.001) | 0.066 (0.087; p=0.446) | 0.012 (0.103; p=0.907) | -0.486*** (0.068; p=<0.001) | 0.046 (0.028; p=0.101) | -1.812*** (0.532; p=<0.001) | -0.064** (0.027; p=0.019) | 0.030 (0.029; p=0.295) |
| Mean among controls | 10.602 | 14.364 | 0.154 | 0.139 | 10.170 | 0.774 | 34.541 | 0.273 | 0.224 |
| N (children x tests) | 2,418 | 2,419 | 1,721 | 1,673 | 2,156 | 2,206 | 2,419 | 2,415 | 2,415 |
|   of which father figure displaced | 950 | 951 | 649 | 617 | 835 | 818 | 951 | 951 | 948 |
| Clusters (fam68) | 453 | 453 | 396 | 391 | 435 | 439 | 453 | 453 | 453 |
| **White: closure or layoff, CDS sample** | | | | | | | | | |
| Father figure displaced | -0.260*** (0.037; p=<0.001) | -0.759*** (0.109; p=<0.001) | 0.068* (0.037; p=0.066) | -0.003 (0.048; p=0.953) | -0.203*** (0.044; p=<0.001) | 0.009 (0.025; p=0.707) | -0.856** (0.406; p=0.035) | -0.167*** (0.028; p=<0.001) | 0.063*** (0.023; p=0.007) |
| Mean among controls | 10.986 | 15.354 | 0.057 | 0.162 | 10.508 | 0.724 | 34.109 | 0.561 | 0.193 |
| N (children x tests) | 5,347 | 5,347 | 4,620 | 4,551 | 5,113 | 5,269 | 5,347 | 5,339 | 5,342 |
|   of which father figure displaced | 1,341 | 1,341 | 1,022 | 999 | 1,219 | 1,303 | 1,341 | 1,341 | 1,341 |
| Clusters (fam68) | 874 | 874 | 830 | 825 | 855 | 868 | 874 | 874 | 874 |
| **Pooled: closure or layoff, CDS sample** | | | | | | | | | |
| Father figure displaced | -0.282*** (0.031; p=<0.001) | -0.704*** (0.084; p=<0.001) | 0.071* (0.039; p=0.069) | 0.007 (0.048; p=0.883) | -0.310*** (0.038; p=<0.001) | 0.023 (0.019; p=0.220) | -1.326*** (0.324; p=<0.001) | -0.130*** (0.020; p=<0.001) | 0.050*** (0.018; p=0.006) |
| Mean among controls | 10.883 | 15.088 | 0.079 | 0.157 | 10.423 | 0.737 | 34.225 | 0.484 | 0.201 |
| N (children x tests) | 7,765 | 7,766 | 6,341 | 6,224 | 7,269 | 7,475 | 7,766 | 7,754 | 7,757 |
|   of which father figure displaced | 2,291 | 2,292 | 1,671 | 1,616 | 2,054 | 2,121 | 2,292 | 2,292 | 2,289 |
| Clusters (fam68) | 1,293 | 1,293 | 1,205 | 1,195 | 1,259 | 1,278 | 1,293 | 1,293 | 1,293 |
| Fixed effects | birth year (+ CDS wave) | birth year (+ CDS wave) | birth year (+ CDS wave) | birth year (+ CDS wave) | birth year (+ CDS wave) | birth year (+ CDS wave) | birth year (+ CDS wave) | birth year (+ CDS wave) | birth year (+ CDS wave) |

### 3d. Controlling for the father's pre-displacement trajectory, occupation and industry

Exposure at 0-17 (Section 1 / 19 designs); the same sample in the three rows of a panel (children with the trajectory variables observed). Baseline = 19's controls; + pre-trend = the father's family-income and labor-income growth over the 3 years before and his log labor income at d-2/d-3; + occupation / industry = 8 occupation and 10 industry groups of his job in the latest interview in d-3..d (missing = own group). Codes: 1970 Census (1968-2001), 2000 Census (2003-15), 2010 / 2012 Census (2017-23).

| | Log lifetime earnings | Log lifetime family income | Earnings rank (0-100) | Family income rank (0-100) | Years of schooling |
|---|---|---|---|---|---|
| **Black, closure or layoff: baseline** | | | | | |
| Father figure displaced | -0.043 (0.075; p=0.566) | -0.049 (0.057; p=0.391) | -3.774* (2.070; p=0.068) | -3.471* (1.975; p=0.079) | -0.251** (0.110; p=0.022) |
| Mean of outcome | 9.696 | 10.315 | 44.543 | 39.902 | 13.207 |
| N (children) | 922 | 935 | 922 | 935 | 1,870 |
|   of which father figure displaced | 454 | 464 | 454 | 464 | 974 |
| Clusters (fam68) | 347 | 348 | 347 | 348 | 536 |
| **Black, closure or layoff: + pre-trend** | | | | | |
| Father figure displaced | -0.015 (0.079; p=0.844) | -0.037 (0.057; p=0.519) | -3.640* (2.082; p=0.080) | -3.504* (1.986; p=0.078) | -0.246** (0.111; p=0.026) |
| Father's family-income growth, 3 yrs before (log) | -0.045 (0.072; p=0.537) | 0.001 (0.049; p=0.982) | -1.732 (1.778; p=0.330) | -0.305 (1.586; p=0.847) | -0.171** (0.080; p=0.032) |
| Father's labor-income growth, 3 yrs before (log) | -0.047 (0.076; p=0.535) | -0.059 (0.039; p=0.131) | -0.744 (1.745; p=0.670) | -1.108 (1.459; p=0.448) | 0.008 (0.069; p=0.907) |
| Log father's labor income, d-2/d-3 | 0.194* (0.113; p=0.086) | 0.090 (0.069; p=0.191) | 0.974 (2.492; p=0.696) | -0.007 (2.293; p=0.997) | 0.060 (0.104; p=0.561) |
| Mean of outcome | 9.696 | 10.315 | 44.543 | 39.902 | 13.207 |
| N (children) | 922 | 935 | 922 | 935 | 1,870 |
|   of which father figure displaced | 454 | 464 | 454 | 464 | 974 |
| Clusters (fam68) | 347 | 348 | 347 | 348 | 536 |
| **Black, closure or layoff: + pre-trend + occupation / industry** | | | | | |
| Father figure displaced | -0.034 (0.082; p=0.679) | -0.044 (0.057; p=0.440) | -3.983* (2.168; p=0.066) | -3.717* (1.981; p=0.061) | -0.253** (0.117; p=0.030) |
| Father's family-income growth, 3 yrs before (log) | -0.050 (0.072; p=0.490) | 0.009 (0.050; p=0.861) | -1.801 (1.865; p=0.334) | -0.120 (1.657; p=0.942) | -0.163* (0.083; p=0.050) |
| Father's labor-income growth, 3 yrs before (log) | -0.039 (0.075; p=0.607) | -0.056 (0.040; p=0.155) | -0.516 (1.784; p=0.772) | -0.975 (1.485; p=0.511) | 0.016 (0.070; p=0.819) |
| Log father's labor income, d-2/d-3 | 0.169 (0.109; p=0.122) | 0.095 (0.067; p=0.154) | 0.823 (2.461; p=0.738) | 0.329 (2.201; p=0.881) | 0.051 (0.104; p=0.627) |
| Mean of outcome | 9.696 | 10.315 | 44.543 | 39.902 | 13.207 |
| N (children) | 922 | 935 | 922 | 935 | 1,870 |
|   of which father figure displaced | 454 | 464 | 454 | 464 | 974 |
| Clusters (fam68) | 347 | 348 | 347 | 348 | 536 |
| **White, closure or layoff: baseline** | | | | | |
| Father figure displaced | -0.135*** (0.043; p=0.002) | -0.089*** (0.030; p=0.003) | -4.366*** (1.276; p=<0.001) | -3.925*** (1.212; p=0.001) | -0.521*** (0.088; p=<0.001) |
| Mean of outcome | 10.170 | 10.936 | 59.176 | 63.388 | 14.053 |
| N (children) | 2,408 | 2,430 | 2,408 | 2,430 | 3,796 |
|   of which father figure displaced | 979 | 992 | 979 | 992 | 1,596 |
| Clusters (fam68) | 882 | 886 | 882 | 886 | 1,158 |
| **White, closure or layoff: + pre-trend** | | | | | |
| Father figure displaced | -0.131*** (0.043; p=0.002) | -0.086*** (0.029; p=0.003) | -4.294*** (1.267; p=<0.001) | -3.797*** (1.202; p=0.002) | -0.517*** (0.088; p=<0.001) |
| Father's family-income growth, 3 yrs before (log) | -0.074*** (0.019; p=<0.001) | -0.028** (0.013; p=0.030) | -2.414*** (0.627; p=<0.001) | -1.016* (0.536; p=0.058) | -0.092** (0.038; p=0.016) |
| Father's labor-income growth, 3 yrs before (log) | 0.117*** (0.040; p=0.003) | 0.049** (0.025; p=0.045) | 3.206*** (1.067; p=0.003) | 1.678* (0.954; p=0.078) | 0.043 (0.057; p=0.452) |
| Log father's labor income, d-2/d-3 | 0.104 (0.065; p=0.112) | 0.104** (0.049; p=0.033) | 2.842 (2.036; p=0.163) | 4.222** (1.963; p=0.032) | 0.194** (0.093; p=0.036) |
| Mean of outcome | 10.170 | 10.936 | 59.176 | 63.388 | 14.053 |
| N (children) | 2,408 | 2,430 | 2,408 | 2,430 | 3,796 |
|   of which father figure displaced | 979 | 992 | 979 | 992 | 1,596 |
| Clusters (fam68) | 882 | 886 | 882 | 886 | 1,158 |
| **White, closure or layoff: + pre-trend + occupation / industry** | | | | | |
| Father figure displaced | -0.134*** (0.044; p=0.002) | -0.080*** (0.029; p=0.007) | -4.388*** (1.290; p=<0.001) | -3.484*** (1.216; p=0.004) | -0.480*** (0.089; p=<0.001) |
| Father's family-income growth, 3 yrs before (log) | -0.073*** (0.020; p=<0.001) | -0.023* (0.013; p=0.077) | -2.307*** (0.634; p=<0.001) | -0.769 (0.541; p=0.155) | -0.087** (0.040; p=0.030) |
| Father's labor-income growth, 3 yrs before (log) | 0.119*** (0.040; p=0.003) | 0.051** (0.025; p=0.039) | 3.182*** (1.073; p=0.003) | 1.655* (0.953; p=0.083) | 0.044 (0.057; p=0.432) |
| Log father's labor income, d-2/d-3 | 0.119* (0.065; p=0.068) | 0.121*** (0.047; p=0.010) | 3.244 (1.995; p=0.104) | 4.740** (1.884; p=0.012) | 0.188** (0.094; p=0.046) |
| Mean of outcome | 10.170 | 10.936 | 59.176 | 63.388 | 14.053 |
| N (children) | 2,408 | 2,430 | 2,408 | 2,430 | 3,796 |
|   of which father figure displaced | 979 | 992 | 979 | 992 | 1,596 |
| Clusters (fam68) | 882 | 886 | 882 | 886 | 1,158 |
| **Pooled, closure or layoff: baseline** | | | | | |
| Father figure displaced | -0.106*** (0.038; p=0.005) | -0.078*** (0.027; p=0.003) | -4.151*** (1.103; p=<0.001) | -3.812*** (1.036; p=<0.001) | -0.430*** (0.069; p=<0.001) |
| Mean of outcome | 10.038 | 10.764 | 55.124 | 56.862 | 13.774 |
| N (children) | 3,330 | 3,365 | 3,330 | 3,365 | 5,666 |
|   of which father figure displaced | 1,433 | 1,456 | 1,433 | 1,456 | 2,570 |
| Clusters (fam68) | 1,223 | 1,228 | 1,223 | 1,228 | 1,683 |
| **Pooled, closure or layoff: + pre-trend** | | | | | |
| Father figure displaced | -0.100*** (0.038; p=0.008) | -0.073*** (0.027; p=0.006) | -4.076*** (1.102; p=<0.001) | -3.674*** (1.035; p=<0.001) | -0.424*** (0.069; p=<0.001) |
| Father's family-income growth, 3 yrs before (log) | -0.071*** (0.020; p=<0.001) | -0.025* (0.014; p=0.068) | -2.316*** (0.592; p=<0.001) | -0.942* (0.533; p=0.077) | -0.107*** (0.035; p=0.002) |
| Father's labor-income growth, 3 yrs before (log) | 0.065* (0.036; p=0.069) | 0.012 (0.020; p=0.563) | 1.704* (0.885; p=0.054) | 0.520 (0.764; p=0.496) | 0.010 (0.043; p=0.811) |
| Log father's labor income, d-2/d-3 | 0.120** (0.059; p=0.041) | 0.092** (0.044; p=0.036) | 2.049 (1.696; p=0.227) | 2.814* (1.698; p=0.098) | 0.137** (0.069; p=0.047) |
| Mean of outcome | 10.038 | 10.764 | 55.124 | 56.862 | 13.774 |
| N (children) | 3,330 | 3,365 | 3,330 | 3,365 | 5,666 |
|   of which father figure displaced | 1,433 | 1,456 | 1,433 | 1,456 | 2,570 |
| Clusters (fam68) | 1,223 | 1,228 | 1,223 | 1,228 | 1,683 |
| **Pooled, closure or layoff: + pre-trend + occupation / industry** | | | | | |
| Father figure displaced | -0.099** (0.039; p=0.010) | -0.071*** (0.027; p=0.008) | -4.084*** (1.109; p=<0.001) | -3.576*** (1.038; p=<0.001) | -0.402*** (0.070; p=<0.001) |
| Father's family-income growth, 3 yrs before (log) | -0.069*** (0.020; p=<0.001) | -0.023* (0.014; p=0.096) | -2.255*** (0.594; p=<0.001) | -0.825 (0.529; p=0.119) | -0.102*** (0.036; p=0.005) |
| Father's labor-income growth, 3 yrs before (log) | 0.065* (0.036; p=0.071) | 0.012 (0.020; p=0.541) | 1.722* (0.880; p=0.051) | 0.522 (0.760; p=0.492) | 0.009 (0.043; p=0.836) |
| Log father's labor income, d-2/d-3 | 0.127** (0.058; p=0.029) | 0.101** (0.043; p=0.020) | 2.314 (1.666; p=0.165) | 3.067* (1.659; p=0.065) | 0.137** (0.069; p=0.047) |
| Mean of outcome | 10.038 | 10.764 | 55.124 | 56.862 | 13.774 |
| N (children) | 3,330 | 3,365 | 3,330 | 3,365 | 5,666 |
|   of which father figure displaced | 1,433 | 1,456 | 1,433 | 1,456 | 2,570 |
| Clusters (fam68) | 1,223 | 1,228 | 1,223 | 1,228 | 1,683 |
| **Black, closures only: baseline** | | | | | |
| Father figure displaced | 0.087 (0.090; p=0.333) | 0.047 (0.072; p=0.512) | -1.584 (2.664; p=0.552) | -0.697 (2.646; p=0.792) | 0.051 (0.169; p=0.762) |
| Mean of outcome | 9.840 | 10.390 | 48.210 | 42.614 | 13.391 |
| N (children) | 652 | 657 | 652 | 657 | 1,267 |
|   of which father figure displaced | 147 | 149 | 147 | 149 | 285 |
| Clusters (fam68) | 294 | 297 | 294 | 297 | 451 |
| **Black, closures only: + pre-trend** | | | | | |
| Father figure displaced | 0.086 (0.092; p=0.345) | 0.049 (0.073; p=0.500) | -1.616 (2.662; p=0.544) | -0.679 (2.655; p=0.798) | 0.053 (0.167; p=0.751) |
| Father's family-income growth, 3 yrs before (log) | -0.051 (0.056; p=0.358) | -0.060 (0.039; p=0.126) | -2.620* (1.449; p=0.071) | -1.934 (1.526; p=0.205) | -0.330*** (0.114; p=0.004) |
| Father's labor-income growth, 3 yrs before (log) | -0.063 (0.077; p=0.413) | -0.049 (0.057; p=0.397) | 0.281 (1.731; p=0.871) | -0.370 (1.767; p=0.834) | 0.101 (0.124; p=0.413) |
| Log father's labor income, d-2/d-3 | 0.009 (0.102; p=0.928) | 0.041 (0.084; p=0.621) | -0.280 (2.904; p=0.923) | 0.567 (3.102; p=0.855) | 0.067 (0.187; p=0.719) |
| Mean of outcome | 9.840 | 10.390 | 48.210 | 42.614 | 13.391 |
| N (children) | 652 | 657 | 652 | 657 | 1,267 |
|   of which father figure displaced | 147 | 149 | 147 | 149 | 285 |
| Clusters (fam68) | 294 | 297 | 294 | 297 | 451 |
| **Black, closures only: + pre-trend + occupation / industry** | | | | | |
| Father figure displaced | 0.101 (0.096; p=0.295) | 0.054 (0.076; p=0.480) | -1.288 (2.729; p=0.637) | -0.637 (2.626; p=0.808) | 0.092 (0.171; p=0.592) |
| Father's family-income growth, 3 yrs before (log) | -0.068 (0.057; p=0.233) | -0.053 (0.041; p=0.195) | -2.788* (1.497; p=0.063) | -1.516 (1.500; p=0.312) | -0.318*** (0.115; p=0.006) |
| Father's labor-income growth, 3 yrs before (log) | -0.041 (0.076; p=0.588) | -0.047 (0.060; p=0.428) | 0.805 (1.777; p=0.650) | -0.260 (1.924; p=0.893) | 0.100 (0.122; p=0.416) |
| Log father's labor income, d-2/d-3 | -0.016 (0.104; p=0.877) | 0.032 (0.082; p=0.694) | -0.547 (2.992; p=0.855) | 0.905 (3.048; p=0.767) | 0.099 (0.190; p=0.601) |
| Mean of outcome | 9.840 | 10.390 | 48.210 | 42.614 | 13.391 |
| N (children) | 652 | 657 | 652 | 657 | 1,267 |
|   of which father figure displaced | 147 | 149 | 147 | 149 | 285 |
| Clusters (fam68) | 294 | 297 | 294 | 297 | 451 |
| **White, closures only: baseline** | | | | | |
| Father figure displaced | -0.061 (0.060; p=0.305) | 0.015 (0.043; p=0.730) | -2.734 (1.841; p=0.138) | -0.499 (1.691; p=0.768) | -0.415*** (0.128; p=0.001) |
| Mean of outcome | 10.237 | 10.998 | 61.494 | 65.959 | 14.253 |
| N (children) | 1,863 | 1,874 | 1,863 | 1,874 | 2,911 |
|   of which father figure displaced | 344 | 346 | 344 | 346 | 580 |
| Clusters (fam68) | 767 | 771 | 767 | 771 | 1,012 |
| **White, closures only: + pre-trend** | | | | | |
| Father figure displaced | -0.063 (0.060; p=0.289) | 0.024 (0.043; p=0.567) | -2.995 (1.826; p=0.101) | -0.157 (1.667; p=0.925) | -0.393*** (0.127; p=0.002) |
| Father's family-income growth, 3 yrs before (log) | -0.045 (0.033; p=0.179) | 0.011 (0.019; p=0.553) | -1.950** (0.958; p=0.042) | 0.405 (0.659; p=0.539) | -0.006 (0.060; p=0.918) |
| Father's labor-income growth, 3 yrs before (log) | -0.030 (0.041; p=0.467) | 0.000 (0.027; p=0.987) | -1.158 (1.303; p=0.374) | -0.178 (1.089; p=0.870) | 0.050 (0.066; p=0.453) |
| Log father's labor income, d-2/d-3 | 0.203** (0.080; p=0.011) | 0.172*** (0.052; p=<0.001) | 4.436** (2.240; p=0.048) | 6.366*** (2.052; p=0.002) | 0.340*** (0.106; p=0.001) |
| Mean of outcome | 10.237 | 10.998 | 61.494 | 65.959 | 14.253 |
| N (children) | 1,863 | 1,874 | 1,863 | 1,874 | 2,911 |
|   of which father figure displaced | 344 | 346 | 344 | 346 | 580 |
| Clusters (fam68) | 767 | 771 | 767 | 771 | 1,012 |
| **White, closures only: + pre-trend + occupation / industry** | | | | | |
| Father figure displaced | -0.053 (0.062; p=0.390) | 0.037 (0.044; p=0.394) | -2.793 (1.838; p=0.129) | 0.380 (1.715; p=0.824) | -0.352*** (0.130; p=0.007) |
| Father's family-income growth, 3 yrs before (log) | -0.043 (0.033; p=0.195) | 0.014 (0.018; p=0.420) | -1.900** (0.958; p=0.047) | 0.521 (0.576; p=0.366) | -0.003 (0.061; p=0.963) |
| Father's labor-income growth, 3 yrs before (log) | -0.030 (0.042; p=0.476) | 0.002 (0.027; p=0.952) | -1.190 (1.321; p=0.367) | -0.154 (1.101; p=0.889) | 0.046 (0.065; p=0.480) |
| Log father's labor income, d-2/d-3 | 0.219*** (0.082; p=0.007) | 0.186*** (0.054; p=<0.001) | 4.586** (2.297; p=0.046) | 6.721*** (2.071; p=0.001) | 0.346*** (0.109; p=0.002) |
| Mean of outcome | 10.237 | 10.998 | 61.494 | 65.959 | 14.253 |
| N (children) | 1,863 | 1,874 | 1,863 | 1,874 | 2,911 |
|   of which father figure displaced | 344 | 346 | 344 | 346 | 580 |
| Clusters (fam68) | 767 | 771 | 767 | 771 | 1,012 |
| **Pooled, closures only: baseline** | | | | | |
| Father figure displaced | -0.010 (0.050; p=0.848) | 0.029 (0.037; p=0.435) | -2.015 (1.546; p=0.192) | -0.276 (1.421; p=0.846) | -0.251** (0.103; p=0.015) |
| Mean of outcome | 10.134 | 10.840 | 58.050 | 59.900 | 13.992 |
| N (children) | 2,515 | 2,531 | 2,515 | 2,531 | 4,178 |
|   of which father figure displaced | 491 | 495 | 491 | 495 | 865 |
| Clusters (fam68) | 1,059 | 1,066 | 1,059 | 1,066 | 1,459 |
| **Pooled, closures only: + pre-trend** | | | | | |
| Father figure displaced | -0.012 (0.050; p=0.816) | 0.034 (0.037; p=0.347) | -2.235 (1.544; p=0.148) | -0.055 (1.412; p=0.969) | -0.240** (0.102; p=0.019) |
| Father's family-income growth, 3 yrs before (log) | -0.050* (0.029; p=0.091) | -0.004 (0.019; p=0.844) | -2.173** (0.847; p=0.010) | -0.106 (0.649; p=0.870) | -0.049 (0.057; p=0.384) |
| Father's labor-income growth, 3 yrs before (log) | -0.040 (0.038; p=0.292) | -0.017 (0.027; p=0.530) | -0.787 (1.084; p=0.468) | -0.392 (0.949; p=0.680) | 0.033 (0.060; p=0.580) |
| Log father's labor income, d-2/d-3 | 0.148** (0.072; p=0.039) | 0.142*** (0.049; p=0.004) | 3.052 (1.983; p=0.124) | 5.057*** (1.890; p=0.007) | 0.234** (0.093; p=0.012) |
| Mean of outcome | 10.134 | 10.840 | 58.050 | 59.900 | 13.992 |
| N (children) | 2,515 | 2,531 | 2,515 | 2,531 | 4,178 |
|   of which father figure displaced | 491 | 495 | 491 | 495 | 865 |
| Clusters (fam68) | 1,059 | 1,066 | 1,059 | 1,066 | 1,459 |
| **Pooled, closures only: + pre-trend + occupation / industry** | | | | | |
| Father figure displaced | 0.005 (0.052; p=0.920) | 0.047 (0.038; p=0.212) | -1.885 (1.550; p=0.224) | 0.323 (1.442; p=0.823) | -0.201* (0.103; p=0.051) |
| Father's family-income growth, 3 yrs before (log) | -0.050* (0.030; p=0.093) | -0.002 (0.018; p=0.905) | -2.146** (0.851; p=0.012) | -0.036 (0.611; p=0.953) | -0.044 (0.056; p=0.437) |
| Father's labor-income growth, 3 yrs before (log) | -0.037 (0.038; p=0.330) | -0.014 (0.027; p=0.593) | -0.737 (1.091; p=0.499) | -0.285 (0.954; p=0.765) | 0.030 (0.058; p=0.600) |
| Log father's labor income, d-2/d-3 | 0.157** (0.073; p=0.032) | 0.151*** (0.050; p=0.003) | 3.062 (2.023; p=0.130) | 5.294*** (1.908; p=0.006) | 0.243** (0.095; p=0.010) |
| Mean of outcome | 10.134 | 10.840 | 58.050 | 59.900 | 13.992 |
| N (children) | 2,515 | 2,531 | 2,515 | 2,531 | 4,178 |
|   of which father figure displaced | 491 | 495 | 491 | 495 | 865 |
| Clusters (fam68) | 1,059 | 1,066 | 1,059 | 1,066 | 1,459 |
| Fixed effects | birth year (+ occupation and industry groups in the third row) | birth year (+ occupation and industry groups in the third row) | birth year (+ occupation and industry groups in the third row) | birth year (+ occupation and industry groups in the third row) | birth year (+ occupation and industry groups in the third row) |
| Other controls | log pre-event family income, parental education, female | log pre-event family income, parental education, female | log pre-event family income, parental education, female | log pre-event family income, parental education, female | log pre-event family income, parental education, female |

## 4. Severity: dose-response and receipt of UI / food stamps

Exposure at 0-17, closure or layoff (19's design). Relative earnings loss = father's mean labor income over d+1..d+3 divided by his mean over d-3..d-2, minus 1 (zeros kept; the event-study reference window); 'above median' = a larger loss than the median among the treated of the sample (pooled across race). Receipt = the head's unemployment compensation > 0 (before 1977 the item includes workers' compensation and, 1970-74, other family members; no item for calendar 1967-68, 1972, 1974) / the family's food stamps in d or d+1. Treated children with the split variable missing are dropped. Receipt is chosen by the family and reflects eligibility, so the receipt splits describe who is hurt; they do not identify the effect of the transfer.

- Adult-outcome sample: median relative loss among the treated -0.088 (Black -0.135, White -0.064); share receiving UI Black 0.322, White 0.407; food stamps Black 0.374, White 0.215.
- CDS sample: median relative loss among the treated -0.028 (Black -0.096, White 0.004); share receiving UI Black 0.282, White 0.355; food stamps Black 0.417, White 0.216.

### 4a. Adult outcomes

| | Log lifetime earnings | Log lifetime family income | Earnings rank (0-100) | Family income rank (0-100) | Years of schooling |
|---|---|---|---|---|---|
| **Black: split by relative earnings loss** | | | | | |
| Displaced, earnings loss above median | -0.100 (0.077; p=0.197) | -0.059 (0.057; p=0.295) | -5.087** (2.101; p=0.015) | -3.730* (1.960; p=0.057) | -0.285*** (0.106; p=0.007) |
| Displaced, earnings loss below median | 0.030 (0.090; p=0.743) | 0.005 (0.060; p=0.937) | 0.311 (2.184; p=0.887) | -0.988 (2.020; p=0.625) | -0.149 (0.114; p=0.189) |
| Difference: Displaced, earnings loss above median minus Displaced, earnings loss below median | -0.129 (0.094; p=0.169) | -0.064 (0.063; p=0.314) | -5.398** (2.363; p=0.022) | -2.742 (2.174; p=0.207) | -0.135 (0.117; p=0.247) |
| Mean of outcome | 9.705 | 10.301 | 45.103 | 39.516 | 13.181 |
| N (children) | 1,256 | 1,275 | 1,256 | 1,275 | 2,502 |
|   of which displaced, earnings loss above median | 301 | 309 | 301 | 309 | 663 |
|   of which displaced, earnings loss below median | 294 | 300 | 294 | 300 | 574 |
| Clusters (fam68) | 434 | 437 | 434 | 437 | 623 |
| **White: split by relative earnings loss** | | | | | |
| Displaced, earnings loss above median | -0.100** (0.047; p=0.033) | -0.084*** (0.032; p=0.009) | -3.415** (1.339; p=0.011) | -3.754*** (1.335; p=0.005) | -0.559*** (0.098; p=<0.001) |
| Displaced, earnings loss below median | -0.108** (0.049; p=0.027) | -0.062* (0.031; p=0.050) | -3.549** (1.427; p=0.013) | -3.065** (1.294; p=0.018) | -0.388*** (0.095; p=<0.001) |
| Difference: Displaced, earnings loss above median minus Displaced, earnings loss below median | 0.008 (0.056; p=0.888) | -0.022 (0.037; p=0.549) | 0.134 (1.613; p=0.934) | -0.689 (1.543; p=0.655) | -0.171 (0.113; p=0.129) |
| Mean of outcome | 10.134 | 10.916 | 58.437 | 62.881 | 13.994 |
| N (children) | 2,953 | 2,981 | 2,953 | 2,981 | 4,573 |
|   of which displaced, earnings loss above median | 576 | 583 | 576 | 583 | 941 |
|   of which displaced, earnings loss below median | 647 | 654 | 647 | 654 | 1,011 |
| Clusters (fam68) | 1,011 | 1,017 | 1,011 | 1,017 | 1,272 |
| **Pooled: split by relative earnings loss** | | | | | |
| Displaced, earnings loss above median | -0.096** (0.040; p=0.017) | -0.076*** (0.029; p=0.008) | -3.780*** (1.136; p=<0.001) | -3.705*** (1.111; p=<0.001) | -0.451*** (0.073; p=<0.001) |
| Displaced, earnings loss below median | -0.065 (0.043; p=0.133) | -0.040 (0.028; p=0.151) | -2.413** (1.196; p=0.044) | -2.465** (1.079; p=0.022) | -0.301*** (0.074; p=<0.001) |
| Difference: Displaced, earnings loss above median minus Displaced, earnings loss below median | -0.030 (0.048; p=0.530) | -0.035 (0.032; p=0.273) | -1.366 (1.310; p=0.297) | -1.239 (1.242; p=0.318) | -0.149* (0.084; p=0.074) |
| Mean of outcome | 10.006 | 10.731 | 54.458 | 55.882 | 13.706 |
| N (children) | 4,209 | 4,256 | 4,209 | 4,256 | 7,075 |
|   of which displaced, earnings loss above median | 877 | 892 | 877 | 892 | 1,604 |
|   of which displaced, earnings loss below median | 941 | 954 | 941 | 954 | 1,585 |
| Clusters (fam68) | 1,439 | 1,448 | 1,439 | 1,448 | 1,885 |
| **Black: split by UI receipt** | | | | | |
| Displaced, head received UI (d or d+1) | 0.022 (0.082; p=0.791) | 0.020 (0.062; p=0.749) | -0.430 (2.239; p=0.848) | 0.155 (2.158; p=0.943) | -0.339*** (0.125; p=0.007) |
| Displaced, no UI received | -0.087 (0.077; p=0.256) | -0.087 (0.054; p=0.107) | -4.327** (1.933; p=0.025) | -4.583** (1.788; p=0.010) | -0.216** (0.092; p=0.019) |
| Difference: Displaced, head received UI (d or d+1) minus Displaced, no UI received | 0.109 (0.084; p=0.198) | 0.106 (0.065; p=0.102) | 3.897* (2.283; p=0.088) | 4.739** (2.265; p=0.036) | -0.123 (0.121; p=0.310) |
| Mean of outcome | 9.678 | 10.275 | 44.155 | 38.680 | 13.118 |
| N (children) | 1,402 | 1,424 | 1,402 | 1,424 | 2,776 |
|   of which displaced, head received ui (d or d+1) | 244 | 251 | 244 | 251 | 543 |
|   of which displaced, no ui received | 497 | 507 | 497 | 507 | 968 |
| Clusters (fam68) | 456 | 459 | 456 | 459 | 647 |
| **White: split by UI receipt** | | | | | |
| Displaced, head received UI (d or d+1) | -0.093** (0.046; p=0.041) | -0.089*** (0.032; p=0.005) | -3.403** (1.351; p=0.012) | -4.019*** (1.324; p=0.002) | -0.455*** (0.097; p=<0.001) |
| Displaced, no UI received | -0.133*** (0.047; p=0.005) | -0.090*** (0.031; p=0.004) | -4.377*** (1.362; p=0.001) | -4.045*** (1.269; p=0.001) | -0.555*** (0.088; p=<0.001) |
| Difference: Displaced, head received UI (d or d+1) minus Displaced, no UI received | 0.040 (0.054; p=0.459) | 0.001 (0.035; p=0.975) | 0.974 (1.565; p=0.534) | 0.026 (1.464; p=0.986) | 0.100 (0.107; p=0.350) |
| Mean of outcome | 10.107 | 10.896 | 57.731 | 62.170 | 13.926 |
| N (children) | 3,118 | 3,152 | 3,118 | 3,152 | 4,855 |
|   of which displaced, head received ui (d or d+1) | 626 | 636 | 626 | 636 | 994 |
|   of which displaced, no ui received | 762 | 772 | 762 | 772 | 1,240 |
| Clusters (fam68) | 1,041 | 1,048 | 1,041 | 1,048 | 1,295 |
| **Pooled: split by UI receipt** | | | | | |
| Displaced, head received UI (d or d+1) | -0.058 (0.039; p=0.143) | -0.055* (0.029; p=0.052) | -2.444** (1.155; p=0.034) | -2.782** (1.123; p=0.013) | -0.416*** (0.078; p=<0.001) |
| Displaced, no UI received | -0.115*** (0.041; p=0.005) | -0.091*** (0.028; p=0.001) | -4.321*** (1.126; p=<0.001) | -4.361*** (1.044; p=<0.001) | -0.417*** (0.065; p=<0.001) |
| Difference: Displaced, head received UI (d or d+1) minus Displaced, no UI received | 0.057 (0.045; p=0.207) | 0.036 (0.032; p=0.256) | 1.877 (1.281; p=0.143) | 1.579 (1.227; p=0.198) | 0.001 (0.082; p=0.989) |
| Mean of outcome | 9.974 | 10.703 | 53.520 | 54.860 | 13.632 |
| N (children) | 4,520 | 4,576 | 4,520 | 4,576 | 7,631 |
|   of which displaced, head received ui (d or d+1) | 870 | 887 | 870 | 887 | 1,537 |
|   of which displaced, no ui received | 1,259 | 1,279 | 1,259 | 1,279 | 2,208 |
| Clusters (fam68) | 1,490 | 1,500 | 1,490 | 1,500 | 1,930 |
| **Black: split by food-stamp receipt** | | | | | |
| Displaced, family received food stamps (d or d+1) | -0.108 (0.097; p=0.267) | -0.055 (0.061; p=0.372) | -4.302* (2.310; p=0.063) | -3.597* (2.024; p=0.076) | -0.337*** (0.123; p=0.006) |
| Displaced, no food stamps | -0.020 (0.067; p=0.763) | -0.049 (0.052; p=0.346) | -2.385 (1.842; p=0.195) | -2.684 (1.778; p=0.131) | -0.240** (0.094; p=0.011) |
| Difference: Displaced, family received food stamps (d or d+1) minus Displaced, no food stamps | -0.087 (0.088; p=0.321) | -0.005 (0.061; p=0.930) | -1.917 (2.190; p=0.381) | -0.912 (2.045; p=0.655) | -0.097 (0.120; p=0.417) |
| Mean of outcome | 9.672 | 10.270 | 43.986 | 38.507 | 13.114 |
| N (children) | 1,413 | 1,436 | 1,413 | 1,436 | 2,794 |
|   of which displaced, family received food stamps (d or d+1) | 279 | 290 | 279 | 290 | 579 |
|   of which displaced, no food stamps | 473 | 480 | 473 | 480 | 950 |
| Clusters (fam68) | 458 | 461 | 458 | 461 | 647 |
| **White: split by food-stamp receipt** | | | | | |
| Displaced, family received food stamps (d or d+1) | -0.204*** (0.069; p=0.003) | -0.224*** (0.045; p=<0.001) | -6.697*** (2.004; p=<0.001) | -9.817*** (1.881; p=<0.001) | -0.594*** (0.143; p=<0.001) |
| Displaced, no food stamps | -0.096** (0.039; p=0.015) | -0.063** (0.027; p=0.020) | -3.366*** (1.156; p=0.004) | -2.926*** (1.110; p=0.008) | -0.492*** (0.078; p=<0.001) |
| Difference: Displaced, family received food stamps (d or d+1) minus Displaced, no food stamps | -0.108 (0.069; p=0.116) | -0.161*** (0.045; p=<0.001) | -3.331* (1.995; p=0.095) | -6.891*** (1.870; p=<0.001) | -0.102 (0.140; p=0.468) |
| Mean of outcome | 10.107 | 10.896 | 57.727 | 62.152 | 13.924 |
| N (children) | 3,122 | 3,156 | 3,122 | 3,156 | 4,864 |
|   of which displaced, family received food stamps (d or d+1) | 269 | 276 | 269 | 276 | 427 |
|   of which displaced, no food stamps | 1,123 | 1,136 | 1,123 | 1,136 | 1,816 |
| Clusters (fam68) | 1,042 | 1,049 | 1,042 | 1,049 | 1,297 |
| **Pooled: split by food-stamp receipt** | | | | | |
| Displaced, family received food stamps (d or d+1) | -0.156*** (0.057; p=0.006) | -0.144*** (0.038; p=<0.001) | -5.474*** (1.511; p=<0.001) | -6.884*** (1.408; p=<0.001) | -0.473*** (0.093; p=<0.001) |
| Displaced, no food stamps | -0.072** (0.034; p=0.034) | -0.057** (0.024; p=0.020) | -2.996*** (0.984; p=0.002) | -2.837*** (0.940; p=0.003) | -0.403*** (0.061; p=<0.001) |
| Difference: Displaced, family received food stamps (d or d+1) minus Displaced, no food stamps | -0.084 (0.054; p=0.123) | -0.087** (0.037; p=0.020) | -2.478* (1.461; p=0.090) | -4.047*** (1.396; p=0.004) | -0.070 (0.091; p=0.443) |
| Mean of outcome | 9.972 | 10.700 | 53.446 | 54.757 | 13.628 |
| N (children) | 4,535 | 4,592 | 4,535 | 4,592 | 7,658 |
|   of which displaced, family received food stamps (d or d+1) | 548 | 566 | 548 | 566 | 1,006 |
|   of which displaced, no food stamps | 1,596 | 1,616 | 1,596 | 1,616 | 2,766 |
| Clusters (fam68) | 1,493 | 1,503 | 1,493 | 1,503 | 1,931 |
| Fixed effects | birth year | birth year | birth year | birth year | birth year |
| Other controls | log pre-event family income, parental education, female | log pre-event family income, parental education, female | log pre-event family income, parental education, female | log pre-event family income, parental education, female | log pre-event family income, parental education, female |

### 4b. CDS

| | WJ Letter-Word | WJ Applied Problems | WJ Passage Comp. | BPI (z, higher = worse) |
|---|---|---|---|---|
| **Black: split by relative earnings loss** | | | | |
| Displaced, earnings loss above median | -1.611 (1.520; p=0.289) | -2.174 (1.621; p=0.180) | -1.214 (1.391; p=0.383) | 0.079 (0.076; p=0.301) |
| Displaced, earnings loss below median | -2.336 (1.622; p=0.150) | -1.321 (1.663; p=0.427) | -0.933 (1.627; p=0.566) | 0.112 (0.079; p=0.156) |
| Difference: Displaced, earnings loss above median minus Displaced, earnings loss below median | 0.725 (1.961; p=0.711) | -0.854 (1.978; p=0.666) | -0.281 (1.948; p=0.885) | -0.033 (0.094; p=0.727) |
| Mean of outcome | 99.378 | 95.713 | 98.212 | -0.132 |
| N (children x tests) | 1,478 | 1,468 | 1,283 | 2,181 |
|   of which displaced, earnings loss above median | 257 | 256 | 228 | 389 |
|   of which displaced, earnings loss below median | 214 | 211 | 198 | 343 |
| Clusters (fam68) | 372 | 370 | 357 | 438 |
| **White: split by relative earnings loss** | | | | |
| Displaced, earnings loss above median | -0.342 (1.259; p=0.786) | -1.340 (1.172; p=0.253) | -0.790 (0.941; p=0.401) | 0.131** (0.059; p=0.027) |
| Displaced, earnings loss below median | -0.259 (1.169; p=0.825) | 0.741 (1.111; p=0.505) | 0.220 (1.095; p=0.841) | 0.073 (0.061; p=0.230) |
| Difference: Displaced, earnings loss above median minus Displaced, earnings loss below median | -0.084 (1.566; p=0.957) | -2.080 (1.456; p=0.153) | -1.010 (1.280; p=0.430) | 0.058 (0.077; p=0.452) |
| Mean of outcome | 107.856 | 108.652 | 106.905 | 0.005 |
| N (children x tests) | 3,144 | 3,135 | 2,756 | 5,108 |
|   of which displaced, earnings loss above median | 341 | 341 | 320 | 544 |
|   of which displaced, earnings loss below median | 361 | 362 | 324 | 593 |
| Clusters (fam68) | 683 | 684 | 661 | 856 |
| **Pooled: split by relative earnings loss** | | | | |
| Displaced, earnings loss above median | -0.575 (0.964; p=0.551) | -1.554 (0.954; p=0.103) | -0.782 (0.792; p=0.323) | 0.099** (0.047; p=0.036) |
| Displaced, earnings loss below median | -0.975 (0.949; p=0.304) | -0.106 (0.934; p=0.910) | -0.193 (0.918; p=0.834) | 0.080* (0.047; p=0.089) |
| Difference: Displaced, earnings loss above median minus Displaced, earnings loss below median | 0.400 (1.228; p=0.744) | -1.448 (1.201; p=0.228) | -0.590 (1.100; p=0.592) | 0.018 (0.060; p=0.760) |
| Mean of outcome | 105.145 | 104.526 | 104.143 | -0.036 |
| N (children x tests) | 4,622 | 4,603 | 4,039 | 7,289 |
|   of which displaced, earnings loss above median | 598 | 597 | 548 | 933 |
|   of which displaced, earnings loss below median | 575 | 573 | 522 | 936 |
| Clusters (fam68) | 1,041 | 1,041 | 1,007 | 1,264 |
| **Black: split by UI receipt** | | | | |
| Displaced, head received UI (d or d+1) | -3.576** (1.435; p=0.013) | -2.414 (1.741; p=0.165) | -2.382* (1.271; p=0.061) | 0.181** (0.085; p=0.032) |
| Displaced, no UI received | -0.532 (1.360; p=0.696) | -0.959 (1.383; p=0.488) | 0.178 (1.334; p=0.894) | 0.068 (0.068; p=0.317) |
| Difference: Displaced, head received UI (d or d+1) minus Displaced, no UI received | -3.044* (1.681; p=0.070) | -1.455 (1.889; p=0.441) | -2.559 (1.566; p=0.102) | 0.113 (0.095; p=0.236) |
| Mean of outcome | 99.297 | 95.674 | 98.244 | -0.119 |
| N (children x tests) | 1,571 | 1,561 | 1,367 | 2,334 |
|   of which displaced, head received ui (d or d+1) | 179 | 178 | 159 | 250 |
|   of which displaced, no ui received | 385 | 382 | 351 | 635 |
| Clusters (fam68) | 383 | 381 | 369 | 448 |
| **White: split by UI receipt** | | | | |
| Displaced, head received UI (d or d+1) | -1.247 (1.195; p=0.297) | -1.198 (1.120; p=0.285) | -1.481 (0.970; p=0.127) | 0.096 (0.064; p=0.135) |
| Displaced, no UI received | -0.219 (1.135; p=0.847) | -0.286 (1.056; p=0.786) | 0.492 (1.051; p=0.640) | 0.151*** (0.052; p=0.004) |
| Difference: Displaced, head received UI (d or d+1) minus Displaced, no UI received | -1.027 (1.512; p=0.497) | -0.912 (1.374; p=0.507) | -1.972 (1.297; p=0.128) | -0.054 (0.072; p=0.452) |
| Mean of outcome | 107.670 | 108.440 | 106.838 | 0.020 |
| N (children x tests) | 3,254 | 3,244 | 2,853 | 5,272 |
|   of which displaced, head received ui (d or d+1) | 304 | 304 | 282 | 463 |
|   of which displaced, no ui received | 508 | 508 | 459 | 838 |
| Clusters (fam68) | 701 | 702 | 681 | 869 |
| **Pooled: split by UI receipt** | | | | |
| Displaced, head received UI (d or d+1) | -2.054** (0.915; p=0.025) | -1.798* (0.956; p=0.060) | -1.874** (0.763; p=0.014) | 0.119** (0.051; p=0.020) |
| Displaced, no UI received | -0.231 (0.858; p=0.788) | -0.517 (0.827; p=0.532) | 0.435 (0.816; p=0.594) | 0.108*** (0.041; p=0.008) |
| Difference: Displaced, head received UI (d or d+1) minus Displaced, no UI received | -1.823 (1.112; p=0.101) | -1.282 (1.111; p=0.249) | -2.309** (0.983; p=0.019) | 0.010 (0.057; p=0.858) |
| Mean of outcome | 104.944 | 104.293 | 104.054 | -0.023 |
| N (children x tests) | 4,825 | 4,805 | 4,220 | 7,606 |
|   of which displaced, head received ui (d or d+1) | 483 | 482 | 441 | 713 |
|   of which displaced, no ui received | 893 | 890 | 810 | 1,473 |
| Clusters (fam68) | 1,068 | 1,068 | 1,037 | 1,285 |
| **Black: split by food-stamp receipt** | | | | |
| Displaced, family received food stamps (d or d+1) | -2.380 (1.517; p=0.117) | -0.557 (1.697; p=0.743) | 0.500 (1.534; p=0.744) | 0.283*** (0.088; p=0.001) |
| Displaced, no food stamps | -1.057 (1.331; p=0.427) | -1.974 (1.404; p=0.160) | -1.242 (1.288; p=0.335) | -0.012 (0.064; p=0.854) |
| Difference: Displaced, family received food stamps (d or d+1) minus Displaced, no food stamps | -1.323 (1.706; p=0.438) | 1.416 (1.865; p=0.448) | 1.743 (1.768; p=0.324) | 0.295*** (0.095; p=0.002) |
| Mean of outcome | 99.297 | 95.676 | 98.263 | -0.119 |
| N (children x tests) | 1,574 | 1,564 | 1,370 | 2,337 |
|   of which displaced, family received food stamps (d or d+1) | 232 | 230 | 207 | 372 |
|   of which displaced, no food stamps | 335 | 333 | 306 | 516 |
| Clusters (fam68) | 383 | 381 | 369 | 448 |
| **White: split by food-stamp receipt** | | | | |
| Displaced, family received food stamps (d or d+1) | -3.992** (1.751; p=0.023) | -3.352* (1.768; p=0.058) | -4.035** (1.668; p=0.016) | 0.381*** (0.092; p=<0.001) |
| Displaced, no food stamps | 0.149 (0.972; p=0.878) | -0.026 (0.894; p=0.976) | 0.582 (0.861; p=0.499) | 0.073 (0.048; p=0.133) |
| Difference: Displaced, family received food stamps (d or d+1) minus Displaced, no food stamps | -4.141** (1.893; p=0.029) | -3.325* (1.841; p=0.071) | -4.618** (1.795; p=0.010) | 0.308*** (0.099; p=0.002) |
| Mean of outcome | 107.670 | 108.440 | 106.838 | 0.020 |
| N (children x tests) | 3,254 | 3,244 | 2,853 | 5,272 |
|   of which displaced, family received food stamps (d or d+1) | 167 | 166 | 153 | 277 |
|   of which displaced, no food stamps | 645 | 646 | 588 | 1,024 |
| Clusters (fam68) | 701 | 702 | 681 | 869 |
| **Pooled: split by food-stamp receipt** | | | | |
| Displaced, family received food stamps (d or d+1) | -2.795** (1.113; p=0.012) | -1.480 (1.200; p=0.218) | -1.336 (1.152; p=0.246) | 0.305*** (0.063; p=<0.001) |
| Displaced, no food stamps | -0.216 (0.787; p=0.784) | -0.789 (0.762; p=0.301) | -0.041 (0.722; p=0.955) | 0.043 (0.039; p=0.267) |
| Difference: Displaced, family received food stamps (d or d+1) minus Displaced, no food stamps | -2.579** (1.237; p=0.037) | -0.691 (1.296; p=0.594) | -1.295 (1.278; p=0.311) | 0.261*** (0.068; p=<0.001) |
| Mean of outcome | 104.940 | 104.288 | 104.056 | -0.023 |
| N (children x tests) | 4,828 | 4,808 | 4,223 | 7,609 |
|   of which displaced, family received food stamps (d or d+1) | 399 | 396 | 360 | 649 |
|   of which displaced, no food stamps | 980 | 979 | 894 | 1,540 |
| Clusters (fam68) | 1,068 | 1,068 | 1,037 | 1,285 |
| Fixed effects | birth year, CDS wave | birth year, CDS wave | birth year, CDS wave | birth year, CDS wave |
| Other controls | log pre-event family income, parental education, female | log pre-event family income, parental education, female | log pre-event family income, parental education, female | log pre-event family income, parental education, female |

## 5. Safety-net buffering: exposure x UI generosity

UI generosity from `IGE/data/ui_generosity.csv` (measures: repl_rate, max_wba_2000), z-scored over the state-year panel, in the state of the father's family at the (pseudo) event year d (interview in d or d-1, else d+1) and year d; events from 1976 on. The interaction compares the displaced-control gap across states and years with more or less generous UI; UI generosity is not randomly assigned (it co-moves with state wages and politics), so the state-FE rows use only within-state changes.

### UI measure `repl_rate`, closure or layoff, adult outcomes

| | Log lifetime earnings | Log lifetime family income | Earnings rank (0-100) | Family income rank (0-100) | Years of schooling |
|---|---|---|---|---|---|
| **Black** | | | | | |
| Father figure displaced | -0.058 (0.071; p=0.413) | -0.072 (0.056; p=0.199) | -3.157 (2.060; p=0.125) | -3.328* (1.962; p=0.090) | -0.304*** (0.101; p=0.003) |
| Displaced x UI generosity (z) | -0.046 (0.097; p=0.635) | -0.030 (0.074; p=0.687) | 0.867 (2.557; p=0.735) | 0.126 (2.498; p=0.960) | 0.072 (0.126; p=0.565) |
| UI generosity (z) | 0.102 (0.077; p=0.185) | 0.055 (0.053; p=0.301) | 1.340 (1.827; p=0.463) | 1.250 (1.832; p=0.495) | -0.130 (0.099; p=0.188) |
| Mean of outcome | 9.763 | 10.299 | 45.160 | 39.316 | 13.206 |
| N (children) | 950 | 962 | 950 | 962 | 2,020 |
|   of which father figure displaced | 488 | 497 | 488 | 497 | 1,102 |
| Clusters (fam68) | 367 | 371 | 367 | 371 | 552 |
| **Black, state FE** | | | | | |
| Father figure displaced | -0.066 (0.074; p=0.377) | -0.067 (0.059; p=0.258) | -3.628* (2.161; p=0.093) | -3.259 (2.080; p=0.117) | -0.279*** (0.101; p=0.006) |
| Displaced x UI generosity (z) | -0.042 (0.098; p=0.671) | -0.042 (0.081; p=0.603) | 0.769 (2.680; p=0.774) | -0.330 (2.707; p=0.903) | 0.104 (0.127; p=0.412) |
| UI generosity (z) | 0.008 (0.082; p=0.920) | 0.051 (0.062; p=0.408) | 0.017 (2.217; p=0.994) | 1.721 (2.140; p=0.421) | -0.148 (0.121; p=0.220) |
| Mean of outcome | 9.763 | 10.299 | 45.160 | 39.316 | 13.206 |
| N (children) | 950 | 962 | 950 | 962 | 2,020 |
|   of which father figure displaced | 488 | 497 | 488 | 497 | 1,102 |
| Clusters (fam68) | 367 | 371 | 367 | 371 | 552 |
| **White** | | | | | |
| Father figure displaced | -0.142*** (0.047; p=0.003) | -0.087*** (0.032; p=0.007) | -4.326*** (1.398; p=0.002) | -3.806*** (1.318; p=0.004) | -0.603*** (0.091; p=<0.001) |
| Displaced x UI generosity (z) | 0.030 (0.048; p=0.526) | 0.007 (0.033; p=0.823) | 0.464 (1.446; p=0.748) | 0.547 (1.385; p=0.693) | 0.135 (0.092; p=0.142) |
| UI generosity (z) | 0.046 (0.031; p=0.136) | 0.023 (0.023; p=0.317) | 1.038 (0.954; p=0.277) | 0.600 (0.921; p=0.515) | 0.006 (0.060; p=0.917) |
| Mean of outcome | 10.134 | 10.898 | 57.898 | 62.229 | 14.021 |
| N (children) | 2,191 | 2,217 | 2,191 | 2,217 | 3,628 |
|   of which father figure displaced | 941 | 956 | 941 | 956 | 1,641 |
| Clusters (fam68) | 801 | 806 | 801 | 806 | 1,088 |
| **White, state FE** | | | | | |
| Father figure displaced | -0.132*** (0.046; p=0.004) | -0.083** (0.033; p=0.011) | -3.923*** (1.352; p=0.004) | -3.493*** (1.328; p=0.009) | -0.573*** (0.089; p=<0.001) |
| Displaced x UI generosity (z) | 0.037 (0.048; p=0.442) | 0.003 (0.034; p=0.932) | 0.927 (1.433; p=0.518) | 0.373 (1.399; p=0.790) | 0.159* (0.094; p=0.090) |
| UI generosity (z) | 0.032 (0.051; p=0.524) | 0.054 (0.039; p=0.162) | 0.805 (1.579; p=0.610) | 1.651 (1.566; p=0.292) | 0.083 (0.105; p=0.425) |
| Mean of outcome | 10.134 | 10.898 | 57.898 | 62.229 | 14.021 |
| N (children) | 2,191 | 2,217 | 2,191 | 2,217 | 3,628 |
|   of which father figure displaced | 941 | 956 | 941 | 956 | 1,641 |
| Clusters (fam68) | 801 | 806 | 801 | 806 | 1,088 |
| **Pooled** | | | | | |
| Father figure displaced | -0.110*** (0.039; p=0.005) | -0.080*** (0.028; p=0.004) | -3.971*** (1.142; p=<0.001) | -3.669*** (1.072; p=<0.001) | -0.477*** (0.068; p=<0.001) |
| Displaced x UI generosity (z) | 0.005 (0.041; p=0.901) | -0.000 (0.030; p=0.994) | 0.383 (1.213; p=0.752) | 0.435 (1.184; p=0.714) | 0.058 (0.074; p=0.431) |
| UI generosity (z) | 0.061** (0.028; p=0.032) | 0.030 (0.021; p=0.147) | 1.251 (0.832; p=0.133) | 0.792 (0.822; p=0.335) | -0.016 (0.052; p=0.760) |
| Mean of outcome | 10.022 | 10.717 | 54.046 | 55.296 | 13.730 |
| N (children) | 3,141 | 3,179 | 3,141 | 3,179 | 5,648 |
|   of which father figure displaced | 1,429 | 1,453 | 1,429 | 1,453 | 2,743 |
| Clusters (fam68) | 1,161 | 1,170 | 1,161 | 1,170 | 1,628 |
| **Pooled, state FE** | | | | | |
| Father figure displaced | -0.100*** (0.038; p=0.009) | -0.074*** (0.028; p=0.008) | -3.591*** (1.128; p=0.001) | -3.343*** (1.091; p=0.002) | -0.458*** (0.067; p=<0.001) |
| Displaced x UI generosity (z) | 0.011 (0.041; p=0.786) | -0.006 (0.031; p=0.857) | 0.667 (1.209; p=0.581) | 0.212 (1.196; p=0.859) | 0.080 (0.076; p=0.289) |
| UI generosity (z) | 0.021 (0.042; p=0.616) | 0.052 (0.032; p=0.103) | 0.737 (1.244; p=0.554) | 1.687 (1.228; p=0.170) | -0.009 (0.078; p=0.912) |
| Mean of outcome | 10.022 | 10.717 | 54.046 | 55.296 | 13.730 |
| N (children) | 3,141 | 3,179 | 3,141 | 3,179 | 5,648 |
|   of which father figure displaced | 1,429 | 1,453 | 1,429 | 1,453 | 2,743 |
| Clusters (fam68) | 1,161 | 1,170 | 1,161 | 1,170 | 1,628 |
| Fixed effects | birth year (+ CDS wave) (+ state) | birth year (+ CDS wave) (+ state) | birth year (+ CDS wave) (+ state) | birth year (+ CDS wave) (+ state) | birth year (+ CDS wave) (+ state) |

### UI measure `repl_rate`, closures only, adult outcomes

| | Log lifetime earnings | Log lifetime family income | Earnings rank (0-100) | Family income rank (0-100) | Years of schooling |
|---|---|---|---|---|---|
| **Black** | | | | | |
| Father figure displaced | 0.052 (0.098; p=0.594) | -0.003 (0.084; p=0.969) | -0.367 (2.751; p=0.894) | -0.851 (2.727; p=0.755) | -0.014 (0.163; p=0.931) |
| Displaced x UI generosity (z) | -0.056 (0.150; p=0.709) | 0.026 (0.125; p=0.835) | -0.651 (3.907; p=0.868) | -0.003 (3.974; p=0.999) | -0.115 (0.203; p=0.572) |
| UI generosity (z) | 0.094 (0.068; p=0.169) | 0.014 (0.052; p=0.785) | 0.057 (1.730; p=0.974) | 0.523 (1.800; p=0.772) | -0.083 (0.106; p=0.431) |
| Mean of outcome | 9.834 | 10.369 | 48.025 | 42.420 | 13.446 |
| N (children) | 629 | 633 | 629 | 633 | 1,268 |
|   of which father figure displaced | 145 | 146 | 145 | 146 | 291 |
| Clusters (fam68) | 295 | 296 | 295 | 296 | 451 |
| **Black, state FE** | | | | | |
| Father figure displaced | 0.060 (0.100; p=0.546) | 0.039 (0.084; p=0.639) | -0.466 (2.874; p=0.871) | -0.119 (2.915; p=0.967) | -0.041 (0.159; p=0.798) |
| Displaced x UI generosity (z) | -0.031 (0.147; p=0.834) | 0.049 (0.122; p=0.689) | -0.185 (3.910; p=0.962) | 0.324 (3.994; p=0.935) | -0.059 (0.206; p=0.773) |
| UI generosity (z) | -0.081 (0.087; p=0.352) | -0.016 (0.069; p=0.814) | -2.526 (2.560; p=0.324) | 0.725 (2.444; p=0.767) | -0.142 (0.138; p=0.303) |
| Mean of outcome | 9.834 | 10.369 | 48.025 | 42.420 | 13.446 |
| N (children) | 629 | 633 | 629 | 633 | 1,268 |
|   of which father figure displaced | 145 | 146 | 145 | 146 | 291 |
| Clusters (fam68) | 295 | 296 | 295 | 296 | 451 |
| **White** | | | | | |
| Father figure displaced | -0.088 (0.063; p=0.162) | -0.017 (0.045; p=0.708) | -3.351* (1.949; p=0.086) | -1.315 (1.817; p=0.469) | -0.478*** (0.133; p=<0.001) |
| Displaced x UI generosity (z) | -0.020 (0.069; p=0.772) | -0.033 (0.046; p=0.473) | 0.323 (2.156; p=0.881) | -1.408 (1.906; p=0.460) | -0.085 (0.147; p=0.562) |
| UI generosity (z) | 0.055* (0.030; p=0.064) | 0.021 (0.022; p=0.328) | 1.323 (0.889; p=0.137) | 0.705 (0.876; p=0.421) | -0.011 (0.061; p=0.860) |
| Mean of outcome | 10.221 | 10.973 | 60.666 | 65.012 | 14.209 |
| N (children) | 1,637 | 1,653 | 1,637 | 1,653 | 2,699 |
|   of which father figure displaced | 319 | 323 | 319 | 323 | 571 |
| Clusters (fam68) | 694 | 700 | 694 | 700 | 958 |
| **White, state FE** | | | | | |
| Father figure displaced | -0.082 (0.062; p=0.182) | -0.004 (0.047; p=0.939) | -3.065 (1.915; p=0.109) | -0.795 (1.857; p=0.669) | -0.403*** (0.130; p=0.002) |
| Displaced x UI generosity (z) | -0.021 (0.069; p=0.759) | -0.042 (0.046; p=0.367) | 0.183 (2.126; p=0.931) | -1.785 (1.937; p=0.357) | -0.057 (0.149; p=0.701) |
| UI generosity (z) | 0.073 (0.056; p=0.194) | 0.082* (0.045; p=0.070) | 1.776 (1.759; p=0.313) | 2.225 (1.750; p=0.203) | -0.077 (0.120; p=0.523) |
| Mean of outcome | 10.221 | 10.973 | 60.666 | 65.012 | 14.209 |
| N (children) | 1,637 | 1,653 | 1,637 | 1,653 | 2,699 |
|   of which father figure displaced | 319 | 323 | 319 | 323 | 571 |
| Clusters (fam68) | 694 | 700 | 694 | 700 | 958 |
| **Pooled** | | | | | |
| Father figure displaced | -0.044 (0.053; p=0.409) | -0.017 (0.040; p=0.672) | -2.317 (1.589; p=0.145) | -1.259 (1.503; p=0.402) | -0.300*** (0.103; p=0.004) |
| Displaced x UI generosity (z) | -0.044 (0.063; p=0.489) | -0.024 (0.045; p=0.589) | -0.503 (1.859; p=0.787) | -1.323 (1.717; p=0.441) | -0.140 (0.121; p=0.249) |
| UI generosity (z) | 0.072*** (0.027; p=0.009) | 0.022 (0.020; p=0.269) | 1.342* (0.788; p=0.089) | 0.766 (0.786; p=0.330) | -0.018 (0.053; p=0.726) |
| Mean of outcome | 10.113 | 10.806 | 57.157 | 58.757 | 13.965 |
| N (children) | 2,266 | 2,286 | 2,266 | 2,286 | 3,967 |
|   of which father figure displaced | 464 | 469 | 464 | 469 | 862 |
| Clusters (fam68) | 987 | 994 | 987 | 994 | 1,405 |
| **Pooled, state FE** | | | | | |
| Father figure displaced | -0.038 (0.053; p=0.476) | -0.009 (0.040; p=0.817) | -2.227 (1.576; p=0.158) | -1.105 (1.539; p=0.473) | -0.253** (0.101; p=0.012) |
| Displaced x UI generosity (z) | -0.056 (0.063; p=0.374) | -0.035 (0.045; p=0.440) | -0.804 (1.831; p=0.661) | -1.751 (1.729; p=0.311) | -0.108 (0.123; p=0.378) |
| UI generosity (z) | 0.027 (0.046; p=0.548) | 0.051 (0.037; p=0.163) | 0.619 (1.406; p=0.660) | 1.764 (1.393; p=0.205) | -0.080 (0.089; p=0.369) |
| Mean of outcome | 10.113 | 10.806 | 57.157 | 58.757 | 13.965 |
| N (children) | 2,266 | 2,286 | 2,266 | 2,286 | 3,967 |
|   of which father figure displaced | 464 | 469 | 464 | 469 | 862 |
| Clusters (fam68) | 987 | 994 | 987 | 994 | 1,405 |
| Fixed effects | birth year (+ CDS wave) (+ state) | birth year (+ CDS wave) (+ state) | birth year (+ CDS wave) (+ state) | birth year (+ CDS wave) (+ state) | birth year (+ CDS wave) (+ state) |

### UI measure `repl_rate`, closure or layoff, CDS

| | WJ Letter-Word | WJ Applied Problems | WJ Passage Comp. | BPI (z, higher = worse) |
|---|---|---|---|---|
| **Black** | | | | |
| Father figure displaced | -2.029* (1.151; p=0.078) | -1.096 (1.210; p=0.365) | -0.834 (1.111; p=0.453) | 0.055 (0.063; p=0.383) |
| Displaced x UI generosity (z) | -1.681 (1.671; p=0.314) | 0.435 (1.587; p=0.784) | 0.076 (1.433; p=0.958) | -0.090 (0.083; p=0.278) |
| UI generosity (z) | 0.435 (1.059; p=0.682) | 0.207 (0.828; p=0.803) | 0.386 (0.802; p=0.630) | 0.028 (0.049; p=0.564) |
| Mean of outcome | 99.275 | 95.708 | 98.206 | -0.122 |
| N (children x tests) | 1,611 | 1,601 | 1,405 | 2,387 |
|   of which father figure displaced | 606 | 602 | 550 | 941 |
| Clusters (fam68) | 388 | 386 | 374 | 451 |
| **Black, state FE** | | | | |
| Father figure displaced | -1.892 (1.158; p=0.102) | -0.804 (1.180; p=0.496) | -0.624 (1.103; p=0.571) | 0.044 (0.065; p=0.495) |
| Displaced x UI generosity (z) | -1.699 (1.654; p=0.304) | 0.501 (1.622; p=0.757) | 0.058 (1.495; p=0.969) | -0.062 (0.080; p=0.441) |
| UI generosity (z) | -0.293 (1.701; p=0.863) | -2.212 (1.403; p=0.115) | -0.863 (1.406; p=0.539) | -0.022 (0.077; p=0.771) |
| Mean of outcome | 99.275 | 95.708 | 98.206 | -0.122 |
| N (children x tests) | 1,611 | 1,601 | 1,405 | 2,387 |
|   of which father figure displaced | 606 | 602 | 550 | 941 |
| Clusters (fam68) | 388 | 386 | 374 | 451 |
| **White** | | | | |
| Father figure displaced | -0.700 (0.908; p=0.441) | -0.743 (0.873; p=0.395) | -0.312 (0.823; p=0.704) | 0.132*** (0.045; p=0.003) |
| Displaced x UI generosity (z) | 2.305** (1.141; p=0.043) | 1.065 (1.205; p=0.377) | 1.461 (1.097; p=0.183) | -0.098* (0.053; p=0.066) |
| UI generosity (z) | -0.858 (0.530; p=0.106) | 0.414 (0.543; p=0.446) | -0.340 (0.501; p=0.497) | 0.033 (0.027; p=0.225) |
| Mean of outcome | 107.688 | 108.439 | 106.847 | 0.020 |
| N (children x tests) | 3,264 | 3,254 | 2,861 | 5,285 |
|   of which father figure displaced | 823 | 823 | 750 | 1,325 |
| Clusters (fam68) | 704 | 705 | 684 | 872 |
| **White, state FE** | | | | |
| Father figure displaced | -1.038 (0.875; p=0.236) | -0.795 (0.851; p=0.350) | -0.400 (0.791; p=0.613) | 0.115** (0.045; p=0.010) |
| Displaced x UI generosity (z) | 1.887* (1.056; p=0.074) | 1.137 (1.151; p=0.323) | 1.235 (1.057; p=0.243) | -0.100* (0.053; p=0.060) |
| UI generosity (z) | 0.044 (0.938; p=0.962) | 0.325 (1.129; p=0.773) | -0.034 (0.946; p=0.972) | 0.006 (0.049; p=0.903) |
| Mean of outcome | 107.688 | 108.439 | 106.847 | 0.020 |
| N (children x tests) | 3,264 | 3,254 | 2,861 | 5,285 |
|   of which father figure displaced | 823 | 823 | 750 | 1,325 |
| Clusters (fam68) | 704 | 705 | 684 | 872 |
| **Pooled** | | | | |
| Father figure displaced | -0.726 (0.694; p=0.296) | -0.822 (0.676; p=0.224) | -0.317 (0.637; p=0.619) | 0.097*** (0.035; p=0.006) |
| Displaced x UI generosity (z) | 1.055 (0.917; p=0.250) | 0.805 (0.907; p=0.375) | 1.074 (0.821; p=0.191) | -0.070 (0.044; p=0.115) |
| UI generosity (z) | -0.607 (0.476; p=0.202) | 0.328 (0.464; p=0.479) | -0.194 (0.428; p=0.651) | 0.027 (0.023; p=0.252) |
| Mean of outcome | 104.907 | 104.240 | 104.001 | -0.024 |
| N (children x tests) | 4,875 | 4,855 | 4,266 | 7,672 |
|   of which father figure displaced | 1,429 | 1,425 | 1,300 | 2,266 |
| Clusters (fam68) | 1,075 | 1,075 | 1,044 | 1,289 |
| **Pooled, state FE** | | | | |
| Father figure displaced | -0.975 (0.681; p=0.152) | -0.910 (0.665; p=0.172) | -0.440 (0.624; p=0.480) | 0.086** (0.035; p=0.014) |
| Displaced x UI generosity (z) | 0.501 (0.881; p=0.569) | 0.857 (0.896; p=0.339) | 0.762 (0.829; p=0.358) | -0.066 (0.043; p=0.122) |
| UI generosity (z) | -0.309 (0.837; p=0.712) | -0.512 (0.896; p=0.568) | -0.188 (0.783; p=0.810) | 0.012 (0.041; p=0.763) |
| Mean of outcome | 104.907 | 104.240 | 104.001 | -0.024 |
| N (children x tests) | 4,875 | 4,855 | 4,266 | 7,672 |
|   of which father figure displaced | 1,429 | 1,425 | 1,300 | 2,266 |
| Clusters (fam68) | 1,075 | 1,075 | 1,044 | 1,289 |
| Fixed effects | birth year (+ CDS wave) (+ state) | birth year (+ CDS wave) (+ state) | birth year (+ CDS wave) (+ state) | birth year (+ CDS wave) (+ state) |

### UI measure `max_wba_2000`, closure or layoff, adult outcomes

| | Log lifetime earnings | Log lifetime family income | Earnings rank (0-100) | Family income rank (0-100) | Years of schooling |
|---|---|---|---|---|---|
| **Black** | | | | | |
| Father figure displaced | -0.079 (0.078; p=0.311) | -0.083 (0.063; p=0.188) | -3.428 (2.301; p=0.136) | -3.322 (2.261; p=0.142) | -0.260** (0.110; p=0.019) |
| Displaced x UI generosity (z) | -0.038 (0.071; p=0.593) | -0.022 (0.061; p=0.713) | -0.058 (2.203; p=0.979) | 0.258 (2.157; p=0.905) | 0.083 (0.119; p=0.487) |
| UI generosity (z) | 0.031 (0.051; p=0.545) | 0.009 (0.045; p=0.839) | 0.342 (1.569; p=0.827) | 0.194 (1.626; p=0.905) | -0.250** (0.099; p=0.012) |
| Mean of outcome | 9.763 | 10.299 | 45.160 | 39.316 | 13.206 |
| N (children) | 950 | 962 | 950 | 962 | 2,020 |
|   of which father figure displaced | 488 | 497 | 488 | 497 | 1,102 |
| Clusters (fam68) | 367 | 371 | 367 | 371 | 552 |
| **Black, state FE** | | | | | |
| Father figure displaced | -0.086 (0.082; p=0.294) | -0.093 (0.067; p=0.165) | -4.082* (2.450; p=0.096) | -3.896 (2.436; p=0.110) | -0.250** (0.111; p=0.024) |
| Displaced x UI generosity (z) | -0.050 (0.073; p=0.494) | -0.057 (0.063; p=0.370) | -0.677 (2.346; p=0.773) | -1.104 (2.302; p=0.632) | 0.067 (0.120; p=0.578) |
| UI generosity (z) | 0.007 (0.088; p=0.938) | 0.084 (0.065; p=0.195) | 0.170 (2.532; p=0.946) | 2.656 (2.338; p=0.256) | -0.175 (0.128; p=0.171) |
| Mean of outcome | 9.763 | 10.299 | 45.160 | 39.316 | 13.206 |
| N (children) | 950 | 962 | 950 | 962 | 2,020 |
|   of which father figure displaced | 488 | 497 | 488 | 497 | 1,102 |
| Clusters (fam68) | 367 | 371 | 367 | 371 | 552 |
| **White** | | | | | |
| Father figure displaced | -0.160*** (0.044; p=<0.001) | -0.098*** (0.032; p=0.002) | -4.836*** (1.347; p=<0.001) | -4.001*** (1.286; p=0.002) | -0.585*** (0.091; p=<0.001) |
| Displaced x UI generosity (z) | -0.084* (0.049; p=0.086) | -0.039 (0.033; p=0.242) | -2.047 (1.416; p=0.148) | -0.710 (1.341; p=0.596) | 0.011 (0.095; p=0.905) |
| UI generosity (z) | 0.114*** (0.031; p=<0.001) | 0.061*** (0.023; p=0.008) | 2.691*** (0.951; p=0.005) | 1.708* (0.921; p=0.064) | 0.065 (0.063; p=0.301) |
| Mean of outcome | 10.134 | 10.898 | 57.898 | 62.229 | 14.022 |
| N (children) | 2,191 | 2,217 | 2,191 | 2,217 | 3,624 |
|   of which father figure displaced | 941 | 956 | 941 | 956 | 1,641 |
| Clusters (fam68) | 801 | 806 | 801 | 806 | 1,088 |
| **White, state FE** | | | | | |
| Father figure displaced | -0.141*** (0.044; p=0.001) | -0.091*** (0.032; p=0.004) | -4.093*** (1.307; p=0.002) | -3.584*** (1.298; p=0.006) | -0.544*** (0.089; p=<0.001) |
| Displaced x UI generosity (z) | -0.072 (0.048; p=0.137) | -0.042 (0.034; p=0.227) | -1.709 (1.428; p=0.231) | -0.846 (1.373; p=0.538) | 0.042 (0.095; p=0.656) |
| UI generosity (z) | 0.069 (0.051; p=0.171) | 0.041 (0.037; p=0.276) | 1.315 (1.589; p=0.408) | 0.884 (1.518; p=0.560) | 0.097 (0.101; p=0.340) |
| Mean of outcome | 10.134 | 10.898 | 57.898 | 62.229 | 14.022 |
| N (children) | 2,191 | 2,217 | 2,191 | 2,217 | 3,624 |
|   of which father figure displaced | 941 | 956 | 941 | 956 | 1,641 |
| Clusters (fam68) | 801 | 806 | 801 | 806 | 1,088 |
| **Pooled** | | | | | |
| Father figure displaced | -0.138*** (0.038; p=<0.001) | -0.095*** (0.028; p=<0.001) | -4.518*** (1.159; p=<0.001) | -3.869*** (1.101; p=<0.001) | -0.473*** (0.072; p=<0.001) |
| Displaced x UI generosity (z) | -0.082** (0.040; p=0.040) | -0.037 (0.029; p=0.194) | -1.616 (1.175; p=0.169) | -0.471 (1.104; p=0.670) | -0.013 (0.074; p=0.856) |
| UI generosity (z) | 0.093*** (0.027; p=<0.001) | 0.051** (0.021; p=0.013) | 2.083*** (0.807; p=0.010) | 1.407* (0.795; p=0.077) | -0.022 (0.054; p=0.679) |
| Mean of outcome | 10.022 | 10.717 | 54.046 | 55.296 | 13.730 |
| N (children) | 3,141 | 3,179 | 3,141 | 3,179 | 5,644 |
|   of which father figure displaced | 1,429 | 1,453 | 1,429 | 1,453 | 2,743 |
| Clusters (fam68) | 1,161 | 1,170 | 1,161 | 1,170 | 1,628 |
| **Pooled, state FE** | | | | | |
| Father figure displaced | -0.122*** (0.038; p=0.001) | -0.089*** (0.029; p=0.002) | -3.964*** (1.155; p=<0.001) | -3.538*** (1.124; p=0.002) | -0.450*** (0.071; p=<0.001) |
| Displaced x UI generosity (z) | -0.072* (0.038; p=0.062) | -0.039 (0.029; p=0.175) | -1.334 (1.166; p=0.253) | -0.514 (1.113; p=0.644) | 0.009 (0.073; p=0.900) |
| UI generosity (z) | 0.057 (0.044; p=0.196) | 0.054* (0.032; p=0.094) | 1.144 (1.319; p=0.386) | 1.249 (1.258; p=0.321) | -0.004 (0.080; p=0.963) |
| Mean of outcome | 10.022 | 10.717 | 54.046 | 55.296 | 13.730 |
| N (children) | 3,141 | 3,179 | 3,141 | 3,179 | 5,644 |
|   of which father figure displaced | 1,429 | 1,453 | 1,429 | 1,453 | 2,743 |
| Clusters (fam68) | 1,161 | 1,170 | 1,161 | 1,170 | 1,628 |
| Fixed effects | birth year (+ CDS wave) (+ state) | birth year (+ CDS wave) (+ state) | birth year (+ CDS wave) (+ state) | birth year (+ CDS wave) (+ state) | birth year (+ CDS wave) (+ state) |

### UI measure `max_wba_2000`, closures only, adult outcomes

| | Log lifetime earnings | Log lifetime family income | Earnings rank (0-100) | Family income rank (0-100) | Years of schooling |
|---|---|---|---|---|---|
| **Black** | | | | | |
| Father figure displaced | -0.000 (0.121; p=1.000) | -0.014 (0.104; p=0.893) | -1.807 (3.237; p=0.577) | -0.665 (3.342; p=0.842) | -0.012 (0.170; p=0.942) |
| Displaced x UI generosity (z) | -0.104 (0.115; p=0.367) | -0.010 (0.109; p=0.927) | -2.764 (3.709; p=0.456) | 0.387 (3.914; p=0.921) | -0.047 (0.168; p=0.778) |
| UI generosity (z) | 0.006 (0.052; p=0.906) | 0.001 (0.046; p=0.989) | -0.648 (1.715; p=0.706) | 0.105 (1.726; p=0.951) | -0.262** (0.106; p=0.013) |
| Mean of outcome | 9.834 | 10.369 | 48.025 | 42.420 | 13.446 |
| N (children) | 629 | 633 | 629 | 633 | 1,268 |
|   of which father figure displaced | 145 | 146 | 145 | 146 | 291 |
| Clusters (fam68) | 295 | 296 | 295 | 296 | 451 |
| **Black, state FE** | | | | | |
| Father figure displaced | 0.020 (0.125; p=0.874) | 0.013 (0.103; p=0.902) | -2.592 (3.447; p=0.452) | -0.857 (3.629; p=0.813) | -0.031 (0.171; p=0.857) |
| Displaced x UI generosity (z) | -0.086 (0.119; p=0.470) | -0.032 (0.107; p=0.765) | -3.938 (3.825; p=0.303) | -1.202 (3.972; p=0.762) | -0.018 (0.168; p=0.913) |
| UI generosity (z) | -0.042 (0.093; p=0.650) | 0.077 (0.075; p=0.308) | -0.806 (2.949; p=0.785) | 3.392 (2.819; p=0.229) | -0.145 (0.150; p=0.334) |
| Mean of outcome | 9.834 | 10.369 | 48.025 | 42.420 | 13.446 |
| N (children) | 629 | 633 | 629 | 633 | 1,268 |
|   of which father figure displaced | 145 | 146 | 145 | 146 | 291 |
| Clusters (fam68) | 295 | 296 | 295 | 296 | 451 |
| **White** | | | | | |
| Father figure displaced | -0.116* (0.061; p=0.056) | -0.034 (0.045; p=0.447) | -3.779** (1.898; p=0.046) | -1.836 (1.803; p=0.309) | -0.483*** (0.135; p=<0.001) |
| Displaced x UI generosity (z) | -0.052 (0.068; p=0.444) | -0.019 (0.050; p=0.710) | 0.163 (2.069; p=0.937) | -0.031 (1.936; p=0.987) | 0.100 (0.138; p=0.469) |
| UI generosity (z) | 0.119*** (0.031; p=<0.001) | 0.057*** (0.022; p=0.009) | 3.063*** (0.926; p=<0.001) | 1.788** (0.888; p=0.044) | -0.009 (0.058; p=0.882) |
| Mean of outcome | 10.221 | 10.974 | 60.688 | 65.041 | 14.208 |
| N (children) | 1,635 | 1,651 | 1,635 | 1,651 | 2,694 |
|   of which father figure displaced | 319 | 323 | 319 | 323 | 571 |
| Clusters (fam68) | 693 | 699 | 693 | 699 | 958 |
| **White, state FE** | | | | | |
| Father figure displaced | -0.098 (0.061; p=0.107) | -0.019 (0.046; p=0.680) | -3.232* (1.886; p=0.087) | -1.271 (1.844; p=0.491) | -0.399*** (0.132; p=0.002) |
| Displaced x UI generosity (z) | -0.053 (0.067; p=0.425) | -0.031 (0.051; p=0.548) | -0.304 (2.093; p=0.885) | -0.564 (2.011; p=0.779) | 0.114 (0.135; p=0.399) |
| UI generosity (z) | 0.076 (0.050; p=0.130) | 0.016 (0.041; p=0.695) | 1.273 (1.640; p=0.438) | -0.545 (1.650; p=0.741) | -0.087 (0.108; p=0.419) |
| Mean of outcome | 10.221 | 10.974 | 60.688 | 65.041 | 14.208 |
| N (children) | 1,635 | 1,651 | 1,635 | 1,651 | 2,694 |
|   of which father figure displaced | 319 | 323 | 319 | 323 | 571 |
| Clusters (fam68) | 693 | 699 | 693 | 699 | 958 |
| **Pooled** | | | | | |
| Father figure displaced | -0.076 (0.054; p=0.157) | -0.030 (0.040; p=0.460) | -2.809* (1.606; p=0.080) | -1.550 (1.520; p=0.308) | -0.305*** (0.108; p=0.005) |
| Displaced x UI generosity (z) | -0.076 (0.058; p=0.192) | -0.026 (0.044; p=0.554) | -0.894 (1.826; p=0.624) | -0.236 (1.696; p=0.889) | -0.008 (0.108; p=0.939) |
| UI generosity (z) | 0.094*** (0.027; p=<0.001) | 0.047** (0.020; p=0.018) | 2.253*** (0.818; p=0.006) | 1.500* (0.780; p=0.055) | -0.071 (0.051; p=0.167) |
| Mean of outcome | 10.114 | 10.806 | 57.170 | 58.772 | 13.964 |
| N (children) | 2,264 | 2,284 | 2,264 | 2,284 | 3,962 |
|   of which father figure displaced | 464 | 469 | 464 | 469 | 862 |
| Clusters (fam68) | 986 | 993 | 986 | 993 | 1,405 |
| **Pooled, state FE** | | | | | |
| Father figure displaced | -0.063 (0.054; p=0.241) | -0.024 (0.041; p=0.565) | -2.692* (1.609; p=0.094) | -1.483 (1.567; p=0.344) | -0.255** (0.106; p=0.016) |
| Displaced x UI generosity (z) | -0.080 (0.057; p=0.159) | -0.036 (0.045; p=0.418) | -1.377 (1.808; p=0.446) | -0.711 (1.703; p=0.676) | 0.008 (0.104; p=0.937) |
| UI generosity (z) | 0.032 (0.045; p=0.474) | 0.021 (0.036; p=0.553) | 0.390 (1.414; p=0.783) | 0.064 (1.396; p=0.964) | -0.119 (0.086; p=0.164) |
| Mean of outcome | 10.114 | 10.806 | 57.170 | 58.772 | 13.964 |
| N (children) | 2,264 | 2,284 | 2,264 | 2,284 | 3,962 |
|   of which father figure displaced | 464 | 469 | 464 | 469 | 862 |
| Clusters (fam68) | 986 | 993 | 986 | 993 | 1,405 |
| Fixed effects | birth year (+ CDS wave) (+ state) | birth year (+ CDS wave) (+ state) | birth year (+ CDS wave) (+ state) | birth year (+ CDS wave) (+ state) | birth year (+ CDS wave) (+ state) |

### UI measure `max_wba_2000`, closure or layoff, CDS

| | WJ Letter-Word | WJ Applied Problems | WJ Passage Comp. | BPI (z, higher = worse) |
|---|---|---|---|---|
| **Black** | | | | |
| Father figure displaced | -1.670 (1.117; p=0.135) | -1.059 (1.220; p=0.385) | -0.578 (1.068; p=0.588) | 0.086 (0.058; p=0.136) |
| Displaced x UI generosity (z) | -0.406 (1.255; p=0.746) | 0.386 (1.319; p=0.770) | 0.757 (1.206; p=0.530) | -0.008 (0.058; p=0.887) |
| UI generosity (z) | -0.391 (0.900; p=0.664) | -0.253 (0.824; p=0.759) | -0.488 (0.795; p=0.539) | 0.008 (0.040; p=0.831) |
| Mean of outcome | 99.275 | 95.708 | 98.206 | -0.122 |
| N (children x tests) | 1,611 | 1,601 | 1,405 | 2,387 |
|   of which father figure displaced | 606 | 602 | 550 | 941 |
| Clusters (fam68) | 388 | 386 | 374 | 451 |
| **Black, state FE** | | | | |
| Father figure displaced | -1.419 (1.109; p=0.201) | -0.548 (1.180; p=0.642) | -0.116 (1.035; p=0.910) | 0.072 (0.059; p=0.225) |
| Displaced x UI generosity (z) | -0.042 (1.223; p=0.972) | 0.852 (1.328; p=0.521) | 1.352 (1.187; p=0.255) | 0.010 (0.059; p=0.864) |
| UI generosity (z) | -1.843 (1.584; p=0.245) | -3.806*** (1.439; p=0.008) | -1.028 (1.396; p=0.462) | -0.073 (0.069; p=0.284) |
| Mean of outcome | 99.275 | 95.708 | 98.206 | -0.122 |
| N (children x tests) | 1,611 | 1,601 | 1,405 | 2,387 |
|   of which father figure displaced | 606 | 602 | 550 | 941 |
| Clusters (fam68) | 388 | 386 | 374 | 451 |
| **White** | | | | |
| Father figure displaced | -0.558 (0.920; p=0.544) | -0.629 (0.872; p=0.471) | -0.240 (0.827; p=0.772) | 0.132*** (0.046; p=0.004) |
| Displaced x UI generosity (z) | 0.669 (0.906; p=0.460) | 0.033 (0.879; p=0.970) | 0.680 (0.831; p=0.413) | -0.021 (0.044; p=0.629) |
| UI generosity (z) | 0.057 (0.463; p=0.902) | 0.370 (0.434; p=0.394) | -0.063 (0.420; p=0.881) | -0.001 (0.022; p=0.948) |
| Mean of outcome | 107.687 | 108.426 | 106.861 | 0.020 |
| N (children x tests) | 3,260 | 3,250 | 2,857 | 5,281 |
|   of which father figure displaced | 823 | 823 | 750 | 1,325 |
| Clusters (fam68) | 703 | 704 | 683 | 872 |
| **White, state FE** | | | | |
| Father figure displaced | -0.828 (0.882; p=0.348) | -0.627 (0.848; p=0.460) | -0.297 (0.791; p=0.708) | 0.116** (0.046; p=0.012) |
| Displaced x UI generosity (z) | 0.506 (0.861; p=0.557) | 0.030 (0.857; p=0.972) | 0.493 (0.802; p=0.539) | -0.027 (0.044; p=0.536) |
| UI generosity (z) | -0.768 (0.908; p=0.398) | -0.380 (1.009; p=0.706) | -0.424 (0.844; p=0.616) | -0.004 (0.044; p=0.936) |
| Mean of outcome | 107.687 | 108.426 | 106.861 | 0.020 |
| N (children x tests) | 3,260 | 3,250 | 2,857 | 5,281 |
|   of which father figure displaced | 823 | 823 | 750 | 1,325 |
| Clusters (fam68) | 703 | 704 | 683 | 872 |
| **Pooled** | | | | |
| Father figure displaced | -0.743 (0.692; p=0.283) | -0.839 (0.679; p=0.216) | -0.315 (0.638; p=0.621) | 0.105*** (0.035; p=0.003) |
| Displaced x UI generosity (z) | 0.436 (0.682; p=0.522) | 0.010 (0.688; p=0.989) | 0.680 (0.643; p=0.291) | -0.008 (0.034; p=0.811) |
| UI generosity (z) | -0.161 (0.412; p=0.696) | 0.226 (0.383; p=0.555) | -0.163 (0.374; p=0.664) | 0.001 (0.019; p=0.977) |
| Mean of outcome | 104.905 | 104.228 | 104.008 | -0.024 |
| N (children x tests) | 4,871 | 4,851 | 4,262 | 7,668 |
|   of which father figure displaced | 1,429 | 1,425 | 1,300 | 2,266 |
| Clusters (fam68) | 1,074 | 1,074 | 1,043 | 1,289 |
| **Pooled, state FE** | | | | |
| Father figure displaced | -0.917 (0.680; p=0.178) | -0.881 (0.666; p=0.186) | -0.419 (0.622; p=0.501) | 0.093*** (0.035; p=0.008) |
| Displaced x UI generosity (z) | 0.487 (0.666; p=0.465) | 0.122 (0.681; p=0.858) | 0.766 (0.639; p=0.231) | -0.016 (0.033; p=0.624) |
| UI generosity (z) | -1.459* (0.758; p=0.054) | -1.239 (0.786; p=0.115) | -0.299 (0.700; p=0.670) | 0.000 (0.036; p=0.991) |
| Mean of outcome | 104.905 | 104.228 | 104.008 | -0.024 |
| N (children x tests) | 4,871 | 4,851 | 4,262 | 7,668 |
|   of which father figure displaced | 1,429 | 1,425 | 1,300 | 2,266 |
| Clusters (fam68) | 1,074 | 1,074 | 1,043 | 1,289 |
| Fixed effects | birth year (+ CDS wave) (+ state) | birth year (+ CDS wave) (+ state) | birth year (+ CDS wave) (+ state) | birth year (+ CDS wave) (+ state) |

## 6. Sample sizes

| | Displaced / exposed | Not | Rows |
|---|---|---|---|
| Closure-first, children, 0-17, Black | 775 | 2,452 | 3,227 |
| Closure-first, children, 0-17, White | 1,194 | 5,640 | 6,834 |
| Closure-first, CDS child-tests, 0-17, Black | 227 | 1,325 | 1,552 |
| Closure-first, CDS child-tests, 0-17, White | 367 | 3,674 | 4,041 |
| Closure or layoff, children, 0-17, Black | 3,152 | 2,503 | 5,655 |
| Closure or layoff, children, 0-17, White | 3,911 | 5,858 | 9,769 |
| Closure or layoff, CDS child-tests, 0-17, Black | 951 | 1,468 | 2,419 |
| Closure or layoff, CDS child-tests, 0-17, White | 1,341 | 4,006 | 5,347 |
| Sibling frame (all children with a mother id), Black | 2,628 | 8,222 | 10,850 |
| Future-displacement frame, Black (exposed 12-17 / not) | 350 | 1,751 | 2,805 |
| Sibling frame (all children with a mother id), White | 3,041 | 12,203 | 15,244 |
| Future-displacement frame, White (exposed 12-17 / not) | 557 | 3,611 | 5,472 |
