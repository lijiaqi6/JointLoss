r"""State x year panel of unemployment-insurance (UI) generosity, 1976-2024 (2026-10-17).

Writes data/ui_generosity.csv (51 states incl. DC x 1976-2024) and output/ui_generosity_checks.md.
Raw downloads (untrusted data, never executed) are cached in data/ext/dol_ui/ (git-ignored with data/).

SOURCES
(1) Statutory parameters - US DOL, ETA, Office of Unemployment Insurance, "Significant Provisions of State Unemployment
    Insurance Laws", semiannual (January / July issues). Archive: https://oui.doleta.gov/unemploy/statelaws.asp ; files
    https://oui.doleta.gov/unemploy/content/sigpros/<decade>/July<year>.pdf (e.g. .../1980-1989/July1985.pdf; the
    file list per decade comes from https://oui.doleta.gov/unemploy/statelaws_search.php). The July issue of year t
    (laws in effect early July) gives the year-t values: maximum and minimum weekly benefit amount (WBA) for total
    unemployment, maximum number of benefit weeks, and whether the WBA formula has dependents' allowances (DA).
    * 1976-1999: the PDFs are scanned images without a text layer and there is no machine-readable DOL series of the
      maximum WBA (checked: DOL data downloads, ET Handbook 394, the BAM replacement-rate query, UKCPR). The values
      below (SCAN) were transcribed by reading each July page image (51 states x 24 issues). Where a scan was
      unreadable the row carries a note; the weeks column of July 1977 p.1 is clipped and carried from 1976.
    * 2000-2024: text-layer PDFs; read here from word positions (poppler `pdftotext -bbox`), cells assigned to columns
      from the header words ("Min./Mini-", "Max./Maxi-", "Weeks"/"Payable", "Earnings"); a few cells that the
      positional parser cannot read, and three evident misprints (KY 2001, VA 2002, WA 2003: out of line with
      both adjacent January issues), are set in OVERRIDES (each checked against the PDFs). The July 2000 issue has
      no text labels for TN-WY: those nine rows were transcribed from the page image (in SCAN). Check: the January
      issues 2000-2025 are parsed the same way and every July maximum is compared with the January values of the
      same and the next year (7 of 1,275 state-years outside that range; listed in the checks file).
    * Missing: MA 1999 (the July 1999 table prints Maryland's $250 in the Massachusetts row; January 1999 issue not
      on the DOL site).
    Conventions. When the table gives a range "a-b" in a state with dependents' allowances, a = maximum WBA without
    and b = with the largest allowance ("When 2 amounts given, higher includes da", footnote 4 of the table): max_wba =
    a, max_wba_dep = b. States with two alternative maxima that are not DA (MN from 1999: maximum based on high-quarter
    vs total base-period wages; CO from 2011: "or" higher maximum for claimants with longer/higher earnings) get the
    higher one in max_wba (note in law_note). Values announced in the table as effective later in the year are ignored.
    max_duration_weeks = maximum weeks of regular state benefits ("Benefit weeks for total unemployment, Max."; plant-
    closing / training extensions noted in the table, e.g. Iowa's 39 weeks, are not used).
(2) Average weekly benefit (AWB) - DOL ETA 5159 "Claims and Payment Activities", monthly state files:
    https://oui.doleta.gov/unemploy/csv/ar5159.csv (layout: https://oui.doleta.gov/unemploy/DataDownloads.asp ;
    item definitions: UI Reports Handbook 401, https://oui.doleta.gov/dmstree/handbooks/401/i_2.htm). Columns
    c38-c43 are weeks compensated (state UI all / total unemployment / interstate / UCFE+UCX / UCFE / UCX) and
    c45-c50 the matching amounts paid; awb = sum(c46) / sum(c39) over the calendar year = state UI benefits paid for
    weeks of total unemployment per week compensated (the DOL definition of the AWB; it reproduces ET Handbook 394,
    e.g. Alabama 1985: 97.50). 1971-2025, all states. Only complete calendar years (12 monthly reports) are used.
(3) Claimants at the maximum - DOL ETA 218 "Benefit Rights and Experience", quarterly:
    https://oui.doleta.gov/unemploy/csv/ar218.csv (definitions: Handbook 401, https://oui.doleta.gov/dmstree/
    handbooks/401/i_5.htm). c4 = claimants establishing benefit years, c5 = of whom eligible for the maximum WBA
    (augmented amount where DA apply), c9 = first payments by potential duration (total), c28 = number at maximum
    potential duration, c29 = average potential duration (weeks). Annual: share_max_wba = sum c5 / sum c4,
    share_max_duration = sum c28 / sum c9, avg_potential_duration = c9-weighted mean of c29.
(4) Average weekly wage - US BEA, Regional Accounts, table SAINC30 "Economic profile", line 300 "Average wages and
    salaries" (per job, annual): https://apps.bea.gov/regional/zip/SAINC.zip ; aww = line 300 / 52. Used because DOL's
    ET Financial Data Handbook 394 (https://oui.doleta.gov/unemploy/hb394.asp, average weekly wage in covered
    employment and the AWB / AWW ratio) could not be downloaded state by state (its query page returned "Unable to
    connect!" throughout 2026-10-17); the one Handbook 394 report retrieved (Alabama, 1971-2024, saved as
    data/ext/dol_ui/hb394_AL_test.html) is used as a check:
    BEA wages per job / 52 track the Handbook's covered-employment AWW closely (see the checks file).
    repl_rate = awb / aww (DOL's "replacement ratio" concept: average weekly benefit / average weekly wage).
(5) UKCPR National Welfare Data 1980-2024 (ExternalData/ukcpr_national_welfare_data_1980_2024_jan26update.xlsx):
    re-checked 2026-10-17 - its Data sheet has no unemployment-insurance variable (only "Workers' compensation",
    the unemployment rate and welfare / EITC / minimum-wage variables). Not used.

Dollar amounts in 2000 dollars use the CPI-U dict of IGE/common.py (through 2022), extended here with the BLS CPI-U
annual averages 2023 = 304.702 and 2024 = 313.689 (1982-84 = 100).
"""
import io
import re
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from html import unescape
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import CPI as CPI_COMMON  # noqa: E402  (read-only import)

DATA, OUT = HERE / "data", HERE / "output"
EXT = DATA / "ext" / "dol_ui"
SIGPROS, BBOX = EXT / "sigpros", EXT / "sigpros_bbox"
YEARS = range(1976, 2025)
CPI = {**CPI_COMMON, 2023: 304.702, 2024: 313.689}
UA = {"User-Agent": "Mozilla/5.0"}

FIPS = {"AL": 1, "AK": 2, "AZ": 4, "AR": 5, "CA": 6, "CO": 8, "CT": 9, "DE": 10, "DC": 11, "FL": 12, "GA": 13,
        "HI": 15, "ID": 16, "IL": 17, "IN": 18, "IA": 19, "KS": 20, "KY": 21, "LA": 22, "ME": 23, "MD": 24, "MA": 25,
        "MI": 26, "MN": 27, "MS": 28, "MO": 29, "MT": 30, "NE": 31, "NV": 32, "NH": 33, "NJ": 34, "NM": 35, "NY": 36,
        "NC": 37, "ND": 38, "OH": 39, "OK": 40, "OR": 41, "PA": 42, "RI": 44, "SC": 45, "SD": 46, "TN": 47, "TX": 48,
        "UT": 49, "VT": 50, "VA": 51, "WA": 53, "WV": 54, "WI": 55, "WY": 56}
ST = list(FIPS)
ALL_LABELS = set(ST) | {"PR", "VI"}
ALT_MAX = {"MN", "CO"}           # two alternative maxima that are not dependents' allowances (see docstring)

