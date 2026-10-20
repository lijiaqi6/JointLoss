r"""Phase 1 first stage: does local labor-market slack at a birth change whether employed mothers keep working?
(2026-10-17)

Prediction of the search-friction model: when re-employment is slow, a mother who works before a birth is less
likely to leave at the birth. Slack for women at the birth (high unemployment, low predicted job growth in women's
industries) should therefore RAISE the share of employed mothers still working after the birth; slack for men
(men's industries) hits the husband (spousal risk). Sign convention: the Bartik shocks are predicted employment
growth (tight market = high), so the friction predicts a NEGATIVE coefficient on bartik_f and a POSITIVE one on the
unemployment rate.

Data (raw files read only):
  births    PSID Childbirth and Adoption History 1985-2023 (Dropbox/PSID/Others/cah85_23): birth records of women
            (CAH2 = 1, CAH5 = 2) with a child, born 1977-2021, mother in the SRC or SEO sample; twins counted once;
            birth order CAH9, mother's marital status at the birth CAH8, mother's birth year CAH7.
  work      head / wife total annual hours in the family files: wave w reports calendar year w-1 (1976-97 annual,
            then biennial); from 2003 the family files also ask 'WTR EMPLOYED IN w-2' with weeks and hours/week,
            which fills the odd calendar years 2001-2021. Calendar years 1997 and 1999 are not observed. Employed =
            hours > 0 (also >= 500 hours). Only women who are head or wife / partner in the reporting wave have hours.
  state     family-file state of residence (PSID alphabetical codes -> FIPS) in the wave of the birth year, else
            the next, else the previous wave.
  race      race of the head of the woman's family unit (psid_person_year.pkl `hrace`) in the year before the birth
            (nearest wave); White and Black only.
  education highest 'COMPLETED EDUCATION' (years, 1-17) reported in any wave of the individual file.
  shocks    IGE/data/state_shocks.pkl from 8a.StateShocks.py (LAUS unemployment rate; CPS-MORG Bartik shocks).

Writes output/first_stage.csv (every coefficient) and output/first_stage.md (tables + sample checks), and the
analysis file data/first_stage_births.pkl.
"""
import re
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

from common import DATA, OUT, stars
import os
DROPBOX = Path(os.environ.get("DROPBOX", Path.home() / "Dropbox"))   # raw data, read only (Mac: export DROPBOX)

PSID = Path(DROPBOX / "PSID")
FAM = PSID / "Family"
IND = PSID / "Individual" / "ind2023er" / "IND2023ER"
CAH = PSID / "Others" / "cah85_23" / "CAH85_23"

WAVES = list(range(1976, 1998)) + list(range(1999, 2024, 2))
HOURS = {1976: ("V4332", "V4344"), 1977: ("V5232", "V5244"), 1978: ("V5731", "V5743"), 1979: ("V6336", "V6348"),
         1980: ("V6934", "V6946"), 1981: ("V7530", "V7540"), 1982: ("V8228", "V8238"), 1983: ("V8830", "V8840"),
         1984: ("V10037", "V10131"), 1985: ("V11146", "V11258"), 1986: ("V12545", "V12657"),
         1987: ("V13745", "V13809"), 1988: ("V14835", "V14865"), 1989: ("V16335", "V16365"),
         1990: ("V17744", "V17774"), 1991: ("V19044", "V19074"), 1992: ("V20344", "V20374"),
         1993: ("V21634", "V21670"), 1994: ("ER4096", "ER4107"), 1995: ("ER6936", "ER6947"),
         1996: ("ER9187", "ER9198"), 1997: ("ER12174", "ER12185"), 1999: ("ER16471", "ER16482"),
         2001: ("ER20399", "ER20410"), 2003: ("ER24080", "ER24091"), 2005: ("ER27886", "ER27897"),
         2007: ("ER40876", "ER40887"), 2009: ("ER46767", "ER46788"), 2011: ("ER52175", "ER52196"),
         2013: ("ER57976", "ER57997"), 2015: ("ER65156", "ER65177"), 2017: ("ER71233", "ER71254"),
         2019: ("ER77255", "ER77276"), 2021: ("ER81582", "ER81603"), 2023: ("ER85436", "ER85457")}
