r"""Layoffs of mothers who head their families, by the child's age (committee memo H5, 2026-10-24)

The layoff analysis follows fathers, so single-mother families - the main recipients of AFDC, Food Stamps and the
EITC - are out of it. The PSID asks female heads the same job-end questions as male heads (19.FatherDisplacement.py's
reports(), head items of either sex).
MOTHERS' LAYOFFS: 19's head reports of a job end for female heads, with 19's definitions (layoff = laid off / fired;
  closure = company folded / moved / went out of business) and dating and de-duplication rules.
CHILDREN: sons and daughters of 24's children (24's frames: own earnings at 25-55 as head or wife, valid years), whose
  family unit was headed by a woman in at least three of their window waves at 13-19 (parental income in bounds).
  Mother's layoff share = share of those waves with a layoff record dated to the income year or the year before (75's
  matching); closure share likewise.
DESIGN (PSID weights; clusters 1968 family): by band 25-29 and 40-44 (45-49 is thin), ln earnings and ln wage on the
  layoff share, the closure share, ln parental income, female and single-age dummies; the change from one stacked
  regression; within child: layoff share x (age-40)/10 with person FE, lyp x age, closure x age, female x age and 5-year
  cohort x age. All children and by sex. Counts of treated children by band.
Writes output/mother_layoffs.md / .json (aggregates only); caches data/female_head_displacement.pkl (person-level,
not in git). DESCRIPTIVE.
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


R19 = _load("s19", "19.FatherDisplacement.py")
R101 = _load("s101", "101.EITCByAge.py")
R24 = R101.R75.R24
c, ols, dummies = R101.c, R101.ols, R101.dummies
CACHE = DATA / "female_head_displacement.pkl"
RES = {}


def female_displacement(py):
    if CACHE.exists():
        return pd.read_pickle(CACHE)
    fam = R19.psid9.family()
    r = R19.reports(fam)
    hd = py[py["head"] & (py["female"] == 1)][["wave", "int", "pid"]].drop_duplicates(["wave", "int"])
    r = r.merge(hd, on=["wave", "int"], how="inner")
    r["year"] = r["year"].astype(int)
    rows = []
    for k in ("layoff", "strict"):
        x = r[r[k]].sort_values(["pid", "year", "dated"], ascending=[True, True, False]).drop_duplicates(["pid", "year"])
        prev = set(zip(x["pid"], x["year"] + 1))
        drop = (~x["dated"]) & pd.Series([(p, y) in prev for p, y in zip(x["pid"], x["year"])], index=x.index)
        rows.append(x[~drop][["pid", "year"]].assign(**{k: 1}))
    d = rows[0].merge(rows[1], on=["pid", "year"], how="outer").fillna(0)
    d.to_pickle(CACHE)
    return d


def main():
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    D = female_displacement(py)
    lay = set(zip(D.loc[D["layoff"] == 1, "pid"], D.loc[D["layoff"] == 1, "year"]))
    clo = set(zip(D.loc[D["strict"] == 1, "pid"], D.loc[D["strict"] == 1, "year"]))
    a, py24, ch = R24.load()
    wt = a[["pid", "wave", "wt"]].drop_duplicates(["pid", "wave"])
    parts = []
    for female in (0, 1):
        r, _ = R24.frames(a, ch, female)
        r = r.merge(wt, on=["pid", "wave"], how="left")
        r["female"] = float(female)
        parts.append(r[r["wt"] > 0])
    r = pd.concat(parts, ignore_index=True)
    kids = r.drop_duplicates("pid")[["pid"]]
    k = py[py["child"] & py["age"].between(13, 19) & py["faminc"].between(R24.LO, R24.HI) & py["pid"].isin(kids["pid"])][
        ["pid", "wave", "int"]]
    fh = py[py["head"] & (py["female"] == 1)][["wave", "int", "pid"]].rename(columns={"pid": "mpid"}).drop_duplicates(
        ["wave", "int"])
    fw = k.merge(fh, on=["wave", "int"], how="inner")
    y = fw["wave"] - 1
    fw["lay"] = [float((p, t) in lay or (p, t - 1) in lay) for p, t in zip(fw["mpid"], y)]
    fw["clo"] = [float((p, t) in clo or (p, t - 1) in clo) for p, t in zip(fw["mpid"], y)]
    g = fw.groupby("pid")
    M = pd.DataFrame({"m_lay": g["lay"].mean(), "m_clo": g["clo"].mean(), "m_n": g.size()})
    M = M[M["m_n"] >= 3]
    r = r.merge(M, left_on="pid", right_index=True, how="inner")
    r["band"] = pd.cut(r["age"], [24, 29, 34, 39, 44, 49, 55], labels=False)
    r["agec"] = (r["age"] - 40) / 10
    r["coh5"] = (r["birth_year"] // 5 * 5).astype(int)
    one = r.drop_duplicates("pid")
    md = ["# Layoffs of mothers who head their families, by the child's age (committee memo H5)", "",
          "Built by `131.MotherLayoffs.py` (2026-10-24); design in its docstring. Per unit share of the child's teen "
          "waves with a layoff of the mother as head; s.e. clustered by 1968 family; *** p<0.01, ** p<0.05, * p<0.1. "
          "**Descriptive.**", "",
          f"Children of mother-headed families (>= 3 teen waves): {len(one):,} ({int((one['female'] == 0).sum()):,} sons, "
          f"{int((one['female'] == 1).sum()):,} daughters); with a teen layoff year {int((one['m_lay'] > 0).sum()):,}; "
          f"mean layoff share {one['m_lay'].mean():.3f}; mean closure share {one['m_clo'].mean():.3f}; Black "
          f"{(one['race'] == 'Black').mean():.3f}.", ""]
    md += ["| sample | outcome | 25-29 | 40-44 | change | within child x age | treated at 25-29 / 40-44 | children |",
           "|---" * 8 + "|"]
    for slab, q0 in (("all children", r), ("sons", r[r["female"] == 0]), ("daughters", r[r["female"] == 1])):
        for y_ in ("ly", "lw"):
            d = q0.dropna(subset=[y_, "lyp"])
            X0 = ["m_lay", "m_clo", "lyp"] + (["female"] if slab == "all children" else [])
            cells = []
            for kb in (0, 3):
                q = d[d["band"] == kb]
                X = np.column_stack([q[X0].to_numpy(float), dummies(q["age"]), np.ones(len(q))])
                b, V = ols(X, q[y_].to_numpy(float), q["wt"].to_numpy(float), q["fam68"].to_numpy())
                cells.append((b[0], np.sqrt(V[0, 0])))
            s = d[d["band"].isin([0, 3])]
            b3 = (s["band"] == 3).to_numpy(float)
            base = np.column_stack([s[X0].to_numpy(float), dummies(s["age"]), np.ones(len(s))])
            b, V = ols(np.column_stack([base, base * b3[:, None]]), s[y_].to_numpy(float), s["wt"].to_numpy(float),
                       s["fam68"].to_numpy())
            K = base.shape[1]
            ch_ = (b[K], np.sqrt(V[K, K]))
            aa = d["agec"].to_numpy()[:, None]
            Xf = np.column_stack([d[X0].to_numpy(float) * aa, dummies(d["coh5"]) * aa, dummies(d["age"])])
            bf, Vf = ols(Xf, d[y_].to_numpy(float), d["wt"].to_numpy(float), d["fam68"].to_numpy(),
                         absorb=d["pid"].to_numpy())
            fe = (bf[0], np.sqrt(Vf[0, 0]))
            t = [int(d[(d["band"] == kb) & (d["m_lay"] > 0)]["pid"].nunique()) for kb in (0, 3)]
            md.append(f"| {slab} | {y_} | {c(cells[0])} | {c(cells[1])} | {c(ch_)} | {c(fe)} | {t[0]} / {t[1]} | "
                      f"{d['pid'].nunique():,} |")
            RES[f"{slab}|{y_}"] = {"a": list(map(float, cells[0])), "b": list(map(float, cells[1])),
                                   "ch": list(map(float, ch_)), "fe": list(map(float, fe)), "treated": t,
                                   "n": int(d["pid"].nunique())}
            print(md[-1], flush=True)
    md.append("")
    (OUT / "mother_layoffs.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "mother_layoffs.json", "w"), indent=1, default=float)
    print("\n".join(md))


if __name__ == "__main__":
    main()
