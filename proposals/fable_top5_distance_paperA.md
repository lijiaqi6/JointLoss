# Fable: how far from a top-5 submission, on substance (2026-10-20)

Asked by the PI: results, identification, the model and its estimates, counterfactuals; not writing or formatting.
Fable read the paper, the model code, the run notes and the two HPC results (recovery 11865966, LM polish 11865967),
and recomputed the fit at the LM estimate moment by moment. Claims below are Fable's; items marked [check] were not
yet verified in the code by the main session.

## 1. Verdict

Not a top-5 submission on substance: two major deliverables short; 6-9 months to a complete draft, 9-12 to
submission quality, and then about a one-in-five chance at a top-5. Today: a strong field-journal empirical paper
(AEJ: Applied, JOLE, JPubE; the CPS fact alone fits AER: Insights). With a credible estimate and the policy
counterfactuals: REStud / AEJ: Macro / JEEA. Missing: (a) an estimate whose fit is credible on the insurance blocks
(consumption, wealth, scarring, separation); (b) the welfare and policy counterfactuals, of which the central one
(EITC against an unconditional transfer) is not coded and rests on an EITC that is mis-timed in the model.

## 2. The headline fact

New and well established (four data sets, monthly timing, state x month x industry FE, 944 same-month joint events,
shared-workplace channel, leads/lags shape, equal by race); the novelty table in sec2 is right; against Bacher et al.
a clean complement, and the age table (joint loss flat in age, added-worker effect declining) is the best
positioning result. Magnitude is the problem: $260 a year, 2% of the family loss, 0.3% of BPS couple-years; the
joint loss offsets two thirds of a gross response of 47 hours. Not fatal if the paper becomes about the state and the
group where it bites (joint-loss couples on SNAP 19% vs 5.9% before; 9.3% of couple-months with no earner and no UI;
same-industry couples lose both jobs one time in five), which needs heterogeneity by liquidity front and centre.
Hendren (2017) is not engaged: the 0.6-point leads raise anticipation (does her entry or looking rise in months -3 to
-1?) - a cheap CPS test.

## 3. What the model must deliver

1. The insurance value of the second earner under correlated vs independent risk holding each spouse's marginal
   hazard fixed. Scenario (i) in counterfactuals.py sets pi_c = 0 and m_H = 1 without rescaling delta, so it also
   removes about 22% of aggregate displacement risk; the smoke CE of +1.09% conflates the two [check]. A
   marginal-preserving decorrelation is the key experiment.
2. The marginal value of a dollar in the no-earner month vs the single-loss month (Baily-Chetty style, from the
   simulated consumption drop in joint-loss months), and the equal-cost ranking of EITC expansion, an unconditional
   child transfer, UI for both spouses and a UI extension, with a full-value consumption equivalent, by liquidity,
   workplace match and race.
3. The same under the re-estimated independent-shock model: how much independent risk overstates the second earner's
   insurance and whether it mis-ranks policies (the methodological contribution).

Missing from counterfactuals.py: both spouses entitled at a joint loss, EITC vs transfer, childcare, full-value
welfare (the CE is consumption-only), children's outcomes. Conceptual: the model pays the EITC monthly on annualised
monthly earnings [check]; the real credit is annual and paid once - exactly sec5's timing argument - so it needs
year-to-date accounting. Cut the child block from the estimated paper (keep as appendix bounds).

## 4. Identification and estimation

Recovery is a genuine pass. The real-data candidate is not reportable:
- Weights: base hazards 91.9%, her exits 6.9%; wealth 0.03%, safety net 0.02%, consumption ~0, added work ~0,
  earnings 0. Fit at the estimate: wealth <= 0 at 45-59 0.18 vs 0.38 (z -23); his labor income loss years 1-3 White
  -3,739 vs -12,054, Black -7,113 vs -3,726 (race pattern reversed); year-6 loss White -3,446 vs -12,127; consumption
  after his single displacement -5.3% vs -1.3%; SNAP Black 0.103 vs 0.150 (z -6.9); wage growth at 35-54 z 6-7;
  SIPP her build-up too fast (0.035 vs 0.019); separation response -0.0008 / +0.0024 vs -0.040 / -0.027.
  Block-balanced weights must be the main specification.
- a_bar at the bound ($60,000 unsecured) while consumption falls 4x the data: smoothing technology misspecified (no
  illiquid wealth, family transfers, severance). Net-worth target (IGE/77) or an illiquid asset needed.
- F 0.10 -> 0.57: its moments are within 1.5 s.e. of zero; acting as a work cost next to phi_F. Fix F.
- d_h ~ 0, pi_dn_w ~ 0: the displacement loss of human capital is absent; re-employment losses (SIPP -0.20 vs model
  -0.02 at 13-24 months) and year-6 scarring missed. Smallest singular value is d_h alone; cond(G'WG) 1.5e10.
- sigmaJ collapsed: the marriage channel is dead at the estimate; race-specific sigmaJ not separable. Pool it, add the
  years 4-6 path and her-displacement response, or drop the response.
- lam_h_B 0.12 vs lam_h_W 0.30: test, do not assert (race-specific husband moments have s.e. 46 / 34).
- Couple type p_H 0.02, m_H 15: over-predicts repeat displacement of Black husbands (0.218 vs 0.151) and the
  different-sector excess (0.062 vs 0.041); under-predicts leads and the same-sector excess (0.126 vs 0.184). With
  s = 1, 2 merged at the estimation size the shared-employer cell is 0.10 vs 0.19. Estimate with three workplace
  groups.
- Husbands' employment 0.99 vs 0.88 / 0.94: husbands leave work only by displacement; add a non-displacement exit.

## 5. Model features

Add: illiquid wealth or the net-worth target; annual EITC accounting; a target for no earner and no UI (SIPP 9.3%,
+5.7) and for consumption in joint-loss months; a non-displacement exit for husbands; three workplace groups.
Not needed: endogenous divorce (but then do not feature the marriage channel), search effort. Cut: child block, F,
race-specific sigmaJ and probably lam_h, c_mem, the lost-hours UI record.

## 6. Empirical additions (public data)

(a) CPS Food Security Supplement (December) linked within the rotation to job-loss months: food insecurity after a
joint vs single loss. (b) SIPP hardship and food-security modules around the joint events. (c) SIPP joint loss and
hardship by liquid-wealth quartile. (d) The Hendren anticipation test. (e) Pre-loss SNAP and income of joint-loss
couples (who they are).

## 7. Plan (ranked)

1. Re-estimate: block-balanced weights, F fixed, sigmaJ pooled, a_bar at a data credit limit, three workplace
   groups; CMA-ES check; independent-shock model. 3-4 weeks incl. HPC.
2. Smoothing technology: net-worth target or illiquid asset; no-earner-no-UI and joint-loss consumption moments.
   3-4 weeks.
3. Annual EITC accounting. 2-3 weeks.
4. Counterfactual hooks: marginal-preserving decorrelation, both-spouse UI, equal-cost EITC vs transfer vs UI,
   full-value CE, by liquidity / workplace / race, the sufficient statistic. 2-3 weeks after 1.
5. Scarring: d_h and depreciation to fit the year-6 loss and re-employment profile; husbands' exit hazard. 2 weeks.
6. CPS Food Security and SIPP hardship, joint vs single loss, by liquidity. 2-3 weeks.
7. Hendren anticipation test in the CPS leads. Days.
8. Cut the child block, F, c_mem and unidentified race splits. 1 week.
