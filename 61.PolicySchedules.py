"""IGE/61.PolicySchedules.py -- era-mean policy schedules for the Paper A structural model (verified version, 2026-10-18).

Writes paperA_model/inputs/schedules_era{1,2,3}.json (format read by paperA_model/params.load_schedule and
paperA_model/model.py) and the check table output/policy_schedules.md (every parameter by year, the era means, the
sources, and the comparison with the minimal version that was transcribed from memory).
Eras (model document D8): 1 = 1984-1996, 2 = 1997-2008, 3 = 2009-2023 (2022-23 with the last). Every parameter is the
mean over the era's calendar years of the statutory value deflated to 2000 dollars with the CPI-U of IGE/common.py
(extended with BLS 2023-24 annual averages, as IGE/12b.UIGenerosity.py does). Monthly programme parameters (SNAP) are
built month by month from the fiscal-year (October-September) tables, so that a calendar year averages the two fiscal
years it overlaps and within-year changes (ARRA April 2009, November 2013 cut, the 2021 15% increase) are weighted by
their months.

SOURCES (all checked 2026-10-18; URLs repeated next to each table below)
  * EITC (phase-in rate, maximum credit, phase-out rate, phase-out start for unmarried and married-joint filers, by
    number of qualifying children 0 / 1 / 2 / 3+):
      1984-2007  CRS RL31768 'The Earned Income Tax Credit (EITC): An Overview' (C. Scott, March 2007), Appendix 2,
                 Table 8 'EITC Parameters, 1975-2007' (https://policyarchive.org/download/19357), with the married
                 phase-out supplement $1,000 (2002-04) / $2,000 (2005-07) of its notes b and c;
      rates and maxima 1975-2022 cross-checked with CRS R44825 'The EITC: Legislative History' (2022), Table B-1
                 (https://www.everycrsreport.com/files/2022-04-28_R44825_f8df668a4b0d35099c02d661d5399ee1b084d206.pdf)
                 and with the UKCPR National Welfare Data (ExternalData/ukcpr_national_welfare_data_1980_2024_
                 jan26update.xlsx, EITC columns). Two typos in those secondary tables were resolved by arithmetic
                 (max credit = rate x earned-income amount; completed phase-out = start + max / phase-out rate):
                 1994 two-child phase-out rate 17.68% (RL31768 prints 17.86); 1994 one-child phase-in 26.3% (UKCPR
                 prints 23.6); 1985-86 credit rate 11% and maximum $550 (RL31768 prints 10% / $500; R44825 and UKCPR
                 11% / $550, and P.L. 98-369);
      2008-2023  IRS Revenue Procedures (section 'Earned Income Credit'): Rev. Proc. 2007-66 (2008), 2008-66 (2009,
                 superseded for MFJ and 3+ children by ARRA: IRS Publication 596 for 2009, completed phase-out amounts
                 $40,295 / $45,295 etc.), 2009-50 (2010), 2011-12 (2011), 2011-52 (2012), 2013-15 (2013), 2013-35
                 (2014), 2014-61 (2015), 2015-53 (2016), 2016-55 (2017), 2018-18 (2018; read through IRS Publication 596
                 for 2018: completed phase-out $45,802 / $51,492 etc., the Rev. Proc. URL returns 404), 2018-57 (2019),
                 2019-44 (2020), 2020-45 (2021; childless parameters of ARPA from Publication 596 for 2021), 2021-45
                 (2022), 2022-38 (2023): https://www.irs.gov/pub/irs-drop/rp-YY-NN.pdf,
                 https://www.irs.gov/pub/irs-prior/p596--YYYY.pdf.
  * SNAP / food stamps (48 states and DC; maximum allotment by household size 1-8, standard deduction by size,
    asset limit):
      FY2006-FY2024  USDA FNS 'Allotments and Deduction Information' pages and COLA tables
                 (https://www.fns.usda.gov/snap/allotment/cola: fy-2006 ... fy-2013 pages; FY14_Allot_Deduct-1/-2,
                 FY15_Allot_Deduct, FY16/FY17 'Maximun', FY18-FY24 Maximum-Allotments-Deductions PDFs, FY21 COVID / ARPA
                 tables);
      FY1984-FY2005  maximum allotments for 1-4 persons from the UKCPR National Welfare Data (FS/SNAP benefit for a
                 1- to 4-person family; equal to the FNS values in all FY2006-FY2024 years checked), cross-checked with
                 the 2004 Green Book Table 15-11 (four-person maximum, FY1985-2002,
                 https://www.govinfo.gov/content/pkg/GPO-CPRT-108WPRT108-6/pdf/GPO-CPRT-108WPRT108-6-2-15.pdf) and with
                 the official tables reproduced in California DSS All County Letters 84-96, 85-90, 86-88, 91-97, 92-79,
                 93-65, 94-73, 95-64 (https://www.cdss.ca.gov/lettersnotices/entres/getinfo/aclYY/YY-NN.pdf) and the
                 Federal Register notice of 11 Jan 1995 (https://www.govinfo.gov/content/pkg/FR-1995-01-11/html/
                 95-636.htm); sizes 5-8 in years without an official table by the statutory Thrifty Food Plan size
                 factors (x 1.1875, 1.425, 1.575, 1.80 of the four-person amount + $0.50, rounded down; within $1 of
                 every official table); the 2004 Green Book's FY1993 four-person value ($375) contradicts ACL 92-79 ($370, 'will
                 remain at the current levels') and ACL 93-65 (FY1994 'will increase' to $375): $370 used;
      standard deduction  FY1984 $89 (ACL 83-92), FY1985 $95 (ACL 84-96), FY1986 $98 (ACL 85-90), FY1987 $99 (ACL
                 86-88), FY1991 $116 and FY1992 $122 (ACL 91-97), FY1993 $127 (ACL 92-79), FY1994 $131 (ACL 93-65),
                 FY1995 $134 (ACL 94-73; FR 1995), FY1996 $138 in Oct-Nov 1995 and $134 from Dec 1995 (ACL 95-64), $134
                 FY1997-FY2002 (PRWORA freeze), FY2004 $134 / $149 / $171 for 1-4 / 5 / 6+ persons (2004 Green Book),
                 FY2006+ FNS. NOT FOUND in an official table and computed by the statute: FY1988-FY1990 ($102, $106,
                 $111: the FY1987 $99 indexed by the CPI-U for items other than food, 12 months to June, rounded down;
                 the same rule reproduces the verified FY1991 $116 and FY1992 $122), FY2003 and FY2005 (8.31% of the
                 net income standard by size with the $134 minimum, the 2002 Farm Bill rule; it reproduces the verified
                 FY2004 and FY2006-08 amounts);
      gross-income test  130% of the HHS poverty guideline of the previous calendar year (FNS standards for fiscal year
                 y use the guideline published in y-1), monthly, rounded up (reproduces the 2004 Green Book Table
                 15-5); HHS guidelines 1983-2023 from ASPE 'Prior HHS Poverty Guidelines and Federal Register
                 References' (https://aspe.hhs.gov/topics/poverty-economic-mobility/poverty-guidelines/
                 prior-hhs-poverty-guidelines-federal-register-references) and the 2016 size-specific table
                 (https://aspe.hhs.gov/2016-poverty-guidelines);
      asset limit  $2,000 through FY2014 (2004 Green Book), $2,250 FY2015-FY2021 (FNS FY2015 resource-limit memo; FY19,
                 FY20, FY21 tables), $2,500 FY2022, $2,750 FY2023-FY2024 (FNS tables); the 20% earned-income deduction
                 and the 30% benefit-reduction rate are statutory. Not modelled: state emergency allotments 2020-23,
                 broad-based categorical eligibility (most states drop the asset test after ~2001), shelter deduction.
  * Tax (chi_e, mu_e): NBER TAXSIM 35 (https://taxsim.nber.org/taxsim35/, web interface, no key), every year
    1984-2023: married filing jointly, two children aged 5 and 10, wage income only split 65 / 35 between spouses,
    200 log-spaced annual incomes from $5,000 to $300,000 in 2000 dollars converted to nominal; tax T = federal income
    tax (TAXSIM fiitax) + the EITC (v25), the CARES / ARPA recovery rebates (v45) and the Making Work Pay credit
    (2009-10, computed: min(6.2% of earnings, $800) less 2% of AGI above $150,000) added back, + the employee
    payroll tax (tfica); child tax credits (incl. the refundable part) stay in T, as the plan says. OLS of
    ln(Y - T) on ln Y in 2000 dollars per year -> (chi, mu); era value = mean of the yearly (chi, mu).
  * c_min: AFDC/TANF maximum monthly benefit for a family of three by state and year, UKCPR National Welfare Data
    (compiled from the Green Book and the Urban Institute Welfare Rules Database), mean over states weighted by the CPS
    couples' state distribution of the year (output/cps_couple_state_shares.csv written by IGE/62; 1994 shares
    for 1984-93); unweighted median and UKCPR-population-weighted mean reported as checks.
  * UI cap: data/ui_generosity.csv (IGE/12b) column max_wba_2000 x 52/12, mean over states weighted as c_min.
    UI replacement 0.5 and expiry 1/6 a month are statutory / design constants; take-up q_UI (one value for both
    spouses, lead 2026-10-18) = mean of the DWS shares of displaced husbands and wives with UI (IGE/60 targets
    dws_ui_h, dws_ui_w; fallback 0.523 from IGE/39).

Run: .venv/Scripts/python.exe IGE/61.PolicySchedules.py   [--no-taxsim  uses the cached TAXSIM output]
     (one TAXSIM request of 8,000 records, ~1 minute; cache data/taxsim_paperA.csv)
"""
import os
import argparse
import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import CPI as CPI_COMMON  # noqa: E402  (read-only import)

