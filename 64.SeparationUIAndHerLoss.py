r"""Separation hazard: does it depend on UI generosity (M2b) and on HER displacement (M3)? PSID, 2026-10-19.

WP4 of IGE/proposals/fable_3h_plan_paperA.md, the two reduced-form checks asked for by the marriage note
(IGE/proposals/fable_marriage_divorce_paperA.md, Section 5: M2b = sigma_J by UI entitlement; M3 = response to her
displacement). Imports 19.FatherDisplacement.py (stacks, men_panel, reports, demean) and 9.ChildExposure.py (family
hours) read only; nothing in 19 / 60-62 is edited or rerun.

Reads (read only): IGE/data/psid_person_year.pkl, psid_displacement.pkl (19), correlated_shocks_wife_disp.pkl (23: the
wife's reason-for-job-end reports, 1984-2023 waves), husband_shocks_fam.pkl (18: state FIPS of the family, 1976-2023
waves), ui_generosity.csv (12b: DOL state UI law parameters, ETA 5159 average benefits, BEA wages), the raw PSID family
files through 19.reports (female heads' own job-end reports). Writes
  IGE/data/sep_ui_femhead_reports.pkl     cache: female heads' job-end reports (person level; git-ignored folder)
  IGE/output/separation_ui_her_loss.csv   every estimate (aggregates only)
  IGE/output/separation_ui_her_loss.md    tables
  IGE/output/bw_present_by_year.csv       'still with baseline wife' by event year, -3..+6 (for WP3.2)

DESIGN (19's stacked event study; Cengiz et al. 2019). Units = person x event year ev; treated = first displacement
(closure or layoff / firing) in ev; clean controls = no displacement up to ev + 6; baseline = the last observed of
ev - 1, ev - 2 with a child 0-17 in the family unit and positive own annual hours; person x stack and calendar year x
stack fixed effects; reference e = -2; s.e. clustered by 1968 family (CR1); p-values normal. Main sample = the Paper A
target sample of IGE/60: events 1984-2021, outcome years <= 2021.

M2b (his displacement x state UI generosity). Outcome 'still with baseline wife' (bw_present: 1 while the baseline wife
is his wife; 0 after separation, divorce or her death). The state is the family's state at the baseline interview
(18's fips; missing 1994-95 values filled from the same man's adjacent interview), the UI parameters those of the
displacement year ev in that state (12b): (a) cap_rel = maximum weekly benefit / state average weekly wage, (b) dur =
maximum weeks of regular benefits, (c) lmaxben = log real maximum potential benefit (max WBA x max weeks, 2000 $),
(d) repl = average weekly benefit / average weekly wage. Each standardised over the units of the pooled sample (z).
Interaction model: y = unit FE + cell FE + sum_e b_e D x 1{e} + sum_e g_e D x 1{e} x z + sum_e c_e 1{e} x z, e != -2
(the last term lets control families in generous states have their own path, so g is a difference-in-differences of
the displacement response across states; z itself is absorbed by the unit FE). Reported: mean of g over e = +1..+3 (the
model's target window) and +4..+6, and the pre-period g at e = -3, -1. Also a median split (treated units at or below /
above the median of lmaxben among treated units; separate event studies; difference with independent-sample s.e.).
The sign the literature leads one to expect (Lindo, Regmi and Swensen 2025: UI generosity mitigates divorce after men's
layoffs) is g > 0 (more generous -> smaller fall in bw_present). UI generosity is not randomly assigned across states
and years; with state-year variation only, the interaction compares displaced fathers in more and less generous
state-years net of what generosity does to controls; no region x year fixed effects (they absorb the variation).

M3 (her displacement as the event). Same design with the roles reversed: women who are wives (or female heads) of the
PSID, race = the family head's race at baseline; event = her first displacement (codes 1 / 3; 2021-23 code 5) from the
wife's reports (23) and, after a separation, her own reports as a female head (19.reports, female heads), calendar years
1983+ (the wife's items start with the 1984 wave); baseline: married (a male head is her husband), a child 0-17,
positive own hours. Outcome 'still with baseline husband' (bh_present: 1 while she is the wife of the baseline husband,
0 when she is a female head or the wife of another man; missing when she is neither wife nor head). Secondary outcome
her own annual hours (the first stage: the event bites). Closures-only variant (first displacement is a closure).

CAVEAT (both designs). The marriage outcome is 1 by construction at the baseline years, so the pre-period
coefficients are mechanical (at e = -3 she was not yet his wife in some couples; e = -1 is the baseline year in about
half of the stacks) and there is no placebo test for this outcome; identification rests on the post-period against
clean controls with person fixed effects (the standard displacement design).
"""
import importlib.util
import os
import warnings

