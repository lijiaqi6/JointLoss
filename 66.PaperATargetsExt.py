r"""Targets of the two pre-built Paper A model extensions (2026-10-19), aggregate rows only.

Writes output/paperA_targets_ext.csv: the columns of output/paperA_targets.csv plus 'ext' (the extension of
paperA_model/estimate.py whose targets the row belongs to). estimate.py merges these rows into the target vector
ONLY when the extension is on (or its targets are requested with --ext-targets); rows with target = 0 are reported
checks (in the fit tables, outside the objective). Nothing in IGE/60-65 is edited; 63's SIPP sample is rebuilt here
with 63's own loaders (imported read only) and its scratch cache (outside the repository).

ext = new_job (new-job separation hazard; evidence proposals/wife_exit_evidence.md, IGE/63)
  sipp_wexit_ten_0_5, sipp_wexit_ten_6_11, sipp_wexit_ten_12p (targets): the persistent monthly exit of married wives
    (25-59) by the tenure of the job held at t: employed at t-1 and t, not employed at t+1 and t+2 (RMESR 6-8: no job
    in any week of the month), husband employed at t and t+1, all four months observed (63's sample exactly); tenure =
    months since the employer-specific start date (63: TSJDATE 2004/08, start year / month 2014; first month seen
    otherwise), bins 0-5, 6-11, 12+ (63's 12-35 and 36+ pooled); unknown tenure (10% of wife-months) dropped; wife's
    weight. Standard errors: cluster (household) bootstrap, 200 replications, weights x multinomial cluster counts
    (63's table (i) reports binomial s.e. with the Kish effective n; the bootstrap is used here because it allows for
    the same wife contributing many months).
  sipp_wexit_return12 (reported): Kaplan-Meier probability of being back in work within 12 months of the first
    non-employed month (63, table iv, all persistent exits; 100-replication cluster bootstrap s.e. from 63).
  psid_wexit_repeat2 (reported): share of PSID couples with an annual exit (hours > 0 in t, 0 in t+1, same couple,
    husband working both years, annual years 1968-1996) that have two or more (63, v-repeat; binomial s.e.).
ext = her_sep (separation hazard after HER displacement; evidence proposals/separation_ui_evidence.md, IGE/64/65)
  psid_es_bh_present_13 (target), psid_es_bh_present_46 (reported): 'still with the baseline husband', mean of the
    event-time coefficients e = +1..+3 (+4..+6) after her first displacement, 64's M3 design (wives of male heads,
    baseline with a child 0-17 and positive own hours; clean controls not displaced to ev + 6; person x stack and year
    x stack FE; reference e = -2; events 1984-2021, outcome years <= 2021), the attrition-equalised variant of IGE/65
    Section 5b (both groups observed at the first interview after ev; the model has no attrition), pooled over races.
    Standard errors: 65's CR1 s.e. clustered by 1968 family (65 has no bootstrap for this design).

Run from the repository root: .venv/Scripts/python.exe -I IGE/66.PaperATargetsExt.py [--scratch DIR] [--reps 200]
(--scratch: 63's scratch folder with sipp_wife_jobs.pkl; it is rebuilt there from the raw SIPP files if missing).
"""
import argparse
import importlib.util
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import numpy as np                            # noqa: E402
import pandas as pd                           # noqa: E402

from common import OUT                        # noqa: E402

T0 = time.time()
COLS = ["block", "moment", "value", "se", "n", "window", "source_script", "definition", "id", "p", "stars",
        "data_source", "target", "n_events", "reps_ok", "ext"]