# ---------------------------------------------------------------------------------------------------------------------
# (1a) July issues 1976-1999 (+ July 2000 TN-WY): year state min max max_weeks dep  [# note]
#      min / max "a-b" = without - with dependents' allowances; NA = not legible / misprinted
SCAN = r"""
1976 AL 15 90 26 0
1976 AK 18-23 90-120 28 1
1976 AZ 15 85 26 0
1976 AR 15 100 26 0
1976 CA 30 104 26 0
1976 CO 25 114 26 0
1976 CT 15-20 110-165 26 1
1976 DE 20 125 26 0
1976 DC 13-14 139 34 1
1976 FL 10 82 26 0
1976 GA 27 90 26 0
1976 HI 5 112 26 0
1976 ID 17 99 26 0
1976 IL 15 106-135 26 1
1976 IN 35 69-115 26 1
1976 IA 10 116 26 0 # table shows 39 (plant-closing extension); regular 26
1976 KS 25 101 26 0
1976 KY 12 87 26 0
1976 LA 10 90 28 0
1976 ME 12-17 79-119 26 1
1976 MD 10-13 89 26 1
1976 MA 14-20 101-152 30 1
1976 MI 16-18 97-136 26 1
1976 MN 18 113 26 0
1976 MS 10 80 26 0
1976 MO 15 85 26 0
1976 MT 12 94 26 0
1976 NE 12 80 26 0
1976 NV 16 94 26 0
1976 NH 14 95 26 0
1976 NJ 20 96 26 0
1976 NM 16 78 30 0
1976 NY 20 95 26 0
1976 NC 15 97 26 0
1976 ND 15 107 26 0
1976 OH 10-16 95-150 26 1
1976 OK 16 93 26 0
1976 OR 26 102 26 0
1976 PA 13-18 125-133 30 1
1976 RI 22-27 100-120 26 1
1976 SC 10 103 26 0
1976 SD 19 89 26 0
1976 TN 14 85 26 0
1976 TX 15 63 26 0
1976 UT 10 110 36 0
1976 VT 15 96 26 0
1976 VA 20 103 26 0
1976 WA 17 102 30 0
1976 WV 14 128 26 0
1976 WI 23 122 34 0
1976 WY 10 95 26 0
1977 AL 15 90 26 0 # weeks column clipped on scan (p1): carried from 1976
1977 AK 18-28 90-120 28 1
1977 AZ 15 85 26 0
1977 AR 15 100 26 0
1977 CA 30 104 26 0
1977 CO 25 121 26 0
1977 CT 15-20 116-174 26 1
1977 DE 20 140 26 0
1977 DC 13-14 148 34 1
1977 FL 10 82 26 0
1977 GA 27 90 26 0
1977 HI 5 120 26 0
1977 ID 17 110 26 0
1977 IL 15 115-138 26 1
1977 IN 35 74-124 26 1
1977 IA 20 124 26 0
1977 KS 27 109 26 0
1977 KY 12 94 26 0
1977 LA 10 120 28 0
1977 ME 12-17 86-129 26 1
1977 MD 10-13 89 26 1
1977 MA 12-18 108-162 30 1
1977 MI 16-18 97-136 26 1
1977 MN 18 122 26 0
1977 MS 10 80 26 0
1977 MO 15 85 26 0
1977 MT 12 104 26 0
1977 NE 12 90 26 0
1977 NV 16 94 26 0
1977 NH 14 95 26 0
1977 NJ 20 104 26 0
1977 NM 17 83 30 0
1977 NY 20 95 26 0
1977 NC 15 105 26 0
1977 ND 15 115 26 0
1977 OH 10-16 102-161 26 1
1977 OK 16 101 26 0
1977 OR 30 112 26 0
1977 PA 13-18 133-141 30 1
1977 RI 26-31 106-126 26 1
1977 SC 10 111 26 0
1977 SD 19 96 26 0
1977 TN 14 95 26 0
1977 TX 15 63 26 0
1977 UT 10 119 36 0
1977 VT 18 102 26 0
1977 VA 28 110 26 0
1977 WA 17 119 30 0
1977 WV 14 139 26 0
1977 WI 25 133 34 0
1977 WY 24 111 26 0
1978 AL 15 90 26 0
1978 AK 18-28 90-120 28 1
1978 AZ 15 85 26 0
1978 AR 15 100 26 0
1978 CA 30 104 26 0
1978 CO 25 130 26 0
1978 CT 15-20 122-183 26 1
1978 DE 20 150 26 0
1978 DC 13-14 160 34 1
1978 FL 10 82 26 0
1978 GA 27 90 26 0
1978 HI 5 126 26 0
1978 ID 17 116 26 0
1978 IL 15 121-145 26 1
1978 IN 35 74-124 26 1
1978 IA 20 133 26 0
1978 KS 29 116 26 0
1978 KY 12 111 26 0
1978 LA 10 130 28 0 # max blurred on scan
1978 ME 12-17 90-135 26 1
1978 MD 10-13 106 26 1
1978 MA 12-18 115-173 30 1
1978 MI 16-18 97-136 26 1
1978 MN 18 133 26 0
1978 MS 10 80 26 0
1978 MO 15 85 26 0
1978 MT 12 113 26 0
1978 NE 12 90 26 0
1978 NV 16 100 26 0
1978 NH 21 102 26 0
1978 NJ 20 110 26 0
1978 NM 18 90 30 0
1978 NY 25 115 26 0
1978 NC 15 112 26 0
1978 ND 15 121 26 0
1978 OH 10-16 111-175 26 1
1978 OK 16 116 26 0
1978 OR 30 119 26 0
1978 PA 13-18 143-151 30 1
1978 RI 26-31 110-130 26 1
1978 SC 10 119 26 0
1978 SD 19 102 26 0
1978 TN 14 95 26 0
1978 TX 15 84 26 0
1978 UT 10 128 36 0
1978 VT 18 109 26 0
1978 VA 38 115 26 0
1978 WA 17 128 30 0
1978 WV 18 149 26 0
1978 WI 26 139 34 0
1978 WY 24 121 26 0
1979 AL 15 90 26 0
1979 AK 18-28 90-120 28 1
1979 AZ 25 90 26 0
1979 AR 15 124 26 0
1979 CA 30 104 26 0
1979 CO 25 137 26 0
1979 CT 15-20 128-192 26 1
1979 DE 20 150 26 0
1979 DC 13-14 172 34 1
1979 FL 10 95 26 0
1979 GA 27 90 26 0
1979 HI 5 134 26 0
1979 ID 17 116 26 0
1979 IL 15 129-154 26 1
1979 IN 35 74-124 26 1
1979 IA 20 131-148 26 1
1979 KS 30 123 26 0
1979 KY 22 120 26 0
1979 LA 10 141 28 0
1979 ME 12-17 96-144 26 1
1979 MD 10-13 106 26 1
1979 MA 12-18 122-183 30 1
1979 MI 16-18 97-136 26 1
1979 MN 30 150 26 0
1979 MS 10 80 26 0
1979 MO 15 85 26 0
1979 MT 30 119 26 0
1979 NE 12 106 26 0
1979 NV 16 115 26 0
1979 NH 21 102 26 0
1979 NJ 20 117 26 0
1979 NM 20 98 26 0
1979 NY 25 125 26 0
1979 NC 15 119 26 0
1979 ND 36 131 26 0
1979 OH 10-16 120-189 26 1
1979 OK 16 132 26 0
1979 OR 33 119 26 0
1979 PA 13-18 152-160 30 1
1979 RI 26-31 120-140 26 1
1979 SC 10 111 26 0
1979 SD 28 109 26 0
1979 TN 14 100 26 0
1979 TX 16 91 26 0
1979 UT 10 137 36 0
1979 VT 18 115 26 0
1979 VA 38 122 26 0
1979 WA 17 128 30 0
1979 WV 18 166 28 0
1979 WI 28 149 34 0
1979 WY 24 131 26 0
1980 AL 15 90 26 0
1980 AK 18-28 90-120 28 1
1980 AZ 29 95 26 0
1980 AR 15 136 26 0
1980 CA 30 120 26 0
1980 CO 25 150 26 0
1980 CT 15-22 134-184 26 1
1980 DE 20 150 26 0
1980 DC 13-14 181 34 1
1980 FL 10 95 26 0
1980 GA 27 90 26 0
1980 HI 5 144 26 0
1980 ID 36 132 26 0
1980 IL 15 135-180 26 1
1980 IN 40 84-141 26 1
1980 IA 17-18 134-162 26 1
1980 KS 34 136 26 0
1980 KY 22 120 26 0
1980 LA 10 149 28 0
1980 ME 12-17 104-156 26 1
1980 MD 25-28 120 26 1
1980 MA 12-18 131-197 30 1
1980 MI 16-18 97-136 26 1
1980 MN 30 162 26 0
1980 MS 10 90 26 0
1980 MO 15 105 26 0
1980 MT 30 131 26 0
1980 NE 12 106 26 0
1980 NV 16 123 26 0
1980 NH 21 114 26 0
1980 NJ 20 123 26 0
1980 NM 22 106 26 0
1980 NY 25 125 26 0
1980 NC 15 130 26 0
1980 ND 39 143 26 0
1980 OH 10 128-202 26 1
1980 OK 16 156 26 0
1980 OR 38 138 26 0
1980 PA 13-18 152-170 30 1
1980 RI 32-37 130-150 26 1
1980 SC 10 114 26 0
1980 SD 28 119 26 0
1980 TN 20 110 26 0
1980 TX 18 105 26 0
1980 UT 10 150 36 0
1980 VT 18 125 26 0
1980 VA 38 122 26 0
1980 WA 41 150 30 0
1980 WV 18 184 28 0
1980 WI 30 160 34 0
1980 WY 24 146 26 0
1981 AL 15 90 26 0
1981 AK 34-58 150-222 26 1
1981 AZ 25 95 26 0
1981 AR 31 136 26 0
1981 CA 30 130 26 0
1981 CO 25 160 26 0
1981 CT 15-22 140-190 26 1
1981 DE 20 150 26 0
1981 DC 13-14 196 34 1
1981 FL 10 105 26 0
1981 GA 27 115 26 0
1981 HI 5 157 26 0
1981 ID 36 145 26 0
1981 IL 45 148-198 26 1
1981 IN 40 84-141 26 1
1981 IA 17-18 146-176 26 1
1981 KS 37 149 26 0
1981 KY 22 140 26 0
1981 LA 10 164 28 0
1981 ME 20-25 115-173 26 1
1981 MD 25-28 140 26 1
1981 MA 12-18 142-213 30 1
1981 MI 16-18 182-221 26 1
1981 MN 30 177 26 0
1981 MS 10 90 26 0
1981 MO 15 105 26 0
1981 MT 36 145 26 0
1981 NE 12 106 26 0
1981 NV 16 136 26 0
1981 NH 21 114 26 0
1981 NJ 20 133 26 0
1981 NM 24 117 26 0
1981 NY 25 125 26 0
1981 NC 15 139 26 0
1981 ND 42 156 26 0
1981 OH 10 136-215 26 1
1981 OK 16 176 26 0
1981 OR 41 160 26 0
1981 PA 35-40 175-183 30 1
1981 RI 35-40 143-163 26 1
1981 SC 10 114 26 0
1981 SD 28 129 26 0
1981 TN 20 110 26 0
1981 TX 21 126 26 0
1981 UT 10 166 36 0
1981 VT 18 135 26 0 # max partly illegible on scan
1981 VA 44 138 26 0
1981 WA 45 163 30 0
1981 WV 18 194 28 0
1981 WI 33 175 34 0
1981 WY 24 165 26 0
1982 AL 15 90 26 0
1982 AK 34-58 150-222 26 1
1982 AZ 40 115 26 0
1982 AR 31 136 26 0
1982 CA 30 136 26 0
1982 CO 25 182 26 0
1982 CT 15-22 156-206 26 1
1982 DE 20 150 26 0
1982 DC 13-14 206 34 1
1982 FL 10 125 26 0
1982 GA 27 115 26 0
1982 HI 5 169 26 0
1982 ID 36 159 26 0
1982 IL 45 154-206 26 1
1982 IN 40 84-141 26 1
1982 IA 17-21 158-191 26 1
1982 KS 40 163 26 0
1982 KY 22 140 26 0
1982 LA 10 183 28 0
1982 ME 20-25 124-186 26 1
1982 MD 25-28 153 26 1
1982 MA 12-18 156-234 30 1
1982 MI 41-44 197 26 1
1982 MN 30 184 26 0
1982 MS 30 105 26 0
1982 MO 15 105 26 0
1982 MT 39 158 26 0
1982 NE 12 106 26 0
1982 NV 16 149 26 0
1982 NH 26 132 26 0
1982 NJ 20 145 26 0
1982 NM 26 130 26 0
1982 NY 25 125 26 0
1982 NC 15 152 26 0
1982 ND 47 175 26 0
1982 OH 10 147-233 26 1
1982 OK 16 197 26 0
1982 OR 44 175 26 0
1982 PA 35-40 190-198 30 1
1982 RI 37-42 154-174 26 1
1982 SC 25 118 26 0
1982 SD 28 129 26 0
1982 TN 20 110 26 0
1982 TX 21 147 26 0
1982 UT 10 166 26 0
1982 VT 18 146 26 0
1982 VA 44 138 26 0
1982 WA 49 178 30 0
1982 WV 18 211 28 0
1982 WI 36 191 34 0
1982 WY 24 180 26 0
1983 AL 22 120 26 0
1983 AK 34-58 156-228 26 1
1983 AZ 40 115 26 0
1983 AR 31 136 26 0
1983 CA 30 166 26 0
1983 CO 25 192 26 0
1983 CT 15-22 156-206 26 1
1983 DE 20 150 26 0
1983 DC 13-14 206 26 1
1983 FL 10 125 26 0
1983 GA 27 125 26 0
1983 HI 5 178 26 0
1983 ID 36 159 26 0
1983 IL 51 154-200 26 1
1983 IN 40 84-141 26 1
1983 IA 22-27 143-176 26 1
1983 KS 40 163 26 0
1983 KY 22 140 26 0
1983 LA 10 205 26 0
1983 ME 22-27 133-199 26 1
1983 MD 25-28 160 26 1
1983 MA 14-21 172-258 30 1
1983 MI 55 197 26 1
1983 MN 50 191 26 0
1983 MS 30 105 26 0
1983 MO 14 105 26 0
1983 MT 41 166 26 0
1983 NE 12 120 26 0
1983 NV 16 158 26 0
1983 NH 26 132 26 0
1983 NJ 20 158 26 0
1983 NM 29 142 26 0
1983 NY 25 125 26 0
1983 NC 15 166 26 0
1983 ND 60 172 26 0
1983 OH 10 147-233 26 1
1983 OK 16 197 26 0
1983 OR 46 197 26 0
1983 PA 35-40 205-213 30 1
1983 RI 37-42 164-184 26 1
1983 SC 20 118 26 0
1983 SD 28 129 26 0
1983 TN 30 110 26 0
1983 TX 27 168 26 0
1983 UT 46 166 26 0
1983 VT 18 146 26 0
1983 VA 44 138 26 0
1983 WA 51 185 30 0
1983 WV 18 223 28 0
1983 WI 37 196 34 0
1983 WY 24 180 26 0
1984 AL 22 120 26 0
1984 AK 34-58 156-228 26 1
1984 AZ 40 115 26 0
1984 AR 40 154 26 0
1984 CA 30 166 26 0
1984 CO 25 206 26 0
1984 CT 15-22 168-252 26 1
1984 DE 20 165 26 0
1984 DC 13-14 206 26 1
1984 FL 10 150 26 0
1984 GA 27 125 26 0
1984 HI 5 188 26 0
1984 ID 45 173 26 0
1984 IL 50 161-209 26 1
1984 IN 40 84-141 26 1
1984 IA 22-27 143-176 26 1
1984 KS 43 175 26 0
1984 KY 22 140 26 0
1984 LA 10 205 26 0
1984 ME 22-27 139-208 26 1
1984 MD 25-28 175 26 1
1984 MA 14-21 185-278 30 1
1984 MI 55 197 26 1
1984 MN 52 198 26 0
1984 MS 30 115 26 0
1984 MO 14 105 26 0
1984 MT 42 171 26 0
1984 NE 12 120 26 0
1984 NV 16 162 26 0
1984 NH 26 141 26 0
1984 NJ 20 170 26 0
1984 NM 29 145 26 0
1984 NY 40 180 26 0
1984 NC 15 166 26 0
1984 ND 60 185 26 0
1984 OH 10 147-233 26 1
1984 OK 16 197 26 0
1984 OR 47 204 26 0
1984 PA 35-40 214-222 26 1
1984 RI 37-42 174-194 26 1
1984 SC 21 125 26 0
1984 SD 28 129 26 0
1984 TN 30 115 26 0
1984 TX 27 182 26 0
1984 UT 46 186 26 0
1984 VT 18 146 26 0
1984 VA 54 150 26 0
1984 WA 51 185 30 0
1984 WV 18 225 28 0
1984 WI 37 196 26 0
1984 WY 20 183 26 0
1985 AL 22 120 26 0
1985 AK 38-62 188-260 26 1
1985 AZ 40 125 26 0
1985 AR 42 189 26 0
1985 CA 30 166 26 0
1985 CO 25 213 26 0
1985 CT 15-22 180-230 26 1
1985 DE 20 165 26 0
1985 DC 26 206 26 1
1985 FL 10 150 26 0
1985 GA 27 135 26 0
1985 HI 5 194 26 0
1985 ID 44 179 26 0
1985 IL 51 161-209 26 1
1985 IN 40 90-151 26 1
1985 IA 23-28 158-194 26 1
1985 KS 47 190 26 0
1985 KY 22 140 26 0
1985 LA 10 205 26 0
1985 ME 22-27 146-219 26 1
1985 MD 25-28 175 26 1
1985 MA 14-21 196-294 30 1
1985 MI 54 197 26 1
1985 MN 56 228 26 0
1985 MS 30 115 26 0
1985 MO 14 120 26 0
1985 MT 43 171 26 0
1985 NE 12 120 26 0
1985 NV 16 166 26 0
1985 NH 26 141 26 0
1985 NJ 20 203 26 1
1985 NM 30 150 26 0
1985 NY 40 180 26 0
1985 NC 15 167 26 0
1985 ND 60 194 26 0
1985 OH 10 147-233 26 1
1985 OK 16 197 26 0
1985 OR 49 211 26 0
1985 PA 35-40 224-232 26 1
1985 RI 37-42 183-203 26 1
1985 SC 21 125 26 0
1985 SD 28 129 26 0
1985 TN 30 120 26 0
1985 TX 29 189 26 0
1985 UT 53 193 26 0
1985 VT 18 146 26 0
1985 VA 58 159 26 0
1985 WA 52 190 30 0
1985 WV 24 225 26 0
1985 WI 37 196 26 0
1985 WY 36 192 26 0
1986 AL 22 120 26 0
1986 AK 38-62 188-260 26 1
1986 AZ 40 135 26 0
1986 AR 44 196 26 0
1986 CA 30 166 26 0
1986 CO 25 213 26 0
1986 CT 15-22 192-242 26 1
1986 DE 20 205 26 0
1986 DC 26 250 26 1
1986 FL 10 175 26 0
1986 GA 27 145 26 0
1986 HI 5 200 26 0
1986 ID 44 185 26 0
1986 IL 51 161-209 26 1
1986 IN 40 96-161 26 1
1986 IA 23-28 162-199 26 1
1986 KS 49 197 26 0
1986 KY 22 140 26 0
1986 LA 10 205 26 0
1986 ME 25-37 152-228 26 1
1986 MD 25-29 195 26 1
1986 MA 14-21 207-310 30 1
1986 MI 54 197 26 1
1986 MN 58 239 26 0
1986 MS 30 130 26 0
1986 MO 14 125 26 0
1986 MT 43 171 26 0
1986 NE 12 126 26 0
1986 NV 16 171 26 0
1986 NH 36 150 26 0
1986 NJ 20 214 26 1
1986 NM 30 154 26 0
1986 NY 40 180 26 0
1986 NC 15 175 26 0
1986 ND 60 197 26 0
1986 OH 10 147-233 26 1
1986 OK 16 197 26 0 # weeks cell reads 25 or 26 (footnote 14); 26 used
1986 OR 50 216 26 0 # weeks cell partly illegible (footnote 7); 26 used
1986 PA 35-40 232-240 26 1
1986 RI 36-41 191-236 26 1
1986 SC 21 125 26 0
1986 SD 28 129 26 0
1986 TN 30 125 26 0
1986 TX 32 203 26 0
1986 UT 13 197 26 0
1986 VT 18 154 26 0
1986 VA 58 167 26 0
1986 WA 53 197 30 0
1986 WV 24 225 26 0
1986 WI 37 196 26 0
1986 WY 36 198 26 0
1987 AL 22 120 26 0
1987 AK 38-62 188-260 26 1
1987 AZ 40 135 26 0
1987 AR 36 205 26 0
1987 CA 30 166 26 0
1987 CO 25 213 26 0
1987 CT 15-22 204-254 26 1
1987 DE 20 205 26 0
1987 DC 26 250 26 1
1987 FL 10 175 26 0
1987 GA 37 155 26 0
1987 HI 5 212 26 0
1987 ID 44 188 26 0
1987 IL 51 168-219 26 1
1987 IN 40 96-161 26 1
1987 IA 25-30 167-205 26 1
1987 KS 51 204 26 0
1987 KY 22 151 26 0
1987 LA 10 205 26 0
1987 ME 26-39 161-241 26 1
1987 MD 25-31 195 26 1
1987 MA 14-21 220-330 30 1
1987 MI 54 229 26 1
1987 MN 60 250 26 0
1987 MS 30 130 26 0
1987 MO 22 130 26 0
1987 MT 45 181 26 0
1987 NE 20 134 26 0
1987 NV 16 175 26 0
1987 NH 39 156 26 0
1987 NJ 48 228 26 1
1987 NM 31 158 26 0
1987 NY 40 180 26 0
1987 NC 16 184 26 0
1987 ND 43 179 26 0
1987 OH 42 147-233 26 1
1987 OK 16 197 26 0
1987 OR 52 222 26 0
1987 PA 35-40 241-249 26 1
1987 RI 39-44 202-252 26 1
1987 SC 20 125 26 0
1987 SD 28 140 26 0
1987 TN 30 145 26 0
1987 TX 33 210 26 0
1987 UT 13 201 26 0
1987 VT 18 160 26 0
1987 VA 58 167 26 0
1987 WA 55 205 30 0
1987 WV 24 225 26 0
1987 WI 37 196 26 0
1987 WY 36 198 26 0
1988 AL 22 120 26 0
1988 AK 38-62 188-260 26 1
1988 AZ 40 145 26 0
1988 AR 37 207 26 0
1988 CA 30 166 26 0
1988 CO 25 214 26 0
1988 CT 15-22 216-266 26 1
1988 DE 20 205 26 0
1988 DC 13 268 26 1
1988 FL 10 200 26 0
1988 GA 37 165 26 0
1988 HI 5 223 26 0
1988 ID 44 193 26 0
1988 IL 51 176-230 26 1
1988 IN 40 96-161 26 1
1988 IA 25-30 174-214 26 1
1988 KS 52 210 26 0
1988 KY 22 166 26 0
1988 LA 10 191 26 0
1988 ME 26-39 171-256 26 1
1988 MD 25-33 205 26 1
1988 MA 14-21 236-354 30 1
1988 MI 58 242 26 1
1988 MN 38 254 26 0
1988 MS 30 145 26 0
1988 MO 22 140 26 0
1988 MT 46 185 26 0
1988 NE 20 134 26 0
1988 NV 16 184 26 0
1988 NH 39 156 26 0
1988 NJ 51 241 26 1
1988 NM 31 159 26 0
1988 NY 40 180 26 0
1988 NC 16 204 26 0
1988 ND 43 183 26 0
1988 OH 42 157-248 26 1
1988 OK 16 197 26 0
1988 OR 53 229 26 0
1988 PA 35-40 252-260 26 1
1988 RI 43-53 240-300 26 1
1988 SC 20 147 26 0
1988 SD 28 140 26 0
1988 TN 30 155 26 0
1988 TX 34 210 26 0
1988 UT 14 202 26 0
1988 VT 25 169 26 0
1988 VA 56 176 26 0
1988 WA 57 209 30 0
1988 WV 24 225 26 0
1988 WI 38 200 26 0
1988 WY 36 200 26 0
1989 AL 22 145 26 0
1989 AK 38-62 188-260 26 1
1989 AZ 40 155 26 0
1989 AR 38 215 26 0
1989 CA 30 166 26 0
1989 CO 25 224 26 0
1989 CT 15-22 234-284 26 1
1989 DE 20 205 26 0
1989 DC 13 283 26 1
1989 FL 10 200 26 0
1989 GA 37 175 26 0
1989 HI 5 239 26 0
1989 ID 44 200 26 0
1989 IL 51 187-244 26 1
1989 IN 40 96-161 26 1
1989 IA 26-32 181-222 26 1
1989 KS 52 210 26 0
1989 KY 22 186 26 0
1989 LA 10 181 26 0
1989 ME 31-46 180-270 26 1
1989 MD 25-33 205 26 1
1989 MA 14-21 255-382 30 1
1989 MI 59 263 26 1
1989 MN 38 255 26 0
1989 MS 30 145 26 0
1989 MO 33 150 26 0
1989 MT 47 190 26 0
1989 NE 20 134 26 0
1989 NV 16 194 26 0
1989 NH 35 162 26 0
1989 NJ 51 258 26 1
1989 NM 33 166 26 0
1989 NY 40 245 26 0
1989 NC 19 228 26 0
1989 ND 43 187 26 0
1989 OH 42 169-268 26 1
1989 OK 16 197 26 0
1989 OR 55 238 26 0
1989 PA 35-40 266-274 26 1
1989 RI 48-58 240-300 26 1
1989 SC 20 165 26 0
1989 SD 28 140 26 0
1989 TN 30 155 26 0
1989 TX 34 210 26 0
1989 UT 14 208 26 0
1989 VT 25 178 26 0
1989 VA 56 176 26 0
1989 WA 59 237 30 0
1989 WV 24 245 26 0
1989 WI 38 200 26 0
1989 WY 36 200 26 0
1990 AL 22 150 26 0
1990 AK 38-62 188-260 26 1
1990 AZ 40 155 26 0
1990 AR 39 220 26 0
1990 CA 40 190 26 0
1990 CO 25 229 26 0
1990 CT 15-22 252-302 26 1
1990 DE 20 225 26 0
1990 DC 13 293 26 1
1990 FL 10 200 26 0
1990 GA 37 185 26 0
1990 HI 5 256 26 0
1990 ID 44 206 26 0
1990 IL 51 199-260 26 1
1990 IN 40 96-161 26 1
1990 IA 27-33 186-228 26 1
1990 KS 55 222 26 0
1990 KY 22 199 26 0
1990 LA 10 181 26 0
1990 ME 33-49 188-282 26 1
1990 MD 25-33 215 26 1
1990 MA 14-21 272-408 30 1
1990 MI 59 275 26 1
1990 MN 38 260 26 0
1990 MS 30 145 26 0
1990 MO 33 160 26 0
1990 MT 48 193 26 0
1990 NE 20 134 26 0
1990 NV 16 202 26 0
1990 NH 35 168 26 0
1990 NJ 59 279 26 1
1990 NM 34 170 26 0
1990 NY 40 260 26 0
1990 NC 20 236 26 0
1990 ND 43 198 26 0
1990 OH 42 184-291 26 1
1990 OK 16 197 26 0
1990 OR 57 247 26 0
1990 PA 35-40 280-288 26 1
1990 RI 39-49 269-334 26 1
1990 SC 20 175 26 0
1990 SD 28 140 26 0
1990 TN 30 160 26 0
1990 TX 36 217 26 0
1990 UT 14 214 26 0
1990 VT 26 182 26 0
1990 VA 56 176 26 0
1990 WA 61 246 30 0
1990 WV 24 251 26 0
1990 WI 42 225 26 0
1990 WY 38 200 26 0
1991 AL 22 150 26 0
1991 AK 44-68 212-284 26 1
1991 AZ 40 175 26 0
1991 AR 41 230 26 0
1991 CA 40 210 26 0
1991 CO 25 239 26 0
1991 CT 15-22 270-320 26 1
1991 DE 20 225 26 0
1991 DC 13 293 26 1
1991 FL 10 225 26 0
1991 GA 37 185 26 0
1991 HI 5 275 26 0
1991 ID 44 215 26 0
1991 IL 51 206-270 26 1
1991 IN 50 116-171 26 1
1991 IA 29-35 194-238 26 1
1991 KS 57 231 26 0
1991 KY 22 209 26 0
1991 LA 10 181 26 0
1991 ME 35-52 198-297 26 1
1991 MD 25-33 223 26 1
1991 MA 14-21 282-423 30 1
1991 MI 59 276 26 1
1991 MN 38 265 26 0
1991 MS 30 165 26 0
1991 MO 45 170 26 0
1991 MT 50 201 26 0
1991 NE 20 144 26 0
1991 NV 16 211 26 0
1991 NH 34 179 26 0
1991 NJ 61 291 26 1
1991 NM 35 177 26 0
1991 NY 40 280 26 0
1991 NC 21 245 26 0
1991 ND 43 206 26 0
1991 OH 42 196-291 26 1
1991 OK 16 212 26 0
1991 OR 60 259 26 0
1991 PA 35-40 291-299 26 1
1991 RI 41-51 285-356 26 1
1991 SC 20 186 26 0
1991 SD 28 154 26 0
1991 TN 30 165 26 0
1991 TX 37 224 26 0
1991 UT 14 221 26 0
1991 VT 26 192 26 0
1991 VA 60 188 26 0
1991 WA 64 258 30 0
1991 WV 24 263 26 0
1991 WI 42 225 26 0
1991 WY 38 200 26 0
1992 AL 22 160 26 0
1992 AK 44-68 212-284 26 1
1992 AZ 40 185 26 0
1992 AR 43 240 26 0
1992 CA 40 230 26 0
1992 CO 25 250 26 0
1992 CT 15-22 288-338 26 1
1992 DE 20 245 26 0
1992 DC 13 335 26 1
1992 FL 10 225 26 0
1992 GA 37 185 26 0
1992 HI 5 306 26 0
1992 ID 44 223 26 0
1992 IL 51 214-279 26 1
1992 IN 50 140-181 26 1
1992 IA 30-36 200-245 26 1
1992 KS 59 239 26 0
1992 KY 22 217 26 0
1992 LA 10 181 26 0
1992 ME 35-52 198-297 26 1
1992 MD 25-33 223 26 1
1992 MA 14-21 296-444 30 1
1992 MI 42 283 26 1
1992 MN 38 279 26 0
1992 MS 30 165 26 0
1992 MO 45 175 26 0
1992 MT 52 209 26 0
1992 NE 20 154 26 0
1992 NV 16 217 26 0
1992 NH 32 188 26 0
1992 NJ 66 308 26 1
1992 NM 37 185 26 0
1992 NY 40 300 26 0
1992 NC 22 258 26 0
1992 ND 43 212 26 0
1992 OH 42 211-294 26 1
1992 OK 16 229 26 0
1992 OR 63 271 26 0
1992 PA 35-40 304-312 26 1
1992 RI 41-51 294-367 26 1
1992 SC 20 191 26 0
1992 SD 28 154 26 0
1992 TN 30 170 26 0
1992 TX 38 231 26 0
1992 UT 14 230 26 0
1992 VT 25 199 26 0
1992 VA 65 208 26 0
1992 WA 68 273 30 0
1992 WV 24 270 26 0
1992 WI 45 240 26 0
1992 WY 40 200 26 0
1993 AL 22 165 26 0
1993 AK 44-68 212-284 26 1
1993 AZ 40 185 26 0
1993 AR 45 254 26 0
1993 CA 40 230 26 0
1993 CO 25 261 26 0
1993 CT 15-22 306-356 26 1
1993 DE 20 245 26 0
1993 DC 50 335 26 1
1993 FL 10 250 26 0
1993 GA 37 185 26 0
1993 HI 5 322 26 0
1993 ID 44 234 26 0
1993 IL 51 227-300 26 1
1993 IN 50 170-192 26 1
1993 IA 31-38 211-259 26 1 # printed 30-36 / 245 hand-corrected on the scan to 31-38 / 211-259
1993 KS 62 250 26 0
1993 KY 22 229 26 0
1993 LA 10 181 26 0
1993 ME 35-52 192-288 26 1
1993 MD 25-33 223 26 1
1993 MA 14-21 312-468 30 1
1993 MI 42 293 26 1
1993 MN 38 305 26 0
1993 MS 30 165 26 0
1993 MO 45 175 26 0
1993 MT 54 217 26 0
1993 NE 20 154 26 0
1993 NV 16 230 26 0
1993 NH 32 196 26 0
1993 NJ 69 325 26 1
1993 NM 38 191 26 0
1993 NY 40 300 26 0
1993 NC 22 267 26 0
1993 ND 43 232 26 0
1993 OH 42 228-306 26 1
1993 OK 16 237 26 0
1993 OR 66 285 26 0
1993 PA 35-40 317-325 26 1
1993 RI 41-51 310-387 26 1
1993 SC 20 203 26 0
1993 SD 28 168 26 0
1993 TN 30 185 26 0
1993 TX 40 245 26 0
1993 UT 14 240 26 0
1993 VT 25 209 26 0
1993 VA 65 208 26 0
1993 WA 73 340 30 0
1993 WV 24 280 26 0
1993 WI 46 243 26 0
1993 WY 40 220 26 0
1994 AL 22 180 26 0
1994 AK 44-68 212-284 26 1
1994 AZ 40 185 26 0
1994 AR 46 256 26 0
1994 CA 40 230 26 0
1994 CO 25 267 26 0
1994 CT 15-25 317-367 26 1
1994 DE 20 265 26 0
1994 DC 50 335 26 1
1994 FL 10 250 26 0
1994 GA 37 195 26 0
1994 HI 5 337 26 0
1994 ID 44 240 26 0
1994 IL 51 235-311 26 1
1994 IN 50 202 26 0
1994 IA 32-38 216-265 26 1
1994 KS 63 255 26 0
1994 KY 22 232 26 0
1994 LA 10 181 26 0
1994 ME 35-52 192-288 26 1
1994 MD 25-33 223 26 1
1994 MA 14-21 325-487 30 1
1994 MI 42 293 26 1
1994 MN 38 304 26 0
1994 MS 30 165 26 0
1994 MO 45 175 26 0
1994 MT 55 223 26 0
1994 NE 20 170 26 0
1994 NV 16 235 26 0
1994 NH 32 204 26 0
1994 NJ 73 347 26 1
1994 NM 39 197 26 0
1994 NY 40 300 26 0
1994 NC 24 282 26 0
1994 ND 43 237 26 0
1994 OH 60 238-319 26 1
1994 OK 16 245 26 0
1994 OR 68 292 26 0
1994 PA 35-40 329-337 26 1
1994 RI 41-51 317-396 26 1
1994 SC 20 207 26 0 # faint scan
1994 SD 28 174 26 0
1994 TN 30 200 26 0
1994 TX 41 245 26 0
1994 UT 17 248 26 0
1994 VT 25 210 26 0
1994 VA 65 208 26 0
1994 WA 73 343 30 0
1994 WV 24 282 26 0
1994 WI 48 256 26 0
1994 WY 40 229 26 0
1995 AL 22 180 26 0
1995 AK 44-68 212-284 26 1
1995 AZ 40 185 26 0
1995 AR 47 264 26 0
1995 CA 40 230 26 0
1995 CO 25 272 26 0
1995 CT 15-25 335-385 26 1
1995 DE 20 300 26 0
1995 DC 50 347 26 1
1995 FL 10 250 26 0
1995 GA 37 205 26 0
1995 HI 5 344 26 0
1995 ID 44 248 26 0
1995 IL 51 242-321 26 1
1995 IN 50 217 26 0
1995 IA 33-40 224-274 26 1
1995 KS 65 260 26 0
1995 KY 22 238 26 0
1995 LA 10 181 26 0
1995 ME 35-52 192-288 26 1
1995 MD 25-33 250 26 1
1995 MA 14-21 336-504 30 1
1995 MI 42 293 26 1
1995 MN 38 304 26 0
1995 MS 30 180 26 0
1995 MO 45 175 26 0
1995 MT 57 228 26 0
1995 NE 20 184 26 0
1995 NV 16 237 26 0
1995 NH 32 204 26 0
1995 NJ 75 354 26 1
1995 NM 41 205 26 0
1995 NY 40 300 26 0
1995 NC 25 289 26 0
1995 ND 43 243 26 0
1995 OH 66 245-328 26 1
1995 OK 16 247 26 0
1995 OR 70 301 26 0
1995 PA 35-40 340-348 26 1
1995 RI 41-51 324-404 26 1
1995 SC 20 213 26 0
1995 SD 28 180 26 0
1995 TN 30 200 26 0
1995 TX 42 252 26 0
1995 UT 17 253 26 0
1995 VT 25 212 26 0
1995 VA 65 208 26 0
1995 WA 75 350 30 0
1995 WV 24 290 26 0
1995 WI 50 266 26 0
1995 WY 16 233 26 0
1996 AL 22 180 26 0
1996 AK 44-68 212-284 26 1
1996 AZ 40 185 26 0
1996 AR 49 273 26 0
1996 CA 40 230 26 0
1996 CO 25 283 26 0
1996 CT 15-25 350-400 26 1
1996 DE 20 300 26 0
1996 DC 50 359 26 1
1996 FL 32 250 26 0
1996 GA 37 215 26 0
1996 HI 5 347 26 0
1996 ID 44 259 26 0
1996 IL 51 251-332 26 1
1996 IN 87 217 26 0
1996 IA 34-41 231-283 26 1
1996 KS 67 270 26 0
1996 KY 22 246 26 0
1996 LA 10 193 26 0
1996 ME 36-54 210-315 26 1
1996 MD 25-33 250 26 1
1996 MA 14-21 347-521 30 1
1996 MI 60 300 26 1
1996 MN 38 314 26 0
1996 MS 30 180 26 0
1996 MO 45 175 26 0
1996 MT 57 230 26 0
1996 NE 20 184 26 0
1996 NV 16 247 26 0
1996 NH 32 228 26 0
1996 NJ 60 362 26 1
1996 NM 42 212 26 0
1996 NY 40 300 26 0
1996 NC 25 297 26 0
1996 ND 43 251 26 0
1996 OH 66 253-339 26 1
1996 OK 16 251 26 0
1996 OR 73 314 26 0
1996 PA 35-40 352-360 26 1
1996 RI 41-51 336-420 26 1
1996 SC 20 221 26 0
1996 SD 28 187 26 0
1996 TN 30 220 26 0
1996 TX 43 259 26 0
1996 UT 17 263 26 0
1996 VT 31 217 26 0
1996 VA 65 208 26 0
1996 WA 78 365 30 0
1996 WV 24 296 26 0
1996 WI 52 274 26 0
1996 WY 17 236 26 0
1997 AL 45 190 26 0
1997 AK 44-68 248-320 26 1
1997 AZ 40 185 26 0
1997 AR 50 281 26 0
1997 CA 40 230 26 0
1997 CO 25 297 26 0
1997 CT 15-25 353-403 26 1
1997 DE 20 300 26 0
1997 DC 50 309 26 1
1997 FL 32 250 26 0
1997 GA 39 224 26 0
1997 HI 5 351 26 0
1997 ID 44 265 26 0
1997 IL 51 257-341 26 1
1997 IN 87 217 26 0
1997 IA 35-43 239-293 26 1
1997 KS 70 281 26 0
1997 KY 22 256 26 0
1997 LA 10 193 26 0
1997 ME 36-54 231-325 26 1
1997 MD 25-33 250 26 1
1997 MA 14-21 362-543 30 1
1997 MI 40 300 26 1
1997 MN 39 324 26 0
1997 MS 30 180 26 0
1997 MO 45 175 26 0
1997 MT 59 237 26 0
1997 NE 20 184 26 0
1997 NV 16 258 26 0
1997 NH 32 246 26 0
1997 NJ 60 374 26 1
1997 NM 43 218 26 0
1997 NY 40 300 26 0
1997 NC 25 310 26 0
1997 ND 43 260 26 0
1997 OH 66 257-345 26 1
1997 OK 16 255 26 0
1997 OR 77 329 26 0
1997 PA 35-40 362-370 26 1
1997 RI 47-57 347-434 26 1
1997 SC 20 229 26 0
1997 SD 28 194 26 0
1997 TN 30 220 26 0
1997 TX 44 266 26 0
1997 UT 17 272 26 0
1997 VT 31 225 26 0
1997 VA 65 224 26 0
1997 WA 82 384 30 0
1997 WV 24 303 26 0
1997 WI 53 282 26 0
1997 WY 17 241 26 0
1998 AL 45 190 26 0
1998 AK 44-68 248-320 26 1
1998 AZ 40 195 26 0
1998 AR 53 294 26 0
1998 CA 40 230 26 0
1998 CO 25 314 26 0
1998 CT 15-25 362-412 26 1
1998 DE 20 300 26 0
1998 DC 50 309 26 0 # dependents allowance no longer in the formula from 1998
1998 FL 32 275 26 0
1998 GA 39 244 26 0
1998 HI 5 356 26 0
1998 ID 51 273 26 0
1998 IL 51 269-355 26 1
1998 IN 87 244 26 0
1998 IA 37-45 251-307 26 1
1998 KS 73 292 26 0
1998 KY 22 268 26 0
1998 LA 10 215 26 0
1998 ME 37-55 227-340 26 1
1998 MD 25-33 250 26 1
1998 MA 14-21 382-573 30 1
1998 MI 87 300 26 1
1998 MN 39 331 26 0
1998 MS 30 190 26 0
1998 MO 45 205 26 0
1998 MT 61 246 26 0
1998 NE 20 184 26 0
1998 NV 16 267 26 0
1998 NH 32 275 26 0
1998 NJ 60 390 26 1
1998 NM 44 224 26 0
1998 NY 40 300 26 0
1998 NC 25 322 26 0
1998 ND 43 271 26 0
1998 OH 66 267-358 26 1
1998 OK 16 262 26 0
1998 OR 81 346 26 0
1998 PA 35-40 375-383 26 1
1998 RI 47-97 364-455 26 1
1998 SC 20 238 26 0
1998 SD 28 203 26 0
1998 TN 30 255 26 0
1998 TX 46 280 26 0
1998 UT 17 284 26 0
1998 VT 40 275 26 0
1998 VA 55 228 26 0
1998 WA 87 410 30 0
1998 WV 24 311 26 0
1998 WI 43 290 26 0
1998 WY 18 250 26 0
1999 AL 45 190 26 0
1999 AK 44-68 248-320 26 1
1999 AZ 40 205 26 0
1999 AR 55 309 26 0
1999 CA 40 230 26 0
1999 CO 25 337 26 0
1999 CT 15-25 362-412 26 1
1999 DE 20 300 26 0
1999 DC 50 309 26 0
1999 FL 32 275 26 0
1999 GA 39 264 26 0
1999 HI 5 364 26 0
1999 ID 51 273 26 0
1999 IL 51 284-376 26 1
1999 IN 87 244 26 0
1999 IA 37-45 251-307 26 1
1999 KS 73 292 26 0
1999 KY 39 268 26 0
1999 LA 10 215 26 0
1999 ME 37-55 227-340 26 1
1999 MD 25-33 250 26 1
1999 MA 14-21 NA 30 1 # printed max "$250" (footnote 4) is evidently a misprint (Maryland's value); left missing
1999 MI 87 300 26 1
1999 MN 39 331-405 26 0
1999 MS 30 190 26 0
1999 MO 45 220 26 0
1999 MT 63 254 26 0
1999 NE 36 206 26 0
1999 NV 16 267 26 0
1999 NH 32 301 26 0
1999 NJ 61 407 26 1
1999 NM 46 246 26 0
1999 NY 40 365 26 0
1999 NC 25 322 26 0
1999 ND 43 283 26 0
1999 OH 77 279-375 26 1
1999 OK 16 276 26 0
1999 OR 81 346 26 0
1999 PA 35-40 375-383 26 1
1999 RI 52-97 383-478 26 1
1999 SC 20 238 26 0
1999 SD 28 214 26 0
1999 TN 30 255 26 0
1999 TX 47 287 26 0
1999 UT 20 298 26 0
1999 VT 40 287 26 0
1999 VA 50 230 26 0
1999 WA 87 410 30 0
1999 WV 24 311 26 0
1999 WI 44 297 26 0
1999 WY 19 261 26 0
2000 TN 30 255 26 0
2000 TX 48 294 26 0
2000 UT 20 309 26 0
2000 VT NA 298 26 0
2000 VA 50 230 26 0
2000 WA 94 441 30 0
2000 WV 24 318 26 0
2000 WI 44 297 26 0
2000 WY 19 261 26 0
"""

