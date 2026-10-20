# Jacobian

S = change of each moment in weighted units (sqrt of the objective weight) per 10% move of a parameter (value scaling: 10% of |theta|; range scaling: 10% of the bound range, the plan's protocol; z: per unit of the logistic coordinate). Moments in the objective with finite rows: 85 of 97.

| parameter | theta | norm (10% of value) | norm (10% of range) | norm (per z) | top block | share |
|---|---:|---:|---:|---:|---|---:|
| delta_w_B | 0.002985 | 2.85 | 28.59 | 25.55 | Base hazards | 0.94 |
| delta_w_W | 0.002044 | 4.92 | 72.16 | 45.63 | Base hazards | 0.97 |
| delta_h_B | 0.004864 | 3.75 | 23.12 | 31.37 | Base hazards | 0.88 |
| delta_h_W | 0.00279 | 7.33 | 78.82 | 66.29 | Base hazards | 0.96 |
| pi_c0 | 4.215e-05 | 0.78 | 37.16 | 7.67 | Joint loss, monthly | 0.94 |
| pi_c1 | 0.00035 | 1.07 | 60.98 | 10.49 | Joint loss, monthly | 0.89 |
| p_H | 0.02139 | 2.17 | 49.63 | 11.27 | Base hazards | 0.65 |
| m_H | 14.94 | 1.99 | 3.86 | 9.64 | Joint loss, annual | 0.36 |
| lam_w_B | 0.0881 | 1.21 | 12.25 | 9.81 | Her exits | 0.45 |
| lam_w_W | 0.1575 | 5.91 | 33.41 | 46.21 | Her exits | 0.70 |
| lam_h_B | 0.1201 | 1.45 | 10.71 | 11.61 | His search | 0.57 |
| lam_h_W | 0.301 | 2.50 | 7.40 | 16.29 | His search | 0.81 |
| pi_up_w | 0.007308 | 13.38 | 108.91 | 110.35 | Employment levels | 0.46 |
| pi_up_h | 0.005125 | 7.35 | 85.37 | 61.20 | Her exits | 0.45 |
| pi_dn_w | 0.0001372 | 0.20 | 298.34 | 2.04 | Her exits | 0.79 |
| pi_dn_h | 0.02036 | 0.68 | 6.72 | 6.14 | Wage growth | 0.27 |
| d_w | 0.09246 | 0.82 | 17.64 | 7.78 | Employment levels | 0.24 |
| d_h | 0.0003988 | 0.00 | 13.69 | 0.03 | Wage growth | 0.21 |
| phi_F | 0.3681 | 18.34 | 74.75 | 182.24 | Employment levels | 0.74 |
| phi_P | 0.1119 | 8.22 | 110.29 | 266.38 | Employment levels | 0.70 |
| theta_05 | 0.02155 | 0.56 | 38.84 | 88.09 | Employment levels | 0.81 |
| theta_617 | 0.007946 | 0.30 | 57.55 | 128.88 | Employment levels | 0.76 |
| phi_h | 0.1781 | 9.22 | 77.63 | 192.29 | Employment levels | 0.95 |
| F | 0.5697 | 9.48 | 9.98 | 4.78 | Employment levels | 0.71 |
| kappa_S | 0.1057 | 0.63 | 5.95 | 5.62 | Safety net | 0.65 |
| sigma0_B | 0.00275 | 2.29 | 16.63 | 19.72 | Separation | 0.78 |
| sigma0_W | 0.001103 | 3.74 | 67.78 | 35.31 | Separation | 0.37 |
| sigmaJ_B | 0.00125 | 0.09 | 7.36 | 0.91 | Separation | 0.40 |
| sigmaJ_W | 0.0007057 | 0.05 | 6.44 | 0.45 | Base hazards | 0.35 |
| a_bar | 59.99 | 2.64 | 2.64 | 0.00 | Wealth | 0.95 |
| eta_up | 0.5015 | 1.45 | 8.65 | 12.04 | Employment levels | 0.61 |

Singular values (value scaling): 23.6, 12.6, 8.78, 7.4, 6.42, 5.02, 4.57, 3.71, 2.91, 2.73, 2.6, 2.25, 2.09, 2.05, 1.81, 1.48, 1.18, 1.02, 0.773, 0.653, 0.608, 0.453, 0.428, 0.351, 0.261, 0.231, 0.133, 0.0485, 0.025, 0.0198, 0.00103
Condition number (value scaling): 2.3e+04; (range scaling): 323

Weakest directions, value scaling (smallest singular values, largest loadings):
- sv 0.00103: {'d_h': -1.0, 'pi_dn_h': 0.003, 'sigmaJ_B': 0.002, 'pi_dn_w': -0.002}
- sv 0.0198: {'pi_dn_w': -0.975, 'sigmaJ_W': -0.199, 'theta_05': -0.075, 'sigmaJ_B': 0.055}
- sv 0.025: {'sigmaJ_W': -0.972, 'pi_dn_w': 0.203, 'sigmaJ_B': 0.119, 'theta_617': 0.017}
- sv 0.0485: {'sigmaJ_B': 0.99, 'sigmaJ_W': 0.127, 'pi_dn_w': 0.033, 'theta_05': -0.024}
- sv 0.133: {'theta_617': -0.884, 'theta_05': -0.415, 'eta_up': 0.174, 'kappa_S': -0.069}

Weakest directions, range scaling:
- sv 1.04: {'m_H': 0.985, 'p_H': -0.095, 'sigmaJ_B': 0.069, 'pi_dn_h': 0.047}
- sv 1.52: {'a_bar': -0.864, 'F': 0.39, 'eta_up': 0.267, 'kappa_S': -0.125}
- sv 1.84: {'eta_up': 0.65, 'F': 0.555, 'a_bar': 0.465, 'lam_h_W': 0.129}
- sv 2.3: {'pi_dn_h': -0.635, 'eta_up': -0.464, 'F': 0.412, 'kappa_S': 0.336}
- sv 2.7: {'pi_dn_h': 0.596, 'F': 0.47, 'kappa_S': 0.37, 'd_h': -0.307}

Near-collinear pairs (|corr| of columns > 0.9):
- none

Parameters with norm < 3 (value scaling): ['delta_w_B', 'pi_c0', 'pi_c1', 'p_H', 'm_H', 'lam_w_B', 'lam_h_B', 'lam_h_W', 'pi_dn_w', 'pi_dn_h', 'd_w', 'd_h', 'theta_05', 'theta_617', 'kappa_S', 'sigma0_B', 'sigmaJ_B', 'sigmaJ_W', 'a_bar', 'eta_up']

Information by block: share of each parameter's sum of squared sensitivities (value scaling), percent; last row = mean over parameters.

| parameter | Employment levels | Base hazards | Her exits | Joint loss, monthly | Separation | His search | Wealth | Her search | Joint loss, annual | Safety net | Wage growth | His earnings | Consumption | Added work | Her earnings |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| delta_w_B | 1 | 94 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| delta_w_W | 1 | 97 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| delta_h_B | 4 | 88 | 0 | 4 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| delta_h_W | 1 | 96 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pi_c0 | 0 | 1 | 0 | 94 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| pi_c1 | 0 | 1 | 0 | 89 | 0 | 0 | 0 | 0 | 9 | 0 | 0 | 0 | 0 | 0 | 0 |
| p_H | 2 | 65 | 0 | 7 | 0 | 0 | 0 | 1 | 24 | 0 | 0 | 0 | 0 | 0 | 0 |
| m_H | 1 | 26 | 0 | 29 | 0 | 5 | 0 | 1 | 36 | 0 | 0 | 0 | 0 | 0 | 0 |
| lam_w_B | 10 | 1 | 45 | 3 | 0 | 2 | 2 | 18 | 3 | 2 | 2 | 0 | 1 | 1 | 11 |
| lam_w_W | 5 | 0 | 70 | 0 | 0 | 0 | 0 | 23 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| lam_h_B | 7 | 6 | 0 | 1 | 0 | 57 | 0 | 0 | 0 | 4 | 1 | 19 | 3 | 1 | 0 |
| lam_h_W | 10 | 0 | 1 | 0 | 0 | 81 | 0 | 2 | 0 | 1 | 1 | 1 | 0 | 2 | 0 |
| pi_up_w | 46 | 0 | 33 | 0 | 0 | 0 | 9 | 6 | 0 | 1 | 3 | 0 | 0 | 0 | 0 |
| pi_up_h | 39 | 0 | 45 | 0 | 0 | 0 | 4 | 1 | 0 | 0 | 11 | 0 | 0 | 0 | 0 |
| pi_dn_w | 18 | 1 | 79 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pi_dn_h | 17 | 9 | 13 | 2 | 0 | 0 | 9 | 4 | 3 | 1 | 27 | 6 | 5 | 4 | 0 |
| d_w | 24 | 19 | 24 | 2 | 0 | 0 | 12 | 7 | 4 | 1 | 4 | 0 | 1 | 0 | 3 |
| d_h | 14 | 8 | 10 | 2 | 0 | 3 | 11 | 8 | 3 | 1 | 21 | 8 | 7 | 3 | 0 |
| phi_F | 74 | 0 | 23 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phi_P | 70 | 0 | 15 | 0 | 0 | 0 | 1 | 12 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| theta_05 | 81 | 0 | 14 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| theta_617 | 76 | 0 | 14 | 0 | 0 | 0 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phi_h | 95 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| F | 71 | 0 | 5 | 0 | 0 | 0 | 2 | 18 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| kappa_S | 19 | 0 | 6 | 1 | 0 | 0 | 7 | 1 | 0 | 65 | 0 | 0 | 0 | 0 | 0 |
| sigma0_B | 9 | 2 | 0 | 0 | 78 | 4 | 1 | 3 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |
| sigma0_W | 30 | 0 | 14 | 0 | 37 | 1 | 9 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| sigmaJ_B | 4 | 25 | 0 | 3 | 40 | 18 | 0 | 4 | 2 | 1 | 1 | 1 | 0 | 0 | 0 |
| sigmaJ_W | 10 | 35 | 1 | 6 | 31 | 1 | 5 | 6 | 1 | 1 | 1 | 0 | 0 | 1 | 0 |
| a_bar | 0 | 0 | 0 | 1 | 0 | 0 | 95 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| eta_up | 61 | 0 | 4 | 1 | 0 | 1 | 4 | 18 | 0 | 7 | 1 | 0 | 1 | 2 | 0 |
| mean | 25.9 | 18.6 | 13.6 | 8.0 | 6.0 | 5.7 | 5.6 | 5.1 | 3.1 | 2.9 | 2.6 | 1.2 | 0.6 | 0.6 | 0.5 |