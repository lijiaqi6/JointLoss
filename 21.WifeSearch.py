r"""Do wives search more after the husband's job loss? Constraint (search friction) or preference (2026-10-17).

Question (PI): where wives' employment does not rise after the husband's displacement, are they looking for work
without finding it (a constraint: the search friction binds) or not looking (a preference: norms, childcare, choice)?
By race and by the age of the youngest child.

Reads (read only): data/psid_person_year.pkl, data/psid_displacement.pkl (events from
19.FatherDisplacement.py), the raw PSID family files and the 2023 individual file in Dropbox/PSID, and
NLSY79/data/women79.pkl + family79.pkl (through NLSY79/common.py). Imports (does not edit) 19.FatherDisplacement.py
for the men's panel, the stacked design (stacks) and the fixed-effect demeaning. Writes
  output/wife_search.csv     every estimate (dataset, table, design, sample, subsample, outcome, term, coef, se,
                                 p, n, treated, controls, clusters, pre_mean)
  output/wife_search.md      tables
  output/wife_search_es.png  event-study figure

1. PSID. Events, sample and design exactly as in 19 (main definition: plant closed / moved or laid off / fired; first
   displacement of a male head with a child 0-17 and positive hours at baseline; clean controls not displaced up to
   the event year + 6; father x stack and calendar year x stack fixed effects; s.e. clustered by 1968 family).
   Wife = the wife present at baseline, while she is still his wife (as for the wife's hours in 19).
   a. Employment status at the interview (individual file; codes 1 working, 2 temporarily laid off, 3 looking for
      work / unemployed, 4 retired, 5 disabled, 6 keeping house, 7 student, 8 other; 0 / 9 -> missing):
        1979 ER30293, 1980 ER30323, 1981 ER30353, 1982 ER30382, 1983 ER30411, 1984 ER30441, 1985 ER30474,
        1986 ER30509, 1987 ER30545, 1988 ER30580, 1989 ER30616, 1990 ER30653, 1991 ER30699, 1992 ER30744,
        1993 ER30816, 1994 ER33111, 1995 ER33211, 1996 ER33311, 1997 ER33411, 1999 ER33512, 2001 ER33612,
        2003 ER33712, 2005 ER33813, 2007 ER33913, 2009 ER34016, 2011 ER34116, 2013 ER34216, 2015 ER34317,
        2017 ER34516, 2019 ER34716, 2021 ER34916, 2023 ER35116.
      employed = 1-2, looking = 3, in the labor force = 1-3, keeping house = 6. Timing: status is measured at the
      spring interview, so its event time is tau = interview year - displacement year; tau = 0 is the interview in
      the displacement year (mostly before the job ended: undated reports are dated to the year between two
      interviews), tau = +1 the first interview after it. Reference tau = -1 (interview a year before). Stacks with
      displacement year >= 1980 (status exists from the 1979 wave). The husband's own status 3 is the first stage.
   b. Flows between consecutive interviews (previous interview = 1 year back to 1997, 2 years back from 1999):
      job finding = employed now | not employed before; starts looking = looking now | out of the labor force
      (4-8) before; looking -> employed = employed now | looking before; job loss = not employed now | employed
      before. Conditional outcomes: estimated with treated x stack and calendar year x stack fixed effects (no
      wife fixed effect, as most wives have few such rows); stacks with displacement year >= 1981.
   c. The wife's unemployment in the calendar year (family file; event time = calendar year - displacement year,
      reference -2, as for hours in 19): hours unemployed 1974-1992 (waves 1975 V3833, 1976 V4727, 1977 V5252,
      1978 V5751, 1979 V6356, 1980 V6954, 1981 V7548, 1982 V8246, 1983 V8848, 1984 V10139, 1985 V11265,
      1986 V12664, 1987 V13816, 1988 V14872, 1989 V16372, 1990 V17781, 1991 V19081, 1992 V20381, 1993 V21674),
      converted to weeks at 40 hours a week (the PSID top code 2,080 = 52 x 40); weeks unemployed 1993-2022 (waves
      1994 ER4112, 1995 ER6952, 1996 ER9203, 1997 ER12190, 1999 ER16487, 2001 ER20415, 2003 ER24097,
      2005 ER27903, 2007 ER40893, 2009 ER46799, 2011 ER52207, 2013 ER58008, 2015 ER65188, 2017 ER71265,
      2019 ER77287, 2021 ER81614, 2023 ER85468; > 52 = NA, e.g. 99.9 in 1994-95). No wife unemployment item in the
      1968-1974 family files; the 2003+ year-before-last weeks (DE8 ... IN yyyy) are not used (the men's panel has
      no row for those years, as in 19). Stacks with displacement year >= 1976.
   Splits: head's race (Black, White); youngest child in the family unit 0-5 vs 6-17 at baseline; wife employed vs
   not employed at the baseline interview (status at tau = -1, else -2).
   Key identity: in the same sample, Delta(in labor force) = Delta(employed) + Delta(looking) exactly.

2. NLSY79 (women are the respondents; exact weekly labor-force status). Husband's weeks worked in calendar year t =
   Q2-15A of the t+1 interview (asked about the spouse present; annual for t = 1979-1993, so t = 1980-1993).
   Woman-years married to the same husband from the interview of t through that of t+1 (marriage history,
   interviews dated mid-May; MARSTAT 1 / 5 at both). Event = husband attached (>= 48 weeks in t-1) and < 40 weeks
   in t (as in 18); the woman's first such year. Clean controls: husband >= 48 weeks in t-1, >= 40 in t, not < 40 in
   t+1 or t+2 where observed, and no event of the woman up to t+2. Sample: mothers with a child 0-17 on 1 January t.
   Quarters q = -8..11 of 13 weeks from the first week of t (the husband's lost weeks fall somewhere in q = 0-3).
   Weekly array: >= 100 employed, 4 unemployed (looking), 5 out of the labor force; 2 (not working, unclassified),
   3, 7 and 0 are left out of the denominators, so employed + unemployed + out of LF = 1 in each quarter (>= 7 valid
   weeks). Also: share of the not-employed weeks spent looking (4 / (4 + 5), >= 4 such weeks); weekly
   re-employment hazard (x 100: weeks employed after a not-employed week / not-employed weeks at risk, >= 4 at
   risk). Quarters before the marriage began or after it ended are dropped (as for the PSID wife). Stacked
   regression: quarter x treated dummies, woman x stack and quarter x stack fixed effects, reference = the four
   quarters of t-1 (husband fully attached); s.e. clustered by woman. Splits: race; youngest child 0-5 vs 6-17;
   not employed in quarter -1 (the 13 weeks before t) vs employed.
   The NLSY79 event is a year with low weeks, not a displacement (layoffs, illness, strikes, quits); it is a
   descriptive complement.

3. Classification per group (PSID mean tau = +1..+3; NLSY79 mean of quarters 0-11): employment up (p < 0.10) ->
   'insurance'; else looking up (p < 0.10) -> 'constraint'; else participation up -> 'participation up'; else
   'no response'. The upper end of the 95% interval of the looking effect is shown, so a 'no response' can be read
   against what is ruled out.
Causal language: these are stacked event studies with clean controls (not experiments); displaced husbands' wives
may differ in trends, and outcomes are observed only while the marriage lasts (separation rises after
displacement), so post-event samples are selected.
"""
import importlib.util
import re
import warnings

