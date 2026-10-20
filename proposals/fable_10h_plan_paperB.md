# Paper B: ten unattended hours without the HPC, 13:50-23:50 (Fable, 2026-10-19)

Read at 8e49c77: `sec7_model.tex` and its eight tables, `sec1`, `sec6`, `sec6c`, `sec8`, the abstract, `model_document.tex`
(targets, lattice, validation, counterfactuals, decisions), EVIDENCE 9-11, `core.py`, `estimate.py`, `build_data.py`,
`postestimation.py`, `lattice_q.py`, `fix_seeds.py`, `validation_run.py`, `tables.py`, `hpc_ige.sh`, the three
polished runs that are back (`P_A`, `P_B`, `P_F`), `final_x4/lattice.md`, `validation_psid.json`, `validation_E.json`,
`output/same_employer_growth_checks.md` (Section C), `41.AgeProfileMeasurement.py` (the attrition weights),
`36.SameEmployerGrowthChecks.py` (the NLSY79 cache), `tab_attrition.tex`, and my three earlier memos. Nothing was run;
nothing but this file was edited.

**Short answer.** Nine blocks, about 45 minutes of 6-core compute in all (the budget allows four hours; none of it is
needed for re-estimation). In order of value: (1) a diagnosis of the two untargeted failures that decide the next
model step, computed with one script on the PSID panel and on the simulated panel: the routes by which sons enter and
leave $G$ jobs after 35 (within-employer reclassification, moves, displacement), and a decomposition of the wage-level
misfit into within-son growth and the composition of who has a wage; (2) the IPW moment set as tested code with the
data moments built, the decisive robustness for H4; (3) the step the $G$-share diagnosis points to, coded, tested and
ready to submit with its new moments; (4) the H4 statistic a referee will ask for: within-son wage growth over ten and
twenty years on parental income, net of schooling in the PSID and net of schooling and the AFQT in the NLSY79, next to
the model's value; (5) the reading of the HPC results when they land (polish round, `ufric`), with the paper changes
that follow from each outcome; (6) the appendix that tells the model's development as a journey; (7) the policy
paragraph on H4. Skipped, with reasons: NLSY cohort simulation, earnings IGE, block weights, any local re-estimation at
R = 20, rewriting the introduction and conclusion.

Rules that bind every block: numbers in the paper come from json through `tables.py` or the script's own writer,
never typed; stars and p-values on every estimate; "human capital accumulation", "search friction"; aggregates only in
git (person-level files, weights and panels stay git-ignored); commit at the end of every block by file name (other
sessions have uncommitted Paper A edits in `paperA_model/`; never `git add -A`, never touch their files), push via
`git fetch` + `git merge origin/main` (never rebase); compile `main.tex` before every paper commit; nulls in the text.

## 0. Timetable

| Time | Block | Local compute | Deliverable |
|---|---|---|---|
| 13:50-14:05 | 0. Setup | none | clean start; HPC check 1 |
| 14:05-15:20 | 1. Routes into and out of $G$ jobs, data vs model | 10 simulations at R = 20 (2 min) + 100 bootstrap draws of a cheap statistic (1 min) | `model/panel_diag.py` (part 1), `output/panel_diag_psid.json`, `final_x4/panel_diag_E.json`, validation item 5 rewritten, EVIDENCE 11.12, the step-6 decision |
| 15:20-16:35 | 2. The wage-level misfit decomposed | same simulations (reuse) | `panel_diag.py` (part 2), validation item 1 rewritten, EVIDENCE 11.13 |
| 16:35-17:35 | 3. IPW moment set as tested code | 500 bootstrap draws (3 min) + 1 evaluation | weighted `core.moments`, `output/data_moments_ipw.json`, `sons_types.csv` gains `ipw_base`, EVIDENCE 11.14 (data side), sbatch lines |
| 17:35-18:50 | 4. Step 6 coded and tested; the `g35` moment set | invariance evaluation, 12-point profile (1 min), SMM_TEST (3 min), 500 bootstrap draws (3 min) | `core.py`, `estimate.py`, `build_data.py` switches; `output/data_moments_g35.json`; commands for Monday |
| 18:50-20:05 | 5. H4 in long differences (PSID, NLSY79 with AFQT, model) | 10 simulations (2 min) | `IGE/67.LongDifferenceH4.py`, `tab_h4_longdiff.tex`, `core.longdiff`, two sentences in Section 8 and a footnote in Section 6, EVIDENCE 11.15 |
| 20:05-21:05 | 6. HPC results integration (or whenever all ten `P_*` and E5/A5 are in; at 22:50 at the latest with what is there) | `fix_seeds` 2 x 2 min; `lattice_q` locally if any model moved (15 min); `postestimation` h4 version if `dlu` passes (7 min) | `final_x4/` updated, `tables.py` rerun, table notes, Section 8 verdict numbers, EVIDENCE 11.2/11.3/11.8 |
| 21:05-22:05 | 7. Appendix "How the model was built" | none | `tables.py: tab_steps()`, `tab_model_steps.tex`, `appC_model.tex`, `main.tex` input, model document decision D13 |
| 22:05-22:50 | 8. Policy paragraph on H4; abstract flag for the PI | none | Section 8 counterfactual closing paragraph, EVIDENCE 11.1 policy column |
| 22:50-23:50 | 9. HPC check, compile, commit, push, status note | none | `proposals/status_20261019_night.md` |

Drop order if a block overruns: 8 first; then 7 is cut to the table only; then 5 is cut to the PSID and the model
(the NLSY79 part only if `data/same_employer_checks_nlsy79.pkl` and `data/career_wage_growth_nlsy79.pkl` load; never a
fresh read of the 35 GB release). Never cut 1, 3, 4 or 6: they decide Monday's submission.

HPC checks (the one cheap completion signal, no polling): at every block boundary,
`git fetch origin; git log --oneline HEAD..origin/main | Select-String "IGE HPC results"`. Merge when something is
there. The job commits are named `IGE HPC results: P_<model>_j<job>` and `E5_j<job>` / `A5_j<job>`.

## 1. Block 0: setup (13:50-14:05)

`git fetch origin; git merge origin/main`; `pdflatex main.tex` compiles as is; `python tables.py` reproduces the eight
tables byte for byte (it reads only json); confirm the three polished runs that are back changed nothing: `P_A` 138.4,
`P_B` 135.0, `P_F` 136.4 against Lx4's 138.4, 135.0, 136.4, and their race parameters (`a3` in B $-0.274$ (0.153),
`dg1` in F $-0.0020$ (0.0019)) equal Lx4's to three decimals. Note it in the status file; the hypothesis-table note
("a polish re-estimation of every model (pending)") is rewritten in Block 6 when the other seven are in.

PowerShell form of every model command below: `$env:IGE_STEPS="age,rehire,xacc"; $env:IGE_FIX="muG,du";
$env:IGE_R="20"; python <script>` from `IGE\model`. `IGE_WORKERS` is 6 by default; leave it.

## 2. Block 1: routes into and out of $G$ jobs (14:05-15:20)

**Why.** The one validation failure that asks for a model step is the share whose modal job at 35-55 is $G$: it rises
in the PSID between 25-34 and 35-55 (White top tercile 0.180 to 0.227, bottom 0.066 to 0.088; Black 0.117 to 0.122,
0.031 to 0.044) and falls in the model (0.181 to 0.134, 0.047 to 0.031; 0.099 to 0.073, 0.032 to 0.021). Section 8
names two candidate steps (access that rises with age; a lower job-loss rate in $G$ jobs) and the one-step rule says
code one. There is a third the model cannot produce at all: in the model a son's job type is fixed for the life of the
employer spell, while in the PSID the type is the occupation $\times$ industry cell of the current job, which changes
within employers (position changes with the same employer are 0.04-0.06 a year at 35-55, EVIDENCE 9.8; coded occupation
changes are noisy, 9.9). Which route carries the data's rise decides the step; a referee who sees "access by age" when
the data say "within-employer upgrading" will say the model is being patched in the wrong place.

