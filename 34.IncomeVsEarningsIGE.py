r"""Family-income IGE vs earnings IGE, by race, sex and age; why they differ (2026-10-17).

PI question: "Dig deeper into family income IGE vs earnings IGE, by race. Do they differ by a lot? And by age?"

DATA (read only): data/psid_person_year.pkl (1.PSID.py), the NLSY79 frames of 26.IGEByAge.py
(data/nlsy79_kids.pkl, nlsy79_person_year.pkl) and the NLSY97 extract of 29.NLSY97AgeProfile.py
(data/nlsy97_ap_kids.pkl, nlsy97_ap_person_year.pkl). Nothing is written to Dropbox.

PSID DEFINITIONS (6.IGEMain.py unless stated)
  Children: SRC + SEO, the head's child at wave-ages 13-19; as adults, child-years as head or spouse / partner
  ("wife") at 25-65 for the Lee-Solon design (as 6.IGEMain.py) and 25-55 for the age bands. Race = race of the
  parental head. Yearly amounts outside $100-$150,000 of 1967 dropped from logs.
  Parental measures (means over the income years of the child's wave-ages 13-19, >= 3 years in bounds):
    (P1) parental total family income (benchmark, 6.IGEMain.py);
    (P2) the same on father-present children (sample of P3, for comparability);
    (P3) father's labor earnings = the head's labor income in waves with a male head, for children whose head at 16
         (nearest wave) is male (24.IGEDecomposition.py's father; here no hours / wage validity screen);
    (P4) parents' combined labor income = head + wife labor income (single parents: the head's own).
  Child outcomes (child's own family unit, income year = wave - 1):
    own earnings  = the child's own labor income (head or wife labor income; 1994+ incl. the labor part of business
                    income, 1.PSID.py);
    spouse earnings = the other partner's labor income (wife's if the child is head, head's if the child is wife);
                    0 if the child has no spouse / partner in the family unit; "partnered" = spouse / partner present;
    couple earnings = own + spouse; other income = family income - couple earnings (transfers, asset income,
                    other family members' income, business / farm income not counted as labor).
    Logs: ln family income; ln own earnings (> 0); ln spouse earnings (> 0, partnered years); ln couple earnings.
    Employed = own earnings >= $100 of 1967 (LPM).
DESIGNS
  1 Lee-Solon IGE at 40 (6.IGEMain.py): child-years 25-65; ln y on ln parental measure x, quartics in (A-45)/10
    (A = parental head's age at 16) and (age-40)/10, and x * ((age-40)/10)^n, n = 1..4; coefficient on x = IGE at 40.
    Black / White unweighted; Pooled = all races weighted by the child-year core longitudinal weight.
    Rank-rank slope "around 40": child's mean outcome over ages 35-44 (>= 2 years; zeros kept; spouse earnings over
    partnered years), ranked within birth year among all children (both sexes, all races) with the outcome;
    parental measure ranked within the child's birth year among all children in the parental sample; weighted by
    the core longitudinal weight at child age 16 (race cells and pooled alike; 26.IGEByAge.py convention).
  2 Age bands 25-29 ... 50-55 + Chetty's 31-37 window (26.IGEByAge.py child-year design): ln y on x (P1), quartic in
    (A-45)/10, single-year age dummies, in each band x group cell. Ranks by band: band means (>= 2 years) ranked
    within birth year and band.
  3 Decomposition of the family-income IGE, common sample = child-years with family income in bounds, own
    earnings > 0 in bounds and spouse earnings known:
      ln Y = ln E_own + ln[(E_own + E_sp)/E_own] + ln[Y/(E_own + E_sp)]
    so beta_famY = beta_own + beta_spouse + beta_other EXACTLY (same rows, same regressors). The spouse term is 0
    for unpartnered years, so it contains marriage (the extensive margin) and the spouse's earnings given marriage:
      beta_spouse ~ mbar_s|m * beta_P + Pbar * beta_s|m (+ remainder),
    beta_P = gradient of partnered (LPM), beta_s|m = gradient of the spouse term among the partnered, means fixed.
    Also a LEVEL decomposition free of ordering and of the positive-earnings restriction: each component divided by
    the race x sex x single-year-of-age mean family income (pooled: the all-race weighted mean),
      Y/Ybar = E_own/Ybar + E_sp/Ybar + O/Ybar,
    regressed on x; the slopes add up to the semi-elasticity of mean family income (sample: family income in bounds,
    own and spouse earnings <= $150,000 of 1967 and known). Plus "holding marriage fixed": ln family income with a
    partnered control, within partnered and within unpartnered child-years.
  4 Margins: employment (LPM) gradient; ln of the band mean of own earnings with zero years averaged in vs over
    positive years only (child-band rows, A quartic + mean age); rank of band-mean earnings with zeros kept vs over
    positive years only.
  5 NLSY79 (born 1960-64; parents = 1978-80 mean family income; 26.IGEByAge.py frame) and NLSY97 (born 1980-84;
    parents = 1996 income; 29.NLSY97AgeProfile.py frame, A quartic + missing-A dummy): family income vs own
    earnings, Lee-Solon (NLSY79 at 40; NLSY97 at 35 and 40, observed to 44) and by band, plus rank slopes and
    employment. No spouse earnings in these extracts.
INFERENCE: within each table, every cell (outcome x parental measure x band x group) is its own (W)LS regression;
  the joint covariance is the cluster-robust sandwich of the stacked fully interacted regression (26.IGEByAge.Cells;
  clusters = 1968 family; NLSY: first-round household), so cross-outcome tests on the same children, cross-race
  gaps and cross-band tests are valid. Tests across the six bands (25-29 ... 50-55; 31-37 never enters):
  Wald test of equality, linear trend per 10 years of band midpoint, mean >= 35 minus mean < 35. Normal p-values.
  *** p<0.01, ** p<0.05, * p<0.1.
Writes output/income_vs_earnings_ige.csv (every estimate), output/income_vs_earnings_ige.md,
output/income_vs_earnings_ige.png.
"""
import importlib.util
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import DATA, OUT, stars  # noqa: E402

warnings.simplefilter("ignore", FutureWarning)
warnings.simplefilter("ignore", RuntimeWarning)


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ige6 = _load("ige6", "6.IGEMain.py")
ige26 = _load("ige26", "26.IGEByAge.py")
ige29 = _load("ige29", "29.NLSY97AgeProfile.py")
Cells, rank_in = ige26.Cells, ige26.rank_in

LO, HI = ige6.LO, ige6.HI
BANDS = [(25, 29), (30, 34), (35, 39), (40, 44), (45, 49), (50, 55)]
BL = [f"{a}-{b}" for a, b in BANDS]
CH = "31-37"
MID = dict(zip(BL, [(a + b) / 2 for a, b in BANDS]))
RACES = ("Black", "White")
PG = "Pooled (weighted)"
GW = "White - Black"
A4 = [f"A{n}" for n in range(1, 5)]
C4 = [f"C{n}" for n in range(1, 5)]
XC4 = [f"xC{n}" for n in range(1, 5)]
SEXES = (("Sons", 0), ("Daughters", 1))
ROWS = []
RES = {}

FAM, ERN = "ln family income", "ln own earnings (>0)"
MEAS = [("lyp", "Parental family income"), ("lyp_fp", "Parental family income, father-present"),
        ("lyfe", "Father's labor earnings"), ("lypl", "Parents' combined labor income")]
GRID_Y = [("lfam", FAM), ("learn", ERN), ("lsp", "ln spouse's earnings (>0, partnered)"),
          ("lcpl", "ln own + spouse earnings")]


def record(key, e, se, p, **info):
    RES[key] = (e, se, p)
    ROWS.append(dict(zip(("data", "part", "sex", "outcome", "measure", "band", "group", "stat"), key), est=e, se=se,
                     p=p, **{k: v for k, v in info.items() if k in ("n", "children", "clusters", "note")}))


def cell(r, dec=3):
    if r is None or not np.isfinite(r[0]):
        return ""
    e, se, p = r[:3]
    pv = "<0.001" if p < 0.001 else f"{p:.3f}"
    return f"{e:.{dec}f}{stars(p)} ({se:.{dec}f}; p={pv})"


def neg(t):
    return [(c, n, -w) for c, n, w in t]


# ================================================================ stacking
def piece(d, key, y, x, w, keep, ls=False, pc=False):
    d = d[d[y].notna() & d[x].notna()]
    if w is not None:
        d = d[d[w] > 0]
    out = d[[c for c in keep if c in d]].copy()
    out["_y"], out["_x"] = d[y].astype(float), d[x].astype(float)
    out["_w"] = 1.0 if w is None else d[w].astype(float)
    if ls:
        for n in range(1, 5):
            out[f"xC{n}"] = out["_x"] * d[f"C{n}"]
    out["pc"] = d["partnered"].astype(float) if pc else 0.0
    out["cell"] = [key] * len(out)
    return out


def by_group(d, pooled_w="wt", weight_all=None):
    """(group, frame, weight column): race cells unweighted (or weighted by weight_all), pooled weighted."""
    for g in RACES:
        yield g, d[d["race"] == g], weight_all
    yield PG, d, (weight_all or pooled_w)


def band_rows(d, b):
    return d[d["age"].between(31, 37)] if b == CH else d[d["band"] == b]


def tests(R, bands, term):
    """Wald equality, linear trend per 10 years, mean >= 35 minus mean < 35, over the bands present."""
    bands = [b for b in bands if all((t[0], t[1]) in R.ix for t in term(b))]
    out = {}
    if len(bands) >= 2:
        st, df, p = R.wald([term(b) + neg(term(bands[0])) for b in bands[1:]])
        out["wald"] = (st, np.nan, p, df)
        mm = np.array([MID[b] for b in bands], float)
        c = (mm - mm.mean()) / ((mm - mm.mean()) ** 2).sum() * 10
        out["trend"] = R.lin([(t[0], t[1], t[2] * cw) for b, cw in zip(bands, c) for t in term(b)])
    early, late = [b for b in bands if MID[b] < 35], [b for b in bands if MID[b] >= 35]
    if early and late:
        out["change"] = R.lin([(t[0], t[1], t[2] / len(late)) for b in late for t in term(b)]
                              + [(t[0], t[1], -t[2] / len(early)) for b in early for t in term(b)])
    return out


def wald_txt(r):
    if r is None:
        return ""
    st, _, p, df = r
    pv = "<0.001" if p < 0.001 else f"{p:.3f}"
    return f"chi2({df})={st:.2f}{stars(p)} (p={pv})"


TESTNAMES = [("wald", "Equal in all bands (Wald)"), ("trend", "Linear trend per 10 years"),
             ("change", "Mean >= 35 minus mean < 35")]


def tcell(k, r):
    return wald_txt(r) if k == "wald" else cell(r)


def T(y, g, *extra):
    return lambda b: [((y, b, g, *extra), "x", 1.0)]


def TG(y, *extra):
    return lambda b: [((y, b, "White", *extra), "x", 1.0), ((y, b, "Black", *extra), "x", -1.0)]


