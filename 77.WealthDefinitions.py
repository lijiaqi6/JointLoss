r"""Wealth definitions for Paper A's wealth targets: is the age shape a model problem or a definition problem? [Paper A]
(2026-10-20, WP4 of proposals/fable_10h_plan_paperA.md)

QUESTION
  The model's single asset (paperA_model/model.py) is annuitised at the wife's 60 into the terminal value (240
  months, plus social security at 40% of the couple's mean wage), so it holds all retirement saving. The SMM targets
  psid_liq_le0_* / psid_liq_hi_* (IGE/60) use liquid wealth only. This script recomputes the two target statistics
  (share <= 0, share above one year of the couple's labor income) and the median under broader definitions, on the
  same couples, the same waves and the same earnings denominator as IGE/60.

SAMPLE (identical to IGE/60's wealth block)
  IGE/60's cached PSID men panel (data/paperA_targets_psid.pkl, read only; IGE/60 is not run): male heads,
  Black or White (head's race), wife present (w_pid), wife aged 25-59 at the wealth interview; PSID wealth waves
  1984, 1989, 1994, 1999-2019 (the 2021 wave is not in estimation/psid_wealth.py, as for the target). Earnings
  denominator = head's + wife's labor income (2000 $) of the income year before the interview, missing = 0 (IGE/60).
DEFINITIONS (PSID imputed components, 2000 $ = nominal / cpi x 5.82 as in IGE/60)
  (a) liquid, as targeted: checking / savings (+ bonds / CDs from 2019) + stocks - unsecured debt
      (estimation/psid_wealth.py, imported read only). In 1984-1994 the stock question includes stocks held in IRAs.
  (b) liquid + IRAs / private annuities (IMP VALUE ANNUITY/IRA; recorded separately from 1999 only)
  (c) net worth excluding home equity (PSID WEALTH1: (a) + IRAs + business / farm + other real estate + vehicles +
      other assets - other debt is already in (a))
  (c') (c) minus vehicles: financial + business + other real estate wealth
  (d) net worth (PSID WEALTH2 = (c) + home equity)
  Employer pensions (DB and 401(k)-type DC accounts) are in none of these: the PSID wealth totals exclude them.
  Home ownership (family file 'OWN/RENT OR WHAT' = 1) and mortgage ('HAVE MORTGAGE?' = 1) shares by band.
PANELS
  1984-2019 (the target's years): (a), (c), (c'), (d). 1999-2019 (matched years for (b)): (a), (b), (c), (c'), (d).
STATISTICS
  By wife's age band (25-34, 35-44, 45-59) x race (all, Black, White; head's race): N, share <= 0, share above one
  year of earnings, P25 / median / P75 (2000 $), median wealth / earnings (couples with earnings > 0). Unweighted
  (as the target). Shares and differences from (a) on the same couple-waves (and Black - White): block bootstrap over
  1968 families, 200 replications (cluster draw counts as weights, as IGE/60); p from the normal approximation;
  *** p<0.01, ** p<0.05, * p<0.1. Descriptive (no causal claim).
OUTPUTS (aggregates only; no person-level file is written)
  output/wealth_definitions.csv, output/wealth_definitions_diffs.csv, output/wealth_definitions.md
Run from the repo root: .venv/Scripts/python.exe -I IGE/77.WealthDefinitions.py [--reps 200]
"""
import os

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")

import argparse                               # noqa: E402
import re                                     # noqa: E402
import sys                                    # noqa: E402
import time                                   # noqa: E402
from pathlib import Path                      # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import numpy as np                            # noqa: E402
import pandas as pd                           # noqa: E402
from scipy.stats import norm                  # noqa: E402

from common import DATA, OUT                  # noqa: E402
from estimation import psid_wealth as PW      # noqa: E402

CACHE_PSID = DATA / "paperA_targets_psid.pkl"
TO2000 = 5.82
BANDS = ((25, 34), (35, 44), (45, 59))
RACES = ("All", "Black", "White")
DEFS = {"a": "(a) liquid (target)", "b": "(b) liquid + IRA/annuity", "c": "(c) net worth excl. home equity",
        "cv": "(c') (c) minus vehicles", "d": "(d) net worth"}
T0 = time.time()


def log(*a):
    print(f"[{time.time() - T0:6.0f}s]", *a, flush=True)


def stars(p):
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""


def fam_folder(wave):
    return {1984: "fam1984", 1989: "fam1989"}.get(wave, f"fam{wave}er")


