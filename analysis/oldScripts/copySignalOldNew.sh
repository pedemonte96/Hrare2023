#!/bin/bash

source_dir="/work/submit/mariadlf/Hrare/D02/2018/ggh-hphipipipi0gamma-powheg/NANOAOD_03_test5/"
destination_dir_OLD="/data/submit/pdmonte/signal_D02/ggh-hphipipipi0gamma-powheg/OLD"
destination_dir_NEW="/data/submit/pdmonte/signal_D02/ggh-hphipipipi0gamma-powheg/NEW"
cutoff_date="2023-08-01"  # Change this to the desired date

echo "Copying new..."
find "$source_dir" -type f -newermt "$cutoff_date" -exec cp -t "$destination_dir_NEW" {} +
ls "$destination_dir_NEW" | wc -l
echo "Copying old..."
find "$source_dir" -type f ! -newermt "$cutoff_date" -exec cp -t "$destination_dir_OLD" {} +
ls "$destination_dir_OLD" | wc -l
