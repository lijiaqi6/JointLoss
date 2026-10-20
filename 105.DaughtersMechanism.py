r"""Why do daughters of laid-off fathers gain with age? (Fable round 2, Objection 2; plan step 3)

92.LayoffDaughters.py: in one reduced specification a father's teen layoff lowers his son's wage profile and RAISES his
daughter's (within person +0.168**, family income +0.560** at 45-49). Is the daughters' gain real, or selection into
work and marriage? Same specification as 92 (24's children; outcome on ln parental income, the father's teen-window ln
wage, ln hours, unemployment, zero-hours and volatility measures, closure share and layoff share; single-age dummies;
PSID weights of the child-year; father present; clustered by 1968 family), for daughters and, alike, sons:
  employed (hours > 0, every child-year at 25-55); ln annual hours (valid years); partnered (daughter: she is the wife /
  partner of the head; son: his unit has a wife / partner); the spouse's ln earnings (valid years of the partner in the
  same family unit and wave); years of schooling (one row per child); ln hourly wage (valid years) with and without
  controls for partnered and employed-full-year (hours >= 1,500) x age; earnings with zeros kept (Poisson PML, stacked
  25-29 / 45-49, every regressor x band).
Statistics: the layoff coefficient at 25-29 and 45-49 and the change (stacked), and the within-person slope (FE, every
regressor x (age-40)/10). Decision rule (plan): a wage gain that survives work and marriage -> a real asymmetry; a gain
that is selection into work or marriage -> the daughters leave the sons' argument.
Writes output/daughters_mechanism.md / .json (aggregates only). DESCRIPTIVE.
"""
import importlib.util
import json
import sys
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


R92 = _load("s92", "92.LayoffDaughters.py")
R24 = R92.R24
c, dummies, ols_cl, FATHER = R92.c, R92.dummies, R92.ols_cl, R92.FATHER
kL = 1 + FATHER.index("f_sh_layoff")
RES = {}


def poisson_stacked(s, y, b4, base):
    """weighted Poisson PML of y on [base, base x b4]; cluster-robust; returns (change, s.e.), (g0, s.e.), (g4, s.e.)."""
    X = np.column_stack([base, base * b4[:, None]])
    yv, w, g = s[y].to_numpy(float), s["wt"].to_numpy(float), s["fam68"].to_numpy()
    b = np.zeros(X.shape[1])
    b[-1 - base.shape[1] + base.shape[1]] = 0.0
    b[base.shape[1] - 1] = np.log(max(np.average(yv, weights=w), 1e-6))     # constant is the last column of base
    for _ in range(100):
        mu = np.exp(np.clip(X @ b, -30, 30))
        z = X @ b + (yv - mu) / mu
        Wt = w * mu
        bn = np.linalg.lstsq(X * np.sqrt(Wt)[:, None], z * np.sqrt(Wt), rcond=None)[0]
        if np.max(np.abs(bn - b)) < 1e-8:
            b = bn
            break
        b = bn
    mu = np.exp(X @ b)
    H = X.T @ (X * (w * mu)[:, None])
    Hi = np.linalg.pinv(H)
    S = pd.DataFrame(X * (w * (yv - mu))[:, None]).groupby(g).sum().to_numpy()
    G = S.shape[0]
    V = Hi @ (S.T @ S) @ Hi * G / (G - 1)
    K = base.shape[1]
    g0 = (b[kL], np.sqrt(V[kL, kL]))
    g4 = (b[kL] + b[K + kL], np.sqrt(V[kL, kL] + V[K + kL, K + kL] + 2 * V[kL, K + kL]))
    return (b[K + kL], np.sqrt(V[K + kL, K + kL])), g0, g4


def stacked(s, y, extra=()):
    b4 = (s["band"] == 4).to_numpy(float)
    base = np.column_stack([s[["lyp"] + FATHER + list(extra)].to_numpy(float), dummies(s["age"]), np.ones(len(s))])
    X = np.column_stack([base, base * b4[:, None]])
    bb, V = ols_cl(X, s[y].to_numpy(float), s["wt"].to_numpy(float), s["fam68"].to_numpy())
    K = base.shape[1]
    return ((bb[kL], np.sqrt(V[kL, kL])), (bb[kL] + bb[K + kL], np.sqrt(V[kL, kL] + V[K + kL, K + kL] + 2 * V[kL, K + kL])),
            (bb[K + kL], np.sqrt(V[K + kL, K + kL])))


def within(d, y, extra=()):
    a = d["agec"].to_numpy()[:, None]
    X = np.column_stack([d[["lyp"] + FATHER + list(extra)].to_numpy(float) * a, dummies(d["age"])])
    bf, Vf = ols_cl(X, d[y].to_numpy(float), d["wt"].to_numpy(float), d["fam68"].to_numpy(), absorb=d["pid"].to_numpy())
    return (bf[kL], np.sqrt(Vf[kL, kL]))


