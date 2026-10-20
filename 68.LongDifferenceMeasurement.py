r"""Is the PSID / NLSY79 disagreement on H4 a matter of how parental income is measured? (Paper B, Fable second
ten-hour plan, Block 1, 2026-10-19.)

Statistic: as in 67.LongDifferenceH4.py, the change of a son's own mean log hourly wage between 25-29 and 35-39 (ten
years) or 45-49 (twenty) on log parental income, by race, raw and net of years of schooling.

  (a) PSID read through other parental measures on the same sons: the 13-19 mean (the paper's), the 12-17 mean and
      one year at 16 (data/psid_kids.pkl, lpinc_av and lpinc_pt).
  (b) Errors-in-variables correction with known reliability ratios (lambda): beta = (S - D)^{-1} s_xy, S the covariance
      of (x, schooling), D = diag((1 - lambda) var(x), 0); PSID 13-19 and 12-17 means W 0.650 / B 0.631, one year
      W 0.585 / B 0.565 (4.Estimates.py); NLSY79 its own one-year ratio W 0.552 / B 0.556 (age_profile_round2.md A6;
      its 1979-81 mean is somewhat more reliable, so this over-corrects slightly). 200 cluster-bootstrap draws.
  (c) Model E with the PSID son's one-year measure in place of the 13-19 mean that generated its wages: the
      statistic on the simulated panel (seeds 7-16, R = 20) regressed on the one-year measure.
  (d) PSID cohorts born 1957-64 (the NLSY79's) with the 13-19 mean.
Writes output/long_difference_measures.json / .md and paperB_age_profile/tab_h4measure.tex.
Run from IGE/ with IGE_STEPS=age,rehire,xacc IGE_FIX=muG,du IGE_R=20.
"""
import importlib.util
import json
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

IGE = Path(__file__).resolve().parent
OUT = IGE / "output"
sys.path.insert(0, str(IGE / "model"))
import core  # noqa: E402
import estimate as est  # noqa: E402

spec = importlib.util.spec_from_file_location("e67", IGE / "67.LongDifferenceH4.py")
L67 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(L67)

LAM = {"psid13": (0.650, 0.631), "psid1217": (0.650, 0.631), "psid1": (0.585, 0.565), "nlsy": (0.552, 0.556)}
NB = 200


def eiv(d, lam):
    """corrected x coefficient of y on [1, x, controls]; d has y, x and control columns (already complete)."""
    Z = d.drop(columns=["y", "cl"]).to_numpy(float)
    Zc = Z - Z.mean(0)
    S = Zc.T @ Zc / len(Z)
    s = Zc.T @ (d["y"].to_numpy() - d["y"].mean()) / len(Z)
    S2 = S.copy()
    S2[0, 0] -= (1 - lam) * S[0, 0]
    return float(np.linalg.solve(S2, s)[0])


def est_group(t, horizon, xcol, ctrl, lam_wb, rng):
    out = {}
    t = t.assign(y=t[f"m{horizon}"] - t["m2529"])
    for g, rv, lam in (("White", 0, lam_wb[0]), ("Black", 1, lam_wb[1])):
        d = t[t["black"] == rv][["y", xcol, *ctrl, "cl"]].dropna().rename(columns={xcol: "x"})
        d = d[["y", "x", *ctrl, "cl"]]
        raw = eiv(d, 1.0)
        cor = eiv(d, lam)
        cls = d["cl"].to_numpy()
        u, inv = np.unique(cls, return_inverse=True)
        rows = [np.where(inv == i)[0] for i in range(len(u))]
        br, bc = [], []
        for _ in range(NB):
            pick = rng.integers(0, len(u), len(u))
            dd = d.iloc[np.concatenate([rows[i] for i in pick])]
            br.append(eiv(dd, 1.0))
            bc.append(eiv(dd, lam))
        out[g] = dict(raw=raw, raw_se=float(np.std(br, ddof=1)), cor=cor, cor_se=float(np.std(bc, ddof=1)), n=len(d),
                      draws_raw=br, draws_cor=bc)
    for k in ("raw", "cor"):
        dd = np.array(out["White"][f"draws_{k}"]) - np.array(out["Black"][f"draws_{k}"])
        out["White - Black"] = out.get("White - Black", {})
        out["White - Black"][k] = out["White"][k] - out["Black"][k]
        out["White - Black"][f"{k}_se"] = float(np.std(dd, ddof=1))
    for g in ("White", "Black"):
        out[g].pop("draws_raw")
        out[g].pop("draws_cor")
    return out


