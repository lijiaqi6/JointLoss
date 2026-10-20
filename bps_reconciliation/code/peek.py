"""Quick look at point estimates of finished specs (development helper): python peek.py spec1 spec2 ..."""
import sys
from pathlib import Path

import pandas as pd

W = Path(r"C:\Users\cm1jil\AppData\Local\Temp\claude\g--My-Drive-Selection-vs-risk\c16f819d-4913-4b50-9f11-a4daf3178246"
         r"\scratchpad\bps_work")
keys = ['eta_c_p', 'pi', 's_report', 'eta_h1_w1', 'eta_h2_w2', 'eta_c_w1', 'eta_h1_w2', 'observations', 'ch_c0',
        'ch_c1', 'ch_c3', 'ch_c4', 'ch_gov', 'ch_fam', 'ch_sav', 'ch_m_h2v1']
for sp in sys.argv[1:]:
    for run in ('gmm10', 'gmm9', 'beta'):
        f = W / sp / f"est_{run}.csv"
        if not f.exists():
            print(sp, run, "missing")
            continue
        e = pd.read_csv(f).set_index('_varname')
        if run == 'gmm10':
            print(sp, run, {k: round(float(e.loc[k, 'value']), 4) for k in keys if k in e.index})
        elif run == 'gmm9':
            print(sp, run, [(k, round(float(e.loc[k, 'value']), 4), round(float(e.loc[k, 'se']), 4)) for k in
                            ['s_u1_1', 's_v1_1', 's_u2_1', 's_v2_1', 'r_u1u2_1', 'r_v1v2_1']])
        else:
            print(sp, run, 'beta', round(float(e.loc['beta', 'value']), 4), round(float(e.loc['beta', 'se']), 4))