def main():
    a, py, ch = R24.load()
    ch = ch.drop(columns=[x for x in ("f_sh_close", "f_sh_layoff") if x in ch]).join(R92.layoff_shares(ch, py, a))
    a = a.copy()
    rows = a[["pid", "wave", "int", "wt", "earn", "wife", "head", "female", "hours"]].drop_duplicates(["pid", "wave"])
    wives = a[a["wife"]][["wave", "int"]].drop_duplicates().assign(unit_wife=1.0)
    husb = a[a["head"] & (a["female"] == 0)][["wave", "int", "ly", "valid"]].drop_duplicates(["wave", "int"]).rename(
        columns={"ly": "h_ly", "valid": "h_valid"})
    wifely = a[a["wife"]][["wave", "int", "ly", "valid"]].drop_duplicates(["wave", "int"]).rename(
        columns={"ly": "w_ly", "valid": "w_valid"})
    md = ["# Why do daughters of laid-off fathers gain with age? (Fable round 2, Objection 2)", "",
          "Built by `105.DaughtersMechanism.py` (2026-10-20); design in its docstring. Coefficient of the father's teen "
          "layoff share (per unit share); clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1. **Descriptive.**", "",
          "| children | outcome | 25-29 | 45-49 | change | within person x age | N children |", "|---" * 7 + "|"]
    for female, lab in ((1, "daughters"), (0, "sons")):
        r, lt = R24.frames(a, ch, female)
        r = r.drop(columns=[x for x in ("f_sh_close", "f_sh_layoff") if x in r]).join(ch[["f_sh_close", "f_sh_layoff"]], on="pid")
        r = r.merge(rows.drop(columns=["hours"]), on=["pid", "wave"], how="left", suffixes=("", "_a"))
        r = r[(r["wt"] > 0) & r["fpid"].notna() & (r["f_n"] >= 3)].dropna(subset=["lyp"] + FATHER).copy()
        r["band"] = pd.cut(r["age"], [24, 29, 34, 39, 44, 49, 55], labels=False)
        r["agec"] = (r["age"] - 40) / 10
        r["emp"] = (r["hours"] > 0).astype(float).where(r["hours"].notna())
        r["ft"] = (r["hours"] >= 1500).astype(float).where(r["hours"].notna())
        r["lh_v"] = r["lh"].where(r["valid"] == True)  # noqa: E712
        if female:
            r["partnered"] = r["wife"].astype(float)
            r = r.merge(husb, on=["wave", "int"], how="left")
            r["sp_ly"] = r["h_ly"].where((r["wife"] == True) & (r["h_valid"] == True))  # noqa: E712
        else:
            r = r.merge(wives, on=["wave", "int"], how="left").merge(wifely, on=["wave", "int"], how="left")
            r["partnered"] = r["unit_wife"].fillna(0.0)
            r["sp_ly"] = r["w_ly"].where(r["w_valid"] == True)  # noqa: E712
        r["earn0"] = r["earn"].clip(lower=0) / 1000
        for x in ("partnered", "ft"):
            r[f"{x}_xa"] = r[x] * r["agec"]
        for y, ylab, extra in (("emp", "employed", ()), ("lh_v", "ln annual hours", ()), ("partnered", "partnered", ()),
                               ("sp_ly", "partner's ln earnings", ()), ("lw", "ln hourly wage", ()),
                               ("lw", "ln hourly wage | partnered, full year", ("partnered", "ft")),
                               ("ly", "ln earnings", ())):
            d = r.dropna(subset=[y] + list(extra))
            s = d[d["band"].isin([0, 4])]
            g0, g4, ch_ = stacked(s, y, extra)
            fe = within(d, y, extra)
            md.append(f"| {lab} | {ylab} | {c(g0)} | {c(g4)} | {c(ch_)} | {c(fe)} | {d['pid'].nunique():,} |")
            RES[f"{lab}|{ylab}"] = {"g0": list(map(float, g0)), "g4": list(map(float, g4)), "change": list(map(float, ch_)),
                                    "fe": list(map(float, fe)), "n": int(d["pid"].nunique())}
        # earnings with zeros kept, Poisson PML (stacked)
        d = r.dropna(subset=["earn0"])
        s = d[d["band"].isin([0, 4])]
        b4 = (s["band"] == 4).to_numpy(float)
        base = np.column_stack([s[["lyp"] + FATHER].to_numpy(float), dummies(s["age"]), np.ones(len(s))])
        ch_, g0, g4 = poisson_stacked(s, "earn0", b4, base)
        md.append(f"| {lab} | earnings with zeros (Poisson PML) | {c(g0)} | {c(g4)} | {c(ch_)} | | {d['pid'].nunique():,} |")
        RES[f"{lab}|ppml"] = {"g0": list(map(float, g0)), "g4": list(map(float, g4)), "change": list(map(float, ch_))}
        # schooling, one row per child
        one = r.drop_duplicates("pid").merge(lt[["pid", "educ"]].rename(columns={"educ": "educ_c"}), on="pid", how="left")
        one = one.dropna(subset=["educ_c"])
        one = one[one["educ_c"].between(0, 20)]
        X = np.column_stack([one[["lyp"] + FATHER].to_numpy(float), dummies(one["birth_year"] // 5), np.ones(len(one))])
        bb, V = ols_cl(X, one["educ_c"].to_numpy(float), one["wt"].to_numpy(float), one["fam68"].to_numpy())
        md.append(f"| {lab} | years of schooling (one row per child) | {c((bb[kL], np.sqrt(V[kL, kL])))} | | | | {len(one):,} |")
        RES[f"{lab}|schooling"] = [float(bb[kL]), float(np.sqrt(V[kL, kL]))]
        print(lab, "done", flush=True)
    md.append("")
    (OUT / "daughters_mechanism.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "daughters_mechanism.json", "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    main()
