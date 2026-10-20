r"""Joint displacement of spouses in the CPS Displaced Worker Supplement 1984-2024 (2026-10-17). [Paper A]

Question: is the joint job loss of spouses (PSID reason-for-job-end, 25.JointJobLoss.py; CPS basic monthly,
30.CPSJointJobLoss.py) also present in the large-sample, REASON-based survey of job loss, the CPS Displaced Worker
Supplement (DWS)? Referee plan item 4 (proposals/fable_review_paperA.md).

DATA (IPUMS CPS extract through the IPUMS API; key read from the environment variable IPUMS_API_KEY, never printed)
  21 supplements: January 1984, 1986, 1988, 1990, 1992; February 1994, 1996, 1998, 2000; January 2002-2024 (biennial).
  (IPUMS also lists January 2026 and February 2002, which carry no DW variables.) Case selection MARST = 1 (married,
  spouse present). Raw files (csv.gz + codebooks, unchanged) in IGE/data/ext/cps_dws/ (git-ignored). Variables: VARS.
  DW variables used
    DWSTAT     displaced worker status (IPUMS): 1984-1992 = lost a job in the last FIVE years for any reason
               (plant closed/moved, insufficient work, position/shift abolished, seasonal job ended, self-operated
               business failed, other); 1994-2024 = lost a wage job in the last THREE calendar years because the plant
               closed or moved, there was insufficient work or the position or shift was abolished (the BLS definition)
    DWREAS     reason (codes 1-6); DWLASTWRK years ago the lost job ended (1 = last year ...); DWCLASS class of worker
    DWIND      industry of the lost job (Census code of the survey year's scheme, same scheme as IND within a year
               for 97-100% of codes); DWWKSUN weeks without work after the loss; DWBEN received UI
    DWSUPPWT   supplement weight; DWRESP eligibility / interview status (1996-2024: 2 = interviewed)
HARMONISED MEASURE (a person, the survey of year Y)
  displaced = lost a wage job in calendar years Y-3..Y-1 because the plant closed / moved (reason 1), insufficient work
  (2) or the position or shift was abolished (3). 1994-2024: DWSTAT = 1. 1984-1992: DWSTAT = 1, DWREAS 1-3, DWCLASS not
  self-employed, DWLASTWRK 1-3 (the five-year window cut to three calendar years; losses in January of Y dropped;
  people with an unknown year are dropped). Sub-reasons: plant closing (1) vs insufficient work / position abolished
  (2-3). Displacement year = Y - DWLASTWRK (unknown for 0.5% of 1994-2024 cases, DWLASTWRK 95-98; they count as
  displaced but are left out of the same-year analysis). Seasonal / business-failure / other losses are measured
  only 1984-1992 (row "any job loss, 1984-1992") and are not displacement.
COUPLES
  Husband (SEX 1) and wife (SEX 2) in the same household who point at each other in SPLOC, both MARST 1, both aged
  20-64, both in the supplement (DWSTAT 0/1; DWSTAT 99 = supplement non-interview, 8-15% of persons 1996-2024).
  Attached couples: each spouse is displaced, employed or unemployed (not out of the labor force) at the survey; the
  closest analogue of the "both working" conditioning in the PSID and the CPS monthly panel (it conditions on current
  status, so it is a robustness sample, not the main one).
  RESPONDENT / RECALL. The CPS takes proxy answers from any responsible adult in the household, so the two spouses'
  supplement answers usually come from the same respondent at the same interview; the extract carries no self /
  proxy flag (IPUMS has no PROXY variable; the Census PUSLFPRX flag is not used here), so self and proxy reports
  cannot be separated. Recall: three calendar years, displacement year in whole years ("years ago"); one job per person (the
  longest-held lost job if several). Couples are observed married at the survey: couples who divorced after a
  displacement are missing (the PSID shows divorce rises after the husband's job loss, EVIDENCE 3.6).
ESTIMATES
  1. Weighted shares (wife's DWSUPPWT): P(wife displaced | husband displaced) vs P(wife displaced | husband not
     displaced), by reason; same calendar year on the couple x year panel (each couple contributes Y-3..Y-1).
     Differences: weighted LPM of the wife's event on the husband's event, s.e. clustered by household.
  2. LPMs (unweighted), state x survey-year FE, controls (both spouses' age, age^2, education 4 groups, Black,
     Hispanic), s.e. clustered by household (one couple per household and survey: equals robust) and, in a row, by
     state. Same-industry interaction: spouses' reference industries equal (lost-job industry if displaced, else the
     current / last job's industry), detailed Census code.
  3. Same calendar year: couple x year panel, state x survey-year x calendar-year FE.
  4. Joint plant closings; same-industry share of joint displacements vs the random-pairing benchmark (displaced
     husbands and wives of the same survey paired at random).
  5. Tetrachoric correlation (weighted 2x2; s.e. from 200 bootstrap draws of couples).
  6. Splits: husband Black vs White non-Hispanic; survey years 1984-1998 vs 2000-2024; recession windows (the three
     calendar years of recall contain >= 2 NBER recession months: 1984, 1992, 1994, 2002, 2004, 2010, 2012, 2022) vs
     expansion windows.
  7. What a joint displacement does to the household at the survey (displaced husbands): weeks without work, UI,
     employment of each spouse, neither spouse employed.
  8. Comparison with the PSID (25) and the CPS monthly panel (30).
Associations, not causal effects.
Writes IGE/output/cps_dws_joint_loss.csv (every estimate), .md (tables), .png (figure).
"""
import json
import os
import shutil
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))                 # -I drops the script directory from sys.path

import numpy as np                            # noqa: E402
import pandas as pd                           # noqa: E402
from scipy import stats                       # noqa: E402
from scipy.integrate import quad              # noqa: E402
from scipy.optimize import brentq             # noqa: E402

from common import DATA, OUT, stars           # noqa: E402

RAW = DATA / "ext" / "cps_dws"
SAMPLES = {1984: 1, 1986: 1, 1988: 1, 1990: 1, 1992: 1, 1994: 2, 1996: 2, 1998: 2, 2000: 2, 2002: 1, 2004: 1,
           2006: 1, 2008: 1, 2010: 1, 2012: 1, 2014: 1, 2016: 1, 2018: 1, 2020: 1, 2022: 1, 2024: 1}
VARS = ("YEAR,SERIAL,MONTH,CPSID,CPSIDP,STATEFIP,PERNUM,WTFINL,RELATE,AGE,SEX,RACE,HISPAN,MARST,SPLOC,EDUC,EMPSTAT,"
        "LABFORCE,CLASSWKR,IND,OCC,IND1990,OCC1990,NCHILD,YNGCH,DWSTAT,DWREAS,DWRECALL,DWLASTWRK,DWYEARS,DWFULLTIME,"
        "DWNOTICE,DWCLASS,DWUNION,DWHI,DWWEEKL,DWWAGEL,DWWEEKC,DWWAGEC,DWHRSWKC,DWBEN,DWEXBEN,DWJOBSINCE,DWWKSUN,"
        "DWMOVE,DWIND,DWOCC,DWRESP,DWSUPPWT").split(",")
