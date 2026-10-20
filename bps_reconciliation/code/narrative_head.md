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

