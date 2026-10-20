r"""Established wives' exits: what moves a wife off a job she has held a year or more? (2026-10-20) [Paper A; WP2 of
proposals/fable_10h_plan_paperA.md]

Why. The largest misfit of the Paper A model is the wife's persistent exit (model 0.14% vs data ~1.0% a month). The
extension table (paperA_model/results/extensions_20261019.md) shows that the model already over-predicts exits at
job tenure 0-5 months and misses those at tenure 12+ (target sipp_wexit_ten_12p = 0.68% a month vs 0.27%), so a
new-job hazard alone cannot close the gap: the gap is established wives. IGE/63 pooled all tenures. This script
decomposes the exits of wives who have held their job for 12 months or more, so that the PI can choose the model
feature after the first estimate in one reading.

DATA (all read only; loaders of the source scripts imported via importlib, nothing of theirs is edited)
  SIPP  40.SIPPJointLoss.py couples panel (data/sipp_couples_panel.pkl; panels 2004, 2008, 2014; reference months
        2003-2016) + the wife's job slots from 63.WifeExitWhy.sipp_slots (tenure from the employer-specific start date,
        usual hours, detailed reason the job ended: exactly 63's and 66's definitions, so the 12+ hazard equals the
        target) + person-month extras re-read here from the same raw core files: monthly earnings (2004/08 TPEARN,
        2014 TPEARN), work-limiting health condition (EDISABL), and the program variables used by IGE/78 (food stamps /
        SNAP, UI, TANF receipt and amounts). The person-level extracts are cached in a scratch folder OUTSIDE the
        repository (--scratch; default: the system temp folder /ige75_scratch).
  PSID  60.PaperATargets.py's cached men's panel (data/paperA_targets_psid.pkl, 'm': male heads x calendar year
        with wife's annual hours, his hours and labor income, youngest child) + data/psid_person_year.pkl
        (children's birth years -> births by calendar year), as in 63.
SAMPLE (63's)
  SIPP: married wives 25-59, employed at t-1 and t, husband employed at t and t+1, all four months observed; persistent
  exit at t+1 = no job in any week at t+1 and t+2 (all reasons incl. involuntary); wife's weight. ESTABLISHED: job
  tenure at t >= 12 months (months since the start date of the main job, 63's definition; unknown tenure dropped).
  PSID 1968-1996 (annual years): hours > 0 in t and 0 in t+1, same husband and wife, husband working in t and t+1.
  ESTABLISHED proxy: the same wife also worked (hours > 0) in t-1 and t-2 (all available years kept; no balanced panel).
ESTIMATES
  (i)   12+ hazard by cell with the cell's share of wife-months and of exits (shares x hazards add up to the pooled 12+
        rate): child aged 0 in the household at t+1..t+9 (births from ~11 months before to 9 months after), youngest
        child, usual hours < 20 / 20-34, his job change t-2..t+1 (a job of his ended, he stays employed), his monthly
        earnings change > 25% up / down (mean of t+1, t+2 vs mean of t-2, t-1, both windows observed, pre > 0), her
        work-limiting health condition at t (EDISABL), age 55-59, education, race, tenure 12-35 / 36+;
  (ii)  joint LPM of the exit on all cells (pp; panel x rotation x month FE; wife's weight; s.e. clustered by
        household); stated reasons among 12+ exits (detailed reason of the job that ended at t+1, t, t+2 or t-1);
  (iii) Kaplan-Meier return to employment within 3 / 6 / 12 / 24 months of 12+ exits, by reason group, birth window
        and the residual group (cluster-bootstrap s.e.);
  (iv)  repeat exits among 12+ wives: an earlier persistent exit of the same wife in the panel (left-censored at the
        panel start), its hazard and LPM coefficient;
  (v)   the arithmetic the model needs: (a) LPM accounting: each cell's contribution b_k x mean(x_k) to the 12+ hazard
        (in % a month and as a share of the hazard; s.e. = se_k x mean(x_k)), residual = hazard - sum of
        contributions; (b) exclusive accounting of the 12+ exits in priority order: involuntary job end (stated) ->
        birth window -> own illness / injury or retirement (stated) -> usual hours < 20 -> his earnings rise > 25% or
        his job change -> residual; shares of exits and the implied piece of the 0.68% hazard; spell length (KM) of each
        piece, in particular the residual;
  PSID: the same on the annual exit of established wives (birth in t / t+1, his labor-income change, her hours in t,
        youngest child, age, race; calendar-year FE; s.e. clustered by 1968 family), return within 1 / 2 / 4 years,
        repeat-exit share and the coefficient on an earlier exit of the same wife (any exit in the window).
  Associations, not causal effects. *** p<0.01, ** p<0.05, * p<0.1 (normal approximation).
OUTPUTS (aggregate only)
  output/established_wife_exits.csv  every estimate: dataset, table, sample, cell, outcome, coef, se, p, stars, n
  output/established_wife_exits.md   tables (one outcome per column, covariates as rows, samples as row panels)
Run from the repository root: .venv/Scripts/python.exe -I IGE/75.EstablishedWifeExits.py [--only sipp,psid]
  [--scratch DIR] [--workers 2]
"""
import argparse
import importlib.util
import os
import sys
import tempfile
import time
import warnings
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import numpy as np                            # noqa: E402
import pandas as pd                           # noqa: E402

from common import DATA, OUT, stars           # noqa: E402

warnings.simplefilter("ignore", FutureWarning)
warnings.simplefilter("ignore", RuntimeWarning)
warnings.simplefilter("ignore", pd.errors.PerformanceWarning)
T0 = time.time()
TAG = "established_wife_exits"


def log(*a):
    print(f"[{time.time() - T0:7.0f}s]", *a, flush=True)


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


