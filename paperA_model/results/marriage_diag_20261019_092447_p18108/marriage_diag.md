# Marriage diagnostics: analytic start (inputs/start_analytic.json + start_overrides.json)

Size k_s2_era1_a20, K = 3, CRN seed 20261018, extensions {'cps_persist': True, 'cps_classif': False, 'cs_memory': False, 'borrow_wedge': True, 'hc_eta': True}. Both evaluations on common draws. 

## (A) Separation switched off (sig_E = sig_N = 0) against the start

Q: 11,726.0 at the start, 8,650.6 with separation off (change -3,075.4; noise floor about 30).

| Block | Q start | Q separation off | change |
|---|---:|---:|---:|
| Joint loss, monthly | 39.2 | 34.4 | -4.9 |
| Joint loss, annual | 23.6 | 49.4 | +25.9 |
| Base hazards | 122.9 | 110.4 | -12.5 |
| Her search | 246.2 | 598.1 | +351.9 |
| Her exits | 4,622.2 | 3,297.4 | -1,324.8 |
| His search | 61.0 | 78.3 | +17.3 |
| His earnings | 22.9 | 21.6 | -1.3 |
| Her earnings | 4.3 | 1.7 | -2.6 |
| Wage growth | 149.4 | 132.9 | -16.6 |
| Added work | 11.6 | 15.1 | +3.5 |
| Employment levels | 3,537.3 | 1,088.3 | -2,449.0 |
| Safety net | 163.1 | 172.2 | +9.0 |
| Separation | 3.0 | 1,220.9 | +1,217.9 |
| Wealth | 2,701.6 | 1,810.3 | -891.3 |
| Consumption | 17.6 | 19.9 | +2.2 |

| Moment | block | data | model (start) | model (separation off) | z start | z off |
|---|---|---:|---:|---:|---:|---:|
| sipp_wife_emp_s0 | Her search | 0.01892 | 0.03431 | 0.03472 | +3.48 | +3.57 |
| sipp_wife_emp_s1 | Her search | 0.03673 | 0.06788 | 0.06143 | +4.69 | +3.72 |
| sipp_wife_emp_s6 | Her search | 0.05433 | 0.119 | 0.1113 | +6.39 | +5.63 |
| cps_entry_pooled (reported) | Her search | 0.07498 | 0.05575 | 0.02983 | -63.67 | -149.53 |
| cps_entry_black (reported) | Her search | 0.09418 | 0.09887 | 0.03955 | +2.88 | -33.58 |
| cps_entry_white (reported) | Her search | 0.07509 | 0.04711 | 0.02638 | -86.06 | -149.81 |
| cps_entry_p_pooled (reported) | Her search | 0.03193 | 0.04421 | 0.01936 | +34.29 | -35.08 |
| cps_entry_p_black | Her search | 0.04039 | 0.08851 | 0.02697 | +25.95 | -7.23 |
| cps_entry_p_white | Her search | 0.03203 | 0.03583 | 0.01669 | +9.40 | -37.91 |
| cps_wife_exit (reported) | Her exits | 0.02615 | 0.002334 | 0.005238 | -228.69 | -200.81 |
| cps_wife_exit_p | Her exits | 0.01006 | 0.00142 | 0.002762 | -68.70 | -58.03 |
| sipp_his_emp_s3_sep | His search | 0.5863 | 0.578 | 0.5835 | -0.58 | -0.20 |
| sipp_his_emp_s3_nosep (reported) | His search | 0.9828 | 0.9896 | 0.9906 | +16.12 | +18.68 |
| sipp_his_emp_s6_sep | His search | 0.7077 | 0.7972 | 0.8061 | +7.16 | +7.87 |
| sipp_his_emp_s6_nosep (reported) | His search | 0.9718 | 0.9858 | 0.9871 | +19.18 | +21.01 |
| sipp_his_emp_s12_sep | His search | 0.791 | 0.8934 | 0.9101 | +7.73 | +8.99 |
| sipp_his_emp_s12_nosep (reported) | His search | 0.9602 | 0.9845 | 0.9853 | +21.22 | +21.90 |
| psid_es_hh_13_B | His search | -104.7 | -115.1 | -112.8 | -0.23 | -0.18 |
| psid_es_hh_13_W | His search | -128.4 | -88.42 | -91.35 | +1.19 | +1.10 |
| psid_es_w_hrs_13_y05 | Added work | 87.93 | 61.52 | 81.62 | -0.61 | -0.14 |
| psid_es_w_emp_13_y05 | Added work | 0.04163 | 0.01064 | 0.02936 | -1.39 | -0.55 |
| psid_es_w_hrs_13_y617 | Added work | -40.09 | 31.61 | 50.1 | +1.66 | +2.09 |
| psid_es_w_emp_13_y617 | Added work | -0.03919 | 0.0104 | 0.02307 | +2.17 | +2.73 |
| psid_gross_all | Added work | 47.34 | 58.78 | 75.86 | +0.38 | +0.94 |
| psid_offset_all | Added work | -35.98 | -15.65 | -12.76 | +1.48 | +1.69 |
| psid_gross_05 | Added work | 93.71 | 81.63 | 101.4 | -0.29 | +0.18 |
| psid_wemp_none | Employment levels | 0.8088 | 0.9545 | 0.8627 | +26.95 | +9.97 |
| psid_wemp_05 | Employment levels | 0.754 | 0.9618 | 0.8602 | +36.43 | +18.62 |
| psid_wemp_617 | Employment levels | 0.8233 | 0.95 | 0.8318 | +29.20 | +1.96 |
| psid_pt_w | Employment levels | 0.3374 | 0.2082 | 0.2268 | -28.10 | -24.06 |
| psid_pt_h | Employment levels | 0.1056 | 0.08605 | 0.0791 | -9.00 | -12.20 |
| psid_hemp_B (reported) | Employment levels | 0.8821 | 0.999 | 0.999 | +22.47 | +22.47 |
| psid_hemp_W (reported) | Employment levels | 0.9425 | 0.9996 | 0.9995 | +23.04 | +23.01 |
| psid_es_bw_present_13_B | Separation | -0.04031 | -0.01882 | 0 | +1.03 | +1.94 |
| psid_es_bw_present_13_W | Separation | -0.02667 | -0.01952 | 0 | +0.59 | +2.21 |
| psid_sep_rate_B | Separation | 0.03164 | 0.03296 | 0 | +0.95 | -22.88 |
| psid_sep_rate_W | Separation | 0.01517 | 0.01568 | 0 | +0.96 | -28.31 |
| psid_liq_le0_25 | Wealth | 0.5681 | 0.4757 | 0.499 | -12.57 | -9.40 |
| psid_liq_hi_25 | Wealth | 0.03436 | 0.02162 | 0.01469 | -5.50 | -8.49 |
| psid_liq_le0_35 | Wealth | 0.4616 | 0.3396 | 0.3825 | -14.87 | -9.64 |
| psid_liq_hi_35 | Wealth | 0.07746 | 0.08222 | 0.04108 | +1.34 | -10.26 |
| psid_liq_le0_45 | Wealth | 0.381 | 0.08557 | 0.11 | -34.95 | -32.06 |
| psid_liq_hi_45 | Wealth | 0.1772 | 0.3892 | 0.3158 | +35.52 | +23.22 |
| psid_cons_single_all | Consumption | -0.01277 | -0.05836 | -0.06322 | -2.72 | -3.01 |
| psid_cons_wife_alone | Consumption | -0.03073 | -0.06203 | -0.04662 | -1.58 | -0.80 |
| psid_cons_joint_minus_single | Consumption | -0.05853 | -0.06458 | -0.04715 | -0.09 | +0.18 |
| psid_cons_single_black | Consumption | -0.00533 | -0.05227 | -0.05307 | -1.90 | -1.93 |
| psid_cons_single_white | Consumption | -0.005342 | -0.06607 | -0.07314 | -2.69 | -3.00 |

