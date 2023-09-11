#!/bin/bash

cardDIR="WS_AUG24"
resultDir="WS_AUG24"

cat="GFcat"
meson="Phi3"
year=2018
regModel=""

for meson in "Phi3"
do

    resultFile="results_${meson}_${cat}_${year}${regModel}.txt"
    inputFileSIG="$cardDIR/Sgn_${meson}_${cat}_${year}${regModel}_workspace.root"
    inputFileBKG="$cardDIR/Bkg_${meson}_${cat}_${year}${regModel}_workspace.root"
    outWorkspace="$cardDIR/workspace_STAT_${meson}_${cat}_${year}${regModel}.root"
    dataCardName="$cardDIR/datacard_STAT_${meson}_${cat}_${year}${regModel}.txt"

    echo -e "\033[0;33mCreating DataCard $dataCardName...\033[0m"
    python createDatacards.py --whichMeson=${meson}Cat --whichCat=$cat --inputFileSIG=$inputFileSIG --inputFileBKG=$inputFileBKG --output=$outWorkspace --dataCardName=$dataCardName
    echo -e "\033[0;33mDataCard created: $dataCardName\033[0m"

    echo "--------------------------------------------------------------------------"

    echo -e "\033[0;35mCalling combine AsymptoticLimits to $resultFile...\033[0m"
    echo "**** ${meson} ${cat} ${regModel} ****" > $resultFile
    combine -M AsymptoticLimits -m 125 -t -1 $dataCardName -n ${meson}${cat} --run expected >> $resultFile
    mv higgsCombine*.AsymptoticLimits.mH125.root $resultFile $resultDir
    echo -e "\033[0;35mLimits computed from $dataCardName to $resultFile\033[0m"

    echo -e "--------------------------------------------------------------------------\n"

done
