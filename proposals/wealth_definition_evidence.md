# Wealth targets: a model problem or a definition problem? (WP4, 2026-10-20)

Script `IGE/77.WealthDefinitions.py`; tables `IGE/output/wealth_definitions.md` (+ `.csv`, `_diffs.csv`, `log77.txt`).
Same couples, waves (1984, 1989, 1994, 1999-2019) and earnings denominator as the targets `psid_liq_*` of `IGE/60`
(the script reproduces all six targets and their N exactly). Unweighted; s.e. from 200 block-bootstrap replications
over 1968 families; *** p<0.01. Model numbers: `results/marriage_diag_20261019_092447_p18108` (analytic start, wedge
on). Nothing in `IGE/60-62`, the targets or the model was changed.

## The numbers (all couples, 1984-2019; (b) is 1999-2019 only)

| wife's age | | share <= 0 | | | | | share > 1 yr of couple earnings | | | | |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| | | (a) liquid | (b) +IRA | (c') | (c) | (d) | (a) | (b) | (c') | (c) | (d) |
| 25-34 | data | **0.568** | 0.565 | 0.476 | 0.257 | 0.206 | **0.034** | 0.051 | 0.120 | 0.166 | 0.302 |
| | model | 0.476 | | | | | 0.022 | | | | |
| 35-44 | data | **0.462** | 0.436 | 0.354 | 0.175 | 0.122 | **0.077** | 0.137 | 0.243 | 0.301 | 0.513 |
| | model | 0.340 | | | | | 0.082 | | | | |
| 45-59 | data | **0.381** | 0.326 | 0.264 | 0.115 | 0.065 | **0.177** | 0.288 | 0.399 | 0.475 | 0.721 |
| | model | 0.086 | | | | | 0.389 | | | | |

(a) liquid as targeted (checking/savings + stocks - unsecured debt); (b) (a) + IRAs/annuities (1999-2019; on those
years (a) is 0.603 / 0.490 / 0.390 and 0.033 / 0.067 / 0.165); (c') net worth excluding home equity and vehicles
(financial + IRA + business + other real estate - non-mortgage debt); (c) PSID WEALTH1 (net worth excluding home
equity); (d) net worth. Employer pensions (DB and 401(k)) are in none of them, so (b)-(d) understate retirement saving.
Every difference from (a) is significant (e.g. 45-59: (c') - (a) = -0.117*** (0.004) for share <= 0 and +0.222***
(0.006) for share above earnings; (b) - (a) = -0.064*** (0.003) and +0.123*** (0.005)). Medians at 45-59 (2000 $):
3,000 (a), 8,226 (b, 1999+), 26,637 (c'), 47,859 (c), 127,620 (d); 86% own a home, 65% have a mortgage, 40% hold an
IRA/annuity (1999+).

By race the definitions move the two groups differently. At 45-59, Black couples: (a) 0.596 / 0.062, (c') 0.496 /
0.170, (c) 0.201 / 0.276; White couples: (a) 0.305 / 0.218, (c') 0.181 / 0.481, (c) 0.085 / 0.547. The Black - White
gap in share <= 0 is +0.291*** (0.017) under (a) and +0.314*** (0.018) under (c'); in the share above earnings it
doubles, from -0.156*** (0.010) to -0.312*** (0.015). IRAs barely move Black couples ((b) - (a) at 45-59: +0.040***
above earnings) and move White couples a lot (+0.153***).

## What this says

1. **The 'too rich at 45-59' misfit comes from the definition.** The model's share above a year of earnings
   (0.39) is the data's value once saving held outside checking and stocks is counted: 0.40 under (c'), 0.29 under (b)
   (a lower bound: no 401(k)), 0.48 under (c). The model's asset funds all retirement consumption beyond social
   security (terminal value: the asset is annuitised over 240 months on top of 40% of the mean wage), so it is
   compared with an object that excludes most retirement saving. Under (a) the model is penalised for saving the
   terminal value forces it to do.
2. **The missing mass at zero at 45-59 is a model problem.** Under any definition without vehicles or housing,
   a quarter to a third of couples reach 45-59 with no wealth ((b) 0.33, (c') 0.26; Black couples 0.50 under (c')).
   The model has 0.09. Only (c) (0.115, because of car values) or (d) (0.065) reach the model's level, and the model
   has neither cars nor houses. In the model every couple saves for retirement against the same flat 40% replacement
   rate. In the data many couples save nothing, which is what a replacement rate that is higher for low earners (the
   progressive benefit formula) would produce, with no new parameter (a fixed input from the SSA bend points). This is
   a candidate, not a test.
3. **The young bands are consistent with (c').** At 25-34 and 35-44 the model's shares at or below zero (0.476,
   0.340) equal (c') (0.476, 0.354) and lie below (a) (0.568, 0.462). So, on this diagnostic, the young misfit is
   too *few* couples at or below zero against the liquid target, not too many. The model's share above earnings
   when young (0.022, 0.082) is close to (a) (0.034, 0.077) and below (c') (0.120, 0.243).
4. **Which definition matches the model's asset.** The asset plays two roles: a buffer that can be borrowed against
   (a_bar from the P10 of *liquid* wealth, `IGE/62`) and the whole retirement saving (terminal value). The definition
   that fits both roles, exists in every target wave and leaves out what the model has no counterpart for (houses, cars)
   is (c'). (b) is the narrowest change, but it exists only from 1999 and misses 401(k) accounts.

## Recommendation (PI decision; after the chain, since `IGE/60` and `IGE/62` are frozen now)

- **Now (paper):** keep the liquid targets for the queued estimate and add a sec7 'Estimation' footnote with the
  numbers in point 1 and point 2: at 45-59 the share above a year of earnings is 0.18 liquid against 0.40 under (c'),
  and the share at or below zero is 0.38 against 0.26. `fit_table` then reads the 45-59 'above earnings' misfit as
  mostly a definition problem and the 'at or below zero' misfit as a model problem.
- **After the chain (recommended):** redefine all six wealth targets as (c'), net worth excluding home equity and
  vehicles, in `IGE/60`, and move a0 and a_bar in `IGE/62` to the same definition so that the initial condition, the
  borrowing limit and the targets refer to one object. Do not mix definitions across age bands. Rerun the baseline on
  the new moment set before comparing steps (one step at a time).
- **Keep the 45-59 share at or below zero as a target under any definition.** It is the informative misfit. The
  progressive replacement rate (point 2) is the first candidate if it stays.
