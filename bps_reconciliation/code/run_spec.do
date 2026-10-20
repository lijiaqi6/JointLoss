/* [bps_reconciliation, 2026-10-18] One specification of BPS (2016) end to end, from BPS's psid_cons.dta.
   Call:  StataMP-64.exe /e do run_spec.do  with the globals below set in a small caller do-file (see the files in the specs folder).
   Globals (defaults = BPS as shipped):
     SPEC        name of the specification (output folder <WORK>/<SPEC>)
     WORK        local work folder for intermediate .dta files (not in the repo, not in Dropbox)
     SW_brk 0    1 = composition break only on a change of spouse identity        (psid_sample.do)
     SW_seo 0    1 = keep the SEO sample                                          (psid_sample.do)
     SW_race ""  1 white / 2 black head                                           (psid_sample.do)
     SW_minw 1   0 = no half-minimum-wage trim                                    (prepare_bootstrap.do)
     SW_nowork 0 1 = drop the zero-hours / zero-earnings year, not the husband     (prepare_bootstrap.do)
     SW_jump 1   0 = no jump / collapse-recovery trim                             (prepare_bootstrap.do)
     SW_dexcl 0  1 = drop couple-years with a displacement of either spouse; 2 = joint only
     SW_status 1 0 = no employment-status controls in the residual regressions    (residual_measures.do)
     WGT ""      "[pw=weight]" for PSID family longitudinal weights (residual regressions, both GMM steps, chain means)
     RUNS        list of runs: gmm10 (T4C11: age-varying variances, GMM s.e., Frisch, chain), gmm9 (T4C41: stationary
                 variances = Table 3 'all ages'), beta (T4C5 point), bs (T4C1 block bootstrap with BN reps), bsbeta
     BN          bootstrap replications (default 0)
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
global SW_specmax 1
global WGTV ""
if "$WGT"!="" global WGTV "weight"

global do "G:\My Drive\JointLoss\bps_reconciliation\code"
global output "$WORK\\$SPEC"
global graphs "$output\graphs"
cap mkdir "$output"
cap mkdir "$graphs"
adopath + "$do\gmm_ado"
* egenmore (egen xtile, used by prepare_bootstrap.do), ivreg2, ranktest: installed from SSC into code\ado on 2026-10-18
adopath + "$do\ado"

copy "$WORK\psid_cons.dta" "$output\psid_cons.dta", replace
copy "$WORK\flags.dta" "$output\flags.dta", replace

cd "$do"
di "SPEC $SPEC brk=$SW_brk seo=$SW_seo race=$SW_race minw=$SW_minw nowork=$SW_nowork jump=$SW_jump dexcl=$SW_dexcl status=$SW_status wgt=$WGT"
do psid_sample
do prepare_bootstrap
cd "$output"
use data4estimation, clear
count
cd "$do"
do residual_measures

foreach r of global RUNS {
	cd "$do"
	global OVR ""
	if "`r'"=="gmm10" {
		global table 4
		global column 11
	}
	if "`r'"=="gmm9" {
		global table 4
		global column 41
	}
	if "`r'"=="beta" {
		global table 4
		global column 5
		global OVR "$do\ovr_bn0.do"
	}
	if "`r'"=="bs" {
		global table 4
		global column 1
		global OVR "$do\ovr_bs.do"
	}
	if "`r'"=="bsbeta" {
		global table 4
		global column 5
		global OVR "$do\ovr_bsbeta.do"
	}
	timer clear 1
	timer on 1
	cap noisily do bootstrap
	di "RUN `r' rc=" _rc
	timer off 1
	timer list 1
	* save the point-estimate table of this run
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
