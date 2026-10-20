r"""Identification checks for the father's displacement -> children link (2026-10-17).

Builds on 19.FatherDisplacement.py (its functions are imported, its main() is not run; nothing there is changed).
Reads (read only) data/psid_displacement.pkl, psid_person_year.pkl, psid_child_exposure.pkl, psid_kids.pkl,
cds_scores.pkl, the raw PSID family files and individual file (Dropbox/PSID, via 1.PSID.py / 9.ChildExposure.py
readers), and data/ui_generosity.csv if it exists. Writes
  output/displacement_id.csv   every estimate (table, design, sample, outcome, term, coef, se, p, n, clusters)
  output/displacement_id.md    tables

Displacement = the head's (father figure's) report that his job ended because the company folded / moved / went out of
business (closure, code 1) or he was laid off / fired (code 3; 2021-23 also code 5 = Covid layoff); see 19's docstring.
Children, father figures, the (pseudo) event design, the controls (log pre-event family income, parental education
<12/12/13-15/16+/missing, female, birth-year FE, + CDS-wave FE; + Black in pooled rows) and the outcomes are those of
19.FatherDisplacement.py, Section 3. S.e. clustered by 1968 family (fam68), CR1; p-values normal; *** <0.01 ** <0.05
* <0.1.

1. CLOSURES ONLY ("closure-first"): treated = the father figure's FIRST displacement in the child's childhood (CDS:
   before the test) is a plant closure / move and falls in the age band; children whose first displacement was a
   layoff / firing are dropped; controls = never displaced (closure or layoff) at 0-17 (CDS: before the test).
   (19's Section 4 kept treated children with an earlier layoff; this is stricter.)
2. SIBLING DESIGN. Family = the mother (CAH mother; for children born 1951-67 without a CAH record, the wife / female
   head of the unit in which the child is first seen as a child). Father figure at birth (fb) = the earliest father
   figure observed for the child; D = fb's first displacement (main definition; observed from 1967); a = D - birth year.
   Categories: exposed (0 <= a <= 17 and living with fb in D; bands 0-5 / 6-11 / 12-17), older sibling (a >= 18;
   the reference group), later-born (a < 0), fb never displaced (own dummy). Exposed and older siblings must have
   lived with fb in >= 80% of their observed childhood years before D (symmetric co-residence rule; without it
   'exposed' selects children living with a father figure). Dropped: a in 0-17 but not living with fb in D;
   children whose own childhood exposure comes from another father figure (or precedes fb's first displacement).
   OLS with mother FE (absorbed; singletons dropped), birth-year FE, female, birth order (2, 3+). Variants: parents
   FE (mother x fb); 'later-born siblings as controls' (only exposed and later-born siblings of displaced fathers);
   closures (families whose fb's first displacement is a closure, plus never-displaced families). Families with
   variation are counted in each regression sample.
3. PRE-TREND / SELECTION. (a) Future displacement: the last childhood father figure (ages 12-17) displaced when the
   child is 18-25 (or 22-25) and the child never displaced at 0-17, vs displaced first at 12-17, vs neither; birth
   years 1956-1997; father figure observed >= 2 years in the 18-25 window and working at child age 12-14; log family
   income at ages 9-12. CDS analogue: displacement of the father figure at the test in test year + 1..+4 (lead) vs
   before the test. (b) Balance: pre-event covariates regressed on 'displaced' + birth-year FE. (c) Controls for the
   father's pre-displacement trajectory: 3-year growth of his family income and labor income (log, latest of d-1/d-2
   minus earliest of d-4/d-5, annualized x 3), log labor income at d-2/d-3, + his occupation (8 groups) and industry
   (10 groups) in the latest interview in d-3..d.
4. SEVERITY. Relative earnings loss = father's mean labor income over d+1..d+3 / mean over d-3..d-2 - 1 (the event-
   study reference window); split at the median among the treated in each sample. Receipt after the loss: head's
   unemployment compensation > 0 (d or d+1) and family food stamps (d or d+1).
5. SAFETY-NET BUFFERING: exposure x UI generosity (state of the father's family in the interview of d or d-1, else
   d+1; data/ui_generosity.csv, z-scored), if the file exists.

Raw family-file variables added here (labels matched in each wave's .do file):
  occupation of head  1968-80 'OCCUPATION OF HEAD yy' (_A retrospective 1970 Census codes); 1981-2001 'MAIN OCC 3 DIG
                      (H-E/HD-E)', else 'OCC-LAST JOB (H-U/HD-U)'; 2003-15 'BC20 MAIN OCC FOR JOB 1: 2000 CODE';
                      2017-23 'BC20 MAIN OCC FOR JOB 1: 2010 CODE' (/10)
  industry of head    likewise ('INDUSTRY OF HEAD yy' _A/_B; 'MAIN IND 3 DIGT'; 'IND-LAST JOB'; 'BC21 MAIN IND FOR
                      JOB 1' 2000 / 2012 codes)
  head's UI amount    1970-72 / 1974 'UNEMP,WRK.COMP' / 'ANN UNEMP COMP' (family, incl. workers' compensation),
                      1976 'HD UNEMP WRK COMP' (incl. workers' compensation), 1977-1993 'HD yy UNEMP COMP', 1994-2003
                      'AMT UNEMPL COMP OF HEAD', 2005-2023 'HEAD / REF PERSN UNEMPLOYMENT COMPENSATION-yyyy'
                      (no item in 1968, 1969 (bracket only), 1973, 1975)
  state               1976-2023 PSID state code (8.FirstStage.py list) -> FIPS
"""
import importlib.util
import re
import warnings

import numpy as np
import pandas as pd
from scipy import stats

from common import DATA, OUT, HERE, stars

warnings.simplefilter("ignore", FutureWarning)
warnings.simplefilter("ignore", RuntimeWarning)
pd.options.mode.chained_assignment = None


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


fd = _load("fd19", "19.FatherDisplacement.py")          # functions only
psid1, psid9 = fd.psid1, fd.psid9
WAVES, FAM, read = psid1.WAVES, psid1.FAM, psid1.read

# ---------------------------------------------------------------- raw family-file extras
INFIX = re.compile(r"(?:long\s+)?([A-Z]+\d+[A-Z0-9_]*)\s+(\d+)\s*-\s*(\d+)")      # allows _A / _B suffixes


def layout(do):
    t = do.read_text(encoding="latin-1")
    block = re.search(r"\binfix\b(.*?)\busing\b", t, re.S).group(1)
    return {v: (int(a) - 1, int(b)) for v, a, b in INFIX.findall(block)}, psid1.layout(do)[1]


PAT = {"occ": r"(OCCUPATION OF HEAD\s+\d\d$)|(MAIN OCC.*(H-E|HD-E|\(HD\)|\(RP\)))|(BC20 MAIN OCC FOR JOB 1)",
       "ind": r"(INDUSTRY\s+OF HEAD\s+\d\d$)|(MAIN IND.*(H-E|HD-E|\(HD\)|\(RP\)))|(BC21 MAIN IND FOR JOB 1)",
       "occu": r"OCC.*LAST JOB.*(H-U|HD-U)", "indu": r"IND.*LAST JOB.*(H-U|HD-U)"}
UI = {1970: "V1214", 1971: "V1916", 1972: "V2517", 1974: "V3482", 1976: "V4397", 1977: "V5308", 1978: "V5808",
      1979: "V6419", 1980: "V7009", 1981: "V7601", 1982: "V8294", 1983: "V8902", 1984: "V10295", 1985: "V11440",
      1986: "V12839", 1987: "V13941", 1988: "V14956", 1989: "V16456", 1990: "V17872", 1991: "V19172",
      1992: "V20472", 1993: "V22108", 1994: "ER3371", 1995: "ER6372", 1996: "ER8489", 1997: "ER11383",
      1999: "ER14649", 2001: "ER18815", 2003: "ER22185", 2005: "ER27968", 2007: "ER40958", 2009: "ER46866",
      2011: "ER52274", 2013: "ER58077", 2015: "ER65270", 2017: "ER71347", 2019: "ER77369", 2021: "ER81696",
      2023: "ER85550"}
