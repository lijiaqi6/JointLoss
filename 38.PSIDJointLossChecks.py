r"""PSID checks on the joint job loss of spouses requested by the referee review of Paper A (2026-10-17).

IGE/proposals/fable_review_paperA.md, Secs. 3.1-3.2 and plan items 3, 6, 11. Four blocks; samples and builders are those
of 19.FatherDisplacement.py (stacked family event study), 25.JointJobLoss.py (wife's own job ends, window designs,
couple-years) and 23.CorrelatedShocks.py (wife's reason-for-job-end items, couples), imported via importlib (no edits).
Unweighted PSID SRC + SEO, Black and White (head's race). S.e. clustered by 1968 family (fam68); *** p<0.01, ** p<0.05,
* p<0.1; p-values normal.

Reads (read only): IGE/data/psid_person_year.pkl, psid_displacement.pkl, correlated_shocks_fam.pkl,
correlated_shocks_units.pkl, husband_shocks_fam.pkl, and the raw PSID family files (Dropbox/PSID/Family; hours via
9.family(), food items below). Writes
  IGE/data/psid_joint_loss_food.pkl            cache of the food items (wave x interview number)
  IGE/output/psid_joint_loss_checks.csv        every estimate
  IGE/output/psid_joint_loss_checks.md         tables
  IGE/output/psid_jl_gross_net_es.png, psid_jl_food_es.png, psid_jl_closures_es.png   event-study figures
  IGE/paperA_joint_loss/fig_gross_net_awe.pdf/.png, fig_food_single_joint.pdf/.png   paper figures

1. GROSS VS NET ADDED-WORKER EFFECT. 19's stacked design (fathers first displaced in ev vs clean controls; father x stack
   and calendar year x stack FE; e = -3..+6, reference e = -2), event years 1984-2021 so that the wife's own window is
   measurable, wife present at baseline. J = the baseline wife reports her own displacement (closure / layoff / fired) in
   ev-1..ev+1 (25's definition: all three years covered; J = 0 if she did not work at baseline). Outcomes: wife's annual
   hours and employment (hours > 0) while she is the baseline wife. (a) descriptive split: separate event studies of
   treated with J = 0 vs controls with J = 0 (gross response), treated with J = 1 vs controls with J = 0 and vs controls
   with J = 1; (b) interaction model: displaced x e, J x e, displaced x J x e (one regression). With P1 / P0 = share of
   J among displaced / control families, net = gross + (P1 - P0) x b_J + P1 x b_DJ exactly in group means; the implied
   net is reported next to the directly estimated net (plain event study, same sample). J is an outcome of the event,
   so conditioning on it is descriptive (the J = 0 wives are selected on not losing their job).
2. CLOSURES ONLY. 19's design with (i) closures only (19's 'strict': first displacement is a plant closure), (ii)
   layoffs only (first displacement is a layoff / firing; closures dropped), for the eight outcomes of Table 1, all
   event-time coefficients, by race and by the youngest child's age. Marriage ('still with baseline wife') by race and
   design with Black - White and closure - layoff differences (separate regressions; clusters treated as independent).
   Pre-displacement dip at e = -1: by dated vs undated reports (undated = placed in the year before the interview) and
   by era (event years before / from 1984), and the head's hourly earnings (labor income / hours, hours >= 260).
3. JOINT LOSS WITH A PLACEBO WINDOW. 25's window design re-estimated (wives employed at baseline, event years
   1987-2021, both windows covered; W = ev-1..ev+1, PL = ev-4..ev-2; future placebo = husband first displaced in
   ev+4..ev+6). Decomposition into a permanent couple component and a contemporaneous component: windows stacked (two
   rows per couple), y = a(ev x window) + pi x 1{husband ever displaced: treated or future placebo} + c x 1{treated} x
   1{W}, so pi is identified from the treated's PL window and both windows of the future placebo, c from the treated's
   W window. Period splits by event year: 1984-89 / 1990-99 / 2000-21; annual interviews (window years 1983-1996: ev
   1984-1995; main sample ev 1987-1995) and employer histories (window years 2001+: ev 2002-2021; main sample, PL also
   2001+: ev 2005-2021). Explanations by period: dual-earner share, the wife's baseline displacement rate, the share of
   her reports dated by a reported end year, same-sector share, the excess in a wider window (ev-2..ev+2) and the
   unconditional excess among all married fathers (J = 0 if she did not work). Couple-year probabilities by period.
4. FOOD (validation only; not a model target). Real family food spending (2000 dollars, CPI-U of the interview year):
   food at home (excluding food stamps) + food eaten out (+ delivered food 1994+), the PSID 'average week' / annual
   amounts at the interview. Waves used: 1981-1987, 1990-1997, 1999-2023 (no food questions in 1988-1989). Items:
     1981 V7564 / V7566; 1982 V8256 / V8258; 1983 V8864 / V8866; 1984 V10235 / V10237; 1985 V11375 / V11377;
     1986 V12774 / V12776; 1987 V13876 / V13878; 1990 V17807 / V17809; 1991 V19107 / V19109; 1992 V20407 / V20409;
     1993 V21707 / V21711 (annual food at home excl. food stamps / annual eating out; values >= 99,998 dropped);
     1994-1997 F15 / F19 (at home, food-stamp / other branch), F17 / F21 (delivered), F18 / F22 (eating out), each an
     amount and a time unit (1994: 1 week, 2 two weeks, 3 month; 1995-97: 3 week, 4 two weeks, 5 month, 6 year;
     other units / DK / NA -> missing): 1994 ER3078-ER3091,
     1995 ER6077-ER6090, 1996 ER8174-ER8187, 1997 ER11068-ER11082;
     1999-2023 the PSID generated 'FOOD AT HOME / FOOD AWAY FROM HOME / FOOD DELIVERED EXPENDITURE yyyy' (found by
     label; PSID-imputed values kept, negative values dropped).
   Timing: the interview of wave w is put on calendar year w - 1 like every other outcome, so food at event time e is
   reported at the interview in early ev + e + 1 (e = 0: the first interview after the job loss; e = -2: clearly
   before). Food is kept while the baseline wife is in the family. Design: 19's stacks, event years 1984-2021, married at
   baseline; single = husband displaced and J = 0, joint = husband displaced and J = 1; interaction model as in 1 (single
   = displaced x e; joint = displaced + J + displaced x J, both relative to control families whose wife was not
   displaced). Levels and logs; dual-earner couples (wife employed at baseline) and all married couples.
"""
import importlib.util
import re
import warnings

import numpy as np
import pandas as pd
from scipy import stats

from common import DATA, OUT, HERE, CPI, stars

warnings.simplefilter("ignore", FutureWarning)
warnings.simplefilter("ignore", RuntimeWarning)
PAPER = HERE / "paperA_joint_loss"


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


P25 = _load("p25", "25.JointJobLoss.py")
P23, P19 = P25.P23, P25.P19
psid1, psid9 = P19.psid1, P19.psid9
ols_cl, md_table = P23.ols_cl, P19.md_table
ES_E = P19.ES_E
CPI2 = {**CPI, 2023: 304.7}
ROWS = []


def pv(b, se):
    return 2 * stats.norm.sf(abs(b / se)) if (se == se and se > 0) else np.nan


def cell(b, se, p=None, d=3):
    if not (se == se and se > 0):
        return "n.a."
    p = pv(b, se) if p is None else p
    return f"{b:,.{d}f}{stars(p)} ({se:,.{d}f}; p={'<0.001' if p < 0.001 else f'{p:.3f}'})"


def big(b, se, p=None):
    return cell(b, se, p, d=0)


def rec(item, table, sample, outcome, term, b, se, p=None, **kw):
    p = pv(b, se) if p is None else p
    ROWS.append(dict(item=item, table=table, sample=sample, outcome=outcome, term=term, coef=b, se=se, p=p, **kw))


def comb(b, V, xs, w):
    """linear combination sum_k w[k] * b[k] -> (est, se, p)."""
    L = np.array([w.get(x, 0.0) for x in xs])
    e, s = L @ b, np.sqrt(L @ V @ L)
    return e, s, pv(e, s)


# ================================================================ food items
INF = re.compile(r"(?:long\s+)?([A-Z]+\d+[A-Z0-9]*)\s+(\d+)\s*-\s*(\d+)")
LAB = re.compile(r'label variable\s+(\S+)\s+"(.*)"')
PRE94 = {1981: ("V7564", "V7566"), 1982: ("V8256", "V8258"), 1983: ("V8864", "V8866"), 1984: ("V10235", "V10237"),
         1985: ("V11375", "V11377"), 1986: ("V12774", "V12776"), 1987: ("V13876", "V13878"),
         1990: ("V17807", "V17809"), 1991: ("V19107", "V19109"), 1992: ("V20407", "V20409"),
         1993: ("V21707", "V21711")}
# (home branch 1, home branch 2, delivered 1, delivered 2, away 1, away 2): (amount, unit)
MID = {1994: (("ER3078", "ER3079"), ("ER3085", "ER3086"), ("ER3081", "ER3082"), ("ER3088", "ER3089"),
              ("ER3083", "ER3084"), ("ER3090", "ER3091")),
       1995: (("ER6077", "ER6078"), ("ER6084", "ER6085"), ("ER6080", "ER6081"), ("ER6087", "ER6088"),
              ("ER6082", "ER6083"), ("ER6089", "ER6090")),
       1996: (("ER8174", "ER8175"), ("ER8181", "ER8182"), ("ER8177", "ER8178"), ("ER8184", "ER8185"),
              ("ER8179", "ER8180"), ("ER8186", "ER8187")),
       1997: (("ER11068", "ER11069"), ("ER11076", "ER11077"), ("ER11071", "ER11072"), ("ER11079", "ER11080"),
              ("ER11073", "ER11074"), ("ER11081", "ER11082"))}
