r"""Paper B: public policies and economic shocks (Fable memo proposals/fable_policy_shocks_paperB.md, designs D1-D3;
2026-10-18).

D1 LABOR-MARKET CONDITIONS AT ENTRY. Entry year = birth year + 18 + max(schooling - 12, 0) (the model's entry age,
   schooling capped at 18). (a) STATE: the unemployment rate (BLS LAUS, data/state_shocks.pkl 'ur', 1976-2024) in the
   entry year, in the state of the son's parental family when he was 17 (intent to treat; the family-file state of the
   unit he lives in as a child at the interview nearest age 17 within 14-20, waves 1976+; data/husband_shocks_fam.pkl
   'fips'); also the mean rate over his first ten years after entry (>= 5 years observed) and the men's Bartik
   (leave-one-out, 'bartik_m') in the entry year. State and entry-year fixed effects; no region x year effects.
   (b) NATIONAL: the national annual unemployment rate (BLS CPS annual averages, hard-coded below; checked against the
   mean of the state rates) in the entry year, with a linear birth-cohort trend and no state FE; all entry years.
   Outcomes (son level; 35's son frame): access = the son's modal job at 25-34 is a well-paid, high-later-growth cell
   (Table 8 / 35 'eset' == 1); ln hourly wage averaged at 25-34 and at 35-55. Regressors: the entry rate, the rate x
   centred ln parental income, ln parental income, years of schooling, quartic in the parent's age. By race and pooled
   (weighted). S.e. clustered by state at 17 (state version) or by entry year (national version).
   (c) The age profile of the racial gap by entry conditions: sons split by the sign of the residual of the state entry
   rate on state and entry-year FE (slack vs tight entry); 33's child-year design by band and race in each group;
   openings and their difference (bands 25-49).
D2 THE PUBLIC SECTOR. The head's 'work for government?' item of the family files (1980 'C3 WORK FOR GOVT (HD-E)';
   1981-2001 'B.. WORK FOR GOVT? (HD-E)', first such item; 2003-2023 'BC24 WORK FOR GOVT?--JOB 1'), 1 = yes, 5 = no; self-
   employed (25.JointJobLoss.py cache, codes 2-3) form their own sector. Son-years as head. (a) Share of sons whose modal
   sector at 25-34 is government, by race and parental tercile; (b) access to good jobs among private starters, by
   race; (c) the age profile of the racial gap among sons whose modal sector at 25-34 is private (33 design); (d) the
   return to schooling by age band and race within the current sector (36's engine; rise = mean >= 35 minus < 35).
D3 THE FATHER'S DISPLACEMENT, RE-SCORED BY THE SON'S AGE. 19.FatherDisplacement.py's child design (father figure's first
   main displacement - plant closure / move or layoff / firing - at the son's 0-17 vs never exposed; controls: log
   pre-event family income, parental schooling, birth-year FE; father figure working before the (pseudo) event).
   Sons only. Outcome: ln of the son's mean own earnings (and family income) at 25-34 and at 35-44 (>= 2 valid years;
   6.IGEMain bounds). One stacked regression with every regressor interacted with the band; the change of the
   displacement coefficient from 25-34 to 35-44 by race; clusters 1968 family. Selection-on-observables comparison
   (an upper bound on the causal effect, EVIDENCE 5.x); the object here is its age profile.
DESCRIPTIVE / reduced form. Writes output/paperB_policy_shocks.csv and .md.
"""
import importlib.util
import re
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


R33 = _load("ige33", "33.AgeProfileRobustness.py")
ige6 = R33.ige6
GC, A4, RACES = R33.GC, R33.A4, R33.RACES
ERN, FAM = R33.FAM.replace("family income", "own earnings"), R33.FAM
CSV = []

# BLS, civilian unemployment rate, annual averages (CPS), percent
NATUR = {1963: 5.7, 1964: 5.2, 1965: 4.5, 1966: 3.8, 1967: 3.8, 1968: 3.6, 1969: 3.5, 1970: 4.9, 1971: 5.9, 1972: 5.6,
         1973: 4.9, 1974: 5.6, 1975: 8.5, 1976: 7.7, 1977: 7.1, 1978: 6.1, 1979: 5.8, 1980: 7.1, 1981: 7.6, 1982: 9.7,
         1983: 9.6, 1984: 7.5, 1985: 7.2, 1986: 7.0, 1987: 6.2, 1988: 5.5, 1989: 5.3, 1990: 5.6, 1991: 6.8, 1992: 7.5,
         1993: 6.9, 1994: 6.1, 1995: 5.6, 1996: 5.4, 1997: 4.9, 1998: 4.5, 1999: 4.2, 2000: 4.0, 2001: 4.7, 2002: 5.8,
         2003: 6.0, 2004: 5.5, 2005: 5.1, 2006: 4.6, 2007: 4.6, 2008: 5.8, 2009: 9.3, 2010: 9.6, 2011: 8.9, 2012: 8.1,
         2013: 7.4, 2014: 6.2, 2015: 5.3, 2016: 4.9, 2017: 4.4, 2018: 3.9, 2019: 3.7, 2020: 8.1, 2021: 5.3, 2022: 3.6,
         2023: 3.6, 2024: 4.0}


