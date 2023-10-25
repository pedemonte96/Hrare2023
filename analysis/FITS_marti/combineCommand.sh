#!/bin/bash

cardDIR="WS_OCT25"
resultDir="WS_OCT25"

cat="GFcat"
meson="Phi3"
#meson="Omega"
year=2018
regModel=""

for meson in "Phi3" "Omega" "D0Star"; do
#for meson in "Phi3"; do
    for is2Dfit in "True" "False"; do
        input_file="models_${meson}.txt"
        if [ "$is2Dfit" == "True" ]; then
            label2D="_2D"
        else
            label2D=""
        fi
        # Loop through each line in the input file
        while IFS="" read -r readLine  || [ -n "$readLine" ]; do
            if [ "${readLine:0:1}" != "#" ]; then
                if [ "$readLine" == "RECO" ]; then
                    regModel=""
                else
                    regModel="_$readLine"
                fi

                echo $regModel

                resultFile="results_${meson}_${cat}_${year}${regModel}${label2D}.txt"
                inputFileSIG="$cardDIR/Sgn_${meson}_${cat}_${year}${regModel}${label2D}_workspace.root"
                inputFileBKG="$cardDIR/Bkg_${meson}_${cat}_${year}${regModel}${label2D}_workspace.root"
                outWorkspace="$cardDIR/workspace_STAT_${meson}_${cat}_${year}${regModel}${label2D}.root"
                dataCardName="$cardDIR/datacard_STAT_${meson}_${cat}_${year}${regModel}${label2D}.txt"

                echo -e "\033[0;33mCreating DataCard $dataCardName...\033[0m"
                python createDatacards.py --whichMeson=${meson}Cat --whichCat=$cat --inputFileSIG=$inputFileSIG --inputFileBKG=$inputFileBKG --output=$outWorkspace --dataCardName=$dataCardName --is2Dfit=$is2Dfit
                echo -e "\033[0;33mDataCard created: $dataCardName\033[0m"

                echo "--------------------------------------------------------------------------"

                echo -e "\033[0;35mCalling combine AsymptoticLimits to $resultFile...\033[0m"
                echo "**** ${meson} ${cat} ${regModel} ****" > $resultFile
                combine -M AsymptoticLimits -m 125 -t -1 $dataCardName -n ${meson}${cat} --run expected >> $resultFile
                mv higgsCombine*.AsymptoticLimits.mH125.root $resultFile $resultDir
                echo -e "\033[0;35mLimits computed from $dataCardName to $resultFile\033[0m"

                echo -e "--------------------------------------------------------------------------\n"
            fi
        done < "$input_file"
    done
done