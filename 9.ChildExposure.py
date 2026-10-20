r"""PSID children born 1968-2020: mother's work at the birth, father's job loss, parents' separation, family income
and welfare in early childhood (2026-10-17).

Reads the raw PSID files in Dropbox/PSID (read only) and IGE/data/psid_person_year.pkl (from 1.PSID.py); writes
IGE/data/psid_child_exposure.pkl, one row per child.

Children: (a) every childbirth record of the Childbirth and Adoption History 1985-2023 (Others/cah85_23; CAH2 = 1)
with a PSID person id for the child (CAH10/CAH11), birth year 1968-2020 (CAH15) and an SRC or SEO 1968 ID; mother and
father = the parent records of sex 2 / 1 (CAH3-CAH5); (b) other SRC + SEO persons born 1968-2020 seen as the head's
child or stepchild (rel 3/30/33/35): mother = the female head or the wife, father = the male head, of the family unit
in the first wave the child is seen in it. `src` says which.

Measures (calendar years; PSID income / hours questions refer to the year before the interview):
  mom_hrs0/1/2, mom_emp0/1/2  mother's annual hours (and hours > 0) in the birth year, +1, +2. Hours: head / wife total
        annual hours of the family file (the AGENTS.md variables), else for 1967-1992 the individual file's annual
        hours (any family member, e.g. a young mother in her parents' unit), else for 1997, 1999, 2001 the
        individual file's year-before-last weeks worked x hours per week (1999-2003 waves). From 1997 the biennial
        survey asks hours only for even years, so +1 is missing for even-year births after 2000 (and +0, +2 for
        odd-year births after 2001).
  fjl0, fjl0_n, fjl0_age1  father figure's job loss at ages 0-17: a year with zero annual hours after an observed
        year (the previous one, or two before in the biennial era) with hours > 0, same man. Father figure = the male
        head of the child's family unit that year (biological father, stepfather or the mother's partner); 0 when
        the child never lives with one (ff_years = 0). ff_bio = share of those years the head is the CAH father.
  fjl_u, fjl_u_age1  the same, also counting a year with head's hours unemployed > 0 after a year with hours > 0;
        unemployment hours exist only for 1967-1992 (family files 1968-1993), so fjl_u = fjl0 for later years.
        The "laid off / fired" reason for leaving the last job is not used (asked of a changing subset each era).
  div_mh  a marriage of the mother ended in separation or divorce (marriage history 1985-2023, Others/mh85_23:
        MH12 = 4 or 5, year = separation year MH16, else divorce year MH14) at child ages 0-17;
  div_rel the mother is the wife of a head in one wave and not the wife of that same head in the next wave she is
        observed, the head still alive (ER32050); dated the year before the later wave, ages 0-17;
  div = div_mh or div_rel; div_age1 the first such age.
  finc05, finc617  mean real (2000$) total family income of the child's family unit over income years at ages 0-5 /
        6-17 (lfinc05, lfinc617 = logs; n_inc05, n_inc617 = years behind them).
  afdc05, fs05, welf05  years at ages 0-5 with AFDC / TANF (head or wife), food stamps, either; welf05_obs = years
        observed (biennial era: food stamps also from the "2 years ago" item, TANF from "year before last" 2005-15).
        AFDC 1967 is the head's only; no food stamp item in the 1973 family file (income year 1972).
  race  head's race in the first family unit the child is seen in; mom_educ = mother's highest years of completed
        education reported in any wave (individual file), mom_educ_cat (<12, 12, 13-15, 16+); mom_age_birth;
        mom_married_birth (CAH8 = 1, else the mother is a wife in the child's first wave).
"""
import importlib.util
import re
from pathlib import Path

import numpy as np
import pandas as pd

from common import DATA, HERE

spec = importlib.util.spec_from_file_location("psid1", HERE / "1.PSID.py")
psid1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(psid1)
WAVES, FAM, IND, PSID, layout, read = psid1.WAVES, psid1.FAM, psid1.IND, psid1.PSID, psid1.layout, psid1.read
OTH = PSID / "Others"

