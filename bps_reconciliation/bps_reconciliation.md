# BPS (2016) reconciliation for Paper A: replication, relaxations, displacement (2026-10-18)

Blundell, Pistaferri and Saporta-Eksten (2016, AER, "BPS"), PSID waves 1999-2009 (income years 1998-2008), run with
BPS's own code (copies in `code/`, every edit listed in `README.md`) on BPS's own constructed PSID panel. Protocol:
`IGE/proposals/fable_bps2016_paperA.md`, Steps 0-2. Every number here is in `bps_reconciliation.csv`.
Stars: \*\*\* p<0.01, \*\* p<0.05, \* p<0.10; p-values from the normal. Standard errors: GMM clustered by household
for the wage process (as in BPS Table 3); block bootstrap over households for preferences, elasticities, the
insurance chain and beta (50 replications; BPS 200; s.e. = IQR/1.349 as in BPS's `bootstrap.do`); a dagger (†)
marks a second-step GMM s.e. that ignores the first step (used only where no bootstrap was run). Associations,
not causal estimates, throughout Step 2.

## Summary

**Step 0: BPS replicate exactly.** Running BPS's `psid_sample.do` and `prepare_bootstrap.do` on their shipped
`psid_cons.dta` reproduces their shipped `data4estimation.dta` in every variable (10,479 household-years). Every point
estimate matches the paper: all 36 entries of Table 3 (e.g. all ages: sigma_u1u2 0.0058\*\* (0.0027),
sigma_v1v2 0.0027 (0.0023), correlation 0.31 / 0.08), Table 4 cols. 1, 4 and 5 to the third decimal (E(pi) 0.150,
E(s) 0.708, eta_c,p 0.418, eta_h1,w1 0.681, eta_h2,w2 0.958, beta -0.138), N = 7,295, Table 5 col. 1 (wife's
Marshallian cross-elasticity -0.752, consumption / husband's wage 0.316), Table 7 (theta_1 -0.168\* (0.087),
N = 3,143; theta_0 0.002 (0.030), N = 4,941) and the insurance chain 7.09 / 6.33 / 5.79 / 3.88 / 3.16
(published 7.1 / 6.3 / 5.8 / 3.9 / 3.2; split 19.4 / 62.3 / 18.3% vs the published rounded 20 / 63 / 17%;
Food-Stamp group 7.15 / 3.57 / 2.32 / 2.08 and 70.6% government vs 7.2 / 3.6 / 2.3 / 2.1 and 71%). The all-ages GMM
s.e. match to four decimals; the age-group GMM s.e. differ by up to about 15% (Stata 19 vs BPS's Stata 13 numerical
derivatives; two stars change: husband's transitory variance at 43-47, \*\*\* -> \*\*, and wife's at 53-57,
\* -> none). Bootstrap s.e. with 50 replications are close to
BPS's 200 (E(pi) 0.004 vs 0.004, E(s) 0.013 vs 0.013, beta 0.213 vs 0.270, eta's within 0.03-0.06). One
code-vs-paper discrepancy: BPS's footnote 15 says the 1997 immigrant refresher is excluded, but the code keeps it
(11% of the estimation rows); dropping it changes nothing material (family share 0.626, sigma_u1u2 0.0060\*\*).

