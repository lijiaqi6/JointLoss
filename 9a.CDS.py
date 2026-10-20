r"""PSID Child Development Supplement: Woodcock-Johnson scores and the Behavior Problems Index (2026-10-17).

Reads the CDS files extracted (data only; the Stata .do layouts are parsed as text) from the zips in
Dropbox/PSID/CDS into data/cds/<wave>/ and writes data/cds_scores.pkl: one row per child x CDS wave with
    pid          child ER30001*1000 + ER30002, from the cumulative CDS ID map (CDSIND9724: CDSCUMID68, CDSCUMPN),
                 matched on the core family interview number and sequence number each CDS file is keyed by
                 (CRFIDyy, CRSNyy; 1997 core IW for CDS-1997, 2001 for CDS-2002, 2007, 2013 for CDS-2014, 2019)
    wave         CDS year (1997, 2002, 2007, 2014, 2019; CDS-2020/2021/2024 have no WJ assessment and no BPI)
    age_m, age   child age at the assessment in months / completed years (age: at the PCG interview if the child
                 has no assessment - 1997 AGEATPCG months, 2002 Q21IWAGE, 2007 Q31IWAGE, 2014 P14AGEX, 2019 P19AGEX)
    lw, ap, pc   WJ standard scores: Letter-Word identification, Applied Problems, Passage Comprehension
    br, bm       WJ Broad Reading, Broad Math standard scores where the release has them (bm: 2019 only)
    bpi, bpi_z   Behavior Problems Index total (count of problem behaviours reported by the PCG) and its z-score
                 within wave x age (the item count differs across waves, so bpi_z is the comparable measure)
    pcg_pid, pcg_rel, pcg_biomom   primary caregiver's person id, relation to the child (1 biological mother,
                 2 stepmother, 3 adoptive mother, 4 biological father, ..., 7 grandmother; same codes 1997-2019),
                 and an indicator for the biological mother
    wt           CDS child-level weight of the wave; wt_n = wt / its wave mean (2014+ weights are population
                 scaled, 1997-2007 ones are not)
Variables per wave (labels differ):
  1997 CHILD97 (CHLDID97, CHLDSN97): Q3LW_SS, Q3AP_SS, Q3PC_SS, Q3BRE_SS (Q3BMA_SS "broad math" is not used: it
       equals Q3AP_SS for 79% of children and correlates 1.00 with it); DEMOG1997: AGEATCH (months at
       the child interview, where the WJ-R was given), RELPCG97, CH97PRWT; PCG97_CHLD: BPI_T97 (0-27)
  2002 ASSESSMT (ASMTID01, ASMTSN01): Q24LWSS, Q24APSS, Q24PCSS, Q24BRSS, Q24IWAGE; DEMOG: RELPCG02, CH02PRWT;
       PCG_CHLD: BPI_T02 (0-32)
  2007 ASSESS07 (ASMID07, ASMSN07): Q34LWSS, Q34APSS, Q34PCSS, Q34BRSS, Q34IWAGE; DEMOG07: RELPCG07, CH07PRWT;
       PCG_CHILD07: BPI_T07 (0-32)
  2014 ASSESS14 (A14YRID, A14CYPSN): A14LWSS, A14APSS, A14PCSS, A14BRSS, A14IWAGE (A14MRSS duplicates A14APSS,
       not used); DEMOG14: X14PCGRLSP, X14CHWGT; PCGCHILD14: P14BPI_T (27 items, age 3+)
  2019 ASSESS2019 (A19YRID, A19CYPSN): A19LWSS, A19APSS, A19PCSS, A19BRSS, A19MRSS (Mathematics = AP + Calculation,
       used as broad math), A19IWAGE; DEMOG2019: X19PCGRLSP, X19CHWGT; PCGCHILD2019: P19BPI_T27 (27 items, age 3+)
Missing codes: standard scores outside 1-300 (999 NA, 995/996 z beyond +-4 in 2019, 0 inap.) -> NaN; BPI 97/99 -> NaN.
The WJ edition changes (WJ-R 1997-2007, WJ-III 2014, WJ-IV 2019), so scores are compared within wave or with wave FE.
"""
import re
from pathlib import Path

import numpy as np
import pandas as pd

from common import DATA