DESC = "Selection vs risk IGE: CPS Displaced Worker Supplements 1984-2026, married spouse present"
API = "https://api.ipums.org/extracts"
NBER = [(1980, 1, 1980, 7), (1981, 7, 1982, 11), (1990, 7, 1991, 3), (2001, 3, 2001, 11), (2007, 12, 2009, 6),
        (2020, 2, 2020, 4)]          # peak, trough; recession months = (peak, trough]
REPS = 200


# ================================================================ 1. data
def _api(url, body=None):
    key = os.environ.get("IPUMS_API_KEY")
    if not key:
        raise SystemExit("IPUMS_API_KEY is not set")
    req = urllib.request.Request(url, data=None if body is None else json.dumps(body).encode(),
                                 headers={"Authorization": key, "Content-Type": "application/json"},
                                 method="GET" if body is None else "POST")
    return urllib.request.urlopen(req, timeout=600)


def fetch():
    """Newest IPUMS csv.gz in RAW; otherwise reuse a matching extract of the account or submit one, wait, download."""
    have = sorted(RAW.glob("cps_*.csv.gz"))
    if have:
        return have[-1]
    RAW.mkdir(parents=True, exist_ok=True)
    samples = {f"cps{y}_{m:02d}s": {} for y, m in SAMPLES.items()}
    hist = json.load(_api(f"{API}?collection=cps&version=2&pageSize=50"))["data"]
    num = None
    for e in hist:
        df = e.get("extractDefinition", {})
        if set(df.get("samples", {})) == set(samples) and set(VARS) <= set(df.get("variables", {})) \
                and e.get("status") == "completed" and "data" in e.get("downloadLinks", {}):
            num = e["number"]
            break
    if num is None:
        body = {"description": DESC, "dataStructure": {"rectangular": {"on": "P"}}, "dataFormat": "csv",
                "samples": samples, "variables": {v: {} for v in VARS}, "caseSelectWho": "individuals"}
        body["variables"]["MARST"] = {"caseSelections": {"general": ["1"]}}
        num = json.load(_api(f"{API}?collection=cps&version=2", body))["number"]
        print("submitted IPUMS CPS extract", num, flush=True)
    for _ in range(240):
        e = json.load(_api(f"{API}/{num}?collection=cps&version=2"))
        if e["status"] == "completed":
            break
        if e["status"] in ("failed", "canceled"):
            raise SystemExit(f"extract {num} {e['status']}")
        time.sleep(60)
    out = None
    for k, v in e["downloadLinks"].items():
        if k in ("data", "basicCodebook", "ddiCodebook"):
            fn = RAW / v["url"].split("/")[-1]
            with _api(v["url"]) as resp, open(fn, "wb") as fh:
                shutil.copyfileobj(resp, fh)
            out = fn if k == "data" else out
    return out


def valid_ind(x, year):
    x = pd.to_numeric(x, errors="coerce")
    ok = (x > 0) & np.where(year <= 2002, x < 990, x < 9900)
    return x.where(ok)


def persons(d):
    """Harmonised displacement measures and covariates, one row per person."""
    early = d.YEAR <= 1992
    lw = d.DWLASTWRK
    o = pd.DataFrame({"year": d.YEAR, "serial": d.SERIAL, "pernum": d.PERNUM, "sploc": d.SPLOC, "sex": d.SEX,
                      "state": d.STATEFIP, "age": d.AGE, "wt": d.DWSUPPWT}, index=d.index)
    o["insupp"] = d.DWSTAT.isin([0, 1])
    rs = d.DWREAS.between(1, 3) & (d.DWSTAT == 1)
    e_disp = rs & (d.DWCLASS != 4)
    disp = np.where(early, e_disp & lw.between(1, 3), d.DWSTAT == 1).astype(float)
    disp[(early & e_disp & ~lw.between(0, 5)).to_numpy()] = np.nan          # early years, unknown year
    o["disp"] = disp
    o.loc[~o["insupp"], "disp"] = np.nan
    o["dyear"] = np.where((o["disp"] == 1) & lw.between(1, 3), d.YEAR - lw, np.nan)
    o["close"] = np.where(o["disp"].isna(), np.nan, (o["disp"] == 1) & (d.DWREAS == 1))
    o["slack"] = np.where(o["disp"].isna(), np.nan, (o["disp"] == 1) & d.DWREAS.isin([2, 3]))
    o["anyjl"] = np.where(early & o["insupp"], (d.DWSTAT == 1) & d.DWREAS.between(1, 6) & lw.between(1, 3), np.nan)
    o.loc[early & (d.DWSTAT == 1) & ~lw.between(0, 5), "anyjl"] = np.nan
    o["dind"] = valid_ind(d.DWIND, d.YEAR).where(o["disp"] == 1)
    o["ind"] = valid_ind(d.IND, d.YEAR)
    o["emp"] = d.EMPSTAT.isin([1, 10, 12]).astype(float)
    o["unemp"] = d.EMPSTAT.isin([20, 21, 22]).astype(float)
    o["attached"] = ((o["disp"] == 1) | (o["emp"] == 1) | d.EMPSTAT.isin([20, 21])).astype(float)
    o["refind"] = o["dind"].where(o["disp"] == 1, o["ind"].where((o["emp"] == 1) | (o["unemp"] == 1)))
    o["wksun"] = d.DWWKSUN.where((o["disp"] == 1) & (d.DWWKSUN < 990))
    o["ui"] = np.where((o["disp"] == 1) & d.DWBEN.isin([1, 2]), (d.DWBEN == 2).astype(float), np.nan)
    ed = d.EDUC
    o["edu"] = np.select([ed.between(2, 71), ed.isin([72, 73]), ed.between(80, 100), ed.between(110, 125)],
                         [1, 2, 3, 4], 0)                    # 0 = missing
    o["black"] = (d.RACE == 200).astype(float)
    o["hisp"] = d.HISPAN.between(1, 899).astype(float)
    o["whitenh"] = ((d.RACE == 100) & (d.HISPAN == 0)).astype(float)
    return o


def couples(path):
    d = pd.read_csv(path)
    flow = {"persons in extract (MARST 1)": len(d)}
    d = d[d["MONTH"] == d["YEAR"].map(SAMPLES)]
    flow["persons in the 21 DWS months"] = len(d)
    p = persons(d[(d.MARST == 1) & (d.SPLOC > 0) & d.SEX.isin([1, 2])])
    h = p[p.sex == 1].add_prefix("h_")
    w = p[p.sex == 2].add_prefix("w_")
    c = h.merge(w, left_on=["h_year", "h_serial", "h_sploc"], right_on=["w_year", "w_serial", "w_pernum"])
    c = c[c.w_sploc == c.h_pernum].copy()
    c["year"], c["state"] = c.h_year, c.h_state
    c["hh"] = c.year * 100000 + c.h_serial
    flow["couples (husband and wife name each other)"] = len(c)
    c = c[c.h_age.between(20, 64) & c.w_age.between(20, 64)]
    flow["both aged 20-64"] = len(c)
    flow["  husband not in supplement (DWSTAT 99)"] = int((~c.h_insupp).sum())
    flow["  wife not in supplement (DWSTAT 99)"] = int((~c.w_insupp).sum())
    c = c[c.h_insupp & c.w_insupp]
    flow["both in supplement"] = len(c)
    c = c.dropna(subset=["h_disp", "w_disp"])
    flow["displacement known for both (analysis sample)"] = len(c)
    c["stateyr"] = c.state * 10000 + c.year
    c["period"] = np.where(c.year <= 1998, "1984-1998", "2000-2024")
    c["recwin"] = c.year.map(recession_window)
    c["w"] = c.w_wt
    for s in ("h", "w"):
        c[f"{s}_age2"] = c[f"{s}_age"] ** 2 / 100
        for k in (1, 3, 4, 0):
            c[f"{s}_edu{k}"] = (c[f"{s}_edu"] == k).astype(float)
    c["both_att"] = ((c.h_attached == 1) & (c.w_attached == 1)).astype(float)
    c["same_ind"] = np.where(c.h_refind.notna() & c.w_refind.notna(), (c.h_refind == c.w_refind).astype(float),
                             np.nan)
    c["hd_x_same"] = c.h_disp * c.same_ind
    c["h_nodisp"] = 1 - c.h_disp
    return c.reset_index(drop=True), flow