def model_task(args):
    th, seed, x1 = args
    T = est.G_["T"]
    idx = np.repeat(np.arange(T.n), 20)
    _, P = est.sim_moments(th, idx=idx, Dr=core.Draws(len(idx), seed))
    res = core.longdiff(P)
    P1 = dict(P)
    P1["x"] = x1[idx[P["pid"]]]
    keep = np.isfinite(P1["x"])
    P1 = {k: v[keep] for k, v in P1.items()}
    r1 = core.longdiff(P1)
    return {**{f"x13_{k}": v for k, v in res.items()}, **{f"x1_{k}": v for k, v in r1.items()}}


def star(p):
    return "^{***}" if p < 0.01 else "^{**}" if p < 0.05 else "^{*}" if p < 0.10 else ""


if __name__ == "__main__":
    rng = np.random.default_rng(2026)
    ps = L67.psid_sons()
    kids = pd.read_pickle(IGE / "data" / "psid_kids.pkl").set_index("pid")
    ps["x1"] = kids["lpinc_pt"].reindex(ps.index)
    ps["x1217"] = kids["lpinc_av"].reindex(ps.index)
    P = pd.read_pickle(IGE / "model" / "output" / "data_panel.pkl")
    by = P.drop_duplicates("pid").set_index("pid")["byear"]
    ps["byear"] = by.reindex(ps.index)
    nl = L67.nlsy_sons()
    R = {}
    for h in ("3539", "4549"):
        for ctrl, cl in (([], "raw"), (["e"], "net")):
            R[(h, cl, "PSID 13-19 mean")] = est_group(ps, h, "x", ctrl, LAM["psid13"], rng)
            R[(h, cl, "PSID 12-17 mean")] = est_group(ps, h, "x1217", ctrl, LAM["psid1217"], rng)
            R[(h, cl, "PSID one year (16)")] = est_group(ps, h, "x1", ctrl, LAM["psid1"], rng)
            R[(h, cl, "PSID born 1957-64")] = est_group(ps[ps["byear"].between(1957, 1964)], h, "x", ctrl,
                                                        LAM["psid13"], rng)
            R[(h, cl, "NLSY79 1979-81 mean")] = est_group(nl, h, "x", ctrl, LAM["nlsy"], rng)
    # model
    kid_pids = P.drop_duplicates("pid")["pid"].to_numpy()
    x1_by_type = kids["lpinc_pt"].reindex(kid_pids).to_numpy()
    E = json.load(open(IGE / "model" / "output" / "final_x4" / "estimates_E.json"))
    th = core.theta_vec(E["E"]["theta"])
    est.G_.update(est.setup())
    with Pool(est.WORKERS, initializer=est.init_worker) as pool:
        mr = pool.map(model_task, [(th, s, x1_by_type) for s in range(7, 17)])
    M = {k: (float(np.mean([r[k] for r in mr])), float(np.std([r[k] for r in mr], ddof=1))) for k in mr[0]}
    out = {"lambda": LAM, "results": {f"{h}|{c}|{s}": v for (h, c, s), v in R.items()}, "model": M}
    json.dump(out, open(OUT / "long_difference_measures.json", "w"), indent=1)
    L = ["# H4 long differences by parental-income measure (raw and EIV-corrected), and the model", "",
         "| horizon | controls | measure | group | raw | (s.e.) | corrected | (s.e.) | n |", "|---|---|---|---|---|---|---|---|---|"]
    for (h, c, s), v in R.items():
        for g in ("White", "Black", "White - Black"):
            r = v[g]
            L.append(f"| {h} | {c} | {s} | {g} | {r['raw']:.4f} | ({r['raw_se']:.4f}) | {r['cor']:.4f} | "
                     f"({r['cor_se']:.4f}) | {r.get('n', '')} |")
    L += ["", "Model E (mean, seed s.d.): " + "; ".join(f"{k} {v[0]:.4f} ({v[1]:.4f})" for k, v in M.items()
                                                       if "_n_" not in k)]
    (OUT / "long_difference_measures.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))