**Do.** `model/panel_diag.py`, built like `validation_run.py` (PSID panel `output/data_panel.pkl`; model E at seeds
7-16, R = 20, `IGE_STEPS=age,rehire,xacc IGE_FIX=muG,du`), with one function `core.routes(P)` applied to both panels.
On consecutive interview pairs one to two years apart with a job type at both (the same pair definition as the
targets, `wave >= 1985`), by race and by the band of the later interview (25-34, 35-55):
- $G$ share at the later interview by band 25-29, 30-34, ..., 50-55 (the age profile of $G$, not only the modal job);
- transition rates by route: stayers $P(G_t \mid O_{t-1}, \text{stay})$ and $P(O_t \mid G_{t-1}, \text{stay})$ (model:
  both exactly 0, a code check); movers (stay = 0, disp = 0) $P(G_t \mid O_{t-1}, \text{move})$, $P(G_t \mid G_{t-1},
  \text{move})$; displaced pairs the same;
- the net annual inflow into $G$ decomposed by route: share of pairs on the route $\times$ [$P(G_t \mid O_{t-1},
  \text{route}) \cdot (1 - s_G) - P(O_t \mid G_{t-1}, \text{route}) \cdot s_G$], with $s_G$ the share in $G$ at the
  earlier interview; the three routes sum to the change of the $G$ share between the two interviews;
- the displacement rate and the move rate at the earlier interview by job type ($G$ vs $O$), 25-34 and 35-55: the
  test of "$G$ jobs are lost at the same rate";
- a noise control: among sons who are stayers at three consecutive interviews, the share whose type is $O, O, G$
  against $O, G, O$ (a one-way change against a flip-back); if flips dominate, within-employer transitions are coding
  noise and the modal-job definition is the right object.
PSID standard errors: 100 cluster-bootstrap draws (reuse `build_data.bootstrap` with `fn=core.routes`, seed 2026);
model: mean and s.d. over the ten seeds. Writes `output/panel_diag_psid.json` and `final_x4/panel_diag_E.json`
(aggregates, commit both) and `output/panel_diag.md`.

**Verify.** The PSID $G$ share at 25-34 by tercile from the pair sample must be within 0.01 of the modal-job moments
`G_t1_W` 0.066, `G_t3_W` 0.180, `G_t1_B` 0.031, `G_t3_B` 0.117 (different object, so not exact; a larger gap means a
sample error); the modal shares at 35-55 must reproduce `validation_psid.json` exactly (same code path); the model's
stayer transitions are 0 to machine precision; the model's displacement rates by band reproduce `dsp_2534_*`,
`dsp_3555_*` in `estimates_E.json` to 0.001.

**Decision rule for step 6** (written into the md and into Block 4):
- if the within-employer net inflow at 35-55 carries more than half of the PSID's rise in the $G$ share and the
  three-interview check says it is not flip noise: step 6 is *within-employer upgrading*, a stayer in $O$ moves to $G$
  with probability $\pi(a) = \Lambda(\pi_0 + \pi_a (a - 30)/10)$ (two parameters; $\pi_a$ only if the age profile of
  the inflow asks for it, else one);
- else if the inflow through moves at 35-55 is higher in the PSID than in the model while the move rate fits: *access
  that rises with age*, $\alpha_a (a - 30)/10$ in (eq. modelaccess), one parameter;
- else if the displacement rate in $G$ jobs is below that in $O$ jobs by more in the PSID than in the model: *$G$-specific
  job loss*, $\delta_G \mathbf 1[j = G]$ in (eq. modeldelta), one parameter;
- if two apply, code the one with the larger share of the rise; the other is step 7.

**Paper.** Validation item 5, last two sentences, become the route numbers: "Between 25-34 and 35-55 the PSID's share
in $G$ jobs rises by [x]; [y] of it enters through [route] (rate [r] a year, s.e. [s]), [z] through [route]. In the
model [the route] is [0 by construction / too low: value]. The step this asks for is [step 6], estimated next." The
model document gets the statistic in Section "Untargeted validation" and the decision as D13 (Block 7). EVIDENCE 11.12.

## 3. Block 2: the wage-level misfit decomposed (15:20-16:35)

**Why.** The model's mean log wage at 35-49 is 0.11-0.15 above the PSID for both races ($t$ 3.9-6.5) with the level at
25-29 fitted, and Section 8 currently attributes at most 0.02 of it to the overstated gain at a move. The arithmetic
says the source is elsewhere: the PSID's cross-sectional growth from 25-29 to 35-39 is 0.319 (White, 2.595 to 2.914)
and 0.174 (Black, 2.315 to 2.489), while the targeted same-employer growth at 25-34 is 0.060 and 0.056 a year, which
the model fits. For Black sons the cross-section grows by less than a third of what stayers grow; the model, which fits
the stayers, grows 0.293. The difference between stayers' growth and the growth of the cross-section is composition:
who has a wage in each band. In the PSID 60 percent of Black sons observed at 25-29 are not observed at 45-49 (White 42
percent; Table attrition), being observed rises with parental income for White sons (0.139$^{***}$, s.e. 0.028) and not
for Black sons (0.005, 0.031), and 11 percent of Black son-years have zero hours. The model has no attrition and too few
Black zero-hours years. If the composition term is the misfit, the level failure is not an accumulation failure, the
$\gamma$'s stand, and the fix is the IPW moment set (Block 3) and the search friction out of work (`ufric`, running);
if within-son growth is the misfit, the accumulation profile in the thirties is too steep and that is a model result
to state. A referee will ask which; the paper should say.

**Do.** Part 2 of `panel_diag.py`, `core.levels(P)`, by race:
- mean log wage by band 25-29, 30-34, 35-39, 40-44, 45-49 (check against `validation_psid.json` / `validation_E.json`);
- the change between 25-29 and 35-39 (and 35-39 to 45-49) split exactly as $m_2 - m_1 = (m_2^{both} - m_1^{both}) +
  (m_2 - m_2^{both}) - (m_1 - m_1^{both})$, where $m^{both}$ are means over sons with a wage in both bands: within-son
  growth, the composition of band 2 (sons with a wage at 35-39 but not at 25-29: late entrants, returners), the
  composition of band 1 (sons with a wage at 25-29 who have none at 35-39: attriters, non-employed);
- within-son growth implied by the routes: annualised pair growth of stayers, movers and displaced pairs with the
  later interview at 30-39, weighted by route shares, cumulated over ten years (this must land near the within-son
  term; the gap is the years without a pair);
- the calendar check on the PSID only: the band means within five-year birth cohorts against the pooled means (the
  model has no calendar wage growth, so its within-cohort profile is its pooled profile).
Same bootstrap and seeds as Block 1; same json files.

**Verify.** Pair growth by route at 25-34 reproduces `gst_2534_B` 0.056, `gst_2534_W` 0.060, `gmv_2534_B` $-0.006$,
`gmv_2534_W` 0.052, `gds` 0.005 (data) and the model's values in `estimates_E.json`; the three terms sum to the band
change to 1e-10; band means equal the validation json.

**Paper.** Validation item 1 replaces its last sentence with the decomposition: "Of the PSID's growth of 0.32 (White)
and 0.17 (Black) between 25-29 and 35-39, [a] is growth within sons observed in both bands and [b] is the composition
of who has a wage; in the model [a'] and [b']. The model's within-son growth is [too fast by / equal to] ...; the level
failure is [a failure of selection into the wage sample, which the model lacks / an accumulation profile too steep in
the thirties]." "What the model leaves open" is updated in the same words. EVIDENCE 11.13.

## 4. Block 3: the IPW moment set as tested code (16:35-17:35)

**Why.** H4 is identified by the Black IGE at 35-55 on sons with a wage; Black non-employment is 11 percent and Black
attrition 60 percent by 45-49; the Black variance misfit at 45-49 is attrition-shaped; and the 3-hour memo already
called the IPW moments the decisive robustness for H4. It needs the HPC for the estimation but not for the data side,
and the one-step rule says the baseline is re-run on the new set first, so the data side must be ready before Monday.
Section 4's IPW result (the opening moves by $-0.014$, n.s.) says H4 will probably survive; the paper then says so with
the model's number rather than the reduced form's.

