"""Paper A model: coded borrowing wedge (PI-approved Fable decision 5.3, 2026-10-18). Not estimated.

Borrowing rate = saving rate + wedge on negative liquid assets. The wedge is the average real interest rate on credit
card plans (Federal Reserve G.19, commercial bank interest rate on credit card plans, all accounts: FRED series
TERMCBCCALLNS, quarterly from 1994Q4; accounts assessed interest: TERMCBCCINTNS) minus 12-month CPI-U inflation
(FRED CPIAUCSL) in the same month, averaged over 1995-2021 (the PSID / CPS target years after the series starts),
minus the model's real saving rate (3% a year, params.FIXED_DEFAULTS r_m). Public data, no API key.
Liquid wealth in the targets nets unsecured debt (credit cards, student, medical and other loans) against liquid
assets (ReducedForm/62.PoorMarriedCouples.py: low liquid wealth is mostly debt, 82% of low person-years with liquid
wealth below zero); the credit-card rate is the marginal rate on that debt.
Run: .venv/Scripts/python.exe -I IGE/paperA_model/borrowing_wedge.py [<folder with the three FRED csv files>]
(without a folder the csv files are downloaded from fred.stlouisfed.org/graph/fredgraph.csv?id=<series> into a new
temporary folder). Writes inputs/borrowing_wedge.json.
"""
import csv
import json
import sys
import tempfile
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
SERIES = ("TERMCBCCALLNS", "TERMCBCCINTNS", "CPIAUCSL")
Y0, Y1 = 1995, 2021
R_SAVE = 0.03


def read(path):
    out = {}
    with open(path, newline="") as f:
        rd = csv.reader(f)
        next(rd)
        for row in rd:
            if len(row) == 2 and row[1] not in ("", "."):
                try:
                    out[row[0][:7]] = float(row[1])
                except ValueError:
                    pass
    return out


def main(folder=None):
    if folder is None:
        folder = Path(tempfile.mkdtemp(prefix="fred_"))
        for s in SERIES:
            urllib.request.urlretrieve(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={s}", folder / f"{s}.csv")
    folder = Path(folder)
    cc_all, cc_int, cpi = (read(folder / f"{s}.csv") for s in SERIES)

    def real_avg(cc, y0, y1):
        vals = []
        for ym, r in cc.items():
            y, m = int(ym[:4]), ym[5:7]
            prev = f"{y - 1}-{m}"
            if y0 <= y <= y1 and ym in cpi and prev in cpi:
                infl = cpi[ym] / cpi[prev] - 1
                vals.append((r / 100 - infl, r / 100, infl))
        n = len(vals)
        return (sum(v[0] for v in vals) / n, sum(v[1] for v in vals) / n, sum(v[2] for v in vals) / n, n)

    real, nom, infl, n = real_avg(cc_all, Y0, Y1)
    real_i, nom_i, _, _ = real_avg(cc_int, Y0, Y1)
    real_e2, nom_e2, _, n_e2 = real_avg(cc_all, 1997, 2008)
    wedge_a = real - R_SAVE
    wedge_m = (1 + R_SAVE + wedge_a) ** (1 / 12) - (1 + R_SAVE) ** (1 / 12)
    out = dict(
        wedge_monthly=wedge_m, wedge_annual=wedge_a, real_cc_rate_annual=real, nominal_cc_rate_annual=nom,
        cpi_inflation_annual=infl, quarters=n, years=[Y0, Y1], saving_rate_annual=R_SAVE,
        check_accounts_assessed_interest=dict(real=real_i, nominal=nom_i),
        check_1997_2008=dict(real=real_e2, nominal=nom_e2, quarters=n_e2),
        source="Federal Reserve G.19 via FRED: TERMCBCCALLNS (all accounts), TERMCBCCINTNS (accounts assessed "
               "interest), CPIAUCSL; real = nominal - 12-month CPI-U inflation, average over the quarters of the "
               "years; wedge = real credit-card rate - 3% real saving rate; monthly wedge = (1 + r_b)^(1/12) - "
               "(1 + r_s)^(1/12)",
        status="coded calibrated input (not estimated)")
    (HERE / "inputs" / "borrowing_wedge.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
