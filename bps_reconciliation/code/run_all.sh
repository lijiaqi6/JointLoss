#!/bin/bash
# [bps_reconciliation] run every specification (4 Stata instances in parallel); logs in ../logs/<spec>.log
cd "$(dirname "$0")/../logs"
S="/c/Program Files/StataNow19/StataMP-64.exe"
printf '%s\n' "$@" | xargs -P 4 -I{} "$S" //e do ../code/specs/{}.do
