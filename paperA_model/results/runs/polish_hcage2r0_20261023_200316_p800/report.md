# Jacobian

S = change of each moment in weighted units (sqrt of the objective weight) per 10% move of a parameter (value scaling: 10% of |theta|; range scaling: 10% of the bound range, the plan's protocol; z: per unit of the logistic coordinate). Moments in the objective with finite rows: 85 of 97.

| parameter | theta | norm (10% of value) | norm (10% of range) | norm (per z) | top block | share |
|---|---:|---:|---:|---:|---|---:|
| delta_w_B | 0.002966 | 2.79 | 28.20 | 25.06 | Base hazards | 0.95 |
| delta_w_W | 0.002051 | 5.20 | 76.11 | 48.27 | Base hazards | 0.97 |
| delta_h_B | 0.004883 | 3.81 | 23.37 | 31.81 | Base hazards | 0.89 |
| delta_h_W | 0.002779 | 7.46 | 80.49 | 67.46 | Base hazards | 0.96 |
| pi_c0 | 4.35e-05 | 0.88 | 40.42 | 8.60 | Joint loss, monthly | 0.94 |
| pi_c1 | 0.000383 | 1.16 | 60.66 | 11.40 | Joint loss, monthly | 0.89 |
| p_H | 0.01928 | 2.14 | 54.38 | 10.10 | Base hazards | 0.63 |
| m_H | 14.66 | 2.56 | 5.07 | 12.64 | Joint loss, annual | 0.47 |
| lam_w_B | 0.07863 | 1.10 | 12.49 | 8.89 | Her exits | 0.59 |
| lam_w_W | 0.1572 | 6.03 | 34.14 | 47.13 | Her exits | 0.70 |
| lam_h_B | 0.123 | 1.66 | 11.99 | 13.29 | His search | 0.59 |
| lam_h_W | 0.325 | 2.24 | 6.14 | 14.03 | His search | 0.81 |
| pi_up_w | 0.008178 | 11.28 | 82.06 | 92.23 | Employment levels | 0.54 |
| pi_up_h | 0.005475 | 5.28 | 57.36 | 43.95 | Employment levels | 0.40 |
| pi_dn_w | 0.0006742 | 0.86 | 255.24 | 8.57 | Her exits | 0.79 |
| pi_dn_h | 0.02163 | 0.76 | 7.00 | 6.76 | Wage growth | 0.48 |
| d_w | 0.02283 | 0.20 | 17.39 | 1.96 | Her exits | 0.30 |
| d_h | 0.001679 | 0.01 | 12.54 | 0.11 | Her exits | 0.22 |
| phi_F | 0.3594 | 17.68 | 73.81 | 180.59 | Employment levels | 0.79 |
| phi_P | 0.1052 | 7.67 | 109.29 | 263.04 | Employment levels | 0.75 |
| theta_05 | -0.00038 | 0.01 | 40.75 | 90.51 | Employment levels | 0.81 |
| theta_617 | -0.01865 | 0.66 | 53.33 | 116.21 | Employment levels | 0.79 |
| phi_h | 0.1697 | 8.56 | 75.63 | 186.90 | Employment levels | 0.97 |
| F | 0.5999 | 11.47 | 11.47 | 0.01 | Employment levels | 0.72 |
| kappa_S | 0.1259 | 0.93 | 7.40 | 8.14 | Safety net | 0.69 |
| sigma0_B | 0.002885 | 2.58 | 17.89 | 22.08 | Separation | 0.73 |
| sigma0_W | 0.001361 | 3.95 | 58.04 | 36.80 | Separation | 0.48 |
| sigmaJ_B | 0.001253 | 0.14 | 11.06 | 1.37 | Her search | 0.26 |
| eta_up | 0.8594 | 2.45 | 8.57 | 17.51 | Employment levels | 0.68 |
| g_age | 0.02873 | 2.43 | 16.91 | 20.81 | Employment levels | 0.40 |
| beta | 0.9949 | 2550.63 | 21.34 | 52.38 | Wealth | 0.68 |

Singular values (value scaling): 2.55e+03, 20, 13.3, 8.2, 7.41, 6.29, 5.4, 3.77, 3.06, 2.9, 2.71, 2.52, 2.39, 2.13, 1.84, 1.58, 1.21, 1.17, 0.879, 0.698, 0.653, 0.632, 0.558, 0.515, 0.329, 0.298, 0.0932, 0.0819, 0.0619, 0.00508, 0.00428
Condition number (value scaling): 5.95e+05; (range scaling): 234

Weakest directions, value scaling (smallest singular values, largest loadings):
- sv 0.00428: {'theta_05': -0.711, 'd_h': 0.703, 'sigmaJ_B': 0.008, 'pi_dn_w': -0.008}
- sv 0.00508: {'d_h': 0.711, 'theta_05': 0.703, 'sigmaJ_B': 0.016, 'pi_dn_w': 0.012}
- sv 0.0619: {'d_w': 0.872, 'sigmaJ_B': 0.468, 'pi_dn_w': 0.14, 'p_H': 0.026}
- sv 0.0819: {'sigmaJ_B': 0.696, 'pi_dn_w': 0.535, 'd_w': -0.459, 'kappa_S': -0.06}
- sv 0.0932: {'pi_dn_w': -0.817, 'sigmaJ_B': 0.541, 'd_w': -0.16, 'lam_w_W': -0.071}

Weakest directions, range scaling:
- sv 1.2: {'m_H': -0.936, 'eta_up': -0.293, 'p_H': 0.117, 'F': -0.09}
- sv 1.54: {'F': 0.856, 'eta_up': 0.435, 'm_H': -0.209, 'kappa_S': 0.09}
- sv 2.08: {'eta_up': 0.788, 'F': -0.403, 'kappa_S': -0.287, 'm_H': -0.229}
- sv 3.38: {'pi_dn_h': 0.692, 'd_h': -0.46, 'lam_h_W': -0.371, 'g_age': 0.239}
- sv 4.33: {'g_age': -0.654, 'lam_h_W': -0.454, 'kappa_S': -0.317, 'beta': 0.219}

Near-collinear pairs (|corr| of columns > 0.9):
- none

Parameters with norm < 3 (value scaling): ['delta_w_B', 'pi_c0', 'pi_c1', 'p_H', 'm_H', 'lam_w_B', 'lam_h_B', 'lam_h_W', 'pi_dn_w', 'pi_dn_h', 'd_w', 'd_h', 'theta_05', 'theta_617', 'kappa_S', 'sigma0_B', 'sigmaJ_B', 'eta_up', 'g_age']

Information by block: share of each parameter's sum of squared sensitivities (value scaling), percent; last row = mean over parameters.

| parameter | Employment levels | Base hazards | Her exits | Joint loss, monthly | Her search | His search | Wealth | Separation | Wage growth | Joint loss, annual | Safety net | His earnings | Consumption | Added work | Her earnings |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| delta_w_B | 1 | 95 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| delta_w_W | 0 | 97 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| delta_h_B | 3 | 89 | 0 | 3 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| delta_h_W | 1 | 96 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pi_c0 | 0 | 1 | 0 | 94 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 |
| pi_c1 | 0 | 1 | 0 | 89 | 0 | 0 | 0 | 0 | 0 | 9 | 0 | 0 | 0 | 0 | 0 |
| p_H | 1 | 63 | 0 | 8 | 2 | 1 | 0 | 0 | 0 | 26 | 0 | 0 | 0 | 0 | 0 |
| m_H | 0 | 19 | 0 | 29 | 2 | 2 | 0 | 0 | 0 | 47 | 0 | 0 | 0 | 0 | 0 |
| lam_w_B | 10 | 1 | 59 | 1 | 14 | 0 | 4 | 0 | 1 | 2 | 1 | 0 | 1 | 1 | 6 |
| lam_w_W | 5 | 0 | 70 | 0 | 23 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| lam_h_B | 7 | 4 | 0 | 1 | 1 | 59 | 0 | 0 | 1 | 0 | 5 | 16 | 4 | 1 | 0 |
| lam_h_W | 10 | 0 | 1 | 0 | 3 | 81 | 1 | 0 | 1 | 0 | 1 | 1 | 1 | 0 | 0 |
| pi_up_w | 54 | 0 | 26 | 0 | 6 | 0 | 6 | 0 | 4 | 0 | 2 | 0 | 0 | 0 | 0 |
| pi_up_h | 40 | 0 | 37 | 0 | 0 | 0 | 5 | 0 | 16 | 0 | 0 | 0 | 0 | 0 | 0 |
| pi_dn_w | 19 | 1 | 79 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pi_dn_h | 13 | 1 | 11 | 4 | 3 | 0 | 3 | 0 | 48 | 0 | 0 | 8 | 6 | 2 | 0 |
| d_w | 18 | 22 | 30 | 4 | 8 | 0 | 7 | 0 | 4 | 5 | 0 | 0 | 1 | 1 | 1 |
| d_h | 16 | 7 | 22 | 3 | 2 | 1 | 7 | 0 | 19 | 2 | 1 | 9 | 9 | 2 | 0 |
| phi_F | 79 | 0 | 18 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| phi_P | 75 | 0 | 9 | 0 | 13 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| theta_05 | 81 | 0 | 13 | 0 | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| theta_617 | 79 | 0 | 7 | 0 | 11 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| phi_h | 97 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| F | 72 | 0 | 5 | 0 | 18 | 0 | 2 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 |
| kappa_S | 21 | 0 | 2 | 2 | 3 | 0 | 1 | 0 | 1 | 0 | 69 | 0 | 0 | 1 | 0 |
| sigma0_B | 14 | 1 | 0 | 0 | 4 | 5 | 0 | 73 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| sigma0_W | 26 | 0 | 6 | 0 | 11 | 1 | 8 | 48 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| sigmaJ_B | 9 | 20 | 0 | 5 | 26 | 7 | 1 | 24 | 1 | 6 | 1 | 0 | 0 | 1 | 0 |
| eta_up | 68 | 0 | 0 | 0 | 19 | 0 | 4 | 0 | 2 | 0 | 5 | 0 | 0 | 1 | 0 |
| g_age | 40 | 0 | 4 | 1 | 14 | 0 | 27 | 0 | 10 | 0 | 2 | 0 | 0 | 1 | 0 |
| beta | 22 | 0 | 7 | 0 | 2 | 0 | 68 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| mean | 28.4 | 16.8 | 13.3 | 8.0 | 6.2 | 5.1 | 4.8 | 4.7 | 3.6 | 3.4 | 3.1 | 1.1 | 0.7 | 0.5 | 0.3 |