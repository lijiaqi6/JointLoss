# Early industry, late payoff: nonlinear industry and occupation x industry cell profiles, and wage persistence after 35

Built by `35.EarlyIndustryLatePayoff.py` (2026-10-17); definitions in its docstring. PSID SRC + SEO sons (32's panel), CPS MORG 1992-2002 men, NLSY79 men. Every coefficient: estimate (s.e.; p), *** p<0.01, ** p<0.05, * p<0.1; s.e. clustered by 1968 family (PSID) / 1979 household (NLSY79); pooled = Black + White weighted, by race unweighted. **Descriptive accounting: sons select into industries, occupations and cells; nothing here is a causal effect of parental income, race, industry or the father's cell.**

## Summary

- **Sample.** PSID: 4,394 sons have an industry at 25-34; of the 3,035 sons observed at 35-55, 2,813 (93%) have one (95% of 35-55 son-years); see Table 0P for their 25-34 characteristics. Son-years in cells with their own MORG profile: current 99%, early 99% (rest: additive occupation + industry fallback).
- **H. Headline, nonlinear profiles (PSID).** 32's sample: pooled rise of the coefficient 0.155*** (0.024; p=<0.001); share carried by the current industry's LINEAR slope B x t 0.084*** (0.014; p=<0.001) vs its NONLINEAR band profile 0.118*** (0.020; p=<0.001) (piecewise 30/35/45: 0.117*** (0.019; p=<0.001)). Change of the Black-White gap -0.170*** (0.038; p=<0.001): linear 0.050*** (0.016; p=0.002), nonlinear 0.074*** (0.023; p=0.001), piecewise 0.072*** (0.023; p=0.002). Common sample (pooled rise 0.146*** (0.024; p=<0.001); B-W change -0.159*** (0.039; p=<0.001)), shares pooled / B-W: industry at 25-34, nonlinear profile 0.132*** (0.024; p=<0.001) / 0.086*** (0.032; p=0.007); occupation x industry CELL profile, current 0.246*** (0.038; p=<0.001) / 0.138*** (0.035; p=<0.001), at 25-34 0.267*** (0.043; p=<0.001) / 0.148*** (0.042; p=<0.001); of which occupation-group profile alone (current) 0.215*** (0.034; p=<0.001) / 0.131*** (0.032; p=<0.001) and what industry adds within the cell (current / at 25-34) 0.031*** (0.010; p=0.003) / 0.007 (0.015; p=0.628) and 0.045*** (0.014; p=0.001) / 0.028 (0.019; p=0.144); current cell level + profile 0.309*** (0.066; p=<0.001) / 0.244*** (0.091; p=0.007).
- **B. What the linear B misses (CPS MORG; s.d. across men of growth 37->52).** Linear 1.5 B 0.055; band growth (35-39)->(50-54) 0.069 (fine industries), 0.067 (cells); correlation with linear growth 0.695, i.e. the linear B misses 52% of the cross-industry variance of growth after 35; cells' later growth correlates 0.456 with their industry's linear growth.
- **D. Data-defined groups (cells ranked by MORG level and band growth after 35; top quartiles of men's employment).** Employment shares: high-paid AND high later growth 0.159, high-paid only 0.121, high later growth only 0.091. The high-paid high-growth set is mostly professional-specialty and managerial occupations in education, public administration, professional services, hospitals and manufacturing; managers in finance, managers in professional services, professionals in legal services and sales in finance / insurance are high-paid but their relative wages FALL after 35 ('high-paid only'). Share of sons in the high-paid high-growth set at 25-34: all 0.119; bottom / top parental-income tercile 0.047 / 0.202; Black 0.057, White 0.161.
- **A. Growth after 35 by the early set (PSID, pooled).** Delta ln wage (40-55)-(25-34) relative to cells in neither set: high-paid high-growth 0.223*** (0.039; p=<0.001), high-paid only 0.203*** (0.043; p=<0.001), high later growth only 0.097*** (0.038; p=0.010). Within person (person + year FE), high-paid high-growth vs neither: slope 25-35 0.329*** (0.044; p=<0.001), slope 35-55 0.059** (0.028; p=0.036) per 10 years; high-paid only: 0.394*** (0.050; p=<0.001) / 0.012 (0.038; p=0.761). Illustrative pre-chosen industries (finance / insurance / legal / professional): Delta 0.229*** (0.059; p=<0.001); slopes 0.333*** (0.060; p=<0.001) / 0.013 (0.057; p=0.818).
- **A. Gelbach, early FE x band (PSID, any profile).** Pooled rise on the early sample 0.132*** (0.023; p=<0.001), B-W change -0.140*** (0.037; p=<0.001). Accounted for by: early data-defined cell set 0.036*** (0.009; p=<0.001) (share 0.271*** (0.067; p=<0.001)) pooled, -0.033*** (0.011; p=0.003) (share 0.237*** (0.087; p=0.006)) of the B-W change; early data-defined industry set 0.005 (0.005; p=0.371) (share 0.034 (0.037; p=0.354)) pooled, -0.001 (0.008; p=0.919) (share 0.006 (0.058; p=0.918)) of the B-W change; early industry group (33) 0.018* (0.010; p=0.076) (share 0.135* (0.072; p=0.061)) pooled, -0.015 (0.016; p=0.332) (share 0.108 (0.105; p=0.304)) of the B-W change; early fine industry 0.036** (0.014; p=0.010) (share 0.276*** (0.098; p=0.005)) pooled, -0.045* (0.025; p=0.069) (share 0.325* (0.167; p=0.052)) of the B-W change; early occupation group (11) 0.051*** (0.010; p=<0.001) (share 0.377*** (0.078; p=<0.001)) pooled, -0.045*** (0.015; p=0.002) (share 0.318*** (0.111; p=0.004)) of the B-W change; occupation group + industry group 0.050*** (0.012; p=<0.001) (share 0.376*** (0.087; p=<0.001)) pooled, -0.050** (0.020; p=0.012) (share 0.352*** (0.129; p=0.006)) of the B-W change; early cell 11 x 33 0.054*** (0.015; p=<0.001) (share 0.405*** (0.099; p=<0.001)) pooled, -0.070*** (0.025; p=0.006) (share 0.493*** (0.171; p=0.004)) of the B-W change; early occupation (occ1990dd) 0.079*** (0.017; p=<0.001) (share 0.591*** (0.120; p=<0.001)) pooled, -0.101*** (0.026; p=<0.001) (share 0.713*** (0.211; p=<0.001)) of the B-W change; illustrative FLP indicator 0.013** (0.005; p=0.011) (share 0.097** (0.039; p=0.013)) pooled, -0.012* (0.006; p=0.050) (share 0.085* (0.046; p=0.066)) of the B-W change. Permuted-cell placebos: mean share og: pooled 0.033, B-W 0.014; occ: pooled 0.028, B-W 0.002.
- **C. Fast track inside the high-paid high-growth cells.** Delta (40-55)-(25-34), pooled: parental-income gradient inside 0.146** (0.059; p=0.013) vs outside 0.043 (0.031; p=0.173) (difference 0.103 (0.065; p=0.113)). Person FE: extra gradient of the slope after 35 inside 0.012 (0.050; p=0.808), of the slope before 35 0.179** (0.085; p=0.035); White 0.018 (0.060; p=0.760) / 0.120 (0.096; p=0.208), Black -0.087 (0.074; p=0.245) / 0.118 (0.092; p=0.199).
- **F. Following the father's cell.** Accounted for in the pooled rise: cell -0.005** (0.002; p=0.030) (share -0.030* (0.016; p=0.053)); in the change of the B-W gap: 0.004 (0.003; p=0.285) of -0.120** (0.051; p=0.019) (share -0.030 (0.032; p=0.349)); industry-group following 0.002 (0.004; p=0.625), occupation-group following -0.003 (0.004; p=0.493). Pay-off of cell following (education and the cell's profile held fixed): ln wage 35-55 -0.031 (0.040; p=0.440); annual growth 35-55 0.001 (0.011; p=0.957); tenure x following -0.040 (0.025; p=0.101). Son in a high-paid high-growth cell when the father was (sons 35-55): pooled 0.090*** (0.028; p=0.001), White 0.094*** (0.027; p=<0.001), Black 0.113 (0.091; p=0.216).
- **E. NLSY79.** Pooled rise (35-55)-(25-34) 0.109*** (0.017; p=<0.001): linear industry slope share 0.097*** (0.017; p=<0.001), nonlinear 0.144*** (0.024; p=<0.001); cell profile at 25-34 0.299*** (0.043; p=<0.001). Gelbach: early cell set 0.040*** (0.006; p=<0.001) (share 0.361*** (0.061; p=<0.001)) pooled, -0.017* (0.010; p=0.085) (share 0.311 (0.194; p=0.109)) of the B-W change; early industry set 0.004 (0.003; p=0.106) (share 0.040 (0.025; p=0.111)) pooled, -0.001 (0.006; p=0.873) (share 0.017 (0.107; p=0.872)) of the B-W change; early occupation group 0.050*** (0.007; p=<0.001) (share 0.454*** (0.070; p=<0.001)) pooled, -0.026** (0.011; p=0.020) (share 0.468* (0.241; p=0.052)) of the B-W change. Delta (40-55)-(25-34), high-paid high-growth vs neither 0.330*** (0.034; p=<0.001).

**Assessment (answer to the PI's question).** Allowing the career payoff to be nonlinear, fixed at 25-34 and specific to occupation x industry cells raises the measured role of early sorting, but what carries the post-35 divergence is the son's early OCCUPATIONAL position (managerial / professional), not his industry and not a late take-off of cells that pay off after 35. (i) Nonlinear industry profiles (headline H): replacing 32's linear B by the industry's full age-band profile raises the share of the pooled post-35 rise of wage persistence carried by the industry's career profile from 0.084*** to 0.118*** (piecewise 30/35/45: 0.117***) and of the change of the Black-White gap from 0.050*** to 0.074***; fixing the industry at 25-34 gives 0.132*** / 0.086***. The linear B misses about half of the cross-industry variance of growth after 35 (correlation 0.70 across men), yet industry remains a second-order channel (about 12-13% of the pooled rise, 7-9% of the Black-White change). (ii) Data-defined groups (Section D): ranking all occupation x industry cells by their MORG level and band growth after 35, the 'high-paid AND high later growth' set (16% of men's employment) is mostly professional-specialty and managerial jobs in education, public administration, professional services, hospitals and manufacturing. The PI's examples mostly fall elsewhere: of men in finance / insurance / legal / professional industries, 56% are in high-paid cells whose wages relative to men of the same age FALL after 35 (managers in finance and in professional services, professionals in legal services, sales in finance / insurance) and 23% in high-paid high-growth cells. (iii) Sons who start in high-paid cells grow faster afterwards (Delta (40-55)-(25-34) 0.223*** for high-paid high-growth, 0.203*** for high-paid only, 0.097*** for high later growth only), but within person the extra growth is concentrated before 35 (slope 25-35 +0.33*** / +0.39*** per 10 years) with at most a small premium after 35 (+0.059** / +0.012). Because the 25-34 band averages over that early climb, growth in the early 30s itself raises the 35-55 vs 25-34 contrast; a payoff that starts only after 35 is not what the data show, in MORG cross-sections or in PSID panels. (iv) Gelbach with early x band fixed effects (any profile, estimated in the PSID): the data-defined early cell set accounts for 0.271*** of the pooled rise and 0.237*** of the change of the Black-White gap; the same ranking applied to industries accounts for 0.034 / 0.006 (not significant); the early occupation group alone 0.377*** / 0.318***, and adding the early industry group changes little (0.376*** / 0.352***); the fine early occupation 0.591*** / 0.713***. Permuted-cell placebos give about 0.03, so these are not over-fitting artefacts, but early-occupation fixed effects also proxy the son's own skills at 25-34: this reads as 'where a son stands at 25-34 predicts how far his wage pulls away later', not as a causal payoff to the occupation. (v) Fast track within the high-paid high-growth cells: the parental-income gradient of growth from 25-34 to 40-55 is 0.146** inside vs 0.043 outside (difference 0.103, p=0.11, imprecise); within person the extra gradient is in the slope before 35 (0.179**) and not after 35 (0.012, p=0.81). (vi) Access: sons of richer and White parents are far more often in high-paid cells at 25-34 (high-paid high-growth: top tercile 0.202 vs bottom 0.047; White 0.161 vs Black 0.057). Following the father's exact cell is about 3-4 times as common as random matching and a father in a high-paid high-growth cell raises the son's chance of being in one (0.090*** at 35-55), but cell following carries no wage-level or growth pay-off once education and the cell's profile are held fixed and accounts for none of the divergence. (vii) NLSY79: the same pattern (early cell set 0.361*** of the pooled rise, industry set 0.040, occupation group 0.454***), with a small and imprecise Black-White divergence. Bottom line for the companion model: early sorting matters, but it is sorting into managerial / professional positions (human capital level at 25-34 and its accumulation in the early 30s), with industry adding little; the illustrative pre-chosen industries (finance / insurance / legal / professional) show the same front-loaded profile (illustrative Gelbach share 0.097** pooled, 0.085* of the gap). Caveats: descriptive accounting; MORG profiles are 1992-2002 cross-sections (synthetic-cohort slopes are noisy and barely correlated with them; PSID within-person group slopes after 35 do not line up with MORG band growth); 'high later growth' is a top-quartile cut of a measure that is near zero for most cells (threshold -0.015); of sons observed at 35-55, 93% have an early industry, while sons never observed after 34 are mostly recent cohorts with slightly lower 25-34 wages (2.45 vs 2.56); codes are bridged across 1970 / 2000 / 2010 classifications.

## 0. Samples

### 0P. Who is kept (PSID)

Fixing the industry at 25-34 requires a son to be observed at 25-34; growth after 35 requires him to be observed again later. This conditioning is necessary for the question, but it is not a balanced panel: every son-year of every son with an early industry is used in the band regressions. Shares and 25-34 characteristics (unweighted means; descriptive):

| Race | sons with a valid wage 25-55 | ... with valid 25-34 son-years | ... with an early industry | ... and observed at 35-55 | ... and observed at 40-55 | share of sons observed at 35-55 who have an early industry | share of son-years 35-55 kept | sons with >= 2 early industry years |
|---|---|---|---|---|---|---|---|---|
| Black + White | 4,647 | 4,447 | 4,394 | 2,813 | 2,048 | 0.927 | 0.949 | 3,938 |
| Black | 1,928 | 1,808 | 1,785 | 1,019 | 688 | 0.888 | 0.923 | 1,528 |
| White | 2,719 | 2,639 | 2,609 | 1,794 | 1,360 | 0.950 | 0.962 | 2,410 |

| Race | sample (sons) | N sons | mean ln wage at 25-34 | ln parental income | years of education | birth year | share early FLP industry (illustrative) | share early high-paid high-growth cell |
|---|---|---|---|---|---|---|---|---|
| Black + White | all sons with valid 25-34 son-years | 4,447 | 2.524 | 10.758 | 13.70 | 1971.6 | 0.056 | 0.119 |
| Black + White | with an early industry | 4,394 | 2.523 | 10.756 | 13.70 | 1971.6 | 0.056 | 0.119 |
| Black + White | with an early industry, observed at 35-55 | 2,813 | 2.563 | 10.802 | 13.90 | 1968.1 | 0.060 | 0.134 |
| Black + White | with an early industry, observed at 40-55 | 2,048 | 2.585 | 10.809 | 13.99 | 1965.9 | 0.058 | 0.142 |
| Black + White | with an early industry, NOT observed after 34 | 1,581 | 2.451 | 10.673 | 13.34 | 1977.8 | 0.048 | 0.093 |
| Black | all sons with valid 25-34 son-years | 1,808 | 2.329 | 10.338 | 13.10 | 1971.5 | 0.032 | 0.057 |
| Black | with an early industry | 1,785 | 2.327 | 10.335 | 13.10 | 1971.5 | 0.032 | 0.057 |
| Black | with an early industry, observed at 35-55 | 1,019 | 2.354 | 10.340 | 13.30 | 1968.2 | 0.032 | 0.066 |
| Black | with an early industry, observed at 40-55 | 688 | 2.368 | 10.313 | 13.33 | 1965.7 | 0.032 | 0.069 |
| Black | with an early industry, NOT observed after 34 | 766 | 2.291 | 10.329 | 12.84 | 1975.9 | 0.033 | 0.044 |
| White | all sons with valid 25-34 son-years | 2,639 | 2.658 | 11.046 | 14.11 | 1971.8 | 0.072 | 0.161 |
| White | with an early industry | 2,609 | 2.657 | 11.043 | 14.11 | 1971.6 | 0.072 | 0.161 |
| White | with an early industry, observed at 35-55 | 1,794 | 2.682 | 11.065 | 14.24 | 1968.0 | 0.076 | 0.172 |
| White | with an early industry, observed at 40-55 | 1,360 | 2.695 | 11.059 | 14.32 | 1966.0 | 0.071 | 0.178 |
| White | with an early industry, NOT observed after 34 | 815 | 2.602 | 10.995 | 13.80 | 1979.6 | 0.063 | 0.137 |

## HP. Headline: nonlinear industry and occupation x industry cell profiles (PSID)

Each row is a piece of the son's ln wage regressed on ln parental income by age band (stacked; controls as in the band regressions); the columns are the change of that coefficient across age bands and its share of the change for ln wage, pooled and for the Black-White gap. 'Linear' = 32's P_j + B_j t; 'nonlinear band profile' = the son's industry's (cell's) relative wage in his five-year age band (CPS MORG), split into its age-weighted level and the age profile around it; 'piecewise' = the knots-30/35/45 profile. The profile rows are the like-for-like comparison with the linear slope (all are the career-growth component of the industry / cell). 'At 25-34' = the industry or cell fixed at the son's modal code at 25-34, evaluated at his current age (payoff of where he started, wherever he works later). Shares blank when the denominator is not different from zero.

| | (1) pooled change (35-55)-(25-34) | (2) share of the ln wage change | (3) change of the B-W gap (35-55)-(25-34) | (4) share | (5) pooled change (45-55)-(25-34) | (6) share | (7) B-W change (45-55)-(25-34) | (8) share |
|---|---|---|---|---|---|---|---|---|
| **A. 32's decomposition sample (current industry and occupation mapped): replication of the linear B and the nonlinear profile** | | | | | | | | |
| ln wage (total) | 0.155*** (0.024; p=<0.001) |  | -0.170*** (0.038; p=<0.001) |  | 0.177*** (0.036; p=<0.001) |  | -0.209*** (0.061; p=<0.001) |  |
| current industry, LINEAR (32): level P | -0.003 (0.007; p=0.690) | -0.019 (0.048; p=0.697) | -0.005 (0.012; p=0.717) | 0.026 (0.071; p=0.710) | 0.001 (0.010; p=0.942) | 0.004 (0.058; p=0.941) | -0.020 (0.020; p=0.327) | 0.094 (0.090; p=0.296) |
| current industry, LINEAR (32): slope B x t | 0.013*** (0.002; p=<0.001) | 0.084*** (0.014; p=<0.001) | -0.009*** (0.002; p=<0.001) | 0.050*** (0.016; p=0.002) | 0.020*** (0.003; p=<0.001) | 0.112*** (0.023; p=<0.001) | -0.016*** (0.005; p=<0.001) | 0.079*** (0.028; p=0.004) |
| current industry, NONLINEAR band profile: level | -0.003 (0.007; p=0.719) | -0.017 (0.048; p=0.724) | -0.006 (0.012; p=0.632) | 0.035 (0.071; p=0.621) | 0.001 (0.010; p=0.950) | 0.004 (0.058; p=0.950) | -0.022 (0.020; p=0.273) | 0.105 (0.090; p=0.243) |
| current industry, NONLINEAR band profile: age profile Q(band) - level | 0.018*** (0.002; p=<0.001) | 0.118*** (0.020; p=<0.001) | -0.013*** (0.003; p=<0.001) | 0.074*** (0.023; p=0.001) | 0.020*** (0.003; p=<0.001) | 0.113*** (0.027; p=<0.001) | -0.015** (0.006; p=0.010) | 0.071** (0.030; p=0.019) |
| current industry, NONLINEAR band profile: total | 0.016** (0.008; p=0.042) | 0.101** (0.045; p=0.026) | -0.019 (0.013; p=0.155) | 0.109 (0.071; p=0.124) | 0.021* (0.011; p=0.071) | 0.117* (0.061; p=0.057) | -0.037 (0.022; p=0.101) | 0.176* (0.100; p=0.079) |
| current industry, piecewise (knots 30/35/45): age profile | 0.018*** (0.002; p=<0.001) | 0.117*** (0.019; p=<0.001) | -0.012*** (0.003; p=<0.001) | 0.072*** (0.023; p=0.002) | 0.021*** (0.003; p=<0.001) | 0.118*** (0.026; p=<0.001) | -0.014*** (0.005; p=0.009) | 0.069** (0.028; p=0.016) |
| N son-years / sons (pooled) | 25-34: 20,276 / 4,212 ; 35-44: 12,074 / 2,838 ; 45-55: 5,396 / 1,472 |  |  |  |  |  |  |  |
| **B. Common sample (also early industry and early cell): current vs early, industry vs cell, linear vs nonlinear** | | | | | | | | |
| ln wage (total) | 0.146*** (0.024; p=<0.001) |  | -0.159*** (0.039; p=<0.001) |  | 0.162*** (0.037; p=<0.001) |  | -0.208*** (0.065; p=0.001) |  |
| current industry, LINEAR slope B x t (32) | 0.013*** (0.002; p=<0.001) | 0.089*** (0.015; p=<0.001) | -0.009*** (0.002; p=<0.001) | 0.055*** (0.018; p=0.002) | 0.020*** (0.003; p=<0.001) | 0.122*** (0.028; p=<0.001) | -0.018*** (0.005; p=<0.001) | 0.085*** (0.031; p=0.005) |
| current industry, NONLINEAR band profile | 0.018*** (0.002; p=<0.001) | 0.124*** (0.022; p=<0.001) | -0.013*** (0.004; p=<0.001) | 0.083*** (0.026; p=0.002) | 0.020*** (0.003; p=<0.001) | 0.123*** (0.032; p=<0.001) | -0.016*** (0.006; p=0.007) | 0.079** (0.034; p=0.019) |
| current industry, piecewise (30/35/45) profile | 0.018*** (0.002; p=<0.001) | 0.124*** (0.021; p=<0.001) | -0.013*** (0.004; p=<0.001) | 0.080*** (0.026; p=0.002) | 0.021*** (0.003; p=<0.001) | 0.129*** (0.031; p=<0.001) | -0.016*** (0.006; p=0.006) | 0.075** (0.031; p=0.016) |
| current industry, band level + profile | 0.013 (0.008; p=0.104) | 0.087* (0.049; p=0.077) | -0.019 (0.013; p=0.163) | 0.117 (0.077; p=0.129) | 0.015 (0.012; p=0.208) | 0.094 (0.071; p=0.185) | -0.039* (0.024; p=0.099) | 0.188* (0.107; p=0.079) |
| industry at 25-34, LINEAR slope B x t | 0.014*** (0.002; p=<0.001) | 0.093*** (0.017; p=<0.001) | -0.009*** (0.003; p=0.003) | 0.058*** (0.022; p=0.009) | 0.020*** (0.003; p=<0.001) | 0.126*** (0.030; p=<0.001) | -0.017*** (0.006; p=0.004) | 0.082** (0.035; p=0.017) |
| industry at 25-34, band level | 0.002 (0.008; p=0.773) | 0.016 (0.053; p=0.769) | -0.015 (0.013; p=0.244) | 0.097 (0.078; p=0.218) | 0.005 (0.013; p=0.708) | 0.030 (0.077; p=0.701) | -0.034 (0.022; p=0.125) | 0.165 (0.102; p=0.105) |
| industry at 25-34, NONLINEAR band profile | 0.019*** (0.003; p=<0.001) | 0.132*** (0.024; p=<0.001) | -0.014*** (0.004; p=0.002) | 0.086*** (0.032; p=0.007) | 0.023*** (0.004; p=<0.001) | 0.140*** (0.033; p=<0.001) | -0.017** (0.007; p=0.022) | 0.080** (0.038; p=0.037) |
| industry at 25-34, piecewise (30/35/45) profile | 0.019*** (0.003; p=<0.001) | 0.133*** (0.024; p=<0.001) | -0.013*** (0.004; p=0.004) | 0.081*** (0.032; p=0.010) | 0.022*** (0.004; p=<0.001) | 0.136*** (0.032; p=<0.001) | -0.014** (0.007; p=0.035) | 0.069* (0.036; p=0.052) |
| industry at 25-34, synthetic-cohort slope after 35 x s2 | -0.003 (0.002; p=0.245) | -0.019 (0.016; p=0.248) | 0.009** (0.004; p=0.033) | -0.057** (0.029; p=0.049) | -0.006 (0.005; p=0.278) | -0.035 (0.033; p=0.286) | 0.019* (0.011; p=0.079) | -0.092 (0.057; p=0.108) |
| industry at 25-34, band level + profile | 0.022** (0.009; p=0.018) | 0.148** (0.058; p=0.011) | -0.029* (0.015; p=0.051) | 0.182** (0.088; p=0.039) | 0.028* (0.015; p=0.064) | 0.170** (0.084; p=0.044) | -0.051* (0.026; p=0.052) | 0.245** (0.122; p=0.045) |
| current CELL (occupation group x industry group), band level | 0.009 (0.010; p=0.341) | 0.063 (0.063; p=0.314) | -0.017 (0.016; p=0.290) | 0.106 (0.091; p=0.242) | 0.019 (0.015; p=0.208) | 0.116 (0.086; p=0.178) | -0.022 (0.027; p=0.420) | 0.106 (0.118; p=0.370) |
| current CELL, NONLINEAR band profile | 0.036*** (0.003; p=<0.001) | 0.246*** (0.038; p=<0.001) | -0.022*** (0.004; p=<0.001) | 0.138*** (0.035; p=<0.001) | 0.042*** (0.004; p=<0.001) | 0.261*** (0.059; p=<0.001) | -0.025*** (0.007; p=<0.001) | 0.120*** (0.040; p=0.002) |
| current occupation group (11), NONLINEAR band profile (occupation only) | 0.031*** (0.002; p=<0.001) | 0.215*** (0.034; p=<0.001) | -0.021*** (0.003; p=<0.001) | 0.131*** (0.032; p=<0.001) | 0.036*** (0.003; p=<0.001) | 0.224*** (0.049; p=<0.001) | -0.025*** (0.005; p=<0.001) | 0.119*** (0.035; p=<0.001) |
| current cell profile minus occupation-group profile (what industry adds within the cell) | 0.005*** (0.001; p=0.002) | 0.031*** (0.010; p=0.003) | -0.001 (0.002; p=0.631) | 0.007 (0.015; p=0.628) | 0.006** (0.003; p=0.018) | 0.038** (0.018; p=0.032) | -0.000 (0.004; p=0.961) | 0.001 (0.022; p=0.961) |
| current CELL, level + profile | 0.045*** (0.010; p=<0.001) | 0.309*** (0.066; p=<0.001) | -0.039** (0.017; p=0.023) | 0.244*** (0.091; p=0.007) | 0.061*** (0.017; p=<0.001) | 0.378*** (0.108; p=<0.001) | -0.047 (0.031; p=0.129) | 0.226* (0.126; p=0.074) |
| within current cell (ln wage - cell level - cell profile) | 0.101*** (0.021; p=<0.001) | 0.691*** (0.066; p=<0.001) | -0.120*** (0.033; p=<0.001) | 0.756*** (0.091; p=<0.001) | 0.101*** (0.035; p=0.004) | 0.622*** (0.108; p=<0.001) | -0.161*** (0.055; p=0.003) | 0.774*** (0.126; p=<0.001) |
| cell at 25-34, band level | 0.010 (0.010; p=0.279) | 0.071 (0.061; p=0.250) | -0.023 (0.015; p=0.134) | 0.145* (0.087; p=0.095) | 0.018 (0.016; p=0.244) | 0.113 (0.090; p=0.207) | -0.046* (0.027; p=0.087) | 0.219* (0.116; p=0.059) |
| cell at 25-34, NONLINEAR band profile | 0.039*** (0.003; p=<0.001) | 0.267*** (0.043; p=<0.001) | -0.024*** (0.005; p=<0.001) | 0.148*** (0.042; p=<0.001) | 0.046*** (0.005; p=<0.001) | 0.286*** (0.064; p=<0.001) | -0.026*** (0.008; p=<0.001) | 0.125*** (0.048; p=0.008) |
| occupation group at 25-34, NONLINEAR band profile (occupation only) | 0.033*** (0.003; p=<0.001) | 0.222*** (0.036; p=<0.001) | -0.019*** (0.004; p=<0.001) | 0.120*** (0.033; p=<0.001) | 0.037*** (0.003; p=<0.001) | 0.229*** (0.051; p=<0.001) | -0.021*** (0.006; p=<0.001) | 0.100*** (0.035; p=0.004) |
| cell at 25-34 profile minus occupation-group profile (what industry adds) | 0.007*** (0.002; p=<0.001) | 0.045*** (0.014; p=0.001) | -0.004 (0.003; p=0.122) | 0.028 (0.019; p=0.144) | 0.009*** (0.003; p=0.002) | 0.058*** (0.022; p=0.009) | -0.005 (0.005; p=0.308) | 0.025 (0.026; p=0.329) |
| cell at 25-34, level + profile | 0.049*** (0.011; p=<0.001) | 0.337*** (0.071; p=<0.001) | -0.047*** (0.018; p=0.008) | 0.294*** (0.100; p=0.003) | 0.065*** (0.018; p=<0.001) | 0.399*** (0.111; p=<0.001) | -0.072** (0.031; p=0.020) | 0.344** (0.140; p=0.014) |
| N son-years / sons (pooled) | 25-34: 20,276 / 4,212 ; 35-44: 11,520 / 2,641 ; 45-55: 4,963 / 1,343 |  |  |  |  |  |  |  |

## B. Nonlinear industry profiles and what the linear slope misses

CPS MORG men 25-64, 1992-2002 (743,983). Q = industry x five-year age-band effect (wage relative to men of the same single year of age); piecewise slopes per 10 years with knots at 30, 35, 45 relative to the average industry; synthetic cohort = slopes within industry net of 5-year birth-cohort FE (identified from the aging of cohorts across 1992-2002; industry-specific period trends not separated). 'Post-35 steep' = top quartile of men's employment by band growth (35-39)->(50-54): Mfg: textiles, apparel, leather, Mfg: chemicals, petroleum, rubber, plastics, Mfg: wood, furniture, stone, glass, Utilities and sanitary services, Education, Social services, religious, membership, Professional services (engineering, accounting, research, consulting), Public administration (incl. postal). Cells: 267 of the 11 x 33 occupation x industry cells have >= 200 men (own profile), covering 99.1% of men's employment; the rest use the additive occupation(band) + industry(band) fallback.

### B0. Industry groups sorted by band growth after 35 (descriptive industry averages; worker composition not held fixed)

| Industry group | linear B (32) | linear growth 37->52 (1.5 B) | piecewise slope 25-30 | 30-35 | 35-45 | 45-64 | Q 25-29 | Q 30-34 | Q 35-39 | Q 40-44 | Q 45-49 | Q 50-54 | Q 55-59 | Q 60-64 | band growth (35-39)->(50-54) | band growth (25-29)->(35-39) | piecewise growth 37->52 | synthetic-cohort growth 37->52 | PSID sons (early) | employment share | N men |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Education (high later growth) | 0.077 | 0.115 | 0.078 | 0.020 | 0.133 | 0.043 | 0.009 | 0.023 | 0.044 | 0.078 | 0.134 | 0.179 | 0.189 | 0.198 | 0.135 | 0.035 | 0.136 | 0.089 | 200 | 0.055 | 43,848 |
| Mfg: chemicals, petroleum, rubber, plastics (high later growth) | 0.038 | 0.057 | -0.010 | 0.062 | 0.028 | 0.045 | 0.094 | 0.092 | 0.106 | 0.106 | 0.117 | 0.142 | 0.154 | 0.221 | 0.036 | 0.012 | 0.054 | -0.008 | 103 | 0.029 | 20,995 |
| Mfg: textiles, apparel, leather (high later growth) | 0.015 | 0.023 | -0.176 | 0.016 | 0.035 | 0.025 | -0.197 | -0.252 | -0.269 | -0.232 | -0.256 | -0.240 | -0.208 | -0.193 | 0.029 | -0.073 | 0.046 | 0.055 | 43 | 0.011 | 7,628 |
| Public administration (incl. postal) (high-paid, high later growth) | 0.009 | 0.014 | -0.037 | -0.018 | 0.016 | 0.016 | 0.170 | 0.143 | 0.126 | 0.129 | 0.125 | 0.135 | 0.144 | 0.173 | 0.009 | -0.044 | 0.024 | -0.031 | 297 | 0.075 | 57,491 |
| Social services, religious, membership (high later growth) | -0.006 | -0.008 | -0.008 | -0.023 | 0.026 | -0.027 | -0.109 | -0.112 | -0.132 | -0.141 | -0.139 | -0.127 | -0.166 | -0.169 | 0.006 | -0.024 | 0.002 | 0.100 | 60 | 0.019 | 14,930 |
| Professional services (engineering, accounting, research, consulting) (FLP) (high-paid, high later growth) | 0.039 | 0.059 | 0.095 | 0.086 | 0.016 | 0.034 | 0.349 | 0.371 | 0.404 | 0.415 | 0.372 | 0.404 | 0.449 | 0.481 | -0.000 | 0.055 | 0.037 | 0.025 | 89 | 0.024 | 18,377 |
| Mfg: wood, furniture, stone, glass (high later growth) | 0.000 | 0.000 | -0.098 | -0.034 | -0.023 | 0.058 | -0.125 | -0.174 | -0.204 | -0.223 | -0.216 | -0.214 | -0.184 | -0.085 | -0.009 | -0.080 | 0.023 | 0.045 | 114 | 0.025 | 18,467 |
| Utilities and sanitary services (high-paid, high later growth) | 0.011 | 0.017 | -0.001 | -0.022 | 0.063 | -0.033 | 0.152 | 0.141 | 0.137 | 0.166 | 0.163 | 0.126 | 0.130 | 0.174 | -0.011 | -0.015 | 0.027 | -0.043 | 63 | 0.023 | 17,921 |
| Wholesale trade | -0.008 | -0.012 | -0.000 | -0.046 | 0.023 | -0.028 | 0.030 | 0.006 | -0.020 | -0.005 | -0.028 | -0.032 | -0.052 | -0.034 | -0.012 | -0.050 | -0.002 | 0.028 | 176 | 0.053 | 39,673 |
| Hospitals | 0.029 | 0.044 | 0.039 | 0.121 | 0.033 | -0.015 | 0.023 | 0.055 | 0.079 | 0.092 | 0.095 | 0.064 | 0.029 | 0.150 | -0.015 | 0.056 | 0.016 | 0.006 | 117 | 0.022 | 16,759 |
| Mfg: primary and fabricated metals | 0.001 | 0.001 | -0.111 | -0.035 | -0.004 | 0.034 | -0.002 | -0.055 | -0.081 | -0.086 | -0.090 | -0.097 | -0.069 | 0.019 | -0.016 | -0.079 | 0.020 | -0.054 | 105 | 0.029 | 20,827 |
| Mfg: paper, printing, publishing | 0.002 | 0.003 | 0.088 | 0.000 | -0.032 | 0.025 | 0.043 | 0.060 | 0.037 | 0.021 | -0.009 | 0.017 | 0.041 | 0.033 | -0.020 | -0.006 | -0.008 | -0.051 | 82 | 0.026 | 18,926 |
| Mfg: motor vehicles, aircraft, other transport eq. (high-paid) | 0.022 | 0.033 | 0.046 | 0.098 | -0.034 | 0.051 | 0.132 | 0.159 | 0.173 | 0.131 | 0.148 | 0.149 | 0.167 | 0.262 | -0.023 | 0.040 | 0.009 | -0.071 | 152 | 0.033 | 23,644 |
| Communications (high-paid) | 0.022 | 0.033 | 0.071 | 0.069 | 0.021 | -0.012 | 0.234 | 0.235 | 0.263 | 0.269 | 0.252 | 0.238 | 0.254 | 0.279 | -0.025 | 0.029 | 0.009 | 0.039 | 73 | 0.018 | 13,340 |
| Mining | 0.011 | 0.016 | -0.131 | 0.141 | 0.003 | -0.008 | 0.081 | 0.033 | 0.079 | 0.075 | 0.054 | 0.053 | 0.042 | 0.095 | -0.026 | -0.002 | -0.003 | -0.104 | 35 | 0.009 | 9,129 |
| Finance: banking, credit, securities (FLP) (high-paid) | 0.021 | 0.031 | 0.248 | 0.100 | -0.018 | -0.021 | 0.340 | 0.405 | 0.440 | 0.391 | 0.401 | 0.407 | 0.356 | 0.381 | -0.033 | 0.100 | -0.029 | -0.089 | 92 | 0.022 | 16,902 |
| Legal services (FLP) (high-paid) | 0.069 | 0.103 | 0.327 | 0.111 | 0.012 | 0.065 | 0.434 | 0.513 | 0.547 | 0.586 | 0.535 | 0.513 | 0.657 | 0.696 | -0.034 | 0.112 | 0.055 | -0.125 | 21 | 0.006 | 4,145 |
| Mfg: food, tobacco | 0.007 | 0.010 | -0.056 | 0.005 | 0.030 | -0.007 | -0.122 | -0.144 | -0.149 | -0.153 | -0.125 | -0.186 | -0.139 | -0.121 | -0.037 | -0.027 | 0.019 | -0.029 | 78 | 0.021 | 15,304 |
| Mfg: instruments, misc. manufacturing | 0.020 | 0.030 | 0.106 | 0.074 | 0.015 | -0.010 | 0.059 | 0.096 | 0.107 | 0.103 | 0.120 | 0.066 | 0.105 | 0.102 | -0.041 | 0.047 | 0.005 | -0.006 | 35 | 0.014 | 10,200 |
| Transportation (excl. postal) | -0.019 | -0.029 | -0.010 | -0.066 | -0.017 | -0.005 | 0.009 | -0.022 | -0.062 | -0.070 | -0.092 | -0.105 | -0.077 | -0.076 | -0.043 | -0.071 | -0.018 | -0.071 | 243 | 0.058 | 43,094 |
| Mfg: electrical equipment (high-paid) | 0.003 | 0.005 | 0.206 | -0.003 | -0.037 | 0.019 | 0.173 | 0.223 | 0.187 | 0.181 | 0.157 | 0.143 | 0.169 | 0.235 | -0.045 | 0.014 | -0.016 | 0.036 | 59 | 0.021 | 14,863 |
| Construction | -0.010 | -0.015 | -0.082 | -0.047 | -0.018 | 0.033 | 0.031 | -0.020 | -0.042 | -0.054 | -0.076 | -0.087 | -0.016 | 0.009 | -0.045 | -0.073 | 0.008 | -0.035 | 543 | 0.096 | 71,466 |
| Mfg: machinery and computers | -0.002 | -0.004 | 0.025 | -0.019 | -0.000 | -0.003 | 0.126 | 0.120 | 0.107 | 0.091 | 0.090 | 0.055 | 0.115 | 0.086 | -0.052 | -0.020 | -0.002 | -0.024 | 86 | 0.033 | 23,737 |
| Other health services | 0.031 | 0.047 | 0.083 | 0.201 | 0.001 | -0.014 | 0.021 | 0.077 | 0.117 | 0.145 | 0.092 | 0.065 | 0.106 | 0.135 | -0.052 | 0.097 | -0.009 | 0.007 | 68 | 0.015 | 11,094 |
| Insurance (FLP) (high-paid) | 0.020 | 0.031 | 0.103 | 0.178 | -0.023 | -0.010 | 0.263 | 0.313 | 0.367 | 0.321 | 0.333 | 0.308 | 0.293 | 0.350 | -0.059 | 0.103 | -0.025 | 0.008 | 44 | 0.014 | 10,241 |
| Retail trade (excl. eating, drinking) | -0.035 | -0.052 | 0.029 | -0.037 | -0.026 | -0.058 | -0.119 | -0.137 | -0.160 | -0.182 | -0.224 | -0.222 | -0.277 | -0.271 | -0.062 | -0.042 | -0.062 | 0.010 | 435 | 0.090 | 67,431 |
| Automotive and repair services | -0.043 | -0.065 | -0.126 | -0.073 | -0.026 | -0.029 | -0.101 | -0.173 | -0.202 | -0.251 | -0.238 | -0.273 | -0.258 | -0.293 | -0.072 | -0.100 | -0.041 | 0.007 | 122 | 0.021 | 15,136 |
| Other business services | -0.043 | -0.065 | -0.076 | 0.036 | -0.062 | -0.052 | -0.098 | -0.140 | -0.132 | -0.192 | -0.245 | -0.207 | -0.265 | -0.307 | -0.075 | -0.033 | -0.086 | 0.125 | 150 | 0.029 | 20,193 |
| Eating, drinking, hotels | -0.023 | -0.034 | -0.023 | -0.074 | -0.004 | -0.014 | -0.404 | -0.443 | -0.472 | -0.489 | -0.491 | -0.550 | -0.501 | -0.461 | -0.078 | -0.068 | -0.013 | 0.061 | 292 | 0.039 | 28,687 |
| Computer and data processing services (high-paid) | 0.001 | 0.002 | 0.192 | 0.011 | -0.032 | -0.010 | 0.459 | 0.485 | 0.474 | 0.462 | 0.436 | 0.393 | 0.461 | 0.430 | -0.081 | 0.016 | -0.032 | 0.012 | 66 | 0.017 | 11,492 |
| Personal services, entertainment | -0.046 | -0.068 | -0.108 | 0.005 | -0.042 | -0.059 | -0.115 | -0.146 | -0.179 | -0.221 | -0.235 | -0.260 | -0.295 | -0.307 | -0.082 | -0.064 | -0.074 | 0.030 | 136 | 0.020 | 14,875 |
| Agriculture, forestry, fishing | -0.064 | -0.095 | -0.291 | -0.069 | -0.071 | -0.001 | -0.368 | -0.504 | -0.535 | -0.573 | -0.616 | -0.641 | -0.641 | -0.536 | -0.106 | -0.167 | -0.058 | 0.054 | 168 | 0.019 | 13,452 |
| Real estate | -0.036 | -0.053 | -0.013 | 0.021 | -0.062 | -0.032 | -0.020 | -0.025 | -0.050 | -0.092 | -0.100 | -0.162 | -0.173 | -0.120 | -0.112 | -0.031 | -0.072 | 0.010 | 47 | 0.014 | 9,716 |

Employment-weighted means by early-industry set:

| Data-defined industry set | linear growth 37->52 (1.5 B) | band growth (25-29)->(35-39) | band growth (35-39)->(50-54) | piecewise growth 37->52 | employment share |
|---|---|---|---|---|---|
| high-paid AND high later growth | 0.024 | -0.019 | 0.003 | 0.027 | 0.122 |
| high-paid only | 0.027 | 0.051 | -0.040 | -0.009 | 0.131 |
| high later growth only | 0.058 | -0.007 | 0.062 | 0.073 | 0.138 |
| neither | -0.024 | -0.047 | -0.050 | -0.020 | 0.608 |

### B1. How much of the cross-industry variance in growth after 35 does the linear B miss?

Each man in CPS MORG is assigned his industry's (group's, cell's) growth measure; s.d. across men (earnings weights). R2 = squared correlation with the linear-B-implied growth across men (fine industries); 1 - R2 = share of the cross-industry variance of that growth measure that the linear B does not capture (includes sampling noise of the fine band cells). PSID column: s.d. across sons of the measure of their industry at 25-34. For cells, the band growth after 35 correlates 0.456 with the industry's linear growth (R2 0.207); s.d. across PSID sons of their early cell's band growth after 35 0.067.

| Growth measure (log points) | s.d. across CPS men: fine industries | 33 industry groups | 11 x 33 cells | s.d. across PSID sons (industry at 25-34) | corr. with linear growth 1.5 B (men, fine) | R2 on linear growth | share of variance NOT captured by linear B |
|---|---|---|---|---|---|---|---|
| linear B-implied growth 37->52 (1.5 B, 32) | 0.055 | 0.045 |  | 0.054 | 1.000 | 1.000 | 0.000 |
| band growth (35-39)->(50-54) | 0.069 | 0.050 | 0.067 | 0.069 | 0.695 | 0.483 | 0.517 |
| piecewise (30/35/45) growth 37->52 | 0.056 | 0.047 |  |  | 0.796 | 0.634 | 0.366 |
| synthetic-cohort growth 37->52 | 0.093 | 0.052 |  |  | 0.154 | 0.024 | 0.976 |
| band growth (25-29)->(35-39) (before 35) | 0.082 | 0.055 | 0.098 |  | 0.703 | 0.494 | 0.506 |

### B2. Within-person slopes by early industry group (PSID, pooled weighted)

One son-year regression: ln wage on person FE, year FE, a common kink at 35 and early-group x s1 / s2 (slopes per 10 years); each group's slope relative to the son-weighted average group. Groups with >= 30 sons. Within-person growth of sons who STARTED in the group (wherever they work later), net of cohort differences.

| Early industry group | PSID sons | PSID slope 25-35 | PSID slope 35-55 | PSID acceleration | MORG band growth (25-29)->(35-39) | MORG band growth (35-39)->(50-54) | MORG linear growth 1.5 B |
|---|---|---|---|---|---|---|---|
| Education | 200 | 0.178*** (0.062; p=0.004) | 0.028 (0.040; p=0.477) | -0.150* (0.077; p=0.053) | 0.035 | 0.135 | 0.115 |
| Mfg: chemicals, petroleum, rubber, plastics | 103 | 0.065 (0.091; p=0.475) | -0.065 (0.052; p=0.213) | -0.130 (0.099; p=0.190) | 0.012 | 0.036 | 0.057 |
| Mfg: textiles, apparel, leather | 43 | 0.031 (0.101; p=0.759) | -0.198* (0.103; p=0.054) | -0.229 (0.163; p=0.161) | -0.073 | 0.029 | 0.023 |
| Public administration (incl. postal) | 297 | 0.095* (0.049; p=0.053) | 0.034 (0.030; p=0.253) | -0.061 (0.056; p=0.274) | -0.044 | 0.009 | 0.014 |
| Social services, religious, membership | 60 | 0.213** (0.084; p=0.011) | 0.047 (0.084; p=0.575) | -0.166 (0.117; p=0.156) | -0.024 | 0.006 | -0.008 |
| Professional services (engineering, accounting, research, consulting) | 89 | 0.136 (0.092; p=0.137) | -0.007 (0.094; p=0.940) | -0.143 (0.140; p=0.305) | 0.055 | -0.000 | 0.059 |
| Mfg: wood, furniture, stone, glass | 114 | -0.202*** (0.058; p=<0.001) | -0.004 (0.040; p=0.912) | 0.198** (0.079; p=0.013) | -0.080 | -0.009 | 0.000 |
| Utilities and sanitary services | 63 | 0.048 (0.095; p=0.615) | -0.034 (0.105; p=0.749) | -0.082 (0.161; p=0.611) | -0.015 | -0.011 | 0.017 |
| Wholesale trade | 176 | -0.011 (0.055; p=0.835) | 0.023 (0.033; p=0.491) | 0.034 (0.065; p=0.597) | -0.050 | -0.012 | -0.012 |
| Hospitals | 117 | 0.540*** (0.166; p=0.001) | 0.016 (0.063; p=0.796) | -0.524*** (0.194; p=0.007) | 0.056 | -0.015 | 0.044 |
| Mfg: primary and fabricated metals | 105 | -0.127 (0.077; p=0.102) | -0.149** (0.061; p=0.014) | -0.023 (0.124; p=0.854) | -0.079 | -0.016 | 0.001 |
| Mfg: paper, printing, publishing | 82 | 0.133 (0.115; p=0.244) | -0.066 (0.060; p=0.274) | -0.199 (0.146; p=0.172) | -0.006 | -0.020 | 0.003 |
| Mfg: motor vehicles, aircraft, other transport eq. | 152 | -0.203*** (0.065; p=0.002) | 0.038 (0.040; p=0.337) | 0.242*** (0.072; p=<0.001) | 0.040 | -0.023 | 0.033 |
| Communications | 73 | 0.179* (0.105; p=0.088) | 0.020 (0.052; p=0.695) | -0.158 (0.133; p=0.235) | 0.029 | -0.025 | 0.033 |
| Mining | 35 | -0.400** (0.162; p=0.013) | 0.154 (0.099; p=0.120) | 0.554** (0.251; p=0.027) | -0.002 | -0.026 | 0.016 |
| Finance: banking, credit, securities | 92 | 0.319*** (0.078; p=<0.001) | 0.054 (0.088; p=0.541) | -0.265** (0.133; p=0.046) | 0.100 | -0.033 | 0.031 |
| Mfg: food, tobacco | 78 | -0.033 (0.116; p=0.777) | 0.021 (0.099; p=0.835) | 0.054 (0.110; p=0.626) | -0.027 | -0.037 | 0.010 |
| Mfg: instruments, misc. manufacturing | 35 | 0.020 (0.137; p=0.883) | -0.102 (0.067; p=0.127) | -0.122 (0.174; p=0.483) | 0.047 | -0.041 | 0.030 |
| Transportation (excl. postal) | 243 | -0.083 (0.069; p=0.227) | -0.008 (0.039; p=0.833) | 0.075 (0.083; p=0.366) | -0.071 | -0.043 | -0.029 |
| Mfg: electrical equipment | 59 | -0.033 (0.074; p=0.652) | -0.121 (0.102; p=0.232) | -0.088 (0.135; p=0.516) | 0.014 | -0.045 | 0.005 |
| Construction (reference in estimation) | 543 | -0.179*** (0.034; p=<0.001) | 0.012 (0.029; p=0.673) | 0.191*** (0.049; p=<0.001) | -0.073 | -0.045 | -0.015 |
| Mfg: machinery and computers | 86 | -0.019 (0.070; p=0.783) | 0.033 (0.049; p=0.496) | 0.052 (0.087; p=0.547) | -0.020 | -0.052 | -0.004 |
| Other health services | 68 | 0.124 (0.125; p=0.320) | -0.042 (0.129; p=0.741) | -0.167 (0.214; p=0.436) | 0.097 | -0.052 | 0.047 |
| Insurance | 44 | 0.390*** (0.100; p=<0.001) | 0.014 (0.049; p=0.773) | -0.376*** (0.123; p=0.002) | 0.103 | -0.059 | 0.031 |
| Retail trade (excl. eating, drinking) | 435 | -0.046 (0.048; p=0.335) | -0.033 (0.035; p=0.340) | 0.013 (0.067; p=0.848) | -0.042 | -0.062 | -0.052 |
| Automotive and repair services | 122 | -0.285*** (0.082; p=<0.001) | 0.075 (0.064; p=0.244) | 0.360*** (0.121; p=0.003) | -0.100 | -0.072 | -0.065 |
| Other business services | 150 | 0.181 (0.112; p=0.107) | -0.029 (0.080; p=0.719) | -0.210 (0.168; p=0.212) | -0.033 | -0.075 | -0.065 |
| Eating, drinking, hotels | 292 | -0.021 (0.046; p=0.648) | 0.022 (0.050; p=0.663) | 0.043 (0.078; p=0.583) | -0.068 | -0.078 | -0.034 |
| Computer and data processing services | 66 | 0.237** (0.118; p=0.044) | -0.210* (0.114; p=0.066) | -0.447** (0.219; p=0.041) | 0.016 | -0.081 | 0.002 |
| Personal services, entertainment | 136 | -0.286** (0.134; p=0.033) | 0.096 (0.085; p=0.258) | 0.382** (0.194; p=0.049) | -0.064 | -0.082 | -0.068 |
| Agriculture, forestry, fishing | 168 | -0.030 (0.073; p=0.684) | 0.013 (0.054; p=0.801) | 0.043 (0.102; p=0.671) | -0.167 | -0.106 | -0.095 |
| Real estate | 47 | 0.060 (0.108; p=0.577) | 0.085 (0.095; p=0.370) | 0.024 (0.152; p=0.872) | -0.031 | -0.112 | -0.053 |

Across early groups with >= 30 sons (weighted by sons): s.d. of the PSID slope after 35 0.058 per 10 years (includes sampling noise); correlation with the MORG band growth after 35 -0.012.

## A. Is wage growth after 35 faster for sons who were in finance / law / professional services at 25-34?

### A1P. Wage growth after 35 by where the son was at 25-34 (PSID)

Son-level regressions (outcome in the column header; one row per son observed at 25-34 and in the later window). Regressors: the son's EARLY occupation x industry cell (modal at 25-34) classified by the data-defined sets of Section D (reference = cells neither high-paid nor high later growth); column (5) the same sets defined on industry groups; column (6) the pre-chosen illustrative industries only. Controls: mean age in each window, birth-year quadratic.

| | (1) Delta ln wage (40-55) - (25-34): early cell sets | (2) ... + ln parental income, Black, education | (3) Delta ln wage (35-55) - (25-34): early cell sets | (4) Delta ln wage (45-55) - (25-34): early cell sets | (5) Delta (40-55) - (25-34): early industry sets | (6) illustrative: early finance / insurance / legal / professional |
|---|---|---|---|---|---|---|
| **Pooled (weighted)** | | | | | | |
| early cell high-paid AND high later growth | 0.223*** (0.039; p=<0.001) | 0.104** (0.041; p=0.012) | 0.220*** (0.029; p=<0.001) | 0.265*** (0.047; p=<0.001) |  |  |
| early cell high-paid only | 0.203*** (0.043; p=<0.001) | 0.094** (0.046; p=0.043) | 0.218*** (0.031; p=<0.001) | 0.249*** (0.051; p=<0.001) |  |  |
| early cell high later growth only | 0.097*** (0.038; p=0.010) | 0.058 (0.038; p=0.124) | 0.089*** (0.030; p=0.003) | 0.143*** (0.054; p=0.009) |  |  |
| early industry high-paid AND high later growth |  |  |  |  | 0.130*** (0.042; p=0.002) |  |
| early industry high-paid only |  |  |  |  | 0.045 (0.042; p=0.278) |  |
| early industry high later growth only |  |  |  |  | 0.080** (0.037; p=0.033) |  |
| illustrative: early finance / insurance / legal / professional |  |  |  |  |  | 0.229*** (0.059; p=<0.001) |
| ln parental income |  | 0.025 (0.028; p=0.362) |  |  |  |  |
| Black |  | 0.010 (0.049; p=0.832) |  |  |  |  |
| years of education |  | 0.048*** (0.008; p=<0.001) |  |  |  |  |
| Mean of outcome (all sons) | 0.330 | 0.330 | 0.266 | 0.345 | 0.331 | 0.331 |
| N sons / clusters | 2,019 / 1,137 | 2,019 / 1,137 | 2,775 / 1,362 | 1,387 / 886 | 2,048 / 1,146 | 2,048 / 1,146 |
| Sons with Delta(40-55) by early cell set: HH ; high-paid only ; high growth only ; neither | 286 ; 215 ; 166 ; 1352 |  |  |  | 242 ; 245 ; 259 ; 1302 | 118 |
| **Black** | | | | | | |
| early cell high-paid AND high later growth | 0.056 (0.059; p=0.341) | 0.015 (0.071; p=0.830) | 0.094** (0.041; p=0.021) | 0.091 (0.070; p=0.196) |  |  |
| early cell high-paid only | 0.107 (0.110; p=0.330) | 0.071 (0.117; p=0.543) | 0.071 (0.068; p=0.294) | 0.136 (0.111; p=0.221) |  |  |
| early cell high later growth only | 0.016 (0.060; p=0.790) | 0.007 (0.060; p=0.914) | 0.034 (0.041; p=0.409) | 0.014 (0.086; p=0.868) |  |  |
| early industry high-paid AND high later growth |  |  |  |  | 0.150*** (0.055; p=0.006) |  |
| early industry high-paid only |  |  |  |  | 0.075 (0.057; p=0.186) |  |
| early industry high later growth only |  |  |  |  | -0.003 (0.047; p=0.957) |  |
| illustrative: early finance / insurance / legal / professional |  |  |  |  |  | 0.220** (0.107; p=0.040) |
| ln parental income |  | -0.015 (0.031; p=0.630) |  |  |  |  |
| years of education |  | 0.016 (0.013; p=0.212) |  |  |  |  |
| Mean of outcome (all sons) | 0.191 | 0.191 | 0.140 | 0.200 | 0.193 | 0.193 |
| N sons / clusters | 670 / 368 | 670 / 368 | 994 / 463 | 439 / 270 | 688 / 374 | 688 / 374 |
| Sons with Delta(40-55) by early cell set: HH ; high-paid only ; high growth only ; neither | 46 ; 25 ; 62 ; 537 |  |  |  | 81 ; 59 ; 90 ; 458 | 22 |
| **White** | | | | | | |
| early cell high-paid AND high later growth | 0.249*** (0.038; p=<0.001) | 0.124*** (0.040; p=0.002) | 0.236*** (0.028; p=<0.001) | 0.277*** (0.050; p=<0.001) |  |  |
| early cell high-paid only | 0.208*** (0.042; p=<0.001) | 0.092** (0.044; p=0.036) | 0.213*** (0.030; p=<0.001) | 0.278*** (0.052; p=<0.001) |  |  |
| early cell high later growth only | 0.106** (0.041; p=0.010) | 0.055 (0.041; p=0.172) | 0.092*** (0.031; p=0.003) | 0.170*** (0.057; p=0.003) |  |  |
| early industry high-paid AND high later growth |  |  |  |  | 0.135*** (0.042; p=0.001) |  |
| early industry high-paid only |  |  |  |  | 0.076* (0.042; p=0.068) |  |
| early industry high later growth only |  |  |  |  | 0.098** (0.038; p=0.010) |  |
| illustrative: early finance / insurance / legal / professional |  |  |  |  |  | 0.219*** (0.056; p=<0.001) |
| ln parental income |  | 0.034 (0.029; p=0.241) |  |  |  |  |
| years of education |  | 0.053*** (0.008; p=<0.001) |  |  |  |  |
| Mean of outcome (all sons) | 0.325 | 0.325 | 0.266 | 0.338 | 0.327 | 0.327 |
| N sons / clusters | 1,349 / 770 | 1,349 / 770 | 1,782 / 903 | 948 / 617 | 1,360 / 773 | 1,360 / 773 |
| Sons with Delta(40-55) by early cell set: HH ; high-paid only ; high growth only ; neither | 240 ; 190 ; 104 ; 815 |  |  |  | 161 ; 186 ; 169 ; 844 | 96 |
| **Black - White** | | | | | | |
| early cell high-paid AND high later growth | -0.193*** (0.070; p=0.006) | -0.108 (0.082; p=0.187) | -0.141*** (0.050; p=0.004) | -0.187** (0.086; p=0.029) |  |  |
| early cell high-paid only | -0.101 (0.117; p=0.389) | -0.021 (0.125; p=0.867) | -0.142* (0.074; p=0.056) | -0.141 (0.123; p=0.251) |  |  |
| early cell high later growth only | -0.090 (0.073; p=0.217) | -0.049 (0.073; p=0.502) | -0.059 (0.051; p=0.254) | -0.156 (0.104; p=0.132) |  |  |
| early industry high-paid AND high later growth |  |  |  |  | 0.016 (0.069; p=0.821) |  |
| early industry high-paid only |  |  |  |  | -0.001 (0.070; p=0.991) |  |
| early industry high later growth only |  |  |  |  | -0.101* (0.061; p=0.097) |  |
| illustrative: early finance / insurance / legal / professional |  |  |  |  |  | 0.000 (0.121; p=0.999) |
| ln parental income |  | -0.049 (0.042; p=0.250) |  |  |  |  |
| years of education |  | -0.037** (0.015; p=0.016) |  |  |  |  |

### A3P. Within-person wage growth before and after 35 by early set (PSID)

Son-year regressions of ln wage on person fixed effects, year fixed effects, a common kink at 35 and the early-set indicators interacted with the piecewise age terms (s1 = min(age-35,0)/10, s2 = max(age-35,0)/10). Coefficients = slope differences (log points per 10 years) relative to sons whose early cell / industry is in neither set (column 3: relative to all other industries). Person FE remove cohort and level differences; with person and year FE the common linear age slope is not identified, the differences are. Ages 25-55, all son-years of sons with an early cell.

| | (1) ln wage, person FE: early cell sets | (2) ln wage, person FE: early industry sets | (3) illustrative: early finance / insurance / legal / professional |
|---|---|---|---|
| **Pooled (weighted)** | | | |
| early cell high-paid AND high later growth x slope 25-35 (per 10 yrs) | 0.329*** (0.044; p=<0.001) |  |  |
| early cell high-paid AND high later growth x slope 35-55 (per 10 yrs) | 0.059** (0.028; p=0.036) |  |  |
| early cell high-paid AND high later growth x acceleration = slope 35-55 - slope 25-35 | -0.269*** (0.054; p=<0.001) |  |  |
| early cell high-paid only x slope 25-35 (per 10 yrs) | 0.394*** (0.050; p=<0.001) |  |  |
| early cell high-paid only x slope 35-55 (per 10 yrs) | 0.012 (0.038; p=0.761) |  |  |
| early cell high-paid only x acceleration = slope 35-55 - slope 25-35 | -0.383*** (0.073; p=<0.001) |  |  |
| early cell high later growth only x slope 25-35 (per 10 yrs) | 0.113*** (0.042; p=0.007) |  |  |
| early cell high later growth only x slope 35-55 (per 10 yrs) | 0.059 (0.038; p=0.116) |  |  |
| early cell high later growth only x acceleration = slope 35-55 - slope 25-35 | -0.054 (0.066; p=0.413) |  |  |
| early industry high-paid AND high later growth x slope 25-35 (per 10 yrs) |  | 0.156*** (0.046; p=<0.001) |  |
| early industry high-paid AND high later growth x slope 35-55 (per 10 yrs) |  | 0.001 (0.036; p=0.980) |  |
| early industry high-paid AND high later growth x acceleration = slope 35-55 - slope 25-35 |  | -0.155*** (0.057; p=0.006) |  |
| early industry high-paid only x slope 25-35 (per 10 yrs) |  | 0.178*** (0.045; p=<0.001) |  |
| early industry high-paid only x slope 35-55 (per 10 yrs) |  | -0.018 (0.036; p=0.613) |  |
| early industry high-paid only x acceleration = slope 35-55 - slope 25-35 |  | -0.196*** (0.066; p=0.003) |  |
| early industry high later growth only x slope 25-35 (per 10 yrs) |  | 0.111*** (0.042; p=0.008) |  |
| early industry high later growth only x slope 35-55 (per 10 yrs) |  | -0.004 (0.028; p=0.876) |  |
| early industry high later growth only x acceleration = slope 35-55 - slope 25-35 |  | -0.116** (0.053; p=0.030) |  |
| early illustrative finance / insurance / legal / professional x slope 25-35 (per 10 yrs) |  |  | 0.333*** (0.060; p=<0.001) |
| early illustrative finance / insurance / legal / professional x slope 35-55 (per 10 yrs) |  |  | 0.013 (0.057; p=0.818) |
| early illustrative finance / insurance / legal / professional x acceleration = slope 35-55 - slope 25-35 |  |  | -0.320*** (0.092; p=<0.001) |
| Person FE, year FE, common kink at 35; N son-years / sons / clusters | 40,550 / 4,307 / 1,686 | 40,550 / 4,307 / 1,686 | 40,550 / 4,307 / 1,686 |
| **Black** | | | |
| early cell high-paid AND high later growth x slope 25-35 (per 10 yrs) | 0.156** (0.067; p=0.019) |  |  |
| early cell high-paid AND high later growth x slope 35-55 (per 10 yrs) | 0.017 (0.047; p=0.726) |  |  |
| early cell high-paid AND high later growth x acceleration = slope 35-55 - slope 25-35 | -0.140 (0.095; p=0.142) |  |  |
| early cell high-paid only x slope 25-35 (per 10 yrs) | 0.348*** (0.128; p=0.007) |  |  |
| early cell high-paid only x slope 35-55 (per 10 yrs) | -0.078 (0.082; p=0.341) |  |  |
| early cell high-paid only x acceleration = slope 35-55 - slope 25-35 | -0.426** (0.189; p=0.024) |  |  |
| early cell high later growth only x slope 25-35 (per 10 yrs) | 0.047 (0.061; p=0.438) |  |  |
| early cell high later growth only x slope 35-55 (per 10 yrs) | -0.040 (0.055; p=0.462) |  |  |
| early cell high later growth only x acceleration = slope 35-55 - slope 25-35 | -0.088 (0.090; p=0.333) |  |  |
| early industry high-paid AND high later growth x slope 25-35 (per 10 yrs) |  | 0.265*** (0.069; p=<0.001) |  |
| early industry high-paid AND high later growth x slope 35-55 (per 10 yrs) |  | 0.016 (0.038; p=0.669) |  |
| early industry high-paid AND high later growth x acceleration = slope 35-55 - slope 25-35 |  | -0.249*** (0.087; p=0.004) |  |
| early industry high-paid only x slope 25-35 (per 10 yrs) |  | 0.071 (0.071; p=0.321) |  |
| early industry high-paid only x slope 35-55 (per 10 yrs) |  | 0.008 (0.050; p=0.866) |  |
| early industry high-paid only x acceleration = slope 35-55 - slope 25-35 |  | -0.062 (0.101; p=0.538) |  |
| early industry high later growth only x slope 25-35 (per 10 yrs) |  | 0.108** (0.053; p=0.041) |  |
| early industry high later growth only x slope 35-55 (per 10 yrs) |  | -0.031 (0.040; p=0.442) |  |
| early industry high later growth only x acceleration = slope 35-55 - slope 25-35 |  | -0.139* (0.073; p=0.056) |  |
| early illustrative finance / insurance / legal / professional x slope 25-35 (per 10 yrs) |  |  | 0.219** (0.097; p=0.023) |
| early illustrative finance / insurance / legal / professional x slope 35-55 (per 10 yrs) |  |  | 0.078 (0.064; p=0.226) |
| early illustrative finance / insurance / legal / professional x acceleration = slope 35-55 - slope 25-35 |  |  | -0.142 (0.136; p=0.298) |
| Person FE, year FE, common kink at 35; N son-years / sons / clusters | 13,791 / 1,724 / 615 | 13,791 / 1,724 / 615 | 13,791 / 1,724 / 615 |
| **White** | | | |
| early cell high-paid AND high later growth x slope 25-35 (per 10 yrs) | 0.354*** (0.043; p=<0.001) |  |  |
| early cell high-paid AND high later growth x slope 35-55 (per 10 yrs) | 0.063** (0.030; p=0.034) |  |  |
| early cell high-paid AND high later growth x acceleration = slope 35-55 - slope 25-35 | -0.291*** (0.055; p=<0.001) |  |  |
| early cell high-paid only x slope 25-35 (per 10 yrs) | 0.366*** (0.050; p=<0.001) |  |  |
| early cell high-paid only x slope 35-55 (per 10 yrs) | 0.038 (0.038; p=0.312) |  |  |
| early cell high-paid only x acceleration = slope 35-55 - slope 25-35 | -0.327*** (0.072; p=<0.001) |  |  |
| early cell high later growth only x slope 25-35 (per 10 yrs) | 0.123*** (0.046; p=0.008) |  |  |
| early cell high later growth only x slope 35-55 (per 10 yrs) | 0.075* (0.040; p=0.064) |  |  |
| early cell high later growth only x acceleration = slope 35-55 - slope 25-35 | -0.048 (0.072; p=0.508) |  |  |
| early industry high-paid AND high later growth x slope 25-35 (per 10 yrs) |  | 0.157*** (0.049; p=0.001) |  |
| early industry high-paid AND high later growth x slope 35-55 (per 10 yrs) |  | 0.007 (0.037; p=0.859) |  |
| early industry high-paid AND high later growth x acceleration = slope 35-55 - slope 25-35 |  | -0.151** (0.061; p=0.014) |  |
| early industry high-paid only x slope 25-35 (per 10 yrs) |  | 0.179*** (0.043; p=<0.001) |  |
| early industry high-paid only x slope 35-55 (per 10 yrs) |  | -0.003 (0.037; p=0.932) |  |
| early industry high-paid only x acceleration = slope 35-55 - slope 25-35 |  | -0.182*** (0.063; p=0.004) |  |
| early industry high later growth only x slope 25-35 (per 10 yrs) |  | 0.113** (0.045; p=0.011) |  |
| early industry high later growth only x slope 35-55 (per 10 yrs) |  | 0.003 (0.030; p=0.928) |  |
| early industry high later growth only x acceleration = slope 35-55 - slope 25-35 |  | -0.111* (0.057; p=0.054) |  |
| early illustrative finance / insurance / legal / professional x slope 25-35 (per 10 yrs) |  |  | 0.331*** (0.063; p=<0.001) |
| early illustrative finance / insurance / legal / professional x slope 35-55 (per 10 yrs) |  |  | 0.020 (0.054; p=0.716) |
| early illustrative finance / insurance / legal / professional x acceleration = slope 35-55 - slope 25-35 |  |  | -0.311*** (0.094; p=<0.001) |
| Person FE, year FE, common kink at 35; N son-years / sons / clusters | 26,772 / 2,586 / 1,078 | 26,772 / 2,586 / 1,078 | 26,772 / 2,586 / 1,078 |
| **Black - White** | | | |
| early cell high-paid AND high later growth x slope 25-35 (per 10 yrs) | -0.197** (0.080; p=0.013) |  |  |
| early cell high-paid AND high later growth x slope 35-55 (per 10 yrs) | -0.046 (0.056; p=0.410) |  |  |
| early cell high-paid AND high later growth x acceleration = slope 35-55 - slope 25-35 | 0.151 (0.110; p=0.168) |  |  |
| early cell high-paid only x slope 25-35 (per 10 yrs) | -0.018 (0.138; p=0.897) |  |  |
| early cell high-paid only x slope 35-55 (per 10 yrs) | -0.117 (0.091; p=0.198) |  |  |
| early cell high-paid only x acceleration = slope 35-55 - slope 25-35 | -0.099 (0.202; p=0.624) |  |  |
| early cell high later growth only x slope 25-35 (per 10 yrs) | -0.076 (0.076; p=0.323) |  |  |
| early cell high later growth only x slope 35-55 (per 10 yrs) | -0.115* (0.068; p=0.090) |  |  |
| early cell high later growth only x acceleration = slope 35-55 - slope 25-35 | -0.040 (0.116; p=0.732) |  |  |
| early industry high-paid AND high later growth x slope 25-35 (per 10 yrs) |  | 0.108 (0.085; p=0.203) |  |
| early industry high-paid AND high later growth x slope 35-55 (per 10 yrs) |  | 0.010 (0.053; p=0.857) |  |
| early industry high-paid AND high later growth x acceleration = slope 35-55 - slope 25-35 |  | -0.098 (0.106; p=0.355) |  |
| early industry high-paid only x slope 25-35 (per 10 yrs) |  | -0.109 (0.083; p=0.191) |  |
| early industry high-paid only x slope 35-55 (per 10 yrs) |  | 0.012 (0.062; p=0.852) |  |
| early industry high-paid only x acceleration = slope 35-55 - slope 25-35 |  | 0.120 (0.119; p=0.312) |  |
| early industry high later growth only x slope 25-35 (per 10 yrs) |  | -0.005 (0.069; p=0.944) |  |
| early industry high later growth only x slope 35-55 (per 10 yrs) |  | -0.034 (0.050; p=0.501) |  |
| early industry high later growth only x acceleration = slope 35-55 - slope 25-35 |  | -0.029 (0.093; p=0.756) |  |
| early illustrative finance / insurance / legal / professional x slope 25-35 (per 10 yrs) |  |  | -0.111 (0.115; p=0.335) |
| early illustrative finance / insurance / legal / professional x slope 35-55 (per 10 yrs) |  |  | 0.058 (0.084; p=0.491) |
| early illustrative finance / insurance / legal / professional x acceleration = slope 35-55 - slope 25-35 |  |  | 0.169 (0.166; p=0.307) |

### A2. Gelbach: early industry / cell x age-band fixed effects (PSID, any profile)

Short: son-years in a band, ln wage on ln parental income with Lee-Solon controls. Long: + fixed effects for the son's EARLY industry (cell, occupation) estimated separately in each band (and race) sample, i.e. early industry x band FE: they absorb any industry-specific age profile, linear or not, estimated in the PSID itself (not imported from the CPS), and any payoff after 35 of where the son started. Accounted for = short - long. Column (3) is the part of the rise from 25-34 to 35-55 that runs through the early industry. Same son-years in short and long. 'Current' rows use the industry / cell at each age. For reference, on ALL valid son-years the pooled coefficient rises by 0.139*** (0.022; p=<0.001) and the Black-White gap changes by -0.159*** (0.036; p=<0.001).

| | (1) accounted for at 25-34 (short - long) | (2) accounted for at 35-55 | (3) change (35-55)-(25-34) of the part accounted for | (4) rise of the coefficient on this sample (short) | (5) share = (3)/(4) | (6) B-W: change of the part accounted for | (7) change of the B-W gap (short) | (8) share = (6)/(7) | (9) pooled: change (45-55)-(25-34) of the part accounted for | (10) its share |
|---|---|---|---|---|---|---|---|---|---|---|
| **Long regression adds (fixed effects estimated separately in each band and race sample)** | | | | | | | | | | |
| early cell set, data-defined (high-paid & high later growth / high-paid only / high growth only / neither) [4 cells] | 0.056*** (0.006; p=<0.001) | 0.093*** (0.012; p=<0.001) | 0.036*** (0.009; p=<0.001) | 0.134*** (0.023; p=<0.001) | 0.271*** (0.067; p=<0.001) | -0.033*** (0.011; p=0.003) | -0.141*** (0.038; p=<0.001) | 0.237*** (0.087; p=0.006) | 0.043*** (0.014; p=0.003) | 0.294*** (0.101; p=0.004) |
| early industry set, data-defined (33 groups ranked the same way) [4 cells] | 0.024*** (0.005; p=<0.001) | 0.029*** (0.008; p=<0.001) | 0.005 (0.005; p=0.371) | 0.132*** (0.023; p=<0.001) | 0.034 (0.037; p=0.354) | -0.001 (0.008; p=0.919) | -0.140*** (0.037; p=<0.001) | 0.006 (0.058; p=0.918) | 0.009 (0.009; p=0.330) | 0.062 (0.061; p=0.308) |
| early industry group (33) [33 cells] | 0.034*** (0.007; p=<0.001) | 0.052*** (0.013; p=<0.001) | 0.018* (0.010; p=0.076) | 0.132*** (0.023; p=<0.001) | 0.135* (0.072; p=0.061) | -0.015 (0.016; p=0.332) | -0.140*** (0.037; p=<0.001) | 0.108 (0.105; p=0.304) | 0.025 (0.016; p=0.108) | 0.178* (0.103; p=0.085) |
| early industry group (33), sons with >= 2 early industry years [33 cells] | 0.034*** (0.007; p=<0.001) | 0.051*** (0.014; p=<0.001) | 0.017 (0.010; p=0.102) | 0.137*** (0.023; p=<0.001) | 0.124* (0.071; p=0.084) | -0.016 (0.016; p=0.312) | -0.136*** (0.037; p=<0.001) | 0.118 (0.110; p=0.283) | 0.023 (0.016; p=0.169) | 0.150 (0.102; p=0.140) |
| early fine industry (ind1990ddx) [208 cells] | 0.047*** (0.009; p=<0.001) | 0.083*** (0.018; p=<0.001) | 0.036** (0.014; p=0.010) | 0.132*** (0.023; p=<0.001) | 0.276*** (0.098; p=0.005) | -0.045* (0.025; p=0.069) | -0.140*** (0.037; p=<0.001) | 0.325* (0.167; p=0.052) | 0.049** (0.024; p=0.041) | 0.339** (0.153; p=0.027) |
| early manager / professional indicator (2 cells; compare with the 5 special cells) [2 cells] | 0.042*** (0.005; p=<0.001) | 0.076*** (0.010; p=<0.001) | 0.035*** (0.008; p=<0.001) | 0.134*** (0.023; p=<0.001) | 0.257*** (0.064; p=<0.001) | -0.035*** (0.010; p=<0.001) | -0.141*** (0.038; p=<0.001) | 0.246*** (0.086; p=0.004) | 0.051*** (0.013; p=<0.001) | 0.352*** (0.113; p=0.002) |
| illustrative: early pre-named cell (5 cells, Section D2; small) [5 cells] | 0.044*** (0.005; p=<0.001) | 0.082*** (0.010; p=<0.001) | 0.038*** (0.008; p=<0.001) | 0.134*** (0.023; p=<0.001) | 0.280*** (0.068; p=<0.001) | -0.037*** (0.010; p=<0.001) | -0.141*** (0.038; p=<0.001) | 0.264*** (0.090; p=0.003) | 0.055*** (0.014; p=<0.001) | 0.380*** (0.120; p=0.002) |
| early cell: occupation group (11) x industry group (33) [272 cells] | 0.091*** (0.011; p=<0.001) | 0.146*** (0.020; p=<0.001) | 0.054*** (0.015; p=<0.001) | 0.134*** (0.023; p=<0.001) | 0.405*** (0.099; p=<0.001) | -0.070*** (0.025; p=0.006) | -0.141*** (0.038; p=<0.001) | 0.493*** (0.171; p=0.004) | 0.066** (0.026; p=0.012) | 0.456*** (0.159; p=0.004) |
| early occupation (occ1990dd) [277 cells] | 0.086*** (0.011; p=<0.001) | 0.165*** (0.020; p=<0.001) | 0.079*** (0.017; p=<0.001) | 0.134*** (0.023; p=<0.001) | 0.591*** (0.120; p=<0.001) | -0.101*** (0.026; p=<0.001) | -0.141*** (0.038; p=<0.001) | 0.713*** (0.211; p=<0.001) | 0.083*** (0.026; p=0.002) | 0.567*** (0.184; p=0.002) |
| early occupation group (11) only [11 cells] | 0.057*** (0.007; p=<0.001) | 0.108*** (0.013; p=<0.001) | 0.051*** (0.010; p=<0.001) | 0.134*** (0.023; p=<0.001) | 0.377*** (0.078; p=<0.001) | -0.045*** (0.015; p=0.002) | -0.141*** (0.038; p=<0.001) | 0.318*** (0.111; p=0.004) | 0.057*** (0.016; p=<0.001) | 0.392*** (0.112; p=<0.001) |
| early occupation group (11) + early industry group (33), additive [11 + 33 cells] | 0.078*** (0.010; p=<0.001) | 0.129*** (0.017; p=<0.001) | 0.050*** (0.012; p=<0.001) | 0.134*** (0.023; p=<0.001) | 0.376*** (0.087; p=<0.001) | -0.050** (0.020; p=0.012) | -0.141*** (0.038; p=<0.001) | 0.352*** (0.129; p=0.006) | 0.068*** (0.020; p=<0.001) | 0.467*** (0.129; p=<0.001) |
| early occupation (occ1990dd) + early industry group (33), additive [277 + 33 cells] | 0.099*** (0.011; p=<0.001) | 0.184*** (0.021; p=<0.001) | 0.085*** (0.018; p=<0.001) | 0.134*** (0.023; p=<0.001) | 0.637*** (0.123; p=<0.001) | -0.109*** (0.028; p=<0.001) | -0.141*** (0.038; p=<0.001) | 0.769*** (0.213; p=<0.001) | 0.094*** (0.027; p=<0.001) | 0.647*** (0.182; p=<0.001) |
| early cell (11 x 33), cells with < 10 sons pooled [109 cells] | 0.077*** (0.010; p=<0.001) | 0.131*** (0.018; p=<0.001) | 0.054*** (0.013; p=<0.001) | 0.134*** (0.023; p=<0.001) | 0.402*** (0.090; p=<0.001) | -0.064*** (0.022; p=0.004) | -0.141*** (0.038; p=<0.001) | 0.452*** (0.156; p=0.004) | 0.068*** (0.022; p=0.002) | 0.467*** (0.140; p=<0.001) |
| early occupation (occ1990dd), occupations with < 10 sons pooled [103 cells] | 0.079*** (0.009; p=<0.001) | 0.136*** (0.018; p=<0.001) | 0.057*** (0.014; p=<0.001) | 0.134*** (0.023; p=<0.001) | 0.428*** (0.099; p=<0.001) | -0.070*** (0.020; p=<0.001) | -0.141*** (0.038; p=<0.001) | 0.496*** (0.162; p=0.002) | 0.052** (0.022; p=0.020) | 0.359** (0.150; p=0.016) |
| current industry group (33), any age profile [33 cells] | 0.029*** (0.006; p=<0.001) | 0.040*** (0.012; p=<0.001) | 0.011 (0.010; p=0.268) | 0.137*** (0.023; p=<0.001) | 0.078 (0.066; p=0.235) | 0.001 (0.015; p=0.964) | -0.145*** (0.038; p=<0.001) | -0.005 (0.106; p=0.964) | 0.020 (0.016; p=0.214) | 0.134 (0.099; p=0.177) |
| current fine industry, any age profile [213 cells] | 0.038*** (0.008; p=<0.001) | 0.065*** (0.015; p=<0.001) | 0.027** (0.012; p=0.027) | 0.137*** (0.023; p=<0.001) | 0.196** (0.076; p=0.010) | -0.007 (0.020; p=0.729) | -0.145*** (0.038; p=<0.001) | 0.049 (0.135; p=0.720) | 0.044* (0.023; p=0.061) | 0.293** (0.132; p=0.026) |
| current cell: occupation group x industry group, any age profile [332 cells] | 0.083*** (0.009; p=<0.001) | 0.142*** (0.018; p=<0.001) | 0.059*** (0.015; p=<0.001) | 0.145*** (0.024; p=<0.001) | 0.407*** (0.090; p=<0.001) | -0.031 (0.022; p=0.164) | -0.152*** (0.038; p=<0.001) | 0.203 (0.126; p=0.107) | 0.104*** (0.026; p=<0.001) | 0.660*** (0.159; p=<0.001) |
| illustrative: early finance / insurance / legal / professional indicator [2 cells] | 0.014*** (0.003; p=<0.001) | 0.027*** (0.007; p=<0.001) | 0.013** (0.005; p=0.011) | 0.132*** (0.023; p=<0.001) | 0.097** (0.039; p=0.013) | -0.012* (0.006; p=0.050) | -0.140*** (0.037; p=<0.001) | 0.085* (0.046; p=0.066) | 0.015* (0.009; p=0.098) | 0.103 (0.064; p=0.109) |

Short and long coefficients by band (detail):

| | ln wage 25-34: short | ln wage 25-34: long | ln wage 35-44: short | ln wage 35-44: long | ln wage 45-55: short | ln wage 45-55: long | ln wage 35-55: short | ln wage 35-55: long |
|---|---|---|---|---|---|---|---|---|
| **early cell set, data-defined (high-paid & high later growth / high-paid only / high growth only / neither)** | | | | | | | | |
| Pooled (weighted) | 0.270*** (0.017; p=<0.001) | 0.213*** (0.017; p=<0.001) | 0.398*** (0.026; p=<0.001) | 0.309*** (0.024; p=<0.001) | 0.415*** (0.041; p=<0.001) | 0.316*** (0.037; p=<0.001) | 0.404*** (0.029; p=<0.001) | 0.311*** (0.026; p=<0.001) |
| Black | 0.155*** (0.020; p=<0.001) | 0.128*** (0.018; p=<0.001) | 0.173*** (0.030; p=<0.001) | 0.141*** (0.028; p=<0.001) | 0.158*** (0.049; p=0.001) | 0.122** (0.048; p=0.010) | 0.169*** (0.032; p=<0.001) | 0.136*** (0.030; p=<0.001) |
| White | 0.254*** (0.020; p=<0.001) | 0.194*** (0.020; p=<0.001) | 0.396*** (0.032; p=<0.001) | 0.299*** (0.029; p=<0.001) | 0.448*** (0.049; p=<0.001) | 0.344*** (0.046; p=<0.001) | 0.410*** (0.033; p=<0.001) | 0.310*** (0.031; p=<0.001) |
| Black - White | -0.100*** (0.028; p=<0.001) | -0.067** (0.027; p=0.013) | -0.224*** (0.043; p=<0.001) | -0.158*** (0.041; p=<0.001) | -0.291*** (0.069; p=<0.001) | -0.222*** (0.066; p=<0.001) | -0.241*** (0.046; p=<0.001) | -0.174*** (0.043; p=<0.001) |
| N son-years: pooled per band ; Black / White per band | 25-34: 22,664 ; 35-44: 12,546 ; 45-55: 5,340 | 8,106 ; 14,570 ; 4,058 ; 8,489 ; 1,627 ; 3,713 |  |  |  |  |  |  |
| **early industry set, data-defined (33 groups ranked the same way)** | | | | | | | | |
| Pooled (weighted) | 0.271*** (0.017; p=<0.001) | 0.247*** (0.016; p=<0.001) | 0.398*** (0.026; p=<0.001) | 0.371*** (0.024; p=<0.001) | 0.414*** (0.040; p=<0.001) | 0.381*** (0.037; p=<0.001) | 0.403*** (0.028; p=<0.001) | 0.375*** (0.026; p=<0.001) |
| Black | 0.160*** (0.020; p=<0.001) | 0.143*** (0.019; p=<0.001) | 0.175*** (0.030; p=<0.001) | 0.154*** (0.029; p=<0.001) | 0.166*** (0.048; p=<0.001) | 0.143*** (0.046; p=0.002) | 0.173*** (0.031; p=<0.001) | 0.151*** (0.030; p=<0.001) |
| White | 0.255*** (0.020; p=<0.001) | 0.227*** (0.019; p=<0.001) | 0.395*** (0.031; p=<0.001) | 0.363*** (0.029; p=<0.001) | 0.446*** (0.049; p=<0.001) | 0.406*** (0.046; p=<0.001) | 0.408*** (0.033; p=<0.001) | 0.374*** (0.031; p=<0.001) |
| Black - White | -0.095*** (0.028; p=<0.001) | -0.084*** (0.027; p=0.002) | -0.219*** (0.043; p=<0.001) | -0.209*** (0.041; p=<0.001) | -0.280*** (0.068; p=<0.001) | -0.263*** (0.065; p=<0.001) | -0.235*** (0.046; p=<0.001) | -0.223*** (0.043; p=<0.001) |
| N son-years: pooled per band ; Black / White per band | 25-34: 22,947 ; 35-44: 12,719 ; 45-55: 5,447 | 8,284 ; 14,675 ; 4,163 ; 8,557 ; 1,692 ; 3,755 |  |  |  |  |  |  |
| **early industry group (33)** | | | | | | | | |
| Pooled (weighted) | 0.271*** (0.017; p=<0.001) | 0.237*** (0.016; p=<0.001) | 0.398*** (0.026; p=<0.001) | 0.348*** (0.024; p=<0.001) | 0.414*** (0.040; p=<0.001) | 0.354*** (0.036; p=<0.001) | 0.403*** (0.028; p=<0.001) | 0.351*** (0.025; p=<0.001) |
| Black | 0.160*** (0.020; p=<0.001) | 0.139*** (0.017; p=<0.001) | 0.175*** (0.030; p=<0.001) | 0.145*** (0.026; p=<0.001) | 0.166*** (0.048; p=<0.001) | 0.105** (0.041; p=0.011) | 0.173*** (0.031; p=<0.001) | 0.136*** (0.026; p=<0.001) |
| White | 0.255*** (0.020; p=<0.001) | 0.218*** (0.019; p=<0.001) | 0.395*** (0.031; p=<0.001) | 0.329*** (0.029; p=<0.001) | 0.446*** (0.049; p=<0.001) | 0.367*** (0.043; p=<0.001) | 0.408*** (0.033; p=<0.001) | 0.340*** (0.030; p=<0.001) |
| Black - White | -0.095*** (0.028; p=<0.001) | -0.079*** (0.025; p=0.002) | -0.219*** (0.043; p=<0.001) | -0.184*** (0.039; p=<0.001) | -0.280*** (0.068; p=<0.001) | -0.262*** (0.059; p=<0.001) | -0.235*** (0.046; p=<0.001) | -0.204*** (0.040; p=<0.001) |
| N son-years: pooled per band ; Black / White per band | 25-34: 22,947 ; 35-44: 12,719 ; 45-55: 5,447 | 8,284 ; 14,675 ; 4,163 ; 8,557 ; 1,692 ; 3,755 |  |  |  |  |  |  |
| **early industry group (33), sons with >= 2 early industry years** | | | | | | | | |
| Pooled (weighted) | 0.271*** (0.017; p=<0.001) | 0.237*** (0.016; p=<0.001) | 0.401*** (0.026; p=<0.001) | 0.352*** (0.023; p=<0.001) | 0.422*** (0.041; p=<0.001) | 0.365*** (0.036; p=<0.001) | 0.408*** (0.028; p=<0.001) | 0.356*** (0.025; p=<0.001) |
| Black | 0.160*** (0.020; p=<0.001) | 0.140*** (0.018; p=<0.001) | 0.185*** (0.031; p=<0.001) | 0.155*** (0.027; p=<0.001) | 0.176*** (0.049; p=<0.001) | 0.121*** (0.043; p=0.005) | 0.182*** (0.032; p=<0.001) | 0.147*** (0.028; p=<0.001) |
| White | 0.255*** (0.020; p=<0.001) | 0.218*** (0.019; p=<0.001) | 0.399*** (0.030; p=<0.001) | 0.333*** (0.027; p=<0.001) | 0.455*** (0.048; p=<0.001) | 0.379*** (0.042; p=<0.001) | 0.413*** (0.032; p=<0.001) | 0.345*** (0.028; p=<0.001) |
| Black - White | -0.095*** (0.028; p=<0.001) | -0.078*** (0.026; p=0.002) | -0.214*** (0.043; p=<0.001) | -0.178*** (0.039; p=<0.001) | -0.280*** (0.069; p=<0.001) | -0.259*** (0.060; p=<0.001) | -0.231*** (0.046; p=<0.001) | -0.199*** (0.040; p=<0.001) |
| N son-years: pooled per band ; Black / White per band | 25-34: 22,449 ; 35-44: 12,316 ; 45-55: 5,298 | 8,017 ; 14,444 ; 3,947 ; 8,370 ; 1,605 ; 3,693 |  |  |  |  |  |  |
| **early fine industry (ind1990ddx)** | | | | | | | | |
| Pooled (weighted) | 0.271*** (0.017; p=<0.001) | 0.224*** (0.015; p=<0.001) | 0.398*** (0.026; p=<0.001) | 0.318*** (0.023; p=<0.001) | 0.414*** (0.040; p=<0.001) | 0.319*** (0.036; p=<0.001) | 0.403*** (0.028; p=<0.001) | 0.320*** (0.024; p=<0.001) |
| Black | 0.160*** (0.020; p=<0.001) | 0.130*** (0.017; p=<0.001) | 0.175*** (0.030; p=<0.001) | 0.139*** (0.026; p=<0.001) | 0.166*** (0.048; p=<0.001) | 0.122** (0.048; p=0.011) | 0.173*** (0.031; p=<0.001) | 0.135*** (0.026; p=<0.001) |
| White | 0.255*** (0.020; p=<0.001) | 0.205*** (0.018; p=<0.001) | 0.395*** (0.031; p=<0.001) | 0.295*** (0.028; p=<0.001) | 0.446*** (0.049; p=<0.001) | 0.335*** (0.046; p=<0.001) | 0.408*** (0.033; p=<0.001) | 0.305*** (0.029; p=<0.001) |
| Black - White | -0.095*** (0.028; p=<0.001) | -0.076*** (0.025; p=0.002) | -0.219*** (0.043; p=<0.001) | -0.156*** (0.038; p=<0.001) | -0.280*** (0.068; p=<0.001) | -0.212*** (0.067; p=0.001) | -0.235*** (0.046; p=<0.001) | -0.170*** (0.040; p=<0.001) |
| N son-years: pooled per band ; Black / White per band | 25-34: 22,947 ; 35-44: 12,719 ; 45-55: 5,447 | 8,284 ; 14,675 ; 4,163 ; 8,557 ; 1,692 ; 3,755 |  |  |  |  |  |  |
| **early manager / professional indicator (2 cells; compare with the 5 special cells)** | | | | | | | | |
| Pooled (weighted) | 0.270*** (0.017; p=<0.001) | 0.228*** (0.017; p=<0.001) | 0.398*** (0.026; p=<0.001) | 0.330*** (0.025; p=<0.001) | 0.415*** (0.041; p=<0.001) | 0.322*** (0.039; p=<0.001) | 0.404*** (0.029; p=<0.001) | 0.328*** (0.027; p=<0.001) |
| Black | 0.155*** (0.020; p=<0.001) | 0.129*** (0.018; p=<0.001) | 0.173*** (0.030; p=<0.001) | 0.144*** (0.029; p=<0.001) | 0.158*** (0.049; p=0.001) | 0.128*** (0.048; p=0.008) | 0.169*** (0.032; p=<0.001) | 0.140*** (0.030; p=<0.001) |
| White | 0.254*** (0.020; p=<0.001) | 0.213*** (0.020; p=<0.001) | 0.396*** (0.032; p=<0.001) | 0.325*** (0.030; p=<0.001) | 0.448*** (0.049; p=<0.001) | 0.348*** (0.047; p=<0.001) | 0.410*** (0.033; p=<0.001) | 0.331*** (0.032; p=<0.001) |
| Black - White | -0.100*** (0.028; p=<0.001) | -0.084*** (0.027; p=0.002) | -0.224*** (0.043; p=<0.001) | -0.180*** (0.042; p=<0.001) | -0.291*** (0.069; p=<0.001) | -0.221*** (0.067; p=0.001) | -0.241*** (0.046; p=<0.001) | -0.190*** (0.044; p=<0.001) |
| N son-years: pooled per band ; Black / White per band | 25-34: 22,664 ; 35-44: 12,546 ; 45-55: 5,340 | 8,106 ; 14,570 ; 4,058 ; 8,489 ; 1,627 ; 3,713 |  |  |  |  |  |  |
| **illustrative: early pre-named cell (5 cells, Section D2; small)** | | | | | | | | |
| Pooled (weighted) | 0.270*** (0.017; p=<0.001) | 0.225*** (0.017; p=<0.001) | 0.398*** (0.026; p=<0.001) | 0.325*** (0.025; p=<0.001) | 0.415*** (0.041; p=<0.001) | 0.316*** (0.039; p=<0.001) | 0.404*** (0.029; p=<0.001) | 0.322*** (0.027; p=<0.001) |
| Black | 0.155*** (0.020; p=<0.001) | 0.128*** (0.019; p=<0.001) | 0.173*** (0.030; p=<0.001) | 0.143*** (0.028; p=<0.001) | 0.158*** (0.049; p=0.001) | 0.128*** (0.048; p=0.008) | 0.169*** (0.032; p=<0.001) | 0.139*** (0.030; p=<0.001) |
| White | 0.254*** (0.020; p=<0.001) | 0.209*** (0.020; p=<0.001) | 0.396*** (0.032; p=<0.001) | 0.319*** (0.030; p=<0.001) | 0.448*** (0.049; p=<0.001) | 0.341*** (0.047; p=<0.001) | 0.410*** (0.033; p=<0.001) | 0.324*** (0.032; p=<0.001) |
| Black - White | -0.100*** (0.028; p=<0.001) | -0.081*** (0.027; p=0.003) | -0.224*** (0.043; p=<0.001) | -0.175*** (0.042; p=<0.001) | -0.291*** (0.069; p=<0.001) | -0.213*** (0.067; p=0.002) | -0.241*** (0.046; p=<0.001) | -0.185*** (0.044; p=<0.001) |
| N son-years: pooled per band ; Black / White per band | 25-34: 22,664 ; 35-44: 12,546 ; 45-55: 5,340 | 8,106 ; 14,570 ; 4,058 ; 8,489 ; 1,627 ; 3,713 |  |  |  |  |  |  |
| **early cell: occupation group (11) x industry group (33)** | | | | | | | | |
| Pooled (weighted) | 0.270*** (0.017; p=<0.001) | 0.178*** (0.016; p=<0.001) | 0.398*** (0.026; p=<0.001) | 0.259*** (0.022; p=<0.001) | 0.415*** (0.041; p=<0.001) | 0.258*** (0.034; p=<0.001) | 0.404*** (0.029; p=<0.001) | 0.258*** (0.023; p=<0.001) |
| Black | 0.155*** (0.020; p=<0.001) | 0.112*** (0.016; p=<0.001) | 0.173*** (0.030; p=<0.001) | 0.133*** (0.026; p=<0.001) | 0.158*** (0.049; p=0.001) | 0.073 (0.045; p=0.108) | 0.169*** (0.032; p=<0.001) | 0.122*** (0.026; p=<0.001) |
| White | 0.254*** (0.020; p=<0.001) | 0.165*** (0.019; p=<0.001) | 0.396*** (0.032; p=<0.001) | 0.239*** (0.028; p=<0.001) | 0.448*** (0.049; p=<0.001) | 0.275*** (0.044; p=<0.001) | 0.410*** (0.033; p=<0.001) | 0.247*** (0.029; p=<0.001) |
| Black - White | -0.100*** (0.028; p=<0.001) | -0.053** (0.025; p=0.032) | -0.224*** (0.043; p=<0.001) | -0.106*** (0.038; p=0.005) | -0.291*** (0.069; p=<0.001) | -0.203*** (0.063; p=0.001) | -0.241*** (0.046; p=<0.001) | -0.125*** (0.039; p=0.001) |
| N son-years: pooled per band ; Black / White per band | 25-34: 22,664 ; 35-44: 12,546 ; 45-55: 5,340 | 8,106 ; 14,570 ; 4,058 ; 8,489 ; 1,627 ; 3,713 |  |  |  |  |  |  |
| **early occupation (occ1990dd)** | | | | | | | | |
| Pooled (weighted) | 0.270*** (0.017; p=<0.001) | 0.184*** (0.016; p=<0.001) | 0.398*** (0.026; p=<0.001) | 0.241*** (0.022; p=<0.001) | 0.415*** (0.041; p=<0.001) | 0.247*** (0.038; p=<0.001) | 0.404*** (0.029; p=<0.001) | 0.239*** (0.024; p=<0.001) |
| Black | 0.155*** (0.020; p=<0.001) | 0.115*** (0.018; p=<0.001) | 0.173*** (0.030; p=<0.001) | 0.135*** (0.029; p=<0.001) | 0.158*** (0.049; p=0.001) | 0.118** (0.048; p=0.014) | 0.169*** (0.032; p=<0.001) | 0.127*** (0.030; p=<0.001) |
| White | 0.254*** (0.020; p=<0.001) | 0.170*** (0.019; p=<0.001) | 0.396*** (0.032; p=<0.001) | 0.214*** (0.026; p=<0.001) | 0.448*** (0.049; p=<0.001) | 0.268*** (0.047; p=<0.001) | 0.410*** (0.033; p=<0.001) | 0.222*** (0.028; p=<0.001) |
| Black - White | -0.100*** (0.028; p=<0.001) | -0.055** (0.026; p=0.036) | -0.224*** (0.043; p=<0.001) | -0.079** (0.039; p=0.046) | -0.291*** (0.069; p=<0.001) | -0.150** (0.067; p=0.026) | -0.241*** (0.046; p=<0.001) | -0.095** (0.041; p=0.020) |
| N son-years: pooled per band ; Black / White per band | 25-34: 22,664 ; 35-44: 12,546 ; 45-55: 5,340 | 8,106 ; 14,570 ; 4,058 ; 8,489 ; 1,627 ; 3,713 |  |  |  |  |  |  |
| **early occupation group (11) only** | | | | | | | | |
| Pooled (weighted) | 0.270*** (0.017; p=<0.001) | 0.212*** (0.017; p=<0.001) | 0.398*** (0.026; p=<0.001) | 0.294*** (0.024; p=<0.001) | 0.415*** (0.041; p=<0.001) | 0.301*** (0.036; p=<0.001) | 0.404*** (0.029; p=<0.001) | 0.296*** (0.025; p=<0.001) |
| Black | 0.155*** (0.020; p=<0.001) | 0.123*** (0.018; p=<0.001) | 0.173*** (0.030; p=<0.001) | 0.126*** (0.028; p=<0.001) | 0.158*** (0.049; p=0.001) | 0.102** (0.047; p=0.029) | 0.169*** (0.032; p=<0.001) | 0.119*** (0.029; p=<0.001) |
| White | 0.254*** (0.020; p=<0.001) | 0.203*** (0.019; p=<0.001) | 0.396*** (0.032; p=<0.001) | 0.283*** (0.028; p=<0.001) | 0.448*** (0.049; p=<0.001) | 0.330*** (0.045; p=<0.001) | 0.410*** (0.033; p=<0.001) | 0.295*** (0.030; p=<0.001) |
| Black - White | -0.100*** (0.028; p=<0.001) | -0.079*** (0.026; p=0.003) | -0.224*** (0.043; p=<0.001) | -0.157*** (0.040; p=<0.001) | -0.291*** (0.069; p=<0.001) | -0.227*** (0.065; p=<0.001) | -0.241*** (0.046; p=<0.001) | -0.176*** (0.042; p=<0.001) |
| N son-years: pooled per band ; Black / White per band | 25-34: 22,664 ; 35-44: 12,546 ; 45-55: 5,340 | 8,106 ; 14,570 ; 4,058 ; 8,489 ; 1,627 ; 3,713 |  |  |  |  |  |  |
| **early occupation group (11) + early industry group (33), additive** | | | | | | | | |
| Pooled (weighted) | 0.270*** (0.017; p=<0.001) | 0.191*** (0.016; p=<0.001) | 0.398*** (0.026; p=<0.001) | 0.278*** (0.023; p=<0.001) | 0.415*** (0.041; p=<0.001) | 0.269*** (0.034; p=<0.001) | 0.404*** (0.029; p=<0.001) | 0.275*** (0.024; p=<0.001) |
| Black | 0.155*** (0.020; p=<0.001) | 0.117*** (0.016; p=<0.001) | 0.173*** (0.030; p=<0.001) | 0.125*** (0.025; p=<0.001) | 0.158*** (0.049; p=0.001) | 0.086** (0.040; p=0.033) | 0.169*** (0.032; p=<0.001) | 0.116*** (0.025; p=<0.001) |
| White | 0.254*** (0.020; p=<0.001) | 0.178*** (0.019; p=<0.001) | 0.396*** (0.032; p=<0.001) | 0.260*** (0.027; p=<0.001) | 0.448*** (0.049; p=<0.001) | 0.291*** (0.041; p=<0.001) | 0.410*** (0.033; p=<0.001) | 0.268*** (0.028; p=<0.001) |
| Black - White | -0.100*** (0.028; p=<0.001) | -0.061** (0.025; p=0.013) | -0.224*** (0.043; p=<0.001) | -0.135*** (0.037; p=<0.001) | -0.291*** (0.069; p=<0.001) | -0.206*** (0.057; p=<0.001) | -0.241*** (0.046; p=<0.001) | -0.153*** (0.037; p=<0.001) |
| N son-years: pooled per band ; Black / White per band | 25-34: 22,664 ; 35-44: 12,546 ; 45-55: 5,340 | 8,106 ; 14,570 ; 4,058 ; 8,489 ; 1,627 ; 3,713 |  |  |  |  |  |  |
| **early occupation (occ1990dd) + early industry group (33), additive** | | | | | | | | |
| Pooled (weighted) | 0.270*** (0.017; p=<0.001) | 0.171*** (0.016; p=<0.001) | 0.398*** (0.026; p=<0.001) | 0.224*** (0.021; p=<0.001) | 0.415*** (0.041; p=<0.001) | 0.222*** (0.035; p=<0.001) | 0.404*** (0.029; p=<0.001) | 0.219*** (0.022; p=<0.001) |
| Black | 0.155*** (0.020; p=<0.001) | 0.112*** (0.017; p=<0.001) | 0.173*** (0.030; p=<0.001) | 0.146*** (0.027; p=<0.001) | 0.158*** (0.049; p=0.001) | 0.078* (0.045; p=0.082) | 0.169*** (0.032; p=<0.001) | 0.130*** (0.027; p=<0.001) |
| White | 0.254*** (0.020; p=<0.001) | 0.155*** (0.019; p=<0.001) | 0.396*** (0.032; p=<0.001) | 0.200*** (0.026; p=<0.001) | 0.448*** (0.049; p=<0.001) | 0.254*** (0.043; p=<0.001) | 0.410*** (0.033; p=<0.001) | 0.206*** (0.027; p=<0.001) |
| Black - White | -0.100*** (0.028; p=<0.001) | -0.044* (0.025; p=0.080) | -0.224*** (0.043; p=<0.001) | -0.054 (0.037; p=0.146) | -0.291*** (0.069; p=<0.001) | -0.176*** (0.062; p=0.005) | -0.241*** (0.046; p=<0.001) | -0.077** (0.038; p=0.045) |
| N son-years: pooled per band ; Black / White per band | 25-34: 22,664 ; 35-44: 12,546 ; 45-55: 5,340 | 8,106 ; 14,570 ; 4,058 ; 8,489 ; 1,627 ; 3,713 |  |  |  |  |  |  |
| **early cell (11 x 33), cells with < 10 sons pooled** | | | | | | | | |
| Pooled (weighted) | 0.270*** (0.017; p=<0.001) | 0.193*** (0.016; p=<0.001) | 0.398*** (0.026; p=<0.001) | 0.275*** (0.022; p=<0.001) | 0.415*** (0.041; p=<0.001) | 0.271*** (0.034; p=<0.001) | 0.404*** (0.029; p=<0.001) | 0.273*** (0.023; p=<0.001) |
| Black | 0.155*** (0.020; p=<0.001) | 0.118*** (0.016; p=<0.001) | 0.173*** (0.030; p=<0.001) | 0.131*** (0.025; p=<0.001) | 0.158*** (0.049; p=0.001) | 0.100** (0.047; p=0.034) | 0.169*** (0.032; p=<0.001) | 0.127*** (0.026; p=<0.001) |
| White | 0.254*** (0.020; p=<0.001) | 0.176*** (0.019; p=<0.001) | 0.396*** (0.032; p=<0.001) | 0.256*** (0.028; p=<0.001) | 0.448*** (0.049; p=<0.001) | 0.288*** (0.044; p=<0.001) | 0.410*** (0.033; p=<0.001) | 0.263*** (0.029; p=<0.001) |
| Black - White | -0.100*** (0.028; p=<0.001) | -0.058** (0.025; p=0.019) | -0.224*** (0.043; p=<0.001) | -0.126*** (0.038; p=<0.001) | -0.291*** (0.069; p=<0.001) | -0.188*** (0.064; p=0.003) | -0.241*** (0.046; p=<0.001) | -0.136*** (0.039; p=<0.001) |
| N son-years: pooled per band ; Black / White per band | 25-34: 22,664 ; 35-44: 12,546 ; 45-55: 5,340 | 8,106 ; 14,570 ; 4,058 ; 8,489 ; 1,627 ; 3,713 |  |  |  |  |  |  |
| **early occupation (occ1990dd), occupations with < 10 sons pooled** | | | | | | | | |
| Pooled (weighted) | 0.270*** (0.017; p=<0.001) | 0.191*** (0.016; p=<0.001) | 0.398*** (0.026; p=<0.001) | 0.263*** (0.022; p=<0.001) | 0.415*** (0.041; p=<0.001) | 0.284*** (0.037; p=<0.001) | 0.404*** (0.029; p=<0.001) | 0.267*** (0.024; p=<0.001) |
| Black | 0.155*** (0.020; p=<0.001) | 0.118*** (0.018; p=<0.001) | 0.173*** (0.030; p=<0.001) | 0.131*** (0.027; p=<0.001) | 0.158*** (0.049; p=0.001) | 0.106** (0.049; p=0.031) | 0.169*** (0.032; p=<0.001) | 0.122*** (0.029; p=<0.001) |
| White | 0.254*** (0.020; p=<0.001) | 0.178*** (0.019; p=<0.001) | 0.396*** (0.032; p=<0.001) | 0.241*** (0.028; p=<0.001) | 0.448*** (0.049; p=<0.001) | 0.306*** (0.047; p=<0.001) | 0.410*** (0.033; p=<0.001) | 0.253*** (0.030; p=<0.001) |
| Black - White | -0.100*** (0.028; p=<0.001) | -0.060** (0.026; p=0.020) | -0.224*** (0.043; p=<0.001) | -0.110*** (0.039; p=0.005) | -0.291*** (0.069; p=<0.001) | -0.200*** (0.068; p=0.004) | -0.241*** (0.046; p=<0.001) | -0.131*** (0.042; p=0.002) |
| N son-years: pooled per band ; Black / White per band | 25-34: 22,664 ; 35-44: 12,546 ; 45-55: 5,340 | 8,106 ; 14,570 ; 4,058 ; 8,489 ; 1,627 ; 3,713 |  |  |  |  |  |  |
| **current industry group (33), any age profile** | | | | | | | | |
| Pooled (weighted) | 0.269*** (0.017; p=<0.001) | 0.240*** (0.015; p=<0.001) | 0.399*** (0.026; p=<0.001) | 0.363*** (0.023; p=<0.001) | 0.418*** (0.041; p=<0.001) | 0.369*** (0.036; p=<0.001) | 0.406*** (0.029; p=<0.001) | 0.366*** (0.024; p=<0.001) |
| Black | 0.160*** (0.020; p=<0.001) | 0.133*** (0.017; p=<0.001) | 0.174*** (0.030; p=<0.001) | 0.131*** (0.025; p=<0.001) | 0.168*** (0.048; p=<0.001) | 0.093** (0.039; p=0.016) | 0.173*** (0.032; p=<0.001) | 0.123*** (0.025; p=<0.001) |
| White | 0.254*** (0.020; p=<0.001) | 0.222*** (0.018; p=<0.001) | 0.398*** (0.032; p=<0.001) | 0.345*** (0.029; p=<0.001) | 0.453*** (0.049; p=<0.001) | 0.385*** (0.044; p=<0.001) | 0.412*** (0.034; p=<0.001) | 0.358*** (0.030; p=<0.001) |
| Black - White | -0.094*** (0.028; p=<0.001) | -0.089*** (0.025; p=<0.001) | -0.223*** (0.043; p=<0.001) | -0.213*** (0.038; p=<0.001) | -0.285*** (0.069; p=<0.001) | -0.291*** (0.058; p=<0.001) | -0.239*** (0.046; p=<0.001) | -0.235*** (0.039; p=<0.001) |
| N son-years: pooled per band ; Black / White per band | 25-34: 22,627 ; 35-44: 12,566 ; 45-55: 5,378 | 8,140 ; 14,499 ; 4,115 ; 8,452 ; 1,666 ; 3,712 |  |  |  |  |  |  |
| **current fine industry, any age profile** | | | | | | | | |
| Pooled (weighted) | 0.269*** (0.017; p=<0.001) | 0.231*** (0.015; p=<0.001) | 0.399*** (0.026; p=<0.001) | 0.338*** (0.022; p=<0.001) | 0.418*** (0.041; p=<0.001) | 0.336*** (0.033; p=<0.001) | 0.406*** (0.029; p=<0.001) | 0.341*** (0.023; p=<0.001) |
| Black | 0.160*** (0.020; p=<0.001) | 0.135*** (0.016; p=<0.001) | 0.174*** (0.030; p=<0.001) | 0.137*** (0.024; p=<0.001) | 0.168*** (0.048; p=<0.001) | 0.076* (0.043; p=0.077) | 0.173*** (0.032; p=<0.001) | 0.122*** (0.025; p=<0.001) |
| White | 0.254*** (0.020; p=<0.001) | 0.214*** (0.018; p=<0.001) | 0.398*** (0.032; p=<0.001) | 0.329*** (0.027; p=<0.001) | 0.453*** (0.049; p=<0.001) | 0.357*** (0.042; p=<0.001) | 0.412*** (0.034; p=<0.001) | 0.339*** (0.028; p=<0.001) |
| Black - White | -0.094*** (0.028; p=<0.001) | -0.079*** (0.024; p=<0.001) | -0.223*** (0.043; p=<0.001) | -0.193*** (0.037; p=<0.001) | -0.285*** (0.069; p=<0.001) | -0.281*** (0.060; p=<0.001) | -0.239*** (0.046; p=<0.001) | -0.217*** (0.038; p=<0.001) |
| N son-years: pooled per band ; Black / White per band | 25-34: 22,627 ; 35-44: 12,566 ; 45-55: 5,378 | 8,140 ; 14,499 ; 4,115 ; 8,452 ; 1,666 ; 3,712 |  |  |  |  |  |  |
| **current cell: occupation group x industry group, any age profile** | | | | | | | | |
| Pooled (weighted) | 0.258*** (0.017; p=<0.001) | 0.176*** (0.015; p=<0.001) | 0.397*** (0.027; p=<0.001) | 0.273*** (0.022; p=<0.001) | 0.416*** (0.041; p=<0.001) | 0.229*** (0.033; p=<0.001) | 0.403*** (0.029; p=<0.001) | 0.261*** (0.022; p=<0.001) |
| Black | 0.151*** (0.020; p=<0.001) | 0.109*** (0.016; p=<0.001) | 0.168*** (0.030; p=<0.001) | 0.108*** (0.023; p=<0.001) | 0.164*** (0.048; p=<0.001) | 0.039 (0.039; p=0.314) | 0.168*** (0.032; p=<0.001) | 0.091*** (0.022; p=<0.001) |
| White | 0.242*** (0.020; p=<0.001) | 0.159*** (0.017; p=<0.001) | 0.398*** (0.032; p=<0.001) | 0.261*** (0.027; p=<0.001) | 0.451*** (0.049; p=<0.001) | 0.253*** (0.039; p=<0.001) | 0.411*** (0.034; p=<0.001) | 0.262*** (0.027; p=<0.001) |
| Black - White | -0.091*** (0.028; p=0.001) | -0.051** (0.023; p=0.030) | -0.229*** (0.044; p=<0.001) | -0.153*** (0.036; p=<0.001) | -0.287*** (0.069; p=<0.001) | -0.214*** (0.055; p=<0.001) | -0.243*** (0.047; p=<0.001) | -0.172*** (0.035; p=<0.001) |
| N son-years: pooled per band ; Black / White per band | 25-34: 21,147 ; 35-44: 12,047 ; 45-55: 5,319 | 7,341 ; 13,818 ; 3,848 ; 8,200 ; 1,642 ; 3,677 |  |  |  |  |  |  |
| **illustrative: early finance / insurance / legal / professional indicator** | | | | | | | | |
| Pooled (weighted) | 0.271*** (0.017; p=<0.001) | 0.257*** (0.017; p=<0.001) | 0.398*** (0.026; p=<0.001) | 0.371*** (0.026; p=<0.001) | 0.414*** (0.040; p=<0.001) | 0.385*** (0.040; p=<0.001) | 0.403*** (0.028; p=<0.001) | 0.376*** (0.028; p=<0.001) |
| Black | 0.160*** (0.020; p=<0.001) | 0.156*** (0.020; p=<0.001) | 0.175*** (0.030; p=<0.001) | 0.168*** (0.029; p=<0.001) | 0.166*** (0.048; p=<0.001) | 0.161*** (0.048; p=<0.001) | 0.173*** (0.031; p=<0.001) | 0.166*** (0.031; p=<0.001) |
| White | 0.255*** (0.020; p=<0.001) | 0.240*** (0.020; p=<0.001) | 0.395*** (0.031; p=<0.001) | 0.366*** (0.031; p=<0.001) | 0.446*** (0.049; p=<0.001) | 0.413*** (0.048; p=<0.001) | 0.408*** (0.033; p=<0.001) | 0.378*** (0.033; p=<0.001) |
| Black - White | -0.095*** (0.028; p=<0.001) | -0.084*** (0.028; p=0.002) | -0.219*** (0.043; p=<0.001) | -0.199*** (0.043; p=<0.001) | -0.280*** (0.068; p=<0.001) | -0.252*** (0.068; p=<0.001) | -0.235*** (0.046; p=<0.001) | -0.212*** (0.045; p=<0.001) |
| N son-years: pooled per band ; Black / White per band | 25-34: 22,947 ; 35-44: 12,719 ; 45-55: 5,447 | 8,284 ; 14,675 ; 4,163 ; 8,557 ; 1,692 ; 3,755 |  |  |  |  |  |  |

Placebo for the many-cell specifications: if early cells were unrelated to wages, how much would the Gelbach accounting attribute to them mechanically (finite-sample over-fitting with many small cells, fewer son-years per cell after 35)?

| Placebo (labels permuted across sons within race, cell sizes kept; 10 draws) | pooled: part of the rise accounted for, mean [min, max] | its share, mean [min, max] | B-W: part of the change accounted for, mean [min, max] | its share, mean [min, max] |
|---|---|---|---|---|
| early cell (11 x 33) | 0.004 [-0.010, 0.015] | 0.033 [-0.076, 0.113] | -0.002 [-0.021, 0.023] | 0.014 [-0.165, 0.150] |
| early occupation (occ1990dd) | 0.004 [-0.006, 0.018] | 0.028 [-0.048, 0.131] | -0.000 [-0.015, 0.019] | 0.002 [-0.136, 0.105] |

## CP. Fast track inside high-paid, high-later-growth cells? (PSID)

Is the after-35 wage growth steeper for sons of richer parents WITHIN the data-defined high-paid / high-growth cells (Section D) than elsewhere? (1)-(3): son-level growth on centred ln parental income, early-set indicators and their interactions (controls as A1). (4)-(5): one son-year regression with person FE and year FE, where the piecewise age terms are interacted with ln parental income, the early-set indicators and the triple products; (4) shows the slope-after-35 terms, (5) the slope-before-35 terms (log points per 10 years per log point of parental income). (6): the pre-chosen illustrative industries instead of the data-defined sets.

| | (1) Delta ln wage (40-55) - (25-34) | (2) Delta ln wage (35-55) - (25-34) | (3) Delta ln wage (45-55) - (25-34) | (4) ln wage, person FE: slope 35-55 terms | (5) ... slope 25-35 terms | (6) illustrative: Delta (40-55) with finance / insurance / legal / professional |
|---|---|---|---|---|---|---|
| **Pooled (weighted)** | | | | | | |
| ln parental income (gradient in cells of neither set) | 0.043 (0.031; p=0.173) | 0.054** (0.023; p=0.019) | 0.053 (0.042; p=0.211) | 0.013 (0.021; p=0.537) | 0.093*** (0.032; p=0.003) | 0.091*** (0.024; p=<0.001) |
| ln parental income x early high-paid high-growth cell (extra gradient inside) | 0.103 (0.065; p=0.113) | 0.091* (0.050; p=0.070) | 0.084 (0.077; p=0.271) | 0.012 (0.050; p=0.808) | 0.179** (0.085; p=0.035) |  |
| gradient inside high-paid high-growth cells = sum of the two rows above | 0.146** (0.059; p=0.013) | 0.144*** (0.046; p=0.002) | 0.137** (0.064; p=0.032) | 0.025 (0.046; p=0.578) | 0.272*** (0.081; p=<0.001) |  |
| early high-paid high-growth cell | 0.160*** (0.049; p=0.001) | 0.155*** (0.038; p=<0.001) | 0.210*** (0.054; p=<0.001) | 0.055 (0.034; p=0.102) | 0.220*** (0.055; p=<0.001) |  |
| ln parental income x early high-paid-only cell | 0.112 (0.088; p=0.203) | 0.064 (0.061; p=0.295) | 0.206* (0.108; p=0.056) | 0.110 (0.092; p=0.235) | -0.042 (0.097; p=0.665) |  |
| early high-paid-only cell | 0.129** (0.061; p=0.034) | 0.159*** (0.048; p=<0.001) | 0.128* (0.069; p=0.064) | -0.043 (0.058; p=0.466) | 0.378*** (0.077; p=<0.001) |  |
| ln parental income x early high-growth-only cell | 0.006 (0.048; p=0.898) | 0.002 (0.043; p=0.960) | -0.030 (0.081; p=0.714) | -0.049 (0.055; p=0.373) | 0.074 (0.061; p=0.219) |  |
| early high-growth-only cell | 0.098*** (0.038; p=0.009) | 0.086*** (0.030; p=0.004) | 0.148*** (0.056; p=0.008) | 0.067* (0.038; p=0.076) | 0.098** (0.041; p=0.016) |  |
| illustrative: ln parental income x early finance / insurance / legal / professional |  |  |  |  |  | 0.008 (0.094; p=0.928) |
| illustrative: early finance / insurance / legal / professional |  |  |  |  |  | 0.188*** (0.072; p=0.009) |
| N sons / clusters (1)-(3), (6); son-years / sons (4)-(5) | 2,019 / 1,137 | 2,775 / 1,362 | 1,387 / 886 | 40,550 / 4,307 | 40,550 / 4,307 | 2,048 / 1,146 |
| Sons with an early high-paid high-growth cell (with Delta 40-55) | 514 (286) |  |  |  |  | FLP: 246 |
| **Black** | | | | | | |
| ln parental income (gradient in cells of neither set) | -0.023 (0.037; p=0.537) | 0.028 (0.027; p=0.300) | -0.047 (0.048; p=0.332) | -0.002 (0.029; p=0.951) | 0.007 (0.033; p=0.829) | -0.004 (0.031; p=0.895) |
| ln parental income x early high-paid high-growth cell (extra gradient inside) | 0.027 (0.087; p=0.754) | -0.003 (0.064; p=0.962) | 0.027 (0.120; p=0.823) | -0.087 (0.074; p=0.245) | 0.118 (0.092; p=0.199) |  |
| gradient inside high-paid high-growth cells = sum of the two rows above | 0.004 (0.077; p=0.957) | 0.025 (0.057; p=0.667) | -0.020 (0.106; p=0.850) | -0.088 (0.066; p=0.180) | 0.125 (0.087; p=0.149) |  |
| early high-paid high-growth cell | 0.067 (0.060; p=0.266) | 0.083** (0.042; p=0.048) | 0.113 (0.073; p=0.124) | 0.010 (0.052; p=0.852) | 0.166** (0.067; p=0.013) |  |
| ln parental income x early high-paid-only cell | 0.077 (0.203; p=0.704) | -0.008 (0.084; p=0.927) | 0.421** (0.177; p=0.017) | 0.313*** (0.119; p=0.009) | -0.192 (0.203; p=0.345) |  |
| early high-paid-only cell | 0.130 (0.111; p=0.243) | 0.062 (0.066; p=0.348) | 0.239* (0.126; p=0.057) | 0.018 (0.075; p=0.805) | 0.290*** (0.097; p=0.003) |  |
| ln parental income x early high-growth-only cell | 0.063 (0.072; p=0.376) | 0.010 (0.058; p=0.861) | 0.014 (0.116; p=0.906) | 0.002 (0.091; p=0.980) | 0.009 (0.101; p=0.932) |  |
| early high-growth-only cell | 0.045 (0.066; p=0.497) | 0.035 (0.043; p=0.417) | 0.021 (0.094; p=0.826) | -0.039 (0.068; p=0.566) | 0.051 (0.059; p=0.392) |  |
| illustrative: ln parental income x early finance / insurance / legal / professional |  |  |  |  |  | -0.029 (0.234; p=0.902) |
| illustrative: early finance / insurance / legal / professional |  |  |  |  |  | 0.218** (0.103; p=0.035) |
| N sons / clusters (1)-(3), (6); son-years / sons (4)-(5) | 670 / 368 | 994 / 463 | 439 / 270 | 13,791 / 1,724 | 13,791 / 1,724 | 688 / 374 |
| Sons with an early high-paid high-growth cell (with Delta 40-55) | 98 (46) |  |  |  |  | FLP: 58 |
| **White** | | | | | | |
| ln parental income (gradient in cells of neither set) | 0.069* (0.036; p=0.057) | 0.052** (0.025; p=0.037) | 0.089* (0.049; p=0.070) | 0.032 (0.027; p=0.238) | 0.095*** (0.035; p=0.006) | 0.112*** (0.029; p=<0.001) |
| ln parental income x early high-paid high-growth cell (extra gradient inside) | 0.046 (0.067; p=0.487) | 0.057 (0.052; p=0.272) | 0.061 (0.092; p=0.505) | 0.018 (0.060; p=0.760) | 0.120 (0.096; p=0.208) |  |
| gradient inside high-paid high-growth cells = sum of the two rows above | 0.115** (0.058; p=0.047) | 0.109** (0.047; p=0.020) | 0.150* (0.077; p=0.052) | 0.050 (0.054; p=0.351) | 0.216** (0.090; p=0.017) |  |
| early high-paid high-growth cell | 0.210*** (0.049; p=<0.001) | 0.192*** (0.038; p=<0.001) | 0.229*** (0.063; p=<0.001) | 0.053 (0.038; p=0.160) | 0.276*** (0.058; p=<0.001) |  |
| ln parental income x early high-paid-only cell | 0.104 (0.089; p=0.240) | 0.059 (0.057; p=0.300) | 0.145 (0.124; p=0.243) | 0.005 (0.085; p=0.949) | 0.072 (0.090; p=0.423) |  |
| early high-paid-only cell | 0.128** (0.061; p=0.038) | 0.159*** (0.046; p=<0.001) | 0.172** (0.082; p=0.035) | 0.029 (0.055; p=0.599) | 0.290*** (0.073; p=<0.001) |  |
| ln parental income x early high-growth-only cell | 0.012 (0.065; p=0.857) | 0.009 (0.055; p=0.869) | -0.092 (0.093; p=0.326) | -0.037 (0.061; p=0.541) | 0.091 (0.074; p=0.220) |  |
| early high-growth-only cell | 0.101** (0.042; p=0.017) | 0.087*** (0.032; p=0.007) | 0.192*** (0.060; p=0.001) | 0.083** (0.041; p=0.044) | 0.100** (0.047; p=0.032) |  |
| illustrative: ln parental income x early finance / insurance / legal / professional |  |  |  |  |  | 0.053 (0.087; p=0.540) |
| illustrative: early finance / insurance / legal / professional |  |  |  |  |  | 0.154** (0.068; p=0.022) |
| N sons / clusters (1)-(3), (6); son-years / sons (4)-(5) | 1,349 / 770 | 1,782 / 903 | 948 / 617 | 26,772 / 2,586 | 26,772 / 2,586 | 1,360 / 773 |
| Sons with an early high-paid high-growth cell (with Delta 40-55) | 416 (240) |  |  |  |  | FLP: 188 |
| **Black - White** | | | | | | |
| ln parental income (gradient in cells of neither set) | -0.092* (0.052; p=0.077) | -0.024 (0.037; p=0.503) | -0.136** (0.069; p=0.049) | -0.034 (0.040; p=0.397) | -0.088* (0.048; p=0.067) | -0.116*** (0.042; p=0.006) |
| ln parental income x early high-paid high-growth cell (extra gradient inside) | -0.019 (0.109; p=0.861) | -0.060 (0.082; p=0.465) | -0.035 (0.151; p=0.818) | -0.105 (0.096; p=0.273) | -0.002 (0.133; p=0.986) |  |
| gradient inside high-paid high-growth cells = sum of the two rows above | -0.111 (0.096; p=0.249) | -0.085 (0.074; p=0.254) | -0.170 (0.132; p=0.196) | -0.139 (0.085; p=0.103) | -0.090 (0.125; p=0.471) |  |
| early high-paid high-growth cell | -0.143* (0.078; p=0.066) | -0.109* (0.057; p=0.056) | -0.116 (0.097; p=0.230) | -0.043 (0.064; p=0.506) | -0.109 (0.089; p=0.217) |  |
| ln parental income x early high-paid-only cell | -0.027 (0.222; p=0.901) | -0.067 (0.102; p=0.510) | 0.276 (0.216; p=0.201) | 0.307** (0.146; p=0.035) | -0.264 (0.222; p=0.235) |  |
| early high-paid-only cell | 0.003 (0.127; p=0.984) | -0.097 (0.081; p=0.230) | 0.067 (0.150; p=0.656) | -0.011 (0.093; p=0.909) | 0.000 (0.121; p=0.999) |  |
| ln parental income x early high-growth-only cell | 0.052 (0.097; p=0.593) | 0.001 (0.080; p=0.990) | 0.105 (0.149; p=0.479) | 0.040 (0.109; p=0.718) | -0.082 (0.125; p=0.512) |  |
| early high-growth-only cell | -0.056 (0.079; p=0.476) | -0.052 (0.054; p=0.335) | -0.172 (0.112; p=0.125) | -0.122 (0.080; p=0.125) | -0.050 (0.076; p=0.512) |  |
| illustrative: ln parental income x early finance / insurance / legal / professional |  |  |  |  |  | -0.082 (0.249; p=0.742) |
| illustrative: early finance / insurance / legal / professional |  |  |  |  |  | 0.064 (0.123; p=0.605) |

## D. Data-defined groups: high-paid and high-later-growth occupation x industry cells (PSID)

All 11 x 33 occupation group x industry group cells observed in CPS MORG 1992-2002 (men 25-64) are ranked by their nonlinear band profile: LEVEL = age-weighted relative wage, LATER GROWTH = band growth from 35-39 to 50-54 (both relative to men of the same age). 'High-paid' = top quartile of men's employment by level (level >= 0.219); 'high later growth' = top quartile by later growth (>= -0.015); the headline group is their intersection. Employment shares: high-paid AND high later growth 0.159; high-paid only 0.121; high later growth only 0.091; neither 0.629. The same ranking on the 33 industry groups (industry sets) is a secondary grouping. Of men in the finance / insurance / legal / professional industries (the PI's examples), 0.23 are in 'high-paid AND high later growth'; 0.56 are in 'high-paid only'; 0.12 are in 'high later growth only'; 0.09 are in 'neither'.

### D0. Cells in the 'high-paid AND high later growth' set (all, by employment)

| Cell (occupation group x industry group) | level (age-weighted Q) | band growth (25-29)->(35-39) | band growth (35-39)->(50-54) | MORG men | employment share | own profile | PSID sons (early cell) | share Black among them |
|---|---|---|---|---|---|---|---|---|
| Professional specialty x Education | 0.219 | 0.079 | 0.156 | 25,339 | 0.0317 | yes | 118 | 0.27 |
| Managerial & management related x Public administration (incl. postal) | 0.298 | -0.004 | 0.050 | 11,009 | 0.0137 | yes | 22 | 0.36 |
| Professional specialty x Professional services (engineering, accounting, research, consulting) (FLP) | 0.471 | 0.019 | 0.015 | 7,893 | 0.0105 | yes | 36 | 0.03 |
| Professional specialty x Public administration (incl. postal) | 0.389 | 0.085 | 0.023 | 8,132 | 0.0103 | yes | 28 | 0.29 |
| Professional specialty x Hospitals | 0.334 | 0.200 | 0.071 | 6,381 | 0.0084 | yes | 35 | 0.11 |
| Managerial & management related x Education | 0.286 | 0.130 | 0.117 | 5,676 | 0.0069 | yes | 11 | 0.36 |
| Managerial & management related x Wholesale trade | 0.276 | 0.026 | 0.013 | 4,411 | 0.0059 | yes | 23 | 0.04 |
| Managerial & management related x Retail trade (excl. eating, drinking) | 0.225 | 0.078 | -0.002 | 4,313 | 0.0058 | yes | 63 | 0.27 |
| Professional specialty x Mfg: motor vehicles, aircraft, other transport eq. | 0.526 | 0.030 | 0.004 | 3,977 | 0.0057 | yes | 19 | 0.21 |
| Managerial & management related x Other business services | 0.271 | 0.130 | 0.008 | 3,920 | 0.0055 | yes | 19 | 0.16 |
| Managerial & management related x Mfg: chemicals, petroleum, rubber, plastics | 0.480 | 0.196 | 0.040 | 3,339 | 0.0044 | yes | 7 | 0.14 |
| Professional specialty x Communications | 0.369 | -0.016 | 0.019 | 2,760 | 0.0038 | yes | 13 | 0.15 |
| Managerial & management related x Mfg: paper, printing, publishing | 0.384 | 0.055 | 0.048 | 2,698 | 0.0036 | yes | 6 | 0.17 |
| Managerial & management related x Mfg: electrical equipment | 0.535 | 0.161 | -0.014 | 2,502 | 0.0036 | yes | 3 | 0.33 |
| Professional specialty x Mfg: chemicals, petroleum, rubber, plastics | 0.543 | -0.027 | 0.017 | 2,692 | 0.0036 | yes | 10 | 0.10 |
| Managerial & management related x Utilities and sanitary services | 0.377 | -0.020 | 0.077 | 2,475 | 0.0031 | yes | 2 | 0.50 |
| Managerial & management related x Mfg: primary and fabricated metals | 0.359 | 0.011 | 0.057 | 2,121 | 0.0029 | yes | 7 | 0.00 |
| Professional specialty x Mfg: paper, printing, publishing | 0.275 | 0.041 | 0.027 | 2,147 | 0.0028 | yes | 15 | 0.00 |
| Managerial & management related x Insurance (FLP) | 0.534 | 0.185 | 0.008 | 2,009 | 0.0027 | yes | 8 | 0.25 |
| Managerial & management related x Mfg: instruments, misc. manufacturing | 0.476 | 0.144 | 0.021 | 1,878 | 0.0026 | yes | 4 | 0.00 |
| Professional specialty x Retail trade (excl. eating, drinking) | 0.376 | -0.120 | 0.013 | 1,914 | 0.0025 | yes | 6 | 0.17 |
| Managerial & management related x Hospitals | 0.389 | 0.020 | -0.003 | 1,985 | 0.0025 | yes | 4 | 0.00 |
| Technicians x Transportation (excl. postal) | 0.429 | 0.302 | 0.096 | 1,900 | 0.0025 | yes | 8 | 0.00 |
| Managerial & management related x Mfg: food, tobacco | 0.349 | 0.087 | 0.022 | 1,835 | 0.0024 | yes | 7 | 0.00 |
| Professional specialty x Construction | 0.427 | -0.029 | 0.078 | 1,768 | 0.0023 | yes | 6 | 0.00 |
| Managerial & management related x Mfg: wood, furniture, stone, glass | 0.266 | -0.002 | 0.035 | 1,728 | 0.0023 | yes | 4 | 0.25 |
| Professional specialty x Insurance (FLP) | 0.533 | -0.040 | -0.011 | 984 | 0.0013 | yes | 2 | 0.00 |
| Technicians x Mfg: motor vehicles, aircraft, other transport eq. | 0.269 | -0.072 | 0.099 | 920 | 0.0013 | yes | 10 | 0.40 |
| Managerial & management related x Mfg: textiles, apparel, leather | 0.395 | 0.166 | 0.008 | 965 | 0.0013 | yes | 0 |  |
| Professional specialty x Transportation (excl. postal) | 0.326 | -0.170 | 0.057 | 800 | 0.0012 | yes | 4 | 0.25 |
| Professional specialty x Agriculture, forestry, fishing | 0.235 | -0.084 | 0.249 | 707 | 0.0007 | yes | 10 | 0.00 |
| Technicians x Insurance (FLP) | 0.368 | -0.033 | -0.003 | 458 | 0.0006 | yes | 2 | 0.00 |
| Professional specialty x Mfg: food, tobacco | 0.408 | -0.003 | 0.046 | 443 | 0.0006 | yes | 2 | 0.00 |

### D0b. Largest cells that are high-paid only (top 15 by employment)

| Cell (occupation group x industry group) | level (age-weighted Q) | band growth (25-29)->(35-39) | band growth (35-39)->(50-54) | MORG men | employment share | own profile | PSID sons (early cell) | share Black among them |
|---|---|---|---|---|---|---|---|---|
| Managerial & management related x Finance: banking, credit, securities (FLP) | 0.485 | 0.112 | -0.025 | 8,766 | 0.0114 | yes | 41 | 0.29 |
| Managerial & management related x Construction | 0.275 | -0.007 | -0.073 | 7,187 | 0.0096 | yes | 45 | 0.04 |
| Managerial & management related x Professional services (engineering, accounting, research, consulting) (FLP) | 0.520 | 0.113 | -0.034 | 5,859 | 0.0079 | yes | 27 | 0.11 |
| Professional specialty x Computer and data processing services | 0.540 | -0.026 | -0.081 | 4,911 | 0.0075 | yes | 28 | 0.11 |
| Sales x Insurance (FLP) | 0.316 | 0.093 | -0.109 | 4,327 | 0.0058 | yes | 17 | 0.18 |
| Professional specialty x Other health services | 0.471 | 0.193 | -0.070 | 4,064 | 0.0054 | yes | 23 | 0.26 |
| Managerial & management related x Transportation (excl. postal) | 0.266 | 0.005 | -0.015 | 3,976 | 0.0053 | yes | 12 | 0.17 |
| Professional specialty x Mfg: electrical equipment | 0.525 | -0.017 | -0.072 | 3,443 | 0.0050 | yes | 12 | 0.00 |
| Sales x Finance: banking, credit, securities (FLP) | 0.509 | 0.053 | -0.108 | 3,484 | 0.0048 | yes | 11 | 0.27 |
| Managerial & management related x Mfg: machinery and computers | 0.472 | 0.076 | -0.032 | 3,401 | 0.0047 | yes | 4 | 0.00 |
| Professional specialty x Mfg: machinery and computers | 0.479 | 0.029 | -0.105 | 3,195 | 0.0045 | yes | 13 | 0.00 |
| Professional specialty x Legal services (FLP) | 0.652 | 0.109 | -0.057 | 3,284 | 0.0043 | yes | 14 | 0.07 |
| Managerial & management related x Computer and data processing services | 0.580 | 0.101 | -0.063 | 2,602 | 0.0039 | yes | 9 | 0.11 |
| Managerial & management related x Communications | 0.498 | 0.195 | -0.137 | 2,739 | 0.0038 | yes | 12 | 0.25 |
| Managerial & management related x Mfg: motor vehicles, aircraft, other transport eq. | 0.480 | 0.073 | -0.058 | 2,461 | 0.0035 | yes | 3 | 0.00 |

### D0c. Largest cells with high later growth only (top 15)

| Cell (occupation group x industry group) | level (age-weighted Q) | band growth (25-29)->(35-39) | band growth (35-39)->(50-54) | MORG men | employment share | own profile | PSID sons (early cell) | share Black among them |
|---|---|---|---|---|---|---|---|---|
| Craft & repair x Mfg: wood, furniture, stone, glass | -0.135 | -0.083 | -0.002 | 4,803 | 0.0065 | yes | 27 | 0.37 |
| Craft & repair x Mfg: chemicals, petroleum, rubber, plastics | 0.069 | -0.018 | -0.003 | 4,609 | 0.0063 | yes | 17 | 0.24 |
| Craft & repair x Communications | 0.116 | -0.077 | 0.048 | 4,502 | 0.0061 | yes | 21 | 0.38 |
| Administrative support x Transportation (excl. postal) | -0.078 | -0.086 | 0.020 | 4,132 | 0.0057 | yes | 26 | 0.58 |
| Craft & repair x Mfg: food, tobacco | -0.153 | -0.034 | 0.023 | 4,215 | 0.0056 | yes | 20 | 0.45 |
| Managerial & management related x Personal services, entertainment | 0.130 | 0.036 | -0.012 | 3,032 | 0.0041 | yes | 23 | 0.22 |
| Managerial & management related x Social services, religious, membership | 0.199 | 0.123 | 0.060 | 3,168 | 0.0040 | yes | 6 | 0.33 |
| Technicians x Professional services (engineering, accounting, research, consulting) (FLP) | 0.144 | -0.014 | 0.053 | 2,604 | 0.0034 | yes | 14 | 0.21 |
| Administrative support x Finance: banking, credit, securities (FLP) | -0.058 | -0.028 | 0.014 | 2,475 | 0.0034 | yes | 20 | 0.45 |
| Administrative support x Wholesale trade | -0.214 | -0.149 | 0.005 | 2,372 | 0.0033 | yes | 16 | 0.62 |
| Craft & repair x Mfg: electrical equipment | 0.059 | -0.125 | -0.003 | 2,319 | 0.0031 | yes | 10 | 0.20 |
| Technicians x Hospitals | 0.050 | -0.022 | 0.023 | 2,237 | 0.0030 | yes | 18 | 0.39 |
| Administrative support x Education | -0.248 | -0.001 | 0.076 | 1,671 | 0.0022 | yes | 20 | 0.50 |
| Transport & material moving x Utilities and sanitary services | -0.132 | -0.122 | 0.001 | 1,564 | 0.0021 | yes | 3 | 0.33 |
| Administrative support x Utilities and sanitary services | 0.028 | -0.105 | 0.031 | 1,461 | 0.0019 | yes | 6 | 0.33 |

### D0d. Industry-group sets (same ranking on 33 industry groups)

| Industry-group set | industries |
|---|---|
| high-paid AND high later growth | Professional services (engineering, accounting, research, consulting); Public administration (incl. postal); Utilities and sanitary services |
| high-paid only | Mfg: electrical equipment; Communications; Mfg: motor vehicles, aircraft, other transport eq.; Insurance; Finance: banking, credit, securities; Computer and data processing services; Legal services |
| high later growth only | Education; Social services, religious, membership; Mfg: wood, furniture, stone, glass; Mfg: chemicals, petroleum, rubber, plastics; Mfg: textiles, apparel, leather |

### D1. Shares of sons by early cell set, race and parental-income tercile (unweighted; pooled terciles)

| Race | parental-income tercile | sons with an early cell | high-paid AND high later growth | high-paid only | high later growth only | neither | illustrative: early FLP industry |
|---|---|---|---|---|---|---|---|
| Black + White | all | 4,310 | 0.119 | 0.089 | 0.082 | 0.710 | 0.057 |
| Black + White | 1 | 1,357 | 0.047 | 0.024 | 0.077 | 0.852 | 0.024 |
| Black + White | 2 | 1,457 | 0.102 | 0.061 | 0.094 | 0.743 | 0.047 |
| Black + White | 3 | 1,496 | 0.202 | 0.174 | 0.076 | 0.548 | 0.096 |
| Black | all | 1,724 | 0.057 | 0.032 | 0.087 | 0.824 | 0.033 |
| Black | 1 | 970 | 0.036 | 0.025 | 0.073 | 0.866 | 0.022 |
| Black | 2 | 529 | 0.059 | 0.036 | 0.104 | 0.802 | 0.043 |
| Black | 3 | 225 | 0.142 | 0.058 | 0.107 | 0.693 | 0.058 |
| White | all | 2,586 | 0.161 | 0.126 | 0.079 | 0.634 | 0.073 |
| White | 1 | 387 | 0.075 | 0.021 | 0.088 | 0.817 | 0.028 |
| White | 2 | 928 | 0.126 | 0.075 | 0.088 | 0.710 | 0.050 |
| White | 3 | 1,271 | 0.212 | 0.195 | 0.070 | 0.522 | 0.103 |

Mean growth by early cell set (descriptive):

| Early cell set | sons | sons observed at 40-55 | mean Delta(40-55) | mean ln wage 25-34 | mean ln parental income | Black share |
|---|---|---|---|---|---|---|
| high-paid AND high later growth | 514 | 286 | 0.451 | 2.808 | 11.151 | 0.191 |
| high-paid only | 382 | 215 | 0.433 | 2.982 | 11.246 | 0.147 |
| high later growth only | 355 | 166 | 0.290 | 2.587 | 10.743 | 0.423 |
| neither | 3,059 | 1,352 | 0.219 | 2.420 | 10.640 | 0.464 |

### D3. Access to high-paid cells at 25-34: does the racial gap survive parental income and the father's job?

Son-level linear probability models; outcome (column header) = the son's early cell (modal at 25-34) is in the data-defined 'high-paid AND high later growth' set (1)-(5) or in any high-paid cell (6)-(10). Regressors: (a) ln parental income; (b) White; (c) both; (d) race x pooled parental-income tercile cells (reference Black tercile 1; in the race samples tercile indicators); (e) (c) + the father's cell (modal at son ages 12-18) in the high-paid high-growth set + years of education (sons with a father's cell). Controls: birth-year quadratic. Pooled weighted, by race unweighted; clusters 1968 family. Descriptive: education is itself an outcome of parental resources, so (e) splits the gap into a part running through education and the father's job and the rest.

| | (1) early cell high-paid AND high later growth: (a) | (2) early cell high-paid AND high later growth: (b) | (3) early cell high-paid AND high later growth: (c) | (4) early cell high-paid AND high later growth: (d) | (5) early cell high-paid AND high later growth: (e) | (6) early cell high-paid (any): (a) | (7) early cell high-paid (any): (b) | (8) early cell high-paid (any): (c) | (9) early cell high-paid (any): (d) | (10) early cell high-paid (any): (e) |
|---|---|---|---|---|---|---|---|---|---|---|
| **Pooled (weighted)** | | | | | | | | | | |
| ln parental income | 0.104*** (0.010; p=<0.001) |  | 0.095*** (0.011; p=<0.001) |  | 0.002 (0.016; p=0.920) | 0.209*** (0.013; p=<0.001) |  | 0.192*** (0.014; p=<0.001) |  | 0.061*** (0.019; p=0.002) |
| White |  | 0.109*** (0.014; p=<0.001) | 0.042*** (0.016; p=0.009) |  | 0.035* (0.020; p=0.083) |  | 0.212*** (0.020; p=<0.001) | 0.078*** (0.022; p=<0.001) |  | 0.106*** (0.023; p=<0.001) |
| Black, tercile 2 (ref. Black tercile 1) |  |  |  | 0.024 (0.022; p=0.285) |  |  |  |  | 0.047* (0.024; p=0.051) |  |
| Black, tercile 3 |  |  |  | 0.125*** (0.044; p=0.005) |  |  |  |  | 0.113** (0.046; p=0.014) |  |
| White, tercile 1 |  |  |  | 0.048** (0.020; p=0.018) |  |  |  |  | 0.041* (0.024; p=0.088) |  |
| White, tercile 2 |  |  |  | 0.092*** (0.017; p=<0.001) |  |  |  |  | 0.151*** (0.022; p=<0.001) |  |
| White, tercile 3 |  |  |  | 0.187*** (0.017; p=<0.001) |  |  |  |  | 0.360*** (0.023; p=<0.001) |  |
| father in a high-paid high-growth cell |  |  |  |  | 0.064** (0.025; p=0.012) |  |  |  |  | 0.060** (0.025; p=0.017) |
| years of education |  |  |  |  | 0.063*** (0.005; p=<0.001) |  |  |  |  | 0.099*** (0.005; p=<0.001) |
| contrast: White tercile 3 - Black tercile 3 |  |  |  | 0.062 (0.045; p=0.171) |  |  |  |  | 0.247*** (0.047; p=<0.001) |  |
| Mean of outcome | 0.156 | 0.156 | 0.156 | 0.156 | 0.174 | 0.278 | 0.278 | 0.278 | 0.278 | 0.309 |
| N sons / clusters | 4,307 / 1,686 | 4,307 / 1,686 | 4,307 / 1,686 | 4,307 / 1,686 | 3,027 / 1,357 | 4,307 / 1,686 | 4,307 / 1,686 | 4,307 / 1,686 | 4,307 / 1,686 | 3,027 / 1,357 |
| **Black** | | | | | | | | | | |
| ln parental income | 0.048*** (0.009; p=<0.001) |  | 0.048*** (0.009; p=<0.001) |  | 0.021 (0.018; p=0.233) | 0.067*** (0.011; p=<0.001) |  | 0.067*** (0.011; p=<0.001) |  | 0.042** (0.019; p=0.026) |
| tercile 2 (within-race samples; ref. tercile 1) |  |  |  | 0.022* (0.013; p=0.089) |  |  |  |  | 0.032** (0.016; p=0.042) |  |
| tercile 3 (within-race samples) |  |  |  | 0.104*** (0.025; p=<0.001) |  |  |  |  | 0.134*** (0.029; p=<0.001) |  |
| father in a high-paid high-growth cell |  |  |  |  | 0.008 (0.051; p=0.871) |  |  |  |  | 0.007 (0.056; p=0.907) |
| years of education |  |  |  |  | 0.052*** (0.007; p=<0.001) |  |  |  |  | 0.070*** (0.007; p=<0.001) |
| Mean of outcome | 0.057 |  | 0.057 | 0.057 | 0.074 | 0.089 |  | 0.089 | 0.089 | 0.104 |
| N sons / clusters | 1,724 / 615 |  | 1,724 / 615 | 1,724 / 615 | 838 / 394 | 1,724 / 615 |  | 1,724 / 615 | 1,724 / 615 | 838 / 394 |
| **White** | | | | | | | | | | |
| ln parental income | 0.103*** (0.012; p=<0.001) |  | 0.103*** (0.012; p=<0.001) |  | -0.001 (0.016; p=0.934) | 0.223*** (0.016; p=<0.001) |  | 0.223*** (0.016; p=<0.001) |  | 0.068*** (0.019; p=<0.001) |
| tercile 2 (within-race samples; ref. tercile 1) |  |  |  | 0.050*** (0.018; p=0.006) |  |  |  |  | 0.105*** (0.021; p=<0.001) |  |
| tercile 3 (within-race samples) |  |  |  | 0.138*** (0.019; p=<0.001) |  |  |  |  | 0.313*** (0.023; p=<0.001) |  |
| father in a high-paid high-growth cell |  |  |  |  | 0.048** (0.023; p=0.037) |  |  |  |  | 0.053** (0.024; p=0.028) |
| years of education |  |  |  |  | 0.064*** (0.005; p=<0.001) |  |  |  |  | 0.101*** (0.005; p=<0.001) |
| Mean of outcome | 0.161 |  | 0.161 | 0.161 | 0.170 | 0.287 |  | 0.287 | 0.287 | 0.305 |
| N sons / clusters | 2,586 / 1,078 |  | 2,586 / 1,078 | 2,586 / 1,078 | 2,192 / 967 | 2,586 / 1,078 |  | 2,586 / 1,078 | 2,586 / 1,078 | 2,192 / 967 |
| **Black - White** | | | | | | | | | | |
| ln parental income | -0.055*** (0.015; p=<0.001) |  | -0.055*** (0.015; p=<0.001) |  | 0.022 (0.024; p=0.344) | -0.156*** (0.019; p=<0.001) |  | -0.156*** (0.019; p=<0.001) |  | -0.026 (0.027; p=0.338) |
| tercile 2 (within-race samples; ref. tercile 1) |  |  |  | -0.028 (0.022; p=0.201) |  |  |  |  | -0.073*** (0.026; p=0.005) |  |
| tercile 3 (within-race samples) |  |  |  | -0.034 (0.031; p=0.269) |  |  |  |  | -0.180*** (0.037; p=<0.001) |  |
| father in a high-paid high-growth cell |  |  |  |  | -0.040 (0.056; p=0.469) |  |  |  |  | -0.046 (0.061; p=0.447) |
| years of education |  |  |  |  | -0.012 (0.008; p=0.135) |  |  |  |  | -0.030*** (0.009; p=<0.001) |


### D2. Illustrative pre-named cells (PSID; small cells, no headline)

Cells defined in the docstring (occ1990dd x industry group); the son's early cell = modal cell over his 25-34 son-years with both codes. Shares by race and parental-income tercile (pooled terciles, unweighted):

| Race | parental-income tercile | sons with an early cell | lawyers in legal services | managers / financial specialists in finance / insurance | managers / professionals in professional services | any of (1)-(3) | managers / professionals elsewhere |
|---|---|---|---|---|---|---|---|
| Black + White | all | 4,310 | 0.003 | 0.012 | 0.013 | 0.027 | 0.183 |
| Black + White | 1 | 1,357 | 0.000 | 0.003 | 0.002 | 0.005 | 0.079 |
| Black + White | 2 | 1,457 | 0.000 | 0.007 | 0.010 | 0.016 | 0.139 |
| Black + White | 3 | 1,496 | 0.008 | 0.024 | 0.025 | 0.057 | 0.319 |
| Black | all | 1,724 | 0.001 | 0.007 | 0.002 | 0.010 | 0.089 |
| Black | 1 | 970 | 0.000 | 0.003 | 0.002 | 0.005 | 0.061 |
| Black | 2 | 529 | 0.000 | 0.006 | 0.004 | 0.009 | 0.091 |
| Black | 3 | 225 | 0.004 | 0.027 | 0.000 | 0.031 | 0.209 |
| White | all | 2,586 | 0.004 | 0.015 | 0.019 | 0.038 | 0.245 |
| White | 1 | 387 | 0.000 | 0.003 | 0.003 | 0.005 | 0.124 |
| White | 2 | 928 | 0.000 | 0.008 | 0.013 | 0.020 | 0.167 |
| White | 3 | 1,271 | 0.009 | 0.024 | 0.029 | 0.061 | 0.338 |

Mean growth and MORG band profiles by early cell (MORG: CPS men 25-64 in the same cell, wage relative to men of the same age):

| Early cell | sons | sons observed at 40-55 | mean Delta(40-55) | mean ln wage 25-34 | Black share | MORG Q 25-29 | MORG Q 35-39 | MORG Q 50-54 | MORG band growth (35-39)->(50-54) | MORG men |
|---|---|---|---|---|---|---|---|---|---|---|
| lawyers in legal services | 12 | 4 | 0.923 | 3.153 | 0.083 | 0.567 | 0.684 | 0.621 | -0.063 | 3,227 |
| managers / financial specialists in finance / insurance | 50 | 26 | 0.498 | 3.042 | 0.240 | 0.451 | 0.556 | 0.521 | -0.035 | 13,572 |
| managers / professionals in professional services | 54 | 28 | 0.511 | 3.047 | 0.074 | 0.446 | 0.504 | 0.500 | -0.003 | 13,752 |
| managers / professionals elsewhere | 787 | 432 | 0.420 | 2.809 | 0.196 | 0.253 | 0.332 | 0.339 | 0.007 | 186,911 |
| all other | 3,407 | 1,529 | 0.232 | 2.448 | 0.456 | -0.088 | -0.142 | -0.183 | -0.041 | 526,521 |

Son-level regressions on early-cell indicators (reference = all other occupations / industries); controls as A1. The contribution of the early cells to the divergence is the 'early occupation x industry cell' row of Table A2.

| | (1) Delta ln wage (40-55) - (25-34) | (2) ... + ln parental income | (3) ... special cells (1)-(3) x ln parental income |
|---|---|---|---|
| **Pooled (weighted)** | | | |
| early lawyers in legal services | 0.716*** (0.208; p=<0.001) | 0.677*** (0.211; p=0.001) |  |
| early managers / financial specialists in finance / insurance | 0.263** (0.116; p=0.023) | 0.225* (0.116; p=0.053) |  |
| early managers / professionals in professional services | 0.257** (0.118; p=0.030) | 0.224* (0.118; p=0.059) |  |
| early managers / professionals elsewhere | 0.171*** (0.032; p=<0.001) | 0.148*** (0.032; p=<0.001) |  |
| early any of cells (1)-(3) |  |  | 0.192 (0.131; p=0.144) |
| ln parental income |  | 0.069*** (0.025; p=0.005) | 0.095*** (0.024; p=<0.001) |
| ln parental income x cells (1)-(3) |  |  | 0.032 (0.164; p=0.844) |
| N sons / clusters | 2,019 / 1,137 | 2,019 / 1,137 | 2,019 / 1,137 |
| **Black** | | | |
| early lawyers in legal services |  |  |  |
| early managers / financial specialists in finance / insurance | 0.039 (0.112; p=0.725) | 0.047 (0.113; p=0.677) |  |
| early managers / professionals in professional services |  |  |  |
| early managers / professionals elsewhere | 0.098 (0.063; p=0.119) | 0.100 (0.063; p=0.109) |  |
| early any of cells (1)-(3) |  |  | 0.085 (0.131; p=0.516) |
| ln parental income |  | -0.010 (0.031; p=0.737) | -0.004 (0.031; p=0.891) |
| ln parental income x cells (1)-(3) |  |  | -0.152 (0.119; p=0.202) |
| N sons / clusters | 670 / 368 | 670 / 368 | 670 / 368 |
| **White** | | | |
| early lawyers in legal services | 0.667*** (0.242; p=0.006) | 0.625** (0.249; p=0.012) |  |
| early managers / financial specialists in finance / insurance | 0.284** (0.118; p=0.016) | 0.244** (0.117; p=0.037) |  |
| early managers / professionals in professional services | 0.258*** (0.100; p=0.010) | 0.226** (0.100; p=0.023) |  |
| early managers / professionals elsewhere | 0.184*** (0.031; p=<0.001) | 0.160*** (0.032; p=<0.001) |  |
| early any of cells (1)-(3) |  |  | 0.185 (0.117; p=0.114) |
| ln parental income |  | 0.092*** (0.028; p=0.001) | 0.121*** (0.028; p=<0.001) |
| ln parental income x cells (1)-(3) |  |  | 0.037 (0.155; p=0.809) |
| N sons / clusters | 1,349 / 770 | 1,349 / 770 | 1,349 / 770 |
| **Black - White** | | | |
| early lawyers in legal services |  |  |  |
| early managers / financial specialists in finance / insurance | -0.244 (0.163; p=0.133) | -0.197 (0.163; p=0.226) |  |
| early managers / professionals in professional services |  |  |  |
| early managers / professionals elsewhere | -0.086 (0.070; p=0.217) | -0.059 (0.070; p=0.397) |  |
| early any of cells (1)-(3) |  |  | -0.100 (0.176; p=0.570) |
| ln parental income |  | -0.102** (0.042; p=0.015) | -0.126*** (0.042; p=0.003) |
| ln parental income x cells (1)-(3) |  |  | -0.189 (0.195; p=0.332) |

## F. Following the father at the occupation x industry cell level (PSID)

Father = male head of the son's family at 16 (24's fpid); his cell = modal occupation group (11) x industry group (33) over his head-waves with the son aged 12-18 (32 Section 4 for his industry and occupation separately). Sons with a father's cell: Black 961, White 2,322; 240 distinct father cells. **Coding drift:** fathers are coded almost only in 1970 Census codes, while 44.7% of the sons' following son-years are coded in 2000 / 2010 codes (waves 2003+); both are bridged to occ1990dd / ind1990ddx, but a cell match requires both codes to agree, so some measured non-following is coding drift (more than for industry or occupation alone). The PSID has no employer identifiers.

### F1. How often do sons work in the father's cell?

Unweighted share of son-years; benchmark = random matching of sons to fathers within race x parental-income tercile (sum_j p_son(j) p_father(j)); ratio = observed / benchmark.

| Race | sons' ages | father's cell (occupation group x industry group): observed | benchmark | ratio | father's industry group (33; as 32): observed | benchmark | ratio | father's occupation group (11; as 32): observed | benchmark | ratio | son-years / sons (cell) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Black + White | 25-34 | 0.066 | 0.016 | 4.05 | 0.136 | 0.051 | 2.65 | 0.204 | 0.141 | 1.44 | 15,658 / 3,031 |
| Black + White | 35-55 | 0.057 | 0.016 | 3.55 | 0.132 | 0.052 | 2.56 | 0.208 | 0.150 | 1.38 | 13,836 / 2,167 |
| Black | 25-34 | 0.058 | 0.017 | 3.42 | 0.107 | 0.053 | 2.03 | 0.160 | 0.121 | 1.32 | 3,773 / 838 |
| Black | 35-55 | 0.053 | 0.019 | 2.79 | 0.101 | 0.054 | 1.87 | 0.153 | 0.117 | 1.31 | 3,171 / 568 |
| White | 25-34 | 0.068 | 0.016 | 4.27 | 0.146 | 0.051 | 2.86 | 0.218 | 0.147 | 1.48 | 11,885 / 2,193 |
| White | 35-55 | 0.058 | 0.015 | 3.82 | 0.142 | 0.051 | 2.79 | 0.224 | 0.160 | 1.40 | 10,665 / 1,599 |

### F2. Does following rise with parental income?

Son-year linear probability models (outcome = son works in the father's cell / industry group / occupation group) on ln parental income, Lee-Solon controls, sons with the father's code.

| | (1) son in the father's cell (occupation group x industry group) | (2) son in the father's industry group (33; as 32) | (3) son in the father's occupation group (11; as 32) |
|---|---|---|---|
| **Pooled (weighted)** | | | |
| ln parental income, sons 25-34 | 0.004 (0.012; p=0.753) | 0.009 (0.016; p=0.587) | 0.051*** (0.016; p=0.001) |
| Mean / N son-years, 25-34 | 0.064 / 15,646 | 0.139 / 16,633 | 0.213 / 15,764 |
| ln parental income, sons 35-55 | 0.031** (0.016; p=0.048) | 0.036 (0.024; p=0.134) | 0.099*** (0.020; p=<0.001) |
| Mean / N son-years, 35-55 | 0.056 / 13,835 | 0.133 / 14,377 | 0.219 / 13,908 |
| Change (35-55) - (25-34) | 0.027*** (0.010; p=0.007) | 0.028* (0.015; p=0.068) | 0.048*** (0.016; p=0.003) |
| **Black** | | | |
| ln parental income, sons 25-34 | -0.014 (0.020; p=0.484) | -0.031 (0.022; p=0.173) | -0.013 (0.024; p=0.590) |
| Mean / N son-years, 25-34 | 0.058 / 3,773 | 0.107 / 4,148 | 0.160 / 3,807 |
| ln parental income, sons 35-55 | 0.012 (0.020; p=0.557) | 0.026 (0.025; p=0.313) | 0.024 (0.025; p=0.332) |
| Mean / N son-years, 35-55 | 0.053 / 3,171 | 0.101 / 3,393 | 0.153 / 3,194 |
| Change (35-55) - (25-34) | 0.026 (0.020; p=0.199) | 0.056*** (0.021; p=0.007) | 0.037 (0.028; p=0.195) |
| **White** | | | |
| ln parental income, sons 25-34 | -0.005 (0.014; p=0.736) | 0.000 (0.019; p=0.997) | 0.040** (0.018; p=0.025) |
| Mean / N son-years, 25-34 | 0.068 / 11,885 | 0.146 / 12,497 | 0.218 / 11,969 |
| ln parental income, sons 35-55 | 0.025 (0.020; p=0.201) | 0.017 (0.030; p=0.554) | 0.099*** (0.023; p=<0.001) |
| Mean / N son-years, 35-55 | 0.058 / 10,665 | 0.142 / 10,985 | 0.224 / 10,715 |
| Change (35-55) - (25-34) | 0.030** (0.012; p=0.015) | 0.017 (0.018; p=0.335) | 0.059*** (0.018; p=0.001) |
| **Black - White** | | | |
| ln parental income, sons 25-34 | -0.009 (0.024; p=0.697) | -0.031 (0.029; p=0.294) | -0.053* (0.030; p=0.077) |
| ln parental income, sons 35-55 | -0.013 (0.028; p=0.643) | 0.008 (0.039; p=0.832) | -0.075** (0.034; p=0.028) |
| Change (35-55) - (25-34) | -0.004 (0.024; p=0.876) | 0.039 (0.028; p=0.159) | -0.022 (0.034; p=0.511) |

### F3. Pay-off of following: wage level and wage growth

Son-year regressions (outcome in the column header; growth = annualised change between consecutive interviews 1-2 years apart, (5) for sons who stayed with the employer). Regressor of interest: following. Held fixed: ln parental income, years of education, the current cell's MORG relative wage at the son's age band (ck) and its local age slope (so the coefficient is the advantage over other sons in equally paid cells with equally steep profiles); age quartic, year FE. Clusters 1968 family; pooled weighted. Followers may differ in unobserved ways (descriptive).

| | (1) ln wage, 25-34 | (2) ln wage, 35-55 | (3) annual ln wage growth, 30-55 | (4) annual ln wage growth, 35-55 | (5) annual growth with the same employer, 35-55 |
|---|---|---|---|---|---|
| **Following = father's cell (occupation group x industry group): Pooled (weighted)** | | | | | |
| son in the father's cell (occupation group x industry group) | 0.022 (0.033; p=0.514) | -0.031 (0.040; p=0.440) | -0.006 (0.010; p=0.541) | 0.001 (0.011; p=0.957) | 0.007 (0.008; p=0.365) |
| N son-years / clusters | 15,645 / 1,357 | 13,834 / 1,122 | 19,870 / 1,231 | 12,920 / 1,093 | 9,391 / 1,007 |
| **Following = father's cell (occupation group x industry group): Black** | | | | | |
| son in the father's cell (occupation group x industry group) | 0.016 (0.053; p=0.756) | 0.073 (0.086; p=0.401) | -0.002 (0.014; p=0.894) | -0.003 (0.017; p=0.865) | -0.017 (0.017; p=0.303) |
| N son-years / clusters | 3,773 / 394 | 3,171 / 293 | 4,439 / 338 | 2,851 / 279 | 2,089 / 255 |
| **Following = father's cell (occupation group x industry group): White** | | | | | |
| son in the father's cell (occupation group x industry group) | -0.015 (0.032; p=0.634) | -0.028 (0.038; p=0.453) | -0.005 (0.010; p=0.600) | 0.002 (0.011; p=0.872) | 0.009 (0.009; p=0.341) |
| N son-years / clusters | 11,884 / 967 | 10,664 / 833 | 15,434 / 897 | 10,070 / 818 | 7,303 / 755 |
| **Following = father's cell (occupation group x industry group): Black - White** | | | | | |
| son in the father's cell (occupation group x industry group) | 0.032 (0.062; p=0.610) | 0.101 (0.094; p=0.285) | 0.003 (0.017; p=0.843) | -0.005 (0.020; p=0.818) | -0.026 (0.019; p=0.174) |
| **Following = father's industry group (33; as 32): Pooled (weighted)** | | | | | |
| son in the father's industry group (33; as 32) | 0.061*** (0.023; p=0.007) | 0.036 (0.029; p=0.218) | 0.004 (0.005; p=0.514) | 0.002 (0.006; p=0.703) | -0.006 (0.006; p=0.282) |
| N son-years / clusters | 15,775 / 1,365 | 13,943 / 1,129 | 20,025 / 1,241 | 13,021 / 1,100 | 9,463 / 1,013 |
| **Following = father's industry group (33; as 32): Black** | | | | | |
| son in the father's industry group (33; as 32) | 0.030 (0.042; p=0.467) | 0.077 (0.066; p=0.244) | -0.005 (0.009; p=0.599) | -0.001 (0.012; p=0.927) | -0.019* (0.011; p=0.078) |
| N son-years / clusters | 3,821 / 398 | 3,214 / 296 | 4,501 / 343 | 2,890 / 282 | 2,116 / 257 |
| **Following = father's industry group (33; as 32): White** | | | | | |
| son in the father's industry group (33; as 32) | 0.038* (0.023; p=0.095) | 0.035 (0.029; p=0.226) | 0.006 (0.006; p=0.323) | 0.004 (0.006; p=0.529) | -0.005 (0.006; p=0.426) |
| N son-years / clusters | 11,966 / 971 | 10,730 / 837 | 15,527 / 902 | 10,132 / 822 | 7,348 / 759 |
| **Following = father's industry group (33; as 32): Black - White** | | | | | |
| son in the father's industry group (33; as 32) | -0.008 (0.047; p=0.869) | 0.042 (0.072; p=0.556) | -0.011 (0.011; p=0.334) | -0.005 (0.013; p=0.710) | -0.015 (0.013; p=0.238) |
| **Following = father's occupation group (11; as 32): Pooled (weighted)** | | | | | |
| son in the father's occupation group (11; as 32) | -0.009 (0.018; p=0.599) | 0.004 (0.026; p=0.894) | -0.001 (0.005; p=0.782) | -0.002 (0.006; p=0.732) | 0.004 (0.005; p=0.390) |
| N son-years / clusters | 15,668 / 1,357 | 13,842 / 1,122 | 19,887 / 1,231 | 12,928 / 1,093 | 9,396 / 1,007 |
| **Following = father's occupation group (11; as 32): Black** | | | | | |
| son in the father's occupation group (11; as 32) | 0.040 (0.033; p=0.225) | 0.035 (0.043; p=0.412) | 0.010 (0.012; p=0.422) | 0.015 (0.015; p=0.322) | 0.020 (0.018; p=0.279) |
| N son-years / clusters | 3,773 / 394 | 3,171 / 293 | 4,439 / 338 | 2,851 / 279 | 2,089 / 255 |
| **Following = father's occupation group (11; as 32): White** | | | | | |
| son in the father's occupation group (11; as 32) | -0.013 (0.018; p=0.488) | -0.006 (0.025; p=0.810) | -0.002 (0.005; p=0.740) | -0.001 (0.006; p=0.833) | 0.005 (0.005; p=0.329) |
| N son-years / clusters | 11,907 / 967 | 10,672 / 833 | 15,451 / 897 | 10,078 / 818 | 7,308 / 755 |
| **Following = father's occupation group (11; as 32): Black - White** | | | | | |
| son in the father's occupation group (11; as 32) | 0.053 (0.038; p=0.162) | 0.041 (0.050; p=0.407) | 0.012 (0.014; p=0.385) | 0.016 (0.016; p=0.317) | 0.015 (0.019; p=0.448) |

### F4. Wage-tenure profiles of followers (person FE)

Within-son regressions of ln wage on tenure with the employer, its square, tenure x following, following, tenure x ln parental income (centred), age quartic and year FE (waves 1984-2023; tenure observed).

| | (1) ln wage; following = father's cell (occupation group x industry group) | (2) ln wage; following = father's industry group (33; as 32) | (3) ln wage; following = father's occupation group (11; as 32) |
|---|---|---|---|
| **Pooled (weighted)** | | | |
| tenure (per 10 years) | 0.237*** (0.022; p=<0.001) | 0.233*** (0.021; p=<0.001) | 0.238*** (0.022; p=<0.001) |
| tenure squared | -0.076*** (0.008; p=<0.001) | -0.074*** (0.008; p=<0.001) | -0.077*** (0.008; p=<0.001) |
| tenure x following | -0.040 (0.025; p=0.101) | -0.042** (0.020; p=0.034) | -0.023 (0.015; p=0.136) |
| following | 0.038 (0.034; p=0.269) | 0.039 (0.025; p=0.112) | 0.035* (0.019; p=0.065) |
| tenure x ln parental income | 0.040** (0.018; p=0.032) | 0.038** (0.018; p=0.036) | 0.041** (0.018; p=0.024) |
| Person FE, year FE, age quartic; N son-years / sons / clusters | 22,851 / 2,975 / 1,326 | 23,404 / 3,020 / 1,338 | 22,990 / 2,986 / 1,327 |
| **Black** | | | |
| tenure (per 10 years) | 0.273*** (0.038; p=<0.001) | 0.245*** (0.040; p=<0.001) | 0.273*** (0.039; p=<0.001) |
| tenure squared | -0.063*** (0.012; p=<0.001) | -0.058*** (0.013; p=<0.001) | -0.065*** (0.013; p=<0.001) |
| tenure x following | -0.094** (0.043; p=0.030) | -0.068* (0.039; p=0.080) | -0.029 (0.033; p=0.386) |
| following | 0.052 (0.054; p=0.328) | 0.115*** (0.040; p=0.004) | 0.026 (0.035; p=0.447) |
| tenure x ln parental income | 0.042 (0.029; p=0.154) | 0.029 (0.030; p=0.326) | 0.039 (0.029; p=0.179) |
| Person FE, year FE, age quartic; N son-years / sons / clusters | 5,372 / 815 / 375 | 5,594 / 836 / 380 | 5,408 / 818 / 376 |
| **White** | | | |
| tenure (per 10 years) | 0.229*** (0.022; p=<0.001) | 0.227*** (0.021; p=<0.001) | 0.232*** (0.022; p=<0.001) |
| tenure squared | -0.075*** (0.008; p=<0.001) | -0.074*** (0.008; p=<0.001) | -0.075*** (0.008; p=<0.001) |
| tenure x following | -0.037 (0.024; p=0.124) | -0.040** (0.019; p=0.039) | -0.027* (0.015; p=0.074) |
| following | 0.028 (0.031; p=0.366) | 0.024 (0.022; p=0.276) | 0.038** (0.019; p=0.043) |
| tenure x ln parental income | 0.048** (0.019; p=0.012) | 0.046** (0.019; p=0.016) | 0.050*** (0.019; p=0.009) |
| Person FE, year FE, age quartic; N son-years / sons / clusters | 17,492 / 2,163 / 956 | 17,823 / 2,187 / 963 | 17,595 / 2,171 / 956 |
| **Black - White** | | | |
| tenure (per 10 years) | 0.044 (0.044; p=0.318) | 0.018 (0.045; p=0.688) | 0.040 (0.044; p=0.363) |
| tenure squared | 0.013 (0.015; p=0.395) | 0.016 (0.015; p=0.292) | 0.010 (0.015; p=0.499) |
| tenure x following | -0.058 (0.049; p=0.244) | -0.028 (0.043; p=0.515) | -0.002 (0.037; p=0.956) |
| following | 0.024 (0.062; p=0.698) | 0.091** (0.045; p=0.045) | -0.011 (0.039; p=0.775) |
| tenure x ln parental income | -0.007 (0.035; p=0.850) | -0.017 (0.035; p=0.632) | -0.010 (0.035; p=0.766) |

### F5. How much of the divergence is following the father? (Gelbach)

(1) the son's ln wage on ln parental income with Lee-Solon controls; (2) adding the following indicator; (3) = (1) - (2) = pi x delta. Stacked; clusters 1968 family; common sample per following measure.

| | (1) ln wage on ln parental income (short) | (2) ... controlling following (long) | (3) accounted for by following = (1) - (2) | (4) following on ln parental income (pi) | (5) ln wage on following (delta, long) |
|---|---|---|---|---|---|
| **Following = father's cell (occupation group x industry group)** | | | | | |
| Pooled (weighted), sons 25-34 | 0.285*** (0.022; p=<0.001) | 0.285*** (0.022; p=<0.001) | -0.000 (0.001; p=0.745) | 0.004 (0.012; p=0.753) | -0.058 (0.046; p=0.204) |
| Pooled (weighted), sons 35-55 | 0.463*** (0.037; p=<0.001) | 0.468*** (0.036; p=<0.001) | -0.006** (0.003; p=0.050) | 0.031** (0.016; p=0.048) | -0.181*** (0.060; p=0.002) |
| Black, sons 25-34 | 0.188*** (0.033; p=<0.001) | 0.187*** (0.033; p=<0.001) | 0.001 (0.002; p=0.566) | -0.014 (0.020; p=0.484) | -0.071 (0.061; p=0.245) |
| Black, sons 35-55 | 0.252*** (0.050; p=<0.001) | 0.253*** (0.050; p=<0.001) | -0.000 (0.001; p=0.665) | 0.012 (0.020; p=0.557) | -0.041 (0.087; p=0.635) |
| White, sons 25-34 | 0.276*** (0.023; p=<0.001) | 0.275*** (0.023; p=<0.001) | 0.000 (0.001; p=0.749) | -0.005 (0.014; p=0.736) | -0.092** (0.045; p=0.041) |
| White, sons 35-55 | 0.460*** (0.039; p=<0.001) | 0.465*** (0.038; p=<0.001) | -0.005 (0.003; p=0.175) | 0.025 (0.020; p=0.201) | -0.187*** (0.059; p=0.002) |
| Black - White, sons 25-34 | -0.088** (0.040; p=0.028) | -0.089** (0.040; p=0.026) | 0.001 (0.002; p=0.791) | -0.009 (0.024; p=0.697) | 0.020 (0.076; p=0.789) |
| Black - White, sons 35-55 | -0.208*** (0.063; p=0.001) | -0.212*** (0.063; p=<0.001) | 0.004 (0.004; p=0.250) | -0.013 (0.028; p=0.643) | 0.145 (0.105; p=0.166) |
| Change of the Black - White gap (35-55) - (25-34) | -0.120** (0.051; p=0.019) | -0.124** (0.051; p=0.015) | 0.004 (0.003; p=0.285) |  |  |
| Share of the change accounted for by following = (3) / (1) | -0.030 (0.032; p=0.349) |  |  |  |  |
| Pooled change (35-55) - (25-34) | 0.178*** (0.030; p=<0.001) |  | -0.005** (0.002; p=0.030) |  |  |
| Share of the pooled change accounted for by following | -0.030* (0.016; p=0.053) |  |  |  |  |
| **Following = father's industry group (33; as 32)** | | | | | |
| Pooled (weighted), sons 25-34 | 0.292*** (0.021; p=<0.001) | 0.291*** (0.021; p=<0.001) | 0.000 (0.000; p=0.911) | 0.009 (0.016; p=0.587) | 0.003 (0.028; p=0.905) |
| Pooled (weighted), sons 35-55 | 0.463*** (0.036; p=<0.001) | 0.466*** (0.036; p=<0.001) | -0.003 (0.002; p=0.198) | 0.036 (0.024; p=0.134) | -0.088** (0.040; p=0.026) |
| Black, sons 25-34 | 0.192*** (0.032; p=<0.001) | 0.191*** (0.032; p=<0.001) | 0.000 (0.002; p=0.846) | -0.031 (0.022; p=0.173) | -0.010 (0.050; p=0.845) |
| Black, sons 35-55 | 0.259*** (0.049; p=<0.001) | 0.259*** (0.049; p=<0.001) | 0.001 (0.002; p=0.750) | 0.026 (0.025; p=0.313) | 0.027 (0.080; p=0.738) |
| White, sons 25-34 | 0.282*** (0.023; p=<0.001) | 0.282*** (0.023; p=<0.001) | -0.000 (0.000; p=0.997) | 0.000 (0.019; p=0.997) | -0.015 (0.028; p=0.595) |
| White, sons 35-55 | 0.457*** (0.038; p=<0.001) | 0.459*** (0.038; p=<0.001) | -0.002 (0.003; p=0.560) | 0.017 (0.030; p=0.554) | -0.094** (0.038; p=0.013) |
| Black - White, sons 25-34 | -0.091** (0.039; p=0.020) | -0.091** (0.039; p=0.020) | 0.000 (0.002; p=0.848) | -0.031 (0.029; p=0.294) | 0.005 (0.057; p=0.930) |
| Black - White, sons 35-55 | -0.198*** (0.063; p=0.002) | -0.200*** (0.062; p=0.001) | 0.002 (0.004; p=0.511) | 0.008 (0.039; p=0.832) | 0.121 (0.088; p=0.171) |
| Change of the Black - White gap (35-55) - (25-34) | -0.107** (0.050; p=0.033) | -0.109** (0.050; p=0.028) | 0.002 (0.004; p=0.625) |  |  |
| Share of the change accounted for by following = (3) / (1) | -0.019 (0.041; p=0.646) |  |  |  |  |
| Pooled change (35-55) - (25-34) | 0.171*** (0.029; p=<0.001) |  | -0.003 (0.003; p=0.201) |  |  |
| Share of the pooled change accounted for by following | -0.019 (0.016; p=0.229) |  |  |  |  |
| **Following = father's occupation group (11; as 32)** | | | | | |
| Pooled (weighted), sons 25-34 | 0.285*** (0.022; p=<0.001) | 0.285*** (0.022; p=<0.001) | 0.000 (0.001; p=0.754) | 0.051*** (0.016; p=0.001) | 0.007 (0.021; p=0.752) |
| Pooled (weighted), sons 35-55 | 0.461*** (0.037; p=<0.001) | 0.460*** (0.037; p=<0.001) | 0.002 (0.004; p=0.631) | 0.099*** (0.020; p=<0.001) | 0.017 (0.035; p=0.621) |
| Black, sons 25-34 | 0.189*** (0.033; p=<0.001) | 0.189*** (0.033; p=<0.001) | 0.000 (0.001; p=0.751) | -0.013 (0.024; p=0.590) | -0.015 (0.039; p=0.698) |
| Black, sons 35-55 | 0.249*** (0.050; p=<0.001) | 0.251*** (0.049; p=<0.001) | -0.002 (0.002; p=0.368) | 0.024 (0.025; p=0.332) | -0.073 (0.046; p=0.111) |
| White, sons 25-34 | 0.275*** (0.023; p=<0.001) | 0.275*** (0.023; p=<0.001) | 0.000 (0.001; p=0.859) | 0.040** (0.018; p=0.025) | 0.004 (0.022; p=0.857) |
| White, sons 35-55 | 0.458*** (0.039; p=<0.001) | 0.457*** (0.039; p=<0.001) | 0.001 (0.003; p=0.828) | 0.099*** (0.023; p=<0.001) | 0.007 (0.033; p=0.825) |
| Black - White, sons 25-34 | -0.086** (0.040; p=0.031) | -0.086** (0.040; p=0.031) | 0.000 (0.001; p=0.975) | -0.053* (0.030; p=0.077) | -0.019 (0.045; p=0.670) |
| Black - White, sons 35-55 | -0.209*** (0.063; p=<0.001) | -0.206*** (0.063; p=0.001) | -0.002 (0.004; p=0.520) | -0.075** (0.034; p=0.028) | -0.081 (0.057; p=0.155) |
| Change of the Black - White gap (35-55) - (25-34) | -0.122** (0.051; p=0.017) | -0.120** (0.051; p=0.019) | -0.003 (0.004; p=0.493) |  |  |
| Share of the change accounted for by following = (3) / (1) | 0.021 (0.031; p=0.500) |  |  |  |  |
| Pooled change (35-55) - (25-34) | 0.176*** (0.030; p=<0.001) |  | 0.001 (0.003; p=0.676) |  |  |
| Share of the pooled change accounted for by following | 0.008 (0.018; p=0.675) |  |  |  |  |

### F7. Are White sons, and sons of rich White parents, more likely to work in the father's cell?

(a) Son-year linear probability models, Black + White sons pooled (weighted), Lee-Solon controls, clusters 1968 family: following on a White indicator, without and with ln parental income. X = the father's cell, his occupation group, or his data-defined cell set (son's current cell in the same set as the father's). Cell sizes: 237 distinct father cells among 3,169 sons with a father's cell (median 6 sons per father cell, 101 cells with < 5 sons). Coding drift: fathers are coded in 1970 codes, sons partly in 2000 / 2010 codes, so measured cell following is a lower bound and drift is larger after 2001 (when more sons are 35+). The 4-set measure is dominated by father and son both in 'neither' (most fathers of poorer sons), so its negative parental-income gradient is mechanical; the informative set measure is the last panel, 'son in a high-paid high-growth cell' among sons whose father was in one (benchmark in (c) = share of ALL sons of that race x tercile in such a cell; cells with < 15 son-years blank).

| | (1) son in the father's X, 25-34 | (2) ... + ln parental income, 25-34 | (3) son in the father's X, 35-55 | (4) ... + ln parental income, 35-55 |
|---|---|---|---|---|
| **X = father's cell (occupation group x industry group)** | | | | |
| White | 0.015 (0.012; p=0.212) | 0.015 (0.013; p=0.251) | 0.026** (0.010; p=0.011) | 0.013 (0.013; p=0.310) |
| ln parental income |  | 0.002 (0.012; p=0.845) |  | 0.029* (0.016; p=0.075) |
| Mean of outcome / N son-years / clusters | 0.064 / 15,646 / 1,358 | 0.064 / 15,646 / 1,358 | 0.056 / 13,835 / 1,123 | 0.056 / 13,835 / 1,123 |
| **X = father's occupation group (11)** | | | | |
| White | 0.059*** (0.022; p=0.006) | 0.042* (0.023; p=0.066) | 0.090*** (0.022; p=<0.001) | 0.049** (0.025; p=0.050) |
| ln parental income |  | 0.047*** (0.016; p=0.003) |  | 0.093*** (0.021; p=<0.001) |
| Mean of outcome / N son-years / clusters | 0.213 / 15,764 / 1,358 | 0.213 / 15,764 / 1,358 | 0.219 / 13,908 / 1,124 | 0.219 / 13,908 / 1,124 |
| **X = father's data-defined cell set (4 sets)** | | | | |
| White | -0.116*** (0.042; p=0.006) | -0.056 (0.044; p=0.201) | -0.212*** (0.043; p=<0.001) | -0.148*** (0.044; p=<0.001) |
| ln parental income |  | -0.165*** (0.020; p=<0.001) |  | -0.145*** (0.026; p=<0.001) |
| Mean of outcome / N son-years / clusters | 0.482 / 15,646 / 1,358 | 0.482 / 15,646 / 1,358 | 0.447 / 13,835 / 1,123 | 0.447 / 13,835 / 1,123 |
| **X = high-paid high-growth set, sons whose father was in it** | | | | |
| White | 0.190*** (0.073; p=0.009) | 0.174** (0.075; p=0.020) | 0.138 (0.103; p=0.182) | 0.124 (0.105; p=0.237) |
| ln parental income |  | 0.098** (0.041; p=0.018) |  | 0.133*** (0.047; p=0.005) |
| Mean of outcome / N son-years / clusters | 0.286 / 2,638 / 327 | 0.286 / 2,638 / 327 | 0.299 / 2,529 / 272 | 0.299 / 2,529 / 272 |

(b) The 'rich White son' test: the same outcome on race x parental-income tercile cells (reference = Black sons in the bottom tercile; terciles pooled over Black and White sons), and on White, centred ln parental income and their interaction.

| | (1) race x tercile cells, 25-34 | (2) race x tercile cells, 35-55 | (3) White x ln parental income, 25-34 | (4) White x ln parental income, 35-55 |
|---|---|---|---|---|
| **Outcome = son in the father's cell (occupation group x industry group)** | | | | |
| Black, tercile 2 (reference: Black, tercile 1) | -0.035 (0.025; p=0.167) | 0.002 (0.012; p=0.852) |  |  |
| Black, tercile 3 (reference: Black, tercile 1) | -0.023 (0.030; p=0.452) | 0.029 (0.028; p=0.304) |  |  |
| White, tercile 1 (reference: Black, tercile 1) | 0.019 (0.031; p=0.543) | 0.042 (0.035; p=0.229) |  |  |
| White, tercile 2 (reference: Black, tercile 1) | -0.024 (0.025; p=0.343) | 0.014 (0.011; p=0.224) |  |  |
| White, tercile 3 (reference: Black, tercile 1) | 0.003 (0.026; p=0.902) | 0.044*** (0.012; p=<0.001) |  |  |
| contrast: White tercile 3 - White tercile 1 (rich vs poor White sons) | -0.015 (0.021; p=0.467) | 0.003 (0.035; p=0.935) |  |  |
| contrast: White tercile 3 - Black tercile 3 (rich White vs rich Black sons) | 0.026 (0.020; p=0.194) | 0.016 (0.029; p=0.582) |  |  |
| contrast: Black tercile 3 - Black tercile 1 | -0.023 (0.030; p=0.452) | 0.029 (0.028; p=0.304) |  |  |
| White (at mean ln parental income) |  |  | 0.015 (0.013; p=0.237) | 0.014 (0.012; p=0.259) |
| ln parental income (Black sons) |  |  | -0.022 (0.020; p=0.263) | 0.008 (0.017; p=0.641) |
| White x ln parental income |  |  | 0.026 (0.023; p=0.265) | 0.023 (0.026; p=0.360) |
| ln parental income, White sons (sum) |  |  | 0.004 (0.013; p=0.743) | 0.031* (0.018; p=0.083) |
| N son-years / clusters | 15,646 / 1,358 | 13,835 / 1,123 | 15,646 / 1,358 | 13,835 / 1,123 |
| **Outcome = son in the father's occupation group (11)** | | | | |
| Black, tercile 2 (reference: Black, tercile 1) | -0.040 (0.036; p=0.278) | -0.071* (0.041; p=0.086) |  |  |
| Black, tercile 3 (reference: Black, tercile 1) | -0.069 (0.046; p=0.131) | -0.047 (0.049; p=0.335) |  |  |
| White, tercile 1 (reference: Black, tercile 1) | 0.012 (0.040; p=0.771) | -0.001 (0.050; p=0.986) |  |  |
| White, tercile 2 (reference: Black, tercile 1) | -0.008 (0.035; p=0.811) | 0.013 (0.038; p=0.731) |  |  |
| White, tercile 3 (reference: Black, tercile 1) | 0.052 (0.035; p=0.139) | 0.084** (0.037; p=0.024) |  |  |
| contrast: White tercile 3 - White tercile 1 (rich vs poor White sons) | 0.040 (0.028; p=0.148) | 0.085** (0.040; p=0.034) |  |  |
| contrast: White tercile 3 - Black tercile 3 (rich White vs rich Black sons) | 0.121*** (0.034; p=<0.001) | 0.131*** (0.038; p=<0.001) |  |  |
| contrast: Black tercile 3 - Black tercile 1 | -0.069 (0.046; p=0.131) | -0.047 (0.049; p=0.335) |  |  |
| White (at mean ln parental income) |  |  | 0.043** (0.021; p=0.044) | 0.055** (0.022; p=0.012) |
| ln parental income (Black sons) |  |  | -0.060* (0.035; p=0.087) | -0.035 (0.035; p=0.322) |
| White x ln parental income |  |  | 0.115*** (0.039; p=0.003) | 0.139*** (0.042; p=<0.001) |
| ln parental income, White sons (sum) |  |  | 0.055*** (0.017; p=0.001) | 0.104*** (0.022; p=<0.001) |
| N son-years / clusters | 15,764 / 1,358 | 13,908 / 1,124 | 15,764 / 1,358 | 13,908 / 1,124 |
| **Outcome = son in the father's data-defined cell set (4 sets)** | | | | |
| Black, tercile 2 (reference: Black, tercile 1) | -0.066 (0.061; p=0.281) | 0.030 (0.080; p=0.706) |  |  |
| Black, tercile 3 (reference: Black, tercile 1) | -0.286*** (0.098; p=0.004) | -0.297*** (0.100; p=0.003) |  |  |
| White, tercile 1 (reference: Black, tercile 1) | -0.013 (0.076; p=0.861) | -0.091 (0.078; p=0.245) |  |  |
| White, tercile 2 (reference: Black, tercile 1) | -0.184** (0.073; p=0.011) | -0.216*** (0.067; p=0.001) |  |  |
| White, tercile 3 (reference: Black, tercile 1) | -0.278*** (0.072; p=<0.001) | -0.318*** (0.065; p=<0.001) |  |  |
| contrast: White tercile 3 - White tercile 1 (rich vs poor White sons) | -0.265*** (0.036; p=<0.001) | -0.227*** (0.052; p=<0.001) |  |  |
| contrast: White tercile 3 - Black tercile 3 (rich White vs rich Black sons) | 0.007 (0.071; p=0.918) | -0.020 (0.082; p=0.807) |  |  |
| contrast: Black tercile 3 - Black tercile 1 | -0.286*** (0.098; p=0.004) | -0.297*** (0.100; p=0.003) |  |  |
| White (at mean ln parental income) |  |  | -0.055 (0.043; p=0.203) | -0.145*** (0.044; p=<0.001) |
| ln parental income (Black sons) |  |  | -0.184*** (0.065; p=0.005) | -0.196*** (0.075; p=0.009) |
| White x ln parental income |  |  | 0.020 (0.068; p=0.769) | 0.056 (0.079; p=0.481) |
| ln parental income, White sons (sum) |  |  | -0.164*** (0.021; p=<0.001) | -0.140*** (0.028; p=<0.001) |
| N son-years / clusters | 15,646 / 1,358 | 13,835 / 1,123 | 15,646 / 1,358 | 13,835 / 1,123 |
| **Outcome = son in the high-paid high-growth set, sons whose father was in it** | | | | |
| Black, tercile 2 (reference: Black, tercile 1) | 0.024 (0.038; p=0.527) | -0.287 (0.284; p=0.313) |  |  |
| Black, tercile 3 (reference: Black, tercile 1) | 0.141* (0.084; p=0.093) | -0.168 (0.300; p=0.575) |  |  |
| White, tercile 1 (reference: Black, tercile 1) | 0.165** (0.079; p=0.036) | -0.393 (0.285; p=0.167) |  |  |
| White, tercile 2 (reference: Black, tercile 1) | 0.187*** (0.043; p=<0.001) | -0.191 (0.283; p=0.500) |  |  |
| White, tercile 3 (reference: Black, tercile 1) | 0.348*** (0.030; p=<0.001) | 0.009 (0.282; p=0.974) |  |  |
| contrast: White tercile 3 - White tercile 1 (rich vs poor White sons) | 0.184** (0.079; p=0.019) | 0.403*** (0.053; p=<0.001) |  |  |
| contrast: White tercile 3 - Black tercile 3 (rich White vs rich Black sons) | 0.207** (0.086; p=0.016) | 0.178 (0.110; p=0.105) |  |  |
| contrast: Black tercile 3 - Black tercile 1 | 0.141* (0.084; p=0.093) | -0.168 (0.300; p=0.575) |  |  |
| White (at mean ln parental income) |  |  | 0.076 (0.097; p=0.436) | -0.228 (0.215; p=0.289) |
| ln parental income (Black sons) |  |  | -0.108 (0.083; p=0.195) | -0.535** (0.249; p=0.031) |
| White x ln parental income |  |  | 0.208** (0.093; p=0.026) | 0.671*** (0.253; p=0.008) |
| ln parental income, White sons (sum) |  |  | 0.100** (0.042; p=0.017) | 0.136*** (0.047; p=0.004) |
| N son-years / clusters | 2,638 / 327 | 2,529 / 272 | 2,638 / 327 | 2,529 / 272 |

(c) Observed share vs random matching within race x parental-income tercile (as 32 Table 4a, at the cell level): benchmark = sum_j p_son(j) p_father(j) in the cell; ratio = observed / benchmark. Unweighted; cells with < 30 son-years blank.

| Race | parental-income tercile | sons' ages | father's cell (occupation group x industry group): observed | benchmark | ratio | father's occupation group (11): observed | benchmark | ratio | father's data-defined cell set (4 sets): observed | benchmark | ratio | high-paid high-growth set, sons whose father was in it: observed | benchmark | ratio | son-years / sons (cell) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Black | 1 | 25-34 | 0.067 | 0.020 | 3.31 | 0.167 | 0.126 | 1.33 | 0.770 | 0.777 | 0.99 | 0.000 | 0.046 | 0.00 | 1,362 / 278 |
| Black | 1 | 35-55 | 0.038 | 0.018 | 2.13 | 0.149 | 0.116 | 1.29 | 0.750 | 0.755 | 0.99 |  |  |  | 1,287 / 203 |
| Black | 2 | 25-34 | 0.050 | 0.015 | 3.35 | 0.164 | 0.122 | 1.34 | 0.700 | 0.710 | 0.99 | 0.042 | 0.058 | 0.72 | 1,612 / 356 |
| Black | 2 | 35-55 | 0.064 | 0.017 | 3.69 | 0.144 | 0.116 | 1.24 | 0.748 | 0.740 | 1.01 |  |  |  | 1,315 / 245 |
| Black | 3 | 25-34 | 0.059 | 0.016 | 3.79 | 0.139 | 0.112 | 1.24 | 0.534 | 0.506 | 1.06 | 0.174 | 0.135 | 1.29 | 799 / 204 |
| Black | 3 | 35-55 | 0.060 | 0.025 | 2.43 | 0.183 | 0.122 | 1.50 | 0.580 | 0.528 | 1.10 | 0.236 | 0.146 | 1.62 | 569 / 120 |
| White | 1 | 25-34 | 0.098 | 0.030 | 3.21 | 0.210 | 0.129 | 1.62 | 0.694 | 0.683 | 1.02 | 0.152 | 0.082 | 1.84 | 1,177 / 216 |
| White | 1 | 35-55 | 0.074 | 0.031 | 2.38 | 0.174 | 0.125 | 1.39 | 0.638 | 0.662 | 0.96 | 0.038 | 0.112 | 0.34 | 835 / 132 |
| White | 2 | 25-34 | 0.053 | 0.016 | 3.24 | 0.187 | 0.143 | 1.31 | 0.527 | 0.519 | 1.02 | 0.156 | 0.126 | 1.24 | 4,306 / 770 |
| White | 2 | 35-55 | 0.039 | 0.014 | 2.86 | 0.184 | 0.139 | 1.32 | 0.487 | 0.477 | 1.02 | 0.177 | 0.155 | 1.14 | 3,977 / 580 |
| White | 3 | 25-34 | 0.073 | 0.013 | 5.58 | 0.240 | 0.154 | 1.56 | 0.408 | 0.319 | 1.28 | 0.311 | 0.202 | 1.54 | 6,402 / 1,207 |
| White | 3 | 35-55 | 0.069 | 0.014 | 4.93 | 0.258 | 0.180 | 1.43 | 0.378 | 0.307 | 1.23 | 0.340 | 0.259 | 1.32 | 5,853 / 887 |

### F6. Sons in a data-defined high-paid high-growth cell when the father was in one

Son-year linear probability model: the son's CURRENT cell is high-paid AND high later growth (Section D) on indicators of the father's cell set (reference = father's cell in neither set) and ln parental income; Lee-Solon controls. Sons whose father's cell is high-paid and high-growth: Black 41, White 498.

| | (1) son in a high-paid high-growth cell |
|---|---|
| **Pooled (weighted)** | |
| father in a high-paid high-growth cell, sons 25-34 | 0.112*** (0.022; p=<0.001) |
| father in a high-paid-only cell, sons 25-34 | 0.021 (0.024; p=0.383) |
| father in a high-growth-only cell, sons 25-34 | -0.038 (0.024; p=0.113) |
| ln parental income, sons 25-34 | 0.061*** (0.014; p=<0.001) |
| Mean / N son-years, 25-34 | 0.178 / 15,646 |
| father in a high-paid high-growth cell, sons 35-55 | 0.090*** (0.028; p=0.001) |
| father in a high-paid-only cell, sons 35-55 | 0.026 (0.032; p=0.421) |
| father in a high-growth-only cell, sons 35-55 | -0.032 (0.034; p=0.337) |
| ln parental income, sons 35-55 | 0.077*** (0.021; p=<0.001) |
| Mean / N son-years, 35-55 | 0.210 / 13,835 |
| **Black** | |
| father in a high-paid high-growth cell, sons 25-34 | 0.019 (0.055; p=0.732) |
| father in a high-paid-only cell, sons 25-34 | -0.006 (0.056; p=0.913) |
| father in a high-growth-only cell, sons 25-34 | -0.020 (0.027; p=0.464) |
| ln parental income, sons 25-34 | 0.053*** (0.018; p=0.003) |
| Mean / N son-years, 25-34 | 0.083 / 3,773 |
| father in a high-paid high-growth cell, sons 35-55 | 0.113 (0.091; p=0.216) |
| father in a high-paid-only cell, sons 35-55 | 0.034 (0.078; p=0.664) |
| father in a high-growth-only cell, sons 35-55 | 0.105 (0.093; p=0.258) |
| ln parental income, sons 35-55 | 0.037 (0.027; p=0.167) |
| Mean / N son-years, 35-55 | 0.089 / 3,171 |
| **White** | |
| father in a high-paid high-growth cell, sons 25-34 | 0.108*** (0.022; p=<0.001) |
| father in a high-paid-only cell, sons 25-34 | 0.018 (0.023; p=0.438) |
| father in a high-growth-only cell, sons 25-34 | -0.016 (0.029; p=0.581) |
| ln parental income, sons 25-34 | 0.060*** (0.015; p=<0.001) |
| Mean / N son-years, 25-34 | 0.175 / 11,885 |
| father in a high-paid high-growth cell, sons 35-55 | 0.094*** (0.027; p=<0.001) |
| father in a high-paid-only cell, sons 35-55 | 0.018 (0.029; p=0.543) |
| father in a high-growth-only cell, sons 35-55 | -0.027 (0.037; p=0.463) |
| ln parental income, sons 35-55 | 0.072*** (0.020; p=<0.001) |
| Mean / N son-years, 35-55 | 0.214 / 10,665 |
| **Black - White** | |
| father in a high-paid high-growth cell, sons 25-34 | -0.089 (0.059; p=0.129) |
| father in a high-paid-only cell, sons 25-34 | -0.024 (0.061; p=0.691) |
| father in a high-growth-only cell, sons 25-34 | -0.004 (0.040; p=0.921) |
| ln parental income, sons 25-34 | -0.007 (0.023; p=0.770) |
| father in a high-paid high-growth cell, sons 35-55 | 0.019 (0.095; p=0.840) |
| father in a high-paid-only cell, sons 35-55 | 0.016 (0.083; p=0.849) |
| father in a high-growth-only cell, sons 35-55 | 0.132 (0.100; p=0.186) |
| ln parental income, sons 35-55 | -0.035 (0.034; p=0.302) |

### F8. Do sons return to the father's line of work after first trying other jobs? (within sons)

#### F8 (i). Level: occupation group x industry group cell

Sons with a father's code and valid son-years: 3,169; observed with a code in BOTH 25-34 and 35-55: 2,029 (64% kept). In / out = the son's modal occupation group x industry group cell in the window equals the father's modal one. Distinct father codes: 237. Coding drift: fathers are coded in 1970 codes, sons after 2001 in 2000 / 2010 codes, and the 35-55 window falls more often after 2001, which biases measured ENTRY down and LEAVING up.

(1) Transitions between 25-34 and 35-55 (shares of sons):

| Race | parental-income tercile | sons in both windows | out -> out | out -> IN (enter) | IN -> IN | IN -> out (leave) | share entering among those out at 25-34 |
|---|---|---|---|---|---|---|---|
| Black + White | all | 2,029 | 0.913 | 0.019 | 0.041 | 0.026 | 0.021 |
| Black + White | 1 | 300 | 0.907 | 0.027 | 0.027 | 0.040 | 0.029 |
| Black + White | 2 | 772 | 0.925 | 0.017 | 0.028 | 0.030 | 0.018 |
| Black + White | 3 | 957 | 0.906 | 0.019 | 0.056 | 0.019 | 0.020 |
| Black | all | 502 | 0.926 | 0.024 | 0.018 | 0.032 | 0.025 |
| Black | 1 | 172 | 0.924 | 0.029 | 0.006 | 0.041 | 0.030 |
| Black | 2 | 220 | 0.918 | 0.023 | 0.023 | 0.036 | 0.024 |
| Black | 3 | 110 | 0.945 | 0.018 | 0.027 | 0.009 | 0.019 |
| White | all | 1,527 | 0.909 | 0.018 | 0.049 | 0.024 | 0.019 |
| White | 1 | 128 | 0.883 | 0.023 | 0.055 | 0.039 | 0.026 |
| White | 2 | 552 | 0.928 | 0.014 | 0.031 | 0.027 | 0.015 |
| White | 3 | 847 | 0.901 | 0.019 | 0.060 | 0.020 | 0.021 |

(2) Son-level linear probability models (outcome in the column header; controls birth-year quadratic; pooled weighted, by race unweighted; clusters 1968 family). Columns (4)-(5): does being in the father's industry (type a) or occupation (type b) at 25-34 predict ending up in his exact cell after 35?

| | (1) enters the father's cell (out at 25-34, in at 35-55) | (2) leaves (in at 25-34, out at 35-55) | (3) in the father's cell at 35-55 (all sons) | (4) enters, on the 25-34 type (ref. different industry and occupation) | (5) in the father's cell at 35-55, on the 25-34 type |
|---|---|---|---|---|---|
| **Pooled (weighted)** | | | | | |
| ln parental income | 0.021* (0.011; p=0.069) | -0.167** (0.067; p=0.014) | 0.041** (0.016; p=0.012) | 0.019* (0.011; p=0.088) | 0.031** (0.013; p=0.014) |
| 25-34: same industry group, different occupation |  |  |  | 0.054** (0.024; p=0.023) | 0.054** (0.024; p=0.021) |
| 25-34: same occupation group, different industry |  |  |  | 0.040** (0.016; p=0.016) | 0.038** (0.016; p=0.021) |
| 25-34: already in the cell |  |  |  |  | 0.623*** (0.045; p=<0.001) |
| Mean of outcome | 0.021 | 0.366 | 0.066 | 0.021 | 0.066 |
| N sons / clusters | 1,891 / 1,031 | 137 / 120 | 2,028 / 1,080 | 1,891 / 1,031 | 2,028 / 1,080 |
| **Black** | | | | | |
| ln parental income | -0.017 (0.019; p=0.364) |  | -0.007 (0.021; p=0.753) | -0.017 (0.019; p=0.372) | -0.006 (0.020; p=0.781) |
| 25-34: same industry group, different occupation |  |  |  | 0.061 (0.057; p=0.286) | 0.061 (0.057; p=0.286) |
| 25-34: same occupation group, different industry |  |  |  | -0.004 (0.019; p=0.822) | -0.005 (0.019; p=0.788) |
| 25-34: already in the cell |  |  |  |  | 0.339*** (0.097; p=<0.001) |
| Mean of outcome | 0.025 |  | 0.042 | 0.025 | 0.042 |
| N sons / clusters | 477 / 268 |  | 502 / 276 | 477 / 268 | 502 / 276 |
| **White** | | | | | |
| ln parental income | 0.016 (0.010; p=0.101) | -0.136** (0.069; p=0.050) | 0.034** (0.017; p=0.045) | 0.014 (0.009; p=0.145) | 0.025** (0.012; p=0.035) |
| 25-34: same industry group, different occupation |  |  |  | 0.052** (0.023; p=0.022) | 0.052** (0.023; p=0.021) |
| 25-34: same occupation group, different industry |  |  |  | 0.032** (0.014; p=0.027) | 0.031** (0.015; p=0.035) |
| 25-34: already in the cell |  |  |  |  | 0.659*** (0.043; p=<0.001) |
| Mean of outcome | 0.019 | 0.330 | 0.067 | 0.019 | 0.067 |
| N sons / clusters | 1,415 / 766 | 112 / 98 | 1,527 / 807 | 1,415 / 766 | 1,527 / 807 |
| **Black - White** | | | | | |
| ln parental income | -0.033 (0.022; p=0.121) |  | -0.040 (0.027; p=0.131) | -0.031 (0.021; p=0.149) | -0.030 (0.023; p=0.194) |
| 25-34: same industry group, different occupation |  |  |  | 0.009 (0.061; p=0.888) | 0.008 (0.061; p=0.891) |
| 25-34: same occupation group, different industry |  |  |  | -0.036 (0.024; p=0.132) | -0.036 (0.024; p=0.138) |
| 25-34: already in the cell |  |  |  |  | -0.321*** (0.106; p=0.003) |

(3) Churning at 25-34: distinct cells and employer changes (tenure resets: the son was not with the previous interview's employer; observed from 1985) at 25-34, by eventual group:

| Race | group of sons | sons | distinct cells at 25-34 | employer changes per observed interview at 25-34 | 25-34 son-years |
|---|---|---|---|---|---|
| Black + White | entrants (out at 25-34, in at 35-55) | 39 | 3.46 | 0.177 | 6.8 |
| Black + White | stayers (in at both) | 84 | 1.82 | 0.124 | 6.5 |
| Black + White | never in the father's cell | 1,853 | 2.89 | 0.222 | 6.0 |
| Black | entrants (out at 25-34, in at 35-55) | 12 | 3.50 | 0.175 | 6.6 |
| Black | stayers (in at both) | 9 | 1.44 | 0.031 | 5.9 |
| Black | never in the father's cell | 465 | 2.72 | 0.247 | 5.2 |
| White | entrants (out at 25-34, in at 35-55) | 27 | 3.44 | 0.178 | 6.9 |
| White | stayers (in at both) | 75 | 1.87 | 0.136 | 6.5 |
| White | never in the father's cell | 1,388 | 2.95 | 0.214 | 6.3 |

| | (1) distinct cells at 25-34 | (2) employer changes per interview at 25-34 |
|---|---|---|
| **Pooled (weighted)** | | |
| entrant (ref. never in the father's cell) | 0.295 (0.245; p=0.227) | -0.005 (0.051; p=0.924) |
| stayer | -1.108*** (0.144; p=<0.001) | -0.069** (0.028; p=0.014) |
| 25-34 son-years / 10 | 2.695*** (0.156; p=<0.001) | -0.292*** (0.053; p=<0.001) |
| ln parental income | -0.102 (0.071; p=0.154) | -0.030* (0.017; p=0.075) |
| N sons / clusters | 2,028 / 1,080 | 1,789 / 999 |
| **Black** | | |
| entrant (ref. never in the father's cell) | 0.402 (0.277; p=0.147) | -0.030 (0.065; p=0.640) |
| stayer | -1.480*** (0.198; p=<0.001) | -0.220*** (0.056; p=<0.001) |
| 25-34 son-years / 10 | 2.870*** (0.237; p=<0.001) | -0.318*** (0.082; p=<0.001) |
| ln parental income | 0.091 (0.110; p=0.410) | -0.013 (0.033; p=0.691) |
| N sons / clusters | 502 / 276 | 420 / 245 |
| **White** | | |
| entrant (ref. never in the father's cell) | 0.312 (0.270; p=0.247) | -0.015 (0.051; p=0.772) |
| stayer | -1.114*** (0.146; p=<0.001) | -0.058* (0.032; p=0.065) |
| 25-34 son-years / 10 | 2.557*** (0.167; p=<0.001) | -0.286*** (0.054; p=<0.001) |
| ln parental income | -0.063 (0.072; p=0.383) | -0.039** (0.017; p=0.024) |
| N sons / clusters | 1,527 / 807 | 1,370 / 757 |
| **Black - White** | | |
| entrant (ref. never in the father's cell) | 0.090 (0.387; p=0.817) | -0.015 (0.083; p=0.852) |
| stayer | -0.366 (0.246; p=0.136) | -0.162** (0.064; p=0.011) |
| 25-34 son-years / 10 | 0.313 (0.290; p=0.280) | -0.032 (0.098; p=0.745) |
| ln parental income | 0.154 (0.132; p=0.243) | 0.026 (0.037; p=0.491) |

(PI) Where were sons at 25-34 relative to the father's cell? Modal 25-34 type for ALL sons in both windows (observed vs random matching of sons' 25-34 cells to fathers' cells within the row), and for the eventual entrants (in the father's cell at 35-55 but not modal at 25-34):

| Race / parental-income tercile | sons | same industry group, different occupation group: observed | benchmark | same occupation group, different industry group: observed | benchmark | different industry AND occupation: observed | benchmark | already in the father's cell: observed | benchmark | entrants (in at 35-55, not modal at 25-34): type a | type b | type c | entrants: mean share of 25-34 son-years in a / b / c / d |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Black + White, all | 2,029 | 0.068 | 0.034 | 0.142 | 0.105 | 0.723 | 0.848 | 0.068 | 0.013 | 39: 0.23 | 0.28 | 0.49 | 0.16 / 0.22 / 0.45 / 0.17 |
| Black, tercile 1 | 172 | 0.064 | 0.036 | 0.128 | 0.109 | 0.762 | 0.835 | 0.047 | 0.020 | 5: 0.40 | 0.00 | 0.60 | 0.23 / 0.00 / 0.52 / 0.25 |
| Black, tercile 2 | 220 | 0.036 | 0.032 | 0.105 | 0.113 | 0.800 | 0.839 | 0.059 | 0.017 | 5: 0.00 | 0.20 | 0.80 | 0.00 / 0.18 / 0.65 / 0.17 |
| Black, tercile 3 | 110 | 0.045 | 0.034 | 0.082 | 0.099 | 0.836 | 0.854 | 0.036 | 0.013 | 2: 0.00 | 0.00 | 1.00 | 0.00 / 0.12 / 0.78 / 0.10 |
| White, tercile 1 | 128 | 0.086 | 0.036 | 0.148 | 0.095 | 0.672 | 0.836 | 0.094 | 0.033 | 3: 0.33 | 0.33 | 0.33 | 0.13 / 0.20 / 0.33 / 0.34 |
| White, tercile 2 | 552 | 0.069 | 0.036 | 0.141 | 0.129 | 0.732 | 0.818 | 0.058 | 0.017 | 8: 0.12 | 0.50 | 0.38 | 0.15 / 0.35 / 0.37 / 0.13 |
| White, tercile 3 (rich White) | 847 | 0.076 | 0.032 | 0.163 | 0.144 | 0.681 | 0.810 | 0.080 | 0.014 | 16: 0.31 | 0.31 | 0.38 | 0.23 / 0.25 / 0.39 / 0.13 |
| Black, all | 502 | 0.048 | 0.032 | 0.108 | 0.104 | 0.795 | 0.849 | 0.050 | 0.015 | 12: 0.17 | 0.08 | 0.75 | 0.10 / 0.10 / 0.62 / 0.19 |
| White, all | 1,527 | 0.074 | 0.034 | 0.154 | 0.118 | 0.699 | 0.833 | 0.073 | 0.015 | 27: 0.26 | 0.37 | 0.37 | 0.19 / 0.28 / 0.38 / 0.16 |

(4) Within sons: son-year linear probability model of being in the father's cell on ln parental income x age with person FE (the age gradient is identified within sons, not across cohorts), year FE and a common after-35 shift. Positive = sons of richer parents move INTO the father's cell as they age.

| | (1) all sons with a father's cell: ln parental income x (age-40)/10 | (2) ... ln parental income x age >= 35 | (3) sons observed in both windows: x (age-40)/10 | (4) ... x age >= 35 |
|---|---|---|---|---|
| **Pooled (weighted)** | | | | |
| ln parental income x age term (within son) | 0.011* (0.006; p=0.075) | 0.015* (0.008; p=0.053) | 0.011* (0.006; p=0.075) | 0.015* (0.008; p=0.054) |
| Person FE, year FE, common after-35 shift; N son-years / sons / clusters | 29,481 / 3,166 / 1,387 | 29,481 / 3,166 / 1,387 | 25,496 / 2,028 / 1,080 | 25,496 / 2,028 / 1,080 |
| **Black** | | | | |
| ln parental income x age term (within son) | 0.020 (0.016; p=0.222) | 0.014 (0.018; p=0.438) | 0.015 (0.017; p=0.361) | 0.016 (0.018; p=0.368) |
| Person FE, year FE, common after-35 shift; N son-years / sons / clusters | 6,944 / 904 / 407 | 6,944 / 904 / 407 | 5,556 / 502 / 276 | 5,556 / 502 / 276 |
| **White** | | | | |
| ln parental income x age term (within son) | 0.011* (0.006; p=0.073) | 0.017** (0.008; p=0.026) | 0.011* (0.006; p=0.062) | 0.017** (0.008; p=0.028) |
| Person FE, year FE, common after-35 shift; N son-years / sons / clusters | 22,550 / 2,265 / 985 | 22,550 / 2,265 / 985 | 19,943 / 1,527 / 807 | 19,943 / 1,527 / 807 |
| **Black - White** | | | | |
| ln parental income x age term (within son) | 0.010 (0.017; p=0.586) | -0.003 (0.019; p=0.877) | 0.004 (0.018; p=0.814) | -0.000 (0.020; p=0.990) |

#### F8 (ii). Level: fine cell occ1990dd x ind1990ddx

Sons with a father's code and valid son-years: 3,174; observed with a code in BOTH 25-34 and 35-55: 2,036 (64% kept). In / out = the son's modal fine cell occ1990dd x ind1990ddx in the window equals the father's modal one. Distinct father codes: 1,204 (fine cells are sparse: the father's fine cell combines his modal occ1990dd and his modal ind1990ddx, which need not come from the same waves; matches at this level are rare and coding drift between 1970 and 2000 / 2010 codes is largest).

(1) Transitions between 25-34 and 35-55 (shares of sons):

| Race | parental-income tercile | sons in both windows | out -> out | out -> IN (enter) | IN -> IN | IN -> out (leave) | share entering among those out at 25-34 |
|---|---|---|---|---|---|---|---|
| Black + White | all | 2,036 | 0.955 | 0.013 | 0.019 | 0.013 | 0.014 |
| Black + White | 1 | 301 | 0.960 | 0.010 | 0.013 | 0.017 | 0.010 |
| Black + White | 2 | 775 | 0.964 | 0.012 | 0.012 | 0.013 | 0.012 |
| Black + White | 3 | 960 | 0.947 | 0.016 | 0.026 | 0.011 | 0.016 |
| Black | all | 505 | 0.972 | 0.012 | 0.006 | 0.010 | 0.012 |
| Black | 1 | 172 | 0.983 | 0.006 | 0.006 | 0.006 | 0.006 |
| Black | 2 | 222 | 0.959 | 0.018 | 0.009 | 0.014 | 0.018 |
| Black | 3 | 111 | 0.982 | 0.009 | 0.000 | 0.009 | 0.009 |
| White | all | 1,531 | 0.950 | 0.014 | 0.023 | 0.014 | 0.014 |
| White | 1 | 129 | 0.930 | 0.016 | 0.023 | 0.031 | 0.016 |
| White | 2 | 553 | 0.966 | 0.009 | 0.013 | 0.013 | 0.009 |
| White | 3 | 849 | 0.942 | 0.016 | 0.029 | 0.012 | 0.017 |

(2) Son-level linear probability models (outcome in the column header; controls birth-year quadratic; pooled weighted, by race unweighted; clusters 1968 family). Columns (4)-(5): does being in the father's industry (type a) or occupation (type b) at 25-34 predict ending up in his exact cell after 35?

| | (1) enters the father's cell (out at 25-34, in at 35-55) | (2) leaves (in at 25-34, out at 35-55) | (3) in the father's cell at 35-55 (all sons) | (4) enters, on the 25-34 type (ref. different industry and occupation) | (5) in the father's cell at 35-55, on the 25-34 type |
|---|---|---|---|---|---|
| **Pooled (weighted)** | | | | | |
| ln parental income | 0.019** (0.010; p=0.050) | -0.173** (0.077; p=0.024) | 0.035*** (0.013; p=0.009) | 0.018** (0.009; p=0.047) | 0.028*** (0.010; p=0.005) |
| 25-34: same industry group, different occupation |  |  |  | 0.065** (0.026; p=0.013) | 0.064** (0.026; p=0.014) |
| 25-34: same occupation group, different industry |  |  |  | 0.031 (0.030; p=0.295) | 0.031 (0.030; p=0.302) |
| 25-34: already in the cell |  |  |  |  | 0.601*** (0.063; p=<0.001) |
| Mean of outcome | 0.014 | 0.388 | 0.034 | 0.014 | 0.034 |
| N sons / clusters | 1,971 / 1,063 | 64 / 57 | 2,035 / 1,082 | 1,971 / 1,063 | 2,035 / 1,082 |
| **Black** | | | | | |
| ln parental income | 0.000 (0.008; p=0.956) |  | -0.002 (0.011; p=0.824) | 0.000 (0.008; p=0.979) | -0.005 (0.010; p=0.648) |
| 25-34: same industry group, different occupation |  |  |  | -0.011** (0.005; p=0.037) | -0.012** (0.005; p=0.027) |
| 25-34: same occupation group, different industry |  |  |  | 0.089 (0.096; p=0.355) | 0.089 (0.096; p=0.354) |
| 25-34: already in the cell |  |  |  |  | 0.369** (0.172; p=0.031) |
| Mean of outcome | 0.012 |  | 0.018 | 0.012 | 0.018 |
| N sons / clusters | 497 / 276 |  | 505 / 277 | 497 / 276 | 505 / 277 |
| **White** | | | | | |
| ln parental income | 0.017* (0.010; p=0.075) | -0.164** (0.082; p=0.046) | 0.032** (0.014; p=0.025) | 0.016* (0.009; p=0.074) | 0.026*** (0.010; p=0.008) |
| 25-34: same industry group, different occupation |  |  |  | 0.066** (0.026; p=0.011) | 0.066** (0.026; p=0.011) |
| 25-34: same occupation group, different industry |  |  |  | 0.028 (0.028; p=0.309) | 0.028 (0.028; p=0.309) |
| 25-34: already in the cell |  |  |  |  | 0.616*** (0.061; p=<0.001) |
| Mean of outcome | 0.014 | 0.375 | 0.037 | 0.014 | 0.037 |
| N sons / clusters | 1,475 / 790 | 56 / 49 | 1,531 / 808 | 1,475 / 790 | 1,531 / 808 |
| **Black - White** | | | | | |
| ln parental income | -0.017 (0.013; p=0.187) |  | -0.035* (0.018; p=0.055) | -0.016 (0.012; p=0.193) | -0.031** (0.014; p=0.028) |
| 25-34: same industry group, different occupation |  |  |  | -0.077*** (0.026; p=0.004) | -0.078*** (0.026; p=0.003) |
| 25-34: same occupation group, different industry |  |  |  | 0.061 (0.100; p=0.543) | 0.061 (0.100; p=0.541) |
| 25-34: already in the cell |  |  |  |  | -0.247 (0.182; p=0.176) |

(3) Churning at 25-34: distinct cells and employer changes (tenure resets: the son was not with the previous interview's employer; observed from 1985) at 25-34, by eventual group:

| Race | group of sons | sons | distinct cells at 25-34 | employer changes per observed interview at 25-34 | 25-34 son-years |
|---|---|---|---|---|---|
| Black + White | entrants (out at 25-34, in at 35-55) | 27 | 3.67 | 0.065 | 6.8 |
| Black + White | stayers (in at both) | 38 | 2.21 | 0.145 | 7.2 |
| Black + White | never in the father's cell | 1,945 | 3.44 | 0.220 | 6.0 |
| Black | entrants (out at 25-34, in at 35-55) | 6 | 4.00 | 0.150 | 5.3 |
| Black | stayers (in at both) | 3 | 2.00 | 0.000 | 8.0 |
| Black | never in the father's cell | 491 | 3.19 | 0.240 | 5.3 |
| White | entrants (out at 25-34, in at 35-55) | 21 | 3.57 | 0.041 | 7.2 |
| White | stayers (in at both) | 35 | 2.23 | 0.160 | 7.2 |
| White | never in the father's cell | 1,454 | 3.52 | 0.214 | 6.3 |

| | (1) distinct cells at 25-34 | (2) employer changes per interview at 25-34 |
|---|---|---|
| **Pooled (weighted)** | | |
| entrant (ref. never in the father's cell) | -0.189 (0.339; p=0.578) | -0.131*** (0.038; p=<0.001) |
| stayer | -1.504*** (0.242; p=<0.001) | -0.018 (0.047; p=0.697) |
| 25-34 son-years / 10 | 3.755*** (0.177; p=<0.001) | -0.295*** (0.053; p=<0.001) |
| ln parental income | -0.137* (0.077; p=0.075) | -0.030* (0.017; p=0.071) |
| N sons / clusters | 2,035 / 1,082 | 1,795 / 1,000 |
| **Black** | | |
| entrant (ref. never in the father's cell) | 0.779* (0.426; p=0.068) | -0.114 (0.083; p=0.168) |
| stayer | -2.221*** (0.288; p=<0.001) | -0.146* (0.085; p=0.088) |
| 25-34 son-years / 10 | 3.970*** (0.258; p=<0.001) | -0.322*** (0.082; p=<0.001) |
| ln parental income | 0.138 (0.106; p=0.193) | -0.017 (0.033; p=0.616) |
| N sons / clusters | 505 / 277 | 423 / 246 |
| **White** | | |
| entrant (ref. never in the father's cell) | -0.264 (0.353; p=0.454) | -0.132*** (0.038; p=<0.001) |
| stayer | -1.479*** (0.243; p=<0.001) | -0.009 (0.048; p=0.847) |
| 25-34 son-years / 10 | 3.679*** (0.190; p=<0.001) | -0.287*** (0.054; p=<0.001) |
| ln parental income | -0.128 (0.080; p=0.106) | -0.039** (0.017; p=0.022) |
| N sons / clusters | 1,531 / 808 | 1,373 / 757 |
| **Black - White** | | |
| entrant (ref. never in the father's cell) | 1.043* (0.553; p=0.059) | 0.018 (0.091; p=0.842) |
| stayer | -0.741** (0.377; p=0.049) | -0.136 (0.098; p=0.164) |
| 25-34 son-years / 10 | 0.292 (0.320; p=0.363) | -0.035 (0.098; p=0.721) |
| ln parental income | 0.267** (0.133; p=0.044) | 0.022 (0.037; p=0.548) |

(PI) Where were sons at 25-34 relative to the father's cell? Modal 25-34 type for ALL sons in both windows (observed vs random matching of sons' 25-34 cells to fathers' cells within the row), and for the eventual entrants (in the father's cell at 35-55 but not modal at 25-34):

| Race / parental-income tercile | sons | same industry group, different occupation group: observed | benchmark | same occupation group, different industry group: observed | benchmark | different industry AND occupation: observed | benchmark | already in the father's cell: observed | benchmark | entrants (in at 35-55, not modal at 25-34): type a | type b | type c | entrants: mean share of 25-34 son-years in a / b / c / d |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Black + White, all | 2,036 | 0.071 | 0.021 | 0.029 | 0.020 | 0.868 | 0.956 | 0.031 | 0.003 | 27: 0.33 | 0.11 | 0.56 | 0.24 / 0.14 / 0.50 / 0.12 |
| Black, tercile 1 | 172 | 0.058 | 0.023 | 0.017 | 0.021 | 0.913 | 0.951 | 0.012 | 0.005 | 1: 0.00 | 0.00 | 1.00 | 0.00 / 0.00 / 0.67 / 0.33 |
| Black, tercile 2 | 222 | 0.045 | 0.020 | 0.023 | 0.018 | 0.910 | 0.958 | 0.023 | 0.003 | 4: 0.00 | 0.25 | 0.75 | 0.00 / 0.31 / 0.56 / 0.13 |
| Black, tercile 3 | 111 | 0.027 | 0.011 | 0.018 | 0.024 | 0.946 | 0.963 | 0.009 | 0.002 | 1: 0.00 | 0.00 | 1.00 | 0.00 / 0.25 / 0.75 / 0.00 |
| White, tercile 1 | 129 | 0.109 | 0.037 | 0.047 | 0.016 | 0.791 | 0.936 | 0.054 | 0.011 | 2: 0.50 | 0.00 | 0.50 | 0.20 / 0.05 / 0.41 / 0.34 |
| White, tercile 2 | 553 | 0.074 | 0.026 | 0.022 | 0.022 | 0.879 | 0.949 | 0.025 | 0.004 | 5: 0.00 | 0.20 | 0.80 | 0.07 / 0.20 / 0.64 / 0.09 |
| White, tercile 3 (rich White) | 849 | 0.079 | 0.020 | 0.038 | 0.029 | 0.842 | 0.947 | 0.041 | 0.004 | 14: 0.57 | 0.07 | 0.36 | 0.41 / 0.09 / 0.41 / 0.10 |
| Black, all | 505 | 0.046 | 0.017 | 0.020 | 0.019 | 0.919 | 0.960 | 0.016 | 0.003 | 6: 0.00 | 0.17 | 0.83 | 0.00 / 0.25 / 0.61 / 0.14 |
| White, all | 1,531 | 0.080 | 0.023 | 0.033 | 0.023 | 0.851 | 0.950 | 0.037 | 0.004 | 21: 0.43 | 0.10 | 0.48 | 0.31 / 0.11 / 0.46 / 0.12 |

(4) Within sons: son-year linear probability model of being in the father's cell on ln parental income x age with person FE (the age gradient is identified within sons, not across cohorts), year FE and a common after-35 shift. Positive = sons of richer parents move INTO the father's cell as they age.

| | (1) all sons with a father's cell: ln parental income x (age-40)/10 | (2) ... ln parental income x age >= 35 | (3) sons observed in both windows: x (age-40)/10 | (4) ... x age >= 35 |
|---|---|---|---|---|
| **Pooled (weighted)** | | | | |
| ln parental income x age term (within son) | 0.008 (0.006; p=0.154) | 0.011 (0.008; p=0.142) | 0.009 (0.006; p=0.150) | 0.011 (0.008; p=0.142) |
| Person FE, year FE, common after-35 shift; N son-years / sons / clusters | 29,575 / 3,171 / 1,387 | 29,575 / 3,171 / 1,387 | 25,583 / 2,035 / 1,082 | 25,583 / 2,035 / 1,082 |
| **Black** | | | | |
| ln parental income x age term (within son) | 0.001 (0.014; p=0.964) | -0.008 (0.012; p=0.517) | -0.004 (0.014; p=0.768) | -0.007 (0.012; p=0.579) |
| Person FE, year FE, common after-35 shift; N son-years / sons / clusters | 6,983 / 906 / 407 | 6,983 / 906 / 407 | 5,597 / 505 / 277 | 5,597 / 505 / 277 |
| **White** | | | | |
| ln parental income x age term (within son) | 0.009 (0.007; p=0.166) | 0.013* (0.008; p=0.099) | 0.010 (0.007; p=0.150) | 0.013 (0.008; p=0.101) |
| Person FE, year FE, common after-35 shift; N son-years / sons / clusters | 22,605 / 2,268 / 985 | 22,605 / 2,268 / 985 | 19,989 / 1,531 / 808 | 19,989 / 1,531 / 808 |
| **Black - White** | | | | |
| ln parental income x age term (within son) | -0.008 (0.015; p=0.574) | -0.021 (0.014; p=0.143) | -0.014 (0.015; p=0.373) | -0.020 (0.014; p=0.168) |

## E. NLSY79 replication

Men of the NLSY79 living with a parent in 1979 (32 Section 5): hourly wage, industry and occupation of the CPS (main) job at each round; early industry = modal industry group of the CPS job over the 25-34 rounds. Regressor ln mean parental income 1979-81; band controls quartic in age + birth-year FE; son-level controls as in A1; clusters 1979 household; pooled weighted by the 1979 weight. Cohorts 1957-64 are observed through 2022 (ages 58-65), so nearly every man observed at 25-34 is also observed after 40.

### 0N. Who is kept (NLSY79)

Fixing the industry at 25-34 requires a son to be observed at 25-34; growth after 35 requires him to be observed again later. This conditioning is necessary for the question, but it is not a balanced panel: every son-year of every son with an early industry is used in the band regressions. Shares and 25-34 characteristics (unweighted means; descriptive):

| Race | sons with a valid wage 25-55 | ... with valid 25-34 son-years | ... with an early industry | ... and observed at 35-55 | ... and observed at 40-55 | share of sons observed at 35-55 who have an early industry | share of son-years 35-55 kept | sons with >= 2 early industry years |
|---|---|---|---|---|---|---|---|---|
| Black + White | 2,966 | 2,894 | 2,893 | 2,622 | 2,462 | 0.973 | 0.981 | 2,811 |
| Black | 1,085 | 1,056 | 1,055 | 948 | 889 | 0.969 | 0.976 | 1,015 |
| White | 1,881 | 1,838 | 1,838 | 1,674 | 1,573 | 0.975 | 0.983 | 1,796 |

| Race | sample (sons) | N sons | mean ln wage at 25-34 | ln parental income | years of education | birth year | share early FLP industry (illustrative) | share early high-paid high-growth cell |
|---|---|---|---|---|---|---|---|---|
| Black + White | all sons with valid 25-34 son-years | 2,894 | 2.476 | 10.649 |  | 1961.1 | 0.063 | 0.121 |
| Black + White | with an early industry | 2,893 | 2.477 | 10.649 |  | 1961.1 | 0.063 | 0.121 |
| Black + White | with an early industry, observed at 35-55 | 2,622 | 2.483 | 10.657 |  | 1961.1 | 0.061 | 0.124 |
| Black + White | with an early industry, observed at 40-55 | 2,462 | 2.487 | 10.657 |  | 1961.1 | 0.062 | 0.125 |
| Black + White | with an early industry, NOT observed after 34 | 271 | 2.412 | 10.570 |  | 1961.0 | 0.081 | 0.096 |
| Black | all sons with valid 25-34 son-years | 1,056 | 2.300 | 10.201 |  | 1961.0 | 0.036 | 0.065 |
| Black | with an early industry | 1,055 | 2.301 | 10.202 |  | 1961.0 | 0.036 | 0.065 |
| Black | with an early industry, observed at 35-55 | 948 | 2.314 | 10.207 |  | 1961.1 | 0.034 | 0.065 |
| Black | with an early industry, observed at 40-55 | 889 | 2.317 | 10.209 |  | 1961.1 | 0.035 | 0.069 |
| Black | with an early industry, NOT observed after 34 | 107 | 2.182 | 10.153 |  | 1960.8 | 0.056 | 0.065 |
| White | all sons with valid 25-34 son-years | 1,838 | 2.577 | 10.906 |  | 1961.1 | 0.078 | 0.153 |
| White | with an early industry | 1,838 | 2.577 | 10.906 |  | 1961.1 | 0.078 | 0.153 |
| White | with an early industry, observed at 35-55 | 1,674 | 2.579 | 10.912 |  | 1961.1 | 0.076 | 0.157 |
| White | with an early industry, observed at 40-55 | 1,573 | 2.583 | 10.911 |  | 1961.1 | 0.077 | 0.157 |
| White | with an early industry, NOT observed after 34 | 164 | 2.562 | 10.841 |  | 1961.1 | 0.098 | 0.116 |

## HN. Headline: nonlinear industry and occupation x industry cell profiles (NLSY79)

Each row is a piece of the son's ln wage regressed on ln parental income by age band (stacked; controls as in the band regressions); the columns are the change of that coefficient across age bands and its share of the change for ln wage, pooled and for the Black-White gap. 'Linear' = 32's P_j + B_j t; 'nonlinear band profile' = the son's industry's (cell's) relative wage in his five-year age band (CPS MORG), split into its age-weighted level and the age profile around it; 'piecewise' = the knots-30/35/45 profile. The profile rows are the like-for-like comparison with the linear slope (all are the career-growth component of the industry / cell). 'At 25-34' = the industry or cell fixed at the son's modal code at 25-34, evaluated at his current age (payoff of where he started, wherever he works later). Shares blank when the denominator is not different from zero.

| | (1) pooled change (35-55)-(25-34) | (2) share of the ln wage change | (3) change of the B-W gap (35-55)-(25-34) | (4) share | (5) pooled change (45-55)-(25-34) | (6) share | (7) B-W change (45-55)-(25-34) | (8) share |
|---|---|---|---|---|---|---|---|---|
| **A. 32's decomposition sample (current industry and occupation mapped): replication of the linear B and the nonlinear profile** | | | | | | | | |
| ln wage (total) | 0.109*** (0.017; p=<0.001) |  | -0.056** (0.027; p=0.040) |  | 0.127*** (0.022; p=<0.001) |  | -0.055 (0.036; p=0.132) |  |
| current industry, LINEAR (32): level P | 0.005 (0.006; p=0.412) | 0.043 (0.051; p=0.400) | -0.012 (0.011; p=0.277) | 0.217 (0.195; p=0.266) | 0.005 (0.008; p=0.528) | 0.040 (0.062; p=0.517) | -0.020 (0.015; p=0.182) |  |
| current industry, LINEAR (32): slope B x t | 0.011*** (0.001; p=<0.001) | 0.097*** (0.017; p=<0.001) | -0.004 (0.002; p=0.110) | 0.072 (0.050; p=0.153) | 0.014*** (0.002; p=<0.001) | 0.110*** (0.022; p=<0.001) | -0.006 (0.004; p=0.120) |  |
| current industry, NONLINEAR band profile: level | 0.005 (0.006; p=0.417) | 0.042 (0.051; p=0.405) | -0.012 (0.011; p=0.289) | 0.212 (0.194; p=0.277) | 0.005 (0.008; p=0.538) | 0.039 (0.062; p=0.528) | -0.020 (0.015; p=0.189) |  |
| current industry, NONLINEAR band profile: age profile Q(band) - level | 0.016*** (0.002; p=<0.001) | 0.144*** (0.024; p=<0.001) | -0.005* (0.003; p=0.090) | 0.094 (0.063; p=0.136) | 0.016*** (0.002; p=<0.001) | 0.123*** (0.025; p=<0.001) | -0.005 (0.004; p=0.218) |  |
| current industry, NONLINEAR band profile: total | 0.020*** (0.006; p=<0.001) | 0.186*** (0.054; p=<0.001) | -0.017 (0.012; p=0.153) | 0.305 (0.214; p=0.153) | 0.021** (0.009; p=0.019) | 0.162** (0.067; p=0.015) | -0.025 (0.017; p=0.136) |  |
| current industry, piecewise (knots 30/35/45): age profile | 0.016*** (0.002; p=<0.001) | 0.144*** (0.024; p=<0.001) | -0.006* (0.003; p=0.061) | 0.102 (0.065; p=0.114) | 0.016*** (0.002; p=<0.001) | 0.125*** (0.025; p=<0.001) | -0.005 (0.004; p=0.181) |  |
| N son-years / sons (pooled) | 25-34: 21,707 / 2,892 ; 35-44: 10,817 / 2,614 ; 45-55: 9,455 / 2,243 |  |  |  |  |  |  |  |
| **B. Common sample (also early industry and early cell): current vs early, industry vs cell, linear vs nonlinear** | | | | | | | | |
| ln wage (total) | 0.110*** (0.017; p=<0.001) |  | -0.057** (0.027; p=0.035) |  | 0.129*** (0.023; p=<0.001) |  | -0.057 (0.037; p=0.121) |  |
| current industry, LINEAR slope B x t (32) | 0.011*** (0.001; p=<0.001) | 0.096*** (0.017; p=<0.001) | -0.004 (0.002; p=0.137) | 0.065 (0.047; p=0.170) | 0.014*** (0.002; p=<0.001) | 0.108*** (0.022; p=<0.001) | -0.005 (0.004; p=0.165) |  |
| current industry, NONLINEAR band profile | 0.016*** (0.002; p=<0.001) | 0.142*** (0.023; p=<0.001) | -0.005 (0.003; p=0.114) | 0.085 (0.059; p=0.150) | 0.015*** (0.002; p=<0.001) | 0.120*** (0.025; p=<0.001) | -0.004 (0.004; p=0.305) |  |
| current industry, piecewise (30/35/45) profile | 0.016*** (0.002; p=<0.001) | 0.142*** (0.023; p=<0.001) | -0.005* (0.003; p=0.079) | 0.093 (0.060; p=0.123) | 0.016*** (0.002; p=<0.001) | 0.122*** (0.024; p=<0.001) | -0.005 (0.004; p=0.258) |  |
| current industry, band level + profile | 0.022*** (0.006; p=<0.001) | 0.195*** (0.054; p=<0.001) | -0.017 (0.012; p=0.148) | 0.300 (0.208; p=0.149) | 0.022** (0.009; p=0.011) | 0.174*** (0.067; p=0.009) | -0.025 (0.017; p=0.145) |  |
| industry at 25-34, LINEAR slope B x t | 0.012*** (0.002; p=<0.001) | 0.106*** (0.022; p=<0.001) | -0.003 (0.003; p=0.317) | 0.061 (0.063; p=0.333) | 0.016*** (0.003; p=<0.001) | 0.122*** (0.029; p=<0.001) | -0.005 (0.005; p=0.294) |  |
| industry at 25-34, band level | -0.006* (0.003; p=0.098) | -0.052 (0.033; p=0.117) | -0.003 (0.007; p=0.631) | 0.060 (0.123; p=0.622) | -0.008* (0.005; p=0.086) | -0.066 (0.041; p=0.111) | -0.001 (0.010; p=0.921) |  |
| industry at 25-34, NONLINEAR band profile | 0.016*** (0.002; p=<0.001) | 0.148*** (0.028; p=<0.001) | -0.003 (0.004; p=0.539) | 0.046 (0.074; p=0.533) | 0.018*** (0.003; p=<0.001) | 0.139*** (0.032; p=<0.001) | -0.004 (0.006; p=0.468) |  |
| industry at 25-34, piecewise (30/35/45) profile | 0.017*** (0.002; p=<0.001) | 0.155*** (0.029; p=<0.001) | -0.003 (0.004; p=0.419) | 0.060 (0.075; p=0.421) | 0.018*** (0.003; p=<0.001) | 0.143*** (0.032; p=<0.001) | -0.005 (0.005; p=0.368) |  |
| industry at 25-34, synthetic-cohort slope after 35 x s2 | -0.003 (0.002; p=0.185) | -0.025 (0.019; p=0.195) | -0.006 (0.004; p=0.177) | 0.097 (0.087; p=0.262) | -0.004 (0.004; p=0.222) | -0.034 (0.028; p=0.233) | -0.010 (0.007; p=0.170) |  |
| industry at 25-34, band level + profile | 0.011** (0.004; p=0.016) | 0.096** (0.040; p=0.016) | -0.006 (0.009; p=0.482) | 0.107 (0.146; p=0.465) | 0.010 (0.006; p=0.121) | 0.074 (0.047; p=0.119) | -0.005 (0.012; p=0.676) |  |
| current CELL (occupation group x industry group), band level | 0.001 (0.007; p=0.910) | 0.007 (0.061; p=0.910) | 0.007 (0.013; p=0.612) | -0.116 (0.249; p=0.642) | -0.006 (0.009; p=0.506) | -0.049 (0.075; p=0.515) | 0.012 (0.018; p=0.503) |  |
| current CELL, NONLINEAR band profile | 0.030*** (0.002; p=<0.001) | 0.276*** (0.039; p=<0.001) | -0.012*** (0.004; p=0.003) | 0.207** (0.100; p=0.039) | 0.032*** (0.003; p=<0.001) | 0.250*** (0.041; p=<0.001) | -0.013** (0.005; p=0.011) |  |
| current occupation group (11), NONLINEAR band profile (occupation only) | 0.025*** (0.002; p=<0.001) | 0.223*** (0.031; p=<0.001) | -0.010*** (0.003; p=<0.001) | 0.178** (0.084; p=0.033) | 0.025*** (0.002; p=<0.001) | 0.197*** (0.032; p=<0.001) | -0.010*** (0.003; p=0.001) |  |
| current cell profile minus occupation-group profile (what industry adds within the cell) | 0.006*** (0.001; p=<0.001) | 0.053*** (0.012; p=<0.001) | -0.002 (0.002; p=0.474) | 0.028 (0.040; p=0.473) | 0.007*** (0.002; p=<0.001) | 0.053*** (0.015; p=<0.001) | -0.003 (0.003; p=0.436) |  |
| current CELL, level + profile | 0.031*** (0.007; p=<0.001) | 0.283*** (0.068; p=<0.001) | -0.005 (0.014; p=0.702) | 0.091 (0.226; p=0.687) | 0.026** (0.010; p=0.011) | 0.201** (0.079; p=0.011) | -0.001 (0.019; p=0.956) |  |
| within current cell (ln wage - cell level - cell profile) | 0.079*** (0.017; p=<0.001) | 0.717*** (0.068; p=<0.001) | -0.052** (0.026; p=0.042) | 0.909*** (0.226; p=<0.001) | 0.103*** (0.023; p=<0.001) | 0.799*** (0.079; p=<0.001) | -0.056 (0.036; p=0.117) |  |
| cell at 25-34, band level | -0.003 (0.004; p=0.560) | -0.023 (0.041; p=0.571) | 0.002 (0.009; p=0.786) | -0.040 (0.156; p=0.796) | -0.005 (0.006; p=0.436) | -0.039 (0.052; p=0.457) | 0.005 (0.012; p=0.678) |  |
| cell at 25-34, NONLINEAR band profile | 0.033*** (0.003; p=<0.001) | 0.299*** (0.043; p=<0.001) | -0.012** (0.006; p=0.025) | 0.216* (0.119; p=0.070) | 0.038*** (0.004; p=<0.001) | 0.292*** (0.049; p=<0.001) | -0.012* (0.007; p=0.081) |  |
| occupation group at 25-34, NONLINEAR band profile (occupation only) | 0.026*** (0.002; p=<0.001) | 0.238*** (0.034; p=<0.001) | -0.013*** (0.004; p=0.001) | 0.219** (0.106; p=0.039) | 0.028*** (0.003; p=<0.001) | 0.217*** (0.036; p=<0.001) | -0.013*** (0.004; p=0.005) |  |
| cell at 25-34 profile minus occupation-group profile (what industry adds) | 0.007*** (0.002; p=<0.001) | 0.061*** (0.017; p=<0.001) | 0.000 (0.003; p=0.961) | -0.003 (0.059; p=0.961) | 0.010*** (0.002; p=<0.001) | 0.074*** (0.020; p=<0.001) | 0.001 (0.004; p=0.819) |  |
| cell at 25-34, level + profile | 0.030*** (0.006; p=<0.001) | 0.275*** (0.052; p=<0.001) | -0.010 (0.011; p=0.347) | 0.176 (0.172; p=0.307) | 0.033*** (0.008; p=<0.001) | 0.253*** (0.061; p=<0.001) | -0.007 (0.015; p=0.651) |  |
| N son-years / sons (pooled) | 25-34: 21,707 / 2,892 ; 35-44: 10,679 / 2,560 ; 45-55: 9,185 / 2,179 |  |  |  |  |  |  |  |

### A1N. Wage growth after 35 by where the son was at 25-34 (NLSY79)

Son-level regressions (outcome in the column header; one row per son observed at 25-34 and in the later window). Regressors: the son's EARLY occupation x industry cell (modal at 25-34) classified by the data-defined sets of Section D (reference = cells neither high-paid nor high later growth); column (5) the same sets defined on industry groups; column (6) the pre-chosen illustrative industries only. Controls: mean age in each window, birth-year quadratic.

| | (1) Delta ln wage (40-55) - (25-34): early cell sets | (2) ... + ln parental income, Black, education | (3) Delta ln wage (35-55) - (25-34): early cell sets | (4) Delta ln wage (45-55) - (25-34): early cell sets | (5) Delta (40-55) - (25-34): early industry sets | (6) illustrative: early finance / insurance / legal / professional |
|---|---|---|---|---|---|---|
| **Pooled (weighted)** | | | | | | |
| early cell high-paid AND high later growth | 0.330*** (0.034; p=<0.001) | 0.299*** (0.033; p=<0.001) | 0.292*** (0.029; p=<0.001) | 0.345*** (0.038; p=<0.001) |  |  |
| early cell high-paid only | 0.266*** (0.047; p=<0.001) | 0.230*** (0.047; p=<0.001) | 0.267*** (0.037; p=<0.001) | 0.275*** (0.054; p=<0.001) |  |  |
| early cell high later growth only | 0.079** (0.034; p=0.020) | 0.072** (0.034; p=0.036) | 0.078*** (0.028; p=0.005) | 0.090** (0.038; p=0.020) |  |  |
| early industry high-paid AND high later growth |  |  |  |  | 0.176*** (0.034; p=<0.001) |  |
| early industry high-paid only |  |  |  |  | 0.112*** (0.036; p=0.002) |  |
| early industry high later growth only |  |  |  |  | 0.044 (0.036; p=0.218) |  |
| illustrative: early finance / insurance / legal / professional |  |  |  |  |  | 0.273*** (0.052; p=<0.001) |
| ln parental income |  | 0.079*** (0.018; p=<0.001) |  |  |  |  |
| Black |  | -0.054** (0.022; p=0.012) |  |  |  |  |
| Mean of outcome (all sons) | 0.288 | 0.288 | 0.260 | 0.296 | 0.287 | 0.287 |
| N sons / clusters | 2,461 / 2,011 | 2,461 / 2,011 | 2,621 / 2,115 | 2,284 / 1,888 | 2,462 / 2,011 | 2,462 / 2,011 |
| Sons with Delta(40-55) by early cell set: HH ; high-paid only ; high growth only ; neither | 308 ; 193 ; 192 ; 1768 |  |  |  | 237 ; 274 ; 272 ; 1679 | 152 |
| **Black** | | | | | | |
| early cell high-paid AND high later growth | 0.271*** (0.064; p=<0.001) | 0.251*** (0.065; p=<0.001) | 0.251*** (0.052; p=<0.001) | 0.323*** (0.063; p=<0.001) |  |  |
| early cell high-paid only | 0.215** (0.086; p=0.012) | 0.202** (0.085; p=0.018) | 0.206*** (0.075; p=0.006) | 0.229** (0.093; p=0.013) |  |  |
| early cell high later growth only | 0.074 (0.053; p=0.165) | 0.064 (0.053; p=0.231) | 0.064 (0.045; p=0.156) | 0.076 (0.060; p=0.203) |  |  |
| early industry high-paid AND high later growth |  |  |  |  | 0.154*** (0.046; p=<0.001) |  |
| early industry high-paid only |  |  |  |  | 0.089* (0.051; p=0.078) |  |
| early industry high later growth only |  |  |  |  | 0.069* (0.042; p=0.099) |  |
| illustrative: early finance / insurance / legal / professional |  |  |  |  |  | 0.080 (0.084; p=0.337) |
| ln parental income |  | 0.047*** (0.018; p=0.009) |  |  |  |  |
| Mean of outcome (all sons) | 0.146 | 0.146 | 0.136 | 0.147 | 0.146 | 0.146 |
| N sons / clusters | 889 / 705 | 889 / 705 | 948 / 742 | 815 / 656 | 889 / 705 | 889 / 705 |
| Sons with Delta(40-55) by early cell set: HH ; high-paid only ; high growth only ; neither | 61 ; 22 ; 76 ; 730 |  |  |  | 87 ; 75 ; 107 ; 620 | 31 |
| **White** | | | | | | |
| early cell high-paid AND high later growth | 0.309*** (0.035; p=<0.001) | 0.287*** (0.035; p=<0.001) | 0.274*** (0.030; p=<0.001) | 0.315*** (0.040; p=<0.001) |  |  |
| early cell high-paid only | 0.263*** (0.045; p=<0.001) | 0.237*** (0.045; p=<0.001) | 0.260*** (0.036; p=<0.001) | 0.273*** (0.052; p=<0.001) |  |  |
| early cell high later growth only | 0.080** (0.039; p=0.038) | 0.075* (0.039; p=0.054) | 0.075** (0.032; p=0.017) | 0.096** (0.044; p=0.028) |  |  |
| early industry high-paid AND high later growth |  |  |  |  | 0.191*** (0.038; p=<0.001) |  |
| early industry high-paid only |  |  |  |  | 0.133*** (0.037; p=<0.001) |  |
| early industry high later growth only |  |  |  |  | 0.029 (0.038; p=0.438) |  |
| illustrative: early finance / insurance / legal / professional |  |  |  |  |  | 0.303*** (0.052; p=<0.001) |
| ln parental income |  | 0.083*** (0.020; p=<0.001) |  |  |  |  |
| Mean of outcome (all sons) | 0.301 | 0.301 | 0.274 | 0.307 | 0.300 | 0.300 |
| N sons / clusters | 1,572 / 1,306 | 1,572 / 1,306 | 1,673 / 1,373 | 1,469 / 1,232 | 1,573 / 1,306 | 1,573 / 1,306 |
| Sons with Delta(40-55) by early cell set: HH ; high-paid only ; high growth only ; neither | 247 ; 171 ; 116 ; 1038 |  |  |  | 150 ; 199 ; 165 ; 1059 | 121 |
| **Black - White** | | | | | | |
| early cell high-paid AND high later growth | -0.038 (0.073; p=0.603) | -0.035 (0.073; p=0.632) | -0.023 (0.060; p=0.701) | 0.008 (0.075; p=0.918) |  |  |
| early cell high-paid only | -0.048 (0.097; p=0.620) | -0.035 (0.097; p=0.718) | -0.055 (0.083; p=0.511) | -0.044 (0.106; p=0.680) |  |  |
| early cell high later growth only | -0.006 (0.066; p=0.922) | -0.011 (0.066; p=0.867) | -0.011 (0.055; p=0.839) | -0.020 (0.074; p=0.785) |  |  |
| early industry high-paid AND high later growth |  |  |  |  | -0.036 (0.059; p=0.542) |  |
| early industry high-paid only |  |  |  |  | -0.044 (0.063; p=0.485) |  |
| early industry high later growth only |  |  |  |  | 0.040 (0.057; p=0.479) |  |
| illustrative: early finance / insurance / legal / professional |  |  |  |  |  | -0.222** (0.099; p=0.024) |
| ln parental income |  | -0.036 (0.027; p=0.184) |  |  |  |  |

### A3N. Within-person wage growth before and after 35 by early set (NLSY79)

Son-year regressions of ln wage on person fixed effects, year fixed effects, a common kink at 35 and the early-set indicators interacted with the piecewise age terms (s1 = min(age-35,0)/10, s2 = max(age-35,0)/10). Coefficients = slope differences (log points per 10 years) relative to sons whose early cell / industry is in neither set (column 3: relative to all other industries). Person FE remove cohort and level differences; with person and year FE the common linear age slope is not identified, the differences are. Ages 25-55, all son-years of sons with an early cell.

| | (1) ln wage, person FE: early cell sets | (2) ln wage, person FE: early industry sets | (3) illustrative: early finance / insurance / legal / professional |
|---|---|---|---|
| **Pooled (weighted)** | | | |
| early cell high-paid AND high later growth x slope 25-35 (per 10 yrs) | 0.289*** (0.036; p=<0.001) |  |  |
| early cell high-paid AND high later growth x slope 35-55 (per 10 yrs) | 0.111*** (0.022; p=<0.001) |  |  |
| early cell high-paid AND high later growth x acceleration = slope 35-55 - slope 25-35 | -0.178*** (0.046; p=<0.001) |  |  |
| early cell high-paid only x slope 25-35 (per 10 yrs) | 0.350*** (0.042; p=<0.001) |  |  |
| early cell high-paid only x slope 35-55 (per 10 yrs) | 0.054* (0.029; p=0.066) |  |  |
| early cell high-paid only x acceleration = slope 35-55 - slope 25-35 | -0.296*** (0.057; p=<0.001) |  |  |
| early cell high later growth only x slope 25-35 (per 10 yrs) | 0.089** (0.035; p=0.011) |  |  |
| early cell high later growth only x slope 35-55 (per 10 yrs) | 0.035 (0.023; p=0.132) |  |  |
| early cell high later growth only x acceleration = slope 35-55 - slope 25-35 | -0.054 (0.045; p=0.234) |  |  |
| early industry high-paid AND high later growth x slope 25-35 (per 10 yrs) |  | 0.213*** (0.034; p=<0.001) |  |
| early industry high-paid AND high later growth x slope 35-55 (per 10 yrs) |  | 0.038* (0.023; p=0.092) |  |
| early industry high-paid AND high later growth x acceleration = slope 35-55 - slope 25-35 |  | -0.175*** (0.045; p=<0.001) |  |
| early industry high-paid only x slope 25-35 (per 10 yrs) |  | 0.185*** (0.039; p=<0.001) |  |
| early industry high-paid only x slope 35-55 (per 10 yrs) |  | -0.009 (0.023; p=0.705) |  |
| early industry high-paid only x acceleration = slope 35-55 - slope 25-35 |  | -0.194*** (0.049; p=<0.001) |  |
| early industry high later growth only x slope 25-35 (per 10 yrs) |  | 0.067** (0.033; p=0.043) |  |
| early industry high later growth only x slope 35-55 (per 10 yrs) |  | 0.017 (0.025; p=0.506) |  |
| early industry high later growth only x acceleration = slope 35-55 - slope 25-35 |  | -0.051 (0.047; p=0.277) |  |
| early illustrative finance / insurance / legal / professional x slope 25-35 (per 10 yrs) |  |  | 0.342*** (0.050; p=<0.001) |
| early illustrative finance / insurance / legal / professional x slope 35-55 (per 10 yrs) |  |  | 0.053 (0.033; p=0.113) |
| early illustrative finance / insurance / legal / professional x acceleration = slope 35-55 - slope 25-35 |  |  | -0.290*** (0.067; p=<0.001) |
| Person FE, year FE, common kink at 35; N son-years / sons / clusters | 42,718 / 2,892 / 2,306 | 42,718 / 2,892 / 2,306 | 42,718 / 2,892 / 2,306 |
| **Black** | | | |
| early cell high-paid AND high later growth x slope 25-35 (per 10 yrs) | 0.286*** (0.064; p=<0.001) |  |  |
| early cell high-paid AND high later growth x slope 35-55 (per 10 yrs) | 0.117*** (0.039; p=0.003) |  |  |
| early cell high-paid AND high later growth x acceleration = slope 35-55 - slope 25-35 | -0.169** (0.081; p=0.037) |  |  |
| early cell high-paid only x slope 25-35 (per 10 yrs) | 0.124* (0.070; p=0.076) |  |  |
| early cell high-paid only x slope 35-55 (per 10 yrs) | 0.095* (0.055; p=0.084) |  |  |
| early cell high-paid only x acceleration = slope 35-55 - slope 25-35 | -0.029 (0.101; p=0.776) |  |  |
| early cell high later growth only x slope 25-35 (per 10 yrs) | 0.129** (0.057; p=0.024) |  |  |
| early cell high later growth only x slope 35-55 (per 10 yrs) | 0.005 (0.035; p=0.875) |  |  |
| early cell high later growth only x acceleration = slope 35-55 - slope 25-35 | -0.124* (0.069; p=0.072) |  |  |
| early industry high-paid AND high later growth x slope 25-35 (per 10 yrs) |  | 0.128** (0.052; p=0.014) |  |
| early industry high-paid AND high later growth x slope 35-55 (per 10 yrs) |  | 0.067** (0.032; p=0.035) |  |
| early industry high-paid AND high later growth x acceleration = slope 35-55 - slope 25-35 |  | -0.061 (0.066; p=0.360) |  |
| early industry high-paid only x slope 25-35 (per 10 yrs) |  | 0.113* (0.064; p=0.074) |  |
| early industry high-paid only x slope 35-55 (per 10 yrs) |  | -0.005 (0.036; p=0.899) |  |
| early industry high-paid only x acceleration = slope 35-55 - slope 25-35 |  | -0.118 (0.082; p=0.150) |  |
| early industry high later growth only x slope 25-35 (per 10 yrs) |  | 0.034 (0.044; p=0.443) |  |
| early industry high later growth only x slope 35-55 (per 10 yrs) |  | 0.070** (0.030; p=0.020) |  |
| early industry high later growth only x acceleration = slope 35-55 - slope 25-35 |  | 0.036 (0.059; p=0.539) |  |
| early illustrative finance / insurance / legal / professional x slope 25-35 (per 10 yrs) |  |  | 0.182** (0.072; p=0.012) |
| early illustrative finance / insurance / legal / professional x slope 35-55 (per 10 yrs) |  |  | -0.055 (0.056; p=0.322) |
| early illustrative finance / insurance / legal / professional x acceleration = slope 35-55 - slope 25-35 |  |  | -0.237** (0.099; p=0.017) |
| Person FE, year FE, common kink at 35; N son-years / sons / clusters | 14,614 / 1,055 / 812 | 14,614 / 1,055 / 812 | 14,614 / 1,055 / 812 |
| **White** | | | |
| early cell high-paid AND high later growth x slope 25-35 (per 10 yrs) | 0.270*** (0.037; p=<0.001) |  |  |
| early cell high-paid AND high later growth x slope 35-55 (per 10 yrs) | 0.099*** (0.023; p=<0.001) |  |  |
| early cell high-paid AND high later growth x acceleration = slope 35-55 - slope 25-35 | -0.171*** (0.047; p=<0.001) |  |  |
| early cell high-paid only x slope 25-35 (per 10 yrs) | 0.340*** (0.043; p=<0.001) |  |  |
| early cell high-paid only x slope 35-55 (per 10 yrs) | 0.055* (0.029; p=0.056) |  |  |
| early cell high-paid only x acceleration = slope 35-55 - slope 25-35 | -0.284*** (0.057; p=<0.001) |  |  |
| early cell high later growth only x slope 25-35 (per 10 yrs) | 0.063 (0.041; p=0.123) |  |  |
| early cell high later growth only x slope 35-55 (per 10 yrs) | 0.046* (0.027; p=0.082) |  |  |
| early cell high later growth only x acceleration = slope 35-55 - slope 25-35 | -0.017 (0.054; p=0.747) |  |  |
| early industry high-paid AND high later growth x slope 25-35 (per 10 yrs) |  | 0.233*** (0.037; p=<0.001) |  |
| early industry high-paid AND high later growth x slope 35-55 (per 10 yrs) |  | 0.045* (0.024; p=0.063) |  |
| early industry high-paid AND high later growth x acceleration = slope 35-55 - slope 25-35 |  | -0.188*** (0.049; p=<0.001) |  |
| early industry high-paid only x slope 25-35 (per 10 yrs) |  | 0.195*** (0.042; p=<0.001) |  |
| early industry high-paid only x slope 35-55 (per 10 yrs) |  | 0.008 (0.024; p=0.744) |  |
| early industry high-paid only x acceleration = slope 35-55 - slope 25-35 |  | -0.187*** (0.052; p=<0.001) |  |
| early industry high later growth only x slope 25-35 (per 10 yrs) |  | 0.062* (0.036; p=0.084) |  |
| early industry high later growth only x slope 35-55 (per 10 yrs) |  | 0.007 (0.027; p=0.810) |  |
| early industry high later growth only x acceleration = slope 35-55 - slope 25-35 |  | -0.055 (0.051; p=0.281) |  |
| early illustrative finance / insurance / legal / professional x slope 25-35 (per 10 yrs) |  |  | 0.352*** (0.053; p=<0.001) |
| early illustrative finance / insurance / legal / professional x slope 35-55 (per 10 yrs) |  |  | 0.073** (0.033; p=0.025) |
| early illustrative finance / insurance / legal / professional x acceleration = slope 35-55 - slope 25-35 |  |  | -0.279*** (0.069; p=<0.001) |
| Person FE, year FE, common kink at 35; N son-years / sons / clusters | 28,104 / 1,837 / 1,494 | 28,104 / 1,837 / 1,494 | 28,104 / 1,837 / 1,494 |
| **Black - White** | | | |
| early cell high-paid AND high later growth x slope 25-35 (per 10 yrs) | 0.016 (0.074; p=0.828) |  |  |
| early cell high-paid AND high later growth x slope 35-55 (per 10 yrs) | 0.017 (0.045; p=0.701) |  |  |
| early cell high-paid AND high later growth x acceleration = slope 35-55 - slope 25-35 | 0.001 (0.094; p=0.989) |  |  |
| early cell high-paid only x slope 25-35 (per 10 yrs) | -0.216*** (0.082; p=0.008) |  |  |
| early cell high-paid only x slope 35-55 (per 10 yrs) | 0.040 (0.062; p=0.524) |  |  |
| early cell high-paid only x acceleration = slope 35-55 - slope 25-35 | 0.255** (0.116; p=0.028) |  |  |
| early cell high later growth only x slope 25-35 (per 10 yrs) | 0.066 (0.071; p=0.352) |  |  |
| early cell high later growth only x slope 35-55 (per 10 yrs) | -0.041 (0.044; p=0.350) |  |  |
| early cell high later growth only x acceleration = slope 35-55 - slope 25-35 | -0.106 (0.087; p=0.223) |  |  |
| early industry high-paid AND high later growth x slope 25-35 (per 10 yrs) |  | -0.105* (0.064; p=0.099) |  |
| early industry high-paid AND high later growth x slope 35-55 (per 10 yrs) |  | 0.023 (0.040; p=0.572) |  |
| early industry high-paid AND high later growth x acceleration = slope 35-55 - slope 25-35 |  | 0.128 (0.082; p=0.121) |  |
| early industry high-paid only x slope 25-35 (per 10 yrs) |  | -0.081 (0.076; p=0.286) |  |
| early industry high-paid only x slope 35-55 (per 10 yrs) |  | -0.013 (0.044; p=0.774) |  |
| early industry high-paid only x acceleration = slope 35-55 - slope 25-35 |  | 0.069 (0.097; p=0.481) |  |
| early industry high later growth only x slope 25-35 (per 10 yrs) |  | -0.028 (0.057; p=0.621) |  |
| early industry high later growth only x slope 35-55 (per 10 yrs) |  | 0.064 (0.041; p=0.119) |  |
| early industry high later growth only x acceleration = slope 35-55 - slope 25-35 |  | 0.092 (0.078; p=0.242) |  |
| early illustrative finance / insurance / legal / professional x slope 25-35 (per 10 yrs) |  |  | -0.170* (0.089; p=0.056) |
| early illustrative finance / insurance / legal / professional x slope 35-55 (per 10 yrs) |  |  | -0.129** (0.065; p=0.047) |
| early illustrative finance / insurance / legal / professional x acceleration = slope 35-55 - slope 25-35 |  |  | 0.041 (0.121; p=0.731) |

### A2N. Gelbach with early industry / cell x band FE (NLSY79)

| | (1) accounted for at 25-34 (short - long) | (2) accounted for at 35-55 | (3) change (35-55)-(25-34) of the part accounted for | (4) rise of the coefficient on this sample (short) | (5) share = (3)/(4) | (6) B-W: change of the part accounted for | (7) change of the B-W gap (short) | (8) share = (6)/(7) | (9) pooled: change (45-55)-(25-34) of the part accounted for | (10) its share |
|---|---|---|---|---|---|---|---|---|---|---|
| **Long regression adds (fixed effects estimated separately in each band and race sample)** | | | | | | | | | | |
| early cell set, data-defined [4 cells] | 0.048*** (0.005; p=<0.001) | 0.088*** (0.010; p=<0.001) | 0.040*** (0.006; p=<0.001) | 0.110*** (0.017; p=<0.001) | 0.361*** (0.061; p=<0.001) | -0.017* (0.010; p=0.085) | -0.055** (0.027; p=0.040) | 0.311 (0.194; p=0.109) | 0.045*** (0.008; p=<0.001) | 0.344*** (0.066; p=<0.001) |
| early industry set, data-defined [4 cells] | 0.015*** (0.003; p=<0.001) | 0.019*** (0.005; p=<0.001) | 0.004 (0.003; p=0.106) | 0.111*** (0.017; p=<0.001) | 0.040 (0.025; p=0.111) | -0.001 (0.006; p=0.873) | -0.055** (0.027; p=0.039) | 0.017 (0.107; p=0.872) | 0.005 (0.004; p=0.148) | 0.039 (0.027; p=0.151) |
| early industry group (33) [33 cells] | 0.035*** (0.006; p=<0.001) | 0.054*** (0.008; p=<0.001) | 0.019*** (0.006; p=<0.001) | 0.111*** (0.017; p=<0.001) | 0.173*** (0.051; p=<0.001) | -0.008 (0.011; p=0.455) | -0.055** (0.027; p=0.039) | 0.149 (0.193; p=0.441) | 0.020*** (0.007; p=0.007) | 0.150*** (0.054; p=0.006) |
| early fine industry (ind1990ddx) [180 cells] | 0.050*** (0.007; p=<0.001) | 0.080*** (0.012; p=<0.001) | 0.029*** (0.010; p=0.002) | 0.111*** (0.017; p=<0.001) | 0.263*** (0.076; p=<0.001) | -0.005 (0.016; p=0.747) | -0.055** (0.027; p=0.039) | 0.096 (0.284; p=0.734) | 0.039*** (0.013; p=0.003) | 0.299*** (0.089; p=<0.001) |
| early special cell [5 cells] | 0.034*** (0.004; p=<0.001) | 0.060*** (0.008; p=<0.001) | 0.026*** (0.005; p=<0.001) | 0.111*** (0.017; p=<0.001) | 0.236*** (0.051; p=<0.001) | 0.001 (0.009; p=0.940) | -0.055** (0.027; p=0.039) | -0.012 (0.166; p=0.940) | 0.032*** (0.007; p=<0.001) | 0.242*** (0.059; p=<0.001) |
| early cell: occupation group x industry group [257 cells] | 0.078*** (0.009; p=<0.001) | 0.134*** (0.014; p=<0.001) | 0.057*** (0.010; p=<0.001) | 0.110*** (0.017; p=<0.001) | 0.513*** (0.091; p=<0.001) | -0.019 (0.018; p=0.283) | -0.055** (0.027; p=0.040) | 0.346 (0.311; p=0.266) | 0.068*** (0.013; p=<0.001) | 0.515*** (0.104; p=<0.001) |
| early occupation group (11) only [11 cells] | 0.056*** (0.006; p=<0.001) | 0.106*** (0.010; p=<0.001) | 0.050*** (0.007; p=<0.001) | 0.110*** (0.017; p=<0.001) | 0.454*** (0.070; p=<0.001) | -0.026** (0.011; p=0.020) | -0.055** (0.027; p=0.040) | 0.468* (0.241; p=0.052) | 0.057*** (0.009; p=<0.001) | 0.436*** (0.077; p=<0.001) |
| early occupation group + early industry group, additive [11 + 33 cells] | 0.075*** (0.008; p=<0.001) | 0.123*** (0.012; p=<0.001) | 0.048*** (0.008; p=<0.001) | 0.110*** (0.017; p=<0.001) | 0.433*** (0.072; p=<0.001) | -0.018 (0.013; p=0.170) | -0.055** (0.027; p=0.040) | 0.334 (0.236; p=0.157) | 0.054*** (0.010; p=<0.001) | 0.414*** (0.079; p=<0.001) |
| current industry group, any age profile [33 cells] | 0.030*** (0.005; p=<0.001) | 0.043*** (0.007; p=<0.001) | 0.013** (0.006; p=0.031) | 0.109*** (0.017; p=<0.001) | 0.122** (0.056; p=0.029) | -0.009 (0.012; p=0.443) | -0.053* (0.027; p=0.050) |  | 0.015* (0.009; p=0.096) | 0.116* (0.068; p=0.088) |
| current cell, any age profile [354 cells] | 0.075*** (0.007; p=<0.001) | 0.124*** (0.012; p=<0.001) | 0.049*** (0.010; p=<0.001) | 0.110*** (0.017; p=<0.001) | 0.445*** (0.088; p=<0.001) | -0.023 (0.017; p=0.185) | -0.057** (0.027; p=0.034) | 0.396 (0.271; p=0.143) | 0.053*** (0.015; p=<0.001) | 0.414*** (0.111; p=<0.001) |

Short and long coefficients by band (detail):

| | ln wage 25-34: short | ln wage 25-34: long | ln wage 35-44: short | ln wage 35-44: long | ln wage 45-55: short | ln wage 45-55: long | ln wage 35-55: short | ln wage 35-55: long |
|---|---|---|---|---|---|---|---|---|
| **early cell set, data-defined** | | | | | | | | |
| Pooled (weighted) | 0.252*** (0.014; p=<0.001) | 0.204*** (0.013; p=<0.001) | 0.344*** (0.020; p=<0.001) | 0.261*** (0.018; p=<0.001) | 0.383*** (0.026; p=<0.001) | 0.290*** (0.023; p=<0.001) | 0.363*** (0.022; p=<0.001) | 0.274*** (0.019; p=<0.001) |
| Black | 0.161*** (0.017; p=<0.001) | 0.132*** (0.016; p=<0.001) | 0.195*** (0.024; p=<0.001) | 0.151*** (0.021; p=<0.001) | 0.224*** (0.029; p=<0.001) | 0.168*** (0.025; p=<0.001) | 0.209*** (0.024; p=<0.001) | 0.159*** (0.021; p=<0.001) |
| White | 0.241*** (0.019; p=<0.001) | 0.194*** (0.018; p=<0.001) | 0.329*** (0.025; p=<0.001) | 0.249*** (0.022; p=<0.001) | 0.359*** (0.032; p=<0.001) | 0.271*** (0.028; p=<0.001) | 0.343*** (0.027; p=<0.001) | 0.259*** (0.023; p=<0.001) |
| Black - White | -0.080*** (0.026; p=0.002) | -0.063*** (0.024; p=0.009) | -0.134*** (0.034; p=<0.001) | -0.098*** (0.030; p=0.001) | -0.135*** (0.043; p=0.002) | -0.103*** (0.037; p=0.006) | -0.135*** (0.036; p=<0.001) | -0.100*** (0.031; p=0.001) |
| N son-years: pooled per band ; Black / White per band | 25-34: 21,881 ; 35-44: 11,049 ; 45-55: 9,788 | 7,548 ; 14,333 ; 3,758 ; 7,291 ; 3,308 ; 6,480 |  |  |  |  |  |  |
| **early industry set, data-defined** | | | | | | | | |
| Pooled (weighted) | 0.252*** (0.014; p=<0.001) | 0.237*** (0.014; p=<0.001) | 0.344*** (0.020; p=<0.001) | 0.325*** (0.020; p=<0.001) | 0.384*** (0.026; p=<0.001) | 0.363*** (0.026; p=<0.001) | 0.363*** (0.022; p=<0.001) | 0.343*** (0.021; p=<0.001) |
| Black | 0.161*** (0.017; p=<0.001) | 0.133*** (0.016; p=<0.001) | 0.195*** (0.024; p=<0.001) | 0.163*** (0.023; p=<0.001) | 0.224*** (0.029; p=<0.001) | 0.189*** (0.027; p=<0.001) | 0.209*** (0.024; p=<0.001) | 0.176*** (0.023; p=<0.001) |
| White | 0.241*** (0.019; p=<0.001) | 0.224*** (0.018; p=<0.001) | 0.329*** (0.025; p=<0.001) | 0.308*** (0.025; p=<0.001) | 0.359*** (0.032; p=<0.001) | 0.335*** (0.031; p=<0.001) | 0.343*** (0.027; p=<0.001) | 0.321*** (0.026; p=<0.001) |
| Black - White | -0.080*** (0.026; p=0.002) | -0.091*** (0.025; p=<0.001) | -0.135*** (0.034; p=<0.001) | -0.145*** (0.034; p=<0.001) | -0.135*** (0.043; p=0.002) | -0.146*** (0.041; p=<0.001) | -0.135*** (0.036; p=<0.001) | -0.145*** (0.035; p=<0.001) |
| N son-years: pooled per band ; Black / White per band | 25-34: 21,889 ; 35-44: 11,054 ; 45-55: 9,793 | 7,548 ; 14,341 ; 3,758 ; 7,296 ; 3,308 ; 6,485 |  |  |  |  |  |  |
| **early industry group (33)** | | | | | | | | |
| Pooled (weighted) | 0.252*** (0.014; p=<0.001) | 0.217*** (0.013; p=<0.001) | 0.344*** (0.020; p=<0.001) | 0.291*** (0.019; p=<0.001) | 0.384*** (0.026; p=<0.001) | 0.329*** (0.025; p=<0.001) | 0.363*** (0.022; p=<0.001) | 0.309*** (0.021; p=<0.001) |
| Black | 0.161*** (0.017; p=<0.001) | 0.120*** (0.016; p=<0.001) | 0.195*** (0.024; p=<0.001) | 0.137*** (0.023; p=<0.001) | 0.224*** (0.029; p=<0.001) | 0.166*** (0.026; p=<0.001) | 0.209*** (0.024; p=<0.001) | 0.151*** (0.023; p=<0.001) |
| White | 0.241*** (0.019; p=<0.001) | 0.209*** (0.018; p=<0.001) | 0.329*** (0.025; p=<0.001) | 0.276*** (0.024; p=<0.001) | 0.359*** (0.032; p=<0.001) | 0.298*** (0.031; p=<0.001) | 0.343*** (0.027; p=<0.001) | 0.287*** (0.025; p=<0.001) |
| Black - White | -0.080*** (0.026; p=0.002) | -0.089*** (0.024; p=<0.001) | -0.135*** (0.034; p=<0.001) | -0.139*** (0.033; p=<0.001) | -0.135*** (0.043; p=0.002) | -0.132*** (0.040; p=0.001) | -0.135*** (0.036; p=<0.001) | -0.136*** (0.034; p=<0.001) |
| N son-years: pooled per band ; Black / White per band | 25-34: 21,889 ; 35-44: 11,054 ; 45-55: 9,793 | 7,548 ; 14,341 ; 3,758 ; 7,296 ; 3,308 ; 6,485 |  |  |  |  |  |  |
| **early fine industry (ind1990ddx)** | | | | | | | | |
| Pooled (weighted) | 0.252*** (0.014; p=<0.001) | 0.202*** (0.013; p=<0.001) | 0.344*** (0.020; p=<0.001) | 0.271*** (0.018; p=<0.001) | 0.384*** (0.026; p=<0.001) | 0.294*** (0.023; p=<0.001) | 0.363*** (0.022; p=<0.001) | 0.283*** (0.019; p=<0.001) |
| Black | 0.161*** (0.017; p=<0.001) | 0.101*** (0.015; p=<0.001) | 0.195*** (0.024; p=<0.001) | 0.108*** (0.023; p=<0.001) | 0.224*** (0.029; p=<0.001) | 0.146*** (0.026; p=<0.001) | 0.209*** (0.024; p=<0.001) | 0.126*** (0.022; p=<0.001) |
| White | 0.241*** (0.019; p=<0.001) | 0.190*** (0.017; p=<0.001) | 0.329*** (0.025; p=<0.001) | 0.260*** (0.023; p=<0.001) | 0.359*** (0.032; p=<0.001) | 0.266*** (0.030; p=<0.001) | 0.343*** (0.027; p=<0.001) | 0.264*** (0.024; p=<0.001) |
| Black - White | -0.080*** (0.026; p=0.002) | -0.089*** (0.023; p=<0.001) | -0.135*** (0.034; p=<0.001) | -0.152*** (0.032; p=<0.001) | -0.135*** (0.043; p=0.002) | -0.120*** (0.040; p=0.003) | -0.135*** (0.036; p=<0.001) | -0.138*** (0.033; p=<0.001) |
| N son-years: pooled per band ; Black / White per band | 25-34: 21,889 ; 35-44: 11,054 ; 45-55: 9,793 | 7,548 ; 14,341 ; 3,758 ; 7,296 ; 3,308 ; 6,485 |  |  |  |  |  |  |
| **early special cell** | | | | | | | | |
| Pooled (weighted) | 0.252*** (0.014; p=<0.001) | 0.218*** (0.014; p=<0.001) | 0.344*** (0.020; p=<0.001) | 0.289*** (0.019; p=<0.001) | 0.384*** (0.026; p=<0.001) | 0.318*** (0.025; p=<0.001) | 0.363*** (0.022; p=<0.001) | 0.303*** (0.021; p=<0.001) |
| Black | 0.161*** (0.017; p=<0.001) | 0.134*** (0.016; p=<0.001) | 0.195*** (0.024; p=<0.001) | 0.149*** (0.022; p=<0.001) | 0.224*** (0.029; p=<0.001) | 0.167*** (0.026; p=<0.001) | 0.209*** (0.024; p=<0.001) | 0.158*** (0.022; p=<0.001) |
| White | 0.241*** (0.019; p=<0.001) | 0.208*** (0.018; p=<0.001) | 0.329*** (0.025; p=<0.001) | 0.278*** (0.023; p=<0.001) | 0.359*** (0.032; p=<0.001) | 0.299*** (0.029; p=<0.001) | 0.343*** (0.027; p=<0.001) | 0.288*** (0.025; p=<0.001) |
| Black - White | -0.080*** (0.026; p=0.002) | -0.074*** (0.025; p=0.003) | -0.135*** (0.034; p=<0.001) | -0.129*** (0.032; p=<0.001) | -0.135*** (0.043; p=0.002) | -0.131*** (0.039; p=<0.001) | -0.135*** (0.036; p=<0.001) | -0.130*** (0.033; p=<0.001) |
| N son-years: pooled per band ; Black / White per band | 25-34: 21,889 ; 35-44: 11,054 ; 45-55: 9,793 | 7,548 ; 14,341 ; 3,758 ; 7,296 ; 3,308 ; 6,485 |  |  |  |  |  |  |
| **early cell: occupation group x industry group** | | | | | | | | |
| Pooled (weighted) | 0.252*** (0.014; p=<0.001) | 0.175*** (0.012; p=<0.001) | 0.344*** (0.020; p=<0.001) | 0.218*** (0.017; p=<0.001) | 0.383*** (0.026; p=<0.001) | 0.238*** (0.023; p=<0.001) | 0.363*** (0.022; p=<0.001) | 0.228*** (0.018; p=<0.001) |
| Black | 0.161*** (0.017; p=<0.001) | 0.104*** (0.015; p=<0.001) | 0.195*** (0.024; p=<0.001) | 0.101*** (0.022; p=<0.001) | 0.224*** (0.029; p=<0.001) | 0.119*** (0.026; p=<0.001) | 0.209*** (0.024; p=<0.001) | 0.112*** (0.021; p=<0.001) |
| White | 0.241*** (0.019; p=<0.001) | 0.169*** (0.017; p=<0.001) | 0.329*** (0.025; p=<0.001) | 0.208*** (0.022; p=<0.001) | 0.359*** (0.032; p=<0.001) | 0.213*** (0.029; p=<0.001) | 0.343*** (0.027; p=<0.001) | 0.212*** (0.023; p=<0.001) |
| Black - White | -0.080*** (0.026; p=0.002) | -0.065*** (0.023; p=0.004) | -0.134*** (0.034; p=<0.001) | -0.107*** (0.031; p=<0.001) | -0.135*** (0.043; p=0.002) | -0.094** (0.039; p=0.015) | -0.135*** (0.036; p=<0.001) | -0.101*** (0.032; p=0.001) |
| N son-years: pooled per band ; Black / White per band | 25-34: 21,881 ; 35-44: 11,049 ; 45-55: 9,788 | 7,548 ; 14,333 ; 3,758 ; 7,291 ; 3,308 ; 6,480 |  |  |  |  |  |  |
| **early occupation group (11) only** | | | | | | | | |
| Pooled (weighted) | 0.252*** (0.014; p=<0.001) | 0.197*** (0.013; p=<0.001) | 0.344*** (0.020; p=<0.001) | 0.244*** (0.018; p=<0.001) | 0.383*** (0.026; p=<0.001) | 0.271*** (0.023; p=<0.001) | 0.363*** (0.022; p=<0.001) | 0.257*** (0.019; p=<0.001) |
| Black | 0.161*** (0.017; p=<0.001) | 0.131*** (0.016; p=<0.001) | 0.195*** (0.024; p=<0.001) | 0.145*** (0.021; p=<0.001) | 0.224*** (0.029; p=<0.001) | 0.163*** (0.025; p=<0.001) | 0.209*** (0.024; p=<0.001) | 0.154*** (0.021; p=<0.001) |
| White | 0.241*** (0.019; p=<0.001) | 0.190*** (0.017; p=<0.001) | 0.329*** (0.025; p=<0.001) | 0.234*** (0.022; p=<0.001) | 0.359*** (0.032; p=<0.001) | 0.250*** (0.028; p=<0.001) | 0.343*** (0.027; p=<0.001) | 0.242*** (0.023; p=<0.001) |
| Black - White | -0.080*** (0.026; p=0.002) | -0.059** (0.024; p=0.013) | -0.134*** (0.034; p=<0.001) | -0.088*** (0.031; p=0.004) | -0.135*** (0.043; p=0.002) | -0.087** (0.038; p=0.021) | -0.135*** (0.036; p=<0.001) | -0.088*** (0.031; p=0.005) |
| N son-years: pooled per band ; Black / White per band | 25-34: 21,881 ; 35-44: 11,049 ; 45-55: 9,788 | 7,548 ; 14,333 ; 3,758 ; 7,291 ; 3,308 ; 6,480 |  |  |  |  |  |  |
| **early occupation group + early industry group, additive** | | | | | | | | |
| Pooled (weighted) | 0.252*** (0.014; p=<0.001) | 0.177*** (0.013; p=<0.001) | 0.344*** (0.020; p=<0.001) | 0.227*** (0.017; p=<0.001) | 0.383*** (0.026; p=<0.001) | 0.254*** (0.023; p=<0.001) | 0.363*** (0.022; p=<0.001) | 0.240*** (0.018; p=<0.001) |
| Black | 0.161*** (0.017; p=<0.001) | 0.108*** (0.015; p=<0.001) | 0.195*** (0.024; p=<0.001) | 0.114*** (0.021; p=<0.001) | 0.224*** (0.029; p=<0.001) | 0.139*** (0.024; p=<0.001) | 0.209*** (0.024; p=<0.001) | 0.126*** (0.020; p=<0.001) |
| White | 0.241*** (0.019; p=<0.001) | 0.172*** (0.017; p=<0.001) | 0.329*** (0.025; p=<0.001) | 0.219*** (0.022; p=<0.001) | 0.359*** (0.032; p=<0.001) | 0.234*** (0.028; p=<0.001) | 0.343*** (0.027; p=<0.001) | 0.227*** (0.023; p=<0.001) |
| Black - White | -0.080*** (0.026; p=0.002) | -0.064*** (0.022; p=0.004) | -0.134*** (0.034; p=<0.001) | -0.105*** (0.030; p=<0.001) | -0.135*** (0.043; p=0.002) | -0.095*** (0.037; p=0.010) | -0.135*** (0.036; p=<0.001) | -0.100*** (0.031; p=0.001) |
| N son-years: pooled per band ; Black / White per band | 25-34: 21,881 ; 35-44: 11,049 ; 45-55: 9,788 | 7,548 ; 14,333 ; 3,758 ; 7,291 ; 3,308 ; 6,480 |  |  |  |  |  |  |
| **current industry group, any age profile** | | | | | | | | |
| Pooled (weighted) | 0.252*** (0.014; p=<0.001) | 0.222*** (0.013; p=<0.001) | 0.345*** (0.020; p=<0.001) | 0.303*** (0.019; p=<0.001) | 0.379*** (0.027; p=<0.001) | 0.334*** (0.025; p=<0.001) | 0.361*** (0.022; p=<0.001) | 0.318*** (0.021; p=<0.001) |
| Black | 0.160*** (0.017; p=<0.001) | 0.126*** (0.015; p=<0.001) | 0.195*** (0.024; p=<0.001) | 0.158*** (0.022; p=<0.001) | 0.220*** (0.029; p=<0.001) | 0.174*** (0.027; p=<0.001) | 0.207*** (0.024; p=<0.001) | 0.167*** (0.022; p=<0.001) |
| White | 0.241*** (0.019; p=<0.001) | 0.211*** (0.018; p=<0.001) | 0.330*** (0.025; p=<0.001) | 0.286*** (0.024; p=<0.001) | 0.353*** (0.033; p=<0.001) | 0.304*** (0.031; p=<0.001) | 0.341*** (0.027; p=<0.001) | 0.295*** (0.026; p=<0.001) |
| Black - White | -0.081*** (0.026; p=0.001) | -0.085*** (0.023; p=<0.001) | -0.135*** (0.035; p=<0.001) | -0.128*** (0.032; p=<0.001) | -0.133*** (0.044; p=0.002) | -0.131*** (0.041; p=0.002) | -0.134*** (0.036; p=<0.001) | -0.129*** (0.034; p=<0.001) |
| N son-years: pooled per band ; Black / White per band | 25-34: 21,774 ; 35-44: 10,780 ; 45-55: 9,377 | 7,500 ; 14,274 ; 3,670 ; 7,110 ; 3,134 ; 6,243 |  |  |  |  |  |  |
| **current cell, any age profile** | | | | | | | | |
| Pooled (weighted) | 0.252*** (0.014; p=<0.001) | 0.177*** (0.011; p=<0.001) | 0.346*** (0.020; p=<0.001) | 0.224*** (0.016; p=<0.001) | 0.381*** (0.027; p=<0.001) | 0.253*** (0.022; p=<0.001) | 0.362*** (0.022; p=<0.001) | 0.238*** (0.017; p=<0.001) |
| Black | 0.159*** (0.017; p=<0.001) | 0.104*** (0.013; p=<0.001) | 0.191*** (0.024; p=<0.001) | 0.117*** (0.019; p=<0.001) | 0.214*** (0.029; p=<0.001) | 0.131*** (0.024; p=<0.001) | 0.202*** (0.025; p=<0.001) | 0.124*** (0.018; p=<0.001) |
| White | 0.240*** (0.019; p=<0.001) | 0.171*** (0.016; p=<0.001) | 0.331*** (0.025; p=<0.001) | 0.219*** (0.021; p=<0.001) | 0.353*** (0.033; p=<0.001) | 0.230*** (0.028; p=<0.001) | 0.341*** (0.027; p=<0.001) | 0.226*** (0.022; p=<0.001) |
| Black - White | -0.081*** (0.026; p=0.001) | -0.068*** (0.021; p=0.001) | -0.139*** (0.035; p=<0.001) | -0.102*** (0.028; p=<0.001) | -0.138*** (0.044; p=0.002) | -0.098*** (0.037; p=0.008) | -0.139*** (0.037; p=<0.001) | -0.102*** (0.028; p=<0.001) |
| N son-years: pooled per band ; Black / White per band | 25-34: 21,707 ; 35-44: 10,682 ; 45-55: 9,190 | 7,478 ; 14,229 ; 3,631 ; 7,051 ; 3,066 ; 6,124 |  |  |  |  |  |  |

## CN. Fast track inside high-paid, high-later-growth cells? (NLSY79)

Is the after-35 wage growth steeper for sons of richer parents WITHIN the data-defined high-paid / high-growth cells (Section D) than elsewhere? (1)-(3): son-level growth on centred ln parental income, early-set indicators and their interactions (controls as A1). (4)-(5): one son-year regression with person FE and year FE, where the piecewise age terms are interacted with ln parental income, the early-set indicators and the triple products; (4) shows the slope-after-35 terms, (5) the slope-before-35 terms (log points per 10 years per log point of parental income). (6): the pre-chosen illustrative industries instead of the data-defined sets.

| | (1) Delta ln wage (40-55) - (25-34) | (2) Delta ln wage (35-55) - (25-34) | (3) Delta ln wage (45-55) - (25-34) | (4) ln wage, person FE: slope 35-55 terms | (5) ... slope 25-35 terms | (6) illustrative: Delta (40-55) with finance / insurance / legal / professional |
|---|---|---|---|---|---|---|
| **Pooled (weighted)** | | | | | | |
| ln parental income (gradient in cells of neither set) | 0.076*** (0.016; p=<0.001) | 0.067*** (0.014; p=<0.001) | 0.088*** (0.019; p=<0.001) | 0.024* (0.013; p=0.058) | 0.076*** (0.020; p=<0.001) | 0.118*** (0.017; p=<0.001) |
| ln parental income x early high-paid high-growth cell (extra gradient inside) | 0.068 (0.072; p=0.340) | 0.050 (0.060; p=0.411) | 0.058 (0.082; p=0.478) | 0.030 (0.044; p=0.494) | 0.006 (0.065; p=0.927) |  |
| gradient inside high-paid high-growth cells = sum of the two rows above | 0.145** (0.071; p=0.040) | 0.116* (0.059; p=0.051) | 0.146* (0.080; p=0.068) | 0.054 (0.042; p=0.201) | 0.082 (0.063; p=0.190) |  |
| early high-paid high-growth cell | 0.275*** (0.042; p=<0.001) | 0.249*** (0.034; p=<0.001) | 0.292*** (0.046; p=<0.001) | 0.090*** (0.026; p=<0.001) | 0.263*** (0.039; p=<0.001) |  |
| ln parental income x early high-paid-only cell | 0.130 (0.095; p=0.172) | 0.122* (0.071; p=0.084) | 0.143 (0.109; p=0.188) | -0.008 (0.056; p=0.892) | 0.137* (0.075; p=0.069) |  |
| early high-paid-only cell | 0.172*** (0.061; p=0.005) | 0.181*** (0.045; p=<0.001) | 0.171** (0.067; p=0.010) | 0.049 (0.031; p=0.115) | 0.255*** (0.053; p=<0.001) |  |
| ln parental income x early high-growth-only cell | -0.029 (0.051; p=0.569) | -0.018 (0.042; p=0.665) | -0.006 (0.056; p=0.914) | 0.021 (0.033; p=0.532) | -0.065 (0.052; p=0.212) |  |
| early high-growth-only cell | 0.079** (0.033; p=0.018) | 0.076*** (0.027; p=0.005) | 0.086** (0.038; p=0.024) | 0.029 (0.023; p=0.194) | 0.097*** (0.034; p=0.004) |  |
| illustrative: ln parental income x early finance / insurance / legal / professional |  |  |  |  |  | 0.087 (0.108; p=0.421) |
| illustrative: early finance / insurance / legal / professional |  |  |  |  |  | 0.208*** (0.066; p=0.002) |
| N sons / clusters (1)-(3), (6); son-years / sons (4)-(5) | 2,461 / 2,011 | 2,621 / 2,115 | 2,284 / 1,888 | 42,718 / 2,892 | 42,718 / 2,892 | 2,462 / 2,011 |
| Sons with an early high-paid high-growth cell (with Delta 40-55) | 350 (308) |  |  |  |  | FLP: 182 |
| **Black** | | | | | | |
| ln parental income (gradient in cells of neither set) | 0.049** (0.020; p=0.014) | 0.030* (0.017; p=0.076) | 0.052** (0.023; p=0.025) | 0.035** (0.014; p=0.015) | 0.013 (0.024; p=0.581) | 0.063*** (0.019; p=<0.001) |
| ln parental income x early high-paid high-growth cell (extra gradient inside) | -0.024 (0.073; p=0.741) | 0.005 (0.063; p=0.941) | -0.045 (0.083; p=0.590) | -0.066 (0.054; p=0.222) | 0.101 (0.082; p=0.218) |  |
| gradient inside high-paid high-growth cells = sum of the two rows above | 0.024 (0.071; p=0.729) | 0.034 (0.061; p=0.572) | 0.007 (0.081; p=0.933) | -0.031 (0.053; p=0.559) | 0.114 (0.077; p=0.141) |  |
| early high-paid high-growth cell | 0.249*** (0.066; p=<0.001) | 0.239*** (0.054; p=<0.001) | 0.299*** (0.066; p=<0.001) | 0.099** (0.040; p=0.012) | 0.285*** (0.066; p=<0.001) |  |
| ln parental income x early high-paid-only cell | 0.061 (0.080; p=0.446) | 0.075 (0.067; p=0.261) | 0.097 (0.085; p=0.250) | 0.011 (0.051; p=0.827) | 0.017 (0.065; p=0.795) |  |
| early high-paid-only cell | 0.209** (0.086; p=0.015) | 0.208*** (0.074; p=0.005) | 0.226** (0.091; p=0.013) | 0.087 (0.056; p=0.118) | 0.123* (0.071; p=0.085) |  |
| ln parental income x early high-growth-only cell | -0.023 (0.065; p=0.719) | -0.016 (0.056; p=0.777) | -0.027 (0.071; p=0.699) | -0.043 (0.042; p=0.305) | 0.058 (0.079; p=0.463) |  |
| early high-growth-only cell | 0.057 (0.061; p=0.353) | 0.053 (0.052; p=0.307) | 0.058 (0.067; p=0.390) | -0.012 (0.040; p=0.771) | 0.137** (0.062; p=0.027) |  |
| illustrative: ln parental income x early finance / insurance / legal / professional |  |  |  |  |  | -0.068 (0.108; p=0.533) |
| illustrative: early finance / insurance / legal / professional |  |  |  |  |  | 0.053 (0.085; p=0.531) |
| N sons / clusters (1)-(3), (6); son-years / sons (4)-(5) | 889 / 705 | 948 / 742 | 815 / 656 | 14,614 / 1,055 | 14,614 / 1,055 | 889 / 705 |
| Sons with an early high-paid high-growth cell (with Delta 40-55) | 69 (61) |  |  |  |  | FLP: 38 |
| **White** | | | | | | |
| ln parental income (gradient in cells of neither set) | 0.064*** (0.021; p=0.002) | 0.058*** (0.018; p=0.001) | 0.075*** (0.025; p=0.003) | 0.025 (0.017; p=0.141) | 0.052* (0.028; p=0.058) | 0.110*** (0.021; p=<0.001) |
| ln parental income x early high-paid high-growth cell (extra gradient inside) | 0.087 (0.074; p=0.240) | 0.061 (0.059; p=0.297) | 0.087 (0.085; p=0.305) | 0.036 (0.047; p=0.450) | 0.032 (0.066; p=0.631) |  |
| gradient inside high-paid high-growth cells = sum of the two rows above | 0.150** (0.072; p=0.037) | 0.119** (0.057; p=0.035) | 0.162** (0.082; p=0.049) | 0.061 (0.044; p=0.171) | 0.084 (0.061; p=0.164) |  |
| early high-paid high-growth cell | 0.252*** (0.045; p=<0.001) | 0.233*** (0.035; p=<0.001) | 0.258*** (0.051; p=<0.001) | 0.077*** (0.029; p=0.009) | 0.243*** (0.041; p=<0.001) |  |
| ln parental income x early high-paid-only cell | 0.137 (0.101; p=0.175) | 0.127* (0.076; p=0.097) | 0.143 (0.114; p=0.210) | 0.004 (0.062; p=0.946) | 0.131 (0.086; p=0.129) |  |
| early high-paid-only cell | 0.174*** (0.066; p=0.008) | 0.179*** (0.049; p=<0.001) | 0.179** (0.072; p=0.013) | 0.046 (0.038; p=0.225) | 0.259*** (0.059; p=<0.001) |  |
| ln parental income x early high-growth-only cell | -0.028 (0.072; p=0.696) | -0.011 (0.061; p=0.860) | 0.004 (0.079; p=0.960) | 0.024 (0.044; p=0.589) | -0.056 (0.075; p=0.454) |  |
| early high-growth-only cell | 0.083** (0.042; p=0.049) | 0.074** (0.034; p=0.032) | 0.092* (0.048; p=0.053) | 0.040 (0.028; p=0.159) | 0.074 (0.045; p=0.100) |  |
| illustrative: ln parental income x early finance / insurance / legal / professional |  |  |  |  |  | 0.063 (0.108; p=0.559) |
| illustrative: early finance / insurance / legal / professional |  |  |  |  |  | 0.255*** (0.067; p=<0.001) |
| N sons / clusters (1)-(3), (6); son-years / sons (4)-(5) | 1,572 / 1,306 | 1,673 / 1,373 | 1,469 / 1,232 | 28,104 / 1,837 | 28,104 / 1,837 | 1,573 / 1,306 |
| Sons with an early high-paid high-growth cell (with Delta 40-55) | 281 (247) |  |  |  |  | FLP: 144 |
| **Black - White** | | | | | | |
| ln parental income (gradient in cells of neither set) | -0.015 (0.029; p=0.600) | -0.029 (0.024; p=0.243) | -0.023 (0.034; p=0.495) | 0.010 (0.022; p=0.643) | -0.039 (0.036; p=0.279) | -0.046 (0.028; p=0.102) |
| ln parental income x early high-paid high-growth cell (extra gradient inside) | -0.111 (0.104; p=0.285) | -0.057 (0.086; p=0.510) | -0.132 (0.119; p=0.267) | -0.102 (0.072; p=0.156) | 0.069 (0.105; p=0.511) |  |
| gradient inside high-paid high-growth cells = sum of the two rows above | -0.126 (0.101; p=0.212) | -0.085 (0.083; p=0.305) | -0.155 (0.115; p=0.179) | -0.091 (0.069; p=0.184) | 0.030 (0.098; p=0.762) |  |
| early high-paid high-growth cell | -0.003 (0.080; p=0.969) | 0.007 (0.064; p=0.916) | 0.042 (0.083; p=0.615) | 0.023 (0.049; p=0.643) | 0.042 (0.078; p=0.591) |  |
| ln parental income x early high-paid-only cell | -0.076 (0.129; p=0.558) | -0.052 (0.101; p=0.609) | -0.046 (0.142; p=0.747) | 0.007 (0.081; p=0.931) | -0.114 (0.108; p=0.292) |  |
| early high-paid-only cell | 0.035 (0.108; p=0.747) | 0.029 (0.089; p=0.743) | 0.047 (0.116; p=0.685) | 0.041 (0.067; p=0.538) | -0.136 (0.093; p=0.143) |  |
| ln parental income x early high-growth-only cell | 0.005 (0.097; p=0.959) | -0.005 (0.083; p=0.951) | -0.031 (0.106; p=0.768) | -0.067 (0.061; p=0.273) | 0.114 (0.108; p=0.295) |  |
| early high-growth-only cell | -0.026 (0.075; p=0.730) | -0.021 (0.062; p=0.738) | -0.034 (0.083; p=0.681) | -0.052 (0.049; p=0.291) | 0.063 (0.077; p=0.408) |  |
| illustrative: ln parental income x early finance / insurance / legal / professional |  |  |  |  |  | -0.131 (0.153; p=0.393) |
| illustrative: early finance / insurance / legal / professional |  |  |  |  |  | -0.201* (0.109; p=0.064) |