def log(*a):
    print(f"[{time.time() - T0:7.0f}s]", *a, flush=True)


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def sipp_sample(m63, scratch, workers):
    """63's SIPP persistent-exit sample (sipp_part, lines up to the cells), returned as arrays: y, weight, tenure,
    household cluster."""
    m40 = m63._load("sipp40", "40.SIPPJointLoss.py")
    cache = scratch / "sipp_wife_jobs.pkl"
    if cache.exists():
        J = pd.read_pickle(cache)
    else:
        J = m63.sipp_slots(scratch, workers)
        J.to_pickle(cache)
    P = m40.build_panel()
    P, L = m40.add_vars(P)
    J = J.rename(columns={"pnum": "pnum_w"})
    J["ssuid"] = J["ssuid"].astype(str)
    P["ssuid"] = P["ssuid"].astype(str)
    P = P.merge(J, on=["panel", "ssuid", "pnum_w", "ym"], how="left")
    assert P.duplicated(["cid", "ym"]).sum() == 0
    L = m40.Look(P)
    P["tenure"] = P["tenure"].astype(float)
    E = {k: L.at("E_w", k) for k in range(-1, 3)}
    Eh = {k: L.at("E_h", k) for k in (0, 1)}
    age = P.age_w.between(25, 59).to_numpy()
    base = (E[-1] == 1) & (E[0] == 1) & (Eh[0] == 1) & (Eh[1] == 1) & np.isfinite(E[1]) & np.isfinite(E[2]) & age
    y = ((E[1] == 0) & (E[2] == 0)).astype(float)
    d = P.loc[base]
    return dict(y=y[base], w=np.nan_to_num(d.wgt_w.to_numpy(float)), ten=d.tenure.to_numpy(float),
                hh=d.hh.to_numpy())


def tenure_hazards(S, reps, seed=66):
    ten = S["ten"]
    known = np.isfinite(ten) & (ten >= 0)
    bins = {"0_5": known & (ten < 6), "6_11": known & (ten >= 6) & (ten < 12), "12p": known & (ten >= 12)}
    g, gu = pd.factorize(S["hh"])
    G = len(gu)
    w, y = S["w"], S["y"]
    num = np.column_stack([np.bincount(g, weights=np.where(mk, w * y, 0.0), minlength=G) for mk in bins.values()])
    den = np.column_stack([np.bincount(g, weights=np.where(mk, w, 0.0), minlength=G) for mk in bins.values()])
    est = num.sum(0) / den.sum(0)
    rng = np.random.default_rng(seed)
    draws = []
    for _ in range(reps):
        cnt = np.bincount(rng.integers(0, G, G), minlength=G).astype(float)
        draws.append((cnt @ num) / (cnt @ den))
    D = np.array(draws)
    se = D.std(axis=0, ddof=1)
    V = np.cov(D.T)
    n = [int(mk.sum()) for mk in bins.values()]
    nev = [int((mk & (y == 1)).sum()) for mk in bins.values()]
    return list(bins), est, se, V, n, nev, G