# ---------------------------------------------------------------- family-file variables by wave
HH = ["V47", "V465", "V1138", "V1839", "V2439", "V3027", "V3423", "V3823", "V4332", "V5232", "V5731", "V6336", "V6934",
      "V7530", "V8228", "V8830", "V10037", "V11146", "V12545", "V13745", "V14835", "V16335", "V17744", "V19044",
      "V20344", "V21634", "ER4096", "ER6936", "ER9187", "ER12174", "ER16471", "ER20399", "ER24080", "ER27886",
      "ER40876", "ER46767", "ER52175", "ER57976", "ER65156", "ER71233", "ER77255", "ER81582", "ER85436"]
WH = ["V53", "V475", "V1148", "V1849", "V2449", "V3035", "V3431", "V3831", "V4344", "V5244", "V5743", "V6348", "V6946",
      "V7540", "V8238", "V8840", "V10131", "V11258", "V12657", "V13809", "V14865", "V16365", "V17774", "V19074",
      "V20374", "V21670", "ER4107", "ER6947", "ER9198", "ER12185", "ER16482", "ER20410", "ER24091", "ER27897",
      "ER40887", "ER46788", "ER52196", "ER57997", "ER65177", "ER71254", "ER77276", "ER81603", "ER85457"]
assert len(HH) == len(WH) == len(WAVES)
# head's hours unemployed, waves 1968-1993
HU = dict(zip(range(1968, 1994), ["V49", "V469", "V1142", "V1843", "V2443", "V3031", "V3427", "V3827", "V4338",
                                  "V5240", "V5739", "V6344", "V6942", "V7538", "V8236", "V8838", "V10045", "V11153",
                                  "V12552", "V13752", "V14842", "V16342", "V17751", "V19051", "V20351", "V21638"]))
# AFDC / TANF: amounts of head + wife (one var) or head, wife (two vars) through 1993; whether received from 1994
AFDC = {1968: ["V256"], 1969: ["V523"], 1970: ["V1209"], 1971: ["V1911"], 1972: ["V2512"], 1973: ["V3065"],
        1974: ["V3477"], 1975: ["V3877"], 1976: ["V4392"], 1977: ["V5303"], 1978: ["V5802"], 1979: ["V6413"],
        1980: ["V7003"], 1981: ["V7595"], 1982: ["V8288"], 1983: ["V8896"], 1984: ["V10282"], 1985: ["V11427"],
        1986: ["V12826", "V12847"], 1987: ["V13928", "V13949"], 1988: ["V14943", "V14964"],
        1989: ["V16443", "V16464"], 1990: ["V17859", "V17880"], 1991: ["V19159", "V19180"],
        1992: ["V20459", "V20480"], 1993: ["V21978", "V22252"],
        1994: ["ER3262", "ER3598"], 1995: ["ER6262", "ER6600"], 1996: ["ER8379", "ER8717"],
        1997: ["ER11272", "ER11599"], 1999: ["ER14538", "ER14865"], 2001: ["ER18697", "ER19046"],
        2003: ["ER22069", "ER22419"], 2005: ["ER26050", "ER26400"], 2007: ["ER37068", "ER37418"],
        2009: ["ER43059", "ER43409"], 2011: ["ER48381", "ER48734"], 2013: ["ER54059", "ER54429"],
        2015: ["ER61101", "ER61505"], 2017: ["ER67153", "ER67508"], 2019: ["ER73176", "ER73531"],
        2021: ["ER79272", "ER79652"], 2023: ["ER83247", "ER83621"]}
