r"""Why is the Black IGE about half the White IGE? Human capital (wage) transmission vs labor-market shocks (2026-10-17).

PSID (SRC + SEO), fathers -> sons (main) and fathers -> daughters (secondary), Black vs White (race of the parental
household head when the child is 16, as in 6.IGEMain.py). Accounting decompositions, not causal estimates.

DATA (raw PSID read only; data/psid_person_year.pkl and psid_displacement.pkl read only)
  Person-year panel of heads and wives: own labor earnings (hlab / wlab, 2000 dollars, 1.PSID.py), total annual hours
  of the income year from the family files (head HH / wife WH lists of 9.ChildExposure.py; 0-5,840, 9999 = NA), the
  head's hours unemployed (family files 1968-1993 = income years 1967-1992, HU list of 9.ChildExposure.py), whether
  the head was unemployed at any time in the income year (B72 'WTR UNEMPLOYED (HD-E)' waves 1994-2001, BC8 'WTR
  UNEMPLOYED (HD/RP)' waves 2003-2023; 1 = yes), the individual-file employment status at the interview (waves
  1979-2023: 2 = temporarily laid off, 3 = looking for work / unemployed), years of completed education (max over
  waves, 1-17; 9.ChildExposure.py rule) and the father's displacement file of 19.FatherDisplacement.py (male heads:
  plant closure / layoff / firing dated to the calendar year).
  Income year t = wave - 1. A year is VALID for the price / quantity split if earnings are within the 6.IGEMain.py
  bounds ($100-$150,000 in 1967 dollars), annual hours >= 100, and the hourly wage = earnings / hours is within
  $2-$200 (2000 dollars). Then ln earnings = ln wage + ln hours exactly.
  Shock flags of a head-year t (sons and fathers alike; male heads):
    displaced   main displacement (closure or layoff / firing) dated t or t - 1 (19.FatherDisplacement.py)
    unemployed  hours unemployed > 0 (t <= 1992), or unemployed at any time in t (t >= 1993), or temporarily laid
                off / looking for work at the interview that follows t (t >= 1978)
    reduced     0 < annual hours < 1,500, counted only for men attached to full-time work (median annual hours over
                their valid years at 25-55 >= 1,500); a never-full-time man's short years are his normal years
    zero hours  annual hours = 0 (not a valid year; enters the instability shares only)
  Clean year = valid and neither displaced nor unemployed (clean A), and also not reduced (clean B).
SAMPLES
  Children: as in 6.IGEMain.py, the head's child at wave-ages 13-19 (parental income = mean total family income over
  those years, >= 3 years in bounds; parental head aged 30-70 at 16). Father = the male head of the child's family
  unit at 16 (nearest wave); children with a female head at 16 have no father here. The father's CHILDHOOD window
  is the same waves (income years when the child is 12-18); his WORKING-LIFE window is his valid years as head at
  25-55. Father measures = means of ln earnings, ln wage, ln hours over valid years (>= 3 childhood, >= 5 working
  life), so ln y = ln w + ln h holds for the means as well.
  Sons: male heads at 25-55; daughters: heads or wives at 25-55; child-years with a valid wage.
DESIGNS
  Lee-Solon (benchmark): child-year regressions, quartics in (A - 45)/10 (A = father's age at 16) and (C/10), C = age
  - 40, and x * (C/10)^n, n = 1..4, so the coefficient on x is the elasticity at 40 (6.IGEMain.py).
  Lifetime mean: one row per child, the means over valid years at 25-55 (>= 3), controls: child's birth-year FE,
  quadratics in the child's mean age and the father's age at 16.
  S.e. clustered by 1968 family (siblings share it). Every table reports coefficient (s.e.; p) with stars.
ANALYSES (sections of output/ige_decomposition.md)
  1. price vs quantity: earnings IGE, wage IGE, hours elasticity, cross elasticities; exact covariance split
     beta = [Cov(w_s,w_f~) + Cov(w_s,h_f~) + Cov(h_s,w_f~) + Cov(h_s,h_f~)] / Var(y_f~), ~ = partialled out on the
     design's controls (Frisch-Waugh), and the shares of Var(y_f~) due to Var(w_f~), Var(h_f~), 2Cov(w_f~,h_f~).
  2. purging shocks: clean years only (both generations), potential earnings = wage x 2,000 hours.
  3. instability: shares of displaced / unemployed / reduced / zero-hours years, the variance of transitory ln
     earnings (residual after person FE, an age quartic and year FE, male heads, by race), and their IGE.
  4. education mediation (Palomino et al. 2018 / BFHO style) of the benchmark (parental family income) IGE of sons'
     ln earnings, ln wage, ln hours; instability mediators; the father's education.
  5. reliability: one-year and childhood-mean reliability ratios of the father's ln earnings, wage, hours and family
     income (slope of his working-life mean, years >= 3 away, on the measure; 4.Estimates.py logic), by race.
  6. composition: White children re-weighted to the Black parental distribution (20 quantile bins of the pooled
     parental measure, child-year level), common support, IGE by parental tercile.
  7. the Black-White gap in the father-earnings IGE = composition + wage transmission + variance-share (hours share
     of the father's earnings variance) + hours transmission + wage-hours cross terms, exact; bootstrap s.e. (200
     draws, families resampled within race).
Writes output/ige_decomposition.csv (every estimate), output/ige_decomposition.md, output/ige_decomposition.png;
caches the panel in data/ige_decomposition_panel.pkl (delete to rebuild from the raw files).
"""
import importlib.util
import os
import warnings

import numpy as np
import pandas as pd
from scipy.stats import norm

from common import DATA, OUT, HERE, CPI, stars

warnings.simplefilter("ignore", FutureWarning)
warnings.simplefilter("ignore", RuntimeWarning)
pd.set_option("display.width", 250)


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


psid1 = _load("psid1", "1.PSID.py")
psid9 = _load("psid9", "9.ChildExposure.py")
ige6 = _load("ige6", "6.IGEMain.py")
WAVES, FAM, IND, layout, read = psid1.WAVES, psid1.FAM, psid1.IND, psid1.layout, psid1.read

LO, HI = ige6.LO, ige6.HI                       # $100 / $150,000 in 1967 dollars, in 2000 dollars
WLO, WHI, HMIN = 2.0, 200.0, 100                # hourly wage bounds (2000 $), minimum annual hours of a valid year
FT, POT = 1500, 2000                            # reduced-hours threshold; potential-earnings hours
NBOOT, SEED = int(os.environ.get("IGE_NBOOT", 200)), 20261017     # IGE_NBOOT only for quick test runs
CACHE = DATA / "ige_decomposition_panel.pkl"
UNEMP = {1994: "ER2188", 1995: "ER5187", 1996: "ER7283", 1997: "ER10199", 1999: "ER13330", 2001: "ER17353",
         2003: "ER21317", 2005: "ER25306", 2007: "ER36311", 2009: "ER42338", 2011: "ER47651", 2013: "ER53351",
         2015: "ER60366", 2017: "ER66369", 2019: "ER72369", 2021: "ER78408", 2023: "ER82395"}
EMPST = {1979: "ER30293", 1980: "ER30323", 1981: "ER30353", 1982: "ER30382", 1983: "ER30411", 1984: "ER30441",
         1985: "ER30474", 1986: "ER30509", 1987: "ER30545", 1988: "ER30580", 1989: "ER30616", 1990: "ER30653",
         1991: "ER30699", 1992: "ER30744", 1993: "ER30816", 1994: "ER33111", 1995: "ER33211", 1996: "ER33311",
         1997: "ER33411", 1999: "ER33512", 2001: "ER33612", 2003: "ER33712", 2005: "ER33813", 2007: "ER33913",
         2009: "ER34016", 2011: "ER34116", 2013: "ER34216", 2015: "ER34317", 2017: "ER34516", 2019: "ER34716",
         2021: "ER34916", 2023: "ER35116"}


# ================================================================ data
def fam_extra():
    out = []
    for i, w in enumerate(WAVES):
        folder = FAM / (f"fam{w}" if w < 1994 else f"fam{w}er")
        base = next(f for f in folder.glob("*.do") if "formats" not in f.name).with_suffix("")
        pos, labs = layout(base.with_suffix(".do"))
        idv = "V3" if w == 1968 else labs[1][0]
        cols = [idv, psid9.HH[i], psid9.WH[i]] + [c for c in (psid9.HU.get(w), UNEMP.get(w)) if c]
        f = read(base, cols, pos)
        x = pd.DataFrame({"wave": w, "int": f[idv]})
        x["hh"] = f[psid9.HH[i]].where(f[psid9.HH[i]].between(0, 5840))
        x["wh"] = f[psid9.WH[i]].where(f[psid9.WH[i]].between(0, 5840))
        x["hu"] = f[psid9.HU[w]].where(f[psid9.HU[w]].between(0, 5840)) if w in psid9.HU else np.nan
        x["ub"] = (f[UNEMP[w]] == 1).astype(float).where(f[UNEMP[w]].isin([1, 5, 0])) if w in UNEMP else np.nan
        out.append(x)
    return pd.concat(out, ignore_index=True)


def ind_extra():
    pos, labs = layout(IND.with_suffix(".do"))
    edu = [v for v, l in labs if psid9.EDU.match(l)]
    d = read(IND, ["ER30001", "ER30002", *EMPST.values(), *edu], pos)
    pid = d.ER30001 * 1000 + d.ER30002
    e = d[edu].where((d[edu] >= 1) & (d[edu] <= 17))
    educ = pd.Series(e.max(axis=1).to_numpy(), index=pid, name="educ")
    est = pd.concat([pd.DataFrame({"pid": pid, "wave": w, "est": d[c]}) for w, c in EMPST.items()])
    return educ, est[est["est"].between(1, 9)]


