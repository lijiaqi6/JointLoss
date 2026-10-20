# Jacobian at the start values

S = change of each moment in standard errors per 10% move of a parameter (value scaling: 10% of |theta|; range scaling: 10% of the bound range, the plan's protocol). Moments 91 of 91 finite.

| parameter | theta | norm (10% of value) | norm (10% of range) | top block | share |
|---|---:|---:|---:|---|---:|
| delta_w_B | 0.001559 | 4.30 | 82.68 | Base hazards | 0.69 |
| delta_w_W | 0.001004 | 7.51 | 224.45 | Base hazards | 0.81 |
| delta_h_B | 0.002562 | 4.88 | 57.17 | Base hazards | 0.93 |
| delta_h_W | 0.00172 | 10.79 | 188.10 | Base hazards | 0.91 |
| pi_c0 | 3.482e-05 | 0.84 | 242.56 | Joint loss, monthly | 0.91 |
| pi_c1 | 0.0002856 | 1.14 | 79.92 | Joint loss, monthly | 0.88 |
| p_H | 0.1 | 9.12 | 44.71 | Base hazards | 0.82 |
| m_H | 12.6 | 9.83 | 22.62 | Base hazards | 0.46 |
| lam_w_B | 0.157 | 4.58 | 25.99 | Her search | 0.94 |
| lam_w_W | 0.1252 | 9.78 | 69.56 | Her search | 0.96 |
| lam_h_B | 0.2611 | 1.99 | 6.80 | His search | 0.74 |
| lam_h_W | 0.2611 | 4.47 | 15.24 | His search | 0.88 |
| pi_up_w | 0.0073 | 14.77 | 120.39 | Her search | 0.73 |
| pi_up_h | 0.005679 | 8.80 | 92.16 | Her search | 0.60 |
| pi_dn_w | 0.01856 | 1.72 | 18.54 | Her exits | 0.46 |
| pi_dn_h | 0.02896 | 0.88 | 6.05 | Her search | 0.35 |
| d_w | 0.09555 | 0.74 | 15.55 | Her search | 0.45 |
| d_h | 0.06962 | 0.47 | 13.56 | Her search | 0.29 |
| phi_F | 0.3112 | 23.93 | 115.31 | Employment levels | 0.62 |
| phi_P | 0.1546 | 21.25 | 206.12 | Her search | 0.76 |
| theta_05 | 0.0002326 | 0.01 | 49.60 | Her search | 0.95 |
| theta_617 | 0.04143 | 2.17 | 78.54 | Her search | 0.95 |
| phi_h | 0.1295 | 9.01 | 104.29 | Employment levels | 0.99 |
| F | 0.1012 | 2.60 | 15.39 | Her search | 0.88 |
| kappa_S | 2.639 | 0.07 | 0.02 | Wealth | 0.47 |
| sigma0_B | 0.002679 | 3.12 | 23.31 | Her search | 0.49 |
| sigma0_W | 0.001274 | 7.69 | 120.78 | Her search | 0.80 |
| sigmaJ_B | 0.008062 | 0.45 | 5.53 | Base hazards | 0.34 |
| sigmaJ_W | 0.005333 | 0.59 | 10.98 | Her search | 0.57 |
| a_bar | 25.64 | 3.09 | 7.24 | Wealth | 0.99 |

Singular values (value scaling): 31.9, 21, 15.4, 9.69, 8.64, 6.06, 5.22, 4.7, 4.52, 3.97, 3.37, 3, 2.68, 2.28, 1.99, 1.79, 1.19, 1.12, 0.878, 0.791, 0.679, 0.665, 0.566, 0.42, 0.286, 0.25, 0.2, 0.149, 0.035, 0.00111
Condition number: 2.87e+04

Weakest directions (smallest singular values, largest loadings):
- sv 0.00111: {'theta_05': -1.0, 'kappa_S': -0.012, 'd_h': -0.001, 'sigmaJ_B': 0.001}
- sv 0.035: {'kappa_S': -0.997, 'sigmaJ_B': 0.05, 'sigmaJ_W': -0.029, 'F': 0.023}
- sv 0.149: {'d_h': -0.893, 'pi_dn_h': 0.44, 'sigmaJ_B': 0.054, 'sigmaJ_W': -0.046}
- sv 0.2: {'sigmaJ_B': 0.815, 'sigmaJ_W': 0.48, 'd_w': 0.258, 'pi_dn_h': -0.097}
- sv 0.25: {'theta_617': 0.944, 'd_w': -0.214, 'sigmaJ_B': 0.164, 'sigmaJ_W': -0.127}

Near-collinear pairs (|corr| of columns > 0.9):
- lam_w_W / theta_05: -0.948
- lam_w_W / theta_617: -0.942
- lam_w_W / F: -0.903
- theta_05 / theta_617: +0.968
- theta_05 / F: +0.940
- theta_617 / F: +0.924

Parameters with norm < 3 (value scaling): ['pi_c0', 'pi_c1', 'lam_h_B', 'pi_dn_w', 'pi_dn_h', 'd_w', 'd_h', 'theta_05', 'theta_617', 'F', 'kappa_S', 'sigmaJ_B', 'sigmaJ_W']