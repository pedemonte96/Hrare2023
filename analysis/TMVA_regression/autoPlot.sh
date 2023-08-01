#!/bin/bash

while true; do
    queueLength=$(squeue -u pdmonte | wc -l)
    python timeJobsPlot.py -n 6160
    if [ "$queueLength" -lt 50 ]; then
        break
    fi
    sleep 30
done

echo "All jobs queued. Exiting the loop."