def first_var(order, labels, pattern):
    rx = re.compile(pattern)
    return next((v for v in order if rx.search(labels.get(v, "").strip().upper())), None)


def read_cols(do_file, cols_fn):
    order, pos = PW._layout(do_file)
    labels = dict(re.findall(r'label variable\s+(\S+)\s+"([^"]*)"', do_file.read_text(encoding="latin-1"), re.I))
    cols = cols_fn(order, labels)
    keep = [c for c in dict.fromkeys(cols) if c is not None]
    f = pd.read_fwf(do_file.with_suffix(".txt"), colspecs=[pos[c] for c in keep], names=keep, header=None,
                    encoding="latin-1")
    return f, cols, labels


def extras():
    """Per (wave, interview number): vehicles, home equity, IRA / annuity value (nominal / cpi, the units of
    psid_wealth.py), owner and mortgage indicators."""
    cpi = pd.read_stata(PW.TEMP / "cpi.dta", convert_categoricals=False).set_index("year")["cpi"]
    parts = []
    for wave, (folder, label, *_) in PW.WAVES.items():
        do_w = [p for p in (PW.FAM / folder).glob("*.do") if "formats" not in p.name.lower()][0]
        f, (iv, veh, heq, ira), lab = read_cols(do_w, lambda o, L: [o[1], first_var(o, L, r"^IMP VALUE VEHICLES"),
                                                                   first_var(o, L, r"^IMP VALUE HOME EQUITY"),
                                                                   first_var(o, L, r"^IMP VALUE ANNUITY/IRA")])
        w = pd.DataFrame({"wave": wave, "int": f[iv], "veh": f[veh] / cpi[label], "heq": f[heq] / cpi[label],
                          "ira": (f[ira] / cpi[label]) if ira else np.nan})
        do_f = [p for p in (PW.FAM / fam_folder(wave)).glob("*.do") if "formats" not in p.name.lower()][0]
        g, (iv2, own, mort), lab2 = read_cols(do_f, lambda o, L: [o[1], first_var(o, L, r"OWN/RENT OR WHAT"),
                                                                  first_var(o, L, r"HAVE MORTGAGE\?")])
        h = pd.DataFrame({"int": g[iv2], "own": (g[own] == 1).astype(float), "mort": (g[mort] == 1).astype(float)})
        w = w.merge(h, on="int", how="left")
        log(f"  {wave}: id {iv} '{lab.get(iv, '').strip()}', veh {veh}, heq {heq}, ira {ira}; family {fam_folder(wave)}"
            f" id {iv2} '{lab2.get(iv2, '').strip()}', own {own}, mortgage {mort}; {len(w):,} families, "
            f"{w['own'].notna().mean():.3f} matched")
        parts.append(w)
    return pd.concat(parts, ignore_index=True)


def build():
    if not CACHE_PSID.exists():
        sys.exit(f"{CACHE_PSID} missing: it is written by IGE/60 (not run here).")
    m = pd.read_pickle(CACHE_PSID)["m"]
    log("psid_wealth.family_wealth()")
    W = PW.family_wealth()
    lab2wave = {lab: w for w, (_, lab, *_) in PW.WAVES.items()}
    W["wave"] = W["year"].map(lab2wave)
    W = W.drop(columns="year")
    log("extra components (vehicles, home equity, IRA, tenure, mortgage)")
    X = extras()
    wl = W.merge(m[["pid", "fam68", "wave", "int", "hrace", "w_pid", "w_age", "hlab", "wlab"]]
                 .rename(columns={"pid": "id"}), on=["id", "wave"])
    wl = wl[wl["w_pid"].notna() & wl["w_age"].between(25, 59) & wl["liquid"].notna()].copy()
    wl = wl.merge(X, on=["wave", "int"], how="left")
    wl["earn"] = wl["hlab"].fillna(0) + wl["wlab"].fillna(0)
    wl["a"] = wl["liquid"] * TO2000
    wl["b"] = (wl["liquid"] + wl["ira"]) * TO2000                     # NaN before 1999
    wl["c"] = wl["nw_noeq"] * TO2000
    wl["cv"] = (wl["nw_noeq"] - wl["veh"]) * TO2000
    wl["d"] = wl["nw"] * TO2000
    wl["heq"] = wl["heq"] * TO2000
    wl["ira_v"] = wl["ira"] * TO2000
    wl["band"] = pd.cut(wl["w_age"], [24, 34, 44, 59], labels=["25-34", "35-44", "45-59"]).astype(str)
    return wl.reset_index(drop=True)


