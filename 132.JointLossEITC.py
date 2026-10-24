r"""Joint job loss and the EITC: does a couple's joint job loss take away the credit? (PI question for Paper A, 2026-10-24)

The EITC is based on the year's earned income (wages and self-employment), not on unemployment benefits; it rises
with earnings in the phase-in, is flat on the plateau and falls in the phase-out, and is paid the next spring. A
husband's job loss with the wife still working usually keeps the family on the schedule, so the credit can rise
(phase-out) or stay; a joint loss removes the second earner, so the credit can fall to zero or be cut in the phase-in.
UNITS: 25.JointJobLoss.py's father x stack units (married male heads with a child 0-17 at baseline; baseline = the
  latest of ev-1, ev-2 with positive hours), husband's first displacement in ev 1984-2021, wife employed at baseline:
  JOINT = the baseline wife displaced (her own report, code 1 / 3) in ev-1 .. ev+1 (25's wife_events); HUSBAND ONLY =
  the others; CONTROLS = 25's clean controls (no displacement up to ev+6) at the same baseline rules.
CREDIT: the federal EITC at the couple's actual earned income (head + wife labor income, nominal), the family's number
  of children (capped at 3) and the year's schedule for joint filers (61's table; 127's credit()); state credits and
  the AGI test with UI income are left out (UI can only lower the credit in the phase-out). Years: baseline, ev and
  ev+1 (the first observed of ev+1, ev+2 in the biennial years).
OUTCOMES: credit received (2000 dollars); eligible (credit > 0); zero earned income; change from baseline classed as
  lost (eligible -> 0), cut (down by $100+), unchanged, raised (up by $100+), gained (0 -> eligible), never.
Writes output/joint_loss_eitc.md / .json (aggregates only). DESCRIPTIVE; unweighted, as 25.
"""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import CPI, DATA, OUT  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R25 = _load("s25", "25.JointJobLoss.py")
R127 = _load("s127", "127.EITCMothers.py")
RES = {}


def classify(b, a):
    if not np.isfinite(b) or not np.isfinite(a):
        return "n/a"
    if b > 0 and a == 0:
        return "lost"
    if b == 0 and a > 0:
        return "gained"
    if b == 0 and a == 0:
        return "never"
    if a < b - 100:
        return "cut"
    if a > b + 100:
        return "raised"
    return "unchanged"


