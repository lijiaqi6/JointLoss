r"""Self-employed fathers and the delayed cost of a father's teen layoff (committee memo Z2, 2026-10-24)

A business owner cannot report 'laid off / fired'; a failed business is reported as code 1 ('company folded / went
out of business'), which the paper counts as a plant closure. So sons of self-employed fathers sit in the comparison
group of the layoff estimates and in the closure group, and among them the gradient of holding the father's exact job
rises after 35 (43.FatherJobSelfEmployment.py). If their earnings rise late for that reason, part of the layoff's
late 'cost' is the comparison group's late rise. And the sons of laid-off fathers are more often self-employed
(118): are they following self-employed fathers?

FATHER'S SELF-EMPLOYMENT. The head's 'work for someone else (1), both (2), self only (3)' for his main job at the
interview, every wave from 1968 (1968-75: V198, V641, V1280, V1986, V2584, V3117, V3532, V3970, same codes; 1976+:
25.JointJobLoss.py's cache), in the father's head-waves at the son's 13-19 (the layoff share's window).
  f_se      father self-employed: codes 2-3 in at least half of his valid window waves (0 if no father in the window)
  f_se_any  any valid window wave with code 2-3
  f_se_na   father in the window without a valid code
DESIGNS (75's baseline sample and components, son-years with a valid wage; 91's band_fit / fe_fit, 200 common draws):
  1. counts: self-employed fathers by race; their layoff and closure shares against other fathers'.
  2. the layoff coefficient at 25-29 and 45-49, the change, the closure change and the layoff - closure difference,
     and the within-son slope, ln earnings and ln wage: (a) all sons, (b) without sons of self-employed fathers (f_se),
     (c) without sons of fathers ever self-employed in the window (f_se_any), (d) all sons with f_se, f_se_na (bands)
     and their x (age-40)/10 (within son) held fixed.
  3. sons and daughters (107's stacked design): the difference without children of self-employed fathers and with
     f_se, f_se_na as regressors (each interacted like the others).
  4. the son's self-employment (118's items): the layoff profile of self-employment under (a)-(d); self-employment by
     the father's; the cost in the son's employee and self-employed years under (b).
Writes output/father_self_employment.md / .json (aggregates only); caches data/father_se_1968_75.pkl (family-level).
DESCRIPTIVE.
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
R118 = _load("s118", "118.SonsEmployerType.py")
R107 = _load("s107", "107.LayoffSexDifference.py")
R18 = R118.R18
R75 = R91.R75
c, fmt, sd, Boot = R91.c, R91.fmt, R91.sd, R91.Boot
COMPS, STRUCT = R91.COMPS, R91.STRUCT
EARLY = {1968: "V198", 1969: "V641", 1970: "V1280", 1971: "V1986", 1972: "V2584", 1973: "V3117", 1974: "V3532",
         1975: "V3970"}
CACHE = DATA / "father_se_1968_75.pkl"
RES = {}


def head_se():
    """wave x int: head's work-for-self code (1-3; else missing), 1968-2023."""
    if CACHE.exists():
        E = pd.read_pickle(CACHE)
    else:
        out = []
        for w, v in EARLY.items():
            do = next(f for f in (R18.FAM / f"fam{w}").glob("*.do") if "formats" not in f.name)
            pos, labs = R18.layout(do)
            idv = labs[1][0]
            f = R18.read(do.with_suffix(".txt"), [idv, v], pos).rename(columns={idv: "int", v: "h_se"})
            f["wave"] = w
            out.append(f[["wave", "int", "h_se"]])
        E = pd.concat(out, ignore_index=True)
        E.to_pickle(CACHE)
    L = pd.read_pickle(DATA / "joint_job_loss_selfemp.pkl")["X"][["wave", "int", "h_se"]]
    X = pd.concat([E, L], ignore_index=True).drop_duplicates(["wave", "int"])
    X["se"] = np.where(X["h_se"].isin([2, 3]), 1.0, np.where(X["h_se"] == 1, 0.0, np.nan))
    return X[["wave", "int", "se"]]


