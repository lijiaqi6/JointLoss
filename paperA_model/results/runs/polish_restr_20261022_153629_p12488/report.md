# Jacobian

S = change of each moment in weighted units (sqrt of the objective weight) per 10% move of a parameter (value scaling: 10% of |theta|; range scaling: 10% of the bound range, the plan's protocol; z: per unit of the logistic coordinate). Moments in the objective with finite rows: 85 of 97.

| parameter | theta | norm (10% of value) | norm (10% of range) | norm (per z) | top block | share |
|---|---:|---:|---:|---:|---|---:|
| delta_w_B | 0.002942 | 2.85 | 29.02 | 25.60 | Base hazards | 0.93 |
| delta_w_W | 0.002034 | 5.15 | 75.97 | 47.81 | Base hazards | 0.97 |
| delta_h_B | 0.004874 | 3.77 | 23.21 | 31.54 | Base hazards | 0.88 |
| delta_h_W | 0.002799 | 7.30 | 78.18 | 65.94 | Base hazards | 0.96 |
| pi_c0 | 4.274e-05 | 0.81 | 38.12 | 7.97 | Joint loss, monthly | 0.94 |
| pi_c1 | 0.0003671 | 1.11 | 60.64 | 10.93 | Joint loss, monthly | 0.89 |
| p_H | 0.01967 | 2.18 | 54.23 | 10.49 | Base hazards | 0.63 |
| m_H | 14.9 | 2.37 | 4.61 | 11.50 | Joint loss, annual | 0.45 |
| lam_w_B | 0.08661 | 1.44 | 14.79 | 11.64 | Her exits | 0.61 |
| lam_w_W | 0.1561 | 6.11 | 34.83 | 47.81 | Her exits | 0.69 |
| lam_h_B | 0.1236 | 1.61 | 11.57 | 12.88 | His search | 0.53 |
| lam_h_W | 0.3086 | 2.36 | 6.80 | 15.17 | His search | 0.74 |
| pi_up_w | 0.007732 | 12.95 | 99.63 | 106.38 | Employment levels | 0.50 |
| pi_up_h | 0.005206 | 7.10 | 81.13 | 59.09 | Employment levels | 0.41 |
| pi_dn_w | 0.0002605 | 0.35 | 271.69 | 3.53 | Her exits | 0.79 |
| pi_dn_h | 0.01983 | 0.72 | 7.31 | 6.53 | Wage growth | 0.22 |
| d_w | 0.04461 | 0.38 | 16.97 | 3.70 | Her exits | 0.35 |
| d_h | 0.005865 | 0.04 | 14.29 | 0.42 | Her exits | 0.23 |
| phi_F | 0.3699 | 18.29 | 74.18 | 180.72 | Employment levels | 0.77 |
| phi_P | 0.1083 | 8.31 | 115.13 | 277.56 | Employment levels | 0.69 |
| theta_05 | 0.007144 | 0.20 | 42.45 | 95.00 | Employment levels | 0.81 |
| theta_617 | -0.002549 | 0.10 | 57.58 | 127.63 | Employment levels | 0.76 |
| phi_h | 0.1808 | 9.97 | 82.77 | 205.15 | Employment levels | 0.95 |
| F | 0.5999 | 10.70 | 10.70 | 0.01 | Employment levels | 0.70 |
| kappa_S | 0.1003 | 0.62 | 6.23 | 5.62 | Safety net | 0.65 |
| sigma0_B | 0.002796 | 2.53 | 18.12 | 21.79 | Separation | 0.69 |
| sigma0_W | 0.001151 | 3.73 | 64.75 | 35.11 | Separation | 0.41 |
| sigmaJ_B | 0.001124 | 0.13 | 11.20 | 1.25 | Her search | 0.29 |
| eta_up | 0.5539 | 1.44 | 7.78 | 11.71 | Employment levels | 0.62 |
| beta | 0.9957 | 2903.81 | 24.28 | 60.37 | Wealth | 0.79 |

Singular values (value scaling): 2.9e+03, 22.8, 13.4, 8.95, 7.42, 6.63, 5.32, 3.75, 3.02, 2.97, 2.67, 2.43, 2.21, 2.14, 1.87, 1.61, 1.3, 1.08, 0.797, 0.678, 0.501, 0.449, 0.393, 0.255, 0.108, 0.102, 0.0687, 0.0472, 0.0283, 0.0161
Condition number (value scaling): 1.81e+05; (range scaling): 319

Weakest directions, value scaling (smallest singular values, largest loadings):
- sv 0.0161: {'d_h': -0.999, 'pi_dn_h': 0.042, 'theta_05': 0.018, 'theta_617': 0.016}
- sv 0.0283: {'pi_dn_w': 0.901, 'theta_617': 0.3, 'theta_05': 0.296, 'd_w': 0.07}
- sv 0.0472: {'theta_617': 0.893, 'pi_dn_w': -0.349, 'sigmaJ_B': -0.203, 'theta_05': 0.193}
- sv 0.0687: {'sigmaJ_B': -0.935, 'theta_617': -0.232, 'theta_05': 0.204, 'd_w': -0.136}
- sv 0.102: {'d_w': 0.958, 'theta_05': 0.177, 'p_H': 0.123, 'pi_dn_w': -0.096}

Weakest directions, range scaling:
- sv 0.964: {'m_H': 0.982, 'eta_up': 0.112, 'p_H': -0.11, 'delta_h_B': 0.045}
- sv 1.57: {'F': 0.925, 'eta_up': 0.27, 'kappa_S': 0.17, 'pi_dn_h': -0.081}
- sv 2.14: {'eta_up': 0.803, 'pi_dn_h': -0.327, 'kappa_S': -0.314, 'F': -0.198}
- sv 2.69: {'pi_dn_h': -0.839, 'd_h': 0.356, 'eta_up': -0.301, 'lam_w_W': -0.131}
- sv 4.13: {'d_w': 0.782, 'lam_w_W': 0.347, 'sigmaJ_B': 0.289, 'lam_h_W': -0.204}

Near-collinear pairs (|corr| of columns > 0.9):
- none

Parameters with norm < 3 (value scaling): ['delta_w_B', 'pi_c0', 'pi_c1', 'p_H', 'm_H', 'lam_w_B', 'lam_h_B', 'lam_h_W', 'pi_dn_w', 'pi_dn_h', 'd_w', 'd_h', 'theta_05', 'theta_617', 'kappa_S', 'sigma0_B', 'sigmaJ_B', 'eta_up']

Information by block: share of each parameter's sum of squared sensitivities (value scaling), percent; last row = mean over parameters.

| parameter | Employment levels | Base hazards | Her exits | Joint loss, monthly | Her search | His search | Separation | Wealth | Joint loss, annual | Safety net | Wage growth | His earnings | Consumption | Added work | Her earnings |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| delta_w_B | 1 | 93 | 1 | 1 | 1 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| delta_w_W | 0 | 97 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| delta_h_B | 4 | 88 | 0 | 3 | 0 | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| delta_h_W | 1 | 96 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pi_c0 | 0 | 1 | 0 | 94 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| pi_c1 | 0 | 1 | 0 | 89 | 0 | 0 | 0 | 0 | 9 | 0 | 0 | 0 | 0 | 0 | 0 |
| p_H | 1 | 63 | 0 | 8 | 1 | 0 | 0 | 0 | 26 | 0 | 0 | 0 | 0 | 0 | 0 |
| m_H | 1 | 24 | 0 | 26 | 0 | 3 | 0 | 0 | 45 | 0 | 0 | 0 | 0 | 0 | 0 |
| lam_w_B | 4 | 1 | 61 | 4 | 18 | 1 | 0 | 1 | 2 | 0 | 2 | 0 | 0 | 0 | 5 |
| lam_w_W | 6 | 0 | 69 | 0 | 23 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| lam_h_B | 8 | 5 | 0 | 0 | 3 | 53 | 0 | 0 | 2 | 3 | 1 | 21 | 3 | 1 | 0 |
| lam_h_W | 9 | 0 | 1 | 2 | 8 | 74 | 0 | 1 | 0 | 3 | 0 | 1 | 1 | 1 | 0 |
| pi_up_w | 50 | 0 | 27 | 0 | 10 | 0 | 0 | 8 | 0 | 1 | 3 | 0 | 0 | 0 | 0 |
| pi_up_h | 41 | 0 | 41 | 0 | 1 | 0 | 0 | 4 | 0 | 0 | 12 | 0 | 0 | 0 | 0 |
| pi_dn_w | 19 | 1 | 79 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pi_dn_h | 17 | 6 | 19 | 0 | 18 | 0 | 0 | 4 | 2 | 1 | 22 | 6 | 3 | 2 | 0 |
| d_w | 18 | 20 | 35 | 3 | 5 | 0 | 0 | 7 | 7 | 0 | 2 | 0 | 0 | 0 | 0 |
| d_h | 13 | 5 | 23 | 1 | 14 | 0 | 0 | 5 | 4 | 0 | 18 | 8 | 7 | 2 | 0 |
| phi_F | 77 | 0 | 19 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phi_P | 69 | 0 | 14 | 0 | 14 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| theta_05 | 81 | 0 | 14 | 0 | 4 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| theta_617 | 76 | 0 | 11 | 0 | 11 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phi_h | 95 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| F | 70 | 0 | 4 | 0 | 23 | 0 | 0 | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| kappa_S | 25 | 0 | 1 | 1 | 5 | 0 | 0 | 2 | 0 | 65 | 0 | 0 | 0 | 1 | 0 |
| sigma0_B | 14 | 2 | 4 | 0 | 3 | 5 | 69 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| sigma0_W | 28 | 0 | 7 | 0 | 14 | 1 | 41 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| sigmaJ_B | 8 | 18 | 1 | 4 | 29 | 6 | 26 | 2 | 4 | 1 | 0 | 1 | 0 | 0 | 0 |
| eta_up | 62 | 1 | 1 | 1 | 21 | 1 | 0 | 4 | 0 | 4 | 2 | 0 | 1 | 1 | 0 |
| beta | 15 | 0 | 6 | 0 | 1 | 0 | 0 | 79 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| mean | 27.1 | 17.4 | 14.7 | 8.1 | 7.7 | 5.0 | 4.6 | 4.3 | 3.7 | 2.8 | 2.2 | 1.3 | 0.5 | 0.3 | 0.3 |