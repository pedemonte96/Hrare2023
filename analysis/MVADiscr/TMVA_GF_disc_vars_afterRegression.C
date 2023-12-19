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

void TMVA_GF_disc_vars_afterRegression(const char* outFileName, const char* channel, int testSet=0, int codeVars = 4194303){

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
    TString fileformatBkg;
    TFile* sgnfile0;
    TFile* sgnfile1;
    TFile* sgnfile2;
    TFile* bkgfile;
    int mesonNum;

    if(std::strcmp(channel, "omega") == 0 || std::strcmp(channel, "o") == 0){
        fileformat = "/data/submit/pdmonte/outputs/NOV05/2018/outname_mc%d_GFcat_OmegaCat_2018_sample%d_after.root";
        fileformatBkg = "/data/submit/pdmonte/outputs/NOV05/2018/outname_mc0_GFcat_OmegaCat_2018_after.root";
        mesonNum = 1038;
    }else if(std::strcmp(channel, "phi") == 0 || std::strcmp(channel, "phi3") == 0 || std::strcmp(channel, "p") == 0){
        fileformat = "/data/submit/pdmonte/outputs/NOV05/2018/outname_mc%d_GFcat_Phi3Cat_2018_sample%d_after.root";
        fileformatBkg = "/data/submit/pdmonte/outputs/NOV05/2018/outname_mc0_GFcat_Phi3Cat_2018_after.root";
        mesonNum = 1039;
    }else if(std::strcmp(channel, "d0starrho") == 0 || std::strcmp(channel, "dr") == 0){
        fileformat = "/data/submit/pdmonte/outputs/NOV05/2018/outname_mc%d_GFcat_D0StarRhoCat_2018_sample%d_after.root";
        fileformatBkg = "/data/submit/pdmonte/outputs/NOV05/2018/outname_mc0_GFcat_D0StarRhoCat_2018_after.root";
        mesonNum = 1040;
    }else if(std::strcmp(channel, "d0star") == 0 || std::strcmp(channel, "d") == 0){
        fileformat = "/data/submit/pdmonte/outputs/NOV05/2018/outname_mc%d_GFcat_D0StarCat_2018_sample%d_after.root";
        fileformatBkg = "/data/submit/pdmonte/outputs/NOV05/2018/outname_mc0_GFcat_D0StarCat_2018_after.root";
        mesonNum = 1041;
    }else
        return -1;

    sgnfile0 = TFile::Open(Form(fileformat, mesonNum, 0), "READ");
    sgnfile1 = TFile::Open(Form(fileformat, mesonNum, 1), "READ");
    sgnfile2 = TFile::Open(Form(fileformat, mesonNum, 2), "READ");
    bkgfile = TFile::Open(fileformatBkg, "READ");


    // Initialize the dataset
    TFile* outfile = TFile::Open(Form("/data/submit/pdmonte/TMVA_disc/rootVars/%s", Form("%s_%s_GF_%d_%d.root", outFileName, channel, codeVars, testSet)), "RECREATE");    
    //TFile* outfile = TFile::Open(Form("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/MVADiscr/rootVars/%s", Form("%s_%s_GF_%d.root", outFileName, channel, testSet)), "RECREATE");    
    TMVA::DataLoader *dataloader = new TMVA::DataLoader("dataset");

    // Add variables to dataset (REVISIT)
    if (codeVars % 2) {dataloader->AddVariable("goodMeson_iso[0]", "goodMeson_iso", "", 'F');}               codeVars /= 2;
    if (codeVars % 2) {dataloader->AddVariable("phi_isoNeuHad[0]", "phi_isoNeuHad", "", 'F');}                    codeVars /= 2;
    if (codeVars % 2) {dataloader->AddVariable("Tau_rawDeepTau2017v2p1VSjet[0]", "Tau_rawDeepTau2017v2p1VSjet", "", 'F');}           codeVars /= 2;
    if (codeVars % 2) {dataloader->AddVariable("var0_input_pred", "var0_input_pred", "", 'F');}                               codeVars /= 2;
    if (codeVars % 2) {dataloader->AddVariable("SV_pt[0]", "SV_pt", "", 'F');}                           codeVars /= 2;
    if (codeVars % 2) {dataloader->AddVariable("var3_input_pred", "var3_input_pred", "GeV/c", 'F');}      codeVars /= 2;
    if (codeVars % 2) {dataloader->AddVariable("Tau_rawIso[0]", "Tau_rawIso", "", 'F');}                                  codeVars /= 2;
    if (codeVars > 0) {cout << "codeVars greater than expected!" << endl; return -1;}


    // Set weights. This is what creates the Signal/Background classes
    dataloader->SetWeightExpression("w * lumiIntegrated / sigmaHCandMass_Rel2");

    // Spectator used for split
    // dataloader->AddSpectator("Entry$", "eventID");
    //dataloader->AddVariable("HCandMass", "HCandMass", "", 'F');
    //dataloader->AddVariable("goodMeson_mass[0]", "meson_mass", "", 'F');
    dataloader->AddSpectator("w", "w");
    dataloader->AddSpectator("lumiIntegrated", "lumiIntegrated");
    dataloader->AddSpectator("scale", "scale");
    dataloader->AddSpectator("HCandMass", "HCandMass");
    dataloader->AddSpectator("HCandMass_varPRED", "HCandMass_varPRED");

    // Apply split
    ////////////////////// TODO: use cross validation /////////////////////////
    const char* trainTreeEventSplitStr = Form("(Entry$ %% 3) != %d", testSet);
    const char* testTreeEventSplitStr = Form("(Entry$ %% 3) == %d", testSet);
    
    // Apply cuts
    const char* higgsMass_full = "HCandMass > 100 && HCandMass < 160";
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
    dataloader->AddTree((TTree*)sgnfile0->Get("events"), "Signal", signalWeight, cutSignalTrain, "train");
    dataloader->AddTree((TTree*)sgnfile1->Get("events"), "Signal", signalWeight, cutSignalTrain, "train");
    dataloader->AddTree((TTree*)sgnfile2->Get("events"), "Signal", signalWeight, cutSignalTrain, "train");
    dataloader->AddTree((TTree*)bkgfile->Get("events"), "Background", backgroundWeight, cutBkgTrain, "train");
    
    //Load test data with the cuts
    cout << "\033[1;35mStart to add the data to the test set\033[0m" << endl;
    dataloader->AddTree((TTree*)sgnfile0->Get("events"), "Signal", signalWeight, cutSignalTest, "test");
    dataloader->AddTree((TTree*)sgnfile1->Get("events"), "Signal", signalWeight, cutSignalTest, "test");
    dataloader->AddTree((TTree*)sgnfile2->Get("events"), "Signal", signalWeight, cutSignalTest, "test");
    dataloader->AddTree((TTree*)bkgfile->Get("events"), "Background", backgroundWeight, cutBkgTest, "test");

    // Preparing trees
    cout << "\033[1;36m------------------------------------------ PREPARING TREES ------------------------------------------\033[0m" << endl;
    
    TString prepareOptions = "!V:SplitMode=Random:NormMode=None:MixMode=Random";
    dataloader->PrepareTrainingAndTestTree("", prepareOptions);
    
    cout << "\033[1;36m---------------------------------------------- FACTORY ----------------------------------------------\033[0m" << endl;
    
    TMVA::Factory factory("TMVAClassification", outfile, "!V:!Silent:Color:DrawProgressBar=F:AnalysisType=Classification");

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
