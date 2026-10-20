r"""Data side of the Paper B structural model (2026-10-18).

1. The PSID long panel in the simulator's format (one row per interview of a Black or White son as male head, ages
   25-55): pid, fam68, wave, age, lw (valid ln hourly wage of the income year, else NaN), zero (zero annual hours), G
   (current job is a well-paid, high-later-growth cell: 35 'kset' == 1), gap (waves since the previous interview of the
   son), stay (27's same-employer flag), disp (main displacement - closure / move or layoff / firing - in an income
   year from the previous wage year to the current one), black, x (ln parental income, 13-19 mean), e (completed years
   of schooling). Built through 35.EarlyIndustryLatePayoff.py's frame (read only).
2. The data moments (core.moments, order core.MOMENT_NAMES) and their cluster-bootstrap standard errors (500 draws of
   1968 families).
3. Closed-form first steps (model document, 'Analytical results'): accumulation by NLS on stayers' wage growth (decisions
   do not depend on h, so stayers' growth is not selected on the human capital shock); the transitory and permanent
   variances from the variance and lag-1 autocovariance of stayers' annual growth; the displacement logit on annual
   pairs; entry-wage OLS; the access logit on the early job type. Used as starting values and as checks.
Writes model/output/data_panel.pkl, data_moments.json, theta_start.json, first_steps.md.
"""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.optimize import least_squares

HERE = Path(__file__).resolve().parent
IGE = HERE.parent
sys.path.insert(0, str(IGE))
sys.path.insert(0, str(HERE))
from common import DATA  # noqa: E402
import core  # noqa: E402

OUTD = HERE / "output"
OUTD.mkdir(exist_ok=True)
NBOOT = 500


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, IGE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def build_panel():
    f = OUTD / "data_panel.pkl"
    if f.exists():
        return pd.read_pickle(f)
    R35 = _load("e35", "35.EarlyIndustryLatePayoff.py")
    D32, D27 = R35.D32, R35.D27
    W = D32.ind_crosswalks()
    XWD = D27.crosswalks()
    M = D32.morg_measures(D32.morg_micro(W, XWD))
    R35.STEEP32 = set(M["steep"])
    MF = R35.morg_flex(M)
    R35.data_sets(MF)
    R35.MF_G = MF
    r = D32.son_panel(W, M)
    rc = r.attrs["rc"]
    r.attrs = {}
    r["fam68"] = r["fam68"].astype(float)
    d = R35.prep(r, MF, W, rc)
    d = d[d["race"].isin(["Black", "White"]) & d["age"].between(25, 55)].copy()
    ed = d.groupby("pid")["educ"].max()
    d["e"] = d["pid"].map(ed)
    d = d[d["lyp"].notna() & d["e"].notna()].sort_values(["pid", "wave"]).reset_index(drop=True)
    P = pd.DataFrame({"pid": d["pid"].astype(int), "fam68": d["fam68"], "wave": d["wave"].astype(int),
                      "age": d["age"].round().astype(int), "byear": d["birth_year"].astype(int),
                      "lw": d["lw"].where(d["valid"].astype(bool)), "zero": d["zero"].astype(float),
                      "G": (d["kset"] == 1).astype(float).where(d["kset"].notna()), "stay": d["stay"],
                      "black": (d["race"] == "Black").astype(float), "x": d["lyp"], "e": d["e"]})
    first = P["pid"].ne(P["pid"].shift())
    P["gap"] = (P["wave"] - P["wave"].shift()).where(~first)
    dp = pd.read_pickle(DATA / "psid_displacement.pkl")
    dy = set(zip(dp.loc[dp["main"] == 1, "pid"], dp.loc[dp["main"] == 1, "year"]))
    gap = P["gap"].fillna(0).astype(int)
    hit = np.zeros(len(P), bool)
    for k in range(0, 3):
        yrs = P["wave"] - 1 - k
        hit |= np.array([(p, y) in dy for p, y in zip(P["pid"], yrs)]) & (k <= gap).to_numpy()
    P["disp"] = np.where(first, np.nan, hit.astype(float))
    P.loc[first, "stay"] = np.nan
    P.to_pickle(f)
    return P


