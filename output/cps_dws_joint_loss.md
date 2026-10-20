# Joint displacement of spouses: CPS Displaced Worker Supplement 1984-2024

Script `IGE/39.CPSDisplacedWorkers.py` (2026-10-17). Data: IPUMS CPS extract of the 21 biennial Displaced Worker Supplements (January 1984-1992, February 1994-2000, January 2002-2024), persons married with spouse present; raw files in `IGE/data/ext/cps_dws/`. Stars: \*\*\* p<0.01, \*\* p<0.05, \* p<0.1; cells are estimate (s.e.; p). Associations, not causal effects.

**Measure.** *Displaced* = lost a wage job in the last three calendar years because the plant or company closed or moved, there was insufficient work, or the position or shift was abolished (the BLS definition; IPUMS DWSTAT = 1 from 1994; 1984-1992 harmonised from the five-year window: reasons 1-3, not self-employed, lost 1-3 calendar years before the survey). The comparison group is always couples whose husband was **not displaced**. *Respondent / recall:* the CPS accepts proxy answers from any responsible household member, so both spouses' supplement answers usually come from one respondent at one interview (the extract carries no self / proxy flag, so the two cannot be separated); recall covers three calendar years with the year of loss in whole years, and only one lost job per person (the longest held). Couples are observed married at the survey, so couples who split after a displacement are missing.

## 0. Sample

| Step | N |
|---|---|
| persons in extract (MARST 1) | 1,180,291 |
| persons in the 21 DWS months | 1,180,291 |
| couples (husband and wife name each other) | 589,435 |
| both aged 20-64 | 459,568 |
|   husband not in supplement (DWSTAT 99) | 38,954 |
|   wife not in supplement (DWSTAT 99) | 32,871 |
| both in supplement | 417,374 |
| displacement known for both (analysis sample) | 417,269 |


Attached couples (each spouse displaced, employed or unemployed at the survey): 276,923. Couple x calendar-year panel (Y-3..Y-1; couples with a displaced spouse of unknown year dropped): 1,250,757 couple-years.

| Survey | Couples | Husband displaced (wtd) | Wife displaced (wtd) | P(w disp | h disp) | P(w disp | h not) | Husbands displaced (N) | Both displaced (N) | Recall window |
|---|---|---|---|---|---|---|---|---|
| 1984 | 26,856 | 0.0766 | 0.0389 | 0.0708 | 0.0363 | 2,032 | 150 | recession |
| 1986 | 26,113 | 0.0600 | 0.0337 | 0.0776 | 0.0309 | 1,543 | 110 | expansion |
| 1988 | 25,652 | 0.0564 | 0.0311 | 0.0642 | 0.0292 | 1,439 | 104 | expansion |
| 1990 | 25,306 | 0.0457 | 0.0295 | 0.0679 | 0.0277 | 1,121 | 88 | expansion |
| 1992 | 24,726 | 0.0706 | 0.0406 | 0.0867 | 0.0371 | 1,707 | 151 | recession |
| 1994 | 23,485 | 0.0743 | 0.0443 | 0.0862 | 0.0409 | 1,687 | 149 | recession |
| 1996 | 18,378 | 0.0742 | 0.0498 | 0.0867 | 0.0468 | 1,326 | 116 | expansion |
| 1998 | 19,063 | 0.0512 | 0.0374 | 0.0951 | 0.0343 | 992 | 85 | expansion |
| 2000 | 18,867 | 0.0484 | 0.0351 | 0.0866 | 0.0325 | 907 | 79 | expansion |
| 2002 | 21,809 | 0.0636 | 0.0394 | 0.0778 | 0.0368 | 1,326 | 114 | recession |
| 2004 | 21,369 | 0.0730 | 0.0479 | 0.1152 | 0.0426 | 1,477 | 161 | recession |
| 2006 | 20,902 | 0.0496 | 0.0337 | 0.0892 | 0.0308 | 1,017 | 88 | expansion |
| 2008 | 20,078 | 0.0475 | 0.0306 | 0.0742 | 0.0284 | 908 | 65 | expansion |
| 2010 | 19,724 | 0.0955 | 0.0536 | 0.0986 | 0.0488 | 1,800 | 168 | recession |
| 2012 | 18,496 | 0.0780 | 0.0447 | 0.0788 | 0.0419 | 1,386 | 115 | recession |
| 2014 | 17,452 | 0.0542 | 0.0371 | 0.0859 | 0.0343 | 887 | 71 | expansion |
| 2016 | 16,528 | 0.0421 | 0.0269 | 0.0632 | 0.0253 | 692 | 49 | expansion |
| 2018 | 15,199 | 0.0386 | 0.0219 | 0.0375 | 0.0213 | 570 | 24 | expansion |
| 2020 | 14,096 | 0.0332 | 0.0235 | 0.0619 | 0.0221 | 442 | 26 | expansion |
| 2022 | 11,624 | 0.0395 | 0.0300 | 0.0980 | 0.0272 | 432 | 40 | recession |
| 2024 | 11,546 | 0.0317 | 0.0207 | 0.0451 | 0.0199 | 347 | 15 | expansion |


