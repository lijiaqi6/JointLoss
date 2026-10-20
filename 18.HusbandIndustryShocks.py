r"""Husband-specific industry shocks at a birth and the wife's work around it (2026-10-17).

Question: does a labor-market shock to the HUSBAND's own industry in the year of a birth move the WIFE's work after
the birth (the cross-spouse insurance margin), does it differ by race, and is it weaker where the safety net is more
generous? State-level shocks were weak (8.FirstStage.py), so the shock is built from the husband's own sector.

PSID (main)
  births     data/first_stage_births.pkl (8.FirstStage.py, read only): PSID Childbirth and Adoption History births
             1977-2021 to SRC/SEO mothers, White/Black head, state, controls, mother's employment b-1..b+3.
             Kept: married at the birth (CAH8 = 1) and the mother is wife / partner of the head in the latest family-
             file wave in [b-3, b-1]; the head of that family = the husband. Birth years 1980-2019 (CPS MORG).
  industry   husband's (head's) main industry in that wave, by label in each family-file .do file:
               1976-80  'INDUSTRY OF HEAD yy' (_A variables: PSID retrospective 3-digit 1970 Census codes)
               1981-92  'MAIN IND:3 DIGT(H-E)'; 1993-2001 'B10 MAIN INDUSTRY: 3 DIGIT (HD-E)' (1970 codes; employed
                        heads); if missing, 'IND-LAST JOB (HD-U)' / 'C11 INDUSTRY-LAST JOB (HD-U)' (unemployed heads)
               2003-15  'BC21 MAIN IND FOR JOB 1: 2000 CODE' (3-digit 2000 Census codes, x10 = CPS 4-digit codes)
               2017-23  'BC21 MAIN IND FOR JOB 1: 2012 CODE' (4-digit). Job 1 = current or most recent main job.
             The wife's industry likewise ('INDUSTRY OF WIFE yy', 'F10/F11 INDUSTRY (WF-E)', 'MAIN IND:3 DIGT(W-E)',
             'D10 MAIN INDUSTRY:3 DIGIT (WF-E)', 'DE21 MAIN IND FOR JOB 1'). Codes -> the 16 sectors of
             8a.StateShocks.py (SECTORS, imported).
  hours      head / wife total annual hours (wave w reports w-1) + the 'WTR EMPLOYED IN w-2' items from 2003
             (same as 8.FirstStage.py); labor income = psid_person_year.pkl `earn` (2000 dollars).
  wealth     liquid assets = 'IMP VAL CHECKING/SAVING' (+ 'IMP VAL CD/BONDS/TB' from 2019) of the mother's family in
             the latest wealth wave in [b-5, b] (wealth files 1984, 1989, 1994, 1999-2007; family files 2009+).
Shocks (CPS MORG 1979-2019, Dropbox/MORG, read only; sector codes as in 8a.StateShocks.py)
  g_nat   growth (log points x 100) of national employment of MEN in the husband's sector, leaving out the state of
          residence, in the birth year. 1982->83 crosses the 1970->1980 code change: set missing.
  ur_nat  unemployment rate of men whose current / last job is in the sector, national leave-one-state-out.
  g_st    growth of men's employment in the husband's sector in his state (cells >= 20 employed men in both years;
          winsorized 1/99). Split-sample version: odd vs even interview months (independent CPS samples); the
          odd-month shock instrumented by the even-month shock removes the attenuation from CPS sampling noise.
  *_dt    relative to the pre-birth trend: value in b minus the mean over b-3..b-1 (at least two years).
Specification: OLS, state FE + birth-year FE + husband-sector FE, controls: mother's age, age^2, education
  (<12, 13-15, 16+, missing), birth order (2, 3+, missing), Black. Clusters: state x sector, and sector (16; wild
  cluster bootstrap-t p-value, Webb weights, null imposed, 999 draws).
Crowd-out: shock x AFDC/TANF maximum benefit for a family of three (and AFDC + food stamps), data/
  policy_calendar.csv (UKCPR), in hundreds of 2000 dollars per month, centred; UI generosity from
  data/ui_generosity.csv when that file exists.
Placebos: shock in b-2; women's employment growth in the WIFE's own pre-birth sector; childless married women.

NLSY79 (complement; the public file has no state and the spouse questions give occupation only, no industry):
  married mothers, births 1980-1993; husband's weeks worked in the calendar year before the birth and in the birth
  year (Q2-15A); event = husband attached (>= 48 weeks in b-1) and < 40 weeks in the birth year. Mother's share of
  weeks employed by quarter around the birth from the weekly array (NLSY79/data/women79.pkl, read only).

Writes output/husband_shocks.csv (every coefficient), output/husband_shocks.md, data/husband_shocks_births.pkl,
data/husband_sector_shocks.pkl, data/husband_shocks_fam.pkl, data/husband_shocks_morg.pkl.
"""
import importlib.util
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from common import CPI, DATA, OUT, stars, to2000
import os
NLSY79_DIR = Path(os.environ.get("NLSY79_DIR", r"G:\My Drive\Selection vs risk\NLSY79"))   # Selection-vs-risk/NLSY79 (helpers + extracts), read only

HERE = Path(__file__).resolve().parent


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


SS = _load("state_shocks_8a", HERE / "8a.StateShocks.py")          # SECTORS, sector_of, CENSUS2FIPS, FIPS, MORG
FS = _load("first_stage_8", HERE / "8.FirstStage.py")               # HOURS, STATE, PSID2FIPS, ODD, cah, education
SNAMES = SS.SNAMES
FAM = FS.FAM
WAVES = [w for w in FS.WAVES if w >= 1976]
INFIX = re.compile(r"(?:long\s+)?([A-Z]+\d+[A-Z0-9_]*)\s+(\d+)\s*-\s*(\d+)")      # _A / _B suffixes allowed
LABEL = re.compile(r'label variable\s+(\S+)\s+"(.*)"')
IND_PAT = {
    "h_ind": [r"^INDUSTRY\s+OF HEAD\s+\d\d$", r"MAIN IND:\s*3 DIGT\s*\(H-E\)", r"MAIN INDUSTRY:\s*3 DIGIT\s*\(HD-E\)",
              r"^BC21 MAIN IND FOR JOB 1"],
    "h_indu": [r"IND(USTRY)?-LAST JOB\s*\((HD|H)-U\)"],
    "w_ind": [r"^INDUSTRY\s+OF WIFE\s+\d\d$", r"^F1[01] INDUSTRY\s*\(WF-E\)", r"MAIN IND:\s*3 DIGT\s*\(W-E\)",
              r"MAIN INDUSTRY:\s*3 DIGIT\s*\(WF-E\)", r"^DE21 MAIN IND FOR JOB 1"],
}
WEALTH_WAVES = [1984, 1989, 1994, 1999, 2001, 2003, 2005, 2007] + list(range(2009, 2022, 2))   # births <= 2019
B_YEARS = (1980, 2019)
SEED, NBOOT = 20261017, 999
WEBB = np.array([-np.sqrt(1.5), -1, -np.sqrt(0.5), np.sqrt(0.5), 1, np.sqrt(1.5)])


def layout(do):
    t = do.read_text(encoding="latin-1")
    block = re.search(r"\binfix\b(.*?)\busing\b", t, re.S).group(1)
    pos = {v: (int(a) - 1, int(b)) for v, a, b in INFIX.findall(block)}
    return pos, [(v, l.strip()) for v, l in LABEL.findall(t)]


def read(txt, cols, pos):
    return pd.read_fwf(txt, colspecs=[pos[c] for c in cols], names=cols, header=None, encoding="latin-1")