def recession_window(y):
    """Number of NBER recession months in calendar years y-3..y-1 >= 2."""
    lo, hi = (y - 3) * 12, (y - 1) * 12 + 11
    n = 0
    for y0, m0, y1, m1 in NBER:
        a, b = y0 * 12 + m0, y1 * 12 + m1 - 1        # (peak, trough] in 0-based month index
        n += max(0, min(b, hi) - max(a, lo) + 1)
    return "recession" if n >= 2 else "expansion"


def couple_years(c):
    """Couple x calendar year panel (Y-3..Y-1); couples with a displaced spouse of unknown year are dropped."""
    k = c[~(((c.h_disp == 1) & c.h_dyear.isna()) | ((c.w_disp == 1) & c.w_dyear.isna()))]
    rows = []
    for j in (1, 2, 3):
        t = k.copy()
        t["cy"] = t.year - j
        for s in ("h", "w"):
            t[f"{s}_y"] = (t[f"{s}_dyear"] == t.cy).astype(float)
            t[f"{s}_oth"] = ((t[f"{s}_disp"] == 1) & (t[f"{s}_dyear"] != t.cy)).astype(float)
            t[f"{s}_cly"] = t[f"{s}_y"] * t[f"{s}_close"]
            t[f"{s}_sly"] = t[f"{s}_y"] * t[f"{s}_slack"]
            t[f"{s}_clo"] = t[f"{s}_oth"] * t[f"{s}_close"]
            t[f"{s}_slo"] = t[f"{s}_oth"] * t[f"{s}_slack"]
        rows.append(t)
    p = pd.concat(rows, ignore_index=True)
    p["fe3"] = p.stateyr * 10 + (p.year - p.cy)
    return p


# ================================================================ 2. estimators
def demean(a, codes, n):
    cnt = np.bincount(codes, minlength=n)
    if a.ndim == 1:
        return a - (np.bincount(codes, weights=a, minlength=n) / np.maximum(cnt, 1))[codes]
    return np.column_stack([demean(a[:, j], codes, n) for j in range(a.shape[1])])


CTRL = [f"{s}_{v}" for s in ("h", "w") for v in ("age", "age2", "edu1", "edu3", "edu4", "edu0", "black", "hisp")]


def lpm(df, y, xs, fe=None, controls=False, weight=None, clusters=("hh", "state")):
    """OLS / WLS of y on xs (+ CTRL), one absorbed FE; cluster-robust s.e. by each column in `clusters`."""
    cols = list(xs) + (CTRL if controls else [])
    d = df.dropna(subset=[y] + cols)
    Y, X = d[y].to_numpy(float), d[cols].to_numpy(float)
    wv = d[weight].to_numpy(float) if weight else np.ones(len(d))
    names = list(cols)
    if fe:
        codes, uniq = pd.factorize(d[fe])
        if weight:                       # weighted within transformation
            sw = np.bincount(codes, weights=wv, minlength=len(uniq))
            mY = np.bincount(codes, weights=wv * Y, minlength=len(uniq)) / sw
            Y = Y - mY[codes]
            X = np.column_stack([X[:, j] - (np.bincount(codes, weights=wv * X[:, j], minlength=len(uniq))
                                            / sw)[codes] for j in range(X.shape[1])])
        else:
            Y, X = demean(Y, codes, len(uniq)), demean(X, codes, len(uniq))
    else:
        X = np.column_stack([X, np.ones(len(X))])
        names += ["const"]
    sq = np.sqrt(wv)
    Xw, Yw = X * sq[:, None], Y * sq
    keep = np.abs(np.diag(Xw.T @ Xw)) > 1e-9
    X, Xw, names = X[:, keep], Xw[:, keep], [n for n, k in zip(names, keep) if k]
    XtXi = np.linalg.pinv(Xw.T @ Xw)
    b = XtXi @ Xw.T @ Yw
    u = Y - X @ b
    N, K = X.shape
    res = {"b": dict(zip(names, b)), "N": N, "se": {}, "p": {}}
    for cl in clusters:
        g, gu = pd.factorize(d[cl])
        G = len(gu)
        S = np.column_stack([np.bincount(g, weights=X[:, j] * wv * u, minlength=G) for j in range(K)])
        V = XtXi @ (S.T @ S) @ XtXi * (G / (G - 1)) * ((N - 1) / max(N - K, 1))
        se = np.sqrt(np.maximum(np.diag(V), 0))
        res["se"][cl] = dict(zip(names, se))
        res["p"][cl] = {n: pval(bb, s) for n, bb, s in zip(names, b, se)}
        res[f"G_{cl}"] = G
    return res


def pval(b, se):
    return 2 * stats.norm.sf(abs(b / se)) if se > 0 else np.nan


def fmt(b, se, nd=3):
    p = pval(b, se)
    pv = "p<0.001" if p < 0.001 else f"p={p:.3f}"
    return f"{b:.{nd}f}{stars(p)} ({se:.{nd}f}; {pv})"


def wmean(x, w):
    x, w = np.asarray(x, float), np.asarray(w, float)
    ok = ~np.isnan(x) & ~np.isnan(w)
    return np.sum(x[ok] * w[ok]) / np.sum(w[ok]) if ok.any() else np.nan


def bvn(a, b, r):
    s = np.sqrt(1 - r * r)
    return quad(lambda x: stats.norm.pdf(x) * stats.norm.cdf((b - r * x) / s), -np.inf, a, epsabs=1e-12)[0]


def tetra(n11, n10, n01, n00):
    N = n11 + n10 + n01 + n00
    ph, pw, p11 = (n11 + n10) / N, (n11 + n01) / N, n11 / N
    if n11 <= 0 or min(ph, pw) <= 0:
        return np.nan
    a, b = stats.norm.ppf(ph), stats.norm.ppf(pw)
    try:
        return brentq(lambda r: bvn(a, b, r) - p11, -0.95, 0.99, xtol=1e-6)
    except ValueError:
        return np.nan


