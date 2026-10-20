r"""Are the shares of what is passed on attenuated by measurement error? (Fable addition B1, 2026-10-20)

The split of 75.WhatIsPassedOn.py writes the IGE as b0 = b + sum_k g_k d_k. Error in a component k biases g_k (its
partial relation to the son's outcome) towards zero and moves its share into the rest b; the NLSY97 column, measured
in one year, carries nothing. Here each component is measured twice, on two halves of the son's teen waves (13-19,
alternating in order: 1st, 3rd, 5th, 7th vs 2nd, 4th, 6th; the PSID is biennial after 1997, so wave parity would not
split those windows), and half A is instrumented by half B (Solon 1992 logic; errors that are independent across
the halves are removed, serially correlated transitory shocks are not, so the corrected shares are lower bounds).

COMPONENTS (both halves, from 24's head-and-wife panel data/ige_decomposition_panel.pkl; the father = fpid as head,
  the mother = the woman of the son's unit in that wave)
  wage    f_lw, m_lw     mean ln hourly wage over valid years in the half
  hours   f_lh, m_lh     mean ln annual hours over valid years; m_zero = share of the half's waves with zero hours
  spells  f_close, f_lay shares of waves with a plant closure / a layoff or firing (t or t-1; psid_displacement)
          f_un, f_zero   the father's shares unemployed (24's flag) / with zero hours
          m_un           the mother's share unemployed (24's flag where measured)
  A component missing in a half (parent absent, no valid year) takes the weighted mean and a flag (75's rule); the
  flags, 75's family-structure group and the state measures (g_ur, g_bart; not measured with error in this sense) are
  exogenous controls; f_vtr is left out (it needs >= 3 years in a half).
DESIGN: 75's son-years (sons 25-55, valid wage, PSID weights), the earnings IGE over 25-55 and at 25-29 / 45-49.
  (a) OLS split with the components measured on the whole window from the same waves (this script's measures);
  (b) OLS split with half-A measures;
  (c) 2SLS: g from the son's outcome on lyp, the half-A measures (instrumented by half B) and the controls; d_k = OLS
      gradient of the half-A measure in lyp (error in the outcome of that regression does not bias it); contribution
      g_k d_k; the rest = b0 - sum. Groups = wage, hours, spells. 200 cluster-bootstrap draws of 1968 families.
  Reliability of each half: the correlation of the two halves among sons with both.
Writes output/split_measurement_error.md / .json (aggregates only). Descriptive accounting.
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


R75 = _load("s75", "75.WhatIsPassedOn.py")
R74, R24 = R75.R74, R75.R24
c, dummies, Boot = R74.c, R74.dummies, R74.Boot
COMP = {"wage": ["f_lw", "m_lw"], "hours": ["f_lh", "m_lh", "m_zero"],
        "spells": ["f_close", "f_lay", "f_un", "f_zero", "m_un"]}
ALLC = [v for g in COMP.values() for v in g]
RES = {}


def halves(r):
    a = pd.read_pickle(R24.CACHE)
    a["unemp"] = pd.to_numeric(a["unemp"], errors="coerce")
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    sons = r.drop_duplicates("pid")[["pid", "fpid"]]
    k = py[py["child"] & py["age"].between(13, 19) & py["faminc"].between(R24.LO, R24.HI) & py["pid"].isin(sons["pid"])][
        ["pid", "wave", "int"]].sort_values(["pid", "wave"])
    k["half"] = k.groupby("pid").cumcount() % 2
    dp = pd.read_pickle(DATA / "psid_displacement.pkl")
    clo = set(zip(dp.loc[dp["strict"] == 1, "pid"], dp.loc[dp["strict"] == 1, "year"]))
    m = (dp["main"] == 1) & (dp["strict"] != 1)
    lay = set(zip(dp.loc[m, "pid"], dp.loc[m, "year"]))
    fa = a[a["head"] & (a["female"] == 0)][["pid", "wave", "valid", "lw", "lh", "unemp", "zero"]].rename(
        columns={"pid": "fpid"}).drop_duplicates(["fpid", "wave"])
    fw = k.merge(sons.dropna(), on="pid").merge(fa, on=["fpid", "wave"])
    yr = fw["wave"] - 1
    fw["f_close"] = [float((p, y) in clo or (p, y - 1) in clo) for p, y in zip(fw["fpid"], yr)]
    fw["f_lay"] = [float((p, y) in lay or (p, y - 1) in lay) for p, y in zip(fw["fpid"], yr)]
    wom = a[a["wife"] | (a["head"] & (a["female"] == 1))].drop_duplicates(["wave", "int"])
    mw = k.merge(wom[["wave", "int", "valid", "lw", "lh", "unemp", "hours"]], on=["wave", "int"])
    mw["m_zero"] = (mw["hours"] == 0).astype(float).where(mw["hours"].notna())
    out = {}
    for h in (0, 1, None):
        f = fw if h is None else fw[fw["half"] == h]
        w = mw if h is None else mw[mw["half"] == h]
        fv, wv = f[f["valid"] == True], w[w["valid"] == True]  # noqa: E712
        D = pd.DataFrame({"f_lw": fv.groupby("pid")["lw"].mean(), "f_lh": fv.groupby("pid")["lh"].mean(),
                          "f_close": f.groupby("pid")["f_close"].mean(), "f_lay": f.groupby("pid")["f_lay"].mean(),
                          "f_un": f.groupby("pid")["unemp"].mean(), "f_zero": f.groupby("pid")["zero"].mean()})
        M = pd.DataFrame({"m_lw": wv.groupby("pid")["lw"].mean(), "m_lh": wv.groupby("pid")["lh"].mean(),
                          "m_zero": w.groupby("pid")["m_zero"].mean(), "m_un": w.groupby("pid")["unemp"].mean()})
        out[{0: "A", 1: "B", None: "W"}[h]] = D.join(M, how="outer")
    return out


def prep(r, H):
    for tag, D in H.items():
        D = D.add_suffix(f"_{tag}")
        r = r.merge(D, left_on="pid", right_index=True, how="left")
    flags = []
    for v in ALLC:
        for tag in ("A", "B", "W"):
            col = f"{v}_{tag}"
            q = r[col].notna()
            r[f"{col}_na"] = (~q).astype(float)
            flags.append(f"{col}_na")
            r[col] = r[col].fillna(float(np.average(r.loc[q, col], weights=r.loc[q, "wt"])) if q.any() else 0.0)
    return r, flags


def split(d, y, tag, flags, iv, w0):
    """exact (OLS) or 2SLS split; returns {b0, group contributions, rest}."""
    M = [f"{v}_{tag}" for v in ALLC]
    exo = [v for v in R75.GROUPS["structure"] + R75.GROUPS["group"] if v in d] + [f for f in flags if f.endswith(f"_{tag}_na")
                                                                                 or (iv and f.endswith("_B_na"))]
    exo = [v for v in exo if d[v].std() > 0]
    A = np.column_stack([dummies(d["age"]), d[exo].to_numpy(float), np.ones(len(d))])
    x = d["lyp"].to_numpy(float)
    Y = d[y].to_numpy(float)
    Mx = d[M].to_numpy(float)
    sw = np.sqrt(w0)

    def wl(X, yy):
        return np.linalg.lstsq(X * sw[:, None], yy * sw if yy.ndim == 1 else yy * sw[:, None], rcond=None)[0]

    XA = np.column_stack([x, A])
    b0 = wl(XA, Y)[0]
    dlt = wl(XA, Mx)[0]                                       # gradient of each component in lyp
    X = np.column_stack([x, Mx, A])
    if iv:
        Zm = d[[f"{v}_B" for v in ALLC]].to_numpy(float)
        Z = np.column_stack([x, Zm, A])
        P = wl(Z, X)
        Xh = Z @ P
        g = wl(Xh, Y)
    else:
        g = wl(X, Y)
    gm = g[1:1 + len(M)]
    out = {"b0": b0}
    for gname, vs in COMP.items():
        ii = [ALLC.index(v) for v in vs]
        out[gname] = float(np.sum(gm[ii] * dlt[ii]))
    out["rest"] = b0 - sum(out[k] for k in COMP)
    return out


def run(d, y, tag, flags, iv, BT):
    w0 = d["wt"].to_numpy(float)
    pt = split(d, y, tag, flags, iv, w0)
    ri = BT.rows(d["fam68"].to_numpy())
    D = {k: [] for k in pt}
    for b in range(BT.cnt.shape[0]):
        wb = w0 * BT.cnt[b, ri]
        keep = wb > 0
        o = split(d[keep], y, tag, flags, iv, wb[keep])
        for k in pt:
            D[k].append(o[k])
    return pt, {k: np.array(v) for k, v in D.items()}


def main():
    r = R75.build()
    r = r[r["lw"].notna()].copy()
    H = halves(r)
    r, flags = prep(r, H)
    BT = Boot(r["fam68"].to_numpy(), r["race"].to_numpy())
    md = ["# Are the shares of what is passed on attenuated by measurement error? (Fable B1)", "",
          "Built by `96.SplitMeasurementError.py` (2026-10-20); design in its docstring. PSID sons 25-55, valid wage, "
          "PSID weights; components measured on the whole teen window (W), on half A, and half A instrumented by half B "
          "(IV); estimate (s.e.; p) from 200 cluster-bootstrap draws of 1968 families; share = contribution / IGE. "
          "*** p<0.01, ** p<0.05, * p<0.1. **Descriptive accounting.**", ""]
    one = r.drop_duplicates("pid")
    md += ["## 0. Reliability: correlation of the two halves (sons with both measured)", "",
           "| component | correlation A-B | sons |", "|---|---|---|"]
    for v in ALLC:
        q = one[(one[f"{v}_A_na"] == 0) & (one[f"{v}_B_na"] == 0)]
        rho = float(np.corrcoef(q[f"{v}_A"], q[f"{v}_B"])[0, 1]) if len(q) > 30 else np.nan
        md.append(f"| {v} | {rho:.3f} | {len(q):,} |")
        RES[f"rho|{v}"] = rho
    md.append("")
    for cell, sub in (("25-55", r), ("25-29", r[r["band"] == 0]), ("45-49", r[r["band"] == 4])):
        md += [f"## Ln earnings, {cell}", "", "| split | IGE | wage | hours | spells | rest | wage share | spells share | "
               "rest share |", "|---" * 9 + "|"]
        for lab, tag, iv in (("whole window, OLS", "W", False), ("half A, OLS", "A", False),
                             ("half A instrumented by half B", "A", True)):
            pt, D = run(sub, "ly", tag, flags, iv, BT)
            cells = [c((pt[k], float(np.nanstd(D[k], ddof=1)))) for k in ("b0", "wage", "hours", "spells", "rest")]
            shr = [c((100 * pt[k] / pt["b0"], float(np.nanstd(100 * D[k] / D["b0"], ddof=1))), 1)
                   for k in ("wage", "spells", "rest")]
            md.append(f"| {lab} | " + " | ".join(cells + shr) + " |")
            RES[f"{cell}|{lab}"] = {k: [float(pt[k]), float(np.nanstd(D[k], ddof=1))] for k in pt}
            RES[f"{cell}|{lab}|shares"] = {k: [float(pt[k] / pt["b0"]), float(np.nanstd(D[k] / D["b0"], ddof=1))]
                                           for k in ("wage", "hours", "spells", "rest")}
        md.append("")
        print(cell, "done", flush=True)
    (OUT / "split_measurement_error.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "split_measurement_error.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
