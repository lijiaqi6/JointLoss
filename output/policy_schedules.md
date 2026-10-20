# Policy schedules by era (IGE/61.PolicySchedules.py, verified version)

2000 dollars (CPI-U, IGE/common.py; 2023-24 BLS). Era value = mean over the era's calendar years; SNAP built month by month from the fiscal-year tables. Sources with URLs: the script's docstring and the comments next to each table. Values marked 'reconstructed' were not found in an official table and follow the statutory rule (listed under 'Unverified').

## Era values written to paperA_model/inputs/schedules_era*.json, verified vs the minimal version

| Parameter | Era 1 new | Era 1 old | Era 2 new | Era 2 old | Era 3 new | Era 3 old |
|---|---:|---:|---:|---:|---:|---:|
| tax chi | -1.2490 | -1.0360 | -1.1108 | -0.8387 | -1.8041 | -0.8607 |
| tax mu | 0.0947 | 0.0853 | 0.0858 | 0.0723 | 0.1077 | 0.0737 |
| EITC n=0 in (annual) | 0.0177 | 0.0177 | 0.0765 | 0.0765 | 0.0816 | 0.0816 |
| EITC n=0 max (annual) | 82 | 82 | 355 | 355 | 396 | 396 |
| EITC n=0 out (annual) | 0.0177 | 0.0177 | 0.0765 | 0.0765 | 0.0816 | 0.0816 |
| EITC n=0 ps_single (annual) | 1340 | 1339 | 5817 | 5811 | 5928 | 5928 |
| EITC n=0 ps_mfj (annual) | 1340 | 1339 | 6678 | 6673 | 9821 | 9821 |
| EITC n=1 in (annual) | 0.1808 | 0.1808 | 0.3400 | 0.3400 | 0.3400 | 0.3400 |
| EITC n=1 max (annual) | 1507 | 1507 | 2369 | 2369 | 2369 | 2369 |
| EITC n=1 out (annual) | 0.1251 | 0.1251 | 0.1598 | 0.1598 | 0.1598 | 0.1598 |
| EITC n=1 ps_single (annual) | 12719 | 12716 | 12790 | 12778 | 12780 | 12780 |
| EITC n=1 ps_mfj (annual) | 12719 | 12716 | 13652 | 13639 | 16673 | 16673 |
| EITC n=2 in (annual) | 0.1917 | 0.1917 | 0.4000 | 0.4000 | 0.4000 | 0.4000 |
| EITC n=2 max (annual) | 1775 | 1775 | 3914 | 3914 | 3914 | 3914 |
| EITC n=2 out (annual) | 0.1349 | 0.1349 | 0.2106 | 0.2106 | 0.2106 | 0.2106 |
| EITC n=2 ps_single (annual) | 12719 | 12716 | 12790 | 12778 | 12780 | 12780 |
| EITC n=2 ps_mfj (annual) | 12719 | 12716 | 13652 | 13639 | 16673 | 16673 |
| EITC n=3 in (annual) | 0.1917 | 0.1917 | 0.4000 | 0.4000 | 0.4500 | 0.4500 |
| EITC n=3 max (annual) | 1775 | 1775 | 3914 | 3914 | 4404 | 4404 |
| EITC n=3 out (annual) | 0.1349 | 0.1349 | 0.2106 | 0.2106 | 0.2106 | 0.2106 |
| EITC n=3 ps_single (annual) | 12719 | 12716 | 12790 | 12778 | 12780 | 12780 |
| EITC n=3 ps_mfj (annual) | 12719 | 12716 | 13652 | 13639 | 16673 | 16673 |
| SNAP max allotment, 1 persons | 130.0 | 129.0 | 130.0 | 129.2 | 144.9 | 143.5 |
| SNAP standard deduction, 1 persons | 150.8 | 147.8 | 126.4 | 127.3 | 110.7 | 111.0 |
| SNAP gross-income limit, 1 persons | 884 | 908 | 897 | 913 | 896 | 911 |
| SNAP max allotment, 2 persons | 238.5 | 236.8 | 238.8 | 237.2 | 266.0 | 263.6 |
| SNAP standard deduction, 2 persons | 150.8 | 147.8 | 126.4 | 127.3 | 110.7 | 111.0 |
| SNAP gross-income limit, 2 persons | 1189 | 1220 | 1207 | 1229 | 1210 | 1230 |
| SNAP max allotment, 3 persons | 342.1 | 339.6 | 342.1 | 340.1 | 381.1 | 378.0 |
| SNAP standard deduction, 3 persons | 150.8 | 147.8 | 126.4 | 127.3 | 110.7 | 111.0 |
| SNAP gross-income limit, 3 persons | 1493 | 1532 | 1516 | 1545 | 1523 | 1549 |
| SNAP max allotment, 4 persons | 434.3 | 430.9 | 434.7 | 431.6 | 483.9 | 479.6 |
| SNAP standard deduction, 4 persons | 150.8 | 147.8 | 127.4 | 129.1 | 117.5 | 117.7 |
| SNAP gross-income limit, 4 persons | 1797 | 1844 | 1826 | 1860 | 1837 | 1868 |
| SNAP max allotment, 5 persons | 516.0 | 512.2 | 516.3 | 513.0 | 574.7 | 570.1 |
| SNAP standard deduction, 5 persons | 150.8 | 147.8 | 136.3 | 138.4 | 137.5 | 137.8 |
| SNAP gross-income limit, 5 persons | 2102 | 2156 | 2135 | 2176 | 2151 | 2188 |
| SNAP max allotment, 6 persons | 619.4 | 614.5 | 619.6 | 615.5 | 689.7 | 684.0 |
| SNAP standard deduction, 6 persons | 150.8 | 147.8 | 146.5 | 148.6 | 157.6 | 157.9 |
| SNAP gross-income limit, 6 persons | 2406 | 2469 | 2445 | 2491 | 2464 | 2507 |
| SNAP asset limit | 2705 | 2705 | 1884 | 1884 | 1541 | 1405 |
| UI cap (monthly) | 1221 | 1203 | 1360 | 1327 | 1348 | 1360 |
| c_min (AFDC/TANF 3 persons) | 511.7 | 481.8 | 389.4 | 366.9 | 329.1 | 320.4 |