def tetra_boot(df, h, w, unit="hh", wt="w", reps=REPS, seed=39):
    """Weighted tetrachoric correlation of two 0/1 events; s.e. from a bootstrap over `unit`."""
    d = df.dropna(subset=[h, w])
    ww = d[wt].to_numpy(float)
    hv, wv = d[h].to_numpy(float), d[w].to_numpy(float)
    cell = np.column_stack([ww * hv * wv, ww * hv * (1 - wv), ww * (1 - hv) * wv, ww * (1 - hv) * (1 - wv)])
    g, gu = pd.factorize(d[unit])
    C = np.column_stack([np.bincount(g, weights=cell[:, j], minlength=len(gu)) for j in range(4)])
    est = tetra(*C.sum(0))
    rng = np.random.default_rng(seed)
    bs = []
    for _ in range(reps):
        cnt = np.bincount(rng.integers(0, len(gu), len(gu)), minlength=len(gu))
        bs.append(tetra(*(C * cnt[:, None]).sum(0)))
    se = np.nanstd(bs, ddof=1)
    n11 = int(((hv == 1) & (wv == 1)).sum())
    return est, se, n11, len(d)


# ================================================================ 3. analysis
REC = []


def rec(table, sample, outcome, spec, term, b, se, n, base=np.nan, p=None, extra=""):
    REC.append(dict(table=table, sample=sample, outcome=outcome, spec=spec, term=term, b=b, se=se,
                    p=pval(b, se) if p is None else p, N=n, base=base, note=extra))


def cell(r, x, cl="hh"):
    if x not in r["b"]:
        return ""
    return fmt(r["b"][x], r["se"][cl][x])


def shares(c, p, sample="all couples"):
    """Table 1: weighted conditional probabilities."""
    out = []
    specs = [("Displaced (any of reasons 1-3)", "h_disp", "w_disp", c, "h_nodisp"),
             ("Plant closed or moved (reason 1), both", "h_close", "w_close", c, "h_nodisp"),
             ("Insufficient work / position abolished (2-3), both", "h_slack", "w_slack", c, "h_nodisp"),
             ("Wife displaced, husband's plant closed", "h_close", "w_disp", c, "h_nodisp"),
             ("Wife plant closing, husband displaced", "h_disp", "w_close", c, "h_nodisp")]
    early = c[c.year <= 1992].dropna(subset=["h_anyjl", "w_anyjl"]).assign(h_nojl=lambda t: 1 - t.h_anyjl)
    specs.append(("Any job loss incl. seasonal / business failed / other (1984-1992)", "h_anyjl", "w_anyjl",
                  early, "h_nojl"))
    for lab, h, w, d, ref in specs:
        s = d[(d[h] == 1) | (d[ref] == 1)]
        p1, p0 = wmean(s.loc[s[h] == 1, w], s.loc[s[h] == 1, "w"]), wmean(s.loc[s[h] == 0, w], s.loc[s[h] == 0, "w"])
        r = lpm(s, w, [h], weight="w", clusters=("hh",))
        b, se = r["b"][h], r["se"]["hh"][h]
        out.append(dict(lab=lab, p1=p1, p0=p0, b=b, se=se, n=len(s), nh=int((s[h] == 1).sum()),
                        n11=int(((s[h] == 1) & (s[w] == 1)).sum())))
        rec("1 shares", sample, w, f"weighted; P(w|{h}) vs P(w|husband not displaced)", h, b, se, len(s), p0,
            extra=f"P(w|h)={p1:.4f}")
    # same calendar year, couple-year panel
    for lab, h, w, ref in (("Same calendar year: displaced (couple-years)", "h_y", "w_y", "h_nodisp"),
                           ("Same calendar year: plant closing, both (couple-years)", "h_cly", "w_cly", "h_nodisp")):
        s = p[(p[h] == 1) | (p[ref] == 1)]
        p1, p0 = wmean(s.loc[s[h] == 1, w], s.loc[s[h] == 1, "w"]), wmean(s.loc[s[h] == 0, w], s.loc[s[h] == 0, "w"])
        r = lpm(s, w, [h], weight="w", clusters=("hh",))
        b, se = r["b"][h], r["se"]["hh"][h]
        out.append(dict(lab=lab, p1=p1, p0=p0, b=b, se=se, n=len(s), nh=int((s[h] == 1).sum()),
                        n11=int(((s[h] == 1) & (s[w] == 1)).sum())))
        rec("1 shares", sample + " (couple-years)", w, "weighted; P(w_y|h_y) vs P(w_y|husband not displaced)", h,
            b, se, len(s), p0, extra=f"P(w|h)={p1:.4f}")
    return out


def main_lpm(c, sample):
    """Table 2: one regression per column."""
    fe = "stateyr"
    cols = [("Wife displaced", "w_disp", ["h_disp"], None, False, None),
            ("Wife displaced", "w_disp", ["h_disp"], fe, False, None),
            ("Wife displaced", "w_disp", ["h_disp"], fe, True, None),
            ("Wife plant closing", "w_close", ["h_close", "h_slack"], fe, True, None),
            ("Wife insufficient work / abolished", "w_slack", ["h_close", "h_slack"], fe, True, None),
            ("Wife displaced", "w_disp", ["h_disp", "hd_x_same", "same_ind"], fe, True, "same_ind")]
    res = []
    for j, (lab, y, xs, f, ctl, need) in enumerate(cols, 1):
        d = c if need is None else c.dropna(subset=[need])
        r = lpm(d, y, xs, fe=f, controls=ctl)
        base = d.loc[d.h_disp == 0, y].mean()
        res.append((lab, y, xs, f, ctl, r, base))
        for x in xs:
            rec("2 LPM", sample, y, f"col {j}; FE={f}; controls={ctl}", x, r["b"][x], r["se"]["hh"][x], r["N"], base,
                extra=f"state-clustered se {r['se']['state'][x]:.4f}")
    return res


def het(c, p, sample_lab, mask_c, mask_p):
    """Table 3 cells for one sample: three regressions (one per outcome)."""
    out = {}
    cc, pp = c[mask_c], p[mask_p]
    r = lpm(cc, "w_disp", ["h_disp"], fe="stateyr", controls=True)
    out["disp"] = (r, "h_disp", cc.loc[cc.h_disp == 0, "w_disp"].mean())
    r = lpm(cc, "w_close", ["h_close", "h_slack"], fe="stateyr", controls=True)
    out["close"] = (r, "h_close", cc.loc[cc.h_disp == 0, "w_close"].mean())
    r = lpm(pp, "w_y", ["h_y", "h_oth"], fe="fe3", controls=True)
    out["same"] = (r, "h_y", pp.loc[pp.h_disp == 0, "w_y"].mean())
    for k, (r, x, base) in out.items():
        rec("3 heterogeneity", sample_lab, k, "FE + controls", x, r["b"][x], r["se"]["hh"][x], r["N"], base)
    return out


def interaction(c, p, g, lab):
    """H x G coefficient (pooled, common FE and controls) for the three outcomes."""
    out = {}
    cc = c.assign(hxg=c.h_disp * c[g], cxg=c.h_close * c[g])
    pp = p.assign(hxg=p.h_y * p[g], oxg=p.h_oth * p[g])
    gx = [] if g in CTRL else [g]
    r = lpm(cc, "w_disp", ["h_disp", "hxg", *gx], fe="stateyr", controls=True)
    out["disp"] = (r, "hxg")
    r = lpm(cc, "w_close", ["h_close", "cxg", "h_slack", *gx], fe="stateyr", controls=True)
    out["close"] = (r, "cxg")
    r = lpm(pp, "w_y", ["h_y", "hxg", "h_oth", "oxg", *gx], fe="fe3", controls=True)
    out["same"] = (r, "hxg")
    for k, (r, x) in out.items():
        rec("3 heterogeneity", f"difference: {lab}", k, "pooled, H x group", x, r["b"][x], r["se"]["hh"][x], r["N"])
    return out


