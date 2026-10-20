r"""NLSY79 Children and Young Adults: child outcomes and the mother's work around each birth (2026-10-17).

Phase 2 of PLAN.md. Reads the public CYA release (Dropbox/NLS/nlscya_all_1979-2020, read only; only the columns
needed), the NLSY79 women extract of NLSY79/1.ExtractWomen.py + 4.ExtractFamily.py (NLSY79/data/women79.pkl,
family79.pkl; helpers of NLSY79/common.py imported read only) and the NLSY79 TNFI_TRUNC columns of the main release.

Writes
  data/cya_codebook.csv     CYA codebook index (column, question name, year, title)
  data/cya_children.pkl     one row per child of a White / Black NLSY79 mother (SAMPLE_ID 5, 6 White; 7, 13 Black;
                                the same women as NLSY79/data/women79.pkl and the female part of IGE/2.NLSY79.py's
                                sample definition White {1,2,5,6}, Black {3,7,10,13})
  output/cya_descriptives.md   variables, sample sizes, means by race of the mother, descriptive OLS
  output/cya_regressions.csv   the OLS coefficients behind the markdown table

Child (CYA, cross-round): CPUBID, MPUBID, CSEX, CMOB, CYRB, BTHORDR, MAGEBIR, CRACE.
Assessments (NLSY-created scores, every survey round 1986-2014; BPI to 2016):
  PIAT Math                    MATHZyyyy   (standard score, national norms: mean 100, sd 15), MATHPyyyy percentile
  PIAT Reading Recognition     RECOGZyyyy, RECOGPyyyy
  PIAT Reading Comprehension   COMPZyyyy,  COMPPyyyy
  PPVT-R                       PPVTZyyyy,  PPVTPyyyy
  Behavior Problems Index      BPIZyyyy (total standard score, all children; HIGHER = MORE problems), BPIPyyyy
  age at assessment (months)   CSAGEyyyy (child supplement: PIAT, PPVT), MSAGEyyyy (mother supplement: BPI)
  child sampling weight        CSAMWTyyyy_REV (1986-2000) else CSAMWTyyyy, 2 implied decimals
Age bands 5-6, 7-8, 9-10, 11-12, 13-14 = 60-83, ..., 156-179 months at assessment. In each band the assessment taken
in it (if two rounds fall in the band, the one closest to the band's middle); no borrowing from outside the band.
Young adults (YA interviews from 1994, ages 15+):
  age                          AGEINTyy / AGEINTyyyy (age at interview)
  highest grade completed      HGCyyyy (created, 2004-2020); before 2004 Q4-19 (not enrolled) or Q4-2 - 1 (enrolled,
                               Q4-1 = 1); hgc25 = max over interviews up to the one closest to age 25 within 24-26
  college                      ever: any interview with grade completed >= 13, or enrolled in college (Q4-2 13-20), or
                               a valid date first attended college (Q4-57~Y); defined if seen at 19+; coll_by21 the
                               same from interviews at <= 21 (defined if seen at 20-21)
  earnings                     wages and salary of the previous calendar year: Q15-5 (1994-98), Q15-5-TOP (2000-20);
                               2000 dollars; mean over interviews at ages 26-35 (income ages ~25-34, zeros kept) and the
                               latest interview at 26+
Mother (NLSY79 weekly array; week 1 = first week of 1978; b = week of the 15th of the birth month):
  wk_0_3, wk_0_12, wk_13_24    weeks employed in weeks [b, b+12], [b, b+51], [b+52, b+103] (scaled up for weeks
                               without information; NaN if more than a quarter of the window has none)
  emp_pre13                    employed in some week of [b-13, b-1]
  same_emp52                   (if employed in [b-13, b-1]) works for the employer of her last employed week before the
                               birth (job roster, employer index JJ) in some week of [b+5, b+52]: kept or returned to
                               the pre-birth employer within a year
  married_b                    married at b (marriage history, NLSY79/common.py marriages)
  afqt                         AFQT-3 (1981, 2006 revision percentile)
  m_hgc, m_edu                 highest grade completed (max over rounds, i.e. completed schooling) and LHS/HS/College
  faminc05, lfaminc05          mean TNFI_TRUNC (2000 dollars) over calendar years of child age 0-5 (income of year t
                               reported in round t+1; at least 2 years observed)
Descriptive, NOT causal: mothers' work after a birth is a choice correlated with unobserved family and child traits.
Usage: python 10.CYAOutcomes.py [--reuse]   (--reuse: read the raw extracts cached in data/ by a previous run)
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from common import DATA, OUT, to2000, nls_index, nls_pick as pick, nls_money, ols, stars
import os
NLSY79_DIR = Path(os.environ.get("NLSY79_DIR", r"G:\My Drive\Selection vs risk\NLSY79"))   # Selection-vs-risk/NLSY79 (helpers + extracts), read only
DROPBOX = Path(os.environ.get("DROPBOX", Path.home() / "Dropbox"))   # raw data, read only

NLS = Path(DROPBOX / "NLS")
CYA = NLS / "nlscya_all_1979-2020"
CYA_CDB, CYA_CSV = CYA / "nlscya_all_1979-2020.cdb", CYA / "nlscya_all_1979-2020.csv"
N79_CSV = NLS / "nlsy79_all_1979-2022" / "nlsy79_all_1979-2022.csv"
SAMPLES = {5: "White", 6: "White", 7: "Black", 13: "Black"}          # mothers: women of IGE/2.NLSY79.py's samples

# NLSY79/common.py (read only) - loaded under another name, IGE's own module is also called `common`
_spec = importlib.util.spec_from_file_location("nlsy79_common", NLSY79_DIR / "common.py")
n79 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(n79)

TESTS = {"math": "MATH", "recog": "RECOG", "comp": "COMP", "ppvt": "PPVT", "bpi": "BPI"}
LABEL = {"math": "PIAT Math", "recog": "PIAT Read. Recog.", "comp": "PIAT Read. Comp.", "ppvt": "PPVT",
         "bpi": "BPI total (+ = more problems)"}
BANDS = {"5_6": (60, 83), "7_8": (84, 107), "9_10": (108, 131), "11_12": (132, 155), "13_14": (156, 179)}


# ---------------------------------------------------------------- column selection
def by_year(ix, stem, letter="C"):
    """{year: col} for question name stem + 4-digit year (e.g. MATHZ1986)."""
    s = ix[ix["col"].str.startswith(letter) & ix["year"].str.fullmatch(r"\d{4}")]
    s = s[s["qname"] == stem + s["year"]]
    return {int(y): c for y, c in zip(s["year"], s["col"])}


def xrnd(ix, q):
    s = ix[(ix["qname"] == q) & (ix["year"] == "XRND")]
    assert len(s) == 1, q
    return s["col"].iloc[0]


def cya_columns(ix):
    v = {"child": {q: xrnd(ix, q) for q in ["CPUBID", "MPUBID", "CRACE", "CSEX", "CMOB", "CYRB", "BTHORDR", "MAGEBIR",
                                             "CYRDEATH", "HGC_DLI"]}}
    for k, T in TESTS.items():
        v[k + "_z"] = by_year(ix, T + "Z")
        v[k + "_p"] = by_year(ix, T + "P")
    v["csage"], v["msage"] = by_year(ix, "CSAGE"), by_year(ix, "MSAGE")
    w = by_year(ix, "CSAMWT")
    rev = ix[ix["qname"].str.fullmatch(r"CSAMWT\d{4}_REV", na=False)]
    w.update({int(q[6:10]): c for q, c in zip(rev["qname"], rev["col"])})
    v["cwt"] = w
    ya = ix[ix["col"].str.startswith("Y")]
    age = ya[ya["qname"].str.fullmatch(r"AGEINT(\d\d|\d{4})", na=False)]
    v["ya_age"] = {int(y): c for y, c in zip(age["year"], age["col"])}
    v["ya_wage"] = pick(ya, ["Q15-5-TOP", "Q15-5"])
    v["ya_hgc"] = by_year(ix, "HGC", "Y")
    v["ya_q419"] = pick(ya, ["Q4-19", "Q4-19AAA"])
    v["ya_q41"] = pick(ya, ["Q4-1"])
    v["ya_q42"] = pick(ya, ["Q4-2"])
    v["ya_coly"] = pick(ya, ["Q4-57~Y"])
    return v


# ---------------------------------------------------------------- raw reads
def read_raw(reuse):
    f_cya, f_inc = DATA / "cya_raw.pkl", DATA / "cya_mother_tnfi_raw.pkl"
    ix = nls_index(CYA_CDB)
    ix.to_csv(DATA / "cya_codebook.csv", index=False)
    v = cya_columns(ix)
    if reuse and f_cya.exists() and f_inc.exists():
        return ix, v, pd.read_pickle(f_cya), pd.read_pickle(f_inc)
    cols = list(dict.fromkeys(c for d in v.values() for c in d.values()))
    print(f"reading {len(cols)} CYA columns ...", flush=True)
    raw = pd.read_csv(CYA_CSV, usecols=cols)
    raw.to_pickle(f_cya)
    ix79 = pd.read_csv(DATA / "nlsy79_codebook.csv", dtype=str)       # written by 2.NLSY79.py
    tnfi = pick(ix79, ["TNFI_TRUNC"])
    print(f"reading {len(tnfi) + 1} NLSY79 columns ...", flush=True)
    inc = pd.read_csv(N79_CSV, usecols=["R0000100"] + list(tnfi.values()))
    inc = inc.rename(columns={"R0000100": "id", **{c: f"tnfi{y}" for y, c in tnfi.items()}})
    inc.to_pickle(f_inc)
    return ix, v, raw, inc


# ---------------------------------------------------------------- child assessments
def assessments(raw, v):
    """child x test x band: standard score, percentile, age (months), weight, survey year."""
    out = pd.DataFrame({"cid": raw[v["child"]["CPUBID"]].values})
    new = {}
    for k in TESTS:
        agevar = v["msage"] if k == "bpi" else v["csage"]
        rows = []
        for y, cz in v[k + "_z"].items():
            if y not in agevar:
                continue
            z = pd.to_numeric(raw[cz], errors="coerce")
            p = pd.to_numeric(raw[v[k + "_p"][y]], errors="coerce") if y in v[k + "_p"] else np.nan
            a = pd.to_numeric(raw[agevar[y]], errors="coerce")
            w = pd.to_numeric(raw[v["cwt"][y]], errors="coerce") / 100 if y in v["cwt"] else np.nan
            rows.append(pd.DataFrame({"cid": out["cid"].values, "year": y, "z": z.values, "p": np.asarray(p, float),
                                      "age": a.values, "w": np.asarray(w, float)}))
        L = pd.concat(rows, ignore_index=True)
        L = L[(L["z"] > 0) & (L["age"] >= 0)]
        L["p"] = L["p"].where(L["p"] >= 0)
        for b, (lo, hi) in BANDS.items():
            s = L[L["age"].between(lo, hi)].copy()
            s["dist"] = (s["age"] - (lo + hi) / 2).abs()
            s = s.sort_values(["cid", "dist", "year"]).groupby("cid").first()
            m = out["cid"].map
            new.update({f"{k}_{b}": m(s["z"]), f"{k}p_{b}": m(s["p"]), f"{k}age_{b}": m(s["age"]),
                        f"{k}wt_{b}": m(s["w"]), f"{k}yr_{b}": m(s["year"])})
    return pd.concat([out, pd.DataFrame(new)], axis=1)


# ---------------------------------------------------------------- young adults
def young_adult(raw, v):
    cid = raw[v["child"]["CPUBID"]].values
    num = lambda c: pd.to_numeric(raw[c], errors="coerce").values.astype(float)   # noqa: E731
    rows = []
    for y in sorted(v["ya_age"]):
        age = num(v["ya_age"][y]); age[age <= 0] = np.nan
        hgc = num(v["ya_hgc"][y]) if y in v["ya_hgc"] else np.full(len(raw), np.nan)
        q419 = num(v["ya_q419"][y]) if y in v["ya_q419"] else np.full(len(raw), np.nan)
        q41 = num(v["ya_q41"][y]) if y in v["ya_q41"] else np.full(len(raw), np.nan)
        q42 = num(v["ya_q42"][y]) if y in v["ya_q42"] else np.full(len(raw), np.nan)
        ok = lambda x: np.where((x >= 0) & (x <= 20), x, np.nan)                 # noqa: E731 (95 ungraded out)
        enr = (q41 == 1) & np.isfinite(ok(q42))
        g = np.where(np.isfinite(ok(hgc)), ok(hgc), np.where(np.isfinite(ok(q419)), ok(q419),
                                                              np.where(enr, ok(q42) - 1, np.nan)))
        col = (np.nan_to_num(ok(hgc)) >= 13) | (np.nan_to_num(ok(q419)) >= 13) | (enr & (np.nan_to_num(ok(q42)) >= 13))
        if y in v["ya_coly"]:
            col |= num(v["ya_coly"][y]) > 1900
        wage = nls_money(raw[v["ya_wage"][y]]).values if y in v["ya_wage"] else np.full(len(raw), np.nan)
        rows.append(pd.DataFrame({"cid": cid, "round": y, "age": age, "hgc": g, "col": col.astype(float),
                                  "earn": to2000(wage, y - 1)}))
    L = pd.concat(rows, ignore_index=True)
    L = L[L["age"].notna()].sort_values(["cid", "round"])
    L["hgc_run"] = L.groupby("cid")["hgc"].cummax()
    out = pd.DataFrame(index=pd.Index(np.unique(cid), name="cid"))
    out["ya_age_last"] = L.groupby("cid")["age"].max()
    out["ya_n"] = L.groupby("cid").size()
    s = L[L["age"].between(24, 26)].assign(d=lambda x: (x["age"] - 25).abs()).sort_values(["cid", "d", "round"])
    s = s.dropna(subset=["hgc_run"]).groupby("cid").first()
    out["hgc25"] = s["hgc_run"]
    out["hgc_last"] = L.dropna(subset=["hgc_run"]).groupby("cid")["hgc_run"].last()
    out["college_any"] = L.groupby("cid")["col"].max().reindex(out.index).where(out["ya_age_last"] >= 19)
    seen21 = (L[L["age"].between(20, 21)].groupby("cid").size() > 0).reindex(out.index, fill_value=False)
    out["coll_by21"] = L[L["age"] <= 21].groupby("cid")["col"].max().reindex(out.index).where(seen21)
    e = L[(L["age"] >= 26) & L["earn"].notna()]
    m = e[e["age"] <= 35].groupby("cid")["earn"].agg(["mean", "count"])
    out["earn2635"], out["n_earn2635"] = m["mean"], m["count"]
    out["learn2635"] = np.log(out["earn2635"].where(out["earn2635"] > 0))
    last = e.groupby("cid").last()
    out["earn_last"], out["age_earn_last"] = last["earn"], last["age"]
    out["learn_last"] = np.log(out["earn_last"].where(out["earn_last"] > 0))
    return out.reset_index()


# ---------------------------------------------------------------- mothers
def window(E, i, a, b):
    """weeks employed in [a, b] (scaled for weeks without information); NaN if > 1/4 of the window lacks it."""
    if a < 1 or b >= E.shape[1]:
        return np.nan
    x = E[i, a:b + 1]
    n = np.isfinite(x).sum()
    return np.nan if n < 0.75 * len(x) else float(np.nansum(x)) / n * len(x)


def mother_exposures(kids, inc):
    d = n79.load()
    W = n79.weekly(d)
    assert W.shape[1] == 2385, W.shape                                   # wk0000 ... wk2384: column = week number
    E = n79.employed_matrix(W)
    mar = n79.marriages(d)
    print("employer spells ...", flush=True)
    spells = n79.employer_spells(d, n79.roster_index(d))
    row = pd.Series(np.arange(len(d)), index=d["id"].values)
    res = []
    for _, k in kids.iterrows():
        i = row.get(k["mid"])
        r = dict(cid=k["cid"])
        b = n79.week_of(k["cyrb"], k["cmob"]) if i is not None else np.nan
        if i is None or not (b == b):
            res.append(r)
            continue
        b = int(b)
        r["bweek"] = b
        r["wk_0_3"], r["wk_0_12"], r["wk_13_24"] = window(E, i, b, b + 12), window(E, i, b, b + 51), \
            window(E, i, b + 52, b + 103)
        r["married_b"] = float(n79.married_at(mar[i], b))
        if b - 13 >= 1 and b + 52 < E.shape[1]:
            pre = E[i, b - 13:b]
            r["emp_pre13"] = np.nan if not np.isfinite(pre).any() else float(np.nanmax(pre) == 1)
            if r["emp_pre13"] == 1:
                wlast = b - 13 + int(np.where(pre == 1)[0].max())
                jj = n79.employer_at(spells[i], wlast)
                if jj is not None:
                    r["same_emp52"] = float(n79.works_for(spells[i], jj, b + 5, b + 52))
        res.append(r)
    x = pd.DataFrame(res)
    m = d.set_index("id")
    mo = pd.DataFrame({"afqt": pd.to_numeric(m["AFQT-3_1981"], errors="coerce") / 1000, "m_hgc": m["hgc"],
                       "m_edu": m["edu"], "m_race": m["race"], "m_wt79": m["SAMPWEIGHT_1979"] / 100})
    mo["afqt"] = mo["afqt"].where(mo["afqt"] >= 0)
    # family income at child ages 0-5 (calendar years cyrb .. cyrb+5; income of year t is reported in round t+1)
    I = inc.set_index("id").apply(nls_money)
    yrs = {int(c[4:]) - 1: c for c in I.columns}
    fam = []
    for _, k in kids[["cid", "mid", "cyrb"]].iterrows():
        vals = []
        if k["mid"] in I.index and k["cyrb"] == k["cyrb"]:
            for t in range(int(k["cyrb"]), int(k["cyrb"]) + 6):
                if t in yrs:
                    z = I.at[k["mid"], yrs[t]]
                    if z == z:
                        vals.append(to2000(z, t))
        fam.append(dict(cid=k["cid"], faminc05=np.mean(vals) if len(vals) >= 2 else np.nan, n_faminc05=len(vals)))
    fam = pd.DataFrame(fam)
    fam["lfaminc05"] = np.log(fam["faminc05"].where(fam["faminc05"] > 0))
    return x, mo, fam


# ---------------------------------------------------------------- output helpers
def pv(p):
    return "<0.001" if p < 0.001 else f"{p:.3f}"


def mean_table(K, cols):
    lines = ["| variable | White mean | (sd) | N | Black mean | (sd) | N |", "|---|---|---|---|---|---|---|"]
    for c, lab in cols:
        cells = []
        for r in ("White", "Black"):
            s = K.loc[K["race"] == r, c].dropna().astype(float)
            cells += [f"{s.mean():.3f}" if len(s) else "", f"({s.std():.3f})" if len(s) > 1 else "", f"{len(s):,}"]
        lines.append(f"| {lab} | " + " | ".join(cells) + " |")
    return lines


def regressions(K):
    K = K.copy()
    K["work13"] = K["wk_0_12"] / 13
    K["afqt10"] = K["afqt"] / 10
    K["m_hs"] = (K["m_edu"] == "HS").astype(float).where(K["m_edu"].notna())
    K["m_col"] = (K["m_edu"] == "College").astype(float).where(K["m_edu"].notna())
    K["female"] = (K["csex"] == 2).astype(float)
    ctrl = ["afqt10", "m_hs", "m_col", "magebir", "married_b", "lfaminc05", "female"]
    rows_lab = {"work13": "Mother's weeks employed, months 0-12 (per 13 weeks)", "afqt10": "Mother's AFQT (per 10 pctile)",
                "m_hs": "Mother HS (vs < HS)", "m_col": "Mother College (vs < HS)", "magebir": "Mother's age at birth",
                "married_b": "Married at birth", "lfaminc05": "Log family income, ages 0-5", "female": "Child female",
                "const": "Constant"}
    outs = [(f"{k}_{b}", f"{LABEL[k]} {b.replace('_', '-')}") for b in ("5_6", "7_8") for k in TESTS]
    res, md = [], []
    for race in ("White", "Black"):
        S = K[K["race"] == race]
        fits = []
        for y, lab in outs:
            _, _, _, n, r = ols(S, y, "work13", controls=ctrl, fe=["cyrb"], cluster="mid")
            used = S[[y, "work13", *ctrl, "cyrb", "mid"]].replace([np.inf, -np.inf], np.nan).dropna()
            fits.append((y, lab, r, n, used["mid"].nunique(), used[y].mean()))
            for x in ["work13", *ctrl]:
                res.append(dict(race=race, outcome=y, regressor=x, coef=r.params[x], se=r.bse[x], p=r.pvalues[x],
                                n=n, mothers=used["mid"].nunique()))
        md += [f"**{race} mothers**", "", "| | " + " | ".join(f[1] for f in fits) + " |",
               "|---|" + "---|" * len(fits)]
        for x in ["work13", *ctrl]:
            md.append(f"| {rows_lab[x]} | " + " | ".join(f"{f[2].params[x]:.3f}{stars(f[2].pvalues[x])}" for f in fits)
                      + " |")
            md.append("| | " + " | ".join(f"({f[2].bse[x]:.3f}) p={pv(f[2].pvalues[x])}" for f in fits) + " |")
        md.append("| Birth-year FE | " + " | ".join("yes" for _ in fits) + " |")
        md.append("| Mean of outcome | " + " | ".join(f"{f[5]:.1f}" for f in fits) + " |")
        md.append("| N children | " + " | ".join(f"{f[3]:,}" for f in fits) + " |")
        md.append("| N mothers (clusters) | " + " | ".join(f"{f[4]:,}" for f in fits) + " |")
        md.append("")
    return pd.DataFrame(res), md


# ---------------------------------------------------------------- main
def main():
    DATA.mkdir(exist_ok=True); OUT.mkdir(exist_ok=True)
    ix, v, raw, inc = read_raw("--reuse" in sys.argv)
    c = v["child"]
    K = pd.DataFrame({"cid": raw[c["CPUBID"]], "mid": raw[c["MPUBID"]], "crace": raw[c["CRACE"]],
                      "csex": raw[c["CSEX"]], "cmob": raw[c["CMOB"]], "cyrb": raw[c["CYRB"]],
                      "border": raw[c["BTHORDR"]], "magebir": raw[c["MAGEBIR"]], "cyrdeath": raw[c["CYRDEATH"]]})
    for col in ("cmob", "cyrb", "magebir", "csex"):
        K[col] = pd.to_numeric(K[col], errors="coerce").where(lambda s: s > 0)
    n_all = len(K)
    # mother's race / sample from the NLSY79 women extract (SAMPLE_ID 5, 6, 7, 13)
    women = pd.read_pickle(Path(n79.DATA) / "women79.pkl")[["id", "sample_id"]]
    K = K.merge(women.rename(columns={"id": "mid"}), on="mid", how="inner")
    K["race"] = K["sample_id"].map(SAMPLES)
    # weight: first positive child sampling weight
    W = pd.DataFrame({y: pd.to_numeric(raw[col], errors="coerce") / 100 for y, col in sorted(v["cwt"].items())})
    W.index = raw[c["CPUBID"]].values
    K["cwt_first"] = K["cid"].map(W.where(W > 0).bfill(axis=1).iloc[:, 0])
    A = assessments(raw, v)
    Y = young_adult(raw, v)
    print("mother exposures ...", flush=True)
    X, MO, FAM = mother_exposures(K, inc)
    K = K.merge(X, on="cid", how="left").merge(MO, left_on="mid", right_index=True, how="left") \
         .merge(FAM, on="cid", how="left").merge(A, on="cid", how="left").merge(Y, on="cid", how="left")
    assert (K["m_race"] == K["race"]).all()
    K = K.drop(columns="m_race")
    K.to_pickle(DATA / "cya_children.pkl")

    # ------------------------------------------------ markdown
    md = ["# NLSY79 Children: mothers' work after a birth and child outcomes (descriptive)", "",
          "Script `IGE/10.CYAOutcomes.py` (2026-10-17). Data: NLSY79 Children and Young Adults 1979-2020 (public "
          "release), NLSY79 women extract (`NLSY79/data/women79.pkl`, `family79.pkl`), NLSY79 TNFI_TRUNC.", "",
          "**These are correlations, not effects.** A mother's work in the year after a birth is chosen jointly with "
          "unobserved traits of the family and the child (selection); the regressions below only show the raw and "
          "covariate-adjusted association.", "", "## Variables", "",
          "| measure | CYA / NLSY79 variables | definition |", "|---|---|---|",
          "| child id, mother id | CPUBID, MPUBID | mother linked to NLSY79 R0000100 |",
          "| race of mother | NLSY79 SAMPLE_ID (R0173600) | White 5, 6 (cross-section incl. poor White); Black 7, 13 "
          "(cross-section + supplemental) - the women of IGE/2.NLSY79.py's samples |",
          "| sex, birth month / year, birth order, mother's age at birth | CSEX, CMOB, CYRB, BTHORDR, MAGEBIR | |",
          "| child weight | CSAMWTyyyy_REV (1986-2000) / CSAMWTyyyy | per band: weight of the assessment round; "
          "`cwt_first`: first positive weight (regressions unweighted) |",
          "| PIAT Math | MATHZyyyy (MATHPyyyy) | NLSY-created total standard score, national norms (mean 100, sd 15); "
          "percentile in parentheses |",
          "| PIAT Reading Recognition | RECOGZyyyy (RECOGPyyyy) | same |",
          "| PIAT Reading Comprehension | COMPZyyyy (COMPPyyyy) | same |",
          "| PPVT-R | PPVTZyyyy (PPVTPyyyy) | same |",
          "| Behavior Problems Index | BPIZyyyy (BPIPyyyy) | total standard score, all-children norms; higher = more "
          "behaviour problems |",
          "| age at assessment | CSAGEyyyy (PIAT, PPVT), MSAGEyyyy (BPI) | months; bands 5-6 = 60-83 m, 7-8 = 84-107, "
          "9-10 = 108-131, 11-12 = 132-155, 13-14 = 156-179; the assessment inside the band (closest to its middle if "
          "two) |",
          "| highest grade completed by 25 | HGCyyyy (2004-20); Q4-19, Q4-1/Q4-2 (1994-2002); AGEINTyy(yy) | running "
          "max up to the YA interview closest to 25 within ages 24-26 |",
          "| college | HGCyyyy >= 13, Q4-2 in 13-20, Q4-57~Y | ever attended by the last interview (seen at 19+); "
          "`coll_by21` from interviews at <= 21 (seen at 20-21) |",
          "| earnings | Q15-5 (1994-98), Q15-5-TOP (2000-20) | wages and salary of the previous year, 2000 $; mean over "
          "interviews at 26-35 (zeros kept), and the latest interview at 26+ |",
          "| mother's weeks employed | NLSY79 weekly array STATUS_WK_NUM | weeks [b, b+12], [b, b+51], [b+52, b+103] "
          "after the birth week b (scaled for weeks without information, NaN if > 1/4 missing) |",
          "| employed before the birth | weekly array | employed in some week of [b-13, b-1] |",
          "| same employer within a year | job roster (employer index JJ) | if employed before: works for the employer "
          "of her last employed week before b in some week of [b+5, b+52] (kept or returned) |",
          "| married at the birth | YRBGkM/MOBGkM, YRENkM/MOENkM | marriage history |",
          "| mother's AFQT | AFQT-3 (1981) | percentile, 2006 revision |",
          "| mother's education | highest grade completed, max over rounds | LHS / HS / College (completed schooling, "
          "may postdate the birth) |",
          "| family income 0-5 | TNFI_TRUNC | mean over calendar years of child age 0-5 (round t+1 reports year t), "
          "2000 $, >= 2 years |", ""]
    md += ["## Sample", "",
           f"CYA children (all NLSY79 mothers): {n_all:,}. Children of White / Black mothers of the cross-sectional "
           f"and Black supplemental samples: {len(K):,} (Hispanic, supplemental poor-White and military-sample mothers "
           f"dropped).", ""]
    md += ["| | White | Black |", "|---|---|---|"]
    cnt = lambda f: [f"{int(f(K[K.race == r])):,}" for r in ("White", "Black")]   # noqa: E731
    md.append("| children | " + " | ".join(cnt(len)) + " |")
    md.append("| mothers | " + " | ".join(cnt(lambda s: s["mid"].nunique())) + " |")
    md.append("| born 1978 Apr or later (weekly array covers the 13 weeks before) | "
              + " | ".join(cnt(lambda s: (s["bweek"] >= 14).sum())) + " |")
    md.append("| with weeks employed months 0-12 | " + " | ".join(cnt(lambda s: s["wk_0_12"].notna().sum())) + " |")
    md.append("| with any test score at 5-6 | " + " | ".join(
        cnt(lambda s: s[[f"{k}_5_6" for k in TESTS]].notna().any(axis=1).sum())) + " |")
    md.append("| with hgc by 25 | " + " | ".join(cnt(lambda s: s["hgc25"].notna().sum())) + " |")
    md.append("| with earnings at 26-35 | " + " | ".join(cnt(lambda s: s["earn2635"].notna().sum())) + " |")
    md.append(f"| cross-check: CRACE Black (2) | " + " | ".join(cnt(lambda s: (s["crace"] == 2).sum())) + " |")
    md.append("")
    md += ["## Means by race of the mother", "", "### Mother and exposures", ""]
    md += mean_table(K, [("wk_0_3", "weeks employed, months 0-3 (of 13)"), ("wk_0_12", "weeks employed, months 0-12 (of 52)"),
                         ("wk_13_24", "weeks employed, months 13-24 (of 52)"), ("emp_pre13", "employed in 13 weeks before"),
                         ("same_emp52", "same employer within 52 weeks (if employed before)"),
                         ("married_b", "married at birth"), ("afqt", "mother's AFQT percentile"),
                         ("m_hgc", "mother's highest grade"), ("magebir", "mother's age at birth"),
                         ("faminc05", "family income ages 0-5 (2000 $)"), ("border", "birth order"),
                         ("cyrb", "child birth year")])
    md += ["", "### Child assessments (standard scores; BPI: higher = more problems)", ""]
    md += mean_table(K, [(f"{k}_{b}", f"{LABEL[k]} {b.replace('_', '-')}") for k in TESTS for b in BANDS])
    md += ["", "### Young adults", ""]
    md += mean_table(K, [("hgc25", "highest grade completed by 25"), ("college_any", "ever attended college"),
                         ("coll_by21", "attended college by 21"), ("earn2635", "wages, mean at 26-35 (2000 $)"),
                         ("earn_last", "wages, latest interview 26+ (2000 $)"), ("age_earn_last", "age at latest earnings")])
    md += ["", "### Sanity check: all children of these mothers, standard scores (norm mean 100, sd 15)", "",
           "| test | band | mean | sd | N |", "|---|---|---|---|---|"]
    for k in TESTS:
        for b in BANDS:
            s = K[f"{k}_{b}"].dropna()
            md.append(f"| {LABEL[k]} | {b.replace('_', '-')} | {s.mean():.1f} | {s.std():.1f} | {len(s):,} |")
    md += ["", "Notes. PIAT and BPI standard scores sit near the norms (means 97-111, sd 11-16). PIAT Reading "
           "Comprehension at 5-6 is selected: it is given only to children whose Reading Recognition raw score is "
           "high enough, hence the small N and high mean. PPVT-R standard scores are well below the norm (about 92 "
           "overall, 81-84 for children of Black mothers, sd 18-20), as is known for the NLSY79 children; PPVT is "
           "mostly given at 3-5 and 10-11 in later rounds, hence the thin 7-8 and 13-14 cells. Children born before "
           "April 1978 have no exposure measures (the weekly array starts in January 1978). `college_any` counts "
           "attendance without a completed year (enrolled in year 1 of college, or a date first attended), so it "
           "exceeds the share with 13+ completed grades.", ""]
    T, regmd = regressions(K)
    T.to_csv(OUT / "cya_regressions.csv", index=False)
    md += ["", "## Descriptive OLS: test scores on the mother's weeks employed in the first year", "",
           "Each column one OLS regression (outcome in the header: standard score at that age band), by race of the "
           "mother; unweighted; s.e. clustered by mother; *** p<0.01, ** p<0.05, * p<0.1. Regressor of interest: "
           "weeks employed in weeks 0-51 after the birth divided by 13 (one unit = one quarter of the year at work). "
           "Controls: AFQT, education, age at birth, married at birth, log family income at 0-5, child sex, "
           "birth-year fixed effects. BPI: a positive coefficient means more behaviour problems. "
           "**Descriptive (selection), not causal.**", ""]
    md += regmd
    (OUT / "cya_descriptives.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md[-60:]))


if __name__ == "__main__":
    main()
