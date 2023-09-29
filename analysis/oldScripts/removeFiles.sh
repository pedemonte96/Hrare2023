#!/bin/bash

# Store the input file name
input_file="files.txt"

# Loop through each line in the input file
while IFS="" read -r file_path; do
    # Check if the file exists before attempting to remove it
    if [ -e "$file_path" ]; then
        rm "$file_path"
        echo "Removed file: $file_path"
    else
        echo "File not found: $file_path"
    fi
done < "$input_file"
