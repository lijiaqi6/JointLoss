# What moves an established wife off her job? Evidence for the exit-feature decision (WP2, 2026-10-20)

Script `IGE/75.EstablishedWifeExits.py`. Every estimate is in `output/established_wife_exits.csv`, with tables in
`output/established_wife_exits.md`. The script uses 63's sample and loaders, imported read only.

- **SIPP 2003-2016.** Married wives aged 25-59 whose husband is employed, employed in months t-1 and t, all four
  months observed. The outcome is the persistent exit: no job in any week of t+1 and t+2, for any reason, involuntary
  job ends included. "Established" means the main job has lasted 12 months or more at t.
- **PSID 1968-1996, annual years.** The exit is hours > 0 in year t and 0 in t+1. "Established" means the same wife
  also worked in t-1 and t-2. All available years are used; there is no balanced panel.

Regressions are LPMs in percentage points (pp), with s.e. clustered by household (SIPP) or by 1968 family (PSID).
SIPP regressions include panel x rotation x month FE and use the wife's weight. PSID regressions include calendar-year
FE. *** p<0.01, ** p<0.05, * p<0.1. These are associations, not causal effects.

## 1. The target and who is behind it

- The 12+ hazard is **0.676% a month** (N = 634,492 wife-months). This reproduces the target sipp_wexit_ten_12p
  (0.6755). The model gives 0.27%.
- Established wives are 82.9% of the wife-months with known tenure and 64.0% of the exits.
- In the PSID, established wives exit at 5.42% a year (N = 34,475), against 15.42% for the others. They account for
  46.7% of annual exits.

## 2. Decomposition of the 12+ hazard (SIPP)

The decomposition is done two ways. They answer different questions.

- **(a) Exclusive accounting.** Each exit is assigned to one cause, in a fixed priority order. This shows what the
  exits are.
- **(b) LPM accounting.** Each cause's contribution is b_k x mean(x_k) from the joint LPM. This is the hazard in
  excess of otherwise identical full-time wives with tenure of 36+ months.

| piece | (a) share of 12+ exits | (a) piece of the 0.676% | (b) LPM contribution, % of the hazard | return within 12 months (KM) | median spell |
|---|---|---|---|---|---|
| involuntary job end (stated: layoff, closure, fired, temporary job ended) | 25.2% (0.8) | 0.17 pp | not a covariate | 56.7% (2.0) | 10 months |
| birth window (child aged 0 at t+1..t+9) | 11.5% (0.6) | 0.08 pp | 7.5% (0.05 pp***) | 42.1% (2.8) | 19 months |
| own illness / injury or retirement (stated) | 6.1% (0.4) | 0.04 pp | work-limiting condition 6.3% (0.04 pp***) | 33.6% (4.0) | 35 months |
| usual hours < 20 | 9.3% (0.5) | 0.06 pp | 11.8% (< 20 h) + 8.8% (20-34 h) | 44.7% (3.5) | 16 months |
| his earnings rise > 25% or his job change | 8.4% (0.5) | 0.06 pp | rise 2.9%, fall 3.1%, job change 1.6% | 58.2% (4.1) | 10 months |
| tenure 12-35 vs 36+ | (inside the others) | | 15.1% (0.10 pp***) | 52.6% vs 52.7% | 11 vs 12 months |
| **residual** | **39.5% (0.9)** | **0.27 pp** | **43.3% (0.29 pp)** | **57.2% (1.5)** | **9 months** |
| all 12+ exits | 100% | 0.676 | | 52.7% (1.0) | 12 months |

Joint LPM (12+ wives, N = 634,451, 28,526 clusters, mean 0.676):

| covariate | coefficient |
|---|---|
| birth window | +0.75*** (0.11; p<0.001) |
| usual hours < 20 | +1.51*** (0.11; p<0.001) |
| usual hours 20-34 | +0.41*** (0.04; p<0.001) |
| work-limiting health condition | +1.37*** (0.12; p<0.001) |
| his job change in t-2..t+1 | +0.38*** (0.10; p<0.001) |
| his earnings rise > 25% | +0.24*** (0.05; p<0.001) |
| his earnings fall > 25% | +0.27*** (0.05; p<0.001) |
| tenure 12-35 months | +0.42*** (0.03; p<0.001) |
| age 55-59 | +0.01 (0.06; p=0.847) |
| Black husband | +0.15*** (0.05; p=0.003) |
| wife < high school | +0.33*** (0.09; p<0.001) |
| wife BA+ | -0.28*** (0.04; p<0.001) |

Without involuntary job ends, the hazard is 0.505%, the coefficients keep their size (birth +0.71***, hours < 20
+1.16***, health +1.11***), and the residual is 39.5% of that hazard.

