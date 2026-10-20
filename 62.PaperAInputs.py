r"""Pre-set inputs of Paper A's structural model from PSID / CPS data (2026-10-18). [Paper A]

Replaces the PLACEHOLDER fixed inputs of paperA_model/params.py (FIXED_STATUS) and the synthetic entry population
of paperA_model/simulate.py by coded mappings from data (proposals/paperA_identification_plan.md Sections 1.2,
1.5 and 1.6; model section paperA_joint_loss/sec7_model.tex). Nothing in paperA_model/*.py is edited: the outputs are
input files that params.load_fixed() and simulate.load_entry() already read.

OUTPUTS
  paperA_model/inputs/fixed_inputs.json        keys read by params.load_fixed() over FIXED_DEFAULTS:
        mu_w, mu_h {B, W} (log 2000 $ an hour), psi_w, psi_h, b0_annual, b2_annual {B, W: 7 age groups},
        n_children {B, W: 3 buckets x 7 age groups, integers}, p_cc [3] (2000 $ an hour), share_s {B, W: [s0, s1, s2]}
        + 'status' / 'source' blocks (ignored by the model code; documentation)
  paperA_model/inputs/psid_entry_couples.csv   simulate.ENTRY_COLS (id, year0, age0, race 0 = Black / 1 = White,
        s, a0 thousand 2000 $, ew0, eh0, k0, hw0, hh0 levels 1-7, uw0, uh0) + documentation columns
  paperA_model/inputs/psid_entry_couples_25_30.csv   the subset entering at wife's age 25-30 (lead's wording)
  paperA_model/inputs/start_overrides.json      a_bar start value (thousand 2000 $) for analytic_start.py / the lead
  output/paperA_inputs.md, output/paperA_inputs.csv   every value with source, window, N
  output/paperA_inputs_T7.csv                  CPS husband monthly hazard by race in the id format of
        paperA_targets.csv (ids cps_h_hazard_B / _W, the keys analytic_start.py looks for)
  output/cps_couple_state_shares.csv           CPS couples' state distribution by year (wife's composite weight),
        read by IGE/61.PolicySchedules.py to weight the UI cap and the AFDC/TANF maximum
  data/paperA_inputs_fam.pkl                   cache of the family-file items read here

DATA (raw files read only; builders imported read-only)
  PSID  60.PaperATargets.psid_build() (men panel m: male heads, Black / White, with the wife's pid, ages, hours, labor
        income in 2000 $, roster children; displacement file d; liquid wealth Wl = estimation/psid_wealth.py, the
        ReducedForm/17 construction, units x 5.82 = 2000 $); 23.CorrelatedShocks (occupation codes, wife's employment
        status, wife's job-end reports -> wife_displacement); 18.HusbandIndustryShocks.family() (3-digit industry of
        head and wife); 8.FirstStage (completed education from the individual file; Childbirth and Adoption History
        1985-2023); 47.PSIDConsumptionEvent.consumption() (annual child-care spending, waves 1999-2021). Read here
        from the family files (labels matched per wave, list in paperA_inputs.md): head's employment status, head's and
        wife's 'work for self / others' and 'work for government' on the main job. Unweighted SRC + SEO (as 60).
  CPS   30.CPSJointJobLoss couples panel (basic monthly 1994-2023) and 37's event sample 'tau'.
DEFINITIONS: see the md (each block lists its own); income year = interview wave - 1; ages in the income year =
  interview age - 1. Associations only; the one regression (wage prediction for non-employed entrants) is reported
  with clustered s.e., p-values and stars.
Run from IGE/: ../.venv/Scripts/python.exe -I 62.PaperAInputs.py [--reps 200] [--skip-cps]
"""
import argparse
import importlib.util
import json
import sys
import time
import warnings
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import numpy as np                            # noqa: E402
import pandas as pd                           # noqa: E402
import statsmodels.api as sm                  # noqa: E402

from common import CPI, DATA, OUT, stars      # noqa: E402

warnings.simplefilter("ignore", FutureWarning)
warnings.simplefilter("ignore", RuntimeWarning)
INPUTS = HERE / "paperA_model" / "inputs"
T0 = time.time()
ROWS = []          # every reported value: block, item, race, value, se, n, window, source, definition


def log(*a):
    print(f"[{time.time() - T0:7.0f}s]", *a, flush=True)


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def rec(block, item, value, se=np.nan, n=np.nan, window="", source="", definition="", race="", p=np.nan, note=""):
    ROWS.append(dict(block=block, item=item, race=race, value=value, se=se, p=p, n=n, note=note, window=window,
                     source=source, definition=definition))


def cl_mean(y, g):
    """Mean and cluster-robust s.e. (clusters g)."""
    y = np.asarray(y, float)
    g = pd.factorize(np.asarray(g))[0]
    mu = y.mean()
    s = np.bincount(g, weights=y - mu)
    G = g.max() + 1
    se = np.sqrt((s ** 2).sum() * G / max(G - 1, 1)) / len(y)
    return float(mu), float(se), len(y)


# =====================================================================================================================
# PSID family-file items (head's employment status, class of worker of both spouses)
# =====================================================================================================================
PAT_X = {
    "h_stat": [r"^[BC]1 EMPLOYMENT STATUS-HD", r"^B1 EMPLMT STATUS-HEAD", r"^B1 1ST MENTION$",
               r"^BC1 EMPLOYMENT STATUS-1ST MENTION", r"^B1 HEAD \d{4} EMPLOYMENT STATUS"],
    "h_self": [r"^[BC]\d+ WORK SELF/OTR\? ?\(HD-E\)", r"^BC22 WORK SELF/OTR\?--JOB 1",
               r"^B4 WTR WORK FOR SELF/SOMEONE ELSE \(HD-E\)"],
    "h_govt": [r"^[BC]\d+ WORK FOR GOVT\? ?\(HD-E\)", r"^BC24 WORK FOR GOVT\?--JOB 1", r"^B6 WTR WORK FOR GOVT \(HD-E\)"],
    "w_self": [r"^[DJF]\d+ WORK SELF/OTR\? ?\(WF-E\)", r"^F5 WORK FOR SELF\?\(WF-E\)", r"^DE22 WORK SELF/OTR\?--JOB 1",
               r"^D4 WTR WORK FOR SELF/SOMEONE ELSE \(WF-E\)"],
    "w_govt": [r"^[DJF]\d+ (WORK|WRK) FOR GOVT\? ?\(WF-E\)", r"^DE24 WORK FOR GOVT\?--JOB 1",
               r"^D6 WTR WORK FOR GOVT \(WF-E\)"],
}


