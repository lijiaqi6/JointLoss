# Counterfactuals (k_s2_era1_a20, K = 3)

Consumption: household consumption, mean log change from the 6 months before his displacement to the loss month and to the mean of the 12 months after (married couples). Shares: of married couple-months. ce_cons_pct: consumption-only consumption-equivalent at entry relative to base, percent (not the full-value welfare measure). Same CRN draws in every scenario.

## main model, group all

| scenario | dlog_c_loss_his | dlog_c_12m_his | dlog_c_loss_joint | dlog_c_12m_joint | share_no_earner | share_no_earner_no_credit | ce_cons_pct | his_losses | joint_losses |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| base | -0.05385 | -0.03983 | -0.1534 | -0.1306 | 0.002272 | 4.615e-05 | 0 | 2.493e+04 | 534 |
| ii_ui12 | -0.05288 | -0.03892 | -0.1496 | -0.1275 | 0.002272 | 4.689e-05 | 0.07295 | 2.493e+04 | 534 |

## main model, group B

| scenario | dlog_c_loss_his | dlog_c_12m_his | dlog_c_loss_joint | dlog_c_12m_joint | share_no_earner | share_no_earner_no_credit | ce_cons_pct | his_losses | joint_losses |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| base | -0.04622 | -0.03329 | -0.1349 | -0.1063 | 0.003003 | 5.043e-05 | 0 | 1.035e+04 | 166 |
| ii_ui12 | -0.04531 | -0.03241 | -0.1316 | -0.1038 | 0.003004 | 5.043e-05 | 0.08862 | 1.035e+04 | 166 |

## main model, group W

| scenario | dlog_c_loss_his | dlog_c_12m_his | dlog_c_loss_joint | dlog_c_12m_joint | share_no_earner | share_no_earner_no_credit | ce_cons_pct | his_losses | joint_losses |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| base | -0.05927 | -0.04448 | -0.1618 | -0.1416 | 0.001974 | 4.441e-05 | 0 | 1.458e+04 | 368 |
| ii_ui12 | -0.05826 | -0.04354 | -0.1578 | -0.1382 | 0.001974 | 4.545e-05 | 0.06397 | 1.458e+04 | 368 |

1.8 minutes. Not implemented (hooks in the docstring): ii_both_entitled (hook (ii-b)), iii_eitc_vs_transfer (hook (iii)), iv_childcare (hook (iv)).
