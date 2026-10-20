r"""Fathers' job displacement in the PSID: the family's response and children's outcomes (2026-10-17).

Replaces the zero-hours "father figure's job loss" of 9.ChildExposure.py with the PSID's reason-for-job-end items
(Stevens 1997; Stephens 2002; Page, Stevens and Lindo 2009). Reads the raw family files in Dropbox/PSID (read only)
and IGE/data/psid_person_year.pkl, psid_child_exposure.pkl, psid_kids.pkl, cds_scores.pkl (read only); writes
  IGE/data/psid_displacement.pkl    one row per male head x calendar year with a reported job end (flags below)
  IGE/output/father_displacement.csv  every estimate (table, sample, outcome, regressor, coef, se, p, N)
  IGE/output/father_displacement.md   tables
  IGE/output/father_displacement_es.png  event-study figure

1. DISPLACEMENT (male heads; head's own report; codes are the same in every wave: 1 company folded / changed hands /
   moved out of town / employer died / went out of business; 2 strike, lockout; 3 laid off, fired; 4 quit,
   resigned, retired, pregnant, wanted a change; 5 first job / not working before (1968-1987 E branch), but
   2021-2023 "laid off / furloughed due to coronavirus"; 6 self-employed before (to 1975) / promotion (1975-1987
   E branch); 7 other, transfer, armed services; 8 job completed, seasonal, temporary; 9 NA; 0 inap.)
     main     = 1 or 3 (or 5 in 2021-2023): plant closed / moved or laid off / fired (Stevens; PSL "layoffs")
     strict   = 1 only (closures; PSL's "firm closings")
     quit     = 4 (placebo)
   Branches: E = employed head, previous job / position / other main-job employer; U = unemployed head, last job
   (U2 = the employer before it, 1988-2001); R = retired / other not in the labor force who worked last year;
   J1-J4 = the four employers of the 2003-2023 employment history (job 1 = current or most recent main job).
   Dating to the calendar year the job ended: the reported end year where the wave has one; otherwise the year
   before the interview (the question covers the ~12 months since the last interview, mostly that year). Reports
   whose end year is more than two years before the interview year are dropped (old job losses), and a report
   undated in year y is dropped if the same man has a report of the same kind dated y - 1 (double reporting across
   the E and U branches of two interviews).
   Variables (wave: branch why-variable [condition] (end-year variable)):
     1968 E V201 [V196=1 working & V200 tenure <= 18 months (codes 1-2)]; U V201 [V196=2, head hours 1967 > 0]
     1969 E V643 [V642=1 job < 12 months]; U V651          1970 E V1282 [V1281=1]; U V1332
     1971 E V1988; U V2038    1972 E V2586; U V2638    1973 E V3119; U V3155    1974 E V3534; U V3571
     1975 E V3986; U V4026    (1971-1975 E asked only if job < 1 year; U undated: kept if head hours last year > 0)
     1976 E V4490; U V4556 (V4557); R V4584      1977 E V5399; U V5458 (V5459); R V5487
     1978 E V5890; U V5986 (V5987)               1979 E V6501; U V6559 (V6560)
     1980 E V7104; U V7161 (V7162); R V7185      1981 E V7727; U V7809 (V7810); R V7871
     1982 E V8391; U V8470 (V8471); R V8531      1983 E V9022; U V9107 (V9108); R V9181
     (1976-1983 E asked if present position < 12 months; R asked if worked for money last year)
     1984 E V10539 (V10534, else V10538; position began 1983+); U V10609 (V10611); R V10664
     1985 E V11679 (V11681); U V11764 (V11766)   1986 E V13079 (V13081); U V13160 (V13162)
     1987 E V14177 (V14179); U V14256 (V14258)
     1988 E V15240 (V15239); U V15328 (V15320 year last worked); U2 V15387 (V15386)
     1989 E V16741 (V16740); U V16843 (V16835); U2 V16902 (V16901)
     1990 E V18179 (V18178); U V18267 (V18259); U2 V18326 (V18325)
     1991 E V19479 (V19478); U V19567 (V19559); U2 V19626 (V19625)
     1992 E V20779 (V20778); U V20867 (V20859); U2 V20926 (V20925)
     1993 E V22551 (V22550); U V22655 (V22646); U2 V22717 (V22716)
     1994 E ER4023 (ER2161); U ER4034 (ER2326); U2 ER4039 (ER2406)
     1995 E ER6863 (ER5160); U ER6874 (ER5325); U2 ER6879 (ER5405)
     1996 E ER9114 (ER7256); U ER9125 (ER7421); U2 ER9130 (ER7501)
     1997 E ER12091 (ER10179); U ER12102 (ER10339); U2 ER12107 (ER10416)
     1999 E ER13310 (ER13309); U ER13498 (ER13478); U2 ER13563 (ER13562)
     2001 E ER17321 (ER17320); U ER17538 (ER17517); U2 ER17603 (ER17602)
     (1988-2001 E = an other main-job employer during the previous calendar year; U = last job if last worked in
     the previous calendar year or later; U2 = other employer of the unemployed. In 1999 and 2001 the year two
     before the interview (1997, 1999) is covered only through the U-branch end years.)
     2003-2023 J1-J4 "BC51 WHY LAST JOB END / WHY JOB ENDED--JOB k" with "BC6 ENDING YEAR--JOB k":
     2003 ER21184/ER21132, ER21216/ER21188, ER21248/ER21220, ER21280/ER21252; 2005 ER25173/ER25114, ER25205/ER25177,
     ER25237/ER25209, ER25269/ER25241; 2007 ER36178/ER36119, ER36210/ER36182, ER36242/ER36214, ER36274/ER36246;
     2009 ER42211/ER42154, ER42241/ER42215, ER42271/ER42245, ER42301/ER42275; 2011 ER47524/ER47466,
     ER47554/ER47528, ER47584/ER47558, ER47614/ER47588; 2013 ER53224/ER53166, ER53254/ER53228, ER53284/ER53258,
     ER53314/ER53288; 2015 ER60239/ER60181, ER60269/ER60243, ER60299/ER60273, ER60329/ER60303;
     2017 ER66242/ER66182, ER66272/ER66246, ER66302/ER66276, ER66332/ER66306; 2019 ER72242/ER72182,
     ER72272/ER72246, ER72302/ER72276, ER72332/ER72306; 2021 ER78247/ER78185, ER78277/ER78251, ER78307/ER78281,
     ER78337/ER78311; 2023 ER82234/ER82168, ER82264/ER82238, ER82294/ER82268, ER82324/ER82298
     (employers since January 1 of the year two before the interview, so the biennial gap is covered).
   Year codes: two digits through the 1994 wave (96 = "one of the two years, DK which" -> interview year - 1;
   97-99 DK/NA), four digits from 1995 (9996 -> interview year - 1; 9997-9999 DK/NA).
   Wives' items exist (D/E, DE branches) but are not used: the object is the father's displacement.
"""
import importlib.util
import warnings

import numpy as np
import pandas as pd

from common import DATA, OUT, HERE, stars

warnings.simplefilter("ignore", FutureWarning)
warnings.simplefilter("ignore", RuntimeWarning)


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


psid1 = _load("psid1", "1.PSID.py")
psid9 = _load("psid9", "9.ChildExposure.py")
WAVES, FAM, layout, read = psid1.WAVES, psid1.FAM, psid1.layout, psid1.read

