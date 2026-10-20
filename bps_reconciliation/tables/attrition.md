### Table S2.2. Which of BPS's restrictions drop the displaced couple-years

Universe: married couples, husband 30-57 (age - 1), head in IGE's PSID person file (SRC + SEO), PSID 1999-2009 waves (income years 1998-2008). BPS's restrictions applied in their order (psid_sample.do, prepare_bootstrap.do); each row = couple-years still in the sample after the step. hd / wd / jd = husband / wife / joint displacement in the couple-year's interval.

| Step | Rows | Husband displaced | Wife displaced | Joint | Either | Husband closure | Wife closure | Joint: couples | Husband displaced: men |
|---|---|---|---|---|---|---|---|---|---|
| 0. U: married, husband 30-57, SRC+SEO | 14,327 | 692 | 480 | 57 | 1,115 | 217 | 168 | 55 | 590 |
| 1. composition break (fchg>1) year dropped | 13,876 | 658 | 460 | 52 | 1,066 | 207 | 163 | 50 | 561 |
| 2. not married / no wife | 13,876 | 658 | 460 | 52 | 1,066 | 207 | 163 | 50 | 561 |
| 3. state missing | 13,811 | 654 | 456 | 51 | 1,059 | 206 | 161 | 49 | 558 |
| 4. female head / age always missing | 13,811 | 654 | 456 | 51 | 1,059 | 206 | 161 | 49 | 558 |
| 5. net worth >= 20M | 13,802 | 654 | 456 | 51 | 1,059 | 206 | 161 | 49 | 558 |
| 6. age outside 30-57 (BPS age recode) | 13,767 | 653 | 455 | 51 | 1,057 | 206 | 161 | 49 | 558 |
| 7. SEO sample dropped | 10,857 | 488 | 345 | 37 | 796 | 157 | 132 | 36 | 418 |
| 8. education missing | 10,157 | 449 | 317 | 33 | 733 | 150 | 123 | 32 | 386 |
| 9. minimum-wage / price merge | 10,157 | 449 | 317 | 33 | 733 | 150 | 123 | 32 | 386 |
| 10. no-work rule (person-level) = data4estim | 9,148 | 404 | 283 | 28 | 659 | 131 | 112 | 27 | 351 |
| 11. rows with a husband wage difference (duw | 6,372 | 293 | 186 | 17 | 462 | 96 | 73 | 17 | 259 |
| 12. rows with both spouses' wage differences | 4,762 | 208 | 160 | 16 | 352 | 62 | 63 | 16 | 188 |
| 101. no-work rule: own year | 463 | 8 | 15 | 1 | 22 | 4 | 6 |  |  |
| 102. no-work rule: other year | 546 | 37 | 19 | 4 | 52 | 15 | 5 |  |  |

Why rows in data4estimation have no husband wage-growth moment (head in IGE person file):

| Group | rows in data4estimation | husband wage difference available | no t-2 observation of the couple | half-min-wage trim at t or t-2 | jump trim at t or t-2 (not min-wage) |
|---|---|---|---|---|---|
| hd | 414 | 302 | 105 | 7 | 0 |
| wd | 288 | 189 | 93 | 5 | 1 |
| jd | 28 | 17 | 11 | 0 | 0 |
| none | 8,637 | 6,015 | 2,481 | 101 | 40 |

### Table S1e. Couples lost to separation at BPS's composition break

Married couples (husband 30-57, head in IGE person file, income years 1998-2006 so that the next wave exists). sep_obs = at the head's next interview the marriage has ended or the wife is another person (heads observed again); bps_break_next = the next interview carries fchg > 1 (BPS drop that year and restart the household). Cell: share [events / couple-years]; differences = linear probability, s.e. clustered by head.

| Sample | Outcome | No displacement | Husband only | Wife only | Joint | Husband only - none | Wife only - none | Joint - none |
|---|---|---|---|---|---|---|---|---|
| SRC+SEO | sep_obs | 0.0282 [289/10,250] | 0.0386 [17/440] | 0.0572 [17/297] | 0.0930 [4/43] | 0.0104 (0.0093; p=0.260) | 0.0290** (0.0136; p=0.033) | 0.0648 (0.0446; p=0.146) |
| SRC+SEO | bps_break_next | 0.0281 [288/10,250] | 0.0409 [18/440] | 0.0572 [17/297] | 0.0930 [4/43] | 0.0128 (0.0095; p=0.178) | 0.0291** (0.0136; p=0.032) | 0.0649 (0.0446; p=0.145) |
| SRC (BPS) | sep_obs | 0.0240 [196/8,158] | 0.0326 [11/337] | 0.0570 [13/228] | 0.1000 [3/30] | 0.0086 (0.0098; p=0.379) | 0.0330** (0.0155; p=0.034) | 0.0760 (0.0550; p=0.167) |
| SRC (BPS) | bps_break_next | 0.0239 [195/8,158] | 0.0356 [12/337] | 0.0614 [14/228] | 0.1000 [3/30] | 0.0117 (0.0102; p=0.250) | 0.0375** (0.0160; p=0.019) | 0.0761 (0.0550; p=0.167) |

Counts: SRC+SEO: couples_ending_in_separation (all) = 327; SRC+SEO: couples_ending_in_separation (any displacement before) = 38; SRC+SEO: couples (all) = 3,689; SRC (BPS): couples_ending_in_separation (all) = 223; SRC (BPS): couples_ending_in_separation (any displacement before) = 27; SRC (BPS): couples (all) = 2,861
