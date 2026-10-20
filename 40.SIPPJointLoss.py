r"""Joint job loss within married couples in the SIPP (2026-10-17). [Paper A; referee plan item 5]

Question: the CPS (30.CPSJointJobLoss.py) shows that a wife is ~10x as likely to lose her job in the month her husband
loses his, but follows couples for at most 4 consecutive months; the PSID (25.JointJobLoss.py) follows them for decades
but annually. The SIPP observes both spouses' monthly employment and the reason each job ended, for 4 (2004, 2014
panels) to 5.3 (2008 panel) years. It gives (i) the monthly hazard of the wife's involuntary separation from tau-6 to
tau+12 around the husband's, (ii) the same-month ratio with a reason-for-separation definition that differs from the
CPS's, and (iii) the added-worker path of non-employed wives over the 36 months after his separation.

DATA (downloaded here, sequential requests, retries; raw files are data only -> run this script with `python -I`)
  Public-use SIPP core wave files, saved unchanged in data/ext/sipp/ (git-ignored):
    raw2004/sippl04puw{1..12}.csv.zip   2004 panel, NBER mirror (data.nber.org/sipp/2004), Oct 2003 - Dec 2007
    raw2008/sippl08puw{1..16}.csv.zip   2008 panel, NBER mirror (data.nber.org/sipp/2008), May 2008 - Nov 2013
    raw2014/pu2014w{1..4}.csv.gz        2014 panel, Census (www2.census.gov/programs-surveys/sipp/data/datasets/2014),
                                        reference years 2013-2016 (annual interviews, event-history calendar)
  Only the needed columns are read (chunked); the harmonised person-months are cached per wave in
  data/ext/sipp/cache/ and the couple panel in data/sipp_couples_panel.pkl.
  2004/2008 (4-month waves; 4 rotation groups interviewed in successive months; one record per person-month):
    identifiers  SSUID, EPPPNUM (person number, stable within the sample unit), SPANEL, SWAVE, SROTATON, SREFMON,
                 RHCALMN, RHCALYR; spouse EPNSPOUS; parents EPNMOM, EPNDAD; TFIPSST (state); EPPINTVW (self / proxy)
    person       ESEX, ERACE (1 White alone, 2 Black alone), EORIGIN, TAGE, EMS (1 married, spouse present), EEDUCATE,
                 WPFINWGT (person weight of the month)
    labor force  RMESR (1-5 with a job at least one week of the month; 6-7 no job, some weeks looking / on layoff;
                 8 no job, not looking), RMWKLKG (weeks looking or on layoff)
    jobs 1, 2    EENO (person-specific employer number, constant across waves), TSJDATE / TEJDATE (start / end date),
                 ERSEND (main reason stopped working for the employer), EJBIND, TJBOCC (2002 Census industry /
                 2000 Census occupation codes), ECLWRK
  2014 (annual waves; 12 monthly records per person and wave; up to 7 jobs):
    SSUID, PNUM, SPANEL, SWAVE, MONTHCODE, TEHC_ST (monthly state), ESEX, ERACE, EORIGIN, TAGE_EHC, EMS_EHC,
    EPNSPOUS_EHC, RPNPAR1_EHC / RPNPAR2_EHC, EEDUC, WPFINWGT, RMESR, RMWKLKG, EINTTYPE (self / proxy);
    jobs k = 1..7: EJBk_JOBID, EJBk_BMONTH / EJBk_EMONTH (first / last month of the spell in the reference year),
    EJBk_RSEND (reason stopped working), EJBk_JBORSE (1 = employer; self-employment dropped), TJBk_IND, TJBk_OCC.
  Employer numbers (EENO, EJBk_JOBID) are person-specific: the public SIPP does not say whether the two spouses work
  for the same employer, so 'same employer' cannot be measured; industry and occupation can.
DEFINITIONS (person-month m)
  employed E_m: RMESR 1-5 (a job at least one week of the month).
  separation at m: an employer job whose end date falls in m (2004/08: TEJDATE year-month = m; 2014: EJBk_EMONTH = m
    with a reason recorded). Reasons harmonised to: layoff (2004/08 'on layoff', 'slack work or business conditions';
    2014 'slack work', 'position or shift abolished'), closure (2004/08 'employer bankrupt', 'employer sold
    business'; 2014 'plant or company closed down or moved'), discharged / fired, temporary job ended, other
    involuntary (2014 only), quit to take another job, other quit / personal (retirement, childcare, family, illness,
    school, unsatisfactory arrangements, other).
  involuntary separation INV_m: a separation for layoff, closure, discharge, temporary job ended or other involuntary
    reason. Narrow (demand-side) INVN_m: layoff or closure only. CPS-like job loss: INV_m and no job all of month m+1.
COUPLES
  Husband (ESEX 1) and wife (ESEX 2) in the same sample unit and month who name each other as spouse, both married
  spouse present, both aged 20-60 that month (as in the CPS script). Couple = sample unit + both person numbers;
  household (cluster) = panel + SSUID. Youngest own child: minimum age of persons < 18 naming either spouse as parent.
  Leads and lags are looked up by calendar month within the couple (missing when the couple is not observed).
ESTIMATES (descriptive probabilities weighted by the wife's person weight of the base month; regressions unweighted
  LPM, s.e. clustered by household)
  1. Same-month joint involuntary separation: both employed at m-1; H = 1 husband INV at m, H = 0 husband employed at
     m with no INV (through the end of the window). Windows: same month, within 1 / 2 / 11 months after. LPMs with
     panel x rotation x calendar-month FE ('panel-month FE'; the rotation absorbs the interview seam) and state x
     panel-month FE. Seam check: the SIPP heaps transitions at the seam between waves, and spouses are interviewed
     together, so the off-seam sample (m-1 and m in the same wave) and self-respondent couples are reported.
  2. Event study: wife's monthly INV hazard (wife employed at m-1) on indicators of the husband's INV at m-j,
     j = -6..12 (his event j months before), each with an indicator for his status unobserved at m-j; FE as in 1.
  3. Added-worker path: base month b, husband employed at b, wife with no job at b; H = 1 husband INV at b+1 (= tau),
     H = 0 husband employed at b+1 without INV. Outcomes at tau+s, s = 0..36: wife employed, wife looking / on layoff
     (RMWKLKG > 0); LPM of each on H with base panel-month FE, by youngest child (none / 0-5 / 6-17) and race.
     Gross vs net: the same comparison for wives employed at b and for all wives (net), and for all wives excluding
     those with their own INV at tau or tau+1 (the joint losers), so net = gross entry - the joint-loss drag.
  4. Race: same-month LPM, event-study sums and the added-worker path by the husband's race (ERACE 1 / 2).
  5. Comparison with the CPS (EVIDENCE 3.24-3.34) and PSID (3.16-3.23) numbers.
Nothing here is a randomised design: the excess joint separation is an association conditional on the fixed effects.
Writes output/sipp_joint_loss.csv (every estimate), .md (tables), .png (figure).
"""
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))                 # -I drops the script directory from sys.path

import numpy as np                            # noqa: E402
import pandas as pd                           # noqa: E402

from common import DATA, OUT, stars           # noqa: E402

RAW = DATA / "ext" / "sipp"
CACHE = RAW / "cache"
PANEL_PKL = DATA / "sipp_couples_panel.pkl"
PANELS = {2004: 12, 2008: 16, 2014: 4}
LEADS, LAGS = 6, 12                            # event window tau-6 .. tau+12
AW_S = 36                                      # added-worker horizon (months after tau)


# ---------------------------------------------------------------- download
def src(panel, w):
    if panel == 2014:
        return (f"https://www2.census.gov/programs-surveys/sipp/data/datasets/2014/w{w}/pu2014w{w}.csv.gz",
                RAW / "raw2014" / f"pu2014w{w}.csv.gz")
    yy = str(panel)[2:]
    return (f"https://data.nber.org/sipp/{panel}/sippl{yy}puw{w}.csv.zip",
            RAW / f"raw{panel}" / f"sippl{yy}puw{w}.csv.zip")


def download():
    for panel, nw in PANELS.items():
        for w in range(1, nw + 1):
            url, path = src(panel, w)
            if path.exists() and path.stat().st_size > 0:
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            for attempt in range(4):
                try:
                    tmp = path.with_suffix(path.suffix + ".part")
                    with urllib.request.urlopen(url, timeout=600) as r, open(tmp, "wb") as fh:
                        while True:
                            b = r.read(1 << 20)
                            if not b:
                                break
                            fh.write(b)
                    tmp.replace(path)
                    print("downloaded", path.name, flush=True)
                    break
                except Exception as e:                   # noqa: BLE001
                    print("retry", url, e, flush=True)
                    time.sleep(10 * (attempt + 1))


