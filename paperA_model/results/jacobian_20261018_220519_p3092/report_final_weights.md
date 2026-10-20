# Jacobian

S = change of each moment in weighted units (sqrt of the objective weight) per 10% move of a parameter (value scaling: 10% of |theta|; range scaling: 10% of the bound range, the plan's protocol; z: per unit of the logistic coordinate). Moments in the objective with finite rows: 87 of 93.

| parameter | theta | norm (10% of value) | norm (10% of range) | norm (per z) | top block | share |
|---|---:|---:|---:|---:|---|---:|
| delta_w_B | 0.002593 | 4.62 | 53.41 | 42.04 | Her search | 0.65 |
| delta_w_W | 0.001669 | 6.55 | 117.76 | 61.55 | Base hazards | 0.51 |
| delta_h_B | 0.004827 | 3.85 | 23.94 | 32.28 | Base hazards | 0.88 |
| delta_h_W | 0.002594 | 7.50 | 86.72 | 68.29 | Base hazards | 0.75 |
| pi_c0 | 3.428e-05 | 0.62 | 36.13 | 6.09 | Joint loss, monthly | 0.91 |
| pi_c1 | 0.0002812 | 0.95 | 67.31 | 9.33 | Joint loss, monthly | 0.87 |
| p_H | 0.02 | 2.15 | 52.62 | 10.52 | Base hazards | 0.52 |
| m_H | 15.95 | 2.93 | 5.33 | 13.32 | Her search | 0.38 |
| lam_w_B | 0.157 | 6.48 | 36.74 | 50.64 | Her search | 0.99 |
| lam_w_W | 0.1252 | 8.39 | 59.64 | 67.19 | Her search | 0.98 |
| lam_h_B | 0.2611 | 1.83 | 6.23 | 12.62 | His search | 0.57 |
| lam_h_W | 0.2611 | 3.43 | 11.71 | 23.71 | His search | 0.73 |
| pi_up_w | 0.006947 | 32.21 | 275.93 | 266.57 | Her search | 0.95 |
| pi_up_h | 0.005572 | 19.04 | 203.28 | 158.50 | Her search | 0.92 |
| pi_dn_w | 0.01856 | 5.14 | 55.38 | 46.62 | Her search | 0.90 |
| pi_dn_h | 0.02896 | 1.14 | 7.90 | 9.78 | Her search | 0.77 |
| d_w | 0.09555 | 1.44 | 30.09 | 13.69 | Her search | 0.92 |
| d_h | 0.06962 | 0.75 | 21.41 | 7.19 | Her search | 0.77 |
| phi_F | 0.3076 | 39.07 | 190.54 | 473.54 | Her search | 0.78 |
| phi_P | 0.1531 | 33.83 | 331.54 | 815.00 | Her search | 0.91 |
| theta_05 | -0.001361 | 0.09 | 98.86 | 219.38 | Her search | 0.97 |
| theta_617 | 0.04027 | 4.07 | 151.54 | 349.22 | Her search | 0.99 |
| phi_h | 0.128 | 7.79 | 91.34 | 222.30 | Employment levels | 0.92 |
| F | 0.1012 | 3.32 | 19.69 | 27.60 | Her search | 0.94 |
| kappa_S | 0.104 | 0.80 | 7.72 | 7.19 | Safety net | 0.62 |
| sigma0_B | 0.002679 | 7.13 | 53.20 | 61.73 | Her search | 0.91 |
| sigma0_W | 0.001274 | 18.10 | 284.17 | 169.43 | Her search | 0.97 |
| sigmaJ_B | 0.008062 | 0.50 | 6.26 | 4.64 | Her search | 0.61 |
| sigmaJ_W | 0.005333 | 0.84 | 15.76 | 7.96 | Her search | 0.87 |
| a_bar | 25.64 | 2.39 | 5.59 | 13.68 | Wealth | 0.98 |
| eta_up | 0.5 | 6.39 | 38.34 | 53.25 | Her search | 0.98 |

Singular values (value scaling): 64.3, 19.5, 12.4, 8.06, 6.6, 5.08, 4.39, 3.72, 3.62, 3.09, 2.68, 2.52, 2.41, 1.85, 1.59, 1.46, 1.15, 0.93, 0.749, 0.67, 0.644, 0.527, 0.481, 0.412, 0.279, 0.245, 0.234, 0.199, 0.174, 0.105, 0.00718
Condition number (value scaling): 8.96e+03; (range scaling): 529

Weakest directions, value scaling (smallest singular values, largest loadings):
- sv 0.00718: {np.str_('theta_05'): 1.0, np.str_('theta_617'): 0.009, np.str_('eta_up'): 0.008, np.str_('sigmaJ_W'): 0.005}
- sv 0.105: {np.str_('d_h'): 0.857, np.str_('pi_dn_h'): -0.488, np.str_('eta_up'): 0.085, np.str_('d_w'): 0.075}
- sv 0.174: {np.str_('sigmaJ_W'): -0.958, np.str_('pi_c0'): -0.161, np.str_('p_H'): -0.118, np.str_('lam_h_B'): 0.101}
- sv 0.199: {np.str_('sigmaJ_B'): 0.884, np.str_('theta_617'): 0.324, np.str_('d_w'): 0.247, np.str_('F'): 0.108}
- sv 0.234: {np.str_('theta_617'): 0.859, np.str_('sigmaJ_B'): -0.389, np.str_('p_H'): -0.15, np.str_('d_w'): 0.147}

Weakest directions, range scaling:
- sv 1.14: {np.str_('m_H'): 0.769, np.str_('eta_up'): 0.492, np.str_('lam_h_B'): 0.246, np.str_('F'): 0.164}
- sv 1.29: {np.str_('pi_dn_h'): 0.907, np.str_('d_h'): -0.325, np.str_('m_H'): 0.226, np.str_('sigmaJ_W'): -0.08}
- sv 2.12: {np.str_('lam_h_B'): 0.697, np.str_('sigmaJ_B'): 0.404, np.str_('lam_h_W'): -0.336, np.str_('eta_up'): -0.318}
- sv 2.17: {np.str_('F'): -0.78, np.str_('sigmaJ_B'): -0.347, np.str_('a_bar'): -0.343, np.str_('m_H'): 0.248}
- sv 2.43: {np.str_('eta_up'): -0.621, np.str_('F'): 0.37, np.str_('sigmaJ_B'): -0.369, np.str_('m_H'): 0.367}

Near-collinear pairs (|corr| of columns > 0.9):
- lam_w_B / sigma0_B: +0.932
- lam_w_W / pi_up_h: -0.909
- lam_w_W / phi_P: -0.915
- lam_w_W / theta_05: -0.924
- lam_w_W / theta_617: -0.945
- lam_w_W / sigma0_W: +0.960
- lam_w_W / sigmaJ_W: +0.915
- pi_up_w / pi_up_h: -0.954
- pi_up_w / pi_dn_w: +0.935
- pi_up_w / d_w: -0.964
- pi_up_w / phi_F: -0.913
- pi_up_w / theta_05: -0.970
- pi_up_w / theta_617: -0.966
- pi_up_w / F: -0.931
- pi_up_w / eta_up: +0.961
- pi_up_h / pi_dn_w: -0.938
- pi_up_h / d_w: +0.924
- pi_up_h / phi_F: +0.918
- pi_up_h / theta_05: +0.958
- pi_up_h / theta_617: +0.962
- pi_up_h / F: +0.933
- pi_up_h / sigma0_W: -0.930
- pi_dn_w / d_w: -0.908
- pi_dn_w / phi_P: -0.927
- pi_dn_w / theta_05: -0.955
- pi_dn_w / theta_617: -0.963
- pi_dn_w / F: -0.925
- pi_dn_w / sigma0_W: +0.926
- pi_dn_h / d_h: +0.976
- d_w / phi_P: +0.908
- d_w / theta_05: +0.947
- d_w / theta_617: +0.951
- d_w / F: +0.907
- d_w / eta_up: -0.916
- phi_P / theta_05: +0.951
- phi_P / theta_617: +0.961
- phi_P / F: +0.952
- phi_P / sigma0_W: -0.911
- theta_05 / theta_617: +0.989
- theta_05 / F: +0.969
- theta_05 / sigma0_W: -0.941
- theta_05 / eta_up: -0.938
- theta_617 / F: +0.964
- theta_617 / sigma0_W: -0.952
- theta_617 / eta_up: -0.925
- F / sigma0_W: -0.901
- F / eta_up: -0.923
- sigma0_W / sigmaJ_W: +0.944

Parameters with norm < 3 (value scaling): [np.str_('pi_c0'), np.str_('pi_c1'), np.str_('p_H'), np.str_('m_H'), np.str_('lam_h_B'), np.str_('pi_dn_h'), np.str_('d_w'), np.str_('d_h'), np.str_('theta_05'), np.str_('kappa_S'), np.str_('sigmaJ_B'), np.str_('sigmaJ_W'), np.str_('a_bar')]