M63 = _load("ige63", "63.WifeExitWhy.py")      # estimators and the SIPP job-slot loader (read only)
sys.modules["ige63"] = M63                     # so that spawned workers can unpickle 63's slot_extract
ROWS = M63.ROWS                                # 63's add / add_reg / decompose append here
add, add_reg, decompose, wlpm, wmean, dummies, km, km_se = (M63.add, M63.add_reg, M63.decompose, M63.wlpm, M63.wmean,
                                                            M63.dummies, M63.km, M63.km_se)

# =====================================================================================================
# SIPP person-month extras (earnings, health, programs) from the raw core files -> scratch (person-level)
# =====================================================================================================
EX0408 = {"tpearn": "earn", "edisabl": "disab", "er05": "ui_r", "t05amt": "ui_a", "er20": "tanf_r", "t20amt": "tanf_a",
          "er27": "fs_r", "t27amt": "fs_a", "rcutyp27": "fs_cov", "thfdstp": "hh_fs_a"}
EX14 = {"TPEARN": "earn", "EDISABL": "disab", "EUC1MNYN": "ui_r", "EUC2MNYN": "ui_r2", "EUC3MNYN": "ui_r3",
        "TUC1AMT": "ui_a", "TUC2AMT": "ui_a2", "TUC3AMT": "ui_a3", "RTANFYN": "tanf_r", "TTANF_AMT": "tanf_a",
        "RFSYN": "fs_r", "TFS_AMT": "fs_a", "RFSCOV": "fs_cov"}


def extras_extract(args):
    """One raw wave -> person-month extras of married adults 18-70 (person-level: written only to the scratch)."""
    panel, w, raw, out = args
    out = Path(out)
    if out.exists():
        return str(out)
    if panel == 2014:
        base = ["SSUID", "PNUM", "SWAVE", "MONTHCODE", "ESEX", "EMS_EHC", "TAGE_EHC"]
        ex = EX14
    else:
        base = ["ssuid", "epppnum", "rhcalyr", "rhcalmn", "esex", "ems", "tage"]
        ex = EX0408
    want = set(base) | set(ex)
    kw = dict(usecols=lambda c: (c if panel == 2014 else c.lower()) in want, chunksize=60000, dtype=str,
              low_memory=False)
    if panel == 2014:
        import gzip
        with gzip.open(raw, "rt") as fh:
            head = fh.readline()
        kw["sep"] = "|" if head.count("|") > head.count(",") else ","
    parts = []
    for d in pd.read_csv(raw, **kw):
        if panel != 2014:
            d.columns = [c.lower() for c in d.columns]
        ms, age = M63._n(d, base[5]), M63._n(d, base[6])
        d = d[(ms == 1) & (age >= 18) & (age <= 70)]
        if not len(d):
            continue
        if panel == 2014:
            ssuid = d["SSUID"].astype(str).str.strip().to_numpy()
            pnum = M63._n(d, "PNUM")
            year, month = 2012 + M63._n(d, "SWAVE"), M63._n(d, "MONTHCODE")
        else:
            ssuid = d["ssuid"].astype(str).str.strip().str.lstrip("0").to_numpy()
            pnum = M63._n(d, "epppnum")
            year, month = M63._n(d, "rhcalyr"), M63._n(d, "rhcalmn")
        o = pd.DataFrame({"panel": panel, "ssuid": ssuid, "pnum": pnum.astype(np.int32),
                          "ym": (year * 12 + month - 1).astype(np.int32)})
        for c, nm in ex.items():
            v = pd.to_numeric(d[c], errors="coerce").to_numpy(float) if c in d else np.full(len(d), np.nan)
            o[nm] = v.astype(np.float32)
        parts.append(o)
    res = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame()
    res.to_pickle(out)
    return str(out)


def sipp_extras(scratch, workers):
    cache = scratch / "sipp_extras.pkl"
    if cache.exists():
        return pd.read_pickle(cache)
    m40 = M63._load("sipp40", "40.SIPPJointLoss.py")
    sd = scratch / "sipp_extras"
    sd.mkdir(parents=True, exist_ok=True)
    jobs = []
    for panel, nw in m40.PANELS.items():
        for w in range(1, nw + 1):
            raw = m40.src(panel, w)[1]
            if raw.exists():
                jobs.append((panel, w, str(raw), str(sd / f"extras_{panel}_{w:02d}.pkl")))
    log(f"SIPP: extracting person-month extras from {len(jobs)} waves with {workers} workers")
    with ProcessPoolExecutor(max_workers=workers) as exe:
        files = list(exe.map(extras_extract, jobs))
    X = pd.concat([pd.read_pickle(f) for f in files], ignore_index=True)
    X = X.drop_duplicates(["panel", "ssuid", "pnum", "ym"])
    # harmonise: receipt flags 1 = yes; amounts >= 0 (missing -> nan)
    for c in [c for c in X.columns if c.endswith(("_r", "_r2", "_r3", "_cov"))] + ["disab"]:
        X[c] = (X[c] == 1).astype(np.int8).where(X[c].notna())
    if "ui_r2" in X:
        X["ui_r"] = X[["ui_r", "ui_r2", "ui_r3"]].max(axis=1)
        X["ui_a"] = X[["ui_a", "ui_a2", "ui_a3"]].clip(lower=0).sum(axis=1, min_count=1)
        X = X.drop(columns=["ui_r2", "ui_r3", "ui_a2", "ui_a3"])
    X.to_pickle(cache)
    return X


