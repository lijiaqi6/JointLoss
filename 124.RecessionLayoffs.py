r"""Layoffs in bad times: the father's own loss against the son's cost, and recession by recession (committee memo H4,
2026-10-24)

104: layoffs in bad times (the father's sector in national decline, or his state's unemployment a point or more above
its mean) cost the son about half as much as other layoffs (within son -0.166 vs -0.408***, p = 0.26 for equality).
Displaced workers lose more when displaced in a recession (Davis and von Wachter 2011). If bad-times layoffs cost the
FATHER more and the SON less, the son's cost does not follow the father's income loss.
(i) THE FATHER'S LOSS BY TIMES. 108's event study (father FE, calendar-year and age dummies, PSID weights, clusters
    1968 family; event = the father's first layoff in a son's teen window; event time -6 .. +6, -1 omitted), with the
    event-time dummies split by whether that first layoff fell in bad times (104's rule, at the layoff year) or not;
    ln earnings and employment; mean of event times 0 .. +6 for each and the difference.
(ii) RECESSION BY RECESSION. Each teen layoff year is assigned to the NBER recession its layoff record falls in
    (1970; 1974-75; 1980-82; 1990-91; 2001; 2008-09) or to no recession; the teen layoff share is split into the seven
    parts; within-son slope of each (91's machinery) with the numbers of treated sons, and at 45-49.
Writes output/recession_layoffs.md / .json (aggregates only). DESCRIPTIVE.
"""
import importlib.util
import json
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


R104 = _load("s104", "104.FatherPathRecession.py")
R91, R93, R75, R24 = R104.R91, R104.R93, R104.R75, R104.R24
c, dummies = R91.c, R91.dummies
COMPS, STRUCT = R91.COMPS, R91.STRUCT
REC = {"1970": [1970], "1974-75": [1974, 1975], "1980-82": [1980, 1981, 1982], "1990-91": [1990, 1991],
       "2001": [2001], "2008-09": [2008, 2009]}
RES = {}


def father_events(r, a):
    """first teen-window layoff year of each father (108) and whether it fell in bad times (104's rule)."""
    dp = pd.read_pickle(DATA / "psid_displacement.pkl")
    m = (dp["main"] == 1) & (dp["strict"] != 1)
    lay = dp.loc[m, ["pid", "year"]].rename(columns={"pid": "fpid"})
    sons = r[r["nofa"] == 0].drop_duplicates("pid")[["pid", "fpid", "birth_year"]].dropna()
    L = lay.merge(sons.assign(lo=sons["birth_year"] + 12, hi=sons["birth_year"] + 18)[["fpid", "lo", "hi"]], on="fpid")
    L = L[(L["year"] >= L["lo"]) & (L["year"] <= L["hi"])]
    ev = L.groupby("fpid")["year"].min().rename("ev").reset_index()
    S = R93.father_sector(r)[["pid", "h_sec"]].merge(sons[["pid", "fpid"]], on="pid").drop_duplicates("fpid")
    ev = ev.merge(S[["fpid", "h_sec"]], on="fpid", how="left")
    _, G = R93.ces_employment()

    def decl(s, y):
        if pd.isna(s) or int(s) not in G.columns:
            return np.nan
        x = [G.loc[t, int(s)] for t in (y, y - 1) if t in G.index]
        return float(any(v < 0 for v in x if pd.notna(v))) if x else np.nan

    ev["sec_decl"] = [decl(s, int(y)) for s, y in zip(ev["h_sec"], ev["ev"])]
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    hd = py[py["head"]][["pid", "wave", "int"]].rename(columns={"pid": "fpid"})
    st = pd.read_pickle(DATA / "husband_shocks_fam.pkl")[["wave", "int", "fips"]].drop_duplicates(["wave", "int"])
    ev = ev.assign(wave=ev["ev"] + 1).merge(hd, on=["fpid", "wave"], how="left").merge(st, on=["wave", "int"], how="left")
    ur = pd.read_pickle(DATA / "state_shocks.pkl")[["fips", "year", "ur"]]
    ur["ur_dev"] = ur["ur"] - ur.groupby("fips")["ur"].transform("mean")
    ev = ev.merge(ur.rename(columns={"year": "ev"}), on=["fips", "ev"], how="left")
    ev["st_high"] = (ev["ur_dev"] >= 1).astype(float).where(ev["ur_dev"].notna())
    ev["bad"] = np.fmax(ev["sec_decl"].fillna(0), ev["st_high"].fillna(0)).where(ev["sec_decl"].notna()
                                                                                 | ev["st_high"].notna())
    return ev[["fpid", "ev", "bad"]].drop_duplicates("fpid")


