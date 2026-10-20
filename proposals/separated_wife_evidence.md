# The separated wife's state: PSID evidence for Diagnostic B (WP3, 2026-10-20)

Script `IGE/76.SeparatedMothers.py`; tables `output/separated_mothers.md`, every number with s.e., p and N in
`output/separated_mothers.csv`. Unweighted PSID SRC + SEO; s.e. clustered by 1968 family; *** p<0.01, ** p<0.05,
* p<0.1. No model file, target or existing script was touched.

## Why

The model's separated state V^S has no child support and no remarriage, and it is where 67% of Black and 41% of
White entry couples end up by the wife's age 60. The marriage note (`fable_marriage_divorce_paperA.md`, Diagnostic B)
asks for two calibrated inputs with no estimated parameters: a monthly child-support transfer to the separated wife
by race (and number of children), and an annual remarriage hazard by race that ends the simulated record, as the
couple's PSID record ends. This memo gives both, and adds the separated mothers' work and program receipt as
untargeted checks of V^S.

## Sample

Mothers whose marriage ended in 1984-2020 according to the PSID marriage history (separation year, else divorce
year = s). Each was observed as that husband's wife at an interview in s-3..s+1, with a child 0-17 in the family unit,
and was aged 25-59 at s. That gives 570 Black and 924 White mothers, observed for 2,884 and 4,608 woman-years at
k = 0..10 (k = income year - s). Age at separation was 34.4 / 35.0, with 2.16 / 1.96 children. The ex-husband had a
displacement (closure or layoff, IGE/19 definition) in s-2..s for 17.2% of Black and 12.2% of White mothers. All
observed years are used; there is no balanced panel.

Where she lives after the separation (Table 2). Black mothers mostly stay single female heads (0.88 at k = 1, 0.74 at
k = 10). White mothers repartner much sooner: 0.83 are single at k = 1 and 0.47 at k = 10. Reconciliations with the
ex-husband are 12% / 8% at k = 0 and below 5% from k = 2 on.

## Input 1: child support (Diagnostic B, monthly transfer)

Her own child-support income, 2000 dollars per month (annual / 12), zeros included. The sample is single mothers
(female heads, the model's V^S) with a child 0-17 in the unit, k = 0-10.

| | 1 child | 2 children | 3+ children | All | Share receiving | Mean if receiving | CS / her labor income |
|---|---|---|---|---|---|---|---|
| Black | 102 (11) | 159 (16) | 134 (17) | **132 (10)** | 0.380 | 347 | 0.076 |
| White | 253 (20) | 362 (23) | 424 (51) | **327 (17)** | 0.643 | 509 | 0.165 |

- Black - White gap: monthly amount -196*** (s.e. 20; p<0.001; N = 4,213 woman-years), and -210*** (s.e. 21;
  p<0.001) with children-count, k and calendar-year FE. Share receiving: -0.264*** (s.e. 0.026; p<0.001); with FE,
  -0.277*** (p<0.001).
- Profile over time since the separation: Black 102 / 140 / 146 and White 272 / 377 / 339 at k = 0-1 / 2-4 / 5-10.
  A constant transfer is a fair approximation after the separation year.
- Calendar period: Black 120 / 146 / 133 and White 335 / 406 / 242 in 1984-95 / 1996-2007 / 2008-21. The White
  amount falls after 2007; the Black amount is flat.
- Proposed input: cs(r, n) = the 'All' column by race, or by race x child count from the first three columns, in
  2000 dollars per month while the separated wife has a child under 18. It is zero after the youngest child turns 18,
  since the sample conditions on a child in the unit.

## Input 2: remarriage hazard (Diagnostic B, end of record)

| | Cumulative share by end of year 1 | year 4 | year 9 | Annual hazard, years 0-9 | Monthly equivalent |
|---|---|---|---|---|---|
| Remarriage, Black | 0.009 | 0.110 | 0.244 | **0.026 (0.0023)** | 0.0022 |
| Remarriage, White | 0.067 | 0.275 | 0.473 | **0.061 (0.0029)** | 0.0052 |
| New partner (remarriage or cohabiting 'wife'), Black | 0.023 | 0.130 | 0.277 | 0.031 (0.0024) | 0.0026 |
| New partner, White | 0.114 | 0.383 | 0.576 | 0.084 (0.0037) | 0.0073 |

- Black - White annual remarriage hazard: -0.035*** (s.e. 0.004; p<0.001; N = 10,384 woman-years at risk). For a new
  partner it is -0.053*** (s.e. 0.004; p<0.001; N = 9,767).
- The hazard is close to zero in the separation year (Black 0.002 and White 0.015 by the end of year 0). The
  Kaplan-Meier curve implies about 0.035 (Black) / 0.081 (White) a year in years 2-4 and 0.032 / 0.062 in years
  5-9. A constant hazard from the month after separation is the zero-parameter version. A two-piece hazard (zero in
  year 0, then the 2-9 rate) is the closer one.
- Proposed input: the remarriage rate in the 'Annual hazard' column, converted to a monthly rate
  (1 - (1 - h)^(1/12)). It ends the simulated record, as the couple's PSID record ends. The 'new partner' rate is
  the upper bound if cohabitation is also treated as leaving V^S.

## Untargeted validation rows (single mothers, k = 1-5, against married mothers 1984-2021)

| | Black | White |
|---|---|---|
| Employed, single mothers k = 1-5 (married mothers) | 0.85 (0.797) | 0.90 (0.787) |
| Difference vs married mothers, age-group and year FE | 0.036** (0.016; p=0.030) | 0.126*** (0.010; p<0.001) |
| Within mother: single k = 1-5 vs married k = -3..-1 (mother FE) | 0.035** (0.014; p=0.016; N 2,249) | 0.118*** (0.014; p<0.001; N 3,385) |
| Annual hours, within mother | +204*** (36; p<0.001) | +407*** (34; p<0.001) |
| AFDC/TANF, single mothers k = 1-5 (married mothers) | 0.10-0.16 (0.039) | 0.02-0.08 (0.011) |
| AFDC/TANF, within mother | 0.075*** (0.014; p<0.001) | 0.030*** (0.008; p<0.001) |
| Food stamps / SNAP, single mothers k = 1-5 (married mothers) | 0.32-0.36 (0.179) | 0.14-0.21 (0.052) |
| Food stamps, within mother | 0.101*** (0.020; p<0.001) | 0.106*** (0.014; p<0.001) |

Separated mothers work more than married mothers and more than they did themselves before the separation. The rise
is three times larger for White mothers. Receipt rises too. The model's V^S should produce both (its single-parent
budget has SNAP and the single-parent EITC), and these are the rows for `fit_table.py`'s 'Validation' block.