def find(labs, pats, w):
    for p in pats:
        for v, l in labs:
            if re.search(p, l):
                if p.startswith(r"IND(USTRY)?-LAST") and not (1981 <= w <= 2001):
                    return None                                 # 1979-80: 2-digit PSID codes, not used
                return v, l
    return None


# ---------------------------------------------------------------- PSID family files
def family():
    fn = DATA / "husband_shocks_fam.pkl"
    if fn.exists():
        return pd.read_pickle(fn)
    out, found = [], []
    for w in WAVES:
        folder = FAM / (f"fam{w}" if w < 1994 else f"fam{w}er")
        do = next(f for f in folder.glob("*.do") if "formats" not in f.name)
        pos, labs = layout(do)
        idv = labs[1][0]
        sel = {k: find(labs, p, w) for k, p in IND_PAT.items()}
        odd = {}
        for v, l in labs:
            m = FS.ODD.match(l)
            if m and int(m.group(2)) == w - 2:
                who = "h" if m.group(3) in ("HD", "RP") else "w"
                kind = {"WTR EMPLOYED IN": "emp", "WEEKS EMPLOYED IN": "wks"}.get(m.group(1), "hpw")
                odd[f"{who}_{kind}"] = v
        ren = {idv: "int", FS.HOURS[w][0]: "hh", FS.HOURS[w][1]: "wh", FS.STATE[w]: "pstate",
               **{v[0]: k for k, v in sel.items() if v}, **{v: k for k, v in odd.items()}}
        f = read(do.with_suffix(".txt"), list(ren), pos).rename(columns=ren)
        f["wave"] = w
        for k in IND_PAT:
            if k not in f:
                f[k] = np.nan
        out.append(f)
        found.append(dict(wave=w, **{k: (f"{v[0]} '{v[1]}'" if v else "") for k, v in sel.items()}))
        print(f"  family {w}: {len(f)} families; " + "; ".join(f"{k}={v[0] if v else '-'}" for k, v in sel.items()),
              flush=True)
    F = pd.concat(out, ignore_index=True)
    for c in ("hh", "wh"):
        F[c] = F[c].where(F[c].between(0, 6000))
    F["fips"] = F["pstate"].map(FS.PSID2FIPS)
    for who in ("h", "w"):
        code = F[f"{who}_ind"]
        if who == "h":                                          # unemployed heads: industry of the last job
            code = code.where(code > 0, F["h_indu"])
        F[f"{who}_code"] = code
        F[f"{who}_sec"] = industry_sector(code, F["wave"])
    F.attrs["found"] = found
    F.to_pickle(fn)
    pd.DataFrame(found).to_csv(DATA / "husband_shocks_industry_vars.csv", index=False)
    return F


def industry_sector(code, wave):
    """PSID industry codes -> 16 sectors. 1970 Census codes to 2001, 3-digit 2000 codes 2003-15 (x10 = CPS 4-digit),
    4-digit 2012 codes from 2017."""
    out = pd.Series(np.nan, index=code.index)
    m70 = (wave <= 2001) & code.between(1, 998)
    m00 = wave.between(2003, 2015) & code.between(1, 998)
    m12 = (wave >= 2017) & code.between(1, 9998)
    out[m70] = SS.sector_of(code[m70], 70)
    out[m00] = SS.sector_of(code[m00] * 10, 2)
    out[m12] = SS.sector_of(code[m12], 2)
    return out


def wealth():
    rows = []
    for w in WEALTH_WAVES:
        if w <= 2007:
            do = FAM / f"wlth{w}" / f"WLTH{w}.do"
        else:
            do = next(f for f in (FAM / f"fam{w}er").glob("*.do") if "formats" not in f.name)
        pos, labs = layout(do)
        idv = labs[1][0]
        liq = [v for v, l in labs if re.match(r"IMP VAL (CHECKING/SAVING|CD/BONDS/TB)", l)]
        wl2 = [v for v, l in labs if re.match(r"IMP WEALTH W/ EQUITY", l)][:1]
        d = read(do.with_suffix(".txt"), [idv] + liq + wl2, pos)
        rows.append(pd.DataFrame({"wave": w, "int": d[idv], "liquid": to2000(d[liq].sum(axis=1), w),
                                  "wealth2": to2000(d[wl2[0]], w)}))
    return pd.concat(rows, ignore_index=True)


def panel(py, F):
    """person x calendar year for heads and wives: annual hours, employed (>0), 500+ hours, labor income."""
    p = py[py["head"] | py["wife"]][["pid", "wave", "int", "head", "earn"]].merge(
        F[["wave", "int", "hh", "wh", "h_emp", "h_wks", "h_hpw", "w_emp", "w_wks", "w_hpw"]], on=["wave", "int"],
        how="inner")
    a = pd.DataFrame({"pid": p["pid"], "year": p["wave"] - 1, "hours": np.where(p["head"], p["hh"], p["wh"]),
                      "earn": p["earn"]})
    o = p[p["wave"] >= 2003]
    eh, hh = FS.odd_hours(o["h_emp"], o["h_wks"], o["h_hpw"])
    ew, hw = FS.odd_hours(o["w_emp"], o["w_wks"], o["w_hpw"])
    b = pd.DataFrame({"pid": o["pid"].values, "year": o["wave"].values - 2,
                      "hours": np.where(o["head"], hh, hw), "emp_odd": np.where(o["head"], eh, ew)})
    P = pd.concat([a, b], ignore_index=True)
    P["emp"] = (P["hours"] > 0).astype(float).where(P["hours"].notna())
    P["emp"] = P["emp"].fillna(P.get("emp_odd"))
    P["emp500"] = (P["hours"] >= 500).astype(float).where(P["hours"].notna())
    P = P.dropna(subset=["emp"]).sort_values(["pid", "year"]).drop_duplicates(["pid", "year"])
    return P.set_index(["pid", "year"])[["hours", "emp", "emp500", "earn"]]


def at(P, pid, year, col):
    idx = pd.MultiIndex.from_arrays([pid, year])
    return pd.Series(P[col].reindex(idx).values, index=pid.index)


def spouse_links(py, F):
    """one row per (wave, wife): wife pid, head (husband) pid, husband's and wife's sectors, state."""
    hd = py[py["head"]][["wave", "int", "pid", "female"]].rename(columns={"pid": "hpid", "female": "hfem"})
    wf = py[py["wife"]][["wave", "int", "pid", "rel"]]
    L = wf.merge(hd, on=["wave", "int"]).merge(
        F[["wave", "int", "h_sec", "w_sec", "h_code", "w_code", "fips"]], on=["wave", "int"], how="left")
    return L[L["hfem"] == 0]


def link(keys, L, window=(-3, -1)):
    """latest wave in [t+window] where the woman is wife; husband pid, sectors from that wave (husband's sector from
    an earlier wave with the same husband if missing)."""
    cand = keys[["pid", "year"]].reset_index().merge(L, on="pid")
    cand = cand[(cand["wave"] >= cand["year"] + window[0]) & (cand["wave"] <= cand["year"] + window[1])]
    cand = cand.sort_values(["index", "wave"])
    last = cand.groupby("index").last()
    hs = cand.dropna(subset=["h_sec"]).merge(last[["hpid"]].reset_index(), on=["index", "hpid"])
    hs = hs.groupby("index").last()
    out = last[["wave", "int", "hpid", "rel", "w_sec", "fips"]].rename(columns={"wave": "link_wave",
                                                                              "fips": "fips_link"})
    out["h_sec"] = hs["h_sec"]
    out["h_sec_wave"] = hs["wave"]
    return out