CDS = DATA / "cds"
INFIX = re.compile(r"(?:long\s+|str\d*\s+|double\s+)?([A-Z][A-Z0-9_]*)\s+(\d+)\s*-\s*(\d+)")

# wave: (folder, [(file, id, seq, {our name: variable})])
SPEC = {
    1997: [("CHILD97", "CHLDID97", "CHLDSN97",
            dict(lw="Q3LW_SS", ap="Q3AP_SS", pc="Q3PC_SS", br="Q3BRE_SS")),
           ("DEMOG1997", "DEMID97", "DEMSN97", dict(age_m="AGEATCH", agep_m="AGEATPCG", pcg_rel="RELPCG97", wt="CH97PRWT")),
           ("PCG97_CHLD", "PCGCHID97", "PCGCHSN97", dict(bpi="BPI_T97"))],
    2002: [("ASSESSMT", "ASMTID01", "ASMTSN01",
            dict(lw="Q24LWSS", ap="Q24APSS", pc="Q24PCSS", br="Q24BRSS", age_m="Q24IWAGE")),
           ("DEMOG", "DEMID01", "DEMSN01", dict(pcg_rel="RELPCG02", wt="CH02PRWT")),
           ("PCG_CHLD", "PCHID01", "PCHSN01", dict(bpi="BPI_T02", agep="Q21IWAGE"))],
    2007: [("ASSESS07", "ASMID07", "ASMSN07",
            dict(lw="Q34LWSS", ap="Q34APSS", pc="Q34PCSS", br="Q34BRSS", age_m="Q34IWAGE")),
           ("DEMOG07", "DEMID07", "DEMSN07", dict(pcg_rel="RELPCG07", wt="CH07PRWT")),
           ("PCG_CHILD07", "PCHID07", "PCHSN07", dict(bpi="BPI_T07", agep="Q31IWAGE"))],
    2014: [("ASSESS14", "A14YRID", "A14CYPSN",
            dict(lw="A14LWSS", ap="A14APSS", pc="A14PCSS", br="A14BRSS", age_m="A14IWAGE")),
           ("DEMOG14", "X14YRID", "X14CYPSN", dict(pcg_rel="X14PCGRLSP", wt="X14CHWGT")),
           ("PCGCHILD14", "P14YRID", "P14CYPSN", dict(bpi="P14BPI_T", agep="P14AGEX"))],
    2019: [("ASSESS2019", "A19YRID", "A19CYPSN",
            dict(lw="A19LWSS", ap="A19APSS", pc="A19PCSS", br="A19BRSS", bm="A19MRSS", age_m="A19IWAGE")),
           ("DEMOG2019", "X19YRID", "X19CYPSN", dict(pcg_rel="X19PCGRLSP", wt="X19CHWGT")),
           ("PCGCHILD2019", "P19YRID", "P19CYPSN", dict(bpi="P19BPI_T27", agep="P19AGEX"))],
}
SCORES = ["lw", "ap", "pc", "br", "bm"]


def layout(do):
    t = do.read_text(encoding="latin-1")
    block = re.search(r"\binfix\b(.*?)\busing\b", t, re.S).group(1)
    return {v: (int(a) - 1, int(b)) for v, a, b in INFIX.findall(block)}


def read(folder, name, cols):
    pos = layout(folder / f"{name}.do")
    missing = [c for c in cols if c not in pos]
    assert not missing, (name, missing)
    return pd.read_fwf(folder / f"{name}.txt", colspecs=[pos[c] for c in cols], names=cols, header=None,
                       encoding="latin-1")


def idmap():
    """Cumulative CDS ID map: (wave, core IW, core seq) -> child pid, PCG pid."""
    yy = {1997: "97", 2002: "02", 2007: "07", 2014: "14", 2019: "19"}
    cols = ["CDSCUMID68", "CDSCUMPN"] + [f"{p}{y}" for y in yy.values()
                                         for p in ("CRFID", "CRSN", "ID68PCG", "PNPCG", "CDSTYPE")]
    m = read(CDS / "2024", "CDSIND9724", cols)
    out = []
    for w, y in yy.items():
        x = pd.DataFrame({"wave": w, "fid": m[f"CRFID{y}"], "sn": m[f"CRSN{y}"],
                          "pid": m.CDSCUMID68 * 1000 + m.CDSCUMPN,
                          "pcg_pid": (m[f"ID68PCG{y}"] * 1000 + m[f"PNPCG{y}"]).where(m[f"ID68PCG{y}"] > 0),
                          "type": m[f"CDSTYPE{y}"]})
        out.append(x[(x.fid > 0) & (x.sn > 0)])
    out = pd.concat(out, ignore_index=True)
    # one child record per (wave, fid, sn): caregivers have no PCG id; prefer the child row
    out = out.sort_values("pcg_pid", na_position="last").drop_duplicates(["wave", "fid", "sn"])
    return out


