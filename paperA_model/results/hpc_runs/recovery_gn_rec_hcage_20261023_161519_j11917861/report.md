# Jacobian

S = change of each moment in weighted units (sqrt of the objective weight) per 10% move of a parameter (value scaling: 10% of |theta|; range scaling: 10% of the bound range, the plan's protocol; z: per unit of the logistic coordinate). Moments in the objective with finite rows: 85 of 97.

| parameter | theta | norm (10% of value) | norm (10% of range) | norm (per z) | top block | share |
|---|---:|---:|---:|---:|---|---:|
| delta_w_B | 0.003075 | 3.03 | 29.59 | 27.15 | Base hazards | 0.92 |
| delta_w_W | 0.001649 | 4.54 | 82.57 | 42.67 | Base hazards | 0.93 |
| delta_h_B | 0.004973 | 4.06 | 24.48 | 33.81 | Base hazards | 0.88 |
| delta_h_W | 0.003759 | 9.32 | 74.33 | 81.30 | Base hazards | 0.95 |
| pi_c0 | 1.819e-05 | 0.28 | 30.41 | 2.74 | Joint loss, monthly | 0.89 |
| pi_c1 | 0.000861 | 1.89 | 43.81 | 18.05 | Joint loss, monthly | 0.87 |
| p_H | 0.01725 | 1.68 | 47.71 | 6.95 | Base hazards | 0.75 |
| m_H | 12.48 | 1.83 | 4.24 | 10.15 | Base hazards | 0.44 |
| lam_w_B | 0.05175 | 1.23 | 21.09 | 9.43 | Employment levels | 0.34 |
| lam_w_W | 0.2228 | 6.15 | 24.58 | 44.72 | Her search | 0.74 |
| lam_h_B | 0.1614 | 1.65 | 9.11 | 12.86 | His search | 0.57 |
| lam_h_W | 0.4652 | 1.66 | 3.18 | 7.95 | His search | 0.60 |
| pi_up_w | 0.01161 | 14.78 | 75.71 | 115.01 | Employment levels | 0.43 |
| pi_up_h | 0.006098 | 6.21 | 60.59 | 51.64 | Employment levels | 0.72 |
| pi_dn_w | 0.0007059 | 0.50 | 141.29 | 4.97 | Her exits | 0.66 |
| pi_dn_h | 0.03147 | 0.84 | 5.34 | 7.08 | Wage growth | 0.36 |
| d_w | 0.02243 | 0.12 | 10.63 | 1.18 | Her exits | 0.25 |
| d_h | 0.0002468 | 0.00 | 14.07 | 0.02 | Employment levels | 0.31 |
| phi_F | 0.4298 | 16.43 | 57.33 | 135.08 | Employment levels | 0.86 |
| phi_P | 0.02623 | 1.81 | 103.34 | 235.36 | Employment levels | 0.37 |
| theta_05 | 0.127 | 4.43 | 52.31 | 127.26 | Employment levels | 0.58 |
| theta_617 | -0.06958 | 0.87 | 18.67 | 38.20 | Her exits | 0.79 |
| phi_h | 0.2959 | 19.83 | 100.51 | 250.34 | Employment levels | 0.99 |
| F | 0.5999 | 15.18 | 15.19 | 0.02 | Her search | 0.54 |
| kappa_S | 0.1442 | 0.97 | 6.71 | 8.28 | Safety net | 0.74 |
| sigma0_B | 0.00146 | 1.59 | 21.80 | 14.75 | Separation | 0.61 |
| sigma0_W | 0.0008837 | 2.74 | 61.95 | 26.16 | Separation | 0.43 |
| sigmaJ_B | 0.002663 | 0.22 | 8.30 | 2.15 | Her search | 0.27 |
| eta_up | 0.9033 | 4.17 | 13.85 | 29.14 | Her search | 0.72 |
| g_age | 0.0294 | 3.69 | 25.10 | 31.47 | Her search | 0.39 |
| beta | 0.9959 | 2993.55 | 25.02 | 61.67 | Wealth | 0.71 |

Singular values (value scaling): 2.99e+03, 27.5, 15.3, 11.5, 9.43, 6.29, 4.49, 4.04, 3.03, 2.86, 2.6, 2.23, 1.97, 1.83, 1.73, 1.43, 1.38, 1.03, 0.995, 0.888, 0.737, 0.643, 0.569, 0.301, 0.263, 0.213, 0.196, 0.108, 0.0574, 0.0413, 0.000651
Condition number (value scaling): 4.6e+06; (range scaling): 175

Weakest directions, value scaling (smallest singular values, largest loadings):
- sv 0.000651: {'d_h': 1.0, 'pi_dn_h': -0.001, 'd_w': -0.0, 'phi_P': 0.0}
- sv 0.0413: {'d_w': -0.906, 'pi_dn_w': 0.383, 'phi_P': 0.131, 'sigmaJ_B': -0.099}
- sv 0.0574: {'pi_dn_w': 0.813, 'sigmaJ_B': 0.43, 'd_w': 0.329, 'phi_P': 0.173}
- sv 0.108: {'sigmaJ_B': 0.87, 'pi_dn_w': -0.377, 'd_w': -0.248, 'p_H': 0.122}
- sv 0.196: {'pi_c0': 0.707, 'p_H': -0.517, 'theta_617': 0.363, 'm_H': 0.263}

Weakest directions, range scaling:
- sv 1.06: {'m_H': -0.962, 'F': 0.201, 'p_H': 0.126, 'eta_up': 0.061}
- sv 1.34: {'F': -0.698, 'eta_up': -0.53, 'lam_h_W': -0.401, 'm_H': -0.166}
- sv 1.68: {'eta_up': -0.73, 'F': 0.387, 'lam_h_W': 0.321, 'sigmaJ_B': -0.224}
- sv 1.94: {'lam_h_W': 0.733, 'F': -0.433, 'pi_dn_h': 0.404, 'theta_617': 0.169}
- sv 2.44: {'pi_dn_h': 0.825, 'lam_h_W': -0.36, 'd_h': -0.325, 'lam_w_W': 0.159}

Near-collinear pairs (|corr| of columns > 0.9):
- p_H / m_H: +0.904

Parameters with norm < 3 (value scaling): ['pi_c0', 'pi_c1', 'p_H', 'm_H', 'lam_w_B', 'lam_h_B', 'lam_h_W', 'pi_dn_w', 'pi_dn_h', 'd_w', 'd_h', 'phi_P', 'theta_617', 'kappa_S', 'sigma0_B', 'sigma0_W', 'sigmaJ_B']

Information by block: share of each parameter's sum of squared sensitivities (value scaling), percent; last row = mean over parameters.

| parameter | Employment levels | Base hazards | Her search | Her exits | Joint loss, monthly | His search | Wealth | Separation | Wage growth | Safety net | Joint loss, annual | His earnings | Her earnings | Consumption | Added work |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| delta_w_B | 2 | 92 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 |
| delta_w_W | 0 | 93 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| delta_h_B | 3 | 88 | 1 | 0 | 2 | 4 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 |
| delta_h_W | 0 | 95 | 1 | 0 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pi_c0 | 0 | 2 | 0 | 0 | 89 | 0 | 0 | 0 | 0 | 0 | 9 | 0 | 0 | 0 | 0 |
| pi_c1 | 0 | 2 | 0 | 0 | 87 | 0 | 0 | 0 | 0 | 0 | 10 | 0 | 0 | 0 | 0 |
| p_H | 1 | 75 | 1 | 0 | 6 | 3 | 0 | 0 | 0 | 0 | 14 | 0 | 0 | 0 | 0 |
| m_H | 0 | 44 | 3 | 0 | 13 | 11 | 0 | 0 | 1 | 0 | 28 | 0 | 0 | 0 | 0 |
| lam_w_B | 34 | 1 | 23 | 7 | 0 | 6 | 6 | 0 | 3 | 3 | 0 | 0 | 15 | 1 | 0 |
| lam_w_W | 1 | 0 | 74 | 24 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| lam_h_B | 8 | 3 | 5 | 0 | 1 | 57 | 1 | 1 | 1 | 4 | 0 | 15 | 0 | 2 | 0 |
| lam_h_W | 17 | 1 | 14 | 2 | 0 | 60 | 1 | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 1 |
| pi_up_w | 43 | 0 | 22 | 24 | 0 | 0 | 5 | 0 | 4 | 2 | 0 | 0 | 0 | 0 | 0 |
| pi_up_h | 72 | 0 | 1 | 10 | 0 | 0 | 3 | 0 | 13 | 0 | 0 | 0 | 0 | 0 | 0 |
| pi_dn_w | 31 | 0 | 0 | 66 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| pi_dn_h | 20 | 0 | 12 | 5 | 0 | 0 | 10 | 0 | 36 | 1 | 0 | 9 | 0 | 6 | 1 |
| d_w | 22 | 4 | 21 | 25 | 0 | 2 | 11 | 0 | 10 | 0 | 1 | 0 | 2 | 1 | 0 |
| d_h | 31 | 1 | 4 | 11 | 0 | 1 | 13 | 0 | 24 | 0 | 0 | 7 | 0 | 5 | 2 |
| phi_F | 86 | 0 | 7 | 5 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| phi_P | 37 | 0 | 32 | 29 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| theta_05 | 58 | 0 | 37 | 3 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| theta_617 | 17 | 0 | 0 | 79 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| phi_h | 99 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| F | 33 | 0 | 54 | 11 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| kappa_S | 15 | 0 | 3 | 4 | 0 | 0 | 1 | 0 | 0 | 74 | 0 | 0 | 0 | 0 | 1 |
| sigma0_B | 26 | 0 | 2 | 0 | 0 | 8 | 0 | 61 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| sigma0_W | 12 | 0 | 19 | 17 | 0 | 2 | 7 | 43 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| sigmaJ_B | 8 | 24 | 27 | 2 | 1 | 8 | 1 | 26 | 1 | 0 | 1 | 0 | 0 | 0 | 1 |
| eta_up | 15 | 0 | 72 | 6 | 0 | 0 | 3 | 0 | 2 | 1 | 0 | 0 | 0 | 0 | 0 |
| g_age | 9 | 0 | 39 | 21 | 0 | 0 | 24 | 0 | 6 | 1 | 0 | 0 | 0 | 0 | 0 |
| beta | 15 | 0 | 7 | 5 | 0 | 0 | 71 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| mean | 23.2 | 17.0 | 15.7 | 11.5 | 6.6 | 5.3 | 5.2 | 4.3 | 3.5 | 3.0 | 2.1 | 1.1 | 0.6 | 0.5 | 0.3 |