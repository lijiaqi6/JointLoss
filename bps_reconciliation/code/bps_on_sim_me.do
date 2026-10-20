/* [WP1, 2026-10-20] GENERATED copy of bps_on_sim.do (do not edit; regenerate from bps_on_sim.do) with one hook:
   global OVRX <do-file>  is run after BPS's parameter file in the gmm9 / gmm10 runs (e.g. ovr_me0.do: BPS's
   measurement-error shares sh_me_y / sh_me_h / sh_me_w set to 0, i.e. no correction). Everything else as
   bps_on_sim.do; OVRX is cleared at the end. */
/* [bps_reconciliation, 2026-10-18] BPS (2016) estimator on an arbitrary PSID-shaped household-year panel
   (simulated data from Paper A's model, written by sim_panel_writer.py, or BPS's own psid_cons.dta for the check).
   Usage and the input layout: IGE/bps_reconciliation/HARNESS.md.

   Call (Stata batch):  StataMP-64.exe /e do caller.do   where caller.do sets the globals below and then
                        do "G:\My Drive\JointLoss\bps_reconciliation\code\bps_on_sim.do"

   Globals
     INPUT       full path of the input .dta (layout: HARNESS.md, "Input layout"); may contain the flag variables
                 (h_pid w_pid hd wd jd ...); if it does not, neutral flags are created (no break / no exclusion)
     SPEC        name of the specification; output folder <WORK>/<SPEC>
     WORK        work folder for intermediate files (scratch, not the repo, not Dropbox)
     RESULTS     cumulative one-row-per-spec CSV (appended; header written when the file is new);
                 default <WORK>/bps_on_sim_results.csv
     RUNS        default "gmm10 gmm9 beta"  (gmm10: T4C11, age-varying variances = Table 3 by age + Table 4 col 1 +
                 Frisch / Marshallian + insurance chain; gmm9: T4C41, stationary variances = Table 3 'all ages';
                 beta: T4C5 point estimate of outside insurance; bs / bsbeta: block bootstraps with BN reps)
     BN          bootstrap replications for bs / bsbeta (default 0)
   Switches (defaults = BPS as shipped), passed to BPS's own do-files (edited copies in this folder):
     SW_nowork 0  no-work rule: 0 = drop the husband's whole history if any year has zero hours / zero earnings /
                  transfers >= 2x earnings (person level, BPS); 1 = drop only that year (observation level)
     SW_status 1  employment-status controls (both spouses' levels, two-year changes, level x year) in the
                  consumption and earnings residual regressions; 0 = removed
     SW_minw   1  half-state-minimum-wage trim of earnings (1 = on)
     SW_jump   1  jump / collapse-recovery trim, bottom 0.25 pct of dlog x_t * dlog x_{t-2} by year (1 = on)
     SW_seo    0  0 = drop rows with seo==1 (BPS drop the SEO); 1 = keep them
     SW_brk    0  composition break: 0 = BPS (break at fchg>1); 1 = break only if h_pid / w_pid change
     SW_race   "" "" all; 1 White head; 2 Black head
     SW_dexcl  0  1 = drop couple-years with hd|wd; 2 = drop jd couple-years
     WGT       "" "[pw=weight]" for weighted residual regressions, GMM moments and chain means
   All SW_* / WGT / RUNS / BN globals are cleared at the end so that several specs in one session do not leak.

   Output in <WORK>/<SPEC>:
     est_<run>.dta/.csv          BPS's point-estimate table of each run (+ the insurance chain, chain.do)
     bps_on_sim_long.csv         every number of every run (spec, run, name, value, se)
     bps_on_sim_row.csv          the key outputs, one row (also appended to $RESULTS)
*/
set more off
set matsize 11000
if "$SW_brk"==""    global SW_brk 0
if "$SW_seo"==""    global SW_seo 0
if "$SW_minw"==""   global SW_minw 1
if "$SW_nowork"=="" global SW_nowork 0
if "$SW_jump"==""   global SW_jump 1
if "$SW_dexcl"==""  global SW_dexcl 0
if "$SW_status"=="" global SW_status 1
if "$BN"==""        global BN 0
if "$RUNS"==""      global RUNS "gmm10 gmm9 beta"
if "$RESULTS"==""   global RESULTS "$WORK\bps_on_sim_results.csv"
global SW_imm ""
global SW_specmax 1
global WGTV ""
if "$WGT"!="" global WGTV "weight"