STATE = {1976: "V4303", 1977: "V5203", 1978: "V5703", 1979: "V6303", 1980: "V6903", 1981: "V7503", 1982: "V8203",
         1983: "V8803", 1984: "V10003", 1985: "V11103", 1986: "V12503", 1987: "V13703", 1988: "V14803",
         1989: "V16303", 1990: "V17703", 1991: "V19003", 1992: "V20303", 1993: "V21603", 1994: "ER4156",
         1995: "ER6996", 1996: "ER9247", 1997: "ER12221", 1999: "ER13004", 2001: "ER17004", 2003: "ER21003",
         2005: "ER25003", 2007: "ER36003", 2009: "ER42003", 2011: "ER47303", 2013: "ER53003", 2015: "ER60003",
         2017: "ER66003", 2019: "ER72003", 2021: "ER78003", 2023: "ER82003"}
FIPS_CHECK = (1999, "ER13005")                                 # FIPS 'CURRENT STATE' next to the PSID code
# PSID state code 1..51 (48 contiguous states + DC alphabetically, then AK, HI) -> FIPS
PSID2FIPS = dict(enumerate([1, 4, 5, 6, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                            30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48, 49, 50, 51, 53,
                            54, 55, 56, 2, 15], start=1))
ODD = re.compile(r"^(WTR EMPLOYED IN|WEEKS EMPLOYED IN|BC14EE HOURS/WK WORKED IN|DE14EE HOURS/WK WORKED IN) "
                 r"(\d{4}) \((HD|RP|WF|SP)\)")

INFIX = re.compile(r"(?:long\s+)?([A-Z]+\d+[A-Z0-9]*)\s+(\d+)\s*-\s*(\d+)")
LABEL = re.compile(r'label variable\s+(\S+)\s+"(.*)"')


def layout(do):
    t = do.read_text(encoding="latin-1")
    block = re.search(r"\binfix\b(.*?)\busing\b", t, re.S).group(1)
    pos = {v: (int(a) - 1, int(b)) for v, a, b in INFIX.findall(block)}
    return pos, [(v, l.strip()) for v, l in LABEL.findall(t)]


def read(base, cols, pos):
    return pd.read_fwf(base.with_suffix(".txt"), colspecs=[pos[c] for c in cols], names=cols, header=None,
                       encoding="latin-1")


# ---------------------------------------------------------------- raw extracts
def family():
    out, check = [], None
    for w in WAVES:
        folder = FAM / (f"fam{w}" if w < 1994 else f"fam{w}er")
        base = next(f for f in folder.glob("*.do") if "formats" not in f.name).with_suffix("")
        pos, labs = layout(base.with_suffix(".do"))
        idv = labs[1][0]
        odd = {}
        for v, l in labs:
            m = ODD.match(l)
            if m and int(m.group(2)) == w - 2:
                who = "h" if m.group(3) in ("HD", "RP") else "w"
                kind = {"WTR EMPLOYED IN": "emp", "WEEKS EMPLOYED IN": "wks"}.get(m.group(1), "hpw")
                odd[f"{who}_{kind}"] = v
        cols = [idv, *HOURS[w], STATE[w]] + list(odd.values()) + ([FIPS_CHECK[1]] if w == FIPS_CHECK[0] else [])
        f = read(base, cols, pos)
        f = f.rename(columns={idv: "int", HOURS[w][0]: "hh", HOURS[w][1]: "wh", STATE[w]: "pstate",
                              **{v: k for k, v in odd.items()}})
        if w == FIPS_CHECK[0]:
            check = (f["pstate"].map(PSID2FIPS) == f[FIPS_CHECK[1]]).mean()
        f["wave"] = w
        keep = ["wave", "int", "hh", "wh", "pstate"] + list(odd)
        out.append(f[keep])
        print(f"  family {w}: {len(f)} families; odd-year items: {sorted(odd)}", flush=True)
    F = pd.concat(out, ignore_index=True)
    for c in ("hh", "wh"):
        F[c] = F[c].where(F[c].between(0, 6000))                # 9999 in 1994-95 = NA
    F["fips"] = F["pstate"].map(PSID2FIPS)
    print(f"  PSID->FIPS state map agrees with the FIPS variable in {FIPS_CHECK[0]}: {check:.4f}", flush=True)
    return F, check


def odd_hours(emp, wks, hpw):
    e = np.where(emp == 1, 1.0, np.where(emp == 5, 0.0, np.nan))
    h = np.where((wks <= 52) & (hpw <= 112), wks * hpw, np.nan)
    h = np.where(e == 0, 0.0, h)
    return e, h