def family_items(P18, P23):
    fn = DATA / "paperA_inputs_fam.pkl"
    if fn.exists():
        return pd.read_pickle(fn)
    out, found = [], []
    for w in [w for w in P23.WAVES if w >= 1984]:
        folder = P23.FAM / (f"fam{w}" if w < 1994 else f"fam{w}er")
        do = next(f for f in folder.glob("*.do") if "formats" not in f.name)
        pos, labs = P18.layout(do)
        labs = [(v, l) for v, l in labs if v in pos]
        idv = labs[1][0]
        sel = {k: P23.find(labs, p) for k, p in PAT_X.items()}
        cols = sorted({idv, *[v[0] for v in sel.values() if v]})
        f = P18.read(do.with_suffix(".txt"), cols, pos)
        x = pd.DataFrame({"wave": w, "int": f[idv]})
        for k, v in sel.items():
            x[k] = f[v[0]] if v else np.nan
        x["w_self_f5"] = int(bool(sel["w_self"]) and "WORK FOR SELF" in sel["w_self"][1])
        out.append(x)
        found.append(dict(wave=w, **{k: (f"{v[0]} '{v[1]}'" if v else "") for k, v in sel.items()}))
        log(f"  family items {w}: " + "; ".join(f"{k}={v[0] if v else '-'}" for k, v in sel.items()))
    res = dict(X=pd.concat(out, ignore_index=True), found=pd.DataFrame(found))
    pd.to_pickle(res, fn)
    return res


# =====================================================================================================================
# Industry / occupation groups analogous to the CPS detailed recodes (PRDTIND1, PRDTOCC1)
# =====================================================================================================================
# CPS detailed industry recode (2003+ definition, 51 groups + armed forces) on Census 2002 / 2012 4-digit codes
IND4 = [(170, 180, 1), (190, 280, 2), (290, 290, 1), (370, 490, 3), (570, 690, 24), (770, 770, 4), (1070, 1290, 14),
        (1370, 1390, 15), (1470, 1790, 16), (1870, 1990, 17), (2070, 2090, 18), (2170, 2290, 19), (2370, 2390, 20),
        (2470, 2590, 5), (2670, 2990, 6), (3070, 3290, 7), (3360, 3390, 8), (3470, 3490, 9), (3570, 3690, 10),
        (3770, 3790, 11), (3870, 3890, 12), (3895, 3990, 13), (4070, 4590, 21), (4670, 5790, 22), (6070, 6390, 23),
        (6470, 6490, 25), (6570, 6590, 26), (6670, 6671, 27), (6672, 6674, 28), (6675, 6690, 29), (6691, 6695, 30),
        (6770, 6780, 31), (6870, 6970, 32), (6990, 6990, 33), (7070, 7070, 34), (7071, 7190, 35), (7270, 7490, 36),
        (7570, 7570, 37), (7580, 7780, 38), (7790, 7790, 39), (7860, 7890, 40), (7970, 8180, 42), (8190, 8190, 41),
        (8270, 8290, 42), (8370, 8470, 43), (8560, 8590, 44), (8660, 8670, 45), (8680, 8690, 46), (8770, 8890, 47),
        (8970, 9090, 48), (9160, 9190, 49), (9290, 9290, 50), (9370, 9590, 51), (9670, 9870, 52)]
# the same 51 groups on 1970 Census industry codes (PSID waves to 2001)
IND70 = [(17, 19, 1), (27, 28, 2), (47, 58, 3), (67, 78, 4), (107, 107, 2), (108, 109, 11), (118, 118, 12),
         (119, 138, 5), (139, 169, 6), (177, 177, 7), (178, 178, 8), (179, 198, 7), (199, 206, 9), (207, 207, 8),
         (208, 209, 9), (219, 238, 10), (239, 239, 8), (247, 259, 13), (268, 288, 14), (289, 289, 15), (297, 298, 14),
         (299, 299, 15), (307, 327, 16), (328, 339, 17), (347, 369, 19), (377, 378, 18), (379, 387, 20),
         (388, 397, 16), (398, 398, 13), (407, 439, 23), (447, 447, 27), (448, 449, 29), (467, 469, 24),
         (477, 477, 24), (478, 478, 39), (479, 479, 24), (507, 599, 21), (607, 668, 22), (669, 669, 46),
         (670, 699, 22), (707, 709, 32), (717, 717, 33), (718, 718, 34), (727, 727, 36), (728, 728, 38),
         (729, 729, 36), (737, 737, 38), (738, 739, 36), (747, 748, 38), (749, 749, 35), (750, 759, 47),
         (769, 769, 50), (777, 778, 45), (779, 798, 48), (807, 809, 44), (828, 837, 42), (838, 838, 41),
         (839, 847, 42), (848, 848, 36), (849, 867, 40), (868, 868, 44), (869, 869, 49), (877, 878, 43),
         (879, 879, 49), (887, 899, 36), (907, 937, 51), (947, 999, 52)]
# CPS detailed occupation recode, 2003+ (23 SOC groups), Census 2002 and 2010 4-digit codes
OCC4 = [(10, 430, 1), (500, 950, 2), (1000, 1240, 3), (1300, 1560, 4), (1600, 1965, 5), (2000, 2060, 6),
        (2100, 2160, 7), (2200, 2550, 8), (2600, 2960, 9), (3000, 3540, 10), (3600, 3655, 11), (3700, 3955, 12),
        (4000, 4160, 13), (4200, 4250, 14), (4300, 4650, 15), (4700, 4965, 16), (5000, 5940, 17), (6000, 6130, 18),
        (6200, 6940, 19), (7000, 7630, 20), (7700, 8965, 21), (9000, 9750, 22), (9800, 9830, 23)]
# CPS detailed occupation recode, 1994-2002 (46 groups, 1990 Census classification), on 1970 Census codes
OCC70 = [(1, 1, 2), (2, 2, 11), (3, 5, 4), (6, 23, 3), (24, 29, 11), (30, 31, 10), (32, 41, 11), (42, 54, 5),
         (55, 55, 4), (56, 56, 2), (57, 60, 11), (61, 73, 6), (74, 76, 7), (80, 85, 12), (86, 101, 11),
         (102, 140, 8), (141, 145, 9), (150, 162, 13), (163, 163, 38), (164, 173, 14), (174, 195, 11), (201, 201, 2),
         (202, 202, 1), (203, 205, 2), (206, 224, 1), (225, 225, 2), (226, 245, 1), (260, 260, 16), (261, 264, 19),
         (265, 265, 16), (266, 266, 18), (267, 271, 16), (272, 281, 17), (282, 284, 18), (285, 285, 19),
         (301, 305, 23), (310, 310, 18), (311, 330, 25), (331, 331, 24), (332, 342, 25), (343, 343, 21),
         (344, 359, 25), (360, 360, 23), (361, 361, 24), (362, 369, 25), (370, 372, 22), (373, 375, 25),
         (376, 376, 23), (377, 380, 25), (381, 381, 22), (382, 390, 25), (391, 391, 22), (392, 395, 25),
         (401, 401, 32), (402, 409, 34), (410, 411, 33), (412, 412, 38), (413, 413, 34), (414, 416, 33),
         (420, 421, 33), (422, 423, 34), (424, 424, 38), (425, 429, 34), (430, 431, 33), (433, 433, 32),
         (434, 435, 34), (436, 436, 38), (440, 440, 33), (441, 444, 34), (445, 445, 33), (446, 454, 34),
         (455, 456, 38), (457, 469, 34), (470, 495, 32), (496, 509, 34), (510, 512, 33), (513, 519, 34),
         (520, 523, 33), (524, 533, 34), (534, 536, 33), (537, 549, 34), (550, 550, 33), (551, 551, 34),
         (552, 554, 32), (555, 559, 34), (560, 560, 33), (561, 579, 34), (580, 600, 45), (601, 601, 35),
         (602, 602, 36), (603, 609, 35), (610, 611, 36), (612, 679, 35), (680, 680, 36), (681, 699, 35),
         (701, 702, 38), (703, 703, 37), (704, 704, 38), (705, 705, 37), (706, 713, 38), (714, 715, 37),
         (740, 749, 41), (750, 751, 39), (752, 752, 44), (753, 753, 40), (754, 760, 41), (761, 761, 44),
         (762, 762, 40), (763, 769, 41), (770, 770, 40), (771, 799, 41), (801, 802, 42), (821, 824, 43),
         (901, 903, 30), (910, 916, 28), (921, 926, 29), (931, 954, 31), (960, 965, 27), (980, 984, 26)]


