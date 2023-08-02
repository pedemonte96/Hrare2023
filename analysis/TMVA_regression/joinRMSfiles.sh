#!/bin/bash

# Directory containing the files
if true; then
    directory="/data/submit/pdmonte/TMVA_models/finalEvalFiles"
    outputFile="eval_all.out"
else
    directory="/data/submit/pdmonte/TMVA_models/evalFiles"
    outputFile="/data/submit/pdmonte/TMVA_models/finalEvalFiles/eval_tmp.txt"
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
