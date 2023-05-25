#!/bin/bash
LANG=en_us_8859_1
ORG='\033[1;33m'
RED='\033[1;31m'
NC='\033[0m' # No Color
dirname=$(date +%B%d)
dirname=${dirname^^}
#dirname="MAY23"

if [[ ! -d "outputs/${dirname}" ]]; then
    mkdir outputs/${dirname}
else
	echo -e "${RED}  !!!  Directory ${dirname} already exists  !!!  ${NC}"
fi
if [[ ! -d "outputs/${dirname}/2018" ]]; then
    mkdir outputs/${dirname}/2018
fi

echo -e "${ORG}┌───────────────────────────────────────────┐\n│                 Directory                 │\n└───────────────────────────────────────────┘${NC}"

ls -lhR --color=auto "outputs/${dirname}"

#changes directory in VGammaMeson_cat.py
bash changeDate.sh $dirname
