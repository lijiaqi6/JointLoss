r"""Why is the opening Black-White log IGE gap strong in the PSID and weak in the NLSY79 / NLSY97? Cohort,
parental-income measurement, sample design, or chance (2026-10-17).

Paper B's core fact (EVIDENCE.md 1.10, 1.18): in the PSID the White - Black gap in the sons' log IGE of family income
is ~0 at 25-29 and opens to ~0.25 by 40-49 (mean gap at >= 35 minus mean gap at < 35: 0.137*** on 25-44); in the
NLSY79 (born 1960-64) the change is 0.064 (n.s.), in the NLSY97 (born 1980-84) 0.079*. Candidate reasons:
  COHORT       the PSID pools children born 1951-98 and its >= 35 bands are dominated by the 1951-64 cohorts;
  MEASUREMENT  PSID parents = mean of up to 7 years at child ages 13-19; NLSY79 = 1-3 years (1978-80), NLSY97 = 1996;
  SAMPLE       PSID SEO oversample (Black children mostly SEO), weights, unbalanced panels, income concept;
  CHANCE       the three estimates may not differ by more than their sampling error.

DATA (read only): data/psid_person_year.pkl (via 6.IGEMain.build), data/nlsy79_kids.pkl, nlsy79_person_year.pkl,
data/nlsy97_ap_kids.pkl, nlsy97_ap_person_year.pkl (29.NLSY97AgeProfile.py's own extract, CV_INCOME -4 = missing),
output/ige_estimates.csv (PSID race-specific reliability ratios of 4.Estimates.py).

DESIGN (as 26.IGEByAge.py, child-year version). Bands 25-29, 30-34, 35-39, 40-44, 45-49 (age at interview).
In each band x race cell: ln y (child-year) on ln parental income, quartic in (A - 45)/10 (A = parental head's age when
the child is 16), single-year age dummies; Black / White unweighted (race = parental head's race). Every
specification x band x race cell is its own regression; all cells of a table panel are STACKED, and the joint
covariance is the cluster-robust sandwich (clusters = 1968 family; NLSY: first-round household), so tests across
bands and across specifications that share children (e.g. one-year vs 13-19 parental income on the same children)
are valid. Statistics on the gap g_b = beta_W,b - beta_B,b:
  gap change = mean g_b over bands >= 35 minus mean g_b over bands < 35 (bands 25-49 where available, and on 25-44
  so the PSID is comparable with the NLSY97); linear trend of g_b per 10 years of the band midpoint; Wald test that
  g_b is equal in all bands. Only bands with >= 50 child-years and >= 20 children in BOTH race cells enter.
  Normal p-values. Cross-specification differences of the gap change use the bands both specifications have.
Outcomes: ln family income of the child's own household, ln own labor earnings (> 0); sons and daughters.
Yearly amounts outside $100-$150,000 of 1967 dropped (6.IGEMain.py).

1 COHORTS (PSID, parents = 13-19 mean): all (26) / born 1951-64 / 1965-79 / 1980-89 / 1951-56 / 1957-64 (NLSY79
  birth years) / 1960-64 (the NLSY79 analysis sample, at home in 1979 aged 14-18) / 1980-84 (NLSY97) / 1951-74 (the
  cohorts that can reach 45-49 by 2023, so every band holds the same cohorts) / all with a cohort-varying IGE
  (controls birth-cohort c = (birth year - 1965)/10, c^2 and ln parental income x c in every cell: the band IGE is
  evaluated at the 1965 cohort).
2 PARENTAL-INCOME MEASUREMENT (PSID; the SAME children: in 26's sample and with every measure below):
  (a) 13-19 mean (>= 3 years; 26); (b) NLSY79-like: mean of the 1-3 waves at child ages 14-16; (c) NLSY97-like: one
  year, the wave at child ages 12-16 nearest to 14; (d) = (c) / RR and (a) / RR with the PSID race-specific
  reliability ratios of 4.Estimates.py (one year: B 0.565, W 0.585; multi-year mean: B 0.631, W 0.650; treated as
  known); (e) IV: (c) instrumented by the mean of parental income at child ages 17-19 (classical transitory error
  that is uncorrelated across these years -> the permanent-income IGE). All four in one stacked regression.
3 SAMPLE (PSID, 13-19 mean): SRC + SEO (26) / SRC only (1968 family <= 2930) / race-specific weighted (child-year
  core longitudinal weight) / balanced (children with the outcome in a band < 35 AND a band >= 35) / parents'
  labor income of head + spouse (13-19 mean, >= 3 years) instead of total family income / labor income in both
  generations (child: head + spouse labor income of the child's household in the family-income column).
4 SIDE BY SIDE on bands 25-44: each data set's main definition; one-year parental income everywhere (PSID 1 year
  at 12-16, NLSY79 1978 income, NLSY97 1996); few-year means (PSID 1-3 years at 14-16, NLSY79 1978-80, NLSY97 1996-99
  for youths with >= 2 parental years); matched cohorts (PSID born 1960-64 vs NLSY79, PSID born 1980-84 vs NLSY97).
  Differences between data sets: independent samples. Inverse-variance pooled gap change across the three data sets
  and Cochran's Q test of equality.
NLSY79 frames as 26 (parents' age = 1979 + years averaged, A quartic, wt79 not used for race cells); NLSY97 frames as
29 (A quartic + missing-A dummy).
Writes output/age_profile_robustness.csv (every estimate), output/age_profile_robustness.md,
output/age_profile_robustness.png.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd
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


ige6 = _load("ige6", "6.IGEMain.py")
ige29 = _load("ige29", "29.NLSY97AgeProfile.py")

LO, HI = ige6.LO, ige6.HI
BANDS = [(25, 29), (30, 34), (35, 39), (40, 44), (45, 49)]
BL = [f"{a}-{b}" for a, b in BANDS]
BL4 = BL[:4]
MID = dict(zip(BL, [27, 32, 37, 42, 47]))
RACES = ("Black", "White")
A4 = [f"A{n}" for n in range(1, 5)]
FAM, ERN = "ln family income", "ln own earnings"
OUTS = [("lfam", FAM), ("learn", ERN)]
SEXES = {"Sons": 0, "Daughters": 1}
COLS4 = [(sx, o) for sx in SEXES for _, o in OUTS]
MIN_N, MIN_CH = 50, 20
ROWS = []
GC = "Mean >= 35 minus mean < 35"


def record(**k):
    ROWS.append(k)


def band_of(age):
    out = pd.Series(pd.NA, index=age.index, dtype="object")
    for (a, b), lab in zip(BANDS, BL):
        out[age.between(a, b)] = lab
    return out


# ================================================================ regression engine (26.IGEByAge.Cells + IV)
class Cells:
    """Separate (W)LS / just-identified IV in each cell (x instrumented by z; z = x gives OLS); joint
    cluster-robust covariance = the stacked, fully interacted regression."""

    def __init__(self, d, y, x, cell, ctrl=(), fe=None, w=None, z=None, cluster="fam68", pid="pid"):
        cols = list(dict.fromkeys([cell, y, x, *ctrl, cluster, pid] + ([fe] if fe else []) + ([w] if w else [])
                                  + ([z] if z else [])))
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
            Z = X.copy()
            if z:
                Z["x"] = g[z].astype(float)
            Xa, Za = X.to_numpy(), Z.to_numpy()
            ww = g[w].to_numpy(float) if w else np.ones(len(g))
            Bi = np.linalg.pinv(Za.T @ (Xa * ww[:, None]))
            yy = g[y].to_numpy(float)
            bb = Bi @ (Za.T @ (ww * yy))
            u = Za * (ww * (yy - Xa @ bb))[:, None]
            S = np.zeros((G, Xa.shape[1]))
            np.add.at(S, gid[g.index.to_numpy()], u)
            breads.append(Bi)
            scores.append(S)
            self.b.extend(bb)
            self.names.extend((c, n) for n in X.columns)
            self.info[c] = dict(n=len(g), children=g[pid].nunique(), clusters=g[cluster].nunique())
        B, S = block_diag(*breads), np.hstack(scores)
        N, K = len(d), len(self.b)
        self.V = B @ (S.T @ S) @ B.T * G / (G - 1) * (N - 1) / max(N - K, 1)
        self.b = np.array(self.b)
        self.ix = {n: i for i, n in enumerate(self.names)}

    def has(self, c):
        return (c, "x") in self.ix

    def lin(self, terms):
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


def prep(d, y, lyp, z=None, w=None, extra=None):
    """standard columns for a stacked run: _y, lyp, zz (instrument; = lyp for OLS), _w (1 = unweighted)."""
    out = d.assign(_y=d[y], lyp=d[lyp], zz=d[z] if z else d[lyp], _w=d[w] if w else 1.0)
    for k, v in (extra or {}).items():
        out[k] = out[v] if isinstance(v, str) else v
    return out


def run(frames, ctrl, fe="agei"):
    """frames {spec: prepared df}; one Cells over (spec, band, race) cells with enough observations."""
    parts = []
    ctrl = list(ctrl)
    for spec, d in frames.items():
        d = d[d["_y"].notna() & d["lyp"].notna() & d["zz"].notna() & d["race"].isin(RACES) & d["band"].notna()]
        d = d.assign(cellk=[(spec, b, r) for b, r in zip(d["band"], d["race"])])
        for c in ctrl:
            if c not in d:
                d[c] = 0.0
        cnt = d.groupby("cellk").agg(n=("pid", "size"), ch=("pid", "nunique"))
        ok = set(cnt[(cnt["n"] >= MIN_N) & (cnt["ch"] >= MIN_CH)].index)
        okb = {(s_, b) for s_, b, r in ok if (s_, b, "Black") in ok and (s_, b, "White") in ok}
        d = d[[(s_, b) in okb for s_, b, _ in d["cellk"]]]
        parts.append(d[["cellk", "_y", "lyp", "zz", "_w", "fam68", "pid", fe, *ctrl]])
    st = pd.concat(parts, ignore_index=True)
    return Cells(st, "_y", "lyp", "cellk", ctrl, fe, w="_w", z="zz")


# ================================================================ tests
def gap_term(spec, sW=1.0, sB=1.0):
    return lambda b: [((spec, b, "White"), "x", sW), ((spec, b, "Black"), "x", -sB)]


def race_term(spec, race, s=1.0):
    return lambda b: [((spec, b, race), "x", s)]


def avail(R, spec, bands):
    return [b for b in bands if R.has((spec, b, "White")) and R.has((spec, b, "Black"))]


def change_terms(bands, term):
    early, late = [b for b in bands if MID[b] < 35], [b for b in bands if MID[b] >= 35]
    if not early or not late:
        return None
    return ([(t[0], t[1], t[2] / len(late)) for b in late for t in term(b)]
            + [(t[0], t[1], -t[2] / len(early)) for b in early for t in term(b)])


def tests(R, bands, term):
    out = []
    if len(bands) >= 2:
        st, df, p = R.wald([term(b) + [(t[0], t[1], -t[2]) for t in term(bands[0])] for b in bands[1:]])
        out.append(("Equal in all bands (Wald chi2)", st, np.nan, p, f"chi2({df})={st:.2f}"))
        mm = np.array([MID[b] for b in bands], float)
        c = (mm - mm.mean()) / ((mm - mm.mean()) ** 2).sum() * 10
        e, se, p = R.lin([(t[0], t[1], t[2] * cw) for b, cw in zip(bands, c) for t in term(b)])
        out.append(("Linear trend per 10 years", e, se, p, ""))
    ct = change_terms(bands, term)
    if ct:
        e, se, p = R.lin(ct)
        out.append((GC, e, se, p, ""))
    return out


def summarize(R, data, block, spec, sex, outcome, label=None, sc=(1.0, 1.0)):
    """band estimates (B, W, gap) and tests on bands 25-49 and 25-44 for one specification of a stacked run."""
    label = label or spec
    meta = dict(data=data, block=block, spec=label, sex=sex, outcome=outcome)
    sW, sB = sc
    for b in avail(R, spec, BL):
        for g, s_ in (("Black", sB), ("White", sW)):
            e, se, p = R.lin(race_term(spec, g, s_)(b))
            record(**meta, band=b, group=g, stat="IGE", bandset="", est=e, se=se, p=p, **R.info[(spec, b, g)])
        e, se, p = R.lin(gap_term(spec, sW, sB)(b))
        iB, iW = R.info[(spec, b, "Black")], R.info[(spec, b, "White")]
        record(**meta, band=b, group="White - Black", stat="IGE", bandset="", est=e, se=se, p=p,
               n=iB["n"] + iW["n"], children=iB["children"] + iW["children"], nB=iB["n"], nW=iW["n"],
               chB=iB["children"], chW=iW["children"])
    for bs, bset in (("25-49", BL), ("25-44", BL4)):
        bands = avail(R, spec, bset)
        for t, e, se, p, txt in tests(R, bands, gap_term(spec, sW, sB)):
            record(**meta, band="test", group="White - Black", stat=t, bandset=bs, est=e, se=se, p=p, note=txt,
                   bands=",".join(bands))
        for g, s_ in (("Black", sB), ("White", sW)):
            ct = change_terms(bands, race_term(spec, g, s_))
            if ct:
                e, se, p = R.lin(ct)
                record(**meta, band="test", group=g, stat=GC, bandset=bs, est=e, se=se, p=p)


def diff(R, data, block, spec, ref, sex, outcome, label=None, sc=(1.0, 1.0), scr=(1.0, 1.0), ref_label=None):
    """gap change of `spec` minus that of `ref` on the bands both have (bands 25-49 and 25-44)."""
    for bs, bset in (("25-49", BL), ("25-44", BL4)):
        bands = [b for b in avail(R, spec, bset) if b in avail(R, ref, bset)]
        a, r = change_terms(bands, gap_term(spec, *sc)), change_terms(bands, gap_term(ref, *scr))
        if not a or not r:
            continue
        e, se, p = R.lin(a + [(t[0], t[1], -t[2]) for t in r])
        record(data=data, block=block, spec=label or spec, sex=sex, outcome=outcome, band="test",
               group="White - Black", stat=f"Gap change minus [{ref_label or ref}]", bandset=bs, est=e, se=se, p=p,
               bands=",".join(bands))


# ================================================================ frames
def psid_frames():
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    s = ige6.build(py)
    s = s[s["age"].between(25, 49)].copy()
    s["band"], s["agei"] = band_of(s["age"]), s["age"].round().astype(int)
    s["wt"] = s["wt"].astype(float)
    k = py[py["child"] & py["age"].between(12, 19)].copy()
    k["fi"] = k["faminc"].where(k["faminc"].between(LO, HI))
    lab = k["hlab"] + k["wlab"]
    k["li"] = lab.where(lab.between(LO, HI))
    par = pd.DataFrame(index=pd.Index(k["pid"].unique(), name="pid"))
    g = k[k["age"].between(14, 16)].groupby("pid")["fi"].agg(["mean", "count"])
    par["y79"] = g["mean"].where(g["count"] >= 1)
    par["n79"] = g["count"]
    one = (k[k["age"].between(12, 16) & k["fi"].notna()].assign(dist=lambda q: (q["age"] - 14).abs())
           .sort_values(["pid", "dist", "age"]).groupby("pid").first())
    par["y97"], par["age97"] = one["fi"], one["age"]
    g = k[k["age"].between(17, 19)].groupby("pid")["fi"].agg(["mean", "count"])
    par["yz"] = g["mean"].where(g["count"] >= 1)
    g = k[k["age"].between(13, 19)].groupby("pid")["li"].agg(["mean", "count"])
    par["ylab"] = g["mean"].where(g["count"] >= 3)
    s = s.join(par, on="pid")
    for c in ("y79", "y97", "yz", "ylab"):
        s["l" + c] = np.log(s[c])
    hw = s["hlab"] + s["wlab"]
    s["lhwl"] = np.log(hw.where(hw.between(LO, HI)))
    s["coh"] = (s["birth_year"] - 1965) / 10
    s["coh2"] = s["coh"] ** 2
    s["lypcoh"] = s["lyp"] * s["coh"]
    s["src"] = s["fam68"] <= 2930
    return s


def nlsy79_frames():
    n = pd.read_pickle(DATA / "nlsy79_kids.pkl")
    n = n[n["age79"] <= 18].copy().set_index("pid")
    q = pd.read_pickle(DATA / "nlsy79_person_year.pkl")
    q = q[q["age"].between(25, 44)].copy()
    s = q.join(n[["pinc_av", "pinc_pt", "page_av", "fam68"]], on="pid", how="inner")
    s["lyp_av"] = np.log(s["pinc_av"].where(s["pinc_av"] > 0))
    s["lyp_pt"] = np.log(s["pinc_pt"].where(s["pinc_pt"] > 0))
    s["lfam"] = np.log(s["faminc"].where(s["faminc"].between(LO, HI)))
    s["learn"] = np.log(s["earn"].where(s["earn"].between(LO, HI)))
    for kk in range(1, 5):
        s[f"A{kk}"] = ((s["page_av"] - 45) / 10) ** kk
    s["band"], s["agei"] = band_of(s["age"]), s["age"].round().astype(int)
    return s


def nlsy97_frames():
    k, L = ige29.load_extract(False)
    s, _, _ = ige29.nlsy97_frames(k, L)
    return s


# ================================================================ blocks
COH = [("All (26)", None), ("Born 1951-64", (1951, 1964)), ("Born 1965-79", (1965, 1979)),
       ("Born 1980-89", (1980, 1989)), ("Born 1951-56", (1951, 1956)), ("Born 1957-64", (1957, 1964)),
       ("Born 1960-64", (1960, 1964)), ("Born 1980-84", (1980, 1984)), ("Born 1951-74 (reach 45-49)", (1951, 1974))]
COH_ADJ = "All, IGE x cohort (at 1965)"
COH_DIFFS = [("Born 1951-64", "Born 1965-79"), ("Born 1951-64", "Born 1980-89"), ("Born 1965-79", "Born 1980-89"),
             ("Born 1957-64", "Born 1980-84"), (COH_ADJ, "All (26)"), ("Born 1951-74 (reach 45-49)", "All (26)")]


def cohort_block(s):
    for sex, fem in SEXES.items():
        x = s[s["female"] == fem]
        for y, ylab in OUTS:
            fr = {}
            for lab, rng in COH:
                d = x if rng is None else x[x["birth_year"].between(*rng)]
                fr[lab] = prep(d, y, "lyp")
            fr[COH_ADJ] = prep(x, y, "lyp", extra={"c1": "coh", "c2": "coh2", "c3": "lypcoh"})
            R = run(fr, A4 + ["c1", "c2", "c3"])
            for lab in fr:
                summarize(R, "PSID", "cohort", lab, sex, ylab)
            for a, b in COH_DIFFS:
                diff(R, "PSID", "cohort", a, b, sex, ylab)
        print(f"cohort {sex} done", flush=True)


MEAS = [("13-19 mean (>= 3 yrs) [26]", "lyp"), ("NLSY79-like: mean of 1-3 waves at 14-16", "ly79"),
        ("NLSY97-like: one year at 12-16 (nearest 14)", "ly97")]
IVLAB = "IV: one year at 12-16, instrument = mean at 17-19"


def rr_values():
    e = pd.read_csv(OUT / "ige_estimates.csv")
    e = e[(e["data"] == "PSID") & (e["sex"] == "Men")]
    get = lambda par, r: float(e[(e["parent"] == par) & (e["race"] == r)]["rr"].iloc[0])  # noqa: E731
    return {"one": (get("one year at 16", "White"), get("one year at 16", "Black")),
            "mean": (get("mean at 12-17", "White"), get("mean at 12-17", "Black"))}


def measure_block(s, rr):
    base = s[s["lyp"].notna() & s["ly79"].notna() & s["ly97"].notna() & s["lyz"].notna()]
    scW1, scB1 = 1 / rr["one"][0], 1 / rr["one"][1]
    scWm, scBm = 1 / rr["mean"][0], 1 / rr["mean"][1]
    for sex, fem in SEXES.items():
        x = base[base["female"] == fem]
        for y, ylab in OUTS:
            fr = {lab: prep(x, y, col) for lab, col in MEAS}
            fr[IVLAB] = prep(x, y, "ly97", z="lyz")
            R = run(fr, A4)
            for lab in fr:
                summarize(R, "PSID", "measure", lab, sex, ylab)
            m0, m2 = MEAS[0][0], MEAS[2][0]
            summarize(R, "PSID", "measure", m0, sex, ylab, label="13-19 mean / RR (B 0.631, W 0.650)",
                      sc=(scWm, scBm))
            summarize(R, "PSID", "measure", m2, sex, ylab, label="One year / RR (B 0.565, W 0.585)",
                      sc=(scW1, scB1))
            for lab in (MEAS[1][0], m2, IVLAB):
                diff(R, "PSID", "measure", lab, m0, sex, ylab)
            diff(R, "PSID", "measure", IVLAB, m2, sex, ylab)
            diff(R, "PSID", "measure", m2, m0, sex, ylab, label="One year / RR (B 0.565, W 0.585)",
                 sc=(scW1, scB1), scr=(scWm, scBm), ref_label="13-19 mean / RR (B 0.631, W 0.650)")
        print(f"measure {sex} done", flush=True)
    # first stage of the IV and the share of children by measure
    fs = []
    for g in RACES:
        b = base[base["race"] == g].drop_duplicates("pid")
        r = np.corrcoef(b["ly97"], b["lyz"])[0, 1]
        c = np.cov(b["ly97"], b["lyz"])
        fs.append(dict(race=g, children=len(b), corr_one_z=r, slope_z_on_one=c[0, 1] / c[0, 0],
                       corr_one_mean=np.corrcoef(b["ly97"], b["lyp"])[0, 1],
                       corr_79_mean=np.corrcoef(b["ly79"], b["lyp"])[0, 1],
                       mean_n79=b["n79"].mean(), share_base=len(b) / s[s["race"] == g]["pid"].nunique()))
    return pd.DataFrame(fs)


SAMP = ["SRC + SEO (26)", "SRC only", "Weighted (race-specific)", "Balanced (< 35 and >= 35)",
        "Parents: labor income head + spouse", "Both generations: labor income head + spouse",
        "Parents: family income, labor-income sample"]


def sample_block(s):
    for sex, fem in SEXES.items():
        x = s[s["female"] == fem]
        for y, ylab in OUTS:
            h = x[x[y].notna()]
            e_ = h[h["age"] < 35].groupby("pid").size()
            l_ = h[h["age"] >= 35].groupby("pid").size()
            both = set(e_.index) & set(l_.index)
            yl = "lhwl" if y == "lfam" else y
            fr = {SAMP[0]: prep(x, y, "lyp"), SAMP[1]: prep(x[x["src"]], y, "lyp"),
                  SAMP[2]: prep(x, y, "lyp", w="wt"), SAMP[3]: prep(x[x["pid"].isin(both)], y, "lyp"),
                  SAMP[4]: prep(x, y, "lylab"), SAMP[5]: prep(x, yl, "lylab"),
                  SAMP[6]: prep(x[x["lylab"].notna()], y, "lyp")}
            R = run(fr, A4)
            for lab in fr:
                summarize(R, "PSID", "sample", lab, sex, ylab)
            for lab in SAMP[1:]:
                diff(R, "PSID", "sample", lab, SAMP[0], sex, ylab)
            diff(R, "PSID", "sample", SAMP[4], SAMP[6], sex, ylab)
        print(f"sample {sex} done", flush=True)


SIDE = {  # panel -> {data set: spec label}
    "(a) Each data set's main definition": {"PSID": "PSID: 13-19 mean, all cohorts", "NLSY79": "NLSY79: 1978-80 mean",
                                           "NLSY97": "NLSY97: 1996 one year"},
    "(b) One-year parental income": {"PSID": "PSID: one year at 12-16, all cohorts", "NLSY79": "NLSY79: 1978 one year",
                                     "NLSY97": "NLSY97: 1996 one year"},
    "(c) Few-year parental mean": {"PSID": "PSID: 1-3 waves at 14-16, all cohorts",
                                   "NLSY79": "NLSY79: 1978-80 mean",
                                   "NLSY97": "NLSY97: 1996-99 mean (>= 2 years)"},
    "(d) NLSY79 cohort, multi-year": {"PSID": "PSID: born 1960-64, 13-19 mean", "NLSY79": "NLSY79: 1978-80 mean"},
    "(e) NLSY79 cohort, one year": {"PSID": "PSID: born 1960-64, one year at 12-16",
                                    "NLSY79": "NLSY79: 1978 one year"},
    "(f) NLSY97 cohort, one year": {"PSID": "PSID: born 1980-84, one year at 12-16",
                                    "NLSY97": "NLSY97: 1996 one year"},
    "(g) NLSY97 cohort, multi-year": {"PSID": "PSID: born 1980-84, 13-19 mean",
                                      "NLSY97": "NLSY97: 1996-99 mean (>= 2 years)"},
    "(h) NLSY97 same children, one year": {"NLSY97": "NLSY97: 1996 one year, (>= 2 years) sample"},
}


def side_block(s, n79, n97):
    s4 = s[s["band"].isin(BL4)]
    for sex, fem in SEXES.items():
        for y, ylab in OUTS:
            x = s4[s4["female"] == fem]
            c6064, c8084 = x[x["birth_year"].between(1960, 1964)], x[x["birth_year"].between(1980, 1984)]
            fr = {"PSID: 13-19 mean, all cohorts": prep(x, y, "lyp"),
                  "PSID: one year at 12-16, all cohorts": prep(x, y, "ly97"),
                  "PSID: 1-3 waves at 14-16, all cohorts": prep(x, y, "ly79"),
                  "PSID: born 1960-64, 13-19 mean": prep(c6064, y, "lyp"),
                  "PSID: born 1960-64, one year at 12-16": prep(c6064, y, "ly97"),
                  "PSID: born 1980-84, one year at 12-16": prep(c8084, y, "ly97"),
                  "PSID: born 1980-84, 13-19 mean": prep(c8084, y, "lyp")}
            R = run(fr, A4)
            for lab in fr:
                summarize(R, "PSID", "side", lab, sex, ylab)
            x = n79[n79["female"] == fem]
            fr = {"NLSY79: 1978-80 mean": prep(x, y, "lyp_av"), "NLSY79: 1978 one year": prep(x, y, "lyp_pt")}
            R = run(fr, A4)
            for lab in fr:
                summarize(R, "NLSY79", "side", lab, sex, ylab)
            # same-children comparison in the NLSY79 (both measures valid)
            xs = x[x["lyp_av"].notna() & x["lyp_pt"].notna()]
            R = run({"av": prep(xs, y, "lyp_av"), "pt": prep(xs, y, "lyp_pt")}, A4)
            summarize(R, "NLSY79", "side-same", "av", sex, ylab, label="NLSY79 same children: 1978-80 mean")
            summarize(R, "NLSY79", "side-same", "pt", sex, ylab, label="NLSY79 same children: 1978 one year")
            diff(R, "NLSY79", "side-same", "pt", "av", sex, ylab, label="NLSY79 same children: 1978 one year",
                 ref_label="NLSY79 same children: 1978-80 mean")
            x = n97[n97["female"] == fem]
            xm = x[(x["n_av"] >= 2) & x["lyp_av"].notna() & x["lyp_pt"].notna()]
            fr = {"NLSY97: 1996 one year": prep(x, y, "lyp_pt"),
                  "NLSY97: 1996-99 mean (>= 2 years)": prep(xm, y, "lyp_av"),
                  "NLSY97: 1996 one year, (>= 2 years) sample": prep(xm, y, "lyp_pt")}
            R = run(fr, A4 + ["Amiss"])
            for lab in fr:
                summarize(R, "NLSY97", "side", lab, sex, ylab)
            diff(R, "NLSY97", "side", "NLSY97: 1996-99 mean (>= 2 years)", "NLSY97: 1996 one year, (>= 2 years) sample",
                 sex, ylab)
        print(f"side {sex} done", flush=True)


def cross_data(res):
    """differences between data sets (independent) and inverse-variance pooling of the 25-44 gap change."""
    out = []
    for panel, specs in SIDE.items():
        for sex in SEXES:
            for _, ylab in OUTS:
                vals = {}
                for dt, lab in specs.items():
                    r = res.get((dt, "side", lab, sex, ylab, "test", "White - Black", GC, "25-44"))
                    if r is not None:
                        vals[dt] = (r["est"], r["se"])
                if "PSID" in vals:
                    for dt in ("NLSY79", "NLSY97"):
                        if dt in vals:
                            e = vals["PSID"][0] - vals[dt][0]
                            se = np.hypot(vals["PSID"][1], vals[dt][1])
                            out.append(dict(panel=panel, sex=sex, outcome=ylab, stat=f"PSID minus {dt}", est=e, se=se,
                                            p=2 * (1 - norm.cdf(abs(e) / se))))
                if len(vals) >= 2:
                    w = {k: 1 / v[1] ** 2 for k, v in vals.items()}
                    e = sum(w[k] * vals[k][0] for k in vals) / sum(w.values())
                    se = 1 / np.sqrt(sum(w.values()))
                    q = sum(w[k] * (vals[k][0] - e) ** 2 for k in vals)
                    out.append(dict(panel=panel, sex=sex, outcome=ylab, stat="Inverse-variance pooled", est=e, se=se,
                                    p=2 * (1 - norm.cdf(abs(e) / se))))
                    out.append(dict(panel=panel, sex=sex, outcome=ylab, stat="Cochran Q (equal across data sets)",
                                    est=q, se=np.nan, p=1 - chi2.cdf(q, len(vals) - 1), note=f"chi2({len(vals) - 1})"))
    return pd.DataFrame(out)


# ================================================================ output
KEYS = ["data", "block", "spec", "sex", "outcome", "band", "group", "stat", "bandset"]
RESD = {}


def cell(e, se, p, dec=3):
    if e is None or not np.isfinite(e):
        return ""
    pv = "<0.001" if p < 0.001 else f"{p:.3f}"
    return f"{e:.{dec}f}{stars(p)} ({se:.{dec}f}; p={pv})"


def g_(data, block, spec, sex, outcome, band, group, stat, bandset=""):
    return RESD.get((data, block, spec, sex, outcome, band, group, stat, bandset))


def c_(r):
    return "" if r is None else cell(r["est"], r["se"], r["p"])


def wald_(r):
    if r is None:
        return ""
    pv = "<0.001" if r["p"] < 0.001 else f"{r['p']:.3f}"
    return f"{r['note']}{stars(r['p'])} (p={pv})"


def hdr():
    return ["| | " + " | ".join(f"({i + 1}) {sx}: {o}" for i, (sx, o) in enumerate(COLS4)) + " |",
            "|---" * (len(COLS4) + 1) + "|"]


def summary_table(data, block, specs, bs, extra_diff=None):
    """rows = specifications, columns = sex x outcome: gap change (and optional difference vs a reference)."""
    L = hdr()
    for sp in specs:
        L.append(f"| **{sp}** |" + " |" * len(COLS4))
        L.append(f"| Gap change, >= 35 minus < 35 (bands {bs}) | " + " | ".join(
            c_(g_(data, block, sp, sx, o, "test", "White - Black", GC, bs)) for sx, o in COLS4) + " |")
        if extra_diff and sp in extra_diff:
            st = f"Gap change minus [{extra_diff[sp]}]"
            L.append(f"| Difference vs {extra_diff[sp]} | " + " | ".join(
                c_(g_(data, block, sp, sx, o, "test", "White - Black", st, bs)) for sx, o in COLS4) + " |")
    return L


def detail_table(data, block, specs, diffs=None, bandsets=("25-49", "25-44")):
    """row panels = specifications; rows = gap by band, race-specific changes, gap tests, differences, N."""
    L = hdr()
    for sp in specs:
        L.append(f"| **{sp}** |" + " |" * len(COLS4))
        for b in BL:
            rs = [g_(data, block, sp, sx, o, b, "White - Black", "IGE") for sx, o in COLS4]
            if any(r is not None for r in rs):
                L.append(f"| W - B gap, age {b} | " + " | ".join(c_(r) for r in rs) + " |")
        for bs in bandsets:
            if bs == "25-49" and not any(g_(data, block, sp, sx, o, "45-49", "White - Black", "IGE") is not None
                                         for sx, o in COLS4):
                continue
            for g in ("Black", "White"):
                L.append(f"| {g} IGE change, >= 35 minus < 35 ({bs}) | " + " | ".join(
                    c_(g_(data, block, sp, sx, o, "test", g, GC, bs)) for sx, o in COLS4) + " |")
            L.append(f"| **Gap change, >= 35 minus < 35 ({bs})** | " + " | ".join(
                c_(g_(data, block, sp, sx, o, "test", "White - Black", GC, bs)) for sx, o in COLS4) + " |")
            L.append(f"| Gap trend per 10 years ({bs}) | " + " | ".join(
                c_(g_(data, block, sp, sx, o, "test", "White - Black", "Linear trend per 10 years", bs))
                for sx, o in COLS4) + " |")
            L.append(f"| Gap equal in all bands ({bs}) | " + " | ".join(
                wald_(g_(data, block, sp, sx, o, "test", "White - Black", "Equal in all bands (Wald chi2)", bs))
                for sx, o in COLS4) + " |")
            for ref in (diffs or {}).get(sp, []):
                st = f"Gap change minus [{ref}]"
                rs = [g_(data, block, sp, sx, o, "test", "White - Black", st, bs) for sx, o in COLS4]
                if any(r is not None for r in rs):
                    L.append(f"| Gap change minus [{ref}] ({bs}; common bands) | " + " | ".join(c_(r) for r in rs)
                             + " |")
        ns = []
        for sx, o in COLS4:
            tot = [(g_(data, block, sp, sx, o, b, "White - Black", "IGE")) for b in BL]
            tot = [r for r in tot if r is not None]
            if not tot:
                ns.append("")
                continue
            ns.append("B " + "/".join(f"{int(r['nB']):,}" for r in tot) + "; W "
                      + "/".join(f"{int(r['nW']):,}" for r in tot))
        L.append("| Child-years by band (B; W) | " + " | ".join(ns) + " |")
    return L


def side_table(sex, ylab, cx):
    L = ["| | (1) PSID | (2) NLSY79 | (3) NLSY97 | (4) PSID minus NLSY79 | (5) PSID minus NLSY97 | "
         "(6) Pooled (inverse-variance) |", "|---|---|---|---|---|---|---|"]
    for panel, specs in SIDE.items():
        L.append(f"| **{panel}** |" + " |" * 6)
        L.append("| Definition | " + " | ".join(specs.get(dt, "") for dt in ("PSID", "NLSY79", "NLSY97"))
                 + " | | | |")
        for b in BL4:
            L.append(f"| W - B gap, age {b} | " + " | ".join(
                c_(g_(dt, "side", specs[dt], sex, ylab, b, "White - Black", "IGE")) if dt in specs else ""
                for dt in ("PSID", "NLSY79", "NLSY97")) + " | | | |")
        xs = cx[(cx["panel"] == panel) & (cx["sex"] == sex) & (cx["outcome"] == ylab)].set_index("stat")
        pick = lambda st: cell(xs.loc[st, "est"], xs.loc[st, "se"], xs.loc[st, "p"]) if st in xs.index else ""  # noqa
        q = ""
        if "Cochran Q (equal across data sets)" in xs.index:
            r = xs.loc["Cochran Q (equal across data sets)"]
            q = f"; Q {r['note']}={r['est']:.2f} (p={r['p']:.3f})"
        L.append("| **Gap change, >= 35 minus < 35** | " + " | ".join(
            c_(g_(dt, "side", specs[dt], sex, ylab, "test", "White - Black", GC, "25-44")) if dt in specs else ""
            for dt in ("PSID", "NLSY79", "NLSY97")) + f" | {pick('PSID minus NLSY79')} | {pick('PSID minus NLSY97')} | "
            f"{pick('Inverse-variance pooled')}{q} |")
        L.append("| Gap trend per 10 years | " + " | ".join(
            c_(g_(dt, "side", specs[dt], sex, ylab, "test", "White - Black", "Linear trend per 10 years", "25-44"))
            if dt in specs else "" for dt in ("PSID", "NLSY79", "NLSY97")) + " | | | |")
        ns = []
        for dt in ("PSID", "NLSY79", "NLSY97"):
            if dt not in specs:
                ns.append("")
                continue
            tot = [g_(dt, "side", specs[dt], sex, ylab, b, "White - Black", "IGE") for b in BL4]
            tot = [r for r in tot if r is not None]
            ns.append("B " + "/".join(f"{int(r['nB']):,}" for r in tot) + "; W "
                      + "/".join(f"{int(r['nW']):,}" for r in tot))
        L.append("| Child-years by band (B; W) | " + " | ".join(ns) + " | | | |")
    return L


def composition(s):
    x = s[(s["female"] == 0) & s["lfam"].notna() & s["race"].isin(RACES)]
    grp = pd.cut(x["birth_year"], [1950, 1956, 1964, 1972, 1979, 1984, 1989, 1999],
                 labels=["1951-56", "1957-64", "1965-72", "1973-79", "1980-84", "1985-89", "1990-98"])
    L = ["| Birth cohort | " + " | ".join(f"{b} B | {b} W" for b in BL) + " |", "|---" * (2 * len(BL) + 1) + "|"]
    tab = pd.crosstab(grp, [x["band"], x["race"]], normalize="columns") * 100
    for c in tab.index:
        L.append(f"| {c} | " + " | ".join(f"{tab.loc[c, (b, r)]:.0f}" if (b, r) in tab.columns else ""
                                          for b in BL for r in RACES) + " |")
    mb = x.groupby(["band", "race"])["birth_year"].mean()
    L.append("| Mean birth year | " + " | ".join(f"{mb.loc[(b, r)]:.1f}" for b in BL for r in RACES) + " |")
    return L


def write_md(comp, fs, cx, rr):
    L = ["# Age profile of the Black-White log IGE gap: cohort, measurement, sample or chance?", "",
         "Generated by `33.AgeProfileRobustness.py` (2026-10-17). Every cell: coefficient (s.e.; p-value), "
         "*** p<0.01, ** p<0.05, * p<0.1; s.e. clustered by 1968 family (NLSY: first-round household), joint across "
         "bands and specifications of a panel (stacked, fully interacted), normal p-values. W - B gap = White minus "
         "Black log IGE (child-year design of `26.IGEByAge.py`: ln y on ln parental income, quartic in parent's age "
         "at 16, single-year age dummies; Black / White unweighted unless stated). Gap change = mean gap in bands "
         ">= 35 minus mean gap in bands < 35 (positive = the gap opens with age), on bands 25-49 or 25-44 (only "
         "bands with >= 50 child-years and >= 20 children of each race). Columns: one regression set per column, "
         "outcome in the header; row panels = samples / specifications. Child-year N by band at the panel foot.",
         ""]
    L += ["## 0. Cohort composition of the PSID age bands (sons, ln family income, % of child-years)", ""]
    L += comp + ["", "The >= 35 bands are dominated by children born 1951-64; children born after 1979 enter only "
                 "the < 45 bands. An unbalanced age profile therefore mixes age and cohort.", ""]
    # cohorts
    L += ["## 1. Cohorts (PSID, parents = 13-19 mean)", "", "### 1a. Summary: gap change by cohort", ""]
    sp = [c for c, _ in COH] + [COH_ADJ]
    L += ["Bands 25-49 (cohorts born after 1974 reach at most 40-44, so their change uses fewer bands):", ""]
    L += summary_table("PSID", "cohort", sp, "25-49") + [""]
    L += ["Bands 25-44 (comparable with the NLSY97):", ""]
    L += summary_table("PSID", "cohort", sp, "25-44") + [""]
    dd = {}
    for a, b in COH_DIFFS:
        dd.setdefault(a, []).append(b)
    L += ["### 1b. Detail", "", f"'{COH_ADJ}': controls (birth year - 1965)/10, its square and ln parental income x "
          "it in every cell; the band IGE is that of the 1965 cohort (linear cohort trend in the IGE, band-specific).",
          ""]
    L += detail_table("PSID", "cohort", sp, dd) + [""]
    # measurement
    m0, m1, m2 = (m for m, _ in MEAS)
    msp = [m0, m1, m2, "13-19 mean / RR (B 0.631, W 0.650)", "One year / RR (B 0.565, W 0.585)", IVLAB]
    L += ["## 2. Parental-income measurement (PSID, the same children under every measure)", "",
          "Children of 26's sample with a valid 13-19 mean (>= 3 years), >= 1 wave at 14-16, a wave at 12-16 and "
          "parental income at 17-19 (the IV instrument). RR = PSID race-specific reliability ratios of "
          f"`4.Estimates.py` (one year: W {rr['one'][0]:.3f}, B {rr['one'][1]:.3f}; multi-year mean: W "
          f"{rr['mean'][0]:.3f}, B {rr['mean'][1]:.3f}), treated as known. IV: one-year measure instrumented by the "
          "mean parental income at child ages 17-19.", "", "Measures (children, one row per child):", "",
          "| Race | Children | Share of 26's children | Corr(1 yr, 13-19 mean) | Corr(1-3 waves at 14-16, 13-19 "
          "mean) | Mean waves at 14-16 | Corr(1 yr, 17-19 mean) | First stage: slope of 17-19 mean on 1 yr |",
          "|---|---|---|---|---|---|---|---|"]
    for r in fs.itertuples():
        L.append(f"| {r.race} | {r.children:,} | {r.share_base:.2f} | {r.corr_one_mean:.3f} | {r.corr_79_mean:.3f} | "
                 f"{r.mean_n79:.2f} | {r.corr_one_z:.3f} | {r.slope_z_on_one:.3f} |")
    L += ["", "### 2a. Summary", ""]
    L += summary_table("PSID", "measure", msp, "25-49", {m1: m0, m2: m0, IVLAB: m0}) + [""]
    L += summary_table("PSID", "measure", msp, "25-44", {m1: m0, m2: m0, IVLAB: m0}) + [""]
    L += ["### 2b. Detail", ""]
    L += detail_table("PSID", "measure", msp, {m1: [m0], m2: [m0], IVLAB: [m0, m2],
                                               "One year / RR (B 0.565, W 0.585)":
                                                   ["13-19 mean / RR (B 0.631, W 0.650)"]}) + [""]
    # sample
    L += ["## 3. Sample and income concept (PSID, parents = 13-19 mean)", "",
          "SRC only: 1968 family number <= 2930. Weighted: Black and White regressions weighted by the child-year "
          "core longitudinal weight. Balanced: children with the outcome in a band < 35 and in a band >= 35. "
          "Labor income = head + spouse labor income (parents: 13-19 mean, >= 3 years in bounds); 'both "
          "generations': the family-income column (1)/(3) uses ln head + spouse labor income of the child's "
          "household as outcome. 'Family income, labor-income sample': parents' family income on the children whose "
          "parents have the labor-income measure (separates concept from sample).", "", "### 3a. Summary", ""]
    L += summary_table("PSID", "sample", SAMP, "25-49", {s_: SAMP[0] for s_ in SAMP[1:]}) + [""]
    L += summary_table("PSID", "sample", SAMP, "25-44", {s_: SAMP[0] for s_ in SAMP[1:]}) + [""]
    L += ["### 3b. Detail", ""]
    dd = {**{s_: [SAMP[0]] for s_ in SAMP[1:]}, SAMP[4]: [SAMP[0], SAMP[6]]}
    L += detail_table("PSID", "sample", SAMP, dd) + [""]
    # side by side
    L += ["## 4. PSID, NLSY79, NLSY97 side by side (bands 25-29 ... 40-44)", "",
          "Columns (1)-(3): one regression set per data set, outcome in the section header; (4)-(5): difference of "
          "the gap change between data sets (independent samples); (6): inverse-variance pooled gap change of the "
          "data sets in the panel, with Cochran's Q test that they are equal. PSID one year = the wave at child "
          "ages 12-16 nearest 14; PSID few-year = mean of the 1-3 waves at 14-16; NLSY79 one year = 1978 income "
          "(1979 round), few-year = 1978-80 (1-3 rounds at home); NLSY97 one year = 1996 (parent report), "
          "multi-year = 1996-99 for youths with >= 2 years at home (later years youth-reported; older, selected "
          "subsample, see 29). PSID children are heads / spouses only; NLSY children are all respondents.", ""]
    for sex in SEXES:
        for _, ylab in OUTS:
            L += [f"### {sex}, {ylab}", ""] + side_table(sex, ylab, cx) + [""]
    L += ["### NLSY79 one year vs 1978-80 mean on the same children (bands 25-44)", ""]
    L += detail_table("NLSY79", "side-same", ["NLSY79 same children: 1978-80 mean",
                                              "NLSY79 same children: 1978 one year"],
                      {"NLSY79 same children: 1978 one year": ["NLSY79 same children: 1978-80 mean"]},
                      bandsets=("25-44",)) + [""]
    L += ["### NLSY97 multi-year vs one year on the same children (bands 25-44)", ""]
    L += detail_table("NLSY97", "side", ["NLSY97: 1996 one year, (>= 2 years) sample",
                                         "NLSY97: 1996-99 mean (>= 2 years)"],
                      {"NLSY97: 1996-99 mean (>= 2 years)": ["NLSY97: 1996 one year, (>= 2 years) sample"]},
                      bandsets=("25-44",)) + [""]
    (OUT / "age_profile_robustness.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    pal = ["#6250d6", "#eda100", "#008300", "#eb6834", "#2a78d6"]
    mk = ["s", "^", "o", "D", "v"]
    sex, y = "Sons", FAM
    panels = [
        ("PSID by birth cohort", [("PSID", "cohort", c) for c in ("All (26)", "Born 1951-64", "Born 1965-79",
                                                                  "Born 1980-89")], BL),
        ("PSID by parental-income measure (same children)",
         [("PSID", "measure", m) for m in (MEAS[0][0], MEAS[1][0], MEAS[2][0], IVLAB)], BL),
        ("PSID by sample", [("PSID", "sample", m) for m in (SAMP[0], SAMP[1], SAMP[2], SAMP[3], SAMP[4])], BL),
        ("Main definitions", [(dt, "side", SIDE["(a) Each data set's main definition"][dt])
                              for dt in ("PSID", "NLSY79", "NLSY97")], BL4),
        ("One-year parental income", [(dt, "side", SIDE["(b) One-year parental income"][dt])
                                      for dt in ("PSID", "NLSY79", "NLSY97")], BL4),
        ("Matched cohorts", [("PSID", "side", "PSID: born 1960-64, 13-19 mean"), ("NLSY79", "side",
                                                                                "NLSY79: 1978-80 mean"),
                             ("NLSY97", "side", "NLSY97: 1996 one year"),
                             ("PSID", "side", "PSID: born 1980-84, one year at 12-16")], BL4),
    ]
    short = {MEAS[0][0]: "13-19 mean", MEAS[1][0]: "1-3 waves at 14-16", MEAS[2][0]: "one year at 12-16",
             IVLAB: "IV (one year; instr. 17-19)", "All (26)": "All cohorts"}
    fig, axes = plt.subplots(2, 3, figsize=(14, 8.8), sharey=True)
    for ax, (title, series, bands) in zip(axes.ravel(), panels):
        k = len(series)
        for i, (dt, blk, sp) in enumerate(series):
            off = (i - (k - 1) / 2) * 0.55
            pts = [(MID[b] + off, g_(dt, blk, sp, sex, y, b, "White - Black", "IGE")) for b in bands]
            pts = [(xx, r) for xx, r in pts if r is not None]
            if not pts:
                continue
            col = pal[i]
            if blk == "side" and title != "Matched cohorts":
                col = pal[("PSID", "NLSY79", "NLSY97").index(dt)]
            lab = short.get(sp, sp)
            ax.errorbar([xx for xx, _ in pts], [r["est"] for _, r in pts], yerr=[1.96 * r["se"] for _, r in pts],
                        color=col, lw=1.8, marker=mk[i], ms=6, elinewidth=1.0, label=lab)
        ax.axhline(0, color="#bbbbbb", lw=0.8)
        ax.grid(axis="y", color="#e5e5e5", lw=0.6)
        ax.set_xticks([MID[b] for b in bands], bands)
        ax.set_xlim(MID[BL[0]] - 2.5, MID[BL[-1]] + 2.5)
        ax.set_title(title, fontsize=10.5)
        for sp_ in ("top", "right"):
            ax.spines[sp_].set_visible(False)
        ax.legend(frameon=False, fontsize=7.8, loc="upper left")
    for ax in axes[:, 0]:
        ax.set_ylabel("White - Black log IGE gap")
    for ax in axes[1]:
        ax.set_xlabel("Son's age at measurement (band)")
    fig.text(0.5, 0.005, "Sons, ln family income; child-year design; band estimates with 95% CI (clustered). "
             "Top: PSID robustness, bands 25-49. Bottom: PSID / NLSY79 / NLSY97, bands 25-44. NLSY79 = born 1960-64, "
             "NLSY97 = born 1980-84.", ha="center", fontsize=8.5, color="#52514e")
    fig.tight_layout(rect=(0, 0.025, 1, 1))
    fig.savefig(OUT / "age_profile_robustness.png", dpi=150)


def main():
    s = psid_frames()
    print("PSID frame:", s.shape, flush=True)
    rr = rr_values()
    comp = composition(s)
    cohort_block(s)
    fs = measure_block(s, rr)
    sample_block(s)
    n79, n97 = nlsy79_frames(), nlsy97_frames()
    side_block(s, n79, n97)
    res = pd.DataFrame(ROWS)
    RESD.update({tuple(r[k] for k in KEYS): r for r in res.to_dict("records")})
    cx = cross_data(RESD)
    OUT.mkdir(exist_ok=True)
    allres = pd.concat([res, cx.assign(data="cross", block="side", spec=cx["panel"], band="test",
                                       group="White - Black", bandset="25-44").drop(columns="panel")],
                       ignore_index=True)
    allres.to_csv(OUT / "age_profile_robustness.csv", index=False)
    write_md(comp, fs, cx, rr)
    figure()
    show = res[(res["band"] == "test") & (res["group"] == "White - Black") & (res["stat"] == GC)]
    show = show.assign(c=[cell(e, se, p) for e, se, p in zip(show.est, show.se, show.p)])
    pd.set_option("display.width", 250)
    pd.set_option("display.max_colwidth", 60)
    pd.set_option("display.max_rows", 500)
    print(show.pivot_table(index=["data", "block", "spec", "bandset"], columns=["sex", "outcome"], values="c",
                           aggfunc="first", sort=False).to_string())
    print(cx.to_string())


if __name__ == "__main__":
    main()
