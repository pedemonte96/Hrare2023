# Search for rare Higgs boson decays to a photon and a meson

This repository contains the analysis code and [2023 ETH Zürich master's thesis](finished_thesis/main.pdf) ([MIT-hosted copy](https://ppc.mit.edu/wp-content/uploads/2026/02/MPedemonte_MscThesisETH.pdf)) by Martí Pedemonte Bernat, conducted at MIT, for a search for $H \to M\gamma$, where $M$ is a $\phi$, $\omega$, or $D^{*0}$ meson.

|                           | At a glance                                                                                                                                                                                                                                                                                                       |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Scientific question**   | Can rare exclusive decays probe the Higgs boson's couplings to light quarks and reveal deviations from the Standard Model?                                                                                                                                                                                        |
| **Dataset**               | 39.54 fb⁻¹ of 13 TeV proton–proton collisions recorded by CMS in 2018, selected with `HLT_Photon35_TwoProngs35`; simulated ggH and VBF events model the signal.                                                                                                                                                   |
| **Method**                | Reconstruct charged tracks and neutral decay products, correct meson transverse momentum with boosted decision tree regression, fit signal simulation and a data-driven background in two mass dimensions, then set expected 95% CL limits with asymptotic CLs in CMS Combine.                                    |
| **Contribution**          | Extend an existing two-track meson analysis to $\phi/\omega \to \pi^+\pi^-\pi^0$ and $D^{*0} \to D^0\pi^0/\gamma$, including neutral-particle recovery, regression, and two-dimensional fits. The repository's 299 commits through March 2024 document this development alongside the broader analysis framework. |
| **Representative result** | For $H \to D^{*0}\gamma$ with $D^0 \to K^-\pi^+$, the **expected**, blinded 95% CL branching-fraction limit is **$7.403 \times 10^{-3}$**. The two-dimensional fit improves on the one-dimensional estimate of $1.008 \times 10^{-2}$ by 27%.                                                                     |

**Analysis path:** MiniAOD → custom meson NanoAOD → skimming and event selection → meson $p_T$ regression → RooFit workspaces → Combine limits. See the [repository guide](#repository-guide) for the code at each stage.

## Run a small example

With CMS Combine available in a compatible Linux/CMSSW environment, run an expected-limit fit from the repository root:

```bash
cd analysis/FITS
combine -M AsymptoticLimits -m 125 -t -1 DATACARDS/datacard_STAT_Phi_Wcat_Run2.txt -n PhiWcat --run expected
```

This reads the checked-in [$\phi\gamma$ W-category datacard](analysis/FITS/DATACARDS/datacard_STAT_Phi_Wcat_Run2.txt) and its [ROOT workspace](analysis/FITS/DATACARDS/workspace_STAT_PhiCat_Wcat_Run2.root), then prints expected limit quantiles. It exercises the statistical stage of the earlier two-track meson analysis; the thesis's final two-dimensional inputs and CMS collision samples are not included in the repository.

## Analysis and results

The thesis studies four decay chains. A photon and a meson candidate are reconstructed from the 2018 data; the background mass distribution is fitted from data with the Higgs signal region blinded at $115 < m_{M\gamma} < 135$ GeV. Signal shapes come from simulated Higgs events. The final fit uses the photon–meson invariant mass and the meson mass, or the charged-track pair mass for the $D^0 \to K^-\pi^+$ channel. RooFit models the signal with Crystal Ball functions and the background with alternative polynomial shapes. CMS Combine uses the asymptotic CLs method to estimate the 95% confidence-level upper limits.

| Higgs decay and reconstructed meson decay          |     Expected limit, 1D |     Expected limit, 2D |
| -------------------------------------------------- | ---------------------: | ---------------------: |
| $H \to \phi\gamma$, $\phi \to \pi^+\pi^-\pi^0$     | $2.281 \times 10^{-2}$ | $1.969 \times 10^{-2}$ |
| $H \to \omega\gamma$, $\omega \to \pi^+\pi^-\pi^0$ | $3.234 \times 10^{-3}$ | $2.867 \times 10^{-3}$ |
| $H \to D^{*0}\gamma$, $D^0 \to K^-\pi^+$           | $1.008 \times 10^{-2}$ | $7.403 \times 10^{-3}$ |
| $H \to D^{*0}\gamma$, $D^0 \to K^-\pi^+\pi^0$      | $1.697 \times 10^{-2}$ | $1.268 \times 10^{-2}$ |

Both $D^{*0}$ channels include $D^{*0} \to D^0\pi^0/\gamma$ and the charge-conjugate decay. These are **expected estimates, not observed limits or evidence of a signal**. The [thesis analysis chapter](finished_thesis/mainmatter/3_analysis.tex) gives the selection, fit validation, and comparison with existing results.

## Repository guide

| Location                                                                                                                                         | Purpose                                                                                                                       |
| ------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| [`NanoAOD/`](NanoAOD/)                                                                                                                           | CMSSW producers and configuration for meson and dimuon candidate tables; dataset lists for the Run 2 campaigns.               |
| [`analysis/skimming/`](analysis/skimming/), [`analysis/VGammaMeson_cat.py`](analysis/VGammaMeson_cat.py), [`analysis/config/`](analysis/config/) | Data skims, event categories, triggers, object selection, and analysis ntuples.                                               |
| [`analysis/TMVA_regression/`](analysis/TMVA_regression/)                                                                                         | Three-sample TMVA training and evaluation for meson $p_T$ regression.                                                         |
| [`analysis/MVADiscr/`](analysis/MVADiscr/)                                                                                                       | Follow-on signal/background discriminator studies.                                                                            |
| [`analysis/FITS_marti/`](analysis/FITS_marti/)                                                                                                   | Histogram production, one- and two-dimensional RooFit models, datacards, and expected-limit commands for the thesis channels. |
| [`analysis/FITS/`](analysis/FITS/)                                                                                                               | Earlier $\rho\gamma$ and $\phi\gamma$ fits, including the archived datacards and workspaces used in the example above.        |
| [`genProduction/UL/`](genProduction/UL/)                                                                                                         | Ultra Legacy generator fragments for related meson–photon decay modes.                                                        |
| [`finished_thesis/`](finished_thesis/)                                                                                                           | Final thesis source and [PDF](finished_thesis/main.pdf).                                                                      |

The full analysis requires CMS MiniAOD/NanoAOD inputs and site-specific paths referenced by the scripts. Histogram production and regression were developed with Python 3.11 and ROOT 6.28; the fit and Combine stage used CMSSW 10_6_27 with Python 2.7 and ROOT 6.14. The [analysis environment notes](analysis/README.md), [regression guide](analysis/TMVA_regression/README.md), and [fit guide](analysis/FITS_marti/README.md) record the original workflow.

## NanoAOD production reference

To build the CMSSW modules, place this checkout at `CMSSW_10_6_27/src/Hrare`, activate the release with `cmsenv`, and run `scram b`. The NanoAOD customization is `--customise=Hrare/NanoAOD/nano_cff.nanoAOD_customizeMesons`; see [`NanoAOD/python/nano_cff.py`](NanoAOD/python/nano_cff.py). The historical NanoAODv9 global tags and eras used by the project are:

| Input dataset                  | Global tag                            | Era                                  |
| ------------------------------ | ------------------------------------- | ------------------------------------ |
| RunIISummer20UL16MiniAODAPV MC | `106X_mcRun2_asymptotic_preVFP_v11`   | `Run2_2016_HIPM,run2_nanoAOD_106Xv2` |
| RunIISummer20UL16MiniAOD MC    | `106X_mcRun2_asymptotic_v17`          | `Run2_2016,run2_nanoAOD_106Xv2`      |
| RunIISummer20UL17MiniAOD MC    | `106X_mc2017_realistic_v9`            | `Run2_2017,run2_nanoAOD_106Xv2`      |
| RunIISummer20UL18MiniAOD MC    | `106X_upgrade2018_realistic_v16_L1v1` | `Run2_2018,run2_nanoAOD_106Xv2`      |
| HIPM UL2016 data (Summer19/20) | `106X_dataRun2_v35`                   | `Run2_2016_HIPM,run2_nanoAOD_106Xv2` |
| 2016 UL data (Summer19/20)     | `106X_dataRun2_v35`                   | `Run2_2016,run2_nanoAOD_106Xv2`      |
| 2017 UL data (Summer19/20)     | `106X_dataRun2_v35`                   | `Run2_2017,run2_nanoAOD_106Xv2`      |
| 2018 UL data (Summer19/20)     | `106X_dataRun2_v35`                   | `Run2_2018,run2_nanoAOD_106Xv2`      |
