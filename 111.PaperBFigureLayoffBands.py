r"""Figure: a father's teen layoff and closure, and his son's and daughter's ln hourly wage, by age band (Paper B,
restructured outline, Figure 2).

92.LayoffDaughters.py's reduced specification (ln parental income; the father's teen-window ln wage, ln hours,
unemployment, zero-hours and volatility measures, closure share and layoff share; single-age dummies; PSID weights;
father present), one regression per sex and band (25-29 ... 50-55), s.e. clustered by 1968 family. Plotted: the
layoff coefficient for sons and daughters and the closure coefficient for sons, with 95% intervals.
Colours: the reference categorical palette of the dataviz skill (slots 1-3), with distinct markers and line styles so
the series read in print and without colour.
Writes output/paperB_layoff_bands.pdf / .png and output/paperB_layoff_bands.json (aggregates only).
"""
import importlib.util
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import OUT  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R107 = _load("s107", "107.LayoffSexDifference.py")
R92, R24 = R107.R92, R107.R24
dummies, ols_cl, FATHER = R92.dummies, R92.ols_cl, R92.FATHER
BL = ["25-29", "30-34", "35-39", "40-44", "45-49", "50-55"]
INK, MUTED, GRID = "#2b2b29", "#6b6a63", "#e4e2dc"
COL = {"sons": "#2a78d6", "daughters": "#eb6834", "closure": "#1baf7a"}


def bands(r, female, y="lw"):
    out = {"layoff": [], "closure": []}
    d = r[(r["female"] == female)].dropna(subset=[y, "lyp"] + FATHER)
    for k in range(6):
        z = d[d["band"] == k]
        X = np.column_stack([z[["lyp"] + FATHER].to_numpy(float), dummies(z["age"]), np.ones(len(z))])
        b, V = ols_cl(X, z[y].to_numpy(float), z["wt"].to_numpy(float), z["fam68"].to_numpy())
        for name, col in (("layoff", "f_sh_layoff"), ("closure", "f_sh_close")):
            j = 1 + FATHER.index(col)
            out[name].append([float(b[j]), float(np.sqrt(V[j, j]))])
    return out


def main():
    a, py, ch = R24.load()
    r = R107.frame(a, py, ch)
    S, D = bands(r, 0), bands(r, 1)
    json.dump({"sons": S, "daughters": D}, open(OUT / "paperB_layoff_bands.json", "w"), indent=1)
    x = np.arange(6)
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    fig.patch.set_facecolor("white")
    ax.axhline(0, color=MUTED, lw=1)
    series = [("sons", S["layoff"], "o", "-", -0.12, "Sons: father laid off or fired"),
              ("daughters", D["layoff"], "s", "-", 0.0, "Daughters: father laid off or fired"),
              ("closure", S["closure"], "^", "--", 0.12, "Sons: father's plant closed")]
    for key, est, mk, ls, dx, lab in series:
        e = np.array(est)
        ax.errorbar(x + dx, e[:, 0], yerr=1.96 * e[:, 1], color=COL[key], marker=mk, ms=6, lw=2, ls=ls, capsize=0,
                    elinewidth=1.2, label=lab, markeredgecolor="white", markeredgewidth=1)
        ax.annotate(lab.split(":")[0] + (" (closure)" if key == "closure" else ""), (x[-1] + dx, e[-1, 0]),
                    xytext=(8, 0), textcoords="offset points", va="center", fontsize=8.5, color=INK)
    ax.set_xticks(x, BL)
    ax.set_xlim(-0.4, 6.1)
    ax.set_xlabel("Child's age", color=INK)
    ax.set_ylabel("Coefficient on the father's teen share\n(ln hourly wage, per unit share)", color=INK)
    ax.grid(axis="y", color=GRID, lw=0.8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=INK, labelsize=9)
    ax.legend(frameon=False, fontsize=8.5, loc="lower left")
    fig.tight_layout()
    fig.savefig(OUT / "paperB_layoff_bands.pdf")
    fig.savefig(OUT / "paperB_layoff_bands.png", dpi=160)
    print({k: [round(v[0], 3) for v in S["layoff"]] for k in ["sons"]}, {k: [round(v[0], 3) for v in D["layoff"]] for k in ["daughters"]})


if __name__ == "__main__":
    main()
