# Paper B: plan to answer Fable's round-2 objections (2026-10-20)

Source: `proposals/fable_qje_round2_paperB_20261020.md`, Section 4. Objections in Fable's order of severity. For each:
what we run, the script, the rule that turns the result into a decision about the paper, and the effort. Everything is
public PSID / NLSY data already on this PC; nothing needs the HPC. Cuts and restructuring stay a PI decision (step 9).

## The order of work

| step | objection | what | script | effort | decides |
|---|---|---|---|---|---|
| 1 | 1 | layoff cost by birth cohort and by how the job-end question was asked; one definition across waves | 103 | 1-2 days | which paper this is |
| 2 | 2 | the father's own path after the layoff; recession-year vs other layoffs | 104 | 2 days | trait vs event |
| 3 | 2 | daughters: employment, marriage, husband, schooling, zeros kept | 105 | 1 day | whether daughters belong in the argument |
| 4 | 3 | the layoff through the career toolkit; son's own displacement, tenure, health | 106 | 3-4 days | the mechanism |
| 5 | 5 | why sons of fathers in declining sectors do better | 93 extended | 1 day | reading of A1 |
| 6 | 4 | headline 1 on the fully measured cohort (born 1964+) with wealth | 98 extended | 1 day | the primary split table |
| 7 | 7 | one baseline sample; like-with-like comparisons; corrected sentences | paper | 1 day | - |
| 8 | 6 | Section 7 stated as nulls with minimum detectable effects | 82 / 99 / 101 / 102 | 1 day | - |
| 9 | all | restructure and cuts (PI decision after steps 1-4) | paper | 1-2 weeks | venue |

Steps 1-3 first (one week); stop and decide with the PI after step 1, because its answer changes what steps 2-4 are for.

---

## Objection 1 (most serious): the layoff cost is not identified, and it may sit in one era and one way of asking

**The objection.** Within son, on sons whose teens fall in 1976 and later, the layoff slope is 0.040 (s.e. 0.113)
against -0.236** overall (`output/simulated_replacement_rate.md`; that sample also requires the father's wage, so it is
a hint, not a test). The older sons' fathers reported job ends under a different net: 1968-75 only if the job was less
than a year old, 1976-83 only if the present position was under twelve months, 1984+ every main-job end of the year,
1988-2001 also the unemployed head's earlier employer (U2), 2003+ a four-job roster (script 19's docstring). Three
readings would each change the paper: (a) the 1970s layoffs were different events (manufacturing, permanent, two oil
recessions); (b) the early net records a different event; (c) chance.

**Step 1 - `103.LayoffCohortRegime.py`.**
- Samples: sons born before 1963 / 1963-75 / 1976 and later (the 1963-75 cohort reaches 45-49 in 2008-25, so the PSID
  has it); and, separately, by the regime of the father's teen-window years (1968-75 / 1976-83 / 1984+).
- Two layoff shares: (a) as now (88/91); (b) one definition in every wave: only the employed-head (E) and
  unemployed-head (U) reports of a job that ended in the 12 months before the interview - the early-wave net applied to
  all waves (drop U2, R and job-history jobs 2-4; job 1 of 2003+ only if it ended in the last 12 months). The
  displacement cache already carries `branch` and `dated`.
- Estimates for every cohort x definition cell: band coefficients 25-29 and 45-49 (40-44 where 45-49 is not reached),
  the change, the within-son slope, treated counts; the closure rows alongside; cohort difference tests on common draws.
- **Decision rule.**
  - Cost of similar sign and size in the 1963-75 cohort under definition (b): the finding is general -> it is the
    layoff paper; go on with steps 2-4 as its mechanism.
  - Cost only before 1963, under both definitions: it is a fact about the layoffs of the 1970s -> the paper says so in
    its title and abstract, and step 2's recession split becomes the main test (were 1970s layoffs different?).
  - Cost only under definition (a): the early net picks up a different event -> report it as a measurement result and
    demote headline 2.

## Objection 2: the selection designs leave a comparison-group problem, which the daughters make visible

**The objection.** The timing comparison (sons whose father was laid off only at 20-26 as the reference) differs in
the father's age and in whether the son was at home; the A3 splits are at p = 0.06-0.15; daughters gain, so the layoff
variable marks something that moves the family's later outcomes in sex-specific ways.

**Step 2 - `104.FatherPathRecession.py`.**
- (i) The father's own path: his ln earnings, employment, further layoffs and unemployment in the five years after the
  son's window, by timing group (T / E / L) and by the A3 parts (small vs large income loss, short vs long
  unemployment, one vs repeated). Shows what kind of father the costly layoff marks: a churner, a recall worker, a man
  on a falling path.
- (ii) Less selected layoffs (Gibbons and Katz): split the teen layoff share into layoff years in which the father's
  sector's national employment fell (93's CES measure) or his state's unemployment rate was above its trend, versus
  other years; within-son slope of each part and their equality.
