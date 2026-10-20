# UI generosity panel: checks

Built by `IGE/12b.UIGenerosity.py` -> `data/ui_generosity.csv` (51 states incl. DC x 1976-2024). Sources and conventions: see the script docstring.

## Coverage

| variable | first_year | last_year | state_years | years_with_all_51 | missing_state_years |
|---|---|---|---|---|---|
| max_wba | 1976 | 2024 | 2498 | 48 | 1 |
| max_wba_dep | 1976 | 2024 | 2497 | 47 | 2 |
| min_wba | 1976 | 2024 | 2498 | 48 | 1 |
| max_duration_weeks | 1976 | 2024 | 2499 | 49 | 0 |
| dep_allowance | 1976 | 2024 | 2499 | 49 | 0 |
| awb | 1976 | 2024 | 2499 | 49 | 0 |
| aww | 1976 | 2024 | 2499 | 49 | 0 |
| repl_rate | 1976 | 2024 | 2499 | 49 | 0 |
| share_max_wba | 1976 | 2024 | 2475 | 40 | 24 |
| share_max_duration | 1976 | 2024 | 2470 | 38 | 29 |
| avg_potential_duration | 1976 | 2024 | 2469 | 38 | 30 |

Missing max_wba: MA 1999

## Summary by year (unweighted means over states)

max_wba / awb in nominal and 2000 dollars; max_repl = max_wba / aww; share_max_wba = share of new claimants eligible for the maximum (ETA 218); pot_dur = average potential duration (weeks).

