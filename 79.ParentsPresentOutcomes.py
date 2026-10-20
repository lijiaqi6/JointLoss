r"""Both parents present in childhood and adult outcomes: the child block's beta_P (PSID, 2026-10-20).

WP7 of IGE/proposals/fable_10h_plan_paperA.md. Paper A's child block maps family income by childhood age and the
presence of both parents into adult outcomes (sec6 'What the model takes from this'); the identification plan
(IGE/proposals/paperA_identification_plan.md, Section 1.6, 'Child-block slopes') sets beta_P = the PSID association of
the share of childhood with both parents present with adult log earnings, with Section 6's controls (high), 0 (low).
This script estimates it. Nothing in IGE/19, IGE/20, IGE/22 or IGE/paperA_model is edited; 19's child functions are
imported (child_frame, design, measures, men_panel), its main() is not run. No sibling comparisons (no family FE).

Reads (read only): IGE/data/psid_person_year.pkl (1), psid_child_exposure.pkl (9), psid_kids.pkl (1),
psid_displacement.pkl (19); the PSID individual file through 9.individual() (education); the family-file hours /
AFDC / food stamps through 9.family(), cached by 76 in IGE/data/sepmoth_fam9.pkl (person-level, git-ignored; rebuilt
if absent). Writes (aggregates only):
  IGE/output/parents_present_outcomes.csv   every estimate (table, sample, spec, outcome, term, coef, se, p, n, ...)
  IGE/output/parents_present_outcomes.md    tables

CHILDREN. Children of psid_child_exposure.pkl (CAH children with a PSID id, and other SRC + SEO persons first seen as
the head's child), born 1968-1995, Black / White (head's race in the first unit the child is seen in), with at least
3 observed childhood interviews at ages 0-17 (age = interview year - birth year) in which they live in a family unit.
PARENTS AT BIRTH: the mother (CAH mother, else the female head / wife of the first unit) and the father (CAH father,
else the male head of the first unit; for a CAH child without a father record, the male head of the first unit if the
mother is his wife there and the child is first seen at 0-2). BOTH PARENTS PRESENT in a childhood year: the head and
the wife / "wife" of the child's family unit are the mother and the father at birth (either way round). A child born
to a mother without a partner in the PSID has both = 0 throughout. Shares: share_both = years with both / observed
years at 0-17; share_both_05 (ages 0-5, >= 1 observed year) and share_both_617 (ages 6-17, >= 2 observed years).
Alternative: share_two = years in a unit with a male head and a wife / "wife" (any two adults as parents, step-parents
included).

ADULT OUTCOMES (the child as head or wife; earnings = own labor income, 2000 $, zeros kept, as IGE/1 and 19):
  log_earn     log mean earnings over ages 25-55, >= 3 years (IGE/1's psid_kids definition, recomputed here)
  log_e3040    log mean earnings over ages 30-40, >= 2 years (the plan's 'mean 30-40 where available')
  rank_earn    percentile of log_earn within 5-year birth cohorts of the sample
  educ         highest completed grade (individual file), children observed at 25+.
CONTROLS (Section 6): female, birth-year FE, parental education (max of the two parents at birth: <12, 12, 13-15, 16+,
missing), + Black in pooled rows. Income: lfinc05 / lfinc617 = log mean family income of the child's unit over ages
0-5 / 6-17 (IGE/9; 2000 $).
SPECIFICATIONS: (A) share_both + controls (total association); (B) + lfinc05 + lfinc617 (presence net of family
income: beta_P for a child block that carries income separately); (C) share_both_05 + share_both_617 + lfinc05 +
lfinc617 + controls (absence by childhood age); (D) as B with share_two; (E) father's displacement sample (19's design:
father figure first displaced at 0-17 vs never, father figure working before the (pseudo) event, controls' pseudo age
= treated median): treat + share_both + lpre (log family income in the 3 years before the (pseudo) event) + controls,
and + lpost (log family income in the 3 years after): the income and the presence channels in one regression.
INFERENCE: OLS, s.e. clustered by 1968 family (CR1); *** p<0.01, ** p<0.05, * p<0.1. Unweighted (SRC + SEO).
Associations, not causal effects: who separates differs in ways the controls do not capture.
"""
import importlib.util
import os
import warnings

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import statsmodels.api as sm  # noqa: E402

from common import DATA, OUT, HERE, stars, lifetime  # noqa: E402

warnings.simplefilter("ignore", FutureWarning)
warnings.simplefilter("ignore", RuntimeWarning)
pd.options.mode.chained_assignment = None


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


