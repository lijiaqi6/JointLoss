r"""The separated wife's state in the PSID: child support, remarriage, work and program receipt (2026-10-20).

WP3 of IGE/proposals/fable_10h_plan_paperA.md. The model's separated state V^S has no child support and no remarriage
and is the terminal state of 67% of Black and 41% of White entry couples; the marriage note's Diagnostic B
(IGE/proposals/fable_marriage_divorce_paperA.md, Section 5) asks for two calibrated inputs with zero parameters:
monthly child support by race x child count, and an annual remarriage hazard by race (treated as the end of the
record). This script supplies both, and the separated mothers' employment, hours and AFDC/TANF / food stamp receipt
as untargeted validation rows. Nothing in IGE/paperA_model, IGE/60-62 or IGE/66 is touched.

Reads (read only): IGE/data/psid_person_year.pkl (1.PSID.py), psid_displacement.pkl (19), the raw PSID family files
(Dropbox/PSID/Family, child-support items below; hours / AFDC / food stamps through 9.ChildExposure.family()), the
marriage history Dropbox/PSID/Others/mh85_23. Caches (person level, git-ignored IGE/data/): sepmoth_cs_items.pkl,
sepmoth_fam9.pkl. Writes (aggregates only):
  IGE/output/separated_mothers.csv   every number (table, sample, outcome, stat, value, se, p, n, clusters)
  IGE/output/separated_mothers.md    tables

SAMPLE. Women of the SRC + SEO samples whose marriage history (MH85_23; MH4 = 2) has a marriage that ended in
separation or divorce (MH12 = 5 / 4) with separation year s = MH16 (else the divorce year MH14), s in 1984-2020;
aged 25-59 in s; observed in the PSID as the wife of that husband (head pid = MH spouse pid MH7/MH8) at an interview
in s - 3 .. s + 1 (baseline = the last such interview) with a child 0-17 in the family unit at baseline; race = the
head's race at baseline (Black / White). Event time k = income year - s (PSID income year = interview year - 1),
k = -3 .. +10, income years <= 2021. All observed years are used (no balanced panel).

STATUS at each interview: female head (single, the model's V^S), wife / cohabiting "wife" (rel 20 / 22) of a new
head (repartnered), wife of the ex-husband (reconciled), other (in another person's unit: no family-file hours).

OUTCOMES (income year wave - 1, 2000 dollars, CPI-U):
  child support received: her own item, the head's item if she is head, the wife's item if she is a wife.
     1984-1993 waves: annual amount ('HD yy CHILD SUPPORT', 'WF yy CHILD SUPPORT'; no wife item in 1984; 1993 'HD/WF
     1992 CHILD SUPPORT INCOME'); 99,999 -> missing.
     1994-2003 waves: amount x time unit x months received ('AMT CHILD SUPPORT OF HD' / 'AMT CHILD SUPPORT HD PER' /
     'CHILD SUPPORT INC H JAN-DEC'; wife 'CHILD SUPPORT OF WF(E) AMT/PER', 'CHILD SUPPORT INC W JAN-DEC'); units 1994-95:
     1 week, 2 two weeks, 3 month, 4 year, 5 other; 1996-2003: 3 week, 4 two weeks, 5 month, 6 year, 7 other (codebooks);
     annual = amount x {52, 26, 12, 1} x months / 12 (months = 12 if none flagged); 'other', DK, NA -> missing;
     amount >= 99,998 -> missing; unit 0 (inap.: none received) -> 0. Any wave: annual > $60,000 (2000 $) -> missing
     (4 head values 1995-2001, up to $624,000: miscoded units; the PSID's generated totals 2005-2023 stay below $56,000).
     2005-2023 waves: the generated annual totals 'CHILD SUPPORT RECEIVED BY HEAD / REF PERSN-yyyy' and 'BY WIFE /
     SPOUSE-yyyy' (missing data assigned by the PSID).
  employment (annual hours > 0) and annual hours: head's / wife's total annual hours of the family file (9.family).
  labor income: head's / wife's labor income (1.PSID.py, + business labor income 1994-2001).
  AFDC/TANF: head or wife received (9.family: amounts > 0 through 1993, 'whether received' from 1994).
  food stamps / SNAP: the family received last year (9.family).
  children: persons aged 0-17 in her family unit other than the head and wife.
Married-mother benchmark: wives (rel 2/20/22) of male heads aged 25-59 with a child 0-17 in the unit, income years
1984-2021, same outcomes.

REMARRIAGE. (a) Marriage history: the next marriage record (MH9 = order + 1), year married MH11; censored at the year
of the last marital-history report (MH17), capped at 2021. (b) New partner: the earlier of (a) and the first interview
after s at which she is the wife or cohabiting "wife" of a head other than the ex-husband (dated interview year - 1);
censored at her last interview year - 1 (or MH17 for marriages). Kaplan-Meier survival and the annual hazard (events /
woman-years at risk, years 0-9); the Black-White difference is a linear probability model on the woman-years at risk.

HUSBAND'S DISPLACEMENT. The ex-husband (MH spouse) had a main displacement (closure or layoff / firing; 19's main
definition) dated s - 2 .. s.

INFERENCE. Means and differences are OLS coefficients with s.e. clustered by 1968 family (CR1, statsmodels);
*** p<0.01, ** p<0.05, * p<0.1. Unweighted (SRC + SEO), separately by race, as in IGE/19 and IGE/64.
"""
import importlib.util
import os
import re
import warnings

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import statsmodels.api as sm  # noqa: E402