- **Decision rule.** Cost present in the recession-year layoffs at a size close to the others -> the event reading
  gains and the trait reading loses. Cost only in the idiosyncratic layoffs -> the selected layoffs carry it; state the
  headline as a marker of the father's unstable employment, not as the effect of a layoff.

**Step 3 - `105.DaughtersMechanism.py`.**
- Daughters at 45-49 (and within person over 25-55) on the father's teen layoff share: employment, hours, married,
  husband's ln earnings, years of schooling, occupation score; earnings with zeros kept (Poisson PML); the within-person
  wage slope with employment and marriage controls. Same reduced specification for sons, and report like with like
  (sons' within-person wage slope is -0.086, s.e. 0.096, in that specification).
- **Decision rule.** A daughters' wage gain that survives employment and marriage -> a real asymmetry, its own paragraph
  (mothers' and fathers' job loss and daughters' attachment to work). A gain that is selection into work or marriage ->
  the daughters leave the sons' argument and are reported as such.

## Objection 3: no mechanism for a wage cost that is zero at 30 and 11 log points at 45, with no change in employment

**Step 4 - `106.LayoffCareerMechanism.py`** (Section 5's tools applied to the layoff).
- 27's split of the son's ln wage into his occupation's wage score and his wage within the occupation, at 25-34 and
  35-55: is the layoff's cost between or within occupations?
- 35's early job: does a teen layoff lower the chance of starting at 25-34 in the well-paid, fast-growing
  occupation-industry cells, and does the cost after 35 shrink once the early cell is held fixed?
- 36's same-employer wage growth: do sons of laid-off fathers grow more slowly with the same employer?
- The son's own displacement, job changes, tenure and health (PSID self-rated health and work-limiting conditions,
  1984 on) at 35-49 as outcomes.
- **Decision rule.** A lower start in the fast-growing cells at 25-34 -> the cost is where the son starts, observable at
  25-34 and a policy margin (job search and placement for young men). A within-cell shortfall that opens after 40 ->
  look at health, own displacement and job changes; if those carry it, the cost is the son's own instability; if
  nothing does, say the mechanism is open.

## Objection 4: the shares of headline 1 depend on the cohort, and "money" is a label

**Step 6 - extend `98.ParentalWealth.py`.**
- On sons born 1964 and later (the fully measured cohort): 80's split B plus wealth rank, by band (25-29, 35-39,
  25-55), with the IV-corrected wage share beside the OLS one. This becomes the primary split table; the full-sample
  split moves to a robustness panel.
- Replace "half of the IGE remains parental income" with what the 1964+ table says (wage, schooling, wealth, spells;
  little rest).

## Objection 5: the industry-shock reduced form is a significant gain, not "no cost"

**Step 5 - extend `93.LayoffIndustryShocks.py`.**
- Does the son avoid the father's sector (share of sons working in the father's sector at 25-34 by the shock)? Does
  the gain survive 3-digit industry x age controls instead of 15 sectors? Is it the national cycle at entry (control for
  the national unemployment rate at the son's 22-25)?
- State the reading, or report the gain as unexplained, as the daughters are.

## Objection 6: Section 7 has no finding

**Step 8.** State the nulls as nulls with what they can exclude: minimum detectable effects for the UI split (82), the
simulated replacement rate (99) and the weeks (102); the EITC with its p-values and the null where the credit binds;
group friction as a between-race contrast. One page in the main text; the tables to an appendix only if the PI agrees
(step 9).

## Objection 7: smaller points (step 7, one day, in the paper)

- One baseline sample for the IGE profile (Fable: three baselines - 0.276 -> 0.484, 0.283 -> 0.492, 0.443 at 45-49),
  named once and used throughout.
- NLSY97: say that the AFQT's contribution rises by the same factor (1.64 vs 1.70), and that it carries 25 percent of
  the NLSY97 opening against 62 percent of the NLSY79's - not "three fifths" for both.
- The Shea contrast stated as the layoff's reduced form over its gradient (a Wald ratio), not as a separate finding.
- Daughters vs sons compared in the same statistic.
- Race: "the cost is not distinguishable by race, on 37 treated Black sons at 45-49", not "as much".

## Step 9 (PI decision, after steps 1-4): structure and cuts

Fable's proposed order: the IGE rises with age -> skill at entry and schooling (NLSY79 / 97) -> wealth and the wage
(PSID 1964+) -> the father's layoff, the one component whose share rises (profile, within son, timing, kind of layoff,
daughters, the father's path, mechanism) -> what the layoff is not (closures, industry declines, income) -> policy in
one page -> race as a subsection of each section. Fable's cut list is in its memo (Section 5, step 6). Nothing is cut
until the PI decides; the restructure depends on step 1.

## What this plan cannot do

A second data set that reaches 45-49 with firings separated (SOEP) stays the one addition that would most change a
QJE referee's mind; it is deferred by the PI. The structural model would not substitute for steps 1-2.
