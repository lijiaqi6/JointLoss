# What identifies the 'rest' of the IGE split? (Fable B2)

Built by `97.RestIdentification.py` (2026-10-20); design in its docstring. One row per son (sons with a valid wage at 25-55), PSID weights. S.d. of ln parental income 0.653.

## 1. How much of ln parental income the mediators predict

| regressors | R2 | residual s.d. |
|---|---|---|
| 75's components + structure | 0.728 | 0.341 |
| + 80's resources (lpl, asset / transfer / other shares, own, AFDC, children, schooling) | 0.834 | 0.266 |
| lpl alone | 0.629 | 0.398 |
| lpl + the three income shares | 0.671 | 0.374 |
| the identity term lpl - ln(1 - shares) | 0.501 | 0.461 |

## 2. The split with and without the income-defined resources (ln earnings, 25-55)

| split | IGE | rest | rest share |
|---|---|---|---|
| 80's split B (with lpl and the income shares) | 0.396*** (0.023; p<0.001) | 0.188*** (0.046; p<0.001) | 0.476*** (0.100; p<0.001) |
| &nbsp;&nbsp;wage share | | | 0.120** (0.060; p=0.045) |
| &nbsp;&nbsp;hours share | | | 0.012 (0.018; p=0.523) |
| &nbsp;&nbsp;stability share | | | 0.049*** (0.018; p=0.006) |
| &nbsp;&nbsp;group share | | | 0.002 (0.005; p=0.616) |
| &nbsp;&nbsp;earnings share | | | 0.089 (0.068; p=0.191) |
| &nbsp;&nbsp;assets share | | | 0.001 (0.029; p=0.965) |
| &nbsp;&nbsp;transfers share | | | 0.065* (0.033; p=0.052) |
| &nbsp;&nbsp;others share | | | 0.003 (0.011; p=0.798) |
| &nbsp;&nbsp;family size share | | | 0.001 (0.006; p=0.908) |
| &nbsp;&nbsp;schooling share | | | 0.129*** (0.035; p<0.001) |
| without lpl and the income shares (non-income resources only) | 0.396*** (0.023; p<0.001) | 0.210*** (0.039; p<0.001) | 0.530*** (0.089; p<0.001) |
| &nbsp;&nbsp;wage share | | | 0.130** (0.054; p=0.017) |
| &nbsp;&nbsp;hours share | | | 0.015 (0.015; p=0.326) |
| &nbsp;&nbsp;stability share | | | 0.053*** (0.018; p=0.003) |
| &nbsp;&nbsp;group share | | | 0.002 (0.005; p=0.636) |
| &nbsp;&nbsp;assets share | | | -0.005 (0.027; p=0.860) |
| &nbsp;&nbsp;transfers share | | | 0.072*** (0.023; p=0.002) |
| &nbsp;&nbsp;family size share | | | 0.001 (0.006; p=0.886) |
| &nbsp;&nbsp;schooling share | | | 0.134*** (0.035; p<0.001) |

