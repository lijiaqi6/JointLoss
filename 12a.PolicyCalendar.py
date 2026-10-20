r"""State x year policy calendar for the Phase 3 policy designs (2026-10-17).

Writes data/policy_calendar.csv: 51 states (incl. DC) x 1980-2024. For every dated policy P three columns:
  P_date   the date the policy took effect in the state (constant within state; empty if never / not coded)
  P        fraction of the calendar year in which the policy was in effect (0-1)
  P_jul1   1 if in effect on 1 July of the year
plus the level variables listed below. Web pages are cached in data/ (downloaded once if missing).

(1) State paid family leave (PFL), date benefits first became payable. Source: A Better Balance, "Paid Leave Program
    Implementation Timelines" (Aug 2023), https://www.abetterbalance.org/wp-content/uploads/2021/07/Paid-Leave-
    Program-Implementation-Timelines_8.1.23.pdf (enactment / start of contributions / start of benefits; footnotes
    for MA, CT, OR delays). Verified dates (benefits start): CA 1 Jul 2004 (enacted 26 Sep 2002); NJ 30 Jun 2009
    (enacted 2 May 2008; contributions from 1 Jan 2009); RI 1 Jan 2014 (enacted 11 Jul 2013); NY 1 Jan 2018
    (enacted 1 Apr 2016); WA 1 Jan 2020 (enacted 5 Jul 2017); DC 1 Jul 2020 (enacted 17 Feb 2017); MA 1 Jan 2021
    (enacted 28 Jun 2018); CT 1 Jan 2022 (enacted 25 Jun 2019; fn 3); OR 3 Sep 2023 (enacted 9 Aug 2019; fn 4: delayed
    from 2023-01-01); CO 1 Jan 2024 (ballot initiative 3 Nov 2020). Programs paying from 2025 on are outside the panel.
(2) Job-protected leave.
    fmla_federal: Title I of the FMLA in effect from 5 Aug 1993 (for workers under a collective bargaining agreement in
    force then: its expiry or 5 Feb 1994, whichever earlier - not coded). Source: DOL final rule, Federal Register
    60(4), 6 Jan 1995, https://www.govinfo.gov/content/pkg/FR-1995-01-06/html/94-32342.htm .
    state_mat_leave / state_pat_leave: state laws mandating job-protected maternity / paternity leave for private-
    sector workers in effect before the FMLA, effective dates from Waldfogel (1999), "Family leave coverage in the
    1990s", Monthly Labor Review 122(10), Appendix, https://www.bls.gov/opub/mlr/1999/10/art2full.pdf (sources there:
    Irwin and Silberman 1993; Women's Legal Defense Fund 1993, 1997). Maternity: CA Jan 1980, CT Jan 1973, DC Apr 1991,
    ME Apr 1988, MA Oct 1972, MN Jul 1987, NJ Apr 1990, OR Jan 1988, RI Jul 1987, TN Jan 1988, VT Jul 1992, WA Oct
    1973, WI Apr 1988. Paternity: CA Jan 1992, CT Jan 1990, DC Apr 1991, ME Oct 1991, MN Jul 1987, NJ Apr 1990, OR Jan
    1988, RI Jul 1987, VT Jul 1992, WA Sep 1989, WI Apr 1988. (The PDF's text layer shifts the date column by one row;
    the assignment above is the one consistent with the article's statement that four states - CA, CT, ME, WA -
    adopted paternity leave later than maternity leave and with the known CA 1980 / DC 1991 / NJ 1990 laws.) The state
    laws differ in employer-size thresholds and leave length (not coded). Laws are kept in force after 1993.
    job_protect = 1 if the federal FMLA or a state maternity-leave law is in effect.
(3) Welfare reform. NOT in the UKCPR file: the January 2026 UKCPR workbook's Data sheet has no waiver / TANF /
    time-limit / exemption columns (the "Spring 2013 Updates" sheet documents such columns, anyapp ... imwrk, but they
    are no longer in the Data sheet). Taken instead from ASPE (Crouse 1999), "State Implementation of Major Changes to
    Welfare Policies, 1992-1998", https://aspe.hhs.gov/reports/state-implementation-major-changes-welfare-policies-
    1992-1998-0 (the dates used by the 1999 CEA caseload study; statewide or majority-of-state implementation dates;
    dates "arbitrarily stated as of the first of the month absent specific information"):
      Table A   waiver_any (earliest major AFDC waiver implemented; coded only until TANF), tanf (TANF implemented:
                the "actual" date where ASPE gives one - CA, MS, NJ, NY, WI - else the official date; both kept)
      Table B   waiver_tl, waiver_exempt, waiver_sanction, waiver_disregard, waiver_famcap, waiver_workreq:
                implementation dates of the six major AFDC waiver policies (cells "--(n)" = partial / phased-in per
                the footnote, left uncoded)
      Table W-1 time_limit = AFDC termination/reduction time-limit waiver implemented, or TANF implemented with a
                time limit (all states except MI, VT; IA "individualized"); tanf_tl (text), tanf_tl_months (first
                number in the text, i.e. the first binding limit), tanf_tl_type (termination / reduction /
                reduction then termination / none)
      Table W-2/W-2a  work_exempt_m = age of the youngest child (months) below which a parent is exempt from work
                requirements, on 1 July: TANF policy from its W-2a date (else the TANF date); AFDC-waiver policy from
                its W-2a date; before that the state's JOBS option as of August 1996 (Family Support Act 1988:
                child under 3, or at state option any age >= 1; 37 jurisdictions 36 m; CT, NJ 24 m; AZ AR CO IN LA MI
                MT NE OK OR SC SD WI WY 12 m), from the JOBS start date 1 Oct 1990 - source: 1998 Green Book, Section
                7 (AFDC/JOBS), https://aspe.hhs.gov/sites/default/files/migrated_legacy_files//155781/7bafdc.txt .
                Before Oct 1990 (WIN) not coded. work_exempt_src says which rule applies. tanf_exempt_12m_lifetime = 1
                if the TANF exemption is limited to 12 months in total. Colorado TANF: county option (NaN).
(4) UKCPR National Welfare Data 1980-2024 (Jan 2026 update; ExternalData/ukcpr_national_welfare_data_1980_2024_
    jan26update.xlsx, sheet Data; note its column "state_name" holds the postal code): unemployment rate,
    AFDC/TANF maximum monthly benefit for 2-, 3-, 4-person families, AFDC/TANF + food stamp 3-person benefit,
    state EITC rate and refundability, state and federal minimum wage, federal EITC maximum credit (1, 2 children).
    The UKCPR file has NO unemployment-insurance variable (no maximum weekly benefit, no replacement rate), so UI
    generosity is not in the calendar.
"""
import re
import urllib.request
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
ROOT = HERE.parent
UKCPR = ROOT / "ExternalData" / "ukcpr_national_welfare_data_1980_2024_jan26update.xlsx"
ASPE_URL = "https://aspe.hhs.gov/reports/state-implementation-major-changes-welfare-policies-1992-1998-0"
ASPE_HTML = DATA / "aspe_welfare_policies_1992_1998.html"
YEARS = range(1980, 2025)