def sipp_panel(scratch, workers):
    """40's couple panel + 63's wife job slots + extras of both spouses (suffix _w / _h). Returns P, L."""
    m40 = M63._load("sipp40", "40.SIPPJointLoss.py")
    cache = scratch / "sipp_wife_jobs.pkl"
    if cache.exists():
        J = pd.read_pickle(cache)
    else:
        J = M63.sipp_slots(scratch, workers)
        J.to_pickle(cache)
    X = sipp_extras(scratch, workers)
    log(f"SIPP: {len(J):,} wife job-months, {len(X):,} married person-months of extras")
    P = m40.build_panel()
    P, L = m40.add_vars(P)
    P["ssuid"] = P["ssuid"].astype(str)
    J = J.rename(columns={"pnum": "pnum_w"})
    J["ssuid"] = J["ssuid"].astype(str)
    P = P.merge(J, on=["panel", "ssuid", "pnum_w", "ym"], how="left")
    X["ssuid"] = X["ssuid"].astype(str)
    for s in ("w", "h"):
        Xs = X.rename(columns={c: f"{c}_{s}" for c in X.columns if c not in ("panel", "ssuid", "pnum", "ym")})
        Xs = Xs.rename(columns={"pnum": f"pnum_{s}"})
        P = P.merge(Xs, on=["panel", "ssuid", f"pnum_{s}", "ym"], how="left")
    assert P.duplicated(["cid", "ym"]).sum() == 0
    P = P.sort_values(["cid", "ym"]).reset_index(drop=True)
    L = m40.Look(P)
    return P, L


# =====================================================================================================
# SIPP: established wives (tenure >= 12 months)
# =====================================================================================================
RG_ORDER = ["involuntary", "childcare / family", "unsatisfactory arrangements / other quit", "quit to another job",
            "own illness / injury", "retirement", "school", "no job end recorded"]


def lpm_accounting(dataset, sample, r, X, w, ybar, terms, outcome):
    """(v-a) contribution of each term b_k x mean(x_k) to the hazard, % a month and share of the hazard."""
    tot = 0.0
    for lab, cols in terms.items():
        c = 0.0
        v = 0.0
        for col in cols:
            if col in r["b"]:
                xb = wmean(X[col].to_numpy(float), w)
                c += r["b"][col] * xb
                v += (r["se"][col] * xb) ** 2          # ignores the covariance between the terms of a group
        tot += c
        add(dataset, "v-lpm", sample, lab, f"{outcome}: contribution (pp)", 100 * c, 100 * np.sqrt(v), r["N"],
            note="b_k x mean(x_k); s.e. = se_k x mean(x_k)")
        add(dataset, "v-lpm", sample, lab, f"{outcome}: share of the hazard (%)", 100 * c / ybar, np.nan, r["N"])
    add(dataset, "v-lpm", sample, "residual (hazard - contributions)", f"{outcome}: contribution (pp)",
        100 * (ybar - tot), np.nan, r["N"])
    add(dataset, "v-lpm", sample, "residual (hazard - contributions)", f"{outcome}: share of the hazard (%)",
        100 * (ybar - tot) / ybar, np.nan, r["N"])
    add(dataset, "v-lpm", sample, "hazard", f"{outcome}: contribution (pp)", 100 * ybar, np.nan, r["N"])