def _ranges(code, table):
    c = np.asarray(code, float)
    out = np.full(len(c), np.nan)
    for lo, hi, g in table:
        out[(c >= lo) & (c <= hi)] = g
    return out


def ind_group(code, wave):
    c, w = np.asarray(code, float), np.asarray(wave)
    out = np.full(len(c), np.nan)
    m70, m00, m12 = w <= 2001, (w >= 2003) & (w <= 2015), w >= 2017
    out[m70] = _ranges(c[m70], IND70)
    out[m00] = _ranges(c[m00] * 10, IND4)
    out[m12] = _ranges(c[m12], IND4)
    return out


def occ_group(code, wave):
    c, w = np.asarray(code, float), np.asarray(wave)
    out = np.full(len(c), np.nan)
    m70, m00, m10 = w <= 2001, (w >= 2003) & (w <= 2015), w >= 2017
    out[m70] = _ranges(c[m70], OCC70)
    out[m00] = _ranges(c[m00] * 10, OCC4)
    out[m10] = _ranges(c[m10], OCC4)
    return out


def cow3(self_, govt, f5flag):
    """Class of worker: 1 private, 2 government, 3 self-employed (PSID 'work for self / others' 1 someone else, 2 both,
    3 self only; 'work for government' 1 yes, 5 no; 1984 wife item 'work for self?' 1 yes / 5 no)."""
    s, g, f5 = (np.asarray(x, float) for x in (self_, govt, f5flag))
    self_emp = np.where(f5 == 1, s == 1, np.isin(s, (2, 3)))
    other = np.where(f5 == 1, s == 5, s == 1)
    out = np.where(self_emp, 3, np.where(other & (g == 1), 2, np.where(other, 1, np.nan)))
    return out


# =====================================================================================================================
def build_psid():
    log("PSID: loading builders")
    M60 = _load("p60", "60.PaperATargets.py")
    P23 = _load("p23", "23.CorrelatedShocks.py")
    P18 = P23.P18
    FS = _load("fs8", "8.FirstStage.py")
    B = M60.psid_build()
    m = B["m"].copy()
    E = P23.extras()
    X = E["X"]
    F18 = pd.read_pickle(DATA / "husband_shocks_fam.pkl")
    FI = family_items(P18, P23)
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    wd, _ = P23.wife_displacement(py, E["R"])
    ed, _ = FS.education()
    cah = FS.cah()
    log("PSID: assembling the couple panel")
    m = m.merge(X[["wave", "int", "h_occ", "w_occ", "w_stat"]].drop_duplicates(["wave", "int"]), on=["wave", "int"],
                how="left")
    m = m.merge(F18[["wave", "int", "h_ind", "w_ind"]].drop_duplicates(["wave", "int"]), on=["wave", "int"], how="left")
    m = m.merge(FI["X"].drop_duplicates(["wave", "int"]), on=["wave", "int"], how="left")
    ed = ed.drop_duplicates("pid").set_index("pid")["educ"]
    m["h_educ"] = m["pid"].map(ed)
    m["w_educ"] = m["w_pid"].map(ed)
    d = B["d"]
    dh = d[d["main"] == 1][["pid", "year"]].drop_duplicates()
    dw = wd[wd["main"] == 1][["pid", "year"]].drop_duplicates()
    hset, wset = set(zip(dh.pid, dh.year)), set(zip(dw.pid, dw.year))
    m["h_disp"] = [((p, w) in hset) or ((p, w - 1) in hset) for p, w in zip(m["pid"], m["wave"])]
    m["w_disp"] = [((p, w) in wset) or ((p, w - 1) in wset) if p == p else False for p, w in zip(m["w_pid"], m["wave"])]
    for sx, lab, hrs in (("h", "hlab", "hh"), ("w", "wlab", "wh")):
        wage = (m[lab] / m[hrs]).where((m[hrs] >= 260) & (m[lab] > 0))
        m[f"lw_{sx}"] = np.log(wage.where(wage.between(2, 200)))
    m["h_agey"] = m["age"] - 1
    m["w_agey"] = m["w_age"] - 1
    m["h_ig"] = ind_group(P23.valid_code(m["h_ind"], m["wave"]), m["wave"])
    m["w_ig"] = ind_group(P23.valid_code(m["w_ind"], m["wave"]), m["wave"])
    m["h_og"] = occ_group(P23.valid_code(m["h_occ"], m["wave"]), m["wave"])
    m["w_og"] = occ_group(P23.valid_code(m["w_occ"], m["wave"]), m["wave"])
    m["h_cow"] = cow3(m["h_self"], m["h_govt"], np.zeros(len(m)))
    m["w_cow"] = cow3(m["w_self"], m["w_govt"], m["w_self_f5"].fillna(0))
    for sx, st in (("h", "h_stat"), ("w", "w_stat")):
        s = pd.to_numeric(m[st], errors="coerce")
        m[f"{sx}_emp"] = np.where(s.isin([1, 2]), 1.0, np.where(s.between(3, 8), 0.0, np.nan))
    return dict(m=m, Wl=B["Wl"], cah=cah, found=FI["found"])


