r"""Shared search friction in two generations and the IGE (PI hypothesis, 2026-10-19).

THE HYPOTHESIS (PI): "Somewhere some pairs of father and son are suppressed: both of them find it hard to find a job,
and it shows in both of their earnings. Overall this impacts the general IGE." Write the son's outcome and the
measured parental income as
    y_son = beta x* - f_son + e,      x = x* - f_father,
with x* the father's friction-free income and f the search friction of each generation (same place, same networks,
same discrimination). Then Cov(y_son, x) = beta Var(x*) + Cov(f_son, f_father) and
    IGE = [beta Var(x*) + Cov(f_son, f_father)] / [Var(x*) + Var(f_father)]:
the friction the two generations share raises the measured IGE (numerator), the father's own friction lowers it
(denominator), independently of any transmission of skills. Friction should act through employment and hours, so the
earnings IGE (ln y = ln w + ln h) and the hourly-wage IGE should differ. 72.FrictionGenerations.py (T2-T5) asked whether
a friction in ONE generation shapes the profile; this script measures the part that needs BOTH.

DATA (read only; nothing person-level is written to tracked files)
  PSID son panel of 36.SameEmployerGrowthChecks.py's psid_build() (= 24.IGEDecomposition.py's child-year frame, via
  27 / 32), cached in data/shared_friction_sonpanel.pkl (git-ignored; delete to rebuild, ~40 s). Sons = male heads
  25-55 of Black or White parental households (race of the parental head at 16), every son-year (valid or not).
  x = lyp      ln parental family income, mean over the son's wave-ages 13-19 (6.IGEMain.py).
  lw, lh, ly   ln hourly wage, ln annual hours, ln annual earnings of a VALID year (24's bounds; ln y = ln w + ln h
               exactly, so on the same rows the earnings IGE = wage IGE + hours IGE, and so is every component below).
  ly0          ln earnings with every zero-hours year set to the 10th percentile of ln earnings of the son's race x
               five-year band (72's T2b rule applied to earnings); rows = valid or zero-hours years. It brings the
               extensive margin, where a search friction acts first, into the earnings IGE.
  Son-year friction flags (24.IGEDecomposition.py): disp (main displacement - closure or layoff / firing - dated t or
               t-1), unemp (hours unemployed > 0, or unemployed at any time in t, or laid off / looking at the
               following interview), zero (annual hours = 0); fr = max(disp, unemp, zero), a FRICTION YEAR.
  SON'S FRICTION (the mediator S): sb_disp, sb_unemp, sb_zero = the son's shares of his son-years in the current
               five-year band that are displaced / unemployed / zero hours (all his years in the band, valid or not);
               s_sh_disp, s_sh_unemp, s_sh_zero = the same over all his years 25-55 (24's career shares; variant A4c);
               s_fr = his share of friction years over all his years 25-55 (career).
  FATHER'S FRICTION (F): f_sh_disp, f_sh_unemp, f_sh_zero = the father's shares of the childhood-window years (income
               years when the son is 12-18) displaced / unemployed / with zero hours (24's person_measures over the
               father's head-years; father = male head of the son's family unit at 16). FH = 1 if the father has at
               least one such year in the window (49% of Black, 36% of White father-present sons).
  Place: fips17 = family-file state nearest age 17 (ages 14-20, waves 1976+; 72's state17); fips_cur = the son's own
               family-file state at each interview (data/husband_shocks_fam.pkl, waves 1976+); ur = state unemployment
               rate (data/state_shocks.pkl, LAUS / UKCPR, 1976-2024); ur_cur = ur of fips_cur in the son's income year;
               ur_win = mean ur of the son's family-file state over his childhood waves (wave-ages 13-19, income year
               wave - 1 >= 1976), the father's local labor market in the window.
  NLSY79 (Section F): men of the cross-sectional + supplemental samples (data/nlsy79_kids.pkl: ln parental income
               1979-81, lpinc_av), weeks worked in each calendar year (WKSWK-PCY; 70.RauhReplication.py's build of
               data/rauh_nlsy79.pkl), census region (4) of the round. Geocodes are restricted and not used.
DESIGNS (IGE by five-year band of the son's age = each band its own regression, single-age dummies, son-years in the
band, by race; opening = 45-49 minus 25-29; W - B adds variances, races are independent samples of 1968 families)
  A. DECOMPOSITION (Gelbach 2016, exact on one sample). In each race x band, on son-years with a valid wage of sons with
     the father's three window shares:
       base  y = b0 x + ages
       full  y = b x + gamma'S + theta'F + ages
       aux   F = d_F x + ages;   S = a x + C'F + ages   (so d_S = a + C'd_F, the omitted-variable identity)
     b0 = b + theta'd_F + gamma'a + gamma'C'd_F, exactly:
       father's friction, direct    theta'd_F    the father's friction lowers x and relates to the son's outcome at
                                                 equal son's friction (e.g. the lost income lowers what the son gets)
       son's friction, own          gamma'a      the son's friction falls with parental income beyond his father's
       SHARED FRICTION              gamma'C'd_F  the PI's term: the son's friction that follows his father's (C)
                                                 times the income the father's friction costs (d_F) times what the
                                                 son's friction costs his outcome (gamma) - needs both generations
       rest                         b            the IGE at equal friction in both generations
     Variants: own schooling as a control in every regression; the son's career shares as S; state-at-17 FE; the
     son's current-state FE (same sons as their no-FE baseline). Section A0: the son's friction alone (S only) on all sons and on father sons.
  B. SUPPRESSED PAIRS. FH (father had a friction year in the window) x SH (son's career friction share s_fr above the
     pooled two-thirds quantile of father-present sons). Cell shares; the concordance P(SH | FH) - P(SH | not FH); the
     IGE in each cell at 25-34 and 35-55 and the triple interaction (both high minus one-high minus other-high plus
     neither); the IGE by band with the suppressed (FH & SH) pairs left out, and as a placebo with the son-only
     high-friction sons (SH, not FH) left out; who the pairs are (South at 17, childhood-state unemployment, cohort,
     father's schooling, parental-income tercile). Conditioning on SH conditions on an outcome of the son: leaving out
     any low-outcome, low-income group flattens the slope, so B is descriptive of where the pairs are; A is the
     accounting.
  SUMMARY (top of the .md): A's shared term by race at 25-29 and 45-49, its share of the band IGE, its opening, and the
     gap share = (W - B) opening of the shared term / (W - B) opening of the IGE (also for R2 b_P of design E), for
     band and career measures of the son's friction.
  C. PLACE. (1) the son's friction year on the father's shares, then + ur_cur and ur_win, + state-at-17 FE, + current
     state x year FE (absorbed): how much of the persistence of friction is the local labor market; (2) the IGE profile
     with state-at-17 FE, current-state FE, current state x year FE, same sons; (3) A's shared component with place FE
     (variants above). Who are the suppressed pairs: shares in the South and in high-unemployment places, by period.
  D. AGE PROFILE: A's components by band and their opening, by race and W - B (the puzzle: White log-wage IGE 0.205 at
     25-29 -> 0.470 at 45-49, Black 0.148 -> 0.140).
  E. IDENTITY with measured pieces: P = the projection of x on F (with ages), x_perp = x - P, R2 = Var(P)/Var(x) (the
     father's friction share of the variance of parental income). Exactly (Frisch-Waugh)
       b0 = (1 - R2) b_clean + R2 b_P,   b_clean = IGE at equal father's friction = the IGE on x* if x* = x - P + const,
     and R2 b_P = Cov(y, P)/Var(x) = the PI's [Cov(f_son, f_father) - Cov(e, f_father)]/Var(x); A's shared term is the
     part of it that runs through the son's measured friction. The IGE without the shared friction = b0 - shared.
  F. NLSY79: share of weeks not worked in the calendar year (1 - weeks / 52) at 25-34 and 35-55 on ln parental income,
     by race, with round FE, then with region x round FE: does a regional labor market carry the son's friction
     gradient in parental income (no father friction measure in the NLSY79).
INFERENCE: regressions with analytic s.e. clustered by 1968 family (PSID) / 1979 household (NLSY79), CR1. Components,
openings, ratios and differences between specifications: cluster bootstrap of 1968 families within race (IGE_NBOOT
draws, default 200), normal p-values from the bootstrap s.e. (for ratios: half the 15.9-84.1 percentile range of the
draws, robust to draws with a denominator near zero; White and Black draws are independent and paired by index). Every estimate: coefficient (s.e.; p), *** p<0.01,
** p<0.05, * p<0.1. DESCRIPTIVE ACCOUNTING: friction years are outcomes of skill as well as of luck and place; nothing
here identifies a causal effect. Writes output/shared_friction.md and output/shared_friction.json (aggregates only).
"""
import importlib.util
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import DATA, OUT  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R72 = _load("s72", "72.FrictionGenerations.py")
fitc, star, state17 = R72.fitc, R72.star, R72.state17
BANDS = [(25, 29), (30, 34), (35, 39), (40, 44), (45, 49), (50, 55)]
BL = [f"{lo}-{hi}" for lo, hi in BANDS]
RACES = ("White", "Black")
SON = ["sb_disp", "sb_unemp", "sb_zero"]
FAT = ["f_sh_disp", "f_sh_unemp", "f_sh_zero"]
NBOOT = int(os.environ.get("IGE_NBOOT", 200))
SEED = 20261019
CACHE = DATA / "shared_friction_sonpanel.pkl"
RES = {}
LAB = {"lyp": "ln parental income (13-19 mean)", "sb_disp": "son's share of band years displaced",
       "sb_unemp": "son's share of band years unemployed", "sb_zero": "son's share of band years with zero hours",
       "f_sh_disp": "father's share of window years displaced", "f_sh_unemp": "father's share of window years unemployed",
       "f_sh_zero": "father's share of window years with zero hours", "ur_cur": "state unemployment rate, son's year (pp)",
       "ur_win": "state unemployment rate, childhood window (pp)", "educ": "son's years of schooling"}