STATE = {1976: "V4303", 1977: "V5203", 1978: "V5703", 1979: "V6303", 1980: "V6903", 1981: "V7503", 1982: "V8203",
         1983: "V8803", 1984: "V10003", 1985: "V11103", 1986: "V12503", 1987: "V13703", 1988: "V14803",
         1989: "V16303", 1990: "V17703", 1991: "V19003", 1992: "V20303", 1993: "V21603", 1994: "ER4156",
         1995: "ER6996", 1996: "ER9247", 1997: "ER12221", 1999: "ER13004", 2001: "ER17004", 2003: "ER21003",
         2005: "ER25003", 2007: "ER36003", 2009: "ER42003", 2011: "ER47303", 2013: "ER53003", 2015: "ER60003",
         2017: "ER66003", 2019: "ER72003", 2021: "ER78003", 2023: "ER82003"}
PSID2FIPS = dict(enumerate([1, 4, 5, 6, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                            30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48, 49, 50, 51, 53,
                            54, 55, 56, 2, 15], start=1))
OCCG = {1: "professional / technical", 2: "managers", 3: "sales / clerical", 4: "craft", 5: "operatives / transport",
        6: "laborers / farm", 7: "service", 8: "other / military"}
INDG = {1: "agriculture / mining", 2: "construction", 3: "durable manufacturing", 4: "nondurable manufacturing",
        5: "transport / communications / utilities", 6: "trade", 7: "finance / insurance / real estate",
        8: "business / personal services", 9: "professional services (education / health)", 10: "public admin."}


def _bins(c, spec):
    out = np.zeros(len(c))
    for lo, hi, g in spec:
        out = np.where((c >= lo) & (c <= hi) & (out == 0), g, out)
    return np.where(np.isnan(c), 0, np.where(out == 0, 8 if spec is OCC70 or spec is OCC00 else 0, out))


OCC70 = [(1, 195, 1), (201, 245, 2), (260, 395, 3), (401, 600, 4), (601, 715, 5), (740, 824, 6), (901, 984, 7)]
OCC00 = [(1, 95, 2), (100, 354, 1), (360, 465, 7), (470, 594, 3), (600, 613, 6), (620, 763, 4), (770, 975, 5)]
IND70 = [(17, 58, 1), (67, 78, 2), (107, 259, 3), (268, 399, 4), (407, 479, 5), (507, 699, 6), (707, 718, 7),
         (727, 817, 8), (828, 897, 9), (907, 947, 10)]
IND00 = [(17, 49, 1), (57, 69, 5), (77, 77, 2), (107, 239, 4), (247, 399, 3), (407, 579, 6), (607, 679, 5),
         (687, 719, 7), (727, 779, 8), (786, 847, 9), (856, 929, 8), (937, 987, 10)]


def fam_extra():
    """wave x int: head's occupation / industry group, head's UI amount, state (FIPS)."""
    out = []
    for w in WAVES:
        folder = FAM / (f"fam{w}" if w < 1994 else f"fam{w}er")
        base = next(f for f in folder.glob("*.do") if "formats" not in f.name).with_suffix("")
        pos, labs = layout(base.with_suffix(".do"))
        idv = "V3" if w == 1968 else labs[1][0]
        v = {k: next((a for a, l in labs if re.search(p, l)), None) for k, p in PAT.items()}
        if not 1981 <= w <= 2001:                    # 1979-80 last-job codes are 2-digit
            v["occu"] = v["indu"] = None
        v["ui"], v["st"] = UI.get(w), STATE.get(w)
        f = read(base, [idv] + [c for c in v.values() if c], pos)
        sysc = "c70" if w <= 2001 else "c00" if w <= 2015 else "c10"
        na = 9999 if sysc == "c10" else 999

        def code(c):
            if not c:
                return pd.Series(np.nan, index=f.index)
            s = pd.to_numeric(f[c], errors="coerce").astype(float)
            return s.where((s > 0) & (s < na))
        occ = code(v["occ"]).fillna(code(v["occu"]))
        ind = code(v["ind"]).fillna(code(v["indu"]))
        if sysc == "c10":
            occ, ind = occ // 10, ind // 10
        x = pd.DataFrame({"wave": w, "int": f[idv]})
        x["occg"] = _bins(occ.to_numpy(), OCC70 if sysc == "c70" else OCC00)
        x["indg"] = _bins(ind.to_numpy(), IND70 if sysc == "c70" else IND00)
        if v["ui"]:
            u = pd.to_numeric(f[v["ui"]], errors="coerce").astype(float)
            x["ui_amt"] = u.where((u >= 0) & (u < 99998))
        else:
            x["ui_amt"] = np.nan
        x["fips"] = f[v["st"]].map(PSID2FIPS) if v["st"] else np.nan
        out.append(x)
    return pd.concat(out, ignore_index=True)


# ---------------------------------------------------------------- regression engine
ROWS = []


def pval(b, se):
    return 2 * stats.norm.sf(abs(b / se)) if se > 0 else np.nan


def reg(df, y, xs, ctrl=(), fe=(), absorb=None, pe=True, extra=(), cluster="fam68"):
    """OLS of y on xs + ctrl + FE dummies (+ parental-education dummies), optionally absorbing one FE (within
    transformation, singletons dropped; FE nested in clusters are not counted in the d.o.f., as in reghdfe).
    CR1 cluster-robust covariance. Returns dict(est, V, idx, n, clusters, kids, mean, q)."""
    cols = list(dict.fromkeys([y, *xs, *ctrl, *fe, cluster, "pid", *extra] + (["pe"] if pe else [])
                              + ([absorb] if absorb else [])))
    q = df[cols].replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)
    if absorb:
        q = q[q.groupby(absorb)[y].transform("size") > 1].reset_index(drop=True)
    Z = q[list(xs) + list(ctrl)].astype(float)
    for f in fe:
        Z = Z.join(pd.get_dummies(q[f].astype(np.int64), prefix=f, drop_first=True, dtype=float))
    if pe:
        Z = Z.join(pd.get_dummies(q["pe"], prefix="pe", dtype=float).drop(columns="pe_12", errors="ignore"))
    Y, X, names = q[y].to_numpy(float), Z.to_numpy(float), list(Z.columns)
    if absorb:
        g = pd.factorize(q[absorb])[0]
        ng = g.max() + 1
        cnt = np.bincount(g, minlength=ng).astype(float)

        def dm(A):
            mu = np.column_stack([np.bincount(g, weights=A[:, j], minlength=ng) for j in range(A.shape[1])]) / cnt[:, None]
            return A - mu[g]
        Y, X = dm(Y[:, None])[:, 0], dm(X)
        keep = X.std(axis=0) > 1e-10
    else:
        X = np.column_stack([np.ones(len(X)), X])
        names = ["const"] + names
        keep = X.std(axis=0) > 1e-10
        keep[0] = True
    for v in xs:
        if not keep[names.index(v)]:
            raise ValueError(f"no variation in {v}")
    X, names = X[:, keep], [n for n, k in zip(names, keep) if k]
    XtX = np.linalg.pinv(X.T @ X)
    b = XtX @ X.T @ Y
    e = Y - X @ b
    cl = pd.factorize(q[cluster])[0]
    G = cl.max() + 1
    S = np.zeros((G, X.shape[1]))
    np.add.at(S, cl, X * e[:, None])
    n, k = X.shape
    V = G / (G - 1) * (n - 1) / max(n - k, 1) * XtX @ (S.T @ S) @ XtX
    idx = {v: names.index(v) for v in list(xs) + list(ctrl) if v in names}
    est = {v: (b[i], np.sqrt(V[i, i]), pval(b[i], np.sqrt(V[i, i]))) for v, i in idx.items()}
    return dict(est=est, V=V, idx=idx, n=n, clusters=G, kids=q["pid"].nunique(), mean=q[y].mean(), q=q,
                groups=q[absorb].nunique() if absorb else None)


def diff_test(r, a, b):
    ia, ib = r["idx"][a], r["idx"][b]
    d = r["est"][a][0] - r["est"][b][0]
    se = np.sqrt(r["V"][ia, ia] + r["V"][ib, ib] - 2 * r["V"][ia, ib])
    return d, se, pval(d, se)


def cell(t):
    b, se, p = t
    pv = "<0.001" if p < 0.001 else f"{p:.3f}"
    return f"{b:.3f}{stars(p)} ({se:.3f}; p={pv})"


