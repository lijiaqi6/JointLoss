# Age or period? The son's tested skill in the NLSY97 IGE (Fable D1)

Built by `94.NLSY97AFQT.py` (2026-10-20); design in its docstring. NLSY97 sons born 1980-84, Black and White pooled with round weights; exact Gelbach split of the earnings IGE by band, A = 85's groups, B = A + the son's AFQT (ASVAB math-verbal percentile, standardised within birth year); estimate (s.e.; p) from 200 cluster-bootstrap draws of 1997 households; *** p<0.01, ** p<0.05, * p<0.1. **Descriptive accounting.**

AFQT observed for 84% of the youths.

## ln own earnings, sons

| row | 25-29 | 30-34 | 35-39 | 40-44 | 25-44 | opening 35-39 - 25-29 | opening 40-44 - 25-29 |
|---|---|---|---|---|---|---|---|
| IGE | 0.175*** (0.021; p<0.001) | 0.213*** (0.023; p<0.001) | 0.241*** (0.024; p<0.001) | 0.258*** (0.027; p<0.001) | 0.211*** (0.019; p<0.001) | 0.067*** (0.024; p=0.006) | 0.083*** (0.027; p=0.002) |
| son's AFQT (split B) | 0.033*** (0.006; p<0.001) | 0.035*** (0.007; p<0.001) | 0.042*** (0.007; p<0.001) | 0.054*** (0.010; p<0.001) | 0.038*** (0.006; p<0.001) | 0.009 (0.006; p=0.128) | 0.021** (0.010; p=0.027) |
| transfers + parents' schooling, split A | 0.020 (0.013; p=0.119) | 0.034** (0.014; p=0.013) | 0.048*** (0.016; p=0.003) | 0.033** (0.016; p=0.040) | 0.031*** (0.011; p=0.006) | 0.028* (0.016; p=0.075) | 0.013 (0.017; p=0.439) |
| transfers + parents' schooling, split B | 0.001 (0.013; p=0.938) | 0.013 (0.014; p=0.324) | 0.023 (0.016; p=0.159) | 0.007 (0.017; p=0.657) | 0.009 (0.011; p=0.408) | 0.022 (0.015; p=0.152) | 0.006 (0.017; p=0.714) |
| rest, split A | 0.129*** (0.031; p<0.001) | 0.161*** (0.034; p<0.001) | 0.192*** (0.038; p<0.001) | 0.179*** (0.044; p<0.001) | 0.159*** (0.028; p<0.001) | 0.063* (0.037; p=0.084) | 0.050 (0.043; p=0.241) |
| rest, split B | 0.113*** (0.031; p<0.001) | 0.145*** (0.034; p<0.001) | 0.171*** (0.038; p<0.001) | 0.152*** (0.044; p<0.001) | 0.141*** (0.028; p<0.001) | 0.058 (0.036; p=0.111) | 0.039 (0.041; p=0.344) |

Share of the 25-44 IGE carried by the son's AFQT: 0.182*** (0.031; p<0.001). Sons / son-years 25-44: 2,190 / 15,164.

## ln hourly wage, sons

| row | 25-29 | 30-34 | 35-39 | 40-44 | 25-44 | opening 35-39 - 25-29 | opening 40-44 - 25-29 |
|---|---|---|---|---|---|---|---|
| IGE | 0.161*** (0.016; p<0.001) | 0.191*** (0.019; p<0.001) | 0.221*** (0.021; p<0.001) | 0.228*** (0.027; p<0.001) | 0.191*** (0.015; p<0.001) | 0.059*** (0.020; p=0.004) | 0.067** (0.027; p=0.013) |
| son's AFQT (split B) | 0.026*** (0.005; p<0.001) | 0.030*** (0.006; p<0.001) | 0.049*** (0.007; p<0.001) | 0.055*** (0.009; p<0.001) | 0.036*** (0.005; p<0.001) | 0.023*** (0.006; p<0.001) | 0.029*** (0.009; p=0.001) |
| transfers + parents' schooling, split A | 0.028*** (0.010; p=0.005) | 0.038*** (0.011; p<0.001) | 0.045*** (0.013; p<0.001) | 0.038** (0.016; p=0.016) | 0.035*** (0.009; p<0.001) | 0.018 (0.012; p=0.141) | 0.011 (0.016; p=0.490) |
| transfers + parents' schooling, split B | 0.013 (0.010; p=0.189) | 0.020* (0.011; p=0.066) | 0.016 (0.013; p=0.215) | 0.011 (0.016; p=0.489) | 0.014 (0.009; p=0.103) | 0.004 (0.012; p=0.757) | -0.001 (0.017; p=0.938) |
| rest, split A | 0.124*** (0.023; p<0.001) | 0.156*** (0.027; p<0.001) | 0.193*** (0.031; p<0.001) | 0.162*** (0.041; p<0.001) | 0.154*** (0.021; p<0.001) | 0.069** (0.030; p=0.022) | 0.039 (0.040; p=0.330) |
| rest, split B | 0.111*** (0.023; p<0.001) | 0.141*** (0.026; p<0.001) | 0.168*** (0.030; p<0.001) | 0.135*** (0.040; p<0.001) | 0.136*** (0.021; p<0.001) | 0.056* (0.030; p=0.057) | 0.024 (0.038; p=0.530) |

Share of the 25-44 IGE carried by the son's AFQT: 0.188*** (0.026; p<0.001). Sons / son-years 25-44: 2,190 / 15,164.

## NLSY79 (87) keys holding the AFQT contribution, for the same-band comparison

sons|pooled|father's schooling element, B (with AFQT); sons|pooled|son's AFQT, B; sons|White|father's schooling element, B (with AFQT); sons|White|son's AFQT, B; sons|Black|father's schooling element, B (with AFQT); sons|Black|son's AFQT, B; daughters|pooled|father's schooling element, B (with AFQT); daughters|pooled|son's AFQT, B; daughters|White|father's schooling element, B (with AFQT); daughters|White|son's AFQT, B; daughters|Black|father's schooling element, B (with AFQT); daughters|Black|son's AFQT, B