os.environ.setdefault("OMP_NUM_THREADS", "4")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "4")
os.environ.setdefault("MKL_NUM_THREADS", "4")

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402

from common import DATA, OUT, HERE, stars  # noqa: E402

warnings.simplefilter("ignore", FutureWarning)
warnings.simplefilter("ignore", RuntimeWarning)


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


P19 = _load("p19", "19.FatherDisplacement.py")
psid9 = P19.psid9
ES_E = P19.ES_E                                  # [-3, -1, 0, 1, 2, 3, 4, 5, 6], reference -2
ROWS = []
EV_LO, EV_HI, Y_HI = 1984, 2021, 2021


def pv(b, se):
    return 2 * stats.norm.sf(abs(b / se)) if (se == se and se > 0) else np.nan


def cell(b, se, p=None, d=3):
    if not (se == se and se > 0):
        return "n.a."
    p = pv(b, se) if p is None else p
    return f"{b:,.{d}f}{stars(p)} ({se:,.{d}f}; p={'<0.001' if p < 0.001 else f'{p:.3f}'})"


def rec(design, sample, outcome, spec, term, b, se, **kw):
    ROWS.append(dict(design=design, sample=sample, outcome=outcome, spec=spec, term=term, coef=b, se=se,
                     p=pv(b, se), **kw))


# ---------------------------------------------------------------- regression (19's twfe, one demeaning per sample)
def fit(q, y, xs):
    """OLS of y on xs with unit and cell FE absorbed; CR1 by fam68 (as 19.twfe)."""
    q = q.dropna(subset=[y]).reset_index(drop=True)
    u = pd.factorize(q["unit"])[0]
    c = pd.factorize(q["cell"])[0]
    A = P19.demean(np.column_stack([q[y].to_numpy(float), q[xs].to_numpy(float)]),
                   [(u, u.max() + 1), (c, c.max() + 1)])
    Y, X = A[:, 0], A[:, 1:]
    XtX = np.linalg.pinv(X.T @ X)
    b = XtX @ X.T @ Y
    res = Y - X @ b
    g = pd.factorize(q["fam68"])[0]
    G = g.max() + 1
    S = np.zeros((G, X.shape[1]))
    np.add.at(S, g, X * res[:, None])
    n, k = X.shape
    adj = G / (G - 1) * (n - 1) / max(n - k - (u.max() + 1) - (c.max() + 1), 1)
    V = adj * XtX @ (S.T @ S) @ XtX
    info = dict(n=n, treated=int(q.loc[q["treat"] == 1, "unit"].nunique()),
                controls=int(q.loc[q["treat"] == 0, "unit"].nunique()), clusters=G,
                pre_mean=float(q.loc[(q["treat"] == 1) & q["e"].isin([-2, -1]), y].mean()))
    return b, V, info


def comb(b, V, xs, w):
    L = np.array([w.get(x, 0.0) for x in xs])
    e, s = L @ b, np.sqrt(L @ V @ L)
    return e, s


W13 = {e: 1 / 3 for e in (1, 2, 3)}
W46 = {e: 1 / 3 for e in (4, 5, 6)}


def add_dummies(q, z=None):
    q = q.copy()
    xs = []
    for e in ES_E:
        q[f"d{e}"] = ((q["e"] == e) & (q["treat"] == 1)).astype(float)
        xs.append(f"d{e}")
    if z is not None:
        for e in ES_E:
            q[f"dz{e}"] = q[f"d{e}"] * q[z]
            q[f"cz{e}"] = (q["e"] == e).astype(float) * q[z]
            xs += [f"dz{e}", f"cz{e}"]
    return q, xs


def es(q, y):
    """plain event study -> dict term -> (b, se), info."""
    q, xs = add_dummies(q)
    b, V, info = fit(q, y, xs)
    out = {f"e={e:+d}": (b[i], np.sqrt(V[i, i])) for i, e in enumerate(ES_E)}
    out["mean +1..+3"] = comb(b, V, xs, {f"d{e}": w for e, w in W13.items()})
    out["mean +4..+6"] = comb(b, V, xs, {f"d{e}": w for e, w in W46.items()})
    return out, info