## 1. Wife's displacement given the husband's (weighted by the wife's supplement weight)


**All couples**

| Event (husband -> wife) | P(w | h event) | P(w | h not displaced) | Ratio | Difference (wtd LPM) | N | Husbands with event | Joint events |
|---|---|---|---|---|---|---|---|
| Displaced (any of reasons 1-3) | 0.0815 | 0.0330 | 2.5 | 0.0485*** (0.0021; p<0.001) | 417,269 | 24,038 | 1,968 |
| Plant closed or moved (reason 1), both | 0.0628 | 0.0133 | 4.7 | 0.0495*** (0.0030; p<0.001) | 402,039 | 8,808 | 548 |
| Insufficient work / position abolished (2-3), both | 0.0574 | 0.0197 | 2.9 | 0.0377*** (0.0022; p<0.001) | 408,461 | 15,230 | 862 |
| Wife displaced, husband's plant closed | 0.0931 | 0.0330 | 2.8 | 0.0601*** (0.0036; p<0.001) | 402,039 | 8,808 | 811 |
| Wife plant closing, husband displaced | 0.0338 | 0.0133 | 2.5 | 0.0205*** (0.0013; p<0.001) | 417,269 | 24,038 | 843 |
| Any job loss incl. seasonal / business failed / other (1984-1992) | 0.1051 | 0.0389 | 2.7 | 0.0662*** (0.0035; p<0.001) | 128,623 | 9,840 | 1,058 |
| Same calendar year: displaced (couple-years) | 0.0466 | 0.0109 | 4.3 | 0.0357*** (0.0016; p<0.001) | 1,203,137 | 23,810 | 1,098 |
| Same calendar year: plant closing, both (couple-years) | 0.0432 | 0.0044 | 9.8 | 0.0388*** (0.0026; p<0.001) | 1,188,060 | 8,733 | 371 |


**Attached couples**

| Event (husband -> wife) | P(w | h event) | P(w | h not displaced) | Ratio | Difference (wtd LPM) | N | Husbands with event | Joint events |
|---|---|---|---|---|---|---|---|
| Displaced (any of reasons 1-3) | 0.1096 | 0.0468 | 2.3 | 0.0627*** (0.0027; p<0.001) | 276,923 | 18,042 | 1,968 |
| Plant closed or moved (reason 1), both | 0.0861 | 0.0187 | 4.6 | 0.0674*** (0.0041; p<0.001) | 265,394 | 6,513 | 548 |
| Insufficient work / position abolished (2-3), both | 0.0763 | 0.0281 | 2.7 | 0.0482*** (0.0029; p<0.001) | 270,410 | 11,529 | 862 |
| Wife displaced, husband's plant closed | 0.1276 | 0.0468 | 2.7 | 0.0808*** (0.0048; p<0.001) | 265,394 | 6,513 | 811 |
| Wife plant closing, husband displaced | 0.0454 | 0.0187 | 2.4 | 0.0267*** (0.0018; p<0.001) | 276,923 | 18,042 | 843 |
| Any job loss incl. seasonal / business failed / other (1984-1992) | 0.1319 | 0.0555 | 2.4 | 0.0764*** (0.0047; p<0.001) | 80,535 | 6,921 | 935 |
| Same calendar year: displaced (couple-years) | 0.0625 | 0.0155 | 4.0 | 0.0471*** (0.0021; p<0.001) | 794,202 | 17,880 | 1,098 |
| Same calendar year: plant closing, both (couple-years) | 0.0591 | 0.0062 | 9.5 | 0.0529*** (0.0035; p<0.001) | 782,786 | 6,464 | 371 |