| year | max_wba | max_wba_2000 | max_wba_dep_2000 | sd_max_2000 | max_weeks | n_dep | awb_2000 | repl_rate | max_repl | share_max_wba | pot_dur |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1976 | 98.04 | 296.70 | 318.84 | 45.04 | 26.90 | 12 | 218.94 | 0.38 | 0.52 | 0.36 | 23.62 |
| 1977 | 104.63 | 297.31 | 318.70 | 50.01 | 26.90 | 12 | 218.94 | 0.38 | 0.52 | 0.37 | 23.68 |
| 1978 | 111.31 | 293.99 | 314.65 | 51.72 | 26.90 | 12 | 217.36 | 0.38 | 0.51 | 0.37 | 24.02 |
| 1979 | 117.80 | 279.42 | 299.46 | 51.40 | 26.86 | 13 | 210.08 | 0.38 | 0.50 | 0.40 | 23.86 |
| 1980 | 126.75 | 264.87 | 284.50 | 49.03 | 26.86 | 13 | 203.31 | 0.38 | 0.49 | 0.42 | 23.83 |
| 1981 | 139.75 | 264.73 | 284.57 | 50.61 | 26.82 | 13 | 199.15 | 0.37 | 0.49 | 0.41 | 23.58 |
| 1982 | 149.88 | 267.46 | 285.58 | 53.34 | 26.63 | 13 | 208.04 | 0.39 | 0.50 | 0.43 | 23.73 |
| 1983 | 155.76 | 269.30 | 287.07 | 53.88 | 26.43 | 13 | 208.02 | 0.38 | 0.50 | 0.39 | 23.20 |
| 1984 | 162.98 | 270.12 | 288.64 | 52.48 | 26.20 | 13 | 200.80 | 0.37 | 0.50 | 0.37 | 22.67 |
| 1985 | 169.59 | 271.40 | 288.73 | 52.96 | 26.16 | 14 | 202.08 | 0.37 | 0.49 | 0.38 | 23.39 |
| 1986 | 176.73 | 277.67 | 295.84 | 54.49 | 26.16 | 14 | 210.19 | 0.38 | 0.50 | 0.39 | 23.63 |
| 1987 | 181.92 | 275.76 | 293.90 | 53.81 | 26.16 | 14 | 209.60 | 0.37 | 0.49 | 0.38 | 23.16 |
| 1988 | 189.22 | 275.43 | 293.78 | 53.38 | 26.16 | 14 | 208.36 | 0.37 | 0.49 | 0.37 | 23.57 |
| 1989 | 198.25 | 275.32 | 293.54 | 55.01 | 26.16 | 14 | 206.01 | 0.37 | 0.49 | 0.38 | 23.89 |
| 1990 | 206.86 | 272.55 | 290.63 | 57.10 | 26.16 | 14 | 204.50 | 0.37 | 0.49 | 0.36 | 23.77 |
| 1991 | 217.12 | 274.51 | 291.83 | 54.37 | 26.16 | 14 | 205.60 | 0.37 | 0.50 | 0.36 | 23.94 |
| 1992 | 227.45 | 279.17 | 295.63 | 57.67 | 26.16 | 14 | 204.52 | 0.36 | 0.49 | 0.35 | 23.74 |
| 1993 | 238.18 | 283.83 | 299.72 | 60.33 | 26.16 | 14 | 205.99 | 0.37 | 0.51 | 0.34 | 23.44 |
| 1994 | 244.80 | 284.45 | 299.78 | 59.34 | 26.16 | 13 | 205.33 | 0.37 | 0.51 | 0.32 | 23.41 |
| 1995 | 251.41 | 284.08 | 299.27 | 59.54 | 26.16 | 13 | 206.87 | 0.37 | 0.50 | 0.32 | 23.57 |
| 1996 | 258.63 | 283.85 | 299.17 | 59.69 | 26.16 | 13 | 205.72 | 0.36 | 0.50 | 0.32 | 23.55 |
| 1997 | 265.20 | 284.53 | 299.63 | 58.39 | 26.16 | 13 | 204.58 | 0.35 | 0.49 | 0.32 | 23.48 |
| 1998 | 277.08 | 292.72 | 308.42 | 58.13 | 26.16 | 12 | 210.15 | 0.35 | 0.49 | 0.33 | 23.37 |
| 1999 | 284.20 | 293.75 | 305.78 | 58.90 | 26.16 | 12 | 218.18 | 0.36 | 0.49 | 0.35 | 23.54 |
| 2000 | 296.12 | 296.12 | 312.76 | 63.52 | 26.16 | 12 | 220.45 | 0.36 | 0.48 | 0.36 | 23.63 |
| 2001 | 317.12 | 308.34 | 325.54 | 68.78 | 26.16 | 12 | 229.67 | 0.37 | 0.50 | 0.37 | 23.82 |
| 2002 | 330.84 | 316.68 | 334.25 | 68.89 | 26.16 | 12 | 237.72 | 0.38 | 0.51 | 0.36 | 23.33 |
| 2003 | 337.20 | 315.57 | 332.80 | 67.38 | 26.08 | 12 | 233.82 | 0.37 | 0.50 | 0.36 | 22.89 |
| 2004 | 344.35 | 313.91 | 332.34 | 66.78 | 26.12 | 13 | 227.28 | 0.35 | 0.49 | 0.34 | 22.88 |
| 2005 | 354.63 | 312.68 | 330.73 | 68.68 | 26.12 | 13 | 224.82 | 0.35 | 0.49 | 0.34 | 23.42 |
| 2006 | 365.24 | 311.97 | 330.08 | 68.83 | 26.12 | 13 | 225.25 | 0.35 | 0.48 | 0.34 | 23.56 |
| 2007 | 377.59 | 313.66 | 332.70 | 71.49 | 26.12 | 13 | 228.00 | 0.35 | 0.48 | 0.35 | 23.59 |
| 2008 | 392.80 | 314.17 | 333.16 | 71.06 | 26.12 | 13 | 229.18 | 0.35 | 0.48 | 0.36 | 23.75 |
| 2009 | 406.78 | 326.57 | 346.21 | 75.31 | 26.12 | 13 | 242.43 | 0.37 | 0.50 | 0.38 | 23.76 |
| 2010 | 407.88 | 322.04 | 342.07 | 75.87 | 26.12 | 14 | 231.64 | 0.35 | 0.49 | 0.32 | 23.31 |
| 2011 | 411.43 | 315.02 | 333.92 | 74.99 | 25.86 | 14 | 221.94 | 0.34 | 0.48 | 0.31 | 22.98 |
| 2012 | 418.04 | 313.53 | 332.40 | 77.15 | 25.55 | 14 | 222.15 | 0.33 | 0.47 | 0.32 | 23.06 |
| 2013 | 421.06 | 311.19 | 330.14 | 78.68 | 25.45 | 14 | 223.66 | 0.34 | 0.47 | 0.32 | 23.25 |
| 2014 | 426.75 | 310.46 | 328.59 | 79.66 | 25.20 | 13 | 223.17 | 0.33 | 0.46 | 0.32 | 22.87 |
| 2015 | 433.43 | 314.92 | 333.34 | 82.82 | 25.12 | 13 | 232.34 | 0.34 | 0.46 | 0.35 | 22.98 |
| 2016 | 440.49 | 316.05 | 334.66 | 85.85 | 24.55 | 13 | 237.97 | 0.35 | 0.46 | 0.37 | 22.93 |
| 2017 | 446.53 | 313.72 | 332.16 | 86.20 | 24.86 | 13 | 237.30 | 0.34 | 0.45 | 0.36 | 22.87 |
| 2018 | 451.43 | 309.58 | 328.09 | 86.36 | 24.90 | 13 | 234.18 | 0.33 | 0.44 | 0.37 | 22.75 |
| 2019 | 465.59 | 313.55 | 332.19 | 90.85 | 25.27 | 13 | 237.18 | 0.33 | 0.44 | 0.40 | 22.92 |
| 2020 | 478.00 | 318.05 | 337.10 | 95.88 | 24.71 | 13 | 210.19 | 0.28 | 0.42 | 0.35 | 22.62 |
| 2021 | 492.71 | 313.08 | 331.98 | 100.51 | 24.94 | 13 | 218.81 | 0.29 | 0.41 | 0.41 | 22.26 |
| 2022 | 516.37 | 303.79 | 324.31 | 104.42 | 24.12 | 13 | 227.02 | 0.31 | 0.41 | 0.41 | 21.84 |
| 2023 | 540.06 | 305.21 | 325.79 | 108.19 | 23.76 | 13 | 237.01 | 0.32 | 0.42 | 0.45 | 21.78 |
| 2024 | 553.71 | 303.96 | 313.85 | 110.63 | 24.00 | 13 | 240.24 | 0.33 | 0.41 | 0.45 | 21.67 |

