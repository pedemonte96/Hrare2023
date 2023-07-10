#!/bin/bash

for file in logfiles/*
do
	if [[ -d $file ]]; then
		for file2 in ${file}/*
		do
			if [[ -f "$file2" ]]; then
				numLines=$(wc -l < $file2)
				if [[ "$numLines" -gt 100 || "$numLines" -lt 30 ]]; then
					echo -e "Removing $file2 with $numLines lines."
					rm $file2
				fi
			fi
		done
	fi
done