# =====================================================================================================================
def wage_levels(m, fx):
    """mu_j(r): mean log hourly wage (2000 $) of employed spouses 25-29; psi_j: (q99 - q01)/6 of the residual at
    40-49 (log wage minus its race x income-year mean), shrunk for the transitory variance and measurement error."""
    c = m[m["w_pid"].notna() & m["year"].between(1984, 2021)]
    out, info = {}, {}
    dmu = ("PSID married couples (male head, wife present, Black / White head), income years 1984-2021; log hourly "
           "wage = annual labor income / annual hours (2000 $), spouses with at least 260 annual hours and a wage of "
           "$2-$200; that spouse's age 25-29 in the income year; unweighted; s.e. clustered by 1968 family.")
    for sx, who in (("w", "wives"), ("h", "husbands")):
        ag = c[f"{sx}_agey"]
        for r, rb in (("Black", "B"), ("White", "W")):
            q = c[(c["hrace"] == r) & ag.between(25, 29) & c[f"lw_{sx}"].notna()]
            mu, se, n = cl_mean(q[f"lw_{sx}"], q["fam68"])
            out.setdefault(f"mu_{sx}", {})[rb] = mu
            rec("Wage levels", f"mu_{sx} (mean log wage of employed {who} 25-29)", mu, se, n, "PSID 1984-2021",
                "IGE/62", dmu, race=rb)
        q = c[ag.between(40, 49) & c[f"lw_{sx}"].notna()].copy()
        q["e"] = q[f"lw_{sx}"] - q.groupby(["hrace", "year"])[f"lw_{sx}"].transform("mean")
        V = float(q["e"].var())
        q01, q99 = (float(v) for v in q["e"].quantile([0.01, 0.99]))
        sig2 = fx[f"bps_var_trans_{sx}"]
        shrink = np.sqrt(max(V - sig2 - 0.13 * V, 0.0) / V)
        psi = (q99 - q01) / 6 * shrink
        out[f"psi_{sx}"] = float(psi)
        info[sx] = dict(V=V, q01=q01, q99=q99, sig2=sig2, shrink=shrink, n=len(q))
        # check: the same without the race x year demeaning (residual from the race mean only)
        e2 = q[f"lw_{sx}"] - q.groupby("hrace")[f"lw_{sx}"].transform("mean")
        psi2 = (e2.quantile(0.99) - e2.quantile(0.01)) / 6 * np.sqrt(max(e2.var() - sig2 - 0.13 * e2.var(), 0) / e2.var())
        rec("Wage levels", f"psi_{sx} (grid step, 7 levels span q01-q99 of the persistent part)", psi, np.nan, len(q),
            "PSID 1984-2021", "IGE/62",
            f"Residual e = log wage minus its race x income-year mean, {who} aged 40-49 in the income year (same sample "
            f"rules as mu); psi = (q99 - q01)/6 x sqrt((V - sigma_nu^2 - 0.13 V)/V) with V = Var(e) = {V:.4f}, q01 = "
            f"{q01:.3f}, q99 = {q99:.3f}, sigma_nu^2 = {sig2} (BPS Table 3 transitory variance, params.FIXED_DEFAULTS), "
            f"0.13 = Bound et al. (1994) measurement-error share; shrink factor {shrink:.3f}. Check without the year "
            f"demeaning (race means only): psi = {psi2:.4f}.")
    return out, info


def wage_prediction(m):
    """OLS log wage on education group, age group and race (each spouse), employed spouses; used for entrants with no
    wage in the entry income year and none in the previous five years."""
    c = m[m["w_pid"].notna() & m["year"].between(1984, 2021)]
    models = {}
    for sx in ("h", "w"):
        q = c[c[f"lw_{sx}"].notna() & c[f"{sx}_agey"].between(25, 59)].copy()
        X = design(q, sx)
        res = sm.OLS(q[f"lw_{sx}"].to_numpy(float), X).fit(cov_type="cluster", cov_kwds={"groups": q["fam68"]})
        models[sx] = res
        for nm, b, se, p in zip(X.columns, res.params, res.bse, res.pvalues):
            rec("Wage prediction (regression)", f"{sx}: {nm}", float(b), float(se), int(res.nobs), "PSID 1984-2021",
                "IGE/62", f"OLS of the log hourly wage on education (base <= 12 years), age group (base 25-29) and Black, "
                f"{'husbands (h)' if sx == 'h' else 'wives (w)'} 25-59 employed (>= 260 hours), income years "
                f"1984-2021; s.e. clustered by 1968 family; R^2 = {res.rsquared:.3f}.", p=float(p))
    return models


def edu3(e):
    e = np.asarray(e, float)
    return np.where(e >= 16, 2, np.where(e >= 13, 1, 0))