# ---------------------------------------------------------------- CPS MORG shocks
def morg_cells():
    fn = DATA / "husband_shocks_morg.pkl"
    if fn.exists():
        return pd.read_pickle(fn)
    out = []
    for yy in list(range(79, 100)) + list(range(0, 20)):
        f = SS.MORG / f"morg{yy:02d}.dta"
        with pd.io.stata.StataReader(f) as r:
            have = set(r.variable_labels())
        st = "stfips" if "stfips" in have else "state"
        lf = next(v for v in ("lfsr94", "lfsr89", "esr") if v in have)
        inds = [v for v in ("ind70", "ind80", "ind02") if v in have]
        d = pd.read_stata(f, columns=[st, lf, "sex", "age", "weight", "intmonth"] + inds, convert_categoricals=False)
        year = 1900 + yy if yy >= 79 else 2000 + yy
        d["fips"] = d[st].map(SS.CENSUS2FIPS) if st == "state" else d[st]
        d = d[d["age"] >= 16]
        d["emp"] = d[lf].isin([1, 2])
        d["unemp"] = (d[lf] == 3) if lf == "esr" else d[lf].isin([3, 4])
        d = d[d["emp"] | d["unemp"]]
        d["female"] = (d["sex"] == 2).astype(int)
        d["half"] = (d["intmonth"] % 2).astype(int)
        vint = [("sec", "ind70" if year <= 1982 else "ind80" if year <= 2002 else "ind02",
                 70 if year <= 1982 else 80 if year <= 2002 else 2)]
        if year == 2002:
            vint.append(("sec02", "ind02", 2))
        for name, col, v in vint:
            x = d.assign(sec=SS.sector_of(d[col], v)).dropna(subset=["sec"])
            x["E"] = x["weight"] * x["emp"]
            x["U"] = x["weight"] * x["unemp"]
            x["nE"] = x["emp"].astype(int)
            g = x.groupby(["fips", "female", "sec", "half"])[["E", "U", "nE"]].sum().reset_index()
            g["year"] = year if name == "sec" else -2002            # -2002 = year 2002 in ind02 codes
            out.append(g)
        print(f"  MORG {year}: {len(d):,} in the labor force", flush=True)
    C = pd.concat(out, ignore_index=True)
    C.to_pickle(fn)
    return C


def detrend(s):
    """s indexed by (..., year): value minus mean of the 3 previous years (>= 2 non-missing)."""
    keys = [n for n in s.index.names if n != "year"]
    w = s.unstack("year")
    w = w.reindex(columns=range(w.columns.min(), w.columns.max() + 1))
    prev = w.T.shift(1).rolling(3, min_periods=2).mean().T
    return (w - prev).stack(future_stack=True).reorder_levels(keys + ["year"])


def build_shocks(C):
    years = sorted(y for y in C["year"].unique() if y > 0)
    full = pd.MultiIndex.from_product([years + [-2002], SS.FIPS, [0, 1], range(len(SNAMES))],
                                      names=["year", "fips", "female", "sec"])

    def grid(x, col):
        return x.groupby(["year", "fips", "female", "sec"])[col].sum().reindex(full, fill_value=0.0)

    E, U = grid(C, "E"), grid(C, "U")
    nat_E = E.groupby(["year", "female", "sec"]).transform("sum") - E          # leave own state out
    nat_U = U.groupby(["year", "female", "sec"]).transform("sum") - U

    def growth(L, minn=None, n=None):
        rows = []
        for t in years[1:]:
            if t == 1983:
                continue                                                         # 1970 -> 1980 code break
            cur = L.xs(t, level="year")
            prev = L.xs(-2002 if t == 2003 else t - 1, level="year")
            g = 100 * (np.log(cur.where(cur > 0)) - np.log(prev.where(prev > 0)))
            if minn is not None:
                ok = (n.xs(t, level="year") >= minn) & (n.xs(-2002 if t == 2003 else t - 1, level="year") >= minn)
                g = g.where(ok)
            rows.append(g.rename("g").reset_index().assign(year=t))
        return pd.concat(rows).set_index(["fips", "female", "sec", "year"])["g"]

    S = pd.DataFrame({"g_nat": growth(nat_E)})
    ur = (100 * nat_U / (nat_E + nat_U)).rename("ur")
    ur = ur[ur.index.get_level_values("year") > 0].reorder_levels(["fips", "female", "sec", "year"])
    S = S.join(ur.rename("ur_nat"), how="outer")
    nE = grid(C, "nE")
    S = S.join(growth(E, 20, nE).rename("g_st"), how="outer")
    for h in (0, 1):
        Ch = C[C["half"] == h]
        S = S.join(growth(grid(Ch, "E"), 10, grid(Ch, "nE")).rename(f"g_st_h{h}"), how="outer")
    for c in ("g_st", "g_st_h0", "g_st_h1"):
        lo, hi = S[c].quantile([0.01, 0.99])
        S[c] = S[c].clip(lo, hi)
    for c in list(S.columns):
        S[c + "_dt"] = detrend(S[c])
    S = S.reset_index()
    S = S[S["year"].between(1979, 2019)]
    return S


def attach_shocks(d, S, sec_col, female, year_col="year", offset=0, suffix="", cols=None):
    cols = cols or [c for c in S.columns if c not in ("fips", "female", "sec", "year")]
    s = S[S["female"] == female][["fips", "sec", "year"] + cols].rename(
        columns={"sec": sec_col, "year": "_y", **{c: c + suffix for c in cols}})
    s["fips"] = s["fips"].astype(float)
    s[sec_col] = s[sec_col].astype(float)
    out = d.assign(_y=d[year_col] + offset).merge(s, on=["fips", sec_col, "_y"], how="left").drop(columns="_y")
    out.index = d.index
    return out


# ---------------------------------------------------------------- regression engine
def dummies(d, fe):
    return [pd.get_dummies(d[f].astype("int64"), prefix=f, drop_first=True, dtype=float).to_numpy() for f in fe]


def basis(Z):
    Z = Z[:, Z.std(axis=0) > 0] if Z.shape[1] > 1 else Z
    Z = np.column_stack([np.ones(len(Z)), Z])
    U, s, _ = np.linalg.svd(Z, full_matrices=False)
    return U[:, s > 1e-9 * s.max()]


def resid(Q, M):
    return M - Q @ (Q.T @ M)


def cluster_vcov(Xz, X, e, g, K):
    """sandwich for (Z'X)^{-1} Z' e; OLS when Xz is X. g: cluster codes 0..G-1."""
    n, G = len(e), g.max() + 1
    A = np.linalg.inv(Xz.T @ X)
    S = np.zeros((G, X.shape[1]))
    np.add.at(S, g, Xz * e[:, None])
    c = G / (G - 1) * (n - 1) / (n - K)
    return c * A @ (S.T @ S) @ A.T, G


def wcb(x, y, g, Kfull, Q, rng):
    """wild cluster bootstrap-t (restricted, Webb weights) for the coefficient on x; x and y already residualized on
    everything else (Q spans the other regressors). Returns the p-value."""
    G = g.max() + 1
    n = len(y)
    xx = x @ x
    b = x @ y / xx
    e = y - x * b
    c = G / (G - 1) * (n - 1) / (n - Kfull)
    sc = np.zeros(G)
    np.add.at(sc, g, x * e)
    t0 = b / np.sqrt(c * (sc @ sc) / xx ** 2)
    W = WEBB[rng.integers(0, 6, size=(G, NBOOT))]
    Ys = y[:, None] * W[g]                                       # y is the restricted residual (beta = 0)
    Ys = Ys - Q @ (Q.T @ Ys)
    bs = x @ Ys / xx
    Es = Ys - x[:, None] * bs[None, :]
    Sc = np.zeros((G, NBOOT))
    np.add.at(Sc, g, x[:, None] * Es)
    ts = bs / np.sqrt(c * (Sc ** 2).sum(axis=0) / xx ** 2)
    return float(np.mean(np.abs(ts) >= np.abs(t0)))