def fmt(e, se, p):
    if e is None or not np.isfinite(e):
        return ""
    pv = "<0.001" if p < 0.001 else f"{p:.3f}"
    return f"{e:.3f}{stars(p)} ({se:.3f}; p={pv})"


def rec(tab, sample, outcome, term, e, se, p, **kw):
    CSV.append(dict(table=tab, sample=sample, outcome=outcome, term=term, coef=e, se=se, p=p, **kw))


def ols(d, y, xs, fe=(), cluster="fam68", w=None):
    cols = list(dict.fromkeys([y, *xs, *fe, cluster] + ([w] if w else [])))
    d = d[cols].replace([np.inf, -np.inf], np.nan).dropna()
    if w:
        d = d[d[w] > 0]
    X = d[list(xs)].astype(float)
    for f in fe:
        X = X.join(pd.get_dummies(d[f].astype(int), prefix=f, drop_first=True, dtype=float))
    X = sm.add_constant(X, has_constant="add")
    X = X.loc[:, (X.std() > 0) | (X.columns == "const")]
    mod = sm.WLS(d[y].astype(float), X, weights=d[w]) if w else sm.OLS(d[y].astype(float), X)
    r = mod.fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d[cluster])[0]})
    return r, len(d), d[cluster].nunique()


# ================================================================ son frame (35)
def son_frames():
    R35 = _load("e35", "35.EarlyIndustryLatePayoff.py")
    D32, D27 = R35.D32, R35.D27
    W = D32.ind_crosswalks()
    XWD = D27.crosswalks()
    M = D32.morg_measures(D32.morg_micro(W, XWD))
    R35.STEEP32 = set(M["steep"])
    MF = R35.morg_flex(M)
    R35.data_sets(MF)
    R35.MF_G = MF
    r = D32.son_panel(W, M)
    rc = r.attrs["rc"]
    r.attrs = {}
    D27.CLIDX = pd.Index(np.unique(r["fam68"].dropna().unique().astype(float)))
    D27.NCL = len(D27.CLIDX)
    r["fam68"] = r["fam68"].astype(float)
    d = R35.prep(r, MF, W, rc)
    S = R35.son_frame(d)
    S["terc"] = S["pid"].map(d.drop_duplicates("pid").set_index("pid")["terc"])
    A = d.drop_duplicates("pid").set_index("pid")["A"]
    S["A"] = S["pid"].map(A)
    for k in range(1, 5):
        S[f"A{k}"] = ((S["A"] - 45) / 10) ** k
    return r, d, S


def entry_vars(S):
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    hs = pd.read_pickle(DATA / "husband_shocks_fam.pkl")[["wave", "int", "fips"]].drop_duplicates(["wave", "int"])
    c = py[py["child"] & py["age"].between(14, 20) & (py["wave"] >= 1976)][["pid", "wave", "int", "age"]]
    c = c.merge(hs, on=["wave", "int"], how="inner").dropna(subset=["fips"])
    c = c.assign(dist=(c["age"] - 17).abs()).sort_values(["pid", "dist", "wave"]).drop_duplicates("pid")
    S = S.merge(c[["pid", "fips"]].rename(columns={"fips": "fips17"}), on="pid", how="left")
    S["entry_age"] = 18 + np.clip(S["educ"].fillna(12) - 12, 0, 6)
    S["entry_year"] = (S["birth_year"] + S["entry_age"]).round()
    st = pd.read_pickle(DATA / "state_shocks.pkl")[["fips", "year", "ur", "bartik_m"]]
    ur = st.set_index(["fips", "year"])["ur"]
    bm = st.set_index(["fips", "year"])["bartik_m"]
    key = list(zip(S["fips17"], S["entry_year"]))
    S["ur_e"] = [ur.get(k, np.nan) for k in key]
    S["bart_e"] = [bm.get(k, np.nan) for k in key]
    S["ur_10"] = [np.nanmean([ur.get((f, y + j), np.nan) for j in range(10)])
                  if np.sum([np.isfinite(ur.get((f, y + j), np.nan)) for j in range(10)]) >= 5 else np.nan
                  for f, y in key]
    S["urN_e"] = S["entry_year"].map(NATUR)
    S["lyp_c"] = S["lyp"] - S["lyp"].mean()
    for v in ("ur_e", "ur_10", "bart_e", "urN_e"):
        S[f"{v}_x"] = S[v] * S["lyp_c"]
    S["coh"] = (S["birth_year"] - 1960) / 10
    S["G25"] = (S["eset"] == 1).astype(float).where(S["eset"].notna())
    # national rate check: correlation with the mean of the state rates
    m = st.groupby("year")["ur"].mean()
    common = [y for y in m.index if y in NATUR]
    chk = np.corrcoef([m[y] for y in common], [NATUR[y] for y in common])[0, 1]
    return S, chk


