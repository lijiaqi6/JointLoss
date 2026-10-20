"""Paper A model: runtime and memory per solve and per SMM evaluation, by solver size (plan Section 4.4 / 4.6).

For each size (params.SIZES) a fresh subprocess (clean memory) on --threads threads:
  * compiles (numba cache), then solves one problem-era (White, s = 0, low type, era 2) over 420 months, storing the
    simulator arrays: seconds per solve, split into separated-wife / expectation / EGM steps;
  * simulates all entry couples x K copies through that solution over their whole window (an upper bound on the
    evaluation's simulation work, since each couple passes through its own problem's solutions);
  * peak resident memory of the process (psutil, sampled every 50 ms) and the stored solution's size.
Evaluation time = (problems x eras) x seconds per solve + simulation.

Run: .venv/Scripts/python.exe paperA_model/bench.py [--sizes full a_hc5 ...] [--threads 2] [--K 3]
Writes results/bench_<threads>t.json and prints the table.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def one(size: str, threads: int, K: int) -> dict:
    os.environ["NUMBA_NUM_THREADS"] = str(max(threads, 1))
    import numpy as np
    import psutil
    from params import Config, SIZES, load_start
    from model import Model
    from solve import solve
    from simulate import load_entry, sim_kernel, level_to_index, M0

    proc = psutil.Process()
    peak = [proc.memory_info().rss]
    stop = [False]

    def sampler():
        while not stop[0]:
            peak[0] = max(peak[0], proc.memory_info().rss)
            time.sleep(0.05)

    th_ = threading.Thread(target=sampler, daemon=True)
    th_.start()
    cfg = Config(**SIZES[size], threads=threads)
    th = load_start()
    # warm-up compile on a short horizon
    cw = Config(**SIZES[size], threads=threads, T=13)
    solve(Model(th, cw, 2, 1, 0, 0), store=True)
    base_rss = proc.memory_info().rss
    peak[0] = base_rss
    t0 = time.perf_counter()
    m = Model(th, cfg, 2, 1, 0, 0)
    t_build = time.perf_counter() - t0
    t0 = time.perf_counter()
    sol = solve(m, store=True)
    t_solve = time.perf_counter() - t0
    # simulation of all couples through this solution
    ent, src = load_entry()
    n = len(ent) * K
    ent = ent.loc[ent.index.repeat(K)].reset_index(drop=True)
    uid = np.arange(n, dtype=np.int64)
    t0v = 12 * (ent["age0"].to_numpy() - 25)
    m_off = ((ent["year0"].to_numpy() - M0) * 12 - t0v).astype(np.int64)
    nm = (cfg.sim_end_year - M0 + 1) * 12
    t_last = np.minimum(cfg.T - 1, nm - 1 - m_off)
    ok = t_last >= t0v
    uid, t0v, m_off, t_last = uid[ok], t0v[ok], m_off[ok], t_last[ok]
    nn = len(uid)
    F = np.zeros((9, nn, nm), np.float32)
    I = np.full((14, nn, nm), -1, np.int8)
    H = cfg.n_hc
    st = dict(a=np.zeros(nn), lw=np.zeros(nn, np.int64), lh=np.zeros(nn, np.int64),
              hw=np.full(nn, (H - 1) // 2, np.int64), hh=np.full(nn, (H - 1) // 2, np.int64),
              k=np.zeros(nn, np.int64), nu=np.zeros(nn, np.int64), mar=np.ones(nn, np.int64), t=t0v.copy())
    rows = np.arange(nn, dtype=np.int64)
    args = lambda: (20261018, uid, rows, t0v.astype(np.int64), t_last.astype(np.int64), m_off, st["a"], st["lw"], st["lh"],
                    st["hw"], st["hh"], st["k"], st["nu"], st["mar"], st["t"], sol.C, sol.W, sol.CS, sol.WS, m.agrid,
                    m.state_cfg, m.state_n, m.cfg_hw, m.cfg_hh, m.inc0, m.snapB, m.disu, m.sc, m.xfloor,
                    m.stateS_cfg, m.stateS_n, m.cfgS_hw, m.incS0, m.snapBS, m.disuS, m.scS, m.xfloorS, m.earn, m.ui,
                    m.eitc_tab, m.eitcS_tab, m.uiS, m.asset_limit, m.beta, m.gamma, m.rm, m.sigma_eps, m.kappa_S,
                    m.pnu, m.pic, m.dw, m.dh, m.lw_, m.lh_, m.qui, m.ui_exp, m.sig_E, m.sig_N, 0.5, m.Aw_idx, m.Aw_p,
                    m.Aw_n, m.Ah_idx, m.Ah_p, m.Ah_n, m.Iw, m.Ih, m.Is, m.p_c, m.Pk, m.E_, m.UP_, m.UF_, m.N_, 0.0,
                    F, I)
    # compile the simulator on a tiny subset first
    extra = (sol.Dlt, sol.DltS, bool(m.ui_accept), getattr(cfg, "w_interp", "hermite") == "hermite", m.r_wedge, m.c_mem, m.jL)
    sim_kernel(*[(x[:5] if (isinstance(x, np.ndarray) and x.shape[:1] == (nn,)) else x) for x in args()[:-2]],
               F[:, :5], I[:, :5], *extra)
    for key in ("a", "lw", "lh", "hw", "hh", "k", "nu", "mar"):
        st[key][:] = 0 if key not in ("hw", "hh", "mar") else ((H - 1) // 2 if key != "mar" else 1)
    t0 = time.perf_counter()
    sim_kernel(*args(), *extra)
    t_sim = time.perf_counter() - t0
    cm = int((I[0] >= 0).sum())
    stop[0] = True
    th_.join()
    nsolve = len(cfg.problems()) * len(cfg.eras())
    return dict(size=size, config=cfg.as_dict(), threads=threads, K=K, entry_source=src, n_copies=nn,
                couple_months=cm, states_per_month=int(m.NLW * 3 * m.H ** 2 * 12 * m.NA), ncfg=int(m.ncfg),
                t_build=t_build, t_solve=t_solve, solve_split=sol.timing, t_sim=t_sim, n_solves=nsolve,
                t_eval=nsolve * (t_solve + t_build) + t_sim, stored_gb=sol.nbytes() / 1e9,
                peak_rss_gb=peak[0] / 1e9, base_rss_gb=base_rss / 1e9)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sizes", nargs="*", default=None)
    ap.add_argument("--threads", type=int, default=2)
    ap.add_argument("--K", type=int, default=3)
    ap.add_argument("--one", default=None)
    a = ap.parse_args()
    if a.one:
        print("RESULT " + json.dumps(one(a.one, a.threads, a.K)))
        return
    from params import SIZES
    sizes = a.sizes or list(SIZES)
    out = []
    for s in sizes:
        env = dict(os.environ, NUMBA_NUM_THREADS=str(a.threads))
        p = subprocess.run([sys.executable, __file__, "--one", s, "--threads", str(a.threads), "--K", str(a.K)],
                           capture_output=True, text=True, env=env)
        line = [l for l in p.stdout.splitlines() if l.startswith("RESULT ")]
        if not line:
            print(s, "FAILED\n", p.stdout[-2000:], p.stderr[-4000:])
            continue
        r = json.loads(line[0][7:])
        out.append(r)
        print(f"{s:20s} states/month {r['states_per_month']:>8,d}  solve {r['t_solve']:6.2f}s "
              f"(sep {r['solve_split']['sep']:.2f} exp {r['solve_split']['expect']:.2f} egm {r['solve_split']['egm']:.2f})"
              f"  x{r['n_solves']:2d} solves + sim {r['t_sim']:5.2f}s ({r['couple_months']:,} couple-months) "
              f"= eval {r['t_eval']:7.1f}s   stored {r['stored_gb']:.2f} GB  peak RSS {r['peak_rss_gb']:.2f} GB",
              flush=True)
    res = HERE / "results"
    res.mkdir(exist_ok=True)
    (res / f"bench_{a.threads}t.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
