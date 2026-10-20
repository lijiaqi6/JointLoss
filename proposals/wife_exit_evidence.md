# Why do wives leave employment at 1% a month? Evidence for the Paper A model decision (WP1, 2026-10-19)

Script `IGE/63.WifeExitWhy.py`; every estimate in `output/wife_exit_why.csv` and the tables in
`output/wife_exit_why.md`. Sample everywhere: married wives aged 25-59 whose husband is employed. CPS 1994-2023
and SIPP 2003-2016 use the persistent monthly exit (employed at t-1 and t, not employed at t+1 and t+2; CPS as in
`cps_wife_exit_p`, so job losers do not count as exits). The PSID 1968-1996 annual exit is hours > 0 in year t and
0 in t+1. Regressions are LPMs in percentage points, with s.e. clustered by household (CPS, SIPP) or 1968 family
(PSID). *** p<0.01, ** p<0.05, * p<0.1. These are associations, not causal effects.

## 1. The key statistic: a high-churn equilibrium with spells of about a year

| | CPS | SIPP | PSID (annual) |
|---|---|---|---|
| persistent exit, % a month | 0.97 | 0.91 (0.68 without an involuntary job end) | 8.29 % a year |
| persistent entry, % a month | 3.15 (Black 3.97, White 3.17) | 2.45 | |
| employment share, % | 71.7 | 71.2 | |
| back in work 6 / 12 / 24 months after the exit | 47% employed 11 months later (stayers 94%) | KM 37 / 53 / 66% | 38% in the next year, 54% within 2, 69% within 4 |

- **Steady state.** The flows balance: x·e/(1-e) = 0.97 x 0.717 / 0.283 = 2.5% a month of entry is needed, and the
  CPS shows 3.2% (the rest replaces job losers). The SIPP gives 2.2% against 2.45%.
- **What the data describe.** About half of the wives who leave are back in work within a year (SIPP KM 53.0%,
  s.e. 0.8; CPS 47.4%, s.e. 1.1). A monthly exit of 0.97% would mean 11.6% of employed wives leaving each year,
  but only 8.3% have a full calendar year with zero hours (PSID). So most spells are shorter than a year.
- **What the model does.** At 0.14% a month it is a low-churn model in which exits are rare and close to permanent.
  The spell-length distribution is the statistic that separates the candidate features.

## 2. What happens around the exit: shares x hazards (SIPP, pooled 0.91%)

| cell | % of wife-months | hazard % | % of exits | joint LPM (pp) |
|---|---|---|---|---|
| job tenure 0-5 months | 8.1 | 2.06 | 18.3 | +1.33*** (0.07; p<0.001) |
| job tenure 6-11 months | 7.3 | 1.60 | 12.8 | +0.91*** (0.07; p<0.001) |
| job tenure 12-35 months | 17.8 | 1.10 | 21.8 | +0.42*** (0.04; p<0.001) |
| job tenure 36+ (base) | 56.4 | 0.54 | 33.6 | - |
| usual hours < 20 | 5.5 | 2.64 | 15.9 | +1.85*** (0.10; p<0.001) |
| usual hours 20-34 | 13.7 | 1.22 | 18.5 | +0.53*** (0.04; p<0.001) |
| child aged 0 in the household at t+1..t+9 | 6.6 | 1.73 | 12.6 | +1.04*** (0.11; p<0.001) |
| husband's job change at t-2..t+1 | 3.0 | 1.69 | 5.7 | +0.70*** (0.10; p<0.001) |
| an earlier persistent exit in the panel | 6.3 | 2.21 | 15.4 | (Section 4) |
| wife 55-59 | 9.2 | 0.80 | 8.1 | +0.07 (0.06; p=0.214) |
| Black husband | 8.2 | 0.90 | 8.2 | +0.11** (0.05; p=0.017) |

Other controls: the wife's education, which has a strong gradient (< high school +0.65***, BA+ -0.45***), age,
youngest child, and panel x rotation x month FE. Without involuntary job ends the coefficients keep their size
(tenure 0-5 months +0.77***, p<0.001; birth window +0.97***, p<0.001).

