/* 	This file prepare the data for estimation  */ 

cd "$output"

u data3,clear

/* merge minimum wage data */ 
sort state
merge state using "$do/psid_states"
drop _merge

sort state_st year
merge state_st year using "$do/min_wage"
drop if _merge!=3
drop _merge

*** merge prices
sort year
merge year using "$do\price_indices"
keep if _m==3
drop _m

* Change base year to 2000
foreach var of varlist p_* {
	su `var' if year==100
	local denom=r(mean)
	replace `var'=`var'/`denom'
}

* Apply configuration
gen price=p_totcons
replace tot_assets3 = tot_assets3/price

sort person year

***************************
*** Additional Sampling ***
***************************
/*
Note: 
-----
(1) Sampling on not working males drops these households. 
(2) Sampling on extreme values (min. wage and 'jumps') does not remove the observations 
	with these values, but replaces the value for the particular variable with a missing value
	so it is not in use for the particular relevant moment
*/

/* Replace observations with wage below half the hourly minimum wage by missing */
gen oly = ly
gen owly = wly
* [bps_reconciliation] switch SW_minw (1 = BPS half-minimum-wage trim; 0 = off)
if $SW_minw==1 {
	replace ly=.  if (ly/hours)<0.5*min_wage
	replace wly=. if (wly/hourw)<0.5*min_wage
}

save data4estimation_nopart, replace	/* Save here to use later as the sample with non-working males for col 1 of Table 8 */

/* 	We remove obervations with eligibility for transfers 2 times 
	or larger than the earned household income (These are only
	7 observations of working males)
	Note that to do that we run here once the tax code policy. */ 

global het_elasticities=12
global tax_graph=0	
do "$do/tax_rate_estimation_snap"
macro drop tax_graph het_elasticities
 
gen 	no_work_d = (hours==0 | oly==0)			/* Note that there are no missing hours. The missing ly is only if the minimum_wage criteria is applied */ 
replace no_work_d = 1 if psample == 0			/* psample==0 comes from tax_rate_estimation_snap */ 
* [bps_reconciliation] switch SW_nowork (0 = BPS person-level drop; 1 = drop only the year)
save "$output/prep_nowork", replace
if $SW_nowork==0 {
	egen todrop = max(no_work_d), by(person)
	drop if todrop == 1
}
else {
	drop if no_work_d == 1
}							/* keeping households where the prime earner is always working */ 

drop tax eitc FSB_pay tau xsi psample			/* Drop the tax variables - projection will be generated again as part of the bootstrap */  

/* Dependent variables and covariates for the estimation of the predicted part of wages, earnings and consumption as well as for selection equation */ 
gen log_y 	= log(ly) - log(price)
gen log_yw 	= log(wly) - log(price)
gen log_c	= log(totcons) - log(price)
gen log_c_nh= log(totcons_nh) - log(price)
gen log_w	= log(ly/hours) - log(price)
gen log_ww	= log(wly/hourw) - log(price)
gen log_toty= log(ly + wly) - log(price)		 

gen mort1_dum = (mortgage1>0 & mortgage1!=.)
gen mort2_dum = (mortgage2>0 & mortgage2!=.)

/* Replace the extreme jumps with missing values */ 
global pec_drop     = 0.25		 

tsset person year
local npec = 100/${pec_drop}
di `npec'

* [bps_reconciliation] switch SW_jump (1 = BPS jump / collapse-recovery trim; 0 = off)
save "$output/prep_prejump", replace
if $SW_jump==1 {
/* 	Generate the first difference for logs and the interaction between first difference and lagged first difference (which would be large in absolute value 
	for large values of transitory shocks or for measurement error */ 
	
foreach var of varlist log_* {
	gen d_`var' = `var' - l2.`var'
	gen d_`var'_lag = d_`var'*l2.d_`var'
}

/* Generate percentiles of the interacted difference by year */ 
foreach var of varlist d_*_lag {
	egen pec_`var'=  xtile(`var'), by(year) n(`npec') 
}

/* Assign missing values for the variable with the potential measurement error  */ 
foreach var of varlist log_*  {
	replace `var'=. if f2.pec_d_`var'_lag==1 	/* 	assigning missing values to the year with the jump */ 
}

/* Check the new distribution of the interacted lag */ 
foreach var of varlist log_* {
	gen d_`var'_trunc = `var' - l2.`var'
	gen d_`var'_trunc_lag = d_`var'_trunc*l2.d_`var'_trunc
}
su d_*_lag
drop d_* pec_*
}

replace log_w = . if log_y==. 
replace log_y = . if log_w==. 

replace log_ww = . if log_yw==. 
replace log_yw = . if log_ww==. 

/* Generate participation for the wife dummy */ 
gen wife_employed = log_ww!=.

* [bps_reconciliation] switch SW_dexcl: 1 = drop couple-years whose two-year interval contains a displacement of
* either spouse (hd | wd); 2 = joint displacements only (jd)
if $SW_dexcl==1 drop if hd==1 | wd==1
if $SW_dexcl==2 drop if jd==1
/* Prepare data for Table 8 regressions */ 
save data4estimation, replace

cd "$do"

erase "$output/data3.dta"
