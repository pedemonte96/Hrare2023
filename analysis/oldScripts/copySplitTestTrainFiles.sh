#!/bin/bash

#for dir in "ggh-hD0StarKmPiPPi0gamma-powheg" "ggh-homegagamma-powheg" "ggh-hphipipipi0gamma-powheg"
for dir in "ggh-hD0StarKmPiPPi0gamma-powheg"
#for dir in "ggh-hD0Stargamma-powheg"
do
    source_dir="/work/submit/mariadlf/Hrare/D02/2018/${dir}/NANOAOD_03_test6"
    destination_dir="/data/submit/pdmonte/signalSplit/${dir}"
    if [[ ! -d "${destination_dir}" ]]; then
        mkdir "${destination_dir}"
    fi
    if [[ ! -d "${destination_dir}/sample0" ]]; then
        mkdir "${destination_dir}/sample0"
    fi
    if [[ ! -d "${destination_dir}/sample1" ]]; then
        mkdir "${destination_dir}/sample1"
    fi
    if [[ ! -d "${destination_dir}/sample2" ]]; then
        mkdir "${destination_dir}/sample2"
    fi
    echo "Copying $dir..."
    i=0
    for file in "$source_dir"/*; do
        if [[ $((i % 3)) == 0 ]]; then
            cp "$file" "${destination_dir}/sample0"
        elif [[ $((i % 3)) == 1 ]]; then
            cp "$file" "${destination_dir}/sample1"
        elif [[ $((i % 3)) == 2 ]]; then
            cp "$file" "${destination_dir}/sample2"
        fi
        i=$((i + 1))
    done
done