# ---------------------------------------------------------------- reason-for-job-end items, heads
# (branch, why, [end-year vars], {condition var: allowed values})
S = {1968: [("E", "V201", [], {"V196": (1,), "V200": (1, 2)}), ("U", "V201", [], {"V196": (2,)})],
     1969: [("E", "V643", [], {"V642": (1,)}), ("U", "V651", [], {})],
     1970: [("E", "V1282", [], {"V1281": (1,)}), ("U", "V1332", [], {})],
     1971: [("E", "V1988", [], {}), ("U", "V2038", [], {})],
     1972: [("E", "V2586", [], {}), ("U", "V2638", [], {})],
     1973: [("E", "V3119", [], {}), ("U", "V3155", [], {})],
     1974: [("E", "V3534", [], {}), ("U", "V3571", [], {})],
     1975: [("E", "V3986", [], {}), ("U", "V4026", [], {})],
     1976: [("E", "V4490", [], {}), ("U", "V4556", ["V4557"], {}), ("R", "V4584", [], {})],
     1977: [("E", "V5399", [], {}), ("U", "V5458", ["V5459"], {}), ("R", "V5487", [], {})],
     1978: [("E", "V5890", [], {}), ("U", "V5986", ["V5987"], {})],
     1979: [("E", "V6501", [], {}), ("U", "V6559", ["V6560"], {})],
     1980: [("E", "V7104", [], {}), ("U", "V7161", ["V7162"], {}), ("R", "V7185", [], {})],
     1981: [("E", "V7727", [], {}), ("U", "V7809", ["V7810"], {}), ("R", "V7871", [], {})],
     1982: [("E", "V8391", [], {}), ("U", "V8470", ["V8471"], {}), ("R", "V8531", [], {})],
     1983: [("E", "V9022", [], {}), ("U", "V9107", ["V9108"], {}), ("R", "V9181", [], {})],
     1984: [("E", "V10539", ["V10534", "V10538"], {}), ("U", "V10609", ["V10611"], {}), ("R", "V10664", [], {})],
     1985: [("E", "V11679", ["V11681"], {}), ("U", "V11764", ["V11766"], {})],
     1986: [("E", "V13079", ["V13081"], {}), ("U", "V13160", ["V13162"], {})],
     1987: [("E", "V14177", ["V14179"], {}), ("U", "V14256", ["V14258"], {})]}
for w, e, ey, u, uy, u2, u2y in [
        (1988, "V15240", "V15239", "V15328", "V15320", "V15387", "V15386"),
        (1989, "V16741", "V16740", "V16843", "V16835", "V16902", "V16901"),
        (1990, "V18179", "V18178", "V18267", "V18259", "V18326", "V18325"),
        (1991, "V19479", "V19478", "V19567", "V19559", "V19626", "V19625"),
        (1992, "V20779", "V20778", "V20867", "V20859", "V20926", "V20925"),
        (1993, "V22551", "V22550", "V22655", "V22646", "V22717", "V22716"),
        (1994, "ER4023", "ER2161", "ER4034", "ER2326", "ER4039", "ER2406"),
        (1995, "ER6863", "ER5160", "ER6874", "ER5325", "ER6879", "ER5405"),
        (1996, "ER9114", "ER7256", "ER9125", "ER7421", "ER9130", "ER7501"),
        (1997, "ER12091", "ER10179", "ER12102", "ER10339", "ER12107", "ER10416"),
        (1999, "ER13310", "ER13309", "ER13498", "ER13478", "ER13563", "ER13562"),
        (2001, "ER17321", "ER17320", "ER17538", "ER17517", "ER17603", "ER17602")]:
    S[w] = [("E", e, [ey], {}), ("U", u, [uy], {}), ("U2", u2, [u2y], {})]
for w, pairs in {2003: "ER21184/ER21132 ER21216/ER21188 ER21248/ER21220 ER21280/ER21252",
                 2005: "ER25173/ER25114 ER25205/ER25177 ER25237/ER25209 ER25269/ER25241",
                 2007: "ER36178/ER36119 ER36210/ER36182 ER36242/ER36214 ER36274/ER36246",
                 2009: "ER42211/ER42154 ER42241/ER42215 ER42271/ER42245 ER42301/ER42275",
                 2011: "ER47524/ER47466 ER47554/ER47528 ER47584/ER47558 ER47614/ER47588",
                 2013: "ER53224/ER53166 ER53254/ER53228 ER53284/ER53258 ER53314/ER53288",
                 2015: "ER60239/ER60181 ER60269/ER60243 ER60299/ER60273 ER60329/ER60303",
                 2017: "ER66242/ER66182 ER66272/ER66246 ER66302/ER66276 ER66332/ER66306",
                 2019: "ER72242/ER72182 ER72272/ER72246 ER72302/ER72276 ER72332/ER72306",
                 2021: "ER78247/ER78185 ER78277/ER78251 ER78307/ER78281 ER78337/ER78311",
                 2023: "ER82234/ER82168 ER82264/ER82238 ER82294/ER82268 ER82324/ER82298"}.items():
    S[w] = [(f"J{k + 1}", p.split("/")[0], [p.split("/")[1]], {}) for k, p in enumerate(pairs.split())]
assert sorted(S) == WAVES


def end_year(v, w):
    """Decode a reported end year (see docstring); NaN if DK/NA/inap."""
    v = pd.to_numeric(v, errors="coerce")
    y = pd.Series(np.nan, index=v.index)
    y = y.mask(v.between(1901, 2025), v)
    if w <= 1994:
        y = y.mask(v.between(1, 95), 1900 + v)
        y = y.mask(v == 96, w - 1) if w >= 1985 else y
    y = y.mask(v == 9996, w - 1)
    return y


def reports(fam_hours):
    """All head reports of a job end: wave, int, branch, code, year, dated."""
    hh = fam_hours.set_index(["wave", "int"])["hh"]
    out = []
    for w in WAVES:
        folder = FAM / (f"fam{w}" if w < 1994 else f"fam{w}er")
        base = next(f for f in folder.glob("*.do") if "formats" not in f.name).with_suffix("")
        pos, labs = layout(base.with_suffix(".do"))
        idv = "V3" if w == 1968 else labs[1][0]
        cols = sorted({idv, *[c for br in S[w] for c in [br[1], *br[2], *br[3]]]})
        f = read(base, cols, pos)
        for br, why, yrs, cond in S[w]:
            m = pd.Series(True, index=f.index)
            for c, vals in cond.items():
                m &= f[c].isin(vals)
            code = f[why].where(m & f[why].between(1, 9))
            if yrs:
                y = end_year(f[yrs[0]], w)
                for c in yrs[1:]:
                    y = y.fillna(end_year(f[c], w))
                dated = y.notna()
                y = y.fillna(w - 1)
            else:
                y, dated = pd.Series(float(w - 1), index=f.index), pd.Series(False, index=f.index)
            r = pd.DataFrame({"wave": w, "int": f[idv], "branch": br, "why": why, "code": code, "year": y,
                              "dated": dated}).dropna(subset=["code"])
            if br == "U" and not yrs:                       # undated unemployed: worked last year
                h = hh.reindex(pd.MultiIndex.from_arrays([r["wave"], r["int"]])).to_numpy()
                r = r[h > 0]
            out.append(r)
    r = pd.concat(out, ignore_index=True)
    r["code"] = r["code"].astype(int)
    r = r[r["year"].between(r["wave"] - 2, r["wave"])]
    r["main"] = r["code"].isin([1, 3]) | ((r["code"] == 5) & (r["wave"] >= 2021))
    r["strict"] = r["code"] == 1
    r["layoff"] = r["main"] & ~r["strict"]
    r["quit"] = r["code"] == 4
    return r


