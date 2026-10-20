r"""Parental income net of the father's search friction: the 'clean' moment set (PI, 2026-10-19; Section 8, "Search
frictions in two generations"; EVIDENCE 11.24).

x_clean = x + (father's mean log family income over his clean window years - over all his window years; f_lfam_cA -
f_lfam_all), where clean = no displacement, no unemployment and not zero hours (24.IGEDecomposition.py's cleanA, both read through 36.SameEmployerGrowthChecks.py's
son panel). Sons without a resident father, or whose father has no clean year or no window income, keep x: no father's
spell to remove. All 4,765 model sons are kept.
Writes (person-level, git-ignored): the column x_clean in output/sons_types.csv; prints aggregates only. Then
`IGE_MOMENTS=clean python moments_set.py` builds data_moments_clean.json and boot_moments_clean.npy with the clean x
and its own terciles and mean (estimate.py reads them for the set).
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
IGE = HERE.parent


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, IGE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def x_clean_map():
    sys.path.insert(0, str(IGE))
    R36 = _load("s36", "36.SameEmployerGrowthChecks.py")
    r, *_ = R36.psid_build()
    f = r.drop_duplicates("pid").set_index("pid")[["f_lfam_all", "f_lfam_cA"]]
    return (f["f_lfam_cA"] - f["f_lfam_all"]).dropna()


if __name__ == "__main__":
    P = pd.read_pickle(HERE / "output" / "data_panel.pkl")
    kid = pd.read_csv(HERE / "output" / "sons_types.csv", float_precision="round_trip")
    first = P.drop_duplicates("pid")
    assert len(first) == len(kid) and np.allclose(first["x"].to_numpy(), kid["x"].to_numpy()), \
        "sons_types.csv rows do not follow data_panel.pkl"
    shift = first["pid"].map(x_clean_map()).fillna(0.0).to_numpy()
    kid["x_clean"] = kid["x"] + shift
    kid.to_csv(HERE / "output" / "sons_types.csv", index=False, float_format="%.17g")
    for b, lab in ((0, "White"), (1, "Black")):
        m = kid["black"] == b
        moved = m & (shift != 0)
        print(f"{lab}: sons {m.sum()}, with a father's clean-year correction {moved.sum()} "
              f"({moved.sum() / m.sum():.2f}); mean shift {shift[moved].mean():+.4f}, s.d. {shift[moved].std():.4f}; "
              f"corr(x, x_clean) {np.corrcoef(kid.loc[m, 'x'], kid.loc[m, 'x_clean'])[0, 1]:.4f}; "
              f"var x {kid.loc[m, 'x'].var():.4f} -> {kid.loc[m, 'x_clean'].var():.4f}")
