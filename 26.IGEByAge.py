r"""Intergenerational persistence by the CHILD'S AGE at measurement, by race (2026-10-17).

Question: Chetty, Hendren, Jones and Porter (2020) measure children only at 31-37 and find similar rank-rank slopes
by race (0.28 Black / 0.32 White); our Lee-Solon log IGE at 40 (6.IGEMain.py) differs a lot (sons 0.268 / 0.473).
Does persistence, and the Black-White difference in it, depend on the age at which the child is measured?

DATA (read only): data/psid_person_year.pkl, psid_kids.pkl, nlsy79_kids.pkl, nlsy79_person_year.pkl, and the
cached head / wife panel of 24.IGEDecomposition.py (data/ige_decomposition_panel.pkl: hours, displacement,
unemployment, reduced-hours and zero-hours flags; built from the raw PSID files and psid_displacement.pkl).
Age = age at the interview (wave), as in 6.IGEMain.py and 7.RankMobility.py; income refers to the previous year.

AGE BANDS 25-29, 30-34, 35-39, 40-44, 45-49, 50-55, plus Chetty's window 31-37 (overlapping, a replication row,
never used in the tests).

A. LOG IGE (PSID; parents and controls as in 6.IGEMain.py)
   parents: ln mean family income while the child is the head's child at 13-19 (>= 3 years in bounds), head's age A
   at 16 between 30 and 70, race = that head's race; child: head or wife (spouse / partner).
   Outcomes: ln family income of the child's own household; ln own labor earnings (> 0). Yearly amounts outside
   $100-$150,000 (1967 dollars) dropped (6.IGEMain.py).
   (i)  child-year: all child-years in the band; ln y on ln parental income, quartic in (A - 45)/10, single-year
        age dummies;
   (ii) band mean: one row per child and band, ln of the mean over the band's years (>= 2 years in bounds);
        quartic in (A - 45)/10 and the child's mean age in the band;
   (iii) Lee-Solon age-interacted: one regression on all child-years at 25-55, ln parental income interacted with
        a quartic in (age - 40)/10 (and the quartics of 6.IGEMain.py); the IGE at each age 25..55 is the linear
        combination b0 + sum_n b_n ((age - 40)/10)^n (delta-method s.e.).
   Samples: Black, White (unweighted, as 6.IGEMain.py), pooled = all races weighted by the child-year core
   longitudinal weight (band-mean rows: the mean weight over the band's years); robustness (child-year design):
   Black / White weighted by the same weight.
B. RANKS (PSID; definitions of 7.RankMobility.py)
   parents: mean family income at child ages 12-17 (psid_kids pinc_av, >= 3 waves), ranked within the child's birth
   year among all children of the file (weight wt_pt, core longitudinal weight at 16); child: mean family income
   of own household over the band's years (>= 2 years; zeros / negatives kept), ranked within birth year AND band
   among all children observed in that band (same weights). Also own labor earnings (zeros kept). Weighted rank-rank
   slope, E[rank] at parental p25 / p75 from the line. Race-specific and pooled (all races) are all weighted.
BALANCED: children observed (>= 1 child-year in bounds for (i); >= 2 years for (ii) and ranks) in every band of
   25-29 ... 45-49 ('balanced 25-49') or of 35-39 ... 50-55 ('balanced 35-55'); child ranks recomputed within birth
   year and band among the balanced children; parents keep their full-file ranks.
INFERENCE: every band x race (or band, pooled) cell is its own regression; the joint covariance of all cells is the
   cluster-robust sandwich of the stacked, fully interacted regression (clusters = 1968 family; NLSY79: 1979
   household), so the same child in several bands is accounted for. Tests on the Black-White gap g_b = beta_W,b -
   beta_B,b across the six bands: (1) Wald test that g_b is equal in all bands; (2) linear trend of g_b in the band
   midpoint, per 10 years of age; (3) mean g_b in bands < 35 minus mean g_b in bands >= 35. The same three tests on
   the pooled slope (the general life-cycle pattern) and on each race's slope. Normal p-values.
C. INTERPRETATION CHECKS (PSID)
   1 Haider-Solon: children observed in an early and a late band; regression of the change in their mean ln income
     (late - early) on ln parental income (controls: A quartic, the change in mean age): the gradient of income
     growth in parental income = the change of the IGE between the two ages in that fixed sample.
   2 Marriage: partnered (a spouse / partner in the child's family unit) on ln parental income (LPM) by band; the
     family-income IGE with and without a partnered control; own earnings vs family income.
   3 Instability (24.IGEDecomposition.py flags; male heads): share of child-years displaced (closure / layoff, t or
     t-1) or unemployed, with reduced hours (< 1,500, full-time attached men), with zero hours; their gradients in
     ln parental income by band; the earnings / family-income IGE in clean years (no displacement / unemployment;
     family income also excluding zero-hours years) vs all valid years. Daughters: laid off / looking at the
     interview (1979+), zero hours.
   4 Log vs rank on the same children and weights (rank frame, positive band-mean income, no controls): log IGE,
     rank slope, their correlation and SD-ratio parts, and the hybrids (ln child on parent rank, child rank on ln
     parent); bootstrap s.e. (200 draws of families, frequency weights, ranks fixed). Also for the NLSY79.
D. NLSY79 (cohorts 1960-64, living with a parent in 1979, as in 7.RankMobility.py): parents = mean family income
   1978-80 rounds, parent's age in 1979 (+ years averaged); child-years 25-55; weight wt79; clusters = 1979 household.
   Log IGE (i) and (iii), ranks by band, same tests.
Writes output/ige_by_age.csv (every estimate), output/ige_by_age.md, output/ige_by_age.png.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.linalg import block_diag
from scipy.stats import chi2, norm

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DATA, OUT, stars  # noqa: E402

_spec = importlib.util.spec_from_file_location("ige6", Path(__file__).resolve().parent / "6.IGEMain.py")
ige6 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ige6)

LO, HI = ige6.LO, ige6.HI
BANDS = [(25, 29), (30, 34), (35, 39), (40, 44), (45, 49), (50, 55)]
BL = [f"{a}-{b}" for a, b in BANDS]
CH = "31-37"
MID = dict(zip(BL, [(a + b) / 2 for a, b in BANDS]))
BAL = {"unbalanced": BL, "balanced 25-49": BL[:5], "balanced 35-55": BL[2:]}
RACES = ("Black", "White")
SEXES = {"Sons": [0], "Daughters": [1], "Both": [0, 1]}
PAIRS = [("25-29", "35-39"), ("25-29", "45-49"), ("30-34", "40-44")]
A4 = [f"A{n}" for n in range(1, 5)]
ROWS = []                                   # every estimate -> csv


def band_of(age):
    out = pd.Series(pd.NA, index=age.index, dtype="object")
    for (a, b), lab in zip(BANDS, BL):
        out[age.between(a, b)] = lab
    return out


def stack(d, bands, with_ch=True):
    """child-year (or child-band) rows of the listed bands plus Chetty's 31-37 window as an extra cell."""
    parts = [d[d["band"] == b].assign(cell=b) for b in bands]
    if with_ch and "age" in d:
        parts.append(d[d["age"].between(31, 37)].assign(cell=CH))
    return pd.concat(parts, ignore_index=True)


