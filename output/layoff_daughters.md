# A father's teen layoff and daughters' outcomes by age (Fable A4)

Built by `92.LayoffDaughters.py` (2026-10-20); design in its docstring. One reduced specification for sons and daughters: the outcome on lyp and the father's window measures (wage, hours, unemployment, zero hours, volatility, closure share, layoff share), single-age dummies, PSID weights, father present. Estimate (s.e.; p) clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**

| children | outcome | layoff 25-29 | layoff 45-49 | change | within-person layoff x age | closure change | within-person closure x age | treated at 45-49 / N children |
|---|---|---|---|---|---|---|---|---|
| sons | ln earnings | 0.121 (0.108; p=0.262) | -0.734*** (0.271; p=0.007) | -0.855*** (0.257; p=<0.001) | -0.180* (0.108; p=0.096) | 0.109 (0.244; p=0.656) | 0.052 (0.123; p=0.675) | 131 / 3,013 |
| sons | ln hourly wage | -0.017 (0.095; p=0.858) | -0.555** (0.219; p=0.011) | -0.538** (0.213; p=0.012) | -0.086 (0.096; p=0.371) | 0.200 (0.181; p=0.267) | 0.091 (0.088; p=0.301) | 131 / 3,013 |
| sons | ln family income | 0.128 (0.126; p=0.310) | -0.709** (0.304; p=0.020) | -0.836*** (0.282; p=0.003) | -0.213* (0.120; p=0.076) | -0.044 (0.296; p=0.882) | -0.018 (0.141; p=0.901) | 142 / 3,055 |
| daughters | ln earnings | 0.023 (0.156; p=0.884) | 0.462 (0.284; p=0.104) | 0.439 (0.285; p=0.123) | 0.200 (0.130; p=0.123) | -0.015 (0.304; p=0.961) | 0.092 (0.129; p=0.475) | 145 / 3,062 |
| daughters | ln hourly wage | 0.085 (0.088; p=0.336) | 0.472** (0.236; p=0.045) | 0.387* (0.214; p=0.070) | 0.168** (0.075; p=0.025) | -0.232 (0.197; p=0.239) | -0.036 (0.072; p=0.613) | 145 / 3,062 |
| daughters | ln family income | 0.039 (0.121; p=0.746) | 0.599** (0.274; p=0.029) | 0.560** (0.259; p=0.031) | 0.124 (0.094; p=0.185) | 0.167 (0.244; p=0.494) | 0.002 (0.108; p=0.985) | 172 / 3,156 |