**Do.**
- `build_data.py --ipw`: load `41.AgeProfileMeasurement.py` through `importlib` as `build_data` loads 35, build 33's
  child-year frame and call `attrition_block(s)`; keep sons only; the weight of son $i$ in band $b$ is `ipw_b` (1 at
  25-29; $1 / \hat P(\text{observed in } b \mid x, \text{race}, \text{income at 25-29}, \text{cohort})$, clipped at 20,
  as 41 does); sons not in 41's base (no valid income at 25-29) are outside the IPW sample. Write `data/ipw_sons.pkl`
  (person-level, git-ignored; add to `.gitignore` if not covered) and a column `ipw_base` (0/1) in
  `output/sons_types.csv` (one flag per son, already committed as types). Merge the weight into the panel rows by
  (pid, band of the row's age); rows of base sons at ages 50-55 get the 45-49 weight (41 stops at 45-49; say so).
  Match rate of the model's sons observed at 25-29 to 41's base must be above 0.95 (same PSID person ids; if not,
  stop and report).
- `core.moments(P, C)` honours an optional `P["w"]`: weighted means (`np.average`), WLS in `_ols` (scale rows by
  $\sqrt w$), weighted variances; default $w = 1$ everywhere. `simulate_panel` sets $w = 1$ and, when
  `IGE_MOMENTS=ipw`, keeps only sons with `ipw_base = 1` (the same sample restriction on both sides; the model has no
  attrition, so its population moments are the comparison).
- `estimate.py`: `IGE_MOMENTS` (default empty) selects `data_moments[_ipw].json`; log it in `estimates.json`
  (`"moments": "ipw"`); `lattice_q.py` refuses to mix moment sets as it refuses to mix steps.
- Data moments and 500-draw bootstrap s.d. on the IPW sample: `output/data_moments_ipw.json` (aggregate, commit).
- One evaluation: E's theta on the IPW set (`IGE_MOMENTS=ipw`, R = 20, seed 7): $Q$ and $Q$ by block next to the
  unweighted 127.6 and its blocks (from `lattice.json`). Write `output/ipw_first_look.md`.

**Verify.** With `w` set to 1 on the full sample the moments equal `data_moments.json` to 1e-12; on the IPW sample with
$w = 1$ the IGE at 25-29 equals the IPW value (weights are 1 there by construction) and differs from the full sample
only by the sample restriction (report both); the IPW opening of the White $-$ Black wage IGE on bands 25-49 should be
within about 0.02 of 41's IPW result on the same sons (41 uses the parent's age quartic; the moment uses single-age
dummies only); the simulated panel restricted to `ipw_base` sons has the same number of sons as the data side.

**Paper.** Nothing in Section 8 until the HPC estimate exists. The model document's "No attrition is simulated; the
inverse-probability-weighted PSID moments are the robustness version of the targets" becomes a paragraph that defines
the IPW sample, the weights and the switch. EVIDENCE 11.14: the IPW data moments that move most (expect `vlw_4549_B`
and the Black IGE at 40-55) with their unweighted values, and E's $Q$ by block on the IPW set.

**Commands for Monday** (from `~/ige`, after `git pull`; E first, then A, both from the polished solutions; the
baseline on the new set before any step on it):
```
cd ~/ige && git pull
PE=hpc_runs/$(ls hpc_runs | grep ^P_E_j); PA=hpc_runs/$(ls hpc_runs | grep ^P_A_j)
S="IGE_STEPS=age,rehire,xacc IGE_FIX=muG,du IGE_R=20 IGE_SIG0=0.15 IGE_MOMENTS=ipw IGE_MAXFEV=6000,6000,6000,6000,6000,6000,6000,6000"
sbatch --time=01:30:00 --mem=24G --job-name=IGE-E-ipw model/hpc_ige.sh full IGE_MODELS=E IGE_RUN=E_ipw IGE_START=$PE/estimates.json:E $S
sbatch --time=01:30:00 --mem=24G --job-name=IGE-A-ipw model/hpc_ige.sh full IGE_MODELS=A IGE_RUN=A_ipw IGE_START=$PA/estimates.json:A $S
```
(`hpc_ige.sh` must learn the argument `IGE_MOMENTS=*` in its `case` list; one line.) Judged by: `dgx`, `dg1`, `db1`
with their p-values on the IPW set against the unweighted ones, the H4 drop by `fix_seeds.py` (E_ipw against an
A-type restriction is not available without a lattice; report the Wald test and the gap at 45-49), and the Black
variance t at 45-49. If `ufric` has passed by Monday, add `ufric` to `IGE_STEPS` in both.

## 5. Block 4: step 6 coded, tested, with its moments (17:35-18:50)

**Why.** Block 1 names the step; the one-step rule wants it coded and tested before submission; and the fact it
addresses, the $G$ share after 35, is not a target, so the parameter would be identified only indirectly through the
returns and IGE bands. The moments that carry it must be targets: the four modal-$G$ shares at 35-55 by race and
parental tercile (bottom and top), already computed in `core.validation`. A new moment set means the baseline is
re-run on it first (one-step rule), so Monday's submission is two jobs: E on the `g35` set, then E + step 6 on it.

**Do** (only the variant Block 1 chose; the other two stay as notes in the md):
- *Within-employer upgrading* (`IGE_STEPS=gup`, `EXTRA += ["pi0"]` or `["pi0", "pia"]`): in `solve`, the stayer's
  continuation in $O$ becomes $(1 - \pi_a) V^E(m, O) + \pi_a V^E(m, G)$ at the same match, inside the `cur` term for
  $j = 0$ (compute `curG = v1[:, 1, :]` once per $k$); in `simulate`, employed sons in $O$ who neither move nor are
  displaced draw the upgrade with the otherwise unused `D.ut[:, k]` (it is drawn for everyone, used only by offer
  receivers) so common random numbers hold and $\pi = 0$ reproduces E exactly; `JOB` records the new type, `EID`
  unchanged (same employer). Start $\pi_0$ from the PSID's net within-employer inflow (Block 1), scale 0.5.
- *Access rising with age* (`IGE_STEPS=aage`, `EXTRA += ["aa"]`): `access(q, T, a)` with `+ aa (a - 30)/10`; in
  `solve` `pG` is computed per $k$ inside the loop (as `db` is under `age`); in `simulate` `pG` per $k$ for `jo` and the
  entry `jj` at $a_0$. No new draws. Scale 0.2.
- *$G$-specific job loss* (`IGE_STEPS=gloss`, `EXTRA += ["dG"]`): `delta_bar(q, T, a, j)` adds `dG * j`; in `solve`
  `db` per $j$ inside the `for j` loop; in `simulate` `dl` depends on the current `j`. Scale 0.3.
- The `g35` moment set (`IGE_MOMENTS=g35`): `core.moments` appends `G3555_t1_B`, `G3555_t3_B`, `G3555_t1_W`,
  `G3555_t3_W` (the `validation` code moved into a helper both call) when the switch is on; `MOMENT_NAMES` is built
  from the switch; `build_data.py --g35` writes `output/data_moments_g35.json` with the 500-draw bootstrap (3 min;
  commit). The IPW and `g35` switches must compose (`IGE_MOMENTS=ipw,g35`) for later; test the composition once.
- `estimate.py`: `SCALE` entry; `theta_vec` already fills the new parameter with 0, so `P_E/estimates.json` is a
  valid start.

**Verify** (in this order). (1) Invariance: $Q$ at E's theta with the new step on and its parameter at 0, unweighted
66 moments, equals 127.6226 to 1e-6 (one evaluation). (2) The profile: $Q$ on the 66-moment set and on the `g35` set at
E's theta with the new parameter on a six-point grid (12 evaluations at R = 20, about one minute with six workers):
the `g35` moments must pull the parameter (a fall of more than 3.84 at some grid value with everything else fixed is a
lower bound on the joint drop); if the profile is flat on both sets the step cannot be identified by these moments and
the memo for Monday says so instead of submitting it. (3) `SMM_TEST=1 IGE_STEPS=age,rehire,xacc,<step> IGE_FIX=muG,du
IGE_R=5 IGE_MOMENTS=g35 IGE_MODELS=E IGE_START=hpc_runs/<P_E>/estimates.json:E IGE_OUT=<scratch> python estimate.py`
runs end to end (2-3 minutes), then `postestimation.py` on its output. Commit as "IGE model step 6 (<name>): ...; g35
moment set".