CPI = {**CPI_COMMON, 2023: 304.702, 2024: 313.689}
OUT_DIR = HERE / "paperA_model" / "inputs"
ERAS = {1: range(1984, 1997), 2: range(1997, 2009), 3: range(2009, 2024)}
UKCPR = HERE.parent / "ExternalData" / "ukcpr_national_welfare_data_1980_2024_jan26update.xlsx"
TAXSIM_CACHE = Path(os.environ.get("IGE_DATA", HERE / "data")) / "taxsim_paperA.csv"
YEARS = range(1984, 2024)


def defl(year):
    """Factor converting nominal dollars of `year` into 2000 dollars (CPI-U)."""
    return CPI[2000] / CPI[year]


# =====================================================================================================================
# EITC (nominal). year -> {n: (phase-in rate, maximum credit, phase-out rate, phase-out start unmarried,
#                              phase-out start married filing jointly)}, n = 0, 1, 2, 3 (3 = three or more).
# =====================================================================================================================
def _eitc_table():
    t = {}
    z = (0.0, 0.0, 0.0, 0.0, 0.0)

    def one(r, mx, ro, ps):                                   # one schedule for families with children (to 1990)
        return {0: z, 1: (r, mx, ro, ps, ps), 2: (r, mx, ro, ps, ps), 3: (r, mx, ro, ps, ps)}
    # CRS RL31768 Table 8 / R44825 Table B-1 (https://policyarchive.org/download/19357)
    t[1984] = one(0.10, 500, 0.125, 6000)
    t[1985] = one(0.11, 550, 0.1222, 6500)                    # 11% / $550 (R44825, UKCPR, P.L. 98-369)
    t[1986] = one(0.11, 550, 0.1222, 6500)
    t[1987] = one(0.14, 851, 0.10, 6920)
    t[1988] = one(0.14, 874, 0.10, 9840)
    t[1989] = one(0.14, 910, 0.10, 10240)
    t[1990] = one(0.14, 953, 0.10, 10730)
    for y, (r1, m1, o1, r2, m2, o2, ps) in {               # supplemental young-child / health credits not included
            1991: (0.167, 1192, 0.1193, 0.173, 1235, 0.1236, 11250),
            1992: (0.176, 1324, 0.1257, 0.184, 1384, 0.1314, 11840),
            1993: (0.185, 1434, 0.1321, 0.195, 1511, 0.1393, 12200)}.items():
        t[y] = {0: z, 1: (r1, m1, o1, ps, ps), 2: (r2, m2, o2, ps, ps), 3: (r2, m2, o2, ps, ps)}
    t[1994] = {0: (0.0765, 306, 0.0765, 5000, 5000), 1: (0.263, 2038, 0.1598, 11000, 11000),
               2: (0.30, 2528, 0.1768, 11000, 11000), 3: (0.30, 2528, 0.1768, 11000, 11000)}
    t[1995] = {0: (0.0765, 314, 0.0765, 5130, 5130), 1: (0.34, 2094, 0.1598, 11290, 11290),
               2: (0.36, 3110, 0.2022, 11290, 11290), 3: (0.36, 3110, 0.2022, 11290, 11290)}
    # 1996-2023: phase-in 7.65 / 34 / 40 / 40 (45 for 3+ from 2009) %, phase-out 7.65 / 15.98 / 21.06 / 21.06 %.
    # year: (max0, ps0 single, ps0 MFJ, max1, max2, max3, ps1+ single, ps1+ MFJ)
    rows = {
        # CRS RL31768 Table 8 (married supplement: +1,000 2002-04, +2,000 2005-07, notes b and c)
        1996: (323, 5300, 5300, 2152, 3556, 3556, 11650, 11650),
        1997: (332, 5450, 5450, 2210, 3656, 3656, 11950, 11950),
        1998: (341, 5600, 5600, 2271, 3756, 3756, 12300, 12300),
        1999: (347, 5700, 5700, 2312, 3816, 3816, 12500, 12500),
        2000: (353, 5800, 5800, 2353, 3888, 3888, 12700, 12700),
        2001: (364, 5950, 5950, 2428, 4008, 4008, 13100, 13100),
        2002: (376, 6100, 7100, 2506, 4140, 4140, 13550, 14550),
        2003: (382, 6240, 7240, 2547, 4204, 4204, 13730, 14730),
        2004: (390, 6390, 7390, 2604, 4300, 4300, 14040, 15040),
        2005: (399, 6530, 8530, 2662, 4400, 4400, 14370, 16370),
        2006: (412, 6740, 8740, 2747, 4536, 4536, 14810, 16810),
        2007: (428, 7000, 9000, 2853, 4716, 4716, 15390, 17390),
        # IRS Rev. Procs (https://www.irs.gov/pub/irs-drop/rp-YY-NN.pdf) / Publication 596
        2008: (438, 7160, 10160, 2917, 4824, 4824, 15740, 18740),      # Rev. Proc. 2007-66
        2009: (457, 7470, 12470, 3043, 5028, 5657, 16420, 21420),      # ARRA; Pub. 596 (2009)
        2010: (457, 7480, 12490, 3050, 5036, 5666, 16450, 21460),      # Rev. Proc. 2009-50
        2011: (464, 7590, 12670, 3094, 5112, 5751, 16690, 21770),      # Rev. Proc. 2011-12
        2012: (475, 7770, 12980, 3169, 5236, 5891, 17090, 22300),      # Rev. Proc. 2011-52
        2013: (487, 7970, 13310, 3250, 5372, 6044, 17530, 22870),      # Rev. Proc. 2013-15
        2014: (496, 8110, 13540, 3305, 5460, 6143, 17830, 23260),      # Rev. Proc. 2013-35
        2015: (503, 8240, 13750, 3359, 5548, 6242, 18110, 23630),      # Rev. Proc. 2014-61
        2016: (506, 8270, 13820, 3373, 5572, 6269, 18190, 23740),      # Rev. Proc. 2015-53
        2017: (510, 8340, 13930, 3400, 5616, 6318, 18340, 23930),      # Rev. Proc. 2016-55
        2018: (519, 8490, 14170, 3461, 5716, 6431, 18660, 24350),      # Rev. Proc. 2018-18 via Pub. 596 (2018)
        2019: (529, 8650, 14450, 3526, 5828, 6557, 19030, 24820),      # Rev. Proc. 2018-57
        2020: (538, 8790, 14680, 3584, 5920, 6660, 19330, 25220),      # Rev. Proc. 2019-44
        2021: (1502, 11610, 17560, 3618, 5980, 6728, 19520, 25470),    # Rev. Proc. 2020-45; ARPA childless, Pub. 596
        2022: (560, 9160, 15290, 3733, 6164, 6935, 20130, 26260),      # Rev. Proc. 2021-45
        2023: (600, 9800, 16370, 3995, 6604, 7430, 21560, 28120),      # Rev. Proc. 2022-38
    }
    for y, (m0, p0, p0j, m1, m2, m3, p1, p1j) in rows.items():
        r0 = 0.153 if y == 2021 else 0.0765
        r3 = 0.45 if y >= 2009 else 0.40
        t[y] = {0: (r0, m0, r0, p0, p0j), 1: (0.34, m1, 0.1598, p1, p1j), 2: (0.40, m2, 0.2106, p1, p1j),
                3: (r3, m3, 0.2106, p1, p1j)}
    return t


