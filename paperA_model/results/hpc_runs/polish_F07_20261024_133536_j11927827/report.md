# Jacobian

S = change of each moment in weighted units (sqrt of the objective weight) per 10% move of a parameter (value scaling: 10% of |theta|; range scaling: 10% of the bound range, the plan's protocol; z: per unit of the logistic coordinate). Moments in the objective with finite rows: 85 of 97.

| parameter | theta | norm (10% of value) | norm (10% of range) | norm (per z) | top block | share |
|---|---:|---:|---:|---:|---|---:|
| delta_w_B | 0.003381 | 2.87 | 25.46 | 25.40 | Base hazards | 0.90 |
| delta_w_W | 0.002202 | 5.77 | 78.58 | 53.25 | Base hazards | 0.95 |
| delta_h_B | 0.00482 | 3.79 | 23.59 | 31.77 | Base hazards | 0.89 |
| delta_h_W | 0.002754 | 7.80 | 84.90 | 70.57 | Base hazards | 0.96 |
| pi_c0 | 3.714e-05 | 0.67 | 36.02 | 6.57 | Joint loss, monthly | 0.93 |
| pi_c1 | 0.0003881 | 1.19 | 61.17 | 11.64 | Joint loss, monthly | 0.89 |
| p_H | 0.02348 | 2.20 | 45.87 | 12.27 | Base hazards | 0.63 |
| m_H | 21.71 | 1.88 | 2.52 | 5.14 | Joint loss, annual | 0.34 |
| lam_w_B | 0.1381 | 1.32 | 8.50 | 10.48 | Her exits | 0.40 |
| lam_w_W | 0.1843 | 6.00 | 28.97 | 45.62 | Her search | 0.54 |
| lam_h_B | 0.1391 | 1.60 | 10.21 | 12.67 | His search | 0.64 |
| lam_h_W | 0.3234 | 2.49 | 6.85 | 15.63 | His search | 0.78 |
| pi_up_w | 0.008212 | 11.05 | 80.08 | 90.34 | Employment levels | 0.48 |
| pi_up_h | 0.005612 | 5.15 | 54.65 | 42.92 | Employment levels | 0.48 |
| pi_dn_w | 0.002207 | 2.39 | 216.59 | 23.64 | Her exits | 0.77 |
| pi_dn_h | 0.01574 | 0.44 | 5.63 | 4.08 | Wage growth | 0.40 |
| d_w | 0.2507 | 2.88 | 22.95 | 25.17 | Base hazards | 0.33 |
| d_h | 0.09531 | 0.66 | 13.94 | 6.32 | Wage growth | 0.19 |
| phi_F | 0.3423 | 15.00 | 65.73 | 161.83 | Employment levels | 0.79 |
| phi_P | 0.09512 | 6.24 | 98.40 | 235.52 | Employment levels | 0.63 |
| theta_05 | -0.007899 | 0.18 | 33.69 | 74.28 | Employment levels | 0.78 |
| theta_617 | -0.0328 | 0.95 | 43.47 | 93.23 | Employment levels | 0.61 |
| phi_h | 0.1684 | 8.28 | 73.74 | 182.16 | Employment levels | 0.98 |
| kappa_S | 0.17 | 1.28 | 7.54 | 10.65 | Safety net | 0.82 |
| sigma0_B | 0.003001 | 2.74 | 18.24 | 23.26 | Separation | 0.79 |
| sigma0_W | 0.001487 | 4.17 | 56.13 | 38.64 | Separation | 0.49 |
| sigmaJ_B | 0.0009431 | 0.11 | 11.47 | 1.07 | Separation | 0.22 |
| eta_up | 0.8192 | 2.26 | 8.27 | 16.42 | Her search | 0.46 |
| g_age | 0.02107 | 2.10 | 19.97 | 18.83 | Her search | 0.28 |
| beta | 0.9944 | 2323.88 | 19.45 | 45.96 | Wealth | 0.69 |

Singular values (value scaling): 2.32e+03, 17.4, 9.4, 8.19, 7.39, 6.04, 5.73, 3.8, 3.18, 3.04, 2.76, 2.67, 2.46, 2.19, 1.83, 1.42, 1.18, 1.05, 1.01, 0.902, 0.77, 0.592, 0.553, 0.517, 0.481, 0.41, 0.277, 0.175, 0.0811, 0.0482
Condition number (value scaling): 4.82e+04; (range scaling): 209

Weakest directions, value scaling (smallest singular values, largest loadings):
- sv 0.0482: {'sigmaJ_B': 0.99, 'theta_05': 0.117, 'pi_dn_w': 0.055, 'p_H': 0.036}
- sv 0.0811: {'theta_05': -0.983, 'sigmaJ_B': 0.121, 'pi_dn_w': -0.091, 'g_age': -0.066}
- sv 0.175: {'pi_dn_h': -0.723, 'd_h': 0.595, 'pi_c0': 0.206, 'eta_up': 0.195}
- sv 0.277: {'pi_dn_w': -0.659, 'eta_up': -0.513, 'pi_dn_h': -0.313, 'phi_P': -0.244}
- sv 0.41: {'theta_617': -0.584, 'eta_up': -0.453, 'pi_dn_w': 0.428, 'pi_dn_h': -0.233}

Weakest directions, range scaling:
- sv 1.13: {'m_H': -0.994, 'p_H': 0.075, 'lam_h_B': -0.048, 'sigmaJ_B': 0.023}
- sv 1.34: {'eta_up': 0.957, 'kappa_S': -0.137, 'pi_dn_h': -0.137, 'phi_F': 0.108}
- sv 2.65: {'pi_dn_h': 0.875, 'd_h': -0.345, 'lam_h_W': -0.243, 'eta_up': 0.154}
- sv 4.09: {'lam_h_W': -0.597, 'lam_h_B': 0.486, 'sigmaJ_B': -0.472, 'd_h': 0.204}
- sv 4.28: {'lam_h_W': -0.584, 'sigmaJ_B': 0.514, 'lam_w_W': 0.494, 'pi_dn_h': -0.174}

Near-collinear pairs (|corr| of columns > 0.9):
- none

Parameters with norm < 3 (value scaling): ['delta_w_B', 'pi_c0', 'pi_c1', 'p_H', 'm_H', 'lam_w_B', 'lam_h_B', 'lam_h_W', 'pi_dn_w', 'pi_dn_h', 'd_w', 'd_h', 'theta_05', 'theta_617', 'kappa_S', 'sigma0_B', 'sigmaJ_B', 'eta_up', 'g_age']

Information by block: share of each parameter's sum of squared sensitivities (value scaling), percent; last row = mean over parameters.

| parameter | Employment levels | Base hazards | Her search | Her exits | Joint loss, monthly | His search | Separation | Wealth | Wage growth | Safety net | Joint loss, annual | His earnings | Consumption | Added work | Her earnings |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| delta_w_B | 3 | 90 | 1 | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 2 | 0 | 0 | 0 | 0 |
| delta_w_W | 2 | 95 | 0 | 2 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| delta_h_B | 4 | 89 | 0 | 0 | 2 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| delta_h_W | 1 | 96 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pi_c0 | 0 | 1 | 0 | 0 | 93 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 |
| pi_c1 | 0 | 1 | 0 | 0 | 89 | 0 | 0 | 0 | 0 | 0 | 10 | 0 | 0 | 0 | 0 |
| p_H | 4 | 63 | 0 | 1 | 8 | 2 | 0 | 1 | 0 | 1 | 21 | 0 | 0 | 0 | 0 |
| m_H | 2 | 16 | 9 | 0 | 19 | 16 | 0 | 2 | 1 | 1 | 34 | 0 | 0 | 0 | 0 |
| lam_w_B | 7 | 3 | 34 | 40 | 3 | 0 | 0 | 1 | 2 | 1 | 1 | 0 | 0 | 2 | 6 |
| lam_w_W | 3 | 1 | 54 | 40 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| lam_h_B | 5 | 6 | 1 | 0 | 2 | 64 | 0 | 0 | 3 | 2 | 1 | 13 | 2 | 0 | 0 |
| lam_h_W | 9 | 1 | 7 | 0 | 1 | 78 | 0 | 0 | 1 | 2 | 0 | 1 | 0 | 0 | 0 |
| pi_up_w | 48 | 2 | 21 | 15 | 0 | 0 | 0 | 7 | 5 | 2 | 0 | 0 | 0 | 0 | 0 |
| pi_up_h | 48 | 1 | 1 | 25 | 0 | 0 | 0 | 4 | 20 | 0 | 0 | 0 | 0 | 0 | 0 |
| pi_dn_w | 17 | 3 | 1 | 77 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| pi_dn_h | 12 | 1 | 11 | 7 | 3 | 0 | 0 | 3 | 40 | 1 | 3 | 6 | 11 | 1 | 0 |
| d_w | 11 | 33 | 12 | 12 | 13 | 0 | 0 | 3 | 2 | 0 | 11 | 0 | 1 | 0 | 1 |
| d_h | 12 | 14 | 11 | 7 | 5 | 1 | 0 | 6 | 19 | 0 | 6 | 10 | 10 | 1 | 0 |
| phi_F | 79 | 1 | 8 | 10 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| phi_P | 63 | 1 | 21 | 11 | 0 | 0 | 0 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| theta_05 | 78 | 0 | 6 | 11 | 0 | 0 | 0 | 1 | 2 | 0 | 0 | 0 | 0 | 1 | 0 |
| theta_617 | 61 | 1 | 23 | 10 | 0 | 0 | 0 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| phi_h | 98 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| kappa_S | 9 | 0 | 2 | 2 | 3 | 0 | 0 | 1 | 0 | 82 | 0 | 0 | 0 | 0 | 0 |
| sigma0_B | 7 | 1 | 3 | 1 | 0 | 6 | 79 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| sigma0_W | 17 | 1 | 19 | 6 | 0 | 1 | 49 | 6 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| sigmaJ_B | 8 | 22 | 15 | 1 | 5 | 21 | 22 | 1 | 1 | 1 | 3 | 0 | 0 | 0 | 0 |
| eta_up | 42 | 1 | 46 | 1 | 1 | 0 | 0 | 3 | 3 | 2 | 1 | 0 | 0 | 0 | 0 |
| g_age | 25 | 2 | 28 | 3 | 2 | 0 | 0 | 25 | 13 | 1 | 0 | 0 | 0 | 0 | 0 |
| beta | 18 | 0 | 3 | 8 | 0 | 0 | 0 | 69 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| mean | 23.1 | 18.2 | 11.3 | 9.8 | 8.4 | 6.5 | 5.0 | 4.6 | 4.1 | 3.4 | 3.3 | 1.0 | 0.9 | 0.3 | 0.3 |