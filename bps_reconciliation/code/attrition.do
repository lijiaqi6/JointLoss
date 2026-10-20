/* [bps_reconciliation, 2026-10-18] Step 2: which of BPS's restrictions drop the couple-years with a displacement.
   Replays psid_sample.do (l. 86-199) and prepare_bootstrap.do (merges, no-work rule) on the BASE specification's
   intermediate files, recording for each row of psid_cons.dta the step at which it leaves the sample.
   Inputs: <WORK>/base/sample_breaks.dta (psid_cons + flags + break_d, saved by psid_sample.do just before the break
   drop), <WORK>/base/prep_nowork.dta (after the minimum-wage and price merges and the tax code, before the no-work
   rule), <WORK>/base/data4estimation.dta, <WORK>/base/data3_resid_cons5_part0.dta.
   Universe U: married couples (marit 1, wife present, male head) with the husband aged 30-57 (age - 1, the
   retrospective convention of psid_sample.do l. 124), head in IGE's person file (SRC + SEO).
   Output: <WORK>/attrition.dta/.csv: step, rows of U remaining, of which with hd / wd / jd / any (hd|wd), and the
   number of distinct couples (h_pid x w_pid) with a joint displacement. */
set more off
if "$B"=="" global B "$WORK/base"
use "$B/sample_breaks", clear
gen long rowid = _n
gen U = marit==1 & agew>0 & agew!=. & sex==1 & inrange(age-1,30,57) & h_match==1
keep if U==1
gen step = .
save "$WORK/att_U", replace

* replay of psid_sample.do on all rows; keep the keys that survive each step
use "$B/sample_breaks", clear
local s = 1
drop if break_d == 1
save "$WORK/att_k`s'", replace
local ++s
drop if marit!=1 | agew==0
save "$WORK/att_k`s'", replace
local ++s
drop if state==.|state==0|state==99
save "$WORK/att_k`s'", replace
local ++s
drop if sex==2
egen n=sum(person!=.),by(person)
egen na=sum(age==.),by(person)
drop if n==na
drop n na
egen n=sum(person!=.),by(person)
egen na=sum(agew==.),by(person)
drop if n==na
drop n na
save "$WORK/att_k`s'", replace
local ++s
egen lasty=max(year) if age!=.,by(person)
gen lastage=age if year==lasty
gen b=year-lastage
replace b=0 if b==.
egen yb=sum(b),by(person)
replace age=year-yb
drop lasty lastage b
replace age=age-1
replace agew=agew-1
drop if tot_assets3>=20000000&tot_assets3!=.
save "$WORK/att_k`s'", replace
local ++s
keep if age>=30 & age<=57
save "$WORK/att_k`s'", replace
local ++s
keep if seo==0
save "$WORK/att_k`s'", replace
local ++s
drop if educ==. | weduc==.
save "$WORK/att_k`s'", replace
local ++s
* prepare_bootstrap.do: state minimum wage and price merges, tax code; then the no-work rule
use "$B/prep_nowork", clear
save "$WORK/att_k`s'", replace
local ++s
keep if no_work_d==0
save "$WORK/att_k`s'_own", replace
use "$B/data4estimation", clear
save "$WORK/att_k`s'", replace
local ++s
use "$B/data3_resid_cons5_part0", clear
keep if uw!=.
save "$WORK/att_k`s'", replace
local ++s
use "$B/data3_resid_cons5_part0", clear
keep if uw!=. & uww!=.
save "$WORK/att_k`s'", replace
local nsteps = `s'

* steps: 1 composition break (fchg>1) | 2 not married / no wife | 3 state missing | 4 female head, age always missing
* 5 net worth >= $20M | 6 age outside 30-57 (BPS recode) | 7 SEO | 8 education missing | 9 min-wage / price merge
* 10 no-work rule (husband with a zero-hours / zero-earnings / transfer-eligible year: person-level) -> data4estimation
* 11 no husband wage difference (no t-2 obs of the couple, jump trim, half-min-wage trim)
* 12 no wife wage difference (wife not working in t or t-2, trims)
use "$WORK/att_U", clear
forvalues s=1/`nsteps' {
	preserve
	use "$WORK/att_k`s'", clear
	keep year id
	gen in`s' = 1
	tempfile k
	save `k'
	restore
	merge 1:1 year id using `k', keep(master match) nogen
	replace in`s' = 0 if in`s'==.
}
preserve
use "$WORK/att_k10_own", clear
keep year id
gen in10own = 1
tempfile k
save `k'
restore
merge 1:1 year id using `k', keep(master match) nogen
replace in10own = 0 if in10own==.
gen anyd = hd==1 | wd==1
gen cpl = string(h_pid,"%12.0f") + "_" + string(w_pid,"%12.0f")
save "$WORK/att_U_marks", replace