# ================================================================ D1
def d1(S, md, chk):
    outs = [("G25", "access: good job at 25-34"), ("lw0", "ln wage, 25-34"), ("lw35", "ln wage, 35-55")]
    specs = [("state: entry rate", "ur_e", ("fips17", "entry_year"), "fips17", ["educ"]),
             ("state: entry rate, no schooling control", "ur_e", ("fips17", "entry_year"), "fips17", []),
             ("state: mean rate over the first 10 years", "ur_10", ("fips17", "entry_year"), "fips17", ["educ"]),
             ("state: men's Bartik at entry", "bart_e", ("fips17", "entry_year"), "fips17", ["educ"]),
             ("national: entry rate, cohort trend", "urN_e", (), "entry_year", ["educ", "coh"])]
    L = ["## D1. Labor-market conditions at entry", "",
         f"Entry year = birth year + 18 + max(schooling - 12, 0). National rate check: correlation of the hard-coded BLS "
         f"annual national rate with the mean of the LAUS state rates, 1976-2024: {chk:.3f}. Each cell: coefficient (s.e.; "
         "p); one regression per outcome x specification x sample; regressors: the shock, shock x centred ln parental "
         "income, ln parental income, quartic in parent's age, (+ years of schooling), FE in the row label. Pooled "
         "weighted (Black + White), races unweighted. The Bartik is a predicted employment growth rate (higher = tighter).",
         ""]
    hdr = "| Specification | Sample | term | " + " | ".join(lab for _, lab in outs) + " |"
    L += [hdr, "|---" * (len(outs) + 3) + "|"]
    for sp, x, fe, cl, extra in specs:
        for g in ("Pooled", "Black", "White"):
            q = S if g == "Pooled" else S[S["race"] == g]
            q = q[q["race"].isin(RACES)]
            res = {}
            for y, ylab in outs:
                xs = [x, f"{x}_x", "lyp", *A4, *extra]
                try:
                    r, n, ncl = ols(q, y, xs, fe, cl, "wpool" if g == "Pooled" else None)
                except Exception as exc:
                    print("skip", sp, g, y, exc)
                    continue
                res[y] = (r, n, ncl)
                for t in (x, f"{x}_x"):
                    rec("D1 entry conditions", g, ylab, f"{sp} | {t}", r.params[t], r.bse[t], r.pvalues[t], n=n,
                        clusters=ncl, mean=float(q[y].mean()))
            for t, tl in ((x, "shock"), (f"{x}_x", "shock x ln parental income")):
                L.append(f"| {sp} | {g} | {tl} | " + " | ".join(
                    fmt(res[y][0].params[t], res[y][0].bse[t], res[y][0].pvalues[t]) if y in res else ""
                    for y, _ in outs) + " |")
            L.append(f"| | {g} | N sons / clusters | " + " | ".join(
                f"{res[y][1]:,} / {res[y][2]}" if y in res else "" for y, _ in outs) + " |")
    # race differences of the shock coefficient (independent samples)
    L += ["", "Race differences (White - Black) of the shock coefficient (independent samples):", "",
          "| Specification | " + " | ".join(lab for _, lab in outs) + " |", "|---" * (len(outs) + 1) + "|"]
    df = pd.DataFrame(CSV)
    for sp, x, *_ in specs:
        cells = []
        for y, ylab in outs:
            z = df[(df["table"] == "D1 entry conditions") & (df["outcome"] == ylab) & (df["term"] == f"{sp} | {x}")]
            zz = z.set_index("sample")
            if {"Black", "White"} <= set(zz.index):
                e = zz.loc["White", "coef"] - zz.loc["Black", "coef"]
                se = np.hypot(zz.loc["White", "se"], zz.loc["Black", "se"])
                p = 2 * norm.sf(abs(e / se))
                cells.append(fmt(e, se, p))
                rec("D1 entry conditions", "White - Black", ylab, f"{sp} | {x}", e, se, p)
            else:
                cells.append("")
        L.append(f"| {sp} | " + " | ".join(cells) + " |")
    md += L + [""]