def arrays(P):
    return {c: P[c].to_numpy() for c in ("pid", "wave", "age", "lw", "zero", "G", "gap", "disp", "stay", "black", "x",
                                         "e")}


def constants(P):
    kid = P.drop_duplicates("pid")
    return {"terc": tuple(kid["x"].quantile([1 / 3, 2 / 3]).to_list()), "xbar": float(kid["x"].mean())}


def bootstrap(P, C):
    """cluster bootstrap over 1968 families on arrays (duplicated families get new person ids)."""
    A = arrays(P)
    fam = P["fam68"].to_numpy()
    fams, inv = np.unique(fam, return_inverse=True)
    order = np.argsort(inv, kind="stable")
    bounds = np.r_[0, np.cumsum(np.bincount(inv))]
    rows = [order[bounds[i]:bounds[i + 1]] for i in range(len(fams))]
    rng = np.random.default_rng(2026)
    draws = []
    for b in range(NBOOT):
        pick = rng.integers(0, len(fams), len(fams))
        idx = np.concatenate([rows[f] for f in pick])
        copy = np.repeat(np.arange(len(pick)), [len(rows[f]) for f in pick])
        Q = {c: v[idx] for c, v in A.items()}
        Q["pid"] = Q["pid"].astype(np.int64) + 10_000_000 * (copy.astype(np.int64) + 1)
        o = np.lexsort((Q["wave"], Q["pid"]))
        Q = {c: v[o] for c, v in Q.items()}
        draws.append(core.moments(Q, C))
        if b % 100 == 0:
            print("boot", b, flush=True)
    return np.array(draws)


