# Search friction and the IGE: can a friction in either generation make the Black profile flat? (Fable, 2026-10-19)

PI's question (verbatim): "search friction and IGE. search friction may suppress both son and father, and its racial
gap?" Read: `model/core.py`, `sec7_model.tex`, `EVIDENCE.md` 1, 8 and 11, `output/ige_decomposition.md` (3a, 3b, 4b),
`output/father_displacement.md`, `tab_job_moves.tex`, `model/output/final_x4/judge_ufric_E.md`,
`model/hpc_runs/E5_j11866020/estimates.json`, `67.LongDifferenceH4.py`, `42.SchoolingAndJobGrowth.py`,
`24.IGEDecomposition.py`. Nothing was run; every number below is from a saved output or the paper.

## 0. Short answer

1. **A search friction on the father's side cannot produce the profile.** Every father-side route either scales the
   Black IGE by a factor that is the same at every age of the son (classical noise in parental income; the reliability
   ratios are 0.650 White / 0.631 Black for the 12-17 mean, 0.585 / 0.565 for one year), or *raises* the Black IGE
   (inherited instability, the causal effect of the father's job loss on the son, compression of Black fathers'
   income relative to their skill, shared local labour markets). None lowers it, and none changes with the son's age.
   All of them together move the Black IGE by less than 0.01: the father's job loss inside the 13-19 window accounts
   for under 1% of the variance of parental income in either race.
2. **A search friction on the son's side, as the model has it (job finding out of work 0.44 Black / 0.58 White), raises
   the Black IGE, by 0.005**, not lowers it: removing it widens the gap by 0.004** (p = 0.036) at 30-34 and 0.005
   (p = 0.11) at 45-49. The friction hits sons of poorer parents more (job loss falls with parental income, delta_1 =
   -0.203***, p < 0.001, common to both races), so it adds persistence. Selection of who has a wage attenuates both
   IGEs by at most 0.03, equally by race: to flatten a profile that should rise by 0.3, the Black share of zero-hours
   years would have to fall by about 47 points per log point of parental income; it falls by 2.7 (-0.027***, s.e.
   0.009), the same as the White 2.2 (-0.022***, 0.006; difference p = 0.59).
3. **The one place where a search friction with a race x parental-income pattern exists in the data is the quality of
   the job found at a move, and the model does not contain it.** Among sons who change employers without a
   displacement, the wage gain falls with parental income for Black sons (-0.064***, s.e. 0.023, per log point at
   25-34) and not for White sons (0.005, 0.017; difference 0.069**, 0.028). On all pairs the move margin contributes
   0.009** (0.004) a year at 25-34 and 0.006** (0.003) at 35-55 to the racial difference in the growth gradient, the
   same-employer margin 0.012* (0.007) and 0.003 (0.004). Cumulated over 25-49 (10 + 15 years) the move margin is
   0.18 and the same-employer margin 0.165 of a cumulated racial difference of 0.345. Move and job-loss rates and their
   parental-income gradients are equal by race (move 0.125 / 0.130; displacement slope -0.037*** / -0.038***), so the
   racial search-margin difference is in what a move pays sons of richer Black parents, not in how often they move or
   lose a job. The model fits the same-employer half (H4: gamma_x(W) 0.0186***, s.e. 0.0072; gamma_x(B) - gamma_x(W)
   -0.0194***, 0.0054) and loads the other half on race-neutral channels (schooling, access, job loss), because it has
   no race x parental-income parameter at the move margin and the race-specific slope of the gain at a move is not a
   target. This is the test the PI's question calls for (Section 5, T1 and T6).
4. **Verdict on H4 unchanged; framing changes in one place.** H4 is identified by the within-employer gradient and the
   age profile, which no father-side friction can mimic. What should change: Section 8 should answer the PI's question
   in one paragraph with the numbers in (1)-(2), and "What the model leaves open" should say that the second half of
   the reduced-form opening sits at the move margin with a race x parental-income pattern the model does not
   reproduce, and name the step (Section 4).

## 1. Bookkeeping

