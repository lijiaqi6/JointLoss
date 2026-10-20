# Checks of the CPS joint job-loss headline

Built by `IGE/37.CPSJointLossChecks.py` (2026-10-17; definitions in its docstring), on the couples panel and definitions of `30.CPSJointJobLoss.py`, answering the referee review `proposals/fable_review_paperA.md` (Sec. 3.2; plan items 1, 2, 4, 7). Sample unless stated: both spouses employed at t; H = 1 if the husband becomes a job loser at t+1 (unemployed, reason job loser on layoff / other job loser / temporary job ended), H = 0 if he stays employed; outcome: the wife becomes a job loser at t+1. Each cell is a separate LPM of the outcome in the column header on H with state x year-month FE (base month t): coefficient*** (s.e. clustered by household; p) [s.e. clustered by state; p]; *** p<0.01, ** p<0.05, * p<0.1. Means weighted by the wife's composite weight. 'Excl. 2020-21' drops base or job-loss months in calendar 2020-2021. Row panels are samples. Associations, not causal effects.

Headline reproduced: P(wife job loser | husband job loser) 0.0545 vs 0.0054 | husband employed; state x month FE 0.040*** (0.002; p=<0.001) [0.003; p=<0.001]; N 2,912,111, husband job losers 19,881, joint events 944.

## 1. Proxy reporting (PUSLFPRX: labor-force information given by self / proxy / both)

Reporting status found for 0.996 of the couple-months in the sample (status in the month of the job loss, t+1; couple key of 30). Among them (unweighted): both self-report 0.000; wife self, husband by proxy 0.548; husband self, wife by proxy 0.399; both by proxy 0.041; 'both self and proxy' (code 3) for either 0.011. Wife self-reports, husband by proxy: the wife is the household respondent in 0.942 of these couple-months. Status at t+1 can respond to the job loss itself (a man at home after losing his job is more likely to answer for himself), so panel B uses couples with the same status at t (before the event) and at t+1.

