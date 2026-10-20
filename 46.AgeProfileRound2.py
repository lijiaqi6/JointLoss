r"""Paper B, Fable round-2 review items A5, A6, A8 (proposals/fable_review_paperB.md, 2026-10-18).

  A5  EXPERIENCE CLOCK. White sons of richer parents enter the labor market later, so at 25-29 they may be compared
      with Black sons who have more experience. (i) The White - Black gap in the log IGE by bands of POTENTIAL
      EXPERIENCE (age - completed years of schooling - 6; 0-4, 5-9, 10-14, 15-19, 20-24; child-years at ages 20-55 as
      head or spouse), opening = mean gap at >= 10 years minus mean gap at < 10 years; (ii) the age profile starting at
      27 (child-years at 25-26 dropped, when many sons of richer parents are still in school). PSID, sons, ln own
      earnings and ln family income; 33's design (A quartic, single-year age dummies; for (i) also single-year
      experience dummies instead of age dummies). Completed schooling = maximum over the son's waves (24's educ).
  A6  RELIABILITY RATIOS SPECIFIC TO EACH DATA SET. The one-year three-data-set openings of 41 (PSID one year at 12-16,
      NLSY79 1978, NLSY97 1996; bands 25-44) divided race by race by each data set's own child-generation reliability
      ratio of one year of family income (4.Estimates.py: PSID W 0.585 (0.010) B 0.565 (0.012); NLSY79 W 0.552 (0.014)
      B 0.556 (0.017); NLSY97 W 0.430 (0.013) B 0.492 (0.020)), with the ratios' sampling error propagated (delta
      method; Black and White families are disjoint, so the race-specific changes are independent); inverse-variance
      pooled with Cochran's Q.
  A8  NLSY79 CHILDREN AND YOUNG ADULTS, a fourth public data set with multi-year parental income. Children of the
      NLSY79 White and Black mothers (10.CYAOutcomes.py sample); child's wage and salary income of the previous year
      (YA Q15-5, 2000 $, $100-$150,000 of 1967 in 2000 $) at each YA interview, by age at interview 25-29 ... 40-44;
      parental income = the mother's NLSY79 family income (TNFI_TRUNC) averaged over the calendar years in which the
      child is 13-19 (>= 3 years), and alternatively one year (the year nearest child age 14 within 12-16) on the same
      children; A = mother's age when the child is 16. Race = the mother's race; clusters = mother. The sample is
      selected: children born to NLSY79 mothers by 1980 (who reach 40) had young mothers.
DESIGN: 33's stacked band x race regressions (Cells engine, joint cluster-robust covariance), gap = White - Black.
Writes output/age_profile_round2.csv and .md.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2, norm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import DATA, OUT, stars, to2000  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R33 = _load("ige33", "33.AgeProfileRobustness.py")
ige6 = R33.ige6
A4, GC, RACES = R33.A4, R33.GC, R33.RACES
FAM, ERN = R33.FAM, R33.ERN
OUTS = [("learn", ERN), ("lfam", FAM)]
prep, run, summarize, diff = R33.prep, R33.run, R33.summarize, R33.diff
ROWS = R33.ROWS
EXTRA = []
EXPB = [(0, 4), (5, 9), (10, 14), (15, 19), (20, 24)]
EXPL = [f"exp {a}-{b}" for a, b in EXPB]


def cell(e, se, p, dec=3):
    if e is None or not np.isfinite(e):
        return ""
    pv = "<0.001" if p < 0.001 else f"{p:.3f}"
    return f"{e:.{dec}f}{stars(p)} ({se:.{dec}f}; p={pv})"


def with_bands(labels, mids, fn):
    """run fn with 33's band globals replaced (summarize / tests read them at call time)."""
    old = R33.BL, R33.BL4, R33.MID
    R33.BL, R33.BL4, R33.MID = labels, labels[:4], mids
    try:
        fn()
    finally:
        R33.BL, R33.BL4, R33.MID = old