from common import DATA, OUT, HERE, stars, to2000  # noqa: E402

warnings.simplefilter("ignore", FutureWarning)
warnings.simplefilter("ignore", RuntimeWarning)
pd.options.mode.chained_assignment = None


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


psid1 = _load("psid1", "1.PSID.py")
psid9 = _load("psid9", "9.ChildExposure.py")
WAVES, FAM, layout, read = psid1.WAVES, psid1.FAM, psid1.layout, psid1.read
OTH = psid1.PSID / "Others"
CS_CACHE, FAM_CACHE = DATA / "sepmoth_cs_items.pkl", DATA / "sepmoth_fam9.pkl"
S_LO, S_HI, Y_HI = 1984, 2020, 2021
K_LO, K_HI = -3, 10
CS_MAX = 60000
MON = "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split()
ROWS = []


# ---------------------------------------------------------------- child-support items
def _find(labs, pat):
    rx = re.compile(pat, re.I)
    return [v for v, l in labs if rx.match(l.strip())]


def cs_wave(w):
    folder = FAM / (f"fam{w}" if w < 1994 else f"fam{w}er")
    base = next(f for f in folder.glob("*.do") if "formats" not in f.name).with_suffix("")
    pos, labs = layout(base.with_suffix(".do"))
    idv = labs[1][0]
    out = {}
    if w <= 1993:
        spec = {who: _find(labs, rf"^{tag} (19)?\d\d CHILD SUPPORT( INCOME.*)?$") for who, tag in
                (("h", "HD"), ("w", "WF"))}
        cols = [idv] + [c for v in spec.values() for c in v[:1]]
        f = read(base, cols, pos)
        res = pd.DataFrame({"wave": w, "int": f[idv]})
        for who, v in spec.items():
            res[f"cs_{who}"] = f[v[0]].where(f[v[0]].between(0, 99998)) if v else np.nan
        out = res
    elif w <= 2003:
        unit_map = ({1: 52, 2: 26, 3: 12, 4: 1} if w <= 1995 else {3: 52, 4: 26, 5: 12, 6: 1})
        spec = {"h": (_find(labs, r"^AMT CHILD SUPPORT OF HD$"), _find(labs, r"^AMT CHILD SUPPORT HD PER$"),
                      [_find(labs, rf"^CHILD SUPPORT INC H {m}$") for m in MON]),
                "w": (_find(labs, r"^CHILD SUPPORT OF WFE? AMT$"), _find(labs, r"^CHILD SUPPORT OF WFE? PER$"),
                      [_find(labs, rf"^CH?ILD SUPPORT INC W {m}$") for m in MON])}
        cols = [idv]
        for amt, per, mons in spec.values():
            assert len(amt) == 1 and len(per) == 1 and all(len(m) == 1 for m in mons), (w, amt, per)
            cols += [amt[0], per[0]] + [m[0] for m in mons]
        f = read(base, cols, pos)
        res = pd.DataFrame({"wave": w, "int": f[idv]})
        for who, (amt, per, mons) in spec.items():
            a = pd.to_numeric(f[amt[0]], errors="coerce")
            u = pd.to_numeric(f[per[0]], errors="coerce")
            nm = (f[[m[0] for m in mons]] == 1).sum(axis=1)
            nm = nm.where(nm > 0, 12)
            mult = u.map(unit_map)
            ann = a * mult * np.where(u.isin([k for k, v in unit_map.items() if v != 1]), nm / 12, 1.0)
            ann = ann.where(a.between(0, 99997.99))
            ann = ann.where(u != 0, 0.0)
            res[f"cs_{who}"] = ann
        out = res
    else:
        h = _find(labs, r"^CHILD SUPPORT RECEIVED BY (HEAD|REF PERSN)-\d{4}$")
        wv = _find(labs, r"^CHILD SUPPORT RECEIVED BY (WIFE|SPOUSE)-\d{4}$")
        assert len(h) == 1 and len(wv) == 1, (w, h, wv)
        f = read(base, [idv, h[0], wv[0]], pos)
        out = pd.DataFrame({"wave": w, "int": f[idv], "cs_h": f[h[0]].where(f[h[0]].between(0, 999999)),
                            "cs_w": f[wv[0]].where(f[wv[0]].between(0, 999999))})
    for c in ("cs_h", "cs_w"):
        out[c] = to2000(out[c].astype(float), w - 1)
    return out