def TSUB(t1, t2):
    return lambda b: t1(b) + neg(t2(b))


# ================================================================ PSID frames
def psid_frames():
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    s = ige6.build(py)
    wives = py.loc[py["wife"], ["wave", "int"]].drop_duplicates().assign(_hw=1.0)
    s = s.merge(wives, on=["wave", "int"], how="left")
    s["partnered"] = np.where(s["wife"] | s["_hw"].eq(1), 1.0, 0.0)
    s["own"] = s["earn"]
    s["sp"] = np.where(s["head"], s["wlab"], s["hlab"])
    s.loc[s["partnered"] == 0, "sp"] = 0.0
    s["couple"] = s["own"] + s["sp"]
    s["other"] = s["faminc"] - s["couple"]
    s["lsp"] = np.log(s["sp"].where((s["partnered"] == 1) & s["sp"].between(LO, HI)))
    s["lcpl"] = np.log(s["couple"].where(s["couple"].between(LO, HI)))
    s["emp"] = (s["own"] >= LO).astype(float).where(s["own"].notna())
    s["wt"] = s["wt"].astype(float)
    s["band"] = ige26.band_of(s["age"])
    s["agei"] = s["age"].round().astype(int)

    # ---- parental measures
    k = py[py["child"] & py["age"].between(13, 19)].copy()
    hd = py[py["head"]][["wave", "int", "female"]].drop_duplicates(["wave", "int"]).rename(columns={"female": "hfem"})
    k = k.merge(hd, on=["wave", "int"], how="left")
    k["fe"] = k["hlab"].where((k["hfem"] == 0) & k["hlab"].between(LO, HI))
    pl = k["hlab"] + k["wlab"]
    k["pl"] = pl.where(pl.between(LO, HI))
    g = k.groupby("pid")
    par = pd.DataFrame({"yfe": g["fe"].mean(), "nfe": g["fe"].count(), "ypl": g["pl"].mean(), "npl": g["pl"].count()})
    k16 = k.assign(dist=(k["age"] - 16).abs()).sort_values(["pid", "dist"]).groupby("pid").first()
    par["fp16"] = k16["hfem"].eq(0)
    par["w"] = k16["wt"].astype(float)
    par["birth_year"], par["female"], par["fam68"] = k16["birth_year"], k16["female"], k16["fam68"]
    par["yfe"] = par["yfe"].where((par["nfe"] >= 3) & par["fp16"])
    par["ypl"] = par["ypl"].where(par["npl"] >= 3)
    P = ige6.parents(py).join(par, how="left")
    s = s.join(P[["yfe", "ypl"]], on="pid")
    s["lyfe"], s["lypl"] = np.log(s["yfe"]), np.log(s["ypl"])
    s["lyp_fp"] = s["lyp"].where(s["lyfe"].notna())

    # ---- decomposition variables
    cs = s["lfam"].notna() & s["learn"].notna() & s["sp"].notna() & (s["sp"] >= 0)
    s["cs"] = cs
    s["lfam_cs"] = s["lfam"].where(cs)
    s["d_own"] = s["learn"].where(cs)
    s["d_sp"] = np.log(s["couple"] / s["own"]).where(cs)
    s["d_oth"] = (s["lfam"] - np.log(s["couple"])).where(cs)
    s["part_cs"] = s["partnered"].where(cs)
    s["d_sp_m"] = s["d_sp"].where(cs & (s["partnered"] == 1))
    s["lfam_pc"] = s["lfam_cs"]
    s["lfam_m"] = s["lfam_cs"].where(s["partnered"] == 1)
    s["lfam_s"] = s["lfam_cs"].where(s["partnered"] == 0)
    s["lfam_all_pc"] = s["lfam"].where(s["partnered"].notna())
    # level components
    lv = s["faminc"].between(LO, HI) & s["own"].between(0, HI) & s["sp"].between(0, HI)
    s["lv"] = lv
    ybar = s[lv].groupby(["race", "female", "agei"])["faminc"].mean().rename("ybar")
    s = s.join(ybar, on=["race", "female", "agei"])
    q = s[lv & (s["wt"] > 0)]
    ybp = q.groupby(["female", "agei"]).apply(lambda z: np.average(z["faminc"], weights=z["wt"])).rename("ybarP")
    s = s.join(ybp, on=["female", "agei"])
    for nm, c in (("fam", "faminc"), ("own", "own"), ("sp", "sp"), ("oth", "other")):
        s["lv_" + nm] = (s[c] / s["ybar"]).where(lv)
        s["lvP_" + nm] = (s[c] / s["ybarP"]).where(lv)
    s["lv_part"] = s["partnered"].where(lv)
    s["lvP_part"] = s["lv_part"]
    s["lv_sp_m"] = s["lv_sp"].where(s["partnered"] == 1)
    s["lvP_sp_m"] = s["lvP_sp"].where(s["partnered"] == 1)
    # common sample for the by-age comparison: family income and positive earnings both valid
    both = s["lfam"].notna() & s["learn"].notna()
    s["lfam_c"], s["learn_c"] = s["lfam"].where(both), s["learn"].where(both)
    return s, P


def psid_rank_frame(s, P):
    """child x window rows with parent ranks and child ranks (within birth year and window, both sexes)."""
    P = P[P["race"].notna()].copy()
    for m, c in (("fi", "yp"), ("fe", "yfe"), ("pl", "ypl")):
        P["rp_" + m] = rank_in(P, c, "birth_year")
    wins = list(zip(BL, BANDS)) + [(CH, (31, 37)), ("35-44", (35, 44))]
    out = []
    for lab, (lo, hi) in wins:
        h = s[s["age"].between(lo, hi)]

        def mean_of(col, mask=None):
            hh = h[h[col].notna() & (True if mask is None else mask.loc[h.index])]
            gg = hh.groupby("pid")[col].agg(["mean", "count"])
            return gg.loc[gg["count"] >= 2, "mean"]

        x = P[["race", "female", "birth_year", "fam68", "w", "rp_fi", "rp_fe", "rp_pl"]].copy()
        x["yf"] = mean_of("faminc").reindex(x.index)
        x["ye"] = mean_of("own").reindex(x.index)
        x["yep"] = mean_of("own", s["own"] >= LO).reindex(x.index)
        x["ysp"] = mean_of("sp", s["partnered"] == 1).reindex(x.index)
        x["ycp"] = mean_of("couple").reindex(x.index)
        x["window"] = lab
        out.append(x)
    r = pd.concat(out).rename_axis("pid").reset_index()
    for y in ("yf", "ye", "yep", "ysp", "ycp"):
        r["r" + y] = rank_in(r, y, ["birth_year", "window"])
    return r


def band_mean_frame(s, ctrl, bands):
    """child x band rows: ln mean own earnings with zero years averaged in, and over positive years only."""
    out = []
    for b in bands + [CH]:
        h = band_rows(s[s["own"].notna()], b)
        g = h.groupby("pid")
        m = pd.DataFrame({"m_all": g["own"].mean(), "n": g["own"].count(), "agem": g["age"].mean(),
                          "wt": g["wt"].mean()})
        hp = h[h["own"] >= LO].groupby("pid")["own"].agg(["mean", "count"])
        m["m_pos"] = hp.loc[hp["count"] >= 2, "mean"]
        m = m[m["n"] >= 2].join(g[["lyp", "race", "fam68", "female", *ctrl]].first())
        m["lbm_all"] = np.log(m["m_all"].where(m["m_all"] >= LO))
        m["lbm_pos"] = np.log(m["m_pos"])
        m["agec"] = m["agem"] - (MID.get(b, 34))
        m["band"] = b
        out.append(m)
    return pd.concat(out).reset_index()


# ================================================================ PART 1: grid at 40
def grid_block(data, s, r, ctrlA, measures, outcomes, sexes):
    L = []
    for sex, fem in sexes:
        x = s[s["female"] == fem]
        log_res = {}
        for mcol, mlab in measures:
            if mcol not in x or x[mcol].notna().sum() == 0:
                continue
            parts = []
            for ycol, _ in outcomes + [("emp", "Employed (LPM)"), ("partnered", "Partnered (LPM)")]:
                if ycol not in x:
                    continue
                for g, d, w in by_group(x):
                    parts.append(piece(d, (ycol, g), ycol, mcol, w, ["pid", "fam68", *ctrlA, *C4], ls=True))
            R = Cells(pd.concat(parts, ignore_index=True), "_y", "_x", "cell", ctrlA + C4 + XC4, w="_w")
            for ycol, _ in outcomes + [("emp", "Employed (LPM)"), ("partnered", "Partnered (LPM)")]:
                if not R.has((ycol, "Black")):
                    continue
                for g in RACES + (PG,):
                    record((data, "1 grid log", sex, ycol, mcol, "40", g, "IGE"), *R.lin([((ycol, g), "x", 1)]),
                           **R.info[(ycol, g)])
                record((data, "1 grid log", sex, ycol, mcol, "40", GW, "IGE"),
                       *R.lin([((ycol, "White"), "x", 1), ((ycol, "Black"), "x", -1)]))
            # within race: family income minus each other outcome (same children)
            for ycol, _ in outcomes[1:]:
                if not (R.has((ycol, "Black")) and R.has(("lfam", "Black"))):
                    continue
                for g in RACES + (PG,):
                    record((data, "1 grid log", sex, "lfam - " + ycol, mcol, "40", g, "IGE diff"),
                           *R.lin([(("lfam", g), "x", 1), ((ycol, g), "x", -1)]))
                record((data, "1 grid log", sex, "lfam - " + ycol, mcol, "40", GW, "IGE diff"),
                       *R.lin([(("lfam", "White"), "x", 1), (("lfam", "Black"), "x", -1),
                               ((ycol, "White"), "x", -1), ((ycol, "Black"), "x", 1)]))
            log_res[mcol] = R
        # ranks (35-44 window)
        if r is not None:
            rr = r[(r["female"] == fem) & (r["window"] == "35-44")]
            parts = []
            for m, mcol in (("fi", "lyp"), ("fe", "lyfe"), ("pl", "lypl")):
                if "rp_" + m not in rr:
                    continue
                for y in ("ryf", "rye", "rysp", "rycp"):
                    for g, d, w in by_group(rr, weight_all="w"):
                        parts.append(piece(d, (y, m, g), y, "rp_" + m, w, ["pid", "fam68"]))
            R = Cells(pd.concat(parts, ignore_index=True), "_y", "_x", "cell", [], w="_w")
            for m, mcol in (("fi", "lyp"), ("fe", "lyfe"), ("pl", "lypl")):
                for y in ("ryf", "rye", "rysp", "rycp"):
                    if not R.has((y, m, "Black")):
                        continue
                    for g in RACES + (PG,):
                        record((data, "1 grid rank", sex, y, mcol, "35-44", g, "slope"),
                               *R.lin([((y, m, g), "x", 1)]), **R.info[(y, m, g)])
                    record((data, "1 grid rank", sex, y, mcol, "35-44", GW, "slope"),
                           *R.lin([((y, m, "White"), "x", 1), ((y, m, "Black"), "x", -1)]))
                    if y != "ryf":
                        for g in RACES + (PG,):
                            record((data, "1 grid rank", sex, "ryf - " + y, mcol, "35-44", g, "slope diff"),
                                   *R.lin([(("ryf", m, g), "x", 1), ((y, m, g), "x", -1)]))
                        record((data, "1 grid rank", sex, "ryf - " + y, mcol, "35-44", GW, "slope diff"),
                               *R.lin([(("ryf", m, "White"), "x", 1), (("ryf", m, "Black"), "x", -1),
                                       ((y, m, "White"), "x", -1), ((y, m, "Black"), "x", 1)]))
    return L