**CPS** (no tenure or hours in this extract): youngest child aged 0 +0.95*** (0.09; p<0.001), 1-2 +0.51***, 3-5
+0.56***. Self-employed +0.85***, government -0.16***, wife < high school +0.90***. Wives whose youngest child is
0-2 account for 17.8% of exits. 93% of the exits go out of the labor force; 4.6% are unemployed job leavers.

**PSID**: a birth in t+1 +6.77pp*** (0.76; p<0.001) and a birth in t +5.64pp*** (0.88; p<0.001), against a mean of
8.29%. Births in t or t+1 account for about a quarter of annual exits. Hours in t matter most: 1-499 hours +24.99pp***
(0.66; p<0.001), and wives under 500 hours provide 43.9% of exits; 500-999 hours +12.99pp***. His labor income
changes little: a rise > 25% gives +1.96pp*** (0.36; p<0.001), a fall > 25% +0.59pp* (0.36; p=0.095), and
d log of his labor income gives +0.07pp per 10% (0.03; p=0.027).

## 3. Stated reasons (SIPP; the reason of her job that ended at t-1..t+2)

| | all | child aged 0 at t+1..t+9 | youngest 0-2 | no child < 18 | wife 55-59 | Black | White |
|---|---|---|---|---|---|---|---|
| involuntary (layoff 12.0, temp job ended 6.6, fired 3.3, closure 1.7, other 1.5) | 25.1 | 14.2 | 20.5 | 26.7 | 25.2 | 26.2 | 25.2 |
| childcare / family obligations | 11.5 | 31.0 | 22.6 | 7.0 | 2.1 | 9.2 | 11.8 |
| unsatisfactory arrangements / other quit | 17.6 | 20.1 | 17.1 | 17.2 | 12.1 | 16.1 | 17.7 |
| quit to take another job | 4.2 | 3.4 | 4.7 | 4.1 | 2.0 | 4.9 | 4.3 |
| own illness / injury | 3.8 | 1.7 | 1.8 | 5.3 | 4.1 | 5.2 | 3.6 |
| retirement | 1.5 | 0.2 | 0.3 | 3.5 | 11.1 | 1.7 | 1.6 |
| school | 1.7 | 0.7 | 1.0 | 1.9 | 0.3 | 1.2 | 1.7 |
| no job end recorded | 34.5 | 28.7 | 32.0 | 34.2 | 43.1 | 35.5 | 34.1 |

The PSID status at the interview after the zero-hours year is "keeping house" for 75.6% of exits. The rest:
working 11.5% (a new spell has already begun), looking 4.7%, student 4.0%, disabled 2.2%, retired 1.5%.

## 4. Spell length and persistence

- **Return within 12 months (SIPP KM, %).** All exits 53.0. Involuntary 60.1. Unsatisfactory / other quit 52.8.
  Childcare / family 38.9. Own illness 36.8. Retirement 36.9. Birth window 39.6, against 55.1 without one; at 24
  months 59.0 against 67.3. Among exits seen 12 months later, the birth window lowers the return by -12.6pp***
  (2.8; p<0.001), and involuntary job ends raise it by +18.0pp*** (3.1; p<0.001) relative to childcare / family.
- **Same wives exit again.** In the PSID, 32.4% of couples with an exit have two or more in about 7 eligible years,
  and they account for 54.2% of all exits. An earlier exit of the same wife raises the annual exit by +8.13pp***
  (0.41; p<0.001), and by +3.84pp*** (0.38; p<0.001) with her hours in t controlled. In the SIPP an earlier exit
  adds +1.39pp*** (0.09; p<0.001), and +0.91pp*** (0.09; p<0.001) with tenure and hours controlled. Tenure 0-5
  months stays at +1.17pp*** (0.07; p<0.001) in that regression.

## 5. Mapping to candidate model features

