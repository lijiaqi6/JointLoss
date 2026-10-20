r"""FMLA (1993) and mothers' return to the pre-birth employer: NLSY79 first stage (2026-10-17).

Search friction: a mother who leaves work at a birth must find a new job; job-protected leave (the FMLA, in force
5 Aug 1993) lets the job survive time out. Eligibility at a birth (29 CFR 825.110): the employer has >= 50 employees
within 75 miles of the work site, >= 12 months with the employer and >= 1,250 hours worked in the previous 12 months.

Data: NLSY79 women (White and Black, cross-sectional + Black supplemental samples) via NLSY79/common.py
(NLSY79/data/women79.pkl, family79.pkl; read only) plus extra columns read from the raw release
(Dropbox/NLS/nlsy79_all_1979-2022/nlsy79_all_1979-2022.csv, usecols only) and cached in data/fmla79_extra.pkl:
  HRS_WORKED_WK_NUM<w>          hours worked at all jobs in week w (weekly array; same week numbers as STATUS_WK_NUM)
  CPS-QES-FIRMSZ2_<y>           # of employees at the location of the CPS (current / most recent) job, 1979, 1980,
                                1986-1993 (not asked 1981-85)
  QES-FIRMSZ2.0k_<y>            # of employees at the location of job #k of round y (1994+, every job, k = 1..5)
  CPS-QES-FIRMSZ1/5             employer has > 1 location / # employees at the other locations (robustness)
  EMPLOYERS_ALL_CPSJOB_<y>.JJ   roster employer JJ is the CPS job of round y (links CPS-QES-FIRMSZ2 to JJ, 1979-93)
  EMPLOYERS_ALL_ID_<y>.JJ       job number k of roster employer JJ in round y (links QES-FIRMSZ2.0k to JJ, 1994+)
  EMPLOYERS_ALL_NUM_ARRAY / TENURE / HOURSWEEK_<y>.JJ   extracted, not used
  EMPLOYERS_ALL_STARTDATE_ORIGINAL.JJ~M/~Y  date she first started working for employer JJ
  REGION_<y>                    extracted, not used (the public NLSY79 has no state, so state leave laws cannot be
                                merged; see IGE/12a.PolicyCalendar.py)

Sample: births 1985-2002 (distinct birth weeks; twins once) to Black and White women, any parity, who were employed in
week b-13 (weekly array code >= 100) with a roster employer; that employer (common.employer_at(b-13), as in
NLSY79/6.BirthEmployment.py) is the pre-birth employer. Robustness: employed in every week b-13..b-1 (excludes women
who stopped before the birth, i.e. prenatal leave, which the FMLA itself covers - hence not the main sample). All
births of a woman kept; s.e. clustered by mother.

FMLA eligibility at the birth:
  large    # employees at the location of the pre-birth employer >= 50 (location size only; the FMLA counts all
           employees within 75 miles, so multi-site employers are partly misclassified as small). Report chosen: the
           last round <= the birth year in which the employer's size is reported (CPS job 1979-80 / 1986-93, any job
           1994+), else the first later round (flag size_after). Robustness: median of all reports; reports at or
           before the birth year only; missing size coded small / large with a missing dummy. Codes 99995+ ("number
           varies"), don't know and refusals are missing.
  tenure   weeks from first start with the employer (STARTDATE_ORIGINAL; fallback first roster work week) to b-1 >= 52
  hours    hours at all jobs in weeks b-52..b-1 (weekly hours array) >= 1,250; employed weeks without hours get her
           mean hours of the employed weeks with hours
  elig = large x tenure x hours

Outcomes (weekly array and roster; b = birth week):
  back_same_12/26/52  works for the pre-birth employer (roster JJ, gaps within the job cut out) in some week of
                      b+1..b+12 / 26 / 52 (includes women who never stopped)
  emp52               employed in week b+52
  weeks_out           weeks not employed in b+1..b+52 (weeks without information dropped, scaled to 52; >= 39 needed)
  leave4              a break of >= 4 weeks without work starting in b-13..b+13 (NLSY79/6.BirthEmployment.py)
  same52_if_leave     among leave4 = 1: works for the pre-birth employer after the break, by b+52 (sanity: ~0.5-0.6)

Design (DiD): y = a + b elig x post + c elig + large + tenure + hours + post + birth-year FE + mother controls (age,
age^2, AFQT percentile, married at the birth, education group, birth order 1/2/3+) + e; post = birth on/after 5 Aug
1993; s.e. clustered by mother. Event study: elig x birth-date bin (1985-87, 1988-90, 1991-4 Aug 1993 [reference],
5 Aug 1993-1995, 1996-98, 1999-2002), same controls. By race: separate regressions for Black and White mothers.

Writes data/fmla_births79.pkl (birth sample), output/fmla_first_stage.csv (every reported coefficient: table,
outcome, term, coef, se, p, stars, n, clusters, mean_y) and output/fmla_first_stage.md (tables).
Run: python IGE/12.FMLA.py [--extract] [--rebuild]   (--extract re-reads the raw csv, ~4 min)
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import os
NLSY79_DIR = Path(os.environ.get("NLSY79_DIR", r"G:\My Drive\Selection vs risk\NLSY79"))   # Selection-vs-risk/NLSY79 (helpers + extracts), read only

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(NLSY79_DIR))
import common as n79  # noqa: E402  (NLSY79/common.py, read only)
import os
DROPBOX = Path(os.environ.get("DROPBOX", Path.home() / "Dropbox"))   # raw data, read only

DATA, OUT = HERE / "data", HERE / "output"
RAW = Path(DROPBOX / "NLS/nlsy79_all_1979-2022/nlsy79_all_1979-2022.csv")
CDB_INDEX = NLSY79_DIR / "data" / "codebook_index.csv"
EXTRA = DATA / "fmla79_extra.pkl"
FMLA_WEEK = n79.week_of(1993, 8, 5)
MAX_WEEK = n79.week_of(2004, 12, 31)


# ---------------------------------------------------------------- extract
def extract():
    ix = pd.read_csv(CDB_INDEX)
    q = ix.qname.astype(str)
    yr = ix.year.astype(str)
    sel = []
    hrs = ix[q.str.fullmatch(r"HRS_WORKED_WK_NUM\d{4}")]
    hrs = hrs[hrs.qname.str[-4:].astype(int) <= MAX_WEEK]
    sel.append(hrs.assign(name="hrs" + hrs.qname.str[-4:]))
    fs = ix[q.str.fullmatch(r"(CPS-)?QES-FIRMSZ[125](\.0\d)?") & yr.str.fullmatch(r"\d{4}")]
    fs = fs[fs.year.astype(int) <= 2004]
    sel.append(fs.assign(name=fs.qname + "_" + fs.year.astype(str)))
    ro = ix[q.str.fullmatch(r"EMPLOYERS_ALL_(CPSJOB|NUM_ARRAY|ID|TENURE|HOURSWEEK)_\d{4}\.\d\d")]
    ro = ro[ro.qname.str.extract(r"_(\d{4})\.")[0].astype(int) <= 2004]
    sel.append(ro.assign(name=ro.qname.str.replace("EMPLOYERS_ALL_", "", regex=False)))
    sd = ix[q.str.fullmatch(r"EMPLOYERS_ALL_(STARTDATE_ORIGINAL\.\d\d~[MY]|UID\.\d\d)")]
    sel.append(sd.assign(name=sd.qname.str.replace("EMPLOYERS_ALL_", "", regex=False)))
    rg = ix[(q == "REGION") & yr.str.fullmatch(r"\d{4}")]
    sel.append(rg.assign(name="REGION_" + rg.year.astype(str)))
    sel = pd.concat(sel)
    assert sel.name.is_unique, sel[sel.name.duplicated()].head()
    cols = ["R0000100"] + list(sel.col)
    print(f"reading {len(cols)} columns from the raw NLSY79 csv ...", flush=True)
    df = pd.read_csv(RAW, usecols=cols, dtype=np.float32).rename(columns={"R0000100": "id", **dict(zip(sel.col, sel.name))})
    ids = pd.read_pickle(n79.DATA / "women79.pkl")[["id"]]
    df = ids.merge(df, on="id", how="left")
    DATA.mkdir(exist_ok=True)
    df.to_pickle(EXTRA)
    print(f"{EXTRA.name}: {df.shape}")


# ---------------------------------------------------------------- employer characteristics
def size_reports(x):
    """per woman: {JJ: [(round year, # employees at the location)]}; 'number varies' (99995+), DK / refusal dropped."""
    rounds_cps = [int(c.split("_")[1]) for c in x.columns if re.fullmatch(r"CPS-QES-FIRMSZ2_\d{4}", c)]
    rounds_job = sorted({int(c.split("_")[1]) for c in x.columns if re.fullmatch(r"QES-FIRMSZ2\.0\d_\d{4}", c)})
    out = [dict() for _ in range(len(x))]

    def ok(v):
        return v == v and 0 <= v < 99995

    for y in rounds_cps:                       # 1979-93: the CPS job only (roster flag CPSJOB_<y>.JJ = 1)
        jjs = [c for c in x.columns if re.fullmatch(rf"CPSJOB_{y}\.\d\d", c)]
        sz = x[f"CPS-QES-FIRMSZ2_{y}"].to_numpy()
        flag = x[jjs].to_numpy()
        for i in range(len(x)):
            if not ok(sz[i]):
                continue
            hit = np.where(flag[i] == 1)[0]
            if len(hit) == 1:
                out[i].setdefault(jjs[hit[0]][-2:], []).append((y, float(sz[i])))
    for y in rounds_job:                       # 1994+: job #k of the round = roster employer with ID_<y>.JJ = k
        jjs = [c for c in x.columns if re.fullmatch(rf"ID_{y}\.\d\d", c)]
        ids = x[jjs].to_numpy()
        for k in range(1, 6):
            col = f"QES-FIRMSZ2.0{k}_{y}"
            if col not in x:
                continue
            sz = x[col].to_numpy()
            for i in range(len(x)):
                if not ok(sz[i]):
                    continue
                hit = np.where(ids[i] == k)[0]
                if len(hit) == 1:
                    out[i].setdefault(jjs[hit[0]][-2:], []).append((y, float(sz[i])))
    return out


def pick_size(reports, birth_year):
    """last report from a round <= the birth year, else the first later one; (size, after?, n reports)."""
    if not reports:
        return np.nan, np.nan, 0
    rs = sorted(reports)
    before = [r for r in rs if r[0] <= birth_year]
    if before:
        return before[-1][1], 0.0, len(rs)
    return rs[0][1], 1.0, len(rs)


def first_start(x, i, jj, spells_i):
    """week she first started with employer JJ (STARTDATE_ORIGINAL; fallback: first roster work week)."""
    m, y = x.at[i, f"STARTDATE_ORIGINAL.{jj}~M"], x.at[i, f"STARTDATE_ORIGINAL.{jj}~Y"]
    w = n79.week_of(y, m, 1) if (y == y and m == m and y > 1900 and 1 <= m <= 12) else np.nan
    w0 = min((a for a, _ in spells_i.get(jj, [])), default=np.nan)
    return w if w == w else w0


# ---------------------------------------------------------------- birth sample
def build():
    d = n79.load()
    x = pd.read_pickle(EXTRA)
    assert (x.id.to_numpy() == d.id.to_numpy()).all()
    E = n79.employed_matrix(n79.weekly(d))
    nW = E.shape[1]
    hc = sorted(c for c in x.columns if re.fullmatch(r"hrs\d{4}", c))
    assert hc[0] == "hrs0000" and len(hc) == int(hc[-1][3:]) + 1          # column index = week number
    H = x[hc].to_numpy().astype(float)
    H[H < 0] = np.nan
    B = n79.births(d)
    mar = n79.marriages(d)
    spells = n79.employer_spells(d, n79.roster_index(d))
    sizes = size_reports(x)
    afqt = np.where(d["AFQT-3_1981"] >= 0, d["AFQT-3_1981"] / 1000.0, np.nan)
    lo, hi = n79.week_of(1985, 1, 1), n79.week_of(2002, 12, 31)
    rows = []
    for i in range(len(d)):
        bw = sorted({int(b) for b in B[i] if b == b})                  # distinct birth weeks (twins once)
        for order, b in enumerate(bw, start=1):
            if not (lo <= b <= hi) or b + 53 >= nW or E[i, b - 13] != 1:
                continue
            jj = n79.employer_at(spells[i], b - 13)
            if jj is None:
                continue
            byear = int(n79.year_of_week(b))
            rep = sizes[i].get(jj, [])
            size, after, nrep = pick_size(rep, byear)
            start = first_start(x, i, jj, spells[i])
            e52, h52 = E[i, b - 52:b], H[i, b - 52:b]
            have = (e52 == 1) & ~np.isnan(h52)
            if have.any():
                fill = h52[have].mean()                                  # employed weeks without hours: her mean
                hrs = float(np.where(e52 == 1, np.where(np.isnan(h52), fill, h52), 0.0).sum())
            else:
                hrs = 0.0 if not np.any(e52 == 1) else np.nan
            post_w = E[i, b + 1:b + 53]
            valid = ~np.isnan(post_w)
            r = dict(i=i, id=int(d.at[i, "id"]), race=d.at[i, "race"], edu=d.at[i, "edu"], afqt=afqt[i],
                     bweek=b, byear=byear, order=order, age=(b - n79.week_of(d.at[i, "birth_year"], 7)) / 52.18,
                     married=float(n79.married_at(mar[i], b)), all13=float(np.all(E[i, b - 13:b] == 1)), jj=jj,
                     size=size, size_after=after, size_nrep=nrep,
                     size_med=float(np.median([v for _, v in rep])) if rep else np.nan,
                     tenure_wk=(b - 1 - start) if start == start else np.nan, hours52=hrs,
                     post=float(b >= FMLA_WEEK))
            for k in (12, 26, 52):
                r[f"back_same_{k}"] = float(n79.works_for(spells[i], jj, b + 1, b + k))
            r["emp52"] = E[i, b + 52] if E[i, b + 52] == E[i, b + 52] else np.nan
            r["weeks_out"] = float(np.sum(post_w[valid] == 0) * 52.0 / valid.sum()) if valid.sum() >= 39 else np.nan
            r["back_any_52"] = float(np.any(post_w[valid] == 1)) if valid.sum() else np.nan
            # leave as in NLSY79/6.BirthEmployment.py: a break of >= 4 weeks without work starting in b-13..b+13
            s0 = next((w for w in range(b - 13, b + 14) if all(E[i, w + k] == 0 for k in range(4))), None)
            r["leave4"] = float(s0 is not None)
            r["same52_if_leave"] = float(n79.works_for(spells[i], jj, s0 + 4, b + 52)) if s0 is not None else np.nan
            rows.append(r)
    s = pd.DataFrame(rows)
    ind = lambda v, c: np.where(v.notna(), (v >= c).astype(float), np.nan)  # noqa: E731
    s["large"], s["large_med"] = ind(s["size"], 50), ind(s["size_med"], 50)
    s["long_tenure"], s["hours_ok"] = ind(s.tenure_wk, 52), ind(s.hours52, 1250)
    s["elig"] = s.large * s.long_tenure * s.hours_ok
    s["elig_med"] = s.large_med * s.long_tenure * s.hours_ok
    s["black"] = (s.race == "Black").astype(float)
    s["age2"] = s.age ** 2
    s["order_c"] = s.order.clip(upper=3)
    s.to_pickle(DATA / "fmla_births79.pkl")
    return s


# ---------------------------------------------------------------- regressions
OUTCOMES = ["back_same_12", "back_same_26", "back_same_52", "emp52", "weeks_out", "leave4"]
LABEL = {"leave4": "Leave >= 4 wk", "same52_if_leave": "Same employer by 52 wk, given leave >= 4 wk", "back_same_12": "Same employer by 12 wk", "back_same_26": "Same employer by 26 wk",
         "back_same_52": "Same employer by 52 wk", "emp52": "Employed at 52 wk", "weeks_out": "Weeks out (yr 1)"}
COMP = ["large", "long_tenure", "hours_ok"]
BINS = ["1985-87", "1988-90", "1991-Jul93", "Aug93-95", "1996-98", "1999-2002"]
REF_BIN = "1991-Jul93"


def bin_of(b, y):
    if b >= FMLA_WEEK:
        return "Aug93-95" if y < 1996 else "1996-98" if y < 1999 else "1999-2002"
    return "1985-87" if y < 1988 else "1988-90" if y < 1991 else "1991-Jul93"


def fit(s, y, terms, elig="elig"):
    """OLS of y on terms + components + post + controls + birth-year FE; s.e. clustered by mother."""
    comp = ["large_med" if (c == "large" and elig == "elig_med") else c for c in COMP]
    ctrl = ["age", "age2", "afqt", "married"]
    dd = s.dropna(subset=[y, *terms, *comp, "post", *ctrl, "edu", "order_c", "byear", "id"]).copy()
    X = dd[[*terms, *comp, "post", *ctrl]].astype(float)
    X = X.join(pd.get_dummies(dd["edu"].astype(str), prefix="edu", drop_first=True, dtype=float))
    X = X.join(pd.get_dummies(dd["order_c"], prefix="order", drop_first=True, dtype=float))
    X = X.join(pd.get_dummies(dd["byear"], prefix="by", drop_first=True, dtype=float))
    X = sm.add_constant(X.loc[:, X.std() > 0])
    r = sm.OLS(dd[y].astype(float), X).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(dd["id"])[0]})
    return r, dd


def stars(p):
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""


def cell(r, t):
    if t not in r.params:
        return ""
    b, se, p = r.params[t], r.bse[t], r.pvalues[t]
    pv = "<0.001" if p < 0.001 else f"{p:.3f}"
    return f"{b:.3f}{stars(p)} ({se:.3f}) [p={pv}]"


def table(s, title, terms, rows, elig="elig", outcomes=OUTCOMES):
    res, recs = {}, []
    for y in outcomes:
        r, dd = fit(s, y, terms, elig)
        res[y] = (r, dd)
        for t in rows:
            if t in r.params:
                recs.append(dict(table=title, outcome=y, term=t, coef=r.params[t], se=r.bse[t], p=r.pvalues[t],
                                 stars=stars(r.pvalues[t]), n=int(r.nobs), clusters=dd.id.nunique(),
                                 mean_y=dd[y].mean()))
    lines = [f"### {title}", "", "| | " + " | ".join(f"({k + 1}) {LABEL[y]}" for k, y in enumerate(outcomes)) + " |",
             "|---" * (len(outcomes) + 1) + "|"]
    for t, lab in rows.items():
        lines.append(f"| {lab} | " + " | ".join(cell(res[y][0], t) for y in outcomes) + " |")
    lines.append("| Birth-year FE, post, components, mother controls | " + " | ".join("Yes" for _ in outcomes) + " |")
    lines.append("| Mean of outcome | " + " | ".join(f"{res[y][1][y].mean():.3f}" for y in outcomes) + " |")
    lines.append("| N births | " + " | ".join(f"{int(res[y][0].nobs):,}" for y in outcomes) + " |")
    lines.append("| Mothers (clusters) | " + " | ".join(f"{res[y][1].id.nunique():,}" for y in outcomes) + " |")
    return lines + [""], recs


def describe(s):
    cnt = lambda q: f"{len(q):,} births / {q.id.nunique():,} mothers"  # noqa: E731
    ok = s.dropna(subset=["elig"])
    out = [f"- Births 1985-2002 (distinct birth weeks), mother employed in week b-13 with a roster employer: {cnt(s)} "
           f"(Black {cnt(s[s.black == 1])}, White {cnt(s[s.black == 0])})",
           f"- of which employed in all 13 weeks b-13..b-1: {cnt(s[s.all13 == 1])}"]
    for c, lab in (("size", "location size reported for the pre-birth employer"), ("tenure_wk", "tenure known"),
                   ("hours52", "hours known")):
        out.append(f"- {lab}: {s[c].notna().mean():.3f} (pre-FMLA {s.loc[s.post == 0, c].notna().mean():.3f}, "
                   f"post {s.loc[s.post == 1, c].notna().mean():.3f})")
    out.append(f"- size taken from a round after the birth year: {s.size_after.mean():.3f}")
    out.append(f"- eligibility known: {cnt(ok)}; eligible share {ok.elig.mean():.3f} (pre "
               f"{ok.loc[ok.post == 0, 'elig'].mean():.3f}, post {ok.loc[ok.post == 1, 'elig'].mean():.3f}); "
               f"location >= 50 {ok.large.mean():.3f}, tenure >= 52 wk {ok.long_tenure.mean():.3f}, "
               f"hours >= 1,250 {ok.hours_ok.mean():.3f}")
    for y in OUTCOMES + ["back_any_52", "same52_if_leave"]:
        out.append(f"- mean {y}: all {s[y].mean():.3f}; eligible {ok.loc[ok.elig == 1, y].mean():.3f}, "
                   f"not eligible {ok.loc[ok.elig == 0, y].mean():.3f}")
    m = s.assign(sz_miss=s["size"].isna().astype(float))
    out.append("- size missing, by post x back_same_52: " + "; ".join(
        f"post={int(p)}, same employer={int(b)}: {g.sz_miss.mean():.3f} (n={len(g)})"
        for (p, b), g in m.groupby(["post", "back_same_52"])))
    out.append("- births by bin: " + ", ".join(f"{k} {v}" for k, v in s["bin"].value_counts().reindex(BINS).items()))
    cells = ok.groupby(["post", "elig"])[OUTCOMES].mean().round(3).reset_index()
    hdr = "| " + " | ".join(cells.columns) + " |"
    tab = [hdr, "|---" * len(cells.columns) + "|"] + ["| " + " | ".join(f"{v:g}" for v in r) + " |"
                                                      for r in cells.itertuples(index=False)]
    return out + ["", "Raw means by period (post) and eligibility:", ""] + tab + [""]


def main():
    if "--extract" in sys.argv or not EXTRA.exists():
        extract()
    s = build() if ("--rebuild" in sys.argv or not (DATA / "fmla_births79.pkl").exists()) else pd.read_pickle(
        DATA / "fmla_births79.pkl")
    s["elig_post"] = s.elig * s.post
    s["elig_med_post"] = s.elig_med * s.post
    s["bin"] = [bin_of(b, y) for b, y in zip(s.bweek, s.byear)]
    es_terms = []
    for name in BINS:
        if name != REF_BIN:
            s[f"elig_x_{name}"] = s.elig * (s["bin"] == name)
            es_terms.append(f"elig_x_{name}")
    OUT.mkdir(exist_ok=True)
    md = ["# FMLA (1993) and the return to the pre-birth employer: NLSY79 first stage", "",
          "Generated by `IGE/12.FMLA.py`. Cells: coefficient with stars (*** p<0.01, ** p<0.05, * p<0.1), (s.e. "
          "clustered by mother), [p-value]. All regressions: eligibility components (location >= 50 employees, "
          "tenure >= 52 weeks, >= 1,250 hours in the 52 weeks before the birth), post (birth on/after 5 Aug 1993), "
          "birth-year FE, mother controls (age, age^2, AFQT percentile, married at the birth, education group, birth "
          "order 1/2/3+).", "", "## Sample", ""]
    md += describe(s)
    recs = []
    rows_did = {"elig_post": "Eligible x post", "elig": "Eligible", "large": "Location >= 50 employees",
                "long_tenure": "Tenure >= 52 weeks", "hours_ok": "Hours >= 1,250", "post": "Post (birth >= 5 Aug 1993)"}
    groups = (("All", s), ("Black mothers", s[s.black == 1]), ("White mothers", s[s.black == 0]))
    md += ["## Difference-in-differences", ""]
    for lab, q in groups:
        lines, rr = table(q, f"DiD - {lab}", ["elig_post", "elig"], rows_did)
        md += lines
        recs += rr
    rows_es = {f"elig_x_{n}": f"Eligible x {n}" for n in BINS if n != REF_BIN}
    rows_es["elig"] = f"Eligible (= eligible x {REF_BIN})"
    md += ["## Event study (eligible x birth-date bin; reference bin 1991 - 4 Aug 1993)", ""]
    for lab, q in groups:
        lines, rr = table(q, f"Event study - {lab}", es_terms + ["elig"], rows_es)
        md += lines
        recs += rr
    md += ["## Robustness (all mothers; eligible x post and eligible shown)", ""]
    rob = [("Employed in all 13 weeks before the birth", s[s.all13 == 1], "elig"),
           ("First births only", s[s.order == 1], "elig"),
           ("Size reported in a round at or before the birth year", s[s.size_after == 0], "elig"),
           ("Size = median of all reports for the employer", s, "elig_med")]
    for lab, code in (("Missing location size coded < 50 (+ missing-size dummy)", 0.0),
                      ("Missing location size coded >= 50 (+ missing-size dummy)", 1.0)):
        q = s.assign(large=s.large.fillna(code), size_miss=s["size"].isna().astype(float))
        q["elig"] = q.large * q.long_tenure * q.hours_ok
        q["elig_post"] = q.elig * q.post
        lines, rr = table(q, f"Robustness - {lab}", ["elig_post", "elig", "size_miss"],
                          {"elig_post": "Eligible x post", "elig": "Eligible", "size_miss": "Size missing"})
        md += lines
        recs += rr
    lines, rr = table(s, "Robustness - conditional on a leave of >= 4 weeks (as NLSY79/6.BirthEmployment.py)",
                      ["elig_post", "elig"], {"elig_post": "Eligible x post", "elig": "Eligible"},
                      outcomes=["same52_if_leave"])
    md += lines
    recs += rr
    for lab, q, el in rob:
        m = "_med" if el == "elig_med" else ""
        lines, rr = table(q, f"Robustness - {lab}", [f"elig{m}_post", f"elig{m}"],
                          {f"elig{m}_post": "Eligible x post", f"elig{m}": "Eligible"}, elig=el)
        md += lines
        recs += rr
    pd.DataFrame(recs).to_csv(OUT / "fmla_first_stage.csv", index=False)
    (OUT / "fmla_first_stage.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
