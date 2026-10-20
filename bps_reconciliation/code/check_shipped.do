* [bps_reconciliation] Step 0 check: data4estimation rebuilt from psid_cons.dta vs BPS's shipped data4estimation.dta
global ship "C:\Users\cm1jil\Dropbox\ReplicationPapers\Consumption Inequality and Family Labor Supply\116142-V1\AER_2012_1549_data\output"
global WORK "C:\Users\cm1jil\AppData\Local\Temp\claude\g--My-Drive-Selection-vs-risk\c16f819d-4913-4b50-9f11-a4daf3178246\scratchpad\bps_work"
use "$ship\data4estimation.dta", clear
ds
local shipvars `r(varlist)'
use "$WORK\base\data4estimation.dta", clear
sort person year
keep `shipvars'
cf `shipvars' using "$ship\data4estimation.dta", all verbose
