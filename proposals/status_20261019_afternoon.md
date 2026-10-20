# Paper B status, 2026-10-19 14:50 (Fable 10-hour plan, local blocks done in one hour)

## For the PI first

1. **H4 does not replicate in the NLSY79 beyond schooling** (Block 5, Table `tab:h4longdiff`). Long differences of a
   son's own wage on log parental income: PSID at equal schooling White 0.073\*\*\* (10 years) and 0.135\*\*\* (20 years),
   Black about 0, and model E (not fitted to them) 0.074 and 0.103. NLSY79: raw White 0.081\*\*\*, but at equal schooling
   -0.001 (0.020) and 0.021 (0.026), with or without the AFQT. Section 8 now says H4 is a PSID result that the NLSY79
   neither confirms nor attributes to measured ability. **The abstract and introduction still state H4 without this
   caveat; how to frame the headline is your call** (options: add "in the PSID; in the NLSY79 the pay-off of background
   in growth runs through schooling"; or keep the headline and leave the caveat to Section 8).
2. **The next model step is G-specific job loss, not access by age** (Block 4). Profiles at E's estimates: access
   rising with age barely moves the G share after 35 (0.131 -> 0.137); a separate job-loss rate for G jobs raises it
   toward the PSID (0.131 -> 0.169) and lowers Q on the extended moments by 11.7 with everything else fixed. The PSID
   loses G jobs at half the rate of O jobs.
3. **The wage-level misfit after 35 is growth within sons, not attrition** (Blocks 2-3): within-son growth 25-29 ->
   35-39 PSID 0.332 / 0.189 (W / B), model 0.442 / 0.310; attrition weights leave the IGE opening at 0.267 (from 0.274)
   and the Black variance at 45-49 at 0.346 (from 0.345).
4. The abstract's "three fifths of the gap at 45-49" is a level share (two fifths of the opening): your call.

## Done (all pushed, origin/main 6728b0a)

| Block | Result | Paper | EVIDENCE |
|---|---|---|---|
| 1 routes into G jobs | PSID net G inflow after 35 only through same-employer reclassification (much of it flips); model loses G jobs through moves and displacement; W movers from O enter G at 0.121 (PSID) vs 0.055 (model) after 35 | validation item 5 | 11.12 |
| 2 wage-level decomposition | within-son growth too fast by 0.11-0.12, composition small | validation item 1 | 11.13 |
| 3 IPW moment set | 4,162 sons, weights from script 41; moments barely move; `IGE_MOMENTS=ipw` coded and tested; E on the IPW set Q 113.7 | footnote, "what remains" corrected | 11.14 |
| 4 next step | `aage` rejected by profile; `gloss` (dG) coded, identified (s.e. 0.29), `g35` moment set (70 moments) with bootstrap draws | validation item 5, what remains | 11.16 |
| 5 H4 long differences | PSID passes, NLSY79 does not replicate beyond schooling | Table h4longdiff + paragraph | 11.15 |
| 7 appendix | Appendix C "How the Model Was Built" with Table modelsteps generated from the run folders | appC_model.tex | |
| 8 policy paragraph | the channel is inside jobs; NLSY79 sources (training, firm size, union, networks) do not carry it | Section 8 | |

## HPC: running and next

Running: polish round P_* (P_A, P_B, P_F, P_G, P_C back, all unchanged: max |dQ| 0.06); P_H, P_E, P_D, P_AnoH4,
P_EnoH4 pending; step 5 `ufric` IGE-E5 (11866020), IGE-A5 (11866021) pending.

**Before the next submissions copy the updated person-level types file (it now carries `ipw_base`) to Stanage**, from
PowerShell on the PC:

    scp "G:\My Drive\JointLoss\model\output\sons_types.csv" cm1jil@stanage.shef.ac.uk:~/ige/IGE/model/output/sons_types.csv

Then on Stanage (`cd ~/ige && git pull` first):

    PE=hpc_runs/$(ls hpc_runs | grep ^P_E_j); PA=hpc_runs/$(ls hpc_runs | grep ^P_A_j)
    # (a) IPW robustness of the selected model and of A (the baseline on the new set)
    S="IGE_STEPS=age,rehire,xacc IGE_FIX=muG,du IGE_R=20 IGE_SIG0=0.15 IGE_MOMENTS=ipw IGE_MAXFEV=6000,6000,6000,6000,6000,6000,6000,6000"
    sbatch --time=01:15:00 --mem=24G --job-name=IGE-E-ipw model/hpc_ige.sh full IGE_MODELS=E IGE_RUN=E_ipw IGE_START=$PE/estimates.json:E $S
    sbatch --time=01:15:00 --mem=24G --job-name=IGE-A-ipw model/hpc_ige.sh full IGE_MODELS=A IGE_RUN=A_ipw IGE_START=$PA/estimates.json:A $S
    # (b) step 6 on the extended moments: baseline E on g35, then E + G-specific job loss
    G="IGE_FIX=muG,du IGE_R=20 IGE_SIG0=0.15 IGE_MOMENTS=g35 IGE_MAXFEV=6000,6000,6000,6000,6000,6000,6000,6000"
    j1=$(sbatch --parsable --time=01:15:00 --mem=24G --job-name=IGE-E-g35 model/hpc_ige.sh full IGE_MODELS=E IGE_RUN=E_g35 IGE_STEPS=age,rehire,xacc IGE_START=$PE/estimates.json:E $G)
    sbatch --dependency=afterok:$j1 --time=01:15:00 --mem=24G --job-name=IGE-E6 model/hpc_ige.sh full IGE_MODELS=E IGE_RUN=E6 IGE_STEPS=age,rehire,xacc,gloss IGE_START=/mnt/parscratch/users/$USER/ige_smm_results/E_g35_j$j1/estimates.json:E,$PE/estimates.json:E $G

If `ufric` passes, add `ufric` to IGE_STEPS in (a) and (b). Judge E6 by `fix_seeds.py --with E6:E --without E_g35:E`
(IGE_MOMENTS=g35, IGE_STEPS=age,rehire,xacc,gloss).