# ---------------------------------------------------------------- harmonise one wave
RS0408 = {1: 1, 13: 1, 9: 2, 10: 2, 8: 3, 11: 4, 12: 6, 2: 7, 3: 7, 4: 7, 5: 7, 6: 7, 7: 7, 14: 7, 15: 7}
RS14 = {1: 2, 2: 1, 3: 1, 4: 4, 5: 3, 6: 5, 7: 6, **{k: 7 for k in range(8, 17)}}
RSNAME = {1: "layoff / slack work", 2: "closure / bankrupt / sold", 3: "discharged / fired", 4: "temporary job ended",
          5: "other involuntary (2014)", 6: "quit to take another job", 7: "other quit / personal"}
BASE0408 = ["ssuid", "spanel", "swave", "srotaton", "srefmon", "rhcalmn", "rhcalyr", "tfipsst", "epppnum", "eppintvw",
            "esex", "erace", "eorigin", "tage", "ems", "epnspous", "epnmom", "epndad", "eeducate", "wpfinwgt", "rmesr",
            "rmwklkg"]
SLOT0408 = ["eeno{j}", "tsjdate{j}", "tejdate{j}", "ersend{j}", "ejbind{j}", "tjbocc{j}"]
BASE14 = ["SSUID", "PNUM", "SPANEL", "SWAVE", "MONTHCODE", "TEHC_ST", "ESEX", "ERACE", "EORIGIN", "TAGE_EHC",
          "EMS_EHC", "EPNSPOUS_EHC", "RPNPAR1_EHC", "RPNPAR2_EHC", "EEDUC", "WPFINWGT", "RMESR", "RMWKLKG", "EINTTYPE"]
SLOT14 = ["EJB{j}_JOBID", "EJB{j}_BMONTH", "EJB{j}_EMONTH", "EJB{j}_RSEND", "EJB{j}_JBORSE", "TJB{j}_IND", "TJB{j}_OCC"]


def wanted(panel):
    if panel == 2014:
        return set(BASE14) | {s.format(j=j) for s in SLOT14 for j in range(1, 8)}
    return set(BASE0408) | {s.format(j=j) for s in SLOT0408 for j in (1, 2)}


def _num(d, c):
    if c not in d:
        return np.full(len(d), -1, dtype=np.int64)
    return pd.to_numeric(d[c], errors="coerce").fillna(-1).astype(np.int64).to_numpy()


def ind_major(c):
    """2002 / 2012 Census industry code -> 16 major groups (0 = missing)."""
    edges = [170, 370, 570, 770, 1070, 4070, 4670, 6070, 6470, 6870, 7270, 7860, 8560, 8770, 9370, 9670, 9900]
    g = np.digitize(c, edges)
    return np.where((c >= 170) & (c < 9900), g, 0)


def occ_major(c):
    """2000 / 2010 Census occupation code -> 10 major groups (0 = missing)."""
    edges = [10, 1000, 3600, 4700, 6000, 6200, 7000, 7700, 9000, 9800, 9999]
    g = np.digitize(c, edges)
    return np.where((c >= 10) & (c < 9999), g, 0)


