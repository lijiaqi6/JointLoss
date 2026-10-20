r"""Paper B, Fable review Item 3 (proposals/fable_review_paperB.md 3.6): is the convergence of sons of richer parents
on their fathers' jobs the inheritance of a family business? Self-employment split (2026-10-17).

The finding (35.EarlyIndustryLatePayoff.py, Sections F2, F7, F8): whether a son works in his father's occupation group x
industry group cell does not depend on ln parental income at 25-34 (0.004) but does at 35-55 (0.031**); in the father's
occupation group the 35-55 gradient is White 0.099***, Black 0.024; rich White vs rich Black sons 0.131***; within sons
observed in both windows, sons of richer parents who are in the father's cell at 25-34 leave it less (-0.167**, 137
sons). Fable: if this is mostly self-employed sons entering the family firm (farms, proprietors, professional
practices), the right reading is business / wealth transmission, not networks.

DATA (read only): 32.IndustryCareers.py's PSID son panel (male heads 25-55; occupation group occ11 and industry group
igrp; father = 24's fpid, male head of the son's family at 16, his codes at son ages 12-18, r.attrs['fathers']),
loaded through 35's module; PSID 'work for someone else (1), both someone else and self (2), self only (3)' for the
head's main job, waves 1976-2023 (25.JointJobLoss.py cache data/joint_job_loss_selfemp.pkl; 1968-75 not asked in this
form).
DEFINITIONS
  son self-employed (son-year) = code 2 or 3 at the interview (1 = 0; other codes missing).
  father self-employed = at least half of the father's valid head-wave codes are 2 or 3, over the waves 1976+ in which
    the son is 10-25 (sons born before 1951 have none); 'father ever self-employed' = any such wave.
  father's cell = his modal occ11 x igrp over the fathers' rows (son 12-18), as 35; father's occupation group = 32's
    focc11; son in the father's cell / occupation group as 35 F2 / F7.
DESIGN: son-year linear probability models, Lee-Solon controls (quartics in (A - 45)/10 and (age - 40)/10), clusters
1968 family; pooled = Black + White weighted (wpool), by race unweighted. Change after 35 from one regression with ln
parental income x (age >= 35). The rich-White-vs-rich-Black contrast as 35 F7(b): race x pooled parental-income tercile
cells (reference Black tercile 1) + ln parental income, son-years 35-55. Within-son transitions as 35 F8 (modal cell at
25-34 and at 35-55). Descriptive: sons select into jobs.
Writes output/father_job_selfemp.csv and .md.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import DATA, OUT, stars  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R35 = _load("e35", "35.EarlyIndustryLatePayoff.py")
D32, D27 = R35.D32, R35.D27
CSV = []


def fmt(e, se, p):
    if e is None or not np.isfinite(e):
        return ""
    pv = "<0.001" if p < 0.001 else f"{p:.3f}"
    return f"{e:.3f}{stars(p)} ({se:.3f}; p={pv})"


def wls(d, y, xs, w=None):
    """WLS with Lee-Solon controls, clusters 1968 family; returns (params, cov, n, sons, clusters, mean)."""
    ctrl = [f"A{k}" for k in range(1, 5)] + [f"C{k}" for k in range(1, 5)]
    d = d.dropna(subset=[y, *xs, *ctrl, "fam68"] + ([w] if w else []))
    if w:
        d = d[d[w] > 0]
    X = sm.add_constant(d[list(xs) + ctrl].astype(float), has_constant="add")
    mod = sm.WLS(d[y].astype(float), X, weights=d[w]) if w else sm.OLS(d[y].astype(float), X)
    r = mod.fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d["fam68"])[0]})
    return r.params, r.cov_params(), len(d), d["pid"].nunique(), d["fam68"].nunique(), \
        float(np.average(d[y], weights=d[w] if w else None))


def lc(res, terms):
    p, V = res[0], res[1]
    e = sum(c * p[k] for k, c in terms)
    v = sum(c1 * c2 * V.loc[k1, k2] for k1, c1 in terms for k2, c2 in terms)
    se = np.sqrt(v)
    return e, se, 2 * norm.sf(abs(e / se)) if se > 0 else np.nan


def rec(tab, sample, group, term, est, **kw):
    CSV.append(dict(table=tab, sample=sample, group=group, term=term, coef=est[0], se=est[1], p=est[2], **kw))


def build():
    W = D32.ind_crosswalks()
    XWD = D27.crosswalks()
    M = D32.morg_measures(D32.morg_micro(W, XWD))
    r = D32.son_panel(W, M)
    f = r.attrs["fathers"].copy()
    r.attrs = {}
    f["og"] = f["occ11"] * 100 + f["f_igrp"]
    fog = f.dropna(subset=["og"]).groupby("pid")["og"].agg(lambda v: v.value_counts().index[0])
    r["og"] = (r["occ11"] * 100 + r["igrp"]).where(r["occ11"].notna() & r["igrp"].notna())
    r["fog"] = r["pid"].map(fog)
    v = r["valid"] & r["lw"].notna() & r["race"].isin(["Black", "White"])
    r["f_cell"] = (r["og"] == r["fog"]).astype(float).where(v & r["og"].notna() & r["fog"].notna())
    r["f_occg"] = (r["occ11"] == r["focc11"]).astype(float).where(v & r["occ11"].notna() & r["focc11"].notna())
    for k in range(1, 5):
        r[f"A{k}"] = ((r["A"] - 45) / 10) ** k
        r[f"C{k}"] = (r["C"] / 10) ** k
    # self-employment
    X = pd.read_pickle(DATA / "joint_job_loss_selfemp.pkl")["X"][["wave", "int", "h_se"]]
    X = X.drop_duplicates(["wave", "int"])
    se = X["h_se"]
    X["se"] = np.where(se.isin([2, 3]), 1.0, np.where(se == 1, 0.0, np.nan))
    r = r.merge(X[["wave", "int", "se"]], on=["wave", "int"], how="left").rename(columns={"se": "son_se"})
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    hd = py[py["head"] & (py["wave"] >= 1976)][["pid", "wave", "int"]].merge(X[["wave", "int", "se"]],
                                                                             on=["wave", "int"], how="inner")
    sons = r.drop_duplicates("pid")[["pid", "fpid", "birth_year"]].dropna(subset=["fpid"])
    fs = sons.merge(hd.rename(columns={"pid": "fpid"}), on="fpid", how="inner")
    fs = fs[(fs["wave"] - fs["birth_year"]).between(10, 25) & fs["se"].notna()]
    fse = fs.groupby("pid")["se"].agg(["mean", "max", "count"])
    r["f_se"] = r["pid"].map((fse["mean"] >= 0.5).astype(float))
    r["f_se_ever"] = r["pid"].map(fse["max"])
    r["late"] = (r["age"] >= 35).astype(float)
    r["lyp_c"] = r["lyp"] - r.drop_duplicates("pid")["lyp"].mean()
    r["lyp_late"] = r["lyp_c"] * r["late"]
    return r, f


GROUPS = [("P", "Pooled (weighted)"), ("B", "Black"), ("W", "White")]


def subset(d, g):
    if g == "P":
        return d, "wpool"
    return d[d["race"] == {"B": "Black", "W": "White"}[g]], None


def sec_desc(r, md):
    v = r[r["valid"] & r["lw"].notna() & r["race"].isin(["Black", "White"]) & r["age"].between(25, 55)]
    s1 = v.drop_duplicates("pid")
    L = ["## 0. Self-employment of fathers and sons", "",
         "| | Black | White |", "|---|---|---|"]
    for lab, col in (("sons with a father's self-employment code", "f_se"),):
        L.append(f"| {lab} | " + " | ".join(f"{int(s1.loc[s1['race'] == g, col].notna().sum()):,} of "
                                             f"{int((s1['race'] == g).sum()):,}" for g in ("Black", "White")) + " |")
    for lab, col in (("father self-employed (>= half of his waves)", "f_se"), ("father ever self-employed", "f_se_ever")):
        L.append(f"| {lab} | " + " | ".join(f"{s1.loc[s1['race'] == g, col].mean():.3f}" for g in ("Black", "White"))
                 + " |")
    for lo, hi in ((25, 34), (35, 55)):
        z = v[v["age"].between(lo, hi)]
        L.append(f"| son-years self-employed, {lo}-{hi} | " + " | ".join(
            f"{z.loc[z['race'] == g, 'son_se'].mean():.3f}" for g in ("Black", "White")) + " |")
    for lo, hi in ((25, 34), (35, 55)):
        z = v[v["age"].between(lo, hi) & (v["f_cell"] == 1)]
        L.append(f"| son-years in the father's cell, {lo}-{hi}: N / son self-employed / father self-employed | " +
                 " | ".join(f"{int((z['race'] == g).sum()):,} / {z.loc[z['race'] == g, 'son_se'].mean():.3f} / "
                            f"{z.loc[z['race'] == g, 'f_se'].mean():.3f}" for g in ("Black", "White")) + " |")
        z = v[v["age"].between(lo, hi) & (v["f_cell"] == 0)]
        L.append(f"| son-years not in the father's cell, {lo}-{hi}: son SE / father SE | " +
                 " | ".join(f"{z.loc[z['race'] == g, 'son_se'].mean():.3f} / {z.loc[z['race'] == g, 'f_se'].mean():.3f}"
                            for g in ("Black", "White")) + " |")
    L.append("")
    # which cells are inherited at 35-55
    z = v[v["age"].between(35, 55) & (v["f_cell"] == 1)]
    top = (z.groupby("og").agg(son_years=("pid", "size"), sons=("pid", "nunique"), son_se=("son_se", "mean"),
                               father_se=("f_se", "mean"), white=("race", lambda x: (x == "White").mean()),
                               lyp=("lyp", "mean"))
           .sort_values("son_years", ascending=False).head(12))
    occn = getattr(R35, "OCC11N", None) or getattr(D27, "OCC11", None)
    ign = getattr(D32, "IGRP", None)
    L += ["### 0b. The father-son cells held at 35-55 (top 12 by son-years)", "",
          "| occupation group x industry group code | son-years | sons | son self-employed | father self-employed | "
          "White share | mean ln parental income |", "|---|---|---|---|---|---|---|"]
    for og, t in top.iterrows():
        L.append(f"| {int(og // 100)} x {int(og % 100)} | {int(t.son_years):,} | {int(t.sons):,} | {t.son_se:.2f} | "
                 f"{t.father_se:.2f} | {t.white:.2f} | {t.lyp:.2f} |")
    for og in top.index:
        CSV.append(dict(table="0b inherited cells", sample=str(int(og)), group="", term="", coef=top.loc[og, "son_years"],
                        se=np.nan, p=np.nan, son_se=top.loc[og, "son_se"], father_se=top.loc[og, "father_se"]))
    L += ["", f"Occupation groups (27's 11 groups) and industry groups (32's 33) are numbered as in those scripts "
          f"(occ11: {occn if occn is not None else 'see 27.CareerWageGrowth.group_of'}; igrp: "
          f"{'32.IGRP' if ign is not None else 'see 32'}).", ""]
    md += L


SAMPLES = [("All sons (35)", lambda d: d),
           ("Father not self-employed", lambda d: d[d["f_se"] == 0]),
           ("Father self-employed", lambda d: d[d["f_se"] == 1]),
           ("Son-years not self-employed", lambda d: d[d["son_se"] == 0]),
           ("Neither father nor son self-employed", lambda d: d[(d["f_se"] == 0) & (d["son_se"] == 0)]),
           ("Father's code known (any)", lambda d: d[d["f_se"].notna()])]


def sec_gradient(r, md):
    v = r[r["valid"] & r["lw"].notna() & r["race"].isin(["Black", "White"]) & r["age"].between(25, 55)]
    for y, ylab in (("f_cell", "son in the father's cell"), ("f_occg", "son in the father's occupation group")):
        hdr = [f"({i + 1}) {lab}" for i, (lab, _) in enumerate(SAMPLES)]
        panels = []
        for g, gname in GROUPS:
            rows = {k: [] for k in ("25-34", "35-55", "change", "n")}
            for lab, fn in SAMPLES:
                d, w = subset(fn(v[v[y].notna()]), g)
                try:
                    a = wls(d[d["age"].between(25, 34)], y, ["lyp"], w)
                    b = wls(d[d["age"].between(35, 55)], y, ["lyp"], w)
                    c = wls(d, y, ["lyp", "lyp_late", "late"], w)
                except Exception:
                    for k in rows:
                        rows[k].append("")
                    continue
                ea, eb, ec = lc(a, [("lyp", 1)]), lc(b, [("lyp", 1)]), lc(c, [("lyp_late", 1)])
                rows["25-34"].append(fmt(*ea))
                rows["35-55"].append(fmt(*eb))
                rows["change"].append(fmt(*ec))
                rows["n"].append(f"{b[2]:,} / {b[3]:,}; mean {b[5]:.3f}")
                for t, e in (("25-34", ea), ("35-55", eb), ("change", ec)):
                    rec(f"1 {ylab} on ln parental income", lab, gname, t, e, n=b[2], sons=b[3], mean=b[5])
            panels.append((gname, [("ln parental income, 25-34", rows["25-34"]),
                                   ("ln parental income, 35-55", rows["35-55"]),
                                   ("change: ln parental income x (age >= 35)", rows["change"]),
                                   ("N son-years / sons at 35-55; mean", rows["n"])]))
        md += [f"## 1. {ylab.capitalize()} on ln parental income, by self-employment", "",
               "Son-year LPMs; Lee-Solon controls; clusters 1968 family; pooled weighted, races unweighted. The change "
               "row is from one regression on 25-55 with ln parental income x (age >= 35) and the age >= 35 dummy.", ""]
        md += R35.table(hdr, panels) if hasattr(R35, "table") else []


def sec_richwhite(r, md):
    v = r[r["valid"] & r["lw"].notna() & r["race"].isin(["Black", "White"]) & r["age"].between(35, 55)].copy()
    rt = [("bT2", "Black", 2), ("bT3", "Black", 3), ("wT1", "White", 1), ("wT2", "White", 2), ("wT3", "White", 3)]
    for c_, race, tq in rt:
        v[c_] = ((v["race"] == race) & (v["terc"] == tq)).astype(float).where(v["terc"].notna())
    xs = [c for c, _, _ in rt] + ["lyp"]
    hdr = [f"({i + 1}) {lab}" for i, (lab, _) in enumerate(SAMPLES)]
    panels = []
    for y, ylab in (("f_occg", "father's occupation group"), ("f_cell", "father's cell")):
        rows = {"wT3 - bT3": [], "wT3 - wT1": [], "n": [], "nb3": []}
        for lab, fn in SAMPLES:
            d = fn(v[v[y].notna()])
            try:
                a = wls(d, y, xs, "wpool")
            except Exception:
                for k in rows:
                    rows[k].append("")
                continue
            e1, e2 = lc(a, [("wT3", 1), ("bT3", -1)]), lc(a, [("wT3", 1), ("wT1", -1)])
            rows["wT3 - bT3"].append(fmt(*e1))
            rows["wT3 - wT1"].append(fmt(*e2))
            rows["n"].append(f"{a[2]:,} / {a[3]:,}")
            nb3 = d.loc[d["bT3"] == 1, "pid"].nunique()
            rows["nb3"].append(f"{nb3:,}")
            rec(f"2 rich White vs rich Black, {ylab}", lab, "P", "wT3 - bT3", e1, n=a[2], sons=a[3], black_t3=nb3)
            rec(f"2 rich White vs rich Black, {ylab}", lab, "P", "wT3 - wT1", e2, n=a[2], sons=a[3])
        panels.append((f"Outcome: son in the {ylab}, 35-55", [
            ("rich White - rich Black (tercile 3)", rows["wT3 - bT3"]),
            ("rich White - poor White (tercile 3 - tercile 1)", rows["wT3 - wT1"]),
            ("N son-years / sons", rows["n"]), ("Black sons in tercile 3", rows["nb3"])]))
    md += ["## 2. Rich White vs rich Black sons in the father's occupation / cell at 35-55, by self-employment", "",
           "As 35 F7(b): race x pooled parental-income tercile cells (reference Black tercile 1) + ln parental income, "
           "Lee-Solon controls, pooled weighted, clusters 1968 family.", ""]
    md += R35.table(hdr, panels)


def sec_keep(r, md):
    v = r[r["valid"] & r["lw"].notna() & r["race"].isin(["Black", "White"]) & r["og"].notna() & r["fog"].notna()]
    mode = lambda s: s.value_counts().index[0]  # noqa: E731
    e = v[v["age"].between(25, 34)].groupby("pid")["og"].agg(mode)
    l_ = v[v["age"].between(35, 55)].groupby("pid")["og"].agg(mode)
    P = pd.DataFrame({"m25": e, "m35": l_}).dropna()
    first = v.drop_duplicates("pid").set_index("pid")
    for c in ("race", "lyp", "fam68", "birth_year", "fog", "f_se", "terc"):
        P[c] = first[c].reindex(P.index)
    sse = v[v["age"].between(35, 55)].groupby("pid")["son_se"].mean()
    P["son_se35"] = (sse.reindex(P.index) >= 0.5).astype(float).where(sse.reindex(P.index).notna())
    P["in25"] = (P["m25"] == P["fog"]).astype(float)
    P["in35"] = (P["m35"] == P["fog"]).astype(float)
    P["leave"] = (1 - P["in35"]).where(P["in25"] == 1)
    P["enter"] = P["in35"].where(P["in25"] == 0)
    P["coh"] = (P["birth_year"] - 1960) / 10
    P["coh2"] = P["coh"] ** 2
    P = P.reset_index().rename(columns={"index": "pid"})
    L = ["## 3. Within sons: keeping the father's cell, by self-employment (35 F8)", "",
         "Sons with a modal cell in both 25-34 and 35-55 and a father's cell. Counts, then LPMs of leaving (in at "
         "25-34, out at 35-55) and entering on ln parental income with a quadratic in birth cohort; clusters 1968 "
         "family; unweighted.", "",
         "| Group | sons | in at both (stay) | leave | enter | stayers: son self-employed at 35-55 | stayers: father "
         "self-employed | all sons: son SE / father SE |", "|---|---|---|---|---|---|---|---|"]
    for lab, z in (("All", P), ("Black", P[P["race"] == "Black"]), ("White", P[P["race"] == "White"])):
        st = z[(z["in25"] == 1) & (z["in35"] == 1)]
        L.append(f"| {lab} | {len(z):,} | {len(st):,} | {int((z['leave'] == 1).sum()):,} | "
                 f"{int((z['enter'] == 1).sum()):,} | {st['son_se35'].mean():.2f} (n={st['son_se35'].notna().sum()}) | "
                 f"{st['f_se'].mean():.2f} (n={st['f_se'].notna().sum()}) | {z['son_se35'].mean():.2f} / "
                 f"{z['f_se'].mean():.2f} |")
        CSV.append(dict(table="3 keep counts", sample=lab, group="", term="", coef=len(z), se=np.nan, p=np.nan,
                        stay=len(st), leave=int((z["leave"] == 1).sum()), enter=int((z["enter"] == 1).sum()),
                        stay_son_se=st["son_se35"].mean(), stay_father_se=st["f_se"].mean()))
    L.append("")
    L += ["| Sample | (1) leave on ln parental income | N sons (in at 25-34) | (2) enter on ln parental income | N sons "
          "(out at 25-34) |", "|---|---|---|---|---|"]
    for lab, z in (("All", P), ("Father not self-employed", P[P["f_se"] == 0]),
                   ("Father self-employed", P[P["f_se"] == 1]), ("Son not self-employed at 35-55", P[P["son_se35"] == 0]),
                   ("Neither self-employed", P[(P["f_se"] == 0) & (P["son_se35"] == 0)])):
        cells = []
        for y in ("leave", "enter"):
            d = z.dropna(subset=[y, "lyp"])
            if len(d) < 25 or d[y].nunique() < 2:
                cells += ["", f"{len(d):,}"]
                continue
            X = sm.add_constant(d[["lyp", "coh", "coh2"]].astype(float))
            res = sm.OLS(d[y].astype(float), X).fit(cov_type="cluster",
                                                    cov_kwds={"groups": pd.factorize(d["fam68"])[0]})
            e = (res.params["lyp"], res.bse["lyp"], res.pvalues["lyp"])
            cells += [fmt(*e), f"{len(d):,}"]
            rec(f"3 {y} on ln parental income", lab, "P", y, e, n=len(d))
        L.append(f"| {lab} | " + " | ".join(cells) + " |")
    md += L + [""]


def main():
    OUT.mkdir(exist_ok=True)
    r, f = build()
    print("built", r.shape, flush=True)
    md = ["# Fathers' jobs and self-employment (Fable review, Item 3)", "",
          "Built by `43.FatherJobSelfEmployment.py` (2026-10-17); definitions in its docstring. Every coefficient: "
          "estimate (s.e.; p), *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**", ""]
    sec_desc(r, md)
    sec_gradient(r, md)
    sec_richwhite(r, md)
    sec_keep(r, md)
    (OUT / "father_job_selfemp.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    pd.DataFrame(CSV).to_csv(OUT / "father_job_selfemp.csv", index=False)
    print("done", flush=True)


if __name__ == "__main__":
    main()