UNIT94 = {1994: {1: 52.0, 2: 26.0, 3: 12.0}}
UNIT95 = {3: 52.0, 4: 26.0, 5: 12.0, 6: 1.0}


def _layout(do):
    t = do.read_text(encoding="latin-1")
    block = re.search(r"\binfix\b(.*?)\busing\b", t, re.S).group(1)
    return {v: (int(a) - 1, int(b)) for v, a, b in INF.findall(block)}, [(v, l.strip()) for v, l in LAB.findall(t)]


def _annual(a, u, w):
    a = pd.to_numeric(a, errors="coerce")
    u = pd.to_numeric(u, errors="coerce")
    mult = u.map(UNIT94.get(w, UNIT95))
    out = a * mult
    out = out.where(a > 0, 0.0)
    out = out.where(~a.isin([99998, 99999]) & a.notna())
    return out


def food():
    fn = DATA / "psid_joint_loss_food.pkl"
    if fn.exists():
        return pd.read_pickle(fn)
    out, found = [], []
    for w in [w for w in psid1.WAVES if w >= 1981 and w not in (1988, 1989)]:
        folder = psid1.FAM / (f"fam{w}" if w < 1994 else f"fam{w}er")
        do = next(f for f in folder.glob("*.do") if "formats" not in f.name)
        pos, labs = _layout(do)
        idv = labs[1][0]
        if w in PRE94:
            h, a = PRE94[w]
            f = pd.read_fwf(do.with_suffix(".txt"), colspecs=[pos[c] for c in (idv, h, a)], names=[idv, h, a],
                            header=None, encoding="latin-1")
            x = pd.DataFrame({"wave": w, "int": f[idv], "f_home": f[h].where(f[h].between(0, 99997)),
                              "f_away": f[a].where(f[a].between(0, 99997)), "f_deliv": 0.0})
            found.append(dict(wave=w, items=f"{h} / {a}", units=""))
        elif w in MID:
            cols = [idv] + [c for pr in MID[w] for c in pr]
            f = pd.read_fwf(do.with_suffix(".txt"), colspecs=[pos[c] for c in cols], names=cols, header=None,
                            encoding="latin-1")
            an = [_annual(f[a], f[u], w) for a, u in MID[w]]
            x = pd.DataFrame({"wave": w, "int": f[idv], "f_home": an[0] + an[1], "f_deliv": an[2] + an[3],
                              "f_away": an[4] + an[5]})
            uc = pd.concat([f[u] for _, u in MID[w]]).value_counts().sort_index().to_dict()
            found.append(dict(wave=w, items=" ".join(f"{a}/{u}" for a, u in MID[w]), units=str(uc)))
        else:
            sel = {}
            for k, pat in (("f_home", r"^FOOD AT HOME EXPENDITURE"), ("f_away", r"^FOOD AWAY FROM HOME EXPENDITURE"),
                           ("f_deliv", r"^FOOD DELIVERED EXPENDITURE")):
                sel[k] = next(v for v, l in labs if re.search(pat, l) and v in pos)
            cols = [idv] + list(sel.values())
            f = pd.read_fwf(do.with_suffix(".txt"), colspecs=[pos[c] for c in cols], names=cols, header=None,
                            encoding="latin-1")
            x = pd.DataFrame({"wave": w, "int": f[idv]})
            for k, v in sel.items():
                x[k] = pd.to_numeric(f[v], errors="coerce").where(lambda s: s >= 0)
            found.append(dict(wave=w, items=" / ".join(sel.values()), units=""))
        out.append(x)
        print("food", w, flush=True)
    F = pd.concat(out, ignore_index=True)
    defl = F["wave"].map(lambda w: CPI2[2000] / CPI2[w])
    for c in ("f_home", "f_away", "f_deliv"):
        F[c] = F[c] * defl
    F["food"] = F["f_home"] + F["f_away"] + F["f_deliv"]
    res = dict(F=F, found=pd.DataFrame(found))
    pd.to_pickle(res, fn)
    return res


# ================================================================ event-study helpers
def es_plain(q, y):
    """19's event study on sample q; dict term -> (b, se, p) + info."""
    o = P19.event_study(q, y)
    return {r["term"]: (r["coef"], r["se"], r["p"]) for r in o}, dict(n=o[0]["n"], units=o[0]["units"],
                                                                         controls=o[0]["controls"],
                                                                         clusters=o[0]["clusters"],
                                                                         pre=o[0]["pre_mean"])


def es_inter(q, y, J="J"):
    """displaced x e, J x e, displaced x J x e with father x stack and year x stack FE (19's twfe)."""
    q = q.dropna(subset=[y, J]).copy()
    xs = []
    for e in ES_E:
        ind = (q["e"] == e).astype(float)
        q[f"d{e}"], q[f"j{e}"], q[f"t{e}"] = ind * q["treat"], ind * q[J], ind * q["treat"] * q[J]
        xs += [f"d{e}", f"j{e}", f"t{e}"]
    b, V, info = P19.twfe(q, y, xs)
    u = q.drop_duplicates("unit")
    info["P1"] = u.loc[u["treat"] == 1, J].mean()
    info["P0"] = u.loc[u["treat"] == 0, J].mean()
    info["n_t1"] = int(((u["treat"] == 1) & (u[J] == 1)).sum())
    info["n_c1"] = int(((u["treat"] == 0) & (u[J] == 1)).sum())
    info["pre_t0"] = q.loc[(q["treat"] == 1) & (q[J] == 0) & q["e"].isin([-2, -1]), y].mean()
    info["pre_t1"] = q.loc[(q["treat"] == 1) & (q[J] == 1) & q["e"].isin([-2, -1]), y].mean()
    return b, V, xs, info


def inter_terms(b, V, xs, info, es):
    """combinations over event times es (equal weights)."""
    w = 1.0 / len(es)
    P1, P0 = info["P1"], info["P0"]
    D = {f"d{e}": w for e in es}
    Jw = {f"j{e}": w for e in es}
    T = {f"t{e}": w for e in es}
    add = lambda *ds: {k: sum(dd.get(k, 0) for dd in ds) for dd in ds for k in dd}
    scale = lambda dd, s: {k: v * s for k, v in dd.items()}
    return {"gross": comb(b, V, xs, D), "own": comb(b, V, xs, Jw), "trip": comb(b, V, xs, T),
            "j1_vs_c0": comb(b, V, xs, add(D, Jw, T)), "j1_vs_c1": comb(b, V, xs, add(D, T)),
            "jt_minus_single": comb(b, V, xs, add(Jw, T)),
            "net_implied": comb(b, V, xs, add(D, scale(Jw, P1 - P0), scale(T, P1))),
            "offset": comb(b, V, xs, add(scale(Jw, P1 - P0), scale(T, P1)))}


def by_e(b, V, xs, info):
    return {e: inter_terms(b, V, xs, info, [e]) for e in ES_E}