def es_inter(q, y, z):
    q, xs = add_dummies(q.dropna(subset=[z]), z)
    b, V, info = fit(q, y, xs)
    out = {}
    for pre, lab in (("d", "displaced"), ("dz", "displaced x z")):
        for e in (-3, -1):
            out[f"{lab}, e={e:+d}"] = comb(b, V, xs, {f"{pre}{e}": 1.0})
        out[f"{lab}, mean +1..+3"] = comb(b, V, xs, {f"{pre}{e}": w for e, w in W13.items()})
        out[f"{lab}, mean +4..+6"] = comb(b, V, xs, {f"{pre}{e}": w for e, w in W46.items()})
    return out, info


# ---------------------------------------------------------------- M2b: UI generosity in his state-year
def ui_table():
    u = pd.read_csv(DATA / "ui_generosity.csv")
    u = u.rename(columns={"state_fips": "fips", "year": "ev"})
    u["cap_rel"] = u["max_wba_repl"]
    u["dur"] = u["max_duration_weeks"]
    u["lmaxben"] = np.log(u["max_benefit_2000"])
    u["repl"] = u["repl_rate"]
    return u[["fips", "ev", "state", "cap_rel", "dur", "lmaxben", "repl", "max_wba_2000", "max_benefit_2000"]]


UIM = [("cap_rel", "Max weekly benefit / state avg weekly wage"), ("dur", "Max weeks of regular benefits"),
       ("lmaxben", "Log max potential benefit (max WBA x weeks, 2000 $)"),
       ("repl", "Avg weekly benefit / avg weekly wage")]


def attach_ui(P, m):
    """baseline interview's state (18) -> UI parameters of ev in that state (12b), standardised over units."""
    F = pd.read_pickle(DATA / "husband_shocks_fam.pkl")[["wave", "int", "fips"]].drop_duplicates(["wave", "int"])
    mm = m[["pid", "year", "wave", "int", "nkid", "hh"]].merge(F, on=["wave", "int"], how="left")
    mm = mm.sort_values(["pid", "year"])
    g = mm.groupby("pid")["fips"]
    mm["fips"] = mm["fips"].fillna(g.ffill()).fillna(g.bfill())     # 1994-95 gaps: same man, adjacent interview
    key = mm.set_index(["pid", "year"])["fips"]
    U = P[["pid", "ev", "unit"]].drop_duplicates("unit")
    f1 = key.reindex(pd.MultiIndex.from_arrays([U["pid"], U["ev"] - 1])).to_numpy()
    f2 = key.reindex(pd.MultiIndex.from_arrays([U["pid"], U["ev"] - 2])).to_numpy()
    U = U.assign(fips=np.where(np.isnan(f1), f2, f1))
    U = U.merge(ui_table(), on=["fips", "ev"], how="left")
    for z, _ in UIM:
        U[f"z_{z}"] = (U[z] - U[z].mean()) / U[z].std()
    return P.merge(U.drop(columns=["pid", "ev"]), on="unit", how="left"), U


# ---------------------------------------------------------------- M3: women's panel and her displacement
def femhead_reports(fam):
    fn = DATA / "sep_ui_femhead_reports.pkl"
    if fn.exists():
        return pd.read_pickle(fn)
    r = P19.reports(fam)
    r.to_pickle(fn)
    return r


def her_events(py, fam):
    """pid -> first year of her main / strict displacement (calendar 1983+): wife reports (23) + female-head reports."""
    wd = pd.read_pickle(DATA / "correlated_shocks_wife_disp.pkl")
    r = femhead_reports(fam)
    fh = py[py["head"] & (py["female"] == 1)][["wave", "int", "pid"]].drop_duplicates(["wave", "int"])
    r = r.merge(fh, on=["wave", "int"], how="inner")
    r["year"] = r["year"].astype(int)
    out = {}
    for k in ("main", "strict"):
        x = r[r[k]].sort_values(["pid", "year", "dated"], ascending=[True, True, False]).drop_duplicates(["pid", "year"])
        prev = set(zip(x["pid"], x["year"] + 1))
        drop = (~x["dated"]) & pd.Series([(p, y) in prev for p, y in zip(x["pid"], x["year"])], index=x.index)
        x = x[~drop]
        ev = pd.concat([x[["pid", "year"]], wd.loc[wd[k] == 1, ["pid", "year"]]])
        ev = ev[ev["year"] >= 1983]
        out[k] = ev.groupby("pid")["year"].min()
    ev_all = pd.concat([r.loc[r["main"], ["pid", "year"]], wd.loc[wd["main"] == 1, ["pid", "year"]]])
    src = dict(wife_reports=int((wd["main"] == 1).sum()), femhead_reports=int(r["main"].sum()),
               first_main=int(out["main"].size), first_strict=int(out["strict"].size), any=len(ev_all))
    return out, src


