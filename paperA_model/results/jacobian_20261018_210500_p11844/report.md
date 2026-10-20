# Jacobian

S = change of each moment in weighted units (sqrt of the objective weight) per 10% move of a parameter (value scaling: 10% of |theta|; range scaling: 10% of the bound range, the plan's protocol; z: per unit of the logistic coordinate). Moments in the objective with finite rows: 85 of 91.

| parameter | theta | norm (10% of value) | norm (10% of range) | norm (per z) | top block | share |
|---|---:|---:|---:|---:|---|---:|
| delta_w_B | 0.001559 | 2.83 | 54.51 | 26.70 | Base hazards | 0.70 |
| delta_w_W | 0.001004 | 4.87 | 145.65 | 46.66 | Base hazards | 0.83 |
| delta_h_B | 0.002902 | 3.49 | 36.09 | 31.45 | Base hazards | 0.91 |
| delta_h_W | 0.00156 | 6.47 | 124.39 | 60.97 | Base hazards | 0.95 |
| pi_c0 | 3.428e-05 | 0.65 | 37.87 | 6.38 | Joint loss, monthly | 0.91 |
| pi_c1 | 0.0002812 | 0.96 | 68.21 | 9.46 | Joint loss, monthly | 0.88 |
| p_H | 0.1 | 5.14 | 25.19 | 37.77 | Base hazards | 0.83 |
| m_H | 12.6 | 5.48 | 12.61 | 30.27 | Base hazards | 0.41 |
| lam_w_B | 0.157 | 3.05 | 17.32 | 23.87 | Her search | 0.95 |
| lam_w_W | 0.1252 | 5.26 | 37.39 | 42.12 | Her search | 0.89 |
| lam_h_B | 0.2611 | 1.72 | 5.88 | 11.91 | His search | 0.75 |
| lam_h_W | 0.2611 | 3.10 | 10.56 | 21.39 | His search | 0.84 |
| pi_up_w | 0.0073 | 8.65 | 70.51 | 71.38 | Her search | 0.36 |
| pi_up_h | 0.005679 | 5.77 | 60.46 | 48.05 | Employment levels | 0.52 |
| pi_dn_w | 0.01856 | 1.35 | 14.52 | 12.23 | Her exits | 0.65 |
| pi_dn_h | 0.02896 | 0.67 | 4.64 | 5.74 | Wage growth | 0.37 |
| d_w | 0.09555 | 0.51 | 10.70 | 4.87 | Wealth | 0.33 |
| d_h | 0.06962 | 0.40 | 11.51 | 3.87 | Wage growth | 0.28 |
| phi_F | 0.3076 | 19.16 | 93.43 | 232.19 | Employment levels | 0.90 |
| phi_P | 0.1531 | 12.74 | 124.86 | 306.93 | Employment levels | 0.61 |
| theta_05 | -0.001361 | 0.02 | 21.88 | 48.55 | Her search | 0.78 |
| theta_617 | 0.04027 | 0.95 | 35.33 | 81.41 | Her search | 0.77 |
| phi_h | 0.128 | 8.24 | 96.61 | 235.12 | Employment levels | 0.99 |
| F | 0.1012 | 1.25 | 7.43 | 10.41 | Her search | 0.57 |
| kappa_S | 0.104 | 0.82 | 7.84 | 7.31 | Safety net | 0.91 |
| sigma0_B | 0.002679 | 2.83 | 21.09 | 24.47 | Separation | 0.52 |
| sigma0_W | 0.001274 | 4.13 | 64.93 | 38.71 | Her search | 0.43 |
| sigmaJ_B | 0.008062 | 0.35 | 4.34 | 3.22 | Base hazards | 0.37 |
| sigmaJ_W | 0.005333 | 0.37 | 6.95 | 3.51 | Her search | 0.43 |
| a_bar | 25.64 | 3.00 | 7.02 | 17.19 | Wealth | 0.99 |

Singular values (value scaling): 21.6, 13.2, 8.96, 8.4, 5.79, 5.08, 4.15, 3.68, 3.31, 3.15, 3.02, 2.54, 2.26, 2.07, 1.73, 1.62, 0.974, 0.842, 0.779, 0.723, 0.659, 0.566, 0.533, 0.526, 0.317, 0.25, 0.212, 0.185, 0.156, 0.00632
Condition number (value scaling): 3.42e+03; (range scaling): 81.5

Weakest directions, value scaling (smallest singular values, largest loadings):
- sv 0.00632: {'theta_05': -1.0, 'theta_617': -0.006, 'F': 0.004, 'd_h': -0.002}
- sv 0.156: {'d_h': -0.735, 'sigmaJ_B': 0.501, 'pi_dn_h': 0.362, 'sigmaJ_W': 0.263}
- sv 0.185: {'sigmaJ_B': 0.695, 'd_h': 0.48, 'sigmaJ_W': 0.362, 'pi_dn_h': -0.276}
- sv 0.212: {'sigmaJ_W': -0.776, 'sigmaJ_B': 0.476, 'd_w': -0.326, 'theta_617': 0.186}
- sv 0.25: {'theta_617': -0.958, 'sigmaJ_W': -0.211, 'd_w': 0.101, 'sigmaJ_B': 0.091}

Weakest directions, range scaling:
- sv 1.96: {'pi_dn_h': 0.84, 'sigmaJ_B': 0.422, 'd_h': -0.278, 'lam_h_B': 0.158}
- sv 2.15: {'lam_h_B': -0.705, 'sigmaJ_B': 0.561, 'lam_h_W': 0.328, 'sigmaJ_W': 0.189}
- sv 2.43: {'sigmaJ_B': 0.665, 'lam_h_B': 0.493, 'pi_dn_h': -0.402, 'lam_h_W': -0.284}
- sv 2.78: {'F': -0.954, 'theta_05': 0.139, 'sigmaJ_B': 0.122, 'sigmaJ_W': 0.104}
- sv 3.84: {'sigmaJ_W': -0.824, 'p_H': -0.311, 'd_w': -0.288, 'm_H': 0.267}

Near-collinear pairs (|corr| of columns > 0.9):
- none

Parameters with norm < 3 (value scaling): ['delta_w_B', 'pi_c0', 'pi_c1', 'lam_h_B', 'pi_dn_w', 'pi_dn_h', 'd_w', 'd_h', 'theta_05', 'theta_617', 'F', 'kappa_S', 'sigma0_B', 'sigmaJ_B', 'sigmaJ_W']