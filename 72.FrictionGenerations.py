r"""Fable T2-T5 (proposals/fable_search_friction_ige.md, 2026-10-19): can a search friction in the son's or the father's
generation produce the flat Black / rising White IGE profile? PSID son panel of 36 (24's frame), sons 25-55.

T2 SELECTION INTO WAGES. (a) share of zero-hours years on log parental income by band and race; (b) the log-wage IGE
   profile with zero-hours years imputed (i) at the son's last observed wage, (ii) at the 10th percentile of his race x
   band. Selection predicts a Black gradient of non-employment that steepens with age and an imputed Black profile
   that rises.
T3 FATHER'S AND MOTHER'S SCHOOLING AS THE BACKGROUND MEASURE (schooling is set before the father meets any labor-market
   friction). By band: son's log wage on the parent's years of schooling, alone, with log parental income, and with the
   son's schooling; and the ten-year wage growth (25-29 -> 35-39) on it at equal schooling. "Parental income is a worse
   signal of Black fathers' skill" predicts that father's schooling pays off in Black sons' wages more with age.
T4 THE FATHER'S FRICTION INSIDE THE WINDOW. (a) the share of the variance of parental income accounted for by the
   father's shares of years displaced / unemployed / with zero hours in the childhood window; (b) the IGE profile with
   those shares as controls; (c) the IGE on the father's family income over all his window years (f_lfam_all) vs his clean years
   (no displacement, unemployment or zero hours; f_lfam_cA), same sons.
T5 SHARED LOCAL LABOR MARKETS. The IGE profile without and with fixed effects for the state at 17 (family-file state,
   waves 1976+, as 49.PaperBPolicyShocks.py), same sons.
IGE by band: log wage on the regressor with single-age dummies, sons' person-years in the band, by race; opening = 45-49
minus 25-29 from one stacked regression per race; races are independent samples (1968 families), so the White - Black
s.e. adds the variances. S.e. clustered by 1968 family. DESCRIPTIVE. Writes output/friction_generations.md and .json.
"""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import DATA, OUT  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R36 = _load("s36", "36.SameEmployerGrowthChecks.py")
BANDS = [(25, 29), (30, 34), (35, 39), (40, 44), (45, 49), (50, 55)]
RES = {}


def fitc(X, y, g):
    X = np.column_stack([X, np.ones(len(y))])
    XtXi = np.linalg.pinv(X.T @ X)
    b = XtXi @ X.T @ y
    u = y - X @ b
    S = pd.DataFrame(u[:, None] * X).groupby(g).sum().to_numpy()
    G, (n, k) = S.shape[0], X.shape
    V = XtXi @ (S.T @ S) @ XtXi * G / (G - 1) * (n - 1) / (n - k)
    return b, V


def profile(d, y, x, ctrl=(), fe=None, extra=()):
    """band slopes of y on x (each band its own slope; single-age dummies; ctrl and fe interacted with band)."""
    out = {}
    need = [y, x, "age", "fam68", "race"] + list(ctrl) + list(extra) + ([fe] if fe else [])
    d = d.dropna(subset=need)
    d = d[d["age"].between(25, 55)].copy()
    d["band"] = pd.cut(d["age"], [24, 29, 34, 39, 44, 49, 55], labels=False)
    for r in ("White", "Black"):
        z = d[d["race"] == r]
        B = pd.get_dummies(z["band"], prefix="b").astype(float)
        cols = [B[c] * z[x] for c in B.columns]
        names = [f"x_b{c[2:]}" for c in B.columns]
        for c in ctrl:
            cols += [B[cc] * z[c] for cc in B.columns]
            names += [f"{c}_b{cc[2:]}" for cc in B.columns]
        A = pd.get_dummies(z["age"].astype(int), prefix="a", drop_first=True).astype(float)
        parts = [pd.concat(cols, axis=1).set_axis(names, axis=1), A]
        if fe:
            parts.append(pd.get_dummies(z[fe].astype(int), prefix="fe", drop_first=True).astype(float))
        X = pd.concat(parts, axis=1)
        b, V = fitc(X.to_numpy(float), z[y].to_numpy(float), z["fam68"].to_numpy())
        idx = {n: i for i, n in enumerate(names)}
        sl = {k: (float(b[idx[f"x_b{k}"]]), float(np.sqrt(V[idx[f"x_b{k}"], idx[f"x_b{k}"]])))
              for k in range(6) if f"x_b{k}" in idx}
        op = None
        if "x_b0" in idx and "x_b4" in idx:
            i0, i4 = idx["x_b0"], idx["x_b4"]
            op = (float(b[i4] - b[i0]), float(np.sqrt(V[i4, i4] + V[i0, i0] - 2 * V[i4, i0])))
        out[r] = {"bands": sl, "open": op, "n_sons": int(z["pid"].nunique()), "n": int(len(z))}
    W, Bk = out["White"], out["Black"]
    out["W-B"] = {"bands": {k: (W["bands"][k][0] - Bk["bands"][k][0],
                                float(np.hypot(W["bands"][k][1], Bk["bands"][k][1])))
                            for k in W["bands"] if k in Bk["bands"]},
                  "open": (W["open"][0] - Bk["open"][0], float(np.hypot(W["open"][1], Bk["open"][1])))
                  if W["open"] and Bk["open"] else None}
    return out


