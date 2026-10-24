r"""Laid off or fired? Splitting the PSID's single code by signs of a layoff (committee re-read memo, action 3, 2026-10-24)

The PSID records 'laid off; fired' as one code in every wave, so the paper's 'layoff' mixes layoffs, which say little
about the worker, with firings, which say more. In the NLSY79 CYA, where the mother's job roster separates them, her
firings add to the stability component of the young-adult IGE (0.008*, p = 0.065) and her layoffs subtract from it
(-0.005**) (83.CYAWhatIsPassedOn.py; children at 26-35 only).
SIGNS OF A LAYOFF for a father's teen 'laid off / fired' year (75's matching, record dated to the income year or the
year before):
  UI     the head drew unemployment compensation in that income year or the one before (130's amounts, 1976+); a worker
         fired for cause is generally not eligible;
  TEMP   'temporarily laid off' at that or the next interview (91's employment status, 1983+);
  RECALL his employer at a later interview predates the job end (120's classification).
PARTS of the teen layoff share: LAYOFF SIGN (any of the three); NO SIGN (UI measured and none, no temporary layoff,
not a recall: more likely a firing, or a layoff without benefits); UNKNOWN (UI not measured, before the 1976 wave, and
no other sign).
DESIGN: 91's machinery on 75's son-years with a valid wage: band change 45-49 minus 25-29 (200 common draws) and
within-son slopes; Wald test of equality of the first two.
Writes output/layoff_vs_firing.md / .json (aggregates only). DESCRIPTIVE.
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


R130 = _load("s130", "130.RealisedUI.py")
R120 = _load("s120", "120.LayoffRecall.py")
R91, R75, R24 = R130.R91, R130.R75, R130.R24
c, fmt, sd, Boot = R91.c, R91.fmt, R91.sd, R91.Boot
COMPS, STRUCT = R91.COMPS, R91.STRUCT
RES = {}


def parts(r):
    a = pd.read_pickle(R24.CACHE)
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    dp = pd.read_pickle(DATA / "psid_displacement.pkl")
    T, F = R120.tenure_all()
    L = R120.classify(dp, py, T, F, R120.R119.head_se())
    CLS = dict(zip(zip(L["pid"], L["year"]), L["cls"]))
    lay = set(zip(dp.loc[(dp["main"] == 1) & (dp["strict"] != 1), "pid"], dp.loc[(dp["main"] == 1) & (dp["strict"] != 1), "year"]))
    sons = r.drop_duplicates("pid")[["pid", "fpid"]].dropna()
    k = py[py["child"] & py["age"].between(13, 19) & py["faminc"].between(R24.LO, R24.HI) & py["pid"].isin(sons["pid"])][
        ["pid", "wave", "int"]]
    fa = a[a["head"] & (a["female"] == 0)][["pid", "wave", "int", "est"]].rename(columns={"pid": "fpid", "int": "fint"})
    fa = fa.drop_duplicates(["fpid", "wave"]).merge(R130.ui_items().rename(columns={"int": "fint"}), on=["wave", "fint"],
                                                    how="left").sort_values(["fpid", "wave"])
    prev = fa.groupby("fpid")[["ui", "wave"]].shift(1)
    fa["ui2"] = fa["ui"] + prev["ui"].where(prev["wave"] == fa["wave"] - 1, 0.0).fillna(0.0)
    nxt = fa.groupby("fpid")[["est", "wave"]].shift(-1)
    fa["temp"] = ((fa["est"] == 2) | (nxt["est"] == 2)).astype(float).where(fa["wave"] >= 1983)
    fw = k.merge(sons, on="pid").merge(fa, on=["fpid", "wave"])
    y = fw["wave"] - 1
    rec = []
    for p, t in zip(fw["fpid"], y):
        q = [CLS.get((p, s)) for s in (t, t - 1) if (p, s) in lay]
        rec.append(None if not q else ("recall" if "recall" in q else q[0]))
    fw["lay"] = [float(x is not None) for x in rec]
    fw["recall"] = [float(x == "recall") for x in rec]
    sign = (fw["ui2"] > 0) | (fw["temp"] == 1) | (fw["recall"] == 1)
    nosign = (fw["ui2"] == 0) & ~sign
    fw["cls"] = np.select([sign, nosign], ["sign", "nosign"], "unk")
    n = fw.groupby("pid").size()
    out = pd.DataFrame(index=n.index)
    for k_ in ("sign", "nosign", "unk"):
        out[f"lay_{k_}"] = (fw["lay"] * (fw["cls"] == k_)).groupby(fw["pid"]).sum() / n
    Lw = fw[fw["lay"] == 1]
    info = {"layoff_years": int(len(Lw)), "share": {k_: float((Lw["cls"] == k_).mean()) for k_ in ("sign", "nosign", "unk")},
            "by_sign": {"ui": float((Lw["ui2"] > 0).mean()), "temp": float((Lw["temp"] == 1).mean()),
                        "recall": float((Lw["recall"] == 1).mean())}}
    out.index.name = "pid"
    return out.reset_index(), info


def main():
    r = R75.build()
    P, info = parts(r)
    r = r.merge(P, on="pid", how="left")
    pres = r["nofa"] == 0
    cols = ["lay_sign", "lay_nosign", "lay_unk"]
    for x in cols:
        r[x] = r[x].where(pres, 0.0).fillna(0.0)
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    cohd = pd.get_dummies(r["coh5"], prefix="coh", drop_first=True).astype(float)
    r = pd.concat([r, cohd], axis=1)
    r["agec"] = (r["age"] - 40) / 10
    noL = [x for x in COMPS if x != "f_sh_layoff"]
    XB = R91.xage(r, ["lyp"] + noL + STRUCT + list(cohd.columns))
    XP = R91.xage(r, cols)
    v = r[r["lw"].notna()].copy()
    BT = Boot(v["fam68"].to_numpy(), v["race"].to_numpy())
    md = ["# Laid off or fired? Splitting the PSID's single code by signs of a layoff (committee re-read memo, action 3)", "",
          "Built by `134.LayoffVsFiring.py` (2026-10-24); design in its docstring. Per unit share; band s.e. from 200 "
          "cluster-bootstrap draws; within-son s.e. clustered by 1968 family. *** p<0.01, ** p<0.05, * p<0.1. "
          "**Descriptive.**", "",
          f"Teen 'laid off / fired' years {info['layoff_years']:,}: with a sign of a layoff {info['share']['sign']:.3f} "
          f"(UI drawn {info['by_sign']['ui']:.3f}, temporarily laid off {info['by_sign']['temp']:.3f}, recall "
          f"{info['by_sign']['recall']:.3f}), no sign {info['share']['nosign']:.3f}, unknown {info['share']['unk']:.3f}.", ""]
    for y, lab in (("ly", "ln earnings"), ("lw", "ln hourly wage")):
        md += [f"## {lab}", "", "| part | 25-29 | 45-49 | change | within son x age | treated sons at 45-49 |",
               "|---|---|---|---|---|---|"]
        g0 = R91.band_fit(v, y, 0, BT, noL + cols, cols)
        g4 = R91.band_fit(v, y, 4, BT, noL + cols, cols)
        f = R91.fe_fit(v, y, XB + XP)
        for x in cols:
            ch = (g4[x][0] - g0[x][0], g4[x][1] - g0[x][1])
            fe = (f["b"][f"{x}_xa"], float(np.sqrt(f["V"].loc[f"{x}_xa", f"{x}_xa"])))
            t45 = int(v[(v["band"] == 4) & (v[x] > 0) & pres.loc[v.index]]["pid"].nunique())
            md.append(f"| {x[4:]} | {fmt(g0[x])} | {fmt(g4[x])} | {fmt(ch)} | {c(fe)} | {t45} |")
            RES[f"{y}|{x}"] = {"ch": [float(ch[0]), sd(ch[1])], "fe": list(map(float, fe)), "t45": t45}
        chd = ((g4["lay_nosign"][0] - g0["lay_nosign"][0]) - (g4["lay_sign"][0] - g0["lay_sign"][0]),
               (g4["lay_nosign"][1] - g0["lay_nosign"][1]) - (g4["lay_sign"][1] - g0["lay_sign"][1]))
        d = R91.lincom(f, {"lay_nosign_xa": 1, "lay_sign_xa": -1})
        W = R91.wald(f, [1, -1], ["lay_nosign_xa", "lay_sign_xa"])
        md += [f"| no sign - sign | | | {fmt(chd)} | {c(d)} (Wald p={W[2]:.3f}) | |", ""]
        RES[f"{y}|diff"] = {"ch": [float(chd[0]), sd(chd[1])], "fe": list(d), "p": W[2]}
        print("\n".join(md[-6:]), flush=True)
    RES["info"] = info
    (OUT / "layoff_vs_firing.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "layoff_vs_firing.json", "w"), indent=1, default=float)
    print("\n".join(md))


if __name__ == "__main__":
    main()