LABY = dict(fd.LABY)
LABX = {"treat": "Father figure displaced", "lpre": "Log pre-event family income", "female": "Female",
        "g_fam": "Father's family-income growth, 3 yrs before (log)", "g_lab": "Father's labor-income growth, 3 yrs "
        "before (log)", "llab2": "Log father's labor income, d-2/d-3",
        "A": "Displaced first at 12-17 (childhood)", "F": "Displaced at 18-25 only (after childhood)",
        "F22": "Displaced at 22-25 only (after childhood)",
        "Bf": "Displaced before the test", "L": "Displaced 1-4 years after the test (lead)",
        "exp": "Exposed at 0-17 (father's first displacement)", "exp05": "Exposed at 0-5", "exp611": "Exposed at 6-11",
        "exp1217": "Exposed at 12-17", "later": "Later-born sibling (born after the displacement)",
        "never": "Father figure never displaced (half-sibling)",
        "dur": "Exposed x years of childhood after the displacement (18 - age)",
        "t_hi": "Displaced, earnings loss above median", "t_lo": "Displaced, earnings loss below median",
        "t_ui1": "Displaced, head received UI (d or d+1)", "t_ui0": "Displaced, no UI received",
        "t_fs1": "Displaced, family received food stamps (d or d+1)", "t_fs0": "Displaced, no food stamps",
        "t_x_ui": "Displaced x UI generosity (z)", "ui_z": "UI generosity (z)"}


def run(df, ys, xs, ctrl, fe, table, design, sample, absorb=None, pe=True, extra=(), tests=(), show=None,
        counts=None):
    """One regression per outcome; returns md rows (show terms, tests, mean, N, clusters, counts)."""
    out = {}
    for y in ys:
        try:
            r = reg(df, y, xs, ctrl, fe, absorb=absorb, pe=pe, extra=extra)
        except Exception as exc:                                     # too few observations / no variation
            print("skip", table, design, sample, y, exc)
            continue
        out[y] = r
        for v, (b, se, p) in r["est"].items():
            ROWS.append(dict(table=table, design=design, sample=sample, outcome=y, term=v, coef=b, se=se, p=p,
                             n=r["n"], clusters=r["clusters"], children=r["kids"], fe_groups=r["groups"]))
        for a, b_ in tests:
            d, se, p = diff_test(r, a, b_)
            ROWS.append(dict(table=table, design=design, sample=sample, outcome=y, term=f"{a} - {b_}", coef=d,
                             se=se, p=p, n=r["n"], clusters=r["clusters"], children=r["kids"],
                             fe_groups=r["groups"]))
    rows = []
    for v in (show or xs):
        rows.append((LABX.get(v, v), [cell(out[y]["est"][v]) if y in out and v in out[y]["est"] else "" for y in ys]))
    for a, b_ in tests:
        rows.append((f"Difference: {LABX.get(a, a)} minus {LABX.get(b_, b_)}",
                     [cell(diff_test(out[y], a, b_)) if y in out else "" for y in ys]))
    rows.append(("Mean of outcome", [f"{out[y]['mean']:.3f}" if y in out else "" for y in ys]))
    rows.append(("N (children" + (" x tests" if "tyear" in fe else "") + ")",
                 [f"{out[y]['n']:,}" if y in out else "" for y in ys]))
    for v in [v for v in xs if all(set(out[y]["q"][v].unique()) <= {0.0, 1.0} for y in out)][:3]:
        rows.append((f"  of which {LABX.get(v, v).lower()}",
                     [f"{int((out[y]['q'][v] > 0).sum()):,}" if y in out else "" for y in ys]))
    if absorb:
        rows.append(("Families (FE groups, 2+ children)", [f"{out[y]['groups']:,}" if y in out else "" for y in ys]))
    if counts:
        for lab, fn in counts:
            rows.append((lab, [f"{fn(out[y]['q']):,}" if y in out else "" for y in ys]))
    rows.append(("Clusters (fam68)", [f"{out[y]['clusters']:,}" if y in out else "" for y in ys]))
    return rows, out


# ---------------------------------------------------------------- helpers on the panels
def lk(s, pid, year):
    return fd.lookup(s, pid, year)


def pick(s, pid, d, offs, positive=True):
    """First available value of s at d + off over offs; returns value, offset used."""
    val = np.full(len(d), np.nan)
    off = np.full(len(d), np.nan)
    for o in offs:
        v = lk(s, pid, d + o)
        if positive:
            v = np.where(v > 0, v, np.nan)
        t = np.isnan(val) & ~np.isnan(v)
        val[t], off[t] = v[t], o
    return val, off


def growth(s, pid, d):
    v1, o1 = pick(s, pid, d, [-1, -2])
    v0, o0 = pick(s, pid, d, [-4, -5])
    return 3 * (np.log(v1) - np.log(v0)) / (o1 - o0)


def nanmean_cols(s, pid, d, offs, positive=False):
    A = np.column_stack([lk(s, pid, d + o) for o in offs])
    if positive:
        A = np.where(A > 0, A, np.nan)
    return np.nanmean(A, axis=1)