# ================================================================ regression engine
class Cells:
    """Separate (W)LS in each cell, joint cluster-robust covariance (= stacked fully interacted regression)."""

    def __init__(self, d, y, x, cell, ctrl=(), fe=None, w=None, cluster="fam68", pid="pid"):
        cols = list(dict.fromkeys([cell, y, x, *ctrl, cluster, pid] + ([fe] if fe else []) + ([w] if w else [])))
        d = d[cols].replace([np.inf, -np.inf], np.nan).dropna()
        if w:
            d = d[d[w] > 0]
        d = d.reset_index(drop=True)
        gid = pd.factorize(d[cluster])[0]
        G = gid.max() + 1
        self.names, breads, scores, self.b, self.info = [], [], [], [], {}
        for c, g in d.groupby(cell, sort=False):
            X = pd.DataFrame({"const": 1.0, "x": g[x].astype(float)}, index=g.index)
            for k in ctrl:
                X[k] = g[k].astype(float)
            if fe:
                X = X.join(pd.get_dummies(g[fe].astype(int), prefix="fe", drop_first=True, dtype=float))
            keep = (X.std() > 1e-12) | (X.columns == "const")
            X = X.loc[:, keep]
            Xa = X.to_numpy()
            ww = g[w].to_numpy(float) if w else np.ones(len(g))
            Bi = np.linalg.pinv(Xa.T @ (Xa * ww[:, None]))
            yy = g[y].to_numpy(float)
            bb = Bi @ (Xa.T @ (ww * yy))
            u = Xa * (ww * (yy - Xa @ bb))[:, None]
            S = np.zeros((G, Xa.shape[1]))
            np.add.at(S, gid[g.index.to_numpy()], u)
            breads.append(Bi)
            scores.append(S)
            self.b.extend(bb)
            self.names.extend((c, n) for n in X.columns)
            self.info[c] = dict(n=len(g), children=g[pid].nunique(), clusters=g[cluster].nunique(),
                                mean_y=np.average(yy, weights=ww))
        B, S = block_diag(*breads), np.hstack(scores)
        N, K = len(d), len(self.b)
        self.V = B @ (S.T @ S) @ B * G / (G - 1) * (N - 1) / max(N - K, 1)
        self.b = np.array(self.b)
        self.ix = {n: i for i, n in enumerate(self.names)}
        self.G = G

    def has(self, c):
        return (c, "x") in self.ix

    def lin(self, terms):
        """terms: [(cell, name, weight)] -> (estimate, se, p)."""
        r = np.zeros(len(self.b))
        for c, n, wt in terms:
            r[self.ix[(c, n)]] += wt
        e, se = r @ self.b, np.sqrt(r @ self.V @ r)
        return e, se, 2 * (1 - norm.cdf(abs(e) / se)) if se > 0 else np.nan

    def wald(self, rows):
        R = np.zeros((len(rows), len(self.b)))
        for i, terms in enumerate(rows):
            for c, n, wt in terms:
                R[i, self.ix[(c, n)]] += wt
        e = R @ self.b
        st = float(e @ np.linalg.pinv(R @ self.V @ R.T) @ e)
        return st, len(rows), 1 - chi2.cdf(st, len(rows))


def slope_terms(cell, race=None, name="x"):
    return [((cell, race) if race else cell, name, 1.0)]


def gap_terms(cell, name="x", c0=0.0, cx=1.0):
    """White - Black of (c0 * const + cx * x) in band `cell`."""
    t = []
    for race, s in (("White", 1), ("Black", -1)):
        if c0:
            t.append(((cell, race), "const", s * c0))
        t.append(((cell, race), name, s * cx))
    return t


def tests(R, bands, mode):
    """mode 'gap' (race cells), 'pooled' (band cells), or a race name. Returns list of (test, est, se, p, stat)."""
    def term(b):
        if mode == "gap":
            return gap_terms(b)
        if mode == "pooled":
            return slope_terms(b)
        return slope_terms(b, mode)
    bands = [b for b in bands if (R.has((b, "White")) and R.has((b, "Black"))) or R.has(b) or R.has((b, mode))]
    out = []
    if len(bands) >= 2:
        st, df, p = R.wald([term(b) + [(t[0], t[1], -t[2]) for t in term(bands[0])] for b in bands[1:]])
        out.append(("Equal in all bands (Wald chi2)", st, np.nan, p, f"chi2({df})={st:.2f}"))
        m = np.array([MID[b] for b in bands])
        c = (m - m.mean()) / ((m - m.mean()) ** 2).sum() * 10
        e, se, p = R.lin([t2 for b, cw in zip(bands, c) for t2 in [(t[0], t[1], t[2] * cw) for t in term(b)]])
        out.append(("Linear trend per 10 years", e, se, p, ""))
    early, late = [b for b in bands if MID[b] < 35], [b for b in bands if MID[b] >= 35]
    if early and late:
        e, se, p = R.lin([(t[0], t[1], t[2] / len(early)) for b in early for t in term(b)])
        out.append(("Mean in bands < 35", e, se, p, ""))
        e, se, p = R.lin([(t[0], t[1], t[2] / len(late)) for b in late for t in term(b)])
        out.append(("Mean in bands >= 35", e, se, p, ""))
        e, se, p = R.lin([(t[0], t[1], t[2] / len(early)) for b in early for t in term(b)]
                         + [(t[0], t[1], -t[2] / len(late)) for b in late for t in term(b)])
        out.append(("Mean < 35 minus mean >= 35", e, se, p, ""))
    return out


def cell(e, se, p, dec=3):
    if not np.isfinite(e):
        return ""
    pv = "<0.001" if p < 0.001 else f"{p:.3f}"
    return f"{e:.{dec}f}{stars(p)} ({se:.{dec}f}; p={pv})"


def record(**k):
    ROWS.append(k)


# ================================================================ PSID data
def psid_frames():
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    s = ige6.build(py)
    s = s[s["age"].between(25, 55)].copy()
    s["band"], s["agei"] = band_of(s["age"]), s["age"].round().astype(int)
    wives = set(zip(py.loc[py["wife"], "wave"], py.loc[py["wife"], "int"]))
    s["partnered"] = [float(wf or (wv, it) in wives) for wf, wv, it in zip(s["wife"], s["wave"], s["int"])]
    a = pd.read_pickle(DATA / "ige_decomposition_panel.pkl")
    fl = a[["pid", "wave", "disp", "unemp", "red", "zero", "est23", "shock", "valid", "ly", "cleanA"]]
    s = s.merge(fl, on=["pid", "wave"], how="left")
    mh = s["head"] & (s["female"] == 0)
    s["shockm"] = s["shock"].where(mh & (s["disp"].notna() | s["unemp"].notna()))
    s["ly_valid"] = s["ly"]
    s["ly_clean"] = s["ly"].where(s["cleanA"].fillna(False).astype(bool) & mh)
    s["lfam_clean"] = s["lfam"].where(mh & (s["shock"] == 0) & (s["zero"] != 1))
    for c in ("red", "zero"):
        s[c + "m"] = s[c].where(mh)
    s["wt"] = s["wt"].astype(float)
    # ranks
    k = pd.read_pickle(DATA / "psid_kids.pkl")
    k = k.assign(w=k["wt_pt"], pinc=k["pinc_av"].where(k["n_av"] >= 3))
    hw = py[(py["head"] | py["wife"]) & py["age"].between(25, 55)].copy()
    return s, k, hw


def wrank(v, w):
    o = np.argsort(v, kind="stable")
    cw = np.cumsum(w[o])
    mid = pd.Series((cw - w[o] / 2) / cw[-1] * 100).groupby(v[o]).transform("mean").to_numpy()
    r = np.empty(len(v))
    r[o] = mid
    return r


def rank_in(d, col, by):
    d = d[d[col].notna() & (d["w"] > 0)]
    return pd.concat([pd.Series(wrank(g[col].to_numpy(), g["w"].to_numpy()), index=g.index)
                      for _, g in d.groupby(by)])


def rank_frame(k, hw, idcol="pid"):
    """child x band rows (incl. 31-37) with parent rank rp and child band means of family income / earnings."""
    k = k.copy()
    k["rp"] = rank_in(k, "pinc", "birth_year")
    out = []
    for lab, (lo, hi) in list(zip(BL, BANDS)) + [(CH, (31, 37))]:
        h = hw[hw["age"].between(lo, hi)]
        f = h.dropna(subset=["faminc"]).groupby(idcol)["faminc"].agg(["mean", "count"])
        e = h.dropna(subset=["earn"]).groupby(idcol)["earn"].agg(["mean", "count"])
        x = k[["birth_year", "w", "rp", "race", "female", "fam68", "pinc"]].copy()
        x["yf"] = f.loc[f["count"] >= 2, "mean"].reindex(x.index)
        x["ye"] = e.loc[e["count"] >= 2, "mean"].reindex(x.index)
        x["band"] = lab
        out.append(x)
    r = pd.concat(out).rename_axis("pid").reset_index()
    return r


def add_child_ranks(r, members=None):
    r = r.copy() if members is None else r[r["pid"].isin(members)].copy()
    for y in ("yf", "ye"):
        r["r" + y] = rank_in(r, y, ["birth_year", "band"])
    return r


def band_means(s, y, raw, min_n=2):
    """one row per child x band (and 31-37): ln of the mean of `raw` over years with `y` non-missing."""
    out = []
    for lab, (lo, hi) in list(zip(BL, BANDS)) + [(CH, (31, 37))]:
        h = s[s["age"].between(lo, hi) & s[y].notna()]
        g = h.groupby("pid")
        m = pd.DataFrame({"m": g[raw].mean(), "n": g[raw].count(), "agem": g["age"].mean(), "wt": g["wt"].mean()})
        m = m[m["n"] >= min_n].join(g[["lyp", "race", "fam68", "female", *A4]].first())
        m["ly"] = np.log(m["m"])
        m["agec"] = m["agem"] - MID.get(lab, 34)
        m["band"] = m["cell"] = lab
        out.append(m)
    return pd.concat(out).reset_index()