| finding | feature | cost | verdict |
|---|---|---|---|
| exits concentrated in the first year of a job (tenure < 12 months: 15% of months, 31% of exits; hazard 2.06% vs 0.54%); re-entrants exit again | **new-job match / separation hazard**: an extra exit hazard (or a match-quality draw) in the first ~12 months of a job | one binary state for employed wives (new / established job); 1-2 parameters, identified by the SIPP tenure profile | **first choice**: it produces the churn and the repeat exits together |
| low hours (< 20 h: 5% of months, 16% of exits; PSID < 500 h: 44% of annual exits); an earlier exit predicts the next one after controlling for tenure and hours (+0.91pp***, +3.84pp***) | **persistent work-cost heterogeneity** (wife type) | one state, which doubles solve time; 2 parameters | second step, only if the repeat-exit moment still misfits after the new-job hazard |
| birth window: +1.04pp***, 12.6% of exits (CPS youngest 0-2: 18%); 31% childcare / family reasons; longer spells (40% back within 12 months) | **birth-timed transitory work-cost shock** (theta jump for k months after a birth) | no new state (the child chain is there); 1-2 parameters | cheap add-on; covers about one exit in eight, so it cannot close the gap alone |
| husband's job change +0.70pp*** (6% of exits); his income rise +1.96pp***, fall +0.59pp* | income effect | none | nothing to add; the model's wealth and income effect carries it |
| illness 3.8%, retirement 1.5% of exits (11% at 55-59); 55-59 has no excess hazard (+0.07, p=0.214) | health / retirement margin | one state | footnote only |
| 25% of persistent exits follow an involuntary job end but she reports no search (93% of CPS exits go out of the labor force) | job loss followed by non-search | none: the model's job-loss hazard plus the participation choice | check that the model's job losers can exit the labor force; this is part of the 1% |

**Recommendation for the PI.** The binding fact is short spells: about half the exiting wives return within a
year. Exits are concentrated on new jobs, and the same wives exit repeatedly. A transitory birth shock covers one
exit in eight. A persistent type alone would make spells long. Add the new-job hazard first: it costs one binary
state for employed wives, and the SIPP tenure profile identifies it as a new moment block (hazard at tenure 0-5,
6-11, 12-35, 36+). Re-estimate, then check the PSID repeat-exit share (32%) and the SIPP 12-month return (53%)
as untargeted validation. Add the type only if they misfit. The birth-timed theta jump has no state cost and can
ride along.

## Footnote-ready sentences (numbers from IGE/63.WifeExitWhy.py)

1. "Married wives (25-59, husband employed) leave employment at 0.97% a month in the CPS (persistent exits,
   1994-2023) and 0.91% in the SIPP (2003-2016). Spells are short: 53% are back in work within 12 months
   (Kaplan-Meier, SIPP) and 47% are employed 11 months after the exit month (CPS)."
2. "The exit hazard falls with job tenure: 2.06% a month in the first six months of a job against 0.54% after
   three years (LPM difference +1.33pp***, s.e. 0.07, p<0.001, with hours, children, education, age, race and
   panel-month fixed effects). Jobs held less than a year account for 31% of exits and 15% of wife-months."
3. "A child aged 0 around the exit raises the hazard by 1.04pp*** (s.e. 0.11, p<0.001) and accounts for 12.6% of
   exits. These spells are longer: 40% return within a year, against 55% of other exits."
4. "Stated reasons: involuntary job end 25%, childcare or family 11%, unsatisfactory arrangements or other quits
   18%, own illness 4%, retirement 1.5% (11% at ages 55-59); no job end is recorded for 34%."
5. "In the PSID (1968-1996), 32% of wives with an annual exit leave again within the window; an earlier exit
   raises the next year's exit by 3.84pp*** (s.e. 0.38, p<0.001) conditional on hours."

Caveats: SIPP tenure is the employer-specific start date, from TSJDATE in 2004/08 and from the start year and month
or the first month seen in 2014. Tenure is unknown for 10% of wife-months. The SIPP seam heaps transitions; the
panel x rotation x month FE absorb the level, not the timing. The "previous exit" in the SIPP is left-censored at
the panel start, so the type and tenure channels are separated only partly. The PSID annual exit captures only
spells that cover a whole calendar year.
