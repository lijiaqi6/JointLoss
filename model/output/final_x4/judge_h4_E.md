# Step test_h4: C:/Users/cm1jil/AppData/Local/Temp/claude/g--My-Drive-Selection-vs-risk/70aba53a-ec10-4a94-80fa-80eb71407d87/scratchpad/runs/IGE/model/hpc_runs/Lx4_E_j11861512:E against C:/Users/cm1jil/AppData/Local/Temp/claude/g--My-Drive-Selection-vs-risk/70aba53a-ec10-4a94-80fa-80eb71407d87/scratchpad/runs/IGE/model/hpc_runs/ige_full_20261018_224720_j11861516:E

Drop in Q over ten seeds: mean 36.1 (s.d. 3.5; min 29.1); passes 3.84 at every seed: True. Verdict: **kept**.

New parameters: dgx -0.0198 (0.0055), p = 0.000

| block | Q without | Q with |
|---|---|---|
| IGE | 34.5 | 4.7 |
| returns | 14.4 | 8.5 |
| levels and variances | 20.0 | 20.6 |
| G shares | 9.7 | 8.5 |
| stayer growth | 28.3 | 27.3 |
| moves and displacement | 30.2 | 33.1 |
| zero hours | 26.6 | 25.0 |

Moments whose |t| changes by more than 1 (t without -> t with): ige_2529_B +1.6 -> -0.4; ige_4044_B +2.0 -> +0.7; ige_4549_B +1.9 -> +0.9; ige_3034_W -2.5 -> -0.5; ige_3539_W -1.9 -> +0.2; ige_4044_W -2.3 -> -0.2; ige_4549_W -1.9 -> -0.2

Race parameters (without -> with): a3 0.0000 -> 0.0000; dg1 -0.0111 -> -0.0085; db1 0.0340 -> 0.0369; dgx 0.0000 -> -0.0198
Gaps (without -> with): gap_3034 0.074 -> 0.164; gap_4549 0.153 -> 0.282