# (1b) cells of the text-layer issues (2000-2024) the positional parser cannot read; checked against the PDFs
#      keys: column names of the law panel (+ "note")
OVERRIDES = {
    (2000, "MA"): dict(max_wba=431, max_wba_dep=646, dep_allowance=1),
    (2000, "ME"): dict(max_wba=265, max_wba_dep=397, dep_allowance=1),
    (2000, "PA"): dict(max_wba=408, max_wba_dep=416, dep_allowance=1),
    (2000, "MD"): dict(dep_allowance=1, note="same maximum with or without dependents (table fn 4)"),
    (2000, "MI"): dict(dep_allowance=1),
    (2000, "NJ"): dict(dep_allowance=1, note="same maximum with or without dependents (table fn 4)"),
    (2000, "DE"): dict(dep_allowance=0),          # parser picked up Connecticut's overflowing "deps" text
    (2001, "DE"): dict(dep_allowance=0),
    (2001, "OK"): dict(dep_allowance=0),
    (2001, "SC"): dict(dep_allowance=0),
    (2001, "MN"): dict(note="only maximum printed is $452 'effective 8/1/01'"),
    (2003, "MN"): dict(max_wba=467, note="$478 effective 8/3/03 not used"),
    (2004, "NC"): dict(max_wba=416, note="$426 effective 8/1/04 not used"),
    (2012, "HI"): dict(max_wba=560, note="table: $523 before 4/1/12, $560 from 4/1/12"),
    (2001, "KY"): dict(max_wba=329, note="July 2001 table prints $341; January 2001, January 2002 and July 2002 all "
                       "$329 (no cut in between): treated as a misprint"),
    (2003, "WA"): dict(max_wba=496, note="July 2003 table prints $510; January 2003, January 2004 and July 2004 all "
                       "$496 (2003 freeze of the maximum): $496 used"),
    (2002, "VA"): dict(min_wba=59, max_wba=318, note="July 2002 table prints $69 / $368, out of line with January "
                       "2002 ($268) and January / July 2003 ($318 / $316): misprint; January 2003 values used"),
    (2020, "AK"): dict(max_wba_dep=442, min_wba_dep=128, note="table: '$370 + DA' (DA $24 per dependent up to $72)"),
    (2021, "AK"): dict(max_wba_dep=442, min_wba_dep=128, note="table: '$370 + DA' (DA $24 per dependent up to $72)"),
    (2022, "AK"): dict(max_wba_dep=442, min_wba_dep=128, note="table: '$370 + DA' (DA $24 per dependent up to $72)"),
    (2024, "MA"): dict(note="dependents' allowance no longer capped (table: 'no cap on DA')"),
}
INDEXED_WEEKS = {"FL": 2012, "GA": 2012, "NC": 2013, "KS": 2014, "MO": 2011, "SC": 2011, "MI": 2012, "AR": 2011, "IL": 2012,
                 "AL": 2020, "IA": 2022, "KY": 2023, "TN": 2024, "OK": 2023, "AZ": 2022, "MT": 2023}


