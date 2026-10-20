r"""Verification of the BPS-on-simulated-data harness (bps_reconciliation, 2026-10-18). Results: HARNESS.md.

  python verify_harness.py roundtrip <WORK_NEW>/<spec> <WORK_REF>/<spec>
      every number of every run (est_gmm10 / est_gmm9 / est_beta) of the harness run vs the reference run of
      run_spec.do (Step 0 / Step 1 work folders), plus the key row vs BPS's published Tables 3, 4 (col. 1, 5) and the
      p. 425 chain and split, at the published rounding.
  python verify_harness.py smoke <WORK>/<spec> <truth.json>
      Table 3 (all ages) of a harness run on a synthetic panel vs the variances of the data-generating process.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from compile_results import PUB_T3, PUB_T4, PUB_T5, PUB_CHAIN  # noqa: E402

RUNS = ("gmm10", "gmm9", "beta")


def compare_runs(new, ref):
    out = []
    for r in RUNS:
        a = pd.read_csv(Path(new) / f"est_{r}.csv").set_index("_varname")
        b = pd.read_csv(Path(ref) / f"est_{r}.csv").set_index("_varname")
        j = a[["value", "se"]].join(b[["value", "se"]], rsuffix="_ref", how="outer")
        for c in ("value", "se"):
            d = (j[c] - j[c + "_ref"]).abs()
            both_nan = j[c].isna() & j[c + "_ref"].isna()
            one_nan = j[c].isna() ^ j[c + "_ref"].isna()
            out.append(dict(run=r, field=c, n=int((~both_nan).sum()), n_one_missing=int(one_nan.sum()),
                            max_abs_diff=float(d.max(skipna=True)) if d.notna().any() else 0.0,
                            n_diff_gt_1e7=int((d > 1e-7).sum())))
    return pd.DataFrame(out)


def vs_published(row_csv):
    k = pd.read_csv(row_csv).iloc[0]
    rows = []
    names = {"s_u1": "s_u1", "s_v1": "s_v1", "s_u2": "s_u2", "s_v2": "s_v2", "r_u1u2": "c_u1u2", "r_v1v2": "c_v1v2"}
    for p, col in names.items():
        for a in range(6):
            c = f"T3a{a + 1}_{col}" if a < 5 else f"T3_{col}"
            pub = PUB_T3[p][a][0]
            rows.append(dict(table="T3", cell=c, published=pub, harness=k[c], rounded=round(k[c], 4),
                             match=abs(k[c] - pub) <= 1.0001e-4))
    t4 = {"pi": "E_pi", "s_report": "E_s", "eta_c_p": "eta_c_p", "eta_h1_w1": "eta_h1_w1", "eta_h2_w2": "eta_h2_w2",
          "eta_c_w1": "eta_c_w1", "eta_h1_p": "eta_h1_p", "eta_c_w2": "eta_c_w2", "eta_h2_p": "eta_h2_p",
          "eta_h1_w2": "eta_h1_w2", "eta_h2_w1": "eta_h2_w1"}
    for p, col in t4.items():
        pub = PUB_T4[p][0][0]
        rows.append(dict(table="T4c1", cell=col, published=pub, harness=k[col], rounded=round(k[col], 3),
                         match=abs(k[col] - pub) <= 1.0001e-3))
    rows.append(dict(table="T4c5", cell="beta", published=-0.137, harness=k["beta"], rounded=round(k["beta"], 3),
                     match=abs(k["beta"] + 0.137) <= 1.0001e-3))
    rows.append(dict(table="T4", cell="N_gmm", published=7295, harness=k["N_gmm"], rounded=k["N_gmm"],
                     match=k["N_gmm"] == 7295))
    m5 = {"ch_f_h1u1": "F_h1u1", "ch_f_h2u2": "F_h2u2", "ch_f_h1u2": "F_h1u2", "ch_f_h2u1": "F_h2u1",
          "ch_f_cu1": "F_cu1", "ch_f_cu2": "F_cu2", "ch_m_h1v1": "M_h1v1", "ch_m_h2v2": "M_h2v2",
          "ch_m_h1v2": "M_h1v2", "ch_m_h2v1": "M_h2v1", "ch_m_cv1": "M_cv1", "ch_m_cv2": "M_cv2"}
    for p, _lab, pub, _se in PUB_T5:
        col = m5[p]
        rows.append(dict(table="T5c1", cell=col, published=pub, harness=k[col], rounded=round(k[col], 2),
                         match=abs(k[col] - pub) <= 1.0001e-2))
    for p, _lab, pub in PUB_CHAIN:
        dec = 1 if p[3] in "cf" and p[4:].isdigit() else 2
        rows.append(dict(table="chain", cell=p, published=pub, harness=k[p], rounded=round(k[p], dec),
                         match=abs(k[p] - pub) <= 1.0001 * 10.0 ** -dec))
    return pd.DataFrame(rows)


def smoke(spec_dir, truth_json):
    t = json.loads(Path(truth_json).read_text())
    k = pd.read_csv(Path(spec_dir) / "bps_on_sim_row.csv").iloc[0]
    rows = []
    for c in ("s_u1", "s_v1", "s_u2", "s_v2", "c_u1u2", "c_v1v2"):
        v, se = k[f"T3_{c}"], k[f"T3_{c}_se"]
        rows.append(dict(param=c, truth=t[c], estimate=v, se=se, z=(v - t[c]) / se if se > 0 else np.nan))
    for c in ("rho_u1u2", "rho_v1v2"):
        rows.append(dict(param=c, truth=t[c], estimate=k[c], se=np.nan, z=np.nan))
    return pd.DataFrame(rows), k


if __name__ == "__main__":
    pd.set_option("display.width", 200)
    if sys.argv[1] == "roundtrip":
        cmp = compare_runs(sys.argv[2], sys.argv[3])
        print(cmp.to_string(index=False))
        if len(sys.argv) < 5 or sys.argv[4] != "nopub":
            pub = vs_published(Path(sys.argv[2]) / "bps_on_sim_row.csv")
            print(pub.to_string(index=False))
            print("published cells matched:", int(pub["match"].sum()), "of", len(pub))
    elif sys.argv[1] == "smoke":
        tab, k = smoke(sys.argv[2], sys.argv[3])
        print(tab.to_string(index=False))
        print(k[["N_input", "N_sample", "N_duw", "N_duww", "N_gmm", "E_pi", "E_s", "eta_h1_w1", "eta_h2_w2",
                 "M_h2v1", "M_cv1", "ch_gov", "ch_fam", "ch_sav", "n_trim_minw", "n_trim_jump"]].to_string())
