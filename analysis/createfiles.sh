#!/bin/bash

CYAN='\033[0;32m'
NC='\033[0m' # No Color

year="2018"
cat="isGFtag"

#Background
for part in "isD0StarCat"
do
for num in "10" "11" "12" "13" "14"
do
	sleep 1	
	#bash createonefile.sh $cat $part $num $year

done
done

#Signal D0Star
#bash createonefile.sh $cat isD0StarCat 1039 $year

#Signal Omega
bash createonefile.sh $cat isOmegaCat 1040 $year