def build_panel():
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    fam = fam_extra()
    educ, est = ind_extra()
    a = py[py["head"] | py["wife"]].merge(fam, on=["wave", "int"], how="left").merge(est, on=["pid", "wave"],
                                                                                    how="left")
    a["year"] = a["wave"] - 1
    a["hours"] = np.where(a["head"], a["hh"], a["wh"])
    a["educ"] = a["pid"].map(educ)
    d = pd.read_pickle(DATA / "psid_displacement.pkl")
    dm = set(zip(d.loc[d["main"] == 1, "pid"], d.loc[d["main"] == 1, "year"]))
    a["disp"] = [float((p, y) in dm or (p, y - 1) in dm) for p, y in zip(a["pid"], a["year"])]
    hd = a["head"] & (a["female"] == 0)
    a["disp"] = a["disp"].where(hd)
    u = pd.concat([(a["hu"] > 0).where(a["hu"].notna()), a["ub"], a["est"].isin([2, 3]).where(a["est"].notna())],
                  axis=1)
    a["unemp"] = u.max(axis=1).where(hd & u.notna().any(axis=1))
    a["est23"] = a["est"].isin([2, 3]).astype(float).where(a["est"].notna())
    a["valid"] = (a["earn"].between(LO, HI) & (a["hours"] >= HMIN)
                  & (a["earn"] / a["hours"]).between(WLO, WHI))
    a["ly"] = np.log(a["earn"].where(a["valid"]))
    a["lh"] = np.log(a["hours"].where(a["valid"]))
    a["lw"] = a["ly"] - a["lh"]
    a["lfam"] = np.log(a["faminc"].where(a["faminc"].between(LO, HI)))
    keep = ["pid", "fam68", "female", "wave", "int", "year", "age", "head", "wife", "hrace", "faminc", "earn",
            "hours", "hu", "ub", "est", "est23", "disp", "unemp", "educ", "valid", "ly", "lh", "lw", "lfam", "wt"]
    return a[keep].reset_index(drop=True), py


def add_flags(a):
    """Reduced hours (full-time attached men), zero hours, clean A / B; transitory ln-earnings residuals."""
    mh = a["head"] & (a["female"] == 0)
    med = a[mh & a["valid"] & a["age"].between(25, 55)].groupby("pid")["hours"].median()
    a["ftatt"] = a["pid"].map(med >= FT).fillna(False)
    a["zero"] = (a["hours"] == 0).astype(float).where(a["hours"].notna())
    a["red"] = (a["hours"].between(1, FT - 1) & a["ftatt"]).astype(float).where(a["hours"].notna())
    a["shock"] = pd.concat([a["disp"], a["unemp"]], axis=1).max(axis=1).fillna(0)
    a["cleanA"] = a["valid"] & (a["shock"] == 0)
    a["cleanB"] = a["cleanA"] & (a["red"] != 1)
    # transitory ln earnings: male heads 25-60, by race; residual of ln y on person FE + age quartic + year FE
    a["eps"] = np.nan
    for race in ("Black", "White"):
        s = a[mh & a["valid"] & a["age"].between(25, 60) & (a["hrace"] == race)]
        X = pd.concat([pd.DataFrame({f"a{n}": ((s["age"] - 40) / 10) ** n for n in range(1, 5)}),
                       pd.get_dummies(s["year"], prefix="y", drop_first=True, dtype=float)], axis=1)
        Z = np.column_stack([s["ly"].to_numpy(), X.to_numpy(float)])
        g = pd.factorize(s["pid"])[0]
        cnt = np.bincount(g)
        for j in range(Z.shape[1]):
            Z[:, j] -= (np.bincount(g, weights=Z[:, j]) / cnt)[g]
        b = np.linalg.lstsq(Z[:, 1:], Z[:, 0], rcond=None)[0]
        a.loc[s.index, "eps"] = Z[:, 0] - Z[:, 1:] @ b
    return a


def children(py, a):
    """One row per child (6.IGEMain.py parents): parental income, father's id, race, the father's measures."""
    par = ige6.parents(py)
    k = py[py["child"] & py["age"].between(13, 19) & py["faminc"].between(LO, HI)]
    k16 = k.assign(dist=(k["age"] - 16).abs()).sort_values(["pid", "dist"]).groupby("pid").first()
    hd = py[py["head"]][["wave", "int", "pid", "female"]].drop_duplicates(["wave", "int"]).rename(
        columns={"pid": "fpid", "female": "hfemale"})
    k16 = k16.reset_index()[["pid", "wave", "int", "fam68", "female", "birth_year"]].merge(hd, on=["wave", "int"],
                                                                                          how="left")
    ch = par.join(k16.set_index("pid"))
    ch = ch[ch["race"].isin(["Black", "White"])].copy()
    ch["lyp"] = np.log(ch["yp"])
    ch.loc[ch["hfemale"] != 0, "fpid"] = np.nan
    # the father's childhood window: income years of the child's wave-ages 13-19
    win = k[["pid", "wave"]].rename(columns={"pid": "cpid"}).merge(ch[["fpid"]].dropna().reset_index(), left_on="cpid",
                                                                   right_on="pid")[["cpid", "fpid", "wave"]]
    fa = a[a["head"] & (a["female"] == 0)]
    fw = win.merge(fa, left_on=["fpid", "wave"], right_on=["pid", "wave"], how="inner")
    ch = ch.join(person_measures(fw, "cpid").add_prefix("f_"))
    # the father's working life: valid years as head at 25-55
    fl = fa[fa["age"].between(25, 55) & fa["pid"].isin(ch["fpid"])]
    lm = person_measures(fl, "pid", min_obs=5).add_prefix("fl_")
    ch = ch.join(lm, on="fpid")
    ch["f_educ"] = ch["fpid"].map(a.groupby("pid")["educ"].first())
    ch["f_age16"] = ch["A"]
    return ch


def person_measures(x, by, min_obs=3):
    """Means of ln y / ln w / ln h over valid years (all, clean A, clean B), instability shares, transitory var."""
    g = x.groupby(by)
    out = pd.DataFrame({"n": g["valid"].sum(), "nyrs": g["year"].count()})
    for tag, m in (("", "valid"), ("_cA", "cleanA"), ("_cB", "cleanB")):
        v = x[x[m]].groupby(by)
        for c in ("ly", "lw", "lh", "lfam"):
            out[c + tag] = v[c].mean()
        out["n" + tag] = v["ly"].count()
    out["lfam_all"] = g["lfam"].mean().where(g["lfam"].count() >= min_obs)
    cf = x[(x["shock"] == 0) & (x["zero"] != 1)].groupby(by)["lfam"]
    out["lfam_cA"] = cf.mean().where(cf.count() >= min_obs)
    for c in ("disp", "unemp", "red", "zero", "shock", "est23"):
        out["sh_" + c] = g[c].mean()
    e = x[x["valid"]].groupby(by)["eps"]
    out["vtr"] = e.var().where(e.count() >= 3)
    out["age_m"] = x[x["valid"]].groupby(by)["age"].mean()
    for c in ("ly", "lw", "lh"):
        out[c] = out[c].where(out["n"] >= min_obs)
        out[c + "_cA"] = out[c + "_cA"].where(out["n_cA"] >= min_obs)
        out[c + "_cB"] = out[c + "_cB"].where(out["n_cB"] >= min_obs)
    return out


def load():
    """Panel of heads / wives with flags (cached), the person-year file, one row per child."""
    if CACHE.exists():
        a, py = pd.read_pickle(CACHE), pd.read_pickle(DATA / "psid_person_year.pkl")
    else:
        a, py = build_panel()
        a = add_flags(a)
        a.to_pickle(CACHE)
    return a, py, children(py, a)


# ================================================================ analysis frames
SON_COLS = ["pid", "fam68", "year", "wave", "age", "valid", "ly", "lw", "lh", "lfam", "cleanA", "cleanB", "shock",
            "zero", "educ", "disp", "unemp", "red", "est23", "eps", "hours"]
INST = ["s_sh_unemp", "s_sh_disp", "s_sh_red", "s_sh_zero"]
SH = [("sh_disp", "Share of years displaced (closure / layoff, t or t-1)"),
      ("sh_unemp", "Share of years with unemployment"),
      ("sh_est23", "Share laid off / looking at the interview"),
      ("sh_red", "Share of years with reduced hours (< 1,500, full-time attached)"),
      ("sh_zero", "Share of years with zero hours"),
      ("sh_shock", "Share of years displaced or unemployed"),
      ("vtr", "Variance of transitory ln earnings"),
      ("nyrs", "Head-years observed")]


def frames(a, ch, female):
    """Child-year frame (Lee-Solon design) and child frame (lifetime-mean design) for sons or daughters."""
    c = ch[ch["female"] == female]
    m = (a["head"] & (a["female"] == 0)) if female == 0 else ((a["head"] | a["wife"]) & (a["female"] == 1))
    r = a[m & a["age"].between(25, 55) & a["pid"].isin(c.index)][SON_COLS].copy()
    sm = person_measures(r, "pid").add_prefix("s_")
    keep = ["race", "A", "lyp", "yp", "birth_year", "fpid", "f_educ"] + [x for x in c.columns
                                                                       if x.startswith(("f_", "fl_")) and x != "f_educ"]
    cc = c[keep]
    r = r.join(cc, on="pid").join(sm[INST], on="pid")
    r["C"] = r["age"] - 40
    r["ly_cA"], r["ly_cB"] = r["ly"].where(r["cleanA"]), r["ly"].where(r["cleanB"])
    r["lfam_s"] = r["lfam"]
    r["lfam_scA"] = r["lfam"].where((r["shock"] == 0) & (r["zero"] != 1))
    lt = sm.join(cc, how="inner")
    for v in ("ly", "lw", "lh", "ly_cA", "ly_cB", "age_m"):
        lt[v] = lt["s_" + v]
    lt["lfam_s"], lt["lfam_scA"] = lt["s_lfam_all"], lt["s_lfam_cA"]
    lt["educ"] = r.groupby("pid")["educ"].first()
    lt["pid"] = lt.index
    lt["fam68"] = lt.index // 1000
    return r.reset_index(drop=True), lt.reset_index(drop=True)


# ================================================================ estimation
def fit(y, X, w=None):
    if w is None:
        return np.linalg.lstsq(X, y, rcond=None)[0]
    s = np.sqrt(w)
    return np.linalg.lstsq(X * s[:, None], y * s, rcond=None)[0]


