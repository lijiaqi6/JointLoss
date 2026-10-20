r"""Can wives respond to the husband's job loss, or are they hit by the same shock? (2026-10-17)

Question (PI): are spouses similar in industry, occupation and location, so that when he loses his job her own labor
market is also weak (a demand-side constraint), as opposed to a preference not to respond or a search friction?
Answered by race (head's race; SRC + SEO; unweighted), with the PSID reason-for-job-end displacements of
19.FatherDisplacement.py.

Reads (read only): data/psid_person_year.pkl, psid_displacement.pkl (19), husband_shocks_fam.pkl (18; head and wife
industry codes / 16 sectors, state, 1976-2023 waves), husband_sector_shocks.pkl (18; CPS MORG sector shocks by sex),
state_shocks.pkl (8a; LAUS state unemployment rate, women's Bartik), the raw PSID family files (Dropbox/PSID/Family) and
output/wife_search.csv if it exists (21.WifeSearch.py, another agent; not required). Imports functions of 1, 9, 18
and 19 via importlib (no edits). Writes
  data/correlated_shocks_fam.pkl   cache of the extra family-file items below (wave x interview number)
  data/correlated_shocks_wife_disp.pkl   wife x calendar year job ends (main / strict / quit)
  output/correlated_shocks.csv     every estimate
  output/correlated_shocks.md      tables

VARIABLES (found by label in each wave's .do file; the list actually used is printed into the .md, section 0)
  Industry   1976-2023: 18.HusbandIndustryShocks.py (husband_shocks_fam.pkl: h_ind, w_ind -> 16 sectors of 8a).
             1968-1975: the PSID retrospective 1970-Census 3-digit codes 'INDUSTRY OF HEAD yy' / 'INDUSTRY OF WIFE yy'
             (_A / _B variables), mapped with 18's industry_sector (1970 codes), so the same-sector measure covers
             every year. Husband's sector for the displacement = latest wave in [event year - 3, event year] (18's
             h_sec: current main job, or the unemployed head's last job 1981-2001; job 1 = current or most recent
             main job from 2003). Wife's sector = latest wave in [event year - 6, event year] with a valid code
             (current main job when she works at the interview; 'job 1' from 2003), so wives not working at baseline
             who worked recently also get a sector.
  Occupation 1968-1980 'OCCUPATION OF HEAD / WIFE yy' (retrospective 1970 codes); 1981-2001 'MAIN OCC:3 DIG(H-E)',
             'OCCUPATION (WF-E)', 'MAIN OCC:3 DIG W-E', 'MAIN OCCUPATION: 3 DIGIT (HD-E / WF-E)' (1970 codes);
             2003-2015 'BC20 / DE20 MAIN OCC FOR JOB 1' (2000 codes); 2017-2023 the same (2010 codes, 4 digits).
             Harmonised into 8 major groups: professional & technical; managers (incl. business & financial
             operations); sales; clerical / office; craft, construction, extraction, installation & repair;
             operatives, laborers, production & transport; farm; service (incl. private household, protective,
             health support). Military and unknown codes are dropped. "Same 3-digit code" compares raw codes within
             a wave (both spouses are coded in the same scheme in a given wave).
  Employer   no PSID public item identifies the employer, and no item asks whether the spouses work for the same
             employer ('WRKG SAME EMP?' 1985 refers to the person's own previous position). Closest proxy: same
             3-digit industry code (and same state, trivially).
  Wife's status at the interview: 'EMPLOYMENT STATUS-WF' (1976), 'F2 EMP STATUS WIFE' / 'EMPLOYMENT STAT-WF'
             (1979-84), 'EMPLMT STATUS-WIFE' (1985-87), 'D1A EMPLOYMENT STATUS-WF' / 'D1A 1ST MENTION' (1988-97),
             'D1 1ST MENTION' (1999-2001), 'DE1 EMPLOYMENT STATUS-1ST MENTION' (2003-23); code 3 = looking for work,
             unemployed. Not asked of wives in 1968-75, 1977, 1978. Interview of wave w (spring) is put on calendar
             year w - 1 like the other outcomes, so it is measured a few months after the end of that year.
  Wife's own job ends (reason-for-job-end, same codes as the head's: 1 company folded / moved / out of business,
             3 laid off / fired, 4 quit ..., 5 = coronavirus layoff in 2021-23); main = 1 or 3 (or 5 in 2021-23),
             strict = 1, quit = 4. Branches mirror 19's head items:
               1984 E V10753 (V10748, V10752); U V10809 (V10811)       1985 E V12042 (V12044); U V12127 (V12129)
               1986 E V13256 (V13258); U V13328 (V13330)               1987 E V14350 (V14352); U V14420 (V14422)
               1988 E V15542 (V15541); U V15630 (V15622); U2 V15689 (V15688)
               1989 E V17060 (V17059); U V17162 (V17154); U2 V17221 (V17220)
               1990 E V18481 (V18480); U V18569 (V18561); U2 V18628 (V18627)
               1991 E V19781 (V19780); U V19869 (V19861); U2 V19928 (V19927)
               1992 E V21081 (V21080); U V21169 (V21161); U2 V21228 (V21227)
               1993 E V22904 (V22903); U V23008 (V22999); U2 V23070 (V23069)
               1994 E ER4054 (ER2655); U ER4065 (ER2820); U2 ER4070 (ER2900)
               1995 E ER6894 (ER5654); U ER6905 (ER5819); U2 ER6910 (ER5899)
               1996 E ER9145 (ER7750); U ER9156 (ER7915); U2 ER9161 (ER7995)
               1997 E ER12122 (ER10661); U ER12133 (ER10821); U2 ER12138 (ER10898)
               1999 E ER13822 (ER13821); U ER14010 (ER13990); U2 ER14075 (ER14074)
               2001 E ER17891 (ER17890); U ER18109 (ER18088); U2 ER18174 (ER18173)
               2003-2023 J1-J4 'DE51 WHY LAST JOB END / WHY JOB ENDED--JOB k' with 'DE6 ENDING YEAR--JOB k' (list
               in WIFE_J below). Before 1984 wives were not asked why a job ended (only 1976 'WTR LAID OFF(U)').
             Dating and de-duplication exactly as 19 (reported end year; reports > 2 years before the interview
             dropped). Coverage: calendar years 1982-2022 (1997 / 1999 partly, as for heads).
  Wife's job loss without a reason: positive annual hours in the previous observed year (<= 2 years back), zero
             hours this year (all years).
Shocks
  g_w_nat   CPS MORG growth (log points x 100) of national WOMEN's employment in the wife's sector, leaving out the
            family's state, in the displacement year (18's husband_sector_shocks.pkl, g_nat, female = 1); 1980-2019,
            1983 missing (1970 -> 1980 code break).  g_h_nat the same for MEN in the husband's sector.
  g_w_st    growth of women's employment in the wife's sector in the family's state (cells >= 20, winsorised).
  bartik_f  state predicted growth of women's employment (8a, shift-share with 1979-81 shares), displacement year.
  d_ur      change in the state unemployment rate (LAUS) from the year before to the displacement year; ur level.
Design: the stacked event study of 19 (stacks(): fathers first displaced in year ev vs clean controls, father x stack
and calendar-year x stack fixed effects, event time -3..+6, reference -2, clusters fam68). Moderators M are measured
at the event year for treated and controls alike; the moderated model adds event-time x M for all units and event-time
x displaced x M (M centred at the displaced fathers' mean and, if continuous, scaled to one s.d.), so the main effect
is the response at the average M and the interaction is the change in the response per s.d. (or for M = 1).
Nothing here identifies a causal effect of the moderators: they are not randomly assigned and correlate with other
family traits; read the interactions as heterogeneity consistent (or not) with a demand-side constraint.
"""
import importlib.util
import re
import sys
import warnings

import numpy as np
import pandas as pd
from scipy import stats

from common import DATA, OUT, HERE, stars

warnings.simplefilter("ignore", FutureWarning)
warnings.simplefilter("ignore", RuntimeWarning)


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


P19 = _load("p19", "19.FatherDisplacement.py")
P18 = _load("p18", "18.HusbandIndustryShocks.py")
psid1, psid9 = P19.psid1, P19.psid9
WAVES, FAM, layout, read = psid1.WAVES, psid1.FAM, psid1.layout, psid1.read
end_year = P19.end_year

# ---------------------------------------------------------------- wife's reason-for-job-end items
W = {1984: [("E", "V10753", ["V10748", "V10752"]), ("U", "V10809", ["V10811"])],
     1985: [("E", "V12042", ["V12044"]), ("U", "V12127", ["V12129"])],
     1986: [("E", "V13256", ["V13258"]), ("U", "V13328", ["V13330"])],
     1987: [("E", "V14350", ["V14352"]), ("U", "V14420", ["V14422"])]}