def boot_counts(fam, reps, seed=20261020):
    codes, uniq = pd.factorize(fam)
    G = len(uniq)
    rng = np.random.default_rng(seed)
    out = np.empty((reps, len(codes)))
    for r in range(reps):
        out[r] = np.bincount(rng.integers(0, G, G), minlength=G)[codes]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=200)
    args = ap.parse_args()
    wl = build()
    log(f"{len(wl):,} couple-waves, {wl['fam68'].nunique():,} 1968 families")
    # reproduce IGE/60's targets
    chk = []
    for lo, hi in BANDS:
        q = wl[wl["w_age"].between(lo, hi)]
        chk.append(f"{lo}-{hi}: N {len(q):,}, le0 {(q['a'] <= 0).mean():.4f}, hi {(q['a'] > q['earn']).mean():.4f}")
    log("target check (IGE/60: N 14,261 / 13,814 / 15,295; le0 0.5681 / 0.4616 / 0.3810; hi 0.0344 / 0.0775 / "
        "0.1772): " + "; ".join(chk))
    Bw = boot_counts(wl["fam68"].to_numpy(np.int64), args.reps)          # reps x rows

    def bmean(y, mk):
        """Point estimate and bootstrap s.e. of the mean of y over rows mk (y may be NaN outside its sample)."""
        ok = mk & np.isfinite(y)
        est = float(y[ok].mean())
        w = Bw[:, ok]
        b = (w * y[ok]).sum(1) / w.sum(1)
        return est, float(b.std(ddof=1)), b

    rows, drows = [], []
    panels = (("1984-2019", wl["wave"] >= 0, ("a", "c", "cv", "d")),
              ("1999-2019", wl["wave"] >= 1999, ("a", "b", "c", "cv", "d")))
    E = wl["earn"].to_numpy(float)
    for pname, pm, defs in panels:
        pm = pm.to_numpy()
        for band in ("25-34", "35-44", "45-59"):
            bm = pm & (wl["band"] == band).to_numpy()
            boots = {}
            for race in RACES:
                mk = bm & ((wl["hrace"] == race).to_numpy() if race != "All" else True)
                for k in defs:
                    v = wl[k].to_numpy(float)
                    ok = mk & np.isfinite(v)
                    le0 = np.where(np.isfinite(v), (v <= 0).astype(float), np.nan)
                    hi_ = np.where(np.isfinite(v), (v > E).astype(float), np.nan)
                    e1, s1, b1 = bmean(le0, mk)
                    e2, s2, b2 = bmean(hi_, mk)
                    boots[(race, k)] = (b1, b2, e1, e2)
                    ep = ok & (E > 0)
                    rows.append(dict(panel=pname, band=band, race=race, definition=DEFS[k], key=k, n=int(ok.sum()),
                                     share_le0=e1, se_le0=s1, share_above_earn=e2, se_above_earn=s2,
                                     p25=np.percentile(v[ok], 25), median=np.median(v[ok]),
                                     p75=np.percentile(v[ok], 75), median_to_earn=np.median(v[ep] / E[ep])))
                # differences from (a) on the same couple-waves (all rows of the definition)
                a = wl["a"].to_numpy(float)
                for k in defs:
                    if k == "a":
                        continue
                    v = wl[k].to_numpy(float)
                    mm = mk & np.isfinite(v)
                    for stat, fy in (("share_le0", lambda x: (x <= 0).astype(float)),
                                     ("share_above_earn", lambda x: (x > E).astype(float))):
                        dlt = np.where(mm, fy(v) - fy(a), np.nan)
                        est, se, _ = bmean(dlt, mm)
                        p = 2 * norm.sf(abs(est / se)) if se > 0 else np.nan
                        drows.append(dict(panel=pname, band=band, race=race, contrast=f"{DEFS[k]} - (a)", stat=stat,
                                          diff=est, se=se, p=p, stars=stars(p), n=int(mm.sum())))
                # housing and IRA holding
                own = wl["own"].to_numpy(float)
                mort = wl["mort"].to_numpy(float)
                heq = wl["heq"].to_numpy(float)
                ira = wl["ira_v"].to_numpy(float)
                ow = mk & (own == 1)
                rows.append(dict(panel=pname, band=band, race=race, definition="housing / IRA", key="h",
                                 n=int(mk.sum()), own=np.nanmean(own[mk]), mortgage=np.nanmean(mort[mk]),
                                 median_home_equity_owners=np.nanmedian(heq[ow]) if ow.any() else np.nan,
                                 has_ira=float((ira[mk & np.isfinite(ira)] > 0).mean())
                                 if (mk & np.isfinite(ira)).any() else np.nan))
            # Black - White for each definition's shares
            for k in defs:
                for j, stat in ((0, "share_le0"), (1, "share_above_earn")):
                    bB, bW = boots[("Black", k)][j], boots[("White", k)][j]
                    est = boots[("Black", k)][j + 2] - boots[("White", k)][j + 2]
                    se = float((bB - bW).std(ddof=1))
                    p = 2 * norm.sf(abs(est / se)) if se > 0 else np.nan
                    drows.append(dict(panel=pname, band=band, race="Black - White", contrast=DEFS[k], stat=stat,
                                      diff=est, se=se, p=p, stars=stars(p), n=np.nan))
        log(f"panel {pname} done")
    R = pd.DataFrame(rows)
    D = pd.DataFrame(drows)
    R.to_csv(OUT / "wealth_definitions.csv", index=False)
    D.to_csv(OUT / "wealth_definitions_diffs.csv", index=False)
    write_md(R, D, wl, args.reps)
    log("written output/wealth_definitions.csv, _diffs.csv, .md")


