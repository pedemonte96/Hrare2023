# BDT Meson's pT Regression
**Requirements:**
- Python 3.11
- ROOT 6.28

## 1. Train different models with different variables and hyperparameters
The main file to train the models is `TMVA_GF_regression.C`. This function require the following arguments:

- `nameModel`: Name of the model (e.g. `BDTG_df13_dl3620_v0_v1_opt70035`).
- `channel`: Channel to sudy (e.g. `omega`, `phi`, `d0starrho`, `d0star`).
- `testSet`: Set used for testing (e.g. 0, 1 or 2).
- `variables`: List of variables of the form `var0_input_pred` to use (e.g. `{0, 1}`).
- `codeDF`: Code referring to which dimensionful variables to use (e.g. 13 for phi and omega, 7 for d0star, 15 for d0starrho).
- `codeDL`: Code referring to which dimensionless variables to use (e.g. 3620 for phi and omega, 3684 for d0star and d0starrho).
- `options`: String of the hypermarameters of the model(e.g. `"!V:VarTransform=G,N,P:NTrees=1000:BoostType=Grad:Shrinkage=0.07:MaxDepth=5:SeparationType=RegressionVariance:nCuts=43:UseRandomisedTrees=T:UseNvars=74:UseBaggedBoost=T:BaggedSampleFraction=0.959:PruneMethod=NoPruning:PruneStrength=56:PruningValFraction=0.084"`).

The sets used for training and testing have to be split beforehand and pass the `VGammaMeson_cat.py` script seperately. They are of the form
```bash
/data/submit/pdmonte/outputs/NOV05/2018/outname_mc1038_GFcat_OmegaCat_2018_sample%d.root
```
where `%d` is 0, 1 or 2. To do so, I splitted the ROOT files of each meson category into 3 different subfolders in 
```bash
(myenv) [13:47:45] pdmonte@submit01 ggh-homegagamma-powheg$ pwd
/data/submit/pdmonte/signalSplit/ggh-homegagamma-powheg
(myenv) [13:47:48] pdmonte@submit01 ggh-homegagamma-powheg$ ll
total 12K
drwxrwxr-x 2 pdmonte pdmonte 4.0K  5. Sep 11:27 sample0
drwxrwxr-x 2 pdmonte pdmonte 4.0K  5. Sep 11:27 sample1
drwxrwxr-x 2 pdmonte pdmonte 4.0K  5. Sep 11:27 sample2
(myenv) [13:47:49] pdmonte@submit01 ggh-homegagamma-powheg$ 
```
and then run the `VGammaMeson_cat.py` seperately for each of these subfolders. This way I ensured proper splitting between sets.

One should train the model three times to have cross-validation, one for each different sample, to obtain three different weight files, to apply to each of the testing samples. Ideally in the future one would need to train the model with a big training set, and have only one weight file to apply to a different (unseen) sample.

Training a model will produce a ROOT file in
```bash
/data/submit/pdmonte/TMVA_models/rootVars/
```
and a weight file in
```bash
/data/submit/pdmonte/TMVA_models/weightsOptsFinal/
```

## 2. Evaluate the model
To evaluate each model, one can use the script `computeErrors.py`, which requires parameters:
- `--modelName`: Name of the model (e.g. `BDTG_df13_dl3620_v0_v1_opt70035`).
- `--channel`: Channel to sudy (e.g. `omega`, `phi`, `d0starrho`, `d0star`).
- `--prodCat`: Production category (e.g. `ggh`, `vbf`, ... . So far only `ggh` is implemented).

This script will produce a file in 
```bash
/data/submit/pdmonte/TMVA_models/evalFiles/
```
with the output of the evaluation, containing the root squared mean error and the value of the shaping function.

Before evaluating a model, the weight file needs to be present, i.e., it has to be trained for the three different samples.

## 3. Training and evaluating many models
To automatize the training and testing of thousands of models, one can use the `slurm.py` script. This script requires the following parameters:
- `--input`: Input file with commands to be executed as slurm jobs.
- `--minIndex`: (optional) First line in the input file of the commands to execute. If not provided, the first command is the one in the first line of the file.
- `--maxIndex`: (optional) Last line in the input file of the commands to execute. If not provided, the last ocmmand is the one in the last line of the file.

