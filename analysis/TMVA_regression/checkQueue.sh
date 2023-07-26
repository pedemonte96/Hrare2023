#!/bin/bash

indexCommands=900

while true; do
    queueLength=$(squeue -u pdmonte | wc -l)
    echo -e "[$(date +'%T')] Queue: ${queueLength}"
    if false; then
    if [ "$queueLength" -lt 1000 ]; then
        python slurm.py -i commands_evaluate.txt --minIndex $indexCommands --maxIndex $((indexCommands + 100))
        ((indexCommands += 100))
        queueLength=$(squeue -u pdmonte | wc -l)
        echo -e "Queue: ${queueLength}"
    fi
    if [ "$indexCommands" -gt 3400 ]; then
        break
    fi
    fi
    sleep 5
done

echo "All jobs queued. Exiting the loop."
