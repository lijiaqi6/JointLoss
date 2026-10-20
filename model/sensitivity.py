r"""Sensitivity of the race parameters and of the H4 counterfactual to the moments, in the sense of Andrews, Gentzkow
and Shapiro (2017), from the saved Jacobians (Fable 3-hour plan, Block 5, 2026-10-19). No simulation.

Lambda = (J'WJ)^{-1} J'W with W = diag(1/sd^2), J the numerical Jacobian of the 66 moments at the estimate (R = 20):
the derivative of the estimate with respect to the data moments (AGS's Lambda has the opposite sign because it is
written for a perturbation of the model's moments).
S_jk = Lambda_jk sd_k / se_j: the shift of parameter j, in its own standard errors, when moment k moves by one data
standard error. For the counterfactual c (H4 off, change in the W - B gap at 45-49) the row is g' Lambda with g its
gradient. Reported: the share of sum_k S_jk^2 in each moment block and the six moments with the largest |S_jk|.
Writes output/final_x4/sensitivity.json."""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import core  # noqa: E402

F = HERE / "output" / "final_x4"
BLOCKS = {"IGE": ("ige_",), "returns to schooling": ("rets_",), "levels and variances": ("mlw", "vlw"),
          "G shares": ("G_",), "stayer growth": ("gst", "vgst", "acgst"),
          "moves and displacement": ("mov", "dsp", "gmv", "gds"), "zero hours": ("zero",)}
D = json.load(open(HERE / "output" / "data_moments.json"))
SD = np.array(D["sd"])
NAMES = core.MOMENT_NAMES


def lam(model):
    e = json.load(open(F / f"estimates_{model}.json"))[model]
    J = np.array(e["jacobian"])
    W = np.diag(1 / SD ** 2)
    Lm = np.linalg.solve(J.T @ W @ J, J.T @ W)
    assert np.allclose(Lm @ J, np.eye(J.shape[1]), atol=1e-6), "Lambda J != I"
    return Lm, e["jac_names"], e


def summarise(row, scale):
    S = row * SD / scale
    tot = float(np.sum(S ** 2))
    shares = {b: float(sum(S[i] ** 2 for i, n in enumerate(NAMES) if n.startswith(pre)) / tot) for b, pre in BLOCKS.items()}
    top = sorted(range(len(NAMES)), key=lambda i: -abs(S[i]))[:6]
    return {"block_shares": shares, "top": [(NAMES[i], float(S[i])) for i in top], "S": S.tolist()}


if __name__ == "__main__":
    out = {}
    for model, pars in (("E", ("dgx", "gx", "dg1", "db1")), ("D", ("a3",))):
        Lm, nm, e = lam(model)
        for p in pars:
            j = nm.index(p)
            out[f"{p} ({model})"] = summarise(Lm[j], e["se"][p])
    pe = json.load(open(HERE / "output" / "postestimation_Lx4_E_h4.json"))
    Lm, nm, e = lam("E")
    assert pe["grad_names"] == nm, "gradient and Jacobian parameters differ"
    rec = pe["cf"]["Equal pay-off of parental income in accumulation (dgx = 0)"]["gap_4549"]
    out["H4 off: change in the gap at 45-49"] = summarise(np.array(rec["grad"]) @ Lm, rec["se"])
    json.dump(out, open(F / "sensitivity.json", "w"), indent=1)
    for k, v in out.items():
        print(k, {b: round(s, 2) for b, s in v["block_shares"].items()})
        print("   top:", ", ".join(f"{n} {s:+.2f}" for n, s in v["top"]))
