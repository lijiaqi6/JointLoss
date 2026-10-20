# Multiple testing: the layoff and sons-daughters results

Built by `110.MultipleTesting.py` (2026-10-20); families in its docstring. Holm = family-wise; BH = false discovery rate.

## A. The layoff cost (Holm, 6 tests)

| test | estimate | p | adjusted p |
|---|---|---|---|
| layoff band change (91) | -0.914 (0.244) | 0.0002 | 0.0011 |
| layoff within-son slope (88) | -0.236 (0.103) | 0.0219 | 0.0437 |
| layoff minus closure change (91) | -0.914 (0.326) | 0.0050 | 0.0150 |
| band change, one job-end net (103) | -1.392 (0.463) | 0.0026 | 0.0131 |
| within-son slope, one job-end net (103) | -0.391 (0.171) | 0.0222 | 0.0437 |
| rank change (108) | -22.163 (7.483) | 0.0031 | 0.0131 |

## B. Sons vs daughters (Holm, 4 tests)

| test | estimate | p | adjusted p |
|---|---|---|---|
| daughters - sons, wage change | 0.925 (0.290) | 0.0014 | 0.0043 |
| daughters - sons, earnings change | 1.294 (0.378) | 0.0006 | 0.0025 |
| daughters - sons, wage within person | 0.254 (0.129) | 0.0489 | 0.0609 |
| daughters - sons, earnings within person | 0.380 (0.176) | 0.0304 | 0.0609 |

## C. Every Section 6 design test (BH, 28 tests)

| test | estimate | p | adjusted p |
|---|---|---|---|
| layoff band change (91) | -0.914 (0.244) | 0.0002 | 0.0015 |
| layoff within-son slope (88) | -0.236 (0.103) | 0.0219 | 0.0357 |
| layoff minus closure change (91) | -0.914 (0.326) | 0.0050 | 0.0117 |
| band change, one job-end net (103) | -1.392 (0.463) | 0.0026 | 0.0081 |
| within-son slope, one job-end net (103) | -0.391 (0.171) | 0.0222 | 0.0357 |
| rank change (108) | -22.163 (7.483) | 0.0031 | 0.0086 |
| daughters - sons, wage change | 0.925 (0.290) | 0.0014 | 0.0051 |
| daughters - sons, earnings change | 1.294 (0.378) | 0.0006 | 0.0034 |
| daughters - sons, wage within person | 0.254 (0.129) | 0.0489 | 0.0596 |
| daughters - sons, earnings within person | 0.380 (0.176) | 0.0304 | 0.0426 |
| timing: teen x age (A2) | -0.157 (0.068) | 0.0214 | 0.0357 |
| timing: 6-12 x age (A2) | -0.110 (0.063) | 0.0815 | 0.0951 |
| small income loss x age | -0.473 (0.144) | 0.0010 | 0.0049 |
| short unemployment x age | -0.338 (0.119) | 0.0046 | 0.0117 |
| repeated layoffs x age | -0.268 (0.106) | 0.0117 | 0.0249 |
| bad-times layoffs, change | -0.675 (0.320) | 0.0349 | 0.0465 |
| other layoffs, change | -1.400 (0.378) | 0.0002 | 0.0015 |
| father unemployed at son's 20-24 | 0.289 (0.061) | 0.0000 | 0.0001 |
| father laid off again at son's 20-24 | 0.132 (0.035) | 0.0002 | 0.0015 |
| industry decline, reduced form within son | 0.143 (0.063) | 0.0242 | 0.0357 |
| born < 1963, within son (103 a) | -0.210 (0.123) | 0.0886 | 0.0992 |
| born 1963-75, within son (103 a) | -0.248 (0.167) | 0.1381 | 0.1487 |
| born 1976+, within son (103 a) | -0.547 (0.219) | 0.0125 | 0.0249 |
| daughters' partner's earnings, change | 0.764 (0.240) | 0.0015 | 0.0051 |
| wage within occupation, change | -0.392 (0.188) | 0.0374 | 0.0476 |
| occupation score, change | -0.171 (0.076) | 0.0239 | 0.0357 |
| UI replacement rate x layoff x age | -0.038 (0.187) | 0.8402 | 0.8402 |
| UI weeks x layoff x age | -0.191 (0.395) | 0.6281 | 0.6514 |