def grid_md(data, measures, outcomes, sexes, rank=True):
    L = []
    cols = [lab for _, lab in outcomes] + [f"{FAM} minus {lab} (test)" for _, lab in outcomes[1:]]
    for sex, _ in sexes:
        L += [f"### {data} {sex}: log IGE at 40 (Lee-Solon)", "",
              "| | " + " | ".join(f"({i + 1}) {c}" for i, c in enumerate(cols)) + " |", "|---" * (len(cols) + 1) + "|"]
        for g in RACES + (GW, PG):
            L.append(f"| **{sex}: {g}** |" + " |" * len(cols))
            for mcol, mlab in measures:
                vals = [cell(RES.get((data, "1 grid log", sex, y, mcol, "40", g, "IGE"))) for y, _ in outcomes]
                vals += [cell(RES.get((data, "1 grid log", sex, "lfam - " + y, mcol, "40", g, "IGE diff")))
                         for y, _ in outcomes[1:]]
                if any(vals):
                    L.append(f"| ln {mlab} | " + " | ".join(vals) + " |")
        L.append("| N child-years / children (B; W), parental family income | " + " | ".join(
            n_txt(data, "1 grid log", sex, y, "lyp", "40") for y, _ in outcomes) + " |" * (len(outcomes) - 1) + " |")
        L.append("| N child-years / children (B; W), father's earnings | " + " | ".join(
            n_txt(data, "1 grid log", sex, y, "lyfe", "40") for y, _ in outcomes) + " |" * (len(outcomes) - 1) + " |")
        L.append("")
        if not rank:
            continue
        rc = [("ryf", "Rank of family income"), ("rye", "Rank of own earnings (zeros kept)"),
              ("rysp", "Rank of spouse's earnings (partnered years, zeros kept)"), ("rycp", "Rank of own + spouse earnings")]
        cols2 = [c for _, c in rc] + [f"(1) minus ({i + 2}) (test)" for i in range(3)]
        L += [f"### {data} {sex}: rank-rank slope, child's mean at 35-44", "",
              "| | " + " | ".join(f"({i + 1}) {c}" for i, c in enumerate(cols2)) + " |",
              "|---" * (len(cols2) + 1) + "|"]
        for g in RACES + (GW, PG):
            L.append(f"| **{sex}: {g}** |" + " |" * len(cols2))
            for mcol, mlab in [m for m in measures if m[0] != "lyp_fp"]:
                vals = [cell(RES.get((data, "1 grid rank", sex, y, mcol, "35-44", g, "slope"))) for y, _ in rc]
                vals += [cell(RES.get((data, "1 grid rank", sex, "ryf - " + y, mcol, "35-44", g, "slope diff")))
                         for y, _ in rc[1:]]
                if any(vals):
                    L.append(f"| Parent rank: {mlab} | " + " | ".join(vals) + " |")
        L.append("| N children (B; W), parental family income | " + " | ".join(
            n_txt(data, "1 grid rank", sex, y, "lyp", "35-44", stat="slope", ch=False) for y, _ in rc)
                 + " |" * (len(rc) - 1) + " |")
        L.append("")
    return L


KEYS = ("data", "part", "sex", "outcome", "measure", "band", "group", "stat")
NIDX = {}


def nidx():
    if len(NIDX) != len(ROWS):
        NIDX.clear()
        NIDX.update({tuple(z[k] for k in KEYS): z for z in ROWS})
    return NIDX


def n_txt(data, part, sex, y, m, band, stat="IGE", ch=True):
    out = []
    for g in RACES:
        z = nidx().get((data, part, sex, y, m, band, g, stat))
        if z is not None and pd.notna(z.get("n")):
            out.append(f"{g[0]} {int(z['n']):,}" + (f" / {int(z['children']):,}" if ch else ""))
    return "; ".join(out)


# ================================================================ PART 2: by age
def age_block(data, s, ctrlA, bands, sexes, specs, tag, extra_tests=True):
    """child-year band regressions, P1. specs: [(ycol, label)]; records band IGEs, gaps, within-race diffs, tests."""
    for sex, fem in sexes:
        x = s[s["female"] == fem]
        parts = []
        for ycol, _ in specs:
            if ycol not in x:
                continue
            for b in bands + [CH]:
                for g, d, w in by_group(band_rows(x, b)):
                    parts.append(piece(d, (ycol, b, g), ycol, "lyp", w, ["pid", "fam68", "agei", *ctrlA]))
        R = Cells(pd.concat(parts, ignore_index=True), "_y", "_x", "cell", ctrlA, "agei", w="_w")
        ys = [y for y, _ in specs if y in x]
        for y in ys:
            for b in bands + [CH]:
                for g in RACES + (PG,):
                    if R.has((y, b, g)):
                        record((data, tag, sex, y, "lyp", b, g, "IGE"), *R.lin(T(y, g)(b)), **R.info[(y, b, g)])
                if R.has((y, b, "Black")) and R.has((y, b, "White")):
                    record((data, tag, sex, y, "lyp", b, GW, "IGE"), *R.lin(TG(y)(b)))
            for g, term in [(g, T(y, g)) for g in RACES + (PG,)] + [(GW, TG(y))]:
                for k, r in tests(R, bands, term).items():
                    record((data, tag, sex, y, "lyp", "test", g, k), *r[:3], note=str(r[3]) if k == "wald" else "")
        # cross-outcome: first spec minus each other spec
        y0 = ys[0]
        for y in ys[1:]:
            dname = f"{y0} - {y}"
            for g in RACES + (PG,):
                term = TSUB(T(y0, g), T(y, g))
                for b in bands + [CH]:
                    if R.has((y0, b, g)) and R.has((y, b, g)):
                        record((data, tag, sex, dname, "lyp", b, g, "IGE diff"), *R.lin(term(b)))
                for k, r in tests(R, bands, term).items():
                    record((data, tag, sex, dname, "lyp", "test", g, k), *r[:3], note=str(r[3]) if k == "wald" else "")
            term = TSUB(TG(y0), TG(y))
            for b in bands + [CH]:
                if all(R.has((yy, b, gg)) for yy in (y0, y) for gg in RACES):
                    record((data, tag, sex, dname, "lyp", b, GW, "IGE diff"), *R.lin(term(b)))
            for k, r in tests(R, bands, term).items():
                record((data, tag, sex, dname, "lyp", "test", GW, k), *r[:3], note=str(r[3]) if k == "wald" else "")


def rank_age_block(data, r, bands, sexes, ys, tag, xcol="rp_fi"):
    for sex, fem in sexes:
        rr = r[r["female"] == fem]
        parts = []
        for y in ys:
            for b in bands + [CH]:
                for g, d, w in by_group(rr[rr["window"] == b], weight_all="w"):
                    parts.append(piece(d, (y, b, g), y, xcol, w, ["pid", "fam68"]))
        R = Cells(pd.concat(parts, ignore_index=True), "_y", "_x", "cell", [], w="_w")
        for y in ys:
            for b in bands + [CH]:
                for g in RACES + (PG,):
                    if R.has((y, b, g)):
                        record((data, tag, sex, y, xcol, b, g, "slope"), *R.lin(T(y, g)(b)), **R.info[(y, b, g)])
                if R.has((y, b, "Black")):
                    record((data, tag, sex, y, xcol, b, GW, "slope"), *R.lin(TG(y)(b)))
            for g, term in [(g, T(y, g)) for g in RACES + (PG,)] + [(GW, TG(y))]:
                for k, rs in tests(R, bands, term).items():
                    record((data, tag, sex, y, xcol, "test", g, k), *rs[:3], note=str(rs[3]) if k == "wald" else "")
        y0 = ys[0]
        for y in ys[1:]:
            dname = f"{y0} - {y}"
            for g, term in [(g, TSUB(T(y0, g), T(y, g))) for g in RACES + (PG,)] + [(GW, TSUB(TG(y0), TG(y)))]:
                for b in bands + [CH]:
                    try:
                        record((data, tag, sex, dname, xcol, b, g, "slope diff"), *R.lin(term(b)))
                    except KeyError:
                        pass
                for k, rs in tests(R, bands, term).items():
                    record((data, tag, sex, dname, xcol, "test", g, k), *rs[:3], note=str(rs[3]) if k == "wald" else "")


def age_md(data, tag, sex, bands, specs, ndiff=1, xcol="lyp", stat="IGE", dstat="IGE diff", title="", nrow=True):
    """band table: columns = outcomes + (1) minus (k) tests for the next `ndiff` outcomes; panels = bands."""
    y0 = specs[0][0]
    diffs = [(f"{y0} - {y}", f"(1) minus ({i + 2}) (test)") for i, (y, _) in enumerate(specs[1:1 + ndiff])]
    cols = [lab for _, lab in specs] + [lab for _, lab in diffs]
    L = [title, "", "| | " + " | ".join(f"({i + 1}) {c}" for i, c in enumerate(cols)) + " |",
         "|---" * (len(cols) + 1) + "|"]
    for b in bands + [CH]:
        L.append(f"| **Age {b}{' (Chetty window)' if b == CH else ''}** |" + " |" * len(cols))
        for g in RACES + (GW, PG):
            vals = [cell(RES.get((data, tag, sex, y, xcol, b, g, stat))) for y, _ in specs]
            vals += [cell(RES.get((data, tag, sex, d, xcol, b, g, dstat))) for d, _ in diffs]
            L.append(f"| {g} | " + " | ".join(vals) + " |")
        if nrow:
            L.append("| N (B; W) | " + " | ".join(n_txt(data, tag, sex, y, xcol, b, stat=stat) for y, _ in specs)
                     + " |" * len(diffs) + " |")
    L.append(f"| **Tests across bands {bands[0]} ... {bands[-1]}** |" + " |" * len(cols))
    for k, kl in TESTNAMES:
        for g in (GW, "Black", "White", PG):
            vals = [tcell(k, RES.get((data, tag, sex, y, xcol, "test", g, k)) if k != "wald" else
                          wald_from(data, tag, sex, y, xcol, g)) for y, _ in specs]
            vals += [tcell(k, RES.get((data, tag, sex, d, xcol, "test", g, k)) if k != "wald" else
                           wald_from(data, tag, sex, d, xcol, g)) for d, _ in diffs]
            L.append(f"| {kl}: {g} | " + " | ".join(vals) + " |")
    L.append("")
    return L