**Optional, only if Block 1 leaves two variants tied** (about 25 minutes of 6-core each, within the budget): a pilot
of each variant at R = 5, seed 7, `g35` set, 2,000 evaluations, sigma 0.15, from E; compare their $Q$ with E's $Q$ on
the same draws and set (one evaluation). The pilot picks Monday's job; nothing from it enters the paper (R = 5 draws
are not the lattice's).

**Commands for Monday** (after the IPW pair, or in parallel; names `IGE-E-g35`, `IGE-E6`):
```
cd ~/ige && git pull
PE=hpc_runs/$(ls hpc_runs | grep ^P_E_j)
S="IGE_FIX=muG,du IGE_R=20 IGE_SIG0=0.15 IGE_MOMENTS=g35 IGE_MAXFEV=6000,6000,6000,6000,6000,6000,6000,6000"
j1=$(sbatch --parsable --time=01:30:00 --mem=24G --job-name=IGE-E-g35 model/hpc_ige.sh full IGE_MODELS=E IGE_RUN=E_g35 IGE_STEPS=age,rehire,xacc IGE_START=$PE/estimates.json:E $S)
sbatch --dependency=afterok:$j1 --time=02:00:00 --mem=24G --job-name=IGE-E6 model/hpc_ige.sh full IGE_MODELS=E IGE_RUN=E6 IGE_STEPS=age,rehire,xacc,<step> IGE_START=/mnt/parscratch/users/$USER/ige_smm_results/E_g35_j$j1/estimates.json:E,$PE/estimates.json:E $S
```
(The chain script already resolves a stage's scratch folder by `IGE_RUN` and job id; use that form if the direct path
is wrong.) Judged by `fix_seeds.py --with E6:E --without E_g35:E --label step6` (drop above 3.84 at every seed), the
$t$ of the four new moments before and after, and whether `dgx`, `dg1`, `db1` keep their signs and p-values. If `ufric`
passed, both jobs carry `ufric` in `IGE_STEPS`.

## 6. Block 5: H4 in long differences, with the AFQT (18:50-20:05)

**Why.** The referee's strongest objection to H4 is that "parental income raises accumulation for White sons" is
unobserved ability correlated with parental income, and the paper's own NLSY79 evidence seems to agree: the
same-employer growth gradient net of the AFQT and schooling is 0.002 (0.005) for White sons (Table growthladder,
column 10). Section 8's answer is that the annual-growth regression is underpowered for a parameter the IGE profile
identifies. The test that has the power is the cumulative one: within-son wage growth from 25-29 to 35-39 and to
45-49 on log parental income, net of schooling (PSID) and of schooling and the AFQT (NLSY79). The model's H4 term alone
predicts for White sons $0.021 \sum_{a=27}^{36} e^{-0.093(a-18)} \approx 0.06$ per log point over ten years and about
0.085 over twenty, and about 0.003 for Black sons; the NLSY79 has 1,200-1,800 White men with wages at both ages, so
the standard error of a ten-year change gradient is about 0.02 and 0.06 is testable. A pass validates H4 against
ability with a statistic the model was not fitted to and in a second data set; a fail (White gradient near zero with
the AFQT held fixed) is a null that must be in the text, and it would say H4 is ability, which changes the reading of
the counterfactual (a decomposition by background, not a channel a policy can touch) but not the fact.