def star(p):
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""


def c(t, dec=3):
    if t is None:
        return ""
    b, s = t
    p = 2 * (1 - norm.cdf(abs(b) / s)) if s > 0 else np.nan
    return f"{b:.{dec}f}{star(p)} ({s:.{dec}f}; p={p:.3f})"


def table(md, title, specs, note=""):
    md += [f"### {title}", ""] + ([note, ""] if note else [])
    md += ["| specification | race | " + " | ".join(f"{lo}-{hi}" for lo, hi in BANDS) + " | opening 45-49 - 25-29 | sons |",
           "|---" * 10 + "|"]
    for lab, o in specs:
        RES[f"{title}|{lab}"] = o
        for r in ("White", "Black", "W-B"):
            cells = [c(o[r]["bands"].get(k)) for k in range(6)]
            md.append(f"| {lab} | {r} | " + " | ".join(cells) + f" | {c(o[r]['open'])} | "
                      f"{o[r].get('n_sons', '')} |")
    md.append("")


def state17(r):
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    hs = pd.read_pickle(DATA / "husband_shocks_fam.pkl")[["wave", "int", "fips"]].drop_duplicates(["wave", "int"])
    ch = py[py["child"] & py["age"].between(14, 20) & (py["wave"] >= 1976)][["pid", "wave", "int", "age"]]
    ch = ch.merge(hs, on=["wave", "int"], how="inner").dropna(subset=["fips"])
    ch = ch.assign(dist=(ch["age"] - 17).abs()).sort_values(["pid", "dist", "wave"]).drop_duplicates("pid")
    return r.merge(ch[["pid", "fips"]].rename(columns={"fips": "fips17"}), on="pid", how="left")


