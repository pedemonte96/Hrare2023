#!/bin/bash

channel=$1
testSet=$2
modelName=$3
modelOptions=$4

rootFileName="outfile_${channel}_${modelName}_${testSet}.root"
outFileName="/data/submit/pdmonte/TMVA_models/rmsFiles/rms_${channel}_${modelName}_${testSet}.out"

root -l -q -b "TMVA_GF_regression_auto.C(\"${rootFileName}\", \"${channel}\", ${testSet}, \"${modelName}\", \"${modelOptions}\")" > ${outFileName}

sed -i '/: dataset/!d' ${outFileName}
numLines=$(wc -l < $outFileName)
if [[ "$numLines" -eq 2 ]]; then
    echo -e "No problem in ${outFileName}. Removing /data/submit/pdmonte/TMVA_models/${rootFileName} and /data/submit/pdmonte/TMVA_models/weights/TMVARegression_${modelName}_${testSet}.weights.xml."
    rm "/data/submit/pdmonte/TMVA_models/${rootFileName}"
    rm "/data/submit/pdmonte/TMVA_models/weights/TMVARegression_${modelName}_${testSet}.weights.xml"
else
    echo -e "PROBLEM in ${outFileName}!!!"
fi