# ================================================================ estimation blocks
def logige_block(data, s, sexes, outcomes, design, members_fn):
    """band-specific log IGE: race cells (unweighted) + pooled (weighted); records and returns Cells objects."""
    res = {}
    for sex, fem in sexes.items():
        if sex == "Both":
            continue
        x = s[s["female"].isin(fem)]
        for yname, ylab, raw in outcomes:
            for bal, bands in BAL.items():
                if design == "child-year":
                    d = x[x[yname].notna()]
                    mem = members_fn(d, bands, 1)
                    d = d if mem is None else d[d["pid"].isin(mem)]
                    st = stack(d, bands, with_ch=(bal == "unbalanced"))
                    ctrl, fe = A4, "agei"
                else:
                    bm = band_means(x, yname, raw)
                    mem = members_fn(bm.rename(columns={"cell": "bandx"}), bands, 0, band_rows=True)
                    st = bm[bm["band"].isin(bands + ([CH] if bal == "unbalanced" else []))]
                    st = st if mem is None else st[st["pid"].isin(mem)]
                    ctrl, fe = A4 + ["agec"], None
                    st = st.rename(columns={"ly": yname + "_bm"})
                yy = yname if design == "child-year" else yname + "_bm"
                Rr = Cells(st[st["race"].isin(RACES)].assign(rc=lambda q: list(zip(q["cell"], q["race"]))),
                           yy, "lyp", "rc", ctrl, fe)
                wcol = "wt"
                Rp = Cells(st, yy, "lyp", "cell", ctrl, fe, w=wcol)
                res[(sex, yname, bal)] = (Rr, Rp)
                sets = [(Rr, "")]
                if design == "child-year":            # race-specific, weighted by the child-year weight
                    Rw = Cells(st[st["race"].isin(RACES)].assign(rc=lambda q: list(zip(q["cell"], q["race"]))),
                               yy, "lyp", "rc", ctrl, fe, w=wcol)
                    sets.append((Rw, " (weighted)"))
                for b in bands + ([CH] if bal == "unbalanced" else []):
                    if Rp.has(b):
                        e, se, p = Rp.lin([(b, "x", 1)])
                        record(data=data, analysis=f"log IGE, {design}", sex=sex, sample=bal, band=b,
                               group="Pooled (weighted)", outcome=ylab, stat="IGE", est=e, se=se, p=p, **Rp.info[b])
                    for R, suf in sets:
                        for g in RACES:
                            if R.has((b, g)):
                                e, se, p = R.lin([((b, g), "x", 1)])
                                record(data=data, analysis=f"log IGE, {design}", sex=sex, sample=bal, band=b,
                                       group=g + suf, outcome=ylab, stat="IGE", est=e, se=se, p=p, **R.info[(b, g)])
                        if R.has((b, "White")) and R.has((b, "Black")):
                            e, se, p = R.lin(gap_terms(b))
                            record(data=data, analysis=f"log IGE, {design}", sex=sex, sample=bal, band=b,
                                   group="White - Black" + suf, outcome=ylab, stat="IGE", est=e, se=se, p=p,
                                   n=R.info[(b, "White")]["n"] + R.info[(b, "Black")]["n"])
                runs = [("pooled", Rp, "")] + [(m, R, suf) for R, suf in sets for m in ("gap", "Black", "White")]
                for mode, R, suf in runs:
                    for t, e, se, p, txt in tests(R, bands, mode):
                        record(data=data, analysis=f"log IGE, {design}", sex=sex, sample=bal, band="test",
                               group={"pooled": "Pooled (weighted)", "gap": "White - Black"}.get(mode, mode) + suf,
                               outcome=ylab, stat=t, est=e, se=se, p=p, note=txt)
    return res


def members_balanced(d, bands, _min, band_rows=False):
    """children observed in every band of `bands` (None if all bands = unbalanced)."""
    if bands == BL:
        return None
    col = "band"
    c = d[d[col].isin(bands)].groupby("pid")[col].nunique()
    return set(c[c == len(bands)].index)


def lee_solon_curve(data, s, sexes, outcomes, label="Lee-Solon"):
    s = s.copy()
    s["C"] = s["age"] - 40
    for n in range(1, 5):
        s[f"C{n}"] = (s["C"] / 10) ** n
        s[f"lypC{n}"] = s["lyp"] * s[f"C{n}"]
    ctrl = A4 + [f"C{n}" for n in range(1, 5)] + [f"lypC{n}" for n in range(1, 5)]
    out = {}
    for sex, fem in sexes.items():
        if sex == "Both":
            continue
        x = s[s["female"].isin(fem)]
        for yname, ylab, _ in outcomes:
            d = x[x[yname].notna()]
            Rr = Cells(d[d["race"].isin(RACES)], yname, "lyp", "race", ctrl)
            Rp = Cells(d.assign(one="all"), yname, "lyp", "one", ctrl, w="wt")
            for age in range(25, 56):
                z = (age - 40) / 10
                for grp, R, c in (("Pooled (weighted)", Rp, "all"), ("Black", Rr, "Black"), ("White", Rr, "White")):
                    e, se, p = R.lin([(c, "x", 1)] + [(c, f"lypC{n}", z ** n) for n in range(1, 5)])
                    out[(sex, ylab, grp, age)] = (e, se, p)
                    record(data=data, analysis=label, sex=sex, sample="unbalanced", band=str(age), group=grp,
                           outcome=ylab, stat="IGE at age", est=e, se=se, p=p, n=R.info[c]["n"],
                           children=R.info[c]["children"], clusters=R.info[c]["clusters"])
                eB, sB, _ = out[(sex, ylab, "Black", age)]
                eW, sW, _ = out[(sex, ylab, "White", age)]
                g, sg = eW - eB, np.hypot(sB, sW)
                pg = 2 * (1 - norm.cdf(abs(g) / sg))
                out[(sex, ylab, "White - Black", age)] = (g, sg, pg)
                record(data=data, analysis=label, sex=sex, sample="unbalanced", band=str(age), group="White - Black",
                       outcome=ylab, stat="IGE at age", est=g, se=sg, p=pg)
            # slope of the race gap in age: d/d age of [IGE_W(a) - IGE_B(a)] averaged 25-55, and 30 vs 45
            for a0, a1 in ((30, 45), (33, 45), (34, 50)):
                vals = []
                for R, c in ((Rr, "White"), (Rr, "Black")):
                    vals.append([(c, f"lypC{n}", ((a1 - 40) / 10) ** n - ((a0 - 40) / 10) ** n) for n in range(1, 5)])
                terms = vals[0] + [(t[0], t[1], -t[2]) for t in vals[1]]
                e, se, p = Rr.lin(terms)
                record(data=data, analysis=label, sex=sex, sample="unbalanced", band=f"{a1} minus {a0}",
                       group="White - Black", outcome=ylab, stat="Change in gap", est=e, se=se, p=p)
                e, se, p = Rp.lin([("all", f"lypC{n}", ((a1 - 40) / 10) ** n - ((a0 - 40) / 10) ** n)
                                   for n in range(1, 5)])
                record(data=data, analysis=label, sex=sex, sample="unbalanced", band=f"{a1} minus {a0}",
                       group="Pooled (weighted)", outcome=ylab, stat="Change in IGE", est=e, se=se, p=p)
    return out


