#!/bin/bash

resultDir="WS_NOV16"

cat="GFcat"
meson="Phi3"
#meson="Omega"
year=2018

for meson in "Phi3" "Omega" "D0Star" "D0StarRho"; do
    outputFile="limits_${meson}.out"
    > "$outputFile"
    # Loop through all files in the directory
    for file in $resultDir/results_${meson}_GFcat_2018*; do
        # Check if the item is a file (not a directory or a symbolic link)
        if [ -f "$file" ]; then
            # Get the first line of the file and append it to the output file
            #echo "$(cat "$file")" >> "$outputFile"
            echo $file
            last_word=$(head -n 9 $file | tail -n 1 | sed 's/.* //')
            modelName=$(echo $file | sed "s/$resultDir\/results_${meson}_GFcat_2018//" | sed "s/.txt//" | sed "s/_//")
            if [ "$modelName" == "" ]; then
                modelName="RECO"
            fi
            echo -e "$modelName\t$last_word" >> "$outputFile"
        fi
    done
done