def main():
    ids = idmap()
    rows = []
    for w, files in SPEC.items():
        d = None
        for name, fid, sn, vars_ in files:
            f = read(CDS / str(w), name, [fid, sn, *vars_.values()])
            f = f.rename(columns={fid: "fid", sn: "sn", **{v: k for k, v in vars_.items()}})
            assert not f.duplicated(["fid", "sn"]).any(), name
            d = f if d is None else d.merge(f, on=["fid", "sn"], how="outer")
        d["wave"] = w
        n0 = len(d)
        d = d.merge(ids, on=["wave", "fid", "sn"], how="left", validate="1:1")
        print(f"CDS {w}: {n0} child records, {d.pid.notna().sum()} matched to a PSID pid", flush=True)
        rows.append(d)
    d = pd.concat(rows, ignore_index=True)
    d = d[d.pid.notna()].copy()
    d["pid"] = d.pid.astype("int64")
    for c in SCORES:
        d[c] = d[c].where(d[c].between(1, 300))
    d["bpi"] = d["bpi"].where(d["bpi"].between(0, 40))
    d["age_m"] = d["age_m"].where(d["age_m"].between(1, 400))
    # completed years at the assessment; children without one (BPI only): age at the PCG interview
    agep = np.floor(d["agep"].where(d["agep"].between(0, 25))) if "agep" in d else np.nan
    agep = pd.Series(agep, index=d.index).fillna(np.floor(d["agep_m"].where(d["agep_m"].between(1, 400)) / 12))
    d["age"] = np.floor(d["age_m"] / 12).fillna(agep)
    d["pcg_rel"] = d["pcg_rel"].where(d["pcg_rel"].between(1, 30))
    d["pcg_biomom"] = (d["pcg_rel"] == 1).astype(float).where(d["pcg_rel"].notna())
    d["wt"] = d["wt"].where(d["wt"] > 0)
    d["wt_n"] = d["wt"] / d.groupby("wave")["wt"].transform("mean")
    g = d.groupby(["wave", "age"])["bpi"]
    d["bpi_z"] = (d["bpi"] - g.transform("mean")) / g.transform("std")
    # children with no assessment and no BPI carry nothing for this file
    d = d[d[SCORES + ["bpi"]].notna().any(axis=1)]
    d = d[["pid", "wave", "age_m", "age", *SCORES, "bpi", "bpi_z", "pcg_pid", "pcg_rel", "pcg_biomom", "wt",
           "wt_n", "fid", "sn"]].sort_values(["pid", "wave"]).reset_index(drop=True)
    assert not d.duplicated(["pid", "wave"]).any()
    d.to_pickle(DATA / "cds_scores.pkl")

    # ---- sanity: standard scores ~ mean 100, sd 15 (weighted and unweighted)
    print(f"\nrows {len(d):,}; children {d.pid.nunique():,}")
    pd.set_option("display.width", 200)
    for c in SCORES + ["bpi"]:
        s = d.dropna(subset=[c])
        t = s.groupby("wave").apply(lambda x: pd.Series({
            "n": len(x), "mean": x[c].mean(), "sd": x[c].std(),
            "wmean": np.average(x[c], weights=x["wt"].fillna(0)) if x["wt"].fillna(0).sum() > 0 else np.nan,
            "age_lo": x["age"].min(), "age_hi": x["age"].max()}), include_groups=False)
        print(f"\n{c}\n{t.round(1)}")
    print("\nPCG relation (share biological mother) by wave:\n", d.groupby("wave")["pcg_biomom"].mean().round(3))


if __name__ == "__main__":
    main()
