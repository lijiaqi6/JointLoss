# Separation hazard: UI generosity (M2b) and her displacement (M3), PSID evidence (WP4, 2026-10-19)

Script `IGE/64.SeparationUIAndHerLoss.py` (imports `IGE/19` read only; nothing in `IGE/60-62` or `paperA_model/` was
touched or run). Tables in `IGE/output/separation_ui_her_loss.md` / `.csv`; the path by event year for WP3.2 is in
`IGE/output/bw_present_by_year.csv`. Options M2a / M2b / M3 as in `fable_marriage_divorce_paperA.md`, Section 5.

## Design

19's stacked event study (Cengiz et al. 2019): person x event-year units; treated = first displacement (closure or
layoff / firing) in ev; clean controls = not displaced up to ev+6; baseline (last observed of ev-1, ev-2) with a child
0-17 and positive own hours; person x stack and calendar year x stack FE; reference e = -2; s.e. clustered by 1968
family; p-values normal; *** p<0.01, ** p<0.05, * p<0.1. Sample = the Paper A target sample of IGE/60 (events
1984-2021, outcome years <= 2021). Check: this sample reproduces the target, Black mean of years 1-3 = -0.040*
(s.e. 0.023; p = 0.084) against `psid_es_bw_present_13_B` = -0.040.

- **M2b.** Outcome 'still with baseline wife'. UI generosity of the displacement year in the family's baseline state
  (IGE/12b: DOL statutory maximum weekly benefit and maximum weeks; ETA 5159 average benefit; BEA wages; public data),
  standardised over units (1 sd). Interaction model: displaced x e x z, with e x z for all families (so control families
  in generous state-years have their own path); z itself is absorbed by the unit FE. No region x year FE (they absorb the
  state-year variation). Four measures: max weekly benefit / state average weekly wage (sd 0.096), max weeks (sd 2.2),
  log real max potential benefit (sd 0.29), average benefit / average wage (sd 0.055). Plus a median split.
- **M3.** Roles reversed: wives of male heads, event = her first displacement (wife's own reason-for-job-end items,
  1984+ waves, plus her own reports as a female head if she has separated by the interview, so events are not
  conditioned on staying married); outcome 'still with baseline husband'; also her hours (first stage) and his hours.

**Caveat (both).** The marriage outcome equals 1 by construction at the baseline years, so the pre-period
coefficients are mechanical and there is no placebo test for this outcome (e = -3: -0.029*** for his displacement,
-0.022** for hers, because at e = -3 some couples were not yet married). Identification rests on the post-period
against clean controls with person FE. UI generosity is not randomly assigned across state-years.

## M2b: no detectable dependence on UI generosity

Displaced x z (1 sd more generous), mean of years 1-3, 'still with baseline wife' (positive = smaller fall):

| UI measure | All | Black | White |
|---|---:|---:|---:|
| Max WBA / avg weekly wage | 0.009 (0.011; p=0.382) | 0.006 (0.020; p=0.778) | 0.007 (0.013; p=0.593) |
| Max weeks | -0.005 (0.021; p=0.825) | -0.018 (0.027; p=0.514) | 0.004 (0.023; p=0.859) |
| Log max potential benefit | 0.006 (0.012; p=0.620) | 0.020 (0.023; p=0.378) | -0.002 (0.014; p=0.867) |
| Avg benefit / avg wage | 0.005 (0.011; p=0.640) | -0.012 (0.020; p=0.568) | 0.007 (0.013; p=0.589) |
| Displaced, at mean generosity | -0.036*** (0.011; p=0.002) | -0.039* (0.023; p=0.090) | -0.028** (0.012; p=0.025) |

