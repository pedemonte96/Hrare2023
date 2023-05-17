#!/bin/bash

CYAN='\033[0;32m'
NC='\033[0m' # No Color

cat=$1
part=$2
num=$3
year=$4

LOGFILE="logfiles/output_${num}_${cat:2:-3}_${part:2:-3}_${year}_$(date '+%Y%m%d_%H%M%S').log"
if [ -f "$LOGFILE" ]; then
	rm $LOGFILE
fi

now1=$(date +'%H:%M:%S')
if [ $num -ge "1037" ]; then
	echo -e "$CYAN[$now1]$NC Creating ${part:2:-3} ${cat:2:-3} signal ${num}..."
else
	echo -e "$CYAN[$now1]$NC Creating ${part:2:-3} ${cat:2:-3} background ${num}..."
fi

#sleep 1
echo -e "python3 VGammaMeson_cat.py $cat $part $num $year\n" >> $LOGFILE
echo -e "python3 VGammaMeson_cat.py $cat $part $num $year"
python3 VGammaMeson_cat.py $cat $part $num $year >> $LOGFILE
now2=$(date +'%H:%M:%S')
dif=$(( $(date -d "$now2" "+%s") - $(date -d "$now1" "+%s") ))
echo -e "$CYAN[$now2]$NC Done ($(($dif / 60))m $(($dif % 60))s)"
