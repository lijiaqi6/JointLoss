# Paper B: primary goal (set by the PI, 2026-10-20)

**What is passed on from parents to sons, and which policy each part points to.** The IGE bundles different things
transmitted through parental income; each has a different policy implication. Paper B's primary question is to separate
them.

**Framing - race or race-neutral - is open and will be decided by what we find** (PI, 2026-10-20). If the components
differ sharply by race (as the wage component does: the racial opening of the IGE with age sits in it), the paper can
lead with race; if the decomposition is the general result and race differences are one panel, it is race-neutral.
Every analysis is therefore run pooled and by race.

| What the father's earnings partly reflect | What would be passed on | Policy it points to |
|---|---|---|
| Hourly wage | human capital, skills, returns | schooling, training |
| Hours when employed | willingness or ability to supply work | tax and transfer incentives, childcare |
| Employment stability (no spells) | a stable childhood environment | unemployment insurance, income smoothing for families with children |
| Search friction faced by a group (place, network, discrimination) | constraints a subpopulation faces | job-search help, place-based policy, anti-discrimination |

Report the general finding first, then the racial difference; never dismiss a result because it is equal by race.

## Where the existing evidence sits

**1. Hourly wage (human capital).**
- Wage transmission dominates: the father's wage is 76-84% of the variance of his log earnings; wage-to-wage
  transmission 0.332*** White, 0.191*** Black, difference -0.141*** (p = 0.003) (`24.IGEDecomposition.py`, Section 7).
- The racial gap is absent at 25-34 and opens after 35, entirely in the wage component (24; Sections 4-6).
- Within jobs: same-employer growth rises with parental income for White sons (0.019***), not Black (0.007); the
  return to schooling rises faster with age for White men within the job (NLSY79 0.021** at equal AFQT).
- Structural model: the pay-off of parental income (H4) and of schooling (H2) in human capital accumulation; H4 carries
  three fifths of the gap at 45-49 and two fifths of its opening; equalising schooling closes less than a tenth.
- Father's schooling (fixed before any friction) gives the same pattern in ten-year wage growth (diff 0.021*, p = 0.051).

**2. Hours when employed (labor supply).**
- Hours-to-hours transmission 0.105*** White, 0.138*** Black (24); the hours IGE on parental income is larger for
  Black sons (0.072 vs 0.027) and works against the racial gap.
- Not yet separated from employment and instability on either side.

**3. Employment stability (childhood environment).**
- Friction-predicted parental income (18% of its variance) is transmitted more strongly than the rest: earnings 0.528
  vs 0.360, difference 0.168*** (p = 0.007); family income 0.287*** (`74.FrictionIGEPooled.py`) - contra Shea (2000).
- The father's instability shares carry three tenths of the racial opening among father-present sons (-0.061*,
  p = 0.094; young Black IGE -0.028**) (`72.FrictionGenerations.py`).
- Clean-year parental income changes nothing (-0.006, p = 0.69): spells do not distort the income measure.
- Parents' friction carries 19%** of the employment IGE (mother 12%**, father 7%*), separate channels.

**4. Search friction faced by a group.**
- Sons' job finding out of work: 0.44 Black vs 0.58 White (model step 5, dlu -0.539***): a wage-level channel, not
  persistence (counterfactual: Black wage +0.015***, IGE gap +0.004**).
- Son's job finding falls with parental income equally by race (PSID -0.022*** / -0.027***; NLSY79 -0.056*** / -0.061***).
- Son's own friction: 31% of the earnings IGE at 25-29 -> 9% at 45-49 (pooled), larger than schooling or occupation as a
  mediator at 25-29; NLSY79 replicates (23% -> 13%).
- Shared father-son friction: 2-6% of the IGE, no age opening (`73.SharedFriction.py`); state fixed effects move nothing.
- PSID-only: the gain at a move falls with parental income for Black sons (NLSY79 does not replicate).

## What is missing (next work)

1. **The 4 x 4 transmission table.** Parent side {log wage, hours when employed, instability (years unemployed /
   displaced; earnings volatility net of spells), group friction (state unemployment / labor-demand shocks in childhood,
   plant closures)} x son side {log wage, hours when employed, employment / instability, friction}, pooled and by race,
   by son's age band. Extends 24's 2 x 2 (wage, hours). The diagonal = like passes like; the off-diagonal (e.g., the
   father's instability lowering the son's wage at equal parental income = the environment channel) is where the policy
   answers are.
2. **Quasi-exogenous handles** for the policy rows: plant closures (instability the father did not choose;
   `psid_displacement.pkl`), state labor-demand shocks during childhood (`state_shocks.pkl`, `8a.StateShocks.py`), state
   UI generosity (`12b.UIGenerosity.py`: does insurance offset the stability channel?).
3. **The mother**, so father-absent sons (48% of Black, 13% of White) are in (74 has a first version).
4. **The structural model's role.** It explains component 1 (human capital accumulation) and the job-finding part of
   4. It has no hours choice and no childhood instability; decide whether the policy rows 2-3 are scored in the model
   (an extension) or reduced form (the paper's evidence sections) - parsimony rule.
5. **Literature check** (Fable): closest precedents for decomposing what the IGE transmits (wage vs hours vs stability),
   so the contribution is stated against them.

## Proposed outline after the reframing (to agree with the PI before rewriting)

1. Introduction: the question (what is passed on), the four components and their policies, the answer.
2. Data.
3. The decomposition of the IGE into the four components (new; the 4 x 4 table), pooled, by age, by race.
4. The age profile and the racial opening: it is in the wage component (current Sections 4-5).
5. Where the wage component is built: careers, jobs, schooling (current Sections 6, fathers' jobs).
6. Stability and friction: what they carry, with the quasi-exogenous handles (new; current 6c, the friction work).
7. The structural model of the wage component (current Section 8), with the friction steps.
8. Policy: what each component implies; what the model and the evidence can score.
9. Conclusion.
