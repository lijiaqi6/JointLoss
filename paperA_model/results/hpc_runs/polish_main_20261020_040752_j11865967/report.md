# Jacobian

S = change of each moment in weighted units (sqrt of the objective weight) per 10% move of a parameter (value scaling: 10% of |theta|; range scaling: 10% of the bound range, the plan's protocol; z: per unit of the logistic coordinate). Moments in the objective with finite rows: 85 of 97.

| parameter | theta | norm (10% of value) | norm (10% of range) | norm (per z) | top block | share |
|---|---:|---:|---:|---:|---|---:|
| delta_w_B | 0.002984 | 2.88 | 28.90 | 25.82 | Base hazards | 0.94 |
| delta_w_W | 0.002044 | 4.98 | 73.10 | 46.22 | Base hazards | 0.97 |
| delta_h_B | 0.004864 | 3.74 | 23.09 | 31.32 | Base hazards | 0.90 |
| delta_h_W | 0.00279 | 7.39 | 79.41 | 66.78 | Base hazards | 0.96 |
| pi_c0 | 4.214e-05 | 0.78 | 37.21 | 7.68 | Joint loss, monthly | 0.94 |
| pi_c1 | 0.0003499 | 1.06 | 60.50 | 10.40 | Joint loss, monthly | 0.89 |
| p_H | 0.02141 | 2.15 | 49.28 | 11.20 | Base hazards | 0.64 |
| m_H | 14.93 | 2.05 | 3.99 | 9.95 | Joint loss, annual | 0.36 |
| lam_w_B | 0.08806 | 1.23 | 12.42 | 9.94 | Her exits | 0.48 |
| lam_w_W | 0.1575 | 6.19 | 34.94 | 48.33 | Her exits | 0.68 |
| lam_h_B | 0.1201 | 1.42 | 10.49 | 11.38 | His search | 0.52 |
| lam_h_W | 0.301 | 2.71 | 8.01 | 17.63 | His search | 0.83 |
| pi_up_w | 0.007308 | 13.61 | 110.84 | 112.32 | Employment levels | 0.45 |
| pi_up_h | 0.005126 | 7.34 | 85.18 | 61.07 | Her exits | 0.43 |
| pi_dn_w | 0.0001385 | 0.20 | 294.48 | 2.04 | Her exits | 0.80 |
| pi_dn_h | 0.02036 | 0.67 | 6.58 | 6.01 | Wage growth | 0.28 |
| d_w | 0.09253 | 0.84 | 18.20 | 8.03 | Her exits | 0.25 |
| d_h | 0.0003391 | 0.00 | 12.74 | 0.02 | Wage growth | 0.19 |
| phi_F | 0.3681 | 18.48 | 75.31 | 183.59 | Employment levels | 0.73 |
| phi_P | 0.1119 | 8.15 | 109.21 | 263.78 | Employment levels | 0.70 |
| theta_05 | 0.02163 | 0.55 | 38.14 | 86.50 | Employment levels | 0.81 |
| theta_617 | 0.007991 | 0.30 | 56.01 | 125.44 | Employment levels | 0.76 |
| phi_h | 0.1781 | 9.01 | 75.88 | 187.95 | Employment levels | 0.94 |
| F | 0.5694 | 9.57 | 10.08 | 4.88 | Employment levels | 0.69 |
| kappa_S | 0.1056 | 0.70 | 6.64 | 6.27 | Safety net | 0.63 |
| sigma0_B | 0.00275 | 2.28 | 16.56 | 19.65 | Separation | 0.79 |
| sigma0_W | 0.001103 | 3.76 | 68.21 | 35.53 | Separation | 0.37 |
| sigmaJ_B | 0.001247 | 0.10 | 7.66 | 0.94 | Separation | 0.37 |
| sigmaJ_W | 0.0007081 | 0.04 | 6.31 | 0.44 | Separation | 0.33 |
| a_bar | 59.99 | 3.01 | 3.01 | 0.00 | Wealth | 0.98 |
| eta_up | 0.5011 | 1.55 | 9.26 | 12.88 | Employment levels | 0.57 |

Singular values (value scaling): 23.9, 12.6, 8.55, 7.44, 6.5, 5.07, 4.67, 3.71, 2.97, 2.84, 2.75, 2.39, 2.1, 2.05, 1.92, 1.58, 1.19, 0.993, 0.831, 0.682, 0.644, 0.456, 0.43, 0.364, 0.288, 0.245, 0.143, 0.0526, 0.0242, 0.0178, 0.000769
Condition number (value scaling): 3.11e+04; (range scaling): 300

Weakest directions, value scaling (smallest singular values, largest loadings):
- sv 0.000769: {'d_h': -1.0, 'pi_dn_w': -0.003, 'pi_dn_h': 0.002, 'sigmaJ_W': -0.002}
- sv 0.0178: {'pi_dn_w': 0.995, 'theta_05': 0.06, 'sigmaJ_W': -0.046, 'theta_617': 0.045}
- sv 0.0242: {'sigmaJ_W': 0.984, 'sigmaJ_B': -0.172, 'pi_dn_w': 0.044, 'p_H': 0.014}
- sv 0.0526: {'sigmaJ_B': -0.984, 'sigmaJ_W': -0.171, 'd_w': -0.036, 'theta_617': 0.022}
- sv 0.143: {'theta_617': -0.966, 'theta_05': -0.241, 'pi_dn_w': 0.059, 'kappa_S': 0.054}

Weakest directions, range scaling:
- sv 1.1: {'m_H': 0.974, 'a_bar': -0.108, 'p_H': -0.09, 'pi_dn_h': -0.087}
- sv 1.79: {'a_bar': -0.819, 'F': 0.515, 'pi_dn_h': -0.186, 'eta_up': 0.107}
- sv 2.06: {'F': 0.612, 'kappa_S': 0.524, 'a_bar': 0.376, 'eta_up': -0.355}
- sv 2.28: {'pi_dn_h': -0.741, 'd_h': 0.394, 'eta_up': 0.378, 'a_bar': 0.274}
- sv 2.54: {'eta_up': 0.69, 'F': 0.438, 'pi_dn_h': 0.368, 'sigmaJ_W': -0.273}

Near-collinear pairs (|corr| of columns > 0.9):
- none

Parameters with norm < 3 (value scaling): ['delta_w_B', 'pi_c0', 'pi_c1', 'p_H', 'm_H', 'lam_w_B', 'lam_h_B', 'lam_h_W', 'pi_dn_w', 'pi_dn_h', 'd_w', 'd_h', 'theta_05', 'theta_617', 'kappa_S', 'sigma0_B', 'sigmaJ_B', 'sigmaJ_W', 'eta_up']