def women_panel(py, fam):
    """women who are wives or female heads (head's race Black / White) x calendar year t = wave - 1."""
    hd = py[py["head"]][["wave", "int", "pid", "female", "hrace"]].drop_duplicates(["wave", "int"])
    hm = hd[hd["female"] == 0][["wave", "int", "pid"]].rename(columns={"pid": "h_pid"})
    w = py[(py["wife"] | py["head"]) & (py["female"] == 1) & py["hrace"].isin(["White", "Black"])]
    w = w[["pid", "fam68", "wave", "int", "hrace", "wife", "head", "age"]].drop_duplicates(["pid", "wave"])
    w = w.merge(hm, on=["wave", "int"], how="left")
    w["h_pid"] = w["h_pid"].where(w["wife"])
    w = w.merge(fam[["wave", "int", "hh", "wh"]], on=["wave", "int"], how="left")
    w["own_hrs"] = np.where(w["wife"], w["wh"], w["hh"])
    w["h_hrs"] = w["hh"].where(w["wife"])
    k = py[py["child"] & py["age"].between(0, 17)].groupby(["wave", "int"]).size().rename("nkid")
    w = w.merge(k.reset_index(), on=["wave", "int"], how="left")
    w["nkid"] = w["nkid"].fillna(0)
    w["year"] = w["wave"] - 1
    return w.sort_values(["pid", "year"]).drop_duplicates(["pid", "year"]).reset_index(drop=True)


def her_stacks(w, first, kind):
    fm = w["pid"].map(first["main"]).fillna(9999)
    fk = w["pid"].map(first[kind]).fillna(9999)
    b = pd.concat([w.assign(ev=w["year"] + 1, pri=0), w.assign(ev=w["year"] + 2, pri=1)])
    b = b.assign(fm=pd.concat([fm, fm]).to_numpy(), fk=pd.concat([fk, fk]).to_numpy())
    b = b.sort_values(["pid", "ev", "pri"]).drop_duplicates(["pid", "ev"]).reset_index(drop=True)
    b = b[(b["nkid"] > 0) & (b["own_hrs"] > 0) & b["h_pid"].notna() & b["ev"].between(EV_LO, EV_HI)]
    tr = (b["fk"] == b["ev"]) & ((b["fm"] >= b["ev"]) if kind == "strict" else True)
    ct = b["fm"] > b["ev"] + 6
    b = b[tr | ct].assign(treat=tr[tr | ct].astype(int))
    base = b[["pid", "ev", "treat", "hrace", "h_pid"]].rename(columns={"h_pid": "h0"})
    p = base.merge(w[["pid", "fam68", "year", "h_pid", "own_hrs", "h_hrs"]], on="pid")
    p = p[(p["year"] >= p["ev"] - 3) & (p["year"] <= p["ev"] + 6) & (p["year"] <= Y_HI)]
    p["e"] = p["year"] - p["ev"]
    p["bh_present"] = (p["h_pid"] == p["h0"]).astype(float)
    p["h_hrs"] = p["h_hrs"].where(p["h_pid"] == p["h0"])
    p["unit"] = pd.factorize(p["pid"].astype(np.int64) * 10000 + p["ev"].astype(np.int64))[0]
    p["cell"] = pd.factorize(p["year"].astype(np.int64) * 10000 + p["ev"].astype(np.int64))[0]
    return p.reset_index(drop=True)


def md_table(header, rows):
    out = ["| | " + " | ".join(header) + " |", "|---|" + "---:|" * len(header)]
    out += [f"| {lab} | " + " | ".join(v) + " |" for lab, v in rows]
    return "\n".join(out)