| | (1) wife job loser t+1 | (2) wife job loser t+1, excl. 2020-21 |
|---|---|---|
| **(a) All couples** | | |
| Husband becomes job loser (t+1) | 0.040*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.035*** (0.001; p=<0.001) [0.003; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0054 / 0.0545 | 0.0051 / 0.0443 |
| N / N(H = 1) | 2,912,111 / 19,881 | 2,775,713 / 18,671 |
| **(a') Reporting status known for both at t+1** | | |
| Husband becomes job loser (t+1) | 0.040*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.035*** (0.001; p=<0.001) [0.003; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0054 / 0.0548 | 0.0051 / 0.0445 |
| N / N(H = 1) | 2,899,899 / 19,736 | 2,764,217 / 18,530 |
| **A (b) Both spouses self-report (t+1)** | | |
| Husband becomes job loser (t+1) | n/a | n/a |
| Mean H = 0 / H = 1 (weighted) |  |  |
| N / N(H = 1) | 1,237 / 14 | 1,203 / 14 |
| **A (c) Wife self-reports, husband by proxy (t+1)** | | |
| Husband becomes job loser (t+1) | 0.038*** (0.002; p=<0.001) [0.004; p=<0.001] | 0.034*** (0.002; p=<0.001) [0.004; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0060 / 0.0547 | 0.0057 / 0.0449 |
| N / N(H = 1) | 1,589,024 / 10,065 | 1,523,514 / 9,493 |
| **A (c'') ... and the wife is the household respondent (she reports his job loss)** | | |
| Husband becomes job loser (t+1) | 0.039*** (0.002; p=<0.001) [0.004; p=<0.001] | 0.034*** (0.002; p=<0.001) [0.004; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0060 / 0.0552 | 0.0057 / 0.0447 |
| N / N(H = 1) | 1,497,408 / 9,414 | 1,432,121 / 8,844 |
| **A (d) Husband self-reports, wife by proxy (t+1)** | | |
| Husband becomes job loser (t+1) | 0.038*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.032*** (0.002; p=<0.001) [0.002; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0047 / 0.0492 | 0.0043 / 0.0393 |
| N / N(H = 1) | 1,157,187 / 8,502 | 1,091,929 / 7,938 |
| **A (d'') ... and the husband is the household respondent (he reports her job loss)** | | |
| Husband becomes job loser (t+1) | 0.039*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.032*** (0.002; p=<0.001) [0.002; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0047 / 0.0498 | 0.0042 / 0.0395 |
| N / N(H = 1) | 1,088,319 / 7,965 | 1,023,414 / 7,406 |
| **A (e) Both by proxy (another member reports both, t+1)** | | |
| Husband becomes job loser (t+1) | 0.093*** (0.010; p=<0.001) [0.015; p=<0.001] | 0.084*** (0.010; p=<0.001) [0.015; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0054 / 0.1119 | 0.0050 / 0.0908 |
| N / N(H = 1) | 119,677 / 874 | 115,147 / 809 |
| **A (f) One spouse reports both ((c) or (d); third-person reports excluded)** | | |
| Husband becomes job loser (t+1) | 0.038*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.033*** (0.001; p=<0.001) [0.003; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0054 / 0.0522 | 0.0051 / 0.0423 |
| N / N(H = 1) | 2,746,211 / 18,567 | 2,615,443 / 17,431 |
| **B (b) Both self-report at t and t+1** | | |
| Husband becomes job loser (t+1) | n/a | n/a |
| Mean H = 0 / H = 1 (weighted) |  |  |
| N / N(H = 1) | 29 / 0 | 29 / 0 |
| **B (c) Wife self, husband proxy at t and t+1** | | |
| Husband becomes job loser (t+1) | 0.037*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.031*** (0.002; p=<0.001) [0.003; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0059 / 0.0535 | 0.0056 / 0.0410 |
| N / N(H = 1) | 1,248,358 / 7,456 | 1,189,952 / 6,949 |
| **B (d) Husband self, wife proxy at t and t+1** | | |
| Husband becomes job loser (t+1) | 0.037*** (0.003; p=<0.001) [0.003; p=<0.001] | 0.030*** (0.002; p=<0.001) [0.002; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0046 / 0.0487 | 0.0041 / 0.0364 |
| N / N(H = 1) | 864,470 / 5,720 | 805,733 / 5,236 |
| **B (e) Both by proxy at t and t+1** | | |
| Husband becomes job loser (t+1) | 0.105*** (0.013; p=<0.001) [0.016; p=<0.001] | 0.095*** (0.013; p=<0.001) [0.016; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0057 / 0.1279 | 0.0051 / 0.0991 |
| N / N(H = 1) | 68,886 / 586 | 65,345 / 529 |
| Fixed effects | state x year-month | state x year-month |
| Clusters | household [state] | household [state] |

**Differences between reporting groups** (pooled LPM on the two groups, state x month FE; regressors H, group, H x group)

| Comparison | H x group | H (reference group) | N |
|---|---|---|---|
| (c'') wife reports both (vs (d'') husband reports both), t+1 | 0.0003 (0.0032; p=0.936) [0.0040; p=0.949] | 0.038*** (0.002; p=<0.001) [0.003; p=<0.001] | 2,585,727 |
| (c) vs (d), same status at t and t+1 | -0.0002 (0.0036; p=0.965) [0.0041; p=0.969] | 0.037*** (0.003; p=<0.001) [0.003; p=<0.001] | 2,112,828 |
| (e) third person reports both (vs (c) or (d)), t+1 | 0.058*** (0.011; p=<0.001) [0.013; p=<0.001] | 0.038*** (0.002; p=<0.001) [0.003; p=<0.001] | 2,865,888 |

The CPS takes one respondent per household and month, who answers for everyone else: couples in which both spouses self-report (b) are almost absent (cells n/a), so the review's sample (b) cannot be formed. The informative contrast is (c'') vs (d''): one spouse, the respondent, reports both statuses; if the joint loss were a reporting artefact of the respondent it should differ by who reports. Share of couple-months with the husband reporting both (d''): 0.374 when he stays employed, 0.401 when he becomes a job loser (a man at home is more often the respondent).

## 2. Temporary layoffs, seasonality, duration, class of worker

Columns: (1)-(2) wife becomes a job loser at t+1 (any reason code); (3)-(4) wife becomes a job loser other than on layoff (PRUNTYPE 2-3; wives on layoff at t+1 dropped); (5)-(6) wife becomes a job loser at t+1 and is still unemployed at t+2 (sample linked to t+2; husbands in the control group employed at t+1 and t+2). Row panels define the husband's event and the sample: 'other than on layoff' drops husbands whose job loss is PRUNTYPE 1; 'persistent' keeps husbands still unemployed at t+2 (t+2-linked sample in every column). Industry and class of worker refer to the main job at t; industry harmonised across the 2003 recode into 10 groups. Even columns exclude 2020-21 (item vi).

| | (1) wife job loser | (2) wife job loser, excl. 2020-21 | (3) wife job loser not on layoff | (4) wife not on layoff, excl. 2020-21 | (5) wife persistent job loser | (6) wife persistent, excl. 2020-21 |
|---|---|---|---|---|---|---|
| **(0) All** | | | | | | |
| Husband becomes job loser (t+1) | 0.040*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.035*** (0.001; p=<0.001) [0.003; p=<0.001] | 0.015*** (0.001; p=<0.001) [0.002; p=<0.001] | 0.015*** (0.001; p=<0.001) [0.002; p=<0.001] | 0.015*** (0.001; p=<0.001) [0.002; p=<0.001] | 0.013*** (0.001; p=<0.001) [0.002; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0054 / 0.0545 | 0.0051 / 0.0443 | 0.0023 / 0.0211 | 0.0023 / 0.0208 | 0.0020 / 0.0200 | 0.0018 / 0.0156 |
| N / N(H = 1) | 2,912,111 / 19,881 | 2,775,713 / 18,671 | 2,902,566 / 19,280 | 2,767,403 / 18,238 | 1,800,044 / 12,319 | 1,717,793 / 11,612 |
| **(i) His job loss other than on layoff (PRUNTYPE 2-3)** | | | | | | |
| Husband becomes job loser (t+1) | 0.027*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.027*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.026*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.025*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.012*** (0.001; p=<0.001) [0.002; p=<0.001] | 0.012*** (0.001; p=<0.001) [0.002; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0054 / 0.0377 | 0.0051 / 0.0360 | 0.0023 / 0.0330 | 0.0023 / 0.0319 | 0.0020 / 0.0164 | 0.0018 / 0.0155 |
| N / N(H = 1) | 2,902,407 / 10,177 | 2,766,871 / 9,829 | 2,893,414 / 10,128 | 2,758,951 / 9,786 | 1,794,027 / 6,302 | 1,712,283 / 6,102 |
| **(i') His job loss on layoff (PRUNTYPE 1) only** | | | | | | |
| Husband becomes job loser (t+1) | 0.054*** (0.002; p=<0.001) [0.005; p=<0.001] | 0.044*** (0.002; p=<0.001) [0.004; p=<0.001] | 0.0038*** (0.0008; p=<0.001) [0.0008; p=<0.001] | 0.0037*** (0.0008; p=<0.001) [0.0007; p=<0.001] | 0.017*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.013*** (0.002; p=<0.001) [0.003; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0054 / 0.0734 | 0.0051 / 0.0546 | 0.0023 / 0.0067 | 0.0023 / 0.0064 | 0.0020 / 0.0239 | 0.0018 / 0.0158 |
| N / N(H = 1) | 2,901,934 / 9,704 | 2,765,884 / 8,842 | 2,892,438 / 9,152 | 2,757,617 / 8,452 | 1,793,742 / 6,017 | 1,711,691 / 5,510 |
| **(ii) Job-loss month (t+1) not June-September** | | | | | | |
| Husband becomes job loser (t+1) | 0.037*** (0.002; p=<0.001) [0.004; p=<0.001] | 0.031*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.015*** (0.001; p=<0.001) [0.002; p=<0.001] | 0.015*** (0.001; p=<0.001) [0.002; p=<0.001] | 0.015*** (0.001; p=<0.001) [0.002; p=<0.001] | 0.012*** (0.001; p=<0.001) [0.002; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0048 / 0.0524 | 0.0045 / 0.0395 | 0.0022 / 0.0209 | 0.0022 / 0.0203 | 0.0018 / 0.0225 | 0.0017 / 0.0163 |
| N / N(H = 1) | 1,970,073 / 14,368 | 1,873,949 / 13,443 | 1,964,724 / 13,970 | 1,869,484 / 13,188 | 1,209,343 / 8,861 | 1,151,508 / 8,323 |
| **(i)+(ii) Not on layoff, not June-September** | | | | | | |
| Husband becomes job loser (t+1) | 0.026*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.025*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.025*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.024*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.012*** (0.002; p=<0.001) [0.002; p=<0.001] | 0.011*** (0.002; p=<0.001) [0.002; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0048 / 0.0366 | 0.0045 / 0.0344 | 0.0022 / 0.0328 | 0.0022 / 0.0315 | 0.0018 / 0.0172 | 0.0017 / 0.0155 |
| N / N(H = 1) | 1,962,751 / 7,046 | 1,867,308 / 6,802 | 1,957,773 / 7,019 | 1,863,075 / 6,779 | 1,204,850 / 4,368 | 1,147,411 / 4,226 |
| Fixed effects | state x year-month | state x year-month | state x year-month | state x year-month | state x year-month | state x year-month |
| Clusters | household [state] | household [state] | household [state] | household [state] | household [state] | household [state] |

**(iv) Persistent job loss of the husband (still unemployed at t+2); t+2-linked sample in every column**

| | (1) wife job loser | (2) wife job loser, excl. 2020-21 | (3) wife job loser not on layoff | (4) wife not on layoff, excl. 2020-21 | (5) wife persistent job loser | (6) wife persistent, excl. 2020-21 |
|---|---|---|---|---|---|---|
| **(0) All, t+2-linked sample** | | | | | | |
| Husband becomes job loser (t+1) | 0.038*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.034*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.014*** (0.001; p=<0.001) [0.002; p=<0.001] | 0.014*** (0.001; p=<0.001) [0.002; p=<0.001] | 0.015*** (0.001; p=<0.001) [0.002; p=<0.001] | 0.013*** (0.001; p=<0.001) [0.002; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0054 / 0.0516 | 0.0051 / 0.0417 | 0.0022 / 0.0191 | 0.0023 / 0.0187 | 0.0020 / 0.0200 | 0.0018 / 0.0156 |
| N / N(H = 1) | 1,800,044 / 12,319 | 1,717,793 / 11,612 | 1,794,237 / 11,959 | 1,712,713 / 11,343 | 1,800,044 / 12,319 | 1,717,793 / 11,612 |
| **(iv) His job loss persistent** | | | | | | |
| Husband becomes job loser (t+1) | 0.033*** (0.003; p=<0.001) [0.004; p=<0.001] | 0.028*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.017*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.017*** (0.002; p=<0.001) [0.002; p=<0.001] | 0.025*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.021*** (0.002; p=<0.001) [0.003; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0054 / 0.0455 | 0.0051 / 0.0356 | 0.0022 / 0.0223 | 0.0023 / 0.0215 | 0.0020 / 0.0317 | 0.0018 / 0.0243 |
| N / N(H = 1) | 1,793,386 / 5,661 | 1,711,527 / 5,346 | 1,787,817 / 5,539 | 1,706,636 / 5,266 | 1,793,386 / 5,661 | 1,711,527 / 5,346 |
| **(iv)+(i) Persistent and not on layoff** | | | | | | |
| Husband becomes job loser (t+1) | 0.027*** (0.003; p=<0.001) [0.004; p=<0.001] | 0.026*** (0.003; p=<0.001) [0.003; p=<0.001] | 0.025*** (0.003; p=<0.001) [0.004; p=<0.001] | 0.024*** (0.003; p=<0.001) [0.003; p=<0.001] | 0.018*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.018*** (0.002; p=<0.001) [0.003; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0054 / 0.0353 | 0.0051 / 0.0322 | 0.0022 / 0.0308 | 0.0023 / 0.0289 | 0.0020 / 0.0231 | 0.0018 / 0.0217 |
| N / N(H = 1) | 1,791,155 / 3,430 | 1,709,509 / 3,328 | 1,785,691 / 3,413 | 1,704,684 / 3,314 | 1,791,155 / 3,430 | 1,709,509 / 3,328 |
| **(iv)+(i)+(ii) Persistent, not on layoff, not June-September** | | | | | | |
| Husband becomes job loser (t+1) | 0.028*** (0.004; p=<0.001) [0.004; p=<0.001] | 0.026*** (0.004; p=<0.001) [0.004; p=<0.001] | 0.026*** (0.003; p=<0.001) [0.004; p=<0.001] | 0.025*** (0.003; p=<0.001) [0.004; p=<0.001] | 0.017*** (0.003; p=<0.001) [0.004; p=<0.001] | 0.016*** (0.003; p=<0.001) [0.004; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0047 / 0.0386 | 0.0044 / 0.0342 | 0.0022 / 0.0346 | 0.0022 / 0.0314 | 0.0018 / 0.0248 | 0.0017 / 0.0225 |
| N / N(H = 1) | 1,202,881 / 2,399 | 1,145,511 / 2,326 | 1,199,914 / 2,389 | 1,142,983 / 2,318 | 1,202,881 / 2,399 | 1,145,511 / 2,326 |
| Fixed effects | state x year-month | state x year-month | state x year-month | state x year-month | state x year-month | state x year-month |
| Clusters | household [state] | household [state] | household [state] | household [state] | household [state] | household [state] |

**(iii) By the husband's major industry at t (harmonised)**

| | (1) wife job loser | (2) wife job loser, excl. 2020-21 | (3) wife job loser not on layoff | (4) wife not on layoff, excl. 2020-21 | (5) wife persistent job loser | (6) wife persistent, excl. 2020-21 |
|---|---|---|---|---|---|---|
| **Agriculture, forestry, fishing, mining** | | | | | | |
| Husband becomes job loser (t+1) | 0.091*** (0.009; p=<0.001) [0.035; p=0.009] | 0.093*** (0.010; p=<0.001) [0.036; p=0.010] | 0.028*** (0.005; p=<0.001) [0.015; p=0.057] | 0.028*** (0.006; p=<0.001) [0.016; p=0.079] | 0.035*** (0.007; p=<0.001) [0.018; p=0.054] | 0.037*** (0.008; p=<0.001) [0.019; p=0.050] |
| Mean H = 0 / H = 1 (weighted) | 0.0061 / 0.1463 | 0.0061 / 0.1461 | 0.0017 / 0.0578 | 0.0017 / 0.0569 | 0.0017 / 0.0572 | 0.0017 / 0.0609 |
| N / N(H = 1) | 121,904 / 1,021 | 116,795 / 965 | 121,350 / 947 | 116,276 / 894 | 75,557 / 633 | 72,456 / 599 |
| **Construction** | | | | | | |
| Husband becomes job loser (t+1) | 0.021*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.019*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.0086*** (0.0014; p=<0.001) [0.0016; p=<0.001] | 0.0077*** (0.0013; p=<0.001) [0.0016; p=<0.001] | 0.0081*** (0.0016; p=<0.001) [0.0017; p=<0.001] | 0.0072*** (0.0016; p=<0.001) [0.0017; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0068 / 0.0338 | 0.0064 / 0.0278 | 0.0029 / 0.0141 | 0.0030 / 0.0122 | 0.0024 / 0.0119 | 0.0022 / 0.0097 |
| N / N(H = 1) | 338,094 / 6,004 | 322,311 / 5,750 | 336,720 / 5,897 | 321,115 / 5,665 | 206,264 / 3,749 | 196,885 / 3,595 |
| **Manufacturing** | | | | | | |
| Husband becomes job loser (t+1) | 0.040*** (0.004; p=<0.001) [0.004; p=<0.001] | 0.037*** (0.004; p=<0.001) [0.004; p=<0.001] | 0.013*** (0.002; p=<0.001) [0.002; p=<0.001] | 0.014*** (0.002; p=<0.001) [0.002; p=<0.001] | 0.011*** (0.003; p=<0.001) [0.003; p=<0.001] | 0.0090*** (0.0025; p=<0.001) [0.0027; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0061 / 0.0561 | 0.0058 / 0.0475 | 0.0026 / 0.0184 | 0.0026 / 0.0198 | 0.0023 / 0.0199 | 0.0021 / 0.0121 |
| N / N(H = 1) | 499,308 / 3,083 | 480,113 / 2,919 | 497,469 / 2,976 | 478,455 / 2,836 | 310,553 / 1,931 | 298,897 / 1,827 |
| **Wholesale and retail trade** | | | | | | |
| Husband becomes job loser (t+1) | 0.037*** (0.005; p=<0.001) [0.006; p=<0.001] | 0.030*** (0.004; p=<0.001) [0.005; p=<0.001] | 0.025*** (0.004; p=<0.001) [0.004; p=<0.001] | 0.024*** (0.004; p=<0.001) [0.004; p=<0.001] | 0.012*** (0.003; p=<0.001) [0.004; p=0.005] | 0.012*** (0.003; p=<0.001) [0.004; p=0.007] |
| Mean H = 0 / H = 1 (weighted) | 0.0053 / 0.0527 | 0.0050 / 0.0399 | 0.0024 / 0.0314 | 0.0024 / 0.0310 | 0.0021 / 0.0187 | 0.0020 / 0.0161 |
| N / N(H = 1) | 408,380 / 1,907 | 393,396 / 1,793 | 407,198 / 1,871 | 392,373 / 1,777 | 252,354 / 1,191 | 243,357 / 1,138 |
| **Transport, utilities, communications / information** | | | | | | |
| Husband becomes job loser (t+1) | 0.034*** (0.005; p=<0.001) [0.005; p=<0.001] | 0.026*** (0.004; p=<0.001) [0.005; p=<0.001] | 0.014*** (0.003; p=<0.001) [0.003; p=<0.001] | 0.014*** (0.003; p=<0.001) [0.003; p=<0.001] | 0.016*** (0.004; p=<0.001) [0.004; p=<0.001] | 0.010*** (0.003; p=0.002) [0.003; p=0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0056 / 0.0499 | 0.0053 / 0.0353 | 0.0024 / 0.0190 | 0.0024 / 0.0197 | 0.0022 / 0.0264 | 0.0021 / 0.0146 |
| N / N(H = 1) | 304,898 / 1,712 | 290,819 / 1,586 | 303,879 / 1,668 | 289,945 / 1,562 | 188,832 / 1,057 | 180,428 / 978 |
| **Finance, insurance, real estate** | | | | | | |
| Husband becomes job loser (t+1) | 0.022*** (0.006; p=<0.001) [0.007; p=<0.001] | 0.015*** (0.005; p=0.003) [0.005; p=0.006] | 0.013*** (0.004; p=0.001) [0.005; p=0.011] | 0.0091** (0.0037; p=0.015) [0.0045; p=0.044] | 0.0097** (0.0047; p=0.040) [0.0063; p=0.125] | 0.0021 (0.0029; p=0.475) [0.0036; p=0.562] |
| Mean H = 0 / H = 1 (weighted) | 0.0044 / 0.0302 | 0.0042 / 0.0178 | 0.0018 / 0.0159 | 0.0019 / 0.0098 | 0.0016 / 0.0177 | 0.0015 / 0.0072 |
| N / N(H = 1) | 174,424 / 632 | 164,839 / 593 | 173,953 / 624 | 164,430 / 588 | 108,175 / 386 | 102,335 / 366 |
| **Business, repair and professional services** | | | | | | |
| Husband becomes job loser (t+1) | 0.033*** (0.004; p=<0.001) [0.004; p=<0.001] | 0.029*** (0.004; p=<0.001) [0.004; p=<0.001] | 0.017*** (0.003; p=<0.001) [0.002; p=<0.001] | 0.017*** (0.003; p=<0.001) [0.002; p=<0.001] | 0.015*** (0.003; p=<0.001) [0.003; p=<0.001] | 0.014*** (0.003; p=<0.001) [0.003; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0053 / 0.0446 | 0.0049 / 0.0367 | 0.0022 / 0.0205 | 0.0023 / 0.0210 | 0.0018 / 0.0182 | 0.0017 / 0.0166 |
| N / N(H = 1) | 345,819 / 2,481 | 327,166 / 2,341 | 344,775 / 2,431 | 326,274 / 2,307 | 213,604 / 1,524 | 202,264 / 1,440 |
| **Education, health and social services** | | | | | | |
| Husband becomes job loser (t+1) | 0.091*** (0.008; p=<0.001) [0.010; p=<0.001] | 0.085*** (0.009; p=<0.001) [0.010; p=<0.001] | 0.011*** (0.003; p=0.001) [0.004; p=0.001] | 0.013*** (0.004; p=0.001) [0.004; p=0.001] | 0.027*** (0.006; p=<0.001) [0.007; p=<0.001] | 0.025*** (0.006; p=<0.001) [0.007; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0040 / 0.1011 | 0.0037 / 0.0907 | 0.0016 / 0.0139 | 0.0016 / 0.0161 | 0.0014 / 0.0293 | 0.0013 / 0.0258 |
| N / N(H = 1) | 330,809 / 1,140 | 312,642 / 1,014 | 329,914 / 1,041 | 311,880 / 935 | 205,338 / 679 | 194,286 / 606 |
| **Leisure, personal and other services (incl. private hh)** | | | | | | |
| Husband becomes job loser (t+1) | 0.054*** (0.006; p=<0.001) [0.006; p=<0.001] | 0.043*** (0.006; p=<0.001) [0.006; p=<0.001] | 0.025*** (0.004; p=<0.001) [0.004; p=<0.001] | 0.026*** (0.004; p=<0.001) [0.004; p=<0.001] | 0.017*** (0.005; p=<0.001) [0.005; p=<0.001] | 0.013*** (0.004; p=0.004) [0.004; p=0.004] |
| Mean H = 0 / H = 1 (weighted) | 0.0055 / 0.0728 | 0.0051 / 0.0473 | 0.0025 / 0.0305 | 0.0025 / 0.0312 | 0.0019 / 0.0214 | 0.0018 / 0.0144 |
| N / N(H = 1) | 196,522 / 1,569 | 185,633 / 1,404 | 195,896 / 1,505 | 185,128 / 1,376 | 119,537 / 965 | 113,130 / 870 |
| **Public administration** | | | | | | |
| Husband becomes job loser (t+1) | 0.042*** (0.011; p=<0.001) [0.011; p=<0.001] | 0.036*** (0.010; p=<0.001) [0.010; p=<0.001] | 0.014** (0.006; p=0.030) [0.006; p=0.027] | 0.015** (0.007; p=0.030) [0.007; p=0.027] | 0.012 (0.008; p=0.146) [0.008; p=0.135] | 0.013 (0.008; p=0.117) [0.008; p=0.104] |
| Mean H = 0 / H = 1 (weighted) | 0.0045 / 0.0599 | 0.0042 / 0.0444 | 0.0017 / 0.0174 | 0.0018 / 0.0191 | 0.0016 / 0.0109 | 0.0015 / 0.0117 |
| N / N(H = 1) | 191,953 / 332 | 181,999 / 306 | 191,412 / 320 | 181,527 / 298 | 119,830 / 204 | 113,755 / 193 |
| **Construction: his job loss other than on layoff** | | | | | | |
| Husband becomes job loser (t+1) | 0.022*** (0.004; p=<0.001) [0.004; p=<0.001] | 0.021*** (0.003; p=<0.001) [0.004; p=<0.001] | 0.019*** (0.003; p=<0.001) [0.003; p=<0.001] | 0.017*** (0.003; p=<0.001) [0.003; p=<0.001] | 0.0097*** (0.0029; p=<0.001) [0.0025; p=<0.001] | 0.0087*** (0.0028; p=0.002) [0.0026; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0068 / 0.0341 | 0.0064 / 0.0301 | 0.0029 / 0.0272 | 0.0030 / 0.0236 | 0.0024 / 0.0130 | 0.0022 / 0.0104 |
| N / N(H = 1) | 334,227 / 2,137 | 318,639 / 2,078 | 332,944 / 2,121 | 317,513 / 2,063 | 203,857 / 1,342 | 194,598 / 1,308 |
| **Manufacturing: his job loss other than on layoff** | | | | | | |
| Husband becomes job loser (t+1) | 0.023*** (0.004; p=<0.001) [0.004; p=<0.001] | 0.023*** (0.004; p=<0.001) [0.004; p=<0.001] | 0.020*** (0.004; p=<0.001) [0.003; p=<0.001] | 0.021*** (0.004; p=<0.001) [0.003; p=<0.001] | 0.0080** (0.0032; p=0.012) [0.0031; p=0.010] | 0.0084** (0.0033; p=0.010) [0.0032; p=0.008] |
| Mean H = 0 / H = 1 (weighted) | 0.0061 / 0.0335 | 0.0058 / 0.0347 | 0.0026 / 0.0285 | 0.0026 / 0.0295 | 0.0023 / 0.0116 | 0.0021 / 0.0121 |
| N / N(H = 1) | 497,790 / 1,565 | 478,720 / 1,526 | 496,049 / 1,556 | 477,136 / 1,517 | 309,605 / 983 | 298,026 / 956 |
| **Education, health and social services: his job loss other than on layoff** | | | | | | |
| Husband becomes job loser (t+1) | 0.020*** (0.006; p=0.001) [0.006; p=<0.001] | 0.022*** (0.007; p=<0.001) [0.007; p=<0.001] | 0.021*** (0.006; p=<0.001) [0.006; p=<0.001] | 0.023*** (0.006; p=<0.001) [0.006; p=<0.001] | 0.016** (0.007; p=0.020) [0.008; p=0.046] | 0.017** (0.007; p=0.018) [0.008; p=0.043] |
| Mean H = 0 / H = 1 (weighted) | 0.0040 / 0.0244 | 0.0037 / 0.0264 | 0.0016 / 0.0241 | 0.0016 / 0.0262 | 0.0014 / 0.0202 | 0.0013 / 0.0216 |
| N / N(H = 1) | 330,259 / 590 | 312,184 / 556 | 329,462 / 589 | 311,500 / 555 | 205,002 / 343 | 194,006 / 326 |
| Fixed effects | state x year-month | state x year-month | state x year-month | state x year-month | state x year-month | state x year-month |
| Clusters | household [state] | household [state] | household [state] | household [state] | household [state] | household [state] |

**(v) By both spouses' class of worker at t (private = for-profit or nonprofit; government = federal, state, local; self-employed = incorporated or not)**

| | (1) wife job loser | (2) wife job loser, excl. 2020-21 | (3) wife job loser not on layoff | (4) wife not on layoff, excl. 2020-21 | (5) wife persistent job loser | (6) wife persistent, excl. 2020-21 |
|---|---|---|---|---|---|---|
| **Husband private, wife private** | | | | | | |
| Husband becomes job loser (t+1) | 0.041*** (0.002; p=<0.001) [0.005; p=<0.001] | 0.036*** (0.002; p=<0.001) [0.005; p=<0.001] | 0.017*** (0.001; p=<0.001) [0.002; p=<0.001] | 0.017*** (0.001; p=<0.001) [0.002; p=<0.001] | 0.017*** (0.002; p=<0.001) [0.002; p=<0.001] | 0.015*** (0.002; p=<0.001) [0.002; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0059 / 0.0563 | 0.0056 / 0.0469 | 0.0029 / 0.0233 | 0.0029 / 0.0234 | 0.0024 / 0.0239 | 0.0022 / 0.0183 |
| N / N(H = 1) | 1,526,975 / 12,752 | 1,454,135 / 12,011 | 1,522,087 / 12,369 | 1,449,908 / 11,735 | 939,644 / 7,896 | 895,955 / 7,476 |
| **Husband private, wife government** | | | | | | |
| Husband becomes job loser (t+1) | 0.013*** (0.003; p=<0.001) [0.003; p=<0.001] | 0.0069*** (0.0022; p=0.002) [0.0030; p=0.019] | 0.0020* (0.0011; p=0.063) [0.0010; p=0.054] | 0.0017 (0.0011; p=0.115) [0.0010; p=0.098] | 0.0037** (0.0018; p=0.037) [0.0018; p=0.043] | 0.0013 (0.0014; p=0.332) [0.0014; p=0.358] |
| Mean H = 0 / H = 1 (weighted) | 0.0060 / 0.0282 | 0.0056 / 0.0159 | 0.0012 / 0.0053 | 0.0012 / 0.0048 | 0.0016 / 0.0082 | 0.0015 / 0.0030 |
| N / N(H = 1) | 341,824 / 2,463 | 324,720 / 2,306 | 340,171 / 2,423 | 323,269 / 2,284 | 212,298 / 1,511 | 201,890 / 1,406 |
| **Husband private, wife self-employed** | | | | | | |
| Husband becomes job loser (t+1) | 0.026*** (0.005; p=<0.001) [0.005; p=<0.001] | 0.021*** (0.005; p=<0.001) [0.005; p=<0.001] | 0.014*** (0.004; p=<0.001) [0.004; p=<0.001] | 0.014*** (0.004; p=<0.001) [0.004; p=<0.001] | 0.0046* (0.0026; p=0.080) [0.0024; p=0.059] | 0.0037 (0.0026; p=0.159) [0.0024; p=0.120] |
| Mean H = 0 / H = 1 (weighted) | 0.0059 / 0.0419 | 0.0054 / 0.0298 | 0.0022 / 0.0209 | 0.0022 / 0.0206 | 0.0017 / 0.0060 | 0.0016 / 0.0047 |
| N / N(H = 1) | 142,190 / 962 | 135,061 / 911 | 141,684 / 944 | 134,631 / 900 | 88,419 / 600 | 84,062 / 572 |
| **Husband government, wife private** | | | | | | |
| Husband becomes job loser (t+1) | 0.027*** (0.007; p=<0.001) [0.005; p=<0.001] | 0.024*** (0.006; p=<0.001) [0.006; p=<0.001] | 0.0083** (0.0038; p=0.029) [0.0034; p=0.015] | 0.0089** (0.0041; p=0.029) [0.0037; p=0.015] | 0.0060 (0.0043; p=0.161) [0.0043; p=0.157] | 0.0069 (0.0046; p=0.131) [0.0045; p=0.125] |
| Mean H = 0 / H = 1 (weighted) | 0.0046 / 0.0340 | 0.0044 / 0.0285 | 0.0020 / 0.0107 | 0.0021 / 0.0117 | 0.0017 / 0.0104 | 0.0016 / 0.0114 |
| N / N(H = 1) | 236,805 / 624 | 225,814 / 576 | 236,186 / 609 | 225,267 / 565 | 147,354 / 387 | 140,691 / 360 |
| **Husband government, wife government** | | | | | | |
| Husband becomes job loser (t+1) | 0.153*** (0.016; p=<0.001) [0.018; p=<0.001] | 0.156*** (0.017; p=<0.001) [0.020; p=<0.001] | 0.013** (0.006; p=0.024) [0.006; p=0.030] | 0.014** (0.006; p=0.024) [0.006; p=0.029] | 0.040*** (0.010; p=<0.001) [0.011; p=<0.001] | 0.040*** (0.010; p=<0.001) [0.012; p=0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0038 / 0.1779 | 0.0035 / 0.1843 | 0.0009 / 0.0135 | 0.0009 / 0.0156 | 0.0011 / 0.0377 | 0.0011 / 0.0422 |
| N / N(H = 1) | 174,694 / 441 | 166,210 / 399 | 174,117 / 373 | 165,692 / 338 | 109,147 / 275 | 103,966 / 250 |
| **Husband government, wife self-employed** | | | | | | |
| Husband becomes job loser (t+1) | 0.035 (0.031; p=0.252) [0.037; p=0.343] | 0.020 (0.032; p=0.537) [0.037; p=0.589] | 0.025 (0.027; p=0.360) [0.031; p=0.419] | 0.028 (0.030; p=0.360) [0.034; p=0.418] | n/a | n/a |
| Mean H = 0 / H = 1 (weighted) | 0.0051 / 0.0740 | 0.0048 / 0.0340 | 0.0022 / 0.0306 | 0.0024 / 0.0340 |  |  |
| N / N(H = 1) | 29,165 / 49 | 27,688 / 42 | 29,082 / 48 | 27,622 / 42 | 18,373 / 34 | 17,454 / 31 |
| **Husband self-employed, wife private** | | | | | | |
| Husband becomes job loser (t+1) | 0.025*** (0.004; p=<0.001) [0.005; p=<0.001] | 0.020*** (0.004; p=<0.001) [0.005; p=<0.001] | 0.014*** (0.003; p=<0.001) [0.003; p=<0.001] | 0.013*** (0.003; p=<0.001) [0.003; p=<0.001] | 0.0077*** (0.0027; p=0.004) [0.0030; p=0.011] | 0.0078*** (0.0028; p=0.005) [0.0031; p=0.014] |
| Mean H = 0 / H = 1 (weighted) | 0.0048 / 0.0404 | 0.0045 / 0.0304 | 0.0022 / 0.0204 | 0.0022 / 0.0189 | 0.0020 / 0.0121 | 0.0019 / 0.0127 |
| N / N(H = 1) | 245,460 / 1,754 | 235,563 / 1,658 | 244,800 / 1,726 | 234,998 / 1,642 | 151,171 / 1,083 | 145,272 / 1,029 |
| **Husband self-employed, wife government** | | | | | | |
| Husband becomes job loser (t+1) | 0.019*** (0.006; p=0.002) [0.007; p=0.007] | 0.013** (0.006; p=0.023) [0.006; p=0.025] | 0.0073** (0.0033; p=0.026) [0.0044; p=0.098] | 0.0052* (0.0029; p=0.073) [0.0038; p=0.178] | 0.0040 (0.0028; p=0.157) [0.0041; p=0.329] | n/a |
| Mean H = 0 / H = 1 (weighted) | 0.0039 / 0.0325 | 0.0038 / 0.0180 | 0.0005 / 0.0062 | 0.0005 / 0.0035 | 0.0008 / 0.0048 |  |
| N / N(H = 1) | 75,083 / 407 | 72,209 / 376 | 74,822 / 401 | 71,966 / 372 | 46,741 / 253 | 45,005 / 230 |
| **Husband self-employed, wife self-employed** | | | | | | |
| Husband becomes job loser (t+1) | 0.159*** (0.016; p=<0.001) [0.017; p=<0.001] | 0.142*** (0.017; p=<0.001) [0.015; p=<0.001] | 0.073*** (0.013; p=<0.001) [0.014; p=<0.001] | 0.068*** (0.013; p=<0.001) [0.014; p=<0.001] | 0.043*** (0.012; p=<0.001) [0.015; p=0.003] | 0.041*** (0.013; p=0.001) [0.014; p=0.004] |
| Mean H = 0 / H = 1 (weighted) | 0.0030 / 0.1793 | 0.0028 / 0.1501 | 0.0010 / 0.0898 | 0.0010 / 0.0782 | 0.0007 / 0.0459 | 0.0007 / 0.0422 |
| N / N(H = 1) | 133,884 / 403 | 128,453 / 369 | 133,598 / 361 | 128,202 / 337 | 83,206 / 265 | 79,914 / 245 |
| **Both private, his job loss other than on layoff** | | | | | | |
| Husband becomes job loser (t+1) | 0.030*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.030*** (0.002; p=<0.001) [0.004; p=<0.001] | 0.029*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.029*** (0.002; p=<0.001) [0.004; p=<0.001] | 0.015*** (0.002; p=<0.001) [0.002; p=<0.001] | 0.015*** (0.002; p=<0.001) [0.002; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0059 / 0.0409 | 0.0056 / 0.0399 | 0.0029 / 0.0371 | 0.0029 / 0.0366 | 0.0024 / 0.0198 | 0.0022 / 0.0191 |
| N / N(H = 1) | 1,520,806 / 6,583 | 1,448,484 / 6,360 | 1,516,274 / 6,556 | 1,444,509 / 6,336 | 935,800 / 4,052 | 892,405 / 3,926 |
| Fixed effects | state x year-month | state x year-month | state x year-month | state x year-month | state x year-month | state x year-month |
| Clusters | household [state] | household [state] | household [state] | household [state] | household [state] | household [state] |

## 3. Same-employer bound

Arithmetic. Let a share s of couples work at the same establishment and suppose that, when the husband loses his job, the wife in such a couple loses hers in the same month with probability p, while all other wives lose theirs at the base rate p0 = 0.0054. Then P(w | h) - p0 = s (p - p0), so p = p0 + excess / s. Hyatt (2019, Monthly Labor Review, LEHD): 10-12% of dual-earner couples work at the same establishment. The last column lets couples outside the same establishment keep the excess estimated for couples in different major industries (0.017*** (0.001; p=<0.001) [0.002; p=<0.001]), so the same-employer p it gives is a lower bound.

| s (share at the same establishment) | p reproducing the state x month FE excess 0.0401 | p reproducing the raw difference 0.0491 | p if other couples keep 0.0174 |
|---|---|---|---|
| 0.10 | 0.406 | 0.496 | 0.250 |
| 0.11 | 0.370 | 0.452 | 0.230 |
| 0.12 | 0.340 | 0.414 | 0.212 |

**The tightest CPS proxies for a shared employer.** Shares are weighted shares of couples in the sample with H = 0 / H = 1; 'contribution' = share of H = 1 couples in the group x (P(w|h) - P(w|not h) within the group), divided by the raw difference P(w|h) - P(w|not h) in the whole sample.

| Match of the spouses' main jobs at t | Share H = 0 | Share H = 1 | P(w\|not h) / P(w\|h) in group | Excess in group (state x month FE) | N / N(H = 1) | Contribution to raw excess |
|---|---|---|---|---|---|---|
| Same major industry | 0.2278 | 0.1556 | 0.0044 / 0.1833 | 0.166*** (0.007; p=<0.001) [0.011; p=<0.001] | 656,004 / 3,028 | 0.567 |
| Same detailed industry | 0.1773 | 0.1159 | 0.0041 / 0.2299 | 0.211*** (0.009; p=<0.001) [0.013; p=<0.001] | 515,458 / 2,274 | 0.533 |
| Same detailed industry x same detailed occupation | 0.0737 | 0.0560 | 0.0041 / 0.3355 | 0.315*** (0.014; p=<0.001) [0.020; p=<0.001] | 209,989 / 1,037 | 0.378 |
| Same detailed industry x detailed occupation x class of worker | 0.0628 | 0.0490 | 0.0041 / 0.3573 | 0.337*** (0.015; p=<0.001) [0.019; p=<0.001] | 179,021 / 905 | 0.353 |
| All couples not in the tightest cell | 0.9372 | 0.9510 | 0.0055 / 0.0389 | 0.026*** (0.001; p=<0.001) [0.002; p=<0.001] | 2,733,090 / 18,976 | |

The tightest proxy covers 6.3% of couples (weighted, H = 0) against 10-12% at the same establishment in the LEHD; within it the wife loses her job in the husband's month with probability 0.357. The proxy is too wide (same cell, different employer) and too narrow (same employer, different occupation or class), so it brackets rather than measures the same-employer channel; the LEHD is needed for the definitive answer.

## 4. Selection: couples observed in all four months of the rotation

A couple-month counts as fully observed if the same couple (both spouses, still naming each other, same line numbers) is linked in the other months of its 4-month rotation (base months with household-ID breaks count as not linked). Share fully observed (unweighted): 0.878 when the husband stays employed, 0.855 when he becomes a job loser.

| | (1) wife job loser t+1 | (2) wife job loser t+1, excl. 2020-21 |
|---|---|---|
| **All couples** | | |
| Husband becomes job loser (t+1) | 0.040*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.035*** (0.001; p=<0.001) [0.003; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0054 / 0.0545 | 0.0051 / 0.0443 |
| N / N(H = 1) | 2,912,111 / 19,881 | 2,775,713 / 18,671 |
| **Observed in all four months** | | |
| Husband becomes job loser (t+1) | 0.038*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.033*** (0.002; p=<0.001) [0.003; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0054 / 0.0525 | 0.0051 / 0.0426 |
| N / N(H = 1) | 2,554,988 / 16,989 | 2,439,688 / 16,031 |
| **Not observed in all four months** | | |
| Husband becomes job loser (t+1) | 0.052*** (0.004; p=<0.001) [0.004; p=<0.001] | 0.045*** (0.004; p=<0.001) [0.004; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0057 / 0.0657 | 0.0054 / 0.0545 |
| N / N(H = 1) | 357,123 / 2,892 | 336,025 / 2,640 |
| Fixed effects | state x year-month | state x year-month |
| Clusters | household [state] | household [state] |

## 5. Figure 1: the wife's excess monthly job-loss hazard around the husband's job-loss month

tau = month in which the husband becomes a job loser. tau-2..tau+2 as in 30 (flow events: employed in the previous month, job loser now; base month tau-1; control husbands employed in every month of the window). At tau-3 the wife's previous month, and at tau+3 the husband's, falls outside the 4-month rotation: there that spouse's job loss is a job loser with unemployment duration <= 4 weeks (risk set: employed or such a new job loser); base month tau-1 (tau-3) or tau (tau+3). The 'duration' columns redo tau-2, tau and tau+2 with the same duration rule (tau: both spouses by duration in one month, no linkage at all). 79% of flow job losers report a duration of 4 weeks or less.

| | (1) wife job loser at tau-3 | (2) wife job loser at tau-2 | (3) wife job loser at tau-2 duration | (4) wife job loser at tau-1 | (5) wife job loser at tau | (6) wife job loser at tau duration | (7) wife job loser at tau+1 | (8) wife job loser at tau+2 | (9) wife job loser at tau+2 duration | (10) wife job loser at tau+3 |
|---|---|---|---|---|---|---|---|---|---|---|
| Husband job loser at tau | 0.0057*** (0.0016; p=<0.001) [0.0022; p=0.009] | 0.0055*** (0.0016; p=<0.001) [0.0014; p=<0.001] | 0.0070*** (0.0011; p=<0.001) [0.0013; p=<0.001] | 0.0071*** (0.0011; p=<0.001) [0.0013; p=<0.001] | 0.040*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.041*** (0.001; p=<0.001) [0.004; p=<0.001] | 0.0084*** (0.0011; p=<0.001) [0.0012; p=<0.001] | 0.0063*** (0.0014; p=<0.001) [0.0017; p=<0.001] | 0.0056*** (0.0010; p=<0.001) [0.0010; p=<0.001] | 0.0081*** (0.0015; p=<0.001) [0.0016; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.0056 / 0.0116 | 0.0054 / 0.0108 | 0.0055 / 0.0141 | 0.0053 / 0.0144 | 0.0054 / 0.0545 | 0.0055 / 0.0542 | 0.0053 / 0.0159 | 0.0052 / 0.0129 | 0.0053 / 0.0114 | 0.0052 / 0.0142 |
| N / N(H = 1) | 837,838 / 4,456 | 833,349 / 4,406 | 1,807,609 / 10,459 | 1,798,024 / 10,326 | 2,912,111 / 19,881 | 4,298,019 / 28,130 | 1,795,387 / 11,850 | 830,606 / 5,715 | 1,795,496 / 11,959 | 830,924 / 6,033 |
| Fixed effects | state x year-month | state x year-month | state x year-month | state x year-month | state x year-month | state x year-month | state x year-month | state x year-month | state x year-month | state x year-month |
| Clusters | household [state] | household [state] | household [state] | household [state] | household [state] | household [state] | household [state] | household [state] | household [state] | household [state] |

**Panel B of the second figure: wives not employed at t (30's section 5)**

| | (1) wife employed at t+1 | (2) wife employed at t+2 | (3) wife employed at t+3 | (4) wife employed at t+12 | (5) wife unemployed (looking / layoff) at t+1 | (6) wife unemployed (looking / layoff) at t+2 | (7) wife unemployed (looking / layoff) at t+3 | (8) wife unemployed (looking / layoff) at t+12 |
|---|---|---|---|---|---|---|---|---|
| Husband becomes job loser (t+1) | 0.022*** (0.003; p=<0.001) [0.003; p=<0.001] | 0.033*** (0.004; p=<0.001) [0.006; p=<0.001] | 0.042*** (0.007; p=<0.001) [0.008; p=<0.001] | 0.040*** (0.008; p=<0.001) [0.008; p=<0.001] | 0.088*** (0.004; p=<0.001) [0.003; p=<0.001] | 0.072*** (0.004; p=<0.001) [0.004; p=<0.001] | 0.064*** (0.006; p=<0.001) [0.006; p=<0.001] | 0.039*** (0.005; p=<0.001) [0.006; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.075 / 0.095 | 0.098 / 0.127 | 0.113 / 0.147 | 0.192 / 0.232 | 0.060 / 0.154 | 0.053 / 0.129 | 0.048 / 0.124 | 0.034 / 0.081 |
| N / N(H = 1) | 1,076,046 / 10,162 | 655,122 / 6,194 | 297,891 / 2,854 | 359,866 / 3,036 | 1,076,046 / 10,162 | 655,122 / 6,194 | 297,891 / 2,854 | 359,866 / 3,036 |
| Fixed effects | state x year-month | state x year-month | state x year-month | state x year-month | state x year-month | state x year-month | state x year-month | state x year-month |

Figure files: `paperA_joint_loss/fig_cps_monthly_hazard.pdf` / `.png` (single panel, 95% CIs from household-clustered s.e.) and `fig_cps_monthly_hazard_awe.png` (adds panel B). The CPS observes t+1..t+3 and t+12 only (rotation 4-8-4).
