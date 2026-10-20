r"""Joint job loss within married couples in the CPS monthly panel (2026-10-17). [Paper A; race-neutral first]

Question: when a husband loses his job, how much more likely is his wife to lose hers in the same month (or within a
few months)? The PSID (23.CorrelatedShocks.py; EVIDENCE rows 3.8-3.13) measures this on annual reports; the CPS basic
monthly survey observes both spouses' labor-force status and the reason for unemployment in the same reference week,
for households in sample for months 1-4 and 13-16 (rotation groups MIS 1-4, then MIS 5-8 one year later).

DATA (downloaded here, sequential requests, retries; raw files are data only -> run this script with `python -I`)
  api.census.gov/data/YYYY/cps/basic/MON, 1994-2023 (2024 lacks GESTFIPS in the API and is not used), two requests per
  month, saved unchanged (header + rows) as csv.gz in IGE/data/ext/cps_couples/ (git-ignored):
    cpl_YYYY_MM.csv.gz  persons with PEMARITL = 1 (married, spouse present) and PRTAGE 20-62
    kid_YYYY_MM.csv.gz  persons with PRTAGE 0-17: identifiers, line number, age, parent line(s)
  Variables requested (VARS / KIDVARS below); a variable the API does not have for that month is dropped from the
  request (the header of each raw file records what was obtained; the .md lists coverage by year):
    identifiers  HRHHID + HRSAMPLE, HRSERSUF, HUHHNUM (to April 2004) / HRHHID2 (May 2004 on); HRMIS; PULINENO; GESTFIPS
    couple       PESPOUSE (spouse's line number; all years), PEMARITL, PRFAMREL, PRFAMNUM
    person       PESEX, PRTAGE, race PERACE (1994-2002) / PTDTRACE (2003-; 1 = White alone, 2 = Black alone),
                 Hispanic PRHSPNON (1994-2002) / PEHSPNON (2003-), PEEDUCA
    labor force  PEMLR (1-2 employed, 3 on layoff, 4 looking, 5-7 not in labor force), PRUNTYPE (1 job loser on layoff,
                 2 other job loser, 3 temporary job ended, 4 job leaver, 5 re-entrant, 6 new entrant), PRUNEDUR (weeks)
    job          PRMJIND1 / PRMJOCC1 (major industry / occupation of the main job, current or last job for the
                 unemployed: 22 / 14 groups 1994-2002, 14 / 11 groups 2003-), PRDTIND1, PRDTOCC1 (detailed recodes),
                 PEIO1COW (class of worker)
    weights      PWCMPWGT (composite), PWSSWGT (final)
    children     PRCHLD, PRNMCHLD (own children < 18; from 2000 only) and, for every year, children aged 0-17 linked to
                 either spouse through PEPARENT (to 2006) / PEPAR1, PEPAR2 (2007-) -> number of own children and age
                 of the youngest (the measure used).
COUPLES
  A couple = husband (PESEX 1) and wife (PESEX 2) in the same household and month who name each other in PESPOUSE, both
  PEMARITL = 1, both aged 20-60 in the base month. Person link across months: household id(s) + line number + state,
  MIS increases by the calendar gap (k = -2..+3 months within a rotation; MIS j -> j+4 twelve months later), same race
  for both spouses, age change 0-1 (0-2 at twelve months); the couple key is household + both line numbers, so a couple
  is linked when both spouses are present with the same line numbers and still name each other. Base months whose link
  rate to t+k is < 50% (household-ID breaks: 1995 identifier scrambling, the January 1997 API file with about half the
  records, May 2004 identifier change) are dropped for that k and listed in the .md.
EVENTS (person employed in the base month t)
  job loser at t+j = employed at t+j-1 and unemployed at t+j (PEMLR 3-4) with PRUNTYPE 1, 2 or 3 (on layoff, other job
  loser, temporary job ended). Exits to non-participation and quits are not job loss ("wife leaves employment" is
  reported separately). Windows: same month (t+1), within 1 or 2 months after (t+1..t+2, t+1..t+3); the one-year link
  compares status at t and t+12 (MIS j -> j+4).
ESTIMATES (all weighted by the wife's composite weight at m where stated; regressions unweighted LPM, clusters by
  household and two-way household + state where stated)
  1. P(wife becomes a job loser | husband becomes a job loser) vs | husband stays employed; both employed at m.
     Same month (k = 1), within 2, 3 months; one-year link. Implied phi correlation of the two binary events.
  2. LPM wife_jl = a + b husband_jl + controls, with (i) no FE, (ii) year-month FE, (iii) state x year-month FE (does
     the excess survive within the same state and month?), (iv) + same-industry / same-occupation interactions.
  3. Heterogeneity: race, same vs different major industry / occupation, recession vs expansion months (NBER),
     youngest child's age, state.
  4. Placebo / timing: wife's job loss in the months BEFORE his (her transition m-1 -> m, for husbands employed in m-1
     and m who lose the job at m+1), against the same transition of wives whose husbands stay employed.
  5. Added-worker response: wives NOT employed at m; P(employed at m+k) and P(unemployed, i.e. looking or on layoff,
     at m+k), k = 1..3, by whether the husband (employed at m) becomes a job loser at m+1 vs stays employed at m+1.
Nothing here is a randomised design: the excess joint job loss within couples is an association conditional on the
fixed effects listed (state x month absorbs common local shocks; a shared employer / sector remains inside it).
Writes IGE/output/cps_joint_job_loss.csv (every estimate), .md (tables), .png (figure).
"""
import gzip
import importlib.util
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))                 # -I drops the script directory from sys.path

import numpy as np                            # noqa: E402
import pandas as pd                           # noqa: E402

from common import DATA, OUT, stars           # noqa: E402

RAW = DATA / "ext" / "cps_couples"
CACHE = DATA / "cps_couples_panel.pkl"
YEARS = list(range(1994, 2024))
MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]


