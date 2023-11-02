#!/bin/bash

eval_dir="/data/submit/pdmonte/TMVA_models/evalFiles/"

for file in "$eval_dir"eval_BDTG_df15_dl3684_v0_v1_opt*_d0starrho.out; do
    # Extract the xxxxx part from the file name
    number="${file##*_opt}"
    number="${number%%_d0starrho.out}"

    echo "$file"
    echo -e "$number"
    if [ -e "$file" ]; then
        # Delete the corresponding line in "commands.txt"
        sed -i "/^o${number}_v01/d" "commands.txt"
        echo "Deleted line $number in commands.txt"
    fi

done