def timing(p, sample):
    cols = [("Wife displaced in year y", "w_y", ["h_y", "h_oth"]),
            ("Wife plant closing in year y", "w_cly", ["h_cly", "h_sly", "h_clo", "h_slo"])]
    res = []
    for j, (lab, y, xs) in enumerate(cols, 1):
        r = lpm(p, y, xs, fe="fe3", controls=True)
        base = p.loc[p.h_disp == 0, y].mean()
        res.append((lab, xs, r, base))
        for x in xs:
            rec("4 same year", sample, y, f"col {j}; state x survey x year FE + controls", x, r["b"][x],
                r["se"]["hh"][x], r["N"], base, extra=f"state-clustered se {r['se']['state'][x]:.4f}")
    return res


def industry(c):
    """Same detailed lost-job industry among joint displacements vs random pairing within the survey."""
    out = []
    jd = c[(c.h_disp == 1) & (c.w_disp == 1) & c.h_dind.notna() & c.w_dind.notna()]
    defs = [("Both displaced (any year)", jd),
            ("Both displaced, same year", jd[jd.h_dyear == jd.w_dyear]),
            ("Both plant closings", jd[(jd.h_close == 1) & (jd.w_close == 1)]),
            ("Both plant closings, same year", jd[(jd.h_close == 1) & (jd.w_close == 1) & (jd.h_dyear == jd.w_dyear)])]
    dh = c[(c.h_disp == 1) & c.h_dind.notna()]
    dw = c[(c.w_disp == 1) & c.w_dind.notna()]
    bench = {}
    for y in c.year.unique():
        ph = dh[dh.year == y].groupby("h_dind")["h_wt"].sum()
        pw = dw[dw.year == y].groupby("w_dind")["w_wt"].sum()
        ph, pw = ph / ph.sum(), pw / pw.sum()
        bench[y] = float((ph * pw.reindex(ph.index).fillna(0)).sum())
    for lab, s in defs:
        if len(s) == 0:
            continue
        share = float((s.h_dind == s.w_dind).mean())
        b0 = float(s.year.map(bench).mean())
        se = np.sqrt(share * (1 - share) / len(s))
        out.append(dict(lab=lab, n=len(s), share=share, bench=b0, ratio=share / b0, b=share - b0, se=se))
        rec("5 industry", "joint displacements", "same detailed lost-job industry", lab, "share - random benchmark",
            share - b0, se, len(s), b0, extra=f"share={share:.3f}")
    # context: spouses' current detailed industry (both employed)
    e = c[(c.h_emp == 1) & (c.w_emp == 1) & c.h_ind.notna() & c.w_ind.notna()]
    share = float((e.h_ind == e.w_ind).mean())
    b0s = []
    for y, g in e.groupby("year"):
        ph = g.groupby("h_ind")["h_wt"].sum()
        pw = g.groupby("w_ind")["w_wt"].sum()
        ph, pw = ph / ph.sum(), pw / pw.sum()
        b0s.append(float((ph * pw.reindex(ph.index).fillna(0)).sum()) * len(g))
    b0 = sum(b0s) / len(e)
    se = np.sqrt(share * (1 - share) / len(e))
    out.append(dict(lab="Context: both employed, current job", n=len(e), share=share, bench=b0, ratio=share / b0,
                    b=share - b0, se=se))
    rec("5 industry", "both employed", "same current detailed industry", "context", "share - random benchmark",
        share - b0, se, len(e), b0, extra=f"share={share:.3f}")
    # P(w disp | h disp) by same / different reference industry (weighted)
    s = c.dropna(subset=["same_ind"])
    by = {}
    for v in (1, 0):
        t = s[s.same_ind == v]
        by[v] = (wmean(t.loc[t.h_disp == 1, "w_disp"], t.loc[t.h_disp == 1, "w"]),
                 wmean(t.loc[t.h_disp == 0, "w_disp"], t.loc[t.h_disp == 0, "w"]),
                 int((t.h_disp == 1).sum()), len(t))
    return out, by


def closings(c, p):
    """Table 6: joint plant closings."""
    out = []
    hc = c[c.h_close == 1]
    nd = c[c.h_disp == 0]
    ph = p[p.h_cly == 1]
    pn = p[p.h_disp == 0]
    rows = [("Wife displaced (any reason 1-3), 3-year window", hc, nd, "w_disp"),
            ("Wife plant closing, 3-year window", hc, nd, "w_close"),
            ("Wife displaced in the same year (couple-years)", ph, pn, "w_y"),
            ("Wife plant closing in the same year (couple-years)", ph, pn, "w_cly")]
    for lab, a, b, w in rows:
        p1, p0 = wmean(a[w], a["w"]), wmean(b[w], b["w"])
        s = pd.concat([a.assign(hh_=1), b.assign(hh_=0)])
        r = lpm(s, w, ["hh_"], weight="w", clusters=("hh",))
        out.append(dict(lab=lab, p1=p1, p0=p0, b=r["b"]["hh_"], se=r["se"]["hh"]["hh_"], n1=len(a),
                        n11=int((a[w] == 1).sum())))
        rec("6 closings", "husband plant closing vs not displaced", w, "weighted", "husband plant closing",
            r["b"]["hh_"], r["se"]["hh"]["hh_"], len(s), p0, extra=f"P(w|h close)={p1:.4f}")
    # same year and same detailed industry: the closest proxy for one closure hitting both
    sy = ph[(ph.w_cly == 1)]
    k = int(((sy.h_dind == sy.w_dind) & sy.h_dind.notna()).sum())
    nsy = len(ph.drop_duplicates("hh"))
    share = wmean(((ph.w_cly == 1) & (ph.h_dind == ph.w_dind) & ph.h_dind.notna()).astype(float), ph["w"])
    return out, dict(n_hclose_known_year=nsy, n_joint_same_year=len(sy), n_same_ind=k, share_same_ind=share)


def consequences(c):
    """Table 7: displaced husbands (known year): outcomes at the survey by the wife's displacement."""
    d = c[(c.h_disp == 1) & c.h_dyear.notna() & ~((c.w_disp == 1) & c.w_dyear.isna())].copy()
    d["w_same"] = ((d.w_disp == 1) & (d.w_dyear == d.h_dyear)).astype(float)
    d["w_othy"] = ((d.w_disp == 1) & (d.w_dyear != d.h_dyear)).astype(float)
    d["neither"] = ((d.h_emp == 0) & (d.w_emp == 0)).astype(float)
    outs = [("His weeks without work", "h_wksun"), ("He received UI", "h_ui"), ("He is employed now", "h_emp"),
            ("She is employed now", "w_emp"), ("Neither spouse employed now", "neither")]
    res = []
    for lab, y in outs:
        r = lpm(d, y, ["w_same", "w_othy"], fe="stateyr", controls=True)
        base = d.loc[(d.w_disp == 0), y].mean()
        res.append((lab, r, base))
        for x in ("w_same", "w_othy"):
            rec("7 consequences", "displaced husbands", y, "FE + controls", x, r["b"][x], r["se"]["hh"][x], r["N"],
                base)
    return res, d


