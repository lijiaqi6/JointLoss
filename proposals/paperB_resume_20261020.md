# Paper B: where to resume after the move (2026-10-20)

For the next Claude session on Paper B. Written by the Paper A session at the PI's request.

**Paper B moved out of Selection-vs-risk.** Since 2026-10-20 it lives in this repository (github.com/lijiaqi6/JointLoss)
with Paper A, at the repository root: `model/`, `paperB_age_profile/`, the numbered scripts, `output/`, `proposals/`,
`EVIDENCE.md`. The copy is Selection-vs-risk commit `c288c72`, which holds all Paper B work up to the 10:52 commit
"Paper B race-neutral rewrite, in progress". Do not edit `IGE/` in Selection-vs-risk any more; it is being removed
there (pointer note left, history kept).

**Your working copy: `G:\My Drive\IGE-B`** (a clone of JointLoss). Paper A works in `G:\My Drive\JointLoss`; the two
sessions never share a working folder. Exchange through GitHub only: commit on main, push after each commit,
`git fetch` + `git merge origin/main` when a push is rejected, never rebase.

## State carried over (from the Paper B session's own hand-off, 2026-10-20)

- The race-neutral rewrite is in progress: `paperB_age_profile/sec4_passedon.tex` and `sec5_skill.tex` are drafted
  but not yet wired into `main.tex`; `90.PaperBRaceNeutralTables.py` writes ten new `tab_*.tex`; 16 new entries in
  `references.bib`. Outline: `proposals/paperB_outline_race_neutral_20261020.md`.
- PI decision: the structural model is dropped from Paper B. `model/` stays as code, but Section 8 and appendices C/D
  leave `main.tex` in the rewrite.
- Nothing was running locally or on the HPC at the move.

## What changed in the move

- Repo-relative `IGE/<folder>` prefixes are gone (`IGE/model` -> `model`, etc.), in code, shell scripts, table notes
  (`model/tables.py`) and the matching `.tex`; HPC run records untouched.
- Environment variables (defaults suit this PC): `DROPBOX` (raw data, `~/Dropbox`); `IGE_DATA` (person-level caches;
  set as a Windows user variable to `G:\My Drive\Selection vs risk\IGE\data`); `NLSY79_DIR` (scripts 10, 12, 18, 21
  read Selection-vs-risk's `NLSY79/`; default `G:\My Drive\Selection vs risk\NLSY79`).
- `model/steps_summary.py`: ROOT is the repository root.
- `model/hpc_ige.sh`: paths without `IGE/`. Before the next IGE- job the PI must move the old Stanage `~/ige` aside
  and re-clone it from JointLoss (sparse checkout `model`), using a JointLoss deploy key (header of the script).
- Git-ignored person-level inputs already copied into IGE-B: `model/output/sons_types.csv`, `data_panel.pkl`,
  `ipw_sons.pkl`.
- Python: `G:\My Drive\Selection vs risk\.venv\Scripts\python.exe` still works.
- Claude memory: a session opened in `G:\My Drive\IGE-B` starts with an empty project memory; the PC's memory files
  are copied in `G:\My Drive\claude_memory_export` (Paper B entries: paperB-*, ige-*, papers-as-journey, etc.).

## Checks run from the merged repository

- Paper B: Q at the starting values (R = 5, steps off) 22,856.15, PASS.
- Paper A: Q at the analytic start 11,733.7, PASS; tests 13/13.
- `model/regen.py --check`: result in the commit that follows this note (Section 8 is leaving the paper anyway).