UI cap and c_min weights: CPS couples' state distribution (IGE/62; 1994 shares for 1984-93). q_UI = 0.493 (unchanged).

## What changed against the minimal (memory) version

- EITC: rates and maximum credits were correct in every year (CRS, UKCPR agree); phase-out starts corrected:
  - 1996-2002 phase-out start (n >= 1, unmarried): statutory amounts 11,610 ... 13,520 -> indexed 11,650 ... 13,550
  - 1996-2000, 2002 childless phase-out start: 5,280 / 5,430 / 5,570 / 5,670 / 5,770 / 6,150 -> 5,300 / 5,450 / 5,600 / 5,700 / 5,800 / 6,100
  - 2018 MFJ phase-out start: 24,340 / 14,170 -> 24,350 / 14,170
  - 2019 MFJ phase-out start (n >= 1): 24,830 -> 24,820
  - 2015 / 2017 / 2023 childless MFJ start: 13,760 / 13,930 / 16,360 -> 13,750 / 13,930 / 16,370
  - the married-joint supplement is now taken year by year from the Rev. Procs (it differs by $10 between childless and other filers in some years) instead of one 'extra' amount.
- SNAP: the minimal version scaled one remembered four-person series by FY2023 size ratios and interpolated the standard deduction between remembered anchors; now every fiscal year's official allotments and deductions (by size), month-weighted. Four-person maxima that were wrong in the memory table: FY1997 397 (400), FY2000 434 (426), FY2005 506 (499), FY2006 499 (506), FY2009 628 (588 Oct-Mar, 668 Apr-Sep), FY2021 757 (680 Oct-Dec, 782 Jan-Sep); the gross-income test now uses the previous year's guideline (FNS practice) and the asset limit follows the FY2015 / FY2022 / FY2023 increases ($2,250 / $2,500 / $2,750) instead of a constant $2,000.
- Tax: TAXSIM 35 every year (era mean of 13 / 12 / 15 yearly fits) instead of one statutory year per era (1990 / 2003 / 2015) from a coded bracket calculator.
- c_min: state AFDC/TANF maxima weighted by the CPS couples' states, every year, instead of nine remembered median-state anchors.
- UI cap: weighted by the CPS couples' states instead of the unweighted state mean.
- Poverty guidelines: all years verified against ASPE (no change; 2016 now size-specific).