A real example of the usage of this function would be the following:
```bash
python slurm.py -i commands.txt
```
This will excecute all the commands in the `commands.txt` file, one command per line (or chained commands), with the format
```
<jobName>:::<command1>
<jobName>:::<command1> && <command2>
```
A real example of such a file would be:
```bash
o70035_v01_ggh:::root -l -q -b 'TMVA_GF_regression.C("BDTG_df13_dl3620_v0_v1_opt70035", "phi", "ggh", 0, {0, 1}, 13, 3620, "!V:VarTransform=G,N,P:NTrees=1000:BoostType=Grad:Shrinkage=0.07:MaxDepth=5:SeparationType=RegressionVariance:nCuts=43:UseRandomisedTrees=T:UseNvars=74:UseBaggedBoost=T:BaggedSampleFraction=0.959:PruneMethod=NoPruning:PruneStrength=56:PruningValFraction=0.084")' && root -l -q -b 'TMVA_GF_regression.C("BDTG_df13_dl3620_v0_v1_opt70035", "phi", "ggh", 1, {0, 1}, 13, 3620, "!V:VarTransform=G,N,P:NTrees=1000:BoostType=Grad:Shrinkage=0.07:MaxDepth=5:SeparationType=RegressionVariance:nCuts=43:UseRandomisedTrees=T:UseNvars=74:UseBaggedBoost=T:BaggedSampleFraction=0.959:PruneMethod=NoPruning:PruneStrength=56:PruningValFraction=0.084")' && root -l -q -b 'TMVA_GF_regression.C("BDTG_df13_dl3620_v0_v1_opt70035", "phi", "ggh", 2, {0, 1}, 13, 3620, "!V:VarTransform=G,N,P:NTrees=1000:BoostType=Grad:Shrinkage=0.07:MaxDepth=5:SeparationType=RegressionVariance:nCuts=43:UseRandomisedTrees=T:UseNvars=74:UseBaggedBoost=T:BaggedSampleFraction=0.959:PruneMethod=NoPruning:PruneStrength=56:PruningValFraction=0.084")' && python computeErrors.py -m BDTG_df13_dl3620_v0_v1_opt70035 -c phi -p ggh
o72810_v01_ggh:::root -l -q -b 'TMVA_GF_regression.C("BDTG_df13_dl3620_v0_v1_opt72810", "omega", "ggh", 0, {0, 1}, 13, 3620, "!V:VarTransform=G,P,D:NTrees=1300:BoostType=Grad:Shrinkage=0.041:MaxDepth=5:SeparationType=RegressionVariance:nCuts=37:UseRandomisedTrees=T:UseNvars=26:UseBaggedBoost=T:BaggedSampleFraction=0.758:PruneMethod=NoPruning:PruneStrength=20:PruningValFraction=1.78")' && root -l -q -b 'TMVA_GF_regression.C("BDTG_df13_dl3620_v0_v1_opt72810", "omega", "ggh", 1, {0, 1}, 13, 3620, "!V:VarTransform=G,P,D:NTrees=1300:BoostType=Grad:Shrinkage=0.041:MaxDepth=5:SeparationType=RegressionVariance:nCuts=37:UseRandomisedTrees=T:UseNvars=26:UseBaggedBoost=T:BaggedSampleFraction=0.758:PruneMethod=NoPruning:PruneStrength=20:PruningValFraction=1.78")' && root -l -q -b 'TMVA_GF_regression.C("BDTG_df13_dl3620_v0_v1_opt72810", "omega", "ggh", 2, {0, 1}, 13, 3620, "!V:VarTransform=G,P,D:NTrees=1300:BoostType=Grad:Shrinkage=0.041:MaxDepth=5:SeparationType=RegressionVariance:nCuts=37:UseRandomisedTrees=T:UseNvars=26:UseBaggedBoost=T:BaggedSampleFraction=0.758:PruneMethod=NoPruning:PruneStrength=20:PruningValFraction=1.78")' && python computeErrors.py -m BDTG_df13_dl3620_v0_v1_opt72810 -c omega -p ggh
o75239_v01_ggh:::root -l -q -b 'TMVA_GF_regression.C("BDTG_df7_dl3684_v0_v1_opt75239", "d0star", "ggh", 0, {0, 1}, 7, 3684, "!V:VarTransform=D,G:NTrees=1400:BoostType=Grad:Shrinkage=0.064:MaxDepth=4:SeparationType=RegressionVariance:nCuts=34:UseRandomisedTrees=F:UseNvars=65:UseBaggedBoost=T:BaggedSampleFraction=1.434:PruneMethod=NoPruning:PruneStrength=26:PruningValFraction=0.474")' && root -l -q -b 'TMVA_GF_regression.C("BDTG_df7_dl3684_v0_v1_opt75239", "d0star", "ggh", 1, {0, 1}, 7, 3684, "!V:VarTransform=D,G:NTrees=1400:BoostType=Grad:Shrinkage=0.064:MaxDepth=4:SeparationType=RegressionVariance:nCuts=34:UseRandomisedTrees=F:UseNvars=65:UseBaggedBoost=T:BaggedSampleFraction=1.434:PruneMethod=NoPruning:PruneStrength=26:PruningValFraction=0.474")' && root -l -q -b 'TMVA_GF_regression.C("BDTG_df7_dl3684_v0_v1_opt75239", "d0star", "ggh", 2, {0, 1}, 7, 3684, "!V:VarTransform=D,G:NTrees=1400:BoostType=Grad:Shrinkage=0.064:MaxDepth=4:SeparationType=RegressionVariance:nCuts=34:UseRandomisedTrees=F:UseNvars=65:UseBaggedBoost=T:BaggedSampleFraction=1.434:PruneMethod=NoPruning:PruneStrength=26:PruningValFraction=0.474")' && python computeErrors.py -m BDTG_df7_dl3684_v0_v1_opt75239 -c d0star -p ggh
o76387_v01_ggh:::root -l -q -b 'TMVA_GF_regression.C("BDTG_df15_dl3684_v0_v1_opt76387", "d0starrho", "ggh", 0, {0, 1}, 15, 3684, "!V:VarTransform=G,N,G:NTrees=2300:BoostType=Grad:Shrinkage=0.054:MaxDepth=9:SeparationType=RegressionVariance:nCuts=37:UseRandomisedTrees=F:UseNvars=66:UseBaggedBoost=F:BaggedSampleFraction=1.167:PruneMethod=NoPruning:PruneStrength=50:PruningValFraction=0.602")' && root -l -q -b 'TMVA_GF_regression.C("BDTG_df15_dl3684_v0_v1_opt76387", "d0starrho", "ggh", 1, {0, 1}, 15, 3684, "!V:VarTransform=G,N,G:NTrees=2300:BoostType=Grad:Shrinkage=0.054:MaxDepth=9:SeparationType=RegressionVariance:nCuts=37:UseRandomisedTrees=F:UseNvars=66:UseBaggedBoost=F:BaggedSampleFraction=1.167:PruneMethod=NoPruning:PruneStrength=50:PruningValFraction=0.602")' && root -l -q -b 'TMVA_GF_regression.C("BDTG_df15_dl3684_v0_v1_opt76387", "d0starrho", "ggh", 2, {0, 1}, 15, 3684, "!V:VarTransform=G,N,G:NTrees=2300:BoostType=Grad:Shrinkage=0.054:MaxDepth=9:SeparationType=RegressionVariance:nCuts=37:UseRandomisedTrees=F:UseNvars=66:UseBaggedBoost=F:BaggedSampleFraction=1.167:PruneMethod=NoPruning:PruneStrength=50:PruningValFraction=0.602")' && python computeErrors.py -m BDTG_df15_dl3684_v0_v1_opt76387 -c d0starrho -p ggh
```

Calling the `slurm.py` with this file will queue 4 jobs (one per line), where in each line the first three commands will train the model with the three different samples, and the last command will evaluate the model.

To evaluate the RECO values of the pT with no model, one can include the following line in the `commands.txt` file:
```
eval_BDTG_NONE:::python computeErrors.py -m BDTG_NONE
```

## 4. Additional scripts and files
- `joinRMSfiles.sh`: To join the different evaluation files into a single one, one can use the `joinRMSfiles.sh` bash script. This will create a file named `eval<channelName>.out` with all the values.
- `autoPlot.sh`, `checkQueue.sh`, `queue.sh`, `timeJobsPlot.py`, `monitoringSlurm.sh`: Files to monitor the queued jobs in slurm, generating a plot of the completed jobs.
- `optionModels.out`: History of attempted models, with their number and hyperparameters used.