P19 = _load("p19", "19.FatherDisplacement.py")
psid9 = P19.psid9
FAM_CACHE = DATA / "sepmoth_fam9.pkl"
BY_LO, BY_HI = 1968, 1995
ROWS = []
YS = [("log_earn", "Log earnings 25-55"), ("log_e3040", "Log earnings 30-40"), ("rank_earn", "Earnings rank"),
      ("educ", "Years of schooling")]
LAB = {"share_both": "Share of childhood with both parents", "share_both_05": "Share with both parents, ages 0-5",
       "share_both_617": "Share with both parents, ages 6-17", "share_two": "Share in a two-adult unit",
       "lfinc05": "Log family income, ages 0-5", "lfinc617": "Log family income, ages 6-17",
       "treat": "Father figure displaced at 0-17", "lpre": "Log family income before (pseudo) event",
       "lpost": "Log family income after (pseudo) event", "female": "Female"}


def ecat(e):
    return pd.cut(e, [0, 11, 12, 15, 17], labels=["lt12", "12", "13_15", "16p"]).astype(str).replace("nan", "miss")


def creg(df, y, xs, ctrl, fe):
    cols = list(dict.fromkeys([y, *xs, *ctrl, *fe, "fam68"]))
    q = df[cols].replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)
    Z = q[list(dict.fromkeys(xs + ctrl))].astype(float)
    for f in fe:
        Z = Z.join(pd.get_dummies(q[f].astype(str), prefix=f, drop_first=True, dtype=float))
    Z = Z.loc[:, Z.std() > 0]
    Z.insert(0, "const", 1.0)
    r = sm.OLS(q[y].astype(float), Z).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(q["fam68"])[0]})
    est = {v: (r.params[v], r.bse[v], r.pvalues[v]) for v in xs if v in r.params}
    return est, dict(n=int(r.nobs), clusters=int(q["fam68"].nunique()), mean=float(q[y].mean()),
                     xmean={v: float(q[v].mean()) for v in xs})


def cell(b, se, p, d=3):
    pv = "<0.001" if p < 0.001 else f"{p:.3f}"
    return f"{b:,.{d}f}{stars(p)} ({se:,.{d}f}; p={pv})"


def md_table(header, rows):
    out = ["| | " + " | ".join(header) + " |", "|---|" + "---|" * len(header)]
    out += ["| " + lab + " | " + " | ".join(v) + " |" for lab, v in rows]
    return "\n".join(out)


def panel(df, xs, ctrl, spec, sample, show=None):
    """Run every outcome; return md rows for the terms in show."""
    show = show or xs
    q = df if sample == "Pooled" else df[df["race"] == sample]
    c = ctrl + (["black"] if sample == "Pooled" else [])
    res = {}
    for y, _ in YS:
        try:
            est, info = creg(q, y, xs, c, ["birth_year", "pe"])
        except Exception as exc:                       # too few observations
            print("skip", spec, sample, y, exc)
            continue
        res[y] = (est, info)
        for v, (b, se, p) in est.items():
            ROWS.append(dict(spec=spec, sample=sample, outcome=y, term=v, coef=b, se=se, p=p, n=info["n"],
                             clusters=info["clusters"], ymean=info["mean"], xmean=info["xmean"].get(v)))
    rows = []
    for v in show:
        rows.append((LAB.get(v, v), [cell(*res[y][0][v], d=2 if y == "rank_earn" else 3)
                                     if y in res and v in res[y][0] else "" for y, _ in YS]))
    rows.append(("Mean of outcome / of first regressor",
                 [f"{res[y][1]['mean']:.3f} / {res[y][1]['xmean'][xs[0]]:.3f}" if y in res else "" for y, _ in YS]))
    rows.append(("N children / clusters", [f"{res[y][1]['n']:,} / {res[y][1]['clusters']:,}" if y in res else ""
                                           for y, _ in YS]))
    return rows