**The residual exits.** They have no birth, no stated illness, no involuntary end, hours of 20 or more, and no
turbulence on his side. 48.6% of them have no job end recorded in t-1..t+2, against 28.8% of all 12+ exits. Where a
reason is stated, 28.5% are "unsatisfactory arrangements / other quit" and 12.3% are "childcare / family". These
exits are over-represented among wives on 20-34 hours (22.8% vs 14.5% of wife-months) and in years 1-3 of the job
(36.5% vs 24.0%). Their spells are short: 40.7% are back within 6 months, 57.2% within 12 and 67.0% within 24. The
median spell is 9 months.

**Return to work, LPM** (12+ exits observed 12 months later, N = 2,574; base = childcare / family). Relative to the
base, involuntary ends raise the 12-month return by +16.10pp*** (3.81; p<0.001), unsatisfactory / other quits by
+14.09pp*** (4.15; p<0.001), and quits to another job by +41.63pp*** (5.80; p<0.001). The birth window lowers it by
-9.64pp*** (3.62; p=0.008). Black husband: +8.08pp** (3.96; p=0.041).

**Repeat exits.** An earlier persistent exit in the panel raises the 12+ hazard by +0.83pp*** (0.11; p<0.001), with
all the controls above. This measure is left-censored at the panel start: 9.3% of 12+ exits are by wives with an
earlier exit, and 3.7% of wife-months have one.

## 3. PSID complement (established = worked in t-1 and t-2)

The sample is N = 34,475 wife-years, with 2,299 family clusters and a mean exit of 5.42%. Joint LPM:

| covariate | coefficient |
|---|---|
| birth in t+1 | +5.04*** (0.82; p<0.001) |
| birth in t | +6.38*** (0.92; p<0.001) |
| hours 1-499 in t | +20.28*** (0.86; p<0.001) |
| hours 500-999 in t | +10.45*** (0.59; p<0.001) |
| hours 1000-1749 in t | +2.86*** (0.25; p<0.001) |
| his labor income rise > 25% | +1.73*** (0.37; p<0.001) |
| his labor income fall > 25% | -0.07 (0.35; p=0.851) |
| Black head | +0.73** (0.31; p=0.017) |

- **LPM accounting.** Births in t or t+1 12.8%, hours < 1000 53.3%, hours 1000-1749 14.8%, his income rise 4.8%,
  residual 15.1%.
- **Return to work.** 40.9% (1.2) work again within 1 year, 57.3% within 2 and 72.3% within 4. After a birth the
  shares are 34.6% and 50.8%. Without a birth and with 1000+ hours in t, they are 47.5% and 63.4%.
- **Repeat exits.** An earlier exit of the same wife adds +3.49pp*** (0.36; p<0.001), and +1.49pp*** (0.36;
  p<0.001) once her hours are controlled (N = 33,363). 12.3% of established couples with an exit have two or more,
  and 23.2% of established exits are by wives with an earlier exit in the window.

## 4. Mapping to model features

| finding | feature it points to | cost | verdict |
|---|---|---|---|
| Involuntary job ends: 25% of 12+ exits, 0.17 pp of the 0.676%. The target counts every reason. | Her displacement hazard, followed by two months without work. **Already in the model.** | none | Check first at intake: split the simulated 12+ exit into her job loss vs voluntary. If her losses already give ~0.15-0.17 pp, the voluntary gap is ~0.25 pp, not 0.41. |
| Birth window: 7.5-11.5% of 12+ exits (0.05-0.08 pp), coefficient +0.75***; spells long (42% back within 12 months, median 19). PSID: births 12.8% of established exits. | **Birth-timed theta jump.** theta_ak is higher for k months after a birth, on the existing child chain. | no state; 1-2 parameters | Cheap; carries about 1/10 of the 12+ hazard. Not enough alone. |
| Residual: ~40% of 12+ exits (0.27-0.29 pp). Short spells (57% back within 12 months, median 9); over-represented on 20-34 hours and in years 1-3 of the job; no observable trigger. | **Transitory, persistent-for-months work-cost state.** A two-state Markov shock to the disutility of labor (enter / leave probabilities), mean duration ~9-12 months. | one binary state (x2 solve); 2 parameters, identified by the 12+ hazard and the 12-month return of exits (52.7%) | **The only candidate that produces the residual's short spells.** The iid taste shock reverses within a month and is removed by the persistence filter. The wives' stock entry rate (2.45% a month) is far below the recent leavers' return (~57% within a year), so leavers are close to work. |
| Repeat exits +0.83*** (SIPP), +1.49*** with hours (PSID). | Permanent work-cost type. | one state (x2 solve); 2 parameters | Weaker than the Markov state. A permanent type makes spells long, while the residual's are short. The Markov state also produces repeat exits. Keep as the fallback if the repeat-exit validation fails. |
| Low hours: < 20 h +1.51***, 20-34 h +0.41*** (11.8% + 8.8% of the hazard). | Part-time already in the model (phi_P). | none | Validation: the simulated exit of part-time wives vs full-time. No new feature. |
| Work-limiting health +1.37***, 6% of exits; very long spells (median 35 months). Age 55-59 has no excess hazard (+0.01, p=0.847). | Health / retirement state. | one state | Footnote only. These exits are near-permanent and few. |
| His earnings rise +0.24*** and fall +0.27***, nearly equal; job change +0.38***. In the PSID only the rise matters (+1.73***), fall -0.07 (p=0.851). | Monthly: joint turbulence (moves, schedules), not an income effect, which would have opposite signs. Annual: an income effect. | none | Nothing to add. The wealth/income channel carries the annual rise. |