## By decade

| decade | max_wba_2000 | awb_2000 | repl_rate | repl_min | repl_max | max_weeks |
|---|---|---|---|---|---|---|
| 1970 | 291.86 | 216.33 | 0.38 | 0.20 | 0.51 | 26.89 |
| 1980 | 271.21 | 205.56 | 0.37 | 0.20 | 0.50 | 26.37 |
| 1990 | 283.32 | 207.14 | 0.36 | 0.22 | 0.51 | 26.16 |
| 2000 | 312.97 | 229.86 | 0.36 | 0.20 | 0.51 | 26.13 |
| 2010 | 314.01 | 230.15 | 0.34 | 0.18 | 0.56 | 25.29 |
| 2020 | 308.82 | 226.65 | 0.31 | 0.17 | 0.49 | 24.31 |

## Sanity checks

* min_wba > max_wba: 0 state-years.
* AWB above the maximum incl. dependents' allowances (x1.02): 0 state-years.
* AWB below 35% of max_wba: 0 state-years.
* Nominal max_wba falls from one July to the next: 48 cases (legislated cuts or freezes are printed values; small declines are indexed maxima following the state average wage, larger ones legislated cuts or freezes, e.g. LA 1988-89, DC 1997, NC 2013, OK 2004/2011/2021 (trust-fund-linked schedule); SC 1978 = 119 is printed between 111 in 1977 and 1979):