# ================================================================ A5
def a5():
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    s = ige6.build(py)
    a = pd.read_pickle(DATA / "ige_decomposition_panel.pkl")
    ed = a.dropna(subset=["educ"]).groupby("pid")["educ"].max()
    s["educ"] = s["pid"].map(ed)
    s = s[(s["female"] == 0) & s["race"].isin(RACES)].copy()
    s["agei"] = s["age"].round().astype(int)
    s["exp"] = s["age"] - np.maximum(s["educ"], 8) - 6
    s["expi"] = s["exp"].round()
    # (i) experience bands
    e = s[s["age"].between(20, 55) & s["exp"].between(0, 24)].copy()
    e["band"] = pd.cut(e["exp"], [-0.5, 4.5, 9.5, 14.5, 19.5, 24.5], labels=EXPL).astype(object)
    mids = dict(zip(EXPL, [27, 32, 37, 42, 47]))                     # < 35 <=> experience < 10
    for y, ylab in OUTS:
        fr = {"Experience bands (age dummies)": prep(e, y, "lyp"),
              "Experience bands (experience dummies)": prep(e.assign(agei=e["expi"].astype(int)), y, "lyp")}
        R = run(fr, A4)
        with_bands(EXPL, mids, lambda: [summarize(R, "PSID", "experience", sp, "Sons", ylab) for sp in fr])
        print(f"A5 experience {ylab} done", flush=True)
    # (ii) age profile from 27
    g = s[s["age"].between(25, 49)].copy()
    g["band"] = R33.band_of(g["age"])
    for y, ylab in OUTS:
        fr = {"Ages 25-49 (33)": prep(g, y, "lyp"), "Ages 27-49 (25-26 dropped)": prep(g[g["age"] >= 27], y, "lyp")}
        R = run(fr, A4)
        for sp in fr:
            summarize(R, "PSID", "start27", sp, "Sons", ylab)
        diff(R, "PSID", "start27", "Ages 27-49 (25-26 dropped)", "Ages 25-49 (33)", "Sons", ylab)
    # schooling and experience at 25-29 by race and parental tercile (the composition behind (i))
    z = g[g["band"] == "25-29"].drop_duplicates("pid")
    q = z["lyp"].quantile([1 / 3, 2 / 3]).to_numpy()
    z = z.assign(terc=np.digitize(z["lyp"], q) + 1)
    for (r_, t_), w in z.groupby(["race", "terc"]):
        EXTRA.append(dict(block="exp_desc", group=r_, spec=f"tercile {t_}", stat="mean schooling / experience at 25-29",
                          est=w["educ"].mean(), se=(w["age"] - np.maximum(w["educ"], 8) - 6).mean(), n=len(w)))


# ================================================================ A6
RR = {"PSID": {"White": (0.585135, 0.010395), "Black": (0.565207, 0.011628)},
      "NLSY79": {"White": (0.552274, 0.013791), "Black": (0.556168, 0.016997)},
      "NLSY97": {"White": (0.429901, 0.013076), "Black": (0.491773, 0.020476)}}
ONE = {"PSID": "PSID: one year at 12-16", "NLSY79": "NLSY79: 1978 one year", "NLSY97": "NLSY97: 1996 one year"}