def sipp_part(scratch, workers):
    P, L = sipp_panel(scratch, workers)
    for c in ("hrs_tot", "tenure", "rsd", "SEP_h", "INV_w", "yc", "earn_h", "disab_w"):
        P[c] = P[c].astype(float)
    E = {k: L.at("E_w", k) for k in range(-1, 3)}
    Eh = {k: L.at("E_h", k) for k in (0, 1)}
    age = P.age_w.between(25, 59).to_numpy()
    base_all = (E[-1] == 1) & (E[0] == 1) & (Eh[0] == 1) & (Eh[1] == 1) & np.isfinite(E[1]) & np.isfinite(E[2]) & age
    y = ((E[1] == 0) & (E[2] == 0)).astype(float)
    rsd = np.zeros(len(P), int)
    for k in (1, 0, 2, -1):
        rk = np.nan_to_num(L.at("rsd", k)).astype(int)
        rsd = np.where((rsd == 0) & (rk > 0), rk, rsd)
    inv = np.isin(rsd, [1, 2, 3, 4, 5]) | ((np.nan_to_num(L.at("INV_w", 1)) + np.nan_to_num(L.at("INV_w", 0))) > 0)
    inf_win = np.zeros(len(P), bool)
    for k in range(1, 10):
        inf_win |= (L.at("yc", k) == 0)
    hsep = np.zeros(len(P), bool)
    for k in (-2, -1, 0, 1):
        hsep |= (np.nan_to_num(L.at("SEP_h", k)) > 0)
    pre = np.nanmean(np.column_stack([L.at("earn_h", -2), L.at("earn_h", -1)]), axis=1)
    post = np.nanmean(np.column_stack([L.at("earn_h", 1), L.at("earn_h", 2)]), axis=1)
    ok_e = np.isfinite(pre) & np.isfinite(post) & (pre > 0)
    ratio = np.where(ok_e, post / np.where(pre > 0, pre, 1), np.nan)
    # previous persistent exit of the same wife (any tenure) within the panel
    P["_ex"] = np.where(base_all, y, 0.0)
    P["_prev"] = P.groupby("cid")["_ex"].cumsum() - P["_ex"]
    prev = P["_prev"].to_numpy() > 0
    ten_all = P.tenure.to_numpy(float)
    est = base_all & np.isfinite(ten_all) & (ten_all >= 12)
    d = P.loc[est].copy()
    d["y"] = y[est]
    d["rsd_x"], d["inv_x"], d["inf_win"], d["hsep"], d["prev_exit"] = rsd[est], inv[est], inf_win[est], hsep[est], prev[est]
    d["ratio"] = ratio[est]
    w = np.nan_to_num(d.wgt_w.to_numpy(float))
    ybar = wmean(d.y, w)
    S = "wives 25-59, husband employed, job tenure 12+ months (persistent exit)"
    log(f"SIPP: {len(d):,} established wife-months, persistent exit {100 * ybar:.3f}%")
    # pooled reference (all tenures) and the target replication
    yall = y[base_all]
    wall = np.nan_to_num(P.wgt_w.to_numpy(float)[base_all])
    add("SIPP", "vii", "wives 25-59, husband employed", "all tenures", "persistent monthly exit (%)",
        100 * wmean(yall, wall), np.nan, int(base_all.sum()))
    add("SIPP", "vii", "wives 25-59, husband employed", "tenure 12+ months (target sipp_wexit_ten_12p = 0.6755)",
        "persistent monthly exit (%)", 100 * ybar, np.nan, len(d))
    add("SIPP", "vii", "wives 25-59, husband employed", "tenure 12+ months: share of wife-months with known tenure",
        "persistent monthly exit (%)",
        100 * wall[np.isfinite(ten_all[base_all]) & (ten_all[base_all] >= 12)].sum()
        / wall[np.isfinite(ten_all[base_all]) & (ten_all[base_all] >= 0)].sum(), np.nan, len(d))
    exw = wall * yall
    add("SIPP", "vii", "wives 25-59, husband employed", "tenure 12+ months: share of all exits with known tenure",
        "persistent monthly exit (%)",
        100 * exw[np.isfinite(ten_all[base_all]) & (ten_all[base_all] >= 12)].sum()
        / exw[np.isfinite(ten_all[base_all]) & (ten_all[base_all] >= 0)].sum(), np.nan, len(d))
    hrs, ten = d.hrs_tot.to_numpy(float), d.tenure.to_numpy(float)
    rat = d.ratio.to_numpy(float)
    cells = {
        "child aged 0 in t+1..t+9": np.where(d.inf_win, "yes", "no"),
        "youngest child": M63.kid_lab(d.yc, -99),
        "usual hours (all jobs)": np.select([~np.isfinite(hrs), hrs < 20, hrs < 35], ["unknown", "< 20", "20-34"], "35+"),
        "husband's job change t-2..t+1": np.where(d.hsep, "yes", "no"),
        "husband's earnings t+1,t+2 vs t-2,t-1": np.select([~np.isfinite(rat), rat > 1.25, rat < 0.75],
                                                            ["unknown / zero", "rise > 25%", "fall > 25%"],
                                                            "within +-25%"),
        "work-limiting health condition at t": np.select([d.disab_w == 1, d.disab_w == 0], ["yes", "no"], "unknown"),
        "wife's age": M63.age_lab(d.age_w),
        "wife's education": np.select([d.educ_w <= 1, d.educ_w == 2, d.educ_w == 3], ["< high school", "high school",
                                                                                    "some college"], "BA+"),
        "race (husband)": np.select([d.race_h == 2, d.race_h == 1], ["Black", "White"], "Other"),
        "job tenure (months)": np.where(ten < 36, "12-35", "36+"),
        "previous persistent exit in panel": np.where(d.prev_exit, "yes", "no"),
        "panel": d.panel.astype(str).to_numpy(),
    }
    decompose("SIPP", S, d.y, w, cells)
    X = pd.concat([dummies(cells["child aged 0 in t+1..t+9"], "child aged 0 in t+1..t+9", "no"),
                   dummies(cells["youngest child"], "youngest child", "none <18"),
                   dummies(cells["usual hours (all jobs)"], "usual hours (all jobs)", "35+"),
                   dummies(cells["husband's job change t-2..t+1"], "husband's job change t-2..t+1", "no"),
                   dummies(cells["husband's earnings t+1,t+2 vs t-2,t-1"], "husband's earnings t+1,t+2 vs t-2,t-1",
                           "within +-25%"),
                   dummies(cells["work-limiting health condition at t"], "work-limiting health condition at t", "no"),
                   dummies(cells["wife's age"], "wife's age", "35-39"),
                   dummies(cells["wife's education"], "wife's education", "high school"),
                   dummies(cells["race (husband)"], "race (husband)", "White"),
                   dummies(cells["job tenure (months)"], "job tenure (months)", "36+")], axis=1)
    X = X.reset_index(drop=True)
    yv = d.y.to_numpy(float)
    ynv = ((yv == 1) & ~d.inv_x.to_numpy()).astype(float)
    SR = "tenure 12+ (panel x rotation x month FE)"
    r = wlpm(yv, X, w, fe=d.pm.to_numpy(), cl=d.hh.to_numpy())
    add_reg("SIPP", "ii", SR, "persistent exit (pp)", r)
    r_nv = wlpm(ynv, X, w, fe=d.pm.to_numpy(), cl=d.hh.to_numpy())
    add_reg("SIPP", "ii", SR, "persistent exit, no involuntary job end (pp)", r_nv)
    # (v-a) LPM accounting
    terms = {"birth window (child aged 0 in t+1..t+9)": ["child aged 0 in t+1..t+9: yes"],
             "youngest child 0-17 (other than the birth window)": [c for c in X.columns if c.startswith("youngest")],
             "usual hours < 20": ["usual hours (all jobs): < 20"],
             "usual hours 20-34": ["usual hours (all jobs): 20-34"],
             "husband's job change t-2..t+1": ["husband's job change t-2..t+1: yes"],
             "husband's earnings rise > 25%": ["husband's earnings t+1,t+2 vs t-2,t-1: rise > 25%"],
             "husband's earnings fall > 25%": ["husband's earnings t+1,t+2 vs t-2,t-1: fall > 25%"],
             "work-limiting health condition": ["work-limiting health condition at t: yes"],
             "wife 55-59": ["wife's age: 55-59"],
             "tenure 12-35 (vs 36+)": ["job tenure (months): 12-35"]}
    lpm_accounting("SIPP", "tenure 12+: LPM accounting (all exits)", r, X, w, ybar, terms, "persistent exit")
    lpm_accounting("SIPP", "tenure 12+: LPM accounting (exits without an involuntary job end)", r_nv, X, w,
                   wmean(ynv, w), terms, "persistent exit, no involuntary")
    # (ii) stated reasons among established exits
    ex = yv == 1
    rs = d.rsd_x.to_numpy()
    rgrp = np.array([M63.RGROUP.get(int(k), "no job end recorded") for k in rs])
    rlab = np.array([M63.RSD.get(int(k), "no job end recorded in t-1..t+2") for k in rs])
    subs = {"all 12+": np.ones(len(d), bool), "tenure 12-35": cells["job tenure (months)"] == "12-35",
            "tenure 36+": cells["job tenure (months)"] == "36+",
            "birth window": d.inf_win.to_numpy(), "no birth window": ~d.inf_win.to_numpy(),
            "race: Black": cells["race (husband)"] == "Black", "race: White": cells["race (husband)"] == "White"}
    for sname, smk in subs.items():
        mk = ex & smk
        if mk.sum() < 20:
            continue
        for labs, tab in ((rgrp, "iii-group"), (rlab, "iii-detail")):
            for c in pd.unique(labs[mk]):
                m2 = mk & (labs == c)
                v = w[m2].sum() / w[mk].sum()
                neff = w[mk].sum() ** 2 / np.sum(w[mk] ** 2)
                add("SIPP", tab, f"12+ exits: {sname}", c, "share of exits (%)", 100 * v,
                    100 * np.sqrt(v * (1 - v) / neff), int(m2.sum()))
    # (v-b) exclusive accounting of the exits (priority order)
    ill = np.isin(rs, [7, 10])
    rise = (cells["husband's earnings t+1,t+2 vs t-2,t-1"] == "rise > 25%") | d.hsep.to_numpy()
    lowh = cells["usual hours (all jobs)"] == "< 20"
    cat = np.select([d.inv_x.to_numpy(), d.inf_win.to_numpy(), ill, lowh, rise],
                    ["1 involuntary job end (stated)", "2 birth window (child aged 0 in t+1..t+9)",
                     "3 own illness / injury or retirement (stated)", "4 usual hours < 20",
                     "5 husband's earnings rise > 25% or job change"], "6 residual")
    for c in sorted(pd.unique(cat[ex])):
        m2 = ex & (cat == c)
        v = w[m2].sum() / w[ex].sum()
        neff = w[ex].sum() ** 2 / np.sum(w[ex] ** 2)
        add("SIPP", "v-excl", "tenure 12+: exclusive accounting of exits", c, "share of exits (%)", 100 * v,
            100 * np.sqrt(v * (1 - v) / neff), int(m2.sum()))
        add("SIPP", "v-excl", "tenure 12+: exclusive accounting of exits", c, "piece of the 12+ hazard (% a month)",
            100 * v * ybar, np.nan, int(m2.sum()))
        # the same category's hazard among all established wife-months with that profile (non-exclusive base)
    # residual: what do these wives look like? (means among residual exits vs all 12+ wife-months)
    res = ex & (cat == "6 residual")
    for lab, x in (("youngest child < 6", np.isin(cells["youngest child"], ["0", "1-2", "3-5"])),
                   ("no child < 18", cells["youngest child"] == "none <18"),
                   ("usual hours 20-34", cells["usual hours (all jobs)"] == "20-34"),
                   ("tenure 12-35", cells["job tenure (months)"] == "12-35"),
                   ("previous persistent exit in panel", d.prev_exit.to_numpy()),
                   ("no job end recorded", rgrp == "no job end recorded"),
                   ("stated quit: unsatisfactory / other", rgrp == "unsatisfactory arrangements / other quit"),
                   ("stated: childcare / family", rgrp == "childcare / family"),
                   ("wife < high school", cells["wife's education"] == "< high school"),
                   ("wife 50-59", np.isin(cells["wife's age"], ["50-54", "55-59"]))):
        add("SIPP", "v-res", "residual exits vs all 12+ wife-months", lab, "residual exits (%)",
            100 * wmean(x[res].astype(float), w[res]), np.nan, int(res.sum()))
        add("SIPP", "v-res", "residual exits vs all 12+ wife-months", lab, "all 12+ exits (%)",
            100 * wmean(x[ex].astype(float), w[ex]), np.nan, int(ex.sum()))
        add("SIPP", "v-res", "residual exits vs all 12+ wife-months", lab, "all 12+ wife-months (%)",
            100 * wmean(x.astype(float), w), np.nan, len(d))
    # (iii) spell length: KM return after the first non-employed month (t+1)
    H = 36
    st = np.column_stack([L.at("E_w", 1 + s) for s in range(1, H + 1)])[est][ex]
    we, cle = w[ex], d.hh.to_numpy()[ex]
    groups = {"all 12+ exits": np.ones(ex.sum(), bool),
              "birth window": d.inf_win.to_numpy()[ex], "no birth window": ~d.inf_win.to_numpy()[ex],
              "tenure 12-35": cells["job tenure (months)"][ex] == "12-35",
              "tenure 36+": cells["job tenure (months)"][ex] == "36+",
              "previous exit in panel": d.prev_exit.to_numpy()[ex]}
    for g in RG_ORDER:
        groups[f"reason: {g}"] = rgrp[ex] == g
    for c in sorted(pd.unique(cat[ex])):
        groups[f"exclusive: {c}"] = cat[ex] == c
    for g, mk in groups.items():
        if mk.sum() < 30:
            continue
        ret, risk = km(st[mk], we[mk], H)
        se = km_se(st[mk], we[mk], H, cle[mk], reps=100, seed=75)
        for h in (3, 6, 12, 24):
            add("SIPP", "iv", f"12+ exits: {g}", f"return within {h} months", "KM probability (%)",
                100 * ret[h - 1], 100 * se[h - 1], int(mk.sum()), note=f"at risk at month {h}: {risk[h - 1]}")
    # median spell (months) by group: first s with KM >= 50%
        med = int(np.argmax(ret >= 0.5) + 1) if (ret >= 0.5).any() else np.nan
        add("SIPP", "iv-med", "12+ exits: median non-employment spell (KM; 37 = not reached in 36 months)", g,
            "months", med if np.isfinite(med) else 37, np.nan, int(mk.sum()))
    # LPM of the return within 12 months among 12+ exits observed 12 months after
    obs12 = np.isfinite(st[:, :12]).all(1)
    if obs12.sum() > 200:
        ret12 = (np.nan_to_num(st[:, :12]) == 1).any(1).astype(float)
        X3 = pd.concat([dummies(rgrp[ex], "reason", "childcare / family"),
                        dummies(cells["child aged 0 in t+1..t+9"][ex], "child aged 0 in t+1..t+9", "no"),
                        dummies(cells["race (husband)"][ex], "race (husband)", "White"),
                        dummies(cells["wife's age"][ex], "wife's age", "35-39"),
                        dummies(cells["job tenure (months)"][ex], "job tenure (months)", "36+")], axis=1)
        X3 = X3.reset_index(drop=True)
        r3 = wlpm(ret12[obs12], X3[obs12], we[obs12], fe=d.panel.to_numpy()[ex][obs12], cl=cle[obs12])
        add_reg("SIPP", "iv-lpm", "12+ exits observed 12 months after (panel FE)", "returned within 12 months (pp)", r3)
    # (iv) repeat exits
    X4 = pd.concat([dummies(cells["previous persistent exit in panel"], "previous persistent exit in panel", "no"), X],
                   axis=1).reset_index(drop=True)
    r4 = wlpm(yv, X4, w, fe=d.pm.to_numpy(), cl=d.hh.to_numpy())
    add_reg("SIPP", "vi", "tenure 12+, all controls (panel x rotation x month FE)", "persistent exit (pp)", r4,
            terms=["previous persistent exit in panel: yes"])
    add("SIPP", "vi-share", "12+ exits", "share by wives with an earlier exit in the panel", "share (%)",
        100 * w[ex & d.prev_exit.to_numpy()].sum() / w[ex].sum(), np.nan, int(ex.sum()))
    add("SIPP", "vi-share", "12+ wife-months", "share with an earlier exit in the panel", "share (%)",
        100 * wmean(d.prev_exit.to_numpy(float), w), np.nan, len(d))


