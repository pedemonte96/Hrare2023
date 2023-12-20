#!/bin/bash

for meson in "D0Star" "D0StarRho"; do
    echo -e "${meson} channel:"
    outputFile="/data/submit/pdmonte/TMVA_models/finalEvalFiles${meson}/eval_run0.out"
    inputFiles="/data/submit/pdmonte/TMVA_models/evalFiles"
    echo $inputFiles
    echo $outputFile
    > "$outputFile"
    for file in "$inputFiles"/*"${meson,,}_ggh.out"; do
        if [ -f "$file" ]; then
            echo "$(cat "$file")" >> "$outputFile"
        fi
    done
    ls ${inputFiles}/*${meson,,}_ggh* | wc
    cat $outputFile | wc
    outputFile="eval${meson}.out"
    inputFiles="/data/submit/pdmonte/TMVA_models/finalEvalFiles${meson}"
    echo $inputFiles
    echo $outputFile
    > "$outputFile"
    for file in "$inputFiles"/*; do
        if [ -f "$file" ]; then
            echo "$(cat "$file")" >> "$outputFile"
        fi
    done
    echo -e "---------------------------------------------------------------------------------------------"
done
