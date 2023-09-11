#!/bin/bash

# Store the input file name
input_file="jobsIDs.txt"

# Loop through each line in the input file
while IFS="" read -r jobID; do
    # Check if the file exists before attempting to remove it
    scancel "$jobID"
done < "$input_file"
