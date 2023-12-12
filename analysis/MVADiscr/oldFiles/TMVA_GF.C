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

void TMVA_GF ( const char* outFileName,
               const char* channel,
               int testSet=0 )
{
    (TMVA::gConfig().GetVariablePlotting()).fMaxNumOfAllowedVariablesForScatterPlots = 25;
    
    // options to control used methods
    bool useRandomSplitting = false; // option for cross validation
    bool useLikelihood = true;    // likelihood based discriminant
    bool useLikelihoodKDE = false;    // likelihood based discriminant
    bool useFischer = false;       // Fischer discriminant
    bool useMLP = false;          // Multi Layer Perceptron (old TMVA NN implementation)
    bool useBDT = false;           // Boosted Decision Tree (AdaBoost)
    bool useBDTG = false;         // BDT with GradBoost
    bool useDL = false;           // TMVA Deep Learning ( CPU or GPU)
    // bool useKeras = false;        // Keras Deep learning
    
    // Open files
    TString fileformat;
    TFile* sgnfile;
    TFile* bkgfile1;
    TFile* bkgfile2;
    TFile* bkgfile3;
    TFile* bkgfile4;
    TFile* bkgfile5;
    TFile* bkgfile6;
    TFile* bkgfile7;
    TFile* bkgfile8;
    TFile* bkgfile9;
    TFile* bkgfile10;
    // TFile* bkgfile11;
    // TFile* bkgfile12;
    if ( std::strcmp(channel, "phi") == 0 ) {
        //fileformat = "/work/submit/kyoon/RareHiggs/data/2023/AUG10pol/2018/outname_mc%d_GFcat_PhiCat_2018.root";
        fileformat = "/work/submit/mariadlf/SEPT29/2018/outname_mc%d_GFcat_PhiCat_2018.root";
        sgnfile = TFile::Open(Form(fileformat, 1017), "READ");
    } else if ( std::strcmp(channel, "rho") == 0 ) {
        //fileformat = "/work/submit/kyoon/RareHiggs/data/2023/AUG10pol/2018/outname_mc%d_GFcat_RhoCat_2018.root";
        fileformat = "/work/submit/mariadlf/SEPT29/2018/outname_mc%d_GFcat_RhoCat_2018.root";
        sgnfile = TFile::Open(Form(fileformat, 1027), "READ");
    } else if ( std::strcmp(channel, "k0star") == 0 ) {
        //fileformat = "/work/submit/kyoon/RareHiggs/data/2023/AUG10pol/2018/outname_mc%d_GFcat_K0StarCat_2018.root";
        fileformat = "/work/submit/mariadlf/SEPT29/2018/outname_mc%d_GFcat_K0StarCat_2018.root";
        sgnfile = TFile::Open(Form(fileformat, 1037), "READ");
    }
    bkgfile1 = TFile::Open(Form(fileformat, 10), "READ");
    bkgfile2 = TFile::Open(Form(fileformat, 11), "READ");
    bkgfile3 = TFile::Open(Form(fileformat, 12), "READ");
    bkgfile4 = TFile::Open(Form(fileformat, 13), "READ");
    bkgfile5 = TFile::Open(Form(fileformat, 14), "READ");
    bkgfile6 = TFile::Open(Form(fileformat, 15), "READ");
    bkgfile7 = TFile::Open(Form(fileformat, 16), "READ");
    bkgfile8 = TFile::Open(Form(fileformat, 17), "READ");
    bkgfile9 = TFile::Open(Form(fileformat, 18), "READ");
    bkgfile10 = TFile::Open(Form(fileformat, 19), "READ");
    // bkgfile11 = TFile::Open(Form(fileformat, -65), "READ");
    // bkgfile12 = TFile::Open(Form(fileformat, -66), "READ");
    
    // Initialize the dataset
    TFile* outfile = TFile::Open(outFileName, "RECREATE");    
    TMVA::DataLoader *dataloader = new TMVA::DataLoader("dataset");
    
    // Add variables to dataset
    dataloader->AddVariable("HCandMass", "HCandMass", "GeV/c^2", 'F'); // DON'T USE!
    
    // dataloader->AddVariable("goodMeson_isoNeuHad[index_pair[0]]", "meson_isoNeuHad", "", 'F');
    //  dataloader->AddVariable("HCandPT", "HCandPT", "", 'F');
    dataloader->AddVariable("HCandPT/HCandMass", "HCandPT__div_HCandMass", "", 'F'); // divide by HCandMass
    // dataloader->AddVariable("goodMeson_isoPho[index_pair[0]]", "goodMeson_isoPho", 'F');
        //  dataloader->AddVariable("goodPhotons_pt[index_pair[1]]", "photon_pt", "", 'F');
        // dataloader->AddVariable("goodPhotons_pt[index_pair[1]]/HCandPT", "photon_pt__div_HCandPT", "", 'F');
    dataloader->AddVariable("goodPhotons_pt[index_pair[1]]/HCandMass", "photon_pt__div_HCandMass", "", 'F'); 
        //  dataloader->AddVariable("goodMeson_pt[index_pair[0]]", "meson_pt", "", 'F');
        // dataloader->AddVariable("goodMeson_pt[index_pair[0]]/HCandPT", "meson_pt__div_HCandPT", "", 'F');
    dataloader->AddVariable("goodMeson_pt[index_pair[0]]/HCandMass", "meson_pt__div_HCandMass", "", 'F'); 
    dataloader->AddVariable("goodMeson_DR[index_pair[0]]", "meson_DR", "", 'F');
    
    // dataloader->AddVariable("goodPhotons_mvaID[index_pair[1]]", "photon_mvaID", "", 'F');
    //   dataloader->AddVariable("SoftActivityJetNjets5", "SoftActivityJetNjets5", "", 'F');
    // dataloader->AddVariable("DeepMETResolutionTune_pt", "DeepMETResolutionTune_pt", "GeV/c", 'F'); // high corr in VBF phi
    // dataloader->AddVariable("DeepMETResolutionTune_phi", "DeepMETResolutionTune_phi", "GeV/c", 'F'); // high corr in VBF phi
    dataloader->AddVariable("goodMeson_iso[index_pair[0]]", "meson_iso", "", 'F');
    //  dataloader->AddVariable("goodMeson_vtx_chi2dof[index_pair[0]]", "meson_vtx_chi2dof", "", 'F');
    //  dataloader->AddVariable("goodMeson_vtx_prob[index_pair[0]]", "meson_vtx_prob", "", 'F');
    //  dataloader->AddVariable("goodMeson_massErr[index_pair[0]]", "meson_massErr", "GeV/c^2", 'F');
    //    dataloader->AddVariable("goodMeson_mass[index_pair[0]]", "meson_mass", "GeV/c^2", 'F');
    // dataloader->AddVariable("goodMeson_sipPV[index_pair[0]]", "meson_sipPV", "", 'F');
    
    // dataloader->AddVariable("goodMeson_trk1_pt[index_pair[0]]", "meson_trk1_pt", "", 'F');
    //  dataloader->AddVariable("goodMeson_trk2_pt[index_pair[0]]", "meson_trk2_pt", "", 'F');
    //  dataloader->AddVariable("goodMeson_trk1_eta[index_pair[0]]", "meson_trk1_eta", "", 'F');
    //  dataloader->AddVariable("goodMeson_trk2_eta[index_pair[0]]", "meson_trk2_eta", "", 'F'); 
    //  dataloader->AddVariable("dPhiGammaMesonCand", "dPhiGammaMesonCand", "", 'F');
    //  dataloader->AddVariable("dEtaGammaMesonCand", "dEtaGammaMesonCand", "", 'F'); 
    //  dataloader->AddVariable("dPhiGammaMesonCand/HCandMass", "dPhiGammaMesonCand__div_HCandMass", "", 'F'); 
    //  dataloader->AddVariable("dEtaGammaMesonCand/HCandMass", "dEtaGammaMesonCand__div_HCandMass", "", 'F');  // high corr in VBF phi and VBFlow rho
 
    //  dataloader->AddVariable("nPhoton", "nPhotons", "", 'F');
    dataloader->AddVariable("nGoodJets", "nGoodJets", "", 'F');
    //  dataloader->AddVariable("sigmaHCandMass_Rel2", "sigmaHCandMass_Rel2", "", 'F');
    //  dataloader->AddVariable("goodPhotons_energyErr", "goodPhotons_energyErr", "", 'F');
    
    // Set weights
    dataloader->SetWeightExpression("(mc>=0 && mc<1000)? (w_allSF * lumiIntegrated / sigmaHCandMass_Rel2) : (w_allSF * lumiIntegrated * 1.5 * TMath::Sin(theta) * TMath::Sin(theta) / sigmaHCandMass_Rel2)");

    // Spectator used for split
    // dataloader->AddSpectator("Entry$", "eventID");

    // Apply split
    ////////////////////// TODO: use cross validation /////////////////////////
    const char* trainTreeEventSplitStr = Form("(Entry$ %% 3) >= %d", testSet);
    const char* testTreeEventSplitStr = Form("(Entry$ %% 3) == %d", testSet); // "(Entry$) >= 0"; 
    
    // Apply cuts
    const char* higgsMass_full = "HCandMass > 110 && HCandMass < 160";
    // const char* higgsMass_full = "HCandMass > 100 && HCandMass < 170";
    // const char* meson_sideband = "((goodMeson_mass[index_pair[0]] > 0.5) && (goodMeson_mass[index_pair[0]] < 0.62)) || ((goodMeson_mass[index_pair[0]] > 0.92) && (goodMeson_mass[index_pair[0]] < 1.00))";
    // const char* higgsMass = "HCandMass > 115 && HCandMass < 135";
    const char* nanRemove = "!TMath::IsNaN(goodMeson_massErr) && !TMath::IsNaN(sigmaHCandMass_Rel2)";
    
    TCut cutSignalTrain = Form("%s && %s && %s", trainTreeEventSplitStr, higgsMass_full, nanRemove);
    TCut cutBkgTrain = Form("%s && %s && %s", trainTreeEventSplitStr, higgsMass_full, nanRemove);
    TCut cutSignalTest = Form("%s && %s && %s", testTreeEventSplitStr, higgsMass_full, nanRemove);
    TCut cutBkgTest = Form("%s && %s && %s", testTreeEventSplitStr, higgsMass_full, nanRemove);

    // TCut cutSignalTrain = Form("%s && %s && %s && %s", trainTreeEventSplitStr, higgsMass_full, nanRemove, meson_sideband);
    // TCut cutBkgTrain = Form("%s && %s && %s && %s", trainTreeEventSplitStr, higgsMass_full, nanRemove, meson_sideband);
    // TCut cutSignalTest = Form("%s && %s && %s && %s", testTreeEventSplitStr, higgsMass_full, nanRemove, meson_sideband);
    // TCut cutBkgTest = Form("%s && %s && %s && %s", testTreeEventSplitStr, higgsMass_full, nanRemove, meson_sideband);
    
    // Register trees
    ///////////////////// TODO: add weight per event basis /////////////////////
    double signalWeight = 1.0;
    double backgroundWeight = 1.0;
    
    dataloader->AddTree((TTree*)sgnfile->Get("events"), "Signal", signalWeight, cutSignalTrain, "train");
    dataloader->AddTree((TTree*)bkgfile1->Get("events"), "Background", backgroundWeight, cutBkgTrain, "train");
    dataloader->AddTree((TTree*)bkgfile2->Get("events"), "Background", backgroundWeight, cutBkgTrain, "train");
    dataloader->AddTree((TTree*)bkgfile3->Get("events"), "Background", backgroundWeight, cutBkgTrain, "train");
    dataloader->AddTree((TTree*)bkgfile4->Get("events"), "Background", backgroundWeight, cutBkgTrain, "train");
    dataloader->AddTree((TTree*)bkgfile5->Get("events"), "Background", backgroundWeight, cutBkgTrain, "train");
    dataloader->AddTree((TTree*)bkgfile6->Get("events"), "Background", backgroundWeight, cutBkgTrain, "train");
    dataloader->AddTree((TTree*)bkgfile7->Get("events"), "Background", backgroundWeight, cutBkgTrain, "train");
    dataloader->AddTree((TTree*)bkgfile8->Get("events"), "Background", backgroundWeight, cutBkgTrain, "train");
    dataloader->AddTree((TTree*)bkgfile9->Get("events"), "Background", backgroundWeight, cutBkgTrain, "train");
    dataloader->AddTree((TTree*)bkgfile10->Get("events"), "Background", backgroundWeight, cutBkgTrain, "train");
    // dataloader->AddTree((TTree*)bkgfile11->Get("events"), "Background", backgroundWeight, cutBkgTrain, "train");
    // dataloader->AddTree((TTree*)bkgfile12->Get("events"), "Background", backgroundWeight, cutBkgTrain, "train");
    
    dataloader->AddTree((TTree*)sgnfile->Get("events"), "Signal", signalWeight, cutSignalTest, "test");
    dataloader->AddTree((TTree*)bkgfile1->Get("events"), "Background", backgroundWeight, cutBkgTest, "test");
    dataloader->AddTree((TTree*)bkgfile2->Get("events"), "Background", backgroundWeight, cutBkgTest, "test");
    dataloader->AddTree((TTree*)bkgfile3->Get("events"), "Background", backgroundWeight, cutBkgTest, "test");
    dataloader->AddTree((TTree*)bkgfile4->Get("events"), "Background", backgroundWeight, cutBkgTest, "test");
    dataloader->AddTree((TTree*)bkgfile5->Get("events"), "Background", backgroundWeight, cutBkgTest, "test");
    dataloader->AddTree((TTree*)bkgfile6->Get("events"), "Background", backgroundWeight, cutBkgTest, "test");
    dataloader->AddTree((TTree*)bkgfile7->Get("events"), "Background", backgroundWeight, cutBkgTest, "test");
    dataloader->AddTree((TTree*)bkgfile8->Get("events"), "Background", backgroundWeight, cutBkgTest, "test");
    dataloader->AddTree((TTree*)bkgfile9->Get("events"), "Background", backgroundWeight, cutBkgTest, "test");
    dataloader->AddTree((TTree*)bkgfile10->Get("events"), "Background", backgroundWeight, cutBkgTest, "test");
    // dataloader->AddTree((TTree*)bkgfile11->Get("events"), "Background", backgroundWeight, cutBkgTest, "test");
    // dataloader->AddTree((TTree*)bkgfile12->Get("events"), "Background", backgroundWeight, cutBkgTest, "test");
    
    TMVA::Factory factory("TMVAClassification", outfile, "!V:!Silent:Color:DrawProgressBar:AnalysisType=Classification"); //:Transformations=P,D");

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
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA01",
        //                    "!V:NTrees=1000:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.10:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA02",
        //                    "!V:NTrees=1000:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.15:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA03",
        //                    "!V:NTrees=1000:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.20:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA04",
        //                    "!V:NTrees=1000:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.25:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA05",
        //                    "!V:NTrees=1000:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.30:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA06",
        //                    "!V:NTrees=1000:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.35:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA07",
        //                    "!V:NTrees=1000:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.40:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA08",
        //                    "!V:NTrees=1000:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.45:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA11",
        //                    "!V:NTrees=800:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.10:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA12",
        //                    "!V:NTrees=800:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.15:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA13",
        //                    "!V:NTrees=800:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.20:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // TO training:
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA",
        //                    "!V:NTrees=800:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.25:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA15",
        //                    "!V:NTrees=800:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.30:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA16",
        //                    "!V:NTrees=800:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.35:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA17",
        //                    "!V:NTrees=800:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.40:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA18",
        //                    "!V:NTrees=800:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.45:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA21",
        //                    "!V:NTrees=600:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.10:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA22",
        //                    "!V:NTrees=600:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.15:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA23",
        //                    "!V:NTrees=600:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.20:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA24",
        //                    "!V:NTrees=600:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.25:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA25",
        //                    "!V:NTrees=600:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.30:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA26",
        //                    "!V:NTrees=600:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.35:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA27",
        //                    "!V:NTrees=600:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.40:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA28",
        //                    "!V:NTrees=600:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.45:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA31",
        //                    "!V:NTrees=400:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.10:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA32",
        //                    "!V:NTrees=400:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.15:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA33",
        //                    "!V:NTrees=400:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.20:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA34",
        //                    "!V:NTrees=400:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.25:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA35",
        //                    "!V:NTrees=400:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.30:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA36",
        //                    "!V:NTrees=400:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.35:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA37",
        //                    "!V:NTrees=400:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.40:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA38",
        //                    "!V:NTrees=400:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.45:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA41",
        //                    "!V:NTrees=200:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.10:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA42",
        //                    "!V:NTrees=200:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.15:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA43",
        //                    "!V:NTrees=200:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.20:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA44",
        //                    "!V:NTrees=200:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.25:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA45",
        //                    "!V:NTrees=200:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.30:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA46",
        //                    "!V:NTrees=200:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.35:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA47",
        //                    "!V:NTrees=200:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.40:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA48",
        //                    "!V:NTrees=200:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.45:NegWeightTreatment=IgnoreNegWeightsInTraining:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
        
    }

    if (useBDTG)
    {
        // rho
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG",
        //                    "!V:NTrees=600:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // k0star
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG",
        //                    "!V:NTrees=200:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.20:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // phi
        factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG",
                           "!V:NTrees=200:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG",
        //                    "!V:NTrees=600:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
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
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG51",
        //                    "!V:NTrees=100:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG52",
        //                    "!V:NTrees=100:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.15:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG53",
        //                    "!V:NTrees=100:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.20:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG54",
        //                    "!V:NTrees=100:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.25:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG55",
        //                    "!V:NTrees=100:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.30:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG56",
        //                    "!V:NTrees=100:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.35:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG57",
        //                    "!V:NTrees=100:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.40:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
        // factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG58",
        //                    "!V:NTrees=100:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.45:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=4:UseBaggedBoost:BaggedSampleFraction=0.5" );
    //     factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG2",
    //                        "!V:VarTransform=D:NTrees=115:BoostType=Grad:Shrinkage=0.075:MaxDepth=3:SeparationType=GiniIndex:nCuts=12:UseRandomisedTrees:UseNvars=12:UseBaggedBoost:BaggedSampleFraction=0.8" );
    //     factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG3",
    //                        "!V:NTrees=115:BoostType=Grad:Shrinkage=0.075:MaxDepth=3:SeparationType=GiniIndex:nCuts=12:UseRandomisedTrees:UseNvars=12:UseBaggedBoost:BaggedSampleFraction=0.8" );
    //     factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG4",
    //                        "!V:VarTransform=P,D:NTrees=800:BoostType=Grad:Shrinkage=0.25:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=20:UseBaggedBoost:BaggedSampleFraction=0.5:MinNodeSize=2.5%:NegWeightTreatment=IgnoreNegWeightsInTraining" );
    //     factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG5",
    //                        "!V:VarTransform=D:NTrees=800:BoostType=Grad:Shrinkage=0.25:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=20:UseBaggedBoost:BaggedSampleFraction=0.5:MinNodeSize=2.5%:NegWeightTreatment=IgnoreNegWeightsInTraining" );
    //     factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG6",
    //                        "!V:NTrees=800:BoostType=Grad:Shrinkage=0.25:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=20:UseBaggedBoost:BaggedSampleFraction=0.5:MinNodeSize=2.5%:NegWeightTreatment=IgnoreNegWeightsInTraining" );
    //     factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG_depth4_with_pruning",
    //                        "!V:VarTransform=P,D:NTrees=100:BoostType=Grad:Shrinkage=0.06:MaxDepth=4:SeparationType=GiniIndex:nCuts=15:UseRandomisedTrees:UseNvars=12:UseBaggedBoost:BaggedSampleFraction=0.8:PruneMethod=CostComplexity:PruneStrength=80" );
    //     factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG",
    //                        "!V:VarTransform=P,D:NTrees=115:BoostType=Grad:Shrinkage=0.075:MaxDepth=3:SeparationType=GiniIndex:nCuts=12:UseRandomisedTrees:UseNvars=12:UseBaggedBoost:BaggedSampleFraction=0.8:PruneMethod=NoPruning" );
    //     factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG_d3",
    //                       "!V:NTrees=600:BoostType=Grad:Shrinkage=0.1:MaxDepth=3:SeparationType=GiniIndex:nCuts=20:UseRandomisedTrees:UseNvars=8:UseBaggedBoost:BaggedSampleFraction=0.6:PruneMethod=CostComplexity:PruneStrength=60" );
    //     factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG__rho",
    //                      "!V:NTrees=100:BoostType=Grad:Shrinkage=0.1:MaxDepth=2:SeparationType=GiniIndex:nCuts=30:UseRandomisedTrees:UseNvars=8:UseBaggedBoost:BaggedSampleFraction=0.15" );
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
        TString inputLayoutString = "InputLayout=1|1|14";
        TString batchLayoutString= "BatchLayout=1|128|14";
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
    // cv.Evaluate();
 
    // after we get the ROC curve and we display
    // auto c1 = factory.GetROCCurve(dataloader);
    // c1->Draw();
}