**Do.** `IGE/67.LongDifferenceH4.py`:
- PSID: the model's own panel (`model/output/data_panel.pkl`, so the sample is Section 8's), per son the mean log wage
  in 25-29, 35-39 and 45-49; the change (35-39 minus 25-29; 45-49 minus 25-29) regressed on log parental income by
  race, (1) raw, (2) with years of schooling; also the level at 25-29 on the same sons (so the reader sees the
  balanced sample's start). Clusters: 1968 family; stars and p-values; N sons.
- NLSY79: 36's cached men's panel (`data/same_employer_checks_nlsy79.pkl`, `data/career_wage_growth_nlsy79.pkl`:
  hourly rate of pay of the CPS job by round, HGC by 35, AFQT standardised within birth year, log parental income
  1979-81; load through `importlib` of 36 as 42 does); the same statistic, (3) raw, (4) + schooling, (5) + schooling +
  AFQT. Clusters: 1979 household. Black, White, and White $-$ Black with joint influence functions as 36 does.
- Model: `core.longdiff(P)` (same code as the PSID side, in `core.py` next to `validation`), on the simulated panel of
  E at seeds 7-16 (mean, seed s.d.); and, for the reader, the H4 component alone from the closed form above.
- Writer: `paperB_age_profile/tab_h4_longdiff.tex` (one regression per column; columns (1)-(5) data, (6)-(7) model raw
  and net of schooling; rows: log parental income, years of schooling, AFQT; panels White, Black, White $-$ Black; two
  horizons as row blocks; N at the bottom). Output `output/long_difference_h4.csv` and `.md`.

**Verify.** On the PSID the raw ten-year change gradient must sit near the difference of the band IGEs on sons observed
in both bands (Appendix "Balanced panels" / Table gaprobust give the balanced opening; report the two side by side);
on the model the raw gradient must be within 0.02 of `ige_3539_W - ige_2529_W` = 0.166 (the model has no attrition,
so composition is small; a larger gap is a code error); the NLSY79 sample reproduces 36's counts (men, rounds).

**Paper.** Section 8, H4 paragraph of the verdict, after the estimates: "Its reduced-form counterpart is the growth of a
son's own wage over ten years on his parents' income at equal schooling: [x]$^{***}$ (s.e.) for White and [y] for Black
sons in the PSID, [x'] and [y'] in the NLSY79 with the AFQT held fixed, against [m] and [m'] in the model
(Table h4longdiff)." Section 6 (growth with the same employer) gets a footnote pointing from the underpowered annual
regression to the long-difference table. EVIDENCE 11.15. The model document lists the statistic under validation.

## 7. Block 6: the HPC results (20:05-21:05, or when they are in)

**Polish round, `P_*`.** For each model compare $Q$ and the race parameters with Lx4. Expected: A, B, F unchanged; the
question is G and H (H's start was B's solution, G's was A's). Cases:
- every $|\Delta Q| < 0.5$ (A, B, F pattern): the lattice stands; the hypothesis-table note replaces "a polish
  re-estimation of every model (pending); until then the rows through G and H are bounds" with "a polish
  re-estimation of every model (4,000 evaluations at $\sigma_0 = 0.15$ from each model's own solution and its
  neighbours') moved no $Q$ by more than [max]; the rows stand"; the lattice-table note drops "pending"; `final_x4/`
  keeps the Lx4 files (do not swap for identical solutions); EVIDENCE 11.2-11.3 add one clause.
- G or H fell by more than 3.84: copy the polished `estimates.json` of every model into `final_x4/estimates_<M>.json`
  (aggregates), run `lattice_q.py` locally on the ten folders (100 evaluations at R = 20 and 100 at R = 5, about 15
  minutes with six workers, about 6 GB), re-run `h4_seeds.py` / `fix_seeds.py` for the two H4 pairs, `tables.py`,
  and re-read every number in the verdict ("8.5 and 7.5 given H1 as well", the H1 drops, $\alpha_3$ values); if E
  moved, re-run `validation_run.py`, `sensitivity.py` and the h4 `postestimation.py` (about 12 minutes) and re-read
  the fit, validation, counterfactual and sensitivity paragraphs. The verdict changes only if H2 or H3 given H1
  falls below 3.84 at some seed or H1 given both exceeds it at every seed; neither is likely on the profiles.

**`ufric`, E5 and A5.** `IGE_STEPS=age,rehire,xacc,ufric python fix_seeds.py --with hpc_runs/E5_j...:E --without
hpc_runs/P_E_j...:E --label ufric_E` (and the A pair); read `dlu` with its sandwich s.e., the `zero_B` / `zero_W` $t$'s
before and after, `gmv_2534_B`, and `dgx`, `dg1`, `db1` with p-values in E5.
- Pass (drop above 3.84 at every seed, $|t| > 2$, race parameters keep sign and significance): `dlu` enters the
  baseline. Section 8 gets a paragraph "A race-specific search friction out of work" after the H1 paragraph (the step,
  its drop, the estimate, what it fixes), the hypothesis table keeps its lattice at the step-4 baseline with a note
  that the lattice is re-run at the step-5 baseline (Monday jobs: the eight models from their polished solutions with
  `ufric`, one stage, names `IGE-L5-<model>`), and every Section 8 number moves to E5: `validation_run.py`,
  `sensitivity.py`, the h4 `postestimation.py` (E5's folder carries the standard `postestimation.json`), `tables.py`
  with `SEL`/paths pointed at the E5 files copied into `final_x4/`. That is about 25 minutes of compute and an hour of
  re-reading; take the hour from Block 8. The model document's D12 becomes "estimated: kept".
- Fail: "What the model leaves open" says "tested and rejected (drop [x], s.d. [y] over ten seeds; $dlu$ = [v], s.e.
  [s], $p$ = [p])", the non-employment misfit stays listed, and D12 becomes "estimated: rejected, parsimony". No
  other number changes.
- Partial (passes the seeds, fails the Wald, or the reverse): "not separable in these data", dropped under the
  parsimony rule, said in the text with both numbers.
In every case `tables.py` is the only writer of table numbers; EVIDENCE 11.8 is updated.

**If nothing has arrived by 22:50**: write the three cases into the status note with the commands, and leave the
"pending" wording as it is.

## 8. Block 7: the appendix that tells the journey (21:05-22:05)

**Why.** The paper's rule is fact, hypotheses, tests, with nulls in the text and failed designs in the appendix. Section
8 states the model as if it had been written down once; its footnotes carry the steps (age slopes $-111$, same-year
re-employment $-36$, $\mu_G = 0$ at $+2.8$, $d_u = 0$ at $+6.2$, $\gamma_x(r)$ $-42.5$, the first lattice that selected
H2 + H3 and reproduced half the opening). A referee reading the footnotes will ask for the sequence in one place, and
the first lattice's result is the paper's best argument that H4 was not assumed: the model without it was tried first,
selected the schooling hypotheses, and left half the opening unexplained.

**Do.** `tables.py: tab_steps()` reads a hand-listed sequence of run folders (all in git under `hpc_runs/`): the first
lattice A-D (`ige_full_20261018_125238`), the yardstick runs, step 2 (`_194443_j11859359`, `_195922_j11859360`), step
3 (`_200455_j11859361`, `_200456_j11859362`), $\mu_G$ (`_200456_j11859363`), $d_u$ (`_212217_j11860451`), step 4
(`_213123_j11860453`, `_j11860454`), the final lattice at R = 20 (`Lx4_*`), the polish (`P_*`), step 5 (E5/A5 if in).
Columns: step; what changed (one line); model; $Q$ at the step's draws; $\Delta Q$ against the previous step on the same
draws; the misfit it addressed ($t$ before, $t$ after); run folder. Each `estimates.json` carries `steps`, `fixed`, `R`
and $Q$, so the table is generated, not typed; the note states that $Q$'s are comparable only within a draw set (R = 5
seed 7 for steps 1-4, R = 20 for the lattice). `appC_model.tex` ("How the model was built", half a page): the first
lattice and its half-opening (gap 0.159 at 45-49, White IGE too flat, Black IGE rising); the displacement block
misfits and steps 2-3; the two fixed parameters; step 4 and the H4 test at the two ends of the lattice; the final
lattice at R = 20 with chained starts; the polish; step 5; what is next (step 6 from Block 1, the IPW set).
`\input{appC_model}` after `appB` in `main.tex`; one sentence in Section 8's introduction pointing to it. Model
document: D13 (step 6, the variant chosen, pending) and the IPW definition; no results (its rule).

**Verify.** The $\Delta Q$ column reproduces the footnote numbers in `sec7_model.tex` (111, 112, 36, 2.8, 6.2, 42.5,
$-0.3$) and EVIDENCE 11.7; the first-lattice gap 0.159 matches the $\gamma_x$ footnote; compile.

## 9. Block 8: the policy paragraph on H4 (22:05-22:50)

**Why.** The PI's question is what the paper says about policies, and the selected channel is the one no listed policy
touches. The paper must say what H4 is and is not, in public-data terms, and not overreach. What the data already say
(EVIDENCE 9 and 36 Section C, NLSY79, same-employer pairs of White sons at 25-34): company training rises with parental
income (0.020$^{***}$, s.e. 0.006) and so does employer size (0.387$^{***}$ in log employees, 0.098); union coverage does
not (0.021, 0.015); but holding training, union, firm size and tenure fixed leaves the parental-income gradient of
growth where it was (0.007 (0.005) to 0.007 (0.006); explained 0.000, s.e. 0.001); a job found through friends or
relatives grows more slowly ($-0.015^{***}$, 0.005) and explains 0.001$^{*}$ (0.001) of the gradient; following the
father's industry pays at entry, not in growth (9.19); and the AFQT does not carry the growth gradient
(Table growthladder). So the pay-off of background in accumulation is not training, union status, firm size, tenure,
networks into the job, the father's industry, or measured ability, as far as public data observe them.

**Do.** Four sentences at the end of the Counterfactuals subsection, after "a policy scored at 30 sees 60 percent":
what H4 is (the growth of a son's wage with his parents' income at equal schooling and job type, for White sons only);
what it is not, with the numbers above and the scripts in a footnote (`IGE/36.SameEmployerGrowthChecks.py`,
`IGE/32.IndustryCareers.py`); the policy statement that follows (the policies the model can score, schooling,
hiring, entry conditions, act on the start and close less than a tenth at 45; the channel that carries the gap is
inside jobs and is not reached by them; a policy acting on it would have to act on what employers do with equally
schooled men over the first twenty years, which the public data do not observe); and the honest limit (no public data
set observes the employer, so the channel is named, bounded and left to the next step). Block 5's long-difference
result enters here if it is in. EVIDENCE 11.1's policy column is updated. House rules: no "small", no hedging lists of
what H4 "might proxy for" beyond the tested items.

**For the PI, not to be changed tonight.** The abstract's "three fifths of the gap at 45-49" is a level share; the
second read suggested "three fifths of the gap at 45-49 and two fifths of its opening". Put it in the status note.

## 10. Block 9: close (22:50-23:50)

HPC check; `pdflatex` twice with `bibtex`; `python tables.py`; `git status` shows only the files of Blocks 1-8; commit by
file name; `git fetch; git merge origin/main; git push`. `proposals/status_20261019_night.md`: what each block found
(with the numbers), what changed in the paper (file and paragraph), what is pending on the HPC and the exact Monday
commands in the order IPW baseline, `g35` baseline, step 6, then the lattice at the step-5 baseline if `ufric` passed;
the PI's two calls (abstract wording; whether step 6's variant is the one to submit).

## 11. Skipped, and why

- **NLSY79 / NLSY97 cohort simulation.** Needs a types file with the NLSY parental measure, its reliability correction
  and three-year income; half a day of data work, and the NLSY79 opening (0.04-0.09) is a different object from the
  PSID's 0.21 until the correction is built in. After Block 5's NLSY79 long difference, which is the cheap version of
  the same question.
- **Earnings IGE validation.** No hours in the model; Section 5 shows hours carry 0.010-0.012 of the elasticity.
- **Rank reconciliation across family income, earnings and wages.** Done in dd7ec63 (family-income ranks do not
  diverge; wage ranks 0.187$^{***}$ at 45-49, own-earnings ranks 0.150$^{*}$ at 40-44); only the abstract wording is
  open, and that is the PI's.
- **Block-balanced or full-covariance weights.** HPC, and answered in the Estimation paragraph (the IGE moments
  contribute 4.9 of 127.6 because they are fitted, not down-weighted).
- **Any local re-estimation at R = 20.** Five hours of six cores for one model; the optional R = 5 pilots in Block 4 are
  the only estimation-like compute, and they decide a submission, not a number in the paper.
- **The autocovariance misfit ($-0.048$ against $-0.037$, $t = -3.6$).** An MA(1) in the transitory shock would fix it
  with one parameter; it touches nothing racial; step 7 at the earliest.
- **A public-sector job type.** Rejected by the data (10.6: the opening among private starters is 0.213$^{***}$ against
  0.232$^{***}$).
- **Rewriting the introduction and conclusion.** Both already carry the model's verdict in the paper's words; tonight's
  blocks add numbers to Section 8 and an appendix, and the PI reads the frame tomorrow. Changing frame sentences
  unattended is where the shared-tree rule and the "PI's call" rule both say stop.

---

# Second ten hours, 14:55-00:55 (Fable, 2026-10-19, after the first plan ran in one hour)

Read at dc70403: `status_20261019_afternoon.md`, `sec7_model.tex` (verdict, validation, policy, what remains),
`appC_model.tex`, `tab_h4longdiff.tex`, `tab_model_steps.tex`, `output/long_difference_h4.md`,
`67.LongDifferenceH4.py` (header and NLSY79 builder), EVIDENCE 11.12-11.16, the columns of `data/psid_kids.pkl` and
`data/nlsy79_kids.pkl`, `3.NLSY97.py` and `29.NLSY97AgeProfile.py` (hourly wage = earnings / hours, parental income
1996 and the 1997-2000 mean), the reliability ratios in `4.Estimates.py` / `age_profile_robustness.md` (one year W
0.585, B 0.565; 12-17 mean W 0.650, B 0.631). Nothing run; nothing edited but this file.

**Short answer.** The afternoon changed the question. H4 is the paper's headline and it now rests on the PSID alone:
in long differences at equal schooling the PSID gives White sons 0.073$^{***}$ (ten years) and 0.135$^{***}$
(twenty), the model 0.074 and 0.103, and the NLSY79 $-0.001$ (0.020) and 0.021 (0.026). Before anything else is
written, that disagreement has to be explained or measured, and public data can do most of it tonight: (1) the NLSY79's
parental income is a one-to-three-year measure at the youth's ages 14-22 with a reliability near the PSID's one-year
0.585, and in a regression with a well-measured correlate (schooling) attenuation of the mismeasured regressor is worse
than its reliability; the PSID carries the same one-year and 12-17-mean measures for the same sons
(`psid_kids.pkl`: `lpinc_pt`, `lpinc_av`), so the PSID can be read through the NLSY79's measure, the errors-in-variables
correction with the known ratios can be applied to both, and the model can be read through a parental-income measure
of NLSY79 reliability by adding noise to $x$ in the statistic on the simulated panel; (2) the NLSY97 is a third data set
with hourly wages to the late thirties and a one-year and a four-year parental measure, untouched for this statistic.
What those two blocks say decides the headline's wording, which is the PI's and is not changed tonight; the memo gives
the sentence for each outcome. Then: Section 8 is 6,600 words with nine tables, a third of the paper; a cut list moves
2,500 words and five tables to appendices and puts one figure in their place. Then the reading tools for the HPC
results (a judging script and a regeneration script, so every incoming estimate is judged by the same rule and the
paper's E-dependent numbers are rebuilt by one command), the integration itself when results land, robustness of the
long differences, the model-document sync, a consistency read, and the status note.

Compute: about 35 minutes of 6-core time in all (ten simulations for the noisy-$x$ statistic, the test runs of the
two scripts, and, if P_E or `ufric` change the selected model, one regeneration of about 15 minutes). Rules as in the
morning plan; in addition, no change to the abstract or the introduction's frame, and no new top-level claims about
H4 in the text beyond what the new tables show.

## 0. Timetable

| Time | Block | Local compute | Deliverable |
|---|---|---|---|
| 14:55-15:05 | 0. Setup, HPC check | none | clean start |
| 15:05-16:35 | 1. H4 across data sets: measurement of parental income | 10 simulations (2 min) | `67` extended; `tab_h4longdiff` panel B; the "H4 in long differences" paragraph rewritten; EVIDENCE 11.17 |
| 16:35-17:50 | 2. NLSY97 long differences | none | `67` NLSY97 columns; EVIDENCE 11.18 |
| 17:50-19:20 | 3. Section 8 referee-proofed: cuts, Appendix D, the fit figure | none | `sec7_model.tex` shorter; `appD_model.tex`; `model/figure_fit.py`, `fig_model_fit.png`; `tables.py: tab_diag()` |
| 19:20-20:20 | 4. Reading tools: `judge_step.py`, `regen.py` | 40 + ~60 simulations (about 12 min) | two scripts tested on existing runs; three pre-written readings |
| 20:20-21:20 | 5. HPC integration (P_H, P_E, P_D, the noH4 pair, E5/A5), when in | `judge_step`, `regen`, `lattice_q` if needed (up to 30 min) | `final_x4/` updated; Section 8 numbers; table notes; EVIDENCE 11.2/11.3/11.8 |
| 21:20-22:05 | 6. Robustness of the long differences; model document sync | none | appendix paragraph; `model_document.tex` validation list, D13, IPW set; EVIDENCE 11.19 |
| 22:05-22:50 | 7. Consistency read of the whole paper against the afternoon's results; the PI's sentence list | none | fixes in Sections 4, 6, 8; `status` section "for the PI" |
| 22:50-00:55 | 8. HPC check, compile, commit, push, status note; buffer | none | `proposals/status_20261019_night.md` |

Drop order if a block overruns: 6 first, then 2 (the NLSY97 part only), then 3 is cut to the appendix move without the
figure. Never cut 1, 4 or 5. HPC checks at every block boundary as before (`git fetch origin; git log --oneline
HEAD..origin/main | Select-String "IGE HPC results"`), merge when something is there.

## 1. Block 1: H4 across data sets, the measurement of parental income (15:05-16:35)

**Why.** The paragraph "H4 in long differences" ends with "a PSID result that the NLSY79 neither confirms nor
attributes to measured ability" and a footnote that asserts the attenuation argument without a number. A referee reads
that as the headline failing out of sample. The argument is testable in the PSID itself, where the same sons have the
13-19 mean, the 12-17 mean and one year of parental income (Section 4 already does this for the opening: replacing the
13-19 mean by one year lowers the family-income opening from 0.162 to 0.093). Three pieces, one script:

- **(a) The PSID read through the NLSY79's measure.** Re-run the long differences (ten and twenty years, by race, raw and
  net of schooling) with `x` = `lpinc_pt` (one year at 16) and `lpinc_av` (12-17 mean), merged into the model's panel
  by `pid` from `data/psid_kids.pkl` (the panel keeps the 13-19 mean as `x`; add `x1`, `x6`). Prediction if measurement
  is the explanation: the raw White ten-year gradient falls from 0.180 toward 0.105 (0.180 $\times$ 0.585) and the
  net-of-schooling gradient from 0.073 to roughly 0.03-0.04 (with a correlated well-measured regressor the attenuation
  factor is $(\lambda - \rho^2)/(1 - \rho^2)$, where $\rho^2$ is the $R^2$ of the observed $x$ on schooling, about 0.2
  in these data); the NLSY79's $-0.001$ (0.020) is within one standard error of that. If the PSID one-year gradient net
  of schooling stays at 0.06-0.07, measurement is not the explanation and the disagreement is cohort or data set.
- **(b) The errors-in-variables correction, both data sets.** With one regressor mismeasured and its reliability $\lambda$
  known, $\beta = (S - D)^{-1} s_{xy}$ with $S$ the regressor covariance, $D = \mathrm{diag}((1 - \lambda)\,
  \mathrm{var}(x_{obs}), 0)$; standard errors by 200 cluster-bootstrap draws (families / 1979 households), $\lambda$
  treated as known as Section 4 does (PSID one year 0.585 / 0.565, 12-17 mean 0.650 / 0.631; NLSY79: its own ratio from
  `age_profile_round2.md` A6, else the PSID one-year ratio with a sentence saying so). Report the corrected ten- and
  twenty-year gradients net of schooling for PSID one-year, PSID 12-17 mean and NLSY79. The verification is internal:
  the corrected PSID one-year and 12-17-mean values must land on the 13-19-mean value (0.073, 0.135) within their
  standard errors; if they do, the same correction applied to the NLSY79 is credible.
- **(c) The model read through an NLSY-grade measure.** `core.longdiff(P, x=...)` on the simulated panel of E (seeds
  7-16, R = 20) with $x$ replaced by $x + u$, $u \sim N(0, \sigma_u^2)$, $\sigma_u^2 = (1/\lambda - 1)\,\mathrm{var}(x)$
  for $\lambda$ = 0.585, drawn once per son with the seed; raw and net of schooling (the son's actual schooling, which
  is correlated with the true $x$ as in the data). This is the model's prediction for a data set with the NLSY79's
  parental measure. Expect the net-of-schooling White value to fall from 0.074 to about 0.03; the closer it is to the
  NLSY79's $-0.001 \pm 0.020$, the more the null is what the model predicts under that measurement.

Also in the script, cheap: the PSID long differences restricted to sons born 1957-64 (the NLSY79 cohort) and to the
SRC sample, so cohort and sample are separated from measurement in the same table (if the 1957-64 cell is below 400
White sons, report it with its standard error and do not interpret).

**Deliverable.** `67.LongDifferenceH4.py` extended (`--measures`), `tab_h4longdiff.tex` gains panel B "Parental-income
measurement" (columns: PSID 13-19 mean, 12-17 mean, one year, one year corrected, NLSY79, NLSY79 corrected, model with
NLSY-grade noise; rows: White, Black, White $-$ Black, ten and twenty years, all net of schooling, s.e. in parentheses,
seed s.d. in brackets for the model). The "H4 in long differences" paragraph is rewritten to state the result:
either "the disagreement is the measure: read through one year of parental income the PSID gives [a] and the model
[b], the NLSY79's [c]; corrected for reliability all three are [d]-[e]" or "it is not the measure: the PSID gives [a]
with one year of parental income; the NLSY79 cohort / data set shows a smaller pay-off of background in growth, as it
shows a smaller opening (Section 4)". Footnote: formulas, ratios, script. EVIDENCE 11.17. **The abstract and the
introduction are not touched**; Block 7 gives the PI the sentence for each outcome.

