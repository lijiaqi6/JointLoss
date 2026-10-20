# First stage: local slack at a birth and mothers' work (8.FirstStage.py)

Each column is one regression (outcome in the header); regressors as rows; panels = separate regressions. Linear probability models with state and birth-year FE; controls: mother's age and age^2, education (<12, 13-15, 16+, missing; base 12), Black, married at birth, birth order (2, 3+, missing). Cell: coefficient, stars, (s.e. clustered by state; p-value); second line: s.e. clustered by mother. *** p<0.01, ** p<0.05, * p<0.1. Unemployment rate in percentage points; Bartik = predicted employment growth in % (higher = tighter). The search friction predicts + on the unemployment rate and - on bartik_f (women's-industry slack -> more mothers keep working).

### Table 1. Mothers employed in the year before the birth

| | Employed b+1 | Employed b+2 | Employed b+3 | Employed 500+ h b+1 |
|---|---|---|---|---|
| **A. State unemployment rate (LAUS, %), birth year** | | | | |
| ur | -0.0147** (0.0060; p=0.014)<br><sub>mother-cl. (0.0048; p=0.002)</sub> | -0.0094 (0.0065; p=0.150)<br><sub>mother-cl. (0.0050; p=0.058)</sub> | -0.0145*** (0.0056; p=0.010)<br><sub>mother-cl. (0.0052; p=0.005)</sub> | -0.0122** (0.0061; p=0.047)<br><sub>mother-cl. (0.0053; p=0.022)</sub> |
| N | 8,458 | 7,964 | 7,594 | 8,402 |
| Women | 5,409 | 5,104 | 4,883 | 5,394 |
| State clusters | 51 | 51 | 51 | 51 |
| Mean outcome | 0.797 | 0.803 | 0.805 | 0.689 |
| **B. Bartik, leave-one-out (women's and men's industries, jointly)** | | | | |
| bartik_f | 0.0380* (0.0208; p=0.068)<br><sub>mother-cl. (0.0198; p=0.055)</sub> | 0.0165 (0.0225; p=0.464)<br><sub>mother-cl. (0.0193; p=0.393)</sub> | 0.0348* (0.0194; p=0.073)<br><sub>mother-cl. (0.0189; p=0.065)</sub> | 0.0199 (0.0206; p=0.333)<br><sub>mother-cl. (0.0221; p=0.368)</sub> |
| bartik_m | -0.0113 (0.0155; p=0.465)<br><sub>mother-cl. (0.0149; p=0.446)</sub> | -0.0188 (0.0146; p=0.198)<br><sub>mother-cl. (0.0145; p=0.195)</sub> | -0.0293* (0.0164; p=0.074)<br><sub>mother-cl. (0.0149; p=0.048)</sub> | -0.0310 (0.0222; p=0.162)<br><sub>mother-cl. (0.0166; p=0.061)</sub> |
| N | 7,599 | 7,258 | 7,030 | 7,551 |
| Women | 4,930 | 4,712 | 4,563 | 4,916 |
| State clusters | 51 | 51 | 51 | 51 |
| Mean outcome | 0.803 | 0.809 | 0.813 | 0.699 |
| **C. Bartik, national growth incl. own state** | | | | |
| bartik_f_nat | 0.0372 (0.0228; p=0.104)<br><sub>mother-cl. (0.0214; p=0.083)</sub> | 0.0073 (0.0232; p=0.752)<br><sub>mother-cl. (0.0207; p=0.723)</sub> | 0.0336 (0.0221; p=0.127)<br><sub>mother-cl. (0.0203; p=0.098)</sub> | 0.0151 (0.0234; p=0.518)<br><sub>mother-cl. (0.0239; p=0.527)</sub> |
| bartik_m_nat | -0.0024 (0.0181; p=0.892)<br><sub>mother-cl. (0.0156; p=0.876)</sub> | -0.0136 (0.0156; p=0.384)<br><sub>mother-cl. (0.0154; p=0.377)</sub> | -0.0211 (0.0177; p=0.232)<br><sub>mother-cl. (0.0155; p=0.175)</sub> | -0.0215 (0.0240; p=0.370)<br><sub>mother-cl. (0.0173; p=0.214)</sub> |
| N | 7,599 | 7,258 | 7,030 | 7,551 |
| Women | 4,930 | 4,712 | 4,563 | 4,916 |
| State clusters | 51 | 51 | 51 | 51 |
| Mean outcome | 0.803 | 0.809 | 0.813 | 0.699 |
| **D. Bartik, rolling lagged shares** | | | | |
| bartik_f_lag | 0.0419 (0.0317; p=0.186)<br><sub>mother-cl. (0.0248; p=0.091)</sub> | 0.0313 (0.0261; p=0.232)<br><sub>mother-cl. (0.0242; p=0.197)</sub> | 0.0377 (0.0291; p=0.195)<br><sub>mother-cl. (0.0242; p=0.120)</sub> | 0.0250 (0.0276; p=0.365)<br><sub>mother-cl. (0.0282; p=0.374)</sub> |
| bartik_m_lag | -0.0018 (0.0227; p=0.936)<br><sub>mother-cl. (0.0191; p=0.924)</sub> | -0.0133 (0.0179; p=0.458)<br><sub>mother-cl. (0.0183; p=0.469)</sub> | -0.0284 (0.0229; p=0.215)<br><sub>mother-cl. (0.0189; p=0.132)</sub> | -0.0310 (0.0294; p=0.292)<br><sub>mother-cl. (0.0210; p=0.140)</sub> |
| N | 7,599 | 7,258 | 7,030 | 7,551 |
| Women | 4,930 | 4,712 | 4,563 | 4,916 |
| State clusters | 51 | 51 | 51 | 51 |
| Mean outcome | 0.803 | 0.809 | 0.813 | 0.699 |
| **E. Unemployment rate x Black** | | | | |
| ur | -0.0153** (0.0069; p=0.027)<br><sub>mother-cl. (0.0052; p=0.003)</sub> | -0.0107 (0.0070; p=0.123)<br><sub>mother-cl. (0.0055; p=0.051)</sub> | -0.0142** (0.0059; p=0.016)<br><sub>mother-cl. (0.0056; p=0.011)</sub> | -0.0139** (0.0071; p=0.049)<br><sub>mother-cl. (0.0058; p=0.017)</sub> |
| ur x black | 0.0012 (0.0045; p=0.786)<br><sub>mother-cl. (0.0046; p=0.790)</sub> | 0.0031 (0.0038; p=0.412)<br><sub>mother-cl. (0.0048; p=0.516)</sub> | -0.0008 (0.0043; p=0.853)<br><sub>mother-cl. (0.0050; p=0.873)</sub> | 0.0039 (0.0044; p=0.378)<br><sub>mother-cl. (0.0052; p=0.456)</sub> |
| N | 8,458 | 7,964 | 7,594 | 8,402 |
| Women | 5,409 | 5,104 | 4,883 | 5,394 |
| State clusters | 51 | 51 | 51 | 51 |
| Mean outcome | 0.797 | 0.803 | 0.805 | 0.689 |
| **F. Bartik x Black** | | | | |
| bartik_f | 0.0388* (0.0199; p=0.051)<br><sub>mother-cl. (0.0203; p=0.056)</sub> | 0.0202 (0.0219; p=0.357)<br><sub>mother-cl. (0.0198; p=0.308)</sub> | 0.0353* (0.0206; p=0.087)<br><sub>mother-cl. (0.0195; p=0.070)</sub> | 0.0146 (0.0204; p=0.475)<br><sub>mother-cl. (0.0226; p=0.519)</sub> |
| bartik_m | -0.0119 (0.0149; p=0.426)<br><sub>mother-cl. (0.0152; p=0.434)</sub> | -0.0215 (0.0146; p=0.142)<br><sub>mother-cl. (0.0149; p=0.148)</sub> | -0.0300* (0.0170; p=0.077)<br><sub>mother-cl. (0.0153; p=0.050)</sub> | -0.0303 (0.0215; p=0.159)<br><sub>mother-cl. (0.0169; p=0.072)</sub> |
| bartik_f x black | -0.0021 (0.0104; p=0.843)<br><sub>mother-cl. (0.0107; p=0.847)</sub> | -0.0085 (0.0085; p=0.315)<br><sub>mother-cl. (0.0104; p=0.411)</sub> | -0.0008 (0.0119; p=0.949)<br><sub>mother-cl. (0.0108; p=0.944)</sub> | 0.0153 (0.0115; p=0.184)<br><sub>mother-cl. (0.0123; p=0.215)</sub> |
| bartik_m x black | 0.0017 (0.0074; p=0.812)<br><sub>mother-cl. (0.0090; p=0.845)</sub> | 0.0085 (0.0072; p=0.237)<br><sub>mother-cl. (0.0090; p=0.343)</sub> | 0.0019 (0.0093; p=0.841)<br><sub>mother-cl. (0.0089; p=0.834)</sub> | -0.0026 (0.0095; p=0.780)<br><sub>mother-cl. (0.0104; p=0.799)</sub> |
| N | 7,599 | 7,258 | 7,030 | 7,551 |
| Women | 4,930 | 4,712 | 4,563 | 4,916 |
| State clusters | 51 | 51 | 51 | 51 |
| Mean outcome | 0.803 | 0.809 | 0.813 | 0.699 |
| **G. Unemployment rate x married at birth** | | | | |
| ur | -0.0137** (0.0063; p=0.031)<br><sub>mother-cl. (0.0060; p=0.022)</sub> | -0.0090 (0.0061; p=0.137)<br><sub>mother-cl. (0.0061; p=0.141)</sub> | -0.0163*** (0.0062; p=0.008)<br><sub>mother-cl. (0.0065; p=0.012)</sub> | -0.0134** (0.0064; p=0.036)<br><sub>mother-cl. (0.0068; p=0.049)</sub> |
| ur x married | -0.0015 (0.0037; p=0.682)<br><sub>mother-cl. (0.0049; p=0.759)</sub> | -0.0005 (0.0055; p=0.921)<br><sub>mother-cl. (0.0051; p=0.915)</sub> | 0.0023 (0.0065; p=0.719)<br><sub>mother-cl. (0.0053; p=0.656)</sub> | 0.0016 (0.0054; p=0.766)<br><sub>mother-cl. (0.0056; p=0.774)</sub> |
| N | 8,458 | 7,964 | 7,594 | 8,402 |
| Women | 5,409 | 5,104 | 4,883 | 5,394 |
| State clusters | 51 | 51 | 51 | 51 |
| Mean outcome | 0.797 | 0.803 | 0.805 | 0.689 |
| **H. Bartik x married at birth** | | | | |
| bartik_f | 0.0250 (0.0227; p=0.270)<br><sub>mother-cl. (0.0213; p=0.241)</sub> | -0.0024 (0.0244; p=0.921)<br><sub>mother-cl. (0.0208; p=0.908)</sub> | 0.0201 (0.0188; p=0.285)<br><sub>mother-cl. (0.0203; p=0.322)</sub> | 0.0087 (0.0203; p=0.668)<br><sub>mother-cl. (0.0242; p=0.718)</sub> |
| bartik_m | 0.0009 (0.0159; p=0.954)<br><sub>mother-cl. (0.0164; p=0.955)</sub> | -0.0015 (0.0158; p=0.922)<br><sub>mother-cl. (0.0162; p=0.924)</sub> | -0.0146 (0.0171; p=0.393)<br><sub>mother-cl. (0.0161; p=0.365)</sub> | -0.0150 (0.0239; p=0.529)<br><sub>mother-cl. (0.0185; p=0.416)</sub> |
| bartik_f x married | 0.0196* (0.0109; p=0.071)<br><sub>mother-cl. (0.0120; p=0.103)</sub> | 0.0286** (0.0132; p=0.030)<br><sub>mother-cl. (0.0120; p=0.017)</sub> | 0.0226** (0.0114; p=0.048)<br><sub>mother-cl. (0.0123; p=0.067)</sub> | 0.0172 (0.0132; p=0.194)<br><sub>mother-cl. (0.0138; p=0.213)</sub> |
| bartik_m x married | -0.0179* (0.0097; p=0.065)<br><sub>mother-cl. (0.0100; p=0.074)</sub> | -0.0247** (0.0112; p=0.027)<br><sub>mother-cl. (0.0104; p=0.017)</sub> | -0.0217** (0.0109; p=0.046)<br><sub>mother-cl. (0.0101; p=0.031)</sub> | -0.0240** (0.0122; p=0.049)<br><sub>mother-cl. (0.0115; p=0.037)</sub> |
| N | 7,599 | 7,258 | 7,030 | 7,551 |
| Women | 4,930 | 4,712 | 4,563 | 4,916 |
| State clusters | 51 | 51 | 51 | 51 |
| Mean outcome | 0.803 | 0.809 | 0.813 | 0.699 |
| State FE, birth-year FE | yes | yes | yes | yes |

