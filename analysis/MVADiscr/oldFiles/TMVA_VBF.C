#include <string.h>
#include "TROOT.h"
#include "TMVA/CrossValidation.h"
#include "TMVA/DataLoader.h"
#include "TMVA/Factory.h"
#include "TMVA/Types.h"
#include "TFile.h"
#include "TCollection.h"
#include "TCut.h"
#include "TObjArray.h"
#include "TString.h"
#include "TTree.h"

void TMVA_VBF ( const char* outFileName,
                const char* channel )
{
    (TMVA::gConfig().GetVariablePlotting()).fMaxNumOfAllowedVariablesForScatterPlots = 40;
    
    // options to control used methods
    bool useRandomSplitting = false; // option for cross validation
    bool useLikelihood = true;    // likelihood based discriminant
    bool useLikelihoodKDE = false;    // likelihood based discriminant
    bool useFischer = false;       // Fischer discriminant
    bool useMLP = false;          // Multi Layer Perceptron (old TMVA NN implementation)
    bool useBDT = false;           // Boosted Decision Tree
    bool useBDTG = false;         // BDT with GradBoost
    bool useDL = false;            // TMVA Deep Learning ( CPU or GPU)
    // bool useKeras = false;        // Keras Deep learning
    
    // Open files
    TString fileformat;
    TFile* sgnfile;
    TFile* bkgfile;
    if ( std::strcmp(channel, "rhophi") == 0 ) {
        sgnfile = TFile::Open("/work/submit/kyoon/RareHiggs/data/2023/SEPT29/comb/VBF_rhophi_combined_signal.root", "READ");
        bkgfile = TFile::Open("/work/submit/kyoon/RareHiggs/data/2023/SEPT29/comb/VBF_rhophi_combined_background.root", "READ");
    } else if ( std::strcmp(channel, "k0star") == 0 ) {
        sgnfile = TFile::Open("/work/submit/kyoon/RareHiggs/data/2023/SEPT29/comb/VBF_k0star_combined_signal.root", "READ");
        bkgfile = TFile::Open("/work/submit/kyoon/RareHiggs/data/2023/SEPT29/comb/VBF_k0star_combined_background.root", "READ");
    }

    // Initialize the dataset
    TFile* outfile = TFile::Open(outFileName, "RECREATE");
    TMVA::DataLoader *dataloader = new TMVA::DataLoader("dataset");
    
    // Add variables to dataset
    dataloader->AddVariable("HCandMass", "HCandMass", "GeV/c^2", 'F'); // DON'T USE!!

    dataloader->AddVariable("HCandPT", "HCandPT", "", 'F');//
    // dataloader->AddVariable("HCandPT/HCandMass", "HCandPT__div_HCandMass", "", 'F');
    dataloader->AddVariable("goodPhotons_pt[index_pair[1]]", "photon_pt", "", 'F');
    // dataloader->AddVariable("goodPhotons_pt[index_pair[1]]/HCandPT", "photon_pt__div_HCandPT", "", 'F');
    // dataloader->AddVariable("goodPhotons_pt[index_pair[1]]/HCandMass", "photon_pt__div_HCandMass", "", 'F');// 
    // dataloader->AddVariable("goodMeson_pt[index_pair[0]]", "meson_pt", "", 'F');//
    // dataloader->AddVariable("goodMeson_pt[index_pair[0]]/HCandPT", "meson_pt__div_HCandPT", "", 'F');
    dataloader->AddVariable("goodMeson_pt[index_pair[0]]/HCandMass", "meson_pt__div_HCandMass", "", 'F'); 
    // dataloader->AddVariable("goodMeson_DR[index_pair[0]]", "meson_DR", "", 'F');//
    // dataloader->AddVariable("goodMeson_DR[index_pair[0]] * HCandMass", "meson_DR__times_HCandMass", "", 'F');


    // dataloader->AddVariable("goodPhotons_eta[index_pair[1]]", "photon_eta", "", 'F');
    dataloader->AddVariable("goodPhotons_mvaID[index_pair[1]]", "photon_mvaID", "", 'F');
    // dataloader->AddVariable("SoftActivityJetNjets5", "SoftActivityJetNjets5", "", 'F');
    // dataloader->AddVariable("DeepMETResolutionTune_pt", "DeepMETResolutionTune_pt", "GeV/c", 'F'); // high corr in VBF phi
    // dataloader->AddVariable("goodMeson_mass[index_pair[0]]", "meson_mass", "GeV/c^2", 'F');
    dataloader->AddVariable("goodMeson_iso[index_pair[0]]", "meson_iso", "", 'F');
    
    // dataloader->AddVariable("goodMeson_vtx_chi2dof[index_pair[0]]", "meson_vtx_chi2dof", "", 'F');
    // dataloader->AddVariable("goodMeson_vtx_prob[index_pair[0]]", "meson_vtx_prob", "", 'F');
    // dataloader->AddVariable("goodMeson_massErr[index_pair[0]]", "meson_massErr", "GeV/c^2", 'F');
    
    // dataloader->AddVariable("goodMeson_sipPV[index_pair[0]]", "meson_sipPV", "", 'F');
    // dataloader->AddVariable("goodMeson_trk1_pt[index_pair[0]]", "meson_trk1_pt", "", 'F');
    // dataloader->AddVariable("goodMeson_trk2_pt[index_pair[0]]", "meson_trk2_pt", "", 'F');
    // dataloader->AddVariable("goodMeson_trk1_eta[index_pair[0]]", "meson_trk1_eta", "", 'F');
    // dataloader->AddVariable("goodMeson_trk2_eta[index_pair[0]]", "meson_trk2_eta", "", 'F');
     
    // dataloader->AddVariable("dPhiGammaMesonCand", "dPhiGammaMesonCand", "", 'F');
    // dataloader->AddVariable("dEtaGammaMesonCand", "dEtaGammaMesonCand", "", 'F');//
    // dataloader->AddVariable("dPhiGammaMesonCand/HCandMass", "dPhiGammaMesonCand__div_HCandMass", "", 'F');//
    // dataloader->AddVariable("dEtaGammaMesonCand/HCandMass", "dEtaGammaMesonCand__div_HCandMass", "", 'F');//  // high corr in VBF phi and VBFlow rho
    
    // dataloader->AddVariable("nGoodJets", "nGoodJets", "", 'F'); // high corr in VBF phi, VBFlow phi
    // dataloader->AddVariable("sigmaHCandMass_Rel2", "sigmaHCandMass_Rel2", "", 'F');
    // dataloader->AddVariable("goodPhotons_energyErr[index_pair[1]]", "photon_energyErr", "", 'F');
    dataloader->AddVariable("mJJ", "mJJ", "", 'F');
    // dataloader->AddVariable("dEtaJJ", "dEtaJJ", "", 'F'); // corr with mJJ
    dataloader->AddVariable("dPhiJJ", "dPhiJJ", "", 'F'); // high corr in VBF phi
    // dataloader->AddVariable("Y1Y2", "Y1Y2", "", 'F');
    // dataloader->AddVariable("deltaJetMeson", "deltaJetMeson", "", 'F');
    // dataloader->AddVariable("deltaJetPhoton", "deltaJetPhoton", "", 'F');
    // dataloader->AddVariable("jet1Pt", "jet1Pt", "", 'F');
    // dataloader->AddVariable("jet2Pt", "jet2Pt", "", 'F');


    // dataloader->AddVariable("jet1Eta", "jet1Eta", "", 'F');
    // dataloader->AddVariable("jet2Eta", "jet2Eta", "", 'F');
    // dataloader->AddVariable("jet1hfsigmaPhiPhi", "jet1hfsigmaPhiPhi", "", 'F');
    // dataloader->AddVariable("jet2hfsigmaPhiPhi", "jet2hfsigmaPhiPhi", "", 'F');
    // dataloader->AddVariable("jet1hfsigmaEtaEta", "jet1hfsigmaEtaEta", "", 'F');
    // dataloader->AddVariable("jet2hfsigmaEtaEta", "jet2hfsigmaEtaEta", "", 'F');
    dataloader->AddVariable("zepVar", "zepVar", "", 'F');
    // dataloader->AddVariable("detaHigJet1", "detaHigJet1", "", 'F');
    // dataloader->AddVariable("detaHigJet2", "detaHigJet2", "", 'F');     

        
    // Set weights
    dataloader->SetWeightExpression("(mc>=0 && mc<1000)? (w_allSF * lumiIntegrated / sigmaHCandMass_Rel2) : (w_allSF * lumiIntegrated * 1.5 * TMath::Sin(theta) * TMath::Sin(theta) / sigmaHCandMass_Rel2)");
    
    // Spectator used for split
    // dataloader->AddSpectator("Entry$", "eventID");

    // Apply split
    ////////////////////// TODO: use cross validation /////////////////////////
    const char* trainTreeEventSplitStr = "(Entry$ % 3) >= 0"; //"(Entry$ % 10)>=5";
    const char* testTreeEventSplitStr = "(Entry$ % 3) == 0"; //"(Entry$ % 10)<5";
    
    // Apply cuts
    // const char* higgsMass_full = "HCandMass > 110 && HCandMass < 160";
    const char* higgsMass_full = "HCandMass > 100 && HCandMass < 170";
    const char* nanRemove = "!TMath::IsNaN(goodMeson_massErr[index_pair[0]]) && !TMath::IsNaN(sigmaHCandMass_Rel2)";
    
    TCut cutSignalTrain = Form("%s && %s && %s", trainTreeEventSplitStr, higgsMass_full, nanRemove);
    TCut cutBkgTrain = Form("%s && %s && %s", trainTreeEventSplitStr, higgsMass_full, nanRemove);
    TCut cutSignalTest = Form("%s && %s && %s", testTreeEventSplitStr, higgsMass_full, nanRemove);
    TCut cutBkgTest = Form("%s && %s && %s", testTreeEventSplitStr, higgsMass_full, nanRemove);
    
    // Register trees
    ///////////////////// TODO: add weight per event basis /////////////////////
    double signalWeight = 1.0;
    double backgroundWeight = 1.0;
    //dataloader->AddTree((TTree*)sgnfile->Get("events"), "Signal",
    //                    signalWeight, cutTrainSignal, "train");
    //dataloader->AddTree((TTree*)sgnfile->Get("events"), "Signal",
    //                    signalWeight, cutTestSignal, "test");
    dataloader->AddTree((TTree*)sgnfile->Get("events"), "Signal", signalWeight, cutSignalTrain, "train");
    dataloader->AddTree((TTree*)bkgfile->Get("events"), "Background", backgroundWeight, cutBkgTrain, "train");
    
    dataloader->AddTree((TTree*)sgnfile->Get("events"), "Signal", signalWeight, cutSignalTest, "test");
    dataloader->AddTree((TTree*)bkgfile->Get("events"), "Background", backgroundWeight, cutBkgTest, "test");

    /*
    dataloader->PrepareTrainingAndTestTree(cutSignal, cutBkg,
                                           "nTrain_Signal=-1"
                                           "nTrain_Background=-1"
                                           "nTest_Signal=0"
                                           ":nTest_Background=0"
                                           ":SplitMode=Random"
                                           ":NormMode=NumEvents"
                                           ":!V");
    */

    TMVA::Factory factory("TMVAClassification", outfile, "!V:!Silent:Color:DrawProgressBar:AnalysisType=Classification");

    /*
    // Use cross validation
    int numFolds = 3;
    const char* analysisType = "Classification";
    const char* splitType = (useRandomSplitting) ? "Random" : "Deterministic";
    const char* splitExpr = (!useRandomSplitting) ? "int(fabs([eventID]))%int([NumFolds])" : "";
    TString cvOptions = Form("!V"
                            ":!Silent"
                            ":ModelPersistence"
                            ":AnalysisType=%s"
                            ":SplitType=%s"
                            ":NumFolds=%i"
                            ":SplitExpr=%s",
                            analysisType, splitType, numFolds, splitExpr);
    TMVA::CrossValidation cv("TMVACrossValidation", dataloader, outfile, cvOptions);
    */
    
    // Prepare training and test trees
    TString prepareOptions = "NormMode=None";
    prepareOptions+=":SplitMode=random:!V";
    prepareOptions+=":MixMode=Random";
    dataloader->PrepareTrainingAndTestTree("", prepareOptions);

    /*
        ## Booking Methods
 
        Here we book the TMVA methods. We book first a Likelihood based on KDE (Kernel Density Estimation), a Fischer discriminant, a BDT
        and a shallow neural network
 
    */
 
    // Likelihood ("naive Bayes estimator")
    if (useLikelihood)
    {
        factory.BookMethod(dataloader,TMVA::Types::kLikelihood, "Likelihood",
                      "H:!V:TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmoothBkg[1]=10:NSmooth=1:NAvEvtPerBin=50" );
    }
    
    // Use a kernel density estimator to approximate the PDFs
    if (useLikelihoodKDE)
    {
        factory.BookMethod(dataloader,TMVA::Types::kLikelihood, "LikelihoodKDE",
                      "!H:!V:!TransformOutput:PDFInterpol=KDE:KDEtype=Gauss:KDEiter=Adaptive:KDEFineFactor=0.3:KDEborder=None:NAvEvtPerBin=50" );
    }
 
    // Fisher discriminant (same as LD)
    if (useFischer)
    {
        factory.BookMethod(dataloader,TMVA::Types::kFisher, "Fisher", "H:!V:Fisher:VarTransform=None:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:NbinsMVAPdf=50:NsmoothMVAPdf=10" );
    }
 
    // Boosted Decision Trees
    if (useBDT)
    {
        factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDT",
                      "!V:VarTransform=P,D:NTrees=110:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
    }

    if (useBDTG)
    {
        // rhophi
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG",
        //                     "!V:NTrees=600:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // k0star
        factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG",
                            "!V:NTrees=800:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG11",
        //                    "!V:NTrees=800:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG12",
        //                    "!V:NTrees=800:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.15:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG13",
        //                    "!V:NTrees=800:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.20:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG14",
        //                    "!V:NTrees=800:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.25:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG15",
        //                    "!V:NTrees=800:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.30:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG16",
        //                    "!V:NTrees=800:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.35:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG17",
        //                    "!V:NTrees=800:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.40:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG18",
        //                    "!V:NTrees=800:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.45:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG21",
        //                    "!V:NTrees=600:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG22",
        //                    "!V:NTrees=600:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.15:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG23",
        //                    "!V:NTrees=600:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.20:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG24",
        //                    "!V:NTrees=600:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.25:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG25",
        //                    "!V:NTrees=600:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.30:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG26",
        //                    "!V:NTrees=600:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.35:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG27",
        //                    "!V:NTrees=600:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.40:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG28",
        //                    "!V:NTrees=600:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.45:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG31",
        //                    "!V:NTrees=400:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG32",
        //                    "!V:NTrees=400:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.15:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG33",
        //                    "!V:NTrees=400:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.20:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG34",
        //                    "!V:NTrees=400:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.25:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG35",
        //                    "!V:NTrees=400:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.30:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG36",
        //                    "!V:NTrees=400:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.35:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG37",
        //                    "!V:NTrees=400:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.40:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG38",
        //                    "!V:NTrees=400:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.45:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG41",
        //                    "!V:NTrees=200:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG42",
        //                    "!V:NTrees=200:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.15:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG43",
        //                    "!V:NTrees=200:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.20:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG44",
        //                    "!V:NTrees=200:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.25:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG45",
        //                    "!V:NTrees=200:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.30:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG46",
        //                    "!V:NTrees=200:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.35:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG47",
        //                    "!V:NTrees=200:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.40:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG48",
        //                    "!V:NTrees=200:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.45:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
    }
 
    // Multi-Layer Perceptron (Neural Network)
    if (useMLP)
    {
        factory.BookMethod(dataloader,TMVA::Types::kMLP, "MLP",
                      "!H:!V:NeuronType=tanh:VarTransform=N:NCycles=100:HiddenLayers=N+5:TestRate=5:UseRegulator" );
    }

    // Deep Neural Network
    if (useDL)
    {
 
        bool useDLGPU = false;
#ifdef R__HAS_TMVAGPU
        useDLGPU = true;
#endif
 
        // Define DNN layout
        TString inputLayoutString = "InputLayout=1|1|19";
        TString batchLayoutString= "BatchLayout=1|128|19";
        TString layoutString ("Layout=DENSE|64|TANH,DENSE|64|TANH,DENSE|64|TANH,DENSE|64|TANH,DENSE|1|LINEAR");
        // Define Training strategies
        // one can catenate several training strategies
        TString training1("LearningRate=1e-3,Momentum=0.9,"
                          "ConvergenceSteps=10,BatchSize=128,TestRepetitions=1,"
                          "MaxEpochs=30,WeightDecay=1e-4,Regularization=None,"
                          "Optimizer=ADAM,ADAM_beta1=0.9,ADAM_beta2=0.999,ADAM_eps=1.E-7," // ADAM default parameters
                          "DropConfig=0.0+0.0+0.0+0.");
        //     TString training2("LearningRate=1e-3,Momentum=0.9"
        //                       "ConvergenceSteps=10,BatchSize=128,TestRepetitions=1,"
        //                       "MaxEpochs=20,WeightDecay=1e-4,Regularization=None,"
        //                       "Optimizer=SGD,DropConfig=0.0+0.0+0.0+0.");
 
        TString trainingStrategyString ("TrainingStrategy=");
        trainingStrategyString += training1; // + "|" + training2;
 
        // General Options.
 
        TString dnnOptions ("!H:V:ErrorStrategy=CROSSENTROPY:VarTransform=G:"
                            "WeightInitialization=XAVIER");
        dnnOptions.Append (":"); dnnOptions.Append (inputLayoutString);
        dnnOptions.Append (":"); dnnOptions.Append (batchLayoutString);
        dnnOptions.Append (":"); dnnOptions.Append (layoutString);
        dnnOptions.Append (":"); dnnOptions.Append (trainingStrategyString);
 
        TString dnnMethodName = "DNN_CPU";
        if (useDLGPU) {
            dnnOptions += ":Architecture=GPU";
            dnnMethodName = "DNN_GPU";
        } else  {
            dnnOptions += ":Architecture=CPU";
        }
 
        factory.BookMethod(dataloader,TMVA::Types::kDL, dnnMethodName, dnnOptions);
    }
 
    /*
    // Keras deep learning
    if (useKeras) {

        Info("TMVA_Higgs_Classification", "Building deep neural network with keras ");
        // create python script which can be executed
        // create 2 conv2d layer + maxpool + dense
        TMacro m;
        m.AddLine("import tensorflow");
        m.AddLine("from tensorflow.keras.models import Sequential");
        m.AddLine("from tensorflow.keras.optimizers import Adam");
        m.AddLine("from tensorflow.keras.layers import Input, Dense");
        m.AddLine("");
        m.AddLine("model = Sequential() ");
        m.AddLine("model.add(Dense(64, activation='relu',input_dim=7))");
        m.AddLine("model.add(Dense(64, activation='relu'))");
        m.AddLine("model.add(Dense(64, activation='relu'))");
        m.AddLine("model.add(Dense(64, activation='relu'))");
        m.AddLine("model.add(Dense(2, activation='sigmoid'))");
        m.AddLine("model.compile(loss = 'binary_crossentropy', optimizer = Adam(learning_rate = 0.001), metrics = ['accuracy'])");
        m.AddLine("model.save('Higgs_model.h5')");
        m.AddLine("model.summary()");
 
        m.SaveSource("make_higgs_model.py");
        // execute
        auto ret = (TString *)gROOT->ProcessLine("TMVA::Python_Executable()");
        TString python_exe = (ret) ? *(ret) : "python";
        gSystem->Exec(python_exe + " make_higgs_model.py");
 
        if (gSystem->AccessPathName("Higgs_model.h5")) {
            Warning("TMVA_Higgs_Classification", "Error creating Keras model file - skip using Keras");
        } else {
            // book PyKeras method only if Keras model could be created
            Info("TMVA_Higgs_Classification", "Booking tf.Keras Dense model");
            factory.BookMethod(
                               dataloader, TMVA::Types::kPyKeras, "PyKeras",
                               "H:!V:VarTransform=None:FilenameModel=Higgs_model.h5:tf.keras:"
                               "FilenameTrainedModel=Higgs_trained_model.h5:NumEpochs=20:BatchSize=100:"
                               "GpuOptions=allow_growth=True"); // needed for RTX NVidia card and to avoid TF allocates all GPU memory
        }
    }
    */
 
    /*
      ## Train Methods
      Here we train all the previously booked methods.
    */
 
    factory.TrainAllMethods();
 
    /*
      ## Test  all methods
      Now we test and evaluate all methods using the test data set
    */
    
    factory.TestAllMethods();
    factory.EvaluateAllMethods();
    //cv.Evaluate();
 
    // after we get the ROC curve and we display
    // auto c1 = factory.GetROCCurve(dataloader);
    // c1->Draw();
}
