r"""Her displacement and the break-up of the couple: robustness of IGE/64's M3 result (PSID, 2026-10-19).

Paper A headline candidate (IGE/64, M3): the wife's own displacement lowers 'still with baseline husband' by
-0.046*** in years 1-3 and -0.090*** in years 4-6, at least as much as his displacement does. This script checks it.
Imports 64.SeparationUIAndHerLoss.py (and through it 19 / 9) read only; nothing existing is edited or rerun.

Reads (read only): data/psid_person_year.pkl, psid_displacement.pkl (19), correlated_shocks_wife_disp.pkl (23),
sep_ui_femhead_reports.pkl (64's cache), the raw PSID family files (hours via 9.family; split-off indicator and
family composition change, 1984-2023 waves) and the individual file (sequence numbers, 1984-2023 waves).
Writes (aggregates only):
  data/her_loss_who_cache.pkl         cache: split-off indicator by family-wave, sequence numbers (git-ignored)
  output/her_loss_robustness.csv      every estimate
  output/her_loss_robustness.md       tables

DESIGN = 64's M3 (19's stacked event study, roles reversed): wives of male heads with a child 0-17 and positive own
hours at baseline (last observed of ev-1, ev-2); treated = her first displacement (closure or layoff / firing) in ev;
clean controls = not displaced herself up to ev+6; person x stack and calendar year x stack FE; reference e = -2;
CR1 s.e. clustered by 1968 family; normal p-values. Target sample: events 1984-2021, outcome years <= 2021.
Outcome 'still with baseline husband' (bh_present). Averages: years 1-3, 4-6, 1-6 (equal weights on e).

1. Her vs his. 64's two designs stacked in one regression (design-specific unit and cell FE, design-specific event
   dummies, one cluster covariance by 1968 family, so couples in both designs are handled); differences with p-values.
   (a) samples as in 64; (b) common population: both spouses with positive hours at baseline (her design: his hours
   > 0; his design: her hours > 0).
2. Selection. (a) Closures vs layoffs / firings as separate treated dummies in one regression (common controls), her
   and his designs, years 1-3, 4-6, 1-6; difference. (b) Baseline balance, displaced vs control stacks (unit level,
   difference within event-year stacks, clustered). (c) Pre-trends of her hours and her earnings (not mechanical,
   unlike the marriage outcome). (d) Main estimate with baseline characteristics x event time (her hours, earnings,
   age, age^2; his earnings and hours; children, age of the youngest; observed marriage duration bins; race).
3. Joint loss. 'Joint' = his displacement (19's male-head reports) in ev-1..ev+1 of hers. (a) her design without the
   joint couples; (b) and controls also free of his displacement in ev-3..ev+6; (c) her-alone and joint as separate
   treated dummies (controls free of both); (d) his design: his-alone vs joint (wife displaced in ev-1..ev+1 by the
   wife / female-head reports; controls free of her displacement in ev-3..ev+6).
4. Heterogeneity. Race (head's race at baseline); her share of the couple's labor earnings at baseline (above / below
   the treated median; >= 0.40 vs < 0.40). Group-specific cells and dummies in one regression (= separate regressions
   point-wise), difference with the joint clustered covariance.
5. Who leaves. The PSID has no reason-for-separation item. For the first year after baseline in which she is not with
   the baseline husband: his sequence number 81-89 (died); otherwise her family's split-off indicator (2 / 4 = she
   moved out into a split-off family; 1 / 3 = she stayed in the continuing family, so he moved out). Outcomes 'separated,
   route k' (the routes add up to 1 - bh_present) in the same event study. Also attrition: her being observed as wife or
   head, and the outcome filled from his side (19's male-head panel: he is a head with another or no wife -> 0).
   Symmetric observation (5b): a displaced wife must be interviewed (as wife or female head) to report the job end,
   a control need not be; both groups are restricted to women observed at the first interview year >= ev.

CAVEAT. bh_present equals 1 at the baseline years by construction, so its pre-period coefficients are mechanical and
there is no placebo test for this outcome; the pre-trends in her hours / earnings and the balance table are the
available checks on selection.
"""
import importlib.util
import os
import warnings

os.environ.setdefault("OMP_NUM_THREADS", "4")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "4")
os.environ.setdefault("MKL_NUM_THREADS", "4")

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from common import DATA, OUT, HERE, stars  # noqa: E402

warnings.simplefilter("ignore", FutureWarning)
warnings.simplefilter("ignore", RuntimeWarning)


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


P64 = _load("p64", "64.SeparationUIAndHerLoss.py")
P19, psid9 = P64.P19, P64.psid9
psid1 = P19.psid1
ES_E = P19.ES_E
EV_LO, EV_HI, Y_HI = P64.EV_LO, P64.EV_HI, P64.Y_HI
pv, cell = P64.pv, P64.cell
ROWS = []
W = {"1-3": {1: 1 / 3, 2: 1 / 3, 3: 1 / 3}, "4-6": {4: 1 / 3, 5: 1 / 3, 6: 1 / 3},
     "1-6": {e: 1 / 6 for e in range(1, 7)}}


# ---------------------------------------------------------------- estimator with treated sub-groups
def est(q, y, tg=None, cg=None, extra=(), tag="", sample="", outcome=None):
    """Stacked event study. tg: column naming the treated sub-group (common controls); cg: column splitting the
    whole sample (cells x group, i.e. separate regressions in one covariance). Returns a result dict."""
    q = q.dropna(subset=[y]).copy()
    if cg is not None:
        q = q.dropna(subset=[cg])
        q["cell"] = pd.factorize(q["cell"].astype(str) + "|" + q[cg].astype(str))[0]
        q["grp"] = q[cg].astype(str)
    elif tg is not None:
        q["grp"] = np.where(q["treat"] == 1, q[tg].astype(str), "ctrl")
    else:
        q["grp"] = "all"
    groups = sorted(q.loc[q["treat"] == 1, "grp"].unique())
    xs = []
    for g in groups:
        for e in ES_E:
            c = f"d|{g}|{e}"
            q[c] = ((q["e"] == e) & (q["treat"] == 1) & (q["grp"] == g)).astype(float)
            xs.append(c)
    xs += list(extra)
    b, V, info = P64.fit(q, y, xs)
    out = dict(info=info, groups=groups, b=b, V=V, xs=xs, n_tr={}, n_ct={})
    for g in groups:
        out["n_tr"][g] = int(q.loc[(q["treat"] == 1) & (q["grp"] == g), "unit"].nunique())
        out["n_ct"][g] = int(q.loc[(q["treat"] == 0) & (q["grp"] == g), "unit"].nunique()) if cg else \
            info["controls"]
        for e in ES_E:
            i = xs.index(f"d|{g}|{e}")
            out[(g, f"e={e:+d}")] = (b[i], np.sqrt(V[i, i]))
        for k, w in W.items():
            out[(g, k)] = P64.comb(b, V, xs, {f"d|{g}|{e}": v for e, v in w.items()})
            ROWS.append(dict(block=tag, sample=sample, outcome=outcome or y, group=g, term=f"mean {k}",
                             coef=out[(g, k)][0], se=out[(g, k)][1], p=pv(*out[(g, k)]), n=info["n"],
                             treated=out["n_tr"][g], controls=out["n_ct"][g], clusters=info["clusters"]))
        for e in (-3, -1):
            ROWS.append(dict(block=tag, sample=sample, outcome=outcome or y, group=g, term=f"e={e:+d}",
                             coef=out[(g, f"e={e:+d}")][0], se=out[(g, f"e={e:+d}")][1],
                             p=pv(*out[(g, f"e={e:+d}")]), n=info["n"], treated=out["n_tr"][g],
                             controls=out["n_ct"][g], clusters=info["clusters"]))
    return out