def displacement(py, fam_hours):
    """Male head x year file of job ends (flags main / strict / layoff / quit)."""
    r = reports(fam_hours)
    hd = py[py["head"] & (py["female"] == 0)][["wave", "int", "pid", "fam68", "hrace"]].drop_duplicates(["wave", "int"])
    r = r.merge(hd, on=["wave", "int"], how="inner")
    r["year"] = r["year"].astype(int)
    rows = []
    for k in ("main", "strict", "layoff", "quit"):
        x = r[r[k]].sort_values(["pid", "year", "dated"], ascending=[True, True, False])
        x = x.drop_duplicates(["pid", "year"])
        prev = set(zip(x["pid"], x["year"] + 1))
        drop = (~x["dated"]) & pd.Series([(p, y) in prev for p, y in zip(x["pid"], x["year"])], index=x.index)
        x = x[~drop]
        rows.append(x[["pid", "year"]].assign(**{k: 1}))
    d = rows[0]
    for x in rows[1:]:
        d = d.merge(x, on=["pid", "year"], how="outer")
    d = d.fillna(0)
    info = r.sort_values(["pid", "year", "dated"], ascending=[True, True, False]).drop_duplicates(["pid", "year"])
    d = d.merge(info[["pid", "year", "wave", "branch", "why", "code", "dated", "fam68", "hrace"]], on=["pid", "year"],
                how="left")
    for k in ("main", "strict", "layoff", "quit"):
        d[k] = d[k].astype(int)
    return d.sort_values(["pid", "year"]).reset_index(drop=True), r


# ---------------------------------------------------------------- family panel: male heads x calendar year
def men_panel(py, fam):
    """Male heads (SRC + SEO, Black / White head's race) x calendar year t = wave - 1 with the outcomes."""
    hd = py[py["head"] & (py["female"] == 0) & py["hrace"].isin(["White", "Black"])]
    m = hd[["pid", "fam68", "wave", "int", "hrace", "age", "faminc", "hlab"]].drop_duplicates(["wave", "int"])
    m = m.merge(fam[["wave", "int", "hh", "wh", "afdc", "fs"]], on=["wave", "int"], how="left")
    wv = py[py["wife"]][["wave", "int", "pid"]].drop_duplicates(["wave", "int"]).rename(columns={"pid": "w_pid"})
    m = m.merge(wv, on=["wave", "int"], how="left")
    k = py[py["child"] & py["age"].between(0, 17)].groupby(["wave", "int"])["age"].agg(["size", "min"])
    k.columns = ["nkid", "youngest"]
    m = m.merge(k.reset_index(), on=["wave", "int"], how="left")
    m["nkid"] = m["nkid"].fillna(0)
    m["year"] = m["wave"] - 1
    m["wh"] = m["wh"].where(m["w_pid"].notna())
    return m.sort_values(["pid", "year"]).reset_index(drop=True)


ES_Y = [("hh", "Head's hours"), ("hlab", "Head's labor income"), ("w_hrs", "Wife's hours"),
        ("w_emp", "Wife employed"), ("faminc", "Family income"), ("bw_present", "Still with baseline wife"),
        ("afdc", "AFDC/TANF"), ("fs", "Food stamps")]
ES_E = [-3, -1, 0, 1, 2, 3, 4, 5, 6]           # reference e = -2
WIFE_Y = {"w_hrs", "w_emp", "bw_present"}


def stacks(m, d, kind):
    """Stacked panel (Cengiz et al. 2019): for each event year, men first displaced (kind) that year and clean
    controls (no main displacement - and for quits no quit - up to event year + 6); both with a child 0-17 in the
    family unit and positive hours at baseline (the last year observed among event year - 2, - 1)."""
    first = {k: d[d[k] == 1].groupby("pid")["year"].min() for k in ("main", "strict", "quit")}
    fm = m["pid"].map(first["main"]).fillna(9999)
    fk = m["pid"].map(first[kind]).fillna(9999)
    fq = m["pid"].map(first["quit"]).fillna(9999)
    b = pd.concat([m.assign(ev=m["year"] + 1, pri=0), m.assign(ev=m["year"] + 2, pri=1)])
    b = b.assign(fm=pd.concat([fm, fm]).to_numpy(), fk=pd.concat([fk, fk]).to_numpy(),
                 fq=pd.concat([fq, fq]).to_numpy())
    b = b.sort_values(["pid", "ev", "pri"]).drop_duplicates(["pid", "ev"]).reset_index(drop=True)
    b = b[(b["nkid"] > 0) & (b["hh"] > 0) & b["ev"].between(1968, 2022)]
    if kind == "main":
        tr = b["fk"] == b["ev"]
        ct = b["fm"] > b["ev"] + 6
    elif kind == "strict":                          # first closure, no layoff before it
        tr = (b["fk"] == b["ev"]) & (b["fm"] >= b["ev"])
        ct = b["fm"] > b["ev"] + 6
    else:                                           # first quit, no main displacement in the window
        tr = (b["fk"] == b["ev"]) & (b["fm"] > b["ev"] + 6)
        ct = (b["fm"] > b["ev"] + 6) & (b["fq"] > b["ev"] + 6)
    b = b[tr | ct].assign(treat=tr[tr | ct].astype(int))
    base = b[["pid", "ev", "treat", "hrace", "youngest", "w_pid", "wh", "age"]].rename(
        columns={"w_pid": "w0", "wh": "wh0", "age": "age0", "youngest": "young0"})
    p = base.merge(m[["pid", "fam68", "year", "hh", "hlab", "wh", "w_pid", "faminc", "afdc", "fs"]], on="pid")
    p = p[(p["year"] >= p["ev"] - 3) & (p["year"] <= p["ev"] + 6)]
    p["e"] = p["year"] - p["ev"]
    same = p["w_pid"] == p["w0"]
    p["bw_present"] = same.astype(float).where(p["w0"].notna())
    p["w_hrs"] = p["wh"].where(same & p["w0"].notna())
    p["w_emp"] = (p["w_hrs"] > 0).astype(float).where(p["w_hrs"].notna())
    p["unit"] = pd.factorize(p["pid"].astype(np.int64) * 10000 + p["ev"].astype(np.int64))[0]
    p["cell"] = pd.factorize(p["year"].astype(np.int64) * 10000 + p["ev"].astype(np.int64))[0]
    return p.reset_index(drop=True)


def demean(A, groups, tol=1e-9, it=500):
    """Alternating projections: residualise the columns of A on several sets of fixed effects."""
    A = A.copy()
    for _ in range(it):
        diff = 0.0
        for g, n in groups:
            cnt = np.bincount(g, minlength=n)
            for j in range(A.shape[1]):
                mu = np.bincount(g, weights=A[:, j], minlength=n) / np.maximum(cnt, 1)
                A[:, j] -= mu[g]
                diff = max(diff, np.abs(mu).max())
        if diff < tol:
            break
    return A


def twfe(p, y, xcols, cluster="fam68"):
    """OLS of y on xcols with unit and cell FE (absorbed); cluster-robust (CR1) covariance."""
    q = p.dropna(subset=[y]).reset_index(drop=True)
    u = pd.factorize(q["unit"])[0]
    c = pd.factorize(q["cell"])[0]
    A = demean(np.column_stack([q[y].to_numpy(float), q[xcols].to_numpy(float)]),
               [(u, u.max() + 1), (c, c.max() + 1)])
    Y, X = A[:, 0], A[:, 1:]
    XtX = np.linalg.pinv(X.T @ X)
    b = XtX @ X.T @ Y
    res = Y - X @ b
    g = pd.factorize(q[cluster])[0]
    G = g.max() + 1
    S = np.zeros((G, X.shape[1]))
    np.add.at(S, g, X * res[:, None])
    n, k = X.shape
    kfe = u.max() + 1 + c.max() + 1
    adj = G / (G - 1) * (n - 1) / max(n - k - kfe, 1)
    V = adj * XtX @ (S.T @ S) @ XtX
    return b, V, dict(n=n, units=q.loc[q["treat"] == 1, "unit"].nunique(), clusters=G,
                      controls=q.loc[q["treat"] == 0, "unit"].nunique())


