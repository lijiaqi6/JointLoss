r"""What is in the "rest" of the IGE split (Paper B primary goal; follows 75.WhatIsPassedOn.py, EVIDENCE 11.29).

QUESTION. In 75, 63%*** of the pooled earnings IGE (0.249 of 0.396) is parental income at equal parental components
(wage, hours, stability, place). What is it? This script adds the other parts of parental income and the family's
other resources as further mediators of the same exact Gelbach split, so the rest is split into:
  LABOUR EARNINGS  lpl    ln of the parents' combined labour income (head + wife), mean over the window years in
                          bounds: earnings not captured by the mean ln wage / ln hours of each parent (years without a
                          valid wage, the second earner's level, aggregation of logs)
  ASSETS           s_asset share of family income that is asset income of head and wife (their taxable income minus
                          their labour income: interest, dividends, rent, the asset part of business income; from 1994
                          also the labour part of business income, which 1.PSID.py leaves out of labour income)
                   own    share of window years in an owner-occupied home ('OWN/RENT OR WHAT' = 1)
  TRANSFERS        s_tr   share of family income that is transfer income of head and wife (welfare, SSI, social
                          security, unemployment insurance, child support, alimony, help from relatives)
                   welf   share of window years with ADC / AFDC / TANF of head or wife (amount > 0 or 'whether' = 1)
  OTHERS           s_oth  share of family income from other family-unit members (family income - head and wife's
                          taxable and transfer income)
  FAMILY SIZE      nkid   mean number of children in the family unit
  PARENTS' SCHOOLING f_ed, m_ed  father's and mother's years of schooling (74's f_educ0 / m_educ0; where missing,
                          the weighted mean of the observed, with the flags f_educ_na, m_educ_na in the structure group)
The four components of 75 and its structure group are kept as they are; inc_na (the son has fewer than 3 window years
with the income items) joins the structure group. Food stamps are not in PSID family income and their items change
form across waves (value saved 1969-72, last month 1975, months used 1980, persons 1981-87, two-years-ago from 1999),
so they are not used.

DATA (read only): PSID family files 1968-2011 (1.PSID.py layout / read), items listed per wave in the output;
  hw_tax / hw_tr as ReducedForm/56.NonlaborIncome.py's patterns, with the waves it misses filled by hand: 1968 tax V76,
  transfers V80 (the family's transfer income, others included - no head-and-wife split that wave), 1971 V1922,
  1972 V2523 ('TRANSFER Y H& W'), 1974 tax V3472; no head-and-wife transfer total in 1969, 1976, 1984 (the window mean
  uses the other years). Shares use the same file's nominal total family income; labour income share from
  psid_person_year (hlab + wlab over faminc, same deflator). Shares are clipped to [0, 1] (asset income can be negative
  through business losses; clipped at 0). Window = the son's wave-ages 13-19 with family income in bounds (75); a
  measure needs >= 3 window years. Missing measures: weighted mean of the observed (75's rule) + inc_na.
DESIGN: 75's exact Gelbach split (74's run_spec), x = lyp, 200 cluster-bootstrap draws of 1968 families stratified by
  race. Two splits on the same son-years: (A) 75's groups (reproduces 75), (B) 75's groups + the six above. b0 is the
  same in both; (B)'s rest is parental income at equal components AND equal other resources. Pooled and by race; son's
  outcomes ln earnings, ln wage, ln hours (valid years), employment, ln family income.
DESCRIPTIVE ACCOUNTING: a mediator's contribution is the part of the IGE carried by parental-income differences that
  are differences in it; nothing here is causal.
Writes output/what_is_passed_on_rest.md and .json (aggregates only); caches the family items in
data/what_is_passed_on_rest_fam.pkl (family-level, git-ignored).
"""
import importlib.util
import json
import re
import sys
import time
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
P1 = _load("p1", "1.PSID.py")
est, cc, Boot, run_spec = R74.est, R74.cc, R74.Boot, R74.run_spec
FCACHE = DATA / "what_is_passed_on_rest_fam.pkl"
CELLS, CLAB = R75.CELLS, R75.CLAB
TAX = (r"^(H\+W (\d\d |\d{4} )?TAXABLE (INC|Y)|HD\+WF (\d{4} )?TAXABLE (INCOME|Y)|TAXABLE INCOME H& W|"
       r"HEAD AND (WIFE|SPOUSE) TAXABLE INCOME|HEAD AND TAXABLE INCOME WIFE|REF PERSN AND SPOUSE TAXABLE INCOME)")
TRN = (r"^(H\+W (\d\d |\d{4} )?TOT ?(\d{4} )?TRANS(FER)? Y|H\+W TOT(AL)? TRANSFER|TRANSFER Y H\+W|TOT TRANSFER Y$|"
       r"HD\+WF (\d{4} )?TOTAL TRANSFER INCOME|HD\+WF TRANSFER INCOME|HEAD AND (WIFE|SPOUSE) TRANSFER INCOME|"
       r"RP AND SPOUSE TRANSFER INCOME)")