def father_se(kids, py, X):
    """per child (pid, fpid, birth_year): f_se, f_se_any, f_n_se over the father's head-waves at the child's 13-19."""
    hd = py[py["head"]][["pid", "wave", "int"]].merge(X, on=["wave", "int"], how="inner").rename(columns={"pid": "fpid"})
    k = kids.dropna(subset=["fpid"]).merge(hd, on="fpid", how="inner")
    k = k[(k["wave"] - k["birth_year"]).between(13, 19) & k["se"].notna()]
    g = k.groupby("pid")["se"].agg(["mean", "max", "count"])
    return pd.DataFrame({"f_se": (g["mean"] >= 0.5).astype(float), "f_se_any": g["max"], "f_n_se": g["count"]})


def attach(r, F, present):
    r = r.drop(columns=[x for x in ("f_se", "f_se_any", "f_n_se") if x in r]).merge(F, left_on="pid", right_index=True,
                                                                                   how="left")
    r["f_se_na"] = (present & r["f_se"].isna()).astype(float)
    for v in ("f_se", "f_se_any"):
        r[v] = r[v].fillna(0.0)
    return r


def profile(q, y, BT, XB, ctrl=(), xfe=()):
    g0 = R91.band_fit(q, y, 0, BT, COMPS, ["f_sh_layoff", "f_sh_close"], ctrl)
    g4 = R91.band_fit(q, y, 4, BT, COMPS, ["f_sh_layoff", "f_sh_close"], ctrl)
    ch = lambda v: (g4[v][0] - g0[v][0], g4[v][1] - g0[v][1])  # noqa: E731
    chL, chC = ch("f_sh_layoff"), ch("f_sh_close")
    f = R91.fe_fit(q, y, XB + list(xfe))
    fe = (f["b"]["f_sh_layoff_xa"], float(np.sqrt(f["V"].loc["f_sh_layoff_xa", "f_sh_layoff_xa"])))
    return {"a": g0["f_sh_layoff"], "b": g4["f_sh_layoff"], "ch": chL, "chC": chC,
            "dif": (chL[0] - chC[0], chL[1] - chC[1]), "fe": fe, "sons": int(q["pid"].nunique()),
            "treated45": int(q[(q["band"] == 4) & (q["f_sh_layoff"] > 0) & (q["nofa"] == 0)]["pid"].nunique())}


def js(o):
    out = {}
    for k, v in o.items():
        if isinstance(v, tuple) and len(v) == 2 and isinstance(v[1], np.ndarray):
            out[k] = [float(v[0]), sd(v[1])]
        elif isinstance(v, tuple):
            out[k] = [float(x) for x in v]
        else:
            out[k] = v
    return out


