#!/bin/bash
RED='\033[1;31m'
NC='\033[0m' # No Color

year="2018"
cat="isGFtag"

if [[ $# == 0 ]]; then
	#Signal------------------------------------------------
	#Signal Omega
	#bash runVGM.sh $cat isOmegaCat 1038 $year
	#Signal Phi3
	#bash runVGM.sh $cat isPhi3Cat 1039 $year
	#Signal D0StarRho
	#bash runVGM.sh $cat isD0StarRhoCat 1040 $year
	#Signal D0Star
	#bash runVGM.sh $cat isD0StarCat 1041 $year

	#Background--------------------------------------------
	for part in "isPhi3Cat"
	do
		for num in "10" "11" "12" "13" "14"
		do
			sleep 0.00001
		#	bash runVGM.sh $cat $part $num $year
		done
	done
else
	#Select meson
	if [[ ${1,,} == "omega" ]]; then
		mesonCat="isOmegaCat"
		numSignal=1038
	elif [[ ${1,,} == "phi" || ${1,,} == "phi3" ]]; then
		mesonCat="isPhi3Cat"
		numSignal=1039
	elif [[ ${1,,} == "d0starrho" ]]; then
		mesonCat="isD0StarRhoCat"
		numSignal=1040
	elif [[ ${1,,} == "d0star" ]]; then
		mesonCat="isD0StarCat"
		numSignal=1041
	else
		echo -e "${RED}ERROR: No matching meson category.${NC}"
		return 1
	fi
	if [[ $# == 1 ]]; then #run all signal and background
		bash runVGM.sh $cat $mesonCat $numSignal $year
		bash runVGM.sh $cat $mesonCat 10 $year
		bash runVGM.sh $cat $mesonCat 11 $year
		bash runVGM.sh $cat $mesonCat 12 $year
		bash runVGM.sh $cat $mesonCat 13 $year
		bash runVGM.sh $cat $mesonCat 14 $year
	elif [[ $# == 2 ]]; then #choose signal, background, or combination 1/2/3
		if [[ ${2,,} == "s" || ${2,,} == "sgn" || ${2,,} == "sig" || ${2,,} == "signal" ]]; then
			bash runVGM.sh $cat $mesonCat $numSignal $year
		elif [[ ${2,,} == "b" || ${2,,} == "bkg" || ${2,,} == "background" ]]; then
			bash runVGM.sh $cat $mesonCat 10 $year
			bash runVGM.sh $cat $mesonCat 11 $year
			bash runVGM.sh $cat $mesonCat 12 $year
			bash runVGM.sh $cat $mesonCat 13 $year
			bash runVGM.sh $cat $mesonCat 14 $year
		elif [[ ${2,,} == 1 ]]; then
			bash runVGM.sh $cat $mesonCat $numSignal $year
			bash runVGM.sh $cat $mesonCat 10 $year
			bash runVGM.sh $cat $mesonCat 13 $year
		elif [[ ${2,,} == 2 ]]; then
			bash runVGM.sh $cat $mesonCat 11 $year
			bash runVGM.sh $cat $mesonCat 14 $year
		elif [[ ${2,,} == 3 ]]; then
			bash runVGM.sh $cat $mesonCat 12 $year
		else #2nd argument invalid
			echo -e "${RED}ERROR: Second argument invalid.${NC}"
			return 1
		fi
	else #3 or more arguments!
		echo -e "${RED}ERROR: Too many arguments.${NC}"
		return 1
	fi
fi