def reg(d, y, xs, ctrl, fe, iv=None, combo=None, boot=True, cl_main="cl_ss", cl_alt="cl_sec", id_col="pid"):
    """OLS (or exactly identified 2SLS, iv = instruments for xs) of y on xs + ctrl + FE dummies. Returns rows (one
    per x, plus the linear combination `combo` = (name, [x1, x2]) if given)."""
    zs = iv or []
    use = [y, *xs, *zs, *ctrl, *fe, cl_main, cl_alt, id_col]
    d = d[list(dict.fromkeys(use))].replace([np.inf, -np.inf], np.nan).dropna()
    if len(d) < 50:
        return []
    Z0 = np.column_stack([d[ctrl].to_numpy(float)] + dummies(d, fe)) if ctrl or fe else np.zeros((len(d), 0))
    Q = basis(Z0)
    K = Q.shape[1] + len(xs)
    Y = resid(Q, d[[y]].to_numpy(float))[:, 0]
    X = resid(Q, d[xs].to_numpy(float))
    Xz = resid(Q, d[zs].to_numpy(float)) if zs else X
    beta = np.linalg.solve(Xz.T @ X, Xz.T @ Y)
    e = Y - X @ beta
    res = {}
    for cl in (cl_main, cl_alt):
        g = pd.factorize(d[cl])[0]
        V, G = cluster_vcov(Xz, X, e, g, K)
        res[cl] = (V, G)
    rng = np.random.default_rng(SEED)
    out = []
    names = list(xs)
    L = [np.eye(len(xs))[i] for i in range(len(xs))]
    if combo:
        names.append(combo[0])
        L.append(np.array([1.0 if x in combo[1] else 0.0 for x in xs]))
    for j, (nm, l) in enumerate(zip(names, L)):
        r = dict(x=nm, b=float(l @ beta), n=len(d), n_id=d[id_col].nunique(), mean_y=float(d[y].mean()),
                 sd_x=float(X[:, j].std()) if j < len(xs) else np.nan, iv=bool(zs))
        for cl, tag in ((cl_main, "ss"), (cl_alt, "sec")):
            V, G = res[cl]
            se = float(np.sqrt(l @ V @ l))
            t = r["b"] / se
            r[f"se_{tag}"], r[f"p_{tag}"], r[f"G_{tag}"] = se, float(2 * stats.t.sf(abs(t), G - 1)), G
            r[f"F_{tag}"] = t ** 2
        r["p_wcb"] = np.nan
        if boot and not zs and j < len(xs):
            others = [k for k in range(len(xs)) if k != j]
            Qj = basis(np.column_stack([Z0, d[[xs[k] for k in others]].to_numpy(float)])) if others else Q
            xj = resid(Qj, d[[xs[j]]].to_numpy(float))[:, 0]
            yj = resid(Qj, d[[y]].to_numpy(float))[:, 0]
            r["p_wcb"] = wcb(xj, yj, pd.factorize(d[cl_alt])[0], K, Qj, rng)
        out.append(r)
    if zs:                                                       # first-stage F of the instrument(s)
        g = pd.factorize(d[cl_main])[0]
        for k, z in enumerate(zs):
            fs = reg(d, xs[k], [z], ctrl, fe, boot=False, cl_main=cl_main, cl_alt=cl_alt, id_col=id_col)
            out[k]["F_iv_ss"], out[k]["F_iv_sec"] = fs[0]["F_ss"], fs[0]["F_sec"]
    return out


# ---------------------------------------------------------------- tables
def pv(p):
    return "<0.001" if p < 0.001 else f"{p:.3f}"


def cell(r, single=False):
    s = f"{r['b']:.4f}{stars(r['p_ss'])} ({r['se_ss']:.4f}; p={pv(r['p_ss'])})"
    if single:
        return s
    w = f"; WCB p={pv(r['p_wcb'])}" if r.get("p_wcb") == r.get("p_wcb") and r.get("p_wcb") is not None else ""
    pst = r["p_wcb"] if (r.get("p_wcb") == r.get("p_wcb") and r.get("p_wcb") is not None) else r["p_sec"]
    return s + f"<br><sub>sector-cl. ({r['se_sec']:.4f}; p={pv(r['p_sec'])}{w}){stars(pst)}</sub>"


def table(res, tid, cols, panels, title, fe_line, extra_rows=(), single=False, cl_label="Clusters: state x sector / sector"):
    L = [f"### {title}", "", "| | " + " | ".join(c for c, _ in cols) + " |", "|---|" + "---|" * len(cols)]
    for pname, xl in panels:
        L.append(f"| **{pname}** |" + " |" * len(cols))
        for x, lab in xl:
            row = [lab]
            for c, _ in cols:
                rr = [r for r in res.get((tid, pname, c), []) if r["x"] == x]
                row.append(cell(rr[0], single) if rr else "")
            L.append("| " + " | ".join(row) + " |")
        for lab, key, f in (("N", "n", "{:,}"), ("Mothers / women", "n_id", "{:,}"),
                            (cl_label, None, None), ("Mean outcome", "mean_y", "{:.3f}"),
                            *extra_rows):
            row = [lab]
            for c, _ in cols:
                rr = res.get((tid, pname, c), [])
                if not rr:
                    row.append("")
                elif key is None:
                    row.append(f"{rr[0]['G_ss']:,}" if single else f"{rr[0]['G_ss']:,} / {rr[0]['G_sec']}")
                elif key in rr[0] and rr[0][key] == rr[0][key]:
                    row.append(f.format(rr[0][key]))
                else:
                    row.append("")
            L.append("| " + " | ".join(row) + " |")
    L += [f"| {fe_line} | " + " | ".join("yes" for _ in cols) + " |", ""]
    return L