HAND = {1968: {"tax": "V76", "tr": "V80"}, 1971: {"tr": "V1922"}, 1972: {"tr": "V2523"}, 1974: {"tax": "V3472"}}
ADC = r"ADC|AFDC|TANF"
ADC_NOT = (r"ACC|BKT|OTH|OFUM|OTR|TIME UNIT|PER$| PER |JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|SSI|ELIG|# ?MO|"
           r"EXC|NON ?ADC|NOADC|TRAN|WAS|PRIOR|MONTH|EVER|LAST|-O\b|INC-O|PREV|WHY|TRY|APPL|PAYBACK|GOV|\bST\b|# ?PREG|WELF|"
           r"WEL/|ETC|NEED")
OWN, OWN_NOT = r"OWN ?/ ?RENT|OWN OR RENT", r"WHY|HOW|RSN|REASON|PARENT|NEITR|NETR"
KID = r"^(# ?(CHILDREN|CHILDRN|KIDS) IN (FU|FAMILY UNIT)|NUMBER OF CHILDREN)$"
NEW = {"earnings": ["lpl"], "assets": ["s_asset", "own"], "transfers": ["s_tr", "welf"], "others": ["s_oth"],
       "family size": ["nkid"], "parents' schooling": ["f_ed", "m_ed"]}
NLAB = {"earnings": "LABOUR EARNINGS beyond the components", "assets": "ASSETS (asset income share, home ownership)",
        "transfers": "TRANSFERS (transfer share, AFDC / TANF years)", "others": "OTHER MEMBERS' income share",
        "family size": "FAMILY SIZE (children in the unit)", "parents' schooling": "PARENTS' SCHOOLING"}
YS = [("V", ["ly", "lw", "lh"]), ("E", ["emp"]), ("F", ["lfam"])]
RES = {}


def fam_items():
    """family-level items by (wave, int), nominal, waves 1968-2011; also the list of items found."""
    if FCACHE.exists():
        return pd.read_pickle(FCACHE)
    rows, found = [], []
    for w, finc in zip(P1.WAVES, P1.FAMINC):
        if w > 2011:
            break
        folder = P1.FAM / (f"fam{w}" if w < 1994 else f"fam{w}er")
        base = next(x for x in folder.glob("*.do") if "formats" not in x.name).with_suffix("")
        pos, labs = P1.layout(base.with_suffix(".do"))
        labs = [(v, l) for v, l in labs if v in pos]
        idv = labs[1][0]
        first = lambda p, no=None: next((v for v, l in labs if re.search(p, l) and not (no and re.search(no, l))),  # noqa
                                        None)
        it = {"tax": first(TAX), "tr": first(TRN), "own": first(OWN, OWN_NOT), "kid": first(KID)}
        it.update(HAND.get(w, {}))
        adc = [(v, "yes" if re.search(r"WHETHER|WTR|WTHR", l) else "amt") for v, l in labs
               if re.search(ADC, l) and not re.search(ADC_NOT, l)]
        cols = [idv, finc] + [v for v in it.values() if v] + [v for v, _ in adc]
        x = P1.read(base, list(dict.fromkeys(cols)), pos)
        o = pd.DataFrame({"wave": w, "int": x[idv], "faminc_n": x[finc]})
        for k, v in it.items():
            o[k] = x[v] if v else np.nan
        o["welf"] = np.nan
        if adc:
            yes = np.zeros(len(x), bool)
            for v, kind in adc:
                yes |= (x[v] == 1).to_numpy() if kind == "yes" else (x[v] > 0).to_numpy()
            o["welf"] = yes.astype(float)
        rows.append(o)
        found.append({"wave": w, **{k: v or "" for k, v in it.items()},
                      "adc": "; ".join(f"{v} ({next(l for vv, l in labs if vv == v)})" for v, _ in adc)})
        print(f"  {w}: {found[-1]}", flush=True)
    F = pd.concat(rows, ignore_index=True)
    out = (F, pd.DataFrame(found))
    pd.to_pickle(out, FCACHE)
    return out


