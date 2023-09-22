#!/bin/bash

filtering=0

if [[ $# == 0 || $# -gt 2 ]]; then
    echo -e "Only 1 parameter (t/f), and if first is t, then second (optional) parameter is the number of variables."
    exit 1
else
    if [[ ${1,,} == "f" || ${1,,} == "false" ]]; then
        directory="/data/submit/pdmonte/TMVA_models/finalEvalFilesPhiOptions"
        outputFile="eval_all_phi_opts.out"
    elif [[ ${1,,} == "t" || ${1,,} == "true" ]]; then
        directory="/data/submit/pdmonte/TMVA_models/evalFiles"
        if [[ $# == 1 ]]; then
            outputFile="/data/submit/pdmonte/TMVA_models/finalEvalFilesPhiOptions/eval_run3.out" 
        elif [[ $2 =~ ^[0-9]+$ ]]; then
            outputFile="/data/submit/pdmonte/TMVA_models/finalEvalFilesPhiOptions/eval_run${2}.out"
            filtering=1
        else
            echo -e "Second parameter is an integer (number of variables)."
            exit 1
        fi
    else
        echo -e "First parameter t (output at /data/submit/pdmonte/TMVA_models/finalEvalFilesPhiOptions/) or f (output at eval_all_phi.out)."
        exit 1
    fi
fi

echo $directory
echo $outputFile

# Clear the output file if it already exists
> "$outputFile"

IFS="_"

# Loop through all files in the directory
for file in "$directory"/*; do
    # Check if the item is a file (not a directory or a symbolic link)
    if [ -f "$file" ]; then
        if [[ $filtering == 1 ]]; then
            first_word=$(cat "$file" | awk '{print $1}') #first word
            read -ra my_array <<< "$first_word"
            numVars=$(( ${#my_array[@]} - 3 ))
            if [[ $numVars == $2 ]]; then
                echo "$(cat "$file")" >> "$outputFile"
                #rm "$file"
            fi
        else
            echo "$(cat "$file")" >> "$outputFile"
        fi
    fi
done