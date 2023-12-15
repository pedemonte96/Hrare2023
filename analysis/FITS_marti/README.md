# Signal and Background 1D/2D Fits

This section of the analysis is divided into three parts due to compatibility reasons with ROOT. First, it is necessary to create and save the histograms to ROOT files. In the second step, one should read these ROOT files and perform the fits. Finally, after the fits are completed, limits can be computed using the combine package of CMSSW.

## 1. Create Histograms
**Requirements:**
- Python 3.11
- ROOT 6.28

The main script for creating and saving histograms is `createHistogramFiles.py`. Two methods are used for signal and background, respectively. These methods require the following arguments:

- `mesonCat`: Channel to study (`["Phi3Cat", "OmegaCat", "D0StarCat", "D0StarRhoCat"]`).
- `year`: Set to 2018 for all channels.
- `date`: Date of the sample (in my final version, NOV05).
- `regModelName`: Name of the pT regression model used (optional).
- `doubleFit`: Boolean to save a 1D (`False`) or 2D (`True`) histogram (default is `False`).

These methods utilize functions defined in `prepareFits.py` to create histograms, generate unique file names, read and save ROOT files, etc.

To create the desired histograms, modify the main part of the `createHistogramFiles.py` script and then run:

```bash
python3 createHistogramFiles.py
```

It is possible to run multiple regression models. The names of these models should be in a file named `models_<channelName>.txt`. If the name of the model is `RECO`, then no regression model is used. These model files are also used in the subsequent steps.

The histograms will be created in `/data/submit/pdmonte/outHistsFits/`.

## 2. Fit Histograms and Create Workspaces
To run this part of the analysis, the `cmsenv` environment is required, which can be activated by running the following commands:

```bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /home/submit/pdmonte/CMSSW_10_6_27/src
cmsenv
```

More information on setting up the CMSSW `cmsenv` can be found [here](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookSetComputerNode). The versions of the main frameworks used within this environment are:
- Python 2.7.14
- ROOT 6.14

The fits are performed in `SIGfits.py` and `BKGfits.py` for signal and background, respectively. In these files, there are two methods, one for the 1D fit and another for the 2D fit. Each method requires the same arguments as for creating the histograms in the previous step. The ROOT files containing the histogram are read from `/data/submit/pdmonte/outHistsFits/`, so they must be created in the first step.

These methods fit the histograms to analytical functions, generate histogram plots in `/home/submit/pdmonte/public_html/fits`, and create the workspaces necessary to create the data cards in the folder `workspaceName = 'WS_NOV16'`.

To fit the previously created histograms, run these two scripts:

```bash
python SIGfits.py # for the signal
python BKGfits.py # for the background
```

## 3. Create Datacards and Compute Asymptotic Limits
Once the workspaces have been created, one can run the limits on the fits. To do so, like the previous step, the `cmsenv` environment is required.

This last step is handled by the bash script `combineCommand.sh`. This script will create the datacards for each channel and model using the `createDatacards.py` Python script. After this, it uses the `combine` command within CMSSW to compute the asymptotic limits. The results will be in `WS_NOV16/results*`, but to put them all together, one can use the `getAllLimits.sh` bash script, which will gather all the result files and combine them into a single file for each channel, of the form `limits_<channelName>.out`.

It can be run by executing the following command:

```bash
bash combineCommand.sh
bash getAllLimits.sh
```