import numpy as np
import pandas as pd
from scipy import stats

from common import DATA, OUT, HERE, stars
import os
NLSY79_DIR = Path(os.environ.get("NLSY79_DIR", r"G:\My Drive\Selection vs risk\NLSY79"))   # Selection-vs-risk/NLSY79 (helpers + extracts), read only

warnings.simplefilter("ignore", FutureWarning)
warnings.simplefilter("ignore", RuntimeWarning)


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


m19 = _load("fd19", HERE / "19.FatherDisplacement.py")
psid1, psid9 = m19.psid1, m19.psid9
NC = _load("nlsy_common", NLSY79_DIR / "common.py")

# ---------------------------------------------------------------- PSID variables
ST = {1979: "ER30293", 1980: "ER30323", 1981: "ER30353", 1982: "ER30382", 1983: "ER30411", 1984: "ER30441",
      1985: "ER30474", 1986: "ER30509", 1987: "ER30545", 1988: "ER30580", 1989: "ER30616", 1990: "ER30653",
      1991: "ER30699", 1992: "ER30744", 1993: "ER30816", 1994: "ER33111", 1995: "ER33211", 1996: "ER33311",
      1997: "ER33411", 1999: "ER33512", 2001: "ER33612", 2003: "ER33712", 2005: "ER33813", 2007: "ER33913",
      2009: "ER34016", 2011: "ER34116", 2013: "ER34216", 2015: "ER34317", 2017: "ER34516", 2019: "ER34716",
      2021: "ER34916", 2023: "ER35116"}
WU_HRS = dict(zip(range(1975, 1994), "V3833 V4727 V5252 V5751 V6356 V6954 V7548 V8246 V8848 V10139 V11265 V12664 "
                                    "V13816 V14872 V16372 V17781 V19081 V20381 V21674".split()))
WU_WKS = dict(zip([1994, 1995, 1996, 1997] + list(range(1999, 2024, 2)),
                  "ER4112 ER6952 ER9203 ER12190 ER16487 ER20415 ER24097 ER27903 ER40893 ER46799 ER52207 ER58008 "
                  "ER65188 ER71265 ER77287 ER81614 ER85468".split()))
WAVES = psid1.WAVES


def ind_status():
    """(pid, wave) -> employment status 1-8 (NaN otherwise)."""
    pos, _ = psid1.layout(psid1.IND.with_suffix(".do"))
    cols = ["ER30001", "ER30002", *ST.values()]
    d = psid1.read(psid1.IND, cols, pos)
    pid = d.ER30001 * 1000 + d.ER30002
    out = []
    for w, c in ST.items():
        s = d[c].where(d[c].between(1, 8))
        out.append(pd.DataFrame({"pid": pid, "wave": w, "st": s}).dropna())
    s = pd.concat(out, ignore_index=True)
    return s.set_index(["pid", "wave"])["st"]


def wife_unemp():
    """Family file: wave, int, weeks the wife was unemployed in the previous calendar year."""
    out = []
    for w in sorted({**WU_HRS, **WU_WKS}):
        folder = psid1.FAM / (f"fam{w}" if w < 1994 else f"fam{w}er")
        base = next(f for f in folder.glob("*.do") if "formats" not in f.name).with_suffix("")
        pos, labs = psid1.layout(base.with_suffix(".do"))
        idv = labs[1][0]
        v = WU_HRS.get(w) or WU_WKS[w]
        f = psid1.read(base, [idv, v], pos)
        x = f[v].astype(float)
        wk = (x.where(x.between(0, 5840)) / 40).clip(upper=52) if w in WU_HRS else x.where(x.between(0, 52))
        out.append(pd.DataFrame({"wave": w, "int": f[idv], "wu_wks": wk}))
    return pd.concat(out, ignore_index=True)


def lookup(s, a, b):
    return s.reindex(pd.MultiIndex.from_arrays([np.asarray(a, dtype=np.int64),
                                                np.asarray(b, dtype=np.int64)])).to_numpy()


def prev_wave(w):
    w = np.asarray(w)
    return np.where(w <= 1997, w - 1, w - 2)