Rows 1-6 use the three-year window (one row per couple); the 'same calendar year' rows use the couple x year panel: the event is displacement in year y for both. Row 6 is limited to 1984-1992, the only surveys that record seasonal, business-failure and other losses with a year.


## 2. LPMs (unweighted; s.e. clustered by household; state-clustered s.e. in the last row)

|  | (1) Wife displaced | (2) Wife displaced | (3) Wife displaced | (4) Wife plant closing | (5) Wife insufficient work / abolished | (6) Wife displaced |
|---|---|---|---|---|---|---|
| **All couples** |  |  |  |  |  |  |
| Husband displaced | 0.049*** (0.002; p<0.001) | 0.046*** (0.002; p<0.001) | 0.044*** (0.002; p<0.001) |  |  | 0.025*** (0.002; p<0.001) |
| Husband plant closing |  |  |  | 0.046*** (0.003; p<0.001) | 0.009*** (0.002; p<0.001) |  |
| Husband insufficient work / position abolished |  |  |  | 0.004*** (0.001; p<0.001) | 0.034*** (0.002; p<0.001) |  |
| Husband displaced x same detailed industry |  |  |  |  |  | 0.399*** (0.014; p<0.001) |
| Same detailed industry |  |  |  |  |  | -0.031*** (0.001; p<0.001) |
| Mean of outcome, husband not displaced | 0.0332 | 0.0332 | 0.0332 | 0.0137 | 0.0195 | 0.0456 |
| Controls (ages, education, race, Hispanic) | no | no | yes | yes | yes | yes |
| State x survey-year FE | no | yes | yes | yes | yes | yes |
| N couples | 417,269 | 417,269 | 417,269 | 417,269 | 417,269 | 276,027 |
| First regressor, s.e. clustered by state | 0.049*** (0.002; p<0.001) | 0.046*** (0.002; p<0.001) | 0.044*** (0.002; p<0.001) | 0.046*** (0.003; p<0.001) | 0.009*** (0.002; p<0.001) | 0.025*** (0.002; p<0.001) |


|  | (1) Wife displaced | (2) Wife displaced | (3) Wife displaced | (4) Wife plant closing | (5) Wife insufficient work / abolished | (6) Wife displaced |
|---|---|---|---|---|---|---|
| **Attached couples** |  |  |  |  |  |  |
| Husband displaced | 0.063*** (0.002; p<0.001) | 0.057*** (0.002; p<0.001) | 0.055*** (0.002; p<0.001) |  |  | 0.025*** (0.002; p<0.001) |
| Husband plant closing |  |  |  | 0.061*** (0.003; p<0.001) | 0.010*** (0.002; p<0.001) |  |
| Husband insufficient work / position abolished |  |  |  | 0.004*** (0.001; p=0.006) | 0.042*** (0.002; p<0.001) |  |
| Husband displaced x same detailed industry |  |  |  |  |  | 0.399*** (0.014; p<0.001) |
| Same detailed industry |  |  |  |  |  | -0.031*** (0.001; p<0.001) |
| Mean of outcome, husband not displaced | 0.0465 | 0.0465 | 0.0465 | 0.0190 | 0.0275 | 0.0456 |
| Controls (ages, education, race, Hispanic) | no | no | yes | yes | yes | yes |
| State x survey-year FE | no | yes | yes | yes | yes | yes |
| N couples | 276,923 | 276,923 | 276,923 | 276,923 | 276,923 | 276,027 |
| First regressor, s.e. clustered by state | 0.063*** (0.003; p<0.001) | 0.057*** (0.003; p<0.001) | 0.055*** (0.003; p<0.001) | 0.061*** (0.003; p<0.001) | 0.010*** (0.002; p<0.001) | 0.025*** (0.002; p<0.001) |


Column (6): sample with a reference industry for both spouses (lost-job industry if displaced, else the current or last job of the employed / unemployed), detailed Census industry code of the survey year; this requires both spouses to be attached, so column (6) is the same regression in both panels.


## 3. Heterogeneity (state x survey-year FE + controls; same-year column: couple x year panel, state x survey x calendar-year FE, also controls the husband's displacement in another year)

