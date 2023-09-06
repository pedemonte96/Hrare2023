#!/bin/bash

outFile="/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/TMVA_regression/timeJobs.txt"

> "$outFile"

while true; do
    doneJobs=$(( $(ls /data/submit/pdmonte/TMVA_models/evalFiles/*.out | wc -l) ))
    queueLength=$(squeue -u pdmonte | wc -l)
    #echo -e "[$(date +'%T')] Done: ${doneJobs}\tQueue: ${queueLength}"
    echo -e "$(date +'%T')\t${doneJobs}\t${queueLength}" >> "$outFile"
    sleep 10
	if [ "$queueLength" -lt 50 ]; then
        break
    fi
done
