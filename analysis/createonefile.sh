#!/bin/bash
ORG='\033[1;33m'
BLU='\033[1;34m'
GRN='\033[1;36m'
CYAN='\033[0;32m'
NC='\033[0m' # No Color

cat=$1
part=$2
num=$3
year=$4

# Create directory if not created
LANG=en_us_8859_1
dirname=$(date +%B%d)
if [[ ! -d "logfiles/${dirname^^}" ]]; then
    mkdir logfiles/${dirname^^}
fi

# Create logfile
LOGFILE="logfiles/${dirname^^}/output_${num}_${cat:2:-3}_${part:2:-3}_${year}_$(date '+%Y%m%d_%H%M%S').log"
if [ -f "$LOGFILE" ]; then
	rm $LOGFILE
fi

# Create Box
echo -ne "${BLU}┌───────────────────────────────────────────────────────────────┐\n│${NC}"
echo -ne "${ORG}┌─────────────────────────────────────────────────────────────┐${BLU}│\n${NC}"
echo -ne "${BLU}│${ORG}│${NC}"
now1=$(date +'%H:%M:%S')
if [ $num -ge "1037" ]; then
    text="$CYAN[$now1]${ORG} Creating ${part:2:-3} ${cat:2:-3} signal ${num}...${NC}                  "
else
    text="$CYAN[$now1]${ORG} Creating ${part:2:-3} ${cat:2:-3} background ${num}...${NC}                "
fi
echo -ne "${text:0:88}${ORG}│${BLU}│"
echo -e "\n${BLU}│${ORG}└─────────────────────────────────────────────────────────────┘${BLU}│${NC}"

# Call python3
echo -e "python3 VGammaMeson_cat.py $cat $part $num $year\n" >> $LOGFILE
text="${BLU}│${NC}  python3 VGammaMeson_cat.py $cat $part $num $year                 "
echo -e "${text:0:81}${BLU}│${NC}"

python3 VGammaMeson_cat.py $cat $part $num $year >> $LOGFILE

location="$(grep -m 1 --color=auto 'outputFile' VGammaMeson_cat.py)"
echo -e "${BLU}│${NC}  Saved at \"${location:22:13}/2018/\"                               ${BLU}│"

now2=$(date +'%H:%M:%S')
dif=$(( $(date -d "$now2" "+%s") - $(date -d "$now1" "+%s") ))
text="${BLU}│${GRN}│$CYAN[$now2]${GRN} Done ✓ ($(($dif / 60))m $(($dif % 60))s)${NC}                                      "
echo -ne "${BLU}│${GRN}┌─────────────────────────────────────────────────────────────┐${BLU}│\n${NC}"
echo -ne "${text:0:110}${GRN}│${BLU}│"
echo -ne "\n${BLU}│${GRN}└─────────────────────────────────────────────────────────────┘${BLU}│${NC}"
echo -e "${BLU}\n└───────────────────────────────────────────────────────────────┘${NC}"
