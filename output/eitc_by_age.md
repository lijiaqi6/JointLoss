# The EITC in childhood re-scored by the son's age (Fable F)

Built by `101.EITCByAge.py` (2026-10-20); design in its docstring. PSID sons whose income years at 13-18 fall in 1975+; exposure = maximum federal + state EITC for the family's number of children, summed over 13-18 (thousands of 2000 dollars); birth-year, state-at-17 and number-of-children FE, single-age dummies; PSID weights; s.e. clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1. **Intent to treat; descriptive.**

Sons 3,017 (born 1962-1998); exposure mean 13.15 (s.d. 6.91); by birth cohort: 1960.0-1964.0 6.64; 1965.0-1969.0 5.63; 1970.0-1974.0 6.89; 1975.0-1979.0 12.00; 1980.0-1984.0 19.10; 1985.0-1989.0 20.19; 1990.0-1994.0 19.96; 1995.0-1999.0 21.37.

## ln earnings
### ln earnings, all sons

| | 25-29 | 30-34 | 35-39 | 40-44 | change 40-44 - 25-29 | within son x age | sons |
|---|---|---|---|---|---|---|---|
| exposure (1,000 2000 $ over 13-18) | -0.0160* (0.0083; p=0.052) | -0.0157 (0.0109; p=0.149) | -0.0096 (0.0129; p=0.455) | -0.0025 (0.0185; p=0.894) | 0.0136 (0.0186; p=0.465) | 0.0294*** (0.0095; p=0.002) | 2,925 |

### ln earnings, all sons, + ln parental income

| | 25-29 | 30-34 | 35-39 | 40-44 | change 40-44 - 25-29 | within son x age | sons |
|---|---|---|---|---|---|---|---|
| exposure (1,000 2000 $ over 13-18) | -0.0159** (0.0077; p=0.039) | -0.0145* (0.0084; p=0.084) | -0.0086 (0.0118; p=0.466) | -0.0061 (0.0162; p=0.704) | 0.0098 (0.0167; p=0.559) | 0.0274*** (0.0091; p=0.003) | 2,925 |

### ln earnings, mother with <= 12 years of schooling

| | 25-29 | 30-34 | 35-39 | 40-44 | change 40-44 - 25-29 | within son x age | sons |
|---|---|---|---|---|---|---|---|
| exposure (1,000 2000 $ over 13-18) | -0.0112 (0.0119; p=0.347) | 0.0067 (0.0135; p=0.621) | 0.0012 (0.0206; p=0.954) | 0.0107 (0.0401; p=0.790) | 0.0219 (0.0399; p=0.583) | 0.0256 (0.0171; p=0.134) | 1,329 |

## employment
### employed, all sons

| | 25-29 | 30-34 | 35-39 | 40-44 | change 40-44 - 25-29 | within son x age | sons |
|---|---|---|---|---|---|---|---|
| exposure (1,000 2000 $ over 13-18) | -0.0003 (0.0016; p=0.850) | -0.0019 (0.0023; p=0.421) | 0.0038 (0.0032; p=0.227) | 0.0060 (0.0066; p=0.364) | 0.0063 (0.0066; p=0.340) | 0.0090*** (0.0027; p=<0.001) | 3,017 |

### employed, mother with <= 12 years of schooling

| | 25-29 | 30-34 | 35-39 | 40-44 | change 40-44 - 25-29 | within son x age | sons |
|---|---|---|---|---|---|---|---|
| exposure (1,000 2000 $ over 13-18) | 0.0015 (0.0035; p=0.681) | -0.0000 (0.0044; p=0.999) | 0.0008 (0.0061; p=0.892) | 0.0034 (0.0193; p=0.859) | 0.0020 (0.0197; p=0.920) | 0.0088 (0.0082; p=0.281) | 1,381 |