def psid_panel(kind, m, d, S, WU):
    p = m19.stacks(m, d, kind)
    p["wave"] = (p["year"] + 1).astype(np.int64)
    mi = m[["pid", "year", "int"]].drop_duplicates(["pid", "year"])
    p = p.merge(mi, on=["pid", "year"], how="left")
    p = p.merge(WU, left_on=["wave", "int"], right_on=["wave", "int"], how="left")
    same = (p["w_pid"] == p["w0"]) & p["w0"].notna()
    w0 = p["w0"].fillna(-1).astype(np.int64)
    ws = np.where(same, lookup(S, w0, p["wave"]), np.nan)
    wprev = np.where(same, lookup(S, w0, prev_wave(p["wave"])), np.nan)
    hs = lookup(S, p["pid"], p["wave"])
    b1 = lookup(S, w0, p["ev"] - 1)
    b2 = lookup(S, w0, p["ev"] - 2)
    p["ws0"] = np.where(p["w0"].notna(), np.where(np.isnan(b1), b2, b1), np.nan)
    p["k"] = p["e"] + 1

    def ind(cond, valid):
        return np.where(valid, cond.astype(float), np.nan)
    v = ~np.isnan(ws)
    p["w_emp_s"] = ind(np.isin(ws, [1, 2]), v)
    p["w_look"] = ind(ws == 3, v)
    p["w_lfp"] = ind(np.isin(ws, [1, 2, 3]), v)
    p["w_house"] = ind(ws == 6, v)
    vh = ~np.isnan(hs)
    p["h_look"] = ind(hs == 3, vh)
    vp = v & ~np.isnan(wprev)
    p["w_find"] = ind(np.isin(ws, [1, 2]), vp & ~np.isin(wprev, [1, 2]))
    p["w_n2u"] = ind(ws == 3, vp & (wprev >= 4))
    p["w_u2e"] = ind(np.isin(ws, [1, 2]), vp & (wprev == 3))
    p["w_exit"] = ind(~np.isin(ws, [1, 2]), vp & np.isin(wprev, [1, 2]))
    p["w_wu_wks"] = p["wu_wks"].where(same)
    p["w_wu_any"] = (p["w_wu_wks"] > 0).astype(float).where(p["w_wu_wks"].notna())
    p["tstack"] = pd.factorize(p["treat"].astype(np.int64) * 10000 + p["ev"].astype(np.int64))[0]
    return p


# ---------------------------------------------------------------- estimation
def fit(q, y, xs, fe, cluster):
    """OLS of y on xs absorbing the fixed effects in columns fe; CR1 clustered covariance."""
    groups = []
    kfe = 0
    for c in fe:
        g = pd.factorize(q[c])[0]
        groups.append((g, g.max() + 1))
        kfe += g.max() + 1
    A = m19.demean(np.column_stack([q[y].to_numpy(float), q[xs].to_numpy(float)]), groups)
    Y, X = A[:, 0], A[:, 1:]
    XtX = np.linalg.pinv(X.T @ X)
    b = XtX @ X.T @ Y
    res = Y - X @ b
    g = pd.factorize(q[cluster])[0]
    G = g.max() + 1
    Sm = np.zeros((G, X.shape[1]))
    np.add.at(Sm, g, X * res[:, None])
    n, k = X.shape
    adj = G / (G - 1) * (n - 1) / max(n - k - kfe, 1)
    V = adj * XtX @ (Sm.T @ Sm) @ XtX
    return b, V, n, G


def pval(b, se):
    return 2 * stats.norm.sf(abs(b / se)) if se > 0 else np.nan


# PSID outcome groups: (column, label, time column, reference, min event year, fixed effects)
FE_U = ["unit", "cell"]
FE_T = ["tstack", "cell"]
K_TERMS = [-2, 0, 1, 2, 3, 4, 5, 6, 7]
E_TERMS = [-3, -1, 0, 1, 2, 3, 4, 5, 6]
PS = {"h_look": ("Husband looking / unemployed (status 3)", "k", 1980, FE_U),
      "w_emp_s": ("Wife employed (status 1-2)", "k", 1980, FE_U),
      "w_look": ("Wife looking / unemployed (status 3)", "k", 1980, FE_U),
      "w_lfp": ("Wife in labor force (status 1-3)", "k", 1980, FE_U),
      "w_house": ("Wife keeping house (status 6)", "k", 1980, FE_U),
      "w_wu_wks": ("Wife's weeks unemployed in year", "e", 1976, FE_U),
      "w_wu_any": ("Wife any unemployment in year", "e", 1976, FE_U),
      "w_emp": ("Wife worked in year (hours > 0)", "e", 1968, FE_U),
      "w_find": ("Job finding: employed | not employed at previous interview", "k", 1981, FE_T),
      "w_n2u": ("Starts looking: looking | out of LF at previous interview", "k", 1981, FE_T),
      "w_u2e": ("Looking -> employed: employed | looking at previous interview", "k", 1981, FE_T),
      "w_exit": ("Job loss: not employed | employed at previous interview", "k", 1981, FE_T)}
MAIN_Y = ["h_look", "w_emp_s", "w_look", "w_lfp", "w_house", "w_wu_wks", "w_wu_any", "w_emp"]
FLOW_Y = ["w_find", "w_n2u", "w_u2e", "w_exit"]


def psid_es(p, y):
    lab, tc, min_ev, fe = PS[y]
    terms = K_TERMS if tc == "k" else E_TERMS
    ref = -1 if tc == "k" else -2
    q = p[(p["ev"] >= min_ev) & p[tc].isin(terms + [ref])].dropna(subset=[y]).copy()
    if y != "h_look":
        q = q[q["w0"].notna()]
    xs = []
    for t in terms:
        c = f"d{t}"
        q[c] = ((q[tc] == t) & (q["treat"] == 1)).astype(float)
        xs.append(c)
    keep = [c for c in xs if q[c].sum() > 0]
    b, V, n, G = fit(q.reset_index(drop=True), y, keep, fe, "fam68")
    bd = dict(zip(keep, b))
    idx = {c: i for i, c in enumerate(keep)}
    info = dict(n=n, clusters=G, treated=q.loc[q["treat"] == 1, "unit"].nunique(),
                controls=q.loc[q["treat"] == 0, "unit"].nunique(),
                pre_mean=q[(q["treat"] == 1) & q[tc].isin([ref, ref - 1] if tc == "e" else [ref, -2])][y].mean())
    out = []
    for t in terms:
        c = f"d{t}"
        if c in idx:
            se = np.sqrt(V[idx[c], idx[c]])
            out.append(dict(term=f"t={t:+d}", coef=bd[c], se=se, p=pval(bd[c], se), **info))
    wv = np.array([1.0 if c in ("d1", "d2", "d3") else 0.0 for c in keep])
    if wv.sum() > 0:
        wv /= wv.sum()
        cb, cs = wv @ b, np.sqrt(wv @ V @ wv)
        out.append(dict(term="mean +1..+3", coef=cb, se=cs, p=pval(cb, cs), **info))
    return out