def fetch(url, path):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(url, headers=UA)
        path.write_bytes(urllib.request.urlopen(req, timeout=120).read())
    return path


def download():
    for f in ("ar5159", "ar218"):
        fetch(f"https://oui.doleta.gov/unemploy/csv/{f}.csv", EXT / f"{f}.csv")
    for y in YEARS:
        d = f"{y // 10 * 10}-{y // 10 * 10 + 9}"
        fetch(f"https://oui.doleta.gov/unemploy/content/sigpros/{d}/July{y}.pdf", SIGPROS / f"July{y}.pdf")
    for y in range(2000, max(YEARS) + 2):            # January issues: cross-check of the July values
        d = f"{y // 10 * 10}-{y // 10 * 10 + 9}"
        fetch(f"https://oui.doleta.gov/unemploy/content/sigpros/{d}/January{y}.pdf", SIGPROS / f"January{y}.pdf")
    fetch("https://apps.bea.gov/regional/zip/SAINC.zip", EXT / "bea" / "SAINC.zip")


# ---------------------------------------------------------------------------------------------------------------------
# (1) statutory parameters
def split_range(tok):
    """'15-22' -> (15, 22); '120' -> (120, nan); 'NA' -> (nan, nan)."""
    if tok in ("NA", ""):
        return np.nan, np.nan
    a, _, b = tok.partition("-")
    return float(a), (float(b) if b else np.nan)