def d1_profile(S, md):
    """33 design by slack vs tight entry (residual of the state entry rate on state and entry-year FE)."""
    q = S.dropna(subset=["ur_e", "fips17", "entry_year"]).copy()
    X = pd.get_dummies(q[["fips17", "entry_year"]].astype(int).astype(str), drop_first=True, dtype=float)
    X = sm.add_constant(X)
    q["ur_res"] = q["ur_e"] - sm.OLS(q["ur_e"], X).fit().fittedvalues
    slack = q.set_index("pid")["ur_res"] > 0
    s = R33.psid_frames()
    s["slack"] = s["pid"].map(slack)
    for y, ylab in (("learn", ERN), ("lfam", FAM)):
        x = s[(s["female"] == 0) & s["slack"].notna()]
        fr = {"Slack entry (state rate above its state and year norm)": R33.prep(x[x["slack"] == True], y, "lyp"),  # noqa
              "Tight entry": R33.prep(x[x["slack"] == False], y, "lyp")}  # noqa: E712
        R = R33.run(fr, A4)
        for sp in fr:
            R33.summarize(R, "PSID", "entry profile", sp, "Sons", ylab)
    res = pd.DataFrame(R33.ROWS)
    res = res[res["block"] == "entry profile"]
    L = ["### D1 (c). Age profile of the racial gap by entry conditions (sons entering 1976+ with a state at 17)", "",
         "| | " + " | ".join(f"{sp}: {o}" for sp in ("Slack", "Tight") for o in ("earnings", "family income")) + " |",
         "|---" * 5 + "|"]
    sps = ["Slack entry (state rate above its state and year norm)", "Tight entry"]
    for b in R33.BL:
        L.append(f"| W - B gap, {b} | " + " | ".join(
            fmt(*res[(res.spec == sp) & (res.outcome == o) & (res.band == b) & (res.group == "White - Black")
                     & (res.stat == "IGE")][["est", "se", "p"]].iloc[0]) if len(
                res[(res.spec == sp) & (res.outcome == o) & (res.band == b) & (res.group == "White - Black")]) else ""
            for sp in sps for o in (ERN, FAM)) + " |")
    for g in ("Black", "White", "White - Black"):
        cells = []
        for sp in sps:
            for o in (ERN, FAM):
                z = res[(res.spec == sp) & (res.outcome == o) & (res.band == "test") & (res.group == g)
                        & (res.stat == GC) & (res.bandset == "25-49")]
                cells.append(fmt(*z[["est", "se", "p"]].iloc[0]) if len(z) else "")
                if len(z):
                    rec("D1 profile by entry", sp, o, f"{g} opening", *z[["est", "se", "p"]].iloc[0])
        L.append(f"| {g}: opening | " + " | ".join(cells) + " |")
    # difference slack - tight in the W-B opening (independent samples: different sons)
    cells = []
    for o in (ERN, FAM):
        a = [res[(res.spec == sp) & (res.outcome == o) & (res.band == "test") & (res.group == "White - Black")
                 & (res.stat == GC) & (res.bandset == "25-49")] for sp in sps]
        if all(len(z) for z in a):
            e = a[0]["est"].iloc[0] - a[1]["est"].iloc[0]
            se = np.hypot(a[0]["se"].iloc[0], a[1]["se"].iloc[0])
            p = 2 * norm.sf(abs(e / se))
            cells.append(fmt(e, se, p))
            rec("D1 profile by entry", "Slack - Tight", o, "W - B opening", e, se, p)
    L.append("| Slack minus tight, W - B opening (earnings; family income) | " + " ; ".join(cells) + " | | | |")
    n = q.groupby("race")["pid"].nunique()
    L += ["", f"Sons with a state entry rate: Black {n.get('Black', 0):,}, White {n.get('White', 0):,}. Shared families "
          "across the two groups make the slack-minus-tight standard error approximate.", ""]
    md += L


# ================================================================ D2
GOVPAT = [r"^[A-Z]\d+ (WTR )?WORK FOR GOVT.*\(HD-E\)", r"^BC24 WORK FOR GOVT\?--JOB 1"]