def event_study(p, y):
    q = p.copy()
    xs = []
    for e in ES_E:
        c = f"d{e}"
        q[c] = ((q["e"] == e) & (q["treat"] == 1)).astype(float)
        xs.append(c)
    if y in WIFE_Y:
        q = q[q["w0"].notna()]
    b, V, info = twfe(q, y, xs)
    from scipy import stats
    out = []
    for i, e in enumerate(ES_E):
        se = np.sqrt(V[i, i])
        out.append(dict(term=f"e={e:+d}", coef=b[i], se=se, p=2 * stats.norm.sf(abs(b[i] / se))))
    w = np.array([1.0 if e in (1, 2, 3) else 0.0 for e in ES_E]) / 3
    cb, cs = w @ b, np.sqrt(w @ V @ w)
    out.append(dict(term="mean +1..+3", coef=cb, se=cs, p=2 * stats.norm.sf(abs(cb / cs))))
    pre = q[(q["treat"] == 1) & q["e"].isin([-2, -1])][y].mean()
    for o in out:
        o.update(info, pre_mean=pre)
    return out


# ---------------------------------------------------------------- zero-hours measure (as in 9.ChildExposure.py)
def zero_hours(m):
    """Male head x year with zero annual hours after positive hours in the previous observed year (<= 2 back)."""
    x = m[["pid", "year", "hh"]].dropna().sort_values(["pid", "year"])
    g = x.groupby("pid")
    ok = (x["year"] - g["year"].shift(1) <= 2) & (g["hh"].shift(1) > 0) & (x["hh"] == 0)
    return x.loc[ok, ["pid", "year"]].assign(zh=1)


# ---------------------------------------------------------------- children
def lookup(s, pid, year):
    return s.reindex(pd.MultiIndex.from_arrays([np.asarray(pid, dtype=np.int64),
                                                np.asarray(year, dtype=np.int64)])).to_numpy()


def child_frame(py, m, kx, pk, ind):
    """Children (psid_child_exposure + psid_kids) with father figures by year and their family's income."""
    k1 = kx[["pid", "birth_year", "female", "race", "fam68"]]
    k2 = pk[~pk["pid"].isin(k1["pid"])][["pid", "birth_year", "female", "race", "fam68"]]
    K = pd.concat([k1, k2], ignore_index=True).dropna(subset=["birth_year"])
    hd = m[["wave", "int", "pid"]].rename(columns={"pid": "f"})
    cr = py[py["pid"].isin(K["pid"])][["pid", "wave", "int", "faminc"]].merge(hd, on=["wave", "int"], how="left")
    cr = cr[cr["f"] != cr["pid"]]
    ff = pd.concat([cr.assign(year=cr["wave"] - 1, pri=0), cr.assign(year=cr["wave"], pri=1)]).dropna(subset=["f"])
    ff = ff.sort_values(["pid", "year", "pri"])[["pid", "year", "f", "pri"]]
    ff["f"] = ff["f"].astype(np.int64)
    inc = cr.assign(year=cr["wave"] - 1).drop_duplicates(["pid", "year"]).set_index(["pid", "year"])["faminc"]
    K["educ_self"] = K["pid"].map(ind.set_index("pid")["educ"])
    return K, ff, inc


def design(K, ff, ev, lo, hi, test=None, astar=None):
    """Children first exposed (event table ev: pid of man, year) at ages lo-hi vs never exposed at 0-17.
    test: Series child pid -> test year (CDS); events must precede it. Returns child x (treat, d, f0)."""
    x = ff.merge(ev, left_on=["f", "year"], right_on=["pid", "year"], suffixes=("", "_m"))
    x = x.merge(K[["pid", "birth_year"]], on="pid")
    x["age"] = x["year"] - x["birth_year"]
    x = x[x["age"].between(0, 17)]
    base = K[["pid", "birth_year"]].copy()
    if test is not None:
        base = test.merge(base, on="pid")
        x = x.merge(test, on="pid")
        x = x[x["year"] < x["tyear"]]
        key = ["pid", "tyear"]
    else:
        key = ["pid"]
    first = x.sort_values(key + ["year", "pri"]).drop_duplicates(key)[key + ["year", "f", "age"]]
    first = first.rename(columns={"year": "d", "f": "f0", "age": "a"})
    base = base.merge(first, on=key, how="left")
    tr = base["a"].between(lo, hi)
    if astar is None:
        astar = int(round(base.loc[tr, "a"].median()))
    ct = base["a"].isna()
    base = base[tr | ct].copy()
    base["treat"] = base["a"].notna().astype(int)
    c = base["treat"] == 0
    base.loc[c, "d"] = base.loc[c, "birth_year"] + astar
    base.loc[c, "a"] = astar
    if test is not None:
        base = base[base["d"] < base["tyear"]]
    f1 = ff.drop_duplicates(["pid", "year"]).set_index(["pid", "year"])["f"]
    base.loc[c, "f0"] = lookup(f1, base.loc[c, "pid"], base.loc[c, "d"])
    base = base.dropna(subset=["f0"])
    base["f0"] = base["f0"].astype(np.int64)
    base["d"] = base["d"].astype(np.int64)
    return base, astar


def measures(b, m, inc, H):
    """Baseline (pre) and post measures around the (pseudo) event year d."""
    mi = m.set_index(["pid", "year"])
    hh, fi, wp, wh = mi["hh"], mi["faminc"], mi["w_pid"], mi["wh"]
    f0, d = b["f0"].to_numpy(), b["d"].to_numpy()
    h1, h2 = lookup(hh, f0, d - 1), lookup(hh, f0, d - 2)
    b["ff_work"] = np.where(np.isnan(h1), h2, h1) > 0
    pre = np.column_stack([lookup(fi, f0, d - j) for j in (1, 2, 3)])
    alt = np.column_stack([lookup(inc, b["pid"], d - j) for j in (1, 2, 3)])
    pre = np.where(np.isnan(pre), alt, pre)
    with np.errstate(all="ignore"):
        pm = np.nanmean(pre, axis=1)
        b["lpre"] = np.log(np.where(pm > 0, pm, np.nan))
        w1, w2 = lookup(wp, f0, d - 1), lookup(wp, f0, d - 2)
        mom = np.where(np.isnan(w1), w2, w1)
        b["mom"] = mom
        mh0 = np.where(np.isnan(w1), lookup(wh, f0, d - 2), lookup(wh, f0, d - 1))
        b["mom_emp_pre"] = np.where(np.isnan(mom), np.nan, (mh0 > 0).astype(float))
        mp = np.where(np.isnan(mom), -1, mom)
        post_h = np.column_stack([lookup(H, mp, d + j) for j in (1, 2, 3)])
        b["dmom"] = (np.nanmean(post_h, axis=1) - mh0) / 1000
        post = np.column_stack([lookup(inc, b["pid"], d + j) for j in (1, 2, 3)])
        qm = np.nanmean(post, axis=1)
        b["lpost"] = np.log(np.where(qm > 0, qm, np.nan))
    return b[b["ff_work"]]


# ---------------------------------------------------------------- child regressions
def ecat(e):
    return pd.cut(e, [0, 11, 12, 15, 17], labels=["lt12", "12", "13_15", "16p"]).astype(str).replace("nan", "miss")


def design_matrix(df, xs, ctrl, fe):
    Z = df[xs + ctrl].astype(float)
    for f in fe:
        Z = Z.join(pd.get_dummies(df[f].astype(int), prefix=f, drop_first=True, dtype=float))
    Z = Z.join(pd.get_dummies(df["pe"], prefix="pe", dtype=float).drop(columns="pe_12", errors="ignore"))
    Z.insert(0, "const", 1.0)
    return Z