# ---------------------------------------------------------------- NLSY79
def nlsy79(results, rows):
    NC = _load("nlsy_common", NLSY79_DIR / "common.py")
    d = NC.load()
    W = NC.weekly(d)
    E = NC.employed_matrix(W)
    nW = E.shape[1]
    B = NC.births(d)
    mar = NC.marriages(d)
    recs = []
    for i in range(len(d)):
        for j in range(B.shape[1]):
            b = B[i, j]
            if not (b == b):
                continue
            b = int(b)
            y = int(NC.year_of_week(b))
            if not (1980 <= y <= 1993) or b - 105 < 0 or b + 117 >= nW or not NC.married_at(mar[i], b):
                continue
            ms = d.at[i, f"MARSTAT-KEY_{y + 1}"] if f"MARSTAT-KEY_{y + 1}" in d else np.nan
            hw = [d.at[i, f"Q2-15A_{t}"] if f"Q2-15A_{t}" in d else np.nan for t in (y, y + 1, y + 2)]
            hw = [x if (x == x and 0 <= x <= 52) else np.nan for x in hw]
            inc = [d.at[i, c] if c in d else np.nan for c in (f"Q13-18_TRUNC_REVISED_{y}", f"Q13-18_TRUNC_REVISED_{y + 1}")]
            inc = [NC.to2000(x, t) if (x == x and x >= 0) else np.nan for x, t in zip(inc, (y - 1, y))]
            r = dict(id=d.at[i, "id"], i=i, birth=j + 1, year=y, race=d.at[i, "race"], edu=d.at[i, "edu"],
                     age=(b - NC.week_of(d.at[i, "birth_year"], 7)) / 52.18, still_married=float(ms in (1, 5)),
                     hw_m1=hw[0], hw_0=hw[1], hw_p1=hw[2], hinc_m1=inc[0], hinc_0=inc[1])
            for q in range(-8, 9):
                seg = E[i, b + 13 * q: b + 13 * q + 13]
                r[f"q{q}"] = np.nanmean(seg) if np.isfinite(seg).sum() >= 7 else np.nan
            for nm, a, z in (("m0_12", 0, 52), ("m13_24", 52, 104), ("pre12", -52, 0)):
                seg = E[i, b + a: b + z]
                r[nm] = np.nanmean(seg) if np.isfinite(seg).sum() >= 26 else np.nan
            recs.append(r)
    N = pd.DataFrame(recs)
    N["black"] = (N["race"] == "Black").astype(float)
    N["age2"] = N["age"] ** 2 / 100
    N["ed_lhs"] = (N["edu"] == "LHS").astype(float)
    N["ed_col"] = (N["edu"] == "College").astype(float)
    N["bo2"] = (N["birth"] == 2).astype(float)
    N["bo3p"] = (N["birth"] >= 3).astype(float)
    N["pre_emp"] = N[["q-4", "q-3", "q-2"]].mean(axis=1)
    N["emp_before"] = (N["pre_emp"] >= 0.5).astype(float).where(N["pre_emp"].notna())
    N = N[(N["still_married"] == 1) & N["hw_m1"].notna() & N["hw_0"].notna()]
    flow = [("married mothers, births 1980-93, still married at the next interview, husband's weeks in b-1 and b",
             len(N))]
    A = N[N["hw_m1"] >= 48].copy()
    flow.append(("  husband attached (>= 48 weeks in b-1)", len(A)))
    A["event"] = (A["hw_0"] < 40).astype(float)
    A["event_p1"] = (A["hw_p1"] < 40).astype(float).where(A["hw_p1"].notna())
    A["weeks_lost"] = 52 - A["hw_0"]
    A["dhinc"] = A["hinc_0"] - A["hinc_m1"]
    A["cl"] = A["id"]
    A["cl2"] = A["id"]
    A["event_x_black"] = A["event"] * A["black"]
    flow.append(("  ... with event (< 40 weeks in the birth year)", int(A["event"].sum())))
    flow.append(("  ... mother employed before (>= half the weeks in quarters -4..-2)", int((A["emp_before"] == 1).sum())))
    flow.append(("  ... event and employed before", int(((A["emp_before"] == 1) & (A["event"] == 1)).sum())))
    ctrl = ["age", "age2", "black", "ed_lhs", "ed_col", "bo2", "bo3p"]
    cols = [("Husband wage income b - b-1 (2000 $)", "dhinc"), ("Share of weeks employed, months -12..-1", "pre12"),
            ("Share of weeks employed, months 0-12", "m0_12"), ("Share of weeks employed, months 13-24", "m13_24")]
    panels = [("A. All married mothers (husband attached)", None, ["event"]),
              ("B. Mother employed before the birth", 1, ["event"]),
              ("C. Mother not employed before the birth", 0, ["event"]),
              ("D. Weeks the husband did not work in the birth year (continuous)", None, ["weeks_lost"]),
              ("E. Event x Black (all married mothers)", None, ["event", "event_x_black"])]
    for pname, eb, xs in panels:
        s = A if eb is None else A[A["emp_before"] == eb]
        for c, y in cols:
            combo = ("event + event x black", xs) if len(xs) == 2 else None
            r = reg(s, y, xs, ctrl, ["year"], combo=combo, boot=False, cl_main="cl", cl_alt="cl2", id_col="id")
            results[("nlsy", pname, c)] = r
            for x in r:
                rows.append(dict(table="nlsy", panel=pname, column=c, outcome=y, **x))
    # event study by quarter
    es = []
    for samp, s in (("all", A), ("employed before", A[A["emp_before"] == 1]), ("Black", A[A["black"] == 1]),
                    ("White", A[A["black"] == 0])):
        for q in range(-8, 9):
            ctrl_q = [c for c in ctrl if not (samp in ("Black", "White") and c == "black")]
            r = reg(s, f"q{q}", ["event"], ctrl_q, ["year"], boot=False, cl_main="cl", cl_alt="cl2", id_col="id")
            if r:
                es.append(dict(sample=samp, quarter=q, **r[0]))
                rows.append(dict(table="nlsy_event_study", panel=samp, column=f"q{q}", outcome=f"q{q}", **r[0]))
    return A, flow, cols, panels, pd.DataFrame(es)