def windows(r):
    """the son's window measures (wave-ages 13-19, family income in bounds; >= 3 years each)."""
    F, found = fam_items()
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    sons = r.drop_duplicates("pid")[["pid"]]
    k = py[py["child"] & py["age"].between(13, 19) & py["faminc"].between(R24.LO, R24.HI) & py["pid"].isin(sons["pid"])][
        ["pid", "wave", "int", "faminc", "hlab", "wlab"]]
    k = k.merge(F, on=["wave", "int"], how="left")
    fn = k["faminc_n"].where(k["faminc_n"] > 0)
    lab = k["hlab"].fillna(0).clip(lower=0) + k["wlab"].fillna(0).clip(lower=0)
    k["pl"] = lab
    s_lab = (lab / k["faminc"]).clip(0, 1)
    s_tax = (k["tax"] / fn).clip(0, 1)
    k["s_asset"] = (s_tax - s_lab).clip(0, 1)
    k["s_tr"] = (k["tr"] / fn).clip(0, 1)
    k["s_oth"] = (1 - s_tax - k["s_tr"]).clip(0, 1)
    k.loc[k["wave"] == 1968, "s_oth"] = np.nan              # 1968 transfers are the whole family's
    k["own"] = (k["own"] == 1).astype(float).where(k["own"].notna())
    k["nkid"] = k["kid"].where(k["kid"].between(0, 20))
    g = k.groupby("pid")
    W = pd.DataFrame(index=g.size().index)
    W["lpl"] = np.log(g["pl"].mean().where(g["pl"].mean() > 0))
    for v in ("s_asset", "s_tr", "s_oth", "own", "welf", "nkid"):
        W[v] = g[v].mean().where(g[v].count() >= 3)
    W.index.name = "pid"
    return W.reset_index(), found, k


def build():
    r = R75.build()
    W, found, k = windows(r)
    r = r.merge(W, on="pid", how="left")
    one = r.drop_duplicates("pid")
    nv = ["lpl", "s_asset", "s_tr", "s_oth", "own", "welf", "nkid"]
    r["inc_na"] = r[nv].isna().any(axis=1).astype(float)
    for v in nv:
        q = one[one[v].notna()]
        r[v] = r[v].fillna(float(np.average(q[v], weights=q["wt"])))
    for p, absent in (("f", "nofa"), ("m", "nomo")):         # mean fill (75's rule), not 74's 0 fill: absent
        ok = (r[f"{p}_educ_na"] == 0) & (r[absent] == 0)    # parents and present ones without schooling alike
        q = one[(one[f"{p}_educ_na"] == 0) & (one[absent] == 0)]
        r[f"{p}_ed"] = r[f"{p}_educ0"].where(ok, float(np.average(q[f"{p}_educ0"], weights=q["wt"])))
    return r, found, k


def run_all(d, BT):
    ga = dict(R75.GROUPS)
    gb = {**{g: v for g, v in R75.GROUPS.items() if g != "structure"}, **NEW,
          "structure": R75.GROUPS["structure"] + ["f_educ_na", "m_educ_na", "inc_na"]}
    out = {}
    for tag, ys in YS:
        base = {"V": d["lw"].notna(), "E": d["emp"].notna(), "F": d["lfam"].notna()}[tag]
        out[tag] = (run_spec(d[base], ys, ga, BT, cells=CELLS), run_spec(d[base], ys, gb, BT, cells=CELLS), ys)
    return out


def table(md, lab, out):
    rows_a = list(R75.GROUPS) + ["b"]
    rows_b = [g for g in R75.GROUPS if g != "structure"] + list(NEW) + ["structure", "b"]
    lab_all = {**R75.GLAB, **NLAB, "b": "rest"}
    md += [f"#### {lab}: contributions to the IGE (A = 75's split, B = with the other resources)", "",
           "| son's outcome | component | " + " | ".join(f"A {CLAB[k]}" if False else CLAB[k] for k in CELLS)
           + " | opening 45-49 - 25-29 | share 25-55 (A) | share 25-55 (B) |", "|---" * 9 + "|"]
    for tag in ("V", "E", "F"):
        ra, rb, ys = out[tag]
        for j, y in enumerate(ys):
            md.append(f"| **{R75.OL[y]}** | IGE (b0) | " + " | ".join(cc(est(rb, k, 'b0', j)) for k in CELLS)
                      + f" | {cc(est(rb, 'open', 'b0', j))} | | |")
            RES[f"{lab}|{y}|b0"] = [list(e[:2]) if e else None for e in [est(rb, k, "b0", j) for k in CELLS]]
            for gname in rows_b:
                stat = "b" if gname == "b" else f"c:{gname}"
                ent = [est(rb, k, stat, j) for k in CELLS] + [est(rb, "open", stat, j)]
                sa = est(ra, 6, stat, j, share=True) if gname in rows_a else None
                sb = est(rb, 6, stat, j, share=True)
                md.append(f"| {R75.OL[y]} | {lab_all[gname]} | " + " | ".join(cc(e) for e in ent)
                          + f" | {cc(sa)} | {cc(sb)} |")
                RES[f"{lab}|{y}|{gname}"] = {"B_contrib": [list(e[:2]) if e else None for e in ent],
                                            "A_share": list(sa[:2]) if sa else None, "B_share": list(sb[:2]) if sb else None}
        n = rb["n"]
        md.append(f"| N sons / son-years / families | {n[0]:,} / {n[1]:,} / {n[2]:,} | | | | | | |")
    md.append("")
    # elements of the new groups, ln earnings
    ra, rb, ys = out["V"]
    md += [f"#### {lab}: each new element, ln earnings (split B)", "", "| element | " + " | ".join(CLAB[k] for k in CELLS)
           + " |", "|---" * 5 + "|"]
    for kk, col in enumerate(rb["cols"]):
        if col in [v for g in NEW.values() for v in g]:
            ent = [est(rb, k, f"e:{kk}", 0) for k in CELLS]
            md.append(f"| {col} | " + " | ".join(cc(e) for e in ent) + " |")
            RES[f"{lab}|element|{col}"] = [list(e[:2]) if e else None for e in ent]
    md.append("")