def a6():
    m = pd.read_csv(OUT / "age_profile_measurement.csv", low_memory=False)
    m = m[(m["table"] == "band") & (m["block"] == "corrected") & (m["band"] == "test") & (m["stat"] == GC)
          & (m["bandset"] == "25-44") & (m["sex"] == "Sons")]
    for _, ylab in OUTS:
        vals = {}
        for dt, sp in ONE.items():
            x = m[(m["data"] == dt) & (m["spec"] == sp) & (m["outcome"] == ylab)].set_index("group")
            cW, sW = x.loc["White", "est"], x.loc["White", "se"]
            cB, sB = x.loc["Black", "est"], x.loc["Black", "se"]
            (rW, srW), (rB, srB) = RR[dt]["White"], RR[dt]["Black"]
            est = cW / rW - cB / rB
            se = np.sqrt((sW / rW) ** 2 + (sB / rB) ** 2 + (cW * srW / rW ** 2) ** 2 + (cB * srB / rB ** 2) ** 2)
            raw = x.loc["White - Black", "est"]
            vals[dt] = (est, se)
            EXTRA.append(dict(block="rr_own", data=dt, outcome=ylab, stat="corrected gap change (own RR)", est=est,
                              se=se, p=2 * norm.sf(abs(est / se)), raw=raw, raw_se=x.loc["White - Black", "se"],
                              chk_se=np.hypot(sW, sB), rrW=rW, rrB=rB))
        w = {k: 1 / v[1] ** 2 for k, v in vals.items()}
        e = sum(w[k] * vals[k][0] for k in vals) / sum(w.values())
        se = 1 / np.sqrt(sum(w.values()))
        qq = sum(w[k] * (vals[k][0] - e) ** 2 for k in vals)
        EXTRA.append(dict(block="rr_own", data="Pooled", outcome=ylab, stat="corrected gap change (own RR)", est=e,
                          se=se, p=2 * norm.sf(abs(e / se)), note=f"Q={qq:.2f}, p={1 - chi2.cdf(qq, 2):.3f}"))


# ================================================================ A8
def cya_frames():
    R10 = _load("c10", "10.CYAOutcomes.py")
    ix, v, raw, inc = R10.read_raw(True)
    cid = raw[v["child"]["CPUBID"]].values
    rows = []
    for y in sorted(v["ya_age"]):
        age = pd.to_numeric(raw[v["ya_age"][y]], errors="coerce").to_numpy(float)
        age[age <= 0] = np.nan
        if y not in v["ya_wage"]:
            continue
        wage = R10.nls_money(raw[v["ya_wage"][y]]).to_numpy(float)
        rows.append(pd.DataFrame({"cid": cid, "round": y, "age": age, "earn": to2000(wage, y - 1)}))
    L = pd.concat(rows, ignore_index=True)
    L = L[L["age"].between(25, 44)]
    k = pd.read_pickle(DATA / "cya_children.pkl")[["cid", "mid", "cyrb", "csex", "race", "magebir", "m_wt79"]]
    I = inc.set_index("id")
    I = I.apply(R10.nls_money)
    yrs = {int(c[4:]) - 1: c for c in I.columns}
    lo, hi = ige6.LO, ige6.HI
    par = []
    for _, r in k.iterrows():
        if r["mid"] not in I.index or not np.isfinite(r["cyrb"]):
            continue
        vals = {}
        for a in range(12, 20):
            t = int(r["cyrb"]) + a
            if t in yrs:
                z = I.at[r["mid"], yrs[t]]
                if z == z:
                    z = to2000(z, t)
                    if lo <= z <= hi:
                        vals[a] = z
        m1319 = [z for a, z in vals.items() if a >= 13]
        one = sorted(((abs(a - 14), a, z) for a, z in vals.items() if 12 <= a <= 16))
        par.append(dict(cid=r["cid"], y1319=np.mean(m1319) if len(m1319) >= 3 else np.nan, n1319=len(m1319),
                        y1=one[0][2] if one else np.nan))
    par = pd.DataFrame(par)
    s = L.merge(k, on="cid").merge(par, on="cid")
    s["lyp"], s["ly1"] = np.log(s["y1319"]), np.log(s["y1"])
    s["learn"] = np.log(s["earn"].where(s["earn"].between(lo, hi)))
    A = s["magebir"] + 16
    for n in range(1, 5):
        s[f"A{n}"] = ((A - 45) / 10) ** n
    s["agei"] = s["age"].round().astype(int)
    s["band"] = R33.band_of(s["age"])
    s["pid"], s["fam68"] = s["cid"], s["mid"]
    s["race"] = s["race"].astype(str)
    return s


