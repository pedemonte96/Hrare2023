#!/bin/bash

# Output file to store the first lines
outputFile="/home/submit/pdmonte/public_html/slurmMonitoring.out"

while true; do
    > "$outputFile"
    totalQueue=$(squeue)
    pdmonteQueue=$(squeue -u pdmonte)
    totalQueueNumber=$(( $(squeue | wc -l) - 1 ))
    totalQueueNumberR=$(( $(squeue -t R | wc -l) - 1 ))
    totalQueueNumberPD=$(( $(squeue -t PD | wc -l) - 1 ))
    pdmonteQueueNumber=$(( $(squeue -u pdmonte | wc -l) - 1 ))
    pdmonteQueueNumberR=$(( $(squeue -u pdmonte -t R | wc -l) - 1 ))
    pdmonteQueueNumberPD=$(( $(squeue -u pdmonte -t PD | wc -l) - 1 ))
    numErrors=$(find /data/submit/pdmonte/TMVA_models/logsVars/*.err -maxdepth 1 -type f -size +0 | wc -l)
    echo -e "[$(date +'%d-%m-%Y') | $(date +'%T')]" >> "$outputFile"
    echo -e "Total number of jobs: ${totalQueueNumber} (R:${totalQueueNumberR}, PD:${totalQueueNumberPD})" >> "$outputFile"
    echo -e "Total number of jobs pdmonte: ${pdmonteQueueNumber} (R:${pdmonteQueueNumberR}, PD:${pdmonteQueueNumberPD})" >> "$outputFile"
    echo -e "Errors: ${numErrors}" >> "$outputFile"
    echo -e "--------------------------------------------------------------------------------------" >> "$outputFile"
    echo -e "Jobs pdmonte:\n${pdmonteQueue}" >> "$outputFile"
    echo -e "--------------------------------------------------------------------------------------" >> "$outputFile"
    echo -e "Jobs:\n${totalQueue}" >> "$outputFile"
    sleep 120
done
