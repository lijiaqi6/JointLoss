# PSID children: mother's work at the birth, father's job loss, separation, welfare - descriptives

Built by `9.ChildExposure.py` (exposures), `9a.CDS.py` (CDS scores), `9b.ChildDescriptives.py` (this file), 2026-10-17. **All numbers below are associations, not causal effects.** Unweighted; race = head's race in the first family unit the child is seen in.

## 1. Descriptives by race

Children born 1968-2020 (all), the adult-earnings sample (also in `psid_kids.pkl` with log lifetime earnings: head's child at 12-17, 3+ years as head/wife at 25-55) and the CDS sample (child x wave assessments at 5-12). Cells: mean (N non-missing).

| | All White | All Black | Adult earnings White | Adult earnings Black | CDS 5-12 White | CDS 5-12 Black |
|---|---|---|---|---|---|---|
| Children | 13,811 | 12,634 | 2,800 | 1,949 | 3,253 | 2,817 |
| Mother employed, birth year | 0.627 (8,679) | 0.567 (6,703) | 0.620 (2,598) | 0.539 (1,623) | 0.747 (2,761) | 0.670 (1,926) |
| Mother employed, year +1 | 0.610 (8,456) | 0.587 (6,658) | 0.591 (2,591) | 0.567 (1,644) | 0.706 (2,876) | 0.697 (1,974) |
| Mother employed, year +2 | 0.624 (8,342) | 0.632 (6,743) | 0.604 (2,588) | 0.612 (1,651) | 0.717 (2,812) | 0.721 (2,083) |
| Mother's hours, year +1 | 777.409 (8,456) | 827.549 (6,658) | 658.228 (2,591) | 794.611 (1,644) | 964.679 (2,876) | 1,049.737 (1,974) |
| Father figure's job loss 0-17 (zero hours) | 0.073 (13,811) | 0.107 (12,634) | 0.076 (2,800) | 0.120 (1,949) | 0.086 (4,047) | 0.116 (3,444) |
| Father figure's job loss 0-17 (zero hours or unemployment; unemp. to 1992 only) | 0.242 (13,811) | 0.244 (12,634) | 0.436 (2,800) | 0.384 (1,949) | 0.151 (4,047) | 0.166 (3,444) |
| Years with a male head observed (0-17) | 7.024 (13,811) | 3.837 (12,634) | 13.164 (2,800) | 7.279 (1,949) | 7.616 (4,047) | 3.773 (3,444) |
| Separation/divorce 0-17, marriage history | 0.263 (13,811) | 0.214 (12,634) | 0.301 (2,800) | 0.308 (1,949) | 0.255 (4,047) | 0.242 (3,444) |
| Separation 0-17, relation change | 0.231 (13,811) | 0.247 (12,634) | 0.312 (2,800) | 0.385 (1,949) | 0.302 (4,047) | 0.335 (3,444) |
| Separation/divorce 0-17, either | 0.306 (13,811) | 0.315 (12,634) | 0.327 (2,800) | 0.429 (1,949) | 0.313 (4,047) | 0.379 (3,444) |
| Years with AFDC/TANF or food stamps, 0-5 | 0.705 (11,902) | 2.194 (10,587) | 0.528 (2,702) | 2.229 (1,809) | 0.773 (4,011) | 2.781 (3,376) |
| Years with AFDC/TANF, 0-5 | 0.189 (11,902) | 0.784 (10,587) | 0.211 (2,702) | 1.299 (1,809) | 0.164 (4,011) | 0.791 (3,376) |
| Years with food stamps, 0-5 | 0.671 (11,902) | 2.080 (10,587) | 0.493 (2,702) | 2.057 (1,809) | 0.761 (4,011) | 2.737 (3,376) |
| Years observed for welfare, 0-5 | 4.470 (13,811) | 4.059 (12,634) | 5.588 (2,800) | 5.094 (1,949) | 5.763 (4,047) | 5.513 (3,444) |
| Family income 0-5 (2000$) | 61,211.203 (11,813) | 31,013.228 (10,466) | 56,788.315 (2,701) | 30,515.635 (1,809) | 64,200.845 (4,008) | 30,229.232 (3,364) |
| Family income 6-17 (2000$) | 75,374.274 (11,274) | 36,168.516 (10,065) | 74,547.503 (2,800) | 36,453.608 (1,949) | 82,594.795 (4,009) | 35,605.473 (3,412) |
| Mother's years of education | 13.797 (12,932) | 12.988 (11,646) | 13.936 (2,768) | 13.140 (1,924) | 14.445 (4,022) | 13.467 (3,363) |
| Mother married at the birth | 0.752 (13,811) | 0.343 (12,634) | 0.908 (2,800) | 0.473 (1,949) | 0.812 (4,047) | 0.292 (3,444) |
| Mother's age at the birth | 26.807 (13,074) | 24.303 (11,922) | 26.491 (2,769) | 24.287 (1,925) | 28.005 (4,024) | 25.272 (3,374) |
| Log lifetime earnings |  |  | 10.099 (2,800) | 9.639 (1,949) |  |  |
| Log parental income 12-17 |  |  | 11.069 (2,696) | 10.273 (1,809) |  |  |
| WJ Letter-Word (std score) |  |  |  |  | 107.216 (2,436) | 98.776 (2,297) |
| WJ Applied Problems (std score) |  |  |  |  | 108.039 (2,428) | 95.101 (2,288) |
| WJ Passage Comprehension (std score) |  |  |  |  | 107.461 (2,210) | 98.585 (2,057) |
| BPI total (z within wave x age) |  |  |  |  | 0.057 (4,009) | -0.037 (3,414) |

## 2. CDS test scores at ages 5-12 on early-childhood exposures

One regression per column (outcome and race in the header). WJ standard scores (population mean 100, sd 15); BPI = behaviour problems, higher = worse, z-scored within CDS wave x age. A child assessed in two waves contributes two rows. Controls: log family income at 0-5, female; fixed effects: birth year, CDS wave. Job loss and separation count only if they happened before the test year. S.e. clustered by fam68 in parentheses; *** p<0.01, ** p<0.05, * p<0.1.

| | Letter-Word, White | Letter-Word, Black | Applied Problems, White | Applied Problems, Black | BPI (z), White | BPI (z), Black |
|---|---|---|---|---|---|---|
| Mother employed in year +1 (hours > 0) | -0.254 (1.002; p=0.800) | 0.507 (1.043; p=0.627) | 0.998 (0.879; p=0.256) | 0.075 (0.965; p=0.938) | 0.089* (0.048; p=0.062) | -0.049 (0.059; p=0.403) |
| Father figure's job loss (0-17; CDS: before the test) | -3.910** (1.830; p=0.033) | -0.658 (1.701; p=0.699) | 0.308 (1.740; p=0.859) | 0.291 (1.541; p=0.850) | -0.081 (0.101; p=0.425) | -0.108 (0.098; p=0.269) |
| Parents' separation / divorce (0-17; CDS: before the test) | 0.130 (1.116; p=0.908) | -1.036 (0.996; p=0.299) | 0.743 (1.081; p=0.492) | -0.651 (0.953; p=0.495) | 0.196*** (0.058; p=<0.001) | 0.032 (0.060; p=0.597) |
| Years with AFDC/TANF or food stamps at 0-5 | -0.310 (0.472; p=0.511) | -0.813*** (0.262; p=0.002) | -0.622 (0.415; p=0.134) | -0.372 (0.266; p=0.161) | 0.059*** (0.020; p=0.004) | 0.069*** (0.017; p=<0.001) |
| Log family income, mean at 0-5 | 6.692*** (0.914; p=<0.001) | 3.178*** (0.745; p=<0.001) | 7.140*** (0.932; p=<0.001) | 2.631*** (0.798; p=<0.001) | -0.168*** (0.043; p=<0.001) | 0.015 (0.043; p=0.721) |
| Female | 2.739*** (0.787; p=<0.001) | 3.755*** (0.862; p=<0.001) | -2.233*** (0.760; p=0.003) | 1.107 (0.960; p=0.249) | -0.094** (0.039; p=0.017) | -0.163*** (0.050; p=0.001) |
| Mean of outcome | 107.805 | 98.928 | 108.673 | 95.752 | 0.015 | -0.063 |
| N | 1,992 | 1,462 | 1,987 | 1,458 | 2,840 | 1,943 |
| Children | 1,567 | 1,165 | 1,565 | 1,160 | 2,197 | 1,533 |
| Clusters (fam68) | 654 | 438 | 654 | 437 | 781 | 487 |

Fixed effects in every column: birth year, CDS wave.

## 3. Child's log lifetime earnings on childhood exposures

Children born 1968-1997 in `psid_kids.pkl` (log of mean annual own labour earnings as head or wife at 25-55, zeros kept, 3+ years). One regression per column. Controls: log parental income (mean at 12-17, or at 0-5), female; birth-year fixed effects. S.e. clustered by fam68; *** p<0.01, ** p<0.05, * p<0.1.

| | Log earnings, White (income 12-17) | Log earnings, Black (income 12-17) | Log earnings, White (income 0-5) | Log earnings, Black (income 0-5) |
|---|---|---|---|---|
| Mother employed in year +1 (hours > 0) | 0.042 (0.040; p=0.291) | 0.044 (0.057; p=0.440) | 0.044 (0.039; p=0.266) | 0.063 (0.057; p=0.265) |
| Father figure's job loss (0-17; CDS: before the test) | -0.099 (0.065; p=0.131) | -0.214*** (0.081; p=0.009) | -0.126* (0.068; p=0.061) | -0.207*** (0.080; p=0.010) |
| Parents' separation / divorce (0-17; CDS: before the test) | -0.061 (0.042; p=0.147) | -0.057 (0.053; p=0.282) | -0.135*** (0.042; p=0.001) | -0.129** (0.051; p=0.012) |
| Years with AFDC/TANF or food stamps at 0-5 | -0.066*** (0.017; p=<0.001) | -0.067*** (0.015; p=<0.001) | -0.042* (0.023; p=0.064) | -0.064*** (0.018; p=<0.001) |
| Log parental income, mean at 12-17 | 0.375*** (0.031; p=<0.001) | 0.235*** (0.042; p=<0.001) |  |  |
| Log family income, mean at 0-5 |  |  | 0.439*** (0.039; p=<0.001) | 0.219*** (0.057; p=<0.001) |
| Female | -0.563*** (0.036; p=<0.001) | -0.159*** (0.050; p=0.001) | -0.543*** (0.035; p=<0.001) | -0.162*** (0.049; p=<0.001) |
| Mean of outcome | 10.131 | 9.651 | 10.118 | 9.643 |
| N | 2,521 | 1,545 | 2,585 | 1,632 |
| Children | 2,521 | 1,545 | 2,585 | 1,632 |
| Clusters (fam68) | 897 | 469 | 911 | 479 |

Fixed effects in every column: birth year.

## Notes

- Associations only. Mothers who work in the year after a birth, families hit by job loss or separation, and welfare recipients differ in unobserved ways; nothing here identifies the time-vs-money trade-off.
- Mother's hours: family-file head/wife hours, else individual-file hours (1967-1992), else year-before-last weeks x hours/week (1997, 1999, 2001). After 1996 the survey is biennial and hours refer to even years only, so year +1 is missing for even-year births from 2002 on; children whose mother is not head or wife after 1993 have no hours.
- Father figure = male head of the child's family unit (biological father, stepfather or partner); children never living with one have job loss = 0. In the biennial era job loss compares hours two years apart.
- Welfare counts only head/wife AFDC/TANF (1967: head only) and family food stamps; no food stamp item for 1972. Years observed at 0-5 fall in the biennial era (partly offset by the 'two years ago' items).
- CDS: WJ-R (1997-2007), WJ-III (2014), WJ-IV (2019) - CDS-wave fixed effects absorb level differences; 2019 scores average about 5 points lower. CDS-2020/2021/2024 have no WJ assessment or BPI. Children born 2001+ are tested only in 2014/2019, so the birth-year fixed effects also absorb the WJ-III/IV vs WJ-R level shift; and since mother's year +1 hours exist only for odd birth years after 2000, the 2014/2019 rows are odd-year births only.
- Later birth cohorts are censored for the 0-17 measures (job loss, separation).