ABBR = {"Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO",
        "Connecticut": "CT", "Delaware": "DE", "Dist. of Columbia": "DC", "DC": "DC", "Florida": "FL", "Georgia": "GA",
        "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
        "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI",
        "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
        "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
        "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
        "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX",
        "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
        "Wisconsin": "WI", "Wyoming": "WY"}

PFL = {"CA": "2004-07-01", "NJ": "2009-06-30", "RI": "2014-01-01", "NY": "2018-01-01", "WA": "2020-01-01",
       "DC": "2020-07-01", "MA": "2021-01-01", "CT": "2022-01-01", "OR": "2023-09-03", "CO": "2024-01-01"}
PFL_ENACTED = {"CA": "2002-09-26", "NJ": "2008-05-02", "RI": "2013-07-11", "NY": "2016-04-01", "WA": "2017-07-05",
               "DC": "2017-02-17", "MA": "2018-06-28", "CT": "2019-06-25", "OR": "2019-08-09", "CO": "2020-11-03"}
FMLA = "1993-08-05"
MAT = {"CA": "1980-01-01", "CT": "1973-01-01", "DC": "1991-04-01", "ME": "1988-04-01", "MA": "1972-10-01",
       "MN": "1987-07-01", "NJ": "1990-04-01", "OR": "1988-01-01", "RI": "1987-07-01", "TN": "1988-01-01",
       "VT": "1992-07-01", "WA": "1973-10-01", "WI": "1988-04-01"}
