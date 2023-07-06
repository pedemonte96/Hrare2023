#!/bin/bash

cardDIR="WS_JUL06"
resultDir="WS_JUL06"

cat="GFcat"
meson="D0Star"

for meson in "D0Star" "Phi3"
do

resultFile="results_${meson}.txt"
inputFileSIG="$cardDIR/Signal_${meson}_${cat}_2018_workspace.root"
inputFileBKG="$cardDIR/Bkg_${meson}_${cat}_2018_workspace.root"
outWorkspace="$cardDIR/workspace_STAT_${meson}_${cat}_2018.root"
dataCardName="$cardDIR/datacard_STAT_${meson}_${cat}_2018.txt"

echo -e "\033[0;33mCreating DataCard $dataCardName...\033[0m"
python createDatacards.py --whichMeson=${meson}Cat --whichCat=$cat --inputFileSIG=$inputFileSIG --inputFileBKG=$inputFileBKG --output=$outWorkspace --dataCardName=$dataCardName
echo -e "\033[0;33mDataCard created: $dataCardName\033[0m"

echo "--------------------------------------------------------------------------"

echo -e "\033[0;35mCalling combine AsymptoticLimits to $resultFile...\033[0m"
echo "**** ${meson} ${cat} ****" > $resultFile
combine -M AsymptoticLimits -m 125 -t -1 $cardDIR/datacard_STAT_${meson}_${cat}_2018.txt -n ${meson}${cat} --run expected >> $resultFile
mv higgsCombine*.AsymptoticLimits.mH125.root $resultFile $resultDir
echo -e "\033[0;35mLimits computed from $dataCardName to $resultFile\033[0m"

echo -e "--------------------------------------------------------------------------\n"

done
