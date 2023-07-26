#!/bin/bash

# Directory containing the files
directory="/data/submit/pdmonte/TMVA_models/evalFiles"

# Output file to store the first lines
outputFile="evaluationAllVars.out"

# Clear the output file if it already exists
> "$outputFile"

# Loop through all files in the directory
for file in "$directory"/*; do
    # Check if the item is a file (not a directory or a symbolic link)
    if [ -f "$file" ]; then
        # Get the first line of the file and append it to the output file
        echo "$(cat "$file")" >> "$outputFile"
        # rm "$file"
    fi
done
