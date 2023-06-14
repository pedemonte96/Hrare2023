#!/bin/bash
LANG=en_us_8859_1
CYAN='\033[1;32m'
NC='\033[0m' # No Color
dirname=$1

newline="        outputFile = \"/data/submit/pdmonte/outputs/$dirname/{0}/outname_mc{1}_{2}_{3}_{0}.root\".format(year,mc,catTag,catM)"
linenum="$(grep -n -m 1 'outputFile' VGammaMeson_cat.py | cut -d : -f 1)"

sed -i "${linenum}s|.*|${newline}|g" VGammaMeson_cat.py

echo -e "${CYAN}┌───────────────────────────────────────────┐\n│ Check changes in file VGammaMeson_cat.py: │\n└───────────────────────────────────────────┘${NC}"

grep -n -m 1 --color=auto "outputFile" VGammaMeson_cat.py
