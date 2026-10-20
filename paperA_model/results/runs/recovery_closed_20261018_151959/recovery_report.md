# Recovery: recovery_closed_20261018_151959

19 free parameters; truth = analytic start values; start = truth + N(0, 0.5) in logistic units (seed 99); targets = model moments at the truth with CRN seed 20261018 (estimation seed 20261018); 496 evaluations in 31 generations (152 min). Best Q 482 (Q at the truth = 0 when the target seed equals the estimation seed); noise band of Q at the real targets across 5 seeds: sd 398.4.

z: (value - truth) / s.e.; noise s.e. = simulation noise only (the plan's yardstick); data s.e. = sandwich with the bootstrap covariance of the targets plus simulation noise (the precision of an estimate on real data).

| parameter | truth | start | estimate | noise s.e. | z start | z estimate | within 2 noise s.e. | data s.e. | z estimate (data s.e.) |
|---|---:|---:|---:|---:|---:|---:|---|---:|---:|
| delta_w_B | 0.001559 | 0.001621 | 0.002059 | 4.31e-05 | +1.4 | +11.6 | NO | 6.92e-05 | +7.22 |
| delta_w_W | 0.001004 | 0.0008033 | 0.0009589 | 1.78e-05 | -11.2 | -2.5 | NO | 3.15e-05 | -1.42 |
| delta_h_B | 0.002562 | 0.002622 | 0.002984 | 7.84e-05 | +0.8 | +5.4 | NO | 0.000123 | +3.44 |
| delta_h_W | 0.00172 | 0.002365 | 0.001974 | 1.44e-05 | +44.7 | +17.7 | NO | 4.2e-05 | +6.06 |
| pi_c0 | 3.482e-05 | 4.179e-05 | 4.327e-05 | 4.16e-06 | +1.7 | +2.0 | NO | 6.99e-06 | +1.21 |
| pi_c1 | 0.0002856 | 0.0006508 | 0.0003875 | 2.24e-05 | +16.3 | +4.5 | NO | 3.78e-05 | +2.69 |
| m_H | 12.6 | 11.05 | 10.69 | 0.19 | -8.2 | -10.1 | NO | 0.432 | -4.43 |
| sigma0_B | 0.002679 | 0.00206 | 0.001175 | 6.24e-05 | -9.9 | -24.1 | NO | 0.000144 | -10.48 |
| sigma0_W | 0.001274 | 0.0007746 | 0.001069 | 2.37e-05 | -21.1 | -8.6 | NO | 4.99e-05 | -4.10 |
| sigmaJ_B | 0.008062 | 0.01226 | 0.01176 | 0.00283 | +1.5 | +1.3 | yes | 0.00429 | +0.86 |
| sigmaJ_W | 0.005333 | 0.007318 | 0.0144 | 0.000788 | +2.5 | +11.5 | NO | 0.00214 | +4.23 |
| pi_up_w | 0.0073 | 0.01203 | 0.008684 | 4e-05 | +118.2 | +34.6 | NO | 0.000172 | +8.06 |
| pi_up_h | 0.005679 | 0.008216 | 0.005906 | 4.02e-05 | +63.1 | +5.7 | NO | 0.000155 | +1.47 |
| pi_dn_w | 0.01856 | 0.0209 | 0.01679 | 0.000736 | +3.2 | -2.4 | NO | 0.00147 | -1.20 |
| pi_dn_h | 0.02896 | 0.03327 | 0.05142 | 0.00323 | +1.3 | +7.0 | NO | 0.00995 | +2.26 |
| d_w | 0.09555 | 0.1483 | 0.2954 | 0.0141 | +3.7 | +14.2 | NO | 0.03 | +6.66 |
| d_h | 0.06962 | 0.04545 | 0.0456 | 0.00838 | -2.9 | -2.9 | NO | 0.0481 | -0.50 |
| lam_h_B | 0.2611 | 0.2569 | 0.2582 | 0.0242 | -0.2 | -0.1 | yes | 0.0467 | -0.06 |
| lam_h_W | 0.2611 | 0.2969 | 0.2866 | 0.0142 | +2.5 | +1.8 | yes | 0.024 | +1.06 |

Within 2 noise s.e.: 3 of 19; within 2 data s.e.: 8 of 19. Q by generation (best): 1: 2.91e+03, 4: 1.9e+03, 7: 1.78e+03, 10: 926, 13: 708, 16: 655, 19: 505, 22: 505, 25: 505, 28: 505, 31: 482