## Unverified or reconstructed (flags)

- SNAP standard deduction FY1988-FY1990 ($102 / $106 / $111): no official table found online; statutory CPI-U-less-food indexing of the verified FY1987 $99 (the same rule reproduces the verified FY1991 and FY1992 amounts).
- SNAP standard deduction FY2003 and FY2005 (sizes 5 and 6+ in FY2003, 6+ in FY2005): 2002 Farm Bill formula (8.31% of the size's poverty-line income standard, $134 minimum); it reproduces FY2004 and FY2006-08.
- SNAP maximum allotments for 5-8 persons in FY1984-86, 1988-91, 1994, 1997-2005: statutory TFP size factors applied to the four-person amount (within $1 of the official tables in the years that have them); 1-4 persons in those years from the UKCPR compilation (it matches FNS exactly in FY2006-24 and the CDSS / FR / Green Book values except FY1993, see docstring).
- EITC 2009 married supplement and 3+ child amounts, 2018 phase-out starts and the 2021 childless (ARPA) parameters are read from IRS Publication 596 (the completed phase-out amounts) because the Rev. Proc. was superseded (2009, 2021) or not downloadable (2018-18): start = completed amount - max / phase-out rate, rounded to $10.
- EITC 1991-93 supplemental young-child and health-insurance credits are not included (as in the minimal version and in CRS's maxima).
- AFDC/TANF maxima: the UKCPR compilation is a secondary source (spot checks: CA / NY / TX / MS 1990 = 694 / 577 / 184 / 120, the Green Book values).
- TAXSIM: federal only (no state income tax), as the plan specifies; 2008 rebates are not in TAXSIM's fiitax; the 2001 rate-reduction credit is not modelled.
- Tax, era 3: 2021 (ARPA fully refundable child credit of $3,000-3,600 a child) is an outlier year (chi -7.69, mu 0.203); the plan's era mean includes it (chi -1.804, mu 0.1077); without 2021: chi -1.804, mu 0.1077 (stored as chi_ex2021 / mu_ex2021, not read by the model). Lead's decision. The refundable additional child tax credit (from 1998; threshold cut to $3,000 by ARRA in 2009) is why every TAXSIM fit is more progressive than the minimal version's non-refundable-only calculator (e.g. 2015: chi -1.88 vs -0.86).

## SNAP four-person maximum: official vs UKCPR (fiscal years with an official table)

|   fy |   official4 |   ukcpr4 |
|-----:|------------:|---------:|
| 1987 |         271 |      271 |
| 1992 |         370 |      370 |
| 1993 |         370 |      370 |
| 1995 |         386 |      386 |
| 1996 |         397 |      397 |
| 2006 |         506 |      506 |
| 2007 |         518 |      518 |
| 2008 |         542 |      542 |
| 2009 |         588 |      588 |
| 2010 |         668 |      668 |
| 2011 |         668 |      668 |
| 2012 |         668 |      668 |
| 2013 |         668 |      668 |
| 2014 |         668 |      632 |
| 2015 |         649 |      649 |
| 2016 |         649 |      649 |
| 2017 |         649 |      649 |
| 2018 |         640 |      640 |
| 2019 |         642 |      642 |
| 2020 |         646 |      646 |
| 2021 |         680 |      680 |
| 2022 |         835 |      835 |
| 2023 |         939 |      939 |
| 2024 |         973 |      973 |

## By calendar year (nominal unless the column says 2000 $; SNAP gross limit, asset limit and UI cap in 2000 $)

|   year |   eitc1_max_nom |   eitc2_max_nom |   eitc3_max_nom |   eitc2_ps_single_nom |   eitc2_ps_mfj_nom |   eitc0_max_nom |   eitc0_ps_mfj_nom |   snap_A4_nom |   snap_D4_nom |   snap_G4 |   snap_asset_limit |   afdc3_nom |   afdc3_median_nom |   afdc3_popw_nom |   ui_cap_month |   ui_cap_month_unweighted |   tax_chi |   tax_mu |   tax_r2 |   tax_avg_rate_40k |
|-------:|----------------:|----------------:|----------------:|----------------------:|-------------------:|----------------:|-------------------:|--------------:|--------------:|----------:|-------------------:|------------:|-------------------:|-----------------:|---------------:|--------------------------:|----------:|---------:|---------:|-------------------:|
|   1984 |             500 |             500 |             500 |                  6000 |               6000 |               0 |                  0 |        255.75 |        90.5   |   1791.61 |            3314.73 |     327.932 |                321 |          329.897 |        1183.44 |                   1170.51 |   -1.7639 |   0.1174 |   0.9987 |             0.1667 |
|   1985 |             550 |             550 |             550 |                  6500 |               6500 |               0 |                  0 |        265    |        95.75  |   1788.02 |            3200.74 |     340.556 |                327 |          342.206 |        1180.55 |                   1176.09 |   -1.7643 |   0.1174 |   0.9987 |             0.1668 |
|   1986 |             550 |             550 |             550 |                  6500 |               6500 |               0 |                  0 |        268.75 |        98.25  |   1828.05 |            3142.34 |     361.867 |                346 |          363.815 |        1200.99 |                   1203.22 |   -1.75   |   0.1169 |   0.9987 |             0.1663 |
|   1987 |             851 |             851 |             851 |                  6920 |               6920 |               0 |                  0 |        275.75 |        99.75  |   1815.22 |            3031.69 |     369.324 |                354 |          371.641 |        1194.6  |                   1194.98 |   -1.3051 |   0.0975 |   0.999  |             0.1524 |
|   1988 |             874 |             874 |             874 |                  9840 |               9840 |               0 |                  0 |        292.5  |       103     |   1784.96 |            2911.24 |     381.685 |                359 |          384.996 |        1191.92 |                   1193.51 |   -1.0333 |   0.0848 |   0.9994 |             0.1552 |
|   1989 |             910 |             910 |             910 |                 10240 |              10240 |               0 |                  0 |        307.75 |       107.25  |   1770.6  |            2777.42 |     389.309 |                360 |          393.101 |        1205.99 |                   1193.05 |   -1.0449 |   0.0855 |   0.9994 |             0.1564 |
|   1990 |             953 |             953 |             953 |                 10730 |              10730 |               0 |                  0 |        336.25 |       112.25  |   1748.68 |            2635.04 |     400.933 |                364 |          405.471 |        1206.75 |                   1181.03 |   -1.0513 |   0.086  |   0.9994 |             0.1591 |
|   1991 |            1192 |            1235 |            1235 |                 11250 |              11250 |               0 |                  0 |        356.5  |       117.5   |   1763.72 |            2528.63 |     404.607 |                367 |          408.875 |        1222.62 |                   1189.52 |   -1.0578 |   0.0863 |   0.9994 |             0.1587 |
|   1992 |            1324 |            1384 |            1384 |                 11840 |              11840 |               0 |                  0 |        370    |       123.25  |   1800.55 |            2454.74 |     400.246 |                372 |          404.11  |        1248.55 |                   1209.72 |   -1.0443 |   0.0855 |   0.9994 |             0.1565 |
|   1993 |            1434 |            1511 |            1511 |                 12200 |              12200 |               0 |                  0 |        371.25 |       128     |   1814.65 |            2383.39 |     396.014 |                364 |          399.349 |        1267.8  |                   1229.95 |   -1.0994 |   0.0882 |   0.9993 |             0.1568 |
|   1994 |            2038 |            2528 |            2528 |                 11000 |              11000 |             306 |               5000 |        377.75 |       131.75  |   1821.06 |            2323.89 |     395.474 |                366 |          398.243 |        1265.38 |                   1232.61 |   -1.1084 |   0.0886 |   0.9993 |             0.1561 |
|   1995 |            2094 |            3110 |            3110 |                 11290 |              11290 |             314 |               5130 |        388.75 |       134.667 |   1823.13 |            2259.84 |     391.338 |                375 |          394.815 |        1255.64 |                   1230.99 |   -1.1064 |   0.0885 |   0.9993 |             0.1564 |
|   1996 |            2152 |            3556 |            3556 |                 11650 |              11650 |             323 |               5300 |        397.75 |       134     |   1815.29 |            2195.03 |     395.547 |                377 |          398.139 |        1248.65 |                   1230.01 |   -1.1081 |   0.0887 |   0.9993 |             0.1569 |
|   1997 |            2210 |            3656 |            3656 |                 11950 |              11950 |             332 |               5450 |        402    |       134     |   1826.34 |            2145.79 |     391.583 |                377 |          392.833 |        1244.38 |                   1232.96 |   -1.0965 |   0.088  |   0.9993 |             0.1561 |
|   1998 |            2271 |            3756 |            3756 |                 12300 |              12300 |             341 |               5600 |        410.75 |       134     |   1848.77 |            2112.88 |     391.562 |                379 |          394.22  |        1279.38 |                   1268.44 |   -1.1059 |   0.0876 |   0.9988 |             0.1345 |
|   1999 |            2312 |            3816 |            3816 |                 12500 |              12500 |             347 |               5700 |        420.75 |       134     |   1849.91 |            2067.23 |     399.26  |                379 |          401.913 |        1287.87 |                   1272.93 |   -1.1202 |   0.0881 |   0.9987 |             0.1301 |
|   2000 |            2353 |            3888 |            3888 |                 12700 |              12700 |             353 |               5800 |        428    |       134     |   1819.5  |            2000    |     403.196 |                379 |          405.852 |        1291.41 |                   1283.18 |   -1.1421 |   0.0893 |   0.9987 |             0.1319 |
|   2001 |            2428 |            4008 |            4008 |                 13100 |              13100 |             364 |               5950 |        438.5  |       134     |   1812.67 |            1944.66 |     408.437 |                403 |          410.701 |        1338.21 |                   1336.16 |   -1.2016 |   0.0903 |   0.9979 |             0.1127 |
|   2002 |            2506 |            4140 |            4140 |                 13550 |              14550 |             376 |               7100 |        455.25 |       134     |   1842.61 |            1914.4  |     415.393 |                421 |          416.954 |        1415.12 |                   1372.29 |   -1.1612 |   0.0884 |   0.9979 |             0.1122 |
|   2003 |            2547 |            4204 |            4204 |                 13730 |              14730 |             382 |               7240 |        466.5  |       134     |   1842.96 |            1871.74 |     417.432 |                396 |          418.295 |        1422.9  |                   1367.48 |   -0.9888 |   0.0788 |   0.9977 |             0.0872 |
|   2004 |            2604 |            4300 |            4300 |                 14040 |              15040 |             390 |               7390 |        478    |       134     |   1828.88 |            1823.19 |     427.584 |                389 |          429.624 |        1420.32 |                   1360.28 |   -1.0443 |   0.0811 |   0.9974 |             0.0891 |
|   2005 |            2662 |            4400 |            4400 |                 14370 |              16370 |             399 |               8530 |        500.75 |       134     |   1813.26 |            1763.44 |     428.627 |                389 |          430.682 |        1417.46 |                   1354.96 |   -1.0648 |   0.0822 |   0.9974 |             0.0909 |
|   2006 |            2747 |            4536 |            4536 |                 14810 |              16810 |             412 |               8740 |        509    |       135.25  |   1806.14 |            1708.33 |     428.529 |                403 |          430.55  |        1407.52 |                   1351.88 |   -1.1148 |   0.0843 |   0.9976 |             0.0911 |
|   2007 |            2853 |            4716 |            4716 |                 15390 |              17390 |             428 |               9000 |        524    |       140     |   1814.83 |            1661.36 |     430.442 |                403 |          432.065 |        1402.59 |                   1359.17 |   -1.0558 |   0.0819 |   0.9975 |             0.093  |
|   2008 |            2917 |            4824 |            4824 |                 15740 |              18740 |             438 |              10160 |        553.5  |       144     |   1801.78 |            1599.63 |     433.723 |                410 |          434.774 |        1387.43 |                   1361.4  |   -1.2339 |   0.0892 |   0.9975 |             0.0958 |
|   2009 |            3043 |            5028 |            5657 |                 16420 |              21420 |             457 |              12470 |        648    |       148.5   |   1862.49 |            1605.59 |     436.165 |                429 |          437.069 |        1427.85 |                   1415.12 |   -1.866  |   0.1106 |   0.9988 |             0.0913 |
|   2010 |            3050 |            5036 |            5666 |                 16450 |              21460 |             457 |              12490 |        668    |       153     |   1886.23 |            1579.09 |     437.854 |                429 |          440.113 |        1412.13 |                   1395.51 |   -1.8751 |   0.1111 |   0.9989 |             0.0935 |
|   2011 |            3094 |            5112 |            5751 |                 16690 |              21770 |             464 |              12670 |        668    |       153.5   |   1835.51 |            1531.35 |     439.076 |                427 |          441.094 |        1380.43 |                   1365.1  |   -1.9082 |   0.1113 |   0.9989 |             0.0861 |
|   2012 |            3169 |            5236 |            5891 |                 17090 |              22300 |             475 |              12980 |        668    |       156.25  |   1830.75 |            1500    |     438.373 |                427 |          440.233 |        1369.4  |                   1358.63 |   -1.901  |   0.111  |   0.999  |             0.0865 |
|   2013 |            3250 |            5372 |            6044 |                 17530 |              22870 |             487 |              13310 |        662    |       160.75  |   1856.14 |            1478.11 |     441.158 |                428 |          442.544 |        1351.23 |                   1348.47 |   -1.8898 |   0.1117 |   0.999  |             0.096  |
|   2014 |            3305 |            5460 |            6143 |                 17830 |              23260 |             496 |              13540 |        636.25 |       163.5   |   1862.41 |            1500.48 |     447.75  |                428 |          449.119 |        1344.07 |                   1345.32 |   -1.8954 |   0.1119 |   0.999  |             0.0967 |
|   2015 |            3359 |            5548 |            6242 |                 18110 |              23630 |             503 |              13750 |        649    |       165.75  |   1885.48 |            1634.81 |     458.362 |                429 |          457.542 |        1359.62 |                   1364.67 |   -1.8809 |   0.1113 |   0.999  |             0.0955 |
|   2016 |            3373 |            5572 |            6269 |                 18190 |              23740 |             506 |              13820 |        649    |       168     |   1886.49 |            1614.38 |     458.491 |                432 |          458.707 |        1361.59 |                   1369.56 |   -1.8885 |   0.1117 |   0.9991 |             0.0965 |
|   2017 |            3400 |            5616 |            6318 |                 18340 |              23930 |             510 |              13930 |        646.75 |       168.5   |   1855.49 |            1580.78 |     461.963 |                432 |          461.851 |        1347.79 |                   1359.45 |   -1.9237 |   0.113  |   0.9991 |             0.0989 |
|   2018 |            3461 |            5716 |            6431 |                 18660 |              24350 |             519 |              14170 |        640.5  |       171     |   1837.04 |            1543.01 |     464.866 |                450 |          465.587 |        1326.09 |                   1341.53 |   -1.5931 |   0.0985 |   0.9991 |             0.072  |
|   2019 |            3526 |            5828 |            6557 |                 19030 |              24820 |             529 |              14450 |        643    |       175     |   1843.56 |            1515.25 |     484.938 |                486 |          486.231 |        1333.47 |                   1358.71 |   -1.6013 |   0.0989 |   0.9992 |             0.0733 |
|   2020 |            3584 |            5920 |            6660 |                 19330 |              25220 |             538 |              14680 |        654.5  |       178.75  |   1864.56 |            1497.1  |     503.947 |                492 |          504.766 |        1352.62 |                   1378.22 |   -1.6064 |   0.0991 |   0.9992 |             0.0739 |
|   2021 |            3618 |            5980 |            6728 |                 19520 |              25470 |            1502 |              17560 |        795.25 |       181.75  |   1809.05 |            1469.42 |     511.623 |                498 |          515.256 |        1319.72 |                   1356.67 |   -7.6917 |   0.203  |   0.9977 |             0.0375 |
|   2022 |            3733 |            6164 |            6935 |                 20130 |              26260 |             560 |              15290 |        861    |       186.25  |   1709.06 |            1507.56 |     526.978 |                498 |          531.848 |        1272.66 |                   1316.42 |   -1.7159 |   0.1037 |   0.9993 |             0.0859 |
|   2023 |            3995 |            6604 |            7430 |                 21560 |              28120 |             600 |              16370 |        947.5  |       196.75  |   1733.72 |            1554.14 |     570.115 |                542 |          572.482 |        1254.29 |                   1322.58 |   -1.7126 |   0.1035 |   0.9993 |             0.0868 |
