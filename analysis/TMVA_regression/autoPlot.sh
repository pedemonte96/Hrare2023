#!/bin/bash

while true; do
    queueLength=$(squeue -u pdmonte | wc -l)
    python timeJobsPlot.py -n 6289
    if [ "$queueLength" -lt 10 ]; then
        break
    fi
    sleep 30
done

echo "All jobs queued. Exiting the loop."
