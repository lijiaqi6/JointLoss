r"""Paper B measurement checks asked for by the Fable review (proposals/fable_review_paperB.md, Item 1 and Item 5;
2026-10-17).

The fact tested: in the PSID the White - Black gap in the sons' log IGE is ~0 at 25-29 and opens after 30 (gap change
= mean gap in bands >= 35 minus mean gap in bands < 35: 0.157*** on family income, bands 25-49, 33.AgeProfileRobustness).
Standard objections and the check that answers each:
  A ATTRITION (Fitzgerald-Gottschalk-Moffitt 1998). Sons observed at 25-29 and old enough to reach a later band: is
    being observed later (as head / spouse with valid income) related to ln parental income, by race, given income at
    25-29? Then the age profile on these sons unweighted and with inverse-probability weights for staying.
  B AGE, PERIOD, COHORT (Bayer-Charles 2018: rising within-White inequality over calendar time). (i) income-year fixed
    effects in every band x race cell; (ii) a period-varying IGE: ln parental income x (year - 1995)/10 in every cell,
    the band IGE evaluated in 1995 (33 has the cohort-varying analogue); (iii) a fixed calendar window, income years
    1990-2010, in which the bands hold different cohorts; (iv) within-race SD of ln income (net of single-age means) by
    band for fixed birth cohorts, with the SD of ln parental income of the same children.
  C HAIDER-SOLON lambda BY RACE (Haider-Solon 2006; Nybom-Stuhler 2016 heterogeneous profiles). Sons observed in each of
    25-34, 35-44 and 45-55 (>= 3 valid years in each): ybar = mean over 25-55 of ln y net of race-specific single-age
    means; lambda_b = slope of current (net) ln y on ybar within band b and race; kappa_b = coefficient on ln parental
    income when it is added (non-zero kappa = profiles that differ with background). Also by pooled parental tercile.
  D POSITION IN THE DISTRIBUTION vs RACE. (i) binned means of ln income by pooled parental-income vigintile at 25-29
    and 40-49, by race (figure); (ii) the age profile with both races restricted to parents below the pooled median /
    in the bottom tercile; (iii) White sons re-weighted (by band) to the Black distribution of ln parental income over
    the 20 pooled vigintile bins (DiNardo-Fortin-Lemieux).
  E OTHER METRICS. (i) within-race ranks: child band-mean family income ranked within race x birth year x band, parents
    within race x birth year (weights wt_pt, the rank frame of 26); national ranks on the same children for comparison;
    (ii) dollar-weighted IGE (Mitnik et al. 2015; Mitnik-Grusky 2020): Poisson pseudo-ML of the income LEVEL on ln
    parental income (zeros kept for earnings), same controls, by band and race.
  F ITEM 5: one common corrected estimate across PSID / NLSY79 / NLSY97. One-year parental income in every data set
    (33's side-by-side panel (b)), each race's IGE divided by the PSID one-year reliability ratio (W 0.585, B 0.565;
    4.Estimates.py), gap change on bands 25-44, inverse-variance pooled; sons' family income and own earnings.
DESIGN: 33's child-year design and engine (ln y on ln parental income, quartic in parent's age at 16, single-year age
dummies, Black / White unweighted, every band x race cell its own regression, stacked cluster-robust covariance with
clusters = 1968 family, so differences between specifications on the same children are tested properly). Bands 25-49.
Writes output/age_profile_measurement.csv, .md and .png. Nothing raw is written.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.linalg import block_diag
from scipy.stats import chi2, norm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import DATA, OUT, stars  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R33 = _load("ige33", "33.AgeProfileRobustness.py")
R26 = _load("ige26", "26.IGEByAge.py")
ige6 = R33.ige6
BL, BL4, MID, RACES, A4, GC = R33.BL, R33.BL4, R33.MID, R33.RACES, R33.A4, R33.GC
FAM, ERN = R33.FAM, R33.ERN
OUTS = [("lfam", FAM), ("learn", ERN)]
prep, run, summarize, diff = R33.prep, R33.run, R33.summarize, R33.diff
ROWS = R33.ROWS
record = R33.record
EXTRA = []                                  # rows that are not band x race estimates
LAST_WAVE = 2023


def rec2(**k):
    EXTRA.append(k)


def cell(e, se, p, dec=3):
    if e is None or not np.isfinite(e):
        return ""
    pv = "<0.001" if p < 0.001 else f"{p:.3f}"
    return f"{e:.{dec}f}{stars(p)} ({se:.{dec}f}; p={pv})"


# ================================================================ Poisson cells (dollar-weighted IGE)
class PCells:
    """Poisson pseudo-ML in each cell; joint cluster-robust covariance of the stacked, fully interacted model."""

    def __init__(self, d, y, x, cell_, ctrl=(), fe=None, w=None, cluster="fam68", pid="pid"):
        cols = list(dict.fromkeys([cell_, y, x, *ctrl, cluster, pid] + ([fe] if fe else []) + ([w] if w else [])))
        d = d[cols].replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)
        gid = pd.factorize(d[cluster])[0]
        G = gid.max() + 1
        self.names, breads, scores, self.b, self.info = [], [], [], [], {}
        for c, g in d.groupby(cell_, sort=False):
            X = pd.DataFrame({"const": 1.0, "x": g[x].astype(float)}, index=g.index)
            for k in ctrl:
                X[k] = g[k].astype(float)
            if fe:
                X = X.join(pd.get_dummies(g[fe].astype(int), prefix="fe", drop_first=True, dtype=float))
            X = X.loc[:, (X.std() > 1e-12) | (X.columns == "const")]
            Xa = X.to_numpy()
            yy = g[y].to_numpy(float)
            yy = yy / yy.mean()
            ww = g[w].to_numpy(float) if w else np.ones(len(g))
            bb = np.zeros(Xa.shape[1])
            bb[0] = np.log(np.average(yy, weights=ww))
            for _ in range(100):
                mu = np.exp(Xa @ bb)
                H = Xa.T @ (Xa * (ww * mu)[:, None])
                step = np.linalg.solve(H, Xa.T @ (ww * (yy - mu)))
                bb += step
                if np.max(np.abs(step)) < 1e-10:
                    break
            mu = np.exp(Xa @ bb)
            Bi = np.linalg.pinv(Xa.T @ (Xa * (ww * mu)[:, None]))
            u = Xa * (ww * (yy - mu))[:, None]
            S = np.zeros((G, Xa.shape[1]))
            np.add.at(S, gid[g.index.to_numpy()], u)
            breads.append(Bi)
            scores.append(S)
            self.b.extend(bb)
            self.names.extend((c, n) for n in X.columns)
            self.info[c] = dict(n=len(g), children=g[pid].nunique(), clusters=g[cluster].nunique())
        B, S = block_diag(*breads), np.hstack(scores)
        self.V = B @ (S.T @ S) @ B.T * G / (G - 1)
        self.b = np.array(self.b)
        self.ix = {n: i for i, n in enumerate(self.names)}

    has = R33.Cells.has
    lin = R33.Cells.lin
    wald = R33.Cells.wald


def run_ppml(frames, ctrl, fe="agei"):
    parts = []
    for spec, d in frames.items():
        d = d[d["_y"].notna() & d["lyp"].notna() & d["race"].isin(RACES) & d["band"].notna()]
        d = d.assign(cellk=[(spec, b, r) for b, r in zip(d["band"], d["race"])])
        cnt = d.groupby("cellk").agg(n=("pid", "size"), ch=("pid", "nunique"))
        ok = set(cnt[(cnt["n"] >= R33.MIN_N) & (cnt["ch"] >= R33.MIN_CH)].index)
        okb = {(s_, b) for s_, b, r in ok if (s_, b, "Black") in ok and (s_, b, "White") in ok}
        d = d[[(s_, b) in okb for s_, b, _ in d["cellk"]]]
        parts.append(d[["cellk", "_y", "lyp", "_w", "fam68", "pid", fe, *ctrl]])
    st = pd.concat(parts, ignore_index=True)
    return PCells(st, "_y", "lyp", "cellk", ctrl, fe, w="_w")


# ================================================================ frames
def psid_all():
    """33's PSID child-year frame (ages 25-49) plus raw levels for PPML."""
    s = R33.psid_frames()
    s["famlev"] = s["faminc"].where(s["faminc"].between(0, ige6.HI))
    s["earnlev"] = s["earn"].where(s["earn"].between(0, ige6.HI)).where(s["head"] & (s["female"] == 0) | s["wife"])
    s["coh5"] = (s["birth_year"] // 5) * 5
    return s


# ================================================================ A attrition
def ols_cl(d, y, xs, cluster="fam68"):
    d = d.dropna(subset=[y, *xs, cluster])
    X = sm.add_constant(d[xs].astype(float), has_constant="add")
    r = sm.OLS(d[y].astype(float), X).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d[cluster])[0]})
    return r, len(d), d["pid"].nunique()


