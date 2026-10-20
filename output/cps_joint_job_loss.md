# Joint job loss within married couples: CPS monthly panel

Built by `IGE/30.CPSJointJobLoss.py` (2026-10-17; definitions in its docstring). CPS basic monthly 1994-2023 from the Census API; married couples (both spouses married-spouse-present, naming each other as spouse, both aged 20-60 at t) linked month to month within the 4-month rotation and from MIS 1-4 to MIS 5-8 twelve months later. **Job loser** = unemployed (on layoff or looking) with PRUNTYPE = job loser on layoff / other job loser / temporary job ended, after being employed the month before. Probabilities are weighted by the wife's composite weight at t; regressions are unweighted linear probability models. Cells: coefficient*** (s.e. clustered by household; p) [s.e. clustered by state; p]; *** p<0.01, ** p<0.05, * p<0.1. Households are nested in states, so two-way household x state clustering equals state clustering. Associations, not causal effects: state x month fixed effects absorb common local shocks; a shared employer or sector remains inside the estimate by design.

## 0. Data

Variables requested but not offered by the API (from the raw-file headers; 'part of the year' = missing in some months). The requested list is in `req_vars()`.

| Year | Months | Missing all year | Missing part of the year |
|---|---|---|---|
| 1994 | 12 | PEPAR1, PEPAR2, PRCHLD, PRNMCHLD | - |
| 1995 | 12 | PEPAR1, PEPAR2, PRCHLD, PRNMCHLD | - |
| 1996 | 12 | PEPAR1, PEPAR2, PRCHLD, PRNMCHLD | - |
| 1997 | 12 | PEPAR1, PEPAR2, PRCHLD, PRNMCHLD | - |
| 1998 | 12 | PEPAR1, PEPAR2, PRCHLD, PRNMCHLD | - |
| 1999 | 12 | PEPAR1, PEPAR2 | PRCHLD, PRNMCHLD |
| 2000 | 12 | PEPAR1, PEPAR2 | - |
| 2001 | 12 | PEPAR1, PEPAR2 | - |
| 2002 | 12 | PEPAR1, PEPAR2 | - |
| 2003 | 12 | PEPAR1, PEPAR2 | - |
| 2004 | 12 | PEPAR1, PEPAR2 | - |
| 2005 | 12 | PEPAR1, PEPAR2 | - |
| 2006 | 12 | PEPAR1, PEPAR2 | - |
| 2007 | 12 | PEPAR1, PEPAR2 | - |
| 2008 | 12 | PEPAR1, PEPAR2 | - |
| 2009 | 12 | PEPAR1, PEPAR2 | - |
| 2010 | 12 | PEPAR1, PEPAR2 | - |
| 2011 | 12 | PEPAR1, PEPAR2 | - |
| 2012 | 12 | PEPAR1, PEPAR2 | - |
| 2013 | 12 | PEPAR1, PEPAR2 | - |
| 2014 | 12 | PEPAR1, PEPAR2 | - |
| 2015 | 12 | PEPAR1, PEPAR2 | - |
| 2016 | 12 | PEPAR1, PEPAR2 | - |
| 2017 | 12 | PEPAR1, PEPAR2 | - |
| 2018 | 12 | PEPAR1, PEPAR2 | - |
| 2019 | 12 | PEPAR1, PEPAR2 | - |
| 2020 | 12 | PEPARENT | - |
| 2021 | 12 | PEPARENT | - |
| 2022 | 12 | PEPARENT | - |
| 2023 | 12 | PEPARENT | - |

Couple-months: 6,666,364; distinct couples (household + both line numbers): 1,299,174; months: 360. Share Black (husband): 0.065; both employed at t: 0.637.

Link rate t -> t+1 (couples in MIS 1-3 / 5-7 found as the same couple next month): median 0.948, 10th percentile 0.906. Base months dropped (link rate < 0.5; household-ID breaks): 1995-05, 1995-06, 1995-07, 1995-08, 1996-12, 2004-04. Twelve-month link (MIS j -> j+4): median 0.742; base months with a usable twelve-month link (rate >= 0.5): 320 of 348 (the 1994-95 sample redesign, the 1995 and 2004 identifier changes and the January 1997 API file, which has about half the usual records, break links).

## 1. Joint job loss: wife's job-loss probability by the husband's transition

Both spouses employed at t. H = 1: husband becomes a job loser at t+1; H = 0: husband stays employed (through the end of the window). Wife's event: becomes a job loser in the window (from employment). The one-year column compares statuses at t and t+12 (12-month link; transitions in between are not observed). Regression row: LPM of the wife's event on H with state x year-month fixed effects.

| | (1) Same month (t+1) | (2) Within 1 month after (t+1..t+2) | (3) Within 2 months after (t+1..t+3) | (4) One year later (MIS j -> j+4, status at t+12) |
|---|---|---|---|---|
| P(wife job loser \| husband job loser) | 0.0545 | 0.0638 | 0.0746 | 0.0581 |
| P(wife job loser \| husband stays employed) | 0.0054 | 0.0099 | 0.0140 | 0.0105 |
| Difference | 0.0491 | 0.0539 | 0.0606 | 0.0476 |
| Ratio | 10.1 | 6.5 | 5.3 | 5.5 |
| P(husband job loser) | 0.0070 | 0.0070 | 0.0071 | 0.0149 |
| Phi correlation of the two events (this sample) | 0.054 | 0.045 | 0.043 | 0.055 |
| Regression: husband job loser (state x ym FE) | 0.040*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.044*** (0.002; p=<0.001) [0.004; p=<0.001] | 0.048*** (0.003; p=<0.001) [0.005; p=<0.001] | 0.039*** (0.002; p=<0.001) [0.003; p=<0.001] |
| N couples (H = 0 + H = 1) | 2,912,111 | 1,800,044 | 834,587 | 1,407,661 |
| N husband job losers / joint events | 19,881 / 944 | 12,319 / 693 | 5,826 / 374 | 20,054 / 1,070 |
| Clusters: households / states | 773,751 / 51 | 684,688 / 51 | 589,162 / 51 | 440,902 / 51 |

