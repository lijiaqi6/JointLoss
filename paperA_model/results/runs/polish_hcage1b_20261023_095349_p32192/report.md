# Jacobian

S = change of each moment in weighted units (sqrt of the objective weight) per 10% move of a parameter (value scaling: 10% of |theta|; range scaling: 10% of the bound range, the plan's protocol; z: per unit of the logistic coordinate). Moments in the objective with finite rows: 85 of 97.

| parameter | theta | norm (10% of value) | norm (10% of range) | norm (per z) | top block | share |
|---|---:|---:|---:|---:|---|---:|
| delta_w_B | 0.002959 | 2.80 | 28.43 | 25.21 | Base hazards | 0.94 |
| delta_w_W | 0.002049 | 5.22 | 76.40 | 48.41 | Base hazards | 0.97 |
| delta_h_B | 0.004878 | 3.81 | 23.43 | 31.86 | Base hazards | 0.89 |
| delta_h_W | 0.002778 | 7.46 | 80.54 | 67.49 | Base hazards | 0.96 |
| pi_c0 | 4.346e-05 | 0.87 | 40.11 | 8.53 | Joint loss, monthly | 0.94 |
| pi_c1 | 0.0003825 | 1.16 | 60.64 | 11.38 | Joint loss, monthly | 0.89 |
| p_H | 0.0193 | 2.16 | 54.82 | 10.21 | Base hazards | 0.64 |
| m_H | 14.68 | 2.47 | 4.88 | 12.16 | Joint loss, annual | 0.44 |
| lam_w_B | 0.07938 | 1.14 | 12.76 | 9.17 | Her exits | 0.53 |
| lam_w_W | 0.1573 | 5.98 | 33.82 | 46.72 | Her exits | 0.69 |
| lam_h_B | 0.1231 | 1.62 | 11.74 | 13.03 | His search | 0.60 |
| lam_h_W | 0.325 | 2.17 | 5.93 | 13.56 | His search | 0.78 |
| pi_up_w | 0.008171 | 11.20 | 81.54 | 91.57 | Employment levels | 0.55 |
| pi_up_h | 0.005444 | 5.21 | 56.89 | 43.34 | Employment levels | 0.40 |
| pi_dn_w | 0.000654 | 0.84 | 257.72 | 8.40 | Her exits | 0.80 |
| pi_dn_h | 0.02142 | 0.75 | 7.02 | 6.71 | Wage growth | 0.41 |
| d_w | 0.0193 | 0.16 | 16.38 | 1.57 | Her exits | 0.25 |
| d_h | 0.0002468 | 0.00 | 12.29 | 0.02 | Wage growth | 0.21 |
| phi_F | 0.3599 | 17.52 | 73.01 | 178.60 | Employment levels | 0.81 |
| phi_P | 0.105 | 7.62 | 108.78 | 261.80 | Employment levels | 0.76 |
| theta_05 | -0.0006428 | 0.02 | 40.96 | 90.97 | Employment levels | 0.81 |
| theta_617 | -0.01806 | 0.64 | 53.06 | 115.71 | Employment levels | 0.79 |
| phi_h | 0.1705 | 8.64 | 75.97 | 187.80 | Employment levels | 0.97 |
| F | 0.5999 | 11.40 | 11.40 | 0.01 | Employment levels | 0.74 |
| kappa_S | 0.1226 | 0.88 | 7.21 | 7.75 | Safety net | 0.72 |
| sigma0_B | 0.002889 | 2.54 | 17.60 | 21.75 | Separation | 0.75 |
| sigma0_W | 0.001347 | 3.91 | 58.11 | 36.50 | Separation | 0.49 |
| sigmaJ_B | 0.001345 | 0.15 | 11.37 | 1.51 | Her search | 0.24 |
| eta_up | 0.8591 | 2.34 | 8.17 | 16.70 | Employment levels | 0.63 |
| beta | 0.9949 | 2549.68 | 21.33 | 52.50 | Wealth | 0.68 |

Singular values (value scaling): 2.55e+03, 19.8, 13.3, 8.2, 7.43, 6.35, 5.43, 3.77, 3.04, 2.91, 2.68, 2.51, 2.3, 2.06, 1.83, 1.55, 1.18, 1.14, 0.721, 0.669, 0.623, 0.531, 0.516, 0.317, 0.254, 0.0892, 0.0854, 0.0553, 0.00859, 0.000677
Condition number (value scaling): 3.77e+06; (range scaling): 290

Weakest directions, value scaling (smallest singular values, largest loadings):
- sv 0.000677: {'d_h': -1.0, 'theta_05': -0.003, 'sigmaJ_B': -0.001, 'pi_dn_h': 0.001}
- sv 0.00859: {'theta_05': 0.999, 'pi_dn_w': 0.033, 'd_w': 0.014, 'theta_617': 0.009}
- sv 0.0553: {'d_w': -0.984, 'pi_dn_w': -0.138, 'sigmaJ_B': -0.096, 'p_H': -0.038}
- sv 0.0854: {'pi_dn_w': -0.966, 'd_w': 0.14, 'eta_up': -0.1, 'p_H': 0.08}
- sv 0.0892: {'sigmaJ_B': -0.988, 'pi_dn_w': 0.094, 'd_w': 0.084, 'lam_w_B': 0.05}

Weakest directions, range scaling:
- sv 0.977: {'m_H': 0.864, 'eta_up': 0.457, 'F': 0.122, 'p_H': -0.11}
- sv 1.49: {'F': -0.662, 'eta_up': -0.608, 'm_H': 0.416, 'beta': -0.072}
- sv 1.85: {'F': 0.681, 'eta_up': -0.577, 'kappa_S': 0.288, 'm_H': 0.245}
- sv 3.07: {'pi_dn_h': -0.754, 'd_h': 0.43, 'lam_h_W': 0.422, 'lam_w_W': 0.152}
- sv 4.18: {'lam_h_W': -0.638, 'lam_w_W': -0.477, 'pi_dn_h': -0.383, 'kappa_S': 0.263}

Near-collinear pairs (|corr| of columns > 0.9):
- none

Parameters with norm < 3 (value scaling): ['delta_w_B', 'pi_c0', 'pi_c1', 'p_H', 'm_H', 'lam_w_B', 'lam_h_B', 'lam_h_W', 'pi_dn_w', 'pi_dn_h', 'd_w', 'd_h', 'theta_05', 'theta_617', 'kappa_S', 'sigma0_B', 'sigmaJ_B', 'eta_up']

Information by block: share of each parameter's sum of squared sensitivities (value scaling), percent; last row = mean over parameters.

| parameter | Employment levels | Base hazards | Her exits | Joint loss, monthly | Her search | His search | Separation | Wealth | Joint loss, annual | Wage growth | Safety net | His earnings | Consumption | Added work | Her earnings |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| delta_w_B | 1 | 94 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| delta_w_W | 0 | 97 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| delta_h_B | 3 | 89 | 0 | 3 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| delta_h_W | 1 | 96 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pi_c0 | 0 | 1 | 0 | 94 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| pi_c1 | 0 | 1 | 0 | 89 | 0 | 0 | 0 | 0 | 9 | 0 | 0 | 0 | 0 | 0 | 0 |
| p_H | 1 | 64 | 0 | 7 | 2 | 1 | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 |
| m_H | 1 | 21 | 0 | 27 | 3 | 3 | 0 | 0 | 44 | 0 | 0 | 0 | 0 | 0 | 0 |
| lam_w_B | 10 | 1 | 53 | 2 | 21 | 0 | 0 | 3 | 1 | 1 | 1 | 0 | 1 | 1 | 5 |
| lam_w_W | 5 | 0 | 69 | 0 | 24 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| lam_h_B | 7 | 4 | 0 | 0 | 1 | 60 | 0 | 0 | 0 | 1 | 4 | 17 | 4 | 0 | 0 |
| lam_h_W | 11 | 0 | 1 | 1 | 5 | 78 | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 0 | 0 |
| pi_up_w | 55 | 0 | 26 | 0 | 6 | 0 | 0 | 6 | 0 | 4 | 2 | 0 | 0 | 0 | 0 |
| pi_up_h | 40 | 0 | 38 | 0 | 0 | 0 | 0 | 5 | 0 | 16 | 0 | 0 | 0 | 0 | 0 |
| pi_dn_w | 19 | 1 | 80 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pi_dn_h | 12 | 1 | 13 | 4 | 5 | 0 | 0 | 5 | 2 | 41 | 0 | 8 | 6 | 2 | 0 |
| d_w | 20 | 23 | 25 | 4 | 7 | 0 | 0 | 8 | 5 | 5 | 0 | 0 | 1 | 0 | 1 |
| d_h | 17 | 5 | 15 | 5 | 1 | 1 | 0 | 8 | 4 | 21 | 1 | 10 | 11 | 1 | 0 |
| phi_F | 81 | 0 | 16 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| phi_P | 76 | 0 | 9 | 0 | 13 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| theta_05 | 81 | 0 | 14 | 0 | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| theta_617 | 79 | 0 | 8 | 0 | 10 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| phi_h | 97 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| F | 74 | 0 | 4 | 0 | 17 | 0 | 0 | 2 | 0 | 0 | 3 | 0 | 0 | 0 | 0 |
| kappa_S | 19 | 0 | 3 | 1 | 2 | 1 | 0 | 2 | 0 | 0 | 72 | 0 | 0 | 0 | 0 |
| sigma0_B | 13 | 1 | 0 | 0 | 3 | 5 | 75 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| sigma0_W | 25 | 0 | 5 | 0 | 11 | 0 | 49 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| sigmaJ_B | 7 | 20 | 0 | 6 | 24 | 10 | 24 | 1 | 6 | 0 | 1 | 0 | 0 | 0 | 0 |
| eta_up | 63 | 0 | 2 | 1 | 21 | 1 | 0 | 5 | 0 | 2 | 4 | 0 | 0 | 1 | 0 |
| beta | 21 | 0 | 7 | 0 | 2 | 0 | 0 | 68 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| mean | 27.9 | 17.4 | 13.0 | 8.3 | 6.1 | 5.5 | 5.0 | 4.3 | 3.5 | 3.3 | 3.2 | 1.2 | 0.8 | 0.3 | 0.3 |