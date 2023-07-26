#!/bin/bash

# Directory containing the files
directory="/data/submit/pdmonte/TMVA_models/rmsFiles"

# Output file to store the first lines
outputFile="allRMS.out"

# Loop through all files in the directory
for file in "$directory"/*; do
    # Check if the item is a file (not a directory or a symbolic link)
    if [ -f "$file" ]; then
        # Get the first line of the file and append it to the output file
        head -n 1 "$file" >> "$outputFile"
        rm "$file"
    fi
done