Phi correlation of the same-month events among all couples employed at t (husband's other transitions kept): 0.053. Joint same-month job-loss rate: observed 0.000375 vs 0.000040 under independence (ratio 9.4).

## 2. Does the excess survive local shocks? Same-month joint job loss with fixed effects

Sample: column (1) of section 1. Controls: age group (20-29/30-39/40-49/50-60) and education (<HS, HS, some college, BA+) of each spouse, husband's race, youngest own child (none / 0-5 / 6-17). Same industry / occupation: equal major group of the main job at t (14 / 11 groups from 2003, 22 / 14 before).

**Outcome: Wife becomes job loser at t+1**

| | (1) none | (2) year-month FE | (3) state x year-month FE | (4) (3) + controls | (5) state x ym x wife's industry FE + controls | (6) (4) + same industry / occupation | (7) (4), excluding 2020-21 |
|---|---|---|---|---|---|---|---|
| Husband becomes job loser (t+1) | 0.042*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.041*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.040*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.039*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.037*** (0.001; p=<0.001) [0.003; p=<0.001] | 0.011*** (0.001; p=<0.001) [0.001; p=<0.001] | 0.034*** (0.001; p=<0.001) [0.003; p=<0.001] |
| x same major industry |  |  |  |  |  | 0.128*** (0.007; p=<0.001) [0.009; p=<0.001] |  |
| x same major occupation |  |  |  |  |  | 0.053*** (0.005; p=<0.001) [0.007; p=<0.001] |  |
| Same major industry |  |  |  |  |  | -0.0014*** (0.0001; p=<0.001) [0.0001; p=<0.001] |  |
| Same major occupation |  |  |  |  |  | -0.0001 (0.0001; p=0.612) [0.0001; p=0.639] |  |
| Fixed effects | none | year-month | state x ym | state x ym | state x ym x wife's major industry | state x ym | state x ym |
| Controls | no | no | no | yes | yes | yes | yes |
| Mean of outcome, H = 0 (unweighted) | 0.0052 | 0.0052 | 0.0052 | 0.0052 | 0.0052 | 0.0052 | 0.0050 |
| N / FE groups | 2,912,111 / 0 | 2,912,111 / 353 | 2,912,111 / 17,978 | 2,912,111 / 17,978 | 2,912,111 / 243,146 | 2,912,111 / 17,978 | 2,794,827 / 16,856 |
| Clusters: households / states | 773,751 / 51 | 773,751 / 51 | 773,751 / 51 | 773,751 / 51 | 773,751 / 51 | 773,751 / 51 | 754,860 / 51 |

**Outcome: Wife leaves employment at t+1 (any)**

| | (1) none | (2) year-month FE | (3) state x year-month FE | (4) (3) + controls | (5) state x ym x wife's industry FE + controls | (6) (4) + same industry / occupation | (7) (4), excluding 2020-21 |
|---|---|---|---|---|---|---|---|
| Husband becomes job loser (t+1) | 0.058*** (0.002; p=<0.001) [0.004; p=<0.001] | 0.056*** (0.002; p=<0.001) [0.004; p=<0.001] | 0.055*** (0.002; p=<0.001) [0.004; p=<0.001] | 0.051*** (0.002; p=<0.001) [0.004; p=<0.001] | 0.047*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.017*** (0.002; p=<0.001) [0.002; p=<0.001] | 0.046*** (0.002; p=<0.001) [0.003; p=<0.001] |
| x same major industry |  |  |  |  |  | 0.153*** (0.008; p=<0.001) [0.011; p=<0.001] |  |
| x same major occupation |  |  |  |  |  | 0.066*** (0.007; p=<0.001) [0.009; p=<0.001] |  |
| Same major industry |  |  |  |  |  | 0.0015*** (0.0003; p=<0.001) [0.0004; p=<0.001] |  |
| Same major occupation |  |  |  |  |  | -0.0035*** (0.0003; p=<0.001) [0.0003; p=<0.001] |  |
| Fixed effects | none | year-month | state x ym | state x ym | state x ym x wife's major industry | state x ym | state x ym |
| Controls | no | no | no | yes | yes | yes | yes |
| Mean of outcome, H = 0 (unweighted) | 0.0305 | 0.0305 | 0.0305 | 0.0305 | 0.0305 | 0.0305 | 0.0304 |
| N / FE groups | 2,912,111 / 0 | 2,912,111 / 353 | 2,912,111 / 17,978 | 2,912,111 / 17,978 | 2,912,111 / 243,146 | 2,912,111 / 17,978 | 2,794,827 / 16,856 |
| Clusters: households / states | 773,751 / 51 | 773,751 / 51 | 773,751 / 51 | 773,751 / 51 | 773,751 / 51 | 773,751 / 51 | 754,860 / 51 |

## 3. Heterogeneity (state x year-month FE within each sample)

Row panels are samples; each column is a separate regression of the outcome in its header on H with state x year-month FE. Means are weighted. 'His job loss: type' compares husbands with that type of job loss with husbands who stay employed.

| | (1) Wife job loser, same month | (2) Wife job loser within 2 months after | (3) Wife leaves employment, same month |
|---|---|---|---|
| **All** | | | |
| Husband becomes job loser | 0.040*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.048*** (0.003; p=<0.001) [0.005; p=<0.001] | 0.055*** (0.002; p=<0.001) [0.004; p=<0.001] |
| Mean H = 0 / H = 1 | 0.0054 / 0.0545 | 0.0140 / 0.0746 | 0.0316 / 0.0980 |
| N / N(H = 1) | 2,912,111 / 19,881 | 834,587 / 5,826 | 2,912,111 / 19,881 |
| **Black couples (husband's race)** | | | |
| Husband becomes job loser | 0.044*** (0.005; p=<0.001) [0.006; p=<0.001] | 0.063*** (0.011; p=<0.001) [0.012; p=<0.001] | 0.055*** (0.006; p=<0.001) [0.008; p=<0.001] |
| Mean H = 0 / H = 1 | 0.0060 / 0.0613 | 0.0157 / 0.0916 | 0.0305 / 0.0973 |
| N / N(H = 1) | 176,506 / 1,826 | 47,673 / 523 | 176,506 / 1,826 |
| **White couples (husband's race)** | | | |
| Husband becomes job loser | 0.038*** (0.002; p=<0.001) [0.004; p=<0.001] | 0.046*** (0.003; p=<0.001) [0.006; p=<0.001] | 0.052*** (0.002; p=<0.001) [0.005; p=<0.001] |
| Mean H = 0 / H = 1 | 0.0054 / 0.0516 | 0.0140 / 0.0723 | 0.0315 / 0.0952 |
| N / N(H = 1) | 2,552,753 / 16,685 | 736,254 / 4,897 | 2,552,753 / 16,685 |
| **Same major industry** | | | |
| Husband becomes job loser | 0.166*** (0.007; p=<0.001) [0.011; p=<0.001] | 0.179*** (0.012; p=<0.001) [0.018; p=<0.001] | 0.209*** (0.008; p=<0.001) [0.014; p=<0.001] |
| Mean H = 0 / H = 1 | 0.0044 / 0.1833 | 0.0117 / 0.2129 | 0.0320 / 0.2556 |
| N / N(H = 1) | 656,004 / 3,028 | 188,068 / 902 | 656,004 / 3,028 |
| **Different major industry (both known)** | | | |
| Husband becomes job loser | 0.017*** (0.001; p=<0.001) [0.002; p=<0.001] | 0.024*** (0.003; p=<0.001) [0.003; p=<0.001] | 0.028*** (0.002; p=<0.001) [0.002; p=<0.001] |
| Mean H = 0 / H = 1 | 0.0057 / 0.0308 | 0.0147 / 0.0487 | 0.0314 / 0.0690 |
| N / N(H = 1) | 2,256,107 / 16,853 | 646,519 / 4,924 | 2,256,107 / 16,853 |
| **Same major occupation** | | | |
| Husband becomes job loser | 0.125*** (0.006; p=<0.001) [0.010; p=<0.001] | 0.143*** (0.011; p=<0.001) [0.017; p=<0.001] | 0.159*** (0.007; p=<0.001) [0.013; p=<0.001] |
| Mean H = 0 / H = 1 | 0.0049 / 0.1428 | 0.0129 / 0.1861 | 0.0286 / 0.2049 |
| N / N(H = 1) | 659,912 / 3,165 | 189,716 / 955 | 659,912 / 3,165 |
| **Different major occupation (both known)** | | | |
| Husband becomes job loser | 0.024*** (0.001; p=<0.001) [0.002; p=<0.001] | 0.029*** (0.003; p=<0.001) [0.003; p=<0.001] | 0.035*** (0.002; p=<0.001) [0.003; p=<0.001] |
| Mean H = 0 / H = 1 | 0.0056 / 0.0368 | 0.0144 / 0.0518 | 0.0325 / 0.0766 |
| N / N(H = 1) | 2,252,199 / 16,716 | 644,871 / 4,871 | 2,252,199 / 16,716 |
| **Same detailed industry** | | | |
| Husband becomes job loser | 0.211*** (0.009; p=<0.001) [0.013; p=<0.001] | 0.224*** (0.015; p=<0.001) [0.020; p=<0.001] | 0.263*** (0.010; p=<0.001) [0.015; p=<0.001] |
| Mean H = 0 / H = 1 | 0.0041 / 0.2299 | 0.0106 / 0.2619 | 0.0332 / 0.3133 |
| N / N(H = 1) | 515,458 / 2,274 | 147,894 / 670 | 515,458 / 2,274 |
| **Both private wage and salary workers** | | | |
| Husband becomes job loser | 0.041*** (0.002; p=<0.001) [0.005; p=<0.001] | 0.049*** (0.004; p=<0.001) [0.007; p=<0.001] | 0.056*** (0.003; p=<0.001) [0.006; p=<0.001] |
| Mean H = 0 / H = 1 | 0.0059 / 0.0563 | 0.0152 / 0.0782 | 0.0302 / 0.0980 |
| N / N(H = 1) | 1,526,975 / 12,752 | 433,868 / 3,709 | 1,526,975 / 12,752 |
| **NBER recession months** | | | |
| Husband becomes job loser | 0.067*** (0.005; p=<0.001) [0.006; p=<0.001] | 0.079*** (0.010; p=<0.001) [0.011; p=<0.001] | 0.079*** (0.006; p=<0.001) [0.008; p=<0.001] |
| Mean H = 0 / H = 1 | 0.0086 / 0.1063 | 0.0217 / 0.1481 | 0.0361 / 0.1504 |
| N / N(H = 1) | 276,291 / 2,783 | 82,054 / 803 | 276,291 / 2,783 |
| **Expansion months** | | | |
| Husband becomes job loser | 0.036*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.043*** (0.003; p=<0.001) [0.005; p=<0.001] | 0.051*** (0.002; p=<0.001) [0.004; p=<0.001] |
| Mean H = 0 / H = 1 | 0.0051 / 0.0457 | 0.0133 / 0.0621 | 0.0311 / 0.0890 |
| N / N(H = 1) | 2,635,820 / 17,098 | 752,533 / 5,023 | 2,635,820 / 17,098 |
| **Excluding 2020-21** | | | |
| Husband becomes job loser | 0.035*** (0.001; p=<0.001) [0.003; p=<0.001] | 0.043*** (0.003; p=<0.001) [0.005; p=<0.001] | 0.050*** (0.002; p=<0.001) [0.004; p=<0.001] |
| Mean H = 0 / H = 1 | 0.0051 / 0.0448 | 0.0137 / 0.0623 | 0.0313 / 0.0878 |
| N / N(H = 1) | 2,794,827 / 18,779 | 802,461 / 5,549 | 2,794,827 / 18,779 |
| **No own child < 18** | | | |
| Husband becomes job loser | 0.043*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.054*** (0.005; p=<0.001) [0.007; p=<0.001] | 0.056*** (0.003; p=<0.001) [0.004; p=<0.001] |
| Mean H = 0 / H = 1 | 0.0051 / 0.0550 | 0.0133 / 0.0830 | 0.0258 / 0.0913 |
| N / N(H = 1) | 1,249,878 / 8,253 | 354,768 / 2,371 | 1,249,878 / 8,253 |
| **Youngest child 0-5** | | | |
| Husband becomes job loser | 0.037*** (0.003; p=<0.001) [0.005; p=<0.001] | 0.048*** (0.006; p=<0.001) [0.008; p=<0.001] | 0.054*** (0.004; p=<0.001) [0.008; p=<0.001] |
| Mean H = 0 / H = 1 | 0.0056 / 0.0544 | 0.0140 / 0.0785 | 0.0429 / 0.1116 |
| N / N(H = 1) | 661,362 / 4,722 | 189,780 / 1,366 | 661,362 / 4,722 |
| **Youngest child 6-17** | | | |
| Husband becomes job loser | 0.039*** (0.003; p=<0.001) [0.004; p=<0.001] | 0.039*** (0.005; p=<0.001) [0.006; p=<0.001] | 0.054*** (0.003; p=<0.001) [0.004; p=<0.001] |
| Mean H = 0 / H = 1 | 0.0057 / 0.0540 | 0.0150 / 0.0628 | 0.0310 / 0.0963 |
| N / N(H = 1) | 1,000,871 / 6,906 | 290,039 / 2,089 | 1,000,871 / 6,906 |
| **Period 1994-2000** | | | |
| Husband becomes job loser | 0.027*** (0.003; p=<0.001) [0.004; p=<0.001] | 0.032*** (0.006; p=<0.001) [0.008; p=<0.001] | 0.042*** (0.004; p=<0.001) [0.006; p=<0.001] |
| Mean H = 0 / H = 1 | 0.0051 / 0.0345 | 0.0132 / 0.0479 | 0.0332 / 0.0785 |
| N / N(H = 1) | 735,775 / 4,682 | 209,690 / 1,368 | 735,775 / 4,682 |
| **Period 2001-07** | | | |
| Husband becomes job loser | 0.036*** (0.003; p=<0.001) [0.005; p=<0.001] | 0.044*** (0.006; p=<0.001) [0.008; p=<0.001] | 0.049*** (0.004; p=<0.001) [0.006; p=<0.001] |
| Mean H = 0 / H = 1 | 0.0051 / 0.0463 | 0.0131 / 0.0624 | 0.0334 / 0.0875 |
| N / N(H = 1) | 793,750 / 5,265 | 226,596 / 1,509 | 793,750 / 5,265 |
| **Period 2008-13** | | | |
| Husband becomes job loser | 0.036*** (0.003; p=<0.001) [0.004; p=<0.001] | 0.047*** (0.006; p=<0.001) [0.006; p=<0.001] | 0.051*** (0.004; p=<0.001) [0.005; p=<0.001] |
| Mean H = 0 / H = 1 | 0.0063 / 0.0460 | 0.0161 / 0.0685 | 0.0302 / 0.0863 |
| N / N(H = 1) | 604,218 / 5,580 | 180,190 / 1,736 | 604,218 / 5,580 |
| **Period 2014-19** | | | |
| Husband becomes job loser | 0.040*** (0.004; p=<0.001) [0.005; p=<0.001] | 0.044*** (0.008; p=<0.001) [0.007; p=<0.001] | 0.058*** (0.006; p=<0.001) [0.006; p=<0.001] |
| Mean H = 0 / H = 1 | 0.0046 / 0.0459 | 0.0118 / 0.0519 | 0.0292 / 0.0934 |
| N / N(H = 1) | 524,898 / 2,697 | 151,894 / 791 | 524,898 / 2,697 |
| **Period 2020-21** | | | |
| Husband becomes job loser | 0.124*** (0.010; p=<0.001) [0.010; p=<0.001] | 0.141*** (0.022; p=<0.001) [0.024; p=<0.001] | 0.135*** (0.011; p=<0.001) [0.012; p=<0.001] |
| Mean H = 0 / H = 1 | 0.0101 / 0.1650 | 0.0258 / 0.2320 | 0.0351 / 0.2112 |
| N / N(H = 1) | 130,159 / 1,178 | 35,397 / 299 | 130,159 / 1,178 |
| **Period 2022-23** | | | |
| Husband becomes job loser | 0.057*** (0.011; p=<0.001) [0.012; p=<0.001] | 0.078*** (0.025; p=0.002) [0.029; p=0.006] | 0.085*** (0.015; p=<0.001) [0.017; p=<0.001] |
| Mean H = 0 / H = 1 | 0.0036 / 0.0699 | 0.0094 / 0.1126 | 0.0268 / 0.1264 |
| N / N(H = 1) | 123,311 / 479 | 30,820 / 123 | 123,311 / 479 |
| **His job loss: on layoff (PRUNTYPE 1)** | | | |
| Husband becomes job loser | 0.054*** (0.002; p=<0.001) [0.005; p=<0.001] | 0.060*** (0.005; p=<0.001) [0.008; p=<0.001] | 0.065*** (0.003; p=<0.001) [0.006; p=<0.001] |
| Mean H = 0 / H = 1 | 0.0054 / 0.0734 | 0.0140 / 0.0947 | 0.0316 / 0.1137 |
| N / N(H = 1) | 2,901,934 / 9,704 | 831,504 / 2,743 | 2,901,934 / 9,704 |
| **His job loss: other job loser (2)** | | | |
| Husband becomes job loser | 0.026*** (0.002; p=<0.001) [0.002; p=<0.001] | 0.032*** (0.004; p=<0.001) [0.004; p=<0.001] | 0.041*** (0.003; p=<0.001) [0.004; p=<0.001] |
| Mean H = 0 / H = 1 | 0.0054 / 0.0363 | 0.0140 / 0.0525 | 0.0316 / 0.0788 |
| N / N(H = 1) | 2,899,637 / 7,407 | 830,986 / 2,225 | 2,899,637 / 7,407 |
| **His job loss: temporary job ended (3)** | | | |
| Husband becomes job loser | 0.031*** (0.004; p=<0.001) [0.006; p=<0.001] | 0.051*** (0.008; p=<0.001) [0.009; p=<0.001] | 0.059*** (0.006; p=<0.001) [0.005; p=<0.001] |
| Mean H = 0 / H = 1 | 0.0054 / 0.0416 | 0.0140 / 0.0724 | 0.0316 / 0.0984 |
| N / N(H = 1) | 2,895,000 / 2,770 | 829,619 / 858 | 2,895,000 / 2,770 |
| Fixed effects | state x ym | state x ym | state x ym |

**Differences across groups** (pooled LPM, outcome = wife job loser in the same month, state x ym FE; regressors H, group, H x group)

| Interaction | Coefficient on H x group | H (reference group) | N |
|---|---|---|---|
| Black (vs White) | 0.0055 (0.0054; p=0.309) [0.0074; p=0.456] | 0.038*** (0.002; p=<0.001) [0.004; p=<0.001] | 2,729,259 |
| Same major industry | 0.148*** (0.007; p=<0.001) [0.010; p=<0.001] | 0.017*** (0.001; p=<0.001) [0.002; p=<0.001] | 2,912,111 |
| Same major occupation | 0.100*** (0.006; p=<0.001) [0.010; p=<0.001] | 0.024*** (0.001; p=<0.001) [0.002; p=<0.001] | 2,912,111 |
| Same detailed industry | 0.193*** (0.009; p=<0.001) [0.012; p=<0.001] | 0.018*** (0.001; p=<0.001) [0.002; p=<0.001] | 2,912,111 |
| Recession month | 0.031*** (0.005; p=<0.001) [0.006; p=<0.001] | 0.036*** (0.002; p=<0.001) [0.003; p=<0.001] | 2,912,111 |
| Youngest child 0-5 (vs none / older) | -0.0039 (0.0035; p=0.264) [0.0039; p=0.313] | 0.041*** (0.002; p=<0.001) [0.003; p=<0.001] | 2,912,111 |
| 2020-21 | 0.090*** (0.011; p=<0.001) [0.009; p=<0.001] | 0.035*** (0.001; p=<0.001) [0.003; p=<0.001] | 2,912,111 |

**By state** (year-month FE, household clusters; states with >= 30 husband job losers: 51): median coefficient 0.039, interquartile range 0.024 to 0.050; positive in 51 states, p < 0.05 in 46. Precision-weighted mean 0.033; weighted variance of the state estimates minus mean sampling variance: 0.00017 (<= 0: dispersion no larger than sampling noise). State rows in the csv (table 3c_state).

## 4. Timing and placebo: the wife's monthly job-loss hazard around the husband's job-loss month

tau = month in which the husband is observed becoming a job loser (employed at tau-1). Column j: the wife's hazard of becoming a job loser in month tau+j (employed at tau+j-1). Controls: husbands employed at tau-1 and tau and in every other month of the window. Negative j is the placebo: if couples merely share a high job-loss propensity, her hazard is already elevated before his job loss. Each column is a separate sample (the CPS observes at most 4 consecutive months).

| | (1) wife job loser at tau-2 | (2) wife job loser at tau-1 | (3) wife job loser at tau+0 | (4) wife job loser at tau+1 | (5) wife job loser at tau+2 |
|---|---|---|---|---|---|
| **A. state x year-month FE** | | | | | |
| Husband job loser at tau | 0.0055*** (0.0016; p=<0.001) [0.0014; p=<0.001] | 0.0071*** (0.0011; p=<0.001) [0.0013; p=<0.001] | 0.040*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.0084*** (0.0011; p=<0.001) [0.0012; p=<0.001] | 0.0063*** (0.0014; p=<0.001) [0.0017; p=<0.001] |
| N / clusters (households) | 833,349 / 588,152 | 1,798,024 / 681,566 | 2,912,111 / 773,751 | 1,795,387 / 681,211 | 830,606 / 585,869 |
| **B. no fixed effects** | | | | | |
| Husband job loser at tau | 0.0059*** (0.0016; p=<0.001) [0.0014; p=<0.001] | 0.0078*** (0.0011; p=<0.001) [0.0014; p=<0.001] | 0.042*** (0.002; p=<0.001) [0.003; p=<0.001] | 0.0091*** (0.0011; p=<0.001) [0.0013; p=<0.001] | 0.0070*** (0.0014; p=<0.001) [0.0016; p=<0.001] |
| N / clusters (households) | 833,349 / 588,152 | 1,798,024 / 681,566 | 2,912,111 / 773,751 | 1,795,387 / 681,211 | 830,606 / 585,869 |
| Mean H = 0 / H = 1 (weighted) | 0.0054 / 0.0108 | 0.0053 / 0.0144 | 0.0054 / 0.0545 | 0.0053 / 0.0159 | 0.0052 / 0.0129 |
| N husband job losers | 4,406 | 10,326 | 19,881 | 11,850 | 5,715 |

## 5. The wife's response: added-worker transitions of non-employed wives

Wives not employed at t (unemployed or out of the labor force), husbands employed at t. H = 1: husband becomes a job loser at t+1; H = 0: husband employed at t+1 and through t+k. Outcomes at t+k (k = 1, 2, 3 within the rotation; t+12 at the one-year link, husband's later status unrestricted): wife employed; wife unemployed (looking or on layoff, PEMLR 3-4). Each column is a separate regression with state x year-month FE.

| | (1) wife employed at t+1 | (2) wife employed at t+2 | (3) wife employed at t+3 | (4) wife employed at t+12 | (5) wife unemployed at t+1 | (6) wife unemployed at t+2 | (7) wife unemployed at t+3 | (8) wife unemployed at t+12 |
|---|---|---|---|---|---|---|---|---|
| **All** | | | | | | | | |
| Husband becomes job loser (t+1) | 0.022*** (0.003; p=<0.001) [0.003; p=<0.001] | 0.033*** (0.004; p=<0.001) [0.006; p=<0.001] | 0.042*** (0.007; p=<0.001) [0.008; p=<0.001] | 0.040*** (0.008; p=<0.001) [0.008; p=<0.001] | 0.088*** (0.004; p=<0.001) [0.003; p=<0.001] | 0.072*** (0.004; p=<0.001) [0.004; p=<0.001] | 0.064*** (0.006; p=<0.001) [0.006; p=<0.001] | 0.039*** (0.005; p=<0.001) [0.006; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.075 / 0.095 | 0.098 / 0.127 | 0.113 / 0.147 | 0.192 / 0.232 | 0.060 / 0.154 | 0.053 / 0.129 | 0.048 / 0.124 | 0.034 / 0.081 |
| N / N(H = 1) | 1,076,046 / 10,162 | 655,122 / 6,194 | 297,891 / 2,854 | 359,866 / 3,036 | 1,076,046 / 10,162 | 655,122 / 6,194 | 297,891 / 2,854 | 359,866 / 3,036 |
| **Black couples** | | | | | | | | |
| Husband becomes job loser (t+1) | 0.047*** (0.012; p=<0.001) [0.017; p=0.007] | 0.035** (0.017; p=0.035) [0.022; p=0.099] | 0.070*** (0.025; p=0.006) [0.037; p=0.062] | 0.100*** (0.034; p=0.004) [0.053; p=0.059] | 0.103*** (0.015; p=<0.001) [0.016; p=<0.001] | 0.075*** (0.018; p=<0.001) [0.018; p=<0.001] | 0.050* (0.028; p=0.071) [0.045; p=0.261] | 0.067*** (0.023; p=0.003) [0.027; p=0.012] |
| Mean H = 0 / H = 1 (weighted) | 0.094 / 0.129 | 0.124 / 0.149 | 0.144 / 0.151 | 0.244 / 0.355 | 0.109 / 0.223 | 0.096 / 0.186 | 0.092 / 0.187 | 0.062 / 0.122 |
| N / N(H = 1) | 53,424 / 819 | 31,575 / 500 | 13,954 / 226 | 16,353 / 228 | 53,424 / 819 | 31,575 / 500 | 13,954 / 226 | 16,353 / 228 |
| **White couples** | | | | | | | | |
| Husband becomes job loser (t+1) | 0.018*** (0.003; p=<0.001) [0.003; p=<0.001] | 0.033*** (0.005; p=<0.001) [0.006; p=<0.001] | 0.044*** (0.007; p=<0.001) [0.009; p=<0.001] | 0.034*** (0.008; p=<0.001) [0.009; p=<0.001] | 0.083*** (0.004; p=<0.001) [0.004; p=<0.001] | 0.068*** (0.004; p=<0.001) [0.005; p=<0.001] | 0.061*** (0.006; p=<0.001) [0.007; p=<0.001] | 0.033*** (0.005; p=<0.001) [0.006; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.075 / 0.091 | 0.098 / 0.127 | 0.113 / 0.147 | 0.190 / 0.223 | 0.057 / 0.146 | 0.050 / 0.122 | 0.045 / 0.117 | 0.032 / 0.072 |
| N / N(H = 1) | 934,496 / 8,570 | 570,760 / 5,232 | 260,306 / 2,409 | 315,836 / 2,608 | 934,496 / 8,570 | 570,760 / 5,232 | 260,306 / 2,409 | 315,836 / 2,608 |
| **Youngest child 0-5** | | | | | | | | |
| Husband becomes job loser (t+1) | 0.036*** (0.005; p=<0.001) [0.005; p=<0.001] | 0.043*** (0.007; p=<0.001) [0.008; p=<0.001] | 0.061*** (0.011; p=<0.001) [0.014; p=<0.001] | 0.060*** (0.013; p=<0.001) [0.012; p=<0.001] | 0.080*** (0.005; p=<0.001) [0.005; p=<0.001] | 0.069*** (0.006; p=<0.001) [0.006; p=<0.001] | 0.067*** (0.009; p=<0.001) [0.009; p=<0.001] | 0.031*** (0.007; p=<0.001) [0.007; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.064 / 0.092 | 0.085 / 0.121 | 0.098 / 0.143 | 0.187 / 0.245 | 0.042 / 0.128 | 0.038 / 0.106 | 0.036 / 0.111 | 0.027 / 0.070 |
| N / N(H = 1) | 400,256 / 4,035 | 243,560 / 2,430 | 110,610 / 1,115 | 131,345 / 1,138 | 400,256 / 4,035 | 243,560 / 2,430 | 110,610 / 1,115 | 131,345 / 1,138 |
| **Youngest child 6-17** | | | | | | | | |
| Husband becomes job loser (t+1) | 0.022*** (0.006; p=<0.001) [0.006; p=<0.001] | 0.036*** (0.008; p=<0.001) [0.009; p=<0.001] | 0.046*** (0.013; p=<0.001) [0.012; p=<0.001] | 0.027* (0.014; p=0.059) [0.014; p=0.065] | 0.095*** (0.007; p=<0.001) [0.007; p=<0.001] | 0.091*** (0.008; p=<0.001) [0.009; p=<0.001] | 0.082*** (0.012; p=<0.001) [0.013; p=<0.001] | 0.056*** (0.009; p=<0.001) [0.009; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.084 / 0.107 | 0.110 / 0.144 | 0.128 / 0.173 | 0.210 / 0.220 | 0.065 / 0.163 | 0.057 / 0.151 | 0.051 / 0.141 | 0.037 / 0.100 |
| N / N(H = 1) | 322,084 / 2,872 | 197,588 / 1,763 | 90,368 / 815 | 113,967 / 953 | 322,084 / 2,872 | 197,588 / 1,763 | 90,368 / 815 | 113,967 / 953 |
| **No own child < 18** | | | | | | | | |
| Husband becomes job loser (t+1) | 0.0043 (0.0050; p=0.382) [0.0058; p=0.456] | 0.019** (0.007; p=0.011) [0.008; p=0.022] | 0.011 (0.011; p=0.309) [0.014; p=0.416] | 0.028** (0.014; p=0.042) [0.014; p=0.045] | 0.094*** (0.007; p=<0.001) [0.006; p=<0.001] | 0.060*** (0.007; p=<0.001) [0.010; p=<0.001] | 0.049*** (0.010; p=<0.001) [0.012; p=<0.001] | 0.034*** (0.008; p=<0.001) [0.010; p=0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.078 / 0.089 | 0.102 / 0.119 | 0.116 / 0.129 | 0.179 / 0.228 | 0.076 / 0.179 | 0.066 / 0.137 | 0.060 / 0.124 | 0.039 / 0.073 |
| N / N(H = 1) | 353,706 / 3,255 | 213,974 / 2,001 | 96,913 / 924 | 114,554 / 945 | 353,706 / 3,255 | 213,974 / 2,001 | 96,913 / 924 | 114,554 / 945 |
| **Wife out of the labor force at t** | | | | | | | | |
| Husband becomes job loser (t+1) | 0.014*** (0.003; p=<0.001) [0.003; p=<0.001] | 0.025*** (0.004; p=<0.001) [0.005; p=<0.001] | 0.035*** (0.007; p=<0.001) [0.008; p=<0.001] | 0.024*** (0.008; p=0.002) [0.010; p=0.010] | 0.056*** (0.003; p=<0.001) [0.003; p=<0.001] | 0.045*** (0.003; p=<0.001) [0.003; p=<0.001] | 0.044*** (0.005; p=<0.001) [0.006; p=<0.001] | 0.028*** (0.004; p=<0.001) [0.005; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.059 / 0.073 | 0.076 / 0.099 | 0.088 / 0.113 | 0.162 / 0.189 | 0.023 / 0.081 | 0.024 / 0.070 | 0.024 / 0.075 | 0.022 / 0.057 |
| N / N(H = 1) | 987,174 / 8,570 | 600,658 / 5,216 | 272,778 / 2,410 | 329,971 / 2,560 | 987,174 / 8,570 | 600,658 / 5,216 | 272,778 / 2,410 | 329,971 / 2,560 |
| **Wife unemployed at t** | | | | | | | | |
| Husband becomes job loser (t+1) | -0.020* (0.011; p=0.066) [0.011; p=0.077] | -0.025 (0.015; p=0.108) [0.017; p=0.140] | -0.050** (0.024; p=0.036) [0.025; p=0.042] | -0.034 (0.025; p=0.181) [0.027; p=0.207] | 0.053*** (0.013; p=<0.001) [0.014; p=<0.001] | 0.051*** (0.017; p=0.002) [0.017; p=0.003] | 0.028 (0.027; p=0.301) [0.022; p=0.199] | 0.045** (0.021; p=0.034) [0.020; p=0.027] |
| Mean H = 0 / H = 1 (weighted) | 0.255 / 0.214 | 0.341 / 0.279 | 0.396 / 0.331 | 0.527 / 0.466 | 0.487 / 0.546 | 0.380 / 0.449 | 0.314 / 0.388 | 0.166 / 0.205 |
| N / N(H = 1) | 88,872 / 1,592 | 54,464 / 978 | 25,113 / 444 | 29,895 / 476 | 88,872 / 1,592 | 54,464 / 978 | 25,113 / 444 | 29,895 / 476 |
| **Black, youngest child 0-5** | | | | | | | | |
| Husband becomes job loser (t+1) | 0.054*** (0.020; p=0.008) [0.031; p=0.086] | 0.081*** (0.031; p=0.009) [0.040; p=0.045] | 0.025 (0.041; p=0.539) [0.066; p=0.700] | 0.189** (0.087; p=0.030) [0.097; p=0.052] | 0.137*** (0.027; p=<0.001) [0.036; p=<0.001] | 0.110*** (0.035; p=0.002) [0.027; p=<0.001] | 0.156*** (0.059; p=0.008) [0.070; p=0.026] | 0.050 (0.035; p=0.162) [0.047; p=0.288] |
| Mean H = 0 / H = 1 (weighted) | 0.095 / 0.115 | 0.128 / 0.146 | 0.150 / 0.125 | 0.283 / 0.379 | 0.097 / 0.241 | 0.085 / 0.195 | 0.081 / 0.230 | 0.057 / 0.120 |
| N / N(H = 1) | 17,446 / 311 | 10,236 / 184 | 4,516 / 86 | 4,997 / 86 | 17,446 / 311 | 10,236 / 184 | 4,516 / 86 | 4,997 / 86 |
| **White, youngest child 0-5** | | | | | | | | |
| Husband becomes job loser (t+1) | 0.032*** (0.005; p=<0.001) [0.005; p=<0.001] | 0.043*** (0.007; p=<0.001) [0.008; p=<0.001] | 0.063*** (0.012; p=<0.001) [0.013; p=<0.001] | 0.055*** (0.014; p=<0.001) [0.013; p=<0.001] | 0.075*** (0.005; p=<0.001) [0.005; p=<0.001] | 0.063*** (0.006; p=<0.001) [0.006; p=<0.001] | 0.063*** (0.009; p=<0.001) [0.009; p=<0.001] | 0.028*** (0.007; p=<0.001) [0.009; p=0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.064 / 0.089 | 0.084 / 0.120 | 0.097 / 0.147 | 0.183 / 0.240 | 0.039 / 0.118 | 0.035 / 0.098 | 0.033 / 0.102 | 0.025 / 0.062 |
| N / N(H = 1) | 346,716 / 3,393 | 211,686 / 2,053 | 96,422 / 928 | 115,124 / 974 | 346,716 / 3,393 | 211,686 / 2,053 | 96,422 / 928 | 115,124 / 974 |
| **Excluding 2020-21** | | | | | | | | |
| Husband becomes job loser (t+1) | 0.022*** (0.003; p=<0.001) [0.004; p=<0.001] | 0.035*** (0.004; p=<0.001) [0.006; p=<0.001] | 0.043*** (0.007; p=<0.001) [0.008; p=<0.001] | 0.040*** (0.008; p=<0.001) [0.008; p=<0.001] | 0.087*** (0.004; p=<0.001) [0.003; p=<0.001] | 0.073*** (0.004; p=<0.001) [0.004; p=<0.001] | 0.066*** (0.006; p=<0.001) [0.007; p=<0.001] | 0.040*** (0.005; p=<0.001) [0.006; p=<0.001] |
| Mean H = 0 / H = 1 (weighted) | 0.075 / 0.097 | 0.098 / 0.129 | 0.113 / 0.147 | 0.190 / 0.229 | 0.059 / 0.153 | 0.052 / 0.130 | 0.048 / 0.126 | 0.034 / 0.082 |
| N / N(H = 1) | 1,030,866 / 9,586 | 628,324 / 5,866 | 286,050 / 2,723 | 344,136 / 2,848 | 1,030,866 / 9,586 | 628,324 / 5,866 | 286,050 / 2,723 | 344,136 / 2,848 |
| Fixed effects | state x ym | state x ym | state x ym | state x ym | state x ym | state x ym | state x ym | state x ym |

## 6. Comparison with the PSID (EVIDENCE rows 3.8-3.10)

| | PSID (annual reports, 23.CorrelatedShocks.py) | CPS (this script) |
|---|---|---|
| Wife's job loss when the husband loses his vs not | B +0.080*** on base 0.090 (ratio ~1.9); W +0.070*** on 0.058 (~2.2); window ev-1..ev+1 | same month 0.0545 vs 0.0054 (ratio 10.1); within 2 months 0.0746 vs 0.0140 (ratio 5.3); one year 0.0581 vs 0.0105 (ratio 5.5) |
| Black: wife job loser, same month | | 0.0436*** (s.e. 0.0049); means H=0 / H=1 0.0060 / 0.0613 (ratio 10.2) |
| Black: wife job loser within 2 months after | | 0.0630*** (s.e. 0.0110); means H=0 / H=1 0.0157 / 0.0916 (ratio 5.8) |
| White: wife job loser, same month | | 0.0375*** (s.e. 0.0016); means H=0 / H=1 0.0054 / 0.0516 (ratio 9.5) |
| White: wife job loser within 2 months after | | 0.0456*** (s.e. 0.0034); means H=0 / H=1 0.0140 / 0.0723 (ratio 5.1) |
| Same-sector couples, extra | +0.124*** (0.041) | same major industry x H: 0.1484*** (0.0071) |

PSID figures are probabilities over a three-year window around an annual displacement report (closures and layoffs, recalled); CPS figures are monthly transitions into unemployment for job-loss reasons (same month or within two months), so levels differ by construction and only ratios are comparable in spirit.
