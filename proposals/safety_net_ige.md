# The safety net and the IGE: can we write it with what we have? (design note, 2026-10-17)

Scope: whether welfare programs (AFDC/TANF, SNAP/Food Stamps, the EITC, Medicaid, UI, SSI, child credits) can
carry a new paper, or a well-defined part of *Money or Time?*, on the intergenerational elasticity of income (IGE),
rank mobility and the Black–White gap at a given parental income, using our data and the companion lifecycle model.
Read-only checks only. Helper code lives in the session scratchpad, not in `IGE/`; snippets are in Section 3.

**Short answer.** Not as a stand-alone reduced-form paper: the public PSID has state but no county, the state-year
variation left after fixed effects is small, and the cohorts with adult outcomes are few. Our first power check
shows this (Section 3.4). It **can** work as the policy block of *Money or Time?*, built on one quasi-experiment
that fits the mechanism closely (**work requirements and the infant exemption**, Design B) plus a structural
counterfactual that the literature does not have (**floor versus wage subsidy under a search friction, by race**,
Design A). If the go/no-go test in Section 4 passes strongly, Design A can be split off as a separate paper.

---

## 1. Literature map

Every number below was checked against the source linked next to it in this session, unless it is marked
*unverified*. "WP" means the working-paper version; where the WP and the journal version differ, both are given.

### 1.1 Long-run effects of childhood exposure to the safety net