# ---------------------------------------------------------------- main
def main():
    print("PSID ...", flush=True)
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    F = family()
    P = panel(py, F)
    L = spouse_links(py, F)
    print("MORG ...", flush=True)
    S = build_shocks(morg_cells())
    S.to_pickle(DATA / "husband_sector_shocks.pkl")

    # ---- births
    b0 = pd.read_pickle(DATA / "first_stage_births.pkl")
    flow = [("births 1977-2021, White/Black head, mother 15-49, state observed (first_stage_births.pkl)", len(b0))]
    b = b0[b0["married"] == 1].copy()
    flow.append(("  married at the birth", len(b)))
    b = b[b["year"].between(*B_YEARS)]
    flow.append((f"  birth years {B_YEARS[0]}-{B_YEARS[1]} (CPS MORG shocks)", len(b)))
    b = b.join(link(b, L))
    b = b[b["hpid"].notna()]
    flow.append(("  mother is wife / partner of a male head in a wave in [b-3, b-1]", len(b)))
    b = b[b["h_sec"].notna()]
    flow.append(("  husband's industry observed and mapped to a sector", len(b)))
    b["hpid"] = b["hpid"].astype("int64")
    # husband's outcomes
    for nm, off in (("m2", -2), ("m1", -1), ("0", 0), ("p1", 1), ("p2", 2)):
        for c in ("hours", "emp", "earn"):
            b[f"h_{c}_{nm}"] = at(P, b["hpid"], b["year"] + off, c)
        for c in ("hours", "emp", "emp500"):
            b[f"w_{c}_{nm}"] = at(P, b["pid"], b["year"] + off, c)
    b["h_hours_pre"] = b["h_hours_m1"].fillna(b["h_hours_m2"])
    b["h_earn_pre"] = b["h_earn_m1"].fillna(b["h_earn_m2"])
    b["h_dhours_0"] = b["h_hours_0"] - b["h_hours_pre"]
    b["h_dhours_p1"] = b["h_hours_p1"] - b["h_hours_pre"]
    b["h_loss_0"] = ((b["h_hours_0"] < 0.75 * b["h_hours_pre"])).astype(float).where(
        b["h_hours_0"].notna() & (b["h_hours_pre"] > 0))
    b["h_loss_p1"] = ((b["h_hours_p1"] < 0.75 * b["h_hours_pre"])).astype(float).where(
        b["h_hours_p1"].notna() & (b["h_hours_pre"] > 0))
    b["h_dlearn_0"] = np.log(b["h_earn_0"].where(b["h_earn_0"] > 0)) - np.log(b["h_earn_pre"].where(b["h_earn_pre"] > 0))
    b["h_dlearn_p1"] = (np.log(b["h_earn_p1"].where(b["h_earn_p1"] > 0))
                        - np.log(b["h_earn_pre"].where(b["h_earn_pre"] > 0)))
    both = b["w_emp_p1"].notna() & b["emp_p1"].notna()
    agree = (b.loc[both, "w_emp_p1"] == b.loc[both, "emp_p1"]).mean()
    # shocks: husband's sector (men), wife's sector (women), lag 2
    b = attach_shocks(b, S, "h_sec", 0)
    b = attach_shocks(b, S, "h_sec", 0, offset=-2, suffix="_l2", cols=["g_nat_dt", "ur_nat_dt", "g_nat"])
    b = attach_shocks(b, S, "w_sec", 1, suffix="_wf", cols=["g_nat_dt", "ur_nat_dt"])
    b["cl_ss"] = b["fips"] * 100 + b["h_sec"]
    b["cl_sec"] = b["h_sec"]
    # wealth
    Wl = wealth()
    pyw = py[["pid", "wave", "int"]].merge(Wl, on=["wave", "int"])
    cand = b[["pid", "year"]].reset_index().merge(pyw, on="pid")
    cand = cand[(cand["wave"] >= cand["year"] - 5) & (cand["wave"] <= cand["year"])].sort_values(["index", "wave"])
    wl = cand.groupby("index").last()
    b["liquid"], b["wealth2"] = wl["liquid"], wl["wealth2"]
    # policy
    pol = pd.read_csv(DATA / "policy_calendar.csv", usecols=["state_fips", "year", "afdc_max3", "afdc_fs_max3"])
    pol = pol.rename(columns={"state_fips": "fips", "year": "_y"})
    pol = pol[pol["_y"] <= max(CPI)]
    pol["fips"] = pol["fips"].astype(float)
    for c in ("afdc_max3", "afdc_fs_max3"):
        pol[c] = [to2000(v, y) / 100 if v == v else np.nan for v, y in zip(pol[c], pol["_y"])]
    b = b.assign(_y=b["year"]).merge(pol, on=["fips", "_y"], how="left").drop(columns="_y").set_index(b.index)
    ui_file = DATA / "ui_generosity.csv"
    ui_cols = []
    if ui_file.exists():
        ui = pd.read_csv(ui_file)
        key_f = next(c for c in ui.columns if c.lower() in ("fips", "state_fips", "statefip"))
        ui_cols = [c for c in ui.columns if re.search(r"(max.*(wba|weekly|benefit))|replace", c, re.I)][:2]
        ui = ui[[key_f, "year"] + ui_cols].rename(columns={key_f: "fips", "year": "_y"})
        ui["fips"] = ui["fips"].astype(float)
        b = b.assign(_y=b["year"]).merge(ui, on=["fips", "_y"], how="left").drop(columns="_y").set_index(b.index)
    b.to_pickle(DATA / "husband_shocks_births.pkl")

    M = b[b["emp_m1"] == 1].copy()
    N0 = b[b["emp_m1"] == 0].copy()
    flow.append(("  mother employed in b-1 (main sample)", len(M)))
    flow.append(("  ... with the national sector shock (g_nat_dt)", int(M["g_nat_dt"].notna().sum())))
    flow.append(("  mother not employed in b-1", len(N0)))
    flow.append(("  mother's employment in b-1 not observed", int(b["emp_m1"].isna().sum())))

    CTRL = ["age", "age2", "ed_lt12", "ed_13_15", "ed_16", "ed_miss", "bo2", "bo3p", "bo_miss", "black"]
    FE = ["fips", "year", "h_sec"]
    res, rows = {}, []

    def run(tid, pname, col, d, y, xs, ctrl=CTRL, fe=FE, **kw):
        r = reg(d, y, xs, ctrl, fe, **kw)
        res[(tid, pname, col)] = r
        for x in r:
            rows.append(dict(table=tid, panel=pname, column=col, outcome=y, **x))

    SHOCKS = [("A. National sector employment growth, men, leave-one-state-out, relative to pre-birth trend",
               ["g_nat_dt"], None),
              ("B. National sector employment growth, men, leave-one-state-out, raw", ["g_nat"], None),
              ("C. National sector unemployment rate, men, leave-one-state-out, relative to pre-birth trend",
               ["ur_nat_dt"], None),
              ("D. State x sector employment growth, men, relative to trend (full CPS sample)", ["g_st_dt"], None),
              ("E. State x sector growth, split sample: odd-month shock instrumented by even-month shock (2SLS)",
               ["g_st_h1_dt"], ["g_st_h0_dt"])]
    h_cols = [("Husband hours b - pre", "h_dhours_0"), ("Husband hours b+1 - pre", "h_dhours_p1"),
              ("Husband hours fell >= 25% in b", "h_loss_0"), ("Husband hours fell >= 25% in b+1", "h_loss_p1"),
              ("Husband log earnings b - pre", "h_dlearn_0"), ("Husband employed in b", "h_emp_0")]
    w_cols = [("Wife employed b+1", "w_emp_p1"), ("Wife employed b+2", "w_emp_p2"),
              ("Wife 500+ hours b+1", "w_emp500_p1"), ("Wife 500+ hours b+2", "w_emp500_p2"),
              ("Wife hours b+1", "w_hours_p1"), ("Wife hours b+2", "w_hours_p2")]
    print("regressions ...", flush=True)
    for pname, xs, iv in SHOCKS:
        for c, y in h_cols:
            run("first", pname, c, M, y, xs, iv=iv)
        for c, y in w_cols:
            run("main", pname, c, M, y, xs, iv=iv)
            run("notemp", pname, c, N0, y, xs, iv=iv)

    # heterogeneity
    M["low_liq"] = (M["liquid"] < M["liquid"].median()).astype(float).where(M["liquid"].notna())
    b["emp_before"] = b["emp_m1"]
    het = []
    for sh, lab in (("g_nat_dt", "national growth (A)"), ("ur_nat_dt", "national unemployment rate (C)")):
        for g, glab, dd, extra in (("black", "Black", M, []), ("low_liq", "low liquid assets (below median)", M,
                                                                ["low_liq"]),
                                   ("emp_before", "mother employed in b-1 (all married mothers)", b[b["emp_m1"].notna()],
                                    ["emp_before"])):
            pname = f"{sh} x {glab}"
            dd = dd.copy()
            dd[f"{sh}_x_{g}"] = dd[sh] * dd[g]
            het.append((pname, [(sh, f"{lab}"), (f"{sh}_x_{g}", f"{lab} x {glab}"),
                                (f"{sh} + x", f"{lab}: total for {glab} = 1")]))
            for c, y in h_cols[:3] + w_cols:
                run("het", pname, c, dd, y, [sh, f"{sh}_x_{g}"], ctrl=CTRL + extra,
                    combo=(f"{sh} + x", [sh, f"{sh}_x_{g}"]))

    # crowd-out
    crowd = []
    pol_vars = [("afdc_max3", "AFDC/TANF max benefit, 3 persons ($100s of 2000 $, centred)"),
                ("afdc_fs_max3", "AFDC/TANF + food stamps max, 3 persons ($100s of 2000 $, centred)")]
    pol_vars += [(c, f"UI: {c} (centred)") for c in ui_cols]
    for sh, lab in (("g_nat_dt", "national growth (A)"), ("ur_nat_dt", "national unemployment rate (C)")):
        for pvn, plab in pol_vars:
            pname = f"{sh} x {pvn}"
            dd = M.copy()
            dd[pvn + "_c"] = dd[pvn] - dd[pvn].mean()
            dd[f"{sh}_x_{pvn}"] = dd[sh] * dd[pvn + "_c"]
            crowd.append((pname, [(sh, lab), (f"{sh}_x_{pvn}", f"{lab} x {plab}")]))
            for c, y in h_cols[:1] + w_cols:
                run("crowd", pname, c, dd, y, [sh, f"{sh}_x_{pvn}"], ctrl=CTRL + [pvn + "_c"])

    # placebos
    plc = [("A. Husband's sector shock in b-2 (national growth, relative to trend)", M, ["g_nat_dt_l2"], CTRL, FE),
           ("B. Husband's sector shock in b and in b-2 jointly", M, ["g_nat_dt", "g_nat_dt_l2"], CTRL, FE),
           ("C. Husband's sector unemployment rate in b-2 (relative to trend)", M, ["ur_nat_dt_l2"], CTRL, FE)]
    Mw = M[M["w_sec"].notna()].copy()
    Mw["cl_ss"] = Mw["fips"] * 100 + Mw["w_sec"]
    Mw["cl_sec"] = Mw["w_sec"]
    plc += [("D. Wife's own pre-birth sector: national women's employment growth (wife-sector FE)", Mw,
             ["g_nat_dt_wf"], CTRL, ["fips", "year", "w_sec"]),
            ("E. Wife's own sector (women) and husband's sector (men) jointly (both sector FE; wife-sector clusters)",
             Mw, ["g_nat_dt_wf", "g_nat_dt"], CTRL, ["fips", "year", "w_sec", "h_sec"])]
    p_cols = [("Husband hours b - pre", "h_dhours_0")] + w_cols[:2] + [w_cols[4]]
    for pname, dd, xs, ctrl, fe in plc:
        for c, y in p_cols:
            run("placebo", pname, c, dd, y, xs, ctrl=ctrl, fe=fe)

    # childless married women
    C = FS.cah()
    fb = C[(C.CAH2 == 1) & (C.CAH10 > 0)].groupby("pid")["CAH15"].agg(["min", "max"])
    women = pd.DataFrame({"pid": C["pid"].unique()})
    women["first_birth"] = women["pid"].map(fb["min"])
    women = women[~women["pid"].isin(fb.index[fb["max"] >= 9000])]
    cw = pd.DataFrame([(p, t) for p in women["pid"] for t in range(B_YEARS[0], B_YEARS[1] + 1)],
                      columns=["pid", "year"]).merge(women, on="pid")
    cw = cw[cw["first_birth"].isna() | (cw["first_birth"] > cw["year"] + 2)]
    cw = cw[cw["pid"].isin(L["pid"])].reset_index(drop=True)
    pby = py.groupby("pid")["birth_year"].median()
    cw["age"] = cw["year"] - cw["pid"].map(pby)
    lo, hi = M["age"].quantile(0.02), M["age"].quantile(0.98)
    cw = cw[cw["age"].between(lo, hi)]
    cw["emp_m1"] = at(P, cw["pid"], cw["year"] - 1, "emp")
    cw = cw[cw["emp_m1"] == 1]
    cw = cw.join(link(cw, L))
    cw = cw[cw["hpid"].notna() & cw["h_sec"].notna() & cw["rel"].isin([2, 20])].copy()
    cw["hpid"] = cw["hpid"].astype("int64")
    cw["fips"] = cw["fips_link"]
    for nm, off in (("p1", 1), ("p2", 2)):
        for c in ("hours", "emp", "emp500"):
            cw[f"w_{c}_{nm}"] = at(P, cw["pid"], cw["year"] + off, c)
    for nm, off in (("m2", -2), ("m1", -1), ("0", 0)):
        cw[f"h_hours_{nm}"] = at(P, cw["hpid"], cw["year"] + off, "hours")
    cw["h_dhours_0"] = cw["h_hours_0"] - cw["h_hours_m1"].fillna(cw["h_hours_m2"])
    rc = py[["pid", "wave", "hrace"]]
    cw["race"] = FS.nearest(cw, rc, "hrace", [-1, 0, -2, 1])
    cw = cw[cw["race"].isin(["White", "Black"])]
    ed, _ = FS.education()
    cw = cw.merge(ed, on="pid", how="left")
    cw["married"] = 1.0
    cw = FS.controls(cw)
    cw = attach_shocks(cw, S, "h_sec", 0, cols=["g_nat_dt", "ur_nat_dt"])
    cw["cl_ss"] = cw["fips"] * 100 + cw["h_sec"]
    cw["cl_sec"] = cw["h_sec"]
    CTRL_C = ["age", "age2", "ed_lt12", "ed_13_15", "ed_16", "ed_miss", "black"]
    cc_cols = [("Husband hours t - pre", "h_dhours_0"), ("Wife employed t+1", "w_emp_p1"),
               ("Wife employed t+2", "w_emp_p2"), ("Wife hours t+1", "w_hours_p1")]
    for pname, xs in (("F. Childless married women (no birth up to t+2), national growth (A)", ["g_nat_dt"]),
                      ("G. Childless married women, national unemployment rate (C)", ["ur_nat_dt"])):
        for c, y in cc_cols:
            run("childless", pname, c, cw, y, xs, ctrl=CTRL_C)

    # NLSY79
    print("NLSY79 ...", flush=True)
    A, nflow, ncols, npanels, es = nlsy79(res, rows)

    out = pd.DataFrame(rows)
    out.to_csv(OUT / "husband_shocks.csv", index=False)

    # ---------------------------------------------------------------- markdown
    sh_panels = [(p, [(xs[0], xs[0] + (" (2SLS)" if iv else ""))]) for p, xs, iv in SHOCKS]
    Fx = (("First-stage F (state x sector cl.)", "F_ss", "{:.2f}"), ("First-stage F (sector cl.)", "F_sec", "{:.2f}"),
          ("Split-sample IV: F of even-month shock", "F_iv_sec", "{:.2f}"))
    fe_line = "State FE, birth-year FE, husband-sector FE, mother controls"
    sd = {c: M[c].std() for c in ("g_nat_dt", "g_nat", "ur_nat_dt", "g_st_dt", "g_st_h1_dt")}
    rsd = {r["x"]: r["sd_x"] for r in res[("first", SHOCKS[0][0], h_cols[0][0])] + res[("first", SHOCKS[2][0], h_cols[0][0])]
           + res[("first", SHOCKS[1][0], h_cols[0][0])] + res[("first", SHOCKS[3][0], h_cols[0][0])]}
    Lmd = ["# Husband-specific industry shocks at a birth and the wife's work (18.HusbandIndustryShocks.py)", "",
           "PSID births 1980-2019 to married mothers; husband = head of the mother's family in the latest wave in "
           "[b-3, b-1]; his main industry in that wave mapped to 16 sectors (8a.StateShocks.py). Shock = CPS MORG "
           "(men) employment growth or unemployment rate in his sector in the birth year b, national leave-own-"
           "state-out or state x sector, relative to the pre-birth trend (value in b minus the mean over b-3..b-1). "
           "Each column is one regression (outcome in the header); regressors as rows; panels are separate "
           "regressions. OLS with state, birth-year and husband-sector FE (variation within sector over time and "
           "across states); controls: mother's age, age^2, education (<12, 13-15, 16+, missing; base 12), birth "
           "order (2, 3+, missing), Black.", "",
           "Cell: coefficient, stars, (s.e. clustered by state x sector; p-value); second line: s.e. clustered by "
           "the 16 sectors (cluster-t p with G-1 df) and the wild cluster bootstrap-t p-value (Webb weights, null "
           "imposed, 999 draws); stars on the second line use the bootstrap p. *** p<0.01, ** p<0.05, * p<0.1. "
           "The shock varies at sector x year (nationally), so the state x sector clusters ignore the common "
           "sector-year component; the sector-clustered bootstrap is the inference to rely on.", "",
           "Units and signs. Growth shocks in log points x 100 (higher = better for the husband's sector); "
           "unemployment-rate shocks in percentage points (higher = worse). The insurance channel predicts: growth "
           "shock -> husband hours +, wife employment -; unemployment shock -> husband hours -, wife employment +. "
           f"S.d. of the shocks in the main sample (raw / after the FE and controls): g_nat_dt {sd['g_nat_dt']:.2f} / "
           f"{rsd.get('g_nat_dt', np.nan):.2f}; g_nat {sd['g_nat']:.2f} / {rsd.get('g_nat', np.nan):.2f}; ur_nat_dt "
           f"{sd['ur_nat_dt']:.2f} / {rsd.get('ur_nat_dt', np.nan):.2f}; g_st_dt {sd['g_st_dt']:.2f} / "
           f"{rsd.get('g_st_dt', np.nan):.2f}.", "",
           "Husband outcomes: 'pre' = his hours (earnings) in b-1, else b-2 (calendar years 1997 and 1999 are not "
           "observed; earnings for odd years after 1997 are not observed). Wife outcomes: employed = annual hours > 0; "
           "500+ hours; annual hours (zeros kept).", ""]
    Lmd += table(res, "first", h_cols, sh_panels,
                 "Table 1. First stage: the husband's own outcomes (mothers employed in b-1)", fe_line, Fx)
    Lmd += table(res, "main", w_cols, sh_panels,
                 "Table 2. Wife's work after the birth (mothers employed in b-1)", fe_line, Fx[2:])
    Lmd += table(res, "notemp", w_cols, sh_panels,
                 "Table 3. Wife's work after the birth (mothers NOT employed in b-1)", fe_line, Fx[2:])
    Lmd += table(res, "het", h_cols[:3] + w_cols, het,
                 "Table 4. Heterogeneity (interactions; 'total' = shock + interaction)", fe_line +
                 " (+ group dummy)")
    Lmd += ["Low liquid assets: checking/savings (+ CDs/bonds from 2019) of the mother's family in the latest wealth "
            "wave in [b-5, b] below the sample median (no wealth data before 1984). The 'mother employed in b-1' "
            "panel pools employed and non-employed mothers.", ""]
    Lmd += table(res, "crowd", h_cols[:1] + w_cols, crowd,
                 "Table 5. Crowd-out: shock x safety-net generosity in the state and year of the birth", fe_line +
                 " + benefit level")
    Lmd += ([f"UI generosity: {', '.join(ui_cols)} from data/ui_generosity.csv.", ""] if ui_cols else
            ["UI generosity: data/ui_generosity.csv not present when this ran (another agent is building it) - "
             "pending.", ""])
    Lmd += table(res, "placebo", p_cols, [(p, [(x, x) for x in xs]) for p, _, xs, _, _ in plc],
                 "Table 6. Placebos (mothers employed in b-1)", "State FE, birth-year FE, sector FE, controls")
    Lmd += ["Panels D-E: mothers with an industry in the link wave; clusters state x wife's sector and wife's "
            "sector. g_nat_dt_wf = national (leave-own-state-out) growth of WOMEN's employment in the wife's sector.",
            ""]
    Lmd += table(res, "childless", cc_cols, [(p, [(x, x)]) for p, x in
                                            (("F. Childless married women (no birth up to t+2), national growth (A)",
                                              "g_nat_dt"),
                                             ("G. Childless married women, national unemployment rate (C)",
                                              "ur_nat_dt"))],
                 "Table 7. Comparison: childless married women (woman-years t, employed in t-1, husband's sector "
                 "shock in t)", "State FE, year FE, husband-sector FE, controls")
    Lmd += [f"Woman-years of CAH women with no birth up to t+2, wife (legal) of a male head in a wave in [t-3, t-1], "
            f"aged {lo:.0f}-{hi:.0f}, employed in t-1: {len(cw):,} woman-years, {cw['pid'].nunique():,} women "
            "(several years per woman; the mother clusters of the other tables are replaced by the same clusters).",
            ""]
    # NLSY79
    Lmd += ["## NLSY79 complement", "",
            "The public NLSY79 has no state, and the spouse questions give the husband's occupation (OCCSP-55I, "
            "1979-1996) but not his industry, so no sector shock can be built. Instead: the husband's own weeks "
            "worked in the calendar year before the birth and in the birth year (Q2-15A, asked 1980-1994 annually) "
            "as an event. Sample: births 1980-93 to married mothers still married at the next interview, husband "
            "worked >= 48 weeks in b-1; event = < 40 weeks in the birth year. OLS with birth-year FE; controls: age, "
            "age^2, Black, education (LHS, college), birth order; s.e. clustered by mother (both lines). The event is "
            "not exogenous (husbands' weeks can respond to the birth and to the wife's work); this is a descriptive "
            "event comparison.", ""]
    Lmd += table(res, "nlsy", ncols, [(p, [(x, x) for x in xs] + ([("event + event x black", "event: total for "
                                                                                             "Black")]
                                                                  if len(xs) == 2 else []))
                                      for p, _, xs in npanels],
                 "Table 8. NLSY79: husband's lost weeks in the birth year and the mother's weekly employment",
                 "Birth-year FE, controls", single=True, cl_label="Clusters (mothers)")
    piv = es.assign(cellv=[f"{r.b:.3f}{stars(r.p_ss)} ({r.se_ss:.3f}; p={pv(r.p_ss)})" for r in es.itertuples()]) \
        .pivot(index="quarter", columns="sample", values="cellv")
    ns = es.groupby("sample")["n"].max()
    Lmd += ["### Table 9. NLSY79 event study: share of weeks employed in quarter q (13 weeks) relative to the birth, "
            "event vs no event", "", "Rows: quarter (0 = the 13 weeks from the birth week). Columns: samples; each "
            "cell a separate regression. N (max over quarters): " + ", ".join(f"{k} {v:,}" for k, v in ns.items()),
            "", piv.to_markdown(), ""]
    Lmd += ["NLSY79 sample: " + "; ".join(f"{a}: {n:,}" for a, n in nflow), ""]
    # sample and data
    Lmd += ["## PSID sample", "", "| step | births |", "|---|---|"] + [f"| {a} | {n:,} |" for a, n in flow]
    Lmd += ["", f"Agreement of the recomputed wife employment at b+1 with first_stage_births.pkl (births observed in "
            f"both): {agree:.4f}.",
            f"Husband's sector taken from the link wave b-1 / b-2 / b-3: "
            + ", ".join(f"{k}: {v:,}" for k, v in (b["year"] - b["h_sec_wave"]).value_counts().sort_index().items())
            + ".", ""]
    sec_tab = pd.DataFrame({"husbands (all married births)": b["h_sec"].map(lambda s: SNAMES[int(s)]).value_counts(),
                            "wives employed in b-1 (own sector)": M["w_sec"].dropna().map(
                                lambda s: SNAMES[int(s)]).value_counts()}).fillna(0).astype(int)
    Lmd += ["### Sectors", "", sec_tab.to_markdown(), ""]
    by_race = M.groupby("black").agg(births=("pid", "size"), h_dhours_0=("h_dhours_0", "mean"),
                                     h_loss_0=("h_loss_0", "mean"), w_emp_p1=("w_emp_p1", "mean"),
                                     w_hours_p1=("w_hours_p1", "mean"), g_nat_dt=("g_nat_dt", "mean"),
                                     ur_nat_dt=("ur_nat_dt", "mean"), liquid=("liquid", "median"),
                                     afdc_max3=("afdc_max3", "mean"))
    Lmd += ["### Main sample by race (black = 1)", "", by_race.round(3).to_markdown(), ""]
    fv = pd.read_csv(DATA / "husband_shocks_industry_vars.csv") if (DATA / "husband_shocks_industry_vars.csv").exists() \
        else pd.DataFrame(F.attrs.get("found", []))
    Lmd += ["### PSID industry variables used (family files)", "", fv.fillna("").to_markdown(index=False), ""]
    (OUT / "husband_shocks.md").write_text("\n".join(Lmd), encoding="utf-8")
    print("\n".join(Lmd[:200]))


if __name__ == "__main__":
    main()
