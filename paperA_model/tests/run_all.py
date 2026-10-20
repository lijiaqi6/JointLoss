"""Run every staged test and print a pass/fail table (writes ../results/tests_<date>.txt).
Run: .venv/Scripts/python.exe paperA_model/tests/run_all.py   (about 10-15 minutes on 2 threads)"""
import datetime
import importlib
import time

import _common

MODULES = ["test_0_egm_bruteforce", "test_1_flat_consumption", "test_2_buffer", "test_3_wife_work",
           "test_4_search_friction", "test_5_ui_lapse", "test_6_independence", "test_7_closed_forms",
           "test_8_sigma_eps", "test_9_grid_accuracy", "test_10_measurement", "test_11_objective_polish",
           "test_12_ext_flags_off", "test_13_block_decorr"]


def main():
    t0 = time.time()
    for mod in MODULES:
        ts = time.time()
        try:
            importlib.import_module(mod).main()
        except Exception as e:                                   # a crash is a failure, not a stop
            _common.report(mod, False, f"ERROR {type(e).__name__}: {e}")
        print(f"    ({time.time() - ts:.0f}s)", flush=True)
    lines = [f"{tag}  {name}: {detail}" for name, tag, detail in _common.RESULTS]
    txt = "\n".join(lines) + f"\n\ntotal {time.time() - t0:.0f}s"
    print("\n" + txt)
    out = _common.HERE.parent / "results" / f"tests_{datetime.date.today():%Y%m%d}.txt"
    out.parent.mkdir(exist_ok=True)
    out.write_text(txt, encoding="utf8")


if __name__ == "__main__":
    main()