def gov_items():
    f = DATA / "paperB_gov_items.pkl"
    if f.exists():
        return pd.read_pickle(f)
    R8 = _load("fs8", "8.FirstStage.py")
    p1 = _load("p1", "1.PSID.py")
    out = []
    for w in [w for w in R8.WAVES if w >= 1980]:
        folder = p1.FAM / (f"fam{w}" if w < 1994 else f"fam{w}er")
        base = next(x for x in folder.glob("*.do") if "formats" not in x.name).with_suffix("")
        pos, labs = R8.layout(base.with_suffix(".do"))
        labs = [(v, l) for v, l in labs if v in pos]
        idv = labs[1][0]
        hit = None
        for pat in GOVPAT:
            hit = next((v for v, l in labs if re.search(pat, l)), None)
            if hit:
                break
        if hit is None:
            print("no govt item", w)
            continue
        x = R8.read(base, [idv, hit], pos).rename(columns={idv: "int", hit: "gov_raw"})
        x["wave"] = w
        x["item"] = hit
        out.append(x)
        print(f"  govt item {w}: {hit}", flush=True)
    G = pd.concat(out, ignore_index=True)
    G.to_pickle(f)
    return G


def d2(r, d, S, md):
    import pandas as pd  # noqa
    G = gov_items()
    se = pd.read_pickle(DATA / "joint_job_loss_selfemp.pkl")["X"][["wave", "int", "h_se"]].drop_duplicates(
        ["wave", "int"])
    v = d[d["valid"] & d["lw"].notna() & d["race"].isin(RACES)].copy()
    v = v.merge(G[["wave", "int", "gov_raw"]], on=["wave", "int"], how="left").merge(se, on=["wave", "int"],
                                                                                      how="left")
    # codes: yes / no waves (1 = yes, 5 = no; 1980-84) or 1-3 = federal / state / local government, 4 = private
    # company, 7 = other (1985+, BC24 2003+); 0 = inap. (self-employed, not working)
    yn = v.groupby("wave")["gov_raw"].transform(lambda c: set(c.dropna().unique()) <= {0, 1, 5, 8, 9})
    gov = np.where(yn, v["gov_raw"] == 1, v["gov_raw"].isin([1, 2, 3]))
    prv = np.where(yn, v["gov_raw"] == 5, v["gov_raw"] == 4)
    v["sector"] = np.where(v["h_se"].isin([2, 3]), "self", np.where(gov, "gov", np.where(prv, "private", None)))
    codes = G["gov_raw"].value_counts().head(6).to_dict()
    e = v[v["age"].between(25, 34) & v["sector"].notna()].groupby("pid")["sector"].agg(
        lambda s: s.value_counts().index[0])
    S = S.copy()
    S["sec25"] = S["pid"].map(e)
    L = ["## D2. The public sector", "", f"Government item codes (all waves, head): {codes}; items by wave: "
         f"{G.groupby('wave')['item'].first().to_dict()}. Son-years as head with a valid wage; sector = self-employed "
         "(codes 2-3 of 'work for self or others'), government (1980-84: 1 = yes; 1985+: federal, state or local "
         "government, codes 1-3), private (1980-84: 5 = no; 1985+: private company, code 4).", ""]
    # (a) shares by race x tercile
    L += ["| Race | parental tercile | sons with a 25-34 sector | government | private | self-employed | "
          "good job at 25-34, government starters | good job, private starters |", "|---|---|---|---|---|---|---|---|"]
    for g in RACES:
        for t in (1, 2, 3, None):
            z = S[(S["race"] == g) & S["sec25"].notna()]
            z = z if t is None else z[z["terc"] == t]
            if len(z) < 20:
                continue
            sh = z["sec25"].value_counts(normalize=True)
            gg = z.loc[z["sec25"] == "gov", "G25"].mean() if "G25" in z else np.nan
            gp = z.loc[z["sec25"] == "private", "G25"].mean() if "G25" in z else np.nan
            L.append(f"| {g} | {'all' if t is None else t} | {len(z):,} | {sh.get('gov', 0):.3f} | "
                     f"{sh.get('private', 0):.3f} | {sh.get('self', 0):.3f} | {gg:.3f} | {gp:.3f} |")
            rec("D2 sector shares", g, "government share at 25-34", f"tercile {t}", sh.get("gov", 0), np.nan, np.nan,
                n=len(z))
    # government share on race at equal parental income
    q = S[S["sec25"].notna() & S["race"].isin(RACES)].assign(gov25=lambda z: (z["sec25"] == "gov").astype(float),
                                                              white=lambda z: (z["race"] == "White").astype(float))
    r1, n1, c1 = ols(q, "gov25", ["white", "lyp", *A4], (), "fam68", "wpool")
    r2, n2, c2 = ols(q, "gov25", ["white", "lyp", "educ", *A4], (), "fam68", "wpool")
    L += ["", f"Government at 25-34 on White (weighted, clusters 1968 family): with ln parental income "
          f"{fmt(r1.params['white'], r1.bse['white'], r1.pvalues['white'])}; + schooling "
          f"{fmt(r2.params['white'], r2.bse['white'], r2.pvalues['white'])} (N {n1:,}).", ""]
    rec("D2 government on race", "Pooled", "government at 25-34", "white | lyp", r1.params["white"], r1.bse["white"],
        r1.pvalues["white"], n=n1)
    rec("D2 government on race", "Pooled", "government at 25-34", "white | lyp + educ", r2.params["white"],
        r2.bse["white"], r2.pvalues["white"], n=n2)
    # (b) access among private starters
    pv = q[q["sec25"] == "private"]
    r3, n3, _ = ols(pv, "G25", ["white", "lyp", *A4], (), "fam68", "wpool")
    r4, n4, _ = ols(q, "G25", ["white", "lyp", *A4], (), "fam68", "wpool")
    L += [f"Access to good jobs on White at equal parental income: all sons with a sector "
          f"{fmt(r4.params['white'], r4.bse['white'], r4.pvalues['white'])} (N {n4:,}); private starters "
          f"{fmt(r3.params['white'], r3.bse['white'], r3.pvalues['white'])} (N {n3:,}).", ""]
    rec("D2 access", "all with sector", "good job at 25-34", "white | lyp", r4.params["white"], r4.bse["white"],
        r4.pvalues["white"], n=n4)
    rec("D2 access", "private starters", "good job at 25-34", "white | lyp", r3.params["white"], r3.bse["white"],
        r3.pvalues["white"], n=n3)
    # (c) age profile among private starters
    s = R33.psid_frames()
    s["sec25"] = s["pid"].map(e)
    for y, ylab in (("learn", ERN), ("lfam", FAM)):
        x = s[(s["female"] == 0)]
        fr = {"All sons (33)": R33.prep(x, y, "lyp"),
              "Sons whose 25-34 sector is private": R33.prep(x[x["sec25"] == "private"], y, "lyp"),
              "Sons whose 25-34 sector is government": R33.prep(x[x["sec25"] == "gov"], y, "lyp")}
        R = R33.run(fr, A4)
        for sp in fr:
            R33.summarize(R, "PSID", "sector profile", sp, "Sons", ylab)
        R33.diff(R, "PSID", "sector profile", "Sons whose 25-34 sector is private", "All sons (33)", "Sons", ylab)
    res = pd.DataFrame(R33.ROWS)
    res = res[res["block"] == "sector profile"]
    L += ["### D2 (c). Opening of the racial gap by sector at 25-34 (bands 25-49)", "",
          "| Sample | W - B opening, earnings | W - B opening, family income | minus all sons (earnings; family) |",
          "|---|---|---|---|"]
    for sp in ("All sons (33)", "Sons whose 25-34 sector is private", "Sons whose 25-34 sector is government"):
        cells = []
        for o in (ERN, FAM):
            z = res[(res.spec == sp) & (res.outcome == o) & (res.band == "test") & (res.group == "White - Black")
                    & (res.stat == GC) & (res.bandset == "25-49")]
            cells.append(fmt(*z[["est", "se", "p"]].iloc[0]) if len(z) else "")
            if len(z):
                rec("D2 sector profile", sp, o, "W - B opening", *z[["est", "se", "p"]].iloc[0])
        dd = []
        for o in (ERN, FAM):
            z = res[(res.spec == sp) & (res.outcome == o) & (res.band == "test") & (res.group == "White - Black")
                    & (res.stat == "Gap change minus [All sons (33)]") & (res.bandset == "25-49")]
            dd.append(fmt(*z[["est", "se", "p"]].iloc[0]) if len(z) else "")
        L.append(f"| {sp} | {cells[0]} | {cells[1]} | {'; '.join(x for x in dd if x)} |")
    md += L + [""]
    return v