def creg(df, y, xs, ctrl, fe):
    """Clustered (fam68) OLS; returns {var: (b, se, p)}, n, clusters, children."""
    import statsmodels.api as sm
    cols = [y, *xs, *ctrl, *fe, "fam68", "pe", "pid"]
    q = df[cols].replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)
    Z = design_matrix(q, xs, ctrl, fe)
    Z = Z.loc[:, Z.std() > 0].assign(const=1.0)
    r = sm.OLS(q[y].astype(float), Z).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(q["fam68"])[0]})
    est = {v: (r.params[v], r.bse[v], r.pvalues[v]) for v in xs + ctrl if v in r.params}
    return est, dict(n=int(r.nobs), clusters=q["fam68"].nunique(), kids=q["pid"].nunique(),
                     treated=int((q[xs[0]] > 0).sum()), mean=q[y].mean())


def mediation(df, y, ctrl, fe, reps=500, seed=19):
    """Total vs direct coefficient of 'treat' with and without the mediators (mother's change in hours, log
    family income after); share mediated with a cluster (fam68) bootstrap."""
    med = ["dmom", "lpost"]
    cols = [y, "treat", *ctrl, *med, *fe, "fam68", "pe", "pid"]
    q = df[cols].replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)
    Z0 = design_matrix(q, ["treat"], ctrl, fe)
    Z0 = Z0.loc[:, (Z0.std() > 0) | (Z0.columns == "const")]
    Zs = {"total": Z0, "dmom": Z0.join(q[["dmom"]]), "lpost": Z0.join(q[["lpost"]]), "both": Z0.join(q[med])}
    Y = q[y].to_numpy(float)
    g = pd.factorize(q["fam68"])[0]
    G = g.max() + 1

    def fit(idx):
        out = {}
        for k, Z in Zs.items():
            A = Z.to_numpy(float)[idx]
            out[k] = np.linalg.lstsq(A, Y[idx], rcond=None)[0][1]
        return out
    full = fit(np.arange(len(q)))
    members = [np.flatnonzero(g == j) for j in range(G)]
    rng = np.random.default_rng(seed)
    bs = []
    for _ in range(reps):
        idx = np.concatenate([members[j] for j in rng.integers(0, G, G)])
        bs.append(fit(idx))
    bs = pd.DataFrame(bs)
    res = {}
    for k in ("total", "dmom", "lpost", "both"):
        res[f"b_{k}"] = (full[k], bs[k].std())
    for k in ("dmom", "lpost", "both"):
        sh = (full["total"] - full[k]) / full["total"]
        shb = (bs["total"] - bs[k]) / bs["total"]
        res[f"share_{k}"] = (sh, shb.std())
        dif = full["total"] - full[k]
        res[f"diff_{k}"] = (dif, (bs["total"] - bs[k]).std())
    return res, dict(n=len(q), clusters=G, treated=int(q["treat"].sum()))


# ---------------------------------------------------------------- output helpers
ROWS = []


def cell(b, se, p):
    pv = "<0.001" if p < 0.001 else f"{p:.3f}"
    return f"{b:.3f}{stars(p)} ({se:.3f}; p={pv})"


def big(b, se, p):
    pv = "<0.001" if p < 0.001 else f"{p:.3f}"
    return f"{b:,.0f}{stars(p)} ({se:,.0f}; p={pv})"


def pval(b, se):
    from scipy import stats
    return 2 * stats.norm.sf(abs(b / se)) if se > 0 else np.nan


def md_table(header, panels, foot=()):
    """panels: list of (panel title, [(row label, [cells])]). One column per regression."""
    out = ["| | " + " | ".join(header) + " |", "|" + "---|" * (len(header) + 1)]
    for title, rows in panels:
        if title:
            out.append(f"| **{title}** |" + " |" * len(header))
        for lab, cells in rows:
            out.append(f"| {lab} | " + " | ".join(cells) + " |")
    for lab, cells in foot:
        out.append(f"| {lab} | " + " | ".join(cells) + " |")
    return "\n".join(out)


