# Husband-specific industry shocks at a birth and the wife's work (18.HusbandIndustryShocks.py)

PSID births 1980-2019 to married mothers; husband = head of the mother's family in the latest wave in [b-3, b-1]; his main industry in that wave mapped to 16 sectors (8a.StateShocks.py). Shock = CPS MORG (men) employment growth or unemployment rate in his sector in the birth year b, national leave-own-state-out or state x sector, relative to the pre-birth trend (value in b minus the mean over b-3..b-1). Each column is one regression (outcome in the header); regressors as rows; panels are separate regressions. OLS with state, birth-year and husband-sector FE (variation within sector over time and across states); controls: mother's age, age^2, education (<12, 13-15, 16+, missing; base 12), birth order (2, 3+, missing), Black.

Cell: coefficient, stars, (s.e. clustered by state x sector; p-value); second line: s.e. clustered by the 16 sectors (cluster-t p with G-1 df) and the wild cluster bootstrap-t p-value (Webb weights, null imposed, 999 draws); stars on the second line use the bootstrap p. *** p<0.01, ** p<0.05, * p<0.1. The shock varies at sector x year (nationally), so the state x sector clusters ignore the common sector-year component; the sector-clustered bootstrap is the inference to rely on.

Units and signs. Growth shocks in log points x 100 (higher = better for the husband's sector); unemployment-rate shocks in percentage points (higher = worse). The insurance channel predicts: growth shock -> husband hours +, wife employment -; unemployment shock -> husband hours -, wife employment +. S.d. of the shocks in the main sample (raw / after the FE and controls): g_nat_dt 4.05 / 3.46; g_nat 3.53 / 2.85; ur_nat_dt 1.94 / 1.01; g_st_dt 13.73 / 13.26.

Husband outcomes: 'pre' = his hours (earnings) in b-1, else b-2 (calendar years 1997 and 1999 are not observed; earnings for odd years after 1997 are not observed). Wife outcomes: employed = annual hours > 0; 500+ hours; annual hours (zeros kept).

### Table 1. First stage: the husband's own outcomes (mothers employed in b-1)

| | Husband hours b - pre | Husband hours b+1 - pre | Husband hours fell >= 25% in b | Husband hours fell >= 25% in b+1 | Husband log earnings b - pre | Husband employed in b |
|---|---|---|---|---|---|---|
| **A. National sector employment growth, men, leave-one-state-out, relative to pre-birth trend** | | | | | | |
| g_nat_dt | 5.6326** (2.6024; p=0.031)<br><sub>sector-cl. (2.0534; p=0.015; WCB p=0.040)**</sub> | 5.6752* (3.2361; p=0.080)<br><sub>sector-cl. (3.2214; p=0.098; WCB p=0.102)</sub> | -0.0020 (0.0013; p=0.141)<br><sub>sector-cl. (0.0008; p=0.024; WCB p=0.029)**</sub> | -0.0012 (0.0014; p=0.418)<br><sub>sector-cl. (0.0012; p=0.364; WCB p=0.342)</sub> | 0.0056* (0.0030; p=0.062)<br><sub>sector-cl. (0.0031; p=0.093; WCB p=0.136)</sub> | 0.0002 (0.0005; p=0.737)<br><sub>sector-cl. (0.0003; p=0.662; WCB p=0.664)</sub> |
| N | 3,939 | 3,822 | 3,873 | 3,761 | 2,907 | 3,959 |
| Mothers / women | 2,771 | 2,671 | 2,735 | 2,635 | 2,216 | 2,781 |
| Clusters: state x sector / sector | 590 / 16 | 585 / 16 | 588 / 16 | 583 / 16 | 548 / 16 | 590 / 16 |
| Mean outcome | -4.061 | -0.293 | 0.090 | 0.112 | 0.066 | 0.983 |
| First-stage F (state x sector cl.) | 4.68 | 3.08 | 2.17 | 0.66 | 3.49 | 0.11 |
| First-stage F (sector cl.) | 7.52 | 3.10 | 6.26 | 0.88 | 3.22 | 0.20 |
| Split-sample IV: F of even-month shock |  |  |  |  |  |  |
| **B. National sector employment growth, men, leave-one-state-out, raw** | | | | | | |
| g_nat | 7.4213** (3.1924; p=0.020)<br><sub>sector-cl. (2.2899; p=0.005; WCB p=0.022)**</sub> | 6.4677* (3.8816; p=0.096)<br><sub>sector-cl. (2.8655; p=0.039; WCB p=0.028)**</sub> | -0.0036** (0.0017; p=0.042)<br><sub>sector-cl. (0.0011; p=0.007; WCB p=0.001)***</sub> | -0.0026 (0.0017; p=0.133)<br><sub>sector-cl. (0.0015; p=0.106; WCB p=0.097)*</sub> | 0.0084** (0.0035; p=0.019)<br><sub>sector-cl. (0.0035; p=0.030; WCB p=0.085)*</sub> | 0.0003 (0.0007; p=0.671)<br><sub>sector-cl. (0.0007; p=0.677; WCB p=0.695)</sub> |
| N | 4,064 | 3,947 | 3,997 | 3,885 | 3,031 | 4,084 |
| Mothers / women | 2,861 | 2,761 | 2,825 | 2,725 | 2,306 | 2,871 |
| Clusters: state x sector / sector | 593 / 16 | 589 / 16 | 591 / 16 | 587 / 16 | 552 / 16 | 593 / 16 |
| Mean outcome | -3.797 | -1.478 | 0.091 | 0.113 | 0.066 | 0.983 |
| First-stage F (state x sector cl.) | 5.40 | 2.78 | 4.17 | 2.27 | 5.54 | 0.18 |
| First-stage F (sector cl.) | 10.50 | 5.09 | 9.88 | 2.96 | 5.76 | 0.18 |
| Split-sample IV: F of even-month shock |  |  |  |  |  |  |
| **C. National sector unemployment rate, men, leave-one-state-out, relative to pre-birth trend** | | | | | | |
| ur_nat_dt | -13.2917 (9.1177; p=0.145)<br><sub>sector-cl. (6.2764; p=0.051; WCB p=0.065)*</sub> | -4.2822 (11.1842; p=0.702)<br><sub>sector-cl. (7.5371; p=0.578; WCB p=0.576)</sub> | 0.0032 (0.0055; p=0.561)<br><sub>sector-cl. (0.0043; p=0.467; WCB p=0.520)</sub> | 0.0006 (0.0056; p=0.909)<br><sub>sector-cl. (0.0040; p=0.875; WCB p=0.883)</sub> | -0.0268** (0.0128; p=0.037)<br><sub>sector-cl. (0.0100; p=0.017; WCB p=0.099)*</sub> | -0.0015 (0.0018; p=0.425)<br><sub>sector-cl. (0.0025; p=0.567; WCB p=0.635)</sub> |
| N | 4,134 | 4,014 | 4,066 | 3,951 | 3,095 | 4,154 |
| Mothers / women | 2,886 | 2,785 | 2,850 | 2,749 | 2,330 | 2,896 |
| Clusters: state x sector / sector | 595 / 16 | 590 / 16 | 593 / 16 | 588 / 16 | 554 / 16 | 595 / 16 |
| Mean outcome | -6.521 | 1.856 | 0.092 | 0.113 | 0.064 | 0.982 |
| First-stage F (state x sector cl.) | 2.13 | 0.15 | 0.34 | 0.01 | 4.39 | 0.64 |
| First-stage F (sector cl.) | 4.48 | 0.32 | 0.56 | 0.03 | 7.15 | 0.34 |
| Split-sample IV: F of even-month shock |  |  |  |  |  |  |
| **D. State x sector employment growth, men, relative to trend (full CPS sample)** | | | | | | |
| g_st_dt | -0.1667 (0.6364; p=0.793)<br><sub>sector-cl. (0.5449; p=0.764; WCB p=0.764)</sub> | -0.2641 (0.7850; p=0.737)<br><sub>sector-cl. (0.7980; p=0.745; WCB p=0.744)</sub> | -0.0002 (0.0004; p=0.646)<br><sub>sector-cl. (0.0004; p=0.655; WCB p=0.674)</sub> | 0.0000 (0.0004; p=0.929)<br><sub>sector-cl. (0.0004; p=0.927; WCB p=0.911)</sub> | 0.0006 (0.0008; p=0.438)<br><sub>sector-cl. (0.0011; p=0.562; WCB p=0.577)</sub> | -0.0003* (0.0002; p=0.063)<br><sub>sector-cl. (0.0001; p=0.042; WCB p=0.044)**</sub> |
| N | 3,889 | 3,770 | 3,823 | 3,709 | 2,874 | 3,909 |
| Mothers / women | 2,744 | 2,640 | 2,708 | 2,604 | 2,198 | 2,754 |
| Clusters: state x sector / sector | 561 / 16 | 557 / 16 | 559 / 16 | 555 / 16 | 524 / 16 | 561 / 16 |
| Mean outcome | -2.897 | 0.202 | 0.091 | 0.112 | 0.066 | 0.982 |
| First-stage F (state x sector cl.) | 0.07 | 0.11 | 0.21 | 0.01 | 0.60 | 3.48 |
| First-stage F (sector cl.) | 0.09 | 0.11 | 0.21 | 0.01 | 0.35 | 4.93 |
| Split-sample IV: F of even-month shock |  |  |  |  |  |  |
| **E. State x sector growth, split sample: odd-month shock instrumented by even-month shock (2SLS)** | | | | | | |
| g_st_h1_dt (2SLS) | -4.0762 (14.3140; p=0.776)<br><sub>sector-cl. (13.5578; p=0.768)</sub> | -8.1913 (13.4354; p=0.542)<br><sub>sector-cl. (9.7383; p=0.413)</sub> | -0.0064 (0.0099; p=0.517)<br><sub>sector-cl. (0.0118; p=0.595)</sub> | 0.0049 (0.0069; p=0.478)<br><sub>sector-cl. (0.0048; p=0.328)</sub> | 0.0125 (0.0218; p=0.568)<br><sub>sector-cl. (0.0317; p=0.700)</sub> | -0.0007 (0.0039; p=0.858)<br><sub>sector-cl. (0.0037; p=0.849)</sub> |
| N | 3,872 | 3,754 | 3,806 | 3,693 | 2,866 | 3,892 |
| Mothers / women | 2,732 | 2,630 | 2,696 | 2,594 | 2,193 | 2,742 |
| Clusters: state x sector / sector | 558 / 16 | 553 / 16 | 556 / 16 | 551 / 16 | 521 / 16 | 558 / 16 |
| Mean outcome | -2.289 | 0.417 | 0.090 | 0.112 | 0.066 | 0.982 |
| First-stage F (state x sector cl.) | 0.08 | 0.37 | 0.42 | 0.50 | 0.33 | 0.03 |
| First-stage F (sector cl.) | 0.09 | 0.71 | 0.30 | 1.02 | 0.15 | 0.04 |
| Split-sample IV: F of even-month shock | 1.31 | 3.80 | 1.31 | 4.18 | 1.26 | 1.20 |
| State FE, birth-year FE, husband-sector FE, mother controls | yes | yes | yes | yes | yes | yes |

### Table 2. Wife's work after the birth (mothers employed in b-1)

| | Wife employed b+1 | Wife employed b+2 | Wife 500+ hours b+1 | Wife 500+ hours b+2 | Wife hours b+1 | Wife hours b+2 |
|---|---|---|---|---|---|---|
| **A. National sector employment growth, men, leave-one-state-out, relative to pre-birth trend** | | | | | | |
| g_nat_dt | -0.0004 (0.0018; p=0.841)<br><sub>sector-cl. (0.0018; p=0.841; WCB p=0.829)</sub> | 0.0018 (0.0017; p=0.306)<br><sub>sector-cl. (0.0022; p=0.436; WCB p=0.465)</sub> | -0.0008 (0.0020; p=0.675)<br><sub>sector-cl. (0.0017; p=0.640; WCB p=0.630)</sub> | 0.0008 (0.0019; p=0.674)<br><sub>sector-cl. (0.0026; p=0.759; WCB p=0.752)</sub> | 1.3183 (3.9383; p=0.738)<br><sub>sector-cl. (3.5291; p=0.714; WCB p=0.722)</sub> | 0.9497 (3.9978; p=0.812)<br><sub>sector-cl. (4.9023; p=0.849; WCB p=0.847)</sub> |
| N | 3,961 | 3,807 | 3,948 | 3,787 | 3,948 | 3,787 |
| Mothers / women | 2,763 | 2,656 | 2,757 | 2,646 | 2,757 | 2,646 |
| Clusters: state x sector / sector | 591 / 16 | 586 / 16 | 591 / 16 | 586 / 16 | 591 / 16 | 586 / 16 |
| Mean outcome | 0.818 | 0.822 | 0.715 | 0.730 | 1265.232 | 1299.462 |
| Split-sample IV: F of even-month shock |  |  |  |  |  |  |
| **B. National sector employment growth, men, leave-one-state-out, raw** | | | | | | |
| g_nat | -0.0010 (0.0024; p=0.681)<br><sub>sector-cl. (0.0022; p=0.658; WCB p=0.672)</sub> | 0.0007 (0.0021; p=0.737)<br><sub>sector-cl. (0.0027; p=0.801; WCB p=0.814)</sub> | -0.0007 (0.0025; p=0.778)<br><sub>sector-cl. (0.0020; p=0.726; WCB p=0.719)</sub> | 0.0007 (0.0025; p=0.789)<br><sub>sector-cl. (0.0028; p=0.818; WCB p=0.799)</sub> | 0.3500 (4.8041; p=0.942)<br><sub>sector-cl. (3.5667; p=0.923; WCB p=0.934)</sub> | -0.5809 (4.9168; p=0.906)<br><sub>sector-cl. (5.6247; p=0.919; WCB p=0.929)</sub> |
| N | 4,082 | 3,925 | 4,069 | 3,905 | 4,069 | 3,905 |
| Mothers / women | 2,849 | 2,740 | 2,843 | 2,730 | 2,843 | 2,730 |
| Clusters: state x sector / sector | 595 / 16 | 590 / 16 | 595 / 16 | 590 / 16 | 595 / 16 | 590 / 16 |
| Mean outcome | 0.813 | 0.817 | 0.708 | 0.722 | 1251.366 | 1283.861 |
| Split-sample IV: F of even-month shock |  |  |  |  |  |  |
| **C. National sector unemployment rate, men, leave-one-state-out, relative to pre-birth trend** | | | | | | |
| ur_nat_dt | 0.0017 (0.0058; p=0.772)<br><sub>sector-cl. (0.0033; p=0.615; WCB p=0.610)</sub> | -0.0051 (0.0057; p=0.371)<br><sub>sector-cl. (0.0031; p=0.124; WCB p=0.107)</sub> | 0.0079 (0.0070; p=0.258)<br><sub>sector-cl. (0.0056; p=0.178; WCB p=0.192)</sub> | 0.0028 (0.0067; p=0.682)<br><sub>sector-cl. (0.0047; p=0.568; WCB p=0.634)</sub> | 7.2850 (13.2360; p=0.582)<br><sub>sector-cl. (10.1644; p=0.485; WCB p=0.493)</sub> | 10.2094 (13.4090; p=0.447)<br><sub>sector-cl. (7.6614; p=0.203; WCB p=0.250)</sub> |
| N | 4,161 | 4,001 | 4,148 | 3,981 | 4,148 | 3,981 |
| Mothers / women | 2,883 | 2,773 | 2,877 | 2,763 | 2,877 | 2,763 |
| Clusters: state x sector / sector | 596 / 16 | 592 / 16 | 596 / 16 | 592 / 16 | 596 / 16 | 592 / 16 |
| Mean outcome | 0.817 | 0.819 | 0.710 | 0.723 | 1254.571 | 1284.854 |
| Split-sample IV: F of even-month shock |  |  |  |  |  |  |
| **D. State x sector employment growth, men, relative to trend (full CPS sample)** | | | | | | |
| g_st_dt | -0.0003 (0.0005; p=0.504)<br><sub>sector-cl. (0.0004; p=0.457; WCB p=0.486)</sub> | 0.0005 (0.0005; p=0.268)<br><sub>sector-cl. (0.0005; p=0.309; WCB p=0.317)</sub> | -0.0002 (0.0006; p=0.706)<br><sub>sector-cl. (0.0006; p=0.735; WCB p=0.738)</sub> | 0.0006 (0.0006; p=0.317)<br><sub>sector-cl. (0.0006; p=0.385; WCB p=0.392)</sub> | -1.0968 (1.0345; p=0.290)<br><sub>sector-cl. (1.0853; p=0.328; WCB p=0.337)</sub> | 0.7924 (1.0460; p=0.449)<br><sub>sector-cl. (1.0476; p=0.461; WCB p=0.468)</sub> |
| N | 3,906 | 3,759 | 3,893 | 3,739 | 3,893 | 3,739 |
| Mothers / women | 2,732 | 2,629 | 2,726 | 2,619 | 2,726 | 2,619 |
| Clusters: state x sector / sector | 563 / 16 | 559 / 16 | 563 / 16 | 559 / 16 | 563 / 16 | 559 / 16 |
| Mean outcome | 0.820 | 0.822 | 0.715 | 0.730 | 1265.978 | 1300.044 |
| Split-sample IV: F of even-month shock |  |  |  |  |  |  |
| **E. State x sector growth, split sample: odd-month shock instrumented by even-month shock (2SLS)** | | | | | | |
| g_st_h1_dt (2SLS) | -0.0049 (0.0082; p=0.548)<br><sub>sector-cl. (0.0058; p=0.411)</sub> | 0.0107 (0.0119; p=0.370)<br><sub>sector-cl. (0.0121; p=0.388)</sub> | -0.0008 (0.0089; p=0.926)<br><sub>sector-cl. (0.0081; p=0.920)</sub> | 0.0027 (0.0106; p=0.800)<br><sub>sector-cl. (0.0115; p=0.819)</sub> | -11.6959 (16.9093; p=0.489)<br><sub>sector-cl. (16.5897; p=0.492)</sub> | 5.3662 (20.6884; p=0.795)<br><sub>sector-cl. (24.1938; p=0.827)</sub> |
| N | 3,890 | 3,743 | 3,878 | 3,724 | 3,878 | 3,724 |
| Mothers / women | 2,723 | 2,620 | 2,718 | 2,611 | 2,718 | 2,611 |
| Clusters: state x sector / sector | 559 / 16 | 555 / 16 | 559 / 16 | 555 / 16 | 559 / 16 | 555 / 16 |
| Mean outcome | 0.820 | 0.822 | 0.715 | 0.730 | 1265.605 | 1300.106 |
| Split-sample IV: F of even-month shock | 3.90 | 2.03 | 4.06 | 2.00 | 4.06 | 2.00 |
| State FE, birth-year FE, husband-sector FE, mother controls | yes | yes | yes | yes | yes | yes |

### Table 3. Wife's work after the birth (mothers NOT employed in b-1)

| | Wife employed b+1 | Wife employed b+2 | Wife 500+ hours b+1 | Wife 500+ hours b+2 | Wife hours b+1 | Wife hours b+2 |
|---|---|---|---|---|---|---|
| **A. National sector employment growth, men, leave-one-state-out, relative to pre-birth trend** | | | | | | |
| g_nat_dt | 0.0039 (0.0045; p=0.386)<br><sub>sector-cl. (0.0047; p=0.420; WCB p=0.460)</sub> | 0.0053 (0.0046; p=0.254)<br><sub>sector-cl. (0.0050; p=0.306; WCB p=0.291)</sub> | 0.0032 (0.0034; p=0.357)<br><sub>sector-cl. (0.0036; p=0.388; WCB p=0.378)</sub> | 0.0038 (0.0044; p=0.389)<br><sub>sector-cl. (0.0039; p=0.344; WCB p=0.362)</sub> | 3.3823 (5.1171; p=0.509)<br><sub>sector-cl. (5.8619; p=0.573; WCB p=0.606)</sub> | 6.7096 (6.1388; p=0.275)<br><sub>sector-cl. (7.7619; p=0.401; WCB p=0.568)</sub> |
| N | 922 | 870 | 919 | 865 | 919 | 865 |
| Mothers / women | 714 | 676 | 712 | 671 | 712 | 671 |
| Clusters: state x sector / sector | 361 / 16 | 355 / 16 | 361 / 16 | 354 / 16 | 361 / 16 | 354 / 16 |
| Mean outcome | 0.240 | 0.300 | 0.132 | 0.209 | 200.402 | 305.949 |
| Split-sample IV: F of even-month shock |  |  |  |  |  |  |
| **B. National sector employment growth, men, leave-one-state-out, raw** | | | | | | |
| g_nat | 0.0018 (0.0049; p=0.711)<br><sub>sector-cl. (0.0035; p=0.616; WCB p=0.579)</sub> | 0.0058 (0.0055; p=0.296)<br><sub>sector-cl. (0.0056; p=0.321; WCB p=0.334)</sub> | 0.0049 (0.0042; p=0.247)<br><sub>sector-cl. (0.0042; p=0.260; WCB p=0.234)</sub> | 0.0023 (0.0051; p=0.656)<br><sub>sector-cl. (0.0039; p=0.575; WCB p=0.522)</sub> | 6.4824 (6.6973; p=0.334)<br><sub>sector-cl. (5.9450; p=0.293; WCB p=0.311)</sub> | 7.9101 (7.5041; p=0.293)<br><sub>sector-cl. (8.3239; p=0.357; WCB p=0.382)</sub> |
| N | 998 | 944 | 995 | 939 | 995 | 939 |
| Mothers / women | 777 | 737 | 775 | 732 | 775 | 732 |
| Clusters: state x sector / sector | 376 / 16 | 369 / 16 | 376 / 16 | 368 / 16 | 376 / 16 | 368 / 16 |
| Mean outcome | 0.243 | 0.304 | 0.132 | 0.207 | 200.261 | 303.234 |
| Split-sample IV: F of even-month shock |  |  |  |  |  |  |
| **C. National sector unemployment rate, men, leave-one-state-out, relative to pre-birth trend** | | | | | | |
| ur_nat_dt | -0.0090 (0.0137; p=0.510)<br><sub>sector-cl. (0.0086; p=0.309; WCB p=0.292)</sub> | 0.0007 (0.0143; p=0.961)<br><sub>sector-cl. (0.0127; p=0.956; WCB p=0.961)</sub> | -0.0096 (0.0109; p=0.379)<br><sub>sector-cl. (0.0102; p=0.358; WCB p=0.343)</sub> | 0.0008 (0.0131; p=0.953)<br><sub>sector-cl. (0.0115; p=0.947; WCB p=0.950)</sub> | -9.3837 (14.7418; p=0.525)<br><sub>sector-cl. (13.6632; p=0.503; WCB p=0.481)</sub> | -3.3081 (19.1452; p=0.863)<br><sub>sector-cl. (17.1048; p=0.849; WCB p=0.858)</sub> |
| N | 1,006 | 950 | 1,003 | 945 | 1,003 | 945 |
| Mothers / women | 779 | 737 | 777 | 732 | 777 | 732 |
| Clusters: state x sector / sector | 377 / 16 | 370 / 16 | 377 / 16 | 369 / 16 | 377 / 16 | 369 / 16 |
| Mean outcome | 0.243 | 0.306 | 0.133 | 0.211 | 201.283 | 310.075 |
| Split-sample IV: F of even-month shock |  |  |  |  |  |  |
| **D. State x sector employment growth, men, relative to trend (full CPS sample)** | | | | | | |
| g_st_dt | -0.0010 (0.0011; p=0.373)<br><sub>sector-cl. (0.0013; p=0.472; WCB p=0.471)</sub> | -0.0030*** (0.0011; p=0.005)<br><sub>sector-cl. (0.0009; p=0.005; WCB p=0.006)***</sub> | -0.0002 (0.0008; p=0.829)<br><sub>sector-cl. (0.0009; p=0.845; WCB p=0.869)</sub> | -0.0025*** (0.0009; p=0.008)<br><sub>sector-cl. (0.0008; p=0.005; WCB p=0.007)***</sub> | 0.1290 (1.3990; p=0.927)<br><sub>sector-cl. (1.3844; p=0.927; WCB p=0.928)</sub> | -4.2253*** (1.3256; p=0.002)<br><sub>sector-cl. (1.1623; p=0.002; WCB p=0.002)***</sub> |
| N | 910 | 859 | 907 | 854 | 907 | 854 |
| Mothers / women | 708 | 671 | 706 | 666 | 706 | 666 |
| Clusters: state x sector / sector | 353 / 16 | 348 / 16 | 353 / 16 | 347 / 16 | 353 / 16 | 347 / 16 |
| Mean outcome | 0.240 | 0.302 | 0.132 | 0.210 | 202.095 | 305.430 |
| Split-sample IV: F of even-month shock |  |  |  |  |  |  |
| **E. State x sector growth, split sample: odd-month shock instrumented by even-month shock (2SLS)** | | | | | | |
| g_st_h1_dt (2SLS) | -0.0103 (0.0166; p=0.537)<br><sub>sector-cl. (0.0166; p=0.545)</sub> | -0.0349 (0.0334; p=0.297)<br><sub>sector-cl. (0.0375; p=0.368)</sub> | -0.0025 (0.0106; p=0.814)<br><sub>sector-cl. (0.0130; p=0.850)</sub> | -0.0255 (0.0249; p=0.306)<br><sub>sector-cl. (0.0281; p=0.379)</sub> | 3.4252 (17.0844; p=0.841)<br><sub>sector-cl. (19.3141; p=0.862)</sub> | -45.6577 (43.2744; p=0.292)<br><sub>sector-cl. (45.9596; p=0.336)</sub> |
| N | 906 | 855 | 903 | 850 | 903 | 850 |
| Mothers / women | 705 | 668 | 703 | 663 | 703 | 663 |
| Clusters: state x sector / sector | 353 / 16 | 348 / 16 | 353 / 16 | 347 / 16 | 353 / 16 | 347 / 16 |
| Mean outcome | 0.241 | 0.303 | 0.133 | 0.211 | 202.990 | 306.867 |
| Split-sample IV: F of even-month shock | 0.84 | 0.74 | 0.86 | 0.80 | 0.86 | 0.80 |
| State FE, birth-year FE, husband-sector FE, mother controls | yes | yes | yes | yes | yes | yes |

### Table 4. Heterogeneity (interactions; 'total' = shock + interaction)

| | Husband hours b - pre | Husband hours b+1 - pre | Husband hours fell >= 25% in b | Wife employed b+1 | Wife employed b+2 | Wife 500+ hours b+1 | Wife 500+ hours b+2 | Wife hours b+1 | Wife hours b+2 |
|---|---|---|---|---|---|---|---|---|---|
| **g_nat_dt x Black** | | | | | | | | | |
| national growth (A) | 4.8885* (2.8475; p=0.087)<br><sub>sector-cl. (2.7144; p=0.092; WCB p=0.145)</sub> | 3.7688 (3.4126; p=0.270)<br><sub>sector-cl. (3.8317; p=0.341; WCB p=0.352)</sub> | -0.0018 (0.0014; p=0.185)<br><sub>sector-cl. (0.0010; p=0.078; WCB p=0.096)*</sub> | -0.0004 (0.0020; p=0.834)<br><sub>sector-cl. (0.0020; p=0.830; WCB p=0.826)</sub> | 0.0019 (0.0019; p=0.330)<br><sub>sector-cl. (0.0022; p=0.404; WCB p=0.426)</sub> | -0.0012 (0.0021; p=0.562)<br><sub>sector-cl. (0.0018; p=0.509; WCB p=0.545)</sub> | 0.0007 (0.0022; p=0.761)<br><sub>sector-cl. (0.0027; p=0.807; WCB p=0.805)</sub> | -0.4945 (4.2425; p=0.907)<br><sub>sector-cl. (4.0442; p=0.904; WCB p=0.919)</sub> | -0.5246 (4.3952; p=0.905)<br><sub>sector-cl. (5.0282; p=0.918; WCB p=0.917)</sub> |
| national growth (A) x Black | 4.6381 (7.2501; p=0.523)<br><sub>sector-cl. (7.8550; p=0.564; WCB p=0.691)</sub> | 11.9332 (8.0589; p=0.139)<br><sub>sector-cl. (7.1276; p=0.115; WCB p=0.113)</sub> | -0.0008 (0.0039; p=0.837)<br><sub>sector-cl. (0.0034; p=0.818; WCB p=0.806)</sub> | 0.0004 (0.0046; p=0.936)<br><sub>sector-cl. (0.0043; p=0.933; WCB p=0.939)</sub> | -0.0007 (0.0032; p=0.826)<br><sub>sector-cl. (0.0030; p=0.815; WCB p=0.844)</sub> | 0.0024 (0.0046; p=0.598)<br><sub>sector-cl. (0.0042; p=0.565; WCB p=0.588)</sub> | 0.0009 (0.0036; p=0.802)<br><sub>sector-cl. (0.0026; p=0.735; WCB p=0.718)</sub> | 10.7968 (8.6427; p=0.212)<br><sub>sector-cl. (7.3215; p=0.161; WCB p=0.203)</sub> | 8.8921 (7.6637; p=0.246)<br><sub>sector-cl. (5.7889; p=0.145; WCB p=0.165)</sub> |
| national growth (A): total for Black = 1 | 9.5266 (6.6205; p=0.151)<br><sub>sector-cl. (6.4133; p=0.158)</sub> | 15.7020** (7.7123; p=0.042)<br><sub>sector-cl. (5.9436; p=0.018)**</sub> | -0.0026 (0.0037; p=0.477)<br><sub>sector-cl. (0.0029; p=0.385)</sub> | -0.0001 (0.0041; p=0.988)<br><sub>sector-cl. (0.0040; p=0.988)</sub> | 0.0012 (0.0028; p=0.674)<br><sub>sector-cl. (0.0035; p=0.744)</sub> | 0.0012 (0.0043; p=0.778)<br><sub>sector-cl. (0.0040; p=0.765)</sub> | 0.0016 (0.0031; p=0.612)<br><sub>sector-cl. (0.0033; p=0.641)</sub> | 10.3023 (7.9732; p=0.197)<br><sub>sector-cl. (6.1058; p=0.112)</sub> | 8.3676 (6.8109; p=0.220)<br><sub>sector-cl. (6.6468; p=0.227)</sub> |
| N | 3,939 | 3,822 | 3,873 | 3,961 | 3,807 | 3,948 | 3,787 | 3,948 | 3,787 |
| Mothers / women | 2,771 | 2,671 | 2,735 | 2,763 | 2,656 | 2,757 | 2,646 | 2,757 | 2,646 |
| Clusters: state x sector / sector | 590 / 16 | 585 / 16 | 588 / 16 | 591 / 16 | 586 / 16 | 591 / 16 | 586 / 16 | 591 / 16 | 586 / 16 |
| Mean outcome | -4.061 | -0.293 | 0.090 | 0.818 | 0.822 | 0.715 | 0.730 | 1265.232 | 1299.462 |
| **g_nat_dt x low liquid assets (below median)** | | | | | | | | | |
| national growth (A) | 2.9125 (3.7100; p=0.433)<br><sub>sector-cl. (2.6390; p=0.287; WCB p=0.299)</sub> | 1.9344 (4.5070; p=0.668)<br><sub>sector-cl. (4.0832; p=0.643; WCB p=0.614)</sub> | -0.0019 (0.0018; p=0.281)<br><sub>sector-cl. (0.0012; p=0.128; WCB p=0.148)</sub> | -0.0012 (0.0024; p=0.628)<br><sub>sector-cl. (0.0022; p=0.593; WCB p=0.616)</sub> | 0.0001 (0.0024; p=0.973)<br><sub>sector-cl. (0.0022; p=0.971; WCB p=0.967)</sub> | -0.0034 (0.0026; p=0.196)<br><sub>sector-cl. (0.0028; p=0.235; WCB p=0.293)</sub> | -0.0036 (0.0027; p=0.184)<br><sub>sector-cl. (0.0027; p=0.204; WCB p=0.231)</sub> | -2.6002 (5.3892; p=0.630)<br><sub>sector-cl. (5.5922; p=0.649; WCB p=0.675)</sub> | -5.8536 (5.6287; p=0.299)<br><sub>sector-cl. (6.2181; p=0.361; WCB p=0.383)</sub> |
| national growth (A) x low liquid assets (below median) | 5.2574 (4.7610; p=0.270)<br><sub>sector-cl. (3.2863; p=0.130; WCB p=0.109)</sub> | 5.6930 (5.9481; p=0.339)<br><sub>sector-cl. (3.1170; p=0.088; WCB p=0.083)*</sub> | 0.0008 (0.0025; p=0.742)<br><sub>sector-cl. (0.0019; p=0.684; WCB p=0.700)</sub> | 0.0002 (0.0033; p=0.950)<br><sub>sector-cl. (0.0029; p=0.943; WCB p=0.949)</sub> | 0.0004 (0.0031; p=0.890)<br><sub>sector-cl. (0.0025; p=0.865; WCB p=0.865)</sub> | 0.0027 (0.0037; p=0.469)<br><sub>sector-cl. (0.0031; p=0.405; WCB p=0.415)</sub> | 0.0051 (0.0038; p=0.185)<br><sub>sector-cl. (0.0034; p=0.154; WCB p=0.116)</sub> | 4.1332 (7.6267; p=0.588)<br><sub>sector-cl. (6.4682; p=0.532; WCB p=0.535)</sub> | 7.4029 (7.6541; p=0.334)<br><sub>sector-cl. (6.7583; p=0.291; WCB p=0.276)</sub> |
| national growth (A): total for low liquid assets (below median) = 1 | 8.1699** (3.6334; p=0.025)<br><sub>sector-cl. (3.5507; p=0.036)**</sub> | 7.6274 (4.7364; p=0.108)<br><sub>sector-cl. (3.7613; p=0.061)*</sub> | -0.0011 (0.0018; p=0.549)<br><sub>sector-cl. (0.0014; p=0.441)</sub> | -0.0010 (0.0027; p=0.718)<br><sub>sector-cl. (0.0027; p=0.722)</sub> | 0.0005 (0.0025; p=0.842)<br><sub>sector-cl. (0.0027; p=0.853)</sub> | -0.0007 (0.0031; p=0.819)<br><sub>sector-cl. (0.0027; p=0.800)</sub> | 0.0014 (0.0030; p=0.638)<br><sub>sector-cl. (0.0041; p=0.732)</sub> | 1.5330 (6.3092; p=0.808)<br><sub>sector-cl. (5.1317; p=0.769)</sub> | 1.5494 (6.1120; p=0.800)<br><sub>sector-cl. (6.7015; p=0.820)</sub> |
| N | 3,661 | 3,540 | 3,598 | 3,672 | 3,541 | 3,659 | 3,521 | 3,659 | 3,521 |
| Mothers / women | 2,595 | 2,490 | 2,560 | 2,579 | 2,489 | 2,573 | 2,479 | 2,573 | 2,479 |
| Clusters: state x sector / sector | 580 / 16 | 572 / 16 | 578 / 16 | 579 / 16 | 575 / 16 | 579 / 16 | 574 / 16 | 579 / 16 | 574 / 16 |
| Mean outcome | -0.335 | 1.141 | 0.088 | 0.820 | 0.821 | 0.720 | 0.731 | 1279.366 | 1302.850 |
| **g_nat_dt x mother employed in b-1 (all married mothers)** | | | | | | | | | |
| national growth (A) | 10.3924 (6.7965; p=0.127)<br><sub>sector-cl. (5.8708; p=0.097; WCB p=0.082)*</sub> | 13.2212* (7.2704; p=0.069)<br><sub>sector-cl. (7.3133; p=0.091; WCB p=0.062)*</sub> | -0.0038 (0.0032; p=0.225)<br><sub>sector-cl. (0.0044; p=0.391; WCB p=0.420)</sub> | 0.0016 (0.0036; p=0.656)<br><sub>sector-cl. (0.0044; p=0.724; WCB p=0.729)</sub> | 0.0023 (0.0039; p=0.551)<br><sub>sector-cl. (0.0053; p=0.667; WCB p=0.688)</sub> | 0.0015 (0.0030; p=0.619)<br><sub>sector-cl. (0.0038; p=0.701; WCB p=0.722)</sub> | 0.0036 (0.0040; p=0.373)<br><sub>sector-cl. (0.0062; p=0.571; WCB p=0.650)</sub> | 1.1677 (4.8120; p=0.808)<br><sub>sector-cl. (6.4114; p=0.858; WCB p=0.883)</sub> | 6.9411 (6.5896; p=0.293)<br><sub>sector-cl. (10.8415; p=0.532; WCB p=0.653)</sub> |
| national growth (A) x mother employed in b-1 (all married mothers) | -4.0951 (7.1157; p=0.565)<br><sub>sector-cl. (6.1231; p=0.514; WCB p=0.512)</sub> | -6.5569 (7.5937; p=0.388)<br><sub>sector-cl. (6.0711; p=0.297; WCB p=0.298)</sub> | 0.0012 (0.0035; p=0.737)<br><sub>sector-cl. (0.0049; p=0.813; WCB p=0.852)</sub> | -0.0021 (0.0038; p=0.588)<br><sub>sector-cl. (0.0036; p=0.574; WCB p=0.596)</sub> | -0.0001 (0.0041; p=0.977)<br><sub>sector-cl. (0.0049; p=0.981; WCB p=0.987)</sub> | -0.0024 (0.0036; p=0.500)<br><sub>sector-cl. (0.0040; p=0.556; WCB p=0.669)</sub> | -0.0028 (0.0043; p=0.509)<br><sub>sector-cl. (0.0057; p=0.628; WCB p=0.675)</sub> | -0.1379 (5.8043; p=0.981)<br><sub>sector-cl. (6.2867; p=0.983; WCB p=0.987)</sub> | -6.3762 (7.3835; p=0.388)<br><sub>sector-cl. (10.1137; p=0.538; WCB p=0.636)</sub> |
| national growth (A): total for mother employed in b-1 (all married mothers) = 1 | 6.2973** (2.5863; p=0.015)<br><sub>sector-cl. (2.0999; p=0.009)***</sub> | 6.6643** (3.1807; p=0.037)<br><sub>sector-cl. (2.8436; p=0.033)**</sub> | -0.0027** (0.0014; p=0.049)<br><sub>sector-cl. (0.0010; p=0.014)**</sub> | -0.0005 (0.0018; p=0.789)<br><sub>sector-cl. (0.0016; p=0.774)</sub> | 0.0022 (0.0017; p=0.188)<br><sub>sector-cl. (0.0021; p=0.318)</sub> | -0.0009 (0.0019; p=0.634)<br><sub>sector-cl. (0.0016; p=0.573)</sub> | 0.0007 (0.0019; p=0.700)<br><sub>sector-cl. (0.0021; p=0.728)</sub> | 1.0298 (3.7768; p=0.785)<br><sub>sector-cl. (3.0450; p=0.740)</sub> | 0.5649 (3.9049; p=0.885)<br><sub>sector-cl. (4.1374; p=0.893)</sub> |
| N | 4,873 | 4,719 | 4,782 | 4,883 | 4,677 | 4,867 | 4,652 | 4,867 | 4,652 |
| Mothers / women | 3,206 | 3,065 | 3,157 | 3,165 | 3,048 | 3,158 | 3,034 | 3,158 | 3,034 |
| Clusters: state x sector / sector | 613 / 16 | 606 / 16 | 608 / 16 | 610 / 16 | 606 / 16 | 610 / 16 | 606 / 16 | 610 / 16 | 606 / 16 |
| Mean outcome | -0.876 | 0.341 | 0.094 | 0.709 | 0.725 | 0.605 | 0.633 | 1064.168 | 1114.727 |
| **ur_nat_dt x Black** | | | | | | | | | |
| national unemployment rate (C) | -15.0471* (9.1141; p=0.099)<br><sub>sector-cl. (6.4588; p=0.034; WCB p=0.051)*</sub> | -4.2684 (11.2626; p=0.705)<br><sub>sector-cl. (7.1445; p=0.559; WCB p=0.559)</sub> | 0.0047 (0.0053; p=0.377)<br><sub>sector-cl. (0.0046; p=0.319; WCB p=0.373)</sub> | 0.0012 (0.0061; p=0.845)<br><sub>sector-cl. (0.0035; p=0.735; WCB p=0.722)</sub> | -0.0055 (0.0060; p=0.355)<br><sub>sector-cl. (0.0036; p=0.149; WCB p=0.122)</sub> | 0.0066 (0.0072; p=0.361)<br><sub>sector-cl. (0.0061; p=0.301; WCB p=0.349)</sub> | 0.0023 (0.0070; p=0.739)<br><sub>sector-cl. (0.0051; p=0.649; WCB p=0.697)</sub> | 6.8905 (13.5064; p=0.610)<br><sub>sector-cl. (10.9523; p=0.539; WCB p=0.567)</sub> | 9.8806 (13.9524; p=0.479)<br><sub>sector-cl. (7.6357; p=0.215; WCB p=0.245)</sub> |
| national unemployment rate (C) x Black | 13.5984 (14.9481; p=0.363)<br><sub>sector-cl. (9.9999; p=0.194; WCB p=0.154)</sub> | -0.1003 (16.6394; p=0.995)<br><sub>sector-cl. (15.6298; p=0.995; WCB p=0.994)</sub> | -0.0122 (0.0083; p=0.144)<br><sub>sector-cl. (0.0045; p=0.017; WCB p=0.054)*</sub> | 0.0032 (0.0077; p=0.674)<br><sub>sector-cl. (0.0064; p=0.623; WCB p=0.654)</sub> | 0.0029 (0.0072; p=0.683)<br><sub>sector-cl. (0.0071; p=0.684; WCB p=0.699)</sub> | 0.0090 (0.0088; p=0.307)<br><sub>sector-cl. (0.0108; p=0.420; WCB p=0.480)</sub> | 0.0027 (0.0073; p=0.707)<br><sub>sector-cl. (0.0089; p=0.761; WCB p=0.779)</sub> | 2.6487 (17.3855; p=0.879)<br><sub>sector-cl. (15.3778; p=0.866; WCB p=0.846)</sub> | 2.2329 (17.0402; p=0.896)<br><sub>sector-cl. (17.8240; p=0.902; WCB p=0.904)</sub> |
| national unemployment rate (C): total for Black = 1 | -1.4486 (16.6941; p=0.931)<br><sub>sector-cl. (11.3814; p=0.900)</sub> | -4.3687 (18.7917; p=0.816)<br><sub>sector-cl. (17.4284; p=0.805)</sub> | -0.0074 (0.0103; p=0.470)<br><sub>sector-cl. (0.0070; p=0.302)</sub> | 0.0044 (0.0079; p=0.575)<br><sub>sector-cl. (0.0061; p=0.480)</sub> | -0.0026 (0.0077; p=0.734)<br><sub>sector-cl. (0.0058; p=0.662)</sub> | 0.0156 (0.0098; p=0.114)<br><sub>sector-cl. (0.0090; p=0.106)</sub> | 0.0051 (0.0081; p=0.532)<br><sub>sector-cl. (0.0085; p=0.557)</sub> | 9.5392 (19.7588; p=0.629)<br><sub>sector-cl. (14.2953; p=0.515)</sub> | 12.1135 (18.4833; p=0.512)<br><sub>sector-cl. (18.2775; p=0.518)</sub> |
| N | 4,134 | 4,014 | 4,066 | 4,161 | 4,001 | 4,148 | 3,981 | 4,148 | 3,981 |
| Mothers / women | 2,886 | 2,785 | 2,850 | 2,883 | 2,773 | 2,877 | 2,763 | 2,877 | 2,763 |
| Clusters: state x sector / sector | 595 / 16 | 590 / 16 | 593 / 16 | 596 / 16 | 592 / 16 | 596 / 16 | 592 / 16 | 596 / 16 | 592 / 16 |
| Mean outcome | -6.521 | 1.856 | 0.092 | 0.817 | 0.819 | 0.710 | 0.723 | 1254.571 | 1284.854 |
| **ur_nat_dt x low liquid assets (below median)** | | | | | | | | | |
| national unemployment rate (C) | -5.1207 (10.9404; p=0.640)<br><sub>sector-cl. (9.3345; p=0.591; WCB p=0.612)</sub> | -0.0340 (14.0544; p=0.998)<br><sub>sector-cl. (12.2128; p=0.998; WCB p=1.000)</sub> | -0.0046 (0.0054; p=0.395)<br><sub>sector-cl. (0.0036; p=0.218; WCB p=0.235)</sub> | 0.0067 (0.0067; p=0.316)<br><sub>sector-cl. (0.0063; p=0.306; WCB p=0.381)</sub> | 0.0006 (0.0075; p=0.933)<br><sub>sector-cl. (0.0057; p=0.914; WCB p=0.929)</sub> | 0.0149* (0.0084; p=0.079)<br><sub>sector-cl. (0.0093; p=0.131; WCB p=0.142)</sub> | 0.0139 (0.0087; p=0.112)<br><sub>sector-cl. (0.0062; p=0.041; WCB p=0.119)</sub> | 16.8526 (16.6247; p=0.311)<br><sub>sector-cl. (15.1166; p=0.282; WCB p=0.355)</sub> | 27.0686 (17.2456; p=0.117)<br><sub>sector-cl. (10.9964; p=0.026; WCB p=0.026)**</sub> |
| national unemployment rate (C) x low liquid assets (below median) | -8.9253 (10.2266; p=0.383)<br><sub>sector-cl. (10.1393; p=0.393; WCB p=0.403)</sub> | -0.2943 (13.9663; p=0.983)<br><sub>sector-cl. (10.9484; p=0.979; WCB p=0.981)</sub> | 0.0040 (0.0053; p=0.457)<br><sub>sector-cl. (0.0051; p=0.450; WCB p=0.462)</sub> | 0.0019 (0.0067; p=0.772)<br><sub>sector-cl. (0.0064; p=0.765; WCB p=0.770)</sub> | 0.0002 (0.0068; p=0.977)<br><sub>sector-cl. (0.0052; p=0.971; WCB p=0.981)</sub> | -0.0040 (0.0076; p=0.601)<br><sub>sector-cl. (0.0065; p=0.549; WCB p=0.586)</sub> | -0.0042 (0.0080; p=0.594)<br><sub>sector-cl. (0.0051; p=0.423; WCB p=0.446)</sub> | -4.4887 (13.4894; p=0.739)<br><sub>sector-cl. (9.9052; p=0.657; WCB p=0.674)</sub> | -9.6950 (15.3304; p=0.527)<br><sub>sector-cl. (9.9260; p=0.344; WCB p=0.369)</sub> |
| national unemployment rate (C): total for low liquid assets (below median) = 1 | -14.0459 (11.4607; p=0.221)<br><sub>sector-cl. (10.6311; p=0.206)</sub> | -0.3283 (14.5400; p=0.982)<br><sub>sector-cl. (12.6732; p=0.980)</sub> | -0.0006 (0.0060; p=0.916)<br><sub>sector-cl. (0.0046; p=0.891)</sub> | 0.0087 (0.0072; p=0.231)<br><sub>sector-cl. (0.0039; p=0.042)**</sub> | 0.0008 (0.0076; p=0.914)<br><sub>sector-cl. (0.0032; p=0.798)</sub> | 0.0108 (0.0089; p=0.223)<br><sub>sector-cl. (0.0069; p=0.136)</sub> | 0.0096 (0.0089; p=0.282)<br><sub>sector-cl. (0.0041; p=0.032)**</sub> | 12.3638 (16.5067; p=0.454)<br><sub>sector-cl. (12.0274; p=0.320)</sub> | 17.3735 (18.2055; p=0.340)<br><sub>sector-cl. (8.8311; p=0.068)*</sub> |
| N | 3,661 | 3,540 | 3,598 | 3,672 | 3,541 | 3,659 | 3,521 | 3,659 | 3,521 |
| Mothers / women | 2,595 | 2,490 | 2,560 | 2,579 | 2,489 | 2,573 | 2,479 | 2,573 | 2,479 |
| Clusters: state x sector / sector | 580 / 16 | 572 / 16 | 578 / 16 | 579 / 16 | 575 / 16 | 579 / 16 | 574 / 16 | 579 / 16 | 574 / 16 |
| Mean outcome | -0.335 | 1.141 | 0.088 | 0.820 | 0.821 | 0.720 | 0.731 | 1279.366 | 1302.850 |
| **ur_nat_dt x mother employed in b-1 (all married mothers)** | | | | | | | | | |
| national unemployment rate (C) | -16.6923 (14.6326; p=0.254)<br><sub>sector-cl. (14.7120; p=0.274; WCB p=0.263)</sub> | -11.2133 (16.0423; p=0.485)<br><sub>sector-cl. (24.2092; p=0.650; WCB p=0.705)</sub> | 0.0097 (0.0061; p=0.109)<br><sub>sector-cl. (0.0072; p=0.199; WCB p=0.178)</sub> | 0.0001 (0.0072; p=0.991)<br><sub>sector-cl. (0.0064; p=0.990; WCB p=0.988)</sub> | 0.0049 (0.0087; p=0.576)<br><sub>sector-cl. (0.0093; p=0.607; WCB p=0.623)</sub> | 0.0045 (0.0074; p=0.540)<br><sub>sector-cl. (0.0059; p=0.458; WCB p=0.453)</sub> | 0.0041 (0.0085; p=0.633)<br><sub>sector-cl. (0.0087; p=0.649; WCB p=0.687)</sub> | 7.3262 (12.8927; p=0.570)<br><sub>sector-cl. (11.5028; p=0.534; WCB p=0.536)</sub> | 10.4281 (14.4259; p=0.470)<br><sub>sector-cl. (18.0744; p=0.573; WCB p=0.620)</sub> |
| national unemployment rate (C) x mother employed in b-1 (all married mothers) | -0.7474 (12.6060; p=0.953)<br><sub>sector-cl. (11.1545; p=0.947; WCB p=0.943)</sub> | 5.9013 (15.1761; p=0.698)<br><sub>sector-cl. (18.9133; p=0.759; WCB p=0.771)</sub> | -0.0020 (0.0057; p=0.734)<br><sub>sector-cl. (0.0069; p=0.781; WCB p=0.793)</sub> | -0.0002 (0.0067; p=0.981)<br><sub>sector-cl. (0.0049; p=0.974; WCB p=0.984)</sub> | -0.0102 (0.0077; p=0.186)<br><sub>sector-cl. (0.0085; p=0.249; WCB p=0.240)</sub> | 0.0013 (0.0067; p=0.845)<br><sub>sector-cl. (0.0064; p=0.839; WCB p=0.851)</sub> | -0.0006 (0.0075; p=0.931)<br><sub>sector-cl. (0.0090; p=0.944; WCB p=0.936)</sub> | -2.2203 (10.7698; p=0.837)<br><sub>sector-cl. (11.2315; p=0.846; WCB p=0.850)</sub> | -1.4524 (13.3451; p=0.913)<br><sub>sector-cl. (16.1136; p=0.929; WCB p=0.935)</sub> |
| national unemployment rate (C): total for mother employed in b-1 (all married mothers) = 1 | -17.4398** (8.8509; p=0.049)<br><sub>sector-cl. (8.5669; p=0.060)*</sub> | -5.3120 (10.1389; p=0.601)<br><sub>sector-cl. (7.0701; p=0.464)</sub> | 0.0078 (0.0051; p=0.127)<br><sub>sector-cl. (0.0052; p=0.158)</sub> | -0.0001 (0.0056; p=0.989)<br><sub>sector-cl. (0.0034; p=0.982)</sub> | -0.0054 (0.0056; p=0.338)<br><sub>sector-cl. (0.0034; p=0.134)</sub> | 0.0058 (0.0065; p=0.372)<br><sub>sector-cl. (0.0053; p=0.291)</sub> | 0.0034 (0.0063; p=0.586)<br><sub>sector-cl. (0.0037; p=0.367)</sub> | 5.1060 (11.9869; p=0.670)<br><sub>sector-cl. (8.9915; p=0.579)</sub> | 8.9757 (12.1815; p=0.462)<br><sub>sector-cl. (6.9375; p=0.215)</sub> |
| N | 5,153 | 4,996 | 5,059 | 5,167 | 4,951 | 5,151 | 4,926 | 5,151 | 4,926 |
| Mothers / women | 3,357 | 3,216 | 3,309 | 3,321 | 3,200 | 3,314 | 3,186 | 3,314 | 3,186 |
| Clusters: state x sector / sector | 617 / 16 | 611 / 16 | 612 / 16 | 616 / 16 | 613 / 16 | 616 / 16 | 613 / 16 | 616 / 16 | 613 / 16 |
| Mean outcome | -3.740 | 3.638 | 0.096 | 0.705 | 0.720 | 0.598 | 0.625 | 1049.476 | 1097.853 |
| State FE, birth-year FE, husband-sector FE, mother controls (+ group dummy) | yes | yes | yes | yes | yes | yes | yes | yes | yes |

Low liquid assets: checking/savings (+ CDs/bonds from 2019) of the mother's family in the latest wealth wave in [b-5, b] below the sample median (no wealth data before 1984). The 'mother employed in b-1' panel pools employed and non-employed mothers.

### Table 5. Crowd-out: shock x safety-net generosity in the state and year of the birth

| | Husband hours b - pre | Wife employed b+1 | Wife employed b+2 | Wife 500+ hours b+1 | Wife 500+ hours b+2 | Wife hours b+1 | Wife hours b+2 |
|---|---|---|---|---|---|---|---|
| **g_nat_dt x afdc_max3** | | | | | | | |
| national growth (A) | 5.6291** (2.6131; p=0.032)<br><sub>sector-cl. (2.1267; p=0.018; WCB p=0.045)**</sub> | -0.0005 (0.0018; p=0.801)<br><sub>sector-cl. (0.0018; p=0.805; WCB p=0.803)</sub> | 0.0017 (0.0017; p=0.322)<br><sub>sector-cl. (0.0022; p=0.454; WCB p=0.475)</sub> | -0.0009 (0.0019; p=0.632)<br><sub>sector-cl. (0.0018; p=0.602; WCB p=0.607)</sub> | 0.0008 (0.0020; p=0.701)<br><sub>sector-cl. (0.0026; p=0.780; WCB p=0.777)</sub> | 1.2644 (3.8909; p=0.745)<br><sub>sector-cl. (3.5820; p=0.729; WCB p=0.733)</sub> | 0.7345 (4.0036; p=0.855)<br><sub>sector-cl. (4.9047; p=0.883; WCB p=0.871)</sub> |
| national growth (A) x AFDC/TANF max benefit, 3 persons ($100s of 2000 $, centred) | -0.7308 (1.1909; p=0.540)<br><sub>sector-cl. (1.2877; p=0.579; WCB p=0.656)</sub> | -0.0002 (0.0009; p=0.840)<br><sub>sector-cl. (0.0007; p=0.794; WCB p=0.791)</sub> | 0.0002 (0.0008; p=0.839)<br><sub>sector-cl. (0.0005; p=0.767; WCB p=0.794)</sub> | -0.0003 (0.0009; p=0.787)<br><sub>sector-cl. (0.0007; p=0.727; WCB p=0.798)</sub> | 0.0002 (0.0009; p=0.804)<br><sub>sector-cl. (0.0005; p=0.657; WCB p=0.632)</sub> | 0.4590 (1.6718; p=0.784)<br><sub>sector-cl. (1.0714; p=0.674; WCB p=0.683)</sub> | -0.2683 (1.8935; p=0.887)<br><sub>sector-cl. (0.9546; p=0.782; WCB p=0.780)</sub> |
| N | 3,939 | 3,961 | 3,807 | 3,948 | 3,787 | 3,948 | 3,787 |
| Mothers / women | 2,771 | 2,763 | 2,656 | 2,757 | 2,646 | 2,757 | 2,646 |
| Clusters: state x sector / sector | 590 / 16 | 591 / 16 | 586 / 16 | 591 / 16 | 586 / 16 | 591 / 16 | 586 / 16 |
| Mean outcome | -4.061 | 0.818 | 0.822 | 0.715 | 0.730 | 1265.232 | 1299.462 |
| **g_nat_dt x afdc_fs_max3** | | | | | | | |
| national growth (A) | 5.5557** (2.6210; p=0.034)<br><sub>sector-cl. (2.1472; p=0.021; WCB p=0.047)**</sub> | -0.0005 (0.0018; p=0.795)<br><sub>sector-cl. (0.0018; p=0.798; WCB p=0.790)</sub> | 0.0017 (0.0017; p=0.327)<br><sub>sector-cl. (0.0022; p=0.456; WCB p=0.477)</sub> | -0.0010 (0.0019; p=0.620)<br><sub>sector-cl. (0.0017; p=0.588; WCB p=0.589)</sub> | 0.0008 (0.0020; p=0.696)<br><sub>sector-cl. (0.0026; p=0.775; WCB p=0.764)</sub> | 1.2495 (3.9128; p=0.750)<br><sub>sector-cl. (3.5901; p=0.733; WCB p=0.741)</sub> | 0.7042 (4.0348; p=0.862)<br><sub>sector-cl. (4.9365; p=0.888; WCB p=0.878)</sub> |
| national growth (A) x AFDC/TANF + food stamps max, 3 persons ($100s of 2000 $, centred) | -1.2076 (1.5151; p=0.426)<br><sub>sector-cl. (1.7108; p=0.491; WCB p=0.560)</sub> | -0.0004 (0.0011; p=0.707)<br><sub>sector-cl. (0.0008; p=0.622; WCB p=0.619)</sub> | 0.0001 (0.0010; p=0.938)<br><sub>sector-cl. (0.0006; p=0.898; WCB p=0.910)</sub> | -0.0007 (0.0012; p=0.550)<br><sub>sector-cl. (0.0009; p=0.434; WCB p=0.573)</sub> | 0.0001 (0.0012; p=0.930)<br><sub>sector-cl. (0.0008; p=0.894; WCB p=0.909)</sub> | -0.0767 (2.2097; p=0.972)<br><sub>sector-cl. (1.4159; p=0.958; WCB p=0.965)</sub> | -1.0976 (2.4700; p=0.657)<br><sub>sector-cl. (1.3639; p=0.434; WCB p=0.457)</sub> |
| N | 3,939 | 3,961 | 3,807 | 3,948 | 3,787 | 3,948 | 3,787 |
| Mothers / women | 2,771 | 2,763 | 2,656 | 2,757 | 2,646 | 2,757 | 2,646 |
| Clusters: state x sector / sector | 590 / 16 | 591 / 16 | 586 / 16 | 591 / 16 | 586 / 16 | 591 / 16 | 586 / 16 |
| Mean outcome | -4.061 | 0.818 | 0.822 | 0.715 | 0.730 | 1265.232 | 1299.462 |
| **g_nat_dt x max_wba** | | | | | | | |
| national growth (A) | 5.6557** (2.6102; p=0.031)<br><sub>sector-cl. (1.9944; p=0.013; WCB p=0.032)**</sub> | -0.0002 (0.0018; p=0.926)<br><sub>sector-cl. (0.0017; p=0.923; WCB p=0.917)</sub> | 0.0018 (0.0017; p=0.289)<br><sub>sector-cl. (0.0023; p=0.436; WCB p=0.465)</sub> | -0.0004 (0.0020; p=0.832)<br><sub>sector-cl. (0.0018; p=0.823; WCB p=0.856)</sub> | 0.0011 (0.0019; p=0.560)<br><sub>sector-cl. (0.0026; p=0.674; WCB p=0.667)</sub> | 2.0645 (3.7871; p=0.586)<br><sub>sector-cl. (3.4841; p=0.562; WCB p=0.588)</sub> | 1.5708 (3.8879; p=0.686)<br><sub>sector-cl. (4.7424; p=0.745; WCB p=0.747)</sub> |
| national growth (A) x UI: max_wba (centred) | -0.0020 (0.0153; p=0.897)<br><sub>sector-cl. (0.0147; p=0.895; WCB p=0.885)</sub> | -0.0000 (0.0000; p=0.244)<br><sub>sector-cl. (0.0000; p=0.081; WCB p=0.079)*</sub> | -0.0000 (0.0000; p=0.916)<br><sub>sector-cl. (0.0000; p=0.881; WCB p=0.884)</sub> | -0.0000** (0.0000; p=0.019)<br><sub>sector-cl. (0.0000; p=0.002; WCB p=0.005)***</sub> | -0.0000* (0.0000; p=0.076)<br><sub>sector-cl. (0.0000; p=0.039; WCB p=0.106)</sub> | -0.0575** (0.0287; p=0.045)<br><sub>sector-cl. (0.0193; p=0.009; WCB p=0.042)**</sub> | -0.0496* (0.0296; p=0.094)<br><sub>sector-cl. (0.0248; p=0.064; WCB p=0.168)</sub> |
| N | 3,939 | 3,960 | 3,806 | 3,947 | 3,786 | 3,947 | 3,786 |
| Mothers / women | 2,771 | 2,762 | 2,655 | 2,756 | 2,645 | 2,756 | 2,645 |
| Clusters: state x sector / sector | 590 / 16 | 591 / 16 | 586 / 16 | 591 / 16 | 586 / 16 | 591 / 16 | 586 / 16 |
| Mean outcome | -4.061 | 0.818 | 0.822 | 0.715 | 0.730 | 1265.451 | 1299.256 |
| **g_nat_dt x max_wba_2000** | | | | | | | |
| national growth (A) | 5.8620** (2.6406; p=0.027)<br><sub>sector-cl. (2.0032; p=0.010; WCB p=0.031)**</sub> | -0.0002 (0.0018; p=0.917)<br><sub>sector-cl. (0.0017; p=0.914; WCB p=0.898)</sub> | 0.0018 (0.0017; p=0.291)<br><sub>sector-cl. (0.0022; p=0.429; WCB p=0.455)</sub> | -0.0004 (0.0020; p=0.851)<br><sub>sector-cl. (0.0017; p=0.832; WCB p=0.845)</sub> | 0.0011 (0.0019; p=0.572)<br><sub>sector-cl. (0.0026; p=0.677; WCB p=0.674)</sub> | 2.1435 (3.8345; p=0.576)<br><sub>sector-cl. (3.4119; p=0.539; WCB p=0.550)</sub> | 1.6366 (3.9108; p=0.676)<br><sub>sector-cl. (4.6882; p=0.732; WCB p=0.737)</sub> |
| national growth (A) x UI: max_wba_2000 (centred) | -0.0282 (0.0286; p=0.324)<br><sub>sector-cl. (0.0235; p=0.250; WCB p=0.207)</sub> | -0.0000 (0.0000; p=0.298)<br><sub>sector-cl. (0.0000; p=0.288; WCB p=0.272)</sub> | -0.0000 (0.0000; p=0.889)<br><sub>sector-cl. (0.0000; p=0.848; WCB p=0.858)</sub> | -0.0001** (0.0000; p=0.021)<br><sub>sector-cl. (0.0000; p=<0.001; WCB p=0.005)***</sub> | -0.0000 (0.0000; p=0.168)<br><sub>sector-cl. (0.0000; p=0.197; WCB p=0.273)</sub> | -0.1015** (0.0489; p=0.038)<br><sub>sector-cl. (0.0430; p=0.032; WCB p=0.057)*</sub> | -0.0881* (0.0516; p=0.088)<br><sub>sector-cl. (0.0402; p=0.045; WCB p=0.070)*</sub> |
| N | 3,939 | 3,960 | 3,806 | 3,947 | 3,786 | 3,947 | 3,786 |
| Mothers / women | 2,771 | 2,762 | 2,655 | 2,756 | 2,645 | 2,756 | 2,645 |
| Clusters: state x sector / sector | 590 / 16 | 591 / 16 | 586 / 16 | 591 / 16 | 586 / 16 | 591 / 16 | 586 / 16 |
| Mean outcome | -4.061 | 0.818 | 0.822 | 0.715 | 0.730 | 1265.451 | 1299.256 |
| **ur_nat_dt x afdc_max3** | | | | | | | |
| national unemployment rate (C) | -14.5359 (8.8234; p=0.100)<br><sub>sector-cl. (6.0867; p=0.031; WCB p=0.054)*</sub> | 0.0024 (0.0059; p=0.680)<br><sub>sector-cl. (0.0032; p=0.462; WCB p=0.456)</sub> | -0.0047 (0.0058; p=0.416)<br><sub>sector-cl. (0.0032; p=0.170; WCB p=0.147)</sub> | 0.0084 (0.0070; p=0.230)<br><sub>sector-cl. (0.0058; p=0.168; WCB p=0.179)</sub> | 0.0033 (0.0068; p=0.624)<br><sub>sector-cl. (0.0047; p=0.484; WCB p=0.583)</sub> | 8.7405 (13.3652; p=0.513)<br><sub>sector-cl. (10.1720; p=0.404; WCB p=0.419)</sub> | 11.4558 (13.5141; p=0.397)<br><sub>sector-cl. (7.7110; p=0.158; WCB p=0.201)</sub> |
| national unemployment rate (C) x AFDC/TANF max benefit, 3 persons ($100s of 2000 $, centred) | -3.5689 (2.5809; p=0.167)<br><sub>sector-cl. (2.1547; p=0.118; WCB p=0.142)</sub> | 0.0014 (0.0019; p=0.442)<br><sub>sector-cl. (0.0015; p=0.351; WCB p=0.331)</sub> | -0.0004 (0.0015; p=0.814)<br><sub>sector-cl. (0.0007; p=0.615; WCB p=0.598)</sub> | -0.0006 (0.0021; p=0.778)<br><sub>sector-cl. (0.0013; p=0.666; WCB p=0.635)</sub> | 0.0003 (0.0020; p=0.866)<br><sub>sector-cl. (0.0015; p=0.823; WCB p=0.839)</sub> | 1.5917 (3.9521; p=0.687)<br><sub>sector-cl. (2.7922; p=0.577; WCB p=0.624)</sub> | 1.6981 (3.8993; p=0.663)<br><sub>sector-cl. (2.0192; p=0.414; WCB p=0.400)</sub> |
| N | 4,134 | 4,161 | 4,001 | 4,148 | 3,981 | 4,148 | 3,981 |
| Mothers / women | 2,886 | 2,883 | 2,773 | 2,877 | 2,763 | 2,877 | 2,763 |
| Clusters: state x sector / sector | 595 / 16 | 596 / 16 | 592 / 16 | 596 / 16 | 592 / 16 | 596 / 16 | 592 / 16 |
| Mean outcome | -6.521 | 0.817 | 0.819 | 0.710 | 0.723 | 1254.571 | 1284.854 |
| **ur_nat_dt x afdc_fs_max3** | | | | | | | |
| national unemployment rate (C) | -14.0560 (8.8175; p=0.111)<br><sub>sector-cl. (6.1734; p=0.038; WCB p=0.057)*</sub> | 0.0022 (0.0059; p=0.703)<br><sub>sector-cl. (0.0033; p=0.508; WCB p=0.510)</sub> | -0.0047 (0.0057; p=0.411)<br><sub>sector-cl. (0.0032; p=0.166; WCB p=0.148)</sub> | 0.0083 (0.0070; p=0.236)<br><sub>sector-cl. (0.0058; p=0.172; WCB p=0.182)</sub> | 0.0031 (0.0068; p=0.648)<br><sub>sector-cl. (0.0046; p=0.514; WCB p=0.606)</sub> | 8.1487 (13.3476; p=0.542)<br><sub>sector-cl. (10.3626; p=0.444; WCB p=0.456)</sub> | 10.9285 (13.4969; p=0.418)<br><sub>sector-cl. (7.6564; p=0.174; WCB p=0.211)</sub> |
| national unemployment rate (C) x AFDC/TANF + food stamps max, 3 persons ($100s of 2000 $, centred) | -4.5256 (3.1534; p=0.152)<br><sub>sector-cl. (2.6979; p=0.114; WCB p=0.149)</sub> | 0.0019 (0.0022; p=0.396)<br><sub>sector-cl. (0.0020; p=0.366; WCB p=0.369)</sub> | -0.0001 (0.0019; p=0.944)<br><sub>sector-cl. (0.0008; p=0.872; WCB p=0.868)</sub> | -0.0005 (0.0025; p=0.840)<br><sub>sector-cl. (0.0017; p=0.761; WCB p=0.739)</sub> | 0.0007 (0.0025; p=0.795)<br><sub>sector-cl. (0.0019; p=0.731; WCB p=0.726)</sub> | 2.1887 (5.0353; p=0.664)<br><sub>sector-cl. (3.4583; p=0.536; WCB p=0.550)</sub> | 2.8366 (4.9927; p=0.570)<br><sub>sector-cl. (2.8195; p=0.330; WCB p=0.297)</sub> |
| N | 4,134 | 4,161 | 4,001 | 4,148 | 3,981 | 4,148 | 3,981 |
| Mothers / women | 2,886 | 2,883 | 2,773 | 2,877 | 2,763 | 2,877 | 2,763 |
| Clusters: state x sector / sector | 595 / 16 | 596 / 16 | 592 / 16 | 596 / 16 | 592 / 16 | 596 / 16 | 592 / 16 |
| Mean outcome | -6.521 | 0.817 | 0.819 | 0.710 | 0.723 | 1254.571 | 1284.854 |
| **ur_nat_dt x max_wba** | | | | | | | |
| national unemployment rate (C) | -13.6210 (9.2256; p=0.140)<br><sub>sector-cl. (6.3072; p=0.047; WCB p=0.055)*</sub> | 0.0007 (0.0058; p=0.898)<br><sub>sector-cl. (0.0033; p=0.827; WCB p=0.812)</sub> | -0.0061 (0.0056; p=0.274)<br><sub>sector-cl. (0.0033; p=0.083; WCB p=0.069)*</sub> | 0.0064 (0.0070; p=0.361)<br><sub>sector-cl. (0.0067; p=0.352; WCB p=0.421)</sub> | 0.0012 (0.0066; p=0.862)<br><sub>sector-cl. (0.0047; p=0.809; WCB p=0.815)</sub> | 4.2205 (13.1846; p=0.749)<br><sub>sector-cl. (11.5882; p=0.721; WCB p=0.735)</sub> | 6.7273 (13.1004; p=0.608)<br><sub>sector-cl. (7.8847; p=0.407; WCB p=0.432)</sub> |
| national unemployment rate (C) x UI: max_wba (centred) | 0.0113 (0.0446; p=0.800)<br><sub>sector-cl. (0.0278; p=0.690; WCB p=0.676)</sub> | 0.0000 (0.0000; p=0.259)<br><sub>sector-cl. (0.0000; p=0.304; WCB p=0.300)</sub> | 0.0000 (0.0000; p=0.260)<br><sub>sector-cl. (0.0000; p=0.282; WCB p=0.327)</sub> | 0.0001 (0.0000; p=0.128)<br><sub>sector-cl. (0.0000; p=0.026; WCB p=0.044)**</sub> | 0.0001 (0.0000; p=0.133)<br><sub>sector-cl. (0.0000; p=0.041; WCB p=0.067)*</sub> | 0.1305* (0.0761; p=0.087)<br><sub>sector-cl. (0.0515; p=0.023; WCB p=0.033)**</sub> | 0.1323* (0.0800; p=0.099)<br><sub>sector-cl. (0.0521; p=0.023; WCB p=0.049)**</sub> |
| N | 4,134 | 4,160 | 4,000 | 4,147 | 3,980 | 4,147 | 3,980 |
| Mothers / women | 2,886 | 2,882 | 2,772 | 2,876 | 2,762 | 2,876 | 2,762 |
| Clusters: state x sector / sector | 595 / 16 | 596 / 16 | 592 / 16 | 596 / 16 | 592 / 16 | 596 / 16 | 592 / 16 |
| Mean outcome | -6.521 | 0.817 | 0.819 | 0.711 | 0.723 | 1254.778 | 1284.654 |
| **ur_nat_dt x max_wba_2000** | | | | | | | |
| national unemployment rate (C) | -13.6557 (9.1850; p=0.138)<br><sub>sector-cl. (6.3805; p=0.049; WCB p=0.060)*</sub> | 0.0008 (0.0056; p=0.882)<br><sub>sector-cl. (0.0031; p=0.794; WCB p=0.794)</sub> | -0.0058 (0.0056; p=0.298)<br><sub>sector-cl. (0.0033; p=0.099; WCB p=0.081)*</sub> | 0.0068 (0.0069; p=0.320)<br><sub>sector-cl. (0.0059; p=0.261; WCB p=0.296)</sub> | 0.0018 (0.0066; p=0.787)<br><sub>sector-cl. (0.0046; p=0.706; WCB p=0.727)</sub> | 5.0716 (12.9934; p=0.696)<br><sub>sector-cl. (10.2719; p=0.629; WCB p=0.631)</sub> | 7.9763 (12.9911; p=0.539)<br><sub>sector-cl. (7.4940; p=0.304; WCB p=0.324)</sub> |
| national unemployment rate (C) x UI: max_wba_2000 (centred) | 0.0222 (0.0648; p=0.733)<br><sub>sector-cl. (0.0430; p=0.614; WCB p=0.617)</sub> | 0.0001 (0.0001; p=0.146)<br><sub>sector-cl. (0.0001; p=0.205; WCB p=0.197)</sub> | 0.0001 (0.0001; p=0.246)<br><sub>sector-cl. (0.0000; p=0.236; WCB p=0.198)</sub> | 0.0001 (0.0001; p=0.128)<br><sub>sector-cl. (0.0000; p=0.018; WCB p=0.076)*</sub> | 0.0001 (0.0001; p=0.178)<br><sub>sector-cl. (0.0000; p=0.037; WCB p=0.063)*</sub> | 0.1855* (0.1074; p=0.085)<br><sub>sector-cl. (0.0654; p=0.012; WCB p=0.055)*</sub> | 0.1803 (0.1180; p=0.127)<br><sub>sector-cl. (0.0713; p=0.023; WCB p=0.056)*</sub> |
| N | 4,134 | 4,160 | 4,000 | 4,147 | 3,980 | 4,147 | 3,980 |
| Mothers / women | 2,886 | 2,882 | 2,772 | 2,876 | 2,762 | 2,876 | 2,762 |
| Clusters: state x sector / sector | 595 / 16 | 596 / 16 | 592 / 16 | 596 / 16 | 592 / 16 | 596 / 16 | 592 / 16 |
| Mean outcome | -6.521 | 0.817 | 0.819 | 0.711 | 0.723 | 1254.778 | 1284.654 |
| State FE, birth-year FE, husband-sector FE, mother controls + benefit level | yes | yes | yes | yes | yes | yes | yes |

UI generosity: max_wba, max_wba_2000 from data/ui_generosity.csv.

### Table 6. Placebos (mothers employed in b-1)

| | Husband hours b - pre | Wife employed b+1 | Wife employed b+2 | Wife hours b+1 |
|---|---|---|---|---|
| **A. Husband's sector shock in b-2 (national growth, relative to trend)** | | | | |
| g_nat_dt_l2 | -1.6503 (2.9669; p=0.578)<br><sub>sector-cl. (2.3861; p=0.500; WCB p=0.494)</sub> | -0.0005 (0.0018; p=0.781)<br><sub>sector-cl. (0.0018; p=0.779; WCB p=0.795)</sub> | -0.0008 (0.0020; p=0.701)<br><sub>sector-cl. (0.0017; p=0.652; WCB p=0.641)</sub> | -2.4462 (3.9411; p=0.535)<br><sub>sector-cl. (4.2535; p=0.574; WCB p=0.605)</sub> |
| N | 3,638 | 3,650 | 3,501 | 3,637 |
| Mothers / women | 2,586 | 2,571 | 2,468 | 2,565 |
| Clusters: state x sector / sector | 575 / 16 | 577 / 16 | 569 / 16 | 577 / 16 |
| Mean outcome | -1.921 | 0.824 | 0.825 | 1287.263 |
| **B. Husband's sector shock in b and in b-2 jointly** | | | | |
| g_nat_dt | 5.0435* (2.8651; p=0.079)<br><sub>sector-cl. (2.7938; p=0.091; WCB p=0.134)</sub> | -0.0010 (0.0020; p=0.606)<br><sub>sector-cl. (0.0019; p=0.598; WCB p=0.578)</sub> | 0.0003 (0.0019; p=0.871)<br><sub>sector-cl. (0.0023; p=0.892; WCB p=0.907)</sub> | -0.7896 (4.3868; p=0.857)<br><sub>sector-cl. (3.6057; p=0.830; WCB p=0.843)</sub> |
| g_nat_dt_l2 | -0.4416 (3.0787; p=0.886)<br><sub>sector-cl. (2.3678; p=0.855; WCB p=0.861)</sub> | -0.0007 (0.0019; p=0.695)<br><sub>sector-cl. (0.0017; p=0.678; WCB p=0.716)</sub> | -0.0007 (0.0021; p=0.738)<br><sub>sector-cl. (0.0018; p=0.701; WCB p=0.701)</sub> | -2.6235 (4.0038; p=0.513)<br><sub>sector-cl. (3.9125; p=0.513; WCB p=0.526)</sub> |
| N | 3,638 | 3,650 | 3,501 | 3,637 |
| Mothers / women | 2,586 | 2,571 | 2,468 | 2,565 |
| Clusters: state x sector / sector | 575 / 16 | 577 / 16 | 569 / 16 | 577 / 16 |
| Mean outcome | -1.921 | 0.824 | 0.825 | 1287.263 |
| **C. Husband's sector unemployment rate in b-2 (relative to trend)** | | | | |
| ur_nat_dt_l2 | 4.3249 (9.8159; p=0.660)<br><sub>sector-cl. (10.0362; p=0.673; WCB p=0.724)</sub> | -0.0024 (0.0061; p=0.694)<br><sub>sector-cl. (0.0092; p=0.799; WCB p=0.840)</sub> | -0.0044 (0.0064; p=0.496)<br><sub>sector-cl. (0.0063; p=0.498; WCB p=0.591)</sub> | -8.4174 (13.3531; p=0.529)<br><sub>sector-cl. (15.3355; p=0.591; WCB p=0.732)</sub> |
| N | 3,935 | 3,955 | 3,799 | 3,942 |
| Mothers / women | 2,764 | 2,754 | 2,648 | 2,748 |
| Clusters: state x sector / sector | 588 / 16 | 588 / 16 | 583 / 16 | 588 / 16 |
| Mean outcome | -3.185 | 0.820 | 0.820 | 1270.815 |
| **D. Wife's own pre-birth sector: national women's employment growth (wife-sector FE)** | | | | |
| g_nat_dt_wf | -3.8160 (2.8013; p=0.174)<br><sub>sector-cl. (3.0932; p=0.236; WCB p=0.279)</sub> | 0.0042** (0.0021; p=0.043)<br><sub>sector-cl. (0.0019; p=0.043; WCB p=0.041)**</sub> | 0.0006 (0.0019; p=0.751)<br><sub>sector-cl. (0.0017; p=0.722; WCB p=0.716)</sub> | 5.8699 (4.1950; p=0.162)<br><sub>sector-cl. (2.8775; p=0.059; WCB p=0.049)**</sub> |
| N | 3,719 | 3,733 | 3,587 | 3,721 |
| Mothers / women | 2,622 | 2,613 | 2,512 | 2,608 |
| Clusters: state x sector / sector | 534 / 16 | 533 / 16 | 533 / 16 | 532 / 16 |
| Mean outcome | -7.041 | 0.827 | 0.834 | 1296.250 |
| **E. Wife's own sector (women) and husband's sector (men) jointly (both sector FE; wife-sector clusters)** | | | | |
| g_nat_dt_wf | -4.2109 (2.8112; p=0.135)<br><sub>sector-cl. (3.1134; p=0.196; WCB p=0.229)</sub> | 0.0043** (0.0020; p=0.036)<br><sub>sector-cl. (0.0019; p=0.037; WCB p=0.043)**</sub> | 0.0006 (0.0019; p=0.770)<br><sub>sector-cl. (0.0018; p=0.764; WCB p=0.761)</sub> | 5.8987 (4.2111; p=0.162)<br><sub>sector-cl. (2.9257; p=0.062; WCB p=0.051)*</sub> |
| g_nat_dt | 5.6059** (2.5246; p=0.027)<br><sub>sector-cl. (2.4547; p=0.037; WCB p=0.055)*</sub> | -0.0003 (0.0019; p=0.860)<br><sub>sector-cl. (0.0029; p=0.910; WCB p=0.933)</sub> | 0.0016 (0.0017; p=0.364)<br><sub>sector-cl. (0.0019; p=0.419; WCB p=0.441)</sub> | 2.0313 (4.1688; p=0.626)<br><sub>sector-cl. (4.4581; p=0.655; WCB p=0.666)</sub> |
| N | 3,719 | 3,733 | 3,587 | 3,721 |
| Mothers / women | 2,622 | 2,613 | 2,512 | 2,608 |
| Clusters: state x sector / sector | 534 / 16 | 533 / 16 | 533 / 16 | 532 / 16 |
| Mean outcome | -7.041 | 0.827 | 0.834 | 1296.250 |
| State FE, birth-year FE, sector FE, controls | yes | yes | yes | yes |

Panels D-E: mothers with an industry in the link wave; clusters state x wife's sector and wife's sector. g_nat_dt_wf = national (leave-own-state-out) growth of WOMEN's employment in the wife's sector.

### Table 7. Comparison: childless married women (woman-years t, employed in t-1, husband's sector shock in t)

| | Husband hours t - pre | Wife employed t+1 | Wife employed t+2 | Wife hours t+1 |
|---|---|---|---|---|
| **F. Childless married women (no birth up to t+2), national growth (A)** | | | | |
| g_nat_dt | 1.6995 (3.2601; p=0.602)<br><sub>sector-cl. (3.1504; p=0.597; WCB p=0.622)</sub> | 0.0007 (0.0009; p=0.413)<br><sub>sector-cl. (0.0010; p=0.477; WCB p=0.499)</sub> | 0.0007 (0.0009; p=0.482)<br><sub>sector-cl. (0.0008; p=0.404; WCB p=0.426)</sub> | -1.6702 (2.9627; p=0.573)<br><sub>sector-cl. (3.2605; p=0.616; WCB p=0.627)</sub> |
| N | 4,191 | 4,484 | 4,153 | 4,462 |
| Mothers / women | 1,153 | 1,157 | 1,109 | 1,153 |
| Clusters: state x sector / sector | 498 / 16 | 507 / 16 | 501 / 16 | 506 / 16 |
| Mean outcome | -3.838 | 0.956 | 0.951 | 1869.680 |
| **G. Childless married women, national unemployment rate (C)** | | | | |
| ur_nat_dt | 4.6415 (9.0412; p=0.608)<br><sub>sector-cl. (7.0962; p=0.523; WCB p=0.598)</sub> | 0.0009 (0.0031; p=0.784)<br><sub>sector-cl. (0.0021; p=0.684; WCB p=0.677)</sub> | -0.0014 (0.0033; p=0.665)<br><sub>sector-cl. (0.0024; p=0.563; WCB p=0.545)</sub> | 1.7456 (11.9835; p=0.884)<br><sub>sector-cl. (12.8063; p=0.893; WCB p=0.969)</sub> |
| N | 4,430 | 4,743 | 4,404 | 4,721 |
| Mothers / women | 1,173 | 1,178 | 1,129 | 1,174 |
| Clusters: state x sector / sector | 503 / 16 | 511 / 16 | 504 / 16 | 510 / 16 |
| Mean outcome | -3.173 | 0.955 | 0.949 | 1858.343 |
| State FE, year FE, husband-sector FE, controls | yes | yes | yes | yes |

Woman-years of CAH women with no birth up to t+2, wife (legal) of a male head in a wave in [t-3, t-1], aged 21-39, employed in t-1: 5,576 woman-years, 1,347 women (several years per woman; the mother clusters of the other tables are replaced by the same clusters).

## NLSY79 complement

The public NLSY79 has no state, and the spouse questions give the husband's occupation (OCCSP-55I, 1979-1996) but not his industry, so no sector shock can be built. Instead: the husband's own weeks worked in the calendar year before the birth and in the birth year (Q2-15A, asked 1980-1994 annually) as an event. Sample: births 1980-93 to married mothers still married at the next interview, husband worked >= 48 weeks in b-1; event = < 40 weeks in the birth year. OLS with birth-year FE; controls: age, age^2, Black, education (LHS, college), birth order; s.e. clustered by mother (both lines). The event is not exogenous (husbands' weeks can respond to the birth and to the wife's work); this is a descriptive event comparison.

### Table 8. NLSY79: husband's lost weeks in the birth year and the mother's weekly employment

| | Husband wage income b - b-1 (2000 $) | Share of weeks employed, months -12..-1 | Share of weeks employed, months 0-12 | Share of weeks employed, months 13-24 |
|---|---|---|---|---|
| **A. All married mothers (husband attached)** | | | | |
| event | -10822.3844*** (2069.0658; p=<0.001) | -0.0387 (0.0338; p=0.253) | 0.0084 (0.0356; p=0.814) | 0.0077 (0.0401; p=0.847) |
| N | 2,028 | 2,431 | 2,434 | 2,423 |
| Mothers / women | 1,338 | 1,531 | 1,534 | 1,528 |
| Clusters (mothers) | 1,338 | 1,531 | 1,534 | 1,528 |
| Mean outcome | 1378.996 | 0.616 | 0.467 | 0.564 |
| **B. Mother employed before the birth** | | | | |
| event | -11353.3336*** (2716.9811; p=<0.001) | -0.0367* (0.0219; p=0.094) | -0.0146 (0.0470; p=0.756) | 0.0239 (0.0480; p=0.618) |
| N | 1,383 | 1,614 | 1,610 | 1,605 |
| Mothers / women | 1,017 | 1,160 | 1,159 | 1,154 |
| Clusters (mothers) | 1,017 | 1,160 | 1,159 | 1,154 |
| Mean outcome | 1284.956 | 0.885 | 0.632 | 0.713 |
| **C. Mother not employed before the birth** | | | | |
| event | -9983.2863*** (3257.5069; p=0.002) | 0.0276 (0.0230; p=0.231) | 0.0828* (0.0461; p=0.073) | 0.0370 (0.0588; p=0.530) |
| N | 636 | 817 | 818 | 811 |
| Mothers / women | 492 | 609 | 610 | 606 |
| Clusters (mothers) | 492 | 609 | 610 | 606 |
| Mean outcome | 1584.880 | 0.084 | 0.144 | 0.271 |
| **D. Weeks the husband did not work in the birth year (continuous)** | | | | |
| weeks_lost | -431.6296*** (60.6494; p=<0.001) | -0.0022** (0.0011; p=0.034) | 0.0001 (0.0011; p=0.953) | -0.0002 (0.0013; p=0.852) |
| N | 2,028 | 2,431 | 2,434 | 2,423 |
| Mothers / women | 1,338 | 1,531 | 1,534 | 1,528 |
| Clusters (mothers) | 1,338 | 1,531 | 1,534 | 1,528 |
| Mean outcome | 1378.996 | 0.616 | 0.467 | 0.564 |
| **E. Event x Black (all married mothers)** | | | | |
| event | -11588.0247*** (2572.5810; p=<0.001) | -0.0050 (0.0387; p=0.898) | 0.0562 (0.0396; p=0.156) | 0.0637 (0.0452; p=0.159) |
| event_x_black | 3561.6329 (3193.2310; p=0.265) | -0.1291* (0.0758; p=0.089) | -0.1830** (0.0807; p=0.024) | -0.2178** (0.0852; p=0.011) |
| event: total for Black | -8026.3918*** (1919.4805; p=<0.001) | -0.1341** (0.0653; p=0.040) | -0.1268* (0.0705; p=0.072) | -0.1540** (0.0724; p=0.034) |
| N | 2,028 | 2,431 | 2,434 | 2,423 |
| Mothers / women | 1,338 | 1,531 | 1,534 | 1,528 |
| Clusters (mothers) | 1,338 | 1,531 | 1,534 | 1,528 |
| Mean outcome | 1378.996 | 0.616 | 0.467 | 0.564 |
| Birth-year FE, controls | yes | yes | yes | yes |

### Table 9. NLSY79 event study: share of weeks employed in quarter q (13 weeks) relative to the birth, event vs no event

Rows: quarter (0 = the 13 weeks from the birth week). Columns: samples; each cell a separate regression. N (max over quarters): Black 503, White 1,932, all 2,432, employed before 1,613

|   quarter | Black                      | White                   | all                      | employed before          |
|----------:|:---------------------------|:------------------------|:-------------------------|:-------------------------|
|        -8 | -0.004 (0.096; p=0.967)    | -0.031 (0.042; p=0.460) | -0.030 (0.039; p=0.446)  | -0.046 (0.044; p=0.289)  |
|        -7 | -0.144 (0.088; p=0.101)    | -0.033 (0.042; p=0.435) | -0.064* (0.038; p=0.095) | -0.079* (0.042; p=0.057) |
|        -6 | -0.174** (0.082; p=0.034)  | -0.033 (0.045; p=0.466) | -0.073* (0.040; p=0.064) | -0.073 (0.045; p=0.105)  |
|        -5 | -0.135 (0.088; p=0.125)    | -0.019 (0.042; p=0.658) | -0.053 (0.038; p=0.167)  | -0.056* (0.033; p=0.088) |
|        -4 | -0.170* (0.093; p=0.068)   | -0.007 (0.043; p=0.871) | -0.055 (0.040; p=0.167)  | -0.023 (0.024; p=0.336)  |
|        -3 | -0.142* (0.083; p=0.087)   | -0.005 (0.045; p=0.907) | -0.047 (0.039; p=0.233)  | -0.021 (0.017; p=0.205)  |
|        -2 | -0.125* (0.075; p=0.096)   | -0.021 (0.048; p=0.662) | -0.047 (0.041; p=0.252)  | -0.063 (0.040; p=0.116)  |
|        -1 | -0.060 (0.089; p=0.503)    | 0.007 (0.045; p=0.868)  | -0.005 (0.040; p=0.896)  | -0.039 (0.048; p=0.409)  |
|         0 | -0.147** (0.062; p=0.018)  | 0.026 (0.041; p=0.532)  | -0.016 (0.035; p=0.659)  | -0.036 (0.051; p=0.478)  |
|         1 | -0.166** (0.082; p=0.045)  | 0.049 (0.048; p=0.315)  | -0.001 (0.043; p=0.981)  | -0.016 (0.059; p=0.785)  |
|         2 | -0.145 (0.092; p=0.115)    | 0.069 (0.049; p=0.164)  | 0.021 (0.044; p=0.636)   | -0.002 (0.055; p=0.970)  |
|         3 | -0.147* (0.086; p=0.088)   | 0.079* (0.048; p=0.100) | 0.027 (0.043; p=0.528)   | -0.004 (0.057; p=0.943)  |
|         4 | -0.209*** (0.073; p=0.004) | 0.077 (0.049; p=0.114)  | 0.006 (0.043; p=0.888)   | 0.011 (0.056; p=0.841)   |
|         5 | -0.164** (0.080; p=0.041)  | 0.071 (0.051; p=0.163)  | 0.019 (0.044; p=0.670)   | 0.049 (0.051; p=0.342)   |
|         6 | -0.172* (0.088; p=0.052)   | 0.040 (0.051; p=0.432)  | -0.007 (0.045; p=0.886)  | 0.015 (0.054; p=0.779)   |
|         7 | -0.157* (0.087; p=0.071)   | 0.077 (0.049; p=0.116)  | 0.023 (0.044; p=0.601)   | 0.030 (0.054; p=0.577)   |
|         8 | -0.154* (0.088; p=0.082)   | 0.080 (0.049; p=0.101)  | 0.028 (0.044; p=0.520)   | 0.017 (0.052; p=0.737)   |

NLSY79 sample: married mothers, births 1980-93, still married at the next interview, husband's weeks in b-1 and b: 2,993;   husband attached (>= 48 weeks in b-1): 2,447;   ... with event (< 40 weeks in the birth year): 120;   ... mother employed before (>= half the weeks in quarters -4..-2): 1,615;   ... event and employed before: 68

## PSID sample

| step | births |
|---|---|
| births 1977-2021, White/Black head, mother 15-49, state observed (first_stage_births.pkl) | 15,815 |
|   married at the birth | 9,211 |
|   birth years 1980-2019 (CPS MORG shocks) | 8,154 |
|   mother is wife / partner of a male head in a wave in [b-3, b-1] | 6,465 |
|   husband's industry observed and mapped to a sector | 6,025 |
|   mother employed in b-1 (main sample) | 4,559 |
|   ... with the national sector shock (g_nat_dt) | 4,289 |
|   mother not employed in b-1 | 1,150 |
|   mother's employment in b-1 not observed | 316 |

Agreement of the recomputed wife employment at b+1 with first_stage_births.pkl (births observed in both): 1.0000.
Husband's sector taken from the link wave b-1 / b-2 / b-3: 1.0: 4,551, 2.0: 1,368, 3.0: 106.

### Sectors

|                                                       |   husbands (all married births) |   wives employed in b-1 (own sector) |
|:------------------------------------------------------|--------------------------------:|-------------------------------------:|
| Agriculture, forestry, fishing                        |                             203 |                                   32 |
| Business, repair, professional services               |                             625 |                                  388 |
| Communications, broadcasting, telecom                 |                             116 |                                   56 |
| Construction                                          |                             687 |                                   48 |
| Durable manufacturing                                 |                             841 |                                  207 |
| Eating, drinking, accommodation                       |                             209 |                                  274 |
| Education and social services                         |                             355 |                                  734 |
| Finance, insurance, real estate                       |                             287 |                                  437 |
| Health                                                |                             251 |                                  765 |
| Mining                                                |                              59 |                                   16 |
| Nondurable manufacturing (incl. printing, publishing) |                             468 |                                  196 |
| Personal, household, entertainment, membership        |                             170 |                                  204 |
| Public administration (incl. postal)                  |                             495 |                                  195 |
| Retail trade (excl. eating, drinking)                 |                             555 |                                  437 |
| Transportation, utilities, sanitary                   |                             422 |                                   99 |
| Wholesale trade                                       |                             282 |                                   91 |

### Main sample by race (black = 1)

|   black |   births |   h_dhours_0 |   h_loss_0 |   w_emp_p1 |   w_hours_p1 |   g_nat_dt |   ur_nat_dt |   liquid |   afdc_max3 |
|--------:|---------:|-------------:|-----------:|-----------:|-------------:|-----------:|------------:|---------:|------------:|
|       0 |     3652 |       -1.764 |      0.081 |      0.802 |      1194.78 |     -0.158 |      -0.086 |  3743.48 |       4.353 |
|       1 |      907 |      -18.062 |      0.137 |      0.858 |      1459.64 |      0.019 |      -0.115 |   830.68 |       3.455 |

### PSID industry variables used (family files)

|   wave | h_ind                                             | h_indu                                 | w_ind                                             |
|-------:|:--------------------------------------------------|:---------------------------------------|:--------------------------------------------------|
|   1976 | V4460_A 'INDUSTRY   OF HEAD         76'           |                                        | V4606_A 'INDUSTRY   OF WIFE         76'           |
|   1977 | V5375_A 'INDUSTRY   OF HEAD         77'           |                                        | V5508_A 'INDUSTRY   OF WIFE         77'           |
|   1978 | V5874_A 'INDUSTRY   OF HEAD         78'           |                                        | V6040_A 'INDUSTRY   OF WIFE         78'           |
|   1979 | V6498_A 'INDUSTRY   OF HEAD         79'           |                                        | V6597_A 'INDUSTRY   OF WIFE         79'           |
|   1980 | V7101_A 'INDUSTRY   OF HEAD         80'           |                                        | V7199_A 'INDUSTRY   OF WIFE         80'           |
|   1981 | V7713 'C9 MAIN IND:3 DIGT(H-E)'                   | V7808 'D10 IND-LAST JOB (HD-U)'        | V7886 'F10 INDUSTRY     (WF-E)'                   |
|   1982 | V8381 'C9 MAIN IND:3 DIGT(H-E)'                   | V8469 'D9 IND-LAST JOB (HD-U)'         | V8545 'F10 INDUSTRY    (WF-E)'                    |
|   1983 | V9012 'C9 MAIN IND:3 DIGT(H-E)'                   | V9106 'D10 IND-LAST JOB (HD-U)'        | V9195 'F10 INDUSTRY     (WF-E)'                   |
|   1984 | V10461 'C10 MAIN IND:3 DIGT(H-E)'                 | V10606 'D10 IND-LAST JOB (HD-U)'       | V10679 'F11 INDUSTRY     (WF-E)'                  |
|   1985 | V11652 'B17 MAIN IND:3 DIGT(H-E)'                 | V11759 'C19 IND-LAST JOB  (HD-U)'      | V12015 'J17 MAIN IND:3 DIGT(W-E)'                 |
|   1986 | V13055 'B11 MAIN IND:3 DIGT(H-E)'                 | V13155 'C19 IND-LAST JOB  (HD-U)'      | V13234 'D11 MAIN IND:3 DIGT(W-E)'                 |
|   1987 | V14155 'B11 MAIN IND:3 DIGT(H-E)'                 | V14253 'C19 IND-LAST JOB  (HD-U)'      | V14330 'D11 MAIN IND:3 DIGT(W-E)'                 |
|   1988 | V15163 'B11 MAIN IND:3 DIGT(H-E)'                 | V15324 'C11 IND-LAST JOB  (HD-U)'      | V15465 'D11 MAIN IND:3 DIGT(W-E)'                 |
|   1989 | V16664 'B11 MAIN IND:3 DIGT(H-E)'                 | V16839 'C11 IND-LAST JOB  (HD-U)'      | V16983 'D11 MAIN IND:3 DIGT(W-E)'                 |
|   1990 | V18102 'B11 MAIN IND:3 DIGT(H-E)'                 | V18263 'C11 IND-LAST JOB  (HD-U)'      | V18404 'D11 MAIN IND:3 DIGT(W-E)'                 |
|   1991 | V19402 'B11 MAIN IND:3 DIGT(H-E)'                 | V19563 'C11 IND-LAST JOB  (HD-U)'      | V19704 'D11 MAIN IND:3 DIGT(W-E)'                 |
|   1992 | V20702 'B11 MAIN IND:3 DIGT(H-E)'                 | V20863 'C11 IND-LAST JOB  (HD-U)'      | V21004 'D11 MAIN IND:3 DIGT(W-E)'                 |
|   1993 | V22457 'B10 MAIN INDUSTRY: 3 DIGIT (HD-E)'        | V22651 'C11 INDUSTRY-LAST JOB (HD-U)'  | V22810 'D10 MAIN INDUSTRY:3 DIGIT (WF-E)'         |
|   1994 | ER4018 'B10 MAIN INDUSTRY: 3 DIGIT (HD-E)'        | ER4033 'C11 INDUSTRY-LAST JOB (HD-U)'  | ER4049 'D10 MAIN INDUSTRY:3 DIGIT (WF-E)'         |
|   1995 | ER6858 'B10 MAIN INDUSTRY: 3 DIGIT (HD-E)'        | ER6873 'C11 INDUSTRY-LAST JOB (HD-U)'  | ER6889 'D10 MAIN INDUSTRY:3 DIGIT (WF-E)'         |
|   1996 | ER9109 'B10 MAIN INDUSTRY: 3 DIGIT (HD-E)'        | ER9124 'C11 INDUSTRY-LAST JOB (HD-U)'  | ER9140 'D10 MAIN INDUSTRY:3 DIGIT (WF-E)'         |
|   1997 | ER12086 'B10 MAIN INDUSTRY: 3 DIGIT (HD-E)'       | ER12101 'C11 INDUSTRY-LAST JOB (HD-U)' | ER12117 'D10 MAIN INDUSTRY:3 DIGIT (WF-E)'        |
|   1999 | ER13216 'B10 MAIN INDUSTRY: 3 DIGIT (HD-E)'       | ER13494 'C11 INDUSTRY-LAST JOB (HD-U)' | ER13728 'D10 MAIN INDUSTRY:3 DIGIT (WF-E)'        |
|   2001 | ER17227 'B10 MAIN INDUSTRY: 3 DIGIT (HD-E)'       | ER17534 'C11 INDUSTRY-LAST JOB (HD-U)' | ER17797 'D10 MAIN INDUSTRY:3 DIGIT (WF-E)'        |
|   2003 | ER21146 'BC21 MAIN IND FOR JOB 1: 2000 CODE (HD)' |                                        | ER21396 'DE21 MAIN IND FOR JOB 1: 2000 CODE (WF)' |
|   2005 | ER25128 'BC21 MAIN IND FOR JOB 1: 2000 CODE (HD)' |                                        | ER25386 'DE21 MAIN IND FOR JOB 1: 2000 CODE (WF)' |
|   2007 | ER36133 'BC21 MAIN IND FOR JOB 1: 2000 CODE (HD)' |                                        | ER36391 'DE21 MAIN IND FOR JOB 1: 2000 CODE (WF)' |
|   2009 | ER42168 'BC21 MAIN IND FOR JOB 1: 2000 CODE (HD)' |                                        | ER42420 'DE21 MAIN IND FOR JOB 1: 2000 CODE (WF)' |
|   2011 | ER47480 'BC21 MAIN IND FOR JOB 1: 2000 CODE (HD)' |                                        | ER47737 'DE21 MAIN IND FOR JOB 1: 2000 CODE (WF)' |
|   2013 | ER53180 'BC21 MAIN IND FOR JOB 1: 2000 CODE (HD)' |                                        | ER53443 'DE21 MAIN IND FOR JOB 1: 2000 CODE (WF)' |
|   2015 | ER60195 'BC21 MAIN IND FOR JOB 1: 2000 CODE (HD)' |                                        | ER60458 'DE21 MAIN IND FOR JOB 1: 2000 CODE (SP)' |
|   2017 | ER66196 'BC21 MAIN IND FOR JOB 1: 2012 CODE (RP)' |                                        | ER66471 'DE21 MAIN IND FOR JOB 1: 2012 CODE (SP)' |
|   2019 | ER72196 'BC21 MAIN IND FOR JOB 1: 2012 CODE (RP)' |                                        | ER72473 'DE21 MAIN IND FOR JOB 1: 2012 CODE (SP)' |
|   2021 | ER78199 'BC21 MAIN IND FOR JOB 1: 2012 CODE (RP)' |                                        | ER78513 'DE21 MAIN IND FOR JOB 1: 2012 CODE (SP)' |
|   2023 | ER82182 'BC21 MAIN IND FOR JOB 1: 2012 CODE (RP)' |                                        | ER82501 'DE21 MAIN IND FOR JOB 1: 2012 CODE (SP)' |