def d2_returns(v, md):
    """return to schooling by band x race within the current sector (36 engine)."""
    R36 = _load("s36", "36.SameEmployerGrowthChecks.py")
    R36.CL = pd.Index(np.unique(v["fam68"].dropna().astype(float)))
    v = v.copy()
    v["yfe"], v["cl"] = v["year"], v["fam68"].astype(float)
    B6 = [(25, 29), (30, 34), (35, 39), (40, 44), (45, 49), (50, 55)]
    for sec in ("private", "gov"):
        R36.run(f"ret_{sec}", v[v["sector"] == sec], "lw", ["educ"], bands=B6, need=["educ"])

    def change(tag, g):
        lo = [b for b in B6 if b[0] < 35]
        hi = [b for b in B6 if b[0] >= 35]
        return R36.lin([(R36.G(tag, "lw", a, b, g, "educ"), 1 / len(hi)) for a, b in hi]
                       + [(R36.G(tag, "lw", a, b, g, "educ"), -1 / len(lo)) for a, b in lo])
    L = ["### D2 (d). Return to a year of schooling (ln hourly wage) by age band and race, within the current sector",
         "", "| Sector | group | 25-29 | 30-34 | 35-39 | 40-44 | 45-49 | 50-55 | rise (>= 35 minus < 35) |",
         "|---|---|---|---|---|---|---|---|---|"]
    for sec in ("private", "gov"):
        for g, gl in (("W", "White"), ("B", "Black"), ("BW", "White - Black")):
            cells = []
            for a, b in B6:
                e = R36.G(f"ret_{sec}", "lw", a, b, g, "educ")
                if g == "BW" and e is not None:
                    e = (-e[0], -e[1])
                cells.append(R36.cell(e))
            ch = change(f"ret_{sec}", g)
            if g == "BW" and ch is not None:
                ch = (-ch[0], -ch[1])
            b_, se_, p_ = R36.tsp(ch)
            rec("D2 return to schooling by sector", sec, "ln hourly wage", f"{gl} rise", b_, se_, p_)
            L.append(f"| {sec} | {gl} | " + " | ".join(cells) + f" | {R36.cell(ch)} |")
    md += L + [""]