def scan_rows():
    rows = []
    for ln in SCAN.strip().splitlines():
        body, _, note = ln.partition("#")
        y, st, mn, mx, wk, dep = body.split()
        a, a2 = split_range(mn)
        b, b2 = split_range(mx)
        rows.append(dict(year=int(y), state=st, min_wba=a, min_wba_dep=a2, max_wba=b, max_wba_dep=b2,
                         max_duration_weeks=float(wk), dep_allowance=int(dep),
                         law_src=f"SigPros July {y} (scan, transcribed)", law_note=note.strip()))
    return pd.DataFrame(rows)


def pdftotext_bbox():
    """poppler pdftotext with -bbox (MiKTeX ships one; the Git-for-Windows xpdf build has no -bbox)."""
    cands = [shutil.which("pdftotext"),
             str(Path.home() / "AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdftotext.exe")]
    for c in cands:
        if c and Path(c).exists():
            h = subprocess.run([c, "-h"], capture_output=True, text=True)
            if "-bbox" in (h.stdout + h.stderr):
                return c
    raise RuntimeError("need poppler pdftotext with -bbox")


WRE = re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>')


def pages(year, month="July"):
    """words per page: [y (= -yMax, up is larger), xMin, height, text, xMax]."""
    html = BBOX / f"{month}{year}.html"
    if not html.exists():
        BBOX.mkdir(parents=True, exist_ok=True)
        subprocess.run([pdftotext_bbox(), "-bbox", str(SIGPROS / f"{month}{year}.pdf"), str(html)], check=True)
    out = []
    for pg in html.read_text(encoding="utf-8").split("<page ")[1:]:
        out.append([[-float(m[3]), float(m[0]), float(m[3]) - float(m[1]), unescape(m[4]), float(m[2])]
                    for m in WRE.findall(pg)])
    return out


