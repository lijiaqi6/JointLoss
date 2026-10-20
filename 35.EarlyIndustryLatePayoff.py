r"""Early industry, late payoff: do sons of richer (and White) parents sort into finance, law and professional services
by 25-34, where wages take off only after 35? Nonlinear industry and occupation x industry cell profiles. (2026-10-17)

Question (PI): 32.IndustryCareers.py found that the industry component of the son's wage gradient is in place by 25-34
and that industry career slopes carry only ~8% of the pooled post-35 rise of wage persistence and ~5% of the change of
the Black-White gap. But 32's slope B_j is LINEAR in age, an industry AVERAGE, CROSS-SECTIONAL, and attached to the
CURRENT industry; a payoff that starts after 35 is understated by a line. The PI's hypothesis predicts exactly the early
sorting: sons enter finance / law / professional services (and, within them, the fast-track occupations) by 25-34, where
wages do not grow faster before 34 but take off after 35. This file:
  HEADLINE (H): replaces P_j + B_j t by the son's industry's FULL NONLINEAR profile from CPS MORG (industry x five-year
      age-band effects 25-29 ... 60-64 relative to men of the same age; and a piecewise-linear profile with knots at 30,
      35 and 45), for the current industry and for the industry fixed at 25-34, and then for occupation x industry CELLS
      (11 occupation groups x 33 industry groups); shares reported next to the linear-B share on the same son-years.
  B   how much of the cross-industry (and cross-cell) variance in wage growth after 35 the linear B misses.
  A   growth after 35 by the industry at 25-34 (son-level and within person), and Gelbach short vs long regressions with
      early-industry (early cell, early occupation) x age-band fixed effects (any profile, estimated in the PSID).
  C   fast track inside finance / law / professional services: parental-income gradient of post-35 growth within them.
  D   special cells (lawyers in legal services, managers / financial specialists in finance, managers / professionals in
      professional services): shares by parental income and race, growth after 35, contribution.
  F   following the father at the cell level (son in the father's occupation group x industry group cell), next to 32's
      industry-group and occupation-group following.
  E   NLSY79 replication of H, A and C.
DESCRIPTIVE ACCOUNTING: sons select into industries, occupations and cells; nothing here is a causal effect.

DATA (all read through 32's builders; nothing raw is written)
  PSID  32's son panel (27 -> 24 frame: 6.IGEMain parents, male heads 25-55, valid wage years; industry harmonised to
        ind1990ddx / 33 groups; occupation occ1990dd and 27's 11 groups; father's codes at son ages 12-18). Race of the
        parental head at 16.
  CPS MORG 1992-2002 men 25-64 (32's cache data/industry_careers_morg.pkl; rel = ln w minus the year's weighted mean).
  NLSY79 32's CPS-job panel (men living with a parent in 1979; industry and occupation of the CPS job at each round).
DEFINITIONS
  MORG nonlinear profiles (men 25-64): rel_a = rel minus the weighted mean rel of all men of the same single year of
        age. Band profile Q_jb = weighted mean of rel_a in industry j and five-year band b (25-29 ... 60-64), so Q is the
        industry's wage relative to men of the same age (any age shape). Level = Q averaged over bands with the all-men
        age weights; profile = Q_jb - level (the nonlinear analogue of B_j t). Piecewise linear: rel = f(age) + a_j +
        sum_k b_jk k_k(age), knots 30 / 35 / 45 (segment slopes 25-30, 30-35, 35-45, 45-64 per 10 years; common quartic
        f; exact FWL), normalised to the employment-weighted average industry; level = age-weighted mean, profile = the
        rest. Fine industries with < 200 men take their group's values, fine x band cells < 30 men their group's band.
        Synthetic-cohort slopes (robustness, men 25-55): within industry, rel on 5-year birth-cohort FE + s1 + s2
        (s1 = min(age-35,0)/10, s2 = max(age-35,0)/10).
  Cells: 11 occupation groups (27) x 33 industry groups; a cell's band value is its own if the cell has >= 200 men and
        the cell x band >= 30 men, else the additive fallback occupation-group(b) + industry-group(b) (two-way model of
        rel_a fitted by backfitting in each band).
  Current industry measures in the PSID / NLSY79 use 32's weighted crosswalk (map_codes); early ones the modal
        ind1990ddx code (group values if missing in MORG).
  Early industry: modal industry group over the son's 25-34 son-years with a valid wage and a mapped industry; early
        fine industry = modal ind1990ddx within that group; early occupation, early cell (occupation group x industry
        group) and early special cell = modal over the 25-34 son-years with both codes.
  DATA-DEFINED SETS (main groupings, PI 2026-10-17): all occupation group x industry group cells (and, secondarily, the
        33 industry groups) are ranked by their MORG nonlinear profile: level = age-weighted relative wage, later growth
        = band growth (35-39) -> (50-54). 'High-paid' = top quartile of men's employment by level, 'high later growth' =
        top quartile by later growth; sets: both (headline), high-paid only, high later growth only, neither. A son's
        early set = the set of his modal cell at 25-34. Pre-chosen named industries / cells below are illustrative only.
  Illustrative industry sets (early): finance / insurance = banking, credit, securities + insurance; legal / professional = legal
        services + engineering / accounting / research / consulting; other steep = 32's top-quartile linear-slope groups
        not in these two; rest = everything else (incl. real estate). FLP = finance / insurance + legal / professional.
  Special cells (Section D): (1) lawyers and judges (occ1990dd 178) in legal services; (2) managers (3-22), accountants
        / auditors (23), underwriters (24), other financial specialists (25), management analysts (26), securities and
        financial services sales (255) in finance / insurance; (3) managers and professional-specialty occupations in
        professional services; (4) managers and professionals elsewhere; (5) everyone else.
  Growth: Delta(40-55) = mean ln wage at 40-55 minus mean ln wage at 25-34 (son-level; also 35-55 and 45-55).
  Father's cell: modal occupation group x industry group over his head-waves with the son aged 12-18 (32 Section 4).
ESTIMATION  27's stacked influence-function machinery (clusters = 1968 family; NLSY79 1979 household); pooled =
  Black + White weighted, by race unweighted. Wage persistence: son-years in a band, outcome on ln parental income,
  Lee-Solon controls (NLSY79: age quartic + birth-year FE). Gelbach: contribution of a set of fixed effects =
  coefficient without them minus coefficient with them, on the same son-years, estimated separately in each band.
Every table: one regression per column (outcome in the header), regressors as rows, N / clusters at the bottom,
coefficient (s.e.; p) with *** p<0.01, ** p<0.05, * p<0.1.
Writes output/early_industry_late_payoff.md, .csv, .png. No caches.
"""
import importlib.util
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd

from common import OUT, HERE

warnings.simplefilter("ignore", FutureWarning)
warnings.simplefilter("ignore", RuntimeWarning)
warnings.simplefilter("ignore", pd.errors.PerformanceWarning)


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


D32 = _load("d32", "32.IndustryCareers.py")
D27 = D32.D27
RES, comb, ratio, cell, one, table = D27.RES, D27.comb, D27.ratio, D27.cell, D27.one, D27.table
ctrl_lsn, ctrl_ageyr, run_cells = D27.ctrl_lsn, D27.ctrl_ageyr, D27.run_cells
GNAMES, group_of, L, Dch, K, safe, dummies, mode = (D32.GNAMES, D32.group_of, D32.L, D32.Dch, D32.K, D32.safe,
                                                    D32.dummies, D32.mode)
ONAMES = [g[2] for g in D27.GROUPS]
GROUPS3 = [("P", "Pooled (weighted)"), ("B", "Black"), ("W", "White")]
GROUPS4 = GROUPS3 + [("BW", "Black - White")]
BANDS = [(25, 34), (35, 44), (45, 55), (35, 55)]
B5 = [f"{25 + 5 * k}-{29 + 5 * k}" for k in range(8)]
QC = [f"Q{k}" for k in range(8)]
SPC = ["sa", "sb1", "sb2", "sb3", "sb4"]
MIN_FINE, MIN_BAND = 200, 30
G_ = GNAMES.index
FININS = {G_("Finance: banking, credit, securities"), G_("Insurance")}
LEGAL, PROF = G_("Legal services"), G_("Professional services (engineering, accounting, research, consulting)")
LEGPRO = {LEGAL, PROF}
FLP = FININS | LEGPRO
CELLN = {1: "lawyers in legal services", 2: "managers / financial specialists in finance / insurance",
         3: "managers / professionals in professional services", 4: "managers / professionals elsewhere",
         5: "all other"}
FIN_OCC = set(range(3, 23)) | {23, 24, 25, 26, 255}
CSV = []
NAN3 = (np.nan,) * 3
STEEP32 = set()
MF_G = None


def rec(tab, sample, outcome, term, t, n=np.nan, **kw):
    b, se, p = t
    CSV.append(dict(table=tab, sample=sample, outcome=outcome, term=term, coef=b, se=se, p=p, n=n, **kw))


def sc(terms):
    return cell(safe(terms))


def sratio(num, den):
    return ratio(num, den) if all(k in RES for k, _ in num + den) else NAN3


def wsd(x, w):
    x, w = np.asarray(x, float), np.asarray(w, float)
    ok = np.isfinite(x) & np.isfinite(w)
    m = np.average(x[ok], weights=w[ok])
    return float(np.sqrt(np.average((x[ok] - m) ** 2, weights=w[ok])))


def wcorr(x, y, w):
    x, y, w = (np.asarray(v, float) for v in (x, y, w))
    ok = np.isfinite(x) & np.isfinite(y) & np.isfinite(w)
    x, y, w = x[ok], y[ok], w[ok]
    mx, my = np.average(x, weights=w), np.average(y, weights=w)
    return float(np.average((x - mx) * (y - my), weights=w) /
                 np.sqrt(np.average((x - mx) ** 2, weights=w) * np.average((y - my) ** 2, weights=w)))


def spl_basis(age):
    a = np.asarray(age, float)
    return np.column_stack([np.ones(len(a)), (np.minimum(a, 30) - 30) / 10, (np.clip(a, 30, 35) - 30) / 10,
                            (np.clip(a, 35, 45) - 35) / 10, (np.maximum(a, 45) - 45) / 10])


