r"""Fit of the selected model (E) to the moments that carry the puzzle (Paper B, Fable second plan Block 3,
2026-10-19): (A) the log-wage IGE by age band and race, (B) the return to schooling by band and race, (C) the White -
Black gap in the IGE. PSID points with 95% intervals (500 cluster-bootstrap draws, output/boot_moments.npy; the gap's
interval from the same draws), model E's values as lines (output/final_x4/estimates_E.json). Colours: the paper's
series colours (reference palette slots 1-2, as in 31.PaperBFigure.py). Writes
paperB_age_profile/fig_model_fit.png and .pdf."""
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import core  # noqa: E402

COL = {"White": "#2a78d6", "Black": "#eb6834"}
INK, MUTED, GRID, GAP = "#1f1f1e", "#6b6a64", "#e4e3de", "#52514e"
BANDS = ["2529", "3034", "3539", "4044", "4549", "5055"]
MID = [27, 32, 37, 42, 47, 52.5]
LAB = ["25-29", "30-34", "35-39", "40-44", "45-49", "50-55"]

D = json.load(open(HERE / "output" / "data_moments.json"))
B = np.load(HERE / "output" / "boot_moments.npy")
MD, SD = dict(zip(core.MOMENT_NAMES, D["m"])), dict(zip(core.MOMENT_NAMES, D["sd"]))
MM = dict(zip(core.MOMENT_NAMES, json.load(open(HERE / "output" / "final_x4" / "estimates_E.json"))["E"]["moments"]))
IX = {n: i for i, n in enumerate(core.MOMENT_NAMES)}


def style(ax, title, ylabel):
    ax.set_title(title, loc="left", fontsize=10.5, color=INK, pad=8)
    ax.set_ylabel(ylabel, color=MUTED, fontsize=9)
    ax.set_xticks(MID, LAB)
    ax.set_xlabel("Son's age band", color=MUTED, fontsize=9)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=8)


def panel(ax, stem, title, ylabel):
    for race, r in (("White", "W"), ("Black", "B")):
        d = np.array([MD[f"{stem}_{b}_{r}"] for b in BANDS])
        s = np.array([SD[f"{stem}_{b}_{r}"] for b in BANDS])
        m = np.array([MM[f"{stem}_{b}_{r}"] for b in BANDS])
        off = -0.5 if r == "W" else 0.5
        ax.errorbar(np.array(MID) + off, d, yerr=1.96 * s, fmt="o", color=COL[race], markersize=5, linewidth=1.2,
                    capsize=0, zorder=3)
        ax.plot(MID, m, color=COL[race], linewidth=2, zorder=2)
        ax.text(MID[-1] + 1.2, m[-1], race, color=INK, fontsize=8.5, va="center")
    style(ax, title, ylabel)
    ax.set_xlim(24, 57.5)


if __name__ == "__main__":
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.9))
    panel(axes[0], "ige", "A. Log-wage IGE by age", "coefficient on log parental income")
    panel(axes[1], "rets", "B. Return to schooling by age", "coefficient on years of schooling")
    ax = axes[2]
    gd = np.array([MD[f"ige_{b}_W"] - MD[f"ige_{b}_B"] for b in BANDS])
    gs = np.array([np.std(B[:, IX[f"ige_{b}_W"]] - B[:, IX[f"ige_{b}_B"]], ddof=1) for b in BANDS])
    gm = np.array([MM[f"ige_{b}_W"] - MM[f"ige_{b}_B"] for b in BANDS])
    ax.errorbar(MID, gd, yerr=1.96 * gs, fmt="o", color=GAP, markersize=5, linewidth=1.2, capsize=0, zorder=3)
    ax.plot(MID, gm, color=GAP, linewidth=2, zorder=2)
    ax.axhline(0, color=MUTED, linewidth=0.8)
    style(ax, "C. White $-$ Black gap in the IGE", "difference in coefficients")
    ax.set_xlim(24, 57.5)
    handles = [plt.Line2D([], [], color=MUTED, marker="o", linewidth=0, markersize=5, label="PSID (95% interval)"),
               plt.Line2D([], [], color=MUTED, linewidth=2, label="Model E")]
    fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False, fontsize=9, bbox_to_anchor=(0.5, -0.04))
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    for ext in ("png", "pdf"):
        fig.savefig(HERE.parent / "paperB_age_profile" / f"fig_model_fit.{ext}", dpi=200, bbox_inches="tight")
    print("figure written")
