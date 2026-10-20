* [bps_reconciliation] caller for Step 2 (attrition on the baseline; step2.do on the listed specifications)
global WORK "C:\Users\cm1jil\AppData\Local\Temp\claude\g--My-Drive-Selection-vs-risk\c16f819d-4913-4b50-9f11-a4daf3178246\scratchpad\bps_work"
global B "$WORK/base"
do "G:\My Drive\JointLoss\bps_reconciliation\code\attrition.do"
global S2SPECS "base b_nostatus a_nowork d_seo f_all"
do "G:\My Drive\JointLoss\bps_reconciliation\code\step2.do"