def band5(age):
    return np.clip((np.asarray(age, float) - 25) // 5, 0, 7).astype(int)


# ================================================================ CPS MORG nonlinear industry / cell profiles
def within_basis(v, gi, G, Bm, w):
    k = Bm.shape[1]
    S = np.zeros((G, k, k))
    R = np.zeros((G, k))
    for a in range(k):
        R[:, a] = np.bincount(gi, w * Bm[:, a] * v, G)
        for b in range(a, k):
            S[:, a, b] = S[:, b, a] = np.bincount(gi, w * Bm[:, a] * Bm[:, b], G)
    coef = (np.linalg.pinv(S) @ R[:, :, None])[:, :, 0]
    return v - (Bm * coef[gi]).sum(1), coef


def spline_fit(m, lev):
    """rel = f(age) + a_j + sum_k b_jk k_k(age), knots 30/35/45, common quartic (exact FWL)."""
    gi, gu = pd.factorize(m[lev])
    G = len(gu)
    w, y = m["wt"].to_numpy(), m["rel"].to_numpy()
    Bm = spl_basis(m["age"].to_numpy())
    u = (m["age"].to_numpy() - 40) / 10
    Z = np.column_stack([u ** 2, u ** 3, u ** 4])
    Zr = np.column_stack([within_basis(Z[:, k], gi, G, Bm, w)[0] for k in range(3)])
    yr = within_basis(y, gi, G, Bm, w)[0]
    gam = np.linalg.solve(Zr.T @ (Zr * w[:, None]), Zr.T @ (yr * w))
    _, coef = within_basis(y - Z @ gam, gi, G, Bm, w)
    return pd.DataFrame(coef, index=gu, columns=SPC)


def synthetic(m, lev, min_n=MIN_FINE):
    out = {}
    for j, z in m.groupby(lev):
        if len(z) < min_n:
            continue
        coh = ((z["year"] - z["age"]) // 5).astype(int)
        X = np.column_stack([z["s1"], z["s2"], pd.get_dummies(coh, dtype=float).to_numpy()])
        sw = np.sqrt(z["wt"].to_numpy())
        b = np.linalg.lstsq(X * sw[:, None], z["rel"].to_numpy() * sw, rcond=None)[0]
        out[j] = (b[0], b[1])
    return pd.DataFrame(out, index=["B1c", "B2c"]).T


def wmean_by(df, keys, col="rel_a"):
    g = df.assign(_wx=df[col] * df["wt"]).groupby(keys)
    return g["_wx"].sum() / g["wt"].sum(), g.size()


def morg_flex(M):
    m = pd.read_pickle(D32.C_MORG)
    m["grp"] = group_of(m["ddx"].to_numpy())
    m = m[m["grp"].notna()].copy()
    m["occ11"] = D27.group_of(m["occ"].to_numpy(float))
    m["b5"] = band5(m["age"])
    m["s1"] = np.minimum(m["age"] - 35, 0) / 10
    m["s2"] = np.maximum(m["age"] - 35, 0) / 10
    agem = wmean_by(m, "age", "rel")[0]
    m["rel_a"] = m["rel"] - m["age"].map(agem)
    pi5 = (m.groupby("b5")["wt"].sum() / m["wt"].sum()).reindex(range(8)).to_numpy()
    pia = m.groupby("age")["wt"].sum() / m["wt"].sum()
    Bage = spl_basis(pia.index.to_numpy())
    out = {}
    m55 = m[m["age"] <= 55]
    for lev in ("grp", "ddx"):
        sp = spline_fit(m, lev)
        sy = synthetic(m55, lev)
        q, nq = wmean_by(m, [lev, "b5"])
        Q = q.unstack().reindex(columns=range(8))
        Q.columns = QC
        NQ = nq.unstack().reindex(columns=range(8)).fillna(0)
        F = sp.join(sy).join(Q)
        F["n"] = m.groupby(lev).size()
        F["share"] = m.groupby(lev)["wt"].sum() / m["wt"].sum()
        F.attrs["NQ"] = NQ
        out[lev] = F
    G, F = out["grp"], out["ddx"]
    for c in SPC + ["B1c", "B2c"]:                                # relative to the employment-weighted industry
        G[c] = G[c] - np.average(G[c], weights=G["share"])
    F["grp"] = group_of(F.index.to_numpy())
    small = (F["n"] < MIN_FINE) | F["B1c"].isna()
    for c in SPC + ["B1c", "B2c"]:
        F[c] = F[c] - np.average(F.loc[~small, c], weights=F.loc[~small, "share"])
        F.loc[small, c] = F.loc[small, "grp"].map(G[c])
    NQ = F.attrs["NQ"]
    for k, c in enumerate(QC):
        bad = small | (NQ[k].reindex(F.index).fillna(0) < MIN_BAND) | F[c].isna()
        F.loc[bad, c] = F.loc[bad, "grp"].map(G[c])
    F["small"] = small
    for D_, M_ in ((G, M["grp"]), (F, M["ddx"])):
        D_["B32"] = M_["B"].reindex(D_.index)
        D_["P32"] = M_["P"].reindex(D_.index)
        if D_ is F:
            for c in ("B32", "P32"):
                miss = F[c].isna()
                F.loc[miss, c] = F.loc[miss, "grp"].map(G[c])
        D_["qlvl"] = D_[QC].to_numpy() @ pi5
        D_["slvl"] = (D_[SPC].to_numpy() @ Bage.T) @ pia.to_numpy()
        D_["G35"] = D_["Q5"] - D_["Q2"]                         # band growth 35-39 -> 50-54
        D_["G25"] = D_["Q2"] - D_["Q0"]                         # band growth 25-29 -> 35-39
        D_["lin35"] = 1.5 * D_["B32"]                           # linear-B growth from 37 to 52
        sp52 = (D_[SPC].to_numpy() @ spl_basis([52]).T)[:, 0]
        sp37 = (D_[SPC].to_numpy() @ spl_basis([37]).T)[:, 0]
        D_["S35"] = sp52 - sp37
        D_["syn35"] = 1.5 * D_["B2c"]
    # ---- occupation group x industry group cells
    mc = m[m["occ11"].notna()].copy()
    mc["o"] = mc["occ11"].astype(int)
    mc["j"] = mc["grp"].astype(int)
    A = np.zeros((11, 8))
    C = np.zeros((33, 8))
    for b in range(8):
        z = mc[mc["b5"] == b]
        y, w, oi, ji = z["rel_a"].to_numpy(), z["wt"].to_numpy(), z["o"].to_numpy(), z["j"].to_numpy()
        a, c = np.zeros(11), np.zeros(33)
        so, sj = np.bincount(oi, w, 11), np.bincount(ji, w, 33)
        for _ in range(50):
            a = np.bincount(oi, w * (y - c[ji]), 11) / np.where(so > 0, so, 1)
            c = np.bincount(ji, w * (y - a[oi]), 33) / np.where(sj > 0, sj, 1)
        A[:, b], C[:, b] = a, c
    qc, nqc = wmean_by(mc, ["o", "j", "b5"])
    QCm = qc.unstack().reindex(columns=range(8))
    NQC = nqc.unstack().reindex(columns=range(8)).fillna(0)
    ncell = mc.groupby(["o", "j"]).size()
    own = {}
    for (o, j), row in QCm.iterrows():
        if ncell.get((o, j), 0) >= MIN_FINE:
            v = row.to_numpy(float).copy()
            bad = (NQC.loc[(o, j)].to_numpy() < MIN_BAND) | ~np.isfinite(v)
            v[bad] = (A[o] + C[j])[bad]
            own[(o, j)] = v
    qo, _ = wmean_by(mc, ["o", "b5"])
    QO = qo.unstack().reindex(index=range(11), columns=range(8)).to_numpy(float)
    cellinfo = dict(A=A, C=C, QO=QO, w=mc.groupby(["o", "j"])["wt"].sum() / mc["wt"].sum(), own=own, ncell=ncell, share_own=float(mc[[(o, j) in own for o, j in
                                                                         zip(mc["o"], mc["j"])]]["wt"].sum()
                                                                     / mc["wt"].sum()), n=len(mc), ncells=len(own))
    # per-man measures (dispersion across CPS men)
    mm = m[["ddx", "grp", "wt", "occ11"]].copy()
    for c in ("G35", "G25", "lin35", "S35", "syn35"):
        mm[c] = mm["ddx"].map(F[c])
        mm[c + "_g"] = mm["grp"].map(G[c])
    QCc = cell_q(mm["occ11"].to_numpy(float), mm["grp"].to_numpy(float), cellinfo)
    mm["cG35"] = QCc[:, 5] - QCc[:, 2]
    mm["cG25"] = QCc[:, 2] - QCc[:, 0]
    # special cells (Section D)
    m["cell5"] = cell_codes(m["occ"], m["grp"])
    q5, n5 = wmean_by(m.dropna(subset=["cell5"]), ["cell5", "b5"])
    cq = q5.unstack().reindex(columns=range(8))
    cq.columns = QC
    cq["n"] = m.dropna(subset=["cell5"]).groupby("cell5").size()
    s = G.sort_values("G35", ascending=False)
    cum = s["share"].cumsum()
    post_steep = set(s.index[(cum - s["share"]) < 0.25].astype(int))
    return dict(grp=G, ddx=F, cells5=cq, cellinfo=cellinfo, post_steep=post_steep, N=len(m), pi5=pi5, pia=pia,
                men=mm)


def cell_q(o, j, ci):
    """(n, 8) band values for occupation group o x industry group j (own cell or additive fallback); flag own."""
    o, j = np.asarray(o, float), np.asarray(j, float)
    out = np.full((len(o), 8), np.nan)
    ok = np.isfinite(o) & np.isfinite(j)
    oi, ji = o[ok].astype(int), j[ok].astype(int)
    vals = ci["A"][oi] + ci["C"][ji]
    for k, (a, b) in enumerate(zip(oi, ji)):
        v = ci["own"].get((a, b))
        if v is not None:
            vals[k] = v
    out[ok] = vals
    return out


def cell_own(o, j, ci):
    return np.array([((int(a), int(b)) in ci["own"]) if np.isfinite(a) and np.isfinite(b) else False
                     for a, b in zip(np.asarray(o, float), np.asarray(j, float))])


def cell_codes(occ, grp):
    dd = pd.Series(np.asarray(occ, float))
    g = pd.Series(np.asarray(grp, float))
    o11 = pd.Series(D27.group_of(dd.to_numpy()))
    mp = o11.isin([0, 1])
    law = (dd == 178) & (g == LEGAL)
    fin = g.isin(FININS) & dd.isin(FIN_OCC)
    pro = (g == PROF) & mp & ~law
    mpo = mp & ~law & ~fin & ~pro
    c = np.select([law, fin, pro, mpo], [1, 2, 3, 4], 5).astype(float)
    c[(dd.isna() | g.isna()).to_numpy()] = np.nan
    return c


# ================================================================ data-defined sets (ranked on the MORG nonlinear profiles)
SETN = {1: "high-paid AND high later growth", 2: "high-paid only", 3: "high later growth only", 0: "neither"}


def topset(vals, w, q=0.25):
    """threshold of the top quartile of men's employment ranked by vals."""
    vals, w = np.asarray(vals, float), np.asarray(w, float)
    o = np.argsort(-vals)
    cum = np.cumsum(w[o])
    inset = (cum - w[o]) < q * w.sum()
    return float(vals[o][inset].min())


def data_sets(MF):
    ci = MF["cellinfo"]
    cw = ci["w"]
    o = np.array([a for a, _ in cw.index], float)
    j = np.array([b for _, b in cw.index], float)
    Q = cell_q(o, j, ci)
    T = pd.DataFrame(Q, columns=QC, index=cw.index)
    T["o"], T["j"] = o, j
    T["lvl"] = Q @ MF["pi5"]
    T["G35"], T["G25"] = Q[:, 5] - Q[:, 2], Q[:, 2] - Q[:, 0]
    T["w"] = cw.to_numpy()
    T["n"] = ci["ncell"].reindex(cw.index).fillna(0).to_numpy()
    T["own"] = [k in ci["own"] for k in cw.index]
    thrG, thrL = topset(T["G35"], T["w"]), topset(T["lvl"], T["w"])
    T["set"] = np.select([(T["lvl"] >= thrL) & (T["G35"] >= thrG), T["lvl"] >= thrL, T["G35"] >= thrG], [1, 2, 3], 0)
    G = MF["grp"]
    ithrG, ithrL = topset(G["G35"], G["share"]), topset(G["qlvl"], G["share"])
    G["set"] = np.select([(G["qlvl"] >= ithrL) & (G["G35"] >= ithrG), G["qlvl"] >= ithrL, G["G35"] >= ithrG],
                         [1, 2, 3], 0)
    MF["sets"] = dict(T=T, thrG=thrG, thrL=thrL, ithrG=ithrG, ithrL=ithrL)


def cell_set(o, j, MF):
    Q = cell_q(o, j, MF["cellinfo"])
    lv, g = Q @ MF["pi5"], Q[:, 5] - Q[:, 2]
    st = MF["sets"]
    hl, hg = lv >= st["thrL"], g >= st["thrG"]
    c = np.select([hl & hg, hl, hg], [1, 2, 3], 0).astype(float)
    c[~np.isfinite(lv)] = np.nan
    return c


def ind_set(j, MF):
    return pd.Series(np.asarray(j, float)).map(MF["grp"]["set"]).to_numpy(float)


# ================================================================ panels: early industry, sets, cells, profile pieces
def lookup(fine, grp, F, G, cols):
    v = F.reindex(np.asarray(fine, float))[cols].to_numpy(float)
    gv = G.reindex(np.asarray(grp, float))[cols].to_numpy(float)
    return np.where(np.isfinite(v), v, gv)


def prep(d, MF, W, rc):
    F, G, ci = MF["ddx"], MF["grp"], MF["cellinfo"]
    d = d.copy()
    if "valid" not in d:
        d["valid"] = True
    d["occ11"] = D27.group_of(d["dd"].to_numpy(float))
    d["cell"] = cell_codes(d["dd"], d["igrp"])
    d["og"] = d["occ11"] * 100 + d["igrp"]
    ok = d["valid"] & d["lw"].notna() & d["age"].between(25, 34)
    e = d[ok & d["igrp"].notna()]
    g = e.groupby("pid")
    E = pd.DataFrame({"egrp": g["igrp"].agg(mode), "en": g.size()})
    e2 = e[e["igrp"] == e["pid"].map(E["egrp"])]
    E["eddx"] = e2.groupby("pid")["ddx"].agg(mode)
    o = e[e["dd"].notna()]
    go = o.groupby("pid")
    E["edd"] = go["dd"].agg(mode)
    E["eog"] = go["og"].agg(mode)
    E["ecell"] = go["cell"].agg(mode)
    d = d.join(E, on="pid")
    d["e_fi"] = d["egrp"].isin(FININS).astype(float).where(d["egrp"].notna())
    d["e_lp"] = d["egrp"].isin(LEGPRO).astype(float).where(d["egrp"].notna())
    d["e_flp"] = d["e_fi"] + d["e_lp"]
    d["e_elite"] = d["ecell"].isin([1, 2, 3]).astype(float).where(d["ecell"].notna())
    for k in range(1, 5):
        d[f"c{k}"] = (d["ecell"] == k).astype(float).where(d["ecell"].notna())
    d["s1"] = np.minimum(d["age"] - 35, 0) / 10
    d["s2"] = np.maximum(d["age"] - 35, 0) / 10
    d["t"] = (d["age"] - 40) / 10
    b5 = band5(d["age"])
    Bs = spl_basis(d["age"].to_numpy())
    lw = d["lw"].where(d["valid"])
    d["lwv"] = lw
    pi5 = MF["pi5"]
    # ---- EARLY industry (modal fine code, group fallback)
    cols = QC + SPC + ["slvl", "B32", "P32", "B2c", "G35", "lin35"]
    V = lookup(d["eddx"], d["egrp"], F, G, cols)
    Q, S_ = V[:, :8], V[:, 8:13]
    d["e_q_t"] = Q[np.arange(len(d)), b5]
    d["e_q_l"] = Q @ pi5
    d["e_q_p"] = d["e_q_t"] - d["e_q_l"]
    d["e_s_p"] = (S_ * Bs).sum(1) - V[:, 13]
    d["e_lin_l"], d["e_lin_p"] = V[:, 15], V[:, 14] * d["t"]
    d["e_c2"] = V[:, 16] * d["s2"]
    d["eG35"], d["elin35"], d["eB32"] = V[:, 17], V[:, 18], V[:, 14]
    # ---- CURRENT industry (32's weighted crosswalk of the raw code)
    meas = {int(k): tuple(v) for k, v in zip(F.index, F[QC + SPC + ["slvl"]].to_numpy(float))}
    dd_, _, mmv = D32.map_codes(d["icode"].to_numpy(), d["isch"].to_numpy(), W, meas, rc)
    mmv[~np.isfinite(d["ddx"].to_numpy(float))] = np.nan
    Qk = mmv[:, :8]
    d["k_q_t"] = Qk[np.arange(len(d)), b5]
    d["k_q_l"] = Qk @ pi5
    d["k_q_p"] = d["k_q_t"] - d["k_q_l"]
    d["k_s_p"] = (mmv[:, 8:13] * Bs).sum(1) - mmv[:, 13]
    d["k_lin_l"], d["k_lin_p"] = d["P"], d["B"] * d["t"]
    # ---- cells: current and early (occupation group x industry group)
    Qc = cell_q(d["occ11"], d["igrp"], ci)
    d["ck_t"] = Qc[np.arange(len(d)), b5]
    d["ck_l"] = Qc @ pi5
    d["ck_p"] = d["ck_t"] - d["ck_l"]
    d["ck_res"] = lw - d["ck_t"]
    up, dn = np.minimum(b5 + 1, 7), np.maximum(b5 - 1, 0)
    d["ck_slope"] = (Qc[np.arange(len(d)), up] - Qc[np.arange(len(d)), dn]) / (5 * (up - dn))
    d["ck_own"] = cell_own(d["occ11"], d["igrp"], ci)
    eo, ej = np.floor(d["eog"] / 100), d["eog"] % 100
    Qe = cell_q(eo, ej, ci)
    d["ce_t"] = Qe[np.arange(len(d)), b5]
    d["ce_l"] = Qe @ pi5
    d["ce_p"] = d["ce_t"] - d["ce_l"]
    d["ce_res"] = lw - d["ce_t"]
    d["ce_own"] = cell_own(eo, ej, ci)
    d["eG35c"] = Qe[:, 5] - Qe[:, 2]
    QO = ci["QO"]
    for pre, oo in (("ko", d["occ11"].to_numpy(float)), ("eo", eo.to_numpy(float))):
        okk = np.isfinite(oo)
        Qo = np.full((len(d), 8), np.nan)
        Qo[okk] = QO[oo[okk].astype(int)]
        d[f"{pre}_p"] = Qo[np.arange(len(d)), b5] - Qo @ pi5
    d["ck_ind"] = d["ck_p"] - d["ko_p"]
    d["ce_ind"] = d["ce_p"] - d["eo_p"]
    d["eo11"] = eo
    d["emp"] = d["ecell"].isin([1, 2, 3, 4]).astype(float).where(d["ecell"].notna())
    d["eset"] = cell_set(eo, ej, MF)
    d["kset"] = cell_set(d["occ11"], d["igrp"], MF)
    d["eiset"] = ind_set(d["egrp"], MF)
    for nm, col_ in (("", "eset"), ("I", "eiset")):
        for k, key in ((1, "hh"), (2, "hlo"), (3, "hgo")):
            d[f"e_{key}{nm}"] = (d[col_] == k).astype(float).where(d[col_].notna())
    return d


def son_frame(d, wt="wpool"):
    v = d[d["valid"] & d["lw"].notna()]
    g = v.groupby("pid")
    S = pd.DataFrame({"fam68": g["fam68"].first(), "race": g["race"].first(), "lyp": g["lyp"].first(),
                      "birth_year": g["birth_year"].first(), "wpool": g[wt].mean()})
    if "educ" in v:
        S["educ"] = g["educ"].max()
    for nm, (lo, hi) in (("0", (25, 34)), ("35", (35, 55)), ("40", (40, 55)), ("45", (45, 55))):
        z = v[v["age"].between(lo, hi)].groupby("pid")
        S[f"lw{nm}"], S[f"a{nm}"], S[f"n{nm}"] = z["lw"].mean(), z["age"].mean(), z.size()
    for nm in ("35", "40", "45"):
        S[f"d{nm}"] = S[f"lw{nm}"] - S["lw0"]
    keep = ["egrp", "eddx", "en", "edd", "eog", "ecell", "eset", "eiset", "e_hh", "e_hlo", "e_hgo", "e_hhI", "e_hloI",
            "e_hgoI", "e_fi", "e_lp", "e_flp", "e_elite", "c1", "c2",
            "c3", "c4", "eG35", "elin35", "eG35c", "eB32"]
    S = S.join(d.drop_duplicates("pid").set_index("pid")[[k for k in keep if k in d]])
    S["pid"] = S.index
    S["black"] = (S["race"] == "Black").astype(float)
    S["lyp_c"] = S["lyp"] - S["lyp"].mean()
    for k in ("flp", "fi", "lp", "elite", "hh", "hlo", "hgo"):
        S[f"e_{k}_lyp"] = S[f"e_{k}"] * S["lyp_c"]
    S["coh"] = (S["birth_year"] - 1960) / 10
    S["educ_c"] = S["educ"] - 12 if "educ" in S else np.nan
    return S.reset_index(drop=True)


# ================================================================ estimation helpers
def fitc(tag, d, y, xcols, ctrl, groups=("P", "B", "W"), minn=100):
    """row-level OLS / WLS; 'black' is dropped in the race samples."""
    info = {}
    for g in groups:
        xs = [x for x in xcols if not (g in ("B", "W") and x == "black")]
        sub, wc = D27.subset(d, g)
        sub = sub.dropna(subset=[y, *xs] + ([wc] if wc else []))
        xs = [x for x in xs if sub[x].nunique() > 1]
        if not xs:
            continue
        Cm = ctrl(sub)
        ok = np.isfinite(Cm).all(1)
        sub, Cm = sub[ok], Cm[ok]
        if len(sub) < minn:
            continue
        X = np.column_stack([sub[x].to_numpy(float) for x in xs] + [Cm])
        clv = D27.CLIDX.get_indexer(sub["fam68"].to_numpy())
        w = sub[wc].to_numpy(float) if wc else None
        D27.est((tag, y, g), sub, y, X, clv, w, names=tuple(xs))
        info[g] = (len(sub), sub["pid"].nunique(), len(np.unique(clv)), float(np.average(sub[y], weights=w)))
    return info


def fit_fe(tag, d, y, xcols, yearcol="year", common=("s2",), groups=("P", "B", "W"), minn=500):
    """person FE (within transformation; son-mean weights for the pooled sample) + year FE + common terms."""
    info = {}
    for g in groups:
        sub, wc = D27.subset(d, g)
        sub = sub.dropna(subset=[y, *xcols, *common, yearcol] + ([wc] if wc else []))
        if len(sub) < minn:
            continue
        wv = sub.groupby("pid")[wc].transform("mean").to_numpy(float) if wc else np.ones(len(sub))
        Mx = np.column_stack([sub[c].to_numpy(float) for c in (*xcols, *common)] + [dummies(sub[yearcol])])
        gi = pd.factorize(sub["pid"])[0]
        cnt = np.bincount(gi, weights=wv)

        def dm(v):
            return v - (np.bincount(gi, weights=v * wv) / cnt)[gi]
        Md = np.column_stack([dm(Mx[:, j]) for j in range(Mx.shape[1])])
        yy = sub.assign(_y=dm(sub[y].to_numpy(float)))
        clv = D27.CLIDX.get_indexer(sub["fam68"].to_numpy())
        D27.est((tag, y, g), yy, "_y", Md, clv, wv, names=tuple(xcols))
        info[g] = (len(sub), sub["pid"].nunique(), len(np.unique(clv)))
    return info


def co(tag, y, g, x):
    if g == "BW":
        ks = [(((tag, y, "B"), x), 1.0), (((tag, y, "W"), x), -1.0)]
    else:
        ks = [(((tag, y, g), x), 1.0)]
    return safe(ks)


def coL(tag, y, g, terms):
    if g == "BW":
        ks = [(((tag, y, "B"), x), c) for x, c in terms] + [(((tag, y, "W"), x), -c) for x, c in terms]
    else:
        ks = [(((tag, y, g), x), c) for x, c in terms]
    return safe(ks)


def nfo(info, g):
    return f"{info[g][0]:,} / {info[g][2]:,}" if g in info else ""


# ================================================================ 0. sample kept
def sec_sample(d, S, md, label):
    v = d[d["valid"] & d["lw"].notna()]
    rows = ["| Race | sons with a valid wage 25-55 | ... with valid 25-34 son-years | ... with an early industry | "
            "... and observed at 35-55 | ... and observed at 40-55 | share of sons observed at 35-55 who have an "
            "early industry | share of son-years 35-55 kept | sons with >= 2 early industry years |",
            "|---|---|---|---|---|---|---|---|---|"]
    for race in ("Black + White", "Black", "White"):
        z = v if race == "Black + White" else v[v["race"] == race]
        s = S if race == "Black + White" else S[S["race"] == race]
        late = z[z["age"].between(35, 55)]
        n_late = late["pid"].nunique()
        kept = late[late["egrp"].notna()]
        rows.append(f"| {race} | {z['pid'].nunique():,} | {s['n0'].notna().sum():,} | {s['egrp'].notna().sum():,} | "
                    f"{(s['egrp'].notna() & s['n35'].notna()).sum():,} | {(s['egrp'].notna() & s['n40'].notna()).sum():,}"
                    f" | {kept['pid'].nunique() / max(n_late, 1):.3f} | {len(kept) / max(len(late), 1):.3f} | "
                    f"{(s['en'] >= 2).sum():,} |")
        CSV.append(dict(table="0 sample", sample=f"{label} {race}", outcome="share of 35-55 sons kept",
                        coef=kept["pid"].nunique() / max(n_late, 1), n=n_late))
    ch = ["| Race | sample (sons) | N sons | mean ln wage at 25-34 | ln parental income | years of education | birth "
          "year | share early FLP industry (illustrative) | share early high-paid high-growth cell |",
          "|---|---|---|---|---|---|---|---|---|"]
    for race in ("Black + White", "Black", "White"):
        s = S if race == "Black + White" else S[S["race"] == race]
        for nm, mk in (("all sons with valid 25-34 son-years", s["n0"].notna()),
                       ("with an early industry", s["egrp"].notna()),
                       ("with an early industry, observed at 35-55", s["egrp"].notna() & s["n35"].notna()),
                       ("with an early industry, observed at 40-55", s["egrp"].notna() & s["n40"].notna()),
                       ("with an early industry, NOT observed after 34", s["egrp"].notna() & s["n35"].isna())):
            z = s[mk]
            ed = f"{z['educ'].mean():.2f}" if "educ" in z else ""
            ch.append(f"| {race} | {nm} | {len(z):,} | {z['lw0'].mean():.3f} | {z['lyp'].mean():.3f} | {ed} | "
                      f"{z['birth_year'].mean():.1f} | {z['e_flp'].mean():.3f} | {z['e_hh'].mean():.3f} |")
    md += [f"### 0{label[0]}. Who is kept ({label})", "",
           "Fixing the industry at 25-34 requires a son to be observed at 25-34; growth after 35 requires him to be "
           "observed again later. This conditioning is necessary for the question, but it is not a balanced panel: "
           "every son-year of every son with an early industry is used in the band regressions. Shares and 25-34 "
           "characteristics (unweighted means; descriptive):", ""] + rows + [""] + ch + [""]


# ================================================================ H. headline: nonlinear industry / cell profiles
H_ROWS32 = [("lwv", "ln wage (total)"),
            ("k_lin_l", "current industry, LINEAR (32): level P"),
            ("k_lin_p", "current industry, LINEAR (32): slope B x t"),
            ("k_q_l", "current industry, NONLINEAR band profile: level"),
            ("k_q_p", "current industry, NONLINEAR band profile: age profile Q(band) - level"),
            ("k_q_t", "current industry, NONLINEAR band profile: total"),
            ("k_s_p", "current industry, piecewise (knots 30/35/45): age profile")]
H_ROWSC = [("lwv", "ln wage (total)"),
           ("k_lin_p", "current industry, LINEAR slope B x t (32)"),
           ("k_q_p", "current industry, NONLINEAR band profile"),
           ("k_s_p", "current industry, piecewise (30/35/45) profile"),
           ("k_q_t", "current industry, band level + profile"),
           ("e_lin_p", "industry at 25-34, LINEAR slope B x t"),
           ("e_q_l", "industry at 25-34, band level"),
           ("e_q_p", "industry at 25-34, NONLINEAR band profile"),
           ("e_s_p", "industry at 25-34, piecewise (30/35/45) profile"),
           ("e_c2", "industry at 25-34, synthetic-cohort slope after 35 x s2"),
           ("e_q_t", "industry at 25-34, band level + profile"),
           ("ck_l", "current CELL (occupation group x industry group), band level"),
           ("ck_p", "current CELL, NONLINEAR band profile"),
           ("ko_p", "current occupation group (11), NONLINEAR band profile (occupation only)"),
           ("ck_ind", "current cell profile minus occupation-group profile (what industry adds within the cell)"),
           ("ck_t", "current CELL, level + profile"),
           ("ck_res", "within current cell (ln wage - cell level - cell profile)"),
           ("ce_l", "cell at 25-34, band level"),
           ("ce_p", "cell at 25-34, NONLINEAR band profile"),
           ("eo_p", "occupation group at 25-34, NONLINEAR band profile (occupation only)"),
           ("ce_ind", "cell at 25-34 profile minus occupation-group profile (what industry adds)"),
           ("ce_t", "cell at 25-34, level + profile")]


def sec_headline(d, md, label, base_mask, ctrl=ctrl_lsn, need=("A", "C"), tag="h"):
    z32 = d[base_mask].copy()
    ys32 = tuple(y for y, _ in H_ROWS32)
    run_cells(f"{tag}32", z32, ys32, ("lyp",), ctrl, need, bands=BANDS)
    zc = d[base_mask & d["egrp"].notna() & d["eog"].notna()].copy()
    ysC = tuple(y for y, _ in H_ROWSC)
    run_cells(f"{tag}C", zc, ysC, ("lyp",), ctrl, need, bands=BANDS)
    hdr = ["(1) pooled change (35-55)-(25-34)", "(2) share of the ln wage change", "(3) change of the B-W gap "
           "(35-55)-(25-34)", "(4) share", "(5) pooled change (45-55)-(25-34)", "(6) share", "(7) B-W change "
           "(45-55)-(25-34)", "(8) share"]
    panels = []
    for smp, rows_def, title in (("32", H_ROWS32, "A. 32's decomposition sample (current industry and occupation "
                                                  "mapped): replication of the linear B and the nonlinear profile"),
                                 ("C", H_ROWSC, "B. Common sample (also early industry and early cell): current vs "
                                                "early, industry vs cell, linear vs nonlinear")):
        tg = f"{tag}{smp}"
        rows = []
        for y, lab in rows_def:
            t = []
            for g, b in (("P", (35, 55)), ("BW", (35, 55)), ("P", (45, 55)), ("BW", (45, 55))):
                num = Dch(tg, y, g, b=b)
                t += [safe(num), sratio(num, Dch(tg, "lwv", g, b=b)) if y != "lwv" else NAN3]
            rows.append((lab, [cell(x) for x in t]))
            for h, x in zip(hdr, t):
                rec(f"H headline {label}", smp, h, y, x)
        ns = []
        for lo, hi in BANDS[:3]:
            k = K(tg, "lwv", lo, hi, "P")
            if k in RES:
                ns.append(f"{lo}-{hi}: {RES[k]['n']:,} / {RES[k]['children']:,}")
        rows.append(("N son-years / sons (pooled)", [" ; ".join(ns)] + [""] * 7))
        panels.append((title, rows))
    md += [f"## H{label[0]}. Headline: nonlinear industry and occupation x industry cell profiles ({label})", "",
           "Each row is a piece of the son's ln wage regressed on ln parental income by age band (stacked; controls as "
           "in the band regressions); the columns are the change of that coefficient across age bands and its share of "
           "the change for ln wage, pooled and for the Black-White gap. 'Linear' = 32's P_j + B_j t; 'nonlinear band "
           "profile' = the son's industry's (cell's) relative wage in his five-year age band (CPS MORG), split into "
           "its age-weighted level and the age profile around it; 'piecewise' = the knots-30/35/45 profile. The "
           "profile rows are the like-for-like comparison with the linear slope (all are the career-growth component "
           "of the industry / cell). 'At 25-34' = the industry or cell fixed at the son's modal code at 25-34, evaluated "
           "at his current age (payoff of where he started, wherever he works later). Shares blank when the "
           "denominator is not different from zero.", ""]
    md += table(hdr, panels)


# ================================================================ B. profiles and dispersion
def sec_morg(MF, md, S):
    G, F, ci, mm = MF["grp"], MF["ddx"], MF["cellinfo"], MF["men"]
    rows = ["| Industry group | linear B (32) | linear growth 37->52 (1.5 B) | piecewise slope 25-30 | 30-35 | 35-45 | "
            "45-64 | " + " | ".join(f"Q {b}" for b in B5) + " | band growth (35-39)->(50-54) | band growth "
            "(25-29)->(35-39) | piecewise growth 37->52 | synthetic-cohort growth 37->52 | PSID sons (early) | "
            "employment share | N men |", "|---" * 23 + "|---|"]
    ns = S.groupby("egrp").size()
    for g, z in G.sort_values("G35", ascending=False).iterrows():
        tag = (" (FLP)" if int(g) in FLP else "") + {1: " (high-paid, high later growth)", 2: " (high-paid)",
                                                      3: " (high later growth)", 0: ""}[int(z["set"])]
        rows.append(f"| {GNAMES[int(g)]}{tag} | {z['B32']:.3f} | {z['lin35']:.3f} | " +
                    " | ".join(f"{z[c]:.3f}" for c in SPC[1:]) + " | " + " | ".join(f"{z[c]:.3f}" for c in QC) +
                    f" | {z['G35']:.3f} | {z['G25']:.3f} | {z['S35']:.3f} | {z['syn35']:.3f} | {int(ns.get(g, 0)):,} | "
                    f"{z['share']:.3f} | {int(z['n']):,} |")
        for c in ["B32", "lin35"] + SPC + QC + ["G35", "G25", "S35", "syn35", "share"]:
            CSV.append(dict(table="B0 MORG nonlinear profiles", sample="men 25-64, 1992-2002", outcome=c,
                            term=GNAMES[int(g)], coef=z[c], n=z["n"]))
    m_rows = ["| Data-defined industry set | linear growth 37->52 (1.5 B) | band growth (25-29)->(35-39) | band growth "
              "(35-39)->(50-54) | piecewise growth 37->52 | employment share |", "|---|---|---|---|---|---|"]
    Gs = G.copy()
    for k in (1, 2, 3, 0):
        z = Gs[Gs["set"] == k]
        f = lambda c: np.average(z[c], weights=z["share"])
        m_rows.append(f"| {SETN[k]} | {f('lin35'):.3f} | {f('G25'):.3f} | {f('G35'):.3f} | {f('S35'):.3f} | "
                      f"{z['share'].sum():.3f} |")
    # dispersion across men
    w = mm["wt"]
    dis = ["| Growth measure (log points) | s.d. across CPS men: fine industries | 33 industry groups | 11 x 33 cells | "
           "s.d. across PSID sons (industry at 25-34) | corr. with linear growth 1.5 B (men, fine) | R2 on linear "
           "growth | share of variance NOT captured by linear B |", "|---|---|---|---|---|---|---|---|"]
    Sv = S[S["egrp"].notna()]
    SD = {}
    for c, lab, cc, ps in (("lin35", "linear B-implied growth 37->52 (1.5 B, 32)", None, "elin35"),
                           ("G35", "band growth (35-39)->(50-54)", "cG35", "eG35"),
                           ("S35", "piecewise (30/35/45) growth 37->52", None, None),
                           ("syn35", "synthetic-cohort growth 37->52", None, None),
                           ("G25", "band growth (25-29)->(35-39) (before 35)", "cG25", None)):
        sf, sg = wsd(mm[c], w), wsd(mm[c + "_g"], w)
        scl = wsd(mm[cc], w) if cc else np.nan
        sp = np.nanstd(Sv[ps]) if ps else np.nan
        r_ = wcorr(mm[c], mm["lin35"], w)
        SD[c] = dict(fine=sf, grp=sg, cell=scl, psid=sp, corr=r_)
        dis.append(f"| {lab} | {sf:.3f} | {sg:.3f} | {'' if not np.isfinite(scl) else f'{scl:.3f}'} | "
                   f"{'' if not np.isfinite(sp) else f'{sp:.3f}'} | {r_:.3f} | {r_ ** 2:.3f} | {1 - r_ ** 2:.3f} |")
        CSV.append(dict(table="B1 dispersion", sample="CPS men", outcome=lab, coef=sf, se=sg, p=scl, mean=r_))
    rcell = wcorr(mm["cG35"], mm["lin35"], w)
    SD["cell_corr"] = rcell
    SD["psid_cell"] = np.nanstd(Sv["eG35c"])
    MF["sd"] = SD
    md += ["## B. Nonlinear industry profiles and what the linear slope misses", "",
           f"CPS MORG men 25-64, 1992-2002 ({MF['N']:,}). Q = industry x five-year age-band effect (wage relative to men "
           "of the same single year of age); piecewise slopes per 10 years with knots at 30, 35, 45 relative to the "
           "average industry; synthetic cohort = slopes within industry net of 5-year birth-cohort FE (identified from "
           "the aging of cohorts across 1992-2002; industry-specific period trends not separated). 'Post-35 steep' = "
           "top quartile of men's employment by band growth (35-39)->(50-54): "
           + ", ".join(GNAMES[i] for i in sorted(MF["post_steep"])) + f". Cells: {ci['ncells']} of the 11 x 33 "
           f"occupation x industry cells have >= {MIN_FINE} men (own profile), covering {ci['share_own']:.1%} of "
           "men's employment; the rest use the additive occupation(band) + industry(band) fallback.", "",
           "### B0. Industry groups sorted by band growth after 35 (descriptive industry averages; worker composition "
           "not held fixed)", ""] + rows + ["", "Employment-weighted means by early-industry set:", ""] + m_rows + \
        ["", "### B1. How much of the cross-industry variance in growth after 35 does the linear B miss?", "",
         "Each man in CPS MORG is assigned his industry's (group's, cell's) growth measure; s.d. across men "
         "(earnings weights). R2 = squared correlation with the linear-B-implied growth across men (fine industries); "
         "1 - R2 = share of the cross-industry variance of that growth measure that the linear B does not capture "
         "(includes sampling noise of the fine band cells). PSID column: s.d. across sons of the measure of their "
         f"industry at 25-34. For cells, the band growth after 35 correlates {rcell:.3f} with the industry's linear "
         f"growth (R2 {rcell ** 2:.3f}); s.d. across PSID sons of their early cell's band growth after 35 "
         f"{SD['psid_cell']:.3f}.", ""] + dis + [""]


def sec_psid_groups(d, S, MF, md):
    z = d[d["valid"] & d["lw"].notna() & d["egrp"].notna()].copy()
    cnt = S.groupby("egrp").size()
    ref = int(cnt.idxmax())
    gs = [int(g) for g in cnt.index if int(g) != ref]
    xs = []
    for g in gs:
        for k in (1, 2):
            z[f"s{k}g{g}"] = z[f"s{k}"] * (z["egrp"] == g)
            xs.append(f"s{k}g{g}")
    fit_fe("pgrp", z, "lw", tuple(xs), groups=("P",))
    sh = cnt / cnt.sum()
    G = MF["grp"]
    rows = ["| Early industry group | PSID sons | PSID slope 25-35 | PSID slope 35-55 | PSID acceleration | MORG band "
            "growth (25-29)->(35-39) | MORG band growth (35-39)->(50-54) | MORG linear growth 1.5 B |",
            "|---|---|---|---|---|---|---|---|"]
    b2s, m2s, ws = [], [], []
    for g in sorted([ref] + gs, key=lambda g: -G.loc[g, "G35"]):
        own = [] if g == ref else [1.0]
        t1 = coL("pgrp", "lw", "P", ([(f"s1g{g}", 1.0)] if g != ref else []) + [(f"s1g{h}", -sh[h]) for h in gs])
        t2 = coL("pgrp", "lw", "P", ([(f"s2g{g}", 1.0)] if g != ref else []) + [(f"s2g{h}", -sh[h]) for h in gs])
        ta = coL("pgrp", "lw", "P", ([(f"s2g{g}", 1.0), (f"s1g{g}", -1.0)] if g != ref else []) +
                 [(f"s2g{h}", -sh[h]) for h in gs] + [(f"s1g{h}", sh[h]) for h in gs])
        del own
        b2s.append(t2[0])
        m2s.append(G.loc[g, "G35"])
        ws.append(cnt[g])
        if cnt[g] < 30:
            continue
        rows.append(f"| {GNAMES[g]}{' (reference in estimation)' if g == ref else ''} | {int(cnt[g]):,} | {cell(t1)} | "
                    f"{cell(t2)} | {cell(ta)} | {G.loc[g, 'G25']:.3f} | {G.loc[g, 'G35']:.3f} | "
                    f"{G.loc[g, 'lin35']:.3f} |")
        for nm, t in (("slope 25-35", t1), ("slope 35-55", t2), ("acceleration", ta)):
            rec("B2 PSID slopes by early group", GNAMES[g], nm, "PSID within-person", t, n=cnt[g])
    big = np.array(ws) >= 30
    MF["psid_sd_b2"] = wsd(np.array(b2s)[big], np.array(ws)[big])
    MF["psid_corr"] = wcorr(np.array(b2s)[big], np.array(m2s)[big], np.array(ws)[big])
    md += ["### B2. Within-person slopes by early industry group (PSID, pooled weighted)", "",
           "One son-year regression: ln wage on person FE, year FE, a common kink at 35 and early-group x s1 / s2 "
           "(slopes per 10 years); each group's slope relative to the son-weighted average group. Groups with >= 30 "
           "sons. Within-person growth of sons who STARTED in the group (wherever they work later), net of cohort "
           "differences.", ""] + rows + \
        ["", f"Across early groups with >= 30 sons (weighted by sons): s.d. of the PSID slope after 35 "
         f"{MF['psid_sd_b2']:.3f} per 10 years (includes sampling noise); correlation with the MORG band growth after "
         f"35 {MF['psid_corr']:.3f}.", ""]


# ================================================================ A(i): growth after 35 by early industry
def ctrl_for(nm):
    def f(z):
        return np.column_stack([np.ones(len(z)), (z["a0"].to_numpy(float) - 30) / 10,
                                (z[f"a{nm}"].to_numpy(float) - 45) / 10, z["coh"].to_numpy(float),
                                z["coh"].to_numpy(float) ** 2])
    return f


CSETL = [("e_hh", "early cell high-paid AND high later growth"), ("e_hlo", "early cell high-paid only"),
         ("e_hgo", "early cell high later growth only")]
ISETL = [("e_hhI", "early industry high-paid AND high later growth"), ("e_hloI", "early industry high-paid only"),
         ("e_hgoI", "early industry high later growth only")]


def sec_growth(S, md, label, tagp=""):
    cs, isx = tuple(x for x, _ in CSETL), tuple(x for x, _ in ISETL)
    specs = [("d40", "40", cs, "(1) Delta ln wage (40-55) - (25-34): early cell sets"),
             ("d40", "40", cs + ("lyp", "black", "educ_c"), "(2) ... + ln parental income, Black, education"),
             ("d35", "35", cs, "(3) Delta ln wage (35-55) - (25-34): early cell sets"),
             ("d45", "45", cs, "(4) Delta ln wage (45-55) - (25-34): early cell sets"),
             ("d40", "40", isx, "(5) Delta (40-55) - (25-34): early industry sets"),
             ("d40", "40", ("e_flp",), "(6) illustrative: early finance / insurance / legal / professional")]
    specs = [(y, nm, tuple(x for x in xs if x in S and S[x].notna().any()), h) for y, nm, xs, h in specs]
    infos = [fitc(f"{tagp}gr{k}", S, y, xs, ctrl_for(nm)) for k, (y, nm, xs, _) in enumerate(specs)]
    labs = CSETL + ISETL + [("e_flp", "illustrative: early finance / insurance / legal / professional"),
                            ("lyp", "ln parental income"), ("black", "Black"), ("educ_c", "years of education")]
    panels = []
    for g, gname in GROUPS4:
        rows = []
        for x, lab in labs:
            cells_, any_ = [], False
            for k, (y, nm, xs, h) in enumerate(specs):
                if x in xs and not (x == "black" and g != "P"):
                    t = co(f"{tagp}gr{k}", y, g, x)
                    cells_.append(cell(t))
                    any_ = any_ or bool(cell(t))
                    rec(f"A1 growth by early set {label}", g, h, x, t)
                else:
                    cells_.append("")
            if any_:
                rows.append((lab, cells_))
        if g != "BW":
            rows.append(("Mean of outcome (all sons)", [f"{infos[k][g][3]:.3f}" if g in infos[k] else ""
                                                        for k in range(len(specs))]))
            rows.append(("N sons / clusters", [nfo(infos[k], g) for k in range(len(specs))]))
            ss = D27.subset(S, g)[0]
            ss = ss[ss["d40"].notna()]
            rows.append(("Sons with Delta(40-55) by early cell set: HH ; high-paid only ; high growth only ; neither",
                         [" ; ".join(f"{int((ss['eset'] == k_).sum())}" for k_ in (1, 2, 3, 0))] + [""] * 3 +
                         [" ; ".join(f"{int((ss['eiset'] == k_).sum())}" for k_ in (1, 2, 3, 0)),
                          f"{int((ss['e_flp'] == 1).sum())}"]))
        panels.append((gname, rows))
    md += [f"### A1{label[0]}. Wage growth after 35 by where the son was at 25-34 ({label})", "",
           "Son-level regressions (outcome in the column header; one row per son observed at 25-34 and in the later "
           "window). Regressors: the son's EARLY occupation x industry cell (modal at 25-34) classified by the "
           "data-defined sets of Section D (reference = cells neither high-paid nor high later growth); column (5) "
           "the same sets defined on industry groups; column (6) the pre-chosen illustrative industries only. "
           "Controls: mean age in each window, birth-year quadratic.", ""]
    md += table([h for _, _, _, h in specs], panels)

def sec_panel(d, md, label, yearcol="year"):
    z = d[d["valid"] & d["lw"].notna() & d["eset"].notna()].copy()
    keys = ("hh", "hlo", "hgo", "hhI", "hloI", "hgoI", "flp")
    for k in keys:
        z[f"s1_{k}"] = z["s1"] * z[f"e_{k}"]
        z[f"s2_{k}"] = z["s2"] * z[f"e_{k}"]
    specs = [(("s1_hh", "s2_hh", "s1_hlo", "s2_hlo", "s1_hgo", "s2_hgo"), "(1) ln wage, person FE: early cell sets"),
             (("s1_hhI", "s2_hhI", "s1_hloI", "s2_hloI", "s1_hgoI", "s2_hgoI"),
              "(2) ln wage, person FE: early industry sets"),
             (("s1_flp", "s2_flp"), "(3) illustrative: early finance / insurance / legal / professional")]
    infos = [fit_fe(f"pfe{label[0]}{k}", z, "lw", xs, yearcol=yearcol) for k, (xs, _) in enumerate(specs)]
    rowsdef = [("hh", "cell high-paid AND high later growth"), ("hlo", "cell high-paid only"),
               ("hgo", "cell high later growth only"), ("hhI", "industry high-paid AND high later growth"),
               ("hloI", "industry high-paid only"), ("hgoI", "industry high later growth only"),
               ("flp", "illustrative finance / insurance / legal / professional")]
    parts = [("slope 25-35 (per 10 yrs)", lambda k_: [(f"s1_{k_}", 1.0)]),
             ("slope 35-55 (per 10 yrs)", lambda k_: [(f"s2_{k_}", 1.0)]),
             ("acceleration = slope 35-55 - slope 25-35", lambda k_: [(f"s2_{k_}", 1.0), (f"s1_{k_}", -1.0)])]
    panels = []
    for g, gname in GROUPS4:
        rows = []
        for k_, lab in rowsdef:
            for part, tf in parts:
                cs = []
                for j_, (xs, h) in enumerate(specs):
                    if f"s1_{k_}" in xs:
                        t = coL(f"pfe{label[0]}{j_}", "lw", g, tf(k_))
                        cs.append(cell(t))
                        rec(f"A3 within-person growth {label}", g, h, f"{k_} {part}", t)
                    else:
                        cs.append("")
                rows.append((f"early {lab} x {part}", cs))
        if g != "BW":
            rows.append(("Person FE, year FE, common kink at 35; N son-years / sons / clusters",
                         [f"{inf[g][0]:,} / {inf[g][1]:,} / {inf[g][2]:,}" if g in inf else "" for inf in infos]))
        panels.append((gname, rows))
    md += [f"### A3{label[0]}. Within-person wage growth before and after 35 by early set ({label})", "",
           "Son-year regressions of ln wage on person fixed effects, year fixed effects, a common kink at 35 and the "
           "early-set indicators interacted with the piecewise age terms (s1 = min(age-35,0)/10, s2 = "
           "max(age-35,0)/10). Coefficients = slope differences (log points per 10 years) relative to sons whose "
           "early cell / industry is in neither set (column 3: relative to all other industries). Person FE remove "
           "cohort and level differences; with person and year FE the common linear age slope is not identified, the "
           "differences are. Ages 25-55, all son-years of sons with an early cell.", ""]
    md += table([h for _, h in specs], panels)

# ================================================================ A(ii): Gelbach with early industry x band FE
def gelbach(tag, d, specs, ctrl, need, bands=BANDS):
    out = {}
    for name, fe, lab, mask in specs:
        fes = (fe,) if isinstance(fe, str) else tuple(fe)
        dd = d[mask].copy()
        run_cells(f"{tag}s_{name}", dd, ("lw",), ("lyp",), ctrl, tuple(need) + fes, bands=bands)
        run_cells(f"{tag}l_{name}", dd, ("lw",), ("lyp",),
                  lambda z, fes=fes: np.column_stack([ctrl(z)] + [dummies(z[f]) for f in fes]), tuple(need) + fes,
                  bands=bands)
        out[name] = " + ".join(str(dd[f].nunique()) for f in fes)
    return out


def pool_small(d, col, min_sons=10):
    """son-level FE code with cells of < min_sons sons (all Black + White sons) pooled into one code."""
    s = d.drop_duplicates("pid")[["pid", col]].dropna()
    n = s[col].value_counts()
    small = n.index[n < min_sons]
    return d[col].where(~d[col].isin(small), -1.0)


def placebo(tag, d, fe, mask, ctrl, need, reps=10, seed=7):
    """permute the son-level FE label across sons within race (cell sizes kept) and redo the Gelbach."""
    rng = np.random.default_rng(seed)
    out = []
    s = d[mask].drop_duplicates("pid")[["pid", "race", fe]]
    for k in range(reps):
        perm = s.copy()
        for race, z in perm.groupby("race"):
            perm.loc[z.index, fe] = rng.permutation(z[fe].to_numpy())
        dd = d.copy()
        dd[fe + "_pl"] = dd["pid"].map(perm.set_index("pid")[fe])
        nm = f"pl{k}"
        gelbach(tag, dd, [(nm, fe + "_pl", "", mask)], ctrl, need)
        out.append((safe(con_change(tag, nm, "P"))[0], sratio(con_change(tag, nm, "P"), Dch(f"{tag}s_{nm}", "lw", "P"))[0],
                    safe(con_change(tag, nm, "BW"))[0],
                    sratio(con_change(tag, nm, "BW"), Dch(f"{tag}s_{nm}", "lw", "BW"))[0]))
    return np.array(out)


def con_terms(tag, name, lo, hi, g):
    s_ = L(f"{tag}s_{name}", "lw", lo, hi, g)
    l_ = L(f"{tag}l_{name}", "lw", lo, hi, g)
    return s_ + [(k, -c) for k, c in l_]


def con_change(tag, name, g, b=(35, 55)):
    return [(k, c) for k, c in con_terms(tag, name, *b, g)] + [(k, -c) for k, c in con_terms(tag, name, 25, 34, g)]


def sec_gelbach_table(tag, specs, nfe, md, label):
    hdr = ["(1) accounted for at 25-34 (short - long)", "(2) accounted for at 35-55", "(3) change (35-55)-(25-34) "
           "of the part accounted for", "(4) rise of the coefficient on this sample (short)", "(5) share = (3)/(4)",
           "(6) B-W: change of the part accounted for", "(7) change of the B-W gap (short)", "(8) share = (6)/(7)",
           "(9) pooled: change (45-55)-(25-34) of the part accounted for", "(10) its share"]
    rows = []
    for name, fe, lab, _ in specs:
        s_ch, s_bw = Dch(f"{tag}s_{name}", "lw", "P"), Dch(f"{tag}s_{name}", "lw", "BW")
        s_45 = Dch(f"{tag}s_{name}", "lw", "P", b=(45, 55))
        t = [safe(con_terms(tag, name, 25, 34, "P")), safe(con_terms(tag, name, 35, 55, "P")),
             safe(con_change(tag, name, "P")), safe(s_ch), sratio(con_change(tag, name, "P"), s_ch),
             safe(con_change(tag, name, "BW")), safe(s_bw), sratio(con_change(tag, name, "BW"), s_bw),
             safe(con_change(tag, name, "P", b=(45, 55))), sratio(con_change(tag, name, "P", b=(45, 55)), s_45)]
        rows.append((f"{lab} [{nfe[name]} cells]", [cell(x) for x in t]))
        for h, x in zip(hdr, t):
            rec(f"A2 Gelbach {label}", "", h, name, x)
    md += table(hdr, [("Long regression adds (fixed effects estimated separately in each band and race sample)", rows)])
    panels = []
    for name, fe, lab, _ in specs:
        rws = []
        for g, gname in GROUPS4:
            cs = []
            for lo, hi in BANDS:
                cs += [sc(L(f"{tag}s_{name}", "lw", lo, hi, g)), sc(L(f"{tag}l_{name}", "lw", lo, hi, g))]
                rec(f"A2 Gelbach detail {label}", g, f"short {lo}-{hi}", name, safe(L(f"{tag}s_{name}", "lw", lo, hi, g)))
                rec(f"A2 Gelbach detail {label}", g, f"long {lo}-{hi}", name, safe(L(f"{tag}l_{name}", "lw", lo, hi, g)))
            rws.append((gname, cs))
        ns = [f"{lo}-{hi}: {RES[K(f'{tag}s_{name}', 'lw', lo, hi, 'P')]['n']:,}" for lo, hi in BANDS[:3]
              if K(f"{tag}s_{name}", "lw", lo, hi, "P") in RES]
        kb = [K(f"{tag}s_{name}", "lw", lo, hi, g) for lo, hi in BANDS[:3] for g in ("B", "W")]
        rws.append(("N son-years: pooled per band ; Black / White per band", [" ; ".join(ns)] +
                    [" ; ".join(f"{RES[k]['n']:,}" for k in kb if k in RES)] + [""] * 6))
        panels.append((lab, rws))
    hdr2 = []
    for lo, hi in BANDS:
        hdr2 += [f"ln wage {lo}-{hi}: short", f"ln wage {lo}-{hi}: long"]
    md += ["Short and long coefficients by band (detail):", ""] + table(hdr2, panels)


# ================================================================ C: within-industry heterogeneity
def sec_hetero(S, d, md, label, yearcol="year", tagp=""):
    xs = ("lyp_c", "e_hh", "e_hh_lyp", "e_hlo", "e_hlo_lyp", "e_hgo", "e_hgo_lyp")
    specs = [("d40", "40", "(1) Delta ln wage (40-55) - (25-34)"), ("d35", "35", "(2) Delta ln wage (35-55) - (25-34)"),
             ("d45", "45", "(3) Delta ln wage (45-55) - (25-34)")]
    infos = [fitc(f"{tagp}het{k}", S, y, xs, ctrl_for(nm)) for k, (y, nm, _) in enumerate(specs)]
    infl = fitc(f"{tagp}hetflp", S, "d40", ("lyp_c", "e_flp", "e_flp_lyp"), ctrl_for("40"))
    z = d[d["valid"] & d["lw"].notna() & d["eset"].notna()].copy()
    z["lyp_c"] = z["lyp"] - S["lyp"].mean()
    for k in (1, 2):
        s = z[f"s{k}"]
        z[f"s{k}_lyp"] = s * z["lyp_c"]
        for key in ("hh", "hlo", "hgo"):
            z[f"s{k}_{key}"] = s * z[f"e_{key}"]
            z[f"s{k}_{key}_lyp"] = s * z[f"e_{key}"] * z["lyp_c"]
    xfe = tuple(f"s{k}_{v}" for k in (2, 1) for v in ("lyp", "hh", "hh_lyp", "hlo", "hlo_lyp", "hgo", "hgo_lyp"))
    infe = fit_fe(f"{tagp}hetfe", z, "lw", xfe, yearcol=yearcol)
    hdr = [h for _, _, h in specs] + ["(4) ln wage, person FE: slope 35-55 terms", "(5) ... slope 25-35 terms",
                                      "(6) illustrative: Delta (40-55) with finance / insurance / legal / professional"]
    labs = [("lyp", "ln parental income (gradient in cells of neither set)"),
            ("hh_lyp", "ln parental income x early high-paid high-growth cell (extra gradient inside)"),
            ("inside", "gradient inside high-paid high-growth cells = sum of the two rows above"),
            ("hh", "early high-paid high-growth cell"),
            ("hlo_lyp", "ln parental income x early high-paid-only cell"), ("hlo", "early high-paid-only cell"),
            ("hgo_lyp", "ln parental income x early high-growth-only cell"), ("hgo", "early high-growth-only cell"),
            ("flp_lyp", "illustrative: ln parental income x early finance / insurance / legal / professional"),
            ("flp", "illustrative: early finance / insurance / legal / professional")]
    son = {"lyp": "lyp_c", "hh_lyp": "e_hh_lyp", "hh": "e_hh", "hlo_lyp": "e_hlo_lyp", "hlo": "e_hlo",
           "hgo_lyp": "e_hgo_lyp", "hgo": "e_hgo"}
    panels = []
    for g, gname in GROUPS4:
        rows = []
        for key, lab in labs:
            cs = []
            for k, (y, nm, h) in enumerate(specs):
                if key == "inside":
                    t = coL(f"{tagp}het{k}", y, g, [("lyp_c", 1.0), ("e_hh_lyp", 1.0)])
                elif key in son:
                    t = co(f"{tagp}het{k}", y, g, son[key])
                else:
                    t = NAN3
                cs.append(cell(t))
                if np.isfinite(t[0]):
                    rec(f"C heterogeneity {label}", g, h, lab, t)
            for pre, h in (("s2", hdr[3]), ("s1", hdr[4])):
                if key == "inside":
                    t = coL(f"{tagp}hetfe", "lw", g, [(f"{pre}_lyp", 1.0), (f"{pre}_hh_lyp", 1.0)])
                elif key in son:
                    t = co(f"{tagp}hetfe", "lw", g, f"{pre}_{key}")
                else:
                    t = NAN3
                cs.append(cell(t))
                if np.isfinite(t[0]):
                    rec(f"C heterogeneity {label}", g, h, lab, t)
            fl = {"lyp": "lyp_c", "flp_lyp": "e_flp_lyp", "flp": "e_flp"}
            t = co(f"{tagp}hetflp", "d40", g, fl[key]) if key in fl else NAN3
            cs.append(cell(t))
            rows.append((lab, cs))
        if g != "BW":
            ss = D27.subset(S, g)[0]
            rows.append(("N sons / clusters (1)-(3), (6); son-years / sons (4)-(5)",
                         [nfo(infos[k], g) for k in range(3)] +
                         [f"{infe[g][0]:,} / {infe[g][1]:,}" if g in infe else ""] * 2 + [nfo(infl, g)]))
            rows.append(("Sons with an early high-paid high-growth cell (with Delta 40-55)",
                         [f"{int((ss['e_hh'] == 1).sum()):,} ({int(((ss['e_hh'] == 1) & ss['d40'].notna()).sum()):,})"]
                         + [""] * 4 + [f"FLP: {int((ss['e_flp'] == 1).sum()):,}"]))
        panels.append((gname, rows))
    md += [f"## C{label[0]}. Fast track inside high-paid, high-later-growth cells? ({label})", "",
           "Is the after-35 wage growth steeper for sons of richer parents WITHIN the data-defined high-paid / "
           "high-growth cells (Section D) than elsewhere? (1)-(3): son-level growth on centred ln parental income, "
           "early-set indicators and their interactions (controls as A1). (4)-(5): one son-year regression with person "
           "FE and year FE, where the piecewise age terms are interacted with ln parental income, the early-set "
           "indicators and the triple products; (4) shows the slope-after-35 terms, (5) the slope-before-35 terms (log "
           "points per 10 years per log point of parental income). (6): the pre-chosen illustrative industries instead "
           "of the data-defined sets.", ""]
    md += table(hdr, panels)

# ================================================================ D: data-defined occupation x industry cells
def sec_datasets(S, MF, md, label="PSID"):
    st = MF["sets"]
    T, G = st["T"].copy(), MF["grp"]
    ns = S.groupby("eog").size()
    sb = S.groupby("eog")["black"].mean()
    T["sons"] = [int(ns.get(o * 100 + j, 0)) for o, j in zip(T["o"], T["j"])]
    T["sblack"] = [sb.get(o * 100 + j, np.nan) for o, j in zip(T["o"], T["j"])]
    shares = T.groupby("set")["w"].sum()
    flp_in = T[T["j"].isin(FLP)]
    fl = flp_in.groupby("set")["w"].sum() / flp_in["w"].sum()

    def rows_for(z, top=None):
        z = z.sort_values("w", ascending=False)
        if top:
            z = z.head(top)
        out = []
        for (o, j), r_ in z.iterrows():
            out.append(f"| {ONAMES[int(o)]} x {GNAMES[int(j)]}{' (FLP)' if int(j) in FLP else ''} | {r_['lvl']:.3f} | "
                       f"{r_['G25']:.3f} | {r_['G35']:.3f} | {int(r_['n']):,} | {r_['w']:.4f} | "
                       f"{'yes' if r_['own'] else 'fallback'} | {int(r_['sons']):,} | "
                       f"{'' if not np.isfinite(r_['sblack']) else format(r_['sblack'], '.2f')} |")
            CSV.append(dict(table="D0 data-defined cells", sample=SETN[int(r_['set'])], outcome="cell",
                            term=f"{ONAMES[int(o)]} x {GNAMES[int(j)]}", coef=r_["G35"], se=r_["lvl"], n=r_["n"],
                            mean=r_["w"]))
        return out
    hdr = ["| Cell (occupation group x industry group) | level (age-weighted Q) | band growth (25-29)->(35-39) | band "
           "growth (35-39)->(50-54) | MORG men | employment share | own profile | PSID sons (early cell) | share "
           "Black among them |", "|---|---|---|---|---|---|---|---|---|"]
    ind_rows = ["| Industry-group set | industries |", "|---|---|"]
    for k in (1, 2, 3):
        ind_rows.append(f"| {SETN[k]} | " + "; ".join(GNAMES[int(i)] for i in G.index[G["set"] == k]) + " |")
    # shares of sons by race x tercile
    sh = ["| Race | parental-income tercile | sons with an early cell | " + " | ".join(SETN[k] for k in (1, 2, 3, 0)) +
          " | illustrative: early FLP industry |", "|---|---|---|---|---|---|---|---|"]
    for race in ("Black + White", "Black", "White"):
        s = S if race == "Black + White" else S[S["race"] == race]
        for tq in (None, 1, 2, 3):
            z = s[s["eset"].notna()]
            z = z if tq is None else z[z["terc"] == tq]
            if len(z) < 20:
                continue
            vals = [(z["eset"] == k).mean() for k in (1, 2, 3, 0)] + [z["e_flp"].mean()]
            sh.append(f"| {race} | {'all' if tq is None else tq} | {len(z):,} | " + " | ".join(f"{v:.3f}" for v in vals)
                      + " |")
            CSV.append(dict(table="D1 set shares", sample=f"{race} T{tq or 'all'}", outcome="HH share", coef=vals[0],
                            n=len(z)))
    gm = ["| Early cell set | sons | sons observed at 40-55 | mean Delta(40-55) | mean ln wage 25-34 | mean ln parental "
          "income | Black share |", "|---|---|---|---|---|---|---|"]
    for k in (1, 2, 3, 0):
        z = S[S["eset"] == k]
        gm.append(f"| {SETN[k]} | {len(z):,} | {int(z['d40'].notna().sum()):,} | {z['d40'].mean():.3f} | "
                  f"{z['lw0'].mean():.3f} | {z['lyp'].mean():.3f} | {z['black'].mean():.3f} |")
    md += [f"## D. Data-defined groups: high-paid and high-later-growth occupation x industry cells ({label})", "",
           "All 11 x 33 occupation group x industry group cells observed in CPS MORG 1992-2002 (men 25-64) are ranked by "
           "their nonlinear band profile: LEVEL = age-weighted relative wage, LATER GROWTH = band growth from 35-39 to "
           "50-54 (both relative to men of the same age). 'High-paid' = top quartile of men's employment by level "
           f"(level >= {st['thrL']:.3f}); 'high later growth' = top quartile by later growth (>= {st['thrG']:.3f}); the "
           "headline group is their intersection. Employment shares: " +
           "; ".join(f"{SETN[k]} {shares.get(k, 0):.3f}" for k in (1, 2, 3, 0)) +
           ". The same ranking on the 33 industry groups (industry sets) is a secondary grouping. Of men in the "
           "finance / insurance / legal / professional industries (the PI's examples), " +
           "; ".join(f"{fl.get(k, 0):.2f} are in '{SETN[k]}'" for k in (1, 2, 3, 0)) + ".", "",
           "### D0. Cells in the 'high-paid AND high later growth' set (all, by employment)", ""] + hdr + \
        rows_for(T[T["set"] == 1]) + ["", "### D0b. Largest cells that are high-paid only (top 15 by employment)", ""] + \
        hdr + rows_for(T[T["set"] == 2], 15) + ["", "### D0c. Largest cells with high later growth only (top 15)", ""] + \
        hdr + rows_for(T[T["set"] == 3], 15) + ["", "### D0d. Industry-group sets (same ranking on 33 industry groups)",
                                                ""] + ind_rows + \
        ["", "### D1. Shares of sons by early cell set, race and parental-income tercile (unweighted; pooled terciles)",
         ""] + sh + ["", "Mean growth by early cell set (descriptive):", ""] + gm + ["", "D3_PLACEHOLDER", ""]


# ================================================================ D3: access to high-paid cells (son-level LPMs)
def sec_access(S, d, md):
    S = S.copy()
    fs = d.drop_duplicates("pid").set_index("pid")["fset"]
    S["fa_hh"] = (S["pid"].map(fs) == 1).astype(float).where(S["pid"].map(fs).notna())
    S["white"] = (S["race"] == "White").astype(float)
    for c_, race, tq in (("bT2", "Black", 2), ("bT3", "Black", 3), ("wT1", "White", 1), ("wT2", "White", 2),
                         ("wT3", "White", 3), ("T2", None, 2), ("T3", None, 3)):
        rm = (S["race"] == race) if race else pd.Series(True, index=S.index)
        S[c_] = (rm & (S["terc"] == tq)).astype(float).where(S["terc"].notna())
    S["y_hh"] = (S["eset"] == 1).astype(float).where(S["eset"].notna())
    S["y_hp"] = S["eset"].isin([1, 2]).astype(float).where(S["eset"].notna())

    def ctrl(z):
        return np.column_stack([np.ones(len(z)), z["coh"].to_numpy(float), z["coh"].to_numpy(float) ** 2])
    specs = [("a", ("lyp",)), ("b", ("white",)), ("c", ("white", "lyp")),
             ("d", ("bT2", "bT3", "wT1", "wT2", "wT3", "T2", "T3")), ("e", ("white", "lyp", "fa_hh", "educ_c"))]
    cols, infos = [], []
    for y, ylab in (("y_hh", "early cell high-paid AND high later growth"), ("y_hp", "early cell high-paid (any)")):
        for k, xs in specs:
            if k == "d":                       # pooled: race x tercile cells; race samples: tercile indicators
                inf = fitc(f"acc_{y}_{k}", S, y, xs[:5], ctrl, groups=("P",))
                inf.update(fitc(f"acc_{y}_{k}", S, y, xs[5:], ctrl, groups=("B", "W")))
            else:
                inf = fitc(f"acc_{y}_{k}", S, y, xs, ctrl)
            infos.append(inf)
            cols.append((y, k, xs, f"({len(cols) + 1}) {ylab}: ({k})"))
    labs = [("lyp", "ln parental income"), ("white", "White"), ("bT2", "Black, tercile 2 (ref. Black tercile 1)"),
            ("bT3", "Black, tercile 3"), ("wT1", "White, tercile 1"), ("wT2", "White, tercile 2"),
            ("wT3", "White, tercile 3"), ("T2", "tercile 2 (within-race samples; ref. tercile 1)"),
            ("T3", "tercile 3 (within-race samples)"), ("fa_hh", "father in a high-paid high-growth cell"),
            ("educ_c", "years of education")]
    panels = []
    for g, gname in GROUPS4:
        rws = []
        for x, lab in labs:
            cs, any_ = [], False
            for y, k, xs, h in cols:
                t = co(f"acc_{y}_{k}", y, g, x) if x in xs else NAN3
                if g == "BW" and x in ("white", "bT2", "bT3", "wT1", "wT2", "wT3"):
                    t = NAN3
                if g == "P" and x in ("T2", "T3"):
                    t = NAN3
                cs.append(cell(t))
                any_ = any_ or bool(cell(t))
                if np.isfinite(t[0]):
                    rec("D3 access LPM", g, h, x, t)
            if any_:
                rws.append((lab, cs))
        if g == "P":
            cs = []
            for y, k, xs, h in cols:
                t = safe([(((f"acc_{y}_{k}", y, "P"), "wT3"), 1.0), (((f"acc_{y}_{k}", y, "P"), "bT3"), -1.0)]) \
                    if k == "d" else NAN3
                cs.append(cell(t))
                if np.isfinite(t[0]):
                    rec("D3 access LPM", g, h, "wT3 - bT3", t)
            rws.append(("contrast: White tercile 3 - Black tercile 3", cs))
        if g != "BW":
            rws.append(("Mean of outcome", [f"{i[g][3]:.3f}" if g in i else "" for i in infos]))
            rws.append(("N sons / clusters", [nfo(i, g) for i in infos]))
        panels.append((gname, rws))
    md_ = ["### D3. Access to high-paid cells at 25-34: does the racial gap survive parental income and the father's "
           "job?", "",
           "Son-level linear probability models; outcome (column header) = the son's early cell (modal at 25-34) is in "
           "the data-defined 'high-paid AND high later growth' set (1)-(5) or in any high-paid cell (6)-(10). "
           "Regressors: (a) ln parental income; (b) White; (c) both; (d) race x pooled parental-income tercile cells "
           "(reference Black tercile 1; in the race samples tercile indicators); (e) (c) + the father's cell (modal "
           "at son ages 12-18) in the high-paid high-growth set + years of education (sons with a father's cell). "
           "Controls: birth-year quadratic. Pooled weighted, by race unweighted; clusters 1968 family. Descriptive: "
           "education is itself an outcome of parental resources, so (e) splits the gap into a part running through "
           "education and the father's job and the rest.", ""]
    md_ += table([h for _, _, _, h in cols], panels)
    return md_


# ================================================================ D2: illustrative named cells
def sec_cells(S, MF, md, label, tagp=""):
    rows = ["| Race | parental-income tercile | sons with an early cell | " + " | ".join(CELLN[k] for k in (1, 2, 3)) +
            " | any of (1)-(3) | " + CELLN[4] + " |", "|---|---|---|---|---|---|---|---|"]
    for race in ("Black + White", "Black", "White"):
        s = S if race == "Black + White" else S[S["race"] == race]
        for tq in (None, 1, 2, 3):
            z = s[s["ecell"].notna()]
            z = z if tq is None else z[z["terc"] == tq]
            if len(z) < 20:
                continue
            vals = [(z["ecell"] == k).mean() for k in (1, 2, 3)] + [z["ecell"].isin([1, 2, 3]).mean(),
                                                                     (z["ecell"] == 4).mean()]
            rows.append(f"| {race} | {'all' if tq is None else tq} | {len(z):,} | " + " | ".join(f"{v:.3f}" for v in vals)
                        + " |")
            CSV.append(dict(table=f"D1 cell shares {label}", sample=f"{race} T{tq or 'all'}", outcome="elite share",
                            coef=vals[3], n=len(z)))
    g2 = ["| Early cell | sons | sons observed at 40-55 | mean Delta(40-55) | mean ln wage 25-34 | Black share | MORG Q "
          "25-29 | MORG Q 35-39 | MORG Q 50-54 | MORG band growth (35-39)->(50-54) | MORG men |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    cq = MF["cells5"]
    for k in (1, 2, 3, 4, 5):
        z = S[S["ecell"] == k]
        q = cq.loc[k] if k in cq.index else pd.Series({c: np.nan for c in QC + ["n"]})
        g2.append(f"| {CELLN[k]} | {len(z):,} | {int(z['d40'].notna().sum()):,} | {z['d40'].mean():.3f} | "
                  f"{z['lw0'].mean():.3f} | {z['black'].mean():.3f} | {q['Q0']:.3f} | {q['Q2']:.3f} | {q['Q5']:.3f} | "
                  f"{q['Q5'] - q['Q2']:.3f} | {int(q['n']) if q['n'] == q['n'] else 0:,} |")

    def ctrl(z):
        return ctrl_for("40")(z)
    S = S.copy()
    S["e_elite_lyp"] = S["e_elite"] * S["lyp_c"]
    specs = [(("c1", "c2", "c3", "c4"), "(1) Delta ln wage (40-55) - (25-34)"),
             (("c1", "c2", "c3", "c4", "lyp_c"), "(2) ... + ln parental income"),
             (("e_elite", "lyp_c", "e_elite_lyp"), "(3) ... special cells (1)-(3) x ln parental income")]
    infos = [fitc(f"{tagp}cel{k}", S, "d40", xs, ctrl) for k, (xs, _) in enumerate(specs)]
    labs = [("c1", "early " + CELLN[1]), ("c2", "early " + CELLN[2]), ("c3", "early " + CELLN[3]),
            ("c4", "early " + CELLN[4]), ("e_elite", "early any of cells (1)-(3)"), ("lyp_c", "ln parental income"),
            ("e_elite_lyp", "ln parental income x cells (1)-(3)")]
    panels = []
    for g, gname in GROUPS4:
        rws = []
        for x, lab in labs:
            cs = []
            for k, (xs, h) in enumerate(specs):
                if x in xs:
                    t = co(f"{tagp}cel{k}", "d40", g, x)
                    cs.append(cell(t))
                    rec(f"D2 growth by early cell {label}", g, h, x, t)
                else:
                    cs.append("")
            rws.append((lab, cs))
        if g != "BW":
            rws.append(("N sons / clusters", [nfo(i, g) for i in infos]))
        panels.append((gname, rws))
    md += [f"### D2. Illustrative pre-named cells ({label}; small cells, no headline)", "",
           "Cells defined in the docstring (occ1990dd x industry group); the son's early cell = modal cell over his "
           "25-34 son-years with both codes. Shares by race and parental-income tercile (pooled terciles, unweighted):",
           ""] + rows + ["", "Mean growth and MORG band profiles by early cell (MORG: CPS men 25-64 in the same "
                         "cell, wage relative to men of the same age):", ""] + g2 + [""]
    md += ["Son-level regressions on early-cell indicators (reference = all other occupations / industries); controls "
           "as A1. The contribution of the early cells to the divergence is the 'early occupation x industry cell' "
           "row of Table A2.", ""]
    md += table([h for _, h in specs], panels)


# ================================================================ F: following the father at the cell level
FOLS = [("f_cell", "og", "fog", "father's cell (occupation group x industry group)"),
        ("f_ind", "igrp", "fgrp", "father's industry group (33; as 32)"),
        ("f_occ", "occ11", "focc11", "father's occupation group (11; as 32)")]


def sec_follow(d, md, fathers):
    f = fathers.copy()
    f["og"] = f["occ11"] * 100 + f["f_igrp"]
    fc = f.dropna(subset=["og"]).groupby("pid")["og"].agg(mode)
    d["fog"] = d["pid"].map(fc)
    d["fset"] = cell_set(np.floor(d["fog"] / 100), d["fog"] % 100, MF_G)
    v = d["valid"]
    d["f_cell"] = (d["og"] == d["fog"]).astype(float).where(v & d["og"].notna() & d["fog"].notna())
    # F1 frequency vs random matching
    dd = d[v & d["lw"].notna()]
    rows = ["| Race | sons' ages | " + " | ".join(f"{lab}: observed | benchmark | ratio" for _, _, _, lab in FOLS) +
            " | son-years / sons (cell) |", "|---|---|" + "---|---|---|" * len(FOLS) + "---|"]
    OUTD = {}
    for race in ("Black + White", "Black", "White"):
        dr = dd if race == "Black + White" else dd[dd["race"] == race]
        for lo, hi in ((25, 34), (35, 55)):
            z = dr[dr["age"].between(lo, hi)]
            cs = []
            for fv, s_, f_, _ in FOLS:
                obs = z[fv].mean()
                parts = []
                for _, zz in z.groupby(["race", "terc"]):
                    zz = zz[zz[fv].notna()]
                    if len(zz):
                        parts.append((D32.bench(zz, s_, f_), len(zz)))
                bm = sum(a * n for a, n in parts) / max(1, sum(n for _, n in parts))
                cs += [f"{obs:.3f}", f"{bm:.3f}", f"{obs / bm:.2f}" if bm > 0 else ""]
                OUTD[(race, lo, fv)] = (obs, bm)
                CSV.append(dict(table="F1 following frequency", sample=race, outcome=fv, term=f"{lo}-{hi}", coef=obs,
                                mean=bm, n=z[fv].notna().sum()))
            zc = z[z["f_cell"].notna()]
            rows.append(f"| {race} | {lo}-{hi} | " + " | ".join(cs) + f" | {len(zc):,} / {zc['pid'].nunique():,} |")
    s1 = d.drop_duplicates("pid")
    nfc = s1.groupby("race")["fog"].apply(lambda x: x.notna().sum())
    ndist = s1["fog"].nunique()
    drift = d.loc[d["f_cell"].notna(), "isch"].ne("1970").mean() if "isch" in d else np.nan
    md += ["## F. Following the father at the occupation x industry cell level (PSID)", "",
           "Father = male head of the son's family at 16 (24's fpid); his cell = modal occupation group (11) x industry "
           "group (33) over his head-waves with the son aged 12-18 (32 Section 4 for his industry and occupation "
           f"separately). Sons with a father's cell: Black {int(nfc.get('Black', 0)):,}, White "
           f"{int(nfc.get('White', 0)):,}; {ndist} distinct father cells. **Coding drift:** fathers are coded almost "
           f"only in 1970 Census codes, while {drift:.1%} of the sons' following son-years are coded in 2000 / 2010 "
           "codes (waves 2003+); both are bridged to occ1990dd / ind1990ddx, but a cell match requires both codes to "
           "agree, so some measured non-following is coding drift (more than for industry or occupation alone). The "
           "PSID has no employer identifiers.", "",
           "### F1. How often do sons work in the father's cell?", "",
           "Unweighted share of son-years; benchmark = random matching of sons to fathers within race x "
           "parental-income tercile (sum_j p_son(j) p_father(j)); ratio = observed / benchmark.", ""] + rows + [""]
    # F2 following on parental income
    for fv, _, _, _ in FOLS:
        run_cells(f"fl_{fv}", d[v].copy(), (fv,), ("lyp",), ctrl_lsn, ("A", "C"), bands=[(25, 34), (35, 55)])
    panels = []
    for g, gname in GROUPS4:
        rws = []
        for lo, hi in ((25, 34), (35, 55)):
            t = [safe(L(f"fl_{fv}", fv, lo, hi, g)) for fv, _, _, _ in FOLS]
            rws.append((f"ln parental income, sons {lo}-{hi}", [cell(x) for x in t]))
            for (fv, _, _, _), x in zip(FOLS, t):
                rec("F2 following on parental income", g, fv, f"{lo}-{hi}", x)
            if g != "BW":
                rws.append((f"Mean / N son-years, {lo}-{hi}",
                            [f"{RES[K(f'fl_{fv}', fv, lo, hi, g)]['mean']:.3f} / {RES[K(f'fl_{fv}', fv, lo, hi, g)]['n']:,}"
                             if K(f"fl_{fv}", fv, lo, hi, g) in RES else "" for fv, _, _, _ in FOLS]))
        t = [safe(Dch(f"fl_{fv}", fv, g)) for fv, _, _, _ in FOLS]
        rws.append(("Change (35-55) - (25-34)", [cell(x) for x in t]))
        panels.append((gname, rws))
    md += ["### F2. Does following rise with parental income?", "",
           "Son-year linear probability models (outcome = son works in the father's cell / industry group / "
           "occupation group) on ln parental income, Lee-Solon controls, sons with the father's code.", ""]
    md += table([f"({k + 1}) son in the {lab}" for k, (_, _, _, lab) in enumerate(FOLS)], panels)
    # F3 pay-off: level and growth, holding education and the cell's profile fixed
    d["g30"] = d["g_lw"]
    cols = [("lw", (25, 34), "(1) ln wage, 25-34"), ("lw", (35, 55), "(2) ln wage, 35-55"),
            ("g30", (30, 55), "(3) annual ln wage growth, 30-55"), ("g30", (35, 55), "(4) annual ln wage growth, 35-55"),
            ("g_stay", (35, 55), "(5) annual growth with the same employer, 35-55")]
    panels = []
    for fv, _, _, lab in FOLS:
        z = d[v & d[fv].notna()].copy()
        z["fol"] = z[fv]
        for y, (lo, hi), _ in cols:
            run_cells(f"pay_{fv}_{y}", z, (y,), ("fol", "lyp", "educ", "ck_t", "ck_slope"), ctrl_ageyr, ("C",),
                      bands=[(lo, hi)])
        for g, gname in GROUPS4:
            t = [safe(L(f"pay_{fv}_{y}", y, lo, hi, g, "fol")) for y, (lo, hi), _ in cols]
            rws = [("son in the " + lab, [cell(x) for x in t])]
            for (y, (lo, hi), h), x in zip(cols, t):
                rec("F3 following pay-off", g, h, fv, x)
            if g != "BW":
                rws.append(("N son-years / clusters", [f"{RES[K(f'pay_{fv}_{y}', y, lo, hi, g)]['n']:,} / "
                                                       f"{RES[K(f'pay_{fv}_{y}', y, lo, hi, g)]['G']:,}"
                                                       if K(f"pay_{fv}_{y}", y, lo, hi, g) in RES else ""
                                                       for y, (lo, hi), _ in cols]))
            panels.append((f"Following = {lab}: {gname}", rws))
    md += ["### F3. Pay-off of following: wage level and wage growth", "",
           "Son-year regressions (outcome in the column header; growth = annualised change between consecutive "
           "interviews 1-2 years apart, (5) for sons who stayed with the employer). Regressor of interest: following. "
           "Held fixed: ln parental income, years of education, the current cell's MORG relative wage at the son's "
           "age band (ck) and its local age slope (so the coefficient is the advantage over other sons in equally paid "
           "cells with equally steep profiles); age quartic, year FE. Clusters 1968 family; pooled weighted. "
           "Followers may differ in unobserved ways (descriptive).", ""]
    md += table([h for _, _, h in cols], panels)
    # F4 tenure x following (person FE)
    zt = d[v & d["lw"].notna() & d["tenure"].notna() & d["age"].between(25, 55)].copy()
    zt["ten"] = zt["tenure"] / 10
    zt["ten2"] = zt["ten"] ** 2
    zt["ten_lyp"] = zt["ten"] * zt["lyp_c"]
    for k in (2, 3, 4):
        zt[f"c{k}a"] = (zt["C"] / 10) ** k
    infos = {}
    for fv, _, _, _ in FOLS:
        zz = zt[zt[fv].notna()].copy()
        zz["fol"] = zz[fv]
        zz["ten_f"] = zz["ten"] * zz["fol"]
        infos[fv] = fit_fe(f"ten_{fv}", zz, "lw", ("ten", "ten2", "ten_f", "fol", "ten_lyp"),
                           common=("c2a", "c3a", "c4a"))
    labs_t = [("ten", "tenure (per 10 years)"), ("ten2", "tenure squared"), ("ten_f", "tenure x following"),
              ("fol", "following"), ("ten_lyp", "tenure x ln parental income")]
    panels = []
    for g, gname in GROUPS4:
        rws = []
        for x, lab in labs_t:
            t = [co(f"ten_{fv}", "lw", g, x) for fv, _, _, _ in FOLS]
            rws.append((lab, [cell(z_) for z_ in t]))
            for (fv, _, _, _), z_ in zip(FOLS, t):
                rec("F4 tenure x following", g, fv, x, z_)
        if g != "BW":
            rws.append(("Person FE, year FE, age quartic; N son-years / sons / clusters",
                        [f"{infos[fv][g][0]:,} / {infos[fv][g][1]:,} / {infos[fv][g][2]:,}" if g in infos[fv] else ""
                         for fv, _, _, _ in FOLS]))
        panels.append((gname, rws))
    md += ["### F4. Wage-tenure profiles of followers (person FE)", "",
           "Within-son regressions of ln wage on tenure with the employer, its square, tenure x following, following, "
           "tenure x ln parental income (centred), age quartic and year FE (waves 1984-2023; tenure observed).", ""]
    md += table([f"({k + 1}) ln wage; following = {lab}" for k, (_, _, _, lab) in enumerate(FOLS)], panels)
    # F5 Gelbach: how much of the divergence is following?
    hdr = ["(1) ln wage on ln parental income (short)", "(2) ... controlling following (long)",
           "(3) accounted for by following = (1) - (2)", "(4) following on ln parental income (pi)",
           "(5) ln wage on following (delta, long)"]
    panels = []
    CON = {}
    for fv, _, _, lab in FOLS:
        z = d[v & d["lw"].notna() & d[fv].notna()].copy()
        z["fol"] = z[fv]
        run_cells(f"fs_{fv}", z, ("lw",), ("lyp",), ctrl_lsn, ("A", "C", "fol"), bands=[(25, 34), (35, 55)])
        run_cells(f"fg_{fv}", z, ("lw",), ("lyp", "fol"), ctrl_lsn, ("A", "C"), bands=[(25, 34), (35, 55)])
        run_cells(f"fp_{fv}", z, ("fol",), ("lyp",), ctrl_lsn, ("A", "C"), bands=[(25, 34), (35, 55)])
        rws = []
        for g, gname in GROUPS4:
            for lo, hi in ((25, 34), (35, 55)):
                s_ = L(f"fs_{fv}", "lw", lo, hi, g)
                l_ = L(f"fg_{fv}", "lw", lo, hi, g, "lyp")
                t = [safe(s_), safe(l_), safe(s_ + [(k, -c) for k, c in l_]), safe(L(f"fp_{fv}", "fol", lo, hi, g)),
                     safe(L(f"fg_{fv}", "lw", lo, hi, g, "fol"))]
                rws.append((f"{gname}, sons {lo}-{hi}", [cell(x) for x in t]))
        s_ = Dch(f"fs_{fv}", "lw", "BW")
        l_ = Dch(f"fg_{fv}", "lw", "BW", x="lyp")
        con = s_ + [(k, -c) for k, c in l_]
        sh = sratio(con, s_)
        rws.append(("Change of the Black - White gap (35-55) - (25-34)", [cell(safe(s_)), cell(safe(l_)),
                                                                          cell(safe(con)), "", ""]))
        rws.append(("Share of the change accounted for by following = (3) / (1)", [cell(sh)] + [""] * 4))
        sP = Dch(f"fs_{fv}", "lw", "P")
        conP = sP + [(k, -c) for k, c in Dch(f"fg_{fv}", "lw", "P", x="lyp")]
        rws.append(("Pooled change (35-55) - (25-34)", [cell(safe(sP)), "", cell(safe(conP)), "", ""]))
        rws.append(("Share of the pooled change accounted for by following", [cell(sratio(conP, sP))] + [""] * 4))
        CON[fv] = dict(bw=safe(con), bwsh=sh, bwtot=safe(s_), p=safe(conP), psh=sratio(conP, sP))
        for c, x in (("B-W change contribution", safe(con)), ("B-W share", sh), ("pooled contribution", safe(conP)),
                     ("pooled share", sratio(conP, sP))):
            rec("F5 following Gelbach", c, fv, "(35-55)-(25-34)", x)
        panels.append((f"Following = {lab}", rws))
    md += ["### F5. How much of the divergence is following the father? (Gelbach)", "",
           "(1) the son's ln wage on ln parental income with Lee-Solon controls; (2) adding the following indicator; "
           "(3) = (1) - (2) = pi x delta. Stacked; clusters 1968 family; common sample per following measure.", ""]
    md += table(hdr, panels)
    # F7 are White sons, and rich White sons, more likely to be in the father's cell?
    d["f_set"] = (d["kset"] == d["fset"]).astype(float).where(v & d["kset"].notna() & d["fset"].notna())
    d["f_hhc"] = (d["kset"] == 1).astype(float).where(v & d["kset"].notna() & (d["fset"] == 1))
    d["white"] = (d["race"] == "White").astype(float)
    d["w_lyp"] = d["white"] * d["lyp_c"]
    rt = [("bT2", "Black, tercile 2", "Black", 2), ("bT3", "Black, tercile 3", "Black", 3),
          ("wT1", "White, tercile 1", "White", 1), ("wT2", "White, tercile 2", "White", 2),
          ("wT3", "White, tercile 3", "White", 3)]
    for c_, _, race, tq in rt:
        d[c_] = ((d["race"] == race) & (d["terc"] == tq)).astype(float).where(d["terc"].notna())
    F7 = [("f_cell", "og", "fog", "father's cell (occupation group x industry group)"),
          ("f_occ", "occ11", "focc11", "father's occupation group (11)"),
          ("f_set", "kset", "fset", "father's data-defined cell set (4 sets)"),
          ("f_hhc", "kset", "fset", "high-paid high-growth set, sons whose father was in it")]
    B2 = [(25, 34), (35, 55)]
    for fv, _, _, _ in F7:
        z = d[v & d[fv].notna()].copy()
        run_cells(f"f7a_{fv}", z, (fv,), ("white",), ctrl_lsn, ("A", "C", "lyp"), bands=B2, groups=("P",))
        run_cells(f"f7b_{fv}", z, (fv,), ("white", "lyp"), ctrl_lsn, ("A", "C"), bands=B2, groups=("P",))
        run_cells(f"f7c_{fv}", z, (fv,), tuple(c_ for c_, _, _, _ in rt), ctrl_lsn, ("A", "C", "lyp"), bands=B2,
                  groups=("P",))
        run_cells(f"f7d_{fv}", z, (fv,), ("white", "lyp_c", "w_lyp"), ctrl_lsn, ("A", "C"), bands=B2, groups=("P",))
    hdrA = ["(1) son in the father's X, 25-34", "(2) ... + ln parental income, 25-34", "(3) son in the father's X, "
            "35-55", "(4) ... + ln parental income, 35-55"]
    panels = []
    for fv, _, _, lab in F7:
        rws = []
        for x, xl in (("white", "White"), ("lyp", "ln parental income")):
            cs = []
            for lo, hi in B2:
                for tg in ("f7a", "f7b"):
                    t = safe(L(f"{tg}_{fv}", fv, lo, hi, "P", x)) if not (tg == "f7a" and x == "lyp") else NAN3
                    cs.append(cell(t))
                    if np.isfinite(t[0]):
                        rec("F7a following by race", fv, f"{tg} {lo}-{hi}", x, t)
            rws.append((xl, cs))
        rws.append(("Mean of outcome / N son-years / clusters",
                    [f"{RES[K(f'{tg}_{fv}', fv, lo, hi, 'P')]['mean']:.3f} / {RES[K(f'{tg}_{fv}', fv, lo, hi, 'P')]['n']:,}"
                     f" / {RES[K(f'{tg}_{fv}', fv, lo, hi, 'P')]['G']:,}" if K(f"{tg}_{fv}", fv, lo, hi, "P") in RES
                     else "" for lo, hi in B2 for tg in ("f7a", "f7b")]))
        panels.append((f"X = {lab}", rws))
    hdrB = ["(1) race x tercile cells, 25-34", "(2) race x tercile cells, 35-55", "(3) White x ln parental income, 25-34",
            "(4) White x ln parental income, 35-55"]
    panelsB = []
    for fv, _, _, lab in F7:
        rws = []
        for c_, cl_, _, _ in rt:
            t = [safe(L(f"f7c_{fv}", fv, lo, hi, "P", c_)) for lo, hi in B2]
            rws.append((f"{cl_} (reference: Black, tercile 1)", [cell(x) for x in t] + ["", ""]))
            for (lo, hi), x in zip(B2, t):
                rec("F7b following by race x tercile", fv, f"{lo}-{hi}", c_, x)
        for nm, terms in (("contrast: White tercile 3 - White tercile 1 (rich vs poor White sons)",
                           [("wT3", 1.0), ("wT1", -1.0)]),
                          ("contrast: White tercile 3 - Black tercile 3 (rich White vs rich Black sons)",
                           [("wT3", 1.0), ("bT3", -1.0)]),
                          ("contrast: Black tercile 3 - Black tercile 1", [("bT3", 1.0)])):
            t = [safe([(K(f"f7c_{fv}", fv, lo, hi, "P", x), c) for x, c in terms]) for lo, hi in B2]
            rws.append((nm, [cell(x) for x in t] + ["", ""]))
            for (lo, hi), x in zip(B2, t):
                rec("F7b following by race x tercile", fv, f"{lo}-{hi}", nm, x)
        for x, xl in (("white", "White (at mean ln parental income)"), ("lyp_c", "ln parental income (Black sons)"),
                      ("w_lyp", "White x ln parental income")):
            t = [safe(L(f"f7d_{fv}", fv, lo, hi, "P", x)) for lo, hi in B2]
            rws.append((xl, ["", ""] + [cell(z_) for z_ in t]))
            for (lo, hi), z_ in zip(B2, t):
                rec("F7b following, White x lyp", fv, f"{lo}-{hi}", x, z_)
        t = [safe([(K(f"f7d_{fv}", fv, lo, hi, "P", "lyp_c"), 1.0), (K(f"f7d_{fv}", fv, lo, hi, "P", "w_lyp"), 1.0)])
             for lo, hi in B2]
        rws.append(("ln parental income, White sons (sum)", ["", ""] + [cell(z_) for z_ in t]))
        rws.append(("N son-years / clusters", [f"{RES[K(f'f7c_{fv}', fv, lo, hi, 'P')]['n']:,} / "
                                               f"{RES[K(f'f7c_{fv}', fv, lo, hi, 'P')]['G']:,}"
                                               if K(f"f7c_{fv}", fv, lo, hi, "P") in RES else "" for lo, hi in B2] +
                    [f"{RES[K(f'f7d_{fv}', fv, lo, hi, 'P')]['n']:,} / {RES[K(f'f7d_{fv}', fv, lo, hi, 'P')]['G']:,}"
                     if K(f"f7d_{fv}", fv, lo, hi, "P") in RES else "" for lo, hi in B2]))
        panelsB.append((f"Outcome = son in the {lab}", rws))
    # observed vs random matching by race x tercile
    dd7 = d[v & d["lw"].notna()]
    obs = ["| Race | parental-income tercile | sons' ages | " + " | ".join(f"{lab}: observed | benchmark | ratio"
                                                                    for _, _, _, lab in F7) +
           " | son-years / sons (cell) |", "|---|---|---|" + "---|---|---|" * len(F7) + "---|"]
    for race in ("Black", "White"):
        for tq in (1, 2, 3):
            for lo, hi in B2:
                z = dd7[(dd7["race"] == race) & (dd7["terc"] == tq) & dd7["age"].between(lo, hi)]
                cs = []
                for fv, s_, f_, _ in F7:
                    zz = z[z[fv].notna()]
                    if len(zz) < (15 if fv == "f_hhc" else 30):
                        cs += ["", "", ""]
                        continue
                    o_ = zz[fv].mean()
                    bm = (z["kset"] == 1).mean() if fv == "f_hhc" else D32.bench(zz, s_, f_)
                    cs += [f"{o_:.3f}", f"{bm:.3f}", f"{o_ / bm:.2f}" if bm > 0 else ""]
                    CSV.append(dict(table="F7c following vs benchmark", sample=f"{race} T{tq}", outcome=fv,
                                    term=f"{lo}-{hi}", coef=o_, mean=bm, n=len(zz)))
                zc = z[z["f_cell"].notna()]
                obs.append(f"| {race} | {tq} | {lo}-{hi} | " + " | ".join(cs) +
                           f" | {len(zc):,} / {zc['pid'].nunique():,} |")
    s7 = d[v & d["f_cell"].notna()].drop_duplicates("pid")
    fsz = s7.groupby("fog").size()
    md += ["### F7. Are White sons, and sons of rich White parents, more likely to work in the father's cell?", "",
           "(a) Son-year linear probability models, Black + White sons pooled (weighted), Lee-Solon controls, clusters "
           "1968 family: following on a White indicator, without and with ln parental income. X = the father's cell, "
           "his occupation group, or his data-defined cell set (son's current cell in the same set as the father's). "
           f"Cell sizes: {s7['fog'].nunique()} distinct father cells among {len(s7):,} sons with a father's cell "
           f"(median {int(fsz.median())} sons per father cell, {int((fsz < 5).sum())} cells with < 5 sons). "
           "Coding drift: fathers are coded in 1970 codes, sons partly in 2000 / 2010 codes, so measured cell "
           "following is a lower bound and drift is larger after 2001 (when more sons are 35+). The 4-set measure is "
           "dominated by father and son both in 'neither' (most fathers of poorer sons), so its negative "
           "parental-income gradient is mechanical; the informative set measure is the last panel, 'son in a high-paid "
           "high-growth cell' among sons whose father was in one (benchmark in (c) = share of ALL sons of that race x "
           "tercile in such a cell; cells with < 15 son-years blank).", ""]
    md += table(hdrA, panels)
    md += ["(b) The 'rich White son' test: the same outcome on race x parental-income tercile cells (reference = Black "
           "sons in the bottom tercile; terciles pooled over Black and White sons), and on White, centred ln parental "
           "income and their interaction.", ""]
    md += table(hdrB, panelsB)
    md += ["(c) Observed share vs random matching within race x parental-income tercile (as 32 Table 4a, at the cell "
           "level): benchmark = sum_j p_son(j) p_father(j) in the cell; ratio = observed / benchmark. Unweighted; "
           "cells with < 30 son-years blank.", ""] + obs + [""]
    # F6 following into a high-paid high-growth cell
    d["k_hh"] = (d["kset"] == 1).astype(float).where(d["kset"].notna() & v)
    d["fa_hh"] = (d["fset"] == 1).astype(float).where(d["fset"].notna())
    d["fa_hl"] = (d["fset"] == 2).astype(float).where(d["fset"].notna())
    d["fa_hg"] = (d["fset"] == 3).astype(float).where(d["fset"].notna())
    run_cells("f6", d[v].copy(), ("k_hh",), ("fa_hh", "fa_hl", "fa_hg", "lyp"), ctrl_lsn, ("A", "C"),
              bands=[(25, 34), (35, 55)])
    panels = []
    for g, gname in GROUPS4:
        rws = []
        for lo, hi in ((25, 34), (35, 55)):
            for x, lab in (("fa_hh", "father in a high-paid high-growth cell"), ("fa_hl", "father in a high-paid-only "
                                                                                       "cell"),
                           ("fa_hg", "father in a high-growth-only cell"), ("lyp", "ln parental income")):
                t = safe(L("f6", "k_hh", lo, hi, g, x))
                rws.append((f"{lab}, sons {lo}-{hi}", [cell(t)]))
                rec("F6 son in HH cell", g, f"{lo}-{hi}", x, t)
            if g != "BW" and K("f6", "k_hh", lo, hi, g) in RES:
                k_ = K("f6", "k_hh", lo, hi, g)
                rws.append((f"Mean / N son-years, {lo}-{hi}", [f"{RES[k_]['mean']:.3f} / {RES[k_]['n']:,}"]))
        panels.append((gname, rws))
    s1_ = d.drop_duplicates("pid")
    nf = s1_.groupby("race")["fset"].apply(lambda x_: int((x_ == 1).sum()))
    md += ["### F6. Sons in a data-defined high-paid high-growth cell when the father was in one", "",
           "Son-year linear probability model: the son's CURRENT cell is high-paid AND high later growth (Section D) "
           "on indicators of the father's cell set (reference = father's cell in neither set) and ln parental income; "
           "Lee-Solon controls. Sons whose father's cell is high-paid and high-growth: Black "
           f"{int(nf.get('Black', 0)):,}, White {int(nf.get('White', 0)):,}.", ""]
    md += table(["(1) son in a high-paid high-growth cell"], panels)
    return OUTD, CON


# ================================================================ F8: returning to the father's line of work (within sons)
TYPEN = {"d": "already in the father's cell", "a": "same industry group, different occupation group",
         "b": "same occupation group, different industry group", "c": "different industry AND occupation"}


def type_of(s_og, f_og, base=100):
    so, si = np.floor(s_og / base), s_og % base
    fo, fi = np.floor(f_og / base), f_og % base
    t = np.where(s_og == f_og, "d", np.where(si == fi, "a", np.where(so == fo, "b", "c")))
    return np.where(np.isfinite(s_og) & np.isfinite(f_og), t, None)


def type_bench(z, scol, fcol, base=100):
    """random matching of sons' 25-34 cells to fathers' cells within the sample: P(type)."""
    ps = z[scol].value_counts(normalize=True)
    pf = z[fcol].value_counts(normalize=True)
    S_, F_ = np.meshgrid(ps.index.to_numpy(float), pf.index.to_numpy(float), indexing="ij")
    W_ = np.outer(ps.to_numpy(), pf.to_numpy())
    T_ = type_of(S_.ravel(), F_.ravel(), base).reshape(S_.shape)
    return {k: float(W_[T_ == k].sum()) for k in "abcd"}


def sec_f8(d, md):
    v = d["valid"] & d["lw"].notna()
    out_md = ["### F8. Do sons return to the father's line of work after first trying other jobs? (within sons)", ""]
    for level, sc_, fc_, lab, base in (("cell", "og", "fog", "occupation group x industry group cell", 100),
                                 ("fine", "fine", "ffine", "fine cell occ1990dd x ind1990ddx", 1000)):
        dd = d[v].copy()
        if level == "fine":
            dd["fine"] = dd["dd"] * 1000 + dd["ddx"]
            dd["ffine"] = dd["fdd"] * 1000 + dd["fddx"]
        dd = dd[dd[sc_].notna() & dd[fc_].notna()]
        e = dd[dd["age"].between(25, 34)]
        l_ = dd[dd["age"].between(35, 55)]
        g0, g1 = e.groupby("pid"), l_.groupby("pid")
        P = pd.DataFrame({"m25": g0[sc_].agg(mode), "m35": g1[sc_].agg(mode)})
        first = dd.drop_duplicates("pid").set_index("pid")
        for c_ in ("race", "terc", "lyp", "fam68", "birth_year", fc_):
            P[c_] = first[c_].reindex(P.index)
        P["wpool"] = dd.groupby("pid")["wpool"].mean().reindex(P.index)
        P["n25"] = g0.size()
        P["ncell25"] = g0[sc_].nunique()
        P["share_in25"] = (e[sc_] == e[fc_]).groupby(e["pid"]).mean()
        mv = e[e["stay"].notna()]
        P["moves25"] = (mv["stay"] == 0).groupby(mv["pid"]).sum().reindex(P.index)
        P["nmv25"] = mv.groupby("pid").size().reindex(P.index)
        for k in "abcd":
            tt = pd.Series(type_of(e[sc_].to_numpy(float), e[fc_].to_numpy(float), base), index=e.index)
            P[f"sh_{k}"] = (tt == k).groupby(e["pid"]).mean()
        n_all = dd["pid"].nunique()
        P = P.dropna(subset=["m25", "m35"])
        P["pid"] = P.index
        P["in25"] = (P["m25"] == P[fc_]).astype(float)
        P["in35"] = (P["m35"] == P[fc_]).astype(float)
        P["type25"] = type_of(P["m25"].to_numpy(float), P[fc_].to_numpy(float), base)
        P["enter"] = P["in35"].where(P["in25"] == 0)
        P["leave"] = (1 - P["in35"]).where(P["in25"] == 1)
        P["t_a"], P["t_b"] = (P["type25"] == "a").astype(float), (P["type25"] == "b").astype(float)
        P["t_d"] = (P["type25"] == "d").astype(float)
        P["coh"] = (P["birth_year"] - 1960) / 10
        P["lyp_c"] = P["lyp"] - P["lyp"].mean()
        P["entrant"] = ((P["in25"] == 0) & (P["in35"] == 1)).astype(float)
        P["stayin"] = ((P["in25"] == 1) & (P["in35"] == 1)).astype(float)
        P["mvrate"] = P["moves25"] / P["nmv25"]
        P = P.reset_index(drop=True)
        tagp = f"f8{level}"

        def ctrl(z):
            return np.column_stack([np.ones(len(z)), z["coh"].to_numpy(float), z["coh"].to_numpy(float) ** 2])
        # (1) transitions by race x tercile
        tr = ["| Race | parental-income tercile | sons in both windows | out -> out | out -> IN (enter) | IN -> IN | IN "
              "-> out (leave) | share entering among those out at 25-34 |", "|---|---|---|---|---|---|---|---|"]
        for race in ("Black + White", "Black", "White"):
            for tq in (None, 1, 2, 3):
                z = P if race == "Black + White" else P[P["race"] == race]
                z = z if tq is None else z[z["terc"] == tq]
                if len(z) < 10:
                    continue
                c00 = ((z["in25"] == 0) & (z["in35"] == 0)).mean()
                c01 = ((z["in25"] == 0) & (z["in35"] == 1)).mean()
                c11 = ((z["in25"] == 1) & (z["in35"] == 1)).mean()
                c10 = ((z["in25"] == 1) & (z["in35"] == 0)).mean()
                tr.append(f"| {race} | {'all' if tq is None else tq} | {len(z):,} | {c00:.3f} | {c01:.3f} | {c11:.3f} | "
                          f"{c10:.3f} | {z['enter'].mean():.3f} |")
        # (2) entering / leaving on parental income; entering on the 25-34 type
        specs = [("enter", ("lyp",), "(1) enters the father's cell (out at 25-34, in at 35-55)"),
                 ("leave", ("lyp",), "(2) leaves (in at 25-34, out at 35-55)"),
                 ("in35", ("lyp",), "(3) in the father's cell at 35-55 (all sons)"),
                 ("enter", ("t_a", "t_b", "lyp"), "(4) enters, on the 25-34 type (ref. different industry and "
                                                  "occupation)"),
                 ("in35", ("t_a", "t_b", "t_d", "lyp"), "(5) in the father's cell at 35-55, on the 25-34 type")]
        infos = [fitc(f"{tagp}_{k}", P, y, xs, ctrl, minn=50) for k, (y, xs, _) in enumerate(specs)]
        labs = [("lyp", "ln parental income"), ("t_a", "25-34: same industry group, different occupation"),
                ("t_b", "25-34: same occupation group, different industry"), ("t_d", "25-34: already in the cell")]
        panels = []
        for g, gname in GROUPS4:
            rws = []
            for x, xl in labs:
                cs = []
                for k, (y, xs, h) in enumerate(specs):
                    t = co(f"{tagp}_{k}", y, g, x) if x in xs else NAN3
                    cs.append(cell(t))
                    if np.isfinite(t[0]):
                        rec(f"F8 within-son following ({level})", g, h, x, t)
                rws.append((xl, cs))
            if g != "BW":
                rws.append(("Mean of outcome", [f"{i[g][3]:.3f}" if g in i else "" for i in infos]))
                rws.append(("N sons / clusters", [nfo(i, g) for i in infos]))
            panels.append((gname, rws))
        # (3) churning at 25-34
        ch = ["| Race | group of sons | sons | distinct cells at 25-34 | employer changes per observed interview at "
              "25-34 | 25-34 son-years |", "|---|---|---|---|---|---|"]
        for race in ("Black + White", "Black", "White"):
            z = P if race == "Black + White" else P[P["race"] == race]
            for nm, mk in (("entrants (out at 25-34, in at 35-55)", z["entrant"] == 1),
                           ("stayers (in at both)", z["stayin"] == 1),
                           ("never in the father's cell", (z["in25"] == 0) & (z["in35"] == 0))):
                zz = z[mk]
                ch.append(f"| {race} | {nm} | {len(zz):,} | {zz['ncell25'].mean():.2f} | {zz['mvrate'].mean():.3f} | "
                          f"{zz['n25'].mean():.1f} |")
        P["never"] = ((P["in25"] == 0) & (P["in35"] == 0)).astype(float)
        P["n25s"] = P["n25"] / 10
        chs = [("ncell25", ("entrant", "stayin", "n25s", "lyp"), "(1) distinct cells at 25-34"),
               ("mvrate", ("entrant", "stayin", "n25s", "lyp"), "(2) employer changes per interview at 25-34")]
        cinf = [fitc(f"{tagp}_ch{k}", P, y, xs, ctrl, minn=50) for k, (y, xs, _) in enumerate(chs)]
        cpan = []
        for g, gname in GROUPS4:
            rws = []
            for x, xl in (("entrant", "entrant (ref. never in the father's cell)"), ("stayin", "stayer"),
                          ("n25s", "25-34 son-years / 10"), ("lyp", "ln parental income")):
                t = [co(f"{tagp}_ch{k}", y, g, x) for k, (y, _, _) in enumerate(chs)]
                rws.append((xl, [cell(z_) for z_ in t]))
                for (y, _, h), z_ in zip(chs, t):
                    rec(f"F8 churning ({level})", g, h, x, z_)
            if g != "BW":
                rws.append(("N sons / clusters", [nfo(i, g) for i in cinf]))
            cpan.append((gname, rws))
        # PI: where were eventual entrants at 25-34? distribution of types + random-matching benchmark
        ty = ["| Race / parental-income tercile | sons | " + " | ".join(f"{TYPEN[k]}: observed | benchmark" for k in "abcd")
              + " | entrants (in at 35-55, not modal at 25-34): " + " | ".join(f"type {k}" for k in "abc") +
              " | entrants: mean share of 25-34 son-years in a / b / c / d |",
              "|---|---|" + "---|---|" * 4 + "---|" * 4 + "---|"]
        groups_ = [("Black + White, all", P)] + [(f"{r_}, tercile {t_}", P[(P["race"] == r_) & (P["terc"] == t_)])
                                                  for r_ in ("Black", "White") for t_ in (1, 2, 3)] + \
            [("Black, all", P[P["race"] == "Black"]), ("White, all", P[P["race"] == "White"])]
        for nm, z in groups_:
            if len(z) < 10:
                continue
            bm = type_bench(z, "m25", fc_, base)
            en = z[z["entrant"] == 1]
            obs = [(z["type25"] == k).mean() for k in "abcd"]
            ent = [(en["type25"] == k).mean() if len(en) else np.nan for k in "abc"]
            shs = " / ".join(f"{en[f'sh_{k}'].mean():.2f}" for k in "abcd") if len(en) else ""
            ty.append(f"| {nm}{' (rich White)' if nm == 'White, tercile 3' else ''} | {len(z):,} | " +
                      " | ".join(f"{o_:.3f} | {bm[k]:.3f}" for o_, k in zip(obs, "abcd")) + f" | {len(en):,}: " +
                      " | ".join(f"{x_:.2f}" for x_ in ent) + f" | {shs} |")
            for k, o_ in zip("abcd", obs):
                CSV.append(dict(table=f"F8 25-34 type ({level})", sample=nm, outcome=k, coef=o_, mean=bm[k], n=len(z)))
        # (4) son FE: in father's cell on ln parental income x age, within sons
        zf = dd.copy()
        zf["fol"] = (zf[sc_] == zf[fc_]).astype(float)
        zf["lyp_c"] = zf["lyp"] - P["lyp"].mean()
        zf["a_lyp"] = zf["lyp_c"] * (zf["age"] - 40) / 10
        zf["p35"] = (zf["age"] >= 35).astype(float)
        zf["p35_lyp"] = zf["lyp_c"] * zf["p35"]
        both = set(P["pid"])
        fe_specs = [("all", zf, ("a_lyp",), "(1) all sons with a father's cell: ln parental income x (age-40)/10"),
                    ("all", zf, ("p35_lyp",), "(2) ... ln parental income x age >= 35"),
                    ("both", zf[zf["pid"].isin(both)], ("a_lyp",), "(3) sons observed in both windows: x (age-40)/10"),
                    ("both", zf[zf["pid"].isin(both)], ("p35_lyp",), "(4) ... x age >= 35")]
        finf = [fit_fe(f"{tagp}_fe{k}", z_, "fol", xs, common=("p35",)) for k, (_, z_, xs, _) in enumerate(fe_specs)]
        fpan = []
        for g, gname in GROUPS4:
            cs = []
            for k, (_, _, xs, h) in enumerate(fe_specs):
                t = co(f"{tagp}_fe{k}", "fol", g, xs[0])
                cs.append(cell(t))
                rec(f"F8 son FE ({level})", g, h, xs[0], t)
            rws = [("ln parental income x age term (within son)", cs)]
            if g != "BW":
                rws.append(("Person FE, year FE, common after-35 shift; N son-years / sons / clusters",
                            [f"{i[g][0]:,} / {i[g][1]:,} / {i[g][2]:,}" if g in i else "" for i in finf]))
            fpan.append((gname, rws))
        ncell_f = dd[fc_].nunique()
        out_md += [f"#### F8 {'(i)' if level == 'cell' else '(ii)'}. Level: {lab}", "",
                   f"Sons with a father's code and valid son-years: {n_all:,}; observed with a code in BOTH 25-34 and "
                   f"35-55: {len(P):,} ({len(P) / max(n_all, 1):.0%} kept). In / out = the son's modal {lab} in the "
                   f"window equals the father's modal one. Distinct father codes: {ncell_f:,}"
                   + (" (fine cells are sparse: the father's fine cell combines his modal occ1990dd and his modal "
                      "ind1990ddx, which need not come from the same waves; matches at this level are rare and coding "
                      "drift between 1970 and 2000 / 2010 codes is largest)." if level == "fine" else
                      ". Coding drift: fathers are coded in 1970 codes, sons after 2001 in 2000 / 2010 codes, and the "
                      "35-55 window falls more often after 2001, which biases measured ENTRY down and LEAVING up."), "",
                   "(1) Transitions between 25-34 and 35-55 (shares of sons):", ""] + tr + \
                  ["", "(2) Son-level linear probability models (outcome in the column header; controls birth-year "
                   "quadratic; pooled weighted, by race unweighted; clusters 1968 family). Columns (4)-(5): does "
                   "being in the father's industry (type a) or occupation (type b) at 25-34 predict ending up in his "
                   "exact cell after 35?", ""] + table([h for _, _, h in specs], panels) + \
                  ["(3) Churning at 25-34: distinct cells and employer changes (tenure resets: the son was not with "
                   "the previous interview's employer; observed from 1985) at 25-34, by eventual group:", ""] + ch + \
                  [""] + table([h for _, _, h in chs], cpan) + \
                  ["(PI) Where were sons at 25-34 relative to the father's cell? Modal 25-34 type for ALL sons in both "
                   "windows (observed vs random matching of sons' 25-34 cells to fathers' cells within the row), and "
                   "for the eventual entrants (in the father's cell at 35-55 but not modal at 25-34):", ""] + ty + \
                  ["", "(4) Within sons: son-year linear probability model of being in the father's cell on ln "
                   "parental income x age with person FE (the age gradient is identified within sons, not across "
                   "cohorts), year FE and a common after-35 shift. Positive = sons of richer parents move INTO the "
                   "father's cell as they age.", ""] + table([h for _, _, _, h in fe_specs], fpan)
    md += out_md


# ================================================================ figure
def figure(MF, d):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ink, muted, grid, bg = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    col = {1: "#2a78d6", 2: "#eb6834", 3: "#1baf7a", 0: "#52514e"}
    fig, ax = plt.subplots(1, 4, figsize=(22, 5.4), gridspec_kw=dict(width_ratios=[1, 1, 1.15, 1.15]))
    fig.patch.set_facecolor(bg)
    T = MF["sets"]["T"]
    x = np.arange(8)
    for k in (1, 2, 3, 0):
        z = T[T["set"] == k]
        v = np.array([np.average(z[c], weights=z["w"]) for c in QC])
        ax[0].plot(x, v - v[0], "o-", color=col[k], lw=2, ms=7, mec=bg, mew=1.5, label=SETN[k])
    ax[0].set_xticks(x, B5, fontsize=8, rotation=45)
    ax[0].set_title("(a) CPS MORG: wage relative to men of the same age,\ndata-defined cell sets (25-29 = 0)",
                    loc="left", fontsize=10.5, color=ink)
    ax[0].set_ylabel("log points", color=muted)
    ax[0].legend(frameon=False, fontsize=9, loc="upper left")
    z = d[d["valid"] & d["lw"].notna() & d["eset"].notna()].copy()
    z["lw0"] = z["pid"].map(z[z["age"].between(25, 34)].groupby("pid")["lw"].mean())
    z["bin"] = np.minimum((z["age"] - 25) // 5, 5)
    for k in (1, 2, 3, 0):
        zz = z[z["eset"] == k]
        mm = zz.groupby("bin").apply(lambda q: (q["lw"] - q["lw0"]).mean())
        nn = zz.groupby("bin")["pid"].nunique()
        mm = mm[nn >= 25]
        ax[1].plot(mm.index, mm.values, "o-", color=col[k], lw=2, ms=7, mec=bg, mew=1.5, label=SETN[k])
    ax[1].set_xticks(range(6), ["25-29", "30-34", "35-39", "40-44", "45-49", "50-55"], fontsize=8)
    ax[1].set_title("(b) PSID sons: ln wage minus own 25-34 mean,\nby cell set at 25-34 (raw, real wages)",
                    loc="left", fontsize=10.5, color=ink)
    ax[1].legend(frameon=False, fontsize=9, loc="upper left")
    items = [("k_lin_p", "current industry, linear B"), ("k_q_p", "current industry, nonlinear"),
             ("e_q_p", "industry at 25-34, nonlinear"), ("ko_p", "current occupation group, nonlinear"),
             ("ck_p", "current cell, nonlinear"), ("ck_ind", "cell minus occupation (industry adds)"),
             ("ce_p", "cell at 25-34, nonlinear"), ("ce_ind", "cell at 25-34 minus occupation")]
    for a_, g, ttl in ((ax[2], "P", "(c) Share of the pooled rise (25-34 -> 35-55)\ncarried by each profile (PSID)"),
                       (ax[3], "BW", "(d) Share of the change of the\nBlack-White gap carried by each profile")):
        b, s = [], []
        for y, _ in items:
            t = sratio(Dch("hC", y, g), Dch("hC", "lwv", g))
            b.append(t[0])
            s.append(t[1])
        yy = np.arange(len(items))[::-1]
        a_.errorbar(b, yy, xerr=1.96 * np.array(s), fmt="o", color="#2a78d6", ms=8, elinewidth=1.5, mec=bg, mew=1.5)
        a_.set_yticks(yy, [lab for _, lab in items], fontsize=8.5)
        a_.axvline(0, color=muted, lw=1)
        a_.set_title(ttl, loc="left", fontsize=10.5, color=ink)
        a_.set_xlabel("share (95% CI)", color=muted)
        a_.grid(axis="x", color=grid, lw=0.8)
    for a_ in ax:
        a_.set_facecolor(bg)
        a_.set_axisbelow(True)
        for sp in ("top", "right"):
            a_.spines[sp].set_visible(False)
        a_.spines["bottom"].set_color(muted)
        a_.spines["left"].set_color(grid)
        a_.tick_params(colors=muted, length=0)
    for a_ in ax[:2]:
        a_.grid(axis="y", color=grid, lw=0.8)
        a_.set_xlabel("Son's age band", color=muted)
    fig.tight_layout()
    fig.savefig(OUT / "early_industry_late_payoff.png", dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)

# ================================================================ summary
def hsh(tg, y, g, b=(35, 55)):
    return cell(sratio(Dch(tg, y, g, b=b), Dch(tg, "lwv", g, b=b))) or "n.a. (denominator ~ 0)"


def summary(MF, nk, CON):
    def gch(tag, name, g, b=(35, 55)):
        return sc(con_change(tag, name, g, b))

    def gsh(tag, name, g):
        return cell(sratio(con_change(tag, name, g), Dch(f"{tag}s_{name}", "lw", g))) or "n.a. (denominator ~ 0)"

    def sh(tag, name, g):
        return sc(Dch(f"{tag}s_{name}", "lw", g))

    def g2(tag, name):
        return (f"{gch(tag, name, 'P')} (share {gsh(tag, name, 'P')}) pooled, {gch(tag, name, 'BW')} (share "
                f"{gsh(tag, name, 'BW')}) of the B-W change")
    sd = MF["sd"]
    st = MF["sets"]
    T = st["T"]
    shares = T.groupby("set")["w"].sum()
    out = ["## Summary", ""]
    out.append(f"- **Sample.** {nk['psid']}")
    out.append("- **H. Headline, nonlinear profiles (PSID).** 32's sample: pooled rise of the coefficient "
               f"{sc(Dch('h32', 'lwv', 'P'))}; share carried by the current industry's LINEAR slope B x t "
               f"{hsh('h32', 'k_lin_p', 'P')} vs its NONLINEAR band profile {hsh('h32', 'k_q_p', 'P')} (piecewise "
               f"30/35/45: {hsh('h32', 'k_s_p', 'P')}). Change of the Black-White gap {sc(Dch('h32', 'lwv', 'BW'))}: "
               f"linear {hsh('h32', 'k_lin_p', 'BW')}, nonlinear {hsh('h32', 'k_q_p', 'BW')}, piecewise "
               f"{hsh('h32', 'k_s_p', 'BW')}. Common sample (pooled rise {sc(Dch('hC', 'lwv', 'P'))}; B-W change "
               f"{sc(Dch('hC', 'lwv', 'BW'))}), shares pooled / B-W: industry at 25-34, nonlinear profile "
               f"{hsh('hC', 'e_q_p', 'P')} / {hsh('hC', 'e_q_p', 'BW')}; occupation x industry CELL profile, current "
               f"{hsh('hC', 'ck_p', 'P')} / {hsh('hC', 'ck_p', 'BW')}, at 25-34 {hsh('hC', 'ce_p', 'P')} / "
               f"{hsh('hC', 'ce_p', 'BW')}; of which occupation-group profile alone (current) {hsh('hC', 'ko_p', 'P')} / "
               f"{hsh('hC', 'ko_p', 'BW')} and what industry adds within the cell (current / at 25-34) "
               f"{hsh('hC', 'ck_ind', 'P')} / {hsh('hC', 'ck_ind', 'BW')} and {hsh('hC', 'ce_ind', 'P')} / "
               f"{hsh('hC', 'ce_ind', 'BW')}; current cell level + profile {hsh('hC', 'ck_t', 'P')} / "
               f"{hsh('hC', 'ck_t', 'BW')}.")
    out.append("- **B. What the linear B misses (CPS MORG; s.d. across men of growth 37->52).** Linear 1.5 B "
               f"{sd['lin35']['fine']:.3f}; band growth (35-39)->(50-54) {sd['G35']['fine']:.3f} (fine industries), "
               f"{sd['G35']['cell']:.3f} (cells); correlation with linear growth {sd['G35']['corr']:.3f}, i.e. the linear "
               f"B misses {1 - sd['G35']['corr'] ** 2:.0%} of the cross-industry variance of growth after 35; cells' "
               f"later growth correlates {sd['cell_corr']:.3f} with their industry's linear growth.")
    out.append("- **D. Data-defined groups (cells ranked by MORG level and band growth after 35; top quartiles of men's "
               f"employment).** Employment shares: high-paid AND high later growth {shares.get(1, 0):.3f}, high-paid "
               f"only {shares.get(2, 0):.3f}, high later growth only {shares.get(3, 0):.3f}. The high-paid high-growth "
               "set is mostly professional-specialty and managerial occupations in education, public administration, "
               "professional services, hospitals and manufacturing; managers in finance, managers in professional "
               "services, professionals in legal services and sales in finance / insurance are high-paid but their "
               "relative wages FALL after 35 ('high-paid only'). Share of sons in the high-paid high-growth set at "
               f"25-34: {nk['hh']}.")
    out.append("- **A. Growth after 35 by the early set (PSID, pooled).** Delta ln wage (40-55)-(25-34) relative to "
               f"cells in neither set: high-paid high-growth {cell(co('gr0', 'd40', 'P', 'e_hh'))}, high-paid only "
               f"{cell(co('gr0', 'd40', 'P', 'e_hlo'))}, high later growth only {cell(co('gr0', 'd40', 'P', 'e_hgo'))}. "
               "Within person (person + year FE), high-paid high-growth vs neither: slope 25-35 "
               f"{cell(coL('pfeP0', 'lw', 'P', [('s1_hh', 1.0)]))}, slope 35-55 "
               f"{cell(coL('pfeP0', 'lw', 'P', [('s2_hh', 1.0)]))} per 10 years; high-paid only: "
               f"{cell(coL('pfeP0', 'lw', 'P', [('s1_hlo', 1.0)]))} / {cell(coL('pfeP0', 'lw', 'P', [('s2_hlo', 1.0)]))}. "
               "Illustrative pre-chosen industries (finance / insurance / legal / professional): Delta "
               f"{cell(co('gr5', 'd40', 'P', 'e_flp'))}; slopes {cell(coL('pfeP2', 'lw', 'P', [('s1_flp', 1.0)]))} / "
               f"{cell(coL('pfeP2', 'lw', 'P', [('s2_flp', 1.0)]))}.")
    out.append("- **A. Gelbach, early FE x band (PSID, any profile).** Pooled rise on the early sample "
               f"{sh('gE', 'grp', 'P')}, B-W change {sh('gE', 'grp', 'BW')}. Accounted for by: early data-defined cell "
               f"set {g2('gE', 'cset')}; early data-defined industry set {g2('gE', 'iset')}; early industry group (33) "
               f"{g2('gE', 'grp')}; early fine industry {g2('gE', 'ddx')}; early occupation group (11) "
               f"{g2('gE', 'o11')}; occupation group + industry group {g2('gE', 'o11+grp')}; early cell 11 x 33 "
               f"{g2('gE', 'og')}; early occupation (occ1990dd) {g2('gE', 'occ')}; illustrative FLP indicator "
               f"{g2('gE', 'flp')}. Permuted-cell placebos: mean share {nk['pl']}.")
    out.append("- **C. Fast track inside the high-paid high-growth cells.** Delta (40-55)-(25-34), pooled: parental-"
               f"income gradient inside {cell(coL('het0', 'd40', 'P', [('lyp_c', 1.0), ('e_hh_lyp', 1.0)]))} vs "
               f"outside {cell(co('het0', 'd40', 'P', 'lyp_c'))} (difference {cell(co('het0', 'd40', 'P', 'e_hh_lyp'))}). "
               "Person FE: extra gradient of the slope after 35 inside "
               f"{cell(co('hetfe', 'lw', 'P', 's2_hh_lyp'))}, of the slope before 35 "
               f"{cell(co('hetfe', 'lw', 'P', 's1_hh_lyp'))}; White {cell(co('hetfe', 'lw', 'W', 's2_hh_lyp'))} / "
               f"{cell(co('hetfe', 'lw', 'W', 's1_hh_lyp'))}, Black {cell(co('hetfe', 'lw', 'B', 's2_hh_lyp'))} / "
               f"{cell(co('hetfe', 'lw', 'B', 's1_hh_lyp'))}.")
    c_ = CON
    out.append("- **F. Following the father's cell.** Accounted for in the pooled rise: cell "
               f"{cell(c_['f_cell']['p'])} (share {cell(c_['f_cell']['psh']) or 'n.a.'}); in the change of the B-W gap: "
               f"{cell(c_['f_cell']['bw'])} of {cell(c_['f_cell']['bwtot'])} (share {cell(c_['f_cell']['bwsh']) or 'n.a.'}); "
               f"industry-group following {cell(c_['f_ind']['bw'])}, occupation-group following "
               f"{cell(c_['f_occ']['bw'])}. Pay-off of cell following (education and the cell's profile held fixed): ln "
               f"wage 35-55 {sc(L('pay_f_cell_lw', 'lw', 35, 55, 'P', 'fol'))}; annual growth 35-55 "
               f"{sc(L('pay_f_cell_g30', 'g30', 35, 55, 'P', 'fol'))}; tenure x following "
               f"{cell(co('ten_f_cell', 'lw', 'P', 'ten_f'))}. Son in a high-paid high-growth cell when the father was "
               f"(sons 35-55): pooled {sc(L('f6', 'k_hh', 35, 55, 'P', 'fa_hh'))}, White "
               f"{sc(L('f6', 'k_hh', 35, 55, 'W', 'fa_hh'))}, Black {sc(L('f6', 'k_hh', 35, 55, 'B', 'fa_hh'))}.")
    out.append("- **E. NLSY79.** Pooled rise (35-55)-(25-34) " + sc(Dch('hN32', 'lwv', 'P')) +
               f": linear industry slope share {hsh('hN32', 'k_lin_p', 'P')}, nonlinear {hsh('hN32', 'k_q_p', 'P')}; "
               f"cell profile at 25-34 {hsh('hNC', 'ce_p', 'P')}. Gelbach: early cell set {g2('gN', 'cset')}; early "
               f"industry set {g2('gN', 'iset')}; early occupation group {g2('gN', 'o11')}. Delta (40-55)-(25-34), "
               f"high-paid high-growth vs neither {cell(co('Ngr0', 'd40', 'P', 'e_hh'))}.")
    return "\n".join(out)


ASSESS = (
    "**Assessment (answer to the PI's question).** Allowing the career payoff to be nonlinear, fixed at 25-34 and "
    "specific to occupation x industry cells raises the measured role of early sorting, but what carries the post-35 "
    "divergence is the son's early OCCUPATIONAL position (managerial / professional), not his industry and not a "
    "late take-off of cells that pay off after 35. (i) Nonlinear industry profiles (headline H): replacing 32's linear "
    "B by the industry's full age-band profile raises the share of the pooled post-35 rise of wage persistence carried "
    "by the industry's career profile from 0.084*** to 0.118*** (piecewise 30/35/45: 0.117***) and of the change of the "
    "Black-White gap from 0.050*** to 0.074***; fixing the industry at 25-34 gives 0.132*** / 0.086***. The linear B "
    "misses about half of the cross-industry variance of growth after 35 (correlation 0.70 across men), yet industry "
    "remains a second-order channel (about 12-13% of the pooled rise, 7-9% of the Black-White change). (ii) "
    "Data-defined groups (Section D): ranking all occupation x industry cells by their MORG level and band growth after "
    "35, the 'high-paid AND high later growth' set (16% of men's employment) is mostly professional-specialty and "
    "managerial jobs in education, public administration, professional services, hospitals and manufacturing. The PI's "
    "examples mostly fall elsewhere: of men in finance / insurance / legal / professional industries, 56% are in "
    "high-paid cells whose wages relative to men of the same age FALL after 35 (managers in finance and in professional "
    "services, professionals in legal services, sales in finance / insurance) and 23% in high-paid high-growth cells. "
    "(iii) Sons who start in high-paid cells grow faster afterwards (Delta (40-55)-(25-34) 0.223*** for high-paid "
    "high-growth, 0.203*** for high-paid only, 0.097*** for high later growth only), but within person the extra "
    "growth is concentrated before 35 (slope 25-35 +0.33*** / +0.39*** per 10 years) with at most a small premium "
    "after 35 (+0.059** / +0.012). Because the 25-34 band averages over that early climb, growth in the early 30s "
    "itself raises the 35-55 vs 25-34 contrast; a payoff that starts only after 35 is not what the data show, in MORG "
    "cross-sections or in PSID panels. (iv) Gelbach with early x band fixed effects (any profile, estimated in the "
    "PSID): the data-defined early cell set accounts for 0.271*** of the pooled rise and 0.237*** of the change of the "
    "Black-White gap; the same ranking applied to industries accounts for 0.034 / 0.006 (not significant); the early "
    "occupation group alone 0.377*** / 0.318***, and adding the early industry group changes little (0.376*** / "
    "0.352***); the fine early occupation 0.591*** / 0.713***. Permuted-cell placebos give about 0.03, so these are "
    "not over-fitting artefacts, but early-occupation fixed effects also proxy the son's own skills at 25-34: this "
    "reads as 'where a son stands at 25-34 predicts how far his wage pulls away later', not as a causal payoff to the "
    "occupation. (v) Fast track within the high-paid high-growth cells: the parental-income gradient of growth "
    "from 25-34 to 40-55 is 0.146** inside vs 0.043 outside (difference 0.103, p=0.11, imprecise); within person the "
    "extra gradient is in the slope before 35 (0.179**) and not after 35 (0.012, p=0.81). (vi) Access: sons of "
    "richer and White parents are far more often in high-paid cells at 25-34 (high-paid high-growth: top tercile "
    "0.202 vs bottom 0.047; White 0.161 vs Black 0.057). Following the father's exact cell is about 3-4 times as common "
    "as random matching and a father in a high-paid high-growth cell raises the son's chance of being in one (0.090*** at "
    "35-55), but cell following carries no wage-level or growth pay-off once education and the cell's profile are "
    "held fixed and accounts for none of the divergence. (vii) NLSY79: the same pattern (early cell set 0.361*** of "
    "the pooled rise, industry set 0.040, occupation group 0.454***), with a small and imprecise Black-White "
    "divergence. Bottom line for the companion model: early sorting matters, but it is sorting into managerial / "
    "professional positions (human capital level at 25-34 and its accumulation in the early 30s), with industry adding "
    "little; the illustrative pre-chosen industries (finance / insurance / legal / professional) show the same "
    "front-loaded profile (illustrative Gelbach share 0.097** pooled, 0.085* of the gap). Caveats: descriptive "
    "accounting; MORG profiles are 1992-2002 cross-sections (synthetic-cohort slopes are noisy and barely correlated "
    "with them; PSID within-person group slopes after 35 do not line up with MORG band growth); 'high later growth' "
    "is a top-quartile cut of a measure that is near zero for most cells (threshold -0.015); of sons observed at "
    "35-55, 93% have an early industry, while sons never observed after 34 are mostly recent cohorts with slightly "
    "lower 25-34 wages (2.45 vs 2.56); codes are bridged across 1970 / 2000 / 2010 classifications.")


# ================================================================ main
def main():
    global STEEP32, MF_G
    OUT.mkdir(exist_ok=True)
    W = D32.ind_crosswalks()
    XWD = D27.crosswalks()
    M = D32.morg_measures(D32.morg_micro(W, XWD))
    STEEP32 = set(M["steep"])
    print("MORG nonlinear profiles ...", flush=True)
    MF = morg_flex(M)
    data_sets(MF)
    MF_G = MF
    r = D32.son_panel(W, M)
    fathers = r.attrs["fathers"]
    J = D32.nlsy_panel(W, M, XWD, D27.SCORES)
    D27.CLIDX = pd.Index(np.unique(np.concatenate([r["fam68"].dropna().unique().astype(float),
                                                   J["fam68"].dropna().unique().astype(float) + 1e7])))
    J["fam68"] = J["fam68"].astype(float) + 1e7
    r["fam68"] = r["fam68"].astype(float)
    D27.NCL = len(D27.CLIDX)
    d = prep(r, MF, W, r.attrs["rc"])
    J["valid"] = True
    J["year"] = J["round"]
    rcN = D32.recode2000(W, np.concatenate([J.loc[J["isch"] == "2000", "icode"].dropna().to_numpy(),
                                            D32.code2000(J.loc[J["isch"] == "2012", "icode"].dropna().to_numpy())]))
    j = prep(J, MF, W, rcN)
    S = son_frame(d)
    S["terc"] = S["pid"].map(d.drop_duplicates("pid").set_index("pid")["terc"])
    SN = son_frame(j)
    q = SN["lyp"].quantile([1 / 3, 2 / 3]).to_numpy()
    SN["terc"] = np.where(SN["lyp"] <= q[0], 1, np.where(SN["lyp"] <= q[1], 2, 3)).astype(float)

    md = ["# Early industry, late payoff: nonlinear industry and occupation x industry cell profiles, and wage "
          "persistence after 35", "",
          "Built by `35.EarlyIndustryLatePayoff.py` (2026-10-17); definitions in its docstring. PSID SRC + SEO sons "
          "(32's panel), CPS MORG 1992-2002 men, NLSY79 men. Every coefficient: estimate (s.e.; p), *** p<0.01, ** "
          "p<0.05, * p<0.1; s.e. clustered by 1968 family (PSID) / 1979 household (NLSY79); pooled = Black + White "
          "weighted, by race unweighted. **Descriptive accounting: sons select into industries, occupations and cells; "
          "nothing here is a causal effect of parental income, race, industry or the father's cell.**", "",
          "SUMMARY_PLACEHOLDER", "", ASSESS, ""]
    md += ["## 0. Samples", ""]
    sec_sample(d, S, md, "PSID")
    sv = d[d["valid"] & d["lw"].notna()]
    late = sv[sv["age"].between(35, 55)]
    nl = late.loc[late["egrp"].notna(), "pid"].nunique()
    own_k = d.loc[d["dec"], "ck_own"].mean()
    own_e = d.loc[d["dec"] & d["eog"].notna(), "ce_own"].mean()
    nk = {"psid": f"PSID: {S['egrp'].notna().sum():,} sons have an industry at 25-34; of the "
                  f"{late['pid'].nunique():,} sons observed at 35-55, {nl:,} ({nl / late['pid'].nunique():.0%}) have one "
                  f"({late['egrp'].notna().mean():.0%} of 35-55 son-years); see Table 0P for their 25-34 "
                  f"characteristics. Son-years in cells with their own MORG profile: current {own_k:.0%}, early "
                  f"{own_e:.0%} (rest: additive occupation + industry fallback)."}
    hs = S[S["eset"].notna()]
    nk["hh"] = (f"all {(hs['eset'] == 1).mean():.3f}; bottom / top parental-income tercile "
                f"{(hs.loc[hs['terc'] == 1, 'eset'] == 1).mean():.3f} / {(hs.loc[hs['terc'] == 3, 'eset'] == 1).mean():.3f}; "
                f"Black {(hs.loc[hs['race'] == 'Black', 'eset'] == 1).mean():.3f}, White "
                f"{(hs.loc[hs['race'] == 'White', 'eset'] == 1).mean():.3f}")
    print("H headline ...", flush=True)
    sec_headline(d, md, "PSID", d["dec"] & d["k_q_t"].notna() & d["ck_t"].notna())
    print("B ...", flush=True)
    sec_morg(MF, md, S)
    sec_psid_groups(d, S, MF, md)
    print("A ...", flush=True)
    md += ["## A. Is wage growth after 35 faster for sons who were in finance / law / professional services at 25-34?",
           ""]
    sec_growth(S, md, "PSID")
    sec_panel(d, md, "PSID")
    base = d["valid"] & d["lw"].notna()
    E = base & d["egrp"].notna()
    d["post_st"] = d["egrp"].isin(MF["post_steep"]).astype(float).where(d["egrp"].notna())
    d["eog10"] = pool_small(d, "eog")
    d["edd10"] = pool_small(d, "edd")
    specs = [("cset", "eset", "early cell set, data-defined (high-paid & high later growth / high-paid only / high "
                              "growth only / neither)", E & d["eset"].notna()),
             ("iset", "eiset", "early industry set, data-defined (33 groups ranked the same way)", E),
             ("grp", "egrp", "early industry group (33)", E),
             ("grp2", "egrp", "early industry group (33), sons with >= 2 early industry years", E & (d["en"] >= 2)),
             ("ddx", "eddx", "early fine industry (ind1990ddx)", E),
             ("mp", "emp", "early manager / professional indicator (2 cells; compare with the 5 special cells)", E),
             ("cell", "ecell", "illustrative: early pre-named cell (5 cells, Section D2; small)", E),
             ("og", "eog", "early cell: occupation group (11) x industry group (33)", E),
             ("occ", "edd", "early occupation (occ1990dd)", E),
             ("o11", "eo11", "early occupation group (11) only", E & d["eo11"].notna()),
             ("o11+grp", ("eo11", "egrp"), "early occupation group (11) + early industry group (33), additive",
              E & d["eo11"].notna()),
             ("occ+grp", ("edd", "egrp"), "early occupation (occ1990dd) + early industry group (33), additive",
              E & d["edd"].notna()),
             ("og10", "eog10", "early cell (11 x 33), cells with < 10 sons pooled", E & d["eog10"].notna()),
             ("occ10", "edd10", "early occupation (occ1990dd), occupations with < 10 sons pooled",
              E & d["edd10"].notna()),
             ("cgrp", "igrp", "current industry group (33), any age profile", E & d["igrp"].notna()),
             ("cddx", "ddx", "current fine industry, any age profile", E & d["igrp"].notna()),
             ("cog", "og", "current cell: occupation group x industry group, any age profile", E & d["og"].notna()),
             ("flp", "e_flp", "illustrative: early finance / insurance / legal / professional indicator", E)]
    nfe = gelbach("gE", d, specs, ctrl_lsn, ("A", "C"))
    print("placebo ...", flush=True)
    PL = {nm: placebo("gP" + nm, d, fe, E & d[fe].notna(), ctrl_lsn, ("A", "C")) for nm, fe in
          (("og", "eog"), ("occ", "edd"))}
    nk["pl"] = "; ".join(f"{nm}: pooled {np.nanmean(PL[nm][:, 1]):.3f}, B-W {np.nanmean(PL[nm][:, 3]):.3f}"
                         for nm in PL)
    run_cells("gFULL", d[base].copy(), ("lw",), ("lyp",), ctrl_lsn, ("A", "C"), bands=BANDS)
    md += ["### A2. Gelbach: early industry / cell x age-band fixed effects (PSID, any profile)", "",
           "Short: son-years in a band, ln wage on ln parental income with Lee-Solon controls. Long: + fixed effects "
           "for the son's EARLY industry (cell, occupation) estimated separately in each band (and race) sample, i.e. "
           "early industry x band FE: they absorb any industry-specific age profile, linear or not, estimated in the "
           "PSID itself (not imported from the CPS), and any payoff after 35 of where the son started. Accounted for "
           "= short - long. Column (3) is the part of the rise from 25-34 to 35-55 that runs through the early "
           "industry. Same son-years in short and long. 'Current' rows use the industry / cell at each age. For "
           f"reference, on ALL valid son-years the pooled coefficient rises by {sc(Dch('gFULL', 'lw', 'P'))} and the "
           f"Black-White gap changes by {sc(Dch('gFULL', 'lw', 'BW'))}.", ""]
    sec_gelbach_table("gE", specs, nfe, md, "PSID")
    pl_rows = ["| Placebo (labels permuted across sons within race, cell sizes kept; 10 draws) | pooled: part of the rise "
               "accounted for, mean [min, max] | its share, mean [min, max] | B-W: part of the change accounted for, mean "
               "[min, max] | its share, mean [min, max] |", "|---|---|---|---|---|"]
    for nm, lab in (("og", "early cell (11 x 33)"), ("occ", "early occupation (occ1990dd)")):
        a = PL[nm]
        pl_rows.append(f"| {lab} | " + " | ".join(f"{np.nanmean(a[:, k]):.3f} [{np.nanmin(a[:, k]):.3f}, "
                                                  f"{np.nanmax(a[:, k]):.3f}]" for k in range(4)) + " |")
        for k, c in enumerate(("pooled contribution", "pooled share", "BW contribution", "BW share")):
            CSV.append(dict(table="A2 placebo PSID", sample=nm, outcome=c, coef=np.nanmean(a[:, k]),
                            se=np.nanstd(a[:, k])))
    md += ["Placebo for the many-cell specifications: if early cells were unrelated to wages, how much would the "
           "Gelbach accounting attribute to them mechanically (finite-sample over-fitting with many small cells, "
           "fewer son-years per cell after 35)?", ""] + pl_rows + [""]
    print("C, D, F ...", flush=True)
    sec_hetero(S, d, md, "PSID")
    sec_datasets(S, MF, md)
    sec_cells(S, MF, md, "PSID")
    OUTD, CON = sec_follow(d, md, fathers)
    print("F8 ...", flush=True)
    sec_f8(d, md)
    print("E: NLSY79 ...", flush=True)
    md += ["## E. NLSY79 replication", "",
           "Men of the NLSY79 living with a parent in 1979 (32 Section 5): hourly wage, industry and occupation of the "
           "CPS (main) job at each round; early industry = modal industry group of the CPS job over the 25-34 rounds. "
           "Regressor ln mean parental income 1979-81; band controls quartic in age + birth-year FE; son-level "
           "controls as in A1; clusters 1979 household; pooled weighted by the 1979 weight. Cohorts 1957-64 are "
           "observed through 2022 (ages 58-65), so nearly every man observed at 25-34 is also observed after 40.", ""]
    sec_sample(j, SN, md, "NLSY79")
    ctrlN = lambda z: ctrl_ageyr(z, "birth_year")
    okN = j["lw"].notna() & j["P"].notna() & j["os"].notna() & j["k_q_t"].notna() & j["ck_t"].notna()
    sec_headline(j, md, "NLSY79", okN, ctrl=ctrlN, need=("C",), tag="hN")
    sec_growth(SN, md, "NLSY79", tagp="N")
    sec_panel(j, md, "NLSY79")
    EN = j["lw"].notna() & j["egrp"].notna()
    specsN = [("cset", "eset", "early cell set, data-defined", EN & j["eset"].notna()),
              ("iset", "eiset", "early industry set, data-defined", EN), ("grp", "egrp", "early industry group (33)", EN),
              ("ddx", "eddx", "early fine industry (ind1990ddx)", EN),
              ("cell", "ecell", "early special cell", EN),
              ("og", "eog", "early cell: occupation group x industry group", EN),
              ("o11", "eo11", "early occupation group (11) only", EN & j["eo11"].notna()),
              ("o11+grp", ("eo11", "egrp"), "early occupation group + early industry group, additive",
               EN & j["eo11"].notna()),
              ("cgrp", "igrp", "current industry group, any age profile", EN & j["igrp"].notna()),
              ("cog", "og", "current cell, any age profile", EN & j["og"].notna())]
    nfeN = gelbach("gN", j, specsN, ctrlN, ("C",))
    md += ["### A2N. Gelbach with early industry / cell x band FE (NLSY79)", ""]
    sec_gelbach_table("gN", specsN, nfeN, md, "NLSY79")
    sec_hetero(SN, j, md, "NLSY79", tagp="N")
    md3 = sec_access(S, d, md)
    md = [y_ for x in md for y_ in (md3 if x == "D3_PLACEHOLDER" else [x])]
    figure(MF, d)
    pd.DataFrame(CSV).to_csv(OUT / "early_industry_late_payoff.csv", index=False)
    summ = summary(MF, nk, CON)
    md = [summ if x == "SUMMARY_PLACEHOLDER" else x for x in md]
    (OUT / "early_industry_late_payoff.md").write_text("\n".join(md), encoding="utf-8")
    print(summ)


if __name__ == "__main__":
    main()