global do "G:\My Drive\JointLoss\bps_reconciliation\code"
global output "$WORK\\$SPEC"
global graphs "$output\graphs"
cap mkdir "$WORK"
cap mkdir "$output"
cap mkdir "$graphs"
adopath + "$do\gmm_ado"
adopath + "$do\ado"
di "BPS_ON_SIM spec=$SPEC input=$INPUT"
di "  nowork=$SW_nowork status=$SW_status minw=$SW_minw jump=$SW_jump seo=$SW_seo brk=$SW_brk race=$SW_race dexcl=$SW_dexcl wgt=$WGT runs=$RUNS"

*=====================================================================
* 1. Read and validate the input; split it into psid_cons.dta + flags
*=====================================================================
use "$INPUT", clear
local req "year id person seo state fsize age sex agew kids marit mortgage1 mortgage2 outkid race1 race2 race3 race4 wrace1 wrace2 wrace3 wrace4 smsa hours hourw educ weduc educ_ind weduc_ind weight empst wempst ly wly fchg totcons totcons_nh tot_assets3 tyoth"
local miss ""
foreach v of local req {
	cap confirm variable `v'
	if _rc local miss "`miss' `v'"
}
if "`miss'"!="" {
	di as error "bps_on_sim: input lacks required variables:`miss'"
	exit 111
}
* BPS's tax / transfer schedules, Food Stamp parameters and poverty lines exist only for income years 1998-2008
cap assert inlist(year, 98, 100, 102, 104, 106, 108)
if _rc {
	di as error "bps_on_sim: year must be the income year - 1900 in {98,100,...,108} (PSID waves 1999-2009)"
	exit 459
}
isid year id
isid person year
assert hours!=.
local N_input = _N
* BPS's wife-participation probit (residual_measures.do) ends with 'testparm _Imor*', which aborts (r(111)) when the
* mortgage dummies never vary (a model without housing debt). In every run used here the participation correction
* is off (fix_var 10: inv_mills and z_eta are set to 0), so the probit's output is not used; a seeded random
* placeholder dummy in mortgage2 lets the code run and changes no estimate. Flagged as mort_placeholder = 1.
gen byte _m = (mortgage1>0 & mortgage1!=.) | (mortgage2>0 & mortgage2!=.)
qui su _m
local mort_placeholder = (r(sd)==0 | r(sd)==.)
drop _m
if `mort_placeholder' {
	set seed 20161
	replace mortgage2 = (runiform()<0.5)
	di "bps_on_sim: mortgages never positive -> random placeholder dummy in mortgage2 (probit exclusion only; not used with fix_var 10)"
}

local flagv "h_pid w_pid hd hs hq wd ws wq wa jd jd_sy hd_n hs_n hq_n wd_n ws_n wq_n wa_n jd_n jd_sy_n hd_p hs_p hq_p wd_p ws_p wq_p wa_p jd_p jd_sy_p h_match w_match"
local have ""
foreach v of local flagv {
	cap confirm variable `v'
	if !_rc local have "`have' `v'"
}
local has_flags = ("`have'"!="")
preserve
keep year id `have'
foreach v in h_pid w_pid {
	cap confirm variable `v'
	if _rc {
		gen double `v' = -1
		di "bps_on_sim: `v' absent, set to -1 (SW_brk=1 then equals BPS's break rule)"
	}
}
foreach v in hd wd jd {
	cap confirm variable `v'
	if _rc {
		gen byte `v' = 0
		di "bps_on_sim: `v' absent, set to 0 (SW_dexcl has no effect)"
	}
}
save "$output\flags.dta", replace
restore
if "`have'"!="" drop `have'
save "$output\psid_cons.dta", replace

*=====================================================================
* 2. BPS's chain: sample, preparation, residuals, GMM runs, accounting
*=====================================================================
cd "$do"
do psid_sample
do prepare_bootstrap

* sample counts and trim / no-work diagnostics
use "$output\prep_nowork.dta", clear
qui su no_work_d
local nowork_obs = r(mean)
egen _td = max(no_work_d), by(person)
qui su _td
local nowork_drop = r(mean)
local N_prep = _N
use "$output\data4estimation_nopart.dta", clear
gen _d = 0
cap replace _d = (hd==1 | wd==1)
gen _tm = (oly>0 & oly!=. & ly==.) | (owly>0 & owly!=. & wly==.)
qui count if _tm
local n_trim_minw = r(N)
qui count if _tm & _d
local n_trim_minw_disp = r(N)
use "$output\data4estimation.dta", clear
local N_sample = _N
qui count if wife_employed==1
local N_wife_emp = r(N)
foreach f in hd wd jd {
	cap qui count if `f'==1
	local n_`f' = cond(_rc, ., r(N))
}
local n_trim_jump = .
local n_trim_jump_disp = .
if $SW_jump==1 {
	* rows where the jump trim set at least one log variable to missing (pre-trim values: prep_prejump.dta)
	keep person year log_y log_yw log_c log_w log_ww hd wd
	foreach v in log_y log_yw log_c log_w log_ww {
		ren `v' a_`v'
	}
	merge 1:1 person year using "$output\prep_prejump.dta", keepusing(log_y log_yw log_c log_w log_ww) keep(master match) nogen
	gen _tj = 0
	foreach v in log_y log_yw log_c log_w log_ww {
		replace _tj = 1 if `v'!=. & a_`v'==.
	}
	qui count if _tj
	local n_trim_jump = r(N)
	qui count if _tj & (hd==1 | wd==1)
	local n_trim_jump_disp = r(N)
}