def employment_panel(py, F):
    """one row per woman x calendar year: employed (hours > 0) and employed 500+ hours."""
    w = py[(py["female"] == 1) & (py["head"] | py["wife"])][["pid", "wave", "int", "head", "wife"]]
    w = w.merge(F, on=["wave", "int"], how="left")
    a = pd.DataFrame({"pid": w["pid"], "year": w["wave"] - 1, "hours": np.where(w["head"], w["hh"], w["wh"])})
    a["emp"] = (a["hours"] > 0).astype(float).where(a["hours"].notna())
    a["emp500"] = (a["hours"] >= 500).astype(float).where(a["hours"].notna())
    a["src"] = "annual hours"
    o = w[w["wave"] >= 2003]
    eh, hh = odd_hours(o["h_emp"], o["h_wks"], o["h_hpw"])
    ew, hw = odd_hours(o["w_emp"], o["w_wks"], o["w_hpw"])
    b = pd.DataFrame({"pid": o["pid"].values, "year": o["wave"].values - 2,
                      "emp": np.where(o["head"], eh, ew), "hours": np.where(o["head"], hh, hw)})
    b["emp500"] = (b["hours"] >= 500).astype(float).where(b["hours"].notna())
    b["src"] = "WTR EMPLOYED IN w-2"
    E = pd.concat([a, b], ignore_index=True).dropna(subset=["emp"])
    return E.sort_values(["pid", "year", "src"]).drop_duplicates(["pid", "year"])


def education():
    pos, labs = layout(IND.with_suffix(".do"))
    vs = []
    for v, l in labs:
        m = re.match(r"^(COMPLETED EDUC|YRS COMPLETED EDUCATION|YEARS COMPLETED EDUCATION)\D*(\d\d)$", l)
        if m:
            yy = int(m.group(2))
            if (1900 + yy if yy >= 68 else 2000 + yy) >= 1975:
                vs.append(v)
    d = read(IND, ["ER30001", "ER30002"] + vs, pos)
    x = d[vs].where((d[vs] >= 1) & (d[vs] <= 17))
    return pd.DataFrame({"pid": d.ER30001 * 1000 + d.ER30002, "educ": x.max(axis=1)}), len(vs)


def cah():
    pos, labs = layout(CAH.with_suffix(".do"))
    cols = ["CAH2", "CAH3", "CAH4", "CAH5", "CAH7", "CAH8", "CAH9", "CAH10", "CAH13", "CAH15"]
    d = read(CAH, cols, pos)
    d = d[(d.CAH5 == 2) & ((d.CAH3 <= 2930) | d.CAH3.between(5001, 6872))]
    d["pid"] = d.CAH3 * 1000 + d.CAH4
    return d


# ---------------------------------------------------------------- helpers
def nearest(keys, panel, col, offsets):
    """value of `col` for (pid, year + offset), first offset found; panel has pid, wave."""
    out = pd.Series(np.nan, index=keys.index, dtype=object)
    p = panel[["pid", "wave", col]].dropna().drop_duplicates(["pid", "wave"]).set_index(["pid", "wave"])[col]
    for o in offsets:
        idx = pd.MultiIndex.from_arrays([keys["pid"], keys["year"] + o])
        v = pd.Series(p.reindex(idx).values, index=keys.index)
        out = out.where(out.notna(), v)
    return out


def emp_at(keys, E, col, offset):
    s = E.set_index(["pid", "year"])[col]
    idx = pd.MultiIndex.from_arrays([keys["pid"], keys["year"] + offset])
    return pd.Series(s.reindex(idx).values, index=keys.index)


def add_shocks(d, S, yearcol="year", suffix="", offset=0):
    cols = ["ur", "bartik_f", "bartik_m", "bartik_f_nat", "bartik_m_nat", "bartik_f_lag", "bartik_m_lag"]
    s = S[["fips", "year"] + cols].rename(columns={"year": "_y", **{c: c + suffix for c in cols}})
    s["fips"] = s["fips"].astype(float)
    d = d.assign(_y=d[yearcol] + offset).merge(s, left_on=["fips", "_y"], right_on=["fips", "_y"], how="left")
    return d.drop(columns="_y")


def controls(d):
    d["age2"] = d["age"] ** 2 / 100
    d["ed_lt12"] = (d["educ"] < 12).astype(float)
    d["ed_13_15"] = d["educ"].between(13, 15).astype(float)
    d["ed_16"] = (d["educ"] >= 16).astype(float)
    d["ed_miss"] = d["educ"].isna().astype(float)
    d["black"] = (d["race"] == "Black").astype(float)
    return d