PAT = {"CA": "1992-01-01", "CT": "1990-01-01", "DC": "1991-04-01", "ME": "1991-10-01", "MN": "1987-07-01",
       "NJ": "1990-04-01", "OR": "1988-01-01", "RI": "1987-07-01", "VT": "1992-07-01", "WA": "1989-09-01",
       "WI": "1988-04-01"}
JOBS_START = "1990-10-01"
JOBS_24 = {"CT", "NJ"}
JOBS_12 = {"AZ", "AR", "CO", "IN", "LA", "MI", "MT", "NE", "OK", "OR", "SC", "SD", "WI", "WY"}

DATE = re.compile(r"(\d{1,2})-(\d{1,2})-(\d{2})")


def pdate(x):
    """ASPE cell 'm-d-yy' (possibly with a footnote mark) -> Timestamp; '--(n)', blanks -> NaT."""
    m = DATE.search(str(x))
    if not m:
        return pd.NaT
    mo, d, y = map(int, m.groups())
    return pd.Timestamp(1900 + y, mo, d)


def months(x):
    """'1 year', '13 weeks', '90 days', 'No exemption' ... -> months (float); county option / blank -> NaN."""
    s = str(x).lower()
    if s.startswith("no"):
        return 0.0
    m = re.match(r"\s*(\d+)\s*(year|month|week|day)", s)
    if not m:
        return np.nan
    v, u = int(m.group(1)), m.group(2)
    return {"year": 12.0 * v, "month": float(v), "week": v / 4.345, "day": v / 30.44}[u]


def frac_year(start, end, year):
    """fraction of calendar year `year` in [start, end) (end NaT = open)."""
    if pd.isna(start):
        return 0.0
    a, b = pd.Timestamp(year, 1, 1), pd.Timestamp(year + 1, 1, 1)
    lo, hi = max(a, start), min(b, end) if not pd.isna(end) else b
    return max(0.0, (hi - lo).days / (b - a).days)


def on(start, end, year):
    j = pd.Timestamp(year, 7, 1)
    return float(not pd.isna(start) and start <= j and (pd.isna(end) or j < end))


def aspe_tables():
    if not ASPE_HTML.exists():
        req = urllib.request.Request(ASPE_URL, headers={"User-Agent": "Mozilla/5.0"})
        ASPE_HTML.write_bytes(urllib.request.urlopen(req, timeout=60).read())
    ts = pd.read_html(ASPE_HTML)
    out = []
    for t in ts:
        t = t.copy()
        t.columns = range(t.shape[1])
        t = t[t[0].astype(str).str.replace(r"\s*\(\d+\)", "", regex=True).str.strip().isin(ABBR)]
        t[0] = t[0].astype(str).str.replace(r"\s*\(\d+\)", "", regex=True).str.strip().map(ABBR)
        out.append(t.set_index(0))
    return out