cd "$do"
do residual_measures
use "$output\estimation_input_all5_rhs1_part0.dta", clear
qui count if duw!=.
local N_duw = r(N)
qui count if duww!=.
local N_duww = r(N)
qui count if duc!=.
local N_duc = r(N)

foreach r of global RUNS {
	cd "$do"
	global OVR ""
	global table 4
	if "`r'"=="gmm10"  global column 11
	if "`r'"=="gmm9"   global column 41
	if "`r'"=="beta" {
		global column 5
		global OVR "$do\ovr_bn0.do"
	}
	if "`r'"=="bs" {
		global column 1
		global OVR "$do\ovr_bs.do"
	}
	if "`r'"=="bsbeta" {
		global column 5
		global OVR "$do\ovr_bsbeta.do"
	}
	if "$OVRX"!="" & inlist("`r'","gmm9","gmm10") global OVR "$OVRX"
	cap erase "$output\est_`r'.dta"
	timer clear 1
	timer on 1
	cap noisily do bootstrap
	di "RUN `r' rc=" _rc
	timer off 1
	timer list 1
	cap {
		use "$output/$directory/estch_$poststring", clear
		gen spec = "$SPEC"
		gen run = "`r'"
		save "$output/est_`r'", replace
		outsheet using "$output/est_`r'.csv", replace comma
	}
	cap {
		use "$output/$directory/reps_$poststring", clear
		save "$output/reps_`r'", replace
	}
}
cd "$do"