for w, e, ey, u, uy, u2, u2y in [
        (1988, "V15542", "V15541", "V15630", "V15622", "V15689", "V15688"),
        (1989, "V17060", "V17059", "V17162", "V17154", "V17221", "V17220"),
        (1990, "V18481", "V18480", "V18569", "V18561", "V18628", "V18627"),
        (1991, "V19781", "V19780", "V19869", "V19861", "V19928", "V19927"),
        (1992, "V21081", "V21080", "V21169", "V21161", "V21228", "V21227"),
        (1993, "V22904", "V22903", "V23008", "V22999", "V23070", "V23069"),
        (1994, "ER4054", "ER2655", "ER4065", "ER2820", "ER4070", "ER2900"),
        (1995, "ER6894", "ER5654", "ER6905", "ER5819", "ER6910", "ER5899"),
        (1996, "ER9145", "ER7750", "ER9156", "ER7915", "ER9161", "ER7995"),
        (1997, "ER12122", "ER10661", "ER12133", "ER10821", "ER12138", "ER10898"),
        (1999, "ER13822", "ER13821", "ER14010", "ER13990", "ER14075", "ER14074"),
        (2001, "ER17891", "ER17890", "ER18109", "ER18088", "ER18174", "ER18173")]:
    W[w] = [("E", e, [ey]), ("U", u, [uy]), ("U2", u2, [u2y])]
WIFE_J = {2003: "ER21434/ER21382 ER21466/ER21438 ER21498/ER21470 ER21530/ER21502",
          2005: "ER25431/ER25372 ER25463/ER25435 ER25495/ER25467 ER25527/ER25499",
          2007: "ER36436/ER36377 ER36468/ER36440 ER36500/ER36472 ER36532/ER36504",
          2009: "ER42463/ER42406 ER42493/ER42467 ER42523/ER42497 ER42553/ER42527",
          2011: "ER47781/ER47723 ER47811/ER47785 ER47841/ER47815 ER47871/ER47845",
          2013: "ER53487/ER53429 ER53517/ER53491 ER53547/ER53521 ER53577/ER53551",
          2015: "ER60502/ER60444 ER60532/ER60506 ER60562/ER60536 ER60592/ER60566",
          2017: "ER66517/ER66457 ER66547/ER66521 ER66577/ER66551 ER66607/ER66581",
          2019: "ER72519/ER72459 ER72549/ER72523 ER72579/ER72553 ER72609/ER72583",
          2021: "ER78561/ER78499 ER78591/ER78565 ER78621/ER78595 ER78651/ER78625",
          2023: "ER82553/ER82487 ER82583/ER82557 ER82613/ER82587 ER82643/ER82617"}
for w, pairs in WIFE_J.items():
    W[w] = [(f"J{k + 1}", p.split("/")[0], [p.split("/")[1]]) for k, p in enumerate(pairs.split())]

# ---------------------------------------------------------------- label patterns (occupation, retro industry, status)
PAT = {
    "h_occ": [r"^OCCUPATION\s+OF HEAD\s+\d\d$", r"MAIN OCC:\s*3\s*DI?GI?T?\s*\(?H-E", r"MAIN OCC:\s*3\s*DIG\s+H-E",
              r"MAIN OCCUPATION:\s*3 DIGIT \(HD-E\)", r"^BC20 MAIN OCC FOR JOB 1"],
    "w_occ": [r"^OCCUPATION\s+OF WIFE\s+\d\d$", r"^F[\d\-/]+ OCCUPATION\s*\(WF-E\)", r"MAIN OCC:\s*3\s*DI?GI?T?\s*\(?W-E",
              r"MAIN OCC:\s*3\s*DIG\s+W-E", r"MAIN OCCUPATION:\s*3 DIGIT \(WF-E\)", r"^DE20 MAIN OCC FOR JOB 1"],
    "h_ind_r": [r"^INDUSTRY\s+OF HEAD\s+\d\d$"],
    "w_ind_r": [r"^INDUSTRY\s+OF WIFE\s+\d\d$"],
    "w_stat": [r"EMPLOYMENT STATUS-WF", r"EMP STATUS WIFE", r"EMPLOYMENT STAT-WF", r"EMPLMT STATUS-WIFE",
               r"WF \d{4} EMPLOYMENT STATUS", r"^D1A 1ST MENTION", r"^D1 1ST MENTION",
               r"^DE1 EMPLOYMENT STATUS-1ST MENTION"],
}


def find(labs, pats):
    for p in pats:
        for v, l in labs:
            if re.search(p, l.strip()):
                return v, l.strip()
    return None


def extras():
    """wave x int: occupation codes, retrospective industry codes (1968-75), wife's status, wife's job-end items."""
    fn = DATA / "correlated_shocks_fam.pkl"
    if fn.exists():
        return pd.read_pickle(fn)
    out, found, rep = [], [], []
    for w in WAVES:
        folder = FAM / (f"fam{w}" if w < 1994 else f"fam{w}er")
        do = next(f for f in folder.glob("*.do") if "formats" not in f.name)
        pos, labs = P18.layout(do)                                   # 18's parser keeps the _A / _B variables
        labs = [(v, l) for v, l in labs if v in pos]
        idv = "V3" if w == 1968 else labs[1][0]
        sel = {k: find(labs, p) for k, p in PAT.items()}
        if w >= 1976:
            sel["h_ind_r"] = sel["w_ind_r"] = None                 # 18's pickle from 1976
        cols = sorted({idv, *[v[0] for v in sel.values() if v],
                       *[c for br in W.get(w, []) for c in [br[1], *br[2]]]})
        f = P18.read(do.with_suffix(".txt"), cols, pos)
        x = pd.DataFrame({"wave": w, "int": f[idv]})
        for k, v in sel.items():
            x[k] = f[v[0]] if v else np.nan
        out.append(x)
        found.append(dict(wave=w, **{k: (f"{v[0]} '{v[1]}'" if v else "") for k, v in sel.items()}))
        for br, why, yrs in W.get(w, []):
            code = f[why].where(f[why].between(1, 9))
            y = end_year(f[yrs[0]], w)
            for c in yrs[1:]:
                y = y.fillna(end_year(f[c], w))
            dated = y.notna()
            r = pd.DataFrame({"wave": w, "int": f[idv], "branch": br, "why": why, "code": code,
                              "year": y.fillna(w - 1), "dated": dated}).dropna(subset=["code"])
            rep.append(r)
        print(f"  extras {w}: " + "; ".join(f"{k}={v[0] if v else '-'}" for k, v in sel.items()), flush=True)
    res = dict(X=pd.concat(out, ignore_index=True), found=pd.DataFrame(found),
               R=pd.concat(rep, ignore_index=True))
    pd.to_pickle(res, fn)
    return res




# ---------------------------------------------------------------- codes -> groups
def occ_group(code, wave):
    """8 harmonised major occupation groups (see docstring); NaN for military / unknown."""
    c = pd.to_numeric(code, errors="coerce")
    w = pd.Series(np.asarray(wave), index=c.index)
    out = pd.Series(np.nan, index=c.index)

    def put(mask, lo, hi, g):
        out[mask & c.between(lo, hi)] = g
    m70, m00, m10 = w <= 2001, w.between(2003, 2015), w >= 2017
    for lo, hi, g in [(1, 195, 1), (201, 245, 2), (260, 285, 3), (301, 395, 4), (401, 575, 5), (601, 785, 6),
                      (801, 824, 7), (901, 984, 8)]:
        put(m70, lo, hi, g)
    for lo, hi, g in [(1, 43, 2), (50, 354, 1), (360, 465, 8), (470, 496, 3), (500, 593, 4), (600, 613, 7),
                      (620, 762, 5), (770, 975, 6)]:
        put(m00, lo, hi, g)
    for lo, hi, g in [(10, 430, 2), (500, 3540, 1), (3600, 4650, 8), (4700, 4965, 3), (5000, 5940, 4),
                      (6000, 6130, 7), (6200, 7630, 5), (7700, 9750, 6)]:
        put(m10, lo, hi, g)
    return out


def valid_code(code, wave):
    c = pd.to_numeric(code, errors="coerce")
    w = np.asarray(wave)
    return c.where(((w < 2017) & c.between(1, 998)) | ((w >= 2017) & c.between(1, 9998)))


OCC_NAMES = {1: "Professional & technical", 2: "Managers", 3: "Sales", 4: "Clerical / office",
             5: "Craft, construction, repair", 6: "Operatives, laborers, transport", 7: "Farm", 8: "Service"}


# ---------------------------------------------------------------- wife's displacements
def wife_displacement(py, R):
    wf = py[py["wife"]][["wave", "int", "pid"]].drop_duplicates(["wave", "int"])
    r = R.merge(wf, on=["wave", "int"], how="inner")
    r = r[r["year"].between(r["wave"] - 2, r["wave"])].copy()
    r["code"] = r["code"].astype(int)
    r["year"] = r["year"].astype(int)
    r["main"] = r["code"].isin([1, 3]) | ((r["code"] == 5) & (r["wave"] >= 2021))
    r["strict"] = r["code"] == 1
    r["quit"] = r["code"] == 4
    rows = []
    for k in ("main", "strict", "quit"):
        x = r[r[k]].sort_values(["pid", "year", "dated"], ascending=[True, True, False]).drop_duplicates(["pid", "year"])
        prev = set(zip(x["pid"], x["year"] + 1))
        drop = (~x["dated"]) & pd.Series([(p, y) in prev for p, y in zip(x["pid"], x["year"])], index=x.index)
        rows.append(x[~drop][["pid", "year"]].assign(**{k: 1}))
    d = rows[0]
    for x in rows[1:]:
        d = d.merge(x, on=["pid", "year"], how="outer")
    d = d.fillna(0)
    for k in ("main", "strict", "quit"):
        d[k] = d[k].astype(int)
    return d, r