# ================================================================ main
def main():
    md = ["# PSID checks on the joint job loss of spouses (referee review of Paper A)", "",
          "Built by `38.PSIDJointLossChecks.py` (2026-10-17); definitions in its docstring. Requested by "
          "`proposals/fable_review_paperA.md` Secs. 3.1-3.2, plan items 3, 6, 11. Unweighted PSID SRC + SEO, Black and "
          "White (head's race). S.e. clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1. Every cell: "
          "coefficient*** (s.e.; p). Dollars are 2000 dollars.", ""]
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    E = P23.extras()
    X, R = E["X"], E["R"]
    fam = psid9.family()
    d = pd.read_pickle(DATA / "psid_displacement.pkl")
    ev_sets = P25.wife_events(py, R)
    m = P19.men_panel(py, fam)
    FD = food()
    F = FD["F"]
    m = m.merge(F[["wave", "int", "food", "f_home", "f_away"]], on=["wave", "int"], how="left")
    m = m.drop_duplicates(["pid", "year"])
    U = P25.build_units(m, d)
    U = P25.add_wife_outcomes(U, m, ev_sets)
    U23 = pd.read_pickle(DATA / "correlated_shocks_units.pkl")[["pid", "ev", "same_sec"]]
    U = U.merge(U23, on=["pid", "ev"], how="left")
    print("units", len(U), int(U["treat"].sum()), flush=True)

    # ---------------- J for the stacked family panels
    Uj = U[U["pseudo"] == 0][["pid", "ev", "treat", "wemp0", "main_W"] + [f"main{k}" for k in (-1, 0, 1)]].copy()
    Uj["J"] = np.where(Uj["wemp0"] == 0, 0.0, Uj["main_W"])
    len_ = Uj[[f"main{k}" for k in (-1, 0, 1)]].max(axis=1, skipna=True)
    Uj["J_len"] = np.where(Uj["wemp0"] == 0, 0.0, len_)
    Uj = Uj.rename(columns={"treat": "treat_u"})
    P = P19.stacks(m, d, "main")
    P = P.merge(m[["pid", "year", "food", "f_home", "f_away"]], on=["pid", "year"], how="left")
    same = (P["w_pid"] == P["w0"]) & P["w0"].notna()
    for c in ("food", "f_home", "f_away"):
        P[c] = P[c].where(same)
    P["lfood"] = np.log(P["food"].where(P["food"] > 0))
    P["hourly"] = (P["hlab"] / P["hh"]).where(P["hh"] >= 260)
    P = P.merge(Uj[["pid", "ev", "treat_u", "J", "J_len", "wemp0"]], on=["pid", "ev"], how="left")
    chk = P.dropna(subset=["treat_u"]).drop_duplicates("unit")
    print("treat agreement", (chk["treat"] == chk["treat_u"]).mean(), flush=True)
    P["wemp0"] = np.where(P["w0"].notna(), (P["wh0"] > 0).astype(float), np.nan)

    # ============================================================ 1. gross vs net
    Q0 = P[P["ev"].between(1984, 2021) & P["w0"].notna()].copy()
    cov = Q0.drop_duplicates("unit")
    covtab = {t: (cov.loc[cov["treat"] == t, "J"].notna().mean(), int((cov["treat"] == t).sum())) for t in (1, 0)}
    Q = Q0.dropna(subset=["J"]).copy()
    u1 = Q.drop_duplicates("unit")
    PANELS1 = [("All wives present at baseline", lambda q: q), ("Youngest child 0-5", lambda q: q[q["young0"] <= 5]),
               ("Youngest child 6-17", lambda q: q[q["young0"] >= 6]),
               ("Wife employed at baseline", lambda q: q[q["wemp0"] == 1]),
               ("Wife employed at baseline, youngest 0-5", lambda q: q[(q["wemp0"] == 1) & (q["young0"] <= 5)]),
               ("Wife employed at baseline, youngest 6-17", lambda q: q[(q["wemp0"] == 1) & (q["young0"] >= 6)]),
               ("Black", lambda q: q[q["hrace"] == "Black"]), ("White", lambda q: q[q["hrace"] == "White"])]
    Y1 = [("w_hrs", "Wife's annual hours"), ("w_emp", "Wife employed")]
    INT, NET, BYE = {}, {}, {}
    for pname, f in PANELS1:
        q = f(Q)
        for y, _ in Y1:
            b, V, xs, info = es_inter(q, y)
            T = inter_terms(b, V, xs, info, [1, 2, 3])
            net, ninf = es_plain(q, y)
            INT[(pname, y)] = (T, info)
            NET[(pname, y)] = (net, ninf)
            if pname in ("All wives present at baseline", "Youngest child 0-5", "Youngest child 6-17",
                         "Wife employed at baseline"):
                BYE[(pname, y)] = by_e(b, V, xs, info)
            for k, (bb, se, p) in T.items():
                rec(1, "interaction_mean+1..+3", pname, y, k, bb, se, p, n=info["n"], P1=info["P1"], P0=info["P0"],
                    treated=info["units"], treated_J1=info["n_t1"], controls_J1=info["n_c1"],
                    clusters=info["clusters"])
            for t, (bb, se, p) in net.items():
                rec(1, "net_plain_event_study", pname, y, t, bb, se, p, n=ninf["n"], treated=ninf["units"])
            if (pname, y) in BYE:
                for e, TT in BYE[(pname, y)].items():
                    for k, (bb, se, p) in TT.items():
                        rec(1, "interaction_by_e", pname, y, f"e={e:+d}:{k}", bb, se, p)
        print("item 1", pname, flush=True)
    # descriptive split (separate regressions)
    SPL = [("Net: all displaced vs all controls", lambda q: q),
           ("Gross: displaced, wife NOT displaced vs controls, wife not displaced", lambda q: q[q["J"] == 0]),
           ("Displaced, wife ALSO displaced vs controls, wife not displaced",
            lambda q: q[((q["treat"] == 1) & (q["J"] == 1)) | ((q["treat"] == 0) & (q["J"] == 0))]),
           ("Displaced, wife also displaced vs controls, wife displaced", lambda q: q[q["J"] == 1])]
    SPLIT = {}
    for pname, f in PANELS1[:4]:
        for sname, g in SPL:
            q = g(f(Q))
            for y, _ in Y1:
                est, inf = es_plain(q, y)
                SPLIT[(pname, sname, y)] = (est, inf)
                for t, (bb, se, p) in est.items():
                    rec(1, "descriptive_split", f"{pname} | {sname}", y, t, bb, se, p, n=inf["n"],
                        treated=inf["units"], controls=inf["controls"], clusters=inf["clusters"])
        print("split", pname, flush=True)
    # lenient J robustness
    QL = Q0.dropna(subset=["J_len"]).copy()
    LEN = {}
    for y, _ in Y1:
        b, V, xs, info = es_inter(QL, y, "J_len")
        LEN[y] = (inter_terms(b, V, xs, info, [1, 2, 3]), info)
        for k, (bb, se, p) in LEN[y][0].items():
            rec(1, "interaction_mean+1..+3_lenientJ", "All wives present at baseline", y, k, bb, se, p,
                n=info["n"], P1=info["P1"], P0=info["P0"])

    NS = {}
    Pw = P[P["w0"].notna()]
    for sname, q in (("Table 1 sample: event years 1968-2022", Pw), ("Event years 1968-1983", Pw[Pw["ev"] <= 1983]),
                     ("Event years 1984-2021, all", Pw[Pw["ev"].between(1984, 2021)]),
                     ("Event years 1984-2021, J defined (section 1a sample)", Q)):
        for kid, g in (("all", lambda x: x), ("youngest 0-5", lambda x: x[x["young0"] <= 5]),
                       ("youngest 6-17", lambda x: x[x["young0"] >= 6])):
            for y, _ in Y1:
                est, inf = es_plain(g(q), y)
                NS[(sname, kid, y)] = (est["mean +1..+3"], inf)
                rec(1, "net_by_sample", f"{sname} | {kid}", y, "mean +1..+3", *est["mean +1..+3"], n=inf["n"],
                    treated=inf["units"])
    print("net by sample", flush=True)
    t19 = pd.read_csv(OUT / "father_displacement.csv")
    t19 = t19[(t19["table"] == "family_event_study") & (t19["design"] == "main") & (t19["sample"] == "All") &
              (t19["subsample"].isna()) & (t19["term"] == "mean +1..+3")].set_index("outcome")
    md += ["## 1. Gross vs net added-worker effect", "",
           "19's stacked design restricted to event years 1984-2021 (the wife's own job-end reports start with the "
           "1984 wave) and to fathers with a wife at baseline. J = the baseline wife reports her own displacement "
           "(closure, layoff or firing) dated ev-1..ev+1, all three years covered (J = 0 if she did not work at "
           "baseline). Coverage: J is defined for "
           f"{covtab[1][0]:.3f} of {covtab[1][1]:,} displaced and {covtab[0][0]:.3f} of {covtab[0][1]:,} control "
           "father-stacks with a wife (it is missing when the couple has split up or is not interviewed by the "
           "interview that covers ev+1). Outcomes: wife's annual hours and employment (hours > 0) while she is the "
           "baseline wife; mean of event years +1..+3 relative to e = -2. Table 1 of the paper (all event years "
           f"1968-2022): wife's hours {big(t19.loc['w_hrs', 'coef'], t19.loc['w_hrs', 'se'])}, employed "
           f"{cell(t19.loc['w_emp', 'coef'], t19.loc['w_emp', 'se'])}.", "",
           "### 1a. Interaction model (one regression per cell column; mean of e = +1..+3)", "",
           "Rows: 'Displaced' = displaced x e (the GROSS response: displaced families whose wife was not displaced "
           "vs control families whose wife was not displaced); 'Wife's own displacement' = J x e among control "
           "families (what a wife's displacement does to her hours absent his); 'Displaced x wife's own "
           "displacement' = the triple interaction. Derived rows are linear combinations of the same regression. "
           "Implied net = gross + (P1 - P0) x own + P1 x triple (exact in group means); 'joint-loss offset' = implied "
           "net - gross. 'Net, plain event study' = 19's event study on the same sample.", ""]
    panels = []
    LBL = [("gross", "Displaced (gross response: wife not displaced)"), ("own", "Wife's own displacement (controls)"),
           ("trip", "Displaced x wife's own displacement"),
           ("j1_vs_c0", "Derived: displaced, wife also displaced, vs controls with wife not displaced"),
           ("j1_vs_c1", "Derived: displaced, wife also displaced, vs controls with wife displaced"),
           ("net_implied", "Derived: implied net = gross + (P1-P0) own + P1 triple"),
           ("offset", "Derived: joint-loss offset (implied net - gross)")]
    for pname, _ in PANELS1:
        rows = []
        for k, lab in LBL:
            rows.append((lab, [(big if y == "w_hrs" else cell)(*INT[(pname, y)][0][k]) for y, _ in Y1]))
        rows.append(("Net, plain event study (same sample)",
                     [(big if y == "w_hrs" else cell)(*NET[(pname, y)][0]["mean +1..+3"]) for y, _ in Y1]))
        rows.append(("P1 / P0 (wife displaced: displaced / control families)",
                     [f"{INT[(pname, y)][1]['P1']:.3f} / {INT[(pname, y)][1]['P0']:.3f}" for y, _ in Y1]))
        rows.append(("Treated mean at e = -2, -1: wife not displaced / displaced",
                     [f"{INT[(pname, y)][1]['pre_t0']:,.3f} / {INT[(pname, y)][1]['pre_t1']:,.3f}" if y == "w_emp"
                      else f"{INT[(pname, y)][1]['pre_t0']:,.0f} / {INT[(pname, y)][1]['pre_t1']:,.0f}"
                      for y, _ in Y1]))
        rows.append(("Displaced fathers (wife displaced) / control stacks (wife displaced)",
                     [f"{INT[(pname, y)][1]['units']:,} ({INT[(pname, y)][1]['n_t1']:,}) / "
                      f"{INT[(pname, y)][1]['controls']:,} ({INT[(pname, y)][1]['n_c1']:,})" for y, _ in Y1]))
        rows.append(("N (man-years, stacked) / clusters",
                     [f"{INT[(pname, y)][1]['n']:,} / {INT[(pname, y)][1]['clusters']:,}" for y, _ in Y1]))
        panels.append((pname, rows))
    md += [md_table([lab for _, lab in Y1], panels,
                    [("Fixed effects", ["father x stack, calendar year x stack"] * 2)]), ""]
    rows = [(lab, [(big if y == "w_hrs" else cell)(*LEN[y][0][k]) for y, _ in Y1]) for k, lab in LBL]
    rows.append(("P1 / P0", [f"{LEN[y][1]['P1']:.3f} / {LEN[y][1]['P0']:.3f}" for y, _ in Y1]))
    rows.append(("N (man-years, stacked)", [f"{LEN[y][1]['n']:,}" for y, _ in Y1]))
    md += ["Robustness: J from the covered years of ev-1..ev+1 (at least one covered) instead of all three:", "",
           md_table([lab for _, lab in Y1], [("All wives present at baseline (lenient J)", rows)]), ""]
    panels = []
    for sname in ("Table 1 sample: event years 1968-2022", "Event years 1968-1983", "Event years 1984-2021, all",
                  "Event years 1984-2021, J defined (section 1a sample)"):
        rows = []
        for kid in ("all", "youngest 0-5", "youngest 6-17"):
            rows.append((f"Displaced, mean e = +1..+3 ({kid})",
                         [(big if y == "w_hrs" else cell)(*NS[(sname, kid, y)][0]) for y, _ in Y1]))
            rows.append((f"Displaced / N ({kid})", [f"{NS[(sname, kid, y)][1]['units']:,} / {NS[(sname, kid, y)][1]['n']:,}"
                                                   for y, _ in Y1]))
        panels.append((sname, rows))
    md += ["### 1a'. The net response by sample period (19's plain event study)", "",
           "Where the Table 1 net (+51 hours) comes from: the added-worker response is concentrated in event years "
           "before 1984, when the wife's own job ends are not measured; the gross / net decomposition can only be "
           "estimated from 1984.", "",
           md_table([lab for _, lab in Y1], panels, [("Fixed effects", ["father x stack, calendar year x stack"] * 2)]),
           ""]
    md += ["### 1b. Descriptive split (separate event studies; every event-time coefficient)", "",
           "Each panel is one sample, each column one regression (19's specification). Wife's own displacement J as "
           "above. 'Gross' compares displaced and control families in which the wife was not displaced.", ""]
    panels = []
    terms = [f"e={e:+d}" for e in ES_E] + ["mean +1..+3"]
    for pname, _ in PANELS1[:4]:
        for sname, _ in SPL:
            rows = [(t, [(big if y == "w_hrs" else cell)(*SPLIT[(pname, sname, y)][0][t]) for y, _ in Y1])
                    for t in terms]
            rows.append(("Displaced / controls / N / clusters",
                         [f"{SPLIT[(pname, sname, y)][1]['units']:,} / {SPLIT[(pname, sname, y)][1]['controls']:,} / "
                          f"{SPLIT[(pname, sname, y)][1]['n']:,} / {SPLIT[(pname, sname, y)][1]['clusters']:,}"
                          for y, _ in Y1]))
            panels.append((f"{pname}: {sname}", rows))
    md += [md_table([lab for _, lab in Y1], panels, [("Fixed effects", ["father x stack, calendar year x stack"] * 2)]),
           "", "![gross vs net](psid_jl_gross_net_es.png)", ""]
    print("item 1 done", flush=True)

    # ============================================================ 2. closures only
    Pc = P19.stacks(m, d, "strict")
    Pc["hourly"] = (Pc["hlab"] / Pc["hh"]).where(Pc["hh"] >= 260)
    typ = d[d["main"] == 1][["pid", "year", "strict", "dated"]].rename(columns={"year": "ev"})
    P = P.merge(typ.rename(columns={"strict": "ev_strict", "dated": "ev_dated"}), on=["pid", "ev"], how="left")
    Pl = P[(P["treat"] == 0) | (P["ev_strict"] == 0)].copy()
    Y2 = P19.ES_Y
    PAN2 = [("All", lambda q: q), ("Black", lambda q: q[q["hrace"] == "Black"]),
            ("White", lambda q: q[q["hrace"] == "White"]), ("Youngest child 0-5", lambda q: q[q["young0"] <= 5]),
            ("Youngest child 6-17", lambda q: q[q["young0"] >= 6])]
    CL = {}
    for dname, src, pans in (("Closures only", Pc, PAN2), ("Layoffs only", Pl, PAN2[:3]), ("Main", P, PAN2[:3])):
        for pname, f in pans:
            for y, _ in Y2:
                if dname == "Main" and y != "bw_present":
                    continue
                est, inf = es_plain(f(src), y)
                CL[(dname, pname, y)] = (est, inf)
                for t, (bb, se, p) in est.items():
                    rec(2, "family_event_study", f"{dname}: {pname}", y, t, bb, se, p, n=inf["n"],
                        treated=inf["units"], controls=inf["controls"], clusters=inf["clusters"], pre_mean=inf["pre"])
            print("item 2", dname, pname, flush=True)
    fmt2 = lambda y, t: (big if y in ("hh", "hlab", "w_hrs", "faminc") else cell)(*t)
    md += ["## 2. Closures only: the family event study and the marriage response", "",
           "19's stacked design (all event years 1968-2022, fathers with a child 0-17 and positive hours at baseline). "
           "Closures only = the father's first displacement is a plant closure / move (19's 'strict'); layoffs only = "
           "his first displacement is a layoff or firing (closure-treated dropped); controls as in 19. All "
           "event-time coefficients (reference e = -2).", "",
           "### 2a. Closures only: full parallel version of Table 1", ""]
    panels = []
    for pname, _ in PAN2:
        est = {y: CL[("Closures only", pname, y)] for y, _ in Y2}
        rows = [(t, [fmt2(y, est[y][0][t]) for y, _ in Y2]) for t in terms]
        rows.append(("Treated mean at e = -2, -1", [f"{est[y][1]['pre']:,.3f}" if est[y][1]['pre'] < 10 else
                                                    f"{est[y][1]['pre']:,.0f}" for y, _ in Y2]))
        rows.append(("Displaced / controls", [f"{est[y][1]['units']:,} / {est[y][1]['controls']:,}" for y, _ in Y2]))
        rows.append(("N / clusters", [f"{est[y][1]['n']:,} / {est[y][1]['clusters']:,}" for y, _ in Y2]))
        panels.append((f"Closures only: {pname}", rows))
    md += [md_table([lab for _, lab in Y2], panels, [("Fixed effects", ["father x stack, calendar year x stack"] *
                                                     len(Y2))]), "", "![closures](psid_jl_closures_es.png)", "",
           "### 2b. Layoffs only (parallel)", ""]
    panels = []
    for pname, _ in PAN2[:3]:
        est = {y: CL[("Layoffs only", pname, y)] for y, _ in Y2}
        rows = [(t, [fmt2(y, est[y][0][t]) for y, _ in Y2]) for t in ["e=-3", "e=-1", "e=+0", "e=+1", "e=+2",
                                                                       "e=+3", "e=+6", "mean +1..+3"]]
        rows.append(("Displaced / controls / N", [f"{est[y][1]['units']:,} / {est[y][1]['controls']:,} / "
                                                  f"{est[y][1]['n']:,}" for y, _ in Y2]))
        panels.append((f"Layoffs only: {pname}", rows))
    md += [md_table([lab for _, lab in Y2], panels, [("Fixed effects", ["father x stack, calendar year x stack"] *
                                                     len(Y2))]), ""]
    # marriage by race
    mar = {}
    rows = []
    for dname in ("Main", "Closures only", "Layoffs only"):
        cells = []
        for pname in ("Black", "White"):
            t = CL[(dname, pname, "bw_present")][0]["mean +1..+3"]
            mar[(dname, pname)] = t
            cells.append(cell(*t))
        b1, s1 = mar[(dname, "Black")][:2]
        b2, s2 = mar[(dname, "White")][:2]
        dd = (b1 - b2, np.sqrt(s1 ** 2 + s2 ** 2))
        rec(2, "marriage_BW_diff", dname, "bw_present", "Black - White mean +1..+3", *dd)
        cells.append(cell(*dd))
        rows.append((dname, cells))
    for t in ("e=+3", "e=+6"):
        for dname in ("Closures only", "Layoffs only"):
            cells = [cell(*CL[(dname, r, "bw_present")][0][t]) for r in ("Black", "White")]
            b1, s1 = CL[(dname, "Black", "bw_present")][0][t][:2]
            b2, s2 = CL[(dname, "White", "bw_present")][0][t][:2]
            cells.append(cell(b1 - b2, np.sqrt(s1 ** 2 + s2 ** 2)))
            rows.append((f"{dname}, {t}", cells))
    rows2 = []
    for r in ("Black", "White"):
        b1, s1 = mar[("Closures only", r)][:2]
        b2, s2 = mar[("Layoffs only", r)][:2]
        rec(2, "marriage_closure_minus_layoff", r, "bw_present", "mean +1..+3", b1 - b2, np.sqrt(s1 ** 2 + s2 ** 2))
        rows2.append(cell(b1 - b2, np.sqrt(s1 ** 2 + s2 ** 2)))
    rows.append(("Closures - layoffs (mean +1..+3)", rows2 + [""]))
    md += ["### 2c. Marriage response by race and type of job loss ('still with baseline wife')", "",
           "Columns: Black fathers, White fathers, difference (separate regressions; 1968-family clusters are "
           "disjoint by race up to a few split-offs, so the variance of the difference is the sum). Charles and "
           "Stephens (2004) find divorce rises after layoffs, not after plant closures.", "",
           md_table(["Black", "White", "Black - White"], [("Mean of e = +1..+3 unless stated", rows)]), ""]
    # dip at e = -1
    DIP = [("Main: all", P), ("Main: dated reports", P[(P["treat"] == 0) | (P["ev_dated"] == True)]),
           ("Main: undated reports (year before the interview)", P[(P["treat"] == 0) | (P["ev_dated"] == False)]),
           ("Main: event years 1968-1983", P[P["ev"] <= 1983]), ("Main: event years 1984-2022", P[P["ev"] >= 1984]),
           ("Closures only", Pc), ("Layoffs only", Pl)]
    YD = [("hh", "Head's hours"), ("hlab", "Head's labor income"), ("hourly", "Head's hourly earnings (hours >= 260)"),
          ("faminc", "Family income")]
    DIPR = {}
    for sname, src in DIP:
        for y, _ in YD:
            est, inf = es_plain(src, y)
            DIPR[(sname, y)] = (est, inf)
            for t in ("e=-3", "e=-1", "e=+0", "mean +1..+3"):
                rec(2, "pre_dip", sname, y, t, *est[t], n=inf["n"], treated=inf["units"])
        print("dip", sname, flush=True)
    panels = []
    for sname, _ in DIP:
        rows = [(t, [(cell if y == "hourly" else big)(*DIPR[(sname, y)][0][t]) for y, _ in YD])
                for t in ("e=-3", "e=-1", "e=+0", "mean +1..+3")]
        rows.append(("Treated mean at e = -2, -1", [f"{DIPR[(sname, y)][1]['pre']:,.2f}" for y, _ in YD]))
        rows.append(("Displaced / N", [f"{DIPR[(sname, y)][1]['units']:,} / {DIPR[(sname, y)][1]['n']:,}"
                                       for y, _ in YD]))
        panels.append((sname, rows))
    md += ["### 2d. The pre-displacement dip at e = -1 (Jacobson-LaLonde-Sullivan)", "",
           "Same design; event-time coefficients relative to e = -2. 'Dated' = the displacement year comes from a "
           "reported end year; 'undated' = placed in the year before the interview (all pre-1984 E-branch reports). "
           "Hourly earnings = labor income / annual hours, years with at least 260 hours.", "",
           md_table([lab for _, lab in YD], panels, [("Fixed effects", ["father x stack, calendar year x stack"] * 4)]),
           ""]
    print("item 2 done", flush=True)

    # ============================================================ 3. placebo window, decomposition, periods
    WS = U[U["ev"].between(1987, 2021) & (U["wemp0"] == 1)].dropna(subset=["main_W", "main_PL"]).copy()
    WC = [("main_W", "Wife displaced, ev-1..ev+1"), ("main_PL", "Wife displaced, ev-4..ev-2 (placebo window)"),
          ("main_D", "Difference W - PL (couple FE)")]
    W3 = {}
    RACES = [("All", lambda q: q), ("Black", lambda q: q[q["hrace"] == "Black"]),
             ("White", lambda q: q[q["hrace"] == "White"])]
    for race, f in RACES:
        for y, _ in WC:
            est, inf = ols_cl(f(WS), y, ["treat", "pseudo"], fe=["ev"])
            inf["ctrl"] = f(WS).loc[(f(WS)["treat"] == 0) & (f(WS)["pseudo"] == 0), y].mean()
            W3[(race, y)] = (est, inf)
            for x, v in est.items():
                rec(3, "window_main_sample", race, y, x, *v, n=inf["n"], control_mean=inf["ctrl"])
    # stacked two-window decomposition
    L = pd.concat([WS.assign(win=0, y=WS["main_PL"]), WS.assign(win=1, y=WS["main_W"])], ignore_index=True)
    L["ever"] = ((L["treat"] == 1) | (L["pseudo"] == 1)).astype(float)
    L["tw"] = L["treat"] * L["win"]
    L["pw"] = L["pseudo"] * L["win"]
    L["evw"] = L["ev"] * 10 + L["win"]
    DEC = {}
    for race, f in RACES:
        q = f(L)
        e1, i1 = ols_cl(q, "y", ["ever", "tw"], fe=["evw"])
        e2, i2 = ols_cl(q, "y", ["treat", "pseudo", "tw", "pw"], fe=["evw"])
        tot = e1["ever"][0] + e1["tw"][0]
        DEC[race] = (e1, i1, e2, i2, tot)
        for x, v in e1.items():
            rec(3, "decomposition_pooled", race, "wife displaced (window)", x, *v, n=i1["n"], clusters=i1["clusters"])
        for x, v in e2.items():
            rec(3, "decomposition_separate", race, "wife displaced (window)", x, *v, n=i2["n"])
    # delta-method s.e. for the permanent share: bootstrap over families (cheap OLS by numpy)
    def share_boot(q, reps=300, seed=38):
        evd = pd.get_dummies(q["evw"].astype(int), drop_first=True, dtype=float).to_numpy()
        Xm = np.column_stack([np.ones(len(q)), q["ever"].to_numpy(), q["tw"].to_numpy(), evd])
        Y = q["y"].to_numpy(float)
        g = pd.factorize(q["fam68"])[0]
        members = [np.flatnonzero(g == j) for j in range(g.max() + 1)]
        rng = np.random.default_rng(seed)
        sh = []
        for _ in range(reps):
            idx = np.concatenate([members[j] for j in rng.integers(0, len(members), len(members))])
            bb = np.linalg.lstsq(Xm[idx], Y[idx], rcond=None)[0]
            sh.append(bb[1] / (bb[1] + bb[2]))
        return np.nanstd(sh)
    shse = share_boot(L)
    e1, i1, e2, i2, tot = DEC["All"]
    sh = e1["ever"][0] / tot
    rec(3, "decomposition_pooled", "All", "share permanent", "pi / (pi + c)", sh, shse)
    md += ["## 3. PSID joint job loss with the placebo window, and its decomposition", "",
           "25's window design (father x stack units, wife employed at baseline, event years 1987-2021, both windows "
           "covered, event-year FE). This reproduces Table 2 of `joint_job_loss.md`.", ""]
    panels = []
    for race, _ in RACES:
        rows = [(lab, [cell(*W3[(race, y)][0][x]) for y, _ in WC]) for x, lab in
                (("treat", "Husband displaced in ev"), ("pseudo", "Husband displaced in ev+4..ev+6 (future placebo)"))]
        rows.append(("Control mean", [f"{W3[(race, y)][1]['ctrl']:.3f}" for y, _ in WC]))
        rows.append(("N couples / clusters", [f"{W3[(race, y)][1]['n']:,} / {W3[(race, y)][1]['clusters']:,}"
                                              for y, _ in WC]))
        panels.append((race, rows))
    md += [md_table([lab for _, lab in WC], panels, [("Fixed effects", ["event year"] * 3)]), ""]
    panels = []
    for race, _ in RACES:
        e1, i1, e2, i2, tot = DEC[race]
        rows = [("Husband ever displaced (treated or future placebo): permanent couple component pi",
                 [cell(*e1["ever"]), ""]),
                ("Treated x window ev-1..ev+1: contemporaneous component c", [cell(*e1["tw"]), cell(*e2["tw"])]),
                ("Treated (level, both windows)", ["", cell(*e2["treat"])]),
                ("Future placebo (level, both windows)", ["", cell(*e2["pseudo"])]),
                ("Future placebo x window ev-1..ev+1", ["", cell(*e2["pw"])]),
                ("pi + c (total excess in the window)", [f"{tot:.3f}", ""]),
                ("N couple-windows / clusters", [f"{i1['n']:,} / {i1['clusters']:,}", f"{i2['n']:,} / {i2['clusters']:,}"])]
        if race == "All":
            rows.insert(6, ("Share permanent pi / (pi + c) (bootstrap s.e., 300 draws of families)",
                            [cell(sh, shse), ""]))
        panels.append((race, rows))
    md += ["### 3a. Permanent couple component vs contemporaneous component", "",
           "Two rows per couple (placebo window ev-4..ev-2 and window ev-1..ev+1), event year x window FE. Column 1: "
           "one permanent component pi for every couple whose husband is ever displaced (treated: their placebo "
           "window; future placebo: both windows), plus the contemporaneous excess c in the treated's window. Column 2 "
           "lets the level differ for treated and future placebo and adds a window effect for the future placebo "
           "(its window ev-1..ev+1 is still 3-7 years before his displacement).", "",
           md_table(["Wife displaced: one permanent component", "Wife displaced: separate levels"], panels,
                    [("Fixed effects", ["event year x window"] * 2)]), ""]
    # periods
    PER = [("1984-89", 1984, 1989, 1987, 1989), ("1990-99", 1990, 1999, 1990, 1999), ("2000-21", 2000, 2021, 2000, 2021),
           ("Annual interviews (window years 1983-96)", 1984, 1995, 1987, 1995),
           ("Employer histories (window years 2001+)", 2002, 2021, 2005, 2021)]
    # wife's reports: dated share by report year
    wf = py[py["wife"]][["wave", "int", "pid"]].drop_duplicates(["wave", "int"])
    rr = R.merge(wf, on=["wave", "int"], how="inner")
    rr = rr[rr["year"].between(rr["wave"] - 2, rr["wave"]) & (rr["code"].isin([1, 3]) | ((rr["code"] == 5) &
                                                                                       (rr["wave"] >= 2021)))]
    U["main_W2"] = U[[f"main{k}" for k in (-2, -1, 0, 1, 2)]].max(axis=1, skipna=False)
    U["J_unc"] = np.where(U["wemp0"] == 0, 0.0, U["main_W"])
    PR = {}
    for lab, a, b, am, bm in PER:
        base = U[(U["wemp0"] == 1) & U["ev"].between(a, b)]
        q = base.dropna(subset=["main_W"])
        est, inf = ols_cl(q, "main_W", ["treat", "pseudo"], fe=["ev"])
        cm = q.loc[(q["treat"] == 0) & (q["pseudo"] == 0), "main_W"].mean()
        q2 = base.dropna(subset=["main_W2"])
        est2, inf2 = ols_cl(q2, "main_W2", ["treat", "pseudo"], fe=["ev"])
        cm2 = q2.loc[(q2["treat"] == 0) & (q2["pseudo"] == 0), "main_W2"].mean()
        qm = U[(U["wemp0"] == 1) & U["ev"].between(am, bm)].dropna(subset=["main_W", "main_PL"])
        em = {y: ols_cl(qm, y, ["treat", "pseudo"], fe=["ev"]) for y in ("main_W", "main_PL", "main_D")}
        qu = U[U["wemp0"].notna() & U["ev"].between(a, b)].dropna(subset=["J_unc"])
        eu, iu = ols_cl(qu, "J_unc", ["treat", "pseudo"], fe=["ev"])
        allm = U[U["w0"].notna() & U["ev"].between(a, b) & (U["pseudo"] == 0)]
        de_all = (allm["wemp0"] == 1).mean()
        de_tr = (allm.loc[allm["treat"] == 1, "wemp0"] == 1).mean()
        ss = base.loc[base["treat"] == 1, "same_sec"].mean()
        ss_all = base.loc[(base["treat"] == 0) & (base["pseudo"] == 0), "same_sec"].mean()
        dated = rr[rr["year"].between(a - 1, b + 1)]["dated"].mean()
        hd_ = base[base["treat"] == 1][["pid", "ev"]].merge(d[d["main"] == 1][["pid", "year", "dated"]].rename(
            columns={"year": "ev"}), on=["pid", "ev"], how="left")
        hdated = (hd_["dated"] == True).mean()
        PR[lab] = dict(est=est, inf=inf, cm=cm, est2=est2, inf2=inf2, cm2=cm2, em=em, eu=eu, iu=iu, de_all=de_all,
                       de_tr=de_tr, ss=ss, ss_all=ss_all, dated=dated, hdated=hdated, nt=int(q["treat"].sum()),
                       ntm=int(qm["treat"].sum()))
        for x in ("treat", "pseudo"):
            rec(3, "period_window", lab, "main_W", x, *est[x], n=inf["n"], control_mean=cm)
            rec(3, "period_window_wide", lab, "main_W2", x, *est2[x], n=inf2["n"], control_mean=cm2)
            rec(3, "period_unconditional", lab, "J_unc", x, *eu[x], n=iu["n"])
            for y in ("main_W", "main_PL", "main_D"):
                rec(3, "period_main_sample", lab, y, x, *em[y][0][x], n=em[y][1]["n"])
        rec(3, "period_descriptives", lab, "dual-earner share (married, child, baseline)", "mean", de_all, np.nan)
        rec(3, "period_descriptives", lab, "dual-earner share among displaced", "mean", de_tr, np.nan)
        rec(3, "period_descriptives", lab, "same-sector share among displaced dual earners", "mean", ss, np.nan)
        rec(3, "period_descriptives", lab, "dated share of wives' displacement reports", "mean", dated, np.nan)
        rec(3, "period_descriptives", lab, "dated share of husbands' displacements (treated)", "mean", hdated, np.nan)
    # period differences (late - early)
    b1, s1 = PR["2000-21"]["est"]["treat"][:2]
    b0, s0 = PR["1984-89"]["est"]["treat"][:2]
    pdiff = (b1 - b0, np.sqrt(s1 ** 2 + s0 ** 2))
    rec(3, "period_window", "2000-21 minus 1984-89", "main_W", "treat", *pdiff)
    cols = [lab for lab, *_ in PER]
    rows = [("Window sample: husband displaced", [cell(*PR[c]["est"]["treat"]) for c in cols]),
            ("Window sample: future placebo", [cell(*PR[c]["est"]["pseudo"]) for c in cols]),
            ("Window sample: control mean / excess as multiple of it",
             [f"{PR[c]['cm']:.3f} / {PR[c]['est']['treat'][0] / PR[c]['cm']:.2f}" for c in cols]),
            ("Window sample: displaced / N", [f"{PR[c]['nt']:,} / {PR[c]['inf']['n']:,}" for c in cols]),
            ("Main sample (both windows): W, husband displaced", [cell(*PR[c]["em"]["main_W"][0]["treat"]) for c in cols]),
            ("Main sample: PL (placebo window), husband displaced",
             [cell(*PR[c]["em"]["main_PL"][0]["treat"]) for c in cols]),
            ("Main sample: difference W - PL (couple FE)", [cell(*PR[c]["em"]["main_D"][0]["treat"]) for c in cols]),
            ("Main sample: PL, future placebo", [cell(*PR[c]["em"]["main_PL"][0]["pseudo"]) for c in cols]),
            ("Main sample: displaced / N", [f"{PR[c]['ntm']:,} / {PR[c]['em']['main_W'][1]['n']:,}" for c in cols]),
            ("Wider window ev-2..ev+2: husband displaced", [cell(*PR[c]["est2"]["treat"]) for c in cols]),
            ("Wider window: control mean / N", [f"{PR[c]['cm2']:.3f} / {PR[c]['inf2']['n']:,}" for c in cols]),
            ("All married fathers (J = 0 if she did not work): husband displaced",
             [cell(*PR[c]["eu"]["treat"]) for c in cols]),
            ("Dual-earner share at baseline: all married fathers / displaced",
             [f"{PR[c]['de_all']:.3f} / {PR[c]['de_tr']:.3f}" for c in cols]),
            ("Same-sector share: displaced / control dual earners",
             [f"{PR[c]['ss']:.3f} / {PR[c]['ss_all']:.3f}" for c in cols]),
            ("Share of wives' displacement reports dated by an end year", [f"{PR[c]['dated']:.3f}" for c in cols]),
            ("Share of the husbands' displacements (treated) dated by an end year",
             [f"{PR[c]['hdated']:.3f}" for c in cols])]
    md += ["### 3b. Period splits and what explains them", "",
           "Columns = event-year periods (each cell a separate regression with event-year FE). Window sample: wives "
           "employed at baseline whose window ev-1..ev+1 is covered; main sample: both windows covered (event years "
           "from 1987, from 2005 for the employer-history column so that both windows come from the 2003+ job "
           "histories). Descriptive rows (shares) are sample means. 2000-21 minus 1984-89 (window sample): "
           f"{cell(*pdiff)}.", "", md_table(cols, [("", rows)], [("Fixed effects", ["event year"] * len(cols))]), ""]
    # couple-years by period
    F18 = pd.read_pickle(DATA / "husband_shocks_fam.pkl")
    C = P23.couples(py, X, F18, fam)
    both = (C["hh"] > 0) & (C["wh"] > 0)
    C["s_sec"] = (C["h_sec"] == C["w_sec"]).astype(float).where(both & C["h_sec"].notna() & C["w_sec"].notna())
    CY = P25.couple_years(m, d, ev_sets, C)
    CYP = [("All, 1984-2022", lambda q: q), ("Intervals ending 1984-89", lambda q: q[q["year"].between(1984, 1989)]),
           ("1990-99", lambda q: q[q["year"].between(1990, 1999)]), ("2000-22", lambda q: q[q["year"].between(2000, 2022)]),
           ("Annual intervals 1984-96", lambda q: q[q["annual"]]),
           ("Two-year intervals 2003-22 (employer histories)", lambda q: q[(q["year"] >= 2003) & ~q["annual"]])]
    rows = []
    for lab, f in CYP:
        q = f(CY).dropna(subset=["h", "w"])
        est, inf = ols_cl(q, "w", ["h"])
        p1, p0 = q.loc[q["h"] == 1, "w"].mean(), q.loc[q["h"] == 0, "w"].mean()
        t = q.groupby("fam68").apply(lambda g: pd.Series({"a": ((g.h == 1) & (g.w == 1)).sum(), "b": (g.h == 1).sum(),
                                                          "c": ((g.h == 0) & (g.w == 1)).sum(), "d": (g.h == 0).sum()}))
        T = t.to_numpy(float)
        rng = np.random.default_rng(38)
        br = []
        for _ in range(300):
            s = T[rng.integers(0, len(T), len(T))].sum(axis=0)
            br.append((s[0] / s[1]) / (s[2] / s[3]) if s[1] > 0 and s[2] > 0 else np.nan)
        rse = np.nanstd(br)
        rec(3, "couple_years_period", lab, "w", "P(w|h)-P(w|not h)", *est["h"], n=inf["n"])
        rec(3, "couple_years_period", lab, "w", "ratio (p vs 1)", p1 / p0, rse, pv(p1 / p0 - 1, rse), n=inf["n"])
        rows.append((lab, [f"{inf['n']:,}", f"{int(q['h'].sum()):,}", f"{p1:.3f}", f"{p0:.4f}", cell(*est["h"]),
                           f"{p1 / p0:.2f}{stars(pv(p1 / p0 - 1, rse))} ({rse:.2f}; p vs 1="
                           f"{'<0.001' if pv(p1 / p0 - 1, rse) < 0.001 else f'{pv(p1 / p0 - 1, rse):.3f}'})"]))
    md += ["### 3c. Couple-year joint-loss probabilities by period", "",
           "25's couple-years (consecutive interviews of the same couple, both working in the earlier year). "
           "Difference: OLS of w on h, clustered; ratio s.e. from 300 bootstrap draws of families, stars / p against "
           "a ratio of 1. P(w|h), P(w|not h) "
           "are sample means.", "",
           md_table(["Couple-years", "Husband displaced", "P(w | h)", "P(w | not h)", "Difference (OLS)", "Ratio"],
                    [("", rows)]), ""]
    print("item 3 done", flush=True)

    # ============================================================ 4. food
    Qf0 = P[P["ev"].between(1984, 2021) & P["w0"].notna()].dropna(subset=["J"]).copy()
    FP = [("Dual-earner couples (wife employed at baseline)", lambda q: q[q["wemp0"] == 1]),
          ("All married couples", lambda q: q)]
    YF = [("food", "Food spending (2000 $)"), ("lfood", "Log food spending"), ("f_home", "Food at home (2000 $)"),
          ("f_away", "Food away from home (2000 $)")]
    FR, FBE = {}, {}
    for pname, f in FP:
        q = f(Qf0)
        for y, _ in YF:
            b, V, xs, info = es_inter(q, y)
            T = inter_terms(b, V, xs, info, [0, 1, 2])
            T3 = inter_terms(b, V, xs, info, [1, 2, 3])
            net, ninf = es_plain(q, y)
            FR[(pname, y)] = (T, T3, info, net, ninf)
            if y in ("food", "lfood"):
                FBE[(pname, y)] = by_e(b, V, xs, info)
                for e, TT in FBE[(pname, y)].items():
                    for k in ("gross", "j1_vs_c0", "jt_minus_single"):
                        rec(4, "food_by_e", pname, y, f"e={e:+d}:{k}", *TT[k])
            for k in ("gross", "own", "trip", "j1_vs_c0", "jt_minus_single"):
                rec(4, "food_mean_0..2", pname, y, k, *T[k], n=info["n"], P1=info["P1"], treated=info["units"],
                    treated_J1=info["n_t1"])
                rec(4, "food_mean_1..3", pname, y, k, *T3[k], n=info["n"])
            rec(4, "food_net_plain", pname, y, "mean +1..+3", *net["mean +1..+3"], n=ninf["n"])
        print("food", pname, flush=True)
    fmtf = lambda y, t: (cell if y == "lfood" else big)(*t)
    panels = []
    for pname, _ in FP:
        rows = []
        for e in ES_E:
            rows.append((f"Husband displaced alone, e={e:+d}", [fmtf(y, FBE[(pname, y)][e]["gross"])
                                                                if (pname, y) in FBE else "" for y, _ in YF[:2]]))
        for e in ES_E:
            rows.append((f"Both displaced, e={e:+d}", [fmtf(y, FBE[(pname, y)][e]["j1_vs_c0"]) for y, _ in YF[:2]]))
        panels.append((pname + " (event-time coefficients)", rows))
    md += ["## 4. Food spending around single and joint job loss (validation, not a target)", "",
           "19's stacked design, event years 1984-2021, married at baseline, J defined as in section 1. Interaction "
           "model: 'husband displaced alone' = displaced x e (displaced families whose wife was not displaced vs control "
           "families whose wife was not displaced); 'both displaced' = displaced + wife's own displacement + their "
           "interaction (displaced families whose wife was also displaced in ev-1..ev+1, vs the same controls). Food at "
           "event time e is reported at the interview in early ev+e+1 (e = 0 is the first interview after his job "
           "loss); food kept while the baseline wife is in the family; no food questions in 1988-89 and biennial "
           "interviews after 1997.", "",
           md_table([lab for _, lab in YF[:2]], panels, [("Fixed effects", ["father x stack, calendar year x stack"] * 2)]),
           ""]
    panels = []
    for pname, _ in FP:
        rows = []
        for k, lab in (("gross", "Husband displaced alone (displaced x e)"), ("own", "Wife's own displacement (controls)"),
                       ("trip", "Displaced x wife's own displacement"),
                       ("j1_vs_c0", "Derived: both displaced"), ("jt_minus_single", "Derived: both - husband alone")):
            rows.append((lab + ", mean e = 0..2", [fmtf(y, FR[(pname, y)][0][k]) for y, _ in YF]))
        for k, lab in (("gross", "Husband displaced alone"), ("j1_vs_c0", "Both displaced"),
                       ("jt_minus_single", "Both - husband alone")):
            rows.append((lab + ", mean e = 1..3", [fmtf(y, FR[(pname, y)][1][k]) for y, _ in YF]))
        rows.append(("All displaced (plain event study), mean e = 1..3",
                     [fmtf(y, FR[(pname, y)][3]["mean +1..+3"]) for y, _ in YF]))
        rows.append(("Treated mean at e = -2, -1: alone / both",
                     [f"{FR[(pname, y)][2]['pre_t0']:,.2f} / {FR[(pname, y)][2]['pre_t1']:,.2f}" for y, _ in YF]))
        rows.append(("Displaced (both displaced) / N / clusters",
                     [f"{FR[(pname, y)][2]['units']:,} ({FR[(pname, y)][2]['n_t1']:,}) / {FR[(pname, y)][2]['n']:,} / "
                      f"{FR[(pname, y)][2]['clusters']:,}" for y, _ in YF]))
        panels.append((pname, rows))
    md += ["### 4b. Means over event years", "", md_table([lab for _, lab in YF], panels,
                                                          [("Fixed effects", ["father x stack, calendar year x stack"] * 4)]),
           "", "![food](psid_jl_food_es.png)", "", "Food items by wave (data check):", "",
           "| Wave | Items | Time-unit codes (1994-97) |", "|---|---|---|"]
    for _, r in FD["found"].iterrows():
        md.append(f"| {r['wave']} | {r['items']} | {r['units']} |")
    fm = F.groupby("wave")["food"].median()
    md += ["", "Median real family food spending by wave (2000 $): " +
           ", ".join(f"{w} {v:,.0f}" for w, v in fm.items()) + ".", ""]

    # ============================================================ figures
    figures(BYE, NET, Q, FBE, CL)
    md += summary(INT, NET, LEN, CL, mar, DIPR, W3, DEC, sh, shse, PR, pdiff, FR, covtab, NS)
    pd.DataFrame(ROWS).to_csv(OUT / "psid_joint_loss_checks.csv", index=False)
    (OUT / "psid_joint_loss_checks.md").write_text("\n".join(md), encoding="utf-8")
    print("written", flush=True)