**Verify.** The raw PSID 13-19-mean values reproduce the existing table (0.180, 0.073, 0.135); the one-year raw
gradient's ratio to the 13-19 one is within 0.1 of the reliability ratio; the correction applied to the PSID 13-19
mean with $\lambda$ = 0.650 (the closest known ratio) moves the gradient up by less than its standard error; the
model's noiseless statistic reproduces 0.074 / 0.103.

## 2. Block 2: the NLSY97 as a third data set (16:35-17:50)

**Why.** Two data sets disagree; a third with its own parental measure (one year 1996 from the parent interview, and
the 1997-2000 mean while the youth lives at home) and hourly wages to the late thirties breaks the tie on the
ten-year statistic. The cohort born 1980-84 reaches 35-39 in 2015-2023, so the 25-29 to 35-39 change exists for most
of it (the 1984 cohort is 37-38 at the 2021-22 round; take the 35-39 mean over the rounds available, two rounds
minimum). Section 4 already uses the NLSY97 for the opening (0.058 (0.040) with one year; 0.131 corrected), so the
reader expects it here.

**Do.** In `67`, a `nlsy97_sons()` builder from `29.NLSY97AgeProfile.py`'s extract (`load_extract()`; hourly wage =
earnings / hours with 29's validity rule, log; parental income `lpinc_pt` 1996 and the 1997-2000 mean; highest degree
or years of schooling as 29 defines them; male, Black and non-Black non-Hispanic as in 29). Columns (8)-(10): raw, net
of schooling, and net of schooling with the one-year measure corrected by the NLSY97's own reliability ratio (29 /
`age_profile_round2.md` A6 have it; else say "PSID one-year ratio"). Ten years only. Clusters: household. Stars,
p-values, N. Note in the table that the NLSY97 "White" is non-Black non-Hispanic.