def diff(r, g1, g2, k, tag="", sample="", outcome=""):
    """(g1 - g2) for average k with the joint covariance."""
    w = {f"d|{g1}|{e}": v for e, v in W[k].items()}
    w.update({f"d|{g2}|{e}": -v for e, v in W[k].items()})
    b, se = P64.comb(r["b"], r["V"], r["xs"], w)
    ROWS.append(dict(block=tag, sample=sample, outcome=outcome, group=f"{g1} - {g2}", term=f"mean {k}", coef=b,
                     se=se, p=pv(b, se), n=r["info"]["n"], clusters=r["info"]["clusters"]))
    return b, se


def md_table(header, rows):
    out = ["| | " + " | ".join(header) + " |", "|---|" + "---:|" * len(header)]
    out += [f"| {lab} | " + " | ".join(v) + " |" for lab, v in rows]
    return "\n".join(out)


def c3(x):
    return cell(*x)


# ---------------------------------------------------------------- data
def her_all_years(py, fam):
    """every (pid, year) of her main displacement, calendar 1983+ (wife reports + female-head reports)."""
    wd = pd.read_pickle(DATA / "correlated_shocks_wife_disp.pkl")
    r = P64.femhead_reports(fam)
    fh = py[py["head"] & (py["female"] == 1)][["wave", "int", "pid"]].drop_duplicates(["wave", "int"])
    r = r.merge(fh, on=["wave", "int"], how="inner")
    x = pd.concat([r.loc[r["main"], ["pid", "year"]], wd.loc[wd["main"] == 1, ["pid", "year"]]])
    x = x.astype({"pid": np.int64, "year": int}).drop_duplicates()
    return x[x["year"] >= 1983]


def women_panel_x(py, fam):
    w = P64.women_panel(py, fam)
    ex = py[["pid", "wave", "earn", "hlab"]].drop_duplicates(["pid", "wave"])
    w = w.merge(ex, on=["pid", "wave"], how="left")
    w["h_earn"] = w["hlab"].where(w["wife"])
    k = py[py["child"] & py["age"].between(0, 17)].groupby(["wave", "int"])["age"].min().rename("young")
    w = w.merge(k.reset_index(), on=["wave", "int"], how="left")
    s = w[w["h_pid"].notna()]
    first = s.groupby(["pid", "h_pid"])["year"].min().rename("m_first").reset_index()
    w = w.merge(first, on=["pid", "h_pid"], how="left")
    w["mdur"] = w["year"] - w["m_first"]
    w["mcens"] = (w["m_first"] == w.groupby("pid")["year"].transform("min")).astype(float)
    return w.sort_values(["pid", "year"]).reset_index(drop=True)


def her_stacks_x(w, first):
    """64.her_stacks (kind 'main') with baseline characteristics and the closure flag kept."""
    fm = w["pid"].map(first["main"]).fillna(9999)
    fs = w["pid"].map(first["strict"]).fillna(9999)
    b = pd.concat([w.assign(ev=w["year"] + 1, pri=0), w.assign(ev=w["year"] + 2, pri=1)])
    b = b.assign(fm=pd.concat([fm, fm]).to_numpy(), fs=pd.concat([fs, fs]).to_numpy())
    b = b.sort_values(["pid", "ev", "pri"]).drop_duplicates(["pid", "ev"]).reset_index(drop=True)
    b = b[(b["nkid"] > 0) & (b["own_hrs"] > 0) & b["h_pid"].notna() & b["ev"].between(EV_LO, EV_HI)]
    tr = b["fm"] == b["ev"]
    ct = b["fm"] > b["ev"] + 6
    b = b[tr | ct].assign(treat=tr[tr | ct].astype(int))
    b["type"] = np.where(b["treat"] == 1, np.where(b["fs"] == b["ev"], "closure", "layoff"), "ctrl")
    base = b[["pid", "ev", "treat", "type", "hrace", "h_pid", "year", "own_hrs", "earn", "h_earn", "h_hrs", "age",
              "nkid", "young", "mdur", "mcens"]].rename(columns={
                  "h_pid": "h0", "year": "by", "own_hrs": "hrs0", "earn": "earn0", "h_earn": "hearn0", "h_hrs": "hhrs0",
                  "age": "age0", "nkid": "nkid0", "young": "young0", "mdur": "mdur0", "mcens": "mcens0"})
    p = base.merge(w[["pid", "fam68", "year", "h_pid", "own_hrs", "h_hrs", "earn", "wave", "int"]], on="pid")
    p = p[(p["year"] >= p["ev"] - 3) & (p["year"] <= p["ev"] + 6) & (p["year"] <= Y_HI)]
    p["e"] = p["year"] - p["ev"]
    p["bh_present"] = (p["h_pid"] == p["h0"]).astype(float)
    p["unit"] = pd.factorize(p["pid"].astype(np.int64) * 10000 + p["ev"].astype(np.int64))[0]
    p["cell"] = pd.factorize(p["year"].astype(np.int64) * 10000 + p["ev"].astype(np.int64))[0]
    p["h0"] = p["h0"].astype(np.int64)
    return p.reset_index(drop=True)


def window_flags(U, key, years, lo, hi, name):
    """U: units (unit, key, ev). years: (pid, year) of displacement. flag = any year in [ev+lo, ev+hi]."""
    M = U[["unit", key, "ev"]].merge(years.rename(columns={"pid": key}), on=key, how="inner")
    M = M[(M["year"] >= M["ev"] + lo) & (M["year"] <= M["ev"] + hi)]
    return U["unit"].isin(M["unit"]).astype(int).rename(name)