EITC = _eitc_table()

# the minimal version's table (from memory), kept only for the comparison table in the md
EITC_MEMORY_DIFFS = {
    "1996-2002 phase-out start (n >= 1, unmarried)": "statutory amounts 11,610 ... 13,520 -> indexed 11,650 ... 13,550",
    "1996-2000, 2002 childless phase-out start": "5,280 / 5,430 / 5,570 / 5,670 / 5,770 / 6,150 -> 5,300 / 5,450 / "
                                                  "5,600 / 5,700 / 5,800 / 6,100",
    "2018 MFJ phase-out start": "24,340 / 14,170 -> 24,350 / 14,170",
    "2019 MFJ phase-out start (n >= 1)": "24,830 -> 24,820",
    "2015 / 2017 / 2023 childless MFJ start": "13,760 / 13,930 / 16,360 -> 13,750 / 13,930 / 16,370",
}

# =====================================================================================================================
# SNAP (nominal, 48 states + DC), by fiscal year (October y-1 to September y)
# =====================================================================================================================
TFP_FACTOR = {5: 1.1875, 6: 1.425, 7: 1.575, 8: 1.80}       # statutory size factors relative to four persons
# official full tables (sizes 1-8): FNS (FY2006+), CDSS ACLs, Federal Register 1995. FY -> [(first month, allotments)]
SNAP_ALLOT_OFFICIAL = {
    1987: [(10, [81, 149, 214, 271, 322, 387, 428, 489])],                        # ACL 86-88
    1992: [(10, [111, 203, 292, 370, 440, 528, 584, 667])],                       # ACL 91-97
    1993: [(10, [111, 203, 292, 370, 440, 528, 584, 667])],                       # ACL 92-79 (no change)
    1995: [(10, [115, 212, 304, 386, 459, 550, 608, 695])],                       # ACL 94-73; FR 11 Jan 1995
    1996: [(10, [119, 218, 313, 397, 472, 566, 626, 716])],                       # ACL 95-64
    2006: [(10, [152, 278, 399, 506, 601, 722, 798, 912])],
    2007: [(10, [155, 284, 408, 518, 615, 738, 816, 932])],
    2008: [(10, [162, 298, 426, 542, 643, 772, 853, 975])],
    2009: [(10, [176, 323, 463, 588, 698, 838, 926, 1058]), (4, [200, 367, 526, 668, 793, 952, 1052, 1202])],
    2010: [(10, [200, 367, 526, 668, 793, 952, 1052, 1202])],
    2011: [(10, [200, 367, 526, 668, 793, 952, 1052, 1202])],
    2012: [(10, [200, 367, 526, 668, 793, 952, 1052, 1202])],
    2013: [(10, [200, 367, 526, 668, 793, 952, 1052, 1202])],
    2014: [(10, [200, 367, 526, 668, 793, 952, 1052, 1202]), (11, [189, 347, 497, 632, 750, 900, 995, 1137])],
    2015: [(10, [194, 357, 511, 649, 771, 925, 1022, 1169])],
    2016: [(10, [194, 357, 511, 649, 771, 925, 1022, 1169])],
    2017: [(10, [194, 357, 511, 649, 771, 925, 1022, 1169])],
    2018: [(10, [192, 352, 504, 640, 760, 913, 1009, 1153])],
    2019: [(10, [192, 353, 505, 642, 762, 914, 1011, 1155])],
    2020: [(10, [194, 355, 509, 646, 768, 921, 1018, 1164])],
    2021: [(10, [204, 374, 535, 680, 807, 969, 1071, 1224]),                       # Jan-Sep 2021: +15% (COVID, ARPA)
           (1, [234, 430, 616, 782, 929, 1114, 1232, 1408])],
    2022: [(10, [250, 459, 658, 835, 992, 1190, 1316, 1504])],
    2023: [(10, [281, 516, 740, 939, 1116, 1339, 1480, 1691])],
    2024: [(10, [291, 535, 766, 973, 1155, 1386, 1532, 1751])],
}
SNAP_FY1993_GREENBOOK_4 = 375                                 # contradicted by ACL 92-79 / 93-65 (see docstring)
# standard deduction by FY: {first month: (sizes 1, 2, 3, 4, 5, 6+)}; one amount for all sizes before FY2003
_one = lambda v: (v, v, v, v, v, v)                            # noqa: E731
SNAP_STD = {1984: {10: _one(89)}, 1985: {10: _one(95)}, 1986: {10: _one(98)}, 1987: {10: _one(99)},
            1988: {10: _one(102)}, 1989: {10: _one(106)}, 1990: {10: _one(111)},       # statutory reconstruction
            1991: {10: _one(116)}, 1992: {10: _one(122)}, 1993: {10: _one(127)}, 1994: {10: _one(131)},
            1995: {10: _one(134)}, 1996: {10: _one(138), 12: _one(134)},
            **{y: {10: _one(134)} for y in range(1997, 2003)},
            2003: {10: (134, 134, 134, 134, 147, 168)},                                # 2002 Farm Bill formula
            2004: {10: (134, 134, 134, 134, 149, 171)},                                # 2004 Green Book
            2005: {10: (134, 134, 134, 134, 153, 175)},                                # formula (5: FNS 153)
            2006: {10: (134, 134, 134, 134, 157, 179)}, 2007: {10: (134, 134, 134, 139, 162, 186)},
            2008: {10: (134, 134, 134, 143, 167, 191)}, 2009: {10: (144, 144, 144, 147, 172, 197)},
            2010: {10: (141, 141, 141, 153, 179, 205)}, 2011: {10: (142, 142, 142, 153, 179, 205)},
            2012: {10: (147, 147, 147, 155, 181, 208)}, 2013: {10: (149, 149, 149, 160, 187, 214)},
            2014: {10: (152, 152, 152, 163, 191, 219)}, 2015: {10: (155, 155, 155, 165, 193, 221)},
            2016: {10: (155, 155, 155, 168, 197, 226)}, 2017: {10: (157, 157, 157, 168, 197, 226)},
            2018: {10: (160, 160, 160, 170, 199, 228)}, 2019: {10: (164, 164, 164, 174, 204, 234)},
            2020: {10: (167, 167, 167, 178, 209, 240)}, 2021: {10: (167, 167, 167, 181, 212, 243)},
            2022: {10: (177, 177, 177, 184, 215, 246)}, 2023: {10: (193, 193, 193, 193, 225, 258)},
            2024: {10: (198, 198, 198, 208, 244, 279)}}
