r"""Shared helpers for the IGE scripts (2026-10-16).

Reference: Bolt, French, Hentall-MacCuish and O'Dea (2024), "The Intergenerational Elasticity of Earnings: Exploring
the Mechanisms" (Literature/IGE/Mediation_BFHO.pdf). Their IGE is the OLS slope of the child's log lifetime earnings
(mean annual gross earnings at 23-55, zeros included) on the log of the parents' family income measured once (child
aged 16), eq. (1); Appendix B corrects it for the error in a point-in-time measure of parental lifetime income:
    rho = rho* / RR,  RR = Cov(ln Y_pt, ln Y_lt) / Var(ln Y_pt),
with the reliability ratio RR estimated in the child generation (point-in-time vs lifetime income) and assumed equal
across generations.
"""
import os
import re
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

HERE = Path(__file__).resolve().parent
# person-level caches (never in git): JOINTLOSS_DATA points at them when they live elsewhere, e.g. the PC's
# "G:/My Drive/Selection vs risk/IGE/data" or the same folder seen through Google Drive on the Mac
DATA = Path(os.environ.get("JOINTLOSS_DATA", HERE / "data"))
OUT = HERE / "output"

# CPI-U annual averages (BLS, 1982-84 = 100); amounts in 2000 dollars
CPI = {1967: 33.4, 1968: 34.8, 1969: 36.7, 1970: 38.8, 1971: 40.5, 1972: 41.8, 1973: 44.4, 1974: 49.3, 1975: 53.8,
       1976: 56.9, 1977: 60.6, 1978: 65.2, 1979: 72.6, 1980: 82.4, 1981: 90.9, 1982: 96.5, 1983: 99.6, 1984: 103.9,
       1985: 107.6, 1986: 109.6, 1987: 113.6, 1988: 118.3, 1989: 124.0, 1990: 130.7, 1991: 136.2, 1992: 140.3,
       1993: 144.5, 1994: 148.2, 1995: 152.4, 1996: 156.9, 1997: 160.5, 1998: 163.0, 1999: 166.6, 2000: 172.2,
       2001: 177.1, 2002: 179.9, 2003: 184.0, 2004: 188.9, 2005: 195.3, 2006: 201.6, 2007: 207.3, 2008: 215.3,
       2009: 214.5, 2010: 218.1, 2011: 224.9, 2012: 229.6, 2013: 233.0, 2014: 236.7, 2015: 237.0, 2016: 240.0,
       2017: 245.1, 2018: 251.1, 2019: 255.7, 2020: 258.8, 2021: 271.0, 2022: 292.7}

# child outcomes: ages over which "lifetime" earnings / income are averaged (BFHO: 23-55)
AGE_LO, AGE_HI = 25, 55
MIN_OBS = 3                      # years observed in [AGE_LO, AGE_HI]


def to2000(x, year):
    return x * CPI[2000] / CPI[int(year)]


# ---------------------------------------------------------------- NLS codebooks
HEAD = re.compile(r"^([A-Z])(\d{5})\.(\d{2})\s+\[([^\]]+)\]\s+Survey Year:\s*(\S+)")


def nls_index(cdb):
    """One row per variable of an NLS .cdb: col (as in the csv), qname, year, title."""
    rows, cur = [], None
    with open(cdb, encoding="latin-1") as fh:
        for line in fh:
            m = HEAD.match(line)
            if m:
                cur = dict(col=f"{m.group(1)}{m.group(2)}{m.group(3)}", qname=m.group(4), year=m.group(5), title="")
                rows.append(cur)
                continue
            s = line.strip()
            if cur is not None and not cur["title"] and s and s not in ("PRIMARY VARIABLE", "SECONDARY VARIABLE"):
                cur["title"] = s
    return pd.DataFrame(rows)


def nls_pick(ix, qnames, title_has=None):
    """{survey year: column} for the first matching question name (in the order given) in each year."""
    s = ix[ix["qname"].isin(qnames)].copy()
    if title_has:
        s = s[s["title"].str.contains(title_has, na=False)]
    s["rank"] = s["qname"].map({q: i for i, q in enumerate(qnames)})
    s = s[s["year"].astype(str).str.fullmatch(r"\d{4}")].sort_values(["year", "rank"]).groupby("year").first()
    return {int(y): c for y, c in s["col"].items()}


def nls_money(x):
    """NLS amounts: -4 (valid skip: no such income) -> 0; -1/-2/-3/-5 -> NaN."""
    x = pd.to_numeric(x, errors="coerce").astype(float)
    return x.where(x >= 0, np.where(x == -4, 0.0, np.nan))


# ---------------------------------------------------------------- lifetime measures
def lifetime(long, value, by="pid", min_obs=MIN_OBS):
    """log of the mean of `value` over a person's rows (zeros kept); NaN if the mean is <= 0 or too few rows."""
    g = long.groupby(by)
    out = pd.DataFrame({"mean": g[value].mean(), "n": g[value].count(), "age_mean": g["age"].mean()})
    out = out[out["n"] >= min_obs]
    out["log"] = np.log(out["mean"].where(out["mean"] > 0))
    return out


# ---------------------------------------------------------------- regressions
def ols(df, y, x, controls=(), fe=(), cluster=None, weight=None):
    """OLS of y on x + controls + fixed-effect dummies; cluster-robust s.e. Returns (coef, se, p, n, result)."""
    cols = [y, x, *controls, *fe] + ([cluster] if cluster else []) + ([weight] if weight else [])
    d = df[cols].replace([np.inf, -np.inf], np.nan).dropna()
    X = d[[x, *controls]].astype(float)
    for f in fe:
        X = X.join(pd.get_dummies(d[f], prefix=f, drop_first=True, dtype=float))
    X = sm.add_constant(X, has_constant="add")
    mod = sm.WLS(d[y].astype(float), X, weights=d[weight]) if weight else sm.OLS(d[y].astype(float), X)
    kw = dict(cov_type="cluster", cov_kwds={"groups": pd.factorize(d[cluster])[0]}) if cluster else dict(cov_type="HC1")
    r = mod.fit(**kw)
    return r.params[x], r.bse[x], r.pvalues[x], int(r.nobs), r


def corrected(rho, se_rho, rr, se_rr):
    """BFHO Appendix B: rho = rho* / RR, delta-method s.e. (the two estimates treated as independent)."""
    c = rho / rr
    se = np.sqrt((se_rho / rr) ** 2 + (rho * se_rr / rr ** 2) ** 2)
    return c, se


def stars(p):
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""


def fmt(b, se, p):
    pv = "<0.001" if p < 0.001 else f"{p:.3f}"
    return f"{b:.3f}{stars(p)} ({se:.3f}; p={pv})"