def who_cache():
    fn = DATA / "her_loss_who_cache.pkl"
    if fn.exists():
        return pd.read_pickle(fn)
    rows = []
    for wv in [x for x in psid1.WAVES if x >= 1984]:
        folder = psid1.FAM / (f"fam{wv}" if wv < 1994 else f"fam{wv}er")
        base = next(f for f in folder.glob("*.do") if "formats" not in f.name).with_suffix("")
        pos, labs = psid1.layout(base.with_suffix(".do"))
        idv = labs[1][0]
        so = next(v for v, lab in labs if "SPLITOFF INDICATOR" in lab.upper())
        f = psid1.read(base, [idv, so], pos)
        rows.append(pd.DataFrame({"wave": wv, "int": f[idv], "splitoff": f[so]}))
    fam_so = pd.concat(rows, ignore_index=True)
    pos, labs = psid1.layout(psid1.IND.with_suffix(".do"))
    seqv = {}
    for v, lab in labs:
        if lab.startswith("SEQUENCE NUMBER"):
            yy = int(lab[-2:])
            seqv[1900 + yy if yy >= 68 else 2000 + yy] = v
    seqv = {k: v for k, v in seqv.items() if k >= 1984}
    d = psid1.read(psid1.IND, ["ER30001", "ER30002", *seqv.values()], pos)
    d["pid"] = d["ER30001"] * 1000 + d["ER30002"]
    seq = d.melt(id_vars="pid", value_vars=list(seqv.values()), var_name="v", value_name="seq")
    seq["wave"] = seq["v"].map({v: k for k, v in seqv.items()})
    seq = seq[seq["seq"] > 0][["pid", "wave", "seq"]]
    out = dict(fam_so=fam_so, seq=seq)
    pd.to_pickle(out, fn)
    return out


# ---------------------------------------------------------------- balance
def balance(U, x):
    """treated - control difference of x within event-year stacks, CR1 by fam68 (unit level)."""
    u = U.dropna(subset=[x]).copy()
    g = pd.factorize(u["ev"])[0]
    A = P19.demean(np.column_stack([u[x].to_numpy(float), u["treat"].to_numpy(float)]), [(g, g.max() + 1)])
    yv, t = A[:, 0], A[:, 1]
    b = (t @ yv) / (t @ t)
    res = yv - b * t
    c = pd.factorize(u["fam68"])[0]
    G = c.max() + 1
    s = np.bincount(c, weights=t * res, minlength=G)
    n = len(u)
    V = G / (G - 1) * (n - 1) / (n - 1 - (g.max() + 1)) * (s @ s) / (t @ t) ** 2
    return (u.loc[u["treat"] == 1, x].mean(), u.loc[u["treat"] == 0, x].mean(), b, np.sqrt(V),
            int((u["treat"] == 1).sum()), int((u["treat"] == 0).sum()))


