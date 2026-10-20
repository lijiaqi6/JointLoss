# Paper A: should marriage and divorce be modelled? (2026-10-18)

Independent note for the PI's question: "Should we instead model marriage and divorce? Will that improve the fit,
given we find joint loss causes break-up?" Read only: `IGE/paperA_joint_loss/sec1_introduction.tex`,
`sec2_literature.tex`, `sec5_household.tex`, `sec7_model.tex`, `model_document.tex` (Sections 11 and 17, D1-D18);
`IGE/paperA_model/model.py`, `simulate.py`, `panels.py`, `analytic_start.py`; `results/diagnostics_20261018/`
(`variants.csv`, `q_by_block_by_variant.csv`, `moments_by_variant.csv`); `IGE/output/paperA_targets.csv`,
`father_displacement.md`, `psid_joint_loss_checks.md`; my notes `fable_model_choice_paperA.md`,
`fable_bps2016_nextsteps.md`, `fable_bacher2025_paperA.md`, `fable_estimation_review_paperA.md`; the companion
paper's collective-household result (`paper/sec4_model.tex`, "Who decides in a marriage") and the Voena (2015)
replication status. Nothing was run. Terminology: search friction; human capital level, accumulation, depreciation.

## 0. Verdict

**No, not now, and not for the fit.** The separation block already fits (Q = 2.5 of 50,920 at the start), and the
five blocks that are off are governed by objects that a marriage model does not touch or pushes the wrong way:

- *Her exits* (40,884; 0.26% a month against 2.6%): no channel. The exit is a quit of a married wife in a couple
  still married next month; divorce risk makes her hold on to the job, if anything.
- *Employment levels* (3,093; 95% against 81%): the first-order effect of divorce risk on a wife is to raise her
  attachment (Fernandez-Wong). Wrong direction. The selection channel (working wives divorce more, so the married
  stock has fewer of them) is right-signed and an order of magnitude too small.
- *Her search* (3,636): divorce risk raises entry of non-employed wives (right) and amplifies her response to his
  displacement, which is already three times the SIPP's (wrong). The exogenous hazard already carries this motive.
- *Wealth* (2,491): two opposing channels (precautionary saving against separation; the halving of assets at a
  separation, which taxes saving). Neither changes the age shape, which is a borrowing-cost problem.
- *Annual joint loss* (211): the horizon of the permanent couple type. Marriage has nothing to do with it.

The "job loss causes break-up" fact is reproduced by construction: sigma_J(r) is a free parameter with one target per
race (the mean of years 1-3), and the race difference in the target is 0.5 standard errors. Endogenous divorce adds a
mechanism the paper's question does not need and a set of parameters the PSID cannot pin down (the companion's
collective version ended at Pareto weights of 0.28 and 0.76 from different starting points, with Q differences inside
run-to-run noise). What the data do force, and what the current hazard cannot produce, is smaller: the separation
gap keeps widening after he is re-employed (pooled -0.027 at year 1, -0.050 at year 6; Black -0.037 to -0.074), and
the hazard is tied to a state (his non-employment) that unemployment insurance does not change, so the policy
counterfactuals leave separations unchanged by construction. Both have one-parameter, zero-state remedies inside the
exogenous form (Section 5). Recommended path: finish the fit work already identified, estimate once, then run the
two cheap diagnostics of Section 5 and decide the one-parameter change on the untargeted years 4-6.

## 1. What the model does now, exactly