def figures(BYE, NET, Q, FBE, CL):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ink, mut, grid = "#1f1e1c", "#52514e", "#e6e5e0"
    C_NET, C_G, C_J = "#3d3c39", "#2a78d6", "#eb6834"
    ee = np.array(sorted(ES_E + [-2]))

    def series(get):
        b = np.array([0.0 if e == -2 else get(e)[0] for e in ee])
        s = np.array([0.0 if e == -2 else get(e)[1] for e in ee])
        return b, s

    def style(ax, ylab):
        ax.axhline(0, color=mut, linewidth=0.8)
        ax.axvline(-0.5, color="#b0afa8", linewidth=0.8, linestyle=":")
        ax.set_xticks(ee)
        ax.tick_params(labelsize=9, colors=mut)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        ax.grid(axis="y", color=grid, linewidth=0.6)
        ax.set_ylabel(ylab, fontsize=9.5, color=mut)
        ax.set_xlabel("Years since the husband's displacement (reference = -2)", fontsize=9.5, color=mut)

    def plot(ax, b, s, col, mk, ls, lab, sh):
        ax.fill_between(ee + sh, b - 1.96 * s, b + 1.96 * s, color=col, alpha=0.10, linewidth=0)
        ax.plot(ee + sh, b, color=col, marker=mk, markersize=5, linewidth=2, linestyle=ls, label=lab)

    # ---- gross vs net (all wives)
    pname = "All wives present at baseline"
    for out, paper in ((OUT / "psid_jl_gross_net_es.png", False), (PAPER / "fig_gross_net_awe", True)):
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
        for ax, (y, ylab) in zip(axes, (("w_hrs", "Wife's annual hours"), ("w_emp", "Wife employed (share)"))):
            net = NET[(pname, y)][0]
            bn, sn = series(lambda e: net[f"e={e:+d}"])
            bg, sg = series(lambda e: BYE[(pname, y)][e]["gross"])
            bj, sj = series(lambda e: BYE[(pname, y)][e]["j1_vs_c0"])
            plot(ax, bn, sn, C_NET, "D", "-", "Net: all displaced families", -0.15)
            plot(ax, bg, sg, C_G, "o", "-", "Gross: wife not displaced", 0.0)
            plot(ax, bj, sj, C_J, "s", "--", "Wife also displaced (ev-1..ev+1)", 0.15)
            style(ax, ylab)
        axes[0].legend(frameon=False, fontsize=9, loc="lower left")
        if not paper:
            fig.suptitle("Wife's labor supply after the husband's displacement: net, gross, and joint job loss "
                         "(PSID, stacked event study, 95% CI)", fontsize=11, color=ink)
        fig.tight_layout()
        if paper:
            fig.savefig(str(out) + ".pdf", facecolor="white")
            fig.savefig(str(out) + ".png", dpi=200, facecolor="white")
        else:
            fig.savefig(out, dpi=150, facecolor="white")
        plt.close(fig)
    # ---- food single vs joint (dual earners)
    pname = "Dual-earner couples (wife employed at baseline)"
    for out, paper in ((OUT / "psid_jl_food_es.png", False), (PAPER / "fig_food_single_joint", True)):
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
        for ax, (y, ylab) in zip(axes, (("lfood", "Log real food spending"), ("food", "Real food spending (2000 $)"))):
            bg, sg = series(lambda e: FBE[(pname, y)][e]["gross"])
            bj, sj = series(lambda e: FBE[(pname, y)][e]["j1_vs_c0"])
            plot(ax, bg, sg, C_G, "o", "-", "Husband displaced alone", -0.08)
            plot(ax, bj, sj, C_J, "s", "--", "Both spouses displaced", 0.08)
            style(ax, ylab)
        axes[0].legend(frameon=False, fontsize=9, loc="lower left")
        if not paper:
            fig.suptitle("Food spending around single and joint job loss, dual-earner couples (PSID, 95% CI; "
                         "e = 0 is the first interview after his job loss)", fontsize=11, color=ink)
        fig.tight_layout()
        if paper:
            fig.savefig(str(out) + ".pdf", facecolor="white")
            fig.savefig(str(out) + ".png", dpi=200, facecolor="white")
        else:
            fig.savefig(out, dpi=150, facecolor="white")
        plt.close(fig)
    # ---- closures vs layoffs, marriage and father's income
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    for ax, (y, ylab) in zip(axes, (("hlab", "Father's labor income (2000 $)"),
                                    ("bw_present", "Still with baseline wife"))):
        for j, (dn, col, mk, ls) in enumerate((("Closures only", C_G, "o", "-"), ("Layoffs only", C_J, "s", "--"))):
            est = CL[(dn, "All", y)][0]
            b, s = series(lambda e: est[f"e={e:+d}"])
            plot(ax, b, s, col, mk, ls, dn, (j - 0.5) * 0.15)
        style(ax, ylab)
    axes[0].legend(frameon=False, fontsize=9, loc="lower left")
    fig.suptitle("Father's displacement by type: closures vs layoffs (PSID, all fathers, 95% CI)", fontsize=11,
                 color=ink)
    fig.tight_layout()
    fig.savefig(OUT / "psid_jl_closures_es.png", dpi=150, facecolor="white")
    plt.close(fig)


