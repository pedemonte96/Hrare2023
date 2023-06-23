#!/bin/bash

year="2018"
cat="isGFtag"

#Signal------------------------------------------------

#Signal Omega
#bash createonefile.sh $cat isOmegaCat 1038 $year
#Signal Phi3
#bash createonefile.sh $cat isPhi3Cat 1039 $year
#Signal D0StarRho
#bash createonefile.sh $cat isD0StarRhoCat 1040 $year
#Signal D0Star
#bash createonefile.sh $cat isD0StarCat 1041 $year

#Background--------------------------------------------
#for part in "isOmegaCat" "isD0StarCat" "isPhi3Cat"
for part in "isPhi3Cat"
do
for num in "12" "13" "14"
do
	sleep 0.00001
	bash createonefile.sh $cat $part $num $year

done
done
