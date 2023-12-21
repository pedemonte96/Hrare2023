# BDT MVA Discriminator
**Requirements:**
- Python 3.11
- ROOT 6.28

## 1. Create Snapshot to Include Predicted pT and HCandMass after Regression
Since the MVA discriminator is computed after the regression of the meson's pT, the first step is to create a snapshot of the files with the regressed pT and its updated HCandMass value.

To do so, one must run the `createSnapshotsAfterRegression.py`. This script iterates through the decay channels, calling the function `createSnapshotAfterRegression`. This function reads the different signal and background files and outputs four ROOT files with the following new columns in the trees:

- `goodMeson_pt_PRED`: Full meson transverse momentum after regression.
- `HCandMass_varPRED`: Higgs invariant mass with new regressed momentum pT.
- `HCandPt_varPRED`: Higgs transverse momentum with new regressed momentum pT.

The four files consist of three for signal and only one joint background file.

## 2. Train Likelihood and BDT Discriminators

The main file to train the models is `TMVA_GF_disc_vars_afterRegression.C`, which is very similar to pT regression. This function requires the following arguments:

- `outFileName`: Name of the output ROOT file.
- `channel`: Channel to study (e.g., `omega`, `phi`, `d0starrho`, `d0star`).
- `testSet`: Set used for testing (e.g., 0, 1, or 2).
- `codeVars`: Code referring to which variables to use.

It would be interesting to add a string variable encoding the hyperparameters of the model, as done in `TMVA_GF_regression.C`, so that many different models can be tested more easily.

The sets used for training and testing follow the previous snapshots and are of the form:

```bash
/data/submit/pdmonte/outputs/NOV05/2018/outname_mc1038_GFcat_OmegaCat_2018_sample%d_after.root
/data/submit/pdmonte/outputs/NOV05/2018/outname_mc0_GFcat_OmegaCat_2018_after.root
```
where `%d` is 0, 1 or 2 for the signal (first line), and the joint background has the arbitrary number 0.

One should train the model three times to have cross-validation, one for each different sample, to obtain three different weight files, to apply to each of the testing samples. Ideally in the future one would need to train the model with a big training set, and have only one weight file to apply to a different (unseen) sample.

Training a model will produce a ROOT file in
```bash
/data/submit/pdmonte/TMVA_disc/rootVars/
```
and a weight file in
```bash
/data/submit/pdmonte/TMVA_disc/weights/
```

## 3. Evaluate the discriminators

To evaluate the discriminants, the file `testEff.ipynb` is used. It reads the test samples and shows the shapes of the discriminant for signal and background. It also optimizes the threshold of the MVA discriminator to maximize the significance (S/sqrt(B)), and compares the shapes of the HCandMass before and after the MVA selection cut, to make sure the model is not using variables that are biasing and shaping the background.

## 4. Check for optimal variables to include in the model

To check which variables might be good to use to distinguish signal from background, the `createAllPlots.py` script can be used. It plots many variables (250+) in the folder
```bash
/home/submit/pdmonte/public_html/MVA_plots
```
which can be qualitatively interpreted to include or not in the MVA model. The script also provides a list of the variables that are more different between signal and background. The most relevant variables to use in the MVA discriminant are the following, in order of importance:

1. 'phi_isoNeuHad'
2. 'goodMeson_iso'
3. 'Tau_rawDeepTau2017v2p1VSjet'
4. 'var0_input_pred'
5. 'SV_pt'
6. 'var3_input_pred'
7. 'Tau_rawIso'
8. 'nTau'
9. 'goodMeson_pt'
10. 'goodMeson_sipPV'
11. 'boostedTau_rawIso'
12. 'goodMeson_photon1_pt'
13. 'Tau_chargedIso'
14. 'goodMeson_photon1_DR'
15. 'var5_input_pred'
16. 'Tau_photonsOutsideSignalCone'
17. 'var1_input_pred'
18. 'var2_input_pred'
19. 'FsrPhoton_pt'
20. 'var8_input_pred'
21. 'var6_input_pred'
22. 'boostedTau_chargedIso'
23. 'var4_input_pred'
24. 'Tau_pt'
25. 'boostedTau_rawIsodR03'
26. 'FsrPhoton_eta'
27. 'goodMeson_mass'
28. 'HCandMass'
29. 'var14_input_pred'
30. 'classify'
31. 'boostedTau_rawMVAoldDMdR032017v2'
32. 'goodPhotons_energyErr'
33. 'nTrigObj'
34. 'boostedTau_photonsOutsideSignalCone'
35. 'goodPhotons_pt'
36. 'SubJet_mass'
37. 'SubJet_n2b1'
38. 'goodMeson_bestVtx_R'
39. 'goodMeson_massErr'
40. 'boostedTau_neutralIso'
41. 'goodMeson_mass_raw'
42. 'goodMeson_DR'
43. 'Tau_rawIsodR03'
44. 'var10_input_pred'
45. 'boostedTau_rawMVAoldDM2017v2'
46. 'SubJet_n3b1'
47. 'Tau_jetIdx'
48. 'sigmaHCandMass_Rel2'
49. 'Tau_neutralIso'
50. 'Photon_sieie'

Among the variables currently available for all the events, the ones uncommented in the `TMVA_GF_disc_vars_afterRegression.C` file in lines 78-87 are the ones that provide a reasonable improvement, with signal (background) efficiency of 56% (14%), resulting in a potential decrement of -32% in the final limits.

## 5. Potential future improvements

It will be interesting to set up a slurm file such as the one used for the BDT regression to test exhaustively the variables of the model.

To avoid shaping the background too much, one can create a metric to compare the shapes of the background before and after the optimal MVA discriminant cut.

Also, a coefficient of importance of the variables in the model can be created to rank them in order of relevance. For example, out of a set of 20 potential variables, create all the possible models with three variables only (1140 different models) and with 17 variables only (also 1140 different models). Then, for each of the models, every variable present in the model gets a score (for example, the maximum value of S/sqrt(B)). This is done for all variables and one should get a ranking of the most meaningful variables. Then one can drop the last 5 variables and have a set of 15 potential variables, and run the same experiment with 5 and 10 variables (which would be 2x3003 models, something feasable). Then one rank the variables once again and exhaustively checks all possible combinations with the top 12 ranked variables (4096 different models) to get the best model.
