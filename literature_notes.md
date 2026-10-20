# Literature notes for "Money or Time?" (IGE paper)

Technical summaries of the six papers in `Literature/`, written 2026-10-17. All six PDFs were read in full: main text, appendices and, for Gayle–Golan–Soytas, the supplementary appendix of first-stage tables. Every number below comes from the paper, with its table, figure or page. Where I derive a number myself from reported parameters, the note says so ("my calculation"). Page numbers are PDF pages unless a journal page is given.

When these notes refer to our own model, they use the terms *search friction* and *human capital level / accumulation / depreciation*.

---

## Gayle, Golan & Soytas (2015), "What Accounts for the Racial Gap in Time Allocation and Intergenerational Transmission of Human Capital?" (Federal Reserve Bank of St. Louis Working Paper 2015-018A) — file: 2015-018.pdf

(The cover says August 2015, the paper is dated 27 February 2015 and the supplementary appendix 15 October 2014.)

### 1. Question and contribution
Why do Black and white children differ in completed education, and how much of that gap runs through parents' early-childhood time? The authors build and estimate a **dynastic life-cycle model**: Barro–Becker altruism with endogenous fertility, life-cycle choices in each generation, two-person households, and stochastic marriage and divorce. Parents choose labor supply, time with children under six and births. Children's education depends on both parents' time and money in the first five years. Married couples play a **non-cooperative complete-information dynamic game**. The paper claims to be the first to estimate a dynamic complete-information game; equilibrium existence comes from supermodularity.

The headline result: racial gaps in assortative mating and divorce account for more of the Black–white education gap than the racial earnings gap does (abstract; p. 4).

### 2. Data and sample
- **PSID Family-Individual File, 1968–1996/97.** The sample keeps heads, wives, sons and daughters. Sons and daughters under 17 are dropped. This leaves 12,051 men and 17,744 women, or 423,631 person-years.
- Only white and Black individuals aged 17–55 are kept. The earnings equation needs four lags of participation, so the sample keeps only people with at least five consecutive observations, leaving 139,827 person-years.
- Parents observed only after the child is 16, parents with gaps in the child's first 16 years, and married people with missing spouse data are all dropped (p. 5).
- Table 1 sample: 115,280 person-years and 12,318 individuals (6,813 parents and 5,505 children). The share Black is 0.202 among parents and 0.286 among children. Money is in 2005 dollars.
- **Parents are linked to children** through PSID family relationships; children are observed into adulthood (at least age 17). The child outcome is completed education in four categories: less than high school (LHS), high school (HS), some college (SC), college (COL).
- **Parental time with children.** The PSID has no child-care hours, so time is *imputed*: annual housework hours minus the mean housework of childless people of the same gender, education and year. Negative values are set to 0, and people without children get 0. The measure is then **discretized** into none / low / high, splitting at the gender-specific median (pp. 6, 20).
  - Validation: the race and marital-status patterns match ATUS time diaries (Fig. 1).
  - Time is summed over the child's first five years. Each child under 6 in the household is assigned the household average (p. 21).
- **Measurement error.** No reliability correction is applied. The authors argue that discretization "reduces the problem" (p. 6).
- **Labor supply** is discretized as none (<3 h/week), part-time (3–20 h/week) and full-time (>20 h/week) (p. 20).

### 3. Empirical / econometric approach
The model is estimated in **two stages**, based on conditional choice probabilities (CCPs).

**Stage 1** estimates CCPs and best-response probabilities, the marriage and divorce transitions, and the spouse-matching functions (logits, supplementary Tables 3-A to 25-A). It also estimates the **earnings equation** with correlated individual effects:

$$\ln w_t=\theta' z_t+\sum_{s=0}^{4}\alpha^{p}_{s}\,\mathbb 1[\text{PT}_{t-s}]+\sum_{s=1}^{4}\alpha^{f}_{s}\,\mathbb 1[\text{FT}_{t-s}]+\eta,$$

Here $\eta$ is a parametric function of race, sex and education (Hausman statistic 2,296; Table 4).

Stage 1 also estimates the **education production function** as linear-probability equations by **three-stage least squares (3SLS)**:
- Regressors: each parent's summed time in years 0–5, each parent's labor income in years 0–5, parents' education, child sex and race, and siblings under 3 and aged 3–6.
- Instruments: parents' labor-market hours over the child's early years (the text says the first 5 years, the Table 5A note says the first 8) and parents' age, linear and squared, at the child's fifth birthday (Table 5A; Table 2-A).
- Identification argument: inputs are "predetermined" relative to an outcome realized a generation later (p. 30).

**Stage 2** is GMM on Hotz–Miller inversions with type-I extreme-value shocks. For couples the moment conditions use best-response differences:

$$v_{k,k'}(z)-v_{0,k'}(z)-\ln\frac{p_{k,k'}(z)}{p_{0,0}(z)}=0 .$$

- There are 286 orthogonality conditions per age (eqs. 47–50).
- The infinite-horizon dynastic continuation value is written as a matrix inversion in the CCPs, $V=\{I-\delta^{T}\ldots\}^{-1}\ldots$ (eq. 45). This turns the problem into a finite-horizon one solved backward.
- Estimation uses ages 25–40. The over-identifying J-test does not reject (p. 33).

**Identification** (pp. 24–26): utility is identified given the shock distribution and the discount factors (Magnac–Thesmar; Pesendorfer–Schmidt-Dengler). Two further assumptions are needed:
- utility from leisure and consumption does not depend on marital status, which separates the sharing rule;
- the per-period payoff depends on the spouse's actions only through transfers and children.

The time discount factor is identified from childless women near the end of life. The intergenerational discount factors are identified from the exclusion that past home hours affect only transitions, not current utility (Fang–Wang).

### 4. Model
- **Agents and timing.** $T=39$ annual periods (ages 17–55); everyone starts single. Women choose among 16 options: {none, PT, FT} work × {none, low, high} time with children × birth (Table 3). Men choose among 9. Marriage and divorce are not choices; they follow stochastic transitions that depend on the state and on past choices, and a spouse is drawn from an exogenous matching function $G(z_{-}\mid z)$.
- **Preferences.** Utility is linear in consumption (risk neutrality). Each discrete choice has its own utility $\psi^{k}$, which proxies for non-pecuniary costs or benefits including leisure. Shocks are type-I extreme value. Altruism follows Barro–Becker:

$$U_g=U^T_g+\delta^{T}\,\lambda N^{-\nu}\sum_{n=1}^{N}U_{g+1,n}.$$

- **Budget.** There is **no borrowing or saving.** Child costs are proportional to earnings and the number of children, $\pi_c(z)(N_t+b_t)w_t$. Because consumption and child expenditure are not observed, the child-cost coefficients are *net* utility from children, interacted with education, race and marital status (eqs. 36, 39).
- **Couples.** The sharing rule is exogenous, in the style of Blundell–Chiappori–Meghir (eq. 38), and depends on race, education, own wage, the relative wage and children. Non-custodial parents provide no time or money.
- **Child technology.** $M(x'\mid z_{T+1})=\Pr(\text{Ed}'\mid z_{T+1})\Pr(\text{skill}'\mid \text{Ed}')$. Race passes automatically to the child, and interracial marriage is ruled out.
- **Equilibrium.** A Markov perfect equilibrium in pure strategies exists if the education production function has increasing differences in the two parents' investments (Assumption 1, Proposition 1). Counterfactuals use the Pareto-best equilibrium.

**Key estimates**

| Object | Estimate | Source |
|---|---|---|
| Earnings: current full-time | 0.938 | Table 4 |
| Earnings: lagged FT, lags 1–4 | 0.160, 0.044, 0.025, 0.040 | Table 4 |
| Earnings: lagged PT for men, lags 1–3 | −0.087, −0.077, −0.070 | Table 4 |
| Earnings: lag-1 PT for women (extra) | +0.150 | Table 4 |
| Correlated fixed effect: Black / female | −0.154 / −0.484 | Table 4 |
| Earnings growth with age: college vs less than HS | 0.096 vs 0.037 | Table 4 |
| Mother's time → some college / college | 0.080 (0.034) / 0.069 (0.027) | Table 5A |
| Father's time → some college / high school | 0.100 (0.029) / 0.031 (0.019) | Table 5A |
| Mother's early labor income → HS equation | −0.025 (0.009) | Table 5A |
| Father's early labor income | ≈0 | Table 5A |
| Black, conditional on inputs | insignificant (0.020, 0.082, 0.043) | Table 5A |
| Siblings under 3 → some college | −0.107 (0.027) | Table 5A |
| Discount factors: time $\delta$ / intergenerational $\lambda$ / number of children $\nu$ | 0.710 / 0.421 / 0.376 | Table 6B |

The education equations use N = 1,335. A $\nu$ of 0.376 gives marginal values of 0.54 for the second child and 0.44 for the third (p. 31).

Predicted education distribution for a white boy (Table 5B):

| Parents (both) | Time input | Education distribution |
|---|---|---|
| Less than HS | none | 20.2% LHS / 79.8% HS |
| Less than HS | sample average | 11.5% LHS / 23.5% HS / 49.2% SC / 15.9% COL |
| Less than HS | maximum | 63.2% college |
| College | average | 43.2% college |
| College | maximum | 90.6% college |

### 5. Main findings
**Descriptive facts**
- 69% of Black children under 6 have a single mother, against 13% of white children (fn. 9).
- Married Black mothers spend about 180 h/yr less with young children than married white mothers (p. 7). In Table 2A the figures are 250.3 vs 331.0 h.
- Married Black mothers work 1,332 h vs 1,209 h, at a wage $1.7 lower (11.1 vs 12.8). Their earnings are about the same as married white mothers' (18,180 vs 19,364) (Table 2A, p. 7).
- Married Black men earn 35,824 vs 51,072 and spend slightly more time with children (99.1 vs 86.0 h).
- Among college-educated couples, Black wives work 1,709 h vs 1,100 h and earn 42,650 vs 26,668 (Table 2B).
- 63% of white college women have a college-graduate husband, against 30% of Black college women (p. 8).
- Whites are about twice as likely to marry, and Blacks more than twice as likely to divorce (Fig. 2).

**Counterfactuals** (Tables 8–9). Each column gives Black families one white market. Mothers' and fathers' time are summed time indices over the first five years.

| Outcome | White | Black | (1) White earnings | (2) White matching | (3) White marriage probability | (4) White divorce probability |
|---|---|---|---|---|---|---|
| Mother's time, total | 9.64 | 7.94 | 8.06 | 7.82 | 11.87 | 8.47 |
| Father's time per child | 3.54 | 3.61 | 3.76 | 4.29 | 2.53 | 3.71 |
| Child college completion | 0.235 | 0.146 | 0.148 | 0.174 | 0.136 | 0.169 |

- Raising Black marriage rates to white rates (3) closes the maternal-time gap but *lowers* children's education. Mothers specialize more and fathers' time falls (p. 36).
- White matching (2) has the largest effect, and white divorce probabilities (4) the second largest.
- White earnings (1) raise lifetime earnings of Black boys from 1,033,688 to 1,329,949, above the white benchmark of 1,220,075, mainly through more labor supply (Table 9).

### 6. Robustness and limitations
**Stated by the authors**
- The model is risk-neutral with no saving and "ignore[s] the insurance aspects of marriage and divorce" (p. 22).
- The sharing rule and the matching function are exogenous.
- Non-custodial parents provide no inputs.
- Unobserved heterogeneity is only a correlated fixed effect in earnings.
- Time with children is imputed from housework.
- The model fit is imperfect. It under-predicts full-time work for singles and mis-fits fertility for single women by race (Figs. 4–6).

**My assessment**
- Identifying the time effect by 3SLS with the parent's *own* hours and age as instruments is weak. Hours directly reduce time and raise income, so the exclusion restriction is doubtful.
- The housework-deviation measure is noisy and mechanically linked to fertility.
- Linear probabilities produce boundary predictions (0% and 63.2% in Table 5B).
- The text and tables disagree in places (5 vs 8 years of hours as instruments; the column layout of Table 7 is ambiguous). Read Table 7 with care.
- With no saving and risk neutrality, labor supply cannot be a response to husbands' income risk. That is exactly the channel our companion paper emphasizes.

### 7. Findings relevant for us
- **Motivating facts for both papers.** Married Black mothers work more hours than married white mothers (1,332 vs 1,209) and spend less time with young children (250 vs 331 h/yr), while the racial wage gap is far larger for husbands (Table 2A). This is the companion paper's "Black mothers work more" pattern in an older PSID window (1968–97), and it already links that labor supply to children's time.
- **External benchmark for our child block.** Mother's early time raises the probability of some college by 0.080 and of college by 0.069 per unit of a 0–10 time index (Table 5A). Father's time matters at the bottom of the distribution. Use these to sanity-check the sign and size of the model-implied effects of a mother leaving work at a birth, but keep in mind the weak identification.
- **Early income does not matter conditional on time and parental education** (Table 5A; p. 4). This favors the "time" side of "Money or Time?". Contrast it with Bolt et al. (BFHO), where parental income does enter investments.
- **The counterfactual design is a template.** "Give Black families white marriage / matching / divorce / earnings" is close to our decomposition by causes and routes. Their finding that marriage-rate changes trigger offsetting specialization is a warning for our marriage-related counterfactuals.
- **Earnings dynamics benchmarks.** Lagged part-time experience is penalized for men but rewarded for women at the first lag (Table 4). This parallels our human capital accumulation with separate FT and PT rates plus depreciation.

### 8. Technical modeling / measurement choices relevant for us
- **Copy**
  - The counterfactual structure: swap race-specific primitives (earnings, marriage probability, matching, divorce) one at a time.
  - The discrete time-input choice (none / low / high) attached to discrete labor supply. Our NW/PT/FT choice could carry an implied time input, $\tau=T-h$, without adding a choice dimension.
  - The two-generation steady state written as a CCP matrix inversion (eq. 45). This is a cheap way to obtain a model-implied IGE without solving an infinite-horizon dynasty, if we go dynastic.
- **Avoid**
  - Linear utility and no saving. Our model has savings, a safety-net floor and husbands' risk; the insurance motive is our contribution and must stay.
  - Imputing time from housework deviations. Use the NLSY79 weekly employment arrays (months not working in year 1) and CDS time diaries instead.
  - 3SLS with parents' own hours as instruments. Use the planned gender-specific Bartik shocks at the birth (`PLAN.md` Phase 1).
- **Where it plugs in**
  - The child block (PLAN Phase 4): the education production function as a function of maternal and paternal time in years 0–5 and income is the closest structural precedent with race and marriage.
  - The counterfactual table in `estimation/decomposition.py`: their counterfactuals (1)–(4) map onto our earnings, matching and divorce switches.

---

## Fagereng, Mogstad & Rønning (2021), "Why Do Wealthy Parents Have Wealthy Children?" (Journal of Political Economy 129(3): 703–756) — file: 712446.pdf

### 1. Question and contribution
How much of the intergenerational correlation in wealth, and in investor behavior, is causal family environment rather than inherited traits? The paper uses the Sacerdote (2007) design: Korean-born children placed with Norwegian families by first-come-first-served queuing, which makes assignment quasi-random given the time of application.

Contributions:
- causal estimates of wealth transmission and of transmission of stock-market participation and risky share;
- a comparison with own-birth children;
- a Heckman–Pinto mediation analysis;
- external-validity checks;
- an extended ACE behavioral-genetics decomposition that allows gene–environment correlation.

### 2. Data and sample
- **Data.** Norwegian registers, including the adoption register since 1965, linked to tax records (1994–2014) that cover income and most assets and liabilities, and to the Land Register for housing transactions.
- **Net wealth** is financial plus non-financial assets minus debt, with housing valued from transactions and hedonic indexes (Eika, Mogstad & Vestad 2020). It is validated against the 2004 survey (App. A; Fig. A1).
- **Financial wealth** (deposits, bonds, stocks, mutual and money-market funds) is third-party reported.
- **Sample.** 2,254 Korean adoptees born 1965–1986 and adopted at 18 months or younger, and 1,206,650 non-adoptees born in the same years (Table 1).
- **Measurement.**
  - Parents' wealth is averaged over 1994–96 (mean age 48) and children's over 2012–14 (mean age 35.8).
  - Wealth is measured at the household level; the top and bottom 0.1% are winsorized.
  - Money is in 2014 USD.
  - The 3-year averages are meant to reduce transitory variation (p. 709).
- **Linking.** Parents are identified as the adoptive parents in the register. Standard errors are clustered by mother.

### 3. Empirical / econometric approach
The baseline regression (eq. 1) is

$$Y_i=\sum_k a_k Z_{k,i}+\beta W_{j(i)}+X'_{j(i)}\eta+\gamma\kappa_{j(i)}+X_i'\lambda+\delta\xi_i+u_i .$$

Here $Z$ are adoption-year dummies. Under conditional random assignment, the family components ($W$, $X_j$, $\kappa_j$) are independent of the child's traits ($X_i$, $\xi_i$). OLS among adoptees then gives the **total effect** of being placed with a wealthier family (without $X_j$) and the **partial effect** (with $X_j$). It does *not* identify the effect of an exogenous increase in wealth, because $W$ can still be correlated with unobserved family traits $\kappa_j$ (pp. 718–719).

**Balance tests** (Table 2). Adoptee age at adoption and gender are regressed on family wealth, schooling, income and the municipality's median income, given the adoption year. The joint F-test p-values are 0.540 and 0.956. Domestic adoptees, by contrast, fail the test (p = 0.000; Table B2).

**Mediation** (Heckman–Pinto; eqs. 2–7). The treatment-effect decomposition is

$$E[Y_{d'}-Y_d]=(d'-d)\tau+\sum_{j}\alpha^j_0(d'-d)m_{2,j}.$$

- The first term is the direct effect; the second is the indirect effect through measured mediators: child education, child income, financial literacy (a business or economics degree), and gifts and inheritances received.
- Identification assumes the unmeasured mediators are uncorrelated with the measured ones and with $X$.
- The test of $\alpha^p=0$ and $\beta=0$ gives p = 0.22.

**ACE models** (eqs. 8–16). Correlations between adoptive–biological, adoptive–adoptive and biological–biological sibling pairs identify the genetic, shared-environment and unexplained shares, and a gene–environment correlation $g$.

### 4. Model
There is no structural model. The mediation model is a linear potential-outcomes system; the ACE is a variance-components model.

### 5. Main findings
**Transmission of net wealth** (Table 3)

| Sample / specification | Coefficient |
|---|---|
| Adoptees: dollars per dollar of parental wealth | 0.225 (0.041) |
| Adoptees, with family controls | 0.204 (0.042) |
| Non-adoptees | 0.575 (0.011) |
| Non-adoptees, propensity-score matched | 0.548 |
| Same families: adoptees | 0.276 (0.139) |
| Same families: own-birth children | 0.468 (0.122) |

- The adoptee coefficient means a 10% wealthier family gives about 3.7% more wealth (p. 720).
- Other specifications for adoptees (Fig. 3; Table B5):
  - rank–rank slope 0.159 vs 0.244 for non-adoptees, and 0.167 conditional on gender and adoption year;
  - log–log elasticity 0.181 vs 0.23 for non-adoptees, but on 1,327 of 2,254 adoptees, because zero and negative wealth must be dropped (fn. 12).
- **Life-cycle checks** (Table B4). For adoptees the coefficient barely changes with the child's age: 0.215 at 35 or younger, 0.211 at 36–40, 0.261 above 40. For non-adoptees it rises with age: 0.462, 0.541, 0.653. Aligning the two generations' measurement ages does not change the results (Fig. B1).
- **Financial wealth and portfolios** (Table 4). Financial wealth 0.247 (0.049); stock-market participation on parents' participation 0.112 (0.022); risky share on parents' risky share 0.157 (0.030).
- **Mediation** (Fig. 5; Table B6). Measured mediators explain about 37% of the effect of moving from the 25th to the 75th percentile of parental wealth ($34,393 to $151,603). **Gifts and inheritances account for about 90% of the indirect effect.**
  - Each $10,000 of parental wealth raises gifts and inheritances by $1,480 and schooling by just 0.01 years (p. 729).
- **ACE** (Table 5). In the standard model, net wealth splits into genes 0.291 and shared environment 0.164, and education into 0.544 and 0.127. The risky share has almost no genetic share: genes 0.005, shared environment 0.171. In the extended model the gene–environment correlation for net wealth is $g=-0.249$ (significant at 10%), consistent with compensation.

### 6. Robustness and limitations
- **Stated by the authors**
  - Assignment to a wealthy family is not the same as an exogenous wealth transfer.
  - Adoptees are 28–49 years old, so wealth transmission and inheritance may be larger at older ages (p. 723).
  - External validity: adoptive parents are older but similar once birth years are conditioned on (Table B7). The comparison of adopted vs adopted-and-biological siblings shows no differential investment (Table B8).
  - The ACE model is restrictive.
- **My assessment**
  - Norway's institutions (free education, compressed wages, an equal-sharing inheritance law) limit how far the 0.225 carries over to the US.
  - The education channel is almost absent, which differs sharply from human-capital IGE models.
  - The mediators exclude parental *time*. No inputs are measured.

### 7. Findings relevant for us
- **Nature vs nurture benchmark.** Within the same family, the genetic link roughly doubles transmission (0.468 vs 0.276). Read any *observational* IGE in PSID or NLSY, ours included, as an upper bound on causal family effects. The paper's language should make clear that the model-implied IGE separates the *mechanism* share, not the causal share against genes.
- **The wealth route works through transfers, not human capital.** In our model, assets and transfers are a separate route from mothers' time. If we add bequests or inter-vivos transfers, Norway shows they can dominate the wealth IGE while contributing almost nothing to education.
- **Life-cycle stability.** Transmission rises with the child's measurement age for biological children but not for adoptees (Table B4). This supports measuring outcomes near age 40, as in our Lee–Solon age-40 design.

### 8. Technical modeling / measurement choices relevant for us
- **Copy**
  - Average parental and child outcomes over several years (3 here).
  - Report levels, ranks and logs, and state the sample lost in logs (41% of adoptees here). For net worth (NLSY79 `8.NetWorth.py`) use levels or ranks, not logs.
  - Use the Heckman–Pinto mediation formulas for the decomposition of the IGE and of the racial gap at a given parental income (PLAN Phase 2). They give a direct/indirect split with a testable invariance restriction ($\alpha^p=0$, $\beta=0$).
- **Adapt**
  - The balance test (child traits regressed on family traits given the assignment period) for our Bartik-shock design: regress pre-birth mother traits on the birth-year shock with state and year fixed effects.
- **Avoid**
  - Interpreting mediation shares causally when the mediators are endogenous. Theirs require uncorrelated unmeasured mediators, a strong assumption.

---

## Bolt, French, Hentall-MacCuish & O'Dea (2024), "The Intergenerational Elasticity of Earnings: Exploring the Mechanisms" (working paper, version of 31 May 2024; the acknowledgments thank "the Editor (James Heckman)") — file: Mediation_BFHO.pdf

### 1. Question and contribution
How do education, cognitive and non-cognitive skills, parental time and school-quality investments, and family background (parents' education, number of siblings) generate the intergenerational elasticity (IGE) of lifetime earnings?

The paper estimates a multi-stage system with latent factors: CES skill technologies, investment and education decision rules, and a CES earnings equation. The earnings equation lets background, investments and parental income affect earnings *directly*, as the sociology "Wisconsin model" allows. The IGE is then decomposed by sequentially equalizing variables in eight "levels" of mediation. The paper bridges path analysis in sociology and skill-formation economics, and it **tests** rather than imposes the human-capital restrictions.

### 2. Data and sample
- **NCDS 1958 British birth cohort.** One week of March 1958 births; waves at birth and ages 7, 11, 16, 23, 33, 42, 50 and 55 (age 46 unused).
- **Final sample:** 1,635 men and 1,673 women (App. A.2).
- **Parental income** is observed *only at child age 16*: father's and mother's net earnings plus other net income.
  - The data come in bands. They are imputed within bands using models from the 1973–75 Family Expenditure Survey (IFS harmonization; App. A.1.1).
  - Families are dropped if a working parent's earnings are missing, and the father must have been 20–45 at the birth.
  - Mean parental income is £18,900 (2014 prices): £12,200 in the bottom tertile and £26,400 in the top (Table 1).
- **Child earnings.** Gross earnings at 23, 33, 42, 50 and 55 are combined into *average undiscounted gross annual earnings over ages 23–55, with non-workers set to 0*.
  - Missing waves are imputed from $\ln Y_{it}=f_i+\chi_0t+\chi_1\text{ed}_i t$. Out-of-work spells are set to 0, and monthly earnings are interpolated linearly.
  - Inclusion requires at least 61 months of work history and at least 2 earnings observations (App. A.1.2).
- **Skills and investments.** Multiple measures at 7, 11 and 16 (Table 2):
  - cognitive skills: tests and teacher assessments;
  - non-cognitive skills: teacher-rated Bristol Social Adjustment Guide;
  - time investments: reading to the child, outings, parents' interest, ambitions;
  - school quality: PTA, class size, GCE shares.
- **Measurement error** is handled throughout (Section 5).

### 3. Empirical / econometric approach
**IGE.** $\ln Y=\rho_0+\rho\ln Y_P+u$ (eq. 1). Point-in-time parental income is a noisy, possibly non-classical measure of lifetime income (eq. 9 / 24):

$$\ln Y_{P,i,16}=\mu_P+\lambda_P\ln Y_{P,i}+\epsilon_{P,i},\qquad \text{plim}\,\hat\rho^{*}=\rho\cdot RR_P,\quad RR_P=\frac{\lambda_P\text{Var}(\ln Y_P)}{\lambda_P^2\text{Var}(\ln Y_P)+\text{Var}(\epsilon_P)}.$$

- $RR_P$ and $\lambda_P$ are unknown for parents. They are **estimated in the child generation**, where both point-in-time and lifetime earnings are observed, and assumed constant across generations.
- The errors-in-variables (EIV) correction rescales $\tilde Z=(\ln Y_{P,16}-\mu_P)/\lambda_P$, giving $\rho=\hat\rho\,\text{Var}(\tilde Z)/\text{Var}(\ln Y_P)$ (App. B.1).

**Measurement system.** $Z_{\omega,i,t,j}=\mu_{\omega,t,j}+\lambda_{\omega,t,j}\,\omega_{i,t}+\epsilon_{\omega,i,t,j}$.
- Loadings come from covariances of at least 3 measures. Latent log factors have variance 1; skill means are 0 in the first period and investment means are 0 in every period (App. D.1–D.2).
- Factors are predicted by Bartlett scores, $\hat\omega=(\lambda'\Omega^{-1}\lambda)^{-1}\lambda'\Omega^{-1}Z$.
- The joint distribution of all variables is approximated by a **mixture of two normals** estimated by EM, net of the known error variances (Attanasio–Meghir–Nix 2020). From it they draw a **synthetic error-free data set of 50 draws per person**.
- Production functions and earnings are estimated by NLS on the synthetic data; decision rules by OLS. Inference uses 250 bootstrap draws (90% confidence intervals).

**Decomposition.** One variable at a time is set to its mean in an increasing set of equations (level 1: earnings only; level 2: + education; 3: + skills at 16; 4: + investments 11–16; … 8: + investments 0–7). The model is re-simulated, the IGE re-estimated, and the percentage change recorded (Section 6.3; Fig. 1).

### 4. Model
There are no preferences; decision rules are approximated (as in Heckman et al. 2018). The equations are:

- **Earnings (CES)** (eq. 2):
  $$Y=[\alpha_0\text{ed}^\phi+\alpha_1\theta_C^\phi+\alpha_2\theta_N^\phi+\alpha_3 I^\phi+\alpha_4\text{ed}_m^\phi+\alpha_5\text{ed}_f^\phi]^{\nu/\phi}\exp(\alpha_6+\alpha_7\text{sib}+\alpha_8\ln Y_P+u_Y).$$
- **Education** (eq. 3): linear in log skills at 16, log investments, parents' education, siblings and $\ln Y_P$.
- **Skills (CES)**, with a free returns-to-scale parameter $\nu_{t,k}$ to avoid the scale-normalization bias of Freyberger (2021) (eq. 4):
  $$\theta_{k,t+1}=[\gamma_1\theta_{C,t}^{\phi}+\gamma_2\theta_{N,t}^{\phi}+\gamma_3 ti_t^{\phi}+\gamma_4 sq_t^{\phi}+\gamma_5\text{ed}_m^{\phi}+\gamma_6\text{ed}_f^{\phi}]^{\nu_{t,k}/\phi}\exp(\gamma_7+\gamma_8\text{sib}+\gamma_9\ln Y_P+u).$$
  The location of log skills is identified from the CES constant, with no TFP growth (App. D.2).
- **Investments** (eqs. 5–6): log time and log school quality are linear in lagged log skills, background and $\ln Y_P$.

**Key estimates**

IGE (Table 3):

| | Men | Women |
|---|---|---|
| Uncorrected | 0.272 (0.039) | 0.247 (0.048) |
| EIV-corrected | 0.335 | 0.298 |
| Model-implied | 0.344 (0.049) | 0.309 (0.070) |

Alternative definitions, uncorrected (Table 8):
- net lifetime earnings: 0.271 for men, 0.202 for women;
- net *family* lifetime earnings: 0.197 for men, 0.163 for women.

Earnings and education equations (Table 4):

| Effect | Men | Women |
|---|---|---|
| Return to a year of education | 4.2% | 11.6% |
| +1 SD log cognitive skill at 16 → earnings | 0.148 | 0.096 |
| +1 log point parental income → earnings, conditional on everything | 0.152 (90% CI 0.073–0.245) | 0.103 (CI includes 0) |
| +1 SD cognitive skill → years of education | 1.12 | 1.08 |
| Joint test: investments have no direct effect on earnings, p | 0.542 | 0.846 |
| Joint test: investments have no direct effect on education, p | 0.093 | 0.000 |
| Elasticity of substitution in earnings | 1.305 | 0.911 (about log-linear) |
| Returns to scale in earnings | 0.733 | 2.48 |

Parental income has *no* effect on education once skills are controlled for (men −0.015).

Skill technology and investments:
- Time-investment productivity for cognitive skill (Table 5): age 7: 0.187 men, 0.230 women; ages 11 and 16: about 0.07–0.12.
- Parental income → age-7 cognitive skill for men: 0.284.
- Elasticities of substitution: 0.71–1.36 for cognitive skill, 0.41–1.01 for non-cognitive skill.
- Investment rules (Table 6): a 10% rise in parental income raises time investment at 0–7 by 0.045 SD for boys and 0.032 SD for girls; one more sibling lowers it by 0.242 SD.

### 5. Main findings
- **Total shares explained.** The channels explain **55% of the IGE for men and 68% for women** (Fig. 2; Table 11). The rest is a direct effect of parental income.

Decomposition shares (Table 11):

| Channel and level | Men | Women |
|---|---|---|
| Direct effect: education | 13.5% | 39.5% |
| Direct effect: cognitive skill at 16 | 32.1% | 22.8% |
| Cognitive skill at 16, level 2 (incl. effect via education) | 43.2% | 49.3% |
| Education at level 2 | about 0 | about 0 |
| Investments at 0–7, level 7 | 21.9% | 21.3% |
| Investments at 0–7, level 8 (after attributing part to parents' education) | 14.2% | 9.9% |
| Parents' education, level 8 | 20.9% | 35.9% |

- At level 2 education's share drops to about 0: the education gradient is *fully* explained by skills.
- Investments explain 28% (men) and 24% (women) of the IGE, and still 20% and 12% conditional on background (pp. 3, 28).
- Conclusion: if credit constraints matter, they bind on early investments, not on education (p. 35). The cohort faced no tuition fees.
- **Ignoring measurement error** (single best measure; Fig. 3; Table 15) leaves the total almost unchanged (about 56%) but more than halves the investment share: investments at 0–7 explain 2.6% instead of 14.2% for men at level 8. Shares shift to the error-free variables, such as parents' education.

### 6. Robustness and limitations
- **Robustness checks**
  - A permanent unobserved factor, identified from 7 self-rated adult skill measures with loadings set to 1 and a unit elasticity in earnings, reduces the share explained for men to about 46% (Table 18). The factor's own share is negative.
  - Three normals instead of two: men 51.6%. The text says women rise to 72%, but Table 19 shows 67.4–68.8%, a discrepancy.
  - Normalizations (Tables 21–22) and mother-reported non-cognitive measures (Table 20) do not matter.
  - Alternative investment measures raise the women's share to about 91–94% (Table 24).
- **Stated by the authors**
  - Parental income is observed once.
  - The unobserved-heterogeneity approach rests on strong restrictions.
  - Period shocks to investments (compensating behavior) would bias the time effects downward.
  - Neighborhoods, networks and occupations are not modeled (pp. 33–35).
- **My assessment**
  - The reliability ratio is imported from the child generation, under assumed stability across generations.
  - Investment measures are retrospective and crude (frequency of reading or outings, teacher-rated "interest"); "parental interest" mixes preferences with time.
  - There is no maternal employment, no money input separate from income, no race, and no family-structure dynamics.
  - The investment decision rules are reduced form, so counterfactual policies that change parents' constraints are not available.
  - Women's earnings combine labor supply with wages (zeros included). The higher women's IGE share explained by education partly reflects participation.

### 7. Findings relevant for us
- **The IGE definition and correction we use.** Log lifetime earnings is regressed on log parental income, and the reliability ratio is estimated from a generation with both point-in-time and lifetime income. The correction raises the IGE by about 25% (0.272 → 0.335–0.344 for men). Our PSID setting is better: we observe parents' income in many years, so $RR_P$ can be estimated *in the parent generation itself*. The cross-generation stability assumption can then be tested.
- **Targets for the child block.**
  - The time-investment productivity at the youngest age (0.19–0.23 SD of age-7 cognitive skill per SD of investment) is the largest of the investment effects in Table 5.
  - Income → investments elasticity: 0.3–0.45 SD per log point (Table 6).
  - Skill → education: about 1.1 years per SD. Skill → earnings: 0.10–0.15 per SD.
  - Investments at 0–7 carry about 20% of the IGE.
  These benchmarks tell us whether a mother-time channel can carry an economically meaningful share (PLAN Phase 2 gate).
- **The direct effect of parental income on earnings** (0.152 for men) leaves 45% unexplained. A model-implied IGE from human capital alone should fall short of the observed IGE; we should report the share it explains, as BFHO do.

### 8. Technical modeling / measurement choices relevant for us
- **Copy**
  - The full measurement pipeline for NLSY79 Children-file scores (PIAT math, PIAT reading, PPVT, Behavior Problems Index) and CDS scores (`9a.CDS.py`): loadings from covariances, Bartlett scores, error variances, a mixture-of-normals joint distribution, synthetic error-free draws, then NLS on CES. This is PLAN Phase 4.1 (`16.SkillTechnology.py`).
  - A free returns-to-scale parameter with unit-variance factors (Freyberger normalization).
  - The level-by-level decomposition design for our model-implied IGE and racial gap. Replace "equalize variable X" with "switch off the search friction / husbands' risk / selection".
- **Adapt**
  - Their "time investment" is a latent factor from frequency items. We want maternal *hours/months not working* by child age as a measured input, with the Bartik shock as an instrument. Unlike BFHO, we have exogenous variation. Their assumption that investment shocks are independent of skills (relaxed only by a fixed effect) is exactly what our instrument can address.
  - Lifetime earnings with zeros and FE imputation: our PSID and NLSY79 "lifetime mean" robustness specification should follow App. A.1.2 (impute missing waves, keep zeros, average).
- **Avoid**
  - Treating the uncorrected single-year parental income IGE as the headline.
  - Interpreting the residual direct effect of parental income as networks without evidence.

---

## Chetty, Hendren, Jones & Porter (2020), "Race and Economic Opportunity in the United States: An Intergenerational Perspective" (Quarterly Journal of Economics 135(2): 711–783) — file: qjz042.pdf

### 1. Question and contribution
What drives racial income gaps across generations? The paper uses population data: Census 2000 and 2010 linked to IRS records 1989–2015 and the ACS.

A Becker–Tomes/Galton rank model shows that long-run disparities depend on the **intergenerational gap**: the gap in children's outcomes *conditional on parental income*. The paper then decomposes the Black–white gap by:
- gender;
- individual vs household income;
- family factors (marital status, education, wealth);
- neighborhoods, using tract and block fixed effects and correlates such as father presence and racial bias;
- causal childhood exposure effects, from movers.

### 2. Data and sample
- **Cohorts:** children born 1978–83, US-born or authorized immigrants, claimed as dependents (1994–2015) by a parent aged 15–50 at the birth. The parent is the *first claimer*, with the assignment fixed permanently.
- **Sample:** 20 million children (about 94% of the target population); 21.3 million in the sample, 94% with race (p. 729).
- **Parent income:** pre-tax household AGI, with zero for non-filers, averaged over 1994, 1995 and 1998–2000 (children aged 11–22). Parents are ranked against all parents of children in the same birth cohort.
- **Child income:** mean household or *individual* income in 2014–15 (ages 31–37). W-2 earnings are used for non-filers. Individual income = own W-2 wages plus non-wage AGI split equally between joint filers. Children are ranked within their cohort.
- **Other variables**
  - race from Census or ACS self-reports;
  - marriage from 2015 joint filing;
  - incarceration from 2010 group quarters;
  - employment, hours, wages, occupation and education from the ACS at age 30 or older;
  - parents' education and wealth proxies (home ownership, value, mortgage, vehicles) from the 2000 long form or the ACS, with the Survey of Consumer Finances used to scale to total wealth (Online Appendix F, not in the PDF).
- **Measurement error and life-cycle bias:** a 5-year parental average; "using longer averages does not affect the results significantly" (fn. 12). The pooled rank slope is 0.35, vs 0.34 in Chetty et al. (2014) at ages 29–32. The 0.01 increase is attributed to less life-cycle bias at older ages (fn. 10).

### 3. Empirical / econometric approach
**Rank model.** $y_{i,t}=\alpha_r+\beta_r y_{i,t-1}+\varepsilon_{i,t}$. This implies a steady state $\bar y^{SS}_r=\alpha_r/(1-\beta_r)$ and a steady-state racial gap $\Delta\bar y^{SS}=\Delta\alpha/(1-\beta)$ when slopes are equal (eqs. 1–4).

**Gap at parental percentile $\bar p$ controlling for $X$** (eq. 5):
$$y_{i}=a+b_p y_{i,p}+b_w\text{white}_i+b_{wp}\text{white}_i\,y_{i,p}+cX_i+e_i,\qquad \Delta_{\bar p\mid X}=b_w+b_{wp}\bar p .$$

**Place effects.** Commuting-zone (CZ) and tract regressions $y=\alpha_{cr}+\beta_{cr}y_p$, weighted by years of exposure before age 23 (eq. 6). Tract-level variances are corrected for sampling noise; correlations are corrected for attenuation by the square root of reliability.

**Movers design** (eq. 7). Children whose families move once across CZs (cohorts 1978–85). The outcome is regressed on the destination-minus-origin predicted outcome for the same race, gender and parental rank, interacted with age-at-move fixed effects. Identification: potential outcomes are orthogonal to the age at move (Chetty–Hendren 2018a).

### 4. Model
There is only the statistical Becker–Tomes rank model above, plus an online-appendix extension in which men's and women's ranks depend on both parents' ranks (Online Appendix E).

### 5. Main findings
**Mobility by race**
- Whites: $\beta_w=0.32$, $\alpha_w=36.8$. Blacks: $\beta_b=0.28$, with a uniformly lower intercept.
- Black children with parents at p25 reach rank 32.6, 12.6 below whites. In the top 1% the gap is still 12.4 (13.1 at the 99th percentile) (pp. 731–733; Fig. II).
- Steady states: whites 54.4, Blacks 35.2, a gap of 19.2. The observed child gap is 20.9 (55.7 vs 34.8), so Blacks are near steady state (Fig. II B; Table I).
- Hispanic steady state 48.7. American Indian steady state 36.5. Asians $\beta=0.18$, but Asians with US-born mothers are close to whites (Fig. III).

**Quintile transitions** (Table I)

| Transition | White | Black |
|---|---|---|
| Household income: P(top quintile \| parents bottom) | 10.6% | 2.5% |
| Household income: P(top \| parents top) | 41.1% | 18.0% |
| Household income: P(bottom \| parents top) | 8.7% | 16.7% |
| Individual income: P(top \| parents bottom) | 11.1% | 6.3% |

**Gender** (Figs. IV–VII)
- The household-income gap of about 13 percentiles falls to about 5 for individual income.
- **Men: about 10–11 percentiles. Women: Black women earn about 1 percentile *more* than white women at the same parental income**, with similar wages, hours and employment (Fig. VI; occupations Online Appendix Fig. IV).
- Black men: wages about 7 percentiles lower and about 9 fewer hours per week. Employment gap 18.9 pp at p25 and 11.4 pp at p75.
- Marriage-rate gap: 32 pp at p25, 34 pp at p75 (Fig. IV A).
- Education gaps at p25:

  | Gap at p25 | Women | Men |
  |---|---|---|
  | High school completion | 3.5 pp | 8.3 pp |
  | College attendance | 2.8 pp | 6.5 pp |

- Incarceration on 1 April 2010: 21% of Black men vs 6.4% of white men from bottom-1% families; 2.2% vs 0.2% from top-1% families (Fig. VII). Overall, 10.3% of Black men in the sample were incarcerated (p. 729).
- Test-score gaps at age 9 (NAEP, low-income) do not differ by gender: 0.48 SD for boys, 0.44 SD for girls (p. 751).

**Family factors** (Fig. VIII A). Black–white gap in men's individual income ranks at p25, adding controls cumulatively:

| Controls | Gap at p25 |
|---|---|
| None (conditional on parental income only) | 10.0 |
| + parents' marital status | 9.3 |
| + parents' education | 9.1 |
| + wealth proxies | 8.4 |
| + SCF-adjusted total wealth | 8.0 |

At p75 the gap goes 11.7 → 11.4 → 11.4 → 11.0 → 10.2 (Fig. VIII B). The unconditional gap is 17.6 for men and 4.8 for women. Controlling for marital status *without* parental income cuts the men's gap from 17.6 to 13.3 (fn. 19).

**Neighborhoods** (Section VII)
- Tract fixed effects: 7.7. Block fixed effects: 7.0 at p25, 7.9 at p75. White boys out-earn Black boys in 98.7% of tracts at p25.
- The gap is larger in low-poverty tracts (+2.5 percentiles; Fig. X B).
- Low-income Black father presence in a tract: +0.0492 (0.0062) per unit, i.e. 10 pp more presence raises Black boys' rank by 0.5 (Table II). It has no association with white boys' or Black girls' outcomes. It holds within single-parent and two-parent families, and with fixed effects for the adult tract.
- Racial bias (IAT): −0.0081 per SD (Table III).
- Exposure effects per year before age 23: 0.027 for Black boys, 0.026 for white boys. They are race-specific: a Black boy's outcome tracks the outcomes of Black children in the destination, not white children (−0.029 vs −0.003; pp. 773–775).
- Only 4.2% of Black children grow up in tracts with poverty below 10% and Black father presence above 50%, against 62.5% of white children in comparable tracts (Fig. XIV).

### 6. Robustness and limitations
- **Stated by the authors**
  - Steady-state predictions assume mobility parameters are constant.
  - Neighborhood correlates are not causal.
  - The IAT sample is selected.
  - Wealth is measured by proxies.
  - Women's wages may be selected (they discuss Neal 2004).
- **My assessment**
  - Parents' income is AGI. It excludes non-taxable transfers (AFDC/TANF, SNAP), which matter for low-income Black families.
  - Ranks hide dollar gaps, and the log IGE is not reported.
  - Children are measured at 31–37 with a 2-year average, which leaves some life-cycle and transitory noise, especially for women's household income through marriage timing.
  - There is no measure of childhood inputs (maternal employment, time, father's job loss), so "family factors" cover only marital status, education and wealth.
  - The finding of no gap for women is conditional on parental household income. It does not say Black mothers' labor supply has no intergenerational effect.

### 7. Findings relevant for us
- **Headline benchmark for the IGE by race.** Rank slopes are similar across races (0.28 vs 0.32); the gap is in the intercept (about 13 percentiles of household income). Our PSID within-race log IGEs (`output/ige_main.md`: Black sons 0.268, white sons 0.473) should be reported alongside **Chetty-comparable rank statistics**: rank–rank slope, expected rank at p25 and p75, P(top quintile | parents bottom quintile). This is PLAN step 0.3 (`7.RankMobility.py`).
- **The racial gap for daughters is about 0 in individual income** at a given parental income, but Black women have far lower household income because of marriage and husbands' earnings (pp. 746–747). This is strong motivation for the companion paper's "husbands' earnings and employment risk" ingredient: the next generation's Black mothers again face low and risky spousal income.
- **The model's IGE by sex must match this pattern.** A child block in which mothers' time affects sons and daughters symmetrically will struggle to produce a men-only gap. Gender-specific technology or a channel through fathers (father presence, fathers' job loss) is needed.
- **Family structure explains little of the gap conditional on parental income** (marital status: 10 → 9.3). The mother-time channel must therefore work *within* parental income, for example through the timing of mothers' work at the birth and the variance of family income, rather than through average income or marital status.
- **Policy framing.** Transitory cash transfers do not change steady-state gaps unless they change $\Delta\alpha$ (p. 714). Our policies (paid leave, the safety net, UI for husbands) should therefore be evaluated on the model-implied intergenerational gap $\Delta\alpha$ and the steady state $\Delta\alpha/(1-\beta)$, not only on income in one generation.
- **Public data for PLAN Phase 5.** Opportunity Atlas CZ and tract outcomes by race × parental percentile × gender can be merged with local women's re-employment frictions.

### 8. Technical modeling / measurement choices relevant for us
- **Copy**
  - Percentile ranks within the child cohort and within the parents' cohort. These handle zero incomes, which logs cannot.
  - Separate **individual vs household** income for children.
  - Report the gap at fixed parental percentiles (p25, p75).
  - Correct place-level variances and correlations for sampling noise.
  - Steady-state formulas to translate a model-implied $\Delta\alpha$ into a long-run gap.
- **Adapt**
  - Their "father presence" is a tax-filing indicator. In the PSID and NLSY79 we can measure father presence and fathers' job loss over the child's whole childhood, as exposure.
  - The movers' exposure design (years before 23) suggests also measuring our childhood exposures by *years of exposure*.
- **Avoid**
  - Interpreting the absence of a women's gap as the absence of a maternal channel. Interpreting rank slopes as log elasticities: in the PSID the log IGE within race is much lower for Blacks (0.27) than for whites (0.47), even though rank slopes are similar. This reflects differences in the spread of the within-race distributions.

---

## Del Boca, Flinn & Wiswall (2014), "Household Choices and Child Development" (Review of Economic Studies 81(1): 137–185) — file: rdt026.pdf

### 1. Question and contribution
How do parents' time and money produce children's cognitive skill, and how do households choose these inputs together with labor supply? The authors estimate a dynamic model of a married couple's labor supply, active and passive time with the child, and child goods expenditure, with a Cobb–Douglas skill technology whose productivities vary with age. Estimation is by the method of simulated moments (MSM) on PSID-CDS time diaries.

The paper's novelty relative to Todd–Wolpin and Cunha–Heckman–Schennach: input endogeneity is handled through an explicit household model, and both parents' time inputs are measured, not proxied by maternal employment.

### 2. Data and sample
- **Data:** PSID core 1997–2003 (biennial: hours, wages, non-labor income for 1996, 1998, 2000, 2002), plus CDS-I (1997) and CDS-II (2002–03).
- **Time diaries:** one weekday and one weekend day, separately for mother and father, *active* (engaged) vs *passive* (present but not engaged). Weekly time is weekday × 5 + weekend × 2, with a Saturday/Sunday adjustment (fn. 19).
- **Outcome:** the Woodcock–Johnson **Letter-Word raw score** (57 items, not age-normed), used for children aged 3–12 in 1997 (p. 156).
- **Sample:** intact two-parent households, both biological parents present in both waves, valid scores in both waves. Wages above $150/h and non-labor income above $1,000/week are dropped.
  - 237 households: 105 with one child, 132 with two (twins excluded).
  - 2001 dollars.
- **Descriptives**
  - Mean mothers' hours: 32.2 (one child) vs 26.9 (two children); fathers 43.8 vs 45.4 (Table 1).
  - One-child mothers' employment rises from 0.75 at child age 3 to 0.82–0.88 later (Table 2).
  - Mothers' active time: 29.3 h/week at age 3 vs fathers' 16.9 (Table 3).
- **Measurement:** latent child quality maps to the test score through a binomial model (Section 3.3).

### 3. Empirical / econometric approach
**Measurement**
- The number correct is $k^*\sim\text{Binomial}(57,p(k))$ with $p(k)=\exp(\lambda_0+\lambda_1\ln k)/(1+\exp(\cdot))$, normalized by $\lambda_0=0$ and $\lambda_1=1$, so that $p=k/(1+k)$.
- The initial latent $k$ is drawn from the Beta(1+$k^*$, 58−$k^*$) posterior given a uniform prior, and $k=\tilde p/(1-\tilde p)$ (pp. 151–153).

**Identification argument** (Section 3.4)
- With consecutive scores, NLS of $\ln k_{t+1}$ on log inputs identifies the technology, given i.i.d. TFP shocks. Inputs are orthogonal to the TFP shock because decisions do not depend on it.
- Given the technology, the input demand system can be inverted for each household's $\alpha$, so $G(\alpha)$ is non-parametrically identified.
- $\beta$ and $\psi$ are identified from households where both parents work.
- In practice there are 5-year gaps between CDS waves and non-random missing wages, so the model is **simulated between waves** and estimated by MSM.

**MSM**
$$\hat\Omega=\arg\min (M_N-\tilde M_S(\Omega))'W_N(M_N-\tilde M_S(\Omega)),$$
where $W_N$ is the inverse of the bootstrap covariance of the data moments (200 resamples; fn. 24).
- Moments: means and SDs of test scores, hours and investment hours by child age; wage moments and the spousal wage correlation; lagged and contemporaneous correlations (list in online Appendix B, not in the PDF).
- Fixed: $\beta=0.95$; horizon $M=16$; annual periods with weekly decisions (fn. 25).

### 4. Model
- **Preferences** (Cobb–Douglas; eq. 1): $u=\alpha_1\ln l_1+\alpha_2\ln l_2+\alpha_3\ln c+\alpha_4\ln k$, with $\sum\alpha=1$.
  - $\alpha$ is heterogeneous across households, from a logistic-normal mapping of a trivariate normal (pp. 149–150).
  - Time with the child gives **no direct utility**; it is a pure investment (p. 141).
- **Technology** (eq. 2):
  $$k_{t+1}=R_t\,\tau_{1t}(a)^{\delta_{1t}(a)}\tau_{2t}(a)^{\delta_{2t}(a)}\tau_{1t}(p)^{\delta_{1t}(p)}\tau_{2t}(p)^{\delta_{2t}(p)}e_t^{\delta_{3t}}k_t^{\delta_{4t}}.$$
  Productivities are $\delta_{j,t}=\exp(\gamma_{j,0}+\gamma_{j,1}t)$, monotone in age, and $R_t=\exp(\gamma_{0,0}+\gamma_{0,1}t+\varpi_t)$.
- **Constraints.** Time: $T=l_j+h_j+\tau_j(a)+\tau_j(p)$. Budget: $c+e=w_1h_1+w_2h_2+I$, with **no borrowing or saving**. Terminal value: $\psi\alpha_4\ln k_{M+1}$.
- **Exogenous processes.**
  - Log wages depend on education, age, age² and birth cohort, with i.i.d. shocks correlated across spouses. AR(1) shocks could not be credibly estimated from biennial data (aliasing; fn. 12).
  - Non-labor income is a Tobit.
- **Closed forms.** Input demands are $\tau^*_{1}(a)=(T-h_1)\varphi_{1}(a)/(\alpha_1+\varphi_1(a)+\varphi_1(p))$ and $e^*=(\text{income})\,\varphi_3/(\alpha_3+\varphi_3)$, with $\varphi=\beta\delta\eta_{t+1}$, where $\eta_t=\alpha_4+\beta\delta_{4t}\eta_{t+1}$ is the marginal value of log child quality (eqs. 6–11). Labor supplies have explicit corner conditions (eq. 12). Investment does not depend on current $k_t$ or on future wages.
- **Two-child version.** Eight time categories per parent (alone vs joint, active vs passive), a preference split $\kappa$, and symmetry restrictions (Section 2.6).

**Key estimates**
- One-child preference means (Table 5): $\alpha_1=0.196$, $\alpha_2=0.194$, $\alpha_3=0.257$, $\alpha_4=0.353$; $\psi=28.89$ (6.61).
- Two-child: $\alpha_4+\alpha_5=0.402$, $\hat\kappa=0.460$; $\psi_1$ and $\psi_2$ are 2.58 and 2.99.
- Technology (Table 6): mother active $(-1.33,-0.139)$, father active $(-2.47,-0.029)$, mother passive $(-1.76,-0.125)$, father passive $(-2.86,-0.012)$, expenditure $(-3.27,+0.104)$, lagged quality $(-2.047,+0.085)$.

Implied productivities, my calculation from Table 6 (cf. Figs. 2–3):

| Input | Age 3 | Age 12 |
|---|---|---|
| Mother's active time | 0.174 | 0.050 |
| Father's active time | 0.078 | 0.060 |
| Mother's passive time | 0.118 | 0.038 |
| Father's passive time | 0.055 | 0.050 |
| Child expenditure | 0.052 | 0.132 |
| Lagged child quality | 0.167 | 0.358 |

- Wages (Table 7): returns to schooling 0.049 for mothers and 0.081 for fathers; spousal shock correlation 0.710.

### 5. Main findings
- **Time is more productive than money, especially early.** Mothers' active time is the most productive input for young children; fathers' time is nearly as productive and declines less with age. Money productivity rises with age but stays modest (pp. 164–166; Figs. 2–3).
- **Fit:** good for wages, time and test-score profiles. The model predicts *rising* maternal employment with child age, while the data show a slight fall (Table 9).
- **Preference experiments** (Table 12)
  - Child-quality-maximizing parents: final latent quality +43% (13.38 → 19.20); mothers' hours 33.25 → 16.38; time inputs up more than 300%.
  - Selfish parents: mothers' hours +30% (43.30).
- **Transfers** (Table 13), percentage change in final child quality:

| Transfer | Child quality |
|---|---|
| Unrestricted $250/week at all ages | +1.61% (mothers' hours −15.1%, fathers' −12.6%) |
| $250 that must be spent on child goods | +4.63% |
| $500 child goods at ages 3–9 | +0.02% |
| $500 child goods at ages 10–15 | +9.42% |

Money is most effective late, because early on time is more productive than money and money's productivity rises with age.

### 6. Robustness and limitations
- **Stated by the authors**
  - Fertility and family structure are exogenous; intact families only.
  - The money–time ranking may partly reflect ceiling effects of an unnormed test.
  - Schooling and children's self-investment are omitted, which may explain the falling parental productivity.
  - Child expenditures are not used because reports are poor (fn. 21).
  - The preference covariance is weakly identified.
  - Production productivities were found not to vary by parents' education (fn. 11).
- **My assessment**
  - The sample is tiny (105 one-child households).
  - Wages are exogenous: no human capital accumulation, no career cost of time with children, no job loss or search friction. The only cost of time is current wages.
  - With no saving and the Cobb–Douglas structure, inputs do not respond to expected future income, so income risk cannot matter.
  - **No observations below age 3.** Infancy productivity is an extrapolation of the exponential-linear age profile. This is precisely the period of our mother's decision at the birth.
  - Unit-elastic Cobb–Douglas rules out complementarity between time and money, and between early and late inputs.

### 7. Findings relevant for us
- **The canonical "money vs time" result.** Time beats money early; cash transfers barely move skill because they are spent on leisure and consumption (+1.6%). This is the benchmark our title answers. Our innovation is that the *cost of time* includes the search friction (a lost job, lost human capital accumulation, lost insurance against husbands' job loss), not just the current wage.
- **External estimates for the child block.** The productivity paths in the table above, if we use a Cobb–Douglas technology. The ratio of mothers' active-time productivity to money productivity is about 3.3 at age 3 and 0.4 at age 12 (my calculation). Mothers' time productivity falls by a factor of about 3.5 between ages 3 and 12.
- **Labor supply patterns by child age.** Married mothers' employment rises from 0.75 (child age 3) to 0.82–0.88 (Table 2), and hours rise from 26 to 40 conditional on working. These are moments our model already targets in another form.
- **Transfer counterfactuals.** Unrestricted vs restricted (in-kind) and early vs late transfers are a direct template for the "safety net: cash vs work requirements" experiment.

### 8. Technical modeling / measurement choices relevant for us
- **Copy**
  - Age-varying productivities $\delta_t=\exp(\gamma_0+\gamma_1 t)$: two parameters per input, cheap in SMM.
  - The marginal-value recursion $\eta_t$, which gives closed-form inputs. If our child block is Cobb–Douglas in log skill, the mother's work choice at a birth affects the continuation value linearly in $\ln k$, which keeps the state space small: a discretized $\ln k$, or even no $k$ state if investment does not depend on $k$.
  - MSM with simulation between sparse survey waves. Our SMM infrastructure (`estimation/smm.py`, `model_moments.py`) already does this.
  - Bootstrap weighting matrix.
  - The binomial test-score measurement model, if we use raw PIAT or PPVT counts.
- **Adapt**
  - Time inputs: CDS diaries give active and passive time for ages 0–12 in CDS-I (1997) and later waves (`9a.CDS.py`). In the NLSY79 the time input is months not employed by child age (weekly arrays). Map our NW/PT/FT labor supply to time via $\tau=T-h$, as DFW's time constraint implies, but allow the residual to include leisure.
  - Exogenous wages: in our model, wages depend on human capital accumulation with FT/PT accumulation and depreciation. This makes the cost of a year out at the birth dynamic, which DFW lack.
  - Intact families: our model has marriage and divorce, so the child block must handle father presence changing over time. The two-child extension shows how to handle siblings (joint vs alone time).
- **Avoid**
  - Raw unnormed scores, which give ceiling effects; use age-normed scores or a measurement system with age-specific intercepts.
  - Identifying infancy productivity by extrapolation: the NLSY79 Children file has the Motor and Social Development scale (ages 0–3), the PPVT (from age 3–4) and the HOME inventory (all ages), which can anchor the earliest stage. (This is from the NLSY documentation, not from DFW.)

---

## Palomino, Marrero & Rodríguez (2018), "One Size Doesn't Fit All: A Quantile Analysis of Intergenerational Income Mobility in the U.S. (1980–2010)" (Journal of Economic Inequality 16: 347–367) — file: s10888-017-9372-8.pdf

### 1. Question and contribution
Does the IGE differ across the conditional distribution of sons' income, and how did it evolve over 1980–2010? The paper combines **conditional quantile regression** with the **Lee–Solon (2009) pooled design**, which uses all of a son's income observations at ages 25–65 with age controls centered at 40. This gives precise tail estimates. It also measures how much of the IGE at each quantile is "mediated" by sons' years of education and by race.

### 2. Data and sample
- **PSID core sample** (SRC + SEO), interview years 1980–2010 (income refers to the prior year).
- **Income:** total family income (taxable income plus transfers of head, spouse and others), in 2010 dollars (CPI). Following Lee–Solon, observations with income below $100 or above $150,000 in 1967 dollars are dropped (about 200 observations, under 1%).
- **Parents:** family income averaged over the son's ages 13–19, requiring at least 3 observations (mean 6.24). Parent's age at the son's 16 must be 30–70 (fn. 9).
- **Sons:** **sons only, who become household heads**, aged 25–65, observed in 1980–2010. Daughters are excluded because their IGE "depended strongly on their marital status" (fn. 10).
- **Sample:** 25,084 son-years from 3,088 sons, 8.12 waves on average (Table 1). The Black share of the son sample falls from 37% (1980) to 25% (2010).
- **Race:** a dummy for white, with Black pooled with all non-white. **Education:** grade completed, 1–17.
- **Measurement error:** a multi-year parental average; there is no reliability-ratio correction. Life-cycle bias is handled by age-40 centering and controls for parents' age.

### 3. Empirical / econometric approach
**Pooled specification** (eq. 2):
$$\ln y^s_{it}=\alpha+\beta\ln y^p_i+\sum_{n=1}^4\gamma_nA^n_i+\sum_{n=1}^4\delta_nC^n_{it}+\sum_{n=1}^4\theta_n[\ln y^p_i]C^n_{it}+\varepsilon_{it},$$
where $A$ is the parent's age when the son was 16, and $C=t-c-40$ is the son's age minus 40. Because of the $\theta$ interactions, $\beta$ is the IGE at son age 40.

**Year-specific IGEs** (eq. 3): year dummies interacted with $\ln y^p$; age terms pooled.

**Quantile regression** at each ventile (Koenker–Bassett), with conditional quantiles. Unconditional quantile regression (RIF-OLS, Firpo et al.) is in the online appendix, not in the PDF.

**Mediation:** add education (eq. 4), then the white dummy (eq. 5). Shares: $(\beta_{\text{base}}-\beta_{\text{edu}})/\beta_{\text{base}}$ and $(\beta_{\text{edu}}-\beta_{\text{edu+race}})/\beta_{\text{base}}$.

**Inference:** cluster bootstrap by individual (Hagemann 2016; `quantreg`; fn. 12). Wald tests of equal IGEs across years at each quantile (Table 3).

### 4. Model
There is no model; the paper is purely reduced form.

### 5. Main findings
**IGE by quantile** (Table 2; Fig. 1)

| Specification | OLS | 10th | 25th | 50th | 70th | 90th | 95th |
|---|---|---|---|---|---|---|---|
| Baseline | 0.473 (0.018) | 0.645 (0.163) | 0.526 | 0.440 | 0.379 (min) | 0.476 | 0.476 |
| + education | 0.343 | | | | | | |
| + education + race | 0.295 | | | | | | |

- The baseline IGE is **U-shaped across quantiles** (abstract and conclusion: 0.64 at the 10th percentile, minimum 0.38 or 0.37 at the 70th, 0.48 at the 95th).
- **Education mediates** 27.4% at the mean and 20–48% across quantiles, most in the tails (Table 2; Fig. 2a).
- **Race mediates** an extra 10.1% at the mean: about 10% below the median and about 5% (down to 1.7% at the 95th) above the 60th percentile (Table 2; Fig. 2b).
- **Trends** (Fig. 3; Table 3). For OLS and quantiles below the median, the IGE fell in the 1980s and 1990s and rose in the 2000s; the upper quantiles were stable. Equal IGEs across years are rejected only for OLS (Wald 78.4, p = 0.000) and the 20th, 35th and 55th percentiles.
- **Literature tables** (Tables 4–5) include Lee–Solon 0.44 and Hertz (2006) 0.51; Hertz finds that controlling for race lowers the IGE from 0.515 to 0.429.

### 6. Robustness and limitations
- **Stated by the authors**
  - Robustness to the SRC-only sample, outlier thresholds, years averaged and RIF (online appendix).
  - Trends are imprecise.
  - Family income includes transfers, which may bias the IGE downward at the bottom (fn. 13).
  - Capital income may explain the higher IGE at the top, compared with earnings-based studies.
- **My assessment**
  - "Mediation" by adding regressors is not causal and depends on ordering.
  - The white dummy mixes Black with other groups, and no race-specific IGE is estimated.
  - Sons only, and only heads, which selects on household formation.
  - No reliability-ratio correction.
  - Conditional quantiles of son income given parental income and age controls are not quantiles of the unconditional distribution.
  - Internal inconsistencies: Table 4 describes their own sample as 1978–2000, the text says 1980–2010; the minimum IGE is given as 0.38 and as 0.37.

### 7. Findings relevant for us
- **Replication benchmark for our PSID IGE code.** Pooled OLS IGE at age 40 of 0.473 (0.018) for sons (Table 2). Our Lee–Solon replication check (`IGE/5.CheckPMR.py`, `output/pmr_check.csv`) and the 1980–2010 column of `output/ige_main.md` should be compared with it. Our pooled sons 1980–2010: 0.559 unweighted, 0.483 SRC-only. The gap is consistent with sample composition (SEO, daughters, heads-or-spouses, weights) and needs a footnote.
- **Race "mediation" of about 10% of the pooled IGE.** A simple fact for the introduction: the pooled US IGE is partly a between-race phenomenon. But the race-specific IGEs (ours, CHJP's slopes) are the relevant parameters for our model.
- **A higher IGE in the bottom tail** (0.55–0.65 at the 5th–20th percentiles). If the mother-time channel matters most for low-income and Black families, the model-implied IGE should show a larger elasticity in the lower tail. Quantile IGEs give a distributional test of the model.

### 8. Technical modeling / measurement choices relevant for us
- **Copy**
  - The exact Lee–Solon specification: quartics in parent's age at the child's 16 and in child age minus 40, plus the interaction of $\ln y^p$ with the child-age quartic, so that $\beta$ is the IGE at 40. Already in `6.IGEMain.py`.
  - A parental average over ages 13–19 with at least 3 observations.
  - Cluster bootstrap by child.
  - The 1967-dollar trimming rule as a robustness check.
- **Adapt**
  - Estimate by race and sex separately rather than with a race dummy.
  - Add the BFHO reliability-ratio correction on top of the Lee–Solon design. The PSID has parents' income for many years, so the ratio can be estimated in the parent generation.
  - Quantile versions of the race-specific IGE as a secondary table.
- **Avoid**
  - Sons-only, heads-only samples.
  - Interpreting the coefficient change after adding education or race as mediation without a model. Our structural decomposition replaces this.

---

## Cross-paper synthesis for our project

### (a) Comparison table

| | Gayle–Golan–Soytas 2015 | Fagereng–Mogstad–Rønning 2021 | Bolt et al. (BFHO) 2024 | Chetty–Hendren–Jones–Porter 2020 | Del Boca–Flinn–Wiswall 2014 | Palomino–Marrero–Rodríguez 2018 |
|---|---|---|---|---|---|---|
| Data | PSID 1968–97, two generations | Norwegian registers; 2,254 Korean adoptees | NCDS 1958 cohort, birth to 55 | Census + IRS 1989–2015; 20m children | PSID core + CDS-I/II; 237 intact families | PSID core 1980–2010; 3,088 sons |
| Child outcome | Completed education (4 levels); simulated earnings | Net and financial wealth; stock-market participation, risky share (age 28–49) | Log lifetime gross earnings, ages 23–55, zeros included | Household and individual income rank at 31–37; employment, wages, education, incarceration | Letter-Word raw score, ages 3–16 | Log family income at ages 25–65, centered at 40 |
| Parental income measure | Parents' labor income in child's years 0–5 (input), education, fixed effects | Parents' net wealth 1994–96 (3-year average) | Net parental income at child age 16 (banded, imputed) | Household AGI, mean of 5 years (child 11–22), rank | Annual wages and non-labor income (model state) | Family income averaged over child ages 13–19 (≥3 years) |
| Measurement error | None (discretized time) | 3-year averages; level, rank and log | Reliability ratio from child generation (EIV); latent factors, Bartlett scores, mixture of normals | 5-year average; ranks; noise correction for place estimates | Binomial test-score model with Beta prior | Multi-year average; Lee–Solon age controls; no reliability correction |
| Time investment | Yes: imputed from housework, discrete, both parents, years 0–5 | No | Yes: latent from reading, outings, interest (ages 0–7, 7–11, 11–16) | No | Yes: diaries, active and passive, both parents | No |
| Race | Yes: Black vs white, central | No | No | Yes: central (5 groups), by sex | No | White dummy (mediator) |
| Search friction / labor-market risk | No (risk-neutral; lagged FT/PT experience in earnings; no job loss) | No | No | No (descriptive employment gaps for sons) | No (i.i.d. wage-offer shocks; no saving) | No |
| Marriage / family structure | Endogenous via stochastic marriage and divorce; couples' game; exogenous matching | Household wealth; assortative mating included | Number of siblings, parents' education | Parents' marital status control; neighborhood father presence | Intact families only (one- and two-child) | Sons who head households |
| Policy experiments | Close earnings, marriage, matching, divorce gaps | None | Decomposition only | Steady-state implications; neighborhood moves | Cash vs in-kind, early vs late transfers | None |

### (b) Five most important takeaways for the new paper's design

1. **Measure the IGE two ways and correct it.** Report the BFHO-style log IGE with a reliability-ratio correction, estimated in the PSID *parent* generation (not imported), together with Chetty-comparable rank statistics by race and sex:
   - rank–rank slope;
   - expected rank at p25 and p75;
   - P(top quintile | parents bottom quintile).

   The correction is worth about +25% (BFHO 0.272 → 0.344). Logs and ranks tell different racial stories: within-race log IGEs differ a lot (PSID: Black 0.27 vs white 0.47), while rank slopes are similar (0.28 vs 0.32) and the gap sits in the intercept.

2. **The racial gap at a given parental income is a sons' phenomenon in individual income and a marriage phenomenon in household income** (CHJP). The child block must deliver:
   - a near-zero gap for daughters in own earnings;
   - a large gap for sons;
   - a large gap in household income through marriage and husbands' earnings.

   A gender-neutral "mother's time → child skill" channel alone cannot do this. Gender-specific technology, or channels through fathers (father presence, fathers' job loss: our husbands'-risk block), are needed.

3. **Early maternal time is the input to model, with a measured cost.**
   - DFW: time productivity is highest at the youngest observed ages and falls by a factor of about 3.5 by age 12; money matters late.
   - BFHO: investments at 0–7 carry about 20% of the IGE.
   - GGS: mothers' time in years 0–5 raises college completion; early income has no conditional effect.

   None of them prices the cost of time correctly. In DFW it is the current wage; in GGS, lagged experience with risk neutrality; in BFHO it is not modeled. Our contribution is the search friction: leaving work at a birth means a slow return, lost human capital accumulation, and lost insurance against the husband's job loss or divorce.

4. **Measurement error in skills and inputs changes decomposition shares by a factor of two** (BFHO: the share for investments at 0–7 falls from 14% to 3% without correction). Use a latent-factor measurement system for NLSY79 Children-file and CDS scores (Bartlett scores, a mixture of normals, synthetic data, CES with free returns to scale), and a measured time input (NLSY79 weekly arrays, CDS diaries) instrumented by gender-specific Bartik shocks at the birth.

5. **Evaluate policies on the intergenerational gap, not on income in one generation.** Following CHJP, compute the model-implied $\Delta\alpha$ and the steady state $\Delta\alpha/(1-\beta)$. Following DFW, distinguish cash vs in-kind and early vs late. Following GGS, expect offsetting household responses: marriage changes trigger specialization, and higher earnings lower fertility. Paid leave (a job that survives a year out), cash vs work requirements, and UI for husbands should each be scored on the child's skill and on the long-run racial gap.

### (c) Gaps none of them fill that our paper can fill
- **Search frictions and the price of time.** No paper models the re-employment friction a mother faces when she leaves work at a birth, or the insurance value of keeping the job against husbands' job loss or divorce. GGS explicitly assume away the insurance aspects of marriage and divorce (p. 22); DFW have no saving and exogenous i.i.d. wages.
- **Exogenous variation in maternal time at infancy.** DFW identify from functional form and timing, GGS from parents' own hours and age, BFHO from a fixed effect. None has a shock that moves the mother's work at the birth. Gender-specific Bartik shocks separate the mother's re-employment friction from the husband's risk.
- **Race and early inputs together.** CHJP have race but no inputs; DFW and BFHO have inputs but no race; GGS have both but with imputed time, no risk, and data ending in 1997.
- **Infancy.** DFW and BFHO start at age 3 or later (BFHO's 0–7 investments are measured retrospectively at 7). Our year-1 exposure (months not employed after the birth) targets the first year directly.
- **A model-implied IGE by race with labor-market risk.** None produces an IGE by race from a model with savings, a safety net and husbands' employment risk, or decomposes the racial gap at a given parental income into the search friction, husbands' risk and selection.
- **Policy with job protection.** None evaluates job-protected leave (FMLA eligibility, state paid family leave) or UI for husbands through children's outcomes.

### (d) Contradictions between papers we must handle
- **Money vs time.**
  - BFHO: parental income raises early investments (0.3–0.45 SD per log point) and has a large *direct* effect on earnings (0.152).
  - GGS: early income has no conditional effect on education (mother's income slightly negative).
  - DFW: money is unproductive early.
  - FMR: in the wealth IGE, transfers dominate and human capital is negligible.
  - Reconciliation: income may matter through investments and later-life channels (networks, transfers) rather than directly early on. Our model should allow income to enter the technology and let the data (Bartik shocks on fathers' industries as the money shock) decide.
- **Marriage and family structure.**
  - GGS: the marriage market (matching, divorce) is the largest source of the racial education gap, but raising Black marriage rates *lowers* child education through specialization.
  - CHJP: parents' marital status explains little of the income gap at a given parental income (10 → 9.3), while *neighborhood* Black father presence matters for boys.
  - Reconciliation: GGS's counterfactuals change parental income (household income endogenously) and time together; CHJP condition on parental income. Our decomposition must state whether parental income is held fixed.
- **Father vs mother time.**
  - DFW: fathers' time is almost as productive as mothers', and stable with age.
  - GGS: fathers' time works at the bottom of the education distribution, mothers' time at the top.
  - BFHO pool both parents in one factor.
  - Our model has only the mother's choice. If fathers' time matters (and father presence matters, per CHJP), divorce and husbands' job loss affect children through time as well as money, which strengthens the husbands'-risk route but must be modeled explicitly.
- **Size and sign of the racial IGE difference.**
  - Rank slopes: Black 0.28 vs white 0.32 (CHJP).
  - PSID log IGEs: Black 0.27 vs white 0.47 (ours).
  - Pooled IGE about 0.47–0.52, about 10% "mediated" by race (Palomino; Hertz 2006: 0.515 → 0.429).
  - These are consistent: lower within-race log elasticities for Blacks, a large between-race intercept gap, and a pooled IGE inflated by the between-race component. But the paper must say which parameter the model targets (the within-race IGE and the gap at a given parental income) and avoid mixing log and rank statements.
- **Women's IGE.**
  - BFHO: women's IGE and share explained (68%) differ from men's (55%), and women's earnings returns to education are higher (11.6% vs 4.2%).
  - Palomino drop daughters as dependent on marriage.
  - CHJP: no racial gap for daughters in individual income.
  - Our sample includes daughters. Report own earnings and family income separately, and treat daughters' family-income IGE as partly a marriage-market outcome, consistent with the companion model.
- **Causal vs observational transmission.** FMR show that genes roughly double observed wealth transmission (0.468 vs 0.276 within the same families). The BFHO and our model-implied decompositions attribute shares to *mechanisms*, conditional on modelled heterogeneity; they cannot separate inherited traits. We need a sentence on this, and permanent types (ability, taste for children) in the model, to absorb part of it.