def join(ws, body):
    """words of one cell -> 'line / line', superscripts (small glyphs) dropped."""
    ws = sorted((w for w in ws if w[2] >= 0.8 * body), key=lambda w: (-round(w[0]), w[1]))
    lines, cur, cy = [], [], None
    for w in ws:
        if cy is not None and abs(w[0] - cy) > 2:
            lines.append(cur)
            cur = []
        cur.append(w)
        cy = w[0]
    if cur:
        lines.append(cur)
    out = []
    for ln in lines:
        ln.sort(key=lambda w: w[1])
        s = ln[0][3]
        for a, b in zip(ln, ln[1:]):
            s += ("" if b[1] - a[4] < 0.6 else " ") + b[3]
        out.append(s.strip())
    return " / ".join(out)


def columns(hdr):
    t = lambda w: w[3].strip()  # noqa: E731
    hs = sorted(hdr, key=lambda w: w[1])
    mnw = next((w for w in hs if re.match(r"^Min", t(w)) and w[1] < 330), None)
    if mnw is None:
        return None
    mn = mnw[1]
    if "Max" in t(mnw):                                   # "Mini-   Maxi-" in one word box (2002-2005)
        mx = mn + t(mnw).index("Max") * 0.3 * mnw[2]
    else:
        mx = next(w[1] for w in hs if re.match(r"^Max", t(w)) and mn < w[1] < 330)
    ed = next((w[1] for w in hs if re.match(r"^Earn", t(w)) and w[1] > mx), mx + 45)
    maxes = [w[1] for w in hs if re.match(r"^Max", t(w)) and mx + 100 < w[1] < 470]
    weeks = [w[1] for w in hs if re.match(r"^(Weeks|Payable)", t(w)) and w[1] > mx + 100]
    cols = {"min": (mn - 12, (mn + mx) / 2), "max": ((mn + mx) / 2, min(ed - 12, mx + 42))}
    if weeks:
        cols["weeks"] = (max(weeks) - 10, max(weeks) + 26)
    elif maxes:                                           # 2000-2001: "Benefit weeks ... Min. / Max."
        cols["weeks"] = (maxes[0] - 12, maxes[0] + 25)
    comp = next((w[1] for w in hs if re.match(r"^Comput", t(w))), None)
    if comp:
        cols["comp"] = (comp - 15, mn - 12)
    return cols


