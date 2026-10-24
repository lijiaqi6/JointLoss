# Jacobian

S = change of each moment in weighted units (sqrt of the objective weight) per 10% move of a parameter (value scaling: 10% of |theta|; range scaling: 10% of the bound range, the plan's protocol; z: per unit of the logistic coordinate). Moments in the objective with finite rows: 85 of 97.

| parameter | theta | norm (10% of value) | norm (10% of range) | norm (per z) | top block | share |
|---|---:|---:|---:|---:|---|---:|
| delta_w_B | 0.003076 | 3.01 | 29.38 | 26.97 | Base hazards | 0.92 |
| delta_w_W | 0.00165 | 4.46 | 81.00 | 41.88 | Base hazards | 0.95 |
| delta_h_B | 0.004973 | 4.04 | 24.36 | 33.65 | Base hazards | 0.88 |
| delta_h_W | 0.003758 | 9.27 | 73.93 | 80.85 | Base hazards | 0.95 |
| pi_c0 | 1.82e-05 | 0.27 | 29.95 | 2.70 | Joint loss, monthly | 0.89 |
| pi_c1 | 0.0008609 | 1.91 | 44.35 | 18.27 | Joint loss, monthly | 0.88 |
| p_H | 0.01725 | 1.66 | 47.15 | 6.87 | Base hazards | 0.76 |
| m_H | 12.48 | 1.76 | 4.08 | 9.76 | Base hazards | 0.44 |
| lam_w_B | 0.05151 | 1.22 | 21.05 | 9.36 | Employment levels | 0.36 |
| lam_w_W | 0.2228 | 5.98 | 23.88 | 43.45 | Her search | 0.68 |
| lam_h_B | 0.1611 | 1.73 | 9.54 | 13.45 | His search | 0.65 |
| lam_h_W | 0.4637 | 1.55 | 2.97 | 7.42 | His search | 0.63 |
| pi_up_w | 0.01161 | 14.02 | 71.83 | 109.11 | Employment levels | 0.45 |
| pi_up_h | 0.006094 | 5.91 | 57.69 | 49.14 | Employment levels | 0.69 |
| pi_dn_w | 0.0007266 | 0.53 | 145.17 | 5.26 | Her exits | 0.66 |
| pi_dn_h | 0.03194 | 0.81 | 5.06 | 6.78 | Wage growth | 0.41 |
| d_w | 0.02199 | 0.11 | 10.06 | 1.09 | Her exits | 0.32 |
| d_h | 0.0002468 | 0.00 | 14.15 | 0.02 | Employment levels | 0.27 |
| phi_F | 0.4297 | 16.57 | 57.84 | 136.31 | Employment levels | 0.87 |
| phi_P | 0.02618 | 1.80 | 103.16 | 234.92 | Employment levels | 0.40 |
| theta_05 | 0.1267 | 4.15 | 49.17 | 119.59 | Employment levels | 0.66 |
| theta_617 | -0.07013 | 1.02 | 21.91 | 44.79 | Her exits | 0.67 |
| phi_h | 0.2958 | 19.58 | 99.28 | 247.27 | Employment levels | 0.99 |
| F | 0.5999 | 14.83 | 14.83 | 0.02 | Her search | 0.47 |
| kappa_S | 0.1455 | 1.12 | 7.68 | 9.55 | Safety net | 0.76 |
| sigma0_B | 0.001467 | 1.54 | 20.98 | 14.26 | Separation | 0.64 |
| sigma0_W | 0.0008869 | 2.60 | 58.74 | 24.89 | Separation | 0.47 |
| sigmaJ_B | 0.002775 | 0.23 | 8.13 | 2.19 | Base hazards | 0.29 |
| eta_up | 0.9036 | 3.90 | 12.93 | 27.22 | Her search | 0.66 |
| g_age | 0.02949 | 3.46 | 23.45 | 29.48 | Her search | 0.34 |
| beta | 0.9949 | 2532.61 | 21.19 | 52.21 | Wealth | 0.67 |

Singular values (value scaling): 2.53e+03, 26.5, 14.8, 11.6, 9.38, 6.32, 4.46, 4.03, 3.03, 2.95, 2.63, 2.15, 2.04, 1.92, 1.78, 1.47, 1.36, 1.15, 0.993, 0.832, 0.776, 0.737, 0.613, 0.334, 0.289, 0.199, 0.173, 0.0914, 0.0498, 0.0429, 0.000717
Condition number (value scaling): 3.53e+06; (range scaling): 181

Weakest directions, value scaling (smallest singular values, largest loadings):
- sv 0.000717: {'d_h': -1.0, 'sigmaJ_B': 0.001, 'pi_dn_h': 0.001, 'd_w': 0.001}
- sv 0.0429: {'d_w': 0.805, 'pi_dn_w': -0.548, 'phi_P': -0.166, 'sigmaJ_B': 0.102}
- sv 0.0498: {'pi_dn_w': 0.794, 'd_w': 0.583, 'phi_P': 0.14, 'theta_617': 0.065}
- sv 0.0914: {'sigmaJ_B': 0.987, 'd_w': -0.08, 'pi_dn_w': 0.073, 'sigma0_B': -0.063}
- sv 0.173: {'phi_P': -0.695, 'theta_617': -0.487, 'p_H': -0.231, 'pi_dn_w': 0.219}

Weakest directions, range scaling:
- sv 1.01: {'m_H': -0.821, 'F': -0.424, 'eta_up': 0.235, 'pi_dn_h': -0.158}
- sv 1.31: {'eta_up': -0.763, 'm_H': -0.446, 'F': 0.257, 'kappa_S': 0.193}
- sv 1.67: {'F': -0.577, 'lam_h_W': 0.574, 'eta_up': -0.368, 'm_H': 0.293}
- sv 1.85: {'lam_h_W': -0.77, 'F': -0.41, 'lam_w_W': -0.297, 'eta_up': -0.289}
- sv 2.45: {'pi_dn_h': 0.881, 'd_h': -0.311, 'F': -0.231, 'sigmaJ_B': 0.191}

Near-collinear pairs (|corr| of columns > 0.9):
- none

Parameters with norm < 3 (value scaling): ['pi_c0', 'pi_c1', 'p_H', 'm_H', 'lam_w_B', 'lam_h_B', 'lam_h_W', 'pi_dn_w', 'pi_dn_h', 'd_w', 'd_h', 'phi_P', 'theta_617', 'kappa_S', 'sigma0_B', 'sigma0_W', 'sigmaJ_B']

Information by block: share of each parameter's sum of squared sensitivities (value scaling), percent; last row = mean over parameters.

| parameter | Employment levels | Base hazards | Her search | Her exits | Joint loss, monthly | His search | Wealth | Separation | Wage growth | Safety net | Joint loss, annual | His earnings | Her earnings | Consumption | Added work |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| delta_w_B | 2 | 92 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 |
| delta_w_W | 0 | 95 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| delta_h_B | 3 | 88 | 2 | 0 | 2 | 3 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| delta_h_W | 0 | 95 | 1 | 0 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pi_c0 | 0 | 2 | 0 | 0 | 89 | 0 | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 |
| pi_c1 | 0 | 2 | 0 | 0 | 88 | 0 | 0 | 0 | 0 | 0 | 10 | 0 | 0 | 0 | 0 |
| p_H | 1 | 76 | 1 | 0 | 6 | 3 | 0 | 0 | 0 | 0 | 13 | 0 | 0 | 0 | 0 |
| m_H | 1 | 44 | 2 | 0 | 14 | 11 | 0 | 0 | 1 | 0 | 27 | 0 | 0 | 0 | 0 |
| lam_w_B | 36 | 1 | 22 | 7 | 0 | 6 | 5 | 0 | 2 | 4 | 0 | 0 | 16 | 1 | 1 |
| lam_w_W | 1 | 0 | 68 | 30 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| lam_h_B | 8 | 3 | 0 | 0 | 0 | 65 | 2 | 1 | 3 | 3 | 0 | 12 | 0 | 2 | 0 |
| lam_h_W | 19 | 2 | 7 | 2 | 0 | 63 | 2 | 1 | 2 | 1 | 0 | 1 | 0 | 1 | 0 |
| pi_up_w | 45 | 0 | 19 | 25 | 0 | 0 | 4 | 0 | 4 | 2 | 0 | 0 | 0 | 0 | 0 |
| pi_up_h | 69 | 0 | 0 | 12 | 0 | 0 | 3 | 0 | 15 | 0 | 0 | 0 | 0 | 0 | 0 |
| pi_dn_w | 31 | 0 | 1 | 66 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| pi_dn_h | 21 | 0 | 2 | 7 | 0 | 1 | 10 | 0 | 41 | 0 | 0 | 10 | 0 | 7 | 1 |
| d_w | 24 | 5 | 7 | 32 | 1 | 1 | 10 | 0 | 13 | 1 | 1 | 0 | 3 | 1 | 1 |
| d_h | 27 | 1 | 4 | 12 | 0 | 0 | 12 | 0 | 27 | 0 | 0 | 6 | 0 | 6 | 4 |
| phi_F | 87 | 0 | 7 | 4 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| phi_P | 40 | 0 | 21 | 37 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| theta_05 | 66 | 0 | 30 | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| theta_617 | 29 | 0 | 2 | 67 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| phi_h | 99 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| F | 38 | 0 | 47 | 13 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| kappa_S | 13 | 0 | 6 | 3 | 0 | 0 | 0 | 0 | 1 | 76 | 0 | 0 | 0 | 0 | 0 |
| sigma0_B | 25 | 0 | 2 | 0 | 0 | 5 | 1 | 64 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |
| sigma0_W | 10 | 0 | 17 | 18 | 0 | 2 | 5 | 47 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| sigmaJ_B | 8 | 29 | 13 | 2 | 2 | 12 | 1 | 26 | 3 | 1 | 1 | 1 | 0 | 1 | 0 |
| eta_up | 23 | 0 | 66 | 5 | 0 | 0 | 2 | 0 | 2 | 3 | 0 | 0 | 0 | 0 | 0 |
| g_age | 11 | 0 | 34 | 26 | 0 | 0 | 21 | 0 | 7 | 1 | 0 | 0 | 0 | 0 | 0 |
| beta | 17 | 0 | 7 | 7 | 0 | 0 | 67 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| mean | 24.4 | 17.3 | 12.6 | 12.2 | 6.7 | 5.6 | 4.8 | 4.5 | 4.1 | 3.2 | 2.1 | 1.0 | 0.8 | 0.6 | 0.3 |