def a8():
    s = cya_frames()
    for sex, cs in (("Sons", 1), ("Daughters", 2)):
        x = s[s["csex"] == cs]
        both = x[x["lyp"].notna() & x["ly1"].notna()]
        fr = {"CYA: mother's income at 13-19": prep(x, "learn", "lyp"),
              "CYA: 13-19 mean, same children as one year": prep(both, "learn", "lyp"),
              "CYA: one year at 12-16": prep(both, "learn", "ly1")}
        R = run(fr, A4)
        for sp in fr:
            summarize(R, "CYA", "cya", sp, sex, ERN)
        diff(R, "CYA", "cya", "CYA: one year at 12-16", "CYA: 13-19 mean, same children as one year", sex, ERN)
        for b in R33.BL4:
            for g in RACES:
                z = x[(x["band"] == b) & (x["race"] == g) & x["learn"].notna() & x["lyp"].notna()]
                EXTRA.append(dict(block="cya_n", sex=sex, band=b, group=g, stat="child-years / children", est=len(z),
                                  se=z["cid"].nunique()))
        print(f"A8 {sex} done", flush=True)
    kk = s.drop_duplicates("cid")
    for g in RACES:
        z = kk[kk["race"] == g]
        EXTRA.append(dict(block="cya_desc", group=g, stat="children with earnings at 25-44 / mean birth year / mean "
                                                             "mother's age at birth", est=len(z), se=z["cyrb"].mean(),
                          n=z["magebir"].mean()))


# ================================================================ output
def G(res, *k):
    return res.get(k)


def c_(r):
    return "" if r is None else cell(r["est"], r["se"], r["p"])