# ================================================================ D3
def d3(md):
    R19 = _load("fd19", "19.FatherDisplacement.py")
    psid9 = R19.psid9
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    fam = psid9.family()
    m = R19.men_panel(py, fam)
    disp = pd.read_pickle(DATA / "psid_displacement.pkl")
    kx = pd.read_pickle(DATA / "psid_child_exposure.pkl")
    pk = pd.read_pickle(DATA / "psid_kids.pkl")
    ind = psid9.individual()[0]
    K, ff, inc = R19.child_frame(py, m, kx, pk, ind)
    hw = py[(py["head"] & (py["female"] == 1)) | py["wife"]][["pid", "wave", "int", "head"]]
    hw = hw.merge(fam[["wave", "int", "hh", "wh"]], on=["wave", "int"], how="left")
    hw["hrs"] = np.where(hw["head"], hw["hh"], hw["wh"])
    H = hw.assign(year=hw["wave"] - 1).dropna(subset=["hrs"]).drop_duplicates(["pid", "year"]).set_index(
        ["pid", "year"])["hrs"]
    educ = ind.set_index("pid")["educ"]
    ev = disp.loc[disp["main"] == 1, ["pid", "year"]]
    b, astar = R19.design(K, ff, ev, 0, 17)
    b = R19.measures(b, m, inc, H)
    b = b.merge(K[["pid", "female", "race", "fam68"]], on="pid", how="left")
    pe = np.fmax(educ.reindex(b["f0"]).to_numpy(), educ.reindex(b["mom"].fillna(-1)).to_numpy())
    b["pe"] = R19.ecat(pd.Series(pe)).to_numpy()
    b = b[(b["female"] == 0) & b["race"].isin(RACES)].copy()
    # son's band means
    s = ige6.build(py)
    s = s[s["pid"].isin(b["pid"])]
    rows = []
    for band, (lo, hi) in (("25-34", (25, 34)), ("35-44", (35, 44))):
        for y, raw in (("earn", "earn"), ("fam", "faminc")):
            col = "learn" if y == "earn" else "lfam"
            h = s[s["age"].between(lo, hi) & s[col].notna()].groupby("pid")[raw].agg(["mean", "count"])
            h = h[h["count"] >= 2]
            rows.append(pd.DataFrame({"pid": h.index, "band": band, "y": y, "ly": np.log(h["mean"].to_numpy())}))
    Y = pd.concat(rows, ignore_index=True)
    L = ["## D3. The father's displacement at the son's 0-17, re-scored at the son's 25-34 and 35-44", "",
         f"19's child design, sons only; controls' pseudo event age {astar}. Each cell: displacement coefficient (s.e.; "
         "p) from one stacked regression in which every regressor (displaced, log pre-event family income, parental "
         "schooling, birth-year FE) is interacted with the band; clusters 1968 family.", "",
         "| Outcome | Sample | displaced, 25-34 | displaced, 35-44 | change (35-44 minus 25-34) | sons (25-34 / 35-44) "
         "| displaced sons |", "|---|---|---|---|---|---|---|"]
    store = {}
    for y, ylab in (("earn", "ln own earnings"), ("fam", "ln family income")):
        for g in ("Pooled", "Black", "White"):
            q = b if g == "Pooled" else b[b["race"] == g]
            z = Y[Y["y"] == y].merge(q[["pid", "treat", "lpre", "pe", "birth_year", "fam68", "race"]], on="pid")
            z = z.dropna(subset=["ly", "lpre"])
            z["late"] = (z["band"] == "35-44").astype(float)
            Xb = pd.DataFrame({"treat": z["treat"].astype(float), "lpre": z["lpre"]})
            Xb = Xb.join(pd.get_dummies(z["pe"], prefix="pe", drop_first=True, dtype=float))
            Xb = Xb.join(pd.get_dummies(z["birth_year"].astype(int), prefix="by", drop_first=True, dtype=float))
            if g == "Pooled":
                Xb["black"] = (z["race"] == "Black").astype(float)
            Xb.insert(0, "const", 1.0)
            X = pd.concat([Xb.mul(1 - z["late"], axis=0).add_suffix("_e"), Xb.mul(z["late"], axis=0).add_suffix("_l")],
                          axis=1)
            X = X.loc[:, X.std() > 0]
            r = sm.OLS(z["ly"].astype(float), X).fit(cov_type="cluster",
                                                     cov_kwds={"groups": pd.factorize(z["fam68"])[0]})
            V = r.cov_params()
            e1, e2 = r.params["treat_e"], r.params["treat_l"]
            ch = e2 - e1
            sch = np.sqrt(V.loc["treat_e", "treat_e"] + V.loc["treat_l", "treat_l"] - 2 * V.loc["treat_e", "treat_l"])
            pch = 2 * norm.sf(abs(ch / sch))
            store[(y, g)] = (ch, sch)
            ne = int((z["late"] == 0).sum())
            nl = int((z["late"] == 1).sum())
            nt = z.loc[z["treat"] == 1, "pid"].nunique()
            L.append(f"| {ylab} | {g} | {fmt(e1, r.bse['treat_e'], r.pvalues['treat_e'])} | "
                     f"{fmt(e2, r.bse['treat_l'], r.pvalues['treat_l'])} | {fmt(ch, sch, pch)} | {ne:,} / {nl:,} | "
                     f"{nt:,} |")
            for t, (e, s_, p_) in (("25-34", (e1, r.bse["treat_e"], r.pvalues["treat_e"])),
                                   ("35-44", (e2, r.bse["treat_l"], r.pvalues["treat_l"])),
                                   ("change", (ch, sch, pch))):
                rec("D3 father displacement by son's age", g, ylab, t, e, s_, p_, n=ne + nl, treated=nt)
        cw, cb = store[(y, "White")], store[(y, "Black")]
        e = cw[0] - cb[0]
        se_ = np.hypot(cw[1], cb[1])
        p_ = 2 * norm.sf(abs(e / se_))
        L.append(f"| {ylab} | White - Black change | | | {fmt(e, se_, p_)} | | |")
        rec("D3 father displacement by son's age", "White - Black", ylab, "change", e, se_, p_)
    md += L + [""]


def main():
    OUT.mkdir(exist_ok=True)
    md = ["# Paper B: public policies and economic shocks (Fable memo designs D1-D3)", "",
          "Built by `49.PaperBPolicyShocks.py` (2026-10-18); definitions in its docstring. Every coefficient: estimate "
          "(s.e.; p), *** p<0.01, ** p<0.05, * p<0.1. **Reduced form / descriptive.**", ""]
    print("son frame ...", flush=True)
    r, d, S = son_frames()
    S, chk = entry_vars(S)
    print("D1 ...", flush=True)
    d1(S, md, chk)
    d1_profile(S, md)
    print("D2 ...", flush=True)
    v = d2(r, d, S, md)
    d2_returns(v, md)
    print("D3 ...", flush=True)
    d3(md)
    (OUT / "paperB_policy_shocks.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    pd.DataFrame(CSV).to_csv(OUT / "paperB_policy_shocks.csv", index=False)
    print("done", flush=True)


if __name__ == "__main__":
    main()
