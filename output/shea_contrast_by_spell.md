# Which spells make friction-predicted parental income pass on more strongly (Shea contrast)

Built by `89.SheaContrastBySpell.py` (2026-10-20); design in its docstring. Pooled PSID sons 25-55, weighted; 200 cluster-bootstrap draws of 1968 families; estimate (s.e.; p), *** p<0.01, ** p<0.05, * p<0.1. b_P = passing on of the part of ln parental income predicted by the spell measures; b_perp = of the rest.

| outcome | spells predicting parental income | R2 | b_P | b_perp | b_P - b_perp |
|---|---|---|---|---|---|
| ln earnings | (A) 74's set: father displaced / unemployed / zero hours, mother unemployed / zero hours | 0.182 | 0.528*** (0.058; p<0.001) | 0.360*** (0.029; p<0.001) | 0.168*** (0.062; p=0.007) |
| ln earnings | (B) father's plant closures only | 0.004 | 0.074 (0.561; p=0.894) | 0.392*** (0.026; p<0.001) | -0.317 (0.565; p=0.575) |
| ln earnings | (C) father's layoffs / firings only | 0.027 | 0.742*** (0.147; p<0.001) | 0.381*** (0.027; p<0.001) | 0.361** (0.150; p=0.016) |
| ln earnings | (D) father's unemployment share only | 0.057 | 0.640*** (0.100; p<0.001) | 0.375*** (0.027; p<0.001) | 0.265*** (0.102; p=0.010) |
| ln earnings | (E) mother's unemployment share only | 0.029 | 0.659*** (0.145; p<0.001) | 0.382*** (0.026; p<0.001) | 0.277* (0.145; p=0.056) |
| ln earnings | (F) father's closures + layoffs | 0.030 | 0.670*** (0.154; p<0.001) | 0.382*** (0.027; p<0.001) | 0.288* (0.157; p=0.067) |
| ln hourly wage | (A) 74's set: father displaced / unemployed / zero hours, mother unemployed / zero hours | 0.182 | 0.428*** (0.050; p<0.001) | 0.344*** (0.024; p<0.001) | 0.084 (0.055; p=0.127) |
| ln hourly wage | (B) father's plant closures only | 0.004 | -0.094 (0.483; p=0.845) | 0.361*** (0.022; p<0.001) | -0.455 (0.486; p=0.349) |
| ln hourly wage | (C) father's layoffs / firings only | 0.027 | 0.631*** (0.116; p<0.001) | 0.352*** (0.022; p<0.001) | 0.279** (0.118; p=0.018) |
| ln hourly wage | (D) father's unemployment share only | 0.057 | 0.559*** (0.089; p<0.001) | 0.347*** (0.022; p<0.001) | 0.212** (0.091; p=0.020) |
| ln hourly wage | (E) mother's unemployment share only | 0.029 | 0.538*** (0.115; p<0.001) | 0.354*** (0.022; p<0.001) | 0.185 (0.117; p=0.115) |
| ln hourly wage | (F) father's closures + layoffs | 0.030 | 0.553*** (0.123; p<0.001) | 0.353*** (0.022; p<0.001) | 0.199 (0.125; p=0.111) |
| ln family income | (A) 74's set: father displaced / unemployed / zero hours, mother unemployed / zero hours | 0.186 | 0.674*** (0.064; p<0.001) | 0.387*** (0.031; p<0.001) | 0.287*** (0.068; p<0.001) |
| ln family income | (B) father's plant closures only | 0.004 | 0.404 (0.687; p=0.557) | 0.441*** (0.029; p<0.001) | -0.037 (0.688; p=0.957) |
| ln family income | (C) father's layoffs / firings only | 0.027 | 0.815*** (0.162; p<0.001) | 0.430*** (0.029; p<0.001) | 0.385** (0.165; p=0.020) |
| ln family income | (D) father's unemployment share only | 0.059 | 0.850*** (0.125; p<0.001) | 0.415*** (0.028; p<0.001) | 0.434*** (0.126; p<0.001) |
| ln family income | (E) mother's unemployment share only | 0.029 | 0.740*** (0.152; p<0.001) | 0.432*** (0.030; p<0.001) | 0.308** (0.154; p=0.046) |
| ln family income | (F) father's closures + layoffs | 0.029 | 0.773*** (0.171; p<0.001) | 0.431*** (0.029; p<0.001) | 0.342** (0.174; p=0.050) |