# ================================================================ formatting
def pv(b, s):
    return 2 * (1 - norm.cdf(abs(b) / s)) if s and s > 0 and np.isfinite(s) else np.nan


def c(t, dec=3):
    if t is None or t[0] is None or not np.isfinite(t[0]):
        return ""
    b, s = t
    p = pv(b, s)
    ps = "p<0.001" if p < 0.001 else f"p={p:.3f}"
    return f"{b:.{dec}f}{star(p) if np.isfinite(p) else ''} ({s:.{dec}f}; {ps})"


# ================================================================ data
def load_panel():
    if CACHE.exists():
        r = pd.read_pickle(CACHE)
    else:
        r, *_ = R72.R36.psid_build()
        r.to_pickle(CACHE)
    r = r[r["race"].isin(RACES) & r["age"].between(25, 55)].copy()
    for v in ["lw", "lh", "ly", "lyp", "zero", "disp", "unemp", "shock", "educ", "age", "year", "wave", "int", "fam68",
              "birth_year", "s_sh_disp", "s_sh_unemp", "s_sh_zero"] + FAT + ["f_sh_shock"]:
        r[v] = pd.to_numeric(r[v], errors="coerce")
    r["valid"] = r["valid"].astype(bool)
    r = r.sort_values(["pid", "wave"]).reset_index(drop=True)
    r["band"] = pd.cut(r["age"], [24, 29, 34, 39, 44, 49, 55], labels=False).astype(int)
    r["fr"] = np.fmax(np.fmax(r["disp"].fillna(0), r["unemp"].fillna(0)), r["zero"].fillna(0))
    g = r.groupby(["pid", "band"])
    for v in ("disp", "unemp", "zero"):
        r[f"sb_{v}"] = g[v].transform("mean")
    r["sb_fr"] = g["fr"].transform("mean")
    r["s_fr"] = r.groupby("pid")["fr"].transform("mean")
    r["FH"] = ((r["f_sh_shock"] > 0) | (r["f_sh_zero"] > 0)).astype(float).where(r[FAT].notna().all(axis=1))
    for v in ("lw", "lh", "ly"):
        r[v] = r[v].where(r["valid"])
    p10 = r[r["valid"]].groupby(["race", "band"])["ly"].quantile(0.10)
    imp = pd.Series([p10.get((a, b), np.nan) for a, b in zip(r["race"], r["band"])], index=r.index)
    r["ly0"] = r["ly"].where(r["valid"], imp.where(r["zero"] == 1))
    r["educ"] = r["educ"].where(r["educ"].between(0, 20))
    return r


def attach_place(r):
    r = state17(r)
    hs = pd.read_pickle(DATA / "husband_shocks_fam.pkl")[["wave", "int", "fips"]].drop_duplicates(["wave", "int"])
    r = r.merge(hs.rename(columns={"fips": "fips_cur"}), on=["wave", "int"], how="left")
    ss = pd.read_pickle(DATA / "state_shocks.pkl")[["fips", "year", "ur"]].dropna()
    ur = ss.set_index(["fips", "year"])["ur"]
    r["ur_cur"] = [ur.get((f, y), np.nan) if np.isfinite(f) else np.nan
                   for f, y in zip(r["fips_cur"].astype(float), r["year"])]
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    ch = py[py["child"] & py["age"].between(13, 19) & (py["wave"] >= 1977) & py["pid"].isin(r["pid"])][
        ["pid", "wave", "int"]]
    ch = ch.merge(hs, on=["wave", "int"], how="inner").dropna(subset=["fips"])
    ch["ur"] = [ur.get((f, y), np.nan) for f, y in zip(ch["fips"].astype(float), ch["wave"] - 1)]
    w = ch.groupby("pid")["ur"].mean()
    r["ur_win"] = r["pid"].map(w)
    r["south"] = r["fips17"].isin([1, 5, 10, 11, 12, 13, 21, 22, 24, 28, 37, 40, 45, 47, 48, 51, 54]).astype(float).where(
        r["fips17"].notna())
    r["stayer"] = (r["fips_cur"] == r["fips17"]).astype(float).where(r["fips_cur"].notna() & r["fips17"].notna())
    r["sy"] = (r["fips_cur"] * 10000 + r["year"]).where(r["fips_cur"].notna())
    return r


