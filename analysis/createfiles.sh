#!/bin/bash

year="2018"
cat="isGFtag"

#Signal

#Signal Omega
#bash createonefile.sh $cat isOmegaCat 1037 $year

#Signal D0Star
bash createonefile.sh $cat isD0StarCat 1039 $year

#Signal Phi3
#bash createonefile.sh $cat isPhi3Cat 1040 $year


#Background
#for part in "isOmegaCat" "isD0StarCat" "isPhi3Cat"
for part in "isD0StarCat"
do
for num in "10" "11" "12" "13" "14"
do
	sleep 0.00001
#	bash createonefile.sh $cat $part $num $year

done
done