STD_STATUS = {1988: "statutory reconstruction", 1989: "statutory reconstruction", 1990: "statutory reconstruction",
              2003: "2002 Farm Bill formula", 2005: "2002 Farm Bill formula (5-person amount = FNS)"}
SNAP_ASSET = {**{y: 2000 for y in range(1984, 2015)}, **{y: 2250 for y in range(2015, 2022)}, 2022: 2500,
              2023: 2750, 2024: 2750}

# HHS poverty guidelines, 48 states: year -> (one person, increment per additional person) (ASPE)
POVERTY = {1983: (4860, 1680), 1984: (4980, 1740), 1985: (5250, 1800), 1986: (5360, 1880), 1987: (5500, 1900),
           1988: (5770, 1960), 1989: (5980, 2040), 1990: (6280, 2140), 1991: (6620, 2260), 1992: (6810, 2380),
           1993: (6970, 2460), 1994: (7360, 2480), 1995: (7470, 2560), 1996: (7740, 2620), 1997: (7890, 2720),
           1998: (8050, 2800), 1999: (8240, 2820), 2000: (8350, 2900), 2001: (8590, 3020), 2002: (8860, 3080),
           2003: (8980, 3140), 2004: (9310, 3180), 2005: (9570, 3260), 2006: (9800, 3400), 2007: (10210, 3480),
           2008: (10400, 3600), 2009: (10830, 3740), 2010: (10830, 3740), 2011: (10890, 3820), 2012: (11170, 3960),
           2013: (11490, 4020), 2014: (11670, 4060), 2015: (11770, 4160), 2016: (11880, 4140), 2017: (12060, 4180),
           2018: (12140, 4320), 2019: (12490, 4420), 2020: (12760, 4480), 2021: (12880, 4540), 2022: (13590, 4720),
           2023: (14580, 5140)}
