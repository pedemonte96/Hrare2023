#!/bin/bash

while true; do
    queueLength=$(squeue -u pdmonte | wc -l)
    python timeJobsPlot.py -n 7200
    if [ "$queueLength" -lt 10 ]; then
        break
    fi
    sleep 29
done

echo "All jobs queued. Exiting the loop."
