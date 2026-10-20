# Paper B status, 2026-10-19 15:35 (Fable's second ten-hour plan; local blocks done by 15:31)

## Decided by the PI (16:00)

- Both wording changes below applied to the abstract and introduction (Option A; level and opening shares), commit
  6dbad28. The conclusion carries no share and is unchanged.
- `sons_types.csv` stays in git history (e0c3c4d-df588c8): 138 KB in a 1.1 GB, private repository. No purge.

## For the PI: two sentences to decide (as written at 15:35)

**1. The H4 headline and the measurement of parental income.** Tonight's result (Table `tab:h4measure`, Section 8
"H4 in long differences"): the PSID / NLSY79 disagreement is the parental-income measure, not the data set. White sons'
ten-year wage growth on parental income at equal schooling: PSID 13-19 mean 0.073\*\*\*, 12-17 mean 0.055\*\*, one year
at 16 0.005 (0.019); NLSY79 (three years at most, ages 14-22) -0.001; NLSY97 (one parent report) 0.000; model E 0.074
with the 13-19 mean and 0.030 with the same sons' one-year measure. A classical errors-in-variables correction does
not restore the multi-year value (0.009), so the paper says a single year loses more than classical noise once
schooling is held fixed.

Current abstract (main.tex, lines 43-47): "A life-cycle model that nests four explanations selects one: parental income
raises the growth of human capital for White sons and not for Black sons, and schooling buys Black sons a higher wage
at entry and slower growth; a racial difference in access to good jobs is rejected."

- Option A (recommended): add after "not for Black sons": ", a channel seen with a multi-year measure of parental income
  and absorbed by schooling with a one-year measure, in the PSID as in the NLSY79 and NLSY97,"
- Option B: keep the abstract; the measurement result stays in Section 8 and Section 6's footnote.

The introduction (sec1_introduction.tex, "The data select one model ...") takes the same clause under Option A.

**2. "Three fifths of the gap at 45-49"** (abstract, introduction, conclusion) is a level share; of the opening between
25-29 and 45-49 the same channel carries two fifths (0.081 of 0.199). Option: "three fifths of the gap at 45-49 and two
fifths of its opening since 25-29".

## Done tonight (all pushed, origin/main 0a31640)

| Block | Result | Paper | EVIDENCE |
|---|---|---|---|
| 1 measurement | one-year measures give ~0 net of schooling in all three data sets; model predicts the fall (0.074 -> 0.030) | Table h4measure, paragraph rewritten | 11.17 |
| 2 NLSY97 | raw 0.053\*\*, net of degree 0.000 (its "multi-year mean" is later youth reports, not usable) | row in Table h4measure, sentence | 11.18 |
| 3 Section 8 | 11 -> 6 tables + Figure modelfit; ~5,570 words; lattice, estimates, fit, H4 by tercile, sensitivity and two diagnostics in new Appendix D | sec7, appD_model.tex | |
| 4 tools | judge_step.py (reproduces the H4 test exactly), regen.py (--check: all tables byte-identical) | | |
| 6 model document | IPW and g35 sets, step 6 as D13, new validation statistics | model_document.tex | |
| 7 consistency | Section 6 footnote to the long differences; terminology sweep clean | sec6 | |

Skipped: Block 6's robustness of the long differences (horizons, SRC, weights): low value next to the measurement
result, and the PSID panel of the model has wages only.

## HPC: what is out and how to read it

**Update 2026-10-20 00:45: everything has landed and is integrated; nothing pending.**
- Polish round, all ten runs: max |dQ| 0.12 (D 127.15 -> 127.03; C 0.06; all others 0.00). Hypothesis-table note,
  Appendix C and Section 8 updated: the G and H rows are minima, not bounds.
- Step 5 (ufric), kept at both ends of the lattice: E5 drop 30.2 (s.d. 1.6, min 26.9), dlu -0.539*** (0.095); A5 drop
  30.6 (s.d. 1.9, min 26.7), dlu -0.536*** (0.094). E5 is the selected model (regen.py --run E5; Section 8, Appendix D
  and introduction numbers updated; lattice tables kept at step 4 via estimates_E_lattice.json). Counterfactual
  dlu = 0 added (Black wage +0.015***, IGE gap +0.004**).
- Next submissions unchanged (IPW pair; g35 then step 6 gloss). The start-up check in hpc_ige.sh now runs on the
  target moments (IGE_MOMENTS= ), which these runs need. scp the sons file first (it now also carries x_clean).
- The clean-parental-income re-estimation is coded (IGE_MOMENTS=clean) but not recommended: corr(x, x_clean) 0.997,
  reduced form unchanged.

Earlier (15:35): back and unchanged P_A 138.35, P_B 134.98, P_F 136.40, P_G 138.22, P_C 133.72.

- Polish round: if every |dQ| < 0.5, the hypothesis-table note's "pending ... bounds" becomes "a polish re-estimation of
  every model moved no Q by more than [max]"; nothing else changes.
- Step 5 (ufric), from the IGE folder:
  `python model/judge_step.py --with model/hpc_runs/E5_j11866020:E --without model/hpc_runs/Lx4_E_j11861512:E --label ufric_E`
  (after a pull; same for A5 against P_A). Kept (drop > 3.84 at every seed and p < 0.05): `python model/regen.py --run
  model/hpc_runs/E5_j11866020 --model E` regenerates Section 8's selected-model outputs, and the text needs a paragraph
  after H1; the lattice stays at the step-4 baseline with a note. Rejected: one sentence in "What the model leaves open".

Next submissions (unchanged from status_20261019_afternoon.md): copy the types file with `ipw_base` to Stanage, then
the IPW pair (E_ipw, A_ipw) and the g35 pair (E_g35, then E6 with `gloss`).