CTRL = ["age", "age2", "ed_lt12", "ed_13_15", "ed_16", "ed_miss", "black", "married"]
CTRL_B = CTRL + ["bo2", "bo3p", "bo_miss"]


def reg(d, y, xs, ctrl, inter=None):
    """OLS with state and year FE; s.e. clustered by state and (separately) by woman."""
    d = d.copy()
    if inter:                                                   # interactions x * inter
        for x in list(xs):
            d[f"{x}_x_{inter}"] = d[x] * d[inter]
        xs = list(xs) + [f"{x}_x_{inter}" for x in xs]
    use = [y, *xs, *ctrl, "fips", "year", "pid"]
    d = d[use].replace([np.inf, -np.inf], np.nan).dropna()
    X = pd.concat([d[xs + ctrl].astype(float),
                   pd.get_dummies(d["fips"], prefix="s", drop_first=True, dtype=float),
                   pd.get_dummies(d["year"], prefix="y", drop_first=True, dtype=float)], axis=1)
    X = sm.add_constant(X, has_constant="add")
    r1 = sm.OLS(d[y].astype(float), X).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d["fips"])[0]})
    r2 = sm.OLS(d[y].astype(float), X).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d["pid"])[0]})
    return [dict(x=x, b=r1.params[x], se=r1.bse[x], p=r1.pvalues[x], se_m=r2.bse[x], p_m=r2.pvalues[x],
                 n=int(r1.nobs), n_states=d["fips"].nunique(), n_women=d["pid"].nunique(), mean_y=d[y].mean())
            for x in xs]


def cell(r):
    pv = "<0.001" if r["p"] < 0.001 else f"{r['p']:.3f}"
    pm = "<0.001" if r["p_m"] < 0.001 else f"{r['p_m']:.3f}"
    return (f"{r['b']:.4f}{stars(r['p'])} ({r['se']:.4f}; p={pv})<br>"
            f"<sub>mother-cl. ({r['se_m']:.4f}; p={pm})</sub>")


def table(results, columns, panels, title):
    """results: {(panel, column): [rows]}; one column per regression, regressors as rows, panels as row groups."""
    lines = [f"### {title}", "", "| | " + " | ".join(c for c, _ in columns) + " |",
             "|---|" + "---|" * len(columns)]
    for pname, xs in panels:
        lines.append(f"| **{pname}** |" + " |" * len(columns))
        for x, xl in xs:
            row = [xl]
            for c, _ in columns:
                rr = [r for r in results.get((pname, c), []) if r["x"] == x]
                row.append(cell(rr[0]) if rr else "")
            lines.append("| " + " | ".join(row) + " |")
        for lab, key in (("N", "n"), ("Women", "n_women"), ("State clusters", "n_states"), ("Mean outcome", "mean_y")):
            row = [lab]
            for c, _ in columns:
                rr = results.get((pname, c), [])
                row.append((f"{rr[0][key]:.3f}" if key == "mean_y" else f"{rr[0][key]:,}") if rr else "")
            lines.append("| " + " | ".join(row) + " |")
    lines += ["| State FE, birth-year FE | " + " | ".join("yes" for _ in columns) + " |", ""]
    return lines


