#!/bin/bash
LANG=en_us_8859_1
ORG='\033[1;33m'
RED='\033[1;31m'
NC='\033[0m' # No Color
dirname=$(date +%b%d)
dirname=${dirname^^}
#dirname="MAY23"

if [[ ! -d "/data/submit/pdmonte/outputs/${dirname}" ]]; then
    mkdir /data/submit/pdmonte/outputs/${dirname}
else
	echo -e "${RED}  !!!  Directory ${dirname} already exists  !!!  ${NC}"
fi
if [[ ! -d "/data/submit/pdmonte/outputs/${dirname}/2018" ]]; then
    mkdir /data/submit/pdmonte/outputs/${dirname}/2018
fi

echo -e "${ORG}┌───────────────────────────────────────────┐\n│                 Directory                 │\n└───────────────────────────────────────────┘${NC}"

ls -lhR --color=auto "/data/submit/pdmonte/outputs/${dirname}"

#changes directory in VGammaMeson_cat.py
bash changeDate.sh $dirname