| state | year | max_prev_year | max_wba | law_src |
|---|---|---|---|---|
| AR | 2012 | 457 | 451 | SigPros July 2012 (text layer) |
| CT | 2014 | 591 | 590 | SigPros July 2014 (text layer) |
| CT | 2018 | 616 | 613 | SigPros July 2018 (text layer) |
| DC | 1997 | 359 | 309 | SigPros July 1997 (scan, transcribed) |
| DE | 2003 | 330 | 320 | SigPros July 2003 (text layer) |
| HI | 2011 | 559 | 549 | SigPros July 2011 (text layer) |
| HI | 2013 | 560 | 534 | SigPros July 2013 (text layer) |
| HI | 2021 | 648 | 639 | SigPros July 2021 (text layer) |
| IA | 1979 | 133 | 131 | SigPros July 1979 (scan, transcribed) |
| IA | 1983 | 158 | 143 | SigPros July 1983 (scan, transcribed) |
| ID | 2005 | 325 | 322 | SigPros July 2005 (text layer) |
| ID | 2009 | 364 | 362 | SigPros July 2009 (text layer) |
| ID | 2010 | 362 | 334 | SigPros July 2010 (text layer) |
| ID | 2017 | 410 | 405 | SigPros July 2017 (text layer) |
| KS | 2010 | 436 | 435 | SigPros July 2010 (text layer) |
| LA | 1988 | 205 | 191 | SigPros July 1988 (scan, transcribed) |
| LA | 1989 | 191 | 181 | SigPros July 1989 (scan, transcribed) |
| LA | 2010 | 284 | 247 | SigPros July 2010 (text layer) |
| MA | 2003 | 512 | 507 | SigPros July 2003 (text layer) |
| MA | 2011 | 629 | 625 | SigPros July 2011 (text layer) |
| ME | 1993 | 198 | 192 | SigPros July 1993 (scan, transcribed) |
| ME | 1998 | 231 | 227 | SigPros July 1998 (scan, transcribed) |
| MN | 1994 | 305 | 304 | SigPros July 1994 (scan, transcribed) |
| MN | 2011 | 585 | 578 | SigPros July 2011 (text layer) |
| NC | 2013 | 522 | 350 | SigPros July 2013 (text layer) |
| ND | 1983 | 175 | 172 | SigPros July 1983 (scan, transcribed) |
| ND | 1987 | 197 | 179 | SigPros July 1987 (scan, transcribed) |
| ND | 2016 | 633 | 630 | SigPros July 2016 (text layer) |
| ND | 2017 | 630 | 606 | SigPros July 2017 (text layer) |
| ND | 2018 | 606 | 595 | SigPros July 2018 (text layer) |
| NJ | 2011 | 600 | 598 | SigPros July 2011 (text layer) |
| NM | 2010 | 403 | 380 | SigPros July 2010 (text layer) |
| NM | 2014 | 407 | 406 | SigPros July 2014 (text layer) |
| NV | 2010 | 400 | 398 | SigPros July 2010 (text layer) |
| NV | 2011 | 398 | 396 | SigPros July 2011 (text layer) |
| OK | 2003 | 304 | 303 | SigPros July 2003 (text layer) |
| OK | 2004 | 303 | 275 | SigPros July 2004 (text layer) |
| OK | 2011 | 430 | 358 | SigPros July 2011 (text layer) |
| OK | 2018 | 510 | 506 | SigPros July 2018 (text layer) |
| OK | 2021 | 539 | 461 | SigPros July 2021 (text layer) |
| PA | 2017 | 573 | 561 | SigPros July 2017 (text layer) |
| SC | 1979 | 119 | 111 | SigPros July 1979 (scan, transcribed) |
| UT | 2004 | 373 | 362 | SigPros July 2004 (text layer) |
| VA | 2003 | 318 | 316 | SigPros July 2003 (text layer) |
| WA | 2010 | 605 | 560 | SigPros July 2010 (text layer) |
| WY | 2010 | 438 | 430 | SigPros July 2010 (text layer) |
| WY | 2016 | 491 | 489 | SigPros July 2016 (text layer) |
| WY | 2017 | 489 | 475 | SigPros July 2017 (text layer) |

* Nominal max_wba rises by more than 25% in a year: 12 cases:

| state | year | max_prev_year | max_wba | law_src |
|---|---|---|---|---|
| AK | 1981 | 90 | 150 | SigPros July 1981 (scan, transcribed) |
| AK | 2009 | 248 | 370 | SigPros July 2009 (text layer) |
| AL | 1983 | 90 | 120 | SigPros July 1983 (scan, transcribed) |
| AZ | 2022 | 240 | 320 | SigPros July 2022 (text layer) |
| CA | 2002 | 230 | 330 | SigPros July 2002 (text layer) |
| GA | 1981 | 90 | 115 | SigPros July 1981 (scan, transcribed) |
| LA | 1977 | 90 | 120 | SigPros July 1977 (scan, transcribed) |
| MI | 1981 | 97 | 182 | SigPros July 1981 (scan, transcribed) |
| NY | 1984 | 125 | 180 | SigPros July 1984 (scan, transcribed) |
| NY | 1989 | 180 | 245 | SigPros July 1989 (scan, transcribed) |
| TX | 1978 | 63 | 84 | SigPros July 1978 (scan, transcribed) |
| WV | 2023 | 424 | 662 | SigPros July 2023 (text layer) |