tempname P
postfile `P' int step str40 label long(rows hd wd jd anyd hs ws jd_cpl hd_cpl) using "$WORK/attrition", replace
local lab0 "U: married, husband 30-57, SRC+SEO"
local lab1 "composition break (fchg>1) year dropped"
local lab2 "not married / no wife"
local lab3 "state missing"
local lab4 "female head / age always missing"
local lab5 "net worth >= 20M"
local lab6 "age outside 30-57 (BPS age recode)"
local lab7 "SEO sample dropped"
local lab8 "education missing"
local lab9 "minimum-wage / price merge"
local lab10 "no-work rule (person-level) = data4estimation"
local lab11 "rows with a husband wage difference (duw)"
local lab12 "rows with both spouses' wage differences"
gen keep0 = 1
forvalues s=0/`nsteps' {
	if `s'>0 replace keep0 = keep0 & in`s'
	qui count if keep0
	local r = r(N)
	foreach v in hd wd jd anyd hs ws {
		qui count if keep0 & `v'==1
		local n_`v' = r(N)
	}
	qui egen _t = tag(cpl) if keep0 & jd==1
	qui count if _t==1
	local jc = r(N)
	drop _t
	qui egen _t = tag(h_pid) if keep0 & hd==1
	qui count if _t==1
	local hc = r(N)
	drop _t
	post `P' (`s') ("`lab`s''") (`r') (`n_hd') (`n_wd') (`n_jd') (`n_anyd') (`n_hs') (`n_ws') (`jc') (`hc')
}
* the no-work rule: rows dropped because that very year has zero hours / earnings vs other years of such husbands
replace keep0 = in1 & in2 & in3 & in4 & in5 & in6 & in7 & in8 & in9
foreach w in own other {
	if "`w'"=="own" gen _d = keep0 & in10own==0
	if "`w'"=="other" gen _d = keep0 & in10own==1 & in10==0
	qui count if _d
	local r = r(N)
	foreach v in hd wd jd anyd hs ws {
		qui count if _d & `v'==1
		local n_`v' = r(N)
	}
	local s = cond("`w'"=="own", 101, 102)
	post `P' (`s') ("no-work rule: `w' year") (`r') (`n_hd') (`n_wd') (`n_jd') (`n_anyd') (`n_hs') (`n_ws') (.) (.)
	drop _d
}
postclose `P'
use "$WORK/attrition", clear
list, clean noobs
outsheet using "$WORK/attrition.csv", replace comma

* which trims remove the husband's wage difference in data4estimation rows with a displacement
use "$B/prep_prejump", clear
keep year id log_w log_y log_ww log_yw
rename (log_w log_y log_ww log_yw) (pj_log_w pj_log_y pj_log_ww pj_log_yw)
tempfile pj
save `pj'
use "$B/data4estimation", clear
merge 1:1 year id using `pj', keep(master match) nogen
tsset person year
gen has_l2 = l2.year!=.
gen minw_h = (oly/hours)<0.5*min_wage & hours>0
gen minw_hl = l2.minw_h==1
gen jump_h = pj_log_w!=. & log_w==.
gen jump_hl = l2.jump_h==1
gen duw_ok = log_w!=. & l2.log_w!=.
keep if h_match==1
tempname Q
postfile `Q' str12 grp str40 reason long n using "$WORK/attrition_duw", replace
foreach g in hd wd jd none {
	if "`g'"=="none" gen _g = hd==0 & wd==0
	else gen _g = `g'==1
	qui count if _g
	post `Q' ("`g'") ("rows in data4estimation") (r(N))
	qui count if _g & duw_ok
	post `Q' ("`g'") ("husband wage difference available") (r(N))
	qui count if _g & !has_l2
	post `Q' ("`g'") ("no t-2 observation of the couple") (r(N))
	qui count if _g & has_l2 & (minw_h | minw_hl)
	post `Q' ("`g'") ("half-min-wage trim at t or t-2") (r(N))
	qui count if _g & has_l2 & !(minw_h | minw_hl) & (jump_h | jump_hl)
	post `Q' ("`g'") ("jump trim at t or t-2 (not min-wage)") (r(N))
	drop _g
}
postclose `Q'
use "$WORK/attrition_duw", clear
list, clean noobs
outsheet using "$WORK/attrition_duw.csv", replace comma
