# Jacobian

S = change of each moment in weighted units (sqrt of the objective weight) per 10% move of a parameter (value scaling: 10% of |theta|; range scaling: 10% of the bound range, the plan's protocol; z: per unit of the logistic coordinate). Moments in the objective with finite rows: 87 of 93.

| parameter | theta | norm (10% of value) | norm (10% of range) | norm (per z) | top block | share |
|---|---:|---:|---:|---:|---|---:|
| delta_w_B | 0.002593 | 2.98 | 34.46 | 27.12 | Base hazards | 0.85 |
| delta_w_W | 0.001669 | 5.71 | 102.51 | 53.58 | Base hazards | 0.94 |
| delta_h_B | 0.004827 | 3.74 | 23.27 | 31.36 | Base hazards | 0.93 |
| delta_h_W | 0.002594 | 7.93 | 91.69 | 72.20 | Base hazards | 0.96 |
| pi_c0 | 3.428e-05 | 0.53 | 30.71 | 5.17 | Joint loss, monthly | 0.86 |
| pi_c1 | 0.0002812 | 0.99 | 70.39 | 9.76 | Joint loss, monthly | 0.87 |
| p_H | 0.02 | 2.37 | 58.14 | 11.62 | Base hazards | 0.59 |
| m_H | 15.95 | 2.76 | 5.01 | 12.51 | Joint loss, annual | 0.32 |
| lam_w_B | 0.157 | 1.75 | 9.95 | 13.71 | Her search | 0.84 |
| lam_w_W | 0.1252 | 2.16 | 15.38 | 17.32 | Her search | 0.62 |
| lam_h_B | 0.2611 | 1.68 | 5.73 | 11.60 | His search | 0.76 |
| lam_h_W | 0.2611 | 3.30 | 11.25 | 22.78 | His search | 0.89 |
| pi_up_w | 0.006947 | 9.55 | 81.83 | 79.06 | Her search | 0.38 |
| pi_up_h | 0.005572 | 6.36 | 67.97 | 53.00 | Employment levels | 0.38 |
| pi_dn_w | 0.01856 | 1.86 | 20.08 | 16.91 | Her exits | 0.61 |
| pi_dn_h | 0.02896 | 0.59 | 4.11 | 5.09 | Wage growth | 0.43 |
| d_w | 0.09555 | 0.51 | 10.64 | 4.84 | Her search | 0.33 |
| d_h | 0.06962 | 0.40 | 11.58 | 3.89 | Wage growth | 0.30 |
| phi_F | 0.3076 | 19.70 | 96.07 | 238.76 | Employment levels | 0.85 |
| phi_P | 0.1531 | 11.58 | 113.50 | 279.02 | Employment levels | 0.71 |
| theta_05 | -0.001361 | 0.02 | 24.69 | 54.80 | Her search | 0.53 |
| theta_617 | 0.04027 | 0.87 | 32.56 | 75.04 | Her search | 0.72 |
| phi_h | 0.128 | 7.67 | 89.83 | 218.63 | Employment levels | 0.99 |
| F | 0.1012 | 1.06 | 6.31 | 8.85 | Her search | 0.32 |
| kappa_S | 0.104 | 0.70 | 6.69 | 6.24 | Safety net | 0.85 |
| sigma0_B | 0.002679 | 2.70 | 20.17 | 23.40 | Separation | 0.60 |
| sigma0_W | 0.001274 | 4.60 | 72.24 | 43.07 | Her search | 0.48 |
| sigmaJ_B | 0.008062 | 0.34 | 4.23 | 3.14 | Separation | 0.36 |
| sigmaJ_W | 0.005333 | 0.36 | 6.75 | 3.41 | Separation | 0.37 |
| a_bar | 25.64 | 2.46 | 5.76 | 14.10 | Wealth | 1.00 |
| eta_up | 0.5 | 1.63 | 9.76 | 13.55 | Her search | 0.60 |

Singular values (value scaling): 22.2, 12.4, 8.31, 7.65, 5.78, 4.93, 3.87, 3.63, 3.24, 2.98, 2.58, 2.44, 2.34, 1.87, 1.55, 1.37, 1.1, 0.973, 0.715, 0.666, 0.592, 0.524, 0.431, 0.406, 0.275, 0.243, 0.235, 0.198, 0.182, 0.106, 0.00723
Condition number (value scaling): 3.07e+03; (range scaling): 129

Weakest directions, value scaling (smallest singular values, largest loadings):
- sv 0.00723: {'theta_05': -1.0, 'theta_617': -0.01, 'eta_up': -0.008, 'sigmaJ_W': -0.006}
- sv 0.106: {'d_h': -0.855, 'pi_dn_h': 0.493, 'eta_up': -0.083, 'sigmaJ_B': 0.074}
- sv 0.182: {'sigmaJ_W': 0.953, 'pi_c0': 0.164, 'sigmaJ_B': -0.138, 'p_H': 0.116}
- sv 0.198: {'sigmaJ_B': -0.844, 'd_w': -0.368, 'theta_617': -0.299, 'sigmaJ_W': -0.137}
- sv 0.235: {'theta_617': -0.836, 'sigmaJ_B': 0.422, 'd_w': -0.183, 'eta_up': -0.14}

Weakest directions, range scaling:
- sv 1.13: {'m_H': -0.807, 'eta_up': -0.45, 'lam_h_B': -0.251, 'F': -0.166}
- sv 1.28: {'pi_dn_h': 0.914, 'd_h': -0.326, 'm_H': 0.161, 'eta_up': -0.104}
- sv 2.1: {'lam_h_B': -0.655, 'eta_up': 0.41, 'lam_h_W': 0.301, 'sigmaJ_B': -0.296}
- sv 2.14: {'F': 0.727, 'sigmaJ_B': 0.346, 'm_H': -0.301, 'a_bar': 0.287}
- sv 2.31: {'eta_up': 0.647, 'm_H': -0.395, 'F': -0.373, 'lam_h_B': 0.362}

Near-collinear pairs (|corr| of columns > 0.9):
- pi_dn_h / d_h: +0.919

Parameters with norm < 3 (value scaling): ['delta_w_B', 'pi_c0', 'pi_c1', 'p_H', 'm_H', 'lam_w_B', 'lam_w_W', 'lam_h_B', 'pi_dn_w', 'pi_dn_h', 'd_w', 'd_h', 'theta_05', 'theta_617', 'F', 'kappa_S', 'sigma0_B', 'sigmaJ_B', 'sigmaJ_W', 'a_bar', 'eta_up']