def main():
    t0 = time.time()
    r, found, k = build()
    md = ["# What is in the rest: parental income at equal components", "",
          "Built by `80.WhatIsPassedOnRest.py` (2026-10-20); definitions in its docstring. Follows "
          "`75.WhatIsPassedOn.py` (EVIDENCE 11.29). PSID sons 25-55, PSID weights; exact Gelbach split of the IGE on ln "
          f"parental income; {R74.NBOOT} cluster-bootstrap draws of 1968 families (stratified by race); estimate (s.e.; "
          "p), *** p<0.01, ** p<0.05, * p<0.1. Split A = 75's groups; split B adds the parents' other resources. b0 = sum "
          "of all rows exactly. **Descriptive accounting.**", ""]
    one = r.drop_duplicates("pid")
    wa = lambda q, v: np.average(q[v], weights=q["wt"])  # noqa: E731
    md += ["## 0. The other resources (weighted means over sons, window ages 13-19)", "",
           "| sample | sons | ln parents' labour income | asset share | transfer share | others' share | home owner | "
           "AFDC/TANF years | children in unit | father's schooling | mother's schooling | measures missing |",
           "|---" * 12 + "|"]
    for lab, s in (("pooled", one), ("White", one[one.race == "White"]), ("Black", one[one.race == "Black"])):
        fe, me = s[(s.f_educ_na == 0) & (s.nofa == 0)], s[(s.m_educ_na == 0) & (s.nomo == 0)]
        md.append(f"| {lab} | {len(s):,} | {wa(s, 'lpl'):.3f} | {wa(s, 's_asset'):.3f} | {wa(s, 's_tr'):.3f} | "
                  f"{wa(s, 's_oth'):.3f} | {wa(s, 'own'):.3f} | {wa(s, 'welf'):.3f} | {wa(s, 'nkid'):.2f} | "
                  f"{wa(fe, 'f_ed'):.2f} | {wa(me, 'm_ed'):.2f} | {wa(s, 'inc_na'):.3f} |")
    md += ["", "Gradients in ln parental income (weighted OLS of each window measure on lyp, one row per son):", "",
           "| sample | " + " | ".join(v for g in NEW.values() for v in g) + " |", "|---" * 10 + "|"]
    for lab, s in (("pooled", one), ("White", one[one.race == "White"]), ("Black", one[one.race == "Black"])):
        cells = []
        for v in [v for g in NEW.values() for v in g]:
            q = s if v not in ("f_ed", "m_ed") else s[(s[f"{v[0]}_educ_na"] == 0) & (s["nofa" if v[0] == "f" else "nomo"] == 0)]
            o = R74.wreg(q.assign(age=0), v, ["lyp"], age_dummies=False)
            cells.append(R74.c(o[0]["lyp"]))
        md.append(f"| {lab} | " + " | ".join(cells) + " |")
    md.append("")
    for lab, d in (("pooled", r), ("White", r[r.race == "White"]), ("Black", r[r.race == "Black"])):
        print(f"{lab} ...", flush=True)
        BT = Boot(d["fam68"].to_numpy(), d["race"].to_numpy(), seed=R74.SEED + (0 if lab == "pooled" else 11))
        md += [f"## {lab}", ""]
        table(md, lab, run_all(d, BT))
        print(f"  {lab} done {time.time() - t0:.0f}s", flush=True)
    md += ["## Family-file items used, by wave", "", "| wave | taxable H+W | transfers H+W | own / rent | children in FU |"
           " ADC / AFDC / TANF items |", "|---" * 6 + "|"]
    for _, f in found.iterrows():
        md.append(f"| {f['wave']} | {f['tax']} | {f['tr']} | {f['own']} | {f['kid']} | {f['adc']} |")
    (OUT / "what_is_passed_on_rest.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "what_is_passed_on_rest.json", "w"), indent=1, default=str)
    print(f"done {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
