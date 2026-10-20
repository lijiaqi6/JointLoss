# Plan: "Money or Time?" (IGE paper) — 2026-10-17

Goal: turn the research plan into a top-5 / REStud candidate. Requirements (from the 2026-10-16 assessment):
(a) our own causal evidence that the search friction moves mothers' work at a birth and, through it, children's
outcomes; (b) an estimated two-generation model (child skill production) replacing borrowed elasticities;
(c) administrative data if access can be obtained. Plus: fix the IGE measurement and rewrite the intro around the
new fact.

Decision points are marked **[GO/NO-GO]**. Nothing in a later phase starts before its gate is passed.

---

## Phase 0 — Clean up the IGE measurement (1–2 days)

| Step | Script | Output |
|---|---|---|
| 0.1 PSID main spec = Lee–Solon age-40 design (5.CheckPMR) for sons and daughters, by race; lifetime-mean spec kept as robustness | `6.IGEMain.py` | `output/ige_main.csv` |
| 0.2 Weights for pooled rows (PSID core longitudinal weight; NLSY sampling weights) + SRC-only check | `4.Estimates.py`, `6.IGEMain.py` | updated tables |
| 0.3 Chetty-comparable statistics: rank–rank slope, expected child rank at parental p25 / p75 by race and sex, P(top quintile \| parents top quintile) | `7.RankMobility.py` | `output/rank_mobility.csv` |
| 0.4 NLSY97 demoted to an appendix check (short lifetime window, youth-reported income after 1997) | README | — |

---

## Phase 1 — The headline first stage (3–5 days) **[GO/NO-GO]**

Prediction of the model (companion paper): when re-employment is slow, mothers who work before a birth are *less*
likely to leave at the birth. A slack labor market at the birth should therefore raise the share of mothers who keep
working through it — the opposite sign to a pure labor-demand story, in which slack raises job loss.

- **Sample**: PSID first (and higher-order) births 1977–2021 to mothers employed in the year before the birth.
- **Shock**: state unemployment rate in the birth year (BLS LAUS 1976+; UKCPR has it too), relative to state and
  year fixed effects. Main variant: **gender-specific Bartik shocks** — predicted job growth in women's vs men's
  industries (CPS / MORG industry shares by sex × national industry growth). Women's-industry slack lowers the
  mother's own chance of getting work back (the friction); men's-industry slack hits the husband (the risk channel).
  Separating the two is the identification of the paper.
- **Outcomes**: employed at +1, +2, +3 years; stayed with the pre-birth employer (NLSY79 roster, for a subsample);
  quit vs laid off (to separate voluntary exits from job loss).
- **Placebos**: the same shock for childless women of the same age (no birth); the shock two years before the birth;
  the shock for mothers not working before the birth (no job to hold on to).
- **Heterogeneity**: race, marital status, husband's earnings risk, education.
- **Script**: `8.FirstStage.py` (+ `data/state_shocks.pkl` from `8a.StateShocks.py`).
- **Gate**: women's-industry slack raises staying-employed-through-the-birth, significantly, with clean placebos →
  GO. No effect or the demand-side sign → stop and reconsider the mechanism before Phases 2–4.

---

## Phase 2 — From mothers to children (1–2 weeks)

1. **Exposure measures** for every child in the PSID kids file and the NLSY79 Children file:
   mother's employment in months 0–12 after the birth (NLSY79 weekly array: exact timing), father's job loss and
   parents' divorce during childhood, years of welfare receipt, family income by childhood age.
2. **Child outcomes**: NLSY79 Children file — PIAT math / reading recognition, PPVT, Behavior Problems Index at
   5–6, 7–8, 9–10, …; young-adult earnings and education. PSID — adult earnings (kids file), Child Development
   Supplement test scores (**needs a manual CDS download**, see below).
3. **Designs**:
   - reduced form: women's-industry slack at the birth → child outcomes; men's-industry slack → child outcomes
     (money through the father vs time through the mother);
   - IV: mother's months worked in year 1 instrumented by women's-industry slack (if Phase 1 is strong);
   - BFHO-style mediation of the IGE and of the racial gap at a given parental income by the exposure measures.