def wald_from(data, tag, sex, y, xcol, g):
    z = nidx().get((data, tag, sex, y, xcol, "test", g, "wald"))
    return None if z is None else (z["est"], np.nan, z["p"], z.get("note", ""))


# ================================================================ PART 3: decomposition
DEC_LOG = [("lfam_cs", "ln family income (common sample)"), ("d_own", "Own earnings: ln E_own"),
           ("d_sp", "Spouse: ln[(E_own+E_sp)/E_own]"), ("d_oth", "Other income: ln[Y/(E_own+E_sp)]")]
DEC_MAR = [("part_cs", "Partnered (LPM)"), ("d_sp_m", "Spouse term among partnered")]
DEC_FIX = [("lfam_cs", "ln family income (common sample)"), ("lfam_pc", "same, partnered control"),
           ("lfam_m", "within partnered"), ("lfam_s", "within unpartnered")]
DEC_LV = [("lv_fam", "Family income / mean"), ("lv_own", "Own earnings / mean"), ("lv_sp", "Spouse earnings / mean"),
          ("lv_oth", "Other income / mean")]
DEC_LVM = [("lv_part", "Partnered (LPM), level sample"), ("lv_sp_m", "Spouse earnings / mean, partnered")]


def dec_block(s, sexes):
    ys = [y for y, _ in DEC_LOG + DEC_MAR + DEC_FIX[1:] + DEC_LV + DEC_LVM]
    ys = list(dict.fromkeys(ys))
    for sex, fem in sexes:
        x = s[s["female"] == fem]
        for design in ("band", "LS"):
            parts = []
            for y in ys:
                ycol_p = y.replace("lv_", "lvP_") if y.startswith("lv_") else y
                if design == "band":
                    for b in BL + [CH]:
                        xb = band_rows(x, b)
                        for g, d, w in by_group(xb):
                            parts.append(piece(d, (y, b, g), ycol_p if g == PG else y, "lyp", w,
                                               ["pid", "fam68", "agei", *A4], pc=(y == "lfam_pc")))
                else:
                    for g, d, w in by_group(x):
                        parts.append(piece(d, (y, "40", g), ycol_p if g == PG else y, "lyp", w,
                                           ["pid", "fam68", *A4, *C4], ls=True, pc=(y == "lfam_pc")))
            st = pd.concat(parts, ignore_index=True)
            if design == "band":
                R = Cells(st, "_y", "_x", "cell", A4 + ["pc"], "agei", w="_w")
                bands = BL + [CH]
            else:
                R = Cells(st, "_y", "_x", "cell", A4 + C4 + XC4 + ["pc"], w="_w")
                bands = ["40"]
            tag = "3 decomposition" if design == "band" else "3 decomposition LS"
            for y in ys:
                for b in bands:
                    for g in RACES + (PG,):
                        if R.has((y, b, g)):
                            record(("PSID", tag, sex, y, "lyp", b, g, "IGE"), *R.lin(T(y, g)(b)), **R.info[(y, b, g)])
                    if R.has((y, b, "Black")):
                        record(("PSID", tag, sex, y, "lyp", b, GW, "IGE"), *R.lin(TG(y)(b)))
                if design == "band":
                    for g, term in [(g, T(y, g)) for g in RACES + (PG,)] + [(GW, TG(y))]:
                        for k, r in tests(R, BL, term).items():
                            record(("PSID", tag, sex, y, "lyp", "test", g, k), *r[:3],
                                   note=str(r[3]) if k == "wald" else "")
            # identity check
            for b in bands:
                if R.has(("lfam_cs", b, "Black")):
                    e0 = R.lin(T("lfam_cs", "Black")(b))[0]
                    e1 = sum(R.lin(T(y, "Black")(b))[0] for y in ("d_own", "d_sp", "d_oth"))
                    assert abs(e0 - e1) < 1e-8, (sex, b, e0, e1)
            # marriage split of the spouse term: mbar * beta_P + Pbar * beta_s|m (means of the cell, fixed)
            for spt, pt, smt, lab in (("d_sp", "part_cs", "d_sp_m", "log"), ("lv_sp", "lv_part", "lv_sp_m", "level")):
                for b in bands:
                    if not R.has((pt, b, "Black")):
                        continue
                    terms = {}
                    for g in RACES + (PG,):
                        pbar, mbar = R.info[(pt, b, g)]["mean_y"], R.info[(smt, b, g)]["mean_y"]
                        terms[g] = dict(marriage=[((pt, b, g), "x", mbar)], conditional=[((smt, b, g), "x", pbar)])
                        terms[g]["remainder"] = ([((spt, b, g), "x", 1.0)] + neg(terms[g]["marriage"])
                                                 + neg(terms[g]["conditional"]))
                    for comp in ("marriage", "conditional", "remainder"):
                        for g in RACES + (PG,):
                            record(("PSID", tag, sex, f"{lab} spouse: {comp}", "lyp", b, g, "IGE"),
                                   *R.lin(terms[g][comp]))
                        record(("PSID", tag, sex, f"{lab} spouse: {comp}", "lyp", b, GW, "IGE"),
                               *R.lin(terms["White"][comp] + neg(terms["Black"][comp])))
                    if design == "band":
                        pass
                if design == "band":
                    for comp in ("marriage", "conditional"):
                        def term(bb, comp=comp, g=None):
                            out = []
                            for gg, sgn in (("White", 1), ("Black", -1)):
                                pbar = R.info[(pt, bb, gg)]["mean_y"]
                                mbar = R.info[(smt, bb, gg)]["mean_y"]
                                out += ([((pt, bb, gg), "x", sgn * mbar)] if comp == "marriage"
                                        else [((smt, bb, gg), "x", sgn * pbar)])
                            return out
                        for k, r in tests(R, BL, term).items():
                            record(("PSID", tag, sex, f"{lab} spouse: {comp}", "lyp", "test", GW, k), *r[:3],
                                   note=str(r[3]) if k == "wald" else "")
            print(f"  decomposition {sex} {design} done", flush=True)


def dec_md(sex, specs, title, extra_note=""):
    cols = [lab for _, lab in specs]
    L = [title, ""] + ([extra_note, ""] if extra_note else []) + [
        "| | " + " | ".join(f"({i + 1}) {c}" for i, c in enumerate(cols)) + " |", "|---" * (len(cols) + 1) + "|"]
    for tag, b in [("3 decomposition LS", "40")] + [("3 decomposition", b) for b in BL + [CH]]:
        L.append(f"| **{'Lee-Solon IGE at 40' if b == '40' else 'Age ' + b}** |" + " |" * len(cols))
        for g in RACES + (GW, PG):
            L.append(f"| {g} | " + " | ".join(cell(RES.get(("PSID", tag, sex, y, "lyp", b, g, "IGE")))
                                             for y, _ in specs) + " |")
        L.append("| N child-years (B; W) | " + " | ".join(n_txt("PSID", tag, sex, y, "lyp", b, ch=False)
                                                       if not y.startswith(("log spouse", "level spouse")) else ""
                                                       for y, _ in specs) + " |")
    L.append("| **Tests across bands 25-29 ... 50-55** |" + " |" * len(cols))
    for k, kl in TESTNAMES:
        for g in (GW, "Black", "White", PG):
            vals = [tcell(k, RES.get(("PSID", "3 decomposition", sex, y, "lyp", "test", g, k)) if k != "wald" else
                          wald_from("PSID", "3 decomposition", sex, y, "lyp", g)) for y, _ in specs]
            if any(vals):
                L.append(f"| {kl}: {g} | " + " | ".join(vals) + " |")
    L.append("")
    return L


# ================================================================ PART 4: margins
def margins_block(data, s, ctrlA, bands, sexes):
    bm = band_mean_frame(s, ctrlA, bands)
    for sex, fem in sexes:
        x = bm[bm["female"] == fem]
        parts = []
        for y in ("lbm_all", "lbm_pos"):
            for b in bands + [CH]:
                for g, d, w in by_group(x[x["band"] == b]):
                    parts.append(piece(d, (y, b, g), y, "lyp", w, ["pid", "fam68", "agec", *ctrlA]))
        R = Cells(pd.concat(parts, ignore_index=True), "_y", "_x", "cell", ctrlA + ["agec"], w="_w")
        tag = "4 band-mean earnings"
        for y in ("lbm_all", "lbm_pos"):
            for b in bands + [CH]:
                for g in RACES + (PG,):
                    if R.has((y, b, g)):
                        record((data, tag, sex, y, "lyp", b, g, "IGE"), *R.lin(T(y, g)(b)), **R.info[(y, b, g)])
                if R.has((y, b, "Black")):
                    record((data, tag, sex, y, "lyp", b, GW, "IGE"), *R.lin(TG(y)(b)))
            for g, term in [(g, T(y, g)) for g in RACES + (PG,)] + [(GW, TG(y))]:
                for k, r in tests(R, bands, term).items():
                    record((data, tag, sex, y, "lyp", "test", g, k), *r[:3], note=str(r[3]) if k == "wald" else "")
        for g, term in [(g, TSUB(T("lbm_all", g), T("lbm_pos", g))) for g in RACES + (PG,)] + \
                       [(GW, TSUB(TG("lbm_all"), TG("lbm_pos")))]:
            for b in bands + [CH]:
                try:
                    record((data, tag, sex, "lbm_all - lbm_pos", "lyp", b, g, "IGE diff"), *R.lin(term(b)))
                except KeyError:
                    pass
            for k, r in tests(R, bands, term).items():
                record((data, tag, sex, "lbm_all - lbm_pos", "lyp", "test", g, k), *r[:3],
                       note=str(r[3]) if k == "wald" else "")


def zero_shares(s, sexes, bands):
    L = ["| Band | " + " | ".join(f"{sx} {g}" for sx, _ in sexes for g in RACES) + " |",
         "|---" * (1 + 2 * len(sexes)) + "|"]
    for b in bands:
        vals = []
        for sx, fem in sexes:
            for g in RACES:
                d = s[(s["female"] == fem) & (s["race"] == g) & (s["band"] == b) & s["emp"].notna()]
                vals.append(f"{1 - d['emp'].mean():.3f}" if len(d) else "")
        L.append(f"| {b} | " + " | ".join(vals) + " |")
    return L


# ================================================================ NLSY frames
def nlsy79():
    s, n, hw = ige26.nlsy_frames()
    s = s.copy()
    s["C"] = s["age"] - 40
    for k in range(1, 5):
        s[f"C{k}"] = (s["C"] / 10) ** k
    s["emp"] = (s["earn"] >= LO).astype(float).where(s["earn"].notna())
    both = s["lfam"].notna() & s["learn"].notna()
    s["lfam_c"], s["learn_c"] = s["lfam"].where(both), s["learn"].where(both)
    r = ige26.nlsy_rank_frame(n, hw)
    r = ige26.add_child_ranks(r).rename(columns={"band": "window"})
    r["rp_fi"] = r["rp"]
    return s, r