Son's log wage at age a: y_a = beta_a x* - f_S(a) + v, parental income x = x* - f_F, with x* the part of parental
income the son's wage tracks, f_F the father's friction-induced shortfall inside the 13-19 window, f_S(a) the son's
own loss from spells out of work by age a (with d_u = 0 it is foregone accumulation, so it grows with a). Then

  IGE_a = Cov(y_a, x) / Var(x)
        = [beta_a Var(x*) + Cov(f_S(a), f_F) - beta_a Cov(x*, f_F) - Cov(f_S(a), x*)] / [Var(x*) + Var(f_F) - 2 Cov(x*, f_F)].

The parent's identity is the case Cov(x*, f_F) = Cov(f_S, x*) = 0. The two extra terms matter for the mechanisms below:
Cov(x*, f_F) is "the friction hits high-x* Black fathers too" (compression), Cov(f_S(a), x*) is "the son's spells
depend on his background" (the model's delta_1). The age profile is the profile of the numerator; the denominator is
fixed. So a father-side term can only scale all ages by one factor, and a son-side term can shape the profile only
through Cov(f_S(a), x*) or through who is observed with a wage.

## 2. Mechanisms, signs and whether each can make the Black profile flat while the White rises

### Son side

**S1. A race-specific level of the search friction out of work (step 5, in the model).** lambda_u = 0.58 White,
0.44 Black (Delta ell_u = -0.539***, s.e. 0.095, p < 0.001). With accumulation only while employed, each year out of
work costs Delta_j(a); Black sons lose about 0.11 x 27 = 3 career years to 45-49, White sons about 1. That is a
*level* (the model's racial wage gap widens from 0.426 at 35-39 to 0.472 at 45-49, as in the PSID 0.425 / 0.418).
For the IGE what matters is Cov(f_S, x*): spells are more frequent for sons of poorer parents (delta_1 = -0.203***),
so the friction adds persistence, and more for Black sons because their spells are longer. Counterfactual dlu = 0:
Black wage at 25-34 +0.015*** (0.003), more for the bottom tercile (+0.038*** at 45-49) than the top (+0.030***);
the IGE gap widens by 0.004** (p = 0.036) at 30-34 and 0.005 (p = 0.11) at 45-49. Sign: raises the Black IGE.
Cannot flatten it.

**S2. A parental-income gradient of the friction that differs by race.** If richer parents bought faster job finding
for White sons only, Cov(f_S(a), x*) would differ by race and grow with age. The data reject it: zero-hours years on
log parental income, White -0.022*** (0.006), Black -0.027*** (0.009), difference -0.006 (0.011, p = 0.59); at equal
schooling -0.006 and -0.009, difference -0.003 (p = 0.76). The displacement slope is also common (-0.037*** /
-0.038***). Not worth a model parameter (parsimony); if anything the Black gradient is steeper, which again raises
the Black IGE.

**S3. The cost of a spell interacts with H4.** For White sons Delta rises with x (gamma_x(W) = 0.0186***), so a year
out of work costs a son of richer parents more; a friction therefore *compresses* the White IGE. It is in the model
already (common lambda_u before step 5), it is race-neutral in parameters, and its size is tiny (White zero-hours
share 0.039 x 0.0186 x 27 years = 0.02 of IGE at 45-49). Sign: lowers the White profile. Wrong direction.

**S4. Selection of who has a wage.** The IGE is estimated on sons with a wage; Black sons have 0.109 of their years
without hours, White 0.039. If the sons without a wage are low-h sons of poorer parents, the observed Black IGE is
attenuated, and could be attenuated more with age if non-employment concentrates. Two facts bound it. (a) A
Heckman-type slope correction is rho sigma_u lambda'(c) c'(x), with c'(x) = (dP/dx)/phi(c). With the measured
gradients (-0.027 Black, -0.022 White) and employment shares (0.891, 0.961) the factor is -0.043 for Black and
-0.042 for White: at most 0.03 of IGE (rho sigma_u <= 0.7), equal by race. (b) To remove a rise of 0.3 the Black
gradient of non-employment would have to be about 0.47 per log point, seventeen times the measured 0.027. (c) The
model has no selection on h at all (decisions do not depend on h; homogeneity), so the data's selection is absorbed
by the data moments, not reproduced; (a)-(b) say it is second order. (d) Attrition from the panel is selective for
White sons, not Black (P(observed at 45-49) on log parental income 0.139*** White, 0.005 Black), and IPW for staying
moves the opening from 0.143** to 0.129** (EVIDENCE 1.32). Sons who are not heads (living with parents,
institutionalised) have no wage record at all; this is the one selection the data cannot bound, and it is largest at
25-29, where it would *lower* the young Black IGE and so make the profile rise, not stay flat. Sign: attenuates both,
equally; cannot produce the shape.

**S5. A race-specific on-the-job search friction.** Move rates without displacement are 0.125 (Black) and 0.130
(White) at 25-34, 0.090 / 0.091 at 35-55; the model's common lambda_e(a) fits them. No room.

**S6. The quality of the job found at a move, by race x parental income (not in the model).** Table jobmoves:
growth if moved, per log point of parental income, 25-34: Black -0.064*** (0.023), White 0.005 (0.017), difference
0.069** (0.028); 35-55: Black -0.013 (0.020), White 0.046*** (0.017), difference 0.059** (0.026). Contribution of
moves to the all-pairs gradient: Black -0.008** (0.003) vs White 0.001 (0.002) at 25-34, difference 0.009** (0.004);
at 35-55 -0.002 vs 0.004**, difference 0.006** (0.003). Same-employer contribution difference 0.012* (0.007) at
25-34, 0.003 (0.004) at 35-55. Displaced: 0.000 at both. Cumulated 25-49: moves 0.18, same employer 0.165, of a
total 0.345 (the PSID opening in the model's sample is 0.274 from 25-29 to 45-49; the cumulation is an upper bound:
all-pairs gradients, raw, age quartic and year FE, no schooling control). This is a growth-rate difference tied to
parental income by race, cumulating over the career, with the right sign and half the size of the opening: it **can**
make the Black profile flat while the White rises. Two readings, same reduced form: (i) worse outside offers for
sons of richer Black parents (a search friction in offer quality); (ii) an entry premium that sits in the match
component for Black sons (H3: b_1(B) - b_1(W) = 0.034**, p = 0.012, schooling "a wage level" for Black sons) and
is lost when the job ends, against a premium in portable human capital for White sons. The two are separated by
where the gradient sits, in the destination wage (i) or the origin wage (ii); T1 does that. In model E5 the offered
match is independent of x and r, the entry level of parental income and schooling is in h (portable), and the
race-specific slope of the gain at a move is not a target, so the model cannot do either and fits the IGE profile
with H4 (within employer, 0.166 of the 0.281 gap at 45-49) plus race-neutral channels (0.115). The paper already
says the model fails this fact ("Why a job side", fourth fact); it does not yet say that the fact is half the
reduced-form opening.

**S7. Outside offers used inside the firm.** Same-employer growth can itself be a search outcome (counter-offers).
Then "the pay-off of parental income in accumulation" for White sons could be the pay-off of parental networks in
outside offers that raise the wage without a move. Public data do not observe offers; the NLSY79 check found jobs
found through friends or relatives grow *more slowly* (-0.014***, s.e. 0.004) and carry 0.001** of the gradient
(Section 8). Not separable from accumulation in the PSID; parsimony says do not add a parameter. One cheap
diagnostic exists (T7, low value).

### Father side

**F1. The father's friction as classical noise in x.** Attenuation by the reliability ratio, the same at every son's
age; ratios equal by race (12-17 mean 0.650 / 0.631; one year 0.585 / 0.565; father's one-year earnings 0.519 /
0.551, EVIDENCE 8.13). Cannot produce the shape, and cannot lower the Black level by more than the 3% ratio
difference. Caveat the parent should state: a persistent friction (a spell that covers most of the window) is not
averaged out by the 13-19 mean and is not fully captured by a lag-correlation reliability ratio; but its variance is
bounded by F2.

**F2. A persistent father-side friction that hits high-skill Black fathers (compression; the parent's "open" point).**
Write x = c x* + u with c_B < c_W (Black fathers' income understates the dispersion of their skill). The slope of y
on x is beta c Var(x*) / (c^2 Var(x*) + Var(u)); its derivative in c is proportional to Var(u) - c^2 Var(x*), negative
whenever the reliability ratio exceeds 0.5. With ratios of 0.63-0.65, *compression raises the measured slope*; and if
the son's wage tracks realised resources rather than x*, the slope is beta regardless. So "Black fathers' income is a
worse signal of their skill" cannot lower the Black IGE, through any age. The father's schooling test (T3) remains
useful as a test of whether Black sons' accumulation tracks *any* parental skill measure; the prior is the level
result of `24` 4b: father's years of schooling given father's earnings and the son's schooling, Black -0.005
(0.008, p = 0.54), White 0.004 (0.006, p = 0.47). Size of the friction in the window: fathers displaced 8.0% a year
Black, 4.8% White; family income -17% (Black) / -24% (White) for three years after; the 7-year mean falls by about
0.1 for a father displaced inside it; 44% / 29% of fathers are hit in a 7-year window; Var(f_F) = p(1-p) 0.1^2 is
about 0.0025 / 0.0020 against Var(x) of about 0.45: under 1% of the variance of parental income in either race, and
already inside the measured reliability ratios.

**F3. Inherited friction, Cov(f_S, f_F) > 0.** Persistence of instability across generations (son's share on
father's share in the childhood window): displaced or unemployed 0.075** (0.036) Black, 0.127*** (0.024) White;
unemployment 0.103*** / 0.114***; zero hours 0.192** (0.097) Black, -0.021 (0.039) White. Sign: raises the IGE, and
more with age as f_S(a) cumulates; the parent is right. Size: Cov(f_S, f_F) / Var(x) with Var(f_F) under 0.003 and a
persistence of 0.1-0.2 is below 0.005. Cannot.

**F4. The father's displacement acts on the son directly.** Father displaced at the son's ages 12-17: son's lifetime
earnings -0.189* (0.101, p = 0.062) Black, -0.137** (0.062, p = 0.026) White; schooling -0.317*** / -0.324***.
Enters y and x with the same sign: raises the IGE by c Var(D) / Var(x), about 0.19 x 0.1 x 0.15 x 0.85 / 0.45 = 0.005,
equal by race within noise, and the schooling part is already in e. Cannot.

**F5. The father's career stage at measurement.** Black fathers are younger when the son is 13-19; current income
then understates lifetime dispersion (Haider-Solon lambda < 1). That is compression (F2): raises the slope; and
`24` controls the father's age at 16. Cannot.

**F6. Half of Black sons have no resident father.** Father present at 16: 52% Black, 87% White (EVIDENCE 8.10). For
48% of Black sons the "father's friction" is not in x at all; x is the mother's family income plus transfers. A
father-side story has to work on the father-present half, where the Black IGE is *higher* (0.363 vs 0.267 all).
Replacing family income by parents' labour income weakens the family-income profile (EVIDENCE 1.31), which points to
transfers in x for Black families, not to the father's search friction.

**F7. Shared local labour markets.** A common regional component in x and y raises the IGE of the race with more
regional dispersion; it shapes the profile only if regional effects cumulate over the son's career. Sign: raises.
Cheap to test with state-at-16 fixed effects (T5); the prior is that both profiles survive.

### Summary table

| Mechanism | Side | Sign on Black IGE | Changes with son's age? | Can give flat Black / rising White? | Size | In model E5? |
|---|---|---|---|---|---|---|
| S1 level friction out of work | son | + | yes (cumulates) | no (wrong sign) | 0.005 | yes (step 5) |
| S2 race x x gradient of friction | son | + if any | yes | no (data: equal gradients, p = 0.59 / 0.76) | 0 | no, not needed |
| S3 cost of spell x H4 | son | - on White | yes | no (flattens White) | 0.02 | yes |
| S4 selection into wages | son | - both | only if gradient steepens | no (needs 0.47 vs 0.027 measured) | <= 0.03 | no (no selection on h) |
| S5 on-the-job friction by race | son | - | yes | no (move rates equal) | 0 | no, not needed |
| S6 job quality at a move, race x x | son | - | yes (cumulates) | **yes** | 0.18 cumulated raw | **no** |
| S7 counter-offers within firm | son | (is H4) | yes | not separable | - | as H4 |
| F1 classical noise | father | x RR | no | no | 3% ratio difference | n/a |
| F2 compression / persistent | father | + | no | no | < 0.01 | n/a |
| F3 inherited friction | father | + | yes | no (wrong sign) | < 0.005 | n/a |
| F4 father's loss acts on son | father | + | no | no | 0.005 | via e |
| F5 father's career stage | father | + | no | no | - | n/a |
| F7 local labour markets | both | + | weakly | no (unless cumulating) | untested | no |

## 3. Where the parent's answer is wrong or incomplete

- (1)-(3) are right. Point (3) should add the compression algebra: the "open" father-side case (Black fathers'
  income a worse signal of their skill) *raises* the measured Black slope whenever the reliability ratio exceeds 0.5,
  so it is closed by the ratios already in the paper, not left open; the father's-schooling test is still worth
  running, but as a test of whether Black sons' accumulation tracks any parental skill measure (prior: null at the
  level, `24` 4b).
- The identity omits Cov(f_S, x*) and Cov(x*, f_F); the first is the model's delta_1 channel (S1, raises) and the
  second is compression (F2, raises).
- It misses the son-side selection into wages (S4) and the bound that closes it (0.47 needed vs 0.027 measured).
- It misses the one search-margin fact with a race x parental-income pattern, the gain at a move (S6), which is half
  of the reduced-form opening and outside the model. That is the substantive answer to "search friction and its
  racial gap": not the father, not job finding, but what a move pays a son of richer Black parents.
- It misses that for 48% of Black sons there is no resident father in x (F6).
- It omits the cost-of-a-spell x H4 interaction (S3, tiny, wrong direction) and the direct effect of the father's
  job loss on the son (F4, raises, 0.005).

## 4. Does it change the verdict? What to write

**Verdict (H4): no.** H4 is identified from the within-employer gradient and the age profile (77% of its
sensitivity from the IGE moments); no father-side friction can produce an age-varying attenuation, and the son-side
friction the model has raises the Black IGE. The counterfactual shares (three fifths of the gap at 45-49, two fifths
of the opening) stand.

**Framing: two changes.**

(a) One paragraph in Section 8, after "Job finding out of work" (or at the end of Counterfactuals, where the dlu = 0
sentence already is), answering the PI's question. Draft:

> *Could a search friction, in either generation, produce the profile?* Not in the father's generation. The father's
> job loss inside the 13-19 window (8.0% a year for Black fathers, 4.8% for White; family income 17-24% lower for
> three years after) accounts for under 1% of the variance of parental income in either race and is inside the
> measured reliability ratios (0.650 White, 0.631 Black for a multi-year mean), which scale an IGE by the same factor
> at every age of the son; instability that passes from father to son (0.103*** and 0.114***, s.e. 0.038 and 0.027,
> for unemployment) raises the Black IGE rather than lowers it; and for the 48% of Black sons without a resident
> father at 16 the father's career is not in parental income at all. Not in the son's generation either, as the
> model has it: job finding out of work is slower for Black sons but does not vary with parental income at equal
> schooling (zero-hours years on log parental income -0.006 Black, -0.009 White, difference p = 0.76), so removing
> the racial difference widens the gap by 0.005 rather than closing it, and selection of who has a wage attenuates
> both profiles by at most 0.03 (the Black gradient of non-employment would have to be seventeen times its measured
> -0.027*** to flatten a rise of 0.3). The search margin on which Black and White sons of richer parents differ is
> the job found at a move (Table jobmoves): the gain falls with parental income for Black sons (-0.064***, s.e.
> 0.023, at 25-34) and not for White sons (0.005), a difference of 0.069** that contributes 0.009** a year at 25-34
> and 0.006** at 35-55 to the racial difference in the growth gradient, against 0.012* and 0.003 with the same
> employer. The model fits the same-employer part and not this one (Section 8.x).

Footnote to carry: the F2 compression argument in one sentence ("a persistent shortfall that hits high-skill Black
fathers compresses parental income; with reliability above one half, compression raises the measured slope"), the
`24` 4b father's-schooling null (Black -0.005, s.e. 0.008, p = 0.54; White 0.004, 0.006, p = 0.47), and the scripts
(`IGE/24.IGEDecomposition.py`, `IGE/19.FatherDisplacement.py`, `IGE/42.SchoolingAndJobGrowth.py`,
`model/postestimation.py`).

(b) In "What the model leaves open": replace the sentence on the Black gain at a move (+3.5) with the fact that the
race x parental-income slope of the gain at a move is not a target and is half of the reduced-form opening, and name
the step (Section 5, T6). Keep the sentence that the step is estimated jointly, never hand-tuned.

Terminology: "search friction", "job finding"; "human capital accumulation"; stars and p-values on every number.

## 5. Tests, ranked by value

All PSID tests use the model's son panel (`model/output/data_panel.pkl`, 4,765 sons, 46,540 son-years) or `24`'s
frame, clustered by 1968 family; every estimate with stars and p-value; nulls go in the text. Local = under one hour
on the laptop; HPC = Stanage, one step at a time, estimated jointly.

**T1 (local, 45 min; highest value). Anatomy of the gain at a move by race x parental income.** Extend
`42.SchoolingAndJobGrowth.py` section C (movers without displacement, consecutive pairs 1-2 years apart, 1985-2023).
Statistics, by race and band (25-34, 35-55), per log point of parental income: (i) the gain, raw and at equal
schooling (the table is raw); (ii) the origin wage residual (the son's wage in the pair's first year minus his own
career mean) and (iii) the destination wage residual, each on x; (iv) the gain split by origin tenure (< 3 years vs
longer) and by origin job type (G / O). Predictions. Offer-quality friction (S6-i): the destination gradient is
lower for Black sons, the origin gradient equal by race, at all tenures. Entry premium lost (S6-ii): the origin
gradient is higher for Black sons (richer Black sons paid above their own mean in the origin job), the destination
gradient equal, concentrated at short tenure and in the first job. Paper's current story (H4 within employer only):
the -0.064*** does not survive schooling and both origin and destination gradients are equal by race. The result
decides the parameterisation of T6.

**T2 (local, 30 min). Selection into wages by age.** Extend `26.IGEByAge.py` (or `24`): (a) zero-hours share and its
gradient in log parental income by band (25-29 ... 50-55) and race, with the race difference and its trend in age;
(b) the IGE profile with a wage imputed for zero-hours years at the son's last observed wage and, as a bound, at the
race-band 10th percentile. Predictions. Selection (S4): the Black gradient steepens with age and the imputed Black
profile rises. Paper's story: gradients flat in age and equal by race (-0.027 / -0.022 pooled), imputed profiles
within 0.03 of the observed (the level check in `24` gave -0.038, s.e. 0.044, on the gap). Closes S4 with numbers.

**T3 (local, 30 min). Father's schooling as the background measure, by age band.** Extend `24.IGEDecomposition.py`
(f_educ exists; father-present sons): son's log wage by band on x and the father's years of schooling (and the
mother's), by race, with and without the son's schooling. Predictions. "x is a worse signal of Black fathers' skill"
(F2 as a skill channel): the father-schooling gradient rises with the son's age for Black sons while the x profile
stays flat. Paper's story: father's schooling adds nothing at any age for either race (level prior: Black -0.005,
p = 0.54; White 0.004, p = 0.47). Note in the write-up that even a positive result would mean Black sons'
accumulation tracks parental skill through a channel x misses, which raises the Black IGE on a better measure; it
cannot explain the flat profile on x.

**T4 (local, 30 min). The father's friction inside the window.** Extend `24` (f_sh_zero, f_sh_disp, f_sh_unemp over
the childhood window exist; `psid_displacement.pkl` dates the father's displacements): (a) the IGE by band and race
with the father's spell shares as controls and interacted with x; (b) the IGE on x_clean, the 13-19 mean excluding
the father's spell years (zero hours or displacement year), same sons. Predictions. Father-side friction: the Black
profile steepens on x_clean by more than the White. Algebra of F1-F2: both move by at most the ratio of reliability
ratios (3%), the Black by less if the Black spells are more persistent. Low cost; it is the direct answer to the
PI's "suppress the father".

**T5 (local, 1 h; needs the state variable built in `8a.StateShocks.py`). Shared local labour markets.** IGE by band
and race with state-at-16 fixed effects, and with state x band. Predictions. F7: both profiles flatten by the
regional share, the Black more if Black families are more regionally concentrated. Paper's story: unchanged. A
referee will ask.

**T6 (HPC, one estimation + the ten-seed judge, overnight). Model step: race x parental income at the move margin.**
Rule compliance: a new target is needed (the race-specific slope of the gain at a move, gmv_x_B and gmv_x_W in place
of the pooled gmv_x, two moments for one; from `core.moments` and `build_data.py`, bootstrap s.e. from the same 500
family draws), so first re-estimate E5 on the new moment set (baseline), then the step, judged by the fall in Q at
ten seeds against that baseline (`judge_step.py`). Parameterisation chosen by T1, one parameter:
  (a) offer quality: the mean of the offered match carries kappa_x(B) (x - xbar) for Black sons (White 0, as the
      pooled slope is already fitted), `mo = ... + kappa_x * bl * xc`, in the simulation and in `solve` (the offer
      distribution per type);
  (b) entry premium in the match: `b_x` and `b_1(r)` split between h_0 and m_0 by one race-specific share s(B):
      m_0 += s (b_x xc + b_1(B) ec), h_0 -= the same (White s = 0).
Predictions. If the step takes over part of the IGE opening, gamma_x(B) - gamma_x(W) shrinks toward zero and the H4
share of the gap at 45-49 falls below three fifths; the counterfactual "equal job quality at a move" then closes part
of the gap and is a search-friction policy channel (hiring, referrals), which the current counterfactual table does
not have. If the step fits the move slope without moving dgx (the two facts are separate), H4 stands at three
fifths and the move margin is the "race-neutral" two fifths relabelled. Either way the paper gains the answer to the
PI's question in a model number. Job name `IGE-E6-move-<a|b>`; `--mail-type=BEGIN,END,FAIL`; 32 cores.

**T7 (local, 20 min; low value). Counter-offers inside the firm.** White same-employer growth gradient in x
interacted with the national unemployment rate of the year (`27`/`36`): counter-offers are procyclical, accumulation
is not. Prediction under S7: the gradient is larger in tight years. Diagnostic only; parsimony says no parameter.

**T8 (local, 1 h; medium value). Replicate S6 in the NLSY79.** `36.SameEmployerGrowthChecks.py` has employer-change
flags; the gain at a move on parental income (1979-81 mean, raw, since one-year parental income absorbs the schooling
part) by race. Prediction: Black movers' gain gradient below White's, as in the PSID (-0.064*** vs 0.005). If it
replicates, S6 is a fact of both data sets, which H4-net-of-schooling is not (EVIDENCE 11.15).

Not proposed, and why: a race x parental-income term in job finding out of work (S2) is rejected in the reduced form
(p = 0.76); a race-specific on-the-job friction (S5) by equal move rates; a father-side parameter of any kind by
F1-F5 (the father's income is data in the model, and the algebra says no father-side friction can produce an
age-varying attenuation). Parsimony: drop what the data cannot separate.

## 6. Numbers used (source)

- lambda_u: logistic(0.3099) = 0.577 White, logistic(0.3099 - 0.5389) = 0.443 Black; dlu -0.5389*** (0.0946);
  gamma_x(W) 0.0186*** (0.0072), dgx -0.0194*** (0.0054); delta_1 -0.2033*** (0.0554); rho = exp(-2.396) = 0.091
  (`model/hpc_runs/E5_j11866020/estimates.json`).
- Step 5 and counterfactual dlu = 0 (`judge_ufric_E.md`, EVIDENCE 11.20-11.21).
- Zero-hours gradient by race, levels 0.109 / 0.039 (parent's check; `data_moments.json` zero_B 0.110, zero_W 0.039).
- Reliability ratios (EVIDENCE 1.38, 1.42, 8.13; Section 8 footnote).
- Fathers' displacement 8.0% / 4.8%, family income -4,832*** of 38,685 (Black), -11,179*** of 57,085 (White) at
  +1..+3; children's outcomes (`output/father_displacement.md` 1, 2a, 3b).
- Instability levels and persistence; father's schooling (`output/ige_decomposition.md` 3a, 3b, 4b).
- Gain at a move by race x parental income (`tab_job_moves.tex`, `42.SchoolingAndJobGrowth.py` section C).
- Father present at 16, IGE by presence (EVIDENCE 8.10); labour-income parental measure (1.31); attrition (1.32).