def first_steps(P, C):
    A = arrays(P)
    out, md = {}, ["# Closed-form first steps (starting values and checks)", ""]
    pid, lw, gap = A["pid"], A["lw"], A["gap"]
    newp = np.r_[True, pid[1:] != pid[:-1]]
    prev = np.r_[np.nan, lw[:-1]]
    prev[newp] = np.nan
    g = (lw - prev) / gap
    st = (np.isfinite(g) & (gap >= 1) & (gap <= 2) & (A["wave"] >= 1985) & (A["stay"] == 1) & (A["disp"] == 0)
          & np.isfinite(A["G"]))
    amid = A["age"] - gap / 2
    ec, bl, G = A["e"] - 12, A["black"], A["G"]

    def resid(th):
        gO, gG, lrho, g1, dg1 = th
        f = (np.where(G[st] == 1, gG, gO) + (g1 + dg1 * bl[st]) * ec[st]) * np.exp(-np.exp(lrho) * (amid[st] - 18))
        return g[st] - f
    fit = least_squares(resid, x0=[0.05, 0.08, np.log(0.05), 0.005, -0.002])
    J = fit.jac
    s2 = np.mean(fit.fun ** 2)
    cov = np.linalg.pinv(J.T @ J) * s2
    for nm_, v, se in zip(["gO", "gG", "lrho", "g1", "dg1"], fit.x, np.sqrt(np.diag(cov))):
        out[nm_] = float(v)
        md.append(f"- {nm_}: {v:.4f} (s.e. {se:.4f}; homoskedastic, for orientation)")
    # variances from annual stayer growth
    z = st & (gap == 1)
    prev_g = np.r_[np.nan, g[:-1]]
    prev_z = np.r_[False, z[:-1]]
    zz = z & prev_z & ~newp
    ac = np.cov(g[zz], prev_g[zz])[0, 1]
    vg = np.var(g[z])
    s_eps2 = max(-ac, 0.005)
    drift_var = np.var((g[st] - fit.fun)[z[st]]) if z[st].any() else 0.0
    s_eta2 = max(vg - 2 * s_eps2 - drift_var, 0.002)
    out["lsigeps"], out["lsigeta"] = float(0.5 * np.log(s_eps2)), float(0.5 * np.log(s_eta2))
    md.append(f"- transitory variance = -lag-1 autocovariance of annual stayer growth = {s_eps2:.4f}; permanent "
              f"variance = Var(growth) - 2 x transitory - drift dispersion = {s_eta2:.4f} (Var = {vg:.4f}, autocov = "
              f"{ac:.4f}, N pairs {zz.sum():,})")
    # displacement logit (annual pairs)
    pr = np.isfinite(A["disp"]) & (gap == 1) & np.isfinite(prev) & np.isfinite(lw)
    X = sm.add_constant(np.column_stack([A["x"][pr] - C["xbar"], bl[pr]]))
    lg = sm.Logit(A["disp"][pr], X).fit(disp=0)
    out["d0W"], out["d1"] = float(lg.params[0]), float(lg.params[1])
    out["d0B"] = float(lg.params[0] + lg.params[2])
    md.append(f"- displacement logit (annual pairs): constant {lg.params[0]:.3f}, x {lg.params[1]:.3f}, Black "
              f"{lg.params[2]:.3f}")
    # entry wage OLS at 25-29
    s = (A["age"] <= 29) & np.isfinite(lw)
    X = sm.add_constant(np.column_stack([A["x"][s] - C["xbar"], ec[s], bl[s], bl[s] * ec[s]]))
    ol = sm.OLS(lw[s], X).fit()
    out["b0"], out["bx"], out["b1"], out["muB"], out["db1"] = (float(ol.params[0]), float(ol.params[1]),
                                                              float(ol.params[2]), float(ol.params[3]),
                                                              float(ol.params[4]))
    out["lsig0"] = float(0.5 * np.log(max(np.var(ol.resid) - s_eps2 - 0.03, 0.02)))
    md.append(f"- entry wage OLS (25-29): constant {ol.params[0]:.3f}, x {ol.params[1]:.3f}, schooling "
              f"{ol.params[2]:.3f}, Black {ol.params[3]:.3f}, Black x schooling {ol.params[4]:.3f}")
    # access logit on the early job type
    kid = P[(P["age"] <= 34) & P["G"].notna()].groupby("pid").agg(G=("G", "mean"), x=("x", "first"),
                                                                    e=("e", "first"), black=("black", "first"))
    X = sm.add_constant(np.column_stack([kid["x"] - C["xbar"], kid["e"] - 12, kid["black"]]))
    la = sm.Logit((kid["G"] > 0.5).astype(float), X).fit(disp=0)
    out["a0"], out["a1"], out["a2"], out["a3"] = (float(v) for v in la.params)
    md.append(f"- access logit on the early job type: {', '.join(f'{v:.3f}' for v in la.params)}")
    zero = np.nanmean(A["zero"])
    dl = core.logistic(out["d0W"])
    lam_u = min(0.9, dl * (1 - zero) / max(zero, 0.01))
    out["llam_u"] = float(np.log(lam_u / (1 - lam_u)))
    out["llam_e"] = float(np.log(0.2 / 0.8))
    out["muG"], out["lsigm"], out["du"] = 0.10, float(np.log(0.20)), 0.10
    th = np.array([out[p] for p in core.PARAMS])
    return th, md


def main():
    P = build_panel()
    C = constants(P)
    A = arrays(P)
    m = core.moments(A, C)
    print("data moments computed", flush=True)
    th, md = first_steps(P, C)
    B = bootstrap(P, C)
    np.save(OUTD / "boot_moments.npy", B)                          # 500 x 66 draws: sandwich s.e. (estimate.py)
    sd = np.nanstd(B, axis=0, ddof=1)
    json.dump({"names": core.MOMENT_NAMES, "m": m.tolist(), "sd": sd.tolist(), "C": C,
               "n_sons": int(P["pid"].nunique()), "n_rows": int(len(P))},
              open(OUTD / "data_moments.json", "w"), indent=1)
    json.dump(dict(zip(core.PARAMS, th.tolist())), open(OUTD / "theta_start.json", "w"), indent=1)
    md += ["", "| moment | data | bootstrap s.e. |", "|---|---|---|"]
    md += [f"| {n} | {v:.4f} | {s:.4f} |" for n, v, s in zip(core.MOMENT_NAMES, m, sd)]
    (OUTD / "first_steps.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[:20]))


if __name__ == "__main__":
    main()