**Hazard.** At the end of every month a married couple separates with probability sigma(r, e_h') = sigma_0(r) +
sigma_J(r) 1{e_h' = 0}, with e_h' his labor state at the start of next month (`model.py:170-171`: `sig_E =
sigma0_r`, `sig_N = sigma0_r + sigmaJ_r`; `simulate.py:421-427`: `ps = sigE if lh2 == 0 else sigN`). He is
non-employed only after a displacement, so the elevation lasts his spell of non-employment, about 1/lambda_h = 4-5
months at the start values, and applies equally whether he is UI-entitled (lh = 1) or not (lh = 2). It does not
depend on her state, on assets, on the children, on his human capital level, or on how long ago the displacement was
(a twelve-month flag and a response to her displacement were considered and not adopted, `model_document.tex:451`).

**After separation.** Separation is absorbing (`mar = 0`). Assets are multiplied by `sep_asset_share` (0.5,
"equal division", `simulate.py:427`; in the solver the continuation uses V^S at a'/2 by interpolation,
`model.py:513-517`). The wife continues alone with the children as the only decision maker: her own labor state,
hours choice (none / part time / full time), human capital level, UI entitlement, transitory shock and child state;
her own displacement hazard delta_w without the common shock (`model.py:338-353`, `cfgS`); her human capital
innovation folds the shared and idiosyncratic components into one draw of probability p_c + p_eps_w
(`model.py:200`, `simulate.py:417-419`). Her budget is the single filer's: tax schedule `ps_single`, EITC for a single
parent, SNAP (`snapBS`, `incS0`, `eitcS_tab`), UI. No child support, no remarriage, no alimony. The husband leaves the
model; his displacements after a separation are imputed only to classify him as treated or control in the PSID
designs, never as an outcome (`panels.py:104-161`). His welfare after a separation is not counted (D15).

**What the separated state does for the fit.** Nothing directly. Every targeted moment is computed on married
couples: CPS couples observed married in t and t+1 (`panels.py:11`), PSID rows "married through all of Y and at the
interview" (`panels.py:28-29`), the separation rate on couples married at Y whose husband is observed at the next
interview (`sep_rows`, `panels.py:547-562`), the event study on fathers with "still with baseline wife". A separated
wife's employment, earnings, wealth and SNAP receipt enter no target. The separated state matters for the fit only
through (i) the married household's continuation value, which anticipates the hazard, and (ii) who leaves the
married sample, which under the current hazard is random given (r, e_h').

**How much weight that continuation value carries.** At the annual rates the model fits (3.2% Black, 1.5% White,
including the wife's death), 1 - (1 - 0.0316)^35 = 67% of Black and 1 - (1 - 0.0152)^35 = 41% of White entry
couples have separated by the wife's age 60. V^S is therefore not a corner of the model but the terminal state of
most Black couples, with no remarriage and no child support. Both omissions make V^S more pessimistic than the US
single mother's state, which overstates the married household's insurance motives: more saving, more attachment of
the wife. That is the wrong direction for employment levels (95% against 81%) and for the share with more than a
year of earnings at 45-59 (0.35 against 0.18), and the right one for the young in debt (0.80 against 0.57). How much
of the misfit this carries is an empirical question with a two-minute answer (Section 5, diagnostic A).

## 2. Would endogenous divorce improve the fit? Block by block

The question is whether a divorce decision (match-quality shock, unilateral divorce, possibly bargaining and
remarriage) moves the blocks that are off, and in which direction. The table uses Q by block at the start
(`q_by_block_by_variant.csv`, column `start`).

| Block | Q at start | Where the misfit comes from (review 2026-10-18) | Channel through which a divorce decision acts | Direction against the misfit |
|---|---:|---|---|---|
| Her exits | 40,884 | monthly churn is governed by sigma_eps alone; `cps_wife_exit` 0.0026 vs 0.0261 | none: the moment conditions on couples married at t and t+1 and on a husband who is employed; divorce risk lowers quits | none / slightly wrong |
| Her search | 3,636 | CPS entry 0.043 vs 0.075; SIPP build-up 0.047/0.086/0.169 vs 0.019/0.037/0.054; sigma_eps = 0.10 cuts the block to 255 | insurance motive: a non-employed wife enters to protect her human capital level and her own earnings; his displacement raises divorce risk and so her incentive | entry right, response to his loss wrong (already 3x too strong); the exogenous sigma_J already carries the second |
| Employment levels | 3,093 | static preference start values; wives work in 95% of months | (a) insurance motive raises attachment; (b) selection: wives with higher human capital levels have a better outside option, divorce more, and leave the married sample | (a) wrong; (b) right but small: a 1-point difference in annual hazards shifts the married stock's composition by a few points over 30 years, not 14 |
| Wealth | 2,491 | one interest rate for saving and borrowing: 0.80 vs 0.57 in debt at 25-34, 0.35 vs 0.18 rich at 45-59 | (a) precautionary saving against separation; (b) the halving of assets at a separation lowers the expected return on saving by about sigma/2 a month (1% a year White, 1.6% Black); endogenous timing concentrates (a) on young, low-quality matches | ambiguous level effect; no effect on the age shape, which is the problem |
| Joint loss, annual | 211 | permanent couple type: 0.118 vs 0.063 (`psid_cy_diff_all`) | couples with a joint loss separate more (BPS panel: +6.5 points after a joint displacement, 4 events, p = 0.15) and leave the measured sample | right sign, about 0.004 of a 0.055 gap |
| Safety net | 126 | SNAP of Black couples 7.2% vs 15% because husbands are rarely non-employed | none: the SNAP targets are married rows; single mothers' receipt is untargeted | none |
| Separation | 2.5 | fits | the block it would re-fit with more parameters | nothing to gain |

Two points of economics behind the table. First, the sign of the effect of divorce risk on a wife's work depends on
the property regime and the decision rule: in Voena (2015) unilateral divorce with community property *lowers* wives'
participation (she is compensated through assets), while Fernandez and Wong find that higher divorce risk *raises*
married women's participation through the insurance motive. In Paper A's unitary household with equal division and
no bargaining the only operative channel is insurance, so the sign is up, and up is the wrong way for a model whose
wives already work too much. Second, in every version the divorce margin is a slow state (match quality, assets,
human capital levels move over years), so it cannot generate monthly churn; the exit block is out of its reach by
construction, exactly as it is out of the reach of the 30 estimated parameters.

**Answer to question 1:** none of the five misfit blocks would be improved by endogenous divorce; two would be made
worse at the margin that matters (employment levels, the SIPP response). The fit problems are in the taste-shock
scale and classification of exits, the preference start values, the borrowing wedge and the memory of the common
shock, all of which have coded options or decisions pending (`sigma_eps` profile, `rwedge`, `c_mem`, `eta_up`).

## 3. What endogenous divorce would add to the paper's question

### 3.1 Is the separation response identified as causal, and does the hazard reproduce it by construction?

The estimate is a stacked event study with father x stack and year x stack fixed effects, clean controls (no
displacement to ev+6), reference e = -2 (`father_displacement.md`, Section 2). Three things to say plainly in the
paper and to the PI:

- *There is no placebo test for this outcome.* "Still with baseline wife" is 1 by construction at the baseline years
  (treated mean 0.989 at e = -2, -1), so the pre-period coefficients are mechanical: e = -3 is -0.024*** pooled
  (she was not yet his wife in some couples) and e = -1 is +0.012** (+0.029*** Black). They are not evidence of a
  pre-trend and not evidence of its absence. Identification rests on the post-period against controls with father
  fixed effects, the standard displacement design, nothing more.
- *The mechanism test the literature uses comes out in favour of an income or strain reading.* Charles and Stephens
  (2004) found divorce rising after layoffs and not after closures and read it as information about the husband.
  Here closures and layoffs give the same response (Black -0.044 vs -0.044, White -0.015 vs -0.021; closures minus
  layoffs 0.000, p = 0.99, and 0.006, p = 0.75; `psid_joint_loss_checks.md`, Section 2c). A response that is the same
  after a closure is what an economic model of the marriage (lower household income, lower surplus) predicts, so
  the fact supports the model's reading without requiring the model to contain the decision.
- *The exogenous hazard reproduces the targeted mean by construction.* sigma_J(r) is free, one target per race
  (`psid_es_bw_present_13_B` -0.040, s.e. 0.021; `_W` -0.027, s.e. 0.012). The race difference is 0.5 s.e. and my
  estimation review already recommends one common sigma_J. The heterogeneity that would discipline a richer form
  is not significant either: by the youngest child's age -0.030 and -0.030; by the wife's baseline employment
  -0.036*** (employed) against -0.019 (not employed, p = 0.16), a difference of 0.017 with s.e. about 0.017.

What is *not* by construction and is a genuine test of the form is the time path. The elevation lasts his spell of
non-employment, so the simulated survival gap opens during the spell and then stays flat. The data's gap keeps
widening long after re-employment: pooled -0.027 (year 1), -0.037 (3), -0.050 (6); Black -0.037, -0.053, -0.074;
White -0.017, -0.022, -0.030. A displacement lowers his human capital level permanently (d_h, then slower
accumulation), so a hazard that depends on his *level* rather than on his *status* produces a permanent elevation
and the widening. That is a one-parameter change with no new state (Section 5, option M2), and years 4-6 are the
untargeted moments that decide it.

### 3.2 BPS selection on stable couples

The paper's point (Section 1 and 2) is that BPS condition on couples whose record does not end, while the job loss
ends records. To quantify the bias in the model, the simulated BPS sample is built from simulated couples with the
BPS trims (the test in `sec2_literature.tex`, "required to reproduce their estimates"). Under the current hazard,
who separates is random given his status, so the simulated selection is the *direct* effect only: the sample loses
the months of displaced households at the rate sigma_J. If real separations after a displacement are concentrated
among couples with less insurance capacity (low assets, a wife without a job), BPS's stable couples are also
selected on insurance capacity and the model understates the bias. The PSID evidence points the other way, if
anywhere: the response is larger when the wife worked at baseline (-0.036*** vs -0.019), consistent with her outside
option, not with a lack of insurance. An endogenous divorce rule would produce this dependence from theory; a
reduced-form hazard that depends on her labor state (already in the state) would produce it with one parameter.
Neither is forced by a 1-s.e. difference. Report the heterogeneity in a footnote; do not model it until it is
significant.

### 3.3 Counterfactuals that need it

| Counterfactual (sec7, list (i)-(v)) | What the current hazard does | What endogenous divorce would add | Needed? |
|---|---|---|---|
| (i) common shock off | separations fall with his non-employment months | same | no |
| (ii) UI for both spouses, 52 weeks | separations unchanged by construction: the hazard depends on e_h', which UI does not alter (lambda_h exogenous, he always looks) | a response of separations to UI through household resources, as in Lindo, Regmi and Swensen (2025), cited in sec2: UI generosity mitigates divorce after men's layoffs | partly: the parental-presence channel to the children is dead for UI policy under the current form; one parameter fixes it (M2b) |
| (iii) EITC-type subsidy vs unconditional transfer | separations unchanged | separations respond to transfers that pay when no one works | same as (ii) |
| (iv) childcare subsidy | unchanged | separations respond to her employment | no |
| (v) Black couples with White hazards, then the White separation response | sigma_0 and sigma_J swapped by hand | the race gap in separation becomes an outcome of the environment (his 8.0% vs 4.8% annual displacement, lower earnings, her higher search friction), consistent with D2 "common preferences, race through the environment" | attractive in principle; see below |

The last row is the strongest conceptual argument for endogenous divorce: sigma_0(B) = 2 sigma_0(W) is a race-specific
parameter with no mechanism, in a paper whose discipline is that race enters only through the environment. But the
Black-White difference in divorce survives controls for income, education and employment in every study I know, so an
endogenous rule would need a race-specific match-quality or taste parameter to fit the baseline rates, and the
parsimony count would not change. The welfare of the marriage itself (insurance value of marriage, who stays married,
the husband's loss) is not the paper's question and cannot be computed without tracking him (D15).

**Answer to question 2:** the exogenous hazard reproduces the targeted fact by construction and the causal reading
is as good as the displacement event study (no placebo for this outcome; closures = layoffs supports an income
reading). Endogenous divorce adds (a) a policy response of separations, which the paper's UI and transfer
counterfactuals currently cannot have, and (b) a mechanism for the race gap in separation that would still need a
race-specific parameter. (a) has a one-parameter alternative.

## 4. Costs

**State space and computation.** Three tiers, from the companion's experience (`paper/sec4_model.tex`, "Who
decides"; `docs/bargaining_design.md`; HPC memory rules):

| Version | New states | New parameters | Solve cost | Memory per worker |
|---|---|---|---|---|
| Wife decides, match-quality shock (companion structure) | match quality (2 points) | 3-4 (quality values, degradation, divorce taste scale), replacing sigma_0(r), sigma_J(r) | x2 | about x2 (4 to 8 GB) |
| Either spouse can leave (unilateral, no bargaining) | match quality + a single man's problem (his assets, human capital level, UI) | + his divorce value scale, remarriage arrival and partner draw (2-3) | x2-3 | x2-3 |
| Collective with limited commitment (Voena, Mazzocco, Low et al.) | + Pareto weight grid (10-20 points), renegotiation | + weight, bargaining shifters | x10-20 | 128-200 GB (companion: bargaining 128G, renegotiation 200G; OOM at 64G) |

Current cost is 84-124 s per evaluation (`variants.csv`), 16 workers at 64 GB, about 4 GB per worker. Tier 1 keeps
the HPC rules; tier 3 breaks them. A remarriage market is required for any version in which V^S is the outside
option, because without it the outside option is too poor and the divorce rule will fit the hazards only with a
match-quality distribution that compensates (the companion found the divorce hazard by duration hump-shaped in the
PSID and flat in the model, `docs/bargaining_design.md:119`).

**Identification.** The PSID has about 850 Black and 1,140 White separations in the target samples
(`paperA_targets.csv`, n columns) and could add hazards by marriage duration and by the wife's employment. That
identifies a match-quality distribution and a taste scale (three duration bins for two types). It does not identify
a Pareto weight: the companion estimated mutual consent, unilateral with a fixed weight and limited commitment, all
parameters free, and found weights of 0.41 and 0.76 (mutual consent) or 0.28 and 0.40 (limited commitment) from
different starting points, with Q differences within the 200 units that separate runs of one specification. The
moments that would identify the weight are responses to divorce-law reforms, which belong to the other paper and
are not among Paper A's targets, and the paper's own sex-ratio tests found no distribution-factor effect on wives.

**Timeline.** The model has not been estimated once. The estimation review lists five code changes, four local
checks and seven HPC stages before a candidate estimate exists. Adding a divorce decision now would mean a new
state, new targets (duration hazards), a new start-value mapping and a re-run of every staged check, against the
PI's rules to code one step at a time and to compare steps on one moment set. Six to eight weeks for tier 1 with
tests, and a tier-1 model is the one the companion already built and found uninformative for its question.

## 5. Middle options, in order of cost, and what decides each

**Diagnostic A (no parameters, one evaluation, about two minutes).** Evaluate the start with `sig_E = sig_N = 0`
(the test overrides in `model.py:172-174`) and read the employment-level, wealth and her-search blocks against the
start. This measures how much the anticipated separation (Section 1, last paragraph) contributes to wives working
too much and to the old being too rich. If the blocks move by less than the noise floor (about 30 units), the
marriage block is irrelevant to the fit and the PI's question is closed on fit grounds with a number. If they move
by hundreds, the first change is not a divorce decision but a less pessimistic V^S (diagnostic B).

**Diagnostic B (calibrated inputs, no state).** Child support as a calibrated monthly transfer to the separated wife
by race (PSID child-support income of divorced mothers with children; one input), and a remarriage exit treated as
the end of the simulated record at a calibrated annual hazard (the record stops, as the PSID record of the couple
does). Zero estimated parameters; only if A says V^S matters.

**M2a (one parameter, no new state): hazard in his human capital level.** sigma(r, e_h', h_h) = sigma_0(r) + sigma_J
1{e_h' = 0} + sigma_H (h_entry - h_h)+ , with h_h already a state. The displacement loss d_h and slower accumulation
make the elevation permanent, which is the widening of years 4-6 the current form cannot produce. Decided by the
untargeted path at the estimate: simulate `bw_present` by event year and compare with -0.027/-0.037/-0.050
(pooled) and -0.037/-0.053/-0.074 (Black). If the simulated gap is flat after year 1 while the data's doubles, add
sigma_H and target years 4-6 (one more moment per race).

**M2b (one parameter, no new state): elevation that differs by his UI entitlement.** sigma_J for lh = 1 (entitled)
and lh = 2 (not), both already states. This is the smallest change that lets the UI counterfactual move separations
and the parental-presence channel, in the direction Lindo, Regmi and Swensen find. Decided by a reduced-form check
first: the separation response by state UI generosity (`IGE/12b.UIGenerosity.py` already builds the schedule) or by
UI receipt in the PSID stacks. With about 2,400 displaced fathers the power is limited; if the interaction is not
significant, say so in a footnote and keep one sigma_J.

**M3 (one parameter): response to her displacement.** Not forced: the only evidence is the BPS panel's +2.9 points
(p = 0.033) on a dual-earner sample with few events; the fathers design has not been run for her displacement. Run
it in IGE/19 (her displacement as the event, "still with baseline husband") before deciding; it is one table.

**M4 (tier 1 endogenous divorce) as an extension.** Only after the main estimate and only to answer "do the
counterfactuals change under an endogenous divorce rule", estimated on the same moment set plus duration hazards,
reported as robustness. The companion's result says the answer is likely "no" for the fit; the counterfactual (ii)
is where it could differ.

**M5 (collective, limited commitment, remarriage market).** Not for this paper. It belongs to the child-penalty
paper's divorce-law agenda, where the moments that identify it exist.

## 6. Recommendation

1. **Now: no marriage model.** Keep D10 and D15. Add one sentence to sec7 stating that the separation hazard is a
   reduced form for the marital surplus, that its time path after re-employment is a test, and that the husband's
   welfare after separation is not counted.
2. **First instead (all already identified, none run yet):** the exit target and sigma_eps, the preference start
   values by one-dimensional roots, the borrowing wedge, the memory of the common shock against the permanent type,
   eta_up, the husband's employment rate as a target; then the Gauss-Newton recovery and the main estimate. These
   are the blocks that carry 98% of Q.
3. **At the estimate, two cheap reads:** diagnostic A (one evaluation) and the simulated `bw_present` path by event
   year against the PSID's years 4-6. The first says whether the marriage block touches the fit at all; the second
   decides M2a. Run the PSID UI-generosity interaction in IGE/19 in parallel to decide M2b.
4. **Later, as robustness only:** tier-1 endogenous divorce (M4) if a referee or the UI counterfactual's marriage
   channel requires it; never tier 3 in this paper.
5. **In the paper:** state the three facts of Section 3.1 (no placebo for this outcome; closures equal layoffs;
   race, child-age and wife's-employment differences within 1-1.5 s.e.), and present sigma_J as what it is: a
   parameter that reproduces the mean response, with the untargeted path as its test.