Correlations (state-years):

| index | max_wba | awb | share_max_wba | repl_rate | max_wba_repl |
|---|---|---|---|---|---|
| max_wba | 1.00 | 0.97 | -0.30 | 0.03 | 0.20 |
| awb | 0.97 | 1.00 | -0.14 | 0.00 | 0.06 |
| share_max_wba | -0.30 | -0.14 | 1.00 | -0.26 | -0.57 |
| repl_rate | 0.03 | 0.00 | -0.26 | 1.00 | 0.86 |
| max_wba_repl | 0.20 | 0.06 | -0.57 | 0.86 | 1.00 |

## Check against ET Handbook 394 (Alabama)

hb_* = Handbook 394 (average weekly benefit, AWW in covered employment, AWB/AWW ratio); right-hand columns = this panel (ETA 5159 AWB, BEA wages per job / 52).

| year | hb_aww | hb_awb | hb_ratio | state_name | awb | aww | repl_rate |
|---|---|---|---|---|---|---|---|
| 1976 | 179.90 | 66.50 | 0.37 | Alabama | 66.50 | 170.19 | 0.39 |
| 1980 | 246.72 | 76.76 | 0.32 | Alabama | 76.76 | 236.98 | 0.32 |
| 1985 | 319.94 | 97.50 | 0.31 | Alabama | 97.50 | 320.35 | 0.30 |
| 1990 | 384.27 | 115.57 | 0.30 | Alabama | 115.57 | 387.33 | 0.30 |
| 1995 | 454.45 | 138.51 | 0.30 | Alabama | 138.51 | 460.62 | 0.30 |
| 2000 | 546.34 | 159.41 | 0.29 | Alabama | 159.41 | 547.96 | 0.29 |
| 2005 | 651.16 | 182.01 | 0.28 | Alabama | 182.01 | 654.75 | 0.28 |
| 2010 | 752.08 | 205.80 | 0.27 | Alabama | 205.80 | 762.44 | 0.27 |
| 2015 | 831.15 | 215.94 | 0.26 | Alabama | 215.94 | 839.35 | 0.26 |
| 2020 | 984.60 | 252.20 | 0.26 | Alabama | 252.20 | 989.12 | 0.26 |
| 2023 | 1128.07 | 257.40 | 0.23 | Alabama | 257.40 | 1137.62 | 0.23 |
| 2024 | 1172.99 | 253.92 | 0.22 | Alabama | 253.92 | 1181.48 | 0.21 |

## Maximum WBA (nominal $), selected states (every 4th year)

| year | CA | FL | MA | MI | MS | NC | NY | TX |
|---|---|---|---|---|---|---|---|---|
| 1976 | 104 | 82 | 101 | 97 | 80 | 97 | 95 | 63 |
| 1980 | 120 | 95 | 131 | 97 | 90 | 130 | 125 | 105 |
| 1984 | 166 | 150 | 185 | 197 | 115 | 166 | 180 | 182 |
| 1988 | 166 | 200 | 236 | 242 | 145 | 204 | 180 | 210 |
| 1992 | 230 | 225 | 296 | 283 | 165 | 258 | 300 | 231 |
| 1996 | 230 | 250 | 347 | 300 | 180 | 297 | 300 | 259 |
| 2000 | 230 | 275 | 431 | 300 | 190 | 356 | 365 | 294 |
| 2004 | 410 | 275 | 508 | 362 | 210 | 416 | 405 | 330 |
| 2008 | 450 | 275 | 600 | 362 | 230 | 457 | 405 | 378 |
| 2012 | 450 | 275 | 653 | 362 | 235 | 522 | 405 | 426 |
| 2016 | 450 | 275 | 722 | 362 | 235 | 350 | 425 | 479 |
| 2020 | 450 | 275 | 823 | 362 | 235 | 350 | 504 | 521 |
| 2024 | 450 | 275 | 1033 | 362 | 235 | 350 | 504 | 577 |