def es_figure(res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    col = {"Black": "#2a78d6", "White": "#eb6834"}
    mk = {"Black": "o", "White": "s"}
    fig, axes = plt.subplots(2, 4, figsize=(15, 7.2))
    for ax, (y, lab) in zip(axes.flat, ES_Y):
        for k, race in enumerate(("Black", "White")):
            o = [r for r in res[("main", race)][y] if r["term"].startswith("e=")]
            z = sorted([(int(r["term"][2:]), r["coef"], r["se"]) for r in o] + [(-2, 0.0, 0.0)])
            e, b, s = (np.array(v) for v in zip(*z))
            sh = (k - 0.5) * 0.18
            ax.fill_between(e + sh, b - 1.96 * s, b + 1.96 * s, color=col[race], alpha=0.12, linewidth=0)
            ax.plot(e + sh, b, color=col[race], marker=mk[race], markersize=4.5, linewidth=1.8, label=race)
        ax.axhline(0, color="#52514e", linewidth=0.8)
        ax.axvline(-0.5, color="#b0afa8", linewidth=0.8, linestyle=":")
        ax.set_title(lab, fontsize=11, color="#0b0b0b")
        ax.set_xticks(range(-3, 7))
        ax.tick_params(labelsize=8, colors="#52514e")
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        ax.grid(axis="y", color="#e6e5e0", linewidth=0.6)
    axes[0, 0].legend(frameon=False, fontsize=9)
    fig.supxlabel("Years since the father's displacement (plant closing or layoff; reference = -2)", fontsize=10)
    fig.suptitle("Fathers' displacement: family outcomes by race (stacked event study, 95% CI)", fontsize=12)
    fig.tight_layout()
    fig.savefig(OUT / "father_displacement_es.png", dpi=150, facecolor="#fcfcfb")
    plt.close(fig)


LABY = {"log_earn": "Log lifetime earnings", "log_fam": "Log lifetime family income",
        "rank_earn": "Earnings rank (0-100)", "rank_fam": "Family income rank (0-100)",
        "educ_self": "Years of schooling", "lw": "WJ Letter-Word", "ap": "WJ Applied Problems",
        "pc": "WJ Passage Comp.", "bpi_z": "BPI (z, higher = worse)"}
LABX = {"treat": "Father figure displaced", "lpre": "Log pre-event family income (mean of 3 yrs before)",
        "female": "Female", "black": "Black", "mom_emp_pre": "Mother figure employed year before",
        "d_x_momemp": "Displaced x mother employed year before", "dmom": "Change in mother's hours (1000s)",
        "d_x_dmom": "Displaced x change in mother's hours"}
AY = ["log_earn", "log_fam", "rank_earn", "rank_fam", "educ_self"]
CY = ["lw", "ap", "pc", "bpi_z"]
CTRL = ["lpre", "female"]


def run_panel(b, ys, race, xs, cdsmode=False, tag=""):
    q = b if race == "Pooled" else b[b["race"] == race]
    ctrl = CTRL + (["black"] if race == "Pooled" else [])
    fe = ["birth_year"] + (["tyear"] if cdsmode else [])
    out = {}
    for y in ys:
        try:
            est, info = creg(q, y, xs, ctrl, fe)
        except Exception as exc:                            # too few observations
            print("skip", tag, race, y, exc)
            continue
        out[y] = (est, info)
        for v, (bb, se, p) in est.items():
            ROWS.append(dict(table=tag, sample=race, outcome=y, term=v, coef=bb, se=se, p=p, n=info["n"],
                             treated=info["treated"], clusters=info["clusters"]))
    return out


def panel_rows(out, ys, show):
    rows = []
    for v in show:
        rows.append((LABX.get(v, v), [cell(*out[y][0][v]) if y in out and v in out[y][0] else "" for y in ys]))
    rows.append(("Mean of outcome", [f"{out[y][1]['mean']:.3f}" if y in out else "" for y in ys]))
    rows.append(("N / displaced", [f"{out[y][1]['n']:,} / {out[y][1]['treated']:,}" if y in out else ""
                                   for y in ys]))
    rows.append(("Clusters (fam68)", [f"{out[y][1]['clusters']:,}" if y in out else "" for y in ys]))
    return rows


# ---------------------------------------------------------------- main
def main():
    OUT.mkdir(exist_ok=True)
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    fam = psid9.family()
    d, rep = displacement(py, fam)
    m = men_panel(py, fam)
    zh = zero_hours(m)
    disp = d.merge(zh, on=["pid", "year"], how="outer")
    for k in ("main", "strict", "layoff", "quit", "zh"):
        disp[k] = disp[k].fillna(0).astype(int)
    disp.to_pickle(DATA / "psid_displacement.pkl")
    md = ["# Fathers' displacement in the PSID: the family's response and children's outcomes", "",
          "Built by `19.FatherDisplacement.py` (2026-10-17); variable list per wave in its docstring. Unweighted "
          "PSID SRC + SEO, Black and White (head's race). S.e. clustered by 1968 family (fam68); *** p<0.01, "
          "** p<0.05, * p<0.1. **Displacement (main)** = the head reports that his job ended because the company "
          "folded / moved / went out of business (closure) or he was laid off / fired; closures only = strict; "
          "quits = placebo. The event study compares displaced fathers with not-yet-displaced and never-displaced "
          "fathers; the child regressions are selection-on-observables comparisons. Neither identifies a causal "
          "effect without the usual assumptions (no selection into layoffs on trends or on unobserved family "
          "traits); the mediation section is descriptive.", ""]

    # ---- 1. coverage
    x = m[["pid", "year", "hh", "hrace", "age"]].merge(disp[["pid", "year", "main", "strict", "layoff", "quit", "zh"]],
                                                     on=["pid", "year"], how="left")
    for k in ("main", "strict", "layoff", "quit", "zh"):
        x[k] = x[k].fillna(0)
    x["hprev"] = x.groupby("pid")["hh"].shift(1)
    x["yprev"] = x.groupby("pid")["year"].shift(1)
    s = x[(x["hprev"] > 0) & (x["year"] - x["yprev"] <= 2) & x["age"].between(20, 60)].copy()
    s["period"] = pd.cut(s["year"], [1966, 1979, 1989, 1999, 2009, 2022],
                         labels=["1967-79", "1980-89", "1990-99", "2000-09", "2010-22"])
    K5 = ("main", "strict", "layoff", "quit", "zh")
    rows = []
    for (per, race), g in s.groupby(["period", "hrace"], observed=True):
        rows.append((f"{per}, {race}", [f"{g[k].mean():.4f}" for k in K5] + [f"{len(g):,}"]))
    for race, g in s.groupby("hrace"):
        rows.append((f"All years, {race}", [f"{g[k].mean():.4f}" for k in K5] + [f"{len(g):,}"]))
    md += ["## 1. The displacement measure", "",
           "Annual rate: share of male heads aged 20-60 with positive hours in the previous observed year who "
           "report a job end of each kind dated to that (observed) calendar year.", "",
           md_table(["Main (closure or layoff)", "Closure", "Layoff / fired", "Quit", "Zero hours", "Head-years"],
                    [("", rows)]), ""]
    ev = disp[disp["main"] == 1][["pid", "year"]].merge(m[["pid", "year", "hh"]], on=["pid", "year"], how="left")
    nxt = m.assign(year=m["year"] - 1)[["pid", "year", "hh"]].rename(columns={"hh": "hh_next"})
    ev = ev.merge(nxt, on=["pid", "year"], how="left")
    zz = disp[disp["zh"] == 1]
    mm = disp[disp["main"] == 1]
    near = {(p, y + dd) for p, y in zip(mm["pid"], mm["year"]) for dd in (-1, 0, 1)}
    zz_main = np.mean([(p, y) in near for p, y in zip(zz["pid"], zz["year"])])
    nzh = {(p, y - dd) for p, y in zip(zz["pid"], zz["year"]) for dd in (-1, 0, 1, 2)}
    main_zz = np.mean([(p, y) in nzh for p, y in zip(ev["pid"], ev["year"])])
    br = rep.merge(py[py["head"] & (py["female"] == 0)][["wave", "int"]].drop_duplicates(), on=["wave", "int"])
    brs = br[br["main"]].groupby("branch").size()
    COV = dict(n_main=int(disp["main"].sum()), n_strict=int(disp["strict"].sum()),
               n_layoff=int(disp["layoff"].sum()), n_quit=int(disp["quit"].sum()),
               dated=br.loc[br["main"], "dated"].mean(), zero_same=(ev["hh"] == 0).mean(),
               zero_next=(ev["hh_next"] == 0).mean(), main_zz=main_zz, zz_main=zz_main)
    md += [f"Main displacements (male heads, all years): {COV['n_main']:,} man-years ({COV['n_strict']:,} "
           f"closures, {COV['n_layoff']:,} layoffs/firings; quits {COV['n_quit']:,}). Main reports by branch: "
           + ", ".join(f"{k} {v:,}" for k, v in brs.items()) + f". Share dated by a reported end year: "
           f"{COV['dated']:.3f}. The head's annual hours are zero in the displacement year for "
           f"{COV['zero_same']:.3f} and in the next year for {COV['zero_next']:.3f} of main displacements; "
           f"{COV['main_zz']:.3f} of main displacements have a zero-hours year within -1..+2 years, and "
           f"{COV['zz_main']:.3f} of zero-hours events have a main displacement within +-1 year. Coverage gaps: "
           "calendar 1997 and 1999 after the spring interview are reached only through the U-branch end years of "
           "the 1999 / 2001 waves (no 1998 / 2000 interview), so displacements then are undercounted; 1968-1983 "
           "E-branch reports have no end year and are dated to the year before the interview.", ""]
    print(COV, flush=True)

    # ---- 2. family event study
    res = {}
    specs = [("main", r, None) for r in ("All", "Black", "White")]
    for race in ("All", "Black", "White"):
        specs += [("main", race, s_) for s_ in ("young05", "young617", "wemp", "wnot")]
    specs += [(k, r, None) for k in ("strict", "quit") for r in ("All", "Black", "White")]
    P = {k: stacks(m, d, k) for k in ("main", "strict", "quit")}
    for kind, race, sub in specs:
        p = P[kind]
        if race != "All":
            p = p[p["hrace"] == race]
        if sub == "young05":
            p = p[p["young0"] <= 5]
        elif sub == "young617":
            p = p[p["young0"] >= 6]
        elif sub == "wemp":
            p = p[p["w0"].notna() & (p["wh0"] > 0)]
        elif sub == "wnot":
            p = p[p["w0"].notna() & (p["wh0"] == 0)]
        key = (kind, race) if sub is None else (kind, race, sub)
        res[key] = {}
        for y, lab in ES_Y:
            o = event_study(p, y)
            res[key][y] = o
            for r in o:
                ROWS.append(dict(table="family_event_study", design=kind, sample=race, subsample=sub or "",
                                 outcome=y, term=r["term"], coef=r["coef"], se=r["se"], p=r["p"], n=r["n"],
                                 treated=r["units"], controls=r["controls"], clusters=r["clusters"],
                                 pre_mean_treated=r["pre_mean"]))
        print("event study", key, flush=True)
    es_figure(res)

    def fmt_es(y, r):
        return (big if y in ("hh", "hlab", "w_hrs", "faminc") else cell)(r["coef"], r["se"], r["p"])

    def es_panels(keys, terms):
        panels = []
        for key, title in keys:
            rows = [(t, [fmt_es(y, next(r for r in res[key][y] if r["term"] == t)) for y, _ in ES_Y]) for t in terms]
            o0 = {y: res[key][y][0] for y, _ in ES_Y}
            rows.append(("Treated mean at e = -2, -1", [f"{o0[y]['pre_mean']:,.3f}" if o0[y]["pre_mean"] < 10 else
                                                        f"{o0[y]['pre_mean']:,.0f}" for y, _ in ES_Y]))
            rows.append(("N (man-years, stacked)", [f"{o0[y]['n']:,}" for y, _ in ES_Y]))
            rows.append(("Displaced fathers / control father-stacks",
                         [f"{o0[y]['units']:,} / {o0[y]['controls']:,}" for y, _ in ES_Y]))
            rows.append(("Clusters (fam68)", [f"{o0[y]['clusters']:,}" for y, _ in ES_Y]))
            panels.append((title, rows))
        return panels
    hdr = [lab for _, lab in ES_Y]
    allterms = [f"e={e:+d}" for e in ES_E] + ["mean +1..+3"]
    short = ["e=-1", "e=+1", "e=+2", "e=+3", "mean +1..+3"]
    foot = [("Fixed effects", ["father x stack, calendar year x stack"] * len(ES_Y))]
    keys = []
    for race in ("All", "Black", "White"):
        keys += [(("main", race, "young05"), f"{race}: youngest child 0-5"),
                 (("main", race, "young617"), f"{race}: youngest child 6-17"),
                 (("main", race, "wemp"), f"{race}: wife employed at baseline"),
                 (("main", race, "wnot"), f"{race}: wife present, not employed at baseline")]
    md += ["## 2. Family event study", "",
           "Stacked event study (Cengiz et al. 2019): for each calendar year, fathers first displaced that year "
           "(main definition) vs clean controls (no displacement up to the event year + 6); all are male heads "
           "with a child 0-17 in the family unit and positive hours at baseline (the latest of event year -2, -1). "
           "Outcomes refer to calendar years (PSID income year = interview year - 1), event time -3..+6, "
           "reference e = -2; regressors = displaced x event-time dummies, with father x stack and calendar year x "
           "stack fixed effects. Hours and income (2000 dollars) in levels; wife's outcomes for the wife present "
           "at baseline while she is still in the family unit; 'Still with baseline wife' = 1 while she is his "
           "wife (its fall = separation, divorce or her death). AFDC/TANF = head or wife received; food stamps = "
           "family received (last year). After 1996 outcomes are observed every other year. A pre-displacement "
           "dip at e = -1 in the head's earnings is the usual Jacobson-LaLonde-Sullivan pattern (and partly "
           "dating error: undated reports are put in the year before the interview).", "",
           "### 2a. Pooled and by race", "",
           md_table(hdr, es_panels([(("main", "All"), "All fathers"), (("main", "Black"), "Black fathers"),
                                    (("main", "White"), "White fathers")], allterms), foot), "",
           "![event study](father_displacement_es.png)", "",
           "### 2b. By the youngest child's age and the wife's work at baseline", "",
           md_table(hdr, es_panels(keys, short), foot), "",
           "### 2c. Closures only (Page-Stevens-Lindo's strict definition) and quits (placebo)", "",
           md_table(hdr, es_panels([((k, r), f"{'Closures' if k == 'strict' else 'Quits'}: {r}")
                                    for k in ("strict", "quit") for r in ("All", "Black", "White")], short), foot),
           ""]

    # ---- 3. children
    kx = pd.read_pickle(DATA / "psid_child_exposure.pkl")
    pk = pd.read_pickle(DATA / "psid_kids.pkl")
    cds = pd.read_pickle(DATA / "cds_scores.pkl")
    ind = psid9.individual()[0]
    K, ff, inc = child_frame(py, m, kx, pk, ind)
    hw = py[(py["head"] & (py["female"] == 1)) | py["wife"]][["pid", "wave", "int", "head"]]
    hw = hw.merge(fam[["wave", "int", "hh", "wh"]], on=["wave", "int"], how="left")
    hw["hrs"] = np.where(hw["head"], hw["hh"], hw["wh"])
    H = hw.assign(year=hw["wave"] - 1).dropna(subset=["hrs"]).drop_duplicates(["pid", "year"]).set_index(
        ["pid", "year"])["hrs"]
    educ = ind.set_index("pid")["educ"]
    events = {k: disp.loc[disp[k] == 1, ["pid", "year"]] for k in ("main", "strict", "quit", "zh")}
    adult = pk[["pid", "log_earn", "log_fam"]].merge(K[["pid", "birth_year"]], on="pid")
    coh = adult["birth_year"] // 5
    for v, r in (("log_earn", "rank_earn"), ("log_fam", "rank_fam")):
        adult[r] = adult.groupby(coh)[v].rank(pct=True) * 100
    adult = adult.drop(columns="birth_year")
    test = cds[cds["age"].between(3, 17)][["pid", "wave"]].rename(columns={"wave": "tyear"}).drop_duplicates()

    def build(kind, lo, hi, cdsmode=False):
        tst = test if cdsmode else None
        b, a = design(K, ff, events[kind], lo, hi, test=tst)
        if kind in ("strict", "quit"):                      # controls and treated clean of main displacement
            bm, _ = design(K, ff, events["main"], 0, 17, test=tst)
            b = b[~b["pid"].isin(set(bm.loc[bm["treat"] == 1, "pid"]))] if kind == "quit" else \
                b[~(b["pid"].isin(set(bm.loc[bm["treat"] == 1, "pid"])) & (b["treat"] == 0))]
        b = measures(b, m, inc, H)
        b = b.merge(K[["pid", "female", "race", "fam68", "educ_self"]], on="pid", how="left")
        pe = np.fmax(educ.reindex(b["f0"]).to_numpy(), educ.reindex(b["mom"].fillna(-1)).to_numpy())
        b["pe"] = ecat(pd.Series(pe)).to_numpy()
        b["black"] = (b["race"] == "Black").astype(float)
        b["female"] = b["female"].astype(float)
        if cdsmode:
            b = b.merge(cds[["pid", "wave", "lw", "ap", "pc", "bpi_z"]].rename(columns={"wave": "tyear"}),
                        on=["pid", "tyear"])
        else:
            b = b.merge(adult, on="pid", how="left")
            b["educ_self"] = b["educ_self"].where(b["birth_year"] <= 1995)
        b = b[b["race"].isin(["Black", "White"])].copy()
        b["d_x_momemp"] = b["treat"] * b["mom_emp_pre"]
        b["d_x_dmom"] = b["treat"] * b["dmom"]
        return b, a

    md += ["## 3. Children's outcomes", "",
           "Children of `psid_child_exposure.pkl` and `psid_kids.pkl`. Father figure = male head of the child's "
           "family unit at the interview in or just after the year (biological father, stepfather or partner). "
           "Treated = the father figure's first main displacement falls in the age band; controls = children never "
           "exposed at 0-17 (CDS: before the test), given a pseudo event year at the treated's median exposure "
           "age. Both need a father figure who worked in the year(s) before the (pseudo) event. Children first "
           "exposed in another band are dropped. Controls: log family income of the father figure's family unit "
           "averaged over the 3 years before the (pseudo) event (the child's own unit if missing), parental "
           "education (max of father and mother figure: <12, 12, 13-15, 16+, missing), female, birth-year FE "
           "(+ CDS-wave FE; + Black in pooled rows). Adult outcomes from `psid_kids.pkl` (mean over years as "
           "head/wife at 25-55, zeros kept, 3+ years); ranks = percentile within 5-year birth cohorts of that "
           "sample; schooling = highest completed grade (born <= 1995). CDS = WJ standard scores and BPI z, "
           "assessments at 3-17.", ""]
    store = {}
    for cdsmode, ys, title, bl in ((True, CY, "3a. CDS test scores and behaviour (displacement before the test)",
                                    [(0, 5, "ages 0-5"), (6, 17, "ages 6-17")]),
                                   (False, AY, "3b. Adult outcomes",
                                    [(0, 5, "ages 0-5"), (6, 11, "ages 6-11"), (12, 17, "ages 12-17")])):
        panels = []
        for lo, hi, blab in bl:
            b, a = build("main", lo, hi, cdsmode)
            for race in ("Black", "White", "Pooled"):
                out = run_panel(b, ys, race, ["treat"], cdsmode=cdsmode,
                                tag=f"child_{'cds' if cdsmode else 'adult'}_{blab}")
                panels.append((f"{race}, displaced at {blab} (controls' pseudo age {a})",
                               panel_rows(out, ys, ["treat", "lpre", "female"])))
            print("children", cdsmode, blab, flush=True)
        md += [f"### {title}", "", md_table([LABY[y] for y in ys], panels,
                                            [("Fixed effects", ["birth year" + (", CDS wave" if cdsmode else "")]
                                              * len(ys)), ("Other controls", ["parental education"] * len(ys))]), ""]

    # ---- 4. definitions
    md += ["## 4. Displacement definitions: Page-Stevens-Lindo check and the zero-hours measure", "",
           "Exposure at any age 0-17 (CDS: before the test). Main = closures + layoffs/firings; closures only: "
           "controls exclude children exposed to a main displacement; quits: treated and controls exclude them; "
           "zero hours = the 9.ChildExposure.py-style measure rebuilt on the same father figures (controls: no "
           "zero-hours year at 0-17). PSL (2009) find about -9% for adult earnings with layoffs included and about "
           "zero with closures only.", ""]
    for cdsmode, ys in ((False, AY), (True, CY)):
        panels = []
        for kind, klab in (("main", "Main (closure or layoff)"), ("strict", "Closures only"), ("quit", "Quits"),
                           ("zh", "Zero hours")):
            b, a = build(kind, 0, 17, cdsmode)
            if kind == "main":
                store[cdsmode] = b
            for race in ("Black", "White", "Pooled"):
                out = run_panel(b, ys, race, ["treat"], cdsmode=cdsmode,
                                tag=f"definitions_{'cds' if cdsmode else 'adult'}_{kind}")
                panels.append((f"{klab}: {race}", panel_rows(out, ys, ["treat"])))
        md += [f"### 4{'b. CDS' if cdsmode else 'a. Adult outcomes'}", "",
               md_table([LABY[y] for y in ys], panels,
                        [("Controls", ["log pre-event income, parental education, female, birth-year FE"
                                       + (", CDS-wave FE" if cdsmode else "")] * len(ys))]), ""]
        print("definitions", cdsmode, flush=True)

    # ---- 5. interactions
    md += ["## 5. Does the association differ with the mother's work? (exposure at 0-17, main definition)", "",
           "Mother figure = the father figure's wife/partner at baseline (children without one drop out of these "
           "rows). 'Employed year before' = her hours > 0 in the year before the (pseudo) event; change in hours "
           "= her mean annual hours over event years +1..+3 minus the baseline year, in 1000s (for controls at "
           "the pseudo event year). The change in hours is itself an outcome of the displacement, so its "
           "interaction is descriptive.", ""]
    for cdsmode, ys in ((False, AY), (True, CY)):
        b = store[cdsmode]
        panels = []
        for race in ("Black", "White", "Pooled"):
            out = run_panel(b, ys, race, ["treat", "d_x_momemp", "mom_emp_pre"], cdsmode=cdsmode,
                            tag=f"interact_momemp_{'cds' if cdsmode else 'adult'}")
            panels.append((f"{race}: x mother employed before",
                           panel_rows(out, ys, ["treat", "d_x_momemp", "mom_emp_pre"])))
            out = run_panel(b, ys, race, ["treat", "d_x_dmom", "dmom"], cdsmode=cdsmode,
                            tag=f"interact_dmom_{'cds' if cdsmode else 'adult'}")
            panels.append((f"{race}: x change in mother's hours", panel_rows(out, ys, ["treat", "d_x_dmom", "dmom"])))
        md += [f"### 5{'b. CDS' if cdsmode else 'a. Adult outcomes'}", "",
               md_table([LABY[y] for y in ys], panels,
                        [("Controls", ["log pre-event income, parental education, female, birth-year FE"
                                       + (", CDS-wave FE" if cdsmode else "")] * len(ys))]), ""]

    # ---- 6. mediation
    md += ["## 6. Mediation (descriptive)", "",
           "Exposure at 0-17, main definition; the same sample in every row of a column (non-missing mediators). "
           "Total = coefficient on 'displaced' without mediators; then adding the mother figure's change in hours "
           "(+1..+3 vs baseline, 1000s), the log of the child's family income over +1..+3, and both. Share "
           "mediated = (total - direct) / total. S.e. from 500 bootstrap replications resampling 1968 families; "
           "p-values from the bootstrap s.e. (normal). The mediators are post-displacement outcomes chosen by the "
           "family, so the shares decompose an association; they are not causal mediation effects and are "
           "unstable when the total is near zero.", ""]
    med_y = [(False, "log_earn"), (False, "log_fam"), (False, "rank_earn"), (False, "educ_self"), (True, "ap"),
             (True, "lw")]
    panels = []
    for race in ("Black", "White", "Pooled"):
        cols = []
        for cdsmode, y in med_y:
            b = store[cdsmode]
            q = b if race == "Pooled" else b[b["race"] == race]
            r, info = mediation(q, y, CTRL + (["black"] if race == "Pooled" else []),
                                ["birth_year"] + (["tyear"] if cdsmode else []))
            cols.append((r, info))
            for k, (v, se) in r.items():
                ROWS.append(dict(table="mediation", sample=race, outcome=y, term=k, coef=v, se=se,
                                 p=pval(v, se), n=info["n"], treated=info["treated"], clusters=info["clusters"]))
        rows = [(lab, [cell(r[k][0], r[k][1], pval(*r[k])) for r, _ in cols]) for k, lab in (
            ("b_total", "Displaced: total"), ("b_dmom", "Displaced, given mother's change in hours"),
            ("b_lpost", "Displaced, given log family income after"), ("b_both", "Displaced, given both"),
            ("share_dmom", "Share mediated: mother's hours"), ("share_lpost", "Share mediated: family income"),
            ("share_both", "Share mediated: both"), ("diff_both", "Total - direct (both)"))]
        rows.append(("N / displaced", [f"{i['n']:,} / {i['treated']:,}" for _, i in cols]))
        rows.append(("Clusters (fam68)", [f"{i['clusters']:,}" for _, i in cols]))
        panels.append((race, rows))
        print("mediation", race, flush=True)
    md += [md_table([f"{LABY[y]}{' (CDS)' if c else ''}" for c, y in med_y], panels,
                    [("Controls", ["log pre-event income, parental education, female, birth-year FE (CDS: + wave)"]
                      * len(med_y))]), ""]

    # ---- 7. sample sizes
    rows = []
    for race in ("Black", "White"):
        o = res[("main", race)]["hh"][0]
        rows.append((f"Family event study, {race}", [f"{o['units']:,}", f"{o['controls']:,}", f"{o['n']:,}"]))
    for cdsmode, lab in ((False, "Children in adult-outcome design (0-17)"), (True, "CDS child-waves in design (0-17)")):
        for race in ("Black", "White"):
            q = store[cdsmode][store[cdsmode]["race"] == race]
            rows.append((f"{lab}, {race}", [f"{int(q['treat'].sum()):,}", f"{int((q['treat'] == 0).sum()):,}",
                                            f"{len(q):,}"]))
    md += ["## 7. Sample sizes", "", md_table(["Displaced", "Controls", "Rows"], [("", rows)]), ""]

    pd.DataFrame(ROWS).to_csv(OUT / "father_displacement.csv", index=False)
    (OUT / "father_displacement.md").write_text("\n".join(md), encoding="utf-8")
    print("done")


if __name__ == "__main__":
    main()