TANF_YBL = {2005: "ER27804", 2007: "ER40779", 2009: "ER46692", 2011: "ER52093", 2013: "ER57897", 2015: "ER65077"}
# food stamps last year: dollar value 1968-1975 (bonus / saved value), number of months 1976-1993, yes/no from 1994
FS = {1968: "V45", 1969: "V510", 1970: "V1183", 1971: "V1884", 1972: "V2478", 1974: "V3443", 1975: "V3851",
      1976: "V4367", 1977: "V5279", 1978: "V5778", 1979: "V6384", 1980: "V6978", 1981: "V7570", 1982: "V8262",
      1983: "V8870", 1984: "V10241", 1985: "V11381", 1986: "V12780", 1987: "V13882", 1988: "V14897",
      1989: "V16397", 1990: "V17813", 1991: "V19113", 1992: "V20413", 1993: "V21729",
      1994: "ER3059", 1995: "ER6058", 1996: "ER8155", 1997: "ER11049", 1999: "ER14255", 2001: "ER18386",
      2003: "ER21652", 2005: "ER25654", 2007: "ER36672", 2009: "ER42691", 2011: "ER48007", 2013: "ER53704",
      2015: "ER60719", 2017: "ER66766", 2019: "ER72770", 2021: "ER78847", 2023: "ER82840"}
FS_YBL = {1999: "ER14240", 2001: "ER18370", 2003: "ER21636", 2005: "ER25638", 2007: "ER36656", 2009: "ER42675",
          2011: "ER47991", 2013: "ER53703", 2015: "ER60718", 2017: "ER66765", 2019: "ER72769", 2021: "ER78846",
          2023: "ER82839"}

# individual file: annual hours worked (waves 1968-1993, everyone in the family unit), year-before-last weeks and
# hours per week (waves 1999-2003), education, year of death
IHRS = dict(zip(range(1968, 1994), ["ER30013", "ER30034", "ER30058", "ER30082", "ER30107", "ER30131", "ER30153",
                                    "ER30177", "ER30204", "ER30233", "ER30270", "ER30300", "ER30330", "ER30360",
                                    "ER30388", "ER30417", "ER30447", "ER30482", "ER30517", "ER30553", "ER30588",
                                    "ER30624", "ER30661", "ER30709", "ER30754", "ER30823"]))
YBL = {1999: ("ER33536C", "ER33536Q"), 2001: ("ER33627C", "ER33627Q"), 2003: ("ER33727C", "ER33727Q")}
EDU = re.compile(r"^(COMPLETED EDUC|YRS COMPLETED EDUC|YEARS COMPLETED EDUC)")


def yes(x):
    return (x == 1).astype(float).where(x.isin([1, 5]))


def family():
    out = []
    for i, w in enumerate(WAVES):
        folder = FAM / (f"fam{w}" if w < 1994 else f"fam{w}er")
        base = next(f for f in folder.glob("*.do") if "formats" not in f.name).with_suffix("")
        pos, labs = layout(base.with_suffix(".do"))
        idv = "V3" if w == 1968 else labs[1][0]
        extra = [c for c in [HU.get(w), *AFDC[w], TANF_YBL.get(w), FS.get(w), FS_YBL.get(w)] if c]
        f = read(base, [idv, HH[i], WH[i], *extra], pos)
        x = pd.DataFrame({"wave": w, "int": f[idv]})
        x["hh"] = f[HH[i]].where(f[HH[i]].between(0, 5840))
        x["wh"] = f[WH[i]].where(f[WH[i]].between(0, 5840))
        x["hu"] = f[HU[w]].where(f[HU[w]].between(0, 5840)) if w in HU else np.nan
        a = f[AFDC[w]]
        if w <= 1993:
            x["afdc"] = (a.where((a >= 0) & (a < 99999)).fillna(0).sum(axis=1) > 0).astype(float)
        else:
            x["afdc"] = pd.concat([yes(a[c]) for c in AFDC[w]], axis=1).max(axis=1)
        x["tanf_ybl"] = yes(f[TANF_YBL[w]]) if w in TANF_YBL else np.nan
        if w in FS:
            v = f[FS[w]]
            x["fs"] = ((v.where(v.between(0, 99998)) > 0).astype(float) if w <= 1975 else
                       (v.where(v.between(0, 12)) > 0).astype(float).where(v.between(0, 12)) if w <= 1993 else
                       yes(v))
        else:
            x["fs"] = np.nan
        x["fs_ybl"] = yes(f[FS_YBL[w]]) if w in FS_YBL else np.nan
        out.append(x)
    fam = pd.concat(out, ignore_index=True)
    print("family files: head hours > 0 / AFDC / food stamps by decade")
    print(fam.assign(dec=fam.wave // 10 * 10).groupby("dec")[["hh", "afdc", "fs"]].agg(
        lambda s: (s > 0).mean()).round(3))
    return fam