def fit_cl(y, X, g, w=None):
    """WLS with CR1 cluster-robust covariance."""
    w = np.ones(len(y)) if w is None else w
    Xw = X * w[:, None]
    XtX = np.linalg.pinv(X.T @ Xw)
    b = XtX @ (Xw.T @ y)
    e = y - X @ b
    gi = pd.factorize(g)[0]
    G = gi.max() + 1
    S = np.zeros((G, X.shape[1]))
    np.add.at(S, gi, Xw * e[:, None])
    n, k = X.shape
    V = G / (G - 1) * (n - 1) / (n - k) * XtX @ (S.T @ S) @ XtX
    return b, np.sqrt(np.maximum(np.diag(V), 0)), G


def base_cols(design):
    return ["A", "C"] if design in ("LS", "LSN") else ["A", "age_m", "birth_year"]


def controls(d, x, design):
    one = np.ones(len(d))
    A = (d["A"].to_numpy(float) - 45) / 10
    if design == "LS":
        C, xv = d["C"].to_numpy(float) / 10, d[x].to_numpy(float)
        return np.column_stack([one] + [A ** k for k in range(1, 5)] + [C ** k for k in range(1, 5)]
                               + [xv * C ** k for k in range(1, 5)])
    if design == "LSN":                         # Lee-Solon controls without the x-age interactions
        C = d["C"].to_numpy(float) / 10
        return np.column_stack([one] + [A ** k for k in range(1, 5)] + [C ** k for k in range(1, 5)])
    am = (d["age_m"].to_numpy(float) - 40) / 10
    fe = pd.get_dummies(d["birth_year"].astype(int), drop_first=True, dtype=float).to_numpy()
    return np.column_stack([one, am, am ** 2, A, A ** 2, fe])


def design_X(d, x, design, extra=()):
    return np.column_stack([d[x].to_numpy(float), *[d[e].to_numpy(float) for e in extra], controls(d, x, design)])


def regress(d, y, x, design, extra=(), w=None):
    """Coefficients on x and the extra regressors, cluster (fam68) s.e."""
    dd = d.dropna(subset=[y, x, *extra, *base_cols(design)] + ([w] if w else []))
    b, s, G = fit_cl(dd[y].to_numpy(float), design_X(dd, x, design, extra), dd["fam68"].to_numpy(),
                     dd[w].to_numpy(float) if w else None)
    names = [x, *extra]
    co = {nm: (b[i], s[i], 2 * norm.sf(abs(b[i] / s[i])) if s[i] > 0 else np.nan) for i, nm in enumerate(names)}
    return dict(beta=b[0], se=s[0], p=co[x][2], coefs=co, n=len(dd), children=dd["pid"].nunique(), clusters=G)


def coef(dd, y, x, design, w=None):
    return fit(dd[y].to_numpy(float), design_X(dd, x, design), w)[0]


def reweight(xb, xw, nb=20):
    """Weights making the White distribution of x match the Black one (nb pooled quantile bins)."""
    q = np.quantile(np.concatenate([xb, xw]), np.linspace(0, 1, nb + 1)[1:-1])
    bb, bw = np.searchsorted(q, xb), np.searchsorted(q, xw)
    pb = np.bincount(bb, minlength=nb) / len(bb)
    pw = np.bincount(bw, minlength=nb) / len(bw)
    return np.where(pw > 0, pb / np.where(pw > 0, pw, 1), 0)[bw]


def decomp(dd, design, fp, w=None):
    """Exact split of the earnings IGE (Frisch-Waugh on the design's controls)."""
    Z = controls(dd, fp + "ly", "LSN" if design == "LS" else design)
    ww = np.ones(len(dd)) if w is None else w

    def res(v):
        return v - Z @ fit(v, Z, ww)

    rw, rh = res(dd[fp + "lw"].to_numpy(float)), res(dd[fp + "lh"].to_numpy(float))
    ry = rw + rh
    V, Vw, Vh, Cwh = (ww * ry * ry).sum(), (ww * rw * rw).sum(), (ww * rh * rh).sum(), (ww * rw * rh).sum()
    sw, sh = dd["lw"].to_numpy(float), dd["lh"].to_numpy(float)
    T = dict(T_ww=(ww * sw * rw).sum() / V, T_wh=(ww * sw * rh).sum() / V, T_hw=(ww * sh * rw).sum() / V,
             T_hh=(ww * sh * rh).sum() / V)
    W = ww.sum()
    return dict(beta=sum(T.values()), **T, s_w=Vw / V, s_h=Vh / V, s_c=2 * Cwh / V, b_w=(ww * sw * rw).sum() / Vw,
                b_h=(ww * sh * rh).sum() / Vh, var_yf=V / W, var_wf=Vw / W, var_hf=Vh / W)


def pieces(B, W, R):
    p = dict(total=B["beta"] - W["beta"], composition=R["beta"] - W["beta"],
             wage_trans=(B["b_w"] - R["b_w"]) * R["s_w"], wage_share=B["b_w"] * (B["s_w"] - R["s_w"]),
             hours_trans=(B["b_h"] - R["b_h"]) * R["s_h"], hours_share=B["b_h"] * (B["s_h"] - R["s_h"]),
             cross=(B["T_wh"] + B["T_hw"]) - (R["T_wh"] + R["T_hw"]))
    p["hours_all"] = p["wage_share"] + p["hours_trans"] + p["hours_share"]
    return p


def meas(fp):
    """(label, son outcome, parental measure, sample filter: column that must be observed)."""
    return [("earn", "ly", fp + "ly", None), ("earn_cs", "ly", fp + "ly", fp + "ly_cA"),
            ("cleanA", "ly_cA", fp + "ly_cA", None), ("cleanB", "ly_cB", fp + "ly_cB", None),
            ("fpot", "ly", fp + "lw", None), ("pot", "lw", fp + "lw", None), ("spot", "lw", fp + "ly", None),
            ("hours", "lh", fp + "lh", None), ("hours_y", "lh", fp + "ly", None), ("earn_h", "ly", fp + "lh", None),
            ("fam_all", "lfam_s", "lyp", None), ("fam_fp", "lfam_s", "lyp", fp + "ly"),
            ("fam_logs", "lfam_s", fp + "lfam_all", fp + "lfam_cA"), ("fam_clean", "lfam_scA", fp + "lfam_cA", None)]


MEAS_LAB = {"earn": "ln earnings on father's ln earnings (benchmark)",
            "earn_cs": "ln earnings on father's ln earnings, children with a clean-years father measure",
            "cleanA": "ln earnings, clean years A (no displacement / unemployment), both generations",
            "cleanB": "ln earnings, clean years B (A and no reduced hours), both generations",
            "fpot": "ln earnings on father's ln potential earnings (ln wage + ln 2,000)",
            "pot": "ln potential earnings on father's ln potential earnings (= wage IGE)",
            "spot": "ln potential earnings on father's ln earnings",
            "hours": "ln hours on father's ln hours", "hours_y": "ln hours on father's ln earnings",
            "earn_h": "ln earnings on father's ln hours",
            "fam_all": "ln family income on ln parental family income (6.IGEMain regressor), all children",
            "fam_fp": "same, father-present children",
            "fam_logs": "ln family income on father's mean ln family income, all years (clean-measure children)",
            "fam_clean": "ln family income on father's mean ln family income, clean years both generations"}


def stats(r, design, fp):
    out = {}
    bc = base_cols(design)
    B, W = r[r["race"] == "Black"], r[r["race"] == "White"]
    cols = bc + ["ly", "lw", "lh", fp + "ly", fp + "lw", fp + "lh"]
    b, w = B.dropna(subset=cols), W.dropna(subset=cols)
    D = {"B": decomp(b, design, fp), "W": decomp(w, design, fp),
         "Wr": decomp(w, design, fp, reweight(b[fp + "ly"].to_numpy(), w[fp + "ly"].to_numpy()))}
    for g, d in D.items():
        out.update({f"{g}|{k}": v for k, v in d.items()})
    out.update({f"gap|{k}": v for k, v in pieces(D["B"], D["W"], D["Wr"]).items()})
    for lab, y, x, flt in meas(fp):
        c = bc + [y, x] + ([flt] if flt else [])
        b, w = B.dropna(subset=c), W.dropna(subset=c)
        out[f"B|{lab}"], out[f"W|{lab}"] = coef(b, y, x, design), coef(w, y, x, design)
        out[f"Wr|{lab}"] = coef(w, y, x, design, reweight(b[x].to_numpy(), w[x].to_numpy()))
        out[f"gap|{lab}"] = out[f"B|{lab}"] - out[f"W|{lab}"]
    for lab in ("cleanA", "cleanB"):
        out[f"close|{lab}"] = 1 - out[f"gap|{lab}"] / out["gap|earn_cs"]
    for lab in ("fpot", "pot", "spot"):
        out[f"close|{lab}"] = 1 - out[f"gap|{lab}"] / out["gap|earn"]
    out["close|fam_clean"] = 1 - out["gap|fam_clean"] / out["gap|fam_logs"]
    for lab, ref in (("cleanA", "earn_cs"), ("cleanB", "earn_cs"), ("fpot", "earn"), ("pot", "earn"),
                     ("spot", "earn"), ("fam_clean", "fam_logs")):
        out[f"dgap|{lab}"] = out[f"gap|{lab}"] - out[f"gap|{ref}"]
    for lab in ("earn", "fam_all", "fam_fp"):
        out[f"close|comp_{lab}"] = (out[f"Wr|{lab}"] - out[f"W|{lab}"]) / out[f"gap|{lab}"]
    return out


def bootstrap(r, design, fp, seed):
    rng = np.random.default_rng(seed)
    codes = pd.factorize(r["race"].astype(str) + ":" + r["fam68"].astype(str))[0]
    order = np.argsort(codes, kind="stable")
    idx = np.split(order, np.flatnonzero(np.diff(codes[order])) + 1)
    grace = np.array([r["race"].iat[i[0]] for i in idx])
    groups = {race: np.flatnonzero(grace == race) for race in ("Black", "White")}
    draws = []
    for _ in range(NBOOT):
        sel = [idx[g] for race in ("Black", "White")
               for g in groups[race][rng.integers(0, len(groups[race]), len(groups[race]))]]
        draws.append(stats(r.iloc[np.concatenate(sel)], design, fp))
    return pd.DataFrame(draws)


