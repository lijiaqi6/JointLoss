# Closed-form first steps (starting values and checks)

- gO: 0.1230 (s.e. 0.0183; homoskedastic, for orientation)
- gG: 0.1454 (s.e. 0.0299; homoskedastic, for orientation)
- lrho: -2.4115 (s.e. 0.1109; homoskedastic, for orientation)
- g1: 0.0229 (s.e. 0.0051; homoskedastic, for orientation)
- dg1: -0.0081 (s.e. 0.0068; homoskedastic, for orientation)
- transitory variance = -lag-1 autocovariance of annual stayer growth = 0.0368; permanent variance = Var(growth) - 2 x transitory - drift dispersion = 0.0469 (Var = 0.1209, autocov = -0.0368, N pairs 7,498)
- displacement logit (annual pairs): constant -2.101, x -0.368, Black 0.501
- entry wage OLS (25-29): constant 2.489, x 0.138, schooling 0.034, Black -0.174, Black x schooling 0.023
- access logit on the early job type: -3.979, 0.183, 0.653, -0.429

| moment | data | bootstrap s.e. |
|---|---|---|
| ige_2529_B | 0.1484 | 0.0212 |
| ige_3034_B | 0.1819 | 0.0240 |
| ige_3539_B | 0.1823 | 0.0300 |
| ige_4044_B | 0.1461 | 0.0344 |
| ige_4549_B | 0.1398 | 0.0443 |
| ige_5055_B | 0.1511 | 0.0590 |
| ige_2529_W | 0.2047 | 0.0173 |
| ige_3034_W | 0.3345 | 0.0233 |
| ige_3539_W | 0.3811 | 0.0297 |
| ige_4044_W | 0.4393 | 0.0360 |
| ige_4549_W | 0.4702 | 0.0486 |
| ige_5055_W | 0.4501 | 0.0537 |
| rets_2529_B | 0.0667 | 0.0068 |
| rets_3034_B | 0.0967 | 0.0082 |
| rets_3539_B | 0.1023 | 0.0093 |
| rets_4044_B | 0.0938 | 0.0111 |
| rets_4549_B | 0.1191 | 0.0124 |
| rets_5055_B | 0.1237 | 0.0152 |
| rets_2529_W | 0.0471 | 0.0046 |
| rets_3034_W | 0.0893 | 0.0057 |
| rets_3539_W | 0.1110 | 0.0069 |
| rets_4044_W | 0.1281 | 0.0081 |
| rets_4549_W | 0.1253 | 0.0101 |
| rets_5055_W | 0.1288 | 0.0123 |
| mlw2529_B | 2.3154 | 0.0155 |
| mlw2529_W | 2.5947 | 0.0108 |
| vlw_2529_B | 0.3116 | 0.0097 |
| vlw_3539_B | 0.3824 | 0.0164 |
| vlw_4549_B | 0.3448 | 0.0205 |
| vlw_2529_W | 0.2755 | 0.0074 |
| vlw_3539_W | 0.4134 | 0.0145 |
| vlw_4549_W | 0.5035 | 0.0226 |
| G_t1_B | 0.0308 | 0.0047 |
| G_t2_B | 0.0405 | 0.0085 |
| G_t3_B | 0.1169 | 0.0223 |
| G_t1_W | 0.0663 | 0.0128 |
| G_t2_W | 0.0920 | 0.0106 |
| G_t3_W | 0.1799 | 0.0110 |
| G_e12 | 0.0159 | 0.0028 |
| G_e1315 | 0.0504 | 0.0062 |
| G_e16 | 0.2647 | 0.0129 |
| gst_2534_O | 0.0554 | 0.0032 |
| gst_2534_G | 0.0754 | 0.0067 |
| gst_3555_O | 0.0213 | 0.0017 |
| gst_3555_G | 0.0349 | 0.0042 |
| gst_2534_B | 0.0559 | 0.0062 |
| gst_2534_W | 0.0603 | 0.0030 |
| gste_2534_B | 0.0028 | 0.0030 |
| gste_2534_W | 0.0093 | 0.0016 |
| vgst | 0.1209 | 0.0055 |
| acgst | -0.0369 | 0.0030 |
| mov_2534_B | 0.1270 | 0.0062 |
| mov_3555_B | 0.0900 | 0.0059 |
| dsp_2534_B | 0.1730 | 0.0087 |
| dsp_3555_B | 0.1112 | 0.0062 |
| mov_2534_W | 0.1306 | 0.0044 |
| mov_3555_W | 0.0908 | 0.0037 |
| dsp_2534_W | 0.1024 | 0.0048 |
| dsp_3555_W | 0.0762 | 0.0039 |
| dsp_x | -0.0170 | 0.0055 |
| gmv_2534_B | -0.0064 | 0.0191 |
| gmv_2534_W | 0.0516 | 0.0099 |
| gmv_x | -0.0164 | 0.0138 |
| gds | 0.0051 | 0.0066 |
| zero_B | 0.1095 | 0.0060 |
| zero_W | 0.0389 | 0.0029 |
