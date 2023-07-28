#!/bin/bash

indexCommands=0

while true; do
    queueLength=$(squeue -u pdmonte | wc -l)
    #echo -e "[$(date +'%T')] Queue: ${queueLength}"
    if true; then
    if [ "$queueLength" -lt 900 ]; then
        python slurm.py -i commands_evaluate.txt --minIndex $indexCommands --maxIndex $((indexCommands + 50))
        ((indexCommands += 50))
        continue
    fi
    if [ "$indexCommands" -gt 5995 ]; then
        break
    fi
    fi
    sleep 15
done

echo "All jobs queued. Exiting the loop."