# ================================================================ output helpers
CSV = []


def pval(b, se):
    return 2 * norm.sf(abs(b / se)) if se > 0 else np.nan


def fmt(b, se, p):
    if b is None or not np.isfinite(b):
        return ""
    pv = "<0.001" if p < 0.001 else f"{p:.3f}"
    return f"{b:.3f}{stars(p)} ({se:.3f}; p={pv})"


def table(header, panels):
    lines = ["| | " + " | ".join(header) + " |", "|---" * (len(header) + 1) + "|"]
    for title, rows in panels:
        if title:
            lines.append(f"| **{title}** |" + " |" * len(header))
        for lab, cells in rows:
            lines.append(f"| {lab} | " + " | ".join(cells) + " |")
    return lines + [""]


def rec(section, sample, race, stat, est, se=np.nan, p=np.nan, n=np.nan, **kw):
    CSV.append(dict(section=section, sample=sample, race=race, statistic=stat, estimate=est, se=se, p=p, n=n, **kw))


CONFIGS = [("Sons", 0, "LS", "f_", "Sons, Lee-Solon (age 40), father's childhood window"),
           ("Sons", 0, "LS", "fl_", "Sons, Lee-Solon (age 40), father's working life 25-55"),
           ("Sons", 0, "LT", "f_", "Sons, lifetime mean, father's childhood window"),
           ("Daughters", 1, "LS", "f_", "Daughters, Lee-Solon (age 40), father's childhood window"),
           ("Sons", 0, "LS", "f_", "Sons 35-55, Lee-Solon (age 40), father's childhood window")]
AGEMIN = {"Sons 35-55, Lee-Solon (age 40), father's childhood window": 35}


def pick(F, fem, design, lab):
    r, lt = F[fem]
    return r[r["age"] >= AGEMIN.get(lab, 25)] if design == "LS" else lt
DESIGN_NOTE = {"LS": "child-years at 25-55; quartics in (A-45)/10 and (age-40)/10, x times the age quartic",
               "LT": "one row per child; birth-year FE, quadratics in mean age and A"}


