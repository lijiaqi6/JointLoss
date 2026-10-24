r"""Romano-Wolf step-down adjusted p-values for the two headline families (simulated JPE round; stricter than 110's Holm).

Family A, the layoff cost (6): band change 45-49 - 25-29 of the teen layoff share (91 A6b); within-son layoff x age
  (88 / 91); layoff minus closure change (91); band change and within-son slope with one job-end net (103 b); the rank
  change (108).
Family B, sons vs daughters (4): the daughters - sons difference in the change of ln wage and of ln earnings and in the
  within-person slopes of both (107 a).
One joint cluster bootstrap: 1968 families resampled with replacement within race (74's Boot logic), the same draw
applied to the son sample (75) and the child sample (24 / 107), so the dependence between the tests is kept. In each
draw every statistic is re-estimated with the PSID weight x the family's count; t*_k = (theta*_k - theta_k) / se_k with
se_k the bootstrap s.e.; Romano and Wolf (2005) step-down on |t| within each family. IGE_NBOOT sets the draws (default
1000). Writes output/romano_wolf.md / .json.
"""
import importlib.util
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import OUT  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R103 = _load("s103", "103.LayoffCohortRegime.py")
R107 = _load("s107", "107.LayoffSexDifference.py")
R108 = _load("s108", "108.LayoffRefereeChecks.py")
R91, R75, R24, R73 = R103.R91, R103.R75, R103.R24, R103.R91.R73
dummies = R91.dummies
COMPS, STRUCT = R91.COMPS, R91.STRUCT
NB = int(os.environ.get("IGE_NBOOT", 1000))
SEED = 20261024


def wls(X, y, w):
    sw = np.sqrt(w)
    return np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)[0]


def band_coefs(z, y, comps, focus, w):
    cols = [v for v in comps + STRUCT if z[v].std() > 0]
    X = np.column_stack([z["lyp"].to_numpy(float), z[cols].to_numpy(float), dummies(z["age"]), np.ones(len(z))])
    keep = w > 0
    b = wls(X[keep], z[y].to_numpy(float)[keep], w[keep])
    return [b[1 + cols.index(f)] for f in focus]


def fe_coef(Xc, y, ids, w, j=0):
    keep = w > 0
    M = R73.demean(np.column_stack([y[keep], Xc[keep]]), ids[keep], w[keep])
    return wls(M[:, 1:], M[:, 0], w[keep])[j]


