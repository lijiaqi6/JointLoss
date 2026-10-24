r"""Why no first stage of the EITC on mothers' work? Already working, not looking, or married (PI question, 2026-10-24)

126.EITCDesign.py: a thousand dollars more of maximum credit in a window year does not move the mother's employment
(-0.009, p = 0.44) or the family's earned income in the PSID. PI: is it because mothers already work; among those not
working, are they looking (search friction); if not looking, what reasons do they give; and what of the credit itself
and the wage?
MOTHERS: the wife or female head of the son's family unit in his window years (income years at 13-18, 1979+ when the
  individual-file employment status exists; 24's panel); single = female head (no husband in the unit that wave).
STATUS at the interview (24's est): working (1), temporarily laid off (2), unemployed and looking (3), retired (4),
  disabled (5), keeping house (6), student (7), other (8).
CREDIT: imputed from the family's actual earned income (head + wife labor income, nominal), number of children and
  year (61's schedule from 1984, joint filers when married; 1975-78 and 1979-83 statutory), times (1 + state rate), in
  thousands of 2000 dollars; take-up assumed. The PSID does not record EITC receipt.
FIRST STAGE: 126's regression (year, state, number-of-children FE; clusters 1968 family) by single / married and in
  126's likely-eligible tercile: employed, annual hours, ln wage (working mothers), looking among those not working,
  and the imputed credit.
REASONS NOT LOOKING (2019-2023, 'BC68 / DE68 MAIN REASON NOT LOOKING'; asked of heads and spouses not working and not
  looking in the last four weeks): women with a child under 18 in the family unit, all PSID families, by whether the
  family's earned income is in the credit's range. Grouped: no work / couldn't find work / lack of schooling /
  employers' views or discrimination / transportation (labor-market reasons); family responsibilities / child care;
  in school; disability; retired; other.
Writes output/eitc_mothers.md / .json (aggregates only). DESCRIPTIVE.
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
from common import CPI, DATA, OUT  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R126 = _load("s126", "126.EITCDesign.py")
R101, R61, R75, R24 = R126.R101, R126.R61, R126.R75, R126.R24
R18 = _load("s18", "18.HusbandIndustryShocks.py")
c = R101.c
RGROUP = {1: "labor market", 2: "labor market", 3: "labor market", 4: "labor market", 5: "labor market",
          7: "labor market", 8: "family / child care", 9: "family / child care", 6: "in school", 10: "disability",
          11: "retired", 97: "other"}
RES = {}


def credit(E, n, year, joint):
    """federal credit (nominal) at earned income E."""
    if n <= 0 or year < 1975 or E <= 0:
        return 0.0
    if year < 1979:
        r_in, mx, r_out, ps = 0.10, 400.0, 0.10, 4000.0
    elif year < 1984:
        r_in, mx, r_out, ps = 0.10, 500.0, 0.125, 6000.0
    else:
        r_in, mx, r_out, ps1, psj = R61.EITC[min(year, max(R61.EITC))][min(n, 3)]
        ps = psj if joint else ps1
    return float(max(0.0, min(r_in * E, mx) - max(0.0, r_out * (E - ps))))


def reasons():
    out = []
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    kids = py[py["age"].between(0, 17)].groupby(["wave", "int"]).size().rename("nk").reset_index()
    for w in (2019, 2021, 2023):
        do = next(f for f in (R18.FAM / f"fam{w}er").glob("*.do") if "formats" not in f.name)
        pos, labs = R18.layout(do)
        idv = labs[1][0]
        hv = next(v for v, l in labs if re.match(r"BC68 MAIN REASON NOT LOOKING", l))
        sv = next(v for v, l in labs if re.match(r"DE68 MAIN REASON NOT LOOKING", l))
        f = R18.read(do.with_suffix(".txt"), [idv, hv, sv], pos).rename(columns={idv: "int", hv: "rh", sv: "rs"})
        f["wave"] = w
        out.append(f)
    F = pd.concat(out, ignore_index=True).merge(kids, on=["wave", "int"], how="inner")
    hd = py[py["head"]][["wave", "int", "female", "hlab", "wlab"]].drop_duplicates(["wave", "int"])
    F = F.merge(hd, on=["wave", "int"], how="left")
    # women: female head (rh) or spouse of a male head (rs)
    F["reason"] = np.where(F["female"] == 1, F["rh"], F["rs"])
    F["single"] = (F["female"] == 1).astype(float)
    F = F[F["reason"].isin(list(RGROUP))].copy()
    defl = {w: CPI[2000] / CPI[w - 1] for w in (2019, 2021, 2023)}
    nom = (F["hlab"].fillna(0) + F["wlab"].fillna(0)) / F["wave"].map(defl)
    F["elig"] = [(e > 0) and (e < R126.phase_end(w - 1, min(int(n), 3), s == 0)) for e, n, w, s in
                 zip(nom, F["nk"], F["wave"], F["single"])]
    F["grp"] = F["reason"].map(RGROUP)
    return F


def main():
    r = R75.build()
    W = R126.window_years(r)
    a = pd.read_pickle(R24.CACHE)
    wom = a[a["wife"] | (a["head"] & (a["female"] == 1))][["wave", "int", "est", "lw", "head"]].drop_duplicates(
        ["wave", "int"]).rename(columns={"lw": "m_lw", "head": "m_head"})
    W = W.merge(wom, on=["wave", "int"], how="left")
    W = W[W["year"] >= 1979].copy()
    W["single"] = (W["m_head"] == True).astype(float)  # noqa: E712
    nom = (W["hlab"].fillna(0) + W["wlab"].fillna(0)) / W["defl"]
    W["credit"] = [credit(e, int(n), int(y), s == 0) for e, n, y, s in zip(nom, W["nk"], W["year"], W["single"])]
    W["credit"] = W["credit"] * (1 + W["state_eitc_rate"]) * W["defl"] / 1000
    W["notwork"] = (~W["est"].isin([1, 2])).astype(float).where(W["est"].notna())
    W["looking"] = (W["est"] == 3).astype(float).where(W["notwork"] == 1)
    # likely eligible from 126 (re-fit the same logit)
    one = r.drop_duplicates("pid")[["pid", "m_educ0", "m_educ_na"]]
    pre = R126.pre_income(r)
    Z = W.merge(one, on="pid", how="left").merge(pre, left_on="pid", right_index=True, how="left").dropna(subset=["lyp612"])
    import statsmodels.api as sm
    Z["m_ed"] = Z["m_educ0"].where(Z["m_educ_na"] == 0, Z["m_educ0"].mean())
    X = pd.concat([Z[["lyp612", "m_ed", "m_educ_na", "nofa"]].astype(float),
                   pd.get_dummies(Z["nk"], prefix="nk", drop_first=True, dtype=float),
                   pd.get_dummies(Z["year"], prefix="y", drop_first=True, dtype=float)], axis=1)
    Z["p"] = sm.Logit(Z["elig"], sm.add_constant(X)).fit(disp=0).predict(sm.add_constant(X))
    pe = Z.groupby("pid")["p"].mean()
    W["likely"] = W["pid"].map((pe >= pe.quantile(2 / 3)).astype(float))
    md = ["# Why no first stage of the EITC on mothers' work? (PI question)", "",
          "Built by `127.EITCMothers.py` (2026-10-24); design in its docstring. *** p<0.01, ** p<0.05, * p<0.1. "
          "**Descriptive.**", "",
          "## 1. The mothers in the sons' window years (1979+)", "",
          "| mothers | window years | employed (hours > 0) | working at interview | temporarily laid off | unemployed, "
          "looking | keeping house | disabled / retired / student / other | looking among not working | imputed credit "
          "(1,000 2000 $) | in the credit's range |", "|---" * 11 + "|"]
    groups = (("all", W), ("married", W[W["single"] == 0]), ("single", W[W["single"] == 1]),
              ("married, likely eligible", W[(W["single"] == 0) & (W["likely"] == 1)]),
              ("single, likely eligible", W[(W["single"] == 1) & (W["likely"] == 1)]))
    for lab, q in groups:
        e = q.dropna(subset=["est"])
        sh = lambda codes: float(e["est"].isin(codes).mean())  # noqa: E731
        row = {"n": len(q), "emp": float(q["m_emp"].mean()), "work": sh([1]), "temp": sh([2]), "look": sh([3]),
               "house": sh([6]), "other": sh([4, 5, 7, 8, 9]), "look_nw": float(q["looking"].mean()),
               "credit": float(q["credit"].mean()), "elig": float(q["elig"].mean())}
        RES[f"desc|{lab}"] = row
        md.append(f"| {lab} | {row['n']:,} | {row['emp']:.3f} | {row['work']:.3f} | {row['temp']:.3f} | {row['look']:.3f} | "
                  f"{row['house']:.3f} | {row['other']:.3f} | {row['look_nw']:.3f} | {row['credit']:.3f} | "
                  f"{row['elig']:.3f} |")
    md += ["", "## 2. First stage by marital status: outcome in the window year on that year's maximum credit "
           "(1,000 2000 $)", "", "| outcome | married | single | married, likely eligible | single, likely eligible |",
           "|---|---|---|---|---|"]
    for y, lab in (("m_emp", "employed"), ("m_hrs", "annual hours"), ("m_lw", "ln wage (working)"),
                   ("looking", "looking for work, among not working"), ("credit", "imputed credit received"),
                   ("l_earn", "ln family earned income")):
        cells = []
        for glab, q in groups[1:]:
            q = q.dropna(subset=[y])
            if len(q) < 200:
                cells.append("")
                continue
            t, n = R126.fs_reg(q, y)
            cells.append(f"{c(t)} [{n:,}]")
            RES[f"fs|{y}|{glab}"] = [float(t[0]), float(t[1]), n]
        md.append(f"| {lab} | " + " | ".join(cells) + " |")
        print(md[-1], flush=True)
    md.append("")
    # 3. reasons
    F = reasons()
    md += ["## 3. Main reason for not looking: women with a child under 18, not working and not looking (2019-2023, "
           "all PSID families, unweighted)", "",
           "| reason | all | single | married | earned income in the credit's range | not in range |",
           "|---|---|---|---|---|---|"]
    cols = (("all", F), ("single", F[F["single"] == 1]), ("married", F[F["single"] == 0]),
            ("in range", F[F["elig"]]), ("not in range", F[~F["elig"]]))
    for g in ["family / child care", "labor market", "disability", "in school", "retired", "other"]:
        md.append(f"| {g} | " + " | ".join(f"{(q['grp'] == g).mean():.3f}" for _, q in cols) + " |")
        RES[f"reason|{g}"] = {lab: float((q["grp"] == g).mean()) for lab, q in cols}
    md.append("| n | " + " | ".join(f"{len(q):,}" for _, q in cols) + " |")
    lm = F[F["grp"] == "labor market"]["reason"].value_counts().to_dict()
    md += ["", f"Labor-market reasons in detail (codes: 1 no work available in the area, 2 couldn't find any work, 3 lack "
           f"schooling / training, 4 employers think too young or old, 5 other discrimination, 7 transportation): {lm}; "
           f"family: 8 family responsibilities {int((F['reason'] == 8).sum())}, 9 can't arrange child care "
           f"{int((F['reason'] == 9).sum())}.", ""]
    (OUT / "eitc_mothers.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "eitc_mothers.json", "w"), indent=1, default=float)
    print("\n".join(md))


if __name__ == "__main__":
    main()
