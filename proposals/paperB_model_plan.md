# Paper B structural model: plan (2026-10-18)

Model: `paperB_age_profile/model_document.tex` (design, analytical results, identification, estimation).
Code: `model/` (`core.py` solution + simulation + moment function; `build_data.py` PSID panel, data moments,
bootstrap, closed-form first steps; `estimate.py` SMM). Paper: Section 8 (model, identification, estimates,
counterfactuals).

## Step 1 - design (done)
- Annual career from the end of school to 55; risk-neutral sons; two job types (G, O) defined as in the paper's access
  table; one access logit for every offer; match component; displacement; human capital accumulation by job type and
  schooling with a race-specific pay-off of schooling; depreciation out of work; transitory shock; national unemployment
  shifts job finding and job loss.
- Parental income enters through schooling (data draw), access and the starting human capital level; race through the
  wage level, displacement, access, the pay-off of schooling in accumulation and (optionally) the entry return.

## Step 2 - analytical results (done; model document Section 9)
- Homogeneity: V = exp(mu_r + h) v(m, j). Decisions do not depend on h -> solve on the match grid only (2 s per
  evaluation for all 4,765 sons).
- Closed forms without simulation: accumulation by NLS on stayers' wage growth (Prop. 2); transitory variance =
  -autocovariance of annual stayer growth (Prop. 3); displacement logit (Prop. 4). Used as starting values and checks.
- Needs the model: access, match parameters, search frictions, initial conditions, depreciation, racial wage level
  (selected outcomes of offers and acceptance).
- Per the PI's rule, everything is estimated jointly in one SMM run per nested model.

## Step 3 - identification map (done; model document Sections 10-11, paper Table 'parameters and moments')
66 moments for 25 parameters (model D); each parameter's identifying moments listed; sensitivity (Jacobian) matrix at
the start reported (condition number, most collinear pairs).

## Step 4 - estimation (launched 2026-10-18)
- Diagonal SMM, cluster-bootstrap s.d. of each moment (500 draws of 1968 families), R = 5 simulated sons per PSID son,
  common random numbers, CMA-ES, nested models A -> B -> C -> D warm-started, 6 local workers (shared machine).
- Selection: a race parameter is kept if it lowers Q by more than 3.84.
- Standard errors: (1 + 1/R)(G'WG)^-1 with a numerical Jacobian.
- Counterfactuals on the selected model: equalising schooling; equal access by race; equal access by parental income;
  equal pay-off of schooling; equal displacement risk; depreciation halved.

## Step 5 - after the first estimates (next)
1. Inspect fit; if the cross-sectional variance and the stayer-growth variance conflict (Prop. 3), add a persistent
   (AR(1)) component or individual-specific growth rates only if the data require it.
2. Replace the calibrated cyclical elasticities (phi) with CPS-flow estimates; add the entry-conditions validation
   (paper Section 7) and the NLSY profiles.
3. Rank moments and the earnings IGE as validation; robustness with IPW-weighted moments.
4. Write the estimates, fit and counterfactuals into Section 8.