def cs_items():
    if CS_CACHE.exists():
        return trim_cs(pd.read_pickle(CS_CACHE))
    parts = []
    for w in [w for w in WAVES if w >= 1984]:
        parts.append(cs_wave(w))
        print(f"  child support {w}: head > 0 {np.nanmean(parts[-1]['cs_h'] > 0):.3f}", flush=True)
    cs = pd.concat(parts, ignore_index=True)
    cs.to_pickle(CS_CACHE)
    return trim_cs(cs)


def trim_cs(cs):
    """Annual amounts above CS_MAX (2000 $) -> missing: the 1994-2003 amount x time-unit items have a handful of
    implausible values (up to $624,000, unit miscoded); the PSID's own generated totals 2005-2023 never exceed
    $56,000."""
    for c in ("cs_h", "cs_w"):
        cs[c] = cs[c].where(~(cs[c] > CS_MAX))
    return cs


def fam9():
    if FAM_CACHE.exists():
        return pd.read_pickle(FAM_CACHE)
    f = psid9.family()
    f.to_pickle(FAM_CACHE)
    return f


# ---------------------------------------------------------------- marriage history
def marriages():
    pos, _ = layout(OTH / "mh85_23" / "MH85_23.do")
    cols = ["MH2", "MH3", "MH4", "MH7", "MH8", "MH9", "MH11", "MH12", "MH14", "MH16", "MH17"]
    m = read(OTH / "mh85_23" / "MH85_23", cols, pos)
    m = m[(m.MH2 <= 2930) | m.MH2.between(5001, 6872)]
    m["pid"] = m.MH2 * 1000 + m.MH3
    m["sp"] = np.where(m.MH7 > 0, m.MH7 * 1000 + m.MH8, np.nan)
    m["ymar"] = m.MH11.where(m.MH11.between(1915, 2023))
    m["ylast"] = m.MH17.where(m.MH17.between(1915, 2023))
    return m


# ---------------------------------------------------------------- regressions
def reg(df, y, xs=(), fe=(), absorb=None, cluster="fam68"):
    """OLS of y on xs (+ FE dummies; absorb = one FE swept by demeaning); CR1 by cluster.
    Returns {term: (b, se, p)}, n, clusters. With xs empty: the mean of y (const)."""
    cols = [y, *xs, *fe, cluster] + ([absorb] if absorb else [])
    d = df[cols].replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)
    if len(d) < 10:
        return None
    X = d[list(xs)].astype(float)
    for f in fe:
        X = X.join(pd.get_dummies(d[f], prefix=f, drop_first=True, dtype=float))
    Y = d[y].astype(float)
    if absorb:
        g = d[absorb]
        Y = Y - Y.groupby(g).transform("mean")
        X = X - X.groupby(g).transform("mean")
        X = X.loc[:, X.std() > 1e-12]
    else:
        X = sm.add_constant(X, has_constant="add")
    r = sm.OLS(Y, X).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d[cluster])[0]})
    terms = list(xs) if xs else ["const"]
    est = {t: (r.params[t], r.bse[t], r.pvalues[t]) for t in terms if t in r.params}
    return est, int(r.nobs), int(d[cluster].nunique())


def cell(b, se, p, d=3):
    if not np.isfinite(se):
        return "n.a."
    pv = "<0.001" if p < 0.001 else f"{p:.3f}"
    return f"{b:,.{d}f}{stars(p)} ({se:,.{d}f}; p={pv})"


def rec(table, sample, outcome, stat, b, se=np.nan, p=np.nan, n=np.nan, clusters=np.nan, **kw):
    ROWS.append(dict(table=table, sample=sample, outcome=outcome, stat=stat, value=b, se=se, p=p, n=n,
                     clusters=clusters, **kw))


def mean_cell(df, y, table, sample, stat, d=3, **kw):
    o = reg(df, y)
    if o is None:
        return "n.a."
    (b, se, p), n, g = o[0]["const"], o[1], o[2]
    rec(table, sample, y, stat, b, se, p, n, g, **kw)
    return f"{b:,.{d}f} ({se:,.{d}f})"


def diff_cell(df, y, x, table, sample, stat, fe=(), absorb=None, d=3, **kw):
    o = reg(df, y, [x], fe=fe, absorb=absorb)
    if o is None or x not in o[0]:
        return "n.a.", None
    (b, se, p), n, g = o[0][x], o[1], o[2]
    rec(table, sample, y, stat, b, se, p, n, g, **kw)
    return cell(b, se, p, d), (n, g)


def md_table(header, rows):
    out = ["| | " + " | ".join(header) + " |", "|---|" + "---|" * len(header)]
    out += ["| " + lab + " | " + " | ".join(v) + " |" for lab, v in rows]
    return "\n".join(out)