# ================================================================ linear algebra
def dummies(v):
    return pd.get_dummies(pd.Series(v).astype(int), drop_first=True).to_numpy(float)


def wls(X, Y, sw):
    return np.linalg.lstsq(X * sw[:, None], Y * sw[:, None], rcond=None)[0]


def demean(M, grp, w):
    """subtract weighted group means of every column of M (one fixed effect absorbed)."""
    g = pd.factorize(grp)[0]
    sw = np.bincount(g, weights=w)
    out = M.copy()
    for j in range(M.shape[1]):
        mu = np.bincount(g, weights=M[:, j] * w) / np.where(sw > 0, sw, 1)
        out[:, j] = M[:, j] - mu[g]
    return out


# ================================================================ A. decomposition
def band_cells(d, ys, ctrl=(), fe=None, son=SON, fat=FAT):
    """per band: arrays of one race's son-years (x, S, F, Y, controls A = single-age dummies + ctrl + fe + 1, clusters)."""
    need = ys + ["lyp", "age", "fam68"] + list(son) + list(fat) + list(ctrl) + ([fe] if fe else [])
    d = d.dropna(subset=need)
    cells = {}
    for k in range(6):
        z = d[d["band"] == k]
        if len(z) < 50:
            continue
        A = [dummies(z["age"])] + [z[list(ctrl)].to_numpy(float)] if ctrl else [dummies(z["age"])]
        if fe:
            A.append(dummies(z[fe]))
        A.append(np.ones((len(z), 1)))
        cells[k] = {"x": z["lyp"].to_numpy(float), "S": z[list(son)].to_numpy(float), "F": z[list(fat)].to_numpy(float),
                    "Y": z[ys].to_numpy(float), "A": np.column_stack(A), "cl": z["fam68"].to_numpy(),
                    "pid": z["pid"].to_numpy()}
    return cells, d


def comps(cell, w):
    """Gelbach split of b0 (one band), for every outcome column of Y; also the identity pieces of design E."""
    x, S, F, Y, A = cell["x"], cell["S"], cell["F"], cell["Y"], cell["A"]
    keep = w > 0
    x, S, F, Y, A, w = x[keep], S[keep], F[keep], Y[keep], A[keep], w[keep]
    sw = np.sqrt(w)
    m, ns, nf = Y.shape[1], S.shape[1], F.shape[1]
    out = {}
    X0 = np.column_stack([x, A])
    B0 = wls(X0, np.column_stack([Y, F, S]), sw)
    b0, dF, dS = B0[0, :m], B0[0, m:m + nf], B0[0, m + nf:]
    XS = np.column_stack([x, S, A])
    BSo = wls(XS, Y, sw)
    son_only = BSo[1:1 + ns].T @ dS
    if nf:
        XF = np.column_stack([x, F, A])
        BF = wls(XF, np.column_stack([Y, S]), sw)
        bcl, a_, C = BF[0, :m], BF[0, m:], BF[1:1 + nf, m:]
        X1 = np.column_stack([x, S, F, A])
        B1 = wls(X1, Y, sw)
        bfull, gam, th = B1[0], B1[1:1 + ns], B1[1 + ns:1 + ns + nf]
        fat_dir, son_own, shared = th.T @ dF, gam.T @ a_, gam.T @ (C.T @ dF)
        # identity: R2 = Var(P)/Var(x~), x~ = x net of ages, P = projection of x~ on F~
        xa = x - A @ wls(A, x[:, None], sw)[:, 0]
        xp = x - np.column_stack([F, A]) @ wls(np.column_stack([F, A]), x[:, None], sw)[:, 0]
        R2 = 1 - np.sum(w * xp ** 2) / np.sum(w * xa ** 2)
        for j in range(m):
            out[j] = {"b0": b0[j], "fat": fat_dir[j], "son_own": son_own[j], "shared": shared[j], "rest": bfull[j],
                      "son_only": son_only[j], "R2": R2, "b_clean": bcl[j], "R2bP": b0[j] - (1 - R2) * bcl[j],
                      "no_shared": b0[j] - shared[j]}
    else:
        for j in range(m):
            out[j] = {"b0": b0[j], "son_only": son_only[j], "rest": BSo[0, j]}
    return out


def boot_decomp(d, ys, ctrl=(), fe=None, fat=FAT, son=SON, nboot=NBOOT, tag=""):
    """point estimates and cluster-bootstrap s.e. of every component, by race, band, opening and W - B."""
    res = {}
    draws = {}
    rng = np.random.default_rng(SEED)
    nsons = {}
    for race in RACES:
        cells, dd = band_cells(d[d["race"] == race], ys, ctrl, fe, son=son, fat=fat)
        nsons[race] = (int(dd["pid"].nunique()), int(len(dd)))
        cl_all = pd.factorize(dd["fam68"])[0]
        cmap = dict(zip(dd["fam68"], cl_all))
        G = cl_all.max() + 1
        for cv in cells.values():
            cv["ci"] = np.array([cmap[f] for f in cv["cl"]])
        pt = {k: comps(cv, np.ones(len(cv["x"]))) for k, cv in cells.items()}
        bs = []
        for _ in range(nboot):
            cnt = np.bincount(rng.integers(0, G, G), minlength=G).astype(float)
            bs.append({k: comps(cv, cnt[cv["ci"]]) for k, cv in cells.items()})
        res[race], draws[race] = pt, bs
    out = {"n": nsons}
    for j, y in enumerate(ys):
        keys = list(res["White"][0][j].keys())
        oy = {}
        for kk in keys:
            row = {}
            for race in RACES:
                pt, bs = res[race], draws[race]
                ent = {}
                for k in pt:
                    vals = np.array([b[k][j][kk] for b in bs])
                    ent[k] = (float(pt[k][j][kk]), float(np.nanstd(vals, ddof=1)), vals)
                if 0 in pt and 4 in pt:
                    vals = np.array([b[4][j][kk] - b[0][j][kk] for b in bs])
                    ent["open"] = (float(pt[4][j][kk] - pt[0][j][kk]), float(np.nanstd(vals, ddof=1)), vals)
                row[race] = ent
            row["W-B"] = {k: (row["White"][k][0] - row["Black"][k][0], float(np.hypot(row["White"][k][1],
                                                                                       row["Black"][k][1])), None)
                          for k in row["White"] if k in row["Black"]}
            oy[kk] = row
        out[y] = oy
    return out


def rse(v):
    """normal-equivalent s.e. of a ratio's bootstrap draws: half the 15.9-84.1 percentile range (robust to draws
    with a denominator near zero)."""
    v = v[np.isfinite(v)]
    return float((np.percentile(v, 84.13) - np.percentile(v, 15.87)) / 2)


def ratio_boot(o, y, num, den):
    """num / den by race x band with bootstrap s.e. (same draws)."""
    row = {}
    for race in RACES:
        ent = {}
        for k in o[y][num][race]:
            a, b = o[y][num][race][k], o[y][den][race][k]
            ent[k] = (a[0] / b[0], rse(a[2] / b[2]), None)
        row[race] = ent
    return row


