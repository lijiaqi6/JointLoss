r"""Paper B headline figure: the age profile of intergenerational persistence, with Chetty et al. (2020) placed on it
(2026-10-17).

Reads output/ige_by_age.csv (built by 26.IGEByAge.py) and writes output/paperB_age_profile.png / .pdf:
  Panel A  log IGE of sons' own earnings (2026-10-18; was family income) at each age 25-50 (one Lee-Solon regression with age interactions, estimated
           on 25-55; ages above 50 not plotted because the age polynomial is unreliable where data are sparse), Black
           and White, 95% confidence bands; the 31-37 window of Chetty et al. (2020) shaded.
  Panel B  rank-rank slope by the child's age band (sons and daughters), with Chetty et al.'s estimates at 31-37
           (Black 0.28, White 0.32; QJE 135(2), p. 721) marked.
  Panel C  expected household income rank of children with parents at the 25th percentile, by age band, with Chetty
           et al.'s estimates (Black 32.6, White 45.2) marked.
Colors: categorical slots 1 (blue, White) and 2 (orange, Black) of the dataviz reference palette; separate panels for
the three measures (no shared or dual axes).
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
D = pd.read_csv(OUT / "ige_by_age.csv")

COL = {"White": "#2a78d6", "Black": "#eb6834"}
INK, MUTED, GRID = "#1f1f1e", "#6b6a64", "#e4e3de"
CHETTY = {"slope": {"Black": 0.28, "White": 0.32}, "E[rank] p25": {"Black": 32.6, "White": 45.2}}
BANDS = ["25-29", "30-34", "35-39", "40-44", "45-49", "50-55"]
MID = {"25-29": 27, "30-34": 32, "35-39": 37, "40-44": 42, "45-49": 47, "50-55": 52.5}


def style(ax, title, ylabel):
    ax.set_title(title, loc="left", fontsize=11, color=INK, pad=8)
    ax.set_ylabel(ylabel, color=MUTED, fontsize=9)
    ax.set_xlabel("Child's age when income is measured", color=MUTED, fontsize=9)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=8.5)
    ax.axvspan(31, 37, color="#f1f0eb", zorder=0)
    ax.set_xlim(24, 56)


def window_label(ax, y):
    ax.text(34, y, "Chetty et al. (2020)\nages 31-37", ha="center", va="top", fontsize=7.5, color=MUTED)


def panel_ige(ax):
    s = D[(D.data == "PSID") & (D.analysis == "Lee-Solon") & (D.sex == "Sons") & (D["sample"] == "unbalanced")
          & (D.outcome == "ln own earnings") & (D.stat == "IGE at age")]
    for race in ("White", "Black"):
        r = s[s.group == race].copy()
        r["age"] = r.band.astype(int)
        r = r[r.age <= 50].sort_values("age")      # the age polynomial is unreliable where data are sparse (> 50)
        ax.fill_between(r.age, r.est - 1.96 * r.se, r.est + 1.96 * r.se, color=COL[race], alpha=0.14, linewidth=0)
        ax.plot(r.age, r.est, color=COL[race], linewidth=2, label=race)
        last = r.iloc[-1]
        ax.text(last.age + 0.6, last.est, race, color=INK, fontsize=8.5, va="center")
    style(ax, "A. Log IGE, sons' own earnings", "Intergenerational elasticity")
    ax.set_ylim(0, 0.75)
    window_label(ax, 0.73)


def panel_rank(ax, stat, title, ylabel, ylim, fmt):
    s = D[(D.data == "PSID") & (D.analysis == "rank") & (D.sex == "Both") & (D["sample"] == "unbalanced")
          & (D.outcome == "ln family income") & (D.stat == stat) & D.band.isin(BANDS)]
    off = {"White": 0.35, "Black": -0.35}
    for race in ("White", "Black"):
        r = s[s.group == race].set_index("band").loc[BANDS].reset_index()
        x = np.array([MID[b] for b in r.band]) + off[race]
        ax.errorbar(x, r.est, yerr=1.96 * r.se, color=COL[race], linewidth=2, marker="o", markersize=6,
                    capsize=0, elinewidth=1.2, label=f"{race} (PSID)")
        c = CHETTY[stat][race]
        ax.errorbar(34, c, xerr=3, color=COL[race], marker="D", markersize=8, markerfacecolor="white",
                    markeredgewidth=2, linewidth=0, elinewidth=2, capsize=0, zorder=5)
        span = ylim[1] - ylim[0]
        below = stat == "slope" and race == "Black"           # keep each label clear of the other series
        ax.text(34, c - 0.035 * span if below else c + 0.035 * span, fmt.format(c), color=INK, fontsize=8,
                ha="center", va="top" if below else "bottom")
    style(ax, title, ylabel)
    ax.set_ylim(*ylim)
    window_label(ax, ylim[1] - 0.02 * (ylim[1] - ylim[0]))


def main():
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.4))
    panel_ige(axes[0])
    panel_rank(axes[1], "slope", "B. Rank-rank slope, sons and daughters", "Rank-rank slope", (0, 0.6), "{:.2f}")
    panel_rank(axes[2], "E[rank] p25", "C. Expected rank, parents at the 25th percentile", "Child's income rank",
               (15, 60), "{:.1f}")
    handles = [plt.Line2D([], [], color=COL["White"], linewidth=2, label="White"),
               plt.Line2D([], [], color=COL["Black"], linewidth=2, label="Black"),
               plt.Line2D([], [], color=MUTED, marker="D", markerfacecolor="white", linewidth=0, markersize=7,
                          label="Chetty et al. (2020), ages 31-37")]
    fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False, fontsize=9, bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"paperB_age_profile.{ext}", dpi=200, bbox_inches="tight")
    print("wrote output/paperB_age_profile.png/.pdf")


if __name__ == "__main__":
    main()
