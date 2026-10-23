# Jacobian

S = change of each moment in weighted units (sqrt of the objective weight) per 10% move of a parameter (value scaling: 10% of |theta|; range scaling: 10% of the bound range, the plan's protocol; z: per unit of the logistic coordinate). Moments in the objective with finite rows: 85 of 97.

| parameter | theta | norm (10% of value) | norm (10% of range) | norm (per z) | top block | share |
|---|---:|---:|---:|---:|---|---:|
| delta_w_B | 0.002985 | 2.85 | 28.61 | 25.56 | Base hazards | 0.94 |
| delta_w_W | 0.002045 | 4.92 | 72.20 | 45.66 | Base hazards | 0.97 |
| delta_h_B | 0.004865 | 3.77 | 23.22 | 31.50 | Base hazards | 0.88 |
| delta_h_W | 0.00279 | 7.34 | 78.91 | 66.37 | Base hazards | 0.96 |
| pi_c0 | 4.217e-05 | 0.77 | 36.65 | 7.56 | Joint loss, monthly | 0.93 |
| pi_c1 | 0.0003502 | 1.08 | 61.43 | 10.57 | Joint loss, monthly | 0.89 |
| p_H | 0.02138 | 2.15 | 49.23 | 11.16 | Base hazards | 0.64 |
| m_H | 14.94 | 2.00 | 3.89 | 9.71 | Joint loss, annual | 0.40 |
| lam_w_B | 0.08816 | 1.21 | 12.22 | 9.79 | Her exits | 0.47 |
| lam_w_W | 0.1575 | 5.93 | 33.50 | 46.33 | Her exits | 0.69 |
| lam_h_B | 0.1202 | 1.45 | 10.71 | 11.61 | His search | 0.57 |
| lam_h_W | 0.3011 | 2.54 | 7.52 | 16.55 | His search | 0.82 |
| pi_up_w | 0.007307 | 13.38 | 108.98 | 110.41 | Employment levels | 0.46 |
| pi_up_h | 0.005124 | 7.35 | 85.34 | 61.16 | Her exits | 0.45 |
| pi_dn_w | 0.0001349 | 0.20 | 299.09 | 2.02 | Her exits | 0.79 |
| pi_dn_h | 0.02036 | 0.70 | 6.83 | 6.25 | Wage growth | 0.27 |
| d_w | 0.09236 | 0.81 | 17.44 | 7.68 | Employment levels | 0.24 |
| d_h | 0.0004255 | 0.00 | 13.98 | 0.03 | Wage growth | 0.21 |
| phi_F | 0.3681 | 18.38 | 74.88 | 182.55 | Employment levels | 0.74 |
| phi_P | 0.1118 | 8.23 | 110.39 | 266.61 | Employment levels | 0.70 |
| theta_05 | 0.02143 | 0.55 | 38.82 | 88.04 | Employment levels | 0.81 |
| theta_617 | 0.007879 | 0.30 | 57.43 | 128.61 | Employment levels | 0.76 |
| phi_h | 0.1781 | 9.20 | 77.48 | 191.92 | Employment levels | 0.95 |
| F | 0.5703 | 9.50 | 10.00 | 4.71 | Employment levels | 0.72 |
| kappa_S | 0.1058 | 0.63 | 5.98 | 5.66 | Safety net | 0.65 |
| sigma0_B | 0.00275 | 2.29 | 16.63 | 19.72 | Separation | 0.78 |
| sigma0_W | 0.001103 | 3.72 | 67.52 | 35.19 | Separation | 0.37 |
| sigmaJ_B | 0.001247 | 0.12 | 10.02 | 1.23 | Separation | 0.34 |
| a_bar | 59.99 | 2.64 | 2.64 | 0.00 | Wealth | 0.95 |
| eta_up | 0.5022 | 1.45 | 8.69 | 12.11 | Employment levels | 0.61 |

Singular values (value scaling): 23.7, 12.6, 8.77, 7.41, 6.39, 5.03, 4.59, 3.73, 2.91, 2.75, 2.62, 2.28, 2.1, 2.06, 1.78, 1.49, 1.19, 1.03, 0.773, 0.629, 0.578, 0.467, 0.434, 0.357, 0.263, 0.232, 0.132, 0.0727, 0.0198, 0.00111
Condition number (value scaling): 2.13e+04; (range scaling): 304

Weakest directions, value scaling (smallest singular values, largest loadings):
- sv 0.00111: {'d_h': 1.0, 'pi_dn_h': -0.003, 'pi_dn_w': 0.001, 'sigmaJ_B': -0.001}
- sv 0.0198: {'pi_dn_w': 0.996, 'theta_05': 0.071, 'theta_617': 0.032, 'lam_w_W': 0.02}
- sv 0.0727: {'sigmaJ_B': -0.998, 'd_w': -0.039, 'pi_dn_h': 0.027, 'p_H': -0.022}
- sv 0.132: {'theta_617': 0.887, 'theta_05': 0.412, 'eta_up': -0.18, 'kappa_S': 0.063}
- sv 0.232: {'theta_05': -0.667, 'eta_up': 0.451, 'theta_617': 0.429, 'd_w': 0.286}

Weakest directions, range scaling:
- sv 1.1: {'m_H': -0.972, 'F': 0.145, 'p_H': 0.098, 'eta_up': 0.094}
- sv 1.55: {'a_bar': 0.889, 'F': -0.346, 'eta_up': -0.246, 'kappa_S': 0.122}
- sv 1.76: {'eta_up': -0.702, 'F': -0.5, 'a_bar': -0.421, 'lam_h_W': -0.153}
- sv 2.48: {'F': -0.682, 'eta_up': 0.492, 'kappa_S': -0.469, 'lam_w_B': -0.181}
- sv 2.71: {'pi_dn_h': -0.875, 'd_h': 0.409, 'lam_h_W': 0.167, 'eta_up': -0.124}

Near-collinear pairs (|corr| of columns > 0.9):
- none

Parameters with norm < 3 (value scaling): ['delta_w_B', 'pi_c0', 'pi_c1', 'p_H', 'm_H', 'lam_w_B', 'lam_h_B', 'lam_h_W', 'pi_dn_w', 'pi_dn_h', 'd_w', 'd_h', 'theta_05', 'theta_617', 'kappa_S', 'sigma0_B', 'sigmaJ_B', 'a_bar', 'eta_up']

Information by block: share of each parameter's sum of squared sensitivities (value scaling), percent; last row = mean over parameters.

| parameter | Employment levels | Base hazards | Her exits | Joint loss, monthly | Wealth | His search | Her search | Separation | Joint loss, annual | Safety net | Wage growth | His earnings | Consumption | Her earnings | Added work |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| delta_w_B | 1 | 94 | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| delta_w_W | 1 | 97 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| delta_h_B | 3 | 88 | 0 | 4 | 0 | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| delta_h_W | 1 | 96 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pi_c0 | 0 | 1 | 0 | 93 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| pi_c1 | 0 | 1 | 0 | 89 | 0 | 0 | 0 | 0 | 10 | 0 | 0 | 0 | 0 | 0 | 0 |
| p_H | 2 | 64 | 0 | 7 | 0 | 0 | 1 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 |
| m_H | 1 | 24 | 0 | 27 | 0 | 5 | 2 | 0 | 40 | 0 | 0 | 0 | 0 | 0 | 1 |
| lam_w_B | 10 | 1 | 47 | 3 | 2 | 2 | 17 | 0 | 3 | 2 | 2 | 0 | 1 | 11 | 1 |
| lam_w_W | 6 | 0 | 69 | 0 | 0 | 0 | 23 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |
| lam_h_B | 7 | 6 | 0 | 1 | 0 | 57 | 0 | 0 | 0 | 4 | 1 | 19 | 4 | 0 | 1 |
| lam_h_W | 9 | 0 | 1 | 0 | 0 | 82 | 3 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 1 |
| pi_up_w | 46 | 1 | 33 | 0 | 9 | 0 | 7 | 0 | 0 | 1 | 3 | 0 | 0 | 0 | 0 |
| pi_up_h | 39 | 0 | 45 | 0 | 4 | 0 | 1 | 0 | 0 | 0 | 11 | 0 | 0 | 0 | 0 |
| pi_dn_w | 18 | 1 | 79 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pi_dn_h | 17 | 8 | 12 | 2 | 8 | 0 | 9 | 0 | 2 | 1 | 27 | 6 | 4 | 0 | 3 |
| d_w | 24 | 19 | 23 | 2 | 12 | 0 | 8 | 0 | 4 | 1 | 4 | 0 | 0 | 3 | 0 |
| d_h | 14 | 9 | 14 | 2 | 11 | 4 | 6 | 0 | 2 | 0 | 21 | 8 | 7 | 0 | 3 |
| phi_F | 74 | 0 | 24 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phi_P | 70 | 0 | 15 | 0 | 1 | 0 | 12 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| theta_05 | 81 | 0 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| theta_617 | 76 | 0 | 14 | 0 | 1 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phi_h | 95 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| F | 72 | 0 | 5 | 0 | 2 | 0 | 17 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| kappa_S | 19 | 0 | 6 | 1 | 7 | 0 | 2 | 0 | 0 | 65 | 0 | 0 | 0 | 0 | 0 |
| sigma0_B | 9 | 2 | 0 | 0 | 1 | 4 | 3 | 78 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| sigma0_W | 29 | 0 | 15 | 0 | 9 | 1 | 8 | 37 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| sigmaJ_B | 10 | 21 | 1 | 7 | 2 | 8 | 11 | 34 | 4 | 1 | 1 | 1 | 0 | 0 | 0 |
| a_bar | 1 | 0 | 0 | 1 | 95 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| eta_up | 61 | 0 | 6 | 1 | 4 | 1 | 17 | 0 | 0 | 7 | 1 | 0 | 0 | 0 | 1 |
| mean | 26.5 | 17.8 | 14.3 | 8.1 | 5.7 | 5.6 | 5.3 | 5.0 | 3.3 | 2.9 | 2.6 | 1.2 | 0.6 | 0.6 | 0.5 |