def design(q, sx):
    e = edu3(q[f"{sx}_educ"])
    ag = np.clip((q[f"{sx}_agey"].to_numpy() - 25) // 5, 0, 6)
    X = pd.DataFrame({"const": 1.0, "edu_13_15": (e == 1).astype(float), "edu_16plus": (e == 2).astype(float),
                      "black": (q["hrace"] == "Black").to_numpy(float)}, index=q.index)
    for g in range(1, 7):
        X[f"age_{25 + 5 * g}_{29 + 5 * g}"] = (ag == g).astype(float)
    return X


# =====================================================================================================================
def workplace_match(m):
    """s = 2 same industry group x same occupation group x same class of worker; s = 1 same industry group only;
    s = 0 otherwise; defined when both spouses are employed at the interview with valid codes."""
    both = (m["h_ig"].notna() & m["w_ig"].notna() & m["h_og"].notna() & m["w_og"].notna())
    si = (m["h_ig"] == m["w_ig"])
    so = (m["h_og"] == m["w_og"])
    sc = (m["h_cow"] == m["w_cow"]) & m["h_cow"].notna()
    s = np.where(si & so & sc, 2, np.where(si, 1, 0)).astype(float)
    m["s_cpl"] = np.where(both, s, np.nan)
    return m


# =====================================================================================================================
def entry_population(m, Wl, mu, psi, models):
    c = m[m["w_pid"].notna() & m["hrace"].isin(["Black", "White"])].copy()
    c = c.sort_values(["pid", "w_pid", "wave"])
    c["cpl"] = c["pid"].astype(np.int64) * 10 ** 7 + c["w_pid"].astype(np.int64)
    ok = (c["wave"] >= 1984) & c["w_age"].between(25, 59)
    e = c[ok].groupby("cpl").head(1).copy()
    # workplace match: at entry, else the first later wave of the same couple with both codes
    sfirst = c[ok & c["s_cpl"].notna()].groupby("cpl")["s_cpl"].first()
    e["s_src"] = np.where(e["s_cpl"].notna(), "entry wave", np.where(e["cpl"].isin(sfirst.index), "later wave",
                                                                     "never both employed: 0"))
    e["s"] = e["s_cpl"].fillna(e["cpl"].map(sfirst)).fillna(0).astype(int)
    # wages: entry income year, else the person's last wage in the previous five years, else the prediction
    for sx, idc in (("h", "pid"), ("w", "w_pid")):
        hist = m[m[f"lw_{sx}"].notna() & m[idc].notna()].sort_values("year")
        hd = {p: (g["year"].to_numpy(), g[f"lw_{sx}"].to_numpy()) for p, g in hist.groupby(idc)}
        prev = []
        for p, y in zip(e[idc], e["year"]):
            yy, ll = hd.get(p, (np.array([]), np.array([])))
            k = (yy < y) & (yy >= y - 5)
            prev.append(ll[k][-1] if k.any() else np.nan)
        e[f"lwp_{sx}"] = prev
        Xp = design(e.assign(**{f"{sx}_agey": e[f"{sx}_agey"].clip(25, 59)}), sx)
        pred = models[sx].predict(Xp)
        src = np.where(e[f"lw_{sx}"].notna(), "entry year", np.where(e[f"lwp_{sx}"].notna(), "previous 5 years",
                                                                      "prediction"))
        lw = e[f"lw_{sx}"].fillna(e[f"lwp_{sx}"]).fillna(pd.Series(pred, index=e.index))
        rb = np.where(e["hrace"] == "Black", "B", "W")
        mur = np.array([mu[f"mu_{sx}"][r] for r in rb])
        e[f"h{sx}0_src"] = src
        e[f"{sx}_lw0"] = lw
        e[f"h{sx}0"] = np.clip(4 + np.round((lw - mur) / psi[f"psi_{sx}"]), 1, 7).astype(int)
    e = e.rename(columns={"hh0": "hh0", "hw0": "hw0"})
    # employment and UI at entry
    for sx in ("h", "w"):
        hrs = e["hh" if sx == "h" else "wh"]
        emp = e[f"{sx}_emp"].fillna((hrs >= 260).astype(float))
        e[f"e{sx}0"] = emp.astype(int)
        e[f"u{sx}0"] = ((emp == 0) & e[f"{sx}_disp"].astype(bool)).astype(int)
    # children at entry (roster at the entry interview)
    yg = e["youngest"]
    e["k0"] = np.where(yg.isna() | (yg > 17), 0, np.where(yg <= 5, 1, 2)).astype(int)
    # liquid wealth (thousand 2000 $): own at the entry wave, else own within +-2 years, else cell median at the
    # nearest wealth wave (wife's age group x race x couple's education)
    W = Wl.dropna(subset=["liquid"]).copy()
    W["liq"] = W["liquid"] * 5.82 / 1000.0
    own = W.set_index(["id", "wave"])["liq"]
    e["a0"] = [own.get((p, w), np.nan) for p, w in zip(e["pid"], e["wave"])]
    e["a0_src"] = np.where(e["a0"].notna(), "own, entry wave", "")
    waves = np.array(sorted(W["wave"].unique()))
    for dw in (-1, 1, -2, 2):
        fill = [own.get((p, w + dw), np.nan) for p, w in zip(e["pid"], e["wave"])]
        miss = e["a0"].isna()
        e.loc[miss, "a0"] = np.array(fill)[miss.to_numpy()]
        e.loc[miss & e["a0"].notna(), "a0_src"] = f"own, wave {dw:+d}"
    # cells
    cw = W.merge(m[["pid", "wave", "w_pid", "w_age", "hrace", "h_educ", "w_educ"]].rename(columns={"pid": "id"}),
                 on=["id", "wave"])
    cw = cw[cw["w_pid"].notna() & cw["w_age"].between(25, 59)]
    cell = lambda d: (np.digitize(d["w_age"], [35, 45]).astype(int) * 100 + (d["hrace"] == "Black").astype(int) * 10  # noqa
                      + edu3(np.fmax(d["h_educ"].fillna(0), d["w_educ"].fillna(0))))
    cw["cell"] = cell(cw)
    med = cw.groupby(["cell", "wave"])["liq"].median()
    e["cell"] = cell(e)
    near = waves[np.abs(e["wave"].to_numpy()[:, None] - waves[None, :]).argmin(axis=1)]
    miss = e["a0"].isna()
    e.loc[miss, "a0"] = [med.get((cc, ww), np.nan) for cc, ww in zip(e.loc[miss, "cell"], near[miss.to_numpy()])]
    e.loc[miss, "a0_src"] = "cell median, nearest wealth wave"
    e["a0"] = e["a0"].fillna(float(cw["liq"].median()))
    e["race"] = (e["hrace"] == "White").astype(int)
    e["year0"] = e["wave"].astype(int)
    e["age0"] = e["w_age"].astype(int)
    e = e.reset_index(drop=True)
    e["id"] = np.arange(len(e))
    cols = ["id", "year0", "age0", "race", "s", "a0", "ew0", "eh0", "k0", "hw0", "hh0", "uw0", "uh0",
            "pid", "w_pid", "fam68", "s_src", "a0_src", "hw0_src", "hh0_src", "h_lw0", "w_lw0", "h_educ", "w_educ"]
    return e[cols]


# =====================================================================================================================
def child_process(m, cah):
    """b_0, b_2 from the Childbirth and Adoption History (births to the wife by calendar year) on married couple-years;
    k at the start of the calendar year from the wife's own births."""
    b = cah[(cah["CAH2"] == 1) & cah["CAH15"].between(1940, 2023)]
    b = b.drop_duplicates(["pid", "CAH15", "CAH13"])                                  # multiple births once
    births = b.groupby("pid")["CAH15"].apply(lambda s: np.sort(s.to_numpy()))
    incah = set(cah["pid"])
    c = m[m["w_pid"].notna() & m["year"].between(1984, 2021) & m["w_agey"].between(25, 59)].copy()
    c = c[c["w_pid"].isin(incah)]
    yb = []
    kk = []
    for p, y in zip(c["w_pid"], c["year"]):
        bb = births.get(p, np.array([]))
        yb.append(int((bb == y).any()))
        prev = bb[bb < y]
        if len(prev) == 0:
            kk.append(0)
        else:
            a = y - prev.max()                                        # youngest child's age (years) during year y
            kk.append(1 if a <= 6 else (2 if a <= 18 else 0))
    c["birth"], c["kj"] = yb, kk
    c["g"] = np.clip((c["w_agey"] - 25) // 5, 0, 6).astype(int)
    out = {"b0_annual": {}, "b2_annual": {}}
    tab = []
    for r, rb in (("Black", "B"), ("White", "W")):
        for key, k in (("b0_annual", 0), ("b2_annual", 2)):
            vals = []
            for g in range(7):
                q = c[(c["hrace"] == r) & (c["kj"] == k) & (c["g"] == g)]
                v = float(q["birth"].mean()) if len(q) >= 30 else 0.0
                vals.append(v)
                tab.append(dict(race=rb, k=k, age=f"{25 + 5 * g}-{29 + 5 * g}", p=v, n=len(q)))
                se = float(np.sqrt(v * (1 - v) / len(q))) if len(q) else np.nan
                rec("Child process", f"{key} age {25 + 5 * g}-{29 + 5 * g}", v, se, len(q), "PSID 1984-2021",
                    "IGE/62 (CAH 1985-2023)",
                    f"Annual probability that the wife gives birth in calendar year y (CAH birth records, multiple births "
                    f"once) among married couple-years (income years 1984-2021, wife observed as the head's wife at "
                    f"the wave reporting year y, wife's age 25-59 in y, wife in the CAH) with "
                    f"{'no own child under 18' if k == 0 else 'own youngest child aged 6-17'} at the start of y "
                    f"(from her own births); set to 0 when the cell has fewer than 30 couple-years; unweighted.",
                    race=rb)
            out[key][rb] = vals
    return out, pd.DataFrame(tab)


def n_children(m):
    c = m[m["w_pid"].notna() & m["year"].between(1984, 2021) & m["w_age"].between(25, 59)].copy()
    yg = c["youngest"]
    c["k"] = np.where(yg.isna() | (yg > 17), 0, np.where(yg <= 5, 1, 2))
    c["g"] = np.clip((c["w_age"] - 25) // 5, 0, 6).astype(int)
    out = {}
    for r, rb in (("Black", "B"), ("White", "W")):
        arr = [[0] * 7, [0] * 7, [0] * 7]
        for k in (1, 2):
            means = []
            for g in range(7):
                q = c[(c["hrace"] == r) & (c["k"] == k) & (c["g"] == g)]
                means.append((float(q["nkid"].mean()) if len(q) >= 30 else np.nan, len(q)))
            vals = np.array([v for v, _ in means])
            for g in range(7):                                         # empty cells: nearest age group with data
                if not np.isfinite(vals[g]):
                    ok = np.nonzero(np.isfinite(vals))[0]
                    vals[g] = vals[ok[np.abs(ok - g).argmin()]] if len(ok) else 1.0
                arr[k][g] = int(max(1, round(vals[g])))
                rec("Number of children", f"n(k={k}, age {25 + 5 * g}-{29 + 5 * g})", arr[k][g], np.nan, means[g][1],
                    "PSID 1984-2021", "IGE/62",
                    "Rounded mean number of children 0-17 in the family unit (roster) of married couples, by wife's "
                    "interview age group and youngest child's bucket (0-5 / 6-17), interviews 1985-2022 "
                    "(income years 1984-2021); "
                    "k = 0 has n = 0 by definition; cells with fewer than 30 couple-years take the nearest age group.",
                    race=rb, note=f"unrounded {vals[g]:.2f}" + (" (nearest age group)" if not np.isfinite(means[g][0])
                                                                else ""))
        out[rb] = arr
    return out


def childcare(m):
    P47 = _load("p47", "47.PSIDConsumptionEvent.py")
    C = P47.consumption()["C"][["wave", "int", "childcare"]]
    c = m[m["w_pid"].notna() & m["wave"].between(1999, 2021)].merge(C, on=["wave", "int"], how="inner")
    c = c[c["wh"] >= 260].copy()
    c["cc"] = [v * CPI[2000] / CPI[int(w) - 1] if np.isfinite(v) else np.nan for v, w in zip(c["childcare"], c["wave"])]
    c = c[c["cc"].notna() & (c["cc"] >= 0)]
    ya = c["youngest"] - 1                                             # youngest child's age in the income year
    c["k"] = np.where(c["youngest"].isna() | (ya > 17), 0, np.where(ya <= 5, 1, 2))
    p = [0.0, np.nan, np.nan]
    for k in (1, 2):
        q = c[c["k"] == k]
        num, den = q.groupby("fam68")["cc"].sum(), q.groupby("fam68")["wh"].sum()
        val = float(q["cc"].sum() / q["wh"].sum())
        # cluster-robust s.e. of a ratio of means (delta method)
        G = len(num)
        z = (num - val * den)
        se = float(np.sqrt((z ** 2).sum() * G / (G - 1)) / q["wh"].sum())
        p[k] = val
        rec("Childcare price", f"p_cc(k={k}) (2000 $ per hour of the wife's work)", val, se, len(q), "PSID 1999-2021",
            "IGE/62 (IGE/47 consumption module)",
            f"Ratio of means: total annual child-care spending (47's 'childcare', per-period amounts annualised, nominal "
            f"-> 2000 $ with the CPI-U of the income year) over total annual hours of wives with >= 260 hours, married "
            f"couples, waves 1999-2021 (income years 1998-2020), youngest child in the income year "
            f"{'0-5' if k == 1 else '6-17'} (roster age - 1); zeros included; share with positive spending "
            f"{(q['cc'] > 0).mean():.3f}; mean of individual ratios {float((q['cc'] / q['wh']).mean()):.3f}; s.e. "
            "clustered by 1968 family (delta method).")
    return p


def a_bar_start(Wl, m):
    W = Wl.dropna(subset=["liquid"]).merge(m[["pid", "wave", "w_pid", "w_age"]].rename(columns={"pid": "id"}),
                                           on=["id", "wave"])
    W = W[W["w_pid"].notna() & W["w_age"].between(25, 34)]
    liq = W["liquid"] * 5.82
    p10 = float(liq.quantile(0.10))
    a = max(-p10, 0.0) / 1000.0
    rec("Borrowing limit (start value)", "a_bar start (thousand 2000 $)", a, np.nan, len(W),
        "PSID 1984-2019 wealth waves", "IGE/62 (estimation/psid_wealth.py, ReducedForm/17)",
        f"Plan 1.5: a_bar starts at minus the 10th percentile of liquid wealth (checking/savings + bonds/CDs from 2019 + "
        f"stocks - unsecured debt, 2000 $) of married couples with the wife aged 25-34 at the wealth interview; P10 = "
        f"{p10:,.0f} 2000 $; share <= 0 = {(liq <= 0).mean():.3f}; unweighted. An SMM parameter: start value only.")
    return a, p10


# =====================================================================================================================
def cps_part(reps, seed=62):
    m37 = _load("cps37", "37.CPSJointLossChecks.py")
    m30 = m37.m30
    log("CPS: loading panel")
    P = m30.add_vars(m30.build_panel())
    P.attrs = {}
    # state distribution by year (both spouses present, base months; wife's composite weight)
    sh = P.groupby(["year", "state"])["w"].sum().rename("w").reset_index()
    sh["share"] = sh["w"] / sh.groupby("year")["w"].transform("sum")
    sh.to_csv(OUT / "cps_couple_state_shares.csv", index=False)
    for k in (-2, -1):                                               # as in IGE/60 (37's event samples need them)
        for c, v in m37.shift(P, ["w_dur"], k).items():
            P[c] = v.astype("int16")
    ev = m37.event_samples(P)
    d = ev["tau"]
    d = d[((d.H == 0) | d["h_unt+1"].isin([2, 3])) & ~((d["w_s+1"] == 2) & (d["w_unt+1"] == 1))]
    hh = pd.factorize(d["hh"])[0]
    G = hh.max() + 1
    H, w, rg = d["H"].to_numpy(float), d["w"].to_numpy(float), d["rgrp"].to_numpy()
    # second definition: all husbands employed at t (wife in any state), H = non-temporary job loser at t+1
    b2 = (P.h_s == 1) & P["h_s+1"].isin([1, 2]) & ~((P["h_s+1"] == 2) & (P["h_unt+1"] == 1))
    d2 = P.loc[b2, ["hh", "w", "rgrp", "h_s+1"]]
    hh2 = pd.factorize(d2["hh"])[0]
    G2 = hh2.max() + 1
    H2, w2, rg2 = (d2["h_s+1"] == 2).to_numpy(float), d2["w"].to_numpy(float), d2["rgrp"].to_numpy()
    rng = np.random.default_rng(seed)
    out = []
    for r, rb in (("Black", "B"), ("White", "W"), ("pooled", "pooled")):
        mk = np.ones(len(H), bool) if rb == "pooled" else rg == r
        mk2 = np.ones(len(H2), bool) if rb == "pooled" else rg2 == r
        val = float((H[mk] * w[mk]).sum() / w[mk].sum())
        val2 = float((H2[mk2] * w2[mk2]).sum() / w2[mk2].sum())
        bs, bs2 = [], []
        for _ in range(reps):
            cnt = rng.poisson(1.0, G).astype(float)
            ww = w * cnt[hh]
            bs.append((H[mk] * ww[mk]).sum() / ww[mk].sum())
            cnt2 = rng.poisson(1.0, G2).astype(float)
            ww2 = w2 * cnt2[hh2]
            bs2.append((H2[mk2] * ww2[mk2]).sum() / ww2[mk2].sum())
        se, se2 = float(np.std(bs, ddof=1)), float(np.std(bs2, ddof=1))
        dfn = ("P(husband becomes a job loser other than on temporary layoff -- unemployed, PRUNTYPE 2-3 -- at t+1) among "
               "couples with both spouses employed at t and the husband employed or a job loser at t+1 (37's 'tau' "
               "sample; husbands on temporary layoff at t+1 and wives on layoff at t+1 dropped, as in the cps_jl_nt "
               "target); wife's composite weight; race = husband's race; household block bootstrap (Poisson weights).")
        out.append(dict(block="Base hazards", moment=f"Husband's monthly non-temporary job-loss rate, both employed, {r}",
                        value=val, se=se, n=int(mk.sum()), window="CPS 1994-2023", source_script="IGE/30, 37 (IGE/62)",
                        definition=dfn, id=f"cps_h_hazard_{rb}", data_source="cps", target=1,
                        n_events=int(H[mk].sum()), reps_ok=reps))
        rec("CPS husband hazard (T7)", "cps_h_hazard (monthly), both employed", val, se, int(mk.sum()), "CPS 1994-2023",
            "IGE/62 (IGE/30, 37 panel)", dfn, race=rb)
        rec("CPS husband hazard (T7)", "check: all employed husbands (wife in any state)", val2, se2, int(mk2.sum()),
            "CPS 1994-2023", "IGE/62 (IGE/30 panel)",
            "Same transition among all married husbands employed at t (wife in any labor-force state), husband "
            "employed or a non-temporary job loser at t+1; wife's composite weight.", race=rb)
    pd.DataFrame(out).to_csv(OUT / "paperA_inputs_T7.csv", index=False)
    log("CPS: T7 " + "; ".join(f"{o['id']} {o['value']:.5f} ({o['se']:.5f})" for o in out))
    return out


# =====================================================================================================================
def write_md(fx_new, entry, ctab, found, t7, info):
    L = ["# Paper A model inputs from data (IGE/62.PaperAInputs.py)", "",
         "Run " + time.strftime("%Y-%m-%d %H:%M") + ". Every value below is a coded mapping from data (no hand tuning); "
         "files written: `paperA_model/inputs/fixed_inputs.json` (read by `params.load_fixed()`), "
         "`paperA_model/inputs/psid_entry_couples.csv` (read by `simulate.load_entry()`), "
         "`paperA_model/inputs/psid_entry_couples_25_30.csv`, `paperA_model/inputs/start_overrides.json`, "
         "`output/paperA_inputs_T7.csv`, `output/cps_couple_state_shares.csv`. Regression estimates carry *** p<0.01, "
         "** p<0.05, * p<0.1.", ""]
    L += ["## Values written to fixed_inputs.json", "", "```json", json.dumps({k: v for k, v in fx_new.items()
                                                                              if k not in ("status", "source")},
                                                                             indent=1), "```", ""]
    D = pd.DataFrame(ROWS)
    for blk, q in D.groupby("block", sort=False):
        L += [f"## {blk}", "", "| Item | Race | Value | s.e. | p | N | Note | Window | Source |",
              "|---|---|---:|---:|---:|---:|---|---|---|"]
        for _, r in q.iterrows():
            v = r["value"]
            vs = f"{v:.5g}" if isinstance(v, (float, np.floating)) else str(v)
            se = "" if not np.isfinite(r["se"]) else f"{r['se']:.3g}"
            pv = ""
            if np.isfinite(r["p"]):
                vs += stars(r["p"])
                pv = f"{r['p']:.3g}"
            n = "" if not np.isfinite(r["n"]) else f"{int(r['n']):,}"
            L.append(f"| {r['item']} | {r['race']} | {vs} | {se} | {pv} | {n} | {r['note']} | {r['window']} | "
                     f"{r['source']} |")
        L += ["", "Definitions:", ""] + [f"- {d}" for d in pd.unique(q["definition"])] + [""]
    # entry population summary
    e = entry
    L += ["## Entry population (psid_entry_couples.csv)", "",
          "Definition: every PSID couple (male head with a wife present, head Black or White) enters at its first "
          "interview from 1984 on at which the wife's interview age is 25-59 (couples together before 1984 enter in "
          "1984; couples formed before the wife is 25 enter at the first wave with her aged 25+), the model's "
          "'January of the year of first observation' (sec7_model.tex). year0 = interview year; age0 = wife's interview "
          "age. Employment = interview status working or temporarily laid off (head: family-file status item; wife: "
          "23's status item), else >= 260 annual hours if the item is missing. UI state = not employed and an own "
          "displacement (closure, layoff / firing; 19's / 23's dating) in the interview year or the year before. "
          "Human capital level h = 4 + round((ln w - mu_j(r)) / psi_j) truncated to 1-7, with ln w the log hourly wage "
          "of the income year before the interview (>= 260 hours, $2-$200), else the same person's last wage in the "
          "previous five years, else the regression prediction above (transitory shock ignored). k0 = youngest child in "
          "the family unit at the interview (none / 0-5 / 6-17). a0 = liquid wealth (thousand 2000 $) at the entry "
          "wave if a wealth wave, else the couple's own value within +-2 waves-years, else the median of its cell "
          "(wife's age 25-34 / 35-44 / 45-59 x race x the higher spouse's education <= 12 / 13-15 / 16+) at the nearest "
          "wealth wave (wealth waves 1984, 1989, 1994, 1999-2019). s = workplace match at entry (below), else at the "
          "couple's first later wave with both spouses' codes, else 0. The file `psid_entry_couples_25_30.csv` keeps "
          "the couples entering at the wife's age 25-30.", ""]
    L.append(f"- Couples: {len(e):,} ({(e.race == 0).sum():,} Black, {(e.race == 1).sum():,} White); entering in 1984: "
             f"{(e.year0 == 1984).sum():,}; entering at wife's age 25-30: {e.age0.between(25, 30).sum():,}.")
    ab = json.loads((INPUTS / "start_overrides.json").read_text())["theta"]["a_bar"]
    L.append(f"- Share of entry couples with a0 below the start borrowing limit -a_bar = {-ab:.1f} (the simulator clips "
             f"a0 to the asset grid): {(e.a0 < -ab).mean():.3f}; a0 percentiles 10/50/90: "
             + "/".join(f"{v:.1f}" for v in e.a0.quantile([0.1, 0.5, 0.9])) + " thousand 2000 $.")
    for nm, col in (("s source", "s_src"), ("a0 source", "a0_src"), ("wife's wage source", "hw0_src"),
                    ("husband's wage source", "hh0_src")):
        vc = e[col].value_counts(normalize=True)
        L.append(f"- {nm}: " + "; ".join(f"{k} {v:.3f}" for k, v in vc.items()))
    g = e.groupby("race")
    L += ["", "| | Black | White |", "|---|---:|---:|"]
    for lab, f in (("mean age0", lambda q: q.age0.mean()), ("share s = 0 / 1 / 2", lambda q: "/".join(
            f"{(q.s == k).mean():.3f}" for k in (0, 1, 2))), ("wife employed", lambda q: q.ew0.mean()),
                   ("husband employed", lambda q: q.eh0.mean()), ("wife UI state", lambda q: q.uw0.mean()),
                   ("husband UI state", lambda q: q.uh0.mean()), ("k0 = 0 / 1 / 2", lambda q: "/".join(
            f"{(q.k0 == k).mean():.3f}" for k in (0, 1, 2))), ("median a0 (thousand 2000 $)", lambda q: q.a0.median()),
                   ("share a0 <= 0", lambda q: (q.a0 <= 0).mean()), ("mean hw0", lambda q: q.hw0.mean()),
                   ("mean hh0", lambda q: q.hh0.mean()),
                   ("hw0 = 1 / 7 shares", lambda q: f"{(q.hw0 == 1).mean():.3f}/{(q.hw0 == 7).mean():.3f}"),
                   ("hh0 = 1 / 7 shares", lambda q: f"{(q.hh0 == 1).mean():.3f}/{(q.hh0 == 7).mean():.3f}")):
        vb, vw = f(e[e.race == 0]), f(e[e.race == 1])
        fm = (lambda v: f"{v:.3f}" if isinstance(v, (float, np.floating)) else str(v))
        L.append(f"| {lab} | {fm(vb)} | {fm(vw)} |")
    L += ["", "## Workplace match coding (CPS analog)", "",
          "CPS (IGE/37): s = 2 if the spouses share the detailed industry recode (PRDTIND1), the detailed occupation "
          "recode (PRDTOCC1) and the class of worker (PEIO1COW, 8 codes); s = 1 same detailed industry only. PSID analog "
          "coded here on both spouses' main jobs at the interview: industry = the CPS 2003+ detailed industry recode "
          "(51 groups + armed forces) mapped from the PSID 3-digit Census codes (1970 codes in waves to 2001, 2000 codes "
          "x 10 in 2003-2015, 2012 codes from 2017; code ranges in IND70 / IND4); occupation = the CPS 1994-2002 "
          "detailed occupation recode (46 groups of the 1990 classification) on 1970 codes (waves to 2001) and the CPS "
          "2003+ recode (23 SOC major groups) on 2000 / 2010 codes (2003+), as the CPS panel itself switches recodes in "
          "2003; class of worker = private / government / self-employed from 'work for self or others' and 'work for "
          "government' (the PSID does not separate federal / state / local or for-profit / nonprofit, so s = 2 is "
          "coarser than the CPS cell: the plan's 'approximate'). Defined when both spouses are employed with valid "
          "codes.", ""]
    L += ["Family-file items read here (per wave):", "", found.to_markdown(index=False), ""]
    (OUT / "paperA_inputs.md").write_text("\n".join(L), encoding="utf8")


# =====================================================================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=200)
    ap.add_argument("--skip-cps", action="store_true")
    a = ap.parse_args()
    sys.path.insert(0, str(HERE / "paperA_model"))
    import params as PA                                     # read-only import (FIXED_DEFAULTS: BPS transitory variances)
    fx = PA.FIXED_DEFAULTS
    t7 = None if a.skip_cps else cps_part(a.reps)
    S = build_psid()
    m = workplace_match(S["m"])
    log("PSID: wage levels and steps")
    wl, info = wage_levels(m, fx)
    models = wage_prediction(m)
    log("PSID: child process, children, childcare, borrowing limit")
    ch, ctab = child_process(m, S["cah"])
    nch = n_children(m)
    pcc = childcare(m)
    abar, p10 = a_bar_start(S["Wl"], m)
    log("PSID: entry population")
    entry = entry_population(m, S["Wl"], {k: wl[k] for k in ("mu_w", "mu_h")}, {k: wl[k] for k in ("psi_w", "psi_h")},
                             models)
    # workplace-match shares P(s | r): entry couples, and both-employed couple-years (CPS-comparable check)
    share = {}
    for r, rb in ((0, "B"), (1, "W")):
        q = entry[(entry.race == r) & (entry.s_src != "never both employed: 0")]
        share[rb] = [float((q.s == k).mean()) for k in (0, 1, 2)]
        for k in (0, 1, 2):
            rec("Workplace match shares", f"P(s={k} | r), entry couples with s observed", share[rb][k], np.nan, len(q),
                "PSID 1984-2023 entries", "IGE/62",
                "Share of entry couples by workplace match, among couples with both spouses' codes at entry or later "
                "(couples never observed with both employed get s = 0 in the entry file and are excluded here).",
                race=rb)
        cy = m[m["s_cpl"].notna() & m["year"].between(1984, 2021) & m["w_age"].between(25, 59)
               & (m["hrace"] == ("Black" if r == 0 else "White"))]
        for k in (0, 1, 2):
            rec("Workplace match shares", f"check: P(s={k} | r), both-employed couple-years", float((cy.s_cpl == k).mean()),
                np.nan, len(cy), "PSID 1984-2021", "IGE/62",
                "Share among married couple-years with both spouses employed and coded (CPS-comparable check; CPS "
                "pooled shares 0.823 / 0.114 / 0.063 among both-employed couples, IGE/60 cps_share_s0-s2).", race=rb)
    fx_new = {"mu_w": wl["mu_w"], "mu_h": wl["mu_h"], "psi_w": wl["psi_w"], "psi_h": wl["psi_h"],
              "b0_annual": ch["b0_annual"], "b2_annual": ch["b2_annual"], "n_children": nch,
              "p_cc": [float(v) for v in pcc], "share_s": share,
              "status": {k: "IGE/62 (data)" for k in ("mu_w", "mu_h", "psi_w", "psi_h", "b0_annual", "b2_annual",
                                                       "n_children", "p_cc", "share_s")},
              "source": "IGE/62.PaperAInputs.py; values, windows and definitions in output/paperA_inputs.md"}
    INPUTS.mkdir(parents=True, exist_ok=True)
    (INPUTS / "fixed_inputs.json").write_text(json.dumps(fx_new, indent=1))
    entry.to_csv(INPUTS / "psid_entry_couples.csv", index=False)
    entry[entry.age0.between(25, 30)].to_csv(INPUTS / "psid_entry_couples_25_30.csv", index=False)
    (INPUTS / "start_overrides.json").write_text(json.dumps(
        {"theta": {"a_bar": abar}, "source": {"a_bar": f"IGE/62: minus P10 of liquid wealth of couples with the wife "
                                                         f"25-34 (P10 = {p10:,.0f} 2000 $), thousand 2000 $"}}, indent=1))
    pd.DataFrame(ROWS).to_csv(OUT / "paperA_inputs.csv", index=False)
    write_md(fx_new, entry, ctab, S["found"], t7, info)
    log("done: " + json.dumps({k: v for k, v in fx_new.items() if k in ("mu_w", "mu_h", "psi_w", "psi_h", "p_cc",
                                                                       "share_s")}))


if __name__ == "__main__":
    main()
