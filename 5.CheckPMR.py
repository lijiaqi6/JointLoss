r"""Check against Palomino, Marrero and Rodriguez (2018, J Econ Inequal 16: 347-367), PSID (2026-10-16).

Their design (Sections 2-3; Literature/s10888-017-9372-8.pdf), rebuilt from data/psid_person_year.pkl:
  sons (PSID core = SRC + SEO) observed as household head at 25-65 in income years 1980-2010 (one row per son-year);
  outcome ln total family income of the son's household (Lee and Solon 2009 pooled design);
  parents: ln of mean total family income while the son is 13-19 and living as the head's child (>= 3 years);
  parent's (head's) age when the son is 16 between 30 and 70;
  yearly incomes below $100 or above $150,000 in 1967 dollars dropped (parents and sons);
  eq. (2): quartics in the parent's age A and in C = son's age - 40, and ln y_p x C^n (n = 1..4), so beta is the
  IGE at age 40; s.e. clustered by son. Eq. (4) adds the son's years of education, eq. (5) also a White dummy.
Their OLS: 0.473 (0.018), N = 25,084 son-years / 3,088 sons; + education 0.343; + education and race 0.295.
QR at the 10/25/50/75/90th: 0.645, 0.526, 0.440, 0.398, 0.476.
Writes output/pmr_check.csv; prints the comparison, then the same regression for Black and White sons separately.
"""
import re
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

from common import DATA, OUT, CPI, fmt
import os
DROPBOX = Path(os.environ.get("DROPBOX", Path.home() / "Dropbox"))   # raw data, read only

IND = Path(DROPBOX / "PSID/Individual/ind2023er/IND2023ER")
LO, HI = (v * CPI[2000] / CPI[1967] for v in (100, 150_000))           # 1967 dollars -> 2000 dollars
PAPER = {"OLS": 0.473, "OLS + education": 0.343, "OLS + education + race": 0.295,
         "QR 0.10": 0.645, "QR 0.25": 0.526, "QR 0.50": 0.440, "QR 0.75": 0.398, "QR 0.90": 0.476}


def education():
    """years of completed education (1-17): the highest report in the 1985+ waves."""
    t = IND.with_suffix(".do").read_text(encoding="latin-1")
    block = re.search(r"\binfix\b(.*?)\busing\b", t, re.S).group(1)
    pos = {v: (int(a) - 1, int(b)) for v, a, b in
           re.findall(r"(?:long\s+)?([A-Z]+\d+[A-Z]?)\s+(\d+)\s*-\s*(\d+)", block)}
    cols = []
    for v, l in re.findall(r'label variable\s+(\S+)\s+"(.*)"', t):
        m = re.match(r"(YEARS |YRS )?COMPLETED EDUCATION\s+(\d\d)$", l.strip())
        if m and (int(m.group(2)) >= 85 or int(m.group(2)) < 68):
            cols.append(v)
    d = pd.read_fwf(IND.with_suffix(".txt"), colspecs=[pos[c] for c in ["ER30001", "ER30002"] + cols],
                    names=["ER30001", "ER30002"] + cols, header=None)
    e = d[cols].where((d[cols] >= 1) & (d[cols] <= 17)).max(axis=1)
    return pd.Series(e.values, index=d.ER30001 * 1000 + d.ER30002, name="edu")