## (B) Still with baseline wife after his displacement (event study, reference e = -2)

Model: the targets' stacked panel (panels.units / stack_rows, events 1984-2021, outcome years to 2021), yearly coefficients with unit and cell effects. PSID: IGE/output/father_displacement.csv (IGE/19). Years 1-3: their mean is the target (psid_es_bw_present_13_B/W, IGE/60's window); years 4-6 reported only.

| e | Pooled model | Pooled PSID | Black model | Black PSID | White model | White PSID |
|---:|---:|---:|---:|---:|---:|---:|
| -3 | -0.005 | -0.024 | -0.006 | -0.025 | -0.004 | -0.020 |
| -1 | -0.001 | +0.012 | +0.003 | +0.029 | -0.002 | +0.002 |
| +0 | -0.018 | -0.013 | -0.011 | -0.013 | -0.016 | -0.011 |
| +1 | -0.029 | -0.027 | -0.028 | -0.037 | -0.018 | -0.017 |
| +2 | -0.030 | -0.030 | -0.015 | -0.043 | -0.022 | -0.018 |
| +3 | -0.029 | -0.037 | -0.014 | -0.053 | -0.018 | -0.022 |
| +4 | -0.029 | -0.044 | -0.017 | -0.058 | -0.013 | -0.030 |
| +5 | -0.031 | -0.049 | -0.011 | -0.077 | -0.013 | -0.028 |
| +6 | -0.039 | -0.050 | -0.026 | -0.074 | -0.014 | -0.030 |

Means: All: model 1-3 -0.029, 4-6 -0.033 vs PSID 1-3 -0.031, 4-6 -0.048; Black: model 1-3 -0.019, 4-6 -0.018 vs PSID 1-3 -0.045, 4-6 -0.070; White: model 1-3 -0.020, 4-6 -0.014 vs PSID 1-3 -0.019, 4-6 -0.029

'All' = pooled over races in both. In the model the separation hazard is sigma_0 + sigma_J only in months in which the husband is non-employed (sigma_0 otherwise).

4.5 minutes.