def rank_block(data, r0, sexes, ycols):
    """rank-rank slope, E[rank] at p25 / p75 by band; race cells and pooled (all weighted)."""
    res = {}
    for bal, bands in BAL.items():
        mem = None
        if bal != "unbalanced":
            ok = r0[r0["band"].isin(bands) & r0["yf"].notna() & r0["rp"].notna() & (r0["w"] > 0)]
            c = ok.groupby("pid")["band"].nunique()
            mem = set(c[c == len(bands)].index)
        r = add_child_ranks(r0, mem)
        r = r[r["band"].isin(bands + ([CH] if bal == "unbalanced" else []))]
        for sex, fem in sexes.items():
            x = r[r["female"].isin(fem)].assign(cell=lambda q: q["band"])
            for yc, ylab in ycols:
                d = x.dropna(subset=["rp", "r" + yc])
                Rr = Cells(d[d["race"].isin(RACES)].assign(rc=lambda q: list(zip(q["cell"], q["race"]))),
                           "r" + yc, "rp", "rc", w="w")
                Rp = Cells(d, "r" + yc, "rp", "cell", w="w")
                res[(sex, yc, bal)] = (Rr, Rp)
                for b in bands + ([CH] if bal == "unbalanced" else []):
                    for grp, R, c in (("Pooled (weighted)", Rp, b), ("Black", Rr, (b, "Black")),
                                      ("White", Rr, (b, "White"))):
                        if not R.has(c):
                            continue
                        for stt, c0, cx in (("slope", 0, 1), ("E[rank] p25", 1, 25), ("E[rank] p75", 1, 75)):
                            e, se, p = R.lin([(c, "const", c0), (c, "x", cx)] if c0 else [(c, "x", cx)])
                            if c0:
                                p = 2 * (1 - norm.cdf(abs(e - 50) / se))
                            record(data=data, analysis="rank", sex=sex, sample=bal, band=b, group=grp, outcome=ylab,
                                   stat=stt, est=e, se=se, p=p, **R.info[c])
                    if Rr.has((b, "White")) and Rr.has((b, "Black")):
                        for stt, c0, cx in (("slope", 0, 1), ("E[rank] p25", 1, 25), ("E[rank] p75", 1, 75)):
                            e, se, p = Rr.lin(gap_terms(b, c0=c0, cx=cx))
                            record(data=data, analysis="rank", sex=sex, sample=bal, band=b, group="White - Black",
                                   outcome=ylab, stat=stt, est=e, se=se, p=p,
                                   n=Rr.info[(b, "White")]["n"] + Rr.info[(b, "Black")]["n"])
                for mode, R in (("pooled", Rp), ("gap", Rr), ("Black", Rr), ("White", Rr)):
                    for t, e, se, p, txt in tests(R, bands, mode):
                        record(data=data, analysis="rank", sex=sex, sample=bal, band="test",
                               group={"pooled": "Pooled (weighted)", "gap": "White - Black"}.get(mode, mode),
                               outcome=ylab, stat=t, est=e, se=se, p=p, note=txt)
    return res


LVR = [("ige", "Log IGE (ln child on ln parent)"), ("rr", "Rank-rank slope"),
       ("rho_l", "Corr(ln child, ln parent)"), ("sdr_l", "SD ln child / SD ln parent"),
       ("rho_r", "Corr(child rank, parent rank)"), ("sdr_r", "SD child rank / SD parent rank"),
       ("lr", "ln child on parent rank / 100"), ("rl", "Child rank on ln parent")]
NBOOT = 200


def lvr_moments(df, v):
    """weighted moments by cell -> statistics of LVR (one row per cell)."""
    z = pd.DataFrame({"cell": df["lcell"].to_numpy(), "v": v})
    cols = {"x": df["lp"].to_numpy(), "y": df["lc"].to_numpy(), "a": df["rp"].to_numpy(), "b": df["rc"].to_numpy()}
    for k, c in cols.items():
        z[k] = v * c
    for k1, k2 in (("x", "x"), ("y", "y"), ("a", "a"), ("b", "b"), ("x", "y"), ("a", "b"), ("a", "y"), ("x", "b")):
        z[k1 + k2] = v * cols[k1] * cols[k2]
    S = z.groupby("cell").sum()
    m = {k: S[k] / S["v"] for k in cols}
    cov = lambda k1, k2: S[k1 + k2] / S["v"] - m[k1] * m[k2]
    out = pd.DataFrame({"ige": cov("x", "y") / cov("x", "x"), "rr": cov("a", "b") / cov("a", "a"),
                        "rho_l": cov("x", "y") / np.sqrt(cov("x", "x") * cov("y", "y")),
                        "sdr_l": np.sqrt(cov("y", "y") / cov("x", "x")),
                        "rho_r": cov("a", "b") / np.sqrt(cov("a", "a") * cov("b", "b")),
                        "sdr_r": np.sqrt(cov("b", "b") / cov("a", "a")),
                        "lr": 100 * cov("a", "y") / cov("a", "a"), "rl": cov("x", "b") / cov("x", "x")})
    return out


def log_vs_rank(data, r0):
    """Same children, same weights: log IGE vs rank slope, with their correlation / dispersion parts. Bootstrap."""
    r = add_child_ranks(r0)
    r = r[(r["yf"] > 0) & (r["pinc"] > 0) & r["rp"].notna() & r["ryf"].notna() & (r["w"] > 0)
          & r["race"].isin(RACES)].copy()
    r["lp"], r["lc"], r["rc"] = np.log(r["pinc"]), np.log(r["yf"]), r["ryf"]
    frames = []
    for sex, fem in SEXES.items():
        x = r[r["female"].isin(fem)].copy()
        x["lcell"] = [f"{sex}|{b}|{g}" for b, g in zip(x["band"], x["race"])]
        frames.append(x)
    d = pd.concat(frames, ignore_index=True)
    w = d["w"].to_numpy(float)
    est = lvr_moments(d, w)
    fam = pd.factorize(d["fam68"])[0]
    G = fam.max() + 1
    rng = np.random.default_rng(20261017)
    draws = [lvr_moments(d, w * np.bincount(rng.integers(0, G, G), minlength=G)[fam]) for _ in range(NBOOT)]
    D = np.stack([dd.reindex(est.index).to_numpy() for dd in draws])
    se = pd.DataFrame(np.nanstd(D, axis=0, ddof=1), index=est.index, columns=est.columns)
    n = d.groupby("lcell").agg(n=("pid", "size"), children=("pid", "nunique"), clusters=("fam68", "nunique"))
    for sex in SEXES:
        for b in BL + [CH]:
            kb, kw = f"{sex}|{b}|Black", f"{sex}|{b}|White"
            if kb not in est.index or kw not in est.index:
                continue
            ib, iw = est.index.get_loc(kb), est.index.get_loc(kw)
            for j, (st, lab) in enumerate(LVR):
                for g, k in (("Black", kb), ("White", kw)):
                    e, s_ = est.loc[k, st], se.loc[k, st]
                    record(data=data, analysis="log vs rank", sex=sex, sample="unbalanced", band=b, group=g,
                           outcome="family income", stat=st, est=e, se=s_, p=2 * (1 - norm.cdf(abs(e) / s_)),
                           n=n.loc[k, "n"], children=n.loc[k, "children"], clusters=n.loc[k, "clusters"])
                gd = D[:, iw, j] - D[:, ib, j]
                e, s_ = est.loc[kw, st] - est.loc[kb, st], np.nanstd(gd, ddof=1)
                record(data=data, analysis="log vs rank", sex=sex, sample="unbalanced", band=b, group="White - Black",
                       outcome="family income", stat=st, est=e, se=s_, p=2 * (1 - norm.cdf(abs(e) / s_)))
        # change of the gap: mean over bands >= 35 minus mean over bands < 35
        for j, (st, lab) in enumerate(LVR):
            def gap(M, bands):
                return np.mean([M[..., est.index.get_loc(f"{sex}|{b}|White"), j]
                                - M[..., est.index.get_loc(f"{sex}|{b}|Black"), j] for b in bands], axis=0)
            E = est.to_numpy()
            early, late = BL[:2], BL[2:]
            e = gap(E, late) - gap(E, early)
            s_ = np.nanstd(gap(D, late) - gap(D, early), ddof=1)
            record(data=data, analysis="log vs rank", sex=sex, sample="unbalanced", band="test", group="White - Black",
                   outcome="family income", stat=st + ": gap >=35 minus <35", est=e, se=s_,
                   p=2 * (1 - norm.cdf(abs(e) / s_)))



def growth_block(s):
    """Haider-Solon: change of mean ln income between bands on ln parental income, fixed children."""
    for sex, fem in (("Sons", [0]), ("Daughters", [1])):
        x = s[s["female"] == fem[0]]
        for yname, ylab in (("lfam", "ln family income"), ("learn", "ln own earnings")):
            h = x[x[yname].notna()]
            m = h.groupby(["pid", "band"]).agg(y=(yname, "mean"), agem=("age", "mean"), wt=("wt", "mean"))
            ch = h.groupby("pid")[["lyp", "race", "fam68", *A4]].first()
            for e0, e1 in PAIRS:
                try:
                    a, b = m.xs(e0, level="band"), m.xs(e1, level="band")
                except KeyError:
                    continue
                d = a.join(b, lsuffix="0", rsuffix="1", how="inner").join(ch)
                d["dy"], d["dage"] = d["y1"] - d["y0"], d["agem1"] - d["agem0"]
                d["wt"] = d[["wt0", "wt1"]].mean(axis=1)
                d = d.reset_index()
                for col, lab in (("y0", f"IGE at {e0}"), ("y1", f"IGE at {e1}"), ("dy", "Growth gradient")):
                    ctrl = A4 + (["dage"] if col == "dy" else [])
                    Rr = Cells(d[d["race"].isin(RACES)], col, "lyp", "race", ctrl)
                    Rp = Cells(d.assign(one="all"), col, "lyp", "one", ctrl, w="wt")
                    for grp, R, c in (("Pooled (weighted)", Rp, "all"), ("Black", Rr, "Black"),
                                      ("White", Rr, "White")):
                        e, se, p = R.lin([(c, "x", 1)])
                        record(data="PSID", analysis="growth", sex=sex, sample=f"{e0} -> {e1}", band=lab,
                               group=grp, outcome=ylab, stat=col, est=e, se=se, p=p, **R.info[c])
                    e, se, p = Rr.lin([("White", "x", 1), ("Black", "x", -1)])
                    record(data="PSID", analysis="growth", sex=sex, sample=f"{e0} -> {e1}", band=lab,
                           group="White - Black", outcome=ylab, stat=col, est=e, se=se, p=p,
                           n=Rr.info["White"]["n"] + Rr.info["Black"]["n"])