def harmonise(d, panel):
    """Raw chunk -> (married adults' person-months with derived job events, children's parent links)."""
    n = len(d)
    if panel == 2014:
        year = 2012 + _num(d, "SWAVE")
        month = _num(d, "MONTHCODE")
        h = dict(wave=_num(d, "SWAVE"), rot=np.zeros(n, np.int64), refmon=month, year=year, month=month,
                 ssuid=d["SSUID"].astype(str).str.strip().to_numpy(), pnum=_num(d, "PNUM"), sp=_num(d, "EPNSPOUS_EHC"),
                 sex=_num(d, "ESEX"), race=_num(d, "ERACE"), hisp=_num(d, "EORIGIN"), age=_num(d, "TAGE_EHC"),
                 ms=_num(d, "EMS_EHC"), par1=_num(d, "RPNPAR1_EHC"), par2=_num(d, "RPNPAR2_EHC"),
                 state=_num(d, "TEHC_ST"), intv=_num(d, "EINTTYPE"), rmesr=_num(d, "RMESR"), lkwks=_num(d, "RMWKLKG"))
        e = _num(d, "EEDUC")
        educ = np.select([e <= 0, e <= 38, e == 39, e <= 42], [0, 1, 2, 3], 4)
        wgt = pd.to_numeric(d["WPFINWGT"], errors="coerce").to_numpy(float)
        slots = []
        for j in range(1, 8):
            jid, bm, em = _num(d, f"EJB{j}_JOBID"), _num(d, f"EJB{j}_BMONTH"), _num(d, f"EJB{j}_EMONTH")
            rsr, jb = _num(d, f"EJB{j}_RSEND"), _num(d, f"EJB{j}_JBORSE")
            present = (jid > 0) & (jb == 1) & (bm > 0) & (em > 0)
            held = present & (bm <= month) & (month <= em)
            end = present & (em == month) & (rsr > 0)
            rs = np.where(end, pd.Series(rsr).map(RS14).fillna(0).astype(int).to_numpy(), 0)
            slots.append((held, end, rs, _num(d, f"TJB{j}_IND"), _num(d, f"TJB{j}_OCC")))
    else:
        year, month = _num(d, "rhcalyr"), _num(d, "rhcalmn")
        h = dict(wave=_num(d, "swave"), rot=_num(d, "srotaton"), refmon=_num(d, "srefmon"), year=year, month=month,
                 ssuid=d["ssuid"].astype(str).str.strip().str.lstrip("0").to_numpy(), pnum=_num(d, "epppnum"),
                 sp=_num(d, "epnspous"), sex=_num(d, "esex"), race=_num(d, "erace"), hisp=_num(d, "eorigin"),
                 age=_num(d, "tage"), ms=_num(d, "ems"), par1=_num(d, "epnmom"), par2=_num(d, "epndad"),
                 state=_num(d, "tfipsst"), intv=_num(d, "eppintvw"), rmesr=_num(d, "rmesr"), lkwks=_num(d, "rmwklkg"))
        e = _num(d, "eeducate")
        educ = np.select([e <= 0, e <= 38, e == 39, e <= 43], [0, 1, 2, 3], 4)
        wgt = pd.to_numeric(d["wpfinwgt"], errors="coerce").to_numpy(float)
        ym = year * 100 + month
        slots = []
        for j in (1, 2):
            eeno, sj, ej, rsr = _num(d, f"eeno{j}"), _num(d, f"tsjdate{j}"), _num(d, f"tejdate{j}"), _num(d, f"ersend{j}")
            present = eeno > 0
            held = present & ((sj <= 0) | (sj <= ym * 100 + 31)) & ((ej <= 0) | (ej >= ym * 100 + 1))
            end = present & (ej > 0) & (ej // 100 == ym)
            rs = np.where(end, pd.Series(rsr).map(RS0408).fillna(0).astype(int).to_numpy(), 0)
            slots.append((held, end, rs, _num(d, f"ejbind{j}"), _num(d, f"tjbocc{j}")))
    out = pd.DataFrame(h)
    out["educ"], out["wgt"] = educ, wgt
    held = np.column_stack([s[0] for s in slots])
    end = np.column_stack([s[1] for s in slots])
    rs = np.column_stack([s[2] for s in slots])
    ind = np.column_stack([s[3] for s in slots])
    occ = np.column_stack([s[4] for s in slots])
    inv = end & (rs >= 1) & (rs <= 5)
    out["INV"] = inv.any(1).astype(np.int8)
    out["INVN"] = (end & (rs >= 1) & (rs <= 2)).any(1).astype(np.int8)
    out["SEP"] = end.any(1).astype(np.int8)
    out["QUIT"] = (end & (rs >= 6)).any(1).astype(np.int8)
    rsfirst = np.where(inv.any(1), rs[np.arange(n), inv.argmax(1)], np.where(end.any(1), rs[np.arange(n), end.argmax(1)], 0))
    out["rs"] = rsfirst.astype(np.int8)
    first = held.argmax(1)
    anyh = held.any(1)
    out["wagejob"] = anyh.astype(np.int8)
    out["ind"] = np.where(anyh, ind[np.arange(n), first], -1)
    out["occ"] = np.where(anyh, occ[np.arange(n), first], -1)
    out["ind_inv"] = np.where(inv.any(1), ind[np.arange(n), inv.argmax(1)], -1)
    out["panel"] = panel
    kids = out.loc[(out.age >= 0) & (out.age < 18), ["panel", "ssuid", "year", "month", "age", "par1", "par2"]]
    adults = out[(out.age >= 18) & (out.age <= 70) & (out.ms == 1) & (out.sp > 0) & (out.sp < 9000)]
    return adults, kids


def extract(panel, w):
    path = CACHE / f"p{panel}w{w:02d}.pkl"
    if path.exists():
        return pd.read_pickle(path)
    url, raw = src(panel, w)
    want = wanted(panel)
    kw = dict(usecols=lambda c: c in want, chunksize=60000, dtype=str, low_memory=False)
    if panel == 2014:
        import gzip
        with gzip.open(raw, "rt") as fh:
            head = fh.readline()
        kw["sep"] = "|" if head.count("|") > head.count(",") else ","
    A, K = [], []
    for ch in pd.read_csv(raw, **kw):
        if panel != 2014:
            ch.columns = [c.lower() for c in ch.columns]
        a, k = harmonise(ch, panel)
        A.append(a)
        K.append(k)
    a, k = pd.concat(A, ignore_index=True), pd.concat(K, ignore_index=True)
    for c in ("wave", "rot", "refmon", "month", "sex", "race", "hisp", "age", "ms", "educ", "intv", "rmesr", "lkwks"):
        a[c] = a[c].astype(np.int16)
    k["age"] = k["age"].astype(np.int16)
    res = {"adults": a, "kids": k}
    CACHE.mkdir(parents=True, exist_ok=True)
    pd.to_pickle(res, path)
    print(f"extracted {panel} w{w}: adults {len(a):,}, kids {len(k):,}", flush=True)
    return res


# ---------------------------------------------------------------- couple panel
def build_panel():
    if PANEL_PKL.exists():
        return pd.read_pickle(PANEL_PKL)
    A, K = [], []
    for panel, nw in PANELS.items():
        for w in range(1, nw + 1):
            if not src(panel, w)[1].exists():
                print("missing raw file", panel, w, flush=True)
                continue
            r = extract(panel, w)
            A.append(r["adults"])
            K.append(r["kids"])
    a = pd.concat(A, ignore_index=True)
    k = pd.concat(K, ignore_index=True)
    a["ym"] = (a.year * 12 + a.month - 1).astype(np.int32)
    k["ym"] = (k.year * 12 + k.month - 1).astype(np.int32)
    a = a.drop_duplicates(["panel", "ssuid", "pnum", "ym"])
    keep = ["panel", "wave", "rot", "refmon", "year", "month", "ym", "ssuid", "pnum", "sp", "race", "hisp", "age",
            "educ", "state", "intv", "wgt", "rmesr", "lkwks", "INV", "INVN", "SEP", "QUIT", "rs", "wagejob", "ind",
            "occ", "ind_inv"]
    H = a[a.sex == 1][keep]
    W = a[a.sex == 2][keep]
    on_h = ["panel", "ssuid", "ym"]
    P = H.merge(W, left_on=on_h + ["sp", "pnum"], right_on=on_h + ["pnum", "sp"], suffixes=("_h", "_w"))
    P = P[(P.age_h.between(20, 60)) & (P.age_w.between(20, 60))].copy()
    for c in ("wave", "rot", "refmon", "year", "month"):
        P[c] = P[c + "_h"]
        P = P.drop(columns=[c + "_h", c + "_w"])
    P = P.drop(columns=["sp_h", "sp_w"])
    # youngest own child of either spouse
    kk = pd.concat([k.rename(columns={"par1": "par"})[["panel", "ssuid", "ym", "par", "age"]],
                    k.rename(columns={"par2": "par"})[["panel", "ssuid", "ym", "par", "age"]]])
    kk = kk[kk.par > 0].groupby(["panel", "ssuid", "ym", "par"], as_index=False)["age"].min()
    for s in ("h", "w"):
        P = P.merge(kk.rename(columns={"par": f"pnum_{s}", "age": f"yc_{s}"}), on=["panel", "ssuid", "ym", f"pnum_{s}"],
                    how="left")
    P["yc"] = P[["yc_h", "yc_w"]].min(axis=1)
    P = P.drop(columns=["yc_h", "yc_w"])
    P["cid"] = pd.factorize(pd.MultiIndex.from_frame(P[["panel", "ssuid", "pnum_h", "pnum_w"]]))[0]
    P["hh"] = pd.factorize(pd.MultiIndex.from_frame(P[["panel", "ssuid"]]))[0]
    P = P.drop_duplicates(["cid", "ym"]).sort_values(["cid", "ym"]).reset_index(drop=True)
    P.to_pickle(PANEL_PKL)
    return P


# ---------------------------------------------------------------- helpers
class Look:
    """Value of a column k months away for the same couple (NaN when not observed)."""

    def __init__(self, P):
        self.P = P
        self.key = P["cid"].to_numpy(np.int64) * 1000 + (P["ym"].to_numpy(np.int64) - int(P["ym"].min()))
        self.idx = pd.Index(self.key)
        self.cache = {}

    def pos(self, k):
        if k not in self.cache:
            self.cache[k] = self.idx.get_indexer(self.key + k)
        return self.cache[k]

    def at(self, col, k):
        if k == 0:
            return self.P[col].to_numpy(float)
        p = self.pos(k)
        v = self.P[col].to_numpy(float)
        return np.where(p >= 0, v[np.maximum(p, 0)], np.nan)


def demean(a, codes, n):
    cnt = np.bincount(codes, minlength=n)
    if a.ndim == 1:
        return a - (np.bincount(codes, weights=a, minlength=n) / np.maximum(cnt, 1))[codes]
    return np.column_stack([demean(a[:, j], codes, n) for j in range(a.shape[1])])


def pval(b, se):
    from scipy.stats import norm
    return 2 * norm.sf(abs(b / se)) if se > 0 else np.nan


def lpm(d, y, xs, fe=None, cl="hh", w=None):
    """OLS (WLS if w) of y on xs absorbing one FE column (codes); s.e. clustered by `cl`. Returns dict with V."""
    if w is not None:
        d = d[np.isfinite(d[w].to_numpy(float)) & (d[w].to_numpy(float) > 0)]
    Y = d[y].to_numpy(float)
    X = d[xs].to_numpy(float)
    names = list(xs)
    if fe is not None:
        codes, uniq = pd.factorize(d[fe])
        Y, X = demean(Y, codes, len(uniq)), demean(X, codes, len(uniq))
    else:
        X = np.column_stack([X, np.ones(len(X))])
        names += ["const"]
    wt = np.ones(len(Y)) if w is None else d[w].to_numpy(float)
    XtX = (X * wt[:, None]).T @ X
    keep = np.abs(np.diag(XtX)) > 1e-12
    X, names = X[:, keep], [nm for nm, kp in zip(names, keep) if kp]
    XtXi = np.linalg.pinv((X * wt[:, None]).T @ X)
    b = XtXi @ (X * wt[:, None]).T @ Y
    u = Y - X @ b
    N, K = X.shape
    g, gu = pd.factorize(d[cl])
    G = len(gu)
    S = np.column_stack([np.bincount(g, weights=X[:, j] * u * wt, minlength=G) for j in range(K)])
    V = XtXi @ (S.T @ S) @ XtXi * (G / (G - 1)) * ((N - 1) / max(N - K, 1))
    se = np.sqrt(np.maximum(np.diag(V), 0))
    return {"b": dict(zip(names, b)), "se": dict(zip(names, se)), "V": pd.DataFrame(V, names, names), "N": N, "G": G,
            "ymean": float(np.mean(d[y]))}


def fmt(b, se, nd=3):
    p = pval(b, se)
    pv = "<0.001" if p < 0.001 else f"{p:.3f}"
    return f"{b:.{nd}f}{stars(p)} ({se:.{nd}f}; p={pv})"


def cell(r, x="H", nd=3):
    return fmt(r["b"][x], r["se"][x], nd) if x in r["b"] else "-"


def wmean(x, w):
    x, w = np.asarray(x, float), np.asarray(w, float)
    ok = ~np.isnan(x) & ~np.isnan(w)
    return np.sum(x[ok] * w[ok]) / np.sum(w[ok]) if ok.any() else np.nan


def phi(a, b, w):
    a, b, w = np.asarray(a, float), np.asarray(b, float), np.asarray(w, float)
    ma, mb = wmean(a, w), wmean(b, w)
    cov = wmean((a - ma) * (b - mb), w)
    return cov / np.sqrt(ma * (1 - ma) * mb * (1 - mb))


ROWS = []


def rec(table, sample, outcome, spec, r, x="H", extra=None):
    if x not in r["b"]:
        return
    b, se = r["b"][x], r["se"][x]
    row = dict(table=table, sample=sample, outcome=outcome, spec=spec, term=x, b=b, se=se, p=pval(b, se), N=r["N"],
               clusters=r["G"], ymean=r["ymean"])
    if extra:
        row.update(extra)
    ROWS.append(row)


def add_vars(P):
    L = Look(P)
    for s in ("h", "w"):
        P[f"E_{s}"] = P[f"rmesr_{s}"].between(1, 5).astype(np.int8)
        P[f"NE_{s}"] = P[f"rmesr_{s}"].between(6, 8).astype(np.int8)
        P[f"LK_{s}"] = (P[f"lkwks_{s}"] > 0).astype(np.int8)
        P[f"E_{s}_l1"] = L.at(f"E_{s}", -1)
        nxt = L.at(f"E_{s}", 1)
        P[f"JL_{s}"] = np.where(np.isnan(nxt), np.nan, P[f"INV_{s}"] * (nxt == 0))   # CPS-like: INV, no job at m+1
        P[f"ind_{s}_l1"] = L.at(f"ind_{s}", -1)
        P[f"occ_{s}_l1"] = L.at(f"occ_{s}", -1)
    P["seam"] = np.where(P.panel == 2014, P.month == 1, P.refmon == 1).astype(np.int8)
    P["pm"] = pd.factorize(pd.MultiIndex.from_frame(P[["panel", "rot", "ym"]]))[0]
    P["spm"] = pd.factorize(pd.MultiIndex.from_frame(P[["state_h", "panel", "rot", "ym"]]))[0]
    P["black"] = (P.race_h == 2).astype(np.int8)
    P["self2"] = ((P.intv_h == 1) & (P.intv_w == 1)).astype(np.int8)
    P["yc_cat"] = np.select([P.yc.isna(), P.yc <= 5], ["none", "0-5"], "6-17")
    P["mi_h"] = ind_major(P.ind_h_l1.fillna(-1).to_numpy(int))
    P["mi_w"] = ind_major(P.ind_w_l1.fillna(-1).to_numpy(int))
    P["same_ind"] = ((P.mi_h == P.mi_w) & (P.mi_h > 0)).astype(np.int8)
    P["same_ind4"] = ((P.ind_h_l1 == P.ind_w_l1) & (P.ind_h_l1 > 0)).astype(np.int8)
    oh, ow = occ_major(P.occ_h_l1.fillna(-1).to_numpy(int)), occ_major(P.occ_w_l1.fillna(-1).to_numpy(int))
    P["same_occ"] = ((oh == ow) & (oh > 0)).astype(np.int8)
    P["ind_known"] = ((P.mi_h > 0) & (P.mi_w > 0)).astype(np.int8)
    return P, L


def controls(d):
    X = []
    for s in ("h", "w"):
        ag = pd.cut(d[f"age_{s}"], [19, 29, 39, 49, 60], labels=False)
        X.append(pd.get_dummies(ag, prefix=f"ag{s}", drop_first=True, dtype=float))
        X.append(pd.get_dummies(d[f"educ_{s}"], prefix=f"ed{s}", drop_first=True, dtype=float))
    X.append(pd.get_dummies(d["race_h"].clip(1, 4), prefix="race", drop_first=True, dtype=float))
    X.append(pd.get_dummies(d["yc_cat"], prefix="yc", drop_first=True, dtype=float))
    return pd.concat(X, axis=1)


def jl_sample(P, L, k_after=0, ev="INV"):
    """Both employed at m-1; H = 1 husband event at m, H = 0 husband employed and no INV at m..m+k_after.
    y = wife's event at any of m..m+k_after (NaN if a month unobserved)."""
    base = (P.E_h_l1 == 1) & (P.E_w_l1 == 1)
    h1 = P[f"{ev}_h"].to_numpy(float) == 1
    stay = np.ones(len(P), bool)
    y = np.zeros(len(P))
    for k in range(0, k_after + 1):
        e_h, i_h = L.at("E_h", k), L.at("INV_h", k)
        stay &= (e_h == 1) & (i_h == 0)
        wy = L.at(f"{ev}_w", k)
        y = y + np.where(np.isnan(wy), np.nan, wy)
    H = np.where(h1, 1.0, np.where(stay, 0.0, np.nan))
    d = P.loc[base].copy()
    d["H"] = H[base.to_numpy()]
    d["y"] = (y[base.to_numpy()] > 0).astype(float)
    d.loc[np.isnan(y[base.to_numpy()]), "y"] = np.nan
    return d[d.H.notna() & d.y.notna()].copy()


def same_month_block(d, label, table="1"):
    """Cells of the same-month table for one sample d (needs H, y, wgt_w)."""
    r = {}
    r["p1"] = wmean(d.y[d.H == 1], d.wgt_w[d.H == 1])
    r["p0"] = wmean(d.y[d.H == 0], d.wgt_w[d.H == 0])
    r["ph"] = wmean(d.H, d.wgt_w)
    r["phi"] = phi(d.H, d.y, d.wgt_w)
    w = lpm(d, "y", ["H"], fe=None, w="wgt_w")               # weighted difference, clustered
    b, a = w["b"]["H"], w["b"]["const"]
    V = w["V"]
    ratio = (a + b) / a
    g = np.array([-b / a ** 2, 1 / a])                         # d ratio / d(a, b)
    se_ratio = float(np.sqrt(g @ V.loc[["const", "H"], ["const", "H"]].to_numpy() @ g))
    r["diff"], r["ratio"], r["se_ratio"] = w, ratio, se_ratio
    r["fe_pm"] = lpm(d, "y", ["H"], fe="pm")
    r["fe_spm"] = lpm(d, "y", ["H"], fe="spm")
    r["n1"], r["nj"] = int((d.H == 1).sum()), int(((d.H == 1) & (d.y == 1)).sum())
    r["N"], r["G"] = len(d), d.hh.nunique()
    rec(table, label, "wife event", "weighted difference (no FE)", w)
    rec(table, label, "wife event", "panel-month FE", r["fe_pm"])
    rec(table, label, "wife event", "state x panel-month FE", r["fe_spm"])
    ROWS.append(dict(table=table, sample=label, outcome="wife event", spec="descriptive", term="ratio", b=ratio,
                     se=se_ratio, p=pval(b, w["se"]["H"]), N=r["N"], clusters=r["G"], ymean=np.nan,
                     p1=r["p1"], p0=r["p0"], phi=r["phi"], n_h=r["n1"], n_joint=r["nj"]))
    return r


def fmt_ratio(r):
    p = pval(r["diff"]["b"]["H"], r["diff"]["se"]["H"])
    pv = "<0.001" if p < 0.001 else f"{p:.3f}"
    return f"{r['ratio']:.1f}{stars(p)} ({r['se_ratio']:.1f}; p={pv})"


def table_sm(cols, colnames):
    """Markdown for same-month style blocks (dict of results by column)."""
    L = ["| | " + " | ".join(colnames) + " |", "|---|" + "---|" * len(colnames)]

    def row(name, f):
        L.append(f"| {name} | " + " | ".join(f(c) for c in cols) + " |")
    row("P(wife event \\| husband event)", lambda c: f"{c['p1']:.4f}")
    row("P(wife event \\| husband employed, no event)", lambda c: f"{c['p0']:.4f}")
    row("Difference (weighted LPM, no FE)", lambda c: cell(c["diff"], nd=4))
    row("Ratio (delta-method s.e.; p for difference = 0)", fmt_ratio)
    row("P(husband event)", lambda c: f"{c['ph']:.4f}")
    row("Phi correlation", lambda c: f"{c['phi']:.3f}")
    row("Husband event: panel-month FE", lambda c: cell(c["fe_pm"], nd=4))
    row("Husband event: state x panel-month FE", lambda c: cell(c["fe_spm"], nd=4))
    row("N couple-months", lambda c: f"{c['N']:,}")
    row("N husband events / joint events", lambda c: f"{c['n1']:,} / {c['nj']:,}")
    row("Clusters (households)", lambda c: f"{c['G']:,}")
    return "\n".join(L)


# ---------------------------------------------------------------- event study
def event_study(P, L, sel=None, fe="spm", ev="INV"):
    base = (P.E_w_l1 == 1).to_numpy().copy()
    if sel is not None:
        base &= sel
    d = P.loc[base, ["hh", "pm", "spm", f"{ev}_w"]].copy()
    d = d.rename(columns={f"{ev}_w": "y"})
    xs = []
    for j in range(-LEADS, LAGS + 1):
        v = L.at(f"{ev}_h", -j)[base]
        nm = f"D{j}".replace("-", "m")
        d[nm] = np.nan_to_num(v, nan=0.0)
        d["M" + nm] = np.isnan(v).astype(float)
        xs += [nm, "M" + nm]
    r = lpm(d, "y", xs, fe=fe)
    js = list(range(-LEADS, LAGS + 1))
    names = [f"D{j}".replace("-", "m") for j in js]
    out = pd.DataFrame({"j": js, "b": [r["b"].get(n, np.nan) for n in names],
                        "se": [r["se"].get(n, np.nan) for n in names]})

    def lin(sub):
        sub = [n for n in sub if n in r["b"]]
        g = np.ones(len(sub))
        return float(sum(r["b"][n] for n in sub)), float(np.sqrt(g @ r["V"].loc[sub, sub].to_numpy() @ g))
    r["sum_0_12"] = lin([f"D{j}" for j in range(0, LAGS + 1)])
    r["sum_1_12"] = lin([f"D{j}" for j in range(1, LAGS + 1)])
    r["sum_m6_m1"] = lin([f"Dm{j}" for j in range(1, LEADS + 1)])
    return out, r


# ---------------------------------------------------------------- added-worker path
def aw_base(P, L, wife="ne"):
    """Base months b: husband employed at b; wife non-employed ('ne'), employed ('e') or any ('all') at b.
    H = 1 husband INV at b+1, H = 0 husband employed at b+1 without INV."""
    hE = P.E_h.to_numpy() == 1
    wsel = {"ne": P.E_w.to_numpy() == 0, "e": P.E_w.to_numpy() == 1, "all": np.ones(len(P), bool)}[wife]
    inv1, e1 = L.at("INV_h", 1), L.at("E_h", 1)
    H = np.where(inv1 == 1, 1.0, np.where((e1 == 1) & (inv1 == 0), 0.0, np.nan))
    base = hE & wsel & ~np.isnan(H)
    return base, H


def aw_path(P, L, base, H, outcome, sel=None, ss=range(-6, AW_S + 1), excl_joint=False, diff=False):
    b0 = base.copy()
    if sel is not None:
        b0 &= sel
    if excl_joint:
        j1, j2 = L.at("INV_w", 1), L.at("INV_w", 2)
        b0 &= ~((j1 == 1) | (j2 == 1))
    out = []
    for s in ss:
        y = L.at(outcome, 1 + s)
        if diff:                                   # change since the base month b = tau-1
            y = y - L.at(outcome, 0)
        ok = b0 & ~np.isnan(y)
        d = pd.DataFrame({"y": y[ok], "H": H[ok], "pm": P.pm.to_numpy()[ok], "hh": P.hh.to_numpy()[ok],
                          "w": P.wgt_w.to_numpy()[ok]})
        if (d.H == 1).sum() < 20 or d.y.std() == 0:
            continue
        r = lpm(d, "y", ["H"], fe="pm")
        out.append(dict(s=s, b=r["b"]["H"], se=r["se"]["H"], N=r["N"], G=r["G"], n1=int((d.H == 1).sum()),
                        p1=wmean(d.y[d.H == 1], d.w[d.H == 1]), p0=wmean(d.y[d.H == 0], d.w[d.H == 0])))
    return pd.DataFrame(out)


# ---------------------------------------------------------------- main
def main():
    P = build_panel()
    P, L = add_vars(P)
    md = []
    A = md.append
    A("# Joint job loss within married couples: SIPP 2004, 2008 and 2014 panels\n")
    A("Built by `IGE/40.SIPPJointLoss.py` (2026-10-17; definitions in its docstring). Public-use SIPP core files "
      "(2004 and 2008 panels from the NBER mirror, 2014 panel from the Census Bureau); married couples who name each "
      "other as spouse, both aged 20-60, followed month by month. **Involuntary separation (INV)** = an employer job "
      "ends in the month for layoff / slack work, closure (bankrupt, sold, plant closed), discharge, temporary job "
      "ended or other involuntary reason (reason-for-leaving item, not the CPS's unemployment reason). Probabilities "
      "are weighted by the wife's person weight; regressions are unweighted linear probability models with s.e. "
      "clustered by household. Cells: coefficient*** (s.e.; p); *** p<0.01, ** p<0.05, * p<0.1. 'Panel-month FE' = "
      "panel x rotation group x calendar month (absorbs the interview seam, which differs across rotation groups); "
      "'state x panel-month FE' adds the state. Associations, not causal effects.\n")

    # ---- 0. data
    A("## 0. Data\n")
    g = P.groupby("panel")
    dd = pd.DataFrame({"couple-months": g.size(), "couples": g.cid.nunique(), "households": g.hh.nunique(),
                       "first month": g.ym.min().map(lambda v: f"{v // 12}-{v % 12 + 1:02d}"),
                       "last month": g.ym.max().map(lambda v: f"{v // 12}-{v % 12 + 1:02d}"),
                       "months per couple (mean)": g.size() / g.cid.nunique(),
                       "share Black husband": g.black.mean(), "both employed": g.apply(lambda x: ((x.E_h == 1) & (x.E_w == 1)).mean()),
                       "husband INV per employed month": g.apply(lambda x: x.INV_h[x.E_h_l1 == 1].mean()),
                       "wife INV per employed month": g.apply(lambda x: x.INV_w[x.E_w_l1 == 1].mean()),
                       "both self-respondents": g.self2.mean()})
    A("| Panel | " + " | ".join(dd.columns) + " |")
    A("|---|" + "---|" * len(dd.columns))
    for p_, r in dd.iterrows():
        A(f"| {p_} | " + " | ".join(f"{v:,}" if isinstance(v, (int, np.integer)) else (f"{v:.3f}" if isinstance(v, float) else str(v)) for v in r.values) + " |")
    A(f"\nAll panels: {len(P):,} couple-months, {P.cid.nunique():,} couples, {P.hh.nunique():,} households.\n")
    # reasons
    rr = []
    for s, nm in (("h", "husbands"), ("w", "wives")):
        sep = P[(P[f"SEP_{s}"] == 1) & (P[f"E_{s}_l1"] == 1)]
        vc = sep.groupby("panel")[f"rs_{s}"].value_counts(normalize=True).unstack(0).fillna(0)
        vc.index = [RSNAME.get(i, "missing") for i in vc.index]
        rr.append((nm, vc, sep.groupby("panel").size()))
    A("Reasons for separations from employer jobs (share of separations of persons employed the month before):\n")
    A("| Reason | " + " | ".join(f"{nm} {p_}" for nm, vc, _ in rr for p_ in vc.columns) + " |")
    A("|---|" + "---|" * sum(len(vc.columns) for _, vc, _ in rr))
    idx = list(RSNAME.values())
    for rn in idx:
        A(f"| {rn} | " + " | ".join(f"{vc.loc[rn, p_]:.3f}" if rn in vc.index else "0" for _, vc, _ in rr for p_ in vc.columns) + " |")
    A("| N separations | " + " | ".join(f"{n[p_]:,}" for _, vc, n in rr for p_ in vc.columns) + " |\n")
    # seam heaping
    s0 = P[(P.E_h_l1 == 1)].copy()
    s0["pos"] = np.where(s0.panel == 2014, np.where(s0.month == 1, "Jan (seam)", "Feb-Dec"),
                         s0.refmon.map({1: "ref. month 1 (seam)", 2: "ref. month 2", 3: "ref. month 3", 4: "ref. month 4"}))
    heap = s0.groupby(["panel", "pos"]).INV_h.mean()
    A("Husband's monthly INV hazard (employed the month before) by position in the wave: " + "; ".join(
        f"{p_} {pos}: {v:.4f}" for (p_, pos), v in heap.items()) +
      ". In the 2004/2008 panels the dated job endings pile up in the most recent reference months (recall), not at "
      "the seam. Spouses are interviewed together, so dating errors can create or destroy same-month coincidences: the "
      "off-seam and 1-2 month window rows are the checks.\n")

    # ---- 1. same-month
    A("## 1. Joint involuntary separation: wife's probability by the husband's transition\n")
    A("Both spouses employed at m-1. H = 1: husband has an involuntary separation in month m; H = 0: husband employed "
      "in m (through the end of the window) without an involuntary separation. Wife's event: involuntary separation "
      "in the window. Columns (1)-(3) correspond to the CPS columns 'same month', 'within 1 month after', 'within 2 "
      "months after'; column (4) is a 12-month window (CPS / PSID one-year comparisons in section 6).\n")
    wins = [(0, "(1) Same month (m)"), (1, "(2) Within 1 month after (m..m+1)"), (2, "(3) Within 2 months after (m..m+2)"),
            (11, "(4) Within 12 months (m..m+11)")]
    res1 = {}
    for k, nm in wins:
        d = jl_sample(P, L, k)
        res1[k] = same_month_block(d, nm, "1")
    A(table_sm([res1[k] for k, _ in wins], [nm for _, nm in wins]))
    A("")
    # definitions
    A("\n**Alternative event definitions, same month** (both employed at m-1; husband and wife events defined alike)\n")
    defs = {}
    for ev, nm in (("INV", "(1) Involuntary (baseline)"), ("INVN", "(2) Layoff / closure only"),
                   ("JL", "(3) CPS-like: involuntary and no job in m+1"), ("SEP", "(4) Any separation"),
                   ("QUIT", "(5) Quit / personal (placebo-type)")):
        d = jl_sample(P, L, 0, ev=ev)
        defs[ev] = same_month_block(d, nm, "1b")
    A(table_sm(list(defs.values()), list(n for n in ("(1) Involuntary (baseline)", "(2) Layoff / closure only",
                                                      "(3) CPS-like: involuntary and no job in m+1",
                                                      "(4) Any separation", "(5) Quit / personal (placebo-type)"))))
    A("")

    # ---- 2. robustness, samples as row panels
    A("\n## 2. Same-month joint involuntary separation: fixed effects and samples\n")
    A("**Outcome: Wife involuntary separation in month m** (both employed at m-1; H as in section 1, column 1). "
      "Controls: age group (20-29/30-39/40-49/50-60) and education (<HS, HS, some college, BA+) of each spouse, "
      "husband's race, youngest own child (none / 0-5 / 6-17).\n")
    d0 = jl_sample(P, L, 0)
    C = controls(d0)
    d0 = pd.concat([d0, C], axis=1)
    cnames = list(C.columns)
    specs = [("(1) none", None, []), ("(2) panel-month FE", "pm", []), ("(3) state x panel-month FE", "spm", []),
             ("(4) (3) + controls", "spm", cnames)]
    samples = [("All", np.ones(len(d0), bool)), ("2004 panel", d0.panel == 2004), ("2008 panel", d0.panel == 2008),
               ("2014 panel", d0.panel == 2014), ("Off-seam months (m-1, m in the same wave)", d0.seam == 0),
               ("Seam months", d0.seam == 1), ("Both spouses self-respondents in m", d0.self2 == 1),
               ("Neither spouse a non-interview (imputed, Type Z)", (d0.intv_h <= 2) & (d0.intv_w <= 2)),
               ("Black husbands", d0.race_h == 2), ("White husbands", d0.race_h == 1),
               ("Excluding 2008-09 recession months (Dec 2007 - Jun 2009)", ~d0.ym.between(2007 * 12 + 11, 2009 * 12 + 5))]
    A("| | " + " | ".join(s[0] for s in specs) + " |")
    A("|---|" + "---|" * len(specs))
    for sn, sel in samples:
        ds = d0[np.asarray(sel)]
        if ds.H.sum() < 5:
            continue
        cells, ns = [], []
        for spn, fe, ctr in specs:
            r = lpm(ds, "y", ["H"] + ctr, fe=fe)
            rec("2", sn, "wife INV (m)", spn, r)
            cells.append(cell(r, nd=4))
            ns.append(f"{r['N']:,}")
        A(f"| **{sn}** | | | | |")
        A("| Husband involuntary separation (m) | " + " | ".join(cells) + " |")
        A(f"| Mean of outcome (H = 0) / husband events / joint | {ds.y[ds.H == 0].mean():.4f} / {int(ds.H.sum()):,} / "
          f"{int((ds.H * ds.y).sum()):,} | | | |")
        A("| N couple-months | " + " | ".join(ns) + " |")
    A("\nFE / clusters: column (1) none, (2) panel x rotation x calendar month, (3)-(4) state x panel x rotation x "
      f"calendar month; s.e. clustered by household ({d0.hh.nunique():,} households in the full sample).\n")

    # same industry
    A("**Shared industry / occupation** (outcome: wife INV in m; state x panel-month FE + controls; spouses' main job at "
      "m-1; sample: both industries known)\n")
    di = d0[d0.ind_known == 1].copy()
    for c in ("same_ind", "same_ind4", "same_occ"):
        di["Hx" + c] = di.H * di[c]
    cols = [("(1) baseline", ["H"]), ("(2) x same major industry", ["H", "same_ind", "Hxsame_ind"]),
            ("(3) x same detailed industry", ["H", "same_ind4", "Hxsame_ind4"]),
            ("(4) x same major occupation", ["H", "same_occ", "Hxsame_occ"]),
            ("(5) all three", ["H", "same_ind", "Hxsame_ind", "same_ind4", "Hxsame_ind4", "same_occ", "Hxsame_occ"])]
    rs_ = [lpm(di, "y", xs + cnames, fe="spm") for _, xs in cols]
    for (cn, xs), r in zip(cols, rs_):
        for x in xs:
            rec("2b", "both industries known", "wife INV (m)", cn, r, x=x)
    A("| | " + " | ".join(c for c, _ in cols) + " |")
    A("|---|" + "---|" * len(cols))
    for x, nm in (("H", "Husband INV (m)"), ("same_ind", "Same major industry"), ("Hxsame_ind", "H x same major industry"),
                  ("same_ind4", "Same detailed industry"), ("Hxsame_ind4", "H x same detailed industry"),
                  ("same_occ", "Same major occupation"), ("Hxsame_occ", "H x same major occupation")):
        A(f"| {nm} | " + " | ".join(cell(r, x, 4) for r in rs_) + " |")
    A("| Controls; FE | " + " | ".join("yes; state x panel-month" for _ in rs_) + " |")
    A("| N couple-months | " + " | ".join(f"{r['N']:,}" for r in rs_) + " |")
    shares = (di.same_ind.mean(), di.same_ind4.mean(), di.same_occ.mean())
    ps = {}
    for c in ("same_ind", "same_ind4"):
        for v in (1, 0):
            dv = di[di[c] == v]
            ps[(c, v)] = (wmean(dv.y[dv.H == 1], dv.wgt_w[dv.H == 1]), wmean(dv.y[dv.H == 0], dv.wgt_w[dv.H == 0]),
                          int((dv.H == 1).sum()))
    A(f"\nShare of couples with the same major industry {shares[0]:.3f}, same detailed industry {shares[1]:.3f}, same "
      f"major occupation {shares[2]:.3f}. P(wife INV | husband INV) vs | husband no INV: same major industry "
      f"{ps[('same_ind', 1)][0]:.4f} vs {ps[('same_ind', 1)][1]:.4f} (N husband events {ps[('same_ind', 1)][2]:,}); different major "
      f"industry {ps[('same_ind', 0)][0]:.4f} vs {ps[('same_ind', 0)][1]:.4f} ({ps[('same_ind', 0)][2]:,}); same detailed industry "
      f"{ps[('same_ind4', 1)][0]:.4f} vs {ps[('same_ind4', 1)][1]:.4f} ({ps[('same_ind4', 1)][2]:,}).\n")

    # ---- 3. event study
    A("## 3. Timing: wife's monthly involuntary-separation hazard around the husband's (tau-6 .. tau+12)\n")
    A("Sample: wife employed at m-1 (at risk). Regressors: husband INV at m-j (j > 0: his separation j months before; "
      "j < 0: after), j = -6..12, each with an indicator for his status unobserved at m-j. Coefficients are excess "
      "hazards relative to months more than 6 months before / 12 months after his separation and couples without one.\n")
    ev = {}
    for nm, sel, fe in (("All, state x panel-month FE", None, "spm"), ("All, panel-month FE", None, "pm"),
                        ("Off-seam months, state x panel-month FE", (P.seam == 0).to_numpy(), "spm"),
                        ("Black husbands", (P.race_h == 2).to_numpy(), "spm"),
                        ("White husbands", (P.race_h == 1).to_numpy(), "spm")):
        ev[nm] = event_study(P, L, sel, fe)
        for _, row in ev[nm][0].iterrows():
            ROWS.append(dict(table="3", sample=nm, outcome="wife INV hazard", spec=fe, term=f"tau{int(row.j):+d}",
                             b=row.b, se=row.se, p=pval(row.b, row.se), N=ev[nm][1]["N"], clusters=ev[nm][1]["G"],
                             ymean=ev[nm][1]["ymean"]))
    evn = list(ev)
    A("| Month relative to husband's INV | " + " | ".join(f"({i + 1}) {n}" for i, n in enumerate(evn)) + " |")
    A("|---|" + "---|" * len(evn))
    for j in range(-LEADS, LAGS + 1):
        A(f"| tau{j:+d} | " + " | ".join(fmt(*ev[n][0].loc[ev[n][0].j == j, ["b", "se"]].iloc[0].tolist(), nd=4)
                                         for n in evn) + " |")
    for key, nm in (("sum_m6_m1", "Sum tau-6..tau-1"), ("sum_0_12", "Sum tau..tau+12"), ("sum_1_12", "Sum tau+1..tau+12")):
        A(f"| {nm} | " + " | ".join(fmt(*ev[n][1][key], nd=4) for n in evn) + " |")
    A("| Mean wife INV hazard | " + " | ".join(f"{ev[n][1]['ymean']:.4f}" for n in evn) + " |")
    A("| N wife-months / households | " + " | ".join(f"{ev[n][1]['N']:,} / {ev[n][1]['G']:,}" for n in evn) + " |\n")
    for n in evn:
        for key in ("sum_m6_m1", "sum_0_12", "sum_1_12"):
            b, se = ev[n][1][key]
            ROWS.append(dict(table="3", sample=n, outcome="wife INV hazard", spec="sum", term=key, b=b, se=se,
                             p=pval(b, se), N=ev[n][1]["N"], clusters=ev[n][1]["G"], ymean=ev[n][1]["ymean"]))

    # ---- 4. added worker
    A("## 4. Added-worker path: wives without a job when the husband separates\n")
    A("Base month b = tau-1: husband employed, wife with no job all month. H = 1: husband INV at tau = b+1; H = 0: "
      "husband employed at tau without INV. Outcome at tau+s. LPM of the outcome on H with base panel-month FE; "
      "P(.) weighted by the wife's weight at b. Couples observed at tau+s only (attrition / divorce drop out). "
      "Columns s < 0 are the months before his separation: a positive difference there means the wives of men about "
      "to separate had left a job more recently (employment) or were already looking (search); the row panel 'No job "
      "at any of tau-6..tau-1' removes the recent leavers.\n")
    base_ne, H = aw_base(P, L, "ne")
    yc = P.yc_cat.to_numpy()
    strict = np.ones(len(P), bool)
    for k in range(0, 6):                          # b-5 .. b = tau-6 .. tau-1
        strict &= L.at("E_w", -k) == 0
    groups = [("All", None), ("Youngest child 0-5", yc == "0-5"), ("Youngest child 6-17", yc == "6-17"),
              ("No child < 18", yc == "none"), ("Black husbands", (P.race_h == 2).to_numpy()),
              ("White husbands", (P.race_h == 1).to_numpy()),
              ("No job at any of tau-6..tau-1 (observed)", strict)]
    aw = {}
    for gname, sel in groups:
        for o in ("E_w", "LK_w"):
            aw[(gname, o)] = aw_path(P, L, base_ne, H, o, sel)
    aw_h = aw_path(P, L, base_ne, H, "E_h")
    show = [-6, -3, 0, 1, 2, 3, 6, 12, 18, 24, 30, 36]
    for o, oname in (("E_w", "Wife employed at tau+s"), ("LK_w", "Wife looking for work / on layoff at tau+s")):
        A(f"**Outcome: {oname}** (one LPM per cell: column = months since his separation, row panel = sample)\n")
        A("| | " + " | ".join(f"s = {s}" for s in show) + " |")
        A("|---|" + "---|" * len(show))
        for gname, _ in groups:
            t = aw[(gname, o)].set_index("s")
            A(f"| **{gname}** |" + " |" * len(show))
            A("| Husband INV at tau | " + " | ".join(fmt(t.loc[s, "b"], t.loc[s, "se"]) if s in t.index else "-" for s in show) + " |")
            A("| P(outcome) H = 1 / H = 0 | " + " | ".join(f"{t.loc[s, 'p1']:.3f} / {t.loc[s, 'p0']:.3f}" if s in t.index else "-" for s in show) + " |")
            A("| N base months (H = 1) | " + " | ".join(f"{int(t.loc[s, 'N']):,} ({int(t.loc[s, 'n1']):,})" if s in t.index else "-" for s in show) + " |")
            for s_, row in t.iterrows():
                ROWS.append(dict(table="4", sample=f"non-employed wives: {gname}", outcome=o, spec="base panel-month FE",
                                 term=f"s={s_}", b=row.b, se=row.se, p=pval(row.b, row.se), N=row.N, clusters=row.G,
                                 ymean=np.nan, p1=row.p1, p0=row.p0, n_h=row.n1))
        A("| FE | base panel x rotation x calendar month |" + " |" * (len(show) - 1))
        A("")
    t = aw_h.set_index("s")
    A("Husband's own employment (same sample): " + "; ".join(
        f"s={s}: H=1 {t.loc[s, 'p1']:.3f} vs H=0 {t.loc[s, 'p0']:.3f}" for s in (0, 1, 3, 6, 12, 24, 36) if s in t.index) + ".\n")
    for s_, row in t.iterrows():
        ROWS.append(dict(table="4", sample="non-employed wives: All", outcome="E_h", spec="base panel-month FE",
                         term=f"s={s_}", b=row.b, se=row.se, p=pval(row.b, row.se), N=row.N, clusters=row.G,
                         ymean=np.nan, p1=row.p1, p0=row.p0, n_h=row.n1))

    # gross vs net
    A("**Gross vs net added work. Outcome: change in wife employed between tau-1 and tau+s** (husband employed at "
      "tau-1; H as above; the change removes level differences between the wives of men who do and do not separate)\n")
    base_e, He = aw_base(P, L, "e")
    base_all, Ha = aw_base(P, L, "all")
    gn = [("Gross entry: wives without a job at tau-1", aw_path(P, L, base_ne, H, "E_w", diff=True)),
          ("Gross entry, strict: no job at any of tau-6..tau-1", aw_path(P, L, base_ne, H, "E_w", sel=strict, diff=True)),
          ("Wives employed at tau-1", aw_path(P, L, base_e, He, "E_w", diff=True)),
          ("Wives employed at tau-1, excluding own INV at tau or tau+1", aw_path(P, L, base_e, He, "E_w", excl_joint=True, diff=True)),
          ("Net: all wives", aw_path(P, L, base_all, Ha, "E_w", diff=True)),
          ("Net without joint losers: all wives excluding own INV at tau or tau+1", aw_path(P, L, base_all, Ha, "E_w", excl_joint=True, diff=True))]
    A("| | " + " | ".join(f"s = {s}" for s in show) + " |")
    A("|---|" + "---|" * len(show))
    for gname, t in gn:
        t = t.set_index("s")
        A(f"| **{gname}** |" + " |" * len(show))
        A("| Husband INV at tau | " + " | ".join(fmt(t.loc[s, "b"], t.loc[s, "se"]) if s in t.index else "-" for s in show) + " |")
        A("| Mean change H = 1 / H = 0 | " + " | ".join(f"{t.loc[s, 'p1']:.3f} / {t.loc[s, 'p0']:.3f}" if s in t.index else "-" for s in show) + " |")
        A("| N base months (H = 1) | " + " | ".join(f"{int(t.loc[s, 'N']):,} ({int(t.loc[s, 'n1']):,})" if s in t.index else "-" for s in show) + " |")
        for s_, row in t.iterrows():
            ROWS.append(dict(table="4b", sample=gname, outcome="E_w", spec="base panel-month FE", term=f"s={s_}", b=row.b,
                             se=row.se, p=pval(row.b, row.se), N=row.N, clusters=row.G, ymean=np.nan, p1=row.p1,
                             p0=row.p0, n_h=row.n1))
    A("| FE | base panel x rotation x calendar month |" + " |" * (len(show) - 1))
    shr = d0[d0.H == 1]
    A(f"\nShare of wives employed at tau-1 among couples with a husband INV (both-employed sample at tau-1 is section 1): "
      f"{wmean(P.E_w.to_numpy()[base_all & (Ha == 1)], P.wgt_w.to_numpy()[base_all & (Ha == 1)]):.3f}; of these, "
      f"share with their own INV in the same month: {wmean(shr.y, shr.wgt_w):.3f}.\n")

    # ---- 5. race summary
    A("## 5. By race (husband's race)\n")
    A("Same-month LPMs: section 2 row panels 'Black husbands' / 'White husbands'; event-study sums: section 3 columns "
      "(4)-(5); added-worker paths: section 4 row panels. Interaction test, same month (state x panel-month FE + "
      "controls; Black and White husbands only):\n")
    dr = d0[d0.race_h.isin([1, 2])].copy()
    dr["Hxblack"] = dr.H * dr.black
    r = lpm(dr, "y", ["H", "Hxblack", "black"] + [c for c in cnames if not c.startswith("race")], fe="spm")
    rec("5", "Black + White husbands", "wife INV (m)", "state x panel-month FE + controls", r, "H")
    rec("5", "Black + White husbands", "wife INV (m)", "state x panel-month FE + controls", r, "Hxblack")
    A("| | (1) Wife INV in month m |")
    A("|---|---|")
    A(f"| Husband INV (m) | {cell(r, 'H', 4)} |")
    A(f"| H x Black husband | {cell(r, 'Hxblack', 4)} |")
    A(f"| Black husband | {cell(r, 'black', 4)} |")
    A(f"| Controls; FE | yes; state x panel-month |")
    A(f"| N couple-months / households | {r['N']:,} / {r['G']:,} |\n")
    awr = {}
    for s in (3, 12, 24, 36):
        tb, tw = aw[("Black husbands", "E_w")].set_index("s"), aw[("White husbands", "E_w")].set_index("s")
        if s in tb.index and s in tw.index:
            dB = tb.loc[s, "b"] - tw.loc[s, "b"]
            seB = np.sqrt(tb.loc[s, "se"] ** 2 + tw.loc[s, "se"] ** 2)
            awr[s] = (dB, seB)
            ROWS.append(dict(table="5", sample="non-employed wives", outcome="E_w", spec="Black - White (independent samples)",
                             term=f"s={s}", b=dB, se=seB, p=pval(dB, seB), N=np.nan, clusters=np.nan, ymean=np.nan))
    A("Added-worker employment effect, Black minus White (independent-sample s.e.): " + "; ".join(
        f"s={s}: {fmt(*v)}" for s, v in awr.items()) + ".\n")

    # ---- 6. comparison
    A("## 6. Comparison with the CPS and the PSID\n")
    A("CPS: `30.CPSJointJobLoss.py` (EVIDENCE 3.24-3.34; job loser = employed -> unemployed with a job-loser reason, "
      "state x month FE). PSID: `25.JointJobLoss.py`, `19.FatherDisplacement.py` (EVIDENCE 3.16-3.23; displacement = "
      "laid off / fired / plant closed, annual reports).\n")
    s1 = res1[0]
    s12 = res1[11]
    s2 = res1[2]
    jl = defs["JL"]
    e0 = ev["All, state x panel-month FE"][0].set_index("j")
    awt = aw[("All", "E_w")].set_index("s")
    awl = aw[("All", "LK_w")].set_index("s")
    A("| Moment | CPS | PSID | SIPP (this script) |")
    A("|---|---|---|---|")
    A(f"| Same month: P(w\\|h) vs P(w\\|h employed); ratio | 0.0545 vs 0.0054; 10.1 | - (annual) | {s1['p1']:.4f} vs {s1['p0']:.4f}; {fmt_ratio(s1)} |")
    A(f"| Same month, CPS-like definition (INV and no job in m+1) | (as above) | - | {jl['p1']:.4f} vs {jl['p0']:.4f}; {fmt_ratio(jl)} |")
    A(f"| Same month, LPM excess (finest FE) | +0.040*** (0.002; p<0.001), state x month | - | {cell(s1['fe_spm'], nd=4)}, state x panel-month |")
    A(f"| Within 2 months after: P(w\\|h) vs P(w\\|h employed); ratio | 0.0746 vs 0.0140; 5.3 | - | {s2['p1']:.4f} vs {s2['p0']:.4f}; {fmt_ratio(s2)} |")
    A(f"| One year: P(w\\|h) vs base; ratio | status t -> t+12: 0.0581 vs 0.0105; 5.5 | per couple-year (both working): 0.102 vs 0.039, +0.063*** (0.005; p<0.001); 2.6 | 12-month window m..m+11: {s12['p1']:.4f} vs {s12['p0']:.4f}; {fmt_ratio(s12)} |")
    A(f"| Timing: excess in the month before / of / after his loss | tau-1 +0.0071***, tau +0.040***, tau+1 +0.0084*** (monthly) | k=-1..+1 years: k=0 +0.036*** (0.011), k=+1 +0.024** (0.010) | tau-1 {fmt(e0.loc[-1, 'b'], e0.loc[-1, 'se'], 4)}, tau {fmt(e0.loc[0, 'b'], e0.loc[0, 'se'], 4)}, tau+1 {fmt(e0.loc[1, 'b'], e0.loc[1, 'se'], 4)} |")
    def aws(s):
        return fmt(awt.loc[s, "b"], awt.loc[s, "se"]) if s in awt.index else "-"
    A(f"| Added worker, non-employed wives, employment: first months | t+1 +0.022***, t+2 +0.033***, t+3 +0.042*** | year of his loss: hours +3.8 (n.s.) | s=0 {aws(0)}, s=1 {aws(1)}, s=2 {aws(2)} |")
    A(f"| Added worker, employment one year on | t+12 +0.040*** (0.075 -> base 0.192) | years +1..+3: hours ~+50; youngest 0-5 emp +0.041*** | s=12 {aws(12)}, s=24 {aws(24)}, s=36 {aws(36)} |")
    A(f"| Added worker, search (looking / on layoff) | unemployed t+1 +0.088***, t+12 +0.039*** | - | s=0 {fmt(awl.loc[0, 'b'], awl.loc[0, 'se'])}, s=12 {fmt(awl.loc[12, 'b'], awl.loc[12, 'se'])} |")
    A("")
    A("Notes: the CPS 'job loser' requires unemployment after the loss and the CPS window ends after 4 months; the SIPP "
      "uses the reason a job ended (also when a new job follows immediately) and follows couples for up to 4-5 years; "
      "the PSID is annual. The SIPP 12-month window is cumulative (any event in m..m+11), the CPS one-year column "
      "compares statuses 12 months apart.\n")

    OUT.mkdir(exist_ok=True)
    (OUT / "sipp_joint_loss.md").write_text("\n".join(md), encoding="utf-8")
    pd.DataFrame(ROWS).to_csv(OUT / "sipp_joint_loss.csv", index=False)
    plot(ev, aw, gn, OUT / "sipp_joint_loss.png")
    print("done", flush=True)


def plot(ev, aw, gn, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ink, ink2, grid, surf = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    c1, c2, c3 = "#2a78d6", "#eb6834", "#1baf7a"
    fig, axs = plt.subplots(2, 2, figsize=(13, 9.5), facecolor=surf)
    axs = axs.ravel()
    for ax in axs:
        ax.set_facecolor(surf)
        ax.grid(color=grid, lw=0.8)
        ax.set_axisbelow(True)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        for sp in ("left", "bottom"):
            ax.spines[sp].set_color(grid)
        ax.tick_params(colors=ink2, labelsize=8)
        ax.axhline(0, color=ink2, lw=0.8)
    ax = axs[0]
    e = ev["All, state x panel-month FE"][0]
    ax.errorbar(e.j, 100 * e.b, yerr=196 * e.se, color=c1, lw=2, marker="o", ms=7, capsize=0, elinewidth=1.2,
                label="all months")
    e2 = ev["Off-seam months, state x panel-month FE"][0]
    ax.errorbar(e2.j + 0.25, 100 * e2.b, yerr=196 * e2.se, color=c2, lw=0, marker="o", ms=6, capsize=0,
                elinewidth=1.0, label="off-seam months only")
    ax.axvline(0, color=ink2, lw=0.8, ls=":")
    ax.set_xticks(range(-LEADS, LAGS + 1, 2))
    ax.set_xlabel("month relative to husband's involuntary separation (tau)", color=ink2)
    ax.set_ylabel("excess monthly hazard of wife's involuntary separation (pp)", color=ink2)
    ax.set_title("A. Wife's involuntary separation around his (95% CI)", fontsize=10, color=ink, loc="left")
    ax.legend(frameon=False, fontsize=8, labelcolor=ink2)
    for ax, o, ttl in ((axs[1], "E_w", "B. Non-employed wives: employment"), (axs[2], "LK_w", "C. Non-employed wives: looking / on layoff")):
        for (gname, col) in (("Youngest child 0-5", c1), ("Youngest child 6-17", c2), ("No child < 18", c3)):
            t = aw[(gname, o)]
            ax.plot(t.s, 100 * t.b, color=col, lw=2, label=gname.lower())
            ax.fill_between(t.s, 100 * (t.b - 1.96 * t.se), 100 * (t.b + 1.96 * t.se), color=col, alpha=0.12, lw=0)
        ax.set_xlabel("months since husband's involuntary separation (s)", color=ink2)
        ax.set_ylabel("effect of his separation (pp; 95% CI)", color=ink2)
        ax.set_title(ttl, fontsize=10, color=ink, loc="left")
        ax.legend(frameon=False, fontsize=8, labelcolor=ink2)
    ax = axs[3]
    labs = ["gross: wives without a job at tau-1", "gross, strict: no job tau-6..tau-1", "net: all wives",
            "net, excluding wives' own loss at tau, tau+1"]
    for (gname, t), col, lab in zip([gn[0], gn[1], gn[4], gn[5]], (c1, "#eda100", c2, c3), labs):
        ax.plot(t.s, 100 * t.b, color=col, lw=2, label=lab)
        ax.fill_between(t.s, 100 * (t.b - 1.96 * t.se), 100 * (t.b + 1.96 * t.se), color=col, alpha=0.12, lw=0)
    ax.set_xlabel("months since husband's involuntary separation (s)", color=ink2)
    ax.set_ylabel("effect on change in wife employed since tau-1 (pp)", color=ink2)
    ax.set_title("D. Gross vs net added work", fontsize=10, color=ink, loc="left")
    ax.legend(frameon=False, fontsize=8, labelcolor=ink2)
    fig.text(0.01, 0.005, "SIPP 2004, 2008, 2014 panels, married couples aged 20-60. Involuntary separation = job ended "
             "for layoff / slack work, closure, discharge, temporary job ended.\nLPMs with panel-month (B-D) or state x "
             "panel-month (A) FE, s.e. clustered by household. Associations, not causal effects.", fontsize=7.5, color=ink2)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(path, dpi=160, facecolor=surf)
    plt.close(fig)


if __name__ == "__main__":
    if "--download-only" in sys.argv:
        download()
    elif "--extract-only" in sys.argv:
        for panel, nw in PANELS.items():
            if str(panel) in sys.argv or not any(str(p) in sys.argv for p in PANELS):
                for w in range(1, nw + 1):
                    if src(panel, w)[1].exists():
                        extract(panel, w)
    else:
        download()
        main()
