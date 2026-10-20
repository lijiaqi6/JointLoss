# Her displacement and separation: robustness of IGE/64 (M3), PSID

Built by `65.HerLossRobustness.py` (2026-10-19); design in its docstring. 64's M3 design: wives of male heads, baseline with a child 0-17 and positive own hours; treated = her first displacement (closure or layoff / firing) in ev; clean controls not displaced herself to ev+6; person x stack and calendar year x stack FE; reference e = -2; s.e. clustered by 1968 family; target sample (events 1984-2021, outcome years <= 2021). Outcome 'still with baseline husband' unless stated. *** p<0.01, ** p<0.05, * p<0.1; every cell: coefficient*** (s.e.; p). Averages of the event-time coefficients over years 1-3, 4-6, 1-6.

**Caveat.** The outcome equals 1 at baseline by construction: no pre-period placebo for it. Selection is checked with the closures, the balance table, the pre-trends in her hours and earnings, and baseline controls x event time.

## 0. Reproduction of IGE/64

Years 1-3: -0.046*** (0.012; p=<0.001); years 4-6: -0.090*** (0.016; p=<0.001); years 1-6: -0.068*** (0.013; p=<0.001). N = 236,761 person-years, 1,205 displaced wives, 41,623 control stacks, 2,037 clusters (64: -0.046*** / -0.090***, 1,205 displaced wives).

## 1. Her displacement vs his: one regression

Her design (outcome 'still with baseline husband') and his (IGE/19 / 64: 'still with baseline wife') stacked in one regression with design-specific unit and cell FE and event dummies, one covariance clustered by 1968 family (a couple can enter both designs). N person-years: (a) 460,811; (b) 406,823.

| | Her displacement | His displacement | Her - his |
|---|---:|---:|---:|
| Samples as in IGE/64: years 1-3 | -0.046*** (0.012; p=<0.001) | -0.036*** (0.011; p=0.002) | -0.010 (0.016; p=0.536) |
| Samples as in IGE/64: years 4-6 | -0.090*** (0.017; p=<0.001) | -0.051*** (0.014; p=<0.001) | -0.038* (0.020; p=0.061) |
| Samples as in IGE/64: years 1-6 | -0.068*** (0.014; p=<0.001) | -0.044*** (0.012; p=<0.001) | -0.024 (0.017; p=0.163) |
| Samples as in IGE/64: displaced / clusters (joint regression) | 1,205 | 1,366 | 2,138 |
| Both spouses with positive hours at baseline: years 1-3 | -0.044*** (0.012; p=<0.001) | -0.043*** (0.013; p=0.001) | -0.001 (0.017; p=0.951) |
| Both spouses with positive hours at baseline: years 4-6 | -0.086*** (0.016; p=<0.001) | -0.051*** (0.016; p=0.001) | -0.035 (0.022; p=0.106) |
| Both spouses with positive hours at baseline: years 1-6 | -0.065*** (0.013; p=<0.001) | -0.047*** (0.014; p=<0.001) | -0.018 (0.018; p=0.329) |
| Both spouses with positive hours at baseline: displaced / clusters (joint regression) | 1,143 | 1,066 | 2,073 |

## 2. Selection into displacement

### 2a. Closures vs layoffs / firings (one regression, common controls)

| | Closure | Layoff / firing | Closure - layoff |
|---|---:|---:|---:|
| Her displacement: years 1-3 | -0.027 (0.021; p=0.194) | -0.056*** (0.015; p=<0.001) | 0.029 (0.026; p=0.267) |
| Her displacement: years 4-6 | -0.044 (0.027; p=0.106) | -0.113*** (0.020; p=<0.001) | 0.069** (0.034; p=0.042) |
| Her displacement: years 1-6 | -0.035 (0.023; p=0.115) | -0.084*** (0.017; p=<0.001) | 0.049* (0.028; p=0.082) |
| Her displacement: displaced (closure / layoff) | 376 | 829 |  |
| His displacement: years 1-3 | -0.025 (0.018; p=0.179) | -0.041*** (0.014; p=0.004) | 0.016 (0.023; p=0.492) |
| His displacement: years 4-6 | -0.029 (0.024; p=0.222) | -0.062*** (0.017; p=<0.001) | 0.033 (0.029; p=0.250) |
| His displacement: years 1-6 | -0.027 (0.020; p=0.189) | -0.051*** (0.015; p=<0.001) | 0.025 (0.025; p=0.325) |
| His displacement: displaced (closure / layoff) | 406 | 960 |  |
| Her hours (her design): years 1-3 | -162*** (61; p=0.008) | -109** (47; p=0.021) | -53 (76; p=0.489) |
| Her hours (her design): years 4-6 | -27 (64; p=0.671) | -39 (52; p=0.449) | 12 (81; p=0.881) |