def simple_band_block(s, analysis, specs, sexes):
    """band x race regressions (child-years, A quartic + age FE): specs = [(y, label, extra controls, sample)]."""
    out = {}
    for sex, fem in sexes:
        x = s[s["female"].isin(fem)]
        for y, ylab, extra in specs:
            d = x[x[y].notna()]
            st = stack(d, BL, with_ch=False)
            Rr = Cells(st[st["race"].isin(RACES)].assign(rc=lambda q: list(zip(q["cell"], q["race"]))), y, "lyp",
                       "rc", A4 + extra, "agei")
            Rp = Cells(st, y, "lyp", "cell", A4 + extra, "agei", w="wt")
            out[(sex, y, tuple(extra))] = (Rr, Rp)
            for b in BL:
                for grp, R, c in (("Pooled (weighted)", Rp, b), ("Black", Rr, (b, "Black")),
                                  ("White", Rr, (b, "White"))):
                    if R.has(c):
                        e, se, p = R.lin([(c, "x", 1)])
                        record(data="PSID", analysis=analysis, sex=sex, sample="unbalanced", band=b, group=grp,
                               outcome=ylab, stat="coef on ln parental income", est=e, se=se, p=p, **R.info[c])
                if Rr.has((b, "White")) and Rr.has((b, "Black")):
                    e, se, p = Rr.lin(gap_terms(b))
                    record(data="PSID", analysis=analysis, sex=sex, sample="unbalanced", band=b,
                           group="White - Black", outcome=ylab, stat="coef on ln parental income", est=e, se=se, p=p,
                           n=Rr.info[(b, "White")]["n"] + Rr.info[(b, "Black")]["n"])
            for mode, R in (("pooled", Rp), ("gap", Rr)):
                for t, e, se, p, txt in tests(R, BL, mode):
                    record(data="PSID", analysis=analysis, sex=sex, sample="unbalanced", band="test",
                           group={"pooled": "Pooled (weighted)", "gap": "White - Black"}[mode], outcome=ylab, stat=t,
                           est=e, se=se, p=p, note=txt)
    return out


def shares(s, cols, sexes):
    """mean of 0/1 flags by band x race (unweighted) and pooled (weighted)."""
    for sex, fem in sexes:
        x = s[s["female"].isin(fem)]
        for c, lab in cols:
            for b in BL:
                xb = x[(x["band"] == b) & x[c].notna()]
                for grp in ("Pooled (weighted)",) + RACES:
                    g = xb if grp.startswith("Pooled") else xb[xb["race"] == grp]
                    g = g[g["wt"] > 0] if grp.startswith("Pooled") else g
                    if len(g):
                        m = np.average(g[c], weights=g["wt"] if grp.startswith("Pooled") else None)
                        record(data="PSID", analysis="share", sex=sex, sample="unbalanced", band=b, group=grp,
                               outcome=lab, stat="mean", est=m, se=np.nan, p=np.nan, n=len(g))


# ================================================================ NLSY79
def nlsy_frames():
    n = pd.read_pickle(DATA / "nlsy79_kids.pkl")
    n = n[n["age79"] <= 18].copy()
    n["w"] = n["wt79"].astype(float)
    n["pinc"] = n["pinc_av"]
    n = n.set_index("pid")
    q = pd.read_pickle(DATA / "nlsy79_person_year.pkl")
    q = q[q["age"].between(25, 55)].copy()
    s = q.join(n[["pinc", "page_av", "w", "fam68"]], on="pid", how="inner")
    s["lyp"] = np.log(s["pinc"].where(s["pinc"] > 0))
    s["lfam"] = np.log(s["faminc"].where(s["faminc"].between(LO, HI)))
    s["learn"] = np.log(s["earn"].where(s["earn"].between(LO, HI)))
    for k in range(1, 5):
        s[f"A{k}"] = ((s["page_av"] - 45) / 10) ** k
    s["wt"] = s["w"]
    s["band"], s["agei"] = band_of(s["age"]), s["age"].round().astype(int)
    hw = q.set_index("pid")
    return s, n, hw


def nlsy_rank_frame(n, q):
    n = n.copy()
    n["rp"] = rank_in(n, "pinc", "birth_year")
    out = []
    for lab, (lo, hi) in list(zip(BL, BANDS)) + [(CH, (31, 37))]:
        h = q[q["age"].between(lo, hi)]
        f = h.dropna(subset=["faminc"]).groupby(level=0)["faminc"].agg(["mean", "count"])
        e = h.dropna(subset=["earn"]).groupby(level=0)["earn"].agg(["mean", "count"])
        x = n[["birth_year", "w", "rp", "race", "female", "fam68", "pinc"]].copy()
        x["yf"] = f.loc[f["count"] >= 2, "mean"].reindex(x.index)
        x["ye"] = e.loc[e["count"] >= 2, "mean"].reindex(x.index)
        x["band"] = lab
        out.append(x)
    return pd.concat(out).rename_axis("pid").reset_index()


# ================================================================ output
KEYS = ["data", "analysis", "sex", "sample", "band", "group", "outcome", "stat"]
RESD = {}


def get(*key):
    return RESD.get(key)


def c_(r, dec=3):
    return "" if r is None else cell(r.est, r.se, r.p, dec)


def n_(data, analysis, sex, sample, band, outcome, stat, groups=("Black", "White")):
    out = []
    for g in groups:
        r = get(data, analysis, sex, sample, band, g, outcome, stat)
        if r is not None and np.isfinite(r.get("children", np.nan)):
            out.append(f"{g[0]} {int(r.n):,} / {int(r.children):,} / {int(r.clusters):,}")
        elif r is not None:
            out.append(f"{g[0]} {int(r.n):,}")
    return "; ".join(out)


def band_table(data, analysis, sex, sample, cols, stat_of=None, groups=("Pooled (weighted)", "Black", "White",
                                                                         "White - Black"), bands=None, rowlab=None):
    """cols = [(outcome, stat, header, dec)]. Panels = bands, rows = groups, then N."""
    bands = bands or (BAL[sample] + ([CH] if sample == "unbalanced" else []))
    order = [b for b in BL if b in bands] + ([CH] if CH in bands else [])
    L = ["| | " + " | ".join(f"({i + 1}) {h}" for i, (_, _, h, _) in enumerate(cols)) + " |",
         "|---" * (len(cols) + 1) + "|"]
    for b in order:
        L.append(f"| **Age {b}{' (Chetty window)' if b == CH else ''}** |" + " |" * len(cols))
        for g in groups:
            L.append(f"| {rowlab or 'ln parental income'}: {g} | "
                     + " | ".join(c_(get(data, analysis, sex, sample, b, g, o, st), d) for o, st, _, d in cols) + " |")
        L.append("| N obs / children / clusters (B; W) | "
                 + " | ".join(n_(data, analysis, sex, sample, b, o, st) for o, st, _, _ in cols) + " |")
    return L


def test_table(data, analysis, sexes, sample, cols, groups=("Pooled (weighted)", "Black", "White", "White - Black")):
    L = ["| | " + " | ".join(f"({i + 1}) {h}" for i, (_, _, h) in enumerate(cols)) + " |",
         "|---" * (len(cols) + 1) + "|"]
    names = ["Equal in all bands (Wald chi2)", "Linear trend per 10 years", "Mean in bands < 35",
             "Mean in bands >= 35", "Mean < 35 minus mean >= 35"]
    for sex in sexes:
        for g in groups:
            L.append(f"| **{sex}: {g}** |" + " |" * len(cols))
            for t in names:
                cells, any_ = [], False
                for o, sx, _ in cols:
                    r = get(data, analysis, sex if sx is None else sx, sample, "test", g, o, t)
                    if r is None:
                        cells.append("")
                        continue
                    any_ = True
                    if t.startswith("Equal"):
                        pv = "<0.001" if r.p < 0.001 else f"{r.p:.3f}"
                        cells.append(f"{r.note}{stars(r.p)} (p={pv})")
                    else:
                        cells.append(c_(r))
                if any_:
                    L.append(f"| {t} | " + " | ".join(cells) + " |")
    return L