**Verify.** The N of men with a wage at 25-29 reproduces 29's counts; the raw ten-year gradient should be of the
order of the NLSY97's one-year opening on bands 25-39 (29's output); the ASVAB is not in 29's extract, so the AFQT
column is NLSY79-only and the note says so (adding the ASVAB means a column read of the 1997 release; not tonight).

**Paper.** One sentence in the long-difference paragraph; EVIDENCE 11.18. If the NLSY97 sides with the PSID (a
positive White gradient net of schooling), the paragraph says two of three data sets; if with the NLSY79, the headline
sentence for the PI (Block 7) must carry the caveat.

## 3. Block 3: a referee-proof Section 8 (17:50-19:20)

**Why.** Section 8 is 6,594 words with nine tables (identification, hypotheses, lattice, long differences, estimates,
fit, untargeted, counterfactuals, H4 by age and tercile) against 2,283 for the careers section; a referee's first
comment will be length and the second that validation diagnostics (routes, levels, profiles) are written as prose
with typed numbers. Target: about 4,000 words, four tables and one figure in the main text; everything else generated
and in two appendices (C "How the model was built", existing; D "Estimates, fit and validation", new).

**Cut list, in order (paragraph, destination).**
1. "What can be solved without simulation" (subsection): keep three sentences (homogeneity, the stayers' closed form
   as starting values, every parameter estimated jointly); the rest, with the starting-value footnote, to the model
   document (it is already there) and one sentence of pointer.