|  | (1) Wife displaced | (2) Wife plant closing | (3) Wife displaced in year y |
|---|---|---|---|
| **All couples** |  |  |  |
| Husband's event (displaced / plant closing / displaced in y) | 0.044*** (0.002; p<0.001) | 0.046*** (0.003; p<0.001) | 0.033*** (0.001; p<0.001) |
| Mean of outcome, husband not displaced | 0.0332 | 0.0137 | 0.0110 |
| N | 417,269 | 417,269 | 1,250,757 |
| **Husband Black** |  |  |  |
| Husband's event (displaced / plant closing / displaced in y) | 0.039*** (0.007; p<0.001) | 0.053*** (0.010; p<0.001) | 0.028*** (0.005; p<0.001) |
| Mean of outcome, husband not displaced | 0.0386 | 0.0154 | 0.0127 |
| N | 25,468 | 25,468 | 76,308 |
| **Husband White non-Hispanic** |  |  |  |
| Husband's event (displaced / plant closing / displaced in y) | 0.043*** (0.002; p<0.001) | 0.044*** (0.003; p<0.001) | 0.031*** (0.002; p<0.001) |
| Mean of outcome, husband not displaced | 0.0331 | 0.0137 | 0.0110 |
| N | 330,013 | 330,013 | 989,319 |
| **Survey years 1984-1998** |  |  |  |
| Husband's event (displaced / plant closing / displaced in y) | 0.041*** (0.003; p<0.001) | 0.043*** (0.003; p<0.001) | 0.031*** (0.002; p<0.001) |
| Mean of outcome, husband not displaced | 0.0343 | 0.0160 | 0.0113 |
| N | 189,579 | 189,579 | 568,029 |
| **Survey years 2000-2024** |  |  |  |
| Husband's event (displaced / plant closing / displaced in y) | 0.046*** (0.003; p<0.001) | 0.049*** (0.004; p<0.001) | 0.035*** (0.002; p<0.001) |
| Mean of outcome, husband not displaced | 0.0323 | 0.0118 | 0.0107 |
| N | 227,690 | 227,690 | 682,728 |
| **Recession windows** |  |  |  |
| Husband's event (displaced / plant closing / displaced in y) | 0.045*** (0.003; p<0.001) | 0.050*** (0.004; p<0.001) | 0.034*** (0.002; p<0.001) |
| Mean of outcome, husband not displaced | 0.0387 | 0.0150 | 0.0128 |
| N | 168,089 | 168,089 | 503,751 |
| **Expansion windows** |  |  |  |
| Husband's event (displaced / plant closing / displaced in y) | 0.042*** (0.002; p<0.001) | 0.043*** (0.003; p<0.001) | 0.032*** (0.002; p<0.001) |
| Mean of outcome, husband not displaced | 0.0296 | 0.0129 | 0.0098 |
| N | 249,180 | 249,180 | 747,006 |
| **Attached couples** |  |  |  |
| Husband's event (displaced / plant closing / displaced in y) | 0.055*** (0.002; p<0.001) | 0.061*** (0.003; p<0.001) | 0.043*** (0.002; p<0.001) |
| Mean of outcome, husband not displaced | 0.0465 | 0.0190 | 0.0154 |
| N | 276,923 | 276,923 | 829,962 |
| **Difference: Black - White non-Hispanic** (pooled, H x group) |  |  |  |
| Husband's event x group | -0.001 (0.008; p=0.894) | 0.011 (0.011; p=0.320) | -0.000 (0.006; p=0.957) |
| N | 355,481 | 355,481 | 1,065,627 |
| **Difference: 2000-2024 - 1984-1998** (pooled, H x group) |  |  |  |
| Husband's event x group | 0.004 (0.004; p=0.252) | 0.005 (0.005; p=0.309) | 0.003 (0.003; p=0.274) |
| N | 417,269 | 417,269 | 1,250,757 |
| **Difference: Recession - expansion windows** (pooled, H x group) |  |  |  |
| Husband's event x group | 0.004 (0.004; p=0.305) | 0.007 (0.005; p=0.192) | 0.002 (0.003; p=0.481) |
| N | 417,269 | 417,269 | 1,250,757 |


The outcome in column (2) is the wife's plant closing and the regressor the husband's plant closing (controlling for his other displacement). Recession windows: the three recall years contain >= 2 NBER recession months (surveys 1984, 1992, 1994, 2002, 2004, 2010, 2012, 2022).


## 4. Same calendar year (couple x year panel; state x survey x calendar-year FE + controls)

