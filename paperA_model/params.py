"""Paper A structural model: parameter container, fixed inputs, era schedules, solver size switches.

Units inside the model: money in thousands of 2000 dollars per month (the JSON inputs are in 2000 dollars and are
converted on load); time in months; wives' age 25 at t = 0, t = 12 (age - 25) in January (model document Sec. 1).

Three kinds of objects:
  * PARAMS: the 31 SMM parameters (name, start, lower, upper, block), sec7_model.tex Table 'Estimated parameters',
    plus the parameters of the PI-approved extensions of 2026-10-18 (c_mem, eta_up; nested value 0, free only when
    their extension is on in estimate.py).
    Start values come from inputs/start_analytic.json (analytic_start.py) when it exists, otherwise the defaults below
    (marked 'default'; analytic_start.py replaces them by the closed forms of plan Sections 1.4-1.5).
  * FIXED: pre-set inputs (plan Section 1): fixed economics, the wage process (inputs/wage_process.json), the child
    process, number of children, childcare price, workplace-match shares. Every entry that is not yet produced by its
    data script carries status 'PLACEHOLDER' in FIXED_STATUS and is listed in README.md.
  * Config: solver sizes and the fallback switches of plan Section 4.4 (5 human capital levels; s = 1, 2 merged; one
    era in estimation; 20 asset points; no lost-hours record).

Human capital terminology: level / accumulation / depreciation; search friction = job-finding probability lambda.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
INPUTS = HERE / "inputs"
RACES = ("B", "W")

# ------------------------------------------------------------------------------------------------------------------
# The 31 estimated parameters: (name, default start, lower, upper, block). Work costs and stigma are in utility units
# of u(x) = (x^(1-gamma) - 1)/(1-gamma) with x in thousands of 2000 dollars a month per equivalent adult; F and a_bar
# in thousands of 2000 dollars (a month / a stock). Probabilities are monthly. pi_up, pi_dn, d are in units of the
# 7-level grid (with Config.n_hc = 5 the model rescales them so that they keep their log-wage meaning).
# ------------------------------------------------------------------------------------------------------------------
PARAMS = [
    # displacement risk (9)
    ("delta_w_B", 0.0016, 1e-5, 0.03, "displacement"),
    ("delta_w_W", 0.0010, 1e-5, 0.03, "displacement"),
    ("delta_h_B", 0.0026, 1e-5, 0.03, "displacement"),
    ("delta_h_W", 0.0018, 1e-5, 0.03, "displacement"),
    ("pi_c0", 4e-5, 0.0, 0.002, "displacement"),     # upper bound 0.01 -> 0.002 (2026-10-18): the analytic start
                                                      # 3.4e-5 sat within 1% of the range of the lower bound
    ("pi_c1", 3e-4, 0.0, 0.02, "displacement"),
    ("pi_c2", 1e-3, 0.0, 0.05, "displacement"),
    ("p_H", 0.10, 0.01, 0.50, "displacement"),
    ("m_H", 12.0, 1.0, 30.0, "displacement"),
    # search friction (4)
    ("lam_w_B", 0.16, 0.01, 0.90, "search"),
    ("lam_w_W", 0.13, 0.01, 0.90, "search"),
    ("lam_h_B", 0.26, 0.01, 0.90, "search"),
    ("lam_h_W", 0.26, 0.01, 0.90, "search"),
    # human capital (6)
    ("pi_up_w", 0.0095, 0.0005, 0.06, "human_capital"),
    ("pi_up_h", 0.0080, 0.0005, 0.06, "human_capital"),
    ("pi_dn_w", 0.03, 0.0, 0.20, "human_capital"),
    ("pi_dn_h", 0.03, 0.0, 0.20, "human_capital"),
    ("d_w", 0.3, 0.0, 2.0, "human_capital"),
    ("d_h", 0.5, 0.0, 2.0, "human_capital"),
    # work, safety net, marriage, credit (12)
    ("phi_F", 0.10, -0.5, 1.0, "work"),
    ("phi_P", 0.05, -0.5, 1.0, "work"),
    ("theta_05", 0.05, -0.5, 1.0, "work"),
    ("theta_617", 0.0, -0.5, 1.0, "work"),
    ("phi_h", 0.05, -0.5, 1.0, "work"),
    ("F", 0.08, 0.0, 2.0, "work"),                   # upper bound 0.6 -> 2.0 (2026-10-24): F sat at 0.6 in every
                                                      # run and F07 (F = 0.7) lowered Q 841 -> 616: the bound bound
    ("kappa_S", 0.05, 0.0, 1.0, "safety_net"),
    ("sigma0_B", 0.0027, 0.0, 0.02, "separation"),
    ("sigma0_W", 0.0013, 0.0, 0.02, "separation"),
    ("sigmaJ_B", 0.008, 0.0, 0.10, "separation"),
    ("sigmaJ_W", 0.0054, 0.0, 0.10, "separation"),
    ("a_bar", 5.0, 0.0, 60.0, "credit"),
    # extensions (2026-10-18, PI-approved Fable decisions; 0 = the model without the extension)
    ("c_mem", 0.0, 0.0, 50.0, "displacement"),     # memory: a spouse's displacement hazard x (1 + c_mem) while the
                                                    # other spouse is non-employed and UI-entitled after a displacement
    ("eta_up", 0.0, 0.0, 3.0, "human_capital"),    # accumulation probability pi_up x (level / 4)^(-eta_up)
]
PARAM_NAMES = [p[0] for p in PARAMS]
N_PARAMS = len(PARAMS)
assert N_PARAMS == 33


# Optional estimated parameters, not in the default free set (estimate.py --free-extra): (name, lower, upper, block). The
# start value is the fixed input of the same name (FIXED_DEFAULTS / inputs/fixed_inputs.json, or --set-fixed).
EXTRA_PARAMS = [
    ("sigma_eps", 0.02, 0.5, "taste_shock"),      # scale of the extreme-value taste shocks (utility units)
    # monthly discount factor, one for all couples (2026-10-21, PI): Bacher et al. (2025) calibrate it to liquid wealth
    # by age (0.9955 a month); bounds 0.90 and 0.995 a year
    ("beta", 0.90 ** (1 / 12), 0.995 ** (1 / 12), "preferences"),
]
EXTRA_NAMES = [p[0] for p in EXTRA_PARAMS]

# Parameters of the extensions pre-built on 2026-10-19 (estimate.py --new-job / --her-sep; README 'Extensions
# 2026-10-19'): (name, default start, lower, upper, block). They are carried AFTER the extras in every theta vector of
# estimate.py (NAMES = PARAM_NAMES + EXTRA_NAMES + LATE_NAMES), so that the indices of every earlier parameter, the
# 33-parameter PARAMS list, N_PARAMS and the default free set are unchanged; each is held at its nested value 0 unless
# its extension is on (estimate.EXT_PARAM), and a vector of an earlier run is padded with the nested values.
LATE_PARAMS = [
    ("xi_nj", 0.02, 0.0, 0.2, "her_exits"),       # extra monthly exit hazard of a wife on a new job (tenure state)
    ("sigmaJw", 0.01, 0.0, 0.10, "separation"),   # separation hazard added while she is UI-entitled after her loss
    # accumulation falling with age (2026-10-22, PI; estimate.py --hc-age on): pi_up x exp(-g_age x 5 x age group), the
    # wife's 5-year age group 0 (25-29) ... 6 (55-59), the same factor for both spouses; g_age per year of age
    ("g_age", 0.03, 0.0, 0.20, "human_capital"),
]
LATE_NAMES = [p[0] for p in LATE_PARAMS]


def default_start() -> dict:
    return {p[0]: p[1] for p in PARAMS}


def bounds() -> tuple[np.ndarray, np.ndarray]:
    return np.array([p[2] for p in PARAMS]), np.array([p[3] for p in PARAMS])


def load_start(path: Path | None = None) -> dict:
    """Start values: inputs/start_analytic.json (analytic_start.py) over the defaults, then inputs/start_overrides.json
    (data-based start values written by IGE/62, e.g. a_bar) when no explicit path is given. Re-read at every call."""
    th = default_start()
    explicit = path is not None
    path = Path(path) if path else INPUTS / "start_analytic.json"
    if path.exists():
        d = json.loads(path.read_text())
        th.update({k: float(v) for k, v in d.get("theta", d).items() if k in th})
    ov = INPUTS / "start_overrides.json"
    if not explicit and ov.exists():
        d = json.loads(ov.read_text())
        th.update({k: float(v) for k, v in d.get("theta", d).items() if k in th})
    return th


def to_vector(theta: dict) -> np.ndarray:
    return np.array([theta[n] for n in PARAM_NAMES], dtype=float)


def from_vector(x) -> dict:
    return {n: float(v) for n, v in zip(PARAM_NAMES, x)}


# ------------------------------------------------------------------------------------------------------------------
# Fixed inputs (plan Section 1). Values in the units stated; converted to model units by fixed_model_units().
# ------------------------------------------------------------------------------------------------------------------
# McClements child shares of a childless adult household, by the youngest child's bucket: mean of the age-band shares
# of model/core.py MCCLEMENTS over ages 0-5 (0.155) and 6-17 (0.265); e(k) = 1 + n(k) x share(k), as in the lifecycle
# model's equivalence_scales (1 + K x share).
MCCLEMENTS_BUCKET = (0.0, (0.09 * 2 + 0.18 * 3 + 0.21) / 6, (0.21 * 2 + 0.23 * 3 + 0.25 * 2 + 0.27 * 3 + 0.38 * 2) / 12)

FIXED_DEFAULTS = {
    "beta": 0.96 ** (1 / 12),
    "gamma": 1.5,
    "r_m": 1.03 ** (1 / 12) - 1,
    "s_M": 1.64,
    "child_share": list(MCCLEMENTS_BUCKET),
    "H_F": 173.0,
    "H_P": 87.0,
    "kappa_up": 0.5,
    "sigma_eps": 0.05,              # taste-shock scale (utility units); set at the solver stage (see README)
    "ret_months": 240,
    "ss_rate": 0.40,
    "sep_asset_share": 0.5,
    "ui_pt_factor": 0.835,          # used only with Config.lost_hours = False: benefit on FT-equivalent earnings x
                                    # this factor (= 1 - 0.337 x (1 - 87/173), the PT share of employed wives)
    # wage levels mu_j(r): PSID mean log hourly wage (2000 $) of employed wives / husbands 25-29 (IGE/60, to come)
    "mu_w": {"B": np.log(11.0), "W": np.log(12.5)},
    "mu_h": {"B": np.log(12.5), "W": np.log(16.0)},
    "psi_w": 0.35,
    "psi_h": 0.35,
    # BPS (2016) Table 3, all ages: permanent variances / covariance, transitory variances, correlation
    "bps_var_perm_w": 0.0382, "bps_var_perm_h": 0.0303, "bps_cov_perm": 0.0027,
    "bps_var_trans_w": 0.0125, "bps_var_trans_h": 0.0275, "bps_rho_trans": 0.31,
    # child process: annual birth probability by wife's 5-year age group (25-29 ... 55-59) and race
    "b0_annual": {"B": [0.15, 0.11, 0.05, 0.01, 0.0, 0.0, 0.0], "W": [0.15, 0.12, 0.05, 0.01, 0.0, 0.0, 0.0]},
    "b2_annual": {"B": [0.08, 0.05, 0.02, 0.005, 0.0, 0.0, 0.0], "W": [0.08, 0.05, 0.02, 0.005, 0.0, 0.0, 0.0]},
    # number of children by bucket k (0, 0-5, 6-17), age group, race (rounded PSID means)
    "n_children": {"B": [[0] * 7, [2] * 7, [2] * 7], "W": [[0] * 7, [2] * 7, [2] * 7]},
    # childcare price per hour of the wife's work by bucket (2000 $)
    "p_cc": [0.0, 2.5, 0.8],
    # workplace-match shares P(s | r), s = 0, 1, 2 (CPS check values; PSID couples' shares from IGE/60 to come)
    "share_s": {"B": [0.823, 0.114, 0.063], "W": [0.823, 0.114, 0.063]},
    # new-job extension (estimate.py --new-job on; unused otherwise): monthly probability that a job held less than
    # ~a year becomes established (geometric, mean 12 months), and whether a new-job exit carries UI like a displacement
    # (1: UI take-up q, displacement loss of human capital, recorded as a displacement) or is treated like a quit (0)
    "nj_grad": 1.0 / 12.0,
    "nj_ui": 0,
}
FIXED_STATUS = {
    "mu_w": "PLACEHOLDER (IGE/60 PSID mean log wage 25-29 by race)",
    "mu_h": "PLACEHOLDER (IGE/60)",
    "psi_w": "PLACEHOLDER (IGE/60 1st-99th percentile rule with shrinkage)",
    "psi_h": "PLACEHOLDER (IGE/60)",
    "b0_annual": "PLACEHOLDER (IGE/60 child process)",
    "b2_annual": "PLACEHOLDER (IGE/60 child process)",
    "n_children": "PLACEHOLDER (IGE/60 PSID means)",
    "p_cc": "PLACEHOLDER (IGE/47 / IGE/60 childcare price)",
    "share_s": "PLACEHOLDER (CPS shares; PSID couples' s from IGE/60)",
    "sigma_eps": "solver-stage choice (README: smoothness profile)",
    "ui_pt_factor": "only for the no-lost-hours fallback",
}


def load_fixed() -> dict:
    """FIXED_DEFAULTS overridden by inputs/fixed_inputs.json and the wage process of inputs/wage_process.json."""
    fx = json.loads(json.dumps(FIXED_DEFAULTS))     # deep copy
    p = INPUTS / "fixed_inputs.json"
    if p.exists():
        fx.update(json.loads(p.read_text()))
    p = INPUTS / "wage_process.json"
    if p.exists():
        wp = json.loads(p.read_text())
        for k in ("p_c", "p_eps_w", "p_eps_h", "sig_nu_w", "sig_nu_h", "rho_nu"):
            if k in wp:
                fx[k] = wp[k]
    # fallback if wage_process.json is absent: closed forms at the default psi and pi_up (plan Section 1.2)
    if "p_c" not in fx:
        fx.update(wage_process_closed_form(fx, default_start()))
    return fx


def wage_process_closed_form(fx: dict, theta: dict, emp_share_w: float = 0.75, emp_share_h: float = 0.95) -> dict:
    """Plan Section 1.2: p_c = Cov / (12 psi_w psi_h); p_eps_j = Var_j / (12 psi_j^2) - p_c - pi_up_j (1 - pi_up_j)
    x employed share; transitory sigma = sqrt(BPS variance) (before the one-time BPS-harness correction)."""
    pw, ph = fx["psi_w"], fx["psi_h"]
    p_c = fx["bps_cov_perm"] / (12 * pw * ph)
    puw, puh = theta["pi_up_w"], theta["pi_up_h"]
    p_eps_w = fx["bps_var_perm_w"] / (12 * pw ** 2) - p_c - puw * (1 - puw) * emp_share_w
    p_eps_h = fx["bps_var_perm_h"] / (12 * ph ** 2) - p_c - puh * (1 - puh) * emp_share_h
    return {"p_c": p_c, "p_eps_w": max(p_eps_w, 0.0), "p_eps_h": max(p_eps_h, 0.0),
            "sig_nu_w": float(np.sqrt(fx["bps_var_trans_w"])), "sig_nu_h": float(np.sqrt(fx["bps_var_trans_h"])),
            "rho_nu": fx["bps_rho_trans"]}


def load_schedule(era: int) -> dict:
    """inputs/schedules_era<e>.json written by IGE/61.PolicySchedules.py."""
    p = INPUTS / f"schedules_era{era}.json"
    if not p.exists():
        raise FileNotFoundError(f"{p} missing: run IGE/61.PolicySchedules.py")
    return json.loads(p.read_text())


ERA_YEARS = {1: (1984, 1996), 2: (1997, 2008), 3: (2009, 2099)}


def era_of_year(y: int) -> int:
    return 1 if y <= 1996 else (2 if y <= 2008 else 3)


# ------------------------------------------------------------------------------------------------------------------
# Solver sizes and fallback switches (plan Section 4.4, items a-e)
# ------------------------------------------------------------------------------------------------------------------
@dataclass
class Config:
    n_hc: int = 7               # (a) human capital levels: 7 (spec) or 5 (fallback; psi rescaled to keep the span)
    merge_s12: bool = False     # (b) merge workplace groups s = 1, 2 (pi_c1 used for both; pi_c2 unused)
    one_era: bool = False       # (c) estimation with the 1997-2008 schedule for every calendar year
    n_assets: int = 30          # (d) asset grid points: 30 (spec) or 20
    lost_hours: bool = True     # (e) wife's UI state records the hours of the lost job (4 wife labor states) or not (3)
    a_max: float = 300.0        # top of the asset grid (thousand 2000 $)
    a_curv: float = 3.0         # grid curvature (dense near the borrowing limit)
    T: int = 420                # months, wife 25-59
    threads: int = 2
    sim_end_year: int = 2023    # simulate calendar months up to December of this year
    ui_accept: bool = True      # Bacher et al. (2025) rule: an entitled wife may decline an offer and keep UI (lead)
    w_interp: str = "hermite"   # continuation value between asset nodes: 'hermite' (node values + node derivatives,
                                # monotone-limited cubic) or 'linear' (chords; the stage-3 code)

    @property
    def n_lw(self) -> int:
        return 4 if self.lost_hours else 3

    def problems(self):
        """(r, s, tau) problems solved one at a time."""
        ss = (0, 1) if self.merge_s12 else (0, 1, 2)
        return [(r, s, tau) for r in (0, 1) for s in ss for tau in (0, 1)]

    def eras(self):
        return (2,) if self.one_era else (1, 2, 3)

    def as_dict(self):
        return asdict(self)


SIZES = {
    # name: Config kwargs. 'full' = model document Table 'State space'; then the plan's fallback sequence in order.
    "full": dict(),
    "a_hc5": dict(n_hc=5),
    "b_hc5_s2": dict(n_hc=5, merge_s12=True),
    "c_hc5_s2_era1": dict(n_hc=5, merge_s12=True, one_era=True),
    "d_hc5_s2_era1_a20": dict(n_hc=5, merge_s12=True, one_era=True, n_assets=20),
    "e_all": dict(n_hc=5, merge_s12=True, one_era=True, n_assets=20, lost_hours=False),
    # economics-preserving default candidate: keeps 3 eras and 3 workplace groups, cuts grids only
    "g_hc5_a20": dict(n_hc=5, n_assets=20),
    "h_hc5_a20_nolh": dict(n_hc=5, n_assets=20, lost_hours=False),
    # keep the three policy eras, cut grids and merge s = 1, 2 (pi_c2 is the first cut-list item anyway)
    "i_hc5_s2_a20_nolh": dict(n_hc=5, merge_s12=True, n_assets=20, lost_hours=False),
    "j_hc5_s2_a20": dict(n_hc=5, merge_s12=True, n_assets=20),
    # keep 7 human capital levels (test 9: 5 levels move mean assets by ~10%, 20 asset points by ~1%)
    "k_s2_era1_a20": dict(merge_s12=True, one_era=True, n_assets=20),
    "l_s2_a20_nolh": dict(merge_s12=True, n_assets=20, lost_hours=False),
}
# Default for estimation runs (<= ~60 s per evaluation on 2 threads; README 'Sizes'): keep the 7 human capital levels
# (5 levels move simulated mean assets by ~10%, 20 asset points by ~1%; tests/test_9), merge s = 1, 2 (pi_c2 is the
# first cut-list item), estimate with the 1997-2008 schedule (plan item c: counterfactuals still re-solve with the
# era schedules), 20 asset points: 33 s. Alternatives: j_hc5_s2_a20 (three eras, 5 levels) 46 s; c_hc5_s2_era1 25 s.
# The lead decides.
DEFAULT_SIZE = "k_s2_era1_a20"