def km(t, e, horizon=11):
    """Kaplan-Meier survival S(k) after k = 0..horizon-1 years; t = years to event or censoring (>= 0)."""
    s, out, atrisk_rows = 1.0, [], []
    for k in range(horizon):
        n = (t >= k).sum()
        d = ((t == k) & e).sum()
        s *= (1 - d / n) if n > 0 else 1
        out.append(s)
        atrisk_rows.append(n)
    return out, atrisk_rows


# ---------------------------------------------------------------- main
def main():
    OUT.mkdir(exist_ok=True)
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    fam = fam9()
    cs = cs_items()
    disp = pd.read_pickle(DATA / "psid_displacement.pkl")
    mh = marriages()

    # family-unit attributes
    heads = py[py["head"]][["wave", "int", "pid", "female"]].drop_duplicates(["wave", "int"]).rename(
        columns={"pid": "h_pid", "female": "h_fem"})
    kid = py[(~py["head"]) & (~py["wife"]) & py["age"].between(0, 17)].groupby(["wave", "int"]).size()
    fu = heads.merge(kid.rename("nkid").reset_index(), on=["wave", "int"], how="left")
    fu["nkid"] = fu["nkid"].fillna(0)
    fu = fu.merge(fam[["wave", "int", "hh", "wh", "afdc", "fs"]], on=["wave", "int"], how="left")
    fu = fu.merge(cs, on=["wave", "int"], how="left")

    women = py[py["female"] == 1][["pid", "fam68", "wave", "int", "rel", "age", "head", "wife", "hrace", "earn"]]
    women = women.merge(fu, on=["wave", "int"], how="left")

    # ---- separations
    sp = mh[(mh.MH4 == 2) & mh.MH12.isin([4, 5])].copy()
    sp["s"] = sp.MH16.where(sp.MH16.between(1915, 2023)).fillna(sp.MH14.where((sp.MH12 == 4)
                                                                             & sp.MH14.between(1915, 2023)))
    sp = sp.dropna(subset=["s", "sp"])
    sp = sp[sp["s"].between(S_LO, S_HI)]
    nxt = mh[["pid", "MH9", "ymar"]].assign(MH9=lambda x: x.MH9 - 1).rename(columns={"ymar": "y_remar"})
    sp = sp.merge(nxt, on=["pid", "MH9"], how="left")
    sp = sp[["pid", "sp", "s", "MH9", "MH12", "ylast", "y_remar"]]
    print(f"marital-history separations of women, {S_LO}-{S_HI}: {len(sp):,}", flush=True)

    # baseline: the last interview in s-3..s+1 as the wife of that husband, a child 0-17 in the unit
    b = women[women["wife"]].merge(sp, on="pid")
    b = b[(b["h_pid"] == b["sp"]) & b["wave"].between(b["s"] - 3, b["s"] + 1)]
    b = b.sort_values(["pid", "s", "wave"]).groupby(["pid", "s"]).last().reset_index()
    n_obs_married = len(b)
    b = b[(b["nkid"] > 0) & (b["s"] - (b["wave"] - b["age"])).between(25, 59) & b["hrace"].isin(["Black", "White"])]
    b = b.rename(columns={"hrace": "race", "nkid": "nkid0", "age": "age_b", "wave": "wave0"})
    b["age_s"] = b["s"] - (b["wave0"] - b["age_b"])
    b = b.sort_values(["pid", "s"]).drop_duplicates("pid", keep="first")      # first qualifying separation
    b["eid"] = np.arange(len(b))
    # ex-husband displaced in s-2..s (19 main)
    dm = disp[disp["main"] == 1][["pid", "year"]]
    x = b[["eid", "sp", "s"]].merge(dm, left_on="sp", right_on="pid")
    x = x[x["year"].between(x["s"] - 2, x["s"])]
    b["hdisp"] = b["eid"].isin(x["eid"]).astype(float)
    b["black"] = (b["race"] == "Black").astype(float)
    print(f"separations with a married baseline: {n_obs_married:,}; with a child 0-17, aged 25-59, Black/White: "
          f"{len(b):,}", flush=True)

    # ---- panel around the separation
    p = women.merge(b[["pid", "eid", "sp", "s", "race", "black", "hdisp", "y_remar", "ylast", "age_s", "nkid0"]],
                    on="pid", suffixes=("", "_b"))
    p = p.drop(columns=["fam68_b"], errors="ignore")
    p["t"] = p["wave"] - 1
    p["k"] = p["t"] - p["s"]
    p = p[p["k"].between(K_LO, K_HI) & (p["t"] <= Y_HI)].copy()
    p["status"] = np.select([p["head"] & (p["h_pid"] == p["pid"]), p["wife"] & (p["h_pid"] == p["sp"]),
                             p["wife"] & (p["h_pid"] != p["sp"])], ["single", "wife_ex", "wife_new"], "other")
    p["hrs"] = np.where(p["status"] == "single", p["hh"], np.where(p["status"].str.startswith("wife"), p["wh"],
                                                                   np.nan))
    p["emp"] = (p["hrs"] > 0).astype(float).where(p["hrs"].notna())
    p["cs"] = np.where(p["status"] == "single", p["cs_h"], np.where(p["status"].str.startswith("wife"), p["cs_w"],
                                                                    np.nan))
    p.loc[p["k"] < 0, "cs"] = np.nan
    p["cs_pos"] = (p["cs"] > 0).astype(float).where(p["cs"].notna())
    p["cs_month"] = p["cs"] / 12
    p["labinc"] = p["earn"].where(p["status"] != "other")
    p["remarried"] = (p["y_remar"] <= p["t"]).astype(float)
    p["kcat"] = pd.cut(p["nkid"], [-1, 0, 1, 2, 99], labels=["0", "1", "2", "3+"]).astype(str)
    for c in ("single", "wife_new", "wife_ex", "other"):
        p[f"st_{c}"] = (p["status"] == c).astype(float)
    p = p.drop_duplicates(["eid", "t"])

    # married-mother benchmark
    mm = women[women["wife"] & (women["h_fem"] == 0) & women["age"].between(25, 59) & (women["nkid"] > 0)
               & women["hrace"].isin(["Black", "White"])].copy()
    mm["t"] = mm["wave"] - 1
    mm = mm[mm["t"].between(S_LO, Y_HI)]
    mm["hrs"], mm["race"] = mm["wh"], mm["hrace"]
    mm["emp"] = (mm["hrs"] > 0).astype(float).where(mm["hrs"].notna())

    md = ["# The separated wife's state in the PSID: child support, remarriage, work, program receipt", "",
          "Built by `IGE/76.SeparatedMothers.py` (2026-10-20; WP3 of `IGE/proposals/fable_10h_plan_paperA.md`); "
          "definitions in its docstring. Mothers whose marriage ended (marital history: separation, else divorce "
          f"year s) in {S_LO}-{S_HI}, observed as that husband's wife at an interview in s-3..s+1 with a child "
          "0-17 in the family unit, aged 25-59 at s, Black / White (head's race). Event time k = income year - s "
          f"(income years <= {Y_HI}; all observed years, no balanced panel). Amounts in 2000 dollars. Unweighted "
          "SRC + SEO. Means with s.e. in parentheses; differences with stars and p-values; s.e. clustered by 1968 "
          "family; *** p<0.01, ** p<0.05, * p<0.1.", ""]

    # ---- 1. sample
    rows = []
    for race in ("Black", "White"):
        g = b[b["race"] == race]
        q = p[p["race"] == race]
        rows.append((race, [f"{len(g):,}", f"{g['age_s'].mean():.1f}", f"{g['nkid0'].mean():.2f}",
                            f"{(g['MH12'] == 4).mean():.3f}", f"{g['hdisp'].mean():.3f}",
                            f"{q.loc[q['k'] >= 0, 'eid'].nunique():,}", f"{(q['k'] >= 0).sum():,}"]))
        for v in ("age_s", "nkid0", "hdisp"):
            rec("sample", race, v, "mean", g[v].mean(), n=len(g))
        rec("sample", race, "separations", "count", len(g))
    md += ["## 1. Sample", "", md_table(["Mothers", "Age at s", "Children 0-17 at baseline", "Status 'divorced'",
                                         "Ex-husband displaced s-2..s", "Observed after s", "Woman-years k>=0"],
                                        rows), ""]

    # ---- 2. status by year since separation
    ks = list(range(0, 11))
    rows = []
    for race in ("Black", "White"):
        q = p[p["race"] == race]
        for c, lab in (("st_single", "single (female head)"), ("st_wife_new", "new partner (wife / 'wife')"),
                       ("st_wife_ex", "with the ex-husband"), ("st_other", "in another person's unit"),
                       ("remarried", "remarried (marital history)")):
            vals = []
            for k in ks:
                g = q[q["k"] == k]
                vals.append(f"{g[c].mean():.3f}" if len(g) else "")
                rec("status", race, c, f"k={k}", g[c].mean(), n=len(g))
            rows.append((f"{race}: {lab}", vals))
        rows.append((f"{race}: N", [f"{(q['k'] == k).sum():,}" for k in ks]))
    md += ["## 2. Where she is, by year since the separation", "",
           "Shares of woman-years at each k (status at the interview of income year s + k).", "",
           md_table([f"k={k}" for k in ks], rows), ""]

    # ---- 3. remarriage / new partner hazard
    last_t = p.groupby("eid")["t"].max()
    first_new = p[(p["status"] == "wife_new") & (p["k"] >= 0)].groupby("eid")["t"].min()
    r = b[["eid", "fam68", "race", "black", "hdisp", "s", "y_remar", "ylast"]].copy()
    r["cens_m"] = r["ylast"].fillna(r["eid"].map(last_t)).clip(upper=Y_HI)
    r["ev_m"] = r["y_remar"].notna() & (r["y_remar"] <= r["cens_m"])
    r["T_m"] = np.where(r["ev_m"], r["y_remar"], r["cens_m"]) - r["s"]
    r["y_new"] = np.fmin(r["y_remar"].to_numpy(), r["eid"].map(first_new).to_numpy())
    r["cens_n"] = np.fmax(r["cens_m"].to_numpy(), r["eid"].map(last_t).fillna(-1).to_numpy())
    r["ev_n"] = r["y_new"].notna() & (r["y_new"] <= r["cens_n"])
    r["T_n"] = np.where(r["ev_n"], r["y_new"], r["cens_n"]) - r["s"]
    r = r[r["T_m"] >= 0]
    r["T_m"], r["T_n"] = r["T_m"].clip(lower=0), r["T_n"].clip(lower=0)
    HZ = {}
    rows = []
    hor = [1, 2, 3, 5, 10]
    for kind, T, E, lab in (("remarriage", "T_m", "ev_m", "Remarriage (marital history)"),
                            ("new_partner", "T_n", "ev_n", "New partner (remarriage or cohabiting 'wife')")):
        # woman-years at risk, years 0-9
        ry = []
        for _, w in r.iterrows():
            last = int(min(w[T], 9))
            for k in range(0, last + 1):
                ry.append((w["eid"], w["fam68"], w["race"], w["black"], w["hdisp"], k,
                           float(bool(w[E]) and k == int(w[T]))))
        ry = pd.DataFrame(ry, columns=["eid", "fam68", "race", "black", "hdisp", "k", "event"])
        for race in ("Black", "White"):
            g = r[r["race"] == race]
            S, nr = km(g[T].to_numpy(), g[E].to_numpy())
            o = reg(ry[ry["race"] == race], "event")
            (h, se, pp), n, cl = o[0]["const"], o[1], o[2]
            HZ[(kind, race)] = (h, se)
            rec("hazard", race, kind, "annual hazard, years 0-9", h, se, pp, n, cl)
            for k in hor:
                rec("hazard", race, kind, f"KM share not yet, end of year {k - 1}", S[k - 1], n=int(nr[k - 1]))
            rows.append((f"{lab}: {race}", [f"{1 - S[k - 1]:.3f}" for k in hor] + [f"{h:.4f} ({se:.4f})",
                                                                                    f"{len(g):,} / {n:,}"]))
        dc, _ = diff_cell(ry, "event", "black", "hazard", "Pooled", f"{kind}: Black - White annual hazard")
        rows.append((f"{lab}: Black - White", [""] * len(hor) + [dc, f"{len(ry):,}"]))
        dd, _ = diff_cell(ry, "event", "hdisp", "hazard", "Pooled", f"{kind}: ex-husband displaced - not",
                          fe=["race"])
        rows.append((f"{lab}: ex-husband displaced - not (race FE)", [""] * len(hor) + [dd, f"{len(ry):,}"]))
    md += ["## 3. Remarriage and new partners", "",
           "Kaplan-Meier cumulative share (1 - survival) by the end of year k after the separation year (k = 0 is the "
           "separation year itself); annual hazard = events / woman-years at risk over years 0-9 (mean of the event "
           "indicator, s.e. clustered by 1968 family). Differences: LPM on the woman-years at risk.", "",
           md_table([f"by end of year {k - 1}" for k in hor] + ["Annual hazard, years 0-9", "Mothers / woman-years"],
                    rows), ""]

    # ---- 4. child support
    single = p[(p["status"] == "single") & (p["k"] >= 0) & (p["nkid"] > 0)]
    allpost = p[(p["k"] >= 0) & p["status"].isin(["single", "wife_new", "wife_ex"])]
    rows = []
    for race in ("Black", "White"):
        for lab, q in (("single, children in unit, k = 0-10", single[single["race"] == race]),
                       ("single, children in unit, k = 1-5", single[(single["race"] == race)
                                                                    & single["k"].between(1, 5)]),
                       ("any status (head or wife), k = 0-10", allpost[allpost["race"] == race])):
            q = q.dropna(subset=["cs"])
            pos = q[q["cs"] > 0]
            ratio = q["cs"].mean() / q["labinc"].mean() if q["labinc"].notna().any() else np.nan
            rows.append((f"{race}: {lab}", [
                mean_cell(q, "cs_pos", "child_support", race, f"share positive | {lab}"),
                mean_cell(q, "cs_month", "child_support", race, f"monthly mean | {lab}", d=0),
                f"{q['cs_month'].median():,.0f}", f"{pos['cs_month'].mean():,.0f}" if len(pos) else "",
                f"{pos['cs_month'].median():,.0f}" if len(pos) else "", f"{ratio:.3f}",
                f"{len(q):,} / {q['eid'].nunique():,}"]))
            rec("child_support", race, "cs_month", f"median | {lab}", q["cs_month"].median(), n=len(q))
            rec("child_support", race, "cs_month", f"mean if positive | {lab}", pos["cs_month"].mean(), n=len(pos))
            rec("child_support", race, "cs/labinc", f"ratio of means | {lab}", ratio, n=len(q))
    dif = []
    for y, lab in (("cs_pos", "share positive"), ("cs_month", "monthly amount")):
        c1, nn = diff_cell(single.dropna(subset=["cs"]), y, "black", "child_support", "Pooled",
                           f"Black - White {lab} | single, k = 0-10", d=3 if y == "cs_pos" else 1)
        c2, _ = diff_cell(single.dropna(subset=["cs"]), y, "black", "child_support", "Pooled",
                          f"Black - White {lab} | single, k = 0-10, children / k / year FE",
                          fe=["kcat", "k", "t"], d=3 if y == "cs_pos" else 1)
        dif.append((f"Black - White, {lab}", [c1, c2, f"{nn[0]:,}" if nn else ""]))
    md += ["## 4. Child support received after the separation", "",
           "Her own child-support income (2000 dollars per month = annual / 12). 'Single' = she is the female "
           "head of her unit (the model's separated state) with at least one child 0-17 in it.", "",
           md_table(["Share receiving", "Mean per month", "Median per month", "Mean if receiving",
                     "Median if receiving", "Child support / her labor income (ratio of means)",
                     "Woman-years / mothers"], rows), "",
           md_table(["Raw", "Children / k / calendar-year FE", "N (woman-years)"], dif), ""]

    # calibrated input: race x number of children (single mothers, k = 0-10)
    rows = []
    for race in ("Black", "White"):
        vals = []
        for kc in ("1", "2", "3+"):
            q = single[(single["race"] == race) & (single["kcat"] == kc)].dropna(subset=["cs"])
            vals.append(mean_cell(q, "cs_month", "cs_input", race, f"monthly mean | children {kc}", d=0,
                                  kcat=kc) + f"; share {q['cs_pos'].mean():.3f}; N {len(q):,}")
            rec("cs_input", race, "cs_pos", f"share positive | children {kc}", q["cs_pos"].mean(), n=len(q), kcat=kc)
        q = single[single["race"] == race].dropna(subset=["cs"])
        vals.append(mean_cell(q, "cs_month", "cs_input", race, "monthly mean | all", d=0))
        rows.append((race, vals))
    # decay with k
    rows2 = []
    for race in ("Black", "White"):
        vals = []
        for lo, hi in ((0, 1), (2, 4), (5, 10)):
            q = single[(single["race"] == race) & single["k"].between(lo, hi)].dropna(subset=["cs"])
            vals.append(mean_cell(q, "cs_month", "cs_by_k", race, f"monthly mean | k {lo}-{hi}", d=0)
                        + f"; share {q['cs_pos'].mean():.3f}")
        rows2.append((race, vals))
    # by period (enforcement: 1984 Amendments, 1988 Family Support Act, PRWORA 1996)
    rows3 = []
    for race in ("Black", "White"):
        vals = []
        for lo, hi in ((1984, 1995), (1996, 2007), (2008, 2021)):
            q = single[(single["race"] == race) & single["t"].between(lo, hi)].dropna(subset=["cs"])
            vals.append(mean_cell(q, "cs_month", "cs_by_period", race, f"monthly mean | {lo}-{hi}", d=0)
                        + f"; share {q['cs_pos'].mean():.3f}; N {len(q):,}")
        rows3.append((race, vals))
    md += ["### 4b. Diagnostic-B input: monthly child support of single mothers by race and number of children",
           "", "Mean per month (2000 dollars, s.e.), zeros included; share receiving; woman-years (k = 0-10).", "",
           md_table(["1 child", "2 children", "3+ children", "All"], rows), "",
           "By years since the separation:", "", md_table(["k = 0-1", "k = 2-4", "k = 5-10"], rows2), "",
           "By calendar income year:", "", md_table(["1984-1995", "1996-2007", "2008-2021"], rows3), ""]

    # ---- 5. employment and hours; 6. program receipt
    def by_k_block(ys, title, note):
        out = ["## " + title, "", note, ""]
        kk = list(range(K_LO, K_HI + 1))
        rows = []
        for race in ("Black", "White"):
            q = p[(p["race"] == race) & p["status"].isin(["single", "wife_new", "wife_ex"])]
            m0 = mm[mm["race"] == race]
            for y, lab in ys:
                vals = []
                for k in kk:
                    g = q[q["k"] == k][y].dropna()
                    vals.append(f"{g.mean():.3f}" if y != "hrs" and len(g) else f"{g.mean():,.0f}" if len(g) else "")
                    rec("by_k", race, y, f"k={k}", g.mean(), n=len(g))
                bm = m0[y].dropna()
                rec("by_k", race, y, "married mothers 1984-2021", bm.mean(), n=len(bm))
                rows.append((f"{race}: {lab}", vals + [f"{bm.mean():.3f}" if y != "hrs" else f"{bm.mean():,.0f}"]))
            rows.append((f"{race}: N (head or wife)", [f"{(q['k'] == k).sum():,}" for k in kk] + [f"{len(m0):,}"]))
        out += [md_table([f"k={k}" for k in kk] + ["Married mothers"], rows), ""]
        # differences
        drows = []
        for race in ("Black", "White", "Pooled"):
            q = p if race == "Pooled" else p[p["race"] == race]
            m0 = mm if race == "Pooled" else mm[mm["race"] == race]
            sg = q[(q["status"] == "single") & q["k"].between(1, 5)]
            st = pd.concat([sg.assign(sep=1.0, unit=sg["eid"]), m0.assign(sep=0.0, unit=-1)], ignore_index=True)
            st["agegrp"] = (st["age"] // 5).astype(float)
            fe = ["agegrp", "t"] + (["race"] if race == "Pooled" else [])
            pre_post = q[q["status"].isin(["single", "wife_ex", "wife_new"])
                         & (q["k"].between(-3, -1) | q["k"].between(1, 5))].copy()
            pre_post["post"] = (pre_post["k"] >= 1).astype(float)
            pre_post = pre_post[((pre_post["k"] < 0) & (pre_post["status"] == "wife_ex"))
                                | ((pre_post["k"] >= 1) & (pre_post["status"] == "single"))]
            for y, lab in ys:
                c1, n1 = diff_cell(st, y, "sep", "differences", race, f"{y}: single mothers k=1-5 - married mothers",
                                   d=3 if y != "hrs" else 0)
                c2, n2 = diff_cell(st, y, "sep", "differences", race,
                                   f"{y}: single mothers k=1-5 - married mothers, age-group and year FE", fe=fe,
                                   d=3 if y != "hrs" else 0)
                c3, n3 = diff_cell(pre_post, y, "post", "differences", race,
                                   f"{y}: within mother, single k=1-5 - married k=-3..-1 (mother FE)",
                                   absorb="eid", d=3 if y != "hrs" else 0)
                c4, n4 = diff_cell(q[(q["status"] == "single") & q["k"].between(1, 5)], y, "hdisp", "differences",
                                   race, f"{y}: single k=1-5, ex-husband displaced s-2..s - not",
                                   fe=["race"] if race == "Pooled" else (), d=3 if y != "hrs" else 0)
                drows.append((f"{race}: {lab}", [f"{c1} [N {n1[0]:,}]" if n1 else c1, c2,
                                                 f"{c3} [N {n3[0]:,}]" if n3 else c3,
                                                 f"{c4} [N {n4[0]:,}]" if n4 else c4]))
        out += ["Differences (OLS, s.e. clustered by 1968 family):", "",
                md_table(["Single mothers k=1-5 - married mothers (raw)", "... with age-group and year FE",
                          "Within mother: single k=1-5 - married k=-3..-1 (mother FE)",
                          "Ex-husband displaced s-2..s - not (single, k=1-5)"], drows), ""]
        return out

    md += by_k_block([("emp", "employed (hours > 0)"), ("hrs", "annual hours")],
                     "5. Her employment and hours by year since the separation",
                     "Woman-years in which she is a head or a wife (family-file hours). k < 0: she is still the "
                     "ex-husband's wife (her hours as a wife). Benchmark: all married mothers 25-59 with a child 0-17, "
                     "income years 1984-2021 (the model's married wives' employment is about 0.81 in the data).")
    md += by_k_block([("afdc", "AFDC/TANF (head or wife)"), ("fs", "food stamps / SNAP (family)")],
                     "6. AFDC/TANF and food stamp receipt by year since the separation",
                     "Same woman-years. AFDC/TANF = head or wife received last year; food stamps = the family "
                     "received last year (biennial era: last-year item only).")

    # by displacement of the ex-husband: child support
    rows = []
    for race in ("Black", "White", "Pooled"):
        q = single if race == "Pooled" else single[single["race"] == race]
        q = q.dropna(subset=["cs"])
        vals = []
        for y in ("cs_pos", "cs_month"):
            c, nn = diff_cell(q, y, "hdisp", "by_hdisp", race, f"{y}: ex-husband displaced s-2..s - not",
                              fe=["race"] if race == "Pooled" else (), d=3 if y == "cs_pos" else 1)
            vals.append(c)
        vals.append(f"{len(q):,} ({int(q.loc[q['hdisp'] == 1, 'eid'].nunique())} mothers with a displaced "
                    f"ex-husband)")
        rows.append((race, vals))
    md += ["## 7. Child support when the ex-husband had been displaced (s-2..s)", "",
           "Single mothers with children, k = 0-10. Difference displaced - not displaced (pooled: race FE).", "",
           md_table(["Share receiving", "Monthly amount", "N (woman-years)"], rows), ""]

    res = pd.DataFrame(ROWS)
    res.to_csv(OUT / "separated_mothers.csv", index=False)
    (OUT / "separated_mothers.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))
    print({k: v for k, v in HZ.items()})


if __name__ == "__main__":
    main()