|  | (1) Wife displaced in year y | (2) Wife plant closing in year y |
|---|---|---|
| **All couples** |  |  |
| Husband displaced in year y | 0.033*** (0.001; p<0.001) |  |
| Husband displaced in another year of the window | 0.005*** (0.001; p<0.001) |  |
| Husband plant closing in year y |  | 0.037*** (0.002; p<0.001) |
| Husband insufficient work / abolished in year y |  | 0.004*** (0.001; p<0.001) |
| Husband plant closing in another year |  | 0.004*** (0.001; p<0.001) |
| Husband insufficient work / abolished, other year |  | 0.000 (0.000; p=0.654) |
| Mean of outcome, husband not displaced | 0.0110 | 0.0045 |
| Controls; state x survey x calendar-year FE | yes | yes |
| N couple-years | 1,250,757 | 1,250,757 |
| First regressor, s.e. clustered by state | 0.033*** (0.002; p<0.001) | 0.037*** (0.002; p<0.001) |


|  | (1) Wife displaced in year y | (2) Wife plant closing in year y |
|---|---|---|
| **Attached couples** |  |  |
| Husband displaced in year y | 0.043*** (0.002; p<0.001) |  |
| Husband displaced in another year of the window | 0.006*** (0.001; p<0.001) |  |
| Husband plant closing in year y |  | 0.050*** (0.003; p<0.001) |
| Husband insufficient work / abolished in year y |  | 0.005*** (0.001; p<0.001) |
| Husband plant closing in another year |  | 0.005*** (0.001; p<0.001) |
| Husband insufficient work / abolished, other year |  | -0.000 (0.001; p=0.738) |
| Mean of outcome, husband not displaced | 0.0154 | 0.0063 |
| Controls; state x survey x calendar-year FE | yes | yes |
| N couple-years | 829,962 | 829,962 |
| First regressor, s.e. clustered by state | 0.043*** (0.002; p<0.001) | 0.050*** (0.003; p<0.001) |



## 5. Same industry

| Couples | N | Share same detailed industry | Random pairing (same survey) | Ratio | Share - benchmark |
|---|---|---|---|---|---|
| Both displaced (any year) | 1,895 | 0.293 | 0.0130 | 22.6 | 0.280*** (0.010; p<0.001) |
| Both displaced, same year | 1,066 | 0.413 | 0.0130 | 31.7 | 0.400*** (0.015; p<0.001) |
| Both plant closings | 522 | 0.548 | 0.0128 | 42.8 | 0.535*** (0.022; p<0.001) |
| Both plant closings, same year | 355 | 0.676 | 0.0129 | 52.6 | 0.663*** (0.025; p<0.001) |
| Context: both employed, current job | 253,443 | 0.149 | 0.0143 | 10.4 | 0.135*** (0.001; p<0.001) |


Random pairing: within each survey, the probability that a displaced husband and a displaced wife drawn independently (weighted) lost jobs in the same detailed industry, averaged over the couples in the row. Lost-job industries of both spouses are coded in the same scheme within a survey.

| Reference industries | P(w disp | h disp) | P(w disp | h not) | Husbands displaced (N) | N |
|---|---|---|---|---|
| same detailed industry | 0.4454 | 0.0202 | 1,229 | 39,057 |
| different industry | 0.0823 | 0.0501 | 16,356 | 236,970 |


### 5b. Tetrachoric correlation of the spouses' events (weighted 2x2; bootstrap s.e., 200 draws)

| Events | Tetrachoric | Joint events (N) | N |
|---|---|---|---|
| Displaced, 3-year window | 0.217*** (0.007; p<0.001) | 1,968 | 417,269 |
| Plant closing, 3-year window | 0.295*** (0.011; p<0.001) | 548 | 417,269 |
| Displaced, same calendar year (couple-years) | 0.260*** (0.007; p<0.001) | 1,098 | 1,250,757 |
| Plant closing, same calendar year (couple-years) | 0.347*** (0.011; p<0.001) | 371 | 1,250,757 |
| Displaced, 3-year window, attached couples | 0.222*** (0.008; p<0.001) | 1,968 | 276,923 |
| Displaced, same year, attached couples | 0.267*** (0.008; p<0.001) | 1,098 | 829,962 |
| Displaced, 3-year window, husband Black | 0.195*** (0.028; p<0.001) | 128 | 25,468 |
| Displaced, 3-year window, husband White NH | 0.210*** (0.008; p<0.001) | 1,502 | 330,013 |