def build():
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    py["year"] = py["wave"] - 1                                          # income year
    ok = py["faminc"].between(LO, HI)
    # parents: son 13-19 living as the head's child
    k = py[py["child"] & py["age"].between(13, 19) & ok]
    g = k.groupby("pid")
    par = pd.DataFrame({"yp": g["faminc"].mean(), "np": g["faminc"].count()})
    k16 = k.assign(dist=(k["age"] - 16).abs()).sort_values(["pid", "dist"]).groupby("pid").first()
    par["A"] = k16["hage"]
    par = par[(par["np"] >= 3) & par["A"].between(30, 70)]
    # sons: male heads at 25-65, income years 1980-2010
    s = py[(py["female"] == 0) & py["head"] & py["age"].between(25, 65) & py["year"].between(1980, 2010) & ok]
    s = s.join(par, on="pid", how="inner").join(education(), on="pid")
    s["lys"], s["lyp"], s["C"] = np.log(s["faminc"]), np.log(s["yp"]), s["age"] - 40
    s["white"] = (s["hrace"] == "White") * 1
    s = s.merge(py[["pid", "wave", "wt"]].rename(columns={"wt": "wt_obs"}), on=["pid", "wave"], how="left")
    # polynomials in (A - 45) / 10 and C / 10: same beta (the IGE at C = 0), but QR converges
    for n in range(1, 5):
        s[f"A{n}"], s[f"C{n}"] = ((s["A"] - 45) / 10) ** n, (s["C"] / 10) ** n
        s[f"lypC{n}"] = s["lyp"] * s[f"C{n}"]
    return s


def X(s, extra=()):
    cols = ["lyp"] + [f"{v}{n}" for v in ("A", "C", "lypC") for n in range(1, 5)] + list(extra)
    return sm.add_constant(s[cols].astype(float))


def main():
    s = build()
    rows = []
    for lab, extra, d in (("OLS", (), s), ("OLS + education", ("edu",), s.dropna(subset=["edu"])),
                          ("OLS + education + race", ("edu", "white"), s.dropna(subset=["edu"]))):
        r = sm.OLS(d["lys"], X(d, extra)).fit(cov_type="cluster", cov_kwds={"groups": d["pid"]})
        rows.append(dict(spec=lab, sample="All sons", beta=r.params["lyp"], se=r.bse["lyp"], p=r.pvalues["lyp"],
                         n=int(r.nobs), sons=d["pid"].nunique(), paper=PAPER[lab]))
    for lab, d, w in (("OLS, SRC only", s[s["fam68"] <= 2930], None),
                      ("OLS, weighted (core longitudinal weight)", s[s["wt_obs"] > 0], "wt_obs")):
        mod = sm.WLS(d["lys"], X(d), weights=d[w]) if w else sm.OLS(d["lys"], X(d))
        r = mod.fit(cov_type="cluster", cov_kwds={"groups": d["pid"]})
        rows.append(dict(spec=lab, sample="All sons", beta=r.params["lyp"], se=r.bse["lyp"], p=r.pvalues["lyp"],
                         n=int(r.nobs), sons=d["pid"].nunique(), paper=PAPER["OLS"]))
    for q in (0.10, 0.25, 0.50, 0.75, 0.90):
        r = sm.QuantReg(s["lys"], X(s)).fit(q=q, max_iter=20000, p_tol=1e-6)
        rows.append(dict(spec=f"QR {q:.2f}", sample="All sons", beta=r.params["lyp"], se=np.nan, p=np.nan,
                         n=len(s), sons=s["pid"].nunique(), paper=PAPER[f"QR {q:.2f}"]))
    for race in ("Black", "White"):
        d = s[s["hrace"] == race]
        r = sm.OLS(d["lys"], X(d)).fit(cov_type="cluster", cov_kwds={"groups": d["pid"]})
        rows.append(dict(spec="OLS", sample=f"{race} sons", beta=r.params["lyp"], se=r.bse["lyp"],
                         p=r.pvalues["lyp"], n=int(r.nobs), sons=d["pid"].nunique(), paper=np.nan))
    res = pd.DataFrame(rows)
    OUT.mkdir(exist_ok=True)
    res.to_csv(OUT / "pmr_check.csv", index=False)
    res["ours"] = [fmt(b, se, p) if se == se else f"{b:.3f}" for b, se, p in zip(res.beta, res.se, res.p)]
    print(res[["sample", "spec", "ours", "paper", "n", "sons"]].to_string(index=False))
    print(s.groupby("year").agg(obs=("pid", "size"), age=("age", "mean"), lys=("lys", "mean"),
                                A=("A", "mean"), lyp=("lyp", "mean"),
                                white=("white", "mean")).round(2).iloc[::3].to_string())


if __name__ == "__main__":
    main()