# =====================================================================================================
# PSID: established proxy = the same wife worked in t-1 and t-2
# =====================================================================================================
def psid_part():
    m = pd.read_pickle(DATA / "paperA_targets_psid.pkl")["m"]
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    k = py[py["child"] & py["birth_year"].notna()][["wave", "int", "birth_year"]]
    by = k.assign(b=1).groupby(["wave", "int", "birth_year"])["b"].max().reset_index()
    del py
    m = m[m.w_pid.notna()].copy()
    m["w_pid"] = m["w_pid"].astype(np.int64)
    bt = by[by.birth_year == by.wave - 1][["wave", "int"]].drop_duplicates().assign(birth_t=1)
    m = m.merge(bt, on=["wave", "int"], how="left")
    m["birth_t"] = m["birth_t"].fillna(0)
    m = m.sort_values(["pid", "year"]).drop_duplicates(["pid", "year"])
    sh = m[["pid", "year", "w_pid", "wh", "hh", "hlab", "birth_t"]].copy()
    q = m.copy()
    for k_ in (-2, -1, 1, 2, 3, 4, 5):
        z = sh.copy()
        z["year"] = z["year"] - k_
        tag = f"p{k_}" if k_ > 0 else f"m{-k_}"
        z = z.rename(columns={c: f"{c}_{tag}" for c in ("w_pid", "wh", "hh", "hlab", "birth_t")})
        q = q.merge(z, on=["pid", "year"], how="left")
    q = q[(q.year >= 1968) & (q.year + 1 <= 1996)]
    base = (q.wh > 0) & (q.w_pid_p1 == q.w_pid) & (q.hh > 0) & (q.hh_p1 > 0) & q.w_age.between(25, 59) & q.wh_p1.notna()
    d0 = q[base].copy()
    d0["y"] = (d0.wh_p1 == 0).astype(float)
    d0["couple"] = d0.pid.astype(np.int64) * 10 ** 7 + d0.w_pid.astype(np.int64)
    d0 = d0.sort_values(["couple", "year"])
    d0["prev_exit"] = (d0.groupby("couple")["y"].cumsum() - d0["y"] > 0).astype(float)
    d0["nprior"] = d0.groupby("couple").cumcount()
    estab = ((d0.w_pid_m1 == d0.w_pid) & (d0.wh_m1 > 0) & (d0.w_pid_m2 == d0.w_pid) & (d0.wh_m2 > 0)
             & (d0.year - 2 >= 1968))
    add("PSID", "vii", "wives 25-59, husband working both years (annual years 1968-1996)", "all",
        "annual exit (%)", 100 * d0.y.mean(), np.nan, len(d0))
    d = d0[estab].copy()
    add("PSID", "vii", "wives 25-59, husband working both years (annual years 1968-1996)",
        "established: worked in t-1 and t-2", "annual exit (%)", 100 * d.y.mean(), np.nan, len(d))
    add("PSID", "vii", "wives 25-59, husband working both years (annual years 1968-1996)",
        "not established (no work in t-1 or t-2, or not observed)", "annual exit (%)", 100 * d0[~estab].y.mean(),
        np.nan, int((~estab).sum()))
    add("PSID", "vii", "wives 25-59, husband working both years (annual years 1968-1996)",
        "established: share of exits (%)", "annual exit (%)", 100 * d.y.sum() / d0.y.sum(), np.nan, len(d))
    log(f"PSID: {len(d):,} established wife-years, annual exit {100 * d.y.mean():.2f}%")
    dl = np.log(d.hlab_p1.clip(lower=1)) - np.log(d.hlab.clip(lower=1))
    dl = np.where((d.hlab > 0) & (d.hlab_p1 > 0), dl, np.nan)
    cells = {
        "birth in t+1": np.where(d.birth_t_p1 == 1, "yes", "no"),
        "birth in t": np.where(d.birth_t == 1, "yes", "no"),
        "youngest child (interview of t+1)": M63.kid_lab(d.youngest, -99),
        "her hours in t": np.select([d.wh < 500, d.wh < 1000, d.wh < 1750], ["1-499", "500-999", "1000-1749"], "1750+"),
        "his labor income t -> t+1": np.select([~np.isfinite(dl), dl < -0.25, dl > 0.25], ["zero / missing",
                                                "fall > 25%", "rise > 25%"], "within +-25%"),
        "wife's age": M63.age_lab(d.w_age),
        "race (head)": d.hrace.to_numpy(),
        "previous exit of the same wife": np.where(d.prev_exit == 1, "yes", "no"),
    }
    S = "established wives (worked t-1, t-2), husband working (annual exit)"
    decompose("PSID", S, d.y, np.ones(len(d)), cells, outcome="annual exit (%)")
    X = pd.concat([dummies(cells["birth in t+1"], "birth in t+1", "no"),
                   dummies(cells["birth in t"], "birth in t", "no"),
                   dummies(cells["youngest child (interview of t+1)"], "youngest child (interview of t+1)", "none <18"),
                   dummies(cells["her hours in t"], "her hours in t", "1750+"),
                   dummies(cells["his labor income t -> t+1"], "his labor income t -> t+1", "within +-25%"),
                   dummies(cells["wife's age"], "wife's age", "35-39"),
                   dummies(cells["race (head)"], "race (head)", "White")], axis=1).reset_index(drop=True)
    r = wlpm(d.y.to_numpy(), X, None, fe=d.year.to_numpy(), cl=d.fam68.to_numpy())
    add_reg("PSID", "ii", "established wives (calendar-year FE)", "annual exit (pp)", r)
    terms = {"birth in t or t+1": ["birth in t+1: yes", "birth in t: yes"],
             "youngest child 0-17": [c for c in X.columns if c.startswith("youngest")],
             "her hours 1-499": ["her hours in t: 1-499"], "her hours 500-999": ["her hours in t: 500-999"],
             "her hours 1000-1749": ["her hours in t: 1000-1749"],
             "his labor income rise > 25%": ["his labor income t -> t+1: rise > 25%"],
             "his labor income fall > 25%": ["his labor income t -> t+1: fall > 25%"],
             "wife 55-59": ["wife's age: 55-59"]}
    lpm_accounting("PSID", "established wives: LPM accounting", r, X, np.ones(len(d)), d.y.mean(), terms,
                   "annual exit")
    # repeat exits: previous exit of the same wife (any earlier exit in the window), wife-years after the first
    mk = (d.nprior >= 1).to_numpy()
    Xp = pd.concat([pd.DataFrame({"previous exit of the same wife": d.prev_exit.to_numpy()}), X], axis=1)
    noh = [c for c in Xp.columns if not c.startswith("her hours")]
    r = wlpm(d.y.to_numpy()[mk], Xp[noh][mk], None, fe=d.year.to_numpy()[mk], cl=d.fam68.to_numpy()[mk])
    add_reg("PSID", "vi", "established wives, no hours controls", "annual exit (pp)", r,
            terms=["previous exit of the same wife"])
    r = wlpm(d.y.to_numpy()[mk], Xp[mk], None, fe=d.year.to_numpy()[mk], cl=d.fam68.to_numpy()[mk])
    add_reg("PSID", "vi", "established wives, with her hours in t", "annual exit (pp)", r,
            terms=["previous exit of the same wife"])
    ne_ = d.groupby("couple")["y"].sum()
    exiters = ne_[ne_ > 0]
    add("PSID", "vi-share", "established couples with an exit", "share with 2+ established exits (%)", "share (%)",
        100 * (exiters >= 2).mean(), np.nan, len(exiters))
    ex = d.y.to_numpy() == 1
    add("PSID", "vi-share", "established exits", "share by wives with an earlier exit in the window (%)", "share (%)",
        100 * d.prev_exit.to_numpy()[ex].mean(), np.nan, int(ex.sum()))
    # return within 1, 2, 4 years
    wpid = d.w_pid.to_numpy(np.int64)
    for h, lab in ((1, "return within 1 year (hours > 0 in t+2)"), (2, "return within 2 years (t+2..t+3)"),
                   (4, "return within 4 years (t+2..t+5)")):
        okh = np.ones(len(d), bool)
        anyr = np.zeros(len(d), bool)
        for j in range(2, 2 + h):
            wj = d[f"wh_p{j}"].to_numpy(float)
            okh &= np.isfinite(wj) & (d[f"w_pid_p{j}"].to_numpy(float) == wpid) & (d.year.to_numpy() + j <= 1996)
            anyr |= np.nan_to_num(wj) > 0
        for sname, smk in (("established exits", ex),
                           ("established exits with a birth in t or t+1",
                            ex & ((d.birth_t_p1 == 1) | (d.birth_t == 1)).to_numpy()),
                           ("established exits without a birth, hours 1000+ in t",
                            ex & (d.birth_t_p1 == 0).to_numpy() & (d.birth_t == 0).to_numpy()
                            & (d.wh >= 1000).to_numpy()),
                           ("established exits without a birth, hours < 1000 in t",
                            ex & (d.birth_t_p1 == 0).to_numpy() & (d.birth_t == 0).to_numpy()
                            & (d.wh < 1000).to_numpy())):
            mk2 = smk & okh
            if mk2.sum() < 20:
                continue
            v = anyr[mk2].mean()
            add("PSID", "v-return", sname, lab, "share (%)", 100 * v, 100 * np.sqrt(v * (1 - v) / mk2.sum()),
                int(mk2.sum()))