def gap_share(o, y, num="shared", den="b0"):
    """(W - B) opening of num / (W - B) opening of den, bootstrap s.e. (independent W and B draws paired by index)."""
    nw, nb = o[y][num]["White"]["open"], o[y][num]["Black"]["open"]
    dw, db = o[y][den]["White"]["open"], o[y][den]["Black"]["open"]
    pt = (nw[0] - nb[0]) / (dw[0] - db[0])
    return pt, rse((nw[2] - nb[2]) / (dw[2] - db[2]))


def summary(md, specs):
    md += ["## Summary: the shared friction component (gamma'C'd_F)", "",
           "Father-present sons. Shared = the son's friction that follows his father's x the parental income the "
           "father's friction costs x what the son's friction costs his outcome. Share = shared / IGE in the band. Gap "
           "share = (W - B) opening of the shared term / (W - B) opening of the IGE. Bootstrap s.e.", "",
           "| outcome | son's friction measured over | race | IGE 25-29 | shared 25-29 | share 25-29 | IGE 45-49 | shared "
           "45-49 | share 45-49 | opening of IGE | opening of shared |", "|---" * 11 + "|"]
    for lab, frame, o, y in specs:
        rt = ratio_boot(o, y, "shared", "b0")
        for race in RACES + ("W-B",):
            b, sh = o[y]["b0"][race], o[y]["shared"][race]
            r0 = c(rt[race][0][:2]) if race in rt else ""
            r4 = c(rt[race][4][:2]) if race in rt else ""
            md.append(f"| {lab} | {frame} | {race} | {c(b[0][:2])} | {c(sh[0][:2])} | {r0} | {c(b[4][:2])} | "
                      f"{c(sh[4][:2])} | {r4} | {c(b['open'][:2])} | {c(sh['open'][:2])} |")
        g = gap_share(o, y)
        md.append(f"| {lab} | {frame} | gap share | {c(g)} |" + " |" * 7)
        RES[f"summary|{lab}|{frame}|gap_share"] = list(g)
        g2 = gap_share(o, y, num="R2bP")
        md.append(f"| {lab} | {frame} | gap share of R2 b_P (all of the father's friction-predicted income) | "
                  f"{c(g2)} |" + " |" * 7)
        RES[f"summary|{lab}|{frame}|gap_share_R2bP"] = list(g2)
    md.append("")


COMP_ROWS = [("b0", "IGE (base)"), ("fat", "father's friction, direct (theta'd_F)"),
             ("son_own", "son's friction, beyond his father's (gamma'a)"),
             ("shared", "SHARED friction (gamma'C'd_F)"), ("rest", "rest: IGE at equal friction (b)")]


def comp_table(md, title, o, y, rows=COMP_ROWS, note="", store=""):
    md += [f"#### {title}", ""] + ([note, ""] if note else [])
    md += ["| component | race | " + " | ".join(BL) + " | opening 45-49 - 25-29 |", "|---" * 9 + "|"]
    for kk, lab in rows:
        for race in RACES + ("W-B",):
            e = o[y][kk][race]
            md.append(f"| {lab} | {race} | " + " | ".join(c(e.get(k)[:2]) if k in e else "" for k in range(6))
                      + f" | {c(e['open'][:2]) if 'open' in e else ''} |")
            RES[f"{store}|{y}|{kk}|{race}"] = {str(k): [v[0], v[1]] for k, v in e.items()}
    md += [f"Sons / son-years: White {o['n']['White'][0]:,} / {o['n']['White'][1]:,}; Black "
           f"{o['n']['Black'][0]:,} / {o['n']['Black'][1]:,}.", ""]


# ================================================================ regressions with analytic clustered s.e.
def reg(d, y, xs, cl="fam68", fe=(), absorb=None, age_dummies=True):
    z = d.dropna(subset=[y] + list(xs) + [cl] + list(fe) + ([absorb] if absorb else []) + ["age"])
    parts = [z[list(xs)].to_numpy(float)]
    if age_dummies:
        parts.append(dummies(z["age"]))
    for f in fe:
        parts.append(dummies(z[f]))
    X = np.column_stack(parts)
    yv = z[y].to_numpy(float)
    if absorb:
        M = demean(np.column_stack([yv, X]), z[absorb].to_numpy(), np.ones(len(z)))
        yv, X = M[:, 0], M[:, 1:]
        X = X[:, np.abs(X).sum(axis=0) > 1e-9]
        XtXi = np.linalg.pinv(X.T @ X)
        b = XtXi @ X.T @ yv
        u = yv - X @ b
        S = pd.DataFrame(u[:, None] * X).groupby(z[cl].to_numpy()).sum().to_numpy()
        G, (n, k) = S.shape[0], X.shape
        V = XtXi @ (S.T @ S) @ XtXi * G / (G - 1) * (n - 1) / (n - k)
    else:
        b, V = fitc(X, yv, z[cl].to_numpy())
    return {v: (float(b[i]), float(np.sqrt(V[i, i]))) for i, v in enumerate(xs)}, len(z), z["pid"].nunique() \
        if "pid" in z else len(z), z[cl].nunique(), (b, V)


def reg_table(md, title, cols, rows, panels, note=""):
    """cols = [(header, fn(sample) -> (coef dict, n, sons, clusters))]; panels = [(label, sample)]."""
    md += [f"#### {title}", ""] + ([note, ""] if note else [])
    md += ["| | " + " | ".join(f"({i + 1}) {h}" for i, (h, _) in enumerate(cols)) + " |", "|---" * (len(cols) + 1) + "|"]
    for plab, samp in panels:
        md.append(f"| **{plab}** |" + " |" * len(cols))
        out = [fn(samp) for _, fn in cols]
        for v, lab in rows:
            md.append(f"| {lab} | " + " | ".join(c(o[0].get(v)) if v in o[0] else "" for o in out) + " |")
        md.append("| N obs / sons / clusters | " + " | ".join(f"{o[1]:,} / {o[2]:,} / {o[3]:,}" for o in out) + " |")
        for i, (h, _) in enumerate(cols):
            RES[f"{title}|{plab}|({i + 1}) {h}"] = {k: list(v) for k, v in out[i][0].items()}
    md.append("")