def main():
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    X = head_se()
    r = R75.build()
    sons = r.drop_duplicates("pid")[["pid", "fpid", "birth_year"]]
    F = father_se(sons, py, X)
    r = attach(r, F, r["nofa"] == 0)
    r = r.merge(R118.items(), on=["wave", "int"], how="left")
    r["selfemp"] = r["self"].isin([2, 3]).astype(float).where(r["self"].isin([1, 2, 3]))
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    cohd = pd.get_dummies(r["coh5"], prefix="coh", drop_first=True).astype(float)
    r = pd.concat([r, cohd], axis=1)
    r["agec"] = (r["age"] - 40) / 10
    XB = R91.xage(r, ["lyp"] + COMPS + STRUCT + list(cohd.columns))
    XS = R91.xage(r, ["f_se", "f_se_na"])
    v = r[r["lw"].notna()].copy()
    BT = Boot(v["fam68"].to_numpy(), v["race"].to_numpy())
    md = ["# Self-employed fathers and the delayed cost of a father's teen layoff (committee memo Z2)", "",
          "Built by `119.FatherSelfEmployment.py` (2026-10-24); design in its docstring. Per unit teen layoff share; band "
          "s.e. from 200 cluster-bootstrap draws of 1968 families (common to all rows), within-son s.e. clustered by 1968 "
          "family. *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**", ""]

    # 1. counts
    one = v[v["nofa"] == 0].drop_duplicates("pid")
    md += ["## 1. Self-employed fathers (father-present sons with a valid wage year)", "",
           "| sample | sons | father self-employed (half+ of window waves) | ever self-employed in window | no valid code | "
           "mean layoff share: SE / other fathers | mean closure share: SE / other | treated sons with SE father |",
           "|---" * 8 + "|"]
    for lab, q in (("pooled", one), ("White", one[one.race == "White"]), ("Black", one[one.race == "Black"])):
        w = q["wt"]
        se, ot = q[q["f_se"] == 1], q[(q["f_se"] == 0) & (q["f_se_na"] == 0)]
        row = {"sons": len(q), "se": float(np.average(q["f_se"], weights=w)),
               "any": float(np.average(q["f_se_any"], weights=w)), "na": float(np.average(q["f_se_na"], weights=w)),
               "lay": [float(np.average(se["f_sh_layoff"], weights=se["wt"])) if len(se) else None,
                       float(np.average(ot["f_sh_layoff"], weights=ot["wt"]))],
               "clo": [float(np.average(se["f_sh_close"], weights=se["wt"])) if len(se) else None,
                       float(np.average(ot["f_sh_close"], weights=ot["wt"]))],
               "treated_se": int(((q["f_se"] == 1) & (q["f_sh_layoff"] > 0)).sum()),
               "treated": int((q["f_sh_layoff"] > 0).sum())}
        RES[f"count|{lab}"] = row
        md.append(f"| {lab} | {row['sons']:,} | {row['se']:.3f} | {row['any']:.3f} | {row['na']:.3f} | "
                  f"{row['lay'][0]:.3f} / {row['lay'][1]:.3f} | {row['clo'][0]:.3f} / {row['clo'][1]:.3f} | "
                  f"{row['treated_se']} of {row['treated']} |")
    md.append("")

    # 2. the layoff profile
    md += ["## 2. The layoff profile with and without self-employed fathers", "",
           "| outcome | sample | 25-29 | 45-49 | change | closure change | layoff - closure | within son x age | sons | "
           "treated at 45-49 |", "|---" * 10 + "|"]
    specs = (("(a) all sons", v, (), ()), ("(b) without SE fathers", v[v["f_se"] == 0], (), ()),
             ("(c) without fathers ever SE", v[v["f_se_any"] == 0], (), ()),
             ("(d) all, father SE (x age) held fixed", v, ("f_se", "f_se_na"), XS))
    for y in ("ly", "lw"):
        for lab, q, ctrl, xfe in specs:
            o = profile(q, y, BT, XB, ctrl, xfe)
            md.append(f"| {y} | {lab} | {fmt(o['a'])} | {fmt(o['b'])} | {fmt(o['ch'])} | {fmt(o['chC'])} | "
                      f"{fmt(o['dif'])} | {c(o['fe'])} | {o['sons']:,} | {o['treated45']} |")
            RES[f"profile|{y}|{lab}"] = js(o)
            print(md[-1], flush=True)
    md.append("")

    # 3. sons and daughters
    a, py24, ch = R107.R24.load()
    rr = R107.frame(a, py24, ch)
    kids = rr.drop_duplicates("pid")[["pid", "fpid", "birth_year"]]
    rr = attach(rr, father_se(kids, py, X), rr["fpid"].notna())
    md += ["## 3. Sons and daughters (107's stacked design)", "",
           "| outcome | sample | sons: change | daughters: change | daughters - sons | sons: within x age | "
           "daughters: within x age | daughters - sons (within) | sons / daughters |", "|---" * 9 + "|"]
    for y in ("lw", "ly"):
        for lab, q, extra in (("all", rr, ()), ("without SE fathers", rr[rr["f_se"] == 0], ()),
                              ("all, father SE held fixed", rr, ("f_se", "f_se_na"))):
            o = R107.estimates(q, y, "f_sh_layoff", "f_sh_close", extra)
            md.append(f"| {y} | {lab} | {c(o['son_change'])} | {c(o['daughter_change'])} | {c(o['difference'])} | "
                      f"{c(o['son_fe'])} | {c(o['daughter_fe'])} | {c(o['difference_fe'])} | {o['n']['sons']:,} / "
                      f"{o['n']['daughters']:,} |")
            RES[f"sex|{y}|{lab}"] = {k: (list(t) if isinstance(t, tuple) else t) for k, t in o.items()}
            print(md[-1], flush=True)
    md.append("")

    # 4. the son's self-employment
    md += ["## 4. The son's self-employment", "",
           "### 4a. Self-employment by the father's (son-years with a valid code)", "",
           "| father | son self-employed 25-34 | 35-44 | 45-55 | sons |", "|---|---|---|---|---|"]
    s = r.dropna(subset=["selfemp"])
    s = s[s["nofa"] == 0]
    for lab, m in (("self-employed", s["f_se"] == 1), ("employee", (s["f_se"] == 0) & (s["f_se_na"] == 0))):
        q = s[m]
        cells = [q[q["age"].between(lo, hi)] for lo, hi in ((25, 34), (35, 44), (45, 55))]
        vals = [float(np.average(z["selfemp"], weights=z["wt"])) for z in cells]
        md.append(f"| {lab} | " + " | ".join(f"{x:.3f}" for x in vals) + f" | {q['pid'].nunique():,} |")
        RES[f"se_by_father|{lab}"] = vals
    md += ["", "### 4b. The layoff profile of the son's self-employment", "",
           "| sample | 25-29 | 45-49 | change | within son x age | sons |", "|---|---|---|---|---|---|"]
    q0 = r.dropna(subset=["selfemp"])
    BTs = Boot(r["fam68"].to_numpy(), r["race"].to_numpy())   # all son-years, as 118
    for lab, q, ctrl, xfe in (("(a) all sons", q0, (), ()), ("(b) without SE fathers", q0[q0["f_se"] == 0], (), ()),
                              ("(c) without fathers ever SE", q0[q0["f_se_any"] == 0], (), ()),
                              ("(d) all, father SE (x age) held fixed", q0, ("f_se", "f_se_na"), XS)):
        a0 = R91.band_fit(q, "selfemp", 0, BTs, COMPS, ["f_sh_layoff"], ctrl)["f_sh_layoff"]
        a4 = R91.band_fit(q, "selfemp", 4, BTs, COMPS, ["f_sh_layoff"], ctrl)["f_sh_layoff"]
        chs = (a4[0] - a0[0], a4[1] - a0[1])
        f = R91.fe_fit(q, "selfemp", XB + list(xfe))
        fe = (f["b"]["f_sh_layoff_xa"], float(np.sqrt(f["V"].loc["f_sh_layoff_xa", "f_sh_layoff_xa"])))
        md.append(f"| {lab} | {fmt(a0)} | {fmt(a4)} | {fmt(chs)} | {c(fe)} | {q['pid'].nunique():,} |")
        RES[f"se_profile|{lab}"] = js({"a": a0, "b": a4, "ch": chs, "fe": fe})
        print(md[-1], flush=True)
    md += ["", "### 4c. Where the cost sits, without sons of self-employed fathers (as 118 section 3)", "",
           "| outcome | spec | layoff share x age | interaction | son-years / sons |", "|---|---|---|---|---|"]
    g = lambda f, x: (f["b"][x], float(np.sqrt(f["V"].loc[x, x])))  # noqa: E731
    for y in ("ly", "lw"):
        q = r[r["lw"].notna() & (r["f_se"] == 0)].dropna(subset=["selfemp"]).copy()
        for lab, sub in (("employee years only", q["selfemp"] == 0), ("self-employed years only", q["selfemp"] == 1)):
            f = R91.fe_fit(q[sub], y, XB)
            md.append(f"| {y} | {lab} | {c(g(f, 'f_sh_layoff_xa'))} | | {f['n']:,} / {f['sons']:,} |")
            RES[f"split|{y}|{lab}"] = list(g(f, "f_sh_layoff_xa"))
        q["lay_self_xa"] = q["f_sh_layoff"] * q["selfemp"] * q["agec"]
        q["self_xa"] = q["selfemp"] * q["agec"]
        f = R91.fe_fit(q, y, XB + ["selfemp", "self_xa", "lay_self_xa"])
        md.append(f"| {y} | all years, layoff x age x self-employed | {c(g(f, 'f_sh_layoff_xa'))} | "
                  f"{c(g(f, 'lay_self_xa'))} | {f['n']:,} / {f['sons']:,} |")
        RES[f"inter|{y}"] = {"base": list(g(f, "f_sh_layoff_xa")), "inter": list(g(f, "lay_self_xa"))}
    md.append("")
    (OUT / "father_self_employment.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "father_self_employment.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