POVERTY_2016 = [11880, 16020, 20160, 24300, 28440, 32580, 36730, 40890]       # size-specific (increments vary)


def poverty(year, size):
    if year == 2016:
        return POVERTY_2016[size - 1]
    b, inc = POVERTY[year]
    return b + inc * (size - 1)


def snap_allot_tables():
    """FY -> [(first month, [a1..a8], source)] for FY1984-FY2024."""
    u = pd.read_excel(UKCPR, sheet_name="Data")
    cols = [f"FS/SNAP Benefit for {k}-person family" for k in (1, 2, 3, 4)]
    uk = u[u["state_name"].isin(["VA", "OH", "PA"])].groupby("year")[cols].median()      # 48-state amounts
    tab, check = {}, []
    for fy in range(1984, 2025):
        if fy in SNAP_ALLOT_OFFICIAL:
            tab[fy] = [(m, a, "official") for m, a in SNAP_ALLOT_OFFICIAL[fy]]
            if fy in uk.index:
                check.append(dict(fy=fy, official4=SNAP_ALLOT_OFFICIAL[fy][0][1][3], ukcpr4=float(uk.loc[fy, cols[3]])))
            continue
        a14 = [float(uk.loc[fy, c]) for c in cols]
        a58 = [float(np.floor((a14[3] + 0.5) * TFP_FACTOR[s])) for s in (5, 6, 7, 8)]
        tab[fy] = [(10, a14 + a58, "UKCPR 1-4; TFP factors 5-8")]
    return tab, pd.DataFrame(check)


def snap_month(y, mth, allot):
    """Nominal SNAP parameters in calendar month (y, mth)."""
    fy = y + 1 if mth >= 10 else y
    order = lambda m: (m - 10) % 12                                  # noqa: E731  months since October
    seg = [s for s in allot[fy] if order(s[0]) <= order(mth)][-1]
    std = [v for m, v in sorted(SNAP_STD[fy].items(), key=lambda kv: order(kv[0])) if order(m) <= order(mth)][-1]
    D = [std[min(s, 6) - 1] for s in range(1, 9)]
    G = [np.ceil(1.3 * poverty(fy - 1, s) / 12.0) for s in range(1, 9)]
    return np.array(seg[1], float), np.array(D, float), np.array(G, float), float(SNAP_ASSET[fy])


# =====================================================================================================================
# Tax: TAXSIM 35
# =====================================================================================================================
YGRID = np.exp(np.linspace(np.log(5000), np.log(300000), 200))         # 2000 dollars


def taxsim(use_cache=False):
    if use_cache and TAXSIM_CACHE.exists():
        return pd.read_csv(TAXSIM_CACHE)
    rows = []
    for y in YEARS:
        for i, y2000 in enumerate(YGRID):
            ynom = y2000 / defl(y)
            rows.append((y * 1000 + i, y, 0, 2, 2, 5, 10, 0, round(0.65 * ynom, 2), round(0.35 * ynom, 2), 2))
    inp = pd.DataFrame(rows, columns=["taxsimid", "year", "state", "mstat", "depx", "age1", "age2", "age3", "pwages",
                                      "swages", "idtl"])
    parts = []
    with tempfile.TemporaryDirectory() as td:                 # batches of 1,000 records (longer uploads get cut)
        for k in range(0, len(inp), 1000):
            f = Path(td) / "txpydata.csv"
            inp.iloc[k:k + 1000].to_csv(f, index=False)
            r = subprocess.run(["curl", "-s", "-m", "600", "-F", f"txpydata.raw=@{f}",
                                "https://taxsim.nber.org/taxsim35/redirect.cgi"], capture_output=True, text=True)
            q = pd.read_csv(io.StringIO(r.stdout))
            q.columns = [c.strip() for c in q.columns]
            parts.append(q)
    out = pd.concat(parts, ignore_index=True)
    out["taxsimid"] = out["taxsimid"].astype(float).astype(int)
    out = out.merge(inp[["taxsimid", "pwages", "swages"]], on="taxsimid")
    out.to_csv(TAXSIM_CACHE, index=False)
    return out


def fit_tax(ts):
    res = {}
    for y, q in ts.groupby("year"):
        ynom = (q["pwages"] + q["swages"]).to_numpy(float)
        mwp = 0.0
        if y in (2009, 2010):
            mwp = np.maximum(np.minimum(0.062 * ynom, 800.0) - 0.02 * np.maximum(ynom - 150000.0, 0.0), 0.0)
        T = q["fiitax"].to_numpy(float) + q["v25"].to_numpy(float) + q["v45"].to_numpy(float) + mwp \
            + q["tfica"].to_numpy(float)
        d = defl(int(y))
        lhs, rhs = np.log((ynom - T) * d), np.log(ynom * d)
        X = np.column_stack([np.ones_like(rhs), rhs])
        b, *_ = np.linalg.lstsq(X, lhs, rcond=None)
        e = lhs - X @ b
        res[int(y)] = dict(chi=float(1.0 - np.exp(b[0])), mu=float(1.0 - b[1]), r2=float(1 - e.var() / lhs.var()),
                           avg_rate_40k=float(np.interp(np.log(40000), rhs, T / ynom)))
    return pd.DataFrame(res).T