def main():
    py = pd.read_pickle(DATA / "psid_person_year.pkl")
    E = R25.P23.extras()
    ev_sets = R25.wife_events(py, E["R"])
    fam = R25.psid9.family()
    d = pd.read_pickle(DATA / "psid_displacement.pkl")
    m = R25.P19.men_panel(py, fam)
    wl = py[py["head"]][["wave", "int", "wlab"]].drop_duplicates(["wave", "int"])
    m = m.merge(wl, on=["wave", "int"], how="left").drop_duplicates(["pid", "year"])
    U = R25.build_units(m, d)
    U = U[(U["pseudo"] == 0) & (U["wemp0"] == 1) & U["ev"].between(1984, 2021)].copy()
    dm = ev_sets["main"]
    U["joint"] = [int(any((int(w), int(y)) in dm for y in (e - 1, e, e + 1))) if pd.notna(w) else 0
                  for w, e in zip(U["w0"], U["ev"])]
    U["grp"] = np.where(U["treat"] == 0, "controls", np.where(U["joint"] == 1, "joint loss", "husband only"))
    P = m.set_index(["pid", "year"])[["hlab", "wlab", "nkid"]]

    def credit_at(pid, y):
        if (pid, y) not in P.index or y not in CPI:
            return np.nan, np.nan
        row = P.loc[(pid, y)]
        if isinstance(row, pd.DataFrame):
            row = row.iloc[0]
        earn = float(np.nansum([row["hlab"], row["wlab"]]))
        nom = earn * CPI[y] / CPI[2000]
        n = int(min(max(row["nkid"], 0), 3)) if pd.notna(row["nkid"]) else 0
        return R127.credit(nom, n, int(y), True) * CPI[2000] / CPI[y], earn

    rows = []
    for pid, ev, grp in zip(U["pid"], U["ev"], U["grp"]):
        b = next(((y, *credit_at(pid, y)) for y in (ev - 1, ev - 2) if (pid, y) in P.index), (np.nan, np.nan, np.nan))
        e0 = credit_at(pid, ev)
        e1 = next((credit_at(pid, y) for y in (ev + 1, ev + 2) if (pid, y) in P.index), (np.nan, np.nan))
        rows.append({"grp": grp, "c_b": b[1], "y_b": b[2], "c_0": e0[0], "y_0": e0[1], "c_1": e1[0], "y_1": e1[1]})
    D = pd.DataFrame(rows)
    D["k0"] = [classify(b, a) for b, a in zip(D["c_b"], D["c_0"])]
    D["k1"] = [classify(b, a) for b, a in zip(D["c_b"], D["c_1"])]
    md = ["# Joint job loss and the EITC (PI question for Paper A)", "",
          "Built by `132.JointLossEITC.py` (2026-10-24); design in its docstring. Federal EITC imputed at the couple's "
          "actual earned income; married fathers with a child 0-17, wife employed at baseline, husband's first "
          "displacement 1984-2021 (25's units); unweighted. **Descriptive.**", ""]
    md += ["## 1. The credit and earned income around the husband's displacement", "",
           "| group | families | eligible: baseline / ev / ev+1 | mean credit (2000 $): baseline / ev / ev+1 | zero "
           "earned income: ev / ev+1 | mean earned income (2000 $): baseline / ev / ev+1 |", "|---|---|---|---|---|---|"]
    for g in ("joint loss", "husband only", "controls"):
        q = D[D["grp"] == g]
        el = [float((q[c] > 0).mean()) for c in ("c_b", "c_0", "c_1")]
        mc = [float(q[c].mean()) for c in ("c_b", "c_0", "c_1")]
        z = [float((q[c] == 0).mean()) for c in ("y_0", "y_1")]
        my = [float(q[c].mean()) for c in ("y_b", "y_0", "y_1")]
        md.append(f"| {g} | {len(q):,} | " + " / ".join(f"{x:.3f}" for x in el) + " | "
                  + " / ".join(f"{x:,.0f}" for x in mc) + " | " + " / ".join(f"{x:.3f}" for x in z) + " | "
                  + " / ".join(f"{x:,.0f}" for x in my) + " |")
        RES[f"levels|{g}"] = {"n": len(q), "eligible": el, "credit": mc, "zero_earn": z, "earn": my}
    for when, k in (("event year (ev)", "k0"), ("the year after (ev+1)", "k1")):
        md += ["", f"## 2. Change in the credit from baseline to {when}", "",
               "| group | lost (eligible -> 0) | cut | unchanged | raised | gained (0 -> eligible) | never eligible | "
               "families with both years |", "|---|---|---|---|---|---|---|---|"]
        for g in ("joint loss", "husband only", "controls"):
            q = D[(D["grp"] == g) & (D[k] != "n/a")]
            sh = {c_: float((q[k] == c_).mean()) for c_ in ("lost", "cut", "unchanged", "raised", "gained", "never")}
            md.append(f"| {g} | " + " | ".join(f"{sh[c_]:.3f}" for c_ in sh) + f" | {len(q):,} |")
            RES[f"change|{k}|{g}"] = {**sh, "n": len(q)}
            el = q[q["c_b"] > 0]
            if len(el):
                RES[f"change|{k}|{g}|eligible_at_baseline"] = {c_: float((el[k] == c_).mean())
                                                               for c_ in ("lost", "cut", "unchanged", "raised")}
        md += ["", "Among families eligible at baseline: " + "; ".join(
            f"{g}: lost {RES[f'change|{k}|{g}|eligible_at_baseline']['lost']:.3f}, cut "
            f"{RES[f'change|{k}|{g}|eligible_at_baseline']['cut']:.3f}, raised "
            f"{RES[f'change|{k}|{g}|eligible_at_baseline']['raised']:.3f}"
            for g in ("joint loss", "husband only", "controls") if f"change|{k}|{g}|eligible_at_baseline" in RES) + "."]
    md.append("")
    (OUT / "joint_loss_eitc.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    json.dump(RES, open(OUT / "joint_loss_eitc.json", "w"), indent=1, default=float)
    print("\n".join(md))


if __name__ == "__main__":
    main()
