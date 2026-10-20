r"""Paper B, Fable round-2 review items A3, A4, A7 (proposals/fable_review_paperB.md, 2026-10-18): is the racial
difference in the pay-off of schooling a parameter of human capital accumulation, or is it sorting into jobs (access)?

The model of Sec. 7 has two race-specific mechanisms: access to good starting jobs, and the pay-off of schooling in on-the-
job accumulation (gamma_1(r)). If only access differed by race (good jobs accumulate faster, the educated of one race get
more of them), the return to schooling would rise faster with age, and schooling would buy faster same-employer growth,
for that race without any gamma_1(r). The tests that separate the two hold the job fixed:
  A3 (i)  return to a year of schooling (ln hourly wage, ln annual earnings) by age band x race, without and with fixed
          effects for the son's EARLY cell (modal 11 occupation groups x 33 industry groups at 25-34) and for his CURRENT
          cell; PSID, and NLSY79 for the hourly rate;
     (ii) education gradient of same-employer wage growth by race, without and with fixed effects for the cell at the
          first interview of the pair and for the early cell; PSID and NLSY79.
  A4      NLSY79: returns to the AFQT (1 s.d., age-adjusted) and to schooling by age band and race, each alone and
          jointly (the Arcidiacono-Bayer-Hizmo design by race): employer learning predicts a falling schooling and a
          rising AFQT coefficient with experience.
  A7      PSID: the rise of the return to schooling with age net of the calendar rise of the college premium: years of
          schooling x (income year - 1995)/10 added (return evaluated in 1995), and the return within the 1955-69
          birth cohorts. (The NLSY79 is one cohort, so age and calendar are collinear there.)
DATA: 36.SameEmployerGrowthChecks.py's builders (PSID son panel of 32; same-employer pairs; NLSY79 CPS-job panel),
loaded read only. ENGINE: 36's WLS with cluster influence functions over one global cluster index (1968 family / 1979
household); by race unweighted, pooled weighted; controls in every regression: quartic in age, year (round) FE.
Change = mean over bands >= 35 minus mean over bands < 35. DESCRIPTIVE.
Writes output/within_cell_identification.csv and .md.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import OUT  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R36 = _load("s36", "36.SameEmployerGrowthChecks.py")
run, G, lin, cell, tsp, table = R36.run, R36.G, R36.lin, R36.cell, R36.tsp, R36.table
B6 = [(25, 29), (30, 34), (35, 39), (40, 44), (45, 49), (50, 55)]
B2 = [(25, 34), (35, 55)]
GR = [("P", "Pooled Black + White (weighted)"), ("B", "Black"), ("W", "White"), ("BW", "Black - White")]
CSV = []


def rec(tab, group, spec, term, e, **kw):
    b, se, p = tsp(e)
    CSV.append(dict(table=tab, group=group, spec=spec, term=term, coef=b, se=se, p=p, **kw))


def change(tag, y, g, x, bands=B6):
    lo = [b for b in bands if b[0] < 35]
    hi = [b for b in bands if b[0] >= 35]
    return lin([(G(tag, y, a, b, g, x), 1 / len(hi)) for a, b in hi]
               + [(G(tag, y, a, b, g, x), -1 / len(lo)) for a, b in lo])


def mode(v):
    v = v.dropna()
    return v.value_counts().index[0] if len(v) else np.nan


def early_cell(d, col, agecol="age"):
    e = d[d[agecol].between(25, 34) & d[col].notna()].groupby("pid")[col].agg(mode)
    return d["pid"].map(e)


# ================================================================ A3 (i), A7: return to schooling by band
def band_returns(md, data, d, ys, specs, title, note):
    """specs: [(tag, label, xs, fe, sample filter)] all run on the same rows (need = early cell, educ)."""
    for y, ylab in ys:
        for tag, _, xs, fe, flt in specs:
            dd = d if flt is None else d[flt(d)]
            run(f"{tag}_{y}", dd, y, xs, fe=fe, bands=B6, need=["educ", "ecell"])
        panels = []
        for g, gname in GR:
            rows = []
            for lo, hi in B6:
                es = [G(f"{t}_{y}", y, lo, hi, g, "educ") for t, *_ in specs]
                rows.append((f"age {lo}-{hi}", [cell(e) for e in es]))
                for (t, lab, *_), e in zip(specs, es):
                    rec(f"{data} return to schooling, {ylab}", gname, lab, f"{lo}-{hi}", e)
            ch = [change(f"{t}_{y}", y, g, "educ") for t, *_ in specs]
            rows.append(("**change: mean >= 35 minus mean < 35**", [cell(e) for e in ch]))
            for (t, lab, *_), e in zip(specs, ch):
                rec(f"{data} return to schooling, {ylab}", gname, lab, "change", e)
            if g != "BW":
                rows.append(("N son-years (25-29 / 50-55)", [
                    "/".join(f"{R36.RES[R36.K(f'{t}_{y}', y, lo, hi, g, 'educ')]['n']:,}" if R36.K(
                        f"{t}_{y}", y, lo, hi, g, "educ") in R36.RES else "" for lo, hi in (B6[0], B6[-1]))
                    for t, *_ in specs]))
            panels.append((gname, rows))
        # differences between specifications in the B-W change (does the racial difference survive the cells?)
        rows = []
        base = specs[0][0]
        for t, lab, *_ in specs[1:]:
            e = lin([(change(f"{t}_{y}", y, "BW", "educ"), 1.0), (change(f"{base}_{y}", y, "BW", "educ"), -1.0)])
            rows.append((f"B-W change, {lab} minus baseline", [cell(e)]))
            rec(f"{data} return to schooling, {ylab}", "Black - White", lab, "change minus baseline", e)
        md += [f"## {title}: {ylab}", "", note, ""]
        md += table([lab for _, lab, *_ in specs], panels)
        md += table(["difference"], [("", rows)])


# ================================================================ A3 (ii): same-employer growth on schooling within cells
def growth_cells(md, data, s, specs):
    for tag, _, xs, fe in specs:
        run(tag, s, "g", xs, fe=fe, bands=B2, need=["educ", "ecell", "cell0", "lyp"])
    panels = []
    for g, gname in GR:
        rows = []
        for lo, hi in B2:
            for x, xl in (("educ", "years of education"), ("lyp", "ln parental income")):
                es = [G(t, "g", lo, hi, g, x) if x in xs else None for t, _, xs, _ in specs]
                if all(e is None for e in es):
                    continue
                rows.append((f"{xl}, {lo}-{hi}", [cell(e) for e in es]))
                for (t, lab, xs, _), e in zip(specs, es):
                    if e is not None:
                        rec(f"{data} same-employer growth", gname, lab, f"{x}, {lo}-{hi}", e)
            if g != "BW":
                k = R36.K(specs[0][0], "g", lo, hi, g, "educ")
                rows.append((f"N pairs / men, {lo}-{hi}", [f"{R36.RES[k]['n']:,} / {R36.RES[k]['men']:,}"
                                                           if k in R36.RES else ""] + [""] * (len(specs) - 1)))
        panels.append((gname, rows))
    md += [f"## A3 (ii). {data}: same-employer wage growth on schooling, within job cells", "",
           "Same-employer pairs; outcome annualised ln wage growth; controls: quartic in age, year (round) FE, plus the "
           "fixed effects in the header. Common sample: education, ln parental income, the early cell and the cell at "
           "the first interview known. Black - White = difference of the separate regressions.", ""]
    md += table([lab for _, lab, _, _ in specs], panels)


# ================================================================ A4: AFQT and schooling by age, NLSY79
def afqt_returns(md, J):
    specs = [("afq_a", "(1) AFQT alone", ["afqt"]), ("afq_e", "(2) schooling alone", ["educ"]),
             ("afq_ae", "(3) AFQT + schooling", ["afqt", "educ"])]
    for tag, _, xs in specs:
        run(tag, J, "lw", xs, bands=B6, need=["afqt", "educ"])
    panels = []
    for g, gname in GR:
        rows = []
        for x, xl in (("afqt", "AFQT (1 s.d.)"), ("educ", "years of education")):
            for lo, hi in B6:
                es = [G(t, "lw", lo, hi, g, x) if x in xs else None for t, _, xs in specs]
                rows.append((f"{xl}, age {lo}-{hi}", [cell(e) for e in es]))
                for (t, lab, xs), e in zip(specs, es):
                    if e is not None:
                        rec("NLSY79 AFQT and schooling by age", gname, lab, f"{x}, {lo}-{hi}", e)
            ch = [change(t, "lw", g, x) if x in xs else None for t, _, xs in specs]
            rows.append((f"**{xl}: change >= 35 minus < 35**", [cell(e) for e in ch]))
            for (t, lab, xs), e in zip(specs, ch):
                if e is not None:
                    rec("NLSY79 AFQT and schooling by age", gname, lab, f"{x}, change", e)
        panels.append((gname, rows))
    md += ["## A4. NLSY79: returns to the AFQT and to schooling by age band and race", "",
           "ln hourly rate of pay of the main (CPS) job at each round, men 25-55 living with a parent in 1979, AFQT-3 "
           "standardised within birth year; one regression per column and band; controls: quartic in age, round FE. "
           "Employer learning (Altonji-Pierret; Arcidiacono-Bayer-Hizmo) predicts that the schooling coefficient falls "
           "and the AFQT coefficient rises with experience when both are included (column 3).", ""]
    md += table([lab for _, lab, _ in specs], panels)


def main():
    OUT.mkdir(exist_ok=True)
    print("PSID ...", flush=True)
    r, D32, D27, W, M, XWD = R36.psid_build()
    s, sp = R36.psid_pairs(r)
    print("NLSY79 ...", flush=True)
    J, kids = R36.nlsy_build(D32, D27, W, M, XWD)
    n_s, _ = R36.nlsy_samples(J)
    R36.CL = pd.Index(np.unique(np.concatenate([r["fam68"].dropna().unique().astype(float),
                                                J["cl"].dropna().unique().astype(float)])))
    for c in ("educ", "afqt"):
        if c not in J:
            J = J.merge(kids[["pid", c]], on="pid", how="left")
        if c not in n_s:
            n_s = n_s.merge(kids[["pid", c]], on="pid", how="left")
    # PSID cells
    r = r.copy()
    r["og"] = (r["occ11"] * 100 + r["igrp"]).where(r["occ11"].notna() & r["igrp"].notna())
    v = r[r["valid"] & r["lw"].notna() & r["age"].between(25, 55) & r["race"].isin(["Black", "White"])].copy()
    v["ecell"] = early_cell(v, "og")
    v["yfe"], v["cl"] = v["year"], v["fam68"].astype(float)
    v["educ_t"] = v["educ"] * (v["year"] - 1995) / 10
    s = s.copy()
    s["ecell"] = s["pid"].map(v.drop_duplicates("pid").set_index("pid")["ecell"])
    # NLSY79 cells
    j = J[J["lw"].notna() & J["age"].between(25, 55) & J["race"].isin(["Black", "White"])].copy()
    j["ecell"] = early_cell(j, "cell")
    n_s = n_s.copy()
    n_s["ecell"] = n_s["pid"].map(j.drop_duplicates("pid").set_index("pid")["ecell"])
    md = ["# Within-cell identification of the racial difference in the pay-off of schooling (Fable round 2, A3 A4 A7)",
          "", "Built by `45.WithinCellIdentification.py` (2026-10-18); definitions in its docstring. Every coefficient: "
          "estimate (s.e.; p), *** p<0.01, ** p<0.05, * p<0.1; s.e. clustered by 1968 family (PSID) / 1979 household "
          "(NLSY79). **Descriptive.**", ""]
    specs = [("ps0", "(1) baseline (same rows)", ["educ"], (), None),
             ("psE", "(2) + early-cell FE", ["educ"], ("ecell",), None),
             ("psC", "(3) + current-cell FE", ["educ"], ("og",), None),
             ("psT", "(4) + schooling x calendar trend (return in 1995)", ["educ", "educ_t"], (), None),
             ("psH", "(5) born 1955-69 only", ["educ"], (), lambda q: q["birth_year"].between(1955, 1969))]
    print("A3 / A7 PSID ...", flush=True)
    band_returns(md, "PSID", v, [("lw", "ln hourly wage"), ("ly", "ln annual earnings")], specs,
                 "A3 (i) / A7. PSID: return to a year of schooling by age band, within job cells and net of the "
                 "calendar", "Son-years 25-55 with a valid wage, education and an early cell (modal 11 x 33 cell at "
                 "25-34). (2) fixed effects for the early cell; (3) for the current cell; (4) adds schooling x (income "
                 "year - 1995)/10, so the row is the return in 1995; (5) sons born 1955-69. Controls: quartic in age, "
                 "year FE.")
    nspecs = [("ns0", "(1) baseline (same rows)", ["educ"], (), None),
              ("nsE", "(2) + early-cell FE", ["educ"], ("ecell",), None),
              ("nsC", "(3) + current-cell FE", ["educ"], ("cell",), None)]
    print("A3 NLSY79 ...", flush=True)
    band_returns(md, "NLSY79", j, [("lw", "ln hourly rate of pay")], nspecs,
                 "A3 (i). NLSY79: return to a year of schooling by age band, within job cells",
                 "Men 25-55 (born 1957-64, one cohort: age and calendar collinear); hourly rate of pay of the main "
                 "job; early cell = modal 11 x 33 cell at 25-34. Controls: quartic in age, round FE.")
    gspecs = [("pg0", "(1) baseline", ["educ"], ()), ("pgF", "(2) + cell FE, first interview", ["educ"], ("cell0",)),
              ("pgE", "(3) + early-cell FE", ["educ"], ("ecell",)),
              ("pgL", "(4) (2) + ln parental income", ["educ", "lyp"], ("cell0",))]
    print("A3 growth ...", flush=True)
    growth_cells(md, "PSID", s, gspecs)
    growth_cells(md, "NLSY79", n_s, [(t.replace("pg", "ng"), lab, xs, fe) for t, lab, xs, fe in gspecs])
    print("A4 ...", flush=True)
    afqt_returns(md, j)
    (OUT / "within_cell_identification.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    pd.DataFrame(CSV).to_csv(OUT / "within_cell_identification.csv", index=False)
    print("done", flush=True)


if __name__ == "__main__":
    main()
