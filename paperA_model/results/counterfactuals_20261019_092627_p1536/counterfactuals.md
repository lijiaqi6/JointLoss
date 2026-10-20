# Counterfactuals (k_s2_era1_a20, K = 3)

Consumption: household consumption, mean log change from the 6 months before his displacement to the loss month and to the mean of the 12 months after (married couples). Shares: of married couple-months. ce_cons_pct: consumption-only consumption-equivalent at entry relative to base, percent (not the full-value welfare measure). Same CRN draws in every scenario.

## main model, group all

| scenario | dlog_c_loss_his | dlog_c_12m_his | dlog_c_loss_joint | dlog_c_12m_joint | share_no_earner | share_no_earner_no_credit | ce_cons_pct | his_losses | joint_losses |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| base | -0.05388 | -0.03989 | -0.1535 | -0.1308 | 0.002272 | 4.615e-05 | 0 | 2.493e+04 | 534 |
| i_common_off | -0.05771 | -0.0415 | -0.1632 | -0.1404 | 0.001506 | 4.337e-05 | 1.093 | 2.026e+04 | 37 |
| v_haz | -0.05647 | -0.04181 | -0.1582 | -0.1334 | 0.002085 | 4.528e-05 | 0.8584 | 2.064e+04 | 503 |
| v_sep | -0.05352 | -0.03963 | -0.1519 | -0.1296 | 0.002308 | 4.603e-05 | 0.1568 | 2.524e+04 | 544 |

## main model, group B

| scenario | dlog_c_loss_his | dlog_c_12m_his | dlog_c_loss_joint | dlog_c_12m_joint | share_no_earner | share_no_earner_no_credit | ce_cons_pct | his_losses | joint_losses |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| base | -0.04621 | -0.03333 | -0.1348 | -0.1065 | 0.003003 | 5.043e-05 | 0 | 1.035e+04 | 166 |
| i_common_off | -0.05031 | -0.03521 | -0.1631 | -0.128 | 0.002071 | 4.764e-05 | 1.331 | 8702 | 21 |
| v_haz | -0.04961 | -0.03523 | -0.1481 | -0.1106 | 0.002355 | 4.739e-05 | 2.382 | 6061 | 135 |
| v_sep | -0.04559 | -0.0329 | -0.1309 | -0.104 | 0.003122 | 4.997e-05 | 0.4311 | 1.065e+04 | 176 |

## main model, group W

| scenario | dlog_c_loss_his | dlog_c_12m_his | dlog_c_loss_joint | dlog_c_12m_joint | share_no_earner | share_no_earner_no_credit | ce_cons_pct | his_losses | joint_losses |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| base | -0.05932 | -0.04454 | -0.162 | -0.1418 | 0.001974 | 4.441e-05 | 0 | 1.458e+04 | 368 |
| i_common_off | -0.06328 | -0.04624 | -0.1634 | -0.1567 | 0.001276 | 4.163e-05 | 0.9565 | 1.156e+04 | 16 |
| v_haz | -0.05932 | -0.04454 | -0.162 | -0.1418 | 0.001974 | 4.441e-05 | 0 | 1.458e+04 | 368 |
| v_sep | -0.05932 | -0.04454 | -0.162 | -0.1418 | 0.001974 | 4.441e-05 | 0 | 1.458e+04 | 368 |

7.7 minutes. Not implemented (hooks in the docstring): ii_both_entitled (hook (ii-b)), iii_eitc_vs_transfer (hook (iii)), iv_childcare (hook (iv)).