### Table 2. Placebos

| | (i) Childless women, employed t+1 | (ii) Shock at b-2: employed b+1 | (iii) Not employed at b-1: employed b+1 | (iii) Not employed at b-1: employed b+2 |
|---|---|---|---|---|
| **A. State unemployment rate (LAUS, %)** | | | | |
| ur | -0.0025 (0.0017; p=0.149)<br><sub>mother-cl. (0.0016; p=0.128)</sub> | -0.0106* (0.0058; p=0.066)<br><sub>mother-cl. (0.0049; p=0.030)</sub> | -0.0153** (0.0069; p=0.028)<br><sub>mother-cl. (0.0090; p=0.088)</sub> | -0.0083 (0.0066; p=0.207)<br><sub>mother-cl. (0.0098; p=0.399)</sub> |
| N | 23,581 | 8,282 | 2,436 | 2,309 |
| Women | 4,500 | 5,311 | 1,740 | 1,662 |
| State clusters | 51 | 51 | 49 | 49 |
| Mean outcome | 0.961 | 0.799 | 0.303 | 0.356 |
| **B. Bartik, leave-one-out (jointly)** | | | | |
| bartik_f | 0.0048 (0.0047; p=0.307)<br><sub>mother-cl. (0.0055; p=0.388)</sub> | -0.0024 (0.0223; p=0.916)<br><sub>mother-cl. (0.0195; p=0.903)</sub> | -0.0506* (0.0305; p=0.098)<br><sub>mother-cl. (0.0425; p=0.234)</sub> | -0.0722* (0.0418; p=0.084)<br><sub>mother-cl. (0.0445; p=0.104)</sub> |
| bartik_m | 0.0018 (0.0040; p=0.656)<br><sub>mother-cl. (0.0043; p=0.684)</sub> | -0.0374** (0.0147; p=0.011)<br><sub>mother-cl. (0.0147; p=0.011)</sub> | 0.0071 (0.0330; p=0.831)<br><sub>mother-cl. (0.0321; p=0.826)</sub> | 0.0312 (0.0393; p=0.428)<br><sub>mother-cl. (0.0357; p=0.383)</sub> |
| N | 21,027 | 7,435 | 2,082 | 1,990 |
| Women | 4,137 | 4,825 | 1,498 | 1,443 |
| State clusters | 51 | 51 | 49 | 49 |
| Mean outcome | 0.962 | 0.811 | 0.295 | 0.361 |
| State FE, birth-year FE | yes | yes | yes | yes |