# ================================================================ 4. output
def md_table(header, rows):
    s = "| " + " | ".join(header) + " |\n|" + "---|" * len(header) + "\n"
    return s + "".join("| " + " | ".join(str(x) for x in r) + " |\n" for r in rows)


def plot(sh, byyear, ind, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ink, ink2, grid, surf = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    blue, orange = "#2a78d6", "#eb6834"
    fig, axs = plt.subplots(1, 3, figsize=(15, 5.4), facecolor=surf)
    for ax in axs:
        ax.set_facecolor(surf)
        ax.grid(color=grid, lw=0.8, axis="y")
        ax.set_axisbelow(True)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        for sp in ("left", "bottom"):
            ax.spines[sp].set_color(grid)
        ax.tick_params(colors=ink2, labelsize=8)
    ax = axs[0]
    pick = [0, 1, 2, 6, 7]
    labs = ["Displaced\n(3 yrs)", "Plant closing,\nboth", "Slack work /\nabolished, both", "Displaced,\nsame year",
            "Plant closing,\nsame year"]
    x = np.arange(len(pick))
    ax.bar(x - 0.2, [100 * sh[i]["p1"] for i in pick], 0.38, color=blue, label="husband displaced (same type)")
    ax.bar(x + 0.2, [100 * sh[i]["p0"] for i in pick], 0.38, color=orange, label="husband not displaced")
    for xi, i in zip(x, pick):
        ax.text(xi - 0.2, 100 * sh[i]["p1"], f"{100 * sh[i]['p1']:.1f}", ha="center", va="bottom", fontsize=7,
                color=ink2)
        ax.text(xi + 0.2, 100 * sh[i]["p0"], f"{100 * sh[i]['p0']:.1f}", ha="center", va="bottom", fontsize=7,
                color=ink2)
    ax.set_xticks(x)
    ax.set_xticklabels(labs, fontsize=7.5)
    ax.set_ylabel("% of wives with the same event", color=ink2)
    ax.set_title("A. Wife's displacement by husband's (weighted)", fontsize=10, color=ink, loc="left")
    ax.legend(frameon=False, fontsize=8, labelcolor=ink2)
    ax = axs[1]
    ax.plot(byyear.year, 100 * byyear.p1, color=blue, lw=2, marker="o", ms=6, label="husband displaced")
    ax.plot(byyear.year, 100 * byyear.p0, color=orange, lw=2, marker="o", ms=6, label="husband not displaced")
    for y in byyear.year[byyear.rec == "recession"]:
        ax.axvspan(y - 0.9, y + 0.9, color=grid, alpha=0.9, lw=0)
    ax.set_xlabel("survey year (shaded: recession in the 3-year recall window)", color=ink2)
    ax.set_ylabel("% of wives displaced in the last 3 years", color=ink2)
    ax.set_title("B. By survey", fontsize=10, color=ink, loc="left")
    ax.legend(frameon=False, fontsize=8, labelcolor=ink2)
    ax = axs[2]
    k = [r for r in ind if not r["lab"].startswith("Context")]
    x = np.arange(len(k))
    ax.bar(x - 0.2, [100 * r["share"] for r in k], 0.38, color=blue, label="observed couples")
    ax.bar(x + 0.2, [100 * r["bench"] for r in k], 0.38, color=orange, label="random pairing (same survey)")
    ax.set_xticks(x)
    ax.set_xticklabels([r["lab"].replace("Both ", "").replace(", ", ",\n") for r in k], fontsize=7.5)
    ax.set_ylabel("% losing jobs in the same detailed industry", color=ink2)
    ax.set_title("C. Joint displacements: same lost-job industry", fontsize=10, color=ink, loc="left")
    ax.legend(frameon=False, fontsize=8, labelcolor=ink2)
    fig.tight_layout()
    fig.savefig(path, dpi=150, facecolor=surf)
    plt.close(fig)


def main():
    path = fetch()
    c, flow = couples(path)
    p = couple_years(c)
    att = c[c.both_att == 1]
    patt = p[p.both_att == 1]
    print("couples", len(c), "couple-years", len(p), flush=True)

    # sample by survey year
    yr = []
    for y, g in c.groupby("year"):
        h1, h0 = g[g.h_disp == 1], g[g.h_disp == 0]
        yr.append(dict(year=y, n=len(g), hd=wmean(g.h_disp, g.w), wd=wmean(g.w_disp, g.w),
                       p1=wmean(h1.w_disp, h1.w), p0=wmean(h0.w_disp, h0.w), nh=len(h1),
                       n11=int((h1.w_disp == 1).sum()), rec=recession_window(y)))
    byyear = pd.DataFrame(yr)

    sh = shares(c, p)
    sh_att = shares(att, patt, "attached couples")
    t2 = {"All couples": main_lpm(c, "all couples"), "Attached couples": main_lpm(att, "attached couples")}
    t4 = {"All couples": timing(p, "all couples"), "Attached couples": timing(patt, "attached couples")}

    samples3 = [("All couples", c.index == c.index, p.index == p.index),
                ("Husband Black", c.h_black == 1, p.h_black == 1),
                ("Husband White non-Hispanic", c.h_whitenh == 1, p.h_whitenh == 1),
                ("Survey years 1984-1998", c.period == "1984-1998", p.period == "1984-1998"),
                ("Survey years 2000-2024", c.period == "2000-2024", p.period == "2000-2024"),
                ("Recession windows", c.recwin == "recession", p.recwin == "recession"),
                ("Expansion windows", c.recwin == "expansion", p.recwin == "expansion"),
                ("Attached couples", c.both_att == 1, p.both_att == 1)]
    t3 = {lab: het(c, p, lab, mc, mp) for lab, mc, mp in samples3}
    bw_c = c[(c.h_black == 1) | (c.h_whitenh == 1)]
    bw_p = p[(p.h_black == 1) | (p.h_whitenh == 1)]
    diffs = {"Black - White non-Hispanic": interaction(bw_c, bw_p, "h_black", "Black - White"),
             "2000-2024 - 1984-1998": interaction(c.assign(g2=(c.period == "2000-2024").astype(float)),
                                                  p.assign(g2=(p.period == "2000-2024").astype(float)), "g2",
                                                  "2000-2024 - 1984-1998"),
             "Recession - expansion windows": interaction(c.assign(g3=(c.recwin == "recession").astype(float)),
                                                          p.assign(g3=(p.recwin == "recession").astype(float)),
                                                          "g3", "recession - expansion")}

    ind, by_ind = industry(c)
    clo, clo_x = closings(c, p)
    cons, dcons = consequences(c)

    tet = []
    for lab, d, h, w, unit in (("Displaced, 3-year window", c, "h_disp", "w_disp", "hh"),
                               ("Plant closing, 3-year window", c, "h_close", "w_close", "hh"),
                               ("Displaced, same calendar year (couple-years)", p, "h_y", "w_y", "hh"),
                               ("Plant closing, same calendar year (couple-years)", p, "h_cly", "w_cly", "hh"),
                               ("Displaced, 3-year window, attached couples", att, "h_disp", "w_disp", "hh"),
                               ("Displaced, same year, attached couples", patt, "h_y", "w_y", "hh"),
                               ("Displaced, 3-year window, husband Black", c[c.h_black == 1], "h_disp", "w_disp", "hh"),
                               ("Displaced, 3-year window, husband White NH", c[c.h_whitenh == 1], "h_disp", "w_disp",
                                "hh")):
        est, se, n11, n = tetra_boot(d, h, w, unit)
        tet.append((lab, est, se, n11, n))
        rec("5b tetrachoric", lab, w, "weighted 2x2; bootstrap s.e. (200 draws of couples)", h, est, se, n)
        print("tetra", lab, round(est, 3), flush=True)

    # ------------------------------------------------------------ write
    OUT.mkdir(exist_ok=True)
    pd.DataFrame(REC).to_csv(OUT / "cps_dws_joint_loss.csv", index=False)
    plot(sh, byyear, ind, OUT / "cps_dws_joint_loss.png")

    L = []
    L.append("# Joint displacement of spouses: CPS Displaced Worker Supplement 1984-2024\n")
    L.append("Script `IGE/39.CPSDisplacedWorkers.py` (2026-10-17). Data: IPUMS CPS extract of the 21 biennial "
             "Displaced Worker Supplements (January 1984-1992, February 1994-2000, January 2002-2024), persons married "
             "with spouse present; raw files in `IGE/data/ext/cps_dws/`. Stars: \\*\\*\\* p<0.01, \\*\\* p<0.05, "
             "\\* p<0.1; cells are estimate (s.e.; p). Associations, not causal effects.\n")
    L.append("**Measure.** *Displaced* = lost a wage job in the last three calendar years because the plant or company "
             "closed or moved, there was insufficient work, or the position or shift was abolished (the BLS "
             "definition; IPUMS DWSTAT = 1 from 1994; 1984-1992 harmonised from the five-year window: reasons 1-3, not "
             "self-employed, lost 1-3 calendar years before the survey). The comparison group is always couples whose "
             "husband was **not displaced**. *Respondent / recall:* the CPS accepts proxy answers from any responsible "
             "household member, so both spouses' supplement answers usually come from one respondent at one interview "
             "(the extract carries no self / proxy flag, so the two cannot be separated); recall covers three calendar years with the year "
             "of loss in whole years, and only one lost job per person (the longest held). Couples are observed "
             "married at the survey, so couples who split after a displacement are missing.\n")
    L.append("## 0. Sample\n")
    L.append(md_table(["Step", "N"], [(k, f"{v:,}") for k, v in flow.items()]))
    L.append(f"\nAttached couples (each spouse displaced, employed or unemployed at the survey): {len(att):,}. "
             f"Couple x calendar-year panel (Y-3..Y-1; couples with a displaced spouse of unknown year dropped): "
             f"{len(p):,} couple-years.\n")
    L.append(md_table(["Survey", "Couples", "Husband displaced (wtd)", "Wife displaced (wtd)",
                       "P(w disp | h disp)", "P(w disp | h not)", "Husbands displaced (N)", "Both displaced (N)",
                       "Recall window"],
                      [(int(r.year), f"{r.n:,}", f"{r.hd:.4f}", f"{r.wd:.4f}", f"{r.p1:.4f}", f"{r.p0:.4f}",
                        f"{r.nh:,}", f"{r.n11:,}", r.rec) for r in byyear.itertuples()]))
    L.append("\n## 1. Wife's displacement given the husband's (weighted by the wife's supplement weight)\n")
    for lab, s in (("All couples", sh), ("Attached couples", sh_att)):
        L.append(f"\n**{lab}**\n")
        L.append(md_table(["Event (husband -> wife)", "P(w | h event)", "P(w | h not displaced)", "Ratio",
                           "Difference (wtd LPM)", "N", "Husbands with event", "Joint events"],
                          [(r["lab"], f"{r['p1']:.4f}", f"{r['p0']:.4f}", f"{r['p1'] / r['p0']:.1f}",
                            fmt(r["b"], r["se"], 4), f"{r['n']:,}", f"{r['nh']:,}", f"{r['n11']:,}") for r in s]))
    L.append("\nRows 1-6 use the three-year window (one row per couple); the 'same calendar year' rows use the couple "
             "x year panel: the event is displacement in year y for both. Row 6 is limited to 1984-1992, the only "
             "surveys that record seasonal, business-failure and other losses with a year.\n")

    L.append("\n## 2. LPMs (unweighted; s.e. clustered by household; state-clustered s.e. in the last row)\n")
    names = {"h_disp": "Husband displaced", "h_close": "Husband plant closing",
             "h_slack": "Husband insufficient work / position abolished",
             "hd_x_same": "Husband displaced x same detailed industry", "same_ind": "Same detailed industry"}
    for lab, res in t2.items():
        hdr = ["", *[f"({j}) {r[0]}" for j, r in enumerate(res, 1)]]
        rows = [[f"**{lab}**", *[""] * len(res)]]
        for x in names:
            rows.append([names[x], *[cell(r[5], x) if x in r[2] else "" for r in res]])
        rows.append(["Mean of outcome, husband not displaced", *[f"{r[6]:.4f}" for r in res]])
        rows.append(["Controls (ages, education, race, Hispanic)", *["yes" if r[4] else "no" for r in res]])
        rows.append(["State x survey-year FE", *["yes" if r[3] else "no" for r in res]])
        rows.append(["N couples", *[f"{r[5]['N']:,}" for r in res]])
        rows.append(["First regressor, s.e. clustered by state",
                     *[fmt(r[5]["b"][r[2][0]], r[5]["se"]["state"][r[2][0]]) for r in res]])
        L.append(md_table(hdr, rows))
        L.append("")
    L.append("Column (6): sample with a reference industry for both spouses (lost-job industry if displaced, else the "
             "current or last job of the employed / unemployed), detailed Census industry code of the survey year; "
             "this requires both spouses to be attached, so column (6) is the same regression in both panels.\n")

    L.append("\n## 3. Heterogeneity (state x survey-year FE + controls; same-year column: couple x year panel, state x "
             "survey x calendar-year FE, also controls the husband's displacement in another year)\n")
    hdr = ["", "(1) Wife displaced", "(2) Wife plant closing", "(3) Wife displaced in year y"]
    rows = []
    for lab, o in t3.items():
        rows.append([f"**{lab}**", "", "", ""])
        rows.append(["Husband's event (displaced / plant closing / displaced in y)",
                     *[cell(o[k][0], o[k][1]) for k in ("disp", "close", "same")]])
        rows.append(["Mean of outcome, husband not displaced", *[f"{o[k][2]:.4f}" for k in ("disp", "close", "same")]])
        rows.append(["N", *[f"{o[k][0]['N']:,}" for k in ("disp", "close", "same")]])
    for lab, o in diffs.items():
        rows.append([f"**Difference: {lab}** (pooled, H x group)", "", "", ""])
        rows.append(["Husband's event x group", *[cell(o[k][0], o[k][1]) for k in ("disp", "close", "same")]])
        rows.append(["N", *[f"{o[k][0]['N']:,}" for k in ("disp", "close", "same")]])
    L.append(md_table(hdr, rows))
    L.append("\nThe outcome in column (2) is the wife's plant closing and the regressor the husband's plant closing "
             "(controlling for his other displacement). Recession windows: the three recall years contain >= 2 NBER "
             "recession months (surveys 1984, 1992, 1994, 2002, 2004, 2010, 2012, 2022).\n")

    L.append("\n## 4. Same calendar year (couple x year panel; state x survey x calendar-year FE + controls)\n")
    tn = {"h_y": "Husband displaced in year y", "h_oth": "Husband displaced in another year of the window",
          "h_cly": "Husband plant closing in year y", "h_sly": "Husband insufficient work / abolished in year y",
          "h_clo": "Husband plant closing in another year", "h_slo": "Husband insufficient work / abolished, other year"}
    for lab, res in t4.items():
        hdr = ["", *[f"({j}) {r[0]}" for j, r in enumerate(res, 1)]]
        rows = [[f"**{lab}**", *[""] * len(res)]]
        for x in tn:
            rows.append([tn[x], *[cell(r[2], x) if x in r[1] else "" for r in res]])
        rows.append(["Mean of outcome, husband not displaced", *[f"{r[3]:.4f}" for r in res]])
        rows.append(["Controls; state x survey x calendar-year FE", *["yes" for _ in res]])
        rows.append(["N couple-years", *[f"{r[2]['N']:,}" for r in res]])
        rows.append(["First regressor, s.e. clustered by state",
                     *[fmt(r[2]["b"][r[1][0]], r[2]["se"]["state"][r[1][0]]) for r in res]])
        L.append(md_table(hdr, rows))
        L.append("")

    L.append("\n## 5. Same industry\n")
    L.append(md_table(["Couples", "N", "Share same detailed industry", "Random pairing (same survey)", "Ratio",
                       "Share - benchmark"],
                      [(r["lab"], f"{r['n']:,}", f"{r['share']:.3f}", f"{r['bench']:.4f}", f"{r['ratio']:.1f}",
                        fmt(r["b"], r["se"])) for r in ind]))
    L.append("\nRandom pairing: within each survey, the probability that a displaced husband and a displaced wife "
             "drawn independently (weighted) lost jobs in the same detailed industry, averaged over the couples in the "
             "row. Lost-job industries of both spouses are coded in the same scheme within a survey.\n")
    L.append(md_table(["Reference industries", "P(w disp | h disp)", "P(w disp | h not)", "Husbands displaced (N)",
                       "N"],
                      [("same detailed industry", f"{by_ind[1][0]:.4f}", f"{by_ind[1][1]:.4f}", f"{by_ind[1][2]:,}",
                        f"{by_ind[1][3]:,}"),
                       ("different industry", f"{by_ind[0][0]:.4f}", f"{by_ind[0][1]:.4f}", f"{by_ind[0][2]:,}",
                        f"{by_ind[0][3]:,}")]))
    L.append("\n### 5b. Tetrachoric correlation of the spouses' events (weighted 2x2; bootstrap s.e., 200 draws)\n")
    L.append(md_table(["Events", "Tetrachoric", "Joint events (N)", "N"],
                      [(lab, fmt(e, s), f"{n11:,}", f"{n:,}") for lab, e, s, n11, n in tet]))

    L.append("\n## 6. Joint plant closings (husband's plant closed vs husband not displaced; weighted)\n")
    L.append(md_table(["Wife's outcome", "P(w | h plant closing)", "P(w | h not displaced)", "Ratio",
                       "Difference (wtd LPM)", "Husbands with closing (N)", "Joint events (N)"],
                      [(r["lab"], f"{r['p1']:.4f}", f"{r['p0']:.4f}", f"{r['p1'] / r['p0']:.1f}",
                        fmt(r["b"], r["se"], 4), f"{r['n1']:,}", f"{r['n11']:,}") for r in clo]))
    L.append(f"\nHusbands with a plant closing in a known year: {clo_x['n_hclose_known_year']:,}; wife's plant also "
             f"closed in the same year: {clo_x['n_joint_same_year']:,}, of which in the same detailed industry "
             f"{clo_x['n_same_ind']:,} (weighted share of husbands' closings: {100 * clo_x['share_same_ind']:.2f}%, the "
             "closest proxy in the DWS for one closure hitting both; Halla, Schmieder and Weber 2020 find both spouses "
             "at the closing plant in 3.5% of Austrian closure households).\n")

    L.append("\n## 7. What a joint displacement does to the household at the survey (displaced husbands with a known "
             "year; state x survey-year FE + controls)\n")
    hdr = ["", *[f"({j}) {r[0]}" for j, r in enumerate(cons, 1)]]
    rows = [["Wife displaced in the same year", *[cell(r[1], "w_same") for r in cons]],
            ["Wife displaced in another year", *[cell(r[1], "w_othy") for r in cons]],
            ["Mean of outcome, wife not displaced", *[f"{r[2]:.3f}" for r in cons]],
            ["Controls; state x survey-year FE", *["yes" for _ in cons]],
            ["N displaced husbands", *[f"{r[1]['N']:,}" for r in cons]]]
    L.append(md_table(hdr, rows))
    L.append("\nWeeks without work: DWWKSUN (weeks before the next job or to the survey). Employment at the survey "
             "is 0-3 years after the loss.\n")

    m1 = sh[0]
    sy = sh[6]
    tw = tet[0]
    L.append("\n## 8. Comparison with the PSID and the CPS monthly panel\n")
    L.append(md_table(["", "PSID (25.JointJobLoss.py)", "CPS monthly 1994-2023 (30)", "CPS DWS 1984-2024 (this)"], [
        ("Event", "reason job ended: plant closed / laid off / fired", "unemployed job loser (layoff, other job loser, "
         "temp. job ended), month to month", "displaced: plant closed, insufficient work, position abolished"),
        ("Window", "couple-year; ev-1..ev+1", "same month", "same calendar year / 3 calendar years"),
        ("P(w | h) vs P(w | not h)", "0.102 vs 0.039 per couple-year (ratio 2.6)", "0.0545 vs 0.0054 (ratio 10.1)",
         f"same year {sy['p1']:.3f} vs {sy['p0']:.4f} (ratio {sy['p1'] / sy['p0']:.1f}); 3 years {m1['p1']:.3f} vs "
         f"{m1['p0']:.3f} (ratio {m1['p1'] / m1['p0']:.1f})"),
        ("Excess (LPM)", "+0.083*** (0.013) ev-1..ev+1", "+0.040*** (0.002), state x month FE",
         f"3 years {cell(t2['All couples'][2][5], 'h_disp')}; same year {cell(t4['All couples'][0][2], 'h_y')}"),
        ("Tetrachoric", "0.237*** (0.016) (annual 0.200)", "phi 0.053",
         f"3 years {fmt(tw[1], tw[2])}; same year {fmt(tet[2][1], tet[2][2])}"),
        ("Same industry", "x same 3-digit industry +0.282*** (0.078)", "same detailed industry: P(w|h) 0.230, "
         "+0.211*** (0.009)", f"H x same detailed industry {cell(t2['All couples'][5][5], 'hd_x_same')}"),
        ("Race", "B +0.088***, W +0.077***", "H x Black +0.0055 (p=0.309)",
         f"H x Black {cell(diffs['Black - White non-Hispanic']['disp'][0], 'hxg')}"),
    ]))
    L.append("\nPSID and CPS-monthly numbers from `IGE/EVIDENCE.md` rows 3.16, 3.20, 3.21, 3.24, 3.27, 3.28.\n")
    (OUT / "cps_dws_joint_loss.md").write_text("\n".join(L), encoding="utf-8")
    print("wrote", OUT / "cps_dws_joint_loss.md", flush=True)


if __name__ == "__main__":
    main()