## 5. Recommendation for the PI (one decision, after the first estimate)

1. **At intake, decompose the model's 12+ exit (0.27%) into her displacement vs voluntary.** No code change is needed;
   this is a simulation tabulation. The data's involuntary piece is 0.17 pp. If the model's displacement piece is of
   that size, the voluntary gap is about 0.25-0.30 pp. That gap equals the residual piece found here (0.27 pp).
2. **If the voluntary gap stays above about 0.1 pp, add the transitory Markov work-cost state.** Use one binary state
   on the disutility of labor, with two parameters (onset and recovery), and add the 12-month return of 12+ exits
   (52.7%, SIPP KM) as a new moment.
   - It is the one feature that matches both the residual's size and its short spells.
   - It also produces the repeat exits, which serve as validation (+0.83*** SIPP; 23% of PSID established exits by
     repeaters).
   - Let the birth-timed theta jump (no state) ride along. It covers about one exit in ten, with long spells.
3. **Do not add the permanent type first.** It lengthens spells, while the residual's are short. Health is a
   footnote.

Cost: the Markov state doubles the solve, the same cost as the type, so the choice between them is by fit, not
by cost. Parsimony: if step 1 shows the gap is mostly her displacement mis-timed or too rare, add nothing. Re-target
her displacement hazard instead (the SIPP base hazard is in 40/60).

## 6. Footnote-ready sentences (numbers from `IGE/75.EstablishedWifeExits.py`)

1. "Wives who have held their job for a year or more leave employment at 0.68% a month (SIPP 2003-2016, persistent
   exits; 64% of all exits). One quarter of these exits follow an involuntary job end. A child aged 0 around the exit
   accounts for 11%, own illness or retirement for 6%, usual hours below 20 for 9%, and a change in the husband's job
   or earnings for 8%. The remaining 40% have no observable trigger."
2. "The exits without a trigger are short: 57% of these wives work again within 12 months (Kaplan-Meier), and the
   median spell is 9 months. After a birth, 42% return within 12 months and the median is 19 months. After own
   illness or retirement, 34% return and the median is 35 months."
3. "In a joint LPM with panel-month fixed effects, a birth window raises the exit of established wives by 0.75pp***
   (s.e. 0.11, p<0.001), usual hours below 20 by 1.51pp*** (0.11), a work-limiting health condition by 1.37pp***
   (0.12), and both a rise and a fall of more than 25% in the husband's monthly earnings by 0.24pp*** (0.05) and
   0.27pp*** (0.05); age 55-59 has no excess (0.01, p=0.85)."
4. "In the PSID (1968-1996), wives who worked in each of the two previous years leave at 5.4% a year (15.4% for the
   others). A birth in the year or the next raises the exit by 5-6pp***, hours below 500 by 20pp***, and a rise in his
   labor income by 1.7pp*** (0.37); a fall does not (-0.07, p=0.85). 41% work again within a year."
5. "An earlier exit of the same wife raises the exit of established wives by 0.83pp*** (SIPP, s.e. 0.11) and by
   1.49pp*** (PSID, s.e. 0.36, conditional on hours)."

Proposed EVIDENCE rows (for WP9; not written here): 3.93 decomposition (sentences 1 and 3), 3.94 spell length
(sentence 2), 3.95 PSID and repeat exits (sentences 4 and 5).

## Caveats

- SIPP tenure is 63's measure: TSJDATE in 2004/08, the start year and month in 2014, otherwise the first month seen.
  Tenure is unknown for 10% of wife-months, which are dropped.
- The 4-month waves of 2004/08 heap transitions at the seam. Exits with "no job end recorded" show a 3-month return
  of 8.8% and a 6-month return of 39.3%, a seam pattern.
- "His earnings" is total person earnings (TPEARN). The window t+1, t+2 is compared with t-2, t-1.
- The residual is a remainder: it contains whatever the observables miss, including unmeasured child-care breakdowns.
- The PSID annual exit captures only spells that cover a whole calendar year.