*=====================================================================
* 3. Results: long file (everything) and the one-row key file
*=====================================================================
clear
gen str20 run = ""
gen str32 name = ""
gen double value = .
gen double se = .
tempfile long
save `long', emptyok
foreach r of global RUNS {
	cap confirm file "$output\est_`r'.dta"
	if !_rc {
		use "$output\est_`r'.dta", clear
		keep _varname value se
		ren _varname name
		gen str20 run = "`r'"
		append using `long'
		save `long', replace
		local n = _N
		forvalues i=1/`n' {
			if run[`i']=="`r'" {
				local k = name[`i']
				local V_`r'_`k' = value[`i']
				local S_`r'_`k' = se[`i']
			}
		}
	}
}
use `long', clear
gen str40 spec = "$SPEC"
order spec run name value se
export delimited using "$output\bps_on_sim_long.csv", replace

* key outputs: <column> <run> <BPS name>
local K ""
* Table 3, all ages (stationary variances, T4C41)
local K "`K' T3_s_u1 gmm9 s_u1_1 T3_s_v1 gmm9 s_v1_1 T3_s_u2 gmm9 s_u2_1 T3_s_v2 gmm9 s_v2_1 T3_c_u1u2 gmm9 r_u1u2_1 T3_c_v1v2 gmm9 r_v1v2_1"
* Table 3 by husband's / wife's age group (T4C11)
forvalues a=1/5 {
	local K "`K' T3a`a'_s_u1 gmm10 s_u1_`a' T3a`a'_s_v1 gmm10 s_v1_`a' T3a`a'_s_u2 gmm10 s_u2_`a' T3a`a'_s_v2 gmm10 s_v2_`a' T3a`a'_c_u1u2 gmm10 r_u1u2_`a' T3a`a'_c_v1v2 gmm10 r_v1v2_`a'"
}
* Table 4 col 1 (T4C11)
local K "`K' E_pi gmm10 pi E_s gmm10 s_report eta_c_p gmm10 eta_c_p eta_h1_w1 gmm10 eta_h1_w1 eta_h2_w2 gmm10 eta_h2_w2 eta_c_w1 gmm10 eta_c_w1 eta_c_w2 gmm10 eta_c_w2 eta_h1_w2 gmm10 eta_h1_w2 eta_h2_w1 gmm10 eta_h2_w1 eta_h1_p gmm10 eta_h1_p eta_h2_p gmm10 eta_h2_p s_omega gmm10 s_omega N_gmm gmm10 observations"
* Table 5 col 1: Marshallian and Frisch means (chain.do)
local K "`K' M_h1v1 gmm10 ch_m_h1v1 M_h2v2 gmm10 ch_m_h2v2 M_h2v1 gmm10 ch_m_h2v1 M_h1v2 gmm10 ch_m_h1v2 M_cv1 gmm10 ch_m_cv1 M_cv2 gmm10 ch_m_cv2"
local K "`K' F_h1u1 gmm10 ch_f_h1u1 F_h2u2 gmm10 ch_f_h2u2 F_h1u2 gmm10 ch_f_h1u2 F_h2u1 gmm10 ch_f_h2u1 F_cu1 gmm10 ch_f_cu1 F_cu2 gmm10 ch_f_cu2"
* insurance chain (BPS p. 425) and split, all and Food-Stamp-eligible
foreach c in c0 c1 c2 c3 c4 tot gov fam sav f0 f1 f2 f3 f4 ftot fgov ffam fsav tau n nfs {
	local K "`K' ch_`c' gmm10 ch_`c'"
}
* outside insurance (Table 4 col 5) and Table 4 col 4 (stationary variances) for reference
local K "`K' beta beta beta beta_eta_c_p beta eta_c_p T4c4_eta_c_p gmm9 eta_c_p T4c4_eta_h2_w2 gmm9 eta_h2_w2 T4c4_ch_fam gmm9 ch_fam"

clear
set obs 1
gen str40 spec = "$SPEC"
gen str244 input = `"$INPUT"'
gen sw_nowork = $SW_nowork
gen sw_status = $SW_status
gen sw_minw = $SW_minw
gen sw_jump = $SW_jump
gen sw_seo = $SW_seo
gen sw_brk = $SW_brk
gen str2 sw_race = "$SW_race"
gen sw_dexcl = $SW_dexcl
gen str20 wgt = "$WGTV"
gen N_input = `N_input'
gen N_prep = `N_prep'
gen N_sample = `N_sample'
gen N_wife_emp = `N_wife_emp'
gen N_duw = `N_duw'
gen N_duww = `N_duww'
gen N_duc = `N_duc'
gen nowork_obs_share = `nowork_obs'
gen nowork_drop_share = `nowork_drop'
gen n_trim_minw = `n_trim_minw'
gen n_trim_minw_disp = `n_trim_minw_disp'
gen n_trim_jump = `n_trim_jump'
gen n_trim_jump_disp = `n_trim_jump_disp'
gen n_hd = `n_hd'
gen n_wd = `n_wd'
gen n_jd = `n_jd'
gen has_flags = `has_flags'
gen mort_placeholder = `mort_placeholder'
local nk : word count `K'
forvalues j=1(3)`nk' {
	local col : word `j' of `K'
	local run : word `=`j'+1' of `K'
	local key : word `=`j'+2' of `K'
	local v "`V_`run'_`key''"
	local s "`S_`run'_`key''"
	if "`v'"=="" local v "."
	if "`s'"=="" local s "."
	gen double `col' = `v'
	if substr("`col'",1,2)=="T3" | substr("`col'",1,3)=="eta" | "`col'"=="beta" | "`col'"=="s_omega" {
		gen double `col'_se = `s'
	}
}
* correlations of the spouses' shocks (all ages): cov / sqrt(var1 var2), missing if a variance is negative
gen double rho_u1u2 = T3_c_u1u2/sqrt(T3_s_u1*T3_s_u2) if T3_s_u1>0 & T3_s_u2>0
gen double rho_v1v2 = T3_c_v1v2/sqrt(T3_s_v1*T3_s_v2) if T3_s_v1>0 & T3_s_v2>0
gen str19 run_time = "`c(current_date)' `c(current_time)'"
export delimited using "$output\bps_on_sim_row.csv", replace
tempfile row
save `row'
cap confirm file "$RESULTS"
if !_rc {
	import delimited using "$RESULTS", clear stringcols(1 2 9 11) varnames(1) case(preserve)
	append using `row', force
}
export delimited using "$RESULTS", replace
di "BPS_ON_SIM done: $output\bps_on_sim_row.csv ; appended to $RESULTS"

macro drop OVRX
macro drop SW_brk SW_seo SW_minw SW_nowork SW_jump SW_dexcl SW_status SW_race SW_imm WGT WGTV RUNS BN SPEC INPUT