def sub_sample(p, race, sub):
    q = p if race == "All" else p[p["hrace"] == race]
    if sub == "young05":
        q = q[q["young0"] <= 5]
    elif sub == "young617":
        q = q[q["young0"] >= 6]
    elif sub == "wemp":
        q = q[q["ws0"].isin([1, 2])]
    elif sub == "wnot":
        q = q[q["ws0"].between(3, 8)]
    return q


SUBLAB = {None: "all", "young05": "youngest child 0-5", "young617": "youngest child 6-17",
          "wemp": "wife employed at baseline", "wnot": "wife not employed at baseline"}

# ---------------------------------------------------------------- NLSY79
NQ = list(range(-8, 12))
NREF = [-4, -3, -2, -1]
NY = {"emp": "Share of weeks employed", "unemp": "Share of weeks unemployed (looking)",
      "olf": "Share of weeks out of the labor force", "lfp": "Share of weeks in the labor force",
      "look_ne": "Looking share of not-employed weeks", "haz": "Weekly re-employment hazard (x100)"}


def nlsy_panel():
    d = NC.load()
    W = NC.weekly(d).astype(float)
    nW = W.shape[1]
    B = NC.births(d)
    mar = NC.marriages(d)
    n = len(d)
    H = {}
    for t in range(1979, 1994):
        c = f"Q2-15A_{t + 1}"
        x = d[c].to_numpy(float) if c in d else np.full(n, np.nan)
        H[t] = np.where((x >= 0) & (x <= 52), x, np.nan)
    for t in range(1994, 1997):
        H[t] = np.full(n, np.nan)
    MS = {t: d[f"MARSTAT-KEY_{t}"].to_numpy(float) if f"MARSTAT-KEY_{t}" in d else np.full(n, np.nan)
          for t in range(1979, 1996)}
    elig = []
    for i in range(n):
        for t in range(1980, 1994):
            hp, hc = H[t - 1][i], H[t][i]
            if not (hp == hp and hc == hc) or MS[t][i] not in (1, 5) or MS[t + 1][i] not in (1, 5):
                continue
            iw0, iw1 = NC.week_of(t, 5), NC.week_of(t + 1, 5)
            cur = [(b, e) for b, e in mar[i] if b <= iw0 and (not (e == e) or e > iw1)]
            if not cur:
                continue
            mb, me = cur[-1]
            elig.append(dict(i=i, t=t, hp=hp, hc=hc, hn=H[t + 1][i], hn2=H[t + 2][i], mb=mb, me=me))
    E = pd.DataFrame(elig)
    E["event"] = (E["hp"] >= 48) & (E["hc"] < 40)
    first = E[E["event"]].groupby("i")["t"].min()
    E["first_ev"] = E["i"].map(first).fillna(9999)
    tr = E["event"] & (E["t"] == E["first_ev"])
    ct = ((E["hp"] >= 48) & (E["hc"] >= 40) & ~(E["hn"] < 40) & ~(E["hn2"] < 40) & (E["first_ev"] > E["t"] + 2))
    E = E[tr | ct].copy()
    E["treat"] = tr[tr | ct].astype(int)
    rows = []
    for r in E.itertuples():
        i, t = r.i, r.t
        w0 = NC.week_of(t, 1, 1)
        bw = B[i][~np.isnan(B[i])]
        kids = bw[(bw <= w0) & (bw > w0 - 18 * 52.18)]
        if len(kids) == 0:
            continue
        young = (w0 - kids.max()) / 52.18
        for q in NQ:
            a = int(w0 + 13 * q)
            z = a + 13
            if a < 1 or z > nW or a < r.mb or (r.me == r.me and a > r.me):
                continue
            seg = W[i, a:z]
            prv = W[i, a - 1:z - 1]
            ne, nu, nn = (seg >= 100).sum(), (seg == 4).sum(), (seg == 5).sum()
            tot = ne + nu + nn
            out = dict(i=i, t=t, q=q, treat=r.treat, young=young, hp=r.hp, hc=r.hc, hn=r.hn)
            if tot >= 7:
                out.update(emp=ne / tot, unemp=nu / tot, olf=nn / tot, lfp=(ne + nu) / tot)
            if nu + nn >= 4:
                out["look_ne"] = nu / (nu + nn)
            risk = np.isin(prv, [2, 4, 5]) & ((seg >= 100) | np.isin(seg, [2, 4, 5]))
            if risk.sum() >= 4:
                out["haz"] = 100 * ((seg >= 100) & risk).sum() / risk.sum()
            rows.append(out)
    P = pd.DataFrame(rows)
    P["race"] = d["race"].to_numpy()[P["i"]]
    P["id"] = d["id"].to_numpy()[P["i"]]
    P["unit"] = pd.factorize(P["i"].astype(np.int64) * 10000 + P["t"])[0]
    P["cell"] = pd.factorize(P["t"].astype(np.int64) * 100 + P["q"] + 50)[0]
    base = P[P["q"] == -1].set_index("unit")["emp"]
    P["emp_qm1"] = P["unit"].map(base)
    return P, E


def nlsy_es(P, y):
    q = P.dropna(subset=[y]).copy()
    xs = []
    for t in NQ:
        if t in NREF:
            continue
        c = f"q{t}"
        q[c] = ((q["q"] == t) & (q["treat"] == 1)).astype(float)
        xs.append(c)
    keep = [c for c in xs if q[c].sum() > 0]
    b, V, n, G = fit(q.reset_index(drop=True), y, keep, ["unit", "cell"], "i")
    idx = {c: j for j, c in enumerate(keep)}
    info = dict(n=n, clusters=G, treated=q.loc[q["treat"] == 1, "unit"].nunique(),
                controls=q.loc[q["treat"] == 0, "unit"].nunique(),
                pre_mean=q[(q["treat"] == 1) & q["q"].isin(NREF)][y].mean())
    out = []
    for c in keep:
        se = np.sqrt(V[idx[c], idx[c]])
        out.append(dict(term=c, coef=b[idx[c]], se=se, p=pval(b[idx[c]], se), **info))
    for lab, qs in (("year t-2", range(-8, -4)), ("year t", range(0, 4)), ("year t+1", range(4, 8)),
                    ("year t+2", range(8, 12)), ("mean q0..q11", range(0, 12))):
        wv = np.array([1.0 if int(c[1:]) in qs else 0.0 for c in keep])
        if wv.sum() == 0:
            continue
        wv /= wv.sum()
        cb, cs = wv @ b, np.sqrt(wv @ V @ wv)
        out.append(dict(term=lab, coef=cb, se=cs, p=pval(cb, cs), **info))
    return out