(i) woman-years t of women with a childbirth history and no birth up to t+1, aged 19-39, employed in t-1; shock in t. (ii) mothers employed at b-1, shock measured two years before the birth. (iii) mothers not employed at b-1.

## Sample

| step | births |
|---|---|
| births 1977-2021 to SRC/SEO women (twins once) | 21,613 |
|   head's race White or Black | 16,113 |
|   mother aged 15-49 | 16,078 |
|   state observed | 15,815 |
|   employment in year before birth observed (head / wife) | 12,061 |
|   employed in year before birth | 9,323 |
|   ... and employment at b+1 observed | 8,597 |

Childless placebo: 23,689 woman-years, 4,511 women.
Education variables used: 30. PSID->FIPS state check (1999): 0.9954.

## Mothers employed at b-1, by birth year (shares)

|   year |   all_births |   emp_before |   births |   emp_p1 |   emp_p2 |   emp_p3 |   black |   married |      ur |
|-------:|-------------:|-------------:|---------:|---------:|---------:|---------:|--------:|----------:|--------:|
|   1977 |          367 |        0.648 |      186 |    0.703 |    0.714 |    0.706 |   0.339 |     0.856 |   6.695 |
|   1978 |          373 |        0.665 |      183 |    0.705 |    0.737 |    0.749 |   0.355 |     0.865 |   5.886 |
|   1979 |          412 |        0.72  |      237 |    0.672 |    0.691 |    0.69  |   0.388 |     0.884 |   5.644 |
|   1980 |          421 |        0.704 |      243 |    0.702 |    0.712 |    0.755 |   0.395 |     0.849 |   7.415 |
|   1981 |          401 |        0.699 |      225 |    0.716 |    0.735 |    0.757 |   0.373 |     0.837 |   7.677 |
|   1982 |          410 |        0.695 |      228 |    0.764 |    0.805 |    0.808 |   0.355 |     0.822 |   9.867 |
|   1983 |          430 |        0.695 |      228 |    0.818 |    0.741 |    0.778 |   0.377 |     0.866 |   9.658 |
|   1984 |          462 |        0.662 |      239 |    0.787 |    0.829 |    0.833 |   0.36  |     0.87  |   7.646 |
|   1985 |          389 |        0.775 |      241 |    0.722 |    0.765 |    0.758 |   0.349 |     0.835 |   7.357 |
|   1986 |          418 |        0.751 |      250 |    0.761 |    0.806 |    0.807 |   0.348 |     0.809 |   6.914 |
|   1987 |          420 |        0.752 |      243 |    0.826 |    0.839 |    0.85  |   0.35  |     0.833 |   6.31  |
|   1988 |          390 |        0.799 |      250 |    0.807 |    0.788 |    0.842 |   0.316 |     0.771 |   5.586 |
|   1989 |          378 |        0.801 |      229 |    0.779 |    0.792 |    0.777 |   0.288 |     0.834 |   5.235 |
|   1990 |          397 |        0.804 |      229 |    0.797 |    0.792 |    0.763 |   0.362 |     0.79  |   5.658 |
|   1991 |          379 |        0.805 |      236 |    0.776 |    0.756 |    0.812 |   0.335 |     0.762 |   6.68  |
|   1992 |          400 |        0.775 |      214 |    0.811 |    0.802 |    0.793 |   0.322 |     0.857 |   7.171 |
|   1993 |          429 |        0.812 |      234 |    0.772 |    0.809 |    0.799 |   0.338 |     0.761 |   6.749 |
|   1994 |          372 |        0.81  |      218 |    0.785 |    0.806 |  nan     |   0.307 |     0.762 |   5.84  |
|   1995 |          372 |        0.766 |      209 |    0.808 |  nan     |    0.819 |   0.359 |     0.728 |   5.388 |
|   1996 |          321 |        0.81  |      200 |  nan     |    0.846 |  nan     |   0.24  |     0.787 |   5.141 |
|   1997 |          273 |        0.844 |      157 |    0.793 |  nan     |    0.816 |   0.382 |     0.667 |   4.745 |
|   1998 |          275 |      nan     |      nan |  nan     |  nan     |  nan     | nan     |   nan     | nan     |
|   1999 |          272 |        0.787 |      166 |    0.868 |    0.785 |    0.854 |   0.319 |     0.722 |   4.035 |
|   2000 |          297 |      nan     |      nan |  nan     |  nan     |  nan     | nan     |   nan     | nan     |
|   2001 |          271 |        0.862 |      188 |    0.777 |    0.781 |    0.82  |   0.271 |     0.717 |   4.612 |
|   2002 |          319 |        0.793 |      199 |    0.778 |    0.881 |    0.761 |   0.417 |     0.653 |   5.716 |
|   2003 |          300 |        0.797 |      188 |    0.815 |    0.809 |    0.855 |   0.383 |     0.69  |   5.982 |
|   2004 |          354 |        0.785 |      233 |    0.787 |    0.842 |    0.772 |   0.33  |     0.678 |   5.566 |
|   2005 |          361 |        0.855 |      247 |    0.847 |    0.786 |    0.821 |   0.316 |     0.706 |   5.352 |
|   2006 |          376 |        0.78  |      238 |    0.803 |    0.86  |    0.816 |   0.361 |     0.637 |   4.839 |
|   2007 |          366 |        0.821 |      234 |    0.893 |    0.805 |    0.833 |   0.321 |     0.688 |   4.604 |
|   2008 |          361 |        0.809 |      250 |    0.784 |    0.823 |    0.814 |   0.348 |     0.577 |   5.779 |
|   2009 |          371 |        0.831 |      246 |    0.831 |    0.807 |    0.812 |   0.354 |     0.671 |   9.162 |
|   2010 |          371 |        0.749 |      227 |    0.823 |    0.833 |    0.824 |   0.401 |     0.625 |   9.564 |
|   2011 |          304 |        0.797 |      200 |    0.865 |    0.831 |    0.848 |   0.405 |     0.619 |   8.708 |
|   2012 |          349 |        0.768 |      225 |    0.799 |    0.834 |    0.845 |   0.458 |     0.644 |   7.827 |
|   2013 |          304 |        0.766 |      196 |    0.822 |    0.793 |    0.828 |   0.337 |     0.662 |   7.282 |
|   2014 |          353 |        0.78  |      238 |    0.818 |    0.836 |    0.797 |   0.454 |     0.524 |   6.154 |
|   2015 |          310 |        0.856 |      226 |    0.829 |    0.825 |    0.864 |   0.363 |     0.612 |   5.115 |
|   2016 |          322 |        0.749 |      203 |    0.843 |    0.89  |    0.86  |   0.394 |     0.645 |   4.823 |
|   2017 |          296 |        0.843 |      204 |    0.894 |    0.832 |    0.816 |   0.402 |     0.584 |   4.297 |
|   2018 |          316 |        0.818 |      224 |    0.854 |    0.864 |    0.831 |   0.438 |     0.62  |   3.875 |
|   2019 |          264 |        0.851 |      194 |    0.773 |    0.777 |    0.788 |   0.418 |     0.605 |   3.676 |
|   2020 |          253 |        0.703 |      156 |    0.872 |    0.879 |  nan     |   0.385 |     0.636 |   7.908 |
|   2021 |          236 |        0.822 |      162 |    0.84  |  nan     |  nan     |   0.377 |     0.658 |   5.111 |

## Employment panel sources (woman-years)

| src                 |      n |   share_emp |   first |   last |
|:--------------------|-------:|------------:|--------:|-------:|
| WTR EMPLOYED IN w-2 |  73941 |       0.706 |    2001 |   2021 |
| annual hours        | 220041 |       0.684 |    1975 |   2022 |
