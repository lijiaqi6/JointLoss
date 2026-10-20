# BPS (2016) estimator on simulated data: the harness (2026-10-18)

Step 4 of `IGE/proposals/fable_bps2016_nextsteps.md`: run Blundell, Pistaferri and Saporta-Eksten (2016)'s own
estimator, unchanged, on a PSID-shaped panel built from Paper A's simulated couples (protocol in
`IGE/proposals/fable_bps2016_paperA.md`, Section 3.4), and verify the harness now on BPS's own panel.
Nothing in the existing results (`bps_reconciliation.md/.csv`, `tables/`, `logs/`) or in BPS's do-file copies was
changed; the harness only calls them.

| File (`code/`) | Role |
|---|---|
| `sim_panel_writer.py` | monthly couple panel -> PSID-shaped biennial panel in BPS's `psid_cons.dta` layout, with displacement flags, measurement error (two-component mixture) and the Stata writer |
| `bps_on_sim.do` | BPS's chain on any such panel: `psid_sample.do` -> `prepare_bootstrap.do` -> `residual_measures.do` -> `bootstrap.do` runs (`tax_rate_estimation_snap.do`, `pi_s_estimation.do`, `variance_estimation.do`, `frisch_estimation.do`, `chain.do`); switches for each restriction; one-row-per-spec results CSV |
| `verify_harness.py` | the checks below (round trip vs the Step 0/1 runs and vs BPS's published numbers; smoke test vs the DGP) |
| `smoke_sim_dgp.py` | synthetic monthly couple panel with known wage-shock variances (the smoke test) |

## 1. Usage

```python
import sys; sys.path.insert(0, r"G:\My Drive\JointLoss\bps_reconciliation\code")
import sim_panel_writer as spw
panel = spw.to_bps_panel(monthly)                       # monthly: schema of Section 2
panel, me_info = spw.add_measurement_error(panel, gross_rate=0.01, gross_sd=0.7)   # Section 4
spw.write_bps_dta(panel, r"<WORK>\sim_panel.dta")      # checks the layout, writes Stata 118
# or in one call: spw.write_sim_panel(monthly, path, me=dict(gross_rate=0.01, gross_sd=0.7))
```

Caller do-file (one per specification; run in batch `"C:\Program Files\StataNow19\StataMP-64.exe" /e do caller.do`):

```stata
global INPUT   "<WORK>\sim_panel.dta"
global SPEC    "sim_base"                 // output folder <WORK>\sim_base
global WORK    "<WORK>"                   // scratch, not the repo, not Dropbox
global RESULTS "<WORK>\bps_on_sim_results.csv"   // one row per spec, appended
global SW_nowork 1                         // switches: Section 3 (unset = BPS as shipped)
do "G:\My Drive\JointLoss\bps_reconciliation\code\bps_on_sim.do"
```

A point-estimate run (gmm10 + gmm9 + beta) takes 2-4 minutes; several Stata instances can run in parallel (separate
`SPEC`; give each its own `RESULTS` file or run them sequentially, since appending is not locked). Switch globals are
cleared at the end of each call. Outputs in `<WORK>\<SPEC>`: `est_<run>.dta/.csv` (BPS's estimate tables plus the
insurance chain), `bps_on_sim_long.csv` (every number: spec, run, name, value, se), `bps_on_sim_row.csv` (key row).

## 2. Schemas

### 2.1 Input of `sim_panel_writer.to_bps_panel`: simulated monthly couple panel

One row per couple x calendar month, amounts in real dollars of `base_year` (default 2000).

| Column | Required | Meaning |
|---|---|---|
| `couple_id` | yes | couple identifier |
| `year`, `month` | yes | calendar year and month (1-12); cover the income years written (1998-2008 for waves 1999-2009), the months up to the interview, and Y-3 if the previous-interval flags are wanted |
| `age_h`, `age_w` | yes | ages in the month |
| `race_h`, `race_w` | yes | 1 White, 2 Black, 3 other |
| `educ_h`, `educ_w` | yes | 1 <12 years, 2 =12, 3 >12 (mapped to 10 / 12 / 16 years); years of schooling with `educ_in_years=True` |
| `hours_h`, `hours_w` | yes | hours worked in the month |
| `earn_h`, `earn_w` | yes | labor earnings in the month |
| `emp_h`, `emp_w` | yes | status, PSID codes: 1 working, 2 temporarily laid off, 3 looking for work / unemployed, 4 retired, 5 disabled, 6 keeping house, 7 student |
| `cons` | yes | consumption flow in the month, BPS's definition (nondurables + services, rent equivalent) |
| `assets` | yes | net worth at the end of the month |
| `kids` | yes | persons under 18 in the family unit |
| `married` | yes | 1 if married / living together |
| `head_id`, `wife_id` | no | identities [couple_id; couple_id while married]; output rows are head x wave, a new wife gives fchg = 2 |
| `fsize` | no | family size [1 + married + kids] |
| `disp_h`, `disp_w` | no | 1 in the month a displacement (closure or layoff) ends the job |
| `closure_h/_w`, `quit_h/_w`, `jobend_w` | no | closures only, quits, wife's any job end [disp_w or quit_w] |
| `wage_h`, `wage_w` | no | hourly wage (not used: BPS's wage is annual earnings / annual hours) |
| `cons_housing` | no | housing part of `cons` (gives `totcons_nh`) |
| `snap`, `eitc`, `ui_h`, `ui_w`, `other_inc` | no | transfers and other income in the month; carried as `x_*` extras only (BPS's pipeline imputes taxes, EITC and Food Stamps from earnings, family size and children; it has no UI) |
| `seo` | no | 1 = SEO-type couple [0] |
| `state` | no | PSID state code 1-51 (`psid_states.dta`) [31]; sets the minimum wage of the half-minimum-wage trim (states without a state minimum have 0 in BPS's file, i.e. no trim) |
| `mortgage` | no | remaining principal [0]; BPS's participation probit uses mortgage dummies as the exclusion restriction, so give the model's housing debt if it has one |
| `smsa`, `outkid`, `weight` | no | PSID codes / weight [1, 5, 1] |

### 2.2 Timing and aggregation (PSID conventions)

- Wave W is interviewed in `interview_month` of year W (default April; a tuple, e.g. `(3, 4, 5)`, draws per head x
  wave). Income year Y = W - 1. BPS's `year` = Y - 1900 (98, 100, ..., 108).
- Annual `hours`, `hourw`, `ly`, `wly`: sums over calendar year Y. With `require_full_year=True` (default) a head
  not observed in all 12 months of Y has no row.
- At the interview month: `empst`, `wempst`, `marit` (1 married, else 4), `kids`, `fsize`, age (`age`, `agew`; BPS's
  code subtracts one), `tot_assets3`, `mortgage1`, and the wife's identity.
- `totcons`: the interview month's flow x 12 (default), or the mean of the `cons_months` months up to the interview,
  or the calendar-year-Y sum (`cons_timing='calendar'`). The default follows the memo: the PSID reports consumption
  at the interview, so a shock in the last months of Y appears in the same row only if it lasts to the spring.
- Nominal dollars: every amount is multiplied by BPS's own price index `p_totcons` of income year Y (rebased to 2000,
  `price_indices.dta`), the deflator BPS's code divides by, so the model's real values come back exactly. The tax
  schedules, Food Stamp rules and state minimum wages in BPS's code are nominal and apply as in the PSID.
- `fchg` (PSID family-composition change since the previous wave of the same head): 2 if the wife's identity
  changed or she left, 1 if family size or children changed, 0 otherwise (and in the head's first wave).
- Rows without a wife are written (`marit` 4, `agew` 0, wife variables missing); BPS's code drops them itself.
- Flags (definitions of `build_flags.py`): `hd`/`wd` displacement of the husband / wife in calendar years Y-1 or Y
  (the row's two-year difference), `hs`/`ws` closures, `hq`/`wq` quits, `wa` wife's any job end, `jd = hd*wd`,
  `jd_sy` both in the same calendar year; `_n` the next interval (Y+1, Y+2), `_p` the previous one (Y-3, Y-2);
  `h_pid`, `w_pid` positive identities (-1 no wife), `h_match`, `w_match`.

### 2.3 Input of `bps_on_sim.do`: BPS's layout

One row per head x wave, unique by (`year`, `id`) and by (`person`, `year`); `year` in {98, ..., 108}. These are the
variables of BPS's `psid_cons.dta` that their code reads (all others in `psid_cons.dta` are not used downstream):

| Variable | Content (PSID / BPS) |
|---|---|
| `year` | income year - 1900 (wave - 1901) |
| `id` | interview number within the wave |
| `person` | head identifier (BPS re-identifies after breaks) |
| `seo` | 1 = SEO sample |
| `state` | PSID state code |
| `fsize`, `kids` | family size; persons under 18 (tax, EITC, Food Stamps, poverty line, controls) |
| `age`, `agew` | ages at the interview (`agew` 0 = no wife) |
| `sex` | sex of head (1) |
| `marit` | 1 married |
| `race1`-`race4`, `wrace1`-`wrace4` | race mentions (1 White, 2 Black, 3+ other); only the first is needed |
| `educ`, `weduc`, `educ_ind`, `weduc_ind` | years of schooling (0-17) |
| `hours`, `hourw` | annual hours of head and wife (income year), never missing for the head |
| `ly`, `wly` | annual labor earnings, nominal |
| `empst`, `wempst` | status at the interview (1 working, 2 temporarily laid off, 3 looking / unemployed) |
| `fchg` | family composition change (break at > 1) |
| `totcons`, `totcons_nh` | annual nondurable + services consumption, nominal; same without housing |
| `tot_assets3` | net worth at the interview, nominal |
| `mortgage1`, `mortgage2` | remaining mortgage principals (participation probit) |
| `outkid`, `smsa`, `tyoth` | supports someone outside (1 yes), city size, other members' taxable income |
| `weight` | PSID family weight (used only with `WGT`) |
| flags (optional) | `h_pid w_pid hd hs hq wd ws wq wa jd jd_sy` and `_n`, `_p` versions, `h_match w_match`; if absent, `h_pid = w_pid = -1` and `hd = wd = jd = 0` are created (no break change, no exclusion) |

Extra columns are allowed but must not begin with the prefixes BPS's code expands as wildcards (`fd edd wedd chd dfd
dchd yrd ybd w_ybd stated _I log_ d_ p_ tot_assets`) or be called `eitc`, `tax`, `tau`, `y` etc.; the writer's
extras are named `x_*`, and `check_layout()` tests this.

## 3. Switches (`bps_on_sim.do`; unset = BPS as shipped)

| Global | Values | Restriction (file of BPS's code) |
|---|---|---|
| `SW_nowork` | 0 / 1 | no-work rule: 0 drops the husband's whole history if any year has zero hours, zero earnings or transfers >= 2x earnings (person level, BPS); 1 drops only that year (`prepare_bootstrap.do`) |
| `SW_status` | 1 / 0 | employment-status controls (both spouses' levels, two-year changes, level x year) in the consumption and earnings residual regressions; 0 = removed (`residual_measures.do`) |
| `SW_minw` | 1 / 0 | half-state-minimum-wage trim (`prepare_bootstrap.do`) |
| `SW_jump` | 1 / 0 | jump / collapse-recovery trim, bottom 0.25% of dlog x_t x dlog x_{t-2} by year (`prepare_bootstrap.do`) |
| `SW_seo` | 0 / 1 | 0 drops `seo == 1` rows (BPS); 1 keeps the SEO-type couples (`psid_sample.do`) |
| `SW_brk` | 0 / 1 | composition break at fchg > 1 (BPS); 1 = break only if `h_pid` / `w_pid` change (`psid_sample.do`) |
| `SW_race` | "" / 1 / 2 | all / White head / Black head |
| `SW_dexcl` | 0 / 1 / 2 | drop couple-years with `hd` or `wd` / with `jd` |
| `WGT` | "" / "[pw=weight]" | weighted residual regressions, GMM moments and chain means |
| `RUNS` | "gmm10 gmm9 beta" | `gmm10` T4C11 (age-varying variances: Table 3 by age, Table 4 col. 1, Table 5, chain); `gmm9` T4C41 (stationary: Table 3 all ages, Table 4 col. 4); `beta` T4C5 (outside insurance, col. 5); `bs`, `bsbeta` block bootstraps with `BN` replications |

## 4. Measurement error (`add_measurement_error`)

Two components, in logs, on positive annual earnings, hours and consumption (the memo's Section 2.1):
1. Classical error on every observation, by age group (BPS's five `age_cat` groups, on age at the income year; wives
   by the wife's age, working wives): (e_y, e_h) bivariate normal with variances that make the error 4% / 23% / 13%
   of the log variance of earnings / hours / hourly wage (BPS's calibration from Bound et al. 1994, `T4C1.do`;
   `shares=` to change), cov(e_y, e_h) = (E_y + E_h - E_w)/2 so that the wage error e_y - e_h has its share
   (clipped to positive semi-definite if needed; `info` reports it). `basis='measured'` (default) makes the share a
   share of the measured variance, which is what BPS's correction subtracts (s_me = share x var(measured log x));
   the true-variance cells are the married couples with the husband 30-57 (`calib=` to change). Consumption: iid
   error with variance `var_c` = 0.0332 (BPS's estimated -E(dc_t dc_{t-2})).
2. Gross errors: each of `ly wly hours hourw totcons` independently, with probability `gross_rate`, gets an extra
   N(0, `gross_sd`^2) log error.

The memo's calibration targets for the mixture (share of displacement rows among trimmed rows; transitory variance
without vs with the jump trim, 0.056 / 0.028 in the PSID) are reported by `bps_on_sim.do` (`n_trim_minw`,
`n_trim_minw_disp`, `n_trim_jump`, `n_trim_jump_disp` in the key row; the ratio from a run with `SW_jump 0`).

## 5. Results file (`bps_on_sim_row.csv`, appended to `RESULTS`)

| Columns | Content |
|---|---|
| `spec input sw_* wgt` | specification |
| `N_input N_prep N_sample N_wife_emp N_duw N_duww N_duc` | rows of the input; after `psid_sample.do` (before the no-work rule); `data4estimation`; working wives; husbands' / wives' wage-growth and consumption-growth residuals |
| `nowork_obs_share nowork_drop_share` | share of rows with a no-work year; share dropped by the person-level rule |
| `n_trim_minw(_disp) n_trim_jump(_disp)` | rows trimmed by each trim (of which with a displacement of either spouse) |
| `n_hd n_wd n_jd` | displacement couple-years in `data4estimation` |
| `T3_s_u1 T3_s_v1 T3_s_u2 T3_s_v2 T3_c_u1u2 T3_c_v1v2` (+`_se`) | Table 3, all ages (u transitory, v permanent; c = covariance) |
| `rho_u1u2 rho_v1v2` | correlations of the spouses' shocks |
| `T3a<k>_*` (+`_se`) | Table 3 by age group k = 1..5 (30-37, 38-42, 43-47, 48-52, 53-57) |
| `E_pi E_s eta_*` (+`_se`), `s_omega`, `N_gmm` | Table 4 col. 1 (GMM s.e.; BPS's bootstrap via `RUNS bs`) |
| `M_h1v1 M_h2v2 M_h2v1 M_h1v2 M_cv1 M_cv2`, `F_*` | Table 5 col. 1 Marshallian / Frisch; `M_h2v1` = wife's hours to husband's permanent wage, `M_cv1` = consumption response kappa_c,v1 |
| `ch_c0`-`ch_c4`, `ch_tot ch_gov ch_fam ch_sav` | chain of BPS p. 425 (consumption response to a 10% permanent fall in his wage, percent) and the government / family / savings split |
| `ch_f0`-`ch_f4`, `ch_fgov ch_ffam ch_fsav`, `ch_n ch_nfs ch_tau` | same for Food-Stamp-eligible households; N; mean tau |
| `beta` (+`_se`), `beta_eta_c_p` | outside insurance (Table 4 col. 5) |
| `T4c4_eta_c_p T4c4_eta_h2_w2 T4c4_ch_fam` | stationary-variance model (col. 4) for reference |

## 6. Verification (2026-10-18)

Work folder: the session scratch (`.../scratchpad/harness/`; not in the repo). Commands: `python code/verify_harness.py
roundtrip <new> <ref>` and `python code/verify_harness.py smoke <run> <truth.json>`.

### 6.1 Round trip of BPS's own panel (no simulation): exact

Input = BPS's shipped `psid_cons.dta` with the displacement flags of `build_flags.py` merged in, run through
`bps_on_sim.do` (a) as written by Stata and (b) re-written by `sim_panel_writer.write_bps_dta` (Python dtypes), and
compared with the Step 0/1 runs of `run_spec.do` (every number of `est_gmm10`, `est_gmm9`, `est_beta`: 93 values and
41-42 standard errors per run).

| Harness run | Reference (run_spec.do) | Max abs. difference, all values and s.e. (3 runs) |
|---|---|---|
| BPS as shipped, Stata-written input (`rt_stata`; re-run with the final do-file, `rt_final`) | `base` | 0.0 |
| same, input re-written by the Python writer (`rt_py`) | `base` | 0.0 |
| `SW_nowork 1` (`rt_a_nowork`) | `a_nowork` | 0.0 |
| `SW_status 0` (`rt_b_nostatus`) | `b_nostatus` | 0.0 |
| `SW_nowork 1, SW_status 0, SW_jump 0, SW_minw 0, SW_seo 1, SW_brk 1` (`rt_f_all`) | `f_all` | 0.0 |

Against BPS's published numbers (key row of `rt_final`, tolerance one unit of the last published digit): 73 of 74
cells match. Table 3: 36 of 36 cells (e.g. all ages sigma2_u1 0.0275, sigma2_v1 0.0303, sigma2_u2 0.0125, sigma2_v2
0.0382, sigma_u1u2 0.0058 (rho 0.312), sigma_v1v2 0.0027 (rho 0.079)). Table 4 col. 1: all 11 (E(pi) 0.150, E(s)
0.708, eta_c,p 0.4176 published 0.417, eta_h1,w1 0.681, eta_h2,w2 0.958, ...), N = 7,295; col. 5 beta -0.1377
(published -0.137; GMM s.e. 0.150, BPS's 0.270 is their bootstrap). Table 5 col. 1: all 12 (wife's hours to his
permanent wage -0.752, consumption 0.316). Chain: 7.09 / 6.33 / 5.79 / 3.88 / 3.16 (published 7.1 / 6.3 / 5.8 / 3.9 /
3.2); Food-Stamp group 7.15 / 3.57 / 2.32 / 2.08, government 70.6% (published 71%). Split 19.4 / 62.3 / 18.3
(published 20 / 63 / 17): the one cell outside the tolerance is the savings share, 0.183 vs 0.17, the same as in
the Step 0 replication (BPS's published shares do not follow from their own chain: (3.9-3.2)/3.9 = 0.18).
Sample diagnostics in the key row: 11,638 rows before the no-work rule and 10,479 after (BPS Table 1 cols. 3 and 1);
the person-level rule drops 9.96% of rows (BPS p. 400: about 10%); min-wage trim 286 rows (18 with a displacement
of either spouse), jump trim 75 rows (5 with a displacement); 414 / 288 / 28 husband / wife / joint displacement
couple-years (Step 2's attrition table).

### 6.2 Synthetic smoke test: the variances are recovered

`smoke_sim_dgp.py`: 10,000 couples, monthly 1995-2009, known wage process (docstring), written by the writer to
waves 1999-2009 (60,000 head-waves; 44,057 in BPS's sample, 34,952 husbands' wage-growth moments, about 3.3 times
BPS's 10,479 / 7,295). Measurement error: (me) Bound et al. shares only; (mix) plus gross errors on 1% of
observations per variable, s.d. 0.7; (noME) none. BPS's sigma2_v is the annual permanent variance
(`variance_estimation.do` fits E(dw_t^2) = p_t + p_{t-1} + t_t + t_{t-2}), so the truth is the annual innovation
variance. Table 3 all ages (T4C41), estimate (GMM s.e.):

| Parameter | Truth | me, BPS trims | me, jump trim off | me, both trims off | mix, BPS trims | mix, jump trim off | no ME |
|---|---|---|---|---|---|---|---|
| sigma2_u1 (his transitory) | 0.030 | 0.0234 (0.0013) | 0.0280 (0.0014) | 0.0269 (0.0014) | 0.0290 (0.0014) | 0.0360 (0.0017) | -0.0211 |
| sigma2_v1 (his permanent) | 0.015 | 0.0163 (0.0009) | 0.0145 (0.0009) | 0.0147 (0.0009) | 0.0170 (0.0010) | 0.0145 (0.0011) | 0.0157 |
| sigma2_u2 (her transitory) | 0.020 | 0.0172 (0.0015) | 0.0225 (0.0017) | 0.0172 (0.0017) | 0.0231 (0.0017) | 0.0315 (0.0021) | -0.0331 |
| sigma2_v2 (her permanent) | 0.020 | 0.0208 (0.0011) | 0.0183 (0.0011) | 0.0197 (0.0011) | 0.0209 (0.0012) | 0.0172 (0.0013) | 0.0201 |
| sigma_u1u2 | 0.006 | 0.0056 (0.0011) | 0.0060 (0.0012) | 0.0063 (0.0012) | 0.0057 (0.0012) | 0.0066 (0.0013) | 0.0051 |
| sigma_v1v2 | 0.003 | 0.0019 (0.0008) | 0.0019 (0.0008) | 0.0018 (0.0008) | 0.0019 (0.0008) | 0.0016 (0.0009) | 0.0030 |
| rho_u1u2 / rho_v1v2 | 0.245 / 0.173 | 0.278 / 0.103 | 0.239 / 0.114 | 0.291 / 0.105 | 0.221 / 0.103 | 0.198 / 0.102 | - / 0.167 |
| s_omega (consumption ME) | 0.0332 | 0.0317 | 0.0333 | 0.0333 | 0.0339 | 0.0379 | 0.0003 |

Reading:
- The permanent variances, the transitory covariance and the consumption measurement error are recovered in every
  panel with measurement error (within 1.5-2 s.e.; sigma_v1v2 is 1.4-1.5 s.e. low in all columns, which share the
  same draws).
- The transitory variances depend on the trims and the error mixture, as the memo (Section 2.1) predicts. With
  Gaussian errors only, BPS's jump trim removes genuine reversals (the bottom 0.25% of dw_t x dw_{t-2} is then
  transitory shocks and errors, not outliers) and sigma2_u1 is 0.007 too low (z = -5); without the trim it is
  recovered (0.028). With the gross-error mixture the trim removes mostly gross errors and all six parameters are
  within 2 s.e. (0.029 / 0.017 / 0.023 / 0.021 / 0.0057 / 0.0019); turning the trim off then inflates the transitory
  variances (0.036 / 0.031). So the harness reproduces the PSID's fragility mechanism; the PSID ratio of sigma2_u1
  without / with the jump trim is 2.0 (0.056 / 0.028), the smoke mixture gives 1.24, i.e. the model's mixture must be
  calibrated (more or larger gross errors) before the comparison is like for like.
- Without measurement error BPS's correction (13% of the wage log variance) over-corrects: negative transitory
  variances and a meaningless chain (family share 3.2). The error must be in the simulated data.
- Diagnostics for that calibration are in the key row: in the 'me' panel 68 of 282 jump-trimmed rows (24%) and 57 of
  579 min-wage-trimmed rows carry a displacement, against a base rate of about 9% of couple-years; in the PSID 5 of
  75 (6.7%) against 6.4%. The smoke mixture (22%) is not enough to make the trimmed set look like the PSID's.
- Preference step: it runs on the synthetic panel (E(pi) 0.10, E(s) 0.71, chain 7.10 / 6.31 / 5.69 / 3.72 / 3.31,
  split 0.21 / 0.68 / 0.11 in 'me'). The smoke DGP writes hours and consumption as reduced-form responses to the wage
  components (his hours: +0.5 transitory own, -0.05 permanent own; hers: +0.9, +0.4; her hours to his permanent
  component -0.3; consumption +0.35 / +0.15 to the permanent components), which do not satisfy BPS's restrictions
  (all kappas from six Frisch elasticities, pi and s), and consumption is taken at the spring interview after the
  income year (Section 2.2). The estimates are therefore not expected to equal the DGP coefficients: Frisch 0.56-0.65
  (his, DGP 0.5), 0.81-0.97 (hers, 0.9), consumption to his permanent wage 0.29-0.33 (0.35), but the wife's
  Marshallian cross-elasticity is -0.75 to -0.86 against a DGP hours response of -0.3. That is a warning for the
  model test: BPS's restricted mapping can produce their -0.75 from a smaller true response, so the test should
  compare the model's own simulated responses with what BPS's estimator reports on the model's data, not only the
  estimates with BPS's.
- Switches on the synthetic panel (`SW_nowork 1, SW_status 0, SW_seo 1, SW_brk 1`): run, N 44,057 -> 49,255, Table 3
  essentially unchanged (sigma2_u1 0.0229, sigma2_v1 0.0169), as expected when the DGP has no status-dependent shocks.
- A panel without mortgages: BPS's `testparm _Imor*` aborts; `bps_on_sim.do` then puts a seeded random placeholder
  dummy in `mortgage2` (flag `mort_placeholder = 1`). Estimates are identical to the run with mortgages (checked on the
  synthetic panel), because the participation correction is off in all runs used (fix_var 10).

## 7. Paper A model panels (`IGE/paperA_model/bps_check.py`, 2026-10-19)

`bps_check.py` builds the model exactly as `estimate.py evaluate --start <start>` (`post_common.setup`:
`estimate._init_worker` and `start_theta`, i.e. `EXT_DEFAULTS` or the run's `run.json` extensions, the borrowing wedge
`r_wedge`, `--set-fixed` entries, the extras as fixed inputs, size and CRN seed), simulates the entry couples x K,
writes the monthly panel of 1995-2009 (`educ_in_years=True`: the entry file's `h_educ` / `w_educ` are years), adds
the measurement error (Bound et al. shares, consumption 0.0332, gross errors 1% x s.d. 0.7) and runs `bps_on_sim.do`
with BPS's default switches. The panel and Stata files stay in `--work` (default `%TEMP%/paperA_bps`); the repo gets
`results/bps_<stamp>/bps_check.json` (aggregates only).

**Fix (shim in `pi_s_estimation.do`).** The first runs (`results/bps_20261019_093701`, `_093959`) stopped in BPS's
`pi_s_estimation.do` with a Mata conformability error (3200), then `frisch_estimation.do` r(498), and every Table 3
value was missing. Cause: the simulated couples are White or Black only (no race 3) and no wife is born before 1941
(no `wyb_coh` 1). `_bpsfix` (our earlier shim for race subsamples) then creates all-zero placeholders
(`_Iwrace_3`, `_IwraXagew_3`, ..., `_Iwyb_coh_2`) in the wife's block; BPS's code does not drop the wife's dummies
before the joint `xi` call, and `xi` drops only the variables it created itself, so the placeholders survived and
`xi` renamed the wife's stubs to unique names (`_Iwracea2`, `_IwraXagewa2`, `_Iwyb_coha3`). The hard-coded Mata
lists (`_Iwrace_2`, ...) then picked the wrong columns and the products no longer conformed. The data cannot avoid
this without inventing couples, so the shim was fixed: each placeholder is added to `xi`'s own drop list
(`_dta[__xi__Vars__To__Drop__]`, prefix `_I`), as `xi` does for its own dummies. It creates nothing on BPS's full
panel and changes nothing there: round trip after the fix (`rt_fix` vs `base`, `rt_fix_black` vs `d_black`,
`rt_fix_white` vs `d_white`; `verify_harness.py roundtrip`): max abs difference 0.0 in all 93 values and 41-42
s.e. of each run (gmm10, gmm9, beta); 73 of 74 published cells (the savings share, as before).

**Simulated Table 3 at the analytic start** (start values, not estimates; all ages, T4C41; GMM s.e.): see
`IGE/paperA_model/POSTESTIMATION.md` ("bps_check.py") for the table at K = 1 and K = 3 next to BPS's published
values. Note for the reading: the writer sets the husband's age to the wife's + 2 and both spouses' race to the
couple's race, so in BPS's joint projection for pi (log total earnings on both spouses' age polynomials, race and
cohort dummies) the collinear terms are omitted by Stata (log at the analytic start: `age`, `age2`, `agew`, the race
and wife's race main effects); this affects pi and s (Table 4), not the Table 3 variances.

## 8. Limitations

- Income years 1998-2008 only (waves 1999-2009): BPS's federal tax, EITC and Food Stamp parameters and poverty lines
  are coded only for those years. The writer can write any window, but `bps_on_sim.do` refuses other years; the model
  must label its simulated calendar years 1998-2008 (as the memo's protocol says).
- The ME calibration cells (married couples with the husband 30-57, by age group) approximate BPS's estimation sample
  (after trims, SEO drop, two consecutive waves for wives); the correction then matches only approximately.
- The trim and attrition diagnostics are counts; the memo's targets (displacement share among trimmed rows, the
  with/without-jump-trim ratio) need a second run with `SW_jump 0` and a calibration loop over `gross_rate` /
  `gross_sd`, not done here.
- Standard errors in the key row are BPS's second-step GMM s.e. (not corrected for the first step); BPS's block
  bootstrap needs `RUNS "... bs bsbeta"` and `BN`. The Step 2 event study and Table 7 (entries / exits) are not in the
  harness yet (`step2.do` can be pointed at `<WORK>/<SPEC>/data4estimation.dta` and the residual file).
- Not represented in the writer: the PSID's top-coding, imputation flags, the immigrant refresher, and wives' annual
  hours from the months before a marriage (the writer sums only the months the couple exists). `fchg` = 1 / 2 only.
- The smoke DGP is a check of the plumbing and of the wage-variance step, not of the preference step (see 6.2).
