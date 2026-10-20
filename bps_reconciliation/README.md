# BPS (2016) reconciliation: what was run and how (2026-10-18)

Replication and relaxation of Blundell, Pistaferri and Saporta-Eksten (2016, AER 106(2), "BPS") for Paper A
(`paperA_joint_loss/`), following the protocol in `proposals/fable_bps2016_paperA.md` (Steps 0-2).
Results: `bps_reconciliation.md` (tables) and `bps_reconciliation.csv` (every number). Stata logs: `logs/`.

## Inputs (all read only)

- BPS replication package (AEA 116142-V1): `Dropbox/ReplicationPapers/Consumption Inequality and Family Labor
  Supply/116142-V1/AER_2012_1549_data/`. The do-files, ado files, parameter files and auxiliary .dta files were
  **copied** to `code/` and only the copies were edited (list below). Nothing was written in Dropbox.
- BPS's own constructed PSID panel `output/psid_cons.dta` (47,206 head-years, PSID waves 1999-2009, output of their
  `psid_interview.do` + `psid_individual.do` + `psid_consumption.do`; shipped in the package). Step 0 starts from this
  file. Running BPS's `psid_sample.do` and `prepare_bootstrap.do` on it reproduces their shipped
  `data4estimation.dta` exactly (all 106 variables, 10,479 rows; `code/check_shipped.do`, `logs/check_shipped.log`).