def main():
    OUT.mkdir(exist_ok=True)
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    fam = psid9.family()
    d = pd.read_pickle(DATA / "psid_displacement.pkl")
    m = P19.men_panel(py, fam)
    first, src = P64.her_events(py, fam)
    w = women_panel_x(py, fam)
    H = her_stacks_x(w, first)
    print("panels built", flush=True)
    his_years = d.loc[d["main"] == 1, ["pid", "year"]].astype({"pid": np.int64, "year": int})
    her_years = her_all_years(py, fam)

    md = ["# Her displacement and separation: robustness of IGE/64 (M3), PSID", "",
          "Built by `65.HerLossRobustness.py` (2026-10-19); design in its docstring. 64's M3 design: wives of male "
          "heads, baseline with a child 0-17 and positive own hours; treated = her first displacement (closure or "
          "layoff / firing) in ev; clean controls not displaced herself to ev+6; person x stack and calendar year x "
          "stack FE; reference e = -2; s.e. clustered by 1968 family; target sample (events 1984-2021, outcome years "
          "<= 2021). Outcome 'still with baseline husband' unless stated. *** p<0.01, ** p<0.05, * p<0.1; every cell: "
          "coefficient*** (s.e.; p). Averages of the event-time coefficients over years 1-3, 4-6, 1-6.", "",
          "**Caveat.** The outcome equals 1 at baseline by construction: no pre-period placebo for it. Selection is "
          "checked with the closures, the balance table, the pre-trends in her hours and earnings, and baseline "
          "controls x event time.", ""]

    # ============================================================ 0. reproduce 64
    r0 = est(H, "bh_present", tag="0 main", sample="her design, all")
    md += ["## 0. Reproduction of IGE/64", "",
           f"Years 1-3: {c3(r0[('all', '1-3')])}; years 4-6: {c3(r0[('all', '4-6')])}; years 1-6: "
           f"{c3(r0[('all', '1-6')])}. N = {r0['info']['n']:,} person-years, {r0['n_tr']['all']:,} displaced wives, "
           f"{r0['info']['controls']:,} control stacks, {r0['info']['clusters']:,} clusters (64: -0.046*** / -0.090***, "
           "1,205 displaced wives).", ""]
    print("0", c3(r0[("all", "1-3")]), flush=True)

    # ============================================================ 1. her vs his, one regression
    P0 = P19.stacks(m, d, "main")
    P0 = P0[P0["w0"].notna() & P0["ev"].between(EV_LO, EV_HI) & (P0["year"] <= Y_HI)].copy()
    P0["w0"] = P0["w0"].astype(np.int64)
    hb = H[["unit", "hhrs0"]].drop_duplicates("unit")

    def joint(qh, qm):
        a = qh[["unit", "cell", "fam68", "treat", "e", "bh_present"]].rename(columns={"bh_present": "stay"})
        b = qm[["unit", "cell", "fam68", "treat", "e", "bw_present"]].rename(columns={"bw_present": "stay"})
        a = a.assign(design="her", unit=a["unit"].astype(str) + "h", cell=a["cell"].astype(str) + "h")
        b = b.assign(design="his", unit=b["unit"].astype(str) + "m", cell=b["cell"].astype(str) + "m")
        q = pd.concat([a, b], ignore_index=True)
        q["unit"] = pd.factorize(q["unit"])[0]
        q["cell"] = pd.factorize(q["cell"])[0]
        return q

    J = {}
    J["a"] = joint(H, P0)
    J["b"] = joint(H[H["unit"].isin(hb.loc[hb["hhrs0"] > 0, "unit"])], P0[P0["wh0"] > 0])
    rows = []
    for key, lab in (("a", "Samples as in IGE/64"), ("b", "Both spouses with positive hours at baseline")):
        r = est(J[key], "stay", tg="design", tag="1 her vs his", sample=lab)
        for k in ("1-3", "4-6", "1-6"):
            dd = diff(r, "her", "his", k, tag="1 her vs his", sample=lab, outcome="stay")
            rows.append((f"{lab}: years {k}", [c3(r[("her", k)]), c3(r[("his", k)]), c3(dd)]))
        rows.append((f"{lab}: displaced / clusters (joint regression)",
                     [f"{r['n_tr']['her']:,}", f"{r['n_tr']['his']:,}", f"{r['info']['clusters']:,}"]))
        print("1", key, c3(diff(r, "her", "his", "1-3")), flush=True)
    md += ["## 1. Her displacement vs his: one regression", "",
           "Her design (outcome 'still with baseline husband') and his (IGE/19 / 64: 'still with baseline wife') "
           "stacked in one regression with design-specific unit and cell FE and event dummies, one covariance "
           "clustered by 1968 family (a couple can enter both designs). N person-years: (a) "
           f"{J['a'].shape[0]:,}; (b) {J['b'].shape[0]:,}.", "",
           md_table(["Her displacement", "His displacement", "Her - his"], rows), ""]

    # ============================================================ 2a. closures vs layoffs
    rows = []
    rc = est(H, "bh_present", tg="type", tag="2a closure vs layoff", sample="her design")
    t_his = d.loc[d["main"] == 1].sort_values(["pid", "year"]).drop_duplicates("pid")[["pid", "year", "strict"]]
    P0 = P0.merge(t_his.rename(columns={"year": "ev", "strict": "clos"}), on=["pid", "ev"], how="left")
    P0["type"] = np.where(P0["treat"] == 1, np.where(P0["clos"] == 1, "closure", "layoff"), "ctrl")
    rm = est(P0, "bw_present", tg="type", tag="2a closure vs layoff", sample="his design")
    for lab, r in (("Her displacement", rc), ("His displacement", rm)):
        for k in ("1-3", "4-6", "1-6"):
            dd = diff(r, "closure", "layoff", k, tag="2a closure vs layoff", sample=lab)
            rows.append((f"{lab}: years {k}", [c3(r[("closure", k)]), c3(r[("layoff", k)]), c3(dd)]))
        rows.append((f"{lab}: displaced (closure / layoff)",
                     [f"{r['n_tr']['closure']:,}", f"{r['n_tr']['layoff']:,}", ""]))
    # first stage by type
    for lab, y in (("Her hours", "own_hrs"),):
        r = est(H, y, tg="type", tag="2a closure vs layoff", sample="her design")
        for k in ("1-3", "4-6"):
            rows.append((f"{lab} (her design): years {k}",
                         [cell(*r[("closure", k)], d=0), cell(*r[("layoff", k)], d=0),
                          cell(*diff(r, "closure", "layoff", k, tag="2a", sample="her design", outcome=y), d=0)]))
    md += ["## 2. Selection into displacement", "", "### 2a. Closures vs layoffs / firings (one regression, common "
           "controls)", "", md_table(["Closure", "Layoff / firing", "Closure - layoff"], rows), ""]
    print("2a", c3(rc[("closure", "1-6")]), c3(rc[("layoff", "1-6")]), flush=True)

    # ============================================================ 2b. balance
    U = H.drop_duplicates("unit").copy()
    U["black"] = (U["hrace"] == "Black").astype(float)
    U["earn0k"] = U["earn0"] / 1000
    U["hearn0k"] = U["hearn0"] / 1000
    tot = U["earn0"] + U["hearn0"]
    U["share0"] = (U["earn0"] / tot).where(tot > 0)
    U["mdur0c"] = U["mdur0"]
    U["new2"] = (U["mdur0"] <= 2).astype(float).where(U["mdur0"].notna())
    BAL = [("hrs0", "Her annual hours"), ("earn0k", "Her labor earnings ($000, 2000)"),
           ("hhrs0", "His annual hours"), ("hearn0k", "His labor earnings ($000, 2000)"),
           ("share0", "Her share of couple labor earnings"), ("age0", "Her age"), ("nkid0", "Children 0-17"),
           ("young0", "Age of youngest child"), ("mdur0c", "Years observed with this husband (left-censored)"),
           ("new2", "Observed with him <= 2 years"), ("mcens0", "Spell left-censored (with him from her first year)"),
           ("black", "Black")]
    rows = []
    for x, lab in BAL:
        mt, mc, b, se, nt, nc = balance(U, x)
        ROWS.append(dict(block="2b balance", sample="her design", outcome=x, group="treated - control",
                         term="within-stack difference", coef=b, se=se, p=pv(b, se), treated=nt, controls=nc,
                         mean_treated=mt, mean_control=mc))
        dg = 0 if x in ("hrs0", "hhrs0") else 3
        rows.append((lab, [f"{mt:,.{dg}f}", f"{mc:,.{dg}f}", cell(b, se, d=dg), f"{nt:,} / {nc:,}"]))
    md += ["### 2b. Baseline balance (unit level, baseline year)", "",
           "Difference displaced - control within event-year stacks, clustered by 1968 family. Job tenure is not in "
           "the extracted PSID files used here. Marriage duration is the years observed with this husband (left-"
           "censored at her first PSID year as a wife or head).", "",
           md_table(["Displaced mean", "Control mean", "Difference", "Displaced / control units"], rows), ""]

    # ============================================================ 2c. pre-trends; 2d. controls x event time
    rows = []
    for y, lab, dg in (("own_hrs", "Her annual hours", 0), ("earn", "Her labor earnings (2000 $)", 0),
                       ("h_hrs", "His annual hours (while with her)", 0)):
        r = est(H, y, tag="2c pre-trends", sample="her design")
        rows.append((lab, [cell(*r[("all", "e=-3")], d=dg), cell(*r[("all", "e=-1")], d=dg),
                           cell(*r[("all", "e=+0")], d=dg), cell(*r[("all", "1-3")], d=dg),
                           cell(*r[("all", "4-6")], d=dg)]))
    md += ["### 2c. Pre-trends in her labor market outcomes (reference e = -2)", "",
           md_table(["e = -3", "e = -1", "e = 0", "Years 1-3", "Years 4-6"], rows), ""]

    X = H.merge(U[["unit", "black", "share0"]], on="unit", how="left")
    X["hrs0k"] = X["hrs0"] / 1000
    X["earn0k"] = X["earn0"].clip(upper=X["earn0"].quantile(0.99)) / 10000
    X["hearn0k"] = X["hearn0"].clip(upper=X["hearn0"].quantile(0.99)) / 10000
    X["hhrs0k"] = X["hhrs0"] / 1000
    X["age0c"] = X["age0"] - 35
    X["age0sq"] = X["age0c"] ** 2 / 10
    md_b = pd.cut(X["mdur0"], [-1, 2, 5, 10, 99], labels=False)
    for j in range(4):
        X[f"md{j}"] = (md_b == j).astype(float)
    BX = ["hrs0k", "earn0k", "hearn0k", "hhrs0k", "age0c", "age0sq", "nkid0", "young0", "md1", "md2", "md3", "mcens0",
          "black"]
    extra = []
    for x in BX:
        miss = X[x].isna()
        if miss.any():
            X[f"{x}_m"] = miss.astype(float)
            X[x] = X[x].fillna(0)
            for e in ES_E:
                X[f"cx|{x}_m|{e}"] = (X["e"] == e) * X[f"{x}_m"]
                extra.append(f"cx|{x}_m|{e}")
        for e in ES_E:
            X[f"cx|{x}|{e}"] = (X["e"] == e) * X[x]
            extra.append(f"cx|{x}|{e}")
    rX = est(X, "bh_present", extra=extra, tag="2d controls x event time", sample="her design")
    rX_c = est(X, "bh_present", tg="type", extra=extra, tag="2d controls x event time, by type", sample="her design")
    rows = [(f"Years {k}", [c3(r0[("all", k)]), c3(rX[("all", k)]), c3(rX_c[("closure", k)]),
                            c3(rX_c[("layoff", k)])]) for k in ("1-3", "4-6", "1-6")]
    rows.append(("Displaced wives", [f"{r0['n_tr']['all']:,}", f"{rX['n_tr']['all']:,}",
                                     f"{rX_c['n_tr']['closure']:,}", f"{rX_c['n_tr']['layoff']:,}"]))
    md += ["### 2d. Baseline characteristics x event time", "",
           "Each baseline characteristic of 2b (her hours, earnings, age, age^2; his earnings and hours; children, "
           "age of the youngest; marriage-duration bins 0-2 / 3-5 / 6-10 / 11+ and left-censoring; race; missing "
           "indicators) interacted with every event-time dummy for all units (so controls with the same "
           "characteristics have their own path).", "",
           md_table(["IGE/64 (no controls)", "With controls x e", "With controls: closures",
                     "With controls: layoffs"], rows), ""]
    print("2d", c3(rX[("all", "1-3")]), flush=True)

    # ============================================================ 3. joint loss
    UH = H.drop_duplicates("unit")[["unit", "h0", "ev"]]
    fl = pd.concat([UH["unit"], window_flags(UH, "h0", his_years, -1, 1, "his_near"),
                    window_flags(UH, "h0", his_years, -3, 6, "his_win")], axis=1)
    H2 = H.merge(fl, on="unit", how="left")
    UM = P0.drop_duplicates("unit")[["unit", "w0", "ev"]]
    fm_ = pd.concat([UM["unit"], window_flags(UM, "w0", her_years, -1, 1, "her_near"),
                     window_flags(UM, "w0", her_years, -3, 6, "her_win")], axis=1)
    P2 = P0.merge(fm_, on="unit", how="left")
    H2["jt"] = np.where(H2["his_near"] == 1, "joint", "alone")
    P2["jt"] = np.where(P2["her_near"] == 1, "joint", "alone")
    r3a = est(H2[~((H2["treat"] == 1) & (H2["his_near"] == 1))], "bh_present", tag="3a her alone",
              sample="joint couples dropped")
    r3b = est(H2[~((H2["treat"] == 1) & (H2["his_near"] == 1)) & ~((H2["treat"] == 0) & (H2["his_win"] == 1))],
              "bh_present", tag="3b her alone, clean controls", sample="joint dropped; controls without his loss")
    Hc = H2[~((H2["treat"] == 0) & (H2["his_win"] == 1))]
    r3c = est(Hc, "bh_present", tg="jt", tag="3c her alone vs joint", sample="controls without his loss")
    Pc = P2[~((P2["treat"] == 0) & (P2["her_win"] == 1))]
    r3d = est(Pc, "bw_present", tg="jt", tag="3d his alone vs joint", sample="controls without her loss")
    rows = []
    for k in ("1-3", "4-6", "1-6"):
        rows.append((f"Years {k}", [c3(r3a[("all", k)]), c3(r3b[("all", k)]), c3(r3c[("alone", k)]),
                                    c3(r3c[("joint", k)]),
                                    c3(diff(r3c, "joint", "alone", k, tag="3c", sample="her design")),
                                    c3(r3d[("alone", k)]), c3(r3d[("joint", k)]),
                                    c3(diff(r3d, "joint", "alone", k, tag="3d", sample="his design"))]))
    rows.append(("Displaced (units)", [f"{r3a['n_tr']['all']:,}", f"{r3b['n_tr']['all']:,}",
                                       f"{r3c['n_tr']['alone']:,}", f"{r3c['n_tr']['joint']:,}", "",
                                       f"{r3d['n_tr']['alone']:,}", f"{r3d['n_tr']['joint']:,}", ""]))
    rows.append(("Control stacks", [f"{r3a['info']['controls']:,}", f"{r3b['info']['controls']:,}",
                                    f"{r3c['info']['controls']:,}", "", "", f"{r3d['info']['controls']:,}", "", ""]))
    nj_h = int(H2.loc[H2["treat"] == 1].drop_duplicates("unit")["his_near"].sum())
    md += ["## 3. Joint loss: her loss alone vs both spouses displaced within a year", "",
           f"'Joint' = his displacement in ev-1..ev+1 of hers ({nj_h} of {r0['n_tr']['all']:,} displaced wives); in "
           "his design, her displacement in ev-1..ev+1 of his (her reports start in calendar 1983). (a) her design "
           "without the joint couples; (b) and controls without his displacement in ev-3..ev+6; (c) her-alone and "
           "joint as separate treated dummies in one regression (controls as in b); (d) the same in his design "
           "(controls without her displacement in ev-3..ev+6).", "",
           md_table(["(a) Her loss, joint dropped", "(b) + clean controls", "(c) Her alone", "(c) Joint",
                     "(c) Joint - her alone", "(d) His alone", "(d) Joint", "(d) Joint - his alone"], rows), ""]
    print("3", c3(r3a[("all", "1-3")]), c3(r3c[("joint", "1-3")]), flush=True)

    # ============================================================ 4. heterogeneity
    rows = []
    r4 = est(H, "bh_present", cg="hrace", tag="4 race", sample="her design")
    for k in ("1-3", "4-6", "1-6"):
        rows.append((f"Race, years {k}", [c3(r4[("Black", k)]), c3(r4[("White", k)]),
                                          c3(diff(r4, "Black", "White", k, tag="4 race", sample="her design"))]))
    rows.append(("Race: displaced wives / control stacks",
                 [f"{r4['n_tr']['Black']:,} / {r4['n_ct']['Black']:,}",
                  f"{r4['n_tr']['White']:,} / {r4['n_ct']['White']:,}", ""]))
    med = U.loc[U["treat"] == 1, "share0"].median()
    has = X["share0"].notna()
    X["earner_med"] = pd.Series(np.where(X["share0"] > med, "1 above", "0 below"), index=X.index).where(has)
    X["earner_40"] = pd.Series(np.where(X["share0"] >= 0.4, "1 >=0.40", "0 <0.40"), index=X.index).where(has)
    for col, lab, g1, g0 in (("earner_med", f"Her share above / below treated median ({med:.2f})", "1 above",
                              "0 below"), ("earner_40", "Her share >= 0.40 / < 0.40", "1 >=0.40", "0 <0.40")):
        r = est(X, "bh_present", cg=col, tag="4 earner", sample=col)
        for k in ("1-3", "4-6", "1-6"):
            rows.append((f"{lab}, years {k}", [c3(r[(g1, k)]), c3(r[(g0, k)]),
                                               c3(diff(r, g1, g0, k, tag="4 earner", sample=col))]))
        rows.append((f"{lab}: displaced wives / control stacks",
                     [f"{r['n_tr'][g1]:,} / {r['n_ct'][g1]:,}", f"{r['n_tr'][g0]:,} / {r['n_ct'][g0]:,}", ""]))
        rh = est(X, "own_hrs", cg=col, tag="4 earner, her hours", sample=col)
        rows.append((f"{lab}: her hours, years 1-3", [cell(*rh[(g1, "1-3")], d=0), cell(*rh[(g0, "1-3")], d=0),
                                                      cell(*diff(rh, g1, g0, "1-3"), d=0)]))
    md += ["## 4. Heterogeneity", "",
           "Group-specific cells and event dummies in one regression (point estimates = separate regressions); the "
           "difference uses the joint clustered covariance. Her share = her / (her + his) labor earnings at baseline "
           f"(treated median {med:.3f}).", "",
           md_table(["First group (Black / higher share)", "Second group (White / lower share)", "Difference"],
                    rows), ""]

    # ============================================================ 5. who leaves; attrition
    wc = who_cache()
    so, seq = wc["fam_so"], wc["seq"]
    q = H.copy()
    sep = q[(q["year"] > q["by"]) & (q["bh_present"] == 0)].sort_values(["unit", "year"]).drop_duplicates("unit")
    sep = sep[["unit", "year", "wave", "int", "h0"]].merge(so, on=["wave", "int"], how="left")
    sep = sep.merge(seq.rename(columns={"pid": "h0", "seq": "hseq"}), on=["h0", "wave"], how="left")
    sep["route"] = np.select([sep["hseq"].between(81, 89), sep["splitoff"].isin([2, 4]),
                              sep["splitoff"].isin([1, 3])], ["died", "she_left", "he_left"], "unknown")
    q = q.merge(sep[["unit", "route"]], on="unit", how="left")
    for k in ("died", "she_left", "he_left", "unknown"):
        q[f"sep_{k}"] = ((q["bh_present"] == 0) & (q["year"] > q["by"]) & (q["route"] == k)).astype(float)
    rows = []
    rb = est(q, "bh_present", tag="5", sample="her design")
    rows.append(("Not with baseline husband (= - main estimate)", [c3((-rb[("all", k)][0], rb[("all", k)][1]))
                                                                   for k in ("1-3", "4-6")]))
    LABR = {"he_left": "He moved out (she stayed in the continuing family)",
            "she_left": "She moved out (split-off family)", "died": "He died",
            "unknown": "Route not identified"}
    for k in ("he_left", "she_left", "died", "unknown"):
        r = est(q, f"sep_{k}", tag="5 who leaves", sample="her design")
        rows.append((f"Separated: {LABR[k]}", [c3(r[("all", kk)]) for kk in ("1-3", "4-6")]))
    sh = sep.merge(H.drop_duplicates("unit")[["unit", "treat", "ev"]], on="unit")
    sh = sh[sh["year"].between(sh["ev"], sh["ev"] + 6)]
    shares = sh.groupby("treat")["route"].value_counts(normalize=True).unstack().fillna(0)
    cnts = sh.groupby("treat").size()
    for t in (1, 0):
        for k in LABR:
            ROWS.append(dict(block="5 who leaves, shares", sample="her design", outcome="route of first separation",
                             group="treated" if t else "control", term=k, coef=shares.loc[t].get(k, 0.0),
                             n=int(cnts.loc[t])))
    desc = ("Route of the first separation in e = 0..+6 (shares): displaced wives (" + f"{cnts.loc[1]:,} separations) "
            + ", ".join(f"{LABR[k].split(' (')[0].lower()} {shares.loc[1].get(k, 0):.2f}" for k in LABR)
            + f"; controls ({cnts.loc[0]:,}) " + ", ".join(f"{LABR[k].split(' (')[0].lower()} "
                                                           f"{shares.loc[0].get(k, 0):.2f}" for k in LABR) + ".")
    # attrition and the outcome filled from his side
    iy = sorted({x - 1 for x in psid1.WAVES})
    UU = H.drop_duplicates("unit")[["unit", "pid", "ev", "h0", "treat", "fam68"]]
    G = UU.assign(k=1).merge(pd.DataFrame({"e": range(-3, 7), "k": 1}), on="k").drop(columns="k")
    G["year"] = G["ev"] + G["e"]
    G = G[G["year"].isin(iy) & (G["year"] <= Y_HI)]
    G = G.merge(H[["unit", "year", "bh_present"]], on=["unit", "year"], how="left")
    G["observed"] = G["bh_present"].notna().astype(float)
    mh = m[["pid", "year", "w_pid"]].rename(columns={"pid": "h0", "w_pid": "hw"})
    G = G.merge(mh, on=["h0", "year"], how="left")
    seen = G.merge(mh[["h0", "year"]].assign(hseen=1.0), on=["h0", "year"], how="left")["hseen"].to_numpy()
    hisside = np.where(seen == 1, (G["hw"] == G["pid"]).astype(float), np.nan)
    G["bh_both"] = G["bh_present"].fillna(pd.Series(hisside, index=G.index))
    G["cell"] = pd.factorize(G["year"].astype(np.int64) * 10000 + G["ev"].astype(np.int64))[0]
    ro = est(G, "observed", tag="5 attrition", sample="her design grid")
    rbb = est(G, "bh_both", tag="5 outcome filled from his side", sample="her design grid")
    rows.append(("Observed as wife or head (attrition; grid of interview years)",
                 [c3(ro[("all", k)]) for k in ("1-3", "4-6")]))
    rows.append(("Still with baseline husband, filled from his side",
                 [c3(rbb[("all", k)]) for k in ("1-3", "4-6")]))
    # symmetric observation: she is observed (wife or head) at the first interview that could report an event in ev
    fiy = {ev: min(y for y in iy if y >= ev) for ev in range(EV_LO, EV_HI + 1)}
    U2 = UU.assign(fy=UU["ev"].map(fiy)).merge(
        w[["pid", "year"]].drop_duplicates().assign(o=1).rename(columns={"year": "fy"}), on=["pid", "fy"], how="left")
    keep = U2.loc[U2["o"] == 1, "unit"]
    kshare = U2.assign(o=U2["o"].fillna(0)).groupby("treat")["o"].mean()
    rs = est(H[H["unit"].isin(keep)], "bh_present", tag="5b observed at reporting interview",
             sample="her design, both groups observed at the first interview >= ev")
    rso = est(G[G["unit"].isin(keep)], "observed", tag="5b observed at reporting interview, attrition",
              sample="her design grid, both groups observed at the first interview >= ev")
    rsb = est(G[G["unit"].isin(keep)], "bh_both", tag="5b observed at reporting interview, filled from his side",
              sample="her design grid, both groups observed at the first interview >= ev")
    rows.append(("Both groups observed at the first interview after ev: still with baseline husband",
                 [c3(rs[("all", k)]) for k in ("1-3", "4-6")]))
    rows.append(("Same, observed as wife or head (attrition)", [c3(rso[("all", k)]) for k in ("1-3", "4-6")]))
    rows.append(("Same, filled from his side", [c3(rsb[("all", k)]) for k in ("1-3", "4-6")]))
    rows.append(("Same: displaced wives / control stacks",
                 [f"{rs['n_tr']['all']:,} / {rs['info']['controls']:,}", ""]))
    unk = sep.loc[sep["route"] == "unknown", "splitoff"].value_counts(dropna=False)
    rsum = sum(est(q, f"sep_{k}", tag="5 routes, sum check")[("all", "1-3")][0] for k in ("died", "she_left", "he_left", "unknown"))
    post = G[G["e"] >= 1]
    att = post.groupby("treat")["observed"].mean()
    fill = (G["bh_present"].isna() & G["bh_both"].notna()).sum()
    desc += (f" Route not identified = split-off indicator of her family "
             + ", ".join(f"{k}: {v:,}" for k, v in unk.items()) + " (all units, first separations). The routes sum "
             f"to {rsum:.3f} in years 1-3, more than the main estimate, because at the reference year e = -2 more "
             "displaced wives were not yet with this husband (shorter marriages, 2b); measured from baseline the "
             "separation response is larger, not smaller. Treated wives must be interviewed to report the "
             f"displacement; share of units observed at the first interview after ev: displaced {kshare.loc[1]:.3f},"
             f" controls {kshare.loc[0]:.3f}.")
    md += ["## 5. Who leaves, and attrition", "",
           "The PSID has no item on the reason for a separation. Route of the first separation after baseline: his "
           "sequence number 81-89 in that wave = he died; otherwise her family's split-off indicator (2 / 4 = she "
           "moved out into a split-off family; 1 / 3 = she is in the continuing family, so he moved out). Each "
           "route is an outcome ('not with him, first separated by route k'); the routes add up to 1 - outcome.", "",
           md_table(["Years 1-3", "Years 4-6"], rows), "", desc, "",
           f"Share of post-event interview years (e >= 1) in which she is observed as wife or head: displaced "
           f"{att.loc[1]:.3f}, controls {att.loc[0]:.3f}. Filling the outcome from his side (he is a male head with "
           f"another or no wife -> 0) adds {fill:,} person-years.", ""]

    pd.DataFrame(ROWS).to_csv(OUT / "her_loss_robustness.csv", index=False)
    (OUT / "her_loss_robustness.md").write_text("\n".join(md), encoding="utf-8")
    print("written", flush=True)


