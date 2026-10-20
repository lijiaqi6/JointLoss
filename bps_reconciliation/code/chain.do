/* [bps_reconciliation, 2026-10-18] Insurance accounting of BPS p. 425 (eq. 11), computed in every run / bootstrap rep.
   Called by bootstrap.do right after frisch_estimation.do, with the transposed estimates table in memory
   (_varname value se t_stat). Reads $output/$directory/data_$poststring (household-level kappas).
   Response of consumption to a 10% permanent fall in the husband's wage (percent):
     ch_c0 = 10*E[s]                          fixed labor supply, no savings, no taxes
     ch_c1 = 10*E[(1-tau)s]                   + progressive taxes and transfers
     ch_c2 = 10*E[(1-tau)s k7]                + husband's own labor supply (k7 = 1 + his Marshallian elasticity)
     ch_c3 = 10*E[(1-tau)(s k7 + (1-s) k11)]  + wife's labor supply (added worker): household earnings response
     ch_c4 = 10*E[k3]                         + savings: consumption response kappa_c,v1
   Shares of the insured amount c0 - c4: government (c0-c1), family labor supply (c1-c3), savings (c3-c4).
   Same for Food-Stamp-eligible households (FSB_pay > 0): ch_f0 ... ch_f4.
   Marshallian (Table 5 col 1): ch_m_h1v1 = E[k7]-1, ch_m_h2v2 = E[k12]-1, ch_m_h2v1 = E[k11], ch_m_h1v2 = E[k8],
   ch_m_cv1 = E[k3], ch_m_cv2 = E[k4]; Frisch (Table 5 col 1): ch_f_h1u1 = E[k5]-1, ch_f_h2u2 = E[k10]-1,
   ch_f_h1u2 = E[k6], ch_f_h2u1 = E[k9], ch_f_cu1 = E[k1], ch_f_cu2 = E[k2]. */
preserve
use "$output/$directory/data_$poststring", clear
gen _w = 1
if "$WGTV"!="" replace _w = $WGTV
gen _ok = k3!=. & k7!=. & k11!=. & s_hat!=. & tau!=.
gen _c0 = 10*s_hat
gen _c1 = 10*(1-tau)*s_hat
gen _c2 = 10*(1-tau)*s_hat*k7
gen _c3 = 10*(1-tau)*(s_hat*k7 + (1-s_hat)*k11)
gen _c4 = 10*k3
local names ""
local vals ""
forvalues j=0/4 {
	qui su _c`j' [aw=_w] if _ok
	local ch_c`j' = r(mean)
	cap qui su _c`j' [aw=_w] if _ok & FSB_pay>0 & FSB_pay!=.
	local ch_f`j' = r(mean)
	if _rc local ch_f`j' = .
}
qui su _ok if _ok
local ch_n = r(N)
cap qui su _ok if _ok & FSB_pay>0 & FSB_pay!=.
local ch_nfs = r(N)
local ch_tot = `ch_c0' - `ch_c4'
local ch_gov = (`ch_c0' - `ch_c1')/`ch_tot'
local ch_fam = (`ch_c1' - `ch_c3')/`ch_tot'
local ch_sav = (`ch_c3' - `ch_c4')/`ch_tot'
local ch_ftot = `ch_f0' - `ch_f4'
local ch_fgov = (`ch_f0' - `ch_f1')/`ch_ftot'
local ch_ffam = (`ch_f1' - `ch_f3')/`ch_ftot'
local ch_fsav = (`ch_f3' - `ch_f4')/`ch_ftot'
foreach k in 1 2 3 4 5 6 7 8 9 10 11 12 {
	qui su k`k' [aw=_w] if _ok
	local K`k' = r(mean)
}
local ch_m_h1v1 = `K7'-1
local ch_m_h2v2 = `K12'-1
local ch_m_h2v1 = `K11'
local ch_m_h1v2 = `K8'
local ch_m_cv1  = `K3'
local ch_m_cv2  = `K4'
local ch_f_h1u1 = `K5'-1
local ch_f_h2u2 = `K10'-1
local ch_f_h1u2 = `K6'
local ch_f_h2u1 = `K9'
local ch_f_cu1  = `K1'
local ch_f_cu2  = `K2'
qui su tau [aw=_w] if _ok
local ch_tau = r(mean)
restore
foreach v in ch_c0 ch_c1 ch_c2 ch_c3 ch_c4 ch_tot ch_gov ch_fam ch_sav ch_f0 ch_f1 ch_f2 ch_f3 ch_f4 ch_ftot ch_fgov ch_ffam ch_fsav ///
	ch_m_h1v1 ch_m_h2v2 ch_m_h2v1 ch_m_h1v2 ch_m_cv1 ch_m_cv2 ch_f_h1u1 ch_f_h2u2 ch_f_h1u2 ch_f_h2u1 ch_f_cu1 ch_f_cu2 ch_tau ch_n ch_nfs {
	local nn = _N + 1
	qui set obs `nn'
	qui replace _varname = "`v'" in `nn'
	qui replace value = ``v'' in `nn'
}
if "$bootstraprep"=="0" {
	save "$output/$directory/estch_$poststring", replace
	outsheet using "$output/$directory/estch_$poststring.csv", replace comma
}