# =====================================================================================================================
def state_weights():
    """CPS couples' state shares by year (IGE/62); 1994 shares for 1984-93."""
    f = HERE / "output" / "cps_couple_state_shares.csv"
    if not f.exists():
        return None
    s = pd.read_csv(f)
    w = {int(y): g.set_index("state")["share"] for y, g in s.groupby("year")}
    for y in range(1984, 1994):
        w[y] = w[1994]
    return w


def weighted_by_state(df, val, w, years):
    out = {}
    for y in years:
        q = df[(df["year"] == y) & df[val].notna()].set_index("state_fips")[val]
        ww = w[y].reindex(q.index).fillna(0.0)
        out[y] = float((q * ww).sum() / ww.sum())
    return pd.Series(out)


# =====================================================================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-taxsim", action="store_true", help="use the cached TAXSIM output")
    a = ap.parse_args()
    W = state_weights()
    wsrc = "CPS couples' state distribution (IGE/62; 1994 shares for 1984-93)"
    u = pd.read_excel(UKCPR, sheet_name="Data")
    if W is None:                                             # fallback: UKCPR population weights
        wsrc = "FALLBACK: UKCPR state population (output/cps_couple_state_shares.csv missing: run IGE/62)"
        W = {int(y): g.set_index("state_fips")["Population"] / g["Population"].sum() for y, g in u.groupby("year")}
    # ---------------- q_UI
    q_ui, q_src = 0.523, "FALLBACK: DWS displaced husbands 0.523 (IGE/39)"
    tp = HERE / "output" / "paperA_targets.csv"
    if tp.exists():
        tt = pd.read_csv(tp).set_index("id")
        if {"dws_ui_h", "dws_ui_w"} <= set(tt.index):
            q_ui = float((tt.loc["dws_ui_h", "value"] + tt.loc["dws_ui_w", "value"]) / 2)
            q_src = (f"mean of DWS UI receipt of displaced husbands {tt.loc['dws_ui_h', 'value']:.3f} and wives "
                     f"{tt.loc['dws_ui_w', 'value']:.3f} (IGE/60)")
    # ---------------- UI cap and AFDC/TANF (state means)
    ui = pd.read_csv(Path(os.environ.get("IGE_DATA", HERE / "data")) / "ui_generosity.csv")
    ui_w = weighted_by_state(ui, "max_wba_2000", W, YEARS) * 52.0 / 12.0
    ui_u = ui.groupby("year")["max_wba_2000"].mean().reindex(list(YEARS)) * 52.0 / 12.0
    af = u.rename(columns={"AFDC/TANF Benefit for 3-person family": "afdc3"})[["state_fips", "year", "afdc3",
                                                                              "Population"]]
    af_w = weighted_by_state(af, "afdc3", W, YEARS)
    af_med = af.groupby("year")["afdc3"].median().reindex(list(YEARS))
    af_pop = af.groupby("year").apply(lambda g: (g.afdc3 * g.Population).sum() / g.Population.sum()).reindex(
        list(YEARS))
    # ---------------- tax
    ts = taxsim(use_cache=a.no_taxsim)
    tax = fit_tax(ts)
    # ---------------- SNAP month by month
    allot, snap_check = snap_allot_tables()
    rows = []
    for y in YEARS:
        d = defl(y)
        r = {"year": y}
        acc = [np.zeros(8), np.zeros(8), np.zeros(8), 0.0]
        for mth in range(1, 13):
            A, D, G, AL = snap_month(y, mth, allot)
            acc[0] += A / 12
            acc[1] += D / 12
            acc[2] += G / 12
            acc[3] += AL / 12
        for s in range(1, 9):
            r[f"snap_A{s}"], r[f"snap_D{s}"], r[f"snap_G{s}"] = acc[0][s - 1] * d, acc[1][s - 1] * d, acc[2][s - 1] * d
            r[f"snap_A{s}_nom"], r[f"snap_D{s}_nom"] = acc[0][s - 1], acc[1][s - 1]
        r["snap_asset_limit"] = acc[3] * d
        for n in range(4):
            r_in, mx, r_out, ps, psj = EITC[y][n]
            r[f"eitc{n}_in"], r[f"eitc{n}_max"], r[f"eitc{n}_out"] = r_in, mx * d, r_out
            r[f"eitc{n}_ps_single"], r[f"eitc{n}_ps_mfj"] = ps * d, psj * d
            r[f"eitc{n}_max_nom"], r[f"eitc{n}_ps_single_nom"], r[f"eitc{n}_ps_mfj_nom"] = mx, ps, psj
        r["ui_cap_month"], r["ui_cap_month_unweighted"] = float(ui_w.loc[y]), float(ui_u.loc[y])
        r["afdc3"], r["afdc3_nom"] = float(af_w.loc[y]) * d, float(af_w.loc[y])
        r["afdc3_median_nom"], r["afdc3_popw_nom"] = float(af_med.loc[y]), float(af_pop.loc[y])
        r["tax_chi"], r["tax_mu"], r["tax_r2"] = (float(tax.loc[y, k]) for k in ("chi", "mu", "r2"))
        r["tax_avg_rate_40k"] = float(tax.loc[y, "avg_rate_40k"])
        rows.append(r)
    tab = pd.DataFrame(rows).set_index("year")
    # the minimal (memory) version's era files, kept once in output/ for the comparison table
    mem = HERE / "output" / "policy_schedules_memory_version.json"
    old = {int(k): v for k, v in json.loads(mem.read_text()).items()} if mem.exists() else {}
    if not old:
        for e in ERAS:
            p = OUT_DIR / f"schedules_era{e}.json"
            if p.exists():
                o = json.loads(p.read_text())
                if "verified" not in json.dumps(o.get("status", {})):
                    old[e] = o
        if old:
            mem.write_text(json.dumps(old, indent=1))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    status = {"eitc": "verified: CRS RL31768 Table 8 (1984-2007), IRS Rev. Procs 2007-66 ... 2022-38 and Pub. 596 "
                      "(2008-2023); rates and maxima cross-checked with CRS R44825 Table B-1 and UKCPR",
              "snap": "verified: FNS tables FY2006-FY2024, CDSS ACLs / FR / Green Book / UKCPR before; standard "
                      "deduction FY1988-90, FY2003, FY2005 reconstructed by statute (see 61 docstring); sizes 5-8 by "
                      "TFP factors in years without an official table",
              "tax": "verified: NBER TAXSIM 35 yearly fits (federal income tax with CTC, without EITC / rebates / "
                     "Making Work Pay, + employee payroll tax), era mean of yearly (chi, mu)",
              "c_min": "verified: UKCPR AFDC/TANF 3-person maximum by state (Green Book / Urban WRD), " + wsrc,
              "ui_cap": "IGE/12b max_wba_2000 x 52/12, " + wsrc,
              "q_ui": q_src}
    eras_out = {}
    for e, yrs in ERAS.items():
        sub = tab.loc[list(yrs)]
        sch = {"era": e, "years": [yrs[0], yrs[-1]], "units": "2000 dollars; monthly unless 'annual'",
               "tax": {"chi": float(sub["tax_chi"].mean()), "mu": float(sub["tax_mu"].mean()),
                       "r2": float(sub["tax_r2"].mean()), "year": f"{yrs[0]}-{yrs[-1]} mean",
                       "status": "TAXSIM 35 era mean"},
               "eitc_annual": {}, "snap": {}, "ui": {}, "status": status}
        for n in range(4):
            sch["eitc_annual"][str(n)] = {"in": float(sub[f"eitc{n}_in"].mean()),
                                          "max": float(sub[f"eitc{n}_max"].mean()),
                                          "out": float(sub[f"eitc{n}_out"].mean()),
                                          "ps_single": float(sub[f"eitc{n}_ps_single"].mean()),
                                          "ps_mfj": float(sub[f"eitc{n}_ps_mfj"].mean())}
        sch["snap"] = {"A": [float(sub[f"snap_A{s}"].mean()) for s in range(1, 9)],
                       "D": [float(sub[f"snap_D{s}"].mean()) for s in range(1, 9)],
                       "gross_limit": [float(sub[f"snap_G{s}"].mean()) for s in range(1, 9)],
                       "asset_limit": float(sub["snap_asset_limit"].mean()),
                       "earned_deduction": 0.2, "benefit_reduction": 0.3}
        sch["ui"] = {"cap_month": float(sub["ui_cap_month"].mean()), "rho": 0.5, "expiry": 1.0 / 6.0, "q_ui": q_ui}
        sch["c_min_family3"] = float(sub["afdc3"].mean())
        if e == 3:                                            # the 2021 ARPA child credit is a one-year outlier
            # Lead's decision (2026-10-18): the era-3 tax schedule excludes the one-year ARPA 2021 child credit;
            # the mean including 2021 is kept for reference as chi_with2021 / mu_with2021.
            x = sub.drop(index=2021)
            sch["tax"]["chi_with2021"], sch["tax"]["mu_with2021"] = sch["tax"]["chi"], sch["tax"]["mu"]
            sch["tax"]["chi"], sch["tax"]["mu"] = float(x["tax_chi"].mean()), float(x["tax_mu"].mean())
            sch["tax"]["chi_ex2021"], sch["tax"]["mu_ex2021"] = sch["tax"]["chi"], sch["tax"]["mu"]
        (OUT_DIR / f"schedules_era{e}.json").write_text(json.dumps(sch, indent=1))
        eras_out[e] = sch
    write_md(tab, eras_out, old, snap_check, wsrc, q_ui)