def nlsy97():
    k, L = ige29.load_extract(False)
    s, _, r = ige29.nlsy97_frames(k, L)
    s = s.copy()
    s["C"] = s["age"] - 40
    for j in range(1, 5):
        s[f"C{j}"] = (s["C"] / 10) ** j
    s["emp"] = (s["earn"] >= LO).astype(float).where(s["earn"].notna())
    both = s["lfam"].notna() & s["learn"].notna()
    s["lfam_c"], s["learn_c"] = s["lfam"].where(both), s["learn"].where(both)
    # add Chetty window to the rank frame
    q = L[L["age"].between(31, 37)]
    kr = r[r["band"] == BL[0]].set_index("pid")[["birth_year", "w", "rp", "race", "female", "fam68", "pinc"]].copy()
    f = q.dropna(subset=["faminc"]).groupby("pid")["faminc"].agg(["mean", "count"])
    e = q.dropna(subset=["earn"]).groupby("pid")["earn"].agg(["mean", "count"])
    kr["yf"] = f.loc[f["count"] >= 2, "mean"].reindex(kr.index)
    kr["ye"] = e.loc[e["count"] >= 2, "mean"].reindex(kr.index)
    kr["band"] = CH
    r = pd.concat([r, kr.reset_index()], ignore_index=True)
    r = ige26.add_child_ranks(r).rename(columns={"band": "window"})
    r["rp_fi"] = r["rp"]
    return s, r


def nlsy_ls(data, s, ctrlA, ages, sexes):
    for sex, fem in sexes:
        x = s[s["female"] == fem]
        parts = []
        ys = [y for y in ("lfam", "learn", "emp", "lfam_c", "learn_c", "partnered") if y in x]
        for y in ys:
            for g, d, w in by_group(x):
                parts.append(piece(d, (y, g), y, "lyp", w, ["pid", "fam68", *ctrlA, *C4], ls=True))
        R = Cells(pd.concat(parts, ignore_index=True), "_y", "_x", "cell", ctrlA + C4 + XC4, w="_w")
        for a in ages:
            z = (a - 40) / 10

            def at(y, g):
                return [((y, g), "x", 1.0)] + [((y, g), f"xC{n}", z ** n) for n in range(1, 5)]
            for y in ys:
                for g in RACES + (PG,):
                    record((data, "5 LS", sex, y, "lyp", str(a), g, "IGE"), *R.lin(at(y, g)), **R.info[(y, g)])
                record((data, "5 LS", sex, y, "lyp", str(a), GW, "IGE"), *R.lin(at(y, "White") + neg(at(y, "Black"))))
            for y0, y1 in (("lfam", "learn"), ("lfam_c", "learn_c")):
                for g in RACES + (PG,):
                    record((data, "5 LS", sex, f"{y0} - {y1}", "lyp", str(a), g, "IGE diff"),
                           *R.lin(at(y0, g) + neg(at(y1, g))))
                record((data, "5 LS", sex, f"{y0} - {y1}", "lyp", str(a), GW, "IGE diff"),
                       *R.lin(at(y0, "White") + neg(at(y0, "Black")) + neg(at(y1, "White")) + at(y1, "Black")))


# ================================================================ output helpers
def g(*key):
    return RES.get(key)


def figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ink, c_own, c_sp, c_oth = "#0b0b0b", "#2a78d6", "#eb6834", "#1baf7a"
    fig, axes = plt.subplots(2, 2, figsize=(12, 9), sharex=True)
    xs = np.array([MID[b] for b in BL])
    for j, (sex, _) in enumerate(SEXES):
        ax = axes[0, j]
        for y, lab, col, off in (("lfam", "Family income", ink, -0.5), ("learn", "Own earnings (>0)", c_own, 0.5)):
            rr = [g("PSID", "2 age", sex, y, "lyp", b, GW, "IGE") for b in BL]
            ax.errorbar(xs + off, [r[0] for r in rr], yerr=[1.96 * r[1] for r in rr], color=col, lw=2, marker="o",
                        ms=7, capsize=0, elinewidth=1.2, label=lab)
        ax.axhline(0, color="#bbbbbb", lw=0.8)
        ax.set_title(f"PSID {sex.lower()}: White - Black gap in the log IGE", fontsize=11)
        ax.legend(frameon=False, fontsize=9, loc="upper left")
        ax = axes[1, j]
        comps = [("d_own", "Own earnings", c_own), ("d_sp", "Spouse (incl. marriage)", c_sp),
                 ("d_oth", "Other income", c_oth)]
        pos, negb = np.zeros(len(BL)), np.zeros(len(BL))
        for y, lab, col in comps:
            v = np.array([g("PSID", "3 decomposition", sex, y, "lyp", b, GW, "IGE")[0] for b in BL])
            bottom = np.where(v >= 0, pos, negb)
            ax.bar(xs, v, width=3.4, bottom=bottom, color=col, edgecolor="white", linewidth=2, label=lab)
            pos, negb = pos + np.clip(v, 0, None), negb + np.clip(v, None, 0)
        tot = [g("PSID", "3 decomposition", sex, "lfam_cs", "lyp", b, GW, "IGE") for b in BL]
        ax.errorbar(xs, [r[0] for r in tot], yerr=[1.96 * r[1] for r in tot], color=ink, marker="D", ms=6, lw=0,
                    elinewidth=1.2, label="Total (family income, common sample)")
        ax.axhline(0, color="#bbbbbb", lw=0.8)
        ax.set_title(f"PSID {sex.lower()}: channels of the family-income IGE gap", fontsize=11)
        ax.set_xlabel("Child's age (band midpoint)")
        ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    for ax in axes.ravel():
        ax.set_axisbelow(True)
        ax.grid(axis="y", color="#e5e5e5", lw=0.6)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    fig.text(0.5, 0.005, "Top: White - Black difference in band log IGEs (parental family income, 13-19 mean), 95% CI, "
             "s.e. clustered by 1968 family. Bottom: exact split ln Y = ln E_own + ln[(E_own+E_sp)/E_own] + "
             "ln[Y/(E_own+E_sp)] on child-years with positive own earnings.", ha="center", fontsize=8.5,
             color="#52514e", wrap=True)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(OUT / "income_vs_earnings_ige.png", dpi=150)


# ================================================================ main
def main():
    s, P = psid_frames()
    print("PSID frames built", flush=True)
    r = psid_rank_frame(s, P)
    print("PSID rank frame built", flush=True)
    # 1 grid
    grid_block("PSID", s, r, A4, MEAS, GRID_Y, SEXES)
    print("grid done", flush=True)
    # 2 by age (25-55)
    sa = s[s["age"].between(25, 55)].copy()
    age_block("PSID", sa, A4, BL, SEXES, [("lfam", FAM), ("learn", ERN), ("emp", "Employed")], "2 age")
    age_block("PSID", sa, A4, BL, SEXES, [("lfam_c", FAM + ", common"), ("learn_c", ERN + ", common")], "2 age common")
    age_block("PSID", sa, A4, BL, SEXES, [("lfam", FAM), ("lcpl", "ln couple earnings"), ("lsp", "ln spouse earnings")],
              "2 age couple")
    rank_age_block("PSID", r, BL, SEXES, ["ryf", "rye", "ryep", "rycp"], "2 rank age")
    print("age blocks done", flush=True)
    # 3 decomposition
    dec_block(s, SEXES)
    # 4 margins
    margins_block("PSID", sa, A4, BL, SEXES)
    print("PSID margins done", flush=True)
    # 5 NLSY
    s79, r79 = nlsy79()
    nlsy_ls("NLSY79", s79, A4, (35, 40, 45), SEXES)
    age_block("NLSY79", s79, A4, BL, SEXES, [("lfam", FAM), ("learn", ERN), ("emp", "Employed")], "2 age")
    age_block("NLSY79", s79, A4, BL, SEXES, [("lfam_c", FAM + ", common"), ("learn_c", ERN + ", common")],
              "2 age common")
    rank_age_block("NLSY79", r79, BL, SEXES, ["ryf", "rye"], "2 rank age")
    print("NLSY79 done", flush=True)
    s97, r97 = nlsy97()
    b97 = BL[:4]
    ctrl97 = A4 + ["Amiss"]
    nlsy_ls("NLSY97", s97, ctrl97, (30, 35, 40), SEXES)
    age_block("NLSY97", s97, ctrl97, b97, SEXES, [("lfam", FAM), ("learn", ERN), ("emp", "Employed")], "2 age")
    age_block("NLSY97", s97, ctrl97, b97, SEXES, [("lfam_c", FAM + ", common"), ("learn_c", ERN + ", common")],
              "2 age common")
    rank_age_block("NLSY97", r97, b97, SEXES, ["ryf", "rye"], "2 rank age")
    print("NLSY97 done", flush=True)

    EXTRA["zeros_psid"] = zero_shares(sa, SEXES, BL)
    EXTRA["zeros_79"] = zero_shares(s79, SEXES, BL)
    EXTRA["zeros_97"] = zero_shares(s97, SEXES, b97)
    EXTRA["means"] = sample_means(s)
    OUT.mkdir(exist_ok=True)
    pd.DataFrame(ROWS).to_csv(OUT / "income_vs_earnings_ige.csv", index=False)
    pd.to_pickle((ROWS, RES, EXTRA), CACHE)
    write_md()
    figure()
    print("written", flush=True)


EXTRA = {}
CACHE = DATA / "income_vs_earnings_cache.pkl"


def sample_means(s):
    """mean shares of components by sex x race x band (level sample), and partnered share."""
    out = []
    for sex, fem in SEXES:
        for g in RACES:
            for b in BL:
                d = s[(s["female"] == fem) & (s["race"] == g) & (s["band"] == b) & s["lv"]]
                out.append(dict(sex=sex, race=g, band=b, partnered=d["partnered"].mean(),
                                own=d["own"].sum() / d["faminc"].sum(), sp=d["sp"].sum() / d["faminc"].sum(),
                                oth=d["other"].sum() / d["faminc"].sum(), faminc=d["faminc"].mean(), n=len(d)))
    return pd.DataFrame(out)


def c(*key):
    return cell(RES.get(key))


def est(*key):
    r = RES.get(key)
    return np.nan if r is None else r[0]


def headline_table():
    cols = [FAM, ERN, f"(1) minus (2) (test)"]
    L = ["| | " + " | ".join(f"({i + 1}) {x}" for i, x in enumerate(cols)) + " |", "|---" * 4 + "|"]
    for data, at in (("PSID", "40"), ("NLSY79", "40"), ("NLSY97", "35")):
        for sex, _ in SEXES:
            L.append(f"| **{data} {sex.lower()}** | | | |")
            for g in RACES + (GW, PG):
                if data == "PSID":
                    vals = [c(data, "1 grid log", sex, y, "lyp", "40", g, "IGE") for y in ("lfam", "learn")]
                    vals.append(c(data, "1 grid log", sex, "lfam - learn", "lyp", "40", g, "IGE diff"))
                else:
                    vals = [c(data, "5 LS", sex, y, "lyp", at, g, "IGE") for y in ("lfam", "learn")]
                    vals.append(c(data, "5 LS", sex, "lfam - learn", "lyp", at, g, "IGE diff"))
                L.append(f"| Lee-Solon IGE at {at}: {g} | " + " | ".join(vals) + " |")
            for g in (GW, "Black", "White", PG):
                vals = [c(data, "2 age", sex, y, "lyp", "test", g, "change") for y in ("lfam", "learn", "lfam - learn")]
                L.append(f"| Change, mean of bands >= 35 minus < 35: {g} | " + " | ".join(vals) + " |")
    return L