def main():
    OUT.mkdir(exist_ok=True)
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    fam = psid9.family()
    d = pd.read_pickle(DATA / "psid_displacement.pkl")
    m = P19.men_panel(py, fam)
    print("panels built", flush=True)
    md = ["# Separation hazard: UI generosity (M2b) and her displacement (M3), PSID", "",
          "Built by `64.SeparationUIAndHerLoss.py` (2026-10-19); design in its docstring. 19's stacked event study "
          "(person x stack and calendar year x stack FE; reference e = -2; clean controls not displaced to ev+6; "
          "baseline with a child 0-17 and positive own hours). Unweighted PSID SRC + SEO, Black and White (head's "
          "race). S.e. clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1; every cell: coefficient*** (s.e.; "
          "p). Main sample = Paper A target sample (IGE/60): events 1984-2021, outcome years <= 2021.", "",
          "**Caveat.** The marriage outcome is 1 by construction at baseline, so the pre-period coefficients are "
          "mechanical (no placebo test for this outcome); identification rests on the post-period against clean "
          "controls with person fixed effects.", ""]

    # ============================================================ 0. bw_present path (target sample) for WP3.2
    P0 = P19.stacks(m, d, "main")
    P0 = P0[P0["w0"].notna()]
    path = []
    samples = {"main": P0[P0["ev"].between(EV_LO, EV_HI) & (P0["year"] <= Y_HI)],
               "ev1977": P0[P0["ev"].between(1977, EV_HI) & (P0["year"] <= Y_HI)]}
    for race in ("All", "Black", "White"):
        q = samples["main"] if race == "All" else samples["main"][samples["main"]["hrace"] == race]
        res, info = es(q, "bw_present")
        for t, (b, se) in res.items():
            path.append(dict(sample="IGE/60 target sample (events 1984-2021, years <= 2021)", race=race, term=t,
                             coef=b, se=se, p=pv(b, se), stars=stars(pv(b, se)), **info))
            rec("his displacement", race, "bw_present", "plain, target sample", t, b, se, **info)
    f19 = pd.read_csv(OUT / "father_displacement.csv")
    f19 = f19[(f19["table"] == "family_event_study") & (f19["design"] == "main") & f19["subsample"].isna()
              & (f19["outcome"] == "bw_present")]
    for _, r in f19.iterrows():
        path.append(dict(sample="IGE/19 full sample (events 1968-2022), copied from father_displacement.csv",
                         race=r["sample"], term=r["term"], coef=r["coef"], se=r["se"], p=r["p"], stars=stars(r["p"]),
                         n=r["n"], treated=r["treated"], controls=r["controls"], clusters=r["clusters"],
                         pre_mean=r["pre_mean_treated"]))
    pd.DataFrame(path).to_csv(OUT / "bw_present_by_year.csv", index=False)
    PATH = pd.DataFrame(path)
    print("path done", flush=True)

    # ============================================================ 1. M2b
    P, U = attach_ui(P0, m)
    cov = U.dropna(subset=["cap_rel"])
    md += ["## 1. M2b: his displacement x state UI generosity", "",
           f"State found for {U['fips'].notna().mean():.3f} of father x stack units and UI parameters for "
           f"{U['cap_rel'].notna().mean():.3f} (all events 1968-2022; 12b starts in 1976). Distribution over units "
           "with UI data (target sample events): " + ", ".join(
               f"{z} mean {cov.loc[cov['ev'].between(EV_LO, EV_HI), z].mean():.3f} / sd "
               f"{cov.loc[cov['ev'].between(EV_LO, EV_HI), z].std():.3f}" for z, _ in UIM) + ".", ""]
    # re-standardise within each estimation sample (units)
    INTER = {}
    for sname, lo in (("main", EV_LO), ("ev1977", 1977)):
        S0 = P[P["ev"].between(lo, EV_HI) & (P["year"] <= Y_HI)].copy()
        uu = S0.drop_duplicates("unit")
        for z, _ in UIM:
            S0[f"z_{z}"] = (S0[z] - uu[z].mean()) / uu[z].std()
        for race in ("All", "Black", "White"):
            q = S0 if race == "All" else S0[S0["hrace"] == race]
            for z, _ in (UIM if sname == "main" else UIM[2:3]):
                res, info = es_inter(q, "bw_present", f"z_{z}")
                INTER[(sname, race, z)] = (res, info)
                for t, (b, se) in res.items():
                    rec("M2b his displacement x UI", race, "bw_present", f"interaction {z}, {sname}", t, b, se, **info)
                print(sname, race, z, cell(*res["displaced x z, mean +1..+3"]), flush=True)
    for sname, title in (("main", "Target sample (events 1984-2021)"), ("ev1977", "Events 1977-2021")):
        rows = []
        for z, lab in (UIM if sname == "main" else UIM[2:3]):
            vals = []
            for race in ("All", "Black", "White"):
                res, info = INTER[(sname, race, z)]
                vals.append(f"{cell(*res['displaced x z, mean +1..+3'])}<br>+4..+6: "
                            f"{cell(*res['displaced x z, mean +4..+6'])}<br>pre e=-3: "
                            f"{cell(*res['displaced x z, e=-3'])}; e=-1: {cell(*res['displaced x z, e=-1'])}")
            rows.append((f"Displaced x z({lab}), mean +1..+3", vals))
        z0 = UIM[0][0] if sname == "main" else "lmaxben"
        vals = []
        for race in ("All", "Black", "White"):
            res, info = INTER[(sname, race, z0)]
            vals.append(cell(*res["displaced, mean +1..+3"]))
        rows.append(("Displaced (at mean generosity), mean +1..+3", vals))
        vals = []
        for race in ("All", "Black", "White"):
            info = INTER[(sname, race, z0)][1]
            vals.append(f"{info['n']:,} / {info['treated']:,} / {info['controls']:,} / {info['clusters']:,}")
        rows.append(("N person-years / displaced fathers / control stacks / clusters", vals))
        md += [f"### 1{'a' if sname == 'main' else 'b'}. Interaction model, {title}", "",
               "Each cell of a row is one regression (outcome 'still with baseline wife'): coefficient on "
               "displaced x event time x z (z = UI measure standardised over the sample's units, 1 sd), mean of "
               "e = +1..+3; below it the mean of +4..+6 and the (mechanical) pre-period terms. Event-time x z for all "
               "families included. A positive coefficient = more generous UI, smaller fall in the probability of "
               "still being with the baseline wife.", "",
               md_table(["All", "Black", "White"], rows), ""]

    # median split on lmaxben (treated units)
    S0 = P[P["ev"].between(EV_LO, EV_HI) & (P["year"] <= Y_HI)].dropna(subset=["lmaxben"]).copy()
    rows, srows = [], {}
    for race in ("All", "Black", "White"):
        q = S0 if race == "All" else S0[S0["hrace"] == race]
        med = q.loc[q["treat"] == 1].drop_duplicates("unit")["lmaxben"].median()
        out = {}
        for half, f in (("low", q["lmaxben"] <= med), ("high", q["lmaxben"] > med)):
            res, info = es(q[f], "bw_present")
            out[half] = (res, info)
            for t, (b, se) in res.items():
                rec("M2b his displacement, median split", race, "bw_present", f"lmaxben {half} (median {med:.3f})",
                    t, b, se, **info)
        srows[race] = (out, med)
    for lab, t in (("Mean +1..+3", "mean +1..+3"), ("Mean +4..+6", "mean +4..+6")):
        for half in ("low", "high"):
            rows.append((f"{lab}, {'below' if half == 'low' else 'above'} median generosity",
                         [cell(*srows[r][0][half][0][t]) for r in ("All", "Black", "White")]))
        vals = []
        for r in ("All", "Black", "White"):
            (bl, sl), (bh, sh) = srows[r][0]["low"][0][t], srows[r][0]["high"][0][t]
            b, se = bh - bl, np.sqrt(sl ** 2 + sh ** 2)
            vals.append(cell(b, se))
            rec("M2b his displacement, median split", r, "bw_present", "high - low", t, b, se)
        rows.append((f"{lab}: above - below", vals))
    rows.append(("Displaced fathers below / above median",
                 [f"{srows[r][0]['low'][1]['treated']:,} / {srows[r][0]['high'][1]['treated']:,}"
                  for r in ("All", "Black", "White")]))
    rows.append(("Median real max potential benefit (2000 $)",
                 [f"{np.exp(srows[r][1]):,.0f}" for r in ("All", "Black", "White")]))
    md += ["### 1c. Median split by the maximum potential benefit (target sample)", "",
           "Separate event studies for displaced fathers (and control stacks) in state-years at or below / above the "
           "median log real maximum potential benefit among displaced fathers of the race; the difference treats "
           "the two regressions as independent.", "", md_table(["All", "Black", "White"], rows), ""]
    print("M2b done", flush=True)

    # ============================================================ 2. M3
    first, src = her_events(py, fam)
    w = women_panel(py, fam)
    HS = {k: her_stacks(w, first, k) for k in ("main", "strict")}
    RES3 = {}
    for kind in ("main", "strict"):
        for race in ("All", "Black", "White"):
            q = HS[kind] if race == "All" else HS[kind][HS[kind]["hrace"] == race]
            for y in (("bh_present", "own_hrs", "h_hrs") if kind == "main" else ("bh_present",)):
                res, info = es(q, y)
                RES3[(kind, race, y)] = (res, info)
                for t, (b, se) in res.items():
                    rec(f"M3 her displacement ({kind})", race, y, "plain", t, b, se, **info)
            print("M3", kind, race, cell(*RES3[(kind, race, "bh_present")][0]["mean +1..+3"]), flush=True)
    rows = []
    for y, lab in (("bh_present", "Still with baseline husband"), ("own_hrs", "Her annual hours"),
                   ("h_hrs", "Husband's annual hours (while with her)")):
        for t in ("e=-3", "e=-1", "e=+0", "e=+1", "e=+2", "e=+3", "e=+4", "e=+5", "e=+6", "mean +1..+3",
                  "mean +4..+6"):
            if y != "bh_present" and t not in ("e=+0", "mean +1..+3", "mean +4..+6"):
                continue
            rows.append((f"{lab}: {t}", [cell(*RES3[("main", r, y)][0][t], d=3 if y == "bh_present" else 0)
                                         for r in ("All", "Black", "White")]))
        rows.append((f"{lab}: N person-years / displaced wives / control stacks / clusters; treated mean e=-2,-1",
                     [f"{RES3[('main', r, y)][1]['n']:,} / {RES3[('main', r, y)][1]['treated']:,} / "
                      f"{RES3[('main', r, y)][1]['controls']:,} / {RES3[('main', r, y)][1]['clusters']:,}; "
                      f"{RES3[('main', r, y)][1]['pre_mean']:.3f}" for r in ("All", "Black", "White")]))
    for t in ("mean +1..+3", "mean +4..+6"):
        rows.append((f"Closures only, still with baseline husband: {t}",
                     [cell(*RES3[("strict", r, "bh_present")][0][t]) for r in ("All", "Black", "White")]))
    rows.append(("Closures only: displaced wives",
                 [f"{RES3[('strict', r, 'bh_present')][1]['treated']:,}" for r in ("All", "Black", "White")]))
    # comparison: his displacement on the same sample window, mean +1..+3 and +4..+6
    for t in ("mean +1..+3", "mean +4..+6"):
        rows.append((f"For comparison, HIS displacement, still with baseline wife: {t}",
                     [cell(*PATH[(PATH["sample"].str.startswith("IGE/60")) & (PATH["race"] == r)
                                 & (PATH["term"] == t)][["coef", "se"]].iloc[0].to_numpy())
                      for r in ("All", "Black", "White")]))
    md += ["## 2. M3: her displacement as the event", "",
           f"Her job-end reports (closure / layoff / fired): {src['wife_reports']:,} wife-years from the wife's items "
           f"(1984-2023 waves) and {src['femhead_reports']:,} report rows from female heads' own items; "
           f"{src['first_main']:,} women with a first displacement in 1983+ ({src['first_strict']:,} first closure). "
           "Baseline: wife of a male head, a child 0-17, positive own hours. Race = the head's race at baseline.", "",
           md_table(["All", "Black", "White"], rows), ""]

    # ============================================================ 3. path for WP3.2
    rows = []
    for t in ["e=-3", "e=-1", "e=+0", "e=+1", "e=+2", "e=+3", "e=+4", "e=+5", "e=+6", "mean +1..+3", "mean +4..+6"]:
        rows.append((t, [cell(*PATH[(PATH["sample"].str.startswith("IGE/60")) & (PATH["race"] == r)
                                    & (PATH["term"] == t)][["coef", "se"]].iloc[0].to_numpy())
                         for r in ("All", "Black", "White")]))
    md += ["## 3. Still with baseline wife by event year after his displacement (target sample; for WP3.2)", "",
           "Same numbers in `bw_present_by_year.csv`, which also carries IGE/19's full-sample path "
           "(events 1968-2022) copied from `father_displacement.csv`.", "",
           md_table(["All", "Black", "White"], rows), ""]

    pd.DataFrame(ROWS).to_csv(OUT / "separation_ui_her_loss.csv", index=False)
    (OUT / "separation_ui_her_loss.md").write_text("\n".join(md), encoding="utf-8")
    print("written", flush=True)


if __name__ == "__main__":
    main()