def individual():
    pos, labs = layout(IND.with_suffix(".do"))
    edu = [v for v, l in labs if EDU.match(l)]
    cols = ["ER30001", "ER30002", "ER32050", *IHRS.values(), *[c for p in YBL.values() for c in p], *edu]
    d = read(IND, cols, pos)
    d["pid"] = d.ER30001 * 1000 + d.ER30002
    e = d[edu].where((d[edu] >= 1) & (d[edu] <= 17))
    ind = pd.DataFrame({"pid": d.pid, "educ": e.max(axis=1),
                        "death_year": d.ER32050.where(d.ER32050.between(1968, 2025))})
    hrs = []
    for w, c in IHRS.items():
        hrs.append(pd.DataFrame({"pid": d.pid, "year": w - 1, "hrs_ind": d[c].where(d[c].between(0, 5840))}))
    hrs = pd.concat(hrs).dropna()
    ybl = []
    for w, (wk, hpw) in YBL.items():
        weeks = d[wk].where(d[wk].between(0, 52))
        h = d[hpw].where(d[hpw].between(0, 112))
        ybl.append(pd.DataFrame({"pid": d.pid, "year": w - 2, "hrs_ybl": np.where(weeks == 0, 0.0, weeks * h)}))
    ybl = pd.concat(ybl).dropna()
    return ind, hrs, ybl


def cah():
    pos, _ = layout(OTH / "cah85_23" / "CAH85_23.do")
    cols = ["CAH2", "CAH3", "CAH4", "CAH5", "CAH7", "CAH8", "CAH10", "CAH11", "CAH12", "CAH13", "CAH15"]
    c = read(OTH / "cah85_23" / "CAH85_23", cols, pos)
    c = c[(c.CAH2 == 1) & (c.CAH10 > 0) & (c.CAH10 < 9999) & c.CAH15.between(1968, 2020)]
    c = c[(c.CAH10 <= 2930) | c.CAH10.between(5001, 6872)]
    c = c.assign(pid=c.CAH10 * 1000 + c.CAH11, ppid=c.CAH3 * 1000 + c.CAH4)
    mom = c[c.CAH5 == 2].drop_duplicates("pid").set_index("pid")
    dad = c[c.CAH5 == 1].drop_duplicates("pid").set_index("pid")
    k = pd.DataFrame(index=pd.Index(sorted(set(mom.index) | set(dad.index)), name="pid"))
    k["mom_pid"] = mom["ppid"]
    k["dad_pid"] = dad["ppid"]
    b = mom[["CAH15", "CAH13", "CAH12", "CAH8", "CAH7"]].combine_first(dad[["CAH15", "CAH13", "CAH12"]])
    k["birth_year"] = b["CAH15"]
    k["birth_month"] = b["CAH13"].where(b["CAH13"].between(1, 12))
    k["female_cah"] = (b["CAH12"] == 2).astype(float).where(b["CAH12"].isin([1, 2]))
    k["mom_married_cah"] = (b["CAH8"] == 1).astype(float).where(b["CAH8"].between(1, 7))
    k["mom_byr_cah"] = b["CAH7"].where(b["CAH7"].between(1900, 2010))
    return k.reset_index()


def marriage():
    pos, _ = layout(OTH / "mh85_23" / "MH85_23.do")
    m = read(OTH / "mh85_23" / "MH85_23", ["MH2", "MH3", "MH12", "MH14", "MH16"], pos)
    m["pid"] = m.MH2 * 1000 + m.MH3
    m = m[m.MH12.isin([4, 5])]
    yr = m.MH16.where(m.MH16.between(1915, 2023)).fillna(m.MH14.where((m.MH12 == 4) & m.MH14.between(1915, 2023)))
    return pd.DataFrame({"pid": m.pid, "year": yr}).dropna()