def write_md(tab, eras, old, snap_check, wsrc, q_ui):
    L = ["# Policy schedules by era (IGE/61.PolicySchedules.py, verified version)", "",
         "2000 dollars (CPI-U, IGE/common.py; 2023-24 BLS). Era value = mean over the era's calendar years; SNAP built "
         "month by month from the fiscal-year tables. Sources with URLs: the script's docstring and the comments next "
         "to each table. Values marked 'reconstructed' were not found in an official table and follow the statutory "
         "rule (listed under 'Unverified').", ""]
    L += ["## Era values written to paperA_model/inputs/schedules_era*.json, verified vs the minimal version", "",
          "| Parameter | Era 1 new | Era 1 old | Era 2 new | Era 2 old | Era 3 new | Era 3 old |",
          "|---|---:|---:|---:|---:|---:|---:|"]

    def g(sch, path):
        x = sch
        for k in path:
            x = x[k]
        return x
    items = [("tax chi", ("tax", "chi"), 4), ("tax mu", ("tax", "mu"), 4)]
    for n in range(4):
        for k in ("in", "max", "out", "ps_single", "ps_mfj"):
            items.append((f"EITC n={n} {k} (annual)", ("eitc_annual", str(n), k), 4 if k in ("in", "out") else 0))
    for s in (1, 2, 3, 4, 5, 6):
        items += [(f"SNAP max allotment, {s} persons", ("snap", "A", s - 1), 1),
                  (f"SNAP standard deduction, {s} persons", ("snap", "D", s - 1), 1),
                  (f"SNAP gross-income limit, {s} persons", ("snap", "gross_limit", s - 1), 0)]
    items += [("SNAP asset limit", ("snap", "asset_limit"), 0), ("UI cap (monthly)", ("ui", "cap_month"), 0),
              ("c_min (AFDC/TANF 3 persons)", ("c_min_family3",), 1)]
    for lab, path, dg in items:
        cells = []
        for e in (1, 2, 3):
            nv = g(eras[e], path)
            ov = g(old[e], path) if e in old else np.nan
            cells += [f"{nv:.{dg}f}", f"{ov:.{dg}f}" if np.isfinite(ov) else ""]
        L.append(f"| {lab} | " + " | ".join(cells) + " |")
    L += ["", f"UI cap and c_min weights: {wsrc}. q_UI = {q_ui:.3f} (unchanged).", ""]
    L += ["## What changed against the minimal (memory) version", "",
          "- EITC: rates and maximum credits were correct in every year (CRS, UKCPR agree); phase-out starts corrected:"]
    L += [f"  - {k}: {v}" for k, v in EITC_MEMORY_DIFFS.items()]
    L += ["  - the married-joint supplement is now taken year by year from the Rev. Procs (it differs by $10 between "
          "childless and other filers in some years) instead of one 'extra' amount.",
          "- SNAP: the minimal version scaled one remembered four-person series by FY2023 size ratios and interpolated "
          "the standard deduction between remembered anchors; now every fiscal year's official allotments and "
          "deductions (by size), month-weighted. Four-person maxima that were wrong in the memory table: FY1997 397 "
          "(400), FY2000 434 (426), FY2005 506 (499), FY2006 499 (506), FY2009 628 (588 Oct-Mar, 668 Apr-Sep), "
          "FY2021 757 (680 Oct-Dec, 782 Jan-Sep); the gross-income test now uses the previous year's guideline (FNS "
          "practice) and the asset limit follows the FY2015 / FY2022 / FY2023 increases ($2,250 / $2,500 / $2,750) "
          "instead of a constant $2,000.",
          "- Tax: TAXSIM 35 every year (era mean of 13 / 12 / 15 yearly fits) instead of one statutory year per era "
          "(1990 / 2003 / 2015) from a coded bracket calculator.",
          "- c_min: state AFDC/TANF maxima weighted by the CPS couples' states, every year, instead of nine remembered "
          "median-state anchors.",
          "- UI cap: weighted by the CPS couples' states instead of the unweighted state mean.",
          "- Poverty guidelines: all years verified against ASPE (no change; 2016 now size-specific).", ""]
    L += ["## Unverified or reconstructed (flags)", "",
          "- SNAP standard deduction FY1988-FY1990 ($102 / $106 / $111): no official table found online; statutory "
          "CPI-U-less-food indexing of the verified FY1987 $99 (the same rule reproduces the verified FY1991 and "
          "FY1992 amounts).",
          "- SNAP standard deduction FY2003 and FY2005 (sizes 5 and 6+ in FY2003, 6+ in FY2005): 2002 Farm Bill formula "
          "(8.31% of the size's poverty-line income standard, $134 minimum); it reproduces FY2004 and FY2006-08.",
          "- SNAP maximum allotments for 5-8 persons in FY1984-86, 1988-91, 1994, 1997-2005: statutory TFP size factors "
          "applied to the four-person amount (within $1 of the official tables in the years that have them); 1-4 "
          "persons in those years from the UKCPR compilation (it matches FNS exactly in FY2006-24 and the CDSS / FR / "
          "Green Book values except FY1993, see docstring).",
          "- EITC 2009 married supplement and 3+ child amounts, 2018 phase-out starts and the 2021 childless (ARPA) "
          "parameters are read from IRS Publication 596 (the completed phase-out amounts) because the Rev. Proc. was "
          "superseded (2009, 2021) or not downloadable (2018-18): start = completed amount - max / phase-out rate, "
          "rounded to $10.",
          "- EITC 1991-93 supplemental young-child and health-insurance credits are not included (as in the minimal "
          "version and in CRS's maxima).",
          "- AFDC/TANF maxima: the UKCPR compilation is a secondary source (spot checks: CA / NY / TX / MS 1990 = 694 / "
          "577 / 184 / 120, the Green Book values).",
          "- TAXSIM: federal only (no state income tax), as the plan specifies; 2008 rebates are not in TAXSIM's "
          "fiitax; the 2001 rate-reduction credit is not modelled.",
          f"- Tax, era 3: 2021 (ARPA fully refundable child credit of $3,000-3,600 a child) is an outlier year (chi "
          f"{tab.loc[2021, 'tax_chi']:.2f}, mu {tab.loc[2021, 'tax_mu']:.3f}); the plan's era mean includes it (chi "
          f"{eras[3]['tax']['chi']:.3f}, mu {eras[3]['tax']['mu']:.4f}); without 2021: chi {eras[3]['tax']['chi_ex2021']:.3f}, "
          f"mu {eras[3]['tax']['mu_ex2021']:.4f} (stored as chi_ex2021 / mu_ex2021, not read by the model). Lead's "
          "decision. The refundable additional child tax credit (from 1998; threshold cut to $3,000 by ARRA in 2009) "
          "is why every TAXSIM fit is more progressive than the minimal version's non-refundable-only calculator "
          "(e.g. 2015: chi -1.88 vs -0.86).", ""]
    L += ["## SNAP four-person maximum: official vs UKCPR (fiscal years with an official table)", "",
          snap_check.to_markdown(index=False), ""]
    cols = ["eitc1_max_nom", "eitc2_max_nom", "eitc3_max_nom", "eitc2_ps_single_nom", "eitc2_ps_mfj_nom",
            "eitc0_max_nom", "eitc0_ps_mfj_nom", "snap_A4_nom", "snap_D4_nom", "snap_G4", "snap_asset_limit",
            "afdc3_nom", "afdc3_median_nom", "afdc3_popw_nom", "ui_cap_month", "ui_cap_month_unweighted", "tax_chi",
            "tax_mu", "tax_r2", "tax_avg_rate_40k"]
    L += ["## By calendar year (nominal unless the column says 2000 $; SNAP gross limit, asset limit and UI cap in 2000 $)",
          "", tab[cols].round(4).to_markdown(), ""]
    (HERE / "output" / "policy_schedules.md").write_text("\n".join(L), encoding="utf8")
    print("\n".join(L[:12 + len(items) + 4]))


if __name__ == "__main__":
    main()