def _load17():
    """Script 17 (read only): month names, state abbreviations, region map."""
    spec = importlib.util.spec_from_file_location("atlas17", HERE / "17.AtlasFrictions.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ================================================================ 1. download
def req_vars(y, m):
    ids = "HRHHID,HRHHID2" if (y, m) >= (2004, 5) else "HRHHID,HRSAMPLE,HRSERSUF,HUHHNUM"
    race = "PTDTRACE,PEHSPNON" if y >= 2003 else "PERACE,PRHSPNON"
    v = (f"{ids},HRMIS,PULINENO,GESTFIPS,PESPOUSE,PEMARITL,PRFAMREL,PRFAMNUM,PESEX,PRTAGE,{race},PEEDUCA,PEMLR,"
         "PRUNTYPE,PRUNEDUR,PRMJIND1,PRMJOCC1,PRDTIND1,PRDTOCC1,PEIO1COW,PWCMPWGT,PWSSWGT,PRCHLD,PRNMCHLD")
    k = f"{ids},HRMIS,PULINENO,GESTFIPS,PRTAGE,PEPARENT,PEPAR1,PEPAR2"
    return v.split(","), k.split(",")


_AVAIL = {}


def available(y, m):
    """Variables the API lists for this month (fetched only when a request is refused)."""
    if (y, m) not in _AVAIL:
        url = f"https://api.census.gov/data/{y}/cps/basic/{MONTHS[m - 1]}/variables.json"
        _AVAIL[(y, m)] = set(json.loads(urllib.request.urlopen(url, timeout=300).read())["variables"])
    return _AVAIL[(y, m)]


def fetch(y, m, kind):
    f = RAW / f"{kind}_{y}_{m:02d}.csv.gz"
    if f.exists():
        return "cached"
    cv, kv = req_vars(y, m)
    vs = cv if kind == "cpl" else kv
    pred = "&PEMARITL=1&PRTAGE=20:62" if kind == "cpl" else "&PRTAGE=0:17"
    key = os.environ.get("CENSUS_API_KEY", "")
    err, rows = "", None
    for attempt in range(5):
        url = (f"https://api.census.gov/data/{y}/cps/basic/{MONTHS[m - 1]}?get={','.join(vs)}{pred}"
               + (f"&key={key}" if key else ""))
        try:
            rows = json.loads(urllib.request.urlopen(url, timeout=900).read())
            break
        except urllib.error.HTTPError as e:            # never print the URL or the exception text (key)
            err = f"HTTP {e.code}"
            if e.code == 400:                          # unknown variable: drop what the month does not have
                try:
                    av = available(y, m)
                    vs2 = [v for v in vs if v in av]
                    if len(vs2) < len(vs):
                        vs = vs2
                        continue
                except Exception:                      # noqa: BLE001
                    pass
            if e.code == 404:
                return "not available (404)"
        except Exception as e:                         # noqa: BLE001
            err = type(e).__name__
        time.sleep(15 * (attempt + 1))
    if rows is None:
        return f"FAILED ({err})"
    tmp = f.with_suffix(".tmp")
    with gzip.open(tmp, "wt", newline="") as fh:
        for r in rows:
            fh.write(",".join("" if x is None else str(x) for x in r) + "\n")
    tmp.replace(f)
    return f"{len(rows) - 1} rows, {len(vs)} vars"


def download():
    RAW.mkdir(parents=True, exist_ok=True)
    for y in YEARS:
        for m in range(1, 13):
            for kind in ("cpl", "kid"):
                print(y, m, kind, fetch(y, m, kind), flush=True)


# ================================================================ 2. couples panel
def _hash(s):
    return pd.util.hash_array(np.asarray(s, dtype=object))


def _num(d, c, fill=-1):
    if c not in d:
        return pd.Series(fill, index=d.index, dtype="int64")
    return pd.to_numeric(d[c], errors="coerce").fillna(fill)


def _idkey(d):
    idc = [c for c in ("HRHHID", "HRHHID2", "HRSAMPLE", "HRSERSUF", "HUHHNUM") if c in d]
    return d[idc + ["GESTFIPS"]].astype(str).agg("|".join, axis=1)


def read_month(y, m):
    """Couples (husband + wife naming each other, both married spouse present, both 20-60) in month (y, m)."""
    f = RAW / f"cpl_{y}_{m:02d}.csv.gz"
    if not f.exists():
        return None
    d = pd.read_csv(f, dtype=str, keep_default_na=False)
    hk = _idkey(d)
    race = "PTDTRACE" if "PTDTRACE" in d else "PERACE"
    hisp = "PEHSPNON" if "PEHSPNON" in d else "PRHSPNON"
    lfs, unt = _num(d, "PEMLR"), _num(d, "PRUNTYPE")
    s = np.select([lfs.isin([1, 2]), lfs.isin([3, 4]) & unt.isin([1, 2, 3]), lfs.isin([3, 4]), lfs.isin([5, 6, 7])],
                  [1, 2, 3, 4], 0)
    w = pd.to_numeric(d["PWCMPWGT"], errors="coerce") if "PWCMPWGT" in d else pd.Series(np.nan, index=d.index)
    w = w.where(w > 0, pd.to_numeric(d.get("PWSSWGT", pd.Series(np.nan, index=d.index)), errors="coerce"))

    def code(c, hi):                               # valid recode 1..hi, else -1 (1994 files carry 127 for NIU)
        x = _num(d, c)
        return x.where((x >= 1) & (x <= hi), -1)
    p = pd.DataFrame({
        "hkey": hk, "line": _num(d, "PULINENO"), "sp": _num(d, "PESPOUSE"), "sex": _num(d, "PESEX"),
        "age": _num(d, "PRTAGE"), "mar": _num(d, "PEMARITL"), "mis": _num(d, "HRMIS"), "state": _num(d, "GESTFIPS"),
        "race": _num(d, race), "hisp": (_num(d, hisp) == 1).astype(int), "edu": _num(d, "PEEDUCA"), "s": s,
        "unt": unt, "dur": _num(d, "PRUNEDUR"), "ind": code("PRMJIND1", 30), "occ": code("PRMJOCC1", 20),
        "dind": code("PRDTIND1", 60), "docc": code("PRDTOCC1", 60), "cow": code("PEIO1COW", 8), "w": w})
    p = p[(p.mar == 1) & p.age.between(20, 60) & (p.sp > 0)]
    h, wf = p[p.sex == 1], p[p.sex == 2]
    c = h.merge(wf, left_on=["hkey", "sp"], right_on=["hkey", "line"], suffixes=("_h", "_w"))
    c = c[(c.sp_w == c.line_h) & (c.mis_h == c.mis_w)]
    c = c.drop_duplicates(["hkey", "line_h"], keep=False).drop_duplicates(["hkey", "line_w"], keep=False)
    # own children 0-17 of either spouse (parent line PEPARENT / PEPAR1 / PEPAR2)
    nk, yk = np.zeros(len(c), int), np.full(len(c), -1)
    fk = RAW / f"kid_{y}_{m:02d}.csv.gz"
    if fk.exists() and len(c):
        k = pd.read_csv(fk, dtype=str, keep_default_na=False)
        k = pd.DataFrame({"hkey": _idkey(k), "kline": _num(k, "PULINENO"), "kage": _num(k, "PRTAGE"),
                          **{pc: _num(k, pc) for pc in ("PEPARENT", "PEPAR1", "PEPAR2") if pc in k}})
        k = k.melt(id_vars=["hkey", "kline", "kage"], value_name="pline").query("pline > 0")
        cc = c[["hkey", "line_h", "line_w"]].reset_index(drop=True).reset_index()
        mk = pd.concat([cc.merge(k, left_on=["hkey", "line_h"], right_on=["hkey", "pline"]),
                        cc.merge(k, left_on=["hkey", "line_w"], right_on=["hkey", "pline"])])
        mk = mk.drop_duplicates(["index", "kline"])
        g = mk.groupby("index").kage.agg(["size", "min"])
        nk[g.index.values], yk[g.index.values] = g["size"].values, g["min"].values
    t = (y - 1994) * 12 + (m - 1)
    out = pd.DataFrame({
        "cid": _hash(c.hkey + "|" + c.line_h.astype(str) + "|" + c.line_w.astype(str)),
        "hh": _hash(c.hkey), "t": np.int16(t), "mis": c.mis_h.astype("int8").values,
        "state": c.state_h.astype("int8").values, "w": c.w_w.astype("float32").values,
        "nkid": np.clip(nk, 0, 20).astype("int8"), "ykid": yk.astype("int8")})
    for v, typ in (("age", "int8"), ("race", "int8"), ("hisp", "int8"), ("edu", "int8"), ("s", "int8"),
                   ("unt", "int8"), ("ind", "int8"), ("occ", "int8"), ("dind", "int8"), ("docc", "int8"),
                   ("cow", "int8"), ("dur", "int16")):
        for sp_ in ("h", "w"):
            out[f"{sp_}_{v}"] = c[f"{v}_{sp_}"].astype(typ).values
    return out


OFFS = [-2, -1, 1, 2, 3, 12]
LINKV = ["h_s", "w_s", "h_unt", "w_unt"]
MIN_MATCH = 0.5


def build_panel(years=YEARS, cache=CACHE):
    """Couple-month base rows with both spouses' status at offsets OFFS (-1 = not linked / ID break)."""
    if cache.exists():
        return pd.read_pickle(cache)
    parts = []
    for y in years:
        for m in range(1, 13):
            r = read_month(y, m)
            if r is not None:
                parts.append(r)
        print("read", y, flush=True)
    P = pd.concat(parts, ignore_index=True)
    del parts
    P = P.drop_duplicates(["cid", "t"], keep=False)
    L = P[["cid", "t", "mis", "h_age", "w_age", "h_race", "w_race"] + LINKV]
    rates = []
    for k in OFFS:
        Lk = L.rename(columns={c: f"{c}_k" for c in L.columns if c not in ("cid", "t")}).copy()
        Lk["t"] = (Lk["t"] - k).astype("int16")
        mm = P[["cid", "t", "mis", "h_age", "w_age", "h_race", "w_race"]].merge(Lk, on=["cid", "t"], how="left")
        dm = 4 if k == 12 else k
        da = mm.h_age_k - mm.h_age if k > 0 else mm.h_age - mm.h_age_k
        dw = mm.w_age_k - mm.w_age if k > 0 else mm.w_age - mm.w_age_k
        amax = 2 if k == 12 else 1
        ok = ((mm.mis_k == mm.mis + dm) & da.between(0, amax) & dw.between(0, amax)
              & (mm.h_race_k == mm.h_race) & (mm.w_race_k == mm.w_race)).to_numpy(copy=True)
        if k == 12:
            elig = P.mis.between(1, 4).values
        elif k > 0:
            elig = (P.mis.between(1, 4 - k) | P.mis.between(5, 8 - k)).values
        else:
            elig = (P.mis.between(1 - k, 4) | P.mis.between(5 - k, 8)).values
        rt = pd.DataFrame({"t": P.t.values, "ok": ok & elig, "el": elig}).groupby("t")[["ok", "el"]].sum()
        rt["rate"] = rt.ok / rt.el.where(rt.el > 0)
        rt["k"] = k
        rates.append(rt.reset_index())
        bad = set(rt.index[rt.rate < MIN_MATCH])
        ok = ok & ~P.t.isin(bad).to_numpy()
        for v in LINKV:
            P[f"{v}{k:+d}"] = np.where(ok, mm[f"{v}_k"].fillna(-1).values, -1).astype("int8")
        del mm, Lk
    P.attrs["rates"] = pd.concat(rates, ignore_index=True)
    P.to_pickle(cache)
    return P


# ================================================================ 3. estimation helpers
def demean(a, codes, n):
    cnt = np.bincount(codes, minlength=n)
    if a.ndim == 1:
        return a - (np.bincount(codes, weights=a, minlength=n) / np.maximum(cnt, 1))[codes]
    return np.column_stack([demean(a[:, j], codes, n) for j in range(a.shape[1])])


def lpm(df, y, xs, fe=None, clusters=("hh", "state"), extra=None):
    """OLS of y on xs (+ dummies `extra`), absorbing one FE (list of columns, combined); cluster-robust s.e."""
    d = df
    Y = d[y].to_numpy(float)
    X = d[xs].to_numpy(float)
    names = list(xs)
    if extra is not None:
        X = np.column_stack([X, extra.to_numpy(float)])
        names += list(extra.columns)
    if fe:
        codes, uniq = pd.factorize(pd.MultiIndex.from_frame(d[fe]) if len(fe) > 1 else d[fe[0]])
        Y, X = demean(Y, codes, len(uniq)), demean(X, codes, len(uniq))
        nfe = len(uniq)
    else:
        X = np.column_stack([X, np.ones(len(X))])
        names += ["const"]
        nfe = 0
    XtX = X.T @ X
    keep = np.abs(np.diag(XtX)) > 1e-9
    X, names = X[:, keep], [n for n, k in zip(names, keep) if k]
    XtXi = np.linalg.pinv(X.T @ X)
    b = XtXi @ X.T @ Y
    u = Y - X @ b
    N, K = X.shape
    res = {"b": dict(zip(names, b)), "N": N, "nfe": nfe}
    for cl in clusters:
        g, gu = pd.factorize(d[cl])
        G = len(gu)
        S = np.column_stack([np.bincount(g, weights=X[:, j] * u, minlength=G) for j in range(K)])
        V = XtXi @ (S.T @ S) @ XtXi * (G / (G - 1)) * ((N - 1) / (N - K))
        res[f"se_{cl}"] = dict(zip(names, np.sqrt(np.maximum(np.diag(V), 0))))
        res[f"G_{cl}"] = G
    return res


def pval(b, se):
    from scipy.stats import norm
    return 2 * norm.sf(abs(b / se)) if se > 0 else np.nan


def fmt(b, se, nd=3):
    p = pval(b, se)
    pv = "<0.001" if p < 0.001 else f"{p:.3f}"
    return f"{b:.{nd}f}{stars(p)} ({se:.{nd}f}; p={pv})"


def wmean(x, w):
    x, w = np.asarray(x, float), np.asarray(w, float)
    ok = ~np.isnan(x) & ~np.isnan(w)
    return np.sum(x[ok] * w[ok]) / np.sum(w[ok]) if ok.any() else np.nan


def phi(a, b, w):
    """Weighted phi (Pearson) correlation of two 0/1 events."""
    a, b, w = np.asarray(a, float), np.asarray(b, float), np.asarray(w, float)
    pa, pb, pab = wmean(a, w), wmean(b, w), wmean(a * b, w)
    return (pab - pa * pb) / np.sqrt(pa * (1 - pa) * pb * (1 - pb))


NBER = [(2001, 3, 2001, 11), (2007, 12, 2009, 6), (2020, 2, 2020, 4)]


def recession(t):
    r = np.zeros(len(t), bool)
    for y0, m0, y1, m1 in NBER:
        r |= (t >= (y0 - 1994) * 12 + m0 - 1) & (t <= (y1 - 1994) * 12 + m1 - 1)
    return r


# ================================================================ 4. analysis
def add_vars(P):
    P["year"] = (1994 + P.t // 12).astype("int16")
    P["sm"] = (P.state.astype("int32") * 1000 + P.t).astype("int32")             # state x year-month
    P["smi"] = P.sm.astype("int64") * 100 + P.w_ind.astype("int64")             # x wife's major industry
    P["rec"] = recession(P.t.values).astype("int8")
    P["covid"] = ((P.t >= (2020 - 1994) * 12 + 2) & (P.t <= (2021 - 1994) * 12 + 11)).astype("int8")
    P["black"] = (P.h_race == 2).astype("int8")
    P["rgrp"] = np.select([P.h_race == 2, P.h_race == 1], ["Black", "White"], "Other")
    P["same_ind"] = ((P.h_ind == P.w_ind) & (P.h_ind > 0)).astype("int8")
    P["same_occ"] = ((P.h_occ == P.w_occ) & (P.h_occ > 0)).astype("int8")
    P["same_dind"] = ((P.h_dind == P.w_dind) & (P.h_dind > 0)).astype("int8")
    P["kidg"] = np.select([P.ykid < 0, P.ykid <= 5], ["no child <18", "youngest 0-5"], "youngest 6-17")
    P["private"] = (P.h_cow.isin([4, 5]) & P.w_cow.isin([4, 5])).astype("int8")
    P["period"] = pd.cut(P.year, [1993, 2000, 2007, 2013, 2019, 2021, 2023],
                         labels=["1994-2000", "2001-07", "2008-13", "2014-19", "2020-21", "2022-23"]).astype(str)

    def edu(e):
        return np.select([e <= 38, e == 39, e <= 42], [0, 1, 2], 3)
    P["h_edg"], P["w_edg"] = edu(P.h_edu), edu(P.w_edu)
    return P


def controls(d):
    """Dummies: age groups and education of each spouse, husband's race, youngest child group."""
    c = {}
    for sp_ in ("h", "w"):
        ag = pd.cut(d[f"{sp_}_age"], [19, 29, 39, 49, 60]).cat.codes
        for j in (1, 2, 3):
            c[f"{sp_}_age{j}"] = (ag == j).astype("int8")
        for j in (1, 2, 3):
            c[f"{sp_}_ed{j}"] = (d[f"{sp_}_edg"] == j).astype("int8")
    c["black"] = d.black
    c["other_race"] = (d.rgrp == "Other").astype("int8")
    c["kid05"] = (d.kidg == "youngest 0-5").astype("int8")
    c["kid617"] = (d.kidg == "youngest 6-17").astype("int8")
    return pd.DataFrame(c, index=d.index)


def jl_sample(P, k_after=0, k_before=0):
    """Both employed at t; husband becomes a job loser at t+1 (H=1) or stays employed through t+1+k_after (H=0).
    Requires the couple linked at the offsets used. Outcome columns built by the caller."""
    m = (P.h_s == 1) & (P.w_s == 1) & (P["h_s+1"].isin([1, 2]))
    for j in range(1, k_after + 2):
        m &= P[f"w_s{j:+d}"] >= 1
        if j >= 2:
            m &= (P["h_s+1"] == 2) | (P[f"h_s{j:+d}"] == 1)
            m &= P[f"h_s{j:+d}"] >= 1
    d = P[m].copy()
    d["H"] = (d["h_s+1"] == 2).astype("int8")
    return d


REG_ROWS = []


def rec(table, sample, outcome, spec, r, x, extra=None):
    se = r["se_hh"][x]
    REG_ROWS.append(dict(table=table, sample=sample, outcome=outcome, spec=spec, regressor=x, coef=r["b"][x],
                         se_hh=se, p_hh=pval(r["b"][x], se), se_state=r["se_state"][x],
                         p_state=pval(r["b"][x], r["se_state"][x]), n=r["N"], clusters_hh=r["G_hh"],
                         clusters_state=r["G_state"], n_fe=r["nfe"], **(extra or {})))


def cellr(r, x):
    """coef*** (s.e. household; p) [state-clustered s.e.; p]"""
    b, se, ss = r["b"][x], r["se_hh"][x], r["se_state"][x]
    ps = pval(b, ss)
    nd = 4 if abs(b) < 0.01 else 3
    return fmt(b, se, nd) + f" [{ss:.{nd}f}; p={'<0.001' if ps < 0.001 else f'{ps:.3f}'}]"


def coverage():
    """Variables obtained (header of each raw couples / kids file), summarised by year."""
    rows = []
    for y in YEARS:
        got, nmon = {}, 0
        for m in range(1, 13):
            for kind in ("cpl", "kid"):
                f = RAW / f"{kind}_{y}_{m:02d}.csv.gz"
                if f.exists():
                    with gzip.open(f, "rt") as fh:
                        hdr = set(fh.readline().strip().split(","))
                    want = req_vars(y, m)[0 if kind == "cpl" else 1]
                    for v in want:
                        got.setdefault(v, [0, 0])
                        got[v][0] += 1
                        got[v][1] += v in hdr
                    nmon += kind == "cpl"
        if not nmon:
            continue
        miss = sorted(v for v, (a, b) in got.items() if b == 0)
        part = sorted(v for v, (a, b) in got.items() if 0 < b < a)
        rows.append(dict(year=y, months=nmon, missing=", ".join(miss) or "-", partial=", ".join(part) or "-"))
    return pd.DataFrame(rows)


def panel_cells(d, y, w="w"):
    """Weighted outcome means for H = 0 / 1 and counts."""
    a, b = d[d.H == 0], d[d.H == 1]
    return dict(p0=wmean(a[y], a[w]), p1=wmean(b[y], b[w]), n=len(d), n1=len(b), n11=int(b[y].sum()))


def main(years=YEARS, cache=CACHE, tag=""):
    OUT.mkdir(exist_ok=True)
    m17 = _load17()
    P = add_vars(build_panel(years, cache))
    rates = P.attrs.get("rates")
    md = ["# Joint job loss within married couples: CPS monthly panel\n",
          f"Built by `IGE/30.CPSJointJobLoss.py` (2026-10-17; definitions in its docstring). CPS basic monthly "
          f"{min(years)}-{max(years)} from the Census API; married couples (both spouses married-spouse-present, naming "
          "each other as spouse, both aged 20-60 at t) linked month to month within the 4-month rotation and from MIS "
          "1-4 to MIS 5-8 twelve months later. **Job loser** = unemployed (on layoff or looking) with PRUNTYPE = job "
          "loser on layoff / other job loser / temporary job ended, after being employed the month before. "
          "Probabilities are weighted by the wife's composite weight at t; regressions are unweighted linear "
          "probability models. Cells: coefficient*** (s.e. clustered by household; p) [s.e. clustered by state; p]; "
          "*** p<0.01, ** p<0.05, * p<0.1. Households are nested in states, so two-way household x state clustering "
          "equals state clustering. Associations, not causal effects: state x month fixed effects absorb common local "
          "shocks; a shared employer or sector remains inside the estimate by design.\n"]
    # ---------------- 0. data
    cov = coverage()
    md.append("## 0. Data\n")
    md.append("Variables requested but not offered by the API (from the raw-file headers; 'part of the year' = missing "
              "in some months). The requested list is in `req_vars()`.\n")
    md.append("| Year | Months | Missing all year | Missing part of the year |\n|---|---|---|---|")
    for r in cov.itertuples():
        md.append(f"| {r.year} | {r.months} | {r.missing} | {r.partial} |")
    md.append("")
    md.append(f"Couple-months: {len(P):,}; distinct couples (household + both line numbers): {P.cid.nunique():,}; "
              f"months: {P.t.nunique()}. Share Black (husband): {P.black.mean():.3f}; both employed at t: "
              f"{((P.h_s == 1) & (P.w_s == 1)).mean():.3f}.\n")
    if rates is not None:
        tmax = P.t.max()
        r1 = rates[(rates.k == 1) & (rates.t < tmax)].set_index("t").rate.dropna()
        bad = r1[r1 < MIN_MATCH]
        r12 = rates[(rates.k == 12) & (rates.t <= tmax - 12)].set_index("t").rate.dropna()
        for r in rates.itertuples():
            REG_ROWS.append(dict(table="0_link_rates", sample=f"{1994 + r.t // 12}-{r.t % 12 + 1:02d}",
                                 outcome=f"link rate t -> t{r.k:+d}", coef=r.rate, n=r.el))
        lab = lambda t: f"{1994 + t // 12}-{t % 12 + 1:02d}"           # noqa: E731
        md.append(f"Link rate t -> t+1 (couples in MIS 1-3 / 5-7 found as the same couple next month): median "
                  f"{r1.median():.3f}, 10th percentile {r1.quantile(0.1):.3f}. Base months dropped (link rate < "
                  f"{MIN_MATCH}; household-ID breaks): {', '.join(lab(t) for t in bad.index) or 'none'}. Twelve-month "
                  f"link (MIS j -> j+4): median {r12.median():.3f}; base months with a usable twelve-month link (rate "
                  f">= {MIN_MATCH}): {int((r12 >= MIN_MATCH).sum())} of {len(r12)} (the 1994-95 sample redesign, the "
                  f"1995 and 2004 identifier changes and the January 1997 API file, which has about half the usual "
                  f"records, break links).\n")
    # ---------------- 1. windows
    W0 = jl_sample(P, 0)
    W0["y"] = (W0["w_s+1"] == 2).astype("int8")
    W0["ysep"] = W0["w_s+1"].isin([2, 3, 4]).astype("int8")
    W1 = jl_sample(P, 1)
    W1["y"] = ((W1["w_s+1"] == 2) | ((W1["w_s+1"] == 1) & (W1["w_s+2"] == 2))).astype("int8")
    W2 = jl_sample(P, 2)
    W2["y"] = ((W2["w_s+1"] == 2) | ((W2["w_s+1"] == 1) & (W2["w_s+2"] == 2))
               | ((W2["w_s+2"] == 1) & (W2["w_s+3"] == 2))).astype("int8")
    A12 = P[(P.h_s == 1) & (P.w_s == 1) & P["h_s+12"].isin([1, 2]) & (P["w_s+12"] >= 1)].copy()
    A12["H"] = (A12["h_s+12"] == 2).astype("int8")
    A12["y"] = (A12["w_s+12"] == 2).astype("int8")
    ALL0 = P[(P.h_s == 1) & (P.w_s == 1) & (P["h_s+1"] >= 1) & (P["w_s+1"] >= 1)]
    phi_all = phi(ALL0["h_s+1"] == 2, ALL0["w_s+1"] == 2, ALL0.w)
    wins = [("Same month (t+1)", W0), ("Within 1 month after (t+1..t+2)", W1),
            ("Within 2 months after (t+1..t+3)", W2), ("One year later (MIS j -> j+4, status at t+12)", A12)]
    dw = dict(wins)
    md.append("## 1. Joint job loss: wife's job-loss probability by the husband's transition\n")
    md.append("Both spouses employed at t. H = 1: husband becomes a job loser at t+1; H = 0: husband stays employed "
              "(through the end of the window). Wife's event: becomes a job loser in the window (from employment). The "
              "one-year column compares statuses at t and t+12 (12-month link; transitions in between are not observed). "
              "Regression row: LPM of the wife's event on H with state x year-month fixed effects.\n")
    md.append("| | " + " | ".join(f"({i + 1}) {n}" for i, (n, _) in enumerate(wins)) + " |")
    md.append("|---" * (len(wins) + 1) + "|")
    cells = {n: panel_cells(d, "y") for n, d in wins}
    regs = {n: lpm(d, "y", ["H"], fe=["sm"]) for n, d in wins}
    for n, d in wins:
        c = cells[n]
        rec("1_windows", "all", n, "state x ym FE", regs[n], "H",
            dict(p0=c["p0"], p1=c["p1"], n1=c["n1"], n11=c["n11"], phi=phi(d.H, d.y, d.w)))
    rows = [("P(wife job loser \\| husband job loser)", lambda n: f"{cells[n]['p1']:.4f}"),
            ("P(wife job loser \\| husband stays employed)", lambda n: f"{cells[n]['p0']:.4f}"),
            ("Difference", lambda n: f"{cells[n]['p1'] - cells[n]['p0']:.4f}"),
            ("Ratio", lambda n: f"{cells[n]['p1'] / cells[n]['p0']:.1f}"),
            ("P(husband job loser)", lambda n: f"{wmean(dw[n].H, dw[n].w):.4f}"),
            ("Phi correlation of the two events (this sample)", lambda n: f"{phi(dw[n].H, dw[n].y, dw[n].w):.3f}"),
            ("Regression: husband job loser (state x ym FE)", lambda n: cellr(regs[n], "H")),
            ("N couples (H = 0 + H = 1)", lambda n: f"{cells[n]['n']:,}"),
            ("N husband job losers / joint events", lambda n: f"{cells[n]['n1']:,} / {cells[n]['n11']:,}"),
            ("Clusters: households / states", lambda n: f"{regs[n]['G_hh']:,} / {regs[n]['G_state']}")]
    for lab_, f in rows:
        md.append(f"| {lab_} | " + " | ".join(f(n) for n, _ in wins) + " |")
    md.append("")
    pj = wmean((ALL0["h_s+1"] == 2) & (ALL0["w_s+1"] == 2), ALL0.w)
    pi = wmean(ALL0["h_s+1"] == 2, ALL0.w) * wmean(ALL0["w_s+1"] == 2, ALL0.w)
    md.append(f"Phi correlation of the same-month events among all couples employed at t (husband's other transitions "
              f"kept): {phi_all:.3f}. Joint same-month job-loss rate: observed {pj:.6f} vs {pi:.6f} under independence "
              f"(ratio {pj / pi:.1f}).\n")
    REG_ROWS.append(dict(table="1_windows", sample="all couples both employed", outcome="phi same month",
                         coef=phi_all, p1=pj, p0=pi, n=len(ALL0)))
    # ---------------- 2. regressions
    md.append("## 2. Does the excess survive local shocks? Same-month joint job loss with fixed effects\n")
    md.append("Sample: column (1) of section 1. Controls: age group (20-29/30-39/40-49/50-60) and education (<HS, HS, "
              "some college, BA+) of each spouse, husband's race, youngest own child (none / 0-5 / 6-17). Same industry "
              "/ occupation: equal major group of the main job at t (14 / 11 groups from 2003, 22 / 14 before).\n")
    ctl = controls(W0)
    nc = (W0.covid == 0).values
    W0["H_si"], W0["H_so"] = W0.H * W0.same_ind, W0.H * W0.same_occ
    specs = [("(1) none", dict(xs=["H"], fe=None, extra=None, d=W0)),
             ("(2) year-month FE", dict(xs=["H"], fe=["t"], extra=None, d=W0)),
             ("(3) state x year-month FE", dict(xs=["H"], fe=["sm"], extra=None, d=W0)),
             ("(4) (3) + controls", dict(xs=["H"], fe=["sm"], extra=ctl, d=W0)),
             ("(5) state x ym x wife's industry FE + controls", dict(xs=["H"], fe=["smi"], extra=ctl, d=W0)),
             ("(6) (4) + same industry / occupation", dict(xs=["H", "H_si", "H_so", "same_ind", "same_occ"],
                                                         fe=["sm"], extra=ctl, d=W0)),
             ("(7) (4), excluding 2020-21", dict(xs=["H"], fe=["sm"], extra=ctl[nc], d=W0[nc]))]
    xl = {"H": "Husband becomes job loser (t+1)", "H_si": "x same major industry", "H_so": "x same major occupation",
          "same_ind": "Same major industry", "same_occ": "Same major occupation"}
    for outc, olab in (("y", "Wife becomes job loser at t+1"), ("ysep", "Wife leaves employment at t+1 (any)")):
        res = {}
        for sn, s in specs:
            res[sn] = lpm(s["d"], outc, s["xs"], fe=s["fe"], extra=s["extra"])
            for x in s["xs"]:
                rec("2_fe", "all", olab, sn, res[sn], x)
        md.append(f"**Outcome: {olab}**\n")
        md.append("| | " + " | ".join(sn for sn, _ in specs) + " |")
        md.append("|---" * (len(specs) + 1) + "|")
        for x in ["H", "H_si", "H_so", "same_ind", "same_occ"]:
            md.append(f"| {xl[x]} | " + " | ".join(cellr(res[sn], x) if x in res[sn]["b"] else ""
                                                  for sn, _ in specs) + " |")
        md.append("| Fixed effects | none | year-month | state x ym | state x ym | state x ym x wife's major industry "
                  "| state x ym | state x ym |")
        md.append("| Controls | no | no | no | yes | yes | yes | yes |")
        md.append("| Mean of outcome, H = 0 (unweighted) | " + " | ".join(
            f"{s['d'].loc[s['d'].H == 0, outc].mean():.4f}" for _, s in specs) + " |")
        md.append("| N / FE groups | " + " | ".join(f"{res[sn]['N']:,} / {res[sn]['nfe']:,}" for sn, _ in specs)
                  + " |")
        md.append("| Clusters: households / states | " + " | ".join(
            f"{res[sn]['G_hh']:,} / {res[sn]['G_state']}" for sn, _ in specs) + " |")
        md.append("")
    # ---------------- 3. heterogeneity
    md.append("## 3. Heterogeneity (state x year-month FE within each sample)\n")
    md.append("Row panels are samples; each column is a separate regression of the outcome in its header on H with state "
              "x year-month FE. Means are weighted. 'His job loss: type' compares husbands with that type of job loss "
              "with husbands who stay employed.\n")
    outs = [("Wife job loser, same month", W0, "y"), ("Wife job loser within 2 months after", W2, "y"),
            ("Wife leaves employment, same month", W0, "ysep")]
    allr = lambda d: np.ones(len(d), bool)                                # noqa: E731
    groups = [("All", allr), ("Black couples (husband's race)", lambda d: d.rgrp == "Black"),
              ("White couples (husband's race)", lambda d: d.rgrp == "White"),
              ("Same major industry", lambda d: d.same_ind == 1),
              ("Different major industry (both known)", lambda d: (d.same_ind == 0) & (d.h_ind > 0) & (d.w_ind > 0)),
              ("Same major occupation", lambda d: d.same_occ == 1),
              ("Different major occupation (both known)",
               lambda d: (d.same_occ == 0) & (d.h_occ > 0) & (d.w_occ > 0)),
              ("Same detailed industry", lambda d: d.same_dind == 1),
              ("Both private wage and salary workers", lambda d: d.private == 1),
              ("NBER recession months", lambda d: d.rec == 1), ("Expansion months", lambda d: d.rec == 0),
              ("Excluding 2020-21", lambda d: d.covid == 0),
              ("No own child < 18", lambda d: d.kidg == "no child <18"),
              ("Youngest child 0-5", lambda d: d.kidg == "youngest 0-5"),
              ("Youngest child 6-17", lambda d: d.kidg == "youngest 6-17")]
    groups += [(f"Period {p}", (lambda p: lambda d: d.period == p)(p))
               for p in ["1994-2000", "2001-07", "2008-13", "2014-19", "2020-21", "2022-23"]]
    types = [("His job loss: on layoff (PRUNTYPE 1)", 1), ("His job loss: other job loser (2)", 2),
             ("His job loss: temporary job ended (3)", 3)]
    md.append("| | " + " | ".join(f"({i + 1}) {o}" for i, (o, _, _) in enumerate(outs)) + " |")
    md.append("|---" * (len(outs) + 1) + "|")

    def hrow(name, sel_fn, typ=None):
        cl, mn, nn = [], [], []
        for o, d, yv in outs:
            dd = d[np.asarray(sel_fn(d))]
            if typ is not None:
                dd = dd[(dd.H == 0) | (dd["h_unt+1"] == typ)]
            if dd.H.sum() < 20:
                cl.append("n/a"), mn.append(""), nn.append(f"{len(dd):,}")
                continue
            r = lpm(dd, yv, ["H"], fe=["sm"])
            c = panel_cells(dd, yv)
            rec("3_heterogeneity", name, o, "state x ym FE", r, "H",
                dict(p0=c["p0"], p1=c["p1"], n1=c["n1"], n11=c["n11"]))
            cl.append(cellr(r, "H"))
            mn.append(f"{c['p0']:.4f} / {c['p1']:.4f}")
            nn.append(f"{c['n']:,} / {c['n1']:,}")
        md.append(f"| **{name}** | | | |")
        md.append("| Husband becomes job loser | " + " | ".join(cl) + " |")
        md.append("| Mean H = 0 / H = 1 | " + " | ".join(mn) + " |")
        md.append("| N / N(H = 1) | " + " | ".join(nn) + " |")
    for name, f in groups:
        hrow(name, f)
    for name, typ in types:
        hrow(name, allr, typ)
    md.append("| Fixed effects | state x ym | state x ym | state x ym |\n")
    md.append("**Differences across groups** (pooled LPM, outcome = wife job loser in the same month, state x ym FE; "
              "regressors H, group, H x group)\n")
    md.append("| Interaction | Coefficient on H x group | H (reference group) | N |\n|---|---|---|---|")
    inter = [("Black (vs White)", W0[W0.rgrp != "Other"].assign(g=lambda d: (d.rgrp == "Black").astype(int))),
             ("Same major industry", W0.assign(g=W0.same_ind)), ("Same major occupation", W0.assign(g=W0.same_occ)),
             ("Same detailed industry", W0.assign(g=W0.same_dind)), ("Recession month", W0.assign(g=W0.rec)),
             ("Youngest child 0-5 (vs none / older)", W0.assign(g=(W0.kidg == "youngest 0-5").astype(int))),
             ("2020-21", W0.assign(g=W0.covid))]
    for name, d in inter:
        d = d.assign(Hg=d.H * d.g)
        r = lpm(d, "y", ["H", "Hg", "g"], fe=["sm"])
        if "Hg" not in r["b"]:
            continue
        rec("3b_interactions", name, "Wife job loser, same month", "state x ym FE", r, "Hg")
        rec("3b_interactions", name + " (reference H)", "Wife job loser, same month", "state x ym FE", r, "H")
        md.append(f"| {name} | {cellr(r, 'Hg')} | {cellr(r, 'H')} | {r['N']:,} |")
    md.append("")
    st = []
    for s_, d in W0.groupby("state"):
        if d.H.sum() < 30:
            continue
        r = lpm(d, "y", ["H"], fe=["t"], clusters=("hh",))
        st.append(dict(state=int(s_), abbr=m17.ABBR.get(int(s_), str(s_)), b=r["b"]["H"], se=r["se_hh"]["H"],
                       n=r["N"], n1=int(d.H.sum())))
    st = pd.DataFrame(st)
    if len(st):
        st["p"] = [pval(b, s) for b, s in zip(st.b, st.se)]
        wi = 1 / st.se ** 2
        bbar = np.average(st.b, weights=wi)
        excess_var = np.average((st.b - bbar) ** 2, weights=wi) - np.average(st.se ** 2, weights=wi)
        for r in st.itertuples():
            REG_ROWS.append(dict(table="3c_state", sample=r.abbr, outcome="Wife job loser, same month",
                                 spec="year-month FE", regressor="H", coef=r.b, se_hh=r.se, p_hh=r.p, n=r.n, n1=r.n1))
        md.append(f"**By state** (year-month FE, household clusters; states with >= 30 husband job losers: {len(st)}): "
                  f"median coefficient {st.b.median():.3f}, interquartile range {st.b.quantile(.25):.3f} to "
                  f"{st.b.quantile(.75):.3f}; positive in {int((st.b > 0).sum())} states, p < 0.05 in "
                  f"{int((st.p < 0.05).sum())}. Precision-weighted mean {bbar:.3f}; weighted variance of the state "
                  f"estimates minus mean sampling variance: {excess_var:.5f} (<= 0: dispersion no larger than sampling "
                  f"noise). State rows in the csv (table 3c_state).\n")
    yr = []
    for y_, d in W0.groupby("year"):
        c = panel_cells(d, "y")
        yr.append(dict(year=int(y_), p0=c["p0"], p1=c["p1"], n1=c["n1"], ph=wmean(d.H, d.w)))
    yr = pd.DataFrame(yr)
    for r in yr.itertuples():
        REG_ROWS.append(dict(table="3d_year", sample=str(r.year), outcome="Wife job loser, same month",
                             spec="weighted means", regressor="H", p0=r.p0, p1=r.p1, n1=r.n1, coef=r.p1 - r.p0))
    # ---------------- 4. timing / placebo
    md.append("## 4. Timing and placebo: the wife's monthly job-loss hazard around the husband's job-loss month\n")
    md.append("tau = month in which the husband is observed becoming a job loser (employed at tau-1). Column j: the "
              "wife's hazard of becoming a job loser in month tau+j (employed at tau+j-1). Controls: husbands employed "
              "at tau-1 and tau and in every other month of the window. Negative j is the placebo: if couples merely "
              "share a high job-loss propensity, her hazard is already elevated before his job loss. Each column is a "
              "separate sample (the CPS observes at most 4 consecutive months).\n")
    b = (P.h_s == 1) & P["h_s+1"].isin([1, 2])
    Hm = P["h_s+1"] == 2
    ev = {-2: P[b & (P["h_s-2"] == 1) & (P["h_s-1"] == 1) & (P["w_s-2"] == 1) & (P["w_s-1"] >= 1)].assign(
              y=lambda d: (d["w_s-1"] == 2).astype("int8")),
          -1: P[b & (P["h_s-1"] == 1) & (P["w_s-1"] == 1)].assign(y=lambda d: (d.w_s == 2).astype("int8")),
          0: P[b & (P.w_s == 1) & (P["w_s+1"] >= 1)].assign(y=lambda d: (d["w_s+1"] == 2).astype("int8")),
          1: P[b & (P["w_s+1"] == 1) & (P["w_s+2"] >= 1) & (P["h_s+2"] >= 1) & (Hm | (P["h_s+2"] == 1))].assign(
              y=lambda d: (d["w_s+2"] == 2).astype("int8")),
          2: P[b & (P["w_s+2"] == 1) & (P["w_s+3"] >= 1) & (P["h_s+2"] >= 1) & (P["h_s+3"] >= 1)
               & (Hm | ((P["h_s+2"] == 1) & (P["h_s+3"] == 1)))].assign(y=lambda d: (d["w_s+3"] == 2).astype("int8"))}
    for j in ev:
        ev[j] = ev[j].assign(H=lambda d: (d["h_s+1"] == 2).astype("int8"))
    js = sorted(ev)
    md.append("| | " + " | ".join(f"({i + 1}) wife job loser at tau{j:+d}" for i, j in enumerate(js)) + " |")
    md.append("|---" * (len(js) + 1) + "|")
    evres = {}
    for pn, fe in (("A. state x year-month FE", ["sm"]), ("B. no fixed effects", None)):
        md.append(f"| **{pn}** |" + " |" * len(js))
        rr = {j: lpm(ev[j], "y", ["H"], fe=fe) for j in js}
        if fe:
            evres = rr
        for j in js:
            c = panel_cells(ev[j], "y")
            rec("4_timing", f"j={j:+d}", f"wife job loser at tau{j:+d}", pn, rr[j], "H",
                dict(p0=c["p0"], p1=c["p1"], n1=c["n1"], n11=c["n11"]))
        md.append("| Husband job loser at tau | " + " | ".join(cellr(rr[j], "H") for j in js) + " |")
        md.append("| N / clusters (households) | " + " | ".join(f"{rr[j]['N']:,} / {rr[j]['G_hh']:,}" for j in js)
                  + " |")
    md.append("| Mean H = 0 / H = 1 (weighted) | " + " | ".join(
        "{p0:.4f} / {p1:.4f}".format(**panel_cells(ev[j], "y")) for j in js) + " |")
    md.append("| N husband job losers | " + " | ".join(f"{int(ev[j].H.sum()):,}" for j in js) + " |\n")
    # ---------------- 5. added worker
    md.append("## 5. The wife's response: added-worker transitions of non-employed wives\n")
    md.append("Wives not employed at t (unemployed or out of the labor force), husbands employed at t. H = 1: husband "
              "becomes a job loser at t+1; H = 0: husband employed at t+1 and through t+k. Outcomes at t+k (k = 1, 2, 3 "
              "within the rotation; t+12 at the one-year link, husband's later status unrestricted): wife employed; wife "
              "unemployed (looking or on layoff, PEMLR 3-4). Each column is a separate regression with state x "
              "year-month FE.\n")
    base = (P.h_s == 1) & P.w_s.isin([2, 3, 4]) & P["h_s+1"].isin([1, 2])
    aw = {}
    for k in (1, 2, 3, 12):
        mk = base & (P[f"w_s{k:+d}"] >= 1)
        if k != 12:
            for j in range(2, k + 1):
                mk &= (P[f"h_s{j:+d}"] >= 1) & ((P["h_s+1"] == 2) | (P[f"h_s{j:+d}"] == 1))
        aw[k] = P[mk].assign(H=lambda d: (d["h_s+1"] == 2).astype("int8"),
                             emp=lambda d, k=k: (d[f"w_s{k:+d}"] == 1).astype("int8"),
                             une=lambda d, k=k: d[f"w_s{k:+d}"].isin([2, 3]).astype("int8"))
    acols = [(k, o) for o in ("emp", "une") for k in (1, 2, 3, 12)]
    alab = {"emp": "employed", "une": "unemployed"}
    md.append("| | " + " | ".join(f"({i + 1}) wife {alab[o]} at t+{k}" for i, (k, o) in enumerate(acols)) + " |")
    md.append("|---" * (len(acols) + 1) + "|")
    agroups = [("All", allr), ("Black couples", lambda d: d.rgrp == "Black"),
               ("White couples", lambda d: d.rgrp == "White"),
               ("Youngest child 0-5", lambda d: d.kidg == "youngest 0-5"),
               ("Youngest child 6-17", lambda d: d.kidg == "youngest 6-17"),
               ("No own child < 18", lambda d: d.kidg == "no child <18"),
               ("Wife out of the labor force at t", lambda d: d.w_s == 4),
               ("Wife unemployed at t", lambda d: d.w_s.isin([2, 3])),
               ("Black, youngest child 0-5", lambda d: (d.rgrp == "Black") & (d.kidg == "youngest 0-5")),
               ("White, youngest child 0-5", lambda d: (d.rgrp == "White") & (d.kidg == "youngest 0-5")),
               ("Excluding 2020-21", lambda d: d.covid == 0)]
    awres = {}
    for name, f in agroups:
        cl, mn, nn = [], [], []
        for k, o in acols:
            dd = aw[k][np.asarray(f(aw[k]))]
            if dd.H.sum() < 20:
                cl.append("n/a"), mn.append(""), nn.append(f"{len(dd):,}")
                continue
            r = lpm(dd, o, ["H"], fe=["sm"])
            c = panel_cells(dd, o)
            awres[(name, k, o)] = (r, c)
            rec("5_added_worker", name, f"wife {alab[o]} at t+{k}", "state x ym FE", r, "H",
                dict(p0=c["p0"], p1=c["p1"], n1=c["n1"]))
            cl.append(cellr(r, "H"))
            mn.append(f"{c['p0']:.3f} / {c['p1']:.3f}")
            nn.append(f"{c['n']:,} / {c['n1']:,}")
        md.append(f"| **{name}** |" + " |" * len(acols))
        md.append("| Husband becomes job loser (t+1) | " + " | ".join(cl) + " |")
        md.append("| Mean H = 0 / H = 1 (weighted) | " + " | ".join(mn) + " |")
        md.append("| N / N(H = 1) | " + " | ".join(nn) + " |")
    md.append("| Fixed effects | " + " | ".join("state x ym" for _ in acols) + " |\n")
    # ---------------- 6. PSID comparison
    md.append("## 6. Comparison with the PSID (EVIDENCE rows 3.8-3.10)\n")
    c0, c2, cA = cells[wins[0][0]], cells[wins[2][0]], cells[wins[3][0]]
    rB = [r for r in REG_ROWS if r["table"] == "3_heterogeneity"]
    get = lambda s, o: next((r for r in rB if r["sample"] == s and r["outcome"] == o), None)   # noqa: E731
    md.append("| | PSID (annual reports, 23.CorrelatedShocks.py) | CPS (this script) |\n|---|---|---|")
    md.append(f"| Wife's job loss when the husband loses his vs not | B +0.080*** on base 0.090 (ratio ~1.9); W "
              f"+0.070*** on 0.058 (~2.2); window ev-1..ev+1 | same month {c0['p1']:.4f} vs {c0['p0']:.4f} (ratio "
              f"{c0['p1'] / c0['p0']:.1f}); within 2 months {c2['p1']:.4f} vs {c2['p0']:.4f} (ratio "
              f"{c2['p1'] / c2['p0']:.1f}); one year {cA['p1']:.4f} vs {cA['p0']:.4f} (ratio "
              f"{cA['p1'] / cA['p0']:.1f}) |")
    for s, lab_ in (("Black couples (husband's race)", "Black"), ("White couples (husband's race)", "White")):
        for o in ("Wife job loser, same month", "Wife job loser within 2 months after"):
            r = get(s, o)
            if r:
                md.append(f"| {lab_}: {o.lower()} | | {r['coef']:.4f}{stars(r['p_hh'])} (s.e. {r['se_hh']:.4f}); "
                          f"means H=0 / H=1 {r['p0']:.4f} / {r['p1']:.4f} (ratio {r['p1'] / r['p0']:.1f}) |")
    rs = [r for r in REG_ROWS if r["table"] == "3b_interactions" and r["sample"] == "Same major industry"
          and r["regressor"] == "Hg"]
    if rs:
        r = rs[0]
        md.append(f"| Same-sector couples, extra | +0.124*** (0.041) | same major industry x H: {r['coef']:.4f}"
                  f"{stars(r['p_hh'])} ({r['se_hh']:.4f}) |")
    md.append("")
    md.append("PSID figures are probabilities over a three-year window around an annual displacement report (closures "
              "and layoffs, recalled); CPS figures are monthly transitions into unemployment for job-loss reasons (same "
              "month or within two months), so levels differ by construction and only ratios are comparable in "
              "spirit.\n")
    (OUT / f"cps_joint_job_loss{tag}.md").write_text("\n".join(md), encoding="utf-8")
    out = pd.DataFrame(REG_ROWS)
    out["stars"] = out["p_hh"].map(lambda p: stars(p) if pd.notna(p) else "") if "p_hh" in out else ""
    out.to_csv(OUT / f"cps_joint_job_loss{tag}.csv", index=False)
    plot(ev, yr, awres, OUT / f"cps_joint_job_loss{tag}.png")
    print("\n".join(md))


# ================================================================ 5. figure
def plot(ev, yr, awres, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ink, ink2, grid, surf = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    blue, orange = "#2a78d6", "#eb6834"
    fig, axs = plt.subplots(1, 3, figsize=(14, 5.2), facecolor=surf)
    for ax in axs:
        ax.set_facecolor(surf)
        ax.grid(color=grid, lw=0.8)
        ax.set_axisbelow(True)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        for sp in ("left", "bottom"):
            ax.spines[sp].set_color(grid)
        ax.tick_params(colors=ink2, labelsize=8)
    ax = axs[0]
    js = sorted(ev)
    cc = {j: panel_cells(ev[j], "y") for j in js}
    ax.plot(js, [100 * cc[j]["p1"] for j in js], color=blue, lw=2, marker="o", ms=7,
            label="husband becomes job loser at tau")
    ax.plot(js, [100 * cc[j]["p0"] for j in js], color=orange, lw=2, marker="o", ms=7,
            label="husband stays employed")
    ax.axvline(0, color=ink2, lw=0.8, ls=":")
    ax.set_xticks(js)
    ax.set_xlabel("month relative to husband's job loss (tau)", color=ink2)
    ax.set_ylabel("wife's monthly job-loss hazard (%)", color=ink2)
    ax.set_title("A. Wife's job loss around his", fontsize=10, color=ink, loc="left")
    ax.legend(frameon=False, fontsize=8, labelcolor=ink2)
    ax = axs[1]
    for y0, m0, y1, m1 in NBER:
        ax.axvspan(y0 + (m0 - 1) / 12, y1 + m1 / 12, color=grid, alpha=0.9, lw=0)
    ax.plot(yr.year + 0.5, 100 * yr.p1, color=blue, lw=2, marker="o", ms=4, label="husband becomes job loser")
    ax.plot(yr.year + 0.5, 100 * yr.p0, color=orange, lw=2, marker="o", ms=4, label="husband stays employed")
    ax.set_yscale("log")
    from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator
    ax.yaxis.set_major_locator(FixedLocator([0.2, 0.3, 0.5, 1, 2, 3, 5, 10, 20, 30, 50]))
    ax.yaxis.set_minor_locator(NullLocator())
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
    ax.set_xlabel("year (shaded: NBER recessions)", color=ink2)
    ax.set_ylabel("P(wife becomes job loser, same month), % (log)", color=ink2)
    ax.set_title("B. Same-month joint job loss by year", fontsize=10, color=ink, loc="left")
    ax.legend(frameon=False, fontsize=8, labelcolor=ink2)
    ax = axs[2]
    ks = [1, 2, 3]
    for o, ls, nm in (("emp", "-", "employed"), ("une", "--", "unemployed")):
        kk = [k for k in ks if ("All", k, o) in awres]
        ax.plot(kk, [100 * awres[("All", k, o)][1]["p1"] for k in kk], color=blue, lw=2, ls=ls, marker="o", ms=7,
                label=f"{nm}: husband job loser")
        ax.plot(kk, [100 * awres[("All", k, o)][1]["p0"] for k in kk], color=orange, lw=2, ls=ls, marker="o",
                ms=7, label=f"{nm}: husband employed")
    ax.set_xticks(ks)
    ax.set_xlabel("months after t (husband's job loss at t+1)", color=ink2)
    ax.set_ylabel("% of wives not employed at t", color=ink2)
    ax.set_title("C. Non-employed wives: added-worker transitions", fontsize=10, color=ink, loc="left")
    ax.legend(frameon=False, fontsize=7.5, labelcolor=ink2, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2)
    fig.text(0.01, 0.005, "CPS basic monthly (Census API), married couples aged 20-60, wife's composite weight. Job "
             "loser = unemployed with reason job loser / on layoff / temporary job ended, after employment. "
             "Associations, not causal effects.", fontsize=7.5, color=ink2)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(path, dpi=160, facecolor=surf)
    plt.close(fig)


if __name__ == "__main__":
    if "--download-only" in sys.argv:
        download()
    elif "--test" in sys.argv:                     # development run on the years downloaded so far
        yrs = [y for y in YEARS if (RAW / f"cpl_{y}_12.csv.gz").exists()]
        main(yrs, DATA / "cps_couples_panel_test.pkl", "_test")
    else:
        download()
        main()
