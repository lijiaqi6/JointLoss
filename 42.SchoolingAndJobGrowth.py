r"""Paper B, Fable review Item 2 (proposals/fable_review_paperB.md): the schooling channel and within- vs between-job
wage growth, by parental income and race (2026-10-17).

Questions (Fable 3.5, 3.7, Item 2):
  A  EDUCATION GRADIENT OF SAME-EMPLOYER WAGE GROWTH BY RACE. Does a year of schooling buy faster wage growth with the
     same employer for White sons and not for Black sons? PSID (32 / 36 same-employer pairs) and NLSY79 (same roster
     employer; AFQT as well). Growth on years of education alone, and with ln parental income.
  B  THE EDUCATION PREMIUM BY AGE BAND AND RACE (Bhuller, Mogstad and Salvanes 2017 JOLE). ln hourly wage and ln annual
     earnings on years of education (and on a BA indicator, education >= 16) by age band 25-29 ... 50-55 and race.
     Does the return to schooling rise with age for White and not for Black sons? Then the wage IGE by band without
     and with years of education: how much of the rise of wage persistence after 35 runs through education?
  C  WITHIN- vs BETWEEN-JOB GROWTH (Altonji, Smith and Vidangos 2013; Topel and Ward 1992). Consecutive interviews 1-2
     years apart (27's transition rows, waves 1985-2023): the son stayed with the employer (27 'stay', no displacement in
     the interval), moved without displacement, or was displaced (plant closure / layoff / firing in an income year
     between the two wage years, psid_displacement.pkl 'main'). Rates of each event, growth conditional on each, and
     the exact split of the gradient of annual wage growth in ln parental income into the three contributions
     g x 1[stay] + g x 1[move] + g x 1[displaced] (they add up to the unconditional gradient on the same pairs).
DESCRIPTIVE: sons select into schooling, employers and moves; nothing here identifies a causal effect.

DATA (read only, through 36.SameEmployerGrowthChecks.py's builders, no edits): PSID son panel of 32 (24's frame: 6.IGEMain
parents, male heads 25-55, valid wage years; ln w = ln earnings - ln hours of income year wave - 1; education = 24's
years of completed education); NLSY79 CPS-job panel of 36 (hourly pay rate of the main job; HGC by 35; AFQT-3
standardised within birth year).
ENGINE: 36's WLS with cluster influence functions over one global cluster index (1968 family / 1979 household), so every
difference between bands, races and specifications has a proper s.e.; by race unweighted, pooled = Black + White
weighted (PSID individual weight; NLSY79 1979 weight). Controls in every regression: quartic in age, year (round) FE.
Writes output/schooling_job_growth.csv and .md.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import DATA, OUT  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R36 = _load("s36", "36.SameEmployerGrowthChecks.py")
run, G, E, lin, cell, tsp, table = R36.run, R36.G, R36.E, R36.lin, R36.cell, R36.tsp, R36.table
B6 = [(25, 29), (30, 34), (35, 39), (40, 44), (45, 49), (50, 55)]
B2 = [(25, 34), (35, 55)]
GR = [("P", "Pooled Black + White (weighted)"), ("B", "Black"), ("W", "White"), ("BW", "Black - White")]
CSV = []


def rec(table_, group, outcome, term, e, **kw):
    b, se, p = tsp(e)
    CSV.append(dict(table=table_, group=group, outcome=outcome, term=term, coef=b, se=se, p=p, **kw))


def change(tag, y, g, x, bands=B6):
    """mean over bands >= 35 minus mean over bands < 35 of a coefficient (g may be 'BW')."""
    lo = [b for b in bands if b[0] < 35]
    hi = [b for b in bands if b[0] >= 35]
    terms = [(G(tag, y, a, b, g, x), 1 / len(hi)) for a, b in hi] + [(G(tag, y, a, b, g, x), -1 / len(lo))
                                                                     for a, b in lo]
    return lin(terms)


# ================================================================ A: education gradient of same-employer growth
def sec_A(s, n_s, md):
    specs = [("A_e", "g", ["educ"], "(1) growth on years of education"),
             ("A_el", "g", ["educ", "lyp"], "(2) growth on education + ln parental income")]
    nspecs = specs + [("A_a", "g", ["afqt"], "(3) growth on AFQT (1 s.d.)"),
                      ("A_ae", "g", ["afqt", "educ"], "(4) growth on AFQT + education")]
    for tag, y, xs, _ in specs:
        run("p" + tag, s, y, xs, bands=B2, need=["educ", "lyp"])
    for tag, y, xs, _ in nspecs:
        run("n" + tag, n_s, y, xs, bands=B2, need=["educ", "lyp", "afqt"])
    for data, pre, sp in (("PSID", "p", specs), ("NLSY79", "n", nspecs)):
        panels = []
        for g, gname in GR:
            rows = []
            for lo, hi in B2:
                for x, lab in (("educ", "years of education"), ("afqt", "AFQT (1 s.d.)"),
                               ("lyp", "ln parental income")):
                    es = [G(pre + t, y, lo, hi, g, x) if x in xs else None for t, y, xs, _ in sp]
                    if all(e is None for e in es):
                        continue
                    rows.append((f"{lab}, {lo}-{hi}", [cell(e) for e in es]))
                    for (t, y, xs, h), e in zip(sp, es):
                        if e is not None:
                            rec(f"A {data} same-employer growth", gname, h, f"{x}, {lo}-{hi}", e)
                if g != "BW":
                    k = R36.K(pre + sp[0][0], "g", lo, hi, g, sp[0][2][0])
                    if k in R36.RES:
                        rows.append((f"N pairs / men / clusters, {lo}-{hi}; mean growth",
                                     [f"{R36.RES[k]['n']:,} / {R36.RES[k]['men']:,} / {R36.RES[k]['G']:,}; "
                                      f"{R36.RES[k]['mean']:.4f}"] + [""] * (len(sp) - 1)))
            panels.append((gname, rows))
        md += [f"## A. Education gradient of same-employer wage growth by race ({data})", "",
               "Same-employer pairs (PSID: 32 Section 3 / 36; NLSY79: same roster employer). Outcome: annualised ln "
               "wage growth. One regression per column; controls: quartic in age, year (round) FE; common sample "
               "(education, ln parental income" + (", AFQT" if data == "NLSY79" else "") + " known).", ""]
        md += table([h for *_, h in sp], panels)


# ================================================================ B: education premium and wage IGE by age band
def sec_B(r, J, md):
    r = r.copy()
    r["ba"] = (r["educ"] >= 16).astype(float).where(r["educ"].notna())
    v = r[r["valid"] & r["lw"].notna() & r["age"].between(25, 55)].copy()
    v["yfe"], v["cl"] = v["year"], v["fam68"].astype(float)
    J = J.copy()
    J["ba"] = (J["educ"] >= 16).astype(float).where(J["educ"].notna())
    j = J[J["lw"].notna() & J["age"].between(25, 55)].copy()
    out = {}
    for data, d, pre, ys in (("PSID", v, "pB", ("lw", "ly")), ("NLSY79", j, "nB", ("lw",))):
        for y in ys:
            run(f"{pre}e_{y}", d, y, ["educ"], bands=B6, need=["lyp", "educ"])
            run(f"{pre}ba_{y}", d, y, ["ba"], bands=B6, need=["lyp", "educ"])
            run(f"{pre}l_{y}", d, y, ["lyp"], bands=B6, need=["lyp", "educ"])
            run(f"{pre}le_{y}", d, y, ["lyp", "educ"], bands=B6, need=["lyp", "educ"])
            # education on ln parental income (same rows): the delta of the Gelbach split
            run(f"{pre}aux_{y}", d.assign(educ_y=d["educ"].where(d[y].notna())), "educ_y", ["lyp"], bands=B6,
                need=["lyp", "educ", y])
            out[(data, y)] = pre
    for (data, y), pre in out.items():
        ylab = {"lw": "ln hourly wage", "ly": "ln annual earnings"}[y]
        cols = [(f"{pre}e_{y}", "educ", "(1) return to a year of education"),
                (f"{pre}ba_{y}", "ba", "(2) BA premium (education >= 16)"),
                (f"{pre}l_{y}", "lyp", "(3) ln parental income (IGE of the outcome)"),
                (f"{pre}le_{y}", "lyp", "(4) ln parental income, + education"),
                ("acc", "lyp", "(5) accounted for by education = (3) - (4)"),
                ("share", "lyp", "(6) share = (5) / (3)")]
        panels = []
        for g, gname in GR:
            rows = []
            for lo, hi in B6:
                es = []
                for tag, x, _ in cols:
                    if tag == "acc":
                        es.append(lin([(G(f"{pre}l_{y}", y, lo, hi, g), 1.0), (G(f"{pre}le_{y}", y, lo, hi, g), -1.0)]))
                    elif tag == "share":
                        es.append(R36.ratio(es[-1], G(f"{pre}l_{y}", y, lo, hi, g)))
                    else:
                        es.append(G(tag, y, lo, hi, g, x))
                rows.append((f"age {lo}-{hi}", [cell(e) for e in es]))
                for (_, _, h), e in zip(cols, es):
                    rec(f"B {data} premium and IGE by band, {ylab}", gname, h, f"{lo}-{hi}", e)
            ch = []
            for tag, x, _ in cols:
                if tag == "acc":
                    ch.append(lin([(change(f"{pre}l_{y}", y, g, "lyp"), 1.0), (change(f"{pre}le_{y}", y, g, "lyp"),
                                                                              -1.0)]))
                elif tag == "share":
                    ch.append(R36.ratio(ch[-1], change(f"{pre}l_{y}", y, g, "lyp")))
                else:
                    ch.append(change(tag, y, g, x))
            rows.append(("**change: mean >= 35 minus mean < 35**", [cell(e) for e in ch]))
            for (_, _, h), e in zip(cols, ch):
                rec(f"B {data} premium and IGE by band, {ylab}", gname, h, "change >= 35 minus < 35", e)
            if g != "BW":
                ns = []
                for lo, hi in B6:
                    k = R36.K(f"{pre}l_{y}", y, lo, hi, g)
                    ns.append(f"{R36.RES[k]['n']:,}" if k in R36.RES else "")
                rows.append(("N son-years by band", ["/".join(ns)] + [""] * (len(cols) - 1)))
            panels.append((gname, rows))
        md += [f"## B. {data}: education premium and the {ylab} IGE by age band", "",
               "Son-years with a valid outcome, education and ln parental income. (1) coefficient on years of "
               "education; (2) on an indicator for >= 16 years; (3) on ln parental income; (4) on ln parental income "
               "with years of education; (5) = (3) - (4) = (return to education in (4)) x (education gradient in "
               "parental income); (6) share. Controls: quartic in age, year FE. Change row: mean over bands >= 35 "
               "minus mean over bands < 35. Black - White panel: difference of the separate regressions.", ""]
        md += table([h for *_, h in cols], panels)


# ================================================================ C: within- vs between-job growth
def sec_C(r, md):
    dp = pd.read_pickle(DATA / "psid_displacement.pkl")
    dy = set(zip(dp.loc[dp["main"] == 1, "pid"], dp.loc[dp["main"] == 1, "year"]))
    d = r[r["g_lw_t"].notna() & r["wave"].ge(1985) & r["race"].isin(["Black", "White"])].copy()
    d["yfe"], d["cl"] = d["year"], d["fam68"].astype(float)
    gap = d["gap"].fillna(1).astype(int)
    disp = np.zeros(len(d), bool)
    for k in range(0, 3):                              # income years wave-1-k for k < gap + 1 (between the wage years)
        yrs = d["wave"] - 1 - k
        disp |= np.array([(p, y) in dy for p, y in zip(d["pid"], yrs)]) & (k <= gap).to_numpy()
    d["disp_iv"] = disp.astype(float)
    d["e_stay"] = ((d["stay"] == 1) & (d["disp_iv"] == 0)).astype(float)
    d["e_disp"] = d["disp_iv"]
    d["e_move"] = ((d["stay"] == 0) & (d["disp_iv"] == 0)).astype(float)
    g = d["g_lw_t"]
    for k in ("stay", "move", "disp"):
        d[f"gc_{k}"] = g.where(d[f"e_{k}"] == 1)                    # growth conditional on the event
        d[f"gx_{k}"] = g * d[f"e_{k}"]                              # contribution (adds up to g)
    d["g_all"] = g
    ys = [("g_all", "(1) annual ln wage growth, all pairs"),
          ("gx_stay", "(2) contribution: stayed"), ("gx_move", "(3) contribution: moved, not displaced"),
          ("gx_disp", "(4) contribution: displaced"),
          ("e_stay", "(5) P(stayed)"), ("e_move", "(6) P(moved, not displaced)"), ("e_disp", "(7) P(displaced)"),
          ("gc_stay", "(8) growth | stayed"), ("gc_move", "(9) growth | moved"), ("gc_disp", "(10) growth | displaced")]
    for y, _ in ys:
        run("C", d, y, ["lyp"], bands=B2)
    panels = []
    for gg, gname in GR:
        rows = []
        for lo, hi in B2:
            es = [G("C", y, lo, hi, gg) for y, _ in ys]
            rows.append((f"ln parental income, sons {lo}-{hi}", [cell(e) for e in es]))
            for (y, h), e in zip(ys, es):
                rec("C within vs between jobs", gname, h, f"{lo}-{hi}", e)
            if gg != "BW":
                rows.append((f"Mean of outcome, {lo}-{hi}", [f"{R36.RES[R36.K('C', y, lo, hi, gg)]['mean']:.4f}"
                                                              if R36.K("C", y, lo, hi, gg) in R36.RES else ""
                                                              for y, _ in ys]))
                rows.append((f"N pairs, {lo}-{hi}", [f"{R36.RES[R36.K('C', y, lo, hi, gg)]['n']:,}"
                                                     if R36.K("C", y, lo, hi, gg) in R36.RES else "" for y, _ in ys]))
        panels.append((gname, rows))
    md += ["## C. Within- vs between-job wage growth by parental income (PSID)", "",
           "Consecutive interviews 1-2 years apart with a valid wage, mapped occupation and tenure (27's transition "
           "rows, waves 1985-2023). Events between the two wage years: stayed (27 'stay' = tenure covers the interval, "
           "no displacement), moved without displacement, displaced (plant closure / layoff / firing in an income year "
           "between the two wage years). (1) = (2) + (3) + (4) exactly on the same pairs; (5)-(7) linear "
           "probabilities; (8)-(10) growth conditional on the event. Controls: quartic in age, year FE.", ""]
    md += table([h for _, h in ys], panels)
    return d


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
    if "educ" not in J:
        J = J.merge(kids[["pid", "educ"]], on="pid", how="left")
    md = ["# Schooling, on-the-job growth and job moves by parental income and race (Fable review, Item 2)", "",
          "Built by `42.SchoolingAndJobGrowth.py` (2026-10-17); definitions in its docstring. Every coefficient: "
          "estimate (s.e.; p), *** p<0.01, ** p<0.05, * p<0.1; s.e. clustered by 1968 family (PSID) / 1979 household "
          "(NLSY79). **Descriptive.**", ""]
    print("A ...", flush=True)
    sec_A(s, n_s, md)
    print("B ...", flush=True)
    sec_B(r, J, md)
    print("C ...", flush=True)
    sec_C(r, md)
    (OUT / "schooling_job_growth.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    pd.DataFrame(CSV).to_csv(OUT / "schooling_job_growth.csv", index=False)
    print("done", flush=True)


if __name__ == "__main__":
    main()
