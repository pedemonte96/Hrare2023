#!/bin/bash
LANG=en_us_8859_1
CYAN='\033[1;33m'
NC='\033[0m' # No Color
dirname=$(date +%B%d)
dirname=${dirname^^}

if [[ ! -d "outputs/${dirname}" ]]; then
    mkdir outputs/${dirname}
fi
if [[ ! -d "outputs/${dirname}/2018" ]]; then
    mkdir outputs/${dirname}/2018
fi

echo -e "${CYAN}┌───────────────────────────────────────────┐\n│                 Directory                 │\n└───────────────────────────────────────────┘${NC}"

ls -lhR --color=auto "outputs/${dirname}"

#changes directory in VGammaMeson_cat.py
bash changeDate.sh $dirname