# ---------------------------------------------------------------- couple-wave frame
def couples(py, X, F18, fam):
    hd = py[py["head"] & (py["female"] == 0) & py["hrace"].isin(["White", "Black"])][
        ["wave", "int", "pid", "fam68", "hrace"]].drop_duplicates(["wave", "int"])
    wf = py[py["wife"]][["wave", "int", "pid"]].drop_duplicates(["wave", "int"]).rename(columns={"pid": "w_pid"})
    k = py[py["child"] & py["age"].between(0, 17)].groupby(["wave", "int"])["age"].min().rename("youngest")
    C = hd.merge(wf, on=["wave", "int"]).merge(k.reset_index(), on=["wave", "int"], how="left")
    C = C.merge(X, on=["wave", "int"], how="left")
    C = C.merge(fam[["wave", "int", "hh", "wh"]], on=["wave", "int"], how="left")
    C = C.merge(F18[["wave", "int", "fips", "h_ind", "w_ind", "h_sec"]].rename(
        columns={"h_sec": "h_sec_u"}), on=["wave", "int"], how="left")
    early = C["wave"] < 1976
    C.loc[early, "h_ind"] = C.loc[early, "h_ind_r"]
    C.loc[early, "w_ind"] = C.loc[early, "w_ind_r"]
    for who in ("h", "w"):
        C[f"{who}_icode"] = valid_code(C[f"{who}_ind"], C["wave"])
        C[f"{who}_sec"] = P18.industry_sector(C[f"{who}_icode"].fillna(0), C["wave"])
        C[f"{who}_ocode"] = valid_code(C[f"{who}_occ"], C["wave"])
        C[f"{who}_ogrp"] = occ_group(C[f"{who}_ocode"], C["wave"])
    # husband's sector incl. 18's fallback to the unemployed head's last job (1976+)
    C["h_sec_any"] = C["h_sec_u"].where(C["wave"] >= 1976, C["h_sec"])
    return C


# ---------------------------------------------------------------- regression helpers
ROWS = []
big, md_table = P19.big, P19.md_table


def cell(b, se, p):
    return "n.a." if not (se > 0) else P19.cell(b, se, p)
BINS = {"pre3": [-3], "pre1": [-1], "e0": [0], "post13": [1, 2, 3], "post46": [4, 5, 6]}


def pv(b, se):
    return 2 * stats.norm.sf(abs(b / se)) if se > 0 else np.nan


def ols_cl(df, y, xs, fe=(), cluster="fam68"):
    """OLS with dummies for fe, clustered s.e.; returns {x: (b, se, p)}, n, clusters, mean_y."""
    import statsmodels.api as sm
    q = df[[y, *xs, *fe, cluster]].replace([np.inf, -np.inf], np.nan).dropna()
    Z = q[xs].astype(float)
    for f in fe:
        Z = Z.join(pd.get_dummies(q[f].astype(int), prefix=f, drop_first=True, dtype=float))
    Z.insert(0, "const", 1.0)
    r = sm.OLS(q[y].astype(float), Z).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(q[cluster])[0]})
    return {x: (r.params[x], r.bse[x], r.pvalues[x]) for x in xs}, dict(n=int(r.nobs), clusters=q[cluster].nunique(),
                                                                        mean=q[y].mean())


def binned(p, y, mods=(), extra=(), wife=True):
    """Stacked DiD with event-time bins (ref e = -2): displaced x bin, and for each moderator M (centred / scaled
    already): bin x M (all units) and displaced x bin x M. extra = list of (name, column) regressors interacted
    with bins for all units only (e.g. Black x bin). Returns dict term -> (b, se, p) for every bin, and info."""
    q = p.copy()
    if wife:
        q = q[q["w0"].notna()]
    xs = []
    for bn, es in BINS.items():
        ind = q["e"].isin(es).astype(float)
        q[f"d_{bn}"] = ind * q["treat"]
        xs.append(f"d_{bn}")
        for nm, col in extra:
            q[f"{nm}_{bn}"] = ind * q[col]
            xs.append(f"{nm}_{bn}")
        for mname in mods:
            q[f"m_{mname}_{bn}"] = ind * q[mname]
            q[f"dm_{mname}_{bn}"] = ind * q["treat"] * q[mname]
            xs += [f"m_{mname}_{bn}", f"dm_{mname}_{bn}"]
    q = q.dropna(subset=[y, *mods, *[c for _, c in extra]])
    b, V, info = P19.twfe(q, y, xs)
    out = {}
    for i, x in enumerate(xs):
        se = np.sqrt(V[i, i])
        out[x] = (b[i], se, pv(b[i], se))
    for stem in ["d"] + [f"dm_{m}" for m in mods] + [nm for nm, _ in extra]:
        i3, i1 = xs.index(f"{stem}_pre3"), xs.index(f"{stem}_pre1")
        l = np.zeros(len(xs))
        l[[i3, i1]] = 0.5
        bb, ss = l @ b, np.sqrt(l @ V @ l)
        out[f"{stem}_pre"] = (bb, ss, pv(bb, ss))
    info["mean_pre"] = q.loc[(q["treat"] == 1) & q["e"].isin([-2, -1]), y].mean()
    return out, info, (b, V, xs)


def record(table, sample, outcome, est, info, keep=None):
    for t, (b, se, p) in est.items():
        if keep and not any(t.startswith(k) for k in keep):
            continue
        ROWS.append(dict(table=table, sample=sample, outcome=outcome, term=t, coef=b, se=se, p=p, n=info.get("n"),
                         treated=info.get("units"), controls=info.get("controls"), clusters=info.get("clusters")))


def fmt_y(y, b, se, p):
    return (big if y in ("w_hrs",) else cell)(b, se, p)


def foot_rows(infos, ys):
    return [("Treated mean at e = -2, -1", [f"{infos[y]['mean_pre']:,.3f}" if infos[y]['mean_pre'] < 10 else
                                            f"{infos[y]['mean_pre']:,.0f}" for y in ys]),
            ("N (man-years, stacked)", [f"{infos[y]['n']:,}" for y in ys]),
            ("Displaced fathers / control father-stacks", [f"{infos[y]['units']:,} / {infos[y]['controls']:,}"
                                                         for y in ys]),
            ("Clusters (fam68)", [f"{infos[y]['clusters']:,}" for y in ys])]


