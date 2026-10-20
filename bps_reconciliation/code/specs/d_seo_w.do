* Step 1d: SEO in, PSID family longitudinal weights
global SPEC "d_seo_w"
global WORK "C:\Users\cm1jil\AppData\Local\Temp\claude\g--My-Drive-Selection-vs-risk\c16f819d-4913-4b50-9f11-a4daf3178246\scratchpad\bps_work"
global SW_seo 1
global WGT "[pw=weight]"
global RUNS "gmm10 gmm9 beta bs bsbeta"
global BN 50
do "G:\My Drive\JointLoss\bps_reconciliation\code\run_spec.do"
