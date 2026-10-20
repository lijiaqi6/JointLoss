# JointLoss

Paper A: **"The Insurer Is Hit Too: Joint Job Loss of Spouses and the Limits of Family Insurance"** (Jiaqi Li,
University of Sheffield). Private.

This repository starts on 2026-10-20 from a snapshot of `IGE/` in github.com/lijiaqi6/Selection-vs-risk at commit
`791bcee` (plus the hand-over commit after it). The history before that date (every commit, HPC run and paper
revision) stays readable there; that repository also holds Paper 1 (child penalty) and Paper B (IGE), which are not
copied here.

## Layout

| Path | What |
|---|---|
| `paperA_joint_loss/` | the paper (`main.tex`, `sec1`-`sec8`, appendices) and the model document (`model_document.tex`) |
| `paperA_model/` | the structural model: monthly two-earner DC-EGM solver (`model.py`, `solve.py`), simulator, moments, SMM (`estimate.py`), HPC job (`hpc_job_a.py`), post-estimation, tests; `results/` holds every run note and HPC result |
| `1.PSID.py` ... `79.ParentsPresentOutcomes.py` | data scripts (numbers keep their Selection-vs-risk names so every note and footnote that cites "IGE/60" etc. still points at the right script); `common.py` shared helpers |
| `output/` | aggregate outputs of the data scripts used by the paper and the model (targets `paperA_targets.csv`, figures, tables) |
| `bps_reconciliation/` | Blundell, Pistaferri and Saporta-Eksten (2016) replication and reconciliation, and the BPS-on-simulated-data harness |
| `proposals/` | Fable memos and evidence notes for Paper A |
| `EVIDENCE.md` | evidence ledger (Paper A sections of the Selection-vs-risk ledger, row numbers kept) |
| `HANDOVER_MAC.md` | current state and next tasks |

## Machines and paths

Nothing machine-specific is hard-coded in the model. Two environment variables point at what is not in git:

- `IGE_DATA`: the person-level caches the data scripts read and write (default `./data`, git-ignored). On the
  PC they are in `G:/My Drive/JointLoss/data`; on the Mac the same folder through Google Drive.
- `DROPBOX`: raw data and replication packages, read only (default `~/Dropbox`).
- `STATA_EXE`: only for the Stata-based BPS harness (being ported to Python).

The model's PSID entry couples (`paperA_model/inputs/psid_entry_couples*.csv`) are person-level and git-ignored:
copy them by hand (they are in the Google Drive folders), and to Stanage with scp (`hpc_job_a.py` docstring).

## Check after a fresh clone

```sh
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python paperA_model/tests/run_all.py        # all tests pass
.venv/bin/python paperA_model/estimate.py evaluate     # Q at the analytic start 11,733.7 (compile variation ~0.1)
```

## Rules

Never commit person-level microdata; aggregates only. Commit on `main`, push after each commit, fetch + merge
(never rebase). Commit messages end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. The full list is
in `HANDOVER_MAC.md`.