## Maximum WBA (2000 $), selected states (every 4th year)

| year | CA | FL | MA | MI | MS | NC | NY | TX |
|---|---|---|---|---|---|---|---|---|
| 1976 | 315 | 248 | 306 | 294 | 242 | 294 | 288 | 191 |
| 1980 | 251 | 199 | 274 | 203 | 188 | 272 | 261 | 219 |
| 1984 | 275 | 249 | 307 | 327 | 191 | 275 | 298 | 302 |
| 1988 | 242 | 291 | 344 | 352 | 211 | 297 | 262 | 306 |
| 1992 | 282 | 276 | 363 | 347 | 203 | 317 | 368 | 284 |
| 1996 | 252 | 274 | 381 | 329 | 198 | 326 | 329 | 284 |
| 2000 | 230 | 275 | 431 | 300 | 190 | 356 | 365 | 294 |
| 2004 | 374 | 251 | 463 | 330 | 191 | 379 | 369 | 301 |
| 2008 | 360 | 220 | 480 | 290 | 184 | 366 | 324 | 302 |
| 2012 | 338 | 206 | 490 | 272 | 176 | 392 | 304 | 320 |
| 2016 | 323 | 197 | 518 | 260 | 169 | 251 | 305 | 344 |
| 2020 | 299 | 183 | 548 | 241 | 156 | 233 | 335 | 347 |
| 2024 | 247 | 151 | 567 | 199 | 129 | 192 | 277 | 317 |

## AWB / AWW, selected states (every 4th year)

| year | CA | FL | MA | MI | MS | NC | NY | TX |
|---|---|---|---|---|---|---|---|---|
| 1976 | 0.33 | 0.36 | 0.39 | 0.38 | 0.35 | 0.39 | 0.33 | 0.30 |
| 1980 | 0.30 | 0.31 | 0.37 | 0.33 | 0.34 | 0.39 | 0.29 | 0.32 |
| 1984 | 0.30 | 0.34 | 0.37 | 0.37 | 0.34 | 0.35 | 0.31 | 0.39 |
| 1988 | 0.27 | 0.37 | 0.41 | 0.40 | 0.33 | 0.37 | 0.28 | 0.40 |
| 1992 | 0.28 | 0.35 | 0.39 | 0.41 | 0.34 | 0.37 | 0.32 | 0.37 |
| 1996 | 0.25 | 0.36 | 0.38 | 0.34 | 0.34 | 0.39 | 0.30 | 0.35 |
| 2000 | 0.20 | 0.37 | 0.35 | 0.35 | 0.32 | 0.38 | 0.29 | 0.34 |
| 2004 | 0.30 | 0.32 | 0.38 | 0.38 | 0.31 | 0.38 | 0.29 | 0.35 |
| 2008 | 0.30 | 0.30 | 0.36 | 0.36 | 0.28 | 0.37 | 0.27 | 0.35 |
| 2012 | 0.27 | 0.27 | 0.34 | 0.33 | 0.27 | 0.35 | 0.26 | 0.34 |
| 2016 | 0.26 | 0.26 | 0.38 | 0.32 | 0.27 | 0.27 | 0.25 | 0.39 |
| 2020 | 0.19 | 0.21 | 0.29 | 0.28 | 0.22 | 0.21 | 0.22 | 0.31 |
| 2024 | 0.21 | 0.19 | 0.39 | 0.27 | 0.22 | 0.26 | 0.24 | 0.34 |

## Cross-check of the July maxima (2000-2024) against the January issues

The January issues of year t and t+1 are parsed the same way; a July value outside [min, max] of the two January values (+-1) is listed. 7 of 1275 state-years. Most are states that index or change the maximum between July and January (the January issue then shows a value on the far side of an increase and a later cut, or a parsing issue of the January table); none was changed on this basis alone except where noted in OVERRIDES.

| state | year | jan_same_year | july | jan_next_year | note |
|---|---|---|---|---|---|
| DC | 2019 | 438 | 432 | 444 |  |
| HI | 2012 | 523 | 560 | 534 | table: $523 before 4/1/12, $560 from 4/1/12 |
| NM | 2010 | 426 | 380 | 386 |  |
| SC | 2003 | 278 | 285 | 278 |  |
| UT | 2004 | 377 | 362 | 371 |  |
| WA | 2009 | 541 | 605 | 560 |  |
| WY | 2000 | 30 | 261 | 30 |  |

