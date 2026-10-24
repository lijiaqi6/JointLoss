# What lowers the pay of sons of laid-off fathers in midlife: health or place?

Built by `116.SonsHealthPlace.py` (2026-10-24); design in its docstring. Coefficient of the father's teen layoff share (per unit share). *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**

## 1. The candidates as outcomes

| outcome | mean | 25-29 | 45-49 | change | within son x age | sons |
|---|---|---|---|---|---|---|
| fair or poor health (1984+) | 0.090 | 0.024 (0.046; p=0.595) | -0.010 (0.096; p=0.916) | -0.035 (0.103; p=0.736) | 0.023 (0.046; p=0.619) | 4,654 |
| health limits his work (1994+) | 0.104 | -0.012 (0.059; p=0.844) | -0.038 (0.086; p=0.660) | -0.026 (0.098; p=0.788) | -0.046 (0.052; p=0.376) | 3,711 |
| lives in his state at 17 | 0.741 | -0.015 (0.105; p=0.886) | 0.073 (0.174; p=0.672) | 0.088 (0.137; p=0.517) | -0.028 (0.041; p=0.484) | 3,952 |
| unemployment rate of his state | 5.988 | -0.387 (0.291; p=0.184) | 0.182 (0.501; p=0.716) | 0.570 (0.519; p=0.272) | 0.225 (0.141; p=0.110) | 4,758 |

## 2. The within-son layoff slope with each candidate held fixed (time-varying control)

| outcome | candidate | sample: as before | + candidate | candidate's own coefficient | son-years |
|---|---|---|---|---|---|
| ly | fair or poor health | -0.270** (0.117; p=0.021) | -0.268** (0.116; p=0.022) | -0.107*** (0.022; p<0.001) | 36,319 |
| ly | health limits work | -0.276* (0.148; p=0.062) | -0.284* (0.147; p=0.053) | -0.193*** (0.031; p<0.001) | 20,339 |
| ly | lives in his state at 17 | -0.300** (0.122; p=0.014) | -0.299** (0.122; p=0.014) | 0.016 (0.035; p=0.647) | 30,144 |
| ly | state unemployment rate | -0.250** (0.103; p=0.015) | -0.243** (0.102; p=0.017) | -0.019*** (0.002; p<0.001) | 41,874 |
| lw | fair or poor health | -0.112 (0.089; p=0.208) | -0.112 (0.089; p=0.208) | -0.007 (0.016; p=0.646) | 36,319 |
| lw | health limits work | -0.165 (0.116; p=0.155) | -0.167 (0.116; p=0.150) | -0.048** (0.023; p=0.037) | 20,339 |
| lw | lives in his state at 17 | -0.141 (0.093; p=0.131) | -0.141 (0.093; p=0.131) | 0.004 (0.028; p=0.898) | 30,144 |
| lw | state unemployment rate | -0.122 (0.082; p=0.141) | -0.120 (0.082; p=0.147) | -0.005*** (0.002; p=0.009) | 41,874 |