**Step 1: which restriction matters.**
- (a) Dropping only the zero-hours / zero-earnings year (not the husband's whole history) adds 637 household-years;
  wage moments barely move, the family-labor-supply share falls from 0.62 to 0.56 and government (0.22) and savings
  (0.22) rise; beta -0.03 (0.27).
- (b) Removing both spouses' employment-status controls from the residual regressions changes nothing material:
  the wage residuals carry no status controls in BPS, so Table 3 is identical, and the preference estimates and
  the 62 / 19 / 18 split move by less than one point.
- (c) The trims are what the estimator rests on. Without the jump / collapse-recovery trim the husband's transitory
  wage variance doubles (0.028 -> 0.056) and the permanent one falls (0.030 -> 0.019); the transitory covariance
  loses significance (0.0043, p = 0.22); the preference step collapses (eta_c,p 0.08, consumption response to a
  permanent shock 0.03, wife's cross-elasticity -1.36). Without the half-minimum-wage trim the permanent variance
  rises to 0.045, sigma_u1u2 = 0.0073\*\* and the family share rises to 0.70. With both off the estimator is
  degenerate (household earnings would rise after a permanent fall in his wage).
- (d) SEO in: E(pi) 0.140, family share 0.68, government 0.18, savings 0.14 (weighted 0.70 / 0.16 / 0.14). By race
  (SEO in): White couples 0.52 / 0.21 / 0.27 (more self-insurance); Black couples (1,625 GMM observations) E(pi)
  0.081 but the preference step is not identified (consumption response -0.005, s.e. 0.157; beta 7.0, s.e. 16).
- (e) Breaking only on a change of spouse identity keeps 8 more household-years and changes nothing. The
  composition break matters through separation itself: the couple's next interview shows a separation or a new wife
  in 2.8% of couple-years without displacement, 5.7% after the wife's displacement (+2.9 pp\*\*, p = 0.033) and 9.3%
  after a joint displacement (+6.5 pp, p = 0.15; 4 of 43). 327 of 3,689 couples end in a separation; 38 of them had
  a displacement in the interval before.
- (f) All together: degenerate, driven by (c). The "BPS without restrictions" column does not exist as an estimate
  of the same model: without the trims the estimator attributes all insurance to the family.

**Step 2: displacement inside BPS's panel.**
- 4.4% of BPS couple-years contain a husband's displacement (414), 3.1% a wife's (288) and 0.30% a joint one (28;
  0.25% in the same calendar year). P(wife displaced | husband displaced) = 6.8% vs 2.9%.
- Of 692 husband-displacement couple-years among married couples with husbands 30-57 (SRC + SEO), 404 reach BPS's
  estimation file and 293 carry a wage-growth moment; of 57 joint ones, 28 and 17. The SEO drop removes the most
  (165 husband / 14 joint), then the missing t-2 observation (105 / 11), the no-work rule (45 / 5; only 8 of the 45
  are the zero-hours year itself), education (39 / 4) and the composition break (34 / 5); the trims remove almost
  none (7 / 0).
- BPS residuals around displacements: in the interval of the husband's displacement his earnings residual is
  -0.123\*\*\* (BPS sample) and consumption -0.022 (n.s.); with a joint displacement his earnings fall -0.335\* and the
  wife's earnings (arc change, zeros in) -0.341\*\*\* (difference from husband-only -0.438\*\*\*), while the
  consumption residual does not fall in that interval (+0.049, n.s.). In the next interval consumption falls more
  after a joint than a single displacement: -0.062 (n.s.) in BPS's sample, -0.110\* with the SEO (joint minus single
  -0.138\*\*, p = 0.027) and -0.101\* with all relaxations (difference -0.134\*\*).
- BPS's transitory wage-shock covariance is not carried by displacement years: without couple-years with either
  spouse displaced it is 0.0063\*\* (0.0030) vs 0.0058\*\* (0.0027); without joint years 0.0054\*\*. Displacement years
  instead carry the earnings covariance: a joint displacement year adds +0.193\*\* (p = 0.019) to E(du_y1 du_y2)
  (mean 0.0029, n.s.). Dropping displacement years from the preference step lowers the family share to 0.56.
- Table 7's theta_1 = -0.168\* is entries: -0.159\*\* (0.064) for 0 -> 1 transitions and -0.009 (0.058) for exits.
  A joint displacement lowers entries (-0.115\*\*, p = 0.023, beyond the husband's and the wife's own terms).

**What this means for Paper A.** BPS's insurance accounting is reproducible and robust to the status controls, the
composition rule and the SEO, but not to the two trims, which remove the collapse-and-recovery years of earnings
and hours that job loss produces; their transitory covariance is not a shadow of joint displacement, which is rare
in their panel (17 couple-years with a wage moment) and shows up in earnings, not hourly wages. The joint-loss
consumption effect appears with a lag, in the broader samples, and is net of BPS's residualisation.

## Specifications

| Column | Switches (code/specs) | What changes |
|---|---|---|
| BPS baseline | none | BPS as shipped |
| without 1997 immigrants | `SW_imm 1` | drop ER30001 3001-3511 (BPS fn. 15) |
| (a) | `SW_nowork 1` | `prepare_bootstrap.do` l. 66-69: drop the no-work year, not the person |
| (b) | `SW_status 0` | `residual_measures.do`: no empl / unempl / retir levels, changes, x year, both spouses |
| (c) | `SW_jump 0`, `SW_minw 0` | `prepare_bootstrap.do` l. 51-52 and 85-116 off (jointly and separately) |
| (d) | `SW_seo 1` (+ `WGT [pw=weight]`, `SW_race`) | `psid_sample.do` l. 196; weights; race of the head |
| (e) | `SW_brk 1` | `psid_sample.do` l. 88-90: break only on a change of the wife's / head's PSID id |
| (f) | a + b + c + d + e | |
| no displacement years | `SW_dexcl 1` (2 = joint only) | drop couple-years whose interval contains a displacement |

## Step 0. BPS as shipped

### Table S0.1. Wage-process estimates (BPS Table 3): published vs replicated

Each cell: estimate (GMM s.e. clustered by household; p). Replicated from BPS's own code and data (T4C11 = age-varying variances, T4C41 = 'all ages' stationary model).

| Parameter | | 30-37 | 38-42 | 43-47 | 48-52 | 53-57 | All ages |
|---|---|---|---|---|---|---|---|
| Males, transitory sigma2_u1 | published | 0.0431*** (0.0127; p=0.001) | 0.0163 (0.0113; p=0.149) | 0.0364*** (0.0141; p=0.010) | -0.0024 (0.0135; p=0.859) | 0.0408** (0.0182; p=0.025) | 0.0275*** (0.0063; p=0.000) |
| | replicated | 0.0431*** (0.0129; p=0.001) | 0.0163 (0.0116; p=0.159) | 0.0364** (0.0153; p=0.017) | -0.0024 (0.0123; p=0.842) | 0.0408** (0.0197; p=0.038) | 0.0275*** (0.0063; p=0.000) |
| Males, permanent sigma2_v1 | published | 0.0273*** (0.0085; p=0.001) | 0.0264*** (0.0075; p=0.000) | 0.0146 (0.0121; p=0.228) | 0.0500*** (0.0142; p=0.000) | 0.0377*** (0.0106; p=0.000) | 0.0303*** (0.0049; p=0.000) |
| | replicated | 0.0273*** (0.0090; p=0.002) | 0.0264*** (0.0080; p=0.001) | 0.0146 (0.0099; p=0.139) | 0.0500*** (0.0136; p=0.000) | 0.0377*** (0.0102; p=0.000) | 0.0303*** (0.0049; p=0.000) |
| Females, transitory sigma2_u2 | published | 0.0257* (0.0142; p=0.070) | 0.0053 (0.0106; p=0.617) | 0.0157 (0.0107; p=0.142) | 0.0111 (0.0088; p=0.207) | -0.0191* (0.0116; p=0.100) | 0.0125** (0.0057; p=0.028) |
| | replicated | 0.0257* (0.0140; p=0.067) | 0.0053 (0.0101; p=0.604) | 0.0157 (0.0107; p=0.141) | 0.0111 (0.0088; p=0.206) | -0.0191 (0.0135; p=0.155) | 0.0125** (0.0057; p=0.028) |
| Females, permanent sigma2_v2 | published | 0.0442*** (0.0120; p=0.000) | 0.0447*** (0.0097; p=0.000) | 0.0245*** (0.0070; p=0.000) | 0.0324*** (0.0071; p=0.000) | 0.0506*** (0.0128; p=0.000) | 0.0382*** (0.0044; p=0.000) |
| | replicated | 0.0442*** (0.0119; p=0.000) | 0.0447*** (0.0103; p=0.000) | 0.0245*** (0.0069; p=0.000) | 0.0324*** (0.0074; p=0.000) | 0.0506*** (0.0144; p=0.000) | 0.0382*** (0.0044; p=0.000) |
| Covariance, transitory sigma_u1u2 | published | 0.0124* (0.0067; p=0.064) | 0.0060 (0.0058; p=0.301) | 0.0007 (0.0059; p=0.906) | 0.0020 (0.0048; p=0.677) | 0.0116** (0.0056; p=0.038) | 0.0058** (0.0027; p=0.032) |
| | replicated | 0.0124* (0.0065; p=0.057) | 0.0060 (0.0058; p=0.296) | 0.0007 (0.0060; p=0.904) | 0.0020 (0.0047; p=0.670) | 0.0116** (0.0056; p=0.039) | 0.0058** (0.0027; p=0.033) |
| Covariance, permanent sigma_v1v2 | published | -0.0008 (0.0067; p=0.905) | 0.0018 (0.0046; p=0.696) | 0.0051 (0.0037; p=0.168) | 0.0072* (0.0041; p=0.079) | 0.0002 (0.0053; p=0.970) | 0.0027 (0.0023; p=0.240) |
| | replicated | -0.0008 (0.0067; p=0.909) | 0.0018 (0.0046; p=0.688) | 0.0051 (0.0036; p=0.153) | 0.0072* (0.0040; p=0.069) | 0.0002 (0.0055; p=0.975) | 0.0027 (0.0023; p=0.246) |

N (husband wage-growth moments) = 7,295 (published 7,295).

### Table S0.2. Preference parameters (BPS Table 4, cols. 1, 4, 5): published vs replicated

Replicated s.e.: block bootstrap (BPS's bootstrap.do, 50 successful replications for col. 1, 50 for col. 5; BPS used 200), with the second-step GMM s.e. (not corrected for the first step) after 'GMM'; a dagger marks cells where only the GMM s.e. is available (col. 4).

| Parameter | Col. 1 published | Col. 1 replicated | Col. 4 published | Col. 4 replicated | Col. 5 published | Col. 5 replicated |
|---|---|---|---|---|---|---|
| pi | 0.150*** (0.004; p=0.000) | 0.150*** (0.004; p=0.000) | 0.150*** (0.004; p=0.000) | 0.150 | 0.150*** (0.004; p=0.000) | 0.150*** (0.004; p=0.000) |
| s_report | 0.708*** (0.013; p=0.000) | 0.708*** (0.013; p=0.000; GMM 0.000) | 0.708*** (0.013; p=0.000) | 0.708 | 0.708*** (0.013; p=0.000) | 0.708*** (0.013; p=0.000; GMM 0.000) |
| eta_c_p | 0.417*** (0.122; p=0.001) | 0.418** (0.174; p=0.016; GMM 0.068) | 0.494*** (0.168; p=0.003) | 0.493*** (0.077†; p=0.000) | 0.433*** (0.121; p=0.000) | 0.434*** (0.152; p=0.004; GMM 0.059) |
| eta_h1_w1 | 0.681*** (0.189; p=0.000) | 0.681*** (0.133; p=0.000; GMM 0.071) | 0.653*** (0.178; p=0.000) | 0.654*** (0.071†; p=0.000) | 0.697*** (0.189; p=0.000) | 0.696*** (0.114; p=0.000; GMM 0.068) |
| eta_h2_w2 | 0.958*** (0.267; p=0.000) | 0.958*** (0.225; p=0.000; GMM 0.095) | 0.976*** (0.281; p=0.001) | 0.976*** (0.096†; p=0.000) | 0.961*** (0.271; p=0.000) | 0.962*** (0.213; p=0.000; GMM 0.094) |
| eta_c_w1 | -0.162** (0.074; p=0.029) | -0.162* (0.086; p=0.059; GMM 0.034) | -0.182*** (0.066; p=0.006) | -0.182*** (0.033†; p=0.000) | -0.169** (0.070; p=0.016) | -0.170*** (0.061; p=0.006; GMM 0.032) |
| eta_h1_p | 0.126** (0.057; p=0.027) | 0.126** (0.060; p=0.037; GMM 0.026) | 0.141*** (0.052; p=0.007) | 0.141*** (0.026†; p=0.000) | 0.131** (0.055; p=0.017) | 0.131*** (0.050; p=0.008; GMM 0.025) |
| eta_c_w2 | -0.050 (0.077; p=0.516) | -0.050 (0.078; p=0.518; GMM 0.030) | -0.072 (0.090; p=0.424) | -0.072** (0.032†; p=0.024) | -0.049 (0.074; p=0.508) | -0.049 (0.068; p=0.476; GMM 0.030) |
| eta_h2_p | 0.079 (0.121; p=0.514) | 0.079 (0.122; p=0.516; GMM 0.047) | 0.114 (0.140; p=0.415) | 0.113** (0.050†; p=0.024) | 0.077 (0.116; p=0.507) | 0.077 (0.108; p=0.476; GMM 0.047) |
| eta_h1_w2 | 0.159** (0.071; p=0.025) | 0.159** (0.079; p=0.045; GMM 0.021) | 0.160** (0.068; p=0.019) | 0.160*** (0.020†; p=0.000) | 0.166** (0.068; p=0.015) | 0.166** (0.072; p=0.022; GMM 0.021) |
| eta_h2_w1 | 0.325** (0.140; p=0.020) | 0.325** (0.158; p=0.040; GMM 0.042) | 0.325** (0.138; p=0.019) | 0.325*** (0.041†; p=0.000) | 0.339** (0.136; p=0.013) | 0.339** (0.157; p=0.031; GMM 0.043) |
| beta | - | - | - | - | -0.137 (0.270; p=0.612) | -0.138 (0.213; p=0.519; GMM 0.150) |

N = 7,295 in all three columns (published 7,295).

### Table S0.3. Frisch and Marshallian elasticities (BPS Table 5, col. 1, before-tax wage change)

| Elasticity | Published | Replicated (bootstrap s.e.) |
|---|---|---|
| Frisch: male labor supply | 0.58*** (0.16; p=0.000) | 0.58*** (0.10; p=0.000) |
| Frisch: female labor supply | 0.88*** (0.23; p=0.000) | 0.88*** (0.20; p=0.000) |
| Frisch: male labor supply / female wage | 0.11* (0.06; p=0.067) | 0.11* (0.06; p=0.089) |
| Frisch: female labor supply / male wage | 0.17 (0.11; p=0.122) | 0.17 (0.11; p=0.131) |
| Frisch: consumption / male wage | -0.14** (0.07; p=0.046) | -0.14** (0.07; p=0.041) |
| Frisch: consumption / female wage | -0.04 (0.07; p=0.568) | -0.04 (0.07; p=0.592) |
| Marshallian: male labor supply | -0.08 (0.08; p=0.317) | -0.08 (0.11; p=0.464) |
| Marshallian: female labor supply | 0.42*** (0.08; p=0.000) | 0.42*** (0.11; p=0.000) |
| Marshallian: male labor supply / female wage | -0.22*** (0.04; p=0.000) | -0.22*** (0.05; p=0.000) |
| Marshallian: female labor supply / male wage | -0.75*** (0.14; p=0.000) | -0.75*** (0.10; p=0.000) |
| Marshallian: consumption / male wage | 0.32*** (0.05; p=0.000) | 0.32*** (0.06; p=0.000) |
| Marshallian: consumption / female wage | 0.19*** (0.03; p=0.000) | 0.19*** (0.04; p=0.000) |

### Table S0.4. Insurance accounting (BPS p. 425-426): response of consumption to a 10% permanent fall in the husband's wage, percent

| Step | Published | Replicated (bootstrap s.e.) |
|---|---|---|
| Fixed labor supply, no taxes, no savings (= 10 E[s]) | 7.1 | 7.09*** (0.13; p=0.000) |
| + progressive taxes and transfers | 6.3 | 6.33*** (0.12; p=0.000) |
| + husband's labor supply | 5.8 | 5.79*** (0.70; p=0.000) |
| + wife's labor supply (household earnings) | 3.9 | 3.88*** (0.69; p=0.000) |
| + savings (consumption) | 3.2 | 3.16*** (0.57; p=0.000) |
| Share: government | 0.2 | 0.194*** (0.031; p=0.000) |
| Share: family labor supply | 0.63 | 0.623*** (0.093; p=0.000) |
| Share: savings | 0.17 | 0.183*** (0.060; p=0.002) |
| Food-Stamp eligible: fixed labor supply | 7.2 | 7.15*** (0.18; p=0.000) |
| FS: + taxes and transfers | 3.6 | 3.57*** (0.15; p=0.000) |
| FS: + wife's labor supply | 2.3 | 2.32*** (0.38; p=0.000) |
| FS: + savings | 2.1 | 2.08*** (0.36; p=0.000) |
| FS: share government | 0.71 | 0.706*** (0.051; p=0.000) |

BPS's 20 / 63 / 17 split is stated in rounded percentage points of a 39 p.p. total (8 / 25 / 7 p.p.); the replicated unrounded chain gives 7.6 / 24.5 / 7.2 p.p. of 39.3 p.p.

## Step 1. Relaxing the restrictions

Columns = specifications (one estimation each); rows = parameters. Wage-process rows: stationary ('all ages') GMM of T4C41 with GMM s.e.; correlations = covariance / sqrt(product of variances), no s.e. (the test of the covariance is the test of the correlation). Preference, elasticity, chain and share rows: T4C1 (age-varying variances) with bootstrap s.e. where a bootstrap was run (last row), else GMM s.e. (†) or none (chain rows). beta: T4C5. 'n.c.' = GMM did not converge. Black couples: the residual and pi / s steps run, but the preference step is not identified (see summary).

### Table S1. Relaxing BPS's restrictions one at a time and together (PSID 1999-2009)

| Parameter | BPS baseline | baseline without 1997 immigrants (fn. 15) | (a) year-level no-work drop | (b) no status controls | (c) both trims off | (c) jump trim off | (c) min-wage trim off | (d) SEO in | (d) SEO in, weighted | (d) no SEO, weighted | (d) White, SEO in | (d) Black, SEO in | (d) White, no SEO | (e) break on spouse identity | (f) a+b+c+e, no SEO | (f) all, SEO in | (f) all, SEO in, weighted |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Var. transitory, husband (sigma2_u1) | 0.0275*** (0.0063; p=0.000) | 0.0343*** (0.0071; p=0.000) | 0.0300*** (0.0065; p=0.000) | 0.0275*** (0.0063; p=0.000) | 0.1010*** (0.0264; p=0.000) | 0.0555*** (0.0107; p=0.000) | 0.0396*** (0.0088; p=0.000) | 0.0280*** (0.0056; p=0.000) | 0.0285*** (0.0060; p=0.000) | 0.0247*** (0.0061; p=0.000) | 0.0390*** (0.0076; p=0.000) | 0.0216** (0.0086; p=0.012) | 0.0390*** (0.0076; p=0.000) | 0.0274*** (0.0063; p=0.000) | 0.1003*** (0.0255; p=0.000) | 0.0996*** (0.0224; p=0.000) | 0.1043*** (0.0226; p=0.000) |
| Var. permanent, husband (sigma2_v1) | 0.0303*** (0.0049; p=0.000) | 0.0299*** (0.0055; p=0.000) | 0.0315*** (0.0050; p=0.000) | 0.0303*** (0.0049; p=0.000) | 0.0269** (0.0116; p=0.021) | 0.0190*** (0.0059; p=0.001) | 0.0450*** (0.0079; p=0.000) | 0.0299*** (0.0043; p=0.000) | 0.0276*** (0.0043; p=0.000) | 0.0279*** (0.0044; p=0.000) | 0.0264*** (0.0055; p=0.000) | 0.0339*** (0.0095; p=0.000) | 0.0264*** (0.0055; p=0.000) | 0.0302*** (0.0049; p=0.000) | 0.0291** (0.0116; p=0.012) | 0.0266*** (0.0101; p=0.008) | 0.0285** (0.0114; p=0.012) |
| Var. transitory, wife (sigma2_u2) | 0.0125** (0.0057; p=0.028) | 0.0128** (0.0058; p=0.028) | 0.0144** (0.0057; p=0.012) | 0.0125** (0.0057; p=0.028) | 0.0487*** (0.0112; p=0.000) | 0.0321*** (0.0081; p=0.000) | 0.0239*** (0.0075; p=0.001) | 0.0189*** (0.0055; p=0.001) | 0.0171*** (0.0063; p=0.006) | 0.0135** (0.0063; p=0.032) | 0.0138** (0.0066; p=0.035) | 0.0271** (0.0136; p=0.047) | 0.0139** (0.0066; p=0.035) | 0.0124** (0.0057; p=0.028) | 0.0559*** (0.0120; p=0.000) | 0.0600*** (0.0114; p=0.000) | 0.0533*** (0.0112; p=0.000) |
| Var. permanent, wife (sigma2_v2) | 0.0382*** (0.0044; p=0.000) | 0.0387*** (0.0046; p=0.000) | 0.0364*** (0.0043; p=0.000) | 0.0382*** (0.0044; p=0.000) | 0.0426*** (0.0083; p=0.000) | 0.0292*** (0.0050; p=0.000) | 0.0525*** (0.0077; p=0.000) | 0.0375*** (0.0042; p=0.000) | 0.0369*** (0.0045; p=0.000) | 0.0382*** (0.0046; p=0.000) | 0.0386*** (0.0050; p=0.000) | 0.0299*** (0.0089; p=0.001) | 0.0384*** (0.0050; p=0.000) | 0.0382*** (0.0044; p=0.000) | 0.0382*** (0.0084; p=0.000) | 0.0387*** (0.0078; p=0.000) | 0.0426*** (0.0085; p=0.000) |
| Cov. transitory shocks (sigma_u1u2) | 0.0058** (0.0027; p=0.033) | 0.0060** (0.0029; p=0.037) | 0.0061** (0.0029; p=0.034) | 0.0058** (0.0027; p=0.033) | 0.0078* (0.0041; p=0.057) | 0.0043 (0.0035; p=0.221) | 0.0073** (0.0034; p=0.029) | 0.0060** (0.0025; p=0.018) | 0.0047* (0.0027; p=0.081) | 0.0050* (0.0027; p=0.067) | 0.0066** (0.0031; p=0.034) | 0.0050 (0.0047; p=0.286) | 0.0066** (0.0031; p=0.034) | 0.0057** (0.0027; p=0.034) | 0.0089** (0.0041; p=0.031) | 0.0100*** (0.0037; p=0.007) | 0.0079* (0.0044; p=0.071) |
|   correlation, transitory | 0.31 | 0.28 | 0.29 | 0.31 | 0.11 | 0.10 | 0.24 | 0.26 | 0.21 | 0.28 | 0.28 | 0.21 | 0.28 | 0.31 | 0.12 | 0.13 | 0.11 |
| Cov. permanent shocks (sigma_v1v2) | 0.0027 (0.0023; p=0.246) | 0.0026 (0.0024; p=0.286) | 0.0022 (0.0023; p=0.342) | 0.0027 (0.0023; p=0.246) | 0.0014 (0.0034; p=0.679) | 0.0039 (0.0025; p=0.120) | 0.0011 (0.0032; p=0.728) | 0.0031 (0.0022; p=0.149) | 0.0031 (0.0022; p=0.168) | 0.0027 (0.0023; p=0.249) | 0.0030 (0.0026; p=0.236) | 0.0034 (0.0038; p=0.369) | 0.0029 (0.0026; p=0.264) | 0.0027 (0.0023; p=0.243) | 0.0006 (0.0034; p=0.864) | 0.0003 (0.0030; p=0.915) | 0.0007 (0.0037; p=0.842) |
|   correlation, permanent | 0.08 | 0.08 | 0.07 | 0.08 | 0.04 | 0.16 | 0.02 | 0.09 | 0.10 | 0.08 | 0.10 | 0.11 | 0.09 | 0.08 | 0.02 | 0.01 | 0.02 |
| E(pi) | 0.150*** (0.004; p=0.000) | 0.155*** (0.004; p=0.000) | 0.152*** (0.004; p=0.000) | 0.150*** (0.004; p=0.000) | 0.154*** (0.006; p=0.000) | 0.151*** (0.004; p=0.000) | 0.154*** (0.006; p=0.000) | 0.140*** (0.003; p=0.000) | 0.140*** (0.003; p=0.000) | 0.150 | 0.158*** (0.004; p=0.000) | 0.081*** (0.006; p=0.000) | 0.159 | 0.150*** (0.004; p=0.000) | 0.157 | 0.146*** (0.004; p=0.000) | 0.146*** (0.004; p=0.000) |
| E(s) | 0.708*** (0.013; p=0.000) | 0.704*** (0.009; p=0.000) | 0.697*** (0.016; p=0.000) | 0.708*** (0.013; p=0.000) | 0.707*** (0.008; p=0.000) | 0.708*** (0.014; p=0.000) | 0.706*** (0.008; p=0.000) | 0.701*** (0.010; p=0.000) | 0.701*** (0.010; p=0.000) | 0.708 | 0.708*** (0.012; p=0.000) | 0.651*** (0.025; p=0.000) | 0.707 | 0.708*** (0.009; p=0.000) | 0.696 | 0.687*** (0.011; p=0.000) | 0.687*** (0.012; p=0.000) |
| eta_c,p | 0.418** (0.174; p=0.016) | 0.425* (0.232; p=0.067) | 0.516*** (0.173; p=0.003) | 0.430*** (0.163; p=0.008) | 0.068 (0.157; p=0.665) | 0.079 (0.069; p=0.247) | 0.259*** (0.081; p=0.001) | 0.311 (0.197; p=0.113) | 0.267* (0.148; p=0.072) | 0.394*** (0.068†; p=0.000) | 0.566 (0.394; p=0.151) | 0.075 (0.138; p=0.588) | 0.575*** (0.115†; p=0.000) | 0.418** (0.197; p=0.034) | 0.047 (0.039†; p=0.229) | 0.010 (0.073; p=0.886) | 0.024 (0.090; p=0.788) |
| eta_h1,w1 | 0.681*** (0.133; p=0.000) | 0.522*** (0.171; p=0.002) | 0.647*** (0.117; p=0.000) | 0.700*** (0.139; p=0.000) | 0.286*** (0.110; p=0.009) | 0.508*** (0.108; p=0.000) | 0.651** (0.256; p=0.011) | 0.719*** (0.175; p=0.000) | 0.704*** (0.197; p=0.000) | 0.764*** (0.078†; p=0.000) | 0.420*** (0.136; p=0.002) | 0.876* (0.450; p=0.051) | 0.418*** (0.067†; p=0.000) | 0.682*** (0.229; p=0.003) | 0.311*** (0.104†; p=0.003) | 0.213* (0.111; p=0.055) | 0.224*** (0.086; p=0.009) |
| eta_h2,w2 | 0.958*** (0.225; p=0.000) | 1.015*** (0.273; p=0.000) | 0.957*** (0.189; p=0.000) | 1.009*** (0.233; p=0.000) | 0.527*** (0.131; p=0.000) | 0.840*** (0.244; p=0.001) | 0.640*** (0.113; p=0.000) | 0.846*** (0.161; p=0.000) | 0.932*** (0.241; p=0.000) | 0.912*** (0.094†; p=0.000) | 1.053*** (0.303; p=0.000) | 0.478** (0.194; p=0.014) | 1.040*** (0.115†; p=0.000) | 0.960*** (0.235; p=0.000) | 0.528*** (0.109†; p=0.000) | 0.487*** (0.075; p=0.000) | 0.573*** (0.138; p=0.000) |
| eta_c,w1 | -0.162* (0.086; p=0.059) | -0.134* (0.072; p=0.062) | -0.167** (0.072; p=0.020) | -0.168** (0.080; p=0.037) | 0.037 (0.038; p=0.332) | 0.055** (0.025; p=0.031) | -0.086 (0.100; p=0.388) | -0.105 (0.091; p=0.249) | -0.081 (0.094; p=0.389) | -0.178*** (0.038†; p=0.000) | -0.137** (0.070; p=0.050) | 0.091 (0.115; p=0.426) | -0.137*** (0.028†; p=0.000) | -0.163* (0.083; p=0.051) | 0.044*** (0.013†; p=0.001) | 0.025 (0.027; p=0.354) | 0.029 (0.024; p=0.220) |
| eta_h1,p | 0.126** (0.060; p=0.037) | 0.100* (0.053; p=0.056) | 0.131** (0.057; p=0.022) | 0.130** (0.057; p=0.022) | -0.029 (0.030; p=0.333) | -0.043** (0.021; p=0.042) | 0.067 (0.079; p=0.396) | 0.083 (0.071; p=0.247) | 0.064 (0.075; p=0.390) | 0.138*** (0.029†; p=0.000) | 0.101** (0.049; p=0.042) | -0.083 (0.106; p=0.431) | 0.101*** (0.020†; p=0.000) | 0.126** (0.064; p=0.047) | -0.035*** (0.010†; p=0.001) | -0.020 (0.022; p=0.356) | -0.024 (0.019; p=0.212) |
| eta_c,w2 | -0.050 (0.078; p=0.518) | -0.059 (0.096; p=0.539) | -0.054 (0.068; p=0.425) | -0.053 (0.080; p=0.506) | 0.050 (0.076; p=0.515) | 0.041 (0.043; p=0.345) | 0.011 (0.035; p=0.757) | -0.027 (0.054; p=0.623) | -0.024 (0.042; p=0.573) | -0.054* (0.030†; p=0.066) | -0.154 (0.116; p=0.186) | 0.052 (0.070; p=0.454) | -0.154*** (0.043†; p=0.000) | -0.051 (0.088; p=0.562) | 0.023 (0.035†; p=0.512) | 0.003 (0.056; p=0.963) | 0.025 (0.034; p=0.464) |
| eta_h2,p | 0.079 (0.122; p=0.516) | 0.091 (0.146; p=0.534) | 0.084 (0.107; p=0.431) | 0.084 (0.128; p=0.508) | -0.081 (0.121; p=0.506) | -0.065 (0.067; p=0.330) | -0.017 (0.056; p=0.756) | 0.041 (0.084; p=0.624) | 0.036 (0.064; p=0.574) | 0.086* (0.047†; p=0.066) | 0.241 (0.178; p=0.176) | -0.066 (0.088; p=0.450) | 0.240*** (0.068†; p=0.000) | 0.080 (0.138; p=0.561) | -0.037 (0.056†; p=0.512) | -0.004 (0.087; p=0.963) | -0.039 (0.053; p=0.460) |
| eta_h1,w2 | 0.159** (0.079; p=0.045) | 0.140** (0.060; p=0.020) | 0.137* (0.078; p=0.080) | 0.165** (0.083; p=0.046) | 0.030 (0.063; p=0.632) | 0.098* (0.054; p=0.072) | 0.159** (0.062; p=0.011) | 0.146*** (0.050; p=0.003) | 0.182** (0.084; p=0.029) | 0.170*** (0.022†; p=0.000) | 0.071 (0.061; p=0.248) | 0.278* (0.158; p=0.078) | 0.067*** (0.019†; p=0.000) | 0.160*** (0.051; p=0.002) | 0.032 (0.029†; p=0.262) | 0.034 (0.055; p=0.530) | 0.059 (0.049; p=0.222) |
| eta_h2,w1 | 0.325** (0.158; p=0.040) | 0.289** (0.130; p=0.026) | 0.274* (0.163; p=0.093) | 0.337** (0.162; p=0.038) | 0.062 (0.132; p=0.641) | 0.199* (0.114; p=0.079) | 0.326*** (0.124; p=0.009) | 0.285*** (0.100; p=0.004) | 0.354** (0.164; p=0.031) | 0.346*** (0.045†; p=0.000) | 0.151 (0.138; p=0.274) | 0.387* (0.233; p=0.096) | 0.143*** (0.040†; p=0.000) | 0.327*** (0.105; p=0.002) | 0.065 (0.058†; p=0.262) | 0.066 (0.103; p=0.521) | 0.114 (0.090; p=0.206) |
| Marshallian: wife's hours / husband's wage (kappa_h2,v1) | -0.752*** (0.098; p=0.000) | -0.777*** (0.136; p=0.000) | -0.691*** (0.119; p=0.000) | -0.773*** (0.093; p=0.000) | -1.322** (0.570; p=0.020) | -1.358*** (0.227; p=0.000) | -0.647*** (0.136; p=0.000) | -0.768*** (0.180; p=0.000) | -0.849*** (0.172; p=0.000) | -0.733 | -0.764*** (0.208; p=0.000) | -0.726** (0.309; p=0.019) | -0.754 | -0.753*** (0.142; p=0.000) | -1.302 | -1.423* (0.782; p=0.069) | -1.501*** (0.556; p=0.007) |
| Marshallian: husband own (kappa_h1,v1 - 1) | -0.079 (0.108; p=0.464) | -0.058 (0.136; p=0.673) | -0.020 (0.081; p=0.808) | -0.068 (0.102; p=0.500) | -0.495* (0.253; p=0.050) | -0.392** (0.174; p=0.024) | -0.245*** (0.058; p=0.000) | -0.130 (0.127; p=0.305) | -0.159** (0.073; p=0.030) | -0.093 | 0.046 (0.108; p=0.670) | -0.615*** (0.190; p=0.001) | 0.048 | -0.079 (0.123; p=0.519) | -0.447 | -0.403 (0.372; p=0.280) | -0.424*** (0.160; p=0.008) |
| Marshallian: wife own (kappa_h2,v2 - 1) | 0.425*** (0.106; p=0.000) | 0.406*** (0.103; p=0.000) | 0.459*** (0.065; p=0.000) | 0.452*** (0.115; p=0.000) | -0.086 (0.279; p=0.756) | 0.043 (0.184; p=0.817) | 0.235** (0.098; p=0.016) | 0.341*** (0.099; p=0.001) | 0.320*** (0.102; p=0.002) | 0.407 | 0.428*** (0.089; p=0.000) | -0.092 (0.228; p=0.685) | 0.429 | 0.425*** (0.066; p=0.000) | -0.171 | -0.371 (0.465; p=0.425) | -0.356 (0.280; p=0.203) |
| Marshallian: consumption / husband's wage (kappa_c,v1) | 0.316*** (0.057; p=0.000) | 0.320*** (0.090; p=0.000) | 0.347*** (0.047; p=0.000) | 0.318*** (0.069; p=0.000) | -0.015 (0.247; p=0.951) | 0.028 (0.101; p=0.780) | 0.245*** (0.051; p=0.000) | 0.279*** (0.091; p=0.002) | 0.246*** (0.070; p=0.000) | 0.307 | 0.383*** (0.073; p=0.000) | -0.005 (0.157; p=0.976) | 0.385 | 0.317*** (0.077; p=0.000) | -0.005 | -0.021 (0.371; p=0.954) | -0.046 (0.166; p=0.782) |
| Chain (10% perm. fall): fixed labor supply, no taxes, no savings | 7.09*** (0.13; p=0.000) | 7.05*** (0.09; p=0.000) | 6.98*** (0.17; p=0.000) | 7.09*** (0.13; p=0.000) | 7.07*** (0.08; p=0.000) | 7.09*** (0.14; p=0.000) | 7.07*** (0.07; p=0.000) | 7.01*** (0.10; p=0.000) | 7.07*** (0.07; p=0.000) | 7.09 | 7.08*** (0.12; p=0.000) | 6.49*** (0.25; p=0.000) | 7.08 | 7.09*** (0.09; p=0.000) | 6.96 | 6.88*** (0.11; p=0.000) | 6.91*** (0.14; p=0.000) |
|   + taxes and transfers | 6.33*** (0.12; p=0.000) | 6.35*** (0.07; p=0.000) | 6.22*** (0.16; p=0.000) | 6.33*** (0.12; p=0.000) | 6.28*** (0.08; p=0.000) | 6.33*** (0.13; p=0.000) | 6.28*** (0.07; p=0.000) | 6.26*** (0.08; p=0.000) | 6.32*** (0.06; p=0.000) | 6.34 | 6.39*** (0.11; p=0.000) | 5.79*** (0.21; p=0.000) | 6.38 | 6.33*** (0.08; p=0.000) | 6.17 | 6.09*** (0.10; p=0.000) | 6.15*** (0.13; p=0.000) |
|   + husband's labor supply | 5.79*** (0.70; p=0.000) | 5.95*** (0.94; p=0.000) | 6.07*** (0.59; p=0.000) | 5.86*** (0.67; p=0.000) | 3.11* (1.70; p=0.067) | 3.78*** (1.07; p=0.000) | 4.69*** (0.41; p=0.000) | 5.40*** (0.81; p=0.000) | 5.28*** (0.49; p=0.000) | 5.71 | 6.66*** (0.60; p=0.000) | 2.16* (1.17; p=0.065) | 6.67 | 5.79*** (0.75; p=0.000) | 3.35 | 3.57 (2.32; p=0.124) | 3.47*** (0.94; p=0.000) |
|   + wife's labor supply | 3.88*** (0.69; p=0.000) | 3.95*** (1.08; p=0.000) | 4.25*** (0.53; p=0.000) | 3.90*** (0.83; p=0.000) | -0.20 (3.02; p=0.947) | 0.38 (1.18; p=0.750) | 3.05*** (0.62; p=0.000) | 3.40*** (1.08; p=0.002) | 3.10*** (0.83; p=0.000) | 3.84 | 4.70*** (0.85; p=0.000) | -0.06 (1.76; p=0.975) | 4.73 | 3.89*** (0.89; p=0.000) | -0.03 | -0.22 (4.48; p=0.960) | -0.52 (2.11; p=0.805) |
|   + savings (= 10 x kappa_c,v1) | 3.16*** (0.57; p=0.000) | 3.20*** (0.90; p=0.000) | 3.47*** (0.47; p=0.000) | 3.18*** (0.69; p=0.000) | -0.15 (2.47; p=0.951) | 0.28 (1.01; p=0.780) | 2.45*** (0.51; p=0.000) | 2.79*** (0.91; p=0.002) | 2.46*** (0.70; p=0.000) | 3.07 | 3.83*** (0.73; p=0.000) | -0.05 (1.57; p=0.976) | 3.85 | 3.17*** (0.77; p=0.000) | -0.05 | -0.21 (3.71; p=0.954) | -0.46 (1.66; p=0.782) |
| Share of insurance: government | 0.194*** (0.031; p=0.000) | 0.181*** (0.040; p=0.000) | 0.215*** (0.030; p=0.000) | 0.194*** (0.035; p=0.000) | 0.109 (0.072; p=0.131) | 0.112*** (0.020; p=0.000) | 0.171*** (0.021; p=0.000) | 0.179*** (0.042; p=0.000) | 0.162*** (0.028; p=0.000) | 0.187 | 0.215*** (0.052; p=0.000) | 0.108*** (0.030; p=0.000) | 0.216 | 0.194*** (0.040; p=0.000) | 0.112 | 0.110 (0.221; p=0.617) | 0.104** (0.044; p=0.017) |
| Share of insurance: family labor supply | 0.623*** (0.093; p=0.000) | 0.626*** (0.129; p=0.000) | 0.561*** (0.086; p=0.000) | 0.621*** (0.099; p=0.000) | 0.897*** (0.219; p=0.000) | 0.875*** (0.063; p=0.000) | 0.700*** (0.054; p=0.000) | 0.678*** (0.110; p=0.000) | 0.700*** (0.081; p=0.000) | 0.621 | 0.517*** (0.155; p=0.001) | 0.893*** (0.064; p=0.000) | 0.511 | 0.623*** (0.109; p=0.000) | 0.886 | 0.891 (0.604; p=0.140) | 0.904*** (0.144; p=0.000) |
| Share of insurance: savings | 0.183*** (0.060; p=0.002) | 0.193** (0.086; p=0.025) | 0.224*** (0.057; p=0.000) | 0.185*** (0.064; p=0.004) | -0.007 (0.147; p=0.964) | 0.014 (0.043; p=0.752) | 0.129*** (0.035; p=0.000) | 0.143** (0.068; p=0.035) | 0.138** (0.054; p=0.010) | 0.192 | 0.268*** (0.103; p=0.009) | -0.001 (0.035; p=0.974) | 0.273 | 0.183*** (0.069; p=0.008) | 0.002 | -0.002 (0.383; p=0.997) | -0.008 (0.100; p=0.933) |
| Outside insurance beta (Table 4 col. 5 spec.) | -0.138 (0.213; p=0.519) | -0.113 (0.144†; p=0.431) | -0.029 (0.270; p=0.915) | -0.105 (0.188; p=0.578) | 0.840 (0.649; p=0.196) | -1.782 (3.224†; p=0.581) | 0.252* (0.145†; p=0.082) | -0.273 (0.307; p=0.374) | 0.059 (0.660; p=0.929) | -0.035 (0.149†; p=0.811) | -0.197 (0.344; p=0.567) | 7.004 (16.218†; p=0.666) | -0.215 (0.158†; p=0.174) | -0.140 (0.291; p=0.631) | n.c. | n.c. | 0.914*** (0.045†; p=0.000) |
| N (preference GMM, household-years) | 7,295 | 6,493 | 7,642 | 7,295 | 7,439 | 7,341 | 7,396 | 8,795 | 8,729 | 7,233 | 5,920 | 1,625 | 5,900 | 7,308 | 7,827 | 9,483 | 9,410 |
| N (household-years in data4estimation) | 10,479 | 9,311 | 11,116 | 10,479 | 10,437 | 10,479 | 10,437 | 12,695 | 12,695 | 10,479 | 8,472 | 2,428 | 8,436 | 10,487 | 11,111 | 13,570 | 13,570 |
| Bootstrap replications (preference / beta) | 50 / 50 | 50 / 0 | 50 / 50 | 50 / 50 | 48 / 48 | 50 / 0 | 50 / 0 | 50 / 50 | 50 / 50 | 0 / 0 | 50 / 50 | 47 / 0 | 0 / 0 | 50 / 50 | 0 / 0 | 47 / 0 | 46 / 0 |

### Table S1e. Couples lost to separation at BPS's composition break

Married couples (husband 30-57, head in IGE person file, income years 1998-2006 so that the next wave exists). sep_obs = at the head's next interview the marriage has ended or the wife is another person (heads observed again); bps_break_next = the next interview carries fchg > 1 (BPS drop that year and restart the household). Cell: share [events / couple-years]; differences = linear probability, s.e. clustered by head.

| Sample | Outcome | No displacement | Husband only | Wife only | Joint | Husband only - none | Wife only - none | Joint - none |
|---|---|---|---|---|---|---|---|---|
| SRC+SEO | sep_obs | 0.0282 [289/10,250] | 0.0386 [17/440] | 0.0572 [17/297] | 0.0930 [4/43] | 0.0104 (0.0093; p=0.260) | 0.0290** (0.0136; p=0.033) | 0.0648 (0.0446; p=0.146) |
| SRC+SEO | bps_break_next | 0.0281 [288/10,250] | 0.0409 [18/440] | 0.0572 [17/297] | 0.0930 [4/43] | 0.0128 (0.0095; p=0.178) | 0.0291** (0.0136; p=0.032) | 0.0649 (0.0446; p=0.145) |
| SRC (BPS) | sep_obs | 0.0240 [196/8,158] | 0.0326 [11/337] | 0.0570 [13/228] | 0.1000 [3/30] | 0.0086 (0.0098; p=0.379) | 0.0330** (0.0155; p=0.034) | 0.0760 (0.0550; p=0.167) |
| SRC (BPS) | bps_break_next | 0.0239 [195/8,158] | 0.0356 [12/337] | 0.0614 [14/228] | 0.1000 [3/30] | 0.0117 (0.0102; p=0.250) | 0.0375** (0.0160; p=0.019) | 0.0761 (0.0550; p=0.167) |

Counts: SRC+SEO: couples_ending_in_separation (all) = 327; SRC+SEO: couples_ending_in_separation (any displacement before) = 38; SRC+SEO: couples (all) = 3,689; SRC (BPS): couples_ending_in_separation (all) = 223; SRC (BPS): couples_ending_in_separation (any displacement before) = 27; SRC (BPS): couples (all) = 2,861

## Step 2. Displacement and joint displacement in BPS's panel

### Table S2.1. Couple-years with a displacement in BPS's panel

Share of BPS couple-years (head in IGE's PSID person file: BPS's rows less the 1997 immigrant refresher) whose two-year interval (calendar years t-1, t) contains a displacement (closure or layoff, own report). Cell: share [events].

Sample: base

| Rows | Husband displaced | Wife displaced | Joint (same interval) | Joint (same year) | Husband: closure | Wife: closure | Wife: any job end | N |
|---|---|---|---|---|---|---|---|---|
| all rows | 0.0445 [414] | 0.0309 [288] | 0.0030 [28] | 0.0025 [23] | 0.0141 [131] | 0.0122 [114] | 0.1564 [1456] | 9,311 |
| rows with husband wage difference | 0.0465 [302] | 0.0291 [189] | 0.0026 [17] | 0.0020 [13] | 0.0148 [96] | 0.0116 [75] | 0.1441 [935] | 6,489 |
| rows with both wage differences | 0.0445 [216] | 0.0335 [163] | 0.0033 [16] | 0.0025 [12] | 0.0128 [62] | 0.0134 [65] | 0.1585 [770] | 4,859 |

Wife displaced in the same interval: P(wd|hd) = 0.0676 (N=414, events=28); P(wd|no hd) = 0.0292 (N=8897, events=260); P(wd|hd,wemp t-2) = 0.0675 (N=237, events=16); P(wd|no hd,wemp t-2) = 0.0305 (N=5174, events=158)

Sample: b_nostatus

| Rows | Husband displaced | Wife displaced | Joint (same interval) | Joint (same year) | Husband: closure | Wife: closure | Wife: any job end | N |
|---|---|---|---|---|---|---|---|---|
| all rows | 0.0445 [414] | 0.0309 [288] | 0.0030 [28] | 0.0025 [23] | 0.0141 [131] | 0.0122 [114] | 0.1564 [1456] | 9,311 |
| rows with husband wage difference | 0.0465 [302] | 0.0291 [189] | 0.0026 [17] | 0.0020 [13] | 0.0148 [96] | 0.0116 [75] | 0.1441 [935] | 6,489 |
| rows with both wage differences | 0.0445 [216] | 0.0335 [163] | 0.0033 [16] | 0.0025 [12] | 0.0128 [62] | 0.0134 [65] | 0.1585 [770] | 4,859 |

Wife displaced in the same interval: P(wd|hd) = 0.0676 (N=414, events=28); P(wd|no hd) = 0.0292 (N=8897, events=260); P(wd|hd,wemp t-2) = 0.0675 (N=237, events=16); P(wd|no hd,wemp t-2) = 0.0305 (N=5174, events=158)

Sample: a_nowork

| Rows | Husband displaced | Wife displaced | Joint (same interval) | Joint (same year) | Husband: closure | Wife: closure | Wife: any job end | N |
|---|---|---|---|---|---|---|---|---|
| all rows | 0.0458 [452] | 0.0311 [307] | 0.0032 [32] | 0.0026 [26] | 0.0148 [146] | 0.0121 [119] | 0.1561 [1539] | 9,861 |
| rows with husband wage difference | 0.0463 [314] | 0.0287 [195] | 0.0025 [17] | 0.0019 [13] | 0.0149 [101] | 0.0111 [75] | 0.1436 [974] | 6,784 |
| rows with both wage differences | 0.0443 [225] | 0.0331 [168] | 0.0031 [16] | 0.0024 [12] | 0.0128 [65] | 0.0128 [65] | 0.1576 [801] | 5,081 |

Wife displaced in the same interval: P(wd|hd) = 0.0708 (N=452, events=32); P(wd|no hd) = 0.0292 (N=9409, events=275); P(wd|hd,wemp t-2) = 0.0645 (N=248, events=16); P(wd|no hd,wemp t-2) = 0.0303 (N=5416, events=164)

Sample: d_seo

| Rows | Husband displaced | Wife displaced | Joint (same interval) | Joint (same year) | Husband: closure | Wife: closure | Wife: any job end | N |
|---|---|---|---|---|---|---|---|---|
| all rows | 0.0460 [530] | 0.0318 [366] | 0.0030 [35] | 0.0025 [29] | 0.0143 [165] | 0.0117 [135] | 0.1559 [1797] | 11,527 |
| rows with husband wage difference | 0.0474 [379] | 0.0299 [239] | 0.0029 [23] | 0.0023 [18] | 0.0148 [118] | 0.0110 [88] | 0.1440 [1150] | 7,988 |
| rows with both wage differences | 0.0457 [276] | 0.0338 [204] | 0.0036 [22] | 0.0028 [17] | 0.0129 [78] | 0.0129 [78] | 0.1569 [948] | 6,042 |

Wife displaced in the same interval: P(wd|hd) = 0.0660 (N=530, events=35); P(wd|no hd) = 0.0301 (N=10997, events=331); P(wd|hd,wemp t-2) = 0.0728 (N=302, events=22); P(wd|no hd,wemp t-2) = 0.0311 (N=6396, events=199)

Sample: f_all

| Rows | Husband displaced | Wife displaced | Joint (same interval) | Joint (same year) | Husband: closure | Wife: closure | Wife: any job end | N |
|---|---|---|---|---|---|---|---|---|
| all rows | 0.0483 [595] | 0.0320 [394] | 0.0034 [42] | 0.0028 [35] | 0.0153 [189] | 0.0115 [142] | 0.1558 [1919] | 12,319 |
| rows with husband wage difference | 0.0488 [420] | 0.0296 [255] | 0.0029 [25] | 0.0023 [20] | 0.0153 [132] | 0.0105 [90] | 0.1439 [1238] | 8,606 |
| rows with both wage differences | 0.0475 [318] | 0.0339 [227] | 0.0037 [25] | 0.0030 [20] | 0.0134 [90] | 0.0124 [83] | 0.1595 [1068] | 6,694 |

Wife displaced in the same interval: P(wd|hd) = 0.0706 (N=595, events=42); P(wd|no hd) = 0.0300 (N=11724, events=352); P(wd|hd,wemp t-2) = 0.0742 (N=337, events=25); P(wd|no hd,wemp t-2) = 0.0308 (N=6857, events=211)

### Table S2.2. Which of BPS's restrictions drop the displaced couple-years

Universe: married couples, husband 30-57 (age - 1), head in IGE's PSID person file (SRC + SEO), PSID 1999-2009 waves (income years 1998-2008). BPS's restrictions applied in their order (psid_sample.do, prepare_bootstrap.do); each row = couple-years still in the sample after the step. hd / wd / jd = husband / wife / joint displacement in the couple-year's interval.

| Step | Rows | Husband displaced | Wife displaced | Joint | Either | Husband closure | Wife closure | Joint: couples | Husband displaced: men |
|---|---|---|---|---|---|---|---|---|---|
| 0. U: married, husband 30-57, SRC+SEO | 14,327 | 692 | 480 | 57 | 1,115 | 217 | 168 | 55 | 590 |
| 1. composition break (fchg>1) year dropped | 13,876 | 658 | 460 | 52 | 1,066 | 207 | 163 | 50 | 561 |
| 2. not married / no wife | 13,876 | 658 | 460 | 52 | 1,066 | 207 | 163 | 50 | 561 |
| 3. state missing | 13,811 | 654 | 456 | 51 | 1,059 | 206 | 161 | 49 | 558 |
| 4. female head / age always missing | 13,811 | 654 | 456 | 51 | 1,059 | 206 | 161 | 49 | 558 |
| 5. net worth >= 20M | 13,802 | 654 | 456 | 51 | 1,059 | 206 | 161 | 49 | 558 |
| 6. age outside 30-57 (BPS age recode) | 13,767 | 653 | 455 | 51 | 1,057 | 206 | 161 | 49 | 558 |
| 7. SEO sample dropped | 10,857 | 488 | 345 | 37 | 796 | 157 | 132 | 36 | 418 |
| 8. education missing | 10,157 | 449 | 317 | 33 | 733 | 150 | 123 | 32 | 386 |
| 9. minimum-wage / price merge | 10,157 | 449 | 317 | 33 | 733 | 150 | 123 | 32 | 386 |
| 10. no-work rule (person-level) = data4estim | 9,148 | 404 | 283 | 28 | 659 | 131 | 112 | 27 | 351 |
| 11. rows with a husband wage difference (duw | 6,372 | 293 | 186 | 17 | 462 | 96 | 73 | 17 | 259 |
| 12. rows with both spouses' wage differences | 4,762 | 208 | 160 | 16 | 352 | 62 | 63 | 16 | 188 |
| 101. no-work rule: own year | 463 | 8 | 15 | 1 | 22 | 4 | 6 |  |  |
| 102. no-work rule: other year | 546 | 37 | 19 | 4 | 52 | 15 | 5 |  |  |

Why rows in data4estimation have no husband wage-growth moment (head in IGE person file):

| Group | rows in data4estimation | husband wage difference available | no t-2 observation of the couple | half-min-wage trim at t or t-2 | jump trim at t or t-2 (not min-wage) |
|---|---|---|---|---|---|
| hd | 414 | 302 | 105 | 7 | 0 |
| wd | 288 | 189 | 93 | 5 | 1 |
| jd | 28 | 17 | 11 | 0 | 0 |
| none | 8,637 | 6,015 | 2,481 | 101 | 40 |

### Table S2.3. BPS residuals around single and joint displacements (biennial event study)

One regression per column: residual (or raw change) of the two-year difference on indicators of a displacement in the interval after it (k=-1), in it (k=0) and in the interval before it (k=+1), separately for husband only, wife only and joint. Reference: couple-years with no displacement in these intervals. S.e. clustered by household. Cell: coefficient (s.e.; p) [couple-years with the event in the regression].

Sample: base

| | Consumption residual | Husband earnings residual | Wife earnings residual | Wife wage residual | Husband wage residual | Wife participation change | Wife earnings arc change (zeros in) | Consumption log change (raw) |
|---|---|---|---|---|---|---|---|---|
| k=-1 husband only | -0.030 (0.019; p=0.130) [331] | 0.010 (0.032; p=0.753) [322] | -0.060 (0.045; p=0.182) [220] | -0.026 (0.031; p=0.408) [220] | -0.032 (0.029; p=0.273) [322] | -0.026 (0.022; p=0.234) [331] | -0.104** (0.050; p=0.039) [331] | -0.046** (0.021; p=0.025) [331] |
| k=-1 wife only | 0.027 (0.023; p=0.235) [180] | -0.015 (0.036; p=0.672) [180] | 0.058 (0.059; p=0.322) [152] | -0.026 (0.042; p=0.538) [152] | -0.026 (0.038; p=0.487) [180] | 0.013 (0.026; p=0.619) [184] | 0.026 (0.062; p=0.679) [184] | -0.003 (0.025; p=0.891) [183] |
| k=-1 joint | 0.059 (0.043; p=0.177) [24] | 0.094 (0.135; p=0.483) [24] | 0.093 (0.115; p=0.419) [21] | -0.082 (0.092; p=0.376) [21] | 0.083 (0.097; p=0.394) [24] | 0.056 (0.075; p=0.454) [24] | 0.287* (0.148; p=0.053) [24] | 0.013 (0.042; p=0.753) [24] |
| k=0 husband only | -0.022 (0.020; p=0.277) [289] | -0.123*** (0.040; p=0.002) [285] | 0.057 (0.039; p=0.145) [204] | 0.055* (0.031; p=0.078) [204] | 0.004 (0.035; p=0.902) [285] | 0.042* (0.023; p=0.070) [292] | 0.097* (0.051; p=0.059) [292] | -0.039* (0.022; p=0.077) [291] |
| k=0 wife only | 0.019 (0.025; p=0.450) [177] | -0.004 (0.032; p=0.912) [172] | -0.101 (0.062; p=0.104) [151] | 0.072 (0.053; p=0.180) [151] | -0.015 (0.032; p=0.641) [172] | 0.094*** (0.031; p=0.003) [178] | 0.050 (0.076; p=0.506) [178] | -0.013 (0.027; p=0.623) [178] |
| k=0 joint | 0.049 (0.087; p=0.572) [17] | -0.335* (0.178; p=0.060) [17] | -0.186 (0.138; p=0.179) [16] | -0.043 (0.124; p=0.727) [16] | -0.184 (0.123; p=0.134) [17] | 0.073 (0.057; p=0.200) [17] | -0.341*** (0.130; p=0.009) [17] | -0.016 (0.091; p=0.860) [17] |
| k=+1 husband only | 0.009 (0.020; p=0.638) [246] | 0.045 (0.045; p=0.315) [243] | 0.015 (0.048; p=0.748) [184] | 0.008 (0.034; p=0.803) [184] | -0.077* (0.042; p=0.071) [243] | 0.017 (0.025; p=0.495) [251] | 0.079 (0.056; p=0.155) [251] | 0.028 (0.022; p=0.208) [250] |
| k=+1 wife only | -0.015 (0.024; p=0.542) [167] | 0.024 (0.031; p=0.436) [162] | 0.026 (0.072; p=0.715) [126] | -0.161*** (0.053; p=0.003) [126] | 0.025 (0.033; p=0.451) [162] | -0.160*** (0.038; p=0.000) [167] | -0.340*** (0.088; p=0.000) [167] | -0.022 (0.024; p=0.364) [167] |
| k=+1 joint | -0.062 (0.050; p=0.215) [18] | 0.152 (0.099; p=0.124) [17] | 0.229 (0.152; p=0.132) [12] | -0.068 (0.266; p=0.798) [12] | -0.089 (0.173; p=0.607) [17] | -0.101 (0.109; p=0.352) [18] | -0.219 (0.222; p=0.323) [18] | -0.060 (0.051; p=0.234) [18] |
| k=0 joint minus husband only | 0.071 (0.089; p=0.426) | -0.211 (0.182; p=0.245) | -0.243* (0.142; p=0.088) | -0.098 (0.126; p=0.437) | -0.189 (0.128; p=0.140) | 0.031 (0.061; p=0.606) | -0.438*** (0.138; p=0.002) | 0.023 (0.094; p=0.803) |
| k=+1 joint minus husband only | -0.071 (0.054; p=0.185) | 0.107 (0.110; p=0.334) | 0.214 (0.159; p=0.179) | -0.077 (0.268; p=0.775) | -0.012 (0.180; p=0.946) | -0.118 (0.111; p=0.286) | -0.298 (0.227; p=0.189) | -0.088 (0.055; p=0.108) |
| N | 6,621 | 6,489 | 4,964 | 4,964 | 6,489 | 6,643 | 6,643 | 6,641 |

Sample: b_nostatus

| | Consumption residual | Husband earnings residual | Wife earnings residual | Wife wage residual | Husband wage residual | Wife participation change | Wife earnings arc change (zeros in) | Consumption log change (raw) |
|---|---|---|---|---|---|---|---|---|
| k=-1 husband only | -0.035* (0.020; p=0.078) [331] | -0.011 (0.032; p=0.727) [322] | -0.079* (0.047; p=0.092) [220] | -0.026 (0.031; p=0.408) [220] | -0.032 (0.029; p=0.273) [322] | -0.026 (0.022; p=0.234) [331] | -0.104** (0.050; p=0.039) [331] | -0.046** (0.021; p=0.025) [331] |
| k=-1 wife only | 0.019 (0.023; p=0.409) [180] | -0.000 (0.036; p=0.993) [180] | 0.013 (0.058; p=0.825) [152] | -0.026 (0.042; p=0.538) [152] | -0.026 (0.038; p=0.487) [180] | 0.013 (0.026; p=0.619) [184] | 0.026 (0.062; p=0.679) [184] | -0.003 (0.025; p=0.891) [183] |
| k=-1 joint | 0.036 (0.040; p=0.364) [24] | 0.059 (0.141; p=0.677) [24] | 0.042 (0.113; p=0.708) [21] | -0.082 (0.092; p=0.376) [21] | 0.083 (0.097; p=0.394) [24] | 0.056 (0.075; p=0.454) [24] | 0.287* (0.148; p=0.053) [24] | 0.013 (0.042; p=0.753) [24] |
| k=0 husband only | -0.026 (0.020; p=0.194) [289] | -0.172*** (0.040; p=0.000) [285] | 0.051 (0.038; p=0.174) [204] | 0.055* (0.031; p=0.078) [204] | 0.004 (0.035; p=0.902) [285] | 0.042* (0.023; p=0.070) [292] | 0.097* (0.051; p=0.059) [292] | -0.039* (0.022; p=0.077) [291] |
| k=0 wife only | 0.012 (0.025; p=0.638) [177] | 0.005 (0.034; p=0.892) [172] | -0.202*** (0.064; p=0.002) [151] | 0.072 (0.053; p=0.180) [151] | -0.015 (0.032; p=0.641) [172] | 0.094*** (0.031; p=0.003) [178] | 0.050 (0.076; p=0.506) [178] | -0.013 (0.027; p=0.623) [178] |
| k=0 joint | 0.045 (0.083; p=0.584) [17] | -0.376* (0.193; p=0.052) [17] | -0.299* (0.156; p=0.055) [16] | -0.043 (0.124; p=0.727) [16] | -0.184 (0.123; p=0.134) [17] | 0.073 (0.057; p=0.200) [17] | -0.341*** (0.130; p=0.009) [17] | -0.016 (0.091; p=0.860) [17] |
| k=+1 husband only | 0.009 (0.020; p=0.660) [246] | 0.028 (0.046; p=0.535) [243] | 0.022 (0.048; p=0.655) [184] | 0.008 (0.034; p=0.803) [184] | -0.077* (0.042; p=0.071) [243] | 0.017 (0.025; p=0.495) [251] | 0.079 (0.056; p=0.155) [251] | 0.028 (0.022; p=0.208) [250] |
| k=+1 wife only | -0.012 (0.024; p=0.622) [167] | 0.024 (0.032; p=0.468) [162] | -0.011 (0.074; p=0.886) [126] | -0.161*** (0.053; p=0.003) [126] | 0.025 (0.033; p=0.451) [162] | -0.160*** (0.038; p=0.000) [167] | -0.340*** (0.088; p=0.000) [167] | -0.022 (0.024; p=0.364) [167] |
| k=+1 joint | -0.056 (0.050; p=0.265) [18] | 0.126 (0.098; p=0.196) [17] | 0.227 (0.151; p=0.133) [12] | -0.068 (0.266; p=0.798) [12] | -0.089 (0.173; p=0.607) [17] | -0.101 (0.109; p=0.352) [18] | -0.219 (0.222; p=0.323) [18] | -0.060 (0.051; p=0.234) [18] |
| k=0 joint minus husband only | 0.071 (0.085; p=0.401) | -0.204 (0.197; p=0.300) | -0.351** (0.159; p=0.028) | -0.098 (0.126; p=0.437) | -0.189 (0.128; p=0.140) | 0.031 (0.061; p=0.606) | -0.438*** (0.138; p=0.002) | 0.023 (0.094; p=0.803) |
| k=+1 joint minus husband only | -0.064 (0.054; p=0.232) | 0.098 (0.109; p=0.369) | 0.206 (0.158; p=0.193) | -0.077 (0.268; p=0.775) | -0.012 (0.180; p=0.946) | -0.118 (0.111; p=0.286) | -0.298 (0.227; p=0.189) | -0.088 (0.055; p=0.108) |
| N | 6,621 | 6,489 | 4,964 | 4,964 | 6,489 | 6,643 | 6,643 | 6,641 |

Sample: a_nowork

| | Consumption residual | Husband earnings residual | Wife earnings residual | Wife wage residual | Husband wage residual | Wife participation change | Wife earnings arc change (zeros in) | Consumption log change (raw) |
|---|---|---|---|---|---|---|---|---|
| k=-1 husband only | -0.030 (0.019; p=0.116) [343] | 0.020 (0.033; p=0.549) [334] | -0.042 (0.045; p=0.347) [229] | -0.014 (0.032; p=0.659) [229] | -0.035 (0.029; p=0.229) [334] | -0.026 (0.021; p=0.218) [343] | -0.091* (0.049; p=0.063) [343] | -0.046** (0.020; p=0.023) [343] |
| k=-1 wife only | 0.019 (0.023; p=0.406) [189] | -0.015 (0.037; p=0.692) [189] | 0.050 (0.057; p=0.380) [157] | -0.027 (0.041; p=0.509) [157] | -0.041 (0.037; p=0.269) [189] | 0.017 (0.026; p=0.515) [193] | 0.033 (0.060; p=0.578) [193] | -0.011 (0.025; p=0.671) [192] |
| k=-1 joint | 0.054 (0.043; p=0.210) [24] | 0.094 (0.135; p=0.486) [24] | 0.069 (0.115; p=0.546) [21] | -0.082 (0.092; p=0.374) [21] | 0.082 (0.097; p=0.394) [24] | 0.056 (0.075; p=0.459) [24] | 0.286* (0.149; p=0.055) [24] | 0.013 (0.042; p=0.751) [24] |
| k=0 husband only | -0.017 (0.020; p=0.383) [302] | -0.101** (0.040; p=0.012) [297] | 0.069* (0.039; p=0.075) [214] | 0.059* (0.031; p=0.056) [214] | 0.012 (0.034; p=0.732) [297] | 0.044* (0.023; p=0.058) [305] | 0.104** (0.051; p=0.040) [305] | -0.039* (0.022; p=0.075) [304] |
| k=0 wife only | 0.025 (0.025; p=0.326) [184] | -0.008 (0.033; p=0.799) [178] | -0.142** (0.063; p=0.024) [157] | 0.073 (0.052; p=0.165) [157] | -0.017 (0.032; p=0.599) [178] | 0.097*** (0.031; p=0.001) [185] | 0.034 (0.075; p=0.654) [185] | -0.007 (0.027; p=0.805) [185] |
| k=0 joint | 0.052 (0.088; p=0.553) [17] | -0.317* (0.179; p=0.077) [17] | -0.197 (0.136; p=0.149) [16] | -0.046 (0.124; p=0.711) [16] | -0.186 (0.125; p=0.137) [17] | 0.073 (0.057; p=0.204) [17] | -0.344*** (0.130; p=0.008) [17] | -0.016 (0.091; p=0.863) [17] |
| k=+1 husband only | 0.009 (0.019; p=0.638) [261] | 0.048 (0.044; p=0.272) [257] | 0.016 (0.048; p=0.732) [194] | 0.009 (0.037; p=0.816) [194] | -0.076* (0.042; p=0.068) [257] | 0.019 (0.025; p=0.447) [266] | 0.091 (0.056; p=0.104) [266] | 0.024 (0.021; p=0.265) [265] |
| k=+1 wife only | -0.014 (0.024; p=0.557) [175] | 0.039 (0.032; p=0.227) [169] | 0.022 (0.073; p=0.763) [132] | -0.158*** (0.052; p=0.003) [132] | 0.039 (0.034; p=0.247) [169] | -0.166*** (0.037; p=0.000) [175] | -0.343*** (0.087; p=0.000) [175] | -0.020 (0.024; p=0.414) [175] |
| k=+1 joint | -0.061 (0.051; p=0.229) [18] | 0.009 (0.159; p=0.953) [18] | 0.220 (0.154; p=0.153) [12] | -0.067 (0.265; p=0.801) [12] | -0.178 (0.185; p=0.334) [18] | -0.102 (0.109; p=0.349) [18] | -0.222 (0.221; p=0.316) [18] | -0.060 (0.051; p=0.234) [18] |
| k=0 joint minus husband only | 0.069 (0.090; p=0.441) | -0.216 (0.183; p=0.239) | -0.266* (0.140; p=0.058) | -0.105 (0.126; p=0.407) | -0.197 (0.129; p=0.128) | 0.029 (0.061; p=0.631) | -0.449*** (0.138; p=0.001) | 0.023 (0.093; p=0.806) |
| k=+1 joint minus husband only | -0.070 (0.054; p=0.197) | -0.038 (0.165; p=0.816) | 0.203 (0.160; p=0.205) | -0.075 (0.267; p=0.778) | -0.102 (0.191; p=0.591) | -0.121 (0.111; p=0.276) | -0.313 (0.227; p=0.168) | -0.084 (0.055; p=0.124) |
| N | 6,929 | 6,784 | 5,196 | 5,196 | 6,784 | 6,951 | 6,951 | 6,949 |

Sample: d_seo

| | Consumption residual | Husband earnings residual | Wife earnings residual | Wife wage residual | Husband wage residual | Wife participation change | Wife earnings arc change (zeros in) | Consumption log change (raw) |
|---|---|---|---|---|---|---|---|---|
| k=-1 husband only | -0.025 (0.018; p=0.153) [421] | 0.013 (0.029; p=0.638) [410] | -0.047 (0.039; p=0.225) [286] | -0.014 (0.027; p=0.607) [286] | -0.049* (0.026; p=0.062) [410] | -0.013 (0.020; p=0.510) [421] | -0.072 (0.045; p=0.107) [421] | -0.050*** (0.019; p=0.008) [421] |
| k=-1 wife only | 0.014 (0.020; p=0.494) [230] | -0.022 (0.031; p=0.484) [230] | 0.047 (0.049; p=0.336) [194] | -0.014 (0.039; p=0.729) [194] | -0.058* (0.031; p=0.064) [230] | 0.031 (0.023; p=0.172) [234] | 0.047 (0.053; p=0.375) [234] | -0.020 (0.022; p=0.379) [233] |
| k=-1 joint | 0.006 (0.047; p=0.899) [32] | -0.132 (0.182; p=0.467) [32] | 0.120 (0.092; p=0.192) [27] | -0.047 (0.078; p=0.546) [27] | 0.002 (0.087; p=0.982) [32] | 0.119* (0.071; p=0.094) [32] | 0.421*** (0.137; p=0.002) [32] | -0.029 (0.049; p=0.556) [32] |
| k=0 husband only | -0.019 (0.019; p=0.312) [365] | -0.105*** (0.037; p=0.004) [356] | 0.038 (0.035; p=0.273) [261] | 0.046* (0.027; p=0.087) [261] | 0.031 (0.031; p=0.320) [356] | 0.042** (0.020; p=0.034) [367] | 0.087* (0.044; p=0.051) [367] | -0.036* (0.020; p=0.074) [366] |
| k=0 wife only | 0.002 (0.022; p=0.943) [220] | -0.015 (0.030; p=0.610) [216] | -0.114** (0.055; p=0.038) [186] | 0.054 (0.047; p=0.258) [186] | -0.008 (0.027; p=0.768) [216] | 0.068** (0.029; p=0.020) [222] | -0.024 (0.069; p=0.729) [222] | -0.033 (0.026; p=0.194) [222] |
| k=0 joint | 0.047 (0.072; p=0.514) [23] | -0.356** (0.140; p=0.011) [23] | -0.086 (0.125; p=0.491) [22] | 0.000 (0.097; p=1.000) [22] | -0.180* (0.098; p=0.066) [23] | 0.054 (0.043; p=0.204) [23] | -0.291*** (0.110; p=0.008) [23] | 0.015 (0.073; p=0.838) [23] |
| k=+1 husband only | 0.028 (0.019; p=0.128) [301] | 0.065 (0.040; p=0.105) [296] | -0.007 (0.045; p=0.877) [225] | -0.016 (0.030; p=0.599) [225] | -0.099** (0.038; p=0.010) [296] | -0.001 (0.022; p=0.957) [305] | 0.043 (0.049; p=0.376) [305] | 0.036* (0.020; p=0.069) [304] |
| k=+1 wife only | -0.007 (0.022; p=0.733) [215] | 0.010 (0.028; p=0.715) [211] | 0.054 (0.061; p=0.369) [164] | -0.153*** (0.047; p=0.001) [164] | 0.034 (0.028; p=0.223) [211] | -0.166*** (0.032; p=0.000) [216] | -0.311*** (0.076; p=0.000) [216] | -0.002 (0.024; p=0.930) [216] |
| k=+1 joint | -0.110* (0.059; p=0.065) [21] | 0.081 (0.142; p=0.570) [21] | 0.010 (0.196; p=0.960) [14] | -0.163 (0.236; p=0.489) [14] | -0.119 (0.162; p=0.463) [21] | -0.141 (0.102; p=0.168) [21] | -0.401* (0.216; p=0.063) [21] | -0.088 (0.057; p=0.126) [21] |
| k=0 joint minus husband only | 0.066 (0.074; p=0.373) | -0.250* (0.144; p=0.082) | -0.124 (0.129; p=0.334) | -0.046 (0.099; p=0.641) | -0.211** (0.102; p=0.039) | 0.012 (0.046; p=0.788) | -0.377*** (0.117; p=0.001) | 0.051 (0.075; p=0.500) |
| k=+1 joint minus husband only | -0.138** (0.062; p=0.027) | 0.016 (0.149; p=0.914) | 0.017 (0.202; p=0.934) | -0.147 (0.238; p=0.536) | -0.020 (0.167; p=0.905) | -0.140 (0.104; p=0.178) | -0.444** (0.221; p=0.044) | -0.124** (0.060; p=0.039) |
| N | 8,132 | 7,988 | 6,163 | 6,163 | 7,988 | 8,157 | 8,157 | 8,153 |

Sample: f_all

| | Consumption residual | Husband earnings residual | Wife earnings residual | Wife wage residual | Husband wage residual | Wife participation change | Wife earnings arc change (zeros in) | Consumption log change (raw) |
|---|---|---|---|---|---|---|---|---|
| k=-1 husband only | -0.034* (0.018; p=0.055) [447] | 0.030 (0.036; p=0.412) [447] | -0.035 (0.042; p=0.395) [315] | -0.011 (0.029; p=0.696) [315] | -0.014 (0.033; p=0.666) [447] | -0.017 (0.018; p=0.337) [447] | -0.065 (0.043; p=0.132) [447] | -0.048*** (0.018; p=0.008) [447] |
| k=-1 wife only | -0.011 (0.021; p=0.605) [246] | -0.006 (0.040; p=0.887) [247] | -0.020 (0.054; p=0.707) [209] | -0.002 (0.045; p=0.968) [209] | -0.047 (0.040; p=0.243) [247] | 0.032 (0.020; p=0.115) [247] | 0.056 (0.052; p=0.279) [247] | -0.028 (0.022; p=0.202) [246] |
| k=-1 joint | -0.022 (0.046; p=0.624) [34] | -0.173 (0.178; p=0.330) [34] | 0.224 (0.159; p=0.158) [31] | 0.067 (0.111; p=0.545) [31] | -0.000 (0.082; p=0.996) [34] | 0.114** (0.050; p=0.023) [34] | 0.384*** (0.130; p=0.003) [34] | -0.035 (0.047; p=0.462) [34] |
| k=0 husband only | -0.017 (0.019; p=0.355) [394] | -0.145*** (0.042; p=0.001) [395] | 0.073 (0.044; p=0.101) [293] | 0.078* (0.042; p=0.064) [293] | 0.038 (0.036; p=0.300) [395] | 0.032* (0.018; p=0.071) [395] | 0.102** (0.043; p=0.017) [395] | -0.032* (0.019; p=0.091) [394] |
| k=0 wife only | -0.013 (0.024; p=0.589) [230] | -0.038 (0.047; p=0.426) [230] | -0.236*** (0.067; p=0.000) [202] | 0.034 (0.051; p=0.503) [202] | -0.006 (0.044; p=0.886) [230] | 0.065*** (0.025; p=0.010) [230] | -0.036 (0.068; p=0.596) [230] | -0.024 (0.025; p=0.335) [230] |
| k=0 joint | -0.009 (0.073; p=0.903) [25] | -0.337** (0.142; p=0.018) [25] | -0.242 (0.197; p=0.219) [25] | -0.017 (0.123; p=0.890) [25] | -0.110 (0.113; p=0.330) [25] | 0.007* (0.004; p=0.064) [25] | -0.275* (0.142; p=0.053) [25] | -0.024 (0.074; p=0.749) [25] |
| k=+1 husband only | 0.033* (0.018; p=0.069) [329] | 0.011 (0.046; p=0.814) [330] | -0.001 (0.049; p=0.979) [254] | -0.023 (0.037; p=0.530) [254] | -0.108** (0.045; p=0.016) [330] | 0.027 (0.019; p=0.164) [330] | 0.061 (0.048; p=0.212) [330] | 0.036* (0.019; p=0.064) [329] |
| k=+1 wife only | 0.009 (0.023; p=0.699) [225] | -0.019 (0.068; p=0.779) [225] | 0.050 (0.060; p=0.402) [174] | -0.146*** (0.049; p=0.003) [174] | 0.000 (0.067; p=0.997) [225] | -0.178*** (0.030; p=0.000) [225] | -0.314*** (0.075; p=0.000) [225] | 0.001 (0.024; p=0.971) [225] |
| k=+1 joint | -0.101* (0.056; p=0.070) [22] | 0.071 (0.135; p=0.596) [22] | 0.261 (0.295; p=0.376) [17] | -0.011 (0.211; p=0.957) [17] | -0.112 (0.155; p=0.471) [22] | -0.225*** (0.087; p=0.010) [22] | -0.354* (0.210; p=0.092) [22] | -0.086 (0.055; p=0.114) [22] |
| k=0 joint minus husband only | 0.008 (0.075; p=0.911) | -0.193 (0.148; p=0.192) | -0.315 (0.201; p=0.118) | -0.095 (0.128; p=0.460) | -0.148 (0.118; p=0.210) | -0.025 (0.017; p=0.144) | -0.377** (0.147; p=0.010) | 0.008 (0.076; p=0.911) |
| k=+1 joint minus husband only | -0.134** (0.059; p=0.022) | 0.061 (0.143; p=0.671) | 0.262 (0.299; p=0.381) | 0.012 (0.214; p=0.955) | -0.003 (0.162; p=0.983) | -0.252*** (0.089; p=0.005) | -0.415* (0.215; p=0.054) | -0.122** (0.057; p=0.034) |
| N | 8,602 | 8,606 | 6,694 | 6,694 | 8,606 | 8,606 | 8,606 | 8,602 |

### Table S2.4. Wage-shock covariances and preference estimates with and without displacement couple-years

| Parameter | BPS baseline | baseline, no displacement years | baseline, no joint-displacement years | (b) no status controls | (b), no displacement years | (f) all relaxations | (f), no displacement years |
|---|---|---|---|---|---|---|---|
| Var. transitory, husband (sigma2_u1) | 0.0275*** (0.0063; p=0.000) | 0.0290*** (0.0071; p=0.000) | 0.0273*** (0.0063; p=0.000) | 0.0275*** (0.0063; p=0.000) | 0.0290*** (0.0071; p=0.000) | 0.0996*** (0.0224; p=0.000) | 0.0775*** (0.0153; p=0.000) |
| Var. permanent, husband (sigma2_v1) | 0.0303*** (0.0049; p=0.000) | 0.0257*** (0.0054; p=0.000) | 0.0301*** (0.0049; p=0.000) | 0.0303*** (0.0049; p=0.000) | 0.0257*** (0.0054; p=0.000) | 0.0266*** (0.0101; p=0.008) | 0.0350*** (0.0109; p=0.001) |
| Var. transitory, wife (sigma2_u2) | 0.0125** (0.0057; p=0.028) | 0.0062 (0.0059; p=0.294) | 0.0123** (0.0057; p=0.031) | 0.0125** (0.0057; p=0.028) | 0.0062 (0.0059; p=0.294) | 0.0600*** (0.0114; p=0.000) | 0.0513*** (0.0120; p=0.000) |
| Var. permanent, wife (sigma2_v2) | 0.0382*** (0.0044; p=0.000) | 0.0391*** (0.0048; p=0.000) | 0.0377*** (0.0043; p=0.000) | 0.0382*** (0.0044; p=0.000) | 0.0391*** (0.0048; p=0.000) | 0.0387*** (0.0078; p=0.000) | 0.0390*** (0.0076; p=0.000) |
| Cov. transitory shocks (sigma_u1u2) | 0.0058** (0.0027; p=0.033) | 0.0063** (0.0030; p=0.033) | 0.0054** (0.0027; p=0.048) | 0.0058** (0.0027; p=0.033) | 0.0063** (0.0030; p=0.033) | 0.0100*** (0.0037; p=0.007) | 0.0084** (0.0039; p=0.032) |
|   correlation, transitory | 0.31 | 0.47 | 0.29 | 0.31 | 0.47 | 0.13 | 0.13 |
| Cov. permanent shocks (sigma_v1v2) | 0.0027 (0.0023; p=0.246) | 0.0024 (0.0025; p=0.339) | 0.0023 (0.0022; p=0.306) | 0.0027 (0.0023; p=0.246) | 0.0024 (0.0025; p=0.339) | 0.0003 (0.0030; p=0.915) | 0.0010 (0.0032; p=0.753) |
|   correlation, permanent | 0.08 | 0.08 | 0.07 | 0.08 | 0.08 | 0.01 | 0.03 |
| E(pi) | 0.150*** (0.004; p=0.000) | 0.149*** (0.004; p=0.000) | 0.150 | 0.150*** (0.004; p=0.000) | 0.149 | 0.146*** (0.004; p=0.000) | 0.145 |
| E(s) | 0.708*** (0.013; p=0.000) | 0.714*** (0.015; p=0.000) | 0.709 | 0.708*** (0.013; p=0.000) | 0.714 | 0.687*** (0.011; p=0.000) | 0.696 |
| eta_c,p | 0.418** (0.174; p=0.016) | 0.538** (0.216; p=0.013) | 0.448*** (0.072†; p=0.000) | 0.430*** (0.163; p=0.008) | 0.540*** (0.098†; p=0.000) | 0.010 (0.073; p=0.886) | 0.062* (0.036†; p=0.086) |
| eta_h1,w1 | 0.681*** (0.133; p=0.000) | 0.543*** (0.204; p=0.008) | 0.672*** (0.072†; p=0.000) | 0.700*** (0.139; p=0.000) | 0.554*** (0.078†; p=0.000) | 0.213* (0.111; p=0.055) | 0.412*** (0.071†; p=0.000) |
| eta_h2,w2 | 0.958*** (0.225; p=0.000) | 1.270*** (0.411; p=0.002) | 0.967*** (0.096†; p=0.000) | 1.009*** (0.233; p=0.000) | 1.346*** (0.156†; p=0.000) | 0.487*** (0.075; p=0.000) | 0.634*** (0.074†; p=0.000) |
| eta_c,w1 | -0.162* (0.086; p=0.059) | -0.163** (0.072; p=0.024) | -0.171*** (0.035†; p=0.000) | -0.168** (0.080; p=0.037) | -0.163*** (0.034†; p=0.000) | 0.025 (0.027; p=0.354) | 0.023 (0.019†; p=0.228) |
| eta_h1,p | 0.126** (0.060; p=0.037) | 0.126** (0.057; p=0.028) | 0.133*** (0.027†; p=0.000) | 0.130** (0.057; p=0.022) | 0.125*** (0.026†; p=0.000) | -0.020 (0.022; p=0.356) | -0.019 (0.016†; p=0.228) |
| eta_c,w2 | -0.050 (0.078; p=0.518) | -0.150 (0.128; p=0.240) | -0.053* (0.031†; p=0.085) | -0.053 (0.080; p=0.506) | -0.156*** (0.054†; p=0.004) | 0.003 (0.056; p=0.963) | 0.001 (0.021†; p=0.961) |
| eta_h2,p | 0.079 (0.122; p=0.516) | 0.236 (0.197; p=0.230) | 0.084* (0.049†; p=0.085) | 0.084 (0.128; p=0.508) | 0.245*** (0.085†; p=0.004) | -0.004 (0.087; p=0.963) | -0.002 (0.033†; p=0.961) |
| eta_h1,w2 | 0.159** (0.079; p=0.045) | 0.150 (0.128; p=0.242) | 0.163*** (0.021†; p=0.000) | 0.165** (0.083; p=0.046) | 0.157*** (0.023†; p=0.000) | 0.034 (0.055; p=0.530) | 0.090*** (0.013†; p=0.000) |
| eta_h2,w1 | 0.325** (0.158; p=0.040) | 0.306 (0.259; p=0.237) | 0.333*** (0.043†; p=0.000) | 0.337** (0.162; p=0.038) | 0.321*** (0.046†; p=0.000) | 0.066 (0.103; p=0.521) | 0.173*** (0.024†; p=0.000) |
| Marshallian: wife's hours / husband's wage (kappa_h2,v1) | -0.752*** (0.098; p=0.000) | -0.854*** (0.212; p=0.000) | -0.734 | -0.773*** (0.093; p=0.000) | -0.886 | -1.423* (0.782; p=0.069) | -1.105 |
| Marshallian: husband own (kappa_h1,v1 - 1) | -0.079 (0.108; p=0.464) | 0.020 (0.094; p=0.831) | -0.071 | -0.068 (0.102; p=0.500) | 0.027 | -0.403 (0.372; p=0.280) | -0.354 |
| Marshallian: wife own (kappa_h2,v2 - 1) | 0.425*** (0.106; p=0.000) | 0.494*** (0.107; p=0.000) | 0.436 | 0.452*** (0.115; p=0.000) | 0.517 | -0.371 (0.465; p=0.425) | -0.069 |
| Marshallian: consumption / husband's wage (kappa_c,v1) | 0.316*** (0.057; p=0.000) | 0.358*** (0.076; p=0.000) | 0.326 | 0.318*** (0.069; p=0.000) | 0.355 | -0.021 (0.371; p=0.954) | 0.081 |
| Chain (10% perm. fall): fixed labor supply, no taxes, no savings | 7.09*** (0.13; p=0.000) | 7.15*** (0.15; p=0.000) | 7.10 | 7.09*** (0.13; p=0.000) | 7.15 | 6.88*** (0.11; p=0.000) | 6.96 |
|   + taxes and transfers | 6.33*** (0.12; p=0.000) | 6.38*** (0.14; p=0.000) | 6.34 | 6.33*** (0.12; p=0.000) | 6.38 | 6.09*** (0.10; p=0.000) | 6.17 |
|   + husband's labor supply | 5.79*** (0.70; p=0.000) | 6.48*** (0.60; p=0.000) | 5.85 | 5.86*** (0.67; p=0.000) | 6.52 | 3.57 (2.32; p=0.124) | 3.93 |
|   + wife's labor supply | 3.88*** (0.69; p=0.000) | 4.37*** (0.86; p=0.000) | 4.00 | 3.90*** (0.83; p=0.000) | 4.34 | -0.22 (4.48; p=0.960) | 1.03 |
|   + savings (= 10 x kappa_c,v1) | 3.16*** (0.57; p=0.000) | 3.58*** (0.76; p=0.000) | 3.26 | 3.18*** (0.69; p=0.000) | 3.55 | -0.21 (3.71; p=0.954) | 0.81 |
| Share of insurance: government | 0.194*** (0.031; p=0.000) | 0.215*** (0.043; p=0.000) | 0.198 | 0.194*** (0.035; p=0.000) | 0.213 | 0.110 (0.221; p=0.617) | 0.128 |
| Share of insurance: family labor supply | 0.623*** (0.093; p=0.000) | 0.564*** (0.109; p=0.000) | 0.609 | 0.621*** (0.099; p=0.000) | 0.568 | 0.891 (0.604; p=0.140) | 0.836 |
| Share of insurance: savings | 0.183*** (0.060; p=0.002) | 0.221*** (0.068; p=0.001) | 0.192 | 0.185*** (0.064; p=0.004) | 0.219 | -0.002 (0.383; p=0.997) | 0.036 |
| Outside insurance beta (Table 4 col. 5 spec.) | -0.138 (0.213; p=0.519) | -0.107 (0.141†; p=0.449) | -0.112 (0.144†; p=0.437) | -0.105 (0.188; p=0.578) | -0.087 (0.140†; p=0.534) | n.c. | 0.432 (0.808†; p=0.593) |
| N (preference GMM, household-years) | 7,295 | 6,458 | 7,261 | 7,295 | 6,458 | 9,483 | 8,339 |
| N (household-years in data4estimation) | 10,479 | 9,805 | 10,451 | 10,479 | 9,805 | 13,570 | 12,623 |
| Bootstrap replications (preference / beta) | 50 / 50 | 50 / 0 | 0 / 0 | 50 / 50 | 0 / 0 | 47 / 0 | 0 / 0 |

### Table S2.5. Cross-spouse residual moments with and without displacement couple-years

Mean of the product of BPS residuals (s.e. clustered by household): m_ww = E(du_w1 du_w2) (contemporaneous wage growth = 2 sigma_u1u2 + 2 sigma_v1v2 in BPS's model), m_wwlag = average of E(du_w1 du_w2,t-2) and E(du_w1,t-2 du_w2) (= -sigma_u1u2), m_yy = E(du_y1 du_y2) (earnings), m_cy = E(du_c du_y1); shift_x = change in the mean product in couple-years with displacement x (regression on hd, wd, jd).

| Sample | Moment | All | Without displacement years | Without joint years | shift: husband displaced | shift: wife displaced | shift: joint (extra) |
|---|---|---|---|---|---|---|---|
| base | m_ww | 0.0177*** (0.0039; p=0.000) [N=4,859] | 0.0183*** (0.0040; p=0.000) [N=4,496] | 0.0177*** (0.0039; p=0.000) [N=4,843] | 0.0024 (0.0161; p=0.882) | -0.0245 (0.0231; p=0.290) | 0.0386 (0.0816; p=0.637) |
| base | m_wwlag | -0.0066** (0.0029; p=0.024) [N=3,087] | -0.0065** (0.0031; p=0.034) [N=2,845] | -0.0063** (0.0029; p=0.032) [N=3,074] | -0.0067 (0.0122; p=0.585) | 0.0148 (0.0180; p=0.412) | -0.0799* (0.0480; p=0.096) |
| base | m_yy | 0.0029 (0.0047; p=0.538) [N=4,859] | 0.0013 (0.0049; p=0.794) [N=4,496] | 0.0022 (0.0047; p=0.639) [N=4,843] | 0.0384* (0.0200; p=0.055) | -0.0222 (0.0245; p=0.364) | 0.1929** (0.0824; p=0.019) |
| base | m_cy | 0.0061*** (0.0023; p=0.009) [N=6,467] | 0.0050** (0.0024; p=0.038) [N=5,997] | 0.0060*** (0.0023; p=0.010) [N=6,450] | 0.0189 (0.0131; p=0.148) | 0.0091 (0.0108; p=0.398) | -0.0137 (0.0417; p=0.743) |
| b_nostatus | m_ww | 0.0177*** (0.0039; p=0.000) [N=4,859] | 0.0183*** (0.0040; p=0.000) [N=4,496] | 0.0177*** (0.0039; p=0.000) [N=4,843] | 0.0024 (0.0161; p=0.882) | -0.0245 (0.0231; p=0.290) | 0.0386 (0.0816; p=0.637) |
| b_nostatus | m_wwlag | -0.0066** (0.0029; p=0.024) [N=3,087] | -0.0065** (0.0031; p=0.034) [N=2,845] | -0.0063** (0.0029; p=0.032) [N=3,074] | -0.0067 (0.0122; p=0.585) | 0.0148 (0.0180; p=0.412) | -0.0799* (0.0480; p=0.096) |
| b_nostatus | m_yy | 0.0032 (0.0047; p=0.499) [N=4,859] | 0.0021 (0.0049; p=0.663) [N=4,496] | 0.0023 (0.0047; p=0.623) [N=4,843] | 0.0271 (0.0168; p=0.108) | -0.0316 (0.0266; p=0.234) | 0.2692*** (0.0951; p=0.005) |
| b_nostatus | m_cy | 0.0059** (0.0024; p=0.013) [N=6,467] | 0.0046* (0.0024; p=0.056) [N=5,997] | 0.0058** (0.0024; p=0.014) [N=6,450] | 0.0217 (0.0137; p=0.113) | 0.0097 (0.0117; p=0.410) | -0.0028 (0.0422; p=0.947) |
| a_nowork | m_ww | 0.0178*** (0.0039; p=0.000) [N=5,081] | 0.0180*** (0.0041; p=0.000) [N=4,704] | 0.0177*** (0.0039; p=0.000) [N=5,065] | 0.0096 (0.0163; p=0.557) | -0.0209 (0.0231; p=0.367) | 0.0271 (0.0836; p=0.746) |
| a_nowork | m_wwlag | -0.0066** (0.0030; p=0.031) [N=3,190] | -0.0064** (0.0032; p=0.047) [N=2,943] | -0.0063** (0.0031; p=0.039) [N=3,177] | -0.0083 (0.0122; p=0.497) | 0.0125 (0.0178; p=0.481) | -0.0751 (0.0481; p=0.119) |
| a_nowork | m_yy | 0.0040 (0.0048; p=0.404) [N=5,081] | 0.0023 (0.0050; p=0.646) [N=4,704] | 0.0034 (0.0048; p=0.484) [N=5,065] | 0.0363* (0.0201; p=0.070) | -0.0147 (0.0252; p=0.561) | 0.1850** (0.0815; p=0.023) |
| a_nowork | m_cy | 0.0069*** (0.0024; p=0.003) [N=6,762] | 0.0062** (0.0024; p=0.010) [N=6,274] | 0.0069*** (0.0024; p=0.004) [N=6,745] | 0.0098 (0.0133; p=0.459) | 0.0077 (0.0113; p=0.495) | 0.0023 (0.0438; p=0.959) |
| d_seo | m_ww | 0.0189*** (0.0034; p=0.000) [N=6,042] | 0.0198*** (0.0036; p=0.000) [N=5,584] | 0.0190*** (0.0034; p=0.000) [N=6,020] | 0.0018 (0.0133; p=0.893) | -0.0297 (0.0191; p=0.121) | 0.0050 (0.0663; p=0.940) |
| d_seo | m_wwlag | -0.0063** (0.0027; p=0.019) [N=3,842] | -0.0061** (0.0028; p=0.029) [N=3,539] | -0.0059** (0.0027; p=0.028) [N=3,825] | -0.0055 (0.0110; p=0.619) | 0.0153 (0.0154; p=0.320) | -0.0978** (0.0478; p=0.041) |
| d_seo | m_yy | 0.0025 (0.0044; p=0.570) [N=6,042] | 0.0018 (0.0045; p=0.692) [N=5,584] | 0.0019 (0.0044; p=0.669) [N=6,020] | 0.0144 (0.0207; p=0.486) | -0.0172 (0.0298; p=0.563) | 0.1715** (0.0813; p=0.035) |
| d_seo | m_cy | 0.0068*** (0.0022; p=0.002) [N=7,963] | 0.0057** (0.0022; p=0.010) [N=7,372] | 0.0068*** (0.0022; p=0.002) [N=7,940] | 0.0188 (0.0137; p=0.168) | 0.0076 (0.0113; p=0.505) | -0.0115 (0.0371; p=0.757) |
| f_all | m_ww | 0.0243*** (0.0051; p=0.000) [N=6,694] | 0.0229*** (0.0053; p=0.000) [N=6,174] | 0.0240*** (0.0051; p=0.000) [N=6,669] | 0.0384* (0.0227; p=0.091) | -0.0189 (0.0217; p=0.383) | 0.0655 (0.1213; p=0.589) |
| f_all | m_wwlag | -0.0117*** (0.0037; p=0.002) [N=4,284] | -0.0099** (0.0039; p=0.012) [N=3,939] | -0.0107*** (0.0037; p=0.004) [N=4,264] | -0.0275* (0.0160; p=0.086) | 0.0126 (0.0186; p=0.499) | -0.1944 (0.1232; p=0.115) |
| f_all | m_yy | 0.0055 (0.0070; p=0.430) [N=6,694] | 0.0035 (0.0072; p=0.628) [N=6,174] | 0.0043 (0.0070; p=0.543) [N=6,669] | 0.0062 (0.0287; p=0.828) | 0.0162 (0.0424; p=0.703) | 0.3205** (0.1272; p=0.012) |
| f_all | m_cy | 0.0082*** (0.0030; p=0.005) [N=8,602] | 0.0078** (0.0031; p=0.011) [N=7,953] | 0.0082*** (0.0030; p=0.006) [N=8,577] | 0.0088 (0.0143; p=0.540) | -0.0006 (0.0134; p=0.963) | 0.0157 (0.0369; p=0.671) |

### Table S2.6. BPS Table 7 (added worker, extensive margin) split into entries and exits

IV regressions as in tables_7_8_9.do: dependent variable = change in the wife's participation (net), entry (0 -> 1) or minus exit (1 -> 0), so that net = entries + (minus exits); husband's wage growth instrumented with long-run wage growth (theta_1, permanent) or future wage growth (theta_0, transitory). Published (BPS sample): theta_1 = -0.168* (0.087), N = 3,143; theta_0 = 0.002 (0.030), N = 4,941. S.e. clustered by household; p from the normal. [N; couple-years with a nonzero outcome]

Sample: base

| | Net change in participation | Entries | Minus exits |
|---|---|---|---|
| theta_1: permanent shock to husband's wage | -0.168* (0.087; p=0.053) [N=3,143; nonzero=410] | -0.159** (0.064; p=0.013) [N=3,143; nonzero=196] | -0.009 (0.058; p=0.880) [N=3,143; nonzero=214] |
| theta_0: transitory shock to husband's wage | 0.002 (0.030; p=0.943) [N=4,941; nonzero=671] | 0.007 (0.018; p=0.688) [N=4,941; nonzero=317] | -0.005 (0.021; p=0.811) [N=4,941; nonzero=354] |

Sample: b_nostatus

| | Net change in participation | Entries | Minus exits |
|---|---|---|---|
| theta_1: permanent shock to husband's wage | -0.168* (0.087; p=0.053) [N=3,143; nonzero=410] | -0.159** (0.064; p=0.013) [N=3,143; nonzero=196] | -0.009 (0.058; p=0.880) [N=3,143; nonzero=214] |
| theta_0: transitory shock to husband's wage | 0.002 (0.030; p=0.943) [N=4,941; nonzero=671] | 0.007 (0.018; p=0.688) [N=4,941; nonzero=317] | -0.005 (0.021; p=0.811) [N=4,941; nonzero=354] |

Sample: a_nowork

| | Net change in participation | Entries | Minus exits |
|---|---|---|---|
| theta_1: permanent shock to husband's wage | -0.192** (0.096; p=0.046) [N=3,227; nonzero=425] | -0.168** (0.071; p=0.018) [N=3,227; nonzero=203] | -0.024 (0.061; p=0.695) [N=3,227; nonzero=222] |
| theta_0: transitory shock to husband's wage | 0.013 (0.030; p=0.651) [N=5,127; nonzero=700] | 0.013 (0.018; p=0.479) [N=5,127; nonzero=331] | 0.001 (0.020; p=0.971) [N=5,127; nonzero=369] |

Sample: d_seo

| | Net change in participation | Entries | Minus exits |
|---|---|---|---|
| theta_1: permanent shock to husband's wage | -0.183** (0.083; p=0.027) [N=3,801; nonzero=489] | -0.183*** (0.063; p=0.003) [N=3,801; nonzero=234] | 0.000 (0.054; p=0.996) [N=3,801; nonzero=255] |
| theta_0: transitory shock to husband's wage | 0.010 (0.029; p=0.719) [N=5,951; nonzero=789] | 0.011 (0.017; p=0.513) [N=5,951; nonzero=371] | -0.001 (0.019; p=0.970) [N=5,951; nonzero=418] |

Sample: f_all

| | Net change in participation | Entries | Minus exits |
|---|---|---|---|
| theta_1: permanent shock to husband's wage | -0.262* (0.148; p=0.077) [N=4,078; nonzero=464] | -0.166 (0.113; p=0.142) [N=4,078; nonzero=225] | -0.096 (0.071; p=0.178) [N=4,078; nonzero=239] |
| theta_0: transitory shock to husband's wage | -0.002 (0.011; p=0.828) [N=6,408; nonzero=755] | 0.004 (0.008; p=0.581) [N=6,408; nonzero=359] | -0.007 (0.007; p=0.303) [N=6,408; nonzero=396] |

theta_1 with the couple-year's displacement indicators as controls (head in IGE person file), sample base:

| | Net | Entries | Minus exits |
|---|---|---|---|
| duw | -0.126 (0.090; p=0.162) | -0.122* (0.065; p=0.060) | -0.005 (0.064; p=0.943) |
| hd | 0.052 (0.038; p=0.169) | 0.033 (0.027; p=0.209) | 0.018 (0.023; p=0.431) |
| wd | 0.044 (0.053; p=0.405) | 0.038 (0.040; p=0.341) | 0.006 (0.031; p=0.845) |
| jd | -0.066 (0.068; p=0.332) | -0.115** (0.051; p=0.023) | 0.049 (0.043; p=0.250) |
| N | 2,791 | 2,791 | 2,791 |

theta_1 with the couple-year's displacement indicators as controls (head in IGE person file), sample b_nostatus:

| | Net | Entries | Minus exits |
|---|---|---|---|
| duw | -0.126 (0.090; p=0.162) | -0.122* (0.065; p=0.060) | -0.005 (0.064; p=0.943) |
| hd | 0.052 (0.038; p=0.169) | 0.033 (0.027; p=0.209) | 0.018 (0.023; p=0.431) |
| wd | 0.044 (0.053; p=0.405) | 0.038 (0.040; p=0.341) | 0.006 (0.031; p=0.845) |
| jd | -0.066 (0.068; p=0.332) | -0.115** (0.051; p=0.023) | 0.049 (0.043; p=0.250) |
| N | 2,791 | 2,791 | 2,791 |

theta_1 with the couple-year's displacement indicators as controls (head in IGE person file), sample a_nowork:

| | Net | Entries | Minus exits |
|---|---|---|---|
| duw | -0.155 (0.101; p=0.123) | -0.136* (0.073; p=0.063) | -0.020 (0.067; p=0.769) |
| hd | 0.053 (0.037; p=0.160) | 0.033 (0.027; p=0.210) | 0.019 (0.023; p=0.404) |
| wd | 0.053 (0.054; p=0.326) | 0.044 (0.041; p=0.277) | 0.008 (0.030; p=0.786) |
| jd | -0.075 (0.069; p=0.280) | -0.122** (0.053; p=0.021) | 0.047 (0.042; p=0.273) |
| N | 2,857 | 2,857 | 2,857 |

theta_1 with the couple-year's displacement indicators as controls (head in IGE person file), sample d_seo:

| | Net | Entries | Minus exits |
|---|---|---|---|
| duw | -0.154* (0.087; p=0.075) | -0.156** (0.065; p=0.016) | 0.002 (0.058; p=0.973) |
| hd | 0.051 (0.034; p=0.136) | 0.044* (0.025; p=0.075) | 0.007 (0.022; p=0.743) |
| wd | 0.030 (0.047; p=0.520) | 0.045 (0.034; p=0.185) | -0.015 (0.029; p=0.598) |
| jd | -0.063 (0.061; p=0.299) | -0.145*** (0.047; p=0.002) | 0.082** (0.038; p=0.029) |
| N | 3,449 | 3,449 | 3,449 |

theta_1 with the couple-year's displacement indicators as controls (head in IGE person file), sample f_all:

| | Net | Entries | Minus exits |
|---|---|---|---|
| duw | -0.220 (0.142; p=0.120) | -0.111 (0.099; p=0.262) | -0.109 (0.078; p=0.159) |
| hd | 0.037 (0.031; p=0.228) | 0.029 (0.022; p=0.186) | 0.008 (0.020; p=0.676) |
| wd | 0.032 (0.046; p=0.486) | 0.053 (0.033; p=0.103) | -0.021 (0.027; p=0.432) |
| jd | -0.064 (0.060; p=0.288) | -0.134*** (0.042; p=0.001) | 0.070* (0.036; p=0.051) |
| N | 3,690 | 3,690 | 3,690 |

## Extension to 1999-2021: not done

The PSID family files to 2021 are on disk, but BPS's pipeline needs, for each new wave, the ER-variable mapping of `psid_interview.do` (about 100 variables per wave), and for each new year the federal tax, EITC and Food Stamp parameters hard-coded in `tax_rate_estimation_snap.do` (1998-2008 only), poverty lines (`poverty_line2.dta` ends in 2008) and state minimum wages (`min_wage.dta` ends in 2010). None of these exist in the package or the repo; see `README.md`. A raw rebuild of 1999-2009 is also blocked by the missing early-release 1999 income file `faminc99`; Step 0 therefore starts from BPS's shipped `psid_cons.dta`, which reproduces their estimation file exactly.

## Caveats

- 50 bootstrap replications (BPS: 200); residual regressions are not re-estimated inside the bootstrap (as in BPS). Failed replications are dropped (kept: c 48, Black 47, f 47, f weighted 46 of 50); in these four runs BPS's own table step in `bootstrap.do` then stops (r(198), logs), after the replications file is saved; s.e. come from that file.
- Weighted runs weight the residual regressions, both GMM steps (through scaled instruments, because Stata's `gmm` refuses weights with `nocommonesample`) and the chain means, not the tax-function and pi / s projections.
- Displacement flags exist only for SRC + SEO heads (IGE's person file): Step 2 shares and event studies use BPS's rows less the 1997 immigrant refresher; Table 7 uses all rows.
- Displacements are dated to calendar years from the reason-for-job-end items (19 / 25); a row with income year t carries those of t-1 and t. Odd calendar years (two years before the interview) are under-reported (recall), as in 19 / 25.
- Joint displacement cells are small (17-28 couple-years in BPS's sample; 25 with all relaxations): every joint estimate is imprecise and an association.