## Separations after the husband's displacement (the model's post-displacement separations)

The comparison is single mothers whose ex-husband had been displaced in s-2..s against the other single mothers
(k = 0-10 for child support, k = 1-5 otherwise).

- Child support is lower: Black -88*** a month (s.e. 16; p<0.001) and White -155*** (s.e. 36; p<0.001). Share
  receiving: Black -0.166*** (p<0.001), White -0.095* (p=0.093). Pooled: -116*** a month (p<0.001; N 4,213; 176
  mothers with a displaced ex-husband).
- Program receipt is higher. Pooled AFDC/TANF +0.072** (p=0.027) and food stamps +0.114*** (p=0.003). For Black
  mothers, food stamps +0.129** (p=0.020) and AFDC/TANF +0.095* (p=0.070).
- Black mothers' employment is lower: -0.090* (p=0.055). For White mothers it is -0.013 (p=0.654).
- The remarriage hazard is the same: 0.000 (s.e. 0.005; p=0.935, race FE).

A separation that follows his job loss leaves the wife with about half the child support (Black -88 of 132, i.e.
-67%; White -155 of 327, -47%), consistent with his lower ability to pay. A child-support input set at the average therefore overstates what the post-displacement separated wife
receives. If Diagnostic B moves the fit, the zero-parameter refinement is cs scaled by the displaced/not ratio
(Black 0.33 and White 0.53 of the average), applied to separations that occur while the husband is displaced.

## Paper and model document (text for the lead; not edited here)

Suggested sec7 'Marriage and separation' footnote, at "there is no remarriage within the horizon and no child
support" (line ~302), with the same text in model_document Section 11:

> In the PSID, separated mothers with children who remain single receive on average \$132 (Black) and \$327
> (White) a month in child support (2000 dollars; 38\% and 64\% receive any; difference $-196^{***}$, $p<0.001$),
> and remarry at annual rates of 2.6\% and 6.1\% ($-3.5$ points$^{***}$, $p<0.001$); a quarter of Black and
> half of White separated mothers have remarried within ten years. Both would make the separated state less bleak,
> more so for White wives. Separated mothers work more than married mothers (0.85 and 0.90 against 0.80 and
> 0.79; within mother $+3.5^{**}$ and $+11.8^{***}$ points) and receive AFDC/TANF and food stamps more often.
> When the husband had been displaced before the separation, the mother receives \$116 a month less
> ($p<0.001$). Code: \texttt{IGE/76.SeparatedMothers.py}.

EVIDENCE 3.96-3.98 (for the lead): 3.96 child support (input 1); 3.97 remarriage / new-partner hazard (input 2); 3.98
single mothers' work and receipt, and the displaced-ex-husband contrast.

## Caveats

- Separation dates come from the marriage history (separation year, else divorce year). Mothers must be observed
  married in s-3..s+1, so separations of couples who joined the PSID after separating are absent.
- Child support is her own report of receipt. In 1994-2003 it is built from amount x time unit x months; 4 annual
  values above \$60,000 (miscoded units, up to \$624,000) are set to missing. From 2005 it is the PSID's generated
  annual total.
- Status is measured at the interview, and outcomes refer to the preceding calendar year. In the biennial era every
  other year is unobserved; the hazards use the marriage-history years, so they are not affected.
- The comparisons with married mothers and with mothers whose husband was not displaced are descriptive, not causal.