def profile(d, y, x="lyp", fe=None, absorb=None, ctrl=()):
    """IGE by band (band-specific slopes, single-age dummies; fe dummies / absorbed FE common across bands)."""
    out = {}
    need = [y, x, "age", "fam68"] + list(ctrl) + ([fe] if fe else []) + ([absorb] if absorb else [])
    d = d.dropna(subset=need)
    for race in RACES:
        z = d[d["race"] == race]
        B = pd.get_dummies(z["band"]).astype(float)
        cols = [B[k].to_numpy() * z[x].to_numpy(float) for k in B.columns]
        names = [f"x{k}" for k in B.columns]
        for cc in ctrl:
            cols += [B[k].to_numpy() * z[cc].to_numpy(float) for k in B.columns]
            names += [f"{cc}{k}" for k in B.columns]
        parts = [np.column_stack(cols), dummies(z["age"])]
        if fe:
            parts.append(dummies(z[fe]))
        X = np.column_stack(parts)
        yv = z[y].to_numpy(float)
        if absorb:
            M = demean(np.column_stack([yv, X]), z[absorb].to_numpy(), np.ones(len(z)))
            yv, X = M[:, 0], M[:, 1:]
            nz = np.abs(X).sum(axis=0) > 1e-9
            idx_keep = np.where(nz)[0]
            X = X[:, nz]
            XtXi = np.linalg.pinv(X.T @ X)
            b_ = XtXi @ X.T @ yv
            u = yv - X @ b_
            S = pd.DataFrame(u[:, None] * X).groupby(z["fam68"].to_numpy()).sum().to_numpy()
            G, (n, kk) = S.shape[0], X.shape
            V_ = XtXi @ (S.T @ S) @ XtXi * G / (G - 1) * (n - 1) / (n - kk)
            b = np.full(len(nz), np.nan)
            b[idx_keep] = b_
            V = np.full((len(nz), len(nz)), np.nan)
            V[np.ix_(idx_keep, idx_keep)] = V_
        else:
            b, V = fitc(X, yv, z["fam68"].to_numpy())
        idx = {n: i for i, n in enumerate(names)}
        sl = {k: (float(b[idx[f"x{k}"]]), float(np.sqrt(V[idx[f"x{k}"], idx[f"x{k}"]]))) for k in range(6)
              if f"x{k}" in idx}
        op = None
        if "x0" in idx and "x4" in idx:
            i0, i4 = idx["x0"], idx["x4"]
            op = (float(b[i4] - b[i0]), float(np.sqrt(V[i4, i4] + V[i0, i0] - 2 * V[i4, i0])))
        out[race] = {"bands": sl, "open": op, "n_sons": int(z["pid"].nunique()), "n": int(len(z))}
    W, Bk = out["White"], out["Black"]
    out["W-B"] = {"bands": {k: (W["bands"][k][0] - Bk["bands"][k][0], float(np.hypot(W["bands"][k][1],
                                                                                     Bk["bands"][k][1])))
                            for k in W["bands"] if k in Bk["bands"]},
                  "open": (W["open"][0] - Bk["open"][0], float(np.hypot(W["open"][1], Bk["open"][1])))
                  if W["open"] and Bk["open"] else None}
    return out


def prof_table(md, title, specs, note=""):
    md += [f"#### {title}", ""] + ([note, ""] if note else [])
    md += ["| specification | race | " + " | ".join(BL) + " | opening 45-49 - 25-29 | sons |", "|---" * 10 + "|"]
    for lab, o in specs:
        RES[f"{title}|{lab}"] = o
        for race in RACES + ("W-B",):
            md.append(f"| {lab} | {race} | " + " | ".join(c(o[race]["bands"].get(k)) for k in range(6))
                      + f" | {c(o[race]['open'])} | {o[race].get('n_sons', '')} |")
    md.append("")


# ================================================================ B. suppressed pairs
def boot_drop(d, y, mask_col, nboot=NBOOT):
    """IGE by band on all sons vs leaving out the rows with mask_col == 1; bootstrap of families within race."""
    rng = np.random.default_rng(SEED + 1)
    out = {}
    for race in RACES:
        z = d[(d["race"] == race)].dropna(subset=[y, "lyp", mask_col])
        cl = pd.factorize(z["fam68"])[0]
        G = cl.max() + 1
        cells = {}
        for k in range(6):
            q = z[z["band"] == k]
            ii = np.where((z["band"] == k).to_numpy())[0]
            cells[k] = (np.column_stack([q["lyp"].to_numpy(float), dummies(q["age"]), np.ones(len(q))]),
                        q[y].to_numpy(float), q[mask_col].to_numpy(float), cl[ii])

        def est(cnt):
            o = {}
            for k, (X, yv, mk, cc) in cells.items():
                w = cnt[cc]
                wa = w
                wb = w * (mk != 1)
                ba = wls(X[wa > 0], yv[wa > 0, None], np.sqrt(wa[wa > 0]))[0, 0]
                bb = wls(X[wb > 0], yv[wb > 0, None], np.sqrt(wb[wb > 0]))[0, 0]
                o[k] = (ba, bb, ba - bb)
            o["open"] = tuple(o[4][i] - o[0][i] for i in range(3))
            return o
        pt = est(np.ones(G))
        bs = [est(np.bincount(rng.integers(0, G, G), minlength=G).astype(float)) for _ in range(nboot)]
        out[race] = {k: [(pt[k][i], float(np.std([b[k][i] for b in bs], ddof=1)), np.array([b[k][i] for b in bs]))
                         for i in range(3)] for k in pt}
        out[race]["share_rows"] = float((z[mask_col] == 1).mean())
    out["W-B"] = {k: [(out["White"][k][i][0] - out["Black"][k][i][0],
                       float(np.hypot(out["White"][k][i][1], out["Black"][k][i][1])), None) for i in range(3)]
                  for k in list(range(6)) + ["open"]}
    return out


