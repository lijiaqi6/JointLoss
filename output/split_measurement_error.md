# Are the shares of what is passed on attenuated by measurement error? (Fable B1)

Built by `96.SplitMeasurementError.py` (2026-10-20); design in its docstring. PSID sons 25-55, valid wage, PSID weights; components measured on the whole teen window (W), on half A, and half A instrumented by half B (IV); estimate (s.e.; p) from 200 cluster-bootstrap draws of 1968 families; share = contribution / IGE. *** p<0.01, ** p<0.05, * p<0.1. **Descriptive accounting.**

## 0. Reliability: correlation of the two halves (sons with both measured)

| component | correlation A-B | sons |
|---|---|---|
| f_lw | 0.845 | 3,217 |
| m_lw | 0.777 | 3,427 |
| f_lh | 0.671 | 3,217 |
| m_lh | 0.690 | 3,427 |
| m_zero | 0.858 | 4,555 |
| f_close | 0.602 | 3,374 |
| f_lay | 0.598 | 3,374 |
| f_un | 0.589 | 3,374 |
| f_zero | 0.838 | 3,374 |
| m_un | nan | 0 |

## Ln earnings, 25-55

| split | IGE | wage | hours | spells | rest | wage share | spells share | rest share |
|---|---|---|---|---|---|---|---|---|
| whole window, OLS | 0.393*** (0.026; p<0.001) | 0.110*** (0.029; p<0.001) | 0.015* (0.009; p=0.082) | 0.017** (0.008; p=0.038) | 0.252*** (0.039; p<0.001) | 28.0*** (7.5; p<0.001) | 4.2** (2.1; p=0.042) | 64.0*** (8.2; p<0.001) |
| half A, OLS | 0.395*** (0.026; p<0.001) | 0.091*** (0.026; p<0.001) | 0.007 (0.008; p=0.380) | 0.019** (0.008; p=0.016) | 0.278*** (0.036; p<0.001) | 23.1*** (6.7; p<0.001) | 4.8** (2.1; p=0.020) | 70.3*** (7.4; p<0.001) |
| half A instrumented by half B | 0.396*** (0.026; p<0.001) | 0.146*** (0.039; p<0.001) | 0.021** (0.011; p=0.049) | 0.011 (0.012; p=0.377) | 0.219*** (0.050; p<0.001) | 36.8*** (10.3; p<0.001) | 2.7 (3.2; p=0.386) | 55.2*** (11.1; p<0.001) |

## Ln earnings, 25-29

| split | IGE | wage | hours | spells | rest | wage share | spells share | rest share |
|---|---|---|---|---|---|---|---|---|
| whole window, OLS | 0.259*** (0.023; p<0.001) | 0.040 (0.030; p=0.193) | 0.016* (0.008; p=0.056) | 0.009 (0.009; p=0.329) | 0.195*** (0.040; p<0.001) | 15.2 (12.0; p=0.204) | 3.4 (3.6; p=0.347) | 75.1*** (13.7; p<0.001) |
| half A, OLS | 0.256*** (0.023; p<0.001) | 0.031 (0.029; p=0.280) | 0.010 (0.008; p=0.230) | 0.011 (0.010; p=0.266) | 0.204*** (0.039; p<0.001) | 12.2 (11.6; p=0.292) | 4.2 (3.9; p=0.285) | 79.7*** (13.1; p<0.001) |
| half A instrumented by half B | 0.257*** (0.023; p<0.001) | 0.060 (0.043; p=0.161) | 0.019** (0.010; p=0.047) | 0.003 (0.013; p=0.784) | 0.175*** (0.050; p<0.001) | 23.1 (16.7; p=0.165) | 1.3 (5.1; p=0.790) | 68.1*** (18.3; p<0.001) |

## Ln earnings, 45-49

| split | IGE | wage | hours | spells | rest | wage share | spells share | rest share |
|---|---|---|---|---|---|---|---|---|
| whole window, OLS | 0.449*** (0.054; p<0.001) | 0.129** (0.059; p=0.029) | 0.007 (0.015; p=0.663) | 0.036* (0.020; p=0.067) | 0.277*** (0.084; p=0.001) | 28.7** (14.3; p=0.045) | 8.0* (4.6; p=0.078) | 61.8*** (15.6; p<0.001) |
| half A, OLS | 0.455*** (0.054; p<0.001) | 0.114** (0.057; p=0.043) | -0.002 (0.014; p=0.893) | 0.046** (0.019; p=0.015) | 0.297*** (0.082; p<0.001) | 25.1* (13.2; p=0.057) | 10.1** (4.4; p=0.022) | 65.2*** (14.7; p<0.001) |
| half A instrumented by half B | 0.457*** (0.055; p<0.001) | 0.168** (0.077; p=0.028) | 0.021 (0.022; p=0.319) | 0.013 (0.029; p=0.659) | 0.255** (0.101; p=0.011) | 36.8** (18.6; p=0.048) | 2.8 (6.5; p=0.667) | 55.7*** (20.1; p=0.006) |