def write_md(R, D, wl, reps):
    L = ["# Wealth definitions: PSID couples of IGE/60's wealth targets (IGE/77.WealthDefinitions.py)", "",
         f"Married couples (male head, Black or White), wife 25-59 at the wealth interview; PSID wealth waves 1984, 1989,"
         f" 1994, 1999-2019 (the target's waves); {len(wl):,} couple-waves, {wl['fam68'].nunique():,} 1968 families. "
         "2000 $. 'Above earnings' = wealth above the couple's labor income (head + wife) of the income year before "
         f"the interview (IGE/60). Unweighted. S.e. in parentheses: block bootstrap over 1968 families ({reps} "
         "replications); *** p<0.01, ** p<0.05, * p<0.1. Employer pensions (DB, 401(k)) are in no definition.", "",
         "(a) liquid as targeted = checking/savings (+ bonds/CDs 2019) + stocks - unsecured debt (stocks include IRA "
         "stocks in 1984-1994); (b) (a) + IRAs/annuities (1999+); (c) net worth excluding home equity (PSID WEALTH1); "
         "(c') (c) minus vehicles; (d) net worth (WEALTH2).", ""]

    def f(x, nd=3):
        return "" if pd.isna(x) else f"{x:.{nd}f}"

    for pname in ("1984-2019", "1999-2019"):
        for race in RACES:
            q = R[(R.panel == pname) & (R.race == race) & (R.key != "h")]
            L += [f"## {pname}, {race}", "",
                  "| band | definition | N | share <= 0 | share > 1 yr earnings | P25 | median | P75 | median / earnings |",
                  "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
            for _, r in q.iterrows():
                L.append(f"| {r.band} | {r.definition} | {r.n:,} | {f(r.share_le0)} ({f(r.se_le0)}) | "
                         f"{f(r.share_above_earn)} ({f(r.se_above_earn)}) | {r.p25:,.0f} | {r['median']:,.0f} | "
                         f"{r.p75:,.0f} | {f(r.median_to_earn, 2)} |")
            h = R[(R.panel == pname) & (R.race == race) & (R.key == "h")]
            L += ["", "| band | N | own home | mortgage | median home equity (owners) | holds IRA/annuity |",
                  "|---|---:|---:|---:|---:|---:|"]
            for _, r in h.iterrows():
                L.append(f"| {r.band} | {r.n:,} | {f(r.own)} | {f(r.mortgage)} | {r.median_home_equity_owners:,.0f} | "
                         f"{f(r.has_ira)} |")
            L.append("")
    L += ["## Differences from (a) on the same couple-waves, and Black - White", "",
          "| panel | band | race | contrast | statistic | difference (s.e.) | p |", "|---|---|---|---|---|---:|---:|"]
    for _, r in D.iterrows():
        L.append(f"| {r.panel} | {r.band} | {r.race} | {r.contrast} | {r.stat} | {r['diff']:+.3f}{r.stars} "
                 f"({r.se:.3f}) | {('<1e-15' if r.p < 1e-15 else f'{r.p:.3g}')} |")
    (OUT / "wealth_definitions.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
