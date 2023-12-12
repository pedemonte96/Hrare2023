#include <string.h>
#include <time.h>
#include <vector>

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

using namespace TMVA;

void TMVA_GF_disc(const char* outFileName, const char* channel, int testSet=0){

    time_t start_t;
    struct tm * timeinfo;
    time (&start_t);
    timeinfo = localtime(&start_t);
    printf("Staring: %s", asctime(timeinfo));

    (TMVA::gConfig().GetVariablePlotting()).fMaxNumOfAllowedVariablesForScatterPlots = 80;
    (TMVA::gConfig().GetIONames()).fWeightFileDir = "../../../../../../../../../data/submit/pdmonte/TMVA_disc/weights";
        
    // options to control used methods
    bool useLikelihood = true;    // likelihood based discriminant
    bool useLikelihoodKDE = false;    // likelihood based discriminant
    bool useFischer = false;       // Fischer discriminant
    bool useMLP = false;          // Multi Layer Perceptron (old TMVA NN implementation)
    bool useBDT = false;           // Boosted Decision Tree (AdaBoost)
    bool useBDTG = true;         // BDT with GradBoost
    
    // Open files
    TString fileformat;
    TFile* sgnfile;
    TFile* bkgfile1;
    TFile* bkgfile2;
    TFile* bkgfile3;
    TFile* bkgfile4;
    TFile* bkgfile5;

    if(std::strcmp(channel, "omega") == 0 || std::strcmp(channel, "o") == 0){
        fileformat = "/data/submit/pdmonte/outputs/NOV05/2018/outname_mc%d_GFcat_OmegaCat_2018.root";
        sgnfile = TFile::Open(Form(fileformat, 1038), "READ");
    }else if(std::strcmp(channel, "phi") == 0 || std::strcmp(channel, "phi3") == 0 || std::strcmp(channel, "p") == 0){
        fileformat = "/data/submit/pdmonte/outputs/NOV05/2018/outname_mc%d_GFcat_Phi3Cat_2018.root";
        sgnfile = TFile::Open(Form(fileformat, 1039), "READ");
    }else if(std::strcmp(channel, "d0starrho") == 0 || std::strcmp(channel, "dr") == 0){
        fileformat = "/data/submit/pdmonte/outputs/NOV05/2018/outname_mc%d_GFcat_D0StarRhoCat_2018.root";
        sgnfile = TFile::Open(Form(fileformat, 1040), "READ");
    }else if(std::strcmp(channel, "d0star") == 0 || std::strcmp(channel, "d") == 0){
        fileformat = "/data/submit/pdmonte/outputs/NOV05/2018/outname_mc%d_GFcat_D0StarCat_2018.root";
        sgnfile = TFile::Open(Form(fileformat, 1041), "READ");
    }else
        return -1;

    bkgfile1 = TFile::Open(Form(fileformat, 10), "READ");
    bkgfile2 = TFile::Open(Form(fileformat, 11), "READ");
    bkgfile3 = TFile::Open(Form(fileformat, 12), "READ");
    bkgfile4 = TFile::Open(Form(fileformat, 13), "READ");
    bkgfile5 = TFile::Open(Form(fileformat, 14), "READ");


    // Initialize the dataset
    TFile* outfile = TFile::Open(Form("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/MVADiscr/rootVars/%s", Form("%s_%s_GF_%d.root", outFileName, channel, testSet)), "RECREATE");    
    TMVA::DataLoader *dataloader = new TMVA::DataLoader("dataset");

    // Add variables to dataset (REVISIT)
    dataloader->AddVariable("HCandPT/HCandMass", "HCandPT__div_HCandMass", "", 'F');
    dataloader->AddVariable("goodMeson_pt[0]/HCandPT", "meson_pt__div_HCandPT", "", 'F');
    ////dataloader->AddVariable("goodMeson_ditrk_pt[0]/HCandPT", "meson_pt__div_HCandPT", "", 'F');
    dataloader->AddVariable("goodPhotons_eta[0]", "photon_eta", "", 'F');
    dataloader->AddVariable("goodPhotons_mvaID[0]", "photon_mvaID", "", 'F');
    dataloader->AddVariable("DeepMETResolutionTune_pt", "DeepMETResolutionTune_pt", "GeV/c", 'F'); // high corr in VBF phi
    dataloader->AddVariable("goodMeson_iso[0]", "meson_iso", "", 'F');
    dataloader->AddVariable("goodMeson_trk2_phi[0]", "meson_trk2_phi", "", 'F');
    dataloader->AddVariable("dEtaGammaMesonCand/HCandMass", "dEtaGammaMesonCand__div_HCandMass", "", 'F');  // high corr in VBF phi and VBFlow rho
    dataloader->AddVariable("nGoodJets", "nGoodJets", "", 'F');
    dataloader->AddVariable("goodMeson_DR", "meson_DR", "", 'F');
    dataloader->AddVariable("goodMeson_vtx_chi2dof", "goodMeson_vtx_chi2dof", "", 'F');
    ////dataloader->AddVariable("goodMeson_vtx_prob", "goodMeson_vtx_prob", "", 'F');
    dataloader->AddVariable("goodMeson_sipPV[0]", "meson_sipPV", "", 'F');
    dataloader->AddVariable("goodMeson_bestVtx_idx[0]", "meson_bestVtx_idx", "", 'F');
    dataloader->AddVariable("goodMeson_bestVtx_X[0]", "meson_bestVtx_X", "", 'F');
    dataloader->AddVariable("goodMeson_bestVtx_Y[0]", "meson_bestVtx_Y", "", 'F');
    dataloader->AddVariable("goodMeson_bestVtx_Z[0]", "meson_bestVtx_Z", "", 'F');
    dataloader->AddVariable("goodMeson_bestVtx_R[0]", "meson_bestVtx_R", "", 'F');
    dataloader->AddVariable("delta_eta_goodMeson_ditrk_goodPhoton_input_pred", "delta_eta_goodMeson_ditrk_goodPhoton_input_pred", "", 'F');
    //dataloader->AddVariable("delta_phi_goodMeson_ditrk_goodPhoton_input_pred", "delta_phi_goodMeson_ditrk_goodPhoton_input_pred", "", 'F');
    dataloader->AddVariable("var0_input_pred", "var0", "", 'F');
    dataloader->AddVariable("goodPhotons_pt[0]", "goodPhotons_pt", "", 'F');


    // Set weights. This is what creates the Signal/Background classes
    dataloader->SetWeightExpression("w / sigmaHCandMass_Rel2");

    // Spectator used for split
    // dataloader->AddSpectator("Entry$", "eventID");
    //dataloader->AddVariable("HCandMass", "HCandMass", "", 'F');
    //dataloader->AddVariable("goodMeson_mass[0]", "meson_mass", "", 'F');

    // Apply split
    ////////////////////// TODO: use cross validation /////////////////////////
    const char* trainTreeEventSplitStr = Form("(Entry$ %% 3) != %d", testSet);
    const char* testTreeEventSplitStr = Form("(Entry$ %% 3) == %d", testSet);
    
    // Apply cuts
    const char* higgsMass_full = "HCandMass > 110 && HCandMass < 160";
    // const char* higgsMass = "HCandMass > 115 && HCandMass < 135";
    const char* nanRemove = "!TMath::IsNaN(goodMeson_massErr) && !TMath::IsNaN(sigmaHCandMass_Rel2)";
    
    TCut cutSignalTrain = Form("%s && %s && %s", trainTreeEventSplitStr, higgsMass_full, nanRemove);
    TCut cutBkgTrain = Form("%s && %s && %s", trainTreeEventSplitStr, higgsMass_full, nanRemove);
    TCut cutSignalTest = Form("%s && %s && %s", testTreeEventSplitStr, higgsMass_full, nanRemove);
    TCut cutBkgTest = Form("%s && %s && %s", testTreeEventSplitStr, higgsMass_full, nanRemove);
    
    // Register trees
    ///////////////////// TODO: add weight per event basis /////////////////////
    double signalWeight = 1.0;
    double backgroundWeight = 1.0;
    cout << "\033[1;36m -------------------------------------- ADD TREES -------------------------------------- \033[0m" << endl;
    cout << "\033[1;35mStart to add the data to the train set\033[0m" << endl;
    //Load train data with the cuts
    dataloader->AddTree((TTree*)sgnfile->Get("events"), "Signal", signalWeight, cutSignalTrain, "train");
    dataloader->AddTree((TTree*)bkgfile1->Get("events"), "Background", backgroundWeight, cutBkgTrain, "train");
    dataloader->AddTree((TTree*)bkgfile2->Get("events"), "Background", backgroundWeight, cutBkgTrain, "train");
    dataloader->AddTree((TTree*)bkgfile3->Get("events"), "Background", backgroundWeight, cutBkgTrain, "train");
    dataloader->AddTree((TTree*)bkgfile4->Get("events"), "Background", backgroundWeight, cutBkgTrain, "train");
    dataloader->AddTree((TTree*)bkgfile5->Get("events"), "Background", backgroundWeight, cutBkgTrain, "train");
    
    //Load test data with the cuts
    cout << "\033[1;35mStart to add the data to the test set\033[0m" << endl;
    dataloader->AddTree((TTree*)sgnfile->Get("events"), "Signal", signalWeight, cutSignalTest, "test");
    dataloader->AddTree((TTree*)bkgfile1->Get("events"), "Background", backgroundWeight, cutBkgTest, "test");
    dataloader->AddTree((TTree*)bkgfile2->Get("events"), "Background", backgroundWeight, cutBkgTest, "test");
    dataloader->AddTree((TTree*)bkgfile3->Get("events"), "Background", backgroundWeight, cutBkgTest, "test");
    dataloader->AddTree((TTree*)bkgfile4->Get("events"), "Background", backgroundWeight, cutBkgTest, "test");

    // Preparing trees
    cout << "\033[1;36m------------------------------------------ PREPARING TREES ------------------------------------------\033[0m" << endl;
    
    TString prepareOptions = "!V:SplitMode=Random:NormMode=None:MixMode=Random";
    dataloader->PrepareTrainingAndTestTree("", prepareOptions);
    
    cout << "\033[1;36m---------------------------------------------- FACTORY ----------------------------------------------\033[0m" << endl;
    
    TMVA::Factory factory("TMVAClassification", outfile, "!V:!Silent:Color:DrawProgressBar:AnalysisType=Classification");

   // Booking Methods ------------------------------------------------------------------------------------
 
    // Likelihood ("naive Bayes estimator")
    if (useLikelihood){
        factory.BookMethod(dataloader,TMVA::Types::kLikelihood, "Likelihood", "H:!V:TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmoothBkg[1]=10:NSmooth=1:NAvEvtPerBin=50" );
    }
    // Use a kernel density estimator to approximate the PDFs
    if (useLikelihoodKDE){
        factory.BookMethod(dataloader,TMVA::Types::kLikelihood, "LikelihoodKDE", "!H:!V:!TransformOutput:PDFInterpol=KDE:KDEtype=Gauss:KDEiter=Adaptive:KDEFineFactor=0.3:KDEborder=None:NAvEvtPerBin=50" );
    }
 
    // Fisher discriminant (same as LD)
    if (useFischer){
        factory.BookMethod(dataloader,TMVA::Types::kFisher, "Fisher", "H:!V:Fisher:VarTransform=None:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:NbinsMVAPdf=50:NsmoothMVAPdf=10" );
    }
 
    // Boosted Decision Trees
    if (useBDT){
        //factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA_d2_t200", "!V:NTrees=200:MinNodeSize=2.5%:MaxDepth=2:BoostType=AdaBoost:AdaBoostBeta=0.1:UseBaggedBoost:BaggedSampleFraction=0.01:SeparationType=GiniIndex:nCuts=30" );
        factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA", "!V:VarTransform=D:NTrees=115:MinNodeSize=5:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.7:SeparationType=GiniIndex:nCuts=12" );
        //factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTA_d4_t60", "!V:NTrees=80:MinNodeSize=2.5%:MaxDepth=4:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );
    }

    if (useBDTG){
        factory.BookMethod(dataloader,TMVA::Types::kBDT, "BDTG150", "!V:VarTransform=P,D:NTrees=150:BoostType=Grad:Shrinkage=0.07:MaxDepth=5:SeparationType=GiniIndex:nCuts=24:UseRandomisedTrees:UseNvars=24:UseBaggedBoost:BaggedSampleFraction=0.7:PruneMethod=NoPruning" );
    }
 
    // Multi-Layer Perceptron (Neural Network)
    if (useMLP){
        factory.BookMethod(dataloader,TMVA::Types::kMLP, "MLP", "!H:!V:NeuronType=tanh:VarTransform=N:NCycles=100:HiddenLayers=N+5:TestRate=5:UseRegulator" );
    }
 
    // Train Methods: Here we train all the previously booked methods.
    cout << "\033[1;36m -------------------------------------- TRAINING... -------------------------------------- \033[0m" << endl;
    factory.TrainAllMethods();
 
    // Test  all methods: Now we test and evaluate all methods using the test data set.
    cout << "\033[1;36m -------------------------------------- TESTING -------------------------------------- \033[0m" << endl;
    factory.TestAllMethods();
    cout << "\033[1;36m -------------------------------------- EVALUATING -------------------------------------- \033[0m" << endl;
    factory.EvaluateAllMethods();

    outfile->Close();
    std::cout << "==> Wrote root file: " << outfile->GetName() << std::endl;

    // cv.Evaluate();
 
    // after we get the ROC curve and we display
    // auto c1 = factory.GetROCCurve(dataloader);
    // c1->Draw();

    time_t end_t;
    time (&end_t);
    double diff_t = difftime(end_t, start_t);
    printf("Execution time: %d seconds\n", (int)diff_t);

    cout << "\033[1;36m -------------------------------------- DONE -------------------------------------- \033[0m" << endl;
}