### 2b. Baseline balance (unit level, baseline year)

Difference displaced - control within event-year stacks, clustered by 1968 family. Job tenure is not in the extracted PSID files used here. Marriage duration is the years observed with this husband (left-censored at her first PSID year as a wife or head).

| | Displaced mean | Control mean | Difference | Displaced / control units |
|---|---:|---:|---:|---:|
| Her annual hours | 1,520 | 1,610 | -58** (23; p=0.012) | 1,205 / 41,623 |
| Her labor earnings ($000, 2000) | 17.393 | 26.067 | -7.149*** (0.620; p=<0.001) | 1,205 / 41,623 |
| His annual hours | 2,038 | 2,164 | -120*** (25; p=<0.001) | 1,205 / 41,623 |
| His labor earnings ($000, 2000) | 34.060 | 45.266 | -10.062*** (1.285; p=<0.001) | 1,205 / 41,623 |
| Her share of couple labor earnings | 0.375 | 0.394 | -0.009 (0.008; p=0.236) | 1,204 / 41,609 |
| Her age | 33.453 | 35.977 | -2.100*** (0.231; p=<0.001) | 1,205 / 41,623 |
| Children 0-17 | 1.944 | 1.854 | 0.090*** (0.030; p=0.003) | 1,205 / 41,623 |
| Age of youngest child | 6.386 | 7.050 | -0.597*** (0.144; p=<0.001) | 1,205 / 41,623 |
| Years observed with this husband (left-censored) | 7.167 | 9.199 | -2.018*** (0.205; p=<0.001) | 1,205 / 41,623 |
| Observed with him <= 2 years | 0.349 | 0.226 | 0.133*** (0.014; p=<0.001) | 1,205 / 41,623 |
| Spell left-censored (with him from her first year) | 0.738 | 0.748 | -0.020 (0.015; p=0.163) | 1,205 / 41,623 |
| Black | 0.367 | 0.283 | 0.083*** (0.016; p=<0.001) | 1,205 / 41,623 |

### 2c. Pre-trends in her labor market outcomes (reference e = -2)

| | e = -3 | e = -1 | e = 0 | Years 1-3 | Years 4-6 |
|---|---:|---:|---:|---:|---:|
| Her annual hours | -9 (32; p=0.776) | 115*** (31; p=<0.001) | -135*** (34; p=<0.001) | -127*** (38; p=<0.001) | -36 (41; p=0.379) |
| Her labor earnings (2000 $) | 455 (667; p=0.495) | -425 (497; p=0.393) | -3,015*** (595; p=<0.001) | -4,140*** (602; p=<0.001) | -2,960*** (718; p=<0.001) |
| His annual hours (while with her) | -0 (30; p=0.988) | 10 (29; p=0.717) | 26 (32; p=0.415) | 57* (32; p=0.073) | 66* (36; p=0.069) |

### 2d. Baseline characteristics x event time

Each baseline characteristic of 2b (her hours, earnings, age, age^2; his earnings and hours; children, age of the youngest; marriage-duration bins 0-2 / 3-5 / 6-10 / 11+ and left-censoring; race; missing indicators) interacted with every event-time dummy for all units (so controls with the same characteristics have their own path).