def nlsy_sub(P, race, sub):
    q = P if race == "All" else P[P["race"] == race]
    if sub == "young05":
        q = q[q["young"] < 6]
    elif sub == "young617":
        q = q[q["young"] >= 6]
    elif sub == "wnot":
        q = q[q["emp_qm1"] == 0]
    elif sub == "wemp":
        q = q[q["emp_qm1"] > 0]
    return q


NSUBLAB = {None: "all", "young05": "youngest child 0-5", "young617": "youngest child 6-17",
           "wnot": "not employed in the quarter before", "wemp": "employed in the quarter before"}


# ---------------------------------------------------------------- formatting
def cellf(r, dec=3):
    if r is None:
        return ""
    pv = "<0.001" if r["p"] < 0.001 else f"{r['p']:.3f}"
    return f"{r['coef']:.{dec}f}{stars(r['p'])} ({r['se']:.{dec}f}; p={pv})"


def dec_of(y):
    return 2 if y in ("w_wu_wks", "haz") else 3


def md_table(header, panels, foot=()):
    out = ["| | " + " | ".join(header) + " |", "|" + "---|" * (len(header) + 1)]
    for title, rows in panels:
        if title:
            out.append(f"| **{title}** |" + " |" * len(header))
        for lab, cells in rows:
            out.append(f"| {lab} | " + " | ".join(cells) + " |")
    for lab, cells in foot:
        out.append(f"| {lab} | " + " | ".join(cells) + " |")
    return "\n".join(out)


def get(res, key, y, term):
    o = res.get(key, {}).get(y)
    if not o:
        return None
    return next((r for r in o if r["term"] == term), None)


def info_rows(res, key, ys, unit_lab):
    rows = []
    o0 = {y: (res.get(key, {}).get(y) or [None])[0] for y in ys}
    rows.append(("Treated mean at reference", [f"{o0[y]['pre_mean']:.3f}" if o0[y] else "" for y in ys]))
    rows.append(("N (stacked rows)", [f"{o0[y]['n']:,}" if o0[y] else "" for y in ys]))
    rows.append((unit_lab, [f"{o0[y]['treated']:,} / {o0[y]['controls']:,}" if o0[y] else "" for y in ys]))
    rows.append(("Clusters", [f"{o0[y]['clusters']:,}" if o0[y] else "" for y in ys]))
    return rows


def classify(emp, look, lfp):
    up = lambda r: r is not None and r["coef"] > 0 and r["p"] < 0.10      # noqa: E731
    down = lambda r: r is not None and r["coef"] < 0 and r["p"] < 0.10    # noqa: E731
    if up(emp):
        return "insurance (employment up" + (", looking up too)" if up(look) else ")")
    if up(look):
        return "constraint (looking up, employment not)"
    if up(lfp):
        return "participation up (split unclear)"
    if down(emp):
        return "no insurance (employment down)"
    return "no response (neither)"


def yn(r):
    if r is None:
        return ""
    s = "up" if (r["coef"] > 0 and r["p"] < 0.10) else "down" if (r["coef"] < 0 and r["p"] < 0.10) else "no"
    return f"{s}: {r['coef']:.3f}{stars(r['p'])} (p={r['p']:.3f})"


# ---------------------------------------------------------------- figure
def figure(res, nres):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ink, muted, grid = "#0b0b0b", "#52514e", "#e6e5e0"
    fig, axes = plt.subplots(3, 4, figsize=(16, 11))
    rows = [
        ([(("main", "Black", None), "Black", "#2a78d6", "o"), (("main", "White", None), "White", "#eb6834", "s")],
         ["w_emp_s", "w_look", "w_lfp", "w_house"], "psid"),
        ([(("main", "All", "young05"), "Youngest 0-5", "#1b8a6b", "o"),
          (("main", "All", "young617"), "Youngest 6-17", "#7d4fc4", "s")],
         ["w_emp_s", "w_look", "w_lfp", "w_house"], "psid"),
        ([(("Black", None), "Black", "#2a78d6", "o"), (("White", None), "White", "#eb6834", "s")],
         ["emp", "unemp", "olf", "look_ne"], "nlsy")]
    for ri, (series, ys, src) in enumerate(rows):
        for ci, y in enumerate(ys):
            ax = axes[ri, ci]
            for k, (key, lab, col, mk) in enumerate(series):
                if src == "psid":
                    o = [r for r in res[key][y] if r["term"].startswith("t=")]
                    z = sorted([(int(r["term"][2:]), r["coef"], r["se"]) for r in o] + [(-1, 0.0, 0.0)])
                    sh = (k - 0.5) * 0.18
                else:
                    o = [r for r in nres[key][y] if re.fullmatch(r"q-?\d+", r["term"])]
                    z = sorted([(int(r["term"][1:]), r["coef"], r["se"]) for r in o] +
                               [(qq, 0.0, 0.0) for qq in NREF])
                    sh = (k - 0.5) * 0.25
                e, b, s = (np.array(v) for v in zip(*z))
                ax.fill_between(e + sh, b - 1.96 * s, b + 1.96 * s, color=col, alpha=0.12, linewidth=0)
                ax.plot(e + sh, b, color=col, marker=mk, markersize=4, linewidth=1.8, label=lab)
            ax.axhline(0, color=muted, linewidth=0.8)
            ax.axvline(-0.5, color="#b0afa8", linewidth=0.8, linestyle=":")
            title = PS[y][0] if src == "psid" else NY[y]
            ax.set_title(("PSID: " if src == "psid" else "NLSY79: ") + title, fontsize=9.5, color=ink)
            ax.tick_params(labelsize=8, colors=muted)
            for sp in ("top", "right"):
                ax.spines[sp].set_visible(False)
            ax.grid(axis="y", color=grid, linewidth=0.6)
            if src == "psid":
                ax.set_xticks(range(-2, 8))
            else:
                ax.set_xticks(range(-8, 12, 2))
        axes[ri, 0].legend(frameon=False, fontsize=9)
    axes[0, 0].set_ylabel("by race", fontsize=9, color=muted)
    axes[1, 0].set_ylabel("by youngest child's age", fontsize=9, color=muted)
    axes[2, 0].set_ylabel("by race (quarters)", fontsize=9, color=muted)
    fig.supxlabel("PSID rows (displacement): interview year - displacement year, reference -1. NLSY79 row (husband "
                  "< 40 weeks in year t): quarters from the first week of t, reference = the four quarters of t-1",
                  fontsize=9.5, color=muted)
    fig.suptitle("Wives' employment, search and participation after the husband's job loss "
                 "(stacked event studies, 95% CI)", fontsize=12, color=ink)
    fig.tight_layout(rect=(0, 0, 1, 0.97), h_pad=2.2)
    fig.savefig(OUT / "wife_search_es.png", dpi=150, facecolor="#fcfcfb")
    plt.close(fig)