| Paper | Venue | Variation / data | Key number (source) |
|---|---|---|---|
| Hoynes, Schanzenbach & Almond, *Long-Run Impacts of Childhood Access to the Safety Net* | AER 106(4), 903–934, 2016 | Food Stamp county roll-out 1961–75; **PSID** with county of residence in childhood (restricted geocode) | Full exposure from in utero to age 5 lowers the metabolic-syndrome index by 0.294 s.d. (p<0.01). The economic self-sufficiency index rises by 0.182 s.d. in the high-participation sample (p=0.14), and significantly for **women** but not men ([AER PDF](https://sites.asit.columbia.edu/wp-content/uploads/sites/32/2018/08/Long-Impact-of-Childhood-Access-to-the-Safety-Net.pdf); [NBER w18535](https://www.nber.org/papers/w18535)) |
| Bailey, Hoynes, Rossin-Slater & Walker, *Is the Social Safety Net a Long-Term Investment?* | REStud 91(3), 1291–1330, 2024 | Same roll-out; 2000 Census + ACS 2001–13 linked to the SSA NUMIDENT, 17.5m people | Treatment-on-the-treated effects of exposure before age 5: +6% s.d. human capital, +3% s.d. self-sufficiency, +8% s.d. neighbourhood quality, +1.1 years of life expectancy, −0.5 pp incarceration. MVPF ≈ 62 ([REStud](https://restud.com/is-the-social-safety-net-a-long-term-investment-large-scale-evidence-from-the-food-stamps-program); WP: [NBER w26942](https://www.nber.org/papers/w26942)) |
| Bastian & Michelmore, *Long-Term Impact of the EITC on Children's Education and Employment* | JOLE 36(4), 1127–1163, 2018 | Federal + state EITC expansions over four decades; **PSID**; simulated exposure by family size × year × state | An extra $1,000 of EITC exposure at ages 13–18: high school completion +1.3%, college +4.2%, employment +1.0%, earnings +2.2%. Mostly through higher pre-tax family earnings ([JOLE](https://www.journals.uchicago.edu/doi/10.1086/697477); the numbers are confirmed in the abstract summary and in [Bastian's CV](https://www.brookings.edu/wp-content/uploads/2024/11/Jacob_Bastian_CV.pdf)) |
| McInnis, Michelmore & Pilkauskas, *Intergenerational Transmission of Poverty and Public Assistance: Evidence from the EITC* | JHR (online 2024); NBER w31429 | Childhood EITC exposure; **PSID** 1968–2017 | Poverty or near-poverty in adulthood −5 pp (journal), −7 pp in the WP. Lower adult public-assistance use, for some groups only ([NBER w31429](https://www.nber.org/papers/w31429); [JHR](https://jhr.uwpress.org/content/early/2024/03/01/jhr.0422-12241R2/tab-article-info)) |
| Akee, Jones & Simeonova, *The EITC and Linking Data for Examining Multigenerational Effects* | NBER CRIW volume, 2022 (CES WP 20-35) | IRS 1040 linked to Census/ACS; EITC generosity varies with siblings' births and siblings aging out | "Significant and mostly positive" effects on children's rank conditional on parents' rank, differing by household type (single mother vs married) and by the child's sex. Effect sizes *unverified* ([NBER chapter](https://www.nber.org/books-and-chapters/measuring-distribution-and-mobility-income-and-wealth/eitc-and-linking-data-examining-multigenerational-effects)) |
| Dahl & Lochner, *Impact of Family Income on Child Achievement: Evidence from the EITC* | AER 102(5), 2012 | **NLSY79 Children** (about 4,500 children); simulated federal EITC instrument (non-linear expansions × family size × income) | $1,000 raises combined math + reading scores by 6% s.d. in the short run, more for disadvantaged children ([HCEO summary](https://hceconomics.uchicago.edu/node/3356); [IRP DP](https://www.irp.wisc.edu/publications/dps/pdfs/dp136109.pdf)) |
| Barr, Eggleston & Smith, *Investing in Infants* | QJE 137(4), 2539–2583, 2022 | Discontinuity at the 1 January birth date for EITC and dependent benefits; IRS records | About $1,300 (≈10% of income) in the first year raises young-adult earnings by at least 1–2%, more for boys; the transfer pays for itself ([NBER w30373](https://www.nber.org/papers/w30373); [IRP brief](https://www.irp.wisc.edu/resource/why-early-financial-support-for-new-parents-is-a-good-investment/)) |
| Aizer, Eli, Ferrie & Lleras-Muney, *Long-Run Impact of Cash Transfers to Poor Families* | AER 106(4), 935–971, 2016 | Mothers' Pension applicants 1911–35, accepted vs rejected, linked records (almost all White) | Sons of accepted mothers lived about 1 year longer and had more schooling and higher income. A newer re-estimate by Eli and co-authors (2026 seminar, unpublished) finds longevity +1% (noisy), income +7%, employment +6% and **no education effect** ([NBER w20103](https://www.nber.org/papers/w20103.pdf); [2026 seminar](https://www.economics.harvard.edu/sites/g/files/omnuum5991/files/2026-02/3.13.26%20Shari%20Eli.pdf)). The schooling magnitude is *unverified* |
| Goodman-Bacon, *Long-Run Effects of Childhood Insurance Coverage* | AER 111(8), 2550–2593, 2021 | Medicaid roll-out 1966–70 × pre-existing welfare-based eligibility | Lower adult mortality and disability and less disability-transfer receipt; employment rises for Whites; the government recoups more than the original cost ([AER](https://www.aeaweb.org/doi/10.1257/aer.20171671); [NBER w22899](https://www.nber.org/papers/w22899)) |
| East, Miller, Page & Wherry, *Multigenerational Impacts of Childhood Access to the Safety Net* | AER 113(1), 98–135, 2023 | State prenatal Medicaid expansions; natality files | Health gains carry over to the **next generation's** birth outcomes ([AER](https://www.aeaweb.org/doi/10.1257/aer.20210937)) |
| Hartley, Lamarche & Ziliak, *Welfare Reform and the Intergenerational Transmission of Dependence* | JPE 130(3), 523–565, 2022 | **PSID** mother–daughter pairs 1968–2013; state welfare reform | A mother's AFDC/TANF participation raises her daughter's adult participation by about 30 pp (some summaries say 25 pp). Reform cuts that transmission by at least 50%, but there is **no** reduction in transmission of education, income or broader safety-net use ([JPE accepted PDF](https://gattonweb.uky.edu/Faculty/Ziliak/HLZ_JPE_Ahead.pdf); [IZA DP 10942](https://docs.iza.org/dp10942.pdf)) |
| Deshpande, *Effect of Disability Payments on Household Earnings: SSI Children's Program* | REStat 98(4), 638–654, 2016 | Removal of child SSI at age-18 / medical reviews | Parents fully offset the lost SSI with their own earnings; the WP says at least $600 per $1,000 lost ([IDEAS](https://ideas.repec.org/a/tpr/restat/v98y2016i4p638-654.html); [NBER RDRC WP](https://www.nber.org/sites/default/files/2023-05/NB13-04%20Deshpande%20FINAL-VD.pdf)) |
| Price & Song, *Long-Term Effects of Cash Assistance* (SIME/DIME) | Princeton IRS WP 621, 2018 | Randomised negative income tax, 1970s | Adults' later earnings −$1,800/yr and disability applications +6.3 pp; **no significant effects on children's** main outcomes ([Princeton WP](https://repec-prod.princeton.edu/econlib/RePEc/pri/papers/1660)) |
| Hendren & Sprung-Keyser, *A Unified Welfare Analysis of Government Policies* | QJE 135(3), 2020 | 133 policies, MVPF | Policies for children have high MVPFs, often infinite (they pay for themselves); policies for adults have MVPFs of about 0.5–2 unless they spill over to children ([QJE PAR copy](https://par.nsf.gov/servlets/purl/10237586)). The EITC-specific MVPF is *unverified* |

Cited in our draft but **not re-verified** here: Herbst (2017) on infant outcomes after the loss of work-requirement
exemptions; Chase-Lansdale et al. (2003) on mothers' time; Cullen & Gruber (2000) on wives' earnings and husbands' UI.

### 1.2 Safety net, the IGE and the racial mobility gap

| Paper | What it says | Source |
|---|---|---|
| Chetty, Hendren, Kline & Saez (QJE 129(4), 2014) | Across places, upward mobility is **correlated** with the level and progressivity of local tax expenditures, including state EITCs. Correlational only | [NBER w19843](https://eml.berkeley.edu/~pkline/papers/w19843.pdf); [EPI summary](https://www.epi.org/blog/mobility-inequality/) |
| Chetty, Hendren, Jones & Porter (QJE 135(2), 711–783, 2020) | At a given parental income the Black–White gap comes from men's wages and employment; there is no comparable gap among women | [IDEAS](https://ideas.repec.org/a/oup/qjecon/v135y2020i2p711-783..html) |
| Parolin (Socio-Economic Review, 2021) | States with larger Black population shares put less TANF money into cash. Equalising states' TANF priorities would cut the Black–White child poverty gap by up to 15% | [WP](https://medialibrary.uantwerpen.be/oldcontent/container2601/files/CSBWP2018/CSBWP2018_04.pdf); [Columbia summary](https://magazine.columbia.edu/article/cash-critical-fight-against-poverty) |
| Hartley, Lamarche & Ziliak (2022) | Covers transmission of *dependence*, not of income. Reform weakened welfare transmission but not income or education transmission | above |
| Beach (Amherst undergraduate thesis, 2022) | PSID: parental EITC exposure at 0–5 lowers reading scores, more for Black children. Not peer-reviewed; suggestive only | [thesis](https://amherst.edu/system/files/media/Sam%20Beach%20Thesis%202022%20Final.pdf) |

A targeted search found **no peer-reviewed paper** that estimates how childhood exposure to AFDC/TANF, SNAP or the
EITC changes the Black–White gap in adult outcomes at a given parental income, or the IGE itself.

### 1.3 Structural models: the mother, or the child, but not both with frictions

| Paper | Contribution | Missing for our question | Source |
|---|---|---|---|
| Mullins, *Designing Cash Transfers in the Presence of Children's Human Capital Formation* (Minneapolis Fed IWP 117, 2025) | Single mothers' work, welfare and child investment, identified from 1990s policy variation. Optimal transfers are up to 50% more generous than the US benchmark (20% in the 2022 version); post-1996 changes lowered child skills on average | No search friction, no race, no husbands | [Minneapolis Fed](https://minneapolisfed.org/research/institute-working-papers/designing-cash-transfers-in-the-presence-of-childrens-human-capital-formation) |
| Daruich & Fernández, *Universal Basic Income: A Dynamic Assessment* (AER 114(1), 38–88, 2024) | UBI causes large welfare losses, mostly through parents' investment in children's skills | No search friction, no race | [AER](https://www.aeaweb.org/doi/10.1257/aer.20221099) |
| Low, Meghir, Pistaferri & Voena, *Marriage, Labor Supply and the Dynamics of the Social Safety Net* (Chicago Fed WP 2025-27; Cowles 2121) | PRWORA time limits lower claims, raise employment and lower divorce, with limited commitment in marriage | No children's outcomes, no search friction, no race | [IDEAS](https://ideas.repec.org/p/cwl/cwldpp/2121.html) |
| Guner, Kaygusuz & Ventura (REStud 87(5), 2290–2321, 2020) | Childcare credits raise married women's participation by 10.6%; child credits lower it by 2.4% | No children's outcomes | [CEMFI PDF](https://www.cemfi.es/~guner/gkv-childtransfers-October-2020.pdf) |
| Keane & Wolpin (IER 51(3), 851–892, 2010) | NLSY79 lifecycle model of school, work, marriage, fertility and welfare for Black, Hispanic and White women; the welfare system amplifies racial gaps | No friction, no spousal risk, no child | [PIER WP](https://economics.sas.upenn.edu/sites/default/files/filevault/working-papers/06-004.pdf) |
| Chan (Econometrica 81(3), 941–1001, 2013) | SIPP model of single mothers with time limits, work requirements and the EITC. The economy explains half of the 1992–99 rise in labour supply; a time limit is the most efficient reform | No child, no friction | [Econometric Society](https://www.econometricsociety.org/publications/econometrica/2013/05/01/dynamic-model-welfare-reform) |

### 1.4 What has not been done (the opening)

1. **Incidence of work-conditioned support when jobs are hard to find.** In 1990–2000 the US moved support for poor
   families with children from an unconditional floor (AFDC) to work-conditioned transfers (the EITC, TANF work
   requirements). Every evaluation treats getting a job as a choice. With a search friction, a work-conditioned
   transfer reaches only mothers who hold a job. If job finding is slower for Black women, as the companion paper
   finds (39% vs 53% of searchers within a quarter), the same reform moves resources away from Black children at a
   given parental income. No paper measures this or connects it to the racial mobility gap.
2. **Time versus money from the same policy.** Work requirements add money and take away the mother's time.
   Long-run studies estimate the net effect of one program at a time. None separates the time channel, and none
   models the infant exemption as buying time without losing the floor.
3. **The safety net as a substitute for the husband.** In our model the floor $b$ is paid when the husband is
   unemployed, so it insures the mother against his risk as well as hers. No paper links that substitution to
   children's outcomes.
4. **Two-generation structural models with race, a search friction and spousal risk.** Mullins and
   Daruich–Fernández have the child. LMPV, Keane–Wolpin and Chan have the mother and the policy. None has the
   friction.

---

## 2. Candidate designs

The companion model, as written in `paper/sec4_model.tex`, already contains the following:
- a safety-net floor $b = 0.25$ (≈ $10,000/yr) for non-employed women who are single or whose husband is not
  employed (it is withdrawn when the husband works);
- $b_m = 0.25$ for non-employed husbands;
- a single-mother child transfer $b_{k,sg} = 0.12$ per child (fixed, not means-tested);
- a search friction (job finding out of work $\lambda_u(E)$, separation, survival of a job across a year out);
- the husband's employment risk $p_m(t,E_m)$;
- a child work penalty $\theta_{ak}$ by age of the youngest child.

It has **no EITC, no work requirement, no time limit and no child-skill block**. Phase 4 of `PLAN.md` adds the
skill block.

### Design A — Floor or wage subsidy? Who gets the safety net under a search friction, and what it does to the racial mobility gap (structural core)

- **Question.** How do the IGE and the Black–White gap at a given parental income change when support moves from
  the floor $b$ to an EITC-style subsidy on mothers' earnings, or when $b$ is made conditional on work or search?
- **Why it matters.** It explains how a dominant policy shift affects a central fact (Chetty et al. 2020). Audience:
  REStud / AEJ:Policy, and a top-5 only if it comes with credible own evidence (Designs B and C) and the
  two-generation model. As a stand-alone counterfactual exercise it is a field-journal paper. Be honest: the
  counterfactual alone, without new identification, will be read as "assumptions in, results out".
- **Mechanism (our ingredients).**
  - With a slow return to work, a wage subsidy reaches mothers who keep their jobs and misses those who lose them.
    The floor reaches both.
  - Because the floor is withdrawn when the husband works, it is also insurance against the husband's job loss.
    An EITC partly replaces it: it pays when *she* works, which happens more often when he does not.
  - Black mothers face a higher search friction and less secure husbands, so their incidence and their insurance
    loss differ from White mothers' at the same income.
  - Work requirements add a further channel. A requirement to search does not create jobs: with a low job-finding
    rate, required search is followed by sanctions and the loss of the floor.
- **Identification.**
  - Structural parameters come from the companion SMM (joint estimation rule).
  - Policy parameters are calibrated from the UKCPR/`policy_calendar.csv`: AFDC/TANF maximum benefit, federal and
    state EITC schedules (phase-in rates, maximum credits 1980–2024), time limits and work exemptions.
  - Validation is out of sample: the model must reproduce, without re-estimation, the 1993–2000 changes in single
    mothers' employment, AFDC receipt and EITC receipt by race (CPS ASEC from IPUMS `cps_1`, which has `INCWELFR`
    1968–2024 and `EITCRED` 1992+), and the reduced-form first stages of Design B.
- **Outcomes.** Model-implied IGE and rank mobility by race (via the Phase 4 skill block); the mother's time with
  infants and family income; the incidence of transfers by race and parental-income quintile.
- **Threats.**
  - Results depend on the child-skill technology. Discipline it with Designs B and C and with the NLSY79 Children
    estimates of Phase 4.
  - Take-up is incomplete and higher for Black women (NLSY79 E.5: 63.8% vs 45.5% of non-employed single mothers on
    AFDC), while the model pays $b$ to every eligible woman. Add a take-up cost or report the results as bounds.
  - The model has no tax system beyond net wages; adding the EITC schedule changes the budget only.
- **What the model adds.** Counterfactuals the data cannot give:
  - (i) cut $b$ by 10/25/50%;
  - (ii) replace the floor with an EITC of equal cost;
  - (iii) $b$ conditional on search after the child is 3 / 12 months (work requirement + exemption);
  - (iv) a 60-month time limit;
  - (v) the same reforms with the White search friction given to Black women: the share of the racial incidence
    gap that comes from the friction rather than from income.
  Welfare: MVPF-style comparisons of (i)–(iv) with the children's earnings included.
- **Feasibility.** All policy inputs are on disk (Section 3.2). The structural block is Phase 4 work, and it
  depends on freezing the companion estimates.

### Design B — Work requirements, the infant exemption and mothers' time at a birth (reduced form; the quasi-experiment)

- **Question.** When a state exempts mothers of young children from welfare work requirements for longer, do
  single mothers stay home longer after a birth, keep the floor, and do their children score higher?
- **Why it matters.** It is the cleanest policy test of time versus money: the exemption buys time without
  removing the floor. It extends Herbst (2017) from infant health to the time channel and to race, and it connects
  to the friction. It fits *Money or Time?* (Phase 3 row "1996 welfare reform + state waivers"). As a stand-alone
  paper it is a field paper (JHR / JPubE / AEJ:Policy).
- **Mechanism.** With the exemption, $b$ is unconditional while the child is young. Without it, a mother must work
  or search. Under a search friction a requirement to search becomes, for many, a loss of the floor or acceptance
  of a poor job. The prediction: a stronger first stage for Black single mothers, both on leaving the welfare
  rolls and on hardship.
- **Identification.**
  - `policy_calendar.csv` has `work_exempt_m`: exemption months, 0–48, from AFDC waivers and TANF, 1,706
    state-years with data. It also has waiver dates (`waiver_any`, `waiver_workreq`, `waiver_exempt`,
    `waiver_tl`), TANF implementation and time limits.
  - Design: a triple difference of single vs married mothers × exemption months × state and year.
  - Within single mothers, compare by the age of the youngest child relative to the state's exemption threshold:
    a mother whose infant is 4 months old in a 3-month state is subject to the requirement, while the same mother
    in a 12-month state is not.
  - State × year fixed effects absorb all common shocks; the comparison is across child ages within a state-year.
- **Outcomes.**
  - First stage (CPS ASEC, PSID): employment and welfare receipt of single mothers by the age of the youngest
    child.
  - Children (PSID CDS): Woodcock–Johnson scores and the BPI for children born 1990–2001 (CDS 1997/2002/2007).
  - NLSY79 Children: excluded from the state design (no public state); it serves only for the time-use and
    test-score mapping.
- **Threats.**
  - States chose exemptions endogenously, e.g. strict states may be those with improving labour markets. The
    within-state-year comparison by child age deals with this.
  - The composition of single motherhood may respond (marriage and fertility). The companion paper's DDD found
    no fertility response to AFDC generosity (`paper/sec3b_fertility_marriage.tex`, Section `fm_welfare`). Repeat
    that check for exemptions.
  - Differential trends for single mothers in the 1990s, from the EITC expansions (state EITC is in the calendar)
    and the boom. Control with state × year × marital-status trends and with EITC exposure.
- **What the model adds.** Design B's first stage becomes a validation target for counterfactual (iii) of Design
  A. The model translates "months at home in the first year" into children's skills and adult earnings, and says
  how much of the effect runs through time and how much through money (the floor kept).
- **Feasibility.**
  - CPS: about 140 Black and 190–280 White single mothers with a child under 1 per ASEC year in 1990–2006
    (≈ 2,300 Black + 3,800 White in total; more with youngest child 0–2).
  - PSID CDS children born 1991–1998: 705 Black and 844 White, of whom 33–39% of the Black and 7–12% of the White
    children had AFDC/TANF in the family at ages 0–5.
  - The PSID first stage is small; the CPS carries it.
  - Clearly feasible for the first stage; the CDS outcome stage is borderline (see the go/no-go).

### Design C — EITC money vs mothers' time in the NLSY79 Children file (Dahl–Lochner with a time channel)

- **Question.** The EITC raises income *and* single mothers' employment, so part of what it does to children may
  come from less time with the mother. How much of the EITC's effect on test scores is money, and how much is
  offset by time?
- **Why it matters.** It would be the first direct split of the Dahl–Lochner effect into money and time. It fits
  Phase 2/4 of *Money or Time?* (it supplies the skill technology). Stand-alone: field journal.
- **Identification.** The Dahl–Lochner simulated federal EITC instrument (schedule × number of children × year ×
  lagged income) for family income. Mother's months worked in the child's first years are instrumented by
  something orthogonal: the FMLA eligibility of `12.FMLA.py`, or birth-month timing relative to the 1993–96
  phase-in. Federal variation only, so the lack of public state data in the NLSY79 does not matter.
- **Outcomes.** PIAT math and reading, PPVT, BPI by age band (from `10.CYAOutcomes.py`, being built); young-adult
  earnings at 26–35.
- **Threats.**
  - The simulated instrument relies on family size, which is endogenous; follow Dahl–Lochner, who use lagged
    family size.
  - A second instrument for time is needed or the split is not identified. FMLA eligibility is the candidate,
    but it acts on married, employed mothers more than on EITC-eligible single mothers.
- **Feasibility.** The CYA has 11,551 children: 3,196 Black, 6,131 non-Black non-Hispanic (including the poor-White
  oversample) and 2,224 Hispanic. Dahl–Lochner worked with about 4,500. Feasible; the binding constraint is the
  second instrument.

### Design D — The floor as insurance against the husband: UI generosity, fathers' job loss and children

- **Question.** When the father loses his job, does a more generous safety net (state UI for him, the floor for
  her) shrink the effect on his children's adult earnings, and does it let the mother stay home with an infant?
- **Mechanism.** In the model, $b$ and $b_m$ insure the family against $e_m = 0$. Generous UI weakens the
  insurance motive that holds wives at work (Cullen–Gruber) and cushions the income loss that hurts sons
  (Oreopoulos et al.).
- **Identification.** PSID fathers' job losses × state UI maximum weekly benefit / replacement rate × year. **UI
  variables are not in UKCPR or `policy_calendar.csv`** and need external DOL data ("Significant Provisions of
  State UI Laws"). This is already Phase 3 row `15.UIHusbands.py` of the plan.
- **Feasibility.** PSID fathers' displacement events while the child is 0–17 number a few hundred per race. Power
  is weak for adult outcomes and better for CDS outcomes and the mother's first stage. It belongs in *Money or
  Time?* Phase 3, **not** as a separate paper.

### Design E — Long-run exposure à la Bastian–Michelmore / Hoynes et al. in the PSID (replication + race; not recommended as the lead)

- **Question.** Replicate the PSID long-run EITC and AFDC exposure designs and report them by race and at a given
  parental income: does childhood safety-net generosity change the IGE slope or the racial intercept gap?
- **Why not lead with it.** It has been done in the PSID (Bastian–Michelmore; McInnis et al.; Hartley et al.),
  without county codes we cannot use the Food Stamp roll-out, and Section 3.4 shows it is badly confounded and
  underpowered by race. Its value is as an appendix: a racial split of known designs and a link to our IGE
  estimates.
- **Better data route (later).** ACS with **state of birth** × cohort (a new IPUMS USA extract with `BPL`,
  `BIRTHYR`, education, earnings, and race 2005–2023; `IPUMS_API_KEY` is set) gives millions of adults exposed to
  state EITCs and AFDC levels by state of birth. That is enough power for a race × parental-proxy design, but
  without parental income it gives no IGE. It suits a separate descriptive paper or an appendix, not the core.

---

## 3. Feasibility checks (run 2026-10-17, read-only)

Helper scripts are in the session scratchpad (`child_state.py`, `kids_exposure.py`, `power.py`, `cds_count.py`,
`cps_count.py`); nothing was written to `IGE/`. PSID counts are **unweighted**, so the SEO sample makes Black
children poorer on average than the Black population.

### 3.1 PSID children with adult outcomes (`data/psid_kids.pkl`, 20,402 children; 9,326 Black, 10,343 White)

Children with adult earnings (`n_earn` ≥ 1, ages 25–55, mean age at measurement shown):

| Birth cohort | Black | White | Mean age of earnings |
|---|---|---|---|
| 1950–64 | 1,725 | 2,061 | 35 |
| 1965–74 | 568 | 983 | 35–37 |
| 1975–79 | 346 | 591 | 35.0 |
| 1980–84 | 469 | 640 | 33.0 |
| 1985–89 | 456 | 509 | 30.9 |
| 1990–94 | 320 | 392 | 28.4 |
| 1995+ | 0 | 0 | — |

- **Observed from early childhood** (≥ 4 waves at ages 0–5) **and** with adult earnings: 1,726 Black and 2,769
  White in cohorts 1965–94. In the UKCPR era (born 1975–94) that is **1,277 Black and 1,932 White**.
- Cohorts exposed to the 1996 reform in early childhood (born 1991–98) have almost no adult outcomes yet. For them
  the outcome must be **CDS test scores**.

### 3.2 Policy variation on disk

- **UKCPR** (`ExternalData/ukcpr_...xlsx`, sheet `Data`, 2,295 state-years 1980–2024, 75 columns). It has:
  - AFDC/TANF maximum benefit for 2/3/4 persons (1980–2023);
  - SNAP maximum benefit (1980–2024) and AFDC/TANF + FS combined;
  - federal EITC phase-in / maximum / phase-out by number of children (1980–2024);
  - state EITC rate and refundability (1980–2023);
  - state and federal minimum wage, unemployment rate;
  - caseloads (AFDC/TANF, SNAP), SSI levels (state supplement to 2011);
  - counts of Medicaid beneficiaries, WIC and school-lunch participation (1989/90+);
  - the share of the year with the ACA expansion.

  It has **no** Medicaid/CHIP income-eligibility thresholds, **no** UI generosity and **no** waiver dates.
- **`data/policy_calendar.csv`** (another agent's file, read only; 2,295 state-years, 66 columns) adds:
  - AFDC waiver dates by type (any, work requirement, exemption, time limit, sanction, earnings disregard, family
    cap);
  - TANF official and actual dates; time limits (months, type);
  - **work-requirement exemption by age of the youngest child (`work_exempt_m`, 0–48 months, 1,706 state-years)**;
  - FMLA, state maternity and paternity leave, and paid family leave.

  Still missing: UI (DOL), Medicaid/CHIP thresholds (would need an external source), SNAP rule changes
  (broad-based categorical eligibility, ABAWD waivers; USDA SNAP Policy Database, external).
- **State EITCs.** 1 state in 1984; 5 in 1990; 7 in 1994; 15 in 2000; 23 in 2009; 31 in 2023. Federal maximum
  credit (2 children): $500 (1980) → $953 (1990) → $2,528 (1994) → $3,556 (1996) → $5,028 (2009).
- **Variation left after fixed effects.**

  | Measure | Raw s.d. | s.d. after FE |
  |---|---|---|
  | Log AFDC 3-person benefit, 1980–96, state + year FE | 0.423 | 0.069 |
  | Log AFDC + FS combined, 1980–96 | 0.258 | **0.032** (SNAP offsets AFDC) |
  | Log AFDC, 1980–2019 | — | 0.099 |
  | Children's average log AFDC + FS benefit at ages 0–5, birth-state + cohort FE | 0.249 | 0.057 |
  | Same, cash only | 0.458 | 0.121 |
  | Children's mean state EITC rate at 0–17 | 0.055 | 0.029 |

  In 1990 the AFDC benefit for a family of three ran from $118 (AL) to $846 (AK), median $364; AFDC + FS ran from
  $378 to $1,067.

### 3.3 PSID program receipt (family files 1968–2023, labels read from the `.do` files)

- **AFDC/TANF.** Head + wife amount every wave 1968–2023: combined H+W amount through 1985, separate head and wife
  amounts 1986–93, and whether-received plus amount by head/RP and wife/spouse from 1994. Monthly receipt flags
  from 1984.
- **Food stamps.** Annual value in 1975–76 and 1982–2023, with monthly flags from 1987. Bonus-value variables in
  1977–80 are not yet mapped cleanly, and there is no clean annual variable in 1968–74 or 1981. SSI from 1975; UI
  head/wife throughout.
- **EITC.** Not reported in any wave; it has to be **simulated** (NBER TAXSIM, or the UKCPR schedule applied to
  PSID earnings and number of children).
- **Medicaid.** Only scattered items (births paid by Medicaid in 1985–87, applications in 1999–2001).
- **State.** Every wave (PSID codes; FIPS from 1985). The state + county field (e.g. 1985 `V11105`) is
  **all zeros** in the public files, so there is no county.
- **Share of family-waves with AFDC/TANF:** 5–7% in 1968–1997, 2.8% in 1999, 0.7–0.8% in 2019–23. With food
  stamps: 12–17% in 1982–97, 8–9% in 1999–2003, 16–21% in 2009–23.
- **Childhood receipt** for children with adult earnings (unweighted):

  | | Any AFDC at 0–17 | Any AFDC at 0–5 | Share of childhood years on AFDC | Any food stamps (in covered waves) |
  |---|---|---|---|---|
  | Black | 45.8% | 37.0% | 21.7% | 64.5% |
  | White | 9.7% | 7.5% | 3.2% | 19.4% |

- **Mobility.** 14.7% of Black and 22.5% of White children lived in more than one state at 0–17, so state of
  residence is not the same as state of birth.

### 3.4 Power check: long-run exposure regressions in the PSID (illustrative, not evidence)

These are OLS regressions of the child's log lifetime earnings on childhood policy exposure. Controls: log
parental income (12–17 mean), sex, race (pooled column), and the state unemployment rate at 0–5 (AFDC rows).
Fixed effects for state of first childhood residence and birth year; standard errors clustered by that state;
coefficients per log point (AFDC) or per unit of the state EITC rate.

| Treatment | Sample | Coef. | s.e. | Stars | p | N |
|---|---|---|---|---|---|---|
| Mean log AFDC+FS benefit, ages 0–5 | all | −0.705 | 0.258 | *** | 0.006 | 2,675 |
| × low parental income (bottom half) | all | −0.135 | 0.127 | | 0.289 | 2,675 |
| Mean log AFDC+FS benefit, ages 0–5 | Black | −0.696 | 0.572 | | 0.224 | 1,104 |
| × low parental income | Black | +0.029 | 0.218 | | 0.895 | 1,104 |
| Mean log AFDC+FS benefit, ages 0–5 | White | −0.585 | 0.389 | | 0.132 | 1,571 |
| × low parental income | White | −0.129 | 0.211 | | 0.540 | 1,571 |
| Mean state EITC rate, ages 0–17 | all | +0.789 | 0.467 | * | 0.091 | 3,710 |
| × low parental income | all | −0.186 | 0.564 | | 0.741 | 3,710 |
| Mean state EITC rate, ages 0–17 | Black | +0.139 | 0.713 | | 0.845 | 1,473 |
| × low parental income | Black | −0.240 | 0.661 | | 0.717 | 1,473 |
| Mean state EITC rate, ages 0–17 | White | +1.070 | 0.573 | * | 0.062 | 2,237 |
| × low parental income | White | +1.363 | 0.775 | * | 0.079 | 2,237 |

What the table shows:
- The main AFDC effect has the **wrong sign** (−7% earnings per 10% more benefit) and is implausibly large. It is
  the same confounding as the two-way FE estimates in `paper/sec3b_fertility_marriage.tex` (Section `fm_welfare`):
  state benefit paths move with state conditions.
- The within-state-cohort comparison of low- vs high-income children is the credible one. It is centred near zero,
  with a 95% CI of [−3.8%, +1.1%] earnings per 10% higher benefit.
- The state EITC estimates are too large to be believed (+8% per 10 pp of state rate) and noisy.
- Bottom line: **PSID-only long-run state-policy designs cannot identify effects of plausible size by race.** That
  rules out Design E as the lead and pushes the reduced form toward first stages (CPS) and short-run outcomes
  (CDS).

### 3.5 Short-run outcomes and first-stage data

- **PSID CDS** (`data/cds_scores.pkl`, from `9a.CDS.py`), with WJ scores, race from the head:
  - by wave: 1997: 962 Black, 1,066 White; 2002: 1,104 / 1,291; 2007: 624 / 746; 2014: 780 / 569;
    2019: 569 / 507;
  - distinct children: 2,508 Black, 2,516 White;
  - by birth cohort: 1986–90: 509 / 573; 1991–94: 454 / 515; 1995–98: 251 / 329;
  - any AFDC/TANF in the family at ages 0–5: Black 38–39% (born 1981–94), 33% (1995–98), 22% (1999–2005); White
    7–12%.
- **NLSY79 Children** (public CYA, 11,551 children; by birth year 1971–80: 2,357; 1981–85: 3,465; 1986–90: 2,948;
  1991–95: 1,722): federal-only designs (Design C). Mothers' monthly AFDC/FS is in the NLSY79 extract
  (`NLSY79/4.ExtractFamily.py`).
- **CPS ASEC (IPUMS `cps_1`, 1968–2024, ages 16–64).** Has `STATEFIP`, `INCWELFR`, `EITCRED` (1992+), `NCHILD`,
  `YNGCH`, `EMPSTAT`, `FTOTVAL`.
  - Single mothers aged 16–49 with a child under 1, unweighted N per year: Black 126–158 and White 91–322 across
    1968–2015.
  - Share of those single mothers with welfare income (weighted):

    | Period | Black | White |
    |---|---|---|
    | 1990–97 | 51.5% | 37.2% |
    | 1998–2006 | 26.2% | 16.6% |
    | 2007–15 | 15.7% | 7.9% |

  - Share of single mothers with a positive imputed EITC: 1998–2006 Black 53.1%, White 47.7%; 2016–24 Black 52.5%,
    White 43.7%.
- **`CPS/cps_asec_eitc_2005_2021.parquet`** is a narrow file: columns `year`, `fips`, `eitc`, `hh_income`, `w`
  only (read from the parquet footer; **pyarrow is not installed in `.venv`**, so the row count was not read). It
  is useful for state-year EITC incidence after 2005 and nothing else.

### 3.6 Helper snippets

```python
# PSID state + AFDC receipt per family-wave (child_state.py, abbreviated)
st = [v for v, l in labs if re.search(r'^(STATE \(68\)|STATE NOW|CURRENT STATE|PSID STATE OF RESIDENCE CODE)', l.strip())]
if wave >= 1994: st = [v for v, l in labs if 'PSID STATE OF RESIDENCE' in l]          # PSID codes, alphabetical, DC=8, AK=50, HI=51
afdc = (amounts > 0) if wave <= 1993 else (whether_head == 1) | (whether_wife == 1)  # H+W amount <=1985; HD/WF 1986-93
# link: data/psid_person_year.pkl on (wave, int); child age = wave - birth_year; receipt refers to wave - 1
PS = "AL AZ AR CA CO CT DE DC FL GA ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY AK HI".split()
```

```python
# power check (power.py, abbreviated)
f = 'log_earn ~ ben05*low + ur05 + lpinc_av + female + C(st0) + C(birth_year)'
smf.ols(f, d).fit(cov_type='cluster', cov_kwds={'groups': pd.factorize(d.st0)[0]})
```

---

## 4. Recommendation

### 4.1 Best design: fold it into *Money or Time?*

Do **not** start a separate reduced-form "safety net and IGE" paper. Our data cannot beat Bailey et al. (linked
Census–SSA) or replicate Hoynes et al. (needs county). The PSID power check shows the long-run state-exposure
design cannot identify plausible effects by race. Instead:

1. **Design B** becomes the policy section of *Money or Time?* (Phase 3, `14.WelfareReform.py`). The infant
   work-requirement exemption is the safety-net analogue of paid leave: it buys a mother time with the infant
   without the loss of income, and with a search friction it decides whether she keeps the floor. It provides the
   second identified time-versus-money margin next to FMLA.
2. **Design A** becomes the main counterfactual of Phase 4: floor vs EITC vs work requirement vs time limit, by
   race, with the friction switched on and off. This is the part no paper has, and the part that can make a REStud
   case. If Design B's first stage is strong and differs by race, as the friction predicts, Design A can later be
   split off as a second paper ("Who does work-conditioned support reach? Search frictions, the 1990s reforms and
   the racial mobility gap").
3. Designs C and D are already near Phase 2/3 tasks. Design E goes to an appendix at most.

### 4.2 Phased work plan (scripts to write; no data written outside `data`, `output`)

| Phase | Script | Content | Time |
|---|---|---|---|
| 0 | `IGE/14a.PSIDChildPolicy.py` | Child × age panel: state of residence, AFDC/TANF and FS receipt and amounts, simulated federal + state EITC (UKCPR schedule × PSID earnings × number of children), policy calendar merged | 2–3 days |
| 1 (gate) | `IGE/14.WelfareReform.py` part 1 | CPS ASEC 1988–2006 first stage: employment and welfare income of single mothers by age of the youngest child × `work_exempt_m`; triple difference (single vs married; child age above vs below the exemption) with state × year FE; by race | 3–4 days |
| 2 | `14.WelfareReform.py` part 2 | PSID births 1990–2003: mother's employment and receipt in the child's first 2 years (same design, smaller N); CDS WJ/BPI reduced form (children born 1990–2001) | 1 week |
| 3 | `15.UIHusbands.py` (Design D) + `IGE/11.ChildEffects.py` EITC block (Design C) | External DOL UI data; Dahl–Lochner instrument in the CYA | 2 weeks |
| 4 | estimation code (companion repo) | Add to the model: an EITC schedule on her earnings, a work/search condition on $b$ by youngest-child age, a time limit (a state for months used), and a take-up cost. Validate on the 1993–2000 CPS changes by race and on Phase 1's first stage, without re-estimation. Counterfactuals (i)–(v) once the skill block exists | 3–6 weeks after the companion estimates are frozen |
| 5 | paper | One subsection "Work requirements and the infant exemption" in the policy section; details in footnotes; PSID-motivated choices footnoted with numbers + script | — |

### 4.3 Go/no-go test (a few days, Phase 1)

**Test.** CPS ASEC 1988–2006 (IPUMS `cps_1`), women aged 18–45 with children, Black and White non-Hispanic.

- Outcome: employed last year (`WKSWORK1` > 0) and, separately, welfare income (`INCWELFR` > 0).
- Regressor: an indicator for "youngest child's age (from `YNGCH`) is below the state's `work_exempt_m`
  threshold in that year", interacted with being unmarried. Before waivers, the counterfactual threshold is ∞:
  everyone is exempt under AFDC (the JOBS program of the 1988 Family Support Act exempted mothers of children under
  3, with a state option to go down to 1; this is from memory and *unverified* here, so check it against the ASPE
  source behind `work_exempt_m`).
- Fixed effects: state × year, child age × year, single × year, single × state.
- Standard errors clustered by state.
- Run by race and pooled; report coefficient, s.e., stars and p.

**GO if all three hold:**
1. Being exempt lowers single mothers' employment and raises welfare receipt, both with p < 0.05 pooled. The
   expected magnitude, from the 1990s literature, is a few percentage points; the first stage needs F > 10.
2. The placebo on married mothers, who are not eligible, is near zero, p > 0.1.
3. The PSID CDS minimum detectable effect, given (1), is ≤ 0.15 s.d. on WJ scores for children born 1990–2001.
   Compute it from the first-stage size and the 1,549 CDS children born 1991–98, which gives roughly 0.2 s.d. at
   80% power for a full-exposure contrast. If the MDE is above that, use NLSY79 Children for the skill mapping
   and keep the CDS result as a bound.

**Racial split.** The friction predicts a larger welfare-exit response for Black single mothers but a smaller
employment response (searchers who do not find work). That pattern is the evidence Design A needs. Finding it is
the signal to plan Design A as a separate paper.

**NO-GO.** If the first stage is null or the placebo fails, drop Design B as an identification source, keep the
safety net only as a mediator in the BFHO decomposition (childhood receipt, Section 3.3) plus model
counterfactuals, and do not write a separate safety-net paper.
