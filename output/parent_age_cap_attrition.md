# Parental income at a fixed parental age, the income cap, and attrition (committee memo K3 + K4)

Built by `125.ParentAgeCapAttrition.py` (2026-10-24); design in its docstring. IGE of ln earnings; estimate (s.e.; p) clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1.

## K3. Parental age and the cap

| specification | 25-29 | oldest band | change | sons |
|---|---|---|---|---|
| baseline | 0.276*** (0.022; p=<0.001) | 0.443*** (0.048; p=<0.001) (45-49) | 0.167*** (0.048; p=<0.001) | 4,644 |
| parental head 40-50 in every window year | 0.279*** (0.036; p=<0.001) | 0.404*** (0.075; p=<0.001) (45-49) | 0.125* (0.072; p=0.081) | 1,423 |
| father-present sons with income at the father's 40-50: baseline income | 0.231*** (0.027; p=<0.001) | 0.430*** (0.067; p=<0.001) (45-49) | 0.199*** (0.062; p=0.001) | 2,987 |
| same sons: parental income at the father's 40-50 | 0.267*** (0.030; p=<0.001) | 0.526*** (0.065; p=<0.001) (45-49) | 0.259*** (0.062; p=<0.001) | 2,987 |
| no upper bound on parental income or son's earnings | 0.274*** (0.022; p=<0.001) | 0.471*** (0.050; p=<0.001) (45-49) | 0.198*** (0.050; p=<0.001) | 4,644 |

Share of parental child-years (son's 13-19) above $150,000 of 1967: 0.0004; share of son-years with earnings above it (of those passing the lower bound and the hours screen): 0.0004.

## K4. Attrition

| band | sons observed | as a share of sons at 25-29 |
|---|---|---|
| 25-29 | 4,053 | 1.000 |
| 30-34 | 3,648 | 0.900 |
| 35-39 | 2,881 | 0.711 |
| 40-44 | 2,146 | 0.529 |
| 45-49 | 1,483 | 0.366 |
| 50-55 | 1,070 | 0.264 |

IGE at 25-29: all sons 0.276*** (0.022; p=<0.001); sons later observed at 45-49 0.257*** (0.033; p=<0.001) (1,252 sons); the others 0.275*** (0.027; p=<0.001); stayers - others -0.018 (0.041; p=0.669).