# ================================================================ main
def main():
    md = ["# Shared search friction in two generations and the IGE (PI hypothesis)", "",
          "Built by `73.SharedFriction.py` (2026-10-19); every variable and design is defined in its docstring. PSID "
          "sons 25-55; estimate (s.e.; p), *** p<0.01, ** p<0.05, * p<0.1; s.e. clustered by 1968 family (analytic "
          f"CR1 for regressions; {NBOOT} cluster-bootstrap draws of 1968 families within race for components, "
          "openings, ratios and differences). Opening = 45-49 minus 25-29. **Descriptive accounting.**", ""]
    r = load_panel()
    r = attach_place(r)
    fs = r[r[FAT].notna().all(axis=1)].copy()             # father-present sons with the father's window shares
    one = r.drop_duplicates("pid")
    onef = fs.drop_duplicates("pid")
    # ------------------------------------------------ 0. samples and friction rates
    md += ["## 0. Samples and friction rates", "",
           "| race | sons | with father's window shares | son-years / with a valid wage | son's friction years: displaced "
           "/ unemployed / zero hours / any (share of son-years) | father's window shares: displaced / unemployed / "
           "zero hours | fathers with a friction year (FH) | sons with a state at 17 / living in it |",
           "|---|---|---|---|---|---|---|---|"]
    for race in RACES:
        q, qo, qf = r[r.race == race], one[one.race == race], onef[onef.race == race]
        md.append(f"| {race} | {len(qo):,} | {len(qf):,} ({len(qf) / len(qo):.0%}) | {len(q):,} / {int(q['lw'].notna().sum()):,} | "
                  f"{q['disp'].mean():.3f} / {q['unemp'].mean():.3f} / {q['zero'].mean():.3f} / {q['fr'].mean():.3f} | "
                  f"{qf['f_sh_disp'].mean():.3f} / {qf['f_sh_unemp'].mean():.3f} / {qf['f_sh_zero'].mean():.3f} | "
                  f"{qf['FH'].mean():.3f} | {qo['fips17'].notna().sum():,} / {q['stayer'].mean():.3f} of son-years |")
        RES[f"0|{race}"] = {"sons": len(qo), "father_sons": len(qf), "fr": float(q["fr"].mean()),
                            "FH": float(qf["FH"].mean())}
    md.append("")
    md.append("<<SUMMARY>>")
    # ------------------------------------------------ A1. pooled regressions (one regression per column)
    md += ["## A. How much of the IGE is shared friction: decomposition by band", "",
           "### A1. The links of the chain, sons 25-55 pooled (single-age dummies)", ""]
    v = fs[fs["lw"].notna()]
    allx = ["lyp"] + SON + FAT

    def col(y, xs):
        return lambda s: reg(s, y, xs)[:4]
    reg_table(md, "A1a. Son's outcome on parental income, then with both generations' friction (valid years, "
                  "father-present sons)",
              [("ln wage", col("lw", ["lyp"])), ("ln wage", col("lw", allx)), ("ln hours", col("lh", ["lyp"])),
               ("ln hours", col("lh", allx)), ("ln earnings", col("ly", ["lyp"])), ("ln earnings", col("ly", allx))],
              [(x_, LAB[x_]) for x_ in allx], [(rr, v[v.race == rr]) for rr in RACES],
              note="Son's shares are over his years in the current five-year band; father's over the childhood window.")
    reg_table(md, "A1b. The father's friction and parental income; the son's friction on his father's (valid years, "
                  "father-present sons)",
              [("father's share displaced", col("f_sh_disp", ["lyp"])),
               ("father's share unemployed", col("f_sh_unemp", ["lyp"])),
               ("father's share zero hours", col("f_sh_zero", ["lyp"])),
               ("son's share displaced", col("sb_disp", ["lyp"] + FAT)),
               ("son's share unemployed", col("sb_unemp", ["lyp"] + FAT)),
               ("son's share zero hours", col("sb_zero", ["lyp"] + FAT))],
              [(x_, LAB[x_]) for x_ in ["lyp"] + FAT], [(rr, v[v.race == rr]) for rr in RACES],
              note="Columns (1)-(3) are d_F (person-year weighted, the weights of the IGE); columns (4)-(6) are a "
                   "(row 1) and C (rows 2-4): the son's friction that follows his father's at equal parental income.")
    # ------------------------------------------------ A2. decomposition by band
    print("A2 ...", flush=True)
    oA = boot_decomp(fs[fs["lw"].notna()], ["lw", "lh", "ly"], tag="A")
    md += ["### A2. Gelbach split of the IGE by band (father-present sons, valid years)", "",
           "b0 = father's friction direct + son's friction beyond his father's + SHARED + rest, exactly; ln earnings = "
           "ln wage + ln hours row by row.", ""]
    for y, lab in (("lw", "ln hourly wage"), ("lh", "ln annual hours"), ("ly", "ln annual earnings")):
        comp_table(md, f"A2 {lab}", oA, y, store="A2")
    for y in ("lw", "ly"):
        rt = ratio_boot(oA, y, "shared", "b0")
        md += [f"Shared friction as a share of the {y} IGE: " + "; ".join(
            f"{rr} " + ", ".join(f"{BL[k]} {c(rt[rr][k][:2])}" for k in range(6) if k in rt[rr]) for rr in RACES), ""]
        RES[f"A2|{y}|shared/b0"] = {rr: {str(k): list(rt[rr][k][:2]) for k in rt[rr]} for rr in RACES}
    print("A3 ...", flush=True)
    vz = fs[fs["ly0"].notna()]
    oZ = boot_decomp(vz, ["ly0"], tag="Z")
    comp_table(md, "A3 ln annual earnings with zero-hours years at the race x band 10th percentile (valid and zero-hours "
                   "years)", oZ, "ly0", store="A3")
    rt = ratio_boot(oZ, "ly0", "shared", "b0")
    md += ["Shared friction as a share of this IGE: " + "; ".join(
        f"{rr} " + ", ".join(f"{BL[k]} {c(rt[rr][k][:2])}" for k in range(6) if k in rt[rr]) for rr in RACES), ""]
    # ------------------------------------------------ A0. son's friction alone, all sons vs father sons
    print("A0 ...", flush=True)
    oS_all = boot_decomp(r[r["lw"].notna()], ["lw", "ly"], fat=[], tag="S")
    oS_fs = oA
    md += ["### A0. The son's friction alone (S only): all sons vs father-present sons", "",
           "b0 = son's friction (gamma~'d_S, from y on x and S) + rest. With the father measured (A2) this term splits "
           "into the son's own part, the shared part and a re-allocation between them.", ""]
    rows0 = [("b0", "IGE (base)"), ("son_only", "son's friction, total (S only)")]
    for y, lab in (("lw", "ln hourly wage"), ("ly", "ln annual earnings")):
        comp_table(md, f"A0 {lab}, all sons", oS_all, y, rows=rows0, store="A0all")
        comp_table(md, f"A0 {lab}, father-present sons", oS_fs, y, rows=rows0, store="A0fs")
    # ------------------------------------------------ A4. variants: schooling, place FE
    print("A4 ...", flush=True)
    md += ["### A4. The shared component at equal schooling and within place", ""]
    rowsV = [("b0", "IGE (base)"), ("shared", "SHARED friction"), ("fat", "father's friction, direct"),
             ("son_own", "son's friction, beyond his father's")]
    oE = boot_decomp(fs[fs["lw"].notna() & fs["educ"].notna()], ["lw", "ly"], ctrl=["educ"])
    comp_table(md, "A4a ln hourly wage, own schooling in every regression", oE, "lw", rows=rowsV, store="A4educ")
    comp_table(md, "A4a ln annual earnings, own schooling in every regression", oE, "ly", rows=rowsV, store="A4educ")
    oC = boot_decomp(fs[fs["lw"].notna()], ["lw", "ly"], son=["s_sh_disp", "s_sh_unemp", "s_sh_zero"])
    comp_table(md, "A4c ln hourly wage, son's friction = his career shares (25-55) instead of his band shares", oC, "lw",
               rows=rowsV, store="A4career")
    comp_table(md, "A4c ln annual earnings, son's friction = his career shares (25-55)", oC, "ly", rows=rowsV,
               store="A4career")
    sm = []
    summary(sm, [("ln hourly wage", "band", oA, "lw"), ("ln annual earnings", "band", oA, "ly"), ("ln earnings incl. zero-hours years", "band", oZ, "ly0"),
                 ("ln hourly wage", "career", oC, "lw"), ("ln annual earnings", "career", oC, "ly")])
    i_ = md.index("<<SUMMARY>>")
    md[i_:i_ + 1] = sm
    ps = fs[fs["lw"].notna() & fs["fips17"].notna() & fs["fips_cur"].notna()]
    oP0 = boot_decomp(ps, ["lw", "ly"])
    oP1 = boot_decomp(ps, ["lw", "ly"], fe="fips17")
    oP2 = boot_decomp(ps, ["lw", "ly"], fe="fips_cur")
    for y, lab in (("lw", "ln hourly wage"), ("ly", "ln annual earnings")):
        comp_table(md, f"A4b {lab}, sons with a state at 17 and a current state: no FE", oP0, y, rows=rowsV,
                   store="A4p0")
        comp_table(md, f"A4b {lab}, same sons: state-at-17 FE in every regression", oP1, y, rows=rowsV, store="A4p17")
        comp_table(md, f"A4b {lab}, same sons: son's current-state FE in every regression", oP2, y, rows=rowsV,
                   store="A4pcur")
    # ------------------------------------------------ E. identity
    md += ["## E. The identity with measured pieces", "",
           "b0 = (1 - R2) b_clean + R2 b_P exactly; R2 = share of the variance of parental income (net of ages) "
           "predicted by the father's three window shares; R2 b_P = Cov(y, P)/Var(x) (the PI's [Cov(f_son, f_father) - "
           "Cov(e, f_father)]/Var(x)); 'IGE without shared friction' = b0 - SHARED.", ""]
    rowsE = [("b0", "IGE (base)"), ("R2", "R2 = Var(P)/Var(x)"), ("b_clean", "b_clean: IGE at equal father's friction"),
             ("R2bP", "R2 b_P: through the friction-predicted part of parental income"),
             ("shared", "of which SHARED (through the son's friction)"), ("no_shared", "IGE without the shared friction")]
    for y, lab in (("lw", "ln hourly wage"), ("ly", "ln annual earnings")):
        comp_table(md, f"E {lab}", oA, y, rows=rowsE, store="E")
    comp_table(md, "E ln annual earnings incl. zero-hours years", oZ, "ly0", rows=rowsE, store="E0")
    # ------------------------------------------------ B. suppressed pairs
    print("B ...", flush=True)
    md += ["## B. Where are the suppressed pairs?", ""]
    thr = float(onef["s_fr"].quantile(2 / 3))
    fs["SH"] = (fs["s_fr"] > thr).astype(float)
    fs["HH"] = ((fs["FH"] == 1) & (fs["SH"] == 1)).astype(float)
    onef = fs.drop_duplicates("pid")
    md += [f"SH = son's career share of friction years (displaced, unemployed or zero hours, 25-55) above {thr:.3f}, the "
           "two-thirds quantile of father-present sons (both races); FH = father had at least one friction year in the "
           "window; suppressed pair = FH and SH.", "",
           "| race | sons | neither | father only | son only | both (suppressed pair) | P(SH given FH) | P(SH given not FH) |",
           "|---|---|---|---|---|---|---|---|"]
    for race in RACES:
        q = onef[onef.race == race]
        cells = {(f, s): float(((q.FH == f) & (q.SH == s)).mean()) for f in (0, 1) for s in (0, 1)}
        md.append(f"| {race} | {len(q):,} | {cells[(0, 0)]:.3f} | {cells[(1, 0)]:.3f} | {cells[(0, 1)]:.3f} | "
                  f"{cells[(1, 1)]:.3f} | {q.loc[q.FH == 1, 'SH'].mean():.3f} | {q.loc[q.FH == 0, 'SH'].mean():.3f} |")
        RES[f"B0|{race}"] = {f"{f}{s}": v_ for (f, s), v_ in cells.items()}
    md.append("")
    onef = onef.assign(age=onef["birth_year"] * 0 + 40)       # son-level regressions: no age dummies (constant)
    sl = lambda y, xs: (lambda s: reg(s, y, xs, age_dummies=False)[:4])   # noqa: E731
    reg_table(md, "B1. Concordance: the son's high friction on the father's (one row per son)",
              [("son high friction SH", sl("SH", ["FH"])), ("son high friction SH", sl("SH", ["FH", "lyp"])),
               ("son's career friction share", sl("s_fr", ["FH"])), ("son's career friction share", sl("s_fr", ["FH", "lyp"])),
               ("son's career friction share", sl("s_fr", FAT + ["lyp"]))],
              [("FH", "father had a friction year in the window (FH)"), ("lyp", LAB["lyp"])] + [(x_, LAB[x_]) for x_ in FAT],
              [(rr, onef[onef.race == rr]) for rr in RACES])
    # IGE by cell, two age groups
    md += ["#### B2. The IGE by cell (valid years), 25-34 and 35-55; triple interaction = both - father only - son only "
           "+ neither", "",
           "| outcome | ages | race | neither | father only | son only | both | triple interaction | both - mean of "
           "one-high cells |", "|---|---|---|---|---|---|---|---|---|"]
    for y in ("lw", "ly"):
        for lo, hi in ((25, 34), (35, 55)):
            for race in RACES:
                z = fs[(fs.race == race) & fs[y].notna() & fs.age.between(lo, hi)].copy()
                cs = [((z.FH == f) & (z.SH == s)).astype(float).to_numpy() for f, s in ((0, 0), (1, 0), (0, 1), (1, 1))]
                X = np.column_stack([cc * z["lyp"].to_numpy(float) for cc in cs] + cs[1:] + [dummies(z["age"])])
                b, V = fitc(X, z[y].to_numpy(float), z["fam68"].to_numpy())
                L = np.zeros(X.shape[1] + 1)
                L[[0, 1, 2, 3]] = [1, -1, -1, 1]
                M2 = np.zeros(X.shape[1] + 1)
                M2[[1, 2, 3]] = [-0.5, -0.5, 1]
                tri = (float(L @ b), float(np.sqrt(L @ V @ L)))
                dm = (float(M2 @ b), float(np.sqrt(M2 @ V @ M2)))
                ent = [(float(b[i]), float(np.sqrt(V[i, i]))) for i in range(4)]
                md.append(f"| {y} | {lo}-{hi} | {race} | " + " | ".join(c(e) for e in ent) + f" | {c(tri)} | {c(dm)} |")
                RES[f"B2|{y}|{lo}-{hi}|{race}"] = {"cells": ent, "triple": tri, "both-mean1": dm}
    md.append("")
    print("B3 ...", flush=True)
    fs["SO"] = ((fs["FH"] == 0) & (fs["SH"] == 1)).astype(float)
    md += ["#### B3. The IGE by band with the suppressed pairs left out, and (placebo) with the son-only high-friction "
           "sons left out (father-present sons, valid years)", "",
           "Leaving out any group of sons with low outcomes and low parental income flattens the slope; the placebo "
           "row (sons with high friction whose father had none) shows how much of the change is specific to pairs.", "",
           "| outcome | race | quantity | " + " | ".join(BL) + " | opening |", "|---" * 10 + "|"]
    for y in ("lw", "ly"):
        for mk, mlab in (("HH", "suppressed pairs (FH and SH)"), ("SO", "son-only high friction (SH, not FH)")):
            ob = boot_drop(fs[fs[y].notna()], y, mk)
            for race in RACES + ("W-B",):
                for i, lab in enumerate(("all sons", f"without {mlab}", f"difference (all - without {mk})")):
                    if i == 0 and mk == "SO":
                        continue
                    md.append(f"| {y} | {race} | {lab} | " + " | ".join(c(ob[race][k][i][:2]) for k in range(6))
                              + f" | {c(ob[race]['open'][i][:2])} |")
                RES[f"B3|{mk}|{y}|{race}"] = {str(k): [list(t[:2]) for t in ob[race][k]]
                                              for k in list(range(6)) + ["open"]}
            md.append(f"| {y} | | share of son-years in {mlab} | White {ob['White']['share_rows']:.3f}, Black "
                      f"{ob['Black']['share_rows']:.3f} |" + " |" * 6)
    md.append("")
    # who and where: South, high-unemployment childhood state, period
    md += ["#### B4. Who are the suppressed pairs (one row per father-present son; shares)", "",
           "| race | group | sons | South at 17 | childhood state ur above the pooled median | born before 1960 | "
           "born 1960-69 | born 1970+ | father's schooling < 12 | parental income bottom pooled tercile |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    med_ur = float(onef["ur_win"].median())
    tq = float(one["lyp"].quantile(1 / 3))
    for race in RACES:
        for lab, m_ in (("suppressed pair", onef.HH == 1), ("other", onef.HH == 0)):
            q = onef[(onef.race == race) & m_]
            fe_ = pd.to_numeric(q["f_educ"], errors="coerce").where(lambda s: s.between(0, 20))
            md.append(f"| {race} | {lab} | {len(q):,} | {q['south'].mean():.3f} | "
                      f"{(q['ur_win'] > med_ur).where(q['ur_win'].notna()).mean():.3f} | "
                      f"{(q['birth_year'] < 1960).mean():.3f} | {q['birth_year'].between(1960, 1969).mean():.3f} | "
                      f"{(q['birth_year'] >= 1970).mean():.3f} | {(fe_ < 12).where(fe_.notna()).mean():.3f} | "
                      f"{(q['lyp'] <= tq).mean():.3f} |")
    md.append("")
    reg_table(md, "B5. Suppressed pair (FH and SH) on place and background (one row per father-present son, linear "
                  "probability)",
              [("suppressed pair", sl("HH", ["south"])), ("suppressed pair", sl("HH", ["ur_win"])),
               ("suppressed pair", sl("HH", ["ur_win", "south", "lyp"]))],
              [("south", "South at 17"), ("ur_win", LAB["ur_win"]), ("lyp", LAB["lyp"])],
              [(rr, onef[onef.race == rr]) for rr in RACES])
    # ------------------------------------------------ C. place
    print("C ...", flush=True)
    md += ["## C. Place: is the shared friction the local labor market?", ""]
    pc = fs[fs["fips17"].notna() & fs["fips_cur"].notna() & fs["ur_cur"].notna() & fs["ur_win"].notna()].copy()
    rl = lambda y, xs, fe=(), ab=None: (lambda s: reg(s, y, xs, fe=fe, absorb=ab)[:4])   # noqa: E731
    reg_table(md, "C1. The son's friction year (displaced, unemployed or zero hours; 0/1) on his father's window "
                  "shares and place (son-years 25-55, father-present sons with place measures)",
              [("son's friction year", rl("fr", FAT + ["lyp"])),
               ("son's friction year", rl("fr", FAT + ["lyp", "ur_cur", "ur_win"])),
               ("son's friction year", rl("fr", FAT + ["lyp", "ur_cur", "ur_win"], fe=("fips17",))),
               ("son's friction year", rl("fr", FAT + ["lyp", "ur_win"], ab="sy"))],
              [(x_, LAB[x_]) for x_ in FAT + ["lyp", "ur_cur", "ur_win"]], [(rr, pc[pc.race == rr]) for rr in RACES],
              note="Single-age dummies in every column; (3) adds state-at-17 FE; (4) absorbs current state x year FE "
                   "(ur_cur is then absorbed).")
    onep = pc.drop_duplicates("pid").assign(age=40)
    reg_table(md, "C2. The father's friction on his local labor market (one row per son)",
              [("father's share unemployed", sl("f_sh_unemp", ["ur_win"])),
               ("father's share displaced", sl("f_sh_disp", ["ur_win"])),
               ("father's share zero hours", sl("f_sh_zero", ["ur_win"])),
               ("father had a friction year FH", sl("FH", ["ur_win"]))],
              [("ur_win", LAB["ur_win"])], [(rr, onep[onep.race == rr]) for rr in RACES])
    pr = r[r["fips17"].notna() & r["fips_cur"].notna()]
    for y, lab in (("lw", "ln hourly wage"), ("ly", "ln annual earnings")):
        prof_table(md, f"C3. IGE profile of the {lab} with place fixed effects (all sons with a state at 17 and a "
                       "current state, same sons)",
                   [("no FE", profile(pr, y)), ("state-at-17 FE", profile(pr, y, fe="fips17")),
                    ("current-state FE", profile(pr, y, fe="fips_cur")),
                    ("current state x year FE", profile(pr, y, absorb="sy"))])
    # ------------------------------------------------ F. NLSY79
    print("F ...", flush=True)
    try:
        R70 = _load("s70", "70.RauhReplication.py")
        P, _ = R70.build(R70.extract())
        k = pd.read_pickle(DATA / "nlsy79_kids.pkl")
        k = k[(k["female"] == 0) & k["race"].isin(RACES)][["pid", "race", "lpinc_av", "hhid"]]
        P = P.merge(k, on="pid")
        P = P[P["wk"].between(0, 52) & P["age"].between(25, 55) & P["lpinc_av"].notna()].copy()
        P["nonemp"] = 1 - P["wk"] / 52
        P["lyp"] = P["lpinc_av"]
        P["fam68"] = P["hhid"]
        P["ry"] = (P["region"] * 10000 + P["cal"]).where(P["region"].notna())
        P["cal_"] = P["cal"]
        nl = lambda xs, fe=(), ab=None: (lambda s: reg(s, "nonemp", xs, cl="hhid", fe=fe, absorb=ab)[:4])  # noqa
        pn = P.dropna(subset=["ry"])
        md += ["## F. NLSY79: the son's non-employment gradient in parental income and the regional labor market", ""]
        reg_table(md, "F1. Share of weeks not worked in the calendar year on ln parental income (men, cross-sectional + "
                      "supplemental samples; single-age dummies)",
                  [("weeks not worked share, 25-34", lambda s: reg(s[s.age <= 34], "nonemp", ["lyp"], cl="hhid",
                                                                    fe=("cal_",))[:4]),
                   ("weeks not worked share, 25-34", lambda s: reg(s[s.age <= 34], "nonemp", ["lyp"], cl="hhid",
                                                                    absorb="ry")[:4]),
                   ("weeks not worked share, 35-55", lambda s: reg(s[s.age >= 35], "nonemp", ["lyp"], cl="hhid",
                                                                    fe=("cal_",))[:4]),
                   ("weeks not worked share, 35-55", lambda s: reg(s[s.age >= 35], "nonemp", ["lyp"], cl="hhid",
                                                                    absorb="ry")[:4])],
                  [("lyp", "ln parental income (1979-81)")], [(rr, pn[pn.race == rr]) for rr in RACES],
                  note="(1), (3): calendar-year FE; (2), (4): census region x calendar-year FE absorbed. Clusters: 1979 "
                       "household.")
    except Exception as ex:  # NLSY79 block is optional
        md += [f"## F. NLSY79: not run ({ex!r})", ""]
    (OUT / "shared_friction.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "shared_friction.json", "w"), indent=1, default=lambda o: None if isinstance(
        o, np.ndarray) else str(o))
    print("\n".join(md))


if __name__ == "__main__":
    main()
