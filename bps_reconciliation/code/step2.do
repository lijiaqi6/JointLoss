/* [bps_reconciliation, 2026-10-18] Step 2: displacement and joint displacement inside BPS's panel.
   Runs on the residual files of finished specifications (run_spec.do): <WORK>/<spec>/data3_resid_cons5_part0.dta,
   which carry build_flags.py's flags (merged in psid_sample.do by year x interview number).
   Globals: WORK, S2SPECS (list of spec folders). Writes <WORK>/step2_results.dta/.csv
   (spec, block, outcome, term, b, se, p, N, nev).
   Flags of a row with income year t (difference x_t - x_{t-2}): displacement in calendar year t-1 or t (k = 0);
   suffix _n: in t+1 or t+2 (the row is the interval before the event, k = -1); _p: in t-3 or t-2 (k = +1).
   h only = husband displaced, wife not (same interval); w only = wife displaced, husband not; joint = both.
   Only rows whose head is in IGE's PSID person file (SRC + SEO; BPS's code also keeps the 1997 immigrant
   refresher, for which IGE has no displacement flags) enter the displacement blocks. */
set more off
tempname P
postfile `P' str16 spec str12 block str24 outcome str24 term double(b se p) long(N nev) using "$WORK/step2_results", replace

foreach sp of global S2SPECS {
	use "$WORK/`sp'/data3_resid_cons5_part0.dta", clear
	tsset person year
	keep if h_match==1
	foreach s in "" "_n" "_p" {
		gen ho`s' = hd`s'==1 & wd`s'==0
		gen wo`s' = wd`s'==1 & hd`s'==0
		gen jt`s' = hd`s'==1 & wd`s'==1
	}
	gen dpart = wife_employed - l2.wife_employed
	gen entry = (wife_employed==1 & l2.wife_employed==0) if dpart!=.
	gen exitn = -(wife_employed==0 & l2.wife_employed==1) if dpart!=.
	gen arc_y  = (oly - l2.oly)/((oly + l2.oly)/2)
	gen arc_yw = (owly - l2.owly)/((owly + l2.owly)/2) if owly!=. & l2.owly!=.
	replace arc_yw = 0 if owly==0 & l2.owly==0
	gen dlogc_raw = log(totcons) - log(l2.totcons)

	* ---------------- 1. shares of couple-years with a displacement (BPS rows; rows with a husband wage difference)
	foreach v in hd wd jd jd_sy hs ws wa hq {
		qui su `v'
		post `P' ("`sp'") ("share") ("all_rows") ("`v'") (r(mean)) (.) (.) (r(N)) (r(sum))
		qui su `v' if uw!=.
		post `P' ("`sp'") ("share") ("rows_duw") ("`v'") (r(mean)) (.) (.) (r(N)) (r(sum))
		qui su `v' if uw!=. & uww!=.
		post `P' ("`sp'") ("share") ("rows_duw_duww") ("`v'") (r(mean)) (.) (.) (r(N)) (r(sum))
	}
	qui su wd if hd==1
	post `P' ("`sp'") ("share") ("cond") ("P(wd|hd)") (r(mean)) (.) (.) (r(N)) (r(sum))
	qui su wd if hd==0
	post `P' ("`sp'") ("share") ("cond") ("P(wd|no hd)") (r(mean)) (.) (.) (r(N)) (r(sum))
	qui su wd if hd==1 & l2.wife_employed==1
	post `P' ("`sp'") ("share") ("cond") ("P(wd|hd,wemp t-2)") (r(mean)) (.) (.) (r(N)) (r(sum))
	qui su wd if hd==0 & l2.wife_employed==1
	post `P' ("`sp'") ("share") ("cond") ("P(wd|no hd,wemp t-2)") (r(mean)) (.) (.) (r(N)) (r(sum))

	* ---------------- 2. event study with BPS residuals (k = -1, 0, +1; reference: rows with no displacement nearby)
	foreach y in uc uy uyw uw uww utoty dpart arc_y arc_yw dlogc_raw {
		cap noisily reg `y' ho_n wo_n jt_n ho wo jt ho_p wo_p jt_p, cluster(person)
		if _rc continue
		local N = e(N)
		foreach t in ho_n wo_n jt_n ho wo jt ho_p wo_p jt_p {
			qui count if `t'==1 & e(sample)
			local nev = r(N)
			local bb = _b[`t']
			local ss = _se[`t']
			post `P' ("`sp'") ("event") ("`y'") ("`t'") (`bb') (`ss') (2*ttail(e(df_r),abs(`bb'/`ss'))) (`N') (`nev')
		}
		cap {
			lincom jt - ho
			post `P' ("`sp'") ("event") ("`y'") ("jt-ho") (r(estimate)) (r(se)) (r(p)) (`N') (.)
			lincom jt_p - ho_p
			post `P' ("`sp'") ("event") ("`y'") ("jt_p-ho_p") (r(estimate)) (r(se)) (r(p)) (`N') (.)
		}
	}

	* ---------------- 3. cross moments with and without displacement couple-years
	gen m_ww   = uw*uww
	gen m_yy   = uy*uyw
	gen m_cy   = uc*uy
	gen m_ww_l = uw*l2.uww
	gen m_wwl  = l2.uw*uww
	gen m_wwlag = (m_ww_l + m_wwl)/2
	foreach m in m_ww m_wwlag m_yy m_cy {
		cap {
			reg `m', cluster(person)
			post `P' ("`sp'") ("moment") ("`m'") ("all") (_b[_cons]) (_se[_cons]) (2*ttail(e(df_r),abs(_b[_cons]/_se[_cons]))) (e(N)) (.)
			reg `m' if hd==0 & wd==0, cluster(person)
			post `P' ("`sp'") ("moment") ("`m'") ("no_disp") (_b[_cons]) (_se[_cons]) (2*ttail(e(df_r),abs(_b[_cons]/_se[_cons]))) (e(N)) (.)
			reg `m' if jd==0, cluster(person)
			post `P' ("`sp'") ("moment") ("`m'") ("no_joint") (_b[_cons]) (_se[_cons]) (2*ttail(e(df_r),abs(_b[_cons]/_se[_cons]))) (e(N)) (.)
			reg `m' hd wd jd, cluster(person)
			foreach t in hd wd jd {
				post `P' ("`sp'") ("moment") ("`m'") ("shift_`t'") (_b[`t']) (_se[`t']) (2*ttail(e(df_r),abs(_b[`t']/_se[`t']))) (e(N)) (.)
			}
		}
	}
}

* ---------------- 4. Table 7 (added worker, extensive margin) and its split into entries and exits; all rows
* (immigrant sample included, as in BPS), code as in tables_7_8_9.do l. 211-240
foreach sp of global S2SPECS {
	use "$WORK/`sp'/data3_resid_cons5_part0.dta", clear
	xtset person year
	g duw=uw
	gen partw=log_ww!=.
	sort person year
	gen dpart=partw-l2.partw
	gen entry = (partw==1 & l2.partw==0) if dpart!=.
	gen exitn = -(partw==0 & l2.partw==1) if dpart!=.
	gen IV_tran=-f2.duw
	gen IV_perm=(l2.duw+duw+f2.duw)
	gen IV_perm2=IV_perm^2
	gen IV_tran2=IV_tran^2
	gen agew2=agew^2
	g age2=age^2
	sort person year
	gen dage_y=age_youngest-l2.age_youngest
	gen nb = age_y==1
	gen dnb = nb-l2.nb
	foreach y in dpart entry exitn {
		foreach iv in perm tran {
			cap noisily xi: ivregress 2sls `y' (duw=IV_`iv'*) i.year agew agew2 age age2 i.weduc i.educ dkids dage_y dnb i.state i.smsa,cluster(person)
			if _rc continue
			local bb = _b[duw]
			local ss = _se[duw]
			qui count if e(sample) & `y'!=0
			post `P' ("`sp'") ("t7") ("`y'") ("theta_`iv'") (`bb') (`ss') (2*normal(-abs(`bb'/`ss'))) (e(N)) (r(N))
		}
	}
	* the same, h_match rows only, with the couple-year's displacement flags as controls
	keep if h_match==1
	foreach y in dpart entry exitn {
		cap noisily xi: ivregress 2sls `y' (duw=IV_perm*) hd wd jd i.year agew agew2 age age2 i.weduc i.educ dkids dage_y dnb i.state i.smsa,cluster(person)
		if _rc continue
		foreach t in duw hd wd jd {
			local bb = _b[`t']
			local ss = _se[`t']
			post `P' ("`sp'") ("t7ctl") ("`y'") ("`t'") (`bb') (`ss') (2*normal(-abs(`bb'/`ss'))) (e(N)) (.)
		}
	}
}
postclose `P'
use "$WORK/step2_results", clear
outsheet using "$WORK/step2_results.csv", replace comma
