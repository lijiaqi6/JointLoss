# Does the EITC in childhood change the IGE, by the son's age? (PI question)

Built by `128.EITCAndIGE.py` (2026-10-24); design in its docstring. Exposure in thousands of 2000 dollars over 13-18; s.e. clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1. **Intent to treat; descriptive.**

Sons 2,918; exposure mean 13.15 (s.d. 6.89); imputed credit over 13-18 mean 1.51 (s.d. 4.13); corr(exposure, lyp) 0.044.

## 1. Exposure x parental income: the change in the IGE per $1,000 of exposure

| | 25-29 | 30-34 | 35-39 | 40-44 | change 40-44 - 25-29 | within son x age |
|---|---|---|---|---|---|---|
| exposure x ln parental income | -0.0001 (0.0039; p=0.980) | 0.0038 (0.0039; p=0.330) | -0.0010 (0.0053; p=0.855) | -0.0044 (0.0071; p=0.537) | -0.0043 (0.0072; p=0.553) | -0.0016 (0.0038; p=0.681) |
| IGE at mean exposure (same regression) | 0.2768*** (0.0589; p=<0.001) | 0.3446*** (0.0638; p=<0.001) | 0.4045*** (0.0770; p=<0.001) | 0.4556*** (0.0953; p=<0.001) | | |

One s.d. of exposure (6.89) times the interaction: 25-29 -0.001, 30-34 +0.026, 35-39 -0.007, 40-44 -0.030.

## 2. The IGE by band, sons with more and less exposure than expected from their birth year, state and number of children

| | 25-29 | 30-34 | 35-39 | 40-44 | change 40-44 - 25-29 | sons |
|---|---|---|---|---|---|---|
| more exposure | 0.2720*** (0.0400; p=<0.001) | 0.4300*** (0.0469; p=<0.001) | 0.4075*** (0.0498; p=<0.001) | 0.4701*** (0.0656; p=<0.001) | 0.1981*** (0.0629; p=0.002) | 1,459 |
| less exposure | 0.2667*** (0.0389; p=<0.001) | 0.3537*** (0.0384; p=<0.001) | 0.3846*** (0.0485; p=<0.001) | 0.3692*** (0.0604; p=<0.001) | 0.1025* (0.0616; p=0.096) | 1,459 |

## 3. The IGE by band without and with the family's imputed credit over 13-18

| | 25-29 | 30-34 | 35-39 | 40-44 |
|---|---|---|---|---|
| IGE without | 0.2756*** (0.0290; p=<0.001) | 0.3943*** (0.0314; p=<0.001) | 0.3926*** (0.0390; p=<0.001) | 0.4106*** (0.0461; p=<0.001) |
| IGE with | 0.2798*** (0.0319; p=<0.001) | 0.3917*** (0.0382; p=<0.001) | 0.3955*** (0.0461; p=<0.001) | 0.3912*** (0.0512; p=<0.001) |
| credit (per $1,000 over 13-18) | 0.0019 (0.0053; p=0.720) | -0.0012 (0.0077; p=0.876) | 0.0015 (0.0079; p=0.850) | -0.0133 (0.0115; p=0.249) |
| IGE carried by the credit (without - with) | -0.0041 | +0.0026 | -0.0028 | +0.0194 |