def main():
    OUT.mkdir(exist_ok=True)
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    kx = pd.read_pickle(DATA / "psid_child_exposure.pkl")
    pk = pd.read_pickle(DATA / "psid_kids.pkl")
    disp = pd.read_pickle(DATA / "psid_displacement.pkl")
    if FAM_CACHE.exists():
        fam = pd.read_pickle(FAM_CACHE)
    else:
        fam = psid9.family()
        fam.to_pickle(FAM_CACHE)
    ind = psid9.individual()[0]
    educ = ind.set_index("pid")["educ"]

    # ---- family units: head and wife of each (wave, int)
    hd = py[py["head"]][["wave", "int", "pid", "female"]].drop_duplicates(["wave", "int"]).rename(
        columns={"pid": "h_pid", "female": "h_fem"})
    wf = py[py["wife"]][["wave", "int", "pid"]].drop_duplicates(["wave", "int"]).rename(columns={"pid": "w_pid"})
    fu = hd.merge(wf, on=["wave", "int"], how="left")

    # ---- children and parents at birth
    K = kx[kx["birth_year"].between(BY_LO, BY_HI) & kx["race"].isin(["Black", "White"])].copy()
    cr = py[py["pid"].isin(K["pid"])][["pid", "wave", "int"]].merge(fu, on=["wave", "int"], how="left")
    cr = cr.merge(K[["pid", "birth_year", "mom_pid", "dad_pid"]], on="pid")
    cr["age"] = cr["wave"] - cr["birth_year"]
    cr = cr[cr["age"].between(0, 17) & (cr["h_pid"] != cr["pid"])].sort_values(["pid", "wave"])
    cr = cr.drop_duplicates(["pid", "wave"])
    first = cr.groupby("pid").first()
    fill = (first["h_fem"] == 0) & (first["w_pid"] == first["mom_pid"]) & (first["age"] <= 2)
    dad_fill = first["h_pid"].where(fill)
    K["father"] = K["dad_pid"].fillna(K["pid"].map(dad_fill))
    cr["father"] = cr["pid"].map(K.set_index("pid")["father"])
    m_, f_ = cr["mom_pid"].to_numpy(float), cr["father"].to_numpy(float)
    h_, w_ = cr["h_pid"].to_numpy(float), cr["w_pid"].to_numpy(float)
    cr["both"] = (((h_ == f_) & (w_ == m_)) | ((h_ == m_) & (w_ == f_))).astype(float)
    cr["two"] = ((cr["h_fem"] == 0) & cr["w_pid"].notna()).astype(float)
    g = cr.groupby("pid")
    K["n_child_obs"] = K["pid"].map(g.size()).fillna(0)
    K["share_both"] = K["pid"].map(g["both"].mean())
    K["share_two"] = K["pid"].map(g["two"].mean())
    for lab, lo, hi, nmin in (("05", 0, 5, 1), ("617", 6, 17, 2)):
        gg = cr[cr["age"].between(lo, hi)].groupby("pid")
        s, n = gg["both"].mean(), gg.size()
        K[f"share_both_{lab}"] = K["pid"].map(s.where(n >= nmin))
    K = K[K["n_child_obs"] >= 3].copy()
    pe = np.fmax(educ.reindex(K["mom_pid"].fillna(-1)).to_numpy(), educ.reindex(K["father"].fillna(-1)).to_numpy())
    K["pe"] = ecat(pd.Series(pe, index=K.index))
    K["black"] = (K["race"] == "Black").astype(float)
    K["female"] = K["female"].astype(float)

    # ---- adult outcomes
    a = py[(py["head"] | py["wife"]) & py["pid"].isin(K["pid"])].dropna(subset=["earn"])
    e1 = lifetime(a[a["age"].between(25, 55)], "earn", min_obs=3)
    e2 = lifetime(a[a["age"].between(30, 40)], "earn", min_obs=2)
    K["log_earn"] = K["pid"].map(e1["log"])
    K["log_e3040"] = K["pid"].map(e2["log"])
    coh = K["birth_year"] // 5
    K["rank_earn"] = K.groupby(coh)["log_earn"].rank(pct=True) * 100
    adult_seen = set(py.loc[py["age"] >= 25, "pid"])
    K["educ"] = K["pid"].map(educ).where(K["pid"].isin(adult_seen))
    chk = K[["pid", "log_earn"]].merge(pk[["pid", "log_earn"]], on="pid", suffixes=("", "_pk")).dropna()
    corr_pk = chk[["log_earn", "log_earn_pk"]].corr().iloc[0, 1] if len(chk) else np.nan
    print(f"children born {BY_LO}-{BY_HI}, >= 3 childhood years: {len(K):,}; with log_earn {K.log_earn.notna().sum():,}"
          f"; corr with psid_kids log_earn {corr_pk:.3f} (N {len(chk):,})", flush=True)

    md = ["# Both parents present in childhood and adult outcomes (beta_P for the child block)", "",
          "Built by `IGE/79.ParentsPresentOutcomes.py` (2026-10-20; WP7 of `IGE/proposals/fable_10h_plan_paperA.md`);"
          " definitions in its docstring. PSID children born 1968-1995 (SRC + SEO, unweighted), Black / White, "
          ">= 3 childhood interviews at 0-17. Both parents present = the head and wife of the child's family unit "
          "are the mother and the father at birth. Controls in every column: female, birth-year FE, parental "
          "education (max of the two parents; 5 groups), + Black in pooled rows. S.e. clustered by 1968 family; "
          "*** p<0.01, ** p<0.05, * p<0.1. No sibling comparisons. Associations, not causal effects.", ""]

    # ---- descriptives
    rows = []
    for race in ("Black", "White"):
        q = K[K["race"] == race]
        rows.append((race, [f"{len(q):,}", f"{q['share_both'].mean():.3f}", f"{(q['share_both'] == 1).mean():.3f}",
                            f"{(q['share_both'] == 0).mean():.3f}", f"{q['share_both_05'].mean():.3f}",
                            f"{q['share_both_617'].mean():.3f}", f"{q['share_two'].mean():.3f}",
                            f"{q['log_earn'].notna().sum():,}", f"{q['log_e3040'].notna().sum():,}",
                            f"{q['educ'].notna().sum():,}"]))
        for v in ("share_both", "share_both_05", "share_both_617", "share_two"):
            ROWS.append(dict(spec="descriptive", sample=race, outcome=v, term="mean", coef=q[v].mean(), n=len(q)))
    md += ["## 1. Children and the share of childhood with both parents", "",
           md_table(["Children", "Mean share both", "Share = 1", "Share = 0", "Mean share 0-5", "Mean share 6-17",
                     "Mean share two-adult unit", "N log earnings 25-55", "N log earnings 30-40", "N schooling"],
                    rows), "",
           f"Check: log earnings 25-55 recomputed here vs IGE/1's psid_kids.pkl: correlation {corr_pk:.3f} "
           f"(N {len(chk):,}).", ""]

    ctrl = ["female"]
    hdr = [lab for _, lab in YS]
    for spec, xs, show, title, note in (
            ("A", ["share_both"], None, "2. (A) Total association: share of childhood with both parents",
             "No income controls: presence and everything that comes with it (including the income it brings)."),
            ("B", ["share_both", "lfinc05", "lfinc617"], None,
             "3. (B) Net of family income by childhood age: beta_P for the child block",
             "The child block carries family income by childhood age separately; the coefficient on the share is the "
             "presence slope beta_P (whole childhood with both parents vs none)."),
            ("C", ["share_both_05", "share_both_617", "lfinc05", "lfinc617"], None,
             "4. (C) Absence by childhood age (0-5 vs 6-17), net of income", ""),
            ("D", ["share_two", "lfinc05", "lfinc617"], None,
             "5. (D) Alternative: any two-adult unit (step-parents included), net of income", "")):
        rows = []
        for race in ("Black", "White", "Pooled"):
            pr = panel(K, xs, ctrl, spec, race, show)
            rows += [(f"{race}: {lab}", v) for lab, v in pr]
        md += ["## " + title, "", note, "", md_table(hdr, rows), ""] if note else \
              ["## " + title, "", md_table(hdr, rows), ""]
        print("spec", spec, flush=True)

    # ---- (E) displacement sample: both channels in one regression
    m = P19.men_panel(py, fam)
    Kc, ff, inc = P19.child_frame(py, m, kx, pk, ind)
    hw = py[(py["head"] & (py["female"] == 1)) | py["wife"]][["pid", "wave", "int", "head"]]
    hw = hw.merge(fam[["wave", "int", "hh", "wh"]], on=["wave", "int"], how="left")
    hw["hrs"] = np.where(hw["head"], hw["hh"], hw["wh"])
    H = hw.assign(year=hw["wave"] - 1).dropna(subset=["hrs"]).drop_duplicates(["pid", "year"]).set_index(
        ["pid", "year"])["hrs"]
    ev = disp.loc[disp["main"] == 1, ["pid", "year"]]
    b, astar = P19.design(Kc, ff, ev, 0, 17)
    b = P19.measures(b, m, inc, H)
    keep = ["pid", "fam68", "race", "black", "female", "pe", "share_both", "share_both_05", "share_both_617",
            "lfinc05", "lfinc617"] + [y for y, _ in YS]
    b = b[["pid", "treat", "lpre", "lpost", "birth_year"]].merge(K[keep], on="pid", how="inner")
    rows = []
    for race in ("Black", "White", "Pooled"):
        for spec, xs in (("E1", ["treat", "share_both", "lpre"]), ("E2", ["treat", "share_both", "lpre", "lpost"])):
            pr = panel(b, xs, ctrl, spec, race)
            rows += [(f"{race}, {spec}: {lab}", v) for lab, v in pr]
    md += ["## 6. (E) Father's displacement sample: the income and presence channels in one regression", "",
           f"19's design: children whose father figure was first displaced (closure or layoff) at 0-17 vs never "
           f"displaced at 0-17 (controls' pseudo event age {astar}); father figure working before the (pseudo) "
           "event; children of section 1 only. E1: treat + share of childhood with both parents + log family income "
           "in the 3 years before the (pseudo) event; E2: + log family income in the 3 years after.", "",
           md_table(hdr, rows), ""]
    print("spec E", flush=True)

    pd.DataFrame(ROWS).to_csv(OUT / "parents_present_outcomes.csv", index=False)
    (OUT / "parents_present_outcomes.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