def attrition_block(s):
    """returns the IPW-weighted son frame; records the attrition regressions."""
    out = []
    for sex, fem in (("Sons", 0), ("Daughters", 1)):
        x = s[(s["female"] == fem) & s["race"].isin(RACES) & s["lfam"].notna()]
        e = x[x["band"] == "25-29"].groupby("pid").agg(early=("lfam", "mean"))
        kid = (x.groupby("pid")[["lyp", "race", "fam68", "birth_year", "src", *A4]].first().join(e, how="inner"))
        kid["black"] = (kid["race"] == "Black").astype(float)
        for c in ("lyp", "early"):
            kid[c + "_c"] = kid[c] - kid[c].mean()
            kid[c + "_B"] = kid[c + "_c"] * kid["black"]
        kid["coh5"] = (kid["birth_year"] // 5) * 5
        cd = pd.get_dummies(kid["coh5"], prefix="c", drop_first=True, dtype=float)
        kid = kid.join(cd)
        cdn = list(cd.columns)
        seen = {b: set(x.loc[x["band"] == b, "pid"]) for b in BL}
        kid["ipw_25-29"] = 1.0
        for b in BL[1:]:
            lo = int(b[:2])
            elig = kid[kid["birth_year"] + lo + 2 <= LAST_WAVE].copy()
            elig["obs"] = elig.index.isin(seen[b]).astype(float)
            # LPM: is being observed in band b related to parental income, by race?
            for spec, xs in (("lyp", ["lyp_c", "lyp_B", "black"]),
                             ("lyp + early income", ["lyp_c", "lyp_B", "black", "early_c", "early_B"])):
                r, n, nc = ols_cl(elig.reset_index(), "obs", xs + A4 + cdn)
                V = r.cov_params()
                for g, terms in (("White", {"lyp_c": 1}), ("Black", {"lyp_c": 1, "lyp_B": 1}),
                                 ("Black - White", {"lyp_B": 1})):
                    est = sum(r.params[k] * v for k, v in terms.items())
                    var = sum(V.loc[k1, k2] * v1 * v2 for k1, v1 in terms.items() for k2, v2 in terms.items())
                    se = np.sqrt(var)
                    rec2(block="attrition", sex=sex, band=b, spec=spec, group=g, stat="P(observed) on ln parental income",
                         est=est, se=se, p=2 * (1 - norm.cdf(abs(est / se))), n=n, children=nc,
                         mean=elig["obs"].mean())
                if spec == "lyp + early income":
                    for g, k in (("White", "early_c"), ("Black - White", "early_B")):
                        rec2(block="attrition", sex=sex, band=b, spec=spec, group=g,
                             stat="P(observed) on ln income at 25-29", est=r.params[k], se=r.bse[k], p=r.pvalues[k],
                             n=n)
            for g in RACES:
                rec2(block="attrition", sex=sex, band=b, spec="share observed", group=g, stat="share",
                     est=elig.loc[elig["race"] == g, "obs"].mean(), se=np.nan, p=np.nan,
                     n=int((elig["race"] == g).sum()))
            # logit for the weights
            Z = sm.add_constant(elig[["lyp_c", "lyp_B", "black", "early_c", "early_B", "src", *A4, *cdn]]
                                .astype(float), has_constant="add")
            try:
                lg = sm.Logit(elig["obs"], Z).fit(disp=0, maxiter=200)
                ph = lg.predict(Z)
            except Exception:                                      # perfect prediction in a small cohort
                ph = sm.OLS(elig["obs"], Z).fit().predict(Z)
            kid.loc[elig.index, f"ipw_{b}"] = 1 / np.clip(ph, 0.05, 1.0)
        out.append(kid)
    kid = pd.concat(out)
    # child-year frame of the base children with their band weight
    base = s[s["pid"].isin(kid.index) & s["race"].isin(RACES)].copy()
    wmap = {b: kid[f"ipw_{b}"] for b in BL}
    base["ipw"] = [wmap[b].get(p, np.nan) if isinstance(b, str) else np.nan for b, p in zip(base["band"], base["pid"])]
    return base


def attrition_runs(base):
    for sex, fem in (("Sons", 0), ("Daughters", 1)):
        x = base[base["female"] == fem]
        for y, ylab in OUTS:
            fr = {"Observed at 25-29, unweighted": prep(x, y, "lyp"),
                  "Observed at 25-29, IPW for staying": prep(x[x["ipw"].notna()], y, "lyp", w="ipw")}
            R = run(fr, A4)
            for lab in fr:
                summarize(R, "PSID", "attrition", lab, sex, ylab)
            diff(R, "PSID", "attrition", "Observed at 25-29, IPW for staying", "Observed at 25-29, unweighted", sex,
                 ylab)
        print(f"attrition {sex} done", flush=True)


# ================================================================ B age / period / cohort
def apc_runs(s):
    s = s.copy()
    s["p1"] = (s["year"] - 1995) / 10
    s["p2"] = s["p1"] ** 2
    s["plyp"] = s["lyp"] * s["p1"]
    yrs = sorted(s["year"].dropna().unique())[1:]
    yd = pd.DataFrame({f"yr{int(t)}": (s["year"] == t).astype(float) for t in yrs}, index=s.index)
    ycols = list(yd.columns)
    for sex, fem in (("Sons", 0), ("Daughters", 1)):
        x = s[s["female"] == fem]
        for y, ylab in OUTS:
            fr = {"Baseline (33)": prep(x, y, "lyp"),
                  "Income-year fixed effects in every cell": prep(x, y, "lyp").join(yd),
                  "Period-varying IGE (evaluated in 1995)": prep(x, y, "lyp",
                                                                 extra={"q1": "p1", "q2": "p2", "q3": "plyp"}),
                  "Income years 1990-2010 only": prep(x[x["year"].between(1990, 2010)], y, "lyp")}
            R = run(fr, A4 + ycols + ["q1", "q2", "q3"])
            for lab in fr:
                summarize(R, "PSID", "apc", lab, sex, ylab)
            for lab in list(fr)[1:]:
                diff(R, "PSID", "apc", lab, "Baseline (33)", sex, ylab)
        print(f"apc {sex} done", flush=True)


def wsd(v, w=None):
    w = np.ones(len(v)) if w is None else w
    m = np.average(v, weights=w)
    return np.sqrt(np.average((v - m) ** 2, weights=w))


def sd_block(s, nboot=200):
    """within-race SD of ln income net of single-age means, by band, for fixed cohorts; SD change bootstrapped."""
    rng = np.random.default_rng(41)
    for sex, fem in (("Sons", 0),):
        for y, ylab in OUTS:
            x = s[(s["female"] == fem) & s[y].notna() & s["race"].isin(RACES) & s["lyp"].notna()].copy()
            x["e"] = x[y] - x.groupby(["race", "agei"])[y].transform("mean")
            for coh, rng_ in (("Born 1951-64", (1951, 1964)), ("Born 1965-79", (1965, 1979)),
                              ("Born 1951-74", (1951, 1974)), ("All cohorts", (1900, 2010))):
                c = x[x["birth_year"].between(*rng_)]
                fams = c["fam68"].unique()
                fidx = {f: i for i, f in enumerate(fams)}
                c = c.assign(fi=c["fam68"].map(fidx))

                def stats(cw):
                    out = {}
                    for g in RACES:
                        for b in BL:
                            z = cw[(cw["race"] == g) & (cw["band"] == b)]
                            if len(z) < 50:
                                continue
                            ww = z["bw"].to_numpy()
                            kids = z.groupby("pid").agg(lyp=("lyp", "first"), bw=("bw", "first"))
                            out[(g, b, "sd")] = wsd(z["e"].to_numpy(), ww)
                            out[(g, b, "sdp")] = wsd(kids["lyp"].to_numpy(), kids["bw"].to_numpy())
                    for g in RACES:
                        ok = [b for b in BL if (g, b, "sd") in out]
                        lo, hi = [b for b in ok if MID[b] < 35], [b for b in ok if MID[b] >= 35]
                        if lo and hi:
                            out[(g, "chg", "sd")] = (np.mean([out[(g, b, "sd")] for b in hi])
                                                     - np.mean([out[(g, b, "sd")] for b in lo]))
                    if ("White", "chg", "sd") in out and ("Black", "chg", "sd") in out:
                        out[("W-B", "chg", "sd")] = out[("White", "chg", "sd")] - out[("Black", "chg", "sd")]
                    return out

                est = stats(c.assign(bw=1.0))
                draws = []
                for _ in range(nboot):
                    cnt = np.bincount(rng.integers(0, len(fams), len(fams)), minlength=len(fams))
                    draws.append(stats(c.assign(bw=cnt[c["fi"].to_numpy()]).query("bw > 0")))
                for k, v in est.items():
                    dv = [d_[k] for d_ in draws if k in d_]
                    se = np.std(dv, ddof=1)
                    rec2(block="sd", sex=sex, band=k[1], spec=coh, group=k[0], stat=k[2], outcome=ylab, est=v,
                         se=se, p=2 * (1 - norm.cdf(abs(v / se))) if k[1] == "chg" and se > 0 else np.nan,
                         n=int(((c["race"] == k[0]) & (c["band"] == k[1])).sum()) if k[1] in BL else np.nan)
        print("sd done", flush=True)


# ================================================================ C Haider-Solon lambda
HSB = [(25, 29), (30, 34), (35, 39), (40, 44), (45, 49), (50, 55)]
HSL = [f"{a}-{b}" for a, b in HSB]


def lambda_block():
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    s = ige6.build(py)
    s = s[s["age"].between(25, 55) & (s["female"] == 0) & s["race"].isin(RACES)].copy()
    s["agei"] = s["age"].round().astype(int)
    s["band"] = pd.cut(s["age"], [24, 29, 34, 39, 44, 49, 55], labels=HSL).astype(object)
    terc = s.groupby("pid")["lyp"].first()
    cuts = terc.quantile([1 / 3, 2 / 3]).to_numpy()
    for y, ylab in OUTS:
        x = s[s[y].notna()].copy()
        x["e"] = x[y] - x.groupby(["race", "agei"])[y].transform("mean")
        win = pd.cut(x["age"], [24, 34, 44, 55], labels=["a", "b", "c"])
        cnt = x.groupby(["pid", win], observed=False).size().unstack(fill_value=0)
        long = cnt[(cnt >= 3).all(axis=1)].index
        x = x[x["pid"].isin(long)].copy()
        x["ybar"] = x.groupby("pid")["e"].transform("mean")
        x["terc"] = np.digitize(x["lyp"], cuts)
        sets = [("All", x)] + [(f"Parental tercile {t + 1}", x[x["terc"] == t]) for t in range(3)]
        for lab, d in sets:
            for spec, ctrl in (("lambda", []), ("lambda | ln parental income", ["lyp"])):
                d2 = d.assign(cellk=[(spec, b, r) for b, r in zip(d["band"], d["race"])])
                d2 = d2[d2.groupby("cellk")["pid"].transform("nunique") >= 15]
                R = R33.Cells(d2, "e", "ybar", "cellk", ctrl, "agei")
                for b in HSL:
                    for g in RACES:
                        k = (spec, b, g)
                        if not R.has(k):
                            continue
                        e_, se, p = R.lin([(k, "x", 1)])
                        rec2(block="lambda", sex="Sons", outcome=ylab, spec=f"{lab}: {spec}", band=b, group=g,
                             stat="lambda", est=e_, se=se, p=p, **R.info[k])
                        if ctrl:
                            e_, se, p = R.lin([(k, "lyp", 1)])
                            rec2(block="lambda", sex="Sons", outcome=ylab, spec=f"{lab}: {spec}", band=b, group=g,
                                 stat="kappa (ln parental income)", est=e_, se=se, p=p, **R.info[k])
                    if R.has((spec, b, "White")) and R.has((spec, b, "Black")):
                        e_, se, p = R.lin([((spec, b, "White"), "x", 1), ((spec, b, "Black"), "x", -1)])
                        rec2(block="lambda", sex="Sons", outcome=ylab, spec=f"{lab}: {spec}", band=b,
                             group="White - Black", stat="lambda", est=e_, se=se, p=p)
                # change of lambda: mean over bands >= 35 minus mean over bands < 35 (25-29, 30-34)
                for g in RACES + ("White - Black",):
                    terms = []
                    hi = [b for b in HSL if int(b[:2]) >= 35]
                    lo = [b for b in HSL if int(b[:2]) < 35]
                    sgn = {"White": [("White", 1)], "Black": [("Black", 1)],
                           "White - Black": [("White", 1), ("Black", -1)]}[g]
                    ok = all(R.has((spec, b, r)) for b in HSL for r, _ in sgn)
                    if not ok:
                        continue
                    for r, sg in sgn:
                        terms += [((spec, b, r), "x", sg / len(hi)) for b in hi]
                        terms += [((spec, b, r), "x", -sg / len(lo)) for b in lo]
                    e_, se, p = R.lin(terms)
                    rec2(block="lambda", sex="Sons", outcome=ylab, spec=f"{lab}: {spec}", band="change", group=g,
                         stat="lambda: mean >= 35 minus mean < 35", est=e_, se=se, p=p)
        nB = x.loc[x["race"] == "Black", "pid"].nunique()
        nW = x.loc[x["race"] == "White", "pid"].nunique()
        rec2(block="lambda", sex="Sons", outcome=ylab, spec="sample", band="", group="", stat="sons (B / W)",
             est=nB, se=nW, p=np.nan)
    print("lambda done", flush=True)


# ================================================================ D position in the distribution
def vigintiles(s):
    kid = s[(s["female"] == 0) & s["race"].isin(RACES)].groupby("pid").agg(lyp=("lyp", "first"), wt=("wt", "mean"))
    kid = kid[kid["wt"] > 0].sort_values("lyp")
    cw = kid["wt"].cumsum() / kid["wt"].sum()
    edges = [kid["lyp"][cw >= q].iloc[0] for q in np.arange(0.05, 1.0, 0.05)]
    return np.array(edges), kid


def position_runs(s):
    edges, kid = vigintiles(s)
    med = edges[9]
    kc = kid["lyp"].to_numpy()
    cw = (kid["wt"].cumsum() / kid["wt"].sum()).to_numpy()
    t1 = kc[np.searchsorted(cw, 1 / 3)]
    for sex, fem in (("Sons", 0),):
        x = s[(s["female"] == fem) & s["race"].isin(RACES)].copy()
        x["vig"] = np.digitize(x["lyp"], edges)
        for y, ylab in OUTS:
            xx = x[x[y].notna()].copy()
            # re-weight White child-years to the Black distribution over the vigintile bins, band by band
            sh = xx.groupby(["band", "race", "vig"]).size()
            sh = sh / sh.groupby(level=[0, 1]).transform("sum")
            ratio = (sh.xs("Black", level="race") / sh.xs("White", level="race")).rename("rw")
            xx = xx.join(ratio, on=["band", "vig"])
            xx["rw"] = np.where(xx["race"] == "Black", 1.0, xx["rw"].fillna(0.0))
            fr = {"All parents (33)": prep(xx, y, "lyp"),
                  "Parents below the pooled median": prep(xx[xx["lyp"] < med], y, "lyp"),
                  "Parents in the bottom pooled tercile": prep(xx[xx["lyp"] < t1], y, "lyp"),
                  "Parents above the pooled median": prep(xx[xx["lyp"] >= med], y, "lyp"),
                  "White re-weighted to the Black parental distribution": prep(xx, y, "lyp", w="rw")}
            R = run(fr, A4)
            for lab in fr:
                summarize(R, "PSID", "position", lab, sex, ylab)
            for lab in list(fr)[1:]:
                diff(R, "PSID", "position", lab, "All parents (33)", sex, ylab)
            # binned means for the figure (child-years net of single-age means within race, plus the band mean)
            for b0, bands in (("25-29", ["25-29"]), ("40-49", ["40-44", "45-49"])):
                z = xx[xx["band"].isin(bands)].copy()
                z["e"] = z[y] - z.groupby(["race", "agei"])[y].transform("mean") + z.groupby("race")[y].transform(
                    "mean")
                gb = z.groupby(["race", "vig"]).agg(m=("e", "mean"), lp=("lyp", "mean"), n=("e", "size"),
                                                   ch=("pid", "nunique"), sd=("e", "std"))
                for (g, v), r in gb.iterrows():
                    rec2(block="bins", sex=sex, outcome=ylab, spec=b0, group=g, band=int(v), stat="mean ln y",
                         est=r["m"], se=r["sd"] / np.sqrt(r["ch"]), p=np.nan, n=int(r["n"]), children=int(r["ch"]),
                         lp=r["lp"])
            share = xx.drop_duplicates("pid").groupby("race")["lyp"].apply(lambda v: (v < med).mean())
            for g in RACES:
                rec2(block="position", sex=sex, outcome=ylab, spec="share of sons below the pooled median", group=g,
                     band="", stat="share", est=share[g], se=np.nan, p=np.nan)
        print("position done", flush=True)


# ================================================================ E within-race ranks and PPML
def rank_runs():
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    k = pd.read_pickle(DATA / "psid_kids.pkl")
    k = k.assign(w=k["wt_pt"], pinc=k["pinc_av"].where(k["n_av"] >= 3))
    hw = py[(py["head"] | py["wife"]) & py["age"].between(25, 55)].copy()
    r0 = R26.rank_frame(k.set_index("pid"), hw.set_index("pid"), idcol="pid")
    r = R26.add_child_ranks(r0)                                          # national ranks (26)
    r = r[r["race"].isin(RACES) & r["band"].isin(BL)].copy()
    # within-race ranks
    kk = k[k["race"].isin(RACES)].copy()
    kk["rp_wr"] = R26.rank_in(kk, "pinc", ["race", "birth_year"])
    r = r.merge(kk[["pid", "rp_wr"]], on="pid", how="left")
    r["ryf_wr"] = R26.rank_in(r, "yf", ["race", "birth_year", "band"])
    r["agei"] = 0
    for sex, fem in (("Sons", [0]), ("Both sexes", [0, 1])):
        x = r[r["female"].isin(fem)]
        fr = {"National ranks (26)": prep(x, "ryf", "rp", w="w"),
              "Within-race ranks": prep(x, "ryf_wr", "rp_wr", w="w")}
        R = run(fr, [])
        for lab in fr:
            summarize(R, "PSID", "ranks", lab, sex, FAM)
        diff(R, "PSID", "ranks", "Within-race ranks", "National ranks (26)", sex, FAM)
    print("ranks done", flush=True)


def ppml_runs(s):
    for sex, fem in (("Sons", 0), ("Daughters", 1)):
        x = s[s["female"] == fem]
        for ylog, ylev, ylab in (("lfam", "famlev", FAM), ("learn", "earnlev", ERN)):
            fr = {"PPML, level (zeros kept)": prep(x, ylev, "lyp")}
            R = run_ppml(fr, A4)
            summarize(R, "PSID", "ppml", "PPML, level (zeros kept)", sex, ylab)
            fr2 = {"OLS on ln y (33)": prep(x, ylog, "lyp")}
            R2 = run(fr2, A4)
            summarize(R2, "PSID", "ppml", "OLS on ln y (33)", sex, ylab)
        print(f"ppml {sex} done", flush=True)


# ================================================================ F common corrected estimate across data sets
RR1 = {"White": 0.585, "Black": 0.565}


def corrected_runs(s):
    n79, n97 = R33.nlsy79_frames(), R33.nlsy97_frames()
    s4 = s[s["band"].isin(BL4)]
    sc = (1 / RR1["White"], 1 / RR1["Black"])
    for y, ylab in OUTS:
        x = s4[s4["female"] == 0]
        R = run({"one": prep(x, y, "ly97")}, A4)
        summarize(R, "PSID", "corrected", "one", "Sons", ylab, label="PSID: one year at 12-16")
        summarize(R, "PSID", "corrected", "one", "Sons", ylab, label="PSID: one year at 12-16 / RR", sc=sc)
        x = n79[n79["female"] == 0]
        R = run({"one": prep(x, y, "lyp_pt")}, A4)
        summarize(R, "NLSY79", "corrected", "one", "Sons", ylab, label="NLSY79: 1978 one year")
        summarize(R, "NLSY79", "corrected", "one", "Sons", ylab, label="NLSY79: 1978 one year / RR", sc=sc)
        x = n97[n97["female"] == 0]
        R = run({"one": prep(x, y, "lyp_pt")}, A4 + ["Amiss"])
        summarize(R, "NLSY97", "corrected", "one", "Sons", ylab, label="NLSY97: 1996 one year")
        summarize(R, "NLSY97", "corrected", "one", "Sons", ylab, label="NLSY97: 1996 one year / RR", sc=sc)
    print("corrected done", flush=True)


def pool_corrected(res):
    for ylab in (FAM, ERN):
        for suf in ("", " / RR"):
            vals = {}
            for dt, lab in (("PSID", "PSID: one year at 12-16"), ("NLSY79", "NLSY79: 1978 one year"),
                            ("NLSY97", "NLSY97: 1996 one year")):
                r = res.get((dt, "corrected", lab + suf, "Sons", ylab, "test", "White - Black", GC, "25-44"))
                if r is not None:
                    vals[dt] = (r["est"], r["se"])
            w = {k: 1 / v[1] ** 2 for k, v in vals.items()}
            e = sum(w[k] * vals[k][0] for k in vals) / sum(w.values())
            se = 1 / np.sqrt(sum(w.values()))
            q = sum(w[k] * (vals[k][0] - e) ** 2 for k in vals)
            rec2(block="corrected", sex="Sons", outcome=ylab, spec="Pooled" + suf, band="test", group="White - Black",
                 stat="Inverse-variance pooled gap change", est=e, se=se, p=2 * (1 - norm.cdf(abs(e / se))),
                 note=f"Q={q:.2f}, p={1 - chi2.cdf(q, len(vals) - 1):.3f}")


# ================================================================ output
def G(res, *k):
    return res.get(k)


def c_(r):
    return "" if r is None else cell(r["est"], r["se"], r["p"])


def change_rows(res, block, specs, sexes_outs, diffs_to=None, bandset="25-49"):
    L = ["| | " + " | ".join(f"({i + 1}) {sx}: {o}" for i, (sx, o) in enumerate(sexes_outs)) + " |",
         "|---" * (len(sexes_outs) + 1) + "|"]
    for sp in specs:
        L.append(f"| **{sp}** |" + " |" * len(sexes_outs))
        for b in BL:
            rs = [G(res, "PSID", block, sp, sx, o, b, "White - Black", "IGE", "") for sx, o in sexes_outs]
            if any(r is not None for r in rs):
                L.append(f"| W - B gap, {b} | " + " | ".join(c_(r) for r in rs) + " |")
        for g in ("Black", "White"):
            L.append(f"| {g} IGE change, >= 35 minus < 35 | " + " | ".join(
                c_(G(res, "PSID", block, sp, sx, o, "test", g, GC, bandset)) for sx, o in sexes_outs) + " |")
        L.append("| **Gap change, >= 35 minus < 35** | " + " | ".join(
            c_(G(res, "PSID", block, sp, sx, o, "test", "White - Black", GC, bandset)) for sx, o in sexes_outs)
                 + " |")
        if diffs_to and sp != diffs_to:
            L.append(f"| Gap change minus [{diffs_to}] | " + " | ".join(
                c_(G(res, "PSID", block, sp, sx, o, "test", "White - Black", f"Gap change minus [{diffs_to}]",
                     bandset)) for sx, o in sexes_outs) + " |")
        ns = []
        for sx, o in sexes_outs:
            tot = [G(res, "PSID", block, sp, sx, o, b, "White - Black", "IGE", "") for b in BL]
            tot = [r for r in tot if r is not None]
            ns.append("" if not tot else "B " + "/".join(f"{int(r['nB']):,}" for r in tot) + "; W "
                      + "/".join(f"{int(r['nW']):,}" for r in tot))
        L.append("| Child-years by band (B; W) | " + " | ".join(ns) + " |")
    return L


def write_md(res, ex):
    so = [("Sons", FAM), ("Sons", ERN)]
    sdo = [("Sons", FAM), ("Sons", ERN), ("Daughters", FAM), ("Daughters", ERN)]
    L = ["# Paper B measurement checks (Fable review, Items 1 and 5)", "",
         "Generated by `41.AgeProfileMeasurement.py` (2026-10-17). Every cell: estimate (s.e.; p-value), *** p<0.01, "
         "** p<0.05, * p<0.1; s.e. clustered by 1968 family, joint across bands and specifications of a panel "
         "(stacked, fully interacted), normal p-values. Design of `33.AgeProfileRobustness.py`: ln y on ln parental "
         "income (13-19 mean), quartic in the parent's age at 16, single-year age dummies; Black / White unweighted. "
         "Gap = White minus Black IGE; gap change = mean gap in bands >= 35 minus mean gap in bands < 35, bands 25-49. "
         "One regression set per column (outcome in the header); row panels = specifications.", ""]
    # A
    L += ["## A. Attrition", "",
          "Sons / daughters with >= 1 valid ln family income year at 25-29, old enough to reach the band (birth year + "
          "band start + 2 <= 2023). Linear probability of being observed (head or spouse with valid ln family income) "
          "in the band, on ln parental income interacted with Black, controls: quartic in parent's age, 5-year "
          "birth-cohort dummies (+ ln family income at 25-29 x Black in the second row of each panel).", "",
          "| | " + " | ".join(f"({i + 1}) {b}" for i, b in enumerate(BL[1:])) + " |", "|---" * len(BL) + "|"]
    for sex in ("Sons", "Daughters"):
        L.append(f"| **{sex}** |" + " |" * (len(BL) - 1))
        for g in ("White", "Black"):
            L.append(f"| Share observed, {g} | " + " | ".join(
                "" if (r := ex.get(("attrition", sex, b, "share observed", g, "share"))) is None
                else f"{r['est']:.3f} (n={int(r['n']):,})" for b in BL[1:]) + " |")
        for spec in ("lyp", "lyp + early income"):
            for g in ("White", "Black", "Black - White"):
                L.append(f"| P(obs) on ln parental income: {g} [{spec}] | " + " | ".join(
                    c_(ex.get(("attrition", sex, b, spec, g, "P(observed) on ln parental income"))) for b in BL[1:])
                         + " |")
        for g in ("White", "Black - White"):
            L.append(f"| P(obs) on ln income at 25-29: {g} | " + " | ".join(
                c_(ex.get(("attrition", sex, b, "lyp + early income", g, "P(observed) on ln income at 25-29")))
                for b in BL[1:]) + " |")
        L.append("| Children (eligible) | " + " | ".join(
            "" if (r := ex.get(("attrition", sex, b, "lyp", "White", "P(observed) on ln parental income"))) is None
            else f"{int(r['children']):,}" for b in BL[1:]) + " |")
    L += ["", "Age profile on the sons observed at 25-29, unweighted and with inverse-probability weights for being "
          "observed in each later band (logit on ln parental income x Black, ln family income at 25-29 x Black, SRC, "
          "parent's age quartic, 5-year cohorts; weights 1 / p, p clipped at 0.05).", ""]
    L += change_rows(res, "attrition", ["Observed at 25-29, unweighted", "Observed at 25-29, IPW for staying"], sdo,
                     "Observed at 25-29, unweighted") + [""]
    # B
    L += ["## B. Age, period and cohort", "",
          "(i) income-year dummies added in every band x race cell; (ii) ln parental income x (income year - 1995)/10 "
          "(+ the period and its square) in every cell, band IGE evaluated in 1995 (33 reports the cohort-varying "
          "analogue: 0.176***); (iii) income years 1990-2010 only. Differences vs the baseline on the same stacked "
          "run.", ""]
    L += change_rows(res, "apc", ["Baseline (33)", "Income-year fixed effects in every cell",
                                  "Period-varying IGE (evaluated in 1995)", "Income years 1990-2010 only"], sdo,
                     "Baseline (33)") + [""]
    L += ["### B(iv). Within-race SD of ln income (net of race x single-age means) by band, fixed cohorts (sons)", "",
          "SD of ln parental income of the same children in brackets. Change = mean SD in bands >= 35 minus < 35; "
          "s.e. from 200 bootstrap draws of 1968 families.", ""]
    for _, ylab in OUTS:
        L += [f"**{ylab}**", "", "| Cohort | Race | " + " | ".join(BL) + " | Change >= 35 minus < 35 |",
              "|---" * (len(BL) + 3) + "|"]
        for coh in ("Born 1951-64", "Born 1965-79", "Born 1951-74", "All cohorts"):
            for g in RACES:
                row = []
                for b in BL:
                    r = ex.get(("sd", "Sons", b, coh, g, "sd", ylab))
                    rp = ex.get(("sd", "Sons", b, coh, g, "sdp", ylab))
                    row.append("" if r is None else f"{r['est']:.3f} [{rp['est']:.3f}]")
                ch = ex.get(("sd", "Sons", "chg", coh, g, "sd", ylab))
                L.append(f"| {coh} | {g} | " + " | ".join(row) + f" | {c_(ch)} |")
            ch = ex.get(("sd", "Sons", "chg", coh, "W-B", "sd", ylab))
            L.append(f"| {coh} | White - Black | " + " |" * len(BL) + f" {c_(ch)} |")
        L.append("")
    # C
    L += ["## C. Haider-Solon lambda by race (sons with >= 3 valid years in each of 25-34, 35-44, 45-55)", "",
          "lambda_b = slope of current ln y (net of race x single-age means) on the son's mean over 25-55 of the same "
          "net ln y, in band b, by race (age dummies in each cell). kappa = coefficient on ln parental income added "
          "to the same regression (Nybom-Stuhler: kappa != 0 means income profiles that differ with background). "
          "Change = mean lambda in bands >= 35 minus bands < 35.", ""]
    for _, ylab in OUTS:
        smp = ex.get(("lambda", "Sons", "", "sample", "", "sons (B / W)", ylab))
        L += [f"### {ylab} ({int(smp['est'])} Black / {int(smp['se'])} White sons)", "",
              "| | " + " | ".join(HSL) + " | Change >= 35 minus < 35 |", "|---" * (len(HSL) + 2) + "|"]
        for lab in ("All", "Parental tercile 1", "Parental tercile 2", "Parental tercile 3"):
            for spec in ("lambda", "lambda | ln parental income"):
                sp = f"{lab}: {spec}"
                for g in RACES + ("White - Black",):
                    if spec != "lambda" and g == "White - Black":
                        continue
                    L.append(f"| {sp}, {g}: lambda | " + " | ".join(
                        c_(ex.get(("lambda", "Sons", b, sp, g, "lambda", ylab))) for b in HSL) + " | "
                             + c_(ex.get(("lambda", "Sons", "change", sp, g, "lambda: mean >= 35 minus mean < 35",
                                          ylab))) + " |")
                    if spec != "lambda":
                        L.append(f"| {sp}, {g}: kappa | " + " | ".join(
                            c_(ex.get(("lambda", "Sons", b, sp, g, "kappa (ln parental income)", ylab)))
                            for b in HSL) + " | |")
            L.append("| N child-years / sons (B; W) | " + " | ".join(
                "; ".join(f"{g[0]} {int(r['n']):,}/{int(r['children']):,}" for g in RACES
                          if (r := ex.get(("lambda", "Sons", b, f"{lab}: lambda", g, "lambda", ylab))) is not None)
                for b in HSL) + " | |")
        L.append("")
    # D
    L += ["## D. Position in the parental distribution vs race (sons)", "",
          "Pooled vigintiles / median / tercile of ln parental income over Black and White sons (one row per son, "
          "weighted by the mean core longitudinal weight). Re-weighted: White child-years in each band weighted by "
          "the Black / White ratio of child-year shares in the 20 vigintile bins.", ""]
    for g in RACES:
        r = ex.get(("position", "Sons", "", "share of sons below the pooled median", g, "share", FAM))
        L.append(f"- {g} sons with parents below the pooled median: {r['est']:.3f}")
    L.append("")
    L += change_rows(res, "position", ["All parents (33)", "Parents below the pooled median",
                                       "Parents in the bottom pooled tercile", "Parents above the pooled median",
                                       "White re-weighted to the Black parental distribution"], so,
                     "All parents (33)") + [""]
    L += ["### Binned means (figure panels): mean ln y net of single-age means, by vigintile, 25-29 and 40-49", "",
          "| Outcome | Ages | Race | " + " | ".join(str(v + 1) for v in range(20)) + " |", "|---" * 23 + "|"]
    for _, ylab in OUTS:
        for b0 in ("25-29", "40-49"):
            for g in RACES:
                L.append(f"| {ylab} | {b0} | {g} | " + " | ".join(
                    "" if (r := ex.get(("bins", "Sons", v, b0, g, "mean ln y", ylab))) is None or r["children"] < 10
                    else f"{r['est']:.2f} ({int(r['children'])})" for v in range(20)) + " |")
    L.append("")
    # E
    L += ["## E. Other metrics", "", "### E(i). Within-race vs national ranks (family income, band means, weighted)",
          "", "Rank-rank slope by band; same children and weights in both rows of a column.", ""]
    for sex in ("Sons", "Both sexes"):
        L += [f"**{sex}**", ""] + change_rows(res, "ranks", ["National ranks (26)", "Within-race ranks"],
                                              [(sex, FAM)], "National ranks (26)") + [""]
    L += ["### E(ii). Dollar-weighted IGE (PPML on the income level) vs log IGE", "",
          "PPML: income level (family income in [0, cap]; own earnings with zero-earnings years kept) on ln parental "
          "income with the same controls; the coefficient is the elasticity of expected income. OLS rows: 33's log "
          "design (positive incomes in bounds).", ""]
    L += change_rows(res, "ppml", ["OLS on ln y (33)", "PPML, level (zeros kept)"], sdo) + [""]
    # F
    L += ["## F. One corrected estimate across PSID, NLSY79 and NLSY97 (sons, bands 25-44)", "",
          "One-year parental income in every data set (PSID: the wave at 12-16 nearest 14; NLSY79: 1978; NLSY97: "
          "1996). '/ RR': each race's IGE divided by the PSID one-year reliability ratio (W 0.585, B 0.565), treated "
          "as known. Inverse-variance pooled gap change with Cochran's Q.", "",
          "| | (1) PSID | (2) NLSY79 | (3) NLSY97 | (4) Pooled |", "|---|---|---|---|---|"]
    for _, ylab in OUTS:
        for suf in ("", " / RR"):
            pr = ex.get(("corrected", "Sons", "test", "Pooled" + suf, "White - Black",
                         "Inverse-variance pooled gap change", ylab))
            L.append(f"| {ylab}{suf}: gap change | " + " | ".join(
                c_(G(res, dt, "corrected", lab + suf, "Sons", ylab, "test", "White - Black", GC, "25-44"))
                for dt, lab in (("PSID", "PSID: one year at 12-16"), ("NLSY79", "NLSY79: 1978 one year"),
                                ("NLSY97", "NLSY97: 1996 one year"))) + f" | {c_(pr)}; {pr['note']} |")
    L.append("")
    (OUT / "age_profile_measurement.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def figure(ex, res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    col = {"Black": "#eb6834", "White": "#2a78d6"}
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.8))
    for ax, (_, ylab) in zip(axes[:2], OUTS):
        for g in RACES:
            for b0, ls, mk in (("25-29", "--", "o"), ("40-49", "-", "s")):
                pts = [ex.get(("bins", "Sons", v, b0, g, "mean ln y", ylab)) for v in range(20)]
                pts = [r for r in pts if r is not None and r["children"] >= 20]
                ax.plot([r["lp"] for r in pts], [r["est"] for r in pts], ls=ls, marker=mk, ms=4.5, lw=1.6,
                        color=col[g], label=f"{g}, {b0}")
        ax.set_xlabel("ln parental income (mean of the pooled vigintile)")
        ax.set_ylabel(f"mean {ylab}")
        ax.set_title(f"Sons' {ylab.replace('ln ', '')} by parental vigintile", fontsize=10.5)
        ax.grid(color="#e5e5e5", lw=0.6)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    axes[0].legend(frameon=False, fontsize=8.5)
    ax = axes[2]
    specs = [("All parents (33)", "All parents", "#52514e"), ("Parents below the pooled median", "Below median",
                                                              "#6250d6"),
             ("White re-weighted to the Black parental distribution", "White re-weighted to Black parents",
              "#008300")]
    for i, (sp, lab, c) in enumerate(specs):
        off = (i - 1) * 0.6
        pts = [(MID[b] + off, G(res, "PSID", "position", sp, "Sons", FAM, b, "White - Black", "IGE", "")) for b in BL]
        pts = [(x_, r) for x_, r in pts if r is not None]
        ax.errorbar([x_ for x_, _ in pts], [r["est"] for _, r in pts], yerr=[1.96 * r["se"] for _, r in pts],
                    color=c, marker="o", ms=5, lw=1.6, elinewidth=1, label=lab)
    ax.axhline(0, color="#bbbbbb", lw=0.8)
    ax.set_xticks([MID[b] for b in BL], BL)
    ax.set_title("White - Black log IGE gap, family income", fontsize=10.5)
    ax.set_xlabel("Son's age (band)")
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax.grid(axis="y", color="#e5e5e5", lw=0.6)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "age_profile_measurement.png", dpi=150)
    fig.savefig(OUT / "age_profile_measurement.pdf")


