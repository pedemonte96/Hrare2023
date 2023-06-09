#!/bin/bash

sed -i '/\*Br/!d' $1
sed -i 's/[^:]*://' $1
sed -i 's/:.*//' $1