# ---------------------------------------------------------------- main
def main():
    OUT.mkdir(exist_ok=True)
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    E = extras()
    X, found, R = E["X"], E["found"], E["R"]
    F18 = pd.read_pickle(DATA / "husband_shocks_fam.pkl")
    S = pd.read_pickle(DATA / "husband_sector_shocks.pkl")
    S["fips"] = S["fips"].astype(float)
    S["sec"] = S["sec"].astype(float)
    SS = pd.read_pickle(DATA / "state_shocks.pkl")
    SS["fips"] = SS["fips"].astype(float)
    fam = psid9.family()
    disp = pd.read_pickle(DATA / "psid_displacement.pkl")
    wd, wr = wife_displacement(py, R)
    wd.to_pickle(DATA / "correlated_shocks_wife_disp.pkl")
    C = couples(py, X, F18, fam)
    md = ["# Correlated shocks: can wives respond to the husband's job loss, or are they hit by the same shock?", "",
          "Built by `23.CorrelatedShocks.py` (2026-10-17; variable lists in its docstring and in section 0). "
          "Unweighted PSID SRC + SEO, married (wife / partner present) male heads, Black and White (head's race). "
          "S.e. clustered by 1968 family (fam68); *** p<0.01, ** p<0.05, * p<0.1. Displacement = the husband's "
          "job ended because the company folded / moved / went out of business (closure) or he was laid off / "
          "fired (19.FatherDisplacement.py). All comparisons are descriptive or difference-in-differences "
          "comparisons with the usual assumptions; the moderators (same sector, sector growth, state slack) are "
          "not randomly assigned, so their interactions describe heterogeneity, not causal effects of demand.", ""]

    # ================================================================ 0. variables
    md += ["## 0. Variables found by label", "",
           "| Wave | Head occupation | Wife occupation | Head industry (1968-75; 18 from 1976) | "
           "Wife industry (1968-75) | Wife's status |", "|---|---|---|---|---|---|"]
    for _, r in found.iterrows():
        md.append(f"| {r['wave']} | {r['h_occ']} | {r['w_occ']} | {r['h_ind_r']} | {r['w_ind_r']} | {r['w_stat']} |")
    cnt = wr.groupby("branch").size()
    md += ["", f"Wife's reason-for-job-end reports linked to a wife (1984-2023 waves): {len(wr):,}; by branch "
           + ", ".join(f"{k} {v:,}" for k, v in cnt.items()) + f". Main (closure / layoff) wife-years: "
           f"{int(wd['main'].sum()):,} (closures {int(wd['strict'].sum()):,}); quits {int(wd['quit'].sum()):,}. "
           f"Share dated by a reported end year: {wr['dated'].mean():.3f}. Employer: no PSID public item "
           "identifies the employer or asks whether the spouses share one, so 'same employer' cannot be measured; "
           "same 3-digit industry code is the closest proxy.", ""]

    # ================================================================ 1. similarity
    C["year"] = C["wave"] - 1
    C["black"] = (C["hrace"] == "Black").astype(int)
    both = (C["hh"] > 0) & (C["wh"] > 0)
    C["s_sec"] = (C["h_sec"] == C["w_sec"]).astype(float).where(both & C["h_sec"].notna() & C["w_sec"].notna())
    C["s_ind3"] = (C["h_icode"] == C["w_icode"]).astype(float).where(both & C["h_icode"].notna() & C["w_icode"].notna())
    C["s_occ"] = (C["h_ogrp"] == C["w_ogrp"]).astype(float).where(both & C["h_ogrp"].notna() & C["w_ogrp"].notna())
    C["s_occ3"] = (C["h_ocode"] == C["w_ocode"]).astype(float).where(both & C["h_ocode"].notna() & C["w_ocode"].notna())
    C["s_both"] = (C["s_sec"] * C["s_occ"]).where(C["s_sec"].notna() & C["s_occ"].notna())

    def random_match(g, a, b):
        """expected share with the same category under random matching within race x wave."""
        ok = g[a].notna() & g[b].notna()
        gg = g[ok]
        ph = gg.groupby(["hrace", "wave"])[a].value_counts(normalize=True).rename("ph")
        pw = gg.groupby(["hrace", "wave"])[b].value_counts(normalize=True).rename("pw")
        ph.index.names = pw.index.names = ["hrace", "wave", "k"]
        j = pd.concat([ph, pw], axis=1).fillna(0)
        e = (j["ph"] * j["pw"]).groupby(level=[0, 1]).sum().rename("exp")
        return gg[["hrace", "wave"]].merge(e.reset_index(), on=["hrace", "wave"], how="left")["exp"].mean()

    SIM = [("s_sec", "Same sector (16)"), ("s_ind3", "Same 3-digit industry"), ("s_occ", "Same occupation group (8)"),
           ("s_occ3", "Same 3-digit occupation"), ("s_both", "Same sector and occupation group")]
    samples = [("All married couples", C), ("Youngest child 0-5", C[C["youngest"] <= 5]),
               ("Any child 0-17", C[C["youngest"].notna()]),
               ("1968-79", C[C["year"] <= 1979]), ("1980-99", C[C["year"].between(1980, 1999)]),
               ("2000-22", C[C["year"] >= 2000])]
    panels = []
    for sname, g in samples:
        rows = []
        for race in ("Black", "White"):
            h = g[g["hrace"] == race]
            sec_ok = h[h["s_sec"].notna()]
            occ_ok = h[h["s_occ"].notna()]
            rs = random_match(sec_ok.assign(a=sec_ok["h_sec"], b=sec_ok["w_sec"]), "a", "b")
            ro = random_match(occ_ok.assign(a=occ_ok["h_ogrp"], b=occ_ok["w_ogrp"]), "a", "b")
            vals = [f"{h[c].mean():.3f}" for c, _ in SIM]
            rows.append((race, vals[:1] + [f"{rs:.3f}"] + vals[1:3] + [f"{ro:.3f}"] + vals[3:] +
                         [f"{int(h['s_sec'].notna().sum()):,}", f"{int(h['s_occ'].notna().sum()):,}"]))
            for c, _ in SIM:
                ROWS.append(dict(table="similarity", sample=f"{sname}: {race}", outcome=c, term="share",
                                 coef=h[c].mean(), n=int(h[c].notna().sum())))
            ROWS.append(dict(table="similarity", sample=f"{sname}: {race}", outcome="s_sec", term="random_match",
                             coef=rs))
            ROWS.append(dict(table="similarity", sample=f"{sname}: {race}", outcome="s_occ", term="random_match",
                             coef=ro))
        dif = []
        for c, _ in SIM:
            est, inf = ols_cl(g, c, ["black"], fe=["wave"])
            dif.append(cell(*est["black"]))
            ROWS.append(dict(table="similarity", sample=sname, outcome=c, term="black (wave FE)", coef=est["black"][0],
                             se=est["black"][1], p=est["black"][2], n=inf["n"], clusters=inf["clusters"]))
        rows.append(("Black - White (wave FE)", dif[:1] + [""] + dif[1:3] + [""] + dif[3:] + ["", ""]))
        panels.append((sname, rows))
    hdr = ["Same sector (16)", "Random-match benchmark", "Same 3-digit industry", "Same occupation group (8)",
           "Random-match benchmark", "Same 3-digit occupation", "Same sector and occupation group",
           "Couple-years (sector)", "Couple-years (occupation)"]
    md += ["## 1. How similar are spouses?", "",
           "Couple-years (wave = interview year) in which both spouses worked in the previous calendar year and "
           "report an industry / occupation for the current (or, from 2003, most recent) main job. Random-match "
           "benchmark = the share expected if husbands and wives were matched at random within race x wave "
           "(sum over categories of the husbands' share x the wives' share). Black - White rows: OLS of the "
           "indicator on Black with wave fixed effects, couple-years, clustered by fam68.", "",
           md_table(hdr, panels), ""]

    # sector composition by race
    comp = []
    work = C[both]
    for k in range(16):
        r = []
        for who in ("h", "w"):
            for race in ("Black", "White"):
                h = work[(work["hrace"] == race) & work[f"{who}_sec"].notna()]
                r.append(f"{(h[f'{who}_sec'] == k).mean():.3f}")
        comp.append((P18.SNAMES[k], r))
    md += ["### 1b. Sector composition of working husbands and wives (couple-years, both working)", "",
           md_table(["Husbands, Black", "Husbands, White", "Wives, Black", "Wives, White"], [("", comp)]), ""]

    # co-movement of the spouses' sector growth (national, leave own state out), 1980-2019
    g = work.copy()
    g["gy"] = g["wave"]
    Sm = S[S["female"] == 0][["fips", "sec", "year", "g_nat"]].rename(columns={"sec": "h_sec", "year": "gy",
                                                                               "g_nat": "g_h"})
    Sf = S[S["female"] == 1][["fips", "sec", "year", "g_nat"]].rename(columns={"sec": "w_sec", "year": "gy",
                                                                               "g_nat": "g_w"})
    g = g.merge(Sm, on=["fips", "h_sec", "gy"], how="left").merge(Sf, on=["fips", "w_sec", "gy"], how="left")
    cm = []
    for race in ("Black", "White", "All"):
        h = g if race == "All" else g[g["hrace"] == race]
        h = h.dropna(subset=["g_h", "g_w"])
        est, inf = ols_cl(h, "g_w", ["g_h"], fe=["gy"])
        est2, inf2 = ols_cl(h[h["s_sec"] == 0], "g_w", ["g_h"], fe=["gy"])
        rho = h[["g_h", "g_w"]].corr().iloc[0, 1]
        cm.append((race, [f"{rho:.3f}", cell(*est["g_h"]), cell(*est2["g_h"]), f"{inf['n']:,}", f"{inf2['n']:,}"]))
        for nm, e_, i_ in (("all couples", est, inf), ("different sectors", est2, inf2)):
            ROWS.append(dict(table="sector_comovement", sample=f"{race}: {nm}", outcome="g_w (women, her sector)",
                             term="g_h (men, his sector), year FE", coef=e_["g_h"][0], se=e_["g_h"][1],
                             p=e_["g_h"][2], n=i_["n"], clusters=i_["clusters"]))
    md += ["### 1c. Do the spouses' sectors move together? (CPS MORG, 1980-2019)", "",
           "Growth (log points x 100) of national employment, leaving the family's state out, of women in the "
           "wife's sector (g_w) and of men in the husband's sector (g_h), in the interview year; couple-years with "
           "both spouses working. Slope: OLS of g_w on g_h with year fixed effects (so the common business cycle "
           "is removed), clustered by fam68.", "",
           md_table(["Raw correlation", "Slope, all couples (year FE)", "Slope, spouses in different sectors",
                     "N (all)", "N (different sectors)"], [("", cm)]), ""]
    print("similarity done", flush=True)

    # ================================================================ stacked panel (19) + extras
    m = P19.men_panel(py, fam)
    m = m.merge(F18[["wave", "int", "fips"]], on=["wave", "int"], how="left")
    m = m.merge(X[["wave", "int", "w_stat"]], on=["wave", "int"], how="left")
    m = m.drop_duplicates(["pid", "year"])
    d = disp
    P = P19.stacks(m, d, "main")
    P = P.merge(m[["pid", "year", "w_stat", "fips"]], on=["pid", "year"], how="left")
    same = P["w_pid"] == P["w0"]
    st = pd.to_numeric(P["w_stat"], errors="coerce")
    P["w_look"] = (st == 3).astype(float).where(same & P["w0"].notna() & st.between(1, 8))
    # wife's own displacement (baseline wife), since the previous observed row
    P = P.sort_values(["unit", "year"]).reset_index(drop=True)
    wdi = wd.set_index(["pid", "year"])
    w0 = P["w0"].fillna(-1).astype(np.int64)
    for k in ("main", "strict", "quit"):
        a = P19.lookup(wdi[k], w0, P["year"])
        b_ = P19.lookup(wdi[k], w0, P["year"] - 1)
        gap = (P["year"] - P.groupby("unit")["year"].shift(1)) == 2
        v = np.where(gap, np.fmax(np.nan_to_num(a), np.nan_to_num(b_)), np.nan_to_num(a))
        P[f"w_disp_{k}"] = pd.Series(v, index=P.index).where(same & P["w0"].notna())
    prev = P.groupby("unit")["w_hrs"].shift(1)
    P["w_loss"] = ((P["w_hrs"] == 0) & (prev > 0)).astype(float).where(prev.gt(0) & P["w_hrs"].notna())

    # ---- unit-level (father x stack) baseline characteristics and moderators
    U = P[["unit", "pid", "ev", "treat", "hrace", "young0", "w0", "wh0", "fam68"]].drop_duplicates("unit").copy()
    base = pd.concat([m.assign(ev=m["year"] + 1, pri=0), m.assign(ev=m["year"] + 2, pri=1)])
    base = base.sort_values(["pid", "ev", "pri"]).drop_duplicates(["pid", "ev"])[["pid", "ev", "fips", "wave"]]
    U = U.merge(base.rename(columns={"wave": "wave0"}), on=["pid", "ev"], how="left")
    # husband's sector: latest wave in [ev-3, ev]; wife's: latest in [ev-6, ev]
    hs = C[["pid", "wave", "h_sec_any"]].dropna().rename(columns={"h_sec_any": "sec"})
    ws = C[["w_pid", "wave", "w_sec"]].dropna().rename(columns={"w_pid": "pid", "w_sec": "sec"})
    ws = ws.drop_duplicates(["pid", "wave"])

    def latest(keys, src, lo):
        x = keys.merge(src, on="pid")
        x = x[(x["wave"] >= x["ev"] - lo) & (x["wave"] <= x["ev"])].sort_values(["unit", "wave"])
        return x.groupby("unit")["sec"].last()
    U["h_sec"] = U["unit"].map(latest(U[["unit", "pid", "ev"]], hs.drop_duplicates(["pid", "wave"]), 3))
    kw = U[U["w0"].notna()][["unit", "w0", "ev"]].rename(columns={"w0": "pid"})
    kw["pid"] = kw["pid"].astype(np.int64)
    U["w_sec"] = U["unit"].map(latest(kw, ws, 6))
    U["same_sec"] = (U["h_sec"] == U["w_sec"]).astype(float).where(U["h_sec"].notna() & U["w_sec"].notna())
    U["black"] = (U["hrace"] == "Black").astype(int)
    U["wemp0"] = (U["wh0"] > 0).astype(float).where(U["w0"].notna() & U["wh0"].notna())
    # closure vs layoff (first main displacement)
    dm = d[d["main"] == 1][["pid", "year", "strict"]].rename(columns={"year": "ev"})
    U = U.merge(dm, on=["pid", "ev"], how="left")
    U["closure"] = (U["strict"] == 1).astype(int) * U["treat"]
    U["layoff"] = (U["strict"] != 1).astype(int) * U["treat"]
    # sector shocks (wife: women in her sector; husband: men in his), state x sector, state slack, women's Bartik
    def shock(col_sec, female, cols, ren):
        s = S[S["female"] == female][["fips", "sec", "year"] + cols].rename(
            columns={"sec": col_sec, "year": "ev", **ren})
        return s
    U = U.merge(shock("w_sec", 1, ["g_nat", "g_st"], {"g_nat": "g_w_nat", "g_st": "g_w_st"}),
                on=["fips", "w_sec", "ev"], how="left")
    U = U.merge(shock("h_sec", 0, ["g_nat"], {"g_nat": "g_h_nat"}), on=["fips", "h_sec", "ev"], how="left")
    ur = SS[["fips", "year", "ur", "bartik_f"]].rename(columns={"year": "ev"})
    U = U.merge(ur, on=["fips", "ev"], how="left")
    urp = SS[["fips", "year", "ur"]].assign(ev=SS["year"] + 1).drop(columns="year").rename(columns={"ur": "ur_prev"})
    U = U.merge(urp, on=["fips", "ev"], how="left")
    U["d_ur"] = U["ur"] - U["ur_prev"]
    # joint shock: wife employed at baseline loses her job around his displacement
    Pw = P[P["w0"].notna()]
    zero = Pw[Pw["e"].isin([0, 1])].groupby("unit")["w_hrs"].apply(lambda s: float((s == 0).any()) if s.notna().any()
                                                                    else np.nan)
    zero2 = Pw[Pw["e"] == 2].groupby("unit")["w_hrs"].apply(lambda s: float((s == 0).any()) if s.notna().any()
                                                             else np.nan)
    U["J_zero"] = U["unit"].map(zero).fillna(U["unit"].map(zero2))
    wmain = set(zip(wd.loc[wd["main"] == 1, "pid"], wd.loc[wd["main"] == 1, "year"]))
    wstr = set(zip(wd.loc[wd["strict"] == 1, "pid"], wd.loc[wd["strict"] == 1, "year"]))
    wq = set(zip(wd.loc[wd["quit"] == 1, "pid"], wd.loc[wd["quit"] == 1, "year"]))
    w0u = U["w0"].fillna(-1).astype(np.int64)
    for nm, sset, lags in (("J_disp", wmain, (-1, 0, 1)), ("J_disp01", wmain, (0, 1)), ("J_closure", wstr, (-1, 0, 1)),
                           ("J_quit", wq, (-1, 0, 1)), ("J_disp_pl", wmain, (-4, -3, -2))):
        U[nm] = [float(any((p_, e_ + l) in sset for l in lags)) for p_, e_ in zip(w0u, U["ev"])]
    # observed requirement: the baseline wife is in the family at a row e in {-1, 0} and at a row e in {+1, +2};
    # otherwise reports could not exist (controls who attrit would be coded 0, while displaced fathers are observed
    # after the event by construction, since the displacement is reported at a later interview)
    seen = Pw[Pw["w_pid"] == Pw["w0"]]
    pre_ok = set(seen.loc[seen["e"].isin([-1, 0]), "unit"])
    post_ok = set(seen.loc[seen["e"].isin([1, 2]), "unit"])
    U["observed"] = [float(u in pre_ok and u in post_ok) for u in U["unit"]]
    cover = U["ev"].between(1984, 2021)
    for nm in ("J_disp", "J_disp01", "J_closure", "J_quit"):
        U[nm] = U[nm].where(cover & (U["wemp0"] == 1) & (U["observed"] == 1))
    U["J_zero"] = U["J_zero"].where((U["wemp0"] == 1) & (U["observed"] == 1))
    seen_pl = set(seen.loc[seen["e"].isin([-3, -2]), "unit"])
    U["J_disp_pl"] = U["J_disp_pl"].where(U["ev"].between(1986, 2021) & (U["wemp0"] == 1) & (U["observed"] == 1) &
                                          U["unit"].isin(seen_pl))
    U["J"] = np.fmax(U["J_zero"].fillna(0), U["J_disp"].fillna(0)).where(U["J_zero"].notna() | U["J_disp"].notna())
    U.to_pickle(DATA / "correlated_shocks_units.pkl")
    print("units", len(U), int(U["treat"].sum()), flush=True)

    # ================================================================ 1d. exposure at the displacement
    ex_rows = []
    EXM = [("same_sec", "Wife in husband's sector"), ("g_w_nat", "Women's growth, wife's sector (national)"),
           ("g_h_nat", "Men's growth, husband's sector (national)"), ("g_w_st", "Women's growth, wife's sector x state"),
           ("bartik_f", "State women's Bartik"), ("d_ur", "Change in state unemployment rate"),
           ("ur", "State unemployment rate")]
    Uw = U[U["w0"].notna()]
    for race in ("Black", "White"):
        h = Uw[Uw["hrace"] == race]
        r = []
        for c, _ in EXM:
            est, inf = ols_cl(h, c, ["treat"], fe=["ev"])
            mt = h.loc[h["treat"] == 1, c].mean()
            r.append(f"{mt:.3f} / " + cell(*est["treat"]))
            ROWS.append(dict(table="exposure", sample=race, outcome=c, term="treat (ev FE)", coef=est["treat"][0],
                             se=est["treat"][1], p=est["treat"][2], n=inf["n"], clusters=inf["clusters"],
                             mean_treated=mt))
        ex_rows.append((race, r))
    r = []
    for c, _ in EXM:
        h = Uw[Uw["treat"] == 1]
        est, inf = ols_cl(h, c, ["black"], fe=["ev"])
        r.append(cell(*est["black"]))
        ROWS.append(dict(table="exposure", sample="displaced, Black - White", outcome=c, term="black (ev FE)",
                         coef=est["black"][0], se=est["black"][1], p=est["black"][2], n=inf["n"]))
    ex_rows.append(("Displaced: Black - White (event-year FE)", r))
    md += ["### 1d. The wife's labor market at the husband's displacement", "",
           "Father x stack units of the stacked design (section 3), wife present at baseline. Cell: mean among "
           "displaced fathers' families / displaced - control difference (OLS with event-year fixed effects, "
           "clustered by fam68). Wife's sector = latest known in the 6 years up to the event year; growth rates in "
           "log points x 100 in the event year (1980-2019); state unemployment rate (LAUS) in percent.", "",
           md_table([lab for _, lab in EXM], [("", ex_rows)]), ""]

    # ================================================================ 2. joint shocks
    JY = [("J_disp", "Wife displaced (closure / layoff), ev-1..ev+1"), ("J_disp01", "Wife displaced, ev..ev+1"),
          ("J_closure", "Wife's employer closed, ev-1..ev+1"), ("J_zero", "Wife's hours fall to 0 (ev, ev+1)"),
          ("J_quit", "Wife quits, ev-1..ev+1 (comparison)"),
          ("J_disp_pl", "Placebo: wife displaced, ev-4..ev-2")]
    W1 = U[U["wemp0"] == 1].copy()
    W1["t_same"] = W1["treat"] * W1["same_sec"]
    W1["t_black"] = W1["treat"] * W1["black"]
    specs = [("A. Displaced vs controls", ["treat"], None),
             ("B. By sector match (wives with a known sector)", ["treat", "t_same", "same_sec"], "same_sec"),
             ("C. Closure vs layoff", ["closure", "layoff"], None)]
    panels = []
    for race in ("Black", "White", "All"):
        h = W1 if race == "All" else W1[W1["hrace"] == race]
        for sname, xs, need in specs:
            xs2 = xs + (["t_black", "black"] if race == "All" and sname.startswith("A") else [])
            rows, infos = {}, {}
            for y, _ in JY:
                hh_ = h.dropna(subset=[need]) if need else h
                est, inf = ols_cl(hh_, y, xs2, fe=["ev"])
                infos[y] = inf
                rows[y] = est
                ctrl_mean = hh_.loc[hh_["treat"] == 0, y].mean()
                inf["ctrl"] = ctrl_mean
                for x, (b, se, p) in est.items():
                    ROWS.append(dict(table="joint_shock", sample=f"{race}: {sname}", outcome=y, term=x, coef=b, se=se,
                                     p=p, n=inf["n"], clusters=inf["clusters"], control_mean=ctrl_mean))
            lab = {"treat": "Husband displaced", "t_same": "Displaced x wife in his sector", "same_sec":
                   "Wife in his sector", "closure": "Husband displaced: closure", "layoff": "Husband displaced: layoff",
                   "t_black": "Displaced x Black", "black": "Black"}
            rr = [(lab[x], [cell(*rows[y][x]) for y, _ in JY]) for x in xs2]
            rr.append(("Control mean", [f"{infos[y]['ctrl']:.3f}" for y, _ in JY]))
            rr.append(("N (father-stacks) / clusters", [f"{infos[y]['n']:,} / {infos[y]['clusters']:,}" for y, _ in JY]))
            panels.append((f"{race} - {sname}", rr))
    md += ["## 2. Joint shocks: does the wife lose her job too?", "",
           "Father x stack units (fathers first displaced in the event year ev vs clean controls, as in 19), wife "
           "present and employed (positive hours) at baseline, and observed in the family both at e = -1 or 0 "
           "and at e = +1 or +2 (so that her reports can exist for displaced and control families alike). Outcomes are 0/1 at the unit level; the wife's own "
           "displacement uses her reason-for-job-end reports (events dated 1983-2022, so ev 1984-2021); the "
           "zero-hours outcome uses her annual hours (all years). OLS with event-year fixed effects, clustered by "
           "fam68. The coefficient is the excess probability relative to wives of comparable non-displaced men in "
           "the same calendar years; it mixes a contemporaneous joint shock with any permanent difference in the "
           "wives' job stability (assortative risk). The placebo column (her displacement 2-4 years BEFORE his, event "
           "years 1986-2021, wife observed at e = -3 or -2) measures the permanent part; section 2b removes it with "
           "family fixed effects.", "",
           md_table([lab for _, lab in JY], panels, [("Fixed effects", ["event year"] * len(JY))]), ""]
    print("joint shocks done", flush=True)

    # event study of the wife's own job loss
    ES_W = [("w_disp_main", "Wife displaced (closure / layoff)"), ("w_disp_strict", "Wife's employer closed"),
            ("w_loss", "Wife's hours fall to 0"), ("w_disp_quit", "Wife quits")]
    Pw1 = P.merge(U[["unit", "wemp0"]], on="unit", how="left")
    Pw1 = Pw1[Pw1["wemp0"] == 1]
    res_es = {}
    for race in ("All", "Black", "White"):
        q = Pw1 if race == "All" else Pw1[Pw1["hrace"] == race]
        res_es[race] = {}
        for y, _ in ES_W:
            qq = q[q["ev"].between(1985, 2019)] if y.startswith("w_disp") else q
            o = P19.event_study(qq, y)
            res_es[race][y] = o
            for r in o:
                ROWS.append(dict(table="wife_job_loss_event_study", sample=race, outcome=y, term=r["term"],
                                 coef=r["coef"], se=r["se"], p=r["p"], n=r["n"], treated=r["units"],
                                 controls=r["controls"], clusters=r["clusters"]))
    terms = [f"e={e:+d}" for e in P19.ES_E] + ["mean +1..+3"]
    panels = []
    for race in ("All", "Black", "White"):
        rows = [(t, [cell(*(lambda r: (r["coef"], r["se"], r["p"]))(next(r for r in res_es[race][y] if r["term"] == t)))
                     for y, _ in ES_W]) for t in terms]
        o0 = {y: res_es[race][y][0] for y, _ in ES_W}
        rows += [("Treated mean at e = -2, -1", [f"{o0[y]['pre_mean']:.3f}" for y, _ in ES_W]),
                 ("N (man-years, stacked)", [f"{o0[y]['n']:,}" for y, _ in ES_W]),
                 ("Displaced fathers / control father-stacks", [f"{o0[y]['units']:,} / {o0[y]['controls']:,}"
                                                              for y, _ in ES_W]),
                 ("Clusters (fam68)", [f"{o0[y]['clusters']:,}" for y, _ in ES_W])]
        panels.append((f"{race} fathers, wife employed at baseline", rows))
    md += ["### 2b. Event study of the wife's own job loss around the husband's displacement", "",
           "Stacked event study as in 19 (father x stack and calendar-year x stack fixed effects, reference e = -2), "
           "wife employed at baseline; outcome = the baseline wife reports a job end of that kind since the previous "
           "observed year (event years 1985-2019 for the reason-based outcomes), or her annual hours fall to zero "
           "from positive hours in the previous observed year (at risk only if she worked then).", "",
           md_table([lab for _, lab in ES_W], panels,
                    [("Fixed effects", ["father x stack, calendar year x stack"] * len(ES_W))]), ""]
    print("wife event study done", flush=True)

    # 2c. year-by-year excess rate of the wife's own displacement (no family fixed effect, so no reference year)
    smain = set(zip(wd.loc[wd["main"] == 1, "pid"], wd.loc[wd["main"] == 1, "year"]))
    K = list(range(-5, 4))
    Wk = U[(U["wemp0"] == 1) & (U["observed"] == 1) & U["ev"].between(1987, 2019)].copy()
    w0k = Wk["w0"].astype(np.int64)
    for k in K:
        Wk[f"k{k}"] = [float((p_, e_ + k) in smain) for p_, e_ in zip(w0k, Wk["ev"])]
    panels = []
    for race in ("Black", "White"):
        h = Wk[Wk["hrace"] == race]
        rows_t, rows_c, rows_d = [], [], []
        for k in K:
            est, inf = ols_cl(h, f"k{k}", ["treat"], fe=["ev"])
            rows_t.append(f"{h.loc[h['treat'] == 1, f'k{k}'].mean():.3f}")
            rows_c.append(f"{h.loc[h['treat'] == 0, f'k{k}'].mean():.3f}")
            rows_d.append(cell(*est["treat"]))
            ROWS.append(dict(table="wife_displacement_by_year", sample=race, outcome=f"wife displaced in ev{k:+d}",
                             term="treat (ev FE)", coef=est["treat"][0], se=est["treat"][1], p=est["treat"][2],
                             n=inf["n"], clusters=inf["clusters"]))
        panels.append((race, [("Displaced families: rate", rows_t), ("Controls: rate", rows_c),
                              ("Excess (OLS, event-year FE)", rows_d),
                              ("N father-stacks (displaced)", [f"{len(h):,} ({int(h['treat'].sum()):,})"] * len(K))]))
    md += ["### 2c. The wife's own displacement year by year (no reference year)", "",
           "Same units as section 2 (wife employed at baseline, observed before and after), event years 1987-2019 so "
           "that her reports cover ev-5..ev+3. Share of wives with a closure / layoff dated to calendar year ev + k. "
           "The wives of displaced men already have twice the control rate at k = -2 and -1 (dating error between "
           "the two spouses' reports and / or local shocks that start before his job ends), so the event study in "
           "2b, whose reference year is k = -2, understates the joint shock; the window measure of section 2 "
           "(k = -1..+1) does not have this problem.", "",
           md_table([f"k={k:+d}" for k in K], panels), ""]

    # ================================================================ 3. demand-side moderation
    P = P.merge(U[["unit", "same_sec", "g_w_nat", "g_h_nat", "g_w_st", "bartik_f", "d_ur", "wemp0", "J",
                   "black"]], on="unit", how="left")
    ws_file = OUT / "wife_search.csv"
    YS = [("w_emp", "Wife employed"), ("w_hrs", "Wife's hours"), ("w_look", "Wife unemployed, looking (interview)")]
    MODS = [("same_sec", "(a) Wife worked in the husband's sector", False, None),
            ("g_w_nat", "(b) Women's employment growth in the wife's sector (national, leave-one-state-out), "
                        "holding the husband's sector growth fixed", True, "g_h_nat"),
            ("g_w_st", "(b') Women's employment growth in the wife's sector in the state", True, None),
            ("bartik_f", "(c) Predicted growth of women's employment in the state (Bartik)", True, None),
            ("d_ur", "(c') Change in the state unemployment rate in the displacement year", True, None)]
    SAMP = [("Black", lambda q: q[q["hrace"] == "Black"]), ("White", lambda q: q[q["hrace"] == "White"]),
            ("Black, wife not employed at baseline", lambda q: q[(q["hrace"] == "Black") & (q["wemp0"] == 0)]),
            ("White, wife not employed at baseline", lambda q: q[(q["hrace"] == "White") & (q["wemp0"] == 0)]),
            ("Black, wife employed at baseline", lambda q: q[(q["hrace"] == "Black") & (q["wemp0"] == 1)]),
            ("White, wife employed at baseline", lambda q: q[(q["hrace"] == "White") & (q["wemp0"] == 1)])]
    md += ["## 3. Demand-side test: is the wife's response weaker when her own market is also hit?", "",
           "Stacked difference-in-differences of 19 with event-time bins (e = -3, -1, 0, +1..+3, +4..+6; reference "
           "e = -2), wife present at baseline, outcomes for the baseline wife while she is in the family unit. For "
           "a moderator M measured in the event year: bin x M for all units and displaced x bin x M; M is centred "
           "at the displaced families' mean and, if continuous, divided by its s.d. among them. Rows: 'Displaced' = "
           "response at e = +1..+3 at the average M; 'Displaced x M' = change in that response per s.d. of M (for "
           "(a): wife in his sector vs not); 'pre' rows = mean of the e = -3 and e = -1 coefficients (a pre-trend "
           "check). A demand-side constraint predicts a smaller response when her sector shrinks or local "
           "unemployment rises: Displaced x M > 0 for (b), (b'), (c) and < 0 for (c'), and < 0 for (a) if the same "
           "sector is hit. 'Wife unemployed, looking' = status 3 at the next interview (wives not asked 1968-75, "
           "1977, 1978)."
           + (" output/wife_search.csv (21.WifeSearch.py) was found and is summarised in section 3f." if
              ws_file.exists() else " output/wife_search.csv (21.WifeSearch.py) did not exist when this ran."),
           ""]
    MOD_RES = {}
    for mname, mlab, cont, ctrl in MODS:
        panels = []
        for sname, f in SAMP:
            q = f(P)
            q = q[q["w0"].notna() & q[mname].notna()]
            if ctrl:
                q = q[q[ctrl].notna()]
            tr = q[q["treat"] == 1].drop_duplicates("unit")
            q = q.copy()
            mods = [mname] + ([ctrl] if ctrl else [])
            for c in mods:
                mu = tr[c].mean()
                sd = tr[c].std() if (cont or c == ctrl) else 1.0
                q[c] = (q[c] - mu) / sd
            ests, infos = {}, {}
            for y, _ in YS:
                try:
                    est, inf, _ = binned(q, y, mods=mods)
                except Exception as exc:
                    print("skip", mname, sname, y, exc, flush=True)
                    continue
                ests[y], infos[y] = est, inf
                record(f"moderation_{mname}", sname, y, est, inf, keep=["d_", f"dm_{mname}", f"dm_{ctrl}" if ctrl
                                                                         else "zz"])
            MOD_RES[(mname, sname)] = (ests, infos)
            ys = [y for y, _ in YS if y in ests]
            rows = [("Displaced, e=+1..+3", [fmt_y(y, *ests[y]["d_post13"]) for y in ys]),
                    ("Displaced, pre", [fmt_y(y, *ests[y]["d_pre"]) for y in ys]),
                    (f"Displaced x M, e=+1..+3", [fmt_y(y, *ests[y][f"dm_{mname}_post13"]) for y in ys]),
                    (f"Displaced x M, pre", [fmt_y(y, *ests[y][f"dm_{mname}_pre"]) for y in ys])]
            if ctrl:
                rows += [("Displaced x husband's sector growth, e=+1..+3",
                          [fmt_y(y, *ests[y][f"dm_{ctrl}_post13"]) for y in ys])]
            sdv = (tr[mname].std() if cont else np.nan)
            rows += foot_rows(infos, ys)
            rows.append(("Displaced: mean of M / s.d.", [f"{tr[mname].mean():.3f} / {sdv:.3f}" if cont else
                                                         f"{tr[mname].mean():.3f}" for _ in ys]))
            panels.append((sname, rows))
        md += [f"### 3{'abcde'[[x[0] for x in MODS].index(mname)]}. {mlab}", "",
               md_table([lab for _, lab in YS], panels,
                        [("Fixed effects", ["father x stack, calendar year x stack"] * len(YS))]), ""]
        print("moderation", mname, flush=True)
    if ws_file.exists():
        try:
            wsr = pd.read_csv(ws_file)
            wsr["subsample"] = wsr["subsample"].fillna("")
            sel = wsr[(wsr["dataset"] == "PSID") & (wsr["table"] == "event_study") & (wsr["design"] == "main") &
                      (wsr["term"] == "mean +1..+3")]
            WSY = [("w_emp_s", "Employed (interview)"), ("w_look", "Looking / unemployed (interview)"),
                   ("w_lfp", "In labor force (interview)"), ("w_wu_any", "Any unemployment in year"),
                   ("w_wu_wks", "Weeks unemployed in year"), ("w_find", "Job finding (not employed before)"),
                   ("w_u2e", "Employed after looking")]
            panels = []
            for race in ("Black", "White"):
                for sub, slab in (("", "all wives"), ("wemp", "wife employed at baseline"),
                                  ("wnot", "wife not employed at baseline")):
                    cells = []
                    for y, _ in WSY:
                        r = sel[(sel["sample"] == race) & (sel["subsample"] == sub) & (sel["outcome"] == y)]
                        cells.append(cell(r["coef"].iloc[0], r["se"].iloc[0], r["p"].iloc[0]) +
                                     f" [{int(r['treated'].iloc[0])}]" if len(r) else "")
                    panels.append((f"{race}, {slab}", [("Displaced, mean +1..+3 [displaced fathers]", cells)]))
            md += ["### 3f. Wife's search (read from output/wife_search.csv, 21.WifeSearch.py; not re-estimated)",
                   "", "Same stacked design; status outcomes at the spring interview (reference = interview a year "
                   "before), calendar-year unemployment as in 19. Copied from that file for comparison.", "",
                   md_table([lab for _, lab in WSY], panels), ""]
        except Exception as exc:
            md += [f"(wife_search.csv could not be read: {exc})", ""]

    # ================================================================ 4. decomposition
    md += ["## 4. Decomposition of the Black-White difference in the wife's response", ""]
    DEC_Y = [("w_hrs", "Wife's hours"), ("w_emp", "Wife employed")]
    dec_panels = []
    for y, ylab in DEC_Y:
        # (i) joint-shock channel, by race: wives employed at baseline (J defined); r = (P1-P0) cost + conditional
        out = {}
        for race in ("Black", "White"):
            q = P[(P["hrace"] == race) & (P["wemp0"] == 1) & P["J"].notna()].copy()
            est0, inf0, _ = binned(q, y)
            est, inf, (b, V, xs) = binned(q, y, mods=["J"])
            u = q.drop_duplicates("unit")
            P1, P0 = u.loc[u["treat"] == 1, "J"].mean(), u.loc[u["treat"] == 0, "J"].mean()
            cost = est["m_J_post13"]
            g0, gJ = est["d_post13"], est["dm_J_post13"]
            ij, ig, igJ = xs.index("m_J_post13"), xs.index("d_post13"), xs.index("dm_J_post13")
            out[race] = dict(r=est0["d_post13"], P1=P1, P0=P0, cost=cost, g0=g0, gJ=gJ, V=V, ij=ij, ig=ig, igJ=igJ,
                             b=b, n=inf["n"], units=inf["units"], ch=(P1 - P0) * cost[0],
                             ch_se=abs(P1 - P0) * cost[1])
            record("decomp_joint", race, y, {"r (no J terms)": est0["d_post13"], "cost of J (controls)": cost,
                                             "response J=0": g0, "extra response J=1": gJ}, inf)
        B_, W_ = out["Black"], out["White"]
        gap = W_["r"][0] - B_["r"][0]
        gap_se = np.sqrt(W_["r"][1] ** 2 + B_["r"][1] ** 2)
        dP = (B_["P1"] - B_["P0"]) - (W_["P1"] - W_["P0"])
        expl_B = dP * B_["cost"][0]              # Black minus counterfactual (White excess probability), Black cost
        expl_W = dP * W_["cost"][0]
        rows = [("Response, Black (e=+1..+3)", [fmt_y(y, *B_["r"])]),
                ("Response, White (e=+1..+3)", [fmt_y(y, *W_["r"])]),
                ("Gap, White - Black", [fmt_y(y, gap, gap_se, pv(gap, gap_se))]),
                ("P(joint job loss): displaced / controls, Black", [f"{B_['P1']:.3f} / {B_['P0']:.3f}"]),
                ("P(joint job loss): displaced / controls, White", [f"{W_['P1']:.3f} / {W_['P0']:.3f}"]),
                ("Cost of a job loss for the wife's outcome (controls), Black", [fmt_y(y, *B_["cost"])]),
                ("Cost of a job loss for the wife's outcome (controls), White", [fmt_y(y, *W_["cost"])]),
                ("Joint-shock channel (excess P x cost), Black", [fmt_y(y, B_["ch"], B_["ch_se"],
                                                                       pv(B_["ch"], B_["ch_se"]))]),
                ("Joint-shock channel (excess P x cost), White", [fmt_y(y, W_["ch"], W_["ch_se"],
                                                                       pv(W_["ch"], W_["ch_se"]))]),
                ("Part of the White - Black gap due to the Black - White difference in excess P (Black cost / "
                 "White cost)",
                 [f"{-expl_B:,.3f} / {-expl_W:,.3f}" + (f" (share of gap {-expl_B / gap:.2f} / {-expl_W / gap:.2f})"
                                                       if abs(gap) > 1e-9 else "")]),
                ("Response with no joint loss (J=0), Black / White", [fmt_y(y, *B_["g0"]) + " / " +
                                                                      fmt_y(y, *W_["g0"])]),
                ("N (man-years) Black / White", [f"{B_['n']:,} / {W_['n']:,}"]),
                ("Displaced fathers Black / White", [f"{B_['units']:,} / {W_['units']:,}"])]
        for k, v in (("gap", gap), ("joint_explained_black_cost", -expl_B), ("joint_explained_white_cost", -expl_W)):
            ROWS.append(dict(table="decomp_joint_summary", sample="wife employed at baseline", outcome=y, term=k,
                             coef=v, se=gap_se if k == "gap" else np.nan))
        dec_panels.append((f"(i) Joint shock, wives employed at baseline: {ylab}", rows))
    md += ["### 4a. (i) The joint-shock channel (accounting)", "",
           "Wives employed at baseline (the only ones who can lose a job). J = the wife's hours fall to zero in "
           "ev / ev+1 or she reports a closure / layoff in ev-1..ev+1. The response decomposes as r = (P1 - P0) x "
           "cost + P1 x (response | J = 1) + (1 - P1) x (response | J = 0), with P1 / P0 = share with J among "
           "displaced / control families and cost = the change in the outcome at e = +1..+3 that comes with J among "
           "controls (bin x J coefficient in the model with displaced x bin x J). The gap accounted for by the "
           "joint shock = the difference between Black and White excess probabilities (P1 - P0) times the cost: "
           "how much larger the Black response would be if Black wives' excess joint-loss probability were the "
           "White one. J is an outcome, so this is an accounting decomposition, not a causal one; s.e. of the "
           "channel treat P1 - P0 as fixed.", "",
           md_table(["Estimate"], dec_panels), ""]

    # (ii) demand: pooled model with race-specific responses and common moderator slopes (Oaxaca / Gelbach)
    DM = ["same_sec_f", "sec_miss", "g_w_f", "bartik_f", "d_ur"]
    DL = {"same_sec_f": "Wife in husband's sector", "sec_miss": "Wife's sector unknown",
          "g_w_f": "Women's growth, wife's sector (national)", "bartik_f": "State women's Bartik",
          "d_ur": "Change in state unemployment rate", "J": "Joint job loss (wives employed at baseline)"}
    q0 = P[P["w0"].notna() & P["ev"].between(1980, 2019) & P["bartik_f"].notna() & P["d_ur"].notna()].copy()
    q0["sec_miss"] = q0["g_w_nat"].isna().astype(float)
    q0["same_sec_f"] = q0["same_sec"].fillna(0)
    q0["J0"] = q0["J"].fillna(0)
    SAMP4 = [("All wives", q0), ("Wife not employed at baseline", q0[q0["wemp0"] == 0]),
             ("Wife employed at baseline", q0[q0["wemp0"] == 1])]
    dec2 = []
    for sname, qs in SAMP4:
        for y, ylab in DEC_Y + [("w_look", "Wife unemployed, looking")]:
            qq = qs.copy()
            tr = qq[qq["treat"] == 1].drop_duplicates("unit")
            qq["g_w_f"] = qq["g_w_nat"]
            mu_g = tr["g_w_nat"].mean()
            qq["g_w_f"] = qq["g_w_f"].fillna(mu_g)
            mods = DM + (["J0"] if sname != "Wife not employed at baseline" else [])
            tr = qq[qq["treat"] == 1].drop_duplicates("unit")
            sds = {}
            for c in mods:
                mu = tr[c].mean()
                sd = tr[c].std() if c in ("g_w_f", "bartik_f", "d_ur") else 1.0
                sds[c] = sd
                qq[c] = (qq[c] - mu) / sd
            extra = [("tb", "tB"), ("mb", "black")]
            qq["tB"] = qq["treat"] * qq["black"]
            # model A: race-specific response only
            estA, infA, _ = binned(qq, y, extra=extra)
            # model B: + common moderator slopes
            estB, infB, (b, V, xs) = binned(qq, y, mods=mods, extra=extra)
            trq = qq[qq["treat"] == 1].drop_duplicates("unit")
            dM = {c: trq.loc[trq["black"] == 1, c].mean() - trq.loc[trq["black"] == 0, c].mean() for c in mods}
            l = np.zeros(len(xs))
            contrib = {}
            for c in mods:
                i = xs.index(f"dm_{c}_post13")
                lc = np.zeros(len(xs))
                lc[i] = dM[c]
                l += lc
                contrib[c] = (lc @ b, np.sqrt(lc @ V @ lc))
            tot = (l @ b, np.sqrt(l @ V @ l))
            gapA, gapB = estA["tb_post13"], estB["tb_post13"]
            rows = [("Black - White response, e=+1..+3 (no moderators)", [fmt_y(y, *gapA)]),
                    ("Black - White response, e=+1..+3 (with moderators)", [fmt_y(y, *gapB)]),
                    ("White response (no moderators)", [fmt_y(y, *estA["d_post13"])])]
            for c in mods:
                lab = DL.get(c.replace("J0", "J"), c)
                rows.append((f"{lab}: Black - White mean among displaced (in s.d. units if continuous) / slope / "
                             "contribution", [f"{dM[c]:.3f} / " + fmt_y(y, *estB[f'dm_{c}_post13']) + " / " +
                                              fmt_y(y, contrib[c][0], contrib[c][1], pv(*contrib[c]))]))
                ROWS.append(dict(table="decomp_demand", sample=sname, outcome=y, term=f"contribution {c}",
                                 coef=contrib[c][0], se=contrib[c][1], p=pv(*contrib[c]), mean_diff=dM[c],
                                 slope=estB[f"dm_{c}_post13"][0], slope_se=estB[f"dm_{c}_post13"][1]))
            rows.append(("Total contribution of the moderators to the Black - White response",
                         [fmt_y(y, tot[0], tot[1], pv(*tot))]))
            rows.append(("Gelbach: gap without - with moderators", [f"{gapA[0] - gapB[0]:,.3f}"]))
            rows.append(("N (man-years) / displaced / clusters", [f"{infB['n']:,} / {infB['units']:,} / "
                                                                  f"{infB['clusters']:,}"]))
            for k, v in (("gap no moderators", gapA), ("gap with moderators", gapB), ("total contribution", tot)):
                ROWS.append(dict(table="decomp_demand", sample=sname, outcome=y, term=k, coef=v[0], se=v[1],
                                 p=pv(v[0], v[1]), n=infB["n"]))
            dec2.append((f"{sname}: {ylab}", rows))
        print("decomposition", sname, flush=True)
    md += ["### 4b. (ii) Demand in the wife's sector and area, and (i) the joint loss, in one pooled model", "",
           "Pooled Black + White stacked DiD (event years 1980-2019, state observed), wife present at baseline: "
           "displaced x bin, displaced x bin x Black, bin x Black (race-specific responses and trends), and for "
           "each moderator M: bin x M and displaced x bin x M with slopes common to both races (M centred at the "
           "displaced mean; continuous M in s.d. units). Contribution of M to the Black - White response = (Black "
           "- White mean of M among displaced families) x slope (Oaxaca with pooled slopes; s.e. by the delta "
           "method, mean differences fixed). Wife's sector growth is set to the displaced mean when her sector is "
           "unknown (indicator 'sector unknown' included). The joint loss J enters only for wives employed at "
           "baseline (0 otherwise) and is an outcome (accounting, not causal). A negative contribution means the "
           "moderator makes the Black response smaller than the White one.", "",
           md_table(["Estimate"], dec2), ""]

    # ================================================================ write
    pd.DataFrame(ROWS).to_csv(OUT / "correlated_shocks.csv", index=False)
    (OUT / "correlated_shocks.md").write_text("\n".join(md), encoding="utf-8")
    print("written", flush=True)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "extras":
        print(extras()["found"].to_string())
    else:
        main()