def welfare():
    A, B1, B2, W1, W2, W2a = aspe_tables()[:6]
    w = pd.DataFrame(index=sorted(set(ABBR.values())))
    w["waiver_any_approved_date"] = A[1].map(pdate)
    w["waiver_any_date"] = A[2].map(pdate)
    w["tanf_official_date"] = A[3].map(pdate)
    w["tanf_actual_date"] = A[4].map(pdate)
    w["tanf_date"] = w.tanf_actual_date.fillna(w.tanf_official_date)
    for name, tab, col in (("waiver_tl", B1, 2), ("waiver_exempt", B1, 4), ("waiver_sanction", B1, 6),
                           ("waiver_disregard", B2, 2), ("waiver_famcap", B2, 4), ("waiver_workreq", B2, 6)):
        w[f"{name}_date"] = tab[col].map(pdate)
    w["tanf_tl"] = W1[5]
    w["tanf_tl_months"] = W1[5].astype(str).str.extract(r"(\d+)")[0].astype(float)
    red = W1[6].astype(str).str.contains(r"reduction|\d", regex=True)
    term = W1[7].astype(str).str.contains(r"termination|\d", regex=True)
    w["tanf_tl_type"] = pd.Series(np.where(W1[5].astype(str).str.lower().eq("none"), "none",
                                           np.where(red & ~term, "reduction",
                                                    np.where(red & term, "reduction then termination",
                                                             "termination"))), index=W1.index)
    w["tanf_has_tl"] = ~W1[5].astype(str).str.lower().isin(["none"])
    w["tanf_exempt_m"] = W2[5].map(months)
    w["tanf_exempt_text"] = W2[5]
    w["tanf_exempt_12m_lifetime"] = (W2[6].astype(str).str.upper() == "X").astype(float)
    w["tanf_exempt_date"] = W2a[[6, 7, 8]].apply(lambda r: next((pdate(v) for v in r if not pd.isna(pdate(v))), pd.NaT),
                                                 axis=1)
    w["tanf_exempt_date"] = w.tanf_exempt_date.fillna(w.tanf_date)
    w["afdc_exempt_m"] = W2a[1].map(months)
    w["afdc_exempt_text"] = W2a[1]
    w["afdc_exempt_date"] = W2a[[2, 3, 4]].apply(lambda r: next((pdate(v) for v in r if not pd.isna(pdate(v))), pd.NaT),
                                                 axis=1)
    w["jobs_exempt_m"] = [24.0 if s in JOBS_24 else 12.0 if s in JOBS_12 else 36.0 for s in w.index]
    return w