def figure_main():
    """Paper A figure (Fable's figure 3, proposals/fable_event_study_figures_paperA.md, 2026-10-21): 'still with the
    baseline spouse' by event year after his displacement alone, hers alone and a joint loss, in one stacked
    regression with one clustered covariance. His design (19's male heads, controls without her displacement in
    ev-3..ev+6) gives 'his alone' (wife not displaced in ev-1..ev+1) and 'joint' (wife displaced in ev-1..ev+1); her
    design (64's M3, controls without his displacement in ev-3..ev+6) gives 'her alone', dropping wives whose husband
    was displaced in ev-1..ev+1 (they are the joint couples of his design). Cells, units and FE separate by design as
    in block 1. Writes output/separation_three_events.csv and paperA_joint_loss/fig_psid_separation_events.pdf."""
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    fam = psid9.family()
    d = pd.read_pickle(DATA / "psid_displacement.pkl")
    m = P19.men_panel(py, fam)
    first, src = P64.her_events(py, fam)
    w = women_panel_x(py, fam)
    H = her_stacks_x(w, first)
    his_years = d.loc[d["main"] == 1, ["pid", "year"]].astype({"pid": np.int64, "year": int})
    her_years = her_all_years(py, fam)
    P0 = P19.stacks(m, d, "main")
    P0 = P0[P0["w0"].notna() & P0["ev"].between(EV_LO, EV_HI) & (P0["year"] <= Y_HI)].copy()
    P0["w0"] = P0["w0"].astype(np.int64)
    UH = H.drop_duplicates("unit")[["unit", "h0", "ev"]]
    fl = pd.concat([UH["unit"], window_flags(UH, "h0", his_years, -1, 1, "his_near"),
                    window_flags(UH, "h0", his_years, -3, 6, "his_win")], axis=1)
    H2 = H.merge(fl, on="unit", how="left")
    UM = P0.drop_duplicates("unit")[["unit", "w0", "ev"]]
    fm_ = pd.concat([UM["unit"], window_flags(UM, "w0", her_years, -1, 1, "her_near"),
                     window_flags(UM, "w0", her_years, -3, 6, "her_win")], axis=1)
    P2 = P0.merge(fm_, on="unit", how="left")
    Hc = H2[~((H2["treat"] == 0) & (H2["his_win"] == 1)) & ~((H2["treat"] == 1) & (H2["his_near"] == 1))]
    Pc = P2[~((P2["treat"] == 0) & (P2["her_win"] == 1))]
    a = Hc[["unit", "cell", "fam68", "treat", "e", "bh_present"]].rename(columns={"bh_present": "stay"})
    a = a.assign(g="her alone", unit=a["unit"].astype(str) + "h", cell=a["cell"].astype(str) + "h")
    b = Pc[["unit", "cell", "fam68", "treat", "e", "bw_present", "her_near"]].rename(columns={"bw_present": "stay"})
    b = b.assign(g=np.where(b["her_near"] == 1, "joint", "his alone"), unit=b["unit"].astype(str) + "m",
                 cell=b["cell"].astype(str) + "m").drop(columns="her_near")
    q = pd.concat([a, b], ignore_index=True)
    q["unit"] = pd.factorize(q["unit"])[0]
    q["cell"] = pd.factorize(q["cell"])[0]
    r = est(q, "stay", tg="g", tag="6 figure", sample="his alone / her alone / joint, one regression")
    rows = []
    for g in r["groups"]:
        for e in ES_E:
            bb, se = r[(g, f"e={e:+d}")]
            rows.append(dict(group=g, term=f"e={e:+d}", coef=bb, se=se, p=pv(bb, se), stars=stars(pv(bb, se)),
                             treated=r["n_tr"][g], n=r["info"]["n"], clusters=r["info"]["clusters"]))
        for k in W:
            bb, se = r[(g, k)]
            rows.append(dict(group=g, term=f"mean {k}", coef=bb, se=se, p=pv(bb, se), stars=stars(pv(bb, se)),
                             treated=r["n_tr"][g], n=r["info"]["n"], clusters=r["info"]["clusters"]))
    for g1, g2 in (("joint", "his alone"), ("her alone", "his alone"), ("joint", "her alone")):
        for k in W:
            bb, se = diff(r, g1, g2, k)
            rows.append(dict(group=f"{g1} - {g2}", term=f"mean {k}", coef=bb, se=se, p=pv(bb, se),
                             stars=stars(pv(bb, se)), n=r["info"]["n"], clusters=r["info"]["clusters"]))
    D = pd.DataFrame(rows)
    D.to_csv(OUT / "separation_three_events.csv", index=False)
    print(D.to_string(), flush=True)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    col = {"his alone": "#2a78d6", "her alone": "#1baf7a", "joint": "#eb6834"}
    lab = {"his alone": "his displacement alone", "her alone": "her displacement alone",
           "joint": "joint (both within a year)"}
    fig, ax = plt.subplots(figsize=(7, 4.2))
    for k, g in enumerate(("his alone", "her alone", "joint")):
        x = D[(D.group == g) & D.term.str.startswith("e=")].copy()
        x["e"] = x.term.str.replace("e=", "").astype(int)
        x = pd.concat([x, pd.DataFrame({"e": [-2], "coef": [0.0], "se": [0.0]})]).sort_values("e")
        xx = x.e.to_numpy() + (k - 1) * 0.12
        n = int(D.loc[D.group == g, "treated"].dropna().iloc[0])
        ax.errorbar(xx, 100 * x.coef, yerr=196 * x.se, color=col[g], lw=1.6, marker="o", ms=4, capsize=0,
                    label=f"{lab[g]} ({n:,} events)")
    ax.axhline(0, color="#555555", lw=0.7)
    ax.axvline(-0.5, color="#999999", lw=0.8, ls=":")
    ax.set_xlabel("years since the displacement")
    ax.set_ylabel("still with the spouse of before (pp)")
    ax.grid(axis="y", color="#e5e5e5", lw=0.6)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.legend(frameon=False, fontsize=8, loc="lower left")
    fig.tight_layout()
    path = HERE / "paperA_joint_loss" / "fig_psid_separation_events.pdf"
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=160)
    plt.close(fig)