def text_cells(year, month="July"):
    """state -> raw cell strings (min, max, weeks, comp) of the July issue."""
    res, cols, last = {}, None, None
    for words in pages(year, month):
        if not words:
            continue
        from collections import Counter
        body = Counter(round(w[2], 1) for w in words).most_common(1)[0][0]
        labs = []
        for w in sorted(words, key=lambda w: -w[0]):
            s = w[3].strip()
            if s in ALL_LABELS and w[1] < 45 and w[2] >= 0.8 * body and s not in res and s not in [l[1] for l in labs]:
                labs.append((w[0], s))
        if not labs:
            continue
        top = labs[0][0]
        c = columns([w for w in words if w[0] > top + 4])
        if c is None:                         # continuation page: same columns; words above the first label
            if cols is None or last is None:  # continue the last state of the previous page
                continue
            cont = [w for w in words if w[0] > top + 12]
            for k, (a, b) in cols.items():
                extra = join([w for w in cont if a <= w[1] < b], body)
                if extra:
                    res[last][k] = (res[last].get(k, "") + " / " + extra).strip(" /")
        else:
            cols = c
        ys = [l[0] for l in labs]
        for i, (ly, st) in enumerate(labs):
            up = (ys[i - 1] + ly) / 2 if i else ly + (12 if c is None else 25)
            dn = max((ly + ys[i + 1]) / 2 if i + 1 < len(ys) else ly - 25, ly - 40)
            up = min(up, ly + 40)
            row = [w for w in words if dn < w[0] <= up]
            # a state label must have a number in the WBA columns on its row (labels in the notes are skipped)
            if not any(re.search(r"\d", w[3]) for w in row if cols["min"][0] <= w[1] < cols["max"][1]):
                continue
            res[st] = {k: join([w for w in row if a <= w[1] < b], body) for k, (a, b) in cols.items()}
            last = st
    return res


NUM = r"(\d+(?:\.\d+)?)"


def clean(s):
    s = s.replace(",", "").replace("$", "").replace("–", "-").replace("—", "-").replace("‐", "-")
    s = re.sub(r"\(.*$", " ", s)                      # values effective later in the year: "(eff. ...)" dropped
    s = re.sub(r"\b\d+\)", " ", s)                    # tails of a previous cell's "(effective 10/5/03)"
    s = re.sub(r"\d{1,2}/\d{1,2}/\d{2,4}", " ", s)
    s = re.sub(r"\d+(?:\.\d+)?\s*%", " ", s)          # "63% of AWW"
    s = re.sub(r"\s*-\s*(?:/\s*)?", "-", s)           # "$56- / 128" -> "56-128"
    return s


def parse_amount(s, st):
    """cell -> (base, upper, alternative-maximum flag)."""
    c = clean(s)
    m = re.search(NUM + r"-" + NUM, c)
    nums = [float(x) for x in re.findall(NUM, c)]
    if not nums:
        return np.nan, np.nan, False
    if st in ALT_MAX:
        return max(nums), np.nan, len(nums) > 1
    if m and c.find(m.group(0)) <= c.find(re.findall(NUM, c)[0]):
        return float(m.group(1)), float(m.group(2)), False
    return nums[0], np.nan, False


def parse_weeks(s):
    c = clean(s)
    m = re.search(NUM + r"\+?-" + NUM, c)
    if m:
        v = float(m.group(2))
    else:
        nums = [float(x) for x in re.findall(NUM, c)]
        if not nums:
            return np.nan
        v = max(nums)
    if v > 52:                                        # "267/" = 26 + footnote 7
        v = float(str(int(v))[:2])
    return v


def text_rows():
    rows = []
    for y in range(2000, max(YEARS) + 1):
        cells = text_cells(y)
        for st in ST:
            c = cells.get(st)
            if c is None:
                continue
            a, a2, _ = parse_amount(c.get("min", ""), st)
            b, b2, alt = parse_amount(c.get("max", ""), st)
            dep = int(bool(re.search(r"(?i)\bdeps?\b|\bDA\b|dependent|d\.a\.", c.get("comp", "") + " "
                                     + c.get("max", "") + " " + c.get("min", ""))) or not np.isnan(b2))
            r = dict(year=y, state=st, min_wba=a, min_wba_dep=a2, max_wba=b, max_wba_dep=b2,
                     max_duration_weeks=parse_weeks(c.get("weeks", "")), dep_allowance=dep,
                     law_src=f"SigPros July {y} (text layer)",
                     law_note="higher of two alternative maxima" if alt else "",
                     raw_min=c.get("min", ""), raw_max=c.get("max", ""), raw_weeks=c.get("weeks", ""))
            o = OVERRIDES.get((y, st))
            if o:
                for k, v in o.items():
                    if k == "note":
                        r["law_note"] = (r["law_note"] + "; " + v).strip("; ")
                    else:
                        r[k] = v
                r["law_src"] += " + manual check"
            rows.append(r)
    return pd.DataFrame(rows)


def law_panel():
    sc, tx = scan_rows(), text_rows()
    tx = tx[~tx.set_index(["year", "state"]).index.isin(sc.set_index(["year", "state"]).index)]
    law = pd.concat([sc, tx], ignore_index=True)
    # alternative (non-DA) maxima transcribed as a range in the scans (MN 1999): keep the higher one
    alt = law.state.isin(ALT_MAX) & (law.dep_allowance == 0) & (law.max_wba_dep > law.max_wba)
    law.loc[alt, "law_note"] = "higher of two alternative maxima"
    law.loc[alt, "max_wba"] = law.loc[alt, "max_wba_dep"]
    law.loc[alt, "max_wba_dep"] = np.nan
    law["max_wba_dep"] = law.max_wba_dep.fillna(law.max_wba)
    law["min_wba_dep"] = law.min_wba_dep.fillna(law.min_wba)
    # (2024 MA: allowance uncapped -> no finite maximum with dependents)
    law.loc[(law.state == "MA") & (law.year == 2024), "max_wba_dep"] = np.nan
    idx = law.state.map(INDEXED_WEEKS)
    ind = idx.notna() & (law.year >= idx)
    law.loc[ind, "law_note"] = (law.loc[ind, "law_note"].fillna("") + "; maximum weeks below 26 or indexed to the unemployment rate by "
                                "later legislation; value as printed in the July table").str.strip("; ")
    return law


# ---------------------------------------------------------------------------------------------------------------------
# (2)-(4) DOL administrative data and BEA wages
def eta5159():
    d = pd.read_csv(EXT / "ar5159.csv")
    d["year"] = d.rptdate.str[:4].astype(int)
    g = d.groupby(["st", "year"]).agg(n=("rptdate", "size"), weeks=("c39", "sum"), paid=("c46", "sum"))
    g = g[g.n == 12]
    g["awb"] = g.paid / g.weeks
    return g.reset_index().rename(columns={"st": "state"})[["state", "year", "awb"]]


def eta218():
    d = pd.read_csv(EXT / "ar218.csv")
    d["year"] = d.rptdate.str[:4].astype(int)
    d["c29w"] = d.c29 * d.c9
    g = d.groupby(["st", "year"]).agg(n=("rptdate", "size"), c4=("c4", "sum"), c5=("c5", "sum"), c9=("c9", "sum"),
                                       c28=("c28", "sum"), c29w=("c29w", "sum"))
    g = g[g.n == 4]
    out = pd.DataFrame({"share_max_wba": g.c5 / g.c4, "share_max_duration": g.c28 / g.c9,
                        "avg_potential_duration": g.c29w / g.c9})
    return out.reset_index().rename(columns={"st": "state"})


def bea_aww():
    with zipfile.ZipFile(EXT / "bea" / "SAINC.zip") as z:
        d = pd.read_csv(io.BytesIO(z.read("SAINC30__ALL_AREAS_1958_2025.csv")), encoding="latin-1", dtype=str)
    d = d[d.LineCode.str.strip() == "300"]
    d["state_fips"] = pd.to_numeric(d.GeoFIPS.str.strip().str.strip('"').str[:2], errors="coerce")
    inv = {v: k for k, v in FIPS.items()}
    d = d[d.state_fips.isin(inv)]
    yrs = [c for c in d.columns if c.isdigit()]
    m = d.melt(id_vars=["state_fips"], value_vars=yrs, var_name="year", value_name="wage")
    m["year"] = m.year.astype(int)
    m["aww"] = pd.to_numeric(m.wage, errors="coerce") / 52
    m["state"] = m.state_fips.map(inv)
    return m[["state", "year", "aww"]]


def hb394_check():
    """Handbook 394 report(s) saved in EXT (only Alabama could be retrieved): AWB, AWW, ratio."""
    out = []
    for f in sorted(EXT.glob("hb394_*.html")):
        ts = pd.read_html(io.StringIO(f.read_text(encoding="utf-8", errors="replace")), flavor="lxml")
        emp, clm = ts[0], ts[3]
        emp.columns = [" | ".join(map(str, c)) for c in emp.columns]
        clm.columns = [" | ".join(map(str, c)) for c in clm.columns]
        e = pd.DataFrame({"year": pd.to_numeric(emp.iloc[:, 0], errors="coerce"),
                          "hb_aww": pd.to_numeric(emp[[c for c in emp.columns if "Average weekly wage" in c
                                                       and "Total" in c][0]].astype(str).str.replace(",", ""),
                                                  errors="coerce")})
        c = pd.DataFrame({"year": pd.to_numeric(clm.iloc[:, 0], errors="coerce"),
                          "hb_awb": pd.to_numeric(clm.iloc[:, -2], errors="coerce"),
                          "hb_ratio": pd.to_numeric(clm.iloc[:, -1], errors="coerce")})
        x = e.merge(c, on="year").dropna(subset=["year"])
        x["year"] = x.year.astype(int)
        title = re.search(r"REPORT FOR \d{4} THROUGH \d{4}\s+(\w[\w ]*?)\s+Taxable", re.sub(r"<[^>]+>", " ",
                                                                                          f.read_text("utf-8")))
        x["state_name"] = title.group(1) if title else f.stem
        out.append(x)
    return pd.concat(out) if out else pd.DataFrame()


# ---------------------------------------------------------------------------------------------------------------------
def to2000(x, year):
    return x * CPI[2000] / CPI[year]


