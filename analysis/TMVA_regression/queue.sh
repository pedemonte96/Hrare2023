#!/bin/bash

outFile="/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/TMVA_regression/timeJobs.txt"

#> "$outFile"

while true; do
    doneJobs=$(( $(ls /data/submit/pdmonte/TMVA_models/evalFiles/*.out | wc -l) ))
    queueLength=$(( $(squeue -u pdmonte | wc -l) - 1 ))
    #echo -e "[$(date +'%Y/%m/%d-%T')] Done: ${doneJobs}\tQueue: ${queueLength}"
    echo -e "$(date +'%Y/%m/%d-%T')\t${doneJobs}\t${queueLength}" >> "$outFile"
    sleep 9
	if [ "$queueLength" -lt 5 ]; then
        break
    fi
done
