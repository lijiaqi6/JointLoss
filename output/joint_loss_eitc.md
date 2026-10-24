# Joint job loss and the EITC (PI question for Paper A)

Built by `132.JointLossEITC.py` (2026-10-24); design in its docstring. Federal EITC imputed at the couple's actual earned income; married fathers with a child 0-17, wife employed at baseline, husband's first displacement 1984-2021 (25's units); unweighted. **Descriptive.**

## 1. The credit and earned income around the husband's displacement

| group | families | eligible: baseline / ev / ev+1 | mean credit (2000 $): baseline / ev / ev+1 | zero earned income: ev / ev+1 | mean earned income (2000 $): baseline / ev / ev+1 |
|---|---|---|---|---|---|
| joint loss | 157 | 0.312 / 0.268 / 0.376 | 427 / 585 / 829 | 0.000 / 0.019 | 48,659 / 40,616 / 37,082 |
| husband only | 909 | 0.217 / 0.190 / 0.197 | 304 / 354 / 387 | 0.000 / 0.012 | 55,912 / 53,268 / 53,070 |
| controls | 33,009 | 0.100 / 0.048 / 0.069 | 142 / 117 / 130 | 0.001 / 0.003 | 74,817 / 75,142 / 80,145 |

## 2. Change in the credit from baseline to event year (ev)

| group | lost (eligible -> 0) | cut | unchanged | raised | gained (0 -> eligible) | never eligible | families with both years |
|---|---|---|---|---|---|---|---|
| joint loss | 0.101 | 0.073 | 0.009 | 0.092 | 0.211 | 0.514 | 109 |
| husband only | 0.058 | 0.050 | 0.010 | 0.077 | 0.109 | 0.696 | 704 |
| controls | 0.040 | 0.016 | 0.005 | 0.023 | 0.039 | 0.877 | 19,261 |

Among families eligible at baseline: joint loss: lost 0.367, cut 0.267, raised 0.333; husband only: lost 0.299, cut 0.255, raised 0.394; controls: lost 0.476, cut 0.191, raised 0.274.

## 2. Change in the credit from baseline to the year after (ev+1)

| group | lost (eligible -> 0) | cut | unchanged | raised | gained (0 -> eligible) | never eligible | families with both years |
|---|---|---|---|---|---|---|---|
| joint loss | 0.089 | 0.059 | 0.007 | 0.163 | 0.207 | 0.474 | 135 |
| husband only | 0.079 | 0.034 | 0.008 | 0.072 | 0.115 | 0.692 | 783 |
| controls | 0.049 | 0.016 | 0.004 | 0.021 | 0.042 | 0.868 | 27,696 |

Among families eligible at baseline: joint loss: lost 0.279, cut 0.186, raised 0.512; husband only: lost 0.411, cut 0.179, raised 0.371; controls: lost 0.553, cut 0.174, raised 0.231.