| | IGE/64 (no controls) | With controls x e | With controls: closures | With controls: layoffs |
|---|---:|---:|---:|---:|
| Years 1-3 | -0.046*** (0.012; p=<0.001) | -0.033*** (0.012; p=0.006) | -0.021 (0.021; p=0.313) | -0.040*** (0.015; p=0.007) |
| Years 4-6 | -0.090*** (0.016; p=<0.001) | -0.065*** (0.017; p=<0.001) | -0.034 (0.027; p=0.213) | -0.080*** (0.020; p=<0.001) |
| Years 1-6 | -0.068*** (0.013; p=<0.001) | -0.049*** (0.013; p=<0.001) | -0.028 (0.023; p=0.223) | -0.060*** (0.017; p=<0.001) |
| Displaced wives | 1,205 | 1,205 | 376 | 829 |

## 3. Joint loss: her loss alone vs both spouses displaced within a year

'Joint' = his displacement in ev-1..ev+1 of hers (244 of 1,205 displaced wives); in his design, her displacement in ev-1..ev+1 of his (her reports start in calendar 1983). (a) her design without the joint couples; (b) and controls without his displacement in ev-3..ev+6; (c) her-alone and joint as separate treated dummies in one regression (controls as in b); (d) the same in his design (controls without her displacement in ev-3..ev+6).

| | (a) Her loss, joint dropped | (b) + clean controls | (c) Her alone | (c) Joint | (c) Joint - her alone | (d) His alone | (d) Joint | (d) Joint - his alone |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Years 1-3 | -0.049*** (0.013; p=<0.001) | -0.052*** (0.013; p=<0.001) | -0.052*** (0.013; p=<0.001) | -0.033 (0.030; p=0.270) | 0.019 (0.033; p=0.561) | -0.033*** (0.012; p=0.007) | -0.081** (0.033; p=0.015) | -0.049 (0.035; p=0.167) |
| Years 4-6 | -0.081*** (0.018; p=<0.001) | -0.088*** (0.018; p=<0.001) | -0.088*** (0.018; p=<0.001) | -0.133*** (0.043; p=0.002) | -0.044 (0.047; p=0.350) | -0.049*** (0.015; p=<0.001) | -0.108** (0.043; p=0.011) | -0.060 (0.045; p=0.184) |
| Years 1-6 | -0.065*** (0.015; p=<0.001) | -0.070*** (0.015; p=<0.001) | -0.070*** (0.015; p=<0.001) | -0.083** (0.035; p=0.017) | -0.012 (0.038; p=0.742) | -0.041*** (0.013; p=0.001) | -0.095*** (0.036; p=0.009) | -0.054 (0.038; p=0.154) |
| Displaced (units) | 961 | 961 | 961 | 244 |  | 1,192 | 174 |  |
| Control stacks | 41,623 | 32,864 | 32,864 |  |  | 34,912 |  |  |

## 4. Heterogeneity

Group-specific cells and event dummies in one regression (point estimates = separate regressions); the difference uses the joint clustered covariance. Her share = her / (her + his) labor earnings at baseline (treated median 0.357).

