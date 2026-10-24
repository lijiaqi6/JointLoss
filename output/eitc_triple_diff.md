# The EITC eligibility contrast as one triple difference (committee re-read memo, action 9)

Built by `136.EITCTripleDiff.py` (2026-10-24); design in its docstring. Per $1,000 of exposure x (age-40)/10; son FE; s.e. clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1. **Intent to treat; descriptive.**

Sons 2,833; likely eligible 925.

| specification | exposure x age (reference group) | exposure x age x likely eligible | exposure x age x middle third | exposure x age x top third |
|---|---|---|---|---|
| birth-year and children x age (as 101): likely eligible | 0.0291*** (0.0098; p=0.003) (others) | 0.0017 (0.0059; p=0.773) | | |
| birth-year and children x age (as 101): parental-income thirds | 0.0286*** (0.0101; p=0.004) (bottom third) | | -0.0000 (0.0068; p=0.999) | 0.0001 (0.0064; p=0.984) |
| children x birth-year cells x age: likely eligible | 0.0289** (0.0114; p=0.011) (others) | 0.0014 (0.0057; p=0.802) | | |
| children x birth-year cells x age: parental-income thirds | 0.0262** (0.0122; p=0.031) (bottom third) | | 0.0003 (0.0067; p=0.964) | 0.0015 (0.0063; p=0.813) |

