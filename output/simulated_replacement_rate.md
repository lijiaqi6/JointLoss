# Does unemployment insurance offset the delayed cost of a teen layoff? Simulated replacement rate (Fable C1)

Built by `99.SimulatedReplacementRate.py` (2026-10-20); design in its docstring. PSID sons 25-55 whose father's teen-window years fall in 1976+ (state UI laws), valid wage, PSID weights; within-son design, s.e. clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**

Sons 2,043; son-years 15,738; simulated replacement rate mean 0.342 (s.d. 0.144; share of window years with the cap binding 0.75); with duration 0.342. Treated sons (teen layoff year): 278.

## Within son: the layoff cost x the replacement rate

| measure | layoff x age | layoff x rr x age | closure x rr x age | father's ln wage x rr x age (placebo) | rr x age | N son-years / sons |
|---|---|---|---|---|---|---|
| rr (1 s.d.) | 0.035 (0.118; p=0.765) | -0.218* (0.129; p=0.091) | 0.108 (0.206; p=0.601) | 0.034 (0.032; p=0.291) | -0.108 (0.110; p=0.327) | 15,738 / 2,043 |
| rr (1 s.d.), + layoff x father's ln wage x age | 0.040 (0.113; p=0.725) | -0.038 (0.187; p=0.840) | 0.126 (0.205; p=0.540) | 0.027 (0.032; p=0.388) | -0.106 (0.110; p=0.336) | 15,738 / 2,043 |

## Layoff coefficient by band, sons above vs below the median simulated rr (0.358)

| sample | 25-29 | 45-49 | change |
|---|---|---|---|
| rr above the median | 0.302* (0.175; p=0.085) | -0.432 (0.457; p=0.344) | -0.734* (0.417; p=0.078) |
| rr below the median | 0.214 (0.259; p=0.409) | 0.031 (0.632; p=0.961) | -0.183 (0.689; p=0.791) |