## Notes on individual cells

| state | year | law_note |
|---|---|---|
| AK | 2020-2022 | table: '$370 + DA' (DA $24 per dependent up to $72) |
| AL | 2020-2024 | maximum weeks below 26 or indexed to the unemployment rate by later legislation; value as printed in the July table |
| AL | 1977 | weeks column clipped on scan (p1): carried from 1976 |
| AR | 2011-2024 | maximum weeks below 26 or indexed to the unemployment rate by later legislation; value as printed in the July table |
| AZ | 2022-2024 | maximum weeks below 26 or indexed to the unemployment rate by later legislation; value as printed in the July table |
| CO | 2007-2024 | higher of two alternative maxima |
| DC | 1998 | dependents allowance no longer in the formula from 1998 |
| FL | 2012-2024 | maximum weeks below 26 or indexed to the unemployment rate by later legislation; value as printed in the July table |
| GA | 2012-2024 | maximum weeks below 26 or indexed to the unemployment rate by later legislation; value as printed in the July table |
| HI | 2012 | table: $523 before 4/1/12, $560 from 4/1/12 |
| IA | 2022-2024 | maximum weeks below 26 or indexed to the unemployment rate by later legislation; value as printed in the July table |
| IA | 1993 | printed 30-36 / 245 hand-corrected on the scan to 31-38 / 211-259 |
| IA | 1976 | table shows 39 (plant-closing extension); regular 26 |
| IL | 2012-2024 | maximum weeks below 26 or indexed to the unemployment rate by later legislation; value as printed in the July table |
| KS | 2014-2024 | maximum weeks below 26 or indexed to the unemployment rate by later legislation; value as printed in the July table |
| KY | 2001 | July 2001 table prints $341; January 2001, January 2002 and July 2002 all $329 (no cut in between): treated as a misprint |
| KY | 2023-2024 | maximum weeks below 26 or indexed to the unemployment rate by later legislation; value as printed in the July table |
| LA | 1978 | max blurred on scan |
| MA | 2024 | dependents' allowance no longer capped (table: 'no cap on DA') |
| MA | 1999 | printed max "$250" (footnote 4) is evidently a misprint (Maryland's value); left missing |
| MD | 2000 | same maximum with or without dependents (table fn 4) |
| MI | 2012-2024 | maximum weeks below 26 or indexed to the unemployment rate by later legislation; value as printed in the July table |
| MN | 1999-2024 | higher of two alternative maxima |
| MN | 2003 | higher of two alternative maxima; $478 effective 8/3/03 not used |
| MN | 2001 | only maximum printed is $452 'effective 8/1/01' |
| MO | 2011-2024 | maximum weeks below 26 or indexed to the unemployment rate by later legislation; value as printed in the July table |
| MT | 2023-2024 | maximum weeks below 26 or indexed to the unemployment rate by later legislation; value as printed in the July table |
| NC | 2004 | $426 effective 8/1/04 not used |
| NC | 2013-2024 | maximum weeks below 26 or indexed to the unemployment rate by later legislation; value as printed in the July table |
| NJ | 2000 | same maximum with or without dependents (table fn 4) |
| OK | 2023-2024 | maximum weeks below 26 or indexed to the unemployment rate by later legislation; value as printed in the July table |
| OK | 1986 | weeks cell reads 25 or 26 (footnote 14); 26 used |
| OR | 1986 | weeks cell partly illegible (footnote 7); 26 used |
| SC | 1994 | faint scan |
| SC | 2011-2024 | maximum weeks below 26 or indexed to the unemployment rate by later legislation; value as printed in the July table |
| TN | 2024 | maximum weeks below 26 or indexed to the unemployment rate by later legislation; value as printed in the July table |
| VA | 2002 | July 2002 table prints $69 / $368, out of line with January 2002 ($268) and January / July 2003 ($318 / $316): misprint; January 2003 values used |
| VT | 1981 | max partly illegible on scan |
| WA | 2003 | July 2003 table prints $510; January 2003, January 2004 and July 2004 all $496 (2003 freeze of the maximum): $496 used |