def row(**kw):
    r = {c: np.nan for c in COLS}
    r.update(kw)
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", default=str(Path(tempfile.gettempdir()) / "ige63_scratch"))
    ap.add_argument("--reps", type=int, default=200)
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()
    scratch = Path(a.scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    assert HERE.parent not in scratch.resolve().parents, "scratch must be outside the repository"
    rows = []
    # ---------------- new_job: SIPP exit hazard by job tenure ----------------
    m63 = _load("ige63", "63.WifeExitWhy.py")
    log("SIPP: rebuilding 63's persistent-exit sample")
    S = sipp_sample(m63, scratch, a.workers)
    log(f"SIPP: {len(S['y']):,} wife-months, pooled exit {np.sum(S['w'] * S['y']) / np.sum(S['w']):.5f}")
    names, est, se, V, n, nev, G = tenure_hazards(S, a.reps)
    lab = {"0_5": "0-5", "6_11": "6-11", "12p": "12 or more"}
    defin = ("63's SIPP sample: married wives 25-59, employed at t-1 and t, husband employed at t and t+1, all four "
             "months observed; exit = not employed (no job in any week) at t+1 and t+2, all reasons incl. involuntary; "
             "tenure at t = months since the employer-specific start date (TSJDATE 2004/08; start year/month 2014; "
             "first month seen otherwise); unknown tenure dropped; wife's weight; cluster (household) bootstrap s.e. "
             f"({a.reps} replications, {G:,} clusters). Model: tenure = months since the start of the current "
             "employment spell (no job-to-job moves in the model); spells running since entry count as unknown "
             "unless 12+ months old.")
    for k, v, s_, nn, ne in zip(names, est, se, n, nev):
        rows.append(row(block="Her exits by tenure", moment=f"Persistent monthly exit of wives, job tenure "
                        f"{lab[k]} months", value=v, se=s_, n=nn, window="SIPP 2003-2016",
                        source_script="IGE/66 (IGE/63 sample)", definition=defin, id=f"sipp_wexit_ten_{k}",
                        data_source="sipp", target=1, n_events=ne, reps_ok=a.reps, ext="new_job"))
        log(f"  tenure {lab[k]:>10}: {100 * v:.3f}% (bootstrap s.e. {100 * s_:.3f}; {nn:,} wife-months, {ne} exits)")
    pd.DataFrame(V, index=[f"sipp_wexit_ten_{k}" for k in names],
                 columns=[f"sipp_wexit_ten_{k}" for k in names]).to_csv(OUT / "paperA_targets_ext_vcov_sipp.csv")
    W = pd.read_csv(OUT / "wife_exit_why.csv")
    km = W[(W.dataset == "SIPP") & (W.table == "iv") & (W["sample"] == "persistent exits: all") &
           (W.cell == "return within 12 months")].iloc[0]
    rows.append(row(block="Her exits by tenure", moment="Back in work within 12 months of a persistent exit "
                    "(Kaplan-Meier)", value=km.coef / 100, se=km.se / 100, n=km.n, window="SIPP 2003-2016",
                    source_script="IGE/63", definition="63 table (iv): KM probability of a return to employment within "
                    "12 months of the first non-employed month t+1, censored at the end of the couple's observation; "
                    "100-replication cluster bootstrap s.e. Model: same KM in the three SIPP windows. Reported only.",
                    id="sipp_wexit_return12", data_source="sipp", target=0, ext="new_job"))
    rp = W[(W.dataset == "PSID") & (W.table == "v-repeat") & (W["sample"] == "couples with at least one exit")].iloc[0]
    p_ = rp.coef / 100
    rows.append(row(block="Her exits by tenure", moment="Share of couples with an annual exit that have two or more",
                    value=p_, se=np.sqrt(p_ * (1 - p_) / rp.n), n=rp.n, window="PSID 1968-1996",
                    source_script="IGE/63", definition="63 (v-repeat): annual exit = wife's hours > 0 in t and 0 in "
                    "t+1, same couple, husband working both years, wife 25-59, annual years (t+1 <= 1996); share of "
                    "couples with >= 1 exit that have >= 2 (mean 7.1 eligible years per couple); binomial s.e. Model: "
                    "same rule on income years 1984-1996 (the simulation starts in 1984). Reported only.",
                    id="psid_wexit_repeat2", data_source="psid", target=0, ext="new_job"))
    # ---------------- her_sep: still with baseline husband after her displacement ----------------
    H = pd.read_csv(OUT / "her_loss_robustness.csv")
    h = H[(H.block == "5b observed at reporting interview") & (H.outcome == "bh_present") & (H.group == "all")]
    for term, rid, tgt in (("mean 1-3", "psid_es_bh_present_13", 1), ("mean 4-6", "psid_es_bh_present_46", 0)):
        x = h[h.term == term].iloc[0]
        yrs = "1-3" if tgt else "4-6"
        rows.append(row(block="Separation after her loss", moment=f"Still with the baseline husband, years {yrs} "
                        "after her displacement (both groups observed at the first interview after ev)",
                        value=x.coef, se=x.se, n=x.n, window="PSID 1984-2021", source_script="IGE/65 (IGE/64 M3)",
                        definition="64's M3 design: wives of male heads with a child 0-17 and positive own hours at "
                        "baseline, first displaced (closure or layoff/firing; wife's and female head's reports) in ev "
                        "vs clean controls (not displaced to ev+6); person x stack and year x stack FE; reference "
                        "e = -2; events 1984-2021, outcome years <= 2021; 65 Section 5b: treated and controls both "
                        "observed at the first interview >= ev (attrition equalised); pooled races; CR1 s.e. clustered "
                        f"by 1968 family. Mean of e = +{yrs.replace('-', '..+')}. "
                        + ("Target." if tgt else "Reported only."),
                        id=rid, p=x.p, stars=("***" if x.p < 0.01 else "**" if x.p < 0.05 else "*" if x.p < 0.1
                                              else ""), data_source="psid", target=tgt, n_events=x.treated,
                        ext="her_sep"))
        log(f"  {rid}: {x.coef:.4f} (s.e. {x.se:.4f}; {int(x.treated)} displaced wives)")
    D = pd.DataFrame(rows)[COLS]
    D.to_csv(OUT / "paperA_targets_ext.csv", index=False)
    log(f"wrote {OUT / 'paperA_targets_ext.csv'} ({len(D)} rows) and paperA_targets_ext_vcov_sipp.csv")


if __name__ == "__main__":
    main()