def event_by_times(r):
    a = pd.read_pickle(R24.CACHE)
    E = father_events(r, a)
    fathers = r[r["nofa"] == 0]["fpid"].dropna().unique()
    fa = a[a["head"] & (a["female"] == 0) & a["pid"].isin(fathers)][["pid", "fam68", "year", "age", "valid", "ly",
                                                                      "hours", "wt"]]
    fa = fa.rename(columns={"pid": "fpid"}).merge(E, on="fpid", how="left")
    fa = fa[fa["age"].between(25, 64) & (fa["wt"] > 0)].copy()
    fa["emp"] = (fa["hours"] > 0).astype(float).where(fa["hours"].notna())
    fa["et"] = (fa["year"] - fa["ev"]).clip(-6, 6)
    ets = [k for k in range(-6, 7) if k != -1]
    cols = []
    for g, mask in (("bad", fa["bad"] == 1), ("good", fa["bad"] == 0), ("na", fa["ev"].notna() & fa["bad"].isna())):
        for k in ets:
            fa[f"{g}{k}"] = ((fa["et"] == k) & mask).astype(float)
            cols.append(f"{g}{k}")
    out = {"n": {g: int(E["bad"].eq(v).sum()) if v is not None else int(E["bad"].isna().sum())
                 for g, v in (("bad", 1), ("good", 0), ("na", None))}}
    for y in ("ly", "emp"):
        d = fa.dropna(subset=[y]) if y == "emp" else fa[fa["valid"] == True].dropna(subset=["ly"])  # noqa: E712
        X = np.column_stack([d[cols].to_numpy(float), dummies(d["year"]), dummies(d["age"])])
        b, V, _ = R93.ols(X, d[y].to_numpy(float), d["wt"].to_numpy(float), d["fam68"].to_numpy(),
                          absorb=d["fpid"].to_numpy())
        k = len(cols)
        b, V = b[:k], V[:k, :k]
        ix = {cname: i for i, cname in enumerate(cols)}
        res = {}
        for g in ("bad", "good"):
            res[g] = {str(e): [float(b[ix[f"{g}{e}"]]), float(np.sqrt(V[ix[f"{g}{e}"], ix[f"{g}{e}"]]))] for e in ets}
            w = np.zeros(k)
            for e in range(0, 7):
                w[ix[f"{g}{e}"]] = 1 / 7
            res[f"{g}_post"] = [float(w @ b), float(np.sqrt(w @ V @ w))]
            wp = np.zeros(k)
            for e in range(-6, -1):
                wp[ix[f"{g}{e}"]] = 1 / 5
            res[f"{g}_pre"] = [float(wp @ b), float(np.sqrt(wp @ V @ wp))]
        w = np.zeros(k)
        for e in range(0, 7):
            w[ix[f"bad{e}"]], w[ix[f"good{e}"]] = 1 / 7, -1 / 7
        res["diff_post"] = [float(w @ b), float(np.sqrt(w @ V @ w))]
        out[y] = res
    return out


def recession_parts(r):
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    a = pd.read_pickle(R24.CACHE)
    lay = R104.lay_set()
    sons = r.drop_duplicates("pid")[["pid", "fpid"]].dropna()
    k = py[py["child"] & py["age"].between(13, 19) & py["faminc"].between(R24.LO, R24.HI) & py["pid"].isin(sons["pid"])][
        ["pid", "wave", "int"]]
    fa = a[a["head"] & (a["female"] == 0)][["pid", "wave"]].rename(columns={"pid": "fpid"}).drop_duplicates()
    fw = k.merge(sons, on="pid").merge(fa, on=["fpid", "wave"])
    y = fw["wave"] - 1
    yr = [t if (p, t) in lay else (t - 1 if (p, t - 1) in lay else np.nan) for p, t in zip(fw["fpid"], y)]
    fw["ly_year"] = yr
    yr2rec = {t: lab for lab, ts in REC.items() for t in ts}
    fw["rec"] = [("none" if pd.notna(t) and t not in yr2rec else yr2rec.get(t, "")) if pd.notna(t) else ""
                 for t in fw["ly_year"]]
    n = fw.groupby("pid").size()
    out = pd.DataFrame(index=n.index)
    for lab in list(REC) + ["none"]:
        out[f"lay_r{lab}"] = (fw["rec"] == lab).groupby(fw["pid"]).sum() / n
    out.index.name = "pid"
    cnt = fw[fw["rec"] != ""]["rec"].value_counts().to_dict()
    return out.reset_index(), cnt