def main():
    t0 = time.time()
    # ------------------------------------------------ son sample (75) with both layoff definitions and ranks
    r = R75.build()
    r = r.merge(R103.shares_b(r), on="pid", how="left")
    pres = r["nofa"] == 0
    for v in ("f_sh_layoff_b", "f_sh_close_b"):
        r[v] = r[v].where(pres, 0.0).fillna(0.0)
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    cohd = pd.get_dummies(r["coh5"], prefix="coh", drop_first=True).astype(float)
    r = pd.concat([r, cohd], axis=1)
    r["agec"] = (r["age"] - 40) / 10
    v = r[r["lw"].notna()].copy().reset_index(drop=True)
    v["rk"] = np.nan
    for _, idx in v.groupby(["age", "year"]).groups.items():
        z = v.loc[idx]
        v.loc[idx, "rk"] = R108.wpct(z["ly"].to_numpy(float), z["wt"].to_numpy(float))
    COMPS_B = [("f_sh_layoff_b" if x == "f_sh_layoff" else "f_sh_close_b" if x == "f_sh_close" else x) for x in COMPS]
    COH = list(cohd.columns)
    a_ = v["agec"].to_numpy()[:, None]
    XA = np.column_stack([v[["f_sh_layoff"] + ["lyp"] + [x for x in COMPS if x != "f_sh_layoff"] + STRUCT + COH].to_numpy(float) * a_,
                          dummies(v["age"])])
    XBb = np.column_stack([v[["f_sh_layoff_b"] + ["lyp"] + [x for x in COMPS_B if x != "f_sh_layoff_b"] + STRUCT + COH].to_numpy(float) * a_,
                           dummies(v["age"])])
    b0, b4 = v[v["band"] == 0], v[v["band"] == 4]
    # ------------------------------------------------ child sample (24 / 107)
    a, py, ch = R24.load()
    q = R107.frame(a, py, ch)
    X0 = ["lyp", "f_lw", "f_lh", "f_sh_unemp", "f_sh_zero", "f_vtr", "f_sh_close", "f_sh_layoff"]
    kL = X0.index("f_sh_layoff")
    Q = {}
    for y in ("lw", "ly"):
        d = q.dropna(subset=[y] + X0).reset_index(drop=True)
        s = d[d["band"].isin([0, 4])].reset_index(drop=True)
        bb4 = (s["band"] == 4).to_numpy(float)
        fe = s["female"].to_numpy(float)
        base = np.column_stack([s[X0].to_numpy(float), dummies(s["age"]), np.ones(len(s))])
        K = base.shape[1]
        Xs = np.column_stack([base, base * bb4[:, None], base * fe[:, None], base * (bb4 * fe)[:, None]])
        ag = d["agec"].to_numpy()[:, None]
        fd = d["female"].to_numpy()[:, None]
        Xw = np.column_stack([d[X0].to_numpy(float) * ag * fd, d[X0].to_numpy(float) * ag, dummies(d["age"]),
                              dummies(d["age"]) * fd])
        Q[y] = dict(s=s, Xs=Xs, js=3 * K + kL, d=d, Xw=Xw, jw=kL)
    print(f"built {time.time() - t0:.0f}s", flush=True)
    # ------------------------------------------------ joint bootstrap over 1968 families within race
    fams = pd.concat([v[["fam68", "race"]], q[["fam68", "race"]]]).drop_duplicates("fam68")
    fam_ids = fams["fam68"].to_numpy()
    pos = {f: i for i, f in enumerate(fam_ids)}
    rng = np.random.default_rng(SEED)

    def counts():
        cnt = np.zeros(len(fam_ids))
        for rc in fams["race"].unique():
            ids = np.where(fams["race"].to_numpy() == rc)[0]
            cnt[ids] = np.bincount(rng.integers(0, len(ids), len(ids)), minlength=len(ids))
        return cnt

    ix = {k: np.array([pos[f] for f in frame["fam68"]]) for k, frame in
          (("v", v), ("b0", b0), ("b4", b4), ("ls", Q["lw"]["s"]), ("ld", Q["lw"]["d"]), ("ys", Q["ly"]["s"]), ("yd", Q["ly"]["d"]))}
    NAMES_A = ["layoff band change", "within-son slope", "layoff minus closure change", "band change, one job-end net",
               "within-son slope, one job-end net", "rank change"]
    NAMES_B = ["daughters - sons, wage change", "daughters - sons, earnings change", "daughters - sons, wage within person",
               "daughters - sons, earnings within person"]

    def stats(cnt):
        w = lambda fr, k: fr["wt"].to_numpy(float) * cnt[ix[k]]  # noqa: E731
        g0 = band_coefs(b0, "ly", COMPS, ["f_sh_layoff", "f_sh_close"], w(b0, "b0"))
        g4 = band_coefs(b4, "ly", COMPS, ["f_sh_layoff", "f_sh_close"], w(b4, "b4"))
        h0 = band_coefs(b0, "ly", COMPS_B, ["f_sh_layoff_b"], w(b0, "b0"))
        h4 = band_coefs(b4, "ly", COMPS_B, ["f_sh_layoff_b"], w(b4, "b4"))
        k0 = band_coefs(b0, "rk", COMPS, ["f_sh_layoff"], w(b0, "b0"))
        k4 = band_coefs(b4, "rk", COMPS, ["f_sh_layoff"], w(b4, "b4"))
        wv = w(v, "v")
        yv, idv = v["ly"].to_numpy(float), v["pid"].to_numpy()
        A = [g4[0] - g0[0], fe_coef(XA, yv, idv, wv), (g4[0] - g0[0]) - (g4[1] - g0[1]), h4[0] - h0[0],
             fe_coef(XBb, yv, idv, wv), k4[0] - k0[0]]
        B = []
        for y, ks, kd in (("lw", "ls", "ld"), ("ly", "ys", "yd")):
            o = Q[y]
            ws = o["s"]["wt"].to_numpy(float) * cnt[ix[ks]]
            keep = ws > 0
            B.append(wls(o["Xs"][keep], o["s"][y].to_numpy(float)[keep], ws[keep])[o["js"]])
        for y, kd in (("lw", "ld"), ("ly", "yd")):
            o = Q[y]
            wd = o["d"]["wt"].to_numpy(float) * cnt[ix[kd]]
            B.append(fe_coef(o["Xw"], o["d"][y].to_numpy(float), o["d"]["pid"].to_numpy(), wd, o["jw"]))
        return np.array(A), np.array([B[0], B[1], B[2], B[3]])

    thA, thB = stats(np.ones(len(fam_ids)))
    print("point A", np.round(thA, 3), "B", np.round(thB, 3), flush=True)
    DA, DB = np.zeros((NB, 6)), np.zeros((NB, 4))
    for b in range(NB):
        DA[b], DB[b] = stats(counts())
        if (b + 1) % 50 == 0:
            print(f"draw {b + 1} {time.time() - t0:.0f}s", flush=True)

    def romano_wolf(th, D):
        se = D.std(axis=0, ddof=1)
        t = np.abs(th / se)
        T = np.abs((D - th) / se)
        order = np.argsort(-t)
        adj = np.empty(len(th))
        run = 0.0
        for i, k in enumerate(order):
            rest = order[i:]
            p = float(np.mean(T[:, rest].max(axis=1) >= t[k]))
            run = max(run, p)
            adj[k] = run
        return se, t, adj

    md = ["# Romano-Wolf step-down adjusted p-values (headline families)", "",
          f"Built by `114.RomanoWolf.py` (2026-10-24); design in its docstring. {NB} joint cluster-bootstrap draws of 1968 "
          "families within race; p (bootstrap) = 2 x normal tail of |t| with the bootstrap s.e.", ""]
    RES = {"nboot": NB}
    MT = json.load(open(OUT / "multiple_testing.json"))
    for fam, names, th, D, key in (("A. The layoff cost", NAMES_A, thA, DA, "A. The layoff cost|"),
                                   ("B. Sons vs daughters", NAMES_B, thB, DB, "B. Sons vs daughters|")):
        se, t, adj = romano_wolf(th, D)
        from scipy.stats import norm
        md += [f"## {fam}", "", "| test | estimate | bootstrap s.e. | p | Romano-Wolf adjusted p |", "|---|---|---|---|---|"]
        for n_, e, s_, tt, aa in zip(names, th, se, t, adj):
            p = 2 * norm.sf(tt)
            md.append(f"| {n_} | {e:.3f} | {s_:.3f} | {p:.4f} | {aa:.4f} |")
            RES[f"{fam}|{n_}"] = {"est": float(e), "se": float(s_), "p": float(p), "rw": float(aa)}
        md.append("")
    (OUT / "romano_wolf.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "romano_wolf.json", "w"), indent=1)
    print("\n".join(md))
    print(f"done {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