4. **Script**: `9.ChildExposure.py`, `10.CYAOutcomes.py`, `11.ChildEffects.py`.
5. **Gate [GO/NO-GO for Phase 4's ambition]**: is the time effect on children economically meaningful relative to
   the money effect? Report the share of the IGE / racial gap the mechanism can carry.

---

## Phase 3 — Policy variation (2–3 weeks; can run alongside Phase 2)

| Policy | Variation | Data | First stage (mothers) | Children |
|---|---|---|---|---|
| FMLA 1993 | eligibility: employer ≥ 50 at location, ≥ 1,250 hours, ≥ 12 months tenure; pre/post 1993 × eligible | NLSY79 (firm size at location every round, roster tenure, hours) | job kept through birth | NLSY79 Children file test scores |
| State paid family leave | CA 2004, NJ 2009, RI 2014, NY 2018, WA 2020, … staggered DiD | PSID | return timing | short-run only (CDS) |
| 1996 welfare reform + state waivers | waiver dates, time limits, work requirements, youngest-child exemptions (Herbst's variation) | UKCPR + PSID + NLSY79 Children file | single mothers' work at birth | early-childhood exposure |
| UI generosity for husbands | state max weekly benefit / replacement | UKCPR / DOL + PSID | wives' work at birth (Cullen–Gruber channel) | via family income |

Script per policy: `12.FMLA.py`, `13.PaidLeave.py`, `14.WelfareReform.py`, `15.UIHusbands.py`.

---

## Phase 4 — Two-generation structural model (1–3 months)

1. **Child skill technology**, estimated outside the lifecycle model first (BFHO / Del Boca–Flinn–Wiswall style):
   latent skills from NLSY79 Children file test scores, measurement system + factor scores; inputs = mother's time
   (months not working by child age), family income, father presence; mother's time instrumented by the Phase 1
   shocks. Script `16.SkillTechnology.py`.
2. **Skill → adult earnings** mapping from NLSY79 young adults and PSID kids.
3. **Embed** in the lifecycle model as an outcome block: the mother values the child's skill (altruism parameter),
   so her work choice at a birth trades income against time. Endogenous parameters (altruism etc.) estimated in
   one coded SMM run with the existing ones (joint-estimation rule); technology parameters from step 1 enter as
   first-stage estimates, as BFHO do.
4. **Outputs**: model-implied IGE by race; decomposition of the IGE and of the racial gap at a given parental income
   into the friction, spousal risk and selection; policy counterfactuals (paid leave = job survival across a year
   out; safety-net cash vs work requirement; UI for husbands; EITC).
5. **Dependency**: the companion paper's estimates must be frozen first (married Black mothers still off: 19.6% vs
   8.0%; common-preferences test pending). HPC runs follow the standing rules (32 cores, `--threads 2`, memory per
   worker, email, job names, code snapshot).

---

## Phase 5 — Administrative data (start now; long lead)

- **Now (public, a few days)**: Opportunity Insights / Opportunity Atlas county- and commuting-zone-level outcomes by
  race × parental percentile. Merge with local women's re-employment frictions measured from CPS flows (job finding
  of non-employed women by area) → do places where mothers' re-entry is harder show different Black–White gaps at
  the same parental income? Script `17.AtlasFrictions.py`.
- ~~Census FSRDC application~~ — dropped 2026-10-18: not feasible from the UK. Restricted US data (FSRDC, SIPP-SSA,
  IRS links) and data requests to US teams are off the agenda; public files only.

---

## Phase 6 — Writing

- Rewrite the introduction around the Phase 1 fact and the Phase 2 magnitudes; cut the companion-paper paragraph to
  two sentences; replace the "three steps" plan with results; move most of the contribution paragraphs to
  Section 2.
- New sections: data and IGE measurement (Phase 0), the first stage (Phase 1), children (Phase 2), policy variation
  (Phase 3), the model (Phase 4).

---

## Needs from the user

1. Download the **PSID Child Development Supplement** (CDS-1997/2002/2007 and CDS-2014/2019) into
   `Dropbox/PSID/CDS/` — the PSID site blocks scripted downloads.
2. Confirm commits go to `main` as usual (current IGE work is uncommitted).

## Order of work

Phase 0 → Phase 1 (gate) → Phases 2 and 3 in parallel → Phase 2 gate → Phase 4 → Phase 6.
Phase 5 public-data step can run any time.
