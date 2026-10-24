r"""Does the unemployment insurance the father actually received soften his son's cost? (committee memo H3, 2026-10-24)

The paper's UI tests use the state's schedule (82), the benefit simulated at the father's wage (99) and the weeks
available (102); none is significant, and their minimum detectable effects exceed the cost itself. The PSID records
the head's unemployment compensation every year from the 1976 wave, which gives the insurance each father received.
UI RECEIVED: the head's unemployment compensation in the income year (2000 dollars): 1976 'HD UNEMP WRK COMP' (with
  workers' compensation), 1977-1993 'HD yyyy UNEMP COMP', 1994-2003 'AMT UNEMPL COMP OF HEAD' x its time unit (week,
  two weeks, month: x 4.33 / 2.17 / 1 per month received, months from the 'UNEMPLOY INCOME HEAD JAN-DEC' flags; year:
  as is), 2005+ 'HEAD / REF PERSN UNEMPLOYMENT COMPENSATION-yyyy'.
REALISED REPLACEMENT of a teen layoff year (75's matching: the layoff record dated to income year y or y-1 of the
  window wave): UI received in y and y-1, per week unemployed (the head's hours unemployed in those years / 40; the PSID
  has them to the 1993 wave), over the father's usual weekly earnings (his mean earnings over the son's layoff-free teen
  waves / 52).
PARTS of the teen layoff share: no UI received; UI with replacement below / above the median among layoff years with a
  ratio; UI received but the ratio not computable; UI unknown. The same split of the closure share is the placebo.
DESIGN: 91's machinery on 75's son-years with a valid wage: band change 45-49 minus 25-29 of each part (200 common
  draws) and within-son slopes; Wald test of low = high replacement.
Writes output/realised_ui.md / .json (aggregates only); caches data/head_ui_amounts.pkl (family-level).
DESCRIPTIVE.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import DATA, OUT, to2000  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R91 = _load("s91", "91.LayoffSelection.py")
R18 = _load("s18", "18.HusbandIndustryShocks.py")
R75, R24 = R91.R75, R91.R24
c, fmt, sd, Boot = R91.c, R91.fmt, R91.sd, R91.Boot
COMPS, STRUCT = R91.COMPS, R91.STRUCT
CACHE = DATA / "head_ui_amounts.pkl"
ANN = r"^(HD +(\d{2,4} )?UNEMP(LOYMENT|LMT)? ?(WRK )?COMP|HD \d{4} UNEMP COMPENSATION|(HEAD|REF PERSN) UNEMPLOYMENT COMPENSATION-\d{4})"
RES = {}


def ui_items():
    if CACHE.exists():
        return pd.read_pickle(CACHE)
    out = []
    for w in [x for x in R18.FS.WAVES if x >= 1976]:
        do = next(f for f in (R18.FAM / (f"fam{w}" if w < 1994 else f"fam{w}er")).glob("*.do") if "formats" not in f.name)
        pos, labs = R18.layout(do)
        idv = labs[1][0]
        x = None
        if 1994 <= w <= 2003:
            amt = next(v for v, l in labs if re.match(r"AMT UNEMPL COMP OF HEAD", l))
            per = next(v for v, l in labs if re.match(r"AMT UNEMPL COMP HD PER", l))
            mon = [v for v, l in labs if re.match(r"UNEMPLOY INCOME HEAD (JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)", l)]
            f = R18.read(do.with_suffix(".txt"), [idv, amt, per] + mon, pos)
            a = pd.to_numeric(f[amt], errors="coerce").where(lambda s: s.between(0, 99_996))
            u = pd.to_numeric(f[per], errors="coerce")
            nm = (f[mon].apply(pd.to_numeric, errors="coerce") == 1).sum(axis=1) if mon else np.nan
            nm = nm.where(nm > 0, np.nan)
            ann = np.select([u == 1, u == 2, u == 3, u == 4], [a * 4.33 * nm, a * 2.17 * nm, a * nm, a], np.nan)
            ann = pd.Series(ann, index=f.index).where(~((a == 0) | (u == 0)), 0.0)
            x = pd.DataFrame({"wave": w, "int": f[idv], "ui": ann})
            src = f"{amt} x {per}, {len(mon)} month flags"
        else:
            v = next((v for v, l in labs if re.match(ANN, l)), None)
            f = R18.read(do.with_suffix(".txt"), [idv, v], pos)
            x = pd.DataFrame({"wave": w, "int": f[idv], "ui": pd.to_numeric(f[v], errors="coerce")})
            src = v
        x["ui"] = to2000(x["ui"], w - 1)
        print(f"  {w}: {src}; received {float((x['ui'] > 0).mean()):.3f}", flush=True)
        out.append(x)
    F = pd.concat(out, ignore_index=True)
    F.to_pickle(CACHE)
    return F


def parts(r):
    a = pd.read_pickle(R24.CACHE)
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    dp = pd.read_pickle(DATA / "psid_displacement.pkl")
    lay = set(zip(dp.loc[(dp["main"] == 1) & (dp["strict"] != 1), "pid"], dp.loc[(dp["main"] == 1) & (dp["strict"] != 1), "year"]))
    clo = set(zip(dp.loc[dp["strict"] == 1, "pid"], dp.loc[dp["strict"] == 1, "year"]))
    sons = r.drop_duplicates("pid")[["pid", "fpid"]].dropna()
    k = py[py["child"] & py["age"].between(13, 19) & py["faminc"].between(R24.LO, R24.HI) & py["pid"].isin(sons["pid"])][
        ["pid", "wave", "int"]]
    fa = a[a["head"] & (a["female"] == 0)][["pid", "wave", "int", "earn", "hu"]].rename(columns={"pid": "fpid", "int": "fint"})
    fa = fa.drop_duplicates(["fpid", "wave"]).merge(ui_items().rename(columns={"int": "fint"}), on=["wave", "fint"], how="left")
    fa = fa.sort_values(["fpid", "wave"])
    prev = fa.groupby("fpid")[["ui", "hu", "wave"]].shift(1)
    fa["ui2"] = fa["ui"] + prev["ui"].where(prev["wave"] == fa["wave"] - 1, 0.0).fillna(0.0)
    fa["hu2"] = fa["hu"] + prev["hu"].where(prev["wave"] == fa["wave"] - 1, 0.0).fillna(0.0)
    fw = k.merge(sons, on="pid").merge(fa, on=["fpid", "wave"])
    y = fw["wave"] - 1
    fw["lay"] = [float((p, t) in lay or (p, t - 1) in lay) for p, t in zip(fw["fpid"], y)]
    fw["clo"] = [float((p, t) in clo or (p, t - 1) in clo) for p, t in zip(fw["fpid"], y)]
    base = fw[(fw["lay"] == 0) & (fw["clo"] == 0)].groupby("pid")["earn"].mean().rename("earn0")
    fw = fw.merge(base, on="pid", how="left")
    wk = fw["hu2"] / 40
    fw["repl"] = (fw["ui2"] / wk.where(wk >= 1)) / (fw["earn0"] / 52).where(fw["earn0"] > 0)
    fw.loc[fw["wave"] > 1993, "repl"] = np.nan
    ev = fw[(fw["lay"] == 1) | (fw["clo"] == 1)]
    med = float(ev.loc[(ev["ui2"] > 0) & ev["repl"].notna(), "repl"].median())
    cls = np.select([fw["ui2"].isna(), fw["ui2"] == 0, fw["repl"].isna(), fw["repl"] < med],
                    ["unk", "noui", "uina", "lo"], "hi")
    fw["cls"] = cls
    n = fw.groupby("pid").size()
    out = pd.DataFrame(index=n.index)
    for ev_, lab in (("lay", "lay"), ("clo", "clo")):
        for k_ in ("noui", "lo", "hi", "uina", "unk"):
            out[f"{lab}_{k_}"] = (fw[ev_] * (fw["cls"] == k_)).groupby(fw["pid"]).sum() / n
    L = fw[fw["lay"] == 1]
    info = {"median_repl": med, "layoff_years": int(len(L)),
            "share": {k_: float((L["cls"] == k_).mean()) for k_ in ("noui", "lo", "hi", "uina", "unk")},
            "mean_repl_lo": float(L.loc[L["cls"] == "lo", "repl"].mean()),
            "mean_repl_hi": float(L.loc[L["cls"] == "hi", "repl"].mean()),
            "mean_ui_received": float(L.loc[L["ui2"] > 0, "ui2"].mean())}
    out.index.name = "pid"
    return out.reset_index(), info


def main():
    r = R75.build()
    P, info = parts(r)
    r = r.merge(P, on="pid", how="left")
    pres = r["nofa"] == 0
    cols = [x for x in P.columns if x != "pid"]
    for x in cols:
        r[x] = r[x].where(pres, 0.0).fillna(0.0)
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    cohd = pd.get_dummies(r["coh5"], prefix="coh", drop_first=True).astype(float)
    r = pd.concat([r, cohd], axis=1)
    r["agec"] = (r["age"] - 40) / 10
    noLC = [x for x in COMPS if x not in ("f_sh_layoff", "f_sh_close")]
    XB = R91.xage(r, ["lyp"] + noLC + STRUCT + list(cohd.columns))
    XP = R91.xage(r, cols)
    v = r[r["lw"].notna()].copy()
    BT = Boot(v["fam68"].to_numpy(), v["race"].to_numpy())
    md = ["# Does the UI the father actually received soften his son's cost? (committee memo H3)", "",
          "Built by `130.RealisedUI.py` (2026-10-24); design in its docstring. Per unit share; band s.e. from 200 "
          "cluster-bootstrap draws; within-son s.e. clustered by 1968 family. *** p<0.01, ** p<0.05, * p<0.1. "
          "**Descriptive.**", "",
          f"Teen layoff years {info['layoff_years']:,}: no UI received {info['share']['noui']:.3f}, UI with low "
          f"replacement {info['share']['lo']:.3f} (mean {info['mean_repl_lo']:.3f}), high {info['share']['hi']:.3f} "
          f"(mean {info['mean_repl_hi']:.3f}), UI but ratio not computable {info['share']['uina']:.3f}, UI unknown "
          f"{info['share']['unk']:.3f}; median realised weekly replacement {info['median_repl']:.3f}; mean UI received "
          f"in the layoff years when positive ${info['mean_ui_received']:,.0f} (2000 dollars).", "",
          "| event | part | 25-29 | 45-49 | change | within son x age | treated sons at 45-49 |", "|---" * 7 + "|"]
    comps2 = noLC + cols
    g0 = R91.band_fit(v, "ly", 0, BT, comps2, cols)
    g4 = R91.band_fit(v, "ly", 4, BT, comps2, cols)
    f = R91.fe_fit(v, "ly", XB + XP)
    for x in cols:
        a0, b4 = g0.get(x), g4.get(x)
        ch = (b4[0] - a0[0], b4[1] - a0[1]) if a0 and b4 else None
        fe = (f["b"][f"{x}_xa"], float(np.sqrt(f["V"].loc[f"{x}_xa", f"{x}_xa"]))) if f"{x}_xa" in f["b"] else (np.nan, np.nan)
        t45 = int(v[(v["band"] == 4) & (v[x] > 0) & pres.loc[v.index]]["pid"].nunique())
        md.append(f"| {x[:3]} | {x[4:]} | {fmt(a0)} | {fmt(b4)} | {fmt(ch)} | {c(fe)} | {t45} |")
        RES[x] = {"ch": [float(ch[0]), sd(ch[1])] if ch else None, "fe": list(map(float, fe)), "t45": t45}
        print(md[-1], flush=True)
    for ev in ("lay", "clo"):
        W = R91.wald(f, [1, -1], [f"{ev}_lo_xa", f"{ev}_hi_xa"])
        d = R91.lincom(f, {f"{ev}_hi_xa": 1, f"{ev}_lo_xa": -1})
        W2 = R91.wald(f, [1, -1], [f"{ev}_noui_xa", f"{ev}_hi_xa"])
        md.append(f"\n{ev}: high - low replacement within son {c(d)} (Wald p={W[2]:.3f}); no UI = high: p={W2[2]:.3f}.")
        RES[f"{ev}|hi-lo"] = {"diff": list(d), "p": W[2], "p_noui_hi": W2[2]}
    md.append("")
    RES["info"] = info
    (OUT / "realised_ui.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "realised_ui.json", "w"), indent=1, default=float)
    print("\n".join(md))


if __name__ == "__main__":
    main()