def write_md(curves):
    P = "PSID"
    L = ["# Intergenerational persistence by the child's age at measurement, by race", "",
         "Generated by `26.IGEByAge.py` (2026-10-17). Every cell: coefficient (s.e.; p-value), *** p<0.01, "
         "** p<0.05, * p<0.1; s.e. clustered by 1968 family (NLSY79: 1979 household), joint across bands (stacked, "
         "fully interacted), normal p-values. E[rank] p-values against 50. Race = parental household head's race. "
         "Black / White log IGE unweighted (as `6.IGEMain.py`); Pooled = all races, weighted (child-year core "
         "longitudinal weight); ranks always weighted (wt_pt, `7.RankMobility.py`). White - Black = difference of "
         "the two race regressions. N row: child-years (or child-bands) / children / clusters for Black (B) and "
         "White (W). Age = age at interview.", ""]
    # sample sizes
    L += ["## 0. Sample sizes by age band (PSID child-years with ln family income / children; NLSY79 likewise)", "",
          "| Band | Sons B | Sons W | Daughters B | Daughters W | NLSY79 sons B | NLSY79 sons W | NLSY79 daughters B "
          "| NLSY79 daughters W |", "|---" * 9 + "|"]
    for b in BL + [CH]:
        c = []
        for dt in ("PSID", "NLSY79"):
            for sex in ("Sons", "Daughters"):
                for g in RACES:
                    r = get(dt, "log IGE, child-year", sex, "unbalanced", b, g, "ln family income", "IGE")
                    c.append("" if r is None else f"{int(r.n):,} / {int(r.children):,}")
        L.append(f"| {b} | " + " | ".join(c) + " |")
    L.append("")
    fam, ern = "ln family income", "ln own earnings"
    for sample in BAL:
        L += [f"## 1{'abc'[list(BAL).index(sample)]}. PSID log IGE by age band, {sample}", "",
              "Columns (1)/(3): child-year regressions within the band (A quartic + single-year age dummies); "
              "(2)/(4): one row per child, ln of the band mean (>= 2 years), A quartic + mean age."
              + (" Balanced: the same children in every band listed." if sample != "unbalanced" else ""), ""]
        for sex in ("Sons", "Daughters"):
            L += [f"### {sex}", ""]
            cols = [(fam, "IGE", "ln family income (child-years)", 3), (fam, "IGE", "ln family income (band mean)", 3),
                    (ern, "IGE", "ln own earnings (child-years)", 3), (ern, "IGE", "ln own earnings (band mean)", 3)]
            L += _mixed_band_table(P, sex, sample, cols) + [""]
    L += ["## 2. Tests: does the IGE, and the Black-White gap in it, change with age? (PSID, child-year design)", "",
          "Rows per panel: Wald test that the slope (or the White - Black gap) is equal in all bands; linear trend of "
          "it in the band midpoint per 10 years; mean in bands < 35, mean in bands >= 35 and their difference. "
          "The 31-37 window is excluded.", ""]
    for sample in BAL:
        L += [f"### {sample}", ""]
        L += test_table(P, "log IGE, child-year", ("Sons", "Daughters"), sample,
                        [(fam, None, "ln family income"), (ern, None, "ln own earnings")]) + [""]
    L += ["### Race-specific weighted (child-year core longitudinal weight; child-year design, unbalanced)", "",
          "| | (1) ln family income | (2) ln own earnings |", "|---|---|---|"]
    for sex in ("Sons", "Daughters"):
        for b in BL + [CH]:
            L.append(f"| **{sex}, age {b}** | | |")
            for g in ("Black (weighted)", "White (weighted)", "White - Black (weighted)"):
                L.append(f"| ln parental income: {g} | " + " | ".join(
                    c_(get(P, "log IGE, child-year", sex, "unbalanced", b, g, o, "IGE")) for o in (fam, ern)) + " |")
    L.append("")
    L += test_table(P, "log IGE, child-year", ("Sons", "Daughters"), "unbalanced",
                    [(fam, None, "ln family income"), (ern, None, "ln own earnings")],
                    groups=("Black (weighted)", "White (weighted)", "White - Black (weighted)")) + [""]
    L += ["## 3. Lee-Solon age-interacted IGE at each age (one regression per column, PSID, child-years 25-55)", "",
          "ln parental income x quartic in (age - 40)/10 with the quartics of `6.IGEMain.py`; the row is the IGE "
          "at that age (delta-method s.e.). White - Black: independent samples. Sample 25-55 (not 25-65), so the "
          "age-40 value differs slightly from `ige_main.md`.", ""]
    for sex in ("Sons", "Daughters"):
        for y in (fam, ern):
            L += [f"### {sex}, {y}", "", "| Age | (1) Pooled (weighted) | (2) Black | (3) White | (4) White - Black |",
                  "|---|---|---|---|---|"]
            for age in range(25, 56):
                L.append(f"| {age} | " + " | ".join(cell(*curves[P][(sex, y, g, age)]) for g in
                                                    ("Pooled (weighted)", "Black", "White", "White - Black")) + " |")
            ch = [get(P, "Lee-Solon", sex, "unbalanced", f"{a1} minus {a0}", g, y,
                      "Change in gap" if g == "White - Black" else "Change in IGE")
                  for a0, a1 in ((30, 45), (33, 45), (34, 50)) for g in ("Pooled (weighted)", "White - Black")]
            L.append("| Change 30 -> 45 (pooled; W-B gap) | " + c_(ch[0]) + " | | | " + c_(ch[1]) + " |")
            L.append("| Change 33 -> 45 (pooled; W-B gap) | " + c_(ch[2]) + " | | | " + c_(ch[3]) + " |")
            L.append("| Change 34 -> 50 (pooled; W-B gap) | " + c_(ch[4]) + " | | | " + c_(ch[5]) + " |")
            r = get(P, "Lee-Solon", sex, "unbalanced", "40", "Black", y, "IGE at age")
            L += [f"| N child-years / children (B) | | {int(r.n):,} / {int(r.children):,} | | |", ""]
    for sample in BAL:
        L += [f"## 4{'abc'[list(BAL).index(sample)]}. PSID rank mobility by age band, {sample}", "",
              "Child's band-mean family income (or own earnings, zeros kept) ranked within birth year and band; "
              "parents ranked within birth year (12-17 mean). Columns: (1) rank-rank slope, family income; (2)/(3) "
              "E[rank] at parental p25 / p75 from that line; (4) rank-rank slope, own earnings.", ""]
        for sex in ("Both", "Sons", "Daughters"):
            L += [f"### {'Both sexes' if sex == 'Both' else sex}", ""]
            L += band_table(P, "rank", sex, sample,
                            [(fam, "slope", "Rank slope, family income", 3),
                             (fam, "E[rank] p25", "E[rank] at p25", 1), (fam, "E[rank] p75", "E[rank] at p75", 1),
                             (ern, "slope", "Rank slope, own earnings", 3)], rowlab="parent rank") + [""]
        L += ["Tests (rank-rank slope; the E[rank] at p25 gap is not tested across bands):", ""]
        L += test_table(P, "rank", ("Both", "Sons", "Daughters"), sample,
                        [(fam, None, "Rank slope, family income"), (ern, None, "Rank slope, own earnings")]) + [""]
    # interpretation checks
    L += ["## 5. Interpretation checks (PSID)", "", "### 5.1 Haider-Solon: income growth by parental income "
          "(fixed children observed in both bands)", "",
          "One regression per column: (1) mean ln y in the early band, (2) in the late band, (3) late - early "
          "(controls: A quartic; (3) also the change in mean age). (3) is the change of the IGE with age in a fixed "
          "sample; > 0 means children of richer parents have steeper growth.", ""]
    for sex in ("Sons", "Daughters"):
        for y in (fam, ern):
            L += [f"#### {sex}, {y}", "", "| | (1) IGE early band | (2) IGE late band | (3) Growth gradient |",
                  "|---|---|---|---|"]
            for e0, e1 in PAIRS:
                smp = f"{e0} -> {e1}"
                L.append(f"| **{smp}** | | | |")
                for g in ("Pooled (weighted)", "Black", "White", "White - Black"):
                    L.append(f"| ln parental income: {g} | " + " | ".join(
                        c_(get(P, "growth", sex, smp, lab, g, y, st)) for lab, st in
                        ((f"IGE at {e0}", "y0"), (f"IGE at {e1}", "y1"), ("Growth gradient", "dy"))) + " |")
                L.append("| N children (B; W) | " + " | ".join(
                    n_(P, "growth", sex, smp, lab, y, st) for lab, st in
                    ((f"IGE at {e0}", "y0"), (f"IGE at {e1}", "y1"), ("Growth gradient", "dy"))) + " |")
            L.append("")
    L += ["### 5.2 Marriage: partnership gradient and family income vs own earnings (child-years)", "",
          "(1) partnered (spouse / partner in the child's family unit) on ln parental income (LPM); (2) ln family "
          "income IGE; (3) the same controlling for partnered; (4) ln own earnings IGE. Controls: A quartic, "
          "single-year age dummies. Row 'Mean partnered' = share partnered.", ""]
    for sex in ("Sons", "Daughters"):
        L += [f"#### {sex}", "", "| | (1) Partnered (LPM) | (2) ln family income | (3) ln family income, "
              "partnered control | (4) ln own earnings |", "|---|---|---|---|---|"]
        for b in BL:
            L.append(f"| **Age {b}** | | | | |")
            for g in ("Pooled (weighted)", "Black", "White", "White - Black"):
                L.append(f"| ln parental income: {g} | " + " | ".join(
                    c_(get(P, "marriage", sex, "unbalanced", b, g, o, "coef on ln parental income")) for o in
                    ("partnered", fam, fam + " | partnered", ern)) + " |")
            sh = [get(P, "share", sex, "unbalanced", b, g, "partnered", "mean") for g in ("Pooled (weighted)",) + RACES]
            L.append("| Mean partnered (pooled; B; W) | " + "; ".join("" if r is None else f"{r.est:.3f}" for r in sh)
                     + " | | | |")
            L.append("| N obs / children / clusters (B; W) | " + " | ".join(
                n_(P, "marriage", sex, "unbalanced", b, o, "coef on ln parental income") for o in
                ("partnered", fam, fam + " | partnered", ern)) + " |")
        L.append("")
    L += test_table(P, "marriage", ("Sons", "Daughters"), "unbalanced",
                    [("partnered", None, "Partnered"), (fam, None, "ln family income"),
                     (fam + " | partnered", None, "ln family income | partnered"), (ern, None, "ln own earnings")],
                    groups=("Pooled (weighted)", "White - Black")) + [""]
    L += ["### 5.3 Instability (sons as male heads; flags of `24.IGEDecomposition.py`)", "",
          "(1) displaced or unemployed in the year (LPM); (2) reduced hours (< 1,500, full-time attached); (3) zero "
          "hours; (4) ln earnings IGE, all valid years (hours >= 100, wage $2-$200); (5) ln earnings IGE, clean "
          "years (valid, not displaced / unemployed); (6) ln family income IGE excluding displaced / unemployed / "
          "zero-hours years. Row 'Mean' = share of child-years with the flag (pooled; B; W).", ""]
    icols = [("shock", "Displaced / unemployed"), ("red", "Reduced hours"), ("zero", "Zero hours"),
             ("ly_valid", "ln earnings, valid years"), ("ly_clean", "ln earnings, clean years"),
             ("lfam_clean", "ln family income, clean years")]
    L += ["| | " + " | ".join(f"({i + 1}) {h}" for i, (_, h) in enumerate(icols)) + " |", "|---" * 7 + "|"]
    for b in BL:
        L.append(f"| **Age {b}** |" + " |" * 6)
        for g in ("Pooled (weighted)", "Black", "White", "White - Black"):
            L.append(f"| ln parental income: {g} | " + " | ".join(
                c_(get(P, "instability", "Sons", "unbalanced", b, g, o, "coef on ln parental income"))
                for o, _ in icols) + " |")
        sh = []
        for o, _ in icols[:3]:
            rr = [get(P, "share", "Sons", "unbalanced", b, g, o, "mean") for g in ("Pooled (weighted)",) + RACES]
            sh.append("; ".join("" if r is None else f"{r.est:.3f}" for r in rr))
        L.append("| Mean (pooled; B; W) | " + " | ".join(sh) + " | | | |")
        L.append("| N obs / children / clusters (B; W) | " + " | ".join(
            n_(P, "instability", "Sons", "unbalanced", b, o, "coef on ln parental income") for o, _ in icols) + " |")
    L.append("")
    L += test_table(P, "instability", ("Sons",), "unbalanced", [(o, None, h) for o, h in icols],
                    groups=("Pooled (weighted)", "White - Black")) + [""]
    dcols = [("est23", "Laid off / looking at interview"), ("zero", "Zero hours")]
    L += ["Daughters (heads or wives):", "",
          "| | " + " | ".join(f"({i + 1}) {h}" for i, (_, h) in enumerate(dcols)) + " |", "|---|---|---|"]
    for b in BL:
        L.append(f"| **Age {b}** | | |")
        for g in ("Pooled (weighted)", "Black", "White", "White - Black"):
            L.append(f"| ln parental income: {g} | " + " | ".join(
                c_(get(P, "instability", "Daughters", "unbalanced", b, g, o, "coef on ln parental income"))
                for o, _ in dcols) + " |")
        sh = []
        for o, _ in dcols:
            rr = [get(P, "share", "Daughters", "unbalanced", b, g, o, "mean") for g in ("Pooled (weighted)",) + RACES]
            sh.append("; ".join("" if r is None else f"{r.est:.3f}" for r in rr))
        L.append("| Mean (pooled; B; W) | " + " | ".join(sh) + " |")
    L.append("")
    # NLSY79
    L += ["### 5.4 Log IGE vs rank slope on the same children and weights (PSID, family income)", "",
          "Rank frame of section 4 (parents 12-17, child band mean >= 2 years), children with positive band-mean "
          "income, weighted by wt_pt, no controls. Log IGE = Corr(logs) x SD ratio (logs); rank slope = Corr(ranks) x "
          "SD ratio (ranks; national ranks within birth year and band). Hybrids: ln child income on parent rank / "
          "100 and child rank on ln parental income. Bootstrap s.e. (200 draws of 1968 families, ranks fixed); "
          "p-values against 0 (correlation / SD-ratio p-values are therefore trivial).", ""]
    for P, sex in (("PSID", "Both"), ("PSID", "Sons"), ("PSID", "Daughters"), ("NLSY79", "Both")):
        L += [f"#### {P}, {'both sexes' if sex == 'Both' else sex.lower()}", "",
              "| | " + " | ".join(f"({i + 1}) {lab}" for i, (_, lab) in enumerate(LVR)) + " |", "|---" * 9 + "|"]
        for b in BL + [CH]:
            L.append(f"| **Age {b}** |" + " |" * len(LVR))
            for g in ("Black", "White", "White - Black"):
                L.append(f"| {g} | " + " | ".join(c_(get(P, "log vs rank", sex, "unbalanced", b, g, "family income", st))
                                                 for st, _ in LVR) + " |")
            r = [get(P, "log vs rank", sex, "unbalanced", b, g, "family income", "ige") for g in RACES]
            L.append(f"| N children (B; W) | {int(r[0].n):,}; {int(r[1].n):,} |" + " |" * (len(LVR) - 1))
        L.append("| **Gap change: mean gap at >= 35 minus mean gap at < 35** | " + " | ".join(
            c_(get(P, "log vs rank", sex, "unbalanced", "test", "White - Black", "family income",
                   st + ": gap >=35 minus <35")) for st, _ in LVR) + " |")
        L.append("")
    P = "PSID"
    L += ["## 6. NLSY79 (cohorts 1960-64): log IGE and rank mobility by age band", "",
          "Parents: mean family income 1978-80 rounds; controls: quartic in (parent's age - 45)/10 and single-year "
          "age dummies; Pooled = Black + White weighted by wt79 (the NLSY79 file holds Black and non-Black "
          "non-Hispanic respondents only). Ranks as in section 4.", ""]
    for sample in BAL:
        L += [f"### 6{'abc'[list(BAL).index(sample)]}. {sample}", ""]
        for sex in ("Sons", "Daughters"):
            L += [f"#### {sex}: log IGE (child-years)", ""]
            L += band_table("NLSY79", "log IGE, child-year", sex, sample,
                            [(fam, "IGE", "ln family income", 3), (ern, "IGE", "ln own earnings", 3)]) + [""]
        for sex in ("Both", "Sons", "Daughters"):
            L += [f"#### {'Both sexes' if sex == 'Both' else sex}: ranks", ""]
            L += band_table("NLSY79", "rank", sex, sample,
                            [(fam, "slope", "Rank slope, family income", 3),
                             (fam, "E[rank] p25", "E[rank] at p25", 1), (fam, "E[rank] p75", "E[rank] at p75", 1),
                             (ern, "slope", "Rank slope, own earnings", 3)], rowlab="parent rank") + [""]
        L += ["Tests:", ""]
        L += test_table("NLSY79", "log IGE, child-year", ("Sons", "Daughters"), sample,
                        [(fam, None, "log IGE, family income"), (ern, None, "log IGE, own earnings")]) + [""]
        L += test_table("NLSY79", "rank", ("Both", "Sons", "Daughters"), sample,
                        [(fam, None, "Rank slope, family income"), (ern, None, "Rank slope, own earnings")]) + [""]
    L += ["## 7. NLSY79 Lee-Solon age-interacted IGE at selected ages", "",
          "| Age | " + " | ".join(f"({i + 1}) {s}, {y}, {g}" for i, (s, y, g) in enumerate(
              [(s, y, g) for s in ("Sons", "Daughters") for y in (fam,) for g in ("Black", "White",
                                                                                    "White - Black")])) + " |",
          "|---" * 7 + "|"]
    for age in (25, 28, 31, 34, 37, 40, 43, 46, 50, 55):
        L.append(f"| {age} | " + " | ".join(cell(*curves["NLSY79"][(s, fam, g, age)]) for s in ("Sons", "Daughters")
                                            for g in ("Black", "White", "White - Black")) + " |")
    L.append("")
    (OUT / "ige_by_age.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def _mixed_band_table(P, sex, sample, cols):
    """log IGE table mixing the child-year and band-mean analyses (columns alternate)."""
    an = ["log IGE, child-year", "log IGE, band mean", "log IGE, child-year", "log IGE, band mean"]
    bands = BAL[sample] + ([CH] if sample == "unbalanced" else [])
    L = ["| | " + " | ".join(f"({i + 1}) {h}" for i, (_, _, h, _) in enumerate(cols)) + " |",
         "|---" * (len(cols) + 1) + "|"]
    for b in bands:
        L.append(f"| **Age {b}{' (Chetty window)' if b == CH else ''}** |" + " |" * len(cols))
        for g in ("Pooled (weighted)", "Black", "White", "White - Black"):
            L.append(f"| ln parental income: {g} | " + " | ".join(
                c_(get(P, a, sex, sample, b, g, o, st)) for a, (o, st, _, _) in zip(an, cols)) + " |")
        L.append("| N obs / children / clusters (B; W) | " + " | ".join(
            n_(P, a, sex, sample, b, o, st) for a, (o, st, _, _) in zip(an, cols)) + " |")
    return L


def figure(curves):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    col = {"Black": "#eb6834", "White": "#2a78d6", "Pooled (weighted)": "#1baf7a"}
    off = {"Black": -0.6, "White": 0.6, "Pooled (weighted)": 0.0}
    fig, axes = plt.subplots(4, 3, figsize=(13, 14), sharex=True)
    spec = [("log IGE, child-year", "ln family income", "IGE"), ("log IGE, child-year", "ln own earnings", "IGE"),
            ("rank", "ln family income", "slope")]
    titles = ["Log IGE, family income", "Log IGE, own earnings", "Rank-rank slope, family income"]
    for i, (dt, sex) in enumerate([("PSID", "Sons"), ("PSID", "Daughters"), ("NLSY79", "Sons"),
                                   ("NLSY79", "Daughters")]):
        for j, (an, y, st) in enumerate(spec):
            ax = axes[i, j]
            for g in ("Pooled (weighted)", "Black", "White"):
                pts = [(MID[b] + off[g], get(dt, an, sex, "unbalanced", b, g, y, st)) for b in BL]
                pts = [(x, r) for x, r in pts if r is not None]
                if not pts:
                    continue
                xs = np.array([x for x, _ in pts])
                es = np.array([r.est for _, r in pts])
                ss = np.array([r.se for _, r in pts])
                ls = "--" if g.startswith("Pooled") else "-"
                ax.errorbar(xs, es, yerr=1.96 * ss, color=col[g], ls=ls, lw=2, marker="o", ms=6, capsize=0,
                            elinewidth=1.2, label=g if (i == 0 and j == 0) else None)
                if j < 2 and (sex, y, g, 25) in curves[dt]:
                    ages = np.arange(25, 56)
                    ax.plot(ages, [curves[dt][(sex, y, g, a)][0] for a in ages], color=col[g], lw=0.9, alpha=0.6,
                            ls=":")
            ax.axvspan(31, 37, color="#999999", alpha=0.12, lw=0)
            ax.axhline(0, color="#bbbbbb", lw=0.8)
            ax.grid(axis="y", color="#e5e5e5", lw=0.6)
            for sp in ("top", "right"):
                ax.spines[sp].set_visible(False)
            if i == 0:
                ax.set_title(titles[j], fontsize=11)
            if j == 0:
                ax.set_ylabel(f"{dt} {sex.lower()}", fontsize=11)
            if i == 3:
                ax.set_xlabel("Child's age at measurement (band midpoint)")
    fig.legend(loc="upper center", ncol=3, frameon=False, fontsize=10, bbox_to_anchor=(0.5, 0.995))
    fig.text(0.5, 0.005, "Points: band estimates with 95% CI (unbalanced). Dotted lines: Lee-Solon age-interacted "
             "IGE. Shaded: Chetty et al. window 31-37.", ha="center", fontsize=9, color="#52514e")
    fig.tight_layout(rect=(0, 0.015, 1, 0.975))
    fig.savefig(OUT / "ige_by_age.png", dpi=150)


def main():
    global RES
    curves = {}
    fam, ern = "ln family income", "ln own earnings"
    outs = [("lfam", fam, "faminc"), ("learn", ern, "earn")]
    sexes = {"Sons": [0], "Daughters": [1]}
    # ---------------- PSID
    s, k, hw = psid_frames()
    print("PSID frames built", flush=True)
    logige_block("PSID", s, sexes, outs, "child-year", members_balanced)
    logige_block("PSID", s, sexes, outs, "band mean", members_balanced)
    print("PSID log IGE done", flush=True)
    curves["PSID"] = lee_solon_curve("PSID", s, sexes, outs)
    r0 = rank_frame(k.set_index("pid"), hw.set_index("pid"), idcol="pid")
    rank_block("PSID", r0, SEXES, [("yf", fam), ("ye", ern)])
    print("PSID ranks done", flush=True)
    growth_block(s)
    log_vs_rank("PSID", r0)
    s["lfam_p"] = s["lfam"]
    simple_band_block(s, "marriage", [("partnered", "partnered", []), ("lfam", fam, []),
                                      ("lfam_p", fam + " | partnered", ["partnered"]), ("learn", ern, [])],
                      [("Sons", [0]), ("Daughters", [1])])
    simple_band_block(s.assign(shock=s["shockm"], red=s["redm"], zero=s["zerom"]), "instability",
                      [(c, c, []) for c in ("shock", "red", "zero", "ly_valid", "ly_clean", "lfam_clean")],
                      [("Sons", [0])])
    simple_band_block(s, "instability", [("est23", "est23", []), ("zero", "zero", [])], [("Daughters", [1])])
    shares(s, [("partnered", "partnered")], [("Sons", [0]), ("Daughters", [1])])
    shares(s.assign(shock=s["shockm"], red=s["redm"], zero=s["zerom"]), [("shock", "shock"), ("red", "red"),
                                                                          ("zero", "zero")], [("Sons", [0])])
    shares(s, [("est23", "est23"), ("zero", "zero")], [("Daughters", [1])])
    print("PSID checks done", flush=True)
    # ---------------- NLSY79
    ns, nk, nq = nlsy_frames()
    logige_block("NLSY79", ns, sexes, outs, "child-year", members_balanced)
    curves["NLSY79"] = lee_solon_curve("NLSY79", ns, sexes, [("lfam", fam, "faminc")])
    nr0 = nlsy_rank_frame(nk, nq)
    rank_block("NLSY79", nr0, SEXES, [("yf", fam), ("ye", ern)])
    log_vs_rank("NLSY79", nr0)
    print("NLSY79 done", flush=True)
    RES = pd.DataFrame(ROWS)
    RESD.update({tuple(r[k] for k in KEYS): r for _, r in RES.iterrows()})
    OUT.mkdir(exist_ok=True)
    RES.to_csv(OUT / "ige_by_age.csv", index=False)
    write_md(curves)
    figure(curves)
    show = RES[(RES["sample"] == "unbalanced") & RES["stat"].isin(["IGE", "slope"])
               & RES["analysis"].isin(["log IGE, child-year", "rank"])]
    show = show.assign(c=[cell(e, se, p) for e, se, p in zip(show.est, show.se, show.p)])
    pd.set_option("display.width", 250)
    print(show.pivot_table(index=["data", "analysis", "outcome", "sex", "group"], columns="band", values="c",
                           aggfunc="first", sort=False).to_string())


RES = None
if __name__ == "__main__":
    main()