# ---------------------------------------------------------------- main
def main():
    ROWS = []
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    d = pd.read_pickle(DATA / "psid_displacement.pkl")
    fam = psid9.family()
    S = ind_status()
    WU = wife_unemp()
    print("status and unemployment items read", flush=True)
    m = m19.men_panel(py, fam)
    P = {k: psid_panel(k, m, d, S, WU) for k in ("main", "strict")}
    res = {}
    specs = [("main", r, s) for r in ("All", "Black", "White") for s in (None, "young05", "young617", "wemp", "wnot")]
    specs += [("strict", r, None) for r in ("All", "Black", "White")]
    for kind, race, sub in specs:
        p = sub_sample(P[kind], race, sub)
        key = (kind, race, sub)
        res[key] = {}
        ys = MAIN_Y + FLOW_Y if kind == "main" else ["h_look", "w_emp_s", "w_look", "w_lfp", "w_house"]
        for y in ys:
            try:
                o = psid_es(p, y)
            except Exception as exc:                      # too few observations
                print("skip", key, y, exc)
                continue
            res[key][y] = o
            for r in o:
                ROWS.append(dict(dataset="PSID", table="event_study", design=kind, sample=race,
                                 subsample=sub or "", outcome=y, **r))
        print("PSID", key, flush=True)

    # ---- NLSY79
    NP, NE = nlsy_panel()
    print("NLSY79 panel", len(NP), flush=True)
    nres = {}
    for race in ("All", "Black", "White"):
        for sub in (None, "young05", "young617", "wnot", "wemp"):
            q = nlsy_sub(NP, race, sub)
            key = (race, sub)
            nres[key] = {}
            for y in NY:
                try:
                    o = nlsy_es(q, y)
                except Exception as exc:
                    print("skip", key, y, exc)
                    continue
                nres[key][y] = o
                for r in o:
                    ROWS.append(dict(dataset="NLSY79", table="event_study", design="husband <40 weeks",
                                     sample=race, subsample=sub or "", outcome=y, **r))
            print("NLSY79", key, flush=True)
    figure(res, nres)

    # ---------------------------------------------------------------- markdown
    md = ["# Do wives search more after the husband's job loss? Constraint or preference", "",
          "Built by `21.WifeSearch.py` (2026-10-17); variables per wave in its docstring. Unweighted. *** p<0.01, "
          "** p<0.05, * p<0.1; every cell = coefficient (s.e.; p-value). The PSID design is the stacked event "
          "study of `19.FatherDisplacement.py` (first displacement = plant closing / move or layoff / firing of a "
          "male head with a child 0-17 and positive hours at baseline; clean controls not displaced up to the event "
          "year + 6; father x stack and calendar year x stack fixed effects; s.e. clustered by 1968 family). These "
          "are comparisons with clean controls, not experiments: they identify the effect of displacement only if "
          "displaced and control families would have followed parallel paths, and wives' outcomes are observed only "
          "while the marriage lasts (separation rises after displacement, see 19), so post-event samples are "
          "selected.", "",
          "**Reading guide.** Status outcomes (employed / looking / in the labor force / keeping house) come from "
          "the employment status at the spring interview: tau = interview year - displacement year, reference "
          "tau = -1, tau = 0 is the interview in the displacement year (mostly before the job ended), tau = +1 the "
          "first interview after it; 'mean +1..+3' = interviews 1-3 years later. Calendar-year outcomes (weeks "
          "unemployed, worked in the year) use tau = calendar year - displacement year, reference -2, as in 19. "
          "Because employed + looking = in the labor force in the same sample, the coefficients add up exactly: "
          "Delta LF = Delta employed + Delta looking.", ""]

    hdr = [PS[y][0] for y in MAIN_Y]
    taus = [-3, -2, -1, 0, 1, 2, 3, 4, 5, 6]

    def tau_cell(key, y, t):
        tc = PS[y][1]
        ref = -1 if tc == "k" else -2
        if t == ref:
            return "ref"
        r = get(res, key, y, f"t={t:+d}")
        return cellf(r, dec_of(y)) if r else ""

    panels = []
    for race in ("All", "Black", "White"):
        key = ("main", race, None)
        rows = [(f"tau={t:+d}", [tau_cell(key, y, t) for y in MAIN_Y]) for t in taus]
        rows.append(("**mean +1..+3**", [cellf(get(res, key, y, "mean +1..+3"), dec_of(y)) for y in MAIN_Y]))
        rows += info_rows(res, key, MAIN_Y, "Displaced fathers / control father-stacks")
        panels.append((f"{race} fathers", rows))
    foot = [("Event time", ["interview" if PS[y][1] == "k" else "calendar year" for y in MAIN_Y]),
            ("Stacks (displacement years)", [f">= {PS[y][2]}" for y in MAIN_Y]),
            ("Fixed effects", ["father x stack, calendar year x stack"] * len(MAIN_Y))]
    md += ["## 1. PSID: wives' employment, search and participation after the husband's displacement", "",
           "### Table 1. Event study, pooled and by race", "",
           "One regression per column (outcome in the header); rows = displaced x event-time coefficients. The first "
           "column is the first stage (the husband's own status at the interview).", "",
           md_table(hdr, panels, foot), "", "![event study](wife_search_es.png)", ""]

    # Table 2: subgroups
    short = ["tau=-2 / -3 (pre)", "tau=+1", "tau=+2", "tau=+3", "mean +1..+3"]

    def short_cells(key, y):
        tc = PS[y][1]
        pre = get(res, key, y, "t=-2" if tc == "k" else "t=-3")
        return [cellf(pre, dec_of(y)), cellf(get(res, key, y, "t=+1"), dec_of(y)),
                cellf(get(res, key, y, "t=+2"), dec_of(y)), cellf(get(res, key, y, "t=+3"), dec_of(y)),
                cellf(get(res, key, y, "mean +1..+3"), dec_of(y))]
    panels = []
    for race in ("All", "Black", "White"):
        for sub in ("young05", "young617", "wemp", "wnot"):
            key = ("main", race, sub)
            cells = {y: short_cells(key, y) for y in MAIN_Y}
            rows = [(lab, [cells[y][j] for y in MAIN_Y]) for j, lab in enumerate(short)]
            rows += info_rows(res, key, MAIN_Y, "Displaced fathers / control father-stacks")
            panels.append((f"{race}: {SUBLAB[sub]}", rows))
    md += ["### Table 2. By the youngest child's age and the wife's status at baseline", "",
           "Baseline status = the wife's employment status at the interview a year before the displacement year "
           "(tau = -1; else -2). For wives not employed at baseline, 'Wife employed' is the cumulative transition "
           "into employment (job finding) and 'Wife looking' the transition into search, relative to controls with "
           "the same baseline status.", "", md_table(hdr, panels, foot), ""]

    # Table 3: flows
    fh = [PS[y][0] for y in FLOW_Y]
    panels = []
    for race in ("All", "Black", "White"):
        for sub in (None, "young05", "young617"):
            key = ("main", race, sub)
            cells = {y: short_cells(key, y) for y in FLOW_Y}
            rows = [(lab, [cells[y][j] for y in FLOW_Y]) for j, lab in enumerate(short)]
            rows += info_rows(res, key, FLOW_Y, "Displaced fathers / control father-stacks")
            panels.append((f"{race}: {SUBLAB[sub]}", rows))
    md += ["### Table 3. Flows between consecutive interviews", "",
           "Each outcome is defined only for wives in the origin state at the previous interview (1 year earlier to "
           "1997, 2 years from 1999). Treated x stack and calendar year x stack fixed effects (most wives have few "
           "rows in an origin state); reference tau = -1; stacks from 1981.", "",
           md_table(fh, panels, [("Fixed effects", ["treated x stack, calendar year x stack"] * len(FLOW_Y))]), ""]

    # Table 4: decomposition
    dh = ["Delta in labor force", "= Delta employed", "+ Delta looking", "Looking share of Delta LF",
          "Delta keeping house", "Husband looking (first stage)"]
    rows = []
    for race in ("All", "Black", "White"):
        for sub in (None, "young05", "young617", "wemp", "wnot"):
            key = ("main", race, sub)
            g = {y: get(res, key, y, "mean +1..+3") for y in ("w_lfp", "w_emp_s", "w_look", "w_house", "h_look")}
            sh = (f"{g['w_look']['coef'] / g['w_lfp']['coef']:.2f}" if g["w_lfp"] and abs(g["w_lfp"]["coef"]) > 1e-9
                  else "")
            rows.append((f"{race}: {SUBLAB[sub]}", [cellf(g["w_lfp"]), cellf(g["w_emp_s"]), cellf(g["w_look"]), sh,
                                                    cellf(g["w_house"]), cellf(g["h_look"])]))
    md += ["### Table 4. Decomposition of the participation response (mean of tau = +1..+3, PSID status)", "",
           "Each cell is the 'mean +1..+3' coefficient of a separate regression (columns 1-3 and 5 on the same "
           "wives); column 1 = column 2 + column 3 exactly. The looking share is not meaningful when Delta LF is near "
           "zero.", "", md_table(dh, [("", rows)]), ""]

    # Table 5: closures only
    sy = ["h_look", "w_emp_s", "w_look", "w_lfp", "w_house"]
    panels = []
    for race in ("All", "Black", "White"):
        key = ("strict", race, None)
        cells = {y: short_cells(key, y) for y in sy}
        rows = [(lab, [cells[y][j] for y in sy]) for j, lab in enumerate(short)]
        rows += info_rows(res, key, sy, "Displaced fathers / control father-stacks")
        panels.append((f"Closures only: {race}", rows))
    md += ["### Table 5. Robustness: plant closures only (19's strict definition)", "",
           md_table([PS[y][0] for y in sy], panels, [("Fixed effects", ["father x stack, calendar year x stack"]
                                                      * len(sy))]), ""]

    # ---------------------------------------------------------------- NLSY79 tables
    ne_tr = NE[NE["treat"] == 1]
    ne_ct = NE[NE["treat"] == 0]
    units = NP.drop_duplicates("unit")
    md += ["## 2. NLSY79: weekly employment, unemployment and participation around the husband's low-weeks year",
           "", "Event = the husband worked >= 48 weeks in t-1 and < 40 in calendar year t (Q2-15A, asked about the "
           "spouse present; t = 1980-1993); controls: >= 48 weeks in t-1, >= 40 in t, not < 40 in t+1 / t+2 where "
           "observed, no event of the woman up to t+2. Mothers with a child 0-17 on 1 January t, married to the same "
           "husband over the two interviews. Quarter q = 13 weeks from the first week of t; reference = the four "
           "quarters of t-1. Woman x stack and quarter x stack fixed effects; s.e. clustered by woman. The event is "
           "a year of low weeks (layoffs but also illness, strikes, quits, seasonal work), not a displacement, and "
           "the husband's weeks can respond to the household: descriptive complement.", "",
           f"Woman-years: events {int(NE['treat'].sum()):,} ({ne_tr['i'].nunique():,} women), control stacks "
           f"{int((NE['treat'] == 0).sum()):,}; with a child 0-17 (in the panel): events "
           f"{int(units['treat'].sum()):,} (Black {int(units.loc[units.race == 'Black', 'treat'].sum()):,}, White "
           f"{int(units.loc[units.race == 'White', 'treat'].sum()):,}), control stacks "
           f"{int((units['treat'] == 0).sum()):,}. Husband's mean weeks, events: t-1 {ne_tr['hp'].mean():.1f}, "
           f"t {ne_tr['hc'].mean():.1f}, t+1 {ne_tr['hn'].mean():.1f}; controls: {ne_ct['hp'].mean():.1f}, "
           f"{ne_ct['hc'].mean():.1f}, {ne_ct['hn'].mean():.1f}. Share of events with 0 weeks in t: "
           f"{(ne_tr['hc'] == 0).mean():.3f}.", ""]
    nys = list(NY)
    nterms = ["year t-2", "year t", "year t+1", "year t+2", "mean q0..q11"]
    panels = []
    for race in ("All", "Black", "White"):
        for sub in (None, "young05", "young617", "wnot", "wemp"):
            key = (race, sub)
            rows = [(t, [cellf(get(nres, key, y, t), dec_of(y)) for y in nys]) for t in nterms]
            rows += info_rows(nres, key, nys, "Event / control woman-stacks")
            panels.append((f"{race}: {NSUBLAB[sub]}", rows))
    md += ["### Table 6. NLSY79: annual means of the quarterly event-study coefficients", "",
           "One regression per column per panel; 'year t-2' = mean of quarters -8..-5 (pre-trend check), 'year t' = "
           "quarters 0-3 (the husband's low-weeks year), etc.", "",
           md_table([NY[y] for y in nys], panels, [("Fixed effects", ["woman x stack, quarter x stack"] * len(nys))]),
           ""]
    qs = [q for q in NQ if q not in NREF]
    panels = []
    for race in ("All", "Black", "White"):
        key = (race, None)
        rows = [(f"q={q:+d}", [cellf(get(nres, key, y, f"q{q}"), dec_of(y)) for y in nys]) for q in qs]
        panels.append((race, rows))
    md += ["### Table 7. NLSY79: quarterly coefficients (reference = quarters -4..-1)", "",
           md_table([NY[y] for y in nys], panels), ""]

    # ---------------------------------------------------------------- classification
    rows = []
    for race in ("All", "Black", "White"):
        for sub in (None, "young05", "young617", "wemp", "wnot"):
            key = ("main", race, sub)
            g = {y: get(res, key, y, "mean +1..+3") for y in ("w_lfp", "w_look", "w_emp_s")}
            hi = g["w_look"]["coef"] + 1.96 * g["w_look"]["se"] if g["w_look"] else np.nan
            rows.append((f"PSID {race}: {SUBLAB[sub]}", [yn(g["w_lfp"]), yn(g["w_look"]), yn(g["w_emp_s"]),
                                                          f"{hi:.3f}", classify(g["w_emp_s"], g["w_look"],
                                                                                g["w_lfp"])]))
            ROWS.append(dict(dataset="PSID", table="classification", design="main", sample=race,
                             subsample=sub or "", outcome="class", term=classify(g["w_emp_s"], g["w_look"],
                                                                                   g["w_lfp"])))
    for race in ("All", "Black", "White"):
        for sub in (None, "young05", "young617", "wnot", "wemp"):
            key = (race, sub)
            g = {y: get(nres, key, y, "mean q0..q11") for y in ("lfp", "unemp", "emp")}
            hi = g["unemp"]["coef"] + 1.96 * g["unemp"]["se"] if g["unemp"] else np.nan
            rows.append((f"NLSY79 {race}: {NSUBLAB[sub]}", [yn(g["lfp"]), yn(g["unemp"]), yn(g["emp"]), f"{hi:.3f}",
                                                             classify(g["emp"], g["unemp"], g["lfp"])]))
            ROWS.append(dict(dataset="NLSY79", table="classification", design="husband <40 weeks", sample=race,
                             subsample=sub or "", outcome="class", term=classify(g["emp"], g["unemp"], g["lfp"])))
    md += ["## 3. Constraint or preference? Classification by group", "",
           "PSID: mean of tau = +1..+3 of the status outcomes (Table 1-2); NLSY79: mean of quarters 0-11 of the "
           "weekly shares (Table 6). 'up' / 'down' = p < 0.10. Rule: employment up -> insurance; else looking up -> "
           "constraint (search friction binds); else participation up -> participation up; else no response "
           "(neither looking nor employment moves: consistent with choice / norms / childcare, or with too little "
           "power - see the upper 95% bound of the looking effect).", "",
           md_table(["Participation rose?", "Looking rose?", "Employment rose?", "Upper 95% bound, looking",
                     "Classification"], [("", rows)]), "",
           "Caveats to the mechanical rule. (i) 'Wife employed at baseline' is labelled 'constraint' because looking "
           "rises while employment falls: these wives lose jobs (or revert towards the mean: the split conditions "
           "on status at the reference interview, and the pre-period coefficient on employment is -0.04*), so this "
           "is not an added-worker search that fails; the job-loss flow in Table 3 is not significant. (ii) The "
           "PSID status measure ('working now' at the interview) rises while 19's 'any hours in the year' does "
           "not (also on stacks from 1980: 0.008, p=0.61): the response is wives already attached working more "
           "continuously (part-year -> working at the interview; hours +46, p=0.13), not new entrants. (iii) The "
           "wife's weeks / any unemployment in the calendar year rise for Black wives already in the year before "
           "the displacement year (tau = -1: +0.084***), so that rise looks like shocks common to both spouses "
           "(or dating error), not search caused by the displacement.", ""]

    pd.DataFrame(ROWS).to_csv(OUT / "wife_search.csv", index=False)
    (OUT / "wife_search.md").write_text("\n".join(md), encoding="utf-8")
    print("done")


if __name__ == "__main__":
    main()
