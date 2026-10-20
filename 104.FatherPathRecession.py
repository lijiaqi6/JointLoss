r"""What kind of father does the costly layoff mark, and do the less selected layoffs cost too? (Fable round 2,
Objection 2; plan proposals/paperB_round2_plan_20261020.md, step 2)

(i) THE FATHER'S PATH. For each father-present son: the father's mean ln earnings (valid years), share of years
    employed (hours > 0), unemployed (24's flag) and with a new layoff (75's definition), over his head-years at the
    son's ages 20-24, against his teen-window means. Regressed (one row per son, PSID weights, clusters 1968 family) on
    the teen layoff share and, separately, on 91's parts (small / large income loss, short / long unemployment, one /
    repeated), with ln parental income, the father's window ln wage and ln hours and 5-year cohort dummies.
(ii) LESS SELECTED LAYOFFS (Gibbons and Katz 1991: layoffs in bad times say less about the worker). Each teen layoff
    year (income year y of a window wave) is classed as a BAD-TIMES layoff if the national (CES) employment of the
    father's sector fell in y or y-1 (93's sector, measured before the window) or his family's state unemployment rate
    in y was at least one point above that state's 1976-2023 mean (LAUS, 1976+); other layoff years are GOOD-TIMES
    layoffs. The teen layoff share is split into the two parts; band change 45-49 minus 25-29 and the within-son slope of
    each (91's machinery: all components, lyp, structure, cohort x age; son FE), and their equality.
    Decision rule (plan): bad-times layoffs costing about as much as the others -> the event reading gains; only
    good-times (idiosyncratic) layoffs costing -> the cost marks the father's unstable employment.
Writes output/father_path_recession.md / .json (aggregates only). DESCRIPTIVE.
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


R91 = _load("s91", "91.LayoffSelection.py")
R93 = _load("s93", "93.LayoffIndustryShocks.py")
R75, R24 = R91.R75, R91.R24
c, Boot, fmt, sd, dummies = R91.c, R91.Boot, R91.fmt, R91.sd, R91.dummies
COMPS, STRUCT = R91.COMPS, R91.STRUCT
RES = {}


def lay_set():
    dp = pd.read_pickle(DATA / "psid_displacement.pkl")
    m = (dp["main"] == 1) & (dp["strict"] != 1)
    return set(zip(dp.loc[m, "pid"], dp.loc[m, "year"]))


def father_path(r, a, lay):
    sons = r.drop_duplicates("pid")[["pid", "fpid", "birth_year"]].dropna()
    fa = a[a["head"] & (a["female"] == 0)][["pid", "wave", "valid", "ly", "hours", "unemp"]].rename(
        columns={"pid": "fpid"}).drop_duplicates(["fpid", "wave"])
    rows = sons.assign(key=1).merge(pd.DataFrame({"off": range(20, 25), "key": 1}), on="key")
    rows["wave"] = (rows["birth_year"] + rows["off"] + 1).astype(int)
    rows = rows.merge(fa, on=["fpid", "wave"])
    y = rows["wave"] - 1
    rows["newlay"] = [float((p, t) in lay or (p, t - 1) in lay) for p, t in zip(rows["fpid"], y)]
    rows["emp"] = (rows["hours"] > 0).astype(float).where(rows["hours"].notna())
    rows["unemp"] = pd.to_numeric(rows["unemp"], errors="coerce")
    v = rows[rows["valid"] == True]  # noqa: E712
    g = rows.groupby("pid")
    out = pd.DataFrame({"fp_ly": v.groupby("pid")["ly"].mean(), "fp_emp": g["emp"].mean(), "fp_unemp": g["unemp"].mean(),
                        "fp_lay": g["newlay"].mean(), "fp_n": g.size()})
    return out[out["fp_n"] >= 2].reset_index()


def bad_times_split(r, a, lay):
    S = R93.father_sector(r)[["pid", "h_sec"]]
    E, G = R93.ces_employment()
    st = pd.read_pickle(DATA / "husband_shocks_fam.pkl")[["wave", "int", "fips"]].drop_duplicates(["wave", "int"])
    ur = pd.read_pickle(DATA / "state_shocks.pkl")[["fips", "year", "ur"]]
    ur["ur_dev"] = ur["ur"] - ur.groupby("fips")["ur"].transform("mean")
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    sons = r.drop_duplicates("pid")[["pid", "fpid"]].dropna()
    k = py[py["child"] & py["age"].between(13, 19) & py["faminc"].between(R24.LO, R24.HI) & py["pid"].isin(sons["pid"])][
        ["pid", "wave", "int"]]
    fa = a[a["head"] & (a["female"] == 0)][["pid", "wave"]].rename(columns={"pid": "fpid"}).drop_duplicates()
    fw = k.merge(sons, on="pid").merge(fa, on=["fpid", "wave"]).merge(S, on="pid", how="left")
    fw = fw.merge(st, on=["wave", "int"], how="left")
    fw["y"] = fw["wave"] - 1
    fw = fw.merge(ur.rename(columns={"year": "y"}), on=["fips", "y"], how="left")
    fw["lay"] = [float((p, t) in lay or (p, t - 1) in lay) for p, t in zip(fw["fpid"], fw["y"])]

    def decl(s, y):
        if pd.isna(s) or int(s) not in G.columns:
            return np.nan
        x = [G.loc[t, int(s)] for t in (y, y - 1) if t in G.index]
        return float(any(v < 0 for v in x if pd.notna(v))) if x else np.nan

    fw["sec_decl"] = [decl(s, int(y)) for s, y in zip(fw["h_sec"], fw["y"])]
    fw["st_high"] = (fw["ur_dev"] >= 1).astype(float).where(fw["ur_dev"].notna())
    fw["bad"] = np.fmax(fw["sec_decl"].fillna(0), fw["st_high"].fillna(0)).where(fw["sec_decl"].notna() | fw["st_high"].notna())
    n = fw.groupby("pid").size()
    out = pd.DataFrame(index=n.index)
    for lab, mask in (("lay_bad", fw["bad"] == 1), ("lay_good", fw["bad"] == 0), ("lay_bad_na", fw["bad"].isna()),
                      ("lay_secdecl", fw["sec_decl"] == 1), ("lay_secnot", fw["sec_decl"] == 0),
                      ("lay_secna", fw["sec_decl"].isna())):
        out[lab] = (fw["lay"] * mask.astype(float)).groupby(fw["pid"]).sum() / n
    info = {"layoff_years": int(fw["lay"].sum()),
            "share_bad": float(fw.loc[fw["lay"] == 1, "bad"].mean()),
            "share_bad_measured": float(fw.loc[fw["lay"] == 1, "bad"].notna().mean()),
            "share_secdecl": float(fw.loc[fw["lay"] == 1, "sec_decl"].mean()),
            "share_all_years_bad": float(fw["bad"].mean())}
    out.index.name = "pid"
    return out.reset_index(), info


def main():
    r = R75.build()
    a = pd.read_pickle(R24.CACHE)
    a["unemp"] = pd.to_numeric(a["unemp"], errors="coerce")
    lay = lay_set()
    det, _ = R91.teen_detail(r)
    bt, info = bad_times_split(r, a, lay)
    r = r.merge(det, on="pid", how="left").merge(bt, on="pid", how="left").merge(father_path(r, a, lay), on="pid", how="left")
    pres = r["nofa"] == 0
    parts = [v for v in det.columns if v.startswith("lay_")] + [v for v in bt.columns if v.startswith("lay_")]
    for v in parts:
        r[v] = r[v].where(pres, 0.0).fillna(0.0)
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    cohd = pd.get_dummies(r["coh5"], prefix="coh", drop_first=True).astype(float)
    r = pd.concat([r, cohd], axis=1)
    COH = list(cohd.columns)
    r["agec"] = (r["age"] - 40) / 10
    md = ["# The father's path after the layoff, and layoffs in bad times (Fable round 2, Objection 2)", "",
          "Built by `104.FatherPathRecession.py` (2026-10-20); design in its docstring. *** p<0.01, ** p<0.05, * p<0.1.", ""]
    # (i) father's path, one row per son
    one = r[pres].drop_duplicates("pid").copy()
    one["fp_dly"] = one["fp_ly"] - (one["f_lw"] + one["f_lh"])
    md += ["## (i) The father's path at the son's 20-24 (one row per father-present son)", "",
           "Each column: the father's outcome at the son's 20-24 on the teen layoff share (row 1) or on its parts (rows "
           "below, one regression per split), with ln parental income, the father's teen-window ln wage and ln hours "
           "and 5-year cohort dummies; PSID weights; clustered by 1968 family. Per unit share.", "",
           "| regressor | ln earnings | ln earnings minus his teen mean | employed | unemployed | laid off again |",
           "|---|---|---|---|---|---|"]
    ys = ["fp_ly", "fp_dly", "fp_emp", "fp_unemp", "fp_lay"]
    ctl = ["lyp", "f_lw", "f_lh"] + COH

    def son_reg(xs):
        out = {}
        for y in ys:
            z = one.dropna(subset=[y] + xs + ctl)
            X = np.column_stack([z[xs + ctl].to_numpy(float), np.ones(len(z))])
            b, V, _ = R93.ols(X, z[y].to_numpy(float), z["wt"].to_numpy(float), z["fam68"].to_numpy())
            out[y] = [(b[j], np.sqrt(V[j, j])) for j in range(len(xs))]
            out[f"{y}_n"] = len(z)
        return out

    o = son_reg(["f_sh_layoff"])
    md.append("| teen layoff share | " + " | ".join(c(o[y][0]) for y in ys) + " |")
    RES["path|f_sh_layoff"] = {y: list(map(float, o[y][0])) for y in ys}
    for title, xs in (("income loss", ["lay_loss_small", "lay_loss_big", "lay_loss_na"]),
                      ("unemployment", ["lay_hu_short", "lay_hu_long", "lay_hu_na"]),
                      ("repeat", ["lay_one", "lay_multi"]),
                      ("bad times", ["lay_bad", "lay_good", "lay_bad_na"])):
        o = son_reg(xs)
        for j, x in enumerate(xs):
            if x.endswith("_na"):
                continue
            md.append(f"| {title}: {x} | " + " | ".join(c(o[y][j]) for y in ys) + " |")
            RES[f"path|{x}"] = {y: list(map(float, o[y][j])) for y in ys}
    md.append(f"| N fathers (ln earnings / employed) | {o['fp_ly_n']:,} | | {o['fp_emp_n']:,} | | |")
    md.append("")
    # (ii) bad-times vs good-times layoffs: band change and within-son slope
    v = r[r["lw"].notna()].copy()
    BT = Boot(v["fam68"].to_numpy(), v["race"].to_numpy())
    noL = [x for x in COMPS if x != "f_sh_layoff"]
    XB2 = [f"{x}_xa" for x in ["lyp"] + noL + STRUCT + COH]
    for x in set(["lyp"] + noL + STRUCT + COH + parts):
        v[f"{x}_xa"] = v[x] * v["agec"]
    md += ["## (ii) Layoffs in bad times vs other layoffs", "",
           f"Teen layoff years {info['layoff_years']:,}; classed in {info['share_bad_measured']:.0%}; bad times "
           f"(sector decline or state unemployment >= 1 point above its mean) {info['share_bad']:.0%} of classed layoff "
           f"years (sector decline alone {info['share_secdecl']:.0%}), against {info['share_all_years_bad']:.0%} of all "
           "classed window years.", "",
           "| split | part | 25-29 | 45-49 | change | within son x age | first two equal (within son) |",
           "|---" * 7 + "|"]
    for title, ps in (("bad times (sector decline or high state unemployment)", ["lay_bad", "lay_good", "lay_bad_na"]),
                      ("sector decline only", ["lay_secdecl", "lay_secnot", "lay_secna"])):
        comps = noL + ps
        g0 = R91.band_fit(v, "ly", 0, BT, comps, ps)
        g4 = R91.band_fit(v, "ly", 4, BT, comps, ps)
        f = R91.fe_fit(v, "ly", XB2 + [f"{p}_xa" for p in ps])
        W = R91.wald(f, np.array([[1, -1]]), [f"{ps[0]}_xa", f"{ps[1]}_xa"])
        for j, p in enumerate(ps):
            a0, b4 = g0.get(p), g4.get(p)
            ch = (b4[0] - a0[0], b4[1] - a0[1]) if a0 and b4 else None
            fe = (f["b"][f"{p}_xa"], float(np.sqrt(f["V"].loc[f"{p}_xa", f"{p}_xa"])))
            md.append(f"| {title if j == 0 else ''} | {p} | {fmt(a0)} | {fmt(b4)} | {fmt(ch)} | {c(fe)} | "
                      + (f"chi2 {W[0]:.2f}, p={W[2]:.3f}" if j == 0 else "") + " |")
            RES[f"bad|{title}|{p}"] = {"ch": [float(ch[0]), sd(ch[1])] if ch else None, "fe": list(map(float, fe))}
        RES[f"bad|{title}|wald"] = list(W)
    md.append("")
    RES["info"] = info
    (OUT / "father_path_recession.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "father_path_recession.json", "w"), indent=1, default=float)
    print("\n".join(md))


if __name__ == "__main__":
    main()