def write_md():
    L = ["# Family-income IGE vs earnings IGE: by race, sex and age, and why they differ", "",
         "Generated by `34.IncomeVsEarningsIGE.py` (2026-10-17); full definitions in its docstring; every estimate in "
         "`output/income_vs_earnings_ige.csv`. Every cell: coefficient (s.e.; p-value), *** p<0.01, ** p<0.05, "
         "* p<0.1. S.e. clustered by 1968 family (NLSY: first-round household). Within each table every cell is its "
         "own regression and the joint covariance is that of the stacked, fully interacted regression, so the "
         "'(1) minus (k)' columns (same children, two outcomes), the White - Black rows and the tests across bands "
         "are valid tests. Race = parental household head's race; Black / White log IGEs unweighted (as "
         "`6.IGEMain.py`), Pooled = all races weighted (child-year core longitudinal weight); ranks weighted "
         "throughout. 'Mean >= 35 minus < 35' = mean over the bands 35-39 ... 50-55 minus the mean over 25-29 and "
         "30-34 (NLSY97: 35-39, 40-44 vs 25-29, 30-34). Own earnings in logs are positive years only; ranks and "
         "band means keep zeros. Lee-Solon s.e. here are clustered by 1968 family (6.IGEMain.py clusters by child), "
         "so they are slightly larger than in `ige_main.md`; the point estimates are identical.", ""]

    # ---------------- headline
    def gpct(num, den):
        return f"{100 * num / den:.0f}%" if np.isfinite(num) and np.isfinite(den) and abs(den) > 1e-9 else "n/a"
    ds = ("PSID", "3 decomposition LS", "Daughters")
    ss = ("PSID", "3 decomposition LS", "Sons")
    dch = ("PSID", "3 decomposition", "Daughters")
    sch = ("PSID", "3 decomposition", "Sons")
    L += ["## 0. Headline", "",
          "**Answer to the PI.** For SONS the family-income IGE and the own-earnings IGE are close within each race "
          "(differences of 0.00-0.05 log points at 40, in all three data sets), so the racial gap is about as large "
          "in earnings as in family income; with age the sons' EARNINGS gap opens somewhat faster, because other "
          "income (transfers, other household members) and, a little, the spouse cushion Black sons' family income "
          "relative to their earnings. For DAUGHTERS the two differ a lot, and the difference is racial and grows "
          "with age: White daughters' family income is far more persistent than their own earnings, Black daughters' "
          "is not, and the gap that opens after 30 in daughters' family income is a gap in their husbands' earnings "
          "given marriage (roughly 55-65% of the spouse channel) and in marriage itself (35-45%), not in their own "
          "earnings.", "",
          f"- **Sons at 40 (PSID, Lee-Solon).** Family income: Black "
          f"{c('PSID', '1 grid log', 'Sons', 'lfam', 'lyp', '40', 'Black', 'IGE')}, White "
          f"{c('PSID', '1 grid log', 'Sons', 'lfam', 'lyp', '40', 'White', 'IGE')}, gap "
          f"{c('PSID', '1 grid log', 'Sons', 'lfam', 'lyp', '40', GW, 'IGE')}. Own earnings: Black "
          f"{c('PSID', '1 grid log', 'Sons', 'learn', 'lyp', '40', 'Black', 'IGE')}, White "
          f"{c('PSID', '1 grid log', 'Sons', 'learn', 'lyp', '40', 'White', 'IGE')}, gap "
          f"{c('PSID', '1 grid log', 'Sons', 'learn', 'lyp', '40', GW, 'IGE')}. Family minus earnings IGE: Black "
          f"{c('PSID', '1 grid log', 'Sons', 'lfam - learn', 'lyp', '40', 'Black', 'IGE diff')}, White "
          f"{c('PSID', '1 grid log', 'Sons', 'lfam - learn', 'lyp', '40', 'White', 'IGE diff')}; difference in the "
          f"racial gap {c('PSID', '1 grid log', 'Sons', 'lfam - learn', 'lyp', '40', GW, 'IGE diff')}.",
          f"- **Daughters at 40.** Family income: Black "
          f"{c('PSID', '1 grid log', 'Daughters', 'lfam', 'lyp', '40', 'Black', 'IGE')}, White "
          f"{c('PSID', '1 grid log', 'Daughters', 'lfam', 'lyp', '40', 'White', 'IGE')}, gap "
          f"{c('PSID', '1 grid log', 'Daughters', 'lfam', 'lyp', '40', GW, 'IGE')}. Own earnings: Black "
          f"{c('PSID', '1 grid log', 'Daughters', 'learn', 'lyp', '40', 'Black', 'IGE')}, White "
          f"{c('PSID', '1 grid log', 'Daughters', 'learn', 'lyp', '40', 'White', 'IGE')}, gap "
          f"{c('PSID', '1 grid log', 'Daughters', 'learn', 'lyp', '40', GW, 'IGE')}. Family minus earnings: White "
          f"{c('PSID', '1 grid log', 'Daughters', 'lfam - learn', 'lyp', '40', 'White', 'IGE diff')}, Black "
          f"{c('PSID', '1 grid log', 'Daughters', 'lfam - learn', 'lyp', '40', 'Black', 'IGE diff')}; difference "
          f"in the racial gap {c('PSID', '1 grid log', 'Daughters', 'lfam - learn', 'lyp', '40', GW, 'IGE diff')}. "
          f"Their husbands' earnings: Black {c('PSID', '1 grid log', 'Daughters', 'lsp', 'lyp', '40', 'Black', 'IGE')}"
          f", White {c('PSID', '1 grid log', 'Daughters', 'lsp', 'lyp', '40', 'White', 'IGE')} (gap "
          f"{c('PSID', '1 grid log', 'Daughters', 'lsp', 'lyp', '40', GW, 'IGE')}).",
          f"- **By age (PSID bands).** Sons: the gap in the family-income IGE goes "
          f"{est('PSID', '2 age', 'Sons', 'lfam', 'lyp', '25-29', GW, 'IGE'):.3f} (25-29) -> "
          f"{est('PSID', '2 age', 'Sons', 'lfam', 'lyp', '40-44', GW, 'IGE'):.3f} (40-44), in own earnings "
          f"{est('PSID', '2 age', 'Sons', 'learn', 'lyp', '25-29', GW, 'IGE'):.3f} -> "
          f"{est('PSID', '2 age', 'Sons', 'learn', 'lyp', '40-44', GW, 'IGE'):.3f}; the change (>= 35 minus < 35) "
          f"is {c('PSID', '2 age', 'Sons', 'lfam', 'lyp', 'test', GW, 'change')} vs "
          f"{c('PSID', '2 age', 'Sons', 'learn', 'lyp', 'test', GW, 'change')}, difference "
          f"{c('PSID', '2 age', 'Sons', 'lfam - learn', 'lyp', 'test', GW, 'change')} (common child-years: "
          f"{c('PSID', '2 age common', 'Sons', 'lfam_c - learn_c', 'lyp', 'test', GW, 'change')}). Daughters: family "
          f"income gap {est('PSID', '2 age', 'Daughters', 'lfam', 'lyp', '25-29', GW, 'IGE'):.3f} -> "
          f"{est('PSID', '2 age', 'Daughters', 'lfam', 'lyp', '50-55', GW, 'IGE'):.3f} (50-55), change "
          f"{c('PSID', '2 age', 'Daughters', 'lfam', 'lyp', 'test', GW, 'change')}; own earnings change "
          f"{c('PSID', '2 age', 'Daughters', 'learn', 'lyp', 'test', GW, 'change')}; difference "
          f"{c('PSID', '2 age', 'Daughters', 'lfam - learn', 'lyp', 'test', GW, 'change')}, trend of the difference "
          f"{c('PSID', '2 age', 'Daughters', 'lfam - learn', 'lyp', 'test', GW, 'trend')} per 10 years.",
          f"- **Channels (exact log split, common sample).** Daughters at 40: gap "
          f"{c(*ds, 'lfam_cs', 'lyp', '40', GW, 'IGE')} = own earnings {c(*ds, 'd_own', 'lyp', '40', GW, 'IGE')} + "
          f"spouse {c(*ds, 'd_sp', 'lyp', '40', GW, 'IGE')} + other income {c(*ds, 'd_oth', 'lyp', '40', GW, 'IGE')}"
          f" (spouse = {gpct(est(*ds, 'd_sp', 'lyp', '40', GW, 'IGE'), est(*ds, 'lfam_cs', 'lyp', '40', GW, 'IGE'))}"
          f"). Rise with age (>= 35 minus < 35): {c(*dch, 'lfam_cs', 'lyp', 'test', GW, 'change')} = own "
          f"{c(*dch, 'd_own', 'lyp', 'test', GW, 'change')} + spouse {c(*dch, 'd_sp', 'lyp', 'test', GW, 'change')} "
          f"+ other {c(*dch, 'd_oth', 'lyp', 'test', GW, 'change')}; the spouse part splits into marriage "
          f"{c(*dch, 'log spouse: marriage', 'lyp', 'test', GW, 'change')} and the husband's earnings given "
          f"marriage {c(*dch, 'log spouse: conditional', 'lyp', 'test', GW, 'change')}. Sons at 40: gap "
          f"{c(*ss, 'lfam_cs', 'lyp', '40', GW, 'IGE')} = own {c(*ss, 'd_own', 'lyp', '40', GW, 'IGE')} + spouse "
          f"{c(*ss, 'd_sp', 'lyp', '40', GW, 'IGE')} + other {c(*ss, 'd_oth', 'lyp', '40', GW, 'IGE')}; rise "
          f"{c(*sch, 'lfam_cs', 'lyp', 'test', GW, 'change')} = own {c(*sch, 'd_own', 'lyp', 'test', GW, 'change')} "
          f"+ spouse {c(*sch, 'd_sp', 'lyp', 'test', GW, 'change')} + other "
          f"{c(*sch, 'd_oth', 'lyp', 'test', GW, 'change')}. The order-free LEVEL split agrees (Section 3d).",
          f"- **Marriage timing.** At 25-29, White children from richer families are less often partnered (gradient "
          f"of partnered in ln parental income, common sample: White daughters "
          f"{c(*dch, 'part_cs', 'lyp', '25-29', 'White', 'IGE')}, White sons "
          f"{c(*sch, 'part_cs', 'lyp', '25-29', 'White', 'IGE')}; Black daughters "
          f"{c(*dch, 'part_cs', 'lyp', '25-29', 'Black', 'IGE')}, Black sons "
          f"{c(*sch, 'part_cs', 'lyp', '25-29', 'Black', 'IGE')}); by 35-39 the White gradients are "
          f"{c(*dch, 'part_cs', 'lyp', '35-39', 'White', 'IGE')} and {c(*sch, 'part_cs', 'lyp', '35-39', 'White', 'IGE')}"
          f". Later marriage of advantaged White children holds down their family-income IGE in the late twenties "
          f"(daughters' spouse channel gap at 25-29: {c(*dch, 'd_sp', 'lyp', '25-29', GW, 'IGE')}), which is part of "
          f"why the racial gap in family income starts near zero.",
          f"- **Parental measure.** With parents' labor income instead of total family income, the sons' racial gap "
          f"at 40 shrinks in family income ({c('PSID', '1 grid log', 'Sons', 'lfam', 'lypl', '40', GW, 'IGE')}) but "
          f"not in earnings ({c('PSID', '1 grid log', 'Sons', 'learn', 'lypl', '40', GW, 'IGE')}); with the father's "
          f"earnings (father-present sons): {c('PSID', '1 grid log', 'Sons', 'lfam', 'lyfe', '40', GW, 'IGE')} vs "
          f"{c('PSID', '1 grid log', 'Sons', 'learn', 'lyfe', '40', GW, 'IGE')}. Black sons' family income is more "
          f"tied to parental labor income than their earnings are "
          f"({c('PSID', '1 grid log', 'Sons', 'lfam - learn', 'lypl', '40', 'Black', 'IGE diff')}), White sons' is "
          f"not ({c('PSID', '1 grid log', 'Sons', 'lfam - learn', 'lypl', '40', 'White', 'IGE diff')}). The "
          f"earnings gap is robust to the parental measure; the family-income gap is not (EVIDENCE 1.31).",
          f"- **General (pooled) findings.** Sons: family-income and earnings IGEs differ by at most ~0.05 at any age "
          f"(pooled difference at 40 {c('PSID', '1 grid log', 'Sons', 'lfam - learn', 'lyp', '40', PG, 'IGE diff')}; "
          f"largest at 30-34, {c('PSID', '2 age', 'Sons', 'lfam - learn', 'lyp', '30-34', PG, 'IGE diff')}); both rise "
          f"with age. Daughters: the family-income IGE exceeds the earnings IGE by "
          f"{c('PSID', '1 grid log', 'Daughters', 'lfam - learn', 'lyp', '40', PG, 'IGE diff')} at 40 and the "
          f"difference grows from {est('PSID', '2 age', 'Daughters', 'lfam - learn', 'lyp', '25-29', PG, 'IGE diff'):.3f}"
          f" at 25-29 to {est('PSID', '2 age', 'Daughters', 'lfam - learn', 'lyp', '50-55', PG, 'IGE diff'):.3f} at "
          f"50-55, because the family-income IGE rises while the White daughters' own-earnings IGE FALLS after 30 "
          f"(change {c('PSID', '2 age', 'Daughters', 'learn', 'lyp', 'test', 'White', 'change')}). Assortative "
          f"mating is strong: the elasticity of a daughter's husband's earnings to her parents' income at 40 is "
          f"{c('PSID', '1 grid log', 'Daughters', 'lsp', 'lyp', '40', PG, 'IGE')}, larger than of her own earnings "
          f"({c('PSID', '1 grid log', 'Daughters', 'learn', 'lyp', '40', PG, 'IGE')}); sons' wives: "
          f"{c('PSID', '1 grid log', 'Sons', 'lsp', 'lyp', '40', PG, 'IGE')}, and it declines with the son's age "
          f"({est('PSID', '2 age couple', 'Sons', 'lsp', 'lyp', '25-29', PG, 'IGE'):.3f} at 25-29, "
          f"{est('PSID', '2 age couple', 'Sons', 'lsp', 'lyp', '45-49', PG, 'IGE'):.3f} at 45-49). Couple earnings "
          f"carry essentially all of family-income persistence (family minus couple-earnings IGE at 40: sons "
          f"{c('PSID', '1 grid log', 'Sons', 'lfam - lcpl', 'lyp', '40', PG, 'IGE diff')}, daughters "
          f"{c('PSID', '1 grid log', 'Daughters', 'lfam - lcpl', 'lyp', '40', PG, 'IGE diff')}).",
          f"- **Zeros.** Employment gradients are small (sons pooled "
          f"{c('PSID', '1 grid log', 'Sons', 'emp', 'lyp', '40', PG, 'IGE')} per log point at 40) and do not differ by "
          f"race for sons; Black daughters' employment is MORE tied to parental income than White daughters' at 30-39 "
          f"(gap at 35-39 {c('PSID', '2 age', 'Daughters', 'emp', 'lyp', '35-39', GW, 'IGE')}). Keeping zero years "
          f"in the sons' band-mean earnings makes the opening of the racial gap, if anything, larger "
          f"({c('PSID', '4 band-mean earnings', 'Sons', 'lbm_all', 'lyp', 'test', GW, 'change')} with zeros vs "
          f"{c('PSID', '4 band-mean earnings', 'Sons', 'lbm_pos', 'lyp', 'test', GW, 'change')} without; difference "
          f"{c('PSID', '4 band-mean earnings', 'Sons', 'lbm_all - lbm_pos', 'lyp', 'test', GW, 'change')}).",
          f"- **Ranks.** National rank-rank slopes show the same SEX pattern (pooled, 35-44: sons family "
          f"{c('PSID', '1 grid rank', 'Sons', 'ryf', 'lyp', '35-44', PG, 'slope')} vs earnings "
          f"{c('PSID', '1 grid rank', 'Sons', 'rye', 'lyp', '35-44', PG, 'slope')}; daughters "
          f"{c('PSID', '1 grid rank', 'Daughters', 'ryf', 'lyp', '35-44', PG, 'slope')} vs "
          f"{c('PSID', '1 grid rank', 'Daughters', 'rye', 'lyp', '35-44', PG, 'slope')}) and the daughters' racial "
          f"difference (ryf - rye gap {c('PSID', '1 grid rank', 'Daughters', 'ryf - rye', 'lyp', '35-44', GW, 'slope diff')}"
          f"), but no racial divergence with age for sons in either outcome (Paper B: ranks are flat by race).",
          f"- **NLSY replication.** Sons' family-income and earnings IGEs are close in both NLSYs (family minus "
          f"earnings, White sons, NLSY79 at 40: {c('NLSY79', '5 LS', 'Sons', 'lfam - learn', 'lyp', '40', 'White', 'IGE diff')}; NLSY97 at "
          f"35: {c('NLSY97', '5 LS', 'Sons', 'lfam - learn', 'lyp', '35', 'White', 'IGE diff')}). Daughters' "
          f"family-income IGE exceeds their earnings IGE and increasingly so with age (pooled change of the "
          f"difference: NLSY79 {c('NLSY79', '2 age', 'Daughters', 'lfam - learn', 'lyp', 'test', PG, 'change')}, "
          f"NLSY97 {c('NLSY97', '2 age', 'Daughters', 'lfam - learn', 'lyp', 'test', PG, 'change')}); the racial "
          f"difference in it opens with age in the NLSY97 "
          f"({c('NLSY97', '2 age', 'Daughters', 'lfam - learn', 'lyp', 'test', GW, 'change')}) and, not "
          f"significantly, in the NLSY79 ({c('NLSY79', '2 age', 'Daughters', 'lfam - learn', 'lyp', 'test', GW, 'change')}).",
          "", "### Headline table", "",
          "One regression per column (outcome in the header); column (3) is the test of (1) minus (2) on the same "
          "children. Parental measure: family income (PSID mean at 13-19; NLSY79 1978-80; NLSY97 1996). NLSY97 "
          "children are observed only to 44, so its Lee-Solon IGE is evaluated at 35.", ""]
    L += headline_table() + [""]

    # ---------------- 1 grid
    L += ["## 1. The grid at 40: child outcome x parental measure (PSID)", "",
          "Each cell is a separate regression of the column outcome on the row's ln parental measure (Lee-Solon: "
          "child-years 25-65, quartics in parental age and (age-40), parental measure x age quartic; IGE at 40). "
          "Parental measures are means over child ages 13-19 (>= 3 years). Father-present = male head at 16; the "
          "'father-present' row repeats the benchmark on that sample so rows 2 and 3 compare like with like. Spouse "
          "earnings: partnered child-years with the spouse's earnings > 0. Columns (5)-(7) test family income minus "
          "the other outcome, same parental measure, same children. N rows: child-years / children for the "
          "benchmark parental measure and for the father's-earnings measure.", ""]
    L += grid_md("PSID", MEAS, GRID_Y, SEXES)
    L += ["Employment and partnership at 40 (LPM on ln parental measure, Lee-Solon design):", "",
          "| | (1) Employed (own earnings > $100 of 1967) | (2) Partnered |", "|---|---|---|"]
    for sex, _ in SEXES:
        L.append(f"| **{sex}** | | |")
        for mcol, mlab in MEAS:
            for g in RACES + (GW, PG):
                L.append(f"| {mlab}: {g} | " + " | ".join(c("PSID", "1 grid log", sex, y, mcol, "40", g, "IGE")
                                                         for y in ("emp", "partnered")) + " |")
    L.append("")

    # ---------------- 2 by age
    L += ["## 2. By age (PSID): family income vs own earnings", "",
          "Child-year regressions within each band: ln y on ln parental family income (13-19 mean), quartic in "
          "parental age, single-year age dummies. Column (4) is test (a): family-income IGE minus earnings IGE "
          "within race (rows Black, White, Pooled) and test (b): the racial gap in the family-income IGE minus "
          "the racial gap in the earnings IGE (row White - Black). The test rows of column (4) are test (c): does the "
          "age slope of the gap differ between the two outcomes. Column (3), employment, is an LPM (Section 4).", ""]
    for sex, _ in SEXES:
        L += age_md("PSID", "2 age", sex, BL, [("lfam", FAM), ("learn", ERN), ("emp", "Employed (LPM)")], ndiff=1,
                    title=f"### 2a. PSID {sex}: family income vs own earnings, own samples")
    L += ["### 2b. Same children: child-years with both family income and positive own earnings", "",
          "Same design on the common child-years, so the comparison cannot come from who has positive earnings.", ""]
    for sex, _ in SEXES:
        L += age_md("PSID", "2 age common", sex, BL, [("lfam_c", FAM), ("learn_c", ERN)], ndiff=1,
                    title=f"#### PSID {sex}, common child-years")
    L += ["### 2c. Household labor earnings and the spouse", "",
          "ln couple earnings = ln(own + spouse earnings), all child-years with a positive sum; ln spouse earnings: "
          "partnered child-years with positive spouse earnings (assortative mating, Chadwick-Solon). (1) minus (2) "
          "measures how much other income adds to persistence; (1) minus (3) compares the child's family income "
          "with the spouse's earnings.", ""]
    for sex, _ in SEXES:
        L += age_md("PSID", "2 age couple", sex, BL, [("lfam", FAM), ("lcpl", "ln couple earnings"),
                                                       ("lsp", "ln spouse's earnings (>0, partnered)")], ndiff=2,
                    title=f"#### PSID {sex}: family income, couple earnings, spouse earnings")
    L += ["### 2d. Ranks by age (PSID)", "",
          "Rank-rank slopes: band means (>= 2 years) of the child's outcome ranked within birth year and band among "
          "all children; parent rank = parental family income (13-19 mean) within birth year; weighted. Own earnings "
          "rank (2) keeps zero years in the band mean; (3) averages positive years only (>= 2).", ""]
    for sex, _ in SEXES:
        L += age_md("PSID", "2 rank age", sex, BL, [("ryf", "Rank of family income"),
                                                     ("rye", "Rank of own earnings (zeros kept)"),
                                                     ("ryep", "Rank of own earnings (positive years)"),
                                                     ("rycp", "Rank of couple earnings")],
                    ndiff=3, xcol="rp_fi", stat="slope", dstat="slope diff",
                    title=f"#### PSID {sex}: rank-rank slopes by band")

    # ---------------- 3 decomposition
    L += ["## 3. Why they differ: channels of the family-income IGE (PSID)", "",
          "Common sample: child-years with family income in bounds, positive own earnings and known spouse earnings "
          "(0 if unpartnered). ln Y = ln E_own + ln[(E_own+E_sp)/E_own] + ln[Y/(E_own+E_sp)], so column (1) = "
          "(2) + (3) + (4) exactly in every row (checked in the code). Rows 'Lee-Solon IGE at 40' use the age-"
          "interacted design on child-years 25-65; band rows the child-year band design. Note that the split is "
          "sequential (own earnings first): a child who earns more has a smaller spouse term for the same spouse; "
          "the level split in 3d has no ordering.", ""]
    for sex, _ in SEXES:
        L += dec_md(sex, DEC_LOG, f"### 3a. {sex}: exact log split of the family-income IGE")
    L += ["### 3b. Marriage vs the spouse's earnings given marriage", "",
          "The spouse term s = ln[(E_own+E_sp)/E_own] is 0 for unpartnered child-years, so beta_s = d E[s]/d ln y_p "
          "~ mean(s | partnered) x beta_partnered + share partnered x beta_(s | partnered). (1) partnered LPM; (2) "
          "spouse term among the partnered; (3) marriage part = mean(s|m) x (1); (4) conditional part = share "
          "partnered x (2); (5) remainder = beta_s - (3) - (4) (means treated as fixed). (3)-(5) are linear "
          "combinations, not separate regressions.", ""]
    for sex, _ in SEXES:
        L += dec_md(sex, DEC_MAR + [("log spouse: marriage", "Marriage part"),
                                    ("log spouse: conditional", "Spouse's earnings given marriage"),
                                    ("log spouse: remainder", "Remainder")],
                    f"#### {sex}: marriage split of the spouse channel (log)")
    L += ["### 3c. Holding marital status fixed", "",
          "ln family income on the common sample: (1) baseline, (2) with a partnered dummy, (3) partnered child-years "
          "only, (4) unpartnered child-years only.", ""]
    for sex, _ in SEXES:
        L += dec_md(sex, DEC_FIX, f"#### {sex}: family-income IGE holding marriage fixed")
    L += ["### 3d. Level split (order-free, zeros kept)", "",
          "Each component divided by the race x sex x single-year-of-age mean family income (pooled rows: the "
          "all-race weighted mean); slopes on ln parental income. (1) = (2) + (3) + (4) exactly; (1) is the "
          "semi-elasticity of mean family income (a 'level IGE'), not the log IGE. Sample: family income in "
          "bounds, own and spouse earnings known and <= $150,000 of 1967 (own earnings may be zero).", ""]
    for sex, _ in SEXES:
        L += dec_md(sex, DEC_LV, f"#### {sex}: level split")
        L += dec_md(sex, DEC_LVM + [("level spouse: marriage", "Marriage part"),
                                    ("level spouse: conditional", "Spouse's earnings given marriage"),
                                    ("level spouse: remainder", "Remainder")],
                    f"#### {sex}: marriage split of the spouse channel (level)")
    m = EXTRA.get("means")
    if m is not None:
        L += ["### 3e. Composition of family income (level sample; sums over child-years)", "",
              "| Sex | Race | Band | Share partnered | Own earnings / family income | Spouse earnings / family income "
              "| Other / family income | Mean family income (2000 $) | Child-years |", "|---" * 9 + "|"]
        for r in m.itertuples():
            L.append(f"| {r.sex} | {r.race} | {r.band} | {r.partnered:.3f} | {r.own:.3f} | {r.sp:.3f} | {r.oth:.3f} "
                     f"| {r.faminc:,.0f} | {r.n:,} |")
        L.append("")

    # ---------------- 4 margins
    L += ["## 4. Margins: zeros and employment (PSID)", "",
          "Employment gradients by band are column (3) of the tables in 2a; at 40 in Section 1. Share of child-years "
          "with own earnings below $100 of 1967 (zero earners), by band:", ""]
    L += EXTRA.get("zeros_psid", []) + [""]
    L += ["ln of the band mean of own earnings (one row per child and band, >= 2 years; A quartic + mean age in the "
          "band): (1) zero years averaged in (children with a band mean below $100 of 1967 dropped), (2) mean over "
          "positive years only (>= 2). Column (3) tests whether including zeros changes the IGE and the racial gap. "
          "Rank versions (zeros kept vs positive years only) are columns (2)-(3) of the tables in 2d.", ""]
    for sex, _ in SEXES:
        L += age_md("PSID", "4 band-mean earnings", sex, BL, [("lbm_all", "ln band-mean earnings, zeros in"),
                                                              ("lbm_pos", "ln band-mean earnings, positive years")],
                    ndiff=1, title=f"#### PSID {sex}: zeros in the earnings IGE")

    # ---------------- 5 NLSY
    L += ["## 5. NLSY79 and NLSY97 replication", "",
          "NLSY79: born 1960-64, at home in 1979; parental income = mean family income 1978-80 (26.IGEByAge.py "
          "frame), ages 25-55; pooled = Black + White (the file's two groups) weighted by wt79. NLSY97: born "
          "1980-84; parental income = 1996 gross household income (one year, parent report; 29.NLSY97AgeProfile.py "
          "frame), ages 25-44; 'White' = non-Black non-Hispanic; pooled = all races weighted by the round weight. "
          "No spouse earnings in these extracts. Common = child-years with both outcomes.", ""]
    for data, ages in (("NLSY79", ("35", "40", "45")), ("NLSY97", ("30", "35", "40"))):
        L += [f"### 5a. {data}: Lee-Solon IGE at selected ages", "",
              "| | (1) ln family income | (2) ln own earnings (>0) | (3) (1) minus (2) (test) | (4) ln family income, "
              "common | (5) ln own earnings, common | (6) (4) minus (5) (test) | (7) Employed (LPM) |", "|---" * 8 + "|"]
        for sex, _ in SEXES:
            for a in ages:
                L.append(f"| **{data} {sex}, age {a}** |" + " |" * 7)
                for g in RACES + (GW, PG):
                    vals = [c(data, "5 LS", sex, "lfam", "lyp", a, g, "IGE"), c(data, "5 LS", sex, "learn", "lyp", a, g, "IGE"),
                            c(data, "5 LS", sex, "lfam - learn", "lyp", a, g, "IGE diff"),
                            c(data, "5 LS", sex, "lfam_c", "lyp", a, g, "IGE"),
                            c(data, "5 LS", sex, "learn_c", "lyp", a, g, "IGE"),
                            c(data, "5 LS", sex, "lfam_c - learn_c", "lyp", a, g, "IGE diff"),
                            c(data, "5 LS", sex, "emp", "lyp", a, g, "IGE")]
                    L.append(f"| {g} | " + " | ".join(vals) + " |")
            L.append(f"| N child-years / children (B; W), {sex.lower()} | " + " | ".join(
                n_txt(data, "5 LS", sex, y, "lyp", ages[1]) if y else "" for y in
                ("lfam", "learn", None, "lfam_c", "learn_c", None, "emp")) + " |")
        L.append("")
        bands = BL if data == "NLSY79" else BL[:4]
        for sex, _ in SEXES:
            L += age_md(data, "2 age", sex, bands, [("lfam", FAM), ("learn", ERN), ("emp", "Employed (LPM)")],
                        ndiff=1, title=f"### 5b. {data} {sex}: by band, own samples")
            L += age_md(data, "2 age common", sex, bands, [("lfam_c", FAM + ", common"), ("learn_c", ERN + ", common")],
                        ndiff=1, title=f"#### {data} {sex}: by band, common child-years")
            L += age_md(data, "2 rank age", sex, bands, [("ryf", "Rank of family income"),
                                                          ("rye", "Rank of own earnings (zeros kept)")],
                        ndiff=1, xcol="rp_fi", stat="slope", dstat="slope diff",
                        title=f"#### {data} {sex}: rank-rank slopes by band")
        L += [f"Share of child-years with zero / below-$100-of-1967 own earnings, {data}:", ""]
        L += EXTRA.get("zeros_79" if data == "NLSY79" else "zeros_97", []) + [""]

    L += ["## 6. Caveats", "",
          "- Spouse = the partner in the child's PSID family unit (married or cohabiting); 'other income' is a residual "
          "(family income minus the two labor incomes) and so includes transfers, asset income, other family members' "
          "income and business / farm income outside labor income; it is negative in ~4% of head-years (business "
          "losses). In the 1976-78 waves the wife's labor income is wages only (1.PSID.py).",
          "- The father's-earnings measure exists only for children with a male head at 16 (about half of Black and "
          "nearly nine in ten White children, `24.IGEDecomposition.py`); compare it with the 'father-present' row, "
          "not with the full-sample benchmark. Here the father's earnings are the head's labor income in bounds, "
          "without 24's hours / wage validity screen, so the estimates differ slightly from `ige_decomposition.md`.",
          "- The log decomposition is sequential and conditions on positive own earnings (it drops non-working "
          "daughters); the level split keeps zeros and has no ordering. The marriage split treats the cell means as "
          "fixed; its remainder is small in every cell.",
          "- Black rank-rank slopes are imprecise (weighted, so the SEO over-sample counts for less); late bands "
          "(45-55) hold few children and early birth cohorts. NLSY97 parental income is a single year (attenuates "
          "both IGEs equally; it does not affect the within-race comparison of outcomes).",
          ""]
    (OUT / "income_vs_earnings_ige.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    if "--md-only" in sys.argv:
        ROWS[:], _res, _ex = pd.read_pickle(CACHE)
        RES.update(_res)
        EXTRA.update(_ex)
        write_md()
        figure()
    else:
        main()