## 6. Joint plant closings (husband's plant closed vs husband not displaced; weighted)

| Wife's outcome | P(w | h plant closing) | P(w | h not displaced) | Ratio | Difference (wtd LPM) | Husbands with closing (N) | Joint events (N) |
|---|---|---|---|---|---|---|
| Wife displaced (any reason 1-3), 3-year window | 0.0931 | 0.0330 | 2.8 | 0.0601*** (0.0036; p<0.001) | 8,808 | 811 |
| Wife plant closing, 3-year window | 0.0628 | 0.0133 | 4.7 | 0.0495*** (0.0030; p<0.001) | 8,808 | 548 |
| Wife displaced in the same year (couple-years) | 0.0558 | 0.0109 | 5.1 | 0.0449*** (0.0029; p<0.001) | 8,733 | 479 |
| Wife plant closing in the same year (couple-years) | 0.0432 | 0.0044 | 9.8 | 0.0388*** (0.0026; p<0.001) | 8,733 | 371 |


Husbands with a plant closing in a known year: 8,727; wife's plant also closed in the same year: 371, of which in the same detailed industry 240 (weighted share of husbands' closings: 2.85%, the closest proxy in the DWS for one closure hitting both; Halla, Schmieder and Weber 2020 find both spouses at the closing plant in 3.5% of Austrian closure households).


## 7. What a joint displacement does to the household at the survey (displaced husbands with a known year; state x survey-year FE + controls)

|  | (1) His weeks without work | (2) He received UI | (3) He is employed now | (4) She is employed now | (5) Neither spouse employed now |
|---|---|---|---|---|---|
| Wife displaced in the same year | -0.183 (0.693; p=0.792) | -0.004 (0.015; p=0.785) | -0.011 (0.014; p=0.402) | -0.101*** (0.015; p<0.001) | 0.088*** (0.011; p<0.001) |
| Wife displaced in another year | -0.705 (0.761; p=0.354) | -0.016 (0.017; p=0.335) | 0.004 (0.015; p=0.804) | -0.090*** (0.017; p<0.001) | 0.041*** (0.011; p<0.001) |
| Mean of outcome, wife not displaced | 14.625 | 0.523 | 0.725 | 0.692 | 0.093 |
| Controls; state x survey-year FE | yes | yes | yes | yes | yes |
| N displaced husbands | 17,642 | 23,284 | 23,810 | 23,810 | 23,810 |


Weeks without work: DWWKSUN (weeks before the next job or to the survey). Employment at the survey is 0-3 years after the loss.


## 8. Comparison with the PSID and the CPS monthly panel

|  | PSID (25.JointJobLoss.py) | CPS monthly 1994-2023 (30) | CPS DWS 1984-2024 (this) |
|---|---|---|---|
| Event | reason job ended: plant closed / laid off / fired | unemployed job loser (layoff, other job loser, temp. job ended), month to month | displaced: plant closed, insufficient work, position abolished |
| Window | couple-year; ev-1..ev+1 | same month | same calendar year / 3 calendar years |
| P(w | h) vs P(w | not h) | 0.102 vs 0.039 per couple-year (ratio 2.6) | 0.0545 vs 0.0054 (ratio 10.1) | same year 0.047 vs 0.0109 (ratio 4.3); 3 years 0.082 vs 0.033 (ratio 2.5) |
| Excess (LPM) | +0.083*** (0.013) ev-1..ev+1 | +0.040*** (0.002), state x month FE | 3 years 0.044*** (0.002; p<0.001); same year 0.033*** (0.001; p<0.001) |
| Tetrachoric | 0.237*** (0.016) (annual 0.200) | phi 0.053 | 3 years 0.217*** (0.007; p<0.001); same year 0.260*** (0.007; p<0.001) |
| Same industry | x same 3-digit industry +0.282*** (0.078) | same detailed industry: P(w|h) 0.230, +0.211*** (0.009) | H x same detailed industry 0.399*** (0.014; p<0.001) |
| Race | B +0.088***, W +0.077*** | H x Black +0.0055 (p=0.309) | H x Black -0.001 (0.008; p=0.894) |


PSID and CPS-monthly numbers from `IGE/EVIDENCE.md` rows 3.16, 3.20, 3.21, 3.24, 3.27, 3.28.