def write_md(res, ex):
    L = ["# Paper B age profile, Fable round 2: experience clock, own reliability ratios, NLSY79 children (A5 A6 A8)",
         "", "Generated by `46.AgeProfileRound2.py` (2026-10-18). Every cell: estimate (s.e.; p), *** p<0.01, ** p<0.05, "
         "* p<0.1; clusters 1968 family (PSID) / mother (CYA); stacked band x race regressions of 33. Gap = White - "
         "Black log IGE; opening = mean gap in the later bands minus mean gap in the earlier bands.", ""]
    for blk, title, bands, specs in (
            ("experience", "A5 (i). By potential experience (opening = >= 10 years minus < 10 years)", EXPL,
             ["Experience bands (age dummies)", "Experience bands (experience dummies)"]),
            ("start27", "A5 (ii). Age profile starting at 27", R33.BL,
             ["Ages 25-49 (33)", "Ages 27-49 (25-26 dropped)"])):
        L += [f"## {title}", "", "| | " + " | ".join(f"({i + 1}) Sons: {o}" for i, (_, o) in enumerate(OUTS)) + " |",
              "|---|---|---|"]
        for sp in specs:
            L.append(f"| **{sp}** | | |")
            for b in bands:
                L.append(f"| W - B gap, {b} | " + " | ".join(c_(G(res, "PSID", blk, sp, "Sons", o, b, "White - Black",
                                                               "IGE", "")) for _, o in OUTS) + " |")
            for g in ("Black", "White", "White - Black"):
                L.append(f"| {g}: opening | " + " | ".join(c_(G(res, "PSID", blk, sp, "Sons", o, "test", g, GC,
                                                              "25-49")) for _, o in OUTS) + " |")
            if blk == "start27" and sp.startswith("Ages 27"):
                L.append("| Opening minus [Ages 25-49 (33)] | " + " | ".join(c_(G(
                    res, "PSID", blk, sp, "Sons", o, "test", "White - Black", "Gap change minus [Ages 25-49 (33)]",
                    "25-49")) for _, o in OUTS) + " |")
            L.append("| Child-years by band (B; W) | " + " | ".join(
                "B " + "/".join(f"{int(r['nB']):,}" for r in rs if r is not None) + "; W "
                + "/".join(f"{int(r['nW']):,}" for r in rs if r is not None)
                for rs in [[G(res, "PSID", blk, sp, "Sons", o, b, "White - Black", "IGE", "") for b in bands]
                           for _, o in OUTS]) + " |")
        L.append("")
    L += ["Mean completed schooling (and potential experience) at 25-29 by race and pooled parental tercile:", "",
          "| Race | tercile | sons | mean schooling | mean potential experience |", "|---|---|---|---|---|"]
    for r in ex:
        if r["block"] == "exp_desc":
            L.append(f"| {r['group']} | {r['spec']} | {r['n']:,} | {r['est']:.2f} | {r['se']:.2f} |")
    L += ["", "## A6. Three data sets, each corrected by its own reliability ratio (sons, bands 25-44, one year of "
          "parental income)", "", "| | raw opening | own ratios (W / B) | corrected opening |", "|---|---|---|---|"]
    for _, o in OUTS:
        L.append(f"| **{o}** | | | |")
        for r in ex:
            if r["block"] == "rr_own" and r["outcome"] == o:
                if r["data"] == "Pooled":
                    L.append(f"| Pooled (inverse variance) | | | {cell(r['est'], r['se'], r['p'])}; {r['note']} |")
                else:
                    praw = 2 * norm.sf(abs(r["raw"] / r["raw_se"]))
                    L.append(f"| {r['data']} | {cell(r['raw'], r['raw_se'], praw)} | {r['rrW']:.3f} / {r['rrB']:.3f} | "
                             f"{cell(r['est'], r['se'], r['p'])} |")
    L += ["", "## A8. NLSY79 Children and Young Adults: earnings IGE by age, mother's multi-year income", "",
          "| | (1) Sons | (2) Daughters |", "|---|---|---|"]
    for sp in ("CYA: mother's income at 13-19", "CYA: 13-19 mean, same children as one year", "CYA: one year at 12-16"):
        L.append(f"| **{sp}** | | |")
        for b in R33.BL4:
            L.append(f"| W - B gap, {b} | " + " | ".join(c_(G(res, "CYA", "cya", sp, sx, ERN, b, "White - Black", "IGE",
                                                             "")) for sx in ("Sons", "Daughters")) + " |")
        for g in ("Black", "White"):
            for b in R33.BL4:
                L.append(f"| {g} IGE, {b} | " + " | ".join(c_(G(res, "CYA", "cya", sp, sx, ERN, b, g, "IGE", ""))
                                                          for sx in ("Sons", "Daughters")) + " |")
        for bs in ("25-44",):
            L.append(f"| **Opening (bands {bs})** | " + " | ".join(c_(G(res, "CYA", "cya", sp, sx, ERN, "test",
                                                                      "White - Black", GC, bs))
                                                                for sx in ("Sons", "Daughters")) + " |")
    L.append("| One year minus 13-19 mean (same children) | " + " | ".join(c_(G(
        res, "CYA", "cya", "CYA: one year at 12-16", sx, ERN, "test", "White - Black",
        "Gap change minus [CYA: 13-19 mean, same children as one year]", "25-44")) for sx in ("Sons", "Daughters"))
        + " |")
    L += ["", "| Band | Sons B | Sons W | Daughters B | Daughters W |", "|---|---|---|---|---|"]
    for b in R33.BL4:
        cs = []
        for sx in ("Sons", "Daughters"):
            for g in RACES:
                r = next((r for r in ex if r["block"] == "cya_n" and r["sex"] == sx and r["band"] == b
                          and r["group"] == g), None)
                cs.append("" if r is None else f"{int(r['est']):,} / {int(r['se']):,}")
        L.append(f"| {b} | " + " | ".join(cs) + " |")
    for r in ex:
        if r["block"] == "cya_desc":
            L.append(f"\n- {r['group']}: {int(r['est']):,} children with earnings at 25-44; mean birth year "
                     f"{r['se']:.1f}; mean mother's age at birth {r['n']:.1f}")
    (OUT / "age_profile_round2.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def main():
    a5()
    a6()
    a8()
    res = pd.DataFrame(ROWS)
    resd = {}
    for r in res.to_dict("records"):
        resd[tuple("" if (isinstance(r.get(k), float) and np.isnan(r.get(k))) else r.get(k, "") for k in R33.KEYS)] = r
    OUT.mkdir(exist_ok=True)
    pd.concat([res.assign(table="band"), pd.DataFrame(EXTRA).assign(table="extra")], ignore_index=True).to_csv(
        OUT / "age_profile_round2.csv", index=False)
    write_md(resd, EXTRA)
    print("done", flush=True)


if __name__ == "__main__":
    main()
