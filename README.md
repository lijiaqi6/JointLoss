# JointLoss: the IGE project, Papers A and B

Private repository of two papers that share data scripts, an evidence ledger and person-level data caches:

- **Paper A**: "The Insurer Is Hit Too: Joint Job Loss of Spouses and the Limits of Family Insurance".
- **Paper B**: the age profile of intergenerational persistence and what is passed on from parents to sons.

Both moved here on 2026-10-20 from `IGE/` in github.com/lijiaqi6/Selection-vs-risk: Paper A from commit `791bcee`,
everything else from `c288c72`. The history before that date stays readable there. Selection-vs-risk keeps Paper 1
(the racial gap in the child penalty) and its `NLSY79/` folder, which some scripts here read (see `NLSY79_DIR`).

## Layout

| Path | What |
|---|---|
| `paperA_joint_loss/`, `paperA_model/` | Paper A: the paper and model document; the structural model (monthly two-earner DC-EGM, SMM, HPC job `hpc_job_a.py`, run notes and HPC results in `results/`) |
| `paperB_age_profile/`, `model/` | Paper B: the paper and model document; the structural model (SMM, HPC job `hpc_ige.sh`, results in `hpc_runs/`, `regen.py` regenerates Section 8) |
| `1.PSID.py` ... `90.*.py`, `common.py` | data scripts, numbered as in Selection-vs-risk so notes and footnotes citing "IGE/60" etc. still point at the right script |
| `output/` | aggregate outputs of the data scripts |
| `bps_reconciliation/` | Blundell, Pistaferri and Saporta-Eksten (2016) replication and the BPS-on-simulated-data harness (Paper A) |
| `proposals/` | Fable memos, plans and evidence notes (file names say which paper) |
| `EVIDENCE.md` | evidence ledger for both papers (sections tagged [Paper A] / [Paper B]) |
| `HANDOVER_MAC.md` | Paper A state and next tasks (the move to a Mac was called off; the file name is historical) |

## One working copy per paper session

Sessions working on different papers at the same time must not share a working folder (they collided in
Selection-vs-risk). Each has its own clone of this repository and exchanges work only through GitHub: commit on
`main`, push after every commit, `git fetch` + `git merge origin/main` when a push is rejected, never rebase.

- Paper A: `G:\My Drive\JointLoss`
- Paper B: its own clone (e.g. `G:\My Drive\IGE-B`)
- Stanage: `~/jointloss` (Paper A jobs, `Joint-` names) and `~/ige` (Paper B jobs, `IGE-` names), both clones of this repository

## Paths outside git (environment variables; defaults suit the PC)

- `IGE_DATA`: person-level caches the data scripts read and write (default `./data`, git-ignored). Shared by both
  papers; on the PC currently `G:\My Drive\Selection vs risk\IGE\data` (6.7 GB).
- `DROPBOX`: raw data and replication packages, read only (default `~/Dropbox`).
- `NLSY79_DIR`: Selection-vs-risk's `NLSY79/` folder (helpers and NLSY79 extracts), read only.
- `STATA_EXE`: Stata for the BPS harness (default the PC's StataNow19).

Person-level inputs are git-ignored and copied by hand (scp to Stanage): `paperA_model/inputs/psid_entry_couples*.csv`;
`model/output/sons_types.csv`, `data_panel.pkl`, `ipw_sons.pkl`.

## Checks after a fresh clone

```sh
python paperA_model/tests/run_all.py          # Paper A: all tests pass
python paperA_model/estimate.py evaluate      # Paper A: Q at the analytic start 11,733.7
cd model && python regen.py --check           # Paper B: Section 8 tables unchanged
```

## Rules

Never commit person-level microdata; aggregates only. No branches. Commit messages end with
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. Full list in `HANDOVER_MAC.md`, section 5.
