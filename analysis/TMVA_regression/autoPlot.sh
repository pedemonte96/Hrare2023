#!/bin/bash

while true; do
    queueLength=$(squeue -u pdmonte | wc -l)
    python timeJobsPlot.py -n 2400
    if [ "$queueLength" -lt 5 ]; then
        break
    fi
    sleep 29
done

echo "All jobs queued. Exiting the loop."