if __name__ == "__main__":
    r, *_ = R36.psid_build()
    r = r[r["race"].isin(["Black", "White"]) & r["age"].between(25, 55)].copy()
    r = r.sort_values(["pid", "wave"])
    md = ["# Search friction in two generations and the IGE profile (Fable T2-T5)", "",
          "Built by `72.FrictionGenerations.py` (2026-10-19); definitions in its docstring. Log-wage IGE by band "
          "(single-age dummies), estimate (s.e.; p), *** p<0.01, ** p<0.05, * p<0.1, s.e. clustered by 1968 family; "
          "opening = 45-49 minus 25-29. **Descriptive.**", ""]
    # ---------------- T2 selection into wages
    z = r[r["zero"].notna()].copy()
    md += ["## T2. Selection into wages", "",
           f"Person-years with the zero-hours flag: {len(z):,}; zero-hours share White {z.loc[z.race=='White','zero'].mean():.3f}, "
           f"Black {z.loc[z.race=='Black','zero'].mean():.3f}; zero-hours years without a wage: "
           f"{int((z['zero'].eq(1) & z['lw'].isna()).sum()):,} of {int(z['zero'].eq(1).sum()):,}.", ""]
    table(md, "T2a. Zero-hours share on log parental income", [
        ("raw", profile(z, "zero", "lyp")), ("at equal schooling", profile(z, "zero", "lyp", ctrl=["educ"]))])
    z["lw_last"] = z.groupby("pid")["lw"].ffill()
    p10 = z.groupby(["race", pd.cut(z["age"], [24, 29, 34, 39, 44, 49, 55])], observed=True)["lw"].transform(
        lambda v: v.quantile(0.10))
    z["imp_last"] = z["lw"].where(z["lw"].notna() | z["zero"].ne(1), z["lw_last"])
    z["imp_p10"] = z["lw"].where(z["lw"].notna() | z["zero"].ne(1), p10)
    table(md, "T2b. Log-wage IGE with zero-hours years imputed", [
        ("observed wages", profile(z, "lw", "lyp")), ("zero years at the last wage", profile(z, "imp_last", "lyp")),
        ("zero years at the race x band 10th percentile", profile(z, "imp_p10", "lyp"))])
    # ---------------- T3 parents' schooling
    ce = pd.read_pickle(DATA / "psid_child_exposure.pkl")[["pid", "mom_educ"]]
    r = r.merge(ce, on="pid", how="left")
    r["mom_educ"] = r["mom_educ"].where(r["mom_educ"].between(0, 20))
    r["f_educ"] = r["f_educ"].where(r["f_educ"].between(0, 20))
    fs = r[r["f_educ"].notna()]
    md += ["## T3. Parents' schooling as the background measure", "",
           f"Sons with father's schooling: White {fs.loc[fs.race=='White','pid'].nunique():,}, Black "
           f"{fs.loc[fs.race=='Black','pid'].nunique():,}; with mother's schooling: White "
           f"{r.loc[r.mom_educ.notna() & (r.race=='White'),'pid'].nunique():,}, Black "
           f"{r.loc[r.mom_educ.notna() & (r.race=='Black'),'pid'].nunique():,}.", ""]
    table(md, "T3a. Log wage on father's years of schooling (father-present sons)", [
        ("father's schooling alone", profile(fs, "lw", "f_educ")),
        ("with log parental income", profile(fs, "lw", "f_educ", ctrl=["lyp"])),
        ("with log parental income and own schooling", profile(fs, "lw", "f_educ", ctrl=["lyp", "educ"]))])
    table(md, "T3b. Log wage on log parental income, same father-present sons", [
        ("alone", profile(fs, "lw", "lyp", extra=["f_educ"])),
        ("with father's schooling", profile(fs, "lw", "lyp", ctrl=["f_educ"])),
        ("with father's and own schooling", profile(fs, "lw", "lyp", ctrl=["f_educ", "educ"]))])
    ms = r[r["mom_educ"].notna()]
    table(md, "T3c. Log wage on mother's years of schooling", [
        ("mother's schooling alone", profile(ms, "lw", "mom_educ")),
        ("with log parental income and own schooling", profile(ms, "lw", "mom_educ", ctrl=["lyp", "educ"]))])
    # ten-year growth on parents' schooling at equal schooling (son level)
    sb = r[r["lw"].notna()].assign(b=pd.cut(r["age"], [24, 29, 34, 39], labels=["2529", "3034", "3539"]))
    S = sb.pivot_table(index="pid", columns="b", values="lw", aggfunc="mean", observed=False)
    S = S.join(r.drop_duplicates("pid").set_index("pid")[["race", "fam68", "lyp", "educ", "f_educ", "mom_educ",
                                                           "birth_year"]])
    S["g10"] = S["3539"] - S["2529"]
    md += ["### T3d. Ten-year wage growth (25-29 -> 35-39) on parents' schooling and income, at equal schooling", "",
           "| regressor | White | Black | White - Black | sons W / B |", "|---|---|---|---|---|"]
    for reg, ctrl in (("f_educ", ["educ"]), ("mom_educ", ["educ"]), ("lyp", ["educ"]), ("f_educ", ["educ", "lyp"])):
        cells, ns, bs = [], [], {}
        for rr in ("White", "Black"):
            q = S[(S["race"] == rr)].dropna(subset=["g10", reg, "fam68"] + ctrl + ["birth_year"])
            Xd = pd.concat([q[[reg] + ctrl], pd.get_dummies(q["birth_year"].astype(int), prefix="by",
                                                             drop_first=True).astype(float)], axis=1)
            b, V = fitc(Xd.to_numpy(float), q["g10"].to_numpy(float), q["fam68"].to_numpy())
            bs[rr] = (float(b[0]), float(np.sqrt(V[0, 0])))
            cells.append(c(bs[rr]))
            ns.append(str(len(q)))
        dif = (bs["White"][0] - bs["Black"][0], float(np.hypot(bs["White"][1], bs["Black"][1])))
        RES[f"T3d|{reg}|{'+'.join(ctrl)}"] = {"White": bs["White"], "Black": bs["Black"], "W-B": dif}
        md.append(f"| {reg} (controls: {', '.join(ctrl)}) | {cells[0]} | {cells[1]} | {c(dif)} | {' / '.join(ns)} |")
    md.append("")
    # ---------------- T4 the father's friction inside the window
    one = r.drop_duplicates("pid")
    md += ["## T4. The father's friction inside the childhood window", "",
           "| race | sons | mean share displaced / unemployed / zero hours | R2 of log parental income on the three shares |",
           "|---|---|---|---|"]
    for rr in ("White", "Black"):
        q = one[(one["race"] == rr)].dropna(subset=["lyp", "f_sh_disp", "f_sh_unemp", "f_sh_zero"])
        X = np.column_stack([q[["f_sh_disp", "f_sh_unemp", "f_sh_zero"]].to_numpy(float), np.ones(len(q))])
        b = np.linalg.lstsq(X, q["lyp"].to_numpy(float), rcond=None)[0]
        u = q["lyp"].to_numpy(float) - X @ b
        r2 = 1 - u.var() / q["lyp"].var(ddof=0)
        RES[f"T4a|{rr}"] = {"r2": float(r2), "n": int(len(q))}
        md.append(f"| {rr} | {len(q):,} | {q['f_sh_disp'].mean():.3f} / {q['f_sh_unemp'].mean():.3f} / "
                  f"{q['f_sh_zero'].mean():.3f} | {r2:.4f} |")
    md.append("")
    fw = r.dropna(subset=["f_sh_disp", "f_sh_unemp", "f_sh_zero"])
    table(md, "T4b. Log-wage IGE with the father's friction shares as controls (same sons)", [
        ("without", profile(fw, "lw", "lyp", extra=["f_sh_disp", "f_sh_unemp", "f_sh_zero"])),
        ("with the three shares", profile(fw, "lw", "lyp", ctrl=["f_sh_disp", "f_sh_unemp", "f_sh_zero"]))])
    fc = r.dropna(subset=["f_lfam_all", "f_lfam_cA"])
    table(md, "T4c. Log-wage IGE on the father's log family income: all window years vs his clean years (same sons)", [
        ("all window years", profile(fc, "lw", "f_lfam_all", extra=["f_lfam_cA"])),
        ("clean years (no displacement / unemployment / zero hours)", profile(fc, "lw", "f_lfam_cA", extra=["f_lfam_all"]))])
    # ---------------- T5 state at 17
    r = state17(r)
    st = r[r["fips17"].notna()]
    md += ["## T5. Shared local labor markets", "",
           f"Sons with a state at 17 (waves 1976+): White {st.loc[st.race=='White','pid'].nunique():,}, Black "
           f"{st.loc[st.race=='Black','pid'].nunique():,}.", ""]
    table(md, "T5. Log-wage IGE without and with state-at-17 fixed effects (same sons)", [
        ("without", profile(st, "lw", "lyp", extra=["fips17"])),
        ("with state-at-17 FE", profile(st, "lw", "lyp", fe="fips17"))])
    (OUT / "friction_generations.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "friction_generations.json", "w"), indent=1, default=str)
    print("\n".join(md))