def first_age(ev, kids, name):
    """ev: child pid, age of event. Adds ever (0-17), count, first age."""
    ev = ev[ev["age"].between(0, 17)]
    g = ev.groupby("pid")["age"]
    kids[name] = kids["pid"].map(g.size()).fillna(0).gt(0).astype(float)
    kids[name + "_n"] = kids["pid"].map(g.size()).fillna(0)
    kids[name + "_age1"] = kids["pid"].map(g.min())
    return kids


def main():
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    fam = family()
    ind, hrs_i, hrs_y = individual()
    py = py.merge(fam, on=["wave", "int"], how="left", validate="m:1")

    # ---- hours by person x calendar year
    # individual-file hours count only for person-waves in a family unit (0 = inap. otherwise)
    inf = py[["pid", "wave"]].drop_duplicates()
    hrs_i = hrs_i.merge(inf.assign(year=inf.wave - 1), on=["pid", "year"]).drop(columns="wave")
    hrs_y = hrs_y.merge(inf.assign(year=inf.wave - 2), on=["pid", "year"]).drop(columns="wave")
    hf = py[py["head"] | py["wife"]].assign(year=py["wave"] - 1)
    hf["hrs_fam"] = np.where(hf["head"], hf["hh"], hf["wh"])
    H = (hf[["pid", "year", "hrs_fam"]].dropna().drop_duplicates(["pid", "year"])
         .merge(hrs_i, on=["pid", "year"], how="outer").merge(hrs_y, on=["pid", "year"], how="outer"))
    H["hrs"] = H["hrs_fam"].fillna(H["hrs_ind"]).fillna(H["hrs_ybl"])
    both = H.dropna(subset=["hrs_fam", "hrs_ind"])
    print(f"family vs individual hours (heads/wives, 1967-1992): identical for {(both.hrs_fam == both.hrs_ind).mean():.3f}")
    H = H.dropna(subset=["hrs"]).set_index(["pid", "year"])["hrs"]

    # ---- the child universe
    k_cah = cah()
    ch = py[py["child"] & py["birth_year"].between(1968, 2020)].sort_values(["pid", "wave"])
    first = ch.groupby("pid").first()
    heads = py[py["head"]][["wave", "int", "pid", "female"]].rename(columns={"pid": "h_pid", "female": "h_fem"})
    wives = py[py["wife"]][["wave", "int", "pid"]].rename(columns={"pid": "w_pid"}).drop_duplicates(["wave", "int"])
    fu = heads.drop_duplicates(["wave", "int"]).merge(wives, on=["wave", "int"], how="left")
    first = first.reset_index().merge(fu, on=["wave", "int"], how="left")
    k_hh = pd.DataFrame({"pid": first["pid"], "birth_year": first["birth_year"],
                         "mom_pid": np.where(first["h_fem"] == 1, first["h_pid"], first["w_pid"]),
                         "dad_pid": np.where(first["h_fem"] == 0, first["h_pid"], np.nan)})
    k_hh = k_hh[~k_hh["pid"].isin(k_cah["pid"])]
    kids = pd.concat([k_cah.assign(src="cah"), k_hh.assign(src="hh")], ignore_index=True)
    # birth year: CAH, else the person-year file's (wave - reported birth year)
    pby = py.groupby("pid")["birth_year"].median()
    kids["birth_year"] = kids["birth_year"].fillna(kids["pid"].map(pby))
    sex = py.groupby("pid")["female"].first()
    kids["female"] = kids["pid"].map(sex).fillna(kids["female_cah"])
    kids["fam68"] = kids["pid"] // 1000
    print(f"children: {len(kids):,} (CAH {int((kids.src == 'cah').sum()):,}; head's child only "
          f"{int((kids.src == 'hh').sum()):,}); mother known {kids.mom_pid.notna().mean():.3f}, "
          f"father known {kids.dad_pid.notna().mean():.3f}")

    # child rows (any relation) with their family unit
    cr = py[py["pid"].isin(kids["pid"])][["pid", "wave", "int", "faminc", "hrace", "wt", "afdc", "fs", "fs_ybl",
                                          "tanf_ybl", "hu"]]
    cr = cr.merge(kids[["pid", "birth_year", "mom_pid", "dad_pid"]], on="pid").merge(fu, on=["wave", "int"],
                                                                                     how="left")
    cr["year"] = cr["wave"] - 1
    cr["age"] = cr["year"] - cr["birth_year"]
    cr = cr.sort_values(["pid", "wave"])

    # ---- race, weight, mother's characteristics
    f1 = cr.dropna(subset=["hrace"]).groupby("pid").first()
    kids["race"] = kids["pid"].map(f1["hrace"])
    kids["wt"] = kids["pid"].map(cr[cr.wt > 0].groupby("pid")["wt"].first())
    kids["mom_educ"] = kids["mom_pid"].map(ind.set_index("pid")["educ"])
    kids["mom_educ_cat"] = pd.cut(kids["mom_educ"], [0, 11, 12, 15, 17], labels=["<12", "12", "13-15", "16+"])
    mby = kids["mom_pid"].map(pby).fillna(kids.get("mom_byr_cah"))
    kids["mom_age_birth"] = (kids["birth_year"] - mby).where(lambda s: s.between(12, 55))
    c0 = cr.groupby("pid").first()
    married0 = (c0["w_pid"] == c0["mom_pid"]).astype(float)
    kids["mom_married_birth"] = kids["mom_married_cah"].fillna(kids["pid"].map(married0))

    # ---- mother's hours in the birth year, +1, +2
    for j in range(3):
        idx = pd.MultiIndex.from_arrays([kids["mom_pid"].fillna(-1).astype("int64"),
                                         (kids["birth_year"] + j).astype("int64")])
        kids[f"mom_hrs{j}"] = H.reindex(idx).to_numpy()
        kids[f"mom_emp{j}"] = (kids[f"mom_hrs{j}"] > 0).astype(float).where(kids[f"mom_hrs{j}"].notna())

    # ---- father figure's job loss, ages 0-17
    ff = cr[(cr["h_fem"] == 0) & cr["age"].between(0, 17) & (cr["h_pid"] != cr["pid"])].copy()
    ff = ff.drop_duplicates(["pid", "year"])

    def h(p, y):
        return H.reindex(pd.MultiIndex.from_arrays([p.astype("int64"), y.astype("int64")])).to_numpy()

    ff["h_t"] = h(ff["h_pid"], ff["year"])
    p1, p2 = h(ff["h_pid"], ff["year"] - 1), h(ff["h_pid"], ff["year"] - 2)
    ff["h_prev"] = np.where(np.isnan(p1), p2, p1)
    ff = ff.dropna(subset=["h_t", "h_prev"])
    ff["jl0"] = (ff["h_prev"] > 0) & (ff["h_t"] == 0)
    ff["jlu"] = (ff["h_prev"] > 0) & ((ff["h_t"] == 0) | (ff["hu"] > 0))
    kids["ff_years"] = kids["pid"].map(ff.groupby("pid").size()).fillna(0)
    kids["ff_bio"] = kids["pid"].map(ff.assign(b=ff.h_pid == ff.dad_pid).groupby("pid")["b"].mean())
    kids = first_age(ff[ff.jl0][["pid", "age"]], kids, "fjl0")
    kids = first_age(ff[ff.jlu][["pid", "age"]], kids, "fjl_u")

    # ---- parents' separation / divorce, ages 0-17
    mh = marriage()
    e = kids[["pid", "mom_pid", "birth_year"]].merge(mh, left_on="mom_pid", right_on="pid", suffixes=("", "_m"))
    e["age"] = e["year"] - e["birth_year"]
    kids = first_age(e[["pid", "age"]], kids, "div_mh")
    kids["mom_in_mh"] = kids["mom_pid"].isin(pd.read_fwf(OTH / "mh85_23" / "MH85_23.txt", colspecs=[(1, 5), (5, 8)],
                                                         header=None, names=["a", "b"]).eval("a*1000+b")).astype(float)
    mo = py[py["pid"].isin(kids["mom_pid"])][["pid", "wave", "int", "wife"]].merge(fu[["wave", "int", "h_pid"]],
                                                                                   on=["wave", "int"], how="left")
    mo = mo.sort_values(["pid", "wave"])
    nx = mo.groupby("pid").shift(-1)
    sp = mo[mo["wife"] & nx["wave"].notna()].copy()
    sp["w2"], sp["wife2"], sp["h2"] = nx.loc[sp.index, "wave"], nx.loc[sp.index, "wife"], nx.loc[sp.index, "h_pid"]
    sp = sp[~(sp["wife2"].astype(bool) & (sp["h2"] == sp["h_pid"]))]
    dy = sp["h_pid"].map(ind.set_index("pid")["death_year"])
    sp = sp[~(dy.notna() & (dy <= sp["w2"]))]
    sp["year"] = sp["w2"] - 1
    e = kids[["pid", "mom_pid", "birth_year"]].merge(sp[["pid", "year", "wave"]], left_on="mom_pid",
                                                     right_on="pid", suffixes=("", "_m"))
    e = e[e["year"] >= e["birth_year"]]
    e["age"] = e["year"] - e["birth_year"]
    kids = first_age(e[["pid", "age"]], kids, "div_rel")
    kids["div"] = kids[["div_mh", "div_rel"]].max(axis=1)
    kids["div_age1"] = kids[["div_mh_age1", "div_rel_age1"]].min(axis=1)

    # ---- family income by childhood age
    for lab, lo, hi, nmin in (("05", 0, 5, 2), ("617", 6, 17, 3)):
        s = cr[cr["age"].between(lo, hi)].drop_duplicates(["pid", "year"]).groupby("pid")["faminc"]
        kids[f"finc{lab}"] = kids["pid"].map(s.mean())
        kids[f"n_inc{lab}"] = kids["pid"].map(s.count()).fillna(0)
        kids[f"lfinc{lab}"] = np.log(kids[f"finc{lab}"].where((kids[f"finc{lab}"] > 0) & (kids[f"n_inc{lab}"] >= nmin)))

    # ---- welfare at ages 0-5 (last year; biennial era also year before last)
    w1 = cr[["pid", "year", "age", "afdc", "fs"]]
    w2 = cr.assign(year=cr["year"] - 1, age=cr["age"] - 1)[["pid", "year", "age", "tanf_ybl", "fs_ybl"]]
    w2 = w2.rename(columns={"tanf_ybl": "afdc", "fs_ybl": "fs"}).dropna(subset=["afdc", "fs"], how="all")
    w = pd.concat([w1, w2]).dropna(subset=["afdc", "fs"], how="all")
    w = w[w["age"].between(0, 5)].sort_values(["pid", "year"]).drop_duplicates(["pid", "year"])
    w["welf"] = w[["afdc", "fs"]].max(axis=1)
    g = w.groupby("pid")
    for c in ("afdc", "fs", "welf"):
        kids[f"{c}05"] = kids["pid"].map(g[c].sum())
    kids["welf05_obs"] = kids["pid"].map(g.size()).fillna(0)

    kids = kids.drop(columns=["female_cah", "mom_married_cah", "mom_byr_cah"])
    kids.to_pickle(DATA / "psid_child_exposure.pkl")

    # ---- sanity
    pd.set_option("display.width", 220, "display.max_columns", 40)
    k = kids[kids["race"].isin(["White", "Black"])]
    cols = ["mom_emp0", "mom_emp1", "mom_emp2", "mom_hrs1", "fjl0", "fjl_u", "div_mh", "div_rel", "div", "finc05",
            "finc617", "welf05", "afdc05", "fs05", "mom_educ", "mom_married_birth", "ff_years", "ff_bio"]
    print(k.groupby("race")[cols].mean().T.round(3))
    print(k.groupby("race")[cols].count().T)
    by = k.assign(dec=(k.birth_year // 10 * 10).astype(int)).groupby(["race", "dec"])
    print(by[["mom_emp1", "fjl0", "div", "welf05"]].mean().round(3))
    print(by[["mom_emp1", "fjl0", "div", "welf05"]].count())


if __name__ == "__main__":
    main()