def main():
    s = psid_all()
    print("PSID frame", s.shape, flush=True)
    base = attrition_block(s)
    attrition_runs(base)
    apc_runs(s)
    sd_block(s)
    lambda_block()
    position_runs(s)
    rank_runs()
    ppml_runs(s)
    corrected_runs(s)
    res = pd.DataFrame(ROWS)
    resd = {tuple(r.get(k, "") if not (isinstance(r.get(k), float) and np.isnan(r.get(k))) else ""
                  for k in R33.KEYS): r for r in res.to_dict("records")}
    pool_corrected(resd)
    ex = pd.DataFrame(EXTRA)
    exd = {}
    for r in EXTRA:
        exd[(r["block"], r["sex"], r["band"], r["spec"], r["group"], r["stat"])] = r
        exd[(r["block"], r["sex"], r["band"], r["spec"], r["group"], r["stat"], r.get("outcome", ""))] = r
    OUT.mkdir(exist_ok=True)
    pd.concat([res.assign(table="band"), ex.assign(table="extra")], ignore_index=True).to_csv(
        OUT / "age_profile_measurement.csv", index=False)
    write_md(resd, exd)
    figure(exd, resd)
    show = res[(res["band"] == "test") & (res["group"] == "White - Black") & (res["stat"] == GC)]
    show = show.assign(c=[cell(e, se, p) for e, se, p in zip(show.est, show.se, show.p)])
    pd.set_option("display.width", 250)
    pd.set_option("display.max_colwidth", 60)
    pd.set_option("display.max_rows", 500)
    print(show.pivot_table(index=["data", "block", "spec", "bandset"], columns=["sex", "outcome"], values="c",
                           aggfunc="first", sort=False).to_string())


if __name__ == "__main__":
    main()