HER_OUT = [("own_hrs", "(a) Her annual hours", 1), ("earn", "(b) Her labor income (2000 $)", 1),
           ("h_hrs", "(c) His annual hours", 1), ("h_earn", "(d) His labor income (2000 $)", 1),
           ("faminc", "(e) Family income (2000 $)", 1), ("fs", "(f) Food stamps (pp)", 100)]


def figure_her_main():
    """Paper A figure (Fable's figure 4, 2026-10-21): her first displacement as the event (64's M3 design, as
    her_stacks_x), outcomes her hours and labor income, his hours and labor income (while still with the baseline
    husband), her family's income and food-stamp receipt (2000 $ from IGE/1); pooled and by the head's race (cells x
    race in one covariance). Writes output/her_displacement_family.csv and paperA_joint_loss/fig_psid_her_displacement.pdf."""
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    fam = psid9.family()
    first, src = P64.her_events(py, fam)
    w = women_panel_x(py, fam)
    H = her_stacks_x(w, first)
    hd = py[py["head"]][["wave", "int", "faminc"]].drop_duplicates(["wave", "int"])
    H = H.merge(hd, on=["wave", "int"], how="left").merge(
        fam[["wave", "int", "fs"]].drop_duplicates(["wave", "int"]), on=["wave", "int"], how="left")
    H = H.merge(w[["pid", "wave", "h_earn"]].drop_duplicates(["pid", "wave"]), on=["pid", "wave"], how="left")
    same = H["h_pid"] == H["h0"]
    H["h_hrs"] = H["h_hrs"].where(same)
    H["h_earn"] = H["h_earn"].where(same)
    rows = []
    for y, _, _ in HER_OUT:
        for lab, kw in (("All", {}), ("by race", {"cg": "hrace"})):
            r = est(H, y, tag="7 her figure", sample=lab, **kw)
            for g in r["groups"]:
                for e in ES_E:
                    bb, se = r[(g, f"e={e:+d}")]
                    rows.append(dict(outcome=y, group=g, term=f"e={e:+d}", coef=bb, se=se, p=pv(bb, se),
                                     stars=stars(pv(bb, se)), treated=r["n_tr"][g], n=r["info"]["n"],
                                     clusters=r["info"]["clusters"]))
                for k in W:
                    bb, se = r[(g, k)]
                    rows.append(dict(outcome=y, group=g, term=f"mean {k}", coef=bb, se=se, p=pv(bb, se),
                                     stars=stars(pv(bb, se)), treated=r["n_tr"][g], n=r["info"]["n"],
                                     clusters=r["info"]["clusters"]))
            if kw:
                for k in W:
                    bb, se = diff(r, "Black", "White", k)
                    rows.append(dict(outcome=y, group="Black - White", term=f"mean {k}", coef=bb, se=se,
                                     p=pv(bb, se), stars=stars(pv(bb, se)), n=r["info"]["n"],
                                     clusters=r["info"]["clusters"]))
        print(y, "done", flush=True)
    D = pd.DataFrame(rows)
    D.to_csv(OUT / "her_displacement_family.csv", index=False)
    print(D[D.term.str.startswith("mean")].to_string(), flush=True)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    col = {"all": "#0b0b0b", "Black": "#eb6834", "White": "#2a78d6"}
    fig, axs = plt.subplots(2, 3, figsize=(12.5, 7.2))
    for ax, (y, title, sc) in zip(axs.ravel(), HER_OUT):
        for k, g in enumerate(("all", "Black", "White")):
            x = D[(D.outcome == y) & (D.group == g) & D.term.str.startswith("e=")].copy()
            x["e"] = x.term.str.replace("e=", "").astype(int)
            x = pd.concat([x, pd.DataFrame({"e": [-2], "coef": [0.0], "se": [0.0]})]).sort_values("e")
            xx = x.e.to_numpy() + (k - 1) * 0.12
            if g == "all":
                ax.fill_between(xx, sc * (x.coef - 1.96 * x.se), sc * (x.coef + 1.96 * x.se), color=col[g],
                                alpha=0.12, lw=0)
                ax.plot(xx, sc * x.coef, color=col[g], lw=2, marker="o", ms=3.5, label="all")
            else:
                ax.plot(xx, sc * x.coef, color=col[g], lw=1.2, marker="o", ms=3, ls="--", label=g)
        ax.axhline(0, color="#555555", lw=0.7)
        ax.axvline(-0.5, color="#999999", lw=0.8, ls=":")
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("years since her displacement")
        ax.grid(axis="y", color="#e5e5e5", lw=0.6)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    h, lb = axs[0, 0].get_legend_handles_labels()
    fig.legend(h, ["all (95% CI)", "Black", "White"], frameon=False, fontsize=9, loc="lower center", ncol=3)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    path = HERE / "paperA_joint_loss" / "fig_psid_her_displacement.pdf"
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    import sys
    if "--figure-her" in sys.argv:
        figure_her_main()
    elif "--figure" in sys.argv:
        figure_main()
    else:
        main()