2. Table modelid (identification): keep in the main text (it is the identification argument); shorten its notes.
3. Table modellattice: to Appendix D; the verdict cites Table modelhyp only.
4. Table modelest (estimates): to Appendix D; the main text keeps the four-line estimates paragraph.
5. Table modelfit: to Appendix D; in its place a figure `fig_model_fit.png` from `model/figure_fit.py` reading
   `estimates_E.json` (model moments) and `data_moments.json` (PSID values and s.d.): two panels, the log-wage IGE by
   band and race (PSID with 95% bands, model as lines) and the return to schooling by band and race; a third small
   panel with the White $-$ Black gap. Follow the `dataviz` skill (load it before writing the plotting code). The "Fit"
   paragraph keeps its numbers (they are the paper's fact reproduced) and cites the figure and the appendix table.
6. "Untargeted validation": the list of six items becomes one paragraph of verdicts (one sentence each: passes / fails,
   with the headline numbers), and the long item 1 (levels decomposition) and item 5 (routes, displacement by job type,
   the two profiles) move to Appendix D as two short subsections with a generated table `tab_model_diag.tex`
   (`tables.py: tab_diag()` from `output/panel_diag_psid.json` and `final_x4/panel_diag_E.json`: the within-son and
   composition terms by race; the $G$ share by band; the net inflow by route; displacement by job type). The numbers
   now typed in the text are then checkable against a generated table, as the house rule requires.
7. "H4 in long differences" with Table h4longdiff: move from the verdict to the validation paragraph, as its first
   item ("the one statistic the model was not fitted to that bears on H4 directly"), after Block 1's rewrite. The
   verdict then reads H4, H2 + H3, H1, selected model, without interruption.
8. Table modelcfh4 (by age and tercile): to Appendix D; "Which sons, which ages" keeps its four numbers.
9. "What policy could reach the channel": keep, at most 150 words; the NLSY79 source numbers stay in the footnote.
10. "What the model leaves open": keep the misfit list and the two next steps (five sentences); the IPW footnote moves
    to Appendix D's validation subsection.
11. Appendix C: add one line per next step as they are estimated; otherwise unchanged.

**Do.** `appD_model.tex` with `\section{The Model: Estimates, Fit and Validation}\label{app:modelfit}`, inputs in the
order lattice, estimates, fit, untargeted, cfh4, diag, sens (`tab_model_sens` moves out of `appB` into D); `main.tex`
inputs D after C. Every `\ref` re-resolved; `pdflatex` twice; the word count of `sec7_model.tex` reported in the
commit message. No wording of substance changes in what is kept; this block moves, it does not rewrite.

**Verify.** Compile with no undefined references; the figure's plotted values equal the fit table's (print both in
the script); word counts before and after.

## 4. Block 4: the reading tools (19:20-20:20)

**Why.** Six estimation results are pending or imminent (P_H, P_E, P_D, P_AnoH4, P_EnoH4, E5/A5) and three more come
Monday (E_ipw, A_ipw, E_g35, E6). Each is judged by the same rule (drop over ten seeds, Wald test, the misfit it was
aimed at before and after, the race parameters' stability), and each change of the selected model means the same
eight regeneration steps. Two scripts make that a five-minute job per result instead of an hour, and remove the risk
of a hand-typed number.

**Do.**
- `model/judge_step.py --with <run>:<M> --without <run>:<M> --moments <set> --steps <steps> --label <name>`: runs
  `fix_seeds` (ten seeds, R = 20) for the pair; prints a table of the new parameter(s) with sandwich s.e. and p;
  $Q$ by moment block at the estimation draws for both; the $t$-ratio of every targeted moment whose $|t|$ changes by
  more than 1 (before, after); the race parameters (`a3`, `dg1`, `db1`, `dgx`) with s.e. and p in both; the gap at
  30-34 and 45-49 in both; a verdict line by the paper's rule (pass / fail / not separable). Writes
  `output/final_x4/judge_<label>.json` and `.md`. Test: `--with Lx4_E:E --without ige_full_..._j11861516:E` (H4 given
  H2 + H3) must reproduce `h4_seeds.json`'s drop 36.1 (s.d. 3.5, min 29.1).
- `model/regen.py --run <folder> --model E`: copies the run's `estimates.json` and `postestimation.json` into
  `final_x4/` under the paper's names (aggregates only), then runs in order `validation_run.py`, `sensitivity.py`,
  `postestimation.py` with `IGE_CFS` for the h4 table, `panel_diag.py`, `67.LongDifferenceH4.py --model-only`,
  `steps_summary.py`, `tables.py`, and `figure_fit.py`; prints a diff of every table against the previous version.
  Test on the current E: every table byte-identical (about 15 minutes of compute).
- Three readings pre-written in the status note (Block 8) with blanks: the polish round (lattice stands / G or H
  moved); `ufric` pass / fail / not separable with the exact paragraph each adds to Section 8 and what it changes in
  Appendix C and the model document (D12); Monday's `E6` and `E_ipw` readings in the same form.

## 5. Block 5: HPC integration (20:20-21:20, or when results land; 22:50 at the latest)

As in the morning plan, Section 7, now with the scripts of Block 4:
- P_H, P_D, P_E, P_AnoH4, P_EnoH4: $|\Delta Q| < 0.5$ for all: table notes rewritten ("a polish re-estimation of every
  model moved no $Q$ by more than [max]"), `final_x4/` kept, EVIDENCE 11.2/11.3 one clause; Appendix C's "among the
  models returned so far" becomes "any model". Any model moved by more than 3.84: copy the polished solutions,
  `lattice_q.py` locally (15 minutes), `fix_seeds` for the H4 pairs, `regen.py` if E moved, re-read the verdict.
- E5/A5 (`ufric`): `judge_step.py --with E5:E --without P_E:E --steps age,rehire,xacc,ufric`. Pass: `regen.py --run E5`;
  the new paragraph after H1; the lattice note "re-run at the step-5 baseline (Monday)"; Appendix C step 6 line; D12
  "kept". Fail: the sentence in "What the model leaves open" with drop, s.d., estimate, s.e., p; D12 "rejected". Not
  separable: dropped under parsimony, both numbers in the text.
If `ufric` passes, Monday's commands in the status note carry `ufric` in `IGE_STEPS` for the IPW and `g35` jobs
(already written in the afternoon note; only the flag changes).

## 6. Block 6: robustness of the long differences; model document (21:20-22:05)

**Robustness** (same script, `--robust`; appendix text and a note line, no new table unless a row changes the
reading): earnings instead of hourly wages (the paper's Section 4 object); the SRC sample only; weighted; sons with a
wage in all three bands (balanced, reported with its N and not used as evidence against anything); the 25-29 to 30-34
and 25-29 to 40-44 horizons (the shape); schooling as degree dummies instead of years (if the White net-of-schooling
gradient is sensitive to the functional form of schooling, say so). EVIDENCE 11.19. One sentence in the Appendix D
validation subsection.

**Model document**: the validation list gains the routes, levels and long-difference statistics (as computed, with
the scripts); D12 (`ufric`) updated per Block 5; D13 (G-specific job loss, with the `g35` set, the profile that chose
it over access by age, and the IPW set defined with its weights and sample); no results in the document.

## 7. Block 7: consistency read and the PI's sentence list (22:05-22:50)

Read Sections 1, 4, 6, 8 and the conclusion against the afternoon's results and tonight's, and fix only Sections 4-8:
- Section 6's same-employer paragraph ("the racial difference in growth within the same job is not established") and
  the new long-difference evidence must point at each other (a footnote in Section 6 was planned; check it is there and
  that its numbers are the rewritten ones).
- Section 4's four-data-set paragraph and the H4 paragraph use the same reliability ratios and the same wording for
  the correction; a cross-reference each way.
- Section 8's validation count ("five pass and three fail") after the long differences are moved into it.
- The policy paragraph's NLSY79 numbers (training 0.020$^{***}$ (0.006), size 0.387$^{***}$ (0.098), union 0.021 (0.015),
  explained 0.000 (0.001), friends $-0.014^{***}$ (0.004), 0.001$^{**}$) against `same_employer_growth_checks.md` once
  more, since my morning memo had two of them slightly off.
- Terminology sweep of the new text ("search friction", "accumulation"; no "small", "little", "slightly" for precise
  shares).
Then the list for the PI, with the current sentence, the proposed replacement under each Block 1-2 outcome, and the
file and line: the abstract's "parental income raises the growth of human capital for White sons and not for Black
sons" and "three fifths of the gap at 45-49"; the introduction's lines 67-73; the conclusion's "it selects the one in
which parental income raises the growth of human capital for White sons". If measurement explains the NLSY79 (Block
1) and the NLSY97 sides with the PSID (Block 2), the proposal is one clause in the abstract ("in the PSID, and in
long differences in the NLSY97; in the NLSY79 the pay-off of background in growth is absorbed by schooling, as its
one-year parental measure predicts"); if not, the proposal is the caveat in the abstract and a paragraph in the
conclusion that states H4 as a PSID result with the two other data sets' values. Not applied tonight.

## 8. Block 8: close (22:50-00:55)

HPC check; `pdflatex` twice with `bibtex`; `python tables.py`; `python model/regen.py --check` (tables unchanged by a
re-run); `git status` shows only tonight's files; commit by file name; fetch, merge, push.
`proposals/status_20261019_night.md`: Block 1-2 results with numbers and the reading; the Section 8 word count and
table count before and after; the three pre-written HPC readings with blanks or filled; Monday's commands (unchanged
from the afternoon note, `ufric` flag per Block 5); the PI's sentence list from Block 7.

## 9. Skipped tonight, and why

- **A simulated NLSY79 cohort** (types file with the NLSY parental measure): Block 1(c) gives the model's prediction
  under NLSY-grade measurement on the PSID sons, which is the comparison the paragraph needs; a cohort simulation adds
  the cohort's own schooling distribution and birth years, a day's work, after the measurement answer.
- **The ASVAB in the NLSY97**: a column read of the 1997 release (minutes of reading, but a new extract to verify);
  the NLSY79's AFQT already answers the ability question in one data set.
- **An MA(1) transitory shock, within-employer upgrading, access by age**: step 7 candidates or rejected; nothing
  tonight.
- **Any estimation**: nothing local; the `g35` and IPW jobs are Monday's.
- **Abstract, introduction, conclusion frame**: the PI's, with the sentence list ready.