# ================================================================ main
def main():
    OUT.mkdir(exist_ok=True)
    a, py, ch = load()
    F = {0: frames(a, ch, 0), 1: frames(a, ch, 1)}
    md = ["# Black-White IGE gap: human capital (wage) transmission vs labor-market shocks", "",
          "Built by `24.IGEDecomposition.py` (2026-10-17); definitions in its docstring. PSID SRC + SEO, unweighted, "
          "race of the parental household head at child age 16. Father = male head of the child's family unit at "
          "16. ln earnings = ln hourly wage + ln annual hours in every valid year (earnings $100-$150,000 in 1967 $, "
          "hours >= 100, wage $2-$200 in 2000 $). Analytic s.e. clustered by 1968 family; bootstrap s.e. = 200 "
          "draws of 1968 families within race. *** p<0.01, ** p<0.05, * p<0.1. **Everything below is accounting: "
          "it says where the covariance and the gap sit, not what causes them.**", ""]

    # ---------------- 0. benchmark replication and samples
    s6 = ige6.build(py)
    rep = {}
    for race in ("Black", "White"):
        x = s6[(s6["female"] == 0) & (s6["race"] == race)]
        rep[race] = ige6.ige(x, "lfam"), ige6.ige(x[x["pid"].isin(ch.index[ch["f_ly"].notna()])], "lfam")
        for k, (lab, v) in enumerate((("all sons", rep[race][0]), ("father-present sons", rep[race][1]))):
            rec("0 benchmark", f"6.IGEMain sons, ln family income, {lab}", race, "IGE", v["beta"], v["se"], v["p"],
                v["n"])
    r0, l0 = F[0]
    nb = {race: dict(children=int((ch["female"].eq(0) & ch["race"].eq(race)).sum()),
                     fpresent=int((ch["female"].eq(0) & ch["race"].eq(race) & ch["fpid"].notna()).sum()),
                     fly=int((ch["female"].eq(0) & ch["race"].eq(race) & ch["f_ly"].notna()).sum()))
          for race in ("Black", "White")}
    md += ["## 0. Benchmark and samples", "",
           "6.IGEMain.py benchmark re-run (sons, ln family income, all years, s.e. by child): Black "
           + fmt(rep['Black'][0]['beta'], rep['Black'][0]['se'], rep['Black'][0]['p']) + ", White "
           + fmt(rep['White'][0]['beta'], rep['White'][0]['se'], rep['White'][0]['p'])
           + ". Same regression on sons whose father's childhood-window earnings are observed: Black "
           + fmt(rep['Black'][1]['beta'], rep['Black'][1]['se'], rep['Black'][1]['p']) + f" ({rep['Black'][1]['children']:,} sons), White "
           + fmt(rep['White'][1]['beta'], rep['White'][1]['se'], rep['White'][1]['p']) + f" ({rep['White'][1]['children']:,} sons).", "",
           f"Sons in the 6.IGEMain parental sample: Black {nb['Black']['children']:,} (male head at 16: "
           f"{nb['Black']['fpresent']:,}; father's childhood ln earnings observed, >= 3 valid years: "
           f"{nb['Black']['fly']:,}), White {nb['White']['children']:,} ({nb['White']['fpresent']:,}; "
           f"{nb['White']['fly']:,}). **The price / quantity analysis is necessarily on father-present children; "
           "for Black sons that is under half of the benchmark sample.**", ""]
    print(md[-4], md[-2], flush=True)

    # ---------------- 1. price vs quantity regressions (analytic s.e.)
    COLS1 = [("ly", "ly", "(1) ln earnings"), ("lw", "lw", "(2) ln wage"), ("lh", "lh", "(3) ln hours"),
             ("lw", "ly", "(4) ln wage"), ("lh", "ly", "(5) ln hours"), ("ly", "lw", "(6) ln earnings"),
             ("ly", "lh", "(7) ln earnings")]
    XLAB = {"ly": "Father's ln earnings", "lw": "Father's ln wage", "lh": "Father's ln hours"}
    panels = []
    for sex, fem, design, fp, lab in CONFIGS:
        d = pick(F, fem, design, lab)
        for race in ("Black", "White"):
            dd = d[d["race"] == race]
            res = [regress(dd, y, fp + x, design) for y, x, _ in COLS1]
            for (y, x, h), v in zip(COLS1, res):
                rec("1 price-quantity", lab, race, f"{y} on {fp}{x}", v["beta"], v["se"], v["p"], v["n"])
            rows = [(XLAB[xv], [fmt(v["beta"], v["se"], v["p"]) if x == xv else "" for (y, x, h), v in
                                zip(COLS1, res)]) for xv in ("ly", "lw", "lh")]
            rows += [("N (child-years or children) / children / clusters",
                      [f"{v['n']:,} / {v['children']:,} / {v['clusters']:,}" for v in res]),
                     ("Controls", [DESIGN_NOTE[design]] * len(res))]
            panels.append((f"{lab}: {race}", rows))
    md += ["## 1. Price vs quantity: earnings IGE, wage IGE, hours elasticity", "",
           "One regression per column (child's outcome in the header); the regressor row says which father measure. "
           "Father measures are means over valid years (childhood window = income years when the child is 12-18; "
           "working life = his valid years at 25-55). Columns (4)+(5) = (1) exactly (same sample, same controls).",
           ""] + table([h for _, _, h in COLS1], panels)

    # ---------------- 1c. age profile of the IGE (sons)
    AC = [("lfam_s", "lyp", "(1) ln family income on ln parental family income"),
          ("ly", "f_ly", "(2) ln earnings on father's ln earnings"), ("lw", "f_lw", "(3) ln wage on father's ln wage"),
          ("lh", "f_lh", "(4) ln hours on father's ln hours"), ("lw", "f_ly", "(5) ln wage on father's ln earnings"),
          ("lh", "f_ly", "(6) ln hours on father's ln earnings"), ("lw", "lyp", "(7) ln wage on ln parental income"),
          ("lh", "lyp", "(8) ln hours on ln parental income")]
    r0 = F[0][0]
    panels = []
    for lo, hi in ((25, 34), (35, 44), (45, 55), (25, 55)):
        res = {race: [regress(r0[(r0["race"] == race) & r0["age"].between(lo, hi)], y, x, "LSN") for y, x, _ in AC]
               for race in ("Black", "White")}
        rows = []
        for race in ("Black", "White"):
            rows.append((race, [fmt(v["beta"], v["se"], v["p"]) for v in res[race]]))
            for (y, x, _), v in zip(AC, res[race]):
                rec("1b age profile", f"sons {lo}-{hi}", race, f"{y} on {x}", v["beta"], v["se"], v["p"], v["n"])
        gp = [(vb["beta"] - vw["beta"], np.sqrt(vb["se"] ** 2 + vw["se"] ** 2)) for vb, vw in zip(res["Black"],
                                                                                              res["White"])]
        rows.append(("Black - White", [fmt(g_, s_, pval(g_, s_)) for g_, s_ in gp]))
        rows.append(("Child-years Black / White", [f"{vb['n']:,} / {vw['n']:,}" for vb, vw in zip(res["Black"],
                                                                                                   res["White"])]))
        panels.append((f"Sons' ages {lo}-{hi}", rows))
    md += ["## 1b. Age profile: where the gap opens", "",
           "Sons, Lee-Solon controls (quartics in the father's age at 16 and the son's age) WITHOUT the x-age "
           "interactions, estimated within son age bands: the slope over the child-years in the band. One "
           "regression per cell (outcome and regressor in the header). Black - White s.e. = root sum of squared "
           "s.e. (races are disjoint clusters). Columns (5)+(6) = (2) and (7)+(8) = the ln earnings IGE on parental "
           "income in each band.", ""] + table([h for *_, h in AC], panels)

    # ---------------- bootstrap: decomposition, purging, composition
    BOOT = {}
    bc = os.environ.get("IGE_BOOTCACHE")             # development only: reuse saved bootstrap results
    if bc and os.path.exists(bc):
        BOOT = pd.read_pickle(bc)
    for k, (sex, fem, design, fp, lab) in enumerate(CONFIGS):
        d = pick(F, fem, design, lab)
        if lab not in BOOT:
            pt = stats(d, design, fp)
            print(f"bootstrap {lab} ...", flush=True)
            BOOT[lab] = (pt, bootstrap(d, design, fp, SEED + k).std())
        pt, se = BOOT[lab]
        for kk, v in pt.items():
            g, st = kk.split("|")
            rec("bootstrap", lab, g, st, v, se[kk], pval(v, se[kk]))

    def bcell(lab, key):
        pt, se = BOOT[lab]
        return fmt(pt[key], se[key], pval(pt[key], se[key]))

    # ---------------- 1b. covariance decomposition
    ROWS = [("T_ww", "Cov(w_s, w_f) / Var(y_f)"), ("T_wh", "Cov(w_s, h_f) / Var(y_f)"),
            ("T_hw", "Cov(h_s, w_f) / Var(y_f)"), ("T_hh", "Cov(h_s, h_f) / Var(y_f)"),
            ("beta", "Sum = earnings IGE"), ("s_w", "Share of Var(y_f): Var(w_f)"),
            ("s_h", "Share of Var(y_f): Var(h_f)"), ("s_c", "Share of Var(y_f): 2Cov(w_f, h_f)"),
            ("b_w", "Wage transmission Cov(w_s, w_f) / Var(w_f)"), ("b_h", "Hours transmission Cov(h_s, h_f) / Var(h_f)"),
            ("var_yf", "Var(y_f) (partialled)"), ("var_wf", "Var(w_f) (partialled)"), ("var_hf", "Var(h_f) (partialled)")]
    panels = []
    for _, _, _, _, lab in CONFIGS:
        pt, se = BOOT[lab]
        rows = []
        for k, nm in ROWS:
            cells = [bcell(lab, f"{g}|{k}") for g in ("B", "W", "Wr")]
            dk = pt[f"B|{k}"] - pt[f"W|{k}"]
            # s.e. of the difference: races are resampled independently
            sd = np.sqrt(se[f"B|{k}"] ** 2 + se[f"W|{k}"] ** 2)
            rows.append((nm, cells + [fmt(dk, sd, pval(dk, sd))]))
        panels.append((lab, rows))
    md += ["## 1c. Exact covariance decomposition of the earnings IGE", "",
           "beta = [Cov(w_s,w_f) + Cov(w_s,h_f) + Cov(h_s,w_f) + Cov(h_s,h_f)] / Var(y_f), father measures "
           "partialled out on the design's controls (Frisch-Waugh). Lee-Solon panels: the quartics in the father's "
           "age at 16 and the child's age, WITHOUT the y_f x age-quartic interactions (partialling y_f on its own "
           "interactions leaves a residual whose variance is a fraction of Var(y_f), and the variance shares then "
           "exceed 1), so the IGE here is the slope averaged over child-years at 25-55 rather than the IGE at 40; "
           "Section 7 reports the age-40 gap next to it. Wage / hours transmission are the identity-"
           "consistent slopes (partialled on the same controls), so they differ slightly from columns (2)-(3) of "
           "Section 1. 'White re-weighted' = White children re-weighted to the Black distribution of the father's "
           "ln earnings. Bootstrap s.e.", ""] + table(["Black", "White", "White re-weighted to Black", "Black - White"],
                                                       panels)

    # ---------------- 2. purging shocks
    ML = ["earn", "earn_cs", "cleanA", "cleanB", "fpot", "pot", "spot", "fam_fp", "fam_logs", "fam_clean"]
    panels = []
    for _, fem, design, fp, lab in CONFIGS:
        d = pick(F, fem, design, lab)
        rows, nrow = {"Black": [], "White": []}, {"Black": [], "White": []}
        for m in ML:
            _, y, x, flt = next(t for t in meas(fp) if t[0] == m)
            for race in ("Black", "White"):
                dd = d[d["race"] == race]
                if flt:
                    dd = dd[dd[flt].notna()]
                v = regress(dd, y, x, design)
                rows[race].append(fmt(v["beta"], v["se"], v["p"]))
                nrow[race].append(f"{v['n']:,} / {v['children']:,}")
                rec("2 purging", lab, race, m, v["beta"], v["se"], v["p"], v["n"])
        gap = [bcell(lab, f"gap|{m}") for m in ML]
        close = [bcell(lab, f"dgap|{m}") + f" [{BOOT[lab][0][f'close|{m}']:.0%}]" if f"dgap|{m}" in BOOT[lab][0]
                 else "" for m in ML]
        panels.append((lab, [("Black: coefficient on the parental measure", rows["Black"]),
                             ("Black: N / children", nrow["Black"]),
                             ("White: coefficient on the parental measure", rows["White"]),
                             ("White: N / children", nrow["White"]),
                             ("Black - White gap (bootstrap)", gap),
                             ("Change in the gap vs its reference column (bootstrap) [share closed]", close)]))
    md += ["## 2. Purging shocks: clean years and potential earnings", "",
           "One regression per column; columns: " + "; ".join(f"({i + 1}) {MEAS_LAB[m]}" for i, m in enumerate(ML))
           + ". Change in the gap (positive = smaller gap) and [share of the gap closed]: (3)-(4) relative to (2) "
           "(same children), (5)-(7) relative to (1), (10) relative to (9); the share is a ratio of noisy gaps, so "
           "only the change carries a bootstrap s.e. "
           "Clean years: a father's (son's) measure is the mean over his clean valid years (>= 3). Potential "
           "earnings use the observed hourly wage, which itself carries shocks (division bias, wage cuts after "
           "displacement); column (6) is the wage IGE in logs. Daughters: the displacement and unemployment flags "
           "exist for male heads only, so the daughters' own years are cleaned only for reduced hours (never, since "
           "the full-time-attachment rule is for men) and the cleaning is on the father's side.", ""] + table(
        [f"({i + 1}) {m}" for i, m in enumerate(ML)], panels)

    # ---------------- 3. instability
    lt0 = F[0][1]
    lt0 = lt0.assign(s_lvtr=np.log(lt0["s_vtr"]), f_lvtr=np.log(lt0["f_vtr"]), fl_lvtr=np.log(lt0["fl_vtr"]))
    rows = []
    for v, nm in SH:
        cells = []
        for pre in ("f_", "fl_", "s_"):
            d = lt0.dropna(subset=[pre + v])
            d = d[d["f_ly"].notna()] if pre != "s_" else d
            X = np.column_stack([np.ones(len(d)), d["race"].eq("Black").to_numpy(float)])
            b, s, G = fit_cl(d[pre + v].to_numpy(float), X, d["fam68"].to_numpy())
            mw, mb = b[0], b[0] + b[1]
            cells += [f"{mb:.3f}", f"{mw:.3f}", fmt(b[1], s[1], pval(b[1], s[1]))]
            rec("3 instability means", {"f_": "fathers, childhood window", "fl_": "fathers, working life",
                                        "s_": "sons 25-55"}[pre], "Black-White", v, b[1], s[1], pval(b[1], s[1]),
                len(d), black=mb, white=mw)
        rows.append((nm, cells))
    md += ["## 3. Instability", "", "### 3a. Instability of fathers and sons, by race", "",
           "Means over the person's head-years in the window (one row per son; fathers repeat across brothers). "
           "Black - White = coefficient on Black in a regression of the measure on a constant and a Black "
           "dummy, s.e. clustered by 1968 family. Transitory ln earnings = residual after person FE, an age quartic "
           "and year FE (male heads 25-60, by race), so it includes any deviation from the person's mean (also "
           "permanent shocks within the window). Fathers: father-present sons with father's childhood earnings.", ""]
    md += table(["Fathers (childhood): Black", "White", "Black - White", "Fathers (25-55): Black", "White",
                 "Black - White", "Sons (25-55): Black", "White", "Black - White"], [("", rows)])
    IV = [("sh_disp", "displaced"), ("sh_unemp", "unemployment"), ("sh_red", "reduced hours"), ("sh_zero", "zero hours"),
          ("sh_shock", "displaced or unemployed"), ("lvtr", "ln transitory variance")]
    panels = []
    for race in ("Black", "White"):
        d = lt0[(lt0["race"] == race) & lt0["f_ly"].notna()]
        res = [regress(d, "s_" + v, "f_" + v, "LT") for v, _ in IV]
        for (v, _), x in zip(IV, res):
            rec("3 instability IGE", "sons on fathers (childhood window)", race, v, x["beta"], x["se"], x["p"], x["n"])
        panels.append((race, [("Father's same measure (childhood window)", [fmt(x["beta"], x["se"], x["p"]) for x in res]),
                              ("N sons / clusters", [f"{x['n']:,} / {x['clusters']:,}" for x in res])]))
    md += ["### 3b. Intergenerational persistence of instability", "",
           "One regression per column: the son's measure (header) on the father's same measure over the childhood "
           "window; controls: son's birth-year FE, quadratics in the son's mean age and the father's age at 16. "
           "Linear in shares (not elasticities).", ""] + table([f"({i + 1}) son's {nm}" for i, (_, nm) in
                                                                  enumerate(IV)], panels)

    # ---------------- 4. education mediation
    r0 = F[0][0]
    MED_A = [("ly", []), ("ly", ["educ"]), ("ly", ["educ"] + INST), ("lw", []), ("lw", ["educ"]), ("lh", []),
             ("lh", ["educ"]), ("lh", ["educ"] + INST)]
    MED_B = [("ly", []), ("ly", ["educ"]), ("ly", ["educ", "f_educ"]), ("ly", ["educ", "f_educ"] + INST),
             ("lw", []), ("lw", ["educ", "f_educ"]), ("lh", []), ("lh", ["educ", "f_educ"])]
    RLAB = {"educ": "Son's years of education", "f_educ": "Father's years of education",
            "s_sh_unemp": "Son's share of years with unemployment", "s_sh_disp": "Son's share of years displaced",
            "s_sh_red": "Son's share of years with reduced hours", "s_sh_zero": "Son's share of years with zero hours"}
    OLAB = {"ly": "ln earnings", "lw": "ln wage", "lh": "ln hours"}
    for tag, spec, x, xl, sub in (("4a", MED_A, "lyp", "ln parental family income (13-19 mean)", None),
                                  ("4b", MED_B, "f_ly", "Father's ln earnings (childhood window)", "f_educ")):
        panels = []
        for race in ("Black", "White"):
            d = r0[(r0["race"] == race)].dropna(subset=["ly", x, "educ"] + INST + ([sub] if sub else []))
            res = [regress(d, y, x, "LS", ex) for y, ex in spec]
            base = {}
            for (y, ex), v in zip(spec, res):
                base.setdefault(y, v["beta"])
                rec(f"{tag} mediation", xl, race, f"{y} + {'+'.join(ex) or 'none'}", v["beta"], v["se"], v["p"], v["n"])
            rows = [(xl, [fmt(v["beta"], v["se"], v["p"]) for v in res])]
            for reg in ["educ", "f_educ"] + INST:
                if any(reg in ex for _, ex in spec):
                    rows.append((RLAB[reg], [fmt(*v["coefs"][reg]) if reg in v["coefs"] else "" for v in res]))
            rows.append(("Share of the IGE mediated (vs the first column of the same outcome)",
                         [f"{1 - v['beta'] / base[y]:.3f}" if ex else "" for (y, ex), v in zip(spec, res)]))
            rows.append(("Child-years / sons / clusters", [f"{v['n']:,} / {v['children']:,} / {v['clusters']:,}"
                                                           for v in res]))
            panels.append((f"Sons: {race}", rows))
        title = ("### 4a. Benchmark regressor (parental family income), all sons" if tag == "4a" else
                 "### 4b. Father's ln earnings, father-present sons with the father's education")
        if tag == "4a":
            md += ["## 4. Human capital mediation (Palomino et al. 2018 / BFHO style)", "",
                   "Lee-Solon design (age 40), sons 25-55, valid years. One regression per column; the outcome is "
                   "the header; the same sample within a panel. Share mediated = 1 - beta(with mediators) / beta"
                   "(without). Because ln earnings = ln wage + ln hours, the ln earnings IGE on the parental measure "
                   "is the sum of the ln wage and ln hours IGEs (columns (1) = (4) + (6) in 4a). Education and the "
                   "son's instability shares are outcomes of the same background, so 'mediation' is an accounting of "
                   "coefficient movements, order-dependent and not causal.", ""]
        md += [title, ""] + table([f"({i + 1}) {OLAB[y]}" for i, (y, _) in enumerate(spec)], panels)

    # ---------------- 5. reliability
    md += reliability_section(a, ch, F, BOOT)

    # ---------------- 6. composition
    md += composition_section(F, BOOT)

    # ---------------- 7. final decomposition
    G = [("B|earn", "Reference: Black earnings IGE at age 40 (Lee-Solon with interactions; = Section 1 col. 1)"),
         ("W|earn", "Reference: White earnings IGE at age 40"), ("gap|earn", "Reference: gap at age 40"),
         ("B|beta", "Black earnings IGE (decomposed)"), ("W|beta", "White earnings IGE (decomposed)"),
         ("gap|total", "Black - White gap (decomposed)"),
         ("gap|composition", "Composition (White re-weighted to the Black father-earnings distribution)"),
         ("gap|wage_trans", "Human capital (wage) transmission: (b_w,B - b_w,W*) s_w,W*"),
         ("gap|hours_all", "Hours / instability, total of the three rows below"),
         ("gap|wage_share", "  wage share of the father's earnings variance: b_w,B (s_w,B - s_w,W*)"),
         ("gap|hours_trans", "  hours transmission: (b_h,B - b_h,W*) s_h,W*"),
         ("gap|hours_share", "  hours share of the father's earnings variance: b_h,B (s_h,B - s_h,W*)"),
         ("gap|cross", "Residual: wage-hours cross terms [Cov(w_s,h_f) + Cov(h_s,w_f)] / Var(y_f)")]
    rows = []
    for key, nm in G:
        cells = []
        for _, _, _, _, lab in CONFIGS:
            pt = BOOT[lab][0]
            sh = (f" [{pt[key] / pt['gap|total']:.0%}]" if key.startswith("gap|") and key not in ("gap|total", "gap|earn")
                  and not lab.startswith("Daughters") else "")
            cells.append(bcell(lab, key) + sh)
        rows.append((nm, cells))
    md += ["## 7. Decomposition of the Black-White gap in the father-earnings IGE", "",
           "Exact identity: gap = composition + wage transmission + (wage-share + hours transmission + hours-share) "
           "+ cross terms (Lee-Solon columns: slope over child-years without the age interactions, Section 1c), with W* = White children re-weighted to the Black distribution of the father's ln "
           "earnings and s = shares of the (partialled) variance of the father's ln earnings (Section 1c). Share of "
           "the gap in brackets (not shown for daughters, whose gap is about zero). Bootstrap s.e. (200 draws of 1968 families within race). Accounting, not causal: "
           "the 'hours' rows say how much of the gap sits in the hours component of measured earnings, which mixes "
           "shocks (layoffs, unemployment, short hours) with labor-supply and search-friction differences.", ""]
    md += table([lab for *_, lab in CONFIGS], [("", rows)])

    if bc:
        pd.to_pickle(BOOT, bc)
    md[md.index("## 0. Benchmark and samples"):md.index("## 0. Benchmark and samples")] = summary_section(BOOT, rep)
    figure(BOOT)
    pd.DataFrame(CSV).to_csv(OUT / "ige_decomposition.csv", index=False)
    (OUT / "ige_decomposition.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md[-40:]))


def reliability_section(a, ch, F, BOOT):
    c = ch[ch["f_ly"].notna() & (ch["female"] == 0)].reset_index()
    c["fam68"] = c["pid"] // 1000
    fa = a[a["head"] & (a["female"] == 0) & a["age"].between(25, 55)][
        ["pid", "wave", "age", "ly", "lw", "lh", "lfam"]].rename(columns={"pid": "fpid", "wave": "fw", "age": "fage"})
    m = c[["pid", "fpid", "wave"]].merge(fa, on="fpid")
    m["dw"] = m["fw"] - m["wave"]
    V = [("ly", "f_ly", "ln earnings"), ("lw", "f_lw", "ln wage"), ("lh", "f_lh", "ln hours"),
         ("lfam", "f_lfam_all", "ln family income")]
    RR, cols, panels = {}, [], {"Black": [], "White": []}
    for v, fv, nm in V:
        one = m[m["dw"] == 0].drop_duplicates("pid").set_index("pid")[[v, "fage"]].rename(columns={v: "x1"})
        o1 = m[m["dw"].abs() >= 3].groupby("pid")[v].agg(["mean", "count"]).rename(columns=lambda s: s + "1")
        o6 = m[m["dw"].abs() >= 6].groupby("pid")[v].agg(["mean", "count"]).rename(columns=lambda s: s + "6")
        d = c.set_index("pid").join(one).join(o1).join(o6)
        d["fage2"], d["A2"] = d["fage"] ** 2, d["A"] ** 2
        for kind, x, y, n, ctr in (("one year at 16", "x1", "mean1", "count1", ["fage", "fage2"]),
                                   ("childhood mean", fv, "mean6", "count6", ["A", "A2"])):
            cols.append(f"{nm}: {kind}")
            for race in ("Black", "White"):
                dd = d[(d["race"] == race) & (d[n] >= 3)].dropna(subset=[x, y] + ctr)
                X = np.column_stack([dd[x], np.ones(len(dd)), dd[ctr]])
                b, s, G = fit_cl(dd[y].to_numpy(float), X, dd["fam68"].to_numpy())
                RR[(v, kind, race)] = (b[0], s[0])
                panels[race].append((b[0], s[0], len(dd)))
                rec("5 reliability", f"fathers' {nm}, {kind}", race, "RR", b[0], s[0], pval(b[0], s[0]), len(dd))
    # transitory share of fathers' single-year ln earnings variance
    tsh = {}
    fy = a[a["head"] & (a["female"] == 0) & a["age"].between(25, 55) & a["valid"] & a["pid"].isin(c["fpid"])]
    for race in ("Black", "White"):
        s = fy[fy["hrace"] == race]
        X = np.column_stack([np.ones(len(s))] + [((s["age"].to_numpy() - 40) / 10) ** k for k in range(1, 5)]
                            + [pd.get_dummies(s["year"], drop_first=True, dtype=float).to_numpy()])
        e = s["ly"].to_numpy() - X @ fit(s["ly"].to_numpy(), X)
        tsh[race] = (np.nanvar(s["eps"]) / np.var(e), np.nanvar(s["eps"]), np.var(e), len(s))
        rec("5 reliability", "fathers' single-year ln earnings", race, "transitory share", tsh[race][0], n=len(s))
    rows = [(f"{race}: reliability ratio", [fmt(b, s, pval(b, s)) for b, s, _ in panels[race]]) for race in
            ("Black", "White")]
    rows += [(f"{race}: N sons", [f"{n:,}" for _, _, n in panels[race]]) for race in ("Black", "White")]
    out = ["## 5. Reliability and attenuation of the father's measure", "",
           "Reliability ratio (4.Estimates.py / BFHO Appendix B logic, in the father generation): slope of the "
           "father's mean over his valid years at 25-55 at least 3 years (one-year measure) or 6 years (childhood-"
           "window mean) away from the measurement, on the measure; controls: his age (quadratic) or his age at the "
           "child's 16 (quadratic). One row per father-present son; s.e. clustered by 1968 family. One column per "
           "regression.", ""] + table(cols, [("", rows)])
    out += ["Transitory share of the variance of single-year ln earnings (fathers, valid years at 25-55, ln "
            "earnings net of an age quartic and year FE; transitory = deviation from the person mean): "
            + "; ".join(f"{r} {t[0]:.3f} (transitory variance {t[1]:.3f} of {t[2]:.3f}, {t[3]:,} father-years)"
                        for r, t in tsh.items()) + ".", ""]
    # implied attenuation
    pt, se = BOOT[CONFIGS[0][4]]
    rows = []
    for key, v, lab in (("earn", "ly", "Father-earnings IGE (sons, Lee-Solon, childhood window)"),
                        ("fam_all", "lfam", "Parental family-income IGE (sons, Lee-Solon, 6.IGEMain regressor)")):
        cells, corr = [], {}
        for race, g in (("Black", "B"), ("White", "W")):
            b, s = pt[f"{g}|{key}"], se[f"{g}|{key}"]
            rr, rs = RR[(v, "childhood mean", race)]
            bc = b / rr
            sc = np.sqrt((s / rr) ** 2 + (b * rs / rr ** 2) ** 2)
            corr[race] = (b, bc)
            cells += [fmt(b, s, pval(b, s)), f"{rr:.3f}", fmt(bc, sc, pval(bc, sc))]
            rec("5 attenuation", lab, race, "corrected IGE", bc, sc, pval(bc, sc), rr=rr)
        cells.append(f"{corr['Black'][0] / corr['White'][0]:.3f} -> {corr['Black'][1] / corr['White'][1]:.3f}")
        rows.append((lab, cells))
    out += ["Implied attenuation (IGE / reliability ratio of the childhood-window mean; delta-method s.e. treating "
            "the two as independent). 4.Estimates.py reports family-income reliability ratios of 0.565 / 0.585 "
            "(one year) and 0.631 / 0.650 (12-17 mean) for Black / White, estimated in the child generation.", ""]
    out += table(["Black IGE", "Black RR", "Black corrected", "White IGE", "White RR", "White corrected",
                  "Black / White ratio: raw -> corrected"], [("", rows)])
    return out


def composition_section(F, BOOT):
    r = F[0][0]
    specs = [("lfam_s", "lyp", "(1) ln family income on ln parental family income (all sons)"),
             ("ly", "f_ly", "(2) ln earnings on father's ln earnings (father-present sons)")]
    keys = ["Black", "White", "White re-weighted to the Black distribution", "Black, common support",
            "White, common support"] + [f"{r_}, pooled parental tercile {k}" for k in (1, 2, 3) for r_ in
                                        ("Black", "White")]
    cells = {k: [] for k in keys}
    shares = []
    for y, x, lab in specs:
        d = r.dropna(subset=[y, x, "A", "C"])
        B, W = d[d["race"] == "Black"], d[d["race"] == "White"].copy()
        W["rw"] = reweight(B[x].to_numpy(), W[x].to_numpy())
        lo, hi = max(B[x].quantile(.05), W[x].quantile(.05)), min(B[x].quantile(.95), W[x].quantile(.95))
        t = np.quantile(d[x], [0, 1 / 3, 2 / 3, 1])
        est = {"Black": regress(B, y, x, "LS"), "White": regress(W, y, x, "LS"),
               keys[2]: regress(W, y, x, "LS", w="rw"),
               "Black, common support": regress(B[B[x].between(lo, hi)], y, x, "LS"),
               "White, common support": regress(W[W[x].between(lo, hi)], y, x, "LS")}
        for k in (1, 2, 3):
            for race, dd in (("Black", B), ("White", W)):
                est[f"{race}, pooled parental tercile {k}"] = regress(dd[dd[x].between(t[k - 1], t[k])], y, x, "LS")
        shares.append(f"{lab}: share of child-years in the bottom / top pooled tercile: Black "
                      f"{(B[x] <= t[1]).mean():.2f} / {(B[x] > t[2]).mean():.2f}, White {(W[x] <= t[1]).mean():.2f} / "
                      f"{(W[x] > t[2]).mean():.2f}; common support = [{lo:.2f}, {hi:.2f}]")
        for k in keys:
            v = est[k]
            cells[k].append(fmt(v["beta"], v["se"], v["p"]) + f" (N {v['n']:,})")
            rec("6 composition", lab, k, "IGE", v["beta"], v["se"], v["p"], v["n"])
    pt, se = BOOT[CONFIGS[0][4]]
    rows = [(k, cells[k]) for k in keys]
    rows.append(("Share of the Black-White gap due to composition (bootstrap)",
                 [bcell2(BOOT, CONFIGS[0][4], "close|comp_fam_all"), bcell2(BOOT, CONFIGS[0][4], "close|comp_earn")]))
    return (["## 6. Composition: the parental income distribution", "",
             "Lee-Solon design, sons 25-55. One regression per cell (column = regression type, row = sample). "
             "Re-weighting: White child-years re-weighted so that the distribution of the parental measure over 20 "
             "pooled quantile bins matches the Black one (DiNardo-Fortin-Lemieux), analytic weighted s.e. Common "
             "support = between the larger of the two 5th percentiles and the smaller of the two 95th percentiles. "
             "Terciles of the pooled child-year distribution (slopes within a tercile are local and noisy).", ""]
            + table([lab for *_, lab in specs], [("", rows)]) + ["; ".join(shares) + ".", ""])


def bcell2(BOOT, lab, key):
    pt, se = BOOT[lab]
    return fmt(pt[key], se[key], pval(pt[key], se[key]))


def summary_section(BOOT, rep):
    """Headline numbers, pulled from the estimates above (CSV records and bootstrap results)."""
    c = pd.DataFrame(CSV)

    def g(section, sample, race, stat, col="estimate"):
        x = c[(c["section"] == section) & (c["sample"].str.startswith(sample)) & (c["race"] == race)
              & (c["statistic"] == stat)]
        return x[col].iat[0]

    L0, L2, L4 = CONFIGS[0][4], CONFIGS[2][4], CONFIGS[4][4]

    def ap(band, race, stat):
        return g("1b age profile", f"sons {band}", race, stat)
    pt, se = BOOT[L0]
    p2, s2 = BOOT[L2]

    def b(lab, key):
        p_, s_ = BOOT[lab]
        return fmt(p_[key], s_[key], pval(p_[key], s_[key]))

    sec1 = "1 price-quantity"
    rr = {(v, race): g("5 reliability", f"fathers' {nm}, childhood", race, "RR")
          for v, nm in (("ly", "ln earnings"), ("lfam", "ln family income")) for race in ("Black", "White")}
    out = ["## Summary", "",
           f"- **Benchmark.** 6.IGEMain family-income IGE of sons: Black {rep['Black'][0]['beta']:.3f}, White "
           f"{rep['White'][0]['beta']:.3f}; on the father-present sons used here {rep['Black'][1]['beta']:.3f} / "
           f"{rep['White'][1]['beta']:.3f}. Father-earnings IGE (Lee-Solon, age 40): Black {pt['B|earn']:.3f}, White "
           f"{pt['W|earn']:.3f}; lifetime-mean design {p2['B|earn']:.3f} / {p2['W|earn']:.3f}.",
           f"- **Price vs quantity (Section 1).** Wage IGE (son's ln wage on father's ln wage): Black "
           f"{g(sec1, L0, 'Black', 'lw on f_lw'):.3f}, White {g(sec1, L0, 'White', 'lw on f_lw'):.3f}; hours "
           f"elasticity: Black {g(sec1, L0, 'Black', 'lh on f_lh'):.3f}, White {g(sec1, L0, 'White', 'lh on f_lh'):.3f}."
           f" Of the earnings IGE on the father's earnings, the son's wage carries Black "
           f"{g(sec1, L0, 'Black', 'lw on f_ly'):.3f} of {g(sec1, L0, 'Black', 'ly on f_ly'):.3f} and White "
           f"{g(sec1, L0, 'White', 'lw on f_ly'):.3f} of {g(sec1, L0, 'White', 'ly on f_ly'):.3f}; the son's hours "
           f"carry almost nothing in either group.",
           f"- **Father's earnings variance (Section 1c, lifetime design).** Share due to Var(ln wage): Black "
           f"{p2['B|s_w']:.2f}, White {p2['W|s_w']:.2f}; due to Var(ln hours): Black {p2['B|s_h']:.2f}, White "
           f"{p2['W|s_h']:.2f}. Var(y_f): Black {p2['B|var_yf']:.3f}, White {p2['W|var_yf']:.3f} - Black fathers' "
           f"earnings are not more dispersed; their wage variance is smaller and their hours variance about the same.",
           f"- **Age profile (Section 1b).** Family-income IGE, sons 25-34: Black {ap('25-34', 'Black', 'lfam_s on lyp'):.3f}, "
           f"White {ap('25-34', 'White', 'lfam_s on lyp'):.3f}; 35-44: {ap('35-44', 'Black', 'lfam_s on lyp'):.3f} / "
           f"{ap('35-44', 'White', 'lfam_s on lyp'):.3f}; 45-55: {ap('45-55', 'Black', 'lfam_s on lyp'):.3f} / "
           f"{ap('45-55', 'White', 'lfam_s on lyp'):.3f}. Father-earnings IGE 25-34: {ap('25-34', 'Black', 'ly on f_ly'):.3f} / "
           f"{ap('25-34', 'White', 'ly on f_ly'):.3f}; 45-55: {ap('45-55', 'Black', 'ly on f_ly'):.3f} / "
           f"{ap('45-55', 'White', 'ly on f_ly'):.3f}. The son's ln wage on parental income: Black "
           f"{ap('25-34', 'Black', 'lw on lyp'):.3f} -> {ap('45-55', 'Black', 'lw on lyp'):.3f}, White "
           f"{ap('25-34', 'White', 'lw on lyp'):.3f} -> {ap('45-55', 'White', 'lw on lyp'):.3f} (25-34 -> 45-55); the son's "
           f"ln hours on parental income, 25-55: Black {ap('25-55', 'Black', 'lh on lyp'):.3f}, White "
           f"{ap('25-55', 'White', 'lh on lyp'):.3f}. **The gap is absent at 25-34 and opens after 35, entirely in "
           f"the wage component; the hours component works the other way.**",
           f"- **Purging shocks (Section 2, Lee-Solon childhood).** Gap, same children: all years "
           f"{pt['gap|earn_cs']:.3f}, clean years A {pt['gap|cleanA']:.3f}, clean years B {pt['gap|cleanB']:.3f}; "
           f"potential earnings (wage IGE) {pt['gap|pot']:.3f} vs earnings {pt['gap|earn']:.3f}. Change in the gap "
           f"(positive = smaller): clean A {b(L0, 'dgap|cleanA')}, clean B {b(L0, 'dgap|cleanB')}, potential "
           f"{b(L0, 'dgap|pot')}; family income, clean years vs all years {b(L0, 'dgap|fam_clean')}.",
           f"- **Instability (Section 3).** Share of years displaced or unemployed: fathers (childhood window) Black "
           f"{g('3 instability means', 'fathers, childhood', 'Black-White', 'sh_shock', 'black'):.3f} vs White "
           f"{g('3 instability means', 'fathers, childhood', 'Black-White', 'sh_shock', 'white'):.3f}; sons Black "
           f"{g('3 instability means', 'sons', 'Black-White', 'sh_shock', 'black'):.3f} vs White "
           f"{g('3 instability means', 'sons', 'Black-White', 'sh_shock', 'white'):.3f}. Transitory variance: fathers "
           f"{g('3 instability means', 'fathers, childhood', 'Black-White', 'vtr', 'black'):.3f} vs "
           f"{g('3 instability means', 'fathers, childhood', 'Black-White', 'vtr', 'white'):.3f}, sons "
           f"{g('3 instability means', 'sons', 'Black-White', 'vtr', 'black'):.3f} vs "
           f"{g('3 instability means', 'sons', 'Black-White', 'vtr', 'white'):.3f}. The race gap in instability "
           f"is in the sons' generation, not among the (father-present) fathers.",
           f"- **Education (Section 4a).** Son's education mediates "
           f"{1 - g('4a mediation', 'ln parental', 'Black', 'ly + educ') / g('4a mediation', 'ln parental', 'Black', 'ly + none'):.0%}"
           f" (Black) and "
           f"{1 - g('4a mediation', 'ln parental', 'White', 'ly + educ') / g('4a mediation', 'ln parental', 'White', 'ly + none'):.0%}"
           f" (White) of the earnings IGE on parental family income; the wage IGE on parental income is Black "
           f"{g('4a mediation', 'ln parental', 'Black', 'lw + none'):.3f}, White "
           f"{g('4a mediation', 'ln parental', 'White', 'lw + none'):.3f}, the hours IGE Black "
           f"{g('4a mediation', 'ln parental', 'Black', 'lh + none'):.3f}, White "
           f"{g('4a mediation', 'ln parental', 'White', 'lh + none'):.3f}.",
           f"- **Reliability (Section 5).** Childhood-mean reliability of the father's ln earnings: Black "
           f"{rr['ly', 'Black']:.3f}, White "
           f"{rr['ly', 'White']:.3f}; of family income Black "
           f"{rr['lfam', 'Black']:.3f}, White "
           f"{rr['lfam', 'White']:.3f}. Differential "
           f"attenuation is small.",
           f"- **Composition (Section 6).** Re-weighting White sons to the Black parental distribution closes "
           f"{b(L0, 'close|comp_fam_all')} of the family-income IGE gap and {b(L0, 'close|comp_earn')} of the "
           f"father-earnings IGE gap (ratios of noisy gaps, hence the s.e.; the composition term of Section 7, "
           f"{b(L0, 'gap|composition')} over 25-55 and {b(L4, 'gap|composition')} at 35-55, is the better-measured "
           f"version): the IGE is flatter in the lower part of the parental distribution, where Black families are "
           f"concentrated.",
           f"- **Decomposition (Section 7, sons, Lee-Solon controls, childhood window, ages 25-55).** Gap "
           f"{b(L0, 'gap|total')} = composition {b(L0, 'gap|composition')} + wage transmission "
           f"{b(L0, 'gap|wage_trans')} + hours / instability {b(L0, 'gap|hours_all')} (of which the hours share of the "
           f"father's earnings variance, the 'inflated denominator', {b(L0, 'gap|hours_share')}) + cross terms "
           f"{b(L0, 'gap|cross')}. Sons 35-55: gap {b(L4, 'gap|total')} = {b(L4, 'gap|composition')} + "
           f"{b(L4, 'gap|wage_trans')} + {b(L4, 'gap|hours_all')} + {b(L4, 'gap|cross')}. Lifetime design: gap "
           f"{b(L2, 'gap|total')} = {b(L2, 'gap|composition')} + {b(L2, 'gap|wage_trans')} + "
           f"{b(L2, 'gap|hours_all')} + {b(L2, 'gap|cross')}.", ""]
    hs = pt["gap|hours_share"] + pt["gap|wage_share"]
    p4 = BOOT[L4][0]
    hs4 = p4["gap|hours_share"] + p4["gap|wage_share"]
    out += ["**Assessment.** The Black-White IGE gap is a gap in the transmission of the price of labor - the hourly "
            "wage - and it builds up over the sons' careers. At 25-34 the IGEs are about equal; after 35 the White "
            "sons' wage keeps tracking their parents' income and the Black sons' wage does not. That is the pattern "
            "of differences in human capital accumulation, in returns to it, or in access to the jobs that pay for "
            "it - not of transitory shocks in measured income. Labor-market shocks are real and racially unequal, but "
            "they sit in the sons' generation and do not produce the gap in this accounting: (i) among father-present "
            "families, Black fathers' earnings are not noisier, their reliability ratio equals the White one, and the "
            "hours share of their earnings variance - the PI's 'inflated denominator' (wage-share + hours-share "
            f"terms) - accounts for {hs:.3f} of the {pt['gap|total']:.3f} gap over ages 25-55 and {hs4:.3f} of the "
            f"{p4['gap|total']:.3f} gap at 35-55, against {pt['gap|wage_trans']:.3f} / {p4['gap|wage_trans']:.3f} for "
            "wage transmission: present, but second order; (ii) Black sons' displacement, unemployment and "
            "zero-hours years are about twice the White rates and are more tied to parental income, so the hours "
            "channel RAISES the Black IGE (the son's hours IGE on parental income is larger for Black sons) and "
            "partly hides the wage gap at young ages; (iii) dropping shock years or using potential earnings leaves "
            "the gap where it is. Composition - Black families sit where the IGE is flatter - accounts for a "
            "sizeable but imprecise share (about 0.04-0.09 log points, a third to three fifths of the decomposed gap). Son's education mediates a third of the Black IGE and a "
            "quarter of the White IGE but does not close the gap. Caveats: father-present Black sons are under half "
            "of the benchmark sample (Section 0) and have a higher family-income IGE than all Black sons; wage = "
            "earnings / hours carries division bias; hours mix shocks, labor supply and search frictions; all "
            "splits are accounting identities, not causal effects.", ""]
    return out


def figure(BOOT):
    """Left: IGE by measure and race (95% bootstrap CI). Right: decomposition of the gap (sons, Lee-Solon)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    lab = CONFIGS[0][4]
    pt, se = BOOT[lab]
    ink, muted, grid = "#0b0b0b", "#52514e", "#e4e3df"
    col = {"Black": "#2a78d6", "White": "#eb6834"}
    M = [("earn", "Earnings (benchmark)"), ("cleanA", "Earnings, clean years A"), ("cleanB", "Earnings, clean years B"),
         ("fpot", "Earnings on father's potential"), ("pot", "Wage (potential earnings)"), ("hours", "Hours"),
         ("fam_fp", "Family income (13-19 mean)"), ("fam_clean", "Family income, clean years")]
    P = [("gap|total", "Gap (decomposed)"), ("gap|composition", "Composition"),
         ("gap|wage_trans", "Wage transmission"), ("gap|hours_all", "Hours / instability"),
         ("gap|cross", "Wage-hours cross terms")]
    fig, ax = plt.subplots(1, 2, figsize=(12, 5.2), gridspec_kw=dict(width_ratios=[1.15, 1]))
    fig.patch.set_facecolor("#fcfcfb")
    y = np.arange(len(M))[::-1]
    for j, race in enumerate(("Black", "White")):
        g = "B" if race == "Black" else "W"
        b = np.array([pt[f"{g}|{m}"] for m, _ in M])
        s = np.array([se[f"{g}|{m}"] for m, _ in M])
        ax[0].errorbar(b, y + (0.15 if j == 0 else -0.15), xerr=1.96 * s, fmt="o", ms=8, color=col[race],
                       ecolor=col[race], elinewidth=2, capsize=0, label=race, mec="#fcfcfb", mew=1.5)
    ax[0].set_yticks(y, [m[1] for m in M], color=ink)
    ax[0].axvline(0, color=muted, lw=1)
    ax[0].set_xlabel("Elasticity on the father's / parental measure (95% bootstrap CI)", color=muted)
    ax[0].set_title("Sons: IGE by measure (Lee-Solon, age 40)", color=ink, loc="left", fontsize=12)
    ax[0].legend(frameon=False, loc="upper right")
    yb = np.arange(len(P))[::-1]
    for j, (lb, nm, cc) in enumerate(((CONFIGS[0][4], "Sons 25-55", "#52514e"), (CONFIGS[4][4], "Sons 35-55", "#a3a29b"))):
        p_, s_ = BOOT[lb]
        bb = np.array([p_[k] for k, _ in P])
        ss = np.array([s_[k] for k, _ in P])
        yy = yb + (0.17 if j == 0 else -0.17)
        ax[1].barh(yy, bb, height=0.32, color=cc, edgecolor="#fcfcfb", lw=2, label=nm)
        ax[1].errorbar(bb, yy, xerr=1.96 * ss, fmt="none", ecolor=ink, elinewidth=1.2, capsize=0)
    ax[1].set_yticks(yb, [p[1] for p in P], color=ink)
    ax[1].axvline(0, color=muted, lw=1)
    ax[1].set_xlabel("Contribution to the gap (95% bootstrap CI)", color=muted)
    ax[1].legend(frameon=False, loc="lower left")
    ax[1].set_title("Sons: father-earnings IGE gap (Section 7)", color=ink, loc="left", fontsize=12)
    for a_ in ax:
        a_.set_facecolor("#fcfcfb")
        a_.grid(axis="x", color=grid, lw=0.8)
        a_.set_axisbelow(True)
        for sp in ("top", "right", "left"):
            a_.spines[sp].set_visible(False)
        a_.spines["bottom"].set_color(muted)
        a_.tick_params(colors=muted, length=0)
    fig.tight_layout()
    fig.savefig(OUT / "ige_decomposition.png", dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    main()
