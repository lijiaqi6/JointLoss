"""Shared set-up for the staged tests (plan Section 4.2, stage 1 checks (1)-(7) and the simulator checks)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from params import Config, load_start  # noqa: E402

# test size: 5 human capital levels, 30 asset points, one era (2), full horizon
def test_config(**kw):
    base = dict(n_hc=5, n_assets=30, one_era=True, threads=2)
    base.update(kw)
    return Config(**base)


def theta(**kw):
    th = load_start()
    th.update(kw)
    return th


def entry(n, seed=11, **fix):
    """Synthetic entry couples; keyword arguments fix columns (e.g. race=1, s=0, age0=25, year0=1984)."""
    from simulate import synthetic_entry
    e = synthetic_entry(n, seed)
    for k, v in fix.items():
        e[k] = v
    return e


RESULTS = []


def report(name, ok, detail):
    tag = "PASS" if ok else "FAIL"
    RESULTS.append((name, tag, detail))
    print(f"[{tag}] {name}: {detail}", flush=True)
    return ok
