#!/bin/bash

if true; then
    #directory="/data/submit/pdmonte/TMVA_models/finalEvalFilesPhi"
    #outputFile="eval_all_phi.out"
    #directory="/data/submit/pdmonte/TMVA_models/finalEvalFilesD0Star"
    #outputFile="eval_all_d0star.out"
    #directory="/data/submit/pdmonte/TMVA_models/finalEvalFilesOmega"
    #outputFile="eval_all_omega.out"
    directory="/data/submit/pdmonte/TMVA_models/finalEvalFilesPhi"
    outputFile="eval_all_phi_loss.out"
else
    directory="/data/submit/pdmonte/TMVA_models/evalFiles"
    #outputFile="/data/submit/pdmonte/TMVA_models/finalEvalFilesPhi/eval_tmp.txt"
    #outputFile="/data/submit/pdmonte/TMVA_models/finalEvalFilesD0Star/eval_tmp.txt"
    #outputFile="/data/submit/pdmonte/TMVA_models/finalEvalFilesOmega/eval_tmp.txt"
    outputFile="/data/submit/pdmonte/TMVA_models/finalEvalFilesPhi/eval_all.out"
fi

# Clear the output file if it already exists
> "$outputFile"

# Loop through all files in the directory
for file in "$directory"/*; do
    # Check if the item is a file (not a directory or a symbolic link)
    if [ -f "$file" ]; then
        # Get the first line of the file and append it to the output file
        echo "$(cat "$file")" >> "$outputFile"
    fi
done