# ---------------------------------------------------------------- main
def main():
    OUT.mkdir(exist_ok=True)
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    fam = psid9.family()
    disp = pd.read_pickle(DATA / "psid_displacement.pkl")
    m = fd.men_panel(py, fam)
    fx = fam_extra()
    m = m.merge(fx, on=["wave", "int"], how="left").drop_duplicates(["pid", "year"]).reset_index(drop=True)
    mi = m.set_index(["pid", "year"])
    kx = pd.read_pickle(DATA / "psid_child_exposure.pkl")
    pk = pd.read_pickle(DATA / "psid_kids.pkl")
    cds = pd.read_pickle(DATA / "cds_scores.pkl")
    ind = psid9.individual()[0]
    K, ff, inc = fd.child_frame(py, m, kx, pk, ind)
    hw = py[(py["head"] & (py["female"] == 1)) | py["wife"]][["pid", "wave", "int", "head"]]
    hw = hw.merge(fam[["wave", "int", "hh", "wh"]], on=["wave", "int"], how="left")
    hw["hrs"] = np.where(hw["head"], hw["hh"], hw["wh"])
    H = hw.assign(year=hw["wave"] - 1).dropna(subset=["hrs"]).drop_duplicates(["pid", "year"]).set_index(
        ["pid", "year"])["hrs"]
    educ = ind.set_index("pid")["educ"]
    events = {k: disp.loc[disp[k] == 1, ["pid", "year"]] for k in ("main", "strict")}
    adult = pk[["pid", "log_earn", "log_fam"]].merge(K[["pid", "birth_year"]], on="pid")
    coh = adult["birth_year"] // 5
    for v, r in (("log_earn", "rank_earn"), ("log_fam", "rank_fam")):
        adult[r] = adult.groupby(coh)[v].rank(pct=True) * 100
    adult = adult.drop(columns="birth_year")
    test = cds[cds["age"].between(3, 17)][["pid", "wave"]].rename(columns={"wave": "tyear"}).drop_duplicates()
    AY, CY = fd.AY, fd.CY
    ui_file = DATA / "ui_generosity.csv"
    print("data ready", flush=True)

    def finish(b, cdsmode):
        """19's build() tail + the pre-event and post-event variables used here."""
        b = fd.measures(b, m, inc, H)
        b = b.merge(K[["pid", "female", "race", "fam68", "educ_self"]], on="pid", how="left")
        pe = np.fmax(educ.reindex(b["f0"]).to_numpy(), educ.reindex(b["mom"].fillna(-1)).to_numpy())
        b["pe"] = fd.ecat(pd.Series(pe)).to_numpy()
        b["pe_years"] = pe
        b["black"] = (b["race"] == "Black").astype(float)
        b["female"] = b["female"].astype(float)
        f0, d = b["f0"].to_numpy(), b["d"].to_numpy()
        b["g_fam"] = growth(mi["faminc"], f0, d)
        b["g_lab"] = growth(mi["hlab"], f0, d)
        b["llab2"] = np.log(nanmean_cols(mi["hlab"], f0, d, [-2, -3], positive=True))
        b["fage"] = pick(mi["age"], f0, d, [-1, -2])[0]
        b["occg"] = np.nan_to_num(pick(mi["occg"], f0, d, [-1, -2, -3, -4])[0], nan=0.0)
        b["indg"] = np.nan_to_num(pick(mi["indg"], f0, d, [-1, -2, -3, -4])[0], nan=0.0)
        b["whitecollar"] = b["occg"].isin([1, 2, 3]).astype(float).where(b["occg"] > 0)
        b["manuf"] = b["indg"].isin([3, 4]).astype(float).where(b["indg"] > 0)
        b["fips"] = pick(mi["fips"], f0, d, [-1, -2, 0])[0]
        pre = nanmean_cols(mi["hlab"], f0, d, [-3, -2])
        post = nanmean_cols(mi["hlab"], f0, d, [1, 2, 3])
        b["rel_loss"] = np.where(pre > 0, post / pre - 1, np.nan)
        for v, src in (("ui_post", "ui_amt"), ("fs_post", "fs")):
            A = np.column_stack([lk(mi[src], f0, d + o) for o in (0, 1)])
            A = np.where(np.isnan(A), np.nan, (A > 0).astype(float))
            b[v] = np.nanmax(A, axis=1)
        if cdsmode:
            b = b.merge(cds[["pid", "wave", "lw", "ap", "pc", "bpi_z"]].rename(columns={"wave": "tyear"}),
                        on=["pid", "tyear"])
        else:
            b = b.merge(adult, on="pid", how="left")
            b["educ_self"] = b["educ_self"].where(b["birth_year"] <= 1995)
        return b[b["race"].isin(["Black", "White"])].copy()

    def build(kind, lo, hi, cdsmode=False):
        tst = test if cdsmode else None
        key = ["pid", "tyear"] if cdsmode else ["pid"]
        if kind == "main":
            b, a = fd.design(K, ff, events["main"], lo, hi, test=tst)
        else:                                                         # closure-first
            b, a = fd.design(K, ff, events["strict"], lo, hi, test=tst)
            bm, _ = fd.design(K, ff, events["main"], 0, 17, test=tst)
            fm = bm.loc[bm["treat"] == 1, key + ["d"]].rename(columns={"d": "d_main"})
            b = b.merge(fm, on=key, how="left")
            b = b[((b["treat"] == 1) & (b["d_main"] == b["d"])) | ((b["treat"] == 0) & b["d_main"].isna())]
            b = b.drop(columns="d_main")
        return finish(b, cdsmode), a

    def ctrl_of(race):
        return ["lpre", "female"] + (["black"] if race == "Pooled" else [])

    def sub(b, race):
        return b if race == "Pooled" else b[b["race"] == race]

    RACES = ("Black", "White", "Pooled")
    md = ["# Identifying the father's displacement -> children link: closures, siblings, pre-trends, severity", "",
          "Built by `22.DisplacementID.py` (2026-10-17) on top of `19.FatherDisplacement.py` (same displacement "
          "measure, children, father figures, controls and outcomes). Unweighted PSID SRC + SEO, Black and White "
          "(child's race). Cells: coefficient, stars, (s.e. clustered by 1968 family; p-value); *** p<0.01, ** p<0.05, "
          "* p<0.1. Every design below is a comparison of children whose father figure was displaced with children "
          "whose father figure was not (or not yet, or not during their childhood). None of them is an experiment; "
          "each removes one source of bias and keeps others, as noted under each table.", ""]
    store = {}

    # ================================================================ 1. closures only
    md += ["## 1. Closures only (closure-first definition)", "",
           "Treated = the father figure's first displacement during the child's childhood (CDS: before the test) is "
           "a plant closure / move and falls in the age band; children whose first displacement was a layoff / "
           "firing are dropped; controls = children never displaced (closure or layoff) at 0-17 (CDS: before the "
           "test), with a pseudo event year at the treated's median exposure age; both need a father figure who "
           "worked in the year(s) before the (pseudo) event. Controls: log family income over the 3 years before "
           "the (pseudo) event, parental education (5 groups), female, birth-year FE (+ CDS-wave FE; + Black in "
           "pooled rows). Closures are the definition least driven by the worker's own performance (Page, Stevens "
           "and Lindo 2009; Oreopoulos, Page and Stevens 2008), but who works at a plant that closes is not random "
           "either (industry, region, firm quality).", ""]
    for cdsmode, ys, sec in ((False, AY, "1a. Adult outcomes"), (True, CY, "1b. CDS test scores and behaviour")):
        panels = []
        for lo, hi in ((0, 5), (6, 11), (12, 17), (0, 17)):
            b, a = build("closure", lo, hi, cdsmode)
            store[("closure", cdsmode, lo, hi)] = b
            for race in RACES:
                rows, _ = run(sub(b, race), ys, ["treat"], ctrl_of(race), ["birth_year"] + (["tyear"] if cdsmode else []),
                              "closures", f"closure_{lo}_{hi}", race)
                panels.append((f"{race}, first closure at ages {lo}-{hi} (controls' pseudo age {a})", rows))
            print("closures", cdsmode, lo, hi, flush=True)
        md += [f"### {sec}", "", fd.md_table([LABY[y] for y in ys], panels,
                                            [("Fixed effects", ["birth year" + (", CDS wave" if cdsmode else "")] * len(ys)),
                                             ("Other controls", ["log pre-event family income, parental education, female"]
                                              * len(ys))]), ""]
    for cdsmode in (False, True):
        store[("main", cdsmode, 0, 17)] = build("main", 0, 17, cdsmode)[0]

    # ================================================================ 2. siblings
    S = K[["pid", "birth_year", "female", "race", "fam68"]].copy()
    mom = kx.set_index("pid")["mom_pid"]
    ch = py[py["child"]].sort_values(["pid", "wave"]).drop_duplicates("pid")[["pid", "wave", "int"]]
    mf = py[py["wife"] | (py["head"] & (py["female"] == 1))].drop_duplicates(["wave", "int"])[["wave", "int", "pid"]]
    ch = ch.merge(mf.rename(columns={"pid": "mf"}), on=["wave", "int"], how="left").set_index("pid")["mf"]
    S["mid"] = S["pid"].map(mom)
    S["mid_cah"] = S["mid"].notna()
    S["mid"] = S["mid"].fillna(S["pid"].map(ch))
    S = S.dropna(subset=["mid"]).sort_values(["mid", "birth_year", "pid"])
    S["bo"] = S.groupby("mid").cumcount() + 1
    fb = ff.sort_values(["pid", "year", "pri"]).drop_duplicates("pid").set_index("pid")["f"]
    S["fb"] = S["pid"].map(fb)
    S = S.dropna(subset=["fb"])
    S["fb"] = S["fb"].astype(np.int64)
    evm = disp[disp["main"] == 1].sort_values(["pid", "year"]).drop_duplicates("pid").set_index("pid")
    S["D"] = S["fb"].map(evm["year"])
    S["Ds"] = S["fb"].map(evm["strict"])
    S["a"] = S["D"] - S["birth_year"]
    co = set(zip(ff["pid"], ff["year"], ff["f"]))
    S["co"] = [(p, int(dd), f) in co if dd == dd else False for p, dd, f in zip(S["pid"], S["D"], S["fb"])]
    x = ff.merge(K[["pid", "birth_year"]], on="pid")
    x["age"] = x["year"] - x["birth_year"]
    e1 = x[x["age"].between(0, 17)].merge(events["main"].rename(columns={"pid": "f"}), on=["f", "year"])
    e1 = e1.sort_values(["pid", "year", "pri"]).drop_duplicates("pid").set_index("pid")
    S["a1"] = S["pid"].map(e1["age"])
    S["f1"] = S["pid"].map(e1["f"])
    # share of the observed childhood years before D (all childhood if D is missing) lived with fb
    f1d = ff.drop_duplicates(["pid", "year"])[["pid", "year", "f"]].merge(S[["pid", "birth_year", "fb", "D"]], on="pid")
    f1d = f1d[(f1d["year"] - f1d["birth_year"]).between(0, 17) & ((f1d["year"] < f1d["D"]) | f1d["D"].isna())]
    S["pre_share"] = S["pid"].map((f1d["f"] == f1d["fb"]).groupby(f1d["pid"]).mean())
    pre_ok = S["pre_share"].isna() | (S["pre_share"] >= 0.8)
    a, a1 = S["a"], S["a1"]
    exp_ok = a.between(0, 17) & S["co"] & pre_ok & (a1.isna() | ((a1 == a) & (S["f1"] == S["fb"])))
    cat = np.select([exp_ok, a.between(0, 17),
                     (a >= 18) & a1.isna() & pre_ok, (a >= 18),
                     (a < 0),
                     a.isna() & a1.isna()],
                    ["exp", "drop", "older", "drop", "later", "never"], "drop")
    S["cat"] = cat
    S = S[S["cat"] != "drop"].copy()
    S["exp"] = (S["cat"] == "exp").astype(float)
    S["exp05"] = ((S["exp"] == 1) & S["a"].between(0, 5)).astype(float)
    S["exp611"] = ((S["exp"] == 1) & S["a"].between(6, 11)).astype(float)
    S["exp1217"] = ((S["exp"] == 1) & S["a"].between(12, 17)).astype(float)
    S["later"] = (S["cat"] == "later").astype(float)
    S["never"] = (S["cat"] == "never").astype(float)
    S["dur"] = np.where(S["exp"] == 1, 18 - S["a"], 0.0)
    S["bo2"] = (S["bo"] == 2).astype(float)
    S["bo3p"] = (S["bo"] >= 3).astype(float)
    S["female"] = S["female"].astype(float)
    S["par"] = pd.factorize(S["mid"].astype(np.int64).astype(str) + "_" + S["fb"].astype(str))[0]
    S["mid"] = S["mid"].astype(np.int64)
    S["catn"] = S["cat"].map({"exp": 1, "older": 2, "never": 3, "later": 4})
    S["band"] = np.select([S["exp05"] == 1, S["exp611"] == 1, S["exp1217"] == 1], [1, 2, 3], 0)
    S = S.merge(adult, on="pid", how="left").merge(K[["pid", "educ_self"]], on="pid", how="left")
    S["educ_self"] = S["educ_self"].where(S["birth_year"] <= 1995)
    S = S[S["race"].isin(["Black", "White"])].copy()
    S["black"] = (S["race"] == "Black").astype(float)

    def nfam(q, g, cond_a, cond_b):
        t = q.assign(A=cond_a(q), B=cond_b(q)).groupby(g)[["A", "B"]].max()
        return int(((t["A"] > 0) & (t["B"] > 0)).sum())

    CNT = {"older": ("Families with an exposed and an older sibling (a >= 18)",
                     lambda g: lambda q: nfam(q, g, lambda z: z["catn"] == 1, lambda z: z["catn"] == 2)),
           "later": ("Families with an exposed and a later-born sibling",
                     lambda g: lambda q: nfam(q, g, lambda z: z["catn"] == 1, lambda z: z["catn"] == 4)),
           "never": ("Families with an exposed and a never-displaced (half-)sibling",
                     lambda g: lambda q: nfam(q, g, lambda z: z["catn"] == 1, lambda z: z["catn"] == 3)),
           "bands": ("Families with siblings exposed in different age bands",
                     lambda g: lambda q: int((q[q["band"] > 0].groupby(g)["band"].nunique() > 1).sum()))}

    def counts_for(g, keys=("older", "later", "never", "bands")):
        return [(CNT[k][0], CNT[k][1](g)) for k in keys]

    SY = ["log_earn", "log_fam", "rank_earn", "rank_fam", "educ_self"]
    SCTRL = ["female", "bo2", "bo3p", "never"]
    md += ["## 2. Sibling design (mother fixed effects)", "",
           "Family = mother (CAH mother; for children born 1951-67, the wife / female head of the unit where the child "
           "is first seen as a child). Father figure at birth (fb) = the earliest father figure observed; D = his "
           "first displacement, closure or layoff (observed from 1967; earlier ones are unobserved, so for the "
           "1951-67 cohorts D may be a second displacement); a = D - birth year. Categories: exposed = 0 <= a <= 17 "
           "and living with fb in D; older sibling = a >= 18 (the reference group); later-born = a < 0 (born after "
           "the displacement; whatever happens later); never = fb never displaced (a half-sibling under mother FE; "
           "own dummy, shown). Exposed and older siblings must have lived with fb in >= 80% of their observed "
           "childhood years before D, so that both groups grew up with the same father figure up to the event (only "
           "children living with a father figure can be 'exposed'). Children whose own "
           "childhood exposure comes from another father figure, or precedes fb's first displacement, are dropped. "
           "OLS with mother FE (absorbed, singletons dropped), birth-year FE, female, birth order (2, 3+). The "
           "comparison removes what siblings share (the mother, the household's permanent traits, the father's type "
           "when he is common). It does not remove differences tied to birth order and cohort within the family "
           "(age at the event and the older / later-born status are functions of birth year given D): older "
           "siblings (born 18+ years before the father's first displacement) are the mother's earliest births, and "
           "every younger group (exposed and later-born alike) has more schooling than they do, which points to a "
           "within-family birth-order / cohort gradient rather than an effect of displacement. The exposed vs "
           "later-born contrast (both younger) is the less contaminated one, but later-born children grow up with "
           "the father's permanent earnings loss, so it identifies the effect of experiencing the job loss during "
           "childhood relative to being born after it, not the level effect. An older sibling can also be affected "
           "through the family (e.g. less help with college).", ""]
    for absorb, flab in (("mid", "Mother FE"), ("par", "Parents FE (mother x father figure at birth)")):
        panels = []
        for race in RACES:
            q = sub(S, race)
            ctrl = SCTRL + (["black"] if race == "Pooled" else [])
            shw = ["exp", "later"] + (["never"] if absorb == "mid" else [])
            rows, _ = run(q, SY, ["exp", "later"], ctrl, ["birth_year"], "siblings", f"{absorb}_any", race,
                          absorb=absorb, pe=False, extra=["catn", "band"], tests=[("exp", "later")], show=shw,
                          counts=counts_for(absorb))
            panels.append((f"{race}: exposed at 0-17 vs older siblings", rows))
            rows, _ = run(q, SY, ["exp05", "exp611", "exp1217", "later"], ctrl, ["birth_year"], "siblings",
                          f"{absorb}_bands", race, absorb=absorb, pe=False, extra=["catn", "band"],
                          tests=[("exp05", "exp1217")], counts=counts_for(absorb, ("bands",)))
            panels.append((f"{race}: by age at the displacement", rows))
            if absorb == "mid":
                rows, _ = run(q, SY, ["exp", "dur", "later"], ctrl, ["birth_year"], "siblings", f"{absorb}_duration",
                              race, absorb=absorb, pe=False, extra=["catn", "band"])
                panels.append((f"{race}: exposure duration", rows))
                ql = q[q["cat"].isin(["exp", "later"])]
                rows, _ = run(ql, SY, ["exp"], SCTRL[:3] + (["black"] if race == "Pooled" else []), ["birth_year"],
                              "siblings", f"{absorb}_laterborn", race, absorb=absorb, pe=False,
                              extra=["catn", "band"], counts=counts_for(absorb, ("later",)))
                panels.append((f"{race}: later-born siblings as controls (exposed vs later-born only)", rows))
            print("siblings", absorb, race, flush=True)
        md += [f"### 2{'a' if absorb == 'mid' else 'b'}. {flab}", "",
               fd.md_table([LABY[y] for y in SY], panels,
                           [("Fixed effects", [f"{flab.split(' (')[0].lower()}, birth year"] * len(SY)),
                            ("Other controls", ["female, birth order (2, 3+), never-displaced dummy; Black in pooled "
                                                "rows"] * len(SY))]),
               ""]
    # closures within families
    Sc = S[(S["cat"] == "never") | (S["Ds"] == 1)]
    panels = []
    for race in RACES:
        q = sub(Sc, race)
        ctrl = SCTRL + (["black"] if race == "Pooled" else [])
        rows, _ = run(q, SY, ["exp", "later"], ctrl, ["birth_year"], "siblings", "mid_closure", race, absorb="mid",
                      pe=False, extra=["catn", "band"], tests=[("exp", "later")], show=["exp", "later", "never"],
                      counts=counts_for("mid"))
        panels.append((f"{race}: father's first displacement a closure (vs older siblings)", rows))
    md += ["### 2c. Mother FE, closures only", "",
           "Families whose father figure's first displacement is a closure / move, plus families whose father figure "
           "was never displaced (families with a first layoff are dropped).", "",
           fd.md_table([LABY[y] for y in SY], panels,
                       [("Fixed effects", ["mother, birth year"] * len(SY)),
                        ("Other controls", ["female, birth order (2, 3+), never-displaced dummy; Black in pooled rows"]
                         * len(SY))]), ""]
    # sibling sample summary
    rows = []
    for race in ("Black", "White"):
        for y in ("log_earn", "educ_self"):
            q = S[(S["race"] == race) & S[y].notna()]
            q = q[q.groupby("mid")["pid"].transform("size") > 1]
            rows.append((f"{race}, {LABY[y]} sample", [
                f"{len(q):,}", f"{q['mid'].nunique():,}", f"{int(q['exp'].sum()):,}"]
                + [f"{CNT[k][1]('mid')(q):,}" for k in ("older", "later", "never", "bands")]
                + [f"{q['mid_cah'].mean():.2f}"]))
    md += ["### 2d. Sibling samples (mother FE, families with 2+ children with the outcome)", "",
           fd.md_table(["Children", "Families", "Exposed children", "Fam.: exposed + older (a >= 18)",
                        "Fam.: exposed + later-born", "Fam.: exposed + never-displaced half-sibling",
                        "Fam.: exposed in different bands", "Share mother from CAH"], [("", rows)]), ""]

    # ================================================================ 3a. future displacement placebo
    evd = disp[disp["main"] == 1][["pid", "year", "strict"]]
    e1s = x[x["age"].between(0, 17)].merge(evd.rename(columns={"pid": "f"}), on=["f", "year"])
    e1s = e1s.sort_values(["pid", "year", "pri"]).drop_duplicates("pid")[["pid", "age", "strict"]]
    e1s = e1s.rename(columns={"age": "a1", "strict": "s1"})
    last = x[x["age"].between(12, 17)].sort_values(["pid", "year", "pri"], ascending=[True, True, False])
    last = last.drop_duplicates("pid", keep="last")[["pid", "f", "year"]].rename(columns={"f": "fl", "year": "yl"})
    P = K[["pid", "birth_year", "female", "race", "fam68"]].merge(last, on="pid").merge(e1s, on="pid", how="left")
    P = P[P["birth_year"].between(1956, 1997)].copy()
    fe_ = evd.rename(columns={"pid": "fl"}).merge(P[["pid", "fl", "birth_year"]], on="fl")
    fe_["age"] = fe_["year"] - fe_["birth_year"]
    fe_ = fe_[fe_["age"].between(18, 25)].sort_values(["pid", "year"])
    f18 = fe_.drop_duplicates("pid").set_index("pid")
    P["af"] = P["pid"].map(f18["age"])
    P["sf"] = P["pid"].map(f18["strict"])
    P["ev1821"] = P["pid"].isin(fe_.loc[fe_["age"] <= 21, "pid"])
    obs = m[["pid", "year", "hh"]].rename(columns={"pid": "fl"}).merge(P[["pid", "fl", "birth_year"]], on="fl")
    obs["age"] = obs["year"] - obs["birth_year"]
    P["nobs1825"] = P["pid"].map(obs[obs["age"].between(18, 25)].groupby("pid").size()).fillna(0)
    P["nobs2225"] = P["pid"].map(obs[obs["age"].between(22, 25)].groupby("pid").size()).fillna(0)
    P["worked"] = P["pid"].isin(obs.loc[obs["age"].between(12, 14) & (obs["hh"] > 0), "pid"])
    by = P["birth_year"].to_numpy()
    with np.errstate(all="ignore"):
        P["lpre"] = np.log(nanmean_cols(inc, P["pid"].to_numpy(), by, [9, 10, 11, 12], positive=True))
    wl = lk(mi["w_pid"], P["fl"].to_numpy(), P["yl"].to_numpy())
    pe = np.fmax(educ.reindex(P["fl"]).to_numpy(), educ.reindex(pd.Series(wl).fillna(-1)).to_numpy())
    P["pe"] = fd.ecat(pd.Series(pe)).to_numpy()
    P = P[P["worked"] & (P["nobs1825"] >= 2) & P["race"].isin(["Black", "White"])].copy()
    P = P.merge(adult, on="pid", how="left").merge(K[["pid", "educ_self"]], on="pid", how="left")
    P["educ_self"] = P["educ_self"].where(P["birth_year"] <= 1995)
    P["black"] = (P["race"] == "Black").astype(float)
    P["female"] = P["female"].astype(float)
    un = P["a1"].isna()
    variants = {
        "main_1825": (P[~P["a1"].between(0, 11)].assign(A=P["a1"].between(12, 17).astype(float),
                                                         F=(un & P["af"].notna()).astype(float)), ["A", "F"]),
        "main_2225": (P[~P["a1"].between(0, 11) & ~(un & P["ev1821"]) & (P["nobs2225"] >= 1)].assign(
            A=P["a1"].between(12, 17).astype(float), F22=(un & P["af"].between(22, 25)).astype(float)), ["A", "F22"]),
        "closure_1825": (P[~P["a1"].between(0, 11) & ~(P["a1"].between(12, 17) & (P["s1"] == 0))
                           & ~(un & (P["sf"] == 0))].assign(A=(P["a1"].between(12, 17) & (P["s1"] == 1)).astype(float),
                                                            F=(un & (P["sf"] == 1)).astype(float)), ["A", "F"])}
    vlab = {"main_1825": "closure or layoff, after-childhood window 18-25",
            "main_2225": "closure or layoff, after-childhood window 22-25 (children displaced at 18-21 dropped)",
            "closure_1825": "closures only (first displacement in the window a closure), window 18-25"}
    panels = []
    for vk, (q0, xs) in variants.items():
        for race in RACES:
            rows, _ = run(sub(q0, race), AY, xs, ctrl_of(race), ["birth_year"], "placebo_future", vk, race,
                          tests=[(xs[0], xs[1])])
            panels.append((f"{race}: {vlab[vk]}", rows))
        print("placebo", vk, flush=True)
    md += ["## 3. Pre-trends and selection", "",
           "### 3a. Future displacement: does a displacement after childhood 'predict' the child's outcomes?", "",
           "Children born 1956-1997 with a father figure at 12-17 (the last one observed) who worked at child age "
           "12-14 and is observed in 2+ years when the child is 18-25. Groups: first displaced at 12-17 "
           "(childhood); never displaced at 0-17 but the father figure displaced when the child is 18-25 (after "
           "childhood); neither (reference). Children first displaced at 0-11 are dropped. Controls: log family "
           "income at ages 9-12, parental education, female, birth-year FE (+ Black). A displacement after "
           "childhood can still matter (college funding, a later transfer), so the 22-25 window is shown too; if "
           "the after-childhood coefficient is as large as the childhood one, the childhood association is "
           "likely selection on family traits.", "",
           fd.md_table([LABY[y] for y in AY], panels,
                       [("Fixed effects", ["birth year"] * len(AY)),
                        ("Other controls", ["log family income at 9-12, parental education, female"] * len(AY))]), ""]

    # CDS lead placebo
    T = test.merge(K[["pid", "birth_year", "female", "race", "fam68"]], on="pid")
    f1 = ff.drop_duplicates(["pid", "year"]).set_index(["pid", "year"])["f"]
    T["ft"] = lk(f1, T["pid"], T["tyear"])
    T["ft"] = T["ft"].fillna(pd.Series(lk(f1, T["pid"], T["tyear"] - 1), index=T.index))
    T = T.dropna(subset=["ft"])
    T["ft"] = T["ft"].astype(np.int64)
    eb = x.merge(evd.rename(columns={"pid": "f"}), on=["f", "year"]).merge(T[["pid", "tyear"]], on="pid")
    eb = eb[(eb["year"] < eb["tyear"]) & (eb["age"] >= 0)].sort_values(["pid", "tyear", "year", "pri"])
    eb = eb.drop_duplicates(["pid", "tyear"])[["pid", "tyear", "strict"]].rename(columns={"strict": "sb"})
    T = T.merge(eb, on=["pid", "tyear"], how="left")
    T["eb"] = T["sb"].notna()
    el = evd.rename(columns={"pid": "ft"}).merge(T[["pid", "tyear", "ft"]], on="ft")
    el = el[(el["year"] >= el["tyear"] + 1) & (el["year"] <= el["tyear"] + 4)].sort_values(["pid", "tyear", "year"])
    el = el.drop_duplicates(["pid", "tyear"])[["pid", "tyear", "strict"]].rename(columns={"strict": "sl"})
    T = T.merge(el, on=["pid", "tyear"], how="left")
    ob = m[["pid", "year", "hh"]].rename(columns={"pid": "ft"}).merge(T[["pid", "tyear", "ft"]], on="ft")
    nob = ob[(ob["year"] >= ob["tyear"] + 1) & (ob["year"] <= ob["tyear"] + 4)].groupby(["pid", "tyear"]).size()
    T["nobs"] = pd.Series(nob.reindex(pd.MultiIndex.from_frame(T[["pid", "tyear"]])).to_numpy()).fillna(0).to_numpy()
    h1 = lk(mi["hh"], T["ft"], T["tyear"] - 1)
    h2 = lk(mi["hh"], T["ft"], T["tyear"] - 2)
    T["worked"] = np.where(np.isnan(h1), h2, h1) > 0
    with np.errstate(all="ignore"):
        T["lpre"] = np.log(nanmean_cols(inc, T["pid"].to_numpy(), T["tyear"].to_numpy(), [-1, -2, -3], positive=True))
    wt = pick(mi["w_pid"], T["ft"].to_numpy(), T["tyear"].to_numpy(), [-1, -2], positive=False)[0]
    pe = np.fmax(educ.reindex(T["ft"]).to_numpy(), educ.reindex(pd.Series(wt).fillna(-1)).to_numpy())
    T["pe"] = fd.ecat(pd.Series(pe)).to_numpy()
    T = T[T["worked"] & (T["nobs"] >= 2) & T["race"].isin(["Black", "White"])].copy()
    T = T.merge(cds[["pid", "wave", "lw", "ap", "pc", "bpi_z"]].rename(columns={"wave": "tyear"}), on=["pid", "tyear"])
    T["black"] = (T["race"] == "Black").astype(float)
    T["female"] = T["female"].astype(float)
    T["Bf"] = T["eb"].astype(float)
    T["L"] = (~T["eb"] & T["sl"].notna()).astype(float)
    Tc = T[~(T["eb"] & (T["sb"] == 0)) & ~(~T["eb"] & (T["sl"] == 0))].copy()
    Tc["Bf"] = (Tc["eb"] & (Tc["sb"] == 1)).astype(float)
    Tc["L"] = (~Tc["eb"] & (Tc["sl"] == 1)).astype(float)
    panels = []
    for vk, q0 in (("main", T), ("closure", Tc)):
        for race in RACES:
            rows, _ = run(sub(q0, race), CY, ["Bf", "L"], ctrl_of(race), ["birth_year", "tyear"], "placebo_lead",
                          vk, race, tests=[("Bf", "L")])
            panels.append((f"{race}: {'closure or layoff' if vk == 'main' else 'closures only'}", rows))
    md += ["### 3b. CDS: displacement after the test (lead) vs before", "",
           "CDS child-tests at 3-17 whose father figure at the test worked in the year(s) before it and is observed "
           "in 2+ years of test year + 1..+4. Before = first displaced before the test year; lead = not displaced "
           "before the test, father figure displaced in test year + 1..+4; reference = neither. Controls: log family "
           "income over the 3 years before the test, parental education, female, birth-year and CDS-wave FE "
           "(+ Black). A lead 'effect' as large as the 'before' coefficient points to selection; a lead "
           "coefficient can also pick up anticipation (a declining firm).", "",
           fd.md_table([LABY[y] for y in CY], panels,
                       [("Fixed effects", ["birth year, CDS wave"] * len(CY)),
                        ("Other controls", ["log family income 3 yrs before the test, parental education, female"]
                         * len(CY))]), ""]

    # ================================================================ 3c. balance
    BAL = [("lpre", "Log pre-event family income"), ("pe_years", "Parental education (years)"),
           ("g_fam", "Family-income growth, 3 yrs before"), ("g_lab", "Father's labor-income growth, 3 yrs before"),
           ("llab2", "Log father's labor income, d-2/d-3"), ("mom_emp_pre", "Mother figure employed year before"),
           ("fage", "Father's age"), ("whitecollar", "Father white-collar (occupation)"),
           ("manuf", "Father in manufacturing")]
    panels = []
    for (kind, cdsmode), klab in ((("main", False), "closure or layoff, adult-outcome sample"),
                                  (("closure", False), "closures only, adult-outcome sample"),
                                  (("main", True), "closure or layoff, CDS sample")):
        b = store[(kind, cdsmode, 0, 17)]
        if not cdsmode:
            b = b[b["log_earn"].notna() | b["educ_self"].notna()]
        for race in RACES:
            q = sub(b, race)
            ys = [v for v, _ in BAL]
            rows, out = run(q, ys, ["treat"], ["black"] if race == "Pooled" else [],
                            ["birth_year"] + (["tyear"] if cdsmode else []), "balance", f"{kind}_{'cds' if cdsmode else 'adult'}",
                            race, pe=False)
            cm = [f"{q.loc[q['treat'] == 0, v].mean():.3f}" for v in ys]
            panels.append((f"{race}: {klab}", rows[:1] + [("Mean among controls", cm)] + rows[2:]))
    md += ["### 3c. Balance: pre-event characteristics of displaced vs control children", "",
           "Each column regresses a pre-event characteristic on 'displaced' with birth-year FE (+ CDS-wave FE; + Black "
           "in pooled rows), in the 0-17 exposure designs of Section 1 / 19 (adult sample: children with log earnings "
           "or schooling). Growth = log change from the earliest of d-4/d-5 to the latest of d-1/d-2, scaled to 3 "
           "years (d = the (pseudo) event year). The family-income and labor-income growth columns are the "
           "pre-trend test of the father's trajectory: d-1 contains part of the Jacobson-LaLonde-Sullivan dip (and "
           "dating error), so a negative growth gap partly reflects the displacement itself.", "",
           fd.md_table([lab for _, lab in BAL], panels,
                       [("Fixed effects", ["birth year (+ CDS wave)"] * len(BAL))]), ""]

    # ================================================================ 3d. trajectory + occupation / industry controls
    TRJ = ["g_fam", "g_lab", "llab2"]
    panels = []
    for kind in ("main", "closure"):
        b = store[(kind, False, 0, 17)]
        for race in RACES:
            q = sub(b, race)
            base = ctrl_of(race)
            for spec, ctrl, fe in (("baseline", base, ["birth_year"]),
                                   ("+ pre-trend", base + TRJ, ["birth_year"]),
                                   ("+ pre-trend + occupation / industry", base + TRJ, ["birth_year", "occg", "indg"])):
                rows, _ = run(q, AY, ["treat"], ctrl, fe, "trajectory", f"{kind}_{spec}", race, extra=TRJ,
                              show=["treat"] + (TRJ if spec != "baseline" else []))
                panels.append((f"{race}, {'closure or layoff' if kind == 'main' else 'closures only'}: {spec}", rows))
        print("trajectory", kind, flush=True)
    md += ["### 3d. Controlling for the father's pre-displacement trajectory, occupation and industry", "",
           "Exposure at 0-17 (Section 1 / 19 designs); the same sample in the three rows of a panel (children with "
           "the trajectory variables observed). Baseline = 19's controls; + pre-trend = the father's family-income "
           "and labor-income growth over the 3 years before and his log labor income at d-2/d-3; + occupation / "
           "industry = 8 occupation and 10 industry groups of his job in the latest interview in d-3..d (missing = "
           "own group). Codes: 1970 Census (1968-2001), 2000 Census (2003-15), 2010 / 2012 Census (2017-23).", "",
           fd.md_table([LABY[y] for y in AY], panels,
                       [("Fixed effects", ["birth year (+ occupation and industry groups in the third row)"] * len(AY)),
                        ("Other controls", ["log pre-event family income, parental education, female"] * len(AY))]),
           ""]

    # ================================================================ 4. severity
    panels = []
    sev_info = []
    for cdsmode, ys in ((False, AY), (True, CY)):
        b = store[("main", cdsmode, 0, 17)].copy()
        t = b["treat"] == 1
        med = b.loc[t, "rel_loss"].median()
        sev_info.append((cdsmode, med, b.loc[t].groupby("race")["rel_loss"].median().to_dict(),
                         b.loc[t].groupby("race")["ui_post"].mean().to_dict(),
                         b.loc[t].groupby("race")["fs_post"].mean().to_dict()))
        splits = {"loss": ("t_hi", "t_lo", b["rel_loss"] < med, b["rel_loss"].notna()),
                  "ui": ("t_ui1", "t_ui0", b["ui_post"] == 1, b["ui_post"].notna()),
                  "fs": ("t_fs1", "t_fs0", b["fs_post"] == 1, b["fs_post"].notna())}
        for sk, (h, l, hi, ok) in splits.items():
            q0 = b[(~t) | ok].copy()
            q0[h] = (t & hi).reindex(q0.index).astype(float)
            q0[l] = (t & ~hi).reindex(q0.index).astype(float)
            for race in RACES:
                rows, _ = run(sub(q0, race), ys, [h, l], ctrl_of(race), ["birth_year"] + (["tyear"] if cdsmode else []),
                              "severity", f"{sk}_{'cds' if cdsmode else 'adult'}", race, tests=[(h, l)])
                panels.append(((cdsmode, f"{race}: split by {dict(loss='relative earnings loss', ui='UI receipt', fs='food-stamp receipt')[sk]}"), rows))
        print("severity", cdsmode, flush=True)
    md += ["## 4. Severity: dose-response and receipt of UI / food stamps", "",
           "Exposure at 0-17, closure or layoff (19's design). Relative earnings loss = father's mean labor income "
           "over d+1..d+3 divided by his mean over d-3..d-2, minus 1 (zeros kept; the event-study reference window); "
           "'above median' = a larger loss than the median among the treated of the sample (pooled across race). "
           "Receipt = the head's unemployment compensation > 0 (before 1977 the item includes workers' compensation "
           "and, 1970-74, other family members; no item for calendar 1967-68, 1972, 1974) / the family's food stamps "
           "in d or d+1. Treated children with the split variable missing are dropped. Receipt is chosen by the "
           "family and reflects eligibility, so the receipt splits describe who is hurt; they do not identify the "
           "effect of the transfer.", ""]
    for cdsmode, med, medr, uir, fsr in sev_info:
        md.append(f"- {'CDS' if cdsmode else 'Adult-outcome'} sample: median relative loss among the treated "
                  f"{med:.3f} (Black {medr.get('Black', np.nan):.3f}, White {medr.get('White', np.nan):.3f}); "
                  f"share receiving UI Black {uir.get('Black', np.nan):.3f}, White {uir.get('White', np.nan):.3f}; "
                  f"food stamps Black {fsr.get('Black', np.nan):.3f}, White {fsr.get('White', np.nan):.3f}.")
    md.append("")
    for cdsmode, ys, sec in ((False, AY, "4a. Adult outcomes"), (True, CY, "4b. CDS")):
        md += [f"### {sec}", "", fd.md_table([LABY[y] for y in ys], [(t, r) for (c, t), r in panels if c == cdsmode],
                                            [("Fixed effects", ["birth year" + (", CDS wave" if cdsmode else "")] * len(ys)),
                                             ("Other controls", ["log pre-event family income, parental education, "
                                                                 "female"] * len(ys))]), ""]

    # ================================================================ 5. UI generosity
    md += ["## 5. Safety-net buffering: exposure x UI generosity", ""]
    if ui_file.exists():
        ui = pd.read_csv(ui_file)
        key_f = next(c for c in ui.columns if c.lower() in ("fips", "state_fips", "statefip", "stfips"))
        cand = [c for c in ui.columns if re.fullmatch(r"repl_rate", c)] + \
               [c for c in ui.columns if re.search(r"max_wba.*(2000|real|_r$)", c)] + \
               [c for c in ui.columns if c == "max_wba"]
        meas = list(dict.fromkeys(cand))[:2]
        panels = []
        for mv in meas:
            u = ui[[key_f, "year", mv]].rename(columns={key_f: "fips", "year": "d"}).dropna()
            u["ui_z"] = (u[mv] - u[mv].mean()) / u[mv].std()
            for kind, cdsmode, ys in (("main", False, AY), ("closure", False, AY), ("main", True, CY)):
                b = store[(kind, cdsmode, 0, 17)]
                b = b.merge(u[["fips", "d", "ui_z"]], on=["fips", "d"], how="left")
                b["t_x_ui"] = b["treat"] * b["ui_z"]
                for race in RACES:
                    for sfe in (False, True):
                        fe = ["birth_year"] + (["tyear"] if cdsmode else []) + (["fips"] if sfe else [])
                        rows, _ = run(sub(b, race), ys, ["treat", "t_x_ui", "ui_z"], ctrl_of(race), fe, "ui_generosity",
                                      f"{mv}_{kind}_{'cds' if cdsmode else 'adult'}_{'stateFE' if sfe else 'noFE'}",
                                      race)
                        panels.append(((mv, kind, cdsmode), f"{race}{', state FE' if sfe else ''}", rows))
        for mv in meas:
            for kind, cdsmode, ys in (("main", False, AY), ("closure", False, AY), ("main", True, CY)):
                md += [f"### UI measure `{mv}`, {'closure or layoff' if kind == 'main' else 'closures only'}, "
                       f"{'CDS' if cdsmode else 'adult outcomes'}", "",
                       fd.md_table([LABY[y] for y in ys], [(t, r) for k, t, r in panels if k == (mv, kind, cdsmode)],
                                   [("Fixed effects", ["birth year (+ CDS wave) (+ state)"] * len(ys))]), ""]
        md.insert(md.index("## 5. Safety-net buffering: exposure x UI generosity") + 2,
                  f"UI generosity from `data/ui_generosity.csv` (measures: {', '.join(meas)}), z-scored over the "
                  "state-year panel, in the state of the father's family at the (pseudo) event year d (interview in d "
                  "or d-1, else d+1) and year d; events from 1976 on. The interaction compares the "
                  "displaced-control gap across states and years with more or less generous UI; UI generosity is not "
                  "randomly assigned (it co-moves with state wages and politics), so the state-FE rows use only "
                  "within-state changes.\n")
    else:
        md += ["**Pending.** `data/ui_generosity.csv` did not exist when this script ran (another agent is building "
               "it with `12b.UIGenerosity.py`). The code in Section 5 of this script merges it by the state of the "
               "father's family at the (pseudo) event year (variables already built: `fips`, `d`) and runs exposure x "
               "UI generosity (z) with and without state FE; rerun the script once the file exists.", ""]

    # ================================================================ 6. sample sizes
    rows = []
    for (kind, cdsmode, lo, hi), b in store.items():
        if (lo, hi) != (0, 17):
            continue
        for race in ("Black", "White"):
            q = b[b["race"] == race]
            rows.append((f"{'Closure-first' if kind == 'closure' else 'Closure or layoff'}, "
                         f"{'CDS child-tests' if cdsmode else 'children'}, 0-17, {race}",
                         [f"{int(q['treat'].sum()):,}", f"{int((q['treat'] == 0).sum()):,}", f"{len(q):,}"]))
    for race in ("Black", "White"):
        q = S[S["race"] == race]
        rows.append((f"Sibling frame (all children with a mother id), {race}",
                     [f"{int(q['exp'].sum()):,}", f"{int((q['exp'] == 0).sum()):,}", f"{len(q):,}"]))
        q = P[P["race"] == race]
        rows.append((f"Future-displacement frame, {race} (exposed 12-17 / not)",
                     [f"{int(q['a1'].between(12, 17).sum()):,}", f"{int(q['a1'].isna().sum()):,}", f"{len(q):,}"]))
    md += ["## 6. Sample sizes", "", fd.md_table(["Displaced / exposed", "Not", "Rows"], [("", rows)]), ""]

    pd.DataFrame(ROWS).to_csv(OUT / "displacement_id.csv", index=False)
    (OUT / "displacement_id.md").write_text("\n".join(md), encoding="utf-8")
    print("done", len(ROWS))


if __name__ == "__main__":
    main()