| | First group (Black / higher share) | Second group (White / lower share) | Difference |
|---|---:|---:|---:|
| Race, years 1-3 | -0.048** (0.023; p=0.036) | -0.040*** (0.014; p=0.005) | -0.008 (0.027; p=0.768) |
| Race, years 4-6 | -0.083*** (0.030; p=0.006) | -0.083*** (0.020; p=<0.001) | -0.000 (0.036; p=0.993) |
| Race, years 1-6 | -0.065*** (0.025; p=0.008) | -0.061*** (0.016; p=<0.001) | -0.004 (0.029; p=0.889) |
| Race: displaced wives / control stacks | 442 / 11,779 | 763 / 29,844 |  |
| Her share above / below treated median (0.36), years 1-3 | -0.033* (0.018; p=0.060) | -0.058*** (0.017; p=<0.001) | 0.024 (0.025; p=0.326) |
| Her share above / below treated median (0.36), years 4-6 | -0.083*** (0.024; p=<0.001) | -0.098*** (0.023; p=<0.001) | 0.015 (0.033; p=0.653) |
| Her share above / below treated median (0.36), years 1-6 | -0.058*** (0.020; p=0.003) | -0.078*** (0.019; p=<0.001) | 0.020 (0.027; p=0.471) |
| Her share above / below treated median (0.36): displaced wives / control stacks | 601 / 22,929 | 603 / 18,680 |  |
| Her share above / below treated median (0.36): her hours, years 1-3 | -270*** (50; p=<0.001) | -4 (54; p=0.938) | -266*** (73; p=<0.001) |
| Her share >= 0.40 / < 0.40, years 1-3 | -0.035* (0.020; p=0.076) | -0.054*** (0.015; p=<0.001) | 0.019 (0.025; p=0.462) |
| Her share >= 0.40 / < 0.40, years 4-6 | -0.096*** (0.027; p=<0.001) | -0.088*** (0.021; p=<0.001) | -0.008 (0.034; p=0.812) |
| Her share >= 0.40 / < 0.40, years 1-6 | -0.066*** (0.022; p=0.003) | -0.071*** (0.017; p=<0.001) | 0.005 (0.028; p=0.851) |
| Her share >= 0.40 / < 0.40: displaced wives / control stacks | 512 / 19,657 | 692 / 21,952 |  |
| Her share >= 0.40 / < 0.40: her hours, years 1-3 | -263*** (55; p=<0.001) | -37 (50; p=0.457) | -226*** (73; p=0.002) |

## 5. Who leaves, and attrition

The PSID has no item on the reason for a separation. Route of the first separation after baseline: his sequence number 81-89 in that wave = he died; otherwise her family's split-off indicator (2 / 4 = she moved out into a split-off family; 1 / 3 = she is in the continuing family, so he moved out). Each route is an outcome ('not with him, first separated by route k'); the routes add up to 1 - outcome.

| | Years 1-3 | Years 4-6 |
|---|---:|---:|
| Not with baseline husband (= - main estimate) | 0.046*** (0.012; p=<0.001) | 0.090*** (0.016; p=<0.001) |
| Separated: He moved out (she stayed in the continuing family) | 0.036*** (0.008; p=<0.001) | 0.054*** (0.012; p=<0.001) |
| Separated: She moved out (split-off family) | 0.009** (0.004; p=0.035) | 0.016*** (0.006; p=0.009) |
| Separated: He died | -0.002 (0.002; p=0.444) | 0.001 (0.004; p=0.769) |
| Separated: Route not identified | 0.019*** (0.007; p=0.006) | 0.034*** (0.010; p=<0.001) |
| Observed as wife or head (attrition; grid of interview years) | 0.066*** (0.013; p=<0.001) | 0.042*** (0.015; p=0.006) |
| Still with baseline husband, filled from his side | -0.025* (0.014; p=0.069) | -0.074*** (0.018; p=<0.001) |
| Both groups observed at the first interview after ev: still with baseline husband | -0.050*** (0.012; p=<0.001) | -0.094*** (0.017; p=<0.001) |
| Same, observed as wife or head (attrition) | 0.011 (0.012; p=0.355) | -0.011 (0.015; p=0.470) |
| Same, filled from his side | -0.051*** (0.014; p=<0.001) | -0.099*** (0.018; p=<0.001) |
| Same: displaced wives / control stacks | 1,159 / 37,255 |  |

Route of the first separation in e = 0..+6 (shares): displaced wives (275 separations) he moved out 0.60, she moved out 0.15, he died 0.04, route not identified 0.21; controls (5,090) he moved out 0.65, she moved out 0.16, he died 0.07, route not identified 0.12. Route not identified = split-off indicator of her family 0: 692 (all units, first separations). The routes sum to 0.063 in years 1-3, more than the main estimate, because at the reference year e = -2 more displaced wives were not yet with this husband (shorter marriages, 2b); measured from baseline the separation response is larger, not smaller. Treated wives must be interviewed to report the displacement; share of units observed at the first interview after ev: displaced 0.962, controls 0.895.

Share of post-event interview years (e >= 1) in which she is observed as wife or head: displaced 0.823, controls 0.807. Filling the outcome from his side (he is a male head with another or no wife -> 0) adds 10,746 person-years.