- IGE displacement builders (not edited): `data/psid_displacement.pkl` (saved output of
  `IGE/19.FatherDisplacement.py`: husband's closure / layoff / quit by head pid x calendar year), and the wife's
  reason-for-job-end reports via `IGE/25.JointJobLoss.wife_events()` applied to `data/psid_person_year.pkl` and
  `IGE/23.CorrelatedShocks.extras()["R"]` (cached `data/correlated_shocks_fam.pkl`). Imported with importlib.
- PSID 2023 individual file (`Dropbox/PSID/Individual/ind2023er`) only to identify the PSID subsample of BPS's rows
  (`code/check_unmatched.py`).

### Why not a rebuild from the raw PSID files

`psid_interview.do` reads, for the 1999 wave, a separate PSID file `faminc99` (variables `ID99 FAMINC99 HDEARN99
HDBUSY99 WFEARN99 WFBUSY99 TXHW99 TXOFM99 TRHW99 TROFM99 HDBUSK99 WFBUSK99`: the early-release 1999 family income
file). It is **not** in the local PSID holdings (`Dropbox/PSID/Family/fam1999er` has the integrated 1999 family file;
the old income-file names would have to be mapped to ER16xxx variables, i.e. improvised). The family files f01-f09
and the individual file needed for the other waves exist locally as PSID text + setup files. Because BPS ship the
constructed panel and it reproduces their estimation file exactly, Step 0 uses it; the raw rebuild was not attempted.

### 1999-2021 extension: not done

The family files `fam2011er`-`fam2021er` and `ind2023er` are on disk, but the extension needs, beyond them:
(i) the ER-variable mapping of `psid_interview.do` (about 100 variables per wave: consumption items, assets, hours,
earnings, status, `fchg`, demographics) for six new waves; (ii) federal income tax brackets, EITC and Food Stamp
parameters for 2010-2020, hard-coded by year in `tax_rate_estimation_snap.do` (only 1998-2008 are coded);
(iii) poverty lines after 2008 (`poverty_line2.dta` ends in 2008) and state minimum wages after 2010
(`min_wage.dta` ends in 2010). None of these exist in the package or the repo; constructing them is the 1-2 week
job of the memo's Step 3 and was not improvised here.

## Code (all in `code/`)

| File | Role |
|---|---|
| `build_flags.py` | displacement flags per BPS row (year x interview number): husband / wife displaced (closure or layoff), closures, quits, wife's any job end, joint, for the row's two-year interval (calendar t-1, t), the next and the previous interval; head and wife PSID pids |
| `run_spec.do` | one specification end to end: `psid_sample.do` -> `prepare_bootstrap.do` -> `residual_measures.do` (baseline residual spec only) -> `bootstrap.do` runs: `gmm10` (paramfile T4C11: age-varying variances, Table 3 by age, Table 4 col. 1 point, chain), `gmm9` (T4C41: stationary variances = Table 3 "all ages", Table 4 col. 4), `beta` (T4C5 point: outside insurance), `bs` (T4C1 block bootstrap), `bsbeta` (T4C5 block bootstrap) |
| `specs/*.do` | one caller per specification (switch values; see the table in `bps_reconciliation.md`) |
| `run_all.sh` | runs a list of specs, four Stata instances in parallel |
| `chain.do` | BPS p. 425 insurance accounting (eq. 11) and Table 5 Frisch / Marshallian means, computed in every run and every bootstrap replication |
| `ovr_*.do` | parameter-file overrides (number of replications, no per-replication data saving) |
| `step2.do` | Step 2: shares of displaced couple-years, residual event studies, cross-spouse moments with and without displacement years, Table 7 split into entries and exits |
| `attrition.do` | Step 2: replays BPS's sample selection and records the step at which each displaced couple-year leaves |
| `separation.py` | Step 1e: couples whose next interview shows a separation / new wife, by displacement status |
| `check_shipped.do` | Step 0: rebuilt vs shipped `data4estimation.dta` (`cf`, all variables) |
| `check_unmatched.py` | PSID subsample of BPS rows without a head in IGE's person file |
| `run_step2.do` | caller: `attrition.do` on the baseline, `step2.do` on base, (b), (a), (d) SEO, (f) |
| `compile_results.py` | all tables and the csv (bootstrap s.e. from the saved replication files) |
| `narrative_head.md`, `assemble.py` | summary text and assembly of `bps_reconciliation.md` |
| `peek.py` | development helper |
| `bps_on_sim.do`, `sim_panel_writer.py`, `verify_harness.py`, `smoke_sim_dgp.py` | Step 4: BPS's estimator on simulated (or any PSID-shaped) panels; usage, schemas and verification in `HARNESS.md` |
| `ado/` | `egenmore` (BPS use `egen xtile()`), `ivreg2`, `ranktest`, installed from SSC on 2026-10-18 into this folder only (`net set ado`) |

### Edits to the copies of BPS's files (every edit is marked `[bps_reconciliation]` in the code)

| File | Edit | Default = BPS as shipped |
|---|---|---|
| `psid_sample.do` | merge `flags.dta` by (year, id); switch `SW_brk` (1 = break only when the wife's or head's PSID identity changes, so fchg>1 years with the same couple are kept); save `sample_breaks.dta` (for `attrition.do`); switches `SW_seo` (1 = keep SEO), `SW_race` (1 White, 2 Black head) and `SW_imm` (1 = drop the 1997 immigrant refresher, as BPS fn. 15 describes; `imm.dta` from `check_unmatched.py`) | `SW_brk 0`, `SW_seo 0`, all races, `SW_imm` off |
| `prepare_bootstrap.do` | switch `SW_minw` (half-minimum-wage trim, l. 51-52); `SW_nowork` (1 = drop the zero-hours / zero-earnings / transfer-eligible year instead of the husband's whole history, l. 66-69); `SW_jump` (jump / collapse-recovery trim, l. 85-116); `SW_dexcl` (1 = drop couple-years with a displacement of either spouse, 2 = joint only); saves `prep_nowork.dta`, `prep_prejump.dta` | `SW_minw 1`, `SW_nowork 0`, `SW_jump 1`, `SW_dexcl 0` |
| `residual_measures.do` | `SW_status` (0 = drop both spouses' employment-status levels, two-year changes and level x year terms from the consumption, earnings and total-earnings regressions); `SW_specmax` (only the baseline residual spec is needed); PSID weights `WGT` in the residual regressions; `_wn` (normalised weight); all-zero placeholders for xi race x year terms that do not exist in one-race subsamples | `SW_status 1` |
| `pi_s_estimation.do` | all-zero placeholders, in xi's order, for race / wife's race / cohort dummies that the hard-coded mata lists name but that a one-race subsample lacks (no effect on the full sample), registered in xi's own drop list so that the next xi call removes them (2026-10-19: otherwise a surviving placeholder made xi rename the stub, e.g. `_Iwracea2`, and the mata lists failed with r(3200) on simulated panels without 'other race' couples or wives born before 1941); the wife's participation probit keeps its estimates when it stops at the iteration limit (perfect prediction in the White-head subsample; the full sample converges, unchanged) | |
| `variance_estimation.do`, `frisch_estimation.do` | `predict ..., residuals` (Stata 19 needs the option; `predict stub*` now defaults to fitted values and fails); weighted moments by scaling the instruments with `_wn` (Stata's `gmm` refuses weights with `nocommonesample`) | unweighted |
| `gmm_ado/*.ado` | `syntax` accepts weights (not used in the end; harmless) | |
| `bootstrap.do` | table/column settable by the caller; override hook `$OVR`; calls `chain.do` after `frisch_estimation.do` | |

## How to run

```
python code/build_flags.py <WORK>            # flags.dta / flags.csv in the work folder; copy psid_cons.dta there too
bash code/run_all.sh base a_nowork ...       # specs/<name>.do; WORK is set inside the spec files
StataMP-64 /e do code/run_step2.do              # attrition.do on WORK/base, step2.do on the listed specs
python code/separation.py <WORK> ; python code/compile_results.py <WORK> ; python code/assemble.py
```

`WORK` (intermediate .dta, about 1 GB with all specs) was a local scratch folder, not the repo and not Dropbox. Run
time: a point-estimate run is about 2 minutes; a bootstrap replication about 30 seconds; 50 replications of the
preference step and 50 of the outside-insurance step per specification (BPS: 200) took about one hour per
specification with four instances in parallel.

## Caveats

- Bootstrap: 50 replications (BPS 200) for the specifications marked in Table S1's last row (the other columns: second-step GMM s.e., dagger), households resampled, s.e. = IQR / 1.349 (BPS's rule). As in BPS, the
  residual regressions are not re-estimated inside the bootstrap.
- Weighted runs: PSID family longitudinal weights in the residual regressions, both GMM steps (through the
  instruments) and the chain means; not in the tax-function and pi / s projections.
- BPS's code keeps the 1997 immigrant refresher sample (`seo` = 0 for ER30001 3001-3511) although footnote 15 of the
  paper says it is excluded: 11% of `data4estimation.dta` rows. IGE's PSID files (SRC + SEO) carry no displacement
  flags for it, so Step 2 shares and event studies use BPS's rows less that sample; Table 7 and all Step 1 estimates
  use all of BPS's rows.
- Displacement dating: a husband's or wife's job end is assigned to the calendar year it ended (19 / 25's rules);
  a BPS row with income year t carries the displacements of calendar years t-1 and t (its two-year difference).