def main():
    DATA.mkdir(exist_ok=True)
    u = pd.read_excel(UKCPR, sheet_name="Data")
    keep = {"Unemployment rate": "ur", "AFDC/TANF Benefit for 2-Person family": "afdc_max2",
            "AFDC/TANF Benefit for 3-person family": "afdc_max3", "AFDC/TANF benefit for 4-person family": "afdc_max4",
            "AFDC/TANF_FS 3-Person Benefit": "afdc_fs_max3", "State EITC Rate": "state_eitc_rate",
            "Refundable State EITC (1=Yes)": "state_eitc_refundable", "State Minimum Wage": "min_wage_state",
            "Federal Minimum Wage": "min_wage_fed", "EITC Maximum Credit 1 Dependent": "eitc_max1",
            "EITC Maximum Credit 2 Dependents": "eitc_max2"}
    u = u.rename(columns={"state_name": "state", "state": "ukcpr_state_code", **keep})
    u = u[["state", "state_fips", "year", *keep.values()]]
    w = welfare()
    rows = []
    for st in sorted(set(ABBR.values())):
        wi = w.loc[st]
        ts = lambda x: pd.Timestamp(x) if x else pd.NaT  # noqa: E731
        spans = {  # policy: (start, end)
            "fmla_federal": (ts(FMLA), pd.NaT),
            "state_mat_leave": (ts(MAT.get(st)), pd.NaT),
            "state_pat_leave": (ts(PAT.get(st)), pd.NaT),
            "pfl": (ts(PFL.get(st)), pd.NaT),
            "waiver_any": (wi.waiver_any_date, wi.tanf_date),
            "tanf": (wi.tanf_date, pd.NaT),
            "time_limit": (min([d for d in (wi.waiver_tl_date, wi.tanf_date if wi.tanf_has_tl else pd.NaT)
                                if not pd.isna(d)], default=pd.NaT), pd.NaT),
        }
        for p in ("waiver_tl", "waiver_exempt", "waiver_sanction", "waiver_disregard", "waiver_famcap",
                  "waiver_workreq"):
            spans[p] = (wi[f"{p}_date"], wi.tanf_date)
        for y in YEARS:
            r = dict(state=st, year=y)
            for p, (a, b) in spans.items():
                r[f"{p}_date"] = a.date().isoformat() if not pd.isna(a) else ""
                r[p] = round(frac_year(a, b, y), 4)
                r[f"{p}_jul1"] = on(a, b, y)
            r["job_protect_jul1"] = max(r["fmla_federal_jul1"], r["state_mat_leave_jul1"])
            r["job_protect"] = max(r["fmla_federal"], r["state_mat_leave"])
            r["pfl_enacted_date"] = PFL_ENACTED.get(st, "")
            r["tanf_official_date"] = wi.tanf_official_date.date().isoformat() if not pd.isna(wi.tanf_official_date) else ""
            r["tanf_actual_date"] = wi.tanf_actual_date.date().isoformat() if not pd.isna(wi.tanf_actual_date) else ""
            r["waiver_any_approved_date"] = (wi.waiver_any_approved_date.date().isoformat()
                                             if not pd.isna(wi.waiver_any_approved_date) else "")
            j = pd.Timestamp(y, 7, 1)
            if not pd.isna(wi.tanf_exempt_date) and j >= wi.tanf_exempt_date:
                em, src = wi.tanf_exempt_m, "TANF"
            elif not pd.isna(wi.afdc_exempt_date) and j >= wi.afdc_exempt_date:
                em, src = wi.afdc_exempt_m, "AFDC waiver"
            elif j >= pd.Timestamp(JOBS_START):
                em, src = wi.jobs_exempt_m, "JOBS option (Aug 1996)"
            else:
                em, src = np.nan, ""
            r["work_exempt_m"] = round(em, 2) if em == em else np.nan
            r["work_exempt_src"] = src
            r["tanf_exempt_text"] = wi.tanf_exempt_text
            r["tanf_exempt_12m_lifetime"] = wi.tanf_exempt_12m_lifetime
            r["tanf_tl"] = wi.tanf_tl
            r["tanf_tl_months"] = wi.tanf_tl_months
            r["tanf_tl_type"] = wi.tanf_tl_type
            rows.append(r)
    cal = pd.DataFrame(rows).merge(u, on=["state", "year"], how="left")
    assert cal.state_fips.notna().all() and len(cal) == 51 * len(YEARS)
    lead = ["state", "state_fips", "year"]
    cal = cal[lead + [c for c in cal.columns if c not in lead]]
    cal.to_csv(DATA / "policy_calendar.csv", index=False)
    print(f"policy_calendar.csv: {cal.shape}")
    show = cal[cal.year.isin([1992, 1994, 1996, 1998])].pivot_table(
        index="state", columns="year", values=["waiver_any_jul1", "tanf_jul1", "work_exempt_m"])
    pd.set_option("display.width", 220)
    print(show.head(12).to_string())
    print(cal.groupby("year")[["fmla_federal", "state_mat_leave_jul1", "pfl_jul1", "waiver_any_jul1", "tanf_jul1",
                               "time_limit_jul1"]].sum().loc[[1988, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 2005, 2015, 2024]])
    print(w[["waiver_any_date", "tanf_date", "afdc_exempt_m", "afdc_exempt_date", "tanf_exempt_m", "tanf_exempt_date",
             "tanf_tl_months", "tanf_tl_type"]].to_string())


if __name__ == "__main__":
    main()