# ---------------------------------------------------------------- main
def main():
    print("reading PSID ...", flush=True)
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    F, fips_check = family()
    E = employment_panel(py, F)
    ed, n_edvars = education()
    C = cah()
    S = pd.read_pickle(DATA / "state_shocks.pkl")
    st = py[["pid", "wave", "int"]].merge(F[["wave", "int", "fips"]], on=["wave", "int"], how="left")
    rc = py[["pid", "wave", "hrace"]]
    wf = py[["pid", "wave", "wife"]].assign(wife=py["wife"].astype(float))
    pby = py.groupby("pid")["birth_year"].median()

    # ---- births
    b = C[(C.CAH2 == 1) & (C.CAH10 > 0) & C.CAH15.between(1977, 2021)].copy()
    b["year"] = b["CAH15"]
    b["month"] = b["CAH13"].map(lambda m: m if 1 <= m <= 12 else {21: 1, 22: 4, 23: 7, 24: 10}.get(m, np.nan))
    b["border"] = b["CAH9"].where(b["CAH9"].between(1, 18))
    b = b.sort_values(["pid", "year", "month", "border"]).drop_duplicates(["pid", "year", "month"])
    n_births_all = len(b)
    b["married"] = np.where(b.CAH8 == 1, 1.0, np.where(b.CAH8.between(2, 7), 0.0, np.nan))
    myob = b["CAH7"].where(b["CAH7"].between(1900, 2010)).fillna(b["pid"].map(pby))
    b["age"] = b["year"] - myob
    b["bo2"] = (b["border"] == 2).astype(float)
    b["bo3p"] = (b["border"] >= 3).astype(float)
    b["bo_miss"] = b["border"].isna().astype(float)
    b["race"] = nearest(b, rc, "hrace", [-1, 0, -2, 1])
    b["fips"] = nearest(b, st, "fips", [0, 1, -1]).astype(float)
    for o, nm in ((-2, "m2"), (-1, "m1"), (1, "p1"), (2, "p2"), (3, "p3")):
        b[f"emp_{nm}"] = emp_at(b, E, "emp", o)
        b[f"emp500_{nm}"] = emp_at(b, E, "emp500", o)
    b = b.merge(ed, on="pid", how="left")
    b = controls(b)
    b = add_shocks(b, S)
    b = add_shocks(b, S, suffix="_l2", offset=-2)
    flow = [("births 1977-2021 to SRC/SEO women (twins once)", len(b))]
    b = b[b["race"].isin(["White", "Black"])]
    flow.append(("  head's race White or Black", len(b)))
    b = b[b["age"].between(15, 49)]
    flow.append(("  mother aged 15-49", len(b)))
    b = b[b["fips"].isin(S["fips"].unique())]
    flow.append(("  state observed", len(b)))
    flow.append(("  employment in year before birth observed (head / wife)", int(b["emp_m1"].notna().sum())))
    flow.append(("  employed in year before birth", int((b["emp_m1"] == 1).sum())))
    flow.append(("  ... and employment at b+1 observed", int(((b["emp_m1"] == 1) & b["emp_p1"].notna()).sum())))
    b.to_pickle(DATA / "first_stage_births.pkl")
    M = b[b["emp_m1"] == 1]
    N = b[b["emp_m1"] == 0]

    # ---- childless women (placebo i)
    fb = C[(C.CAH2 == 1) & (C.CAH10 > 0)].groupby("pid")["CAH15"].agg(["min", "max"])
    women = pd.DataFrame({"pid": C["pid"].unique()})
    women["first_birth"] = women["pid"].map(fb["min"])
    bad = fb.index[fb["max"] >= 9000]                           # some birth year unknown
    women = women[~women["pid"].isin(bad)]
    cw = pd.DataFrame([(p, t) for p in women["pid"] for t in range(1977, 2022)], columns=["pid", "year"]) \
        .merge(women, on="pid")
    cw = cw[cw["first_birth"].isna() | (cw["first_birth"] > cw["year"] + 1)]
    cw["age"] = cw["year"] - cw["pid"].map(pby)
    lo, hi = M["age"].quantile(0.02), M["age"].quantile(0.98)
    cw = cw[cw["age"].between(lo, hi)]
    cw["emp_m1"] = emp_at(cw, E, "emp", -1)
    cw["emp_p1"] = emp_at(cw, E, "emp", 1)
    cw = cw[(cw["emp_m1"] == 1) & cw["emp_p1"].notna()]
    cw["race"] = nearest(cw, rc, "hrace", [-1, 0, -2, 1])
    cw = cw[cw["race"].isin(["White", "Black"])]
    cw["fips"] = nearest(cw, st, "fips", [0, 1, -1]).astype(float)
    cw["married"] = nearest(cw, wf, "wife", [0, 1, -1]).astype(float)
    cw = cw.merge(ed, on="pid", how="left")
    cw = controls(cw)
    cw = add_shocks(cw, S)

    # ---- regressions
    res, rows = {}, []

    def run(table_id, panel, col, d, y, xs, ctrl, inter=None):
        r = reg(d, y, xs, ctrl, inter)
        res[(table_id, panel, col)] = r
        for x in r:
            rows.append(dict(table=table_id, panel=panel, column=col, outcome=y, **x))

    main_cols = [("Employed b+1", "emp_p1"), ("Employed b+2", "emp_p2"), ("Employed b+3", "emp_p3"),
                 ("Employed 500+ h b+1", "emp500_p1")]
    UR, BK = ["ur"], ["bartik_f", "bartik_m"]
    panels_main = [
        ("A. State unemployment rate (LAUS, %), birth year", UR, None),
        ("B. Bartik, leave-one-out (women's and men's industries, jointly)", BK, None),
        ("C. Bartik, national growth incl. own state", ["bartik_f_nat", "bartik_m_nat"], None),
        ("D. Bartik, rolling lagged shares", ["bartik_f_lag", "bartik_m_lag"], None),
        ("E. Unemployment rate x Black", UR, "black"),
        ("F. Bartik x Black", BK, "black"),
        ("G. Unemployment rate x married at birth", UR, "married"),
        ("H. Bartik x married at birth", BK, "married"),
    ]
    for pname, xs, inter in panels_main:
        for c, y in main_cols:
            run("main", pname, c, M, y, xs, CTRL_B, inter)

    plc_cols = [("(i) Childless women, employed t+1", "child"), ("(ii) Shock at b-2: employed b+1", "lag2"),
                ("(iii) Not employed at b-1: employed b+1", "ne1"), ("(iii) Not employed at b-1: employed b+2", "ne2")]
    panels_plc = [("A. State unemployment rate (LAUS, %)", UR), ("B. Bartik, leave-one-out (jointly)", BK)]
    for pname, xs in panels_plc:
        run("placebo", pname, plc_cols[0][0], cw, "emp_p1", xs, CTRL)
        run("placebo", pname, plc_cols[1][0], M.drop(columns=xs).rename(columns={x + "_l2": x for x in xs}),
            "emp_p1", xs, CTRL_B)
        run("placebo", pname, plc_cols[2][0], N, "emp_p1", xs, CTRL_B)
        run("placebo", pname, plc_cols[3][0], N, "emp_p2", xs, CTRL_B)

    out = pd.DataFrame(rows)
    out.to_csv(OUT / "first_stage.csv", index=False)

    # ---- markdown
    def tab(table_id, cols, panels, title):
        rr = {(p, c): v for (t, p, c), v in res.items() if t == table_id}
        pl = []
        for p in panels:
            pname, xs = p[0], p[1]
            inter = p[2] if len(p) > 2 else None
            xl = [(x, x) for x in xs] + ([(f"{x}_x_{inter}", f"{x} x {inter}") for x in xs] if inter else [])
            pl.append((pname, xl))
        return table(rr, cols, pl, title)

    L = ["# First stage: local slack at a birth and mothers' work (8.FirstStage.py)", "",
         "Each column is one regression (outcome in the header); regressors as rows; panels = separate "
         "regressions. Linear probability models with state and birth-year FE; controls: mother's age and age^2, "
         "education (<12, 13-15, 16+, missing; base 12), Black, married at birth, birth order (2, 3+, missing). "
         "Cell: coefficient, stars, (s.e. clustered by state; p-value); second line: s.e. clustered by mother. "
         "*** p<0.01, ** p<0.05, * p<0.1. Unemployment rate in percentage points; Bartik = predicted employment "
         "growth in % (higher = tighter). The search friction predicts + on the unemployment rate and - on "
         "bartik_f (women's-industry slack -> more mothers keep working).", ""]
    L += tab("main", main_cols, panels_main, "Table 1. Mothers employed in the year before the birth")
    L += tab("placebo", plc_cols, panels_plc, "Table 2. Placebos")
    L += ["(i) woman-years t of women with a childbirth history and no birth up to t+1, aged "
          f"{lo:.0f}-{hi:.0f}, employed in t-1; shock in t. (ii) mothers employed at b-1, shock measured two years "
          "before the birth. (iii) mothers not employed at b-1.", ""]
    L += ["## Sample", "", "| step | births |", "|---|---|"] + [f"| {a} | {n:,} |" for a, n in flow]
    L += ["", f"Childless placebo: {len(cw):,} woman-years, {cw['pid'].nunique():,} women.",
          f"Education variables used: {n_edvars}. PSID->FIPS state check ({FIPS_CHECK[0]}): {fips_check:.4f}.", ""]
    yr = M.groupby("year").agg(births=("pid", "size"), emp_p1=("emp_p1", "mean"), emp_p2=("emp_p2", "mean"),
                               emp_p3=("emp_p3", "mean"), black=("black", "mean"), married=("married", "mean"),
                               ur=("ur", "mean"))
    yr_all = b.groupby("year").agg(all_births=("pid", "size"), emp_before=("emp_m1", "mean"))
    L += ["## Mothers employed at b-1, by birth year (shares)", "",
          yr_all.join(yr).round(3).to_markdown(), ""]
    L += ["## Employment panel sources (woman-years)", "", E.groupby("src").agg(
        n=("emp", "size"), share_emp=("emp", "mean"), first=("year", "min"), last=("year", "max"))
        .round(3).to_markdown(), ""]
    (OUT / "first_stage.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