def main():
    r = R75.build()
    md = ["# Layoffs in bad times: the father's own loss and recession by recession (committee memo H4)", "",
          "Built by `124.RecessionLayoffs.py` (2026-10-24); design in its docstring. *** p<0.01, ** p<0.05, * p<0.1. "
          "**Descriptive.**", ""]
    E = event_by_times(r)
    RES["event"] = E
    md += ["## (i) The father's earnings and employment around his first teen-window layoff, by times", "",
           f"Fathers with a first layoff in bad times {E['n']['bad']:,}, in other times {E['n']['good']:,}, "
           f"unclassed {E['n']['na']:,}.", "",
           "| outcome | times | -4 | -2 | 0 | +2 | +4 | +6 | mean -6..-2 | mean 0..+6 |", "|---" * 10 + "|"]
    for y, lab in (("ly", "ln earnings"), ("emp", "employed")):
        for g in ("bad", "good"):
            cells = [c(tuple(E[y][g][str(e)])) for e in (-4, -2, 0, 2, 4, 6)]
            md.append(f"| {lab} | {g} | " + " | ".join(cells) + f" | {c(tuple(E[y][g + '_pre']))} | "
                      f"{c(tuple(E[y][g + '_post']))} |")
        md.append(f"| {lab} | bad - good | | | | | | | | {c(tuple(E[y]['diff_post']))} |")
    md.append("")
    print("\n".join(md), flush=True)
    P, cnt = recession_parts(r)
    r = r.merge(P, on="pid", how="left")
    parts = [f"lay_r{lab}" for lab in list(REC) + ["none"]]
    pres = r["nofa"] == 0
    for p in parts:
        r[p] = r[p].where(pres, 0.0).fillna(0.0)
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    cohd = pd.get_dummies(r["coh5"], prefix="coh", drop_first=True).astype(float)
    r = pd.concat([r, cohd], axis=1)
    r["agec"] = (r["age"] - 40) / 10
    noL = [x for x in COMPS if x != "f_sh_layoff"]
    XB = R91.xage(r, ["lyp"] + noL + STRUCT + list(cohd.columns))
    XP = R91.xage(r, parts)
    v = r[r["lw"].notna()].copy()
    md += ["## (ii) The within-son cost by recession (ln earnings, one regression)", "",
           "| layoff years in | teen layoff years | layoff share x age | treated sons | treated at 45-49 |",
           "|---|---|---|---|---|"]
    f = R91.fe_fit(v, "ly", XB + XP)
    for lab, p in zip(list(REC) + ["no recession"], parts):
        est = (f["b"][f"{p}_xa"], float(np.sqrt(f["V"].loc[f"{p}_xa", f"{p}_xa"]))) if f"{p}_xa" in f["b"] else (np.nan, np.nan)
        tr = int(v[(v[p] > 0) & pres.loc[v.index]]["pid"].nunique())
        t45 = int(v[(v[p] > 0) & (v["band"] == 4) & pres.loc[v.index]]["pid"].nunique())
        key = lab if lab != "no recession" else "none"
        md.append(f"| {lab} | {cnt.get(key, 0)} | {c(est)} | {tr} | {t45} |")
        RES[f"rec|{lab}"] = {"fe": [float(est[0]), float(est[1])], "years": int(cnt.get(key, 0)), "treated": tr,
                             "treated45": t45}
    rec_xa = [f"{p}_xa" for p in parts[:-1] if f"{p}_xa" in f["b"]]
    allrec = R91.lincom(f, {x: 1 / len(rec_xa) for x in rec_xa})
    W = R91.wald(f, np.eye(len(rec_xa))[1:] - np.eye(len(rec_xa))[0], rec_xa)
    dif = R91.lincom(f, {**{x: 1 / len(rec_xa) for x in rec_xa}, f"{parts[-1]}_xa": -1})
    md += ["", f"Mean of the recession slopes {c(allrec)}; recessions equal: chi2({W[1]}) = {W[0]:.2f}, p = {W[2]:.3f}; "
           f"mean recession minus no recession {c(dif)}.", ""]
    RES["rec|summary"] = {"mean": list(allrec), "equal": list(W), "diff": list(dif)}
    (OUT / "recession_layoffs.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "recession_layoffs.json", "w"), indent=1, default=float)
    print("\n".join(md))


if __name__ == "__main__":
    main()
