#!/bin/bash

eval_dir="/data/submit/pdmonte/TMVA_models/evalFiles/"
output_file="output_numbers.txt"

for file in "$eval_dir"eval_BDTG_df*_dl*_v0_v1_opt*_*.out; do
    # Extract the xxxxx part from the file name
    number=$(echo "$file" | awk -F'_opt' '{print $2}' | awk -F'_.*' '{print $1}')

    echo "$file"
    echo -e "$number"
    if [ -e "$file" ]; then
        # Delete the corresponding line in "commands.txt"
        sed -i "/^o${number}_v01/d" "commands.txt"
        #echo "Deleted line $number in commands.txt"
        #echo "$number" >> "$output_file"
    fi

done