def summary(INT, NET, LEN, CL, mar, DIPR, W3, DEC, sh, shse, PR, pdiff, FR, covtab, NS):
    c = lambda t, d=3: cell(*t, d=d)
    a = "All wives present at baseline"
    I, Ie = INT[(a, "w_hrs")], INT[("Wife employed at baseline", "w_hrs")]
    y5, y6 = INT[("Youngest child 0-5", "w_hrs")], INT[("Youngest child 6-17", "w_hrs")]
    e1, i1, e2, i2, tot = DEC["All"]
    clm = lambda r: c(CL[("Closures only", r, "bw_present")][0]["mean +1..+3"])
    lom = lambda r: c(CL[("Layoffs only", r, "bw_present")][0]["mean +1..+3"])
    fd = "Dual-earner couples (wife employed at baseline)"
    out = ["## 5. Summary", "",
           f"1. Gross vs net (event years 1984-2021, wives present at baseline; J defined for {covtab[1][0]:.0%} of "
           f"displaced families). Wife's hours, mean of years +1..+3: net {c(NET[(a, 'w_hrs')][0]['mean +1..+3'], 0)}; "
           f"gross (wife not displaced) {c(I[0]['gross'], 0)}; wife also displaced vs controls whose wife was not "
           f"displaced {c(I[0]['j1_vs_c0'], 0)}; implied net {c(I[0]['net_implied'], 0)} = gross + joint-loss offset "
           f"{c(I[0]['offset'], 0)} (P1 {I[1]['P1']:.3f}, P0 {I[1]['P0']:.3f}). Wives employed at baseline: gross "
           f"{c(Ie[0]['gross'], 0)}, offset {c(Ie[0]['offset'], 0)}, net {c(NET[('Wife employed at baseline', 'w_hrs')][0]['mean +1..+3'], 0)}. "
           f"Youngest 0-5: gross {c(y5[0]['gross'], 0)}, net {c(NET[('Youngest child 0-5', 'w_hrs')][0]['mean +1..+3'], 0)}; "
           f"6-17: gross {c(y6[0]['gross'], 0)}, net {c(NET[('Youngest child 6-17', 'w_hrs')][0]['mean +1..+3'], 0)}. "
           f"Employment: gross {c(INT[(a, 'w_emp')][0]['gross'])}, offset {c(INT[(a, 'w_emp')][0]['offset'])}. "
           f"Net by period (all wives / youngest 0-5): 1968-2022 {c(NS[('Table 1 sample: event years 1968-2022', 'all', 'w_hrs')][0], 0)} / "
           f"{c(NS[('Table 1 sample: event years 1968-2022', 'youngest 0-5', 'w_hrs')][0], 0)}; 1968-1983 "
           f"{c(NS[('Event years 1968-1983', 'all', 'w_hrs')][0], 0)} / {c(NS[('Event years 1968-1983', 'youngest 0-5', 'w_hrs')][0], 0)}; "
           f"1984-2021 {c(NS[('Event years 1984-2021, all', 'all', 'w_hrs')][0], 0)} / "
           f"{c(NS[('Event years 1984-2021, all', 'youngest 0-5', 'w_hrs')][0], 0)}. Reading: the joint loss lowers the "
           f"average wife's hours by {-I[0]['offset'][0]:.0f} a year relative to the gross response (P1 - P0 = "
           f"{100 * (I[1]['P1'] - I[1]['P0']):.1f} points; a displaced wife works {-I[0]['own'][0]:.0f} hours less "
           f"absent his job loss and {-I[0]['j1_vs_c0'][0]:.0f} less with it); after 1984 the gross response is small "
           "except with a child under 6, so the back-of-envelope '85-90 gross vs 51 net' mixes the pre-1984 net with a "
           "1984+ offset: in the years where both are measured, net and gross are small and the offset is a large "
           "share of the gross response.",
           "",
           f"2. Closures only, still with baseline wife (mean +1..+3): Black {clm('Black')}, White {clm('White')}; "
           f"layoffs only: Black {lom('Black')}, White {lom('White')}. Pre-displacement dip in the father's labor "
           f"income at e = -1: main {c(DIPR[('Main: all', 'hlab')][0]['e=-1'], 0)}, dated reports "
           f"{c(DIPR[('Main: dated reports', 'hlab')][0]['e=-1'], 0)}, undated "
           f"{c(DIPR[('Main: undated reports (year before the interview)', 'hlab')][0]['e=-1'], 0)}; hours "
           f"{c(DIPR[('Main: all', 'hh')][0]['e=-1'], 0)}; hourly earnings {c(DIPR[('Main: all', 'hourly')][0]['e=-1'])}.",
           "",
           f"3. Placebo window (main sample): W {c(W3[('All', 'main_W')][0]['treat'])}, PL "
           f"{c(W3[('All', 'main_PL')][0]['treat'])}, difference {c(W3[('All', 'main_D')][0]['treat'])}, future "
           f"placebo in PL {c(W3[('All', 'main_PL')][0]['pseudo'])}. Decomposition: permanent pi {c(e1['ever'])}, "
           f"contemporaneous c {c(e1['tw'])}, share permanent {c((sh, shse))}. Periods (window sample): "
           + "; ".join(f"{k} {c(v['est']['treat'])}" for k, v in PR.items()) + f"; 2000-21 minus 1984-89 {c(pdiff)}.",
           "",
           f"4. Food, dual earners, mean e = 0..2: husband alone, log {c(FR[(fd, 'lfood')][0]['gross'])}, level "
           f"{c(FR[(fd, 'food')][0]['gross'], 0)}; both displaced, log {c(FR[(fd, 'lfood')][0]['j1_vs_c0'])}, level "
           f"{c(FR[(fd, 'food')][0]['j1_vs_c0'], 0)}; difference log {c(FR[(fd, 'lfood')][0]['jt_minus_single'])}.",
           ""]
    return out


if __name__ == "__main__":
    main()