N = 223,731 person-years, 1,366 displaced fathers (Black 526, White 840), 41,176 control stacks, 1,929 clusters.
None of the 12 interactions is significant in years 1-3; years 4-6 likewise (one of 12 at p < 0.1, White, log max
benefit, -0.031*, p = 0.074, the wrong sign). Events 1977-2021 (1,754 displaced fathers): log max benefit 0.005
(0.010; p = 0.637). Median split (log max benefit), years 1-3: below -0.036** (0.016; p = 0.025), above -0.034**
(0.016; p = 0.031), difference 0.002 (0.023; p = 0.926); Black below -0.064** (0.032; p = 0.050), above -0.015 (0.033;
p = 0.647), difference 0.049 (0.046; p = 0.290). Power: the pooled 95% interval for the cap interaction, [-0.013,
0.031] per sd, cannot exclude a mitigation as large as most of the -0.036 response, so this is "not detected", not
"zero". The Black point estimates lean in the Lindo-Regmi-Swensen direction, but none is significant.

**Implication.** Keep one sigma_J (no split by UI entitlement lh = 1 / 2). M2b is not supported by the PSID; the UI
counterfactual leaving separations unchanged stays a stated property of the model, with this footnote as the evidence.

## M3: her displacement moves separations as much as his does

'Still with baseline husband' after HER displacement (1,205 displaced wives: Black 442, White 763; 41,623 control
stacks; N = 236,761; treated mean at e = -2, -1: 0.986):

| | All | Black | White |
|---|---:|---:|---:|
| Mean years 1-3 | -0.046*** (0.012; p<0.001) | -0.048** (0.023; p=0.037) | -0.040*** (0.014; p=0.005) |
| Mean years 4-6 | -0.090*** (0.016; p<0.001) | -0.083*** (0.030; p=0.006) | -0.083*** (0.020; p<0.001) |
| e = +1 / +2 / +6 (All) | -0.014 (0.012; p=0.214) / -0.057*** (0.014; p<0.001) / -0.100*** (0.019; p<0.001) | | |
| His displacement, years 1-3 (same sample window) | -0.036*** (0.011; p=0.002) | -0.040* (0.023; p=0.084) | -0.027** (0.012; p=0.028) |
| His displacement, years 4-6 | -0.051*** (0.014; p<0.001) | -0.069** (0.027; p=0.010) | -0.033** (0.016; p=0.035) |

First stage: her hours -127*** (38; p < 0.001) in years 1-3 (Black -211***, White -85*), back to -36 (41; p = 0.379)
in years 4-6; his hours +61* (32; p = 0.061) in years 1-3. Closures only (376 events): -0.027 (0.021; p = 0.194) in
years 1-3, -0.044 (0.027; p = 0.107) in years 4-6, about 60% of the main response and not significant; part of the
layoff / firing response may be selection (women in failing marriages more often laid off or fired), which the
closure variant cannot rule in or out with 376 events.

**Implication.** M3 goes on the PI's list. Her displacement lowers 'still with baseline husband' by 4.6 points in
years 1-3 and 9.0 in years 4-6, at least as much as his displacement (3.6 and 5.1), with the same race pattern. As for
his displacement, the gap keeps widening after her hours have recovered (years 4-6), which argues for a hazard tied to
a lasting consequence of the displacement (M2a-type, his / her human capital level) rather than to the non-employment
spell alone. If M3 is adopted, it should key on her displacement (the entitled non-employment state after a job
loss), not on all her non-employment (most of her exits are quits and child-related).

## Footnote sentences for sec7 (marriage paragraph)

- M2b: "In the PSID the separation response to his displacement does not vary with the generosity of unemployment
  insurance in his state and year: a one-standard-deviation higher maximum weekly benefit relative to the state's
  average wage changes the fall in the probability of still being with the baseline wife in years 1-3 by 0.009
  (s.e. 0.011; p = 0.38; 1,366 displaced fathers), and the maximum duration, the maximum potential benefit and the
  average replacement rate give 0.006 or less in absolute value, none significant, by race either (IGE/64). We
  therefore keep one sigma_J."
- M3: "Her displacement, in the same design with the roles reversed, lowers the probability of still being with the
  baseline husband by 0.046*** (s.e. 0.012; p < 0.001; 1,205 displaced wives) in years 1-3 and by 0.090*** (0.016)
  in years 4-6, Black -0.048** and White -0.040***, at least as much as his displacement (-0.036***); closures alone
  give -0.027 (0.021; p = 0.19; 376 events). The model's hazard does not respond to her displacement (IGE/64)."