def build():
    download()
    law = law_panel()
    grid = pd.DataFrame([(s, y) for s in ST for y in YEARS], columns=["state", "year"])
    p = grid.merge(law, on=["state", "year"], how="left")
    p = p.merge(eta5159(), on=["state", "year"], how="left").merge(eta218(), on=["state", "year"], how="left")
    p = p.merge(bea_aww(), on=["state", "year"], how="left")
    p["state_fips"] = p.state.map(FIPS)
    p["repl_rate"] = p.awb / p.aww
    p["max_wba_repl"] = p.max_wba / p.aww
    for v in ("max_wba", "max_wba_dep", "min_wba", "awb", "aww"):
        p[f"{v}_2000"] = [to2000(x, y) for x, y in zip(p[v], p.year)]
    p["max_benefit_2000"] = p.max_wba_2000 * p.max_duration_weeks
    p["src_awb"] = np.where(p.awb.notna(), "DOL ETA 5159 (ar5159.csv): c46/c39", "")
    p["src_218"] = np.where(p.share_max_wba.notna(), "DOL ETA 218 (ar218.csv)", "")
    p["src_aww"] = np.where(p.aww.notna(), "BEA SAINC30 line 300 / 52", "")
    cols = ["state", "state_fips", "year", "max_wba", "max_wba_2000", "max_wba_dep", "max_wba_dep_2000", "min_wba",
            "min_wba_2000", "min_wba_dep", "max_duration_weeks", "max_benefit_2000", "dep_allowance", "awb",
            "awb_2000", "aww", "aww_2000", "repl_rate", "max_wba_repl", "share_max_wba", "share_max_duration",
            "avg_potential_duration", "law_src", "law_note", "src_awb", "src_218", "src_aww"]
    p = p[cols].sort_values(["state", "year"]).reset_index(drop=True)
    for c in p.columns:
        if p[c].dtype == float:
            p[c] = p[c].round(4)
    return p, law


# ---------------------------------------------------------------------------------------------------------------------
def md_table(df, floatfmt="{:.2f}"):
    df = df.copy()
    head = "| " + " | ".join(map(str, df.columns)) + " |"
    sep = "|" + "|".join("---" for _ in df.columns) + "|"
    rows = []
    for r in df.itertuples(index=False):
        rows.append("| " + " | ".join(floatfmt.format(v) if isinstance(v, float) and v == v else
                                     ("" if isinstance(v, float) else str(v)) for v in r) + " |")
    return "\n".join([head, sep, *rows])


def checks(p, law):
    L = ["# UI generosity panel: checks", "",
         "Built by `IGE/12b.UIGenerosity.py` -> `data/ui_generosity.csv` (51 states incl. DC x 1976-2024). "
         "Sources and conventions: see the script docstring.", ""]
    # coverage
    cov = []
    for v in ("max_wba", "max_wba_dep", "min_wba", "max_duration_weeks", "dep_allowance", "awb", "aww",
              "repl_rate", "share_max_wba", "share_max_duration", "avg_potential_duration"):
        nn = p[p[v].notna()]
        full = nn.groupby("year").state.nunique()
        cov.append(dict(variable=v, first_year=int(nn.year.min()), last_year=int(nn.year.max()),
                        state_years=len(nn), years_with_all_51=int((full == 51).sum()),
                        missing_state_years=int(len(p[(p.year >= nn.year.min()) & (p.year <= nn.year.max())])
                                                - len(nn))))
    L += ["## Coverage", "", md_table(pd.DataFrame(cov)), ""]
    miss = p[p.max_wba.isna()][["state", "year", "law_note"]]
    if len(miss):
        L += ["Missing max_wba: " + ", ".join(f"{r.state} {r.year}" for r in miss.itertuples()), ""]
    # summary by year
    g = p.groupby("year").agg(max_wba=("max_wba", "mean"), max_wba_2000=("max_wba_2000", "mean"),
                              max_wba_dep_2000=("max_wba_dep_2000", "mean"), sd_max_2000=("max_wba_2000", "std"),
                              max_weeks=("max_duration_weeks", "mean"), n_dep=("dep_allowance", "sum"),
                              awb_2000=("awb_2000", "mean"), repl_rate=("repl_rate", "mean"),
                              max_repl=("max_wba_repl", "mean"), share_max_wba=("share_max_wba", "mean"),
                              pot_dur=("avg_potential_duration", "mean")).reset_index()
    L += ["## Summary by year (unweighted means over states)", "",
          "max_wba / awb in nominal and 2000 dollars; max_repl = max_wba / aww; share_max_wba = share of new "
          "claimants eligible for the maximum (ETA 218); pot_dur = average potential duration (weeks).", "",
          md_table(g), ""]
    dec = p.assign(decade=p.year // 10 * 10).groupby("decade").agg(
        max_wba_2000=("max_wba_2000", "mean"), awb_2000=("awb_2000", "mean"), repl_rate=("repl_rate", "mean"),
        repl_min=("repl_rate", "min"), repl_max=("repl_rate", "max"), max_weeks=("max_duration_weeks", "mean"))
    L += ["## By decade", "", md_table(dec.reset_index()), ""]
    # sanity checks
    s = p.copy()
    s["prev"] = s.groupby("state").max_wba.shift()
    s["chg"] = s.max_wba / s.prev - 1
    fall = s[s.chg < -0.001][["state", "year", "prev", "max_wba", "law_src"]]
    jump = s[s.chg > 0.25][["state", "year", "prev", "max_wba", "law_src"]]
    bad_awb = s[s.awb > s.max_wba_dep * 1.02][["state", "year", "awb", "max_wba", "max_wba_dep"]]
    low_awb = s[s.awb < 0.35 * s.max_wba][["state", "year", "awb", "max_wba"]]
    minmax = s[s.min_wba > s.max_wba][["state", "year", "min_wba", "max_wba"]]
    L += ["## Sanity checks", "",
          f"* min_wba > max_wba: {len(minmax)} state-years.",
          f"* AWB above the maximum incl. dependents' allowances (x1.02): {len(bad_awb)} state-years"
          + (": " + ", ".join(f"{r.state} {r.year} ({r.awb:.0f} vs {r.max_wba_dep:.0f})" for r in bad_awb.itertuples())
             if len(bad_awb) else "."),
          f"* AWB below 35% of max_wba: {len(low_awb)} state-years"
          + (": " + ", ".join(f"{r.state} {r.year}" for r in low_awb.itertuples()) if len(low_awb) else "."),
          f"* Nominal max_wba falls from one July to the next: {len(fall)} cases (legislated cuts or freezes are "
          "printed values; small declines are indexed maxima following the state average wage, larger ones "
          "legislated cuts or freezes, e.g. LA 1988-89, DC 1997, NC 2013, OK 2004/2011/2021 (trust-fund-linked "
          "schedule); SC 1978 = 119 is printed between 111 in 1977 and 1979):", "",
          md_table(fall.rename(columns={"prev": "max_prev_year"}), "{:.0f}"), "",
          f"* Nominal max_wba rises by more than 25% in a year: {len(jump)} cases:", "",
          md_table(jump.rename(columns={"prev": "max_prev_year"}), "{:.0f}"), ""]
    corr = p[["max_wba", "awb", "share_max_wba", "repl_rate", "max_wba_repl"]].corr().round(2)
    L += ["Correlations (state-years):", "", md_table(corr.reset_index()), ""]
    # Handbook 394 check
    hb = hb394_check()
    if len(hb):
        st = {"Alabama": "AL"}.get(hb.state_name.iloc[0], None)
        x = hb.merge(p[p.state == st][["year", "awb", "aww", "repl_rate"]], on="year", how="inner")
        x = x[x.year.isin([1976, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2023, 2024])]
        L += [f"## Check against ET Handbook 394 ({hb.state_name.iloc[0]})", "",
              "hb_* = Handbook 394 (average weekly benefit, AWW in covered employment, AWB/AWW ratio); right-hand "
              "columns = this panel (ETA 5159 AWB, BEA wages per job / 52).", "", md_table(x), ""]
    # a few states
    for v, lab in (("max_wba", "Maximum WBA (nominal $)"), ("max_wba_2000", "Maximum WBA (2000 $)"),
                   ("repl_rate", "AWB / AWW")):
        w = p[p.state.isin(["CA", "TX", "NY", "MI", "MS", "MA", "FL", "NC"])].pivot(index="year", columns="state",
                                                                                    values=v)
        w = w[w.index % 4 == 0]
        L += [f"## {lab}, selected states (every 4th year)", "", md_table(w.reset_index(), "{:.2f}" if
                                                                          v == "repl_rate" else "{:.0f}"), ""]
    # January issues: the July maximum should lie between the January values of the same and the next year
    jan = {}
    for y in range(2000, max(YEARS) + 2):
        for st_, c in text_cells(y, "January").items():
            if st_ in FIPS:
                jan[(y, st_)] = parse_amount(c.get("max", ""), st_)[0]
    rows = []
    for r in p[p.year >= 2000].itertuples():
        a, b = jan.get((r.year, r.state), np.nan), jan.get((r.year + 1, r.state), np.nan)
        lo, hi = np.nanmin([a, b]), np.nanmax([a, b])
        if r.max_wba == r.max_wba and lo == lo and not (lo - 1 <= r.max_wba <= hi + 1):
            rows.append(dict(state=r.state, year=r.year, jan_same_year=a, july=r.max_wba, jan_next_year=b,
                             note=r.law_note))
    L += ["## Cross-check of the July maxima (2000-2024) against the January issues", "",
          "The January issues of year t and t+1 are parsed the same way; a July value outside [min, max] of the two "
          f"January values (+-1) is listed. {len(rows)} of {int(p[p.year >= 2000].max_wba.notna().sum())} "
          "state-years. Most are states that index or change the maximum between July and January (the "
          "January issue then shows a value on the far side of an increase and a later cut, or a parsing issue of "
          "the January table); none was changed on this basis alone except where noted in OVERRIDES.", "",
          md_table(pd.DataFrame(rows), "{:.0f}") if rows else "(none)", ""]
    # notes, grouped by state and text
    notes = p[p.law_note.fillna("") != ""][["state", "year", "law_note"]]
    g = notes.groupby(["state", "law_note"]).year.agg(lambda s: f"{s.min()}-{s.max()}" if len(s) > 1 else
                                                      str(s.min())).reset_index()
    L += ["## Notes on individual cells", "", md_table(g[["state", "year", "law_note"]]), ""]
    (OUT / "ui_generosity_checks.md").write_text("\n".join(L), encoding="utf-8")


def main():
    p, law = build()
    p.to_csv(DATA / "ui_generosity.csv", index=False)
    print(f"ui_generosity.csv: {p.shape}")
    checks(p, law)
    print(p.groupby(p.year // 10 * 10)[["max_wba_2000", "awb_2000", "repl_rate", "max_duration_weeks"]].mean())


if __name__ == "__main__":
    main()