# =====================================================================================================
# output
# =====================================================================================================
REG_TABLES = ("ii", "vi", "iv-lpm")


def cellfmt(r, nd=2):
    if not np.isfinite(r.coef):
        return "-"
    if np.isfinite(r.se) and (r.table in REG_TABLES or (r.table == "v-lpm" and "pp" in r.outcome)):
        pv = "p<0.001" if r.p < 0.001 else f"p={r.p:.3f}"
        return f"{r.coef:.{nd}f}{r.stars} ({r.se:.{nd}f}; {pv})"
    if np.isfinite(r.se):
        return f"{r.coef:.{nd}f} ({r.se:.{nd}f})"
    return f"{r.coef:.{nd}f}"


def write_md(D):
    L = [f"# Established wives' exits (IGE/75.EstablishedWifeExits.py, 2026-10-20)", "",
         "SIPP 2003-2016: married wives 25-59, husband employed, job tenure 12+ months at t; persistent monthly exit "
         "(employed t-1, t; no job in any week of t+1, t+2). PSID 1968-1996 (annual years): hours > 0 in t, 0 in t+1, "
         "for wives who also worked in t-1 and t-2. Regression cells: coefficient in percentage points, stars, (cluster "
         "s.e.; p); N = observations. *** p<0.01, ** p<0.05, * p<0.1. Hazard and share cells: rate (s.e.). "
         "Associations, not causal effects. Aggregates only.", ""]

    def table(sub, title, rowkey="cell", colkey="outcome", nd=2):
        if sub.empty:
            return
        L.append(f"## {title}")
        L.append("")
        for samp, g in sub.groupby("sample", sort=False):
            cols = list(dict.fromkeys(g[colkey]))
            L.append(f"*{samp}*")
            L.append("")
            L.append("| | " + " | ".join(cols) + " | N |")
            L.append("|---" * (len(cols) + 2) + "|")
            for rk, gg in g.groupby(rowkey, sort=False):
                vals = []
                for c in cols:
                    x = gg[gg[colkey] == c]
                    vals.append(cellfmt(x.iloc[0], nd) if len(x) else "")
                nmax = gg.n.max()
                L.append(f"| {rk} | " + " | ".join(vals) + f" | {int(nmax) if np.isfinite(nmax) else ''} |")
            notes = [x for x in g.note.unique() if isinstance(x, str) and x and not x.startswith("at risk")]
            if notes and len(notes) <= 3:
                L.append("")
                L.append("Notes: " + "; ".join(notes))
            L.append("")

    for ds in ("SIPP", "PSID"):
        X = D[D.dataset == ds]
        table(X[X.table == "vii"], f"{ds}: hazards and sample")
        table(X[X.table == "i"], f"{ds}: exit hazard by cell, share of wife-months and of exits (i)")
        table(X[X.table == "ii"], f"{ds}: LPM of the exit on all cells jointly (ii)")
        table(X[X.table == "v-lpm"], f"{ds}: the arithmetic the model needs, LPM accounting (v-a)")
        table(X[X.table == "v-excl"], f"{ds}: exclusive accounting of the exits, priority order (v-b)")
        table(X[X.table == "v-res"], f"{ds}: who the residual exits are (v-b)")
        table(X[X.table == "iii-group"], f"{ds}: stated reason for the 12+ exits, grouped", rowkey="cell",
              colkey="sample")
        table(X[X.table == "iii-detail"], f"{ds}: stated reason, detailed", rowkey="cell", colkey="sample")
        table(X[X.table == "iv"], f"{ds}: return to work after the exit (iii)")
        table(X[X.table == "iv-med"], f"{ds}: median spell (iii)")
        table(X[X.table == "iv-lpm"], f"{ds}: LPM of the return within 12 months (iii)")
        table(X[X.table == "v-return"], f"{ds}: return to work (iii)")
        table(X[X.table == "vi"], f"{ds}: repeat exits, earlier exit of the same wife (iv)")
        table(X[X.table == "vi-share"], f"{ds}: repeat exits, shares (iv)")
    (OUT / f"{TAG}.md").write_text("\n".join(L), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="sipp,psid")
    ap.add_argument("--scratch", default=str(Path(tempfile.gettempdir()) / "ige75_scratch"))
    ap.add_argument("--workers", type=int, default=2)
    a = ap.parse_args()
    scratch = Path(a.scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    assert HERE.parent not in scratch.resolve().parents, "scratch must be outside the repository"
    for part in a.only.split(","):
        ROWS.clear()
        if part == "sipp":
            sipp_part(scratch, min(a.workers, 2))
        elif part == "psid":
            psid_part()
        pd.DataFrame(ROWS).to_pickle(scratch / f"rows75_{part}.pkl")
        log(f"{part}: {len(ROWS)} rows")
    D = pd.concat([pd.read_pickle(scratch / f"rows75_{p}.pkl") for p in ("sipp", "psid")
                   if (scratch / f"rows75_{p}.pkl").exists()], ignore_index=True)
    D.to_csv(OUT / f"{TAG}.csv", index=False)
    write_md(D)
    log(f"wrote {len(D)} rows")


if __name__ == "__main__":
    main()
