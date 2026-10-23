# Jacobian

S = change of each moment in weighted units (sqrt of the objective weight) per 10% move of a parameter (value scaling: 10% of |theta|; range scaling: 10% of the bound range, the plan's protocol; z: per unit of the logistic coordinate). Moments in the objective with finite rows: 85 of 97.

| parameter | theta | norm (10% of value) | norm (10% of range) | norm (per z) | top block | share |
|---|---:|---:|---:|---:|---|---:|
| delta_w_B | 0.002963 | 2.81 | 28.45 | 25.25 | Base hazards | 0.95 |
| delta_w_W | 0.00205 | 5.22 | 76.35 | 48.40 | Base hazards | 0.97 |
| delta_h_B | 0.004881 | 3.83 | 23.51 | 31.99 | Base hazards | 0.89 |
| delta_h_W | 0.002779 | 7.45 | 80.36 | 67.34 | Base hazards | 0.96 |
| pi_c0 | 4.351e-05 | 0.88 | 40.43 | 8.60 | Joint loss, monthly | 0.94 |
| pi_c1 | 0.000383 | 1.17 | 60.89 | 11.44 | Joint loss, monthly | 0.89 |
| p_H | 0.01929 | 2.16 | 54.87 | 10.21 | Base hazards | 0.63 |
| m_H | 14.66 | 2.56 | 5.07 | 12.62 | Joint loss, annual | 0.47 |
| lam_w_B | 0.07905 | 1.10 | 12.41 | 8.88 | Her exits | 0.58 |
| lam_w_W | 0.1572 | 6.03 | 34.17 | 47.16 | Her exits | 0.70 |
| lam_h_B | 0.1231 | 1.64 | 11.82 | 13.11 | His search | 0.57 |
| lam_h_W | 0.3247 | 2.21 | 6.06 | 13.85 | His search | 0.79 |
| pi_up_w | 0.008173 | 11.30 | 82.26 | 92.41 | Employment levels | 0.55 |
| pi_up_h | 0.005461 | 5.29 | 57.62 | 44.03 | Employment levels | 0.40 |
| pi_dn_w | 0.0006611 | 0.85 | 256.91 | 8.46 | Her exits | 0.79 |
| pi_dn_h | 0.02158 | 0.77 | 7.10 | 6.83 | Wage growth | 0.45 |
| d_w | 0.02146 | 0.18 | 17.22 | 1.83 | Her exits | 0.30 |
| d_h | 0.0002468 | 0.00 | 12.52 | 0.02 | Wage growth | 0.22 |
| phi_F | 0.3597 | 17.66 | 73.66 | 180.21 | Employment levels | 0.79 |
| phi_P | 0.1052 | 7.66 | 109.23 | 262.90 | Employment levels | 0.75 |
| theta_05 | -0.0004076 | 0.01 | 40.75 | 90.52 | Employment levels | 0.81 |
| theta_617 | -0.01824 | 0.65 | 53.48 | 116.60 | Employment levels | 0.79 |
| phi_h | 0.17 | 8.58 | 75.66 | 187.00 | Employment levels | 0.97 |
| F | 0.5999 | 11.55 | 11.55 | 0.01 | Employment levels | 0.72 |
| kappa_S | 0.1242 | 0.91 | 7.32 | 7.96 | Safety net | 0.69 |
| sigma0_B | 0.002883 | 2.59 | 17.94 | 22.13 | Separation | 0.73 |
| sigma0_W | 0.001354 | 3.93 | 58.10 | 36.68 | Separation | 0.48 |
| sigmaJ_B | 0.001285 | 0.15 | 11.43 | 1.45 | Her search | 0.27 |
| eta_up | 0.859 | 2.43 | 8.50 | 17.37 | Employment levels | 0.67 |
| g_age | 0.02858 | 2.38 | 16.62 | 20.36 | Employment levels | 0.40 |
| beta | 0.9949 | 2562.63 | 21.44 | 52.69 | Wealth | 0.68 |

Singular values (value scaling): 2.56e+03, 20, 13.4, 8.19, 7.42, 6.33, 5.42, 3.78, 3.04, 2.92, 2.68, 2.52, 2.39, 2.1, 1.83, 1.57, 1.2, 1.16, 0.859, 0.694, 0.663, 0.596, 0.566, 0.489, 0.329, 0.284, 0.0913, 0.0863, 0.0596, 0.00497, 0.000736
Condition number (value scaling): 3.48e+06; (range scaling): 246

Weakest directions, value scaling (smallest singular values, largest loadings):
- sv 0.000736: {'d_h': 1.0, 'theta_05': -0.031, 'd_w': 0.001, 'sigmaJ_B': 0.001}
- sv 0.00497: {'theta_05': -0.999, 'd_h': -0.031, 'pi_dn_w': -0.015, 'd_w': -0.008}
- sv 0.0596: {'d_w': 0.964, 'sigmaJ_B': 0.259, 'pi_dn_w': 0.038, 'p_H': 0.038}
- sv 0.0863: {'pi_dn_w': 0.955, 'sigmaJ_B': 0.222, 'd_w': -0.092, 'phi_P': 0.079}
- sv 0.0913: {'sigmaJ_B': 0.937, 'd_w': -0.242, 'pi_dn_w': -0.242, 'lam_w_B': -0.024}

Weakest directions, range scaling:
- sv 1.15: {'m_H': -0.868, 'eta_up': -0.419, 'F': -0.205, 'p_H': 0.112}
- sv 1.52: {'F': 0.878, 'm_H': -0.329, 'eta_up': 0.279, 'kappa_S': 0.139}
- sv 2.01: {'eta_up': 0.795, 'm_H': -0.338, 'F': -0.323, 'kappa_S': -0.272}
- sv 3.6: {'pi_dn_h': 0.736, 'd_h': -0.439, 'g_age': 0.322, 'lam_h_W': -0.303}
- sv 4.18: {'lam_h_W': 0.766, 'g_age': 0.494, 'lam_h_B': -0.244, 'd_h': -0.149}

Near-collinear pairs (|corr| of columns > 0.9):
- none

Parameters with norm < 3 (value scaling): ['delta_w_B', 'pi_c0', 'pi_c1', 'p_H', 'm_H', 'lam_w_B', 'lam_h_B', 'lam_h_W', 'pi_dn_w', 'pi_dn_h', 'd_w', 'd_h', 'theta_05', 'theta_617', 'kappa_S', 'sigma0_B', 'sigmaJ_B', 'eta_up', 'g_age']

Information by block: share of each parameter's sum of squared sensitivities (value scaling), percent; last row = mean over parameters.

| parameter | Employment levels | Base hazards | Her exits | Joint loss, monthly | Her search | His search | Wealth | Separation | Wage growth | Joint loss, annual | Safety net | His earnings | Consumption | Added work | Her earnings |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| delta_w_B | 1 | 95 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| delta_w_W | 0 | 97 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| delta_h_B | 4 | 89 | 0 | 3 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| delta_h_W | 1 | 96 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pi_c0 | 0 | 1 | 0 | 94 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 |
| pi_c1 | 0 | 1 | 0 | 89 | 0 | 0 | 0 | 0 | 0 | 9 | 0 | 0 | 0 | 0 | 0 |
| p_H | 1 | 63 | 0 | 7 | 2 | 1 | 0 | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |
| m_H | 1 | 19 | 0 | 28 | 4 | 2 | 0 | 0 | 0 | 47 | 0 | 0 | 0 | 0 | 0 |
| lam_w_B | 9 | 0 | 58 | 1 | 16 | 0 | 4 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 5 |
| lam_w_W | 5 | 0 | 70 | 0 | 24 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| lam_h_B | 8 | 4 | 0 | 1 | 1 | 57 | 0 | 0 | 1 | 0 | 5 | 17 | 4 | 1 | 0 |
| lam_h_W | 10 | 0 | 1 | 1 | 4 | 79 | 1 | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 0 |
| pi_up_w | 55 | 0 | 26 | 0 | 6 | 0 | 6 | 0 | 4 | 0 | 2 | 0 | 0 | 0 | 0 |
| pi_up_h | 40 | 0 | 38 | 0 | 0 | 0 | 5 | 0 | 16 | 0 | 0 | 0 | 0 | 0 | 0 |
| pi_dn_w | 19 | 1 | 79 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pi_dn_h | 13 | 1 | 13 | 2 | 4 | 1 | 4 | 0 | 45 | 0 | 0 | 7 | 6 | 3 | 0 |
| d_w | 20 | 21 | 30 | 3 | 7 | 0 | 7 | 0 | 5 | 4 | 1 | 0 | 1 | 1 | 1 |
| d_h | 15 | 8 | 18 | 2 | 2 | 1 | 6 | 0 | 22 | 3 | 0 | 9 | 10 | 3 | 0 |
| phi_F | 79 | 0 | 18 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| phi_P | 75 | 0 | 9 | 0 | 13 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| theta_05 | 81 | 0 | 13 | 0 | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 |
| theta_617 | 79 | 0 | 7 | 0 | 11 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| phi_h | 97 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| F | 72 | 0 | 4 | 0 | 18 | 0 | 2 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 |
| kappa_S | 22 | 0 | 2 | 1 | 2 | 0 | 1 | 0 | 1 | 0 | 69 | 0 | 0 | 1 | 0 |
| sigma0_B | 14 | 1 | 0 | 0 | 4 | 6 | 0 | 73 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| sigma0_W | 26 | 0 | 6 | 0 | 11 | 1 | 8 | 48 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| sigmaJ_B | 8 | 18 | 0 | 6 | 27 | 9 | 1 | 24 | 0 | 5 | 1 | 0 | 0 | 0 | 0 |
| eta_up | 67 | 0 | 0 | 0 | 19 | 0 | 4 | 0 | 2 | 0 | 5 | 0 | 0 | 1 | 0 |
| g_age | 40 | 0 | 5 | 1 | 13 | 0 | 27 | 0 | 11 | 0 | 2 | 0 | 0 | 0 | 0 |
| beta | 21 | 0 | 7 | 0 | 2 | 0 | 68 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| mean | 28.6 | 16.7 | 13.2 | 7.9 | 6.3 | 5.1 | 4.8 | 4.7 | 3.7 | 3.4 | 3.0 | 1.1 | 0.8 | 0.5 | 0.3 |