# Jacobian

S = change of each moment in weighted units (sqrt of the objective weight) per 10% move of a parameter (value scaling: 10% of |theta|; range scaling: 10% of the bound range, the plan's protocol; z: per unit of the logistic coordinate). Moments in the objective with finite rows: 85 of 97.

| parameter | theta | norm (10% of value) | norm (10% of range) | norm (per z) | top block | share |
|---|---:|---:|---:|---:|---|---:|
| delta_w_B | 0.002595 | 2.80 | 32.30 | 25.45 | Base hazards | 0.89 |
| delta_w_W | 0.001665 | 4.87 | 87.78 | 45.78 | Base hazards | 0.91 |
| delta_h_B | 0.004826 | 3.78 | 23.47 | 31.64 | Base hazards | 0.92 |
| delta_h_W | 0.002598 | 6.64 | 76.60 | 60.39 | Base hazards | 0.95 |
| pi_c0 | 3.512e-05 | 0.66 | 37.34 | 6.44 | Joint loss, monthly | 0.91 |
| pi_c1 | 0.0002783 | 0.96 | 68.91 | 9.46 | Joint loss, monthly | 0.88 |
| p_H | 0.02033 | 2.15 | 51.85 | 10.70 | Base hazards | 0.54 |
| m_H | 15.63 | 2.92 | 5.42 | 13.56 | Her search | 0.35 |
| lam_w_B | 0.1572 | 1.86 | 10.56 | 14.58 | Her search | 0.87 |
| lam_w_W | 0.1224 | 2.78 | 20.21 | 22.30 | Her search | 0.79 |
| lam_h_B | 0.257 | 1.57 | 5.44 | 10.91 | His search | 0.80 |
| lam_h_W | 0.2628 | 2.69 | 9.12 | 18.55 | His search | 0.82 |
| pi_up_w | 0.007039 | 8.19 | 69.22 | 67.72 | Her search | 0.30 |
| pi_up_h | 0.005575 | 5.54 | 59.18 | 46.16 | Employment levels | 0.47 |
| pi_dn_w | 0.01824 | 1.01 | 11.05 | 9.16 | Her exits | 0.45 |
| pi_dn_h | 0.03341 | 0.82 | 4.88 | 6.79 | Wage growth | 0.58 |
| d_w | 0.09666 | 0.46 | 9.55 | 4.39 | Wealth | 0.34 |
| d_h | 0.04926 | 0.27 | 10.89 | 2.62 | Wage growth | 0.34 |
| phi_F | 0.3036 | 18.44 | 91.12 | 226.63 | Employment levels | 0.90 |
| phi_P | 0.1497 | 11.18 | 112.00 | 275.00 | Employment levels | 0.71 |
| theta_05 | -0.007298 | 0.10 | 21.09 | 46.52 | Her search | 0.59 |
| theta_617 | 0.03976 | 0.73 | 27.47 | 63.29 | Her search | 0.66 |
| phi_h | 0.1263 | 7.36 | 87.42 | 212.60 | Employment levels | 0.99 |
| F | 0.1041 | 0.94 | 5.44 | 7.80 | Employment levels | 0.35 |
| kappa_S | 0.1083 | 0.70 | 6.47 | 6.25 | Safety net | 0.89 |
| sigma0_B | 0.00268 | 2.48 | 18.48 | 21.44 | Separation | 0.70 |
| sigma0_W | 0.001272 | 4.14 | 65.05 | 38.73 | Her search | 0.47 |
| sigmaJ_B | 0.008001 | 0.32 | 3.97 | 2.93 | Separation | 0.44 |
| sigmaJ_W | 0.005251 | 0.29 | 5.49 | 2.73 | Separation | 0.48 |
| a_bar | 25.9 | 2.25 | 5.22 | 12.81 | Wealth | 0.99 |
| eta_up | 0.3791 | 1.00 | 7.93 | 8.76 | Her search | 0.48 |

Singular values (value scaling): 20.8, 11, 7.75, 6.63, 5.34, 4.51, 3.8, 3.63, 3.06, 2.72, 2.54, 2.29, 2.17, 1.68, 1.47, 1.27, 0.961, 0.828, 0.814, 0.716, 0.688, 0.616, 0.498, 0.42, 0.332, 0.247, 0.188, 0.175, 0.162, 0.102, 0.0335
Condition number (value scaling): 619; (range scaling): 86.9

Weakest directions, value scaling (smallest singular values, largest loadings):
- sv 0.0335: {'theta_05': -0.995, 'eta_up': -0.079, 'd_w': -0.047, 'F': 0.03}
- sv 0.102: {'d_h': -0.97, 'pi_dn_h': 0.205, 'eta_up': -0.068, 'F': -0.064}
- sv 0.162: {'sigmaJ_W': 0.907, 'sigmaJ_B': -0.332, 'eta_up': -0.225, 'F': -0.05}
- sv 0.175: {'sigmaJ_B': 0.726, 'd_w': 0.449, 'sigmaJ_W': 0.371, 'eta_up': 0.285}
- sv 0.188: {'d_w': 0.534, 'theta_617': -0.518, 'sigmaJ_B': -0.506, 'eta_up': 0.371}

Weakest directions, range scaling:
- sv 1.58: {'eta_up': 0.833, 'm_H': -0.26, 'd_w': 0.219, 'sigmaJ_B': 0.219}
- sv 1.72: {'m_H': -0.753, 'eta_up': -0.344, 'F': 0.314, 'sigmaJ_B': 0.305}
- sv 1.92: {'lam_h_B': -0.562, 'pi_dn_h': 0.546, 'm_H': -0.353, 'F': -0.349}
- sv 2.18: {'F': 0.602, 'sigmaJ_B': -0.589, 'lam_h_B': -0.348, 'a_bar': 0.296}
- sv 2.37: {'pi_dn_h': -0.572, 'F': -0.428, 'sigmaJ_B': -0.42, 'm_H': -0.331}

Near-collinear pairs (|corr| of columns > 0.9):
- none

Parameters with norm < 3 (value scaling): ['delta_w_B', 'pi_c0', 'pi_c1', 'p_H', 'm_H', 'lam_w_B', 'lam_w_W', 'lam_h_B', 'lam_h_W', 'pi_dn_w', 'pi_dn_h', 'd_w', 'd_h', 'theta_05', 'theta_617', 'F', 'kappa_S', 'sigma0_B', 'sigmaJ_B', 'sigmaJ_W', 'a_bar', 'eta_up']