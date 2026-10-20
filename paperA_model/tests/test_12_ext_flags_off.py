"""Check (12), extensions of 2026-10-19 (new_job, her_sep; README 'Extensions 2026-10-19'): with the flags off the
default path is unchanged.
 (a) Model arrays: a Model built with the flags off (keys absent, or new_job / her_sep False with xi_nj and sigmaJw
     non-zero in theta) has exactly the arrays of the base model (state space, configurations, outcome tables, budget,
     transitions); the solver uses the base separation kernel (sep_table None);
 (b) start moments: estimate.py's moments at the analytic start with --new-job off --her-sep off and xi_nj = 0.05,
     sigmaJw = 0.03 in the theta vector equal, bit for bit, those of a 34-entry theta vector of a run before the
     extensions (padded, no extension keys); same process, so the same numba compilation;
 (c) information and the HPC rule: Q against hpc_job_a.EXPECTED_Q (relative 1e-3) and the largest moment difference
     against inputs/expected_start_moments.csv. These are not bit-comparable: the numba binaries differ between a
     fresh compilation and a cache-loaded one (and the PC's EXPECTED_Q 11,726.0 came from an older cache state;
     Stanage gave 11,733.6, a clean PC build 11,733.7: results/extensions_20261019.md).
Default size (k_s2_era1_a20), 2 threads: two full evaluations (~3-6 minutes)."""
import json
import re
from pathlib import Path

from _common import report
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
MODEL = HERE.parent


def part_a():
    from params import Config, SIZES, DEFAULT_SIZE, load_fixed, load_start
    from model import Model
    from solve import sep_table
    cfg = Config(**SIZES[DEFAULT_SIZE], threads=2)
    th = load_start()
    fx = load_fixed()
    m0 = Model(th, cfg, 2, 1, 1, 0, fixed=fx)
    th1 = dict(th, xi_nj=0.05, sigmaJw=0.03)
    fx1 = dict(fx, new_job=False, her_sep=False, her_sep_tie=False)
    m1 = Model(th1, cfg, 2, 1, 1, 0, fixed=fx1)
    diff = []
    for k, v in vars(m0).items():
        w = getattr(m1, k)
        if isinstance(v, np.ndarray):
            if v.shape != w.shape or not np.array_equal(v, w):
                diff.append(k)
        elif isinstance(v, (int, float, bool, np.integer, np.floating)) and v != w:
            diff.append(k)
    ok = not diff and m1.NLW == cfg.n_lw and m1.EN_ == -1 and sep_table(m1) is None and m1.sig_Jw == 0.0 and \
        m1.xi_nj == 0.0
    return ok, f"(a) arrays differing with the flags off: {diff or 'none'}; NLW {m1.NLW}, EN_ {m1.EN_}"


def part_bc():
    import estimate as E
    import moments as M
    expected_q = float(re.search(r"^EXPECTED_Q = ([0-9.]+)", (MODEL / "hpc_job_a.py").read_text(encoding="utf-8"),
                                 re.M).group(1))                 # read, not imported (hpc_job_a is a job script)
    args = E.build_parser().parse_args(["evaluate", "--threads", "2", "--new-job", "off", "--her-sep", "off",
                                        "--her-sep-tie", "off"])
    E.resolve(args)
    E._init_worker(E.spec_of(args))
    th = E.start_theta(args)
    tv = E.vec_dict(th)
    old = th[:len(E.PARAM_NAMES) + len(E.EXTRA_NAMES)]             # a vector of a run before the extensions
    m_old, _ = E.model_moments(old)
    th_x = E.dict_vec(dict(tv, xi_nj=0.05, sigmaJw=0.03))          # extension parameters set, flags off
    m_x, _ = E.model_moments(th_x)
    T = E._W["targets"]
    q, miss = M.objective(m_x, T, E._W["W"])
    same = np.array_equal(np.nan_to_num(m_old, nan=-9e9), np.nan_to_num(m_x, nan=-9e9))
    ok_b = same and tv["xi_nj"] == 0.0 and tv["sigmaJw"] == 0.0 and not args.ext_targets and miss == 0
    exp = pd.read_csv(MODEL / "inputs" / "expected_start_moments.csv")
    sim = dict(zip(T["id"], m_x))
    dmax = max(abs(sim[k] - v) for k, v in zip(exp["id"], exp["sim"]) if np.isfinite(v))
    ok_c = abs(q - expected_q) <= 1e-3 * expected_q and list(T["id"]) == list(exp["id"])
    return ok_b, ok_c, (f"(b) flags off with xi_nj, sigmaJw set vs a pre-extension vector: identical {same} "
                        f"({len(m_x)} moments); start xi_nj {tv['xi_nj']}, sigmaJw {tv['sigmaJw']}; (c) Q {q:,.2f} vs "
                        f"EXPECTED_Q {expected_q:,.1f} (relative {(q - expected_q) / expected_q:+.1e}, HPC rule 1e-3), "
                        f"max |moment - expected file| {dmax:.2e}")


def main():
    ok_a, msg_a = part_a()
    ok_b, ok_c, msg_bc = part_bc()
    report("12 extensions off = base model", ok_a and ok_b and ok_c, f"{msg_a}; {msg_bc}")
    print(json.dumps({"a": [ok_a, msg_a], "bc": [ok_b, ok_c, msg_bc]}, indent=1), flush=True)


if __name__ == "__main__":
    main()
